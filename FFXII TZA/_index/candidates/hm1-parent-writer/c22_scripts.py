# HM-1 (OPUS, 2026-09-27): in the four maps whose manifest loads hc1006_03 (C:22), name the script that calls attach.
import io, os, sys, struct, csv
DB = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA"
sys.path.insert(0, os.path.join(DB, "25-EBP-Script-Container", "Bytecode-And-Opcodes", "members"))
os.chdir(os.path.abspath(os.path.join(DB, "..", "..")))
import gen_req_channel_census as G
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
MAPS = ["dgl_g/dgl_g0102/dgl_g0102", "gol_a/gol_a0200/gol_a0200", "hne_b/hne_b0102/hne_b0102", "rsn_z/rsn_z0200/rsn_z0200"]
att = {}
for r in csv.reader(open(os.path.join(os.environ.get("TEMP", "."), "attach-census.tsv"), encoding="latin1"), delimiter="\t"):
    if r[0] != "file": att.setdefault(r[0], []).append((int(r[1], 16), r[2], r[5]))
f = io.open(G.VBF, "rb"); names, blocks = G.V.load_index(f)
def cstr(b, o): return b[o:b.index(b"\0", o)].decode("cp932", "replace")
for m in MAPS:
    path = "ps2data/plan_master/us/event/%s.ebp" % m
    b = G.V.read_entry(f, names, blocks, path)
    img = b[0x80:0x80 + U32(b, 0x84)]
    diroff, nm = U32(img, 0x18), U32(img, 0x4C); n = U32(img, diroff)
    ents = []
    for si in range(n):
        e = diroff + 4 + si * 0x30
        nameOff, stype, pcid, start, ninstr = struct.unpack_from("<IHHII", img, e)
        ents.append((start, si, cstr(img, nm + nameOff) if nm else str(si), stype))
    ents.sort()
    print("==", m, "scripts", n, "| manifest:", end=" ")
    o = U32(b, 0x40); cnt = U32(b, o)
    print([(chr(struct.unpack_from("<HH", b, o + 4 + 4 * i)[1]), struct.unpack_from("<HH", b, o + 4 + 4 * i)[0]) for i in range(cnt)])
    for pc, verb, args in sorted(att.get(path, [])):
        owner = max((e for e in ents if e[0] <= pc), default=None)
        print("   %-9s pc %5x  args %-22s script #%s '%s' type %s" % (verb, pc, args, owner[1], owner[2], owner[3]))
