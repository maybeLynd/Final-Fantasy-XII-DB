"""bom_reader.py - control for NS-4 (FABLE, Claude Opus 5.5, 2026-09-26): the namespace byte-order mark IS read.

Domain: every occurrence of the dword 0x01020304 in .text, decoded as the instruction a linear decode of its containing
function (functions.tsv) places over it; hits inside no instruction are reported, not dropped.
Checks:
  B1 exactly one .text instruction carries the immediate 0x01020304 as a compare: 0059E167 `cmp dword ptr [rdi], 0x1020304`
     in 0059E070, the header reader's only caller.
  B2 rdi there is the namespace buffer's data pointer: 0059E15A `mov rdi, [rsp+0x60]`, the +0x08 of the buffer whose
     address 0059E147 passes to the header reader as r8 (`lea r8, [rsp+0x58]`).
  B3 a mismatch branches to 0059E295 `mov ebx, 6` - the refusal code the header reader itself returns - and the same body
     checks the namespace self-size at 0059E191 `cmp dword ptr [rdi+4], ecx`.
Known positive (sensitivity): the same search for the header marker 0x50485952 must find the two compares the cluster
header contract documents (0059A3FF, 0059A419); a search that finds nothing cannot pass.
"""
import bisect, re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(n):
    o = pe + 24 + opt + i * 40
    secs.append((d[o:o + 8].rstrip(b"\0").decode(), *struct.unpack_from("<IIII", d, o + 8)))
def off(v):
    for nm, vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
funcs = sorted(int(l.split("\t")[0], 16) for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8",
               errors="replace") if re.match(r"[0-9A-Fa-f]{8}\t", l))
cs = Cs(CS_ARCH_X86, CS_MODE_64); lin = {}
text = [s for s in secs if s[0] == ".text"][0]
def sites(value):
    out, off_hits = [], []
    _, vs, va, rs, ro = text
    pat = struct.pack("<I", value); p = ro
    while True:
        p = d.find(pat, p, ro + rs)
        if p < 0: break
        v = BASE + va + p - ro; f = funcs[bisect.bisect_right(funcs, v) - 1]
        if f not in lin: lin[f] = list(cs.disasm(d[off(f):off(f) + 0x4000], f))
        cov = [x for x in lin[f] if x.address <= v < x.address + x.size]
        (out if cov else off_hits).append((cov[0] if cov else v, f))
        p += 1
    return out, off_hits
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
hdr, _ = sites(0x50485952)
cmps = sorted(x.address for x, f in hdr if x.mnemonic == "cmp")
check("known positive: header marker compares at 0059A3FF and 0059A419 (instruction starts)", cmps == [0x59A3FF, 0x59A419], str([hex(c) for c in cmps]))
bom, offb = sites(0x01020304)
bcmp = [(x, f) for x, f in bom if x.mnemonic == "cmp"]
check("B1 exactly one compare against 0x01020304, at 0059E167 in 0059E070",
      len(bcmp) == 1 and bcmp[0][0].address == 0x59E167 and bcmp[0][1] == 0x59E070 and bcmp[0][0].op_str == "dword ptr [rdi], 0x1020304",
      "(%s; %d other on-boundary hits, %d off-boundary)" % ([(hex(x.address), x.op_str) for x, f in bcmp], len(bom) - len(bcmp), len(offb)))
body = {x.address: x for x in lin[0x59E070]}
check("B2 rdi is the namespace buffer's data pointer (r8 = &rsp+0x58, rdi = [rsp+0x60])",
      body[0x59E147].op_str == "r8, [rsp + 0x58]" and body[0x59E15A].op_str == "rdi, qword ptr [rsp + 0x60]" and body[0x59E153].op_str == "0x59a3b0")
check("B3 mismatch -> 0059E295 mov ebx, 6; self-size compare at 0059E191",
      body[0x59E16D].mnemonic == "jne" and body[0x59E16D].op_str == "0x59e295" and body[0x59E295].op_str == "ebx, 6"
      and body[0x59E191].op_str == "dword ptr [rdi + 4], ecx")
print("FAILS %d" % fails); sys.exit(1 if fails else 0)
