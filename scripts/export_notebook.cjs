/* Print an nbconvert HTML export as a reading copy, without executing notebook code. */
const {pathToFileURL} = require('node:url');
const path = require('node:path');
const {createRequire} = require('node:module');
const load = createRequire(require.resolve('@mermaid-js/mermaid-cli'));
const puppeteer = load('puppeteer');

(async () => {
  const [input, output, baseUrl] = process.argv.slice(2);
  if (!input || !output || !baseUrl?.startsWith('https://github.com/')) {
    throw new Error('Expected HTML input, PDF output and GitHub case-folder URL');
  }
  const browser = await puppeteer.launch({headless: true, executablePath: process.env.PUPPETEER_EXECUTABLE_PATH});
  try {
    const page = await browser.newPage();
    await page.setRequestInterception(true);
    page.on('request', request => /^(file:|data:|about:)/.test(request.url()) ? request.continue() : request.abort());
    await page.goto(pathToFileURL(path.resolve(input)).href, {waitUntil: 'load'});
    await page.evaluate((base) => {
      document.querySelectorAll('a[href]').forEach(a => {
        const href = a.getAttribute('href');
        if (href && !/^(https?:|#|data:)/.test(href)) a.href = new URL(href, base).href;
      });
      document.querySelectorAll('details').forEach(d => d.remove());
      const intro = document.querySelector('h1');
      const note = document.createElement('p');
      note.textContent = 'Versión de lectura: explicación, políticas y tablas de la notebook. El código, las diferencias entre versiones y las trazas completas están en la notebook enlazada.';
      intro.after(note);
      document.querySelectorAll('.jp-OutputArea-output').forEach(e => {
        if (e.textContent.trim().startsWith('Entradas locales cargadas.') || e.textContent.trim().startsWith('Lectura de evidencia guardada.')) e.closest('.jp-CodeCell')?.remove();
      });
    }, baseUrl);
    await page.addStyleTag({content: `
      @page {size: A4; margin: 18mm 17mm 18mm;}
      body {font-family: Arial,sans-serif; font-size:10pt; color:#18212a; background:white;}
      main {max-width:none !important; padding:0 !important;}
      .jp-Notebook {padding:0 !important;}
      .jp-Cell {padding:0 !important; margin:0 0 9pt !important;}
      .jp-CodeCell > .jp-Cell-inputWrapper, .jp-InputPrompt, .jp-OutputPrompt {display:none !important;}
      .jp-Cell-outputWrapper, .jp-OutputArea, .jp-OutputArea-child, .jp-OutputArea-output, .jp-RenderedHTMLCommon {display:block !important; width:100% !important; padding:0 !important; margin:0 !important; overflow:visible !important;}
      .jp-RenderedHTMLCommon p, p {font-size:10pt !important;line-height:1.45 !important;margin:6pt 0 !important;}
      h1 {font-size:22pt !important;line-height:1.2 !important;margin:0 0 12pt !important;}
      h2 {font-size:16pt !important;margin:18pt 0 10pt !important;break-after:avoid;}
      h3 {font-size:12pt !important;margin:12pt 0 7pt !important;break-after:avoid;}
      table {border-collapse:collapse; width:100%;font-size:8.3pt !important; margin:9pt 0 !important;}
      td, th {white-space:normal !important; padding:5pt 6pt !important;overflow-wrap:anywhere;}
      thead {display:table-header-group;}
      tr {break-inside:avoid;}
      img {display:block;max-width:100% !important;max-height:470px;object-fit:contain;margin:10pt auto;}
      p:has(img) {break-inside:avoid;}
      a {color:#214e75;text-decoration:none;}
      .evidence-view {max-width:none !important;}
      .jp-OutputArea-output:has(.evidence-view h3) {break-inside:avoid;}
      .jp-Cell:has(h2) {break-inside:avoid;}
      .jp-Cell:has(h2):nth-child(6), .jp-Cell:has(h2):nth-child(10), .jp-Cell:has(h2):nth-child(12) {break-before:page;}
    `});
    await page.pdf({path: output, format:'A4', preferCSSPageSize:true, printBackground:true,
      displayHeaderFooter:true, headerTemplate:'<div></div>',
      footerTemplate:'<div style="font-family:Arial;font-size:8px;width:100%;padding:0 17mm;color:#666;display:flex;justify-content:space-between"><span>Thinking Harness · Caso 0003 · Evidencia registrada</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>'});
    console.log(path.resolve(output));
  } finally { await browser.close(); }
})();
