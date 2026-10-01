"""sd160_indep_census.py - SWE2-AUDIT-SPEC independent recount for SD-160 (review of OPUS af6684173, 2026-09-30).

Input: the full game extract D:/FFXII_TZA_extract (every *.ebp, all nine plan_master language trees and anything else),
NOT the VBF the package reads, and NOT gen_req_channel_census.py / script_verb_census.py. Own parse:
  * container: section at +0x80 with u32 magic 0x8000000B, section size at +0x84; directory offset = sec u32 +0x18,
    count = u32 at the directory, 0x30-byte entries: +0x00 name offset into the pool (sec u32 +0x4C), +0x08 code start.
  * bytecode (BW pages): opcode byte; op >= 0x48 carries a u16 immediate (3 bytes), else 1 byte; op > 0x63 stops the
    segment. Each script's segment runs from its code start to the next code start / the directory / the section end.
  * a call site = op 0x58/0x59/0x5D/0x5E with immediate 0x265 (setfreetargettype) or 0x3005 (btlAtelSetUnitType).
  * the argument: the instruction immediately before the call. PUSHII (0x4F) / PUSHI (0x4E) give imm; PUSHI0..3
    (0x3E..0x41) are NOT treated as constants here (they push a variable slot) - any such or other predecessor is
    reported as "not-a-direct-constant".
Type 3 := (setfreetargettype, 3) or (btlAtelSetUnitType, 2) (F2/F3, re-read in the review from the image).
Controls: the total call count must reproduce the package's 63,432 (sensitive to missed files / misaligned decode);
a raw byte search for the 3-byte call encodings bounds the aligned count from above (sensitive to decode drift).
"""
import os, struct, collections, sys

ROOT = "D:/FFXII_TZA_extract"
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
WANT = {0x265: "setfreetargettype", 0x3005: "btlAtelSetUnitType"}
CALLS = (0x58, 0x59, 0x5D, 0x5E)
LANGS = ("ch", "cn", "de", "es", "fr", "in", "it", "kr", "us")

files = []
for dp, dn, fn in os.walk(ROOT):
    for f in fn:
        if f.lower().endswith(".ebp"):
            files.append(os.path.join(dp, f))
files.sort()

rows = []            # (rel, script, pc, verb, op, arg)
raw_hits = 0
skipped = collections.Counter()
opc = collections.Counter()
for p in files:
    b = open(p, "rb").read()
    rel = os.path.relpath(p, ROOT).replace("\\", "/")
    for imm in WANT:
        for op in CALLS:
            pat = bytes((op, imm & 0xFF, imm >> 8))
            i = b.find(pat)
            while i >= 0:
                raw_hits += 1
                i = b.find(pat, i + 1)
    if len(b) < 0x88 or U32(b, 0x80) != 0x8000000B:
        skipped["no-section"] += 1
        continue
    sec = b[0x80:0x80 + U32(b, 0x84)]
    d = U32(sec, 0x18)
    n = U32(sec, d)
    if n > 0x400 or d + 4 + n * 0x30 > len(sec):
        skipped["bad-directory"] += 1
        continue
    pool = U32(sec, 0x4C)
    starts = {}
    for s in range(n):
        e = d + 4 + s * 0x30
        no, cs = U32(sec, e), U32(sec, e + 8)
        o = pool + no
        nm = sec[o:sec.find(b"\0", o)].decode("cp932", "replace")
        starts.setdefault(cs, nm)
    edges = sorted(set(starts) | {d, len(sec)})
    for cs in sorted(starts):
        end = min([x for x in edges if x > cs] or [len(sec)])
        if cs >= len(sec):
            continue
        pc, prev = cs, None
        while pc < end:
            op = sec[pc]
            if op > 0x63:
                break
            if op >= 0x48:
                if pc + 3 > end:
                    break
                im = sec[pc + 1] | (sec[pc + 2] << 8)
                if op in CALLS and im in WANT:
                    opc[op] += 1
                    if prev and prev[0] in (0x4E, 0x4F):
                        arg = str(prev[1])
                    else:
                        arg = "not-a-direct-constant(%s)" % (hex(prev[0]) if prev else None)
                    rows.append((rel, starts[cs], cs, pc, WANT[im], op, arg))
                prev = (op, im)
                pc += 3
            else:
                prev = (op, None)
                pc += 1

print("ebp files: %d; skipped %s" % (len(files), dict(skipped)))
print("raw 3-byte call-pattern hits (upper bound, unaligned): %d" % raw_hits)
print("decoded call sites of the two verbs: %d" % len(rows))
print("call opcodes: %s" % {hex(k): v for k, v in sorted(opc.items())})
by = collections.Counter((r[4], r[6]) for r in rows)
for k, v in sorted(by.items()):
    print("  %6d  %s" % (v, k))
nc = [r for r in rows if r[6].startswith("not")]
print("not a direct constant: %d" % len(nc))
for r in nc[:10]:
    print("   ", r)

T3 = {("setfreetargettype", "3"), ("btlAtelSetUnitType", "2")}
t3 = [r for r in rows if (r[4], r[6]) in T3]
print("type-3 sites: %d in %d files" % (len(t3), len(set(r[0] for r in t3))))
outside = [r for r in t3 if r[0].split("/")[1] != "plan_master"]
print("type-3 sites outside plan_master: %d" % len(outside))
per_lang = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
for r in t3:
    parts = r[0].split("/")
    lang = parts[2]
    zone = parts[-1]
    per_lang[lang][zone][(r[4], r[1])] += 1
print("languages with type-3 sites: %s" % sorted(per_lang))
for lg in sorted(per_lang):
    print("  %s: sites %d, zone files %d" % (lg, sum(sum(c.values()) for c in per_lang[lg].values()), len(per_lang[lg])))
ref = per_lang.get("us", {})
same = all({z: dict(c) for z, c in per_lang[lg].items()} == {z: dict(c) for z, c in ref.items()} for lg in per_lang)
print("all languages identical to us (zone, verb, script, count): %s" % same)
print("-- us type-3 list (zone, verb, script, sites):")
for z in sorted(ref):
    for (vb, s), c in sorted(ref[z].items()):
        print("  %s\t%s\t%s\t%d" % (z, vb, s, c))
distinct_pairs = set((z, s) for z in ref for (vb, s) in ref[z])
print("us distinct (zone, script) pairs: %d; sites %d" % (len(distinct_pairs), sum(sum(c.values()) for c in ref.values())))
fam = collections.Counter()
for z in ref:
    for (vb, s), c in ref[z].items():
        k = "THIRD" if s.startswith("THIRD_") else s.rstrip("0123456789_ABC")
        fam[(vb, k)] += c
print("us families: %s" % dict(sorted(fam.items())))
print("us zone families: %s" % dict(sorted(collections.Counter(z[:3] for z in ref).items())))
