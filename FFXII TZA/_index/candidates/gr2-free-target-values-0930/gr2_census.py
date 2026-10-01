"""gr2_census.py - GR-2 (OPUS, 2026-09-30), reusing sd160_census.py's decoding loop verbatim. SD-160: which shipped scripts give their actor free-target type 3 (OPUS, 2026-09-30).
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
import re as _re
TAB = {0: 1, 1: 5, 2: 3, 3: 4}      # btlAtelSetUnitType -> 002396B0 stores {1, 5, 3, 4}[v] (0 when v > 3) from 01E09EE8
def typ(verb, a):
    v = int(a.split(":")[-1])
    return v if verb == "setfreetargettype" else TAB.get(v, 0)
def lang_free(p):                    # plan_master copies differ only in the language segment
    return _re.sub(r"/plan_master/[a-z]{2}/", "/plan_master/*/", p)
by = collections.defaultdict(collections.Counter); files = collections.defaultdict(set); calls = collections.Counter()
for r in rows:
    if r[5] != "ok" or not r[6].startswith("PUSHI"):
        continue
    t = typ(r[3], r[6]); calls[(t, r[3])] += 1
    by[t][r[1]] += 1; files[t].add(lang_free(r[0]))
print("CALL-family sites decoded: %d | rows: %d" % (calls_total, len(rows)))
for (t, verb), n in sorted(calls.items()):
    print("type %d <- %-20s %6d calls" % (t, verb, n))
for t in sorted(by):
    print("type %d: %d distinct scripts in %d language-folded files; top: %s" % (t, len(by[t]), len(files[t]),
          ", ".join("%s x%d" % kv for kv in by[t].most_common(14))))
with open(os.path.join(HERE, "gr2-values.tsv"), "w", newline="\n", encoding="utf-8") as w:
    w.write("type\tscript\tcalls\n")
    for t in sorted(by):
        for s, n in sorted(by[t].items(), key=lambda kv: -kv[1]):
            w.write("%d\t%s\t%d\n" % (t, s, n))
