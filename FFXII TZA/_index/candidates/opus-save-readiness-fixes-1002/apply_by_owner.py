"""apply_by_owner.py OWNER [--apply] - run apply_19save.py's edits for one owner's pages only (OPUS, 2026-10-02).

FABLE is working again (user, 2026-10-02), so OPUS applies only the edits on OPUS-led and shared pages. The edits on
FABLE-led pages and on SWE2-EC7's language page go to those lanes as requests; each lane can run this script with its
own name. OWNER is one of OPUS, FABLE, SWE2-EC7. Page ownership: the identity with most commits on the page.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import apply_19save as base  # noqa: E402

F = "19-Save-Load-Settings/"
OWNERS = {
    "FABLE": {
        F + "CONTRACT-save-image-pipeline.md",
        F + "Game-Settings-Config/ff12config-and-debglobal.md",
        F + "Game-Settings-Config/game-settings-ini-and-runtime-config.md",
        F + "how-a-manual-save-is-committed.md",
        F + "README.md",
        F + "Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md",
        F + "the-save-load-screen-widgets.md",
    },
    "SWE2-EC7": {
        F + "Language-And-Locale/language-selection-and-locale-ids.md",
    },
}


def main():
    owner = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "OPUS"
    others = set().union(*OWNERS.values())
    if owner == "OPUS":
        keep = [e for e in base.EDITS if e[0] not in others]
    elif owner in OWNERS:
        keep = [e for e in base.EDITS if e[0] in OWNERS[owner]]
    else:
        print("unknown owner", owner); print("FAILS 1"); return 1
    print("owner", owner, "edits", len(keep), "of", len(base.EDITS))
    base.EDITS = keep
    return base.main()


if __name__ == "__main__":
    sys.exit(main())
