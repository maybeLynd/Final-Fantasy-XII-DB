"""ms3.py - MS-3: which ancestors of a map container can be released (FABLE, Claude Opus 5.5, 2026-09-29). STATIC.

Answer: none - each map container is created parentless and is never attached, so it has no ancestor.
  K  THE CONSTRUCTOR 00244F50 only allocates (002497B0 for a size above 0x120; the containers are 0x179E0) and constructs
     through 002465F0, which calls only memset: nothing attaches
  P  THE CREATORS (location 002B9D30, track 002B6350) attach only the PAGE: 00244960(container, page) attaches the page
     under the container when the page has no parent (00244960 -> 00248220)
  N  NO ATTACH ROUTINE IS HANDED A CONTAINER: at every call site of the three tree-attach routines 00248220 (link under a parent), 00244960
     (link when parentless) and 00247950 (attach under the root) -
     no rip-relative load of the two container globals (0209E5F0 location, 0209E5C0 track) sits in the preceding 40 bytes
  F  THE OTHER DIRECTION: from each of the rip loads of either global, no attach routine is called within 12 instructions
     (00247570, which a first version counted, attaches a transition DESCRIPTOR, not a tree link: the forward sweep
     flagged its call at 002B9EFA with the page in rcx, and reading it removed it from the set; 00248030 is the per-frame
     generation walker)
  Limit: N and F are bounded sweeps (a global loaded further back and carried in a register would escape it); a manager-wide
  release of every widget, if one exists, is not read here - it would not be an ancestor's release.
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
S = [(d[pe + 24 + opt + i * 40:pe + 24 + opt + i * 40 + 8].rstrip(b"\0"),) + struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8)
     for i in range(n)]
TX = [s for s in S if s[0] == b".text"][0]
def off(v): return v - B - TX[2] + TX[4]
text = d[TX[4]:TX[4] + TX[3]]; tb = B + TX[2]
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, msg):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, msg))
def calls(a, b): return [x.op_str for x in cs.disasm(d[off(a):off(b)], a) if x.mnemonic == "call"]
def dis(a, b): return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(a):off(b)], a)}
check("K", calls(0x244F50, 0x245000) == ["0x2497b0", "0x2465f0"] and calls(0x2465F0, 0x246700)[:1] == ["0x861ec0"],
      "constructor: allocate + construct (memset); no attach")
at = dis(0x244960, 0x24496C)
loc = dis(0x2B9F60, 0x2B9F6F); trk = dis(0x2B6510, 0x2B6520)
check("P", at.get(0x244960) == "cmp qword ptr [rdx + 0x10], 0" and at.get(0x244965) == "je 0x248220"
      and loc.get(0x2B9F60) == "mov rdx, rbx" and loc.get(0x2B9F6A) == "call 0x244960"
      and trk.get(0x2B651B) == "call 0x244960",
      "the creators attach the page (rdx) under the container (rcx), never the container itself")
G = {0x209E5F0: "location", 0x209E5C0: "track"}
found = []; total = 0
for tgt in (0x248220, 0x244960, 0x247950):
    for j in range(len(text) - 5):
        if text[j] in (0xE8, 0xE9) and tb + j + 5 + struct.unpack_from("<i", text, j + 1)[0] == tgt:
            s0 = tb + j; total += 1
            for st in range(s0 - 40, s0):
                ins = list(cs.disasm(d[off(st):off(s0) + 5], st))
                if ins and any(x.address == s0 for x in ins): break
            for x in ins:
                m = re.search(r"\[rip \+ (0x[0-9a-f]+)\]", x.op_str)
                if m and x.address < s0 and x.address + x.size + int(m.group(1), 16) in G: found.append((s0, tgt))
# F (the other direction): from every rip-relative load of either global, the next 12 instructions call no attach routine.
# The loads are found by resolving every rip operand in .text, so the count of loads is the sweep's positive control.
ATT = {"0x248220", "0x244960", "0x247950"}
loads = []
for j in range(len(text) - 4):
    r = struct.unpack_from("<i", text, j)[0]
    for extra in (0, 1, 4):
        if tb + j + 4 + extra + r in G:
            for back in range(7, 0, -1):
                ins = list(cs.disasm(text[j - back:j + 15], tb + j - back, 1))
                if ins and "rip" in ins[0].op_str and ins[0].address + ins[0].size == tb + j + 4 + extra:
                    loads.append(ins[0].address); break
bad = []
for a in loads:
    nxt = list(cs.disasm(d[off(a):off(a) + 80], a))[:12]
    bad += ["%08X" % a for x in nxt if x.mnemonic in ("call", "jmp") and x.op_str in ATT]
check("N", total > 100 and not found, "%d attach call sites, %d with a container global loaded in the 40 bytes before" % (total, len(found)))
check("F", len(loads) > 20 and not bad, "%d loads of the two globals; attach calls within 12 instructions after one: %s" % (len(loads), bad or "none"))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
