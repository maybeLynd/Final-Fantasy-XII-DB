"""bit46_writers.py - who sets, clears and tests battle-unit flag bit 46 (qword +0x00, mask 0x0000400000000000)?
FABLE (Claude Opus 5.5), 2026-09-30, for DATA-REQ-FABLE-BATTLEUNIT-BIT46-0930.

Method: an image-wide raw sweep of .text for every instruction form that names bit 46 by an immediate --
movabs of 0x0000400000000000 / 0xFFFFBFFFFFFFFFFF, bt/bts/btr/btc with imm8 0x2E, and dword or/and/test/xor with
0x4000 / 0xFFFFBFFF (the high dword of the flag qword). Each raw byte hit is decoded at every start 0..12 bytes back.
It does NOT see a mask built in a register (shl/not), loaded from memory, or a whole-qword store of a computed or
saved value; C5 reads the two whole-qword writers the field map already names.

Checks (each prints PASS/FAIL; FAILS n at the end):
  C0 control: the sweep finds the three sites already cited by pages (00304EF3, 00304F9F, 0023B0D4).
  C1 exactly one set: 00304EF3-00304EFD, phase 9 of BattleUnit_AdvanceStandardActionState.
  C2 exactly one immediate-form clear: 00304F9F-00304FA9, and it is guarded by (dword [unit+0x690] & 0xA) == 0xA
     (r12 = rcx + 0x690 at 00304886; 00304F91-00304F9A), on the arm where the definition +0x0C bit 30 is clear.
  C3 phase 10's bit-30 arm (00304F62-00304F8C) advances the phase with no write through the unit pointer rdi.
  C4 the high-dword 0x4000 hits in 00239960 address [02EBF190]+4 (the battle-state block's registry slot), not a unit.
  C5 the whole-qword writers 00300EAA / 00300198 are read-modify-writes that clear only bit 14 (btr ..., 0xe).
  C6 the reader: PartyControl_RecomputeSuppressionFromLeaderBattleState tests the party leader's (BattleUnit_GetPartyLeader
     003272A0) flag qword at 0023B0E6 and forces ebx = -1 (all suppressed) at 0023B0E9."""
import sys, struct, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "Tools", "work", "FABLE", "takebacks"))
import tk
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
md = Cs(CS_ARCH_X86, CS_MODE_64)
d = tk.d
BASE = 0x00120000
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
text = None
for i in range(nsec):
    s = pe + 24 + opt + 40 * i
    if d[s:s + 8].rstrip(b"\0") == b".text":
        vs, va, rs, ro = struct.unpack_from("<IIII", d, s + 8); text = (va, ro, rs)
va, ro, rs = text
blob = d[ro:ro + rs]
cands = set()
for p in (struct.pack("<Q", 0x0000400000000000), struct.pack("<Q", 0xFFFFBFFFFFFFFFFF),
          struct.pack("<I", 0x00004000), struct.pack("<I", 0xFFFFBFFF), b"\x0f\xba"):
    i = blob.find(p)
    while i >= 0:
        cands.add(i); i = blob.find(p, i + 1)
def names_bit46(x):
    s = x.op_str.replace(" ", "")
    if x.mnemonic == "movabs": return s.endswith(",0x400000000000") or s.endswith(",0xffffbfffffffffff")
    if x.mnemonic in ("bt", "bts", "btr", "btc"): return s.endswith(",0x2e")
    if x.mnemonic in ("test", "and", "or", "xor") and s.startswith("dwordptr"): return s.endswith(",0x4000") or s.endswith(",0xffffbfff")
    return False
found = {}
for c in sorted(cands):
    for back in range(13):
        st = c - back
        if st < 0: continue
        for x in md.disasm(blob[st:st + 16], BASE + va + st, 1):
            if x.address + x.size > BASE + va + c and names_bit46(x): found[x.address] = x
hits = sorted(found.values(), key=lambda x: x.address)
movabs = [x for x in hits if x.mnemonic == "movabs"]
btfam = [x for x in hits if x.mnemonic.startswith("bt")]
hidword = [x for x in hits if x.mnemonic in ("test", "and", "or", "xor") and ("+ 4]" in x.op_str)]
print("sweep: %d hits; movabs %d, bt-family imm 0x2E %d, high-dword [reg+4] forms %d" % (len(hits), len(movabs), len(btfam), len(hidword)))
for x in movabs + btfam + hidword:
    o, _ = tk.owner(x.address)
    print("  %08X %-6s %-40s in %08X %s" % (x.address, x.mnemonic, x.op_str, o, tk.fname(o)))
fails = 0
def check(name, ok):
    global fails
    print("%s %s" % (name, "PASS" if ok else "FAIL")); fails += 0 if ok else 1
def win(fn, lo, hi): return [x for x in tk.fdis(fn) if lo <= x.address <= hi]
def at(fn, a):
    return [x for x in tk.fdis(fn) if x.address == a][0]
check("C0 control: 00304EF3, 00304F9F, 0023B0D4 found", {0x00304EF3, 0x00304F9F, 0x0023B0D4} <= set(found))
SM = 0x00304850
sets = [x for x in movabs if x.op_str.endswith("0x400000000000") and x.address != 0x0023B0D4]
c1 = [x.address for x in sets] == [0x00304EF3] and at(SM, 0x00304EFD).mnemonic == "or" and at(SM, 0x00304EFD).op_str == "qword ptr [rdi], rax"
check("C1 one set: 00304EF3 movabs + 00304EFD or qword ptr [rdi], rax", c1)
clears = [x.address for x in movabs if x.op_str.endswith("0xffffbfffffffffff")]
g = win(SM, 0x00304F91, 0x00304FA9)
r12 = at(SM, 0x00304886)
c2 = (clears == [0x00304F9F] and not btfam and r12.op_str == "r12, [rcx + 0x690]"
      and [(x.mnemonic, x.op_str) for x in g[:4]] == [("mov", "eax, dword ptr [r12]"), ("and", "eax, 0xa"), ("cmp", "al, 0xa"), ("jne", "0x304fc3")]
      and at(SM, 0x00304FA9).op_str == "qword ptr [rdi], rax"
      and at(SM, 0x00304F62).op_str == "dword ptr [r15 + 0xc], 0x40000000" and at(SM, 0x00304F6A).op_str == "0x304f91")
