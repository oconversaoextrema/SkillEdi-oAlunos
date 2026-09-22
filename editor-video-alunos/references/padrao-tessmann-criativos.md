# Padrão Tessmann — CRIATIVOS (anúncios)

Este é o padrão de edição de **anúncios** do Tiago Tessmann. Ele é separado do padrão de Reels: aqui não tem cor de destaque, não tem grafismo, não tem lettering espalhado. O que segura a atenção é rosto grande, legenda curta e ritmo de troca.

Fonte do padrão: **TikTok Sans**, arquivo **variável** em `ferramentas/fontes/TikTokSans-Variable.ttf` (eixos opsz 12–36, wdth, wght 300–900, slnt — o código chama `set_variation_by_axes([36, 100, wght, 0])`). Um `.ttf` estático não serve.

Quem executa este padrão: `scripts/criativo_prep.py` (corte, grade, voz, transcrição, rosto) e `scripts/criativo.py` (render). Instalação, estrutura de pastas, campos do config e comandos estão em `references/pipeline-tecnico.md` — leia junto com este arquivo. O render sai em **30 fps** (a referência medida é 29,97).

---

## 1. Duas variantes — PERGUNTE ANTES DE EDITAR

Antes de qualquer edição, pergunte ao aluno: **"essa leva é dividida ou inteira?"**. Não comece sem a resposta.

| Variante | O que é |
|---|---|
| **Dividida** | Gancho em tela dividida: apresentador em cima, material real embaixo. Título na divisória. Corte seco pra tela cheia. Cutaways voltam pra dividida no meio. |
| **Inteira** | Tela cheia do primeiro quadro ao fim. Sem material embaixo, sem cutaway. Título e legenda iguais aos da dividida — confirmar com o aluno se o título entra. |

No config do vídeo (`work/<id>/<id>.py`, lido por `criativo.py`) isso é o campo `variante`: `'dividida'` (padrão) ou `'inteira'`.

---

## 2. Estrutura (tempos medidos na referência)

Referência do padrão: 1080x1920, 29,97 fps, 1:21 de duração. Apresentador em estúdio escuro, camiseta preta, microfone.

| Trecho | Layout | O que acontece |
|---|---|---|
| 0,00–3,70 s | Tela dividida (divisória em y ≈ 960) | Embaixo, clipes reais de notícia. Corte seco a cada ~0,6–1,3 s (cortes em 0,47 / 1,10 / 1,67 / 2,44 / 3,70). |
| 0,00–9,80 s | Título | Título do gancho centrado na divisória, já na tela desde o quadro 1, sem animação. Some de uma vez em 9,8 s. |
| 3,70 s | Corte seco | Sai a dividida, entra o apresentador em tela cheia. O título continua exatamente no mesmo lugar (y ≈ 940). |
| 9,80–81 s | Tela cheia | Só apresentador + legenda. **Título e legenda nunca aparecem juntos.** |
| 48,55–50,62 s | Cutaway em dividida | Apresentador em cima (enquadramento mais aberto), embaixo o vídeo do que está sendo citado. Corte seco entrando e saindo. Legenda continua no mesmo y, por cima do material. |

**Cortes no trecho de tela cheia:** jump cuts simples entre takes, nos tempos 9,8 / 15,5 / 21,8 / 32,6 / 36,3 / 58,2 / 65,8 / 78,6 / 79,6 s.

**Não existe zoom punch nem Ken Burns.** A variação de tamanho do rosto vem do próprio apresentador se mexendo, não do editor. O único movimento programado é um leve push de 1,00 → 1,04 no material da área de baixo enquanto ele está na tela.

O vídeo termina 0,5 s depois da última palavra, com um fade pra preto de 0,3 s.

---

## 3. Título do gancho

