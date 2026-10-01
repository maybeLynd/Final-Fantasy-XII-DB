"""Falsification pass 1 on CONTRACT-loot-rolls-and-the-chain (OPUS, 2026-09-29), from the shipping image.
Each row states what the bytes show; a row marked REFUTES is a clause of the page they break. Censuses run bounded by the
function list AND as a linear sweep of .text (every 4-byte window whose rip target is the state, confirmed by decoding).

  L1  LC-1: 022C256C has 17 rip-relative accesses on both instruments (linear-only 0), 9 writers and 8 readers; the accessing
      functions are 00328370, its setter, and the seven inliners 00317ED0, 003183D0, 00318510, 003185D0, 003186F0, 00318820,
      00319530; 00328370 has 23 direct call sites in 15 functions, none of them one of the seven
  L2  LC-2: 00318540..0031858B and 00328370..003283B9 are the same sequence (mnemonics and operands, each rip displacement
      resolved to its target) except ONE register copy, `mov ecx, eax` at 00318589, which the inline keeps for its own result
      composition; the three multiply-adds, the composition and the single writeback are identical
  L3  LC-3: three `imul .., 0x41c64e6d` and three `add .., 0x3039` per draw, one store; 00318594 `mov eax, 0x51eb851f`, 003185A4 `sar edx, 5`
  L4  LC-4's guards: 0031815C `cmp [022C3164], r14d` / jle; 003181F8 `cmp word ptr [rsi], r13w` / je; 0031820A jne / 00318213 jne;
      00318521, 0031852A, 0031853A each `je 0x3185c0` before the draw at 00318540; the chance, quantity and profile rolls draw
      unconditionally on entry (their first imul precedes every branch)
  K1  (REFUTES LC-4's and section 2's "between 2 and 13 draws" and section 12's "at most once") the orchestrator's draws are
      P + C + Q + E: P = 1 only when [022C3164] > 0, C = one per slot whose id is not 0xFFFF, Q = one per kept slot, E = 0..2.
      Every term can be 0, so the floor is 0, not 2. And an EMPTY slot is not skipped: 003181FC sends it to the +0xE64
      override at 0031820C, and a matching index keeps it (00318215 stores 0xFFFF) and draws a quantity (00318220) - so an
      all-empty kill with both extras disabled can draw twice (profile + one override quantity), not "at most once"
  L5  LC-5: 00319530 has one call site, 00311146 in BattleUnit_RunPeriodicCombatMaintenance; 00311130 tests stats +5 and 00311136
      branches past the call
  L6  LC-6: 00318116 loads 022C3158 into r12d; only 0031816A overwrites r12d, after the 00318820 call that 0031815C guards;
      0017D340 is 20 B and returns dword [001D50D0() + 0xE64]
  L7  LC-7: fourteen pre-fill stores 0031811D..00318158 (seven 0xFFFF words, seven zero dwords) precede the first roll;
      00318225 `inc eax` after the quantity call
  L8  section 10 / section 2: 00318174 `test rdx, rdx` / 00318177 je to a zero slot count; the orchestrator is 641 B
"""
import collections, io, os, struct
from array import array
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


sizes, names = {}, {}
for i, line in enumerate(io.open(FUNCS, encoding="utf-8", errors="replace")):
    p = line.rstrip("\n").split("\t")
    if i and len(p) > 2:
        try:
            sizes[int(p[0], 16)] = int(p[2]); names[int(p[0], 16)] = p[1]
        except ValueError:
            pass
S = lambda x: ("%s %s" % (x.mnemonic, x.op_str)).strip()
rip = lambda x: [x.address + x.size + o.mem.disp for o in x.operands if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP]
body = lambda fa: {x.address: x for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa)}
at = lambda I, a: S(I[a]) if a in I else "?"
imm = lambda x: x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None
is_w = lambda x: bool(x.operands) and x.operands[0].type == X86_OP_MEM and x.mnemonic in ("mov", "add", "sub", "and", "or", "xor", "inc", "dec")
LCG, GEN = 0x022C256C, 0x00328370
SEVEN = [0x00317ED0, 0x003183D0, 0x00318510, 0x003185D0, 0x003186F0, 0x00318820, 0x00319530]
text = next(x for x in SECS if x[0] == ".text")

