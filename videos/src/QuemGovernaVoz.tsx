import React from 'react';
import {Audio} from '@remotion/media';
import DUR from './duracoes.json';
import {AbsoluteFill, Easing, Img, interpolate, Sequence, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';

// Reels "Quem governa o seu Instagram?" — versão em vídeo do carrossel de 26/10
const C = {roxo: '#5423CB', prof: '#26039B', preto: '#121212', nevoa: '#F3EEFF', lilas: '#E2D6FF', branco: '#FFFFFF', verm: '#FF3B5C'};
const MONT = 'Montserrat, sans-serif';
const PF = "'Playfair Display', Georgia, serif";
const ease = Easing.bezier(0.16, 1, 0.3, 1);
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

const Fonts: React.FC = () => {
  const ff = (fam: string, w: number, st: string, file: string) =>
    `@font-face{font-family:'${fam}';font-weight:${w};font-style:${st};src:url(${staticFile('fonts/' + file)})}`;
  return (
    <style>
      {[
        ff('Montserrat', 500, 'normal', 'montserrat-latin-500-normal.woff2'),
        ff('Montserrat', 600, 'normal', 'montserrat-latin-600-normal.woff2'),
        ff('Montserrat', 800, 'normal', 'montserrat-latin-800-normal.woff2'),
        ff('Playfair Display', 400, 'italic', 'playfair-display-latin-400-italic.woff2'),
        ff('Playfair Display', 700, 'italic', 'playfair-display-latin-700-italic.woff2'),
        ff('Space Mono', 700, 'normal', 'space-mono-latin-700-normal.woff2'),
      ].join('')}
    </style>
  );
};

const Grain: React.FC<{dark?: boolean}> = ({dark}) => {
  const f = useCurrentFrame();
  return (
    <svg width="1080" height="1920" style={{position: 'absolute', inset: 0, opacity: dark ? 0.18 : 0.22, mixBlendMode: dark ? 'overlay' : 'multiply', pointerEvents: 'none'}}>
      <filter id={`g${dark ? 'd' : 'l'}`}>
        <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={2} seed={f % 8} stitchTiles="stitch" />
        <feColorMatrix type="saturate" values="0" />
      </filter>
      <rect width="1080" height="1920" filter={`url(#g${dark ? 'd' : 'l'})`} />
    </svg>
  );
};

// Entrada com mola (sobe + aparece)
const Up: React.FC<{delay?: number; children: React.ReactNode; dist?: number; style?: React.CSSProperties}> = ({delay = 0, children, dist = 80, style}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame: f - delay, fps, config: {damping: 16, mass: 0.7}});
  return <div style={{...style, opacity: interpolate(f - delay, [0, 6], [0, 1], clamp), translate: `0px ${(1 - s) * dist}px`}}>{children}</div>;
};

const Slam: React.FC<{delay?: number; children: React.ReactNode; style?: React.CSSProperties}> = ({delay = 0, children, style}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const s = spring({frame: f - delay, fps, config: {damping: 11, stiffness: 180}});
  return <div style={{...style, opacity: f >= delay ? 1 : 0, scale: String(interpolate(s, [0, 1], [1.9, 1]))}}>{children}</div>;
};

