#!/usr/bin/env bash
# Instala todas as ferramentas de edição (Mac e Linux), sem senha de administrador.
#   bash scripts/instalar.sh              instala o que falta
#   bash scripts/instalar.sh --verificar  só confere
# Pasta: ~/.editor-video (ou EDITOR_VIDEO_DIR). Rodar de novo é seguro.
set -euo pipefail
AQUI="$(cd "$(dirname "$0")" && pwd)"
DIR="${EDITOR_VIDEO_DIR:-$HOME/.editor-video}"
mkdir -p "$DIR"
export EDITOR_VIDEO_DIR="$DIR"

# 1) uv: gerenciador de Python (astral.sh). Instala na pasta do usuário.
UV="$(command -v uv || true)"
[ -z "$UV" ] && [ -x "$HOME/.local/bin/uv" ] && UV="$HOME/.local/bin/uv"
if [ -z "$UV" ]; then
  echo "== instalando uv (gerenciador de Python)"
  curl -LsSf https://astral.sh/uv/install.sh | env UV_NO_MODIFY_PATH=1 sh
  UV="$HOME/.local/bin/uv"
fi

# 2) Python 3.12 + bibliotecas num ambiente só da skill
if [ ! -x "$DIR/venv/bin/python" ]; then
  echo "== criando o Python 3.12 da skill"
  "$UV" venv --python 3.12 "$DIR/venv"
fi
echo "== bibliotecas Python (Whisper, PyAV, OpenCV, Pillow, yt-dlp...)"
"$UV" pip install --quiet --python "$DIR/venv/bin/python" -r "$AQUI/requirements.txt"

# 3) o resto (ffmpeg, Node, HyperFrames, Remotion, modelos, fontes)
"$DIR/venv/bin/python" "$AQUI/instalar.py" "$@"
