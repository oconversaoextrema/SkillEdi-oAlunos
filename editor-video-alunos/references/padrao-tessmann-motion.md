# Padrão Tessmann — Motion (estilo "prévia premium")

Vídeo **animado** que apresenta um produto, app ou serviço — sem a pessoa na câmera, com narração. É o estilo
das prévias das soluções do Tiago: interface de verdade se mexendo em 3D, câmera dentro da janela, cursor
clicando, tudo no tempo da voz. Também é a **linguagem das animações** que entram no YouTube (seção 6).

Feito em **HyperFrames** (`work/modelos/hyperframes-modelo`). Formato: o que o aluno pedir —
1440x1440 (padrão das prévias), 1080x1920 ou 1920x1080. 30 fps.

---

## 1. Estrutura (sempre a mesma, troca só o conteúdo)

1. **Assinatura do logo** (0–2,4 s, sem voz): o contorno do logo se desenha girando → preenche na batida com
   clarão e anéis → vira o ícone com brilho.
2. **A dor**: a cena do problema — notificações de WhatsApp sem resposta empilhando, contador subindo, planilha
   bagunçada, post-it escrito à mão com itens riscados. Tudo desbota e cai um **carimbo vermelho torto** com o nome
   do problema.
3. **Título** palavra por palavra (Bold, grande) com **sublinhado que se desenha** na palavra-chave + **3 cards**
   entrando nas palavras que eles nomeiam.
4. **A janela 3D do produto entra no "drop" da trilha**: janela clara com sidebar, em perspectiva, balançando
   devagar (rotationY 1,5° / rotationX 1,1°, sine, vai e volta).
5. **Cenas na fala**: câmera com **zoom dentro da janela**, cursor clicando no menu (o destaque desliza), formulário
   que se preenche sozinho, toasts, contadores subindo, gráfico se desenhando. Cada cena entra na frase que ela
   ilustra.
6. **CTA** com clique no botão.

Legenda das cenas (quando a tela precisa explicar): **pílula pequena** com um ponto (o tema) + **frase curta Bold**
com 2–3 palavras destacadas na cor da marca, entrando palavra por palavra. Não é obrigatória em toda cena.

---

## 2. A pegada

- **Mini-história** (problema → solução), não lista de recursos.
- **Objetos reais de interface** (janela de app, formulário, fotos entrando, site com filtro, página do produto) —
  nunca caixas abstratas ou ícones soltos.
- Entrada: sobe + desfoca → nítido. Saída: sobe + desfoca. Troca de tela: fusão com blur.
- **Respiro grande, uma ideia por quadro.** Nada encostado na borda (≥ ~140 px em cima e embaixo; conteúdo ~10 %
  menor a partir do centro). Título → conteúdo ≥ ~80 px.
- Fundo escuro: quase preto (#070908 → #0A0D0B) + um degradê sutil da cor da marca num canto + grão. Sem grade, sem
  brilho animado (fica "bugado").
- Cores: caixa escura/colorida = letra branca; vermelho vivo (#FF3B3B), verde (#14A05A), azul (#1F6FE5); nada de
  caixa branca com texto preto em fundo escuro (vira vidro escuro com texto branco).
- Janelas e cartões com **borda clara de 2 px** (borda de 1 px some na compressão), corpo #161B18, respiro no pé.
- Zoom lento liso: a câmera numa camada composta (`will-change:transform` + `force3D`), senão o texto anda aos
  saltos de meio pixel.
- Tipografia vazada: **nunca** `-webkit-text-stroke` (desenha os traços internos da fonte variável). "Vazada" =
  letra cheia cinza apagada.
- Centralizar elemento que o GSAP anima com `left:0; right:0; margin:0 auto; width:max-content` — **não** com
  `left:50%` + `translateX(-50%)` (desloca quando a fonte carrega).

---

## 3. Som

- **Narração**: voz por IA (ElevenLabs ou outra) ou do próprio aluno. Transcrever com o Whisper e **amarrar cada
  animação ao tempo da palavra**. Trocar a voz depois = mapear tempo antigo → tempo novo palavra a palavra, não
  reescrever a animação.
- **Trilha** cortada para o drop cair na entrada da janela 3D; **ducking** pela voz; master ~−15 LUFS.
- **Efeitos sonoros tirados da própria animação**: janela/cartão = whoosh de interface, título = whoosh de entrada,
  item = pop, notificação = popup, cursor = clique, check = tick (o último = sucesso), risco = snap, saída = whoosh
  de saída. Sem som a animação fica "seca".

---

## 4. Fluxo de trabalho

1. Levantar as telas do produto (site/app do aluno, prints).
2. Escrever o roteiro no tamanho das cenas (dor → título → janela → 3–5 cenas → CTA) e mandar para o aluno aprovar.
3. Montar com tempos estimados enquanto a narração não chega; quando chegar, transcrever e mapear os tempos reais.
4. Mandar 3–5 quadros das cenas principais antes do render final.
5. Render, mixar voz + trilha + efeitos, conferir quadros e entregar.

---

## 5. Erros já cometidos — não repetir

- Cópia fiel de referência sem vida → "precisa ser mais animado, algo premium, logo de início top".
- Cards colados uns nos outros → espaço folgado sempre.
- Tela cheia de coisa (frase + chips + anotações juntos) → uma ideia por vez.
- Pílula do título torta → centralização com margin auto (seção 2).
- Fundo com brilho animado ou grade → reprovado como "bugado".

---

## 6. Dentro do YouTube

No YouTube, a **linguagem** deste padrão (não o conteúdo) é o estilo das telas cheias e das animações ao lado da
pessoa: quando ela explica um recurso, um fluxo, um número ou uma comparação, em vez de print parado ou cartão de
texto, entra motion assim — adaptado a 1920x1080, sincronizado à fala dela, sem voz nem trilha próprias (só os
efeitos sonoros). Detalhes em `padrao-tessmann-youtube.md`, seção 0.
