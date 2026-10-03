"""test_interior_applier.py [--applier PATH] [--control PATH] - regression test for the shared-heading clobber (OPUS, 2026-10-03).

890844135, 33eb7192f and e63502b10 each applied a record to a page another record of the same mode and date had already
written. Both render the same heading, and the second record's applier re-rendered the first record's block with its own
rows: 55 published rows were deleted. This test builds a throwaway tree (stub check_dispositions / family_prover over a
NOP image, so no real page or image is touched) and requires of interior_applier.py:

  T1  record A then record B on one page: both PATCHED, every row of both present (check_record_rows_present)
  T2  re-running A and B: ALREADY, page unchanged
  T3  a corrected A rows.json: REWRITTEN, B's rows untouched
  T4  a block that links A but holds a row A no longer carries: REFUSED, page unchanged
  C1  control: the pre-fix applier applied for B over A must lose A's rows, so T1 is shown to discriminate the defect.
Defaults: the two applier copies pinned in _index/candidates/opus-interior-clobber-1003/ (interior_applier_fixed.py, the
fixed master; interior_applier_prefix.py, byte-identical to the copy 047553008 published). Tools/work is not tracked,
so the test never depends on it.
Prints one line per case and FAILS n."""
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = HERE
REC = os.path.normpath(os.path.join(HERE, "..", "..", "..", "FFXII TZA", "_index", "candidates", "opus-interior-clobber-1003"))
sys.path.insert(0, KIT)
import check_record_rows_present as CR  # noqa: E402

BASE = 0x00400000
STUB_CD = "def load_functions():\n    return {0x00400000: 0x100, 0x00400100: 0x100, 0x00400200: 0x100}\n"
STUB_FP = ("def load_image():\n    return b'\\x90' * 0x400, (lambda f: f - 0x%X)\n" % BASE)
PAGE = "Area/page.md"


def rec(fns, text="does a thing"):
    return {"page": PAGE, "date": "2026-10-03", "session": "test", "mode": "",
            "rows": [{"fn": f, "text": text, "anchors": [["%08X" % (int(f, 16) + 4), "nop"], ["%08X" % (int(f, 16) + 9), "nop"]]}
                     for f in fns]}


def setup(root, applier):
    db = os.path.join(root, "FFXII TZA")
    kit = os.path.join(root, "Tools", "analysis-kit", "gfz-scripts")
    os.makedirs(kit)
    io.open(os.path.join(kit, "check_dispositions.py"), "w").write(STUB_CD)
    io.open(os.path.join(kit, "family_prover.py"), "w").write(STUB_FP)
    os.makedirs(os.path.join(db, "Area"))
    io.open(os.path.join(db, *PAGE.split("/")), "w", newline="\n").write("# Page\n\nText.\n")
    for name in ("rec-a", "rec-b"):
        d = os.path.join(db, "_index", "candidates", name)
        os.makedirs(d)
        shutil.copy(applier, os.path.join(d, "interior_applier.py"))
    return db


def put(db, name, cfg):
    json.dump(cfg, io.open(os.path.join(db, "_index", "candidates", name, "rows.json"), "w", encoding="utf-8"))


def run(db, name):
    r = subprocess.run([sys.executable, "-B", "interior_applier.py", "--apply"],
                       cwd=os.path.join(db, "_index", "candidates", name), capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip().splitlines()
    return [l for l in out if not l.startswith("VERIFY") and not l.startswith("FAILS")], r.returncode


def page(db):
    return io.open(os.path.join(db, *PAGE.split("/")), encoding="utf-8").read()


def main():
    fails = 0
    arg = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
    applier = arg("--applier", os.path.join(REC, "interior_applier_fixed.py"))
    control = arg("--control", os.path.join(REC, "interior_applier_prefix.py"))
    A, B = rec(["00400000", "00400100"]), rec(["00400200"])

    def case(name, ok, detail=""):
        nonlocal fails
        print("%s %s%s" % ("PASS" if ok else "FAIL", name, (" - " + detail) if detail and not ok else ""))
        fails += not ok

    with tempfile.TemporaryDirectory() as root:
        db = setup(root, applier)
        put(db, "rec-a", A)
        put(db, "rec-b", B)
        ra, _ = run(db, "rec-a")
        rb, _ = run(db, "rec-b")
        t = page(db)
        miss = CR.missing_rows(A, t) + CR.missing_rows(B, t)
        case("T1 two records, one page: both PATCHED, all rows present",
             ra[:1] == ["PATCHED"] and rb[:1] and rb[0].startswith("PATCHED") and not miss, "%s %s %s" % (ra, rb, miss))
        ra2, _ = run(db, "rec-a")
        rb2, _ = run(db, "rec-b")
        case("T2 re-run: ALREADY, page unchanged", ra2 == ["ALREADY"] and rb2 == ["ALREADY"] and page(db) == t,
             "%s %s" % (ra2, rb2))
        put(db, "rec-a", rec(["00400000", "00400100"], text="does a corrected thing"))
        ra3, _ = run(db, "rec-a")
        t3 = page(db)
        case("T3 corrected A: REWRITTEN, B untouched",
             ra3 == ["REWRITTEN"] and "does a corrected thing" in t3 and not CR.missing_rows(B, t3), "%s" % ra3)
        put(db, "rec-a", rec(["00400000"], text="does a corrected thing"))
        ra4, rc4 = run(db, "rec-a")
        case("T4 rewrite that would drop a row: REFUSED, page unchanged",
             ra4[:1] and ra4[0].startswith("REFUSED") and rc4 == 1 and page(db) == t3, "%s rc=%s" % (ra4, rc4))

    if control:
        with tempfile.TemporaryDirectory() as root:
            db = setup(root, control)
            put(db, "rec-a", A)
            put(db, "rec-b", B)
            run(db, "rec-a")
            run(db, "rec-b")
            lost = CR.missing_rows(A, page(db))
            case("C1 control: the pre-fix applier loses A's rows", len(lost) == 2, "lost %s" % lost)
    print("FAILS %d" % fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
