"""Authored commands 0x20 and 0x21 - the two alias-bone slot moves - tallied as their handlers read them.

Read-only over an extracted copy of the game (set FF12_EXTRACT; default D:/FFXII_TZA_extract), every *.ca under
ps2data/obj_finish. Block and command format as in ../authored-command-census/census.py.

What the code does (FABLE, Claude Opus 5, 2026-09-20):
  005207A0 (0x20, 23 B) writes record word +0x2F4; 00520780 (0x21, 23 B) writes word +0x2F6.
  The special-bone resolver 00421E20 substitutes +0x2F4 for bone id 0x107 (00421E7D..00421E8E) and +0x2F6 for
  0x108 (00421E90..00421E9A), and ids 0x300.. are FCP attachment slots. The record reset (0041FA0B) and every
  render-event selection (0042529D) store the defaults 0x303 and 0x305, and each command stores
  default + (its word != 0) - so a command moves one alias to the NEXT attachment slot until the next motion
  selection restores the default.

PREDICTION THAT COULD FAIL, and the reason this tally is worth running: because the handler stores
default + (word != 0), a command whose word is ZERO would be a no-op - it would write the default that is
already there. If the authored data contains any such command, "each command moves the alias on" is wrong and
the row has to say so. The tally below reports the zero/non-zero split rather than asserting it.

Second prediction: the two commands are expected to sit in DIFFERENT block families - 0x21 in the item/throw
family and 0x20 in id-named monster blocks - which is a claim about authored placement, not about code, so the
per-block-name breakdown is printed in full rather than summarised.

Control: the same walk counts every command id, so the 0x20/0x21 totals can be checked against the
authored-command census's own totals for the same tree.
"""
import os, struct, collections

ROOT = os.environ.get("FF12_EXTRACT", "D:/FFXII_TZA_extract")
u16 = lambda b, o: struct.unpack_from("<H", b, o)[0]
u32 = lambda b, o: struct.unpack_from("<I", b, o)[0]

words = {0x20: collections.Counter(), 0x21: collections.Counter()}
names = {0x20: collections.Counter(), 0x21: collections.Counter()}
zeros = {0x20: 0, 0x21: 0}
allcmd = collections.Counter()
bad = collections.Counter()
files = blocks = 0

for dp, dn, fn in os.walk(ROOT + "/ps2data/obj_finish"):
    for f in fn:
        if not f.endswith(".ca"):
            continue
        d = open(os.path.join(dp, f), "rb").read()
        if d[:4] != b"@FRP":
            continue
        files += 1
        ver = u32(d, 4)
        base = 0x30 if ver == 0 else 0x40
        for i in range(u32(d, 0xC)):
            o = u32(d, base + 4 * i)
            if ver == 1 and not o:
                continue
            b = base + o
            if d[b:b + 4] != b"@FMC":
                continue
            blocks += 1
            name = d[b + 0x10:b + 0x30].split(b"\0")[0].decode("latin1")
            h = b + 0x30
            for t in range(u32(d, b + 0xC)):
                ng, dist = d[h + 3], u16(d, h + 4)
                g = h + 6
                for _ in range(ng):
                    w = u16(d, g + 2)
                    glen, nc = w >> 6, w & 0x3F
                    c = g + 4
                    for _ in range(nc):
                        w0 = u16(d, c)
                        cid, clen = w0 & 0x7F, w0 >> 7
                        allcmd[cid] += 1
                        if cid in (0x20, 0x21):
                            v = u16(d, c + 2)
                            words[cid][v] += 1
                            names[cid][name] += 1
                            if v == 0:
                                zeros[cid] += 1
                        if clen == 0:
                            bad["zero-length command"] += 1
                            break
                        c += clen
                    if c != g + glen:
                        bad["group end mismatch"] += 1
                    g += glen if glen else 4
                h += dist

print("tree: %s/ps2data/obj_finish   files %d   blocks %d" % (ROOT, files, blocks))
for cid, default in ((0x20, 0x303), (0x21, 0x305)):
    tot = sum(words[cid].values())
    print()
    print("command 0x%02X  ->  record word +0x%X, alias for bone id 0x%X, default 0x%X"
          % (cid, 0x2F4 if cid == 0x20 else 0x2F6, 0x107 if cid == 0x20 else 0x108, default))
    print("   authored: %d   with word == 0 (would be a no-op): %d" % (tot, zeros[cid]))
    print("   distinct word values: %s" % (", ".join("0x%X x%d" % (v, n) for v, n in words[cid].most_common(8))))
    print("   block names (%d distinct):" % len(names[cid]))
    for n, k in names[cid].most_common(12):
        print("      %-28s %d" % (n, k))
    if len(names[cid]) > 12:
        print("      ... %d more" % (len(names[cid]) - 12))
print()
print("CONTROL against figures the page already publishes:")
for cid,pub in ((0x24,1493),(0x25,740),(0x15,1218),(0x2F,30)):
    print("   0x%02X: this walk %6d   page says %s" % (cid, allcmd[cid], pub))
print("   total %d over %d ids" % (sum(allcmd.values()), len(allcmd)))
print("   walk integrity: %s" % (dict(bad) or "clean"))
