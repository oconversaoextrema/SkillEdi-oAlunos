"""Corte de pausas SEGURO: corta somente dentro de silêncio real, nunca em cima da fala.

Motivo: em 09/09/2026 o usuário apontou cortes "comendo palavra". A causa foi usar os
timestamps de palavra do whisper e um limiar de silêncio permissivo (-30 dB). O fim de uma
palavra decai abaixo de -30 dB enquanto ainda é audível, então o ponto de corte caía no
rabo da palavra ou já na entrada da seguinte.

Regras deste módulo:
  1. O silêncio é medido no áudio, com limiar ESTRITO (-38 dB por padrão).
  2. Só se corta DENTRO de um silêncio, respeitando uma margem de segurança nas duas bordas
     (120 ms por padrão). O corte nunca encosta na fala.
  3. Um silêncio só é cortado se, depois das margens, ainda sobrar pelo menos `min_remover`
     de material para tirar. Silêncio curto fica inteiro.
  4. Os timestamps do whisper NÃO são usados para decidir corte. Servem só para legenda.

Uso:
    from cortar_silencios import detectar_silencios, montar_segmentos
    sil = detectar_silencios(FF, "work/vX/clean.wav")
    segs, total = montar_segmentos(sil, dur_total, inicio_fala, fim_fala)
"""
import re, subprocess


def detectar_silencios_relativo(wav, dur_min=0.20, fator=0.28):
    """Pausas medidas em relação ao PISO DE RUÍDO da própria gravação.

    Limiar fixo em dB não serve para gravação com ruído de fundo (carro, rua): o piso sobe
    e nenhum silêncio é detectado. Aqui o limiar fica a `fator` do caminho entre o piso
    (percentil 10 do RMS) e o nível de fala (percentil 75).
    """
    import numpy as np, wave
    w = wave.open(wav); sr = w.getframerate()
    a = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float32) / 32768
    jan = int(0.02 * sr)
    rms = np.array([np.sqrt((a[i:i + jan] ** 2).mean() + 1e-12) for i in range(0, len(a) - jan, jan)])
    db = 20 * np.log10(rms + 1e-12)
    piso, fala = np.percentile(db, 10), np.percentile(db, 75)
    lim = piso + (fala - piso) * fator
    quieto = db < lim
    blocos, ini = [], None
    for i, q in enumerate(quieto):
        if q and ini is None: ini = i
        if not q and ini is not None:
            if (i - ini) * 0.02 >= dur_min: blocos.append((round(ini * 0.02, 3), round(i * 0.02, 3)))
            ini = None
    if ini is not None and (len(quieto) - ini) * 0.02 >= dur_min:
        blocos.append((round(ini * 0.02, 3), round(len(quieto) * 0.02, 3)))
    return blocos


def detectar_silencios(ffmpeg, wav, limiar_db=-38, dur_min=0.25):
    """Limiar absoluto. Só serve para gravação limpa. Em áudio com ruído use a versão relativa."""
    p = subprocess.run([ffmpeg, "-hide_banner", "-i", wav, "-af",
                        f"silencedetect=noise={limiar_db}dB:d={dur_min}", "-f", "null", "-"],
                       capture_output=True, text=True)
    nums = re.findall(r"silence_(start|end): ([0-9.]+)", p.stderr)
    sil, ini = [], None
    for tipo, val in nums:
        if tipo == "start": ini = float(val)
        elif ini is not None: sil.append((ini, float(val))); ini = None
    return sil


def montar_segmentos(silencios, dur_total, inicio_fala=None, fim_fala=None,
                     margem=0.12, pausa_alvo=0.22, min_remover=0.12,
                     entrada=0.20, saida=0.45):
    """Segmentos a manter. Corta só o excedente do miolo de cada silêncio.

    margem      : quanto de silêncio fica preservado colado em cada lado da fala.
    pausa_alvo  : pausa que sobra entre as frases depois do corte.
    min_remover : só corta se der para remover pelo menos isso; senão deixa o silêncio inteiro.
    """
    cortes = []          # trechos a REMOVER
    for s, e in silencios:
        util_i, util_f = s + margem, e - margem
        if util_f - util_i <= 0:
            continue                                   # silêncio curto: não encosta
        sobra = (e - s) - pausa_alvo                   # quanto daria para tirar
        if sobra < min_remover:
            continue                                   # não vale o risco
        meio = (s + e) / 2
        ini = max(util_i, meio - sobra / 2)
        fim = min(util_f, ini + sobra)
        if fim - ini >= min_remover:
            cortes.append((round(ini, 3), round(fim, 3)))

    ini_video = max(0.0, (inicio_fala - entrada)) if inicio_fala is not None else 0.0
    fim_video = min(dur_total, (fim_fala + saida)) if fim_fala is not None else dur_total
    segs, cur = [], ini_video
    for a, b in cortes:
        # silêncio de entrada/saída não é encurtado: a folga de `entrada`/`saida` fica inteira
        # (em 15/09/2026 o corte comia a folga e o vídeo abria com 0,15 s antes da fala)
        if a < ini_video + entrada or b > fim_video - saida: continue
        if b <= cur or a >= fim_video: continue
        a = max(a, cur)
        if a - cur > 0.05: segs.append((round(cur, 3), round(a, 3)))
        cur = b
    if fim_video - cur > 0.05: segs.append((round(cur, 3), round(fim_video, 3)))
    return segs, sum(e - s for s, e in segs)


def conferir(segs, silencios, tolerancia=0.06):
    """Confere que toda fronteira de corte caiu dentro de um silêncio real. Retorna os problemas."""
    ruins = []
    for k in range(len(segs) - 1):
        for rotulo, t in (("fim", segs[k][1]), ("inicio", segs[k + 1][0])):
            if not any(s - tolerancia <= t <= e + tolerancia for s, e in silencios):
                ruins.append((rotulo, k, t))
    return ruins
