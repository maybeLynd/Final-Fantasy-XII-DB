"""sn1_x_oeb.py - OPUS (Claude Opus 5.5), 2026-09-28. The OUT OF EVIDENCE BOUNDARY guard for SN-1's residue, q3's head
word X, per FRONTIER's ruling (OPUS-REQ-FRONTIER-SN1-X-RULING, batch-K-scope-rulings.md @58abf37c6). Parts 1-3 are
executed here; part 4 is a non-author signature (neither OPUS nor FABLE, who authored the negatives).

  P1  THE EXCLUDED ARTEFACT: the ATEL script compiler that emitted each module's .ebp / .dbg pair. The shipped .sbn source
      blocks name its environment: btlctrl, evctrl and mapctrl include headers through ${ATEL_HEADERPATH} (ctrl does not)
  P2  NO ADMITTED SOURCE CARRIES IT:
      (a) the certified image has no reader of the companions - sn1_residue_boundary.py B1 / B2 (no .dbg/.sbn/.msb name in
          the image; the ATEL sibling loader's size query returns -1 before any lookup), run as a checked prerequisite;
      (b) the archive ships only the writer's outputs: a walk of the extract finds no executable of any kind (no PE "MZ"
          with a valid "PE\\0\\0" header, no ELF), so no toolchain is present to read
  P3  THE NEGATIVES, EXECUTED as checked prerequisites (exit 0, exactly their PASS tags, then FAILS 0):
      sn1_q3_x_content.py (Q X G P B N C; its C recovers E in 50 of 50 with the same search), FABLE's x_negatives.py
      (N1 N2 N3 C) and sn1_q3_pagemap.py (M1 M2 X C)
  PC  CONTROL for P2(b): a planted PE and a planted ELF in a scratch directory are both found by the same walker
Not claimed: what X counts. The row's residue text stays: closed for the gate once signed, unanswered in fact.
Usage: python sn1_x_oeb.py [EXTRACT]
"""
import importlib.util, os, struct, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); CAND = os.path.dirname(HERE)
EXTRACT = sys.argv[1] if len(sys.argv) > 1 else "D:/FFXII_TZA_extract"
BIN = os.path.join(EXTRACT, "ps2data", "image", "ff12", "in", "bin")
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
_ps = importlib.util.spec_from_file_location("sn1_prereq", os.path.join(CAND, "sn1-layouts", "sn1_prereq.py"))
PR = importlib.util.module_from_spec(_ps); _ps.loader.exec_module(PR)
FABLE_LINE = __import__("re").compile(r"^(PASS|FAIL) (\S+)  ")   # x_negatives.py's fixed form: 'PASS N1  ...'
def run(rel, tags, line=None):
    p = os.path.join(CAND, rel); _, why = PR.run(p, [p], tags, (), **({"line": line} if line else {})); return why
# P1
mods = ("ctrl", "btlctrl", "evctrl", "mapctrl")
inc = {m: open(os.path.join(BIN, m + ".sbn"), "rb").read().count(b"${ATEL_HEADERPATH}") for m in mods}
check("P1", sum(v > 0 for v in inc.values()) == 3 and inc["ctrl"] == 0, "the .sbn sources of btlctrl, evctrl and mapctrl include through ${ATEL_HEADERPATH} (ctrl does not): %s" % inc)
# P2 (a)
why = run("sn1-layouts/sn1_residue_boundary.py", ("B1", "B2", "R1", "P"))
check("P2a", why is None, "prerequisite sn1_residue_boundary.py (no companion reader in the image): %s" % (why or "exit 0, PASS B1 B2 R1 P, FAILS 0"))
# P2 (b)
def walk(root):
    n, pe, elf = 0, [], []
    for dp, _, fs in os.walk(root):
        for f in fs:
            n += 1; p = os.path.join(dp, f)
            try:
                with open(p, "rb") as h: b = h.read(0x40)
                if b[:2] == b"MZ" and len(b) >= 0x40:
                    with open(p, "rb") as h:
                        h.seek(struct.unpack_from("<I", b, 0x3C)[0]); sig = h.read(4)
                    if sig == b"PE\0\0": pe.append(p)
                elif b[:4] == b"\x7fELF": elf.append(p)
            except (OSError, struct.error):
                continue
    return n, pe, elf
n, pe, elf = walk(EXTRACT)
check("P2b", n > 80000 and not pe and not elf, "%d files in the extract; PE executables %r; ELF files %r" % (n, pe[:3], elf[:3]))
with tempfile.TemporaryDirectory() as d:
    mz = bytearray(0x80); mz[:2] = b"MZ"; struct.pack_into("<I", mz, 0x3C, 0x40); mz[0x40:0x44] = b"PE\0\0"
    open(os.path.join(d, "planted.dll"), "wb").write(bytes(mz)); open(os.path.join(d, "planted.elf"), "wb").write(b"\x7fELF" + b"\0" * 60)
    pn, ppe, pelf = walk(d)
check("PC", pn == 2 and len(ppe) == 1 and len(pelf) == 1, "planted PE and ELF found: %d / %d" % (len(ppe), len(pelf)))
# P3
for tag, rel, tags, line in (("P3a", "sn1-layouts/sn1_q3_x_content.py", ("Q", "X", "G", "P", "B", "N", "C"), None),
                       ("P3b", "sn1-q3-page-map/x_negatives.py", ("N1", "N2", "N3", "C"), FABLE_LINE),
                       ("P3c", "sn1-q3-page-map/sn1_q3_pagemap.py", ("M1", "M2", "X", "C"), None)):
    why = run(rel, tags, line)
    check(tag, why is None, "prerequisite %s: %s" % (rel, why or "exit 0, PASS %s, FAILS 0" % " ".join(tags)))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
