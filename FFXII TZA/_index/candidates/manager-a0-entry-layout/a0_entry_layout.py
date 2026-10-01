"""ManagerSub00A0Entry (0x100, 64 inline at ManagerSub0209BE80_00A0 +0x20): its layout from its own initialiser, reset
and list code (OPUS, 2026-09-27). Control. Static.

Corrects OPUS's own declaration of 2026-09-18. It read +0x00 'ptr0000' and +0x10 'ptr0010' from 003F12A0 / 003F12A8,
but those instructions address the LIST HEAD 003F1290 is given in rcx, not the entry. It also called +0x18..+0xFF
'unobservedTail0018 - no access', yet the entry's own initialiser writes most of that span.
  L1 the entry is the NODE of an intrusive list: 003F8C70 calls 003F1290(rcx = its caller's list head, rdx = parent
     + 0x20 + (i << 8)); 003F1290 writes the node's +0xD0 (next) / +0xD8 (prev) and the HEAD's +0x00 (first) / +0x10
     (last) - so +0x00 / +0x10 of the entry are not those pointers
  L2 +0x00..+0x0F is a float vector with w = 1.0: 003F9390 calls 00270260 with rcx = the entry (003F9561 / 003F956E),
     which stores floats at [rcx], [rcx+4], [rcx+8] and 1.0 at [rcx+0xC]
  L3 the reset 003F00F0 (only caller: 003F9390, rcx = the entry): +0x10 and +0x70 16-byte constants (so +0x10 covers +0x18), +0x60 / +0x6C
     cos(a), +0x64 sin(a), +0x68 -sin(a) through the cosf / sinf imports (00861F08 / 00861F0E), +0x0C 1.0, +0x80 0,
     +0xEC -1, +0xF0 0; 003F1230(entry, a) rewrites only +0x60..+0x6C
  L4 the initialiser 003F9390 forms the entry as parent + 0x20 + (i << 8) and writes +0x20 (qword), +0x28 (qword 6),
     +0x30 (16 bytes copied from the parent by 00202C90), +0x40 / +0x44 / +0x48 (0xFF), +0x4C, +0x50..+0x5C (-0.25,
     -0.25, 0.25, 0.25), +0xE0 (the parent's +0x52B8 qword), +0xE8 (word 0), +0xEC, +0xF0
  L5 STORE REGRESSION: the store no longer carries ptr0000 / ptr0010 as void* or an unobserved tail over +0x18..+0xFF,
     and it has the list links at +0xD0 / +0xD8
Not claimed: what the vectors, the 0xFF triple or the rectangle mean; the list head's type; +0x84..+0xCF,
+0xEA, +0xF4..+0xFF (no access found).
"""
import os, re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]; DB = HERE.parents[2]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes(); BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
sizes = {}
for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8"):
    c = l.split("\t")
    try: sizes[int(c[0], 16)] = int(c[2])
    except ValueError: pass
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def I(f): return {x.address: "%s %s" % (x.mnemonic, x.op_str) for x in cs.disasm(d[off(f):off(f) + sizes[f]], f)}
def imp(t):
    x = next(cs.disasm(d[off(t):off(t) + 6], t)); iat = t + 6 + struct.unpack_from("<i", d, off(t) + 2)[0]
    rva = struct.unpack_from("<Q", d, off(iat))[0]
    return d[off(BASE + rva + 2):off(BASE + rva + 2) + 16].split(b"\0")[0].decode()
def callers(t):
    out = set()
    for vs, va, rs, ro in SECS[:1]:
        for p in range(ro, ro + rs - 5):
            if d[p] == 0xE8 and BASE + va + p - ro + 5 + struct.unpack_from("<i", d, p + 1)[0] == t: out.add(BASE + va + p - ro)
    return out
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

A, H = I(0x3F8C70), I(0x3F1290)
check("L1 the entry is 003F1290's NODE (+0xD0 next, +0xD8 prev); +0x00 / +0x10 there are the HEAD's",
      A.get(0x3F8C89) == "mov rbp, rdx" and A.get(0x3F8CB3) == "lea rdx, [rdi + 0x20]" and A.get(0x3F8CB7) == "shl rax, 8"
      and A.get(0x3F8CBB) == "mov rcx, rbp" and A.get(0x3F8CBE) == "add rdx, rax" and A.get(0x3F8CC1) == "call 0x3f1290"
      and H.get(0x3F1292) == "mov qword ptr [rdx + 0xd0], rax" and H.get(0x3F1299) == "mov qword ptr [rdx + 0xd8], rax"
      and H.get(0x3F12A0) == "cmp qword ptr [rcx], rax" and H.get(0x3F12A8) == "mov qword ptr [rcx + 0x10], rdx"
      and H.get(0x3F12BC) == "mov qword ptr [rdx + 0xd8], rax")
