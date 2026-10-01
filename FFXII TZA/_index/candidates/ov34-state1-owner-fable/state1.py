"""state1.py - OV-34: what eventually moves a prepared state1 source owner (FABLE, Claude Opus 5.5, 2026-09-29). STATIC.

Answer: nothing moves it forward. A state1 owner (prepared and pinned, produced while its manager's skip mask +0x201 is
non-zero) leaves state1 only when a deleter frees its backing and writes 0.
  A  THE ARRAY (02B581A0, 80 records x 0x1C, state at +4) is addressed by rip only in 003DD380 (group delete),
     003DD420 (single delete), 003DD4C0 (the producer), 003DD740 / 003DD770 (handle getters), 003DD790 / 003DD7E0 (init), the armer 003DDA20 (state0 -> 2 only),
     003DD8D0 / 003DD980 (state-4 consumers)
  D  THE DELETERS: state1 -> free the backing (00369800), clear handle and state (qword store of 0 over +0/+4) and the
     route byte; state3 -> write 5; state4 -> dispose, free, clear. Nothing else
  G  THE READERS act only on state 4 (003DD740 returns the handle only for state4; 003DD8D0 / 003DD980 test == 4)
  C  THE ONLY PATH TO STATE 4 is the completion callback 003DD850 (writes state4 for a non-5 owner), referenced only by
     the submitter 003DDA70 (lea at 003DDA83), whose only caller is the producer's mask-zero branch (003DD644). A state1
     owner has no queued read, so the callback never runs for it
  Not claimed: how often shipped play produces sources while a manager is skipped (a live question).
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
S = [(d[pe + 24 + opt + i * 40:pe + 24 + opt + i * 40 + 8].rstrip(b"\0"),) + struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8)
     for i in range(n)]
TX = [s for s in S if s[0] == b".text"][0]; PD = [s for s in S if s[0] == b".pdata"][0]
def off(v): return v - B - TX[2] + TX[4]
text = d[TX[4]:TX[4] + TX[3]]; tb = B + TX[2]
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, msg):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, msg))
def dis(a, b): return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(a):off(b)], a)}
def rip_refs(lo, hi):
    out = []
    for j in range(len(text) - 4):
        r = struct.unpack_from("<i", text, j)[0]
        for extra in (0, 1, 4):
            t = tb + j + 4 + extra + r
            if lo <= t < hi:
                for back in range(7, 0, -1):
                    ins = list(cs.disasm(text[j - back:j + 15], tb + j - back, 1))
                    if ins and ins[0].address + ins[0].size == tb + j + 4 + extra and ("rip" in ins[0].op_str or ins[0].mnemonic in ("call", "jmp")):
                        out.append(ins[0].address); break
    return out
pdl = [struct.unpack_from("<III", d, PD[4] + k) for k in range(0, PD[1], 12)]
def owner(a):
    for b_, e_, u_ in pdl:
        if B + b_ <= a < B + e_: return B + b_
    return None       # the leaf helpers 003DD740..003DD7F8 carry no .pdata; reported by address below
refs = rip_refs(0x2B581A0, 0x2B58A74)
fns = sorted(set(owner(a) or 0 for a in refs))
leafs = sorted(set(a for a in refs if 0x3DD740 <= a < 0x3DD7F8))
FIVE = {0x3DD380, 0x3DD420, 0x3DD4C0, 0x3DD8D0, 0x3DD980}
unowned = [a for a in refs if owner(a) is None]
arm = dis(0x3DDA20, 0x3DDA6C)
check("A", set(owner(a) for a in refs if owner(a)) == FIVE
      and all(0x3DD740 <= a < 0x3DD800 or 0x3DDA20 <= a < 0x3DDA70 for a in unowned)
      and arm.get(0x3DDA3B) == "cmp dword ptr [rax + rcx + 4], 0" and arm.get(0x3DDA4E) == "mov dword ptr [rax + rcx + 4], 2",
      "array users: %s + leaf helpers (no .pdata) at %s" % (["%08X" % f for f in sorted(FIVE)], ["%08X" % a for a in unowned]))
dl = dis(0x3DD420, 0x3DD4B2); dg = dis(0x3DD380, 0x3DD417)
check("D", dl.get(0x3DD444) == "sub ecx, 1" and dl.get(0x3DD447) == "je 0x3dd49d" and dl.get(0x3DD49F) == "call 0x369800"
      and dl.get(0x3DD4A9) == "mov qword ptr [rdi], rax" and dl.get(0x3DD490) == "mov dword ptr [rdi + 4], 5"
      and dg.get(0x3DD3B5) == "je 0x3dd3e0" and dg.get(0x3DD3E3) == "call 0x369800" and dg.get(0x3DD3EC) == "mov qword ptr [rbx - 4], rbp"
      and dg.get(0x3DD40F) == "mov dword ptr [rbx], 5",
      "deleters: state1 -> free + clear to 0; state3 -> 5")
g1 = dis(0x3DD740, 0x3DD766); g2 = dis(0x3DD8D0, 0x3DD90B); g3 = dis(0x3DD980, 0x3DD9BB)
check("G", g1.get(0x3DD758) == "cmp dword ptr [rax + rcx + 4], 4" and g2.get(0x3DD905) == "cmp dword ptr [rax + rcx], 4"
      and g3.get(0x3DD9B5) == "cmp dword ptr [rax + rcx], 4", "readers act only on state 4")
cb = rip_refs(0x3DD850, 0x3DD851); sub = [tb + j for j in range(len(text) - 5) if text[j] in (0xE8, 0xE9) and tb + j + 5 + struct.unpack_from("<i", text, j + 1)[0] == 0x3DDA70]
ptr = [i for t in (0x3DD850, 0x3DDA70) for i in [d.find(struct.pack("<Q", t))] if i != -1]
check("C", cb == [0x3DDA83] and sub == [0x3DD644] and not ptr,
      "callback 003DD850 referenced only at %s; submitter 003DDA70 called only from %s; absolute pointers: %d"
      % (["%08X" % a for a in cb], ["%08X" % a for a in sub], len(ptr)))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
