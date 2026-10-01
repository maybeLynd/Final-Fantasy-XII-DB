# SD-164, SD-166, SD-167: the arena allocator's callback, arena 7, and the handle callers (OPUS, 2026-09-30)

Register rows SD-164, SD-166 and SD-167 were registered by SWE2-DATA
([where-the-games-memory-comes-from.md](../../../24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md)
sections 1 and 2). This record is static. The checker is `sd164_arena.py` (output `sd164_arena.out`, `FAILS 0`).

## SD-164: what the heap's callback slot holds (OPUS) — answered

- **H1: the slot and its writers.**
  - `0036BFE0` calls the qword at heap record `+0xA0` with (heap index, size). The records are the 15 heaps of
    `0xA8` bytes at `022D7FD0`, and `[022D89BC]` selects which one.
  - The boot initializer `00369D30` zeroes the slot for every heap (`r8`, cleared at `00369D57`, stored at
    `00369E36`).
  - The only other writer is the setter `0036C5A0(id ≤ 0xE, fn)`. Its one caller, the boot-time request-ring seeder
    `002EA320`, installs `002E6D60` for **heaps 6 and 0xA** (`002EA4F3`, `002EA504`).
  - This pairing was already on [render-event-selection-evidence.md](../../../17-Presentation-Rendering/Character-Render-Records/render-event-selection-evidence.md).
    No instruction addresses any record's `+0xA0` directly.
- **H2: what the callback does.** *(H2 narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd164-167-0930/REVIEW.md): the struck bullets are replaced by the review's wording that follows them; H1, A1 and K1 are unchanged.)*
  - ~~`002E6D60` takes the **tail of the request list `0215FD88`**, the list the per-frame gate drains. It delivers
    that entry (`0041E490`) and frees it (`002E9360`), unless the entry is flagged (`+0x18` bit 3, `+0x19` bit 2) or
    empty.~~
  - ~~It **always returns 0**.~~
  - ~~So a failed allocation in arena 6 or 0xA first retires one pending request, freeing its memory. The allocator
    never retries on the callback's answer (`test esi, esi` at `0036C0B7` sees 0); its reclaim step decides.~~
  - `002E6D60` first calls `002E6900(0)`. That call retires the tail node of a second list, `0215FD90`: each set
    slot goes to `0041E490` and `00369800` and is cleared, the node is unlinked, and the rest of that list is walked.
    It always returns 0 (one exit, `002E6A70 xor eax, eax`), so the skip at `002E6D6D` is never taken.
  - The callback then takes the tail of `0215FD88`, the list the per-frame gate drains.
    - An entry with `+0x10 = 0` is left in place.
    - A flagged entry (`+0x18` bit 3, `+0x19` bit 2) is freed (`002E9360`) without being delivered.
    - Any other entry is delivered (`0041E490`) and then freed.
    - If `0215FD88` was empty, it calls `002E6900(0)` again.
  - It always returns 0.
  - `0036BFE0` calls it before **every** attempt in arena 6 or 0xA, including each retry after a reclaim. The three
    allocation entries `0036A100`, `0036A1A0` and `0036B160` reach `0036BFE0` only after a direct `0036BC60` attempt
    has returned null, so on those paths the retirement follows a failure. The realloc's null-pointer arm `0036D050`
    (from `0036CAD0`) calls `0036BFE0` with no prior attempt, so there the callback runs before any failure.
  - The allocator never retries on the callback's answer (`test esi, esi` at `0036C0B7` sees 0); its reclaim step
    (`edi`) decides.
  - Every other arena has no callback.

## SD-166: does anything allocate from arena 7 after boot? (OPUS) — narrowed

- **A1: the push census.**
  - The active arena `[022D89BC]` is set by the scope push `0036C1F0`, whose only caller is the wrapper `0036C1D0`,
    and by the allocator's own helpers.
  - Of the wrapper's 135 call sites, **88 pass a constant arena**, resolved directly or as `lea ecx, [reg ± k]`
    over a register constant: 2 (8), 3 (9), 4 (4), 5 (5), 6 (18), 8 (42) and 9 (2). **None passes 7.**
  - A wider hand resolution (scratch) resolves more sites to 6, 8, 10 and 11. Again none is 7.
- **The 47 variable sites** mostly pass their caller's arena through the `0024918x`–`002493Dx` allocation helpers.
  Their callers are a second level, not closed here. So **no constant-arena site selects arena 7**, but pass-through
  chains are not excluded. That is consistent with the page's reading that arena 7's backing is used as a raw
  effect-file load buffer.

## SD-167: which callers take handles (OPUS) — answered

- **K1.** The handle-issuing path `0036C4B0` is reached only from `0036B160` and `0036B980`.

| entry | callers (sites) | pages the address index files them under |
|---|---|---|
| `0036B160` | `002E60F0` (1), `002E6700` (1), `002E6EB0` (1), `003DC5B0` (1), `003DD4C0` (2) | the per-frame update gate's request rings; `002E60F0` the character SE tables |
| | `0036ED50` (2) | the party read-in state machine |
| | `003A13F0` (3) | the R2 force-fight toggle |
| | `003AB8B0` (1) | resource-section addressing |
| | `0050DAD0` (1) | the actor-manager record |
| `0036B980` | `0036B970` (1), itself called from `00378BC0` (loader-bound bin families) and `003DF2C0` | |

**For modding:** only these request, party, force-fight, resource-section and actor-manager paths hold arena
*handles*. Every other allocation holds a raw pointer.

## Limits (OPUS)

- **SD-166.** The 47 variable push sites' pass-through chains are open.
- **SD-164.** What the retired request is (which subsystem's pending load) depends on the list's contents at run
  time.
- **Static only.**

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register rows belong to SWE2-DATA's page.
