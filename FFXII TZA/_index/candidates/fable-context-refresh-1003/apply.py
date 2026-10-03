"""apply.py [--apply] - FABLE's part of the user's context refresh (FFXII_DB_RECONSTRUCTION_CONTEXT_REFRESH_PACKAGE_2026-10-02_v3
+ FFXII_PROJECT_IMPROVEMENT_ADDENDUM_2026-10-03): exact, anchored edits to the database README, TEAM.md's startup
section, PROGRAM-STATE.md's coordination header and DASHBOARD-MEANINGS.md (new section 6). Every anchor must occur
exactly once. Refuses a file with uncommitted changes. Keeps each file's line endings. Prints FAILS N last."""
import io, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
CH = "../../RECONSTRUCTION-CHARTER.md#0-project-lifecycle-fable-user-directive-2026-10-02"


def frag(name):
    return io.open(os.path.join(HERE, name), encoding="utf-8").read().rstrip("\n")


README = os.path.join(DB, "README.md")
TEAM = os.path.join(DB, "_index", "_inbox", "TEAM.md")
PS = os.path.join(DB, "_index", "PROGRAM-STATE.md")
DM = os.path.join(DB, "_index", "workflow", "DASHBOARD-MEANINGS.md")

EDITS = {
    README: [
        # lifecycle clarification right after the L1/L2/L3 authority paragraph
        ("revision is [`_index/GOAL-REVISION-2026-09-08.md`](_index/GOAL-REVISION-2026-09-08.md).",
         "revision is [`_index/GOAL-REVISION-2026-09-08.md`](_index/GOAL-REVISION-2026-09-08.md).\n\n" + frag("readme_lifecycle_short.txt")),
        # source-of-truth terminology
        ("**Source of truth:** the GFZ/GZF V121 reconstruction of `FFXII_TZA.exe`",
         "**Reference executable and provenance authority:** the GFZ/GZF V121 reconstruction of `FFXII_TZA.exe`"),
        ("Nothing in this database is allowed to be a guess. See",
         "**Canonical technical knowledge:** this database, reconciled under the evidence standard. The executable is what\n"
         "that knowledge is checked against; it is not a second truth system.\n\n"
         "Nothing in this database is allowed to be a guess. See"),
        # volatile team facts -> live authority
        ("**Concurrent researchers:** begin at the [team operating protocol](_index/_inbox/TEAM.md) (eleven fixed identities since 2026-09-13)\n"
         "and check [current claims](_index/_inbox/TEAM.json) before substantive work.",
         "**Concurrent researchers:** the live team, role and claim authority is the [team operating protocol](_index/_inbox/TEAM.md)\n"
         "plus [`TEAM.json`](_index/_inbox/TEAM.json). Read the roster there, not from this README, and check current claims before\n"
         "substantive work. Resume from your identity's **Resume state** block, never from an old handoff (TEAM.md, *Starting or\n"
         "resuming*)."),
        # current-state authority table after the Start-here table
        ("| [`_templates/SYSTEM.md`](_templates/SYSTEM.md) | The document template |",
         "| [`_templates/SYSTEM.md`](_templates/SYSTEM.md) | The document template |\n\n" + frag("readme_current_state.txt")),
        # residual-gate contradiction
        ("| **0** at the certified GN162 parent ~~30 (GN161)~~ — *see Status below; the figure is reached but the gate is not sealed* |",
         "| **0** at the certified GN162 parent ~~30 (GN161)~~ — the residual gate is **SEALED** (2026-09-16, independently "
         "re-certified; see Status below) *(corrected 2026-10-03, FABLE: this row still said \"not sealed\" after the Status "
         "row recorded the seal)* |"),
        # the two format folders the category tables omitted
        ("Category totals overlap by design",
         frag("readme_formats.txt") + "\n\nCategory totals overlap by design"),
        # lifecycle section + status pointers
        ("## Status\n", frag("readme_lifecycle_section.txt") + "\n\n---\n\n## Status\n"),
        ("| Engine *documented here* | see [`_index/COVERAGE.md`](_index/COVERAGE.md) |",
         "| Whole-database goal (L1+L2) | decided by `goal_gate.py`; read the current result in the generated [`PROGRESS.md`](PROGRESS.md) — not copied here |\n"
         "| Engine *documented here* | see the generated [`PROGRESS.md`](PROGRESS.md) and [`_index/COVERAGE.md`](_index/COVERAGE.md) (per-folder document counts, kept against disk by `check_coverage.py`) |"),
    ],
    TEAM: [
        ("a **primary reconstruction phase needs a separate user instruction**.",
         "a **primary reconstruction phase needs a separate user instruction**. *(2026-10-03: the full lifecycle after the database "
         "is now written once, in [`RECONSTRUCTION-CHARTER.md` §0](../../../../RECONSTRUCTION-CHARTER.md#0-project-lifecycle-fable-user-directive-2026-10-02), "
         "with a machine-readable twin [`PROJECT-LIFECYCLE.json`](../workflow/PROJECT-LIFECYCLE.json).)*"),
        ("## Exact starting instructions\n", frag("team_startup.txt") + "\n\n## Exact starting instructions\n"),
        ("1. **FABLE:** use ID FABLE; run the startup commands and required reading; inspect READY candidates",
         "*(HISTORICAL CHECKPOINT, 2026-09-13. The three package names below were the first claims of that week and are long "
         "finished. Do not resume from them; follow *Starting or resuming* above.)*\n\n"
         "1. **FABLE:** use ID FABLE; run the startup commands and required reading; inspect READY candidates"),
    ],
    PS: [
        ("Small reconstruction probes test database sufficiency; the main transition awaits\n"
         "the existing charter quality/readiness gate.",
         "Small reconstruction probes test database sufficiency; ~~the main transition awaits\n"
         "the existing charter quality/readiness gate~~ the main transition needs L1+L2 completion (`goal_gate.py`, including\n"
         "the thirty-pass terminal certification) **and then the user's explicit authorization** *(corrected 2026-10-03, FABLE:\n"
         "the readiness-gate endpoint was replaced on 2026-09-12, TEAM.md; lifecycle: RECONSTRUCTION-CHARTER.md §0)*."),
    ],
    DM: [
        ("A non-author (AUDIT-SPEC) reviews this file, because FABLE authored it.",
         "A non-author (AUDIT-SPEC) reviews this file, because FABLE authored it.\n\n" + frag("meanings_section6.txt")),
    ],
}

fails, out = 0, []
for p, edits in EDITS.items():
    if subprocess.run(["git", "diff", "--quiet", "--", p], cwd=HERE).returncode != 0:
        print("REFUSED: %s has uncommitted changes" % os.path.relpath(p, DB)); fails += 1; continue
    raw = io.open(p, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in raw else "\n"
    text = raw.replace("\r\n", "\n")
    done = 0
    for old, new in edits:
        if new in text:
            done += 1; continue
        n = text.count(old)
        if n != 1:
            print("MISS %s (%d): %r" % (os.path.relpath(p, DB), n, old[:70])); fails += 1; continue
        text = text.replace(old, new); done += 1
    out.append((p, text.replace("\n", nl), raw))
    print("%s: %d of %d edits ready" % (os.path.relpath(p, DB), done, len(edits)))
if fails == 0 and "--apply" in sys.argv:
    for p, t, raw in out:
        if t != raw:
            io.open(p, "w", encoding="utf-8", newline="").write(t); print("PATCHED %s" % os.path.relpath(p, DB))
elif fails == 0:
    print("WOULD PATCH %d files" % sum(1 for p, t, raw in out if t != raw))
print("FAILS %d" % fails)
