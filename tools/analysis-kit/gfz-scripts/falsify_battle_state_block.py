"""Falsification pass 1 on CONTRACT-battle-state-block (OPUS, 2026-09-29), from the shipping image.
Each row states what the bytes show; a row marked REFUTES is a clause of the page they break.

  K1  section 2 / BS-2 / BS-3 treat the binder's reset as 002370C0. The binder 00233C10 branches to one reset body only,
      BattleSystem_ResetRuntimeState 00237DF0 (00233C3F call, 00233C48 jmp, 00233C59 jmp) and never to 002370C0; 00237DF0's
      first call is 0023AF50, whose first call is 002370C0; 00237DF0 then calls BattleSlotMap_InitializeMappingClasses
      00329CC0 at 00237E41, and its only conditional branch is the record loop's `jl` at 00237E30
  K2  BS-5 / sections 10, 11, 16: after a reset maps 1-4 are zero and a class-1-to-4 lookup answers 0. On every binder path
      the reset returns only after 00329CC0 has copied map 0 into maps 1-4, so the zeroed maps never survive a binder reset.
      They survive only where 002370C0 is called directly: its other caller is 00239960 (at 002399E9), whose direct arm
      reaches neither 00329CC0, the refresher 003266C0 nor 00237DF0 through direct calls and jumps to depth 8
      (indirect calls are not followed)
  K3  BS-3: "the second invocation takes a block whose magic is already correct - the two resets are not two identical
      operations against the same input". Nothing reads the block before the memset: 00237DF0 and 0023AF50 each make their
      first call before any memory read, and 002370C0 memsets before reading it. The block's prior contents, magic included,
      cannot change what the block becomes
  B1  BS-1: 00233C25 calls SaveImage_GetActiveRuntimeBuffer (002EF640), 00233C2A adds 0x4E68C, 00233C33 stores 02EBF190
  B2  BS-2's arms: 00233C20 test / 00233C23 jne; 00233C4D cmp dword [rax], 0x5071901 then 00233C53 `je 0x233c5e`, the wrong
      magic being the FALL-THROUGH to 00233C59 (the page's table says `jne`); two invocations on the unbound arm, one on a
      wrong magic, none on a right one
  B3  BS-3's bytes: 002370CD `mov r8d, 0x7410`, 002370D3 the memset call, 002370DF `mov dword ptr [rax], 0x5071901`
  B4  BS-5's loop: starts at 0x5A48 (002370EA), stores 0xFFFF words (00237107), bound `cmp rcx, 0x5a5a` (0023710F)
  B5  section 3: 002370C0 zeroes +0x5ACC and +0x5AC8; sizes 214 B and 121 B
"""
import bisect, collections, io, os
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_MEM

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
starts = sorted(sizes)
S = lambda x: ("%s %s" % (x.mnemonic, x.op_str)).strip()
body = lambda fa: list(md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa))
br = lambda x: x.operands[0].imm if (x.mnemonic == "call" or x.mnemonic.startswith("j")) and x.operands and x.operands[0].type == X86_OP_IMM else None


def owner(va):
    k = bisect.bisect_right(starts, va) - 1
    return starts[k] if k >= 0 and va < starts[k] + sizes[starts[k]] else None


def reads_mem_before_first_call(ins):
    for x in ins:
        if x.mnemonic == "call":
            return False
        if any(o.type == X86_OP_MEM and x.reg_name(o.mem.base) not in ("rsp",) for o in x.operands) and x.mnemonic != "lea":
            return True
    return False


B = body(0x00233C10); BI = {x.address: x for x in B}
RST = 0x00237DF0
bt = sorted({br(x) for x in B if br(x) in (RST, 0x002370C0)})
R = body(RST); calls_R = [(x.address, br(x)) for x in R if x.mnemonic == "call"]
A = body(0x0023AF50); first_A = next(br(x) for x in A if x.mnemonic == "call")
cond = [(x.address, x.mnemonic) for x in R if x.mnemonic.startswith("j") and x.mnemonic != "jmp"]
check("K1", bt == [RST] and [(x.address, br(x)) for x in B if br(x) == RST] == [(0x00233C3F, RST), (0x00233C48, RST), (0x00233C59, RST)]
      and calls_R[0][1] == 0x0023AF50 and first_A == 0x002370C0 and (0x00237E41, 0x00329CC0) in calls_R and cond == [(0x00237E30, "jl")],
      "(REFUTES 'the reset' = 002370C0 on the binder's paths) binder reaches %s at %s; 00237DF0's first call %08X, whose first call %08X; "
      "00329CC0 called at 00237E41: %s; conditional branches in 00237DF0 %s"
      % (["%08X" % t for t in bt], ["%08X" % x.address for x in B if br(x) == RST], calls_R[0][1], first_A, (0x00237E41, 0x00329CC0) in calls_R, ["%08X %s" % c for c in cond]))

