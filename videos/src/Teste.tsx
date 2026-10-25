import {AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
export const Teste = () => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig();
  const s = spring({frame: f, fps, config: {damping: 12}});
  return (
    <AbsoluteFill style={{background: '#5423CB', alignItems: 'center', justifyContent: 'center'}}>
      <div style={{fontFamily: 'sans-serif', fontWeight: 800, fontSize: 140, color: '#F3EEFF', transform: `scale(${s})`, opacity: interpolate(f, [0, 10], [0, 1])}}>ADULLAM</div>
    </AbsoluteFill>
  );
};