check("C2 the EXACT single-bit clear mask appears only at 00304F9F-00304FA9, guarded by ([unit+0x690] & 0xA) == 0xA on the bit-30-clear arm", c2)
# C7/C8 (added 2026-09-30 after SWE2-AUDIT-SEM's REJECT, auditsem-review-bit46-0930): the exact-mask test above is blind
# to COMPOSITE masks - any and-mask with bit 46 clear clears it. Widened sweep: every `movabs r64, imm64` whose register
# is next applied as `and qword ptr [m], r64` (bit 46 clear in imm) or `or qword ptr [m], r64` (bit 46 set in imm).
B46 = 1 << 46
wide = []
i = blob.find(b"\xb8")
starts = set()
for p in range(1, len(blob) - 10):
    if blob[p - 1] in (0x48, 0x49) and 0xB8 <= blob[p] <= 0xBF: starts.add(p - 1)
for st in sorted(starts):
    seq = list(md.disasm(blob[st:st + 64], BASE + va + st, 9))
    if not seq or seq[0].mnemonic != "movabs": continue
    reg, imm = [o.strip() for o in seq[0].op_str.split(",")]
    imm = int(imm, 16)
    for x in seq[1:]:
        ops = [o.strip() for o in x.op_str.split(",")]
        if len(ops) == 2 and ops[1] == reg and ops[0].startswith("qword ptr ["):
            if (x.mnemonic == "and" and not imm & B46) or (x.mnemonic == "or" and imm & B46):
                wide.append((seq[0].address, x.address, x.mnemonic, imm, ops[0]))
            break
        if reg in x.op_str.split(",")[0]: break          # register overwritten or used another way first
print("widened sweep: %d movabs masks applied to a qword in memory that change bit 46" % len(wide))
for m, a, mn, imm, dst in wide:
    o, _ = tk.owner(m)
    print("  %08X-%08X %-3s %-24s mask 0x%016X in %08X %s" % (m, a, mn, dst, imm, o, tk.fname(o)))
need_wide = {0x00304967, 0x00304DDD, 0x0031063F, 0x003082CB, 0x00304F9F, 0x00304EF3}
check("C7 widened sweep finds the composite clears 00304967, 00304DDD, 0031063F, 003082CB (+ 00304F9F clear, 00304EF3 set)",
      need_wide <= {w[0] for w in wide})
check("C8 regression: the exact-mask test finds none of the four composite clears (the defect C7 fixes)",
      not ({0x00304967, 0x00304DDD, 0x0031063F, 0x003082CB} & set(found)))
arm = win(SM, 0x00304F62, 0x00304F8C)
writes_rdi = [x for x in arm if x.op_str.startswith(("qword ptr [rdi", "dword ptr [rdi", "byte ptr [rdi", "word ptr [rdi"))
              and x.mnemonic not in ("test", "cmp", "bt")]
c3 = (not writes_rdi and at(SM, 0x00304F7E).op_str == "byte ptr [rsi + 4]" and at(SM, 0x00304F7E).mnemonic == "inc"
      and at(SM, 0x00304F8C).mnemonic == "jmp")
check("C3 bit-30 arm 00304F62-00304F8C: no write through rdi; 00304F7E inc byte ptr [rsi + 4] advances the phase", c3)
g2 = win(0x00239960, 0x00239A0B, 0x00239A21) + win(0x00239960, 0x00239A70, 0x00239A77)
def ripq(x): return x.address + x.size + int(x.op_str.split("rip + ")[1].rstrip("]"), 16)
loads = [x for x in g2 if x.mnemonic == "mov" and "rip +" in x.op_str]
c4 = (len(loads) == 2 and all(ripq(x) == 0x02EBF190 for x in loads)
      and sorted(x.address for x in hidword if 0x00239960 <= x.address < 0x00239E00) == [0x00239A18, 0x00239A21, 0x00239A77]
      and all(0x00239960 <= x.address < 0x00239E00 for x in hidword))
check("C4 every high-dword [reg+4] hit is in 00239960 and addresses [02EBF190]+4", c4)
ww = [(0x00300E40, 0x00300EA5, 0x00300EAA), (0x00300140, 0x00300193, 0x00300198)]
c5 = all(at(f, b).mnemonic == "btr" and at(f, b).op_str.endswith(", 0xe") and at(f, s).op_str.startswith("qword ptr [") for f, b, s in ww)
check("C5 00300EAA / 00300198 store the loaded qword with only bit 14 cleared (btr ..., 0xe)", c5)
R = 0x0023B040
c6 = (at(R, 0x0023B084).op_str == "0x3272a0" and at(R, 0x0023B089).op_str == "rdi, rax"
      and at(R, 0x0023B0E6).op_str == "qword ptr [rdi], rax" and at(R, 0x0023B0E9).mnemonic == "cmovne"
      and at(R, 0x0023B0E9).op_str == "ebx, r14d" and at(R, 0x0023B05C).op_str == "r14d, 0xffffffff"
      and tk.fname(0x003272A0).endswith("BattleUnit_GetPartyLeader"))
check("C6 0023B0E6 tests the party leader's qword; 0023B0E9 cmovne ebx, r14d (= -1)", c6)
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
