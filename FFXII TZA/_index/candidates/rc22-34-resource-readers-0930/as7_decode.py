"""RC-22/23/24: the .as7 page walker, the payload codec and the tail block (SWE2-DATA 2026-09-30), static + corpus.

Code (certified image):
  0024AA00(as7, out, first, n)  - the offsets[] walker. count = be16 [+2] (bytes +2,+3 combined high-first); first >= count
      fails; n = 0 or n > count means all, then n is clamped to count - first; tail = as7 + be32 [+4]; the output cursor
      global 02091090 is zeroed and the output base stored at 02090788; for each page i in [first, first+n):
      00248500(as7 + be32 offsets[i] (bytes +8+4i..+0xB+4i), tail); a 0 return fails the walk.
  00248500(payload, tail)       - the page codec. tail[0] = mode, tail[1] = k; mode <= 2: outLen = be16 tail[2..3],
      dictionary = tail + 4; mode 3: outLen = be16 payload[0..1] (payload += 2), dictionary = tail + 2; mode 1/2 return 0
      (only 0 and 3 decode). Tokens until outLen bytes are produced:
        byte c with bit 7 set : literal run, (c & 0x7F) + 1 bytes copied from the payload;
        byte c with bit 7 clear, next byte c2 : copy ((2c & 0xFFFF) >> (8 - k)) + 3 bytes from dictionary[off..],
            off = (c << 8 | c2) & (0xFFFF >> (k + 1)); the source is the static dictionary, never the output.
      producing more than outLen fails (the ja at 0024866A).
Callers of the walker: 00292390 (item_gra: sheet slot (id >> 6) + 2 via 00292050, page id & 63, n = 1) and 002CEFD0
(char_silhouette: two calls, pages [g*0x204, +0x102) and [g*0x204 + 0x102, +0x102)).
Corpus: every page of all shipped .as7 files is decoded with exactly these rules.
Checks: D1 every page decodes to exactly outLen with no overshoot; D2 every page's tokens consume exactly its
[offsets[i], offsets[i+1] or tailOff) span (the page boundaries are the codec's); D3 every dictionary reference stays
inside the tail block. Controls: X1 decoding with k-1 (a wrong window split) must fail on most pages; X2 treating the
payload as raw texels (no codec) cannot give outLen bytes per page (sizes differ).
"""
import os, re, struct, sys, glob, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pe import dis  # noqa

FAILS = 0


def check(name, ok, detail=""):
    global FAILS
    print(("PASS " if ok else "FAIL ") + name + (" - " + detail if detail else ""))
    if not ok:
        FAILS += 1


# --- code pins
w = {x.address: x for x in dis(0x0024AA00)}
c = {x.address: x for x in dis(0x00248500)}
pins = [
    (w, 0x0024AA0A, "r10d, byte ptr [rcx + 2]"), (w, 0x0024AA26, "eax, byte ptr [rdi + 3]"),
    (w, 0x0024AA62, "ebp, byte ptr [rdi + 4]"), (w, 0x0024AA97, "rbp, rdi"),
    (w, 0x0024AAC3, "ecx, byte ptr [rdi + rax*4 + 8]"), (w, 0x0024AAF4, "0x248500"),
    (c, 0x00248516, "edx, byte ptr [rdx]"), (c, 0x00248525, "r9d, byte ptr [rdi + 1]"),
    (c, 0x0024852E, "dl, 2"), (c, 0x00248559, "r15w, cl"), (c, 0x00248561, "dl, 3"),
    (c, 0x002485B6, "0x2485fd"), (c, 0x002485B8, "cl, 0x7f"), (c, 0x00248610, "r9w, cl"),
    (c, 0x00248614, "r9w, 3"), (c, 0x00248628, "r10w, r15w"), (c, 0x0024864C, "ecx, byte ptr [rcx + rdi]"),
    (c, 0x0024866A, "0x248696"),
]
bad = [(hex(a), t[a].op_str) for t, a, s in pins if t[a].op_str != s]
for t, a, s in pins:
    print("   %08X %s %s" % (a, t[a].mnemonic, t[a].op_str))
check("P1 the walker/codec instructions read as described (%d pins)" % len(pins), not bad, str(bad))


