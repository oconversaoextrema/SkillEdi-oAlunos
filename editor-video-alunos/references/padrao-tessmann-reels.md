# Padrão Tessmann — Reels

Padrão de Reels do Tiago Tessmann, medido em Reels reais editados por ele no Premiere. Tudo que está aqui foi medido em pixels e em segundos: reproduza os valores, não "algo parecido".

Formato: **1080x1920, 30 fps**. Um formato só.

---

## 1. Estrutura do vídeo

| Trecho | Layout |
|---|---|
| Do **primeiro quadro** até ~**60 %** do vídeo | **Tela dividida**: em cima material real, embaixo o apresentador. Sem título de abertura. |
| Virada | **Transição de filme (film burn)**, 1,12 s, em **modo tela (screen)**, com o som do overlay em **volume baixo (0,45)**. O corte para tela cheia acontece no **pico branco, +0,40 s** depois do início da transição. Usada **uma vez só** no vídeo inteiro. |
| ~60 % até o fim | **Apresentador em tela cheia** — é a parte do argumento final e da chamada. |

Referência dos ~60 %: os Reels medidos duram de 1:33 a 1:51 e a virada caiu em 56 s, 62 s e 67 s — ou seja, entre ~60 % e ~70 % da duração. Escolha o ponto pela fala (onde começa o argumento final), não pelo cronômetro.

O overlay da transição é um arquivo de vídeo (`.mov`) mais o som dele (`.wav`) que **você tem que ter**: não vem com a skill. Como apontar o seu no config (`burn=`) está em `pipeline-tecnico.md`. Sem overlay nenhum, `burn=None` corta seco na virada — o resto do padrão continua igual.

**Divisória em y = 899.** Área de cima: 0–899. Área de baixo (apresentador): 899–1920. **Sem linha na divisória.**

---

## 2. Legenda

| Item | Valor |
|---|---|
| Fonte | TikTok Sans |
| Peso | wght **500** (Medium) |
| Tamanho | **59 px** (em 1080x1920) |
| Tracking | **−30/1000 em** (negativo, letras mais juntas) |
| Cor | Branca, **sombra suave**, sem caixa e sem contorno |
| Alinhamento | Centralizada em x = 540 |
| Baseline na **dividida** | **y = 912** (o texto ocupa y 871–924, centro ≈ 897 — ou seja, centrado exatamente sobre a divisória) |
| Baseline na **tela cheia** | **y = 1130** (texto em y 1087–1142, ≈ 58 % da altura, logo abaixo do queixo) |

Conferência de tamanho: "toda empresa" mede 340 px de largura e 54 px do ascendente ao descendente.

**Blocos muito curtos: 1–3 palavras.** Troca a legenda inteira de uma vez — sem palavra por palavra, sem fade, sem destaque de cor. Nos Reels medidos: 114, 121 e 73 trocas, com **mediana de 0,67 s por bloco**.

### Quebra por unidade de sentido

Cada bloco fecha uma ideia curta. Nunca separar artigo, preposição ou adjetivo da palavra que acompanham. Nunca começar frase nova no meio de um bloco — ponto final e vírgula fecham o bloco.

BOM: `A cidade` / `despertava lentamente` / `enquanto a chuva fina` / `cobria as ruas.` / `No café da esquina,` / `pessoas conversavam` / `sobre planos,` / `viagens e problemas` / `que pareciam enormes` / `naquela manhã.` / `Um cachorro` / `observava tudo` / `pela janela,` / `esperando seu dono` / `terminar o café.`

RUIM: `A cidade despertava` / `lentamente enquanto a` / `chuva fina cobria as` / `ruas. No café da` / `esquina, pessoas` / `conversavam sobre` / `planos, viagens e` / `problemas que` / `pareciam enormes naquela` / `manhã. Um cachorro`

### Primeiros 10 s sem legenda

**Nenhuma legenda antes dos 10,0 s.** Essa abertura fica livre para o título ser colocado à mão por cima, depois, no editor de vídeo do aluno (ou na própria ferramenta de publicação). O render não desenha título nenhum. Regra fixa, vale para todo vídeo.

---

## 3. Apresentador

