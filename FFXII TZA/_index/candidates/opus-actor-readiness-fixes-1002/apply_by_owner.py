"""apply_by_owner.py OWNER [--apply] - run apply_04actor.py's edits for one owner's pages only (OPUS, 2026-10-02).

FABLE is working again (user, 2026-10-02), so OPUS applies only the edits on OPUS-led and shared pages. The edits on
pages another identity leads, and on lines another identity last wrote, go to that identity as requests; each can run
this script with its own name. OWNER is one of OPUS, OPUS-HELD, FABLE, SWE2-EC7, SWE2-FRONTIER, SWE2-DATA, FRONTIER,
SWE2-STRUCT.
Page ownership: the identity with most commits on the page (git log --format=%s, 2026-10-02). Unprefixed subjects are
shared and counted as OPUS; SWE2-EC7-NN and the bare "EC7" prefix count as SWE2-EC7, "SWE2CONTRACT-" as SWE2-CONTRACT
and "AUDIT-SPEC:" as SWE2-AUDIT-SPEC; FRONTIER and SWE2-FRONTIER are separate identities.
OPUS: README.md 12 shared / FABLE 1; the-record-behind-every-actor.md OPUS 5 + 55 shared / FABLE 5 / FRONTIER 5 /
SWE2-EC7 4; the-actor-storage-record-field-map.md OPUS 1 + 27 shared / SWE2-EC7 10; CONTRACT-actor-record-pool-and-
region-map.md OPUS 4 + 15 shared / SWE2-EC7 3; CONTRACT-manager-slot-entry-tables.md OPUS 3 + 11 shared / FABLE 3;
battleunit-slot-pool-and-actor-class.md OPUS 2 + 23 shared / SWE2-EC7 3; battle-record-kind-byte.md OPUS 2 + 14 shared /
FABLE 9; actor-type-id-partition-and-the-13-value-band.md OPUS 2 + 5 shared; CONTRACT-field-runtime-pass.md OPUS 6 +
16 shared / SWE2-EC7 11; the-movement-and-secondary-context-censuses.md OPUS 1 + 22 shared / SWE2-STRUCT 7;
the-definition-record-flag-pair.md OPUS 1 + 9 shared; the-battle-unit-field-map.md OPUS 5 + 68 shared / SWE2-EC7 54
(held, below).
FABLE: CONTRACT-actor-storage-record-initialisation.md FABLE 3 / OPUS 1 / SWE2-CONTRACT 1.
SWE2-EC7: the-actor-manager-record-field-map.md SWE2-EC7 39 / OPUS 4 + 22 shared; the-npc-name-dictionary.md SWE2-EC7 27
/ OPUS 1 + 16 shared; the-record-00329220-builds.md SWE2-EC7 31 / OPUS 1 + 17 shared.
Overlay carriers (scope_guard.py, 2026-10-02) go to SWE2-FRONTIER whatever the commits say: the-field-runtime-pass.md,
Unit-Definition/CONTRACT-battle-unit-construction.md, Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md.
Held: the-battle-unit-field-map.md is named by the ACTIVE board task OPUS-REQ-AUDITSPEC-RECORD-EIGHT-PASS6-SIGNATURES-1001
(SWE2-AUDIT-SPEC, auditing the page's record); apply `apply_by_owner.py OPUS-HELD --apply` after it closes.
Guard on the OPUS pages (2026-10-02): README.md BLOCKs on board-name collisions only (two ACTIVE tasks naming other
folders' README.md); battleunit-slot-pool-and-actor-class.md and CONTRACT-field-runtime-pass.md BLOCK on ASTRA tasks in
BLOCKED state (ASTRA-HANDLE-SEMANTIC-CLOSURE, OPUS-REQ-ASTRA-MGRMARK-RELOAD: live checks, not edits); the other OPUS
pages are WARN (FABLE's pass-22 sweep 7903502f7 or peer sweeps 24-72 h ago); none is dirty. Re-run the guard before
--apply.
No census TSV is edited, so SWE2-DATA has no edits (the count drift in section 3.2 is stated on the pages).
LINE_OWNERS (git blame --porcelain on every edited line of the OPUS-led pages): FRONTIER last wrote the record page's
00265FF0 / 00265B60 subtree lines (3668e438d) and the battle-unit field map's 00233AD0 and 00383670 subtree lines
(04dc361cf); SWE2-FRONTIER the field map's 00234200 subtree line (0cdb6009a); FABLE the manager contract's subscript-110
line (c99411da6), the kind-byte page's GR-2 row (8c6f1e4df) and body banner (797b72780), and the census page's
+0x14C / +0x14D / +0x14E rows (ba69c0caa); SWE2-STRUCT the census page's radius-floor line (e19bf3542) and
SecondaryContext array line (9089d4786). Every other edited line on the OPUS-led pages was last written by an OPUS or
an unprefixed (shared) commit.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import apply_04actor as base  # noqa: E402

F = "04-Actor-Entity/"
OWNERS = {
    "FABLE": {
        F + "CONTRACT-actor-storage-record-initialisation.md",
    },
    "SWE2-EC7": {
        F + "Actor-Manager-Record/the-actor-manager-record-field-map.md",
        F + "Actor-Names/the-npc-name-dictionary.md",
        F + "Unit-Display-Record/the-record-00329220-builds.md",
    },
    # Overlay carriers go to SWE2-FRONTIER whatever the commits say (scope_guard.py, 2026-10-02).
    "SWE2-FRONTIER": {
        F + "the-field-runtime-pass.md",
        F + "Unit-Definition/CONTRACT-battle-unit-construction.md",
        F + "Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md",
    },
    # Generated census TSVs are never hand-edited; none is edited here (regenerate requests only).
    "SWE2-DATA": set(),
    # OPUS-led page, held: SWE2-AUDIT-SPEC is auditing a record that names it
    # (OPUS-REQ-AUDITSPEC-RECORD-EIGHT-PASS6-SIGNATURES-1001, ACTIVE 2026-10-02). Apply after that task closes:
    # `apply_by_owner.py OPUS-HELD --apply`.
    "OPUS-HELD": {
        F + "Battle-Unit/the-battle-unit-field-map.md",
    },
}
LINE_OWNERS = {
    "FRONTIER": ("`00265FF0` (~97 B) — frame record op",
                 "`00265B60` (~90 B) — `qword[rcx+0xC0]` null-gate",
                 "flag-word writes set `ACTIVATION_COMMITTED` (bit 1)",
                 "`00383670` `Navigation_SelectNextWaypointXZ` (1,223 B)"),
    "SWE2-FRONTIER": ("frees the slot through `00861EC0` with stride",),
    "FABLE": ("a store at `+0xF4`, inside the `0x200` slot.",
              "Open: joining the other values, including 6",
              "| `+0x14C` | 1 | 0 / 1 |",
              "| `+0x14D` | 1 | 0 / 1 |",
              "| `+0x14E` | 1 | 0 / 1 |",
              "**PARTIAL — deliberately.** The census is exact"),
    "SWE2-STRUCT": ("the turn/blend scalar `max(0.05,",
                    "SecondaryContext's first 192 bytes are a"),
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
