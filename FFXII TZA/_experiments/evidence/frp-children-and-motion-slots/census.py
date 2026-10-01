"""What the parts of an @FRP container are: the tag of every child of every .ca and .cm.

Read-only over an extracted copy of the game (set FF12_EXTRACT; default D:/FFXII_TZA_extract), every *.ca and *.cm
under ps2data.
Container, as the child selector 004090D0 reads it: '@FRP'; u32 version at +4; version 0 - u32 count at +0x0C, u32
child offsets (from +0x30) at +0x30; version 1 - u32 total at +0x0C, children per group at +0x30, groups at +0x34,
u32 child offsets (from +0x40) at +0x40, 0 = absent.
Predictions that could fail:
  P1  every child begins with a four-byte tag '@' + three capitals or digits
  P2  in a .ca, @FMN and @FMW come in equal numbers (one weight child per bone-motion child)
  P3  every file has exactly one @FRM
Control: 3,164 .ca and 1,066 .cm, all '@FRP' (the container page).
"""
import os, re, struct, collections

ROOT = os.environ.get("FF12_EXTRACT", "D:/FFXII_TZA_extract")
u32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
files = collections.Counter(); ver = collections.Counter(); tags = {".ca": collections.Counter(), ".cm": collections.Counter()}
badtag = 0; p2_bad = 0; frm = collections.Counter(); order = {".ca": collections.Counter(), ".cm": collections.Counter()}
absent = 0; named = collections.defaultdict(collections.Counter)
for dp, dn, fn in os.walk(os.path.join(ROOT, "ps2data")):
    for f in fn:
        e = os.path.splitext(f)[1].lower()
        if e not in (".ca", ".cm"):
            continue
        d = open(os.path.join(dp, f), "rb").read()
        if d[:4] != b"@FRP":
            continue
        files[e] += 1
        v = u32(d, 4); ver[(e, v)] += 1
        base = 0x30 if v == 0 else 0x40
        seq = []
        for i in range(u32(d, 0xC)):
            o = u32(d, base + 4 * i)
            if v == 1 and not o:
                absent += 1; continue
            t = d[base + o: base + o + 4]
            if not re.match(rb"@[A-Z0-9]{3}$", t):
                badtag += 1; continue
            t = t.decode()
            tags[e][t] += 1; seq.append(t)
            nm = d[base + o + 0x10: base + o + 0x30].split(b"\0")[0]
            if nm and len(named[t]) < 4000:
                named[t][nm.decode("latin1")] += 1
        c = collections.Counter(seq)
        frm[(e, c["@FRM"])] += 1
        if e == ".ca" and c["@FMN"] != c["@FMW"]:
            p2_bad += 1
        sig = []
        for t in seq:
            if not sig or sig[-1] != t:
                sig.append(t)
        order[e][" ".join(sig)] += 1
print("control: files", dict(files), "(container page: 3,164 .ca, 1,066 .cm); versions", sorted(ver.items()))
print("P1  children whose first four bytes are not a tag:", badtag, "; absent slots in version-1 tables:", absent)
for e in (".ca", ".cm"):
    print(e, "children by tag:", sorted(tags[e].items(), key=lambda kv: -kv[1]))
print("P2  .ca files where @FMN and @FMW counts differ:", p2_bad)
print("P3  @FRM per file (extension, count) -> files:", sorted(frm.items()))
for e in (".ca", ".cm"):
    print(e, "order of child kinds (runs collapsed), commonest:")
    for k, n in order[e].most_common(6):
        print("    %5d  %s" % (n, k))
for t in ("@FMN", "@FMW", "@FRM"):
    print(t, "commonest names at +0x10:", [k for k, _ in named[t].most_common(8)])
