"""clients.py - OV-25 narrowing: every client of the tail requester 0032E620, grouped by the completion callback it loads
(FABLE, Claude Opus 5.5, 2026-09-29). STATIC.

  C  CENSUS: every rel32 call/jmp to 0032E620; for each, a converged decode of the preceding bytes, and every rip-relative
     `lea` into .text within the last 30 instructions (how a request descriptor's callback is built)
  K  CONTROLS (known clients must appear with their callback): the indexed source owner (003DDAB9 -> 003DD850) and the
     four package-directory completions of the manager resource-set load (0032FE9E/0032FF0B/0032FF76/0032FFE2 ->
     00331760/003302B0/00331820/003317C0, the voice-pack page)
  Output: one line per callback set with its call sites, and the sites with no code address loaded nearby. Which of these
  clients keep a persistent, pinned owner record (an "external-owner family" like 003DD850's) is NOT classified here.
"""
import hashlib, os, re, struct, sys, collections
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
text = d[TX[4]:TX[4] + TX[3]]; tb = B + TX[2]; te = tb + TX[3]
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(tag, ok, msg):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, msg))
sites = [tb + j for j in range(len(text) - 5) if text[j] in (0xE8, 0xE9) and tb + j + 5 + struct.unpack_from("<i", text, j + 1)[0] == 0x32E620]
def conv(a, back=0xA0):
    for st in range(a - back, a - 8):
        ins = list(cs.disasm(text[st - tb:a - tb + 5], st))
        k = [i for i, x in enumerate(ins) if x.address == a]
        if k: return ins[:k[0] + 1]
    return []
bysite = {}
for s in sites:
    cbs = set()
    for x in conv(s)[-30:]:
        if x.mnemonic != "lea": continue
        m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", x.op_str)
        if m:
            t = x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 16)
            if tb <= t < te: cbs.add(t)
    bysite[s] = tuple(sorted(cbs))
fam = collections.defaultdict(list)
for s, c in bysite.items(): fam[c].append(s)
KNOWN = {0x3DDAB9: 0x3DD850, 0x32FE9E: 0x331760, 0x32FF0B: 0x3302B0, 0x32FF76: 0x331820, 0x32FFE2: 0x3317C0}
check("C", len(sites) == 51, "%d call sites of 0032E620; %d distinct callback sets; %d sites with no code address loaded"
      % (len(sites), len([k for k in fam if k]), len(fam.get((), []))))
check("K", all(KNOWN[s] in bysite.get(s, ()) for s in KNOWN), "known clients found with their callbacks")
for k, v in sorted(fam.items(), key=lambda kv: (not kv[0], kv[0])):
    print("      %-20s %s" % (" ".join("%08X" % c for c in k) or "(none)", " ".join("%08X" % a for a in v)))
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
