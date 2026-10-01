# movie_fade_schedule_names.py (FABLE, Claude Opus 5.5, 2026-09-25) - UQ-238.
# Joins the 49-row movie fade schedule (battle_pack.bin directory entry +0x118, st2e, stride 8) to the movie each
# id plays. The player 001B7F30 takes the name from path kind 0x1C: 002DF980(0x1C, id*2) -> g_pathTables[0x1C]
# = 01ECB4D0 (installed by ResourcePath_Init at 002DFAF9/002DFB00), keeps the basename between the last '\' and
# '.', and opens "<video dir><basename>.webm". This reads that .rdata array from the shipping EXE, the schedule
# from the us battle_pack.bin, and the shipped .webm names from the full extract.
# Controls: the st2e header must declare count 49 / stride 8, and byte +0 of every row must equal its index.
# Output: movie-fade-schedule-names.tsv beside this file.
import os, struct
HERE = os.path.dirname(os.path.abspath(__file__))
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
EXTRACT = r"D:\FFXII_TZA_extract"
PACK = os.path.join(EXTRACT, r"ps2data\image\ff12\test_battle\us\binaryfile\battle_pack.bin")
VIDEO = os.path.join(EXTRACT, r"gamedata\d3d11\artdata\video")
KIND28 = 0x01ECB4D0
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = []
for i in range(nsec):
    o = pe + 24 + opt + 40 * i
    vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs.append((0x120000 + va, min(vs, rs), ro))
def off(v):
    for a, s, r in secs:
        if a <= v < a + s:
            return r + v - a
    return None
def path_of(movie_id):
    p = struct.unpack_from("<Q", d, off(KIND28 + 8 * (2 * movie_id)))[0]
    if not p:
        return None
    o = off(p)
    return d[o:d.index(b"\0", o)].decode("latin1")
pack = open(PACK, "rb").read()
start, end = struct.unpack_from("<II", pack, 0x118)
sec = pack[start:end]
assert sec[:4] == b"st2e", sec[:4]
count, stride = struct.unpack_from("<II", sec, 4)
assert (count, stride) == (49, 8), (count, stride)
webm = {f.lower()[:-5] for f in os.listdir(VIDEO) if f.lower().endswith(".webm")}
rows = []
for i in range(count):
    r = sec[0x20 + 8 * i: 0x20 + 8 * i + 8]
    assert r[0] == i, (i, r[0])
    p = path_of(i)
    base = p.rsplit("\\", 1)[-1].rsplit(".", 1)[0] if p else ""
    rows.append((i, base or "-", p or "NULL", "yes" if base.lower() in webm else "no", r.hex(" "),
                 "all-zero" if r[1:] == bytes(7) else ""))
with open(os.path.join(HERE, "movie-fade-schedule-names.tsv"), "w", newline="\n") as w:
    w.write("id\tmovie\tpath_kind_0x1C_entry\twebm_ships\trow_bytes\tnote\n")
    for r in rows:
        w.write("\t".join(str(x) for x in r) + "\n")
print("webm files:", len(webm), "| ids with a name:", sum(1 for r in rows if r[1] != "-"),
      "| ids whose webm ships:", sum(1 for r in rows if r[3] == "yes"))
for r in rows:
    print("%2d %-8s webm=%-3s %s %s" % (r[0], r[1], r[3], r[4], r[5]))
