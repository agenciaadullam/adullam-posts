import React from 'react';
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

// 01 — Trono vazio
const Cena1: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill style={{background: C.nevoa}}>
      <Grain />
      <Header n={1} />
      <div style={{position: 'absolute', left: 80, top: 300}}>
        <Up delay={2}><span style={{fontFamily: MONT, fontWeight: 600, fontSize: 28, letterSpacing: '0.24em', color: C.roxo}}>PASSADA A ELEIÇÃO</span></Up>
        <Slam delay={6} style={{transformOrigin: 'left center'}}><p style={{margin: '24px 0 0', fontFamily: MONT, fontWeight: 800, fontSize: 196, lineHeight: 0.86, letterSpacing: '-0.055em', color: C.preto}}>QUEM</p></Slam>
        <Slam delay={12} style={{transformOrigin: 'left center'}}><p style={{margin: 0, fontFamily: MONT, fontWeight: 800, fontSize: 196, lineHeight: 0.86, letterSpacing: '-0.055em', color: C.preto}}>GOVERNA</p></Slam>
        <div style={{marginTop: 36, position: 'relative', display: 'inline-block'}}>
          <div style={{position: 'absolute', inset: '0 0 0 0', background: C.roxo, transformOrigin: 'left', scale: `${interpolate(f, [20, 32], [0, 1], {...clamp, easing: ease})} 1`}} />
          <span style={{position: 'relative', display: 'block', padding: '6px 26px 16px', fontFamily: PF, fontStyle: 'italic', fontWeight: 700, fontSize: 92, color: C.nevoa, opacity: interpolate(f, [26, 32], [0, 1], clamp)}}>o seu Instagram?</span>
        </div>
      </div>
      <div style={{position: 'absolute', left: 520, top: 1060, width: 480, height: 600, borderRadius: '240px 240px 0 0', overflow: 'hidden', boxShadow: '0 30px 80px rgba(38,3,155,0.4)',
        translate: `0px ${interpolate(spring({frame: f - 24, fps, config: {damping: 18}}), [0, 1], [700, 0])}px`}}>
        <div style={{scale: String(interpolate(f, [24, 105], [1.15, 1], clamp))}}><Foto src="fotos/trono.jpg" w={480} h={600} /></div>
      </div>
      <div style={{position: 'absolute', left: 80, top: 1180, width: 400}}>
        <Up delay={40}><div style={{width: 70, height: 5, background: C.verm}} /></Up>
        <Up delay={44}><p style={{margin: '30px 0 0', fontFamily: MONT, fontWeight: 500, fontSize: 40, lineHeight: 1.35, color: C.preto}}>E o <b style={{color: C.roxo}}>trono do seu perfil</b> continua <b style={{color: C.roxo}}>vazio.</b></p></Up>
      </div>
    </AbsoluteFill>
  );
};

// 02 — Você discutiu
const Cena2: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const drop = spring({frame: f - 10, fps, config: {damping: 13}});
  return (
    <AbsoluteFill style={{background: C.roxo}}>
      <div style={{position: 'absolute', left: 380, top: 900, scale: String(interpolate(f, [4, 16], [0, 1], {...clamp, easing: ease}))}}><Star size={760} /></div>
      <div style={{position: 'absolute', left: 430, top: 860, padding: 16, background: C.nevoa, boxShadow: '0 26px 60px rgba(0,0,0,0.4)', rotate: `${interpolate(drop, [0, 1], [-14, 4])}deg`, translate: `0px ${interpolate(drop, [0, 1], [-1300, 0])}px`}}>
        <Foto src="fotos/rosto.jpg" w={520} h={680} tint={0} crop="50% 30%" />
      </div>
      <Grain dark />
      <Header dark n={2} />
      <div style={{position: 'absolute', left: 80, right: 80, top: 300}}>
        <Up><span style={{fontFamily: MONT, fontWeight: 600, fontSize: 28, letterSpacing: '0.24em', color: C.nevoa}}>VAMOS FALAR A REAL</span></Up>
        <Up delay={4}><p style={{margin: '28px 0 0', fontFamily: MONT, fontWeight: 800, fontSize: 104, lineHeight: 0.95, letterSpacing: '-0.045em', color: C.nevoa}}>VOCÊ DISCUTIU<br />O MÊS INTEIRO.</p></Up>
      </div>
      <div style={{position: 'absolute', left: 80, top: 900, width: 330}}>
        <Up delay={30}><p style={{margin: 0, fontFamily: PF, fontStyle: 'italic', fontSize: 50, lineHeight: 1.15, color: C.nevoa}}>No grupo, no comentário, no almoço de domingo.</p></Up>
        <Up delay={48}><p style={{margin: '40px 0 0', fontFamily: MONT, fontWeight: 600, fontSize: 38, lineHeight: 1.35, color: C.nevoa}}>E o perfil da empresa ficou <b style={{background: C.preto, padding: '0 10px'}}>sem governo.</b></p></Up>
      </div>
    </AbsoluteFill>
  );
};

