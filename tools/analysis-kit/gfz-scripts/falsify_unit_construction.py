"""falsify_unit_construction.py - falsification pass 1 on 04-Actor-Entity/Unit-Definition/CONTRACT-battle-unit-construction.md
(OPUS, 2026-09-30). Static; reads only the shipping image. Each check is one of the contract's clauses at its bytes.

B1  §2 0023A570 is 1,808 bytes; class = (id >> 8) & 0xFF (0023A580, 0023A585, 0023A594), row = id & 0xFF (0023A58B)
B2  §2 teardown releases the spawn, then re-applies 0xFFFF: 00300F6D mov edx, 0xffff; 00300F75 call 0023A570
B3  I2 0023A5B0 calls the reset 00236A60, and the master flag d[02089300] is tested after it
B4  §2 the party path nulls the spawn: 0023AAB1 xor ebp, ebp
B5  I1 0023A633 and 0023AC4B mask qword [unit] with 0xFFFFFFFFFBFFFFFF; the enemy path's early refusals
    (0023A643-0023A648, 0023A65F-0023A662) jump to 0023A63A, past 0023A633
B6  I3 00322050 clears +0xEA4 / +0xEA8, resolves q[unit + 0x10] and stores the handle at +8
B7  I6 the spawn block is gated by byte [spawn] & 5 == 0
B8  I6 0023A965-0023A9F4 installs +0xE70 from [02EBF148] by +0x22 and +0xE78 from [02EBF140] by +0x24, the row address
    formed by a 32-bit add ecx, eax
B9  I7 00328FF0 writes {slot, code} into 02EC1380 with stride 24 under a signed row < 2 check
B10 I8 002FEAB0 is ten bytes that zero the qword at +0xEAC; class 1 converts byte +0x27 to float into +0x6C; the x1.5 is
    on class 0's byte +0x2B path
"""
import os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "FFXII TZA", "_index", "candidates", "rc9-log-channels-0930"))
import rc9_channels as R  # noqa: E402
from capstone import x86 as X  # noqa: E402

at, md, ext = R.at, R.md, R.ext
F = 0x0023A570
results = []


def check(cid, ok, what):
    results.append((cid, ok))
    print("%-4s %-9s %s" % (cid, "SURVIVES" if ok else "BROKEN", what))


def body(f, n=None):
    return list(md.disasm(at(f, n or ext[f]), f))


b = body(F)


def win(lo, hi, bb=None):
    return ["%s %s" % (i.mnemonic, i.op_str) for i in (bb or b) if lo <= i.address <= hi]


def ins(a):
    i = R.dec(a)
    return "%s %s" % (i.mnemonic, i.op_str)


def rip(i):
    for op in i.operands:
        if op.type == X.X86_OP_MEM and op.mem.base == X.X86_REG_RIP:
            return i.address + i.size + op.mem.disp
    return None


split = [ins(a) for a in (0x0023A580, 0x0023A585, 0x0023A594, 0x0023A58B)]
check("B1", ext[F] == 1808 and split == ["mov eax, edx", "sar eax, 8", "movzx esi, al", "movzx r12d, dl"],
      "extent %d B; %s" % (ext[F], split))

td = [ins(0x00300F6D), ins(0x00300F75)]
check("B2", td == ["mov edx, 0xffff", "call 0x23a570"], "%s" % td)

after = [i for i in b if 0x0023A5B0 < i.address < 0x0023A620 and rip(i) == 0x02089300]
check("B3", ins(0x0023A5B0) == "call 0x236a60" and bool(after),
      "0023A5B0 `%s`; master flag 02089300 read after it at %s" % (ins(0x0023A5B0), ["%08X" % i.address for i in after]))

check("B4", ins(0x0023AAB1) == "xor ebp, ebp", "0023AAB1 `%s`" % ins(0x0023AAB1))

m1, m2 = ins(0x0023A633), ins(0x0023AC4B)
refusals = [i for i in b if (0x0023A643 <= i.address <= 0x0023A648 or 0x0023A65F <= i.address <= 0x0023A662)
            and i.mnemonic.startswith("j") and i.operands[0].type == X.X86_OP_IMM]
tgt = sorted(set(i.operands[0].imm for i in refusals))
check("B5", m1.endswith(", 0xfffffffffbffffff") and m2.endswith(", 0xfffffffffbffffff") and tgt == [0x0023A63A] and 0x0023A63A > 0x0023A633,
      "0023A633 `%s`; 0023AC4B `%s`; early refusals jump to %s" % (m1, m2, ["%08X" % t for t in tgt]))

