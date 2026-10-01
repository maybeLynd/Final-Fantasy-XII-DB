"""RC-28 leftover: does a refused .btm request still fire its completion callback 00364380? (SWE2-DATA 2026-09-30)
Static, instruction pins in the certified image plus the shipped FileSizeTables. Reads only.

Chain pinned below:
  F  FileSizeTable_KR/_CN hold -1 for kind 7 ids 0xDA..0xDF (the six .btm); US holds sizes (control).
  A  00365810 sizes with 0032E400 (a -1 entry comes back unrounded) and allocates through 00249810 / 002497E0 ->
     0036A190 / 0036A100 -> 0036BC60, which clamps a negative size to 0 before rounding to 64 (0036BC89-0036BC9D).
  D  00365810's request descriptor on its stack: +0x08 = row (n - 1), +0x10 = 00364380; 0032E620 copies it and hands it
     to 0032E870, which stores slot +0x40 = descriptor +0x10 (the callback), +0x60 = descriptor +0x08, +0x28 = the byte
     count (-1 here), +0x38 / +0x70 = the destination, +0x22 = 0 (one-shot mode), +0x20 = 1 (state 1).
  P  the pump 0032E070: state 1 issues through 0046E030 -> 002DF780 whenever +0x28 != 0, and 0046E030 returns 1
     whatever the issuer did; the slot goes to state 2 (0032E0FF), then 3 (0032E149); state 3 waits only while the
     status word 0215EFF4 == -1 (0046DFE0) and then sets state 5 + (status < 0) (0032E19C-0032E1A8); mode 0 runs
     0032E330 for state 5 and 0032E370 for state 6 (0032E266-0032E285).
  C  0032E330 calls slot +0x40 (rcx = +0x60, rdx = +0x70, r8 = 1); 0032E370 calls it when +0x28 == -1 (r8 = 0).
  S  002DF780's refusal (entry == -1, 002DF7B0 / 002DF7B9 -> 002DF85D) returns before the only place it passes the status
     pointer (002DF808 / 002DF838); the status word 0215EFF4 is written only through that pointer: -1 at issue
     (001D6DD4, the archive job) and the job result at completion (001D6D70). So a refused read leaves the previous
     completed value, which is never -1 once the pump has completed that earlier request.
  B  00364380 sets bit cl (= row) of [022CBE00] + 0x240 and ignores r8; 003657E0(n) tests bit n - 1 of the same word.
Controls: K1 the rip sweep of 0215EFF4 finds its two known readers 0046DFE0 and 0046E0E0; K2 the pump's jump table
decodes to six addresses inside 0032E070; K3 FileSizeTable_US sizes the six .btm positively.
"""
import os, re, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
from pe import d, off, dis, raw_rip_refs, owner, funcs, BASE  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


def ins(fn):
    return {x.address: (x.mnemonic, x.op_str) for x in dis(fn)}


def has(body, addr, mn, op):
    got = body.get(addr)
    ok = got == (mn, op)
    if not ok:
        print("   mismatch %08X: got %s, want %s %s" % (addr, got, mn, op))
    return ok


# F
FST = r"D:/SteamLibrary/steamapps/common/FINAL FANTASY XII THE ZODIAC AGE/FileSizeTables"


def fst(lang):
    b = open(os.path.join(FST, "FileSizeTable_%s.fst" % lang), "rb").read()
    return [struct.unpack_from("<i", b, 4 * (7 * 5000 + i))[0] for i in range(0xDA, 0xE0)]


check("K3 control: FileSizeTable_US sizes the six .btm", all(v > 0 for v in fst("US")), str(fst("US")))
check("F  FileSizeTable_KR and _CN hold -1 for the six .btm", fst("KR") == [-1] * 6 and fst("CN") == [-1] * 6)

# A
s = ins(0x00365810)
check("A1 00365810 sizes with 0032E400(7, id) and allocates through 00249810 / 002497E0 with that size",
      has(s, 0x00365878, "mov", "ecx, 7") and has(s, 0x00365882, "call", "0x32e400") and has(s, 0x00365889, "mov", "edx, eax")
      and has(s, 0x00365895, "call", "0x249810") and has(s, 0x0036589C, "call", "0x2497e0"))
