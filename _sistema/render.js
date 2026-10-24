// Uso: node _sistema/render.js <pasta-do-post>
// Gera um JPG 1080x1440 para cada slide-NN.html da pasta.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const dir = path.resolve(process.argv[2]);
  const slides = fs.readdirSync(dir).filter(f => /^slide-\d+\.html$/.test(f)).sort();
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1440 }, deviceScaleFactor: 1 });
  for (const f of slides) {
    await page.goto('file://' + path.join(dir, f));
    await page.evaluate(() => document.fonts.ready);
    const out = path.join(dir, f.replace('.html', '.jpg'));
    await page.screenshot({ path: out, type: 'jpeg', quality: 95, clip: { x: 0, y: 0, width: 1080, height: 1440 } });
    console.log('ok', path.basename(out));
  }
  await browser.close();
})();
