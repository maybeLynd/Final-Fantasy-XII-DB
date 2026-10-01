"""tga_origin.py - FR-3: does the title-image TGA path honour the descriptor's origin bit? (FABLE, Claude Opus 5.5, 2026-09-26)

  T1 the loader 001D8D60 reads the 18-byte header into a stack buffer (`mov r8d, 0x12` / `lea rdx, [rsp + 0xa0]`
     before the stream read 0059F4A0), so the header occupies [rsp + 0xa0 .. 0xb1] and the descriptor byte 17 is
     [rsp + 0xb1].
  T2 every access to that buffer in the loader's whole body is one of: the lea that fills it, and word reads of
     +0x0C (width, rsp + 0xac) and +0x0E (height, rsp + 0xae). No access touches rsp + 0xb1 (descriptor), rsp + 0xa2
     (image type) or rsp + 0xa0 (id length).  Planted positive for the matcher: it must find the width and height
     reads, or T2 fails.
  T3 the pixels are read as width * height * 3 bytes straight after the header, and handed to the row copier
     001EE820 with its seventh argument - the flip byte at [rsp + 0x30] - set to the literal 0 (001D8E9E).
  T4 001EE820 is a bottom-up/top-down row copier: its flip byte (arg 7, [rsp + 0x48] after two pushes) selects a start
     at row (height - 1) and a negative row step (the `lea r10d, [rbx - 1]` / `imul` start and the `cmovne` step);
     it swaps bytes 0 and 2 and writes alpha 0xFF (BGR -> RGBA).
  T5 census: every direct `call 001EE820` in .text, with the flip literal each caller stores at [rsp + 0x30].
The shipped title image carries descriptor 0x20 (top-left), which is what a flip of 0 produces, so it displays
upright; a bottom-left TGA would be shown upside down.
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
names = [d[pe + 24 + opt + i * 40:pe + 24 + opt + i * 40 + 8].rstrip(b"\0") for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def body(a, b): return [(x.address, x.mnemonic, x.op_str) for x in cs.disasm(d[off(a):off(b)], a)]
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)

L = body(0x1D8D60, 0x1D8D60 + 0x1E2)            # functions.tsv body_bytes 0x1e2
S = {a: "%s %s" % (m, o) for a, m, o in L}
check("T1 18-byte header read into rsp+0xa0",
      S.get(0x1D8DE8) == "mov r8d, 0x12" and S.get(0x1D8DEE) == "lea rdx, [rsp + 0xa0]" and S.get(0x1D8DFB) == "call 0x59f4a0")
acc = []
for a, m, o in L:
    for mm in re.finditer(r"\[rsp \+ (0x[0-9a-f]+)\]", o):
        v = int(mm.group(1), 16)
        if 0xA0 <= v <= 0xB1: acc.append((a, m, o, v))
seen = sorted({(m, v) for a, m, o, v in acc})
check("T2 header accesses are the fill lea and the width/height word reads only",
      seen == [("lea", 0xA0), ("movsx", 0xAC), ("movsx", 0xAE), ("movzx", 0xAC), ("movzx", 0xAE)],
      " ".join("%08X:%s[%#x]" % (a, m, v) for a, m, o, v in acc))
check("T2 planted positive: width and height reads found", any(v == 0xAC for *_, v in acc) and any(v == 0xAE for *_, v in acc))
check("T2 no access to descriptor (0xb1), image type (0xa2) or id length (0xa0 as data)",
      not any(v in (0xB1, 0xA2) or (v == 0xA0 and m != "lea") for a, m, o, v in acc))
check("T3 pixels = w*h*3 after the header; copier called with flip literal 0",
      S.get(0x1D8E43) == "lea ebx, [rcx + rcx*2]" and S.get(0x1D8E9E) == "mov byte ptr [rsp + 0x30], 0"
      and S.get(0x1D8EBD) == "call 0x1ee820")
C = {a: "%s %s" % (m, o) for a, m, o in body(0x1EE820, 0x1EE820 + 0xB9)}
check("T4 copier: flip byte selects a last-row start and a negative step; BGR->RGBA",
      C.get(0x1EE828) == "movzx r14d, byte ptr [rsp + 0x48]" and C.get(0x1EE83D) == "lea r10d, [rbx - 1]"
      and C.get(0x1EE8B0) == "sub rax, rbp" and C.get(0x1EE8B6) == "cmovne r11, rax"
      and C.get(0x1EE896) == "mov byte ptr [rax - 4], cl" and C.get(0x1EE89C) == "mov byte ptr [rax - 2], r8b"
      and C.get(0x1EE8A0) == "mov byte ptr [rax - 1], 0xff")
# T5: raw E8 census over .text
ti = names.index(b".text"); vs, va, rs, ro = secs[ti]
tx = d[ro:ro + rs]; sites = []
for i in range(len(tx) - 5):
    if tx[i] == 0xE8 and BASE + va + i + 5 + struct.unpack_from("<i", tx, i + 1)[0] == 0x1EE820:
        sites.append(BASE + va + i)
res = []
for s in sites:
    pre = [x for x in cs.disasm(d[off(s - 0x40):off(s) + 5], s - 0x40)]
    ok = any(x.address == s and x.mnemonic == "call" for x in pre)
    flip = [x.op_str for x in pre if x.mnemonic == "mov" and x.op_str.startswith("byte ptr [rsp + 0x30], ")]
    res.append((s, ok, flip[-1].split(", ")[1] if flip else "?"))
check("T5 census of direct calls to 001EE820", 0x1D8EBD in [s for s, ok, f in res if ok],
      " ".join("%08X%s:flip=%s" % (s, "" if ok else "(not a boundary)", f) for s, ok, f in res))
print("FAILS", fails)
sys.exit(1 if fails else 0)
