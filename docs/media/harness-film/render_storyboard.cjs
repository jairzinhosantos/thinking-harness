/* Render editable SVG keyframes as 1920 x 1080 PNGs without network access. */
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {createRequire} = require('node:module');
const load = createRequire(require.resolve('@mermaid-js/mermaid-cli'));
const puppeteer = load('puppeteer');
(async()=>{
  const browser=await puppeteer.launch({headless:true,executablePath:process.env.PUPPETEER_EXECUTABLE_PATH});
  try {
    const page=await browser.newPage();
    await page.setViewport({width:1920,height:1080,deviceScaleFactor:1});
    await page.setRequestInterception(true);
    page.on('request',r=>/^(file:|data:|about:)/.test(r.url())?r.continue():r.abort());
    for(const name of ['01-assembly','02-selection','03-recursion']){
      await page.goto(pathToFileURL(path.join(__dirname,name+'.svg')).href);
      await page.evaluate(()=>document.fonts.ready);
      await page.screenshot({path:path.join(__dirname,name+'.png')});
      console.log(name+'.png');
    }
  } finally {await browser.close();}
})();
