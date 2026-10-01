"""RC-31: who parses menuquest.lst (qstl), and which header/directory fields are read (SWE2-DATA 2026-09-30), static.

The quest-list widget 0037F4D0 requests kind 7 0x128 (menuquest.dat) and 0x13A (menuquest.lst) and stores their
buffers at +0xC8 / +0xD0 of its object (0037F750 / 0037F778); the object is the singleton [02AED490].
L1 census: every function holding a raw rip reference to 02AED490 (pe.raw_rip_refs) is walked linearly; a register
   loaded from the global is tracked, then a register loaded from [that + 0xD0] (the .lst buffer), then every memory
   operand based on the .lst register is recorded with its displacement and width, and every lea off it.
L2 the lookup bodies are decoded by hand below (0037EFC0 and 0037E5B0's two probes): the loop bound, the compare, the
   0xFFFF sentinel, the dataOff read width and the directory +0x04 read.
L3 corpus: every shipped menuquest.lst is parsed with exactly the decoded lookup (first match in file order) and with
   a sorted-order lookup; the two must agree for every questId (ids are unique), so the shipped order does not matter.
Controls: C1 the census must find 0037EFC0 reading word +0xE and word +0x8 of the .lst; C2 the census must find the
.dat reader 0037E5B0 reading [+0xC8] (the sibling buffer) - the tracker sees the other field of the same object.
"""
import os, re, struct, sys, glob, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe import d, off, owner, dis, raw_rip_refs, u32, names  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


G = 0x02AED490
refs = raw_rip_refs(G, G + 8)
fns = sorted({owner(a) for a, *_ in refs if owner(a)})
print("L1 raw rip references to %08X: %d sites in %d listed functions (+%d unlisted sites)" %
      (G, len(refs), len(fns), sum(1 for a, *_ in refs if not owner(a))))

R64 = {"eax": "rax", "ebx": "rbx", "ecx": "rcx", "edx": "rdx", "esi": "rsi", "edi": "rdi", "ebp": "rbp", "esp": "rsp"}
for i in range(8, 16):
    R64["r%dd" % i] = "r%d" % i


def c64(r):
    return R64.get(r, r)


def rip_t(x):
    m = re.search(r"\[rip ([+-]) 0x([0-9a-f]+)\]", x.op_str)
    if not m:
        return None
    v = int(m.group(2), 16)
    return x.address + x.size + (v if m.group(1) == "+" else -v)


w = {x.address: x for x in dis(0x0037F4D0)}
check("L0 the widget object IS the singleton: 0037F614 stores the widget (rbx) to 02AED490, 0037F51E clears it",
      rip_t(w[0x0037F614]) == G and w[0x0037F614].op_str.endswith("rbx") and rip_t(w[0x0037F51E]) == G)
callees = sorted({int(x.op_str, 16) for x in w.values() if x.mnemonic == "call" and x.op_str.startswith("0x")})
touch = [c for c in callees if c in names and any(re.search(r"\[\w+ \+ 0xd0\]", x.op_str) for x in dis(c))]
print("   widget-proc direct callees touching +0xD0 of any base: %s" % " ".join("%08X" % c for c in touch))
check("L0b of the widget proc's own callees only the release 0037F860 touches +0xD0", touch == [0x0037F860],
      " ".join("%08X" % c for c in touch))

reads = collections.defaultdict(set)   # fn -> {(field, width, how)}
objreads = collections.defaultdict(set)
for f in fns:
    obj, lst = set(), set()
    for x in dis(f):
        ops = x.op_str.split(", ", 1)
        dst = c64(ops[0]) if len(ops) == 2 and not ops[0].startswith(("qword", "dword", "word", "byte")) else None
        t = rip_t(x)
        if x.mnemonic == "mov" and t == G and dst:
            obj.add(dst); lst.discard(dst); continue
        m = re.search(r"(qword|dword|word|byte) ptr \[(\w+)(?: \+ (0x[0-9a-f]+|\d+))?\]", x.op_str)
        if m and c64(m.group(2)) in obj:
            objreads[f].add(int(m.group(3) or "0", 0))
            if x.mnemonic == "mov" and m.group(3) == "0xd0" and dst:
                lst.add(dst); obj.discard(dst); continue
        if m and c64(m.group(2)) in lst and not re.search(r"\[\w+ \+ \w+\*", x.op_str):
            reads[f].add((int(m.group(3) or "0", 0), m.group(1), x.mnemonic))
        if x.mnemonic == "lea":
            mm = re.search(r"\[(\w+) \+ (0x[0-9a-f]+|\d+)\]", x.op_str)
            if mm and c64(mm.group(1)) in lst:
                reads[f].add((int(mm.group(2), 0), "lea", "lea"))
        if dst and x.mnemonic not in ("cmp", "test", "push"):
            if dst in obj and not (x.mnemonic == "mov" and t == G):
                obj.discard(dst)
            if dst in lst and not (x.mnemonic == "mov" and m and m.group(3) == "0xd0"):
                lst.discard(dst)
        if x.mnemonic == "call":
            for r in ("rax", "rcx", "rdx", "r8", "r9", "r10", "r11"):
                obj.discard(r); lst.discard(r)
