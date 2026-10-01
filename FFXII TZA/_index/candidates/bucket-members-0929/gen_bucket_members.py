#!/usr/bin/env python3
"""gen_bucket_members.py - the member formats of the `.bin` and `.dat` extension buckets (SWE2-DATA, 2026-09-29).

OPUS-REQ-DATA-BUCKET-MEMBER-FORMATS / FABLE C4 (mp1-meanings-review): a bucketed extension is not a requirement; its
member formats are. This script assigns EVERY archive entry of the two bucketed extensions to exactly one member format
and writes the declaration My Progress (Database/Tools/dashboard/requirements.py, family X) reads.

A member format is a byte layout with a consumer-bound sheet, not a leading dword. The leading dword is kept as the
signature column because that is what the census measures, but it is not the key: four census signatures are shared by
unrelated formats (`00 00 00 00`, `80 00 00 00`, `01 00 00 00`, `'FLAG'`), and six different leading patterns belong to
one format (the byte-doubled `bin_menu` images, whose first bytes are pixels). So the unit of assignment is the
LOGICAL UNIT (the archive path with the locale segment folded, as census_bin_signatures.py keys it), matched by the
rules below; the signature column is derived from the entries a member actually took, written `SIG=N` when a signature
is split between members (DATA-REQ-OPUS-BUCKET-MEMBERS-SHARED-SIGNATURES).

Inputs
  --bin-census / --dat-census  per-entry signature censuses from census_bin_signatures.py (--ext .bin / .dat) over
                               FFXII_TZA.vbf; default Database/Tools/work/formats/{bin,dat}-signature-census.tsv
  --full-census                the tracked full-archive leading-signature census (census_format_magics.py --sample
                               100000): _index/candidates/bucket-members-input-0929/format-magic-census-full.tsv
Outputs (canonical copy first)
  Database/FFXII TZA/_index/bucket-members.tsv                    ext, family, signatures, entries, units, sheet
  _index/candidates/bucket-members-0929/bucket-member-units.tsv   ext, unit, signature, entries, family
  Database/Tools/work/formats/bucket-members.tsv                  byte-identical convenience copy for the MP-2 reader
                                                                  committed before MP-3 (gitignored, NOT canonical)
Checks (printed; FAILS count; exit 1 on any failure; --check writes nothing)
  C1 every entry matches exactly one rule                 C2 per-signature entry counts reproduce the full census
  C3 member entries sum to the extension's census total    C4 every member names a sheet that exists
  C5 each rule's expected signatures are exactly the ones it took (a rule that silently absorbs a new signature fails)
  C6 control: a synthetic unit that matches no rule is reported, not absorbed
"""
import argparse, collections, io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
REPO = os.path.normpath(os.path.join(DB, "..", ".."))
WORK = os.path.join(REPO, "Database", "Tools", "work", "formats")
FULL = os.path.join(DB, "_index", "candidates", "bucket-members-input-0929", "format-magic-census-full.tsv")
OUT_CANON = os.path.join(DB, "_index", "bucket-members.tsv")
OUT_UNITS = os.path.join(HERE, "bucket-member-units.tsv")
OUT_WORK = os.path.join(WORK, "bucket-members.tsv")

