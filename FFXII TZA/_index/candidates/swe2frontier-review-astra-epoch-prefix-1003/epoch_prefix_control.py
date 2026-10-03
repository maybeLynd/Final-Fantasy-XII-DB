"""epoch_prefix_control.py - SWE2-FRONTIER review control for ASTRA-REQ-FRONTIER-PUBLICATION-EPOCH-PREFIX-1002 (2026-10-03).

Pins the reviewed helper (sha256 7d18f9c5...) and its preimage (4a99d95a...), extracts the ASTRA.md as-of prefix line
from each, and evaluates it against synthetic boards. Expected: the preimage emits "epoch3" whatever the board says
(the original false-epoch defect); the fixed line follows b['recovery_epoch'] and b['revision'] (3, 4, 7 and a
non-default revision all appear verbatim), and neither the fixed line nor the rest of the fixed helper carries a
literal epoch3/epoch4 prefix. Also checks prepare() runs team.board_status() before it reads the board it prints.
Prints FAILS n.
"""
import hashlib, os, re, sys
WORK = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "Tools", "work"))
FIXED = (os.path.join(WORK, "_specw8", "prepare-residue-packet-publication.py"),
         "7d18f9c528d2ffbec110e3bd5ea3484366bf949979ec26984ad9ccfda3ef20fb")
PRE = (os.path.join(WORK, "ASTRA", "runtime-residue-method-retriage", "publication-epoch4-preimage.py"),
       "4a99d95a679d6b5e9eb4a13f47abf4f78388c5f5d17f6de97125770c61978c42")
fails = 0
def check(ok, what):
    global fails
    print(("ok   " if ok else "FAIL ") + what); fails += (not ok)
def load(path, sha):
    raw = open(path, "rb").read()
    check(hashlib.sha256(raw).hexdigest() == sha, "pinned sha256 %s... for %s" % (sha[:8], os.path.basename(path)))
    return raw.decode("utf-8")
def prefix_line(src):
    ls = [l.strip() for l in src.splitlines() if "publication task '+id+'" in l and "board" in l]
    return ls[0] if len(ls) == 1 else None
fixed, pre = load(*FIXED), load(*PRE)
lf, lp = prefix_line(fixed), prefix_line(pre)
check(lf is not None and lp is not None, "exactly one as-of prefix line in each file")
ev = lambda line, b: eval(line, {"str": str}, {"b": b, "id": "T-1"})
for ep, rev in ((3, 100), (4, 48088), (7, 123456)):
    b = {"recovery_epoch": ep, "revision": rev}
    out = ev(lf, b)
    check(("epoch%d " % ep) in out and ("revision%d;" % rev) in out, "fixed line follows epoch %d revision %d: %r" % (ep, rev, out.strip()))
    outp = ev(lp, b)
    check(("epoch3" in outp) == True, "preimage line says epoch3 regardless (board epoch %d): %r" % (ep, outp.strip()))
check(not re.search(r"epoch[34]", lf), "fixed prefix line has no literal epoch3/epoch4")
check(not re.search(r"board (healthy|checked) epoch[0-9]", fixed), "no other hardcoded prefix epoch in the fixed helper")
# guard order inside prepare(): board_status must precede the board read that feeds the prefix
L = fixed.splitlines()
i0 = next(i for i, l in enumerate(L) if l.startswith("def prepare("))
i1 = next(i for i in range(i0 + 1, len(L)) if L[i].startswith("def "))
body = [(i, l) for i, l in enumerate(L[i0:i1], i0) if l.strip()]
st = [i for i, l in body if "team.board_status(team.BOARD)" in l]
rd = [i for i, l in body if "b=json.loads(team.BOARD.read_text())" in l]
pf = [i for i, l in body if "publication task '+id+'" in l]
check(len(st) == 1 and len(rd) == 1 and len(pf) == 1 and st[0] < rd[0] < pf[0], "prepare(): board_status -> board read -> prefix, in that order")
print("FAILS", fails)
sys.exit(1 if fails else 0)
