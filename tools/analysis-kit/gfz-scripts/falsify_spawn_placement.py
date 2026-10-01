"""Falsification pass 1 on CONTRACT-spawn-placement (OPUS, 2026-09-29), from the shipping image. Killers first.

  P0  section 2: 00234AF0 has one caller, Spawn_SelectAndPrepareAutomaticEntry (00235950); ECX reaches 003209C0 untouched;
      min / max arrive in xmm2 / xmm3, the out position in rdx, out_observed as argument 5 and a slot flag as argument 6
  P1  I1 SpawnKeep_SetReturnWindow is `test ecx, ecx / mov eax, 0x12c / cmovs ecx, eax / mov [cell], ecx / ret`
  P2  I5 the band test `ucomiss (max - min), 0` runs before the fetch, and only an exact 0.0 is refused (NaN proceeds);
      I2 the fetch is refused on `js`; I4 a null leader returns 0 after the authored position was copied out
  P3  I3 POINT: the arc half is the INTEGER arcDeg / 2 (`cdq / sub / sar 1`) times 2pi / 360, compared with
      Math_NormalizeAngleDifference, which returns an absolute value; then 00234DA0 with SQUARED bounds
  P4  I4 made exact: the point-mode band is 00234DA0's slot walk over 0..3 (0031B810), rejecting on the first eligible
      slot outside [min^2, max^2]; the one caller passes argument 6 = 0, admitting only the party-focus slot (003273B0)
  P4b (the check that withdrew a first-draft refutation of I4) the leader getter 003272A0 and the focus test 003273B0 read
      the SAME handle, PartyFocus_GetCurrentPackedActorHandle (003590D0), so with 0 the band is measured to the leader's
      own slot                                         KILLER: the two read different handles
  P5  I3 AREA: r = (RNG % (int)((max - min) * 100)) / 100 + min and theta offset = ((RNG % arcDeg) - arcDeg / 2) degrees,
      both integer `idiv`, so the radius is quantised to 0.01 and the angle to whole degrees; the only filter is
      FieldRegion_ContainsWorldPosition; a divisor of 0 (band under 0.01, or arcDeg 0) is not guarded
  P6  section 9: exactly two calls to RNG_SharedGameplayLCG_NextU32, both on the area side; each call steps the LCG three
      times (three `imul 0x41c64e6d`) and stores once; its result is at most 31 bits, so the signed `idiv` is safe;
      the point path's closure calls no RNG
  P7  (state the contract did not list) arcDeg is the global 02089358: read only here, written by
      Spawn_SetCandidateHeadingArcDegrees (0023A1F0) and set to 180 by 0023A520
  P8  I7 / I8 00319390 writes [rdx] and [rdx + 8] only, through the 01F004E0 table with `& 0x7fff` and the 0x2000 offset;
      00234AF0 never writes rsp+0x50..0x5B and copies rsp+0x54 into result.y
"""
import collections, io, os, re, struct
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP, X86_REG_RSP

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


sizes, names = {}, {}
for i, line in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
    p = line.rstrip("\n").split("\t")
    if i and len(p) > 2:
        try:
            sizes[int(p[0], 16)] = int(p[2]); names[p[1]] = int(p[0], 16)
        except ValueError:
            pass
S = lambda x: ("%s %s" % (x.mnemonic, x.op_str)).strip()
rip = lambda x: [x.address + x.size + o.mem.disp for o in x.operands if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP]
T = lambda x: x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None
f32 = lambda va: struct.unpack("<f", blob[OFF(va):OFF(va) + 4])[0]
text = next(x for x in SECS if x[0] == ".text")

refs = collections.defaultdict(list)          # target -> [(function, insn)]
calls_to = collections.defaultdict(list)      # target -> [(function, address, mnemonic)]
bodies = {}
for fa in sorted(sizes):
    if not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        code = blob[OFF(fa):OFF(fa) + sizes[fa]]
    except ValueError:
        continue
    ins = list(md.disasm(code, fa))
    bodies[fa] = ins
    for x in ins:
        for t in rip(x):
            refs[t].append((fa, x))
        if x.mnemonic in ("call", "jmp") and T(x) is not None:
            calls_to[T(x)].append((fa, x.address, x.mnemonic))


