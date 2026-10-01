"""dm2_code27.py - DM-2: what keymap control code 27 is (FABLE, Claude Opus 5.5, 2026-09-27). Static.

  D1 the pad band is 17 codes, 11..27: the raw-state getter 0079D670 reads controller +0x43C + (code - 11) and the
     node binder 00799F40 points a button node at that same byte, both for code - 11 <= 0x10; the any-pad test 0079E650
     tests +0x30 + (code - 11) for code - 11 < 0x11. So code 27 is pad slot 16, the 17th.
  D2 the controller base constructor 00792940 zeroes the 17 raw bytes +0x43C..+0x44C (qword, qword, byte).
  D3 the XInput poll 007A2140 and the Steam poll 007A1CD0 store exactly the 16 bytes +0x43C..+0x44B, never +0x44C.
  D4 the DirectInput poll 007A1A50 reads a 0x110-byte DIJOYSTATE2 (GetDeviceState, vtable +0x48) to rsp+0x20 and copies
     17 bytes, rgbButtons[0..16] (rsp+0x50) >> 7, into +0x43C.. - so slot 16 is DirectInput button 16.
  D5 over every function in 00780000-007C0000, the only store to displacement 0x44C is the constructor's, and the only
     loop that stores through a pointer into the raw array is the DirectInput poll's (the known positive).
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
def body(a): return [(x.address, ("%s %s" % (x.mnemonic, x.op_str)).strip()) for x in cs.disasm(d[off(a):off(a) + SIZES[a]], a)]
def dmap(a): return dict(body(a))
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

g, b, t = dmap(0x79D670), dmap(0x799F40), dmap(0x79E650)
check("D1 the pad band is codes 11..27: three readers bound code - 11 to 17 slots",
      g.get(0x79D670) == "lea eax, [rdx - 0xb]" and g.get(0x79D673) == "cmp eax, 0x10" and g.get(0x79D676) == "ja 0x79d687"
      and g.get(0x79D67E) == "movzx eax, byte ptr [rdx + rcx + 0x43c]"
      and b.get(0x799F40) == "lea eax, [r8 - 0xb]" and b.get(0x799F4D) == "cmp eax, 0x10" and b.get(0x799F75) == "lea rdx, [r11 + 0x43c]"
      and b.get(0x799F83) == "mov qword ptr [r9 + 0x38], rdx"
      and t.get(0x79E66D) == "lea ecx, [rdx - 0xb]" and t.get(0x79E670) == "cmp ecx, 0x11" and t.get(0x79E675) == "cmp byte ptr [rcx + r9 + 0x30], 0")

c = dmap(0x792940)
check("D2 the base constructor zeroes +0x43C..+0x44C",
      c.get(0x792A14) == "mov qword ptr [rbx + 0x43c], rdx" and c.get(0x792A1B) == "mov qword ptr [rbx + 0x444], rdx"
      and c.get(0x792A22) == "mov byte ptr [rbx + 0x44c], dl")

def raw_stores(a):
    out = set()
    for addr, s in body(a):
        m = re.match(r"mov (byte|word) ptr \[rbx \+ 0x(4[3-4][0-9a-f])\], ", s)
        if m:
            o = int(m.group(2), 16)
            if 0x43C <= o <= 0x44C: out |= {o} if m.group(1) == "byte" else {o, o + 1}
    return out
xi, st = raw_stores(0x7A2140), raw_stores(0x7A1CD0)
want = set(range(0x43C, 0x44C))
check("D3 the XInput and Steam polls store exactly +0x43C..+0x44B, never +0x44C",
      xi == want and st == want, "xinput %d, steam %d" % (len(xi), len(st)))

p = dmap(0x7A1A50)
check("D4 the DirectInput poll copies rgbButtons[0..16] >> 7 into +0x43C..+0x44C",
      p.get(0x7A1B3E) == "lea r8, [rsp + 0x20]" and p.get(0x7A1B43) == "mov edx, 0x110" and p.get(0x7A1B4B) == "call qword ptr [rax + 0x48]"
      and p.get(0x7A1B5A) == "lea r8, [rsp + 0x50]" and p.get(0x7A1B65) == "lea rcx, [rbx + 0x43c]"
      and p.get(0x7A1B90) == "movzx eax, byte ptr [r8 + rcx - 0x43c]" and p.get(0x7A1B9D) == "shr al, 7"
      and p.get(0x7A1BA2) == "mov byte ptr [rcx - 1], al" and p.get(0x7A1BA5) == "cmp edx, 0x11" and p.get(0x7A1BA8) == "jb 0x7a1b90")

s44c, loops = [], []
for f in sorted(a for a in SIZES if 0x780000 <= a < 0x7C0000):
    if off(f) is None or SIZES[f] <= 0: continue
    ins = body(f)
    for addr, s in ins:
        if re.match(r"mov (byte|word|dword|qword) ptr \[\w+ \+ 0x44c\], ", s): s44c.append((f, addr))
    if any(s.startswith("lea ") and s.endswith("+ 0x43c]") for _, s in ins) and any(re.match(r"mov byte ptr \[r\w+ - 1\], ", s) for _, s in ins):
        loops.append(f)
check("D5 the only store at +0x44C is the constructor's; the only pointer loop into the raw array is the DirectInput poll's",
      [f for f, _ in s44c] == [0x792940] and loops == [0x7A1A50], "stores %s loops %s" % (["%08X" % a for _, a in s44c], ["%08X" % f for f in loops]))
print("FAILS", fails)
sys.exit(1 if fails else 0)
