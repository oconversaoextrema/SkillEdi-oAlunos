# Ferramentas — o que cada uma faz e como usar

Tudo é instalado pelo `scripts/instalar.sh` (Mac/Linux) ou `scripts/instalar.ps1` (Windows) na pasta
`~/.editor-video` do aluno, sem senha de administrador e sem mexer no resto do computador. Os caminhos ficam em
`~/.editor-video/ambiente.json`; os scripts da skill leem de lá (`scripts/ambiente.py`).

Antes de usar no terminal, carregue o ambiente (põe ffmpeg, node, `hf` e `remotion` no PATH):

```bash
source ~/.editor-video/ambiente.sh            # Mac/Linux
. $HOME\.editor-video\ambiente.ps1           # Windows (PowerShell)
PY=~/.editor-video/venv/bin/python           # Windows: $HOME\.editor-video\venv\Scripts\python.exe
```

## Mapa rápido

| ferramenta | para quê | como chamar |
|---|---|---|
| **ffmpeg / ffprobe** | cortar, juntar, converter, extrair áudio e quadros, render final | `ffmpeg`, `ffprobe` (no PATH depois do `ambiente.sh`) |
| **Whisper** (faster-whisper, modelo `small`) | transcrição palavra por palavra → legenda, cortes, cenas amarradas à fala | `$PY work/transcrever.py audio.wav` |
| **yt-dlp** | baixar trecho de vídeo do YouTube/TikTok/Instagram para usar de material | `$PY work/baixar.py URL pasta [ini fim] [nome]` |
| **OpenCV** | achar o rosto (enquadramento), folha de contato | `$PY work/folha.py video.mp4` |
| **Robust Video Matting** | recortar a pessoa do fundo (texto/imagem passando atrás dela) | `$PY work/recortar_pessoa.py video.mp4 pessoa.webm [--degrade A B]` |
| **Pillow + PyAV** | pipeline Python de Reels/criativo (legenda desenhada quadro a quadro) | `work/criativo_prep.py`, `reels2.py`, `criativo.py` |
| **Remotion** | vídeo em React: montagem completa com legenda, inserts, tela dividida, motion | `remotion render` na pasta do projeto Remotion |
| **HyperFrames** | animação em HTML/CSS/GSAP → MP4 (telas de app, cursor, cartões, lettering) | `hf snapshot`, `hf render` |
| **Fontes** | TikTok Sans (variável), Manrope, Inter, Montserrat — todas OFL | `~/.editor-video/fontes/` (ligada em `ferramentas/fontes/` do projeto) |

Helvetica Neue / SF Pro já vêm no Mac. No Windows, o equivalente mais próximo instalado é Arial — avisar o aluno se
a referência dele usa Helvetica e ele estiver no Windows.

## Projeto novo

Uma vez por projeto (pasta onde o aluno edita):

```bash
$PY ~/.claude/skills/editor-video-alunos/scripts/novo_projeto.py .
```

Cria `brutos/ saidas/ referencias/ work/ ferramentas/`, copia os scripts para `work/`, grava
`ferramentas/ffmpeg_path.txt`, liga `models/` e `ferramentas/fontes/` às pastas instaladas e copia os modelos de
Remotion e HyperFrames para `work/modelos/`.

## Receitas de ffmpeg que mais aparecem

```bash
ffprobe -v error -show_entries stream=width,height,r_frame_rate:format=duration -of default=nw=1 bruto.mov
ffmpeg -i bruto.mov -vn -ac 1 -ar 16000 audio.wav                         # áudio para o Whisper
ffmpeg -ss 12.5 -i bruto.mov -frames:v 1 quadro.png                        # um quadro
ffmpeg -i in.mp4 -vf "crop=608:1080:656:0,scale=1080:1920:flags=lanczos" -c:v libx264 -crf 16 cheio.mp4   # 16:9 → 9:16 no rosto
ffmpeg -i in.mp4 -af "highpass=f=90,afftdn,loudnorm=I=-16:TP=-1.5:LRA=9" -c:v copy voz.mp4                # voz tratada
ffmpeg -i video.mp4 -i voz.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest final.mp4           # juntar áudio
```

Entrega para redes: H.264, `yuv420p`, `-crf 16` a `18`, `-movflags +faststart`, AAC 192k, 30 fps.

## Cortes de silêncio e transcrição

