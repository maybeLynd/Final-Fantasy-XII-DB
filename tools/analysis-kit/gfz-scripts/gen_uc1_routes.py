"""gen_uc1_routes.py - finds the unlisted blocks whose start is referenced and 16-byte aligned - UC-1's floor.

PUBLISHED INTO THE KIT 2026-09-14 from `Tools/work/OPUS/uc1_routes.py`, which `.gitignore` excludes.
A canonical candidates file under `_index/candidates/` named it in its header, so the instruction
for reproducing a file this corpus cites pointed at a tool no peer had. Found by extending
`check_cited_instruments.py` to side files - it had been closed over `_index/*.md` and the kit's own
`*.py` and was blind to `.tsv` entirely.

THE BODY BELOW IS THE ORIGINAL, UNCHANGED. Rewriting its paths and defaults while publishing it
would mean the tool in the kit is not the tool that produced the file beside it, and seeing how the
rows were derived is the whole reason for publishing. The only addition is the two lines under this
docstring, which resolve the repository root from `__file__` and change into it so the tool's
repo-relative paths mean what they have always meant, from any working directory.

NAMED `gen_*`, NOT `check_*`: `run_gates.py` globs `check_*.py`, and a generator under that prefix
would run as a gate every suite and rewrite its own output as a side effect of auditing.
"""
import os as _os
import sys as _sys

# The repository root, four levels above this file: gfz-scripts -> analysis-kit -> Tools -> Database
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.dirname(
    _os.path.dirname(_os.path.abspath(__file__)))))))

# The original module docstring, kept verbatim:
# uc1_routes.py - split the UC-1 `referenced` signal by route, and control it on listed bodies.
#
# WHY: unlisted_admissions.py builds `referenced` as a union of three routes, and route 1 is the
# PE exception directory. FINAL-AUDIT-PROTOCOL pass 6 bans .pdata / .xdata / unwind data as
# supporting evidence. A block admitted because .pdata announces a range is admitted on banned
# evidence, so the union has to be decomposed before any of it carries a disposition.
#
# Routes, kept apart:
#   1  exception directory  (BANNED as evidence - measured here only to show what it contributes)
#   2  rel32 call/jmp targets and RIP-relative lea targets decoded out of .text
#   3  base relocation DIR64 targets
#
# Run from the repo root.

import io, os, re, struct, collections

IMAGE = 0x120000
EXE = r"Database\Tools\work\exe\FFXII_TZA.exe"
ADM = "Database/FFXII TZA/99-Unresolved-Residual/Unlisted-Code/unlisted-body-admissions.tsv"
FTS = r"Database\Tools\work\graph\functions.tsv"

d = io.open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
optsz = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
o = pe + 24 + optsz
for _ in range(nsec):
    name = d[o:o + 8].rstrip(b"\0").decode()
    vsz, va, rsz, rptr = struct.unpack_from("<IIII", d, o + 8)
    secs.append((name, va, vsz, rptr, rsz))
    o += 40


def off(va):
    r = va - IMAGE
    for _n, sva, vsz, rptr, rsz in secs:
        if sva <= r < sva + max(vsz, rsz):
            return rptr + (r - sva)
    return None


magic = struct.unpack_from("<H", d, pe + 24)[0]
ddoff = pe + 24 + (112 if magic == 0x20B else 96)

