"""Renderizador do PADRÃO REELS 2 (references/padrao-reels-2.md), medido nos Reels do próprio usuário.

Dividida do quadro 1 (divisória y 899) com material real em cima (vídeo, imagem, card) até `t_cheia`;
flash quente de 11 quadros; apresentador em tela cheia até o fim. Sem título. Legenda TikTok Sans
wght 500 ~59 px tracking −30, centrada na divisória / em 58 % na cheia, blocos de 1–3 palavras.

CFG: id, ref, saida, t_cheia, repl, frases, enquadro, topo=[dict(t0,t1,tipo='video'|'img'|'card', ...)]
  video: src, ini (segundo de início dentro do clipe), foco
  img:   src, rec (recorte opcional), foco
  card:  linhas=[(texto, tamanho_px, wght), ...]
Uso: python work/rN/rN.py [--stills t,t | --blocos]
"""
import json, os, sys, functools
import numpy as np
import av
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import criativo as C
from criativo import tk, cobrir, carregar_palavras, montar_blocos, com_sombra, cl, ease, lerp
from PIL import ImageEnhance

W, H, FPS = 1080, 1920, 30
SPLIT = 899
WHITE = (255, 255, 255); CARD_BG = (242, 242, 242); CARD_INK = (1, 1, 1)
LEG_SIZE, LEG_WGHT, LEG_TRACK = 59, 500, -30          # Premiere: TikTok Sans Medium 55, tracking -30
LEG_BASE_DIV, LEG_BASE_CHEIA = 912, 1130               # medido: texto y 871–924 na dividida, 1087–1142 na cheia
# Transição (uma vez só, na virada dividida -> cheia), em modo TELA (screen) como ele usa no Premiere, com o som do overlay.
# Padrão desde 18/09/2026: "_11.mov" do Essencial Pack (Film Transitions), 1,12 s, pico branco em +0,40 s = corte. Volume baixo.
# Alternativa usada no Reel "editado por IA": film-burn-overlay.mp4 (trecho 13,60 s, pico +0,31 s, dur 0,90 s).
BURN = dict(src="trilhas/efeitos/film-transition-11.mov", ini=0.0, pico=0.40, dur=1.12, wav="trilhas/efeitos/film-transition-11.wav", vol=0.45)

def texto_track(d, x, base, txt, f, fill, track):
    """Desenha com tracking (milésimos de em) — Pillow não tem tracking nativo."""
    dx = track * f.size / 1000
    for ch in txt:
        d.text((x, base), ch, font=f, fill=fill, anchor="ls"); x += f.getlength(ch) + dx
def larg_track(txt, f, track):
    return sum(f.getlength(c) for c in txt) + track * f.size / 1000 * (len(txt) - 1)

SEM_LEGENDA_ATE = 10.0   # pedido 15/09: "nos primeiros 10 s deixa sem legenda, que vou colocar uma manualmente. Sempre."

def legenda(img, blocos, t, cheia):
    if t < SEM_LEGENDA_ATE: return
    b = next((x for x in blocos if x["s"] <= t < x["e"]), None)
    if not b: return
    f = tk(LEG_SIZE, LEG_WGHT)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    texto_track(d, (W - larg_track(b["txt"], f, LEG_TRACK)) / 2, LEG_BASE_CHEIA if cheia else LEG_BASE_DIV, b["txt"], f, WHITE, LEG_TRACK)
    com_sombra(img, lay, 0.55, 6, 2)

def card(linhas, w, h):
    """Card off-white com texto escuro centrado (medido: 8.000 em ~270 px Bold, frases ~72 px)."""
    im = Image.new("RGB", (w, h), CARD_BG); d = ImageDraw.Draw(im)
    fontes = [tk(s, wg) for _, s, wg in linhas]
    alturas = [f.getmetrics()[0] + f.getmetrics()[1] for f in fontes]
    gap = 14; total = sum(alturas) + gap * (len(linhas) - 1); y = (h - total) / 2
    for (txt, s, wg), f, alt in zip(linhas, fontes, alturas):
        d.text(((w - f.getlength(txt)) / 2, y + f.getmetrics()[0]), txt, font=f, fill=CARD_INK, anchor="ls"); y += alt + gap
    return im

