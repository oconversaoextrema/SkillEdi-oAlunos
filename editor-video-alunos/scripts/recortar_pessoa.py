# -*- coding: utf-8 -*-
"""Recorta a pessoa do fundo (Robust Video Matting) -> .webm com transparência, para pôr texto/imagem ATRÁS dela.

    python recortar_pessoa.py <video> <saida.webm> [--degrade A B]

--degrade A B  mantém o fundo original na parte de baixo e só some com ele de cima: o fundo é transparente acima
               da linha y=A e inteiro abaixo de y=B (px do vídeo), com transição suave entre as duas.
               Ex.: num 1080x1920 com o rosto em y~700, "--degrade 600 900" deixa da orelha pra cima recortado.

Roda no processador (sem placa de vídeo): ~3 a 6 quadros por segundo em 1080p. Usa a cor do quadro original e só o
alpha do RVM. Grava em bt709 (mesma cor do vídeo de origem — sem isso a cor "pula" quando a camada entra).
"""
import subprocess, sys
from pathlib import Path
import numpy as np, av, onnxruntime as ort
sys.path.insert(0, str(Path(__file__).resolve().parent))
from ambiente import FFMPEG, RVM  # noqa: E402

ent, saida = sys.argv[1], sys.argv[2]
DEG = None
if '--degrade' in sys.argv:
    i = sys.argv.index('--degrade'); DEG = (float(sys.argv[i + 1]), float(sys.argv[i + 2]))
src = av.open(ent); vs = src.streams.video[0]
W, H = vs.codec_context.width, vs.codec_context.height
fps = float(vs.average_rate or 30)
rampa = None
if DEG:
    u = np.clip((np.arange(H, dtype=np.float32) - DEG[0]) / max(1.0, DEG[1] - DEG[0]), 0, 1)
    rampa = (u * u * (3 - 2 * u) * 255).astype(np.uint8)[:, None]
sess = ort.InferenceSession(RVM, providers=['CPUExecutionProvider'])
rec = [np.zeros([1, 1, 1, 1], dtype=np.float32)] * 4
ds = np.array([0.4 if max(W, H) > 1280 else 0.6], dtype=np.float32)
enc = subprocess.Popen([FFMPEG, '-hide_banner', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba',
                        '-s', f'{W}x{H}', '-r', f'{fps}', '-i', '-',
                        '-vf', 'scale=out_color_matrix=bt709:out_range=tv',
                        '-c:v', 'libvpx-vp9', '-pix_fmt', 'yuva420p', '-b:v', '0', '-crf', '20', '-row-mt', '1',
                        '-deadline', 'good', '-cpu-used', '4', '-auto-alt-ref', '0',
                        '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', saida], stdin=subprocess.PIPE)
n = 0
for fr in src.decode(vs):
    rgb = fr.to_ndarray(format='rgb24')
    x = (rgb.astype(np.float32) / 255.0).transpose(2, 0, 1)[None]
    fgr, pha, *rec = sess.run(None, {'src': x, 'r1i': rec[0], 'r2i': rec[1], 'r3i': rec[2], 'r4i': rec[3], 'downsample_ratio': ds})
    a = np.clip(pha[0, 0] * 255.0 + 0.5, 0, 255).astype(np.uint8)
    if rampa is not None:
        a = np.maximum(a, np.broadcast_to(rampa, a.shape))
    enc.stdin.write(np.dstack([rgb, a]).tobytes())
    n += 1
    if n % 150 == 0: print(n, 'quadros', flush=True)
enc.stdin.close(); enc.wait()
print('ok', saida, n, 'quadros')
