"""apply_by_owner.py OWNER [--apply] - run apply_01scriptvm.py's edits for one owner's pages only (OPUS, 2026-10-02).

FABLE is working again (user, 2026-10-02), so OPUS applies only the edits on OPUS-led and shared pages. The edits on
pages another identity leads, and on lines another identity last wrote, go to that identity as requests; each can run
this script with its own name. OWNER is one of OPUS, OPUS-HELD, FABLE, SWE2-FRONTIER, SWE2-DATA, FRONTIER, SWE2-EC7,
SWE2-CONTRACT.
Page ownership: the identity with most commits on the page (git log --format=%s, 2026-10-02). Unprefixed subjects are
shared and counted as OPUS; SWE2-EC7-NN and the bare "EC7" prefix count as SWE2-EC7, "SWE2CONTRACT-" as SWE2-CONTRACT
and "AUDIT-SPEC:" as SWE2-AUDIT-SPEC; FRONTIER and SWE2-FRONTIER are separate identities; a tie including OPUS stays
OPUS.
OPUS: README.md 1 shared; scriptvm-native-dispatch-table.md OPUS 4 + 10 shared / FABLE 5; verbs-that-only-wait-and-
verbs-that-do-nothing.md OPUS 3 + 8 shared / FABLE 3 / SWE2-EC7 3; how-a-script-names-a-thing-in-the-world.md OPUS 5 +
16 shared; CONTRACT-native-command-lifecycle.md OPUS 2 + 1 shared / FABLE 2; Interpreter-Core/worldactor-scriptvm-
interpreter.md OPUS 2 + 25 shared / FABLE 4; Interpreter-Core/the-script-from-bytecode-through-wait-and-resume.md OPUS 1
+ 2 shared / SWE2-CONTRACT 2 / FRONTIER 2; Interpreter-Core/script-variables-and-their-storage-classes.md OPUS 2 + 18
shared / FABLE 10; ATEL-Control-Modules/the-ctrl-module-debug-companions.md OPUS 4 + 46 shared / SWE2-DATA 14;
Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md OPUS 3 + 12 shared / FABLE 5 / SWE2-EC7 5;
Verb-Dispatch/CONTRACT-verb-dispatch-abi.md OPUS 4 + 16 shared; Verb-Dispatch/the-shape-of-the-verb-population.md OPUS
6 + 3 shared / SWE2-EC7 6; Verb-Dispatch/what-each-script-verb-touches.md OPUS 4 + 4 shared / SWE2-CONTRACT 3 /
FRONTIER 3; Spawn-Verbs/the-script-to-native-calling-convention.md OPUS 2 + 11 shared / SWE2-EC7 5 / FABLE 4 / FRONTIER
4; Party-Presentation-Verbs/the-party-read-in-state-machine.md OPUS 1 + 13 shared / SWE2-EC7 7;
Party-Presentation-Verbs/the-party-standard-motion-verbs.md OPUS 3 + 13 shared / SWE2-EC7 11;
Party-Presentation-Verbs/how-a-script-changes-how-the-party-looks.md OPUS 3 + 15 shared / SWE2-EC7 6;
Interpreter-Core/how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md OPUS 2 + 5 shared / SWE2-CONTRACT 6
(held, below).
FABLE: Interpreter-Core/the-actor-request-from-arming-through-start-and-return.md FABLE 3 / OPUS 1 + 1 shared;
Party-Presentation-Verbs/how-a-script-changes-the-battle-party.md FABLE 4 / OPUS 1.
Overlay carriers (scope_guard.py, 2026-10-02) go to SWE2-FRONTIER whatever the commits say: CONTRACT-interpreter-core.md
(FABLE 3 / SWE2-FRONTIER 2 / 1 shared), CONTRACT-script-to-native-bridge.md, Native-Command-Lifecycle/native-command-
lifecycle.md.
Held: how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md is named by the ACTIVE board task
SWE2AUDITSPEC-REQ-CONTRACT-RC13-CLAIMS-ROW-0930 (SWE2-CONTRACT, editing the page's claims-table row); apply
`apply_by_owner.py OPUS-HELD --apply` after it closes.
Dirty: ATEL-Control-Modules/the-ctrl-module-debug-companions.md (OPUS-led by commits) became dirty in the working
tree at 04:08 local while this was drafted - SWE2-DATA is editing it under three ACTIVE tasks
(FABLE-REQ-DATA-SN1-Q0-DOMAIN, FABLE-NOTICE-DATA-SN1-Q0-ONE-BASED, FABLE-NOTICE-DATA-SN1-Q0-LOGICAL; the 0-based -> 1-based
q0 line strike) - so all its edits go to SWE2-DATA, including the 003306E0 line FRONTIER last wrote (cb9885bcf).
Guard on the OPUS pages (2026-10-02): README.md BLOCKs on board-name collisions only (README basename); the resume
specification and the party-looks page BLOCK on peer commits under 24 h only (SWE2-CONTRACT de4492e21, pass-22 debt
final) - neither an ACTIVE task editing the page; the other OPUS pages are WARN (peer sweeps 24-72 h ago); none of them
is dirty. Re-run the guard before --apply.
No census TSV is edited; the regenerate requests (the adapter census C-V50, the read-before-write column C-V56, the reach
census C-V58) go to SWE2-DATA as requests, not hand edits.
LINE_OWNERS (git blame --porcelain on every edited line of the OPUS-led and held pages): FABLE last wrote the lifecycle
contract's AO-1 line, two 1,155 lines and the World-crossing line (fb3117aea, 7903502f7), the dispatch-table page's
dispatch-TSV paragraph (da9015016), the CR-3 dissolution lines (5f71d89b1), the BQ-9 row (ba1da098f) and the read-in
page's part-slot, pending-handle and installer lines (cb0ca0ca2); FRONTIER the binding page's subtree and Input-crossing
lines (3668e438d, 5834fb056) (and the 003306E0 subtree line, cb9885bcf, routed with its dirty page); SWE2-EC7 the
003B7180 / 0030AA00 lines (3151002b3, a1abec5e8), the 0037CE80 lines (220c9e379), the 002E9C00 and 0037CA80 hub lines
(ab562fd9e, 412c9a96c, be08c2af1) and the 020FB7xx line (f6cb9491d); SWE2-CONTRACT the interpreter claims row, the RC-12
footer line, the standard-motion helper row, the 003EC3D0 line and the reach map's two RC-21 lines (bed8dcd91). Every
other edited line on the OPUS-led pages was last written by an OPUS or an unprefixed (shared) commit.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import apply_01scriptvm as base  # noqa: E402

F = "01-Script-VM-Native-Bridge/"
OWNERS = {
    "FABLE": {
        F + "Interpreter-Core/the-actor-request-from-arming-through-start-and-return.md",
        F + "Party-Presentation-Verbs/how-a-script-changes-the-battle-party.md",
    },
    # Overlay carriers go to SWE2-FRONTIER whatever the commits say (scope_guard.py, 2026-10-02).
    "SWE2-FRONTIER": {
        F + "CONTRACT-interpreter-core.md",
        F + "CONTRACT-script-to-native-bridge.md",
        F + "Native-Command-Lifecycle/native-command-lifecycle.md",
    },
    # Dirty in the working tree under SWE2-DATA's ACTIVE SN-1 q0 tasks (2026-10-02, 04:08 local); no census TSV is
    # edited here (regenerate requests only).
    "SWE2-DATA": {
        F + "ATEL-Control-Modules/the-ctrl-module-debug-companions.md",
    },
    # OPUS-led page, held: SWE2-CONTRACT is editing its claims table
    # (SWE2AUDITSPEC-REQ-CONTRACT-RC13-CLAIMS-ROW-0930, ACTIVE 2026-10-02). Apply after that task closes:
    # `apply_by_owner.py OPUS-HELD --apply`.
    "OPUS-HELD": {
        F + "Interpreter-Core/how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md",
    },
}
LINE_OWNERS = {
    "FABLE": ("is `AO-1` and is not settled here.*",
              "every one of the 1,155 single-callback commands",
              "— three-visit phasing is the natural design and it would make 1,155",
              "Area initialisation is where the sixteen family-table pointers",
              "**`scriptvm-dispatch.tsv` has the two callbacks one call id early.**",
              "  five ATRAC3 verbs the same way, with a result callback only",
              "  is no two-shape split to explain.",
              "- [x] The **90 rows still without a measured arity**",
              "> 2. release what the old definition loaded",
              "  +0x04  u32   pending handle",
              "| `partyallread2` `0x46F` begin `0034D8B0`"),
    "FRONTIER": ("`003DBDC0` `ActorResource_StartEntryScriptExecution` (41 B)",
                 "`dword[r8]` bound (`00358A04`)",
                 "`00268850` (`ScriptVM_SubmitActorRuntimeRequest`, ~250 B)",
                 "`00226BE0`, an Input-layer helper",
                 "at `00226BFA`–`00226C03`): the entry-start path"),
    "SWE2-EC7": ("`003B7180` (129 B) is a wait/do-nothing verb body",
                 "`0030AA00` (179 B) is the four-slot readiness poll",
                 "`+8`/`+9`/`+0xA`/`+0xB` come from the",
                 "under the `0016D6A0` gate,",
                 "[`002E9C1C`](../../_index/ADDRESS-INDEX.md) — the signed definition byte",
                 "(`0037C730`) at [`0037CAA3`]",
                 "globals get field resets",
                 "two flag bytes, then it tails `00233CF0`.",
                 "render-record array at `020FB7xx`"),
    "SWE2-CONTRACT": ("| The interpreter has one entry, `0025DF00`",
                      "sites read other slots of the same footer;",
                      "pops the `-1.0f` inside `003580C0`, and the discarded",
                      "`cx == -1` exits; `sx(cx) * 0x740 + 022C6F28`",
                      "- The depth-1 table is reproducible in method and stale in detail",
                      "| Five of fourteen depth-1 rows drift"),
}


# Holds lifted 2026-10-02 (OPUS): these pages' holds are lifted; their held edits on other identities' lines go to them.
OWNERS["OPUS-HELD"] = set(OWNERS.get("OPUS-HELD", set())) - set(['01-Script-VM-Native-Bridge/Interpreter-Core/how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md'])


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
