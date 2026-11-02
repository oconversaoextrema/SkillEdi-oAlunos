# -*- coding: utf-8 -*-
"""Montagem do YouTube no estilo LABS (references/padrao-tessmann-youtube.md): troca pessoa ↔ motion pelas cenas,
punch-in alternado na pessoa, transições (clarão leitoso pessoa→motion e em capítulo, chicote motion→motion,
desfoque motion→pessoa), ACABAMENTO só no motion (retícula a 45° nos tons médios, aberração cromática, glow, grão
mínimo, vinheta) e áudio (voz + trilha contínua baixa + efeitos + whoosh das transições).

uso:  python work/labs_compor.py work/<video>/labs.json [--quadros t1,t2,...]

labs.json:
{
  "pessoa": "work/<video>/base.mp4",        vídeo da pessoa já cortado (com a voz)
  "motion": "work/<video>/motion.mp4",      render do HyperFrames com a MESMA duração, cenas nos tempos de saída
  "saida": "saidas/<titulo>.mp4",
  "cenas": [[0, 2.5, 0], [4.6, 9.2, 0], [26.9, 29.5, 1]],   [início, fim, capítulo? 1/0] dos trechos de motion
  "cortes": [12.3, 40.1],                   (opcional) cortes do vídeo da pessoa, pra trocar o punch-in
  "centro": [950, 400],                     (opcional) ponto do zoom (rosto), em px de 1080p
  "trilha": "trilhas/<musica>.mp3",         (opcional) trilha contínua, ~16 dB abaixo da voz
  "nivel_trilha": 0.16,
  "efeitos_dir": "trilhas/efeitos",         (opcional) pasta dos .wav: pop, click, tick, ding, whoosh_in, whoosh2, whoosh_out…
  "efeitos": [[0.9, "pop", 0.3]],           [tempo, nome do .wav sem extensão, ganho]
  "k4": false                               true = saída 3840x2160 (motion renderizado em 4K)
}"""
import os, sys, json, subprocess, wave
from pathlib import Path
import numpy as np, cv2, av
sys.path.insert(0, str(Path(__file__).resolve().parent))
from ambiente import FFMPEG as FF

CFG = json.loads(Path(sys.argv[1]).read_text())
K = 2 if CFG.get('k4') else 1
FPS, W, H = 30, 1920 * K, 1080 * K
PESSOA, MOTION = CFG['pessoa'], CFG['motion']
DUR = float(av.open(PESSOA).streams.video[0].duration * av.open(PESSOA).streams.video[0].time_base)
N = int(round(DUR * FPS))
qm = lambda t: int(round(t * FPS))
CENAS = CFG['cenas']
eh_motion = np.zeros(N, bool)
for a, b, _ in CENAS: eh_motion[qm(a):qm(b)] = True

# punch-in: alterna 1,0 / 1,1 a cada corte da pessoa e a cada volta do motion
escala = np.ones(N); k = 0; ultimo = -1
marcas = sorted(set([qm(c) for c in CFG.get('cortes', []) if c < DUR] + [i for i in range(1, N) if not eh_motion[i] and eh_motion[i - 1]]))
for i in range(N):
    if i in marcas and i - ultimo > 20: k += 1; ultimo = i
    escala[i] = (1.0, 1.1)[k % 2]
TR = {}
for a, b, cap in CENAS:
    ia, ib = qm(a), qm(b)
    TR[ia] = 'clarao' if (cap or ia == 0 or not eh_motion[ia - 1]) else 'whip'
    if ib < N and not eh_motion[ib]: TR[ib] = 'blur'
TR.pop(0, None)
CX, CY = CFG.get('centro', [950, 400])

def zoom(img, s):
    if img.shape[1] != W or s != 1:
        s2 = s * W / img.shape[1]
        M = np.float32([[s2, 0, CX * K - s2 * CX * img.shape[1] / 1920], [0, s2, CY * K - s2 * CY * img.shape[1] / 1920]])
        return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)
    return img

yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
_u, _v = (xx + yy) / np.sqrt(2), (xx - yy) / np.sqrt(2); _P = 5.0 * K
_d = np.hypot((_u % _P) - _P / 2, (_v % _P) - _P / 2)
DOT = (np.exp(-(_d / (1.55 * K)) ** 2) - .5).astype(np.float32)[..., None]
VIN = (1 - .18 * np.clip(((xx - W / 2) ** 2 / (W * .62) ** 2 + (yy - H / 2) ** 2 / (H * .62) ** 2) - .35, 0, 1))[..., None]
rng = np.random.default_rng(3)

