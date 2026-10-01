#!/usr/bin/env python3
"""check_assets.py - how much of what the game SHIPS the database explains.

The gap this measures
---------------------
The database reads engines well and the files they eat barely at all.  Audio has eleven documents
and 2,064 owned functions; `.sab` (4,609 sound banks) and `.snd` (2,304) had one passing mention
between them.  `engine_explained` cannot see that, because it counts functions, and a format nobody
documents costs no functions.

Population, and why it may be scored
------------------------------------
**Every extension in `FFXII_TZA.vbf`.**  `container_format:` was deliberately counted and not
scored, for a stated reason: *"no censused universe of container formats exists, so a percentage
would be invented."*  **That reason is gone.**  The archive index lists all 89,414 shipped entries,
so the population is a `GROUP BY`, not an opinion -- see `census_archive_formats.py`, which
generates the frozen TSV this reads.

The census includes rows nobody will write a sheet for (`.txt`, `.ico`, two `.tga` files).  **They
stay in the denominator**, because pre-trimming a census to the interesting rows is an author
choosing what they will be graded against.  They are cleared by DISPOSITION instead.

The three dispositions
----------------------
Deliberately the same shape as the A/B/C policy `COMPLETION-PLAN.md` sets for `engine_explained`,
because it answers the same objection: *volume of citation is not explanation.*

    explained   a sheet with the loader contract -- what the engine reads, rejects, clamps, ignores.
                The default, and the only one that needs no note.

    standard    an open public format the game did not author.  **Bar: name the standard.**  And the
                note is not a formality -- a game that "uses WebM" still decides which codecs it
                accepts and what it does with one it does not.

    external    the format is documented outside this database and is cross-linked rather than
                re-derived, per `COMPLETION-PLAN.md` section 7.  **Bar: name the reference.**

`standard` and `external` are REFUSED without a note, and a refused entry does not count.  That is
the whole anti-gaming mechanism: the cheap disposition is the one that requires you to write down a
falsifiable claim somebody can check.

Declaring
---------
    archive_formats:
      - "sab"
      - "webm | standard | WebM/Matroska container, VP8 video"
      - "phyre | external | ffxii-tza-tools docs/formats/phyre.md"

Declared, never scraped -- a mention of `.sab` in prose is not a claim to have explained it.  One
owner per format; a format claimed twice is a collision under the standing rule that nothing is
described two ways.

`container_format:` is unchanged and still counted-not-scored.  It names formats that are NOT
archive entries -- the save image, the VBF container itself, `GameSetting.ini` -- and those have no
census, so they keep their honest un-scored count.

A declaration may name a byte signature instead of an extension.  `.dat` is a bucketed namespace
carrying several signatures (`himg`, `hdat`, numeric headers), so a sheet for one of them cannot
declare `dat`.  It declares the signature (`himg`); the token is resolved against
`format-magic-census.tsv`, is reported as signature-scoped, and does not move the numerator -- the
extension row stays the unit.

Usage
-----
    python check_assets.py --db "Database/FFXII TZA"
    python check_assets.py --db "Database/FFXII TZA" --quiet
    python check_assets.py --self-test
"""
import argparse
import collections
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CENSUS_TSV = os.path.join(HERE, "..", "..", "work", "formats", "archive-extension-census.tsv")
MAGIC_TSV = os.path.join(HERE, "..", "..", "work", "formats", "format-magic-census.tsv")

DISPOSITIONS = ("explained", "standard", "external", "bucket")
NEEDS_NOTE = ("standard", "external", "bucket")

# `- "ext | disposition | note"`, with the last two optional.
ENTRY = re.compile(r"^\s*-\s*[\"']?([A-Za-z0-9()]+)"
                   r"(?:\s*\|\s*([a-z]+))?"
                   r"(?:\s*\|\s*(.*?))?[\"']?\s*$")
SKIP_DIRS = ("_index", "_templates", "_inbox")


def load_census(path=None):
    """ext -> (files, bytes, top_dirs) from the generated TSV."""
    path = path or CENSUS_TSV
    out = collections.OrderedDict()
    for line in io.open(path, encoding="utf-8", errors="replace"):
        line = line.rstrip("\n")
        if not line or line.startswith("#") or line.startswith("ext\t"):
            continue
        p = line.split("\t")
        if len(p) >= 3:
            out[p[0]] = (int(p[1]), int(p[2]), p[3] if len(p) > 3 else "")
    return out


