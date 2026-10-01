"""Falsification pass 1 on an-effect-element-frame-by-frame (OPUS, 2026-09-29), from the shipping image.
Each row states what the bytes show; a row marked REFUTES is a clause of the page they break.

  E0  sizes: the nine tails, 005002E0 389, 002F31C0 233, 003A8950 394, 002F35C0 387, 0044B960 212, 002F3570 69, 003A2570 285,
      003A2A10 261, 001EDDA0 27, 002F2530 2,094
  E1  section 2 / 4: every one of the nine tails calls 005002E0, then 002F31C0 on zero and 003A8950 with ecx = 2 on non-zero
      (type 0x02 by tail-jump); each compares definition +0x49 with 0x20 except type 0x05
  E2  section 3: 005002E0 picks [02F97348] + 0x2E0 or, on 0xFF, definition +0x60; mode 1 full distance, mode 2 lane 1 zeroed on
      both points; cull below +4 or above +8; byte +1 bit 0 projects through 02AEECB0 and culls outside 0x6000..0xA000
  E3  section 3: 002F31C0 unlinks through +0x28 / +0x30 with head +0x118 and tail +0x128 and pushes onto +0x120
  E4  section 3: 003A8950 walks eight slots (+0x298 tag, +0x288 index, +0x2A0 start, +0x2C6 parameter, +0x1D0 last-fired),
      tag 2 needs trigger 2 and skips odd frames when 001EDDA0 is 0, tag 3 needs trigger 3, and each firing calls 003A8AE0 with 2
  E5  section 4: 002F35C0 keeps the difference at +0x130 only above [008C5B2C] (= 0.001); first frame clears it and builds the
      up vector at +0x140 from 02064AB0 with lane 1 = 1.0 through [+8] + 0x40
  E6  section 4: mode 3 calls 002F3570 in types 0x04, 0x05, 0x06, 0x07; type 0x05 also tests mode 6 and passes +0x90 / +0xA0
  E7  section 4: round-up to a multiple of word +0x670 (0x04) and +0x6D0 (0x06, 0x07); 0x02 samples at age - word +0x28C floored
      at zero; 0x08 converts by [00D12480] (= 0.00174533)
  E8  section 4: 0x0A fills 32 history entries at age 0 (16 x 2 stores) and shifts 31 on cadence frames
  E9  section 5: 001EDDA0 returns 0 only when [01DFE0C0] is 0 and [01F82E38] is non-zero
  E10 section 4 (REFUTES "four steps"): 0044B960 runs the recurrence five times before its store to 01EF93E8
  E11 section 1 / 3 (REFUTES "child spawns happen only for elements that passed the cull on that frame, or that are expiring"):
      element +0 is definition +0x44 (002F30F2 / 002F30F6), and the base 002F2530, when that type byte is 0x00, runs
      002F3890 and 003A8950(2) at 002F2C4D..002F2C76 with no cull test anywhere in the base
  E12 section 1 (REFUTES "expiry" as lifetime only): the base has a second trigger-3 + release pair (002F2D42 / 002F2D52),
      reached from 002F2A5F when 002F3750's height exceeds element +0x64
  E13 method and section 4 counts (REFUTES "ten per-type tails" and "the other seven tails"): 0044B960 has more than forty
      direct callers, so it is a shared helper and not a tail; section 4 lists six types
  E14 competing case for E11: the update dispatcher 002F3910 sends type 0x00 to the base alone, each of the nine
      types through a wrapper that runs the base and then the cited tail, and type 0x09 to the default arm
  E15 for the dispatch page (REFUTES "released (002F3890)" and "the 394-byte kind-3 release"): 002F3890 (122 B) calls only
      0039AF70, 00398F90 and the cookie check, copies +0x1F0 to +0x1F4 and shifts +0x70 to +0x80, and touches no list field;
      the 394-byte body is 003A8950, the child-spawn slots, and the release is 002F31C0
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
txt = lambda fa: [S(x) for x in body(fa)]
rips = lambda fa: {r for x in body(fa) for r in rip(x)}
imm = lambda x: x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None
at = lambda fa: {x.address: S(x) for x in body(fa)}
f32 = lambda va: struct.unpack("<f", blob[OFF(va):OFF(va) + 4])[0]

TAILS = {0x01: 0x00442600, 0x03: 0x004428F0, 0x08: 0x0044B3C0, 0x02: 0x00449560, 0x04: 0x00445B50, 0x05: 0x0044A180,
         0x06: 0x00447830, 0x07: 0x00448800, 0x0A: 0x0044C850}
SZ = {0x00442600: 346, 0x004428F0: 1587, 0x0044B3C0: 1273, 0x00449560: 965, 0x00445B50: 1269, 0x0044A180: 1071,
      0x00447830: 1436, 0x00448800: 1387, 0x0044C850: 959, 0x005002E0: 389, 0x002F31C0: 233, 0x003A8950: 394,
      0x002F35C0: 387, 0x0044B960: 212, 0x002F3570: 69, 0x003A2570: 285, 0x003A2A10: 261, 0x001EDDA0: 27, 0x002F2530: 2094}
bad = {("%08X" % a): sizes.get(a) for a in SZ if sizes.get(a) != SZ[a]}
check("E0", not bad, "mismatches %s" % bad if bad else "all nineteen sizes as cited")

fork = {}
for ty, fa in TAILS.items():
    B = body(fa)
    cl = [x for x in B if x.mnemonic == "call" and imm(x) == 0x005002E0]
    rel = [x for x in B if x.mnemonic in ("call", "jmp") and imm(x) == 0x002F31C0]
    spn = [x for x in B if x.mnemonic in ("call", "jmp") and imm(x) == 0x003A8950]
    two = spn and any(S(y) == "mov ecx, 2" for y in B if spn[-1].address - 12 <= y.address < spn[-1].address)
    pct = any(S(x).startswith("cmp byte ptr [") and S(x).endswith("+ 0x49], 0x20") for x in B)
    fork[ty] = (bool(cl) and bool(rel) and bool(two) and cl[-1].address < rel[-1].address < spn[-1].address, pct,
                spn[-1].mnemonic if spn else None)
check("E1", all(v[0] for v in fork.values()) and [t for t, v in fork.items() if not v[1]] == [0x05] and fork[0x02][2] == "jmp",
      "fork in all nine: %s; +0x49 percent test missing only in %s; type 0x02 reaches the spawn slots by %s"
      % (all(v[0] for v in fork.values()), ["0x%02X" % t for t, v in fork.items() if not v[1]], fork[0x02][2]))

C = at(0x005002E0)
check("E2", 0x02F97348 in rips(0x005002E0) and C.get(0x00500303) == "add rbx, 0x2e0" and C.get(0x0050030A) == "cmp byte ptr [rbx], 0xff"
      and C.get(0x0050030F) == "lea rbx, [rcx + 0x60]" and C.get(0x0050033B) == "mov dword ptr [rsp + 0x24], 0"
      and C.get(0x00500361) == "mov dword ptr [rsp + 0x34], 0" and C.get(0x00500319) == "je 0x50038a"
      and {0x02AED5F0, 0x02AEEA20, 0x02AEECB0} <= rips(0x005002E0) and C.get(0x00500373) == "movss xmm1, dword ptr [rbx + 4]"
      and C.get(0x0050037D) == "comiss xmm0, dword ptr [rbx + 8]" and C.get(0x005003DD) == "and ecx, 1"
      and C.get(0x00500415) == "mov ecx, 0x6000" and C.get(0x00500423) == "mov edx, 0xa000" and C.get(0x00500448) == "mov eax, 1",
      "record choice, the two distance modes (lane 1 zeroed only in mode 2), the +4 / +8 window, the screen window")

R = at(0x002F31C0)
check("E3", R.get(0x002F3263) == "mov qword ptr [rdi + 0x118], rax" and R.get(0x002F327D) == "mov qword ptr [rdi + 0x128], rax"
      and R.get(0x002F3297) == "mov qword ptr [rdi + 0x120], rbx" and R.get(0x002F3284) == "mov qword ptr [rbx + 0x28], 0",
      "unlink via +0x28 / +0x30, head +0x118, tail +0x128, push onto +0x120")

P = at(0x003A8950)
check("E4", P.get(0x003A898D) == "lea r14, [rax + 0x298]" and P.get(0x003A8994) == "mov r12d, 8" and P.get(0x003A899A) == "lea rsi, [rax + 0x2a0]"
      and P.get(0x003A8972) == "lea rdi, [rdx + 0x1d0]" and P.get(0x003A8A77) == "movzx ecx, word ptr [rsi - 0x18]"
      and P.get(0x003A8A73) == "movzx edx, word ptr [rsi + 0x26]" and P.get(0x003A89DF) == "call 0x1edda0"
      and P.get(0x003A89E8) == "test byte ptr [rbx + 0x40], 1" and P.get(0x003A89F2) == "cmp r15d, 2" and P.get(0x003A89D3) == "cmp r15d, 3"
      and 0x02EBEF90 in rips(0x003A8950) and P.get(0x003A8A2A) == "call 0x4314e0" and P.get(0x003A8A8D) == "mov r8d, 2"
      and P.get(0x003A8A97) == "call 0x3a8ae0",
      "eight slots at +0x298 / +0x288 / +0x2A0 / +0x2C6, last-fired +0x1D0; tag 2 on trigger 2 with the odd-frame skip; tag 3 on 3")

M = at(0x002F35C0)
check("E5", M.get(0x002F35CA) == "cmp dword ptr [rdx + 0x40], 0" and abs(f32(0x008C5B2C) - 0.001) < 1e-9 and 0x008C5B2C in rips(0x002F35C0)
      and M.get(0x002F369A) == "movdqa xmmword ptr [rdi + 0x130], xmm0" and M.get(0x002F36AE) == "mov qword ptr [rdx + 0x130], rax"
      and 0x02064AB0 in rips(0x002F35C0) and M.get(0x002F36D2) == "mov dword ptr [rdx + 0x144], 0x3f800000"
      and M.get(0x002F36CE) == "add rcx, 0x40" and M.get(0x002F370F) == "call 0x3a2570",
      "direction kept above %.4f; first-frame up vector from 02064AB0, lane 1 = 1.0, through [+8] + 0x40" % f32(0x008C5B2C))

m3 = {ty: any(x.mnemonic == "call" and imm(x) == 0x002F3570 for x in body(TAILS[ty])) for ty in (0x04, 0x05, 0x06, 0x07)}
F5 = at(0x0044A180)
check("E6", all(m3.values()) and F5.get(0x0044A4BE) == "cmp al, 6" and F5.get(0x0044A4C2) == "lea r9, [rbx + 0x90]"
      and F5.get(0x0044A4CC) == "lea r8, [rbx + 0xa0]" and F5.get(0x0044A4D8) == "call 0x2f35c0"
      and not any(S(x) == "cmp al, 6" for ty in (0x04, 0x06, 0x07) for x in body(TAILS[ty])),
      "mode 3 -> 002F3570 in %s; only 0x05 tests mode 6, with the pre-parent history" % sorted("0x%02X" % t for t in m3))
F4, F2 = at(0x00445B50), at(0x00449560)
rnd = {ty: [s for s in txt(TAILS[ty]) if s.startswith("movzx") and ("+ 0x670]" in s or "+ 0x6d0]" in s)] for ty in (0x04, 0x06, 0x07)}
check("E7", "0x670" in str(rnd[0x04]) and "0x6d0" in str(rnd[0x06]) and "0x6d0" in str(rnd[0x07])
      and F4.get(0x00445D99) == "cmp cx, 1" and F4.get(0x00445DA4) == "jl 0x445dae" and F4.get(0x00445DB1) == "inc eax" and F4.get(0x00445DB3) == "imul eax, ecx"
      and F2.get(0x0044966E) == "movzx eax, word ptr [rbx + 0x28c]" and F2.get(0x00449677) == "cmovns edx, ecx"
      and 0x00D12480 in rips(0x0044B3C0) and abs(f32(0x00D12480) - 0.00174533) < 1e-8,
      "round-up words %s; delayed colour time floored at 0; degree-tenths factor %.8f" % (rnd, f32(0x00D12480)))
T = at(0x0044C850)
check("E8", T.get(0x0044CB53) == "mov ecx, 0x10" and T.get(0x0044CB68) == "movups xmmword ptr [rax - 0x30], xmm0"
      and T.get(0x0044CB70) == "movups xmmword ptr [rax - 0x20], xmm0" and T.get(0x0044CB8B) == "mov ecx, 0x1f"
      and T.get(0x0044CB7C) == "call 0x1edda0" and T.get(0x0044CB85) == "test byte ptr [rbx + 0x40], 1"
      and T.get(0x0044CBB8) == "movups xmmword ptr [rbx + 0x250], xmm0",
      "32 entries filled at age 0; 31 shifted on cadence frames; newest at +0x250")
H = txt(0x001EDDA0)
check("E9", H[:6] == ["cmp dword ptr [rip + 0x1c10319], 0", "jne 0x1eddb5", "cmp dword ptr [rip + 0x1d95088], 0", "je 0x1eddb5", "xor eax, eax", "ret"]
      and rips(0x001EDDA0) == {0x01DFE0C0, 0x01F82E38}, "0 only when [01DFE0C0] == 0 and [01F82E38] != 0")

G = body(0x0044B960)
steps = sum(1 for x in G if S(x).endswith(", 0x1fc00000"))
store = [x.address for x in G if 0x01EF93E8 in rip(x) and x.operands[0].type == X86_OP_MEM]
check("E10", steps == 5 and store == [0x0044BA00],
      "(REFUTES) %d recurrence steps (each '| 0x1FC00000') before the single state store at %s; the page says four; "
      "the 1.0 path reads [01CEBBA8] = %.1f" % (steps, ["%08X" % a for a in store], f32(0x01CEBBA8)))

D = at(0x002F2D60)
Bz = at(0x002F2530)
spawn_in_base = [a for a, s in Bz.items() if s == "call 0x3a8950"]
cull_in_base = [a for a, s in Bz.items() if s == "call 0x5002e0"]
check("E11", D.get(0x002F30F2) == "movzx ecx, byte ptr [rax + 0x44]" and D.get(0x002F30F6) == "mov byte ptr [rbx], cl"
      and Bz.get(0x002F2C51) == "cmp byte ptr [rax + 0x44], r15b" and Bz.get(0x002F253C) == "xor r15d, r15d"
      and Bz.get(0x002F2C69) == "call 0x2f3890" and Bz.get(0x002F2C71) == "mov ecx, 2" and 0x002F2C76 in spawn_in_base and not cull_in_base
      and txt(0x002F3890).count("movdqa xmmword ptr [rbx + 0x80], xmm0") == 1,
      "(REFUTES) type byte = definition +0x44; with it 0 the base runs 002F3890 (history shift, colour copy) and "
      "003A8950(2) at 002F2C76; the base never calls 005002E0 (%d calls)" % len(cull_in_base))
check("E12", Bz.get(0x002F2A56) == "call 0x2f3750" and Bz.get(0x002F2A5B) == "comiss xmm0, dword ptr [rbx + 0x64]" and Bz.get(0x002F2A5F) == "ja 0x2f2d37"
      and Bz.get(0x002F2D42) == "mov ecx, 3" and Bz.get(0x002F2D47) == "call 0x3a8950" and Bz.get(0x002F2D52) == "call 0x2f31c0"
      and Bz.get(0x002F25B2) == "mov ecx, dword ptr [rbx + 0x4c]" and Bz.get(0x002F25C8) == "mov ecx, 3",
      "(REFUTES lifetime-only) trigger 3 + release twice: the lifetime arm 002F25B2..002F25D8 and the height arm 002F2A5F -> 002F2D37..002F2D52")
text = next(x for x in SECS if x[0] == ".text")
raw = blob[text[3]:text[3] + text[4]]
n = sum(1 for k in range(len(raw) - 5) if raw[k] == 0xE8 and text[1] + k + 5 + struct.unpack_from("<i", raw, k + 1)[0] == 0x0044B960)
check("E13", n > 40 and len(TAILS) == 9,
      "(REFUTES the counts) 0044B960 has %d direct call sites, so it is a shared helper; the method's ten includes it, "
      "section 4's 'other seven' lists six types" % n)
idx = blob[OFF(BASE + 0x1D3AEC):OFF(BASE + 0x1D3AEC) + 0x0B]
tab = struct.unpack("<60I", blob[OFF(BASE + 0x1D3A2C):OFF(BASE + 0x1D3A2C) + 240])
upd = {}
for ty in range(0x0B):
    arm = BASE + tab[idx[ty]]
    upd[ty] = imm(next(md.disasm(blob[OFF(arm):OFF(arm) + 8], arm)))
wrap = {ty: [imm(x) for x in body(upd[ty]) if x.mnemonic in ("call", "jmp") and imm(x)][:2] for ty in TAILS}
check("E14", at(0x002F3910).get(0x002F3939) == "jmp r8" and upd[0x00] == 0x002F2530
      and all(w == [0x002F2530, TAILS[ty]] for ty, w in wrap.items()) and upd[0x09] == 0x0043EAB0,
      "update dispatch 002F3910: type 0x00 is the base alone (%08X); each of the nine runs the base then its cited tail; "
      "type 0x09 goes to the default %08X" % (upd[0x00], upd[0x09]))
Q = body(0x002F3890)
qcalls = sorted({imm(x) for x in Q if x.mnemonic == "call"})
qtxt = [S(x) for x in Q]
check("E15", sizes[0x002F3890] == 122 and qcalls == [0x00398F90, 0x0039AF70, 0x00808C40] and "mov dword ptr [rcx + 0x1f4], eax" in qtxt
      and "movdqa xmmword ptr [rbx + 0x80], xmm0" in qtxt and "movdqa xmmword ptr [rbx + 0x70], xmm1" in qtxt
      and not any(("+ 0x118]" in t or "+ 0x120]" in t or "+ 0x128]" in t) for t in qtxt) and sizes[0x003A8950] == 394,
      "(REFUTES the dispatch page's two release labels) 002F3890 calls %s, copies the colour and shifts the history, no list "
      "field; 003A8950 (394 B) is the spawn slots; the release is 002F31C0" % ["%08X" % c for c in qcalls])
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
