"""Replay original provider outputs through the simplified loop, without inference."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

CASE = Path(__file__).resolve().parents[2] / 'research/cases/case-0003-debt-negotiation'
sys.path.insert(0, str(CASE / 'utils'))
import paired_search as search
import models
import task
from study_view import RUNS


class SearchReplayTests(unittest.TestCase):
    def test_existing_searches_keep_prompts_selection_and_scores(self):
        for key, name in RUNS.items():
            if key in ('inference', 'confirmation'):
                continue
            with self.subTest(run=name):
                protocol, expected = task.read_record(CASE / 'results' / name)
                calls = [json.loads(line) for line in (CASE / 'results' / name / 'calls.jsonl').read_text().splitlines()]
                lengths = {}
                for row in expected['rounds']:
                    for text, count in [('policy', 'policy_tokens'), ('strategy_used', 'strategy_tokens')]:
                        if count in row:
                            lengths[row[text]] = row[count]
                owner = self
                class ReplayClient:
                    def __init__(self, key, folder, snapshot, started, *, sampling, limits):
                        self.calls = self.tokens = 0
                        self.sampling, self.limits = sampling, limits
                    def length(self, text): return lengths[text]
                    def seed(self, value): pass
                    def peak_memory(self): return 0
                    def ask(self, role, instructions, payload, schema):
                        saved = calls[self.calls]
                        owner.assertEqual(role, saved['role'])
                        owner.assertEqual(models.messages_for('qwen3-8b', instructions, payload, schema), saved['messages'])
                        self.calls += 1
                        self.tokens += saved['input_tokens'] + saved['output_tokens']
                        return saved.get('parsed'), saved.get('error')
                with tempfile.TemporaryDirectory() as folder, patch.object(search.importlib.metadata, 'version', return_value='test-only'):
                    path = search.run(protocol['strategy'], folder, ReplayClient,
                                      output_tokens=protocol['limits']['output_tokens'], decoding=protocol.get('decoding', 'prompt_only'))
                    actual = json.loads((path / 'report.json').read_text())
                for field in ('status', 'search_status', 'rounds', 'strategy_updates', 'selected_iteration',
                              'selected_policy', 'selected_strategy', 'test', 'passes', 'tokens', 'calls'):
                    self.assertEqual(actual[field], expected[field], field)
                self.assertEqual(actual['calls'], len(calls))

    def test_dirty_sources_cannot_start_live_inference(self):
        with tempfile.TemporaryDirectory() as folder:
            fake = CASE / 'utils' / 'untracked-test.py'
            with patch.object(task, 'digest', return_value='changed'), patch.object(task.subprocess, 'check_output', side_effect=['commit\n', b'original']):
                with self.assertRaisesRegex(ValueError, 'Commit experiment sources'):
                    task.source_record([fake])

    def test_api_requires_explicit_live_execution(self):
        with self.assertRaisesRegex(ValueError, 'allow-live'):
            search.run('fixed', model='gpt-4o-mini-2024-07-18')
