"""Keep answered-question advisories tied to current status and their own text block."""
from pathlib import Path
import tempfile
import unittest
import check_answered_not_established as checker


class AdvisoryControls(unittest.TestCase):
    def scan(self, text, ids=None):
        out = []
        checker.scan({'I-6', 'DD-1', 'EN-1', 'EE-3'} if ids is None else ids, text, 'fixture.md', out)
        return out

    def test_true_present_negative_is_retained_across_hard_wrap(self):
        found = self.scan('The location is unknown,\nand its extent is\nstill being checked. I-6.\n')
        self.assertEqual([(r[1], r[2]) for r in found], [(1, 'I-6')])

    def test_adjacent_bullet_cannot_lend_its_answered_id(self):
        text = '- [x] EN-1. The numeric mapping is measured.\n- [ ] Its purpose is not established.\n'
        self.assertEqual(self.scan(text), [])

    def test_adjacent_heading_cannot_lend_its_id(self):
        text = 'Which axes are used is not established here.\n\n### DD-1 — converter\nKnown converter.\n'
        self.assertEqual(self.scan(text), [])

    def test_struck_history_is_ignored_but_live_negative_on_same_line_survives(self):
        text = '~~The mode is not established — EE-3.~~ Established later.\n\n'
        text += '~~old is unknown~~ The writer is unknown. DD-1.\n'
        found = self.scan(text)
        self.assertEqual([(r[1], r[2]) for r in found], [(3, 'DD-1')])

    def test_multiline_strike_keeps_reported_line_numbers(self):
        text = '~~Old first line\nis unknown. EE-3.~~\n\nCurrent writer is unknown. DD-1.\n'
        self.assertEqual(self.scan(text)[0][1], 4)

    def test_open_id_in_same_block_keeps_ownership_ambiguous(self):
        self.assertEqual(self.scan('The parent DD-1 is discussed; the residual XX-9 is unknown.\n'), [])

    def test_current_status_not_historical_answered_word(self):
        rows = ('| I-6 | identity | CLOSED |\n'
                '| DG-1 | producer | **REOPENED 2026-09-10.** Earlier ANSWERED was withdrawn. |\n'
                '| ER-1 | table | ANSWERED in an earlier pass | OPEN |\n'
                '| AY-10 | keys | ANSWERED in an earlier pass | **STILL OPEN** — mixed row |\n'
                '| XX-1 | residual | **PARTLY ANSWERED** with work remaining |\n')
        with tempfile.TemporaryDirectory() as scratch:
            folder = Path(scratch) / '_index'
            folder.mkdir()
            (folder / 'OPEN-QUESTIONS.md').write_text(rows, encoding='utf-8')
            self.assertEqual(checker.answered_ids(scratch), {'I-6'})

    def test_duplicate_or_empty_question_census_is_not_a_pass(self):
        with tempfile.TemporaryDirectory() as scratch:
            folder = Path(scratch) / '_index'
            folder.mkdir()
            path = folder / 'OPEN-QUESTIONS.md'
            for text in ['', '| I-6 | identity | CLOSED |\n' * 2]:
                path.write_text(text, encoding='utf-8')
                with self.assertRaises(ValueError):
                    checker.answered_ids(scratch)


if __name__ == '__main__':
    unittest.main()
