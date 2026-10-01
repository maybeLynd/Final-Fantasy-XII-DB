"""sd80_82_trees.py - SD-80 (the fourteen profiled MSVC std::_Tree bodies, read) and SD-82 (single-direction EASTL
rotation copies, every body) (OPUS, 2026-09-30). Static, the certified image, via
Database/Tools/analysis-kit/gfz-scripts/retool.py and the dd-data-2 matcher's `pe` module.
"""
import difflib, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
import retool as T  # noqa: E402
import pe  # noqa: E402

R, SZ = T.R, T.sizes()
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def dis(f):
    return list(R.md.disasm(R.at(f, SZ[f]), f))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return "%s %s" % (i.mnemonic, i.op_str)


def norm(f, labels=True):
    """instructions with rip displacements masked, local branch targets as offsets (or 'L'), outside targets listed"""
    out, tg = [], []
    for i in dis(f):
        op = i.op_str
        if (i.mnemonic in ("call", "jmp") or i.mnemonic.startswith("j")) and op.startswith("0x"):
            t = int(op, 16)
            if 0 <= t - f < SZ[f]:
                op = ("L+%x" % (t - f)) if labels else "L"
            else:
                tg.append(t)
                op = "T"
        out.append(i.mnemonic + " " + re.sub(r"\[rip \+ 0x[0-9a-f]+\]", "[RIP]", op))
    return out, tg


# ---------------- SD-80 ----------------
# S1 - twelve of the fourteen are instruction-for-instruction the body of a sibling the page read (or this record reads),
#      differing only in call targets, and each target is the same-role body of its own instantiation (A / B / C)
SAME = [  # (read sibling, profiled body, the profiled body's targets in order)
    (0x00714B60, 0x00714BE0, [0x00714980, 0x00210EB0]),   # _Tidy (A)            -> A's subtree erase, free
    (0x00714B60, 0x00714C60, [0x00714980, 0x00210EB0]),   # _Tidy (A)
    (0x00714B60, 0x0079B0D0, [0x00799B80, 0x00210EB0]),   # _Tidy (C)            -> C's subtree erase
    (0x0079B930, 0x00714CE0, [0x00714B60, 0x00714DC0]),   # erase(first, last) A -> A's tidy, A's node erase
    (0x0079B930, 0x00715110, [0x00714BE0, 0x00714DC0]),
    (0x0079B930, 0x007151F0, [0x00714C60, 0x00714DC0]),
    (0x0079B930, 0x0071F4B0, [0x0071F3A0, 0x0071F590]),   # erase(first, last) B -> B's tidy, B's node erase
    (0x00714980, 0x00799B80, [0x00210EB0]),               # _Erase subtree (C)
    (0x00799BD0, 0x0071F240, []),                         # _Lrotate (A/B), same code as C's
]
ok, rows = True, []
for ref, f, want in SAME:
    a, _ = norm(ref)
    b, tb = norm(f)
    good = a == b and [t for t in tb if t != f] == want
    ok &= good
    rows.append("%08X=%08X%s" % (f, ref, "" if good else "(!)"))
check("S1", ok and len(SAME) == 9, "identical to a read sibling, own-instantiation targets: " + " ".join(rows))
# S2 - the two rotations, read: 0071F240 / 00799BD0 are _Lrotate (y = x->_Right at +0x10; x->_Right = y->_Left; the
#      parent (+8) relinked, root at head +8; y->_Left = x) and 00714B00 / 00799C30 _Rrotate (the mirror, y = x->_Left);
#      the _Isnil byte is +0x19
check("S2", txt(0x0071F240) == "mov r8, qword ptr [rdx + 0x10]" and txt(0x0071F244) == "mov rax, qword ptr [r8]"
      and txt(0x0071F247) == "mov qword ptr [rdx + 0x10], rax" and txt(0x0071F24E) == "cmp byte ptr [rax + 0x19], 0"
      and txt(0x0071F263) == "cmp rdx, qword ptr [rax + 8]" and txt(0x0071F26D) == "mov qword ptr [r8], rdx"
      and txt(0x00714B00) == "mov r8, qword ptr [rdx]" and txt(0x00714B03) == "mov rax, qword ptr [r8 + 0x10]"
      and norm(0x00714B00)[0] == norm(0x00799C30)[0],
      "0071F240 = _Lrotate, 00714B00 = 00799C30 = _Rrotate (node: _Left +0, _Parent +8, _Right +0x10, _Isnil +0x19)")
