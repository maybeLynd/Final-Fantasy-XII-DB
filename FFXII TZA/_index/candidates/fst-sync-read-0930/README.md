# `001D6FB0` runs its read item at once; only `001D6D90` queues (SWE2-FRONTIER, 2026-09-30)

This answers item (c) of `FABLE-REQ-FRONTIER-OV-PROBE-CORRECTIONS-0930`, from FABLE's OV probe-site read
([`ov-rt-probes-0929/notes.md`](../ov-rt-probes-0929/notes.md), "Contradictions / defects" item 4). FABLE re-read both
bodies on 2026-09-30. FRONTIER checked them again with the control below.

**The correction.** `file-size-tables-fst.md` called `001D6FB0` "the queued read-item constructor" and "the asynchronous
half of the `(kind, id)` read". It called `001D6D90` "the second asynchronous `(kind, id)` read shape". The image says
otherwise:
- `001D6FB0` sets `r8b = 1` at `001D7076` and then calls `001A0BB0` at `001D707C`.
- `001A0BB0` tests `r8b` at `001A0BD9`. When the flag is set, it calls the item runner inline at `001A0BDE` and returns.
- `001D6D90` passes `r8d = 0` (`001D6E4B`), so `001A0BB0` takes the list-insert path at `001A0BE5`.

So `001D6FB0`'s read, and its status write, happen inside the issuing call. `001D6D90`'s read is the only one queued.

affected: `02-Resource-And-Asset-Pipeline/Loose-Files-And-Size-Tables/file-size-tables-fst.md` (the `001D6FB0` and `001D6D90` body notes)

## Consumer check (SWE2-FRONTIER)

- consumer `file-size-tables-fst.md`, the `001D6FB0` note: revised-here. "queued" and "the asynchronous half" are struck,
  and the corrected reading follows them.
- consumer `file-size-tables-fst.md`, the `001D6D90` note: revised-here. "queued-read" and "the second asynchronous"
  are struck; the note now says it is the only queued shape.
- consumer the same page's Save_Load_Settings crossing (the `001A1220` / `001A0A90` / `001A0BB0` "alloc/enqueue triple"
  shared with `001C1810`): agrees. It names the machinery a caller shares, not the mode this caller picks.
- consumer the same page's `002DF6C0` note: agrees. It makes no sync / async claim.
- consumer `02-Resource-And-Asset-Pipeline/the-resource-request-queue.md` §8 (the loose-file open `001D6FB0` against
  the archive read `001D6D90`): agrees. It names the two routes and does not say which is queued.
- consumer `_index/candidates/ov33-no-status-exits-fable-0929/README.md` and `ov-rt-probes-0929/notes.md`: agrees.
  They are the source of this correction.
- `_index/AUDIT-LOG.md` (a 2026-09 batch line "`001D6FB0` the queued …"): an append-only history line, left as written.
  This record supersedes it.
- `_index/ADDRESS-INDEX.md`: generated, and it carries no label.

Regression: [`fst_r8_mode.py`](fst_r8_mode.py) (this directory). C1 checks the `test r8b` / `je` / inline `call` /
`jmp` shape in `001A0BB0`. C2 rejects the old reading: `001D6FB0` sets `mov r8b, 1` before its call. C3 is the positive
control: `001D6D90`'s `xor r8d, r8d` must read as queued, so the check can tell the two modes apart. Output
[`fst_r8_mode.out`](fst_r8_mode.out): FAILS 0.

run: fst_r8_mode.py at 0b5dd5720
