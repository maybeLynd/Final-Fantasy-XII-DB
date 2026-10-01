#!/usr/bin/env python3
"""charter_grade_audit.py - audit the database against the charter's own quality standard.

Charter §38 lists *"audit the database against the reconstruction-grade requirements (§3)"* as a
first action. It has been open since the program began, and every readiness statement so far has
been by proxy - contracts held, types declared, runtime evidence counted. **Nobody has checked the
database against the definition of the quality it is trying to reach.**

Two things are measured, and a third is deliberately refused.

1. The §3 dimensions
-------------------
§3 names seven dimensions - Identity, Interface, Data, Behaviour, Relationships, Runtime,
Validation. For each this tool states **the instrument, the population, the count and the
denominator**, or reports the dimension **UNMEASURABLE** and says what record type would have to
exist first. A dimension nobody can query is the finding; inventing a keyword proxy for it would
repeat `DR-1`, where a marker list counted documents that were *denying* runtime evidence.

2. Ladder monotonicity - "rung debt"
------------------------------------
The readiness ladder is written as one ordered sequence:

    DISCOVERED -> CLASSIFIED -> SEMANTICALLY IDENTIFIED -> SIGNATURE RESOLVED -> TYPE RESOLVED
    -> DEPENDENCIES RESOLVED -> BEHAVIORALLY UNDERSTOOD -> RUNTIME VALIDATED -> CONTRACT READY
    -> RECONSTRUCTION READY -> IMPLEMENTED -> DIFFERENTIAL TESTED -> PARITY CERTIFIED

An ordered ladder means a document at rung N asserts rungs 1..N. **Six of the thirteen rungs have a
mechanically checkable criterion**; this tool evaluates those six for every rung *below* each
document's stated rung and reports the ones that are unmet. The other seven are reported
`not-evaluable` - never as passing.

**This tool does not demote anybody.** Rung debt is a fact about the label and the evidence; whether
the fix is to relabel documents or to say in the charter that the ladder is not ordinal is a
decision, and a decision is not a measurement.

3. What it refuses to score
---------------------------
§26 and §27 are lists of questions a human must answer by reading. **No mechanical proxy for "can a
researcher answer what its invariants are" is honest**, so this tool does not emit one. It prints
the question list so a hand-audit has something to be scored against, and the hand-audit lives in
`_index/RECONSTRUCTION-GRADE-AUDIT.md` with its subject named.

Usage
-----
    python charter_grade_audit.py
    python charter_grade_audit.py --out <path.tsv>
"""
import argparse
import io
import os
import re
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit_paths as KP  # noqa: E402
# `check_consistency` is deliberately NOT imported here any more. It owns the name patterns and
# `knowledge_db.py` imports them to build `doc_names`; this tool reads that table. One traversal,
# one definition, one place to fix. `DU-1`.

ROOT = KP.ROOT
DB = os.path.join(ROOT, "Database", "FFXII TZA")
DBF = os.path.join(ROOT, "Database", "Tools", "work", "knowledge", "knowledge.sqlite")
RECON = os.path.join(ROOT, "Reconstruction")

LADDER = ["DISCOVERED", "CLASSIFIED", "SEMANTICALLY IDENTIFIED", "SIGNATURE RESOLVED",
          "TYPE RESOLVED", "DEPENDENCIES RESOLVED", "BEHAVIORALLY UNDERSTOOD",
          "RUNTIME VALIDATED", "CONTRACT READY", "RECONSTRUCTION READY", "IMPLEMENTED",
          "DIFFERENTIAL TESTED", "PARITY CERTIFIED"]

# Charter §27, with the compound clauses split. The charter writes "how is it initialized,
# updated, destroyed" and "what state does it read and write" as single clauses; they are three
# and two distinct questions and are counted as such, which is why this list is 21 and a casual
# count of the sentence gives 18.
GATE27 = [
    "what is this system", "what does it do", "what owns it", "what does it own",
    "how is it initialized", "how is it updated", "how is it destroyed",
    "what types does it use", "what state does it read", "what state does it write",
    "what calls it", "what does it call", "what state machines and events exist",
    "what scripts, resources and RNG affect it", "what are its invariants",
    "what side effects occur", "what can fail", "how does it interact with other systems",
    "how can we observe and test it", "what is still unknown",
    "what evidence supports what we believe",
]


