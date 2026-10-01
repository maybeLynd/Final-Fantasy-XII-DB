"""Falsification pass 1 on CONTRACT-steam-integration-subsystem (OPUS, 2026-09-29), from the shipping image, using the
contract's own "Falsified by" tests. Each row states what the bytes show.

  K1  (MEETS I-1's own falsifier "a writer of 01F83450 outside 0020CD30") the stores to 01F83450 are 0020CD71 in 0020CD30 and
      0020CDED in 0020CD80 - the manager's destructor, which frees the 0x80 bytes and stores 0 (the linear sweep finds the same
      two). The substance survives: the only non-null store is 0020CD30's, so no route installs a manager without it; 0020CE00
      is `mov rax, [01F83450]; ret` and 008632B0 returns on null before tail-jumping to 0020CE60
  W2  I-2 / I-3: every SetAchievement (slot +0x38 through the context) is in 0020CE60, 0020CB50 (twice), 0020C940 or 0020CE10.
      The first three test +0x190 and +0x18 in the body. 0020CE10 tests +0x18 only; its one caller, the 1103 handler 0020C8C0,
      re-reads entry 0's flag from Steam (slot +0x30 into +0x190) and tests it immediately before the call
  W3  section 9's `cmp ebx, 6` branch: when the matched by-id row is index 6, 0020CB50 walks entry offsets 0x3168..0x3C90 in
      0x198 steps - entries 31..37 - awarding each under the same two tests
  W4  I-4: the seven by-id rows (00906290, 12 B each) map to entry indices none of which is 0; each by-index call site of
      008632B0 passes a non-constant index or a constant other than 0
  W5  I-5: SteamAPI_RunCallbacks is called from exactly one site, 007A312E, and 007A3110 returns 9 first when [02EA5368]+0x69 is set
  W6  I-6 / section 3: in 007980A0, ContextInit (00798116) and SteamAPI_Init (00798123) precede the manager (0079812D) and
      RestartAppIfNecessary(0x91640) (0079813C), and a true return reaches exit(1) (0079814B)
"""
import io, os, struct
from array import array
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_MEM, X86_REG_RIP

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
FUNCS = os.path.join(ROOT, "Tools", "work", "graph", "functions.tsv")
blob = io.open(EXE, "rb").read()
pe = pefile.PE(EXE); BASE = pe.OPTIONAL_HEADER.ImageBase
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
body = lambda fa: {x.address: x for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa)}
at = lambda I, a: S(I[a]) if a in I else "?"
imm = lambda x: x.operands[0].imm if x.operands and x.operands[0].type == X86_OP_IMM else None
text = next(x for x in SECS if x[0] == ".text")
iat = {}
for e in pe.DIRECTORY_ENTRY_IMPORT:
    for imp in e.imports:
        if imp.name:
            iat[imp.name.decode()] = imp.address
MGR, CTX = 0x01F83450, 0x01DFE0D0

stores_b, fn_of, all_fn = [], {}, {}
slot38, callers_by_index, run_cb = [], [], []
for fa in sorted(sizes):
    if not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        ins = list(md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa))
    except ValueError:
        continue
    for k, x in enumerate(ins):
        if MGR in rip(x) and x.operands[0].type == X86_OP_MEM and x.mnemonic.startswith("mov"):
            stores_b.append((x.address, fa))
        if x.mnemonic in ("call", "jmp") and imm(x) == 0x008632B0:
            callers_by_index.append((x.address, fa, [S(y) for y in ins[max(0, k - 3):k]]))
        if x.mnemonic in ("call", "jmp") and iat.get("SteamAPI_RunCallbacks") in rip(x):
            run_cb.append(x.address)
        if x.mnemonic in ("call", "jmp") and x.operands and x.operands[0].type == X86_OP_MEM and x.operands[0].mem.disp == 0x38 \
                and x.reg_name(x.operands[0].mem.base) not in ("rip", "rsp") and not x.operands[0].mem.index:
            back = ins[max(0, k - 5):k]
            if any("+ 0x28]" in S(y) for y in back) and any(CTX in rip(y) for y in ins[max(0, k - 8):k]):
                slot38.append((x.address, fa))
# linear sweep for stores to MGR
raw = blob[text[3]:text[3] + text[4]]
want = {MGR - t for t in (0, 1, 2, 4)}
cands = set()
for s in range(4):
    a = array("i"); n = (len(raw) - s) // 4; a.frombytes(raw[s:s + 4 * n])
    base = text[1] + s + 4
    for kk, d in enumerate(a):
        if base + 4 * kk + d in want:
            cands.add(text[1] + s + 4 * kk)
lin = {}
for pos in cands:
    for L in range(1, 12):
        x = next(md.disasm(blob[OFF(pos - L):OFF(pos - L) + 16], pos - L), None)
        if x and x.address < pos < x.address + x.size and MGR in rip(x):
            lin[x.address] = x; break
lin_st = sorted(a for a, x in lin.items() if x.operands[0].type == X86_OP_MEM and x.mnemonic.startswith("mov"))
T = body(0x008632B0); G = body(0x0020CE00)
D = body(0x0020CD80)
check("K1", sorted(stores_b) == [(0x0020CD71, 0x0020CD30), (0x0020CDED, 0x0020CD80)] and len(lin_st) == 2 and all(abs(a - b_) <= 1 for a, (b_, _f) in zip(lin_st, sorted(stores_b)))
      and at(D, 0x0020CDED) == "mov qword ptr [rip + 0x1d76658], 0" and at(D, 0x0020CDE0) == "mov edx, 0x80" and at(D, 0x0020CDE8) == "call 0x809950"
      and [S(x) for x in sorted(G.values(), key=lambda y: y.address)][:2] == ["mov rax, qword ptr [rip + 0x1d76649]", "ret"] and rip(G[0x0020CE00]) == [MGR]
      and any(x.mnemonic in ("je", "jne") for x in T.values()) and any(x.mnemonic == "jmp" and imm(x) == 0x0020CE60 for x in T.values()),
      "(MEETS I-1's falsifier; substance survives) stores to 01F83450 %s (linear %s); the second stores 0 after freeing 0x80 bytes; 0020CE00 %s; 008632B0 null test then jmp 0020CE60"
      % (["%08X in %08X" % s for s in stores_b], ["%08X" % a for a in lin_st], [S(x) for x in sorted(G.values(), key=lambda y: y.address)][:2]))