def signature_groups(path=None):
    """signature -> [extensions], for extensions that show exactly ONE signature.

    **An extension is a filename convention; a format is a byte layout, and the two do not line
    up in either direction.**  `census_format_magics.py` sampled the archive and found:

        .mot .snd .vpc .vpcjp   all `PKFL`   -- 10,314 files, ONE format, four extensions
        .ca .cm                 both `@FRP`
        .tm2 .nfs               both `TIM2`

    So a sheet that explains `PKFL` has explained four census rows and should declare all four.
    This grouping exists to say so, rather than leaving the author to notice.

    Extensions with several signatures are EXCLUDED from the grouping, because a split is equally
    the shape of a version field in the first four bytes -- `census_format_magics.py` refuses to
    call that either way, and so does this.
    """
    path = path or MAGIC_TSV
    per_ext = collections.defaultdict(list)
    try:
        for line in io.open(path, encoding="utf-8", errors="replace"):
            if line.startswith("#") or line.startswith("ext\t") or not line.strip():
                continue
            p = line.rstrip("\n").split("\t")
            if len(p) >= 3:
                per_ext[p[0]].append(p[2])
    except OSError:
        return {}
    groups = collections.defaultdict(list)
    for ext, sigs in per_ext.items():
        if len(sigs) == 1:
            groups[sigs[0]].append(ext)
    return {s: sorted(e) for s, e in groups.items() if len(e) > 1}


def claimed_formats(db):
    """ext -> [(document, disposition, note)] from `archive_formats:` frontmatter."""
    out = collections.defaultdict(list)
    for root, dirs, files in os.walk(db):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(root, fn), db).replace(os.sep, "/")
            inside = False
            for line in io.open(os.path.join(root, fn), encoding="utf-8",
                                errors="replace").read().split("\n"):
                if line.strip().startswith("archive_formats:"):
                    inside = True
                    continue
                if inside:
                    if line.lstrip().startswith("#"):      # a commented example is not a claim
                        continue
                    m = ENTRY.match(line)
                    if m:
                        disp = (m.group(2) or "explained").strip()
                        note = (m.group(3) or "").strip().rstrip('"').rstrip("'").strip()
                        out[m.group(1)].append((rel, disp, note))
                    elif line.strip():
                        inside = False
    return out


def magic_signatures(path=None):
    """quoted ASCII signature -> [extensions] from the magic census.

    The extension census keys on the filename convention; a declaration may
    instead name a *signature* inside a bucketed extension (`himg` inside
    `.dat`).  A declared token that matches a magic-census signature row is a
    real format, not a stray -- `format-magic-census.tsv` already carries the
    answer (OPUS-REQ-SWE2-DATA-HIMG-TURNS-CHECK-ASSETS-RED).
    """
    path = path or MAGIC_TSV
    out = collections.defaultdict(list)
    try:
        for line in io.open(path, encoding="utf-8", errors="replace"):
            if line.startswith("#") or line.startswith("ext\t") or not line.strip():
                continue
            p = line.rstrip("\n").split("\t")
            if len(p) >= 3 and p[2].startswith("'") and p[2].endswith("'"):
                out[p[2][1:-1]].append(p[0])
    except OSError:
        return {}
    return dict(out)


