"""Falsification pass 1 on CONTRACT-license-check (OPUS, 2026-09-29), from the shipping image. Killers first.

  L0  section 2: 00323EC0 materialises class 0x14 as `lea ecx, [r8 + 0x14]` after `xor r8d, r8d`; the validator 00322C50
      takes classes 1..32 (`lea eax, [rcx-1]` / `cmp eax, 0x1f` / `ja`), dispatches through image + 0x203054, and its first
      touch of r8 is a write                                                    KILLER: another class, range, table or an r8 read
  L1  I1 the exits, in order: validator -> 0; null record, kind byte +5 != 0, slot +4 > 6 (UNSIGNED `ja`) -> 1
  L2  I3 `test word ptr [rcx + 0x2c], 0x2000`; the null arms load rcx from the zeroed rdi; the row sum is formed in 32 BITS
      (`imul ecx, ebx` / `add ecx, eax`), which the contract's formula does not say
  L3  I5 ids 0xD0..0xE1 (`lea eax, [rbx-0xd0]` / `cmp eax, 0x11` / `ja`); the party row is indexed by byte +4, also summed in
      32 bits; 0030A330 compares the BYTES at row+4..+6, loads 0xFFFF when the row is null, returns 0..3; the gate is `setl`
  L4  00324020 is three passes (`lea edi, [r9+3]` ... `sub rdi, 1` / `jne`) of six bit tests against rbx + 0x194
  L5  (REFUTES "the only caller fixes at 1") 00323BB0 has TWO entrants, both tail jumps: 00323EC0 with `mov edx, 1` and the
      equipment check 00323C60 with `xor edx, edx`; the builder 002F8FA0's one caller is 00323BB0, and it compares that first
      argument with 00323890's class of the row's byte +5
  L6  (REFUTES "the early exit is semantically load-bearing") after the builder returns, 00323BB0 writes no memory and calls
      only __security_check_cookie; its two exits load the constants 1 and 0. The result is the OR of all 46 byte-ANDs, so
      the early return cannot change it                                   KILLER: a write, a call or a non-constant return
  L7  sections 7 and 9: the closure of 00323EC0 writes memory only at 002F9085 (the caller's buffer, through r15), in memset
      and on the GS-failure path; the only global it reads outside descriptors and image tables is 01EEBCF8, which nothing
      writes except the GS cookie                                           KILLER: another write site or a written global read
  L8  (context for section 14) the Quickening counter 00324020 is called at 13 sites in 7 functions; 00323EC0 has two callers
"""
import collections, io, os, re, struct
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
    return bool(x.operands) and x.operands[0].type == X86_OP_MEM and x.mnemonic in ("mov", "inc", "dec", "add", "sub", "or", "and", "xor", "bts", "btr")


def at(fa, va):
    return next(S(x) for x in bodies[fa] if x.address == va)


def run(fa, lo, hi):
    return [S(x) for x in bodies[fa] if lo <= x.address <= hi]


ASK, PRE, BLD, CNT, ROW, VAL, EQP = 0x00323EC0, 0x00323BB0, 0x002F8FA0, 0x00324020, 0x0030A330, 0x00322C50, 0x00323C60

# L0 section 2: the class materialisation, the validator's range and table, and the unused incoming r8
v = bodies[VAL]
base_lea = next(x for x in v if x.mnemonic == "lea" and x.operands[0].type != X86_OP_MEM and rip(x))
tbl = [S(x) for x in v if "+ 0x203054]" in x.op_str]
R8 = {"r8", "r8d", "r8w", "r8b"}
first_r8 = None
for x in v:
    rd, wr = x.regs_access()
    rd = {x.reg_name(r) for r in rd}; wr = {x.reg_name(r) for r in wr}
    if rd & R8 or wr & R8:
        first_r8 = ("read" if rd & R8 else "write", "%08X" % x.address, S(x)); break
check("L0", run(ASK, 0x00323ECA, 0x00323ED6) == ["xor r8d, r8d", "mov rsi, rcx", "mov ebx, edx", "lea ecx, [r8 + 0x14]", "call 0x322c50"]
      and run(VAL, 0x00322C5A, 0x00322C62) == ["lea eax, [rcx - 1]", "mov ebx, edx", "cmp eax, 0x1f", "ja 0x322c8d"]
      and rip(base_lea) == [BASE] and len(tbl) == 1 and first_r8 is not None and first_r8[0] == "write",
      "class via %s; validator range %s; table base %08X + 0x203054 (%s); first r8 touch %s"
      % (at(ASK, 0x00323ED2), run(VAL, 0x00322C5A, 0x00322C62), rip(base_lea)[0], tbl, first_r8))
