"""be6_two_singletons.py - BE-6: roles for two of the pump's unnamed singletons, from code (FABLE, Claude Opus 5.5,
2026-09-26). Static.

  P1 01F81248 (getter 001BDAB0) is the CharacterRenderObject pool: the acquire wrapper 0017F0D0 and the release wrapper
     0017F100 tail-jump to 001BD4A0 / 001BD840 with it as rcx (the pool mechanism: BB-4's control).
  P2 its per-frame update 001BDAC0 walks the pool tree (+0x28 sentinel, +0x30 first node), and for each pooled element
     either decrements the element's count (+0x18) or, at zero, calls the object's slot 3 (+0x18) and drops the element
     when it returns true; empty nodes are erased; then every object in the active vector gets +0x4B5 = 1.
  P3 01F81240 (getter 001BC000) is the character model asset cache: the asset loader 001BB2B0 searches its id map
     (+0xB0 header) and builds entries whose .ah path comes from the format "./GameData/%s/ArtData/chr/%s_%s.ah"
     (008F9158), also used by the name-keyed loader 001BB920.
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
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def dis(a, size): return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(a):off(a) + size], a)}
def rip_target(a):
    x = next(cs.disasm(d[off(a):off(a) + 16], a))
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", x.op_str)
    return x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16)
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
g1 = rip_target(0x1BDAB0)
w1 = dis(0x17F0D0, 0x2C); w2 = dis(0x17F100, 0x33)
check("P1 01F81248 is the render-object pool the acquire / release wrappers pass on", g1 == 0x1F81248
      and w1.get(0x17F0F1) == "jmp 0x1bd4a0" and w2.get(0x17F128) == "jmp 0x1bd840", "getter -> %08X" % g1)
u = dis(0x1BDAC0, 0x17E)
check("P2 its update expires pooled objects (count at +0x18, then slot 3) and marks active objects +0x4B5",
      u.get(0x1BDAEB) == "mov rdi, qword ptr [r14 + 0x30]" and u.get(0x1BDB20) == "mov eax, dword ptr [rbx + 0x18]"
      and u.get(0x1BDB2E) == "call qword ptr [rax + 0x18]" and u.get(0x1BDB67) == "dec eax"
      and u.get(0x1BDB9B) == "call 0x1bcfb0" and u.get(0x1BDC1B) == "mov byte ptr [rdx + 0x4b5], 1")
g2 = rip_target(0x1BC000)
fmt_off = off(0x8F9158); fmt = d[fmt_off:d.find(b"\0", fmt_off)].decode("latin-1")
refs = [a for a in (0x1BB7B7, 0x1BB9A4) if rip_target(a) == 0x8F9158]
h = dis(0x1BB2B0, 0x70)
check("P3 01F81240 is the character model asset cache the .ah loaders fill", g2 == 0x1F81240 and fmt.endswith("/ArtData/chr/%s_%s.ah")
      and refs == [0x1BB7B7, 0x1BB9A4] and h.get(0x1BB30C) == "lea rax, [rcx + 0xb0]", "getter -> %08X, format %r" % (g2, fmt))
print("FAILS", fails)
sys.exit(1 if fails else 0)
