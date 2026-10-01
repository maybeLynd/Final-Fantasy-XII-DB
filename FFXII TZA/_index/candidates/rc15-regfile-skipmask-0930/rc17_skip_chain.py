"""rc17_skip_chain.py - RC-17: the skip chain read from the image, each link asserted. ORACLE, 2026-09-30. Static.

Checks (each prints PASS/FAIL):
 K1 verb 0x539 (= 1337, skipexec) result handler 0034ECF0 pops n and tail-jumps 00360710 with edx = owner byte +0x15;
    verb 0x51A (skipstart) handler 0034D3A0 calls 00360980(n, byte +0x15, word +0); verb 0x51C (skipcheck) handler
    0034F160 returns 003604A0(n, +0x15) = dword [022CB738 + (n + m*8)*16] (the entry's +8 "begun" flag).
 K2 00360710 refuses m == 0, addresses entry 022CB730 + (n + m*8)*16, moves the entry bit from the registered mask
    022CB9C0 + m*4 to the begun mask 022CB9D8 + m*4, and calls 0026A5B0(m, 1, n) (the +0x201 bit setter).
 K3 0026A5B0 and 00267310 address 02098E10 + m*0x288 + 0x201 (the skip mask); 00360980 sets the registered bit.
 K4 00360880 walks the registered masks for m = 1..3 (022CB9C4 + 4k) and calls 00360710 once per manager, with the
    LOWEST set bit n < 8.
 K5 00360880's only rel32 caller is 00228130 (at 002281B7); 00228130 has no rel32 caller and one rip reference, in
    00228700 (the procedure installed by the widget factory 00244F50), and runs 00360880 only in its message-18 arm
    when bit 13 of dword [[0209AC30] + 0x400] is set, clearing the bit after.
 K6 bit 13 of that dword: the only instruction image-wide that writes it with a variable is 00285EA0 (sets it to
    the argument's bit 0); 00285EA0's only rel32 caller is 0022917A in the pause-menu procedure 00228C70, message 2,
    state 4 (jump table 002294EC), with ecx = 1.
Paths are relative to this folder; image and function extents come through ../k14-closure-stores-0930.
"""
import os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "k14-closure-stores-0930"))
import k14_actorflow as K  # noqa: E402
from capstone import x86 as X  # noqa: E402
R = K.R
FAILS = 0


def ins(f):
    return list(R.md.disasm(R.at(f, K.ext[f]), f))


def rip(i):
    for op in i.operands:
        if op.type == X.X86_OP_MEM and op.mem.base == X.X86_REG_RIP:
            return i.address + i.size + op.mem.disp
    return None


def check(ok, name):
    global FAILS
    print("%s  %s" % ("PASS" if ok else "FAIL", name))
    FAILS += not ok


CALLS = {}
RIPREFS = {}
for f in sorted(K.ext):
    for i in R.md.disasm(R.at(f, K.ext[f]), f):
        if i.mnemonic in ("call", "jmp") and i.op_str.startswith("0x"):
            CALLS.setdefault(int(i.op_str, 16), []).append((f, i.address, i.mnemonic))
        t = rip(i)
        if t is not None:
            RIPREFS.setdefault(t, []).append((f, i.address, i.mnemonic))

# verb table rows
p = os.path.join(HERE, "..", "..", "..", "01-Script-VM-Native-Bridge", "Verb-Dispatch", "scriptvm-verb-table.tsv")
rows = {l.split("\t")[0]: l.split("\t") for l in open(p, encoding="utf-8").read().splitlines()[1:]}
check(rows["0539"][3] == "skipexec" and rows["0539"][13] == "0034ECF0" and 0x539 == 1337, "K1a verb 0539 = 1337 = skipexec, result 0034ECF0")
check(rows["051A"][3] == "skipstart" and rows["051A"][10] == "0034D3A0", "K1b verb 051A = skipstart, begin 0034D3A0")
check(rows["051C"][3] == "skipcheck" and rows["051C"][13] == "0034F160", "K1c verb 051C = skipcheck, result 0034F160")
a = [(i.mnemonic, i.op_str) for i in ins(0x0034ECF0)]
check(("movzx", "edx, byte ptr [rbx + 0x15]") in a and ("jmp", "0x360710") in a, "K1d 0034ECF0 -> jmp 00360710, edx = owner +0x15")
a = [(i.mnemonic, i.op_str) for i in ins(0x0034D3A0)]
check(("call", "0x360980") in a and ("movzx", "edx, byte ptr [rbx + 0x15]") in a and ("movzx", "r8d, word ptr [rbx]") in a,
      "K1e 0034D3A0 -> 00360980(n, +0x15, word +0)")