- TikTok Sans **Bold (wght 700)**, **64 px**, branco.
- **2 linhas**, centrado em x = 540 (metade da largura).
- Linhas em y 875–934 e 945–1004; passo de 70 px entre linhas. Bloco centrado em y ≈ 940, ou seja, **exatamente em cima da divisória**.
- Sombra escura suave. **Sem caixa, sem contorno, sem animação.**
- Some de uma vez, no fim da frase do gancho (~9,8 s na referência).
- Durante o gancho, o render desenha sempre uma sombra em gradiente no topo da área de baixo (240 px, preto até alpha 190 no topo) pro título não cair em fundo claro de manchete.

Exemplo de título da referência: "Algo está acontecendo no / Brasil e ninguém está vendo".

---

## 4. Legenda

- TikTok Sans **wght ~650**, **~51 px**. Referência de medida: o bloco "tá sendo um ano difícil," mede 521 px de largura e 52 px de ascendente a descendente.
- Branca, **sem caixa, sem contorno**, sombra escura suave.
- **Centrada em x = 540, baseline em y ≈ 1218** (63,4 % da altura; topo do texto em 1178). Fica abaixo do queixo, nunca em cima da boca. Mesma posição em tela cheia e no cutaway dividido.
- **Uma linha só, 1 a 4 palavras.** Caixa normal de frase, pontuação mantida ("vê nos comentários,", "do que uma agência cobra.", "Fechado?").
- **Troca inteira, sem animação.** Na referência: 73 blocos em 81 s, intervalo mediano **1,03 s** (mínimo 0,17 s, máximo 7,4 s no gancho). Sem palavra por palavra, sem destaque de cor, sem fade.

### 4.1 Quebra por unidade de sentido

Cada bloco fecha uma **ideia completa**, nunca um pedaço arbitrário de N palavras. Corte onde a fala respira: entre sujeito e ação, antes de conector ("enquanto", "que", "e"), antes de complemento longo.

Nunca separe artigo, preposição ou adjetivo da palavra que acompanham. Ponto final e vírgula fecham o bloco — não comece frase nova no meio de um bloco.

**BOM:**
`A cidade` / `despertava lentamente` / `enquanto a chuva fina` / `cobria as ruas.` / `No café da esquina,` / `pessoas conversavam` / `sobre planos,` / `viagens e problemas` / `que pareciam enormes` / `naquela manhã.` / `Um cachorro` / `observava tudo` / `pela janela,` / `esperando seu dono` / `terminar o café.`

**RUIM:**
`A cidade despertava` / `lentamente enquanto a` / `chuva fina cobria as` / `ruas. No café da` / `esquina, pessoas` / `conversavam sobre` / `planos, viagens e` / `problemas que` / `pareciam enormes naquela` / `manhã. Um cachorro`

Repare no RUIM: "cobria as / ruas" separa o artigo do substantivo, e "ruas. No café da" começa frase nova no meio do bloco. Os dois são erro.

---

## 5. Enquadramento

**Tela cheia — bem fechado:** rosto ocupando **~55–65 % da largura** do quadro, **olhos em ~30 % da altura**. O padrão do renderizador é zoom 1,32 com o rosto ancorado em 0,33 da altura do recorte.

**Como chegar lá:** rastreie o rosto quadro a quadro e recorte a partir da posição rastreada — não no olho. A trilha do rosto precisa ser **limpa antes de usar**, senão a câmera "buga":

- descartar detecção falsa (salto maior que 380 px, ou tamanho fora de 45 % da mediana local);
- interpolar os buracos;
- suavizar (~0,8 s de janela);
- limitar a velocidade do movimento a 260 px/s.

Isso é o `rosto_suave()` de `scripts/criativo.py` (parâmetros `n=8`, `vmax=260.0`), aplicado automaticamente no render em cima do `face_track.json` que o prep gerou. Sem essa limpeza, seis amostras falsas seguidas já bastam pra estragar a abertura.

**Dividida:** o apresentador ocupa a faixa de cima inteira, sem zoom extra (zoom 1,0), com o rosto mais alto no recorte (`face_at` por formato — ver tabela).

