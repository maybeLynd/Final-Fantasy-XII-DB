#!/usr/bin/env python3
"""check_dispositions.py - the A/B/C/D disposition surface for functions (EC-7).

The gap this closes
-------------------
`COMPLETION-PLAN.md` section 3 defines **A individually explained / B class-explained /
C dispositioned**, `GOAL-REVISION-2026-09-08.md` adds **D**, and section 3 says all of them are
*"declared in frontmatter, never inferred -- the same rule as `registry_slots` and `ebp_units`"*.

**No such key existed and nothing read one.**  A search on 2026-09-12 found exactly one
`disposition:` and one `family:` key in the whole database, neither in the plan's sense; of the ~90
scripts here, only `check_assets.py` implemented A/B/C and it did so **for archive formats**.  So the
formats dimension got the mechanism and the function dimension, which the policy was written for,
never did.  That is `EC-7`, and this file is its declaration surface, census and validator.

What this is NOT
----------------
This tool reports a **separate** measurement from `engine_explained`, and `progress.py` prints it
**unweighted, taking weight from nothing**, until all three identities have recorded a position --
OPUS and FABLE have, ASTRA's is requested as `OPUS-REQ-ASTRA-DISPOSITION-POSITION`.  A weighted
dimension is the program-level decision `EC-7` reserves and it is not being taken by one identity.

**This paragraph used to say "it does not redefine `engine_explained` -- that dimension keeps its
meaning (a citation count)", and the second half of that is no longer true.**  On 2026-09-14
SWE2-AUDIT-SPEC adjudicated the rule after OPUS measured its three axes and routed the choice:
`engine_explained` now counts a function when an EVIDENCE-BEARING page cites it interior, or cites
the entry of a body under 128 bytes.  The headline fell 41.45% -> 23.54%.  What stands is the reason
the sentence was written: **one agent does not move the headline**, and one did not.

The four dispositions
---------------------
Deliberately the same shape as `check_assets.py`, because it answers the same objection:
*volume of citation is not explanation.*

    A  individually explained  MEASURED, never declared.  A function is A when an EVIDENCE-BEARING
                               document cites an address STRICTLY INSIDE its body.  Evidence-bearing
                               is ONE LADDER across both vocabularies -- `status: DOCUMENTED` or
                               `AUDITED`, or `readiness:` at BEHAVIORALLY UNDERSTOOD or above -- and
                               the test is imported from `progress.evidence_bearing` so this gate
                               and the headline cannot drift apart again.  Reading `status:` alone
                               was blind to 47 CONTRACT pages and to 88 interior citations.
                               An entry-only citation is a mention and stays in the frontier --
                               that is the whole difference from `engine_explained`, which counts
                               any citation that lands in the body, entry included.

    B  class-explained         a family with one shared body shape, explained once.  **Bar: the
                               note must answer "could ignorance of this family prevent
                               reproducing FFXII?"**  A B family is one where the answer is
                               "no, given this page".

    C  dispositioned           not this game's code.  **Bar: the note must name the upstream
                               (vendor, CRT, compiler, template) AND state the boundary.**

    D  declared exception      an unresolved operation kept VISIBLE.  **Bar: the note must give a
                               reason and a resume condition.**  Counted separately and NEVER
                               added to any explained total -- D exists so that something unsolved
                               cannot be quietly retired.

                               **D IS 0 AND THAT IS A RULING, NOT AN OVERSIGHT.**  Two populations
                               have been proposed for it and both were refused, on the same
                               ground:

                                 the ~1,309 unlisted code blocks -- UC-1, voted 3-0 (FABLE, OPUS,
                                 ASTRA) for admitting them to the population AS FRONTIER with a
                                 recorded series break.  FABLE's objection defeated the D route
                                 and OPUS, who proposed it, changed vote: *"D means declared
                                 exception and these bytes are UNEXPLAINED ENGINE CODE, which is
                                 precisely the exclusion COMPLETION-PLAN forbids inventing."*

                                 the 30 remaining ledger residuals -- considered 2026-09-14 and
                                 refused by the same argument before it was filed.  They have a
                                 reason and a resume condition, so they clear the stated bar, but
                                 declaring them would shrink the FRONTIER by 30 and make unsolved
                                 engine code read as dispositioned.  The bar is necessary and not
                                 sufficient.

                               **The test D actually encodes is not "is it unresolved" but "is it
                               OURS to resolve".**  Unexplained engine code always is, however
                               long it stays unexplained, so it belongs in the frontier where its
                               size is visible -- never in a category that removes it from the
                               count.  Anything that legitimately enters D would be an operation
                               the project cannot perform at all, and the corpus has not yet found
                               one.  **A zero here is a finding; do not fill it to make a surface
                               look complete.**

B, C and D are **refused without a note**, and a refused row counts as nothing.  That is the
anti-gaming mechanism: the cheap disposition is the one that makes you write down a falsifiable
claim somebody can check.

Declaring
---------
In a document's frontmatter::

    function_families:
      - "owned-buffer-reset adapters | B | members/df1-reset-adapters.tsv | 46 | <the note>"

Five fields, `|`-separated: **name | letter | members file | count | note**.  The members file is
relative to the declaring document and holds one function entry address per line (a `#` comment
line and a blank line are ignored).  It is the reproducible artefact: the population is a list
somebody else can re-derive and diff, not a number in prose.

Refusals, and every one of them is a hard zero for that row
-----------------------------------------------------------
    1. a letter that is not B, C or D
    2. a missing or empty note
    3. a members file that cannot be read
    4. a members file with NO members -- a zero-case cannot pass
    5. a members file that names the same function TWICE -- cardinality counts unique functions
    6. a declared count that does not match the members file
    7. a member address that is not a function entry in the census
    8. one function declared by two families
    9. one function both declared and measured as A

Known limitation, stated rather than hidden
-------------------------------------------
A row records its selector in the note; this tool **does not re-run it**.  It verifies the members
file is internally consistent, matches its declared count, and names only real function entries.
Whether the checker should dispatch a named selector itself -- and whether a
shell-command-in-frontmatter is an acceptable instrument at all -- is the open half of
`OPUS-REQ-ASTRA-DISPOSITION-POSITION`, because it is a tooling and reproducibility question and
that is ASTRA's lane.  Until it is answered, a members file is a committed artefact under review,
not a re-derived one, and this docstring is the place that says so.

Usage
-----
    python check_dispositions.py --db "Database/FFXII TZA"
    python check_dispositions.py --db "Database/FFXII TZA" --json
    python check_dispositions.py --self-test
"""
import argparse
import bisect
import collections
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import uc1_band

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB = os.path.join(HERE, "..", "..", "..", "FFXII TZA")
DEFAULT_FN = os.path.join(HERE, "..", "..", "work", "graph", "functions.tsv")

