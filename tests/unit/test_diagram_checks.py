import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('diagrams', Path(__file__).resolve().parents[2] / 'scripts/check_diagrams.py')
diagrams = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(diagrams)


class DiagramChecksTests(unittest.TestCase):
    def test_fenced_example_is_not_a_live_diagram(self):
        content = '````text\n```mermaid\ninvalid\n```\n````\n~~~mermaid\nflowchart LR\nA-->B\n~~~'
        self.assertEqual(list(diagrams.mermaid_blocks(content)), [(6, 'flowchart LR\nA-->B\n')])

    def test_unclosed_mermaid_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'unclosed'):
            list(diagrams.mermaid_blocks('```mermaid\nflowchart LR'))

    def test_empty_mermaid_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'empty'):
            list(diagrams.mermaid_blocks('```mermaid\n\n```'))

    def test_source_change_invalidates_recorded_preview(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'diagrams/source').mkdir(parents=True)
            (root / 'diagrams/exports').mkdir()
            source = root / 'diagrams/source/example.drawio'
            source.write_text('<mxfile/>')
            (root / 'diagrams/exports/example.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
            (root / 'diagrams/exports/manifest.json').write_text(json.dumps({'schema_version': 1, 'diagrams': diagrams.drawio_records(root)}))
            self.assertEqual(diagrams.preview_checks(root), [])
            source.write_text('<mxfile host="changed"/>')
            self.assertTrue(any('hashes differ' in e for e in diagrams.preview_checks(root)))

    def test_missing_preview_is_reported(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'diagrams/source').mkdir(parents=True)
            (root / 'diagrams/source/example.drawio').write_text('<mxfile/>')
            self.assertTrue(any('Missing Draw.io preview' in e for e in diagrams.preview_checks(root)))


if __name__ == '__main__':
    unittest.main()
