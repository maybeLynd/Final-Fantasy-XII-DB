# HM-1 (OPUS, 2026-09-27): which maps load the c1006 model (section_012 manifest), and which of them call attach.
import io, os, sys, re, struct, collections, csv
DB = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA"
PS2 = r"D:/FFXII_TZA_extract/ps2data"
sys.path.insert(0, os.path.join(DB, "25-EBP-Script-Container", "Bytecode-And-Opcodes", "members"))
os.chdir(os.path.abspath(os.path.join(DB, "..", "..")))
import gen_req_channel_census as G
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
fl = open(PS2 + "/image/ff12/ch/bin/filelistlocalin.bin", "rb").read()
fsecs = struct.unpack_from("<38I", fl, 0)
def sec(k):
    s = fsecs[k]; c = struct.unpack_from("<I", fl, s)[0]
    return [fl[o:fl.index(b"\0", o)].decode("latin1") if o else "" for o in struct.unpack_from("<%dI" % c, fl, s + 4)]
base = lambda p: p.split("\\")[-1]
k14 = sec(14); k15 = sec(15)
cN = [j // 25 for j in range(0, len(k14), 25) if base(k14[j]).startswith("c1006")]
CM = [j for j, p in enumerate(k15) if base(p).startswith("hc1006")]
print("c1006 -> c:N", cN, [base(k14[25 * n]) for n in cN]); print("hc1006 -> C:M", [(m, base(k15[m])) for m in CM])
want = {("c", n) for n in cN} | {("C", m) for m in CM}
f = io.open(G.VBF, "rb"); names, blocks = G.V.load_index(f)
hits = collections.defaultdict(set)
for path in sorted(p for p in names if p.lower().endswith(".ebp") and "/us/" in p.replace("\\", "/")):
    try: b = G.V.read_entry(f, names, blocks, path)
    except Exception: continue
    if len(b) < 0x80 or b[:4] != b"EBP2": continue
    o = U32(b, 0x40)
    if not o: continue
    cnt = U32(b, o)
    for i in range(min(cnt, 64)):
        idv, let = struct.unpack_from("<HH", b, o + 4 + 4 * i)
        if (chr(let) if 32 < let < 127 else "?", idv) in want: hits[path].add((chr(let), idv))
print("us maps whose manifest loads c1006/hc1006:", len(hits))
att = collections.defaultdict(list)
for r in csv.reader(open(os.path.join(os.environ.get("TEMP", "."), "attach-census.tsv"), encoding="latin1"), delimiter="\t"):
    if r[0] != "file" and r[2] == "attach": att[r[0]].append(r[5])
for p in sorted(hits):
    print(" ", p, sorted(hits[p]), "attach sites:", len(att.get(p, [])), att.get(p, [])[:6])
