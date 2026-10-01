"""bq23_ordered_residue.py - BQ-23: the nine unmatched OrderedContainerRuntime members classified (FABLE, Claude Opus
5.5, 2026-09-27). Follows bq23-tier6/bq23_tier6.py, whose T4 predates SWE2-EC7's EASTL relabel; that receipt stays as run.
Static; upstream = EASTL rbtree (DoNukeSubtree / DoCopySubtree) and MSVC <xtree> (_Erase tests _Isnil at +0x19).

  V1 the relabel landed, extended: 25 members carry EASTL.OrderedContainerRuntime, 3 keep CxxStandardLibrary
     (the MSVC _Tree members 00712F60 / 0071E500 / 0079BA10), and the packed-colour pair carries
     Phyre.OrderedContainerRuntime. (Updated 2026-09-27 for FABLE-REQ-SWE2EC7-BQ23-RELABEL-AND-TWO-NOTES.)
  V2 seven are EASTL rbtree subtree routines on the EASTL node {right +0, left +8, parent +0x10, colour byte +0x18}:
     DoNukeSubtree 001FDA60 / 001FD9A0 / 001FDAC0 / 00200140 (recurse on [node+0], keep [node+8], free through the
     rbtree allocator's slot +0x18, loop to null); the inlined clear 001FC3A0 (the same loop from the root at +0x18,
     recursion through 001FDA60); DoCopySubtree 001FC770 / 001FF990 (allocate through slot +0x10 or DoCreateNode
     001FFAB0, recurse on the source's [+0], walk its [+8]).
  V3 two are a packed-colour tree - children +0 / +8, parent|colour at +0x10 with the colour in bit 0, key at node +0x18:
     005A7BF0 (insert; its caller 005A9560 builds and self-links array nodes, key filled by 005C5BC0) and 0067F9D0.
     That is the layout of Phyre's PRedBlackTreeNode as the class descriptor carries it (RTTI base at +8, the
     constructor self-links +8 / +0x10 / +0x18, PHashEntryConstKey at +0x20 = node +0x18). The claim is the node type,
     not that these trees hold descriptors.
  V4 sensitivity: the three MSVC _Tree members (00712F60, 0071E500, 0079BA10) fail the V2 shape.
Exit 1 on any FAIL.
"""
import re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]; W = ROOT / "Database/Tools/work"
d = (W / "exe/FFXII_TZA.exe").read_bytes(); BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
SIZES, LAB = {}, {}
for l in (W / "graph/functions.tsv").read_text(encoding="utf-8").splitlines()[1:]:
    q = l.split("\t")
    try: SIZES[int(q[0], 16)] = int(q[2]); LAB[int(q[0], 16)] = q[8] if len(q) > 8 else ""
    except (ValueError, IndexError): pass
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def body(f): return [("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(f):off(f) + SIZES[f]], f)]
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
e = sum("EASTL.OrderedContainerRuntime" in v for v in LAB.values()); c = sum("CxxStandardLibrary.OrderedContainerRuntime" in v for v in LAB.values())
p = sum("Phyre.OrderedContainerRuntime" in v for v in LAB.values())
check("V1 the relabel landed, extended (25 EASTL / 3 CxxStandardLibrary / 2 Phyre)", (e, c, p) == (25, 3, 2), "%d / %d / %d" % (e, c, p))
def nuke(f):
    b = body(f); me = "call %s" % hex(f)
    rec = any(t == me for t in b) or any(t == "call 0x1fda60" for t in b)
    return rec and any(re.fullmatch(r"mov r\w+, qword ptr \[r\w+ \+ 8\]", t) for t in b) \
        and any(t == "call qword ptr [rax + 0x18]" for t in b) and not any("0x19]" in t for t in b)
def copy(f):
    b = body(f)
    return any(t == "call %s" % hex(f) for t in b) and (any(t == "call qword ptr [rax + 0x10]" for t in b) or "call 0x1ffab0" in b) \
        and any(re.fullmatch(r"mov r\w+, qword ptr \[r\w+ \+ 8\]", t) for t in b)
N = [0x1FDA60, 0x1FD9A0, 0x1FDAC0, 0x200140, 0x1FC3A0]; C = [0x1FC770, 0x1FF990]
cc = body(0x1FC770)
check("V2 seven EASTL subtree routines (5 DoNukeSubtree-shaped incl. the inlined clear, 2 DoCopySubtree)",
      all(nuke(f) for f in N) and all(copy(f) for f in C) and "movzx ecx, byte ptr [rdi + 0x18]" in cc and "mov byte ptr [rbp + 0x18], cl" in cc,
      "nuke=%s copy=%s" % ([nuke(f) for f in N], [copy(f) for f in C]))
def packed(f):
    b = body(f)
    return any(re.fullmatch(r"movzx e\w+, byte ptr \[r\w+ \+ 0x10\]", t) for t in b) and any(re.fullmatch(r"and e\w+, 1", t) for t in b) \
        and any(re.fullmatch(r"(add|sub) (qword ptr \[r\w+ \+ 0x10\], r\w+|r\w+, qword ptr \[r\w+ \+ 0x10\])", t) for t in b)
ctor = body(0x632C90); a = body(0x5A7BF0)
import itertools
check("V3 005A7BF0 / 0067F9D0 use the packed-colour node (parent|colour at +0x10); 005A7BF0 keys on node +0x18; the "
      "descriptor ctor self-links its node at +8",
      packed(0x5A7BF0) and packed(0x67F9D0) and "mov edx, dword ptr [rax]" in a and "lea rax, [r9 + 0x18]" in a
      and "lea rax, [rcx + 8]" in ctor and "mov qword ptr [rax + 0x10], rax" in ctor)
check("V4 sensitivity: the MSVC _Tree members fail the EASTL shape",
      not any(nuke(f) or copy(f) for f in (0x712F60, 0x71E500, 0x79BA10) if f in SIZES), "")
print("FAILS", fails); sys.exit(1 if fails else 0)
