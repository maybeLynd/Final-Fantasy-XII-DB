"""effect_type_usage.py: which element types the shipped effect corpus actually authors.

Walks every extracted .efx/.efb under Database/Tools/work/DATA/mesh54/fx_all
(the extractor is ../Tools/work/DATA/mesh54/extract_fx.py; 3,698 files). For each
0xA00 element-definition chunk the element type is the record-header byte at
chunk+0xE (the {u16 id, u8 type, u8 pad} triple at +0xC; payload proper begins at
+0x10 and its first byte is 0 in every record). 0x800 chunks are a different
record class - their +0xE is a sub-record subtype bounded 0..8, never an element
type.

Writes effect-type-authored-usage.tsv beside this script: type, chunk count,
file count. Run from the repository root."""
import os, struct, glob, collections
HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\DATA\mesh54\fx_all"
files = [p for p in glob.glob(os.path.join(CORPUS, "**", "*"), recursive=True) if os.path.isfile(p)]
hist = collections.Counter()
fcount = collections.defaultdict(set)
n800 = 0
sub8 = collections.Counter()
for f in files:
    b = open(f, "rb").read()
    cur = 0x10                                 # file header
    while cur + 8 <= len(b):
        ln, _flag, ty = struct.unpack_from("<IHH", b, cur)
        if ln < 8 or cur + ln > len(b):
            break
        if ty == 0xA00:
            t = b[cur + 0xE]
            hist[t] += 1
            fcount[t].add(f)
        elif ty == 0x800:
            n800 += 1
            sub8[b[cur + 0xE]] += 1
        cur += ln
assert n800 and max(sub8) <= 8, "0x800 +0xE out of its sub-record bound"
with open(os.path.join(HERE, "effect-type-authored-usage.tsv"), "w", encoding="utf-8", newline="\n") as fo:
    fo.write("type\tchunks\tfiles\n")
    for t in sorted(hist):
        fo.write("0x%02X\t%d\t%d\n" % (t, hist[t], len(fcount[t])))
print("written: %d distinct types, %d 0xA00 chunks in %d files; %d 0x800 chunks (subtypes %s)"
      % (len(hist), sum(hist.values()), len({f for s in fcount.values() for f in s}),
         n800, sorted(sub8)))
