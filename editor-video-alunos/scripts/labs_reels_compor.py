# -*- coding: utf-8 -*-
"""Montagem do REELS no estilo LABS (references/padrao-tessmann-reels-labs.md), 1080x1920: alterna três modos —
R = pessoa em tela cheia, M = motion em tela cheia, D = dividida NORMAL (metade de cima do motion, 1080x960, e a
pessoa na metade de baixo, 1080x960, com uma sombra suave na emenda). Punch-in alternado na pessoa, transições (clarão
leitoso pessoa→motion e em capítulo, chicote motion→motion, desfoque →pessoa), ACABAMENTO só no motion (retícula a 45°
nos tons médios, aberração, glow, grão mínimo, vinheta) e áudio (voz + trilha baixa contínua + efeitos). Som das
transições (aprovado 03/11/2026): clique "mágico" no clarão e clique "orgânico" (5 variações) no chicote e no desfoque,
todos os efeitos a −6 dB (sfx_ganho 0,5).

uso:  python work/labs_reels_compor.py work/<video>/labs-reels.json [--quadros t1,t2,...]

labs-reels.json:
{
  "pessoa": "work/<video>/base.mp4",          vídeo da pessoa já cortado, 1080x1920 (com a voz)
  "metade": "work/<video>/metade.mp4",        (opcional, recomendado se o bruto é DEITADO) vídeo 1080x960 da pessoa
                                              enquadrada pra metade de baixo, tirado do quadro deitado (mais folga que
                                              cortar do vertical): cabeça inteira, rosto a ~1/3 da altura
  "metade_topo": 200,                         (sem "metade") linha do vídeo 1080x1920 onde começa a faixa 1080x960:
                                              ~150 px acima do alto da cabeça. Padrão: centro[1] - 400
  "motion": "work/<video>/motion.mp4",        render do HyperFrames (modelo hyperframes-labs-reels), MESMA duração
  "saida": "saidas/<titulo>.mp4",
  "cenas": [[0, 4.5, "D", 0], [4.5, 6.3, "R", 0], [14.3, 16, "M", 1]],   [início, fim, modo R/M/D, capítulo? 1/0];
                                              o que não estiver listado é R
  "cortes": [12.3, 40.1],                     (opcional) cortes do vídeo da pessoa, pra trocar o punch-in
  "centro": [540, 600],                       (opcional) ponto do zoom na tela cheia (rosto)
  "trilha": "trilhas/<musica>.mp3",           (opcional) trilha contínua, ~16 dB abaixo da voz
  "nivel_trilha": 0.16,
  "efeitos_dir": "trilhas/efeitos",           (opcional) pasta dos .wav. click-organico.wav (clique com reverb, 5 variações
                                              em 0 / 1,4 / 2,65 / 4,25 / 5,7 s) e click-magico.wav (clique de menu), das
                                              transições, já vêm na skill em assets/efeitos; o aluno pode trocar pondo um
                                              de mesmo nome nessa pasta. Os outros (pop, tick, click, sucesso…) são opcionais
  "efeitos": [[0.9, "pop", 0.3], [3.8, "magico", 0.3], [5.3, "organico", 1.3]],
                                              [tempo, nome do .wav sem extensão (ou "organico"/"magico"), ganho]
  "sfx_ganho": 0.5                            (opcional) multiplica TODOS os efeitos e transições (0,5 = −6 dB)
}"""
import os, sys, json, subprocess, wave
from pathlib import Path
import numpy as np, cv2, av
sys.path.insert(0, str(Path(__file__).resolve().parent))
from ambiente import FFMPEG as FF

CFG = json.loads(Path(sys.argv[1]).read_text())
FPS, W, H = 30, 1080, 1920
PESSOA, MOTION = CFG['pessoa'], CFG['motion']
_s = av.open(PESSOA).streams.video[0]
DUR = float(_s.duration * _s.time_base)
N = int(round(DUR * FPS))
qm = lambda t: int(round(t * FPS))
SEG = sorted(CFG['cenas'])
MODO = np.array(['R'] * N, dtype='<U1')
for a, b, m, _ in SEG: MODO[qm(a):qm(b)] = m
CAP = {qm(a) for a, b, m, c in SEG if c}

# punch-in: alterna 1,0 / 1,1 a cada corte da pessoa e a cada troca de modo
cortes = {qm(c) for c in CFG.get('cortes', []) if c < DUR}
escala = np.ones(N); k = 0; ultimo = -99
for i in range(N):
    if (i in cortes or (i and MODO[i] != MODO[i - 1])) and i - ultimo > 20: k += 1; ultimo = i
    escala[i] = (1.0, 1.1)[k % 2]
TR = {}
for i in range(1, N):
    if MODO[i] == MODO[i - 1] and i not in CAP and not (MODO[i] != 'R' and any(qm(a) == i for a, *_ in SEG)): continue
    if MODO[i] == 'R': TR[i] = 'blur'
    elif i in CAP or MODO[i - 1] == 'R': TR[i] = 'clarao'
    else: TR[i] = 'whip'