// 03 — 21 dias (contador)
const Cena3: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const n = Math.round(interpolate(f, [4, 40], [0, 21], {...clamp, easing: Easing.out(Easing.cubic)}));
  const notif = spring({frame: f - 42, fps, config: {damping: 14}});
  return (
    <AbsoluteFill style={{background: C.preto}}>
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
        <Up delay={52}><p style={{margin: 0, fontFamily: MONT, fontWeight: 800, fontSize: 112, lineHeight: 0.95, letterSpacing: '-0.045em', color: C.nevoa}}>DIAS SEM<br /><span style={{fontFamily: PF, fontStyle: 'italic', fontWeight: 700, letterSpacing: '-0.02em'}}>ninguém no comando.</span></p></Up>
        <div style={{marginTop: 56, display: 'flex', flexWrap: 'wrap', gap: 16}}>
          {['Stories parados', 'Direct sem resposta', 'Cliente esperando'].map((t, i) => (
            <Up key={t} delay={66 + i * 6} dist={40}>
              <span style={{display: 'inline-block', fontFamily: MONT, fontWeight: 600, fontSize: 32, color: C.nevoa, padding: '12px 28px', borderRadius: 99, border: `2px solid ${i === 2 ? C.verm : 'rgba(243,238,255,0.6)'}`, background: i === 2 ? C.verm : 'transparent'}}>{t}</span>
            </Up>
          ))}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// 04 — O concorrente postou (círculo desenhado)
const Cena4: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const slide = spring({frame: f, fps, config: {damping: 16}});
  const draw = interpolate(f, [34, 52], [1, 0], {...clamp, easing: ease});
  return (
    <AbsoluteFill style={{background: C.branco}}>
      <Grain />
      <div style={{position: 'absolute', left: 110, top: 280, rotate: '-2deg', boxShadow: '0 26px 60px rgba(18,18,18,0.25)', translate: `${interpolate(slide, [0, 1], [-1200, 0])}px 0px`}}>
        <Foto src="fotos/loja.jpg" w={860} h={620} tint={0.4} />
        <span style={{position: 'absolute', left: 30, bottom: 30, background: C.verm, color: C.branco, fontFamily: MONT, fontWeight: 800, fontSize: 26, letterSpacing: '0.14em', padding: '12px 20px', borderRadius: 10, scale: String(interpolate(spring({frame: f - 18, fps, config: {damping: 9}}), [0, 1], [0, 1]))}}>● NOVO POST</span>
      </div>
      <Header n={4} />
      <div style={{position: 'absolute', left: 80, right: 80, top: 1020}}>
        <Up delay={14}><span style={{fontFamily: MONT, fontWeight: 600, fontSize: 28, letterSpacing: '0.24em', color: C.roxo}}>ENQUANTO VOCÊ DISCUTIA</span></Up>
        <Up delay={18}><p style={{margin: '24px 0 0', fontFamily: MONT, fontWeight: 800, fontSize: 94, lineHeight: 0.95, letterSpacing: '-0.045em', color: C.preto}}>O CONCORRENTE</p></Up>
        <Up delay={24}>
          <span style={{position: 'relative', display: 'inline-block', fontFamily: PF, fontStyle: 'italic', fontWeight: 700, fontSize: 180, lineHeight: 1.05, color: C.prof}}>
            postou.
            <svg width="640" height="230" viewBox="0 0 420 120" preserveAspectRatio="none" fill="none" style={{position: 'absolute', left: -50, top: -14}}>
              <path d="M215 9C110 4 12 22 9 60c-3 38 110 52 215 48 104-4 186-26 183-56-3-30-90-46-196-42" stroke={C.verm} strokeWidth="3.5" strokeLinecap="round" pathLength={1} strokeDasharray="1" strokeDashoffset={draw} />
            </svg>
          </span>
        </Up>
        <Up delay={58}><p style={{margin: '26px 0 0', fontFamily: PF, fontStyle: 'italic', fontSize: 46, lineHeight: 1.25, color: C.preto}}>E o cliente foi comprar com ele, sem perguntar em quem ele votou.</p></Up>
      </div>
    </AbsoluteFill>
  );
};

