// Uso: node _sistema/render-video.js <pasta-do-post> [--quadros 0,2.5,7] [--saida <pasta>]
// Grava <pasta>/video.mp4 (H.264, 1080x1920) a partir de <pasta>/animacao.html, quadro a quadro.
// A página expõe FPS, DUR, pronto (Promise) e desenhar(t). Com --quadros, salva só esses instantes em PNG.
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

(async () => {
  const dir = path.resolve(process.argv[2]);
  const arg = n => { const i = process.argv.indexOf(n); return i > 0 ? process.argv[i + 1] : null; };
  const quadros = arg('--quadros');
  const saida = path.resolve(arg('--saida') || dir);

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  page.on('pageerror', e => { console.error(e); process.exit(1); });
  await page.goto('file://' + path.join(dir, 'animacao.html') + '?render');
  await page.evaluate(() => window.pronto);
  const { fps, dur } = await page.evaluate(() => ({ fps: window.FPS, dur: window.DUR }));
  const frame = t => page.evaluate(t => { desenhar(t); return document.getElementById('c').toDataURL('image/png').slice(22); }, t)
    .then(b64 => Buffer.from(b64, 'base64'));

  if (quadros) {
    fs.mkdirSync(saida, { recursive: true });
    for (const t of quadros.split(',').map(Number)) {
      const out = path.join(saida, `quadro-${t.toFixed(2)}.png`);
      fs.writeFileSync(out, await frame(t));
      console.log('ok', path.basename(out));
    }
  } else {
    const out = path.join(saida, 'video.mp4');
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-',
      '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out],
      { stdio: ['pipe', 'inherit', 'inherit'] });
    const n = Math.round(fps * dur);
    for (let i = 0; i < n; i++) {
      if (!ff.stdin.write(await frame(i / fps))) await new Promise(r => ff.stdin.once('drain', r));
      if (i % fps === 0) process.stdout.write(`\r${i}/${n} quadros`);
    }
    ff.stdin.end();
    await new Promise((res, rej) => ff.on('close', c => c ? rej(new Error('ffmpeg ' + c)) : res()));
    console.log(`\rok ${path.relative(process.cwd(), out)} (${n} quadros)`);
  }
  await browser.close();
})();
