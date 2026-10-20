# Pipeline técnico — padrão Tessmann

Manual para você rodar a edição na sua máquina. Tudo o que está aqui foi tirado dos scripts em `scripts/` desta skill. Se um número não aparece aqui, é porque não está medido no código — não invente.

## 1. Estrutura de pastas

Os scripts fazem `chdir` para a pasta-mãe deles. Ou seja: eles precisam morar em `work/` dentro da pasta do seu projeto, e todos os caminhos são relativos à raiz do projeto.

```
meu-projeto/
  brutos/                      vídeo original da câmera (nunca sobrescrever)
  saidas/                      entregas, com versão no nome (ex.: reel-x-v1.mp4)
  referencias/<nome-do-video>/ material real usado em cima (vídeos, prints, fotos) + fontes.md
  work/                        os scripts desta skill, copiados pra cá
    cortar_silencios.py
    criativo_prep.py
    criativo.py
    reels2.py
    baixar.py
    <id>/                      pasta de trabalho de cada vídeo (criada pelo prep)
    <id>/<id>.py               o config daquele vídeo (baseado nos exemplos)
  ferramentas/
    ffmpeg_path.txt            uma linha: caminho absoluto do binário ffmpeg
    fontes/TikTokSans-Variable.ttf
  models/                      cache do faster-whisper (modelo small)
  trilhas/efeitos/             film-transition-11.mov e film-transition-11.wav (transição do Reels)
```

Detalhes que o código exige:

| Caminho | Quem usa | Observação |
|---|---|---|
| `ferramentas/ffmpeg_path.txt` | `criativo_prep.py`, `criativo.py`, `baixar.py` | lido com `.read().strip()`; só o caminho, sem aspas |
| `ferramentas/fontes/TikTokSans-Variable.ttf` | `criativo.py` (constante `FONTE`) | precisa ser a **variável**; o código chama `set_variation_by_axes([36, 100, wght, 0])`, ou seja 4 eixos |
| `models/` | `criativo_prep.py` | `download_root="models"` |
| `trilhas/efeitos/film-transition-11.mov` e `.wav` | `reels2.py` (constante `BURN`) | só no padrão Reels |

Os exemplos `exemplo-criativo.py` e `exemplo-reel.py` fazem `sys.path.insert` de `".."` e importam `criativo` / `reels2`. Então o config de cada vídeo fica em `work/<id>/<id>.py`, um nível abaixo dos renderizadores.

## 2. Instalação

Feita pelo instalador da skill (Passo 0 do SKILL.md): `bash scripts/instalar.sh` (Windows: `scripts\instalar.ps1`).
Ele cria o Python 3.12 com todas as bibliotecas, o ffmpeg, o modelo Whisper `small` e as fontes em `~/.editor-video`.
Depois, `scripts/novo_projeto.py <pasta>` monta a estrutura acima: copia os scripts para `work/`, grava
`ferramentas/ffmpeg_path.txt` e liga `models/` e `ferramentas/fontes/` (com a `TikTokSans-Variable.ttf`) às pastas
instaladas. Rodar os scripts sempre com o Python das ferramentas: `~/.editor-video/venv/bin/python`.

Fonte: a **TikTok Sans** variável já vem do instalador (`ferramentas/fontes/TikTokSans-Variable.ttf`). Um `.ttf` estático não serve: o código muda o peso pelos eixos da variável (a legenda usa peso 500 no Reels e 650 no criativo; o título usa 700).

Transição do Reels: os dois arquivos `trilhas/efeitos/film-transition-11.mov` e `.wav` **não vêm com a skill** (são de um pack pago). Sem eles, ponha um overlay seu com esses nomes, aponte o campo `burn` do config para os seus arquivos (item 6) ou use `burn=None` para cortar seco na virada.

Bruto: grave **vertical 9:16**. O prep faz `scale=1620:2880` sem preservar proporção; um bruto 16:9 sai esticado.

Whisper: o modelo `small` já vem baixado pelo instalador (`models/` aponta para `~/.editor-video/models`). O `criativo_prep.py` usa `local_files_only=True`: nunca tenta rede.

## 3. Passo a passo de uma edição