// 05 — Cédula
const Cena5: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const x = interpolate(f, [40, 52], [1, 0], {...clamp, easing: ease});
  const opts = ['Você', 'O algoritmo', 'A sorte'];
  return (
    <AbsoluteFill style={{background: C.nevoa}}>
      <Grain />
      <Header n={5} />
      <div style={{position: 'absolute', left: 80, right: 80, top: 300, textAlign: 'center'}}>
        <Up><span style={{fontFamily: MONT, fontWeight: 600, fontSize: 28, letterSpacing: '0.24em', color: C.roxo}}>A ÚNICA ELEIÇÃO QUE É SUA</span></Up>
        <Up delay={4}><p style={{margin: '26px 0 0', fontFamily: MONT, fontWeight: 800, fontSize: 82, lineHeight: 1.02, letterSpacing: '-0.035em', color: C.preto}}>Nas urnas, você tem <span style={{fontFamily: PF, fontStyle: 'italic', fontWeight: 700, color: C.roxo}}>um voto.</span></p></Up>
      </div>
      <div style={{position: 'absolute', left: 110, top: 640, width: 860, background: C.branco, border: `2px solid ${C.preto}`, padding: '48px 56px 44px', boxShadow: `16px 16px 0 ${C.prof}`,
        rotate: `${interpolate(spring({frame: f - 10, fps, config: {damping: 14}}), [0, 1], [-8, 1.5])}deg`, translate: `0px ${interpolate(spring({frame: f - 10, fps, config: {damping: 14}}), [0, 1], [1400, 0])}px`}}>
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
        <Up delay={56}><p style={{margin: 0, fontFamily: MONT, fontWeight: 800, fontSize: 62, lineHeight: 1.1, letterSpacing: '-0.03em', color: C.preto}}>No seu negócio, você decide <span style={{background: C.roxo, color: C.nevoa, padding: '0 18px 8px'}}>tudo.</span></p></Up>
      </div>
    </AbsoluteFill>
  );
};

