# -*- coding: utf-8 -*-
"""Folha de contato de um vídeo (quadros com o tempo escrito) para conferir enquadramento, texto e ritmo.

    python folha.py <video> [passo_s] [ini] [fim]     -> <video>-folha.png
"""
import sys
import cv2, numpy as np

v = sys.argv[1]
c = cv2.VideoCapture(v); fps = c.get(cv2.CAP_PROP_FPS) or 30; dur = c.get(cv2.CAP_PROP_FRAME_COUNT) / fps
ini = float(sys.argv[3]) if len(sys.argv) > 3 else 0
fim = float(sys.argv[4]) if len(sys.argv) > 4 else dur
passo = float(sys.argv[2]) if len(sys.argv) > 2 else max(0.5, (fim - ini) / 60)
ims, t = [], ini
while t < fim and len(ims) < 80:
    c.set(cv2.CAP_PROP_POS_MSEC, t * 1000); ok, f = c.read()
    if not ok: break
    h, w = f.shape[:2]; f = cv2.resize(f, (240, int(240 * h / w)))
    cv2.rectangle(f, (0, 0), (70, 18), (0, 0, 0), -1); cv2.putText(f, f'{t:.1f}', (2, 14), 0, 0.5, (0, 255, 255), 1)
    ims.append(f); t += passo
while len(ims) % 10: ims.append(np.zeros_like(ims[0]))
g = np.vstack([np.hstack(ims[i:i + 10]) for i in range(0, len(ims), 10)])
o = v.rsplit('.', 1)[0] + '-folha.png'; cv2.imwrite(o, g); print(o, f'{dur:.1f}s')