def acabamento(img):
    f = img.astype(np.float32) / 255
    f = cv2.GaussianBlur(f, (0, 0), .6 * K)
    hl = cv2.GaussianBlur(np.clip(f - .68, 0, 1), (0, 0), 8 * K); f = f + hl * .35
    b, g, r = cv2.split(f)
    def esc(c, s, dx): return cv2.warpAffine(c, np.float32([[s, 0, W / 2 * (1 - s) + dx], [0, s, H / 2 * (1 - s)]]), (W, H), borderMode=cv2.BORDER_REPLICATE)
    f = cv2.merge([esc(b, .998, -1.0 * K), g, esc(r, 1.002, 1.0 * K)])
    w = np.clip((f - .08) / .25, 0, 1) * np.clip((.97 - f) / .15, 0, 1)   # retícula só nos tons médios
    f = (f + .16 * DOT * w) * VIN
    f = f + rng.normal(0, .004, (H, W, 1)).astype(np.float32)
    return np.clip(f * 255, 0, 255).astype(np.uint8)

def borra(img, s): return img if s <= 0 else cv2.GaussianBlur(img, (0, 0), s)
def leitoso(img, a, cor=(214, 210, 208)): return cv2.addWeighted(img, 1 - a, np.full_like(img, cor), a, 0)
def chicote(img, dx, l):
    out = np.roll(img, int(dx), axis=1)
    return cv2.blur(out, (int(l), 1)) if l > 1 else out

def quadros(path):
    c = av.open(path); s = c.streams.video[0]; s.thread_type = 'AUTO'
    for fr in c.decode(s): yield fr.to_ndarray(format='bgr24')
    c.close()

def video(saida, so=None):
    gens = {'p': quadros(PESSOA), 'm': quadros(MOTION)}; bufs = {'p': [], 'm': []}
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
    cache = {}
    def B(i):
        i = min(max(i, 0), N - 1)
        if i not in cache:
            m = get('m', i)
            if m.shape[1] != W: m = cv2.resize(m, (W, H), interpolation=cv2.INTER_LANCZOS4)
            cache[i] = acabamento(m) if eh_motion[i] else zoom(get('p', i), escala[i])
        return cache[i]
    for i in range(N):
        img = B(i)
        for t, tipo in TR.items():
            d = i - t
            if tipo == 'clarao' and -3 <= d <= 3:
                img = leitoso(borra(img, K * [16, 9, 4, 18, 10, 5, 2][d + 3]), [.55, .3, .12, .6, .32, .14, .04][d + 3])
            elif tipo == 'whip' and -2 <= d <= 2:
                dx, l = [(-170, 120), (-60, 60), (170, 150), (60, 70), (14, 18)][d + 2]
                img = chicote(img, dx * K, l * K)
            elif tipo == 'blur' and -2 <= d <= 2:
                img = borra(img, K * [6, 12, 12, 6, 2][d + 2])
        for j in [x for x in cache if x < i - 4]: del cache[j]
        for q in bufs:
            if len(bufs[q]) > 8: bufs[q][:len(bufs[q]) - 8] = [None] * (len(bufs[q]) - 8)
        if so is not None:
            if i in so: Path('work/quadros-labs').mkdir(exist_ok=True); cv2.imwrite(f'work/quadros-labs/q{i / FPS:07.2f}.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 88])
            if i > max(so): break
        else: pipe.stdin.write(img.tobytes())
        if i % 900 == 0: print(f'  {i}/{N}', flush=True)
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
    ED = Path(CFG.get('efeitos_dir', 'trilhas/efeitos'))
    def poe(t, nome, g):
        p = ED / f'{nome}.wav'
        if not p.exists(): return
        s = le(p); a = max(0, int(t * SR)); s = s[:max(0, len(mix) - a)]; mix[a:a + len(s)] += s * g
    for t, nome, g in CFG.get('efeitos', []): poe(t, nome, g)
    for t, tipo in TR.items():
        nome, g = {'clarao': ('whoosh_in', .3), 'whip': ('whoosh2', .28), 'blur': ('whoosh_out', .18)}[tipo]
        poe(t / FPS - .12, nome, g)
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
    subprocess.run([FF, '-y', '-loglevel', 'error', '-i', tmpv, '-i', tmpa, '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k',
                    '-shortest', '-movflags', '+faststart', out], check=True)
    os.remove(tmpv); os.remove(tmpa); print('ok', out)
