"""apply_by_owner.py OWNER [--apply] - run apply_00engine_b.py's edits for one owner's pages only (OPUS, 2026-10-02).

FABLE is working again (user, 2026-10-02), so OPUS applies only the edits on OPUS-led and shared pages. The edits on
pages another identity leads, and on lines another identity last wrote, go to that identity as requests; each can run
this script with its own name. OWNER is one of OPUS, OPUS-HELD, FABLE, FRONTIER, SWE2-FRONTIER, SWE2-EC7,
SWE2-CONTRACT.
Page ownership: the identity with most commits on the page (git log --format=%s, 2026-10-02). Unprefixed subjects are
shared and counted as OPUS; SWE2-EC7-NN counts as SWE2-EC7 and SWE2CONTRACT-* as SWE2-CONTRACT; FRONTIER and
SWE2-FRONTIER are separate identities; a tie including OPUS stays OPUS.
OPUS: README.md 4 shared / FABLE 3; the-ee-and-vu0-register-bank.md 13 / FABLE 6; the-workbench-has-a-save-and-
restore-and-nine-functions-use-it.md 1 + 12 / SWE2-CONTRACT 2; the-shared-transform-workbench.md 3 + 11 / SWE2-EC7 14
(tie, stays OPUS); CONTRACT-transform-workbench-save-restore.md 2 + 6 / SWE2-CONTRACT 4; CONTRACT-transform-
primitives.md 4 + 10 / SWE2-CONTRACT 4; rtti-vtable-object-model.md 1 + 13 / SWE2-EC7 9; CONTRACT-developer-tuning-
console.md 5 + 5 / FABLE 1; the-282-command-parameter-console.md 4 + 16 / SWE2-CONTRACT 3; what-the-console-tunes.md
8 + 14 / SWE2-CONTRACT 7; the-second-console-table.md 3 + 6 / SWE2-CONTRACT 4; ARM-CATALOGUE-WORK-DIVISION.md 6 /
SWE2-EC7 4; arm-catalogue slices A 13 / FABLE 5, B 13 / SWE2-EC7 4, C 14 / FABLE 3, D 17 / FABLE 3, E 7 / SWE2-EC7 5,
F 16 / SWE2-EC7 3, G 14 / SWE2-EC7 3, I 11 / SWE2-CONTRACT 1; force-fight-mode.md 17 / SWE2-EC7 7;
generated-float-table-builders.md 15 / SWE2-CONTRACT 5; what-the-engine-fixes-at-boot.md 24 / SWE2-CONTRACT 6;
CONTRACT-boot-fixups.md 20 / SWE2-EC7 9; CONTRACT-world-simulation-tick.md 6 / FABLE 3; one-word-decides-which-
fifteen-subsystems-tick.md 21 / FRONTIER 4; CONTRACT-per-frame-update-gate.md 59 / SWE2-EC7 44; battle-runtime-mode-
ladder.md 45 / SWE2-EC7 34; CONTRACT-battle-runtime-mode.md 18 / SWE2-EC7 5; the-formatted-log-call-and-its-level-
gate.md 7 / SWE2-CONTRACT 4; derived-call-signatures.md 19 / FABLE 1; the-shared-neighbours-pass-22-keeps-finding.md
23 / SWE2-EC7 5.
SWE2-EC7: the-two-transform-primitives.md 50 / 66; cross-subsystem-accessor-hubs.md 29 / 32;
intentionally-ownerless-functions-and-shared-scratch.md 31 / 39; the-world-tick-and-the-field-frame.md 60 / 83.
FABLE: CONTRACT-shared-transform-workbench.md 1 / 2.
SWE2-CONTRACT: the-event-slot-panel-and-its-dead-feeder.md 3 / 8 (its part-A correction on the 001EC560 row, dirty
at drafting, was committed by SWE2-CONTRACT in 85718f321 before this was finished; no edit here touches that row).
No overlay carrier among these pages (scope_guard.py, 2026-10-02). derived-call-signatures.md is dirty with OPUS's own
"Interior citations" section (appended at its end); it stays OPUS and no OLD string here reaches that section.
Held: none. The open board tasks naming an edited page are READY, not ACTIVE: FABLE-REQ-EC7-TITLE-PACKET-CORRECTIONS-
1002 (SWE2-EC7, on the-two-transform-primitives.md, which SWE2-EC7 leads anyway) and OPUS-REQ-AUDITSPEC-OPUS-ARM-
CATALOGUE-SLICE-I-IDS-268-293-CLOUDINT (SWE2-AUDIT-SPEC, a review of OPUS's interior citations on the slice-I page).
The README board hits are basename collisions. Re-run the guard first.
Guard on the OPUS pages (2026-10-02, re-run at finish): BLOCKs are SWE2-CONTRACT's finished pass-22 sweep de4492e21,
its finished d0809ac13 (console tunes) and c40870e2d (log page), SWE2-AUDIT-SPEC's promotion sweep 058c93e21, the dirty
OPUS section on the ABI page and the README basename collisions; the rest WARN (sweeps 24-72 h, inbox mentions) or
CLEAR (the console contract). No census TSV is edited, and vtable-method-index.md is not touched (its 6,886 / 4,275 / follow-up slot
numbers are reported to SWE2-DATA / SWE2-EC7 instead).
LINE_OWNERS (git blame --porcelain on every edited line of the OPUS-led pages): SWE2-CONTRACT last wrote the
save-restore contract's §15a capacity sentence, its 022D8F0C paragraph and its lea-address census line (95b1f3a4c), and
the 282-command page's 01F82D20 line (3754d9b4d); FABLE the register-bank page's banner-string lines (2637d917f), the
README's register-bank status line (2637d917f), the console contract's run-time step paragraph (ad3ba074e), slice C's
UQ-11 answer (0f6eebd93), slice B's UQ-8 answer (8e7ea1e84), the boot contract's tail-bytes note (6cdd4e333), the
tick contract's unread-gates bullet (2a5eb4ff9) and the rtti page's glue "still open" line (0d808278a); FRONTIER the
rtti page's 00385F60 subtree line (b775a7ba4) and the workbench page's 0025A8E0 subtree row and note (891f0849f); SWE2-EC7 slice E's SWE2-EC7-126 ctor paragraph (e19990a66). Every other
edited line on the OPUS-led pages was last written by an OPUS or an unprefixed (shared) commit.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import apply_00engine_b as base  # noqa: E402

F = "00-Engine-Core-Runtime/"
OWNERS = {
    "SWE2-EC7": {
        F + "Shared-Transform-Workbench/the-two-transform-primitives.md",
        F + "Shared-State-Accessors/cross-subsystem-accessor-hubs.md",
        F + "Ownership-Boundary/intentionally-ownerless-functions-and-shared-scratch.md",
        F + "Battle-Frame/the-world-tick-and-the-field-frame.md",
    },
    "FABLE": {
        F + "CONTRACT-shared-transform-workbench.md",
    },
    "SWE2-CONTRACT": {
        F + "Developer-Tuning-Console/the-event-slot-panel-and-its-dead-feeder.md",
    },
    # No held OPUS page and no overlay carrier at drafting (see above); kept so every owner runs and reports.
    # Held 2026-10-02 (OPUS): the page carries OPUS's own uncommitted F-interior section; apply after that publishes.
    "OPUS-HELD": {"00-Engine-Core-Runtime/ABI-Recovery/derived-call-signatures.md"},
    "SWE2-FRONTIER": set(),
}
LINE_OWNERS = {
    "SWE2-CONTRACT": ("second Save overwrites the first frame in place (§10), a single save window",
                      "cell is borrowed scratch like every other row, and the wholesale-clear hazard",
                      "values array `lea`'d at `0036D954`",
                      "The hottest single address is `01F82D20`, nudged by **18** different commands (18 rows"),
    "FABLE": ("> **`\"PS2 Assembly emulation initilization completed! \"`**",
              "`00908D80` = `\"PS2 Assembly emulation initilization completed! \"`",
              "1.0 (4), **0.005 (4)**, 0.03 (3) and **0.005556 (2)**.",
              "All 36 are named, and in this build nothing",
              "- **So even the nine that the scene JSON sets per scene",
              "- **What they control in this build: nothing outside the console.**",
              "Whatever the shipped renderer uses for hair and",
              "  **PARTIAL, tier 1.** The workbench is the **register bank",
              "**What the tail bytes are *for* is still open**",
              "**those gates are unread** and this",
              "- **Still open:** whether Phyre's reflection glue"),
    "FRONTIER": ("`00385F60` (`BattleFormula_ResolveTargetResult`, ~144 B)",
                 "bumps the `022D9130` staging bank",
                 "`0025A8E0`'s `022D9130` cells are the same"),
    "SWE2-EC7": ("`005DC580` + `005DC430`\ninit the `+0xD0` member,",),
}


# Holds lifted 2026-10-02 (OPUS): these pages' holds are lifted; their held edits on other identities' lines go to them.
OWNERS["OPUS-HELD"] = set(OWNERS.get("OPUS-HELD", set())) - set(['00-Engine-Core-Runtime/ABI-Recovery/derived-call-signatures.md'])


def owner_of(e):
    for o, pages in OWNERS.items():
        if e[0] in pages:
            return o
    for o, prefixes in LINE_OWNERS.items():
        if e[1].startswith(prefixes):
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