- Selfie de celular, **enquadramento fechado** (rosto grande).
- Na dividida ocupa a faixa 899–1920, preenchendo a área inteira (cover) — sem barra, sem borda, sem fundo desfocado nas laterais.
- **Jump cuts** entre takes. **Sem zoom punch.**
- O recorte segue o rosto detectado, mas a câmera **não pode bugar**: descartar detecção falsa, interpolar entre quadros e limitar a velocidade do movimento a **260 px/s**.

---

## 4. Área de cima — ritmo

- **Trocar o material a cada 2–3 s.** Um clipe só pode ficar mais tempo se ele tiver movimento próprio (gravação de tela, por exemplo).
- Medido nos Reels: 33 cortes em 57 s (~1,7 s, em rajadas), 23 cortes em 62 s (~2,7 s) e 7 cortes em 67 s (gravações de tela longas).
- O material **preenche a área inteira (cover)**, sem moldura e sem crédito desenhado na tela.

---

## 5. Área de cima — regras duras

1. **Só material real**: vídeo do TikTok, do YouTube, do Instagram, print de notícia, logo oficial, gravação de tela real, foto da pessoa citada.
2. **Nada de banco de imagem** nem b-roll de peça publicitária (estúdio, modelos, cena genérica). "Live no TikTok" = vídeo real de alguém fazendo live no TikTok; "app" = gravação de tela real do app.
3. **Nada de card branco com número ou frase.** A área de cima é só material real passando.
4. **Cada clipe ou imagem aparece uma vez só** no vídeo inteiro. Antes de entregar, olhar a folha de contato procurando repetição.
5. **Famosos e influenciadores grandes do nicho** no começo e no meio, pegos do TikTok (perfil ou busca) e do YouTube (coberturas). Chamativo, até meio polêmico.
6. **Empresa ou plataforma citada = rosto do dono / CEO** (foto ou vídeo de entrevista, keynote, coletiva). Tela de sistema só quando a fala é literalmente sobre a tela.
7. **Fallback**: quando não souber o que colocar, o apresentador no palco (material dele palestrando) é o coringa.
8. **O que está em cima bate com o que está sendo dito naquele instante.** Método: ler a transcrição inteira, listar cada coisa concreta citada (matéria, evento, empresa, ferramenta, número, história) e buscar **aquilo mesmo** — a matéria citada com print legível do trecho certo, o vídeo do evento citado, a tela real da ferramenta citada. Nunca material genérico "do tema". Trocar assim que a fala muda de assunto.
9. **Print de notícia**: o texto tem que caber inteiro, sem cortar nas bordas.
10. **Sem música de fundo.**

---

## 6. Enquadramento — conferir quadro a quadro

Antes de renderizar, extrair o **quadro real** de cada slot no segundo em que ele vai ser usado (não a folha de contato geral), com grade de pixels, e definir o recorte cortando fora âncora, tarja, legenda de fonte, relógio e logo do canal.

- Conferir a **janela inteira** do clipe a **2 fps**: o trecho não pode passar por transição de estúdio no meio.
- **Descartar** trechos com texto queimado do clipe original, split-screen ou cartela.
- Fonte em 1280x720 precisa de recorte menor para não sobrar barra preta.

**Recortes medidos:**

| Caso | Recorte | Observação |
|---|---|---|
| Clipe vertical | **576 x 479** | rosto a 42 % da altura |
| Clipe 16:9 / pessoa em cena | **1300 x 1080** | mesma proporção da área de cima (1080x899), foco 0,0 (topo do recorte = topo do quadro), para a cabeça ficar inteira no terço de cima |

**Centrar pelo rosto detectado, não a olho.** Rodar detecção de rosto no quadro extraído e posicionar o recorte pelo centro do rosto (para o recorte de 1300 px: `esquerda = centro_x − 650`, preso ao intervalo [0, 620]). Recorte centrado no quadro corta a cabeça das pessoas; recorte chutado cola a pessoa na borda. Conferir no quadro real que cabeça e mãos cabem.

---

## 7. Abertura

