#!/usr/bin/env python3
"""gi4_mask800.py - GI-4 residue (FABLE, 2026-09-29): what the confirm window's +0x630 mask 0x800 does.

Checks from the shipping EXE:
  A. the mask's one producer: of the three flag words passed to 0057C380, only the Yes/No question's 0xC812 carries 0x800;
  B. the mask sets the list child's +0xE4 bit 0x80 (0057C7CC); every list is built with bit 0x40 already set (002D14E0);
  C. the list's reconcile arm (002D2DB0, id 2 -> 002D37AE) walks from the list up the +0x10 parent chain: every node must
     have +0x40 bits 0 and 3; a node with +0x40 bit 9 and transition state (+0x7C signed low nibble) 2 arms the hold when
     the list has bit 0x40, state 4 when it has bit 0x80; states 0/1 end the walk; the focused widget (00244820 ->
     0208EBC0) must be on the chain; then 002D4330(list, 1, 0, 0) runs;
  D. 002D4330 only builds a position record for the list's current row and hands it to the hand-pointer step 00368360;
  E. +0x40 bit 3: set on every widget by the constructor (0x80A at 00246653), and the confirm window clears its own bit 3
     on both ways out (0057CAE9, reached from the cancel post and from a pick the owner did not claim); the Yes/No host
     002CDF20 always answers 0 and closes itself only from its id-2 arm after an answer (+0xD8 == 1).
Positive control for the bit-3 writer census: 005668AA. Exit status 1 on any failed check.
"""
import struct, sys, re
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
FUNCS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\graph\functions.tsv"
BASE = 0x120000
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]; nsec = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(nsec):
    o = pe + 24 + opt + i * 40
    secs.append((struct.unpack_from("<I", d, o + 12)[0], struct.unpack_from("<I", d, o + 8)[0], struct.unpack_from("<I", d, o + 20)[0]))
def off(a):
    r = a - BASE
    for va, vs, ro in secs:
        if va <= r < va + vs: return ro + (r - va)
