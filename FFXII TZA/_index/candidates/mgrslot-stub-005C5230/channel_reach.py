"""channel_reach.py - control for the manager-slot owed item 2 (FABLE, Claude Opus 5.5, 2026-09-26): no shipped script can
make either bind write its reverse-lookup subscript past the 0x200 slot.

Domain: the four verb handlers, which are the binds' only direct callers (raw call index), plus the decompiled `us`
scripts (the corpus camerashake_census.py reads). Neither bind's address is stored anywhere in the image as a
qword/dword, and no rip-relative reference to it exists (checked separately, 2026-09-26).
Checks:
  H1 the two-argument handlers 00349730 (camerashakestart_1a3) and 0034F930 (camerastart_7e) push -1 before popping
     three values, and the first pop becomes the bind's fifth argument ([rsp+0x20]), so it is always -1, i.e. subscript 0.
  H2 the three-argument handlers 003492F0 (camerashakestart_1a2) and 0034F2F0 (camerastart_7d) take the fifth argument
     from the script's last argument (the first pop, no push before it).
  G1 getcamerasubframe (verb 0x1DE, 0050D1C0) returns 0053DD10() = `mov eax, 1 / ret`; getcameramainframe (0x1DF,
     0050F100) returns 005C5230() = `xor eax, eax / ret`.
  C1 shipped calls: camerashakestart_1a2 never; every camerastart_7d third argument is getcamerasubframe(),
     getcameramainframe() or a constant, and the largest resolved value keeps 0x18 + 2*sub + 2 <= 0x200 (sub <= 0xF3).
Known positive: C1's parser must count exactly the camerastart_7d( call sites a plain substring count finds.
"""
import os, re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
CORPUS = ROOT / "Database/Tools/work/FABLE/pub140-scratch/corpus/us"
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def ins(a, size): return list(cs.disasm(d[off(a):off(a) + size], a))
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
def shape(a):
    L = ins(a, 0x75); txt = ["%s %s" % (x.mnemonic, x.op_str) for x in L]
    push = any(t == "or edx, 0xffffffff" for t in txt) and "call 0x267f90" in txt
    pops = [i for i, t in enumerate(txt) if t == "call 0x267e10"]
    first = txt[pops[0] + 2] if pops else ""
    fifth = next((t for t in txt if t.startswith("mov dword ptr [rsp + 0x20], ")), "")
    return push, first, fifth
for a, name in ((0x349730, "camerashakestart_1a3"), (0x34F930, "camerastart_7e")):
    push, first, fifth = shape(a)
    check("H1 %s pushes -1 and passes the first pop as the fifth argument" % name,
          push and first.startswith("mov ebx, eax") and fifth.endswith("ebx"), "(%s | %s)" % (first, fifth))
for a, name in ((0x3492F0, "camerashakestart_1a2"), (0x34F2F0, "camerastart_7d")):
    push, first, fifth = shape(a)
    check("H2 %s takes the fifth argument from the script (no push)" % name,
          (not push) and first.startswith("mov ebx, eax") and fifth.endswith("ebx"), "(%s | %s)" % (first, fifth))
check("G1 0053DD10 is mov eax,1 / ret and 005C5230 is xor eax,eax / ret",
      d[off(0x53DD10):off(0x53DD10) + 6] == b"\xB8\x01\x00\x00\x00\xC3" and d[off(0x5C5230):off(0x5C5230) + 3] == b"\x33\xC0\xC3")
g = {x.address: x for x in ins(0x50D1C0, 0x1D) + ins(0x50F100, 0x1D)}
check("G1 the getters call them and return the result", g[0x50D1C9].op_str == "0x53dd10" and g[0x50F109].op_str == "0x5c5230")
calls, plain, vals, n1a2 = 0, 0, {}, 0
for fn in sorted(os.listdir(CORPUS)):
    if not fn.endswith(".txt"): continue
    t = open(CORPUS / fn, encoding="utf-8", errors="replace").read()
    plain += t.count("camerastart_7d(")
    n1a2 += len(re.findall(r"\bcamerashakestart_1a2\(", t))
    for m in re.finditer(r"\bcamerastart_7d\((.*)\)", t):
        args = [a.strip() for a in re.split(r",(?![^(]*\))", m.group(1))]
        calls += 1
        vals[args[-1]] = vals.get(args[-1], 0) + 1
resolve = {"getcamerasubframe()": 1, "getcameramainframe()": 0}
resolved = [resolve.get(k, int(k, 0) if re.fullmatch(r"-?(0x[0-9a-fA-F]+|\d+)", k) else None) for k in vals]
check("known positive: parsed camerastart_7d calls equal the substring count", calls == plain and calls > 0, "(%d parsed, %d substrings)" % (calls, plain))
check("C1 camerashakestart_1a2 is never called", n1a2 == 0, "(%d)" % n1a2)
check("C1 every camerastart_7d fifth argument resolves, and the largest stays inside the slot (<= 0xF3)",
      None not in resolved and max(resolved) <= 0xF3, "(%s -> max %s)" % (vals, max(r for r in resolved if r is not None)))
print("FAILS %d" % fails); sys.exit(1 if fails else 0)
