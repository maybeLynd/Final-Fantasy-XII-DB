"""sibling_gate.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only; nothing executed.
The ATEL sibling loader 003306E0 returns at its first size query on every call in this build.

  Q  QUERIES: every direct call to 0032E400 in the body (14 sites) loads ecx = 0xFF in the instruction before or two before,
     and 0032E400 returns -1 for kind 0xFF before it reads rdx (0032E404 cmp ecx, 0xff -> 0032E438 or eax, -1 -> ret)
  G  GATE: the first query's result goes to r15d (00330E58), nothing else writes r15 before 00330F7A test r15d, r15d, and
     00330F7D jle goes to 003315E7, the epilogue (cookie check, add rsp, pops, ret)
  E  ONE ENTRY: one pdata range covers the body (003306E0..0033160A); inside it no jump from before the gate lands after it and
     no jump is indirect; no rel32 call/jmp/jcc from outside the body lands in 00330F7E..003315E7; the body's one rel32
     caller is 00330029
  D  THE .dbg AND .sbn NAMES: rbp+0x720 and rbp+0x830 get the extensions at 00D10994 "dbg" and 00D10998 "sbn" and are passed
     only to two size queries (00330E5B, 00330E6C) whose eax is overwritten by the next query before any read
  M  THE 0x10 LOOP: esi 0..15 formats "m%02d" (00D109CC) and appends ".mld" (00D109D4), so it names <stem>.mNN.mld at
     rbp+0xD80 + 0x104*i, and its sizes go to rsp+0x60 + 4*i (00330F40..00330F5E)
  T  THE STRINGS AFTER vld (the companions page's "whether the nine strings after vld belong to the same consumer"): every
     rip-relative reference from the body into 00D10990..00D10A14, in order - the extensions bin..vld before the gate, m%02d
     and .mld in the loop, and the six tags CAMDAT CAMCTL SHKDAT SHKCTL CHRMDL LGTDAT after the gate (each after an
     atelload.c allocation tag). The ninth, PREFIX (00D10A0C), is not referenced from the body: its reference is 0032F67C, the
     tag of another loader's buffer, whose size query 0032F617 is kind 8 (ecx = rdi + 8 after the loop counts rdi to 0),
     index 0x350
  C  CONTROL: the same kind reader finds kind 0x20 at the 0032E400 call 002E61A8, so Q does not read 0xFF by construction
Usage: python sibling_gate.py
"""
import hashlib, os, re, struct, sys
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
EXEP = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
d = open(EXEP, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = pefile.PE(EXEP)
off = lambda v: pe.get_offset_from_rva(v - B)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
def dis(lo, hi): return [(x.address, x.mnemonic, x.op_str) for x in cs.disasm(d[off(lo):off(hi)], lo)]
F0, F1, GATE_LO, EPI = 0x3306E0, 0x33160A, 0x330F7E, 0x3315E7
body = dis(F0, F1)
A = {a: (m, o) for a, m, o in body}
def kind_before(ins, k):
    for a, m, o in reversed(ins[max(0, k - 3):k]):
        if o.startswith("ecx, "): return o[5:]
    return None
calls = [k for k, (a, m, o) in enumerate(body) if m == "call" and o == "0x32e400"]
kinds = [kind_before(body, k) for k in calls]
qbody = dis(0x32E400, 0x32E450)
QA = {a: (m, o) for a, m, o in qbody}
check("Q", body[-1][0] < F1 and len(calls) == 14 and all(k == "0xff" for k in kinds)
      and QA.get(0x32E404) == ("cmp", "ecx, 0xff") and QA.get(0x32E40A) == ("je", "0x32e438") and QA.get(0x32E438) == ("or", "eax, 0xffffffff")
      and QA.get(0x32E43B) == ("test", "eax, eax") and QA.get(0x32E43D) == ("jle", "0x32e44b") and QA.get(0x32E44F) == ("ret", ""),
      "%d direct 0032E400 calls, kinds %s; kind 0xFF returns -1 before rdx is read" % (len(calls), sorted(set(kinds))))
r15w = [a for a, m, o in body if 0x330E58 < a < 0x330F7A and re.match(r"r15[dwb]?\b", o)]
epi = [A.get(a) for a in (0x3315E7, 0x3315EE, 0x3315F1, 0x3315F6)]
check("G", A.get(0x330E47) == ("call", "0x32e400") and A.get(0x330E58) == ("mov", "r15d, eax") and not r15w
      and A.get(0x330F7A) == ("test", "r15d, r15d") and A.get(0x330F7D) == ("jle", "0x3315e7")
      and epi == [("mov", "rcx, qword ptr [rbp + 0x1dc0]"), ("xor", "rcx, rsp"), ("call", "0x808c40"), ("add", "rsp, 0x1ed8")]
      and [m for a, m, o in body if a >= 0x3315FD][:9] == ["pop"] * 8 + ["ret"],
      "first query -> r15d; test r15d / jle 003315E7 (epilogue); no other r15 write before the gate")
ex = pe.OPTIONAL_HEADER.DATA_DIRECTORY[3]; pd = pe.get_data(ex.VirtualAddress, ex.Size)
rf = [struct.unpack_from("<III", pd, i) for i in range(0, len(pd) - 11, 12)]
cover = [(b + B, e + B) for b, e, u in rf if b + B < F1 and e + B > F0]
cross, indirect = [], []
for a, m, o in body:
    if m.startswith("j"):
        if not re.fullmatch(r"0x[0-9a-f]+", o): indirect.append(a); continue
        t = int(o, 16)
        if (a < 0x330F7A and t > 0x330F7D) or not (F0 <= t < F1): cross.append((a, t))
outside, callers = [], []
for s in pe.sections:
    if not s.Name.startswith(b".text"): continue
    base = B + s.VirtualAddress; buf = d[s.PointerToRawData:s.PointerToRawData + s.SizeOfRawData]
    for mm in re.finditer(rb"[\xE8\xE9]|\x0F[\x80-\x8F]", buf, re.S):
        i = mm.end()
        if i + 4 > len(buf): continue
        t = base + i + 4 + struct.unpack_from("<i", buf, i)[0]; src = base + mm.start()
        if F0 <= src < F1: continue
        if GATE_LO <= t < EPI: outside.append(src)
        if t == F0 and buf[mm.start()] == 0xE8: callers.append(src)
check("E", cover == [(F0, F1)] and not cross and not indirect and not outside and callers == [0x330029],
      "pdata %s; in-body gate crossings %d, indirect jumps %d; outside rel32 into the gated range %d; rel32 callers %s"
      % ([(hex(a), hex(b)) for a, b in cover], len(cross), len(indirect), len(outside), [hex(c) for c in callers]))
def cstr(v): o = off(v); return d[o:d.index(b"\0", o)].decode()
seq = lambda lo, hi: [(m, o) for a, m, o in body if lo <= a < hi]
check("D", cstr(0xD10994) == "dbg" and cstr(0xD10998) == "sbn"
      and A.get(0x330819) == ("lea", "rdx, [rip + 0x9e0174]") and 0x330819 + 7 + 0x9E0174 == 0xD10994
      and A.get(0x3308A9) == ("lea", "rdx, [rip + 0x9e00e8]") and 0x3308A9 + 7 + 0x9E00E8 == 0xD10998
      and [a for a, m, o in body if "rbp + 0x720" in o and m == "lea" and a > 0x330900] == [0x330E4C]
      and [a for a, m, o in body if "rbp + 0x830" in o and m == "lea" and a > 0x330900] == [0x330E60]
      and seq(0x330E5B, 0x330E71) == [("call", "0x32e400"), ("lea", "rdx, [rbp + 0x830]"), ("mov", "ecx, 0xff"), ("call", "0x32e400")]
      and seq(0x330E6C, 0x330E82) == [("call", "0x32e400"), ("lea", "rdx, [rbp + 0xc0]"), ("mov", "ecx, 0xff"), ("call", "0x32e400")],
      "the dbg and sbn names reach only 00330E5B / 00330E6C, and each result is overwritten by the next query unread")
check("M", cstr(0xD109CC) == "m%02d" and cstr(0xD109D4) == ".mld"
      and A.get(0x330D53) == ("xor", "esi, esi") and A.get(0x330D5C) == ("lea", "rbx, [rbp + 0xd80]")
      and A.get(0x330D73) == ("lea", "rdx, [rip + 0x9dfc52]") and 0x330D7A + 0x9DFC52 == 0xD109CC
      and A.get(0x330E1A) == ("mov", "eax, dword ptr [rip + 0x9dfbb4]") and 0x330E20 + 0x9DFBB4 == 0xD109D4
      and A.get(0x330E24) == ("add", "rbx, 0x104") and A.get(0x330E35) == ("cmp", "esi, 0x10") and A.get(0x330E38) == ("jl", "0x330d70")
      and A.get(0x330F2D) == ("mov", "esi, 0x10") and A.get(0x330F32) == ("lea", "rdi, [rbp + 0xd80]") and A.get(0x330F4D) == ("add", "rdi, 0x104")
      and A.get(0x330F54) == ("mov", "dword ptr [rbx], eax") and A.get(0x330F56) == ("lea", "rbx, [rbx + 4]"),
      "sixteen names <stem>.mNN.mld (0x104 apart), sixteen sizes to rsp+0x60")
refs = []
for k, (a, m, o) in enumerate(body[:-1]):
    mm = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", o)
    if mm:
        t = body[k + 1][0] + int(mm.group(2), 16) * (1 if mm.group(1) == "+" else -1)
        if 0xD10990 <= t < 0xD10A14: refs.append((a, cstr(t)))
EXT = ["bin", "dbg", "sbn", "msb", "msf", "fnt", "cam", "camera", "lgt", "camera", "cml", "cmi", "shk", "camera", "skl", "vld"]
TAGS = ["CAMDAT", "CAMCTL", "SHKDAT", "SHKCTL", "CHRMDL", "LGTDAT"]
names = [s for a, s in refs]
pre = dis(0x32F5F8, 0x32F68B)
PA = {a: (m, o) for a, m, o in pre}
check("T", names == EXT + ["m%02d", ".mld", ""] + TAGS and all(a < 0x330F7A for a, s in refs[:19]) and all(a > 0x330F7D for a, s in refs[19:])
      and cstr(0xD10A0C) == "PREFIX" and "PREFIX" not in names
      and PA.get(0x32F5F8) == ("sub", "rdi, 1") and PA.get(0x32F5FC) == ("jne", "0x32f520") and PA.get(0x32F602) == ("mov", "edx, 0x350")
      and PA.get(0x32F60E) == ("lea", "ecx, [rdi + 8]") and PA.get(0x32F617) == ("call", "0x32e400")
      and PA.get(0x32F67C) == ("lea", "rdx, [rip + 0x9e1389]") and 0x32F683 + 0x9E1389 == 0xD10A0C,
      "the body makes %d extension references (14 strings) and names m%%02d/.mld before the gate and the six tags after it; PREFIX is 0032F67C's, "
      "another loader's tag, whose size query 0032F617 is kind 8, index 0x350" % len(EXT))
ctl = dis(0x2E61A3, 0x2E61AD)
ck = [kind_before(ctl, k) for k, (a, m, o) in enumerate(ctl) if m == "call" and o == "0x32e400"]
check("C", ck == ["0x20"], "the same reader gives kind %s at the 0032E400 call 002E61A8" % ck)
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
