"""SWE2-AUDIT-SEM RC-25 attack, part 2 (own code): the callees that receive a party-block-derived pointer in rcx
(from rc25_blockcopy.out (b)) - does any of them store over byte +4/+5 of that pointer, at any width?
Each callee body is taken from .pdata (chain roots followed: UNWIND_INFO chained flag), decoded linearly; rcx is
tracked into the registers it is copied to (mov r64, rcx) until overwritten; a store [alias + d] of width w is
reported when d <= 5 and d + w > 4.
Positive control: 0023AC80 (BattleStats_InitializeDefinitionRecord) must be reported (0023AD8E word [rdi + 4]) when
run through the same code with its page argument in rcx.
"""
import struct, re
import img

def pdata():
    for n, rva, vsz, rp, rs in img.secs:
        if n == ".pdata":
            out = []
            for k in range(0, vsz, 12):
                b, e, u = struct.unpack_from("<III", img.raw, rp + k)
                if b == 0:
                    break
                out.append((b + img.BASE, e + img.BASE, u))
            return out
PD = pdata()

def fragments_of(root):
    """all .pdata fragments whose chain root is `root` (chained unwind info points back to the root's entry)"""
    frs = []
    for b, e, u in PD:
        if b == root:
            frs.append((b, e))
            continue
        uo = img.off(u + img.BASE)
        if uo is None:
            continue
        flags = img.raw[uo] >> 3
        if flags & 4:  # UNW_FLAG_CHAININFO
            cnt = img.raw[uo + 2]
            co = uo + 4 + ((cnt + 1) & ~1) * 2
            cb = struct.unpack_from("<I", img.raw, co)[0] + img.BASE
            if cb == root:
                frs.append((b, e))
    return frs

R64 = {}
for r in ("ax", "bx", "cx", "dx", "si", "di", "bp"):
    R64["r" + r] = "r" + r
for n in range(8, 16):
    R64["r%d" % n] = "r%d" % n
W = {"byte": 1, "word": 2, "dword": 4, "qword": 8, "xmmword": 16, "ymmword": 32}
MEM = re.compile(r"(byte|word|dword|qword|xmmword|ymmword) ptr \[(\w+)(?: \+ (0x[0-9a-f]+|\d+))?\]$")

def scan(fn):
    hits = []
    frs = fragments_of(fn)
    if not frs:  # leaf without .pdata: linear decode to the first ret
        ins = img.dis(fn, 400)
        frs = [(fn, ins[-1].address + ins[-1].size)]
    for b, e in frs:
        alias = {"rcx"} if b == fn else set()
        for x in img.md.disasm(img.rd(b, e - b), b):
            ops = [o.strip() for o in x.op_str.split(",")]
            if x.mnemonic == "call":
                alias -= {"rcx", "rdx", "r8", "r9", "r10", "r11", "rax"}
                continue
            if ops and ops[0] in R64:
                if x.mnemonic == "mov" and len(ops) == 2 and ops[1] in alias:
                    alias.add(ops[0])
                elif x.mnemonic not in ("cmp", "test", "push"):
                    alias.discard(ops[0])
                continue
            m = MEM.match(ops[0]) if ops else None
            if m and x.mnemonic not in ("cmp", "test") and m.group(2) in alias:
                d = int(m.group(3), 0) if m.group(3) else 0
                w = W[m.group(1)]
                if d <= 5 and d + w > 4:
                    hits.append("%08X %s %s" % (x.address, x.mnemonic, x.op_str))
    return hits

CALLEES = [0x30E990, 0x2EF4A0, 0x861EC0, 0x326030, 0x327DE0, 0x30D9A0, 0x35C620, 0x317930, 0x318B40, 0x30FED0,
           0x31B860, 0x31C000, 0x316DF0, 0x328990, 0x243260, 0x5683F0]
for f in CALLEES:
    h = scan(f)
    print("%08X fragments %d  stores covering rcx+4/+5: %s" % (f, len(fragments_of(f)), h if h else "none"))
pc = scan(0x0023AC80)
print("CONTROL 0023AC80:", pc)
print("PASS control" if any("0023AD8E" in s for s in pc) else "FAIL control")
