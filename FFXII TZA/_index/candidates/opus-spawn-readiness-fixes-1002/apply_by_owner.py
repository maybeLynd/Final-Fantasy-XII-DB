"""apply_by_owner.py OWNER [--apply] - run apply_05spawn.py's edits for one owner's pages only (OPUS, 2026-10-02).

FABLE is working again (user, 2026-10-02), so OPUS applies only the edits on OPUS-led and shared pages. The edits on
pages another lane leads go to that lane as requests; each lane can run this script with its own name. OWNER is one
of OPUS, FABLE, FRONTIER, SWE2-EC7.
Page ownership: the identity with most commits on the page (git log --format=%s, 2026-10-02; unprefixed subjects are
shared and do not lead; SWE2-EC7-NN task subjects count as the SWE2-EC7 lane, SWE2-FRONTIER as FRONTIER):
spawn-placement-and-retirement.md FRONTIER 13 / OPUS 5 / FABLE 4; the-spawn-keep-entry-field-map.md FRONTIER 5 /
SWE2-EC7 2 / SWE2-STRUCT 1 / OPUS 1; why-the-enemies-you-killed-come-back.md FABLE 3 / OPUS 2 / FRONTIER 1;
when-a-group-is-wiped-and-when-it-comes-back.md FABLE 12 / SWE2-EC7 10 / OPUS 4 / FRONTIER 5;
spawn-placement-height-and-authored-tunables.md SWE2-EC7 4 / OPUS 3 / SWE2-DATA 1 / FRONTIER 1;
CONTRACT-group-completion-and-respawn.md OPUS 5 / FABLE 2 / FRONTIER 1; CONTRACT-spawn-placement.md OPUS 2 /
FABLE 1 / SWE2-EC7 1; README.md two unprefixed commits (shared, OPUS).
One line on the OPUS-led group contract is FRONTIER's (git blame: the "`00307140` (~97 B)" subtree line, from
"FRONTIER: 26 more exclusive-subtree roots"), so its edit goes to FRONTIER (LINE_OWNERS).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import apply_05spawn as base  # noqa: E402

F = "05-Spawn-Encounter-Lifecycle/"
OWNERS = {
    "FRONTIER": {
        F + "spawn-placement-and-retirement.md",
        F + "Spawn-Record/the-spawn-keep-entry-field-map.md",
    },
    "FABLE": {
        F + "why-the-enemies-you-killed-come-back.md",
        F + "Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md",
    },
    "SWE2-EC7": {
        F + "spawn-placement-height-and-authored-tunables.md",
    },
}
LINE_OWNERS = {"FRONTIER": ("`00307140` (~97 B)",)}


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