def is_write(x):
    return bool(x.operands) and x.operands[0].type == X86_OP_MEM and x.mnemonic in ("mov", "movss", "movaps", "movups", "movdqa", "inc", "dec", "add", "sub", "or", "and", "xor")


def at(fa, va):
    return next(S(x) for x in bodies[fa] if x.address == va)


def run(fa, lo, hi):
    return [S(x) for x in bodies[fa] if lo <= x.address <= hi]


def calls(fa, lo=0, hi=1 << 40):
    return [(x.address, T(x)) for x in bodies[fa] if x.mnemonic == "call" and T(x) is not None and lo <= x.address <= hi]


PLACE, VALID, AUTO, RNG, LEADER, FOCUS = 0x00234AF0, 0x00234DA0, 0x00235720, 0x00328370, 0x003272A0, 0x003273B0
N = lambda n: names.get(n)
pb = bodies[PLACE]

# P0 section 2: the one caller and the argument registers
c0 = [("%08X" % f, "%08X" % a) for f, a, _m in calls_to[PLACE]]
auto = run(AUTO, 0x00235930, 0x00235950)
check("P0", c0 == [("00235720", "00235950")] and N("Spawn_SelectAndPrepareAutomaticEntry") == AUTO
      and auto == ["lea rax, [rsp + 0x34]", "mov dword ptr [rsp + 0x28], 0", "movaps xmm3, xmm8", "mov qword ptr [rsp + 0x20], rax",
                   "movaps xmm2, xmm7", "lea rdx, [rsp + 0x60]", "mov ecx, edi", "call 0x234af0"]
      and at(PLACE, 0x00234B55) == "call 0x3209c0" and not [x for x in pb if x.address < 0x00234B55 and "cx" in x.op_str.split(",")[0]]
      and run(PLACE, 0x00234B20, 0x00234B20) == ["mov r14, qword ptr [rbp + 0x77]"] and at(PLACE, 0x00234C20) == "mov eax, dword ptr [rbp + 0x7f]",
      "one caller %s passing: %s; argument 5 -> r14 (out_observed), argument 6 -> [rbp + 0x7f] (the slot flag)" % (c0, auto))
# P1 I1
setw = N("SpawnKeep_SetReturnWindow")
sw = [S(x) for x in bodies.get(setw, [])]
cell = rip(bodies[setw][3])[0] if setw else None
check("P1", sw[:3] == ["test ecx, ecx", "mov eax, 0x12c", "cmovs ecx, eax"] and sw[4:] == ["ret"] and cell is not None,
      "SpawnKeep_SetReturnWindow %08X: %s -> cell %08X" % (setw or 0, sw, cell or 0))
# P2 I5, I2, I4
check("P2", run(PLACE, 0x00234B42, 0x00234B55) == ["ucomiss xmm8, xmm0", "jp 0x234b51", "jne 0x234b51", "xor eax, eax", "jmp 0x234d0a",
                                                   "lea rdx, [rbp - 0x69]", "call 0x3209c0"]
      and run(PLACE, 0x00234B5A, 0x00234B5C) == ["test eax, eax", "js 0x234b4a"]
      and run(PLACE, 0x00234B68, 0x00234B76) == ["movss dword ptr [rbx], xmm0", "movss xmm0, dword ptr [rbp - 0x51]", "movss dword ptr [rbx + 8], xmm0", "movss dword ptr [rbx + 4], xmm1"]
      and at(PLACE, 0x00234B83) == "call 0x3272a0" and N("BattleUnit_GetPartyLeader") == LEADER and at(PLACE, 0x00234B8E) == "je 0x234d02",
      "empty band refused before the fetch (NaN proceeds: jp); fetch refused on js; authored position copied out, then the leader test")