bounded, gcalls, fn_of = {}, [], {}
for fa in sorted(sizes):
    if not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa):
            if LCG in rip(x):
                bounded[x.address] = x; fn_of[x.address] = fa
            if x.mnemonic == "call" and imm(x) == GEN:
                gcalls.append((x.address, fa))
    except ValueError:
        continue
raw = blob[text[3]:text[3] + text[4]]
want = {LCG - t for t in (0, 1, 2, 4)}
cands = set()
for s in range(4):
    a = array("i"); n = (len(raw) - s) // 4; a.frombytes(raw[s:s + 4 * n])
    base = text[1] + s + 4
    for k, d in enumerate(a):
        if base + 4 * k + d in want:
            cands.add(text[1] + s + 4 * k)
linear = {}
for pos in cands:
    for L in range(1, 12):
        st = pos - L
        x = next(md.disasm(blob[OFF(st):OFF(st) + 16], st), None)
        if x and st < pos < x.address + x.size and LCG in rip(x):
            linear[x.address] = x; break
wr = [a for a, x in linear.items() if is_w(x)]
fns = sorted({fn_of[a] for a in bounded})
gfun = {f for _a, f in gcalls}
check("L1", len(linear) == 17 and set(linear) == set(bounded) and len(wr) == 9 and len(linear) - len(wr) == 8
      and set(SEVEN) <= set(fns) and GEN in fns and len(fns) == 9 and len(gcalls) == 23 and len(gfun) == 15 and not (gfun & set(SEVEN)),
      "%d accesses (bounded %d, linear-only %d), %d writers; functions %s; generator: %d call sites in %d functions, overlap with the seven %d"
      % (len(linear), len(bounded), len(set(linear) - set(bounded)), len(wr), ["%08X" % f for f in fns], len(gcalls), len(gfun), len(gfun & set(SEVEN))))


def norm(x):
    r = rip(x)
    return (x.mnemonic, x.op_str if not r else x.op_str.split("[")[0] + "[%08X]" % r[0] + x.op_str.split("]")[-1])


AI = list(md.disasm(blob[OFF(0x00318540):OFF(0x0031858B) + 6], 0x00318540))
extra = [S(x) for x in AI if x.address == 0x00318589]
A = [norm(x) for x in AI if x.address != 0x00318589]
G = [norm(x) for x in md.disasm(blob[OFF(0x00328370):OFF(0x003283B9) + 6], 0x00328370)]
check("L2", A == G and extra == ["mov ecx, eax"], "%d instructions identical after resolving rip targets; the one extra in the inline copy: %s" % (len(A), extra)
      if A == G else "differ: %s" % [(a, g) for a, g in zip(A, G) if a != g][:3])
R = body(0x00318510)
nimul = sum(1 for x in md.disasm(blob[OFF(0x00318540):OFF(0x0031858B) + 6], 0x00318540) if x.mnemonic == "imul" and "0x41c64e6d" in x.op_str)
nadd = sum(1 for x in md.disasm(blob[OFF(0x00318540):OFF(0x0031858B) + 6], 0x00318540) if x.mnemonic == "add" and "0x3039" in x.op_str)
check("L3", nimul == 3 and nadd == 3 and at(R, 0x00318594) == "mov eax, 0x51eb851f" and at(R, 0x003185A4) == "sar edx, 5",
      "%d imul / %d add per draw; %% 100 via %s, %s" % (nimul, nadd, at(R, 0x00318594), at(R, 0x003185A4)))
O = body(0x003180F0); X = body(0x00318510)


def draws_first(fa):
    ins = sorted(body(fa).items())
    first_draw = next(a for a, x in ins if x.mnemonic == "imul" and "0x41c64e6d" in x.op_str)
    return not any(x.mnemonic.startswith("j") for a, x in ins if a < first_draw), first_draw


