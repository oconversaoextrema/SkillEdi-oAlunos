# -*- coding: utf-8 -*-
"""Caminhos das ferramentas instaladas pelo instalar.sh/.ps1 (lidos de ~/.editor-video/ambiente.json).

    from ambiente import AMB, FFMPEG
"""
import json, os
from pathlib import Path

DIR = Path(os.environ.get('EDITOR_VIDEO_DIR', Path.home() / '.editor-video')).expanduser()
try:
    AMB = json.loads((DIR / 'ambiente.json').read_text())
except FileNotFoundError:
    raise SystemExit('Ferramentas não instaladas. Rode: bash scripts/instalar.sh  (Windows: scripts\\instalar.ps1)')
FFMPEG, FFPROBE, MODELS, RVM, FONTES = AMB['ffmpeg'], AMB['ffprobe'], AMB['models'], AMB['rvm'], AMB['fontes']