### 3.1 Prep (uma vez por vídeo)

```bash
python work/criativo_prep.py r1 brutos/IMG_0001.MOV
```

`r1` é o **id** do vídeo (vira a pasta `work/r1/`). O prep faz, nessa ordem:

1. detecta silêncios pelo piso de ruído da própria gravação (`detectar_silencios_relativo`, `dur_min=0.20`, `fator=0.42`) e monta os segmentos a manter (`margem=0.07`, `pausa_alvo=0.12`, `min_remover=0.10`, `entrada=0.20`, `saida=0.45`). `conferir()` trava com `assert` se algum corte cair fora de silêncio;
2. gera `base.mov` em 1620x2880, 30 fps, com a grade fixa `eq=contrast=1.32:saturation=1.28:gamma=0.97`, `colorbalance`, `unsharp=5:5:0.6`;
3. trata a voz (highpass 90 Hz, afftdn, lowpass 12 kHz, compressor, `loudnorm=I=-16:TP=-1.5:LRA=9`) em `voice.wav`;
4. transcreve o áudio **já cortado** com faster-whisper `small` (pt, `word_timestamps=True`, `beam_size=5`);
5. rastreia o rosto com Haar cascade a cada 3 quadros.

O `initial_prompt` do whisper (no passo 3 do `criativo_prep.py`) vem com nomes e termos do nicho de marketing; troque pelos nomes próprios, marcas e jargões **do seu** vídeo — é o que faz a transcrição acertar palavra difícil.

No fim ele imprime a duração antes/depois, o número de palavras, a transcrição inteira e a largura mediana do rosto.

### 3.2 Conferir a transcrição

Leia a transcrição impressa. Toda palavra errada vira uma entrada no campo `repl` do config (item 3.3). Nada de legenda com erro: o render trava se o texto das frases não bater com as palavras.

### 3.3 Montar o config do vídeo

Crie `work/<id>/<id>.py` copiando o exemplo do padrão certo. Campos:

**Comuns aos dois padrões**

| Campo | O que é |
|---|---|
| `id` | mesmo id do prep; aponta para `work/<id>/` (base.mov, voice.wav, words_cut.json, face_track.json, cuts.json) |
| `ref` | pasta do material real, ex.: `referencias/reel-x` |
| `saida` | caminho do mp4, ex.: `saidas/reel-x-v1.mp4` |
| `repl` | correções da transcrição: `{indice: (n_tokens, [novas_palavras])}`. O índice é a posição em `words_cut.json`; `n_tokens` é quantas palavras originais serão substituídas; o tempo delas é dividido igualmente entre as novas |
| `frases` | o texto inteiro, com `\|` separando cada bloco de legenda e quebra de linha entre parágrafos. Blocos por unidade de sentido: 1–4 palavras no criativo, 1–3 no Reels (~0,7 s cada). **Tem que cobrir todas as palavras**, na mesma ordem |
| `enquadro` | `lambda t: (zoom, face_at)` da tela cheia. Padrão: `(1.32, 0.33)` no criativo, `(1.15, 0.33)` no Reels |
| `legenda_desde` | palavra depois da qual a legenda começa. No criativo, o padrão é a última palavra antes de `t_titulo`. No Reels, se você não passar, a legenda começa da primeira palavra |

**Só no criativo (`criativo.py`)**

| Campo | O que é |
|---|---|
| `titulo` | lista de linhas (Bold 64, passo 70), centrada na divisória |
| `t_gancho` | segundo do corte seco: tela dividida → tela cheia |
| `t_titulo` | segundo em que o título some e a legenda começa |
| `gancho` | `[(t0, t1, arquivo, foco_vertical, recorte_ou_None), ...]` — material na área de baixo durante o gancho |
| `cutaways` | mesmo formato; voltas à tela dividida no miolo |
| `variante` | `'dividida'` (padrão) ou `'inteira'` (tela cheia do primeiro quadro ao fim, sem material). Mesmo na `'inteira'`, `t_gancho`, `t_titulo` e `titulo` continuam obrigatórios (sem eles o render dá `KeyError`); o título aparece sobre a tela cheia até `t_titulo` |
| `yt` | layout do formato YT: `'central'` (padrão — composição 4:5 reduzida pra 864x1080 com laterais pretas), `'coluna'` ou `'painel'` |

