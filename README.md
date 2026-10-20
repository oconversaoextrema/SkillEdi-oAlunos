# Skill de edição — alunos

Editor de vídeo para usar no Claude (Claude Code ou o app Claude no computador). Traz **todas as ferramentas** que a
gente usa nas edições do Tiago Tessmann — e instala sozinha na primeira vez.

Quando você escreve **`editar`**, ela pergunta como você quer editar:

- **a) A partir de uma referência** — você manda um vídeo editado do jeito que gosta e ela copia o estilo.
- **b) Do zero** — você explica como imagina a edição e ela monta.
- **c) No padrão do Tiago Tessmann** — Reels, criativos (anúncios) e YouTube, medidos nas edições originais.

## Instalar

Baixe o `.zip` (botão **Code → Download ZIP**) ou clone:

```bash
git clone https://github.com/ruanhoracio-ue/SkillEdi-oAlunos.git
mkdir -p ~/.claude/skills
cp -R SkillEdi-oAlunos/editor-video-alunos ~/.claude/skills/
```

No app do Claude, você também pode enviar a pasta `editor-video-alunos` compactada em Configurações → Skills.

Depois abra o Claude na pasta onde você vai editar e escreva **`editar`**.

## Ferramentas (instaladas automaticamente)

Na primeira vez a skill instala tudo em `~/.editor-video` — 5 a 10 minutos, ~1,5 GB, sem senha de administrador:

| ferramenta | para quê |
|---|---|
| Python 3.12 + bibliotecas | o motor dos scripts (PyAV, OpenCV, Pillow, numpy) |
| ffmpeg / ffprobe | cortar, juntar, converter, render final |
| Whisper (faster-whisper, modelo small) | transcrição e legenda palavra por palavra, offline |
| yt-dlp | baixar trechos de vídeo da internet para usar de material |
| Remotion | montar o vídeo em React (tela dividida, inserts, legenda, YouTube 16:9) |
| HyperFrames | animações em HTML/GSAP (telas de app, cursor, cartões, lettering) |
| Robust Video Matting | recortar você do fundo (texto passando atrás) |
| Fontes TikTok Sans, Manrope, Inter, Montserrat | licença OFL |

Para instalar ou conferir antes, no terminal:

```bash
bash ~/.claude/skills/editor-video-alunos/scripts/instalar.sh              # instala
bash ~/.claude/skills/editor-video-alunos/scripts/instalar.sh --verificar  # só confere
```

Windows (PowerShell): `powershell -ExecutionPolicy Bypass -File $HOME\.claude\skills\editor-video-alunos\scripts\instalar.ps1`

## O que tem no pacote

| arquivo | o que é |
|---|---|
| `SKILL.md` | instalação automática, a pergunta de abertura, as regras de toda edição e a entrega |
| `references/ferramentas.md` | manual das ferramentas: comandos, receitas de ffmpeg, regras do Remotion e do HyperFrames |
| `references/editar-do-zero.md` | as perguntas e o padrão-base quando você descreve a edição |
| `references/treinar-com-referencia.md` | como medir uma referência sua e transformar em padrão |
| `references/modelo-padrao-do-aluno.md` | esqueleto do seu padrão |
| `references/padrao-tessmann-*.md` | os padrões do Tiago: Reels, criativos, YouTube |
| `references/pipeline-tecnico.md` | o pipeline Python do padrão Tessmann, passo a passo |
| `scripts/` | instalador, corte de silêncio, transcrição, recorte de pessoa, download, render de Reels/criativo |
| `assets/remotion-modelo/` | projeto Remotion pronto (vídeo + inserts + legenda palavra por palavra) |
| `assets/hyperframes-modelo/` | composição HyperFrames de exemplo |

Se você edita no Premiere, CapCut ou DaVinci, a skill também entrega o roteiro de edição (cena por cena, legenda
já quebrada, lista de material) em vez do MP4.

## Aviso

Os assets de transição usados no padrão original de Reels (overlay de film burn) são de um pack pago e **não vêm
aqui**. Use um overlay seu ou `burn=None` no config, que corta seco na virada.