# L1 I1: the four exits in order
check("L1", at(ASK, 0x00323EDD) == "jne 0x323eea" and run(ASK, 0x00323EEA, 0x00323F03) == [
          "test rsi, rsi", "je 0x324002", "movzx eax, byte ptr [rsi + 5]", "test eax, eax", "jne 0x324002", "cmp byte ptr [rsi + 4], 6", "ja 0x324002"]
      and at(ASK, 0x00324002) == "mov eax, 1",
      "validator fail falls through to ret with eax = 0 (%s); then %s; 00324002 %s"
      % (at(ASK, 0x00323EDD), run(ASK, 0x00323EEA, 0x00323F03), at(ASK, 0x00324002)))
# L2 I3: the escape bit, the null arms, and the 32-bit row sum
check("L2", run(ASK, 0x00323F3F, 0x00323F56) == ["movzx ecx, word ptr [rcx + 8]", "imul ecx, ebx", "add ecx, eax", "jmp 0x323f4d",
                                                 "mov rcx, rdi", "mov eax, 0x2000", "test word ptr [rcx + 0x2c], ax", "je 0x323f6d"]
      and at(ASK, 0x00323F15) == "xor edi, edi" and at(ASK, 0x00323F1A) == "je 0x323f4a" and at(ASK, 0x00323F27) == "je 0x323f4a",
      "row = (u32)(stride * id + (u32)decode) - %s; null arms -> %s" % (run(ASK, 0x00323F43, 0x00323F46), at(ASK, 0x00323F4A)))
# L3 I5: the id range, the party row, the byte search, the signed gate
rs = [S(x) for x in bodies[ROW]]
check("L3", run(ASK, 0x00323F6D, 0x00323F76) == ["lea eax, [rbx - 0xd0]", "cmp eax, 0x11", "ja 0x323fe3"]
      and run(ASK, 0x00323FAB, 0x00323FB2) == ["movzx ecx, byte ptr [rsi + 4]", "imul ecx, edx", "add ecx, eax"]
      and at(ASK, 0x00323FB9) == "movzx edx, bx" and run(ASK, 0x00323FCB, 0x00323FCD) == ["cmp ebx, eax", "setl dil"]
      and "movzx ecx, byte ptr [rax + r9 + 4]" in rs and "mov ecx, 0xffff" in rs and "cmp rax, 2" in rs and "cmp rax, 3" in rs
      and "cmp cx, dx" in rs and rs[-2:] == ["mov eax, r8d", "ret"],
      "range %s; party row %s; search %d instructions, byte ids at +4..+6, sentinel 0xFFFF; gate %s"
      % (run(ASK, 0x00323F6D, 0x00323F76), run(ASK, 0x00323FAB, 0x00323FB2), len(rs), run(ASK, 0x00323FCB, 0x00323FCD)))
# L4 00324020: three passes of six
cb = bodies[CNT]
tests = [x for x in cb if "+ rbx + 0x194]" in x.op_str]
check("L4", "lea edi, [r9 + 3]" in [S(x) for x in cb] and run(CNT, 0x003240C5, 0x003240C5) == ["add r11d, 6"]
      and run(CNT, 0x003240E2, 0x003240E6) == ["sub rdi, 1", "jne 0x324040"] and len(tests) == 6,
      "%d byte tests against rbx + 0x194 per pass, trip count 3, stride 6 bits" % len(tests))
