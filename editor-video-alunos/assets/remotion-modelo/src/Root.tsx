import {Composition, staticFile} from 'remotion';
import {Video, type Props} from './Video';
import dados from '../public/edicao.json';

// Tudo que muda de um vídeo para outro fica em public/edicao.json (a skill escreve esse arquivo).
const d = dados as Props;

export const Root = () => (
  <Composition
    id="Video"
    component={Video}
    durationInFrames={Math.round(d.duracao * d.fps)}
    fps={d.fps}
    width={d.largura}
    height={d.altura}
    defaultProps={{...d, bruto: staticFile(d.bruto)}}
  />
);
