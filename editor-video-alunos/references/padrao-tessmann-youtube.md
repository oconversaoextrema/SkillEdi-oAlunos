# Padrão Tessmann — YouTube (16:9) — estilo LABS (desde 02/11/2026)

Padrão dos vídeos longos de YouTube do Tiago Tessmann a partir de novembro/2026. Inspirado na edição do canal LABS
("Como BOMBAR um canal com Claude em 7 dias", https://youtu.be/cCTRLHp5tJM): **a pessoa em tela cheia limpa, em
blocos curtos, intercalada o tempo todo com motion de 1–4 s** em coral sobre fundos escuros e creme, com **serifa nos
números e títulos**, **retícula de pontinhos por cima de todo o motion**, transições de clarão e chicote, **sem
legenda**, trilha baixa contínua e muito efeito sonoro.

Formato: **1920x1080, 30 fps** (4K só se o aluno pedir). Um formato só. Não tem tela dividida, não tem legenda,
não tem texto em cima da pessoa. (O padrão anterior, com texto grande sobre o vídeo, está em
`padrao-tessmann-youtube-anterior.md` — só usar se o aluno pedir aquele visual.)

> **O que a skill entrega neste padrão.** O corte, a transcrição revisada, o motion em **HyperFrames**
> (`work/modelos/hyperframes-labs/index.html` como ponto de partida) e a montagem final com `work/labs_compor.py`
> (troca pessoa/motion, transições, acabamento e áudio). Se o aluno edita no Premiere/DaVinci/CapCut, entregar o
> **roteiro de cenas** (tempo, peça de motion, texto exato, material) + o motion renderizado solto.

---

## 0. Atualização (02/11/2026) — vale por cima das seções abaixo
1. **Cores das animações na paleta do cenário do vídeo** (não um coral fixo): tire 5 tons do fundo/luz da gravação. No estúdio do Tiago:
   `#1A120B · #3D2314 · #8C4F2B · #D97724 · #F2A65A` — fundos marrons, destaque âmbar. Prints reais seguem em cartão branco.
2. **Pouca tela cheia — a maior parte em TELA DIVIDIDA**: motion no painel da esquerda (61 % da largura = 1170 px) e a pessoa à direita
   (750 px, recorte centrado no rosto, corte seco). Tela cheia só às vezes: capítulos "Passo N", matéria real de impacto, gráfico-chave,
   frase de virada. Na dividida, o conteúdo da cena é ampliado até encher o painel (margem 70 px) — nada miúdo.

## 1. Ritmo e estrutura
- **Corte a cada ~1,7 s em média.** A pessoa fica ~1/3 do tempo, em blocos de ~5 s; o resto é motion e telas,
  cada cena de 1–4 s, encadeadas.
- Entre trechos da pessoa: **jump cut com punch-in/out de 10–15 %** (alternar 1,0 ↔ 1,1 a cada corte).
- **Gancho de ~10 s** com números contando e peças entrando em sequência.
- **Capítulos "Passo N"** (cartão "Passo **N**" + o nome do passo embaixo) em cada parte ou ação do roteiro.
- Final: cena de "Inscreva-se · like · sino · link" em motion, depois volta pra pessoa até o fim.
- **Sem legenda.** Todo texto da tela é rótulo curto do motion (1–3 palavras, no máximo uma frase curta).
  A pessoa aparece sempre em tela cheia **limpa** — sem recorte, sem janelinha, sem texto por cima.

## 2. Paleta
| uso | cor |
|---|---|
| destaque (coral) | `#D87259` · claro `#EE9471` · anel/progresso `#DC6658` |
| fundo marrom-vinho | centro `#1C1012` → cantos `#08070A`, brilho quente embaixo |
| fundo azul-ardósia | `#232634` → `#0B0B14` |
| fundo creme (gráficos, contadores, prints) | `#F4EAE4` com brilho rosado `#FFF8F3` |
| "Passo N" | quase preto `#121214` → `#060608`, poeira colorida parada |
| cards de vidro | marrom `rgba(86,62,58,.78)` / azul `rgba(66,76,96,.8)`, cantos 36–40 px, borda 1,5 px clara, sombra longa; ativo = contorno coral + brilho |
| ok / não | `#3FBF7F` / `#E5484D` |
Alternar os três fundos ao longo do vídeo.

## 3. Tipografia
- **Serifa regular** (Newsreader) em números e títulos: "Passo **2**", "2,4 *mi*", "73%". Número/unidade de destaque
  **em coral**, sufixo menor.
- **Kicker** em caixa-alta coral, espaçamento largo (~.34em), junto do título ("O QUE MUDOU").
- **Sans** (Inter SemiBold/Bold) nos rótulos de interface.

## 4. Acabamento — o segredo do look (obrigatório em todo motion, nunca na pessoa)
Sem isso o motion vira interface lisa genérica. Feito na montagem (`labs_compor.py`, função `acabamento`),
só nos quadros de motion. Valores calibrados (1080p; em 4K tudo ×2):
- **Retícula**: pontinhos redondos numa grade a **45°, passo 5 px**, **só nos tons médios** (branco segue branco,
  preto segue preto), intensidade .16.
- **Aberração cromática** de 1 px (franja vermelha/ciano), **glow** leve nos claros (.35), **grão quase zero** (.004),
  maciez .6 px, **vinheta** −18 %.
- Conferir num quadro em tamanho real (1:1) que a retícula aparece nos cards e no coral, sem sujar o fundo.
  Exagero é o erro mais comum: "tira um pouco, deixe igual à referência" foi a correção no primeiro teste.

## 5. Peças de motion (repertório — exemplos no modelo `hyperframes-labs`)
1. **Ícone 3D quadrado-arredondado** (ícone coral dentro de quadrado escuro com volume) — entra com pop; contorno coral quando ativo.
2. **Fluxo de nós** ligados por linha coral fina que se desenha; vencedor com contorno coral + chip "MELHOR OPÇÃO", perdedores cinza com ✗.
3. **Celulares/cards em fila** entrando um a um, às vezes com contador grande ao lado.
4. **Contador e anel de progresso** coral contando; barras de %.
5. **Cards rótulo + ícone** em linha, o ativo com contorno coral.
6. **Checklist em cascata**: cards entrando na hora da fala, ✓ coral no fim.
7. **Gráfico de barras** em card branco sobre creme, barra coral subindo + **círculo desenhado à mão** no número.
8. **Print real** em janela flutuante com zoom lento, sublinhado/círculo à mão e cursor clicando (com a fonte legível embaixo).
9. **Interface recriada** (busca, chat com IA, formulário, checkout) com cursor, digitação letra a letra e clique.
10. **Pixel-dissolve**: a peça vira quadradinhos que voam até o destino.
11. **Cards de valor** contando ("R$ 0,00 → 4,50").
12. **"Passo N"**: "Passo **N**" serifado à esquerda, kicker coral embaixo, dois ícones ligados à direita.
Cada peça é a **ideia literal da frase** e entra na palavra (≈0,2 s antes). Entradas rápidas com leve overshoot, saídas curtas,
zoom lento de câmera (1 → 1,045) em cada cena.

## 6. Transições (feitas na montagem)
- **Pessoa → motion** e toda entrada de capítulo: **clarão leitoso** (borrão forte + estouro para cinza-claro em ~3 quadros;
  o motion entra desfocado e ganha foco).
- **Motion → motion**: **chicote horizontal** com borrão de movimento.
- **Motion → pessoa**: desfoque rápido de ~4 quadros.
- Cada transição tem seu whoosh.

## 7. Áudio
- Voz tratada e limpa (ver `pipeline-tecnico.md`), cortes de respiro como sempre.
- **Trilha baixa contínua o vídeo inteiro** (~−16 dB abaixo da voz; o vídeo nunca fica em silêncio), com fade no começo e no fim.
  O aluno escolhe a trilha (precisa ter licença); se não tiver, perguntar.
- **Muitos efeitos curtos**: pop (ícone/card), clique (cursor), tique (contador), ding (check), whoosh (transição),
  da pasta `trilhas/efeitos/` do projeto. Volume baixo, por baixo da voz.

## 8. Regras de conteúdo que continuam
- Cada coisa concreta que a pessoa cita (notícia, empresa, produto, número) vira **material real** (print em alta,
  vídeo oficial) ou peça de motion daquela coisa — registrar em `referencias/<vídeo>/fontes.md`.
- **Nada em inglês na tela** se o vídeo é em português: print estrangeiro ganha rótulos traduzidos por cima ou é recriado.
- Interface recriada usa nomes fictícios; nunca apresentar mockup como print real.
- Tela legível no celular, **nada cortado nos cards**, texto a ≥ 70 px da borda.
- **Nada colado**: entre um chip/título e o conteúdo de baixo, ≥ 60 px livres; se não couber, diminua e desça o elemento de baixo.
- Mostrar uma **folha de quadros** das cenas ao aluno antes de exportar o vídeo inteiro.

## 9. Passo a passo
1. **Corte e transcrição** como em `pipeline-tecnico.md` (começar na primeira fala útil, tirar largadas e respiros) →
   vídeo da pessoa já cortado (`work/<vídeo>/base.mp4`) + palavras com tempo no vídeo cortado.
2. **Roteiro de cenas**: lista `[início, fim, capítulo?]` no tempo do vídeo cortado — pessoa ~1/3 em blocos de ~5 s,
   motion 1–4 s por ideia, "Passo N" nas partes, gancho de 10 s, inscreva-se no fim. Mostrar ao aluno.
3. **Motion**: copiar `work/modelos/hyperframes-labs/` para `work/<vídeo>/motion/`, escrever as cenas nos tempos do roteiro
   (helpers prontos no modelo: `mostra`, `pop`, `entra`, `linha`, `digita`, `conta`, `pixela`), render pelo atalho `hf`
   (`references/ferramentas.md`) → `motion.mp4` com a duração do vídeo inteiro.
4. **Folha de quadros** (`work/folha.py`) → OK do aluno.
5. **Montagem**: `work/labs_compor.py work/<vídeo>/labs.json` (configuração explicada no topo do script) →
   `saidas/<título>.mp4`. `--quadros t1,t2` tira quadros sem renderizar tudo.
6. **Conferir**: quadros a cada 0,5 s (nada em inglês, nada cortado, retícula visível no motion), áudio sem estouro.

## 10. Imagens
`labs/teste-folha.jpg` (folha do primeiro teste aprovado) e `labs/reticula-zoom.png` (acabamento em zoom 1:1).