# P3 I3 POINT: integer half-arc, absolute wrapped difference, squared bounds
nad = [S(x) for x in bodies[0x0031A930]]
k2pi = f32(rip(next(x for x in pb if x.address == 0x00234C07))[0]); k360 = f32(rip(next(x for x in pb if x.address == 0x00234C0F))[0])
check("P3", run(PLACE, 0x00234BF8, 0x00234C1A) == ["mov eax, r15d", "cdq", "sub eax, edx", "sar eax, 1", "movd xmm1, eax", "cvtdq2ps xmm1, xmm1",
                                                   "mulss xmm1, dword ptr [rip + 0x1ab7069]", "divss xmm1, dword ptr [rip + 0x6cd821]", "comiss xmm1, xmm0", "jb 0x234cf7"]
      and abs(k2pi - 6.2831853) < 1e-5 and k360 == 360.0 and nad[1] == "subss xmm0, xmm1" and any(s.startswith("andps xmm0") for s in nad)
      and run(PLACE, 0x00234BC8, 0x00234BC8) == ["mulss xmm7, xmm7"] and at(PLACE, 0x00234BD4) == "mulss xmm6, xmm6" and at(PLACE, 0x00234C37) == "call 0x234da0",
      "half arc = (arcDeg / 2, integer) * %.7f / %.0f against |wrap(yaw - toCandidate)| (0031A930 ends in andps); bounds squared; then 00234DA0" % (k2pi, k360))
# P4 (REFUTES I4 for point mode): four slots, universal rejection, and the focus-only flag the one caller passes
vb = bodies[VALID]
check("P4", at(VALID, 0x00234DC3) == "mov r12d, dword ptr [rsp + 0xb0]" and at(VALID, 0x00234DE2) == "call 0x31b810"
      and run(VALID, 0x00234E19, 0x00234E28) == ["test r12d, r12d", "jne 0x234e2a", "mov ecx, dword ptr [rbx + 8]", "call 0x3273b0", "test eax, eax", "je 0x234e87"]
      and N("PartyFocus_IsCurrentPackedActorHandle") == FOCUS and run(VALID, 0x00234E87, 0x00234E8C) == ["inc edi", "cmp edi, 4", "jl 0x234de0"]
      and run(VALID, 0x00234E57, 0x00234E6A) == ["movss xmm1, dword ptr [r15]", "comiss xmm1, xmm6", "ja 0x234ebe", "test r14, r14", "je 0x234e6c", "comiss xmm6, dword ptr [r14]", "ja 0x234ebe"]
      and at(VALID, 0x00234EBE) == "xor eax, eax" and LEADER not in [t for _a, t in calls(VALID)]
      and "mov dword ptr [rsp + 0x28], 0" in auto,
      "00234DA0 walks slots 0..3 (0031B810), rejects on the first eligible slot outside [min^2, max^2], never calls 003272A0; argument 6 = 0 "
      "from the one caller admits only the party-focus slot (003273B0) - the leader's, see P4b")
# P4b the leader and the focus slot are the same handle
lg = [S(x) for x in bodies[LEADER]]; fc = [S(x) for x in bodies[FOCUS]]
check("P4b", lg[1] == "call 0x3590d0" and "call 0x3588b0" in lg and fc[3:6] == ["call 0x3590d0", "xor edx, edx", "cmp eax, ebx"]
      and N("PartyFocus_GetCurrentPackedActorHandle") == 0x003590D0 and len(bodies[0x003590D0]) == 2,
      "003272A0 resolves %s through 003588B0; 003273B0 compares a slot's handle with %s - the same handle"
      % (lg[1], fc[3]))
