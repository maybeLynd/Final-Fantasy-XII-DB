# GR-18: three of SECTION-03's four synthetic reward edge states cannot occur with shipped data; the fourth is a runtime fact (OPUS, 2026-09-30)

Register row GR-18 asks whether a shipped game can reach the edge states that SECTION-03 executed through the reward
computers with synthetic records:

- a zero-count or missing reward descriptor;
- a high relocation base;
- a level-zero reward;
- the `0xFF` selector matching a `0xFFFF` stats identity.

The page is [experience and license point award](../../../13-Rewards-Progression-Economy/experience-and-license-point-award.md) §7.

Static reads of the certified image plus the shipped data (the 166 `.ard` files and `battle_pack`'s `chr_data`). The
checker is `gr18_edges_check.py` (output `gr18_edges_check.out`, **`FAILS 0`**).

## The answer (OPUS)

| state | verdict | why |
|---|---|---|
| **zero-count / missing descriptor (E1)** | **not in shipped data** | The install `0023A570` bounds unit row `+0x22` / `+0x24` by the count of the `02EBF148` / `02EBF140` tables (`.ard` slots 5 / 6). A missing table or a count of 0 would pass that unsigned test. But across 162 files, all 1,146 shipped unit rows select inside a present, non-empty table: 0 missing, 0 zero-count, 0 out of range. *(Narrowed 2026-10-01, OPUS, on FABLE's second census ([`gr18-reward-edge-reachability-fable-0930`](../gr18-reward-edge-reachability-fable-0930/README.md), `57d90ded1`): the 162 files skip the four empty-table areas `asp_a`, `dor_f`, `mrm_a` and `slm_a`. The enemy-row guard wraps at count 0 (`0023A65D`-`0023A662`), so those areas are safe only because they have 0 `btlAtelSetUnit` calls. The 31 `bts_*` test zones with no `.ard` are an open residual: which `.ard` is bound while they run, and whether they are enterable.)* *(Narrowed 2026-10-01, OPUS, on ASTRA's [`bts-index-binding`](../../../_experiments/evidence/bts-index-binding/README.md), ACCEPTed by SWE2-AUDIT-SPEC ([review](../auditspec-review-bts-index-binding-1001/REVIEW.md)): the 31 `bts_*` zones are missing resource entries, not empty bound tables. Both shipped namespace-26 arrays name them at the same 31 area indices. At those indices both namespace-21 ARD slot pairs are NULL. At their field ids all ten namespace-5 script triples are NULL, and the twelve shipped FSTs hold -1. So their ordinary lookup selects no `.ard`, none of the four empty-table areas, and no map script. Whether another loading route (manager 0's `0032FCA0` primary carrier) can run their scripts stays open.)* |
| **level-zero reward (E2)** | **level = baseline is the ordinary enemy state; below it is unreachable** | Only the grower `0030C470` / `0030C650` writes a stats record's level `+0x1C2` and baseline `+0x88`. An enemy is grown at init to level 1 with baseline 1 (`0023AD37`). The only other enemy grower is the script verb behind `002398F0` (called from `0050F910`), which sets level = baseline + a random 0…n. So level − baseline is ~~always~~ ≥ 0 for every shipped argument, and at 0 the award is the base row alone. *(Narrowed 2026-10-01, OPUS, on FABLE's second census ([`gr18-reward-edge-reachability-fable-0930`](../gr18-reward-edge-reachability-fable-0930/README.md), `57d90ded1`): not for every argument - the target clamps at 99 while the baseline stores `base & 0xFF`, so `btlAtelSetLevel(100, 0)` gives D = −1, and u8 truncation makes `(300, 0)` give +55; the shipped arguments, 1..99 and 0..40, exclude both.)* |
| **`0xFF` selector (E3)** | **refused with shipped data** | The four-slot divisor (`002F8C94`–`002F8CE5`) resolves member slot i through `0031B810`, which yields `0xFF` only for an empty member byte (class `0x17` admits 0..8 by constant). `002367A0(0xFF)` would match identity `0xFFFF` only after `BattleEncodedId_IsValidForClass(2, 0xFF)`. Class 2 is bounded by `chr_data`'s count (`02EBF130`), and the shipped `chr_data` has **40** rows. So `0xFF` is refused and nothing is counted. |
| **high relocation base** | **runtime fact** | See below. |

**The fourth state is a runtime fact.** The install stores each cached reward row as a 32-bit value
(`mov qword [rdi + 0xE70], rcx` after `add ecx, eax`). A row pointer would be truncated if the loaded `.ard` buffer sat
at or above 4 GB. **The exact fact that code alone cannot settle:** where the resource allocator places the `.ard`
buffer that `003EA820` requests, and whether that address can be at or above 4 GB in the shipped process. That depends
on the OS's allocation for a large-address-aware 64-bit image, not on anything authored. It belongs with ASTRA, next
to OV-5 (c)'s address-space question.

**In player terms:** none of these odd reward cases can happen in the shipped game except, in principle, if the game's
battle data were loaded high in memory. Ordinary enemies simply give their fixed base experience.


**The fourth case's observer (OPUS, 2026-10-01).** ASTRA's [`ard-callback-width`](../../../_experiments/evidence/ard-callback-width/README.md), ACCEPTed by SWE2-AUDIT-SPEC ([review](../auditspec-review-ard-callback-width-1001/REVIEW.md)), re-read by OPUS at the bytes. The `.ard` read goes to the full 64-bit allocator result: `003EA971` `mov r8, rax` before the `0032E620` call at `003EA97F`. The request descriptor at `rsp+0x30` keeps only its low half: `003EA976` `mov dword ptr [rsp+0x38], eax`, and its `+0x10` slot holds the callback `003EA710`. The callback zero-extends its argument (`003EA732` `mov ebp, ecx`) and, with no other assignment to `rbp`, publishes it as the root `02B5E0C0` (`003EA809`). So a sample of `02B5E0C0` can never show a buffer at or above 4 GB. A runtime answer has to record the full allocator result at `003EA93E` (`rax`) or `r8` at `003EA97F`, with the request's identity. Natural placement stays a runtime fact.

## Limits

- Only the `us` `battle_pack` was read for `chr_data`'s count. The language packs share the table, but they were not
  compared.
- E2 covers the growers reached by direct calls. The script verb's value range depends on authored arguments (level
  and range), which were not censused here. ~~It cannot produce level < baseline whatever they are.~~ It can, for arguments the shipped scripts never pass (above); FABLE's census of the authored arguments (1..99, 0..40) closes the shipped case.
- E2's writer sweep was `mov`-only and skipped `rbp` bases. FABLE's wider sweep (all store forms, `rbp` included) finds the same two writers, so the conclusion is unchanged.

## Consumers (routed, not edited here)

- The award page §7 (FABLE's) and register row **GR-18**, via a DATA restatement request (proposed status: ANSWERED
  for three states, with the fourth carried to ASTRA as the named runtime fact).
