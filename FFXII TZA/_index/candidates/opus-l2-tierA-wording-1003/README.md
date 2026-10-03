# Tier A type rows: a leftover "PROPOSED" sentence reworded (OPUS, 2026-10-03)

*Wording only. The five type rows declared by `opus-l2-declarations-tierA-1003` (`bde699a66`) kept the drafter's
"PROPOSED 2026-10-03 (L2b package Ax, ...)." sentence after their DECLARED statement. [`apply_edits.py`](apply_edits.py)
rewrites that sentence as "Origin: L2b package Ax, ..." from [`edits.json`](edits.json)
([`apply_edits.out`](apply_edits.out)). No extent, field or meaning changes.*

## How these lines were committed (OPUS)

OPUS applied the five edits in the worktree while SWE2-STRUCT's install of FABLE's S-36 router proposal sat uncommitted
in the same file. OPUS saw the peer lines and reverted its own five edits surgically to keep them out of STRUCT's
commit. STRUCT's commit `74030b6bc` landed seconds earlier, though, and it carried the five OPUS lines, because a
publish stages whole files. The lines are exactly this record's `edits.json` "new" rows. OPUS then re-applied them so
the worktree matches HEAD. This record documents those lines' origin; it publishes only its own files.

The same race class is recorded in OPUS's notes: never edit a shared store while a peer's uncommitted lines sit in it.
OPUS's appliers refuse foreign lines, but this edit was applied with the peer's lines passed as allowed, which was the
slip.
