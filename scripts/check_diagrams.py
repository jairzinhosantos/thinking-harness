#!/usr/bin/env python3
"""Check Draw.io provenance and render Markdown Mermaid diagrams."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

IGNORED = {'.git', '.venv', '__pycache__', 'node_modules', '_scratch', '_local', 'runs'}


def mermaid_blocks(content):
    """Read fenced blocks without mistaking examples inside other fences for diagrams."""
    fence = None
    active = False
    body = []
    start = 0
    for number, line in enumerate(content.splitlines(), 1):
        if fence is None:
            opening = re.match(r'^\s{0,3}(`{3,}|~{3,})(.*)$', line)
            if opening:
                fence = opening.group(1)
                active = opening.group(2).strip() == 'mermaid'
                start, body = number, []
        elif re.fullmatch(r'\s{0,3}' + re.escape(fence[0]) + '{' + str(len(fence)) + r',}\s*', line):
            if active:
                if not '\n'.join(body).strip():
                    raise ValueError(f'empty Mermaid block at line {start}')
                yield start, '\n'.join(body) + '\n'
            fence, active = None, False
        elif active:
            body.append(line)
    if fence is not None and active:
        raise ValueError(f'unclosed Mermaid block at line {start}')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def drawio_records(root):
    return [
        {'source': source.relative_to(root).as_posix(),
         'preview': (Path('diagrams/exports') / (source.stem + '.svg')).as_posix(),
         'source_sha256': digest(source),
         'preview_sha256': digest(root / 'diagrams/exports' / (source.stem + '.svg'))}
        for source in sorted((root / 'diagrams/source').glob('*.drawio'))
    ]


def preview_checks(root):
    errors = []
    try:
        expected = drawio_records(root)
    except FileNotFoundError as exc:
        return [f'Missing Draw.io preview: {exc.filename}']
    manifest = root / 'diagrams/exports/manifest.json'
    if not expected and not manifest.exists():
        return []
    try:
        actual = json.loads(manifest.read_text())
        if actual.get('diagrams') != expected:
            errors.append('Draw.io source/preview hashes differ from the recorded export; regenerate and review.')
    except (OSError, ValueError, AttributeError) as exc:
        errors.append(f'Invalid Draw.io export manifest: {exc}')
    for record in expected:
        try:
            tree = ET.parse(root / record['preview'])
            if tree.getroot().tag.split('}')[-1] != 'svg':
                errors.append(f"{record['preview']}: expected SVG root")
        except ET.ParseError as exc:
            errors.append(f"{record['preview']}: invalid XML: {exc}")
    return errors


def render_mermaid(root, destination, executable=None):
    if not executable:
        local = root / 'node_modules/.bin/mmdc'
        executable = str(local) if local.exists() else shutil.which('mmdc')
    if not executable:
        raise RuntimeError('Mermaid CLI not found; run npm ci, then npm run check:diagrams.')
    destination.mkdir(parents=True, exist_ok=True)
    # GitHub-hosted Linux runners require this for Chromium. Local rendering keeps its sandbox.
    extra = []
    if os.environ.get('GITHUB_ACTIONS') == 'true':
        config = destination / 'puppeteer.json'
        config.write_text(json.dumps({'args': ['--no-sandbox']}))
        extra = ['--puppeteerConfigFile', str(config)]
    count = 0
    for path in sorted(root.rglob('*.md')):
        if any(part in IGNORED for part in path.relative_to(root).parts):
            continue
        for line, body in mermaid_blocks(path.read_text(encoding='utf-8')):
            count += 1
            name = str(count).zfill(3) + '-' + path.stem
            source, output = destination / (name + '.mmd'), destination / (name + '.svg')
            source.write_text(body)
            result = subprocess.run([executable, '-i', str(source), '-o', str(output),
                                     '-b', 'white', '-t', 'neutral', *extra],
                                    capture_output=True, text=True, timeout=120)
            if result.returncode or not output.exists():
                raise RuntimeError(f'{path.relative_to(root)}:{line}: Mermaid rendering failed\n'
                                   + result.stderr + result.stdout)
            print(f'Rendered {path.relative_to(root)}:{line} -> {output.name}')
    return count


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output-dir', type=Path)
    parser.add_argument('--record-drawio', action='store_true')
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if args.record_drawio:
        target = root / 'diagrams/exports/manifest.json'
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            target.write_text(json.dumps({'schema_version': 1, 'diagrams': drawio_records(root)}, indent=2) + '\n')
        except OSError as exc:
            print(exc, file=sys.stderr)
            return 1
        print('Recorded Draw.io source and preview hashes. Visual review is required.')
        return 0
    errors = preview_checks(root)
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    try:
        if args.output_dir:
            count = render_mermaid(root, args.output_dir.resolve())
        else:
            with tempfile.TemporaryDirectory(prefix='thinking-harness-diagrams-') as directory:
                count = render_mermaid(root, Path(directory))
    except (RuntimeError, ValueError, subprocess.TimeoutExpired, OSError) as exc:
        print(exc, file=sys.stderr)
        return 1
    print(f'Diagram checks passed: {count} Mermaid blocks rendered; Draw.io previews verified.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
