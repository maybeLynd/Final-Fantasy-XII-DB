# section012_model_ids.py (FABLE, Claude Opus 5.5, 2026-09-25) - UQ-334 / UQ-333.
# Writes out the id list section-012.md says the database never stored: every (letter, id) section_012 entry in
# every shipped .ebp, resolved against the obj_finish model stems of the full extract.
#   container: the EBP2 directory slot 12 at +0x40 (file-relative offset, 0 = absent), ebp2-container.md
#   section:   +0x00 u32 count, then count x {u16 id, u16 categoryLetter}, section-012.md 2
#   rule:      letters c / m / n -> <letter><id + 1000>; b / g / s / t -> <letter><id:04>  (section-012.md 5)
# Controls: 842 containers carry the section and 6,771 entries (the sheet's census), else the run refuses;
#           and the n resolution count must reproduce 77 of 112.
# Output: section012-model-ids.tsv beside this file: letter, id, model_stem, resolves, containers.
import io, os, re, sys, struct, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\agent_flow\tools")
import vbfextract as V
VBF = r"D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf"
EXTRACT = r"D:\FFXII_TZA_extract\ps2data\obj_finish"
U16 = lambda b, o: struct.unpack_from("<H", b, o)[0]
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
stems = collections.defaultdict(set)
for root, dirs, files in os.walk(EXTRACT):
    for name in dirs + files:
        m = re.match(r"^([a-z]{1,2})(\d{4})", name.lower())
        if m:
            stems[m.group(1)].add(int(m.group(2)))
f = open(VBF, "rb")
names, blocks = V.load_index(f)
ids = collections.defaultdict(set)
containers = 0
entries = 0
seen = set()
for path in sorted(p for p in names if p.lower().endswith(".ebp") and "/us/" in p.lower()):   # one language, as the sheet counted
    b = V.read_entry(f, names, blocks, path)
    if len(b) < 0x80 or b[:4] != b"EBP2":
        continue
    off = U32(b, 0x40)
    if not off:
        continue
    containers += 1
    count = U32(b, off)
    for k in range(count):
        mid, letter = U16(b, off + 4 + 4 * k), U16(b, off + 6 + 4 * k)
        entries += 1
        ids[(chr(letter), mid)].add(path)
if (containers, entries) != (842, 6771):
    sys.exit("REFUSE: control failed - %d containers, %d entries (expected 842 / 6771)" % (containers, entries))
def stem_of(letter, mid):
    if letter in "cmn":
        return letter, mid + 1000
    return letter, mid
rows = []
for (letter, mid), paths in sorted(ids.items()):
    l, num = stem_of(letter, mid)
    ok = num in stems.get(l, set())
    rows.append((letter, mid, "%s%04d" % (l, num), "yes" if ok else "no", len(paths)))
with open(os.path.join(HERE, "section012-model-ids.tsv"), "w", newline="\n") as w:
    w.write("letter\tid\tmodel_stem\tresolves\tcontainers\n")
    for r in rows:
        w.write("\t".join(str(x) for x in r) + "\n")
n = [r for r in rows if r[0] == "n"]
print("containers", containers, "entries", entries, "| n ids", len(n), "resolve", sum(r[3] == "yes" for r in n))
lo, hi = min(stems["n"]), max(stems["n"])
unres = [r for r in n if r[3] == "no"]
inside = [r for r in unres if lo <= r[1] + 1000 <= hi]
print("n stem range n%d..n%d, stems %d, gaps %d" % (lo, hi, len(stems["n"]), (hi - lo + 1) - len(stems["n"])))
print("unresolved n ids: %d, inside the stem range: %d, outside: %d" % (len(unres), len(inside), len(unres) - len(inside)))
print("  outside:", [r[2] for r in unres if not (lo <= r[1] + 1000 <= hi)])
print("  inside :", [r[2] for r in inside])
for L in "CNS":
    print("letter", L, sorted(r[1] for r in rows if r[0] == L)[:30])
