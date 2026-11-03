# Padrão Tessmann — Reels LABS (9:16) — 02/11/2026, revisto 03/11/2026 (aprovado)

O estilo LABS do YouTube (`padrao-tessmann-youtube.md`) levado para o Reels vertical. Motion com serifa, ícones 3D
e retícula, **na paleta do cenário da gravação**. A pessoa aparece muito, principalmente no começo, porque metade do
tempo é **tela dividida normal**: motion na metade de cima (1080x960) e a pessoa na metade de baixo (1080x960).
Alterna com a pessoa em tela cheia e com motion em tela cheia. Sem legenda. Transições com clarão, chicote e desfoque,
cada uma com um clique (orgânico ou "mágico"), e efeitos curtos nas animações, tudo baixinho.

> **Versão aprovada (03/11/2026).** A primeira versão (02/11) usava a pessoa **recortada** sobre um degradê, sem linha.
> Foi trocada pela dividida **normal**, que é a aprovada: não use mais o recorte na dividida.

Formato: **1080x1920, 30 fps**, um arquivo só.

> **O que a skill entrega.** Corte e transcrição revisada, o motion
> em **HyperFrames** (`work/modelos/hyperframes-labs-reels/index.html` como ponto de partida: é um vídeo inteiro de
> 1:35 já montado, sobre público semelhante na Meta) e a montagem final com `work/labs_reels_compor.py`.

---

## 1. Três modos, alternando

| modo | o que aparece | quando |
|---|---|---|
| **D — dividida** | motion na metade de cima (y 0–960) e a pessoa embaixo (y 960–1920) | **abre o vídeo**; a maior parte do tempo; frases que explicam algo |
| **R — pessoa em tela cheia** | a pessoa, 1080x1920, sem nada por cima | blocos curtos de 1,5–3 s: pergunta direta, "né?", virada, fechamento |
| **M — motion em tela cheia** | só a animação | capítulos "Passo N", telas de app com cursor, a frase-chave, o CTA |

- **A pessoa precisa aparecer, principalmente no início.** Os primeiros ~15 s são D, com R no meio. Ela aparece em
  ~60 % do vídeo, somando D e R.
- Cada cena dura 1,5–4,5 s. Nunca mais de ~5 s parado no mesmo modo.
- **Punch-in** alternado 1,0 ↔ 1,1 a cada corte do bruto e a cada troca de modo.

## 2. A dividida normal

- Metade de cima: o motion (y 0–960). Metade de baixo: a pessoa enquadrada em 1080x960, **cabeça inteira com folga
  em cima e rosto a ~1/3 da altura**. Uma sombra suave de ~40 px no alto da metade de baixo (a montagem faz) tira a
  emenda seca. Nada de borda, moldura ou fundo desfocado nas laterais.
- **Bruto deitado (16:9)**: gere um vídeo próprio da metade (`"metade"` no json), cortado do quadro deitado em volta
  do rosto. Dá mais folga que cortar do vertical e é o que foi aprovado.
- **Bruto em pé (9:16)**: a montagem corta a faixa 1080x960 do próprio vídeo (`"metade_topo"`, ~150 px acima do alto
  da cabeça).
- Na tela cheia (R) a pessoa precisa estar **centrada**: se o bruto é deitado, corte a faixa 9:16 pelo centro do
  rosto (x0 = centro do rosto − metade da largura do corte), nunca por um valor fixo. Conferir em vários momentos.
- O conteúdo do motion na dividida tem que caber em **y 290–925**. No `index.html`, a tabela `DV` dá
  `[escala, deslocamento y]` por cena: meça a caixa do conteúdo e reduza até caber (largura ≤ 1000 px, margem ≥ 70 px
  dos lados). Na dividida, rótulos pequenos ganham corpo (classes `.dv .k`, `.dv .lab`, `.dv .chip`), senão somem
  no celular.
- Título em serifa grande demais estoura na dividida (a escala do `DV` aumenta tudo até 1,1x): frase de 2–3 palavras
  a 90–110 px; nome comprido (marca, produto) a 90 px ou com o rótulo `.k` em cima.

## 3. Cores: a paleta do cenário

As animações usam as cores da **luz e do fundo da gravação**, não um coral fixo. Tire 5 tons do vídeo da pessoa.
No estúdio do Tiago (luz âmbar, parede escura):

| uso | cor |
|---|---|
| fundo mais escuro | `#1A120B` |
| fundo / vidro dos cards | `#3D2314` |
| cobre (avatares, tons médios) | `#8C4F2B` |
| destaque (ícones, botões, números) | `#D97724` |
| destaque claro (brilho, texto em destaque) | `#F2A65A` |

