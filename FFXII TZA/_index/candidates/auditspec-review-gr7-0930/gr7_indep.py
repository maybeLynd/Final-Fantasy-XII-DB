"""gr7_indep.py - SWE2-AUDIT-SPEC independent re-derivation for the GR-7 review (2026-09-30).
pefile + capstone + numpy only (img.py, sha asserted); none of the package's retool / regval census.

J  jump tables: 00321190 (reader) and 00329E60 (writer) kind tables, all 10 slots; the selector candidate-loop table in
   00301AD0 (bound cmp 0x45, byte index table + dword table, both image-base-relative), all 70 opcodes.
C  raw census of every instruction whose memory operand (any non-rip base, any index/scale) covers a byte of
   +0xB90..+0xB93, at any width: raw scan of every executable section for disp32 values 0xB81..0xB93, each confirmed by
   decoding an instruction that starts 1..10 bytes earlier and carries the value as its displacement. `lea` with disp
   0xB90 and imm32 0xB90 are listed too. Each hit is attributed to its .pdata function (or 'no-pdata').
X  raw E8/E9 and jcc (0F 8x) sites targeting 00321190 / 00329E60 by rel32 arithmetic over .text, plus any qword in
   any section equal to the target (a stored pointer).
"""
import struct, bisect, collections, re
import numpy as np
from img import raw, SECS, IB, md, off, rd, u8, u32, s32, dis, pdata
from capstone import CS_OP_MEM, CS_OP_IMM
from capstone.x86 import X86_REG_RIP

P = sorted(pdata())
PS = [b for b, e in P]


def func_of(a):
    k = bisect.bisect_right(PS, a) - 1
    if k >= 0 and P[k][0] <= a < P[k][1]:
        return P[k][0]
    return None


print("== J  jump tables")
rt = [IB + u32(IB + 0x2012AC + 4 * k) for k in range(10)]
wt = [IB + u32(IB + 0x209F40 + 4 * k) for k in range(10)]
print("reader 00321190 kind->arm:", " ".join("%d:%08X" % (k + 1, a) for k, a in enumerate(rt)))
print("writer 00329E60 kind->arm:", " ".join("%d:%08X" % (k + 1, a) for k, a in enumerate(wt)))
print("slots pointing at 0032126F:", [k + 1 for k, a in enumerate(rt) if a == 0x0032126F],
      " at 00329F1C:", [k + 1 for k, a in enumerate(wt) if a == 0x00329F1C])
idx = [u8(IB + 0x1E3680 + k) for k in range(0x46)]
arms = [IB + u32(IB + 0x1E3604 + 4 * i) for i in idx]
by = collections.defaultdict(list)
for k, a in enumerate(arms):
    by[a].append(k)
print("selector loop: %d opcodes, %d distinct arms, max byte index %d (dword table has room for %d entries)"
      % (len(idx), len(by), max(idx), (0x1E3680 - 0x1E3604) // 4))
for a in sorted(by):
    print("  arm %08X <- opcodes %s" % (a, ",".join("0x%02X" % k for k in by[a])))

print("== C  raw +0xB90 census")
hits = {}
PAT = re.compile(bytes([0x5B, 0x81, 0x2D, 0x93, 0x5D, 0x0B, 0, 0]), re.S)
for n, v, vs, p, rs, x in SECS:
    if not x:
        continue
    end = p + min(vs, rs)
    for m in PAT.finditer(raw, p, end):
        o = m.start()
        d = struct.unpack_from("<I", raw, o)[0]
        va = v + (o - p)
        f = func_of(va)
        cands = []
        if f and va - f < 0x8000:
            # boundary-true decode: linear from the .pdata start (its own unwind-backed entry)
            cands = [j for j in dis(f, va + 12) if j.address < va < j.address + j.size]
        backs = [cands[0].address - va] if cands else [-k for k in range(10, 0, -1)]
        for back in [-b for b in backs]:
            s = va - back
            i = next(md.disasm(raw[o - back:o - back + 16], s, 1), None)
            if i is None or not (va + 4 <= s + i.size):
                continue
            ok = False
            for op in i.operands:
                if op.type == CS_OP_MEM and op.mem.base != X86_REG_RIP and op.mem.disp == d:
                    w = op.size or 1
                    if (i.mnemonic == "lea" and d == 0xB90) or (d < 0xB94 and d + w > 0xB90):
                        ok = ("mem", w)
                if op.type == CS_OP_IMM and op.imm == d and d == 0xB90:
                    ok = ("imm", 4)
            if ok:
                hits.setdefault(s, (i, ok))
                break
cnt = collections.Counter()
for s in sorted(hits):
    i, (k, w) = hits[s]
    f = func_of(s)
    cnt[f] += 1
    print("%08X  %-9s %-4s w%-2d %-6s %s" % (s, "%08X" % f if f else "no-pdata", k, w, i.mnemonic, i.op_str))
print("hits %d in %d functions" % (len(hits), len(cnt)))

print("== X  raw callers of the store reader / writer")
tx = [(v, p, p + min(vs, rs)) for n, v, vs, p, rs, x in SECS if x]
for tgt in (0x00321190, 0x00329E60):
    e8, jcc, ptr = [], [], []
    for v, p, end in tx:
        a = np.frombuffer(raw, dtype=np.uint8, count=end - p, offset=p).astype(np.int64)
        L = len(a) - 6
        r1 = a[1:L + 1] | (a[2:L + 2] << 8) | (a[3:L + 3] << 16) | (a[4:L + 4] << 24)
        r1 = np.where(r1 >= 1 << 31, r1 - (1 << 32), r1)
        r2 = a[2:L + 2] | (a[3:L + 3] << 8) | (a[4:L + 4] << 16) | (a[5:L + 5] << 24)
        r2 = np.where(r2 >= 1 << 31, r2 - (1 << 32), r2)
        vas = v + np.arange(L, dtype=np.int64)
        m1 = ((a[:L] == 0xE8) | (a[:L] == 0xE9)) & (vas + 5 + r1 == tgt)
        e8 += [int(t) for t in vas[m1]]
        m2 = (a[:L] == 0x0F) & (a[1:L + 1] >= 0x80) & (a[1:L + 1] <= 0x8F) & (vas + 6 + r2 == tgt)
        jcc += [int(t) for t in vas[m2]]
    pat = struct.pack("<Q", tgt)
    for n, v, vs, p, rs, x in SECS:
        for m in re.finditer(re.escape(pat), raw[p:p + min(vs, rs)]):
            ptr.append(v + m.start())
    print("%08X: rel32 E8/E9 %d; jcc %d; stored qwords %d" % (tgt, len(e8), len(jcc), len(ptr)))
    for a in e8:
        f = func_of(a)
        ins = dis(f, a + 5) if f and a - f < 0x4000 else []
        me = [j for j in ins if j.address == a]
        pre = [j for j in ins if j.address < a and j.op_str.split(",")[0] in ("ecx", "rcx")]
        print("  %08X %-5s in %s  on-boundary %s  last ecx write: %s" % (
            a, me[0].mnemonic if me else "?", "%08X" % f if f else "no-pdata", bool(me),
            "%08X %s %s" % (pre[-1].address, pre[-1].mnemonic, pre[-1].op_str) if pre else "-"))
    for a in jcc:
        print("  jcc %08X in %s" % (a, func_of(a)))
    for a in ptr:
        print("  qword %08X" % a)
