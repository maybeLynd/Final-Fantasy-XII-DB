"""generator_replay.py - OPUS (Claude Opus 5.5), 2026-09-28. Fresh-input regression for child_widget.py's --patch generator.

Runs the REAL producer - child_widget.py's source with ONLY its FIELDS path redirected to a temporary copy of a legacy
fields.tsv, and __file__ kept (certified-image lookup and hash guard unchanged) - then compares the five rows it writes
(Widget +0x68 / +0x70 / +0x74 / +0x78 and the MapScreenContainer +0xC0 region row) with the store's, byte for byte, and runs the
check on the regenerated file. The legacy input is the store before 22102235b:
    git show "22102235b^:./FFXII TZA/_types/fields.tsv" > legacy_fields.tsv
Usage: python generator_replay.py --legacy legacy_fields.tsv [--src PRODUCER]
"""
import os, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.abspath(sys.argv[sys.argv.index("--src") + 1]) if "--src" in sys.argv else os.path.join(HERE, "child_widget.py")
LEG = os.path.abspath(sys.argv[sys.argv.index("--legacy") + 1])
KEYS = {("Widget", "0x068"), ("Widget", "0x070"), ("Widget", "0x074"), ("Widget", "0x078"), ("MapScreenContainer", "0x00C0")}
def rows(path): return {tuple(l.split("\t")[:2]): l.split("\t") for l in open(path, "rb").read().decode("utf-8").splitlines() if tuple(l.split("\t")[:2]) in KEYS}
cur = rows(os.path.join(DB, "_types", "fields.tsv"))
code = open(SRC, encoding="utf-8").read(); T = 'FIELDS = os.path.join(DB, "_types", "fields.tsv")'
assert code.count(T) == 1
fails = 0
with tempfile.TemporaryDirectory() as td:
    fx = os.path.join(td, "fields.tsv"); shutil.copyfile(LEG, fx); drv = os.path.join(td, "drv.py")
    open(drv, "w", encoding="utf-8").write("__file__ = %r\n" % os.path.join(HERE, "child_widget.py") + code.replace(T, "FIELDS = %r" % fx))
    a = subprocess.run([sys.executable, drv, "--patch"], capture_output=True, text=True)
    b = subprocess.run([sys.executable, drv], capture_output=True, text=True)
    got = rows(fx)
    for k in sorted(KEYS):
        ok = got.get(k) == cur.get(k); fails += not ok
        print("%s  R %s %s regenerated == store" % ("PASS" if ok else "FAIL", k[0], k[1]))
    ok = a.returncode == 0 and b.returncode == 0; fails += not ok
    print("%s  C --patch rc %d, check on the regenerated file rc %d" % ("PASS" if ok else "FAIL", a.returncode, b.returncode))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
