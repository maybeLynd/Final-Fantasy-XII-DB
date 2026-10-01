# SWE2-AUDIT-SPEC review of SD-164 / SD-166 (first pass) / SD-167 (sd164-167-arena-allocator-0930, OPUS, 1f1defd7d): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30). Reviewed: OPUS's
`1f1defd7d`, the [README](../sd164-167-arena-allocator-0930/README.md) and `sd164_arena.py`. First half measured at HEAD
`9b6c5bc93`, resumed and finished at HEAD `b58c633f7`. Static, certified image.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD164-167-0930 | sd164-167-arena-allocator-0930 | `1f1defd7d` | ACCEPT-WITH-NARROWING (H2 wording; H1, A1, K1 accepted) |

**Re-run.** [rerun_sd164_arena.out](rerun_sd164_arena.out) is identical to the committed `sd164_arena.out` (CR ignored),
H1/H2/A1/K1 PASS, `FAILS 0`. `git status --porcelain` on the package dir shows nothing, before and after.

**Re-derived independently.** Tools: [arena_ix.py](arena_ix.py) (certified image, sha asserted; raw E8/E9/`0F 8x` index,
DIR64, rva32, rip and image-base displacement sweeps, `.pdata` roots) and [adump.py](adump.py). None of the author's tools.
- **H1, the slot's writers** ([slot_sweep.py](slot_sweep.py) / [.out](slot_sweep.out)).
  - rip operands into the record array `022D7FD0..022D89A8`: 19, all `lea` of the array base. None lands on `+0xA0`.
  - Image-base form (non-rip base, displacement `0x21B7FD0 + 0xA8·k`, plus 0 or `0xA0`): 0 hits.
  - All 19 `lea` sites are inside `00369000..0036E000`. Every operand there with displacement `0xA0` (7) was listed:
    writes are `00369E36` (the init), `0036C5B6` and `0036C5C1` (both in the setter `0036C5A0`), and two stack
    spills. The only read is `0036C02D`. The two known writers show up in the list, which is the control.
  - `0036C5A0` has 2 raw callers, `002EA4F3` and `002EA504` (ecx 6 and 0xA, rdx `lea` = `002E6D60`), no DIR64 and no
    rva32. The setter's `0036C5C1` is its out-of-range arm, which writes through a null record.
  - Boot chain: `002EA320` <- `00266D10` <- `0022A0B0` <- `0017D4C0` <- `0017D000`. Each link has exactly one raw
    call site and no stored pointer. H1 holds.
- **H2, the order of the callback and the allocation** ([callback_order.py](callback_order.py) / [.out](callback_order.out)).
  - In `0036BFE0` the callback (`0036C03B call rax`) comes before the attempt (`0036C0A9 call 0x36bc60`), and both
    retry edges (`0036C0B9`, `0036C0C4`) jump back to `0036C013`, which is above the callback. So the callback runs
    before every attempt, including each retry.
  - `0036BFE0` has 4 raw callers. Three of them, `0036A100`, `0036A1A0` and `0036B160`, first try `0036BC60`
    directly (`0036A11F`, `0036A1C9`, `0036B181`) and call `0036BFE0` only when that returned null. In those three
    the README's "a failed allocation ... first retires" is right.
  - The fourth, `0036D050` (`0036D08F`), is the null-pointer arm of the realloc that `0036CAD0` calls (raw callers
    `00251E00`, `0050EF00`). It calls `0036BFE0` without trying first, so there the callback runs before any failure.
  - **The gate `002E6900` (read in full).** It has one `ret` (`002E6A79`). Its one exit block starts with
    `002E6A70 xor eax, eax`, and the only jump into that block (`002E6A2F`) lands on the `xor`. So it always returns 0,
    and the callback's skip `002E6D6D jne` is never taken.
  - The gate is not a "memory is short" test: it is itself a retirement step. It takes the tail node of a second list,
    `0215FD90`. For each of the 32 set bits it passes that slot's dword to `0041E490` and `00369800` and clears it
    (`002E6960..002E69B4`), then unlinks the node. With `ecx = 0` it does one node. It then walks the rest of the list
    and calls `002E6A80` on nodes whose word at node `+0x12` is negative. The README does not mention `0215FD90`.
  - **The `0215FD88` tail.**
    - `+0x10 == 0`: `002E6DB1` jumps to `002E6DF6`, so the node is neither delivered nor freed; the head is cleared
      only if it is the list's only node.
    - `+0x18` bit 3 or `+0x19` bit 2 set: it skips only the deliver (`002E6DB7`/`002E6DBD` -> `002E6DE7`) and still
      frees the node (`002E6DEA call 0x2e9360`).
    - Otherwise it delivers (`002E6DDD`) and then frees.
    - When the list was empty it calls `002E6900(0)` a second time (`002E6E19`).
    - It always returns 0 (`002E6E1E`).
  - So the README's "unless the entry is flagged or empty" describes the deliver but not the free. The facts that
    the callback always returns 0 and the allocator retries only on its reclaim step (`edi`) are confirmed.
