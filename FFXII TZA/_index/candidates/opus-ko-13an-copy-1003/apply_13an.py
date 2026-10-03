"""apply_13an.py [--apply] - CONTRACT-auto-status-rebuild section 13an restated EXP-231's 0030EDA0 snapshot copy as
0x480 bytes to obj+0x730; the bytes copy 0x4F0 bytes to [obj+0x6B0, obj+0xBA0) (OPUS, 2026-10-03, on
ASTRA-REQ-OPUS-UQ147-KO-RELEASE-PARTITION-1003 after SWE2-AUDIT-SPEC's ACCEPT; SWE2-ORACLE corrected EXP-231 itself
and section 13g in c03ad4d97). Strikes the old span in place and states the correction beside it. Refuses unless the
contract is clean; idempotent (ALREADY). Prints FAILS n."""
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.normpath(os.path.join(HERE, "..", "..", "..", "10-Status-Periodic-Terminal", "CONTRACT-auto-status-rebuild.md"))
OLD = "  `q[obj+0xB88]`→`obj+0x730` (0x480) → `q[obj] &="
NEW = ("  `q[obj+0xB88]`→~~`obj+0x730` (0x480)~~ `obj+0x6B0` (0x4F0: `0030EDA7 add rcx,0x6b0`, 9×0x80 then a "
       "0x70-byte tail; *corrected 2026-10-03, OPUS, on ASTRA's SPEC-accepted `uq147-ko-release-partition` - record "
       "`opus-ko-13an-copy-1003`*) → `q[obj] &=")
b = io.open(P, encoding="utf-8", newline="").read()
if NEW in b:
    print("ALREADY")
    print("FAILS 0")
    sys.exit(0)
fails = 0
if b.count(OLD) != 1:
    print("the old 13an line occurs %d times (need exactly 1)" % b.count(OLD))
    fails += 1
d = subprocess.run(["git", "-C", os.path.dirname(P), "diff", "--quiet", "--", os.path.basename(P)])
if d.returncode != 0:
    print("REFUSED: the contract has uncommitted changes (another lane's?)")
    fails += 1
if fails or "--apply" not in sys.argv:
    print("DRY" if not fails else "")
    print("FAILS %d" % fails)
    sys.exit(1 if fails else 0)
tmp = P + ".opus-tmp"
io.open(tmp, "w", encoding="utf-8", newline="").write(b.replace(OLD, NEW, 1))
os.replace(tmp, P)
print("APPLIED")
print("FAILS 0")
