# Padrão Tessmann — YouTube (16:9) — ANTERIOR (até 02/11/2026, substituído pelo `padrao-tessmann-youtube.md` novo, estilo LABS). Usar só se o aluno pedir este visual antigo.

Padrão dos vídeos longos de YouTube do Tiago Tessmann: **apresentador em tela cheia com texto grande por cima
do vídeo**, ilustrações animadas ao lado dele, alguns painéis pretos e inserts de site/matéria real.

Formato: **1920x1080, 30 fps**. Um formato só.

Não confunda com Reels e criativo: aqui **não tem tela dividida em cima/embaixo**, não tem legenda queimada o
vídeo inteiro e a fonte é outra. Se a edição for YouTube, o que vale é este arquivo.

> **O que a skill entrega neste padrão.** O corte, a transcrição revisada e a montagem em **Remotion** (vídeo
> 1920x1080) com as animações e telas cheias feitas em **HyperFrames** (WebM com transparência, encaixado por cima).
> Se o aluno preferir editar no Premiere, DaVinci ou CapCut, a skill entrega o **roteiro de edição completo** —
> bloco por bloco, com o tempo, o tipo de elemento, o texto exato, o tamanho em px e o material a buscar — mais as
> animações renderizadas soltas. Tudo aqui está em px de 1080p.

---

## 0. Atualização (outubro/2026) — vale por cima do resto deste arquivo

O padrão base (seções 1 a 7) continua: apresentador em tela cheia, texto grande por cima, painéis, inserts reais.
Por cima dele **somam** estas camadas, corrigidas vídeo a vídeo. Onde houver conflito, vale esta seção.

### 0.1 Camada 3D (soma ao básico, não substitui)
- **Recortar o apresentador** (`work/recortar_pessoa.py`) para textos e gráficos passarem **atrás dele** — é o que
  faz o elemento parecer estar na cena. Texto lateral atrás dele **por padrão**, alternando com blocos limpos.