# route 1 - exception directory (BANNED as evidence)
r1 = set()
exc_rva, exc_sz = struct.unpack_from("<II", d, ddoff + 3 * 8)
po = off(IMAGE + exc_rva)
if po is not None:
    for k in range(exc_sz // 12):
        b, e, _u = struct.unpack_from("<III", d, po + k * 12)
        if b or e:
            r1.add(IMAGE + b)

# route 2 - rel32 call/jmp and RIP-relative lea decoded out of .text
r2 = set()
text = next((s for s in secs if s[0] == ".text"), None)
_n, tva, _vs, tpr, trs = text
for k in range(tpr, tpr + trs - 5):
    if d[k] in (0xE8, 0xE9):
        r2.add(IMAGE + tva + (k - tpr) + 5 + struct.unpack_from("<i", d, k + 1)[0])
for k in range(tpr, tpr + trs - 8):
    if d[k] in (0x48, 0x4C) and d[k + 1] == 0x8D and (d[k + 2] & 0xC7) == 0x05:
        r2.add(IMAGE + tva + (k - tpr) + 7 + struct.unpack_from("<i", d, k + 3)[0])

# route 3 - base relocation DIR64 targets
r3 = set()
rel_rva, rel_sz = struct.unpack_from("<II", d, ddoff + 5 * 8)
ro = off(IMAGE + rel_rva)
if ro is not None:
    p = ro
    while p < ro + rel_sz:
        page, sz = struct.unpack_from("<II", d, p)
        if sz == 0:
            break
        for q in range(p + 8, p + sz, 2):
            e = struct.unpack_from("<H", d, q)[0]
            if e >> 12 == 10:
                o2 = off(IMAGE + page + (e & 0xFFF))
                if o2 is not None:
                    r3.add(struct.unpack_from("<Q", d, o2)[0])
        p += sz

clean = r2 | r3
print("reference routes")
print("  1 exception directory (BANNED) : %7d targets" % len(r1))
print("  2 call/jmp/lea in .text        : %7d" % len(r2))
print("  3 base relocations (DIR64)     : %7d" % len(r3))
print("  clean union (2|3)              : %7d" % len(clean))

# admitted bodies
rows, hdr = [], None
for l in io.open(ADM, encoding="utf-8", errors="replace"):
    if l.startswith("#"):
        continue
    p = l.rstrip("\n").split("\t")
    if hdr is None:
        hdr = p
        continue
    rows.append(p)
i = {n: k for k, n in enumerate(hdr)}
body = [r for r in rows if r[i["verdict"]] == "body"]

ref_yes = [r for r in body if r[i["referenced"]] == "yes"]
only1 = [r for r in ref_yes if int(r[i["start_va"]], 16) not in clean]
keep = [r for r in ref_yes if int(r[i["start_va"]], 16) in clean]
print("\nadmitted `body` rows: %d" % len(body))
print("  referenced (union, as published)      : %d" % len(ref_yes))
print("  still referenced WITHOUT .pdata       : %d" % len(keep))
print("  referenced ONLY by .pdata (banned)    : %d" % len(only1))

trip = [r for r in body
        if int(r[i["start_va"]], 16) in clean
        and r[i["decodes_to_end"]] == "yes" and r[i["aligned16"]] == "yes"]
print("\nTHREE AGREEING SIGNALS, .pdata excluded")
print("  referenced(2|3) + decodes_to_end + aligned16 : %d blocks, %d bytes"
      % (len(trip), sum(int(r[i["bytes"]]) for r in trip)))

# CONTROL: how do LISTED bodies score on the same signals?
fh = io.open(FTS, encoding="utf-8", errors="replace")
head = fh.readline().rstrip("\n").split("\t")
j = {n: k for k, n in enumerate(head)}
listed = []
for ln in fh:
    q = ln.rstrip("\n").split("\t")
    if q and re.fullmatch(r"[0-9A-Fa-f]{8}", q[0]):
        try:
            listed.append((int(q[0], 16), int(q[j["body_bytes"]])))
        except ValueError:
            pass
print("\nCONTROL over %d LISTED bodies (known-true), same signals:" % len(listed))
lr = sum(1 for va, _n in listed if va in clean)
la = sum(1 for va, _n in listed if va % 16 == 0)
lb = sum(1 for va, _n in listed if va in clean and va % 16 == 0)
print("  referenced by route 2|3 : %6d  (%.1f %%)" % (lr, 100.0 * lr / len(listed)))
print("  16-byte aligned         : %6d  (%.1f %%)" % (la, 100.0 * la / len(listed)))
print("  both                    : %6d  (%.1f %%)" % (lb, 100.0 * lb / len(listed)))
lp = sum(1 for va, _n in listed if va in r1)
print("  announced by .pdata     : %6d  (%.1f %%)" % (lp, 100.0 * lp / len(listed)))
