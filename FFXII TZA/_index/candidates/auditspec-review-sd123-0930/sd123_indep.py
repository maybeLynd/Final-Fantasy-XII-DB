"""sd123_indep.py - SWE2-AUDIT-SPEC independent re-derivation for SD-123 (review of OPUS 524d5aacd, 2026-09-30).

Uses this lane's loader ../auditspec-review-ov31-type-store-0929/ov31_indep.py (sha256 asserted), not retool.py.

  A  the record-store table: every abs64 slot holding the loader 00500C00, with the neighbouring qwords, so the kind
     id the slot belongs to is read from the table, not from the page.
  B  the format byte: every write to [rdi+0xA0] in the loader 00500C00..005010EB (linear decode), to show what values
     +0xA0 can hold when the palette switch (00500CE1) and the jump table (00500EE4) read it.
  C  the format jump table at 00500EF1..00500F0A: byte index table (IB + 0x3E110C) and dword arm table (IB + 0x3E10EC),
     decoded for every index 0..0x81; each arm's creator call and the +0xB8 value it stores.
  D  the palette loops: per-palette stride, entry count and the data pointer given to 001837A0 and 00183760.
  E  callers of 00500C00 (rel32, jcc, data slots) and of the helper 003AA280 with edx = 0x52 (the mesh / group
     resolvers), to check I4.
  Controls: A must find the 00500C00 slot (known positive: the page names it); C's index table must send index 0 and 1
  to different arms (a decode that collapses all arms to one would show as one target); B must find the first
  store at 00500C2A (known positive).
"""
import os, struct, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402
from capstone.x86 import X86_REG_RDI

IB = T.IB


def q(va):
    return struct.unpack_from("<Q", T.raw, T.off(va))[0]


def line(i):
    return "%08X  %-8s %s" % (i.address, i.mnemonic, i.op_str)


print("== A record-store slots holding 00500C00 (abs64), with neighbours")
dr = T.data_refs(0x00500C00)
print("  data_refs(00500C00):", dr)
for s in dr["abs64"]:
    va = int(s.split("(")[0], 16)
    for k in range(-4, 5):
        v = q(va + 8 * k)
        print("   %08X %+d: %016X" % (va + 8 * k, k, v))

print("== B writes to [rdi+0xA0] inside 00500C00..005010EB")
ins = T.dis(0x00500C00, 0x005010EB)
for i in ins:
    for m, s in T.mem_ops(i):
        if m.base == X86_REG_RDI and m.disp in (0xA0,) and m.index == 0:
            first_is_mem = i.op_str.split(",")[0].strip().endswith("]")
            if first_is_mem and i.mnemonic not in ("cmp", "test"):
                print("  WRITE " + line(i))
            else:
                print("  read  " + line(i))

print("== C format jump table")
bidx = IB + 0x3E110C
dtab = IB + 0x3E10EC
arms = {}
for f in range(0, 0x82):
    b = T.raw[T.off(bidx + f)]
    tgt = IB + struct.unpack_from("<I", T.raw, T.off(dtab + 4 * b))[0]
    arms.setdefault(tgt, []).append(f)
nidx = max(T.raw[T.off(bidx + f)] for f in range(0x82))
print("  index-table max entry %d -> %d dword arms" % (nidx, nidx + 1))
for tgt, fs in sorted(arms.items()):
    body = T.dis(tgt, count=40)
    call = next((i for i in body if i.mnemonic == "call"), None)
    b8 = next((i for i in body if i.mnemonic == "mov" and "[rdi + 0xb8]" in i.op_str), None)
    shown = fs if len(fs) <= 8 else fs[:4] + ["..."] + fs[-2:]
    print("  arm %08X  formats %s (n=%d)  call %s  %s" % (
        tgt, ["0x%X" % x if isinstance(x, int) else x for x in shown], len(fs),
        call.op_str if call else "-", b8.op_str if b8 else "-"))

print("== D palette loops")
for a in (0x00500D20, 0x00500D80):
    for i in T.dis(a, count=22):
        if i.mnemonic in ("call", "add", "shl") or "edx" in i.op_str or "ecx" in i.op_str or "r8d" in i.op_str:
            print("  " + line(i))
        if i.mnemonic == "jl":
            print("  " + line(i))
            break
    print("  --")

print("== E callers")
print("  00500C00 rel32", T.rel32_callers(0x00500C00), "jcc", T.jcc_callers(0x00500C00))
print("  00500BF0 rel32", T.rel32_callers(0x00500BF0), "data", T.data_refs(0x00500BF0))
print("  00500B70 rel32", T.rel32_callers(0x00500B70), "data", T.data_refs(0x00500B70))
print("  I4 mesh site 00437090..004370F0:")
for i in T.dis(0x00437090, 0x004370F0):
    print("   " + line(i))
print("  I4 evaluator site 00431AB0..00431B00:")
for i in T.dis(0x00431AB0, 0x00431B00):
    print("   " + line(i))
