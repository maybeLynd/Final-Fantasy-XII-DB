"""test_readiness_hook.py - SWE2-STRUCT's readiness_view.py wired into the systems view (HOOK.md;
SWE2STRUCT-REQ-FRONTIER-READINESS-VIEW-HOOK-1003; SWE2-FRONTIER, 2026-10-03). Fixtures only.
  H1  no capture -> every system says UNMEASURED for open obligations (never 0)
  H2  a captured row fills "open obligations under this system" from register_live / register_closed and shows the
      maturity label and the withholding conditions in counts (not as a node state: the state vocabulary is
      DASHBOARD-MEANINGS sections 1-2)
  H3  the phase cap: a maturity label past SPECIFICATION READY is never shown, it reads WITHHELD
  H4  parity pilots appear only under the PROBE label; nothing is summed and no percentage is drawn
  H5  the capture and the generator are declared, optional inputs
"""
import os, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "analysis-kit", "gfz-scripts"))
import build_views as BV  # noqa: E402

fails = 0


def check(tag, ok, text=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
    fails += (not ok)


tmp = tempfile.mkdtemp(prefix="readiness-test-")
COLS = ["system", "name", "l2", "pages", "contracts", "types", "fields", "gap_spans", "census_rows", "register_live", "register_closed",
        "contradictions_unresolved", "residue_partial_pages", "residue_unmapped", "readiness_pending", "unresolved_unregistered",
        "runtime_exp", "parity_probes", "board_open", "maturity", "maturity_withheld_by"]
rows = [["S-01", "boot", "MET", "2", "1", "0", "0", "0", "0", "3", "6", "0", "0", "0", "0", "0", "4", "2", "1", "SPECIFICATION READY", ""],
        ["S-02", "tick", "MET", "3", "3", "0", "0", "0", "0", "0", "2", "0", "0", "0", "0", "1", "1", "1", "2", "", "unresolved_unregistered=1"],
        ["S-03", "mode", "MET", "1", "1", "1", "42", "7", "1135", "0", "1", "0", "0", "0", "0", "0", "2", "1", "1", "PARITY CERTIFIED", ""]]
p = os.path.join(tmp, "readiness.tsv")
open(p, "w", encoding="utf-8").write("# readiness_view.py generated x; phase=DATABASE; a view input, not a gate\n" + "\t".join(COLS) + "\n"
                                     + "".join("\t".join(r) + "\n" for r in rows))
# H1
c = BV.readiness_counts(BV.readiness_rows({"readiness": os.path.join(tmp, "absent.tsv")}), "S-01")
check("H1 absent -> UNMEASURED", c == {"open obligations under this system": "UNMEASURED (readiness_view.py capture absent)"}, c)
rr = BV.readiness_rows({"readiness": p})
# H2
c1 = BV.readiness_counts(rr, "S-01")
check("H2 obligations from register_live/closed", c1["open obligations under this system"].startswith("3 live / 6 closed"), c1)
check("H2 maturity in counts", c1["maturity (DASHBOARD-MEANINGS 6.4)"] == "SPECIFICATION READY")
c2 = BV.readiness_counts(rr, "S-02")
check("H2 withheld names its condition", c2["maturity (DASHBOARD-MEANINGS 6.4)"] == "no label - withheld by unresolved_unregistered=1", c2)
check("H2 unknown system -> UNMEASURED", BV.readiness_counts(rr, "S-99")["open obligations under this system"].startswith("UNMEASURED"))
# H3
c3 = BV.readiness_counts(rr, "S-03")
check("H3 phase cap", c3["maturity (DASHBOARD-MEANINGS 6.4)"].startswith("WITHHELD") and "PARITY CERTIFIED" not in c3["maturity (DASHBOARD-MEANINGS 6.4)"].split("(")[0], c3)
# H4
check("H4 probes labelled", c1["parity probes (PROBE, database phase)"] == "2" and not any(k for k in c1 if "percent" in k or "total" in k or "score" in k))
# H5
ins = BV.declare_inputs(tmp)
check("H5 declared optional", ins["readiness"]["required"] is False and ins["readiness_view.py"]["required"] is False)
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