- Cortar com `work/cortar_silencios.py` (detector relativo ao piso de ruído). Nunca cortar pelo tempo das palavras.
- **Transcrever depois de cortar**: os tempos nascem na linha do tempo final.
- `transcrever.py` imprime `índice:palavra@tempo`. Cena, legenda e efeito sonoro se amarram a esses índices.
- `--prompt "Nome da Marca, Fulano, CPF, ChatGPT"` ajuda o Whisper a acertar nome próprio e jargão. Mesmo assim,
  revisar a transcrição inteira antes de renderizar.

## Remotion

Modelo em `work/modelos/remotion-modelo/` (copiado do `assets/remotion-modelo/` da skill):
- `public/edicao.json` = tudo que muda por vídeo: bruto, duração, palavras do Whisper, blocos de legenda, inserts
  (vídeo/imagem, início/fim, `cima` = tela dividida ou `cheia`) e estilo (fonte, tamanho, cor, y da legenda).
- `src/Video.tsx` = a montagem. Para um estilo novo, mudar aqui (componentes, transições, motion).

Para cada vídeo: copiar o modelo para `work/<id>/remotion/`, ligar o `node_modules` instalado e renderizar:

```bash
cp -R work/modelos/remotion-modelo work/r1/remotion
ln -s ~/.editor-video/remotion-modelo/node_modules work/r1/remotion/node_modules    # Windows: mklink /J
cp brutos/corte.mp4 work/r1/remotion/public/bruto.mp4
cd work/r1/remotion && remotion still Video quadro.png --frame=90 && remotion render Video ../../../saidas/video-v1.mp4
```

Conferir com `remotion still` (um quadro) antes do render inteiro. Arquivos usados no vídeo ficam em `public/` e
entram com `staticFile()`.

## HyperFrames

Modelo em `work/modelos/hyperframes-modelo/index.html`. Uma página HTML 1080x1920 (ou 1920x1080) com uma timeline
GSAP; o HyperFrames abre no Chrome e captura quadro a quadro.

```bash
hf check pasta/          # erros de JS, mídia faltando, elementos sem id
hf snapshot pasta/ --at 1.5,4.0,8.2 --no-end    # PNGs nesses tempos (conferir antes de renderizar)
hf render pasta/ -o saidas/anim-v1.mp4 --fps 30 --quality delivery
```

Regras que quebram o render se esquecer:
1. Todo `<video>`/`<audio>` com `data-start` precisa de `id` — sem id ele congela.
2. Cronometrar o pai **ou** o `<video>` filho, nunca os dois.
3. `data-media-start="2.5"` = de onde o vídeo começa a tocar (trim).
4. Elemento animado pelo GSAP não pode ter `transform` no CSS (usar `tl.fromTo`).
5. A timeline começa pausada e é registrada em `window.__timelines["<data-composition-id>"]`.
6. Elementos com tempo próprio levam `class="clip"`.

Bom para: telas de app recriadas (WhatsApp, ChatGPT, planilha) com cursor clicando e caixa de destaque, cartões,
contadores, lettering grande, colagens. Para posicionar cursor/caixa em cima de um item, colocar a caixa **dentro**
do elemento-alvo (com `position:relative`) em vez de chutar coordenadas.

## Recorte da pessoa (texto atrás dela)

`recortar_pessoa.py` gera `.webm` VP9 com alpha. Por cima de um fundo/animação, a pessoa fica na frente e o
conteúdo passa atrás. `--degrade A B` mantém o fundo real na parte de baixo e só recorta da cabeça para cima (efeito
suave, sem cara de tela dividida). Em HyperFrames: `<video id="rc" class="clip" src="pessoa.webm" ...>` com z-index
acima do conteúdo. Em Remotion: `<OffthreadVideo transparent src=...>`.

## Material da internet

`baixar.py` usa o yt-dlp: baixa só o trecho necessário. Antes de baixar, pedir autorização ao aluno (o que é, de
onde vem, tamanho). Registrar em `referencias/<vídeo>/fontes.md`: URL, autor, data, onde entrou no vídeo.

## Se algo falhar

- `bash scripts/instalar.sh --verificar` (Windows: `instalar.ps1 --verificar`) mostra o que está faltando.
- Rodar o instalador de novo completa o que faltou; o que já está instalado é pulado.
- Sem internet na hora: a instalação não termina, mas depois de instalado tudo roda offline (Whisper inclusive).
- Mac com chip Intel e Linux funcionam igual; no Windows o render do HyperFrames/Remotion é mais lento.