def decode(pay, tail, k_override=None):
    mode, k = tail[0], tail[1]
    if k_override is not None:
        k = k_override
    p = 0
    if mode <= 2:
        outlen = tail[2] << 8 | tail[3]
        dic = tail[4:]
    else:
        dic = tail[2:]
        outlen = pay[0] << 8 | pay[1]
        p = 2
    if mode not in (0, 3):
        return None, "mode %d refused" % mode, p, 0
    mask = 0xFFFF >> (k + 1)
    out = bytearray()
    maxref = 0
    while len(out) != outlen:
        if p >= len(pay):
            return None, "ran off the payload", p, maxref
        b = pay[p]
        if b & 0x80:
            n = (b & 0x7F) + 1
            out += pay[p + 1:p + 1 + n]
            p += 1 + n
        else:
            if p + 1 >= len(pay):
                return None, "ran off the payload", p, maxref
            n = (((2 * b) & 0xFFFF) >> (8 - k)) + 3
            off = ((b << 8) | pay[p + 1]) & mask
            maxref = max(maxref, off + n)
            out += dic[off:off + n]
            p += 2
        if len(out) > outlen:
            return None, "overshoot", p, maxref
    return bytes(out), "ok", p, maxref


EX = "D:/FFXII_TZA_extract/ps2data/image/ff12/myoshiok"
files = sorted(glob.glob(EX + "/*/bin_menu/*.as7"))
tot = collections.Counter()
per = []
for f in files:
    b = open(f, "rb").read()
    cnt = b[2] << 8 | b[3]
    tailoff = struct.unpack_from(">I", b, 4)[0]
    offs = [struct.unpack_from(">I", b, 8 + 4 * i)[0] for i in range(cnt)]
    tail = b[tailoff:]
    ok = exact = inside = wrongk = 0
    sizes = collections.Counter()
    vals = collections.Counter()
    for i in range(cnt):
        end = offs[i + 1] if i + 1 < cnt else tailoff
        pay = b[offs[i]:end]
        out, why, used, maxref = decode(pay, tail)
        if out is not None:
            ok += 1
            sizes[len(out)] += 1
            exact += used == len(pay)
            inside += maxref <= len(tail) - 4
            vals.update(out)
        o2, *_ = decode(pay, tail, k_override=tail[1] - 1)
        wrongk += o2 is not None
    name = os.path.normpath(f).split(os.sep)[-3] + "/" + os.path.basename(f)
    per.append((name, cnt, ok, exact, inside, wrongk, dict(sizes), tail[0], tail[1], len(tail),
                max(vals) if vals else None, len(vals)))
    tot["pages"] += cnt; tot["ok"] += ok; tot["exact"] += exact; tot["inside"] += inside; tot["wrongk"] += wrongk
for r in per:
    print("   %-28s pages %4d decoded %4d exact-span %4d dict-inside %4d wrong-k-ok %4d outLen %s tail mode %d k %d "
          "tail %d B, output byte max %s distinct %d" % r)
check("D1 every page of every shipped .as7 decodes to exactly outLen (no overshoot)", tot["ok"] == tot["pages"],
      "%d / %d pages, %d files" % (tot["ok"], tot["pages"], len(files)))
check("D2 every page's tokens consume exactly its offsets[] span", tot["exact"] == tot["pages"],
      "%d / %d" % (tot["exact"], tot["pages"]))
check("D3 every dictionary copy stays inside the tail block (after its 4-byte head)", tot["inside"] == tot["pages"],
      "%d / %d" % (tot["inside"], tot["pages"]))
check("X1 control: with k - 1 the same pages mostly fail (the window split is load-bearing)",
      tot["wrongk"] < tot["pages"] // 10, "%d of %d still decode" % (tot["wrongk"], tot["pages"]))
rawsz = collections.Counter()
for f in files:
    b = open(f, "rb").read()
    cnt = b[2] << 8 | b[3]
    tailoff = struct.unpack_from(">I", b, 4)[0]
    offs = [struct.unpack_from(">I", b, 8 + 4 * i)[0] for i in range(cnt)] + [tailoff]
    rawsz.update(offs[i + 1] - offs[i] for i in range(cnt))
check("X2 control: raw page spans are not a constant texel size (%d distinct span sizes)" % len(rawsz), len(rawsz) > 10)
print("FAILS %d" % FAILS)
