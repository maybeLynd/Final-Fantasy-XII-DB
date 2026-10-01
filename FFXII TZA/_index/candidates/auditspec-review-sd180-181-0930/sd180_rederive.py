"""sd180_rederive.py - SWE2-AUDIT-SPEC independent re-derivation for sd180-181-emitter-walk-0930 (1dbac71de).

Own loader sdx_indep.py (pefile + capstone, sha asserted); no retool. Shipped data from D:/FFXII_TZA_extract.
  A  the walk 003631B0: per shape-class arm, what reaches 00361810's stack arguments 6..10 (the W1 claim).
  B  00361810: which stack arguments it reads, and whether it reads record +0x38 itself (it has the record as arg 5).
  C  W2/W3 polarities (ucomiss/jp/jne; 003638B0's js on +0x1A).
  D  the driver 00362850: initial value, the two walks, everything between the second walk and 002DF410.
  E  022CBAF0 writer/reader census: rip, image-base-relative, abs64/rva32, DIR64; callers of 003635C0 (E8/E9, jcc, data).
     Positive controls: 022CBAF8 (the SPP1 pointer next door, known rip readers) and 003635E0 (known caller 003775D0).
  F  shipped SP1 blocks (slot 16 of every .mpk): records, shape-class counts, file values of +0x1A and +0x38.
"""
import collections, glob, os, struct, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sdx_indep as X  # noqa: E402

print("image sha256 asserted:", X.SHA[:16])


def f32(va):
    return struct.unpack("<f", X.rd(va, 4))[0]


def ripv(i):
    for k, m, sz in X.mem_ops(i):
        if m.base == X.X86_REG_RIP:
            return i.address + i.size + m.disp
    return None


# ---- A
print("\n== A  003631B0 shape arms (class = byte [rec+9] & 0x7F)")
ins = {i.address: i for i in X.dis(0x003631B0, 0x003633B0)}
for a in (0x0036326A, 0x0036326E, 0x00363271, 0x00363276, 0x0036327B):
    print("  %08X %s" % (a, X.txt(ins[a])))
for a in (0x00363212, 0x00363221):
    print("  %08X %-45s const [%08X] = %r" % (a, X.txt(ins[a]), ripv(ins[a]), f32(ripv(ins[a]))))
arms = {"class 0 (je 003632C1)": (0x003632C1, 0x003632E0), "class 1 (je 003632AF)": (0x003632AF, 0x003632C1),
        "class 2 (je 00363293)": (0x00363293, 0x003632AF), "class >=3 (fall-through 0036327D)": (0x0036327D, 0x00363293)}
for name, (s, e) in arms.items():
    print("  --", name)
    a = s
    seen = 0
    while True:
        i = ins[a]
        print("     %08X %s" % (a, X.txt(i)))
        seen += 1
        if i.mnemonic == "jmp":
            a = i.operands[0].imm
            if a in (0x003632D1, 0x003632DB, 0x003632E0):
                # follow into the shared tail up to the 00361810 call
                while a < 0x00363320:
                    print("     %08X %s" % (a, X.txt(ins[a])))
                    a = a + ins[a].size
                break
            continue
        a += i.size
        if a == 0x003632D1:   # class 0 falls into the shared loads
            while a < 0x00363320:
                print("     %08X %s" % (a, X.txt(ins[a])))
                a = a + ins[a].size
            break
print("  xmm6 is set to xmm7 (0) at 0036325A before the dispatch:", X.txt(ins[0x0036325A]), "| xmm7:", X.txt(ins[0x00363206]))
print("  [rsp+0x30] source %08X = .data cell %08X (file bytes: %s)" % (
    0x003632EB, ripv(ins[0x003632EB]), X.off(ripv(ins[0x003632EB])) is not None))

