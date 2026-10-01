"""Authored presentation commands, counted where they are authored: the @FMC blocks of the .ca animation containers.

Read-only over an extracted copy of the game (set FF12_EXTRACT; default D:/FFXII_TZA_extract), every *.ca under ps2data.
Format, as the engine reads it (FABLE, 2026-09-19):
  .ca file   = '@FRP' container; version 0: u32 count at +0x0C, child offsets (from +0x30) at +0x30;
               version 1: u32 total at +0x0C, per-group at +0x30, groups at +0x34, child offsets (from +0x40) at +0x40,
               0 = absent                                                          (child selector 004090D0)
  child      = '@FMC' block: name at +0x10, track count at +0x0C, first track header at +0x30
  track      = u8 kind, u8, u8, u8 groupCount, u16 distance to the next header; groups from +6
               (track initialiser 0041CD30)
  group      = u16 time key, u16 (length << 6 | commandCount); commands from +4; 0xFFFF key = the preamble marker
  command    = u16 (length << 7 | id), id clamped to 0x4B by the drain               (drain 0041DA90, 0041DB1D..0041DB7F)
Predictions that could fail:
  P1  every track's groups end exactly at the header's distance
  P2  every group's commands end exactly at the group's length
  P3  no command id above 0x4B is authored
Control: number of .ca files that are '@FRP' (survey of 2026-09-19: 3,164).
"""
import os, struct, collections, sys

ROOT = os.environ.get("FF12_EXTRACT", "D:/FFXII_TZA_extract")
u16 = lambda b, o: struct.unpack_from("<H", b, o)[0]
u32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
files = frp = blocks = tracks = groups = cmds = 0
bad = collections.Counter(); ids = collections.Counter(); blocks_with = collections.defaultdict(set); files_with = collections.defaultdict(set)
sub4 = collections.Counter(); other = collections.Counter(); sub11 = collections.Counter(); sub1d = collections.Counter(); names_with = collections.defaultdict(collections.Counter); kinds = collections.Counter(); folder_of = collections.defaultdict(collections.Counter)
def parse_block(d, b, p, i, folder):
    global blocks, tracks, groups, cmds
    blocks += 1
    name = d[b + 0x10: b + 0x30].split(b"\0")[0].decode("latin1")
    nt = u32(d, b + 0xC)
    h = b + 0x30
    for t in range(nt):
        tracks += 1
        kinds[d[h]] += 1
        ng, dist = d[h + 3], u16(d, h + 4)
        g = h + 6
        for _ in range(ng):
            groups += 1
            key, w = u16(d, g), u16(d, g + 2)
            glen, nc = w >> 6, w & 0x3F
            c = g + 4
            for _ in range(nc):
                w0 = u16(d, c)
                cid, clen = w0 & 0x7F, w0 >> 7
                cmds += 1
                ids[cid] += 1
                blocks_with[cid].add((p, i)); files_with[cid].add(p); names_with[cid][name] += 1; folder_of[cid][folder] += 1
                if cid == 4:
                    sub4[d[c + 2]] += 1
                if cid == 0x11:
                    sub11[d[c + 2]] += 1
                if cid == 0x1D:
                    sub1d[(d[c + 2], d[c + 3])] += 1
                if clen == 0:
                    bad["zero-length command"] += 1; break
                c += clen
            if c != g + glen:
                bad["P2 group end mismatch"] += 1
            g += glen if glen else 4
        if g != h + dist and t != nt - 1:
            bad["P1 track end mismatch"] += 1
        if not dist:
            break
        h += dist


for dp, dn, fn in os.walk(os.path.join(ROOT, "ps2data")):
    for f in fn:
        if not f.endswith(".ca"):
            continue
        files += 1
        p = os.path.join(dp, f)
        d = open(p, "rb").read()
        if d[:4] != b"@FRP":
            continue
        frp += 1
        ver = u32(d, 4)
        if ver == 0:
            n = u32(d, 0xC); base = 0x30
        elif ver == 1:
            n = u32(d, 0xC); base = 0x40
        else:
            bad["container version %d" % ver] += 1; continue
        folder = os.path.relpath(p, ROOT).replace(os.sep, "/").split("/")[3] if len(os.path.relpath(p, ROOT).split(os.sep)) > 3 else "?"
        for i in range(n):
            o = u32(d, base + 4 * i)
            if ver == 1 and not o:
                continue
            b = base + o
            if d[b:b + 4] != b"@FMC":
                other[d[b:b + 4].decode("latin1")] += 1; continue
            parse_block(d, b, p, i, folder)
ca_blocks, ca_cmds = blocks, cmds
ca_ids = collections.Counter(ids)
# second pass: command blocks outside the containers - event motion files (.mot) and the few model files that carry one
other_files = collections.Counter()
for dp, dn, fn in os.walk(os.path.join(ROOT, "ps2data")):
    q = dp.replace(os.sep, "/") + "/"
    if "/event/" in q and "/us/" not in q:
        continue                                   # one language copy of the event tree
    for f in fn:
        e = os.path.splitext(f)[1].lower()
        if e not in (".mot", ".cm"):
            continue
        p = os.path.join(dp, f)
        d = open(p, "rb").read()
        k = d.find(b"@FMC")
        while k >= 0:
            if k + 0x36 <= len(d) and u32(d, k + 4) == 1 and 0 < u32(d, k + 0xC) <= 64 and u32(d, k + 8) <= len(d) - k:
                other_files[e] += 1
                try:
                    parse_block(d, k, p, k, "event" if e == ".mot" else "model-file")
                except (IndexError, struct.error):
                    bad["second pass: block ran off the end of its file"] += 1
            else:
                bad["second pass: '@FMC' bytes that are not a block header"] += 1
            k = d.find(b"@FMC", k + 4)
print("second pass: '@FMC' blocks found by tag outside the containers (extension -> blocks):", dict(other_files))
print("  commands added by the second pass:", cmds - ca_cmds, "; ids that appear ONLY there:", " ".join("0x%02X" % i for i in sorted(ids) if i not in ca_ids) or "none")
print("control: .ca files", files, "; '@FRP' containers", frp, "(survey 3,164)")
print("@FMC blocks", blocks, "; tracks", tracks, "; groups", groups, "; commands", cmds)
print("track kind byte (value -> tracks):", sorted(kinds.items()))
print("P1 / P2 / other structural failures:", dict(bad) if bad else "none")
print("P3  largest command id authored: 0x%X" % max(ids))
print("command id -> commands / blocks / files ; top folders ; five commonest block names")
for cid in sorted(ids):
    print("  0x%02X  %7d / %6d / %5d ; %s ; %s" % (cid, ids[cid], len(blocks_with[cid]), len(files_with[cid]),
          ", ".join("%s %d" % kv for kv in folder_of[cid].most_common(3)), ", ".join(k for k, _ in names_with[cid].most_common(5))))
print("children of other kinds, not command blocks (tag -> children):", sorted(other.items()))
print("class 0x04 subtype byte +2 (value -> commands):", sorted(sub4.items()))
print("class 0x11 (bone trails) byte +2 (value -> commands):", sorted(sub11.items()))
print("class 0x1D (pose sequencer) (byte +2, byte +3) -> commands:", sorted(sub1d.items(), key=lambda kv: -kv[1])[:16])
print("ids 0x00-0x4B never authored:", " ".join("0x%02X" % i for i in range(0x4C) if i not in ids))
