"""arena.py - OV-42 / OV-19 static residue: does any higher-level release free an orphaned owner source?
(FABLE, Claude Opus 5.5, 2026-09-29). STATIC.

An orphan arises when a submission is rejected: the owner writes state 3 without a queue entry, no callback ever runs, and
group re-initialisation clears the record without freeing its source (../ov42-submit-recovery-fable/). The source is an
arena allocation; this asks whether an arena-level release reclaims it.

  A  THE ARENA: the producer 003DD4C0 allocates from arena 11 (`0036C1D0(11, 5)`) only when 0037B330() returns 2 and the
     record's +0x17 bit 6 is set, and otherwise from arena 6 (`0036C1D0(6, 5)`)
  C  ARENA-LEVEL CENSUS: the teardown steps 00369760 (report) and 0036D160 (disable), the backing release 0036D250 and the
     re-init 00369D30 are called only with these arena ids, every one resolved (immediates, `lea ecx, [r9 +/- k]` after a
     `mov`/`xor` of r9, and 002628B0's 13 + a non-negative manager index): 00369760/0036D160 with 11-14 and 13+index;
     00369D30 at boot 0022A0B0 (arenas 2-9 and 11) and for 11-14; 0036D250 only in 0037B3D0. Arena 6 appears only in the
     boot init
  T  ARENA 11's REPLACEMENT 0037B3D0, when the state byte 02ADD930 differs from 02ADD931: 00369760(11), 0036D160(11),
     free the old backing (0036D250 -> free), malloc a new one (0036D240), re-init 00369D30(11, backing, size, 0x100)
  D  THE REPORT FREES NOTHING: 00369760's worker 0036A570 and its helper 0036A850 format block labels ('M2/U', 'FREE', ...)
     through strncpy and call no allocator release
  K  sensitivity: the census's argument reader resolves the immediate arena ids at the known replacement sites (11) and
     the boot site for arena 6
So an orphaned source in arena 11 is reclaimed with the whole backing at the next arena-11 state change; one in arena 6
is never reclaimed by any arena-level release for the life of the process.
"""
import hashlib, os, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "exe", "FFXII_TZA.exe")
d = open(EXE, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [(d[pe + 24 + opt + i * 40:pe + 24 + opt + i * 40 + 8].rstrip(b"\0"),) + struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8)
        for i in range(n)]
def off(v):
    for nm, vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
TX = [s for s in SECS if s[0] == b".text"][0]
text = d[TX[4]:TX[4] + TX[3]]; tb = B + TX[2]
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, msg):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, msg))
def dis(a, b): return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(a):off(b)], a)}
at = lambda c, w: all(c.get(a) == s for a, s in w.items())
def callers(t):
    return [tb + j for j in range(len(text) - 5) if text[j] in (0xE8, 0xE9) and tb + j + 5 + struct.unpack_from("<i", text, j + 1)[0] == t]
def arg_ecx(site):
    """the arena id in ecx at a call: `mov ecx, imm`, or `lea ecx, [r9 +/- k]` with r9 set by `mov r9d, imm` /
    `xor r9d, r9d` in the same window. 002628B0's `lea ecx, [rdi + 0xd]` (rdi = the movsxd manager index, >= 0) is
    returned as the string 'rdi+13'. Anything else is None."""
    for back in range(48, 0, -1):
        ins = list(cs.disasm(d[off(site - back):off(site + 5)], site - back))
        if not ins or ins[-1].address != site: continue
        body = ins[:-1]
        for i in range(len(body) - 1, -1, -1):
            x = body[i]
            if x.mnemonic == "call": return None
            if x.mnemonic == "mov" and x.op_str.startswith("ecx, "):
                v = x.op_str.split(", ")[1]
                return int(v, 0) if re.fullmatch(r"0x[0-9a-f]+|\d+", v) else None
            m = re.fullmatch(r"ecx, \[(r9|rdi) ([+-]) (0x[0-9a-f]+|\d+)\]", x.op_str) if x.mnemonic == "lea" else None
            if m:
                k = int(m.group(3), 0) * (1 if m.group(2) == "+" else -1)
                if m.group(1) == "rdi": return "rdi+%d" % k
                for y in reversed(body[:i]):
                    if y.mnemonic == "xor" and y.op_str == "r9d, r9d": return k
                    if y.mnemonic == "mov" and y.op_str.startswith("r9d, "): return int(y.op_str.split(", ")[1], 0) + k
                return None
        return None
    return None
