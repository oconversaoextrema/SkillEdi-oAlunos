"""Baixa vídeo de YouTube/TikTok/Instagram pra área de cima dos Reels (yt-dlp local em ferramentas/pydeps).

    PYTHONPATH=ferramentas/pydeps $PY work/baixar.py URL pasta-destino [inicio-seg fim-seg] [nome]

Pega h264 até 1080p com áudio, mescla em mp4. Com início/fim baixa só o trecho (mais rápido).
Registrar a fonte em referencias/<video>/fontes.md depois.
"""
import os, sys, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
FF = open("ferramentas/ffmpeg_path.txt").read().strip()
PY = sys.executable

def baixar(url, destino, ini=None, fim=None, nome=None):
    os.makedirs(destino, exist_ok=True)
    saida = os.path.join(destino, (nome or "%(id)s") + ".%(ext)s")
    cmd = [PY, "-m", "yt_dlp", "--ffmpeg-location", FF, "--no-playlist", "--quiet", "--no-warnings",
           "-f", "bv*[vcodec^=avc1][height<=1080]+ba[ext=m4a]/bv*[height<=1080]+ba/b", "--merge-output-format", "mp4",
           "-o", saida, "--print", "after_move:filepath"]
    if ini is not None and fim is not None:
        cmd += ["--download-sections", f"*{ini}-{fim}", "--force-keyframes-at-cuts"]
    cmd.append(url)
    env = dict(os.environ, PYTHONPATH="ferramentas/pydeps")
    r = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if r.returncode: raise SystemExit(r.stderr[-800:])
    return r.stdout.strip().splitlines()[-1]

if __name__ == "__main__":
    a = sys.argv[1:]
    ini = float(a[2]) if len(a) > 3 else None; fim = float(a[3]) if len(a) > 3 else None
    nome = a[4] if len(a) > 4 else (a[2] if len(a) == 3 else None)
    print(baixar(a[0], a[1], ini, fim, nome))
