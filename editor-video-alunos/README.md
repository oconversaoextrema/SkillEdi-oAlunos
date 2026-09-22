# Skill de edição — alunos

Pacote de edição de Reels, criativos (anúncios) e vídeos de YouTube no padrão do Tiago Tessmann, para os
alunos usarem no Claude Code.

## Instalar

Copie a pasta inteira para o projeto onde você edita:

```
<seu-projeto>/.claude/skills/editor-video-alunos/
```

Ou, para deixar disponível em todos os seus projetos:

```
~/.claude/skills/editor-video-alunos/
```

Abra o Claude Code na pasta do projeto e escreva **`editar`**. A skill começa perguntando se você quer usar
uma referência sua ou o padrão do Tessmann.

## O que tem aqui

| arquivo | o que é |
|---|---|
| `SKILL.md` | as perguntas de abertura, as regras que valem em toda edição e o fluxo de entrega |
| `references/padrao-tessmann-reels.md` | o padrão de Reels, medido nas edições originais |
| `references/padrao-tessmann-criativos.md` | o padrão de criativos (anúncios), com os quatro formatos |
| `references/padrao-tessmann-youtube.md` | o padrão de YouTube 16:9 (texto grande sobre o vídeo, painéis, inserts) |
| `references/treinar-com-referencia.md` | como medir uma referência sua e virar padrão |
| `references/modelo-padrao-do-aluno.md` | esqueleto em branco do seu padrão |
| `references/pipeline-tecnico.md` | instalação e passo a passo de render |
| `scripts/` | o pipeline (corte, transcrição, rosto, render) e dois configs de exemplo |

## Antes de rodar

Você precisa de Python 3.11 ou mais novo, ffmpeg e a fonte TikTok Sans variável. Está tudo em
`references/pipeline-tecnico.md`.

Você não precisa dos scripts para usar a skill: se você edita no Premiere, CapCut ou DaVinci, os arquivos de
padrão valem como especificação (tamanho de fonte, posição, tempos, ritmo) e a skill monta o roteiro de
edição — cena por cena, com a legenda já quebrada e a lista de material a buscar.

O padrão de YouTube é 16:9 e não tem renderizador aqui (os scripts fazem vertical): nele a skill entrega o
corte, a transcrição revisada e o roteiro de edição, e você monta no seu editor.
