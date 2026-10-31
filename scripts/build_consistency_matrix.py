"""Render the academic README matrix as one landscape A4 page.

Requires reportlab and DejaVu Sans; run from the repository with Python 3.11+.
Use --font-dir when the fonts are not installed in a known location.
"""
from html import escape
from pathlib import Path
import argparse
import os
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'docs/academic/README.md'
OUTPUT = ROOT / 'docs/academic/consistency-matrix.pdf'
LINK = 'https://github.com/jairzinhosantos/thinking-harness/blob/develop/docs/academic/README.md'


def register_fonts(directory=None):
    candidates = [Path(directory)] if directory else []
    if os.environ.get('THINKING_HARNESS_FONT_DIR'):
        candidates.append(Path(os.environ['THINKING_HARNESS_FONT_DIR']))
    candidates += [Path('/usr/share/fonts/truetype/dejavu'),
                   Path.home() / '.cache/codex-runtimes/codex-primary-runtime/dependencies/native/libreoffice-headless/libreoffice/LibreOfficeDev.app/Contents/Resources/fonts/truetype']
    font_dir = next((p for p in candidates if (p / 'DejaVuSans.ttf').exists()), None)
    if font_dir is None:
        raise RuntimeError('Set THINKING_HARNESS_FONT_DIR or --font-dir to a DejaVu Sans font directory')
    for name, suffix in [('Matrix', ''), ('Matrix-Bold', '-Bold'), ('Matrix-Italic', '-Oblique')]:
        pdfmetrics.registerFont(TTFont(name, str(font_dir / f'DejaVuSans{suffix}.ttf')))
    pdfmetrics.registerFontFamily('Matrix', normal='Matrix', bold='Matrix-Bold', italic='Matrix-Italic', boldItalic='Matrix-Bold')


def math_text(value):
    value = value.replace(r'\widehat', '').replace(r'\mathbf', '').strip()
    value = re.sub(r'\\mathrm\{([^}]+)\}', r'\1', value)
    for raw, cooked in [(r'\Delta', 'Δ'), (r'\rho', 'ρ'), (r'\ge', '≥'),
                        (r'\le', '≤'), (r'\in', '∈'), (r'\{', '{'), (r'\}', '}')]:
        value = value.replace(raw, cooked)
    value = escape(value)
    value = re.sub(r'_\{([^}]+)\}', r'<sub>\1</sub>', value)
    value = re.sub(r'_([a-zA-Z0-9]+)', r'<sub>\1</sub>', value)
    if '\\' in value:
        raise ValueError(f'Unmapped math: {value}')
    return value


def rich(value):
    parts = re.split(r'(\$[^$]+\$)', value)
    output = ''.join(math_text(p[1:-1]) if p.startswith('$') else escape(p) for p in parts)
    output = output.replace('&lt;br&gt;', '<br/>')
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', output)


