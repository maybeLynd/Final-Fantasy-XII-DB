"""Loss-prevention controls for mixed extracted and curated contradiction records."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import contradiction_index as ci


class PreservationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.db = Path(self.temp.name)
        (self.db / '_index').mkdir()
        self.doc = self.db / 'actor.md'
        self.header = '## CORRECTED 2026-09-10 — original actor claim'
        self.doc.write_text(self.header + '\nbody\n', encoding='utf-8')
        self.rows, _ = ci.merge(ci.extract(self.db), [])
        self.rows[0].update(id='CON-021', claim='curated claim', correction='curated correction',
                            instrument='typed writer trace', addresses='00265020')
        self.ledger = self.db / '_index' / 'CONTRADICTIONS.tsv'

    def test_line_drift_and_earlier_new_record_preserve_id_and_all_manual_cells(self):
        self.doc.write_text('\n\n' + self.header + '\nbody\n', encoding='utf-8')
        (self.db / 'earlier.md').write_text('## CORRECTED 2020-01-01 — earlier\n', encoding='utf-8')
        rows, _ = ci.merge(ci.extract(self.db), self.rows)
        self.assertEqual([r['id'] for r in rows], ['CON-021', 'CON-022'])
        self.assertEqual(rows[0]['line'], '3')
        for name in ci.MANUAL:
            self.assertEqual(rows[0][name], self.rows[0][name])
        again, _ = ci.merge(ci.extract(self.db), rows)
        self.assertEqual(rows, again)

    def test_legacy_snippet_adopts_after_line_drift(self):
        old = dict(self.rows[0], claim=ci.snippet(self.header))
        old.pop('source_header')
        old.pop('source_status')
        self.doc.write_text('\n' + self.header, encoding='utf-8')
        rows, _ = ci.merge(ci.extract(self.db), [old])
        self.assertEqual(rows[0]['id'], 'CON-021')
        self.assertEqual(rows[0]['source_header'], self.header)
        self.assertEqual(rows[0]['instrument'], old['instrument'])

    def test_missing_source_retains_history(self):
        self.doc.unlink()
        rows, _ = ci.merge(ci.extract(self.db), self.rows)
        self.assertEqual(rows[0]['source_status'], 'missing')
        for key, value in self.rows[0].items():
            if key != 'source_status':
                self.assertEqual(rows[0][key], value)

    def test_legacy_snippet_keeps_internal_spacing_during_adoption(self):
        line = 'count:  10,472     CORRECTED 2026-09-10 — recount'
        self.doc.write_text(line, encoding='utf-8')
        old = dict(self.rows[0], claim=ci.snippet(line))
        old.pop('source_header')
        rows, _ = ci.merge(ci.extract(self.db), [old])
        self.assertEqual(rows[0]['claim'], old['claim'])
        self.assertEqual(rows[0]['source_header'], ' '.join(line.split()))

    def test_reappearing_source_reuses_id(self):
        missing, _ = ci.merge([], self.rows)
        rows, _ = ci.merge(ci.extract(self.db), missing)
        self.assertEqual(rows, self.rows)

    def test_changed_header_requires_review_instead_of_duplicate_id(self):
        self.doc.write_text(self.header + ' changed', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'overlaps'):
            ci.merge(ci.extract(self.db), self.rows)

    def test_legacy_manual_claim_does_not_match_by_line_number(self):
        old = dict(self.rows[0])
        old.pop('source_header')
        with self.assertRaisesRegex(ValueError, 'overlaps'):
            ci.merge(ci.extract(self.db), [old])

    def test_duplicate_header_and_duplicate_ids_are_rejected(self):
        self.doc.write_text(self.header + '\n' + self.header, encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'duplicate source'):
            ci.merge(ci.extract(self.db), self.rows)
        with self.assertRaisesRegex(ValueError, 'duplicate or invalid IDs'):
            ci.merge([], self.rows * 2)

    def test_ledger_examples_ignored_but_permanent_correction_retained(self):
        (self.db / '_index' / 'CONTRADICTION-LEDGER.md').write_text(
            'A dated header — `CORRECTED 2026-09-02`, etc.\n'
            '1. It saw CORRECTED 2026-09-03 in an example.\n'
            '## CORRECTED 2026-09-10 — actual permanent correction\n', encoding='utf-8')
        found = ci.extract(self.db)
        rows = [r for r in found if r['document'].endswith('CONTRADICTION-LEDGER.md')]
        self.assertEqual(len(rows), 1)
        self.assertIn('actual permanent', rows[0]['source_header'])

    def test_replacement_failure_leaves_original_bytes_and_no_temporary_file(self):
        self.ledger.write_bytes(b'original receipt')
        with patch.object(ci.os, 'replace', side_effect=OSError('injected replacement failure')):
            with self.assertRaises(OSError):
                ci.write_ledger(self.ledger, self.rows, b'original receipt')
        self.assertEqual(self.ledger.read_bytes(), b'original receipt')
        self.assertEqual(list(self.ledger.parent.glob('.contradictions-*')), [])

    def test_concurrent_ledger_change_is_not_overwritten(self):
        self.ledger.write_bytes(b'peer update')
        with self.assertRaisesRegex(ValueError, 'changed during'):
            ci.write_ledger(self.ledger, self.rows, b'previous bytes')
        self.assertEqual(self.ledger.read_bytes(), b'peer update')

    def test_roundtrip_preserves_all_cells_and_source_anchors(self):
        ci.write_ledger(self.ledger, self.rows, None)
        self.assertEqual(ci.read_ledger(self.ledger), self.rows)

    def test_unknown_columns_and_malformed_rows_fail_without_truncation(self):
        self.ledger.write_text('\t'.join(ci.COLUMNS + ['extra_curated']) + '\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'columns'):
            ci.read_ledger(self.ledger)
        self.ledger.write_text('\t'.join(ci.COLUMNS) + '\nCON-001\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'cell count'):
            ci.read_ledger(self.ledger)

    def test_db_option_defaults_to_that_databases_ledger(self):
        r = subprocess.run([sys.executable, ci.__file__, 'extract', '--db', str(self.db)],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(self.ledger.exists())
        self.assertEqual(len(ci.read_ledger(self.ledger)), 1)


if __name__ == '__main__':
    unittest.main()
