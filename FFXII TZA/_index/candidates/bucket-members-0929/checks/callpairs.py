"""callpairs.py KIND ID [KIND ID ...] [--control SITE ...]
Every call (E8 direct, or call through register/memory) in every listed function, with the constant values the
argument registers hold at the call (linear forward constant tracking from the function start, as
res_request_census.py does; a call clobbers volatile registers). Reports every call site, to ANY target, where
(rcx, rdx) or (rdx, r8) carry one of the requested (KIND, ID) constant pairs. Catching every target (not just the
known request APIs) is the point: an enqueue wrapper or record builder that forwards the pair is found too.
--control SITE: a site that must be reported (FAIL otherwise). Prints FAILS n.
"""
import sys, struct, re, argparse
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_REG, X86_OP_MEM
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
BASE = 0x120000
ap = argparse.ArgumentParser(); ap.add_argument("pairs", nargs="+"); ap.add_argument("--control", nargs="*", default=[])
a = ap.parse_args()
vals = [int(x, 0) for x in a.pairs]; want = set(zip(vals[0::2], vals[1::2]))
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; ns = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(ns)]
def off(va):
    r = va - BASE
    for vs, sva, rs, ro in secs:
        if sva <= r < sva + min(vs, rs): return ro + r - sva
funcs = []
for l in open(FUNCS, encoding="utf-8", errors="replace"):
    p = l.split("\t")
    try: funcs.append((int(p[0], 16), p[1], int(p[2])))
    except (ValueError, IndexError): pass
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
VOL = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}
C32 = {"eax": "rax", "ecx": "rcx", "edx": "rdx", "ebx": "rbx", "esi": "rsi", "edi": "rdi", "ebp": "rbp", "r8d": "r8", "r9d": "r9",
       "r10d": "r10", "r11d": "r11", "r12d": "r12", "r13d": "r13", "r14d": "r14", "r15d": "r15"}
def canon(r): return C32.get(r, r)
hits = []; ncalls = 0
for f, name, sz in funcs:
    o = off(f)
    if o is None or sz <= 0: continue
    val = {}
    for ins in md.disasm(d[o:o + sz], f):
        ops = ins.operands
        if ins.mnemonic == "call":
            ncalls += 1
            for kr, ir in (("rcx", "rdx"), ("rdx", "r8")):
                k, i = val.get(kr), val.get(ir)
                if (k, i) in want: hits.append((ins.address, f, name, kr, k, i, ins.op_str))
            for r in VOL: val.pop(r, None)
            continue
        if ins.mnemonic in ("ret", "jmp") and not ins.op_str.startswith("0x"):
            val = {}; continue
        if len(ops) == 2 and ops[0].type == X86_OP_REG:
            dst = canon(ins.reg_name(ops[0].reg))
            if ins.mnemonic == "mov" and ops[1].type == X86_OP_IMM: val[dst] = ops[1].imm & 0xFFFFFFFF
            elif ins.mnemonic == "xor" and ops[1].type == X86_OP_REG and ops[1].reg == ops[0].reg: val[dst] = 0
            elif ins.mnemonic == "lea" and ops[1].type == X86_OP_MEM and ops[1].mem.base and not ops[1].mem.index and ins.reg_name(ops[1].mem.base) != "rip":
                b = canon(ins.reg_name(ops[1].mem.base))
                if isinstance(val.get(b), int): val[dst] = (val[b] + ops[1].mem.disp) & 0xFFFFFFFF
                else: val.pop(dst, None)
            elif ins.mnemonic == "mov" and ops[1].type == X86_OP_REG:
                sr = canon(ins.reg_name(ops[1].reg))
                if sr in val: val[dst] = val[sr]
                else: val.pop(dst, None)
            elif ins.mnemonic not in ("cmp", "test"): val.pop(dst, None)
        elif len(ops) == 1 and ops[0].type == X86_OP_REG and ins.mnemonic in ("inc", "dec", "pop", "neg", "not"):
            val.pop(canon(ins.reg_name(ops[0].reg)), None)
print(f"# call sites scanned: {ncalls}; wanted pairs: {sorted((hex(k), hex(i)) for k, i in want)}")
for s, f, name, kr, k, i, tgt in sorted(hits):
    print(f"{s:08X}\t{f:08X} {name}\t({kr}={k:#x}, next={i:#x})\tcall {tgt}")
fails = 0
sites = {h[0] for h in hits}
for c in a.control:
    ok = int(c, 16) in sites; fails += not ok
    print(f"CONTROL {c}: {'PASS' if ok else 'FAIL'}")
print(f"FAILS {fails}")
