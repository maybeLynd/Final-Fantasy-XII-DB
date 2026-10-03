# SWE2-AUDIT-SPEC review: OPUS homing rows (opus-the-unit-shape-distance-primitives-homing-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-UNIT-SHAPE-DISTANCE-PRIMITIVES-HOMING-1` · Package: `_index/candidates/opus-the-unit-shape-distance-primitives-homing-1002/` · Page: `06-Movement-And-Navigation/the-unit-shape-distance-primitives.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh (verify mode) -> exit 0, `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0`.
- `rows.json`: 1 row, 5 anchors; rejected 0, missing 0.
- **Entry.** The row states none, and the class file `fable-homing-stream-1003/callee-host-bodies.tsv` lists no direct callers. A raw image census (`E8`/`E9`/`0F 8x`/rel8 targets, qwords, rip candidates) finds no reference either. The only 32-bit hits are `.rdata` unwind data and `.pdata`.
- **Host fit.** The body calls `00380FA0`, `0022E6D0` and `0022CF50`, and the page documents all three outside the homed row. The homing premise holds.
- **Semantic pass, all 1 row (765 B, read in full).** Exact, apart from the item below:
  - the `0x90`-byte high record (`lea r10,[rax+rax*8]; shl r10,4` at `0022CCEC`) and the 32-byte low record;
  - the per-group mask/value override `(flags & ~M) | (V & M)` at `0209A2D0` + 0x110/0x114, group = bits 13-17 + 0x20;
  - the type-1, type-4 and other-type rules on both paths;
  - the `comiss`/`jb` non-negative test (which also drops unordered) and the strict `< float +0x30`;
  - the hit point origin `[rdx+0x10]` + direction x (dist / `+0x34`), which must pass `0022CF50`;
  - the 16-byte store through qword `+0x20`, the id at `+0x42`, and the early stop on dword `+0x38`.

## SWE2-AUDIT-SPEC narrowing / notes

**Narrowing (row `0022CC50`, signed compare).** The id is a word compared **signed**. `0022CCD1 cmp di, dx` (dx = 0x5000) / `jge` skips; `0022CCDA cmp di, r12w` (0x4000) / `jl` goes to the low path. On the low path, `0022CD88 movsx r9, di; shl r9, 5` indexes the 32-byte table. So an id from 0x8000 to 0xFFFF is **not** skipped. It is negative, takes the low-id path and indexes before the table. "Skipping ids from 0x5000 up" is false for those ids. The row also never gives a base for the count and start words, which are `rdx`'s (`0022CC7B cmp r15w, [rdx+0x40]`, `0022CCC0 movsx eax, word [rbx+0x3e]` with `rbx = rdx`).

Replacement wording: replace "scans the word `+0x40` ids listed from word `+0x3E` in the index array at qword `+0x28` of `rcx`, skipping ids from 0x5000 up;" with "scans the word `+0x40` of `rdx` ids listed from word `+0x3E` of `rdx` in the index array at qword `+0x28` of `rcx`, skipping ids 0x5000 to 0x7FFF (the word id is compared signed, so an id from 0x8000 is negative and takes the low-id path with a negative index);". The rest of the row stands. The producer applies the narrowing and re-runs `interior_applier.py --apply`.
