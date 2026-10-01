"""Check 24, extended to INSTRUMENT retractions rather than content corrections.

Check 24 asks: for every correction ever made, was every downstream citer reopened? As run, it
followed CONTENT corrections - a claim about an address changed, so find the pages citing that
address. Today showed a second kind.

On 2026-09-15 the UI page retracted a conclusion and named the METHOD that produced it: an
address-based sweep cannot see a reference formed as image-base + file-offset. On 2026-09-18 the
step-table page made an absence claim resting on exactly that sweep, and it was wrong. Nothing
cites an address in common; the dependency is on the INSTRUMENT. Check 24 as run could not have
found it, because a method retraction has no citers to enumerate - it has USERS, and they are
invisible until someone tests them.

So: enumerate the database's absence claims that name an address, and test every address with
the instrument the retraction says is missing. Any hit is a page still resting on an overturned
method.

A claim qualifies if its sentence carries absence language - "no reference", "zero references",
"never materialised", "occurs zero times", "not referenced", "no caller", "unreferenced" - and a
VA in the same line or the line before. That is deliberately broad: a false positive costs one
lookup, a false negative is the failure this exists to catch.
"""
import collections
import io
import os
import re
import struct
import subprocess
import sys

DB = "C:/Users/Kristian/source/repos/XIIOnline/Database/FFXII TZA"
K = "C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/analysis-kit/gfz-scripts"
sys.path.insert(0, K)
os.chdir(DB)

ABS = re.compile(r"no (static )?(reference|caller|reader|writer|user|lea)|zero (references|times|"
                 r"occurrences)|never materiali|not referenced|unreferenced|occurs zero|"
                 r"appears zero|no shipped (recipe|user)|reached by (neither|no)", re.I)
VA = re.compile(r"\b(0x0?[0-9A-Fa-f]{7,8}|0[0-9A-F]{7})\b")

EXE = "C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/work/exe/FFXII_TZA.exe"
raw = open(EXE, "rb").read()
pe = struct.unpack_from("<I", raw, 0x3C)[0]
ns = struct.unpack_from("<H", raw, pe + 6)[0]
opt = struct.unpack_from("<H", raw, pe + 20)[0]
ib = struct.unpack_from("<Q", raw, pe + 24 + 24)[0]
off, secs = pe + 24 + opt, []
for _ in range(ns):
    nm = raw[off:off + 8].rstrip(b"\x00").decode("latin1")
    vs, va, rs, pr = struct.unpack_from("<IIII", raw, off + 8)
    secs.append((nm, ib + va, vs, rs, pr))
    off += 40


def sect(x):
    for nm, va, vs, rs, pr in secs:
        if va <= x < va + vs:
            return nm


# the set of addresses reachable image-base-relatively, computed once
sys.argv = ["x"]
import member_reach_scan as M
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP
TVA, TVS, TPR = next((ib + va, vs, pr) for nm, va, vs, rs, pr in secs if nm == ".text")
blob = raw[TPR:TPR + TVS]
fsizes, names = M.load_funcs()
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True
reach = collections.defaultdict(list)
for fn in sorted(fsizes):
    o = fn - TVA
    if not (0 <= o < len(blob)):
        continue
    for i in md.disasm(blob[o:o + fsizes[fn]], fn):
        for op in i.operands:
            if op.type != X86_OP_MEM or op.mem.base == X86_REG_RIP:
                continue
            if not op.mem.base and not op.mem.index:
                continue
            if op.mem.disp <= 0:
                continue
            va = ib + op.mem.disp
            s = sect(va)
            if s and s != ".text":
                reach[va].append((fn, i.address, "%s %s" % (i.mnemonic, i.op_str),
                                  bool(op.mem.index)))
print("addresses reachable image-base-relatively: %d" % len(reach))
print()

claims = []
for root, _, files in os.walk("."):
    if "/." in root.replace("\\", "/"):
        continue
    for fnm in files:
        if not fnm.endswith(".md"):
            continue
        p = os.path.join(root, fnm)
        try:
            lines = io.open(p, encoding="utf-8", errors="replace").read().split("\n")
        except OSError:
            continue
        for n, l in enumerate(lines):
            if not ABS.search(l):
                continue
            ctx = l + " " + (lines[n - 1] if n else "")
            for m in VA.finditer(ctx):
                v = int(m.group(1), 16)
                if 0x00120000 <= v < 0x03100000:
                    claims.append((p, n + 1, v, l.strip()[:110], l))

seen = set()
uniq = []
for c in claims:
    if (c[0], c[2]) in seen:
        continue
    seen.add((c[0], c[2]))
    uniq.append(c)
print("absence-style claims naming a VA: %d (over %d page(s))"
      % (len(uniq), len({c[0] for c in uniq})))
print()
# A CLAIM THAT ALREADY CARRIES ITS OWN CORRECTION IS NOT A LIVE GAP. Pages preserve the
# original wording beside the repair - CA-1 still reads "Two searches found no reader" and then
# "ANSWERED - CORRECTED 2026-09-12 (FABLE)" in the same row - so matching absence language alone
# re-reports work already done. Check 24 asks whether citers were REOPENED, and a row carrying
# its own retraction IS reopened.
REPAIRED = re.compile(r"ANSWERED|CORRECTED|OVERTURNED|REFUTED|RETRACTED|~~|SUPERSEDED", re.I)
# TEST THE FULL LINE, NOT THE DISPLAY TRUNCATION. c[3] is cut at 110 characters and a
# row's 'ANSWERED - CORRECTED' clause routinely sits past that, so filtering on the
# truncation re-reported CA-1 - a question answered on 2026-09-12 - as a live gap.
live = [c for c in uniq if not REPAIRED.search(c[4])]
print("of those, already carrying their own correction (not a gap): %d"
      % (len(uniq) - len(live)))
print("LIVE absence claims naming a VA: %d" % len(live))
print()
# A LOG OR AN INBOX IS A HISTORICAL RECORD, NOT A LIVE CLAIM. AUDIT-LOG.md preserves what was
# believed on the day and _index/_inbox/* are agent mailboxes; neither is a subject page a
# reconstruction would read, and "repairing" them would falsify the record. Check 24 is about
# documents that still REST on an overturned claim.
HIST = re.compile(r"_inbox/|AUDIT-LOG|COVERAGE\.md|ABSENCE-CLAIM-CLASSIFICATION")
subj = [c for c in live if not HIST.search(c[0].replace("\\", "/"))]
print("of the live ones, in a log or inbox (historical, not a live claim): %d"
      % (len(live) - len(subj)))
hit = [c for c in subj if c[2] in reach]
print("LIVE CLAIMS WHOSE ADDRESS IS REACHABLE BY THE IMAGE-BASE IDIOM: %d" % len(hit))
for p, n, v, l, _full in hit:
    r = reach[v]
    print("   %08X  %s:%d" % (v, p.replace("\\", "/")[2:], n))
    print("      claim : %s" % l)
    print("      reached: %d site(s), e.g. %08X in %s%s"
          % (len(r), r[0][1], names.get(r[0][0], "%08X" % r[0][0]),
             "   [INDEXED - reaches a range, not one address]" if r[0][3] else ""))
if not hit:
    print("   none")
