"""SWE2-AUDIT-SPEC independent file-side decode of the shipped PhyreText.fx.phyre (no EA-3/CU-3 code).
Uses only the header words, the 36-byte list headers and raw bytes; class names are found by string search
in the namespace and matched to class records by offset."""
import struct, hashlib, sys
SHIP = r"D:\FFXII_TZA_extract\gamedata\d3d11\artdata\shaders\phyretext.fx.phyre"
RET = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_experiments\evidence\phyretext-softedges-field-extent\softedges-resource-source-01\phyretext.fx.phyre"
d = open(SHIP, "rb").read(); r = open(RET, "rb").read()
print("shipped", len(d), hashlib.sha256(d).hexdigest()); print("retained == shipped:", d == r)
h = struct.unpack_from("<21I", d)
print("header", [hex(x) for x in h])
ns0, nsz = h[1], h[2]; ns = d[ns0:ns0 + nsz]
nt = struct.unpack_from("<I", ns, 8)[0]; ncls = struct.unpack_from("<I", ns, 12)[0]
print("nt", nt, "ns words 0..7", [struct.unpack_from("<I", ns, 4 * i)[0] for i in range(8)])
L0 = ns0 + nsz; lists = [struct.unpack_from("<9I", d, L0 + 36 * i) for i in range(18)]
for i, l in enumerate(lists): print("list", i, l)
data_start = L0 + 36 * 18
tail = data_start + sum(l[2] for l in lists)
print("data_start", data_start, "sum sizes == h14:", sum(l[2] for l in lists) == h[14])
fix = tail + h[13] + 12 * h[12] + 4 * h[15] + 16 * h[16]
print("fixup tables start", fix, "+ packed sizes", h[9], h[7], h[5], "=", fix + h[9] + h[7] + h[5], "file len", len(d))
p = data_start
for i, l in enumerate(lists):
    if l[1] == 12: print("12-count list", i, "class", l[0], "start", p, "obj", l[3], "arr", l[4], "arrays_start", p + l[3])
    p += l[2]
# class records: search names
def find_all(b):
    out = []; i = ns.find(b)
    while i >= 0: out.append(i); i = ns.find(b, i + 1)
    return out
for nm in (b"PShaderParameterDefinition\0", b"PShaderParameterCaptureBufferLocationSize\0", b"PShaderParameterCaptureBufferLocation\0", b"m_offset\0", b"m_size\0", b"m_name\0", b"m_bufferLoc\0"):
    print(nm[:-1].decode(), "ns offsets", find_all(nm))
cs = 32 + 4 * nt
for cid in (38, 43, 44):
    w = struct.unpack_from("<9I", ns, cs + 36 * (cid - 1)); print("class", cid, [hex(x) for x in w])