No config, a tela cheia vem do campo `enquadro`: `lambda t: (zoom, face_at)`, padrão `(1.32, 0.33)`.

---

## 6. Cutaway

Sempre que a fala citar algo mostrável — uma tela, um produto, uma notícia — entra um cutaway:

- volta pra tela dividida, **corte seco entrando e saindo**, 1–2 s;
- material real embaixo, apresentador em cima com enquadramento mais aberto;
- a legenda continua no mesmo y, sem se mexer.

No formato vertical (RL) o material encosta na divisória e a legenda cai por cima dele com um gradiente escuro por baixo. Nos formatos mais baixos, o material recua e a legenda cai em faixa preta (ver tabela).

---

## 7. Cores e clima

**Preto e branco, só.** Nenhuma cor de destaque, nenhum grafismo, nenhum lettering em tela cheia, nenhuma vinheta, nenhum ícone. Fundo dos painéis e das bordas: preto puro.

---

## 8. Os quatro formatos

O criativo pode sair em até quatro arquivos — pergunte ao aluno quais ele quer (RL é o padrão). Como a largura é a mesma em três deles, **título 64 px e legenda 51 px não mudam**. O que muda:

| | **RL** 1080x1920 | **IN** 1080x1350 | **GL** 1080x1080 | **YT** 1920x1080 |
|---|---|---|---|---|
| Divisória (y) | 960 | 675 | 600 | usa a do IN |
| Legenda (baseline) | 1218 | 856 | 685 | usa a do IN |
| Tela cheia | zoom do config, rosto em 0,33 | zoom x0,95, rosto em 0,34 | zoom x0,85, rosto em 0,34 | usa o IN |
| Dividida (rosto) | 0,44 | 0,47 | 0,50 | usa o IN |
| Cutaway | material encosta na divisória, legenda cai por cima com gradiente | material recuado 200 px, legenda em faixa preta | recuado 120 px | usa o IN |

Notas:

- **GL (1:1)** tem a faixa de cima maior (divisória em 600, não em 540) pra a cabeça caber.
- **Quadro mais baixo pede menos zoom** — por isso IN é x0,95 e GL é x0,85: o queixo não pode bater na legenda.
- **YT 1920x1080** é a composição do IN reduzida a **864x1080 e centrada, com laterais pretas**. Não é um layout novo: é o IN dentro de um quadro 16:9 preto. Esse é o modelo aprovado.

---

## 9. Grade de cor

A grade é aplicada uma vez, na preparação do bruto, e vale pra todos os renders. Valores medidos:

```
eq=contrast=1.32:saturation=1.28:gamma=0.97,
colorbalance=rs=0.04:bs=-0.05:rm=0.03:bm=-0.03,
unsharp=5:5:0.6
```

Ou seja: contraste **1,32**, saturação **1,28**, gamma **0,97**, um leve quente nas sombras e médios (vermelho pra cima, azul pra baixo) e nitidez. Motivo: sem isso o vídeo sai "sem cor".

O bruto é escalado pra **1620x2880** antes da grade, pra aguentar zoom de 1,3–1,5 sem perder nitidez.

---

## 10. Como reproduzir, passo a passo

1. **Pergunte a variante** (dividida ou inteira).
2. **Corte os respiros** do bruto com detector de silêncio relativo ao piso de ruído — cortes só dentro de silêncio. O vídeo abre 0,20 s antes da primeira palavra e esse respiro de entrada (e os 0,45 s de saída) não é encurtado.
3. **Prepare a base:** concatenar os segmentos, escalar pra 1620x2880, aplicar a grade.
4. **Trate a voz:** highpass 90 Hz, redução de ruído, lowpass 12 kHz, compressor leve, loudness normalizado em **I = −16 LUFS, TP = −1,5 dB, LRA 9**.
5. **Transcreva o áudio JÁ cortado**, com timestamps por palavra, e revise a transcrição (erros viram entradas no campo `repl` do config).
6. **Rastreie o rosto** e limpe a trilha (seção 5).

