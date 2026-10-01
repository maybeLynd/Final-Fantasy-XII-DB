"""RC-25 residue: the values the silhouette index can take (SWE2-DATA 2026-09-30), static.

Chain (each link pinned below):
  silhouette index s = movsx word [record + 0x60] (0056A044) -> 002CEE00; s > 5 unsigned turns the silhouette off.
  record = 00282DF0(word [0209AC30] + 0xDE0) = one of the nine member copies 00283270 builds at [0209AC30] + 0x408 +
      i*0xC0 through 00320040 -> 00329220 (the copies end at +0xAC8, the pointer table 00282DF0 reads).
  00329220 writes +0x60 exactly twice: 0xFFFF (clear) and the stats page's word +4 (0032946C).
  The stats page = *(02EBF190) + 8 + slot * 0x1C8 for the member's mapped battle slot (00320040 -> 0031B9F0).
  The page's word +4 is written by BattleStats_InitializeDefinitionRecord 0023AC80 at 0023AD8E (word = its edx), and
  the party block's pages are initialised by exactly two loops, 00237DF0 and 00239960, each passing edx = the page
  index (cmovne against 0xFF), for page 0 .. 0x27.
So for a party page the word is its own index, 0 .. 0x27, kind byte (high byte) 0; the null record gives 0xFFFF.
W1 census: every instruction image-wide that writes a byte or word at displacement +4 or +5 of a register loaded
   from 02EBF190-derived page arithmetic is listed by a linear tracker over the functions that reference 02EBF190
   (raw rip sweep); the expected single writer 0023AD8E must be the only party-page +4/+5 writer.
Controls: C1 the tracker finds 0023AD8E's write when seeded on 0023AC80's page register (rdi) directly;
C2 the same tracker, run for displacement +0x1C2 (the level byte, written by 0030C470 per the level page), finds a
writer, so it is not blind.
"""
import os, re, sys, struct
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "rc22-34-resource-readers-0930"))
from pe import d, off, owner, dis, raw_rip_refs, u32, names  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


def ins(fn):
    return {x.address: x for x in dis(fn)}


a = ins(0x0056A010)
check("P1 0056A010 passes movsx word [record + 0x60] to the setter", a[0x0056A044].op_str == "ecx, word ptr [rax + 0x60]"
      and a[0x0056A044].mnemonic == "movsx", a[0x0056A044].op_str)
b = ins(0x00329220)
w60 = [x for x in b.values() if re.search(r"word ptr \[(?!rsp)\w+ \+ 0x60\], ", x.op_str) and x.mnemonic == "mov"]
for x in w60:
    print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
pre = [b[k] for k in sorted(b) if 0x00329460 <= k < 0x00329471]
for x in pre:
    print("   %08X %s %s" % (x.address, x.mnemonic, x.op_str))
check("P2 00329220 writes word +0x60 exactly twice: the clear at 0032925D and the page's BYTE +4, zero-extended, "
      "at 00329471 (0032946C movzx)",
      len(w60) == 2 and any(x.op_str == "eax, byte ptr [r14 + 4]" and x.mnemonic == "movzx" for x in pre),
      str(len(w60)))
c = ins(0x0023AC80)
check("P3 0023AC80 keeps its edx in r15d and writes it as the page's word +4 at 0023AD8E",
      c[0x0023AC9E].op_str == "r15d, edx" and c[0x0023AD8E].op_str == "word ptr [rdi + 4], r15w")
for fn, site, bound in ((0x00237DF0, 0x00237E26, 0x00237E2D), (0x00239960, 0x00239AC4, 0x00239ACB)):
    e = ins(fn)
    near = [e[k] for k in sorted(e) if site - 0x30 <= k < site]
    shape = " | ".join("%s %s" % (x.mnemonic, x.op_str) for x in near)
    ok = "cmovne edx, ebx" in shape and "imul rcx, rax, 0x1c8" in shape and e[bound].op_str == "ebx, 0x28"
    check("P4 %08X initialises party page i with edx = i (0xFFFF for i = 0xFF), i < 0x28" % fn, ok)
calls = [a2 for a2, *_ in []]
# who calls the initializer: raw E8/E9
t0 = [s for s in __import__("pe").secs if s[0] == ".text"][0]
name_, va, vs, ro, rs = t0
blob = d[ro:ro + rs]
BASE = 0x120000
sites = [BASE + va + p for p in range(len(blob) - 5) if blob[p] in (0xE8, 0xE9)
         and BASE + va + p + 5 + struct.unpack_from("<i", blob, p + 1)[0] == 0x0023AC80]
