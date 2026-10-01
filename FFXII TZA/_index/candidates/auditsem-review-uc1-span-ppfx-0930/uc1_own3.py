"""SWE2-AUDIT-SEM UC1-SPAN check, part 3 (own code): do the sampled unreferenced PPFX bodies share their data with the
span? For each data target the part-1 sample reads (rip operands), count the rip references to it from code inside the
PPFX span [006DA880, 007911E0) and from outside it."""
import struct
import img
t0, t1, rp = img.text_range()
text = img.raw[rp:rp + (t1 - t0)]
va0 = img.BASE + t0
LO, HI = 0x006DA880, 0x007911E0
TG = [0x02EA0B70, 0x01CEBB70, 0x00E202A8, 0x00E20298, 0x00E20288, 0x00E20278, 0x00E20268, 0x00E20258]
res = {t: [0, 0] for t in TG}
for i in range(len(text) - 4):
    d = struct.unpack_from("<i", text, i)[0]
    for tail in (0, 1, 4):
        t = va0 + i + 4 + tail + d
        if t in res:
            for L in range(15, 4, -1):
                st = i + 4 + tail - L
                xs = list(img.md.disasm(text[st:st + L], va0 + st, 1))
                if xs and xs[0].size == L and "rip" in xs[0].op_str:
                    res[t][0 if LO <= xs[0].address < HI else 1] += 1
                    break
for t in TG:
    print("%08X  rip refs inside the PPFX span %d, outside %d" % (t, res[t][0], res[t][1]))
