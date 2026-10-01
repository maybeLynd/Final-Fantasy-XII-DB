#!/usr/bin/env python3
"""readiness_rank.py - which subsystem is closest to being reconstructable, and why.

Charter §38 asks the program to **identify subsystems near reconstruction readiness** and to build a
**prioritized roadmap**. Both are still open, and the reason is `DJ-1`: the readiness ladder is
stated in the frontmatter of **6 of 221 documents**. The column that would answer this directly is
empty, so ranking has to come from evidence the database already holds.

**This is a proxy and it says so.** It measures the things that must be true before a subsystem can
be reconstructed, not reconstruction readiness itself:

    contract    a behavioural §4 contract exists                       - the strongest single signal
    types       entries in `_types/` for this category                 - a contract without types is prose
    attention   distinct functions cited by documents / functions owned - has anybody looked
    runtime     documents citing runtime evidence                      - the charter's readiness gate
    recon       a reconstruction and a differential harness exist       - already past the line

**Every column is a count with its denominator printed.** No composite score is emitted: a single
number would hide which of the five is missing, and *which one is missing* is the whole output.

A caution the tool enforces on itself
-------------------------------------
The owner->category map below is **hand-written and partial**. The ledger's owner names and the
database's category names are two independent vocabularies; where a category has no owner, the
`owned` denominator is blank and the attention ratio is **not computed** rather than divided by a
guess. `00-Engine-Core-Runtime` and `99-Unresolved-Residual` deliberately have no owner: they are
cross-cutting, and an attention ratio for them would be meaningless.
"""
import argparse
import io
import os
import sqlite3
import sys
import kit_paths as KP  # noqa: E402

ROOT = KP.ROOT
DBF = os.path.join(ROOT, "Database", "Tools", "work", "knowledge", "knowledge.sqlite")

