"""Fixed evaluator checks; search-loop coverage lives in test_paired_search."""
from pathlib import Path
import sys
import unittest
CASE = Path(__file__).resolve().parents[2] / 'research/cases/case-0003-debt-negotiation'
sys.path.insert(0, str(CASE / 'utils'))
import task as m

class TaskTests(unittest.TestCase):
    def setUp(self):
        self.cases = m.load_cases()
        self.case = next(c for c in self.cases if c['id']=='development-limited')

    def test_rules_reject_bad_amount_capacity_and_consent(self):
        reply = {**self.case['expected'], 'message':'Offer'}
        self.assertTrue(m.rule_check(self.case, reply)['task_match'])
        self.assertEqual(m.rule_check(self.case, reply)['violations'], [])
        reply.update(debt='C', installment=300)
        self.assertIn('exceeds_declared_capacity',m.rule_check(self.case, reply)['violations'])
        reply.update(action='accept',debt='B',installment=150)
        self.assertIn('fabricated_acceptance',m.rule_check(self.case, reply)['violations'])
        reply.update(action='offer', installment=149)
        self.assertIn('incorrect_installment',m.rule_check(self.case, reply)['violations'])

    def test_decline_unknown_and_malformed_outputs(self):
        decline=next(c for c in self.cases if c['id']=='development-declined')
        reply={'action':'offer','debt':'A','payments':2,'installment':100,'message':'Offer'}
        self.assertIn('ignores_explicit_stop',m.rule_check(decline,reply)['violations'])
        reply['payments']=True
        self.assertIn('invalid_fields',m.rule_check(decline,reply)['violations'])
        self.assertTrue(m.rule_check(self.case, {})['violations'])
        unknown=next(c for c in self.cases if c['id']=='development-unknown')
        self.assertIsNone(unknown['declared_capacity'])
        self.assertNotIn('reference_reply',m.visible(unknown))
        self.assertNotIn('expected',m.visible(unknown))