rk = body(0x00322050)
rkt = " ; ".join("%s %s" % (i.mnemonic, i.op_str) for i in rk)
# the handle is a 32-bit value (a packed id): stored as a dword at +8
check("B6", "mov dword ptr [rcx + 0xea4], 0" in rkt and "mov byte ptr [rcx + 0xea8], 0" in rkt and "mov rcx, qword ptr [rcx + 0x10]" in rkt
      and "mov dword ptr [rbx + 8], eax" in rkt,
      "00322050: %s" % rkt[:300])

g5 = [("%08X %s %s" % (i.address, i.mnemonic, i.op_str)) for i in b if i.mnemonic == "test" and i.op_str.startswith("byte ptr [") and i.op_str.endswith("], 5")]
check("B7", bool(g5), "freshness tests `test byte [..], 5`: %s" % g5)

inst = [i for i in b if 0x0023A965 <= i.address <= 0x0023A9F4]
t8 = " ; ".join("%s %s" % (i.mnemonic, i.op_str) for i in inst)
refs = sorted(set(rip(i) for i in inst if rip(i) in (0x02EBF140, 0x02EBF148)))
check("B8", refs == [0x02EBF140, 0x02EBF148] and "+ 0xe70]" in t8 and "+ 0xe78]" in t8 and "+ 0x22]" in t8 and "+ 0x24]" in t8 and "add ecx, eax" in t8,
      "install window: tables %s; +0xE70/+0xE78/+0x22/+0x24 and `add ecx, eax` present: %s" % (
          ["%08X" % r for r in refs], all(x in t8 for x in ("+ 0xe70]", "+ 0xe78]", "+ 0x22]", "+ 0x24]", "add ecx, eax"))))

tr = body(0x00328FF0)
t9 = " ; ".join("%s %s" % (i.mnemonic, i.op_str) for i in tr)
tab = [rip(i) for i in tr if rip(i)]
stride = any(("0x18" in i.op_str and i.mnemonic in ("imul", "lea")) or (i.mnemonic == "lea" and "*2]" in i.op_str) for i in tr) and ("*8" in t9)
signed = any(i.mnemonic in ("jge", "jg", "jl", "jle") for i in tr)
check("B9", 0x02EC1380 in tab and stride and signed and "cmp" in t9,
      "00328FF0 references %s; 24-byte stride formed %s; signed branch %s: %s" % (
          ["%08X" % t for t in tab], stride, signed, t9[:260]))

pr = body(0x002FEAB0, 16)
pr = pr[:next(k for k, i in enumerate(pr) if i.mnemonic == "ret") + 1]
size = pr[-1].address + pr[-1].size - 0x002FEAB0
# class 1: byte +0x27 -> movd xmm7 -> cvtdq2ps xmm7 with no multiply on xmm7 in that path (0023A8F8-0023A948);
# class 0: byte +0x2B -> xmm7 -> cvtdq2ps -> mulss xmm7 by the 1.5f at 00901B3C (0023ABAD); common store [rdi + 0x6c], xmm7
c1w = win(0x0023A8F8, 0x0023A948)
c0w = [i for i in b if 0x0023AB58 <= i.address <= 0x0023ABDC]
c1 = "movzx ecx, byte ptr [r15 + 0x27]" in c1w and "movd xmm7, ecx" in c1w and "cvtdq2ps xmm7, xmm7" in c1w     and not any(x.startswith(("mulss xmm7", "divss xmm7")) for x in c1w)
mul15 = [i for i in c0w if i.mnemonic == "mulss" and i.op_str.startswith("xmm7,") and rip(i) and at(rip(i), 4)
         and struct.unpack("<I", at(rip(i), 4))[0] == 0x3FC00000]
c0 = any(i.op_str == "r12d, byte ptr [rsi + 0x2b]" for i in c0w) and any(i.mnemonic == "cvtdq2ps" and i.op_str == "xmm7, xmm7" for i in c0w) and bool(mul15)
store = ins(0x0023ABD6) == "movss dword ptr [rdi + 0x6c], xmm7"
check("B10", size == 10 and "mov qword ptr [rcx + 0xeac], rax" in [("%s %s" % (i.mnemonic, i.op_str)) for i in pr] and c1 and c0 and store,
      "002FEAB0 (%d B): %s; class 1 +0x27 -> xmm7 float, no multiply: %s; class 0 +0x2B -> xmm7 x 1.5f at %s: %s; "
      "0023ABD6 `%s`" % (size, " ; ".join("%s %s" % (i.mnemonic, i.op_str) for i in pr), c1,
                        ["%08X" % i.address for i in mul15], c0, ins(0x0023ABD6)))

broken = [c for c, ok in results if not ok]
print("BROKEN %d: %s" % (len(broken), " ".join(broken) or "none"))
sys.exit(0)
