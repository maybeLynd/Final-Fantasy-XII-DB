"""skip_mask.py - OV-15: the "actor-indexed control byte" some ScriptVM polls consult (FABLE, Claude Opus 5.5, 2026-09-29).
STATIC, certified image.

The byte is 02099011 + slot*0x288 = the actor-manager slot record (02098E10, stride 0x288) field +0x201, which the world-tick
page already identifies as the per-manager SKIP mask (bit k = request k is being skipped; a non-zero byte makes the tick run the
slot's sixteen sub-steps). This control ties that identity to the ScriptVM side:

  A  ACCESS CENSUS: every instruction in .text whose memory operand ends in "+ 0x201]" (found by searching the raw disp32 bytes
     and decoding backwards, so leaf functions without .pdata are included; a candidate is kept only if a linear decode from
     most starts 16..48 bytes earlier converge on it, which drops immediates such as `mov edx, 0x201` read from mid-instruction), plus
     every rip-relative reference to 02099011. Expected, and each read: the bind's zero store 0026CC38; the bit setter/clearer
     0026A5B0 (a byte read-modify-write: movzx, bts or btr, mov); the interpreter's read 0025E5C5; the manager-index reader
     00267310 (lea at 0026731A); and the record-pointer reader 00267300. Any other site fails A until it is read.
     (00264830, which looked like a reader, addresses 02099010 = +0x200: a different byte.)
  C  no image-base-relative displacement 0x1F79011; stores wider than a byte whose span covers +0x201 are LISTED (they may
     belong to other records; each listed one must be read before a writer claim is made)
  R  00267310(manager) returns byte [02098E10 + manager*0x288 + 0x201]; its rel32 call sites are counted (every form)
  W  THE WAIT POLL: family 0 command 0 has begin 0034CF90 and poll 0034DCC0 (table 01EED700 row 0, poll at +0x10 as the accessor
     003DC240 reads it). The poll decrements the countdown [r8]; negative -> 0 (done); otherwise it calls 00267310 with the target
     actor's manager byte +0x15 and, when that mask is non-zero, stores 0 to the countdown; returns 1 (running). So a skipped
     manager's waits end on their next poll
  I  THE INTERPRETER loads its own manager's mask (movzx edx, [r13+0x201] at 0025E5C5) before each opcode dispatch
  Not claimed: what each of the other 71 callers of 00267310 does with the mask; which requests a skip names in practice.
"""
import hashlib, os, struct, sys
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
TX = [s for s in SECS if s[0] == b".text"][0]
def off(v):
    for nm, vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def dis(a, b): return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(a):off(b)], a)}
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
at = lambda c, w: all(c.get(a) == s for a, s in w.items())
text = d[TX[4]:TX[4] + TX[3]]; tbase = B + TX[2]
# A: raw disp32 0x201 and rip-relative 02099011
found = {}
def aligned(s0):
    """True if most linear decodes started 16..48 bytes before s0 land exactly on s0 (x86 decoding self-synchronises, so
    true boundaries collect the majority; a boundary inside another instruction's immediate does not)."""
    hit = 0
    for st in range(s0 - 48, s0 - 16):
        for x in cs.disasm(text[st - tbase:s0 - tbase + 16], st):
            if x.address >= s0:
                hit += x.address == s0; break
    return hit * 2 > 32
pat = struct.pack("<I", 0x201)
i = text.find(pat)
while i != -1:
    for back in range(8, 0, -1):   # longest first, so a REX prefix is not dropped
        s0 = i - back
        ins = list(cs.disasm(text[s0:s0 + 15], tbase + s0, 1))
        if ins and ins[0].address + ins[0].size >= tbase + i + 4 and "+ 0x201]" in ins[0].op_str and aligned(tbase + s0):
            found[ins[0].address] = "%s %s" % (ins[0].mnemonic, ins[0].op_str); break
    i = text.find(pat, i + 1)
for j in range(len(text) - 4):
    r = struct.unpack_from("<i", text, j)[0]
    for extra in (0, 1, 4):
        if tbase + j + 4 + extra + r == 0x2099011:
            for back in range(7, 0, -1):
                ins = list(cs.disasm(text[j - back:j + 15], tbase + j - back, 1))
                if ins and "rip" in ins[0].op_str and ins[0].address + ins[0].size == tbase + j + 4 + extra:
                    found[ins[0].address] = "%s %s" % (ins[0].mnemonic, ins[0].op_str); break
want = {0x26CC38: "mov byte ptr [rdi + 0x201], bl", 0x25E5C5: "movzx edx, byte ptr [r13 + 0x201]",
        0x26A5C4: "movzx eax, byte ptr [rcx + 0x201]", 0x26A5D3: "mov byte ptr [rcx + 0x201], al",
        0x26A5DE: "mov byte ptr [rcx + 0x201], al", 0x267300: "movzx eax, byte ptr [rcx + 0x201]",
        0x26731A: "lea rax, [rip + 0x1e31cf0]"}
