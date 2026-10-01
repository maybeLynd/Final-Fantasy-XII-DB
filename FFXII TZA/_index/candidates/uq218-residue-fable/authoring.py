"""authoring.py - UQ-218 residue: where a presentation entry's +0x31A (group) and +0x31C (child slot) come from (FABLE, Claude
Opus 5.5, 2026-09-29; supply-side for SWE2-DATA's page, FRONTIER-REQ-FABLE-UQ218-SEMANTIC-RESIDUE). STATIC, certified image.

  D  the entry initialiser 0041D220 copies descriptor word +0x20 -> entry +0x31C (0041D242 / 0041D249) and descriptor word
     +0x24 -> entry +0x31A (0041D2A6 / 0041D2AA)
  A  both admission sites build that descriptor at rsp+0x30 and call 0051BA80 (the only caller of 0041D220, at 0051BAD7):
     descriptor +0x20 = the render event (rsp+0x50), descriptor +0x24 = movsx byte [render + 0x413] (rsp+0x54); sites
     00424550 (call 004247AD) and 00424D80 (call 00425244)
  V  render +0x413 is the actor's STANDARD-MOTION VARIATION: 002E8220 (verb 01AA stdmotionvariation) stores v << 3 into
     actor-record +0x14F bits 3-7 and mirrors +0x14F >> 3 to render +0x413 (002E827D)
  So: +0x31C & 0xFFF is the selected render event = the motion slot; +0x31A is the variation = which bank of 80 slots
  (004090D0: slot[80 x group + cmdSlot]); both are authored through scripts (stdmotionvariation) and the unit definition
  refresh, not stored in the motion container.
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
def dis(a, b): return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(a):off(b)], a)}
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
at = lambda c, w: all(c.get(a) == s for a, s in w.items())
init = dis(0x41D220, 0x41D2B2)
check("D", at(init, {0x41D242: "movzx eax, word ptr [rdx + 0x20]", 0x41D249: "mov word ptr [rcx + 0x31c], ax",
                     0x41D2A6: "movzx eax, word ptr [rbx + 0x24]", 0x41D2AA: "mov word ptr [rsi + 0x31a], ax"}),
      "0041D220: descriptor +0x20 -> +0x31C, +0x24 -> +0x31A")
# the only rel32 caller of 0041D220, and the two callers of 0051BA80
t = [s for s in SECS]; text = None
calls = {}
for tgt in (0x41D220, 0x51BA80):
    hits = []
    for vs, va, rs, ro in SECS:
        blob = d[ro:ro + rs]
        for i in range(len(blob) - 5):
            if blob[i] == 0xE8 and B + va + i + 5 + struct.unpack_from("<i", blob, i + 1)[0] == tgt: hits.append(B + va + i)
    calls[tgt] = hits
s1 = dis(0x424700, 0x4247B2); s2 = dis(0x425180, 0x425250)
ok_a = (calls[0x41D220] == [0x51BAD7] and calls[0x51BA80] == [0x4247AD, 0x425244]
        and at(s1, {0x424730: "movsx eax, byte ptr [rdi + 0x413]", 0x424742: "mov dword ptr [rsp + 0x54], eax",
                    0x42474B: "mov dword ptr [rsp + 0x50], r14d", 0x424793: "lea rcx, [rsp + 0x30]"})
        and at(s2, {0x4251C7: "movsx eax, byte ptr [rbx + 0x413]", 0x4251D9: "mov dword ptr [rsp + 0x54], eax",
                    0x4251E2: "mov dword ptr [rsp + 0x50], esi", 0x42522A: "lea rcx, [rsp + 0x30]"}))
check("A", ok_a, "callers: 0041D220 <- %s; 0051BA80 <- %s; both blocks put the event at +0x20 and render +0x413 at +0x24"
      % (["%08X" % a for a in calls[0x41D220]], ["%08X" % a for a in calls[0x51BA80]]))
v = dis(0x2E8220, 0x2E8284)
check("V", at(v, {0x2E822C: "and byte ptr [rax + 0x14f], 7", 0x2E8233: "shl dl, 3", 0x2E8236: "or byte ptr [rax + 0x14f], dl",
                  0x2E827A: "shr al, 3", 0x2E827D: "mov byte ptr [rdx + 0x413], al"}),
      "002E8220 (stdmotionvariation): v << 3 into actor +0x14F, mirrored >> 3 to render +0x413")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
