# MODELO — padrão medido do aluno

Este arquivo é um **molde em branco**. Ele serve pra transformar o vídeo de referência do aluno num padrão de edição reproduzível.

Como usar:

1. O aluno escolhe um (ou até três) vídeo(s) de referência — edição que ele quer copiar.
2. O Claude mede a referência quadro a quadro (fonte, tamanho em px, posições, tempos de corte, cores) e preenche cada campo abaixo.
3. Tudo entre `[colchetes]` é buraco pra preencher. **Nada pode ficar com valor chutado**: se não deu pra medir, escrever `não medido`.
4. Os valores entre parênteses marcados como *(ex. padrão Tessmann: ...)* são só exemplo de como um campo preenchido fica. **Não copiar** esses números pro padrão do aluno — eles são de outra referência.
5. Salvar o arquivo preenchido como `references/padrao-do-aluno.md` **no projeto do aluno** (não dentro da skill), guardando ao lado os quadros e recortes usados na medição. Ele passa a ser a fonte de verdade das edições seguintes e é atualizado a cada correção do aluno.

**Os comandos de medição não estão aqui**: o passo a passo (ffprobe, extração de quadros, detecção de divisória, cortes, legenda, cor, transições) está em `references/treinar-com-referencia.md`, seção por seção, na mesma ordem das seções abaixo. Cada número escrito aqui vem acompanhado de **como foi medido** (ex.: "mediana de 73 intervalos entre trocas de bloco").

---

## 1. Cabeçalho

| Campo | Valor |
|---|---|
| Nome do padrão | `[nome curto, ex.: "padrão do aluno X"]` |
| Data da medição | `[dd/mm/aaaa]` |
| Arquivo(s) de referência | `[nome do arquivo na pasta do aluno]` |
| Origem | `[gravou / editou / baixou de onde]` |
| Quem edita | `[aluno]` |
| Observação do aluno | `[o que ele disse querer copiar, nas palavras dele]` |

---

## 2. Ficha técnica da referência

*Como medir: `ffprobe` na referência (passo 1 de `treinar-com-referencia.md`). `r_frame_rate` vem em fração: 30000/1001 = 29,97. Se não houver stream de áudio, escrever "referência veio sem áudio" — sem áudio não dá pra checar sincronia de legenda.*

| Campo | Valor |
|---|---|
| Resolução | `[larg x alt]` |
| FPS | `[nn,nn]` |
| Duração | `[m:ss]` |
| Tem áudio? | `[sim / não]` |
| Cenário / luz | `[descrição curta]` |
| Roupa / mic / enquadramento geral | `[descrição curta]` |

---

## 3. Estrutura e tempos

*Como medir: passos 2, 3 e 4 de `treinar-com-referencia.md` — folha de contato a 1 fps, quadros a 5 fps no vídeo inteiro, detecção da divisória e do instante em que ela some, detecção de cortes. Nunca concluir a partir de 2 ou 3 instantes soltos: amostra pequena já inverteu a resposta.*

| Trecho (timecode) | Layout | O que aparece |
|---|---|---|
| `[0,00–x,xx s]` | `[dividida / tela cheia / cutaway]` | `[descrição]` |
| `[x,xx–y,yy s]` | `[...]` | `[...]` |
| `[y,yy–fim]` | `[...]` | `[...]` |

- Ponto da virada dividida → tela cheia: `[t = ... s, ou ... % do vídeo]`
- Tem título de abertura? `[sim / não]` — se sim, entra em `[...]` e sai em `[...]`
- Cortes no trecho de tela cheia (timecodes): `[lista]`
- Tipo de corte entre takes: `[jump cut / corte seco / outro]`
- Tem zoom punch / Ken Burns? `[sim / não]`

*(ex. padrão Tessmann Reels: dividida até ~60 % do vídeo, depois tela cheia até o fim, sem título de abertura — só exemplo.)*

---

## 4. Layout e divisória