LETTERS = ("B", "C", "D")
SKIP_DIRS = ("_index", "_templates", "_inbox", "_experiments", "_types")

# `- "name | letter | members | count | note"`
ENTRY = re.compile(r'^\s*-\s*["\']?(.+?)["\']?\s*$')
# the same citation pattern progress.py uses, so the two dimensions read one corpus the same way
CITE = re.compile(r"`(?:0x)?(0[0-9A-Fa-f]{7})`")


def load_functions(path=None):
    """entry -> body size, from the frozen census. The denominator is a census, not an opinion.

    **Funclets are excluded, exactly as `progress.py` excludes them** -- names beginning
    `Unwind@` or `Catch_All@`, 3,887 of them.  This is not a detail.  `progress.py` carries a
    comment recording the day that exclusion was applied on one side of a cross-check and not the
    other: *"a cross-check between two counts is only a check when both count the same
    population.  I built this warning to catch mixed state and its first act was to manufacture
    some."*  This dimension exists to be read BESIDE `engine_explained`, so it must count the
    same population or the comparison is noise.

    SERIES BREAK 2026-09-28 (OPUS-REQ-DATA-UC1-POPULATION-READERS): loading the
    DEFAULT census applies the UC-1 B bands (`uc1_band.apply`) - 34,269
    listed + 795 frontier = 35,064. A fixture path loads exactly what it names.
    """
    path = path or DEFAULT_FN
    sizes = {}
    with io.open(path, encoding="utf-8", errors="replace") as f:
        head = f.readline().rstrip("\n").split("\t")
        ia, inm, isz = head.index("entry"), head.index("name"), head.index("body_bytes")
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) <= max(ia, inm, isz):
                continue
            if p[inm].startswith(("Unwind@", "Catch_All@")):
                continue
            try:
                a, n = int(p[ia], 16), int(p[isz])
            except ValueError:
                continue
            if n > 0:
                sizes[a] = n
    if os.path.realpath(path) == os.path.realpath(DEFAULT_FN):
        sizes, _band_info = uc1_band.apply(sizes)
    return sizes


