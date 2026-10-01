"""test_sn1_prereq.py - OPUS (Claude Opus 5.5), 2026-09-28. FRONTIER-REQ-OPUS-SN1-NEITHER-PARTITION-PREREQ.

Runs the ACTUAL caller, `python sn1_neither_partition.py`, as a subprocess on a fresh copy of this folder's .py files,
once valid and once per broken prerequisite. The copy is broken by an exact text edit whose anchor must occur exactly
once (an edit that does not apply is a test ERROR, never a pass).

  V   valid copy: exit 0, 'PASS  P', and the partition lines N A E L U Z C byte-equal (CR stripped) to the original
      publication's sn1_neither_partition.out at 2c7d810c8
  F1  FRONTIER's control: mapctrl's T0 count 127 -> 126 in the producer's check T (producer FAILS 1 / exit 1)
  F2  producer file missing
  F3  producer truncated mid-file (does not run)
  F4  producer prints FAIL T, then 'FAILS 0' and exits 0 (a lying exit)
  F5  producer's check X disabled (its check set changed)
  F6  producer runs clean but no longer defines SBN
  F7  producer prints an extra non-check line
  F8  sn1_q0_domain.py fails (FAILS 1 / exit 1): the producer itself must FAIL Q, and the wrapper must refuse
  F9  sn1_q0_domain.py missing
  F10 producer exits 0 without printing anything
Every F case must give: exit code 1, a 'FAIL  P' line, no 'PASS  N' line and no 'FAILS 0' line.
Usage: python test_sn1_prereq.py [source folder]   (default: this folder; another folder holding the same .py files, e.g. the
       pre-repair versions, tests those instead - the pre-repair wrapper and producer fail F1..F10)
"""
import glob, os, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else HERE
ROOT = subprocess.check_output(["git", "-C", HERE, "rev-parse", "--show-toplevel"], text=True).strip()
ORIG = subprocess.check_output(["git", "-C", ROOT, "show", "2c7d810c8:Database/FFXII TZA/_index/candidates/sn1-layouts/sn1_neither_partition.out"],
                               text=True, encoding="utf-8").replace("\r", "").splitlines()
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))

def edit(d, fn, old, new):
    p = os.path.join(d, fn); s = open(p, encoding="utf-8").read()
    if s.count(old) != 1:
        raise RuntimeError("anchor %r occurs %d times in %s" % (old[:50], s.count(old), fn))
    open(p, "w", encoding="utf-8", newline="").write(s.replace(old, new))

TAIL = 'print("FAILS %d" % fails)\nsys.exit(1 if fails else 0)'
VB, Q0 = "sn1_variable_binding.py", "sn1_q0_domain.py"
def f1(d): edit(d, VB, "[56, 92, 115, 127]", "[56, 92, 115, 126]")
def f2(d): os.remove(os.path.join(d, VB))
def f3(d):
    p = os.path.join(d, VB); s = open(p, encoding="utf-8").read(); open(p, "w", encoding="utf-8").write(s[:len(s) // 2])
def f4(d): f1(d); edit(d, VB, TAIL, 'print("FAILS 0")\nsys.exit(0)')
def f5(d): edit(d, VB, 'check("X", ', '(lambda *a: None)(')
def f6(d): edit(d, VB, TAIL, "del SBN\n" + TAIL)
def f7(d): edit(d, VB, TAIL, 'print("note: extra line")\n' + TAIL)
def f8(d): edit(d, Q0, TAIL, 'fails += 1\n' + TAIL)
def f9(d): os.remove(os.path.join(d, Q0))
def f10(d): edit(d, VB, 'MODS = ("ctrl", "btlctrl", "evctrl", "mapctrl")', 'sys.exit(0)\nMODS = ("ctrl", "btlctrl", "evctrl", "mapctrl")')
CASES = [("V", None), ("F1", f1), ("F2", f2), ("F3", f3), ("F4", f4), ("F5", f5), ("F6", f6), ("F7", f7), ("F8", f8), ("F9", f9), ("F10", f10)]

def run(d, script):
    r = subprocess.run([sys.executable, script], cwd=d, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, (r.stdout + r.stderr).replace("\r", "").splitlines()

for tag, brk in CASES:
    d = tempfile.mkdtemp(prefix="sn1prereq_")
    try:
        for f in glob.glob(os.path.join(SRC, "*.py")):
            if os.path.basename(f) != os.path.basename(__file__): shutil.copy(f, d)
        try:
            brk and brk(d)
        except Exception as e:
            check(tag, False, "ERROR applying the break: %s" % e); continue
        code, out = run(d, "sn1_neither_partition.py")
        p_line = next((l for l in out if l.startswith(("PASS  P", "FAIL  P"))), "(no P line)")
        if tag == "V":
            check(tag, code == 0 and p_line.startswith("PASS  P") and out[1:] == ORIG,
                  "valid: exit %d, %s; partition N..C equal to 2c7d810c8's .out: %s" % (code, p_line[:40], out[1:] == ORIG))
            continue
        ok = code == 1 and p_line.startswith("FAIL  P") and not any(l.startswith("PASS  N") for l in out) and "FAILS 0" not in out
        extra = ""
        if tag == "F8":   # the direct caller of sn1_q0_domain.py must itself refuse
            c2, o2 = run(d, VB)
            q = next((l for l in o2 if l.startswith(("PASS  Q", "FAIL  Q"))), "(no Q line)")
            ok &= c2 == 1 and q.startswith("FAIL  Q") and not any(l.startswith("PASS  T") for l in o2)
            extra = "; producer alone: exit %d, %s" % (c2, q[:70])
        check(tag, ok, "exit %d, %s%s" % (code, p_line[:150], extra))
    finally:
        shutil.rmtree(d, ignore_errors=True)
print("source: %s" % ("this folder" if SRC == HERE else SRC))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