funcs = {}
for line in open(FUNCS, encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try: funcs[int(p[0], 16)] = int(p[2])
    except (ValueError, IndexError): pass
md = Cs(CS_ARCH_X86, CS_MODE_64)
def dis(fn): return list(md.disasm(d[off(fn):off(fn) + funcs[fn]], fn))
def ins(a): x = list(md.disasm(d[off(a):off(a) + 16], a))[0]; return f"{x.mnemonic} {x.op_str}"
fails = 0
def check(name, ok, detail=""):
    global fails
    print(("PASS " if ok else "FAIL ") + name + (" :: " + str(detail) if detail != "" else ""))
    if not ok: fails += 1

print("== A. producer")
edis = sorted({int(x.op_str.split(", ")[1], 16) for x in dis(0x2CE370) if x.mnemonic == "mov" and x.op_str.startswith("edi, 0x")})
words = {"002CDF20 Yes/No": 0xC812, "00566680 sort picker": 0x8036}
words.update({f"002CE370 notice {v:#x}": v for v in edis})
check("flag words read from the producers (0xC812 at 002CE086, 0x8036 at 00566939)",
      ins(0x2CE086) == "mov dword ptr [rsp + 0x48], 0xc812" and ins(0x566939) == "mov dword ptr [rsp + 0x40], 0x8036" and bool(edis))
check("only the Yes/No question's 0xC812 carries 0x800", [k for k, v in words.items() if v & 0x800] == ["002CDF20 Yes/No"], {k: hex(v) for k, v in words.items()})

print("== B. the list bit")
check("0057C7C0 tests 0x800 and 0057C7CC sets list +0xE4 bit 0x80",
      ins(0x57C7C0) == "test dword ptr [rsi + 0x630], 0x800" and ins(0x57C7CC) == "or dword ptr [rcx + 0xe4], 0x80")
check("every list is built with +0xE4 |= 0x2000050 (bit 0x40 on, 0x80 off) (002D1643)", ins(0x2D1643) == "or dword ptr [rbx + 0xe4], 0x2000050")
check("002D14E0 is the list constructor: 00244F50(0x150, 002D2DB0, 0)", ins(0x2D14ED) == "lea rdx, [rip + 0x18bc]" and 0x2D14F4 + 0x18BC == 0x2D2DB0)

print("== C. the reconcile walk in 002D2DB0")
check("id 2 -> 002D37AE (002D2DE8 / 002D2DEB)", ins(0x2D2DE8) == "sub ecx, 1" and ins(0x2D2DEB) == "je 0x2d37ae")
walk = {0x2D37C1: "test dword ptr [rbx + 0xe0], 0x10000", 0x2D37D1: "test byte ptr [rbx + 0xe4], 0xc0", 0x2D37DE: "call 0x244820",
        0x2D37FD: "and ecx, esi", 0x2D3801: "test r8b, 8", 0x2D3807: "bt r8d, 9", 0x2D380E: "mov eax, dword ptr [rdx + 0x7c]",
        0x2D3811: "shl eax, 0x1c", 0x2D3814: "sar eax, 0x1c", 0x2D381B: "cmp eax, esi", 0x2D381D: "jle 0x2d3868",
        0x2D381F: "cmp eax, 2", 0x2D3824: "cmp eax, 4", 0x2D3829: "test byte ptr [rbx + 0xe4], 0x80",
        0x2D3832: "test byte ptr [rbx + 0xe4], 0x40", 0x2D383E: "cmp rdx, r10", 0x2D3841: "mov rdx, qword ptr [rdx + 0x10]",
        0x2D3845: "cmove edi, esi", 0x2D3863: "call 0x2d4330"}
for a, s in walk.items(): check(f"{a:08X}: {s}", ins(a) == s, ins(a))
check("00244820 returns the focus top 0208EBC0", ins(0x244820).startswith("mov rax, qword ptr [rip") and 0x244827 + 0x1E4A399 == 0x208EBC0)
check("00248220 (attach) writes the parent into the child's +0x10 (00248267)", ins(0x248267) == "mov qword ptr [rdx + 0x10], rbx")

print("== D. 002D4330 places the hand pointer")
b = dis(0x2D4330)
stores = [x for x in b if x.mnemonic == "mov" and x.op_str.startswith(("dword ptr [rbx", "word ptr [rbx", "byte ptr [rbx", "qword ptr [rbx"))]
check("002D4330 writes no field of the list (selection untouched)", not stores, [f"{x.address:08X} {x.op_str}" for x in stores])
check("002D4330 ends in 00368360(list, &rec) (002D4557)", ins(0x2D4557) == "call 0x368360")
check("00368360 is the 022CBE30 pointer step (gate 0036836A)", ins(0x36836A).startswith("cmp word ptr [rip") and 0x368372 + 0x1F63ABE == 0x22CBE30)

print("== E. +0x40 bit 3")
check("constructor 002465F0 sets 0x80A (bits 1, 3, 11) at 00246653", ins(0x246653) == "or ecx, 0x80a")
clears = []
for fn in sorted(funcs):
    if not (0x121000 <= fn < 0x8C2000): continue
    try: xs = dis(fn)
    except Exception: continue
    for x in xs:
        m = re.match(r"dword ptr \[r\w+ \+ 0x40\], (0x[0-9a-f]+|\d+)$", x.op_str)
        if m and x.mnemonic == "or" and int(m.group(1), 0) & 8: clears.append(("set", x.address))
        if m and x.mnemonic == "and" and not int(m.group(1), 0) & 8: clears.append(("clear", x.address))
sets = [a for k, a in clears if k == "set"]; clr = [a for k, a in clears if k == "clear"]
check("positive control: the immediate-set census finds 005668AA", 0x5668AA in sets, [f"{a:08X}" for a in sets])
check("immediate clears of +0x40 bit 3: 0024194E, 0056683A, 0057CAE9 only", sorted(clr) == [0x24194E, 0x56683A, 0x57CAE9], [f"{a:08X}" for a in clr])
check("the confirm window reaches 0057CAE9 after the cancel post (0057CAE4) and after an unclaimed pick (0057CBF9 jne)",
      ins(0x57CAE4) == "call 0x247510" and ins(0x57CBF9) == "jne 0x57cae9")
check("the Yes/No host answers every pick with 0 (002CE189 / 002CE193)", ins(0x2CE189) == "mov dword ptr [rbx + 0xd8], 1" and ins(0x2CE193) == "xor eax, eax")
check("the host closes itself only from id 2 once +0xD8 == 1 (002CE197 ... 002CE1BA)", ins(0x2CE197) == "cmp dword ptr [rbx + 0xd8], 1" and ins(0x2CE1BA) == "call 0x244f00")
print("== F. the outside closer")
check("002CE2D0 destroys the host registered at [0209AC30]+0x2E8 unless its +0x7C bit 0x20 is set",
      ins(0x2CE2D7) == "mov rcx, qword ptr [rax + 0x2e8]" and ins(0x2CE2E3) == "test byte ptr [rcx + 0x7c], 0x20" and ins(0x2CE2E7) == "je 0x244f00")
check("the Yes/No host registers itself in that slot (002CDF6C) and so does the notice host (002CE48A)",
      ins(0x2CDF6C) == "mov qword ptr [rax + 0x2e8], rbx" and ins(0x2CE48A) == "mov qword ptr [rax + 0x2e8], rbp")
callers = []
for fn in sorted(funcs):
    if not (0x121000 <= fn < 0x8C2000): continue
    try: xs = dis(fn)
    except Exception: continue
    callers += [x.address for x in xs if x.mnemonic in ("call", "jmp") and x.op_str == "0x2ce2d0"]
check("002CE2D0 is called from the license screens only: 0055C7EF, 0055D557, 0055D667, 0055D7C2, 0055F4B1",
      callers == [0x55C7EF, 0x55D557, 0x55D667, 0x55D7C2, 0x55F4B1], [f"{a:08X}" for a in callers])
print(f"FAILS {fails}")
sys.exit(1 if fails else 0)
