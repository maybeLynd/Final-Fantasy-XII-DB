"""Falsification pass 1 on how-a-camera-reaches-the-renderer (OPUS, 2026-09-29), from the shipping image.
Each row states what the bytes show; a row marked REFUTES is a clause of the page they break. The camerashake census
(members/camerashake_census.py) is carried, not re-run.

  W0  the 38 cited sizes
  W1  caller sets: three submitters with 0x14 / 0x14 / 0x64; one caller each for the update, the reset and the driver; two for
      the offset setter; 003DD230 from the 1a3 handler and one more
  W2  section 2: 003829D0 walks eight 0xE0 slots from 02AED630 for a zero +0xD0, copies 0xD0 bytes, stores +0xD4 and +0xD0 = 1,
      drops when full, and then runs the default-view test either way
  W3  section 3: the selection - flag 1 consumed, best from -1, strictly greater, slot 0 then 1..7 in order
  W4  section 3: 00229D20 returns 4/3 unless byte 02064AD1 is 1, 2, 3 or 5, when it tail-calls the device's value; the update
      stores it at 02AED4E0 / 02AED540 and passes it as the aspect of the projections (xmm8 -> xmm2)
  W5  section 4: the constants the builder reads - 0.7854 (the 45-degree cap), 1.7778 and 1.1547 (the reference projection),
      1000 (the far plane) - and 003CBA50's s / aspect
  W6  section 4a: 0037D970 calls 003D83A0 before testing 02089350 (ebx), then 02EBF3C4 and 02EBF3C0 against the zero in ebx
  W7  section 4a: the MT thunk 00379CE0 has nine call sites, all inside 0037D1F0; its body 00863C80 reads 02EB3870 / 02EB4230
  W8  section 4a correction box: 00314370 loops ebx over five slots, testing +0x10 bit 0, calling 003DA050 then 003DCFB0
  W9  section 4a: 003DD230's four rejections (channel > 3, no bank, negative index, index >= count), a negative draw mapped
      through 005C5230 (xor eax, eax; ret), and the per-draw word +0x1C + draw x 2
  W10 section 4a: the 1a3 handler pushes -1 and pops it back as the draw; camerashakestart (019C) pushes -1 and jumps to it
  W11 section 4a (REFUTES "Every start form ends in 003DD230 ... reached through the handler of camerashakestart_1a3" and, as a
      mechanism, "script shakes always apply to draw 0"): verb 01A2 camerashakestart_1a2 has its own handler 003492F0, which
      pops the draw from the script and passes it on; 003DD230 bounds only a negative draw. The shipped us scripts never call it
      (the census counts no 1a2 call), so shipped shakes still reach draw 0 only
  W12 appended note on 00229D20 (REFUTES "the speed-mode factor" and "the authored answer"): it is the aspect ratio of W4 -
      4/3 by default, otherwise the device's own value through 00182EE0 - as section 3 already says
"""
import io, os, struct
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")
blob = io.open(EXE, "rb").read()
pe = pefile.PE(EXE, fast_load=True); BASE = pe.OPTIONAL_HEADER.ImageBase
SECS = [(s.Name.rstrip(b"\0").decode(), BASE + s.VirtualAddress, max(s.Misc_VirtualSize, s.SizeOfRawData), s.PointerToRawData, s.SizeOfRawData)
        for s in pe.sections]
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
fails = 0


def OFF(va):
    for _n, start, size, raw, rawsz in SECS:
        if start <= va < start + min(size, rawsz):
            return raw + (va - start)
    raise ValueError("VA %08X in no raw section" % va)


def check(tag, ok, text):
    global fails
    fails += not ok
    print("%s  %s  %s" % ("SURVIVES" if ok else "BROKEN  ", tag, text))


sizes = {}
for i, line in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
    p = line.rstrip("\n").split("\t")
    if i and len(p) > 2:
        try:
            sizes[int(p[0], 16)] = int(p[2])
        except ValueError:
            pass
S = lambda x: ("%s %s" % (x.mnemonic, x.op_str)).strip()
rip = lambda x: [x.address + x.size + o.mem.disp for o in x.operands if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP]
body = lambda fa: [x for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa)]
at = lambda fa: {x.address: S(x) for x in body(fa)}
txt = lambda fa: [S(x) for x in body(fa)]
rips = lambda fa: {r for x in body(fa) for r in rip(x)}
f32 = lambda va: struct.unpack("<f", blob[OFF(va):OFF(va) + 4])[0]
text = next(x for x in SECS if x[0] == ".text")
raw = blob[text[3]:text[3] + text[4]]