def evaluate(census, claims, magics=None):
    """-> (counted, refused, collisions, stray, bucketed, magic_scoped)

    `bucket` (SWE2-AUDIT-SPEC ruling, OPUS-REQ-AUDITSPEC-FORMATS-BUCKET-DISPOSITION)
    records that the extension names no single format -- it is a namespace of
    signature families, and the note must name them. It is dispositioned but is
    NOT counted in the numerator: 'adjudicated non-format' is not 'explained'.
    A later `explained` claim on the same extension lands in `collisions`,
    which is the intended upgrade path.

    A declaration that names no extension but DOES name a signature row in the
    magic census is signature-scoped inside a bucketed extension: resolved, not
    counted (the extension row is the numerator unit), and not stray.
    """
    magics = magic_signatures() if magics is None else magics
    counted, refused, stray, bucketed, magic_scoped = {}, [], {}, {}, {}
    for ext, rows in claims.items():
        if ext not in census:
            if ext in magics:
                magic_scoped[ext] = rows
            else:
                stray[ext] = rows
            continue
        good, buckets = [], []
        for doc, disp, note in rows:
            if disp not in DISPOSITIONS:
                refused.append((ext, doc, disp, "unknown disposition"))
            elif disp in NEEDS_NOTE and not note:
                refused.append((ext, doc, disp,
                                "no contents list named" if disp == "bucket"
                                else "no standard/reference named"))
            elif disp == "bucket":
                buckets.append((doc, disp, note))
            else:
                good.append((doc, disp, note))
        if good:
            counted[ext] = good + buckets
        if buckets:
            bucketed[ext] = buckets
    collisions = {e: r for e, r in counted.items() if len(r) > 1}
    return counted, refused, collisions, stray, bucketed, magic_scoped


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db")
    ap.add_argument("--census", default=None)
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)

    if a.self_test:
        import tempfile
        return self_test(tempfile.mkdtemp())
    if not a.db:
        return ap.error("--db or --self-test required")

    census = load_census(a.census)
    counted, refused, collisions, stray, bucketed, magic_scoped = evaluate(
        census, claimed_formats(a.db))

    if a.quiet:
        print("%d\t%d" % (len(counted), len(census)))
        return 0

    print("SHIPPED FILE FORMAT COVERAGE")
    print("  population: %d extensions, censused over %d archive entries. Not a chosen list."
          % (len(census), sum(v[0] for v in census.values())))
    print("")
    print("  covered:    %d / %d  (%.2f %%)"
          % (len(counted), len(census), 100.0 * len(counted) / len(census) if census else 0.0))
    if bucketed:
        print("  bucketed:   %d  (dispositioned non-formats -- not counted above, ceiling stands)"
              % len(bucketed))
    print("")
    by_disp = collections.Counter(r[0][1] for r in counted.values())
    for d in DISPOSITIONS:
        if d == "bucket":
            print("    %-10s %d" % (d, len(bucketed)))
        else:
            print("    %-10s %d" % (d, by_disp.get(d, 0)))
    print("")
    for ext, (n, b, dirs) in census.items():
        if ext in counted:
            doc, disp, note = counted[ext][0]
            print("    [x] %-8s %-9s %s" % (ext, disp, doc))
        elif ext in bucketed:
            doc, disp, note = bucketed[ext][0]
            print("    [~] %-8s %-9s %s" % (ext, disp, doc))
        else:
            print("    [ ] %-8s %6d files  %10.1f MB  %s" % (ext, n, b / 1048576.0, dirs))

    rc = 0
    # MISCATEGORISATION GUARD, added 2026-09-04 after repos-4b found the case.
    #
    # `container_format:` is for formats that are NOT archive entries. A censused extension put
    # there instead of in `archive_formats:` is always wrong -- and it was **invisible**, because
    # this checker only ever read the scored field. `repos-d6` declared `container_format: nmb`
    # for a format that is one of the 48 censused extensions (332 files); the unit simply did not
    # count and nothing said so.
    #
    # **A checker that reads only the field it scores cannot see a value in the wrong field.**
    _c, containers = None, None
    try:
        import check_formats
        _c, containers = check_formats.claimed_slots(a.db)
    except Exception:
        containers = {}
    miscat = {k: v for k, v in (containers or {}).items() if k.lower() in census}
    if miscat:
        rc = 1
        print("\n  MISCATEGORISED - a censused archive extension declared as `container_format`:")
        for ext in sorted(miscat):
            docs = miscat[ext] if isinstance(miscat[ext], list) else [str(miscat[ext])]
            print("    %-8s %s" % (ext, ", ".join(docs)))
        print("  `container_format` is for formats that are NOT archive entries. Move these to")
        print("  `archive_formats:` or the unit stays uncounted and nothing warns you.")

    groups = signature_groups()
    if groups:
        print("\n  SAME-FORMAT GROUPS - one byte layout, several extensions:")
        for sig, exts in sorted(groups.items()):
            claimed_here = [e for e in exts if e in counted]
            gap = [e for e in exts if e not in counted]
            mark = ""
            if claimed_here and gap:
                mark = "   <-- %s claimed, %s not" % (",".join(claimed_here), ",".join(gap))
                rc = 1
            print("    %-14s %s%s" % (sig, " ".join("." + e for e in exts), mark))
        print("  A sheet explaining the layout has explained every row in its group; declare them"
              "\n  all. Extensions with several signatures are excluded - a split is equally the"
              "\n  shape of a version field, and the magic census refuses to call that either way.")
    if refused:
        rc = 1
        print("\n  REFUSED - a disposition that names nothing is not a disposition:")
        for ext, doc, disp, why in refused:
            print("    %-8s %-9s %-28s %s" % (ext, disp, why, doc))
    if collisions:
        rc = 1
        print("\n  FORMATS CLAIMED TWICE - nothing is described two ways:")
        for e in sorted(collisions):
            print("    %-8s %s" % (e, ", ".join(d for d, _p, _n in collisions[e])))
    if magic_scoped:
        magics = magic_signatures()
        print("\n  SIGNATURE-SCOPED DECLARATIONS - resolved through the magic census:")
        for e in sorted(magic_scoped):
            exts = ", ".join("." + x for x in sorted(set(magics.get(e, []))))
            print("    %-8s %s   (signature inside %s)"
                  % (e, ", ".join(d for d, _p, _n in magic_scoped[e]), exts))
        print("  These name a byte signature inside a bucketed extension; the extension")
        print("  row is the numerator unit, so they resolve without being counted.")
    if stray:
        rc = 1
        print("\n  DECLARED FORMATS THAT ARE NOT IN THE CENSUS:")
        for e in sorted(stray):
            print("    %-8s %s" % (e, ", ".join(d for d, _p, _n in stray[e])))
        print("  Either a typo, or a format that ships somewhere the archive listing does not")
        print("  cover. If it is real, that is a finding: regenerate the census and write up why.")
    return rc


