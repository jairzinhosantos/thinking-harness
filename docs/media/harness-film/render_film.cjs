/* Deterministic Canvas-to-H.264 render. Browser requests stay local. */
const path = require('node:path');
const fs = require('node:fs');
const {pathToFileURL} = require('node:url');
const {spawn} = require('node:child_process');
const {once} = require('node:events');
const {createRequire} = require('node:module');
const load = createRequire(require.resolve('@mermaid-js/mermaid-cli'));
const puppeteer = load('puppeteer');
const fps=24, seconds=45;
const previews=process.argv.includes('--previews');
const output=path.join(__dirname,'thinking-harness.mp4');
(async()=>{
  const browser=await puppeteer.launch({headless:true,executablePath:process.env.PUPPETEER_EXECUTABLE_PATH});
  let encoder;
  try {
    const page=await browser.newPage();
    await page.setViewport({width:1920,height:1080,deviceScaleFactor:1});
    await page.setRequestInterception(true);
    page.on('request',r=>/^(file:|data:|about:)/.test(r.url())?r.continue():r.abort());
    page.on('pageerror',e=>{throw e;});
    await page.goto(pathToFileURL(path.join(__dirname,'film.html')).href);
    await page.evaluate(()=>document.fonts.ready);
    if(previews){
      const folder=process.env.FILM_PREVIEW_DIR || '/tmp/thinking-harness-film-preview';
      fs.mkdirSync(folder,{recursive:true});
      for(const t of [0,3,7,10,13,16,20,23,26,30,33,36,38,39.8,43]) {
        await page.evaluate(t=>window.drawFrame(t),t);
        await page.screenshot({path:path.join(folder,`frame-${String(t).padStart(4,'0')}.png`),clip:{x:0,y:0,width:1920,height:1080}});
      }
      console.log(folder);return;
    }
    encoder=spawn('ffmpeg',['-y','-loglevel','warning','-f','image2pipe','-framerate',String(fps),'-vcodec','png','-i','pipe:0','-an','-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',output],{stdio:['pipe','inherit','inherit']});
    const finished=once(encoder,'close');
    let streamError;encoder.stdin.on('error',e=>{streamError=e;});
    for(let i=0;i<fps*seconds;i++) {
      if(streamError)throw streamError;
      const encoded=await page.evaluate(t=>{
        window.drawFrame(t);
        return document.querySelector('#film').toDataURL('image/png').split(',')[1];
      },i/fps);
      const png=Buffer.from(encoded,'base64');
      if(!encoder.stdin.write(png))await once(encoder.stdin,'drain');
      if(i===fps*10)fs.writeFileSync(path.join(__dirname,'poster.png'),png);
      if(i%(fps*5)===0)console.log(`Rendered ${i/fps}s / ${seconds}s`);
    }
    encoder.stdin.end();const [code]=await finished;
    if(code!==0)throw new Error(`ffmpeg exited with ${code}`);
    console.log(output);
  } finally {if(encoder && encoder.exitCode===null)encoder.kill();await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