sz = ins(0x0032E400)
check("A2 0032E400 returns a non-positive size unrounded (jle)", has(sz, 0x0032E43D, "jle", "0x32e44b"))
h = ins(0x0036BC60)
check("A3 0036BC60 clamps a negative size to 0, then rounds up to 64 (so -1 allocates 0 bytes)",
      has(h, 0x0036BC89, "xor", "eax, eax") and has(h, 0x0036BC8D, "cmovns", "eax, edx")
      and has(h, 0x0036BC92, "add", "eax, 0x3f") and has(h, 0x0036BC9D, "and", "r14d, 0xffffffc0"))

# D
check("D1 00365810's descriptor: +0x10 = 00364380 (rsp+0x40), +0x08 = row n-1 (rsp+0x38), handed as arg 5 (rsp+0x20)",
      has(s, 0x00365837, "lea", "rax, [rip - 0x14be]") and has(s, 0x00365841, "mov", "qword ptr [rsp + 0x40], rax")
      and has(s, 0x0036582E, "dec", "ecx") and has(s, 0x00365871, "mov", "dword ptr [rsp + 0x38], ecx")
      and has(s, 0x003658BD, "lea", "rax, [rsp + 0x30]") and has(s, 0x003658C2, "mov", "qword ptr [rsp + 0x20], rax")
      and has(s, 0x003658C7, "call", "0x32e620"))
r = ins(0x0032E620)
check("D2 0032E620 copies the descriptor (arg 5) and passes it to 0032E870",
      has(r, 0x0032E65D, "mov", "rax, qword ptr [rsp + 0x90]") and has(r, 0x0032E678, "movups", "xmm0, xmmword ptr [rax]")
      and has(r, 0x0032E6B4, "lea", "rax, [rsp + 0x30]") and has(r, 0x0032E6C4, "mov", "qword ptr [rsp + 0x20], rax")
      and has(r, 0x0032E6DD, "call", "0x32e870"))
b = ins(0x0032E870)
check("D3 0032E870: +0x40 = desc+0x10, +0x60 = desc+8, +0x28 = byte count, +0x22 = 0, +0x20 = 1, +0x70 = destination",
      has(b, 0x0032E8DD, "mov", "r8, qword ptr [rcx + 0x10]") and has(b, 0x0032E8E5, "mov", "r11d, dword ptr [rcx + 8]")
      and has(b, 0x0032E951, "mov", "qword ptr [r10 + 0x40], r8") and has(b, 0x0032E961, "mov", "dword ptr [r10 + 0x60], r11d")
      and has(b, 0x0032E92C, "mov", "dword ptr [r10 + 0x28], esi") and has(b, 0x0032E88A, "mov", "esi, r9d")
      and has(b, 0x0032E969, "mov", "word ptr [r10 + 0x22], 0") and has(b, 0x0032E93B, "mov", "byte ptr [r10 + 0x20], r12b")
      and has(b, 0x0032E970, "mov", "qword ptr [r10 + 0x70], rdi"))

# P
p = ins(0x0032E070)
JT = BASE + 0x20E2D0
tab = [BASE + struct.unpack_from("<I", d, off(JT + 4 * i))[0] for i in range(6)]
print("   pump states 1..6 -> %s" % " ".join("%08X" % a for a in tab))
check("K2 control: the pump's jump table decodes to six addresses inside 0032E070",
      all(0x0032E070 <= a < 0x0032E070 + funcs[0x0032E070] for a in tab))
check("P1 state 1 issues through 0046E030 when +0x28 != 0, then state 2 unconditionally",
      tab[0] == 0x0032E0BD and has(p, 0x0032E0CE, "test", "r8d, r8d") and has(p, 0x0032E0F1, "call", "0x46e030")
      and has(p, 0x0032E0FF, "mov", "byte ptr [rbx + 0x20], 2"))
w = ins(0x0046E030)
check("P2 0046E030 calls 002DF780 and returns 1 whatever it returned", has(w, 0x0046E03E, "call", "0x2df780")
      and has(w, 0x0046E043, "mov", "eax, 1"))
check("P3 state 2 -> 3 (0032E15A); state 3 waits on 0046DFE0, then state = 5 + (status < 0)",
      tab[1] == 0x0032E149 and has(p, 0x0032E15A, "mov", "byte ptr [rbx + 0x20], 3") and tab[2] == 0x0032E163
      and has(p, 0x0032E163, "call", "0x46dfe0") and has(p, 0x0032E19C, "call", "0x46e0e0")
      and has(p, 0x0032E1A3, "sets", "al") and has(p, 0x0032E1A6, "add", "al, 5"))
