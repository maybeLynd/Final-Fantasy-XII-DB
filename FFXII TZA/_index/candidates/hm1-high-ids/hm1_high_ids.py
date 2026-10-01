"""HM-1: what highmodelreplace.bin's upper-case ids name (OPUS, 2026-09-27). Control..

Records (the loader's own variable-length shape, HM-1 2026-09-15): {u32 id; i32 b; i32 c; {u32 id; u32 x}[..]; FFFFFFFF},
ended by a lone FFFFFFFF. An id is {u16 number; u16 ASCII letter}.
  H1 22 records; the upper-case replacement letters are C / N / S only
  H2 reading an upper-case id X:M as entry M of the PS2 disc file list's (filelistlocalin.bin) high-model kind -
     C -> kind 15 (obj_finish\\in\\high\\c*), N -> kind 20 (high\\n*), S -> kind 24 (high\\s*) - every id lands on a .cm file
  H3 the discriminator: those kind lists are NOT in model-number order (kind 15 entry 8 is hc1011, entry 9 hc1005), yet the
     resolved model numbers rise strictly in record order within each letter (C: 14 records, N: 6, S: 2), and c:11's two
     replacements C:26 / C:43 resolve to two variants of ONE model (hc1021_03 / hc1021_13) - which a wrong index would not do
  H4 a lower-case id x:N is the Nth .cm file of its model kind (c -> 14, n -> 19, s -> 23; those lists interleave .cm and
     .ca, so the raw entry index is NOT it), and in all 22 records the source and every replacement name ONE model number
Not claimed: how the executable turns a letter into a kind.
"""
import struct, sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else r"D:/FFXII_TZA_extract/ps2data")
fl = (ROOT / "image/ff12/ch/bin/filelistlocalin.bin").read_bytes()
secs = struct.unpack_from("<38I", fl, 0)


def sec(k):
    s = secs[k]; c = struct.unpack_from("<I", fl, s)[0]
    return [fl[o:fl.index(b"\0", o)].decode("latin1") if o else "" for o in struct.unpack_from("<%dI" % c, fl, s + 4)]


KIND = {"C": sec(15), "N": sec(20), "S": sec(24)}
b = (ROOT / "add_motion/highmodelreplace.bin").read_bytes()
w = struct.unpack_from("<%dI" % (len(b) // 4), b, 0)
i = 0; recs = []
while w[i] != 0xFFFFFFFF:
    idw = w[i]; i += 3; reps = []
    while w[i] != 0xFFFFFFFF:
        reps.append(w[i]); i += 2
    i += 1; recs.append((idw, reps))
fails = 0


def check(nm, ok, d=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", nm, d)); fails += (not ok)


letters = {chr(r >> 16) for _, reps in recs for r in reps}
check("H1 22 records; replacement letters C/N/S", len(recs) == 22 and letters == {"C", "N", "S"}, str(sorted(letters)))
res = [[(chr(r >> 16), KIND[chr(r >> 16)][r & 0xFFFF]) for r in reps] for _, reps in recs]
check("H2 every upper-case id is a .cm in its letter's high-model kind", all(p.endswith(".cm") for rr in res for _, p in rr))
num = lambda p: int(p.split("\\")[-1][2:6])
ok = True; seqs = {}
for rr in res:
    L, p = rr[0]
    seqs.setdefault(L, []).append(num(p))
for L, s in seqs.items():
    ok &= all(s[k] < s[k + 1] for k in range(len(s) - 1))
unsorted15 = num(KIND["C"][8]) > num(KIND["C"][9])
two = [rr for rr in res if len(rr) == 2]
check("H3 resolved models rise strictly per letter in record order although the lists are unsorted; the double record is one model",
      ok and unsorted15 and len(two) == 1 and num(two[0][0][1]) == num(two[0][1][1]),
      str({L: s for L, s in seqs.items()}))
LOW = {"c": [p for p in sec(14) if p.endswith(".cm")], "n": [p for p in sec(19) if p.endswith(".cm")],
       "s": [p for p in sec(23) if p.endswith(".cm")]}
pairs_ok = 0
for (idw, reps), rr in zip(recs, res):
    src = LOW[chr(idw >> 16)][idw & 0xFFFF].split("\\")[-1]
    srcnum = src[1:5]
    if all(p.split("\\")[-1][2:6] == srcnum for _, p in rr):
        pairs_ok += 1
check("H4 a lower-case id x:N is the Nth .cm of its model kind (c 14, n 19, s 23), and every record's source and"
      " replacements name ONE model number (normal and high variant)", pairs_ok == 22, "(%d / 22)" % pairs_ok)
print("FAILS", fails)
sys.exit(1 if fails else 0)
