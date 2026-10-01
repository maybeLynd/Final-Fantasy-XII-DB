"""SWE2-AUDIT-SEM (own code): the active image 02164280 (002EF640's return) holds a 0x6000-byte mirror at +0x2200
(02166480) that 002EF4A0 copies over the live state 021B290C (+0x4E68C), which contains region A (state +0x4748..
+0x4F0F). This lists (1) the callers of 00235AF0 (the only caller of 002EF4A0), (2) for each of the direct sites into
002EF640, the next 30 instructions' uses of rax-derived pointers with their displacement (so a store into the mirror
range +0x2200..+0x8200 is visible), and (3) the reverse copy (live -> mirror), searched as any caller of a copy loop
whose source is 021B290C and destination 02166480 (rip-relative lea pairs).
"""
import struct, re
import img
t0, t1, rp = img.text_range()
text = img.raw[rp:rp + (t1 - t0)]
va0 = img.BASE + t0

def direct(target):
    out = []
    for i in range(len(text) - 5):
        if text[i] in (0xE8, 0xE9) and va0 + i + 5 + struct.unpack_from("<i", text, i + 1)[0] == target:
            out.append(va0 + i)
    return out

def owner(a):
    for n, rva, vsz, rpp, rs in img.secs:
        if n == ".pdata":
            for k in range(0, vsz, 12):
                b, e, u = struct.unpack_from("<III", img.raw, rpp + k)
                if b + img.BASE <= a < e + img.BASE:
                    return b + img.BASE
    return 0

print("callers of 00235AF0:", ["%08X in %08X" % (a, owner(a)) for a in direct(0x00235AF0)])
for a in direct(0x00235AF0):
    for x in img.dis(a - 0x20, 16, stop_ret=False):
        if a - 0x20 <= x.address <= a:
            print("     %08X %s %s" % (x.address, x.mnemonic, x.op_str))
print()
print("uses of 002EF640's return (rax) after each direct site, displacements shown:")
for a in direct(0x002EF640):
    seq = list(img.md.disasm(img.rd(a + 5, 200), a + 5))[:14]
    taint = {"rax"}
    uses = []
    for x in seq:
        ops = [o.strip() for o in x.op_str.split(",")]
        if x.mnemonic in ("ret", "jmp", "call"):
            break
        mem = re.findall(r"\[(\w+)(?: \+ (0x[0-9a-f]+))?\]", x.op_str)
        for base, d in mem:
            if base in taint:
                uses.append("%08X %s %s" % (x.address, x.mnemonic, x.op_str))
        if ops and ops[0] in ("rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15"):
            src = " ".join(ops[1:])
            if x.mnemonic in ("mov", "lea") and any(re.search(r"\b%s\b" % t, src) for t in taint):
                taint.add(ops[0])
            elif x.mnemonic == "add" and ops[0] in taint:
                uses.append("%08X %s %s" % (x.address, x.mnemonic, x.op_str))
            elif x.mnemonic not in ("cmp", "test"):
                taint.discard(ops[0])
    print("  site %08X in %08X: %s" % (a, owner(a), " | ".join(uses) if uses else "-"))