EXP_ID = re.compile(r"EXP-([0-9]{3})")


def experiment_status():
    """id -> status word, from _experiments/*.md frontmatter.

    The rung below asks whether a document is backed by runtime evidence. The only machine-readable
    link between a document and a capture is the EXP id it cites, so that is the instrument, and it
    is a PROXY twice over: a citation is not a demonstration that the capture covers the document's
    claims, and an uncited capture is invisible here. Both directions are reported.
    """
    out = {}
    d = os.path.join(DB, "_experiments")
    if not os.path.isdir(d):
        return out
    for name in sorted(os.listdir(d)):
        if not name.endswith(".md"):
            continue
        head = io.open(os.path.join(d, name), encoding="utf-8", errors="replace").read(2000)
        m = EXP_ID.search(name) or EXP_ID.search(head)
        st = re.search(r"(?m)^status:\s*(\S+)", head)
        if m and st:
            out[m.group(1)] = st.group(1).strip().upper().rstrip(":-—")
    return out


def cited_experiments(path):
    full = os.path.join(DB, path.replace("/", os.sep))
    try:
        body = io.open(full, encoding="utf-8", errors="replace").read()
    except OSError:
        return set()
    return set(EXP_ID.findall(body))


def q1(conn, sql, args=()):
    return conn.execute(sql, args).fetchone()[0]


def prose_named(conn):
    """(upper, lower) count of cited function entries a document gives a name to.

    **This reads the index, not the corpus.** The first version of this tool re-scanned every
    document with `check_consistency`'s patterns - a second traversal of the same files by the same
    rules, which is the shape of every drift this project has paid for. `knowledge_db.py` now
    carries a `doc_names` table built by importing those same patterns, so there is one traversal
    and this is a caller. `DU-1`.

    **Two numbers, because the honest answer is a range.** `NAME_PATTERNS` was written for
    disagreement detection - two different names for one address - where a loose match is harmless
    because it fires only on a conflict. As a census the looseness shows: ``ADDR` | heaviest``
    matches, and so does ``ADDR` | PArray``, and only one is noise. The identifier-shaped count is
    the defensible lower bound; the raw count is the upper. Neither is narrowed further, because
    the narrowing rule would itself be a guess.
    """
    upper = q1(conn, "SELECT COUNT(DISTINCT resolved_entry) FROM doc_names "
                     "WHERE is_generated_index = 0 AND is_entry = 1 AND resolved_entry IN "
                     "(SELECT resolved_entry FROM citations WHERE resolved_entry IS NOT NULL)")
    lower = q1(conn, "SELECT COUNT(DISTINCT resolved_entry) FROM doc_names "
                     "WHERE is_generated_index = 0 AND is_entry = 1 AND resolved_entry IN "
                     "(SELECT resolved_entry FROM citations WHERE resolved_entry IS NOT NULL) "
                     "AND (instr(name,'_') > 0 OR name GLOB '*[a-z][A-Z]*' "
                     "     OR instr(name,':') > 0 OR instr(name,'.') > 0)")
    return upper, lower