callers = []
for fa in starts:
    try:
        for x in body(fa):
            if br(x) == 0x002370C0:
                callers.append((x.address, fa))
    except ValueError:
        continue


def succ(fa):
    out = set()
    for x in body(fa):
        t = br(x)
        if t is not None and x.mnemonic in ("call", "jmp") and not (fa <= t < fa + sizes[fa]):
            o = owner(t)
            if o:
                out.add(o)
    return out


GOAL = {0x00329CC0, 0x003266C0, RST}
first = succ(0x00239960) - {RST}          # the direct arm: everything but the tail-jump 0023998E
seen, q, hit = {}, collections.deque((f, 1) for f in first), []
while q:
    f, d = q.popleft()
    if f in seen:
        continue
    seen[f] = d
    if f in GOAL:
        hit.append("%08X" % f); continue
    if d < 8:
        q.extend((g, d + 1) for g in succ(f))
tail = [x.address for x in body(0x00239960) if br(x) == RST and x.mnemonic == "jmp"]
check("K2", sorted(callers) == [(0x002399E9, 0x00239960), (0x0023AF56, 0x0023AF50)] and tail == [0x0023998E] and not hit,
      "(REFUTES 'after a reset maps 1-4 are zero' for the binder's reset) 002370C0's callers %s; 00239960 tail-jumps to the full reset at %s; "
      "its direct arm reaches %d functions to depth 8 and none of 00329CC0 / 003266C0 / 00237DF0: %s"
      % (["%08X in %08X" % c for c in sorted(callers)], ["%08X" % a for a in tail], len(seen), hit or "none"))

Z = body(0x002370C0); ZI = {x.address: x for x in Z}
check("K3", not reads_mem_before_first_call(R) and not reads_mem_before_first_call(A)
      and [S(x) for x in Z if x.address < 0x002370D8] == ["sub rsp, 0x28", "mov rcx, qword ptr [rip + 0x2c880c5]", "xor edx, edx", "mov r8d, 0x7410", "call 0x861ec0"],
      "(REFUTES 'not two identical operations against the same input' for the block) 00237DF0 and 0023AF50 read no memory before their "
      "first call, and 002370C0 loads only the block pointer before the memset")

at = lambda a: S(BI[a]) if a in BI else "?"
check("B1", at(0x00233C25) == "call 0x2ef640" and at(0x00233C2A) == "add rax, 0x4e68c" and at(0x00233C33).startswith("mov qword ptr [rip"),
      "%s | %s | %s" % (at(0x00233C25), at(0x00233C2A), at(0x00233C33)))
check("B2", at(0x00233C20) == "test rax, rax" and at(0x00233C23) == "jne 0x233c4d" and at(0x00233C4D) == "cmp dword ptr [rax], 0x5071901"
      and at(0x00233C53) == "je 0x233c5e" and at(0x00233C59) == "jmp 0x237df0" and not any(x.mnemonic == "jne" and 0x00233C4D <= x.address < 0x00233C5E for x in B),
      "%s / %s; %s / %s; wrong magic falls through to %s" % (at(0x00233C20), at(0x00233C23), at(0x00233C4D), at(0x00233C53), at(0x00233C59)))
z = lambda a: S(ZI[a]) if a in ZI else "?"
check("B3", z(0x002370CD) == "mov r8d, 0x7410" and z(0x002370D3) == "call 0x861ec0" and z(0x002370DF) == "mov dword ptr [rax], 0x5071901",
      "%s | %s | %s" % (z(0x002370CD), z(0x002370D3), z(0x002370DF)))
check("B4", z(0x002370EA) == "mov ecx, 0x5a48" and z(0x002370EF) == "mov edx, 0xffff" and z(0x00237107) == "mov word ptr [rcx + rax], dx"
      and z(0x0023710F) == "cmp rcx, 0x5a5a", "%s .. %s .. %s" % (z(0x002370EA), z(0x00237107), z(0x0023710F)))
check("B5", z(0x00237121) == "mov dword ptr [rax + 0x5acc], ecx" and z(0x0023712E) == "mov dword ptr [rax + 0x5ac8], ecx"
      and sizes[0x00233C10] == 214 and sizes[0x002370C0] == 121, "%s | %s" % (z(0x00237121), z(0x0023712E)))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
