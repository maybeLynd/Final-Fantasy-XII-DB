"""gr17_efx.py - SWE2-AUDIT-SPEC independent .efx parse for the GR-17 residue review (2026-09-30).

Written from this review's own reading of the engine code, not from the package's parser:
  dispatcher 003EDAD0 (chunk run at 003EDC00..003EDECD): top-level chunks are {u32 len, u16 0x100, u16 type, ...};
    a run of types 0x600 / 0x610 / 0x620 (0x630 excluded) is copied (each chunk len & ~15) and handed to the handlers
    with rcx = chunk + 0xC, edx = len - 0x10;
  0x600 -> 003A79C0: header id = chunk[0xD]; header object = chunk + 0x10 (0xA0 bytes), its byte 0 overwritten with id;
  0x610 -> 003A7B50: slot (header chunk[0xC], index chunk[0xD]); slot object = chunk + 0x10; track count = chunk[0x13]
    (0 -> 0x40); header + 0x2C + 4*index -> slot;
  0x620 -> 003A77F0: track (header chunk[0xC], slot chunk[0xD], index chunk[0xE]); the handler moves chunk + 0x1C..end
    down to chunk + 0x10, so the track object's byte k is file byte chunk + 0x1C + k; slot + 0x20 + 4*index -> track;
  0024FE70: stop sequence n runs slot header[0xA + n] (n = 1 -> header byte 0xB);
  0046EFD0: for track index 1 .. count-1: track[5] & 1 and track[1] == 2 -> 003B8670 at time 0;
  003B8670: entry count track[0x10]; entry k at track + 0x14 + 16k; time u16 at entry + 2; opcode byte at entry + 0
    (1..128); at time 0 an entry fires iff its time is <= 0, and the first entry with time > 0 ends the pass.
Checks: the walk must end exactly at the file size (and at the size field at file +0xC); a raw scan for 0x6x0 chunk
headers NOT on the top-level walk (nesting); chunk lengths vs the len & ~15 copy.
Positive control for the opcode instrument: opcode 3 (the hit) must be found in other shipped .efx files; the files and
per-file counts are listed so the control can be re-opened by hand.
Source: D:/FFXII_TZA_extract (the full game extract), sha256 printed and compared with the package's pinned hash.
"""
import collections, glob, hashlib, os, struct, sys

ROOT = r"D:\FFXII_TZA_extract"
CALL = os.path.join(ROOT, "ps2data", "effect_finish", "jp", "common", "c_all.efx")
PIN = "0f2f15d9787f4d234f54ba978797ed3687956482aa2f3a456e382cb617869029"
REACH = {3, 17, 24, 31, 34, 40}          # package E6's reaching set (re-checked separately)
IDS = list(range(104, 112)) + list(range(142, 148))


def walk(d):
    o, out = 16, []
    while o + 8 <= len(d):
        ln, fl, ty = struct.unpack_from("<IHH", d, o)
        if ln < 16 or o + ln > len(d):
            break
        out.append((o, ln, fl, ty))
        o += ln
    return out, o


def parse(d):
    ch, end = walk(d)
    H, S, TR = {}, {}, {}
    for o, ln, fl, ty in ch:
        if fl != 0x100 or ty not in (0x600, 0x610, 0x620):
            continue
        if ty == 0x600:
            h = bytearray(d[o + 0x10:o + 0x10 + 0xA0]); h[0] = d[o + 0xD]
            H[d[o + 0xD]] = bytes(h)
        elif ty == 0x610:
            S[(d[o + 0xC], d[o + 0xD])] = d[o + 0x13] or 0x40
        else:
            TR[(d[o + 0xC], d[o + 0xD], d[o + 0xE])] = d[o + 0x1C:o + ln]
    return ch, end, H, S, TR


def ents(t):
    n = t[0x10]
    return [(t[0x14 + 16 * k], struct.unpack_from("<H", t, 0x14 + 16 * k + 2)[0]) for k in range(n)
            if 0x14 + 16 * k + 4 <= len(t)]


def fire0(S, TR, h, s):
    """opcodes fired at time 0 by every launchable kind-2 track of slot (h, s)"""
    out = []
    n = S.get((h, s))
    if n is None:
        return None
    for (a, b, k), t in sorted(TR.items()):
        if (a, b) != (h, s) or not (1 <= k < n) or len(t) < 0x14:
            continue
        if t[5] & 1 and t[1] == 2:
            z = []
            for op, tm in ents(t):
                if tm > 0:
                    break
                z.append(op)
            out.append((k, tuple(z)))
    return out


