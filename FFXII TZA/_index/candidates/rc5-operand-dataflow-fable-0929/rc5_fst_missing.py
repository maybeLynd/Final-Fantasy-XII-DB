"""rc5_fst_missing.py - RC-5 residue item 4, the size entries for the three kind-8 'us' event sets whose paths the archive
lacks (FABLE, 2026-09-29). The FST is 41 x 5,000 dwords read whole at boot from ../FileSizeTables/FileSizeTable_<lang>.fst
(file-size-tables-fst.md "How the file is found"); 002DF960 / 0032E400 read size[kind*5000 + id]; the issuer 002DF780
refuses an entry of -1 (002DF7B0-002DF7B9).
The kind-8 FST id of an event set is ORACLE's `row` column in rc5_paths.tsv (set * 4, four entries per set), NOT the set
id: a first version of this script indexed by set id, and its control (set 30 must be present) FAILED, which is how the
mapping was found.
Prints rows row..row+3 of kind 8 for sets 355 (chb_z0000), 398 (msg_z0000), 440 (men_z0004) in all twelve tables.
Control: sets 30 (nal_a0100) and 31 (nal_b0100), both in the archive, must have four positive entries in the US table;
every table must be exactly 41*5000*4 bytes."""
import os, struct, sys
D = r"D:/SteamLibrary/steamapps/common/FINAL FANTASY XII THE ZODIAC AGE/FileSizeTables"
SETS = {355: ("chb_z0000", 1420), 398: ("msg_z0000", 1592), 440: ("men_z0004", 1760)}
CTRL = {30: 120, 31: 124}
fails = 0
for fn in sorted(os.listdir(D)):
    b = open(os.path.join(D, fn), "rb").read()
    if len(b) != 41 * 5000 * 4:
        print(fn, "size", len(b), "not 41x5000 dwords"); fails += 1; continue
    e = lambda k, i: struct.unpack_from("<i", b, (k * 5000 + i) * 4)[0]
    row = "  ".join("%d %s rows %d..%d = %s" % (s, n, r, r + 3, [e(8, r + d) for d in range(4)]) for s, (n, r) in SETS.items())
    print("%-22s %s" % (fn, row))
    if fn.endswith("_US.fst"):
        for s, r in CTRL.items():
            v = [e(8, r + d) for d in range(4)]
            ok = all(x > 0 for x in v)
            print("   CONTROL set %d rows %d..%d = %s -> %s" % (s, r, r + 3, v, "PASS" if ok else "FAIL"))
            fails += not ok
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