df = {f: draws_first(f) for f in (0x003185D0, 0x003186F0, 0x00318820)}
check("L4", at(O, 0x0031815C) == "cmp dword ptr [rip + 0x1fab001], r14d" and rip(O[0x0031815C]) == [0x022C3164] and at(O, 0x00318163) == "jle 0x31816d"
      and at(O, 0x003181F8) == "cmp word ptr [rsi], r13w" and at(O, 0x0031820A) == "jne 0x318215" and at(O, 0x00318213) == "jne 0x31822b"
      and all(at(X, a) == "je 0x3185c0" for a in (0x00318521, 0x0031852A, 0x0031853A)) and all(v[0] for v in df.values()),
      "guards read; chance / quantity / profile rolls draw before any branch: %s" % {("%08X" % f): ("%08X" % v[1]) for f, v in df.items()})
check("K1", at(O, 0x003181FC) == "je 0x31820c" and at(O, 0x0031820C) == "call 0x17d340" and at(O, 0x00318211) == "cmp eax, edi"
      and at(O, 0x00318215) == "movzx eax, word ptr [rsi]" and at(O, 0x0031821C) == "mov word ptr [r14], ax" and at(O, 0x00318220) == "call 0x3186f0"
      and at(O, 0x003181E9) == "mov r13d, 0xffff",
      "(REFUTES 'between 2 and 13' and 'at most once') draws = P + C + Q + E, each able to be 0, floor 0; an empty slot "
      "(%s) goes to the override (%s / %s), and a match stores id 0xFFFF and draws a quantity (%s)"
      % (at(O, 0x003181FC), at(O, 0x0031820C), at(O, 0x00318211), at(O, 0x00318220)))
M = body(0x00311070) if 0x00311070 in sizes else None
site = [(a, f) for f in sorted(sizes) if text[1] <= f < text[1] + text[2] for a, x in [] ]
c19 = []
for fa in sorted(sizes):
    if not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa):
            if x.mnemonic in ("call", "jmp") and imm(x) == 0x00319530:
                c19.append((x.address, fa))
    except ValueError:
        continue
mf = c19[0][1] if c19 else None
MI = body(mf) if mf else {}
check("L5", c19 and [a for a, _ in c19] == [0x00311146] and names.get(mf) == "BattleUnit_RunPeriodicCombatMaintenance"
      and "+ 5]" in at(MI, 0x00311130) and MI[0x00311136].mnemonic.startswith("j") and imm(MI[0x00311136]) > 0x00311146,
      "call sites %s in %s; %s / %s" % (["%08X" % a for a, _ in c19], names.get(mf), at(MI, 0x00311130), at(MI, 0x00311136)))
w12 = [a for a, x in O.items() if x.operands and x.operands[0].type == 1 and x.reg_name(x.operands[0].reg) == "r12d" and x.mnemonic.startswith("mov")]
Z = body(0x0017D340)
check("L6", rip(O[0x00318116]) == [0x022C3158] and at(O, 0x00318116).startswith("mov r12d, dword ptr [rip") and sorted(w12) == [0x00318116, 0x0031816A]
      and at(O, 0x00318165) == "call 0x318820" and sizes[0x0017D340] == 20 and at(Z, 0x0017D344) == "call 0x1d50d0" and at(Z, 0x0017D349) == "mov eax, dword ptr [rax + 0xe64]",
      "r12d written at %s; accessor %s / %s" % (["%08X" % a for a in sorted(w12)], at(Z, 0x0017D344), at(Z, 0x0017D349)))
pre = [S(O[a]) for a in sorted(O) if 0x00318122 <= a <= 0x00318158 and O[a].mnemonic == "mov" and O[a].operands[0].type == X86_OP_MEM]
check("L7", len(pre) == 14 and sum(1 for p in pre if p.endswith(", ax")) == 7 and sum(1 for p in pre if p.endswith(", r14d")) == 7
      and at(O, 0x0031811D) == "mov eax, 0xffff" and at(O, 0x00318225) == "inc eax", "%d pre-fill stores; %s" % (len(pre), at(O, 0x00318225)))
check("L8", at(O, 0x00318174) == "test rdx, rdx" and at(O, 0x00318177) == "je 0x31817e" and at(O, 0x0031817E) == "mov esi, r14d" and sizes[0x003180F0] == 641,
      "%s / %s -> %s; 641 B" % (at(O, 0x00318174), at(O, 0x00318177), at(O, 0x0031817E)))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