bits = dis(0x26A5B0, 0x26A5E5); rd = dis(0x267310, 0x267326)
A = found == want and bits.get(0x26A5CF) == "bts eax, r8d" and bits.get(0x26A5DA) == "btr eax, r8d"
check("A", A, "the +0x201 sites are exactly the seven read: %s" % A)
for a0 in sorted(found):
    print("      %08X  %s%s" % (a0, found[a0], "" if a0 in want else "   UNREAD"))
# C: stores wider than a byte whose span covers +0x201 (disp 0x1FA..0x200 with a 2/4/8/16-byte write), and image-base-relative
# forms (disp32 0x1F79011 or 0x1F78E10 with +0x201 applied through a register are covered by A's "+ 0x201]" only when folded)
cover = {}
for dsp in range(0x1FA, 0x201):
    pat2 = struct.pack("<I", dsp); k = text.find(pat2)
    while k != -1:
        for back in range(8, 0, -1):
            s0 = k - back
            ins = list(cs.disasm(text[s0:s0 + 15], tbase + s0, 1))
            if ins and ins[0].address + ins[0].size >= tbase + k + 4 and ("+ 0x%x]" % dsp) in ins[0].op_str and aligned(tbase + s0):
                o = ins[0].op_str; w = {"word": 2, "dword": 4, "qword": 8, "xmmword": 16}.get(o.split(" ptr")[0], 0) if " ptr" in o else 0
                if ins[0].mnemonic.startswith(("mov", "and", "or", "xor", "add", "sub")) and o.split(",")[0].endswith("]") and dsp + w > 0x201:
                    cover[ins[0].address] = "%s %s" % (ins[0].mnemonic, o)
                break
        k = text.find(pat2, k + 1)
ibr = text.find(struct.pack("<I", 0x1F79011))
check("C", ibr == -1, "image-base-relative disp 0x1F79011: %s; wider stores covering +0x201 (other records possible, listed for reading): %d"
      % ("none" if ibr == -1 else "%08X" % (tbase + ibr), len(cover)))
for a0 in sorted(cover): print("      %08X  %s" % (a0, cover[a0]))
# R
calls, calls2 = [], []
for j in range(len(text) - 5):
    if text[j] in (0xE8, 0xE9):
        t = tbase + j + 5 + struct.unpack_from("<i", text, j + 1)[0]
        if t == 0x267310: calls.append(tbase + j)
        elif t == 0x267300: calls2.append(tbase + j)
check("R", at(rd, {0x267310: "movsxd rax, ecx", 0x267313: "imul rcx, rax, 0x288", 0x267321: "movzx eax, byte ptr [rcx + rax]"})
      and found.get(0x26731A, "").startswith("lea rax"), "00267310 = mask of manager ecx; %d rel32 call sites; 00267300 (mask of a record pointer) %d" % (len(calls), len(calls2)))
# W
row = struct.unpack_from("<QQQ", d, off(0x1EED700))
acc = dis(0x3DC240, 0x3DC264); w = dis(0x34DCC0, 0x34DCF5)
check("W", struct.unpack_from("<I", d, off(0x1EED700))[0] == 0x5D8 and row[1] == 0x34CF90 and row[2] == 0x34DCC0
      and acc.get(0x3DC25E) == "mov rax, qword ptr [rax + rcx + 0x10]"
      and at(w, {0x34DCC6: "sub dword ptr [r8], 1", 0x34DCCD: "jns 0x34dcd7", 0x34DCCF: "xor eax, eax",
                 0x34DCD7: "movzx ecx, byte ptr [rdx + 0x15]", 0x34DCDB: "call 0x267310", 0x34DCE2: "je 0x34dcea",
                 0x34DCE4: "mov dword ptr [rbx], 0", 0x34DCEA: "mov eax, 1"}) and 0x34DCDB in calls,
      "wait poll 0034DCC0: countdown-1 < 0 -> done; target manager's mask != 0 -> countdown = 0")
# model of the poll: returns (running, countdown)
def poll(c, mask):
    c -= 1
    if c < 0: return 0, c
    return 1, (0 if mask else c)
seq = lambda c, mask: [poll(*x) for x in [(c, mask)]][0]
r1 = poll(5, 1); r2 = poll(r1[1], 1)
check("I", found.get(0x25E5C5) == want[0x25E5C5] and r1 == (1, 0) and r2 == (0, -1) and poll(5, 0) == (1, 4),
      "interpreter reads its manager's mask per opcode; model: countdown 5 under a skip ends on the second poll")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
