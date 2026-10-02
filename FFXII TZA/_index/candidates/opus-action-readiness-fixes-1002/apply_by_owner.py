"""apply_by_owner.py OWNER [--apply] - run apply_07action.py's edits for one owner's pages only (OPUS, 2026-10-02).

FABLE is working again (user, 2026-10-02), so OPUS applies only the edits on OPUS-led and shared pages. The edits on
pages another identity leads go to that identity as requests; each can run this script with its own name. OWNER is one
of OPUS, FABLE, SWE2-EC7, SWE2-CONTRACT, SWE2-FRONTIER (the overlay-carrier page applying-a-result-to-a-target.md).
Page ownership: the identity with most commits on the page (git log --format=%s, 2026-10-02; unprefixed subjects are
shared and not counted; SWE2-EC7-NN counted apart from SWE2-EC7, as for the save pages). Two ties, broken by the most
recent commit of the tied identities: battle-command-availability-and-reason-codes.md FABLE 3 / SWE2-EC7 3 (FABLE
2026-09-30 after SWE2-EC7 2026-09-25) -> FABLE; how-a-combo-continues-and-what-it-blocks.md OPUS 3 / FABLE 3 (OPUS
e54b8e670 after FABLE 797b72780, both 2026-09-30) -> OPUS.
OPUS: CONTRACT-commit-action.md OPUS 6 / FABLE 1; CONTRACT-battle-target-buffer.md OPUS 7; applying-a-result-to-a-target.md
OPUS 2 / SWE2-FRONTIER 1 / FRONTIER 1 / SWE2-AUDIT-SPEC 1; how-a-combo-continues-and-what-it-blocks.md (tie, above).
FABLE: README.md 3; the-moment-an-action-is-committed.md 3 / OPUS 2; CONTRACT-the-moment-an-action-is-committed.md 2 /
OPUS 1; native-command-seam.md 3 / OPUS 1; CONTRACT-native-command-seam.md 5 / OPUS 1; battle-action-handler-table.md
3 / OPUS 1; CONTRACT-battle-action-handler-table.md 3 / OPUS 1; CONTRACT-combo-continuation.md 4 / OPUS 1;
the-action-definition-row.md 9 / OPUS 6; how-an-action-gathers-its-targets.md 2 / OPUS 1; how-close-a-unit-must-stand-
to-act.md 2 / OPUS 1; the-result-record-field-map.md 4 / OPUS 2; the availability page (tie, above).
SWE2-EC7: the-post-result-events-and-the-battle-message-table.md SWE2-EC7 8 / FRONTIER 4 / FABLE 2 / OPUS 2.
(CONTRACT-apply-result-to-target.md is SWE2-FRONTIER's, 2 / FABLE 1, and carries no edit.)
LINE_OWNERS (git blame on every edited line of the OPUS-led pages): the target-buffer contract's outcome-word lines
("knockback / parry / combo-continues ... mode-2 resource-reaction chance rolled") were last written by
630ef9be5 "SWE2-CONTRACT: six parity-map drifts closed + bit-11 outcome-word ...", so that edit goes to SWE2-CONTRACT.
Every other edited line on the OPUS-led pages was last written by an OPUS or an unprefixed (shared) commit.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import apply_07action as base  # noqa: E402

F = "07-Combat-Action/"
OWNERS = {
    "FABLE": {
        F + "README.md",
        F + "the-moment-an-action-is-committed.md",
        F + "CONTRACT-the-moment-an-action-is-committed.md",
        F + "Command-And-Action-Seam/native-command-seam.md",
        F + "CONTRACT-native-command-seam.md",
        F + "Action-Dispatch/battle-action-handler-table.md",
        F + "CONTRACT-battle-action-handler-table.md",
        F + "CONTRACT-combo-continuation.md",
        F + "Action-Availability/battle-command-availability-and-reason-codes.md",
        F + "Action-Definition-Row/the-action-definition-row.md",
        F + "how-an-action-gathers-its-targets.md",
        F + "how-close-a-unit-must-stand-to-act.md",
        F + "Result-Record/the-result-record-field-map.md",
    },
    "SWE2-EC7": {
        F + "Post-Result-Events/the-post-result-events-and-the-battle-message-table.md",
    },
    # OPUS-led by commits, but an overlay carrier (scope_guard census, 2026-10-02): only SWE2-FRONTIER publishes it.
    "SWE2-FRONTIER": {
        F + "applying-a-result-to-a-target.md",
    },
}
LINE_OWNERS = {"SWE2-CONTRACT": ("   > knockback / parry / combo-continues",)}


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