def build(font_dir=None):
    register_fonts(font_dir)
    document = SOURCE.read_text()
    rows = [line.split('|')[1:-1] for line in document.splitlines()
            if line.startswith(('| **General**', '| **OE1**', '| **OE2**'))]
    if len(rows) != 3 or any(len(row) != 5 for row in rows):
        raise ValueError('Expected general objective and two specific objectives in the README')
    navy = colors.HexColor('#203348')
    burgundy = colors.HexColor('#7F3440')
    grey = colors.HexColor('#5C6670')
    line = colors.HexColor('#D3D9DF')
    style = ParagraphStyle('body', fontName='Matrix', fontSize=8.4, leading=11.6, textColor=navy, alignment=TA_LEFT)
    small = ParagraphStyle('small', parent=style, fontSize=7.7, leading=10.2)
    heading = ParagraphStyle('heading', parent=style, fontName='Matrix-Bold', fontSize=20, leading=25)
    title = ParagraphStyle('title', parent=style, fontName='Matrix-Bold', fontSize=10.6, leading=14)
    th = ParagraphStyle('th', parent=style, fontName='Matrix-Bold', fontSize=8, leading=11, textColor=colors.white)
    label = ParagraphStyle('label', parent=small, fontName='Matrix-Bold', textColor=burgundy)
    width, height = landscape(A4)
    usable = width - 56
    story = [Paragraph('THINKING HARNESS  /  PROYECTO DE TESIS II', label), Spacer(1, 5),
             Paragraph('Matriz de consistencia', heading),
             Paragraph('Mejora recursiva de harnesses agénticos con modelos de pesos abiertos', title), Spacer(1, 8),
             Paragraph('<b>Problema.</b> Construir agentes exige ajustar instrucciones, roles y coordinación por ensayo y error. '
                       'Se busca que el sistema haga esos ajustes y comprobar si conviene que también cambie su forma de proponer mejoras.', style), Spacer(1, 6)]
    cells = [[Paragraph(x, th) for x in ['Nivel', 'Objetivo', 'Hipótesis', 'Variables', 'Indicadores y criterios']]]
    cells += [[Paragraph(rich(value.strip().replace('**General**', '**OG**')), style) for value in row] for row in rows]
    table = Table(cells, colWidths=[40, 180, 176, 120, usable - 516], repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), navy), ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 7), ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 8), ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#F3F5F7'), colors.white]),
        ('LINEBELOW', (0, 0), (-1, 0), 1, burgundy), ('INNERGRID', (0, 1), (-1, -1), .3, line),
        ('BOX', (0, 1), (-1, -1), .4, line),
    ]))
    story += [table, Spacer(1, 7),
              Paragraph('<b>OG:</b> objetivo general. <b>Comparación:</b> B1 cambia el harness con instrucciones de mejora fijas (Z=0). '
                        'B2 también puede actualizar esas instrucciones (Z=1). Modelo, evaluación y presupuesto se mantienen iguales.', small), Spacer(1, 4),
              Paragraph('<b>Lectura:</b> q: éxito válido; v: incumplimientos; N<sub>h</sub>: intervenciones humanas; '
                        'T<sub>meta</sub>: tiempo hasta la meta; r<sub>uso</sub>: tokens, llamadas y costo; M<sub>h</sub>: minutos humanos. '
                        'N<sub>uso</sub>: actualizaciones reutilizadas; V<sub>prot</sub>: cambios en partes protegidas; '
                        'ρ<sub>traza</sub>: propuestas reconstruibles / registradas.', small), Spacer(1, 4),
              Paragraph('Δ<sub>q</sub> y Δ<sub>v</sub>: diferencias medias B2 menos B1; L<sub>95</sub> y U<sub>95</sub>: '
                        'límites inferior y superior del intervalo de confianza del 95%. Los valores medidos son estimaciones. '
                        '<b>Los umbrales se revisarán en factibilidad y se fijarán antes del contraste.</b>', small)]
    content_height = sum(flowable.wrap(usable, height)[1] for flowable in story)
    if content_height > height - 58:
        raise ValueError(f'Content needs {content_height:.1f} pt; available {height - 58:.1f}; edit content rather than overflow')

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(line); canvas.line(28, 25, width - 28, 25)
        canvas.setFont('Matrix', 7); canvas.setFillColor(grey)
        canvas.drawString(28, 14, 'Jairzinho Santos')
        canvas.drawRightString(width - 28, 14, 'Definiciones y Test 1 en develop  ·  1 / 1')
        canvas.linkURL(LINK, (width - 250, 8, width - 28, 23), relative=0)
        canvas.restoreState()
    doc = SimpleDocTemplate(str(OUTPUT), pagesize=(width, height), leftMargin=28, rightMargin=28,
                            topMargin=22, bottomMargin=36, title='Thinking Harness | Matriz de consistencia', author='Jairzinho Santos')
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f'{OUTPUT}: content {content_height:.1f} pt')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--font-dir')
    build(parser.parse_args().font_dir)
