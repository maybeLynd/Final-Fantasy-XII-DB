#!/usr/bin/env python3
"""check_surface_figures.py - the four current-state surfaces against the authoritative stores.

WHY THIS EXISTS. README.md, PROGRAM-STATE.md, TYPE-COVERAGE.md and COVERAGE-DIMENSIONS.md each quote
figures that live somewhere else: the type store, the GFZ ledger, the layout validator. Nothing
regenerates COVERAGE-DIMENSIONS, and no gate reads its type-store row - so on 2026-09-16 it still
said "1992 / 1389 named" after sixteen namings had landed, and every other gate passed. A figure that
no instrument regenerates and no gate reads is exactly where staleness survives.

WHAT IS AUTHORITATIVE, and it is never the prose:

    types / fields / named / unresolved   _types/fields.tsv, counted
    gap records                           types_index.py --validate
    GFZ explicit / internal / unresolved   Tools/work/verify_GFZ_PARENT/coverage.tsv

WHAT IT DOES NOT DO. It reads the numbers a surface quotes for ITS OWN CURRENT STATE. It does not
touch struck-through or dated checkpoint text, because preserving history is the point of writing it
that way - a line reading "~~247 / 1,857~~" is a record of what was true, not a claim about now, and
a checker that cannot tell those apart would force the history to be rewritten to stay green.

usage: check_surface_figures.py [--db DB]
"""
import argparse
import io
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
DEFAULT_DB = os.path.join(ROOT, "Database", "FFXII TZA")
LEDGER = os.path.join(ROOT, "Database", "Tools", "work", "verify_GFZ_PARENT", "coverage.tsv")


def strip_history(text):
    """Drop struck-through spans, so preserved checkpoint text is not read as a current claim."""
    return re.sub(r"~~.*?~~", " ", text, flags=re.S)


def store_counts(db):
    rows = [l.split("\t") for l in io.open(os.path.join(db, "_types", "fields.tsv"),
                                           encoding="utf-8").read().splitlines()[1:]
            if l.count("\t") >= 8]
    unres = sum(1 for r in rows if r[3] == "UNRESOLVED")
    types = len({r[0] for r in rows})
    return types, len(rows), len(rows) - unres, unres


def ledger_figures():
    if not os.path.exists(LEDGER):
        return None
    head = io.open(LEDGER, encoding="utf-8").readline()
    return {k: v for k, v in re.findall(r"(\w+)=([\d.]+)", head)}


def game_engine_split(db):
    """(game types, engine types, fields on a game type) from the type store.

    DERIVED, not declared: types.tsv has no game/engine flag. Its `category` column is the
    system folder, and 22-Middleware-PhyreEngine holds the engine/middleware types. The
    partition is safe to gate on because TWO independently written figures agree with it -
    COVERAGE-DIMENSIONS' 182 engine and 69 GAME, and PROGRAM-STATE's GAME types 69.
    """
    tp = os.path.join(db, "_types", "types.tsv")
    fp = os.path.join(db, "_types", "fields.tsv")
    if not (os.path.exists(tp) and os.path.exists(fp)):
        return None
    tl = io.open(tp, encoding="utf-8", errors="replace").read().split(chr(10))
    th = tl[0].split(chr(9))
    ti = {k: th.index(k) for k in th}
    if "category" not in ti or "type" not in ti:
        return None
    rows = [l.split(chr(9)) for l in tl[1:] if l.strip()]
    engine = {r[ti["type"]] for r in rows if len(r) > ti["category"]
              and r[ti["category"]] == "22-Middleware-PhyreEngine"}
    gm = {r[ti["type"]] for r in rows} - engine
    fl_ = io.open(fp, encoding="utf-8", errors="replace").read().split(chr(10))
    fr = [l.split(chr(9)) for l in fl_[1:] if l.strip()]
    return len(gm), len(engine), sum(1 for r in fr if r[0] in gm)


def per_type_counts(db):
    """named and total per type, from the authoritative field store."""
    import collections
    p = os.path.join(db, "_types", "fields.tsv")
    tot, named = collections.Counter(), collections.Counter()
    lines = io.open(p, encoding="utf-8", errors="replace").read().split(chr(10))
    hdr = lines[0].split(chr(9))
    idx = {k: hdr.index(k) for k in hdr}
    for l in lines[1:]:
        if not l.strip():
            continue
        r = l.split(chr(9))
        if len(r) <= idx["name"]:
            continue
        tot[r[0]] += 1
        if r[idx["name"]].strip() not in ("", "UNRESOLVED"):
            named[r[0]] += 1
    return named, tot


