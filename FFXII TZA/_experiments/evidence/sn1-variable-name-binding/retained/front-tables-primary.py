"""sn1_front_tables.py - SN-1 (OPUS, Claude Opus 5.5, 2026-09-28): the .dbg header's second words, and the front region
they index, in the four ATEL control-script companions (ctrl, btlctrl, evctrl, mapctrl; ps2data/image/ff12/in/bin).

The header's first three slots are (sectionOffset, tableOffset) - not (offset, size). The second words point into the
front region [+0x6C, first section), which is three counted tables, not one pair stream:
  F1 T1 = header +0x0C (0x6C in all four): {u32 n; u32 nameOffset[n]} - the source files (n = the .sbn block count, 2 / 3
     / 2 / 3), names relative to the string pool (header +0x08): `ctrl.src`, the systemctrl.ath path, `mapctrl_mj.src`.
     It ends exactly at T0.
  F2 T0 = header +0x04 (0x78 / 0x7C = 0x6C + 4 + 4n): {u32 count; u32 nameOffset[count]}, every entry a name start, then
     zero padding to 16 bytes. The names are the module's source-declared variables (every one in ctrl's .sbn text; a
     name recurs once per scope that declares it).
  F3 T2 = header +0x14: {u32 count; {u32 id; u32 namePos}[count]} - the global-variable directory the page describes, with
     its count explicit (815 / 4,950 / 943 / 4,953). Every namePos is a name start, the first id 0x30000000 names
     global_flag[0], and the table plus zero padding to 16 bytes ends exactly at the first section offset (header +0x2C).
  F4 the page's reading - one {id; nameHeapPos} stream from +0x6C (846 / 5,000 - elsewhere 4,999 - / 1,004 / 5,020 pairs) - folds T1, T0,
     their padding and T2's count word into 'pairs': the pair count it gives equals T2's count plus those words / 2, and
     the words it reads as ids before T2 are name offsets (control: every T0 word is a name start; no T2 id is).
Not claimed: what the .dbg's q3 listA / listB cut marks (the SN-1 residue).
Usage: python sn1_front_tables.py [dir]
"""
import os, struct, sys
DIR = sys.argv[1] if len(sys.argv) > 1 else r"D:/FFXII_TZA_extract/ps2data/image/ff12/in/bin"
MODS = ("ctrl", "btlctrl", "evctrl", "mapctrl")
PAGE_PAIRS = {"ctrl": 846, "btlctrl": 4999, "evctrl": 1004, "mapctrl": 5020}  # btlctrl: the page's "5000 pairs" is rounded; it also says "4,999/4,999"
fails = 0
def check(name, ok, detail=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", name, detail)); fails += not ok
f1 = f2 = f3 = f4 = True; rows = []
for m in MODS:
    b = open(os.path.join(DIR, m + ".dbg"), "rb").read(); sbn = open(os.path.join(DIR, m + ".sbn"), "rb").read()
    h = struct.unpack_from("<16I", b, 0); pool, T0, T1, T2, sec0 = h[2], h[1], h[3], h[5], h[11]
    start = lambda p: pool + p < len(b) and (p == 0 or b[pool + p - 1] == 0) and b[pool + p] != 0
    name = lambda p: b[pool + p:b.index(b"\0", pool + p)]
    n = struct.unpack_from("<I", b, T1)[0]; src = struct.unpack_from("<%dI" % n, b, T1 + 4)
    nblk = struct.unpack_from("<I", sbn, 0)[0]
    f1 &= T1 == 0x6C and n == nblk and all(start(x) for x in src) and T1 + 4 + 4 * n == T0 and name(src[0]).endswith(b".src")
    c0 = struct.unpack_from("<I", b, T0)[0]; L0 = struct.unpack_from("<%dI" % c0, b, T0 + 4); e0 = T0 + 4 + 4 * c0
    pad0 = b[e0:T2]
    txt = sbn
    f2 &= all(start(x) for x in L0) and pad0 == bytes(len(pad0)) and T2 == (e0 + 15) // 16 * 16 \
          and (m != "ctrl" or all(name(x) in txt for x in L0))
    c2 = struct.unpack_from("<I", b, T2)[0]; P = struct.unpack_from("<%dI" % (2 * c2), b, T2 + 4); e2 = T2 + 4 + 8 * c2
    f3 &= all(start(P[2 * i + 1]) for i in range(c2)) and P[0] == 0x30000000 and name(P[1]) == b"global_flag[0]" \
          and b[e2:sec0] == bytes(sec0 - e2) and sec0 == (e2 + 15) // 16 * 16
    words_before = (T2 + 4 - 0x6C) // 4
    f4 &= PAGE_PAIRS[m] == c2 + (words_before + 1) // 2 and not any(start(P[2 * i]) for i in range(min(c2, 50)))
    rows.append("%s: T1 n=%d | T0=%X count=%d | T2=%X count=%d, ends %X = section 0 %X" % (m, n, T0, c0, T2, c2, e2, sec0))
for r in rows: print("      " + r)
check("F1", f1, "T1 at +0x6C = the source-file table, n = the .sbn block count, ending at T0")
check("F2", f2, "T0 = {count; nameOffset[count]}, all name starts (ctrl: all in the .sbn text), zero-padded to 16")
check("F3", f3, "T2 = {count; {id; namePos}[count]}, first id 0x30000000 = global_flag[0], padded to the first section")
check("F4", f4, "the page's pair counts = T2's count + the front words read as pairs; its pre-T2 'ids' are name offsets")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
