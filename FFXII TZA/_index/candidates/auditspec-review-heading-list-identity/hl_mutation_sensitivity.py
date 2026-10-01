"""Does ASTRA's heading-list-identity discriminator actually refuse a mutated image?
ASTRA's controls re-decode a mutated instruction in isolation and compare the resulting operand
to the original (a != test on a value the control itself changed). This runs the checker's OWN
assertion pipeline over an in-memory mutated image instead: the SHA/prior-hash gates are disabled
(they would refuse any mutation before the discriminator is reached), everything else is the
committed check.py text. A sensitive discriminator must raise AssertionError on each mutant and
pass on the unmutated image (positive control). Also verifies the retained .bin members and
manifest hashes against an independent extraction.
"""
import hashlib, json, re, subprocess, sys, tempfile, os
from pathlib import Path
ROOT = Path.cwd()  # run from the repo root
D = ROOT / "Database/FFXII TZA/_experiments/evidence/heading-list-identity"
EXE = ROOT / "Database/Tools/work/exe/FFXII_TZA.exe"
PY = str(ROOT / "Collaboration/Tools/analysis/venv/Scripts/python.exe")
src = (D / "check.py").read_text(encoding="utf-8")
img = EXE.read_bytes()

# independent member checks
man = json.loads((D / "manifest.json").read_bytes())
for m in man["members"]:
    b = (D / m["path"]).read_bytes()
    print("member %-14s bytes %s sha %s" % (m["path"], len(b) == m["bytes"], hashlib.sha256(b).hexdigest() == m["sha256"]))
def fo(va):  # .text raw offset: .text RVA 0x1000 -> file 0x600 (PointerToRawData); asserted on known bytes below
    return va - 0x120000 - 0x1000 + 0x600
assert img[fo(0x3A949A):fo(0x3A949A) + 7].hex() == "488b05e75ab102", "offset map"
for va, name in ((0x3A8390, "003A8390.bin"), (0x43EF40, "0043EF40.bin")):
    b = (D / name).read_bytes()
    print("bin %s == image[%08X:+%d]: %s" % (name, va, len(b), img[fo(va):fo(va) + len(b)] == b))

patched = src
patched = patched.replace("assert sha(image) == EXPECTED_EXE", "pass  # auditor: sha gate off")
patched = patched.replace("assert bodies['003A9490']['sha256'] == retained['code_sha256']", "pass  # auditor")
patched = patched.replace("assert bodies['003B3CA0']['sha256'] == retained_publish['code_sha256']", "pass  # auditor")
patched = patched.replace("image = EXE.read_bytes()", "image = Path(os.environ['AUDIT_IMG']).read_bytes()")
patched = patched.replace("import hashlib\n", "import hashlib, os\n", 1)
patched = patched.replace("if '--write' in sys.argv", "if False")
assert patched.count("auditor") == 3
drv = Path(tempfile.gettempdir()) / "auditspec_hl_check_mut.py"
drv.write_text(patched, encoding="utf-8")

def run(label, edits, expect_fail):
    b = bytearray(img)
    for va, old, new in edits:
        o = fo(va)
        assert b[o:o + len(old)] == old, (label, hex(va))
        b[o:o + len(new)] = new
    p = Path(tempfile.gettempdir()) / "auditspec_hl_img.bin"
    p.write_bytes(bytes(b))
    r = subprocess.run([PY, "-B", str(drv)], cwd=str(ROOT), capture_output=True, text=True,
                       env=dict(os.environ, AUDIT_IMG=str(p)))
    failed = r.returncode != 0
    last = (r.stderr.strip().splitlines() or [""])[-1]
    print("%-34s rc=%d %s %s" % (label, r.returncode, "REFUSED" if failed else "passed",
                                 ("OK" if failed == expect_fail else "**UNEXPECTED**"), ) + ("  | " + last if failed else ""))

run("unmutated (positive control)", [], False)
# flag walker loads 02EBEF90 instead of 02EBEF88 (same length)
run("wrong root in flag walker", [(0x3A949A, bytes.fromhex("488b05e75ab102"), bytes.fromhex("488b05ef5ab102"))], True)
# flag walker node link +0x38 instead of +0x30
run("wrong node link in flag walker", [(0x3A94EE, bytes.fromhex("488b5b30"), bytes.fromhex("488b5b38"))], True)
# flag walker list head +0x110 instead of +0x118
run("wrong list head in flag walker", [(0x3A94D0, bytes.fromhex("488b9f18010000"), bytes.fromhex("488b9f10010000"))], True)
# update path root 02EBEF90
run("wrong root in update", [(0x3A83BD, bytes.fromhex("488b05c46bb102"), bytes.fromhex("488b05cc6bb102"))], True)
# update node link +0x38
run("wrong node link in update node", [(0x43EFB0, bytes.fromhex("488b5930"), bytes.fromhex("488b5938"))], True)
# flag walker holder filter byte +0x44 -> +0x45 (checker asserts it)
run("filter byte offset +0x45", [(0x3A94BD, bytes.fromhex("0fb65044"), bytes.fromhex("0fb65045"))], True)
# NOT asserted by the checker: filter type set (test al,0xfb -> test al,0xff) - shows scope of checker
run("filter type set changed (unasserted)", [(0x3A94C4, bytes.fromhex("a8fb"), bytes.fromhex("a8ff"))], False)