*Como medir: passo 3 de `treinar-com-referencia.md` (pico de descontinuidade por linha, confirmado a olho num quadro a 30 fps). Se o pico não for estável, não existe divisória — o vídeo é tela cheia do início ao fim.*

| Campo | Valor |
|---|---|
| Quem fica em cima na dividida | `[apresentador / material]` |
| Quem fica embaixo | `[...]` |
| Linha da divisória (y em px) | `[...]` |
| Tem linha/moldura visível? | `[sim / não]` |
| Material preenche a área inteira (cover)? | `[sim / não]` |
| Tem crédito/atribuição na tela? | `[sim / não, e onde]` |

*(ex. padrão Tessmann Reels: divisória em y = 899 num quadro 1080x1920, sem linha — só exemplo.)*

---

## 5. Legenda

*Como medir: passo 5 de `treinar-com-referencia.md` — máscara de branco pra achar a caixa do texto em qualquer altura (a legenda pode mudar de y), altura ascendente-descendente em px, largura de uma palavra conhecida pra achar corpo + tracking juntos, e trocas de bloco em quadros a 30 fps num trecho de pelo menos 30 s. Duração do bloco é a **mediana** dos intervalos, não a média.*

| Campo | Valor |
|---|---|
| Fonte | `[nome — se duas candidatas empataram, escrever as duas e "fonte inferida, não confirmada" até o aluno confirmar]` |
| Arquivo da fonte no computador do aluno | `[caminho do .ttf/.otf — sem ele não dá pra renderizar]` |
| Peso (wght) | `[...]` |
| Tamanho em px (na largura da referência) | `[...]` |
| Tracking | `[.../1000 em]` |
| Cor do texto | `[hex]` |
| Caixa / contorno / sombra | `[...]` |
| Alinhamento | `[centralizado em x = ... / outro]` |
| Posição na tela dividida (y) | `[...]` |
| Posição na tela cheia (y da baseline, e % da altura) | `[...]` |
| Nº de linhas por bloco | `[...]` |
| Palavras por bloco | `[n a n]` |
| Nº total de blocos / duração | `[n blocos em m:ss]` |
| Duração mediana do bloco | `[..., s]` |
| Animação | `[troca inteira / palavra por palavra / fade / nenhuma]` |
| Caixa do texto | `[frase normal / maiúsculas]` |
| Pontuação mantida? | `[sim / não]` |
| Primeiros segundos sem legenda? | `[sim, até ... s / não]` |

**Quebra dos blocos:** a regra vale pra qualquer padrão — cada bloco é uma **unidade de sentido** completa, nunca um pedaço arbitrário de N palavras. Cortar onde a fala respira. Nunca separar artigo, preposição ou adjetivo da palavra que acompanham. Ponto final e vírgula fecham o bloco.

*(ex. padrão Tessmann Reels: TikTok Sans wght 500, ~59 px, tracking −30/1000, branca, blocos de 1–3 palavras, mediana 0,67 s — só exemplo.)*

---

## 6. Título / lettering

*Como medir: mesmo método da legenda (passo 6 de `treinar-com-referencia.md`) — altura do texto em px, largura de uma palavra conhecida, posição e passo das linhas, cor, sombra, e se entra com animação ou já começa na tela.*

| Campo | Valor |
|---|---|
| Existe título de gancho? | `[sim / não]` |
| Fonte e peso | `[...]` |
| Tamanho em px | `[...]` |
| Cor | `[hex]` |
| Nº de linhas e passo entre linhas | `[...]` |
| Posição (x, y das linhas e centro do bloco) | `[...]` |
| Entrada / saída | `[já começa na tela / anima / some de uma vez em ... s]` |
| Título e legenda aparecem juntos? | `[sim / não]` |
| Texto da referência | `[transcrever]` |
| Outros letterings (cartelas, grifos, cards) | `[descrever ou "nenhum"]` |

