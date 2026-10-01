"""recovery.py - OV-42 (and OV-19's recovery half): what recovers a source owner whose queue submission is rejected
(FABLE, Claude Opus 5.5, 2026-09-29). STATIC.

Answer: nothing. A rejected submission orphans a pinned backing.
  Q  THE REQUESTER 0032E620 fails in two ways: a negative (narrowed) file index returns -1 at once (0032E64A-0032E651), and
     a failed queue insert returns 0032E870's 0 (0032E6DD-0032E6E7 -> 0032E738-0032E73D)
  S  THE SUBMITTER 003DDA70 ignores that return and writes owner state 3 unconditionally (003DDAB9 call, 003DDABE store)
  N  NO CALLBACK FOLLOWS: the completion callback 003DD850 is carried only by the queue entry (its one reference is the
     submitter's lea at 003DDA83), so a rejected owner never reaches state 4, and a delete of that state3 owner writes 5
     (003DD490), which again only the callback resolves
  I  RE-INITIALISATION DROPS IT: the group initialiser 003DD790 zeroes each record's handle/state qword and route byte and
     calls nothing, so the pinned backing is neither unpinned nor freed
  H  HELD STATE1 IS NEVER SUBMITTED: OV-34 (ov34-state1-owner-fable/state1.py)
  Not claimed: whether shipped play ever feeds a negative narrowed index or fills the queue (runtime / data).
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
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, msg):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, msg))
def dis(a, b): return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(a):off(b)], a)}
at = lambda c, w: all(c.get(a) == s for a, s in w.items())
q = dis(0x32E620, 0x32E760)
check("Q", at(q, {0x32E64A: "test edx, edx", 0x32E64C: "jns 0x32e656", 0x32E64E: "or eax, 0xffffffff", 0x32E6DD: "call 0x32e870",
                  0x32E6E2: "mov r8d, eax", 0x32E6E7: "je 0x32e738", 0x32E73D: "mov eax, r8d"}),
      "requester: negative index -> -1; failed insert -> 0")
s = dis(0x3DDA70, 0x3DDACB)
check("S", at(s, {0x3DDAB9: "call 0x32e620", 0x3DDABE: "mov dword ptr [rbx + 4], 3"}), "submitter writes state 3 whatever the requester returned")
dl = dis(0x3DD420, 0x3DD4B2)
check("N", dl.get(0x3DD490) == "mov dword ptr [rdi + 4], 5" and dl.get(0x3DD44C) == "je 0x3dd490",
      "a deleted state3 owner goes to 5 and waits for a callback its missing queue entry will never deliver")
init = list(cs.disasm(d[off(0x3DD790):off(0x3DD7D5)], 0x3DD790))
check("I", init[-1].mnemonic == "ret" and not any(x.mnemonic == "call" for x in init)
      and any(x.op_str == "qword ptr [rax - 0xd], r10" for x in init),
      "group init clears handle/state and calls nothing: no unpin, no free")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