CX, CY = CFG.get('centro', [540, 600])
MT = int(min(max(CFG.get('metade_topo', CY - 400), 0), H - 960))
METADE = CFG.get('metade')

def zoom(img, s, cx, cy):
    if s == 1: return img
    M = np.float32([[s, 0, cx - s * cx], [0, s, cy - s * cy]])
    return cv2.warpAffine(img, M, (img.shape[1], img.shape[0]), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)

def prepara(Hh):   # grades do acabamento pra uma altura (tela cheia 1920 ou metade 960)
    yy, xx = np.mgrid[0:Hh, 0:W].astype(np.float32)
    u, v = (xx + yy) / np.sqrt(2), (xx - yy) / np.sqrt(2); P = 5.0
    d = np.hypot((u % P) - P / 2, (v % P) - P / 2)
    dot = (np.exp(-(d / 1.55) ** 2) - .5).astype(np.float32)[..., None]
    vin = (1 - .18 * np.clip(((xx - W / 2) ** 2 / (W * .62) ** 2 + (yy - Hh / 2) ** 2 / (Hh * .62) ** 2) - .35, 0, 1))[..., None].astype(np.float32)
    return dot, vin
GR = {1920: prepara(1920), 960: prepara(960)}
rng = np.random.default_rng(3)
def acabamento(img):
    Hh = img.shape[0]; DOT, VIN = GR[Hh]
    f = img.astype(np.float32) / 255
    f = cv2.GaussianBlur(f, (0, 0), .6)
    hl = cv2.GaussianBlur(np.clip(f - .68, 0, 1), (0, 0), 8); f = f + hl * .35
    b, g, r = cv2.split(f)
    def esc(c, s, dx): return cv2.warpAffine(c, np.float32([[s, 0, W / 2 * (1 - s) + dx], [0, s, Hh / 2 * (1 - s)]]), (W, Hh), borderMode=cv2.BORDER_REPLICATE)
    f = cv2.merge([esc(b, .998, -1.0), g, esc(r, 1.002, 1.0)])
    w = np.clip((f - .08) / .25, 0, 1) * np.clip((.97 - f) / .15, 0, 1)   # retícula só nos tons médios
    f = (f + .16 * DOT * w) * VIN
    f = f + rng.normal(0, .004, (Hh, W, 1)).astype(np.float32)
    return np.clip(f * 255, 0, 255).astype(np.uint8)

# dividida normal: a pessoa na metade de baixo, com uma sombra suave no alto (a emenda não fica seca)
SOMBRA = (1 - .45 * np.clip(1 - np.arange(960, dtype=np.float32) / 40, 0, 1))[:, None, None]
def metade(p, s):
    if METADE:   # vídeo próprio da metade, 1080x960: zoom no rosto a ~1/3 da altura
        if p.shape[:2] != (960, W): p = cv2.resize(p, (W, 960), interpolation=cv2.INTER_LANCZOS4)
        b = zoom(p, s, 540, 330)
    else:
        if p.shape[:2] != (H, W): p = cv2.resize(p, (W, H), interpolation=cv2.INTER_LANCZOS4)
        b = zoom(np.ascontiguousarray(p[MT:MT + 960]), s, CX, min(max(CY - MT, 0), 959))
    return (b.astype(np.float32) * SOMBRA).astype(np.uint8)

def borra(img, s): return img if s <= 0 else cv2.GaussianBlur(img, (0, 0), s)
def leitoso(img, a, cor=(196, 214, 232)): return cv2.addWeighted(img, 1 - a, np.full_like(img, cor), a, 0)   # creme quente
def chicote(img, dx, l):
    out = np.roll(img, int(dx), axis=1)
    return cv2.blur(out, (int(l), 1)) if l > 1 else out

def quadros(path):
    c = av.open(path); s = c.streams.video[0]; s.thread_type = 'AUTO'
    for fr in c.decode(s): yield fr.to_ndarray(format='bgr24')
    c.close()
