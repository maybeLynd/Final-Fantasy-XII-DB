"""apply_by_owner.py OWNER [--apply] - run apply_21rng.py's edits for one owner's pages only (OPUS, 2026-10-02).

FABLE is working again (user, 2026-10-02), so OPUS applies only the edits on OPUS-led pages: the two CONTRACT pages and
the README. The edits on FABLE-led pages (rng-streams.md, which-roll-is-on-which-generator.md) go to FABLE as a request;
FABLE can run this script with its own name. OWNER is one of OPUS, FABLE, SWE2-FRONTIER, SWE2-EC7. Page ownership: the identity with most
content commits on the page (readiness-21-rng.md, "Page owners"). One line on an OPUS page is SWE2-FRONTIER's (the
`00863C80` row of CONTRACT-gameplay-generators.md's parity table), so its edit goes to FRONTIER, and one line on a FABLE page is SWE2-EC7's
(which-roll-is-on-which-generator.md's graphics-twist line, from EC7-49's batch 17), so it goes to EC7 (LINE_OWNERS).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import apply_21rng as base  # noqa: E402

F = "21-RNG-And-Determinism/"
OWNERS = {
    "FABLE": {
        F + "rng-streams.md",
        F + "which-roll-is-on-which-generator.md",
    },
}
LINE_OWNERS = {"SWE2-FRONTIER": ("| `00863C80` | `byte[02EB4234]` debug gate;",),
               "SWE2-EC7": ("call-free MT twist: `(mt[i]&0x7FFFFFFE | mt[i+1]&1) >> 1",)}


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
