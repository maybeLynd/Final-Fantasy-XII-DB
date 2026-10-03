"""test_readiness_view.py - focused tests for readiness_view.py (SWE2-STRUCT, 2026-10-03): the phase cap and the UNMAPPED
condition from FABLE's ruling on the readiness-views design note, plus fail-closed handling. No live board writes and no
writes to the database tree; generated output goes to a temporary directory."""
import json, os, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import readiness_view as R  # noqa: E402

LAD = ["SPECIFICATION READY", "SEMANTIC CORE IMPLEMENTED", "NATIVE OPERATION REPLACEMENT", "PARITY CERTIFIED"]
GOOD = {"l2": "MET", "register_live": 0, "contradictions_unresolved": 0, "readiness_pending": 0,
        "unresolved_unregistered": 0, "residue_unmapped": 0}


class PhaseCap(unittest.TestCase):
    def test_database_phase_shows_at_most_spec_ready(self):
        self.assertEqual(R.maturity(GOOD, "DATABASE", LAD)[0], R.SR)
        for later in LAD[1:]:
            self.assertFalse(R.capped(later, "DATABASE"), later)

    def test_other_phase_is_unmeasured_not_guessed(self):
        for ph in ("RECONSTRUCTION", "INTEGRATION", "PARITY_CERTIFICATION"):
            self.assertEqual(R.maturity(GOOD, ph, LAD)[0], R.UNM)

    def test_lifecycle_missing_or_malformed_fails_closed(self):
        self.assertEqual(R.lifecycle_phase(None), (None, None))
        self.assertEqual(R.lifecycle_phase({"current_primary_phase": "DATABASE"}), (None, None))
        self.assertEqual(R.maturity(GOOD, None, None)[0], R.UNM)


class SpecReadyEvidence(unittest.TestCase):
    def test_unmapped_residue_withholds(self):
        lab, why = R.maturity(dict(GOOD, residue_unmapped=1), "DATABASE", LAD)
        self.assertEqual(lab, "")
        self.assertIn("residue_unmapped=1", why)

    def test_each_condition_withholds(self):
        for col, bad in (("l2", "NOT MET"), ("register_live", 1), ("contradictions_unresolved", 1),
                         ("readiness_pending", 1), ("unresolved_unregistered", 1)):
            self.assertEqual(R.maturity(dict(GOOD, **{col: bad}), "DATABASE", LAD)[0], "", col)

    def test_unmeasured_is_not_zero(self):
        lab, why = R.maturity(dict(GOOD, register_live=R.UNM), "DATABASE", LAD)
        self.assertEqual(lab, "")
        self.assertIn("register_live=UNMEASURED", why)

    def test_section14_items(self):
        sec = ("1. ~~**Old** spanning\n   lines.~~ **ANSWERED** here.\n2. Registered as OV-12.\n- Bare open question.\n")
        self.assertEqual(len(R.unregistered_items(sec)), 1)

    def test_self_test_passes(self):
        self.assertEqual(R.self_test(), 0)


class Generation(unittest.TestCase):
    def test_real_tree_generation_honours_cap_and_lists_unattributed(self):
        with tempfile.TemporaryDirectory() as td:
            lc = os.path.join(td, "lc.json")
            json.dump({"current_primary_phase": "DATABASE", "maturity_ladder": LAD}, open(lc, "w"))
            out = os.path.join(td, "rv.tsv")
            r = subprocess.run([sys.executable, os.path.join(HERE, "readiness_view.py"), "--lifecycle", lc,
                                "--board", os.path.join(td, "absent.json"), "--out", out], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            lines = open(out, encoding="utf-8").read().splitlines()
            hdr = lines[1].split("\t")
            rows = [dict(zip(hdr, l.split("\t"))) for l in lines[2:]]
            self.assertTrue(any(x["system"] == "UNATTRIBUTED" for x in rows))
            for x in rows:
                self.assertIn(x["maturity"], ("", R.SR), x["system"])
                if x["system"] != "UNATTRIBUTED":
                    self.assertEqual(x["board_open"], R.UNM)   # absent board -> UNMEASURED, never 0

    def test_absent_lifecycle_gives_unmeasured_labels(self):
        with tempfile.TemporaryDirectory() as td:
            out = os.path.join(td, "rv.tsv")
            r = subprocess.run([sys.executable, os.path.join(HERE, "readiness_view.py"), "--lifecycle",
                                os.path.join(td, "none.json"), "--board", os.path.join(td, "absent.json"), "--out", out],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            rows = open(out, encoding="utf-8").read().splitlines()[2:]
            self.assertTrue(all(l.split("\t")[19] in (R.UNM, "") for l in rows))
            self.assertTrue(any(l.split("\t")[19] == R.UNM for l in rows))


if __name__ == "__main__":
    unittest.main()
