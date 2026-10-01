"""procedural_stream_census.py - UQ-276: the complete consumer census of the shared procedural random stream, state
01EF93E8 (FABLE, Claude Opus 5.5, 2026-09-26).

The page names two helpers, 003D8E50 (seven steps, [0, A)) and 004005E0 (one step, [0, 1)), and the seeder 00259180.
This census is image-wide over the whole .text section, listed bodies or not.
  P1 every rip-relative operand into the state dword 01EF93E8..EB, at any width, by a raw disp32 sweep confirmed by
     decoding. The functions that touch the state are the ACCESSORS, printed and written to the TSV.
  P2 every rel32 branch (E8 call, E9 jmp, 0F 8x jcc) into any accessor, confirmed at an instruction boundary. The
     functions that branch there are the CALLERS, one hop out. Accessors and callers together are the consumers.
  P3 no accessor's address is taken (no rip-relative lea/mov, no absolute qword in .rdata/.data), so no indirect call
     adds consumers. No data word points into the state's 0x100-byte neighbourhood, and no lea forms a base up to
     0x100 below it.
  P4 controls, the page's own figures:
     - the seed 0x458DC800 is stored at 00259216 in the seeder;
     - 0040AAD0 calls 003D8E50 twice;
     - 004005E0's only caller is 004010A0.
  P5 the page's "paired seed" 022D92E0 is NOT a stream global. It lies inside a 16-byte region that far more
     functions store whole xmm registers to; the count is printed. It is a scratch vector, so it is left out.
Writes procedural-stream-consumers.tsv beside the page. Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import bisect, collections, csv, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM
HERE = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[4]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
optsz = struct.unpack_from("<H", d, pe + 20)[0]
secs = {struct.unpack_from("<8s", d, pe + 24 + optsz + i * 40)[0].rstrip(b"\0").decode():
        struct.unpack_from("<IIII", d, pe + 24 + optsz + i * 40 + 8) for i in range(n)}
def off(v):
    for vs, va, rs, ro in secs.values():
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
F = {}; NAME = {}
for r in list(csv.reader(open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8"), delimiter="\t"))[1:]:
    try: F[int(r[0], 16)] = int(r[2]); NAME[int(r[0], 16)] = r[1]
    except (ValueError, IndexError): pass
ST = sorted(F)
def owner(a):
    i = bisect.bisect_right(ST, a) - 1
    return ST[i] if i >= 0 and a < ST[i] + F[ST[i]] else None
_cache = {}
def body(f):
    if f not in _cache: _cache[f] = {x.address: x for x in cs.disasm(d[off(f):off(f) + F[f]], f)}
    return _cache[f]
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
vs, va, rs, ro = secs[".text"]; T0 = BASE + va; text = d[ro:ro + rs]
def rip_hits(lo, hi):
    """(function, insn) for every instruction with a rip-relative operand into [lo, hi)."""
    out = set()
    for i in range(0, len(text) - 4):
        disp = int.from_bytes(text[i:i + 4], "little", signed=True)
        for imm in (0, 1, 2, 4):
            t = T0 + i + 4 + imm + disp
            if lo <= t < hi:
                f = owner(T0 + i)
                if f is None: out.add((None, T0 + i)); continue
                for a, x in body(f).items():
                    if a < T0 + i < a + x.size and any(op.type == X86_OP_MEM and cs.reg_name(op.mem.base) == "rip"
                                                       and lo <= a + x.size + op.mem.disp < hi for op in x.operands):
                        out.add((f, a))
    return out
STATE = 0x01EF93E8
hits = rip_hits(STATE, STATE + 4)
acc = sorted({f for f, a in hits if f is not None})
unl = sorted(a for f, a in hits if f is None)
print("   accessors (%d): %s" % (len(acc), ", ".join("%08X" % f for f in acc)))
check("P1 the state's accessors are listed bodies, and include the seeder and both page helpers",
      unl == [] and {0x259180, 0x3D8E50, 0x4005E0} <= set(acc), "unlisted hits %s" % ["%08X" % a for a in unl])
# P2 callers of every accessor
callers = collections.defaultdict(collections.Counter); badb = []
accset = set(acc)
for i in range(0, len(text) - 6):
    b0 = text[i]
    L = 1 if b0 in (0xE8, 0xE9) else 2 if (b0 == 0x0F and 0x80 <= text[i + 1] <= 0x8F) else 0
    if not L: continue
    t = T0 + i + L + 4 + int.from_bytes(text[i + L:i + L + 4], "little", signed=True)
    if t in accset:
        f = owner(T0 + i)
        if f is None or (T0 + i) not in body(f): badb.append("%08X" % (T0 + i)); continue
        kind = "call" if b0 == 0xE8 else "jmp" if b0 == 0xE9 else "jcc"
        callers[t][(f, kind)] += 1
cons = set(acc) | {f for t in callers for (f, k) in callers[t]}
for t in acc:
    c = callers.get(t, {})
    print("   %08X %-40s callers %d functions, %d sites %s" % (t, NAME.get(t, "")[:40], len({f for f, k in c}), sum(c.values()),
          sorted({k for f, k in c})))
check("P2 every rel32 branch into an accessor is at an instruction boundary", badb == [], "non-boundary %s" % badb[:5])
# P3 address-taking and displacement reach
taken = []
for i in range(0, len(text) - 4):
    t = T0 + i + 4 + int.from_bytes(text[i:i + 4], "little", signed=True)
    if t in accset:
        f = owner(T0 + i)
        if f is None: continue
        x = next((x for a, x in body(f).items() if a + x.size == T0 + i + 4 and a < T0 + i), None)
        if x is not None and x.mnemonic in ("lea", "mov"): taken.append("%08X %s %s" % (x.address, x.mnemonic, x.op_str))
absq = []
for nm in (".rdata", ".data"):
    _, sva, srs, sro = secs[nm]; blob = d[sro:sro + srs]
    for k in range(0, len(blob) - 7, 8):
        v = struct.unpack_from("<Q", blob, k)[0]
        if v in accset or STATE - 0x100 <= v < STATE + 4: absq.append("%s+%X=%X" % (nm, k, v))
below = sorted({"%08X %s" % (a, body(f)[a].op_str) for f, a in rip_hits(STATE - 0x100, STATE)
                if f is not None and body(f)[a].mnemonic == "lea"})
check("P3 no accessor is address-taken, no data pointer reaches the state, no lea base below it",
      taken == [] and absq == [] and below == [], "taken %s abs %s lea %s" % (taken[:3], absq[:3], below[:3]))
# P4 controls
seed = body(0x259180).get(0x259216)
c40 = callers[0x3D8E50].get((0x40AAD0, "call"), 0)
c10 = set(callers[0x4005E0])
check("P4 controls: seed 0x458DC800 at 00259216; 0040AAD0 calls 003D8E50 twice; 004005E0's only caller is 004010A0",
      seed is not None and seed.op_str.endswith("0x458dc800") and c40 == 2 and c10 == {(0x4010A0, "call")},
      "seed %s; 0040AAD0 x%d; 004005E0 callers %s" % (seed and seed.op_str, c40, c10))
# P5 the paired-seed label
p5 = rip_hits(0x022D92E0 - 0x10, 0x022D92E0 + 4)
wide = {f for f, a in p5 if f is not None and body(f)[a].mnemonic in ("movups", "movdqu", "movaps", "movdqa")}
check("P5 022D92E0 lies in a scratch vector stored whole by many functions (not a stream global)", len(wide) > 50,
      "%d functions store or load a whole xmm there" % len(wide))
with open(HERE.parent / "procedural-stream-consumers.tsv", "w", encoding="utf-8", newline="\n") as fo:
    fo.write("function\tname\troute\n")
    for f in sorted(cons):
        route = []
        if f in accset: route.append("touches the state directly")
        for t in acc:
            k = {kk: v for (ff, kk), v in callers.get(t, {}).items() if ff == f}
            if k: route.append("%s %08X x%d" % ("/".join(sorted(k)), t, sum(k.values())))
        fo.write("%08X\t%s\t%s\n" % (f, NAME.get(f, ""), "; ".join(route)))
print("   consumers: %d functions (%d accessors + %d callers only)" % (len(cons), len(acc), len(cons - set(acc))))
print("FAILS", fails)
sys.exit(1 if fails else 0)
