import {AbsoluteFill, OffthreadVideo, Img, Sequence, interpolate, spring, useCurrentFrame, useVideoConfig, staticFile} from 'remotion';

// Modelo genérico: vídeo da pessoa + inserts (vídeo/imagem) em cima ou em tela cheia + legenda palavra por palavra.
// A skill gera public/edicao.json com a transcrição (Whisper) e o plano de cenas. Ajuste o estilo em ESTILO.

type Palavra = {w: string; s: number; e: number};
type Insert = {
  arquivo: string;            // dentro de public/
  tipo: 'video' | 'imagem';
  ini: number; fim: number;   // segundos na linha do tempo final
  modo: 'cima' | 'cheia';     // cima = tela dividida (pessoa embaixo); cheia = cobre a tela toda
  inicioMidia?: number;
};
export type Props = {
  bruto: string; fps: number; largura: number; altura: number; duracao: number;
  palavras: Palavra[]; blocos: number[][]; inserts: Insert[];
  estilo: {fonte: string; tamanho: number; cor: string; destaque: string; yLegenda: number; yLegendaDividida: number; divisoria: number};
};

const Legenda = ({p}: {p: Props}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const i = p.blocos.findIndex((b, k) => {
    const ini = p.palavras[b[0]].s;
    const prox = p.blocos[k + 1] ? p.palavras[p.blocos[k + 1][0]].s : p.duracao;
    const fim = Math.min(prox, p.palavras[b[b.length - 1]].e + 0.5);
    return t >= ini && t < fim;
  });
  if (i < 0) return null;
  const dividida = p.inserts.some((x) => x.modo === 'cima' && t >= x.ini && t < x.fim);
  return (
    <div style={{position: 'absolute', left: 40, right: 40, top: dividida ? p.estilo.yLegendaDividida : p.estilo.yLegenda,
      transform: 'translateY(-50%)', textAlign: 'center', fontFamily: p.estilo.fonte, fontWeight: 700,
      fontSize: p.estilo.tamanho, lineHeight: 1.02, letterSpacing: '-0.05em', color: p.estilo.cor,
      textShadow: '0 0 3px rgba(0,0,0,.55), 0 4px 22px rgba(0,0,0,.55)'}}>
      {p.blocos[i].map((k) => {
        const w = p.palavras[k];
        const f0 = Math.round(w.s * fps);
        const s = spring({frame: frame - f0, fps, config: {damping: 14, stiffness: 220}});
        return (
          <span key={k} style={{display: 'inline-block', marginRight: '0.22em', opacity: frame >= f0 ? 1 : 0,
            transform: `scale(${interpolate(s, [0, 1], [0.86, 1])})`}}>{w.w}</span>
        );
      })}
    </div>
  );
};

export const Video = (p: Props) => {
  const {fps, width, height} = useVideoConfig();
  return (
    <AbsoluteFill style={{backgroundColor: '#000'}}>
      <OffthreadVideo src={p.bruto} style={{width, height, objectFit: 'cover'}} />
      {p.inserts.map((x, k) => {
        const h = x.modo === 'cima' ? p.estilo.divisoria : height;
        const src = staticFile(x.arquivo);
        return (
          <Sequence key={k} from={Math.round(x.ini * fps)} durationInFrames={Math.round((x.fim - x.ini) * fps)}>
            <AbsoluteFill style={{height, backgroundColor: x.modo === 'cima' ? '#000' : undefined, top: 0}}>
              {x.modo === 'cima' && (
                <OffthreadVideo src={p.bruto} startFrom={Math.round(x.ini * fps)}
                  style={{position: 'absolute', top: h, width, height: height - h, objectFit: 'cover'}} />
              )}
              <div style={{position: 'absolute', top: 0, width, height: h, overflow: 'hidden'}}>
                {x.tipo === 'video'
                  ? <OffthreadVideo src={src} muted startFrom={Math.round((x.inicioMidia ?? 0) * fps)} style={{width, height: h, objectFit: 'cover'}} />
                  : <Img src={src} style={{width, height: h, objectFit: 'cover'}} />}
              </div>
            </AbsoluteFill>
          </Sequence>
        );
      })}
      <Legenda p={p} />
    </AbsoluteFill>
  );
};
