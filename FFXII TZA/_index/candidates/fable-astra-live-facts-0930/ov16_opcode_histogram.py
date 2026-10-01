"""bf1_opcode_histogram.py - full opcode histogram over every distinct shipped .ebp (decode rules copied from
_index/candidates/bf5-inert-opcodes/bf5_inert_opcode_census.py: section at 0x80 tag 0x8000000B, directory at +0x18,
stride 0x30, start at +8; 1 byte below 0x48, 3 bytes at or above). Read-only; prints counts for all 100 opcodes."""
import collections, hashlib, struct, sys
from pathlib import Path
EX = Path(sys.argv[1] if len(sys.argv) > 1 else "D:/FFXII_TZA_extract")
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
seen = set(); files = scripts = anomalies = 0; ops = collections.Counter()
for p in sorted(EX.rglob("*.ebp")):
    b = p.read_bytes(); h = hashlib.md5(b).digest()
    if h in seen: continue
    seen.add(h)
    if len(b) < 0x88 or U32(b, 0x80) != 0x8000000B: continue
    files += 1
    sec = b[0x80:0x80 + U32(b, 0x84)]
    diroff = U32(sec, 0x18); cnt = U32(sec, diroff)
    if cnt > 0x400 or diroff + 4 + cnt * 0x30 > len(sec): continue
    starts = sorted(U32(sec, diroff + 4 + s * 0x30 + 8) for s in range(cnt))
    bounds = sorted(set(starts) | {diroff, len(sec)})
    for start in starts:
        end = min((x for x in bounds if x > start), default=len(sec))
        if start >= len(sec) or end <= start: continue
        scripts += 1; code = sec[start:end]; i = 0
        while i < len(code):
            op = code[i]
            if op > 0x63: anomalies += 1; break
            ops[op] += 1
            i += 3 if op >= 0x48 else 1
print("distinct .ebp %d, code sections %d, scripts %d, anomalies %d, instructions %d"
      % (len(seen), files, scripts, anomalies, sum(ops.values())))
for k in range(0x64): print("0x%02X\t%d" % (k, ops[k]))
