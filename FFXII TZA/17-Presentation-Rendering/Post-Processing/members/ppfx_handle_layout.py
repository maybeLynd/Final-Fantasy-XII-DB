"""UQ-224: where each post-processing handle lands in the TEXSHADERSET object.

Walks the catalogue body 0072A320 linearly. For every inline lookup
    lea rdx, [rip+NAME] ; call qword ptr [rax+SLOT] ; mov dword ptr [BASE+OFF], eax
it emits (offset, slot, name). For every family call (0072DCF0 suffix family, 0072EB20 numbered family,
0072DFD0 two-dimensional) it emits the out-pointer `lea rdx,[BASE+OFF]`, the name in r8 and the count in r9d.
Rows whose store or name does not resolve within the window are emitted as unresolved, not dropped.
"""
import struct, sys, re
import capstone

ROOT = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work"
d = open(ROOT + r"\exe\FFXII_TZA.exe", "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
secs = []
o = pe + 24 + struct.unpack_from("<H", d, pe + 20)[0]
for i in range(struct.unpack_from("<H", d, pe + 6)[0]):
    vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs.append((va, ro, rs))
    o += 40


def off(va):
    rva = va - 0x120000
    for a, ro, rs in secs:
        if a <= rva < a + rs:
            return ro + rva - a
    return None


def cstr(va):
    so = off(va)
    return d[so:so + 120].split(b"\0")[0].decode("latin1") if so is not None else None


HEAD, SIZE = 0x0072A320, 13547
FAM = {0x0072DCF0: "suffix-family", 0x0072EB20: "numbered-family", 0x0072DFD0: "two-dimensional"}
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True
ins = list(md.disasm(d[off(HEAD):off(HEAD) + SIZE], HEAD))
rows = []
for k, x in enumerate(ins):
    if x.mnemonic != "call":
        continue
    m = re.match(r"qword ptr \[r[a-z0-9]+ \+ (0x[0-9a-f]+)\]", x.op_str)
    if m and m.group(1) in ("0x60", "0x48"):
        name = None
        for y in reversed(ins[max(0, k - 6):k]):
            if y.mnemonic == "lea" and y.op_str.startswith("rdx, [rip"):
                name = cstr(y.address + y.size + y.operands[1].mem.disp)
                break
        dest = None
        for y in ins[k + 1:k + 4]:
            mm = re.match(r"dword ptr \[(r[a-z0-9]+) \+ (0x[0-9a-f]+)\], eax", y.op_str)
            if y.mnemonic == "mov" and mm:
                dest = (mm.group(1), int(mm.group(2), 16))
                break
        rows.append((dest[1] if dest else -1, dest[0] if dest else "?", "inline " + m.group(1), 1, name or "?", x.address))
        continue
    try:
        t = int(x.op_str, 16)
    except ValueError:
        continue
    if t in FAM:
        name = cnt = dest = None
        for y in reversed(ins[max(0, k - 10):k]):
            ops = y.op_str
            if name is None and y.mnemonic == "lea" and ops.startswith("r8, [rip"):
                name = cstr(y.address + y.size + y.operands[1].mem.disp)
            if cnt is None and y.mnemonic == "mov" and re.match(r"r9d, (0x[0-9a-f]+|\d+)$", ops):
                v = ops.split(",")[1].strip()
                cnt = int(v, 16) if v.startswith("0x") else int(v)
            # r15d holds the constant 1 for the whole body (mov r15d, 1 at 0072A85F, its only write),
            # and most counts are formed from it: lea r9d, [r15 + k] is 1 + k, mov r9d, r15d is 1.
            if cnt is None and y.mnemonic == "lea":
                mk = re.match(r"r9d, \[r15 \+ (0x[0-9a-f]+|\d+)\]$", ops)
                if mk:
                    v = mk.group(1)
                    cnt = 1 + (int(v, 16) if v.startswith("0x") else int(v))
            if cnt is None and y.mnemonic == "mov" and ops == "r9d, r15d":
                cnt = 1
            mm = re.match(r"rdx, \[(r[a-z0-9]+) \+ (0x[0-9a-f]+)\]", ops)
            if dest is None and y.mnemonic == "lea" and mm:
                dest = (mm.group(1), int(mm.group(2), 16))
        rows.append((dest[1] if dest else -1, dest[0] if dest else "?", FAM[t], cnt if cnt is not None else -1, name or "?", x.address))

res = sum(1 for r in rows if r[0] >= 0 and r[4] != "?")
bases = sorted({r[1] for r in rows})
offs = [r[0] for r in rows if r[0] >= 0]
print("# lookups %d  fully resolved %d  base registers %s  offset range 0x%X..0x%X" % (len(rows), res, bases, min(offs), max(offs)))
BASEOFF = {"r14": 8, "rsi": 0x1AA10}   # lea r14,[rbx+8] at 0072A496; lea rsi,[r14+0x1aa08] at 0072BA97 (rbx = this)
print("this_offset\tbase\tkind\tcount\tname\tsite")
for r in sorted(rows, key=lambda r: (r[0] + BASEOFF.get(r[1], 0) if r[0] >= 0 else 1 << 40, r[5])):
    print("%s\t%s\t%s\t%d\t%s\t%08X" % ("0x%X" % (r[0] + BASEOFF[r[1]]) if r[0] >= 0 and r[1] in BASEOFF else "?",
                                       r[1], r[2], r[3], r[4] if r[4] != "?" else "(built string)", r[5]))
