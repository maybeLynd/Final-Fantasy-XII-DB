"""sd107_kind1.py - SD-107: does anything write text-element kind 1 (+0xA3 == 1)? (OPUS, 2026-09-30). Static, the
certified image, via Database/Tools/analysis-kit/gfz-scripts/retool.py and the `pe` module of
_index/candidates/rc22-34-resource-readers-0930/ (38,161 function bodies).
"""
import collections, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts")))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
import retool as T  # noqa: E402
import pe  # noqa: E402

R, SZ, c = T.R, T.sizes(), T.scan()
fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


def txt(a):
    i = next(R.md.disasm(R.at(a, 16), a, 1))
    return "%s %s" % (i.mnemonic, i.op_str)


W = {"byte": 1, "word": 2, "dword": 4, "qword": 8, "xmmword": 16, "ymmword": 32}
PAT = re.compile(r"^(byte|word|dword|qword|xmmword|ymmword) ptr \[(\w+)(?: \+ (\w+)\*\d)?(?: ([+-]) (0x[0-9a-f]+|\d+))?\]")
CORE = {0x002B3400, 0x002B3C30, 0x002B3D50, 0x002A4830, 0x002AF960, 0x002A9980, 0x002A8C50, 0x002A9F00, 0x002AA800,
        0x002AAE40, 0x002AC5F0, 0x002B32D0}
callees = collections.defaultdict(set)
for t, lst in c["calls"].items():
    for f, _ in lst:
        callees[f].add(t)
hood = set(CORE)
for f in CORE:
    hood |= {g for g, _ in c["calls"].get(f, ())} | callees.get(f, set())

imm1, inhood, nobj = [], [], 0
for f in pe.funcs:
    for x in pe.dis(f):
        if x.mnemonic in ("cmp", "test", "lea") or x.mnemonic.startswith("j"):
            continue
        ops = x.op_str.split(", ")
        m = PAT.match(ops[0]) if ops else None
        if not m or m.group(2) in ("rip", "rsp"):
            continue
        d = int(m.group(5), 0) if m.group(5) else 0
        if m.group(4) == "-":
            d = -d
        w = W[m.group(1)]
        if not d <= 0xA3 < d + w:
            continue
        nobj += 1
        if x.mnemonic == "mov" and len(ops) == 2 and re.fullmatch(r"-?0x[0-9a-f]+|\d+", ops[1]):
            v = int(ops[1], 0) & ((1 << (8 * min(w, 8))) - 1)
            if (v >> (8 * (0xA3 - d))) & 0xFF == 1:
                imm1.append((f, x.address))
        if f in hood:
            inhood.append((f, x.address, "%s %s" % (x.mnemonic, x.op_str)))
# K1 - image-wide, the one instruction that stores the constant 1 into a byte at +0xA3 (at any store width) is 007E7401
check("K1", imm1 == [(0x007E73F0, 0x007E7401)] and txt(0x007E7401) == "mov byte ptr [rcx + 0xa3], 1",
      "the only constant-1 store covering +0xA3 in %d bodies (%d object stores cover +0xA3): 007E7401" % (len(pe.funcs), nobj))
# K2 - 007E7401's object is a sound object: 007E73F0 (position floats +0x48..+0x50, then +0xA3 = 1) is called only
#      from 007BFD00 (a sound-trigger parameter operation), with rcx = 007B5070(handle): the type-3 handle resolver
#      over the table 02EAD610 (stride 0x28, live bit +0x1C, object +0x20)
cal = sorted(c["calls"].get(0x007E73F0, ()))
check("K2", cal == [(0x007BFD00, 0x007BFD7C)] and txt(0x007BFD5D) == "call 0x7b5070" and txt(0x007BFD6D) == "mov rcx, rax"
      and txt(0x007B507F) == "cmp byte ptr [rcx], 3" and txt(0x007B50A0) == "test byte ptr [rax + rdx*8 + 0x1c], 1"
      and txt(0x007B50A7) == "mov rdi, qword ptr [rax + rdx*8 + 0x20]" and txt(0x007E73F0) == "movss dword ptr [rcx + 0x48], xmm1",
      "007E73F0 <- 007BFD00 only, on a resolved sound handle (007B5070, table 02EAD610)")
# K3 - inside the text cluster's neighbourhood (builders, dispatchers, emitters, handlers and one hop of callers and
#      callees) the only object stores covering +0xA3 are the four kind writes (3, 2, 0, 0) and 002B41F0's frame slot
#      [rbp+0xA0], which is element +0x60 of its frame element at rbp+0x40 (K5), not a kind byte
want = [(0x002A4830, 0x002A49CA, "mov byte ptr [rbx + 0xa3], 3"), (0x002B3400, 0x002B3470, "mov byte ptr [rdi + 0xa3], 2"),
        (0x002B3C30, 0x002B3C40, "mov byte ptr [rcx + 0xa3], 0"), (0x002B3D50, 0x002B3D78, "mov byte ptr [rcx + 0xa3], 0"),
        (0x002B41F0, 0x002B42AA, "mov qword ptr [rbp + 0xa0], rax")]
check("K3", sorted(inhood) == want, "neighbourhood of %d bodies: only the kind writes 3/2/0/0 and one frame slot" % len(hood))
# K4 - the builders' stack-resident elements: in each holder, no store covers the element's kind byte except the builder
pat2 = re.compile(r"(byte|word|dword|qword|xmmword|ymmword) ptr \[(rsp|rbp)(?: ([+-]) (0x[0-9a-f]+|\d+))?\]")
holders, bad = [], []
for tgt in (0x002B3400, 0x002B3C30, 0x002B3D50):
    for f, site in sorted(c["calls"].get(tgt, ())):
        ins = list(R.md.disasm(R.at(f, SZ.get(f, 0x800)), f))
        pre = [i for i in ins if i.address < site][-12:]
        lea = next((i for i in reversed(pre) if i.op_str.startswith("rcx,")), None)
        m = re.match(r"rcx, \[(rsp|rbp) \+ (0x[0-9a-f]+|\d+)\]", lea.op_str) if lea is not None and lea.mnemonic == "lea" else None
        if not m:
            continue
        base, S = m.group(1), int(m.group(2), 0)
        holders.append("%08X" % site)
        for i in ins:
            if i.mnemonic in ("cmp", "test", "lea") or i.mnemonic.startswith("j"):
                continue
            mm = pat2.match(i.op_str.split(", ")[0])
            if mm and mm.group(2) == base:
                d = (-1 if mm.group(3) == "-" else 1) * (int(mm.group(4), 0) if mm.group(4) else 0)
                if d <= S + 0xA3 < d + W[mm.group(1)]:
                    bad.append(i.address)
check("K4", len(holders) == 8 and not bad, "8 stack-element builder calls; no holder store covers its element's kind: %s" % holders)
# K5 - 002B41F0 builds an element in its frame without a builder: memset(rbp+0x40, 0, 0xD0) covers its kind byte
#      (rbp+0xE3), which is then never stored - kind 0
check("K5", txt(0x002B4249) == "lea rcx, [rbp + 0x40]" and txt(0x002B422E) == "xor edx, edx" and txt(0x002B4235) == "mov r8d, 0xd0"
      and txt(0x002B424D) == "call 0x861ec0" and txt(0x002B42A5) == "call 0x39c4a0",
      "002B41F0's frame element is zero-filled over +0xA3 (kind 0) and gets its +0x60 from 0039C4A0 like 002B3400's")
print("FAILS %d" % fails)