q = ins(0x0046DFE0)
check("P4 0046DFE0 reports busy only while the status word 0215EFF4 is -1", has(q, 0x0046DFE7, "cmp", "dword ptr [rip + 0x1cf1006], -1")
      and has(q, 0x0046DFEE, "cmove", "eax, ecx"))
check("P5 mode 0 (+0x22 == 0) runs 0032E330 for state 5 and 0032E370 for state 6",
      has(p, 0x0032E1AB, "movzx", "ecx, byte ptr [rbx + 0x22]") and has(p, 0x0032E1B1, "je", "0x32e266")
      and has(p, 0x0032E266, "cmp", "byte ptr [rbx + 0x20], 5") and has(p, 0x0032E26F, "call", "0x32e330")
      and has(p, 0x0032E285, "call", "0x32e370"))

# C
c1, c2 = ins(0x0032E330), ins(0x0032E370)
check("C1 0032E330 calls +0x40 with rcx = +0x60, rdx = +0x70, r8 = 1",
      has(c1, 0x0032E336, "mov", "rax, qword ptr [rcx + 0x40]") and has(c1, 0x0032E346, "mov", "r8d, 1")
      and has(c1, 0x0032E34C, "mov", "ecx, dword ptr [rcx + 0x60]") and has(c1, 0x0032E34F, "call", "rax"))
check("C2 0032E370 calls +0x40 (r8 = 0) exactly when +0x28 == -1, the refused .btm's byte count",
      has(c2, 0x0032E382, "cmp", "dword ptr [rcx + 0x28], -1") and has(c2, 0x0032E386, "jne", "0x32e394")
      and has(c2, 0x0032E38C, "xor", "r8d, r8d") and has(c2, 0x0032E392, "call", "rax"))

# S
i = ins(0x002DF780)
check("S1 002DF780 refuses an FST entry of -1 (002DF7B0 / 002DF7B9) and returns 0 from 002DF85D",
      has(i, 0x002DF7B0, "cmp", "dword ptr [r15 + rax*4 + 0x2da3ee0], -1") and has(i, 0x002DF7B9, "je", "0x2df85d")
      and has(i, 0x002DF862, "xor", "eax, eax"))
refs = raw_rip_refs(0x0215EFF4, 0x0215EFF8)
for a, mn, op, t in refs:
    print("   0215EFF4 ref %08X %-4s %-44s in %08X" % (a, mn, op, owner(a) or 0))
readers = {owner(a) for a, mn, op, t in refs if mn != "lea"}
leas = sorted(a for a, mn, op, t in refs if mn == "lea")
check("K1 control: the sweep finds the two readers 0046DFE0 and 0046E0E0", {0x0046DFE0, 0x0046E0E0} <= readers)
check("S2 every other reference only passes the address (lea), and 002DF780's two are after its refusal branch",
      readers == {0x0046DFE0, 0x0046E0E0} and [a for a in leas if owner(a) == 0x002DF780] == [0x002DF808, 0x002DF838])
j = ins(0x001D6D90)
k = ins(0x001D6D70)
check("S3 the archive job writes -1 through the pointer at issue (001D6DD4) and its completion 001D6D70 writes the result",
      has(j, 0x001D6DD4, "mov", "dword ptr [rax], 0xffffffff") and has(k, 0x001D6D7C, "mov", "dword ptr [rax], ecx"))

# B
cb = ins(0x00364380)
rdy = ins(0x003657E0)
check("B1 00364380 sets bit cl of [022CBE00] + 0x240 and reads no r8",
      has(cb, 0x00364391, "shl", "eax, cl") and has(cb, 0x00364393, "or", "dword ptr [rdx + 0x240], eax")
      and not any("r8" in op for mn, op in cb.values()))
check("B2 003657E0(n) tests bit n - 1 of the same word", has(rdy, 0x003657ED, "dec", "ecx")
      and has(rdy, 0x003657F2, "mov", "ecx, dword ptr [rax + 0x240]") and has(rdy, 0x003657FA, "bt", "ecx, edx"))
print("RESULT a refused .btm request completes: state 5 (stale status >= 0) calls 00364380 with r8 = 1, state 6 "
      "(stale status < 0) calls it with r8 = 0 because the byte count is -1; either way the ready bit is set")
print("FAILS %d" % FAILS)
