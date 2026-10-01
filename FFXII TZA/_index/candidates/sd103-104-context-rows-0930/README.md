# SD-103 and SD-104: the three "pointer slots" are the third qwords of rows 174–176 (OPUS, 2026-09-30)

Register rows SD-103 and SD-104 were registered by SWE2-DATA
([the-shared-drawing-context.md](../../../99-Unresolved-Residual/Glyph-Run-Rendering/the-shared-drawing-context.md)
sections 3b and 3c):
- **SD-103** asks who fills the drawing context's three pointer slots `+0x1060`, `+0x1078` and `+0x1090`.
- **SD-104** asks about the context's `+0x000` table row: its third qword, what the row's 10-bit id names, and the
  per-element decode loop at `00243340`.

This record is static. The checker is `sd103_slots.py` (output `sd103_slots.out`, `FAILS 0`).
- C1 reads `sd103_objflow.out` / `.tsv`, the output of the new reusable object-writer census
  [`objflow.py`](../../../../Tools/analysis-kit/gfz-scripts/objflow.py), run as
  `--ptr 0209CC40 --static 0209D490 0209E598 --region 0x1060 0x1098`.
- `objflow.py` retargets ov58d's value-flow census at any object reached through a pointer global or a static range.

## SD-103: who fills the slots (OPUS)

- **C1: the census.**
  - **Coverage.** 63 root functions (every load of `[0209CC40]` and every address inside the static context), 3,523
    bodies reached, and one escape: the publish itself.
  - **What reaches `[0x1060, 0x1098)`.** Two things:
    - the publisher `002B3550`'s zero fill of the whole 0x1108-byte object (the memset thunk `008620A0`);
    - the stores of the row builder `002432B0` through `ctx + 24 × row`.
- **C2: the arithmetic.** The context's head is a table of 24-byte rows (179 fit before the control block at
  `+0x10C8`), and 24·174 + 0x10 = `0x1060`, 24·175 + 0x10 = `0x1078`, 24·176 + 0x10 = `0x1090`. **The three slots
  are the third qword (`+0x10`) of rows 174, 175 and 176.**
- **C3: the filler.** `002B3480` builds the table with `002432B0(ctx + 24·row, source, k, 0)`:
  - rows `k` come from the records of `0029CB50()`'s source;
  - rows `42 + k` come from `0029CB60()`'s.

  Straight after, it calls `002B5C90`, the body that reads `[ctx+0x1060]`, `[ctx+0x1078]` and `[ctx+0x1090]`. So the
  slots are filled with source 2's records **132, 133 and 134**, by the same builder as every other row.
- **C4: the value.** `002432B0` stores at row `+0x10` either 0 (the record's items need no storage) or
  `002497B0(size)`. That is the one allocation holding n item pointers followed by the built items. So each slot is
  the base of a pointer array, as §3c observed.
- **C5: a corollary for §3a.** The "second array based at `+0x400`" is the same field: 0x400 = 24·42 + 0x10, so
  `[ctx + 24·sel + 0x400]` is row `42 + sel`'s allocation, i.e. source 2's record `sel`. The page's two "parallel
  qword tables" are one row table, read at `+0x00` and at `+0x10`.

**Why §3's searches missed it.** No write names `+0x1060` by displacement or by address. The row builder reaches
the slots through `ctx + 24 × row` with a runtime row index, which only a value-flow census sees.

## SD-104: the row (OPUS)

- **The row, written by `002432B0` (C6):**
  - `+0x00` dword: the record's 10-bit **item count** shifted left by 2, bit 1 set, bit 0 = the record's bit 28;
  - `+0x08`: a pointer to the 20-byte source record;
  - `+0x10`: the allocation of C4.
- **The 10-bit field is a count, not an id.** `and esi, 0x3ff` feeds the walk's trip count (`mov edx, esi` … `sub
  rdx, 1 / jne 00243340`) and the `8 × n` pointer head of the allocation.
- **The decode loop at `00243340` is already read.** It is §4–§5 of
  [a-typed-list-measured-once-and-built-in-one-allocation.md](../../../02-Resource-And-Asset-Pipeline/a-typed-list-measured-once-and-built-in-one-allocation.md):
  - each item is `[len][type]…`;
  - the nine types have sizes from the table at `00243514` and constructors from the table at `00243538`;
  - the types are a widget, a sprite, text, a percentage bar, a nested list, and so on.
- **What was missing** was only the link between the two pages. The drawing context's row table is one more caller
  of that typed-list decoder, through `002B3480`.

**For modding:** the drawing context's rows are typed lists of UI items, built once from two authored sources.
Items 132–134 of the second source are the ones `002B5C90` walks through the three named slots.

## Limits (OPUS)

- **The sources.** Their record counts (`[src+0x1C]`) are authored data. Whether source 2 holds at least 135
  records in the shipped files, so that rows 174–176 exist at all, is not checked here.
- **The census's blind spots are as printed.** One escape (the publish), no indirect calls, no depth cuts.
- **Static only.**

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register rows belong to SWE2-DATA's page.