# ---- B
print("\n== B  00361810: stack-argument reads and record reads (record = arg5 = [rsp+0xd0] -> rsi)")
body = X.dis(0x00361810, 0x00361BE6)
argname = {0xD0: "arg5 record", 0xD8: "arg6 (xmm6: 0 / 00362230 result)", 0xE0: "arg7 ([022CBA8C])",
           0xE8: "arg8 (xmm1: +0x54 or 0)", 0xF0: "arg9 (xmm2: +0x58 or const)", 0xF8: "arg10 (xmm0: +0x38 or const)"}
for i in body:
    for k, m, sz in X.mem_ops(i):
        if m.base == X.capstone_rsp if hasattr(X, "capstone_rsp") else False:
            pass
    s = X.txt(i)
    for d, nm in argname.items():
        if ("[rsp + 0x%x]" % d) in s:
            print("  %08X %-50s %s" % (i.address, s, nm))
rsi_reads = [(i.address, X.txt(i)) for i in body if "[rsi + " in X.txt(i) or "[rsi]" in X.txt(i)]
print("  memory operands on rsi (the record) in 00361810:", rsi_reads)
print("  rsi writes in 00361810 (other than the load):",
      [(hex(i.address), X.txt(i)) for i in body if X.txt(i).startswith(("mov rsi", "lea rsi", "pop rsi", "xchg rsi"))])

# ---- C
print("\n== C  W2 / W3")
for a in (0x00363341, 0x00363344, 0x00363349, 0x0036334C, 0x0036334E, 0x00363350):
    print("  %08X %s" % (a, X.txt(ins[a])))
b3 = {i.address: i for i in X.dis(0x003638B0, 0x00363A10)}
for a in (0x003638D2, 0x003638D5, 0x003638DC, 0x003638DE, 0x003638E0, 0x003638E3):
    print("  %08X %s" % (a, X.txt(b3[a])))
print("  003639FF:", X.txt(X.one(0x003639FF)))
print("  esi writes in 003638B0..003639FF:", [(hex(i.address), X.txt(i)) for i in X.dis(0x003638B0, 0x003639FF)
                                             if X.txt(i).startswith(("mov esi", "movsx esi", "movzx esi", "xor esi", "lea esi", "or esi", "cmov"))])

# ---- D
print("\n== D  driver 00362850")
d = {i.address: i for i in X.dis(0x00362850, 0x00362C06)}
for a in (0x00362870, 0x00362AC0, 0x00362ACE, 0x00362ADE, 0x00362B12, 0x00362B63, 0x00362B76, 0x00362B82, 0x00362B87,
          0x00362B8F, 0x00362BB1, 0x00362BB7, 0x00362BBC, 0x00362BBE, 0x00362BC4, 0x00362BCB, 0x00362BD1, 0x00362BD3,
          0x00362BD6, 0x00362BDB, 0x00362BE0, 0x00362BE5):
    i = d[a]
    r = ripv(i)
    print("  %08X %-48s %s" % (a, X.txt(i), ("-> %08X" % r) if r else ""))
print("  ebx writes between 00362B12 and 00362BBE:", [(hex(a), X.txt(d[a])) for a in sorted(d)
      if 0x00362B12 <= a < 0x00362BBE and X.txt(d[a]).startswith(("mov ebx", "mov rbx", "xor ebx", "inc rbx", "add rbx", "lea ebx", "mov bl", "pop rbx"))])
print("  022CBA80..022CBA9F references (rip):")
for h in X.rip_refs(0x022CBA80, 0x022CBAA0):
    print("    %08X -> %08X  %-50s w%d %s  owner %s" % (h[0], h[1], h[2], h[3], h[4], X.owner(h[0])))

