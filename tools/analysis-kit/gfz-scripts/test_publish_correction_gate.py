#!/usr/bin/env python3
"""Fixtures for publish_correction_gate.py (FABLE-REQ-FRONTIER-CONTRACT-
CORRECTION-PUBLISH-NEEDS-CONSUMER-CHECK): the gate's positive and negative
self-test, run end-to-end against a scratch git repo.

Covered:
  - no correction marker           -> pass
  - ~~ alone / keyword alone       -> pass (not a correction publish)
  - correction + staged record     -> pass
  - correction + record in message -> pass
  - PENDING PROPAGATION record     -> pass, note surfaced
  - correction, no record          -> refuse
  - record lacking consumer rows   -> refuse
  - exec-shaped claim, record with no .py -> refuse
  - exec-shaped claim, record names .py   -> pass
  - missing record file in message -> refuse
"""
import os, subprocess, sys, tempfile, unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import publish_correction_gate as g

PAGE = "Database/FFXII TZA/00-Engine-Core-Runtime/CONTRACT-fixture.md"
REC = "Database/FFXII TZA/_index/candidates/fixture-consumer-check.md"


class Gate(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.email", "t@t"], cwd=self.root)
        subprocess.run(["git", "config", "user.name", "t"], cwd=self.root)
        subprocess.run(["git", "config", "commit.gpgsign", "false"], cwd=self.root)
        page = Path(self.root) / PAGE
        page.parent.mkdir(parents=True)
        page.write_text("# page\n\nold prose claim\n\ndispatch says `(0, cx)` "
                        "here\n\nother text\n", encoding="utf-8")
        subprocess.run(["git", "add", "-A"], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "base"], cwd=self.root,
                       check=True)

    def _edit(self, text):
        (Path(self.root) / PAGE).write_text(text, encoding="utf-8")

    def _correct(self, exec_claim=False, kw="Corrected"):
        """Replace a real claim line with its struck+keyword correction, so
        the strike quotes removed text (strike-provenance)."""
        old, new = ("dispatch says `(0, cx)` here",
                    "~~dispatch says `(0, cx)` here~~ **as `handler(id, 0)`**") \
            if exec_claim else \
            ("old prose claim", "~~old prose claim~~ **new prose claim**")
        page = Path(self.root) / PAGE
        self._edit(page.read_text().replace(
            old, new + " *%s 2026-09-26.*" % kw))

    def _record(self, body, rel=REC):
        p = Path(self.root) / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body, encoding="utf-8")
        return rel

    GOOD_REC = ("# Affected-consumer check - fixture\n\n"
                "affected: CONTRACT-fixture.md claim rows\n\n"
                "| consumer | agrees |\n|---|---|\n"
                "| `CONTRACT-fixture.md` | yes |\n\n"
                "regression: fixture_check.py\n")
    BAD_REC = "# notes\n\nno consumer table and no agreement tokens\n"
    PENDING_REC = ("# Affected-consumer check\n\nStatus: PENDING PROPAGATION\n\n"
                   "affected: EXP-999 fixture claim\n\n"
                   "| consumer | agrees |\n|---|---|\n| `x.md` | routed-to-"
                   "ORACLE-FIX-1 |\n\nregression: see text\n")

    def test_no_marker_passes(self):
        self._edit("# page\n\nold claim line\n\nplain addition\n\nother text\n")
        ok, refuse, _ = g.gate(self.root, [PAGE], "msg")
        self.assertTrue(ok, refuse)

    def test_strike_alone_passes(self):
        self._edit("# page\n\nold claim line\n\n~~struck only~~\n\nother text\n")
        ok, refuse, _ = g.gate(self.root, [PAGE], "msg")
        self.assertTrue(ok, refuse)

    def test_keyword_alone_passes(self):
        self._edit("# page\n\nold claim line\n\nCorrected. new text\n\n"
                   "other text\n")
        ok, refuse, _ = g.gate(self.root, [PAGE], "msg")
        self.assertTrue(ok, refuse)

    def test_correction_no_record_refuses(self):
        self._correct()
        ok, refuse, _ = g.gate(self.root, [PAGE], "msg")
        self.assertFalse(ok)
        self.assertTrue(any("consumer-check" in r for r in refuse))

    def test_staged_record_passes(self):
        self._correct()
        rec = self._record(self.GOOD_REC + "run: not_a_real_check.py\n")
        ok, refuse, _ = g.gate(self.root, [PAGE, rec], "msg")
        self.assertTrue(ok, refuse)

    def test_record_named_in_message_passes(self):
        self._correct()
        self._record(self.GOOD_REC + "run: not_a_real_check.py\n")
        ok, refuse, _ = g.gate(self.root, [PAGE],
                               "see _index/candidates/fixture-consumer-check.md")
        self.assertTrue(ok, refuse)

    def test_record_without_consumers_refuses(self):
        self._correct()
        rec = self._record(self.BAD_REC)
        ok, refuse, _ = g.gate(self.root, [PAGE, rec], "msg")
        self.assertFalse(ok)

    def test_exec_claim_needs_py_control(self):
        self._correct(exec_claim=True)
        rec = self._record(self.GOOD_REC)  # names a .py that does not exist
        ok, refuse, _ = g.gate(self.root, [PAGE, rec], "msg")
        self.assertFalse(ok)
        self.assertTrue(any(".py" in r for r in refuse))

    def test_exec_claim_with_existing_py_and_run_passes(self):
        # 2026-09-27: an existing .py alone is not the control - the record
        # must pin the run to a commit that is an ancestor of HEAD.
        self._correct(exec_claim=True)
        (Path(self.root) / "fixture_check.py").write_text("print(1)\n")
        run_commit = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=self.root,
            capture_output=True, text=True).stdout.strip()
        rec = self._record(self.GOOD_REC + "run: verified at %s\n" % run_commit)
        ok, refuse, _ = g.gate(self.root, [PAGE, rec], "msg")
        self.assertTrue(ok, refuse)

    def test_pending_propagation_passes_with_note(self):
        self._correct()
        rec = self._record(self.PENDING_REC)
        ok, refuse, notes = g.gate(self.root, [PAGE, rec], "msg")
        self.assertTrue(ok, refuse)
        self.assertTrue(any("PENDING" in n for n in notes))

    def test_missing_record_in_message_refuses(self):
        self._correct()
        ok, refuse, _ = g.gate(self.root, [PAGE],
                               "see _index/candidates/nope-consumer-check.md")
        self.assertFalse(ok)

    def test_reedited_correction_row_does_not_refire(self):
        # A ledger row is one line: once a publish struck text in it, every
        # later edit re-adds the strike+keyword the row already carries.
        # The gate must count only markers NEW to the hunk
        # (FABLE-NOTICE-FRONTIER-CORRECTION-GATE-REFIRES-ON-ROW-EDITS).
        self._correct()
        subprocess.run(["git", "add", "-A"], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "correction landed"],
                       cwd=self.root, check=True)
        # re-edit the same row: strike and 'Corrected' ride along unchanged
        self._edit("# page\n\nold claim line\n\n~~old prose claim~~ "
                   "**new prose claim** *Corrected 2026-09-26.* note "
                   "(narrowed: only when the flag is set)\n\nother text\n")
        ok, refuse, _ = g.gate(self.root, [PAGE], "msg")
        self.assertTrue(ok, refuse)

    def test_new_marker_in_reedited_hunk_still_fires(self):
        # An edit to a corrected row that adds a NEW strike+keyword is a
        # new correction and must still be gated.
        self._correct()
        subprocess.run(["git", "add", "-A"], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "correction landed"],
                       cwd=self.root, check=True)
        self._edit("# page\n\nold claim line\n\n~~old prose claim~~ "
                   "**new prose claim** *Corrected 2026-09-26.* note "
                   "~~and this too~~ *Superseded* now\n\nother text\n")
        ok, refuse, _ = g.gate(self.root, [PAGE], "msg")
        self.assertFalse(ok)
        self.assertTrue(any("consumer-check" in r for r in refuse))

    def test_invented_strike_refuses(self):
        # A strike is a claim the page once said those words; an invented
        # span must be refused even with a clean consumer record
        # (FABLE-REQ-FRONTIER-STRIKE-MUST-QUOTE-REMOVED-TEXT).
        self._edit("# page\n\nold prose claim\n\n~~a phrase this file never "
                   "carried~~ **replacement** *Corrected 2026-09-26.*\n\n"
                   "other text\n")
        rec = self._record(self.GOOD_REC)
        ok, refuse, _ = g.gate(self.root, [PAGE, rec], "msg")
        self.assertFalse(ok)
        self.assertTrue(any("never said" in r for r in refuse))

    def test_history_requote_passes(self):
        # A strike verbatim-quoting an EARLIER revision (removed by an
        # intervening commit) is legal history, not an invented claim.
        page = Path(self.root) / PAGE
        page.write_text("# page\n\nan older reading stood here\n\nother\n",
                        encoding="utf-8")
        subprocess.run(["git", "add", "-A"], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "older text"], cwd=self.root,
                       check=True)
        page.write_text("# page\n\nintermediate text\n\nother\n",
                        encoding="utf-8")
        subprocess.run(["git", "add", "-A"], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "intermediate"],
                       cwd=self.root, check=True)
        page.write_text("# page\n\n~~an older reading stood here~~ "
                        "**intermediate text** *Corrected 2026-09-26.*\n\n"
                        "other\n", encoding="utf-8")
        rec = self._record(self.GOOD_REC)
        ok, refuse, _ = g.gate(self.root, [PAGE, rec], "msg")
        self.assertTrue(ok, refuse)

    def test_non_db_paths_ignored(self):
        self._edit("# page\n\nold claim line\n\n~~s~~ Corrected\n\nother\n")
        ok, refuse, _ = g.gate(self.root, ["tools/x.md"], "msg")
        self.assertTrue(ok, refuse)

    # --- 2026-09-27 directive: declarations, receipted runs, overrides ---

    def test_record_without_affected_declaration_refuses(self):
        # 'consumer + agrees' alone no longer qualifies: the record must say
        # WHICH claim it corrects.
        self._correct()
        rec = self._record("# check\n\n| consumer | agrees |\n"
                           "|---|---|\n| `x.md` | yes |\n\n"
                           "regression: fixture_check.py\n")
        ok, refuse, _ = g.gate(self.root, [PAGE, rec], "msg")
        self.assertFalse(ok)

    def test_no_strike_declared_correction_passes(self):
        # A correction need not carry ~~markers~~: a record explicitly
        # declaring the affected claim+path covers it - detection is the
        # supplement, the declaration is the contract.
        self._edit("# page\n\nold prose claim (restated 2026-09-27)\n\n"
                   "other text\n")
        rec = self._record(
            "# Affected-consumer check\n\n"
            "affected: CONTRACT-fixture.md - the 'old prose claim' wording\n\n"
            "| consumer | agrees |\n|---|---|\n| `CONTRACT-fixture.md` | yes |\n\n"
            "regression: none - prose-only wording\n")
        ok, refuse, _ = g.gate(self.root, [PAGE, rec], "msg")
        self.assertTrue(ok, refuse)

    def test_declared_untouched_path_refuses(self):
        self._edit("# page\n\nold prose claim (restated)\n\nother text\n")
        rec = self._record(
            "# check\n\naffected: Database/FFXII TZA/other/never-touched.md\n\n"
            "| consumer | agrees |\n|---|---|\n| `x.md` | yes |\n")
        ok, refuse, _ = g.gate(self.root, [PAGE, rec], "msg")
        self.assertFalse(ok)
        self.assertTrue(any("does not touch" in r for r in refuse))

    def test_declared_touched_tsv_passes(self):
        # SWE2STRUCT-REQ-FRONTIER-CORRECTION-GATE-TSV-AFFECTED-1003: a record
        # naming a database TSV that this publish touches is not refused.
        tsv = "Database/FFXII TZA/_types/fields.tsv"
        self._record("id\tvalue\nA\tnew\n", rel=tsv)
        self._edit("# page\n\nold prose claim (restated)\n\nother text\n")
        rec = self._record(
            "# check\n\naffected: `%s` row A\naffected: CONTRACT-fixture.md\n\n"
            "| consumer | agrees |\n|---|---|\n| `x.md` | yes |\n" % tsv)
        ok, refuse, _ = g.gate(self.root, [PAGE, tsv, rec], "msg")
        self.assertFalse(any("does not touch" in r for r in refuse), refuse)

    def test_declared_untouched_tsv_refuses(self):
        self._edit("# page\n\nold prose claim (restated)\n\nother text\n")
        rec = self._record(
            "# check\n\naffected: Database/FFXII TZA/_types/fields.tsv\n\n"
            "| consumer | agrees |\n|---|---|\n| `x.md` | yes |\n")
        ok, refuse, _ = g.gate(self.root, [PAGE, rec], "msg")
        self.assertFalse(ok)
        self.assertTrue(any("does not touch" in r for r in refuse))

    def test_exec_claim_needs_run_commit(self):
        # The .py control exists but the record pins no commit it ran at.
        self._correct(exec_claim=True)
        (Path(self.root) / "fixture_check.py").write_text("print(1)\n")
        rec = self._record(self.GOOD_REC)
        ok, refuse, _ = g.gate(self.root, [PAGE, rec], "msg")
        self.assertFalse(ok)
        self.assertTrue(any("not proof it ran" in r for r in refuse))

    def test_exec_claim_with_receipted_run_passes(self):
        self._correct(exec_claim=True)
        (Path(self.root) / "fixture_check.py").write_text("print(1)\n")
        run_commit = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=self.root,
            capture_output=True, text=True).stdout.strip()
        rec = self._record(self.GOOD_REC + "run: verified at %s\n" % run_commit)
        ok, refuse, _ = g.gate(self.root, [PAGE, rec], "msg")
        self.assertTrue(ok, refuse)

    def test_wrong_revision_receipt_refuses(self):
        # A receipt naming a commit that is not in history is the EXP-201/214
        # failure: same shape, different bytes, attached to the wrong revision.
        self._correct(exec_claim=True)
        (Path(self.root) / "fixture_check.py").write_text("print(1)\n")
        rec = self._record(self.GOOD_REC +
                           "run: verified at deadbeefdeadbeefdeadbeef\n")
        ok, refuse, _ = g.gate(self.root, [PAGE, rec], "msg")
        self.assertFalse(ok)
        self.assertTrue(any("wrong-revision" in r for r in refuse))


if __name__ == "__main__":
    unittest.main(verbosity=2)
