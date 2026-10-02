"""apply_by_owner.py OWNER [--apply] - run apply_24crt.py's edits for one owner's pages only (OPUS, 2026-10-02).

FABLE is working again (user, 2026-10-02), so OPUS applies only the edits on OPUS-led and shared pages. The edits on
pages another identity leads, and on lines another identity last wrote, go to that identity as requests; each can run
this script with its own name. OWNER is one of OPUS, OPUS-HELD, FABLE, FRONTIER, SWE2-EC7, SWE2-FRONTIER, SWE2-DATA.
Page ownership: the identity with most commits on the page (git log --format=%s, 2026-10-02). Unprefixed subjects are
shared and counted as OPUS; SWE2-EC7-NN and the bare "EC7" prefix count as SWE2-EC7; FRONTIER and SWE2-FRONTIER are
separate identities; a tie including OPUS stays OPUS.
OPUS: README.md 2 shared; Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md OPUS 2 +
7 shared / FABLE 7; Lazy-Static-Initialization/lazy-statics-and-the-one-time-init-lock.md OPUS 2 + 9 shared / SWE2-EC7
10; Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md OPUS 4 + 10 shared;
Cxx-Runtime-Families/object-construction-destruction-and-static-lifetime.md OPUS 2 + 14 shared / SWE2-EC7 13;
Cxx-Runtime-Families/the-ordered-container-runtime.md OPUS 3 + 6 shared; Cxx-Runtime-Families/the-msvc-ordered-
container-runtime.md OPUS 3 + 7 shared; Generated-Adapters/the-return-value-adapter-family.md OPUS 3 + 7 shared / FABLE
3; Memory-And-Allocation/where-the-games-memory-comes-from.md OPUS 10 + 24 shared / SWE2-EC7 16 / FABLE 9; Thunk-Layer/
the-thunk-layer-and-why-call-counts-disagree.md OPUS 5 + 16 shared / SWE2-EC7 14; Runtime-Service-Surface/what-the-game-
asks-windows-for.md OPUS 3 + 11 shared / FABLE 8; Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-
cookies.md OPUS 3 + 10 shared / FABLE 7; Maths-Library/the-maths-the-game-runs-on.md OPUS 2 + 14 shared / SWE2-EC7 6.
SWE2-EC7: Static-Initialization-And-Teardown/static-initialisers-and-teardowns.md SWE2-EC7 15 / OPUS 3 + 7 shared;
Generated-Families/generated-function-families.md SWE2-EC7 26 / OPUS 6 + 4 shared.
No overlay carrier and no dirty page among them (scope_guard.py and git status, 2026-10-02; the dirty paths in the
folder are six Generated-Families members TSVs, which no edit touches).
Held: none. The ACTIVE board tasks the guard names on README.md (AUTO-INCORP-FABLE-REQ-AUDITSEM-REVIEW-TAKEBACKS2-0930,
SWE2-CONTRACT) are README basename collisions; OPUS-CLOUD-F-INTERIOR-W24-1002 (ACTIVE, the exception-funclet page among
its targets) is OPUS's own cloud stream, not another lane. OPUS-HELD is kept as an empty owner so the call shape matches
the other folders. Re-run the guard before --apply.
Guard on the OPUS pages (2026-10-02): README.md BLOCKs on board-name collisions only; the two ordered-container pages
BLOCK on a READY task (SWE2-EC7-PUB-B1-ADRIFT2-0930) and a finished promotion sweep only; the return-value adapter page
and the memory page BLOCK on peer commits under 24 h only (FABLE befd3553c and 1851971f3, no ACTIVE task editing them);
the others are WARN.
No census TSV is edited. Count items that rest on a tag census or a members file are left; the ones that need a TSV
changed are SWE2-DATA regenerate requests, not hand edits.
LINE_OWNERS (git blame --porcelain on every edited line of the OPUS-led pages): SWE2-EC7 last wrote the 0015BD30 and
005FD0E0 interior lines (442eb5209, ceae38d05), the 005CD820 release line (0f7160ab3), the 00194CD0 and 0061ECF0 lines
(442eb5209, ceae38d05), the dealloc-list line and the 00194F50 line (4ebb37e46, 6c3dd0d0c), the 0036D2F0 line
(4db391af9), the 00280750 line (b65119a80) and the 00334120 line (394b9a092); SWE2-DATA the SD-82 sweep note
(959a77e13); FRONTIER the 00624580 subtree lines (74eea5091); SWE2-FRONTIER the 0036A240 row (0cdb6009a); FABLE the
six-doors banner (1e660c3a5), the 022D8E10 ruling line (ab3dd7aa5), the WinMain SEH row (362ba0a41), the second-dump
trigger line (00b54a48c), the S-3 correction (976709d80) and the S-2 / T-9 line (c641f4cdb). Every other edited line on
the OPUS-led pages was last written by an OPUS or an unprefixed (shared) commit.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import apply_24crt as base  # noqa: E402

F = "24-Compiler-And-CRT-Runtime/"
OWNERS = {
    "SWE2-EC7": {
        F + "Static-Initialization-And-Teardown/static-initialisers-and-teardowns.md",
        F + "Generated-Families/generated-function-families.md",
    },
    # Held 2026-10-02 (OPUS): OPUS's own ACTIVE cloud F task OPUS-CLOUD-F-INTERIOR-W24-1002 holds this page, so a
    # publish touching it would loop on the claim. Apply after that page's F-interior ingest.
    "OPUS-HELD": {
        "24-Compiler-And-CRT-Runtime/Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md",
    },
}
LINE_OWNERS = {
    "SWE2-EC7": ("(`01DF09E0` into `01F80140`+)",
                 "a higher value runs `008092FC` (the lock-init)",
                 "one-time-init / shared-lock pair this page documents.",
                 "`00194CD0` (455 B) is a call-free exception funclet",
                 "`0061ECF0` (3 B) is the `return 1` stub",
                 "`0078A960` and `0085E730`, the free/dealloc entries",
                 "`00194F50` (270 B) is a sound-request body",
                 "`0036D280` runs at init: `0016D6A0` packs",
                 "then fires `00249180(rsi, 7, 3, 0xD7, proc 00280740)`",
                 "`andps` with the `0x7FFFFFFF` mask at"),
    "SWE2-DATA": ("are what the sweep cannot rule out: **SD-82**.",),
    "FRONTIER": ("`00624580` (~32 B)",
                 "| `0061A250` | `PClassDescriptorConcrete` class body |"),
    "SWE2-FRONTIER": ("(`0036A266`–`0036A270`), byte store at `022D89A8`",),
    "FABLE": ("through exactly **six** doors.",
              "establishes it is an **8-element dword array",
              "| the whole application, `007980A0` — **the crash-dump filter** |",
              "Its trigger, and whether it can run before the filter,",
              "> to `atexit` (`00808B90`), so each **runs once at process exit**",
              "`S-2` and\n`T-9` stay open."),
}


# Holds lifted 2026-10-02 (OPUS): these pages' holds are lifted; their held edits on other identities' lines go to them.
OWNERS["OPUS-HELD"] = set(OWNERS.get("OPUS-HELD", set())) - set(['24-Compiler-And-CRT-Runtime/Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md'])


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
