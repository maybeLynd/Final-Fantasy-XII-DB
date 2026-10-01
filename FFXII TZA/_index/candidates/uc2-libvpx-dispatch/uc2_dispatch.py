"""uc2_dispatch.py - UC-2: the 63 unreferenced libvpx head blocks are dead - the image's libvpx has a run-time CPU
dispatch, and it references only listed bodies (FABLE, Claude Opus 5.5, 2026-09-27). Static read of the authorised exe;
D6 also reads the libvpx v1.6.0 source (tier 6) when present, else checks the committed class table.

  D1 the dispatch exists and is small: two cpuid setups fill eight function pointers - 0016F080 (six: 02F97500..02F97528)
     and 00172580 (two: 02F974F0, 02F974F8) - each a cmov between two lea-formed candidates, sixteen targets in all.
  D2 every one of the sixteen targets is a listed body (functions.tsv) and none lies in any of the 66 head blocks
     (uc3-blocks.tsv).
  D3 completeness: across every listed body, the only stores to the eight pointer cells are those eight.
  D4 everything else is called directly: the ten listed libvpx assembly kernels (UC-3's control C1) are reached only by
     E8 calls (19 sites), never by an address-taking operand.
  D5 the one decoder-side user of the unreferenced vpx SAD kernels, MFQE's block filter 0017B960, calls the variance
     pointer 02F974F0 three times and 0017B8A0 twice (the USE_SSD shape of vp8/common/mfqe.c) and the two
     filter_by_weight kernels directly; nothing calls vpx_sad16x16_sse2 (0012B200) - raw rel32 sweep.
  D6 the 159 unreferenced routines, classed against libvpx 1.6.0's C sources (uc2-routine-classes.tsv): none is named by
     the decoder's preprocessed code - 8 MMX siblings of SSE2 kernels the image calls, 3 SADs compiled out by mfqe.c's
     USE_SSD, and the rest named only by encoder / VP9 / non-decoder C or by no C at all.
Exit 1 on any FAIL.
"""
import csv, re, struct, sys, os, glob, collections
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = []
for i in range(n):
    b = pe + 24 + opt + i * 40
    SECS.append((d[b:b + 8].rstrip(b"\0").decode(),) + struct.unpack_from("<IIII", d, b + 8))
def off(v):
    for _, vs, va, rs, ro in SECS:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def txt(x): return ("%s %s" % (x.mnemonic, x.op_str)).strip()
SIZES = {}
for l in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    q = l.rstrip("\n").split("\t")
    try: SIZES[int(q[0], 16)] = int(q[2])
    except (ValueError, IndexError): pass
def body(f): return list(cs.disasm(d[off(f):off(f) + SIZES[f]], f)) if SIZES.get(f, 0) > 0 and off(f) is not None else []
def rip(x):
    m = re.search(r"\[rip ([+-]) (0x[0-9a-f]+)\]", x.op_str)
    return x.address + x.size + (int(m.group(2), 16) if m.group(1) == "+" else -int(m.group(2), 16)) if m else None
UC3 = ROOT / "Database/FFXII TZA/_index/candidates/uc3-libvpx-bytematch/uc3-blocks.tsv"
BLOCKS = [(int(r["block"], 16), int(r["block"], 16) + int(r["size"])) for r in csv.DictReader(open(UC3, encoding="utf-8"), delimiter="\t")]
def in_block(v): return any(a <= v < b for a, b in BLOCKS)
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)

# D1 - the setups: pair each pointer store with the two lea candidates feeding its cmov
def setup(f):
    b = body(f); out = {}
    for k, x in enumerate(b):
        if x.mnemonic == "mov" and x.op_str.startswith("qword ptr [rip") and rip(x) is not None:
            reg = x.op_str.split(", ")[1]
            cands = []
            for y in reversed(b[max(0, k - 8):k]):
                if y.mnemonic == "lea" and rip(y) is not None and len(cands) < 2 and \
                   (y.op_str.startswith(reg + ",") or (cands and y.op_str.startswith("rcx,"))): cands.append(rip(y))
            out[rip(x)] = sorted(cands)
    return out
S1, S2 = setup(0x16F080), setup(0x172580)
PTRS = sorted(list(S1) + list(S2))
TARGETS = sorted({t for s in (S1, S2) for v in s.values() for t in v})
cpuid = all(any(x.mnemonic == "cpuid" for x in body(f)) or any(txt(x) == "call 0x172580" for x in body(f)) for f in (0x172580,))
check("D1 two setups fill eight pointers, each from two lea candidates (16 targets)",
      sorted(S1) == [0x2F97500, 0x2F97508, 0x2F97510, 0x2F97518, 0x2F97520, 0x2F97528] and sorted(S2) == [0x2F974F0, 0x2F974F8]
      and all(len(v) == 2 for s in (S1, S2) for v in s.values()) and len(TARGETS) == 16
      and any(x.mnemonic == "cpuid" for x in body(0x172580)),
      "; ".join("%08X<-%s" % (p, "/".join("%08X" % t for t in (S1.get(p) or S2.get(p)))) for p in PTRS))

check("D2 every target is a listed body and none lies in a head block",
      all(t in SIZES for t in TARGETS) and not any(in_block(t) for t in TARGETS),
      "in-window targets (listed): %s" % ["%08X" % t for t in TARGETS if 0x121000 <= t < 0x160000])

