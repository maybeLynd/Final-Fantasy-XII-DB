"""What the native callers of the draw-pass mask setters pass.

The pass-mask block at 022C7F90 is two 4-byte entries (pass 0 and pass 1: a low word of pass bits 0..8 and an upper
word of four more bits) followed by three bytes at +8, +9 and +0xA. For every direct call or tail jump to one of its
setters, walk the twelve instructions before it forward (linear, not following branches), tracking registers loaded
with constants (mov imm, xor self, mov reg, lea reg+imm), and print ecx (pass index; or the value, for the
one-argument setters) and edx (value). An unresolved source is printed as written.
The setters and what each writes were read from their bodies and are listed in SETTERS.
"""
import struct
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
BASE = 0x120000
SETTERS = {0x003586E0: "bit0", 0x00358580: "bit1", 0x00358670: "bit2", 0x00358720: "bit3", 0x00358780: "bit4",
           0x00358610: "bit5", 0x003585B0: "bit6", 0x003585E0: "bit7", 0x00358750: "bit8",
           0x00358450: "bits0-7 together (bit8 cleared, upper word |= 0xF)",
           0x003586C0: "pass0 upper word bit0 (value in ecx)", 0x00358560: "pass0 upper word bit1 (value in ecx)",
           0x00358650: "pass0 upper word bit2 (value in ecx)", 0x00358700: "pass0 upper word bit3 (value in ecx)",
           0x00358640: "byte+8 (value in ecx)", 0x003587B0: "byte+9 (value in ecx)"}
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
       "r12": "r12d", "r13": "r13d", "r14": "r14d", "r15": "r15d"}
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
            else:
                val = known.get(N64.get(inner, inner))
        if b.mnemonic in ("mov", "lea", "xor", "movzx", "movsx", "and", "or", "add", "sub"):
            if val is None:
                known.pop(dst, None)
                expr[dst] = ops[1]
            else:
                known[dst] = val
                expr.pop(dst, None)
    return {r: (str(known[r]) if r in known else expr.get(r, "?")) for r in ("ecx", "edx")}


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
    if fo is None or size <= 0 or fa in SETTERS:
        continue
    body = d[fo:fo + size]
    ins = list(md.disasm(body, fa))
    for k, x in enumerate(ins):
        if x.mnemonic not in ("call", "jmp"):
            continue
        try:
            t = int(x.op_str, 16)
        except ValueError:
            continue
        if t not in SETTERS:
            continue
        got = track(ins[max(0, k - 12):k])
        rows.append((fa, name, x.address, t, SETTERS[t], got["ecx"], got["edx"] if "value in ecx" not in SETTERS[t] else "-"))
print("# call or jump sites %d in %d functions" % (len(rows), len({r[0] for r in rows})))
print("caller\tcaller_name\tsite\tsetter\twrites\tecx\tedx")
for r in rows:
    print("%08X\t%s\t%08X\t%08X\t%s\t%s\t%s" % r)
