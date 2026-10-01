"""uq46_packet_ends.py - UQ-46: the six objects the 2026-09-17 narrowing left bracketed or unbounded are sized by their
own packet structure (FABLE, Claude Opus 5.5, 2026-09-27). Static.

Each object is a startup-built PS2 packet template. Its length is stated inside it, in one of two ways:
  - a DMA cnt tag written by 008631D0(tag, qwc) - word qwc, byte +3 = 0x10 - so the packet ends at
    tag + 0x10 + qwc * 16;
  - or, where the builder writes no tag, the UNPACK V4_32 header at +0x1C (0x6C, count in bits 16-23) covering
    count * 16 bytes from +0x20, then one closing qword.

  P1 the six ends: 02AE06B0 0x1A0, 02AE1DA0 0x150, 02AE4F20 0xC70, 02AE9EE0 0x150, 02AEC660 0x200, 02AED330 0x130.
     02AEC660's builder 004E7980 writes the header and tail-jumps to 004E7A90 with rcx = object + 0x10, whose cnt tag
     (qwc 0x1E) and stores run to +0x1FF - the extent census recorded 0x10 because it did not follow that jump.
  P2 positive control: the same reading of 02ADFD00 (builder 004C0C70), one of the 42 exact objects, gives 0x190 -
     its measured extent and gap.
  P3 for 02AE06B0, 02AE1DA0, 02AE4F20 and 02AE9EE0 the functions that reference their tails (0044D4A0, 004595C0,
     00453150, 003B6020) reference nothing inside the object and begin at or past its packet end - for 02AE9EE0
     exactly at it: the tail is the next variable. References are rip-relative or image-base-relative.
  P4 sensitivity to the addressing form: 003B6020 reaches 02AE9EE0 + 0x150 (a 0xA0-byte template it copies) only
     through rbx = the image base; a rip-only reading of it starts at +0x1F0 and would have left +0x150..+0x1EF
     looking unreferenced.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
SIZES = {}
for line in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    q = line.rstrip("\n").split("\t")
    try: SIZES[int(q[0], 16)] = int(q[2])
    except (ValueError, IndexError): pass
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def body(a): return [(x.address, x.mnemonic, x.op_str) for x in cs.disasm(d[off(a):off(a) + SIZES[a]], a)]
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

cnt = dict((a, "%s %s" % (m, o)) for a, m, o in body(0x8631D0))
assert cnt.get(0x8631D0) == "mov word ptr [rcx], dx" and cnt.get(0x8631D3) == "mov byte ptr [rcx + 3], 0x10"

def cnt_end(builder, rcx_off=0):
    """end of the packet from 008631D0 calls whose rcx is the object (or object + k) and edx an immediate"""
    ends = []; k = rcx_off; edx = None; objregs = {"rcx": rcx_off}
    for a, m, o in body(builder):
        mm = re.fullmatch(r"(r\w+), rcx", o)
        if m == "mov" and mm and "rcx" in objregs: objregs[mm.group(1)] = objregs["rcx"]
        mm = re.fullmatch(r"rcx, \[(r\w+) \+ (0x[0-9a-f]+)\]", o)
        if m == "lea" and mm and mm.group(1) in objregs: objregs["rcx"] = objregs[mm.group(1)] + int(mm.group(2), 16)
        mm = re.fullmatch(r"edx, (0x[0-9a-f]+|\d+)", o)
        if m == "mov" and mm: edx = int(mm.group(1), 0)
        if m in ("call", "jmp") and o == "0x8631d0" and objregs.get("rcx") is not None:
            ends.append(objregs["rcx"] + 0x10 + edx * 16)
    return max(ends) if ends else None

def unpack_end(builder):
    """end from the UNPACK V4_32 header stored at +0x1C, plus the closing qword the builder stores right after"""
    st = {}
    for a, m, o in body(builder):
        mm = re.fullmatch(r"(?:dword|qword) ptr \[rcx \+ (0x[0-9a-f]+)\], (0x[0-9a-f]+|\w+)", o)
        if m == "mov" and mm: st[int(mm.group(1), 16)] = mm.group(2)
    h = int(st.get(0x1C, "0"), 16) if st.get(0x1C, "").startswith("0x") else 0
    if (h >> 24) != 0x6C: return None, st
    data_end = 0x20 + ((h >> 16) & 0xFF) * 16
    closing = [o for o in st if data_end <= o < data_end + 0x10]
    return (data_end + 0x10 if closing else data_end), st

e06b0, s06b0 = unpack_end(0x4A1C10); e1da0, s1da0 = unpack_end(0x482410)
e4f20 = cnt_end(0x4B8F20); e9ee0 = cnt_end(0x4DB060); ed330 = cnt_end(0x4ED960)
jmp = [(a, o) for a, m, o in body(0x4E7980) if m == "jmp"]
ec660 = cnt_end(0x4E7A90, 0x10) if jmp == [(0x4E79AF, "0x4e7a90")] else None
last7a90 = max(int(x, 16) for _, m, o in body(0x4E7A90) for x in re.findall(r"\[rbx \+ (0x[0-9a-f]+)\]", o))
got = {"02AE06B0": e06b0, "02AE1DA0": e1da0, "02AE4F20": e4f20, "02AE9EE0": e9ee0, "02AEC660": ec660, "02AED330": ed330}
want = {"02AE06B0": 0x1A0, "02AE1DA0": 0x150, "02AE4F20": 0xC70, "02AE9EE0": 0x150, "02AEC660": 0x200, "02AED330": 0x130}
check("P1 the six packet ends, each read from the object's own DMA tag or UNPACK header",
      got == want and 0x10 + last7a90 + 8 == 0x200 and s1da0.get(0x140) == "0x15000000" and s1da0.get(0x144) == "0x13000000",
      str({k: (hex(v) if v else v) for k, v in got.items()}))
check("P2 positive control: 02ADFD00 (a measured-exact object) reads 0x190", cnt_end(0x4C0C70) == 0x190)

RIP = re.compile(r"\[rip ([+-]) (0x[0-9a-f]+)\]")
def rip_offsets(f, base, lo, hi):
    out = []
    for a, m, o in body(f):
        mm = RIP.search(o)
        if mm:
            t = a + next(cs.disasm(d[off(a):off(a) + 16], a)).size + (int(mm.group(2), 16) if mm.group(1) == "+" else -int(mm.group(2), 16))
            if base + lo <= t < base + hi: out.append(t - base)
    return out
def refs(f, base, lo, hi):
    """rip-relative targets plus image-base-relative ones: a [reg + disp] operand whose disp + image base lands in
    the range (the image-base register form, e.g. lea rbx, [rip - x] = 0x120000 then [rbx + disp])"""
    out = rip_offsets(f, base, lo, hi)
    for a, m, o in body(f):
        for mm in re.finditer(r"\[r\w+(?: \+ r\w+(?:\*\d)?)? \+ (0x[0-9a-f]{7,})\]", o):
            t = BASE + int(mm.group(1), 16)
            if base + lo <= t < base + hi: out.append(t - base)
    return out
p3 = {}
for base, user, end, gap in ((0x2AE06B0, 0x44D4A0, 0x1A0, 0x2F0), (0x2AE1DA0, 0x4595C0, 0x150, 0x2E0), (0x2AE4F20, 0x453150, 0xC70, 0x1A30),
                             (0x2AE9EE0, 0x3B6020, 0x150, 0x390)):
    inside = refs(user, base, 0, end); tail = refs(user, base, end, gap)
    p3["%08X" % base] = (not inside) and bool(tail) and min(tail) >= end and (min(tail) == end or base != 0x2AE9EE0)
check("P3 the tail users touch nothing inside the object and start at or past its end (rip and image-base-relative references)",
      all(p3.values()), str(p3))

rb = dict((a, "%s %s" % (m, o)) for a, m, o in body(0x3B6020))
check("P4 sensitivity: 02AE9EE0's next variable is found only through image-base-relative addressing - 003B6020 sets rbx to the image base and copies the 0xA0-byte template at +0x150; its rip references start at +0x1F0",
      rb.get(0x3B60A6) == "lea rbx, [rip - 0x2960ad]" and 0x3B60AD - 0x2960AD == BASE
      and rb.get(0x3B6181) == "movups xmm0, xmmword ptr [rbx + 0x29ca030]" and BASE + 0x29CA030 == 0x2AE9EE0 + 0x150
      and rip_offsets(0x3B6020, 0x2AE9EE0, 0x150, 0x200) == [0x1F0])
print("FAILS", fails)
sys.exit(1 if fails else 0)