SELF_CENSUS = ("ext\tfiles\tbytes\ttop_dirs\n"
               "sab\t4609\t879218608\tps2data/sound (4609)\n"
               "webm\t40\t10881781239\tgamedata/d3d11 (40)\n"
               "phyre\t35984\t27154292432\tgamedata/d3d11 (35984)\n"
               "efx\t3288\t4579689088\tps2data/effect_finish (3288)\n"
               "dat\t2948\t2427457536\tgamedata/d3d11 (2948)\n")

SELF_A = ('---\nsystem: a\narchive_formats:\n'
          '  - "sab"\n'
          '  - "webm | standard | WebM/Matroska, VP8"\n'
          '  - "efx | standard"\n'
          '---\nbody\n')
SELF_B = ('---\nsystem: b\narchive_formats:\n'
          '  - "sab"\n'
          '  - "phyre | external | ffxii-tza-tools docs/formats"\n'
          '  - "zzz"\n'
          '  - "himg"\n'
          '  - "dat | bucket | himg, hdat, hchk, qstd and numeric headers"\n'
          '# - "efx"\n'
          '---\nbody\n')

SELF_MAGIC = {"himg": ["dat"]}


def self_test(tmp):
    db = os.path.join(tmp, "fmt_db")
    if not os.path.isdir(db):
        os.makedirs(db)
    cpath = os.path.join(tmp, "census.tsv")
    io.open(cpath, "w", encoding="utf-8").write(SELF_CENSUS)
    io.open(os.path.join(db, "a.md"), "w", encoding="utf-8").write(SELF_A)
    io.open(os.path.join(db, "b.md"), "w", encoding="utf-8").write(SELF_B)

    census = load_census(cpath)
    counted, refused, collisions, stray, bucketed, magic_scoped = evaluate(
        census, claimed_formats(db), magics=SELF_MAGIC)
    ok = True
    if set(counted) != {"sab", "webm", "phyre"}:
        print("SELF-TEST FAILED: counted %s" % sorted(counted)); ok = False
    if not any(e == "efx" and w == "no standard/reference named" for e, _d, _p, w in refused):
        print("SELF-TEST FAILED: note-less `standard` was not refused"); ok = False
    if "efx" in counted:
        print("SELF-TEST FAILED: refused entry still counted"); ok = False
    if "sab" not in collisions:
        print("SELF-TEST FAILED: collision not detected"); ok = False
    if "zzz" not in stray:
        print("SELF-TEST FAILED: out-of-census extension accepted"); ok = False
    if set(bucketed) != {"dat"} or "dat" in counted:
        print("SELF-TEST FAILED: bucket counted or not tracked (%s)" % sorted(bucketed)); ok = False
    if set(magic_scoped) != {"himg"} or "himg" in stray or "himg" in counted:
        print("SELF-TEST FAILED: signature-scoped declaration not resolved (%s)"
              % sorted(magic_scoped)); ok = False
    if len(census) != 5:
        print("SELF-TEST FAILED: census parsed as %d rows" % len(census)); ok = False
    if not ok:
        return 1
    print("self-test ok: a note-less `standard` refused and not counted, a commented example "
          "ignored, a double claim caught, an extension outside the census refused, "
          "a `bucket` dispositioned but not counted, a signature-scoped claim resolved")
    return 0


if __name__ == "__main__":
    sys.exit(main())
