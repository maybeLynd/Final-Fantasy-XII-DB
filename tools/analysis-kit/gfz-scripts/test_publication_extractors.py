"""Boundary controls for address guards and module-docstring extraction."""
from pathlib import Path
import tempfile
import unittest

import gen_address_index as address
import gen_rules_index as rules
import knowledge_db as knowledge
import program_coverage as coverage
import census_bin_signatures as signatures


class ExtractorControls(unittest.TestCase):
    def test_long_hex_guards_match_text_without_backspace_and_keep_short_address(self):
        text = '00265020abcdef0123456789 00265020'
        for guard in [address.ADDR_LONGHEX, knowledge.ADDR_LONGHEX, coverage.LONGHEX]:
            with self.subTest(pattern=guard.pattern):
                self.assertEqual(guard.sub('', text), ' 00265020')
                self.assertIsNone(guard.search('00265020'))
                self.assertIsNone(guard.search('x00265020abcdef0123456789'))

    def test_real_citation_forms_survive_with_neighboring_long_hex(self):
        text = '`00265020` FUN_002F9860\n```\n00267E18 ret\n```\n00265020abcdef0123456789'
        expected = {'00265020', '002F9860', '00267E18'}
        self.assertEqual(set(knowledge.citation_forms(text)), expected)
        self.assertEqual(coverage.cited_addresses(text), expected)

    def test_nav_version_test_bytes_keep_classifier_behavior(self):
        self.assertEqual(signatures.classify(b'NAV\x02', b'NAV\x02' + bytes(60), 3470)[0],
                         'MAGIC_TAG_VERSION')

    def test_module_docstrings_have_no_delimiters_and_are_not_executed(self):
        with tempfile.TemporaryDirectory() as scratch:
            root = Path(scratch)
            folder = root / rules.SCRIPT_DIR
            folder.mkdir(parents=True)
            (folder / 'one.py').write_text('"""One line."""\nraise AssertionError("must not execute")\n')
            (folder / 'single.py').write_text("'''Single quoted module.'''\n")
            (folder / 'late.py').write_text('# comment\n' * 100 + '"""After long comments.\nMore detail.\n"""\n')
            (folder / 'nested.py').write_text('def f():\n    """A function docstring is not a module rule."""\n')
            (folder / 'multi.py').write_text('"""\nFirst meaningful line.\n\nOther detail.\n"""\n')
            self.assertEqual(dict(rules.script_rules(root)), {
                'one.py': 'One line.', 'single.py': 'Single quoted module.',
                'late.py': 'After long comments.', 'multi.py': 'First meaningful line.'})

    def test_invalid_python_is_not_silently_indexed_as_a_valid_checker(self):
        with tempfile.TemporaryDirectory() as scratch:
            folder = Path(scratch) / rules.SCRIPT_DIR
            folder.mkdir(parents=True)
            (folder / 'broken.py').write_text('"""Apparently valid rule."""\ndef invalid(:\n')
            with self.assertRaises(SyntaxError):
                rules.script_rules(scratch)


if __name__ == '__main__':
    unittest.main()
