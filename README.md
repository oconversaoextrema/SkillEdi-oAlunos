# Skill de edição — alunos

Pacote de edição de **Reels** e **criativos (anúncios)** verticais no padrão do Tiago Tessmann, para usar
dentro do Claude Code.

A skill começa perguntando se você quer **mandar uma referência sua** de edição, para ela copiar o seu
estilo, ou usar o **padrão do Tessmann** — que já está medido aqui, em pixels e em segundos.

Padrões prontos: **Reels**, **criativo (anúncio)** e **YouTube (16:9)**.

## Instalar

Clone e copie a pasta `editor-video-alunos/` para as skills do seu projeto:

```bash
git clone https://github.com/ruanhoracio-ue/SkillEdi-oAlunos.git
mkdir -p <seu-projeto>/.claude/skills
cp -R SkillEdi-oAlunos/editor-video-alunos <seu-projeto>/.claude/skills/
```

Para deixar disponível em todos os seus projetos, copie para `~/.claude/skills/` em vez da pasta do projeto.

Depois abra o Claude Code na pasta do projeto e escreva **`editar`**.

## O que a skill pergunta

1. Referência sua ou padrão do Tiago Tessmann?
2. Reels, criativo (anúncio) ou YouTube?
3. Se for criativo: tela dividida ou tela inteira?
4. Formatos — criativo sai em RL 1080x1920, IN 1080x1350, GL 1080x1080 e YT 1920x1080; Reels é só RL 1080x1920 e YouTube só 1920x1080.
5. Algo específico: título, material que você já tem, trecho para cortar fora.

Só depois das respostas ela começa a editar.

## O que tem no pacote

| arquivo | o que é |
|---|---|
| `SKILL.md` | as perguntas de abertura, as regras de toda edição e o fluxo de entrega |
| `references/padrao-tessmann-reels.md` | o padrão de Reels, medido nas edições originais |
| `references/padrao-tessmann-criativos.md` | o padrão de criativos, com os quatro formatos |
| `references/padrao-tessmann-youtube.md` | o padrão de YouTube 16:9: texto grande sobre o vídeo, painéis pretos, inserts |
| `references/treinar-com-referencia.md` | como medir uma referência sua e transformar em padrão |
| `references/modelo-padrao-do-aluno.md` | esqueleto em branco do seu padrão |
| `references/pipeline-tecnico.md` | instalação e passo a passo do render |
| `scripts/` | o pipeline (corte de respiros, transcrição, rastreio de rosto, render) e dois configs de exemplo |

## Antes de rodar

Python 3.11 ou mais novo, ffmpeg e a fonte TikTok Sans variável. O passo a passo está em
`editor-video-alunos/references/pipeline-tecnico.md`.

Você não precisa dos scripts para usar a skill: se você edita no Premiere, CapCut ou DaVinci, os arquivos de
padrão valem como especificação (tamanho de fonte, posição, tempos, ritmo) e a skill monta o roteiro de
edição — cena por cena, com a legenda já quebrada e a lista de material a buscar.

## YouTube

O padrão de YouTube é 16:9 e **não tem renderizador aqui** — os scripts do pacote fazem vertical. Nesse padrão a
skill entrega o corte, a transcrição revisada e o **roteiro de edição completo** (tempo, elemento, texto, tamanho
em px e material a buscar), e você monta no seu editor.

## Aviso

Os assets de transição usados no padrão original (overlay de film burn) são de um pack pago e **não vêm
aqui**. Use um overlay seu ou `burn=None` no config, que corta seco na virada.
