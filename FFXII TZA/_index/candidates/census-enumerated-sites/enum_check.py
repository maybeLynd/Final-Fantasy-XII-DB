"""enum_check.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only.

census_receiver_fixpoint's generous join enumerates a loop's induction values (up to BASECAP) and so reaches a callee, or
a [base + disp] operand, at bases the loop's trip count never produces. The over-report is the tool's design - its
negatives are published - but store rows took such POSITIVES as proof of an access. EMIT_JSON now lists
`enumerated_sites`: sites no recording of which is traceable to a seed through single-candidate steps.

  E  control, run live on LegacyPs2GsTextureContext (SEED=ctor 002F6AB0, extent 0x240): the clear 00231F50 reached at
     +0x110 (00231F52) and +0x148 (00231F69), and 002F7236 at +0x23C (a fourth pass of a two-pass loop), are enumerated;
     the first element's clear at +0x40 (00231F52) and the direct bind of +0xA8 (002323DB, `lea rcx, [rsi+0xa8]`) are
     not; and the per-site map is unchanged by the marking
  L  002F6AB0's second loop runs exactly twice: [rsp+0x28] = rdi = 2 at 002F6AEA / 002F6AF6, and only the loop's own
     `sub rax, 1` / store writes it (002F7273 / 002F7277); rbx starts at +0x1E8 with stride 0x18
  A  AUDIT over every type whose TYPE RESOLVED rows cite a census_receiver_fixpoint seed (receipts/, one JSON per seed):
     rows whose census hits are ALL enumerated AND whose cited sites include one of them - i.e. the row rests on the
     enumeration. Rows whose census hits are all enumerated but that cite other evidence are listed, not failed.
  S  REGRESSION: no TYPE RESOLVED row rests on enumerated sites alone (FAILS before the patch: LegacyPs2GsTextureContext
     +0x23C)
Usage: python enum_check.py [--receipt] [--patch]
  --receipt  re-runs the census for every audited seed into receipts/ (several minutes)
  --patch    corrects the rows S names in _types/fields.tsv (mixed EOLs, per line)
"""
import collections, hashlib, json, os, re, struct, subprocess, sys, tempfile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ROOT = os.path.abspath(os.path.join(DB, ".."))
EXE = os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe")
CENSUS = os.path.join(ROOT, "Tools", "analysis-kit", "gfz-scripts", "census_receiver_fixpoint.py")
RCP = os.path.join(HERE, "receipts")
FIELDS = os.path.join(DB, "_types", "fields.tsv"); TYPES = os.path.join(DB, "_types", "types.tsv")
REC = "_index/candidates/census-enumerated-sites/enum_check.py"
d = open(EXE, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
def census(mode, cell, ext, path):
    subprocess.run([sys.executable, CENSUS, cell, "0", ext], env=dict(os.environ, SEED=mode, EMIT_JSON=path),
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=ROOT, check=True)
    return json.load(open(path, encoding="utf-8"))

fl = open(FIELDS, "rb").read().decode("utf-8").splitlines(keepends=True)
def cells(l): return l.rstrip("\r\n").split("\t")
T = {cells(l)[0]: cells(l)[1] for l in open(TYPES, encoding="utf-8").read().splitlines()[1:]}
seeds = collections.defaultdict(set)
for l in fl[1:]:
    c = cells(l)
    if len(c) > 8:
        # a citation carried inside MIGRATED evidence names the SOURCE type's seed, not this row's (2026-09-28)
        own = c[8].split("MIGRATED from")[0]
        for m in re.finditer(r"census_receiver_fixpoint SEED=(\w+) ([0-9A-Fa-f]{8})", own): seeds[c[0]].add((m.group(1), m.group(2)))
if "--receipt" in sys.argv:
    os.makedirs(RCP, exist_ok=True)
    for t, ss in sorted(seeds.items()):
        for mode, cell in sorted(ss): census(mode, cell, T[t], os.path.join(RCP, "%s.%s.%s.json" % (t, mode, cell)))

def rests(t, ss):
    """rows of t whose census hits are all enumerated: [(line index, cells, hits, cited-enumerated)]"""
    sites = collections.defaultdict(set); plain = set()
    for mode, cell in sorted(ss):
        j = json.load(open(os.path.join(RCP, "%s.%s.%s.json" % (t, mode, cell)), encoding="utf-8"))
        en = set(j["enumerated_sites"])
        for k, v in j["sites"].items():
            for s in v:
                sites[k].add(s)
                if "%s:%s" % (k, s) not in en: plain.add((k, s))
    out = []
    for i, l in enumerate(fl):
        c = cells(l)
        if c[0] != t or c[6] != "TYPE RESOLVED": continue
        o, w = int(c[1], 16), int(c[2])
        hits = {(k, s) for k in sites for s in sites[k] if o <= int(k.split(":")[0]) < o + w}
        if hits and not (hits & plain):
            cited = set(re.findall(r"\b00[0-9A-F]{6}\b", c[5] + " " + c[8]))
            out.append((i, c, sorted(s for k, s in hits), sorted(cited & {s for k, s in hits})))
    return out
bad = [(t, r) for t, ss in sorted(seeds.items()) for r in rests(t, ss)]
resting = [(t, r) for t, r in bad if r[3]]

if "--patch" in sys.argv:
    for t, (i, c, hits, cited) in resting:
        eol = fl[i][len(fl[i].rstrip("\r\n")):]
        c = list(c); was = c[4]
        c[3] = "unobservedSpan" + c[1][2:]; c[4] = "u8[%s]" % c[2]; c[6] = "DISCOVERED"; c[7] = "UNKNOWN"
        c[5] = "~~" + c[5] + "~~ NO ESTABLISHED ACCESS: the only census hit (%s) is an ENUMERATED site - the census reached it " \
               "at a loop induction value the loop's trip count does not produce; %s" % (", ".join(cited), REC)
        c[8] = c[8] + " || CORRECTED 2026-09-28 (OPUS, %s S): rested on an enumerated census site alone. WAS %s" % (REC, was)
        fl[i] = "\t".join(c) + eol
    open(FIELDS, "wb").write("".join(fl).encode("utf-8"))
    print("corrected %d row(s)" % len(resting)); sys.exit(0)

tmp = os.path.join(tempfile.mkdtemp(), "lgs.json")
j = census("ctor", "002F6AB0", "0x240", tmp)
en = set(j["enumerated_sites"])
ok = ({"272:8:00231F52", "328:8:00231F69", "572:4:002F7236"} <= en and "64:8:00231F52" not in en
      and "168:8:002323DB" not in en and "002F7236" in j["sites"].get("572:4", {}))
ref = json.load(open(os.path.join(RCP, "LegacyPs2GsTextureContext.ctor.002F6AB0.json"), encoding="utf-8"))
check("E", ok and j["sites"] == ref["sites"], "enumerated: +0x110 / +0x148 clears and the +0x23C read; plain: +0x40 clear, "
      "+0xA8 bind; live run == receipt (%d enumerated sites)" % len(en))
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
off = lambda v: next(v - B - va + ro for vs, va, rs, ro in SECS if B + va <= v < B + va + rs)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
body = list(cs.disasm(d[off(0x2F6AB0):off(0x2F6AB0) + 2118], 0x2F6AB0))
st = [(x.address, x.mnemonic, x.op_str) for x in body if "[rsp + 0x28]" in x.op_str and x.op_str.startswith("qword ptr [rsp + 0x28]")]
at = {x.address: (x.mnemonic, x.op_str) for x in body}
check("L", st == [(0x2F6AF6, "mov", "qword ptr [rsp + 0x28], rdi"), (0x2F7277, "mov", "qword ptr [rsp + 0x28], rax")]
      and at[0x2F6AEA] == ("mov", "edi, 2") and at[0x2F722A] == ("lea", "rbx, [rsi + 0x1e8]")
      and at[0x2F726F] == ("add", "rbx, 0x18") and at[0x2F7273] == ("sub", "rax, 1") and at[0x2F7236] == ("mov", "edi, dword ptr [rbx + 0xc]"),
      "the second loop's count is 2 and only the loop writes it: +0x1E8 and +0x200, so +0x23C (a fourth pass) is not read")
for t, (i, c, hits, cited) in bad:
    print("      %-28s %s %s %-20s all hits enumerated %s; cited among them %s" % (t, c[1], c[2], c[3], hits[:3], cited))
check("A", True, "%d seeded types audited; %d TYPE RESOLVED row(s) with only enumerated hits, %d of them resting on one"
      % (len(seeds), len(bad), len(resting)))
check("S", not resting, "rows resting on enumerated sites alone: %s" % [(t, r[1][1], r[1][3]) for t, r in resting])
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
