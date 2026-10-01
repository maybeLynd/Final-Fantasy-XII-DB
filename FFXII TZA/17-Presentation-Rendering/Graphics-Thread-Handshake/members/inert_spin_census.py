"""Image-wide census of the *hoisted-load spin*: a backward conditional jump whose whole loop body can change
nothing it tests - every instruction from the jump target to the jump is `test`, `cmp`, `nop` or `pause` on
registers or immediates only (no memory operand, no call, no register write). Such a loop either falls through on
its first pass or never ends; it cannot wait for anything.

Positive control: GraphicsSync_WaitBackendState100ClearAndResetSharedState (0036F2F0) must be reported.
Negative control: the eleven two-load settle loops on 02EBA3F8 must NOT be reported (their bodies load memory).
"""
import struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM

EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
BASE = 0x120000
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
o = pe + 24 + opt
for i in range(nsec):
    vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs.append((va, ro, rs))
    o += 40


def off(va):
    rva = va - BASE
    for a, ro, rs in secs:
        if a <= rva < a + rs:
            return ro + rva - a
    return None


md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True
OK = {"test", "cmp", "nop", "pause"}
funcs = []
for l in open(FUNCS, encoding="utf-8", errors="replace"):
    p = l.split("\t")
    try:
        funcs.append((int(p[0], 16), p[1], int(p[2])))
    except (ValueError, IndexError):
        pass
hits = []
nf = 0
for fa, name, size in funcs:
    fo = off(fa)
    if fo is None or size <= 0:
        continue
    nf += 1
    ins = list(md.disasm(d[fo:fo + size], fa))
    idx = {x.address: k for k, x in enumerate(ins)}
    for k, x in enumerate(ins):
        if not (x.mnemonic.startswith("j") and x.mnemonic not in ("jmp",)):
            continue
        try:
            tgt = int(x.op_str, 16)
        except ValueError:
            continue
        if not (fa <= tgt <= x.address) or tgt not in idx:
            continue
        body = ins[idx[tgt]:k]
        if not body or len(body) > 6:
            continue
        good = True
        for b in body:
            if b.mnemonic not in OK:
                good = False
                break
            if b.mnemonic in ("test", "cmp") and any(op.type == X86_OP_MEM for op in b.operands):
                good = False
                break
        if good:
            hits.append((x.address, tgt, fa, name, "; ".join("%s %s" % (b.mnemonic, b.op_str) for b in body) + "; " + x.mnemonic))
print("# functions scanned %d; inert backward loops %d" % (nf, len(hits)))
print("jump\ttarget\tfunction\tname\tbody")
for h in hits:
    print("%08X\t%08X\t%08X\t%s\t%s" % h)