def callers(t):
    return sorted(text[1] + k for k in range(len(raw) - 5)
                  if raw[k] in (0xE8, 0xE9) and text[1] + k + 5 + struct.unpack_from("<i", raw, k + 1)[0] == t)


SZ = {0x003829D0: 373, 0x00382910: 163, 0x003820C0: 2125, 0x00259970: 17, 0x00229D20: 33, 0x003CBA50: 114, 0x003CBC40: 91,
      0x003B4150: 15, 0x00182570: 33, 0x001824E0: 72, 0x003829C0: 8, 0x00382B70: 119, 0x0037DB40: 35, 0x0037DCC0: 35,
      0x0037D890: 209, 0x0037D4C0: 808, 0x0037D970: 0xF5, 0x003DCFB0: 285, 0x0037D1F0: 712, 0x0037D130: 190, 0x00314370: 85,
      0x003DD230: 225, 0x0037DCF0: 81, 0x003DD320: 33, 0x003DCF60: 70, 0x002563F0: 185, 0x003CBD60: 571, 0x00233230: 524,
      0x00380650: 427, 0x0022FF10: 201, 0x00380190: 198, 0x003CBCA0: 178, 0x00182640: 157, 0x001897C0: 1101, 0x0018A120: 505,
      0x001854C0: 830, 0x0024E180: 140, 0x004679C0: 173}
bad = {("%08X" % a): sizes.get(a) for a in SZ if sizes.get(a) != SZ[a]}
check("W0", not bad, "mismatches %s" % bad if bad else "all 38 sizes as cited")
CW = {0x003829D0: [0x00259932, 0x0025997C, 0x003ED9A2], 0x003820C0: [0x0036F514], 0x00382910: [0x0036F4F2],
      0x00382B70: [0x0037D7C4, 0x0037D910], 0x003DCFB0: [0x0031439E], 0x003DD230: [0x00349340, 0x0034978B]}
cbad = {("%08X" % t): ["%08X" % c for c in callers(t)] for t, w in CW.items() if callers(t) != w}
pri = {}
for site in (0x00259932, 0x0025997C, 0x003ED9A2):
    win = list(md.disasm(blob[OFF(site - 16):OFF(site)], site - 16))
    pri["%08X" % site] = [S(x) for x in win if S(x).startswith("mov edx, ")][-1:]
check("W1", not cbad and [v[0] if v else None for v in pri.values()] == ["mov edx, 0x14", "mov edx, 0x14", "mov edx, 0x64"],
      "caller sets %s; submit priorities %s" % (cbad or "as measured", pri))
U = at(0x003829D0)
check("W2", U.get(0x00382A70) == "cmp dword ptr [rcx + 0xd0], 0" and U.get(0x00382A79) == "add rcx, 0xe0" and 0x02AEDD30 in rips(0x003829D0)
      and U.get(0x00382A85) == "jmp 0x382b15" and U.get(0x00382B01) == "mov dword ptr [rcx + 0xd4], edi" and U.get(0x00382B07) == "mov dword ptr [rcx + 0xd0], 1"
      and U.get(0x00382B18) == "call 0x259fa0" and U.get(0x00382B21) == "call 0x1821f0" and U.get(0x00382B28) == "call 0x182340",
      "eight 0xE0 slots to 02AEDD30; full -> straight to the view test; priority +0xD4, flag +0xD0")
C = at(0x003820C0)
tail = [C.get(a) for a in (0x0038212B, 0x0038212D, 0x0038214D, 0x0038214F)]
check("W3", C.get(0x003820F6) == "or ebx, 0xffffffff" and C.get(0x00382100) == "cmp dword ptr [rip + 0x276b5f9], 1" and C.get(0x00382125) == "mov dword ptr [rip + 0x276b5d5], edi"
      and tail == ["cmp eax, ebx", "jle 0x382138", "cmp ebx, eax", "jge 0x38215a"],
      "best from -1; the flag cleared; slot 0 takes on eax > ebx, later slots on ebx < eax - strictly greater, earliest wins")
G = at(0x00229D20)
proj = [a for a, s in C.items() if s == "call 0x3cbb30"]
check("W4", G.get(0x00229D27) == "lea eax, [rcx - 1]" and G.get(0x00229D2A) == "cmp al, 2" and G.get(0x00229D2E) == "cmp cl, 5" and G.get(0x00229D3C) == "jmp 0x182ee0"
      and abs(f32(0x00908D54) - 4.0 / 3.0) < 1e-6 and C.get(0x003820FB) == "call 0x229d20" and C.get(0x0038210B, "").endswith(", xmm8")
      and C.get(0x00382637) == "movaps xmm2, xmm8" and 0x00382651 in proj,
      "4/3 unless the mode byte is 1-3 or 5 (then the device's value); stored at 02AED4E0 / 02AED540 and passed as the projection's aspect")