# P5 I3 AREA: quantised radius and angle, region-only filter, unguarded divisors
k100a = f32(rip(next(x for x in pb if x.address == 0x00234C48))[0]); k100b = f32(rip(next(x for x in pb if x.address == 0x00234C60))[0])
area = run(PLACE, 0x00234C43, 0x00234C83)
check("P5", area[:10] == ["call 0x328370", "mulss xmm8, dword ptr [rip + 0x6be4e3]", "cdq", "cvttss2si ecx, xmm8", "idiv ecx", "movd xmm6, edx",
                          "cvtdq2ps xmm6, xmm6", "divss xmm6, dword ptr [rip + 0x6be4cc]", "addss xmm6, xmm7", "call 0x328370"]
      and k100a == 100.0 and k100b == 100.0 and "idiv r15d" in area and area[-4:] == ["cdq", "sub eax, edx", "sar eax, 1", "sub ecx, eax"]
      and at(PLACE, 0x00234C83) == "sub ecx, eax" and run(PLACE, 0x00234CC9, 0x00234CD0) == ["call 0x2374e0", "test eax, eax", "je 0x234cf7"]
      and not [s for s in run(PLACE, 0x00234C43, 0x00234C76) if s.startswith(("test ecx", "test r15d", "cmp ecx", "cmp r15d"))]
      and 0x00234DA0 not in [t for a, t in calls(PLACE, 0x00234C43, 0x00234CF2)],
      "r = (RNG %% (int)((max-min)*%.0f)) / %.0f + min; offset = RNG %% arcDeg - arcDeg/2 whole degrees; region test only; no divisor guard" % (k100a, k100b))
# P6 section 9: two draws, three LCG steps each, 31-bit result; nothing on the point path draws
rb = [S(x) for x in bodies[RNG]]
rc = [a for a, t in calls(PLACE) if t == RNG]
seen, st = set(), [VALID, 0x0031AC90, 0x0031A930]
while st:
    f = st.pop()
    if f in seen or f not in bodies:
        continue
    seen.add(f)
    for x in bodies[f]:
        t = T(x) if x.mnemonic in ("call", "jmp") else None
        if t is not None and t in bodies and not (f <= t < f + sizes[f]):
            st.append(t)
check("P6", rc == [0x00234C43, 0x00234C6C] and sum("0x41c64e6d" in s for s in rb) == 3 and sum(s.startswith("mov dword ptr [rip") for s in rb) == 1
      and "and edx, 0x7ff" in rb and rb[-3:] == ["and eax, 0x3ff", "xor eax, r8d", "ret"] and RNG not in seen,
      "draws at %s; NextU32 steps the LCG %d times and stores once, result < 2^31; point-path closure (%d functions) draws nothing"
      % (["%08X" % a for a in rc], sum("0x41c64e6d" in s for s in rb), len(seen)))
# P7 arcDeg is global state
ARC = rip(next(x for x in pb if x.address == 0x00234B27))[0]
acc7 = sorted(("%08X" % f, S(x)) for f, x in refs[ARC])
check("P7", ARC == 0x02089358 and [f for f, _s in acc7] == ["00234AF0", "0023A1F0", "0023A520"] and N("Spawn_SetCandidateHeadingArcDegrees") == 0x0023A1F0
      and ("0023A520", "mov dword ptr [rip + 0x1e4edfe], 0xb4") in acc7,
      "arcDeg cell %08X: %s; its setter is called from %s" % (ARC, acc7, sorted({"%08X" % f for f, _a, _m in calls_to[0x0023A1F0]})))
# P8 I7 / I8: the polar writer and the unwritten Y
pol = bodies[0x00319390]
pw = [S(x) for x in pol if is_write(x) and "rsp" not in x.op_str.split(",")[0]]
tab = [S(x) for x in pol if 0x01F004E0 in rip(x)]
ps = [S(x) for x in pol]
yw = [S(x) for x in pb if is_write(x) and x.operands[0].mem.base == X86_REG_RSP and 0x50 <= x.operands[0].mem.disp <= 0x5B]
check("P8", sorted(w.split(", ")[0] for w in pw) == ["movss dword ptr [rdx + 8]", "movss dword ptr [rdx]"],
      "00319390 writes %s; table refs %d; & 0x7fff %s; 0x2000 %s; 00234AF0 writes into rsp+0x50..0x5B: %s; result.y from %s"
      % (pw, len(tab), any("0x7fff" in s for s in ps), any("0x2000" in s for s in ps), yw or "none", at(PLACE, 0x00234CDD)))
check("P8b", (tab or any(0x01F004E0 in rip(x) for f in (0x00319390,) for x in bodies[f])) and not yw and at(PLACE, 0x00234CDD) == "movss xmm1, dword ptr [rsp + 0x54]",
      "the sine table is 01F004E0 and Y is never written before it is copied")
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
