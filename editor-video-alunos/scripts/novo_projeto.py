# -*- coding: utf-8 -*-
"""Prepara a pasta de um projeto de edição (uma vez por projeto).

    python scripts/novo_projeto.py <pasta-do-projeto>

Cria brutos/ saidas/ referencias/ work/ ferramentas/, copia os scripts da skill para work/, grava
ferramentas/ffmpeg_path.txt, liga models/ e ferramentas/fontes/ às pastas instaladas, e copia os modelos de
Remotion e HyperFrames para work/modelos/ (sem node_modules: os renders usam os atalhos remotion/hf).
"""
import os, shutil, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from ambiente import AMB  # noqa: E402

SKILL = Path(AMB['skill'])
proj = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
for p in ['brutos', 'saidas', 'referencias', 'work/modelos', 'ferramentas', 'trilhas/efeitos']:
    (proj / p).mkdir(parents=True, exist_ok=True)
(proj / 'ferramentas' / 'ffmpeg_path.txt').write_text(AMB['ffmpeg'] + '\n')


def ligar(origem, destino):
    origem, destino = Path(origem), Path(destino)
    if destino.exists() or destino.is_symlink():
        return
    try:
        os.symlink(origem, destino, target_is_directory=True)
    except OSError:          # Windows sem permissão de link: junction
        if os.name == 'nt':
            os.system(f'mklink /J "{destino}" "{origem}" >nul')
        else:
            shutil.copytree(origem, destino)


ligar(AMB['models'], proj / 'models')
ligar(AMB['fontes'], proj / 'ferramentas' / 'fontes')
for f in (SKILL / 'scripts').glob('*.py'):
    if f.name not in ('instalar.py', 'novo_projeto.py'):
        shutil.copy2(f, proj / 'work' / f.name)
for m in ['remotion-modelo', 'hyperframes-modelo']:
    d = proj / 'work' / 'modelos' / m
    if not d.exists():
        shutil.copytree(SKILL / 'assets' / m, d)
gsap = Path(AMB['pasta']) / 'hyperframes' / 'node_modules' / 'gsap' / 'dist' / 'gsap.min.js'
if gsap.exists():
    (proj / 'work' / 'modelos' / 'hyperframes-modelo' / 'vendor').mkdir(exist_ok=True)
    shutil.copy2(gsap, proj / 'work' / 'modelos' / 'hyperframes-modelo' / 'vendor' / 'gsap.min.js')
print('projeto pronto:', proj)
print('python das ferramentas:', AMB['python'])
