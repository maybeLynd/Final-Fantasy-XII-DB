"""Falsification pass 1 on CONTRACT-authored-expression-evaluation (OPUS, 2026-09-29), from the shipping image. Killers first.

  A0  section 2: 00431350 is 190 B and is tail-jumped from 004314E0; f 003A6E60 is 345 B and calls nothing; 00431080 is
      718 B; 0020E600 is 10 B
  A1  I1: kind A 0 -> 0, 1 -> resolve the payload and read [target + 4], >= 2 -> 00431080 with index 0; kind B 0 -> return A
      without the combiner; kind B 1 -> [target + 4]; >= 2 -> 00431080 with index 1
  A2  I2 for b != 0: op = (word [rec + 0xE] >> 4) & 0xF, op > 5 returns a; the table sends 0 -> return a, 1 -> a + f(b),
      2 -> a - f(b), 3 -> a - b + f(2b), 4 -> a * (f(b) + 1), 5 -> b == a ? a : a + f(b - a)
  A3  (REFUTES I2's draw column, which gives ops 1-4 one draw unconditionally) the combiner tests b first
      (`test r8d, r8d / je 004313E9`): with b == 0 every op but 5 returns a WITHOUT calling f, and op 5 draws f(-a) when
      a != 0. The page (how-an-authored-number-gets-its-randomness.md) states this; the contract dropped it
  A4  I4 in context: the combiner's f calls take b (ops 1, 2, 4), 2b (op 3) or b - a (op 5 and the zero-b path), each
      only after b != 0 or b - a != 0 was established, so f(0) is reachable from here only through op 3 with
      b = 0x80000000 (2b wraps to 0)
  A5  I3 / I4 / I6: f runs the RNEXT-style step (`shr 0x12 / xor / and 0x3fffff / or 0x1fc00000`) five times, stores,
      then twice more and stores; both step blocks are gated on the mode word 022D9138; P = v * B, then B * [01EF93FC]
      (vf00.w, 1.0; its two writers, the bank's start-up 0036D990 and clear
      0036D9E0, store the .rdata 1.0 at 01CEBBA8), then P - that, in that order
  A6  section 5: the six writes in order - 01EF93E8, 022D91A0 (ACC.x), 022D92E0 (vf20.x), 01EF93E8, 022D92F0 (vf21.x),
      022D92E0 (vf20, all four lanes, after cvttps2dq)
  A7  section 3: the operator is loaded as a u16 at +0x0E, so the path reads sixteen bytes; the operator's bits 4-7 lie in
      the byte at +0x0E, so fifteen of them matter
"""
import collections, io, os, struct
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
            sizes[int(p[0], 16)] = int(p[2]); names[p[1]] = int(p[0], 16)
        except ValueError:
            pass
S = lambda x: ("%s %s" % (x.mnemonic, x.op_str)).strip()
rip = lambda x: [x.address + x.size + o.mem.disp for o in x.operands if o.type == X86_OP_MEM and o.mem.base == X86_REG_RIP]
T = lambda x: x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None
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
    return bool(x.operands) and x.operands[0].type == X86_OP_MEM and x.mnemonic in ("mov", "movss", "movups", "movaps", "movdqu", "movdqa", "inc", "add", "sub", "or", "and", "xor")


def at(fa, va):
    return next(S(x) for x in bodies[fa] if x.address == va)


def run(fa, lo, hi):
    return [S(x) for x in bodies[fa] if lo <= x.address <= hi]


EVAL, COMB, F, CURVE, FIX = 0x004314E0, 0x00431350, 0x003A6E60, 0x00431080, 0x0020E600

