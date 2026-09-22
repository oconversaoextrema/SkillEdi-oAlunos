"""Preparação de um criativo: corte de respiros -> base.mov (1620x2880) -> voz tratada -> transcrição
do áudio JÁ cortado -> rastreio de rosto. Uso:

    PYTHONPATH=ferramentas/cvdeps:ferramentas/pydeps:work $PY work/criativo_prep.py c2 brutos/IMG_2966.MOV
"""
import json, os, subprocess, sys
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
sys.path.insert(0, "work")
from cortar_silencios import detectar_silencios_relativo, montar_segmentos, conferir

ID, SRC = sys.argv[1], sys.argv[2]
D = f"work/{ID}"; os.makedirs(D, exist_ok=True)
FF = open("ferramentas/ffmpeg_path.txt").read().strip()
def ff(*a): subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", *a], check=True)

p = subprocess.run([FF, "-hide_banner", "-i", SRC], capture_output=True, text=True).stderr
import re; h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", p).groups(); DUR = int(h) * 3600 + int(m) * 60 + float(s)

# 1. silêncios relativos ao piso de ruído, cortes só dentro de silêncio
ff("-i", SRC, "-vn", "-ac", "1", "-ar", "16000", f"{D}/voz16k.wav")
sil = detectar_silencios_relativo(f"{D}/voz16k.wav", dur_min=0.20, fator=0.42)
ini = sil[0][1] if sil and sil[0][0] < 0.05 else 0.0
fim = sil[-1][0] if sil and sil[-1][1] > DUR - 0.1 else DUR
segs, total = montar_segmentos(sil, DUR, ini, fim, margem=0.07, pausa_alvo=0.12, min_remover=0.10, entrada=0.20, saida=0.45)
ruins = conferir(segs, sil); assert not ruins, ruins
json.dump({"segs": segs, "total": total, "sil": sil, "dur": DUR}, open(f"{D}/cuts.json", "w"))
print(f"{ID}: bruto {DUR:.2f} s -> {total:.2f} s ({len(segs)} segmentos, tirou {DUR-total:.1f} s)")

# 2. base cortada (1620x2880 p/ permitir zoom 1,3–1,5 sem perder nitidez) + voz tratada
n = len(segs)
vf = "".join(f"[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS[v{i}];" for i, (a, b) in enumerate(segs))
af = "".join(f"[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS,afade=t=in:d=0.010,afade=t=out:st={max(0,b-a-0.010)}:d=0.010[a{i}];" for i, (a, b) in enumerate(segs))
# Grade de cor: render sem grade sai "sem cor" perto da referência. Medido contra os Reels editados no Premiere:
# contraste 1,32, saturação 1,28, gamma 0,97, leve quente nas sombras/médios, nitidez. Fica no base.mov, vale pra todo render.
GRADE = "eq=contrast=1.32:saturation=1.28:gamma=0.97,colorbalance=rs=0.04:bs=-0.05:rm=0.03:bm=-0.03,unsharp=5:5:0.6"
cat = "".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[vc][a];[vc]scale=1620:2880,{GRADE},format=yuv420p[v]"
ff("-i", SRC, "-filter_complex", vf + af + cat, "-map", "[v]", "-map", "[a]", "-r", "30",
   "-c:v", "libx264", "-preset", "fast", "-crf", "14", "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", f"{D}/base.mov")
ff("-i", f"{D}/base.mov", "-vn", "-ac", "1", "-ar", "48000",
   "-af", "highpass=f=90,afftdn=nr=10:nf=-34,lowpass=f=12000,acompressor=threshold=-20dB:ratio=2.5:attack=8:release=140:makeup=3,loudnorm=I=-16:TP=-1.5:LRA=9",
   f"{D}/voice.wav")
ff("-i", f"{D}/voice.wav", "-ac", "1", "-ar", "16000", f"{D}/voice16k.wav")

# 3. transcrição do áudio cortado (tempos já na linha do tempo final)
from faster_whisper import WhisperModel
mdl = WhisperModel("small", device="cpu", compute_type="int8", download_root="models", local_files_only=True)
segw, _ = mdl.transcribe(f"{D}/voice16k.wav", language="pt", word_timestamps=True, beam_size=5, vad_filter=False,
                         initial_prompt="Tiago Tessmann. Meta Ads, Google Ads, tráfego pago, inteligência artificial, IA, ChatGPT, anúncios, empresário, Máquina de Clientes, Conversão Extrema.")
W = [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3), "p": round(w.probability, 2)} for sg in segw for w in sg.words]
json.dump(W, open(f"{D}/words_cut.json", "w"), ensure_ascii=False)
print(len(W), "palavras"); print(" ".join(w["w"] for w in W))

# 4. rosto
import av, cv2
casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
c = av.open(f"{D}/base.mov"); vs = c.streams.video[0]; vs.thread_type = "AUTO"
out = []; last = None; k = 0
for fr in c.decode(vs):
    t = float(fr.pts * vs.time_base)
    if k % 3 == 0:
        g = fr.to_ndarray(format="gray"); sm = cv2.resize(g, (405, 720))
        f = casc.detectMultiScale(sm, 1.1, 4, minSize=(40, 40))
        if len(f):
            x, y, w, h = max(f, key=lambda r: r[2] * r[3]); last = (int(x * 4 + w * 2), int(y * 4 + h * 2), int(w * 4))
        if last: out.append({"t": round(t, 3), "cx": last[0], "cy": last[1], "w": last[2]})
    k += 1
json.dump(out, open(f"{D}/face_track.json", "w"))
ws = [o["w"] for o in out]; print("rosto: larg mediana", int(np.median(ws)), "de 1620")