Formatos disponíveis no criativo (largura, altura, divisória): RL 1080x1920 / 960, IN 1080x1350 / 675, GL 1080x1080 / 600, YT 1920x1080 / 960.

**Só no Reels (`reels2.py`)**

| Campo | O que é |
|---|---|
| `t_cheia` | segundo em que a dividida vira tela cheia (o corte cai no pico do flash) |
| `topo` | lista de itens da área de cima, montados com os atalhos `V()` e `I()` |
| `burn` | dict da transição; padrão `film-transition-11.mov`, `ini=0.0`, `pico=0.40`, `dur=1.12`, `wav=...`, `vol=0.45`. `burn=None` desliga a transição (corte seco em `t_cheia`) |

Atalhos do `exemplo-reel.py`:

```python
V = lambda t0, t1, src, ini, foco=0.5, rec=None: dict(t0=t0, t1=t1, tipo="video", src=src, ini=ini, foco=foco, rec=rec)
I = lambda t0, t1, src, rec=None, foco=0.0: dict(t0=t0, t1=t1, tipo="img", src=src, rec=rec, foco=foco)
```

- `t0`/`t1`: janela na linha do tempo do vídeo final.
- `src`: nome do arquivo dentro de `ref`.
- `ini` (só vídeo): segundo de onde começar a tocar dentro daquele clipe.
- `foco`: 0 = topo, 1 = base, no corte vertical.
- `rec`: recorte `(x0, y0, x1, y1)` na resolução do arquivo original — use pra tirar lower-third, legenda queimada, barra de relógio.
- Os itens do `topo` precisam cobrir toda a faixa de 0 até `t_cheia` sem buraco: segundo sem item nenhum sai com a área de cima preta.
- Existe também `tipo="card"`, com `linhas=[(texto, tamanho_px, peso), ...]`, que desenha um card off-white com texto escuro.

Dois detalhes do Reels: a legenda só aparece depois de 10 s (`SEM_LEGENDA_ATE = 10.0`), e o material de cima leva um realce leve (saturação 1,18 / contraste 1,10) que **não** é aplicado em arquivo `.png` — deixe prints de notícia em `.png`.

### 3.4 Render

Rodar sempre da raiz do projeto.

Conferir os blocos de legenda com o tempo de cada um (funciona nos dois padrões):

```bash
python work/r1/r1.py --blocos
```

Tirar quadros de prévia em segundos específicos (vão para `work/<id>/prev/`):

```bash
python work/r1/r1.py --stills 0.5,3.2,12.0
```

Render final do Reels (só formato RL, 1080x1920):

```bash
python work/r1/r1.py
```

Criativo — RL é o padrão; os outros formatos saem com `--formatos`, e o nome do arquivo ganha o sufixo do formato:

```bash
python work/c1/c1.py                       # RL
python work/c1/c1.py --formatos IN,GL      # gera ...-IN.mp4 e ...-GL.mp4
python work/c1/c1.py --formatos IN --stills 2.0,8.0
```

No criativo, `--formatos` tem que vir **antes** de `--stills`/`--blocos`. Saída em H.264 CRF 19, preset medium, áudio AAC 192k, `+faststart`. O fade para preto (0,3 s) fecha em `T_END = min(total do cuts.json, última palavra + 0,5 s)`; o render continua escrevendo os quadros restantes do `base.mov`, que saem pretos. Se sobrar preto demais no fim, é sinal de que o `total` do corte ficou bem maior que a última palavra.

### 3.5 Conferência final

Assista inteiro, com som. Confira: nenhum corte comendo palavra; a legenda batendo com a fala; o material de cima mostrando exatamente o que está sendo dito naquele segundo; nenhum clipe repetido; o rosto centrado sem tremer; a transição caindo no ponto do corte. Achou erro, corrige o config e renderiza uma versão nova — `saidas/...-v2.mp4`, sem sobrescrever a anterior.

## 4. Arquivos intermediários (`work/<id>/`)