a = [(i.mnemonic, i.op_str) for i in ins(0x0034F160)]
b = ins(0x003604A0)
check(("call", "0x3604a0") in a and any(rip(i) == 0x022CB738 for i in b), "K1f skipcheck returns dword [022CB738 + (n+m*8)*16]")

s = ins(0x00360710)
check(any(i.mnemonic == "test" and i.op_str == "edx, edx" for i in s[:10]) and s[8].mnemonic == "jne" and s[9].op_str == "eax, eax",
      "K2a 00360710 returns 0 at once when m == 0 (test edx, edx / jne / xor eax, eax)")
check(any(rip(i) == 0x022CB730 for i in s), "K2b entry base 022CB730")
disps = set(i.operands[0].mem.disp for i in s if i.mnemonic in ("or", "and") and i.operands[0].type == X.X86_OP_MEM)
check({0x21AB9D8, 0x21AB9C0} <= disps, "K2c or into 022CB9D8 + m*4 (begun), and-not into 022CB9C0 + m*4 (registered)")
check(any(i.mnemonic == "call" and i.op_str == "0x26a5b0" for i in s), "K2d calls 0026A5B0(m, 1, n)")
check(any(rip(i) == 0x02098E10 for i in ins(0x0026A5B0)) and any(i.op_str.endswith("+ 0x201]") for i in ins(0x0026A5B0)),
      "K3a 0026A5B0 writes 02098E10 + m*0x288 + 0x201")
check(any(rip(i) == 0x02099011 for i in ins(0x00267310)), "K3b 00267310 reads 02098E10 + 0x201 + m*0x288")
t = ins(0x00360980)
check(any(i.mnemonic == "or" and i.operands[0].type == X.X86_OP_MEM and i.operands[0].mem.disp == 0x21AB9C0 for i in t),
      "K3c 00360980 sets the registered bit (022CB9C0 + m*4)")
l = ins(0x00360880)
check(any(rip(i) == 0x022CB9C4 for i in l) and any(i.op_str == "ebx, 3" for i in l) and any(i.op_str == "ebx, 1" for i in l)
      and any(i.mnemonic == "bt" for i in l) and sum(1 for i in l if i.mnemonic == "call") == 1,
      "K4 00360880: m = 1..3 over 022CB9C4 + 4(m-1), first set bit < 8, one 00360710 call per m")
check([c[1] for c in CALLS.get(0x00360880, [])] == [0x002281B7], "K5a only rel32 caller of 00360880 is 002281B7 (in 00228130)")
check(not CALLS.get(0x00228130) and [r[0] for r in RIPREFS.get(0x00228130, [])] == [0x00228700], "K5b 00228130: no rel32 caller; one rip reference, in 00228700")
m = ins(0x00228130)
k = [i.address for i in m]
check(any(i.mnemonic == "bt" and i.op_str == "eax, 0xd" for i in m) and
      any(i.mnemonic == "and" and "0xffffdfff" in i.op_str and i.address == 0x002281C3 for i in m),
      "K5c message-18 arm: bt 13 then 00360880, then clear bit 13 (002281C3)")
# K6: who writes bit 13 of +0x400 with a variable / immediate
w = []
for f in sorted(K.ext):
    for i in R.md.disasm(R.at(f, K.ext[f]), f):
        if i.operands and i.operands[0].type == X.X86_OP_MEM and i.operands[0].mem.disp == 0x400 and i.operands[0].size >= 2:
            if i.mnemonic in ("or", "xor", "mov", "bts", "btc", "add") and (len(i.operands) < 2 or i.operands[1].type != X.X86_OP_IMM
                                                                        or (i.operands[1].imm & 0x2000) or i.mnemonic == "mov"):
                w.append((f, i.address, i.mnemonic, i.op_str))
print("  writes at disp 0x400 (word or wider) that can set bit 13: %s" % "; ".join("%08X %08X %s %s" % x for x in w))
ctxf = set(r[0] for r in RIPREFS.get(0x0209AC30, []))
print("  of them in functions that reference 0209AC30: %s" % " ".join("%08X" % x[1] for x in w if x[0] in ctxf))
check([x[1] for x in w if x[0] in ctxf] == [0x00285EB6], "K6a among functions referencing 0209AC30, only 00285EA0 (00285EB6) can set bit 13 of +0x400")
check([c[1] for c in CALLS.get(0x00285EA0, [])] == [0x0022917A], "K6b only rel32 caller of 00285EA0 is 0022917A (00228C70)")
jt = [0x120000 + struct.unpack_from("<I", R.at(0x002294EC, 28), 4 * k)[0] for k in range(7)]
check(jt[3] == 0x00229159, "K6c 0022917A lies in 00228C70 message-2 state 4 (table 002294EC entry 4 = 00229159)")
print("FAILS %d" % FAILS)
sys.exit(1 if FAILS else 0)