- Fundos de cena: marrom-escuro com uma luz alaranjada vindo de cima.
- Cards de vidro e janelas de app em marrom translúcido. Cards claros (resultado, planilha) em creme quente `#FBF1E4`.
- Texto secundário em bege quente, nunca cinza frio.
- Ficam fora da paleta: o **vermelho do "não"** (✗, valor zerado) e o **verde do "ok"**.
- O clarão das transições é creme quente, não cinza.
- Fundos alternando entre as cenas: marrom (`.marrom`), quase preto (`.preto`) e o escuro-azulado quente (`.azul`).

## 4. Motion (`work/modelos/hyperframes-labs-reels`)

- **Newsreader** (serifa) nos números e títulos, **Inter** nos rótulos. Ícones em quadrado 3D (`.sq` com `.in`
  laranja). Rótulo em versalete espaçado (`.k`) em cima do título.
- Cada cena "vive": zoom lento de câmera 1 → 1,045. As peças entram na hora da palavra, com pop, contador ou cursor
  clicando.
- Capítulos: cartão **"Passo N"** em tela cheia (`passo(n, a, b)`).
- Fala de passo a passo em app: tela recriada com cursor branco clicando no item citado.
- CTA no fim: card de perfil com o link destacado e o cursor clicando.
- Dados de exemplo (nomes, e-mails, números) são inventados: avisar o aluno.
- **Nada cortado no card**: conferir quadro a quadro a borda dos cards e da metade de cima.

## 5. Acabamento e transições (a montagem faz)

- Só no motion: retícula de pontinhos a 45° nos tons médios, aberração de 1 px, glow leve, grão quase zero, vinheta.
- Transições (aprovadas): **clarão leitoso** quando entra motion vindo da pessoa e em capítulo, **chicote** entre
  motions, **desfoque** ao voltar pra pessoa.
- Som das transições: **clique "mágico"** (`click-magico.wav`) no clarão e **clique orgânico com reverb**
  (`click-organico.wav`, 5 variações dentro do arquivo, uma de cada vez) no chicote e no desfoque. Whoosh comprido
  não: soa velho.
- Fade de 0,3 s no último quadro.

## 6. Áudio

- Voz a −15 LUFS. Trilha contínua bem baixa (`nivel_trilha` 0,16 ≈ 16 dB abaixo da voz), sem voz na música, com
  fade de 1,5 s no fim.
- Efeitos curtos (pop, click, tick, sucesso) **nos tempos das animações** do `index.html`: cada `pop()`, clique de
  cursor, check ou contador ganha um som. Onde antes ia um whoosh ou brilho, use o clique orgânico (`"organico"`,
  ganho ~1,3) ou o mágico (`"magico"`, ganho ~0,3).
- **Todos os efeitos baixos**: `sfx_ganho` 0,5 (−6 dB em tudo). Efeito não pode competir com a voz.
- Os sons ficam em `trilhas/efeitos/` (`efeitos_dir`). `click-organico.wav` e `click-magico.wav` precisam existir
  com esses nomes; sem eles a montagem avisa e segue sem o som da transição. Use cliques seus com os mesmos nomes.
- **Monte a lista `efeitos` a partir das animações DESTE vídeo.** Copiar a lista de outro vídeo deixa os sons fora
  do lugar.

## 7. Passo a passo

1. Cortar as pausas e transcrever o áudio já cortado (`cortar_silencios.py`, `transcrever.py`). Revisar a transcrição.
2. Enquadrar a pessoa: tela cheia 1080x1920 centrada no rosto e, se o bruto é deitado, o vídeo da metade 1080x960.
   Conferir quadros em vários momentos: cabeça inteira, rosto centrado.
3. Planejar as cenas: lista `[início, fim, modo, capítulo]` nos tempos da fala, abrindo em D.
4. Escrever o motion no `index.html` do modelo (uma `.sc` por cena, com os mesmos tempos). Nas cenas D, acertar a
   tabela `DV`.
5. Fotografar o motion (`hyperframes snapshot`), conferir e renderizar (`hyperframes render ... --fps 30`).
6. Montar o `labs-reels.json` e tirar quadros: `python work/labs_reels_compor.py work/<video>/labs-reels.json --quadros 1.5,9.5,37.5`.
   Conferir a dividida em tamanho real: conteúdo de cima inteiro, cabeça com folga embaixo.
7. Mostrar os quadros ao aluno e exportar só depois do OK: `python work/labs_reels_compor.py work/<video>/labs-reels.json`.

## 8. Conferência antes de entregar

- [ ] Abre em dividida, com a pessoa aparecendo.
- [ ] Dividida normal: pessoa preenchendo a metade de baixo, cabeça inteira, rosto centrado (também na tela cheia).
- [ ] Cores das animações na paleta do cenário.
- [ ] Nada cortado na borda dos cards nem fora da metade de cima.
- [ ] Nada em inglês na tela (nome de produto, como "Advantage+", pode).
- [ ] Voz a −15 LUFS e trilha baixa até o fim.
- [ ] Efeitos nos tempos das animações deste vídeo, baixos (−6 dB); clique mágico no clarão, orgânico no chicote e
      no desfoque.
