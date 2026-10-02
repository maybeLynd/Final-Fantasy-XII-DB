"""apply_by_owner.py OWNER [--apply] - run apply_00engine_a.py's edits for one owner's pages only (OPUS, 2026-10-02).

FABLE is working again (user, 2026-10-02), so OPUS applies only the edits on OPUS-led and shared pages. The edits on
pages another identity leads, and on lines another identity last wrote, go to that identity as requests; each can run
this script with its own name. OWNER is one of OPUS, OPUS-HELD, FABLE, FRONTIER, SWE2-FRONTIER, SWE2-EC7,
SWE2-CONTRACT.
Page ownership: the identity with most commits on the page (git log --format=%s, 2026-10-02). Unprefixed subjects are
shared and counted as OPUS; SWE2-EC7-NN counts as SWE2-EC7 and SWE2CONTRACT-* as SWE2-CONTRACT; FRONTIER and
SWE2-FRONTIER are separate identities; a tie including OPUS stays OPUS.
OPUS: force-fight-mode.md 15 shared + 1 / SWE2-EC7 7; what-the-console-tunes.md 14 + 7 / SWE2-CONTRACT 7;
what-the-engine-fixes-at-boot.md 18 + 5 / SWE2-CONTRACT 6; CONTRACT-boot-fixups.md 18 + 1 / SWE2-EC7 9;
generated-float-table-builders.md 11 + 3 / SWE2-CONTRACT 5, FABLE 5; CONTRACT-battle-runtime-mode.md 15 + 2 / SWE2-EC7 5;
one-word-decides-which-fifteen-subsystems-tick.md 19 + 1 / FRONTIER 4; CONTRACT-per-frame-update-gate.md 49 + 9 /
SWE2-EC7 44; CONTRACT-system-stop-registry.md 2 + 1 / FABLE 3 (tie, stays OPUS); battle-runtime-mode-ladder.md 42 + 2 /
SWE2-EC7 34; the-encoded-id-class-registry.md 19 + 5 / SWE2-CONTRACT 6; the-shared-neighbours-pass-22-keeps-finding.md
22 / SWE2-EC7 5; the-basis-column-helpers.md 5 + 1 / SWE2-EC7 4; rtti-vtable-object-model.md 13 + 1 / SWE2-EC7 9.
SWE2-EC7: the-world-tick-and-the-field-frame.md 83 / 56 + 4; game-application.md 83 / 44 + 3;
cross-subsystem-accessor-hubs.md 32 / 27 + 2.
SWE2-CONTRACT: the-event-slot-panel-and-its-dead-feeder.md 7 / 2 + 1.
Overlay carrier (scope_guard.py, 2026-10-02): the-encoded-id-space-and-the-query-record.md -> SWE2-FRONTIER.
the-formatted-log-call-and-its-level-gate.md is OPUS 3 + 3 shared / SWE2-CONTRACT 4. It was dirty at drafting (an
uncommitted SWE2-AUDIT-SEM review note), and SWE2-CONTRACT committed that note in c40870e2d before this was finished, so
it is OPUS-led and clean now. No 00-Engine page is dirty (git status, 2026-10-02; the one modified file in the folder is
the census TSV members/ee-register-census.tsv, which no edit touches). Re-check before --apply.
Held: none. The one open board task naming an OPUS page, OPUS-REQ-AUDITSPEC-OPUS-BATTLE-RUNTIME-MODE-LADDER-CLOUDINT-1001
(SWE2-AUDIT-SPEC, a review of OPUS's own interior citations on battle-runtime-mode-ladder.md), is READY with no agent,
not ACTIVE; OPUS-HELD is kept as an empty owner so the call shape matches the other folders. Re-run the guard first.
Guard on the OPUS pages (2026-10-02): BLOCKs on peer commits under 24 h are SWE2-CONTRACT's finished pass-22 sweep
de4492e21 and, on the log page, its finished c40870e2d and SWE2-AUDIT-SPEC's promotion sweep 058c93e21 only; the mode-ladder BLOCK is the READY request above; the rest WARN (sweeps 24-72 h, inbox mentions).
No census TSV is edited, and vtable-method-index.md is not touched.
LINE_OWNERS (git blame --porcelain on every edited line of the OPUS-led pages): SWE2-EC7 last wrote the rtti page's
00864210 paragraph (b41ae281f), the mode ladder's 00313550 paragraph (ce6080204), the mode contract's 002E73C0 paragraph
(cf08c3ec8) and the class registry's 00323890 paragraph (6ff80b8c3); FRONTIER the mode ladder's 0037D110/0037D120 thunk
table (b775a7ba4), its two 00303F00/00304060 subtree sections and the 00306760 extent line (3668e438d); SWE2-CONTRACT the
class registry's "Do not confuse with" 00309EC0 sentence (3754d9b4d). Every other edited line on the OPUS-led pages was
last written by an OPUS or an unprefixed (shared) commit.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import apply_00engine_a as base  # noqa: E402

F = "00-Engine-Core-Runtime/"
OWNERS = {
    "SWE2-EC7": {
        F + "Battle-Frame/the-world-tick-and-the-field-frame.md",
        F + "Application-Root/game-application.md",
        F + "Shared-State-Accessors/cross-subsystem-accessor-hubs.md",
    },
    "SWE2-CONTRACT": {
        F + "Developer-Tuning-Console/the-event-slot-panel-and-its-dead-feeder.md",
    },
    "SWE2-FRONTIER": {
        F + "the-encoded-id-space-and-the-query-record.md",
    },
    # No held OPUS page and no FABLE-led page at drafting (see above); kept so every owner runs and reports.
    "OPUS-HELD": set(),
    "FABLE": set(),
}
LINE_OWNERS = {
    "SWE2-EC7": ("`+0x18` - each allocation\nimmediately handed back to",
                 "of the `+0x5B04` dword on the `02EC4BA9` object",
                 "`0x740`-stride render-record array, and only when",
                 "indexes a 9-entry jump table at `002038E4`"),
    "FRONTIER": ("Two plain `jmp` thunks into the",
                 "| `0037D110` | `00307200` |",
                 "| `0037D120` | `00307240` |",
                 "`00303F00` (~27 B) — `qword[02EBF190]` base load",
                 "`001D50D0()` → `byte[rax+0xE1E] != 0` bool getter",
                 "`001D50D0()` then `byte[rax+0xE1E] != 0` bool getter",
                 "`00306760` `BattleAction_UpdateSpecialPresentationSequence` (293 B)"),
    "SWE2-CONTRACT": ("which routes by nibble to a record's mutate or query",),
}


def owner_of(e):
    for o, prefixes in LINE_OWNERS.items():
        if e[1].startswith(prefixes):
            return o
    for o, pages in OWNERS.items():
        if e[0] in pages:
            return o
    return "OPUS"


def main():
    owner = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "OPUS"
    if owner in ("OPUS", *OWNERS, *LINE_OWNERS):
        keep = [e for e in base.EDITS if owner_of(e) == owner]
    else:
        print("unknown owner", owner); print("FAILS 1"); return 1
    print("owner", owner, "edits", len(keep), "of", len(base.EDITS))
    base.EDITS = keep
    return base.main()


if __name__ == "__main__":
    sys.exit(main())
