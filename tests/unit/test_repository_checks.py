import importlib.util
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('checks', Path(__file__).resolve().parents[2] / 'scripts/check_repository.py')
checks = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checks)


class RepositoryChecksTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write_doc(self, name, revision='1'):
        (self.root / name).write_text('---\nid: doc-0001\ntitle: Example\nstatus: draft\nrevision: '
                                     + revision + '\ncreated: 2026-09-29\nupdated: 2026-09-29\n---\n\nText\n')

    def test_duplicate_identity_is_rejected_even_with_different_names(self):
        self.write_doc('doc-0001-first.md')
        self.write_doc('doc-0001-second.md')
        _, errors = checks.controlled_documents(self.root)
        self.assertTrue(any('duplicate id' in error for error in errors))

    def test_invalid_revision_is_reported_without_crashing(self):
        self.write_doc('doc-0001-example.md', 'invalid')
        _, errors = checks.controlled_documents(self.root)
        self.assertTrue(any('positive integer' in error for error in errors))

    def test_local_link_cannot_escape_repository(self):
        (self.root / 'README.md').write_text('[outside](../external.md)\n[missing](missing.md)\n[remote](https://example.org)')
        self.assertEqual(len(checks.local_links(self.root)), 2)

    def test_valid_controlled_document_and_relative_link(self):
        self.write_doc('doc-0001-example.md')
        (self.root / 'README.md').write_text('[document](doc-0001-example.md#example)')
        rows, errors = checks.controlled_documents(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(checks.local_links(self.root), [])
        self.assertIn('doc-0001-example.md', checks.render_catalog(rows))

    def test_mathematical_calls_inside_code_are_not_links(self):
        (self.root / 'README.md').write_text('~~~text\nI[t](meta, I[t], L)\n~~~\n`I[t](meta)`')
        self.assertEqual(checks.local_links(self.root), [])

    def test_external_narration_is_rejected_across_line_breaks(self):
        (self.root / 'README.md').write_text('The researcher\nprefers observable progress.')
        self.assertTrue(any('external narration' in error for error in checks.editorial_checks(self.root)))

    def test_direct_voice_and_attributed_sources_are_preserved(self):
        (self.root / 'README.md').write_text(
            'Progress will be tracked through evidence.\n'
            'Human acceptance is required.\n'
            '> The researcher prefers a different method. [Source](https://example.org)\n'
            '`The user requested` is a code example.\n'
            '```text\nThe researcher prefers\n```\n')
        self.assertEqual(checks.editorial_checks(self.root), [])

    def test_external_narration_in_metadata_and_diagram_labels_is_rejected(self):
        (self.root / 'catalog.csv').write_text('id,notes\ndoc-0001,The user requested this layout.\n')
        (self.root / 'example.drawio').write_text(
            '<mxfile><diagram><mxGraphModel><root>'
            '<mxCell id="x" value="The researcher&amp;lt;br&amp;gt;prefers this"/>'
            '</root></mxGraphModel></diagram></mxfile>'.replace('&amp;', '&'))
        self.assertEqual(len(checks.editorial_checks(self.root)), 2)

    def test_dangling_diagram_edge_is_rejected(self):
        (self.root / 'example.drawio').write_text('<mxfile><diagram><mxGraphModel><root>'
            '<mxCell id="0"/><mxCell id="1" parent="0"/>'
            '<mxCell id="2" edge="1" source="1" target="missing"/>'
            '</root></mxGraphModel></diagram></mxfile>')
        self.assertTrue(any('unresolved target' in e for e in checks.diagram_checks(self.root)))


if __name__ == '__main__':
    unittest.main()