A = body(0x0020CE60); B = body(0x0020CB50)
guards = lambda I, sites: all(any("+ 0x190]" in S(I[a]) and I[a].mnemonic == "cmp" for a in I if a < s) and any("+ 0x18]" in S(I[a]) and I[a].mnemonic == "cmp" for a in I if a < s) for s in sites)
a38 = [a for a, x in A.items() if x.mnemonic in ("call", "jmp") and "[rax + 0x38]" in x.op_str]
b38 = [a for a, x in B.items() if x.mnemonic in ("call", "jmp") and "[rax + 0x38]" in x.op_str]
C8 = body(0x0020C8C0); C9 = body(0x0020C940); E10 = body(0x0020CE10)
ce10_callers = []
for fa in sorted(sizes):
    if not (text[1] <= fa < text[1] + text[2]):
        continue
    try:
        for x in md.disasm(blob[OFF(fa):OFF(fa) + sizes[fa]], fa):
            if x.mnemonic in ("call", "jmp") and imm(x) == 0x0020CE10:
                ce10_callers.append(x.address)
    except ValueError:
        continue
check("W2", a38 == [0x0020CEB2] and sorted(b38) == [0x0020CBF2, 0x0020CC5F] and guards(A, a38)
      and at(B, 0x0020CBBB) == "cmp byte ptr [rcx + 0x190], bpl" and at(B, 0x0020CBD5) == "cmp byte ptr [rdi + 0x18], bpl"
      and at(B, 0x0020CC24) == "cmp byte ptr [rbx + rax + 0x190], bpl" and at(B, 0x0020CC42) == "cmp byte ptr [rdi + 0x18], bpl"
      and {f for _a, f in slot38} == {0x0020CE60, 0x0020CB50, 0x0020C940, 0x0020CE10}
      and at(C8, 0x0020C901) == "call qword ptr [rax + 0x30]" and at(C8, 0x0020C8F3) == "lea r8, [rdx + 0x190]" and at(C8, 0x0020C908) == "cmp byte ptr [rdx + 0x190], 0"
      and at(C8, 0x0020C918) == "call 0x20ce10" and ce10_callers == [0x0020C918] and at(E10, 0x0020CE16) == "cmp byte ptr [rcx + 0x18], 0"
      and at(C9, 0x0020CAB1) == "cmp byte ptr [rax + 0x190], 0" and at(C9, 0x0020CABA) == "cmp byte ptr [rbx + 0x18], 0",
      "SetAchievement sites 0020CE60 %s, 0020CB50 %s, each after the +0x190 and +0x18 tests; every slot-0x38 call through the context in %s"
      % (["%08X" % a for a in a38], ["%08X" % a for a in sorted(b38)], sorted({"%08X" % f for _a, f in slot38})))
check("W3", at(B, 0x0020CC0C) == "cmp ebx, 6" and at(B, 0x0020CC11) == "mov ebx, 0x3168" and at(B, 0x0020CC79) == "add rbx, 0x198"
      and at(B, 0x0020CC80) == "cmp rbx, 0x3c90" and 0x3168 // 0x198 == 31 and 0x3C90 // 0x198 == 38 and 0x3168 % 0x198 == 0,
      "row 6 also awards entries %d..%d" % (0x3168 // 0x198, 0x3C90 // 0x198 - 1))
rows = [struct.unpack("<iii", blob[OFF(0x00906290 + 12 * k):OFF(0x00906290 + 12 * k) + 12]) for k in range(7)]
lit0 = [(a, pre) for a, f, pre in callers_by_index if pre and pre[-1] in ("xor ecx, ecx", "mov ecx, 0")]
check("W4", all(r[2] != 0 for r in rows) and not lit0 and len(callers_by_index) >= 6,
      "by-id rows (key1, key2, entry) %s; by-index call sites %d, literal 0 index %s" % (rows, len(callers_by_index), lit0))
W = body(0x007A3110)
check("W5", run_cb == [0x007A312E] and any("+ 0x69]" in S(x) for x in W.values()) and any(S(x) == "mov eax, 9" for x in W.values()),
      "SteamAPI_RunCallbacks call sites %s" % ["%08X" % a for a in run_cb])
St = body(0x007980A0)
order = [(a, rip(St[a])) for a in (0x00798116, 0x00798123, 0x0079813C) if a in St]
imp_at = lambda a: next((n for n, v in iat.items() if St.get(a) and v in rip(St[a])), None)
check("W6", imp_at(0x00798116) == "SteamInternal_ContextInit" and imp_at(0x00798123) == "SteamAPI_Init" and at(St, 0x0079812D) == "call 0x20cd30"
      and imp_at(0x0079813C) == "SteamAPI_RestartAppIfNecessary" and any(S(St[a]) == "mov ecx, 0x91640" for a in St if 0x0079812D < a < 0x0079813C)
      and 0x0079814B in St and St[0x0079814B].mnemonic in ("call", "jmp"),
      "%s -> %s -> manager -> %s; %s" % (imp_at(0x00798116), imp_at(0x00798123), imp_at(0x0079813C), at(St, 0x0079814B)))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)