# S3 - the subtree erase, read: while the node is not nil, recurse on _Right (+0x10), step to _Left (+0), free; B's copy
#      0071F1E0 destroys the value (0071EE70 on node +0x20) before the free and is otherwise 00714980
a, _ = norm(0x00714980, False)
b, tb = norm(0x0071F1E0, False)
ops = [op for op in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes() if op[0] != "equal"]
check("S3", txt(0x0071498F) == "cmp byte ptr [rdx + 0x19], 0" and txt(0x007149A0) == "mov rdx, qword ptr [rbx + 0x10]"
      and txt(0x007149A7) == "call 0x714980" and txt(0x007149AC) == "mov rbx, qword ptr [rbx]" and txt(0x007149B2) == "call 0x210eb0"
      and [(o[0], b[o[3]:o[4]]) for o in ops] == [("insert", ["lea rcx, [rdi + 0x20]", "call T"])] and 0x0071EE70 in tb,
      "_Erase(subtree): recurse right, go left, free; B adds the value destructor 0071EE70(node + 0x20)")
# S4 - 0071EE70, read: pair<string, string>::~pair - the second string (+0x20) then the first (+0): when capacity
#      (+0x18) >= 0x10 the heap buffer is released (001DFA10, capacity + 1), then capacity = 15, size = 0, buffer[0] = 0
check("S4", txt(0x0071EE7A) == "mov r8, qword ptr [rcx + 0x38]" and txt(0x0071EE7E) == "lea rdi, [rcx + 0x20]"
      and txt(0x0071EE85) == "cmp r8, 0x10" and txt(0x0071EE94) == "call 0x1dfa10" and txt(0x0071EE99) == "mov qword ptr [rdi + 0x18], 0xf"
      and txt(0x0071EEB6) == "mov r8, qword ptr [rbx + 0x18]" and txt(0x0071EEC9) == "call 0x1dfa10"
      and txt(0x0071EECE) == "mov qword ptr [rbx + 0x18], 0xf",
      "0071EE70 = pair<string, string> destructor: +0x20 then +0x00, SSO threshold 16")
# S5 - 0079BA10 read whole: _Tree::erase(iterator) -> iterator. Successor first (right subtree's minimum, else climb);
#      unlink (successor spliced in place with the colours +0x18 swapped when both children exist); head's leftmost (+0) /
#      rightmost (+0x10) refreshed; if the erased colour is black (1) the fix-up loop recolours and rotates through
#      00799C30 / 00799BD0; the node is freed, the size (tree +8) decremented, the successor returned
check("S5", txt(0x0079BA1D) == "cmp byte ptr [r8 + 0x19], 0" and txt(0x0079BA5C) == "mov qword ptr [rsp + 0x50], r8"
      and txt(0x0079BBC2) == "movzx eax, byte ptr [rsi + 0x18]" and txt(0x0079BBCF) == "mov byte ptr [rsi + 0x18], cl"
      and txt(0x0079BBD2) == "cmp byte ptr [rsi + 0x18], 1" and txt(0x0079BCA9) == "call 0x799c30" and txt(0x0079BCCB) == "call 0x799bd0"
      and txt(0x0079BDA3) == "mov byte ptr [rdi + 0x18], 1" and txt(0x0079BDAA) == "call 0x210eb0"
      and txt(0x0079BDC7) == "dec rax" and txt(0x0079BDCA) == "mov qword ptr [r14 + 8], rax" and txt(0x0079BDD3) == "mov qword ptr [r15], rax",
      "0079BA10 = erase(iterator): successor, unlink, black fix-up with both rotations, free, --size, return successor")
