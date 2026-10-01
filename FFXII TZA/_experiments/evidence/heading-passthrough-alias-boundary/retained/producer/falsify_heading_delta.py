"""Falsification pass 1 on CONTRACT-heading-speed-to-position-delta (OPUS, 2026-09-29), from the shipping image. Killers first.

  H0  section 2 / LD-1: 002E4380 is 601 B and 00265020 61 B; the class-3 gate (`and al, 0xe0` / `cmp al, 0x60`) appears once
      in Movement_SetRequestedSpeed, once in Actor_SetDesiredMovementHeading, twice in Movement_UpdateActorFrame and once here
  H1  LD-2: 00265020 null-checks, then `shr 5 / sub 1 / je / cmp 2 / jne` - classes 1 and 3 - and a refusal zeros all three outputs
  H2  LD-3 / LD-5: X, Y, Z are zeroed (qword + dword) before the gate; the refusal exit 002E45C9 writes W = 1.0 only
  H3  (REFUTES section 5 "Written: only the caller's output vector") the body writes the movement block's +0xF8 on two paths:
      the pass-through stores sqrtf(|v|^2) at 002E43E6, and the decomposition path repairs a negative +0xF8 to the speed at
      002E445C
  H4  (section 7 omits it) after the wrap, when [actor + 0xC0] is non-null and its first dword is not -1, 00424080 gets the
      wrapped yaw and the speed by address (002E4510) before the speed-0 test and the decomposition
  H5  LD-4: the flat branch is 00267260 != 0 && 00264460 == 0, which leaves Y = 0 and X / Z unscaled by cos(pitch)
  H6  LD-6: both angles take the truncating wrap (`cvttss2si` over 2pi, add and subtract +-pi) at 002E4464..002E44EF
  H7  section 9: the call closure of 002E4380 reaches no generator entry and no reference to the gameplay LCG cell
"""
import collections, io, os
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
refs = collections.defaultdict(list)
bodies = {}
for fa in sorted(sizes):
    if not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        code = blob[OFF(fa):OFF(fa) + sizes[fa]]
    except ValueError:
        continue
    bodies[fa] = list(md.disasm(code, fa))
    for x in bodies[fa]:
        for t in rip(x):
            refs[t].append((fa, x))


def run(fa, lo, hi):
    return [S(x) for x in bodies[fa] if lo <= x.address <= hi]


D, P = 0x002E4380, 0x00265020
dt = [S(x) for x in bodies[D]]
# H0
gates = {}
for n in ("Movement_SetRequestedSpeed", "Actor_SetDesiredMovementHeading", "Movement_UpdateActorFrame", "Movement_ComputeDeltaFromHeadingSpeed"):
    b = bodies[names[n]]
    gates[n] = sum(1 for i, x in enumerate(b) if x.mnemonic == "and" and S(x).endswith(", 0xe0")
                   and any(y.mnemonic == "cmp" and S(y).endswith(", 0x60") for y in b[i + 1:i + 6]))
check("H0", sizes[D] == 601 and sizes[P] == 61 and list(gates.values()) == [1, 1, 2, 1], "sizes %d / %d; gates %s" % (sizes[D], sizes[P], gates))
# H1
check("H1", [S(x) for x in bodies[P]][:8] == ["test rcx, rcx", "je 0x265052", "movzx r10d, byte ptr [rcx + 3]", "shr r10d, 5", "sub r10d, 1", "je 0x26503a",
                                              "cmp r10d, 2", "jne 0x265052"]
      and run(P, 0x00265052, 0x00265059) == ["xor eax, eax", "mov dword ptr [rdx], eax", "mov dword ptr [r8], eax", "mov dword ptr [r9], eax"],
      "null first; classes 1 and 3; refusal zeros x, y, z")
# H2
check("H2", run(D, 0x002E438E, 0x002E4394) == ["mov qword ptr [rdx], rax", "mov rbx, rdx", "mov dword ptr [rdx + 8], eax"]
      and run(D, 0x002E439A, 0x002E43A2) == ["movzx eax, byte ptr [rcx + 3]", "and al, 0xe0", "cmp al, 0x60", "jne 0x2e45c9"]
      and run(D, 0x002E45C9, 0x002E45C9) == ["mov dword ptr [rdx + 0xc], 0x3f800000"],
      "X/Y/Z zeroed before the gate; refusal writes W = 1.0 and returns")
# H3 (REFUTES section 5)
w8 = [(("%08X" % x.address), S(x)) for x in bodies[D] if x.mnemonic.startswith("mov") and x.operands[0].type == X86_OP_MEM and "[rdi + 0xf8]" in x.op_str.split(",")[0]]
check("H3", w8 == [("002E43E6", "movss dword ptr [rdi + 0xf8], xmm0"), ("002E445C", "movss dword ptr [rdi + 0xf8], xmm3")]
      and run(D, 0x002E43B0, 0x002E43B0) == ["mov rdi, qword ptr [rcx + 0xb8]"] and "call 0x3a1d30" in run(D, 0x002E43E1, 0x002E43E1)
      and run(D, 0x002E443E, 0x002E445A)[0] == "comiss xmm7, dword ptr [rdi + 0xf8]",
      "writes to the movement block (actor+0xB8)+0xF8: %s" % w8)
# H4
check("H4", run(D, 0x002E44D6, 0x002E44D6) == ["mov rax, qword ptr [rcx + 0xc0]"] and run(D, 0x002E44F3, 0x002E4510) == [
          "test rax, rax", "je 0x2e451e", "cmp dword ptr [rax], -1", "je 0x2e451e", "movzx ecx, word ptr [rax]", "lea r8, [rsp + 0x80]", "lea rdx, [rsp + 0x88]", "call 0x424080"]
      and run(D, 0x002E451E, 0x002E4523) == ["ucomiss xmm3, xmm7", "jp 0x2e4525", "je 0x2e45a1"],
      "00424080(word [actor+0xC0], &yaw, &speed) runs after the wrap and before the speed-0 test")
# H5
check("H5", run(D, 0x002E4525, 0x002E4547) == ["mov rcx, rsi", "call 0x267260", "test eax, eax", "je 0x2e4549", "mov rcx, rsi", "call 0x264460", "test eax, eax",
                                               "jne 0x2e4549", "movss xmm8, dword ptr [rsp + 0x80]", "jmp 0x2e4570"],
      "flat branch when 00267260 != 0 and 00264460 == 0: Y stays 0, X/Z use speed unscaled")
# H6
wr = run(D, 0x002E4464, 0x002E44EF)
check("H6", wr.count("cvttss2si eax, xmm0") == 2 and wr.count("mulss xmm1, xmm9") == 2 and "subss xmm2, xmm5" in wr and "subss xmm6, xmm4" in wr,
      "two truncating wraps (yaw with xmm5, pitch with xmm4 = +-pi)")
# H7
seen, st = set(), [D]
while st:
    f = st.pop()
    if f in seen or f not in bodies:
        continue
    seen.add(f)
    for x in bodies[f]:
        t = T(x) if x.mnemonic in ("call", "jmp") else None
        if t is not None and t in bodies and not (f <= t < f + sizes[f]):
            st.append(t)
GEN = [0x00328370, 0x00379CD0, 0x00863BF0, 0x00863D30, 0x0018EE20, 0x0018D740, 0x003A6E60]
check("H7", not [g for g in GEN if g in seen] and not [f for f, _x in refs[0x022C256C] if f in seen],
      "closure %d bodies; no generator entry, no gameplay-LCG reference" % len(seen))
print("FAILS %d" % fails)
