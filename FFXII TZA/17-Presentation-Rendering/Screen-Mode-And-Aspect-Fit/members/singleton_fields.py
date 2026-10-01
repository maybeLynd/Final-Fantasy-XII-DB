"""singleton_fields.py GLOBAL GETTER [LO HI]: field accesses on an object reached as *GLOBAL.

Sources of the object pointer: `mov reg, [rip -> GLOBAL]` anywhere, and `rax` after `call GETTER`. From each source the
register is followed linearly (through plain `mov r2, r1` copies) until it is overwritten, a call clobbers a volatile
register, or 40 instructions pass. Every memory operand based on a tracked register is reported with its displacement
and access kind (w when the operand is the destination of mov/movss/movsd/movups/movaps/set*/inc/dec/add/sub/and/or/xor).
Optionally only displacements in [LO, HI] are printed. Linear tracking misses pointers stored and reloaded - stated,
not hidden."""
import sys, struct, bisect, collections
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_REG

EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
BASE = 0x120000
G = int(sys.argv[1], 16); GET = int(sys.argv[2], 16)
LO = int(sys.argv[3], 16) if len(sys.argv) > 3 else 0
HI = int(sys.argv[4], 16) if len(sys.argv) > 4 else 0xFFFFFFFF
sizes, names = {}, {}
for l in open(FUNCS, encoding="utf-8", errors="replace"):
    p = l.split("\t")
    try:
        sizes[int(p[0], 16)] = int(p[2]); names[int(p[0], 16)] = p[1]
    except (ValueError, IndexError):
        pass
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; ns = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(ns):
    o = pe + 24 + opt + i * 40
    secs.append((d[o:o + 8].rstrip(b"\0").decode(), *struct.unpack_from("<IIII", d, o + 8)))
text = [s for s in secs if s[0] == ".text"][0]


def v2o(v):
    for n, vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs:
            return v - BASE - va + ro


FULL = {"rax": "rax", "eax": "rax", "rcx": "rcx", "ecx": "rcx", "rdx": "rdx", "edx": "rdx", "rbx": "rbx", "ebx": "rbx",
        "rsi": "rsi", "esi": "rsi", "rdi": "rdi", "edi": "rdi", "rbp": "rbp", "ebp": "rbp"}
for k in range(8, 16):
    FULL["r%d" % k] = "r%d" % k; FULL["r%dd" % k] = "r%d" % k
VOLATILE = {"rax", "rcx", "rdx", "r8", "r9", "r10", "r11"}
WRITES = ("mov", "movss", "movsd", "movups", "movaps", "movdqa", "movdqu", "inc", "dec", "add", "sub", "and", "or", "xor")
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
hits = collections.defaultdict(list)
n, vs, va, rs, ro = text
for e in sorted(sizes):
    if not (BASE + va <= e < BASE + va + vs):
        continue
    o = v2o(e)
    if o is None:
        continue
    ins = list(md.disasm(d[o:o + sizes[e]], e))
    for i, x in enumerate(ins):
        start = None
        if x.mnemonic == "mov" and len(x.operands) == 2 and x.operands[1].type == X86_OP_MEM and x.operands[0].type == X86_OP_REG:
            m = x.operands[1].mem
            if m.base and x.reg_name(m.base) == "rip" and x.address + x.size + m.disp == G:
                start = FULL.get(x.reg_name(x.operands[0].reg))
        if x.mnemonic == "call" and x.op_str == hex(GET):
            start = "rax"
        if not start:
            continue
        tracked = {start}
        for y in ins[i + 1:i + 41]:
            ops = y.operands
            for k, op in enumerate(ops):
                if op.type == X86_OP_MEM and op.mem.base and FULL.get(y.reg_name(op.mem.base)) in tracked and not op.mem.index:
                    kind = "w" if (k == 0 and (y.mnemonic in WRITES or y.mnemonic.startswith("set"))) else "r"
                    if LO <= op.mem.disp <= HI:
                        hits[(op.mem.disp, kind)].append((y.address, e))
            if y.mnemonic == "mov" and len(ops) == 2 and ops[0].type == X86_OP_REG:
                dst = FULL.get(y.reg_name(ops[0].reg))
                if ops[1].type == X86_OP_REG and FULL.get(y.reg_name(ops[1].reg)) in tracked:
                    tracked.add(dst)
                elif dst in tracked:
                    tracked.discard(dst)
            elif y.mnemonic in ("lea", "xor", "pop", "movzx", "movsxd") and ops and ops[0].type == X86_OP_REG:
                tracked.discard(FULL.get(y.reg_name(ops[0].reg)))
            if y.mnemonic == "call":
                tracked -= VOLATILE
            if y.mnemonic in ("ret", "jmp") or not tracked:
                break
for (disp, kind), sites in sorted(hits.items()):
    fns = sorted(set(f for _, f in sites))
    print("+0x%02X %s  %3d sites  %2d fns  %s" % (disp, kind, len(sites), len(fns),
          " ".join("%08X:%s" % (a, names[f][:28]) for a, f in sorted(sites)[:6])))