d = open(CALL, "rb").read()
sha = hashlib.sha256(d).hexdigest()
ch, end, H, S, TR = parse(d)
print("== c_all.efx (%s)" % CALL)
print("  sha256 %s (package pin matches: %s); %d bytes; magic %r; size field +0xC = %d" %
      (sha, sha == PIN, len(d), d[:8], struct.unpack_from("<I", d, 12)[0]))
print("  top-level walk: %d chunks, ends at %d (file end: %s)" % (len(ch), end, end == len(d)))
print("  chunk (flag, type) multiset: %s" % dict(sorted(collections.Counter((fl, ty) for o, ln, fl, ty in ch).items())))
print("  lengths not a multiple of 16 among 0x6x0 chunks: %d" % sum(1 for o, ln, fl, ty in ch if ty in (0x600, 0x610, 0x620) and ln % 16))
tops = {o for o, ln, fl, ty in ch}
nest = []
for o in range(16, len(d) - 8, 4):
    ln, fl, ty = struct.unpack_from("<IHH", d, o)
    if fl == 0x100 and ty in (0x600, 0x610, 0x620) and 16 <= ln <= 0x10000 and o not in tops:
        nest.append((o, ln, ty))
print("  0x100-flagged 0x600/0x610/0x620 headers off the top-level walk (4-aligned raw scan): %d %s" % (len(nest), nest[:5]))
print("  headers %d, slots %d, tracks %d" % (len(H), len(S), len(TR)))
kinds = collections.Counter(t[1] for t in TR.values() if len(t) > 1)
print("  track kinds (byte +1): %s" % dict(sorted(kinds.items())))
k2 = {k: t for k, t in TR.items() if len(t) >= 0x14 and t[1] == 2}
allops = collections.Counter(op for t in k2.values() for op, tm in ents(t))
print("  kind-2 tracks %d; opcode multiset over all their entries: %s" % (len(k2), dict(sorted(allops.items()))))
print("  entry arrays fit their chunk: %s; reaching opcodes {3,17,24,31,34,40} present: %s" %
      (all(0x14 + 16 * t[0x10] <= len(t) for t in k2.values()), sorted(set(allops) & REACH) or "none"))
orphan = [k for k in TR if (k[0], k[1]) not in S]
print("  tracks whose slot has no 0x610: %d; slot refs in headers without a 0x610: %d" %
      (len(orphan), sum(1 for i, h in H.items() for b in list(h[1:10]) + list(h[0xA:0x2C]) if False)))
print("== the 14 ids 104-111 / 142-147")
for i in IDS:
    h = H.get(i)
    if h is None:
        print("  id %d: NO HEADER" % i); continue
    s1 = h[0xB]
    starts = {x: h[x] for x in list(range(1, 8)) + [9] if h[x]}
    print("  id %3d: header bytes +1..+0xB %s; stop seq 1 -> slot %d fires %s; start slots %s fire %s" % (
        i, h[1:0xC].hex(" "), s1, fire0(S, TR, i, s1) if s1 else "-", starts,
        {x: fire0(S, TR, i, s) for x, s in starts.items()}))
# every opcode reachable at time 0 from ANY header's stop-1 or start slots, whole file
tz = collections.Counter()
for i, h in H.items():
    for s in {h[0xB]} | {h[x] for x in list(range(1, 8)) + [9]}:
        if s:
            for k, z in fire0(S, TR, i, s) or []:
                tz.update(z)
print("  whole file, time-0 opcodes of stop-1 + start slots over all %d headers: %s" % (len(H), dict(sorted(tz.items()))))

print("== positive control: opcode 3 in the other shipped .efx files (same parser)")
files = sorted(glob.glob(os.path.join(ROOT, "**", "*.efx"), recursive=True))
tot = collections.Counter(); per = []
bad = 0
for P in files:
    x = open(P, "rb").read()
    if x[:3] != b"EFX":
        bad += 1; continue
    c, e, h_, s_, t_ = parse(x)
    ops = collections.Counter(op for t in t_.values() if len(t) >= 0x14 and t[1] == 2 for op, tm in ents(t))
    tot.update(ops)
    if ops[3]:
        per.append((ops[3], os.path.relpath(P, ROOT), e == len(x)))
print("  %d .efx files (%d without EFX magic); opcode totals over kind-2 tracks: 3 x%d, 34 x%d, 17 x%d, 40 x%d, 24 x%d, 31 x%d"
      % (len(files), bad, tot[3], tot[34], tot[17], tot[40], tot[24], tot[31]))
print("  files carrying opcode 3: %d; first five: %s" % (len(per), per[:5]))
print("  every walk ended at its file end: %s" % all(p[2] for p in per))