def video(saida, so=None):
    gens = {'p': quadros(PESSOA), 'm': quadros(MOTION), 'h': quadros(METADE or PESSOA)}; bufs = {q: [] for q in gens}
    def get(q, i):
        lst = bufs[q]
        while len(lst) <= i:
            try: lst.append(next(gens[q]))
            except StopIteration: lst.append(lst[-1])
        return lst[i]
    pipe = None
    if so is None:
        pipe = subprocess.Popen([FF, '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                                 '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-color_primaries', 'bt709',
                                 '-color_trc', 'bt709', '-colorspace', 'bt709', saida], stdin=subprocess.PIPE)
    def base(i):
        m = MODO[i]
        if m == 'R': return zoom(get('p', i), escala[i], CX, CY)
        mo = get('m', i)
        if mo.shape[:2] != (H, W): mo = cv2.resize(mo, (W, H), interpolation=cv2.INTER_LANCZOS4)
        if m == 'M': return acabamento(mo)
        cima = acabamento(np.ascontiguousarray(mo[:960]))
        return np.vstack([cima, metade(get('h', i), escala[i])])
    cache = {}
    def B(i):
        i = min(max(i, 0), N - 1)
        if i not in cache: cache[i] = base(i)
        return cache[i]
    for i in range(N):
        img = B(i)
        for t, tipo in TR.items():
            d = i - t
            if tipo == 'clarao' and -3 <= d <= 3:
                img = leitoso(borra(img, [16, 9, 4, 18, 10, 5, 2][d + 3]), [.55, .3, .12, .6, .32, .14, .04][d + 3])
            elif tipo == 'whip' and -2 <= d <= 2:
                dx, l = [(-170, 120), (-60, 60), (170, 150), (60, 70), (14, 18)][d + 2]
                img = chicote(img, dx, l)
            elif tipo == 'blur' and -2 <= d <= 2:
                img = borra(img, [6, 12, 12, 6, 2][d + 2])
        if i >= N - 9: img = (img.astype(np.float32) * ((N - 1 - i) / 9)).astype(np.uint8)   # fade final 0,3 s
        for j in [x for x in cache if x < i - 4]: del cache[j]
        for q in bufs:
            if len(bufs[q]) > 8: bufs[q][:len(bufs[q]) - 8] = [None] * (len(bufs[q]) - 8)
        if so is not None:
            if i in so: Path('work/quadros-labs').mkdir(parents=True, exist_ok=True); cv2.imwrite(f'work/quadros-labs/q{i / FPS:07.2f}.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 88])
            if i > max(so): break
        else: pipe.stdin.write(img.tobytes())
        if i % 300 == 0: print(f'  {i}/{N}', flush=True)
    if pipe: pipe.stdin.close(); pipe.wait()

SR = 48000
def le(path, ini=0, dur=None):
    cmd = [FF, '-loglevel', 'error', '-ss', str(ini), '-i', str(path)] + (['-t', str(dur)] if dur else []) + ['-f', 'f32le', '-ac', '2', '-ar', str(SR), '-']
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).reshape(-1, 2).copy()

def audio(saida):
    mix = le(PESSOA, 0, DUR)
    if CFG.get('trilha'):
        tr = le(CFG['trilha'])
        while len(tr) < len(mix): tr = np.concatenate([tr, tr])
        tr = tr[:len(mix)]
        rv = np.sqrt((mix ** 2).mean()); rt = np.sqrt((tr ** 2).mean()) + 1e-9
        tr *= rv * CFG.get('nivel_trilha', .16) / rt
        f = np.ones(len(tr)); n = int(1.5 * SR); f[-n:] = np.linspace(1, 0, n); f[:int(.3 * SR)] = np.linspace(0, 1, int(.3 * SR))
        mix = mix + tr * f[:, None]
    ED = Path(CFG.get('efeitos_dir', 'trilhas/efeitos')); G = CFG.get('sfx_ganho', .5)
    ED2 = Path(__file__).resolve().parent.parent / 'assets' / 'efeitos'   # os 2 cliques vêm com a skill
    def acha(arq): return ED / arq if (ED / arq).exists() else ED2 / arq
    ORG = [0.0, 1.4, 2.65, 4.25, 5.7]   # as 5 variações dentro do click-organico.wav
    n_org = [0]
    def som(nome):
        if nome == 'organico':
            k = n_org[0] % 5; n_org[0] += 1; p = acha('click-organico.wav')
            return le(p, ORG[k], 1.15) if p.exists() else None
        if nome == 'magico': nome = 'click-magico'
        p = acha(f'{nome}.wav')
        return le(p) if p.exists() else None
    def poe(t, nome, g):
        s = som(nome)
        if s is None: print('  sem o efeito', nome, 'em', ED); return
        a = max(0, int(t * SR)); s = s[:max(0, len(mix) - a)]; mix[a:a + len(s)] += s * g * G
    for t, nome, g in CFG.get('efeitos', []): poe(t, nome, g)
    for t, tipo in sorted(TR.items()):
        nome, g = {'clarao': ('magico', .38), 'whip': ('organico', 1.5), 'blur': ('organico', 1.1)}[tipo]
        poe(t / FPS - .02, nome, g)
    pico = np.abs(mix).max()
    if pico > .98: mix *= .98 / pico
    w = wave.open(saida, 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype(np.int16).tobytes()); w.close()

if __name__ == '__main__':
    if '--quadros' in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index('--quadros') + 1].split(',')]
        video(None, so=set(qm(t) for t in ts)); print('quadros em work/quadros-labs/'); sys.exit()
    out = CFG['saida']; tmpv, tmpa = out + '.video.mp4', out + '.audio.wav'
    video(tmpv); audio(tmpa)
    subprocess.run([FF, '-y', '-loglevel', 'error', '-i', tmpv, '-i', tmpa, '-c:v', 'copy',
                    '-af', 'loudnorm=I=-15:TP=-1.5:LRA=11', '-c:a', 'aac', '-b:a', '256k',
                    '-shortest', '-movflags', '+faststart', out], check=True)
    os.remove(tmpv); os.remove(tmpa); print('ok', out)
