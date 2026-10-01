"""metadata.py - OV-35: the indexed source's selector and metadata - creation, lifetime, permitted indices, mode meanings
(FABLE, Claude Opus 5.5, 2026-09-29). STATIC.

  S  THE SELECTOR 0032F240(g) returns the manager's recorded resource-set index (dword 022C6D28 + 4g) when its flag byte
     (022C6D18 + g) is set, else -1 - the index ActorResource_BeginManagerResourceSetLoad records for the manager
  K  THE MODE MAPPING 0032F170(g, index, &ns, &id): g <= 0 (and any value not 1..4) -> namespace 5, id = index*3; g = 1..3 ->
     namespace 8, id = index*4; g = 4 -> namespace 1, id = index + 0x6B. These are the package namespaces of the PKFL page
     ({ebp, mot, fpk} triples in namespace 5; {ebp, mot, snd, vpc} quadruples in namespace 8)
  M  THE METADATA PROVIDERS 0032F260 (offset) / 0032F290 (length) accept g <= 3 only, read the pointer at 022C6E70 + 8g, return
     -1 unless its first byte is non-zero, and read {offset, size} pair i at +8 + 8i / +0xC + 8i
  So: the metadata is the manager's .mot PKFL directory (magic byte non-zero = loaded; 16 {offset, size} slots, 0x88 bytes),
  requested into a boot-allocated table by the manager resource-set load (the voice-pack page) and rewritten on each such
  load; permitted indices are g 0..3 (group 4 has no metadata: both providers return -1) and i 0..15 (every shipped .mot has
  16 slots, the PKFL page's audited corpus)
"""
import hashlib, os, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "exe", "FFXII_TZA.exe")
d = open(EXE, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, msg):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, msg))
def dis(a, b): return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(a):off(b)], a)}
at = lambda c, w: all(c.get(a) == s for a, s in w.items())
s = dis(0x32F240, 0x32F260)
check("S", at(s, {0x32F243: "lea rcx, [rip - 0x20f24a]", 0x32F24A: "cmp byte ptr [rax + rcx + 0x21a6d18], 0",
                  0x32F254: "mov eax, dword ptr [rcx + rax*4 + 0x21a6d28]", 0x32F25C: "or eax, 0xffffffff"})
      and 0x32F24A - 0x20F24A == B and B + 0x21A6D28 == 0x22C6D28,
      "selector = the recorded resource-set index at 022C6D28 + 4g, or -1")
k = dis(0x32F170, 0x32F1AC)
check("K", at(k, {0x32F17E: "lea eax, [rdx + 0x6b]", 0x32F181: "mov dword ptr [r8], 1", 0x32F18C: "lea eax, [rdx*4]",
                  0x32F193: "mov dword ptr [r8], 8", 0x32F19E: "lea eax, [rdx + rdx*2]", 0x32F1A1: "mov dword ptr [r8], 5",
                  0x32F174: "cmp ecx, 3", 0x32F179: "cmp ecx, 4"}),
      "mode: g 1..3 -> ns 8 / index*4; g 4 -> ns 1 / index+0x6B; otherwise ns 5 / index*3")
m = {**dis(0x32F260, 0x32F284), **dis(0x32F290, 0x32F2B4)}
check("M", at(m, {0x32F260: "cmp ecx, 3", 0x32F263: "jg 0x32f280", 0x32F273: "cmp byte ptr [rcx], 0", 0x32F27B: "mov eax, dword ptr [rcx + rax*8 + 8]",
                  0x32F290: "cmp ecx, 3", 0x32F293: "jg 0x32f2b0", 0x32F2A3: "cmp byte ptr [rcx], 0", 0x32F2AB: "mov eax, dword ptr [rcx + rax*8 + 0xc]"})
      and 0x32F26F + 0x1F97C01 == 0x22C6E70,
      "providers: g <= 3; loaded (first byte != 0); {offset, size} pair i at +8 / +0xC + 8i of 022C6E70[g]")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
