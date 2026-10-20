# -*- coding: utf-8 -*-
"""Instala (ou confere) TODAS as ferramentas de edição da skill, numa pasta só do aluno — sem senha de administrador.

Não rode este arquivo direto: use scripts/instalar.sh (Mac/Linux) ou scripts/instalar.ps1 (Windows), que criam o
Python certo antes e depois chamam este aqui.

Pasta das ferramentas: ~/.editor-video  (ou a variável EDITOR_VIDEO_DIR)

    ~/.editor-video/
      venv/                 Python 3.12 com faster-whisper, PyAV, OpenCV, Pillow, numpy, onnxruntime, yt-dlp
      bin/                  ffmpeg, ffprobe, hf (HyperFrames) e remotion (atalhos que já põem tudo no PATH)
      node/                 Node.js portátil (só se o computador não tiver Node 18+)
      hyperframes/          HyperFrames (HTML/CSS/GSAP -> MP4)
      remotion-modelo/      projeto Remotion pronto (React -> MP4), com node_modules e navegador do Remotion
      models/               Whisper "small" (transcrição) e models/rvm/ (recorte da pessoa, Robust Video Matting)
      fontes/               TikTok Sans, Manrope, Inter, Montserrat (licença OFL, Google Fonts)
      ambiente.json         caminho de tudo (os scripts da skill leem daqui)
      ambiente.sh / .ps1    exports de PATH para usar no terminal

Rodar de novo é seguro: o que já está instalado é pulado. --verificar só confere e mostra o que falta.
"""
import json, os, platform, shutil, subprocess, sys, tarfile, urllib.request, zipfile
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
DIR = Path(os.environ.get('EDITOR_VIDEO_DIR', Path.home() / '.editor-video')).expanduser()
WIN = os.name == 'nt'
BIN = DIR / 'bin'
HF_VERSAO = '0.8.76'
FONTES = {
    'TikTokSans-Variable.ttf': 'ofl/tiktoksans/TikTokSans%5Bopsz,slnt,wdth,wght%5D.ttf',
    'Manrope.ttf': 'ofl/manrope/Manrope%5Bwght%5D.ttf',
    'Inter.ttf': 'ofl/inter/Inter%5Bopsz,wght%5D.ttf',
    'Montserrat.ttf': 'ofl/montserrat/Montserrat%5Bwght%5D.ttf',
}
RVM = 'https://github.com/PeterL1n/RobustVideoMatting/releases/download/v1.0.0/rvm_mobilenetv3_fp32.onnx'
SO_VERIFICAR = '--verificar' in sys.argv


def passo(t): print(f'\n== {t}', flush=True)
def ok(t): print(f'   ok  {t}', flush=True)
def falta(t): print(f'   FALTA  {t}', flush=True)


def baixar(url, destino):
    destino = Path(destino); destino.parent.mkdir(parents=True, exist_ok=True)
    tmp = destino.with_suffix(destino.suffix + '.parcial')
    req = urllib.request.Request(url, headers={'User-Agent': 'editor-video-alunos'})
    with urllib.request.urlopen(req, timeout=120) as r, open(tmp, 'wb') as f:
        shutil.copyfileobj(r, f, 1 << 20)
    tmp.replace(destino)


def rodar(cmd, **kw):
    print('   $', ' '.join(str(c) for c in cmd), flush=True)
    return subprocess.run([str(c) for c in cmd], check=True, **kw)


def env_com_bin():
    e = dict(os.environ)
    extra = [str(BIN)]
    if (DIR / 'node').exists():
        extra.append(str(node_dir()))
    e['PATH'] = os.pathsep.join(extra + [e.get('PATH', '')])
    e['DO_NOT_TRACK'] = '1'; e['HYPERFRAMES_NO_TELEMETRY'] = '1'
    return e


# ---------------------------------------------------------------- ffmpeg / ffprobe
def ffmpeg():
    passo('ffmpeg e ffprobe')
    BIN.mkdir(parents=True, exist_ok=True)
    nomes = ['ffmpeg.exe', 'ffprobe.exe'] if WIN else ['ffmpeg', 'ffprobe']
    if all((BIN / n).exists() for n in nomes):
        ok(str(BIN / nomes[0])); return
    if SO_VERIFICAR:
        falta('ffmpeg/ffprobe'); return
    from static_ffmpeg import run
    ff, fp = run.get_or_fetch_platform_executables_else_raise()
    for src, n in zip((ff, fp), nomes):
        shutil.copy2(src, BIN / n)
        if not WIN: os.chmod(BIN / n, 0o755)
    ok(str(BIN / nomes[0]))


# ---------------------------------------------------------------- Node.js
def node_dir():
    d = DIR / 'node'
    if not d.exists(): return None
    sub = next(d.iterdir())
    return sub if WIN else sub / 'bin'