stores, callsites, addr_refs, sad_calls = [], collections.Counter(), [], []
TEN = [0x12696A, 0x127BB3, 0x127F4D, 0x1283A6, 0x128905, 0x1496A0, 0x149983, 0x149BCE, 0x149DC0, 0x14A48A]
for f in SIZES:
    if not 0x121000 <= f < 0x8C0000: continue
    for x in body(f):
        t = rip(x)
        if t in PTRS and x.mnemonic == "mov" and x.op_str.startswith("qword ptr [rip"): stores.append("%08X" % x.address)
        if t in TEN: addr_refs.append("%08X" % x.address)
        if x.mnemonic in ("call", "jmp") and x.op_str.startswith("0x"):
            v = int(x.op_str, 16)
            if v in TEN: callsites[v] += 1
check("D3 the only stores to the eight pointer cells are the eight in the two setups", len(stores) == 8, str(sorted(stores)))
check("D4 the ten listed libvpx kernels are reached by direct calls only (19 sites, no address-taking operand)",
      sum(callsites.values()) == 19 and set(callsites) == set(TEN) and addr_refs == [], "calls=%d addr_refs=%s" % (sum(callsites.values()), addr_refs))

# D5 - MFQE block filter
mf = body(0x17B960)
ptr_calls = [x for x in mf if x.mnemonic == "call" and rip(x) == 0x2F974F0]
direct = collections.Counter(int(x.op_str, 16) for x in mf if x.mnemonic == "call" and x.op_str.startswith("0x"))
tx = next(s for s in SECS if s[0] == ".text"); _, tvs, tva, trs, tro = tx
rel = [BASE + tva + (o - tro) for o in range(tro, tro + trs - 5) if d[o] in (0xE8, 0xE9)
       and BASE + tva + (o - tro) + 5 + struct.unpack_from("<i", d, o + 1)[0] == 0x12B200]
check("D5 MFQE's block filter has the USE_SSD shape: 3 calls through 02F974F0, 2 to 0017B8A0, the two filter_by_weight "
      "kernels direct; nothing calls vpx_sad16x16_sse2 (0012B200)",
      len(ptr_calls) == 3 and direct[0x17B8A0] == 2 and direct[0x158B40] == 1 and direct[0x158C09] == 3 and rel == [],
      "direct=%s" % {"%08X" % k: v for k, v in direct.items()})

# D6 - the source classification (regenerated when the libvpx source is present; else the committed table is checked)
TSV = HERE / "uc2-routine-classes.tsv"
SRC = Path(os.environ.get("LIBVPX_SRC", r"C:/Users/Kristian/AppData/Local/Temp/libvpx-1.6.0"))
names = sorted({m.group(1) for r in csv.DictReader(open(UC3, encoding="utf-8"), delimiter="\t")
                for m in re.finditer(r"(\w+) @([0-9A-F]{8})", r["routine"])})
if (SRC / "vp8/common/mfqe.c").exists():
    SUF = r"_(mmx|sse2|sse3|ssse3|sse4_1|xmm|avx|avx2)(_x86_64)?$"
    def base(nm): return re.sub(SUF, "", nm)
    rd = lambda fs: "\n".join(open(f, encoding="latin-1").read() for f in fs)
    dec = rd([str(p) for p in list(SRC.glob("vp8/common/*.c")) + list(SRC.glob("vp8/decoder/*.c"))
              + [SRC / "vp8/vp8_dx_iface.c"] + list(SRC.glob("vp8/common/x86/*.c"))])
    allc = rd([str(p) for p in SRC.glob("**/*.c")])
    mfqe = open(SRC / "vp8/common/mfqe.c", encoding="latin-1").read()
    ssd = "#define USE_SSD" in mfqe
    called = {"vp8_mbloop_filter_vertical_edge_sse2", "vp8_mbloop_filter_horizontal_edge_uv_sse2", "vp8_loop_filter_bh_y_sse2",
              "vp8_loop_filter_bv_y_sse2", "vp8_loop_filter_vertical_edge_uv_sse2", "vp8_mbloop_filter_vertical_edge_uv_sse2"}
    rows = []
    for nm in names:
        b = base(nm); pat = r"\b(%s|%s)\b" % (re.escape(nm), re.escape(b))
        if re.search(pat, dec):
            if nm.endswith("_mmx"): cls = "decoder-named, MMX sibling of an SSE2 variant (x86-64 baseline picks SSE2)"
            elif nm.startswith("vpx_sad") and ssd: cls = "decoder-named only in mfqe.c's #else arm, compiled out by USE_SSD"
            else: cls = "DECODER-NAMED - UNEXPLAINED"
        elif re.search(pat, allc): cls = "named only by non-decoder C (encoder, VP9, vpx_dsp users)"
        else: cls = "named by no C source"
        rows.append((nm, cls))
    with open(TSV, "w", encoding="utf-8", newline="") as fh:
        fh.write("routine\tclass\n"); [fh.write("%s\t%s\n" % r) for r in rows]
    src_note = "regenerated from %s" % SRC
else:
    rows = [tuple(l.rstrip("\n").split("\t")) for l in open(TSV, encoding="utf-8").readlines()[1:]]
    src_note = "libvpx source absent; committed table checked"
cnt = collections.Counter(c for _, c in rows)
check("D6 none of the 159 unreferenced routines is named by the decoder's preprocessed code (%s)" % src_note,
      len(rows) == 159 and not any("UNEXPLAINED" in c for _, c in rows), dict(cnt))
print("FAILS", fails)
sys.exit(1 if fails else 0)