---

## 7. Paleta e cor

*Como medir: passo 6 de `treinar-com-referencia.md` — histograma de cores dominantes e saturação/contraste médios (média de HSV[...,1] e desvio da luma), rodados na referência e no render do aluno. Se o render ficar 30–60 % abaixo da referência, o vídeo parece "sem cor".*

| Campo | Valor |
|---|---|
| Tem cor de destaque? | `[qual / nenhuma]` |
| Cores usadas em grafismos (hex) | `[...]` |
| Clima geral da imagem | `[quente / frio / neutro]` |
| Saturação da referência vs. bruto | `[...]` |
| Contraste da referência vs. bruto | `[...]` |
| Grade a aplicar no material do aluno | `[contraste ..., saturação ..., gamma ..., nitidez ...]` |
| Realce no material de cima | `[sim, sat ... / contraste ... — ou não]` |
| O que NÃO leva realce | `[prints, logos, ...]` |

*(ex. padrão Tessmann criativos: preto e branco só, nenhuma cor de destaque — só exemplo.)*

---

## 8. Área de cima (material de apoio)

*Como medir: listar, na folha de contato, cada clipe da área de cima com timecode e contar quantas trocas existem no trecho. Ritmo e movimento: passo 4 de `treinar-com-referencia.md`.*

| Campo | Valor |
|---|---|
| Tipos de material que entram | `[vídeo real / print de notícia / gravação de tela / foto de pessoa / logo / card]` |
| Nº de cortes no trecho e tempo | `[n cortes em ... s]` |
| Intervalo mediano entre trocas | `[..., s — mediana, não média]` |
| Movimento médio da área de cima | `[... — conta do passo 4.2; abaixo de ~2 é área parada]` |
| Clipe longo é permitido? | `[sim, se tiver movimento próprio / não]` |
| Primeiro quadro do vídeo | `[o que é]` |
| Cards de número/frase | `[existem? fonte, fundo, texto, tamanho — ou "não existem"]` |
| Proibições observadas | `[banco de imagem, b-roll genérico, texto queimado, split-screen dentro do clipe, repetir cena...]` |

**Regras que valem em qualquer padrão:**

- Cada clipe/imagem aparece **uma vez só** no vídeo.
- O material de cima mostra **exatamente o que está sendo dito naquele instante**. Trocar quando a fala muda de assunto.
- Se a fala cita algo específico (uma matéria, um app, uma pessoa, um evento), buscar **aquilo mesmo**, não material genérico "do tema".
- Conferir no fim: linha por linha, "o que ele diz aqui?" x "o que está em cima?" têm que bater.
- Material de terceiros: usar fonte confiável e mostrar atribuição quando for o caso. Nunca apresentar imagem inventada como real.

---

## 9. Apresentador e enquadramento

*Como medir: num quadro de tela cheia, medir a largura do rosto em % da largura do quadro e a altura dos olhos em % da altura.*

| Campo | Valor |
|---|---|
| Tipo de captação | `[selfie de celular / câmera em tripé / estúdio]` |
| Enquadramento em tela cheia | `[rosto ocupa ... % da largura, olhos a ... % da altura]` |
| Enquadramento na dividida | `[rosto a ... % da altura da faixa]` |
| Recorte do material com pessoa | `[larg x alt, centrado no quê]` |
| Câmera acompanha o rosto? | `[sim, suavizada / não]` |
| Movimento de câmera / estabilização | `[...]` |

**Regra fixa:** o recorte é centrado no **rosto detectado**, não a olho. Antes de renderizar, conferir no quadro real do segundo usado que cabeça e mãos cabem, e que não sobra barra preta, tarja, relógio ou logo de canal na borda.

---

## 10. Transições

*Como medir: passo 7 de `treinar-com-referencia.md` — classificar cada corte pelos 10 quadros em volta (pico isolado = corte seco; diferença elevada por vários quadros = dissolve; pulso de luma = flash/overlay).*

