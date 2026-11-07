"""Check the reading notebook against preserved experimental evidence."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

CASE = Path(__file__).resolve().parents[2] / 'research/cases/case-0003-debt-negotiation'
spec = importlib.util.spec_from_file_location('study_view_test', CASE / 'utils/study_view.py')
view = importlib.util.module_from_spec(spec)
spec.loader.exec_module(view)


class StudyViewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = view.load_records(CASE)

    def test_lengths_match_recorded_text_and_token_counts(self):
        record = self.records['adaptive']
        rows = view.length_rows(record)
        initial = record['protocol']['initial_policy']
        self.assertEqual(rows[0][3:6], [len(initial), len(initial.split()), 28])
        first_policy = next(row for row in rows if row[1:3] == [1, 'H'])
        self.assertEqual(first_policy[5], 107)
        invalid_strategy = next(row for row in rows if row[1:3] == [3, 'φ'])
        self.assertEqual(invalid_strategy[5], 'No registrado')
        self.assertFalse(any(row[1:3] == [3, 'H'] for row in rows))

    def test_trace_matches_calls_and_selection(self):
        record = self.records['adaptive']
        call = view.call_for(record, 'proposer', 1)
        self.assertEqual(call['parsed']['prompt'], record['report']['rounds'][1]['policy'])
        self.assertEqual(record['report']['selected_policy'], record['report']['rounds'][1]['policy'])
        for update in record['report']['strategy_updates']:
            following = next(r for r in record['report']['rounds'] if r['iteration'] == update['after_iteration'] + 1)
            self.assertEqual(following['strategy_used'], update['after'])
        self.assertEqual(sum(r['success'] for r in record['report']['test']['selected']['rows']), 7)

    def test_prompt_rendering_escapes_source_text(self):
        with patch.object(view, 'display') as display:
            view.prompt('H <candidate>', '<script>alert(1)</script>\nA & B', folded=True)
            rendered = display.call_args.args[0].data
        self.assertNotIn('<script>', rendered)
        self.assertIn('&lt;script&gt;', rendered)
        self.assertIn('A &amp; B', rendered)
        self.assertIn('<details>', rendered)


if __name__ == '__main__':
    unittest.main()
