r"""uq38_example.py - UQ-38: a concrete carried value inside a 'whole' translated member (FABLE, Claude Opus 5.5,
2026-09-27). The row's proposed criterion assumed 'a translation reloads every operand from the bank'. This prints the
first xmm register in 003CD840 (21,276 B, the largest member both instruments call whole) that is written, survives a
bank store, and is read after it in the same basic block - the pattern the criterion says only C produces.
E1 such a triple exists in 003CD840. E2 control: the same search over a stretch with no bank stores finds none.
Exit 1 on any FAIL.
"""
import struct, sys, re
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if 0x120000 + va <= v < 0x120000 + va + rs: return v - 0x120000 - va + ro
def in_bank(t): return 0x022D8F10 <= t < 0x022D93C0 or 0x01EF93F0 <= t < 0x01EF9400
STORE = re.compile(r"^(mov|movaps|movups|movss|movsd|movq|movd|movdqa|movdqu|movlps|movhps)")
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
def first_triple(addr, size):
    ins = list(cs.disasm(d[off(addr):off(addr) + size], addr))
    targets = {o.imm for x in ins if x.group(1) or x.group(7) for o in x.operands if o.type == 2}
    defs, last_store = {}, None
    for i, x in enumerate(ins):
        if x.address in targets: defs, last_store = {}, None
        rr, rw = x.regs_access()
        for r in (cs.reg_name(q) for q in rr):
            if r.startswith("xmm") and r in defs and last_store is not None and last_store[0] > defs[r][0]:
                return defs[r][1], last_store[1], x
        o = x.operands
        if o and o[0].type == X86_OP_MEM and o[0].mem.base == X86_REG_RIP and STORE.match(x.mnemonic) and in_bank(x.address + x.size + o[0].mem.disp):
            last_store = (i, x)
        for r in (cs.reg_name(q) for q in rw):
            if r.startswith("xmm"): defs[r] = (i, x)
        if x.mnemonic in ("call", "ret") or x.mnemonic.startswith("j"): defs, last_store = {}, None
    return None
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
t = first_triple(0x3CD840, 21276)
fmt = lambda x: "%08X %s %s" % (x.address, x.mnemonic, x.op_str)
check("E1 a register value carried across a bank store in 003CD840", t is not None,
      " | ".join(fmt(x) for x in t) if t else "")
t0 = first_triple(0x861EC0, 0x40)  # memset head: no bank stores
check("E2 control: no triple where there is no bank store (00861EC0)", t0 is None)
print("FAILS", fails); sys.exit(1 if fails else 0)