const Header: React.FC<{dark?: boolean; n: number}> = ({dark, n}) => (
  <div style={{position: 'absolute', top: 120, left: 80, right: 80, display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
    <Img src={staticFile(dark ? 'adullam-escura.png' : 'adullam-clara.png')} style={{height: 60}} />
    <span style={{fontFamily: MONT, fontWeight: 600, fontSize: 26, letterSpacing: '0.14em', color: dark ? C.nevoa : C.preto}}>{String(n).padStart(2, '0')}/07</span>
  </div>
);

const Foto: React.FC<{src: string; w: number; h: number; tint?: number; crop?: string}> = ({src, w, h, tint = 0.35, crop = '50% 50%'}) => (
  <div style={{position: 'relative', width: w, height: h, overflow: 'hidden', background: C.preto}}>
    <Img src={staticFile(src)} style={{width: w, height: h, objectFit: 'cover', objectPosition: crop, filter: 'grayscale(1) contrast(1.3)'}} />
    <div style={{position: 'absolute', inset: 0, backgroundImage: 'radial-gradient(rgba(18,18,18,0.5) 1.4px, transparent 1.8px)', backgroundSize: '8px 8px', mixBlendMode: 'multiply'}} />
    <div style={{position: 'absolute', inset: 0, background: `rgba(84,35,203,${tint})`, mixBlendMode: 'multiply'}} />
  </div>
);

const Star: React.FC<{size: number; color?: string}> = ({size, color = C.verm}) => {
  const f = useCurrentFrame();
  return (
    <svg width={size} height={size} viewBox="0 0 200 200" style={{rotate: `${f * 0.6}deg`}}>
      <polygon points="100,4 116,62 176,30 140,84 196,104 136,120 168,178 112,142 100,198 86,142 30,176 62,120 4,100 62,84 26,28 84,62" fill={color} />
    </svg>
  );
};


// ===== Linha do tempo guiada pela narração =====

const FPS = 30;
const LEAD = 10; // respiro no início de cada cena (frames)
const GAP = 9; // pausa entre falas
const TAIL = 20; // respiro no fim da cena
const ROTEIRO: string[][] = [
  ['c1a', 'c1b', 'c1c'],
  ['c2a', 'c2b', 'c2c'],
  ['c3a', 'c3b', 'c3c'],
  ['c4a', 'c4b', 'c4c'],
  ['c5a', 'c5b', 'c5c', 'c5d'],
  ['c6a', 'c6b', 'c6c', 'c6d', 'c6e'],
  ['c7a', 'c7b', 'c7c', 'c7d'],
];
const d = (id: string) => Math.ceil((DUR as Record<string, number>)[id] * FPS);
type Tempo = {t: number[]; dur: number[]; total: number};
const TEMPOS: Tempo[] = ROTEIRO.map((falas) => {
  const t: number[] = [];
  let cur = LEAD;
  falas.forEach((id) => {
    t.push(cur);
    cur += d(id) + GAP;
  });
  return {t, dur: falas.map(d), total: cur - GAP + TAIL};
});
export const DURACAO_VOZ = TEMPOS.reduce((a, b) => a + b.total, 0);

const Sfx: React.FC<{src: string; at: number; vol?: number}> = ({src, at, vol = 0.5}) => (
  <Sequence from={Math.max(0, Math.round(at))} durationInFrames={90} layout="none">
    <Audio src={staticFile('sfx/' + src)} volume={vol} />
  </Sequence>
);

type P = {t: number[]; dur: number[]};

// 01 — Trono vazio
const V1: React.FC<P> = ({t, dur}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const q = t[1];
  return (
    <AbsoluteFill style={{background: C.nevoa}}>
      <Sfx src="whip.wav" at={q} vol={0.35} />
      <Sfx src="whip.wav" at={q + 9} vol={0.35} />
      <Sfx src="switch.wav" at={q + 18} vol={0.5} />
      <Sfx src="whoosh.wav" at={t[2] - 12} vol={0.45} />
      <Grain />
      <Header n={1} />
      <div style={{position: 'absolute', left: 80, top: 300}}>
        <Up delay={t[0]}><span style={{fontFamily: MONT, fontWeight: 600, fontSize: 28, letterSpacing: '0.24em', color: C.roxo}}>PASSADA A ELEIÇÃO</span></Up>
        <Slam delay={q} style={{transformOrigin: 'left center'}}><p style={{margin: '24px 0 0', fontFamily: MONT, fontWeight: 800, fontSize: 196, lineHeight: 0.86, letterSpacing: '-0.055em', color: C.preto}}>QUEM</p></Slam>
        <Slam delay={q + 9} style={{transformOrigin: 'left center'}}><p style={{margin: 0, fontFamily: MONT, fontWeight: 800, fontSize: 196, lineHeight: 0.86, letterSpacing: '-0.055em', color: C.preto}}>GOVERNA</p></Slam>
        <div style={{marginTop: 36, position: 'relative', display: 'inline-block'}}>
          <div style={{position: 'absolute', inset: 0, background: C.roxo, transformOrigin: 'left', scale: `${interpolate(f, [q + 18, q + 30], [0, 1], {...clamp, easing: ease})} 1`}} />
          <span style={{position: 'relative', display: 'block', padding: '6px 26px 16px', fontFamily: PF, fontStyle: 'italic', fontWeight: 700, fontSize: 92, color: C.nevoa, opacity: interpolate(f, [q + 24, q + 30], [0, 1], clamp)}}>o seu Instagram?</span>
        </div>
      </div>
      <div style={{position: 'absolute', left: 520, top: 1060, width: 480, height: 600, borderRadius: '240px 240px 0 0', overflow: 'hidden', boxShadow: '0 30px 80px rgba(38,3,155,0.4)',
        translate: `0px ${interpolate(spring({frame: f - (t[2] - 12), fps, config: {damping: 18}}), [0, 1], [700, 0])}px`}}>
        <div style={{scale: String(interpolate(f, [t[2] - 12, t[2] + dur[2] + 20], [1.15, 1], clamp))}}><Foto src="fotos/trono.jpg" w={480} h={600} /></div>
      </div>
      <div style={{position: 'absolute', left: 80, top: 1180, width: 400}}>
        <Up delay={t[2]}><div style={{width: 70, height: 5, background: C.verm}} /></Up>
        <Up delay={t[2] + 4}><p style={{margin: '30px 0 0', fontFamily: MONT, fontWeight: 500, fontSize: 40, lineHeight: 1.35, color: C.preto}}>E o <b style={{color: C.roxo}}>trono do seu perfil</b> continua <b style={{color: C.roxo}}>vazio.</b></p></Up>
      </div>
    </AbsoluteFill>
  );
};

// 02 — Você discutiu
const V2: React.FC<P> = ({t}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const dropAt = t[1] - 14;
  const drop = spring({frame: f - dropAt, fps, config: {damping: 13}});
  return (
    <AbsoluteFill style={{background: C.roxo}}>
      <Sfx src="switch.wav" at={dropAt - 8} vol={0.4} />
      <Sfx src="whoosh.wav" at={dropAt - 4} vol={0.45} />
      <Sfx src="page-turn.wav" at={dropAt + 10} vol={0.6} />
      <Sfx src="click.wav" at={t[2] + 30} vol={0.4} />
      <div style={{position: 'absolute', left: 380, top: 900, scale: String(interpolate(f, [dropAt - 8, dropAt + 4], [0, 1], {...clamp, easing: ease}))}}><Star size={760} /></div>
      <div style={{position: 'absolute', left: 430, top: 860, padding: 16, background: C.nevoa, boxShadow: '0 26px 60px rgba(0,0,0,0.4)', rotate: `${interpolate(drop, [0, 1], [-14, 4])}deg`, translate: `0px ${interpolate(drop, [0, 1], [-1300, 0])}px`}}>
        <Foto src="fotos/rosto.jpg" w={520} h={680} tint={0} crop="50% 30%" />
      </div>
      <Grain dark />
      <Header dark n={2} />
      <div style={{position: 'absolute', left: 80, right: 80, top: 300}}>
        <Up delay={t[0]}><span style={{fontFamily: MONT, fontWeight: 600, fontSize: 28, letterSpacing: '0.24em', color: C.nevoa}}>VAMOS FALAR A REAL</span></Up>
        <Up delay={t[0] + 30}><p style={{margin: '28px 0 0', fontFamily: MONT, fontWeight: 800, fontSize: 104, lineHeight: 0.95, letterSpacing: '-0.045em', color: C.nevoa}}>VOCÊ DISCUTIU<br />O MÊS INTEIRO.</p></Up>
      </div>
      <div style={{position: 'absolute', left: 80, top: 900, width: 330}}>
        <Up delay={t[1]}><p style={{margin: 0, fontFamily: PF, fontStyle: 'italic', fontSize: 50, lineHeight: 1.15, color: C.nevoa}}>No grupo, no comentário, no almoço de domingo.</p></Up>
        <Up delay={t[2]}><p style={{margin: '40px 0 0', fontFamily: MONT, fontWeight: 600, fontSize: 38, lineHeight: 1.35, color: C.nevoa}}>E o perfil da empresa ficou <b style={{background: C.preto, padding: '0 10px'}}>sem governo.</b></p></Up>
      </div>
    </AbsoluteFill>
  );
};

// 03 — 21 dias
const V3: React.FC<P> = ({t, dur}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const c0 = t[0], c1 = t[0] + dur[0];
  const n = Math.round(interpolate(f, [c0, c1], [0, 21], {...clamp, easing: Easing.out(Easing.cubic)}));
  const notif = spring({frame: f - t[1], fps, config: {damping: 14}});
  const ninguem = t[1] + Math.round(dur[1] * 0.62);
  const chips = [t[2], t[2] + Math.round(dur[2] * 0.3), t[2] + Math.round(dur[2] * 0.62)];
  const ticks: number[] = [];
  for (let k = 1; k <= 21; k++) {
    const p = 1 - Math.cbrt(1 - k / 21);
    ticks.push(c0 + p * (c1 - c0));
  }
  return (
    <AbsoluteFill style={{background: C.preto}}>
      {ticks.map((at, i) => <Sfx key={i} src="click.wav" at={at} vol={0.18} />)}
      <Sfx src="notificacao.wav" at={t[1] + 2} vol={0.55} />
      {chips.map((at, i) => <Sfx key={'c' + i} src={i === 2 ? 'ding.wav' : 'switch.wav'} at={at} vol={i === 2 ? 0.35 : 0.4} />)}
      <Grain dark />
      <Header dark n={3} />
      <span style={{position: 'absolute', left: 80, top: 300, fontFamily: MONT, fontWeight: 600, fontSize: 28, letterSpacing: '0.24em', color: C.nevoa}}>O MANDATO QUE NINGUÉM ASSUMIU</span>
      <p style={{position: 'absolute', left: 50, top: 330, margin: 0, fontFamily: MONT, fontWeight: 800, fontSize: 720, lineHeight: 1, letterSpacing: '-0.07em', color: 'transparent', WebkitTextStroke: `5px ${C.roxo}`}}>{n}</p>
      <div style={{position: 'absolute', left: 300, top: 560, width: 700, display: 'flex', alignItems: 'center', gap: 26, background: 'rgba(243,238,255,0.97)', borderRadius: 32, padding: '30px 34px', boxShadow: '0 24px 60px rgba(0,0,0,0.5)',
        rotate: '-3deg', translate: `${interpolate(notif, [0, 1], [1100, 0])}px 0px`}}>
        <div style={{width: 84, height: 84, borderRadius: 22, background: C.prof, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
          <svg width="46" height="46" viewBox="0 0 24 24" fill="none" stroke={C.nevoa} strokeWidth="2"><rect x="3" y="3" width="18" height="18" rx="5" /><circle cx="12" cy="12" r="4" /></svg>
        </div>
        <div>
          <div style={{fontFamily: MONT, fontWeight: 600, fontSize: 22, letterSpacing: '0.08em', color: 'rgba(18,18,18,0.55)'}}>SEU PERFIL · AGORA</div>
          <div style={{fontFamily: MONT, fontWeight: 800, fontSize: 38, color: C.preto}}>Último post: há 21 dias</div>
        </div>
        <span style={{marginLeft: 'auto', width: 22, height: 22, borderRadius: 99, background: C.verm, opacity: f % 20 < 10 ? 1 : 0.3}} />
      </div>
      <div style={{position: 'absolute', left: 80, right: 80, top: 1150}}>
        <Up delay={ninguem}><p style={{margin: 0, fontFamily: MONT, fontWeight: 800, fontSize: 112, lineHeight: 0.95, letterSpacing: '-0.045em', color: C.nevoa}}>DIAS SEM<br /><span style={{fontFamily: PF, fontStyle: 'italic', fontWeight: 700, letterSpacing: '-0.02em'}}>ninguém no comando.</span></p></Up>
        <div style={{marginTop: 56, display: 'flex', flexWrap: 'wrap', gap: 16}}>
          {['Stories parados', 'Direct sem resposta', 'Cliente esperando'].map((tx, i) => (
            <Up key={tx} delay={chips[i]} dist={40}>
              <span style={{display: 'inline-block', fontFamily: MONT, fontWeight: 600, fontSize: 32, color: C.nevoa, padding: '12px 28px', borderRadius: 99, border: `2px solid ${i === 2 ? C.verm : 'rgba(243,238,255,0.6)'}`, background: i === 2 ? C.verm : 'transparent'}}>{tx}</span>
            </Up>
          ))}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 04 — O concorrente postou
const V4: React.FC<P> = ({t}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const slide = spring({frame: f - t[0], fps, config: {damping: 16}});
  const p = t[1];
  const draw = interpolate(f, [p + 8, p + 26], [1, 0], {...clamp, easing: ease});
  return (
    <AbsoluteFill style={{background: C.branco}}>
      <Sfx src="whoosh.wav" at={t[0] - 4} vol={0.45} />
      <Sfx src="scratch.wav" at={p - 6} vol={0.3} />
      <Sfx src="ding.wav" at={p + 2} vol={0.4} />
      <Grain />
      <div style={{position: 'absolute', left: 110, top: 280, rotate: '-2deg', boxShadow: '0 26px 60px rgba(18,18,18,0.25)', translate: `${interpolate(slide, [0, 1], [-1200, 0])}px 0px`}}>
        <Foto src="fotos/loja.jpg" w={860} h={620} tint={0.4} />
        <span style={{position: 'absolute', left: 30, bottom: 30, background: C.verm, color: C.branco, fontFamily: MONT, fontWeight: 800, fontSize: 26, letterSpacing: '0.14em', padding: '12px 20px', borderRadius: 10, scale: String(interpolate(spring({frame: f - p, fps, config: {damping: 9}}), [0, 1], [0, 1]))}}>● NOVO POST</span>
      </div>
      <Header n={4} />
      <div style={{position: 'absolute', left: 80, right: 80, top: 1020}}>
        <Up delay={t[0] + 6}><span style={{fontFamily: MONT, fontWeight: 600, fontSize: 28, letterSpacing: '0.24em', color: C.roxo}}>ENQUANTO VOCÊ DISCUTIA</span></Up>
        <Up delay={p - 4}><p style={{margin: '24px 0 0', fontFamily: MONT, fontWeight: 800, fontSize: 94, lineHeight: 0.95, letterSpacing: '-0.045em', color: C.preto}}>O CONCORRENTE</p></Up>
        <Up delay={p + 4}>
          <span style={{position: 'relative', display: 'inline-block', fontFamily: PF, fontStyle: 'italic', fontWeight: 700, fontSize: 180, lineHeight: 1.05, color: C.prof}}>
            postou.
            <svg width="640" height="230" viewBox="0 0 420 120" preserveAspectRatio="none" fill="none" style={{position: 'absolute', left: -50, top: -14}}>
              <path d="M215 9C110 4 12 22 9 60c-3 38 110 52 215 48 104-4 186-26 183-56-3-30-90-46-196-42" stroke={C.verm} strokeWidth="3.5" strokeLinecap="round" pathLength={1} strokeDasharray="1" strokeDashoffset={draw} />
            </svg>
          </span>
        </Up>
        <Up delay={t[2]}><p style={{margin: '26px 0 0', fontFamily: PF, fontStyle: 'italic', fontSize: 46, lineHeight: 1.25, color: C.preto}}>E o cliente foi comprar com ele, sem perguntar em quem ele votou.</p></Up>
      </div>
    </AbsoluteFill>
  );
};

// 05 — Cédula
const V5: React.FC<P> = ({t}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const up = spring({frame: f - (t[1] - 8), fps, config: {damping: 14}});
  const x = interpolate(f, [t[2], t[2] + 10], [1, 0], {...clamp, easing: ease});
  const opts = ['Você', 'O algoritmo', 'A sorte'];
  return (
    <AbsoluteFill style={{background: C.nevoa}}>
      <Sfx src="page-turn.wav" at={t[1] - 8} vol={0.6} />
      <Sfx src="click.wav" at={t[2]} vol={0.5} />
      <Sfx src="click.wav" at={t[2] + 5} vol={0.5} />
      <Sfx src="boom.wav" at={t[3] + Math.round(55)} vol={0.22} />
      <Grain />
      <Header n={5} />
      <div style={{position: 'absolute', left: 80, right: 80, top: 300, textAlign: 'center'}}>
        <Up delay={t[0]}><span style={{fontFamily: MONT, fontWeight: 600, fontSize: 28, letterSpacing: '0.24em', color: C.roxo}}>A ÚNICA ELEIÇÃO QUE É SUA</span></Up>
        <Up delay={t[0] + 4}><p style={{margin: '26px 0 0', fontFamily: MONT, fontWeight: 800, fontSize: 82, lineHeight: 1.02, letterSpacing: '-0.035em', color: C.preto}}>Nas urnas, você tem <span style={{fontFamily: PF, fontStyle: 'italic', fontWeight: 700, color: C.roxo}}>um voto.</span></p></Up>
      </div>
      <div style={{position: 'absolute', left: 110, top: 640, width: 860, background: C.branco, border: `2px solid ${C.preto}`, padding: '48px 56px 44px', boxShadow: `16px 16px 0 ${C.prof}`,
        rotate: `${interpolate(up, [0, 1], [-8, 1.5])}deg`, translate: `0px ${interpolate(up, [0, 1], [1400, 0])}px`}}>
        <div style={{display: 'flex', justifyContent: 'space-between', paddingBottom: 22, borderBottom: '2px dashed rgba(18,18,18,0.35)', fontFamily: MONT, fontWeight: 800, fontSize: 26, letterSpacing: '0.2em'}}>
          <span>CÉDULA DO SEU NEGÓCIO</span><span style={{color: 'rgba(18,18,18,0.5)', fontWeight: 600}}>Nº 001</span>
        </div>
        <p style={{margin: '32px 0 8px', fontFamily: PF, fontStyle: 'italic', fontSize: 46}}>Quem decide o que a empresa posta?</p>
        {opts.map((o, i) => (
          <div key={o} style={{display: 'flex', alignItems: 'center', gap: 28, padding: '26px 0', borderBottom: i < 2 ? '1px solid rgba(18,18,18,0.12)' : 'none'}}>
            <span style={{position: 'relative', width: 60, height: 60, border: `3px solid ${C.preto}`}}>
              {i === 0 ? (
                <svg width="84" height="84" viewBox="0 0 70 70" fill="none" style={{position: 'absolute', left: -14, top: -16}}>
                  <path d="M10 12l50 46M58 10L12 60" stroke={C.verm} strokeWidth="7" strokeLinecap="round" pathLength={1} strokeDasharray="1" strokeDashoffset={x} />
                </svg>
              ) : null}
            </span>
            <span style={{fontFamily: MONT, fontWeight: i === 0 ? 800 : 500, fontSize: i === 0 ? 52 : 46, color: i === 0 ? C.preto : 'rgba(18,18,18,0.55)'}}>{o}</span>
          </div>
        ))}
      </div>
      <div style={{position: 'absolute', left: 80, right: 80, top: 1440, textAlign: 'center'}}>
        <Up delay={t[3]}><p style={{margin: 0, fontFamily: MONT, fontWeight: 800, fontSize: 62, lineHeight: 1.1, letterSpacing: '-0.03em', color: C.preto}}>No seu negócio, você decide <span style={{background: C.roxo, color: C.nevoa, padding: '0 18px 8px'}}>tudo.</span></p></Up>
      </div>
    </AbsoluteFill>
  );
};

// 06 — Plano de governo
const V6: React.FC<P> = ({t}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const itens = ['1 post no feed', 'Stories todo dia', 'Direct respondido em 1h'];
  const paper = spring({frame: f - (t[0] - 6), fps, config: {damping: 15}});
  return (
    <AbsoluteFill style={{background: C.prof}}>
      <Sfx src="page-turn.wav" at={t[0] - 6} vol={0.65} />
      <Sfx src="switch.wav" at={t[0] + 10} vol={0.3} />
      {[t[1], t[2], t[3]].map((at, i) => <Sfx key={i} src="click.wav" at={at + 4} vol={0.55} />)}
      <Sfx src="ding.wav" at={t[3] + 30} vol={0.35} />
      <Grain dark />
      <Header dark n={6} />
      <div style={{position: 'absolute', left: 100, top: 330, width: 880, height: 1100, background: C.nevoa, padding: '80px 70px 60px 130px', boxShadow: '0 30px 70px rgba(0,0,0,0.45)',
        backgroundImage: 'repeating-linear-gradient(180deg, transparent 0, transparent 89px, rgba(84,35,203,0.22) 89px, rgba(84,35,203,0.22) 91px)',
        rotate: `${interpolate(paper, [0, 1], [6, -2])}deg`, translate: `0px ${interpolate(paper, [0, 1], [1500, 0])}px`}}>
        <div style={{position: 'absolute', left: 96, top: 0, bottom: 0, width: 3, background: 'rgba(255,59,92,0.55)'}} />
        <span style={{fontFamily: MONT, fontWeight: 800, fontSize: 28, letterSpacing: '0.24em', color: C.roxo}}>PLANO DE GOVERNO</span>
        <p style={{margin: '20px 0 0', fontFamily: MONT, fontWeight: 800, fontSize: 92, lineHeight: 0.98, letterSpacing: '-0.04em', color: C.preto}}>PRA ESSA<br />SEMANA</p>
        <div style={{marginTop: 70, display: 'flex', flexDirection: 'column', gap: 46}}>
          {itens.map((tx, i) => {
            const dl = t[i + 1];
            return (
              <div key={tx} style={{display: 'flex', alignItems: 'center', gap: 28, opacity: interpolate(f, [dl - 6, dl], [0, 1], clamp), translate: `${interpolate(f, [dl - 6, dl + 2], [-30, 0], {...clamp, easing: ease})}px 0px`}}>
                <span style={{position: 'relative', width: 58, height: 58, border: `3px solid ${C.preto}`, borderRadius: 12, flex: 'none'}}>
                  <svg width="78" height="70" viewBox="0 0 64 58" fill="none" style={{position: 'absolute', left: -2, top: -20}}>
                    <path d="M8 32l14 14L58 6" stroke={C.verm} strokeWidth="7" strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray="1" strokeDashoffset={interpolate(f, [dl + 4, dl + 12], [1, 0], clamp)} />
                  </svg>
                </span>
                <span style={{fontFamily: PF, fontStyle: 'italic', fontWeight: 700, fontSize: 52, color: C.preto, whiteSpace: 'nowrap'}}>{tx}</span>
              </div>
            );
          })}
        </div>
      </div>
      <div style={{position: 'absolute', left: 430, top: 300, width: 240, height: 64, background: 'rgba(226,214,255,0.85)', rotate: '3deg', opacity: interpolate(f, [t[0] + 8, t[0] + 12], [0, 1], clamp)}} />
      <div style={{position: 'absolute', left: 80, right: 80, top: 1530, textAlign: 'center'}}>
        <Up delay={t[4]}><p style={{margin: 0, fontFamily: PF, fontStyle: 'italic', fontSize: 54, color: C.nevoa}}>(sem esperar a próxima eleição)</p></Up>
      </div>
    </AbsoluteFill>
  );
};

// 07 — Salva
const V7: React.FC<P> = ({t}) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{background: C.preto}}>
      <Sfx src="boom.wav" at={t[2]} vol={0.35} />
      <Sfx src="ding.wav" at={t[2] + 8} vol={0.35} />
      <Sfx src="whoosh.wav" at={t[3] + 60} vol={0.3} />
      <Sfx src="shutter.wav" at={t[3] + 72} vol={0.35} />
      <Grain dark />
      <div style={{position: 'absolute', left: 80, right: 80, top: 380, display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center'}}>
        <Up delay={t[0]}><p style={{margin: 0, fontFamily: PF, fontStyle: 'italic', fontSize: 84, color: C.nevoa}}>A eleição acabou.</p></Up>
        <Up delay={t[1]}><p style={{margin: '30px 0 0', fontFamily: MONT, fontWeight: 600, fontSize: 50, lineHeight: 1.25, color: 'rgba(243,238,255,0.85)'}}>O seu Instagram continua esperando você.</p></Up>
        <div style={{position: 'relative', marginTop: 90}}>
          <Slam delay={t[2]}><p style={{margin: 0, fontFamily: MONT, fontWeight: 800, fontSize: 290, lineHeight: 0.85, letterSpacing: '-0.07em', color: C.roxo}}>SALVA.</p></Slam>
          <div style={{position: 'absolute', right: -60, top: -80, scale: String(interpolate(f, [t[2] + 6, t[2] + 14], [0, 1], {...clamp, easing: ease}))}}><Star size={140} /></div>
        </div>
        <Up delay={t[3]}><p style={{margin: '70px 0 0', maxWidth: 860, fontFamily: PF, fontStyle: 'italic', fontSize: 54, lineHeight: 1.25, color: C.nevoa}}>E manda pro amigo que passou o mês discutindo no grupo da família.</p></Up>
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 200, display: 'flex', justifyContent: 'center'}}>
        <Up delay={t[3] + 66}><Img src={staticFile('adullam-escura.png')} style={{width: 380}} /></Up>
      </div>
    </AbsoluteFill>
  );
};

const FlashV: React.FC = () => {
  const f = useCurrentFrame();
  return <AbsoluteFill style={{background: C.nevoa, opacity: interpolate(f, [0, 4], [0.7, 0], clamp), pointerEvents: 'none'}} />;
};

export const QuemGovernaVoz: React.FC = () => {
  const lista = [V1, V2, V3, V4, V5, V6, V7];
  let from = 0;
  return (
    <AbsoluteFill style={{background: C.preto}}>
      <Fonts />
      {lista.map((Cena, i) => {
        const s = from;
        const tm = TEMPOS[i];
        from += tm.total;
        return (
          <Sequence key={i} from={s} durationInFrames={tm.total} name={`Cena ${i + 1}`}>
            <Cena t={tm.t} dur={tm.dur} />
            {ROTEIRO[i].map((id, j) => (
              <Sequence key={id} from={tm.t[j]} durationInFrames={tm.dur[j] + 6} name={`Voz ${id}`} layout="none">
                <Audio src={staticFile(`voz/${id}.wav`)} volume={1} />
              </Sequence>
            ))}
            {i > 0 ? <FlashV /> : null}
            {i > 0 ? <Sfx src="whip.wav" at={0} vol={0.22} /> : null}
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
