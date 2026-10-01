"""c20_indep.py - SWE2-AUDIT-SPEC independent re-derivation for ASTRA ov42-class20-action-admission (2026-09-30).

Not the packet's drivers. Image via ../auditspec-review-ov31-type-store-0929/ov31_indep.py (sha asserted).
  A  class dispatch of 00322C50: bound, image-base-relative jump table at 00323054 (32 entries), entry 19 target
  B  the caller 0030CC25..0030CC32 and how the same slot word becomes the row pointer given to 0030CE10
  C  every direct/jcc/data reference to 0030CE10 and 0030CBE0
  D  the descriptor installer 003845F0: which header fields it rewrites (is +4, the count, among them?)
  E  EMULATION (isolated original code, unicorn): 00322C50 run from its entry with ecx=0x14 for all 65536 edx values,
     with INJECTED state: the qword 02EBF138 set to a fake st2e header whose +4 is 543 (and controls 0 / null / 511).
     Nothing else of the game is initialised; the class-20 arm reads only 02EBF138 and [desc+4].
"""
import os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "auditspec-review-ov31-type-store-0929"))
import ov31_indep as T  # noqa: E402
from unicorn import Uc, UC_ARCH_X86, UC_MODE_64, UC_HOOK_MEM_UNMAPPED, UC_HOOK_CODE
from unicorn.x86_const import UC_X86_REG_RSP, UC_X86_REG_RCX, UC_X86_REG_RDX, UC_X86_REG_RAX, UC_X86_REG_RIP, \
    UC_X86_REG_R8


def p(*a):
    print(" ".join(str(x) for x in a))


def show(a, b):
    for i in T.dis(a, b):
        p("   %08X %-7s %s" % (i.address, i.mnemonic, i.op_str))


p("== A 00322C50 dispatch")
show(0x322C50, 0x322C7E)
jt = [struct.unpack_from("<I", T.rd(0x323054, 128), 4 * k)[0] + 0x120000 for k in range(32)]
p("   table 00323054 (32 x rva32):", " ".join("%d:%06X" % (k, v) for k, v in enumerate(jt)))
p("   class 0x14 -> index 19 -> %08X" % jt[19])
show(jt[19], jt[19] + 0x17)
show(0x32302A, 0x323051)

p("== B caller 0030CBE0 (slot list walk), class-20 call and the row pointer")
show(0x30CC11, 0x30CC92)
show(0x30CD93, 0x30CD9E)

p("== C references")
for tgt in (0x30CE10, 0x30CBE0, 0x322C50):
    rc = T.rel32_callers(tgt)
    p("   %08X rel32 %d%s jcc %s data %s" % (tgt, len(rc), (" " + str(rc)) if len(rc) < 5 else "", T.jcc_callers(tgt),
                                           T.data_refs(tgt)))
p("   class-20 call sites among 00322C50 callers (ecx=0x14 set in the 3 instructions before the call):")
n20 = []
for s in T.rel32_callers(0x322C50):
    va = int(s.split()[0], 16)
    ok = None
    for st in range(va - 40, va):  # first back-decode start whose linear decode lands exactly on the call
        seq = T.dis(st, va + 5)
        if any(i.address == va for i in seq):
            ok = [i for i in seq if i.address < va]
            break
    if ok and any(i.mnemonic == "mov" and i.op_str == "ecx, 0x14" for i in ok[-3:]):
        n20.append("%08X" % va)
p("   ", len(n20), n20, "(known positive 0030CC32 present: %s)" % ("0030CC32" in n20))

p("== D 003845F0 header fields rewritten")
for i in T.dis(0x3845F0, 0x384665):
    if i.mnemonic in ("mov", "add") and i.op_str.startswith("dword ptr [r"):
        p("   %08X %s %s" % (i.address, i.mnemonic, i.op_str))

p("== E emulation of 00322C50 (class 0x14)")
PAGE = 0x1000
mu = Uc(UC_ARCH_X86, UC_MODE_64)
for n, v, vs, po, rs, x in T.SECS:
    lo = v & ~(PAGE - 1); hi = (v + max(vs, rs) + PAGE - 1) & ~(PAGE - 1)
    mu.mem_map(lo, hi - lo)
    mu.mem_write(v, T.raw[po:po + min(vs, rs)])
STACK = 0x70000000; mu.mem_map(STACK, 0x10000)
DESC = 0x71000000; mu.mem_map(DESC, 0x1000)
RET = 0x72000000; mu.mem_map(RET, 0x1000); mu.mem_write(RET, b"\xf4")
bad = []
mu.hook_add(UC_HOOK_MEM_UNMAPPED, lambda uc, acc, addr, size, val, ud: bad.append(hex(addr)) or False)
calls = []


def on_code(uc, addr, size, ud):
    b = bytes(uc.mem_read(addr, 1))
    if b == b"\xe8":
        calls.append(hex(addr))


mu.hook_add(UC_HOOK_CODE, on_code, begin=0x322C50, end=0x323051)


def run(word, desc_count, null=False):
    mu.mem_write(0x2EBF138, struct.pack("<Q", 0 if null else DESC))
    mu.mem_write(DESC, b"st2e" + struct.pack("<IHH", desc_count, 60, 0))
    rsp = STACK + 0x8000
    mu.mem_write(rsp, struct.pack("<Q", RET))
    mu.reg_write(UC_X86_REG_RSP, rsp)
    mu.reg_write(UC_X86_REG_RCX, 0x14); mu.reg_write(UC_X86_REG_RDX, word); mu.reg_write(UC_X86_REG_R8, 1)
    mu.emu_start(0x322C50, RET, count=200)
    return mu.reg_read(UC_X86_REG_RAX) & 0xFFFFFFFF


for label, cnt, null in (("count 543", 543, False), ("count 511 (control)", 511, False), ("count 0 (control)", 0, False),
                         ("null descriptor (control)", 543, True)):
    acc = [w for w in range(65536) if run(w, cnt, null) == 1]
    rng = "none" if not acc else "%d..%d (%d ids, contiguous %s)" % (acc[0], acc[-1], len(acc),
                                                                     acc == list(range(acc[0], acc[-1] + 1)))
    p("   %-28s accepted %s ; 511..534 all accepted: %s" % (label, rng, all(w in acc for w in range(511, 535))))
p("   unmapped accesses:", bad[:5], " direct calls executed inside 00322C50:", sorted(set(calls)))
