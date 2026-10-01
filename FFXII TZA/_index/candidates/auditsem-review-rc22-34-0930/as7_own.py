"""SWE2-AUDIT-SEM own .as7 decoder, written from my reading of 0024AA00 (walker) and 00248500 (codec) in this review,
not from the producer's as7_decode.py. Walker: count = be16 [+2]; tail = file + be32 [+4]; page i at file + be32
[+8 + 4i]. Codec: mode = tail[0], k = tail[1]; mode 0 -> outLen = be16 tail[2..3], dict = tail + 4; mode 3 -> outLen
= be16 of the page's first two bytes (page advances 2), dict = tail + 2; modes 1/2 -> fail (0024869A). mask =
0xFFFF >> (k + 1); tokens until produced == outLen (produced > outLen -> fail, 0024866A):
  c & 0x80 : literal, n = (c & 0x7F) + 1 bytes from the page
  else     : c2 = next; len = (((2c) & 0xFFFF) >> (8 - k)) + 3; off = ((c << 8) | c2) & mask; copy len bytes from
             dict[off], dict[off + 1], ... (16-bit offset increment, not re-masked)
Checks per page: exact outLen, tokens consume exactly the page span [off_i, off_{i+1}) (last page: up to tail),
copies stay inside the tail block. Controls: k-1 and k+1 decodes (should mostly fail); a flipped literal/copy bit
(treat bit 7 inverted) must fail.
"""
import glob, struct, collections

def pages(b):
    n = struct.unpack_from(">H", b, 2)[0]
    tail = struct.unpack_from(">I", b, 4)[0]
    offs = [struct.unpack_from(">I", b, 8 + 4 * i)[0] for i in range(n)]
    return n, tail, offs

def decode(b, p, end, tail, kd=0, flip=False):
    mode, k = b[tail], b[tail + 1] + kd
    if mode in (1, 2) or mode > 3:
        return None, "mode"
    if mode == 0:
        outlen = struct.unpack_from(">H", b, tail + 2)[0]
        dic = tail + 4
    else:
        outlen = struct.unpack_from(">H", b, p)[0]
        p += 2
        dic = tail + 2
    mask = 0xFFFF >> (k + 1)
    out = bytearray()
    maxsrc = 0
    while len(out) < outlen:
        if p + 1 >= len(b):
            return None, "overrun"
        c = b[p]
        lit = bool(c & 0x80) != flip
        if lit:
            n = (c & 0x7F) + 1
            out += b[p + 1:p + 1 + n]
            p += 1 + n
        else:
            c2 = b[p + 1]
            ln = ((((c * 2) & 0xFFFF) >> (8 - k)) if 0 <= 8 - k < 16 else 0) + 3
            off = ((c << 8) | c2) & mask
            for j in range(ln):
                src = dic + ((off + j) & 0xFFFF)
                maxsrc = max(maxsrc, src)
                out.append(b[src] if src < len(b) else 0)
            p += 2
        if len(out) > outlen:
            return None, "overproduce"
    return (bytes(out), p, maxsrc, mode, k), None

tot = ok = exact_span = incopy = 0
ctrl = collections.Counter()
rows = []
for f in sorted(glob.glob("D:/FFXII_TZA_extract/ps2data/image/ff12/myoshiok/*/bin_menu/*.as7")):
    b = open(f, "rb").read()
    n, tail, offs = pages(b)
    good = span = cp = 0
    outs = set()
    distinct = set()
    for i in range(n):
        end = offs[i + 1] if i + 1 < n else tail
        r, why = decode(b, offs[i], end, tail)
        tot += 1
        if r:
            data, p, maxsrc, mode, k = r
            good += 1
            span += (p == end)
            cp += (maxsrc < len(b))
            outs.add(len(data))
            distinct |= set(data)
        for kd in (-1, 1):
            r2, _ = decode(b, offs[i], end, tail, kd=kd)
            if r2 and r2[1] == end:
                ctrl["k%+d exact" % kd] += 1
        r3, _ = decode(b, offs[i], end, tail, flip=True)
        if r3 and r3[1] == end:
            ctrl["flip exact"] += 1
    ok += good
    exact_span += span
    incopy += cp
    rows.append("%-60s pages %4d decoded %4d exact-span %4d mode %d k %d tail %5d outlen %s distinct-bytes %d" % (
        f[-60:], n, good, span, b[tail], b[tail + 1], len(b) - tail, sorted(outs), len(distinct)))
for r in rows:
    print(r)
print("TOTAL pages %d, decoded to exact outLen %d, consuming exactly their span %d, copies inside the file %d" % (
    tot, ok, exact_span, incopy))
print("controls (pages still decoding exactly to their span):", dict(ctrl))
