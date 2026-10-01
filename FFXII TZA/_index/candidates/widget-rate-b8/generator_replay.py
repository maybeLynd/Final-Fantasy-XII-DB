"""generator_replay.py - OPUS (Claude Opus 5.5), 2026-09-28. Fresh-input regression for widget_b8_rate.py's --patch generator
(ASTRA-REQ-OPUS-RATE-GENERATOR-POSTCONDITION; ASTRA's replay _experiments/evidence/widget-rate-template-replay/ showed the old
generator turning the legacy row into one its own S rejected).

Runs the REAL producer - widget_b8_rate.py's own source, with ONLY its FI path redirected to a temporary one-row fixture and
__file__ kept, so the certified-image lookup and hash guard are unchanged - on:
  P  a positive control: the current accepted row -> check exits 0
  L  the legacy row ('1.0f on every widget in the game', evidence without the QUALIFIED tag) -> --patch -> check exits 0, and the
     regenerated meaning AND evidence equal the accepted row's byte for byte
  I  the intermediate d9c76486b row (qualified, no FP limits) -> --patch -> check exits 0 and equals the accepted row
Nothing under _types is written; the fixture lives in a temporary directory.
Usage: python generator_replay.py [--src PRODUCER]   (--src runs another producer, e.g. the pre-repair e867536cf copy, which must FAIL L and I)
"""
import os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.abspath(sys.argv[sys.argv.index("--src") + 1]) if "--src" in sys.argv else os.path.join(HERE, "widget_b8_rate.py"); FIELDS = os.path.join(DB, "_types", "fields.tsv")
L = open(FIELDS, "rb").read().decode("utf-8").splitlines(keepends=True)
hdr = L[0]; row = next(l for l in L if l.split("\t")[0] == "Widget" and l.split("\t")[1] == "0x0B8")
cur = row.rstrip("\r\n").split("\t"); eol = row[len(row.rstrip("\r\n")):]
TAG = " || QUALIFIED 2026-09-28 (OPUS, _index/candidates/widget-rate-b8/widget_b8_rate.py R1 R2 M)"
LIMITS_AT = cur[5].index(" - all under a COMPLETED comparison"); LIMITS_END = cur[5].index(". Actual game rates are not established.")
legacy = list(cur); legacy[5] = "1.0f on every widget in the game"; legacy[8] = cur[8].replace(TAG, "")
mid = list(cur); mid[5] = cur[5][:LIMITS_AT] + cur[5][LIMITS_END:]
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
code = open(SRC, encoding="utf-8").read()
assert code.count('FI = os.path.join(DB, "_types", "fields.tsv")') == 1
with tempfile.TemporaryDirectory() as td:
    def run(cells, patch):
        fx = os.path.join(td, "fields.tsv"); open(fx, "wb").write((hdr + "\t".join(cells) + eol).encode("utf-8"))
        drv = os.path.join(td, "drv.py")
        open(drv, "w", encoding="utf-8").write("__file__ = %r\n" % os.path.join(HERE, "widget_b8_rate.py") + code.replace('FI = os.path.join(DB, "_types", "fields.tsv")', "FI = %r" % fx))
        rc_p = subprocess.run([sys.executable, drv, "--patch"], capture_output=True, text=True).returncode if patch else 0
        r = subprocess.run([sys.executable, drv], capture_output=True, text=True)
        return rc_p, r.returncode, open(fx, "rb").read().decode("utf-8").splitlines()[1].split("\t")
    p = run(cur, False); check("P", p[1] == 0 and p[2] == cur, "current accepted row: check exits 0, row untouched")
    l = run(legacy, True); check("L", l[0] == 0 and l[1] == 0 and l[2] == cur, "legacy row -> --patch -> accepted row exactly (meaning and evidence), check exits 0")
    i = run(mid, True); check("I", i[0] == 0 and i[1] == 0 and i[2] == cur, "d9c76486b row -> --patch -> accepted row exactly, check exits 0")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
