"""gr1315_indep.py - SWE2-AUDIT-SPEC independent re-derivation for the GR-13/14/15 review (2026-09-30).

Written without the package's checker and without retool/structflow: the lane's own image loader
(../auditspec-review-ov31-type-store-0929/ov31_indep.py, sha256 asserted), capstone, .pdata extents.

  R  raw references image-wide (one pass): E8/E9 rel32, 0F 8x jcc, rip-relative lea/mov (disp32 arithmetic + decode),
     abs64 (and whether a DIR64 relocation covers it) and rva32, for the dispatch-reach targets.
  L  0057DAD0's stores, re-based to the entry (rbx = entry+8, r14 = entry).
  M  message dispatch: 0056E140 (msg-1 table bound), 0056D370, 005636F0-family procs, 002D2DB0 (list control) msg 26.
  J  the 00564B90 jump table decoded from bytes (ids 0x405..0x40F -> which procedure lea).
  K  +0x17F stores image-wide, any width (disp32 search; width-covering displacements 0x178..0x17F).
  P  the 14 +0x10 price-read sites: width + the mask/sentinel test after them.
  Q  independent row-consumer sweep, image-wide: every qword load of +0xC8 / +0xD0 / +0xE0 (disp32 search), then a
     short linear forward window that follows the loaded register (mov/add/lea copies, and the `shl r,5; add r,[X+d]`
     index form) to any dword read at +0x10 through it. Positive controls: 0056D461 (via +0xD0) and the 14 sites.
  T  tables: 00D233A0 id->kind, 00D23920 shop tab ids, 00D23D60 / 00D23D6C remaps, 00D0F990 nibble table.
"""
import os, struct, sys, bisect, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402
from capstone import CS_OP_MEM, CS_OP_REG, CS_OP_IMM
from capstone.x86 import X86_REG_RIP, X86_REG_INVALID

IB = T.IB
raw = T.raw