- Título com **degradê no próprio texto** (branco → #B9B9B9) revelado por máscara de baixo para cima; **sublinhado
  fino** (~3,4 % da altura do corpo) que se desenha na palavra-chave.
- **Sem chapéu/kicker** (a linha pequena em caixa alta em cima do título) — nem nos painéis. Na cartela de virada, o
  número entra GRANDE ("01") no lugar da linha.
- Painéis e cartões com **profundidade real** (perspectiva 3D), entrando do fundo e recuando quando o próximo entra.

### 0.2 Edição dinâmica
- Varrer a transcrição e marcar **tudo que ele cita de concreto** (notícia, lei, empresa, ferramenta, número,
  pessoa, site, app): cada um vira **insert real** com fonte, ou tela cheia da coisa.
- Primeiro minuto: **uma troca a cada 3–5 s**, abertura com título curto e grande + animação puxando a fala nos
  primeiros 3–4 s. Depois: **nunca mais de ~15–20 s** só ele + texto.
- Variar o tipo (notícia em tela cheia, insert ao lado, cartela, animação, cartão) — não repetir o mesmo seguido.

### 0.3 Telas cheias — 5 modelos
Toda tela cheia usa um destes, variando ao longo do vídeo, na linguagem de `padrao-tessmann-motion.md`:
1. **Editorial** — título à esquerda + cards escuros (rótulo, palavra grande, descrição), barra desenhando.
2. **Dividida** — linha central se desenhando; lado ruim riscado/apagado, lado bom aceso.
3. **Vidro 3D** — painéis em perspectiva flutuando, ✗/✓.
4. **Tipografia grande** — palavra apagada × palavra cheia, giro 3D.
5. **Interface** (preferido quando explica recurso) — janela de app real, cursor clicando, notificações, busca.

Fundo: quase preto + degradê verde sutil num canto + grão. Entra e sai em **corte seco**; **nunca abre vazia** (1º
elemento grande em ≤ 0,6 s); último elemento ≥ 1,5 s inteiro na tela; respiro ≥ ~140 px em cima e embaixo; **uma
ideia por tela**. A legenda pílula + frase embaixo **não é obrigatória** — só quando a tela precisa explicar.
**Nenhuma tela seca**: cartela/tela cheia sempre com texto animado (palavras entrando, sublinhado, movimento).

### 0.4 Ao lado dele (laterais)
- Não é só título: **lateral animada** na pegada do motion — cartão de interface que **cresce** com os itens (nunca
  cartão grande vazio esperando a fala), contador, avatares, check, chip riscado. Faixa ≤ ~480–600 px, texto ≥ 40 px.
- Texto lateral **grande e largo** (lista ~74 px, mín. 56), **nunca uma palavra por linha** — se bater no
  apresentador, passa atrás dele, não encolhe a coluna.
- **Lateral parada no máximo ~8–10 s**; fala longa vira várias laterais curtas, uma por ideia.
- Espaço folgado sempre (≥ 24–40 px entre blocos; título → conteúdo ≥ ~80 px). Nada colado.
- Animações seguidas do mesmo lado: **o zoom fica**, só troca a animação (sem sair e voltar).
- Frase longa (> ~26 letras) em **duas linhas equilibradas**, quebrando no sentido.

### 0.5 Textos
- Maiúscula no início e depois de ? e !. Imperativo certo ("Escreva", "Comente", "Deixe" — nunca "Escreve",
  "Comenta"). Sem a informalidade da fala ("galera", "tipo"). Sigla com o nome completo.
- Passo a passo: **todo "Passo N" abre em tela cheia** com o mesmo cabeçalho "Passo N · Título" no topo.
- Lettering que não acrescenta nada sai. Título depois de tela cheia começa no fim dela; texto sai quando a fala acaba.

### 0.6 Som
- **Trilha só na abertura**: uma trilha dramática (cara de trailer) que **bate forte já no 0 s**, vai baixando
  devagar (~8 s) e some no fim da abertura; o resto do vídeo **sem música**. Trilha diferente em cada vídeo.
- **Efeitos sonoros em toda animação** (pop, whoosh de interface, clique do cursor, tick no check, snap no risco).
- Botão "Inscreva-se" animado (foto do canal limpa, sem aro; clique + sino) — **nunca por cima de texto**.

### 0.7 Corte e áudio
- Começa direto na primeira fala. Antes de retomar uma tomada ele costuma bater palma: o trecho começa **depois**
  do estalo.
- Cortar gaguejo e autocorreção — mas se o corte de um tropeço fica feio, **manter a fala original**.
- Corte que termina em "s"/"ch" (fricativa): conferir os agudos, não só a energia — senão "chia".
- Pulo de posição no meio da frase: cobrir com tela cheia até depois do corte.
- Cortes na grade de 30 quadros por segundo.

### 0.8 Antes de exportar
Mandar ao aluno a **folha de quadros das telas cheias** (3 momentos por tela) e esperar o OK; depois render,
conferir quadros de cada tela nova e de cada corte, e a fala contra a tela.

---

## 1. O vídeo, do começo ao fim

1. **Corte.** Erro e retake fora — fica o último take. Respiros apertados, **sem cortar dentro da palavra**: só
   vão maiores que 0,5 s, com proteção nas bordas. Quantizar os cortes a 30 fps. Deixar **+1,2 s de respiro depois
   da última palavra** e fechar com **fade para preto de 0,8 s**. Contraste **1,08** na câmera (o bruto sai chapado).
2. **Apresentador em tela cheia quase o tempo todo.** A abertura é densa: **uma intervenção a cada 4–8 s no primeiro
   minuto**, nunca mais de ~10 s só de pessoa falando. Depois disso, elemento só nos momentos que merecem.
3. **Texto por cima do vídeo** — é a marca do padrão. SF Pro, branco, sombra leve. Entrada com **blur de 14 px → 0
   em 0,38 s** mais uma leve subida; saída em 0,26 s. Som de **clique de mouse** a cada entrada, em volume baixo.
4. **Painel preto** — o momento mais elaborado, **~5 por vídeo de 17 min**. Apresentador num retângulo de altura
   inteira à direita (x de 1290 a 1920); à esquerda fundo `#0A0A0A` com chapéu em caixa alta espaçada (26 px),
   título em caixa alta (72 px, ou 60 se passar de 28 caracteres), itens com fio (46 px) e/ou número grande
   (150 px, contando de 0). **Sem ícone, sem emoji. Painel nunca branco nem cinza.**
5. **Insert** — só de coisa real (site, matéria, produto, painel de anúncios). Base **preta**, print à esquerda
   (x 60, y 85, 1225×890, raio 24, com zoom lento) e apresentador numa **janela vertical arredondada à direita**
   (x 1345, y 85, 525×890, raio 24). Os dois retângulos têm **a mesma altura e o mesmo alinhamento** — desnivelar
   é erro conhecido. Fonte do print em cinza 26 px embaixo à esquerda. Whoosh na entrada e na saída.
   Print na proporção 1280×930. **A janelinha pequena no canto não é deste padrão.**
6. **Ritmo e remate.** Flash branco de 0,45 s na troca de bloco; punch-in de 1,08–1,12 de vez em quando; selo de
   "Inscreva-se" quando ele pede inscrição no meio (~10 min) e no fim.

---

## 2. Tamanhos de texto — a regra que mais foi corrigida

Tudo SF Pro, branco. **Nada abaixo de 40 px em cima do vídeo** (a única exceção é a legenda de fonte do insert,
26 px). Texto ao lado do apresentador: **no máximo ~26 caracteres por linha** — quebrar a linha na mão.

| elemento | px |
|---|---|
| frase de impacto (centro, com scrim escuro embaixo) | **78–108**, Bold |
| frase âncora embaixo | **57–73**, Bold, com sublinhado branco animado na palavra-chave |
| palavra ao lado dele | **68–84**, Semibold |
| lista "->" / fluxo | **50–58**, Semibold, quebra automática (largura 840 à esquerda) |
| ponto (tópico) | **49–54** no título, itens a 0,82× |
| painel preto | título **72** (60 se > 28 caracteres), itens **46**, números **150**, chapéu **26** |
| chat | 40 · anúncio 42 · relógio 160 · ciclo 34/50 · linha 46/32 · anel 40 · rede 52 |

Referências usadas para calibrar o tamanho (medidas em 1080p): frases Bold de ~85–100 px centralizadas embaixo,
blocos laterais de ~75 px em 2–3 linhas com sublinhado na palavra-chave; e títulos de ~56 px com sub-itens de
~45 px em dois blocos lado a lado. **Texto pequeno é o erro clássico deste padrão** — na dúvida, aumente.

---

## 3. Tipos de elemento

- **Frase de impacto** — scrim escuro embaixo, Bold, centralizada, ancorada a **96 px da base**. Serve para
  capítulo ("01 | O criativo que filtra") e para as frases fortes. Nas mais pesadas, entra junto um tratamento de
  drama (dessatura a imagem e fecha uma vinheta).
- **Frase âncora** — embaixo, Bold, com **sublinhado branco que se desenha** sob a palavra-chave.
- **Palavra ao lado**, **lista "->"**, **ponto com sub-itens**, **número grande contando de 0**, **balões de chat**
  de vidro (uma linha cada, **≥ 120 px entre eles** — balão sobreposto é erro conhecido).
- Quando o texto vai para a lateral, **o apresentador vai para o outro lado**: punch-in de 1,18 e deslocamento de
  no máximo 170 px. **Nunca pode abrir faixa preta** na borda.

### Ilustrações animadas

Ficam **direto sobre o vídeo, à esquerda** (x 60–110), todas **brancas**, SF Pro, **sem ícone e sem emoji**, com o
apresentador empurrado para a direita.

| tipo | o que é | quando usar |
|---|---|---|
| `fluxo` | passos com bolinha e linha vertical que se desenha entre eles | sequência de etapas |
| `chat` | cartão de vidro estilo WhatsApp (largura 720), mensagens alternadas, "digitando…" antes de cada uma, etiqueta no cabeçalho | conversa, qualificação — as respostas são ilustrativas, **nunca print de conversa real** |
| `rede` | rede em linhas, bolinhas caindo e se separando em dois grupos com rótulo | separar A de B |
| `relogio` | relógio girando rápido, número contando e marcas com ✓ | tempo de resposta, prazo |
| `anuncio` | mock de anúncio (avatar, marca, "Patrocinado", linhas entrando, botão com clique) | exemplo de criativo/anúncio |
| `ciclo` | dois nós em pílula com setas curvas que se desenham, resultado embaixo | loop, uma coisa alimentando a outra |
| `linha` | linha do tempo horizontal com pontos e rótulos (Dia 1 · Dia 3 · Semana 1) | sequência, follow-up |
| `anel` | anel de porcentagem com contagem | percentual |

Escala usada para não ficarem miúdas em 1080p: rede ×1,32, ciclo ×1,25, linha ×1,2, anel ×1,3, relógio ×1,12.
Números grandes **contam de 0 até o valor**, com dígitos de largura fixa (tabular).

**Som**: clique de mouse na entrada de cada item; pop nas mensagens do chat; click no botão e na etiqueta.

---

## 4. Erros já cometidos neste padrão — não repetir

- Frase grande no meio do rosto → frase de impacto é **sempre embaixo**.
- Whoosh e pop na entrada de texto → o som de texto é **clique de mouse**; whoosh é do insert.
- Deslocar o apresentador demais e abrir **faixa preta** → punch-in 1,18, deslocamento ≤ 170 px.
- Insert com janelinha pequena e base cinza → **base preta** + janela vertical, com as alturas iguais.
- Painel branco → **painel é sempre preto**.
- Título transbordando o painel → quebrar a linha e cair para 60 px.
- Balões de chat sobrepostos → uma linha cada, ≥ 120 px de distância.
- Final seco → +1,2 s de respiro e fade.
- **Texto pequeno demais** → a tabela da seção 2 é o piso, não o teto.
- Cara de apresentação de slides ("PowerPoint", "cara de IA") → o vídeo é o protagonista; o texto e a animação vão
  **em cima dele**, não numa tela separada.

---

## 5. Material real

Insert só de coisa que existe: a matéria citada, o site citado, o painel citado. Capturar o print na proporção
1280×930 e registrar veículo, autor, data e URL em `referencias/<vídeo>/fontes.md`. Print de conversa de cliente
não entra — conversa vira o `chat` ilustrado.

---

## 6. Entrega

Uma pasta com o nome do vídeo:

- `<título>.mp4` — 1920x1080.
- Opcional, uma versão leve em 720p para mandar por WhatsApp/Telegram.
- `fontes.md` com o material usado.
- Se for tirar frame para thumbnail, exportar PNG em 1080p do bruto **com o mesmo contraste 1,08**.

Versionar: `<título>-v2.mp4`, `-v3.mp4`. Nunca por cima da versão anterior.

---

## 7. Checklist antes de entregar

- [ ] Nenhum texto abaixo de 40 px em cima do vídeo (fora a legenda de fonte, 26 px).
- [ ] Primeiro minuto com intervenção a cada 4–8 s, sem buraco de mais de ~10 s só falando.
- [ ] Nenhuma faixa preta ao deslocar o apresentador.
- [ ] Painéis pretos (não brancos, não cinzas), ~5 no vídeo longo, sem ícone nem emoji.
- [ ] Insert: base preta, print e janela do apresentador com a mesma altura e alinhados.
- [ ] Todo insert é de material real e está registrado no `fontes.md`.
- [ ] Balões de chat sem sobreposição.
- [ ] Contraste 1,08 aplicado na câmera.
- [ ] Fim com +1,2 s de respiro e fade de 0,8 s.
- [ ] Assistir do começo ao fim: cada elemento entra na hora da frase que ele ilustra.
- [ ] Seção 0: recorte com texto atrás, nenhuma tela seca, nenhuma lateral parada > ~10 s, nenhum kicker.
- [ ] Trilha só na abertura (forte no 0 s) e efeitos sonoros nas animações.
- [ ] Inscreva-se fora de cima de texto; Passo N em tela cheia com o mesmo cabeçalho.
