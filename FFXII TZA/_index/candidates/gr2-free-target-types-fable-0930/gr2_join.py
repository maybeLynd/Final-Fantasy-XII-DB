"""gr2_join.py - GR-2 (FABLE, 2026-09-30): every shipped call of the two verbs that set the actor's free-target type
(setfreetargettype 0x265, stored as is; btlAtelSetUnitType 0x3005, mapped through the table {1, 5, 3, 4} at 01E09EE8 per
SD-160's record), grouped by the TYPE VALUE it produces, with the calling scripts' names. The decode loop is copied
verbatim from OPUS's sd160_census.py (SD-160 record, af6684173); only the output differs.
Control: the per-(verb, argument) counts must equal sd160_census.out's (59,814 / 234 / 297 / 369 and 18 / 315 / 2,340 /
45), or the run refuses to write. Output: gr2_join.out (printed) and gr2-type-scripts.tsv beside this file."""
import collections, io, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB =os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "25-EBP-Script-Container", "Bytecode-And-Opcodes", "members"))
os.chdir(os.path.abspath(os.path.join(DB, "..", "..")))
import gen_req_channel_census as G  # noqa: E402

U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
WANT = {0x265: "setfreetargettype", 0x3005: "btlAtelSetUnitType"}
verbs = G.load_verbs()
f = io.open(G.VBF, "rb")
names, blocks = G.V.load_index(f)
rows, seen, calls_total = [], set(), 0
for path in sorted(p for p in names if p.lower().endswith(".ebp")):
    try:
        b = G.V.read_entry(f, names, blocks, path)
    except Exception:
        continue
    if len(b) < 0x80 or U32(b, 0x80) != 0x8000000B:
        continue
    sec = b[0x80:0x80 + U32(b, 0x84)]
    diroff = U32(sec, 0x18)
    cnt = U32(sec, diroff)
    if cnt > 0x400 or diroff + 4 + cnt * 0x30 > len(sec):
        continue
    pool = U32(sec, 0x4C)  # the name pool; directory entry +0x00 is the script's name offset in it (BW-5)
    sname = {}
    for s in range(cnt):
        o = pool + U32(sec, diroff + 4 + s * 0x30)
        sname.setdefault(U32(sec, diroff + 4 + s * 0x30 + 8), sec[o:sec.find(b"\0", o)].decode("cp932", "replace"))
    starts = sorted(sname)
    bounds = sorted(set(starts) | {diroff, len(sec)})
    for start in starts:
        end = min((x for x in bounds if x > start), default=len(sec))
        if start >= len(sec) or end <= start:
            continue
        ins, _ = G.decode(sec[start:end])
        for j, (pc, op, imm) in enumerate(ins):
            if op not in (0x58, 0x59, 0x5D, 0x5E):
                continue
            calls_total += 1
            if imm not in WANT:
                continue
            key = (path, start + pc)
            if key in seen:
                continue
            seen.add(key)
            v = verbs.get(imm)
            need = (v[0] if v and v[0] is not None else 1) + (1 if op in (0x59, 0x5E) else 0)
            args, st = G.resolve_args(ins, j, need, verbs)
            rows.append((path, sname[start], "%x" % (start + pc), WANT[imm], G.OPN.get(op), st,
                         ";".join("%s:%s" % (a[0], a[1]) for a in args) if args else ""))
if calls_total == 0:
    sys.exit("REFUSE: control failed - no CALL-family site decoded")
print("CALL-family sites decoded: %d | rows: %d" % (calls_total, len(rows)))
by = collections.Counter((r[3], r[6]) for r in rows)
for k, n in sorted(by.items(), key=lambda kv: (kv[0][0], str(kv[0][1]))):
    print("  %5d  %s" % (n, k))
nonconst = [r for r in rows if r[5] != "ok" or not r[6].startswith("PUSHI")]
print("sites whose argument is not a pushed constant: %d" % len(nonconst))
EXPECT = {("btlAtelSetUnitType", "PUSHII:0"): 59814, ("btlAtelSetUnitType", "PUSHII:1"): 234,
          ("btlAtelSetUnitType", "PUSHII:2"): 297, ("btlAtelSetUnitType", "PUSHII:3"): 369,
          ("setfreetargettype", "PUSHII:1"): 18, ("setfreetargettype", "PUSHII:3"): 315,
          ("setfreetargettype", "PUSHII:4"): 2340, ("setfreetargettype", "PUSHII:6"): 45}
if dict(by) != EXPECT:
    sys.exit("REFUSE: control failed - counts differ from sd160_census.out: %r" % dict(by))
MAP = {"btlAtelSetUnitType": {0: 1, 1: 5, 2: 3, 3: 4}}
def ttype(verb, arg):
    v = int(arg.split(":")[-1])
    return MAP[verb][v] if verb in MAP else v
import re
def cls(s):
    m = re.match(r"[A-Za-z]+", s)
    return (m.group(0).lower() if m else s[:4])
per = collections.defaultdict(collections.Counter)
langs = collections.defaultdict(set)
files = collections.defaultdict(set)
for r in rows:
    t = ttype(r[3], r[6])
    per[t][(r[3], r[6].split(":")[-1], r[1])] += 1
    files[(t, r[3], r[6].split(":")[-1])].add(r[0].split("/")[-1])
print()
for t in sorted(per):
    c = per[t]
    print("type %d: %d sites, %d distinct (verb, arg, script)" % (t, sum(c.values()), len(c)))
    pc = collections.Counter()
    for (vb, a, s), n in c.items(): pc[(vb, a, cls(s))] += n
    for k, n in pc.most_common(12): print("    %6d  %s(%s)  script class %r" % (n, k[0], k[1], k[2]))
    for k, n in c.most_common(8): print("      e.g. %6d  %s(%s)  %s" % (n, k[0], k[1], k[2]))
print()
for k in sorted(files):
    if k[0] == 1: continue
    fs = sorted(files[k]); print("files type %d %s(%s): %d  %s" % (k[0], k[1], k[2], len(fs), " ".join(fs[:40])))
with open(os.path.join(HERE, "gr2-type-scripts.tsv"), "w", newline="\n", encoding="utf-8") as w:
    w.write("type\tverb\targ\tscript\tsites\n")
    for t in sorted(per):
        for (vb, a, s), n in sorted(per[t].items(), key=lambda kv: -kv[1]):
            w.write("%d\t%s\t%s\t%s\t%d\n" % (t, vb, a, s, n))