def recon_units():
    """(implemented, differential-tested) subsystem stems from the reconstruction tree."""
    impl, diff = set(), set()
    g = os.path.join(RECON, "Game")
    if os.path.isdir(g):
        for root, _d, files in os.walk(g):
            for f in files:
                if f.endswith(".c"):
                    impl.add(os.path.splitext(f)[0])
    t = os.path.join(RECON, "Tests", "Differential")
    if os.path.isdir(t):
        for f in os.listdir(t):
            m = re.match(r"^diff_(.+)\.py$", f)
            if m:
                diff.add(m.group(1))
    return impl, diff


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DBF)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    if not os.path.exists(a.db):
        sys.stderr.write("no index at %s - run `knowledge_db.py build`\n" % a.db)
        return 2
    # The index is a CACHE and nothing here used to say how old it was. On 2026-09-13 OPUS
    # refreshed RECONSTRUCTION-GRADE-AUDIT from a two-day-old build and published it as the
    # figures "its own instrument says" - Behaviour claims read 227 when the tree held 706.
    # A timestamp cannot say that, so the check is the mirror's own recorded provenance:
    # knowledge_db.freshness_report recomputes the dependency fingerprints and names the
    # moved inputs. Every number below is only as fresh as this line.
    import knowledge_db as _kd
    _status, _stale, _meta = _kd.freshness_report(a.db)
    print("index %s (built %s, pin=%s)  (%s)" % (
        _status.upper(), _meta.get("built_at"),
        (_meta.get("pinned_commit") or "worktree")[:12], a.db))
    for _line in _stale[:15]:
        print("  STALE " + _line)
    if _status != "current":
        print("  rebuild with `knowledge_db.py build` before quoting anything below.")
    print()
    conn = sqlite3.connect(a.db)
    impl, diff = recon_units()

    docs = q1(conn, "SELECT COUNT(*) FROM documents WHERE is_template=0")
    cited = q1(conn, "SELECT COUNT(DISTINCT resolved_entry) FROM citations "
                     "WHERE resolved_entry IS NOT NULL")

    print("CHARTER §3 - RECONSTRUCTION-GRADE QUALITY STANDARD")
    print("Population for the per-function rows: the %d distinct function entries any document"
          % cited)
    print("cites. That is this database's own definition of \"important\" - it is what anybody")
    print("bothered to write about - and it is a PROXY, stated as one.")
    print()
    print("  dimension       measurable  value                                    instrument")
    print("  " + "-" * 96)

    rows = []

    def emit(dim, ok, value, instrument):
        rows.append((dim, "yes" if ok else "NO", value, instrument))
        print("  %-15s %-11s %-40s %s" % (dim, "yes" if ok else "**NO**", value, instrument))

    # substr, not LIKE. A first version wrote `NOT LIKE 'FUN[_]%' ESCAPE '['`, which asks for a
    # literal `]` and matched every row - the dimension reported 7376/7376 named, i.e. that every
    # cited function has a semantic name, which is false by two orders of magnitude. The tool's own
    # implausible 100 % is what exposed it.
    named = q1(conn, "SELECT COUNT(*) FROM functions WHERE entry IN "
                     "(SELECT resolved_entry FROM citations) AND substr(name,1,4) <> 'FUN_'")
    owned = q1(conn, "SELECT COUNT(*) FROM functions WHERE entry IN "
                     "(SELECT resolved_entry FROM citations) AND owner IS NOT NULL AND owner<>''")
    hi, lo = prose_named(conn)
    emit("Identity", True,
         "%d-%d/%d named in PROSE; %d in the ledger" % (lo, hi, cited, named),
         "knowledge_db doc_names (a RANGE - see prose_named) vs functions.tsv")
    emit("Identity/owner", True, "%d/%d owned" % (owned, cited),
         "functions.tsv owner, joined to citations")

    contracts = q1(conn, "SELECT COUNT(*) FROM documents WHERE is_contract=1 AND is_template=0")
    emit("Interface", True, "%d/%d documents declare signatures" % (contracts, docs),
         "contract §2 is the only parsable signature record")

    types = q1(conn, "SELECT COUNT(*) FROM types")
    fields = q1(conn, "SELECT COUNT(*) FROM fields")
    game = q1(conn, "SELECT COUNT(*) FROM types WHERE category IS NOT NULL AND category<>'' "
                    "AND category NOT LIKE '22-%'")
    emit("Data", True, "%d types / %d fields; %d GAME types" % (types, fields, game),
         "_types/ store, validated by types_index.py")

    # Behaviour was reported UNMEASURABLE when this tool was written, and the reason given was
    # "the schema has nowhere to put preconditions, postconditions, invariants, state transitions
    # or failure paths outside contract prose". That is now false: `knowledge_db.py` indexes the
    # contracts' own sections, and the five that carry behaviour are sections 4, 5, 7, 10 and 12.
    # **The dimension did not become well-covered -- it became ASKABLE**, and the number it returns
    # is small on purpose.
    beh = q1(conn, "SELECT COUNT(DISTINCT path) FROM contract_sections WHERE num IN (4,5,7,10,12) "
                   "AND chars > 200")
    claims = q1(conn, "SELECT COUNT(*) FROM contract_claims")
    unk = q1(conn, "SELECT COUNT(*) FROM contract_claims WHERE upper(confidence) LIKE '%UNKNOWN%'")
    emit("Behaviour", True,
         "%d/%d documents; %d claims, %d UNKNOWN" % (beh, docs, claims, unk),
         "knowledge_db contract_sections 4/5/7/10/12 + contract_claims")


    emit("Relationships", True, "%d/%d have graph callers+callees" % (cited, cited),
         "edges.tsv with caller_is_eh filtered - true by construction")

    rt = q1(conn, "SELECT COUNT(*) FROM documents WHERE is_template=0 AND readiness LIKE "
                  "'%RUNTIME VALIDATED%'")
    # Two different questions, and reporting only the first made the dimension look static while
    # captures accumulated. The frontmatter count says how many documents CLAIM the rung; the
    # citation count says how many are LINKED to a validated capture. They are not the same set.
    exps = experiment_status()
    val = {k for k, v in exps.items() if v.startswith("VALIDATED")}
    linked = [p for (p,) in conn.execute(
        "SELECT path FROM documents WHERE is_template=0").fetchall()
        if cited_experiments(p) & val]
    emit("Runtime", True,
         "%d/%d claim the rung; %d linked to a VALIDATED experiment (%d of %d validated)"
         % (rt, docs, len(linked), len(val), len(exps)),
         "readiness frontmatter, and EXP citations resolved against _experiments/ status")
    # Report the vocabulary, because the rung above is only as good as the word it keys on.
    # `VALIDATED` is required deliberately - it is the only status that ASSERTS the evidence
    # stands - but it is not the only status a validated capture has worn, so this number is a
    # FLOOR. Some RUN and COMPLETE experiments carry real validation in their status line
    # (EXP-008's "400 cases over the game's own data, 0 mismatches" is one), and none of them
    # count above. The fix is a status vocabulary, not a looser match here.
    import collections as _cc
    vocab = _cc.Counter(exps.values())
    print("     experiment status vocabulary: %s"
          % ", ".join("%s %d" % (w, n) for w, n in sorted(vocab.items())))
    print("     only VALIDATED counts above, so the linked figure is a FLOOR, not a census.")

    conf = q1(conn, "SELECT COUNT(*) FROM documents WHERE is_template=0 AND confidence IS NOT NULL "
                    "AND confidence<>''")
    emit("Validation", True, "%d/%d carry a confidence label" % (conf, docs),
         "frontmatter; DJ-1 is the labelling backlog")

    print()
    print("  ALL SEVEN DIMENSIONS ARE NOW ASKABLE. Behaviour was the last one that was not:")
    print("  the contracts index (`knowledge_db.py`, 2026-09-08) made sections 4, 5, 7, 10")
    print("  and 12 queryable, so the charter's preconditions, state, transitions, failure")
    print("  paths and reproduction formula have a record type at last.")
    print()
    # These two numbers were written as prose when there were seven contracts and no linked
    # capture, and they stayed literal while both moved. A readiness statement that cites this
    # tool would have carried the stale pair, so they are computed now.
    print("  ASKABLE IS NOT COVERED. Behaviour is answerable for the %d documents that are"
          % beh)
    print("  contracts and for no others, and Runtime is claimed by %d of %d and LINKED to a"
          % (rt, docs))
    print("  VALIDATED experiment by %d." % len(linked))

    print()
    print("LADDER MONOTONICITY - RUNG DEBT")
    print("A document at rung N asserts rungs 1..N. Six of 13 rungs have a checkable criterion;")
    print("the other seven are reported not-evaluable, never as passing.")
    print()

    labelled = conn.execute(
        "SELECT path, category, readiness FROM documents WHERE is_template=0 "
        "AND readiness IS NOT NULL AND readiness<>'' ORDER BY path").fetchall()
    print("  documents carrying a readiness label: %d of %d (%.1f %%) - DJ-1"
          % (len(labelled), docs, 100.0 * len(labelled) / docs))
    print()

    debts = []
    validated_exp = {k for k, v in experiment_status().items() if v.startswith("VALIDATED")}
    for path, cat, rung in labelled:
        if rung not in LADDER:
            continue
        n = LADDER.index(rung)
        unmet = []
        # LIMIT, recorded 2026-09-13 (OPUS): TYPE RESOLVED and SIGNATURE RESOLVED are tested
        # PER CATEGORY, not per document - "does this category have any types / any contract".
        # So a document in a category that deliberately declares neither (23-Third-Party-
        # Libraries, whose internals are EC-7 family C) inherits an unmet rung it cannot fix,
        # and a document in a rich category inherits a met rung it did nothing to earn. The
        # open question in this file's docstring - relabel, or declare the ladder non-ordinal -
        # is ANSWERED in KNOWLEDGE-SCHEMA 5a: not ordinal. All 16 rows this emitted on
        # 2026-09-13 dissolve under that ruling plus the two caveats above; see
        # RECONSTRUCTION-GRADE-AUDIT.md for the three-way split.
        for lower in LADDER[:n]:
            if lower == "TYPE RESOLVED":
                if not q1(conn, "SELECT COUNT(*) FROM types WHERE category=?", (cat,)):
                    unmet.append(lower)
            elif lower == "SIGNATURE RESOLVED":
                if not q1(conn, "SELECT COUNT(*) FROM documents WHERE category=? AND is_contract=1",
                          (cat,)):
                    unmet.append(lower)
            elif lower == "RUNTIME VALIDATED":
                # Was `unmet.append(lower)` unconditionally, with the comment "nothing in the
                # database reaches it". That was true when written and stopped being true as
                # captures landed, and because it was a constant the report could never say so -
                # every document owed the rung by construction, which is not a measurement.
                if not (cited_experiments(path) & validated_exp):
                    unmet.append(lower)
            elif lower == "IMPLEMENTED":
                if not impl:
                    unmet.append(lower)
            elif lower == "DIFFERENTIAL TESTED":
                if not diff:
                    unmet.append(lower)
            elif lower == "PARITY CERTIFIED":
                unmet.append(lower)
        if unmet:
            debts.append((path, rung, unmet))

    print("  %-64s %-20s %s" % ("document", "stated rung", "unmet rungs below it"))
    print("  " + "-" * 116)
    for path, rung, unmet in sorted(debts, key=lambda r: (-LADDER.index(r[1]), r[0])):
        short = path if len(path) <= 62 else path.split("/")[0] + "/.../" + path.split("/")[-1]
        print("  %-64s %-23s %s" % (short[:64], rung, ", ".join(unmet)))
    print()
    owe_rt = [d for d in debts if "RUNTIME VALIDATED" in d[2]]
    owe_pre = [d for d in debts if "RUNTIME VALIDATED" not in d[2]]
    print("  %d of %d labelled documents carry rung debt, in two distinct shapes:"
          % (len(debts), len(labelled)))
    print("    %d sit AT OR ABOVE `RUNTIME VALIDATED` and owe exactly that rung - they cite no"
          % len(owe_rt))
    print("       experiment whose status is VALIDATED, so they assert a rung nothing links them to.")
    # Do not assert the CAUSE in the summary. An earlier version said all of these owed both
    # `SIGNATURE RESOLVED` and `TYPE RESOLVED` "over a category with no types and no contract",
    # and it went stale the moment a category gained a type: three rows then owed one rung, not
    # two, while the sentence still claimed both. Print what is unmet, not why.
    import collections as _c
    shapes = _c.Counter(", ".join(d[2]) for d in owe_pre)
    print("    %d sit BELOW `RUNTIME VALIDATED` and owe a rung under them:" % len(owe_pre))
    for shape, n in shapes.most_common():
        print("       %2d owing %s" % (n, shape))
    print()
    print("  Those are different failures. The first is a missing LINK between a document and a")
    print("  capture - which is sometimes a missing capture and sometimes only a missing citation,")
    print("  and this tool cannot tell those apart. The second is work nobody has done.")

    print()
    print("CHARTER §27 - THE COMPLETION QUALITY GATE (%d questions)" % len(GATE27))
    print("Not scored here. No mechanical proxy for these is honest; they are answered by reading.")
    for i, qq in enumerate(GATE27, 1):
        print("  %2d. %s" % (i, qq))

    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("section\tkey\tmeasurable\tvalue\tinstrument\n")
            for dim, ok, value, instrument in rows:
                fh.write("charter-3\t%s\t%s\t%s\t%s\n" % (dim, ok, value, instrument))
            fh.write("#\n#\tladder rung debt\n")
            fh.write("section\tdocument\tstated_rung\tunmet_rungs_below\t\n")
            for path, rung, unmet in sorted(debts):
                fh.write("ladder\t%s\t%s\t%s\t\n" % (path, rung, ";".join(unmet)))
        print("\nwrote %s" % a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
