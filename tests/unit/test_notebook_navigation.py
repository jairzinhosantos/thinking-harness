"""Validate moved notebook navigation, preserved outputs and replay from their folder."""
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import re
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
CASE = ROOT / 'research/cases/case-0003-debt-negotiation'

class NotebookNavigationTests(unittest.TestCase):
    def test_navigation_outputs_and_replay_from_notebook_directory(self):
        notebooks = sorted((CASE / 'notebooks').glob('*.ipynb'))
        self.assertEqual(len(notebooks), 7)
        self.assertFalse(list(CASE.glob('*.ipynb')))
        before = Path.cwd()
        try:
            os.chdir(CASE / 'notebooks')
            for path in notebooks:
                notebook = json.loads(path.read_text())
                output = [c.get('outputs', []) for c in notebook['cells'] if c['cell_type'] == 'code']
                digest = hashlib.sha256(json.dumps(output, sort_keys=True).encode()).hexdigest()
                self.assertEqual(digest, notebook['metadata']['navigation_revision']['outputs_sha256'])
                first = ''.join(notebook['cells'][0]['source'])
                self.assertIn('../../../../docs/README.md', first)
                self.assertIn('../README.md', first)
                scope = {}
                with patch('urllib.request.urlopen', side_effect=AssertionError('Unexpected network')), patch('IPython.display.display'), contextlib.redirect_stdout(io.StringIO()):
                    for cell in notebook['cells']:
                        source = ''.join(cell['source'])
                        if cell['cell_type'] == 'markdown':
                            for link in re.findall(r'\]\(([^)]+)\)', source):
                                if not link.startswith(('https:', 'http:', 'attachment:', '#')):
                                    self.assertTrue((path.parent / link.split('#')[0]).exists(), link)
                        else:
                            exec(compile(source, path.name, 'exec'), scope)
        finally:
            os.chdir(before)

if __name__ == '__main__':
    unittest.main()