# L5 (REFUTES "the only caller fixes at 1"): two entrants, kind 1 (actions) and kind 0 (equipment)
ent = sorted(("%08X" % f, "%08X" % a, m) for f, a, m in calls_to[PRE])
kind_ask = at(ASK, 0x00323FE6)
kind_eqp = at(EQP, 0x00323CE8)
bc = sorted("%08X" % f for f, _a, _m in calls_to[BLD])
check("L5", ent == [("00323C60", "00323CF7", "jmp"), ("00323EC0", "00323FFD", "jmp")] and kind_ask == "mov edx, 1" and kind_eqp == "xor edx, edx"
      and names.get("BattleStats_HasRequiredLicenseForEquipment") == EQP and bc == ["00323BB0"]
      and run(BLD, 0x002F8FC8, 0x002F8FC8) == ["mov r12d, ecx"] and run(BLD, 0x002F9045, 0x002F9051) == [
          "movzx ecx, byte ptr [rbx + 5]", "call 0x323890", "cmp r12d, eax", "jne 0x2f908b"],
      "00323BB0 entered from %s; kinds: actions %s, equipment %s (00323CE5 passes the item id in r8d); builder <- %s"
      % (ent, kind_ask, kind_eqp, bc))
# L6 (REFUTES "the early exit is semantically load-bearing"): nothing after the builder can depend on where the loop stops
tail = [x for x in bodies[PRE] if x.address > 0x00323BFC]
wr6 = [S(x) for x in tail if is_write(x)]
cl6 = sorted({"%08X" % T(x) for x in tail if x.mnemonic == "call"})
exits = [S(x) for x in tail if x.address in (0x00323C2D, 0x00323C42)]
check("L6", not wr6 and cl6 == ["00808C40"] and names.get("__security_check_cookie") == 0x00808C40 and exits == ["xor eax, eax", "mov eax, 1"]
      and run(PRE, 0x00323C20, 0x00323C2B) == ["test byte ptr [rdx], cl", "jne 0x323c42", "inc rax", "cmp rax, 0x2e", "jl 0x323c10"],
      "after the builder: writes %s; calls %s; exits %s - the result is OR over all 0x2E byte-ANDs, early return or not"
      % (wr6 or "none", cl6, exits))
# L7 sections 7 and 9: the closure's writes and the globals it reads
GS = {0x00809620, 0x00809654, 0x00809848, 0x0087AF34, 0x00808C40}
seen, st = set(), [ASK]
while st:
    f = st.pop()
    if f in seen or f not in bodies:
        continue
    seen.add(f)
    for x in bodies[f]:
        t = T(x) if x.mnemonic in ("call", "jmp") else None
        if t is not None and t in bodies and not (f <= t < f + sizes[f]):
            st.append(t)
body = seen - GS
wr7 = sorted(("%08X" % f, "%08X" % x.address) for f in body for x in bodies[f] if is_write(x) and "rsp" not in x.op_str.split(",")[0])
reads = sorted({t for f in body for x in bodies[f] for t in rip(x)})
table = {t for t in reads if t == BASE}
descs = {t for t in reads if 0x02EBF000 <= t < 0x02EBF200}
other = [t for t in reads if t not in table | descs]
COOKIE = names.get("__security_cookie", 0x01F44830)   # the GS cookie: fixed after CRT start-up, read only to verify the frame
cookie_writers = sorted({"%08X" % f for f, x in refs[COOKIE] if is_write(x)})
written = [("%08X" % t) for t in other if t != COOKIE and any(is_write(x) for _f, x in refs[t])]
check("L7", wr7 == [("002F8FA0", "002F9085")] and at(BLD, 0x002F8FC2) == "mov r15, r8" and 0x00861EC0 in body
      and sorted("%08X" % t for t in other) == ["008C2A60", "01EEBCF8", "01F44830", "01F83530"] and written == [] and len(cookie_writers) <= 2,
      "%d functions (%d GS-failure helpers set aside); writes %s; globals read beside the %d descriptor cells: %s; any with a rip-relative writer in a listed body (the cookie aside, written by %s): %s"
      % (len(seen), len(seen & GS), wr7, len(descs), ["%08X" % t for t in other], cookie_writers, written or "none"))
# L8 context for section 14: who else counts bits 0..17, and who asks
cnt = calls_to[CNT]
ask = sorted("%08X" % f for f, _a, _m in calls_to[ASK])
check("L8", len(cnt) == 13 and len({f for f, _a, _m in cnt}) == 7 and ask == ["00306480", "003064F0"],
      "00324020 called at %d sites in %d functions %s; 00323EC0 <- %s"
      % (len(cnt), len({f for f, _a, _m in cnt}), sorted({"%08X" % f for f, _a, _m in cnt}), ask))
print("FAILS %d" % fails)
raise SystemExit(1 if fails else 0)   # a BROKEN row must fail the process, not only the text (ASTRA feb631dd4, 2026-09-29)
