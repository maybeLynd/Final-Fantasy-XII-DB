"""SWE2-AUDIT-SEM: bind bucket-member-units.tsv to my own VBF census (vbf_bin_dat.tsv).
Locale folding is mine: drop one path segment that is a locale directory. Each VBF entry must land on
exactly one units.tsv row whose signature equals the entry's own leading 4 bytes, and each row's
entry count must equal the number of VBF entries landing on it."""
import collections, io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA"
UNITS = os.path.join(DB, "_index", "candidates", "bucket-members-0929", "bucket-member-units.tsv")
MEM = os.path.join(DB, "_index", "bucket-members.tsv")
LOC = {"ch", "cn", "de", "es", "fr", "in", "it", "kr", "us", "jp", "in_sdver"}

def sigtext(b):
    if len(b) == 4 and all(0x20 <= c < 0x7f for c in b):
        return "'%s'" % b.decode("latin-1")
    return " ".join("%02X" % c for c in b)

def fold(p):
    segs = p.split("/")
    out = [s for i, s in enumerate(segs[:-1]) if s not in LOC] + [segs[-1]]
    return "/".join(out)

vbf = []
for l in io.open(os.path.join(HERE, "vbf_bin_dat.tsv"), encoding="utf-8"):
    if l.startswith("path\t"):
        continue
    p, e, s, h = l.rstrip("\n").split("\t")
    vbf.append((e, p, fold(p), sigtext(bytes.fromhex(h))))

rows = {}
for l in io.open(UNITS, encoding="utf-8"):
    if l.startswith("#") or l.startswith("ext\t"):
        continue
    c = l.rstrip("\r\n").split("\t")
    rows[(c[0], c[1], c[2])] = (int(c[3]), c[4])

got = collections.Counter()
miss = []
for e, p, u, s in vbf:
    k = (e, u, s)
    if k in rows:
        got[k] += 1
    else:
        # a printable-looking signature the producer writes as hex, or vice versa
        alt = [r for r in rows if r[0] == e and r[1] == u]
        miss.append((p, u, s, alt))
bad = [(k, rows[k][0], got[k]) for k in rows if rows[k][0] != got[k]]
print("VBF .bin/.dat entries:", len(vbf), dict(collections.Counter(v[0] for v in vbf)))
print("units.tsv rows:", len(rows), " distinct units:", len({(k[0], k[1]) for k in rows}))
print("entries not landing on a units row (my folding/signature):", len(miss))
for m in miss[:15]:
    print("  MISS", m)
print("rows whose count differs from my VBF count:", len(bad))
for b in bad[:15]:
    print("  BAD", b)
# per family entry totals vs bucket-members.tsv
fam = collections.Counter()
famu = collections.defaultdict(set)
for (e, u, s), (n, f) in rows.items():
    fam[(e, f)] += got[(e, u, s)]
    famu[(e, f)].add(u)
mb = []
for l in io.open(MEM, encoding="utf-8"):
    if l.startswith("#") or l.startswith("ext\t"):
        continue
    c = l.rstrip("\r\n").split("\t")
    if fam[(c[0], c[1])] != int(c[3]) or len(famu[(c[0], c[1])]) != int(c[4]):
        mb.append((c[0], c[1], c[3], c[4], fam[(c[0], c[1])], len(famu[(c[0], c[1])])))
print("bucket-members.tsv rows whose entries/units differ from the VBF-bound units:", len(mb), mb[:10])
# signature split check: signatures carried by >1 family
sf = collections.defaultdict(set)
for (e, u, s), (n, f) in rows.items():
    sf[(e, s)].add(f)
print("signatures held by more than one family:")
for k, v in sorted(sf.items()):
    if len(v) > 1:
        print("  ", k, sorted(v))
print("FAILS", int(bool(miss)) + int(bool(bad)) + int(bool(mb)))