# A0
fcalls = [S(x) for x in bodies[F] if x.mnemonic == "call"]
tail = [(f, a, m) for f, a, m in calls_to[COMB] if f == EVAL]
check("A0", sizes.get(COMB) == 190 and sizes.get(F) == 345 and not fcalls and sizes.get(CURVE) == 718 and sizes.get(FIX) == 10
      and tail == [(EVAL, 0x0043156E, "jmp")], "sizes %s; f calls %s; 004314E0 -> 00431350 %s"
      % ([sizes.get(x) for x in (COMB, F, CURVE, FIX)], fcalls or "nothing", [("%08X" % a, m) for _f, a, m in tail]))
# A1
check("A1", run(EVAL, 0x004314EF, 0x004314EF) == ["movzx eax, byte ptr [rcx + 0xc]"] and run(EVAL, 0x004314FC, 0x004314FC) == ["xor edi, edi"]
      and run(EVAL, 0x00431505, 0x0043150C) == ["mov ecx, dword ptr [rcx]", "call 0x20e600", "mov edi, dword ptr [rax + 4]"]
      and run(EVAL, 0x00431511, 0x00431514) == ["xor r8d, r8d", "call 0x431080"]
      and run(EVAL, 0x0043151B, 0x00431523) == ["movzx eax, byte ptr [rbx + 0xd]", "test eax, eax", "jne 0x431535", "mov eax, edi"]
      and run(EVAL, 0x0043153A, 0x00431542) == ["mov ecx, dword ptr [rbx + 4]", "call 0x20e600", "mov eax, dword ptr [rax + 4]"]
      and at(EVAL, 0x00431547) == "mov r8d, 1",
      "kind A at +0x0C, kind B at +0x0D; kind 1 reads [target + 4]; curve index 0 / 1; B absent returns A")
# A2 the dispatch for b != 0
jt = [BASE + struct.unpack("<I", blob[OFF(0x00431410 + 4 * k):OFF(0x00431410 + 4 * k) + 4])[0] for k in range(6)]
arms = {1: run(COMB, 0x00431390, 0x00431397), 2: run(COMB, 0x004313A4, 0x004313AD), 3: run(COMB, 0x004313BA, 0x004313C5),
        4: run(COMB, 0x004313D2, 0x004313DB), 5: run(COMB, 0x004313FD, 0x004313FF)}
check("A2", run(COMB, 0x00431368, 0x00431375) == ["movzx eax, word ptr [rcx + 0xe]", "shr eax, 4", "and eax, 0xf", "cmp eax, 5", "ja 0x431401"]
      and jt == [0x00431401, 0x00431390, 0x004313A4, 0x004313BA, 0x004313D2, 0x004313FD]
      and arms[1] == ["mov ecx, edi", "call 0x3a6e60", "add eax, ebx"] and arms[2] == ["mov ecx, edi", "call 0x3a6e60", "sub ebx, eax", "mov eax, ebx"]
      and arms[3] == ["lea ecx, [r8 + r8]", "call 0x3a6e60", "sub ebx, edi", "add eax, ebx"] and arms[4] == ["mov ecx, edi", "call 0x3a6e60", "inc eax", "imul eax, ebx"]
      and arms[5] == ["sub edi, ebx", "jne 0x431390"] and at(COMB, 0x00431401) == "mov eax, ebx",
      "table %s" % ["%08X" % v for v in jt])
# A3 (REFUTES the unconditional draw column): the zero-b path
zb = run(COMB, 0x004313E9, 0x004313FF)
check("A3", run(COMB, 0x0043135F, 0x00431362) == ["test r8d, r8d", "je 0x4313e9"]
      and zb == ["movzx ecx, word ptr [rcx + 0xe]", "shr ecx, 4", "and ecx, 0xf", "sub ecx, 4", "je 0x431401", "cmp ecx, 1", "jne 0x431401",
                 "sub edi, ebx", "jne 0x431390"]
      and not [x for x in bodies[COMB] if 0x004313E9 <= x.address <= 0x004313FF and x.mnemonic == "call"],
      "b == 0 -> 004313E9: op 4 and every op but 5 return a without calling f; op 5 computes 0 - a and draws only if it is non-zero")