PF = "02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/"
VB = "02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/"
# (ext, family token, unit regex, expected census signatures, sheet). Order matters only for readability: C1 fails on
# any unit two rules match. The family token is what a sheet's signature-scoped `archive_formats:` row names.
RULES = [
    # ---- .dat (five families; the buckets page's closed-bucket table) ----
    ("dat", "himg", r"/handbook/menuhandbook_[a-z]+\d+\.dat$@himg", {"'himg'"}, PF + "himg-handbook-image-bundles.md"),
    ("dat", "hdat", r"/handbook/menuhandbook_[a-z]+\d+\.dat$@hdat", {"'hdat'"}, PF + "hchk-hctg-hdat-handbook-indexes.md"),
    ("dat", "hchk", r"/handbook/menuhandbook_[a-z]+\.dat$", {"'hchk'"}, PF + "hchk-hctg-hdat-handbook-indexes.md"),
    ("dat", "qstd", r"/quest/menuquest\.dat$", {"'qstd'"}, PF + "five-small-bin-tables.md"),
    ("dat", "fontdat", r"^gamedata/d3d11/artdata/font/[^/]+\.dat$", None,
     "16-UI/Text-And-Number-Rendering/font-data-kerning-and-expansion.md"),
    # ---- .bin ----
    ("bin", "sloc", r"/worldmap/menumap_sub\d+(_e\d+)?\.bin$", {"'sloc'"}, PF + "sloc-menumap-container.md"),
    ("bin", "st2e", r"/binaryfile/[a-z_0-9]+\.bin$@st2e", {"'st2e'"}, VB + "vbf-archive-and-st2e-tables.md"),
    ("bin", "hctg", r"/handbook/menuhandbook_(knowledge|monster|person|story|tutorial|world)\.bin$", {"'hctg'"},
     PF + "hchk-hctg-hdat-handbook-indexes.md"),
    ("bin", "licd", r"/binaryfile/(board_\d+|license_board)\.bin$", {"'licd'"},
     "12-Items-Equipment-Shops-License/license-board-grid-format.md"),
    ("bin", "gmap", r"/worldmap/menumap_guide\d+\.bin$", {"'gmap'"}, PF + "gmap-menumap-guide-texts.md"),
    ("bin", "flagdef", r"/bin/mapjumpgroupinit\.bin$", {"'FLAG'"}, "14-Story-Event-Quest-Hunt/persistent-flag-banks.md"),
    ("bin", "flagrom", r"/bin/mapjumpgroupflagrom\.bin$", {"'FLAG'"}, "14-Story-Event-Quest-Hunt/persistent-flag-banks.md"),
    ("bin", "binmenuimage", r"/bin_menu/(face_guest\d+|map_efe\d+|mini_guest_face)\.bin$",
     {"'CCdd'", "D1 D1 F4 F4", "C9 C9 E3 E3", "E5 E5 E5 E5", "BA BA A3 A3", "'//22'", "00 00 00 00"},
     PF + "binmenu-guest-face-and-map-effect-images.md"),
    ("bin", "CHSE", r"/common/charseinfo_[a-z]\.bin$", {"'CHSE'"}, PF + "chse-character-se-tables.md"),
    ("bin", "NPC0", r"/bin/npcdic\.bin$", {"'NPC0'"}, "04-Actor-Entity/Actor-Names/the-npc-name-dictionary.md"),
    ("bin", "PLMN", r"/bin/planmapname\.bin$", {"'PLMN'"},
     "03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md"),
    ("bin", "QST1", r"/bin/questbase\.bin$", {"'QST1'"}, PF + "five-small-bin-tables.md"),
    ("bin", "sign", r"/bin_menu/key_signal_data\.bin$", {"'sign'"}, PF + "five-small-bin-tables.md"),
    ("bin", "bwin", r"/bin_menu/menubtlwndinfo\.bin$", {"'bwin'"}, PF + "five-small-bin-tables.md"),
    ("bin", "MENU", r"/bin_menu/menu_version\.bin$", {"'MENU'"}, PF + "five-small-bin-tables.md"),
    ("bin", "hcom", r"/handbook/menuhandbook\.bin$", {"'hcom'"}, "16-UI/Handbook/the-handbook-screen.md"),
    ("bin", "hodr", r"/handbook/menuhandbook_order\.bin$", {"'hodr'"}, "16-UI/Handbook/the-handbook-screen.md"),
    ("bin", "menuquest", r"/quest/menuquest\d+\.bin$", None, PF + "menuquest-bin-quest-detail-tables.md"),
    ("bin", "amap", r"/worldmap/menumap_area\.bin$", {"'amap'"}, PF + "amap-menumap-area-table.md"),
    ("bin", "cmap", r"/worldmap/menumap_common\.bin$", {"'cmap'"}, PF + "cmap-menumap-common-sublocation-directory.md"),
    ("bin", "lmap", r"/worldmap/menumap_location\.bin$", {"'lmap'"}, PF + "lmap-menumap-location-graph.md"),
    ("bin", "wmap", r"/worldmap/menumap_world\.bin$", {"'wmap'"}, PF + "wmap-menumap-world-map-graph.md"),
    ("bin", "battlepack", r"/binaryfile/battle_pack\.bin$", {"47 00 00 00"}, VB + "vbf-archive-and-st2e-tables.md"),
    ("bin", "wordbanks", r"/binaryfile/word\.bin$", {"0F 00 00 00"}, VB + "St2e-Carriers/battle-text-banks.md"),
    ("bin", "commandpack", r"/binaryfile/commandpack\.bin$", {"3A 03 00 00"}, VB + "vbf-archive-and-st2e-tables.md"),
    ("bin", "shopdata", r"/binaryfile/shop_data\.bin$", {"64 00 00 00"}, VB + "vbf-archive-and-st2e-tables.md"),
    ("bin", "wepjobmatrix", r"/binaryfile/wepjob_matrix\.bin$", {"01 00 17 00"}, VB + "vbf-archive-and-st2e-tables.md"),
    ("bin", "scriptimage", r"/bin/(ctrl|btlctrl|evctrl|mapctrl)\.bin$", {"0B 00 00 80"},
     "25-EBP-Script-Container/Bytecode-And-Opcodes/section-000-bytecode.md"),
    ("bin", "NAV", r"/bin/navimapdata\.bin$", {"4E 41 56 02"},
     "03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md"),
    ("bin", "skeletonmapping", r"^ps2data/add_motion/skeletonmapping\.bin$", {"01 00 00 00"},
     "17-Presentation-Rendering/Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md"),
    ("bin", "highmodelreplace", r"^ps2data/add_motion/highmodelreplace\.bin$", {"00 00 63 00"},
     "17-Presentation-Rendering/Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md"),
    ("bin", "testmapref", r"/common/test_map_ref\.bin$", {"01 00 00 00"}, "03-World-Area-Field/choosing-the-field-environment-variant.md"),
    ("bin", "testarearef", r"/common/test_area_ref\.bin$", {"00 00 01 00"}, "03-World-Area-Field/choosing-the-field-environment-variant.md"),
    ("bin", "MRF", r"/common/map_ref\.bin$", {"4D 52 46 02"}, "03-World-Area-Field/choosing-the-field-environment-variant.md"),
    ("bin", "filelistlocalin", r"/bin/filelistlocalin\.bin$", {"98 00 00 00"}, PF + "unnamed-bin-families.md"),
    ("bin", "GRMI", r"/common/gramap_weatherinfo\.bin$", {"'GRMI'"}, "03-World-Area-Field/Weather/mweather-resource-format.md"),
    ("bin", "MUS0", r"/common/musicctrl\.bin$", {"'MUS0'"}, "18-Audio/the-music-control-file-and-the-bgm-stream.md"),
    ("bin", "musicinfo", r"/common/musicinfo\.bin$", {"80 00 00 00"}, "18-Audio/how-the-music-changes-when-you-change-area.md"),
    ("bin", "pcskillmotion", r"/common/pc_skillmotion\.bin$", {"21 00 00 00"}, PF + "loader-bound-bin-families.md"),
    ("bin", "fontcolor", r"/bin_menu/fontcolor\.bin$", {"07 01 00 00"}, PF + "loader-bound-bin-families.md"),
    ("bin", "itemclut", r"/bin_menu/item_clut\.bin$", {"00 00 00 80"}, PF + "binmenu-guest-face-and-map-effect-images.md"),
    ("bin", "licensechip", r"/bin_menu/license_chip\.bin$", {"01 00 02 00"}, "12-Items-Equipment-Shops-License/license-board-grid-format.md"),
    ("bin", "monotonechr", r"/bin_menu/monotone_chr\.bin$", {"'CLT2'"}, PF + "loader-bound-bin-families.md"),
    ("bin", "st2enames", r"/binaryfile/(basic_skill_basic_skill_name|growth_rate_growth_rate_name)\.bin$",
     {"41 05 00 00", "80 00 00 00"}, PF + "unnamed-bin-families.md"),
    ("bin", "logicpack", r"/binaryfile/logicpack\.bin$", {"1E 05 00 00"}, PF + "unnamed-bin-families.md"),
    ("bin", "ashd", r"^ps2data/image/ff12/katano/event\.bin$", {"'ashd'"}, PF + "unnamed-bin-families.md"),
    ("bin", "EVME", r"/common/eventmemorylist\.bin$", {"'EVME'"}, "14-Story-Event-Quest-Hunt/event-memory-at-actor-bind.md"),
    ("bin", "VIB0", r"/common/eventvib\.bin$", {"'VIB0'"}, PF + "five-small-bin-tables.md"),
    ("bin", "fhmusicdata", r"/common/fhmusicdata\.bin$", {"1B 00 00 00"}, "18-Audio/the-music-control-file-and-the-bgm-stream.md"),
    ("bin", "FOOT", r"/common/soundfoottable\.bin$", {"'FOOT'"}, PF + "five-small-bin-tables.md"),
    ("bin", "summoneffectdata", r"/common/summoneffectdata\.bin$", {"'dP<d'"}, PF + "five-small-bin-tables.md"),
    ("bin", "behindcamera", r"/common/behindcamera\.bin$", {"00 00 00 00"}, PF + "loader-bound-bin-families.md"),
    ("bin", "packdirectory", r"/packfiles/((clut|tex|tex2|mrp)pack_ys|fontpack_(fs|it))\.bin$", {"40 00 00 00", "80 00 00 00"},
     PF + "loader-bound-bin-families.md"),
]


