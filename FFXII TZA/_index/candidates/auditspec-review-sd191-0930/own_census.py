# own_census.py - independent .ebp CALL census (SWE2-AUDIT-SPEC), no FABLE decoder.
# Parses the extracted tree directly: section @file+0x80 (magic 0x8000000B, size +0x84),
# directory @sec+u32(+0x18) (cnt, cnt*0x30 entries; +0x00 nameoff, +0x08 codestart),
# linear decode: op>0x63 -> anomaly; op>=0x48 -> 3-byte imm16; else 1-byte.
import glob, struct, collections

U32 = lambda b, o: struct.unpack_from('<I', b, o)[0]

files = glob.glob(r'D:/FFXII_TZA_extract/**/*.ebp', recursive=True)
print("ebp files:", len(files))

VERBS = {0x202: 'disposepartywithoutcontrol', 0x2A3: 'duplicatepartyinfo_spattack',
         0x232: 'capturepartyforsummon', 0x191: 'setpossummonspace',
         0x195: 'resumeposbattletarget', 0x205: 'changetosummonparty', 0x2A4: 'resumepartyinfo_spattack'}
CTRL = 0x3B1  # setposparty: SD-184 counted 7,092 - positive control

calls_total = hits_n = ctrl = anomalies = no_dir = 0
hits = []
for path in sorted(files):
    b = open(path, 'rb').read()
    if len(b) < 0x84 or U32(b, 0x80) != 0x8000000B:
        continue
    sec = b[0x80:0x80 + U32(b, 0x84)]
    diroff = U32(sec, 0x18); cnt = U32(sec, diroff)
    if cnt > 0x400 or diroff + 4 + cnt * 0x30 > len(sec):
        no_dir += 1
        continue
    starts = sorted({U32(sec, diroff + 4 + s * 0x30 + 8) for s in range(cnt)})
    bounds = sorted(set(starts) | {diroff, len(sec)})
    for start in starts:
        end = min((x for x in bounds if x > start), default=len(sec))
        code = sec[start:end]
        i = 0
        while i < len(code):
            op = code[i]
            if op > 0x63:
                anomalies += 1; break
            if op >= 0x48:
                if i + 2 >= len(code):
                    anomalies += 1; break
                imm = code[i + 1] | (code[i + 2] << 8)
                if op in (0x58, 0x59, 0x5D, 0x5E):
                    calls_total += 1
                    if imm in VERBS:
                        hits.append((path, start + i, op, imm))
                    if imm == CTRL:
                        ctrl += 1
                i += 3
            else:
                i += 1

print("files w/o parseable dir:", no_dir, "| decode anomalies:", anomalies)
print("total CALL-family instructions:", calls_total)
print("control setposparty (0x3B1) calls:", ctrl)
print("target-verb calls:", len(hits))
byverb = collections.Counter(h[3] for h in hits)
for v, n in sorted(byverb.items()):
    print("  0x%03X %-28s %d" % (v, VERBS[v], n))
print("files containing them:", len(set(h[0] for h in hits)))


def fold(p):
    parts = p.replace('\\', '/').split('/')
    i = parts.index('plan_master')
    return '/'.join(parts[:i] + parts[i + 2:]), parts[i + 1]


zones = collections.Counter(fold(h[0])[0] for h in hits)
print("distinct zone paths:", len(zones))
for z, n in sorted(zones.items()):
    print("  %-70s %d" % (z, n))

# per-language totals
langtot = collections.Counter(fold(h[0])[1] for h in hits)
print("per-language:", dict(langtot))

# also: raw upper bound - immediate bytes <id_lo><id_hi> following a CALL op byte anywhere in each
# file's section (no decode), to prove the decoded census is not missing code-start gaps.
rawmax = 0
for path in files:
    b = open(path, 'rb').read()
    if len(b) < 0x84 or U32(b, 0x80) != 0x8000000B:
        continue
    sec = b[0x80:0x80 + U32(b, 0x84)]
    for j in range(len(sec) - 2):
        if sec[j] in (0x58, 0x59, 0x5D, 0x5E):
            imm = sec[j + 1] | (sec[j + 2] << 8)
            if imm in VERBS:
                rawmax += 1
print("raw-pattern upper bound (undecoded):", rawmax)
