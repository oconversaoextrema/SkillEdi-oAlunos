# Padrão Tessmann — YouTube (16:9)

Padrão dos vídeos longos de YouTube do Tiago Tessmann: **apresentador em tela cheia com texto grande por cima
do vídeo**, ilustrações animadas ao lado dele, alguns painéis pretos e inserts de site/matéria real.

Formato: **1920x1080, 30 fps**. Um formato só.

Não confunda com Reels e criativo: aqui **não tem tela dividida em cima/embaixo**, não tem legenda queimada o
vídeo inteiro e a fonte é outra. Se a edição for YouTube, o que vale é este arquivo.

> **O que a skill entrega neste padrão.** Os scripts em `scripts/` renderizam Reels e criativo (vertical), **não
> este formato**. Para YouTube a skill entrega: o corte, a transcrição revisada e o **roteiro de edição completo** —
> bloco por bloco, com o tempo, o tipo de elemento, o texto exato, o tamanho em px e o material a buscar. Você
> monta no seu editor (Premiere, DaVinci, CapCut) ou implementa em Remotion. Tudo aqui está em px de 1080p, então
> dá para reproduzir em qualquer editor.

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
