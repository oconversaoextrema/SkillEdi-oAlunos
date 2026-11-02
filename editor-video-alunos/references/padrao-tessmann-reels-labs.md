# Padrão Tessmann — Reels LABS (9:16) — 02/11/2026

O estilo LABS do YouTube (`padrao-tessmann-youtube.md`) levado para o Reels vertical. Motion com serifa, ícones 3D
e retícula, **na paleta do cenário da gravação**. A pessoa aparece muito, principalmente no começo, porque metade do
tempo é **tela dividida**: motion na metade de cima e a pessoa **recortada** embaixo, com o fundo dela dissolvendo
num degradê da cor do motion. **Não tem linha de divisão.** Alterna com a pessoa em tela cheia e com motion em tela
cheia. Sem legenda.

Formato: **1080x1920, 30 fps**, um arquivo só.

> **O que a skill entrega.** Corte e transcrição revisada, o recorte da pessoa (`work/recortar_pessoa.py`), o motion
> em **HyperFrames** (`work/modelos/hyperframes-labs-reels/index.html` como ponto de partida: é um vídeo inteiro de
> 1:35 já montado, sobre público semelhante na Meta) e a montagem final com `work/labs_reels_compor.py`.

---

## 1. Três modos, alternando

| modo | o que aparece | quando |
|---|---|---|
| **D — dividida** | motion na metade de cima (y 0–960) e a pessoa recortada embaixo | **abre o vídeo**; a maior parte do tempo; frases que explicam algo |
| **R — pessoa em tela cheia** | a pessoa, 1080x1920, sem nada por cima | blocos curtos de 1,5–3 s: pergunta direta, "né?", virada, fechamento |
| **M — motion em tela cheia** | só a animação | capítulos "Passo N", telas de app com cursor, a frase-chave, o CTA |

- **A pessoa precisa aparecer, principalmente no início.** Os primeiros ~15 s são D, com R no meio. Ela aparece em
  ~60 % do vídeo, somando D e R.
- Cada cena dura 1,5–4,5 s. Nunca mais de ~5 s parado no mesmo modo.
- **Punch-in** alternado 1,0 ↔ 1,1 a cada corte do bruto e a cada troca de modo.

## 2. A dividida sem linha (o detalhe que mais importa)

- Usar o **recorte com alfa** da pessoa: `python work/recortar_pessoa.py base.mp4 pessoa-rc.webm --degrade A B`,
  com o fundo transparente da orelha pra cima e o fundo real embaixo. A montagem usa uma faixa 1080x1080 do
  recorte, começando ~150 px acima do alto da cabeça (`recorte_topo` no json; um recorte já quadrado entra inteiro).
- O recorte vai em **y 900**. Por trás dele, um degradê que continua a cor do fundo do motion: a parede do vídeo
  dela aparece embaixo e some subindo. **Não pode ter linha.**
- **Erros já cometidos, não repetir:**
  - Fundir o vídeo inteiro (sem recorte) com um degradê deixa a emenda visível: a parede clara corta em linha.
  - "Descer" a pessoa repetindo as primeiras linhas do vídeo **duplica a cabeça** dentro do degradê.
  - Com o zoom crescendo a partir do centro, a cabeça sobe e cobre o fim do conteúdo de cima. Na montagem o
    punch-in cresce **pra baixo**.
- O conteúdo do motion na dividida tem que caber em **y 290–925**. No `index.html`, a tabela `DV` dá
  `[escala, deslocamento y]` por cena: meça a caixa do conteúdo e reduza até caber (largura ≤ 1000 px). Na dividida,
  rótulos pequenos ganham corpo (classes `.dv .k`, `.dv .lab`, `.dv .chip`), senão somem no celular.

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
- Transições: **clarão leitoso** quando entra motion vindo da pessoa e em capítulo, **chicote** entre motions,
  **desfoque** ao voltar pra pessoa. Cada uma com seu whoosh.
- Fade de 0,3 s no último quadro.

## 6. Áudio

Voz a −15 LUFS. Trilha contínua bem baixa (`nivel_trilha` 0,16 ≈ 16 dB abaixo da voz), sem voz na música. Muitos
efeitos curtos (pop, click, tick, shine) nos tempos das animações.

## 7. Passo a passo

1. Cortar as pausas e transcrever o áudio já cortado (`cortar_silencios.py`, `transcrever.py`). Revisar a transcrição.
2. Recortar a pessoa (`recortar_pessoa.py --degrade`). Conferir um quadro: cabeça inteira, fundo sumindo da orelha
   pra cima.
3. Planejar as cenas: lista `[início, fim, modo, capítulo]` nos tempos da fala, abrindo em D.
4. Escrever o motion no `index.html` do modelo (uma `.sc` por cena, com os mesmos tempos). Nas cenas D, acertar a
   tabela `DV`.
5. Fotografar o motion (`hyperframes snapshot`), conferir e renderizar (`hyperframes render ... --fps 30`).
6. Montar o `labs-reels.json` e tirar quadros: `python work/labs_reels_compor.py work/<video>/labs-reels.json --quadros 1.5,9.5,37.5`.
   Conferir a emenda da dividida em tamanho real.
7. Mostrar os quadros ao aluno e exportar só depois do OK: `python work/labs_reels_compor.py work/<video>/labs-reels.json`.

## 8. Conferência antes de entregar

- [ ] Abre em dividida, com a pessoa aparecendo.
- [ ] Nenhuma linha na emenda da dividida e nenhuma parte da pessoa repetida.
- [ ] A cabeça não encosta no conteúdo de cima, nem no punch-in.
- [ ] Cores das animações na paleta do cenário.
- [ ] Nada cortado na borda dos cards nem fora da metade de cima.
- [ ] Nada em inglês na tela (nome de produto, como "Advantage+", pode).
- [ ] Voz a −15 LUFS e trilha baixa até o fim.
