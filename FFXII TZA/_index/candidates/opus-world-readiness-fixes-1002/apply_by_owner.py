"""apply_by_owner.py OWNER [--apply] - run apply_03world.py's edits for one owner's pages only (OPUS, 2026-10-02).

FABLE is working again (user, 2026-10-02), so OPUS applies only the edits on OPUS-led and shared pages. The edits on
pages another lane leads go to that lane as requests; each lane can run this script with its own name. OWNER is one
of OPUS, SWE2-EC7, FABLE, SWE2-DATA, SWE2-FRONTIER.
Page ownership: the identity with most commits on the page (git log --format=%s, 2026-10-02; unprefixed subjects are
shared and do not lead; SWE2-EC7-NN task subjects count as the SWE2-EC7 lane, SWE2-FRONTIER as FRONTIER; a tie that
includes OPUS stays with OPUS, as shared pages do):
Map-Pack/the-map-ctrl-pack.md SWE2-EC7 27 / FRONTIER 9 / SWE2-DATA 7 / OPUS 5 / FABLE 1 (39 shared);
Weather/weather-apply-and-environment-materialization.md SWE2-EC7 18 / FABLE 4 / FRONTIER 4 / OPUS 2 (11 shared);
Field-Record-Table/field-record-table-navimapdata.md SWE2-EC7 10 / FRONTIER 6 / FABLE 4 / OPUS 2 / SWE2-DATA 1
(21 shared); Weather/weather-probability-and-transition-roll.md SWE2-EC7 4 / OPUS 3 / FRONTIER 1 (13 shared);
Weather/weather-slot-state-model.md SWE2-EC7 3 / OPUS 2 / FABLE 1 (9 shared); Weather/mweather-resource-format.md
SWE2-EC7 3 / OPUS 2 / FRONTIER 2 / SWE2-DATA 1 / FABLE 1 (8 shared);
FABLE: CONTRACT-field-environment-variant.md FABLE 3 / OPUS 1 (1 shared); CONTRACT-authored-trigger-points.md FABLE 2 /
OPUS 1 (2 shared); Field-Record-Table/field-record-bit15-action-permission.md FABLE 2 / OPUS 1 / FRONTIER 1
(10 shared);
SWE2-DATA: choosing-the-field-environment-variant.md SWE2-DATA 3 / OPUS 2 / FABLE 2 / SWE2-AUDIT-SPEC 1 /
SWE2-AUDIT-SEM 1 (6 shared);
SWE2-FRONTIER: CONTRACT-field-record-accessors.md FRONTIER 2 / FABLE 1 / SWE2-EC7 1 / OPUS 1 (15 shared);
OPUS: CONTRACT-weather.md OPUS 3 / SWE2-CONTRACT 1 / FABLE 1 (1 shared); walking-into-an-authored-trigger-point.md
OPUS 1 (9 shared); README.md (4 shared); ties with OPUS: Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md
OPUS 2 / FRONTIER 2 / FABLE 1 (11 shared).
scope_guard.py (2026-10-02) reports no overlay carrier and no dirty page among the fifteen. It BLOCKs three for other
reasons the receiving lane should read first: the map-pack page (board OPUS-REQ-AUDITSPEC-MAPCTRL-INTERIOR-1001 ACTIVE,
SWE2-AUDIT-SPEC), the variant page (SWE2-AUDIT-SPEC's promotion sweep 058c93e21 under 24 h) and README.md (board
OPUS-REQ-ASTRA-BJ1-GUARD-SNAPSHOT BLOCKED, ASTRA, a name match on "README").
Lines on OPUS-led pages whose last writer is another lane (git blame --porcelain, 2026-10-02) go to that lane
(LINE_OWNERS): FRONTIER wrote the call-chain page's 0026D910 subtree line ("FRONTIER: 26 more exclusive-subtree
roots"). Every other edited line on an OPUS-led page was last written by OPUS or by an unprefixed commit.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import apply_03world as base  # noqa: E402

F = "03-World-Area-Field/"
OWNERS = {
    "SWE2-EC7": {
        F + "Map-Pack/the-map-ctrl-pack.md",
        F + "Weather/weather-apply-and-environment-materialization.md",
        F + "Field-Record-Table/field-record-table-navimapdata.md",
        F + "Weather/weather-probability-and-transition-roll.md",
        F + "Weather/weather-slot-state-model.md",
        F + "Weather/mweather-resource-format.md",
    },
    "FABLE": {
        F + "CONTRACT-field-environment-variant.md",
        F + "CONTRACT-authored-trigger-points.md",
        F + "Field-Record-Table/field-record-bit15-action-permission.md",
    },
    "SWE2-DATA": {
        F + "choosing-the-field-environment-variant.md",
    },
    "SWE2-FRONTIER": {
        F + "CONTRACT-field-record-accessors.md",
    },
}
LINE_OWNERS = {
    "SWE2-FRONTIER": ("`0026D910` (`WorldField_InitializeCurrentFieldRuntimeParameters`, ~44 B)",),
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
