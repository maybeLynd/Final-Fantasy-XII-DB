#!/usr/bin/env python3
"""Census of atlas names referenced by every shipped typed-list (.mrp) file
in FFXII_TZA.vbf, for FABLE-REQ-SWE2-DATA-ATLAS-NAME-CLOSURE on
a-typed-list-measured-once-and-built-in-one-allocation.md.

Authored side (verified against the same walk as gen_listtype_census.py):

    header  +0x08 u32   items-blob end = start of the 16-byte atlas-name
                        record array
            +0x10 u32   end of the name array (== +0x18 == +0x28 when the
                        +0x24 row table is empty)
            +0x24 u32   file-row count (0 in every shipped unit/file - the
                        "file row" registration path is unpopulated)
            +0x28 u32   file-row table offset
    name record, 16 bytes: NUL-padded atlas name
    items: {u8 length, u8 type} self-sized stream after the outer table
            type 2/9 : atlas index u16 at item +0x0C
            type 7   : required atlas index u16 at +0x0C, optional second
                       atlas index u16 at +0x40 (0xFFFF = none)

Executable side (static reads of the shipping EXE, SHA256
73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8):

    (i) literals that reach 0024A4E0 (atlas-table insert; the only writer
        of the 64-slot table at 0208F580, compare byte-exact in 0024A610):
        - 22-entry pointer block 01E0C1E0..01E0C288 -> strings at
          009152A0.. (used directly by texpack 002467A0 x5 and tex2pack
          00280750's walk, and through .data indirection by 0024A440 /
          0024A480 / 002493D0 call sites)
        - direct literal args at the 00249380/002493D0/0024A440 wrapper
          call sites (incl. the 00D11390 pointer -> 'title_logo')
        - static record tables feeding 00393460/003934F0/003C1D70
          (0x18-stride {subtype,?,name} tables and the 00D231C0 11-row
          0x10-stride table)
    (ii) file rows via 00406D48/004070A1: those loops read the objects at
        [0209AC30]+0x68/70/78/80, which 00280980 fills with mrppack_ys.bin
        units 13..16 (8-byte slots, units 0..22 at +0x00..+0xA8).  Row
        count is the unit's u32 at +0x24 (bound in relocator 002A00F0 and
        the handlers' byte read) - ZERO in every shipped mrppack file, so
        this path registers no name.
    (iii) loca_%d_%d formatted at 003C2824 (fmt literal 00D11630, values
        read from the loaded image - runtime-generated names).

Usage: gen_atlas_name_census.py [vbf-path]
    -> writes atlas-name-census.tsv beside this script and prints the
       per-name classification.
"""
import io, os, sys, struct, re, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..",
                                                 "agent_flow", "tools")))
import vbfextract as V

VBF = sys.argv[1] if len(sys.argv) > 1 else \
    r"D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf"

U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
U16 = lambda b, o: struct.unpack_from("<H", b, o)[0]

# (i) image literals registered through 0024A4E0 - every name verified as a
# literal/pointer-table string argument on a path that ends in 0024A4E0.
BLOCK22 = [
    "targetline_p", "battle_4_c", "battle_4_p", "icons_c", "partytop_4_c",
    "partytop_8_c", "itemgra_c", "bt_win_0_c", "cursol_4_p", "buttonicon",
    "s_font_c", "party_grd_2", "sort_cha_c", "navi_Load", "shop_8_c",
    "chrback_top", "chrback_bottom", "cm_win_c", "shape", "mini_face_c",
    "extra_c", "keyboard",
]
DIRECT = [
    # 00249380 call site 002D6F59 (name in r9)
    "tuto_win_c",
    # 002493D0 call sites (name at [rsp+0x20])
    "Loca_8_c", "LocaBack_c", "w_line01", "sf_logo_c", "lic_4_c",
    "lic_b_4_c", "maru_c", "maru_c_2", "lic_b_8_c", "lic_bk", "cm2_win_c",
    "lic_8_c", "lic_8_c2", "lic_8_c3", "handbook2_c",
    # 0024A440 call site 00575C0D (name in rdx)
    "hb_tex",
    # .data pointer at 00D11390 (00393FF0 site)
    "title_logo",
]
TABLES = [
    # 00D231C0, 11x0x10, walked by 00562F90
    "w_shade_p", "w_main0", "w_main1", "w_main2", "w_main3", "w_icon_p",
    "w_line01", "w_line02", "w_win_c", "map_gra_c", "baseicon",
    # 0x18-stride record tables: 003EF830 00D11C88 / 00572D80 00D23668 /
    # 00574E80 00D23628 / 00579AF0 00D237E0 / 00582790 00D23D80 /
    # 005632C0 [00D23250]
    "gameover_c", "medal_c", "handbook_c", "hand_4_c", "q_img_c",
    "q_under_c", "dataface_c", "map_gra_c",
]
CLASS_I = frozenset(BLOCK22 + DIRECT + TABLES)

LOCA = re.compile(r"^loca_\d+_\d+$")


def classify(name):
    if name in CLASS_I:
        return "i"
    if LOCA.match(name):
        return "iii"
    return "iv"


def cstr(b, off, lim):
    s = b[off:off + lim]
    return s.split(b"\0", 1)[0].decode("ascii", "replace")


