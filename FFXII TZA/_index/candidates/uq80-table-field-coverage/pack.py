# pack.py - shared: read the us battle_pack.bin, parse st2e sections by directory offset, verify headers.
import struct
PACK = "D:/FFXII_TZA_extract/ps2data/image/ff12/test_battle/us/binaryfile/battle_pack.bin"
pk = open(PACK, "rb").read()
u32 = lambda o: struct.unpack_from("<I", pk, o)[0]

# table: (name, slot, dir offset)
TABLES = [
    ("chr_data", "02EBF130", 0x44), ("dougu_data", "02EBF100", 0x4C), ("eventitem_data", "02EBF098", 0x84),
    ("maho_data", "02EBF0F0", 0x78), ("waza_data", "02EBF0E8", 0x7C), ("gambit_data", "02EBF0E0", 0x24),
    ("m_daiji", "02EBF090", 0x88), ("g_daiji", "02EBF088", 0x8C), ("q_daiji", "02EBF080", 0x90),
    ("eis_data", "02EBF070", 0x98), ("questreward_data", "02EBF068", 0x9C), ("price_data", "02EBF060", 0x74),
    ("menkyo_data", "02EBF0C8", 0x6C), ("horidashi", "02EBF058", 0xE8), ("comac_data", "02EBF128", 0x48),
    ("mgccategory_data", "02EBF110", 0x30), ("license_data", "02EBF038", 0x34), ("attribute_data", "02EBF050", 0xA8),
    ("sobicategory_data", "02EBF0B0", 0x18), ("ability_data", "02EBF040", 0xEC),
    ("eitm_data", "02EBF0F8", 0x38), ("status_data", "02EBF118", 0x40), ("action_data", "02EBF138", 0x3C),
]

def section(doff):
    t = u32(doff)
    nxt = None
    return t

def header(doff):
    t = u32(doff)
    return dict(start=t, magic=pk[t:t+4], count=u32(t+4), size=u32(t+8), hdr=u32(t+0xC), f10=u32(t+0x10), f14=u32(t+0x14), f18=u32(t+0x18), f1c=u32(t+0x1C))

def records(doff):
    h = header(doff)
    base = h["start"] + h["hdr"]
    return [pk[base + i*h["size"]: base + (i+1)*h["size"]] for i in range(h["count"])], h

if __name__ == "__main__":
    # directory: sorted section starts, to bound each section and check the record area fits
    ndir = u32(0) if u32(0) < 0x1000 else None
    starts = sorted(set(u32(4*k) for k in range(1, 0x100//4) if 0 < u32(4*k) < len(pk)))
    print("pack size", len(pk), "dword0", hex(u32(0)))
    for name, slot, doff in TABLES:
        h = header(doff)
        nxt = min([s for s in starts if s > h["start"]] + [len(pk)])
        end = h["start"] + h["hdr"] + h["count"] * h["size"]
        print("%-18s %s +%#04x start=%#07x magic=%s count=%d size=%d hdr=%#x f10..1c=%#x,%#x,%#x,%#x recend=%#x next=%#x fits=%s" % (
            name, slot, doff, h["start"], h["magic"], h["count"], h["size"], h["hdr"], h["f10"], h["f14"], h["f18"], h["f1c"], end, nxt, end <= nxt))
