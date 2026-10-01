"""Dump the 'eps ' chunk of the shipped sead.win.config: per class section header and each preset as f32 + hex.
Layout per page: chunk at file +0x250; u32 table at chunk + u16[chunk+2], indexed by classId;
section {u16@0, u16 dataOfs@2, u8 presetCnt@4, u8 flag@5}; preset k at sec + dataOfs + k*stride[classId]."""
import struct, sys
CFG = r"D:\FFXII_TZA_extract\ps2data\sound\sead.win.config"
d = open(CFG, "rb").read()
STRIDE = [0, 0x80, 0x20, 0x10, 0x10, 0x10, 0, 0x10, 0, 0x10, 0x20]
CH = 0x250
print("file size %#x; chunk head bytes: %s" % (len(d), d[CH:CH + 16].hex(" ")))
tbl = CH + struct.unpack_from("<H", d, CH + 2)[0]
# number of entries: the page says 11 class sections
out = {}
for cid in range(11):
    so = CH + struct.unpack_from("<I", d, tbl + cid * 4)[0]
    w0, dofs, cnt, flag = struct.unpack_from("<HHBB", d, so)
    print("class %2d sec@file %#x  u16@0=%#x dataOfs=%#x presetCnt=%d flag=%d stride=%#x  hdr=%s" % (
        cid, so, w0, dofs, cnt, flag, STRIDE[cid], d[so:so + 16].hex(" ")))
    for k in range(cnt):
        if not STRIDE[cid]:
            continue
        po = so + dofs + k * STRIDE[cid]
        n = STRIDE[cid] // 4
        fs = struct.unpack_from("<%df" % n, d, po)
        us = struct.unpack_from("<%dI" % n, d, po)
        print("   preset %d @file %#x" % (k, po))
        for i in range(n):
            print("      +%#04x  %-14.6g %08X" % (i * 4, fs[i], us[i]))
        out.setdefault(cid, []).append(fs)
