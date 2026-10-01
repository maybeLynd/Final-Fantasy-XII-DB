"""UC-3: head blocks matched to NAMED libvpx 1.6.0 routines by contiguous instruction runs (OPUS, 2026-09-27). Control.

Upstream source (tier 6): libvpx tag v1.6.0, commit 1c108eb0e1dcae0149c6db693eb56b2fc963422b
(https://chromium.googlesource.com/webm/libvpx), the version the image's banner names ("WebM Project VP8 Decoder
v1.6.0"). Pass the checkout path as argv[1]. No assembler is used: each hand-written x86 routine's source mnemonic
sequence (x86inc aliases mova / movu / movh mapped) is compared with the block's disassembly, and the score is the
longest CONTIGUOUS matching run over the routine's length.
  M1 eleven of the 66 unlisted head blocks carry a run of at least 20 instructions covering at least 85% of a named
     routine - the table below
  M2 NULL CONTROL: 80 random listed game functions (0x200000..0x5E0000, 200..4,000 B, seed 7) never exceed a run of
     10 instructions against any routine - so the head-block runs (20..280) are not chance
Not claimed: the other 55 blocks (many are larger than any one routine or are compiled intrinsics C, which a source
mnemonic sequence cannot match); that the matched blocks are exactly one routine each.
"""
import difflib, random, re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]; DB = HERE.parents[2]
SRC = Path(sys.argv[1])
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes(); BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in SECS:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
ALIAS = {"mova": "movdqa", "movu": "movdqu", "movh": "movq"}
def norm(m): m = m.lower(); return ALIAS.get(m, m)
funcs = {}
for p in SRC.rglob("*.asm"):
    if {"arm", "mips", "ppc"} & set(p.parts): continue
    cur = None
    for raw in p.read_text(encoding="latin-1").splitlines():
        line = raw.split(";")[0].strip()
        if not line: continue
        m = re.match(r"(?:sym\()?(\w+)\)?:\s*$", line) or re.match(r"cglobal\s+(\w+)", line)
        if m: cur = "%s:%s" % (p.relative_to(SRC).as_posix(), m.group(1)); funcs[cur] = []; continue
        if cur is None or line.startswith(("%", ".", "global", "SECTION", "section", "align", "ALIGN", "times", "dw", "dd", "db", "dq")): continue
        tok = line.split()[0]
        if not tok.endswith(":") and re.fullmatch(r"[a-zA-Z][a-zA-Z0-9]*", tok): funcs[cur].append(norm(tok))
funcs = {k: v for k, v in funcs.items() if len(v) >= 15}
def seq(a, s): return [norm(x.mnemonic) for x in cs.disasm(d[off(a):off(a) + s], a) if x.mnemonic not in ("nop", "int3")]
def best(bs):
    top = (0, 0, 0, None)
    for k, fs in funcs.items():
        mb = difflib.SequenceMatcher(None, bs, fs, autojunk=False).find_longest_match(0, len(bs), 0, len(fs))
        if (mb.size, mb.size / len(fs)) > (top[1], top[0]): top = (mb.size / len(fs), mb.size, len(fs), k)
    return top
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)
blocks = []
for l in open(DB / "99-Unresolved-Residual/Unlisted-Code/unlisted-code-blocks.tsv", encoding="utf-8"):
    if l.startswith("#"): continue
    c = l.rstrip("\n").split("\t")
    try: a, s = int(c[0], 16), int(c[1])
    except (ValueError, IndexError): continue
    if a < 0x160000: blocks.append((a, s))
hits = []
for a, s in blocks:
    frac, run, ln, k = best(seq(a, s))
    if run >= 20 and frac >= 0.85: hits.append((a, s, run, ln, k))
for h in hits: print("   %08X %6d B  run %3d of %3d  %s" % h)
check("M1 at least eleven of the 66 head blocks match a named libvpx 1.6.0 routine (run >= 20, >= 85%)", len(blocks) == 66 and len(hits) >= 11,
      "%d blocks matched" % len(hits))
sizes = {}
for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8"):
    c = l.split("\t")
    try: sizes[int(c[0], 16)] = int(c[2])
    except ValueError: pass
random.seed(7)
pool = sorted(f for f, s in sizes.items() if 0x200000 <= f < 0x5E0000 and 200 <= s <= 4000)
null = [best(seq(f, sizes[f]))[1] for f in random.sample(pool, 80)]
check("M2 null control: random game functions never exceed a 10-instruction run", max(null) <= 10, "max run %d" % max(null))
print("FAILS", fails)
sys.exit(1 if fails else 0)