// 06 — Plano de governo (checklist)
const Cena6: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const itens = ['1 post no feed', 'Stories todo dia', 'Direct respondido em 1h'];
  const paper = spring({frame: f, fps, config: {damping: 15}});
  return (
    <AbsoluteFill style={{background: C.prof}}>
      <Grain dark />
      <Header dark n={6} />
      <div style={{position: 'absolute', left: 100, top: 330, width: 880, height: 1100, background: C.nevoa, padding: '80px 70px 60px 130px', boxShadow: '0 30px 70px rgba(0,0,0,0.45)',
        backgroundImage: 'repeating-linear-gradient(180deg, transparent 0, transparent 89px, rgba(84,35,203,0.22) 89px, rgba(84,35,203,0.22) 91px)',
        rotate: `${interpolate(paper, [0, 1], [6, -2])}deg`, translate: `0px ${interpolate(paper, [0, 1], [1500, 0])}px`}}>
        <div style={{position: 'absolute', left: 96, top: 0, bottom: 0, width: 3, background: 'rgba(255,59,92,0.55)'}} />
        <span style={{fontFamily: MONT, fontWeight: 800, fontSize: 28, letterSpacing: '0.24em', color: C.roxo}}>PLANO DE GOVERNO</span>
        <p style={{margin: '20px 0 0', fontFamily: MONT, fontWeight: 800, fontSize: 92, lineHeight: 0.98, letterSpacing: '-0.04em', color: C.preto}}>PRA ESSA<br />SEMANA</p>
        <div style={{marginTop: 70, display: 'flex', flexDirection: 'column', gap: 46}}>
          {itens.map((t, i) => {
            const d = 26 + i * 16;
            return (
              <div key={t} style={{display: 'flex', alignItems: 'center', gap: 28, opacity: interpolate(f, [d - 8, d - 2], [0, 1], clamp)}}>
                <span style={{position: 'relative', width: 58, height: 58, border: `3px solid ${C.preto}`, borderRadius: 12, flex: 'none'}}>
                  <svg width="78" height="70" viewBox="0 0 64 58" fill="none" style={{position: 'absolute', left: -2, top: -20}}>
                    <path d="M8 32l14 14L58 6" stroke={C.verm} strokeWidth="7" strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray="1" strokeDashoffset={interpolate(f, [d, d + 8], [1, 0], clamp)} />
                  </svg>
                </span>
                <span style={{fontFamily: PF, fontStyle: 'italic', fontWeight: 700, fontSize: 52, color: C.preto, whiteSpace: 'nowrap'}}>{t}</span>
              </div>
            );
          })}
        </div>
      </div>
      <div style={{position: 'absolute', left: 430, top: 300, width: 240, height: 64, background: 'rgba(226,214,255,0.85)', rotate: '3deg', opacity: interpolate(f, [10, 14], [0, 1], clamp)}} />
      <div style={{position: 'absolute', left: 80, right: 80, top: 1530, textAlign: 'center'}}>
        <Up delay={80}><p style={{margin: 0, fontFamily: PF, fontStyle: 'italic', fontSize: 54, color: C.nevoa}}>(sem esperar a próxima eleição)</p></Up>
      </div>
    </AbsoluteFill>
  );
};

// 07 — Salva
const Cena7: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{background: C.preto}}>
      <Grain dark />
      <div style={{position: 'absolute', left: 80, right: 80, top: 380, display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center'}}>
        <Up><p style={{margin: 0, fontFamily: PF, fontStyle: 'italic', fontSize: 84, color: C.nevoa}}>A eleição acabou.</p></Up>
        <Up delay={8}><p style={{margin: '30px 0 0', fontFamily: MONT, fontWeight: 600, fontSize: 50, lineHeight: 1.25, color: 'rgba(243,238,255,0.85)'}}>O seu Instagram continua esperando você.</p></Up>
        <div style={{position: 'relative', marginTop: 90}}>
          <Slam delay={22}><p style={{margin: 0, fontFamily: MONT, fontWeight: 800, fontSize: 290, lineHeight: 0.85, letterSpacing: '-0.07em', color: C.roxo}}>SALVA.</p></Slam>
          <div style={{position: 'absolute', right: -60, top: -80, scale: String(interpolate(f, [28, 36], [0, 1], {...clamp, easing: ease}))}}><Star size={140} /></div>
        </div>
        <Up delay={40}><p style={{margin: '70px 0 0', maxWidth: 860, fontFamily: PF, fontStyle: 'italic', fontSize: 54, lineHeight: 1.25, color: C.nevoa}}>E manda pro amigo que passou o mês discutindo no grupo da família.</p></Up>
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 200, display: 'flex', justifyContent: 'center'}}>
        <Up delay={54}><Img src={staticFile('adullam-escura.png')} style={{width: 380}} /></Up>
      </div>
    </AbsoluteFill>
  );
};

// Corte com flash rápido entre cenas
const Flash: React.FC = () => {
  const f = useCurrentFrame();
  return <AbsoluteFill style={{background: C.nevoa, opacity: interpolate(f, [0, 4], [0.7, 0], clamp), pointerEvents: 'none'}} />;
};

export const CENAS = [105, 105, 120, 110, 105, 115, 120];
export const DURACAO = CENAS.reduce((a, b) => a + b, 0);

export const QuemGoverna: React.FC = () => {
  const lista = [Cena1, Cena2, Cena3, Cena4, Cena5, Cena6, Cena7];
  let from = 0;
  return (
    <AbsoluteFill style={{background: C.preto}}>
      <Fonts />
      {lista.map((Cena, i) => {
        const s = from;
        from += CENAS[i];
        return (
          <Sequence key={i} from={s} durationInFrames={CENAS[i]} name={`Cena ${i + 1}`}>
            <Cena />
            {i > 0 ? <Flash /> : null}
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