- **H1 detail.** `00369D30` clears `+0xA0` for the heap it initialises (`00369E36`). `r8` is zero from `00369D57` to
  that point, with no write in between. The slot of a heap that is never initialised sits in the zero-initialised
  `.bss` tail. So "null at boot" holds for all 15 heaps.
- **K1, the handle callers.** Raw E8/E9/jcc: `0036C4B0` has 2 callers (`0036B1AE` in `0036B160`, `0036BBF6` in
  `0036B980`); `0036B160` has 13 sites in the 9 functions of the table (per-function counts match); `0036B980` has 1,
  the `jmp` at `0036B97B` in `0036B970`; `0036B970` has 2 (`00378BF3`, `003DF2D8`). None has a DIR64 slot. Every
  `.rdata` rva32 hit (`01D7B004/20/30`, `01D7B1B4/D0`, `01D7B214/5C`, `01D736EC/20`) is a chained unwind entry,
  which equals a `.pdata` record. `0036B970` is not reached by fall-through: the code before it ends
  `0036B962 ret` and then `int3`. K1 holds.
- **A1 (88 constant / 47 variable).** It is consistent with the later SD-166 package. My push-site figures are in
  [../auditspec-review-sd166-0930/REVIEW.md](../auditspec-review-sd166-0930/REVIEW.md). Every constant here appears
  there, and there is no 7.

**Controls.**
- The `+0xA0` sweep must return the setter's `0036C5B6` and the init's `00369E36`, and it does. The image-base form was
  searched too; it is the form the push `0036C1F0` uses for its own tables.
- The order claim was tested on the only thing that can break it: whether each of `0036BFE0`'s callers makes an attempt
  before calling it. Three do and one does not.

**Citations checked.**
- `0036C02D`/`0036C03B`/`0036C039`, `0036C5B6`, `002EA4E7`/`EE`/`F8`/`FF`, `00369D57`/`00369E36`, `002E6D6D`/`6E1E`/
  `6E24`, `002E6DDD`, `002E6DEA`, `002E6D73` (-> `0215FD88`), `0036C043` and `0036C0B7`: each says what its sentence
  says.
- `0215FD88` is drained by the per-frame gate `002E65A0` (reads at `002E65C4`/`002E6642`), as
  [CONTRACT-per-frame-update-gate.md](../../../00-Engine-Core-Runtime/CONTRACT-per-frame-update-gate.md) line 409 says.

**Runtime routing.** The package's limit "which subsystem's pending load" depends on what the lists hold at run time.
That is a live fact. Everything else here is settled statically.

**Correction wording** (the producer replaces the H2 bullets):
> - `002E6D60` first calls `002E6900(0)`. That call retires the tail node of a second list, `0215FD90`: each set
>   slot goes to `0041E490` and `00369800` and is cleared, the node is unlinked, and the rest of that list is walked.
>   It always returns 0 (one exit, `002E6A70 xor eax, eax`), so the skip at `002E6D6D` is never taken.
> - The callback then takes the tail of `0215FD88`, the list the per-frame gate drains.
>   - An entry with `+0x10 = 0` is left in place.
>   - A flagged entry (`+0x18` bit 3, `+0x19` bit 2) is freed (`002E9360`) without being delivered.
>   - Any other entry is delivered (`0041E490`) and then freed.
>   - If `0215FD88` was empty, it calls `002E6900(0)` again.
> - It always returns 0.
> - `0036BFE0` calls it before **every** attempt in arena 6 or 0xA, including each retry after a reclaim. The three
>   allocation entries `0036A100`, `0036A1A0` and `0036B160` reach `0036BFE0` only after a direct `0036BC60` attempt
>   has returned null, so on those paths the retirement follows a failure. The realloc's null-pointer arm `0036D050`
>   (from `0036CAD0`) calls `0036BFE0` with no prior attempt, so there the callback runs before any failure.
> - The allocator never retries on the callback's answer (`test esi, esi` at `0036C0B7` sees 0); its reclaim step
>   (`edi`) decides.

No change to H1, A1 or K1.
