"""RC-28 leftovers 2 and 3 (SWE2-DATA 2026-09-30), static + shipped data.

(2) The KR and CN arms name ExFont .btm paths the archive does not hold. The file-size tables decide what happens:
    FileSizeTable_<LANG>.fst holds size[kind * 5000 + id], 0xFFFFFFFF = no file. The read issuer 002DF780 refuses a
    (kind, id) whose entry is -1 before resolving any path (002DF7B0 cmp dword [..], -1 / je -> return 0), and the size
    query 0032E400 returns the entry unrounded when it is not positive (0032E43D jle). So a KR/CN .btm request opens
    no file (no fallback path is tried in 002DF780) and sizes its buffer with -1.
(3) Whether any shipped staff-roll text in the six arms that pair the us fontpack_fs.bin with the in .btm (lang 1..6:
    US FR DE IT ES UK, rc28_lang_arms.py) uses one of the 49 accented glyphs that only the us tables 8..11 carry.
    The staff-roll text is the ex00 UTF-16 rows of menu03.bin (roles) and menu04.bin (names) (the glyph-run page's
    UQ census). For each lang the file is the arm's kind-2 array entry (ids 0x41 menu03, 0x42 menu04; the same
    arm simulation) for 'menu03.bin' / 'menu04.bin'; every ex00 row is decoded (UTF-16LE to a zero unit) and its
    characters are classified against the 78-glyph set (table 6 of the us pack) and the 49 extra (tables 8..11).
Controls: C1 the us pack's tables 8..11 hold 127 codes = the 78 of table 6 plus 49; C2 the ex00 row scan of
us/menu04.bin decodes 'Hiroshi Minagawa' (the glyph-run page's first name); C3 FileSizeTable_US has positive
sizes for the six .btm (the KR/CN -1 is not a reader artefact).
"""
import os, re, struct, sys, collections, glob
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc22-34-resource-readers-0930"))
src = open(os.path.join(HERE, "rc28_lang_arms.py"), encoding="utf-8").read().split("rows = []")[0]
exec(src.replace("print(\"FAILS %d\" % FAILS)", ""))   # arm simulation: run(lang), LANG, u64, cstr, check, FAILS

FST = r"D:/SteamLibrary/steamapps/common/FINAL FANTASY XII THE ZODIAC AGE/FileSizeTables"
EXT = "D:/FFXII_TZA_extract"


def fst(lang):
    b = open(os.path.join(FST, "FileSizeTable_%s.fst" % lang), "rb").read()
    return lambda k, i: struct.unpack_from("<i", b, 4 * (k * 5000 + i))[0]


# (2)
print("(2) kind-7 .btm sizes (ids 0xDA..0xDF) per language")
for L in ("US", "KR", "CN", "CH", "IN"):
    v = fst(L)
    print("   %-4s %s" % (L, [v(7, i) for i in range(0xDA, 0xE0)]))
check("C3 FileSizeTable_US sizes the six .btm positively", all(fst("US")(7, i) > 0 for i in range(0xDA, 0xE0)))
check("R2a FileSizeTable_KR and _CN hold -1 (no file) for all six .btm ids",
      all(fst(L)(7, i) == -1 for L in ("KR", "CN") for i in range(0xDA, 0xE0)))
rd = {x.address: x for x in dis(0x002DF780)}
check("R2b the read issuer refuses an entry of -1 before resolving a path (002DF7B0 / 002DF7B9 -> 002DF85D returns 0)",
      rd[0x002DF7B0].op_str.endswith(", -1") and rd[0x002DF7B9].op_str == "0x2df85d"
      and rd[0x002DF862].op_str == "eax, eax")
sz = {x.address: x for x in dis(0x0032E400)}
check("R2c the size query returns a non-positive entry unrounded (0032E43D jle 0032E44B)",
      sz[0x0032E43D].mnemonic == "jle" and sz[0x0032E43D].op_str == "0x32e44b")

# (3)
PS2 = EXT + "/ps2data/image/ff12/myoshiok"


def tables(path):
    b = open(path, "rb").read()
    g = struct.unpack_from("<I", b, 0)[0]
    n = struct.unpack_from("<h", b, g)[0]
    t = g + 4
    out = []
    for i in range(n):
        if i:
            t += struct.unpack_from("<i", b, t)[0]
        cnt = struct.unpack_from("<i", b, t + 4)[0]
        out.append([struct.unpack_from("<HBBBBBBI", b, t + 16 + 12 * k)[0] for k in range(cnt)])
    return out


tb = tables(PS2 + "/us/packfiles/fontpack_fs.bin")
set78 = set(tb[6])
ext = set(tb[8]) - set78
check("C1 us tables 8..11 = the 78 of table 6 plus 49 more", all(set(tb[s]) == set78 | ext for s in (8, 9, 10, 11))
      and len(set78) == 78 and len(ext) == 49, "%d + %d" % (len(set78), len(ext)))


def ex_rows(path):
    b = open(path, "rb").read()
    rows = []
    for m in re.finditer(rb"ex00", b):
        p = m.end()
        units = []
        while p + 1 < len(b):
            u = b[p] | b[p + 1] << 8
            if u == 0:
                break
            units.append(u)
            p += 2
        rows.append("".join(chr(u) for u in units))
    return rows


def find_file(lang, name):
    """the kind-2 array (test_battle BinaryFile, the message banks) of the lang's arm: menu03 = id 0x41, menu04 = 0x42"""
    slots, _, _ = run(lang)
    arr = slots.get(2)
    i = {"menu03.bin": 0x41, "menu04.bin": 0x42}[name]
    p = u64(arr + 8 * i) if arr else None
    s = cstr(p, 260) if p else None
    return s if s and s.lower().endswith(name) else None


r = ex_rows(EXT + "/ps2data/image/ff12/test_battle/us/binaryfile/menu04.bin")
check("C2 the us/menu04.bin ex00 scan decodes 'Hiroshi Minagawa'", "Hiroshi Minagawa" in r, repr(r[:2]))
tot_acc = collections.Counter()
other = collections.Counter()
for lang in range(1, 7):
    for nm in ("menu03.bin", "menu04.bin"):
        pth = find_file(lang, nm)
        if pth is None:
            print("   lang %d %s: no path" % (lang, nm))
            continue
        parts = pth.split(chr(92))
        rel = "/".join(p.lower() for p in parts[1:])
        f = EXT + "/ps2data/" + rel
        rows = ex_rows(f) if os.path.exists(f) else []
        chars = collections.Counter(c for row in rows for c in row)
        acc = {c: n for c, n in chars.items() if ord(c) in ext}
        oth = {c: n for c, n in chars.items() if ord(c) not in ext and ord(c) not in set78 and c != " "}
        tot_acc.update(acc)
        other.update(oth)
        print("   lang %d %-2s %-10s -> %s: %d rows, accented-49 chars %s, outside both sets %s" %
              (lang, LANG[lang], nm, "/".join(parts[3:]), len(rows),
               "".join(sorted(acc)).encode("ascii", "backslashreplace").decode() or "none",
               "".join(sorted(oth)).encode("ascii", "backslashreplace").decode() or "none"))
print("   accented-49 occurrences over the six arms: %d" % sum(tot_acc.values()))
print("RESULT accented glyphs in staff-roll text of the us-pack arms: %s" %
      ("none" if not tot_acc else "".join(sorted(tot_acc)).encode("ascii", "backslashreplace").decode()))
print("FAILS %d" % FAILS)
