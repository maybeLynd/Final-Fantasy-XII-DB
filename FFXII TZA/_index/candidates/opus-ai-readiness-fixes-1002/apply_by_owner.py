"""apply_by_owner.py OWNER [--apply] - run apply_09ai.py's edits for one owner's pages only (OPUS, 2026-10-02).

FABLE is working again (user, 2026-10-02), so OPUS applies only the edits on OPUS-led and shared pages. The edits on
FABLE-led pages go to FABLE as requests; FABLE can run this script with its own name. OWNER is one of OPUS, FABLE.
Page ownership: the identity with most commits on the page (git log --format=%s, 2026-10-02):
CONTRACT-enmity.md FABLE 3 / OPUS 2; gambit-evaluation-and-enmity.md FABLE 9 / OPUS 6;
which-gambit-set-fires-and-how-a-command-switches-it.md FABLE 3 / OPUS 2; CONTRACT-gambit-walk.md OPUS 8 / FABLE 2;
README.md one unprefixed commit (shared, OPUS). One line on the OPUS-led gambit-walk contract is FABLE's (the
"Whether the unit arm" sentence, from FABLE-REQ-OPUS-305), so its edit goes to FABLE (LINE_OWNERS).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import apply_09ai as base  # noqa: E402

F = "09-Combat-AI-And-Gambits/"
OWNERS = {
    "FABLE": {
        F + "CONTRACT-enmity.md",
        F + "gambit-evaluation-and-enmity.md",
        F + "which-gambit-set-fires-and-how-a-command-switches-it.md",
    },
}
LINE_OWNERS = {"FABLE": ("Whether the unit arm\nor the slot combiner",)}


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