vals = sorted({round(f32(r), 4) for x in body(0x003820C0) for r in rip(x) if 0x00800000 < r < 0x01000000 or 0x01C00000 < r < 0x01E00000})
P = at(0x003CBA50)
check("W5", {0.7854, 1.7778, 1.1547, 1000.0} <= set(vals) and P.get(0x003CBA50) == "mulss xmm3, dword ptr [rcx + 0x10]" and P.get(0x003CBA68) == "divss xmm0, xmm2",
      "constants %s; 003CBA50 scales by +0x10 and divides by the aspect" % vals)
H = at(0x0037D970)
check("W6", H.get(0x0037D989) == "call 0x237420" and H.get(0x0037D9F6) == "call 0x3d83a0" and H.get(0x0037D9FB) == "test ebx, ebx"
      and H.get(0x0037D9FF) == "cmp dword ptr [rip + 0x2b419bf], ebx" and H.get(0x0037DA07) == "cmp dword ptr [rip + 0x2b419b3], ebx",
      "the candidate calculation precedes both option compares, which test against the zero in ebx")
th = callers(0x00379CE0)
check("W7", len(th) == 9 and all(0x0037D1F0 <= s < 0x0037D1F0 + 712 for s in th) and txt(0x00379CE0)[0] == "jmp 0x863c80"
      and {0x02EB3870, 0x02EB4230} <= rips(0x00863C80),
      "nine thunk sites, all in 0037D1F0; 00863C80 on the gameplay state 02EB3870 / 02EB4230")
L = at(0x00314370)
check("W8", [L.get(a) for a in (0x00314381, 0x0031438D, 0x00314396, 0x0031439E, 0x003143A5)] == ["xor ebx, ebx", "test byte ptr [rax + 0x10], 1", "call 0x3da050", "call 0x3dcfb0", "cmp ebx, 5"],
      "five slots, +0x10 bit 0, the camera driver then the shake driver")
D = at(0x003DD230)
check("W9", D.get(0x003DD263) == "jns 0x3dd26c" and D.get(0x003DD265) == "call 0x5c5230" and txt(0x005C5230) == ["xor eax, eax", "ret"]
      and D.get(0x003DD26C) == "cmp edi, 3" and D.get(0x003DD278) == "je 0x3dd2f6" and D.get(0x003DD27C) == "js 0x3dd2f6" and D.get(0x003DD282) == "jae 0x3dd2f6"
      and D.get(0x003DD2EC) == "mov word ptr [rbx + rax*2 + 0x1c], di",
      "the four rejections; a negative draw becomes 0; the per-draw word +0x1C + draw x 2")
A3, A9 = at(0x00349730), at(0x00349A60)
check("W10", A3.get(0x00349744) == "or edx, 0xffffffff" and A3.get(0x0034974D) == "call 0x267f90" and A3.get(0x0034977C) == "mov dword ptr [rsp + 0x20], ebx"
      and A9.get(0x00349A8E) == "or edx, 0xffffffff" and txt(0x00349A60)[-1] == "jmp 0x349730",
      "1a3 pushes -1 and pops it back as the draw; 019C pushes -1 and jumps to 1a3")
A2 = at(0x003492F0)
draw_checks = [s for s in D.values() if "ecx" in s and s.startswith("cmp")]
check("W11", A2.get(0x00349307) == "call 0x2640c0" and A2.get(0x00349312) == "call 0x267e10" and A2.get(0x0034931A) == "mov ebx, eax"
      and A2.get(0x00349331) == "mov dword ptr [rsp + 0x20], ebx" and A2.get(0x00349340) == "call 0x3dd230"
      and not any(s == "call 0x267f90" for s in A2.values()) and not draw_checks,
      "(REFUTES) 01A2's handler 003492F0 pushes nothing and pops the draw from the script (the first of three pops); "
      "003DD230 has no upper bound on a non-negative draw (%s)" % (draw_checks or "no compare on it"))
check("W12", G.get(0x00229D33) == "movss xmm0, dword ptr [rip + 0x6df019]" and txt(0x00182EE0)[1] == "call 0x1ddab0" and "jmp 0x1dd120" in txt(0x00182EE0),
      "(REFUTES the label) 00229D20 returns 4/3 or tail-calls 00182EE0, which asks the device object (001DDAB0) through 001DD120 - "
      "the aspect of W4, not a speed-mode factor or an authored answer")
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
