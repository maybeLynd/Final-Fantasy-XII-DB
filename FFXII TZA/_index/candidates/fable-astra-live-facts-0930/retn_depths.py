# retn_depths.py - OV-16 (B): the depth operand of every shipped RETN (0x2E) / RETTN (0x30). The handler pops a depth and
# recycles channels from depth+1 upward only when depth+1 <= the running channel (0026131C-0026133A). The instruction
# before the RETN is classified: PUSHII (0x4F, the operand itself, sign-extended 16-bit), PUSHI (0x4E, an int-pool index,
# resolved here from the script's int pool is NOT attempted - counted as 'pool'), or other (a computed value).
# Decode rules as bf1_opcode_histogram.py / bf5_inert_opcode_census.py: section at 0x80 tag 0x8000000B, directory at
# +0x18, stride 0x30, start at +8; 1 byte below 0x48, 3 bytes at or above.
# Control: the RETN / RETTN totals must equal the histogram's (135,429 / 6,039).
import collections, hashlib, struct, sys
from pathlib import Path
EX = Path(sys.argv[1] if len(sys.argv) > 1 else "D:/FFXII_TZA_extract")
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
seen = set()
tot = collections.Counter()
prev_kind = collections.Counter()
depth = {0x2E: collections.Counter(), 0x30: collections.Counter()}
for p in sorted(EX.rglob("*.ebp")):
    b = p.read_bytes(); h = hashlib.md5(b).digest()
    if h in seen: continue
    seen.add(h)
    if len(b) < 0x88 or U32(b, 0x80) != 0x8000000B: continue
    sec = b[0x80:0x80 + U32(b, 0x84)]
    diroff = U32(sec, 0x18); cnt = U32(sec, diroff)
    if cnt > 0x400 or diroff + 4 + cnt * 0x30 > len(sec): continue
    starts = sorted(U32(sec, diroff + 4 + s * 0x30 + 8) for s in range(cnt))
    bounds = sorted(set(starts) | {diroff, len(sec)})
    for start in starts:
        end = min((x for x in bounds if x > start), default=len(sec))
        if start >= len(sec) or end <= start: continue
        code = sec[start:end]; i = 0; prev = None
        while i < len(code):
            op = code[i]
            if op > 0x63: break
            if op in (0x2E, 0x30):
                tot[op] += 1
                if prev and prev[0] == 0x4F:
                    v = struct.unpack_from("<h", code, prev[1] + 1)[0] if prev[1] + 3 <= len(code) else None
                    depth[op][v] += 1; prev_kind[(op, "PUSHII")] += 1
                elif prev and prev[0] == 0x4E:
                    prev_kind[(op, "PUSHI(pool)")] += 1
                else:
                    prev_kind[(op, "other:%s" % (hex(prev[0]) if prev else "none"))] += 1
            prev = (op, i)
            i += 3 if op >= 0x48 else 1
print("RETN %d  RETTN %d  (control: histogram 135,429 / 6,039: %s)" % (tot[0x2E], tot[0x30],
      "PASS" if (tot[0x2E], tot[0x30]) == (135429, 6039) else "MISMATCH"))
print("preceding instruction:", dict(prev_kind.most_common(12)))
for op, name in ((0x2E, "RETN"), (0x30, "RETTN")):
    print("%s PUSHII depth values:" % name, dict(sorted(depth[op].items(), key=lambda kv: (kv[0] is None, kv[0]))))