| Arquivo | Para que serve |
|---|---|
| `voz16k.wav` | áudio mono 16 kHz do bruto, só para detectar os silêncios |
| `cuts.json` | `segs` (trechos mantidos), `total` (duração final), `sil` (silêncios), `dur` (duração do bruto). O render lê `total` para saber onde o vídeo acaba |
| `base.mov` | vídeo já cortado, 1620x2880, com a grade de cor aplicada. É a fonte de imagem do render (o zoom até ~1,5 não perde nitidez) |
| `voice.wav` | áudio tratado e normalizado; é o áudio do mp4 final |
| `voice16k.wav` | versão 16 kHz do tratado, entrada do whisper |
| `words_cut.json` | palavras com `s`/`e`/`p` já na linha do tempo do corte. Base da legenda e dos índices de `repl` |
| `face_track.json` | `t`, `cx`, `cy`, `w` do rosto ao longo do `base.mov`. O render passa por `rosto_suave()` antes de usar |

Apagou algum? É só rodar o prep de novo — ele regenera tudo.

## 5. Material de referência

Baixe só o trecho que vai usar:

```bash
python work/baixar.py URL referencias/reel-x                       # vídeo inteiro
python work/baixar.py URL referencias/reel-x 12.0 20.0 cnn-fulano  # trecho 12–20 s, nome do arquivo
```

Ele pega H.264 até 1080p com áudio e mescla em mp4; imprime o caminho do arquivo salvo.

Depois registre em `referencias/<nome-do-video>/fontes.md`: URL, autor/veículo, data e em que momento do vídeo o material aparece. Material de terceiros vai com atribuição legível na tela. Nunca apresente uma imagem inventada como real — não achou, diga que não achou.

## 6. Se der errado

**`SyntaxError` estranho ou biblioteca não encontrada** — você está no Python errado. Ative o venv (`source .venv/bin/activate`) e confira com `python -V` (tem que ser 3.11+).

**`FileNotFoundError: ferramentas/ffmpeg_path.txt`, ou o ffmpeg não roda** — refaça o arquivo com o comando do item 2 e confirme que o caminho existe e é executável. Erro de permissão: `chmod +x "$(cat ferramentas/ffmpeg_path.txt)"`.

**Whisper reclama de modelo ausente** — é o `local_files_only=True`. Rode uma vez com `False` pra ele baixar o `small` para `models/` e volte para `True`.

**Corte comendo palavra** — o `assert not ruins` do prep já barra corte fora de silêncio. Se ainda assim ficou apertado, aumente `margem` e `pausa_alvo` na **chamada** de `montar_segmentos` dentro do `criativo_prep.py` (a função em si mora no `cortar_silencios.py`) ou baixe o `fator` de `detectar_silencios_relativo`, e rode o prep de novo.

**Câmera bugada / rosto pulando** — detecção falsa. O render já passa a trilha por `rosto_suave()`, que joga fora salto acima de 380 px ou tamanho fora de 45% da mediana local, interpola os buracos, suaviza e limita a velocidade a 260 px/s. Se ainda pular, edite a chamada de `rosto_suave()` no `criativo.py` / `reels2.py` com janela maior (`n`) ou `vmax` menor — não dá para passar isso pelo config.

**`baixar.py` falha com início/fim** — alguns links não aceitam `--download-sections`. Baixe o vídeo inteiro (sem os dois tempos) e recorte o trecho no config, com `ini` no `V()`.

**Transição do Reels: `.mov`/`.wav` não encontrado** — aponte no config para um overlay seu:

```python
burn=dict(src="trilhas/efeitos/meu-overlay.mov", ini=0.0, pico=0.40, dur=1.12,
          wav="trilhas/efeitos/meu-overlay.wav", vol=0.45)
```

Se você não tem overlay nenhum, coloque `burn=None` no config: o render corta seco para a tela cheia em `t_cheia`, sem overlay e sem o som dele.

**Render trava com `'palavra' != 'outra' em N`** — o texto de `frases` não bate com a transcrição naquela posição. Corrija a palavra em `frases` ou conserte a transcrição via `repl`. Se aparecer `sobraram palavras: ...` (no Reels a mensagem é só `sobraram: ...`), faltou incluir o fim da fala em `frases`.