class ClipeVideo:
    """Leitura sequencial de um clipe (t só cresce durante o render)."""
    def __init__(self, src, ini):
        self.c = av.open(src); self.s = self.c.streams.video[0]; self.s.thread_type = "AUTO"
        self.ini = ini; self.it = self.c.decode(self.s); self.ult = None; self.ult_t = -1
        self.c.seek(int(max(0, ini - 1) / self.s.time_base), stream=self.s, backward=True); self.it = self.c.decode(self.s)
    def quadro(self, tau):
        alvo = self.ini + tau
        while self.ult_t < alvo:
            try: fr = next(self.it)
            except StopIteration: break
            self.ult_t = float(fr.pts * self.s.time_base); self.ult = fr
        return self.ult.to_image() if self.ult is not None else Image.new("RGB", (16, 16), (0, 0, 0))

def realce(im, sat=1.18, con=1.10):
    """Leve realce de cor/contraste no material de cima (vídeo e foto). Não aplicar em print de notícia."""
    im = ImageEnhance.Color(im.convert("RGB")).enhance(sat)
    return ImageEnhance.Contrast(im).enhance(con)

def flash_layer(k):
    """k em [0,1): clarão quente com textura radial (light leak)."""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    a = int(255 * k)
    base = Image.new("RGBA", (W, H), (255, 208, 90, int(a * 0.74)))   # referência: lavagem amarela com a imagem visível por baixo
    grad = Image.radial_gradient("L").resize((W * 2, W * 2)).crop((W // 2, W // 2 + 200, W // 2 + W, W // 2 + 200 + H))
    grad = grad.point(lambda v: 255 - v).filter(ImageFilter.GaussianBlur(40))
    quente = Image.new("RGBA", (W, H), (255, 170, 60, 0)); quente.putalpha(grad.point(lambda v: int(v * k * 0.45)))
    lay.alpha_composite(base); lay.alpha_composite(quente)
    return lay

def rodar(CFG):
    D = f"work/{CFG['id']}"; REF = CFG["ref"]
    WORDS = carregar_palavras(D, CFG.get("repl", {}))
    T_END = min(json.load(open(f"{D}/cuts.json"))["total"], WORDS[-1]["e"] + 0.5)
    BLOCOS = montar_blocos(WORDS, CFG["frases"], CFG.get("legenda_desde", "__inicio__"), T_END) if CFG.get("legenda_desde") else _blocos_do_inicio(WORDS, CFG["frases"], T_END)
    enq = CFG.get("enquadro", lambda t: (1.15, 0.33))
    T_CHEIA = CFG["t_cheia"]

    ft, cx, cy = C.rosto_suave(json.load(open(f"{D}/face_track.json")))
    def face(t): return float(np.interp(t, ft, cx)), float(np.interp(t, ft, cy))
    src_c = av.open(f"{D}/base.mov"); VS = src_c.streams.video[0]; VS.thread_type = "AUTO"; SW, SH = VS.width, VS.height
    def frames():
        for fr in src_c.decode(VS): yield fr.to_image()
    def presenter(src, t, y0, rh, zoom, face_at):
        cw = SW / zoom; ch = cw * rh / W
        if ch > SH: ch = SH; cw = ch * W / rh
        fx, fy = face(t)
        left = max(0, min(SW - cw, fx - cw / 2)); top = max(0, min(SH - ch, fy - ch * face_at))
        return src.crop((int(left), int(top), int(left + cw), int(top + ch))).resize((W, rh), Image.LANCZOS)

    clipes = {}
    @functools.lru_cache(32)
    def img_ref(n): return Image.open(f"{REF}/{n}").convert("RGB")
    def topo(img, t):
        for i, it in enumerate(CFG["topo"]):
            if it["t0"] <= t < it["t1"]:
                if it["tipo"] == "card":
                    img.paste(card(it["linhas"], W, SPLIT), (0, 0))
                elif it["tipo"] == "img":
                    im = img_ref(it["src"]); im = im.crop(it["rec"]) if it.get("rec") else im
                    push = lerp(1.0, 1.04, (t - it["t0"]) / max(0.4, it["t1"] - it["t0"]))
                    q = cobrir(im, W, SPLIT, it.get("foco", 0.5), push)
                    img.paste(realce(q) if it.get("realce", not it["src"].endswith(".png")) else q, (0, 0))
                else:
                    if i not in clipes: clipes[i] = ClipeVideo(f"{REF}/{it['src']}", it.get("ini", 0))
                    q = clipes[i].quadro(t - it["t0"]); q = q.crop(it["rec"]) if it.get("rec") else q
                    img.paste(realce(cobrir(q, W, SPLIT, it.get("foco", 0.5))), (0, 0))
                return
    burn = [None]
    def compose(src, t):
        cheia = t >= T_CHEIA - 1e-6                    # corte no pico do burn
        img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
        if cheia:
            z, fa = enq(t); img.paste(presenter(src, t, 0, H, z, fa), (0, 0))
        else:
            topo(img, t); img.paste(presenter(src, t, SPLIT, H - SPLIT, 1.0, 0.50), (0, SPLIT))
        legenda(img, BLOCOS, t, cheia)
        B = CFG.get("burn", BURN); t0 = (T_CHEIA - B["pico"]) if B else 0.0
        if B and t0 <= t < t0 + B["dur"]:           # overlay em modo tela: 1 - (1-a)(1-b)
            if burn[0] is None: burn[0] = ClipeVideo(B["src"], B["ini"])
            b = np.asarray(burn[0].quadro(t - t0).resize((W, H), Image.BILINEAR).convert("RGB")).astype(np.uint16)
            a = np.asarray(img.convert("RGB")).astype(np.uint16)
            img = Image.fromarray((255 - ((255 - a) * (255 - b) // 255)).astype(np.uint8)).convert("RGBA")
        if t > T_END - 0.3:
            ImageDraw.Draw(img).rectangle((0, 0, W, H), fill=(0, 0, 0, int(255 * ease((t - (T_END - 0.3)) / 0.3))))
        return img.convert("RGB")

    if sys.argv[1:2] == ["--blocos"]:
        for b in BLOCOS: print(f"{b['s']:6.2f}-{b['e']:6.2f}  {b['txt']}")
        return
    if sys.argv[1:2] == ["--stills"]:
        want = sorted(float(x) for x in sys.argv[2].split(",")); os.makedirs(f"{D}/prev", exist_ok=True); i = 0
        for n, src in enumerate(frames()):
            t = n / FPS
            while i < len(want) and want[i] <= t + 1e-6:
                compose(src, t).save(f"{D}/prev/t{want[i]:06.2f}.png"); i += 1
            if i >= len(want): break
        print("prévias:", i); return
    import subprocess
    out = CFG["saida"]
    B = CFG.get("burn", BURN)
    # burn=None no config (ou sem o .mov/.wav da transição): renderiza sem overlay e sem o som dele.
    som = ["-i", B["wav"]] if B else []
    mix = ["-filter_complex", f"[2]adelay={int((T_CHEIA - B['pico']) * 1000)}|{int((T_CHEIA - B['pico']) * 1000)},volume={B.get('vol', 0.45)}[b];[1][b]amix=inputs=2:duration=first:normalize=0[a]",
           "-map", "0:v", "-map", "[a]"] if B else ["-map", "0:v", "-map", "1:a"]
    p = subprocess.Popen([C.FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", f"{D}/voice.wav", *som, *mix,
                          "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", out], stdin=subprocess.PIPE)
    for n, src in enumerate(frames()):
        p.stdin.write(compose(src, n / FPS).tobytes())
        if n % 600 == 0: print(n, flush=True)
    p.stdin.close(); p.wait(); print("saída:", out, p.returncode)

def _blocos_do_inicio(WORDS, frases, t_end):
    """Legenda desde a primeira palavra (Reels não têm título)."""
    from criativo import norm
    lista = [p.strip() for ln in frases.strip().split("\n") for p in ln.split("|") if p.strip()]
    k = 0; blocos = []
    for fr in lista:
        toks = fr.split(); ws = WORDS[k:k + len(toks)]
        for a, b in zip(toks, ws):
            assert norm(a) == norm(b["w"]), f"'{a}' != '{b['w']}' em {k} ({' '.join(x['w'] for x in WORDS[k-2:k+5])})"
        blocos.append({"txt": fr, "s": ws[0]["s"], "e": ws[-1]["e"]}); k += len(toks)
    assert k == len(WORDS), f"sobraram: {' '.join(w['w'] for w in WORDS[k:])}"
    for a, b in zip(blocos, blocos[1:]): a["e"] = b["s"]
    blocos[-1]["e"] = t_end
    return blocos
