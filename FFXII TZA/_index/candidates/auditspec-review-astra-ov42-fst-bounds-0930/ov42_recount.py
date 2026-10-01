"""SWE2-AUDIT-SPEC independent recount of the OV-42 FST discriminator (not ASTRA's reducer).
Reads the INSTALL FileSizeTable_*.fst (not the packet's frozen copies), checks each equals the frozen copy,
and models the path re-derived from the EXE:
  0032FCA0: selector k -> (kind, base) with group0 -> (5, 3k), groups1-3 -> (8, 4k)   [0032FD35 / 0032FD44]
  0032FD99: size = 0032E400(kind, base+1) -> override only if index < 0x400, else 002DF960 flat word
            [02EC3EE0 + 4*(kind*5000 + index)], filled by fread(820000) at 002E0444; -1 / <=0 not rounded
  0032FED2: jl on that size -> header byte clear at 0032FF2D; else requester with the FULL base+1
  003DD610..003DD61D: owner WORD = low16(base) + 1 (inc ax), 003DDAA8 movsx -> 0032E620 rejects < 0
Counts per language: negative narrowed WORDs, first negative selector, and the size class of the FULL
index lookup: absent (0xFFFFFFFF), other negative, zero, positive. Also the first selector whose positive
alias is common to all 12 languages. Control: a deliberately wrong model (narrowed index into the lookup)
must give different counts, and word 0 must be 57 in every table."""
import struct, hashlib, os, glob
INST = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\FileSizeTables"
FROZ = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_experiments\evidence\ov42-selector-fst-bound\fst-inputs-01"
def s16(x):
    x &= 0xFFFF
    return x - 0x10000 if x & 0x8000 else x
def s32(x): return x - (1 << 32) if x & 0x80000000 else x
tables = {}
for p in sorted(glob.glob(os.path.join(INST, "FileSizeTable_*.fst"))):
    b = open(p, "rb").read(); n = os.path.basename(p)
    f = open(os.path.join(FROZ, n), "rb").read() if os.path.exists(os.path.join(FROZ, n)) else None
    print("%-24s %d bytes sha256 %s... frozen-equal=%s word0=%d" % (n, len(b), hashlib.sha256(b).hexdigest()[:16], f == b, struct.unpack_from("<I", b, 0)[0]))
    tables[n] = struct.unpack("<%dI" % (len(b) // 4), b)
print("languages:", len(tables))
common = {}
for model in ("full", "WRONG-narrowed"):
    print("== model:", model)
    for name, w in tables.items():
        row = []
        for group, kind, stride in ((0, 5, 3), (1, 8, 4)):
            neg = 0; first = None; cls = dict(absent=0, negother=0, zero=0, positive=0, oob=0); firstpos = None
            for k in range(0x8000):
                base = stride * k
                word = s16((base & 0xFFFF) + 1)          # inc ax on the low WORD
                if word >= 0: continue
                neg += 1
                if first is None: first = k
                idx = base + 1 if model == "full" else word
                flat = kind * 5000 + idx
                if not (0 <= flat < len(w)): cls["oob"] += 1; continue
                v = w[flat]
                if v == 0xFFFFFFFF: cls["absent"] += 1
                elif s32(v) < 0: cls["negother"] += 1
                elif v == 0: cls["zero"] += 1
                else:
                    cls["positive"] += 1
                    if model == "full":
                        common.setdefault((group, k), set()).add(name)
                        if firstpos is None: firstpos = (k, base + 1, word, flat, flat // 5000, flat % 5000, v)
            row.append("g%d ns%d neg=%d first=%s %s firstpos=%s" % (group, kind, neg, first,
                       " ".join("%s=%d" % kv for kv in cls.items()), firstpos))
        print("  %-24s %s | %s" % (name, row[0], row[1]))
for group in (0, 1):
    ks = sorted(k for (g, k), s in common.items() if g == group and len(s) == len(tables))
    print("first selector with a positive alias in all %d languages, group%d: %s (total %d)" % (len(tables), group, ks[0] if ks else None, len(ks)))
