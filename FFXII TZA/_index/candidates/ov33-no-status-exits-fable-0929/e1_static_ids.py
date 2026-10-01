"""e1_static_ids.py - every UNGATED producer whose (kind, id) is a constant or an authored/static table, checked against
the -1 set of all 12 shipped FileSizeTables.  (OV-33 E1)

"Ungated" = the 0032E620/0032E780 call is reached whatever 0032E400 returned for the same pair (read by hand; sites
in README). Gated producers (a size <= 0 or < 0 skips the call) cannot reach E1 and are not listed here.
Positive controls: (0,0) sized in every language (system.cnf, 57 B); (35, 9) is -1 in every language (kind 35 empty).
Terminal line: FAILS n / STATUS.
"""
import struct, os
ROOT = r"D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\FileSizeTables"
LANGS = ["JP", "US", "FR", "DE", "IT", "ES", "UK", "KR", "CH", "ASIA", "IN", "CN"]
T = {L: struct.unpack("<205000i", open(os.path.join(ROOT, "FileSizeTable_%s.fst" % L), "rb").read()) for L in LANGS}
SITES = [
    ("0024AC9F 0024AC30 via 0024AC10(p) p!=1 (router tick, +0xCC=2 -> p=2) : kind 35 id p+7", [(35, 9)]),
    ("0024AC9F 0024AC30 via 0024ACE0 -> 0024AC30(1,1) (002D70F0 state 11)   : kind 35 id 8", [(35, 8)]),
    ("0024AC9F 0024AC30 any p (id = p+7), p in 0..15 shown", [(35, 7 + p) for p in range(16)]),
    ("00268809 MapRef_BeginLoadResources (size from 00268762 not tested)", [(9, 4)]),
    ("00291D04 00291C80 loop ebx 0..9 : kind 7 id 0x98+ebx", [(7, 0x98 + i) for i in range(10)]),
    ("002C900B 002C8EE0 loop edi 0..1 : kind 7 id 0x74+edi", [(7, 0x74 + i) for i in range(2)]),
    ("00365967 003658F0 : kind 7 id 0xD2", [(7, 0xD2)]),
    ("003658C7 00365810 via 0053EB90 msg 1, ecx 7..12 -> table 00D10C98[6..11]", [(7, i) for i in (218, 219, 220, 221, 222, 223)]),
    ("003658C7 00365810 table 00D10C98[0..5] (no caller passes 1..6; shown for completeness)", [(7, i) for i in (130, 131, 132, 133, 134, 135)]),
    ("0039C45D 0039C3F0 : kind 7 id 0xD5", [(7, 0xD5)]),
    ("003B5427 003B53C0 : kind 9 id 0x2A", [(9, 0x2A)]),
    ("0051ED89 via 003EAB60 (boot 00379D32) : kind 9 id 0x20", [(9, 0x20)]),
    ("0051ED89 via 003EAC40 NpcDictionary_Load (boot 00379D24) : kind 9 id 0x1F", [(9, 0x1F)]),
    ("0051ED89 via 00473D20 (boot 00379D29) : kind 9 id 0x21", [(9, 0x21)]),
    ("002EF336 002EF300 debug_loadjfdata, const bytes 0xE240 : kind 1 id 0x75+clamp(slot,0,15)", [(1, 0x75 + s) for s in range(16)]),
    ("003EAE4C 003EADE0 BGM stream (script verbs) : kind 0x24 any index, 0..3 shown", [(0x24, i) for i in range(4)]),
    ("002FC96F 002FC860 fallback ids after a failed size (0x78 / 0x8A / 0) for kinds 0xB and 0x26", [(0xB, 0x78), (0xB, 0x8A), (0xB, 0), (0x26, 0x78), (0x26, 0x8A), (0x26, 0)]),
]
fails = 0
c1 = all(T[L][0] == 57 for L in LANGS); c2 = all(T[L][35 * 5000 + 9] == -1 for L in LANGS)
print("control (0,0) == 57 in all 12:", c1); fails += not c1
print("control (35,9) == -1 in all 12:", c2); fails += not c2
for desc, pairs in SITES:
    print("\n" + desc)
    for k, i in pairs:
        bad = [L for L in LANGS if T[L][k * 5000 + i] == -1]
        print("  (%2d,%4d)  -1 in: %s" % (k, i, ",".join(bad) if bad else "none (sized in all 12)"))
print("\nFAILS %d" % fails)
print("STATUS %s" % ("COMPLETE" if fails == 0 else "INCOMPLETE"))
