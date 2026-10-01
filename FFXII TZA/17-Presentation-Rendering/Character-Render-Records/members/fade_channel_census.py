"""Who drives which fade channel of a character render record.

The record holds ten 8-byte channels at +0x4C0 ({base, delta, progress, step}, Q12). Three functions address a
channel by index in edx: the ramp starter 003E5D60 (record, channel, target, frames), the immediate setter 003E5D00
(record, channel, value) and the evaluator 003E48E0 (record, selector), whose selectors 0xB, 0xD and 0xE are
products of several channels. For every direct call or tail jump to one of them, walk the sixteen instructions
before it forward (linear, not following branches), tracking registers loaded with constants, and print edx.
Control: the three call counts must equal an independent raw E8/E9 sweep (rawcalls).
"""
import struct
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
BASE = 0x120000
TARGETS = {0x003E5D60: "start_ramp", 0x003E5D00: "set_immediate", 0x003E48E0: "evaluate"}
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


N64 = {"rcx": "ecx", "rdx": "edx", "rbx": "ebx", "rax": "eax", "rsi": "esi", "rdi": "edi", "rbp": "ebp",
       "r8": "r8d", "r9": "r9d", "r12": "r12d", "r13": "r13d", "r14": "r14d", "r15": "r15d"}
VOLATILE = ("eax", "ecx", "edx", "r8d", "r9d", "r10d", "r11d")


def track(window):
    known, expr = {}, {}
    for b in window:
        ops = b.op_str.split(", ")
        if b.mnemonic == "call":
            for r in VOLATILE:
                known.pop(r, None)
                expr.pop(r, None)
            continue
        if len(ops) != 2:
            continue
        dst = N64.get(ops[0], ops[0])
        src = N64.get(ops[1], ops[1])
        val = None
        if b.mnemonic == "xor" and ops[0] == ops[1]:
            val = 0
        elif b.mnemonic == "mov":
            try:
                val = int(src, 0)
            except ValueError:
                val = known.get(src)
        elif b.mnemonic == "lea" and src.startswith("["):
            inner = src.strip("[]")
            if " + " in inner:
                base, add = inner.split(" + ", 1)
                base = N64.get(base, base)
                try:
                    val = known[base] + int(add, 0) if base in known else None
                except ValueError:
                    val = None
            elif " - " in inner:
                base, add = inner.split(" - ", 1)
                base = N64.get(base, base)
                try:
                    val = known[base] - int(add, 0) if base in known else None
                except ValueError:
                    val = None
            else:
                val = known.get(N64.get(inner, inner))
        if b.mnemonic in ("mov", "lea", "xor", "movzx", "movsx", "movsxd", "and", "or", "add", "sub"):
            if val is None:
                known.pop(dst, None)
                expr[dst] = ops[1]
            else:
                known[dst] = val
                expr.pop(dst, None)
    return str(known["edx"]) if "edx" in known else expr.get("edx", "?")


md = Cs(CS_ARCH_X86, CS_MODE_64)
funcs = []
for l in open(FUNCS, encoding="utf-8", errors="replace"):
    p = l.split("\t")
    try:
        funcs.append((int(p[0], 16), p[1], int(p[2])))
    except (ValueError, IndexError):
        pass
rows = []
for fa, name, size in funcs:
    fo = off(fa)
    if fo is None or size <= 0 or fa in TARGETS:
        continue
    ins = list(md.disasm(d[fo:fo + size], fa))
    for k, x in enumerate(ins):
        if x.mnemonic not in ("call", "jmp"):
            continue
        try:
            t = int(x.op_str, 16)
        except ValueError:
            continue
        if t in TARGETS:
            rows.append((TARGETS[t], track(ins[max(0, k - 16):k]), fa, name, x.address))
for what in ("start_ramp", "set_immediate", "evaluate"):
    print("# %s sites %d" % (what, sum(1 for r in rows if r[0] == what)))
print("operation\tchannel_or_selector\tcaller\tcaller_name\tsite")
for r in sorted(rows, key=lambda r: (r[0], r[1], r[2], r[4])):
    print("%s\t%s\t%08X\t%s\t%08X" % r)
