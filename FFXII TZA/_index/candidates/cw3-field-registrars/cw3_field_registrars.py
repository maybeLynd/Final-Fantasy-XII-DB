"""cw3_field_registrars.py - CW-3: every field name a shipped Phyre cluster declares is registered by this build
(FABLE, Claude Opus 5.5, 2026-09-26; found by a delegated read-only pass, re-derived here from the extract and the
bytes).

The recovered field schema (phyre-field-schema.tsv) is a census of one member registrar, 00632960. The engine has
three more, and the schema never counted their sites:
  - 00632A10 calls 00632960 and then installs the array-member vtable (the form CL-1 names);
  - 00632A70 and 00632BE0 each build the member record through the shared base 00632FB0.
  R1 the corpus: the member names declared by every distinct packed namespace of every .phyre in the extract
     (member record word 0 is the name offset into the string pool).
  R2 the schema misses some of them; this script counts how many.
  R3 each registrar's direct call sites, image-wide, each with its name argument: the last `lea r9, [rip+X]` before
     the call in the same function.
     Control: the same resolver recovers nearly all of the schema's own names at 00632960 sites.
  R4 every corpus name the schema misses is registered at a site of 00632A10, 00632A70 or 00632BE0. None is left.
Prints PASS/FAIL per check; exit 1 on any FAIL.
"""
import bisect, csv, re, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
ROOT = Path(__file__).resolve().parents[5]
DB = ROOT / "Database/FFXII TZA"
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
funcs = {}
for line in open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8", errors="replace"):
    p = line.rstrip("\n").split("\t")
    try: funcs[int(p[0], 16)] = int(p[2])
    except (ValueError, IndexError): pass
starts = sorted(funcs)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
fails = 0
def check(nm, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, detail)); fails += (not ok)
EX = Path(sys.argv[1] if len(sys.argv) > 1 else "D:/FFXII_TZA_extract")
corpus = set(); pools = set(); nfiles = 0
for p in EX.rglob("*.phyre"):
    nfiles += 1
    with open(p, "rb") as f:
        h = f.read(12)
        if len(h) < 12: continue
        hs, ns = struct.unpack_from("<II", h, 4); f.seek(hs); b = f.read(ns)
    if len(b) < 0x20: continue
    A_, nC, nM, sp = struct.unpack_from("<IIII", b, 8)
    base = 0x20 + 4 * A_; mb = base + 36 * nC; pool = b[mb + 24 * nM:mb + 24 * nM + sp]
    key = (pool, b[mb:mb + 24 * nM])
    if key in pools: continue
    pools.add(key)
    for k in range(nM):
        o = struct.unpack_from("<I", b, mb + 24 * k)[0]
        corpus.add(pool[o:pool.find(b"\0", o)].decode("latin-1"))
schema = {r["member"] for r in csv.DictReader(open(DB / "22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/phyre-field-schema.tsv", encoding="utf-8"), delimiter="\t") if r.get("member")}
absent = sorted(corpus - schema)
print("   .phyre %d, distinct namespaces %d, corpus member names %d, schema names %d, corpus names not in the schema %d"
      % (nfiles, len(pools), len(corpus), len(schema), len(absent)))
check("R1/R2 the corpus is read and the schema misses some of its names", len(corpus) > 300 and 0 < len(absent) < len(corpus))
vs, va, rs, ro = secs[0]
def sites(t):
    out = []; k = d.find(b"\xE8", ro)
    while 0 <= k < ro + rs - 5:
        a = BASE + va + k - ro
        if a + 5 + struct.unpack_from("<i", d, k + 1)[0] == t: out.append(a)
        k = d.find(b"\xE8", k + 1)
    return out
def name_at(site):
    s = starts[bisect.bisect_right(starts, site) - 1]
    last = None
    for x in cs.disasm(d[off(s):off(site) + 5], s):
        if x.address >= site: break
        dst = x.op_str.split(",")[0].strip()
        if dst in ("r9", "r9d"):
            m = re.search(r"rip \+ (0x[0-9a-f]+)\]", x.op_str)
            last = x.address + x.size + int(m.group(1), 16) if (x.mnemonic == "lea" and m) else None
        if x.mnemonic == "call": last = None
    if last is None or off(last) is None: return None
    o = off(last); return d[o:d.find(b"\0", o)].decode("latin-1")
names = {}
for t in (0x632960, 0x632A10, 0x632A70, 0x632BE0):
    ss = sites(t); nm = [name_at(s) for s in ss]
    names[t] = {x for x in nm if x}
    print("   %08X: %d call sites, %d names resolved" % (t, len(ss), sum(1 for x in nm if x)))
got = len(schema & names[0x632960])
check("R3 control: the resolver recovers the schema's own names at 00632960 sites", got >= 0.95 * len(schema), "%d of %d" % (got, len(schema)))
other = names[0x632A10] | names[0x632A70] | names[0x632BE0]
left = [m for m in absent if m not in other and m not in names[0x632960]]
by = {hex(t): len([m for m in absent if m in names[t]]) for t in (0x632A10, 0x632A70, 0x632BE0)}
check("R4 every corpus name the schema misses is registered at a 00632A10 / 00632A70 / 00632BE0 site", left == [],
      "absent %d; by registrar %s; left %s" % (len(absent), by, left))
print("FAILS", fails)
sys.exit(1 if fails else 0)
