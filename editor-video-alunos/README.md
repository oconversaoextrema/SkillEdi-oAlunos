# Skill de edição — alunos

Editor de vídeo para usar no Claude (Claude Code ou o app Claude no computador). Traz todas as ferramentas que a
gente usa nas edições do Tiago Tessmann e edita de três jeitos:

- **a partir de uma referência** — você manda um vídeo editado do jeito que gosta e ele copia o estilo;
- **do zero** — você explica como imagina a edição;
- **no padrão do Tiago Tessmann** — Reels, criativos (anúncios) e YouTube, medidos nas edições originais.

## Instalar

1. Coloque a pasta `editor-video-alunos` em `~/.claude/skills/` (vale para todos os projetos) ou em
   `<seu-projeto>/.claude/skills/`. No app do Claude, você também pode enviar o `.zip` em Configurações → Skills.
2. Abra o Claude na pasta onde você vai editar e escreva **`editar`**.

Na primeira vez a skill instala sozinha as ferramentas (5 a 10 minutos, ~1,5 GB, sem senha de administrador), na
pasta `~/.editor-video`:

| ferramenta | para quê |
|---|---|
| Python 3.12 + bibliotecas | o motor dos scripts (PyAV, OpenCV, Pillow, numpy) |
| ffmpeg / ffprobe | cortar, juntar, converter, render final |
| Whisper (faster-whisper, modelo small) | transcrição e legenda palavra por palavra, offline |
| yt-dlp | baixar trechos de vídeo da internet para usar de material |
| Remotion | montar o vídeo em React (tela dividida, inserts, legenda, YouTube) |
| HyperFrames | animações em HTML/GSAP (telas de app, cursor, cartões, lettering) |
| Robust Video Matting | recortar você do fundo (texto passando atrás) |
| Fontes TikTok Sans, Manrope, Inter, Montserrat | licença OFL |

Se quiser instalar antes, no terminal:

```bash
bash ~/.claude/skills/editor-video-alunos/scripts/instalar.sh
```

No Windows (PowerShell):

```powershell
powershell -ExecutionPolicy Bypass -File $HOME\.claude\skills\editor-video-alunos\scripts\instalar.ps1
```

Para só conferir o que está instalado, acrescente `--verificar`.

## O que tem aqui

| arquivo | o que é |
|---|---|
| `SKILL.md` | instalação automática, a pergunta de abertura, as regras de toda edição e a entrega |
| `references/ferramentas.md` | manual das ferramentas: comandos, receitas de ffmpeg, regras do Remotion e do HyperFrames |
| `references/editar-do-zero.md` | as perguntas e o padrão-base quando você descreve a edição |
| `references/treinar-com-referencia.md` | como medir um vídeo de referência e virar o seu padrão |
| `references/modelo-padrao-do-aluno.md` | esqueleto do seu padrão (fica salvo no seu projeto) |
| `references/padrao-tessmann-*.md` | os padrões do Tiago: Reels, criativos, YouTube |
| `references/pipeline-tecnico.md` | o pipeline Python do padrão Tessmann, passo a passo |
| `scripts/instalar.*` | instalador (Mac/Linux `.sh`, Windows `.ps1`) |
| `scripts/` | corte de silêncio, transcrição, recorte de pessoa, download, render de Reels/criativo |
| `assets/remotion-modelo/` | projeto Remotion pronto (vídeo + inserts + legenda palavra por palavra) |
| `assets/hyperframes-modelo/` | composição HyperFrames de exemplo |

Se você edita no Premiere, CapCut ou DaVinci, a skill também entrega o roteiro de edição (cena por cena, legenda
já quebrada, lista de material) em vez do MP4.

Testado em 20/10/2026 num Mac (Apple Silicon) instalando do zero: Whisper, Remotion, HyperFrames, recorte e o
pipeline do padrão Tessmann renderizaram.