# ------------------------------------------------------------------ .pdata and relocations
dd = T.pe.OPTIONAL_HEADER.DATA_DIRECTORY[3]
o = T.off(IB + dd.VirtualAddress)
PD = sorted(struct.unpack_from("<III", raw, o + 12 * k) for k in range(dd.Size // 12))
ST = [e[0] for e in PD]


def root(va):
    rva = va - IB
    j = bisect.bisect_right(ST, rva) - 1
    if j < 0 or not (PD[j][0] <= rva < PD[j][1]):
        return None
    e = PD[j]
    while True:
        uo = T.off(IB + e[2]); fl = raw[uo] >> 3; cnt = raw[uo + 2]
        if not (fl & 4):
            return IB + e[0]
        e = struct.unpack_from("<III", raw, uo + 4 + ((cnt + 1) & ~1) * 2)


def ranges_of(f):
    return [(IB + b, IB + e) for b, e, u in PD if root(IB + b) == f]


rd = T.pe.OPTIONAL_HEADER.DATA_DIRECTORY[5]
RELOC = set()
ro, rend = T.off(IB + rd.VirtualAddress), T.off(IB + rd.VirtualAddress) + rd.Size
while ro < rend:
    page, bsz = struct.unpack_from("<II", raw, ro)
    if bsz == 0:
        break
    for k in range((bsz - 8) // 2):
        w = struct.unpack_from("<H", raw, ro + 8 + 2 * k)[0]
        if w >> 12 == 10:
            RELOC.add(IB + page + (w & 0xFFF))
    ro += bsz


def dis1(a):
    return next(T.md.disasm(T.rd(a, 16), a, 1))


def s(i):
    return "%08X %s %s" % (i.address, i.mnemonic, i.op_str)


print("== R. raw references (rel32 E8/E9, jcc 0F 8x, rip lea/mov, abs64 [DIR64?], rva32)")
TG = [0x005651E0, 0x005636F0, 0x00563930, 0x00563B10, 0x00563D20, 0x0056E140, 0x0056D370, 0x00564B90, 0x00564AC0,
      0x002D2600, 0x002D28E0, 0x002D1420, 0x002D2DB0, 0x005655F0, 0x00564780]
TGS = set(TG)
rel = collections.defaultdict(list)
for n, v, vs, p, rs in T.TEXT:
    blob = raw[p:p + min(vs, rs)]
    L = len(blob)
    for k in range(L - 6):
        b = blob[k]
        if b == 0xE8 or b == 0xE9:
            t = v + k + 5 + struct.unpack_from("<i", blob, k + 1)[0]
            if t in TGS:
                ins = list(T.md.disasm(blob[k:k + 5], v + k, 1))
                rel[t].append("%08X %s%s" % (v + k, "call" if b == 0xE8 else "jmp", "" if ins and ins[0].size == 5 else "(nodecode)"))
        elif b == 0x0F and 0x80 <= blob[k + 1] <= 0x8F:
            t = v + k + 6 + struct.unpack_from("<i", blob, k + 2)[0]
            if t in TGS:
                rel[t].append("%08X jcc" % (v + k))
for t in TG:
    rr = T.rip_refs(t, t + 1)
    dr = T.data_refs(t)
    a64 = ["%s%s" % (x, "[DIR64]" if int(x[:8], 16) in RELOC else "") for x in dr["abs64"]]
    print("  %08X rel/jcc %s | rip %s | abs64 %s | rva32 %d" % (t, rel[t], ["%08X %s %s" % h[:3] for h in rr], a64, len(dr["rva32"])))
print("  control: 005636F0's four tail jumps must include 00563721; 00564B90's leas must include 00564C0A")

print("== L. 0057DAD0 stores re-based to the entry (rbx = entry + 8 from 0057DAFF; r14 = rbx - 8 from 0057DB55)")
for i in T.dis(0x0057DAD0, 0x0057DC27):
    if i.operands and i.operands[0].type == CS_OP_MEM and i.mnemonic.startswith(("mov", "bts")):
        m = i.operands[0].mem
        rn = i.reg_name(m.base)
        if rn in ("rbx", "r14"):
            print("  %-40s -> entry + 0x%X (%dB)" % (s(i), m.disp + (8 if rn == "rbx" else 0), i.operands[0].size))

print("== M. message dispatch")
i = dis1(0x0056E14D); j = dis1(0x0056E150)
print("  0056E140: eax = msg - 1 (0056E14B); %s ; %s ; default 0056E3AB -> %s" % (s(i), s(j), s(dis1(0x0056E3B3))))
print("    msg 26 -> eax 25 > 0x13 -> default: %s" % (25 > i.operands[1].imm))
tb = []
for k in range(20):
    tb.append(IB + struct.unpack_from("<I", T.rd(0x0056E3B8 + 4 * k, 4))[0])
print("    table 0056E3B8 msgs 1..20 -> %s" % " ".join("%d:%08X" % (k + 1, t) for k, t in enumerate(tb)))
print("    any table arm = 005651E0 or a list proc: %s" % any(t in (0x005651E0, 0x005636F0, 0x00563930, 0x00563B10, 0x00563D20) for t in tb))
print("  005C5230: %s ; %s" % (s(dis1(0x005C5230)), s(dis1(0x005C5232))))
for pr in (0x005636F0, 0x00563930, 0x00563B10, 0x00563D20):
    body = T.dis_func(pr, 0x400)
    c26 = [s(x) for x in body if x.mnemonic == "cmp" and x.op_str.endswith(", 0x1a")]
    tails = [s(x) for x in body if x.mnemonic == "jmp" and x.operands[0].type == CS_OP_IMM and x.operands[0].imm == 0x005651E0]
    print("  %08X cmp 0x1a %s ; tail to 005651E0 %s" % (pr, c26, tails))
print("  002D2DB0 (list control proc) msg 26 arm: %s / %s / %s .. %s" % (s(dis1(0x002D2DFF)), s(dis1(0x002D2E02)), s(dis1(0x002D2E11)), s(dis1(0x002D2E29))))
print("    (ecx = msg-1-1-2-1 = msg-5 at 002D2DFF, so 0x15 = message 26: forwarded to the procedure of [control+0xC8])")

print("== J. 00564B90 id switch")
for i in T.dis(0x00564B90, 0x00564C80):
    if i.mnemonic in ("cmp", "sub", "add", "ja", "jmp", "movzx", "lea", "mov") and ("0x40" in i.op_str or "rip" in i.op_str or i.mnemonic in ("ja", "jmp")):
        extra = ""
        for m, sz in T.mem_ops(i):
            if m.base == X86_REG_RIP:
                extra = " ; -> %08X" % (i.address + i.size + m.disp)
        print("  %s%s" % (s(i), extra))

print("== K. +0x17F stores image-wide (any width covering +0x17F)")
hits = set()
for n, v, vs, p, rs in T.TEXT:
    blob = raw[p:p + min(vs, rs)]
    for d in range(0x178, 0x180):
        pat = struct.pack("<i", d)
        k = blob.find(pat)
        while k >= 0:
            for back in range(10, 0, -1):
                if k - back < 0:
                    continue
                ii = list(T.md.disasm(blob[k - back:k - back + 15], v + k - back, 1))
                if not ii:
                    continue
                x = ii[0]
                if not (x.address < v + k and v + k + 4 <= x.address + x.size):
                    continue
                if x.operands and x.operands[0].type == CS_OP_MEM and x.operands[0].mem.disp == d and \
                        x.operands[0].mem.base != X86_REG_RIP and not x.mnemonic.startswith(("cmp", "test")):
                    sz = x.operands[0].size
                    if d + sz > 0x17F and x.mnemonic not in ("push",):
                        hits.add((x.address, x.mnemonic, x.op_str, sz))
                    break
                if x.operands and any(op.type == CS_OP_MEM and op.mem.disp == d for op in x.operands):
                    break
            k = blob.find(pat, k + 1)
rows = sorted(hits)
for a, mn, op, sz in rows:
    r = root(a)
    print("  %08X root %s %dB %s %s" % (a, "%08X" % r if r else "--------", sz, mn, op))
print("  total %d (memory-destination, non-cmp/test) instructions covering +0x17F; control 005647B4 & 003FD371 present: %s"
      % (len(rows), {0x005647B4, 0x003FD371} <= {r[0] for r in rows}))

print("== P. the 14 +0x10 read sites")
P14 = [0x0056CC7E, 0x0056CCA2, 0x0056CE07, 0x0056CE31, 0x0056CFF3, 0x0056D023, 0x0056D0C8, 0x0056D267, 0x0056D291,
       0x0056D461, 0x0056D8F1, 0x0056DBCA, 0x0056E71A, 0x0056E797]
cmpn = maskn = 0
for a in P14:
    x = dis1(a)
    mo = [(m, sz) for m, sz in T.mem_ops(x)]
    ok = mo and mo[0][0].disp == 0x10 and mo[0][1] == 4
    kind = "?"
    if x.mnemonic == "cmp" and "0x80000000" in x.op_str:
        kind = "cmp-sentinel"; cmpn += 1
    else:
        dst = x.reg_name(x.operands[0].reg) if x.operands[0].type == CS_OP_REG else None
        nxt = list(T.md.disasm(T.rd(x.address + x.size, 80), x.address + x.size, 10))
        for y in nxt[:8]:
            if dst and y.op_str.startswith(dst) and (("btr" == y.mnemonic and "0x1f" in y.op_str) or ("and" == y.mnemonic and "0x7fffffff" in y.op_str)):
                kind = "masked@%08X(%s)" % (y.address, y.mnemonic); maskn += 1
                break
            if dst and y.op_str.startswith(dst) and y.mnemonic not in ("cmp", "test"):
                kind = "OTHER-WRITE-FIRST@%08X %s %s" % (y.address, y.mnemonic, y.op_str)
                break
    print("  %s  dword+0x10=%s root %08X  %s" % (s(x), bool(ok), root(a), kind))
print("  cmp-sentinel %d, masked %d, total %d" % (cmpn, maskn, len(P14)))

print("== Q. row-consumer sweep image-wide: qword loads of +0xC8/+0xD0/+0xE0 followed through the loaded register "
      "to a dword +0x10 read")


def regs_of(x, op):
    return x.reg_name(op.reg)


FAM = {"rax": "rax", "eax": "rax", "rbx": "rbx", "ebx": "rbx", "rcx": "rcx", "ecx": "rcx", "rdx": "rdx", "edx": "rdx",
       "rsi": "rsi", "esi": "rsi", "rdi": "rdi", "edi": "rdi", "rbp": "rbp", "ebp": "rbp"}
for q in range(8, 16):
    FAM["r%d" % q] = "r%d" % q; FAM["r%dd" % q] = "r%d" % q


def fam(n):
    return FAM.get(n, n)


found = collections.defaultdict(list)
nload = 0
for n, v, vs, p, rs in T.TEXT:
    blob = raw[p:p + min(vs, rs)]
    for d in (0xC8, 0xD0, 0xE0):
        pat = struct.pack("<i", d)
        k = blob.find(pat)
        while k >= 0:
            x = None
            for back in range(10, 0, -1):
                if k - back < 0:
                    continue
                ii = list(T.md.disasm(blob[k - back:k - back + 15], v + k - back, 1))
                if ii and ii[0].address < v + k and v + k + 4 <= ii[0].address + ii[0].size:
                    x = ii[0]
                    break
            k2 = k
            k = blob.find(pat, k + 1)
            if x is None or x.mnemonic not in ("mov", "add") or len(x.operands) != 2:
                continue
            if not (x.operands[0].type == CS_OP_REG and x.operands[1].type == CS_OP_MEM and x.operands[1].size == 8
                    and x.operands[1].mem.disp == d and x.operands[1].mem.base != X86_REG_RIP):
                continue
            nload += 1
            live = {fam(regs_of(x, x.operands[0]))}
            pos = x.address + x.size
            for y in T.md.disasm(T.rd(pos, 160), pos, 24):
                for m, sz in T.mem_ops(y):
                    b = fam(y.reg_name(m.base)) if m.base else None
                    ix = fam(y.reg_name(m.index)) if m.index else None
                    if m.disp == 0x10 and sz == 4 and (b in live or ix in live) and y.mnemonic != "lea":
                        found[y.address].append((x.address, d, y.mnemonic, y.op_str))
                # propagate copies; kill on other writes
                if len(y.operands) == 2 and y.operands[0].type == CS_OP_REG:
                    dst = fam(y.reg_name(y.operands[0].reg))
                    src = y.operands[1]
                    if y.mnemonic in ("mov",) and src.type == CS_OP_REG and fam(y.reg_name(src.reg)) in live:
                        live.add(dst)
                    elif y.mnemonic == "add" and src.type == CS_OP_REG and fam(y.reg_name(src.reg)) in live:
                        live.add(dst)
                    elif y.mnemonic == "lea" and src.type == CS_OP_MEM and (
                            (src.mem.base and fam(y.reg_name(src.mem.base)) in live) or
                            (src.mem.index and fam(y.reg_name(src.mem.index)) in live)):
                        live.add(dst)
                    elif y.mnemonic in ("mov", "movzx", "movsx", "movsxd", "lea", "xor", "pop") and dst in live:
                        live.discard(dst)
                if y.mnemonic in ("ret", "jmp") or (y.mnemonic == "call"):
                    if y.mnemonic != "call":
                        break
                    for r_ in ("rax", "rcx", "rdx", "r8", "r9", "r10", "r11"):
                        live.discard(r_)
                if not live:
                    break
print("  qword loads (mov/add) of +0xC8/+0xD0/+0xE0 image-wide: %d" % nload)
byroot = collections.defaultdict(list)
for a in sorted(found):
    byroot[root(a)].append(a)
for r_ in sorted(byroot, key=lambda z: z or 0):
    print("  root %s: %s" % ("%08X" % r_ if r_ else "--------",
                             ", ".join("%08X(%s %s <- %08X +0x%X)" % (a, found[a][0][2], found[a][0][3], found[a][0][0], found[a][0][1]) for a in byroot[r_])))
print("  of the 14 P sites the sweep finds: %d (%s missing)" % (sum(1 for a in P14 if a in found),
      [("%08X" % a) for a in P14 if a not in found]))
print("  sweep hits outside the 14 P sites: %d" % sum(1 for a in found if a not in P14))

print("== T. tables")
kinds = {}
for idn in list(range(0x405, 0x410)) + [0x5A2, 0x5AE, 0x5AF]:
    pass
print("  00D233A0 first 0x40 bytes: %s" % T.rd(0x00D233A0, 0x40).hex())
print("  00D23920 u16 x4: %s" % [hex(x) for x in struct.unpack("<4H", T.rd(0x00D23920, 8))])
print("  00D23D60 bytes: %s ; 00D23D6C bytes: %s" % (T.rd(0x00D23D60, 12).hex(), T.rd(0x00D23D6C, 8).hex()))
print("  00D0F990 bytes: %s ; 00D113B8[0..11]: %s" % (list(struct.unpack("<8b", T.rd(0x00D0F990, 8))), list(T.rd(0x00D113B8, 12))))