- **Primeiro quadro forte**: b-roll de vídeo da empresa, cena de notícia, algo bom. **Nunca só o logo.**
- **Os primeiros 10 s não podem ter fundo branco ou claro**, porque o título entra por cima.
- Sem título de abertura desenhado no render. A legenda começa depois dos 10 s.

---

## 8. Cor

Grade fixa aplicada no vídeo do apresentador (base):

| Ajuste | Valor |
|---|---|
| Contraste | **1,32** |
| Saturação | **1,28** |
| Gamma | **0,97** |
| Extra | leve tom quente, nitidez |

Realce aplicado **no material de cima** (vídeo e foto):

| Ajuste | Valor |
|---|---|
| Saturação | **1,18** |
| Contraste | **1,10** |

**Print de notícia e logo ficam sem realce.**

Motivo da grade: sem ela o render sai 30–60 % abaixo dos Reels de referência em saturação e contraste, e o vídeo fica "meio sem cor".

---

## 9. Entrega

- **Um formato só: RL 1080x1920** (vertical). Reels não sai em IN/GL/YT — isso é só para criativo.
- Renderizado com `scripts/reels2.py`; o passo a passo (preparo, config, render) está em `pipeline-tecnico.md`.
- Arquivo salvo numa **pasta com o nome do vídeo**, na sua própria máquina.
- Versionar: cada revisão vira um arquivo novo (`nome-v2.mp4`, `nome-v3.mp4`). Nunca sobrescrever a versão anterior.
- Nunca modificar o bruto original.

---

## Checklist antes de entregar

**Estrutura**
- [ ] Dividida começa no primeiro quadro, sem título desenhado.
- [ ] Virada para tela cheia entre ~60 % e ~70 % da duração, no ponto em que começa o argumento final.
- [ ] Transição de filme usada **uma vez só**, 1,12 s, em modo tela, corte no pico a +0,40 s, som em volume 0,45.
- [ ] Divisória em y = 899, sem linha.

**Legenda**
- [ ] TikTok Sans wght 500, 59 px, tracking −30, branca com sombra suave, sem caixa.
- [ ] Baseline 912 na dividida, 1130 na tela cheia, centralizada.
- [ ] Nenhuma legenda antes dos 10,0 s.
- [ ] Blocos de 1–3 palavras, mediana perto de 0,67 s.
- [ ] Nenhum bloco separa artigo/preposição/adjetivo do nome; nenhum bloco começa frase nova no meio.

**Área de cima**
- [ ] Troca a cada 2–3 s (ou clipe longo com movimento próprio).
- [ ] Zero banco de imagem, zero b-roll publicitário, zero card de número/frase.
- [ ] Nenhum clipe ou imagem repetido.
- [ ] Pelo menos um famoso/influenciador do nicho no começo e no meio.
- [ ] Toda empresa citada aparece pelo rosto do dono/CEO.
- [ ] Folha de contato conferida linha por linha: o que ele diz bate com o que está em cima naquele instante.
- [ ] Prints de notícia com o texto inteiro visível, sem corte nas bordas.

**Enquadramento**
- [ ] Quadro real de cada slot extraído e conferido no segundo usado.
- [ ] Janela inteira de cada clipe conferida a 2 fps, sem transição de estúdio no meio.
- [ ] Nenhum clipe com texto queimado, split-screen ou cartela.
- [ ] Recortes 576x479 (vertical) / 1300x1080 (16:9) centrados pelo rosto detectado; cabeça e mãos cabendo.
- [ ] Nenhuma barra preta em nenhum slot.

**Abertura e cor**
- [ ] Primeiro quadro forte, não é logo.
- [ ] Primeiros 10 s sem fundo branco/claro.
- [ ] Grade no base: contraste 1,32, saturação 1,28, gamma 0,97.
- [ ] Realce 1,18 / 1,10 no material de cima; prints e logos sem realce.

**Apresentador e áudio**
- [ ] Rosto acompanhado sem bugar (velocidade limitada a 260 px/s).
- [ ] Área de baixo preenchida inteira, sem barra nem fundo desfocado.
- [ ] Sem música de fundo.

**Arquivo**
- [ ] RL 1080x1920, 30 fps.
- [ ] Salvo em pasta com o nome do vídeo, com versão no nome.