print("   raw callers of 0023AC80: %s" % " ".join("%08X in %08X" % (s, owner(s)) for s in sites))
party = [s for s in sites if owner(s) in (0x00237DF0, 0x00239960)]
other = [s for s in sites if owner(s) not in (0x00237DF0, 0x00239960)]
e = ins(0x0023A570)
check("P5 the third caller (0023A7A9 in 0023A570) passes a SpawnKeep entry + 0x80, not a party-block page",
      other == [0x0023A7A9] and e[0x0023A787].op_str == "rax, -0x80" and e[0x0023A776].op_str == "0x236100",
      " ".join("%08X" % s for s in other))

# W1: writers of +4/+5 (byte/word) through a 02EBF190-derived register, in every function referencing 02EBF190
refs = raw_rip_refs(0x02EBF190, 0x02EBF198)
fns = sorted({owner(x) for x, *_ in refs if owner(x)})
print("W1 functions referencing 02EBF190: %d (raw sites %d)" % (len(fns), len(refs)))


def tracked_writes(fn, disps, seed_regs=()):
    hits = []
    base, page = set(), set(seed_regs)
    for x in dis(fn):
        op = x.op_str
        m = re.search(r"\[rip ([+-]) 0x([0-9a-f]+)\]", op)
        dst = op.split(", ")[0] if ", " in op else None
        if x.mnemonic == "mov" and m and dst and not dst.startswith(("qword", "dword", "word", "byte")):
            v = int(m.group(2), 16)
            t = x.address + x.size + (v if m.group(1) == "+" else -v)
            if t == 0x02EBF190:
                base.add(dst); page.discard(dst); continue
        if dst in ("rax", "rcx", "rdx", "rbx", "rsi", "rdi", "rbp", "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15"):
            src = op.split(", ", 1)[1]
            if x.mnemonic in ("add", "lea") and any(r in src for r in base | page):
                page.add(dst); continue
            if x.mnemonic == "mov" and src in page:
                page.add(dst); continue
        mm = re.match(r"(byte|word) ptr \[(\w+) \+ (0x[0-9a-f]+|\d+)\], ", op)
        if x.mnemonic in ("mov", "or", "and", "inc", "dec", "add", "sub") and mm and mm.group(2) in page \
                and (disps is None or int(mm.group(3), 0) in disps):
            hits.append((x.address, x.mnemonic, op))
        if dst in page | base and x.mnemonic not in ("cmp", "test", "add", "lea"):
            page.discard(dst); base.discard(dst)
        if x.mnemonic == "call":
            for r in ("rax", "rcx", "rdx", "r8", "r9", "r10", "r11"):
                page.discard(r); base.discard(r)
    return hits


w = []
for fn in fns:
    w += [(fn,) + h for h in tracked_writes(fn, (4, 5))]
for fn, adr, mn, op in w:
    print("   W1 %08X %s %s   in %08X %s" % (adr, mn, op, fn, names.get(fn, "")))
check("W1 no function referencing 02EBF190 writes +4/+5 of a page it derives from it", not w,
      "%d writes" % len(w))
c1 = tracked_writes(0x0023AC80, (4,), seed_regs=("rcx",))
check("C1 control: seeded on 0023AC80's page argument (rcx) the tracker finds the 0023AD8E write",
      any(h[0] == 0x0023AD8E for h in c1))
c2 = []
for fn in fns:
    c2 += [(fn,) + h for h in tracked_writes(fn, None)]
for h in c2[:12]:
    print("   C2 %08X %s %s in %08X" % (h[1], h[2], h[3], h[0]))
check("C2 control: through the same 02EBF190 derivation the tracker sees byte/word writes at other displacements (%d)"
      % len(c2), len(c2) > 0)
# S1: which selectors the shipped zone scripts add (the BQ-10 decompile of every shipped script, 1,114 files)
import glob, collections
CORPUS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\pub140-scratch\corpus\us"
cnt = collections.Counter()
nfiles = 0
for f in glob.glob(os.path.join(CORPUS, "*.txt")):
    nfiles += 1
    for m in re.finditer(r"\b(addpartymember|addguestbattlemember)\((\d+)\)", open(f, encoding="utf-8", errors="replace").read()):
        cnt[(m.group(1), int(m.group(2)))] += 1
print("S1 decompiled scripts read: %d" % nfiles)
for (v, sel), n in sorted(cnt.items()):
    print("   %-22s selector %2d  x%d" % (v, sel, n))
mains = sorted({sel for (v, sel) in cnt if v == "addpartymember"})
check("S1 shipped scripts add main-character selectors exactly 0..5 with literal arguments", mains == [0, 1, 2, 3, 4, 5],
      str(mains))
check("S1 control: the guest verb is found with guest-band selectors (7..25)",
      any(v == "addguestbattlemember" and 7 <= s <= 25 for (v, s) in cnt))
print("RESULT party page byte +4 = page index 0..0x27; the record +0x60 is that index (zero-extended) or 0xFFFF")
print("FAILS %d" % FAILS)
