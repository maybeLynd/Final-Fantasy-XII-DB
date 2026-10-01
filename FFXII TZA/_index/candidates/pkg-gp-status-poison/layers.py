"""layers.py - PKG-GP-STATUS-POISON Q3: does an inflicted Poison go into the +0x68 effect layer? (FABLE, Claude Opus 5.5,
2026-09-29). STATIC.

  N  THE STATUS WRITE 0030E360 (its .pdata fragments 0030E360-0030E8E4, 0030E8F0-0030E96B) never calls the layer mutator
     0030E130. The call at 0030E97F belongs to 0030E970, a separate 25-byte wrapper with its own .pdata entry
  A  THE APPLIER'S STEP 14 feeds the result record's effect-id bytes to 0030E130 (call sites 003117CB, 00311807)
  C  0030E130 has seven rel32 call sites in all (002FDFAC, 002FE00B, 0030E97F, 00310378, 00310396, 003117CB, 00311807)
  So "status" names two namespaces: the 32 battle statuses (Poison is id 8) live in the status words +0x64 / +0x3C, written
  only by the status write; the 128-bit +0x68 / +0x78 layers hold effect ids (the table at 02EBF040), which attacks reach
  through the applier's step 14. An inflicted Poison never enters +0x68.
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
PD = [s for s in S if s[0] == b".pdata"][0]; TX = [s for s in S if s[0] == b".text"][0]
def off(v): return v - B - TX[2] + TX[4]
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
pdata = [struct.unpack_from("<III", d, PD[4] + j) for j in range(0, PD[1], 12)]
# the status write's two fragments, named by address (0030E970 right after them is checked to be a separate entry)
mine = [(B + b, B + e) for b, e, u in pdata if B + b in (0x30E360, 0x30E8F0)]
wrap = [(B + b, B + e) for b, e, u in pdata if B + b == 0x30E970]
calls = set()
for s, e in mine:
    for x in cs.disasm(d[off(s):off(e)], s):
        if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x"): calls.add(int(x.op_str, 16))
w = [("%s %s" % (x.mnemonic, x.op_str)) for x in cs.disasm(d[off(0x30E970):off(0x30E989)], 0x30E970)]
check("N", mine == [(0x30E360, 0x30E8E4), (0x30E8F0, 0x30E96B)] and 0x30E130 not in calls and wrap == [(0x30E970, 0x30E989)]
      and "call 0x30e130" in w, "status write fragments call 0030E130: %s; 0030E970 is its own function: %s" % (0x30E130 in calls, bool(wrap)))
text = d[TX[4]:TX[4] + TX[3]]; tb = B + TX[2]
sites = [tb + j for j in range(len(text) - 5) if text[j] in (0xE8, 0xE9) and tb + j + 5 + struct.unpack_from("<i", text, j + 1)[0] == 0x30E130]
check("C", sites == [0x2FDFAC, 0x2FE00B, 0x30E97F, 0x310378, 0x310396, 0x3117CB, 0x311807], "0030E130 call sites %s" % ["%08X" % s for s in sites])
check("A", 0x3117CB in sites and 0x311807 in sites, "the applier's step 14 (00311781-00311819) reaches the layer mutator")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
