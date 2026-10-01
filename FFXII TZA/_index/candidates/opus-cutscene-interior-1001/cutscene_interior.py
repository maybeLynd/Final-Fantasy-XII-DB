"""cutscene_interior.py - interior citations for the F-frontier functions that cutscene-name-slots-and-the-depth-of-field-sidecar.md
cited by entry only
(OPUS, 2026-10-01). Every body was read by hand from the certified image (retool.py dis with its '; ->' annotations); every
rip-relative address named in a sentence was resolved by that annotation. Nothing skipped. The rows live in rows.py beside this script.

Before writing, the script VERIFIES every anchor against the image: it must be an instruction boundary strictly inside its
function's extent (functions.tsv) and decode to the recorded mnemonic. Any mismatch -> FAILS, nothing written.
Then it appends one OPUS section to the page (byte-preserving, CRLF-aware, idempotent). Prints VERIFY lines,
PATCHED / ALREADY, FAILS n. Same pattern as opus-mapctrl-interior-1001/mapctrl_interior.py (the rows are in rows.py)."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
KIT = os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts"))
sys.path.insert(0, KIT)
sys.path.insert(0, HERE)
import check_dispositions as cd  # noqa: E402
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

P = os.path.join(DB, "99-Unresolved-Residual", "Cutscene-Asset-Slots", "cutscene-name-slots-and-the-depth-of-field-sidecar.md")
from rows import ROWS  # noqa: E402  (rows.py beside this script)
HEAD = ("## Interior citations for the entry-cited functions (OPUS, 2026-10-01)\n\n"
        "*The functions this page named only at their entry. Each was read from the certified image; the sentence states what "
        "the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. "
        "Verified by [`cutscene_interior.py`](../../_index/candidates/opus-cutscene-interior-1001/cutscene_interior.py): every "
        "anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*\n\n"
        "| function | size | what the body does | interior anchors |\n|---|---|---|---|\n")
fails = 0
sizes = cd.load_functions()
d, off = fp.load_image()
md = Cs(CS_ARCH_X86, CS_MODE_64)
for fn, text, anchors in ROWS:
    f = int(fn, 16)
    n = sizes.get(f)
    if not n:
        print("VERIFY FAIL %s: not a function entry" % fn); fails += 1; continue
    ins = {i.address: i.mnemonic for i in md.disasm(d[off(f):off(f) + n], f)}
    for a, mn in anchors:
        av = int(a, 16)
        if not (f < av < f + n):
            print("VERIFY FAIL %s: anchor %s outside the body" % (fn, a)); fails += 1
        elif ins.get(av) != mn:
            print("VERIFY FAIL %s: %s decodes to %r, recorded %r" % (fn, a, ins.get(av), mn)); fails += 1
    if "|" in text:
        print("VERIFY FAIL %s: pipe in text" % fn); fails += 1
print("VERIFY %d functions, %d anchors" % (len(ROWS), sum(len(r[2]) for r in ROWS)))
if not fails:
    body = HEAD + "".join("| `%s` | %d B | %s | %s |\n" % (fn, sizes[int(fn, 16)], text, ", ".join("`%s`" % a for a, _m in anchors))
                          for fn, text, anchors in ROWS)
    b = open(P, "rb").read()
    crlf = b"\r\n" in b[:4000]
    s = body.encode("utf-8")
    if crlf:
        s = s.replace(b"\n", b"\r\n")
    if HEAD.splitlines()[0].encode("utf-8") in b:
        print("ALREADY")
    else:
        nl = b"\r\n" if crlf else b"\n"
        b = b.rstrip(b"\r\n") + nl + nl + s
        open(P, "wb").write(b)
        print("PATCHED")
print("FAILS", fails)
sys.exit(1 if fails else 0)