def read_entries(path, ext):
    out = []
    for l in io.open(path, encoding="utf-8"):
        if l.startswith("#") or l.startswith("path\t"):
            continue
        c = l.rstrip("\r\n").split("\t")
        if len(c) >= 4:
            out.append((ext, c[0], c[1], bytes.fromhex(c[3])))
    return out


def read_full(path):
    """ext -> {sig bytes: (printed signature, entries)}."""
    out = collections.defaultdict(dict)
    for l in io.open(path, encoding="utf-8-sig"):
        c = l.rstrip("\r\n").split("\t")
        if l.startswith("#") or len(c) < 4 or c[0] not in ("bin", "dat"):
            continue
        s = c[2].strip()
        b = s[1:-1].encode("latin-1") if s.startswith("'") and s.endswith("'") else bytes.fromhex(s.replace(" ", ""))
        out[c[0]][b] = (s, int(c[3]))
    return out


def match(rule, unit, sigtext):
    rx = rule[2]
    need = None
    if "@" in rx:
        rx, need = rx.split("@")
    return bool(re.search(rx, unit)) and (need is None or sigtext == "'%s'" % need)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--bin-census", default=os.path.join(WORK, "bin-signature-census.tsv"))
    ap.add_argument("--dat-census", default=os.path.join(WORK, "dat-signature-census.tsv"))
    ap.add_argument("--full-census", default=FULL)
    ap.add_argument("--check", action="store_true", help="run the checks, write nothing")
    a = ap.parse_args(argv)
    fails = []

    def chk(cid, ok, msg):
        print("%s %s  %s" % (cid, "PASS" if ok else "FAIL", msg))
        if not ok:
            fails.append(cid)

    full = read_full(a.full_census)
    entries = read_entries(a.bin_census, "bin") + read_entries(a.dat_census, "dat")
    assign = collections.defaultdict(lambda: collections.Counter())        # family -> Counter(sig printed)
    units = collections.defaultdict(lambda: collections.Counter())         # (ext, unit, sig, family) -> n
    fam_units = collections.defaultdict(set)
    unmatched, multi, unknown_sig = [], [], []
    for ext, path, unit, sb in entries:
        if sb not in full[ext]:
            unknown_sig.append((ext, path, sb.hex()))
            continue
        sig = full[ext][sb][0]
        hits = [r for r in RULES if r[0] == ext and match(r, unit, sig)]
        if len(hits) != 1:
            (unmatched if not hits else multi).append((ext, unit, sig, [h[1] for h in hits]))
            continue
        fam = hits[0][1]
        assign[(ext, fam)][sig] += 1
        units[(ext, unit, sig, fam)][0] += 1
        fam_units[(ext, fam)].add(unit)
    chk("C1", not unmatched and not multi and not unknown_sig,
        "%d entries; unmatched %d, matched by two rules %d, signature absent from the full census %d %s"
        % (len(entries), len(unmatched), len(multi), len(unknown_sig), (unmatched + multi + unknown_sig)[:4]))
    per_sig = collections.Counter()
    for (ext, fam), c in assign.items():
        for s, n in c.items():
            per_sig[(ext, s)] += n
    bad = [(ext, v[0], v[1], per_sig.get((ext, v[0]), 0)) for ext in ("bin", "dat") for v in full[ext].values()
           if per_sig.get((ext, v[0]), 0) != v[1]]
    chk("C2", not bad, "per-signature entries reproduce the full census: %d bin + %d dat rows%s"
        % (len(full["bin"]), len(full["dat"]), "" if not bad else "; mismatches %s" % bad[:6]))
    for ext in ("bin", "dat"):
        tot = sum(sum(c.values()) for (e, f), c in assign.items() if e == ext)
        want = sum(v[1] for v in full[ext].values())
        chk("C3", tot == want, ".%s members sum to %d entries, census %d" % (ext, tot, want))
    missing_sheet = [(r[1], r[4]) for r in RULES if r[4] and not os.path.isfile(os.path.join(DB, r[4]))]
    pending = [r[1] for r in RULES if not r[4]]
    chk("C4", not missing_sheet, "every named sheet exists%s; %d member(s) with no sheet yet: %s"
        % ("" if not missing_sheet else " - missing %s" % missing_sheet, len(pending), ", ".join(pending) or "none"))
    drift = []
    for r in RULES:
        got = set(assign.get((r[0], r[1]), {}))
        if not got:
            drift.append((r[1], "took no entries"))
        elif r[3] is not None and got != r[3]:
            drift.append((r[1], sorted(got ^ r[3])))
    chk("C5", not drift, "each rule took exactly its expected signatures%s" % ("" if not drift else ": %s" % drift))
    probe = [r for r in RULES if r[0] == "bin" and match(r, "ps2data/image/ff12/zz/nosuch_table.bin", "'zzzz'")]
    chk("C6", not probe, "control: an invented unit matches no rule (%d matched)" % len(probe))
    sys.path.insert(0, os.path.join(REPO, "Database", "Tools", "analysis-kit", "gfz-scripts"))
    import check_assets as CA
    claims = CA.claimed_formats(DB)
    unclaimed = [(r[1], r[4]) for r in RULES if r[4] and not any(
        doc == r[4] and disp in ("explained", "standard", "external") for doc, disp, _n in claims.get(r[1], []))]
    chk("C7", not unclaimed, "each member's sheet carries a signature-scoped explained/standard/external row naming it%s"
        % ("" if not unclaimed else "; missing %s" % unclaimed))

    # signature column: bare when the member holds every entry of that signature, SIG=N when it is shared
    holders = collections.defaultdict(set)
    for (ext, fam), c in assign.items():
        for s in c:
            holders[(ext, s)].add(fam)
    rows = []
    for r in RULES:
        ext, fam = r[0], r[1]
        c = assign.get((ext, fam), collections.Counter())
        sigs = []
        for s, n in sorted(c.items(), key=lambda kv: (-kv[1], kv[0])):
            sigs.append(s if len(holders[(ext, s)]) == 1 else "%s=%d" % (s, n))
        rows.append((ext, fam, ",".join(sigs), sum(c.values()), len(fam_units[(ext, fam)]), r[4] or "PENDING"))
    for ext in ("bin", "dat"):
        print("  .%s: %d members, %d entries, %d units" % (ext, sum(1 for x in rows if x[0] == ext),
              sum(x[3] for x in rows if x[0] == ext), sum(x[4] for x in rows if x[0] == ext)))
    print("FAILS %d" % len(fails))
    if a.check:
        return 1 if fails else 0
    if fails:
        print("not written: checks failed")
        return 1
    head = ("# Member formats of the bucketed extensions (.bin, .dat) - generated by "
            "_index/candidates/bucket-members-0929/gen_bucket_members.py; do not hand-edit.\n"
            "# CANONICAL copy (OPUS-REQ-DATA-BUCKET-MEMBER-FORMATS). A member is a byte layout bound to a consumer by its sheet;\n"
            "# 'signatures' are the census leading signatures its entries carry - SIG=N where one signature is split between\n"
            "# members (the leading dword is not a format identity). Entry-level assignment: bucket-member-units.tsv.\n"
            "ext\tfamily\tsignatures\tentries\tunits\tsheet\n")
    body = "".join("%s\t%s\t%s\t%d\t%d\t%s\n" % x for x in rows)
    for p in (OUT_CANON, OUT_WORK):
        if os.path.isdir(os.path.dirname(p)):
            with io.open(p, "w", encoding="utf-8", newline="\n") as f:
                f.write(head + body)
    with io.open(OUT_UNITS, "w", encoding="utf-8", newline="\n") as f:
        f.write("# every logical unit of .bin/.dat -> its member format; entries = archive entries (locale copies) of that "
                "unit carrying that signature\next\tunit\tsignature\tentries\tfamily\n")
        for (ext, unit, sig, fam), c in sorted(units.items()):
            f.write("%s\t%s\t%s\t%d\t%s\n" % (ext, unit, sig, c[0], fam))
    print("wrote %s, %s, %s" % (OUT_CANON, OUT_UNITS, OUT_WORK))
    return 0


if __name__ == "__main__":
    sys.exit(main())