# category -> the ledger owner that maps to it. Partial ON PURPOSE; see the module docstring.
OWNER = {
    "01-Script-VM-Native-Bridge": "Script_VM_Native_Bridge",
    "02-Resource-And-Asset-Pipeline": "Resource",
    "03-World-Area-Field": "WorldAreaField",
    "04-Actor-Entity": "ActorEntity",
    "05-Spawn-Encounter-Lifecycle": "Spawn_Encounter_Lifecycle",
    "06-Movement-And-Navigation": "Movement",
    "07-Combat-Action": "CombatAction",
    "08-Combat-Formula": "CombatFormula",
    "09-Combat-AI-And-Gambits": "CombatAI",
    "10-Status-Periodic-Terminal": "Status_Periodic_Terminal",
    "11-Party": "Party",
    "12-Items-Equipment-Shops-License": "Items_Equipment_Shops_License",
    "13-Rewards-Progression-Economy": "Rewards_Progression_Economy",
    "14-Story-Event-Quest-Hunt": "Story_Event_Quest_Hunt",
    "15-Input": "Input",
    "16-UI": "UI",
    "17-Presentation-Rendering": "Presentation",
    "18-Audio": "Audio",
    "19-Save-Load-Settings": "Save_Load_Settings",
    "20-Platform-Online-Achievements": "PlatformOnlineAchievements",
    "21-RNG-And-Determinism": "RNG_Random_Selection",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DBF)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    if not os.path.exists(a.db):
        sys.stderr.write("no index at %s - run `knowledge_db.py build`\n" % a.db)
        return 2
    import knowledge_db as _kd
    _status, _stale, _meta = _kd.freshness_report(a.db)
    if _status != "current":
        print("index %s (built %s, pin=%s) - figures below read a dated snapshot:"
              % (_status.upper(), _meta.get("built_at"),
                 (_meta.get("pinned_commit") or "worktree")[:12]))
        for _line in _stale[:10]:
            print("  STALE " + _line)
    conn = sqlite3.connect(a.db)
    q = conn.execute

    cats = [r[0] for r in q("SELECT DISTINCT category FROM documents "
                            "WHERE is_template = 0 AND category IS NOT NULL "
                            "ORDER BY category")]
    rows = []
    for c in cats:
        if not c or not c[0].isdigit():
            continue
        # Each signal is its OWN query. A first attempt joined documents to citations and summed
        # is_contract in the same statement, which multiplied every contract by that document's
        # citation count and reported 51 contracts in 16-UI. Counting two things across one join
        # counts neither.
        docs = q("SELECT COUNT(*) FROM documents WHERE category=? AND is_template=0",
                 (c,)).fetchone()[0]
        contracts = q("SELECT COUNT(*) FROM documents WHERE category=? AND is_contract=1",
                      (c,)).fetchone()[0]
        cited = q("SELECT COUNT(DISTINCT c.resolved_entry) FROM citations c "
                  "JOIN documents d ON d.path=c.path "
                  "WHERE d.category=? AND c.resolved_entry IS NOT NULL", (c,)).fetchone()[0]
        types = q("SELECT COUNT(*) FROM types WHERE category=?", (c,)).fetchone()[0]
        fields = q("SELECT COUNT(*) FROM fields WHERE type IN "
                   "(SELECT name FROM types WHERE category=?)", (c,)).fetchone()[0]
        runtime = q("SELECT COUNT(*) FROM documents WHERE category=? AND is_template=0 "
                    "AND runtime_markers > 0", (c,)).fetchone()[0]
        corrections = q("SELECT COUNT(*) FROM contradictions WHERE category=?", (c,)).fetchone()[0]
        owner = OWNER.get(c)
        owned = covered = None
        if owner:
            owned = q("SELECT COUNT(*) FROM functions WHERE owner=? AND is_generated=0",
                      (owner,)).fetchone()[0]
            # COVERAGE is the INTERSECTION - functions this owner owns that ANY document cites -
            # not "functions cited by this category's documents". The first version divided the
            # second by `owned` and produced 313 % for 14-Story-Event-Quest-Hunt, because a
            # category's documents freely cite functions another category owns. A ratio whose
            # numerator and denominator come from different populations is not a ratio.
            covered = q("SELECT COUNT(*) FROM functions f WHERE f.owner=? AND f.is_generated=0 "
                        "AND f.entry IN (SELECT resolved_entry FROM citations "
                        "                WHERE resolved_entry IS NOT NULL)",
                        (owner,)).fetchone()[0]
        rows.append((c, docs, contracts, cited, owned, covered, types, fields, runtime,
                     corrections))

    print("Charter §38: which subsystem is closest to reconstructable.")
    print("A PROXY. The readiness column would answer this directly and is stated in 6 of 221")
    print("documents (`DJ-1`), so these are the preconditions instead - counts, no composite score.")
    print()
    print("  category                          docs  contr  cited  owned   cov%  types fields  rt  corr")
    for c, docs, contracts, cited, owned, covered, types, fields, runtime, corr in rows:
        attn = ("%5.1f" % (100.0 * covered / owned)) if owned else "    -"
        print("  %-32s %5d %6d %6d %6s %s %6d %6d %3d %5d"
              % (c[:32], docs, contracts, cited, owned if owned else "-", attn, types, fields,
                 runtime, corr))
    print()
    print("  cited = distinct functions this category's documents cite, WHEREVER they are owned.")
    print("  cov%%  = functions this owner owns that ANY document cites, over functions owned.")
    print("          Different populations; only cov%% is a coverage ratio. Blank where no owner maps.")
    print()
    ranked = [r for r in rows if r[2] > 0]
    print("HAS A CONTRACT (%d of %d categories):" % (len(ranked), len(rows)))
    for c, docs, contracts, cited, owned, covered, types, fields, runtime, corr in ranked:
        print("  %-32s %d contract(s), %d type(s), %d runtime-cited document(s)"
              % (c[:32], contracts, types, runtime))
    print()
    nort = [r[0] for r in rows if r[8] == 0]        # index 8 is `runtime`; adding `covered`
    #                                                 shifted it, and index 7 is `fields`
    print("NO DOCUMENT CITES RUNTIME EVIDENCE in %d of %d categories:" % (len(nort), len(rows)))
    print("  " + ", ".join(x[:26] for x in nort[:12]))
    if len(nort) > 12:
        print("  ... and %d more" % (len(nort) - 12))
    # THE LINE ABOVE IS ABOUT CATEGORY PAGES AND WAS BEING READ AS "no runtime evidence exists".
    # Every experiment record is stored with is_template = 1 - one flag doing two jobs - so the
    # runtime query drops all of them, and they are the only documents in this database that ARE
    # runtime evidence. Reported here rather than folded into the per-category counts, because an
    # experiment record carries no category and inventing one for it would be worse.
    exp = q("SELECT COUNT(*), SUM(runtime_markers > 0) FROM documents "
            "WHERE is_template = 1 AND path LIKE '_experiments/%'").fetchone()
    print()
    print("  EXPERIMENT RECORDS, which the line above does not count: %d indexed, %d carrying a"
          % (exp[0] or 0, exp[1] or 0))
    print("  runtime marker. They hold the project's runtime evidence and are excluded from every")
    print("  is_template = 0 query, including that one.")
    print()
    print("**The charter gates reconstruction readiness on runtime validation.** On that gate the")
    print("ranking above is advisory only: no category passes it.")

    if a.out:
        with io.open(a.out, "w", encoding="utf-8", newline="\n") as f:
            f.write("category\tdocs\tcontracts\tcited_functions\towned_functions\t"
                    "owned_and_cited\tcoverage_pct\ttypes\tfields\truntime_docs\tcorrections\n")
            for c, docs, contracts, cited, owned, covered, types, fields, runtime, corr in rows:
                f.write("%s\t%d\t%d\t%d\t%s\t%s\t%s\t%d\t%d\t%d\t%d\n"
                        % (c, docs, contracts, cited, owned if owned else "",
                           covered if covered is not None else "",
                           ("%.1f" % (100.0 * covered / owned)) if owned else "",
                           types, fields, runtime, corr))
        print("\nwrote %s" % a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
