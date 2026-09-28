// Optional PNG export / browser smoke check. Requires Playwright and Chrome.
// See concepts/software-factory/README.md for the reproducible commands.
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');

const directory = path.resolve(__dirname, '../concepts/software-factory');
const url = file => pathToFileURL(path.join(directory, file)).href;

(async () => {
  const browser = await chromium.launch(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE
    ? { executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE }
    : { channel: 'chrome' });
  try {
    const page = await browser.newPage({ viewport: { width: 1000, height: 700 }, deviceScaleFactor: 2 });
    const concepts = JSON.parse(fs.readFileSync(path.join(directory, 'concepts.json'), 'utf8'));
    for (const { slug } of concepts) {
      await page.goto(url(`${slug}.svg`));
      await page.evaluate(() => document.fonts.ready);
      assert(await page.evaluate(() => document.fonts.check('23px "Patrick Hand SC"')));
      await page.screenshot({ path: path.join(directory, `${slug}.png`) });
      console.log(`Exported ${slug}.png (2000 × 1400)`);
    }
    // Local brand fonts should keep the preview usable with no network.
    await page.route(/^https?:/, route => route.abort());
    await page.goto(url('index.html'));
    await page.evaluate(() => document.fonts.ready);
    for (const width of [1440, 768, 390]) {
      await page.setViewportSize({ width, height: 1000 });
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `Overflow at ${width}px`);
      assert(await page.locator('img').evaluateAll(images => images.every(img => img.complete && img.naturalWidth)), 'Broken image');
      for (const [label, view] of [['Just the drawings', 'art'], ['In a homepage', 'homepage']]) {
        await page.getByRole('button', { name: label }).click();
        assert.equal(await page.locator('body').getAttribute('data-view'), view);
        assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `Overflow in ${view} at ${width}px`);
      }
    }
    console.log('Preview passed at 1440, 768 and 390px; both view controls work.');
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
