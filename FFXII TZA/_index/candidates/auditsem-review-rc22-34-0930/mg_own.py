"""SWE2-AUDIT-SEM own parse of worldmap/meshdata.mg (both shipped copies): the header as two {offset, size} pairs
(read by 00274780 as buf + u32[buf + 8i]), each sub-mesh's {idxOff, idxCount, vtxOff, vtxCount, slotOff, slotCount}
and its 0x20-byte slots {char name[16], s32 indexStart, s32 indexCount, s16 colour[4]}."""
import struct
for L in ('in', 'ch'):
    b = open('D:/FFXII_TZA_extract/ps2data/image/ff12/myoshiok/%s/worldmap/meshdata.mg' % L, 'rb').read()
    h = struct.unpack_from('<4I', b, 0)
    print(L, len(b), [hex(x) for x in h], 'fills exactly:', h[0] + h[1] == h[2] and h[2] + h[3] == len(b))
    for so in (h[0], h[2]):
        sub = struct.unpack_from('<6i', b, so)
        print('   sub@%#x' % so, sub)
        io, ic, vo, vc, slo, slc = sub
        for s in range(slc):
            e = b[so + slo + 0x20 * s:so + slo + 0x20 * s + 0x20]
            print('     slot', e[:16].split(b'\0')[0], struct.unpack_from('<2i4h', e, 16))
