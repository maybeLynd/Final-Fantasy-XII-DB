"""SWE2-AUDIT-SPEC: independent member-table and record decode for PhyreText (continues fe_file.py).
Namespace = [32-byte head][nt type words][78 x 36-byte classes][members x 24 bytes][strings]; the string base is
fixed by three class-name offsets (fe_file.out). Members are taken cumulatively by each class's member count."""
import struct
SHIP = r"D:\FFXII_TZA_extract\gamedata\d3d11\artdata\shaders\phyretext.fx.phyre"
d = open(SHIP, "rb").read(); h = struct.unpack_from("<21I", d)
ns = d[h[1]:h[1] + h[2]]; nt, ncls, nmem = struct.unpack_from("<3I", ns, 8)
cs = 32 + 4 * nt; ms = cs + 36 * ncls; sb = ms + 24 * nmem
print("classes", ncls, "members", nmem, "member table", ms, "string base", sb, "(fe_file: 8628)")
def s(o):
    e = ns.find(b"\0", sb + o); return ns[sb + o:e].decode("latin1")
cls = [struct.unpack_from("<9I", ns, cs + 36 * i) for i in range(ncls)]
first = []; k = 0
for c in cls: first.append(k); k += c[3]
print("member counts sum", k, "== members:", k == nmem)
for cid in (38, 43, 44):
    c = cls[cid - 1]; print("class %d %s parent=%d packed_width=%d members=%d" % (cid, s(c[2]), c[0], c[1] & 0xfffffff, c[3]))
    for j in range(first[cid - 1], first[cid - 1] + c[3]):
        w = struct.unpack_from("<6I", ns, ms + 24 * j)
        tn = ("type%d" % w[1]) if w[1] <= nt else ("class%d:%s" % (w[1] - nt, s(cls[w[1] - nt - 1][2])))
        print("   member", s(w[0]), "words", [hex(x) for x in w], "type", tn)
# records of list 12 (class 43), 12 x 13 bytes from 29224; array region 29380..29544
start, arr = 29224, 29380
region = d[arr:arr + 164]
print("array region strings:", [(arr + i, x.decode()) for i, x in zip([0] + [j + 1 for j, b in enumerate(region) if b == 0][:-1], region.split(b"\0")) if x])
for i in range(12):
    rec = d[start + 13 * i:start + 13 * i + 13]; off, sz = struct.unpack_from("<HH", rec, 5)
    print("record %2d @%d %s  loc.offset=%d size_word=%d masked=%d" % (i, start + 13 * i, rec.hex(), off, sz, sz & 0x1fff))
print("record 8 name bytes at 29518:", d[29518:d.find(b'\0', 29518)])
