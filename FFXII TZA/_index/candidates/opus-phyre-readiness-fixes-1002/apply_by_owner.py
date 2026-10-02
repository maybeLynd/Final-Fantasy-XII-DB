"""apply_by_owner.py OWNER [--apply] - run apply_22phyre.py's edits for one owner's pages only (OPUS, 2026-10-02).

FABLE is working again (user, 2026-10-02), so OPUS applies only the edits on OPUS-led and shared pages. The edits on
pages another identity leads, and on lines another identity last wrote, go to that identity as requests; each can run
this script with its own name. OWNER is one of OPUS, OPUS-HELD, FABLE, SWE2-EC7, SWE2-FRONTIER, SWE2-DATA, FRONTIER,
SWE2-CONTRACT.
Page ownership: the identity with most commits on the page (git log --format=%s, 2026-10-02). Unprefixed subjects are
shared and counted as OPUS; SWE2-EC7-NN counts as SWE2-EC7; a tie that includes OPUS stays OPUS.
OPUS: the-camera-state-snapshot.md OPUS 2 + 4 shared / SWE2-DATA 2; Subsystem-Map/phyre-subsystem-map.md OPUS 2 + 9
shared / FABLE 4; Subsystem-Map/the-fifteen-modules-registered-before-main.md OPUS 3 + 13 shared / SWE2-EC7 14;
Phyre-Asset-Container/the-packed-namespace-and-the-file-side-schema.md OPUS 2 + 9 shared / FABLE 6;
Phyre-Asset-Container/CONTRACT-phyre-packed-namespace.md OPUS 1 + 4 shared / FABLE 4;
Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md OPUS 18 + 21 shared / SWE2-EC7 25;
CONTRACT-phyre-class-descriptor.md OPUS 7 + 12 shared / FABLE 6; member-registration-and-the-recovered-field-schema.md
OPUS 14 + 13 shared / FABLE 12; how-a-class-registers-its-array-members-and-annotations.md OPUS 2 + 7 shared;
phyre-class-instance-sizes-and-alignments.md OPUS 3; Embedded-Lua-And-Object-Bindings/... OPUS 2 + 10 shared / FABLE 4;
Script-Object-Accessors/... OPUS 5 + 11 shared / SWE2-EC7 5; Shader-Variant-Selection/... OPUS 1 + 8 shared / FABLE 6;
Animation-Channel-Binding/... OPUS 5 + 15 shared / FABLE 3.
FABLE: README.md FABLE 3 / OPUS 0 + 1 shared; Post-Process-Chain/the-phyre-post-effect-class-family.md FABLE 12 / OPUS 5
+ 6 shared.
SWE2-EC7: Application-Framework-Boundary/the-game-is-a-phyre-application.md SWE2-EC7 20 / OPUS 3 + 14 shared;
Phyre-Asset-Container/CONTRACT-phyre-cluster-header.md SWE2-EC7 16 / OPUS 1 + 11 shared;
Phyre-Asset-Container/the-cluster-header-and-what-the-loader-rejects.md SWE2-EC7 20 / OPUS 3 + 14 shared;
Post-Process-Chain/the-post-process-passes-and-their-shader-constants.md SWE2-EC7 30 / OPUS 6 + 21 shared;
The-Frame/what-happens-between-two-frames.md SWE2-EC7 35 / OPUS 6 + 18 shared (also named by the ACTIVE board task
OPUS-REQ-AUDITSPEC-TWOFRAMES-INTERIOR-1001, SWE2-AUDIT-SPEC: tell SWE2-EC7 to apply after that audit closes).
Overlay carriers (scope_guard.py, 2026-10-02): none in this folder, so SWE2-FRONTIER has no edits.
Held: no OPUS-led page is named by an ACTIVE task of another lane (the CDMS / modules BLOCKs are READY tasks, the array
and file-schema BLOCKs a finished promotion sweep 058c93e21, the packed-namespace BLOCK a SWE2-DATA commit <24h); so
OPUS-HELD is empty.
Guard on the OPUS pages (2026-10-02): BLOCK on class-descriptor-and-metadata-system.md and the fifteen-modules page
(READY SWE2-EC7-PUB-B1-ADRIFT* tasks + SWE2-EC7 commits 24-72 h), on the array-members and file-schema pages (the
promotion sweep 058c93e21 <24 h) and on the packed-namespace page (SWE2-DATA af4b761dd <24 h); CLEAR on
CONTRACT-phyre-packed-namespace.md and the instance-sizes page; the others WARN (pass-22 sweeps 24-72 h ago). None is
dirty. Re-run the guard before --apply.
No census TSV is edited, so SWE2-DATA has no page edits (its LINE_OWNERS edits below are prose lines it last wrote).
LINE_OWNERS (git blame --porcelain on every edited line of the OPUS-led pages): FRONTIER last wrote the modules page's
00686C40 battery row (a2cfa20d1); SWE2-DATA the camera page's SD-60 note (959a77e13), the namespace page's two w7
bit lines (af4b761dd) and the array page's static-init lines (959a77e13); SWE2-EC7 the namespace page's 00597F80 row
(bba30de07), the metadata page's 00639160 row (cfd5e9a57), the member page's 0063C0C0 interior line and pointer-width
line (c7f00bddf) and 006329B6 line (d1d2332ac), and the accessor page's three optional-pointer family rows
(5700227c9); SWE2-CONTRACT the packed-namespace contract's NS-1 / NS-4 line (9c762c421); FABLE the descriptor
contract's +0x50 ring row (e02cf5967) and the context-switch page's vtable-slot and 0065xxxx rows (7e700b748). Every
other edited line on the OPUS-led pages was last written by an OPUS or an unprefixed (shared) commit.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import apply_22phyre as base  # noqa: E402

F = "22-Middleware-PhyreEngine/"
OWNERS = {
    "FABLE": {
        F + "README.md",
        F + "Post-Process-Chain/the-phyre-post-effect-class-family.md",
    },
    "SWE2-EC7": {
        F + "Application-Framework-Boundary/the-game-is-a-phyre-application.md",
        F + "Phyre-Asset-Container/CONTRACT-phyre-cluster-header.md",
        F + "Phyre-Asset-Container/the-cluster-header-and-what-the-loader-rejects.md",
        F + "Post-Process-Chain/the-post-process-passes-and-their-shader-constants.md",
        F + "The-Frame/what-happens-between-two-frames.md",
    },
    # Overlay carriers go to SWE2-FRONTIER whatever the commits say (scope_guard.py, 2026-10-02): none here.
    "SWE2-FRONTIER": set(),
    # Generated census TSVs are never hand-edited; none is edited here (regenerate requests only).
    "SWE2-DATA": set(),
    # No OPUS-led page is named by an ACTIVE task of another lane (scope_guard.py, 2026-10-02).
    "OPUS-HELD": set(),
}
LINE_OWNERS = {
    "FRONTIER": ("(including `00617810`, the `PUtilityDynamicGeometry` registrar of the §2 table)",),
    "SWE2-DATA": ("What is still not claimed is what the two matrices and the two floats mean",
                  "set on 0 shipped records** (`SD-65`); bits 1–5 stay",
                  "bits 1–5 not established (values 0, 2, 8, 12, 20, 32, 34, 40",
                  "class-descriptor initialisers (static init)",
                  "the member descriptors are built by code at static initialisation."),
    "SWE2-EC7": ("is the four-vector teardown sibling covering the upper half of the same record:",
                 "dealloc-and-clear pattern. Together with `00598040`",
                 "else appending `rdi+0x50` into `[rbx+0x10]`'s list",
                 "no direct calls; returns 8 when attribute bit 1 is set",
                 "(`0063C106: call qword ptr [rax+8]` with `rcx = rdx = ctx`)",
                 "`00D580B0` installs at `006329B6`, `+0x48`/`+0x50` take the name and context args,",
                 "the member records - this row disposes of the adapter, not the adapted.",
                 "x2 subset-shared, 6 distinct others).",
                 "plus member-specific ops (5 distinct)."),
    "SWE2-CONTRACT": ("`NS-1`'s bit names and `NS-4` stay open, and the",),
    "FABLE": ("when the parent's `+0x70` is the same registry, and appends it otherwise |",
              "| vtable-slot members (reached only through a data qword) | 7 |",
              "they are vtable slots, one of them `PPostProcessing::PScreenSpaceReflection` slot 1."),
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