Os passos 2 a 6 são um comando só: `python work/criativo_prep.py <id> brutos/<arquivo>`.
7. **Gancho:** primeiros ~4 s em dividida, com clipes/imagens reais embaixo trocando a cada ~1 s. Título Bold 64 px centrado na divisória até ~10 s. Corte seco pra tela cheia em ~4 s.
8. **Legenda:** blocos de 1–4 palavras, ~1 s cada, wght 650 / 51 px, baseline em 63,4 % da altura.
9. **Cutaways** onde a fala cita algo mostrável.
10. **Renderize os formatos pedidos**, sempre da raiz do projeto. RL é o padrão; os outros saem com `--formatos`, que precisa vir antes de `--stills`/`--blocos`:

```bash
python work/c1/c1.py --blocos              # confere os blocos de legenda e os tempos
python work/c1/c1.py --stills 0.5,4.2,12.0 # prévias em work/c1/prev/
python work/c1/c1.py                       # RL
python work/c1/c1.py --formatos IN,GL,YT   # gera ...-IN.mp4, ...-GL.mp4, ...-YT.mp4
```

---

## 11. Material real da área de baixo

O que aparece embaixo no gancho e nos cutaways tem que ser **material real e verificado** do que está sendo dito: a notícia citada, o print da tela citada, a página do produto citado. Confira identidade, contexto e data antes de usar. Não invente imagem e não apresente coisa genérica como se fosse a notícia real. Se não achar, diga e peça o arquivo em vez de improvisar.

Guarde o material numa pasta de referências do vídeo, com anotação de URL, autor e data de cada arquivo, e mostre a atribuição na tela quando o material for de terceiros.

---

## 12. Checklist antes de entregar

- [ ] A variante (dividida ou inteira) foi perguntada e confirmada antes da edição.
- [ ] Título: TikTok Sans Bold 64 px, 2 linhas, centrado na divisória, sem animação, some de uma vez.
- [ ] Título e legenda **nunca** aparecem juntos na tela.
- [ ] Legenda: 1–4 palavras por bloco, ~1 s cada, wght 650 / 51 px, baseline em 63,4 % da altura, sem animação.
- [ ] Nenhum bloco de legenda separa artigo/preposição/adjetivo da palavra que acompanham.
- [ ] Nenhum bloco começa uma frase nova no meio (ponto final e vírgula fecham bloco).
- [ ] Transcrição revisada: a legenda bate palavra por palavra com a fala.
- [ ] Tela cheia fechada: rosto em ~55–65 % da largura, olhos em ~30 % da altura.
- [ ] Trilha do rosto limpa e suavizada — nenhum tranco de câmera, principalmente nos primeiros segundos.
- [ ] Jump cuts secos, sem zoom punch e sem Ken Burns.
- [ ] Material da área de baixo é real, verificado e corresponde ao que está sendo dito naquele segundo.
- [ ] Preto e branco: nenhuma cor de destaque, nenhum grafismo, nenhum lettering em tela cheia.
- [ ] Grade de cor aplicada (contraste 1,32 / saturação 1,28 / gamma 0,97).
- [ ] Respiros cortados, áudio normalizado, sem clique nas emendas.
- [ ] Os formatos escolhidos renderizados e conferidos: no IN e no GL o queixo não encosta na legenda; no YT as laterais pretas estão simétricas.
- [ ] Fade final de 0,3 s pra preto, vídeo terminando ~0,5 s depois da última palavra.

---

## 13. Entrega

Os arquivos dos formatos escolhidos vão numa **pasta local do aluno**, com o nome do vídeo, no formato:

```
<título> - RL.mp4
<título> - IN.mp4
<título> - GL.mp4
<título> - YT.mp4
```

Evite `?`, `:`, `/` e `*` no nome do arquivo — alguns sistemas de arquivo não aceitam. Cada nova versão ganha número no nome (`-v2`, `-v3`); nunca sobrescreva a versão anterior.