# S6 - 0071F590 is 0079BA10 for pair B: the only differences are register allocation (three copies, two operands) and
#      one insertion, the value destructor call before the free
a, _ = norm(0x0079BA10, False)
b, _ = norm(0x0071F590, False)
ops = [op for op in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes() if op[0] != "equal"]
kinds = [(o[0], o[2] - o[1], o[4] - o[3]) for o in ops]
ins_ = [b[o[3]:o[4]] for o in ops if o[0] == "insert"]
check("S6", kinds == [("delete", 3, 0), ("replace", 1, 1), ("replace", 1, 1), ("insert", 0, 2)]
      and ins_ == [["lea rcx, [rsi + 0x20]", "call T"]],
      "0071F590 = 0079BA10 + the value destructor (differences: %s)" % kinds)

# ---------------- SD-82 ----------------
def qstores(fn):
    out = []
    for x in pe.dis(fn):
        m = re.match(r"qword ptr \[(\w+)(?: \+ (0x[0-9a-f]+|\d+))?\], \w+$", x.op_str)
        if x.mnemonic == "mov" and m:
            out.append(int(m.group(2), 0) if m.group(2) else 0)
    return out


def rot_hits(seq, first, last):
    n = 0
    for i in range(len(seq) - 4):
        if tuple(seq[i:i + 3]) == first:
            tail = seq[i + 3:i + 7]
            if any(tuple(tail[j:j + 2]) == last for j in range(len(tail) - 1)):
                n += 1
    return n


L = ((0, 0x10, 0x10), (8, 0x10))
Rt = ((8, 0x10, 0x10), (0, 0x10))
hits, big = {}, 0
for f, sz in pe.funcs.items():
    big += sz > 20000
    s = qstores(f)
    nl, nr = rot_hits(s, *L), rot_hits(s, *Rt)
    if nl or nr:
        hits[f] = (nl, nr)
print("   rotation-shaped bodies (no size cap, %d bodies, %d over 20,000 bytes):" % (len(pe.funcs), big))
for f in sorted(hits):
    print("      %08X  left-shaped %d  right-shaped %d" % ((f,) + hits[f]))
BOTH = {0x0016D840, 0x0016DA60, 0x0067F700, 0x0067F9D0}
EASTL_ROT = {0x0016D780, 0x0016D7E0}
single = sorted(f for f, (nl, nr) in hits.items() if not (nl and nr) and f not in EASTL_ROT)
check("B1", {f for f, (nl, nr) in hits.items() if nl and nr} == BOTH and big == 8
      and single == [0x00207DE0, 0x00712F60, 0x00714B00, 0x0071E500, 0x00799C30, 0x00820D00],
      "no size cap: both shapes only in the four known bodies; single-shape bodies %s" % ["%08X" % f for f in single])
# B2 - the single-shape bodies are not EASTL: four are MSVC-layout code (they test the _Isnil byte +0x19 and link the
#      parent at +8): the _Rrotate copies 00714B00 / 00799C30 and the inserts 00712F60 / 0071E500 (page section 3);
#      00207DE0 allocates a 0x30 record and links it (no rotation), 00820D00 pushes 16-byte stack slots and calls on
msvc = all(any(re.search(r"byte ptr \[\w+ \+ 0x19\], 0", i.op_str) for i in dis(f)) for f in (0x00714B00, 0x00799C30, 0x00712F60, 0x0071E500))
check("B2", msvc and txt(0x00207E2D) == "mov ecx, 0x30" and txt(0x00207E32) == "call 0x210ec0"
      and not any("0x19]" in i.op_str for i in dis(0x00207DE0))
      and txt(0x00820D26) == "lea rax, [r10 + 0x10]" and txt(0x00820D2A) == "mov qword ptr [rcx + 0x10], rax"
      and not any("0x19]" in i.op_str for i in dis(0x00820D00)),
      "single-shape hits: 4 MSVC-layout (_Isnil +0x19), 2 not tree code - no EASTL single-direction copy")
print("FAILS %d" % fails)
