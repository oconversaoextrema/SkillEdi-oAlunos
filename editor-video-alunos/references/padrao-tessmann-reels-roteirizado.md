# Padrão Tessmann — Reels roteirizado (tutorial)

Reels de **dica/tutorial com roteiro**: a pessoa explica um passo a passo (uma ferramenta, uma configuração, um
checklist) e a tela mostra **exatamente aquilo**, no instante da fala. Estilo de criador de conteúdo, não de anúncio.

Formato: **1080x1920, 30 fps**. Um formato só. Feito em **HyperFrames** (HTML/CSS/GSAP → MP4) a partir do modelo em
`work/modelos/hyperframes-modelo`.

Não confundir com o Reels de tela dividida (`padrao-tessmann-reels.md`): aqui a legenda é palavra por palavra desde
o primeiro segundo, os modos alternam o vídeo inteiro e não tem música.

---

## 1. Os três modos — alternar a cada ~3–6 s

| modo | o que aparece | legenda |
|---|---|---|
| **dividida** | material real em **largura total** em cima (1080x900, de y 0 a 900), fundindo num **degradê suave** até o escuro; a pessoa **recortada** embaixo (da orelha para cima recortada, fundo real embaixo) | y ≈ 845, no escuro entre o material e a cabeça — **nunca na testa** |
| **cheia** | a pessoa em tela cheia 9:16, com **a mesma cor** da metade de baixo da dividida | y ≈ 1190, no peito |
| **tela** | tela de app em tela cheia (réplica fiel: WhatsApp, Gerenciador de Anúncios, site, documento…) com cursor | y ≈ 1250–1290; **preta com halo branco** quando a tela é clara |

- **Abertura sempre com a pessoa** (dividida ou cheia). Alternar o tipo de abertura entre os vídeos da série para
  eles não começarem todos iguais. A abertura entra **seca** (sem zoom de entrada no primeiro quadro).
- Nunca o mesmo modo mais de ~20 s seguidos; quatro dividida seguidas só se o material de cima troca a cada ~5 s.

### Degradê da dividida (o detalhe que mais foi corrigido)

Sem card arredondado, sem moldura: o material ocupa a largura toda e some no escuro. O degradê **termina opaco no
fim do material** (y 900) e tem curva suave, nunca uma faixa:

```css
.larga-fade{position:absolute;left:0;top:400px;width:1080px;height:500px;
  background:linear-gradient(rgba(7,7,7,0) 0%,rgba(7,7,7,.04) 15%,rgba(7,7,7,.13) 30%,rgba(7,7,7,.28) 45%,
  rgba(7,7,7,.48) 60%,rgba(7,7,7,.7) 75%,rgba(7,7,7,.88) 88%,#070707 100%)}
```

O fundo da dividida é **#070707** — a mesma cor do fim do degradê (cor diferente = faixa visível).

---

## 2. Legenda

- **Helvetica Neue Bold 86 px**, tracking −0,055 em, branca com sombra. **Uma palavra por vez**, troca **seca** (sem
  animação de entrada).
- Pontuação revisada (vírgula, ponto, interrogação). Artigo, preposição, "e", "ou" **grudam na palavra seguinte** —
  nunca aparecem sozinhos ("a conta", "no Google Ads", "e o perfil"). Expressões fixas juntas ("24 horas", "Google Ads").
- **Nunca duas legendas ao mesmo tempo**: palavras que começam juntas viram um bloco; cada bloco termina quando o
  próximo começa e nunca atravessa a troca de cena.
- **Nunca abaixo de y ≈ 1300** (a interface do Reels cobre). Tela de app alta sobe/encolhe para caber.
- Aqui **não** vale a regra dos 10 s sem legenda — a legenda vai do primeiro ao último segundo.

---

## 3. Material de cima e telas

- **Material real do que está sendo dito**: gravação de tela da ferramenta (do YouTube, do site oficial, do próprio
  aluno), página real, vídeo do produto. Recortar o miolo útil da tela (sem barra do navegador, sem a webcam de quem
  gravou) e redimensionar para 1080x900.
- **Telas recriadas** quando não existe gravação boa (aviso de erro, consulta, conversa): réplica fiel do app, com
  dados de exemplo (empresa, CNPJ, e-mails inventados — avisar o aluno na entrega).
