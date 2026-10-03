"""count_fp_control.py [CHECK_CONSISTENCY_PATH] - fixture control for check_consistency.py's CALLER-COUNT attribution
(FABLE-REQ-FRONTIER-CHECK-CONSISTENCY-COUNT-FP-1003; SWE2-FRONTIER, 2026-10-03). Builds a scratch database and runs the
checker's main() on it. Expected on the repaired checker, FAILS 0:
  C1  a struck count "(~~16 callers~~ 47 direct ...)" is not a claim       -> no disagreement for 003A1DB0
  C2  "**00194290** (...) `005CDAA0` call ... [`001942C0`] - 4 callers" goes to the bullet subject 00194290
                                                                           -> no disagreement for 005CDAA0
  C3  "`00379CD0`, whose other 53 callers" is a scoped count             -> no disagreement against a total 66
  P1  positive control: two pages stating 12 vs 13 callers for 00AAAA00  -> still reported
On the pre-repair checker C1 and C2 report disagreements (the control is sensitive to both defects); C3 guards the
repaired attribution, which would otherwise give the scoped 53 to its owner and compare it with a total."""
import contextlib, importlib.util, io, os, sys, tempfile

here = os.path.dirname(os.path.abspath(__file__))
def _kit():                                       # walk up to the repository's Database/Tools kit, wherever this file sits
    d = here
    while os.path.dirname(d) != d:
        c = os.path.join(d, "Database", "Tools", "analysis-kit", "gfz-scripts", "check_consistency.py")
        if os.path.isfile(c):
            return c
        d = os.path.dirname(d)
    raise SystemExit("check_consistency.py not found above " + here)


path = sys.argv[1] if len(sys.argv) > 1 else _kit()
sys.path.insert(0, os.path.dirname(os.path.abspath(path)))
spec = importlib.util.spec_from_file_location("cc_ut", path)
cc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cc)

# one case per page: the checker's retraction look-behind spans 240 characters, so cases sharing a page leak into each other
H = "---\nstatus: DOCUMENTED\n---\n# P\n\n"
pages = {
    "c1.md": H + "`003A1DB0` (~~16 callers~~ 47 direct call sites in 38 functions).\n",
    "c2.md": H + "**00194290** (107 B, 4 A-measured callers) - setter; `005CDAA0` call + `+0x1F0` store [`001942C0`](x.md) - 4 callers, all A.\n",
    "c3.md": H + "(`0025ACA0` / `0025ABA0`) calls the thunk (`00379CD0`), whose other 53 callers are combat formula.\n",
    "p1.md": H + "`00AAAA00` has 12 callers.\n",
    "b.md": H + "`003A1DB0` has 38 callers.\n\n`005CDAA0` has 9 callers.\n\n`00379CD0` has 66 callers.\n\n`00AAAA00` has 13 callers.\n",
}
db = tempfile.mkdtemp(prefix="ccfp-")
os.makedirs(os.path.join(db, "00-Fixture"))           # check_consistency.docs() reads only NN- category folders
for n, t in pages.items():
    open(os.path.join(db, "00-Fixture", n), "w", encoding="utf-8").write(t)
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    try:
        cc.main(["--db", db])
    except SystemExit:
        pass
out = buf.getvalue()
sec = out[out.find("CALLER-COUNT disagreements"):]
sec = sec[:sec.find("\n\n")] if "\n\n" in sec else sec
fails = 0
for tag, addr, want in (("C1 struck count", "003A1DB0", False), ("C2 bullet subject", "005CDAA0", False),
                        ("C3 scoped other-count", "00379CD0", False), ("P1 real disagreement", "00AAAA00", True)):
    got = addr in sec
    ok = got == want
    fails += not ok
    print("%s  %s (%s %s)" % ("PASS" if ok else "FAIL", tag, addr, "reported" if got else "not reported"))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
