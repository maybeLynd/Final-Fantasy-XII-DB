# SWE2-AUDIT-SPEC review of SD-81 (sd81-eastl-callers-0930 at 08f4c0821): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75, 2026-09-30). Producer: SWE2-ORACLE, commit
`08f4c0821`. The record is unchanged between that commit and HEAD `cb5b622f2`. Static review against the certified image.

| request | record | commit | verdict |
|---|---|---|---|
| ORACLE-REQ-AUDITSPEC-SD81-0930 | [sd81-eastl-callers-0930](../sd81-eastl-callers-0930/README.md) | `08f4c0821` | ACCEPT |

**Re-run.** `sd81_callers.py`, run from its own directory at HEAD, prints 19 PASS lines and `FAILS 0`. Its output
([rerun_sd81_callers.out](rerun_sd81_callers.out)) is identical to the committed `sd81_callers.out`, ignoring CR. The
record directory was clean before and after the run.

**Re-derived independently** ([sd81_indep.py](sd81_indep.py) / [sd81_indep.out](sd81_indep.out),
[sd81_indep2.py](sd81_indep2.py) / [sd81_indep2.out](sd81_indep2.out)). This check does not use `retool.scan`, the
author's census instrument.

- **The census (A1).** I swept every `.text` byte for E8 / E9 rel32, `0F 8x` rel32 and EB / 7x rel8 transfers whose
  target is one of the six bodies (`0016D6D0`, `0016D720`, `0016D780`, `0016D7E0`, `0016D840`, `0016DA60`). Each hit
  was decoded at its site and required to lie on an instruction boundary of its owner, where the owner is a listed
  function or else a `.pdata` range.
  - Result: 213 sites, all of them `call`, with no jmp, jcc or rel8 transfer.
  - They belong to 99 owners, none reached through `.pdata` alone, and form 170 (owner, body) pairs.
  - The owner set equals the 99-row TSV exactly, in both directions.
  - `rawcalls.json` gives the same 213 call sites, with nothing extra on either side.
- **No wrapper or pointer in front of the six (A3 / A4).** There are 0 verified rip-relative references and 0 DIR64
  relocations to any of the six. The raw-only rip hits are exactly the call rel32 fields. The smallest owners are 134
  bytes (`001AEF70`, `001F5B80`).
- **The tags (F).** `008F4120` holds "EASTL map" and `008F3CB0` holds "EASTL set", read from the image.
- **I01 and I20, read whole or in part.**
  - `00199DB0` (I01 insert-unique):
    - it descends with a qword `cmp` / `setb` / `jae`, so the compare is unsigned;
    - it allocates through the allocator at `tree+0x30`, slot `+0x10`, with `lea edx, [r8 + 0x28]`, a 0x28 node;
    - it copies the qword key to `node+0x20` and increments the size at `tree+0x28`;
    - it stores `byte [ret+8] = 1` on both accept paths and `= 0` on the reject path (`00199EDC`). This is the
      unique-key reject path of B5.
  - `001FCB40` (I20) allocates 0x60 nodes (`lea edx, [r8 + 0x60]`) and calls the tree-copy `001FBEF0` before `ins`.
- **K1 / K2 (the font-page contradiction).**
  1. `001FDC15` spills `r8d` to `[rsp+0x18]`.
  2. After `push rdi` and `sub rsp, 0x40`, `001FDC25 lea rdx, [rsp + 0x60]` addresses that same slot.
  3. That address is the key argument of the call to `001FC420` at `001FDC2D`, with `rcx = font + 0x70`.
  4. `001FDCA0` then calls `001FC9F0`.
  5. In `001FC420`, `001FC487` loads "EASTL map" (`008F4120`) and `001FC4E8` calls `001FBEF0`.
  6. `001FC55C` is `lea rax, [rbx + 0x28]`, which returns the node value.
  7. The reader `001FDDD0` walks the outer tree's anchor at `font + 0x78`. For the inner tree it reads the root at
     `node+0x40` and the anchor at `node+0x30`. That is an EASTL tree object at `node+0x28`.

  So the writer builds the nested map, and K1 / K2 hold.

**Controls (the author's).**
- A1 compares the author's census with the published TSV, and both come from one instrument family. On its own it is
  not sensitive to a miss the two share. The raw byte sweep and `rawcalls.json` above supply that sensitivity, and they
  agree.
- A3 is rip-only. The relocation check above covers absolute pointers.
- P1 is a real known-answer positive control: the `.ker` node shape is recovered untold.
- The INFERENCE labels (method names, set/map for 8 untagged instantiations, the three inferred ties, the pool and job
  readings) are marked in the record and are not relied on by the answer.

**Not reviewed here.** The 21 thin wrappers of section W and the per-owner lists of section G were not re-derived row
by row.

**Routing already in place.** The contradiction with
[font-data-kerning-and-expansion.md](../../../16-UI/Text-And-Number-Rendering/font-data-kerning-and-expansion.md) §3
still stands on the page: "flat map", "never read back", "structurally inert". It is on the board as
`OPUS-CON-FONT-KERN-WRITER-NESTED-0930` (READY, SWE2-DATA), and the row edit as `ORACLE-REQ-DATA-SD81-ROW-0930`.
This review supports that contradiction and files no duplicate.
