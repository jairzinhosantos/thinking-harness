#!/usr/bin/env python3
"""Refresh notebook image attachments from their recorded Mermaid sources."""
import base64
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / 'research/proposals/case-0003-debt-negotiation'


def main():
    local = ROOT / 'node_modules/.bin/mmdc'
    executable = str(local) if local.exists() else shutil.which('mmdc')
    if not executable:
        raise RuntimeError('Mermaid CLI is not installed')
    for notebook in sorted(CASE.glob('*.ipynb')):
        content = json.loads(notebook.read_text())
        for cell in content['cells']:
            record = cell.get('metadata', {}).get('diagram')
            if not record:
                continue
            source = (CASE / record['source']).resolve()
            if not source.is_relative_to(ROOT) or source.suffix != '.mmd':
                raise ValueError('Expected a repository-local Mermaid source')
            with tempfile.TemporaryDirectory() as tmp:
                output = Path(tmp) / 'workflow.png'
                subprocess.run([executable, '-i', str(source), '-o', str(output),
                                '-b', 'white', '-t', 'neutral', '-s', '2'], check=True)
                data = output.read_bytes()
            record['source_sha256'] = hashlib.sha256(source.read_bytes()).hexdigest()
            record['preview_sha256'] = hashlib.sha256(data).hexdigest()
            cell['attachments'] = {'workflow.png': {'image/png': base64.b64encode(data).decode()}}
        notebook.write_text(json.dumps(content, ensure_ascii=False, indent=1) + '\n')
        print(notebook.relative_to(ROOT))


if __name__ == '__main__':
    main()