def docs(db):
    out = []
    for root, _d, files in os.walk(db):
        rel = os.path.relpath(root, db).split(os.sep)[0]
        if rel in SKIP_DIRS:
            continue
        for f in sorted(files):
            if f.endswith(".md") and f != "README.md":
                out.append(os.path.join(root, f))
    return out


def _bearing(text):
    """`progress.evidence_bearing`, loaded from the scorer so the two gates share ONE definition.

    Duplicating the ladder here is how they drifted apart in the first place: this gate read
    `status:` and the corpus also writes `readiness:`. Importing costs a module load and makes a
    silent divergence impossible."""
    global _EB
    try:
        return _EB(text)
    except NameError:
        pass
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "progress_eb", os.path.join(os.path.dirname(os.path.abspath(__file__)), "progress.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    _EB = m.evidence_bearing
    return _EB(text)


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    return m.group(1) if m else ""


def measure_a(db, sizes, paths=None):
    """A = a DOCUMENTED page cites an address STRICTLY INSIDE a body. Entry-only is not A.

    Two filters separate this from `engine_explained`: the page must be DOCUMENTED, and the
    citation must be interior.  The two are reported separately (`any_interior`, `documented_any`)
    so the gap between the dimensions can be ATTRIBUTED rather than asserted -- a single headline
    difference invites the reading that one number is the truth and the other is a lie, and
    neither is.
    """
    entries = sorted(sizes)
    a_set, entry_only = set(), set()
    any_interior, documented_any = set(), set()
    for p in (paths if paths is not None else docs(db)):
        t = io.open(p, encoding="utf-8", errors="replace").read()
        # ONE LADDER, NOT TWO. `^status:\s*DOCUMENTED$` was blind to every CONTRACT page, which
        # carries `readiness:` instead - 47 system documents, 21 of them at BEHAVIORALLY UNDERSTOOD
        # and 13 at CONTRACT READY, with 88 functions cited INSIDE THE BODY by such a page and by no
        # `DOCUMENTED` page. SWE2-AUDIT-SPEC adjudicated the two ladders into one (9efc6221) and
        # named this gate as carrying the same blind spot as `engine_explained`; both now use
        # `progress.evidence_bearing`, so they cannot drift apart again.
        is_doc = _bearing(t)
        for h in CITE.findall(t):
            v = int(h, 16)
            i = bisect.bisect_right(entries, v) - 1
            if i < 0:
                continue
            e = entries[i]
            if not (e <= v < e + sizes[e]):
                continue
            if v > e:
                any_interior.add(e)
            if is_doc:
                documented_any.add(e)
                (a_set if v > e else entry_only).add(e)
    # UC-1 frontier bodies are frontier BY RULING, never A/B/C by default (FABLE
    # band ruling s5).  A mechanical interior cite cannot explain one; strip them
    # from every measured set.  `& set(sizes)` keeps fixture populations (which
    # never carry the band) unaffected.
    uc1f = uc1_band.frontier_starts() & set(sizes)
    a_set -= uc1f
    entry_only -= uc1f
    any_interior -= uc1f
    documented_any -= uc1f
    return a_set, (entry_only - a_set), any_interior, documented_any


def parse_families(db, paths=None):
    """Every `function_families:` row in the corpus, with the document that declares it."""
    rows = []
    for p in (paths if paths is not None else docs(db)):
        t = io.open(p, encoding="utf-8", errors="replace").read()
        fm = frontmatter(t)
        m = re.search(r"^function_families:\s*$", fm, re.M)
        if not m:
            continue
        for line in fm[m.end():].split("\n"):
            if re.match(r"^\S", line):          # next top-level key ends the block
                break
            if not line.strip():
                continue
            g = ENTRY.match(line)
            if not g:
                continue
            parts = [x.strip() for x in g.group(1).split("|")]
            rows.append((p, parts))
    return rows


def read_members(doc_path, rel):
    """One function entry address per line. `#` and blank lines ignored.

    A LEADING COLUMN HEADER IS ALLOWED, because the corpus writes them: 25 of the 123 files under
    a `members/` directory begin with a header row - `address\tname\tbytes...`,
    `function\tname\tsize...`, `entry\tname\tfamily...`. On 2026-09-16 that refused a whole
    family declaration with "members file unreadable: invalid literal for int() with base 16:
    'address'", which reads as a corrupt file and was a perfectly good one written in the other
    half of the house style.

    ONLY THE FIRST DATA LINE may be a header, because a header can only be first. A non-hex line
    anywhere else still raises, so a genuinely corrupt file fails exactly as loudly as before -
    this widens the grammar, it does not soften the check.
    """
    base = os.path.join(os.path.dirname(doc_path), rel.replace("/", os.sep))
    out = []
    first = True
    for line in io.open(base, encoding="utf-8", errors="replace"):
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        tok = line.split()[0].replace("0x", "")
        if first:
            first = False
            if not re.fullmatch(r"[0-9A-Fa-f]{6,8}", tok):
                continue                  # a column header, not a member
        out.append(int(tok, 16))
    return out


def evaluate(db, sizes, paths=None):
    a_set, entry_only, any_interior, documented_any = measure_a(db, sizes, paths)
    rows = parse_families(db, paths)

    accepted, refused = [], []
    owner = {}                       # function -> (family name, doc) for the collision test
    for doc, parts in rows:
        name = parts[0] if parts else "(unnamed)"
        who = "%s :: %s" % (os.path.basename(doc), name)

        def reject(why):
            refused.append((who, why))

        if len(parts) < 5:
            reject("needs five fields: name | letter | members | count | note")
            continue
        _, letter, rel, count, note = parts[0], parts[1], parts[2], parts[3], "|".join(parts[4:])
        if letter not in LETTERS:
            reject("letter %r is not B, C or D (A is measured, never declared)" % letter)
            continue
        if not note.strip():
            reject("%s without a note -- the bar is a falsifiable claim, not a label" % letter)
            continue
        try:
            members = read_members(doc, rel)
        except (IOError, OSError, ValueError) as e:
            reject("members file %r unreadable: %s" % (rel, e))
            continue
        if not members:
            reject("members file %r names NO functions -- a zero-case cannot pass" % rel)
            continue
        # A family's cardinality must count UNIQUE functions.  `len(list)` certifies a population
        # that the deduplicated bucket below does not agree with, so a repeat inside one file is
        # refused here rather than silently inflating the declared count.
        # ASTRA-CONTRA-OPUS-EC7-DUPLICATE-MEMBER, 2026-09-13.  The cross-family collision test
        # further down cannot catch this: `owner` is only populated AFTER this row's members are
        # accepted, so a row never sees itself.
        repeated = sorted(m for m, n in collections.Counter(members).items() if n > 1)
        if repeated:
            reject("members file %r repeats %d function(s), e.g. %08X -- a family's cardinality "
                   "must count unique functions" % (rel, len(repeated), repeated[0]))
            continue
        try:
            declared = int(count)
        except ValueError:
            reject("count %r is not a number" % count)
            continue
        if declared != len(members):
            reject("declared %d, members file holds %d" % (declared, len(members)))
            continue
        bad = [m for m in members if m not in sizes]
        if bad:
            reject("%d member(s) are not function entries, e.g. %08X" % (len(bad), bad[0]))
            continue
        # UC-1 frontier bodies enter `sizes` through the band but are frontier BY
        # RULING - a family declaration cannot claim one (s5: never A/B/C by
        # default, never D). Naming one is a refused declaration, not a member.
        uc1f = uc1_band.frontier_starts() & set(sizes)
        uc1bad = [m for m in members if m in uc1f]
        if uc1bad:
            reject("%d member(s) are UC-1 frontier bodies - frontier by ruling, "
                   "never declared, e.g. %08X" % (len(uc1bad), uc1bad[0]))
            continue
        clash = [m for m in members if m in owner]
        if clash:
            reject("%d function(s) already declared by %s, e.g. %08X"
                   % (len(clash), owner[clash[0]][0], clash[0]))
            continue
        overlap_a = [m for m in members if m in a_set]
        if overlap_a:
            # This refusal is almost always STALENESS, not a bad family: someone cited a member
            # well enough to measure it as A, and the members file has not been regenerated since.
            # It happened twice on 2026-09-13 (Lua, then PPFX) and each time cost a manual
            # diagnosis and a misleading headline, so the message names the cure. A generated
            # family declares its selector in its own note; re-running it re-excludes the new A.
            sel = re.search(r"\(([\w/.-]*select_[\w-]+\.py)\)", note or "")
            cure = ("  -- re-run %s, which excludes A-measured entries by design" % sel.group(1)
                    if sel else
                    "  -- if this family is generated, re-run its selector; A beats a declaration")
            reject("%d member(s) are already measured as A, e.g. %08X%s"
                   % (len(overlap_a), overlap_a[0], cure))
            continue
        for m in members:
            owner[m] = (who, doc)
        accepted.append((who, letter, members, note))

    buckets = collections.OrderedDict((k, set()) for k in ("A", "B", "C", "D"))
    buckets["A"] = set(a_set)
    for who, letter, members, note in accepted:
        buckets[letter] |= set(members)
    explained = buckets["A"] | buckets["B"] | buckets["C"]      # D is NEVER added
    frontier = set(sizes) - explained - buckets["D"]
    uc1f = uc1_band.frontier_starts() & set(sizes)
    band = ({"listed": len(sizes) - len(uc1f), "frontier": len(uc1f),
             "held": len(uc1_band.held())} if uc1f else None)
    return {
        "total": len(sizes), "band": band, "uc1_frontier": len(uc1f),
        "A": len(buckets["A"]), "B": len(buckets["B"]),
        "C": len(buckets["C"]), "D": len(buckets["D"]),
        "explained": len(explained), "frontier": len(frontier),
        "entry_only": len(entry_only),
        # HALF THE ENTRY-ONLY POPULATION IS ALREADY EXPLAINED ABOVE. A body can be
        # cited only at its entry by one page AND claimed by a declared B/C family that
        # explains it as a class; the arithmetic counts it in A+B+C while the prose
        # below counted it as an outstanding mention, in the same report. The two
        # measures were never intersected. EVIDENCE-STANDARD addendum 2026-09-13p.
        "entry_only_declared": sum(1 for f in entry_only if f in owner),
        "any_interior": len(any_interior), "documented_any": len(documented_any),
        "families_accepted": len(accepted), "families_refused": len(refused),
        "refusals": refused,
        "accepted": [(w, l, len(m)) for w, l, m, _n in accepted],
        # THE SETS THEMSELVES, so no second reader has to rebuild them. check_frontier_shape did
        # rebuild them - it walked the members files directly, under a comment saying its
        # definition was "EXACTLY check_dispositions'". It was not: reading the members files
        # counts every family, while the accounting above counts only the ACCEPTED ones, so four
        # families refused for overlapping A still claimed their 300 members over there. The two
        # readers reported frontiers 296 apart and check_frontier_shape failed its own control,
        # taking check_untouched_runs down with it. One definition, exported, consumed.
        "frontier_set": frontier, "explained_set": explained,
        "claimed_set": buckets["B"] | buckets["C"] | buckets["D"],
    }


def report(r, quiet=False):
    print("FFXII TZA - function disposition (A/B/C/D), EC-7")
    print()
    print("  population (function bodies in the census): %d" % r["total"])
    if r.get("band"):
        b = r["band"]
        print("      post-2026-09-28 series: %d listed + %d UC-1 frontier"
              % (b["listed"], b["frontier"]))
        print("      held (declared uncertainty, counted nowhere)    : %d"
              % b["held"])
        print("      pre-2026-09-28 figures count the 34,270 listed bodies - a")
        print("      different population identity, annotated, not restated")
    print("  A  individually explained (interior cite, evidence-bearing page)   : %6d"
          % r["A"])
    print("  B  class-explained          (declared)                               : %6d" % r["B"])
    print("  C  dispositioned            (declared)                               : %6d" % r["C"])
    print("  D  declared exception       (declared, NOT counted as explained)     : %6d" % r["D"])
    print("  -" * 36)
    pct = (100.0 * r["explained"] / r["total"]) if r["total"] else 0.0
    print("  explained (A + B + C)                                                : %6d  %.2f%%"
          % (r["explained"], pct))
    print("  frontier  (declared by nothing)                                      : %6d"
          % r["frontier"])
    if r.get("band"):
        print("      of which UC-1 1-64 B band (unexplained code admitted"
              " 2026-09-28)  : %6d" % r["band"]["frontier"])
    print()
    print("  WHERE THE GAP COMES FROM -- attributed, not asserted. Two filters separate A from")
    print("  engine_explained, and they are worth different amounts:")
    print("      cited anywhere in a body, any document      (engine_explained's measure)")
    print("      cited anywhere in a body, DOCUMENTED page : %6d" % r["documented_any"])
    print("      cited INSIDE a body, any document         : %6d" % r["any_interior"])
    print("      cited INSIDE a body, DOCUMENTED page  = A : %6d" % r["A"])
    print("      of the DOCUMENTED set, ENTRY-ONLY         : %6d" % r["entry_only"])
    print("          of those, ALREADY declared B/C      : %6d   <- counted as explained above"
          % r["entry_only_declared"])
    print("          genuinely undeclared entry-only     : %6d"
          % (r["entry_only"] - r["entry_only_declared"]))
    print()
    print("  An entry-only citation is a mention -- but HALF of them are bodies a declared")
    print("  family already explains as a class, so they are inside A+B+C above and are not")
    print("  an outstanding gap. Read the A figure carefully too: interior")
    print("  citation is a PROXY for explanation, not explanation itself. A page can explain a")
    print("  six-instruction function perfectly while citing only its entry, and that function")
    print("  scores 0 here. A is a STRICTER proxy than engine_explained, not a true count, and")
    print("  the honest reading of the gap is that the citation dimension is dominated by")
    print("  mentions -- not that the database is %.1f%% finished." % pct)
    print()
    print("  families accepted: %d   refused: %d" % (r["families_accepted"], r["families_refused"]))
    for who, letter, n in r["accepted"]:
        print("      %-6s %-60s %5d" % (letter, who[:60], n))
    for who, why in r["refusals"]:
        print("      REFUSED %-52s %s" % (who[:52], why))
    if not r["families_accepted"] and not r["families_refused"]:
        print("      No document declares `function_families:` yet. The surface exists and is")
        print("      empty; that is an honest zero, and populating it is evidence work, not a")
        print("      tooling change. FABLE has three enumerations ready (DF-1 46, DF-4 401,")
        print("      BK-6 4) and will declare them now that the key and format are fixed.")
    print()
    print("  NOT weighted into the headline - A/B/C/D is a separate dimension, and whether it")
    print("  should be weighted is the three-identity decision EC-7 names.")
    print("  (engine_explained IS no longer the old citation count: since 2026-09-14 the scorer")
    print("  applies SWE2-AUDIT-SPEC's adjudicated rule, and this gate shares its ladder test.)")


# --------------------------------------------------------------------------- self-test
FIXTURE_FN = "entry\tname\tbody_bytes\n00120000\ta\t16\n00120010\tb\t16\n00120020\tc\t16\n"


def self_test(tmp):
    """Every refusal reason, driven. A validator nobody tried to break is not a validator."""
    os.makedirs(tmp, exist_ok=True)
    fn = os.path.join(tmp, "functions.tsv")
    io.open(fn, "w", encoding="utf-8", newline="\n").write(FIXTURE_FN)
    sizes = load_functions(fn)
    assert sizes == {0x120000: 16, 0x120010: 16, 0x120020: 16}, sizes

    def doc(name, fam, members=None, status="DOCUMENTED", body=""):
        p = os.path.join(tmp, name + ".md")
        fm = "---\nstatus: %s\n" % status
        if fam:
            fm += "function_families:\n" + "".join('  - "%s"\n' % r for r in fam)
        fm += "---\n" + body
        io.open(p, "w", encoding="utf-8", newline="\n").write(fm)
        if members is not None:
            io.open(os.path.join(tmp, name + ".tsv"), "w", encoding="utf-8",
                    newline="\n").write("".join("%08X\n" % m for m in members))
        return p

    def run(paths):
        return evaluate(tmp, sizes, paths)

    ok = 0
    # 1. a clean B family
    p = doc("good", ["fam | B | good.tsv | 2 | ignorance of this family cannot block reproduction"],
            [0x120010, 0x120020])
    r = run([p])
    assert r["B"] == 2 and r["families_refused"] == 0, r
    ok += 1
    # 2. zero-case
    p = doc("zero", ["fam | B | zero.tsv | 0 | a note"], [])
    r = run([p])
    assert r["families_accepted"] == 0 and "zero-case" in r["refusals"][0][1], r
    ok += 1
    # 2b. the duplicate-member pair: a UNIQUE two-entry file is accepted with cardinality 2,
    #     and the same entry twice is refused rather than certifying a population of 2.
    #     ASTRA-CONTRA-OPUS-EC7-DUPLICATE-MEMBER.  The positive control comes first, because a
    #     refusal test alone cannot tell a working rule from one that refuses everything.
    p = doc("uniqpair", ["fam | B | uniqpair.tsv | 2 | a note"], [0x120010, 0x120020])
    r = run([p])
    assert r["B"] == 2 and r["families_refused"] == 0 and r["accepted"][0][2] == 2, r
    ok += 1
    p = doc("dup", ["fam | B | dup.tsv | 2 | a note"], [0x120010, 0x120010])
    r = run([p])
    assert r["families_accepted"] == 0 and "repeats 1 function" in r["refusals"][0][1], r
    assert r["B"] == 0 and r["frontier"] == 3, r
    ok += 1
    # 3. count mismatch
    p = doc("mismatch", ["fam | B | mismatch.tsv | 3 | a note"], [0x120010])
    r = run([p])
    assert "declared 3" in r["refusals"][0][1], r
    ok += 1
    # 4. no note
    p = doc("nonote", ["fam | C | nonote.tsv | 1 |"], [0x120010])
    r = run([p])
    assert "without a note" in r["refusals"][0][1], r
    ok += 1
    # 5. bad letter -- A may not be declared
    p = doc("bada", ["fam | A | bada.tsv | 1 | a note"], [0x120010])
    r = run([p])
    assert "is not B, C or D" in r["refusals"][0][1], r
    ok += 1
    # 6. a member that is not a function entry
    p = doc("ghost", ["fam | B | ghost.tsv | 1 | a note"], [0x999999])
    r = run([p])
    assert "not function entries" in r["refusals"][0][1], r
    ok += 1
    # 7. two families claiming one function
    p1 = doc("one", ["f1 | B | one.tsv | 1 | a note"], [0x120010])
    p2 = doc("two", ["f2 | C | two.tsv | 1 | a note"], [0x120010])
    r = run([p1, p2])
    assert r["families_accepted"] == 1 and "already declared" in r["refusals"][0][1], r
    ok += 1
    # 8. declared AND measured as A -- interior citation wins, declaration is refused
    p = doc("clash", ["f | B | clash.tsv | 1 | a note"], [0x120010],
            body="the body at `00120014` is interior to it")
    r = run([p])
    assert r["A"] == 1 and "already measured as A" in r["refusals"][0][1], r
    ok += 1
    # 9. an ENTRY-only citation is NOT A, and D is never explained
    p = doc("entryonly", None, None, body="see `00120010` for the entry")
    r = run([p])
    assert r["A"] == 0 and r["entry_only"] == 1, r
    ok += 1
    p = doc("dee", ["f | D | dee.tsv | 1 | reason; resume when x"], [0x120010])
    r = run([p])
    assert r["D"] == 1 and r["explained"] == 0 and r["frontier"] == 2, r
    ok += 1
    # 10. a citation from a non-DOCUMENTED page is not A
    p = doc("partial", None, None, status="PARTIAL", body="`00120014`")
    r = run([p])
    assert r["A"] == 0, r
    ok += 1
    print("self-test: %d case(s) passed, including every refusal reason" % ok)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=None)
    ap.add_argument("--functions", default=None)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        import tempfile
        return self_test(os.path.join(tempfile.gettempdir(), "gfz_disp_selftest"))
    db = a.db or DEFAULT_DB
    sizes = load_functions(a.functions)
    r = evaluate(db, sizes)
    if a.json:
        print(json.dumps({k: v for k, v in r.items() if k not in ("refusals", "accepted")}))
    else:
        report(r, a.quiet)
    return 1 if r["families_refused"] else 0


if __name__ == "__main__":
    sys.exit(main())
