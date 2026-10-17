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

    def test_paper_folder_readme_keeps_catalog_identity(self):
        folder = self.root / 'research/literature/reviews/pap-0001-stop'
        folder.mkdir(parents=True)
        self.write_doc('doc-0001-original.md')
        original = self.root / 'doc-0001-original.md'
        (folder / 'README.md').write_text(original.read_text().replace('doc-0001', 'pap-0001'))
        original.unlink()
        rows, errors = checks.controlled_documents(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(rows[0]['id'], 'pap-0001')
        self.assertEqual(rows[0]['path'], 'research/literature/reviews/pap-0001-stop/README.md')

    def test_readme_exception_rejects_wrong_folder_and_identity(self):
        for directory, identifier in [
            ('research/literature/reviews/pap-0002-example', 'pap-0001'),
            ('docs/pap-0001-example', 'pap-0001'),
            ('research/literature/reviews/doc-0001-example', 'doc-0001'),
        ]:
            with self.subTest(directory=directory):
                folder = self.root / directory
                folder.mkdir(parents=True)
                self.write_doc('doc-0001-original.md')
                original = self.root / 'doc-0001-original.md'
                readme = folder / 'README.md'
                readme.write_text(original.read_text().replace('doc-0001', identifier))
                original.unlink()
                _, errors = checks.controlled_documents(self.root)
                self.assertTrue(any('filename must start' in error for error in errors))
                readme.unlink()

    def test_local_upstream_is_excluded_from_document_checks(self):
        folder = self.root / 'research/literature/reviews/pap-0001-stop/_local/upstream'
        folder.mkdir(parents=True)
        (folder / 'README.md').write_text('---\nid: invalid\n---\n[missing](missing.md)')
        rows, errors = checks.controlled_documents(self.root)
        self.assertEqual((rows, errors), ([], []))
        self.assertEqual(checks.local_links(self.root), [])

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


    def case_readme(self, folder, identifier='case-0003'):
        path = self.root / folder / 'README.md'
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f'---\nid: {identifier}\ntitle: Example\nstatus: in-review\n'
                        'revision: 1\ncreated: 2026-10-16\nupdated: 2026-10-16\n---\n')
        return path

    def test_paper_and_case_folder_rules_coexist(self):
        self.case_readme('research/proposals/case-0003-example')
        self.case_readme('research/literature/reviews/pap-0001-stop', 'pap-0001')
        rows, errors = checks.controlled_documents(self.root)
        self.assertEqual(errors, [])
        self.assertEqual({row['id'] for row in rows}, {'case-0003', 'pap-0001'})

    def test_case_folder_readme_has_one_catalog_identity(self):
        path = self.case_readme('research/proposals/case-0003-example')
        path.with_name('README.es.md').write_text('---\ntranslation_of: case-0003\nsource: README.md\n---\n')
        rows, errors = checks.controlled_documents(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['path'], 'research/proposals/case-0003-example/README.md')

    def test_case_folder_mismatched_identity_is_rejected(self):
        self.case_readme('research/proposals/case-0002-example')
        _, errors = checks.controlled_documents(self.root)
        self.assertTrue(any('filename must start' in error for error in errors))

    def test_case_folder_exception_does_not_allow_other_locations_or_types(self):
        for folder, identifier in [('other/case-0003-example', 'case-0003'),
                                   ('research/proposals/doc-0001-example', 'doc-0001')]:
            with self.subTest(folder=folder):
                path = self.case_readme(folder, identifier)
                _, errors = checks.controlled_documents(self.root)
                self.assertTrue(any('filename must start' in error for error in errors))
                path.unlink()

    def test_case_folder_does_not_hide_duplicate_document_identity(self):
        self.case_readme('research/proposals/case-0003-first')
        self.case_readme('research/proposals/case-0003-second')
        _, errors = checks.controlled_documents(self.root)
        self.assertTrue(any('duplicate id' in error for error in errors))


if __name__ == '__main__':
    unittest.main()
