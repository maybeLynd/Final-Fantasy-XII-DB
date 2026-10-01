"""SWE2-AUDIT-SEM controls for requirements.bucket_members_check and the tracked full census.
1) the tracked full census's bin/dat rows equal my own VBF per-signature counts;
2) mutants of bucket-members.tsv (scratch copies) must each raise a problem."""
import collections, io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\dashboard")
import requirements as R
def sigtext(b):
    if len(b) == 4 and all(0x20 <= c < 0x7f for c in b):
        return "'%s'" % b.decode("latin-1")
    return " ".join("%02X" % c for c in b)

mine = collections.Counter()
for l in io.open(os.path.join(HERE, "vbf_bin_dat.tsv"), encoding="utf-8"):
    if l.startswith("path\t"):
        continue
    p, e, s, h = l.rstrip("\n").split("\t")
    mine[(e, sigtext(bytes.fromhex(h)))] += 1
theirs = collections.Counter()
for l in io.open(R.MAGIC_CENSUS, encoding="utf-8-sig").read().splitlines():
    c = l.split("\t")
    if l.startswith("#") or len(c) < 4 or c[0] not in ("bin", "dat"):
        continue
    theirs[(c[0], c[2].strip())] = int(c[3])
diff = {k: (mine.get(k), theirs.get(k)) for k in set(mine) | set(theirs) if mine.get(k) != theirs.get(k)}
print("full-census bin/dat rows:", len(theirs), " my VBF signatures:", len(mine), " differences:", diff)

src = io.open(R.BUCKET_MEMBERS, encoding="utf-8").read().splitlines(True)
def run(name, lines):
    p = os.path.join(HERE, "mut_%s.tsv" % name)
    io.open(p, "w", encoding="utf-8", newline="").write("".join(lines))
    _, probs = R.bucket_members_check(["bin", "dat"], members_path=p)
    print("MUTANT %-28s problems=%d %s" % (name, len(probs), (probs[:1] or [""])[0][:160]))
    return bool(probs)
ok = True
# drop the summoneffectdata row
ok &= run("drop_summoneffect", [l for l in src if "\tsummoneffectdata\t" not in l])
# change flagrom's split count
ok &= run("flag_split_8", [l.replace("'FLAG'=9\t9", "'FLAG'=8\t8") if "\tflagrom\t" in l else l for l in src])
# claim a signature the census lacks
ok &= run("phantom_sig", [l.replace("\t'dP<d'\t", "\t'dP<e'\t") for l in src])
# entries not equal to takes
ok &= run("entries_mismatch", [l.replace("\tMUS0\t'MUS0'\t2\t", "\tMUS0\t'MUS0'\t3\t") for l in src])
_, base = R.bucket_members_check(["bin", "dat"])
print("unmutated problems:", base)
print("controls", "PASS" if ok and not base and not diff else "FAIL")