N, L = I(0x3F9390), I(0x270260)
check("L2 +0x00..+0x0F is a float vector with w = 1.0 (00270260 on the entry)",
      N.get(0x3F9561) == "mov rcx, rdi" and N.get(0x3F956E) == "call 0x270260"
      and L.get(0x270282) == "mov rdi, rcx" and L.get(0x27029C) == "movss dword ptr [rcx], xmm1"
      and L.get(0x2702B3) == "movss dword ptr [rcx + 4], xmm0" and L.get(0x2702D2) == "movss dword ptr [rcx + 8], xmm2"
      and L.get(0x2702CB) == "mov dword ptr [rcx + 0xc], 0x3f800000")
R, T = I(0x3F00F0), I(0x3F1230)
check("L3 the reset 003F00F0 (its one caller passes the entry): vectors at +0x10 / +0x70, cos / sin / -sin / cos at"
      " +0x60..+0x6C, +0x0C 1.0, +0x80 0, +0xEC -1, +0xF0 0; 003F1230 rewrites only the four",
      callers(0x3F00F0) == {0x3F953E} and N.get(0x3F953B) == "mov rcx, rdi"
      and imp(0x861F08) == "cosf" and imp(0x861F0E) == "sinf"
      and R.get(0x3F0101) == "call 0x861f08" and R.get(0x3F010C) == "call 0x861f0e"
      and R.get(0x3F011F) == "movss dword ptr [rbx + 0x60], xmm6" and R.get(0x3F0124) == "movss dword ptr [rbx + 0x6c], xmm6"
      and R.get(0x3F0111) == "movss dword ptr [rbx + 0x64], xmm0" and R.get(0x3F012E) == "movss dword ptr [rbx + 0x68], xmm0"
      and R.get(0x3F0118, "").startswith("xorps xmm0, xmmword ptr [rip")
      and R.get(0x3F0133) == "mov dword ptr [rbx + 0xc], 0x3f800000" and R.get(0x3F013A) == "mov dword ptr [rbx + 0x80], eax"
      and R.get(0x3F0147) == "movups xmmword ptr [rbx + 0x70], xmm0" and R.get(0x3F0162) == "movups xmmword ptr [rbx + 0x10], xmm1"
      and R.get(0x3F0152) == "mov dword ptr [rbx + 0xec], 0xffffffff" and R.get(0x3F015C) == "mov dword ptr [rbx + 0xf0], eax"
      and sorted(int(m, 16) for v in T.values() for m in re.findall(r"\[rbx \+ (0x[0-9a-f]+)\]", v)) == [0x60, 0x64, 0x68, 0x6C])
W = {"+0x20": N.get(0x3F95E9) == "mov qword ptr [rdi + 0x20], rdx", "+0x28": N.get(0x3F95F0) == "mov qword ptr [rdi + 0x28], 6",
     "+0x30": N.get(0x3F95E1) == "lea rcx, [rdi + 0x30]" and N.get(0x3F95ED) == "mov rdx, rsi" and N.get(0x3F961E) == "call 0x202c90",
     "+0x40": N.get(0x3F9629) == "mov dword ptr [rdi + 0x40], 0xff", "+0x44": N.get(0x3F9630) == "mov dword ptr [rdi + 0x44], 0xff",
     "+0x48": N.get(0x3F9637) == "mov dword ptr [rdi + 0x48], 0xff", "+0x4C": N.get(0x3F9623) == "mov dword ptr [rdi + 0x4c], ebx",
     "+0x50": N.get(0x3F963E) == "mov dword ptr [rdi + 0x50], 0xbe800000", "+0x5C": N.get(0x3F9653) == "mov dword ptr [rdi + 0x5c], 0x3e800000",
     "+0xE0": N.get(0x3F965A) == "mov rax, qword ptr [rsi + 0x52b8]" and N.get(0x3F9661) == "mov qword ptr [rdi + 0xe0], rax",
     "+0xE8": N.get(0x3F9668) == "mov word ptr [rdi + 0xe8], r10w", "+0xEC": N.get(0x3F9610) == "mov dword ptr [rdi + 0xec], eax",
     "+0xF0": N.get(0x3F9606) == "mov dword ptr [rdi + 0xf0], 0",
     "entry": N.get(0x3F9530) == "shl rax, 8" and N.get(0x3F9534) == "lea rdi, [rsi + 0x20]" and N.get(0x3F9538) == "add rdi, rax"}
check("L4 the initialiser 003F9390 writes the entry's +0x20..+0xF0 fields", all(W.values()), str([k for k, v in W.items() if not v]))
rows = {}
for l in open(os.environ.get("FIELDS_PATH") or DB / "_types/fields.tsv", encoding="utf-8"):
    c = l.rstrip("\r\n").split("\t")
    if len(c) == 9 and c[0] == "ManagerSub00A0Entry": rows[int(c[1], 16)] = c
bad = [c[3] for c in rows.values() if (c[3] in ("ptr0000", "ptr0010") and c[4] == "void*") or (int(c[1], 16) <= 0x18 and int(c[2]) >= 0xE8)]
check("L5 STORE REGRESSION: no ptr0000 / ptr0010 void* rows, no unobserved tail over +0x18..+0xFF, list links at +0xD0 / +0xD8",
      not bad and 0xD0 in rows and 0xD8 in rows, "offending %s; +0xD0 %s" % (bad, 0xD0 in rows))
print("FAILS", fails)
sys.exit(1 if fails else 0)
