"""selector_criteria.py - UQ-218: what @FMC 0x0B's selector kinds 1, 2, 0x20, 0x21, 0x24 and 0x25 choose by (FABLE, Claude
Opus 5.5, 2026-09-29). STATIC, certified image; follows selector_kinds.py (S1-S4, C).

  N  0x0B (00417110) calls the selector and skips entirely when it returns -1 (cmp edx, -1 / je at 00417262); otherwise the
     low half is the list index (movzx) and the high half the track offset (sar 0x10)
  Q  the battle unit's view request 0031ADB0: query bit 0x10 sets view flag bit 1 (value 2) to 0030C010(unit) & 1, the
     combo-may-continue predicate; query bit 0x20 sets view flag bit 2 (value 4) when the unit's first target entry
     (+0x788) has knockback (bit 8) clear and its target-entry code is 2..5 or 7 (result kinds 1-4 = band A/B evade, plain
     or with parry, and 7 = absorbed by a defensive layer)
  K1 kind 1 (00422420): counter +0x40E == 0 -> draw r = bounded(5) (003A6E60), keep it at +0x411, set the counter to
     frameLimit, return r (0..4); later, exactly when the counter == 11 x frameLimit and view query 0x20's flag 4 is set, add 5
     to +0x411 and return it (5..9); otherwise count up to 100 and return -1 (no change)
  K2 kind 2 (00422500): view query 0x30; while +0x410 is 0xFF (undecided): flag 2 -> 0, else flag 4 -> 1, else 2; once
     decided, +0x410 is returned unchanged
  Y  the yaw family (query 4 = the target's world position; yaw to it via the steering contract's yaw-to-point, x 57.2958):
     0x20 (00422630): 0 within [-90, 90] degrees, else 1; 0x21 (004226C0): 0 within [-60, 60], else 1 above and 2 below,
     then + 3 on a bounded(2) coin; 0x24 (00422870): 0 in [-45, 45], 1 in (45, 135], 2 in [-135, -45), else 3 - kept in
     record +0x2AF - then + 4 on a coin; 0x25 (00422940): the yaw to the actor named by record +0x18 (0 if it does not
     resolve): 0 in (-90, 0], 1 at or below -90, 3 in (0, 90], 2 above 90
  Not claimed: which side of zero is the character's left; what the tracks chosen look like; kinds 0 / 0xA / 0xB (the
  locomotion classifier 004256E0, read only in outline).
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
def f32(a): return struct.unpack_from("<f", d, off(a))[0]
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
at = lambda c, w: all(c.get(a) == s for a, s in w.items())

nb = dis(0x4171EE, 0x417296)
check("N", at(nb, {0x4171FA: "call qword ptr [rdx]", 0x417262: "cmp edx, -1", 0x417265: "je 0x4173c0", 0x41727D: "sar r15d, 0x10",
                   0x417281: "movzx r14d, dx", 0x41728D: "cmp r14d, ecx", 0x417290: "jge 0x4173b6"}),
      "0x0B: -1 skips (00417262); index = low half, offset = high half; index must be below the list length")
q = dis(0x31B0C4, 0x31B11A)
check("Q", at(q, {0x31B0C4: "test r14b, 0x10", 0x31B0CD: "call 0x30c010", 0x31B0D6: "and eax, 1", 0x31B0D9: "add eax, eax",
                  0x31B0DB: "or dword ptr [rdi + 0x3c], eax", 0x31B0E1: "test r14b, 0x20", 0x31B0E7: "test dword ptr [rbx + 0x788], 0x100",
                  0x31B0FA: "lea eax, [rcx - 2]", 0x31B0FD: "cmp eax, 3", 0x31B102: "cmp ecx, 7", 0x31B107: "mov eax, 4",
                  0x31B110: "and dword ptr [rdi + 0x3c], 0xfffffffb"}),
      "view query 0x10 -> flag 2 = combo predicate & 1; query 0x20 -> flag 4 = entry0 code in 2..5 or 7 with knockback clear")
k1 = dis(0x422420, 0x4224FF)
check("K1", at(k1, {0x42243C: "movzx eax, byte ptr [rbx + 0x40e]", 0x422447: "mov ecx, 5", 0x42244C: "call 0x3a6e60",
                    0x422451: "mov byte ptr [rbx + 0x411], al", 0x42247A: "imul ecx, dword ptr [rip + 0x19dbc33], 0xb",
                    0x42248D: "mov edx, 0x20", 0x42249A: "test byte ptr [rsp + 0x5c], 4", 0x4224A1: "add byte ptr [rbx + 0x411], 5",
                    0x4224CE: "mov ecx, 0x64", 0x4224E9: "or eax, 0xffffffff"}) and 0x42247A + 7 + 0x19dbc33 == 0x1DFE0B4,
      "kind 1: draw 0..4, keep it; at 11 x frameLimit (01DFE0B4) with view flag 4 -> +5; else -1, counter capped at 100")
k2 = dis(0x422500, 0x42259D)
check("K2", at(k2, {0x422524: "mov edx, 0x30", 0x42252E: "cmp byte ptr [rbx + 0x410], 0xff", 0x42253B: "test al, 2",
                    0x42254C: "mov byte ptr [rbx + 0x410], 0", 0x42256F: "test al, 4", 0x422573: "mov byte ptr [rbx + 0x410], 1",
                    0x42257C: "mov byte ptr [rbx + 0x410], 2", 0x422583: "movsx eax, byte ptr [rbx + 0x410]"}),
      "kind 2: sticky; combo-continues -> 0, else evaded/absorbed -> 1, else 2")
DEG = 0xD117E0
consts = {a: f32(a) for a in (0xD117E0, 0xD117E4, 0x9166FC, 0xD12440, 0x8F6D54, 0xD1243C, 0x902EF0, 0xD12438, 0xD12444)}
y20 = dis(0x422630, 0x4226BA); y21 = dis(0x4226C0, 0x422757); y24 = dis(0x422870, 0x42293F); y25 = dis(0x422940, 0x422A0B)
yok = (at(y20, {0x422654: "mov edx, 4", 0x42266A: "call 0x424370", 0x42268D: "xor eax, eax", 0x4226A2: "mov eax, 1"})
       and at(y21, {0x42272C: "setbe bl", 0x42272F: "inc ebx", 0x422731: "mov ecx, 2", 0x422736: "call 0x3a6e60", 0x42273D: "lea eax, [rbx + 3]"})
       and at(y24, {0x4228ED: "mov byte ptr [rbx + 0x2af], 1", 0x422904: "mov byte ptr [rbx + 0x2af], 2", 0x42290D: "mov byte ptr [rbx + 0x2af], 3",
                    0x422919: "call 0x3a6e60", 0x422929: "add eax, 4"})
       and at(y25, {0x422951: "mov ebx, dword ptr [rdi + 0x18]", 0x4229BA: "call 0x424370", 0x4229D8: "setbe al", 0x4229F0: "add eax, 2", 0x4229FE: "xor eax, eax"}))
cok = (abs(consts[0xD117E0] - 57.29578) < 1e-3 and consts[0xD117E4] == -90 and consts[0x9166FC] == 90 and consts[0xD12440] == -60
       and consts[0x8F6D54] == 60 and consts[0xD1243C] == -45 and consts[0x902EF0] == 45 and consts[0xD12438] == 135 and consts[0xD12444] == -135)
def k20(dg): return 0 if -90 <= dg <= 90 else 1
def k21(dg, coin): b = 0 if -60 <= dg <= 60 else (2 if dg <= 0 else 1); return b + 3 if coin else b
def k24(dg, coin):
    b = 0 if -45 <= dg <= 45 else 1 if 45 < dg <= 135 else 2 if -135 <= dg < -45 else 3
    return b + 4 if coin else b
def k25(dg): return (3 if dg <= 90 else 2) if dg > 0 else (1 if dg <= -90 else 0)
model = ([k20(x) for x in (0, 91, -91)], [k21(x, 0) for x in (0, 61, -61)], [k24(x, 0) for x in (0, 90, -90, 180)], [k25(x) for x in (-45, -120, 45, 120)])
check("Y", yok and cok and model == ([0, 1, 1], [0, 1, 2], [0, 1, 2, 3], [0, 1, 3, 2]),
      "anchors %s; constants %s; model 0x20 %s, 0x21 %s, 0x24 %s, 0x25 %s" % (yok, cok, model[0], model[1], model[2], model[3]))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
