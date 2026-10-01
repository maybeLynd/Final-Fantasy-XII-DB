"""delivery.py - OV-36: callback single delivery and reuse for the resource queue (FABLE, Claude Opus 5.5, 2026-09-29).
STATIC.

  D  THE PUMP 0032E070 dispatches the head slot only in states 1..6 (dec / cmp 5 / ja -> the service tail); state 0 is
     never dispatched
  P  EVERY DELIVERY in the pump - the completion helper 0032E330 (0032E133, 0032E1FA, 0032E26F), the error completion
     0032E370 (0032E1D3, 0032E285) and the cancel callback [slot+0x48] (0032E189) - is followed, before the loop runs
     again, by slot state := 0 and the recycle 0032EC40. So one slot delivers at most once
  H  THE HELPERS: 0032E330 calls [slot+0x40](owner, ..., 1) whenever it is set; 0032E370 only when the requested length
     is -1; neither clears the pointer - delivery uniqueness rests on P, not on the helpers
  O  ONE LIVE REQUEST PER OWNER: the armer admits only owner state 0 and the producer only state 2 (then 3), so an owner
     never has two queued slots (the same owner address across successive requests is sequential, not concurrent)
  R  RE-ENTRY (bounded): the owner callback 003DD850 runs before the slot is reset; its direct callees are listed and none
     is the pump. Transitive reachability of the pump from those callees is not claimed
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
ins = list(cs.disasm(d[off(0x32E070):off(0x32E2CD)], 0x32E070))
at = {x.address: ("%s %s" % (x.mnemonic, x.op_str)) for x in ins}
check("D", at.get(0x32E0A0) == "movzx eax, byte ptr [rbx + 0x20]" and at.get(0x32E0A4) == "dec eax"
      and at.get(0x32E0A6) == "cmp eax, 5" and at.get(0x32E0A9) == "ja 0x32e2a0", "only slot states 1..6 are dispatched")
# P: from each delivery site, follow the straight line (and one unconditional jmp) until the next jmp to the loop head
DELIV = [0x32E133, 0x32E1FA, 0x32E26F, 0x32E1D3, 0x32E285, 0x32E189]
idx = {x.address: k for k, x in enumerate(ins)}
def after(a):
    seen, k, hops = [], idx[a] + 1, 0
    while k < len(ins) and len(seen) < 12:
        x = ins[k]; seen.append("%s %s" % (x.mnemonic, x.op_str))
        if x.mnemonic == "jmp":
            t = int(x.op_str, 16)
            if t == 0x32E090: break
            k = idx[t]; hops += 1
            if hops > 2: break
            continue
        k += 1
    return seen
bad = []
for a in DELIV:
    seq = after(a)
    if not (any(s.startswith("mov byte ptr [rbx + 0x20], 0") for s in seq) and "call 0x32ec40" in seq and seq[-1] == "jmp 0x32e090"):
        bad.append(("%08X" % a, seq))
check("P", at.get(0x32E189) == "call rax" and at.get(0x32E176) == "mov rax, qword ptr [rbx + 0x48]" and not bad,
      "all six delivery sites reset the slot to 0 and recycle it before the next dispatch %s" % (bad or ""))
h = {x.address: ("%s %s" % (x.mnemonic, x.op_str)) for x in cs.disasm(d[off(0x32E330):off(0x32E3AE)], 0x32E330)}
check("H", h.get(0x32E336) == "mov rax, qword ptr [rcx + 0x40]" and h.get(0x32E34F) == "call rax"
      and h.get(0x32E382) == "cmp dword ptr [rcx + 0x28], -1" and h.get(0x32E392) == "call rax"
      and not any("qword ptr [rbx + 0x40], " in v or "qword ptr [rcx + 0x40], " in v for v in h.values() if v.startswith("mov qword ptr")),
      "helpers call the completion pointer without clearing it")
arm = {x.address: ("%s %s" % (x.mnemonic, x.op_str)) for x in cs.disasm(d[off(0x3DDA20):off(0x3DDA6C)], 0x3DDA20)}
check("O", arm.get(0x3DDA3B) == "cmp dword ptr [rax + rcx + 4], 0" and arm.get(0x3DDA4E) == "mov dword ptr [rax + rcx + 4], 2",
      "armer admits only state 0 (the producer requires 2 and leaves 3: see ov34-state1-owner-fable)")
cb = [x.op_str for x in cs.disasm(d[off(0x3DD850):off(0x3DD8D0)], 0x3DD850) if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x")]
check("R", "0x32e070" not in cb, "owner callback 003DD850 direct callees: %s" % sorted(set(cb)))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