**Do overlay da referência registra-se só o efeito** (modo de mistura, duração, onde cai). O arquivo em si não se reaproveita: o aluno tem que ter o dele.

| Campo | Valor |
|---|---|
| Transição entre dividida e tela cheia | `[corte seco / overlay / flash — nome do arquivo se houver]` |
| Duração | `[..., s]` |
| Modo de mistura | `[screen / normal / outro]` |
| Som da transição | `[tem? volume]` |
| Quantas vezes aparece no vídeo | `[...]` |
| Outras transições | `[...]` |

---

## 11. Áudio e música

| Campo | Valor |
|---|---|
| Tem música de fundo? | `[sim / não]` — a trilha da referência **não** se reaproveita; se o aluno quiser música, ele manda o arquivo licenciado dele |
| Estilo e volume | `[...]` |
| Efeitos sonoros | `[quais, onde, volume — ou "nenhum"]` |
| Respiros e silêncios são cortados? | `[sim / não]` |
| Tratamento do áudio da voz | `[...]` |

---

## 12. Formatos de entrega

*O aluno decide quais formatos precisa. Preencher só os que ele vai usar.*

| Formato | Resolução | Usa? | Ajustes específicos |
|---|---|---|---|
| Vertical (Reels/TikTok/Shorts) | `[1080x1920]` | `[sim/não]` | `[divisória, posição da legenda, zoom]` |
| Feed retrato | `[1080x1350]` | `[sim/não]` | `[...]` |
| Quadrado | `[1080x1080]` | `[sim/não]` | `[...]` |
| Horizontal | `[1920x1080]` | `[sim/não]` | `[...]` |

Reels é **um formato só** (RL 1080x1920). Os quatro formatos valem para criativo.

- Pasta de saída: `[caminho local do aluno]` — uma pasta por vídeo, com o nome do vídeo
- Nome do arquivo: `[padrão, sempre com versão, ex.: nome-v2.mp4; criativo sai como "<título> - RL.mp4", "- IN", "- GL", "- YT"]`
- Evitar `?`, `:`, `/` e `*` no nome (quebram em pendrive e HD externo, ExFAT).
- Nunca sobrescrever a versão anterior nem o arquivo bruto.

---

## 13. Checklist antes de entregar

- [ ] Todos os campos deste arquivo preenchidos ou marcados como `não medido`
- [ ] Nenhum valor chutado: cada número veio de uma medição na referência
- [ ] Padrão medido mostrado ao aluno, com as perguntas que a medição não resolve (fonte exata e arquivo dela, trilha, overlays, cor de destaque)
- [ ] Teste de 5 s renderizado no estilo medido e comparado lado a lado com um quadro da referência (tolerâncias no passo 9 de `treinar-com-referencia.md`)
- [ ] Estrutura e tempos batem com o padrão medido
- [ ] Divisória e posição da legenda conferidas num quadro exportado
- [ ] Fonte, peso, tamanho e tracking da legenda conferidos com zoom
- [ ] Blocos de legenda quebrados por unidade de sentido, nenhum artigo/preposição solto
- [ ] Legenda sincronizada com a fala do começo ao fim
- [ ] Área de cima bate com o que está sendo dito, cena por cena
- [ ] Nenhum clipe/imagem repetido
- [ ] Nenhum material genérico de banco de imagem
- [ ] Enquadramento conferido no quadro real de cada clipe (sem barra, tarja, relógio, logo cortado)
- [ ] Cor e realce aplicados conforme a seção 7
- [ ] Áudio sem estouro, sem corte no meio de palavra
- [ ] Formatos exportados conforme a seção 12, com versão no nome
- [ ] Quadros do render final extraídos e lidos linha por linha na folha de contato (não afirmar que assistiu sem ter extraído quadro)
- [ ] Aluno assistiu ao arquivo final, do início ao fim, e aprovou antes de publicar
