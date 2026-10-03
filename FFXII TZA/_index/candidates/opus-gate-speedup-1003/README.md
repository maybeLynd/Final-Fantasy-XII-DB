# Pass-22 gate speed-up: same findings, about six minutes less per publish (OPUS, 2026-10-03)

Every lane's publish runs `check_publish_neighbours.py`. It runs the pass-22 audit (`audit_crossrefs.py`) twice: once on
HEAD and once on HEAD plus the publish. Each audit took about 210 s, and the whole check took 582-626 s. The user asked
OPUS to cut the time-heavy parts of the process where possible.

## What changed (OPUS)

**`audit_crossrefs.py`**: three exact equivalents in the per-document loop.

| site | before | after |
|---|---|---|
| control-only test (R5) | `re.search(r"\bcontrol\b", line, re.I)` once per (cited address, line) | the test once per line (`CONTROL_WORD`), looked up per address |
| "calls it unresolved" (check 3) | a fresh regex built and run per (document, cited address); about 53k one-off compiles per run, overflowing `re`'s cache | runs only when the body is classified and the page holds one of the three phrases (`UNRES_PHRASE`). The per-address pattern needs one of them to match, and its result was only used when `classified` |
| neighbour accounting (check 4) | `doc_accounts_for(xlow, folder_low, sub)` per (cited address, neighbour) | memoised per document by subsystem. `xlow` and `folder_low` are fixed for the page |

**`check_publish_neighbours.py`**:
- It builds one sparse worktree instead of two. The publish side is the same worktree with the batch copied over it.
- It caches the HEAD side by HEAD commit plus the census inputs. The cache rarely hits, because peers commit every few
  minutes; the audit change above is where the time went.

## Equivalence (OPUS)

`ab_audit.py BASE` runs the audit as of `BASE` and as in the working tree on the same docs tree, both read-only (the
tripwire register is not rewritten), and compares the JSON outputs. Both copies run with the kit's `__file__`, because
`load_functions` applies the UC-1 band only for the kit copy.

[`ab_audit.out`](ab_audit.out), base = HEAD before this change:

```
findings   SAME  base 185  work 185
neighbours SAME  base 524  work 524
tripwires  SAME  base 1333  work 1333
time base 206s  work 32s
EQUIVALENT
```

A first A/B loaded the base copy from a temp path and differed by one finding: `002FE7D0`, a UC-1 frontier body, as
UNLISTED CODE. The cause was that path (the band was skipped), not the change. The harness now pins `__file__`.

## Note (OPUS)

The change was first applied as three separate in-place edits. One publish (OPUS's own 1003G batch) imported the file
between two of them and refused with a `NameError`. It stopped before any commit and re-ran afterwards. Shared gate
scripts are now changed in one write.