# A PER-TYPE ROW IS A QUOTED FIGURE TOO. The gate checked only the aggregates, and on
# 2026-09-16 six of 251 rows disagreed with the store while the total was exactly right
# because the errors cancelled - BattleUnit 122/140 against a store of 115/140, and
# BattleSystemState 19/33 against 24/33. A total that is right because two mistakes offset
# is precisely what these gates exist to refuse.
PER_TYPE_ROW = re.compile(r"^\|\s*`([A-Za-z0-9_]+)`\s*\|[^|]*\|[^|]*\|\s*(\d+)\s*/\s*(\d+)\s*\|")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DEFAULT_DB)
    a = ap.parse_args()

    types, fields, named, unres = store_counts(a.db)
    print("authoritative: %d types, %d fields, %d named, %d UNRESOLVED" % (types, fields, named, unres))
    led = ledger_figures()
    if led:
        print("authoritative: GFZ explicit=%s internal=%s unresolved=%s pct=%s"
              % (led.get("explicit"), led.get("internal"), led.get("unresolved"), led.get("pct")))

    bad = []
    surfaces = {
        "README.md": os.path.join(a.db, "README.md"),
        "_index/PROGRAM-STATE.md": os.path.join(a.db, "_index", "PROGRAM-STATE.md"),
        "_index/TYPE-COVERAGE.md": os.path.join(a.db, "_index", "TYPE-COVERAGE.md"),
        "_index/COVERAGE-DIMENSIONS.md": os.path.join(a.db, "_index", "COVERAGE-DIMENSIONS.md"),
    }
    for name, path in surfaces.items():
        if not os.path.exists(path):
            continue
        body = strip_history(io.open(path, encoding="utf-8", errors="replace").read())
        # "1,991 / 1,405" and "1991 field(s) ... 1405 named" are the two shapes in use
        for m in re.finditer(r"(\d[\d,]*)\s*(?:field\(s\)|fields)[^.\n]{0,40}?(\d[\d,]*)\s*named", body):
            f, n = (int(x.replace(",", "")) for x in m.groups())
            if (f, n) != (fields, named):
                bad.append("%s: quotes %d fields / %d named, store has %d / %d" % (name, f, n, fields, named))
        for m in re.finditer(r"(\d[\d,]*)\s*/\s*(\d[\d,]*)\s*/\s*(\d[\d,]*)", body):
            t, f, n = (int(x.replace(",", "")) for x in m.groups())
            if t == types and (f, n) != (fields, named):
                bad.append("%s: quotes %d / %d / %d, store has %d / %d / %d"
                           % (name, t, f, n, types, fields, named))
        # COVERAGE-DIMENSIONS writes it as a bare pair in a table cell - "| fields recorded / of
        # those named | 1991 / 1415 |" - which neither shape above matches. That row is the reason
        # this checker exists, so it has to be the one shape it cannot miss.
        for m in re.finditer(r"fields recorded / of those named\s*\|\s*(\d[\d,]*)\s*/\s*(\d[\d,]*)",
                             body, re.I):
            f, n = (int(x.replace(",", "")) for x in m.groups())
            if (f, n) != (fields, named):
                bad.append("%s: quotes %d / %d recorded/named, store has %d / %d"
                           % (name, f, n, fields, named))
        for m in re.finditer(r"(\d[\d,]*)\s*fields?\s+UNRESOLVED", body, re.I):
            u = int(m.group(1).replace(",", ""))
            if u != unres:
                bad.append("%s: quotes %d UNRESOLVED, store has %d" % (name, u, unres))
        if led:
            for m in re.finditer(r"(\d[\d,]*)\s*/\s*(\d[\d,]*)\s*=\s*([\d.]+)\s*%", body):
                e, i, p = m.group(1).replace(",", ""), m.group(2).replace(",", ""), m.group(3)
                if i == led.get("internal") and (e != led.get("explicit") or p != led.get("pct")):
                    bad.append("%s: quotes GFZ %s / %s = %s %%, ledger has %s / %s = %s %%"
                               % (name, e, i, p, led.get("explicit"), led.get("internal"), led.get("pct")))
            # AND THE KEY=VALUE FORM, which was unchecked and is a SECOND COPY OF THE SAME NUMBERS
            # ON THE SAME LINE. README.md carries both: the prose "38,131 / 38,161 = 99.92139 %"
            # and, beside it, `V121_COVERAGE internal=38161 owner=9409 finalNo=585
            # codeDomain=28137 overlap=0 explicit=38131 unresolved=30`. Only the prose form was
            # matched, so the block could drift on its own and this gate would still report the
            # surfaces agreeing with the stores.
            #
            # Found by CONTROL rather than by reading: a scratch copy of the four surfaces with
            # README's `explicit=38131` changed to `explicit=38099` still passed, 2026-09-15. The
            # gate was put in the baseline that morning on the strength of it catching four stale
            # figures, which is exactly how a partial check earns trust it has not got - it had
            # never been asked to fail on this shape.
            for key, want in (("explicit", led.get("explicit")), ("internal", led.get("internal")),
                              ("unresolved", led.get("unresolved"))):
                if want is None:
                    continue
                # NO WHITESPACE AROUND THE `=`, and that is the whole discriminator. The ledger
                # block is emitted machine-style - `internal=38161 ... explicit=38131
                # unresolved=30` - while PROSE about the same quantity is spaced: PROGRAM-STATE
                # line 50 reads "`unresolved = 0` is the terminal gate's first precondition" and
                # line 5579 "the largest single residual movement of the campaign, and
                # `unresolved = 0`". Those are statements about the TARGET, not quotations of the
                # current value, and the first cut of this check reported both as stale figures.
                # A checker that cannot tell a goal from a measurement manufactures defects.
                for m in re.finditer(r"\b%s=(\d[\d,]*)" % key, body):
                    got = m.group(1).replace(",", "")
                    if got != str(want):
                        bad.append("%s: quotes %s=%s, ledger has %s=%s"
                                   % (name, key, got, key, want))

    # the GAME / engine split in COVERAGE-DIMENSIONS section 6 - three more quoted figures
    # that no gate read. 'fields on a GAME type' drifted to 1347 against a store of 1346.
    split = game_engine_split(a.db)
    cd = os.path.join(a.db, "_index", "COVERAGE-DIMENSIONS.md")
    if split and os.path.exists(cd):
        cdt = io.open(cd, encoding="utf-8", errors="replace").read()
        for label, want, pat in (
                ("GAME types in the store", split[0],
                 r"GAME types in the `_types/` store\*\*\s*\|\s*\*\*(\d+)\*\*"),
                ("engine/middleware types", split[1],
                 r"engine / middleware types in the store\s*\|\s*(\d+)"),
                ("fields on a GAME type", split[2],
                 r"fields on a GAME type\*?\s*\|\s*(\d+)")):
            m = re.search(pat, cdt)
            if m and int(m.group(1)) != want:
                bad.append("_index/COVERAGE-DIMENSIONS.md: %s quotes %s, store has %d"
                           % (label, m.group(1), want))

    # the per-type rows, against the same store the totals came from
    ptn, ptt = per_type_counts(a.db)
    cov = os.path.join(a.db, "_index", "TYPE-COVERAGE.md")
    if os.path.exists(cov) and ptt:
        checked = 0
        for line in io.open(cov, encoding="utf-8", errors="replace"):
            m = PER_TYPE_ROW.match(line)
            if not m or m.group(1) not in ptt:
                continue
            checked += 1
            t = m.group(1)
            if (int(m.group(2)), int(m.group(3))) != (ptn[t], ptt[t]):
                bad.append("_index/TYPE-COVERAGE.md: %s row says %s/%s, store has %d/%d"
                           % (t, m.group(2), m.group(3), ptn[t], ptt[t]))
        print("  per-type rows checked against the store: %d" % checked)

    print()
    if bad:
        print("SURFACE FIGURES STALE: %d" % len(bad))
        for b in bad:
            print("  " + b)
        return 1
    print("surface figures agree with the authoritative stores")
    return 0


if __name__ == "__main__":
    sys.exit(main())