- **Cursor branco** normal; clique com leve ripple. **Caixa vermelha (#FF3B30) só em detalhe pequeno ou difícil de
  ver** (um link, um contador, um "Adm." numa tabela). Nada de caixa em item que já entra sozinho ou em card grande.
- Animação **pontual e no tempo da palavra**: mensagem entra quando é dita, item do checklist marca no "falhou",
  conta apaga (cinza + escuro) no "perde o histórico". Nada de mockup animado em série, ícone solto ou texto grande.
- **Material HDR** (vídeo de iPhone em HLG/bt2020) tem que ser convertido para SDR bt709 antes de entrar — senão o
  render do HyperFrames trava telas e legendas no MP4 final:
  `zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p`
  (conferir com `ffprobe -show_entries stream=color_transfer`).

---

## 4. Transições e som

- **Queima de filme (film burn) só quando muda o tipo de tela** — cheia → dividida, dividida → cheia, entrada e saída de
  tela de app em tela cheia. Dividida → dividida e tela → tela são corte seco (queima em todo corte fica carregado). Overlay em **modo tela (screen)**, o pico de luz alinhado no
  corte, uma queima diferente a cada corte, ~88 % de intensidade. Overlay deitado (16:9) é **girado 90°** para caber
  inteiro no vertical — recortar o meio vira só um clarão branco. Aplicar depois do render com
  `work/queima_cortes.py` (o overlay é do aluno; sem overlay, corte seco).
- Pessoa volta para a tela cheia: close 1,55x desfocado que abre em 0,45 s. Tela → tela: zoom 1,08 → 1.
- **Sem whoosh**. Efeitos só de **clique** (cursor), **pop** (mensagem, item, caixa) e **popup** (janela/aviso).
- **Sem música** — só a voz, master **−15 LUFS** (`loudnorm=I=-15:TP=-1.5:LRA=11`).

---

## 5. Cortes na grade de quadros (obrigatório)

Todo início e fim de cena tem que cair **num quadro exato** (múltiplo de 1/30 s). Corte no meio do quadro
(ex. 49,55 s) faz o HyperFrames **repetir 1 quadro a cada 3** no vídeo daquele trecho — a pessoa fica "travadinha"
(~20 fps). Arredondar os tempos das cenas: `t = round(t * 30) / 30`.

Conferir no MP4 final, trecho por trecho, a diferença entre quadros vizinhos: quadro parado 1 a cada 3 com
movimento nos vizinhos = travado.

---

## 6. Chamada final (CTA)

- **"Me segue / deixa o like"**: card branco do Instagram (foto, @perfil com selo, botão azul "Seguir") com o cursor
  clicando **exatamente na palavra "segue"** → vira "Seguindo"; coração vermelho estourando no "like".
- **"Link na bio"**: perfil do Instagram em escuro (foto, números, bio) → zoom no link com caixa vermelha → toque →
  navegador do Instagram sobe → a página/chat do link carregando. Fica na **dividida**, não em tela cheia.
- Emenda conteúdo → CTA (tomadas diferentes): conferir a forma de onda e **nunca cortar no meio da última palavra**.
  O fim vai **até a última palavra do CTA** e fecha com fade de 0,3 s para o preto.

---

## 7. Corte do bruto

Roteiro gravado várias vezes: fica **a última tomada completa** de cada frase. Pular a frase que ele interrompeu no
meio e usar a regravação. Cortar sempre dentro do silêncio (conferir a energia), nunca no meio da palavra. Depois de
juntar as tomadas, cortar as pausas longas e **transcrever o áudio já cortado**.

---

## 8. Checklist antes de entregar

- [ ] Abre com a pessoa, entrada seca.
- [ ] Cada cena mostra o que está sendo dito naquele instante; nenhum material repetido.
- [ ] Degradê da dividida liso, sem faixa; fundo #070707.
- [ ] Legenda: uma palavra por vez, nada solto, nada sobreposto, nada abaixo de 1300, preta nas telas claras.
- [ ] Caixa vermelha só em detalhe pequeno.
- [ ] Cortes na grade de 1/30 s e nenhum trecho travado no MP4 final.
- [ ] Queima de filme só nas trocas de tipo de tela, alinhada no corte.
- [ ] Sem música; voz a −15 LUFS.
- [ ] CTA inteiro até a última palavra.
- [ ] Dados inventados das telas recriadas avisados ao aluno; `fontes.md` com o material real usado.
