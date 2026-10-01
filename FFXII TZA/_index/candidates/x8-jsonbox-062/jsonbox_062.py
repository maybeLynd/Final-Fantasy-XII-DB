"""jsonbox_062.py [JSONBOX_GIT] - X-8: the linked JsonBox is 0.6.2 (FABLE, Claude Opus 5.5, 2026-09-27). Static read of the
shipped exe against the upstream JsonBox history (tier 6). Corrects the 2026-09-27 X-8 status, which called the 0.6.x
fork tag unrecoverable.

  Upstream (needs JSONBOX_GIT; the committed .out carries the run with the clone):
  U1 0.6 -> 0.6.1 changes only comments in include/ and src/.
  U2 0.6.1 -> 0.6.2 changes String32 from std::basic_string<int32_t> to std::vector<int32_t> (Convert.h), besides the
     Array / Object wrappers that the EASTL port replaced anyway.
  U3 after 0.6.2 (untagged master) src/Value.cpp changes only inside Value::getToString (0.6.2 lines 478-507); the other
     changed files are build scripts and docs.
  Image:
  I1 readString's backslash-u arm appends the code point as a vector does - 'if (end < cap) {*end = v; end += 4} else insert'
     (002023FB-00202414, helper 001A4250) - and writes no terminator, which basic_string's append always does. So
     String32 is the vector: 0.6.2 or later.
  I2 getToString is not linked: of the functions that read JsonBox's per-unit literal globals ("true" 008FCDA0,
     "false" 008FCD98, "null" 00904780), only the writer 001FF210 and the parser 00200E60 read more than one kind;
     getToString reads all three. So master's only code change is invisible, and 0.6.2 is the tag.
Exit 1 on any FAIL.
"""
import re, subprocess, sys, struct, collections
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
G = sys.argv[1] if len(sys.argv) > 1 else None
def git(*a): return subprocess.run(["git", "-C", G] + list(a), capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
if G:
    ch = [l for l in git("diff", "0.6", "0.6.1", "--", "include", "src").splitlines()
          if l[:1] in "+-" and not l.startswith(("+++", "---")) and l[1:].strip() and not l[1:].strip().startswith(("*", "/*", "//"))]
    check("U1 0.6 -> 0.6.1 changes only comments", ch == [], str(ch[:3]))
    v1 = git("show", "0.6.1:include/JsonBox/Convert.h"); v2 = git("show", "0.6.2:include/JsonBox/Convert.h")
    check("U2 0.6.1 -> 0.6.2 turns String32 from basic_string<int32_t> into vector<int32_t>",
          "typedef std::basic_string<int32_t> String32;" in v1 and "typedef std::vector<int32_t> String32;" in v2)
    src = git("show", "0.6.2:src/Value.cpp").splitlines()
    s0 = next(i + 1 for i, l in enumerate(src) if "Value::getToString() const" in l)
    s1 = next(i + 1 for i, l in enumerate(src) if i + 1 > s0 and re.match(r"\t\S.*Value::\w+\(", l))  # next member
    rng = [tuple(int(x) for x in (m.group(1), m.group(2) or 1)) for m in re.finditer(r"^@@ -(\d+)(?:,(\d+))? ", git("diff", "-U0", "0.6.2", "HEAD", "--", "src/Value.cpp"), re.M)]
    inside = all(s0 <= a and a + max(n, 1) - 1 < s1 for a, n in rng)
    other = [f for f in git("diff", "--name-only", "0.6.2", "HEAD").split() if f.startswith(("src/", "include/")) and not f.endswith(("Value.cpp", "Android.mk"))]
    check("U3 after 0.6.2 the only code change is inside getToString (lines %d-%d)" % (s0, s1 - 1), inside and other == [], "hunks=%s other=%s" % (rng, other))
else:
    print("SKIP  U1-U3 (no JSONBOX_GIT)")
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if 0x120000 + va <= v < 0x120000 + va + rs: return v - 0x120000 - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def at(a, b): return {x.address: ("%s %s" % (x.mnemonic, x.op_str)).strip() for x in cs.disasm(d[off(a):off(b)], a)}
p = at(0x2023F1, 0x202427); h = at(0x1A4250, 0x1A42B4)
check("I1 the backslash-u append is a vector push with no terminator (inline path and the insert helper 001A4250)",
      p.get(0x2023FB) == "cmp rdx, qword ptr [rsp + 0x70]" and p.get(0x202402) == "lea rax, [rdx + 4]"
      and p.get(0x202414) == "mov dword ptr [rdx], eax" and p.get(0x202422) == "call 0x1a4250"
      and h.get(0x1A42A3) == "mov dword ptr [r14], eax" and h.get(0x1A42A6) == "add qword ptr [rdi + 8], 4"
      and not any(re.match(r"mov dword ptr \[r\w+ \+ 4\], 0$", v) for v in list(p.values()) + list(h.values())))
SIZES = {}
for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    q = l.rstrip("\n").split("\t")
    try: SIZES[int(q[0], 16)] = int(q[2])
    except (ValueError, IndexError): pass
def rip(x):
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", x.op_str)
    return x.address + x.size + (int(m.group(2), 16) if m.group(1) == "+" else -int(m.group(2), 16)) if m else None
LIT = {0x8FCDA0: "true", 0x8FCD98: "false", 0x904780: "null"}
inits, bodies, refs = {}, {}, collections.defaultdict(set)
for f, sz in SIZES.items():
    o = off(f)
    if o is None or sz <= 0 or not 0x121000 <= f < 0x8C0000: continue
    b = list(cs.disasm(d[o:o + sz], f)); tg = [rip(x) for x in b]
    kinds = {LIT[t] for t in tg if t in LIT}
    if kinds:
        g = [rip(x) for x in b if x.mnemonic == "movdqu" and x.op_str.startswith("xmmword ptr [rip")]
        if g: inits[g[0]] = (next(iter(kinds)), f)
    bodies[f] = tg
for f, tg in bodies.items():
    for t in tg:
        if t in inits and inits[t][1] != f: refs[f].add(inits[t][0])
multi = sorted("%08X" % f for f, s in refs.items() if len(s) >= 2)
check("I2 only the writer 001FF210 and the parser 00200E60 read more than one literal kind (getToString not linked)",
      multi == ["001FF210", "00200E60"] and len(inits) == 12, "readers=%s literal globals=%d" % (multi, len(inits)))
print("FAILS", fails); sys.exit(1 if fails else 0)
