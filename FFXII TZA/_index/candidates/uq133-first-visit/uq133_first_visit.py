"""uq133_first_visit.py ATS_DIR - UQ-133: the story progress at which the Vendor of Goods (shop row 24, field fon_b01)
can first be used (FABLE, Claude Opus 5.5, 2026-09-27). DATA: the us battle_pack.bin shop table and the shipped field
and event scripts, decompiled to .ats by ff12-script (ATS_DIR = the decompiled corpus, 1,114 files; fon_b01's listing
is pinned by SHA-256 below).

  R1 row 24 (name 0x1F9, section +0x1338): entry 0 gate kind 2 at 5,100, entry 1 at 3,100, entry 2 at 3,050.
  F1 fon_b01's main(1) plays arrival event 0 when the story counter (シナリオフラグ) is at most 0xBFE (3,070):
     PUSHV counter / PUSHII 0xbfe / OPLSE / POPXNCJMP (skip when false) / PUSHII 0x0 / CALLPOPA eventplay_ec.
  F2 fon_b01 sets the counter to 0xC1C (3,100) in three actor functions, outside the PUSHDBG debug jump table
     (a write is table-borne when three or more counter writes sit within 8 lines of it).
  C1 no script in the corpus writes a counter value in 3,071..3,099 (so first contact is at >= 3,100); control: the
     same census finds writers of 3,070 and of 3,100.
  C2 the counter reaches 5,100 in normal play: a non-debug field script writes 5,100 (gil_d01).
Exit 1 on any FAIL.
"""
import glob, hashlib, os, re, struct, sys, collections
from pathlib import Path
ATS = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[4] / "Tools/work/FABLE/fz21-scratch/ats"
PACK = Path("D:/FFXII_TZA_extract/ps2data/image/ff12/test_battle/us/binaryfile/battle_pack.bin")
FON = ATS / "plan_map_fon_b_fon_b01_global_fon_b01.ats"
FON_SHA = "94537ae1fd9930347019355710236b6fc9d249496cdda8a0d9b1daf4f177d3a6"
CTR = "シナリオフラグ"
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += (not ok)

b = PACK.read_bytes()
s = struct.unpack_from("<I", b, 0xA0)[0]
tag, stride, count, data = struct.unpack_from("<IHHI", b, s)
name, sec = struct.unpack_from("<II", b, s + data + stride * 24)
st, sstride, scount, sdata = struct.unpack_from("<IHHI", b, s + sec)
ents = [struct.unpack_from("<BBHI", b, s + sdata + sstride * j) for j in range(scount)]   # offsets are relative to the shop section base
check("R1 row 24: name 0x1F9, 39 entries, gates 5,100 / 3,100 / 3,050 (kind 2)",
      name == 0x1F9 and sec == 0x1338 and scount == 39 and [(e[0], e[2]) for e in ents[:3]] == [(2, 5100), (2, 3100), (2, 3050)],
      str([(e[0], e[2]) for e in ents[:3]]))

check("F0 the fon_b01 listing is the pinned decompile", hashlib.sha256(FON.read_bytes()).hexdigest() == FON_SHA)
L = [x.strip() for x in FON.read_text(encoding="utf-8").split("\n")]
ops = [re.split(r"\s+", x)[:2] for x in L]
arrive = False
for i in range(len(L) - 6):
    if L[i].startswith("function main(1)") and ops[i + 2][:2] == ["PUSHV", CTR] and ops[i + 3] == ["PUSHII", "0xbfe"] \
       and ops[i + 4][:1] == ["OPLSE"] and ops[i + 5][:1] == ["POPXNCJMP"] and ops[i + 6] == ["PUSHII", "0x0"] \
       and ops[i + 7] == ["CALLPOPA", "eventplay_ec"]:
        arrive = True; break
check("F1 fon_b01 main(1): counter <= 3,070 plays arrival event 0", arrive)

def writes(lines):
    out = []
    for i, x in enumerate(lines):
        if x.startswith("POPV") and CTR in x:
            m = re.match(r"PUSHII\s+(-?0x[0-9a-f]+|-?\d+)", lines[i - 1])
            if m:
                out.append([i, int(m.group(1), 0), False])
    for w in out:   # a switch table: three or more counter writes within +-8 lines (fon_b01's PUSHDBG jump table)
        w[2] = sum(1 for o in out if abs(o[0] - w[0]) <= 8) >= 3
    return [(v, d) for i, v, d in out]
fw = writes(L)
check("F2 fon_b01 writes 3,100 three times outside the debug table", sum(1 for v, d in fw if v == 0xC1C and not d) == 3,
      str([v for v, d in fw if not d]))

allw = collections.defaultdict(set)
files = glob.glob(str(ATS / "*.ats"))
for fn in files:
    for v, d in writes([x.strip() for x in open(fn, encoding="utf-8", errors="replace").read().split("\n")]):
        allw[v].add((os.path.basename(fn), d))
gap = sorted(v for v in allw if 3071 <= v <= 3099)
check("C1 %d scripts: no counter write in 3,071..3,099; writers of 3,070 and 3,100 exist" % len(files),
      len(files) > 1000 and not gap and 3070 in allw and 3100 in allw, "gap=%s" % gap)
check("C2 a non-debug field script writes 5,100", any(not d and f.startswith("plan_map_") for f, d in allw.get(5100, ())),
      str(sorted(allw.get(5100, ()))))
print("FAILS", fails)
sys.exit(1 if fails else 0)
