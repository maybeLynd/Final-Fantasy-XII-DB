"""sd160_census.py - SD-160: which shipped scripts give their actor free-target type 3 (OPUS, 2026-09-30).
Every call, in every shipped .ebp, of the two script verbs that write the actor's free-target type nibble (AL-3):
setfreetargettype (call 0x265) and btlAtelSetUnitType (call 0x3005), each taking one int. It reuses FABLE's decoder
(25-EBP-Script-Container/Bytecode-And-Opcodes/members/gen_req_channel_census.py) exactly as
20-Platform-Online-Achievements/members/script_award_verb_census.py does.
Control: the decoded CALL-family site count must be non-zero, or the run refuses to write.
Output: sd160-census.tsv (the type-3 sites) and sd160-type3-scripts.tsv beside this file; the full-corpus counts by
verb and argument are printed (sd160_census.out).
"""
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
# type 3 comes from setfreetargettype(3) (stored as is by 00269FE0) or btlAtelSetUnitType(2) (00510340 -> 002396B0
# stores the table {1, 5, 3, 4} at 01E09EE8 [v] into the unit's +0x58, which the refresh copies into the nibble)
T3 = {("setfreetargettype", "3"), ("btlAtelSetUnitType", "2")}
t3 = [r for r in rows if (r[3], r[6].split(":")[-1]) in T3]
print("type-3 sites: %d in %d files" % (len(t3), len(set(r[0] for r in t3))))
with open(os.path.join(HERE, "sd160-census.tsv"), "w", newline="\n", encoding="utf-8") as w:  # the type-3 sites only
    w.write("file\tscript\tpc\tverb\topcode\tstatus\targs_push_order\n")
    for r in t3:
        w.write("\t".join(str(x) for x in r) + "\n")
# the plan_master copies per language: strip the language segment and check the copies carry the same sites
langs = collections.defaultdict(set)
for r in t3:
    parts = r[0].split("/")
    key = "/".join(parts[:2] + parts[3:]) if len(parts) > 3 and parts[1] == "plan_master" else r[0]
    langs[key].add((parts[2] if parts[1] == "plan_master" else "-", r[1], r[2], r[3]))
# the pc differs between language copies (their sections differ in size), so the copies are compared by (script, verb)
same = 0
for k, v in langs.items():
    by_l = collections.defaultdict(collections.Counter)
    for l, s, _, vb in v:
        by_l[l][(s, vb)] += 1
    same += len(set(frozenset(c.items()) for c in by_l.values())) == 1
print("zone files: %d (language copies carry the same (script, verb) sites in %d)" % (len(langs), same))
per = collections.OrderedDict()
for k in sorted(langs):
    per[k] = sorted(set((vb, s) for _, s, _, vb in langs[k]))
with open(os.path.join(HERE, "sd160-type3-scripts.tsv"), "w", newline="\n", encoding="utf-8") as w:
    w.write("zone_file\tverb\tscript\tsites_per_language\n")
    for k, v in per.items():
        for vb, s in v:
            w.write("%s\t%s\t%s\t%d\n" % (k.split("/")[-1], vb, s, len(set(p for l, s2, p, v2 in langs[k] if s2 == s and v2 == vb and l == min(x[0] for x in langs[k])))))
names = collections.Counter(s for v in per.values() for _, s in v)
print("distinct script names: %d; most common:" % len(names))
for s, n in names.most_common(30):
    print("  %3d  %s" % (n, s))
zones = collections.Counter(k.split("/")[-1][:3] for k in per)
print("zone families: %s" % dict(sorted(zones.items())))