# A4 f(0) from the combiner
fc = [(x.address, run(COMB, x.address - 4, x.address - 1)) for x in bodies[COMB] if S(x) == "call 0x3a6e60"]
check("A4", [a for a, _p in fc] == [0x00431392, 0x004313A6, 0x004313BE, 0x004313D4] and "lea ecx, [r8 + r8]" in fc[2][1],
      "f is called at %s; the op-3 bound is 2b (wraps to 0 only at b = 0x80000000); every other bound is b != 0 or b - a != 0"
      % ["%08X" % a for a, _p in fc])
# A5 the step, the gate, the arithmetic order
fb = [S(x) for x in bodies[F]]
steps = sum(1 for s in fb if s.endswith("0x1fc00000"))
first_store = next(i for i, x in enumerate(bodies[F]) if S(x).startswith("mov dword ptr [rip") and rip(x) == [0x01EF93E8])
pre = sum(1 for s in fb[:first_store] if s.endswith("0x1fc00000"))
gates = [S(x) for x in bodies[F] if S(x) == "test r8d, r8d"]
mode = rip(bodies[F][0])
one = [x for x in bodies[F] if x.mnemonic == "mulss" and rip(x)]
vf00w = rip(one[0])[0] if one else None
# vf00.w's writers are the bank's start-up 0036D990 and clear 0036D9E0; each stores the .rdata 1.0 at 01CEBBA8
vfw = sorted({f for f, x in refs[0x01EF93FC] if is_write(x)})
def stores_one(f):
    b = bodies[f]; k = next(i for i, x in enumerate(b) if 0x01EF93FC in rip(x) and is_write(x))
    src = b[k].op_str.split(", ")[-1]
    return any(y.mnemonic == "movss" and y.op_str.startswith(src + ",") and rip(y) == [0x01CEBBA8] for y in b[max(0, k - 4):k])
vf_ok = vfw == [0x0036D990, 0x0036D9E0] and all(stores_one(f) for f in vfw) and struct.unpack("<f", blob[OFF(0x01CEBBA8):OFF(0x01CEBBA8) + 4])[0] == 1.0
check("A5", steps == 7 and pre == 5 and len(gates) == 2 and mode == [0x022D9138] and vf00w == 0x01EF93FC
      and struct.unpack("<f", blob[OFF(0x01EF93FC):OFF(0x01EF93FC) + 4])[0] == 1.0 and vf_ok
      and run(F, 0x003A6F2D, 0x003A6F41) == ["mulss xmm1, xmm0", "mulss xmm0, dword ptr [rip + 0x1b524c3]", "movss dword ptr [rip + 0x1f3225f], xmm1", "subss xmm1, xmm0"],
      "%d steps, %d before the first store; %d mode gates on %s; B x [%08X] (vf00.w = 1.0; writers 0036D990/0036D9E0 store .rdata 1.0); P = v*B, then B*1, then P - B*1"
      % (steps, pre, len(gates), ["%08X" % m for m in mode], vf00w or 0))
# A6 the six writes, in order
ws = [("%08X" % rip(x)[0], x.mnemonic) for x in bodies[F] if is_write(x) and rip(x)]
check("A6", ws == [("01EF93E8", "mov"), ("022D91A0", "movss"), ("022D92E0", "movss"), ("01EF93E8", "mov"), ("022D92F0", "movss"), ("022D92E0", "movups")],
      "%s" % ws)
# A7 the record bytes read
recops = sorted({(o.mem.disp, o.size) for fa in (EVAL, COMB) for x in bodies[fa] for o in x.operands
                 if o.type == X86_OP_MEM and o.mem.base != X86_REG_RIP and x.reg_name(o.mem.base) in ("rcx", "rbx") and o.mem.disp < 0x10})
last = max(d + s for d, s in recops)
check("A7", last == 0x10 and (0x0E, 2) in recops, "record operands (disp, size) %s: bytes 0x00..0x%02X are loaded" % (recops, last - 1))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
