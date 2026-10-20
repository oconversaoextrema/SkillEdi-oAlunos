# Instala todas as ferramentas de edição (Windows), sem administrador.
#   powershell -ExecutionPolicy Bypass -File scripts\instalar.ps1
#   powershell -ExecutionPolicy Bypass -File scripts\instalar.ps1 --verificar
$ErrorActionPreference = "Stop"
$Aqui = Split-Path -Parent $MyInvocation.MyCommand.Path
$Dir = if ($env:EDITOR_VIDEO_DIR) { $env:EDITOR_VIDEO_DIR } else { Join-Path $HOME ".editor-video" }
New-Item -ItemType Directory -Force -Path $Dir | Out-Null
$env:EDITOR_VIDEO_DIR = $Dir

$uv = (Get-Command uv -ErrorAction SilentlyContinue).Source
if (-not $uv) { $cand = Join-Path $HOME ".local\bin\uv.exe"; if (Test-Path $cand) { $uv = $cand } }
if (-not $uv) {
  Write-Host "== instalando uv (gerenciador de Python)"
  $env:UV_NO_MODIFY_PATH = "1"
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  $uv = Join-Path $HOME ".local\bin\uv.exe"
}
$py = Join-Path $Dir "venv\Scripts\python.exe"
if (-not (Test-Path $py)) { Write-Host "== criando o Python 3.12 da skill"; & $uv venv --python 3.12 (Join-Path $Dir "venv") }
Write-Host "== bibliotecas Python (Whisper, PyAV, OpenCV, Pillow, yt-dlp...)"
& $uv pip install --quiet --python $py -r (Join-Path $Aqui "requirements.txt")
& $py (Join-Path $Aqui "instalar.py") @args