def node_exe():
    """Node do sistema se for 18+, senão o portátil."""
    n = shutil.which('node')
    if n:
        try:
            v = subprocess.run([n, '-v'], capture_output=True, text=True).stdout.strip()
            if int(v.lstrip('v').split('.')[0]) >= 18:
                return Path(n)
        except Exception:
            pass
    d = node_dir()
    if d:
        return d / ('node.exe' if WIN else 'node')
    return None


def npm_exe():
    n = node_exe()
    if not n: return None
    cand = n.parent / ('npm.cmd' if WIN else 'npm')
    return cand if cand.exists() else Path(shutil.which('npm') or 'npm')


def npx_exe():
    n = node_exe()
    cand = n.parent / ('npx.cmd' if WIN else 'npx')
    return cand if cand.exists() else Path(shutil.which('npx') or 'npx')


def node():
    passo('Node.js (precisa para Remotion e HyperFrames)')
    n = node_exe()
    if n:
        ok(f'{n} ({subprocess.run([str(n), "-v"], capture_output=True, text=True).stdout.strip()})'); return
    if SO_VERIFICAR:
        falta('Node.js 18+'); return
    idx = json.load(urllib.request.urlopen('https://nodejs.org/dist/index.json', timeout=60))
    lts = next(v for v in idx if v.get('lts'))
    ver = lts['version']
    arq = platform.machine().lower()
    arq = 'arm64' if arq in ('arm64', 'aarch64') else 'x64'
    so = {'Darwin': 'darwin', 'Linux': 'linux', 'Windows': 'win'}[platform.system()]
    ext = 'zip' if WIN else ('tar.gz' if so == 'darwin' else 'tar.xz')
    nome = f'node-{ver}-{so}-{arq}.{ext}'
    destino = DIR / 'node'; destino.mkdir(parents=True, exist_ok=True)
    pacote = DIR / nome
    print(f'   baixando {nome} (nodejs.org)', flush=True)
    baixar(f'https://nodejs.org/dist/{ver}/{nome}', pacote)
    if ext == 'zip':
        zipfile.ZipFile(pacote).extractall(destino)
    else:
        t = tarfile.open(pacote)
        t.extractall(destino, filter='data') if hasattr(tarfile, 'data_filter') else t.extractall(destino)
    pacote.unlink()
    ok(f'{node_exe()} ({ver})')


# ---------------------------------------------------------------- HyperFrames
def hyperframes():
    passo(f'HyperFrames {HF_VERSAO} (animação em HTML/CSS/GSAP -> MP4)')
    d = DIR / 'hyperframes'
    cli = d / 'node_modules' / '.bin' / ('hyperframes.cmd' if WIN else 'hyperframes')
    if not cli.exists():
        if SO_VERIFICAR:
            falta('HyperFrames'); return
        d.mkdir(parents=True, exist_ok=True)
        (d / 'package.json').write_text(json.dumps({'name': 'hyperframes-local', 'private': True}, indent=1))
        rodar([npm_exe(), 'install', '--no-fund', '--no-audit', f'hyperframes@{HF_VERSAO}', 'gsap@3'], cwd=d, env=env_com_bin())
    # atalho "hf" que já põe ffmpeg/ffprobe/node no PATH
    if WIN:
        (BIN / 'hf.cmd').write_text(f'@echo off\r\nset "PATH={BIN};{node_dir() or ""};%PATH%"\r\nset DO_NOT_TRACK=1\r\nset HYPERFRAMES_NO_TELEMETRY=1\r\n"{cli}" %*\r\n')
    else:
        nd = node_dir()
        (BIN / 'hf').write_text(f'#!/bin/sh\nexport PATH="{BIN}:{nd or ""}:$PATH" DO_NOT_TRACK=1 HYPERFRAMES_NO_TELEMETRY=1\n'
                                f'export HYPERFRAMES_FFMPEG_PATH="{BIN / "ffmpeg"}" HYPERFRAMES_FFPROBE_PATH="{BIN / "ffprobe"}"\n'
                                f'exec "{cli}" "$@"\n')
        os.chmod(BIN / 'hf', 0o755)
    ok(f'{BIN / ("hf.cmd" if WIN else "hf")}')


