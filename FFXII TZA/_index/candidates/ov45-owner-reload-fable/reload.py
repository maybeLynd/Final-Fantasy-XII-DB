"""reload.py - OV-45 narrowing: what a manager reload does to its indexed source owners, and the queue order it relies on
(FABLE, Claude Opus 5.5, 2026-09-29). STATIC.

  U  THE UNLOAD (the manager slot unload, call at 00262982) runs the group deleter 003DD380 over the manager's sixteen
     owners: state1 freed and cleared, state3 -> 5 (its queued read and callback preserved), state4 disposed
  I  THE BIND (0026C8C0) ends by tail-jumping to the group initialiser 003DD790 (0026CDE3), which clears every record
     without releasing anything
  Q  THE QUEUE INSERT 0032E870 never fails for a full queue: with no free slot it loops, running the pump 0032E070 and a
     service call until one frees; then 0032E990 links the slot at the HEAD when its flag is 0 and at the TAIL otherwise
  R  THE SOURCE-OWNER REQUESTER 0032E620 passes flag 1 (tail)
  H  HEAD INSERTION HAS ONE USER: of the four insert call sites only 0032E7A2 (inside the head wrapper 0032E780) passes
     flag 0, and 0032E780's two call sites are both in 003EADE0, the BGM stream reader (the queue page: "the BGM stream's
     reads jump the pending queue"). Every other request, the manager reload's included, links at the tail
  So an old owner's read queued before a reload completes before the reload's own requests do; the pump serves the head in
  order, so its callback frees the state5 owner before the new payload binds and I clears the records.
  E  A FAILED READ calls back only when its byte count is -1: the insert stores the caller's count at slot +0x28
     (0032E92C), and the failure helper 0032E370 calls the completion, with ok = 0, only when +0x28 == -1; otherwise the
     slot is released with no callback. The owner's completion 003DD850 never reads its ok argument (r8)
  Residue: a failed read with a real byte count never calls back, and its state-5 owner is forgotten by I. (A first draft
  said every failed read never calls back, citing OV-42 - but OV-42 is about a submission with no queue entry.)
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
text_sec = [s for s in SECS if True]
def callers(t):
    out = []
    for vs, va, rs, ro in SECS:
        blob = d[ro:ro + rs]
        for j in range(len(blob) - 5):
            if blob[j] in (0xE8, 0xE9) and B + va + j + 5 + struct.unpack_from("<i", blob, j + 1)[0] == t: out.append(B + va + j)
    return out
check("U", callers(0x3DD380) == [0x262982] and dis(0x262980, 0x262987).get(0x262982) == "call 0x3dd380"
      and dis(0x3DD380, 0x3DD417).get(0x3DD40F) == "mov dword ptr [rbx], 5", "unload -> group deleter (state3 -> 5)")
check("I", callers(0x3DD790) == [0x26CDE3] and dis(0x26CDE3, 0x26CDE8).get(0x26CDE3) == "jmp 0x3dd790"
      and not any(s.startswith("call") for s in dis(0x3DD790, 0x3DD7D5).values()), "bind -> group init, which calls nothing")
q = dis(0x32E870, 0x32E98D); l = dis(0x32E990, 0x32EA1A)
check("Q", at(q, {0x32E88D: "cmp qword ptr [rip + 0x1f9693c], rbx", 0x32E8AA: "call 0x32e070", 0x32E8C3: "je 0x32e8a2",
                  0x32E8C9: "call 0x32e990"})
      and at(l, {0x32E9E6: "test r9d, r9d", 0x32E9E9: "jne 0x32ea1a", 0x32E9EB: "mov qword ptr [rip + 0x1f967ce], rdx"}),
      "insert waits (pumping) for a free slot; link: flag 0 -> head, else tail")
r = dis(0x32E742, 0x32E760)
check("R", r.get(0x32E742) == "mov dword ptr [rsp + 0x28], 1" and r.get(0x32E759) == "call 0x32e870"
      and dis(0x32E6B9, 0x32E6C1).get(0x32E6B9) == "mov dword ptr [rsp + 0x28], 1",
      "the source-owner requester links with flag 1 (tail) on both of its paths")
ins = [(a, v) for a, v in ((0x32E6DD, 0x32E6B9), (0x32E759, 0x32E742), (0x32E7A2, 0x32E795), (0x32E84D, 0x32E836))]
flags = {a: dis(v, v + 8).get(v) for a, v in ins}
check("H", callers(0x32E870) == [a for a, _ in ins] and flags[0x32E7A2] == "mov dword ptr [rsp + 0x28], 0"
      and all(f == "mov dword ptr [rsp + 0x28], 1" for a, f in flags.items() if a != 0x32E7A2)
      and callers(0x32E780) == [0x3EAE4C, 0x3EAF9A],
      "only the head wrapper links at the head; its callers are both in the BGM stream reader 003EADE0")
e = dis(0x32E370, 0x32E3AE)
cb = dis(0x3DD850, 0x3DD8C2)
check("E", dis(0x32E92C, 0x32E930).get(0x32E92C) == "mov dword ptr [r10 + 0x28], esi"
      and at(e, {0x32E382: "cmp dword ptr [rcx + 0x28], -1", 0x32E386: "jne 0x32e394", 0x32E38C: "xor r8d, r8d", 0x32E392: "call rax"})
      and callers(0x32E370) == [0x32E1D3, 0x32E285]
      and not any(re.search(r"r8[dwb]?", s) for s in cb.values()),
      "a failed read calls back (ok = 0) only when its byte count is -1; 003DD850 never reads ok")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