def main():
    f = io.open(VBF, "rb")
    names, blocks = V.load_index(f)
    mrps = sorted(p for p in names if p.lower().endswith(".mrp"))

    # --- shipped MRP blobs: standalone .mrp files + mrppack_ys units ------
    blobs = [(p, V.read_entry(f, names, blocks, p)) for p in mrps]
    pack_rows = collections.Counter()
    for p in sorted(n for n in names if "packfiles/mrppack_ys.bin" in n):
        d = V.read_entry(f, names, blocks, p)
        offs = []
        for i in range(0, 0x100, 4):
            v = U32(d, i)
            if v == 0xFFFFFFFF:
                break
            offs.append(v)
        for idx, o in enumerate(offs):
            end = offs[idx + 1] if idx + 1 < len(offs) else len(d)
            blobs.append(("%s#unit%02d" % (p, idx), d[o:end]))
            if idx in (13, 14, 15, 16):
                pack_rows[U32(d, o + 0x24)] += 1
    print("mrppack units 13..16 +0x24 row counts:", dict(pack_rows))

    # --- authored census -------------------------------------------------
    refs = []           # (file, rec, item, type, idx, name, idx2, name2)
    names_seen = collections.defaultdict(set)   # name -> {files referencing}
    array_names = collections.defaultdict(set)  # name -> {files declaring}
    bad_files = []
    idx_oob = []        # references past the name array
    n_ref = 0

    for p, blob in blobs:
        if len(blob) < 0x30 or blob[:4] != b"MRP\x00":
            bad_files.append((p, "bad magic/short"))
            continue
        na, nb = U32(blob, 0x08), U32(blob, 0x10)
        if nb < na or nb > len(blob) or (nb - na) % 16:
            bad_files.append((p, "name array bounds"))
            continue
        nrec = (nb - na) // 16
        nm = [cstr(blob, na + 16 * i, 16) for i in range(nrec)]
        for x in nm:
            array_names[x].add(p)
        n = U32(blob, 0x1C)
        toff = U32(blob, 0x20)
        if toff + 20 * n > len(blob):
            bad_files.append((p, "outer table range"))
            continue
        counts = [U32(blob, toff + 20 * i) & 0x3FF for i in range(n)]
        pos = toff + 20 * n
        rec_i = -1
        left = 0
        for it in range(sum(counts)):
            while left == 0:
                rec_i += 1
                left = counts[rec_i]
            left -= 1
            if pos + 2 > len(blob):
                bad_files.append((p, "item walk past EOF"))
                break
            ln = blob[pos]
            ty = blob[pos + 1]
            if ln < 2 or pos + ln > len(blob):
                bad_files.append((p, "bad item at 0x%x" % pos))
                break
            if ty in (2, 9, 7):
                i1 = U16(blob, pos + 0x0C) if pos + 0x0E <= len(blob) else -1
                i2 = U16(blob, pos + 0x40) if ty == 7 else -1
                n1 = nm[i1] if 0 <= i1 < nrec else None
                n2 = nm[i2] if 0 <= i2 < nrec else None
                if i1 >= nrec or (ty == 7 and 0 <= i2 < 0xFFFF and i2 >= nrec):
                    idx_oob.append((p, it, ty, i1, i2, nrec))
                refs.append((p, rec_i, it, ty, i1, n1, i2, n2))
                n_ref += 1
                if n1 is not None:
                    names_seen[n1].add(p)
                if n2 is not None:
                    names_seen[n2].add(p)
            pos += ln

    # --- emit ------------------------------------------------------------
    tsv = io.open(os.path.join(HERE, "atlas-name-census.tsv"), "w",
                  encoding="utf-8", newline="\n")
    tsv.write("# typed-list atlas-name census - every shipped .mrp; item "
              "atlas refs (type2/9 +0x0C; type7 +0x0C required, +0x40 "
              "optional 0xFFFF=none) resolved through the 16-byte name "
              "records at [hdr+0x08 .. hdr+0x10)\n")
    tsv.write("file\trec\titem\ttype\tatlas_idx\tname\tidx2\tname2\n")
    for r in refs:
        tsv.write("%s\t%d\t%d\t%d\t%d\t%s\t%s\t%s\n" % (
            r[0], r[1], r[2], r[3], r[4],
            r[5] if r[5] is not None else "<OOB:%d>" % r[4],
            "0x%04x" % r[6] if r[6] >= 0 else "-",
            r[7] if r[7] is not None else "-"))
    tsv.write("\n# distinct name-record census - every name in a shipped "
              "typed-list name array, referenced or not; class = (i) image-"
              "literal/registration-table name, (ii) file-row name "
              "(mrppack units 13..16 +0x24 rows), (iii) loca_%d_%d, "
              "(iv) none of those\n")
    tsv.write("name\tdeclared_files\treferenced\tclass\tref_files\n")
    for name in sorted(array_names):
        rf = sorted(names_seen.get(name, ()))
        tsv.write("%s\t%d\t%s\t%s\t%s\n" % (
            name, len(array_names[name]),
            "yes" if rf else "no",
            classify(name) if rf else "-",
            ";".join(rf) if rf else "-"))
    tsv.close()

    print("blobs", len(blobs), "refs", n_ref, "distinct names",
          len(names_seen), "bad", bad_files, "oob", idx_oob)
    by_cls = collections.defaultdict(list)
    for name in sorted(names_seen):
        by_cls[classify(name)].append((name, len(names_seen[name]),
                                       sorted(names_seen[name])))
    for c in ("i", "ii", "iii", "iv"):
        for name, nf, files in by_cls[c]:
            print("(%s) %-16s files=%2d  %s" % (
                c, name, nf,
                files[0] if nf == 1 else "%s (+%d)" % (files[0], nf - 1)))


if __name__ == "__main__":
    main()