lst_users = sorted(f for f in fns if 0xD0 in objreads[f])
print("functions reading [%08X]+0xD0 (the .lst buffer): %s" % (G, " ".join("%08X" % f for f in lst_users)))
for f in lst_users:
    print("   %08X: %s" % (f, ", ".join("+0x%X %s(%s)" % r for r in sorted(reads[f])) or "(pointer only: stored/compared/freed)"))
allf = set().union(*[{r[0] for r in reads[f]} for f in lst_users]) if lst_users else set()
check("C1 0037EFC0 reads word +0xE and word +0x8 of the .lst",
      {(0xE, "word", "movzx"), (0x8, "word", "movzx")} <= reads[0x0037EFC0], str(sorted(reads[0x0037EFC0])))
check("C2 the tracker sees 0037E5B0's read of the sibling +0xC8 (.dat)", 0xC8 in objreads[0x0037E5B0])
check("R1 no census function reads header +0x04 (the 'capacity' 100) of the .lst", 0x4 not in allf, str(sorted(allf)))

# L2 the lookup, decoded
b = {x.address: x for x in dis(0x0037EFC0)}
for a in (0x0037EFC7, 0x0037EFD9, 0x0037EFE8, 0x0037EFF0, 0x0037EFFC, 0x0037F000, 0x0037F00E, 0x0037F01C, 0x0037F025,
          0x0037F02A, 0x0037F039):
    print("   %08X %s %s" % (a, b[a].mnemonic, b[a].op_str))
check("L2a the lookup compares the u16 questId at dir+0 against the u16 argument, stride 8, bound = u16 [+0xE]",
      b[0x0037EFF0].op_str == "word ptr [rcx], r11w" and b[0x0037EFFC].op_str == "rcx, 8"
      and b[0x0037EFD9].op_str == "r10d, word ptr [r8 + 0xe]")
check("L2b dataRel (dir+2) = 0xFFFF means 'no string'; else result = lst + u16[+8] + dataRel",
      b[0x0037F01C].op_str == "edx, word ptr [rax + 2]" and b[0x0037F02A].op_str == "ecx, word ptr [r8 + 8]")
e = {x.address: x for x in dis(0x0037E5B0)}
check("L2c 0037E5B0 reads dir+0x04 as a byte, low nibble only (and al, 0xf) into its output +0xE",
      e[0x0037E6A6].op_str == "eax, byte ptr [rcx + 4]" and e[0x0037E6AA].op_str == "al, 0xf"
      and e[0x0037E6AC].op_str == "byte ptr [rbx + 0xe], al")
check("L2d 0037E5B0's key is (dat record u32 +0x10 >> 8) & 0x3FF (the questId the .lst is probed with)",
      e[0x0037E611].op_str == "eax, 8" and e[0x0037E60C].op_str == "ecx, 0x3ff")

# L2e the consumer of dir+0x04: 00577C30 (one of 0037E5B0's four callers) builds the record at rsp+0x30, and when the
# record's +0xF byte (the .dat record's low byte) equals 1 it sets the row state to 0037EE10(questId) >= record +0xE
c = {x.address: x for x in dis(0x00577C30)}
for a in (0x00577C93, 0x00577C98, 0x00577C9D, 0x00577CA4, 0x00577CA9, 0x00577CB1, 0x00577CB3, 0x00577CB9):
    print("   %08X %s %s" % (a, c[a].mnemonic, c[a].op_str))
check("L2e 00577C30 compares 0037EE10's result with the record's +0xE nibble (setge) on the +0xF == 1 path",
      c[0x00577C9D].op_str == "byte ptr [rsp + 0x3f], r12b" and c[0x00577CA4].op_str == "0x37ee10"
      and c[0x00577CA9].op_str == "ecx, byte ptr [rsp + 0x3e]" and c[0x00577CB3].mnemonic == "setge")

# L3 corpus
EX = "D:/FFXII_TZA_extract/ps2data/image/ff12/myoshiok"
files = sorted(glob.glob(EX + "/*/quest/menuquest.lst"))
agree = True
for p in files:
    bb = open(p, "rb").read()
    n = struct.unpack_from("<H", bb, 0xE)[0]
    dataoff16 = struct.unpack_from("<H", bb, 8)[0]
    ent = [struct.unpack_from("<HHI", bb, 0x10 + 8 * i) for i in range(n)]
    ids = [q for q, _, _ in ent]
    first = {}
    for q, rel, k in ent:
        first.setdefault(q, (rel, k))
    srt = {q: (rel, k) for q, rel, k in sorted(ent)}
    same = first == srt and len(set(ids)) == len(ids)
    agree &= same
    kinds = collections.Counter(k for _, _, k in ent)
    lows = collections.Counter(k & 0xF for _, _, k in ent)
    sentinel = sum(1 for _, rel, _ in ent if rel == 0xFFFF)
    print("   %s: n=%d ids unique %s, dataOff u16=0x%X, dir+4 values %s (low nibble %s), dataRel 0xFFFF %d" %
          (os.path.normpath(p).split(os.sep)[-3], n, len(set(ids)) == len(ids), dataoff16, dict(kinds), dict(lows), sentinel))
check("L3 in every shipped file the first-match lookup equals the sorted lookup (order-independent)", agree and files,
      "%d files" % len(files))
print("FAILS %d" % FAILS)