# ---------------------------------------------------------------- Remotion
def remotion():
    passo('Remotion (vídeo em React -> MP4)')
    d = DIR / 'remotion-modelo'
    if not (d / 'node_modules' / 'remotion').exists():
        if SO_VERIFICAR:
            falta('Remotion'); return
        if d.exists(): shutil.rmtree(d)
        shutil.copytree(SKILL / 'assets' / 'remotion-modelo', d)
        rodar([npm_exe(), 'install', '--no-fund', '--no-audit'], cwd=d, env=env_com_bin())
        rodar([npx_exe(), 'remotion', 'browser', 'ensure'], cwd=d, env=env_com_bin())
    if WIN:
        (BIN / 'remotion.cmd').write_text(f'@echo off\r\nset "PATH={BIN};{node_dir() or ""};%PATH%"\r\n"{d / "node_modules" / ".bin" / "remotion.cmd"}" %*\r\n')
    else:
        (BIN / 'remotion').write_text(f'#!/bin/sh\nexport PATH="{BIN}:{node_dir() or ""}:$PATH"\nexec "{d / "node_modules" / ".bin" / "remotion"}" "$@"\n')
        os.chmod(BIN / 'remotion', 0o755)
    ok(str(d))


# ---------------------------------------------------------------- modelos de IA
def whisper():
    passo('Whisper "small" (transcrição e legenda, roda no computador)')
    m = DIR / 'models'
    if any(m.glob('models--Systran--faster-whisper-small*')):
        ok(str(m)); return
    if SO_VERIFICAR:
        falta('modelo Whisper small'); return
    from faster_whisper import WhisperModel
    WhisperModel('small', device='cpu', compute_type='int8', download_root=str(m))
    ok(str(m))


def rvm():
    passo('Robust Video Matting (recortar a pessoa do fundo)')
    f = DIR / 'models' / 'rvm' / 'rvm_mobilenetv3_fp32.onnx'
    if f.exists():
        ok(str(f)); return
    if SO_VERIFICAR:
        falta('modelo RVM'); return
    baixar(RVM, f)
    ok(str(f))


def fontes():
    passo('Fontes (OFL, Google Fonts)')
    d = DIR / 'fontes'; d.mkdir(parents=True, exist_ok=True)
    for nome, cam in FONTES.items():
        if (d / nome).exists():
            ok(nome); continue
        if SO_VERIFICAR:
            falta(nome); continue
        baixar('https://github.com/google/fonts/raw/main/' + cam, d / nome)
        ok(nome)


# ---------------------------------------------------------------- python
def python_libs():
    passo('Bibliotecas Python')
    faltando = []
    for mod in ['av', 'cv2', 'PIL', 'numpy', 'faster_whisper', 'onnxruntime', 'yt_dlp', 'imageio_ffmpeg']:
        try:
            __import__(mod)
        except Exception:
            faltando.append(mod)
    if faltando:
        falta(', '.join(faltando) + ' — rode o instalar.sh / instalar.ps1 de novo')
    else:
        ok(sys.executable)


def gravar_ambiente():
    amb = {
        'pasta': str(DIR), 'python': sys.executable,
        'ffmpeg': str(BIN / ('ffmpeg.exe' if WIN else 'ffmpeg')), 'ffprobe': str(BIN / ('ffprobe.exe' if WIN else 'ffprobe')),
        'node': str(node_exe() or ''), 'hf': str(BIN / ('hf.cmd' if WIN else 'hf')),
        'remotion_modelo': str(DIR / 'remotion-modelo'), 'remotion': str(BIN / ('remotion.cmd' if WIN else 'remotion')),
        'models': str(DIR / 'models'), 'rvm': str(DIR / 'models' / 'rvm' / 'rvm_mobilenetv3_fp32.onnx'),
        'fontes': str(DIR / 'fontes'), 'skill': str(SKILL),
    }
    (DIR / 'ambiente.json').write_text(json.dumps(amb, indent=1, ensure_ascii=False))
    nd = node_dir()
    (DIR / 'ambiente.sh').write_text(f'export PATH="{BIN}:{nd or ""}:{Path(sys.executable).parent}:$PATH"\n'
                                     f'export DO_NOT_TRACK=1 HYPERFRAMES_NO_TELEMETRY=1 EDITOR_VIDEO_DIR="{DIR}"\n')
    (DIR / 'ambiente.ps1').write_text(f'$env:PATH = "{BIN};{nd or ""};{Path(sys.executable).parent};" + $env:PATH\n'
                                      f'$env:DO_NOT_TRACK = "1"; $env:HYPERFRAMES_NO_TELEMETRY = "1"; $env:EDITOR_VIDEO_DIR = "{DIR}"\n')
    return amb


def main():
    DIR.mkdir(parents=True, exist_ok=True)
    print(f'Pasta das ferramentas: {DIR}')
    python_libs()
    ffmpeg(); node()
    if node_exe():
        hyperframes(); remotion()
    whisper(); rvm(); fontes()
    amb = gravar_ambiente()
    passo('Resumo')
    for k in ['python', 'ffmpeg', 'node', 'hf', 'remotion', 'models', 'rvm', 'fontes']:
        print(f'   {k:9} {amb[k]}')
    print('\nPronto. Em cada projeto de vídeo, rode uma vez:  <python> scripts/novo_projeto.py <pasta-do-projeto>')


if __name__ == '__main__':
    main()
