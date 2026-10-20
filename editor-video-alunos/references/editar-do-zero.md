# Editar do zero — o aluno explica como quer

Caminho para quando o aluno não tem vídeo de referência nem quer o padrão do Tessmann: ele descreve a edição e
eu transformo a descrição numa especificação medível, mostro um quadro de teste e só então edito.

## 1. As perguntas (numa mensagem só, numeradas)

> 1. **Onde vai postar e em qual formato?** Reels/TikTok/Shorts (1080x1920), feed (1080x1350), quadrado (1080x1080) ou YouTube (1920x1080). Pode ser mais de um.
> 2. **Como você imagina o vídeo?** Me descreve com suas palavras: ritmo (calmo, dinâmico, frenético), o que aparece na tela além de você, se tem texto grande, se tem tela dividida, efeitos, transições. Se lembrar de algum perfil que edita parecido, me diz o nome.
> 3. **Legenda:** tem? Palavra por palavra ou frase inteira? Cor, tamanho (pequena, média, grande), onde fica (meio, embaixo), alguma palavra em destaque com outra cor?
> 4. **Cores e fonte da sua marca**, se tiver (código da cor, nome da fonte, logo).
> 5. **Música e efeitos sonoros:** sim ou não? Se sim, você manda a música?
> 6. **Material:** você já tem prints, vídeos, fotos, logo? Ou quer que eu busque material real na internet sobre o que você fala?
> 7. **Algo que você NÃO quer** (ex.: "nada de emoji", "sem zoom", "sem música").

Se o aluno responder curto ("quero dinâmico e bonito"), não travar: propor o padrão-base abaixo e perguntar só
"posso seguir assim?".

## 2. Padrão-base (quando a descrição for vaga)

- Vertical 1080x1920, 30 fps, cortes de silêncio, entrada ~0,4 s antes da primeira palavra.
- Legenda palavra por palavra, 1 a 3 palavras por bloco por unidade de sentido, branca, sem serifa, bold, ~80 px,
  tracking levemente negativo, sombra suave, a ~60 % da altura.
- A cada 3–6 s algo muda: zoom leve na pessoa, tela dividida com material real em cima, ou tela cheia de material.
- Material de cima = a coisa citada na fala, no instante da fala (print, gravação de tela, vídeo real).
- Sem música, a menos que ele mande.

## 3. Virar especificação

Escrever `referencias/padrao-do-aluno.md` (esqueleto em `modelo-padrao-do-aluno.md`) com o que ele descreveu,
traduzido em número: tamanho de fonte em px, posição em px, duração de cada bloco, cor em hex, frequência de troca
de cena. O que ele não disse e eu decidi fica marcado **"decidido por mim — confirmar"**.

## 4. Quadro de teste antes do vídeo inteiro

Montar 5 a 10 segundos (ou 3 quadros-chave com `remotion still` / `hf snapshot`) e mostrar: legenda, uma cena com
material, uma troca. Perguntar o que muda. Só depois de "pode seguir" editar o resto. Cada correção dele vai para o
`padrao-do-aluno.md` — na próxima edição esse arquivo já é o padrão dele.

## 5. Ferramenta certa para cada pedido

| ele pediu | usar |
|---|---|
| legenda + cortes + zoom, nada mais | pipeline Python (`criativo_prep.py` + `reels2.py`) ou Remotion |
| tela dividida com material, transições, layouts que mudam | Remotion (`assets/remotion-modelo`) |
| tela de app recriada, cursor clicando, cartões, contadores, lettering animado | HyperFrames |
| texto passando atrás da pessoa | `recortar_pessoa.py` + Remotion ou HyperFrames |
| YouTube 16:9 | Remotion (mesmo modelo, `largura` 1920 / `altura` 1080) |

Detalhes de cada uma em `references/ferramentas.md`.