# A
a = dis(0x3DD58B, 0x3DD5D0)
check("A", at(a, {0x3DD58B: "call 0x37b330", 0x3DD590: "cmp eax, 2", 0x3DD593: "jne 0x3dd5b8", 0x3DD595: "test byte ptr [rsi + 0x17], 0x40",
                  0x3DD59B: "lea edx, [rax + 3]", 0x3DD59E: "lea ecx, [rax + 9]", 0x3DD5A1: "call 0x36c1d0",
                  0x3DD5B8: "mov edx, 5", 0x3DD5BD: "lea ecx, [rdx + 1]", 0x3DD5C0: "call 0x36c1d0"}),
      "the producer takes arena 11 (2 + 9) only when 0037B330() == 2 and +0x17 bit 6; otherwise arena 6 (5 + 1)")
# C
census = {}
for t in (0x369760, 0x36D160, 0x369D30, 0x36D250):
    census[t] = [(c, arg_ecx(c)) for c in callers(t)]
six = [(hex(t), hex(c)) for t, cl in census.items() for c, v in cl if v == 6]
check("C", six == [(hex(0x369D30), hex(0x22A321))] and census[0x36D250] == [(0x37B419, None)]
      and all(v in (11, 12, 13, 14, "rdi+13") for t in (0x369760, 0x36D160) for c, v in census[t])
      and all(v is not None and v != 6 or c == 0x22A321 for t in (0x369760, 0x36D160, 0x369D30) for c, v in census[t])
      and dis(0x2628D3, 0x2628D7).get(0x2628D3) == "movsxd rdi, ecx",
      "arena 6 is named only by the boot init 0022A321; teardown/disable name only 11-14 (or a computed id); the backing "
      "release is called only in 0037B3D0. Census: %s" % {("%08X" % t): [("%08X" % c, v) for c, v in cl] for t, cl in census.items()})
# T
r = dis(0x37B3D0, 0x37B44F)
check("T", at(r, {0x37B3F6: "cmp byte ptr [rip + 0x2762535], al", 0x37B3FC: "je 0x37b442", 0x37B3FE: "mov ecx, 0xb", 0x37B403: "call 0x369760",
                  0x37B40D: "call 0x36d160", 0x37B419: "call 0x36d250", 0x37B420: "call 0x36d240", 0x37B438: "mov ecx, 0xb",
                  0x37B43D: "call 0x369d30"})
      and dis(0x36D250, 0x36D25A) == {0x36D250: "test rcx, rcx", 0x36D253: "jne 0x19c590", 0x36D259: "ret"}
      and dis(0x19C590, 0x19C597).get(0x19C590, "").startswith("jmp qword ptr [rip + 0x7265b1]"),
      "on a state change arena 11 is reported, disabled, its backing freed (free), a new one allocated and re-initialised")
# D
FREES = {0x369800, 0x36A100, 0x19C590, 0x36D250}
calls = [s for f, e in ((0x36A570, 0x36A849), (0x36A850, 0x36A9BF)) for s in dis(f, e).values() if s.startswith("call")]
check("D", not any(s == "call %#x" % f for s in calls for f in FREES) and "call 0x36a850" in calls,
      "the report worker 0036A570 and its helper call no release: %s" % sorted(set(calls)))
# K
check("K", arg_ecx(0x37B403) == 11 and arg_ecx(0x22A321) == 6, "the argument reader resolves known sites (0037B403 -> 11, 0022A321 -> 6)")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