# ---- E
print("\n== E  022CBAF0 census")
for lo, hi, nm in ((0x022CBAF0, 0x022CBAF8, "022CBAF0 (base)"), (0x022CBAF8, 0x022CBB00, "022CBAF8 (control: SPP1 ptr)")):
    rr = X.rip_refs(lo, hi)
    print("  %s rip refs: %d" % (nm, len(rr)))
    for h in rr:
        print("    %08X %-50s w%d %s  owner %s" % (h[0], h[2], h[3], h[4], X.owner(h[0])))
    ib = X.imagebase_refs(lo, hi)
    print("  %s image-base-relative refs: %d %s" % (nm, len(ib), ib))
    print("  %s data refs: %s  DIR64 targets: %s" % (nm, [(k, "%08X" % v, s) for k, v, s in X.data_refs(lo)], X.reloc_in(lo, hi)))
print("  structure-base forms: rip lea/refs into 022CBA00..022CBAF0 that are lea:",
      [("%08X" % h[0], h[2]) for h in X.rip_refs(0x022CBA00, 0x022CBAF0) if h[4] == "A"])
for tgt in (0x003635C0, 0x003635E0):
    print("  callers of %08X: rel32 %s jcc %s data %s DIR64 %s" % (tgt, [("%08X" % a, k) for a, k in X.rel32_callers(tgt)],
          X.jcc_callers(tgt), [(k, "%08X" % v, s) for k, v, s in X.data_refs(tgt)], X.reloc_in(tgt, tgt + 1)))
print("  rip lea of 003635C0:", [("%08X" % h[0], h[2]) for h in X.rip_refs(0x003635C0, 0x003635C1)])

# ---- F
print("\n== F  shipped SP1 blocks")
files = sorted(glob.glob(r"D:/FFXII_TZA_extract/ps2data/plan_master/map_ctrl/*/*/bin/*.mpk"))
cls = collections.Counter()
o1a = collections.Counter()
o38_by_cls = collections.defaultdict(collections.Counter)
nsp1 = nrec = nidx = 0
cls_rec0 = collections.Counter()
default_list = collections.Counter()
for fn in files:
    b = open(fn, "rb").read()
    cnt = struct.unpack_from("<I", b, 0)[0]
    sizes = struct.unpack_from("<%dI" % cnt, b, 4)
    pos = ((cnt + 1) * 4 + 0x3F) & ~0x3F
    sp1 = None
    for s, sz in enumerate(sizes):
        if sz:
            pos += 0x40
            if s == 16:
                sp1 = b[pos:pos + sz]
            pos += sz
    if sp1 is None:
        continue
    assert sp1[:4] == b"SP1\0", fn
    nsp1 += 1
    offIdx = struct.unpack_from("<I", sp1, 0x0C)[0]
    offEm = struct.unpack_from("<I", sp1, 0x10)[0]
    if offIdx == 0:
        continue
    nidx += 1
    bound = struct.unpack_from("<H", sp1, offIdx)[0]
    offs = struct.unpack_from("<%dH" % bound, sp1, offIdx + 2)
    for j, ro in enumerate(offs):
        rec = sp1[ro:]
        c = rec[9] & 0x7F
        cls[c] += 1
        o1a[rec[0x1A]] += 1
        o38_by_cls[c][round(struct.unpack_from("<f", rec, 0x38)[0], 4)] += 1
        nrec += 1
        if j == 0:
            cls_rec0[c] += 1
    # the arena-head default list (offEmitters region starts with a bit15-terminated u16 list)
    lst = []
    k = offEm
    while True:
        w = struct.unpack_from("<H", sp1, k)[0]
        lst.append(w)
        k += 2
        if w & 0x8000:
            break
    default_list[tuple(lst)] += 1
print("  .mpk files %d, with SP1 %d, with an emitter index %d, records %d" % (len(files), nsp1, nidx, nrec))
print("  shape class counts:", dict(sorted(cls.items())))
print("  class of index entry 0:", dict(cls_rec0))
print("  arena-head default lists:", dict(default_list))
print("  +0x1A file bytes:", dict(o1a))
for c in sorted(o38_by_cls):
    print("  +0x38 values, class %d: %s" % (c, dict(o38_by_cls[c].most_common(6))))
