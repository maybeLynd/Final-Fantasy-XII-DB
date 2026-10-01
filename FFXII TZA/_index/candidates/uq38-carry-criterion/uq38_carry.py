"""UQ-38: per member, the fraction of xmm register uses whose value was defined BEFORE the most recent bank store in the
same basic block (a value carried in a register across a bank store = C-like; a translation reloads from the bank)."""
import struct, csv, re, collections, statistics
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_REG, X86_OP_MEM, X86_REG_RIP
from pathlib import Path as _P
ROOT = str(_P(__file__).resolve().parents[5]).replace("\\", "/") + "/"
d = open(ROOT + "Database/Tools/work/exe/FFXII_TZA.exe", "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if 0x120000 + va <= v < 0x120000 + va + rs: return v - 0x120000 - va + ro
def in_bank(t): return 0x022D8F10 <= t < 0x022D93C0 or 0x01EF93F0 <= t < 0x01EF9400
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
MEMBERS = ROOT + "Database/FFXII TZA/00-Engine-Core-Runtime/Shared-Transform-Workbench/members/"
calls = {r["function"]: r for r in csv.DictReader(open(MEMBERS + "ee-member-calls.tsv", encoding="utf-8"), delimiter="\t")}
STORE_MN = re.compile(r"^(mov|movaps|movups|movss|movsd|movq|movd|movdqa|movdqu|movlps|movhps|stmxcsr)")
def metric(addr, size):
    ins = list(cs.disasm(d[off(addr):off(addr) + size], addr))
    targets = set()
    for x in ins:
        if x.group(1) or x.group(7):  # jump or branch-relative
            for o in x.operands:
                if o.type == 2: targets.add(o.imm)
    carried = total = 0; stores = 0
    defs = {}; last_store = -1
    for i, x in enumerate(ins):
        if x.address in targets: defs = {}; last_store = -1
        regs_read, regs_write = x.regs_access()
        xr = [cs.reg_name(r) for r in regs_read if cs.reg_name(r).startswith("xmm")]
        xw = [cs.reg_name(r) for r in regs_write if cs.reg_name(r).startswith("xmm")]
        for r in xr:
            if r in defs:
                total += 1
                if last_store > defs[r]: carried += 1
        # bank store?
        ops = x.operands
        if ops and ops[0].type == X86_OP_MEM and ops[0].mem.base == X86_REG_RIP and STORE_MN.match(x.mnemonic):
            t = x.address + x.size + ops[0].mem.disp
            if in_bank(t): last_store = i; stores += 1
        for r in xw: defs[r] = i
        if x.mnemonic in ("call", "ret") or x.mnemonic.startswith("j"):
            defs = {}; last_store = -1
    return carried, total, stores
rows = []
for f, r in calls.items():
    a = int(f, 16); size = int(r["size"])
    c, t, s = metric(a, size)
    rows.append((f, r["verdict"], r["frontier_split"], c, t, s, c / t if t else None))
grp = collections.defaultdict(list)
for f, v, fs, c, t, s, m in rows:
    key = "whole" if v == "whole" else ("C-agreed" if v == "C+fragments" and fs == "C+fragments" else ("undecided" if fs == "translated" and v != "whole" else "other:" + v + "/" + fs))
    if m is not None: grp[key].append(m)
for k, v in sorted(grp.items()):
    v = sorted(v)
    print("%-28s n=%3d  min %.3f  p25 %.3f  median %.3f  p75 %.3f  max %.3f" % (k, len(v), v[0], v[len(v)//4], statistics.median(v), v[3*len(v)//4], v[-1]))
with open(str(_P(__file__).resolve().parent / "uq38_carry.tsv"), "w", encoding="utf-8") as fo:
    fo.write("function\tverdict\tfrontier\tcarried\tuses\tbank_stores\tratio\n")
    for r in rows: fo.write("\t".join(str(x) for x in r) + "\n")
