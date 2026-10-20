# -*- coding: utf-8 -*-
"""Transcreve um áudio/vídeo com Whisper (local), palavra por palavra.

    python transcrever.py <arquivo> [saida.json] [--modelo small] [--prompt "Nomes, Marcas, Jargões"]

Saída: lista [{"w": palavra, "s": início, "e": fim}] em segundos + imprime o texto numerado (índice:palavra@tempo),
que é como as cenas e a legenda são amarradas à fala. Transcreva SEMPRE o áudio já cortado (linha do tempo final).
"""
import json, subprocess, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from ambiente import FFMPEG, MODELS  # noqa: E402
from faster_whisper import WhisperModel  # noqa: E402

args = [a for a in sys.argv[1:]]
def opc(nome, padrao):
    if nome in args:
        i = args.index(nome); v = args[i + 1]; del args[i:i + 2]; return v
    return padrao
modelo, prompt = opc('--modelo', 'small'), opc('--prompt', None)
ent = args[0]
saida = args[1] if len(args) > 1 else str(Path(ent).with_suffix('.palavras.json'))
wav = Path(tempfile.gettempdir()) / 'transcrever-16k.wav'
subprocess.run([FFMPEG, '-loglevel', 'error', '-y', '-i', ent, '-vn', '-ac', '1', '-ar', '16000', str(wav)], check=True)
m = WhisperModel(modelo, device='cpu', compute_type='int8', download_root=MODELS)
segs, info = m.transcribe(str(wav), language='pt', word_timestamps=True, beam_size=5, vad_filter=True, initial_prompt=prompt)
pal = [{'w': w.word.strip(), 's': round(w.start, 3), 'e': round(w.end, 3)} for s in segs for w in s.words]
json.dump(pal, open(saida, 'w'), ensure_ascii=False, indent=0)
print(' '.join(f"{i}:{p['w']}@{p['s']:.2f}" for i, p in enumerate(pal)))
print(f'\n{len(pal)} palavras -> {saida}')
