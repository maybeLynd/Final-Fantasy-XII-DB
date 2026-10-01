"""The speaker tables the SQEX Sd pan-to-gain function 007B8430 indexes by output-channel count.

For each output count n (0..8): the speaker-angle array and its length (16-byte records at 01CB50A0 + 16*n), the
output-channel index of each ring speaker (pointer at 01F41C70 + 8*n), the centre-speaker flag (byte 01CB5178 + n)
and the low-frequency-channel flag (byte 01CB5188 + n); then the three-speaker front arc (angles 01F41CC0, output
indices 01CB5168). Angles are radians in the image and printed in degrees, clockwise from dead ahead.
A pointer outside the file's initialised data is printed as `runtime`.
The speaker names beside the indices follow the standard Windows channel order (FL FR C LFE RL RR SL SR) and are an
inference; the image holds only the indices. They are not printed for the one-output row.

Control: the two-output row must read 90 and 270 degrees, the constants the function also loads directly for a
stereo source.
"""
import struct, math, sys

EXE = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
d = open(EXE, "rb").read()
pe = struct.unpack_from("<I", d, 0x3C)[0]
nsec = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
pref = struct.unpack_from("<Q", d, pe + 24 + 24)[0]
BASE = 0x120000  # the database's address convention
secs = []
o = pe + 24 + opt
for i in range(nsec):
    vs, va, rs, ro = struct.unpack_from("<IIII", d, o + 8)
    secs.append((va, ro, rs))
    o += 40


def off(va):
    rva = va - BASE
    for a, ro, rs in secs:
        if a <= rva < a + rs:
            return ro + rva - a
    return None


def ptr(va):
    v = struct.unpack_from("<Q", d, off(va))[0]
    return v - pref + BASE if v else 0


NAMES = {0: "FL", 1: "FR", 2: "C", 3: "LFE", 4: "RL", 5: "RR", 6: "SL", 7: "SR"}
print("outputs\tangle_table\tring_speakers\tangles_deg\toutput_index\tcentre_flag\tlfe_flag")
for n in range(9):
    a = ptr(0x01CB50A0 + 16 * n)
    cnt = struct.unpack_from("<i", d, off(0x01CB50A8 + 16 * n))[0]
    m = ptr(0x01F41C70 + 8 * n)
    cf = d[off(0x01CB5178 + n)]
    lf = d[off(0x01CB5188 + n)]
    ang = idx = "-"
    if a and off(a) is None:
        ang = "runtime"
    elif a:
        ang = " ".join("%.1f" % math.degrees(x) for x in struct.unpack_from("<%df" % cnt, d, off(a)))
    if m and off(m) is not None and cnt:
        idx = " ".join(("%d" % x) if n == 1 else "%d(%s)" % (x, NAMES.get(x, "?")) for x in struct.unpack_from("<%di" % cnt, d, off(m)))
    print("%d\t%s\t%d\t%s\t%s\t%d\t%d" % (n, ("%08X" % a) if a else "-", cnt, ang, idx, cf, lf))
arc = struct.unpack_from("<3f", d, off(0x01F41CC0))
ai = struct.unpack_from("<3i", d, off(0x01CB5168))
print("# front arc (used when the centre flag is set and the centre weight is above 0): angles_deg %s  output_index %s"
      % (" ".join("%.1f" % math.degrees(x) for x in arc), " ".join("%d(%s)" % (x, NAMES.get(x, "?")) for x in ai)))
