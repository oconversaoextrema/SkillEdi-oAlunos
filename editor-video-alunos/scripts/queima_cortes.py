"""Queima de filme (film burn) em todos os cortes de cena de um vídeo já renderizado.

    python work/queima_cortes.py entrada.mp4 cortes.json saida.mp4 --overlay meu-overlay.mp4 [--picos 10.05,13.35,...]

cortes.json = {"cortes": [3.17, 5.87, ...], "dur": 76.4}   (tempos em segundos, já na grade de 1/30 s)

O overlay é do aluno (vídeo de queimas de luz sobre fundo preto — não vem com a skill). Cada corte recebe uma queima
diferente, com o pico de luz alinhado no corte, misturada em modo TELA (screen): o preto some, só a luz aparece.
Overlay deitado (16:9) num vídeo em pé é girado 90° para caber inteiro (recortar o meio vira só um clarão branco).

Sem --picos, o script acha sozinho os picos de luz do overlay (média de brilho por quadro). Prefira passar só as
queimas que têm formato (borda de luz varrendo) — as que viram branco chapado ficam feias.
"""
import argparse, json, subprocess
from ambiente import FFMPEG, FFPROBE

ANTES, DEPOIS = 0.40, 0.45   # janela da queima em volta do pico
FORCA = 0.88                 # intensidade (1 = pico vira branco total)


def medida(arq):
    r = subprocess.run([FFPROBE, '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height',
                        '-of', 'csv=p=0', arq], capture_output=True, text=True, check=True)
    w, h = r.stdout.strip().split(',')[:2]
    return int(w), int(h)


def achar_picos(ov, limiar=120.0, min_dist=0.8):
    """picos de brilho do overlay: só quadros quase brancos (média > limiar) contam — vinheta e logo do canal ficam de fora."""
    w, h = 64, 36
    r = subprocess.run([FFMPEG, '-v', 'error', '-i', ov, '-vf', f'scale={w}:{h},format=gray,fps=30', '-f', 'rawvideo', '-'],
                       capture_output=True, check=True)
    n = len(r.stdout) // (w * h)
    medias = [sum(r.stdout[i * w * h:(i + 1) * w * h]) / (w * h) for i in range(n)]
    picos, ult = [], -10.0
    for i in range(30, n - 30):
        m = medias[i]
        if m > limiar and m >= max(medias[i - 6:i + 7]) and i / 30 - ult > min_dist:
            picos.append(round(i / 30, 2)); ult = i / 30
    return picos


def aplicar(ent, cortes, sai, dur, ov, picos):
    W, H = medida(ent)
    ow, oh = medida(ov)
    girar = 'transpose=1,' if (ow > oh) != (W > H) else ''
    fc = [f'color=c=black:s={W}x{H}:r=30:d={dur:.3f},format=yuv420p[b0]']
    passo = 3 if len(picos) > 3 else 1
    for k, t in enumerate(cortes):
        p = picos[(k * passo) % len(picos)]   # pula de 3 em 3: queimas vizinhas no arquivo não caem em cortes seguidos
        fc.append(f'[1:v]trim=start={max(p - ANTES, 0):.3f}:duration={ANTES + DEPOIS:.3f},setpts=PTS-STARTPTS,fps=30,'
                  f'{girar}scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,format=yuv420p,'
                  f'setpts=PTS+{max(t - ANTES, 0):.3f}/TB[q{k}]')
        fc.append(f'[b{k}][q{k}]overlay=eof_action=pass[b{k + 1}]')
    fc.append(f'[b{len(cortes)}]format=gbrp,colorchannelmixer=rr={FORCA}:gg={FORCA}:bb={FORCA}[ov]')
    fc.append('[0:v]format=gbrp[base];[base][ov]blend=all_mode=screen:shortest=1,format=yuv420p[v]')
    subprocess.run([FFMPEG, '-v', 'error', '-y', '-i', ent, '-i', ov, '-filter_complex', ';'.join(fc), '-map', '[v]',
                    '-map', '0:a?', '-c:v', 'libx264', '-crf', '14', '-preset', 'medium', '-pix_fmt', 'yuv420p',
                    '-c:a', 'copy', sai], check=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('entrada'); ap.add_argument('cortes'); ap.add_argument('saida')
    ap.add_argument('--overlay', required=True)
    ap.add_argument('--picos', help='segundos dos picos de luz no overlay, separados por vírgula')
    a = ap.parse_args()
    c = json.load(open(a.cortes))
    picos = [float(x) for x in a.picos.split(',')] if a.picos else achar_picos(a.overlay)
    if not picos:
        raise SystemExit('não achei queimas no overlay — passe --picos')
    aplicar(a.entrada, c['cortes'], a.saida, c['dur'], a.overlay, picos)
    print('ok', a.saida, len(c['cortes']), 'queimas', '| picos usados:', picos)
