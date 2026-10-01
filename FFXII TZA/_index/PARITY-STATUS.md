# Parity status — the eleven dimensions, per reconstructed subsystem

**GENERATED — do not hand-edit.** `Tools/analysis-kit/gfz-scripts/parity_status.py`

Criteria: [`../../../Reconstruction/PARITY-STANDARD.md`](../../../Reconstruction/PARITY-STANDARD.md). Charter §21 requires parity status to be explicit per dimension; this is that table.

> **14 declaration problem(s):**
> - diff_field_gate.py: section-15 claim STRUCK but still verdicted NOT EXERCISED: `022C6D20[m]` has **no clear anywhere in the image** -- **REFUTED 2026-09-21 (ASTRA; consumed by FABLE)** — the clear is `0032F14B mov byte ptr [rdi+r14+0x21A6D20], bpl` in `0032ED80 ActorResource_ResetManagerLoadState`, with `r14 = 00120000` from `0032EDBB lea r14,[rip-0x20EDC2]`, `rdi` the sign-extended manager index and `bpl` zeroed at `0032EDC2`, behind the `0032F107 cmp rdi,5` / `jae` valid-index check
> - diff_render_pool.py: 9 section-15 claim(s) not in CONTRACT_MAP: the slot handle is `(gen << 8) \; a full pool returns handle `0`, and the allocator stamps the slot BEFORE it resolves the parent; **CORRECTS the static reading**: RES routes EVERY nonzero mode to `0036B130`, and the mode-1 arm is dead code; RES bounds the resolver's result: a low dword unsigned-`<= 0x40` is returned as `0`; the allocator requires a LIVE parent record - `arg = -1`, or a zero `+0x284` gate, faults; `002ED570`'s two handle deposits are CONDITIONAL, not cleared; `002ED570`'s index product is SIGNED; row 550 NARROWS and does not close: two of its thirteen named callees have now executed real; `002ED570`'s context IS the slot-bank container shape, independently
> - 00-Engine-Core-Runtime/CONTRACT-boot-fixups.md: section 15 yields no claims -- the '## 15.' heading or the 'claim' table header is missing or renamed
> - 00-Engine-Core-Runtime/CONTRACT-encoded-id-space-and-class-registry.md: section 15 yields no claims -- the '## 15.' heading or the 'claim' table header is missing or renamed
> - 02-Resource-And-Asset-Pipeline/Authored-Expressions/CONTRACT-authored-expression-evaluation.md: section 15 yields no claims -- the '## 15.' heading or the 'claim' table header is missing or renamed
> - 02-Resource-And-Asset-Pipeline/CONTRACT-resource-request-queue.md: section 15 yields no claims -- the '## 15.' heading or the 'claim' table header is missing or renamed
> - 04-Actor-Entity/Unit-Definition/CONTRACT-battle-unit-construction.md: section 15 yields no claims -- the '## 15.' heading or the 'claim' table header is missing or renamed
> - 05-Spawn-Encounter-Lifecycle/CONTRACT-spawn-placement.md: section 15 yields no claims -- the '## 15.' heading or the 'claim' table header is missing or renamed
> - 07-Combat-Action/CONTRACT-apply-result-to-target.md: section 15 yields no claims -- the '## 15.' heading or the 'claim' table header is missing or renamed
> - 12-Items-Equipment-Shops-License/CONTRACT-license-check.md: section 15 yields no claims -- the '## 15.' heading or the 'claim' table header is missing or renamed
> - 13-Rewards-Progression-Economy/CONTRACT-world-loot-pickup-pool.md: section 15 yields no claims -- the '## 15.' heading or the 'claim' table header is missing or renamed
> - 15-Input/CONTRACT-input-subsystem.md: section 15 yields no claims -- the '## 15.' heading or the 'claim' table header is missing or renamed
> - 16-UI/CONTRACT-ui-request-router.md: section 15 yields no claims -- the '## 15.' heading or the 'claim' table header is missing or renamed
> - 21-RNG-And-Determinism/CONTRACT-which-generator-serves-which-roll.md: section 15 yields no claims -- the '## 15.' heading or the 'claim' table header is missing or renamed

| dimension | `achievement_counters` | `actor_pool` | `angle_wrap` | `auto_status` | `battle_mode` | `bazaar` | `binding_publish` | `body_pool` | `character_publish` | `class_descriptor` | `class_descriptor_dtor` | `coast_down` | `commit_action` | `field_gate` | `field_music` | `field_record` | `flag_banks` | `frame_gate` | `gambit_walk` | `group_completion` | `hp_write` | `inventory_query` | `lua_header` | `manager_slot` | `name_registry` | `party_slots` | `phyre_header` | `phyre_namespace` | `prep_step` | `quality_preset` | `ramp_channels` | `render_pool` | `reward_award` | `rng_generators` | `save_image` | `sound_request` | `status_write` | `storage_read` | `table_lookup` | `target_buffer` | `transform` | `verb_dispatch` | `verb_marshal` | `widget_construct` | `workbench_save` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **CALCULATION** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | n/a | **yes** | **yes** | **yes** | n/a | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | n/a | **yes** |
| **STRUCTURAL** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | n/a | n/a | **yes** | **yes** | n/a | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** |
| **STATE-TRANSITION** | **yes** | **yes** | n/a | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | n/a | n/a | **yes** | **yes** | **yes** | **yes** | **yes** | n/a | n/a | **yes** | **yes** | **yes** | n/a | n/a | **yes** | **yes** | **yes** | **yes** | n/a | **yes** | **yes** | n/a | **yes** | **yes** | n/a | **yes** | n/a | no | **yes** | **yes** | **yes** |
| **CONTRACT** | **yes** | no | no | no | no | no | no | no | **yes** | no | no | no | no | no | no | no | no | no | no | no | no | no | **yes** | no | no | **yes** | no | no | no | no | no | no | no | no | **yes** | no | no | no | no | no | no | no | no | no | no |
| **EDGE-CASE** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** | **yes** |
| **SERIALIZATION** | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | no | n/a | n/a | n/a | n/a | n/a | **yes** | n/a | n/a | n/a | **yes** | **yes** | n/a | n/a | n/a | n/a | n/a | n/a | **yes** | n/a | n/a | n/a | n/a | n/a | n/a | n/a | **yes** | n/a | n/a |
| **RNG** | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | **yes** | n/a | n/a | n/a | n/a | **yes** | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| **TIMING** | n/a | n/a | n/a | n/a | no | n/a | n/a | n/a | n/a | n/a | n/a | no | n/a | no | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | no | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| **INTEGRATION** | no | no | no | no | no | no | no | no | no | no | no | no | no | no | no | no | no | no | no | no | no | no | no | no | no | no | no | no | **yes** | no | no | no | no | no | no | no | no | no | no | no | no | no | no | no | no |
| **PRESENTATION** | n/a | n/a | no | n/a | n/a | n/a | n/a | n/a | no | n/a | n/a | no | n/a | n/a | no | n/a | n/a | no | n/a | no | no | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | no | no | no | n/a | n/a | n/a | n/a | no | n/a | n/a | n/a | n/a | n/a | n/a | no | n/a |
| **FULL-SUBSYSTEM** | no | no | no | no | no | no | no | no | no | no | no | no | no | no | no | **yes** | no | no | no | no | no | no | no | no | no | no | no | no | no | no | no | no | no | no | no | no | no | no | no | **yes** | no | no | no | no | no |

| dimension | covered | not covered | n/a |
|---|---:|---:|---:|
| CALCULATION | 42 | 0 | 3 |
| STRUCTURAL | 42 | 0 | 3 |
| STATE-TRANSITION | 33 | 1 | 11 |
| CONTRACT | 5 | 40 | 0 |
| EDGE-CASE | 45 | 0 | 0 |
| SERIALIZATION | 5 | 1 | 39 |
| RNG | 2 | 0 | 43 |
| TIMING | 0 | 4 | 41 |
| INTEGRATION | 1 | 44 | 0 |
| PRESENTATION | 0 | 12 | 33 |
| FULL-SUBSYSTEM | 2 | 43 | 0 |

## Contract coverage — derived, not declared

Charter §21's `CONTRACT` dimension asks whether the harness exercises the claims its contract makes. **Each harness now carries a `CONTRACT_MAP`** and this table is computed from it; the claim strings are checked against each contract's §15 table on every run, so a reworded claim shows up as drift rather than as silent coverage.

> **`OPEN QUESTION` rows are excluded from the denominator and named anyway.** A §15 row whose confidence is `UNKNOWN` records a question, not a behaviour, and no case can exercise it. Excluding it without saying so would be the quiet kind of denominator this project keeps catching.

| subsystem | §15 rows | exercised | partial | not exercised | of which scope | open questions | verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| `achievement_counters` | 9 | 8 | 0 | 0 | 0 | 1 | COVERED |
| `actor_pool` | 13 | 4 | 0 | 9 | 5 | 0 | NOT COVERED |
| `angle_wrap` | 28 | 3 | 2 | 22 | 17 | 1 | NOT COVERED |
| `auto_status` | 24 | 21 | 0 | 2 | 0 | 1 | NOT COVERED |
| `battle_mode` | 15 | 5 | 0 | 10 | 3 | 0 | NOT COVERED |
| `bazaar` | 22 | 17 | 0 | 5 | 2 | 0 | NOT COVERED |
| `binding_publish` | 14 | 2 | 0 | 10 | 5 | 2 | NOT COVERED |
| `body_pool` | 8 | 6 | 0 | 1 | 0 | 1 | NOT COVERED |
| `character_publish` | 11 | 10 | 0 | 0 | 0 | 1 | COVERED |
| `class_descriptor` | 19 | 6 | 0 | 12 | 3 | 1 | NOT COVERED |
| `class_descriptor_dtor` | 19 | 12 | 0 | 6 | 1 | 1 | NOT COVERED |
| `coast_down` | 13 | 9 | 0 | 3 | 1 | 1 | NOT COVERED |
| `commit_action` | 16 | 14 | 0 | 1 | 0 | 1 | NOT COVERED |
| `field_gate` | 25 | 11 | 0 | 13 | 9 | 1 | NOT COVERED |
| `field_music` | 12 | 7 | 0 | 4 | 0 | 1 | NOT COVERED |
| `field_record` | 7 | 6 | 0 | 1 | 0 | 0 | NOT COVERED |
| `flag_banks` | 15 | 6 | 1 | 7 | 1 | 1 | NOT COVERED |
| `frame_gate` | 10 | 6 | 1 | 2 | 0 | 1 | NOT COVERED |
| `gambit_walk` | 15 | 11 | 0 | 2 | 0 | 2 | NOT COVERED |
| `group_completion` | 24 | 3 | 0 | 19 | 3 | 2 | NOT COVERED |
| `hp_write` | 19 | 14 | 2 | 2 | 2 | 1 | NOT COVERED |
| `inventory_query` | 16 | 9 | 0 | 6 | 0 | 1 | NOT COVERED |
| `lua_header` | 6 | 5 | 0 | 0 | 0 | 1 | COVERED |
| `manager_slot` | 14 | 9 | 1 | 3 | 0 | 1 | NOT COVERED |
| `name_registry` | 13 | 8 | 1 | 4 | 0 | 0 | NOT COVERED |
| `party_slots` | 9 | 8 | 0 | 0 | 0 | 1 | COVERED |
| `phyre_header` | 33 | 15 | 0 | 16 | 2 | 2 | NOT COVERED |
| `phyre_namespace` | 22 | 6 | 0 | 14 | 1 | 2 | NOT COVERED |
| `prep_step` | 25 | 17 | 0 | 8 | 3 | 0 | NOT COVERED |
| `quality_preset` | 13 | 3 | 2 | 5 | 0 | 3 | NOT COVERED |
| `ramp_channels` | 12 | 6 | 1 | 5 | 0 | 0 | NOT COVERED |
| `render_pool` | 31 | 23 | 0 | 8 | 2 | 0 | NOT COVERED |
| `reward_award` | 22 | 14 | 0 | 5 | 0 | 3 | NOT COVERED |
| `rng_generators` | 12 | 8 | 0 | 4 | 0 | 0 | NOT COVERED |
| `save_image` | 10 | 9 | 0 | 0 | 0 | 1 | COVERED |
| `sound_request` | 31 | 14 | 0 | 16 | 4 | 1 | NOT COVERED |
| `status_write` | 25 | 10 | 1 | 14 | 1 | 0 | NOT COVERED |
| `storage_read` | 55 | 5 | 0 | 49 | 41 | 1 | NOT COVERED |
| `table_lookup` | 26 | 9 | 0 | 14 | 5 | 3 | NOT COVERED |
| `target_buffer` | 13 | 9 | 0 | 3 | 0 | 1 | NOT COVERED |
| `transform` | 17 | 10 | 0 | 6 | 0 | 1 | NOT COVERED |
| `verb_dispatch` | 20 | 9 | 0 | 11 | 2 | 0 | NOT COVERED |
| `verb_marshal` | 20 | 2 | 2 | 16 | 2 | 0 | NOT COVERED |
| `widget_construct` | 16 | 2 | 2 | 12 | 2 | 0 | NOT COVERED |
| `workbench_save` | 12 | 6 | 0 | 5 | 0 | 1 | NOT COVERED |

> **`of which scope` counts `NOT EXERCISED` rows whose own reason carries a literal marker saying the claim is about code this pilot does not contain or does not reach.** Those rows close through `INTEGRATION` — the pilot growing into a subsystem harness — not through new test cases. It is a floor: only author-written markers count (`parity_claim_scope.py`), so an unmarked unexercised row is neither confirmed work nor confirmed scope.

**397 of 768 testable contract claims are exercised across the 45 pilot(s) that have a contract** — 43 of the 811 §15 rows record open questions and are excluded. At least **117 of the unexercised are out of pilot scope**, not test debt.

### `achievement_counters` — 20-Platform-Online-Achievements/CONTRACT-achievement-counters.md

| claim | status | note |
|---|---|---|
| the descriptor table is 30 entries of 8 bytes at 00D10460 | **EXERCISED** | descriptors are planted per id and driven at id 29 and id 30, so a wrong stride reads the wrong descriptor and a wrong bound accepts an id the original refuses |
| the first descriptor byte is the counter's WIDTH: 2 is a signed word, 4 a signed dword | **EXERCISED** | each kind is read back at its own width, and a value too large for a word is stored under kind 2 and read back truncated and sign-extended |
| update saturates at 0x7FFF for kind 2 and 0x7FFFFFFF for kind 4 | **EXERCISED** | both caps driven from just below and from far above; the caps are the signed maxima of the two widths, which is why the width row and this row are one fact read twice |
| a sum that goes negative is clamped to zero on kinds 2 and 4 but NOT on the fall-through | **EXERCISED** | a negative amount driven on all three arms; two clamp and one does not |
| submode 3 treats the amount as a bit index biased by 0xE2, and submode 8 stores nothing | **EXERCISED** | both driven, with the counter compared before and after |
| when the id has no counter, submode 0 fires on a threshold and submode 1 on an exact match | **EXERCISED** | both driven at, below and above the threshold, and the exact-match arm driven one either side |
| the fire lookup supplies the threshold when it is non-zero | **EXERCISED** | driven at zero and non-zero with the descriptor's own threshold set differently, so the two sources are distinguishable |
| the store is 00316BF0, not 00315E90 | **EXERCISED** | the trace shows 00315E90 called with the id alone and its result unused, immediately before 00316BF0 is called with the value - and the counter only changes at the second |
| any runtime observation | OPEN QUESTION | none exists |

### `actor_pool` — 04-Actor-Entity/CONTRACT-actor-record-pool-and-region-map.md

| claim | status | note |
|---|---|---|
| the descriptor table at 01E0C328 is four bytes per sequence for eight sequences | **EXERCISED** | the fixture addresses it with a literal stride and drives every one of the eight entries |
| the table's first byte is a layout class, not an unrelated field | **EXERCISED** | both tables decoded from the image and compared; the run also shows the region map never reads that byte, so the agreement is corroboration and not causation |
| 0x6E0 is the largest record size and not a stride | NOT EXERCISED · scope | a statement about the allocator, which is out of scope |
| a record is always reached through the pointer table at pool + 8 + index × 8, never by stride | NOT EXERCISED · scope | the allocator and the initialiser are out of scope |
| each record size is rounded up to 16 before being multiplied by its count | NOT EXERCISED | the allocator |
| the per-sequence counts are authored per-area data, not constants | NOT EXERCISED · scope | authored data; nothing here loads an area |
| the header is two tables of roundUp16(8 × definitionValueTotal + 8) | NOT EXERCISED | the allocator |
| the pool tallies per-layout-class counts at +0x1D0 + class × 2 | NOT EXERCISED | the allocator |
| the region map's four arms write +0xB8, +0xC0 and +0xA0 as record-relative offsets, and an out-of-range sequence writes NOTHING | **EXERCISED** | every sequence 0-9 plus the mask's boundaries, with all four pointers poisoned first |
| +0xA8 is +0xA0 plus 0xC8 or 0xA0, chosen by the descriptor's sub flag **compared against 1 exactly** | **EXERCISED** | sub values 0, 1, 2 and 0xFF for every sequence, each entry differing from its neighbours |
| none of the three construction paths writes +0x64–0x78 | NOT EXERCISED · scope | two of the three paths are out of scope, and an absence over a range is not what this fixture measures |
| the binder's `+0x60` store installs `ActorManagerSlot` `groupPersistentBank` and cannot reach the record entry lists — the §14 ordering item dissolves on object identity, not sequencing | NOT EXERCISED · scope | a static provenance/object-identity claim about the binder 0026C8C0 and the ActorResource_* family, all out of this fixture's scope |
| nothing observed at runtime | NOT EXERCISED | still true for the allocator and the initialiser; the region map is isolated original-code, not a running game |

### `angle_wrap` — 06-Movement-And-Navigation/CONTRACT-facing-and-steering.md

| claim | status | note |
|---|---|---|
| the record is `0x80`, inline, two of them | NOT EXERCISED | `00269F9F`'s `shl rax,7` plus `add rax,0x120` indexing is not emulated; `run_fmod` hands the callee one record at a fixed address |
| the wrap and its three constants | **EXERCISED** | both shipped forms run over the real `01CEBC50`, `00915620` and `01CEBC78` bytes for every float bit pattern in the case set |
| the bias cancels exactly only while x + bias stays in its binade | **EXERCISED** | the crossing at 4 - pi, its ulp neighbours, a 64-point spread across [4 - pi, 1), the negative mirror and the 8 - 2pi crossing are driven against the shipped bytes. The family exists because exhausting the bias branch's differing domains showed the crossing is where the branch becomes observable at all: 890,824 of the 1,065,353,216 floats in [+0.0, 1.0) distinguish the two biases and every one is at or above 4 - pi. It kills no mutant the old sweep did not already kill - the counts are 4/3/2 before and after - and it replaces incidental coverage of the crossing with named coverage |
| the two facing variants are identical **for kind ≠ 3** | **EXERCISED** | checked on EVERY run, not inherited: both bodies are normalised -- RIP targets resolved, branch targets made relative to the entry -- and compared instruction by instruction. 29 each, exactly one differing, `xor r8d,r8d` against `mov r8d,1` at position 12 |
| `0026B6A0` never touches `r8` — but its kind-3 arm forwards it live | PARTIAL | the first half is checked on every run with capstone's regs_access, which reports IMPLICIT reads and writes too, so a `push r8` or an `xor r8d,r8d` would count: 0 of 30 instructions. A CONTROL on `rcx` finds 6, so a blind instrument cannot pass this silently. The second half -- the tail-jump forwarding `r8d` into `002E5FB0`/`002E5E10` -- is static evidence; `0026B6A0` kind 3 is not separately driven |
| kind dispatch in `0026B6A0` and `0026C090` | PARTIAL | all THREE arms of `0026C090` now run per case, and they are behaviourally distinct at the observable: only kind 3 writes the record, kind 1 TAIL-JUMPS to `0026B6A0` (with the r8 it forwards live to `002E5FB0` when the kind is 3) and kind 2 does nothing at all. `0026B6A0`'s own dispatch is executed but not separately driven -- 3 of the 6 function-by-kind combinations |
| push/pop are the only slot callers | NOT EXERCISED | a four-instrument reachability census over the image |
| mode 4 reads the `FrameLimit` base | NOT EXERCISED · scope | no case sets `+0x68`, so mode 4 is never reached |
| `002E5FB0` is a 12-byte thunk into `002E5E10`: `context = actor[+0xB8]`, `xmm2 = context[+0xAC]` (the prior rate, handed back unchanged), `r9d = flag` | NOT EXERCISED | static derivation only; `0026B6A0` kind 3 is not separately driven, so the thunk never executes in this suite |
| `002E5E10` is the kind-3 steering-record write: re-wraps the heading (third wrap site), stores `context[+0xA8]` and `{id,target}` fields `+0x50`/`+0x60`/`+0x70` via `003DA850` (a `[rcx+8]` leaf) — `+0x60`/`+0x70` only when `actor+0x0D` bit 5 clear — plus `record[+0x138]+0xF0` when that object exists, and finally `003EC260(word[record], prior_rate, heading, 0, flag!=0)` | NOT EXERCISED · scope | static derivation only; reached only through the undriven kind-3 arm |
| the flag is `003EC260`'s commit gate: 0 stages the `{rate, heading, 0}` triple into slot `+0x120`–`+0x128`; 1 additionally shifts it to `+0x250`–`+0x258` and calls `004288B0(slot,-1)` or `003B3CA0([slot+0x288],0x1E)` | NOT EXERCISED · scope | static derivation only; `003EC260` is two calls below the undriven kind-3 arm |
| `002E6300` is a 10-byte flag gate — `test r8b,r8b` / `js → 00265510` / `ret` | NOT EXERCISED · scope | static derivation only; reached from the undriven mode/teardown paths |
| `00265510`–`0026567F` is an eight-leaf kind-3 accessor cluster — each gated `(+3 & 0xE0)==0x60` (else 0): `sub[+0x64]` byte, `sub[+0x66]` word, `slot[+0xDC]` record `+0x34` float, slot-`edx` (clamped) record `+0x34`, `sub[+0x62]>>6 &1`, `sub[+0x28]&0x7F`, `cvttss2si(sub[+0x78])`, `movsx(sub[+0x68])` | NOT EXERCISED · scope | static derivation only; the leaf getters are not driven |
| `002627C0` copies the `0x80` steering record from slot `+0xDC` to slot `+0xDC+1` | NOT EXERCISED | static derivation only; the push helper is not on any driven path |
| `002EC2C0` is the kind-3 vector-writer: stores `[rdx]` (a `Vec4`) into `[ctx+0xF0]+0x10`, clears `+0x62` bits 0–2, then `002E7B40`/`00265020`/`003A19A0`/`0026A8E0` apply a position-derived heading and `0026A870`/`0026A950` zero two channels | NOT EXERCISED | static derivation only; reached through `00263230`/`002EAAA0`/`002EBFA0`, none driven |
| `002EBE50` is the mode initiator: `edx==0` zeroes `+0xB4`/`+0x224`; else snapshots `sub[+0x70]`/`+0x74` into them after `003A1C50`-wrapping the deltas, derives a frame count `abs(Δ)/sub[+0x6C]` (clamped by a constant) into `word[+0x60]` (`derived_turn_frames` in `_types/`), `+0x62` bit 5 cleared and bit 4 set, stamps `+0x63 = arg2`, then calls `002EC3F0` and `002E8EE0` | NOT EXERCISED · scope | static derivation only; the mode arms are not driven |
| `002EBFA0` steers toward a resolved target body: `003587C0` resolves the target, `[rsi+0xC0]` record must exist with `dword != -1`; writes the target triple `+0x10`/`+0x14`/`+0x18` and `003589B0(rsi)` id into `+0x1C` (`resume_target_handle` in `_types/`), `+0x62` bit 0 set and bits 1–2 cleared; heading from both `00265020` world positions via `003A19A0` → `0026A8E0`; fallback arms call `00265470`+`002EC2C0` or `002E64E0` | NOT EXERCISED · scope | static derivation only; the target-steer path is not driven |
| `002EAB80` is the push driver: gated `actor[+0x18]!=1` then kind-3 then `ctx[+0xDC]==0`; `002627C0` clones slot 0→1, `inc [+0xDC]`, `00269F90(ctx)`, `0026AE90(actor,0)`, `0026C120(actor,0)` | NOT EXERCISED · scope | static derivation only; the push op is not driven |
| `002EAAA0` is the pop driver: same `+0x18`/kind gates, then `ctx[+0xDC]!=0`; `dec [+0xDC]` (slot 0 was never overwritten — it is the saved pre-push state), `00269F90(ctx)`, then replays `sub[+0x62]&7` — 0 → `002EC2C0(actor,sub+0x10)`, 1 → `002EBFA0(actor,sub+0x10/0x14/0x18)`, else nothing — and always `002EC3F0`+`002E8EE0` | NOT EXERCISED · scope | static derivation only; the pop op is not driven |
| the push/pop caller side is a script op dispatch: `003DBDC0`→`00263230`(op==1) drives push; `003DB2A0`→`00263050`(op==4) drives pop only when `actor[+0xB]` bit 4 is set and clears that bit after | NOT EXERCISED · scope | static derivation only; the script op dispatchers are not driven |
| `002EC140` stamps resume shape 2: kind-3 gate, raw `{xmm1,xmm2}` into `sub+0x10`/`+0x14`, `+0x62 = (&0xFA) or 2`, then `0026A8E0`/`0026A870` apply and `0026A9C0`/`0026A950` zero | NOT EXERCISED · scope | static derivation only; the look-at writers are not driven |
| `002EC1C0` stamps resume shape 3: two-sided wrap (±π offset by arg sign, mod 2π) of `{xmm1,xmm2}` into `sub+0x10`/`+0x14`, `+0x62 = (&0xFB) or 3`, then `0026A8E0`/`0026A870` apply | NOT EXERCISED · scope | static derivation only; the look-at writers are not driven |
| the mode-4 timed turn interpolates `heading(t) = turn_start_heading(+0x38) + wrap(target_heading(+0x34) − +0x38) × min(turn_frame_index, turn_frames)/turn_frames`, then advances the frame index by 1; `0026C290` captures `+0x38` as the argument's two-sided wrap at arm time | NOT EXERCISED · scope | static derivation only; the mode-4 arm is not among this suite's driven entries |
| `+0x70`/`+0x74` are the two steer channels' wrapped targets (heading and aux/pitch): written only via wrap helpers `0026A8E0`/`0026A870`; the initiator `002EBE50` wraps `(+0x70 − ctx+0xB4)` against a mirror seeded from `ctx+0xA8` via `00265200`, derives `derived_turn_frames` from the residual, then snapshots both to `ctx+0xB4`/`ctx+0x224` | NOT EXERCISED · scope | static derivation only; the initiator paths are not driven |
| `+0x63` is `steer_arm_state` — the steer channel's armed-state byte: `002EBE50` stores its `edx` op verbatim and gates fresh-arm mirror reseeding on the byte being 0; the teardown/reset paths zero it in the same store sequence that clears `ctx+0xB4`/`ctx+0x224` | NOT EXERCISED · scope | static derivation only; the initiator and teardown paths are not driven |
| `+0x6C` is `initiator_turn_step` — the per-frame angular step the initiator divides the wrapped delta by to derive `derived_turn_frames` (`+0x60`): `max(1.0, abs(Δwrapped) / +0x6C)`; written by `0026AAD0` as the two-sided wrap of its argument times the rate global `[01DFE0BC]` — a rate-scaled step, not a bare residual | NOT EXERCISED · scope | static derivation only; the initiator and writer paths are not driven |
| `002EC3F0` is the steer dispatcher: it decodes two packed fields from `+0x62` — dispatch mode = bits 3–5 (`shr 3, &7`), resume shape = bits 0–2 (`&7`) — then tail-jumps one of six apply arms carrying `derived_turn_frames` as `xmm1` (shape ≤1: mode 1 → `002E7650`, mode 2 → `002E79A0`; shape 2: mode 1 → `002E7720`, mode 2 → `002E77F0`; shape 3: mode 1 → `002E78D0`, mode 2 → `002E7860`; the shape-2/3 arms also forward the `+0x10`/`+0x14` resume pair in `xmm2`/`xmm3`). `+0x6A` bit 0 is a one-shot latch that remaps mode 2 → mode 1 and is consumed (`&0xFE`) in the same pass | NOT EXERCISED · scope | static derivation only; the dispatcher and its apply arms are not driven |
| any runtime observation | OPEN QUESTION | none exists |

### `auto_status` — 10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md

| claim | status | note |
|---|---|---|
| the derived set is a pure function of its sources, never updated incrementally | **EXERCISED** | driven from empty and non-empty prior sets over both accumulation sources |
| the status space is 128 bits | **EXERCISED** | driven with every bit of the kind-1 mask set, which reaches bit 127 |
| the character's own row contributes 64 bits from two masks | **EXERCISED** | driven at all-ones, at the two ends of each mask, and at zero |
| each of the five equipment slots contributes at most one status, from row +0x1A, and 0xFF means none | **EXERCISED** | all five slots driven with distinct ids and one carrying the sentinel |
| an equipment row contributes only when its gate returns exactly 3 | **EXERCISED** | driven at gate 0 and 3 with the validity oracle both ways |
| the licence contribution walks ids 0 to 360 against the owned bits at +0x194 | **EXERCISED** | driven at ids 0 and 3, with the owned bit set and clear |
| a licence row contributes only when its gate returns exactly 2 | **EXERCISED** | driven at gate 1 and 2 |
| the licence lookup has no bounds check against the table's record count | NOT EXERCISED | the fixture's table is larger than any id the walk reaches, so nothing here stands past its end - driving that would read unmapped memory on both sides rather than compare |
| the apply is a DIFF, not a reapply | **EXERCISED** | driven from a non-empty prior set, where unchanged bits produce no call |
| the applier is called once per CHANGED bit, with 3 for an addition and 1 for a removal | **EXERCISED** | 255 applier calls compared with their arguments across the suite |
| the tail calls 002FEF30 exactly once | **EXERCISED** | it appears once per run in every trace |
| this function computes no stat contribution | NOT EXERCISED | a negative about code that is not here; nothing a run of this function can show |
| the entry takes a SECOND parameter, a flag word | **EXERCISED** | driven at 0, 1, 0x202 and 0xFFFF, and compared where it arrives - the applier's and the cascade's sixth argument |
| a kind-1 record accumulates from 128 bits at [unit + 0xE80] and never reads a definition row | **EXERCISED** | driven at kinds 0, 1 and 2 with both sources planted, so taking the wrong one shows |
| the definition row and the licence rows are reached through the authored-table lookup shape, resolving twice | **EXERCISED** | the resolver is NOT stubbed - its three real instructions run - and a failed resolve is driven on the definition lookup |
| the two definition masks are walked differently from each other | **EXERCISED** | driven at masks whose set bits differ between the halves, where a shared loop shape would put a bit in the wrong place |
| one licence node can grant EIGHT statuses | **EXERCISED** | driven with all eight present, with some 0xFFFF, and with all 0xFFFF |
| the function does not end at the applier: four further stages follow | **EXERCISED** | 36 cascade calls at mode 5, both copy directions, and all three clamps |
| a status change can lower current HP here rather than in the HP write | **EXERCISED** | driven with HP above the cap, at the freeze bit, at the doubling bit, and at HP 0 |
| the second half is gated on kind ONE, and every other kind lands on the clamps | **EXERCISED** | driven at kinds 0, 1 and 2; the control gating it on kind 0 failed |
| nothing writes the accumulation back into +0x78 | **EXERCISED** | the record's derived bytes are compared after every run; the control that copied the accumulation back failed |
| the spawn record and the stats record exchange FIVE bytes, in one direction chosen by a flag | **EXERCISED** | driven with the flag set, clear, and with no spawn record at all |
| the equipment gate receives the row ADDRESS, which is zero when the resolve failed | **EXERCISED** | driven with all three registry slots null, by a case that runs before any fixture reset |
| nothing observed at runtime | OPEN QUESTION | none exists |

### `battle_mode` — 00-Engine-Core-Runtime/Battle-Runtime-Mode/CONTRACT-battle-runtime-mode.md

| claim | status | note |
|---|---|---|
| the ladder's six tests, their order, and the two early returns | **EXERCISED** | all 16 flag nibbles driven against both callee answers; the order is what the pre-emption cases measure - flags 0b1111 returns 5 and not 4, 3, 2 or 1 |
| the flags word is `*(0x02EBF190) + 0x5B04` | **EXERCISED** | the harness plants the slot and the block and drives the word; a wrong offset reads the zero-filled page and returns 0 for every case |
| the ladder does not null-check the state pointer | NOT EXERCISED | driving it would fault the original rather than compare, which is the behaviour and not a result; the contract states it from the absence of a `test rax,rax` between the load and the use |
| the table-absent path returns 0, written as `0xFFF >> 15` | **EXERCISED** | driven with the slot null; the reconstruction writes the same shift rather than a literal 0 |
| the bound is unsigned, the row stride is 3, and the data starts at `+8` | **EXERCISED** | index at count-1, count, count+1 and -1, and only row `index` seeded - so a stride of 2 or 4 reads a zero row and disagrees |
| bit 0 is the summon and bit 1 the chocobo | NOT EXERCISED | a naming claim from the script verbs and their setters; nothing here can distinguish a bit's NAME, only its position |
| modes 4 and 5 are script-set and reachable only through thunks | NOT EXERCISED | a reachability claim about callers, which this fixture has none of |
| the six verbs and their arities | NOT EXERCISED · scope | the dispatch table, not these two functions |
| `geteventpartymode` returns `ladder() == 4`, so it is 0 while bit 3 is set | NOT EXERCISED | a different function; the ladder's own behaviour under both bits IS driven here and is what that wrapper would observe |
| the mode survives a transition and a save | NOT EXERCISED · scope | the capture and restore pair, out of this fixture's scope |
| the chocobo setter's asymmetric side effects | NOT EXERCISED · scope | the setter, not the ladder |
| mode 4 writes slot-map entries 0, 1 and 3 and mode 5 restores entry 3 | NOT EXERCISED | a consumer's behaviour, and the thinnest kind of claim to test from here |
| `*(0x02EBF190)` can be null only before the first save-image init — the slot is BSS-zero, the two writers `00238A92` (unconditional, `002EF650` tail) and `00233C33` (lazy fill in `00233C10`) both store the constant `021B290C` (`SaveImage_GetActiveBuffer()+0x4E68C`), and **no consumer can call the ladder while it is null**: the master tick `0022A580` dispatches on `byte[02064AD3]`, state 0 is exactly the boot frame `0022B6E0`, and the state-0 exit write `0022B74E` is the first instruction of the `0209273C==5` block that ends with `call 002EF650` (`0022B78B`) — leaving state 0 requires running the init in the same tick | NOT EXERCISED | an image-wide writer/caller census plus master-state ordering claim; the harness plants the slot itself and cannot speak to install ordering |
| any execution of this operation, isolated or live | **EXERCISED** | this suite is that execution for the two functions it drives, and it is isolated original-code rather than live |
| which entry-3 reader an event script relies on | NOT EXERCISED | answered 2026-09-22 statically: the party-read-in machine 0037B4D0 via the partyallread/partyallread2/summonread verb tasks; a reader-identity claim no ladder fixture can drive |

### `bazaar` — 12-Items-Equipment-Shops-License/CONTRACT-bazaar-unlock-and-purchase.md

| claim | status | note |
|---|---|---|
| the goods row index is the id minus 0xD000 | **EXERCISED** | purchase and the script path driven at 0xD000 and 0xD001 against a planted stride |
| the good's flag byte is at BattleSystemState + 0x59C8 + row | **EXERCISED** | the fixture plants and reads that byte through a LITERAL offset, not the subject's macro, so the offset is the thing under test |
| the flag byte and the sold tallies are both inside the save payload | NOT EXERCISED · scope | a containment claim about the save image; nothing here saves |
| a purchase clears bit 1 and never bit 0 | **EXERCISED** | driven from all four states of the two bits |
| a purchase zeroes all three recipe loots' sold tallies absolutely | **EXERCISED** | the three calls and their four arguments are compared; the WRITE itself is an oracle, so what 003008A0 does is not proved here |
| a failed row resolution does not abort the purchase | **EXERCISED** | a null registry and a zero resolver base, both with a page planted at address zero |
| a one-time good does not return after a save and reload | **EXERCISED** | the ARITHMETIC only: refresh, purchase, refresh, for a repeatable and a one-time row. The save round trip is not executed |
| the refresh predicate is: repeatable or never unlocked, not already available, **at least one threshold non-zero**, and three loot thresholds met | **EXERCISED** | each clause driven where it alone decides, and the third - a row requiring nothing - on the one line built for it |
| a script can set availability only for rows whose +0x14 bit 1 is set | **EXERCISED** | row flags driven at 0, 1, 2 and 3, so a mask widened to bit 0 is visible |
| script-set availability does not consult bit 0 | **EXERCISED** | the same rows with the flag byte's bit 0 set and clear |
| the purchase entry is 0030B180, and it is GATED before anything else | **EXERCISED** | the gate driven at both answers; a reconstruction without it differs on 140 of 215 lines |
| the gate's first argument is the bazaar CLASS NUMBER | **EXERCISED** | every gate call is compared as a trace line, arguments included |
| the purchase's state byte is derived inside the function, not passed in | **EXERCISED** | purchase driven at two ids against a multi-row flag array |
| refresh raises BOTH bits at once | **EXERCISED** | a reconstruction raising availability alone differs on 133 lines |
| the third loot's tally query passes a DEAD argument | **EXERCISED** | the kind argument is compared on every traced call, and it is 3 on all three |
| the class bounds check is a SIGNED compare against count - 1 | **EXERCISED** | driven at index == count - 1 and at a count of zero, which are the only places a stricter or unsigned reading disagrees |
| a tally query refuses in four different ways, and two of them are not the same | **EXERCISED** | all four driven - and the run is what shows the -1 and the 0 are indistinguishable through this predicate |
| every one of the three entry points reaches a NULL goods row and none tests it | **EXERCISED** | all three, by a null registry and by a zero resolver base; the fixture maps a page at zero and section 13 says what that does and does not prove |
| what the three scripted callees do | NOT EXERCISED | by construction: they are the oracles HERE. EXP-092 executed all sixteen bodies separately - a different instrument, and not this pilot's coverage to claim |
| flag byte bit 2 is the "newly unlocked" marker — written by `0030B630`, read by `0030B4B0`, bulk-marked by `0057B6F0`, cleared by `0056D370`, mirrored to UI record `+0x44` | NOT EXERCISED · scope | a whole-image displacement census plus body reads; the bit is not driven by this suite |
| `02EBF058` has exactly one writer — the `003845F0` relocation bind at `00236F6E`, unconditional — and `0020E600` is `ref + *(01F85530)`, so the §10 null path fires only in a goods-resource-absent state | NOT EXERCISED | a topology claim (writer census + resolver body), not the fault path itself; the fault arithmetic this bounds was already exercised above |
| nothing observed at runtime, and the containment argument carries one untested assumption | NOT EXERCISED | still true: this pilot is isolated original-code, not a running game |

### `binding_publish` — 15-Input/Binding-Profiles/CONTRACT-binding-profiles.md

| claim | status | note |
|---|---|---|
| ten operations, their entries and their signatures | NOT EXERCISED | this suite drives ONE of the ten, 00195DF0; the other nine are not called |
| the GFZ names two of these backwards | NOT EXERCISED | a naming claim about an annotation, not a behaviour a run can show |
| `00195DF0` builds at `01DF1738 + i*0x15C` from `01F80F90` and copies `0x15C` to `01F80130` | **EXERCISED** | this is the operation under test: all three runtime records, all three published records and the dirty flag compared byte for byte over 42 cases, with every mapped byte outside those regions laid over a sentinel fill so a stray write anywhere is caught |
| `001DFA70` compares a DWORD, not a byte | **EXERCISED** | 001DFA70 is NOT stubbed - eight bytes and a leaf, so it is mapped and executed and the pair-order decision is the shipped one. The suite found its own fixture writing a single byte into a sentinel page, making the compared dword 0x5A5A5A00 and swapping the keep case: the fixture was wrong, not the reconstruction |
| flat index = `profile * 0x1C + slot + {0, 0x10, 0x18}` | NOT EXERCISED | the flat index belongs to the assigner and the conflict scan; the publisher does not compute it |
| the conflict scan is global, bound `flat <= 0x53` | NOT EXERCISED · scope | 00196550 is not driven |
| a pressed control CLEARS its bit | NOT EXERCISED | the mask is written by the poll and the translator, neither of which is driven |
| the 35 ids at `01DF13E0` can never be bound | NOT EXERCISED · scope | the assigner 00198A00 is not driven |
| `00196FF0` does nothing unless `mgr[+0x39] != 0` | NOT EXERCISED · scope | the poll is not driven |
| `00198A00` returns 0, 1, 2 or 3 | NOT EXERCISED · scope | the assigner is not driven |
| the translator requires an already-initialised frame | NOT EXERCISED · scope | 00197160 is not driven |
| the read path resolves in a live process | NOT EXERCISED | live evidence from EXP-005 and EXP-006. This suite runs offline against the shipped bytes and neither reproduces nor tests it |
| the assignment and publication paths in a live process | OPEN QUESTION | section 15 records UNKNOWN. This suite executes the publication path in ISOLATION, which is a different class of evidence and does not close a live question |
| what the three banks ARE, and what `mgr[+0x39]`/`+0x3A`/`+0x3B` mean | OPEN QUESTION | section 15 records UNKNOWN - a question about meaning, with no stated behaviour to exercise |

### `body_pool` — 06-Movement-And-Navigation/CONTRACT-movement-body-pool.md

| claim | status | note |
|---|---|---|
| the pool is 128 bodies of 0x130 at 02B4E4C0 | NOT EXERCISED | the STRIDE is exercised - a fixture of eight at 0x130 resolves the wrong body under any other - but the EXTENT is not. 128 is computed from the free head's address, and a fixture of eight cannot reach it |
| the list links are 16-bit indices with 0xFFFF as null | **EXERCISED** | every link word is read back after every operation, and exhaustion drives the sentinel into both heads |
| a body carries its own index at +0x04, and release reads it rather than recomputing | **EXERCISED** | the self word is compared on every body after every operation; a reconstruction that recomputed the index from the pointer would still have to maintain this word to match |
| allocate moves a body from the free list to the ACTIVE list | **EXERCISED** | both heads and every link compared after each allocate, so a body that reached the caller without joining the active list shows |
| allocate returns NULL when the free list is empty | **EXERCISED** | allocation to exhaustion and one past it, on a pool of eight and on a pool of one |
| release unlinks from whichever list the body is on, then pushes onto the free list | **EXERCISED** | driven on the active head, a middle body and the tail, which take three different arms |
| release accepts a NULL body and does not guard a double release | **EXERCISED** | both driven; the double release is compared for what it actually does rather than avoided |
| any runtime observation | OPEN QUESTION | none exists |

### `character_publish` — 17-Presentation-Rendering/CONTRACT-character-transform-publish.md

| claim | status | note |
|---|---|---|
| the ready flag gates the whole operation | **EXERCISED** | driven at 0 and 1. At 0 the whole block must be unchanged - both banks, both scalar pairs and the sink buffer - and the accessor must not even be called, which the trace shows |
| the record array stride is 0x318 | **EXERCISED** | driven at index 0 and index 1, so a wrong stride writes into the wrong record and both are dumped |
| the bank is chosen by a byte behind a global | **EXERCISED** | the accessor is answered with a fixture object and its +0x1C driven at both values; every case runs at both |
| bank A is `+0x4C4` and takes the `== 0` branch | **EXERCISED** | compared inside one 0x180 span covering both banks, so writing A's bytes into B fails the same line a wrong base would |
| bank B is `+0x584` and is the fall-through | **EXERCISED** | same span, and a case publishes at both parities over one object so the bank NOT being written must survive |
| each bank is three 64-byte matrices | **EXERCISED** | three distinct source matrices planted and compared in place; a stride other than 64, or two swapped, changes the span |
| the scalar slots are four bytes apart between banks | **EXERCISED** | the record's first 0x20 bytes are compared, so publishing one bank's matrices beside the other bank's scalars is caught |
| the motion flag is a two-float zero test with NaN handling | **EXERCISED** | driven at (0,0), (0,x), (x,0), (NaN,0) and (0,NaN). The NaN cases are the ones the jp arms exist for, and without them a reconstruction writing a plain == 0 test passes everything |
| the flag argument is tested only for zero | **EXERCISED** | driven at 0, 1 and 12345; 1 and 12345 must publish the same dword, which is what makes this a test of the claim rather than of one value |
| two optional sinks publish the two flags before any matrix moves | **EXERCISED** | each driven present and absent independently and at two offsets, with the 64-byte buffer compared. This row did not exist in section 15 before this pilot |
| nothing observed live | OPEN QUESTION | none exists |

### `class_descriptor` — 22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/CONTRACT-phyre-class-descriptor.md

| claim | status | note |
|---|---|---|
| six circular intrusive lists at `+0x50`, `+0x60`, `+0x80`, `+0x90`, `+0xA0`, `+0xB0` | **EXERCISED** | the whole object is compared, and each list head and tail becomes the list's OWN ADDRESS - so the planted object base is part of the expected bytes and a list written at the wrong offset differs in sixteen of them. The unusual write ORDER (+0x60 last) is not separately observable, only the result |
| a list is empty when its head points at itself | **EXERCISED** | that is precisely what the reset writes, and the comparison is over those bytes; what is NOT driven is a NON-empty list being walked, which belongs to the destructor |
| the type name is a `char *` at `+0x30` | **EXERCISED** | the byte written at +0x30 is compared in every case; that the pointer is a STRING is 006388C0's claim and that function is not run here |
| `+0x30` is `[+0x138]` with bit 0 cleared, so `+0x138` is a tagged pointer | **EXERCISED** | six tagged values with bit 0 set and clear, including 0x7FFFFFFFFFFF and 1 - the claim the source page did not have at all, and the one two earlier versions of it got wrong |
| the sub-object at `+0x70` is released first, after the vftable is overwritten | NOT EXERCISED · scope | the destructor 00633390 is not driven by this pilot; section 16 records that as half the contract still unexecuted |
| the destructor runs TWO free-walks (`+0x90`, `+0xA0`) and then FOUR drain loops (`+0x80`, `+0x90`, `+0xA0`, `+0xB0`) that free nothing | NOT EXERCISED | the destructor is the subject of diff_class_descriptor_dtor.py; this pilot drives only the reset |
| a node in `+0x80` or `+0xB0` is never released, whatever its ownership bit | NOT EXERCISED | a destructor claim; the reset writes list HEADS and never a node |
| after the drains every walked head points at itself and every survivor is self-linked | NOT EXERCISED | a destructor claim - though the RESET leaves the heads in exactly that state, which is what makes an empty list recognisable to both |
| the vftable is written TWICE, with different constants | NOT EXERCISED | both writes belong to the destructor; the reset never touches +0x00 |
| `+0xE8` is a high-water mark wound back only when it is the topmost | NOT EXERCISED · scope | inside the destructor, which is not driven |
| the parent is at `+0x78`, and four fields are copied from it | **EXERCISED** | five parent values including 0x80000000 and 0xFFFFFFFF, comparing +0x38, +0x3C, +0x104 and the NEGATION into +0xF0; plus a null parent and a parent whose copy the guard suppresses |
| a list node is `{next, prev, ..., owned ptr at +0x18, flag at +0x20}`, and bit 0 of the flag gates BOTH the unlink and the two frees | NOT EXERCISED | the list NODES are only touched by the destructor 00633390, which this pilot does not run. The reset writes list HEADS and never a node |
| the walk advances the cursor before unlinking the current node | NOT EXERCISED | inside the destructor |
| six `test rax, rax` guards in `0063D550` are provably dead | NOT EXERCISED | they cannot be driven, which IS the claim - a lea of a non-null base is never null, so no input reaches the branch. The reconstruction omits them and agrees on every case |
| descriptors are `_aligned_malloc` storage freed by `_aligned_free` | NOT EXERCISED | an allocation claim; 0063D550 neither allocates nor frees |
| the deleting-destructor flag convention: bit 0 frees, bit 2 takes the CFG path | NOT EXERCISED · scope | 005847E0 is not driven |
| 4,557 generated reflection functions in 42 families, 1,149 deleting destructors | NOT EXERCISED | a whole-image census |
| any execution of any of this | **EXERCISED** | this suite is that execution for 0063D550, isolated original-code rather than live - and the row it replaces said none had been performed |
| what the six lists hold, what bit 0 tags, the descriptor's size, the `+0x100` guard, `0063E410` | OPEN QUESTION | the guard's BEHAVIOUR is driven - including at 0x8000, the one value that separates a 16-bit read from a mis-shifted one - but its MEANING is not, and neither are the other four |

### `class_descriptor_dtor` — 22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/CONTRACT-phyre-class-descriptor.md

| claim | status | note |
|---|---|---|
| six circular intrusive lists at `+0x50`, `+0x60`, `+0x80`, `+0x90`, `+0xA0`, `+0xB0` | **EXERCISED** | four of the six are driven here as free-walk or drain targets, with nodes seeded so the freed addresses name their list; +0x50 and +0x60 are driven only as UNTOUCHED, which is itself the claim |
| a list is empty when its head points at itself | **EXERCISED** | every case seeds empty lists that way and the drains leave every walked head that way; both directions are compared as bytes |
| the type name is a `char *` at `+0x30` | NOT EXERCISED | the destructor never touches +0x30 |
| `+0x30` is `[+0x138]` with bit 0 cleared, so `+0x138` is a tagged pointer | NOT EXERCISED | the reset pilot's claim, not this one's |
| the sub-object at `+0x70` is released first, after the vftable is overwritten | **EXERCISED** | 0063D640 is hooked and counted, and the entry vftable write precedes it in every case; what the sub-object destructor DOES is scripted and not claimed |
| the destructor runs TWO free-walks (`+0x90`, `+0xA0`) and then FOUR drain loops (`+0x80`, `+0x90`, `+0xA0`, `+0xB0`) that free nothing | **EXERCISED** | THE CASE THAT CORRECTED THE CONTRACT: one owned node in each of the four lists freed FOUR addresses where the previous reading predicted eight |
| a node in `+0x80` or `+0xB0` is never released, whatever its ownership bit | **EXERCISED** | driven directly - an OWNED node in +0x80 and in +0xB0, each still never freed |
| after the drains every walked head points at itself and every survivor is self-linked | **EXERCISED** | the object and the node heap are both compared byte for byte |
| the vftable is written TWICE, with different constants | **EXERCISED** | the EXIT constant is compared in the final object; the ENTRY one is overwritten before anything can observe it, which the campaign confirmed by leaving that mutant alive |
| `+0xE8` is a high-water mark wound back only when it is the topmost | **EXERCISED** | driven at equal, one below, one above, far away, and at counter values whose upper BYTES matter - the global is compared afterwards |
| the parent is at `+0x78`, and four fields are copied from it | NOT EXERCISED | the reset pilot's claim |
| a list node is `{next, prev, ..., owned ptr at +0x18, flag at +0x20}`, and bit 0 of the flag gates BOTH the unlink and the two frees | **EXERCISED** | an owned and an unowned node in the same list, both orders, plus a null owned pointer that must NOT count as a release |
| the walk advances the cursor before unlinking the current node | **EXERCISED** | implicitly - a walk that unlinked first would lose the chain and free fewer nodes; the three-owned-node case would drop to one |
| six `test rax, rax` guards in `0063D550` are provably dead | NOT EXERCISED | in the reset, and unreachable there |
| descriptors are `_aligned_malloc` storage freed by `_aligned_free` | **EXERCISED** | the FREE half: every release goes through 00584730, which is hooked. The ALLOCATION half is not driven |
| the deleting-destructor flag convention: bit 0 frees, bit 2 takes the CFG path | NOT EXERCISED · scope | 005847E0 is not driven |
| 4,557 generated reflection functions in 42 families, 1,149 deleting destructors | NOT EXERCISED | a whole-image census |
| any execution of any of this | **EXERCISED** | this suite and the reset pilot together are that execution |
| what the six lists hold, what bit 0 tags, the descriptor's size, the `+0x100` guard, `0063E410` | OPEN QUESTION | unchanged; the destructor tells us which lists are freed FROM, not what any of them holds |

### `coast_down` — 17-Presentation-Rendering/CONTRACT-coast-down-latch.md

| claim | status | note |
|---|---|---|
| the record is `pool + id*0x740` and the id is signed | **EXERCISED** | a negative index is driven and must land on the record before the pool centre, which the harness plants distinctly; a stride or a sign error moves it somewhere else |
| the decay is `0.83f` | **EXERCISED** | a 24-call glide compared as bit patterns, and the constant is re-read from the image on every run rather than inherited |
| the release threshold is `0.05f` and the boundary releases | **EXERCISED** | a cached speed chosen so the decayed value lands exactly on 0.05f, plus its two neighbours one ULP either side |
| five arming conditions | **EXERCISED** | each failed ALONE with the other four satisfied - which is what exposed that they do not share an exit: conditions 1 and 2 skip the cache and go straight to the tail |
| the motion blocks are 16-byte mirrors | **EXERCISED** | 48 bytes are compared after every call, not 32, so a block copy one byte too long spills into compared territory instead of into silence |
| the cache path clears the LIVE flags word | **EXERCISED** | driven with the live flag word planted as 1, 3 and 0xFFFF - the only arrangement in which that mask does anything at all. Every earlier case had it zero and a mutation of the constant survived |
| a NaN speed caches and a negative zero arms | **EXERCISED** | both driven with the other four arming conditions satisfied; the two cases differ only in the speed's bit pattern |
| the stop-frame counter is sign-extended then compared unsigned | **EXERCISED** | driven at -128, -1, 0, 29, 30, 31 and 127 against time bases 1, 2 and 5; the negative values arm, which is the wrap |
| there is a fourth stage after every path except servicing | **EXERCISED** | driven on both entry paths, through each subtype branch and each of its three early exits |
| `0020E600`'s result is dereferenced unchecked | NOT EXERCISED | deliberately. A NULL there is an access violation on both sides and a case that crashes both is not a test. What would exercise it is a harness that can observe a fault as an outcome, which this one cannot |
| what `0020E600` and `0051B9E0` are | NOT EXERCISED | answered statically outside this harness: 0020E600 is ImageAddress_ResolveRuntimePointer (three instructions, read whole) and 0051B9E0 is a 5-byte tail jump to 0051F240, PresentationEntryReferenceContainer_ResolveEntryById - CONTRACT-coast-down-latch section 7a, published 2026-09-13. Both remain supplied as oracles here |
| `+0x006` is the piece's owner-record link (`-1` = unattached, the latch precondition) and `+0x0CC` is the current render-event word (kind nibble + 12-bit index) | NOT EXERCISED · scope | the driver calls the latch function directly; it never runs a piece-attach commit (0042F2A0/0042F77A/0042F93B) or a detach store, and the event-selection writer 00424D80 is outside the harness - static census evidence only |
| nothing observed live | OPEN QUESTION | none exists |

### `commit_action` — 07-Combat-Action/CONTRACT-commit-action.md

| claim | status | note |
|---|---|---|
| two acceptance bands | **EXERCISED** | driven on both sides of all four bounds, including the unsigned wrap at 0x3FFF and 0x4167 |
| returns 1 on commit, 0 on refusal | **EXERCISED** | the return value is compared on every commit, and a refusal is checked to write nothing |
| the optional cancel precedes the band test, so a REFUSED commit still cancels | **EXERCISED** | driven with the fifth argument set at an id outside both bands: the cancel is in the trace and the verdict is 0 |
| the commitment block is 24 bytes and copied whole, with the low two bits of its first dword cleared | **EXERCISED** | driven over recognisable prior contents in both the block and the copy, and both are dumped |
| only a BAND ONE commit resets the target buffer and appends to it | **EXERCISED** | band one and band two driven back to back on the same world; the control that reset unconditionally failed on 607 of 659 lines |
| the attacker mask is a SET: nothing happens when the actor's bit is already present | **EXERCISED** | driven with the bit present and absent and with a full mask; the control that ored unconditionally failed |
| the mask bit is 1 << the actor's own slot byte, with the shift masked to five bits | **EXERCISED** | driven at slots 31, 32 and 33, where 32 and 33 must alias 0 and 1 |
| bit 22 of the dword at the unit's +0x00 vetoes the whole mask step | **EXERCISED** | driven set and clear, and against the neighbouring bit 21 so a wrong bit number shows |
| a commit whose query answers more than 1 writes the parameter onto every eligible unit of the actor's group | **EXERCISED** | driven at query 0, 1, 2 and 100, with NULL units, a unit with no stats record, a unit in another group, and the refusing statuses with the field override off and on |
| the walk re-reads the unit count on every pass | **EXERCISED** | driven at counts 0, 1, 2 and 3; the count appears once per pass in the trace |
| +0x770 survives exactly two ways | **EXERCISED** | driven across kinds 0, 1 and 2 with the id and parameter pair matching and not matching |
| when +0x770 is already zero the stats record is never read | **EXERCISED** | driven with a NULL stats pointer, which the original would fault on if it read it |
| the posture byte is re-picked only when bit 1 of +0x6B0 is set, and that bit is consumed | **EXERCISED** | driven at slots 0, 1, 3 and 255, with the bit set, clear, and set alongside its neighbours |
| `0x21E` is not a distinguished constant | NOT EXERCISED | an image-wide frequency claim about other functions; nothing in this pilot can bear on it |
| the unit count is re-read by a CALL on every pass, not merely re-loaded | **EXERCISED** | the walk is driven at counts 0, 1, 2 and 3 and the scripted 00236850 returns the fixture count each time, so a reconstruction that hoisted the bound would differ where the count changes. That the original fetches it by CALL rather than by load is read from 0030F928 |
| nothing observed live | OPEN QUESTION | none exists |

### `field_gate` — 04-Actor-Entity/CONTRACT-field-runtime-pass.md

| claim | status | note |
|---|---|---|
| slot block base `02098E10`, stride `0x288`, index sign-extended and unchecked | **EXERCISED** | the blocks are planted at that exact virtual address - the gate reaches them by a hard-coded lea - and slots -1, 5, 32 and 33 are driven, each landing on a block the fixture planted rather than on a refusal |
| the save-busy refusal returns 1 | **EXERCISED** | four non-zero busy values, and the CALL TRACE shows nothing else is called - which is the part of the claim that bytes cannot show |
| a **second** refusal, `+0x10` bit 0 clear, returns the same 1 | **EXERCISED** | driven, along with a THIRD way to return 1 that this contract had not listed: 003603C0's byte being non-zero |
| `+0x11` bit 0 is republished from `+0x10` bit 7 every frame | **EXERCISED** | all sixteen combinations of the source bit and the target byte. The 1 -> 0 cases are the only ones that separate a copy from a sticky OR, and they are in the set |
| `0026A5F0` RECURSES for slot 0, marking slots 1, 2 and 3 before itself | **EXERCISED** | the trace is compared entry by entry, so the ORDER is checked and not only the result: slot 0 makes fourteen entries, any other slot three |
| the mark's shift count is masked to five bits | **EXERCISED** | slots 32 and 33 driven against a ZEROED mark, so the bit is visible rather than lost in a filler word that already had it set |
| `0032F6E0` and `003603C0` sign-extend their bytes, and four of the six callees take NO argument | **EXERCISED** | bytes 0x80 and 0xFF drive the first; the argument-less claim comes from the trace, where 003603C0 is entered with the table base 0032F6E0 left in rcx |
| `002E1690` sets the byte `002E15D0` has just cleared | **EXERCISED** | the whole latch block is compared after every mark. That the clear is DEAD is the campaign's kind-A survivor rather than a case |
| slot 5's block CONTAINS the mark global | **EXERCISED** | the blocks are planted as ONE region spanning slots -1 through 5 precisely because the two overlap, and slot 5 is driven through the mark |
| the drive loop's two exits are different continuations | NOT EXERCISED · scope | inside the pass, past 0025DA5C. This pilot stops at the gate |
| the tail increments `+0x24` and `+0x38` and returns `r12d` | NOT EXERCISED · scope | the tail of the pass, not of the gate |
| bits 0–3 of the record's `+0x14` are never written, so the inner repeat is dead | NOT EXERCISED | a property of the drive loop |
| no iteration cap on the drive loop | NOT EXERCISED · scope | the drive loop is not entered |
| `02099D78` is null two ways | NOT EXERCISED · scope | the publish is past the gate |
| `[rbx+0x20]` is the actor count and is folded by AND twice | NOT EXERCISED | read by the drive loop, not by the gate |
| the four-iteration loop walks the party roster at `0209A1F0` | NOT EXERCISED · scope | past the gate |
| the wait dispatch marks the WAIT SLOT's `+0x14`, not the record's | NOT EXERCISED · scope | past the gate |
| the entry gate executed in isolation | **EXERCISED** | THIS PILOT IS THAT EXECUTION - 54 cases, 0 mismatches, and nothing scripted |
| any execution of the PASS, or any live observation | NOT EXERCISED · scope | the first 120 bytes of 1,297 are executed and the rest is not. This row is why section 13 does not call the contract validated |
| what `+0x14` bit 5 means | NOT EXERCISED | FP-1, and no execution of the gate can reach it - the gate never touches +0x14 |
| `022C6D20[m]` has **no clear anywhere in the image** | NOT EXERCISED · scope | a universal negative over the whole image, measured four ways in the contract; this pilot executes the gate only, and a gate that never clears the mark says nothing about the other 1,177 bytes of the pass or any other function |
| the pass's request needs **all four** of no-save, `+0x13 != 0` or `+0x10` bit 0, `+0x11` bit 3 clear, and the byte | **EXERCISED** | each condition is failed alone and the mark is compared: save-busy at four values, +0x10 bit 0 clear with +0x13 set, +0x11 bit 3 set, and the slot byte 0 (cases() - "save-busy", "taken by +0x13", "+0x11 bit 3 refuses the mark", "the slot byte is 0 - no mark") |
| the one-shot behaviour lives in the block bits, not the byte | NOT EXERCISED · scope | a set/clear site census across the image (0026D305, 00262DA8, 003303DF, 003306AF, 0032F9AA); none of those sites is inside the gate this pilot runs |
| whether a **re-loaded** manager whose mark is still set is unloaded on the next pass | OPEN QUESTION | UNKNOWN in the contract and routed live as OPUS-REQ-ASTRA-MGRMARK-RELOAD; there is nothing to exercise |
| what `+0x10` bit 0 means — disabled, uninitialised, or other | NOT EXERCISED | FRP-3, a writer/reader census claim (the slot live flag): the pilot executes the gate, which reads the bit but proves nothing about who writes it or what the state means |

### `field_music` — 18-Audio/CONTRACT-field-music-selection.md

| claim | status | note |
|---|---|---|
| Signature and return convention | **EXERCISED** | field id in `rcx`, signed 32-bit result in `eax`, on both sides of every case |
| Table layout, page stride 128, absolute page addresses | **EXERCISED** | `build_table` lays pages out at stride 128 with absolute `page[]` addresses, and both sides are handed the image at the SAME virtual address so the absolute entries mean the same thing |
| Run header 11/5 split, stride `4 + 3*count` | **EXERCISED** | runs packed `(start & 0x7FF) | (length << 11)`, `4 + 3*count` bytes each, counts 0/1/2/5 |
| Ladder takes the last threshold passed | **EXERCISED** | thresholds accumulate inside a run and progress is drawn across them |
| What fills the table | NOT EXERCISED | EXP-008 captured MUS0 contents, not their producer. The differential substitutes that image and cannot test its writer, binding, ownership or lifetime (DG-1) |
| The four callers of `003EAA70` | NOT EXERCISED | this suite drives 003EAA70 itself, at its own virtual address, and never enters it from a caller. The four edges are a call-graph reading and stay one |
| 291 runs, 48 with a ladder | NOT EXERCISED | a statistic over the SHIPPED authored file. Every table this suite runs is built here, to reach branches a shipped table might never contain, so nothing here re-measures it - which is what section 15's own 'not re-measured here' says |
| Track `0` folds to `-1` | **EXERCISED** | the track byte is drawn from a set containing 0, and the -1 outcomes are counted |
| Progress is compared as **signed 16-bit** | **EXERCISED** | progress values include 40000 and 65535, above the signed 16-bit boundary, against thresholds up to 0xFFFF -- the one place the signedness is observable |
| Writes no state | **EXERCISED** | the --real-table run re-reads the WHOLE table image and the table pointer after the call and counts any changed byte -- 80 of 400 cases sampled, 0 changed. It proves nothing was written to the pages the function can address; a store outside them would have faulted and been reported as an emulation error |
| Who writes and binds the table at runtime | NOT EXERCISED | the loader path 0051ED10 and the rebase callback 003EAB90 are read, not run: this suite hands both sides a table already in memory and starts after binding has happened |
| The table's lifetime after binding — release, reload on a language change, reuse of the block | OPEN QUESTION | section 15 records this as UNKNOWN. There is no stated behaviour to exercise, only a question |

### `field_record` — 03-World-Area-Field/CONTRACT-field-record-accessors.md

| claim | status | note |
|---|---|---|
| the shared prologue is identical in all seven | **EXERCISED** | all seven run on every case, and the null/out-of-range/in-range branches of the prologue are each reached by cases built for them |
| the bound is an UNSIGNED compare against the count | **EXERCISED** | ids 0x80000000 and 0xFFFFFFFF are rejected exactly like 4 against a 4-record table; a signed compare would accept them and index far outside |
| the record is three bytes and the u16 is composed, not loaded | **EXERCISED** | records are planted at a 3-byte stride and every accessor's answer depends on the stride being right; a 2- or 4-byte stride shifts every case |
| the failure constants differ per accessor | **EXERCISED** | the null-table and out-of-range cases compare all seven answers at once - and this is the check that falsified §10's row for 00377700, which returns 1 and not 0 |
| `003779F0`'s `0xFFF` is an authored sentinel, not only a failure value | **EXERCISED** | a record containing 0xFFF is planted alongside a null table; both return -1, which is the indistinguishability §10 describes |
| the save override on bits 12–13 REPLACES rather than merges | **EXERCISED** | the override is driven over all four values against a record whose authored bits 12-13 are 3, so a merge and a replacement disagree on every case rather than on some |
| who consumes each accessor | NOT EXERCISED | a caller census settles it and a census is not an execution. What would exercise it is a harness that drives the consumers, which needs the CombatAction and Status state this one does not build |

### `flag_banks` — 14-Story-Event-Quest-Hunt/CONTRACT-persistent-flag-banks.md

| claim | status | note |
|---|---|---|
| six banks, offsets and sizes | **EXERCISED** | all eleven accessors over ids straddling every bank bound, with the whole `0x1538` payload compared -- a wrong base or a wrong size mismatches |
| the two routes, re-counted here | PARTIAL | `002EF2B0` and `002EF640` are both mapped and executed as shipped, so both routes RUN. Their call-site census (121 and 40) is a static count no differential can execute |
| payload is `0x1538` bytes | **EXERCISED** | `PAYLOAD_BYTES = 0x1538` is compared in full after every case |
| bit arithmetic identical in all six | **EXERCISED** | all eleven accessors against zero, ones and pseudo-random payloads, so a set that sets and a clear that clears are both visible |
| encoded id: bit 14 selects, 0/1 hardwired | **EXERCISED** | `0032A8A0` is op 11 since 2026-09-08: 87 encoded ids x 3 payloads = 261 comparisons, and **42 of the 87 carry bit 14**, so BOTH arms of the selection are taken. The schedule at 00377970 is stubbed with a sentinel both sides answer with -- the SELECTION is what the claim is about, not what the schedule computes |
| the schedule is a parity | NOT EXERCISED | `00377970` is not reimplemented and not emulated |
| new game applies an authored list | NOT EXERCISED · scope | `002EF2D0`'s memset and tail-jump to `00379160` are never run |
| the two shipped files and their sizes | NOT EXERCISED | a file-system fact about the two `.fst` files; nothing here opens one |
| the two shipped lists' ids — `mapjumpgroupinit.bin` carries 53 (`0x0056`–`0x0158`, all in `SetPrimary` range); `eventmemorylist.bin` carries 8 including `0x0000`, consumed by membership predicate `00377440`, not a setter | NOT EXERCISED | authored-data contents of two shipped files; the fixture synthesises its own payload and never reads the shipped lists |
| four `Bank64` accessors accept negatives | **EXERCISED** | 13 hand-chosen negative ids plus random negatives across all four guard shapes, and the run prints which accessors accepted them |
| a negative id writes before the bank | **EXERCISED** | the whole payload is compared INCLUDING every offset below a bank base, and the run reports the negative ids that wrote outside their bank |
| the only paths into a `Bank64` accessor are six verb result-callbacks (verbs `0x2F8`–`0x2FD`), each passing a raw `00267E10` pop unmasked — and zero authored call sites for all six verbs exist across 1,114 decoded scripts | NOT EXERCISED | a shipped-corpus claim, not an accessor property - the fixture DOES pass negatives, which is exactly the behaviour this claim bounds as unreachable from authored data |
| the `+0x1394`–`+0x13B3` gap has no accessor by any route, and `+0x1534` is the saved music-override id (gated by `+0x1063` bit `0x40`), `+0x1535` is a written-only byte, `+0x1536`/`+0x1537` are untouched tail | NOT EXERCISED | an access-census claim about the shipped image; the fixture exercises the accessors it contains but never reads the payload tail fields nor enumerates callers |
| `Bank2048` is the NPC-name-reveal bank with real engine consumers; `Bank64A`/`Bank64B` are script-facing only (six `shutoral*` verb callbacks, zero authored call sites); hunts are script conventions over these banks while the bestiary is a separate native 512-byte block at payload `+0xB404` keyed by class row `+0x52` | NOT EXERCISED | a caller-census and authored-data claim about the shipped image; the fixture exercises accessor semantics, not who calls them or where the bestiary lives |
| any runtime observation | OPEN QUESTION | none exists |

### `frame_gate` — 00-Engine-Core-Runtime/CONTRACT-per-frame-update-gate.md

| claim | status | note |
|---|---|---|
| the enable word is at 01E0C464 and gates sixteen groups | **EXERCISED** | each of the sixteen test sites is reached by driving its bit alone, and the resulting traces partition the twenty-three callees between them |
| the function tests TWO objects, and only sixteen of its eighteen tests are the gate | PARTIAL | RE-GRADED 2026-09-18 (OPUS) from NOT EXERCISED, whose reason this suite own script refutes. It said the pilot "does not drive the second object at [rbx+0x10F68]". It does, and both of that object tests gate observably: with the enable at 4 and PTR 10F00 set, flags 0 gives 28C4C0 28C4B0 while flags 8 gives 2917E0 first - and with the enable at 0x100, flags 0 gives an EMPTY trace while flags 0x100 gives 3F8EC0(+A0). Two different traces from the same enable word, so the two tests on the second object are exercised rather than asserted. The reason also said "nothing here establishes what that object is"; it is now declared in the type store as ManagerSingleton0209BE80, 0x10FD0 bytes, allocated at 0028F8CF and published to 0209BE80, whose +0x10F68 is this very flag word. PARTIAL RATHER THAN EXERCISED because the other half of the claim is a COUNT - eighteen test sites, sixteen of them the gate - and an enumeration of a function test sites is a census of its body that no execution establishes, however many traces differ. |
| eight sites test it as a byte and eight as a dword | **EXERCISED** | bits 8 to 15 are driven individually and each produces its group; under a uint8 reading none of them would, so the width claim fails loudly rather than subtly |
| bit 4 is never tested and bit 1 is tested twice | **EXERCISED** | bit 4 alone must produce an EMPTY trace and bit 1 alone must produce two groups separated by the sites between them. This row did not exist before this pilot |
| the first argument gates bit 1's second group | **EXERCISED** | bit 1 driven at arg0 = 0 and arg0 = 1; the traces must differ by exactly that group. This row did not exist before this pilot |
| the last group is a tail jump | **EXERCISED** | bit 11 combined with every other bit: its callee must be last in every trace it appears in |
| each group's inner conditions are its own | **EXERCISED** | every inner pointer is driven null and non-null, and the two flag-bit tests at +0x10F68 are driven at both values, independently of the enable bit that reaches them |
| any runtime observation | OPEN QUESTION | none exists |
| the sixteen tests are the word's only accessors | NOT EXERCISED | an image-wide rip-relative census over all 35,713 .pdata bodies - exactly 16 references, all the pump's tests. A census is not an execution; nothing a trace drives would distinguish 'bit 4 dead' from 'bit 4 live-but-untested', and this suite already proved the in-pump half by driving bit 4 alone to an empty trace |
| the two `0x0002` groups are two authored `if`s, not one group | NOT EXERCISED | a claim about authorship proven from structure - out-of-sort position, the extra dil&1 gate, the caller's own 001EDE80 call at 00250896 - not from anything the harness can drive; the runtime distinction is empty because the word is never written |

### `gambit_walk` — 09-Combat-AI-And-Gambits/CONTRACT-gambit-walk.md

| claim | status | note |
|---|---|---|
| null set returns 0 | **EXERCISED** | driven, and the trace must be empty - a walk that offered a record before noticing the null set would return 0 and still be wrong |
| the no-target sentinel is `0xFFFF` and the parameter slot starts at 0 | **EXERCISED** | only because the evaluator has a SILENT mode that matches while writing neither the target nor the parameter. With an evaluator that always writes them the initial values are never observed at all - this row was declared exercised on that mistake for one round, and a mutation of the parameter's initial value survived every case until the silent mode existed |
| the header is per-subgroup count bytes | **EXERCISED** | headers with non-zero counts before the target subgroup are driven at even and odd indices, so both the unrolled pair loop and the odd leftover are reached |
| records begin at `+0x20`, stride 24 | **EXERCISED** | records are planted at a 24-byte stride and every traced record index depends on it; a wrong stride or a wrong base moves every offered record |
| an empty subgroup walks nothing | **EXERCISED** | a zero count byte at the subgroup index returns 0 with an EMPTY trace - no callee is offered anything, which the trace shows and a return value would not |
| the count byte is re-read on every iteration | **EXERCISED** | the evaluator oracle rewrites the count byte mid-walk, shorter and longer; a latched reconstruction diverges on both |
| the two record resume bits are tested against different conditions | **EXERCISED** | 0x40, 0x80 and the context's 0x4000 are driven in combination, including the two cases that separate `resuming` from `resume_mode`: mode set with no context, and mode set with a context lacking 0x4000 where the first record does NOT opt in |
| reaching the resume point returns 1 without evaluating it | **EXERCISED** | the context pointer is planted equal to a record address; the trace must stop before that record and must not contain an evaluate for it |
| both the evaluation and the commit must succeed | **EXERCISED** | scripted so that an early record matches and fails to commit while a later one succeeds - the arrangement a reconstruction treating a match as a commitment gets wrong |
| there is a third call on the success path | **EXERCISED** | driven with resume mode set and +0x714 both at and away from the sentinel; caught on the TRACE only, because the return value is identical either way |
| the subgroup index is sign-extended and never bounds-checked | **EXERCISED** | a negative index reads a planted count byte from in front of the header, and the harness maps the same bytes there so both sides read the same thing rather than faulting |
| at most twelve header bytes are counts; `subgroupIndex` cannot exceed 11 | NOT EXERCISED | static bound from the +0x6B5 writer census (four touchers, max stored value 11) and the sole caller's argument shapes - the suite can drive any index it plants, but no replay proves what the shipped writers can produce |
| `record + 0x04` is the record's whole behaviour flags word — every shipped bit has a named reader | NOT EXERCISED | the walk reads only 0x40/0x80; the other readers (locomotion step, timeout check, evaluator modes) are outside this replay entirely |
| what `004697C0` does | OPEN QUESTION | not established |
| nothing observed live | OPEN QUESTION | none exists |

### `group_completion` — 05-Spawn-Encounter-Lifecycle/CONTRACT-group-completion-and-respawn.md

| claim | status | note |
|---|---|---|
| record stride `0x250`, base `*(char**)0x0208E690` | NOT EXERCISED | this suite plants its own unit block at its own stride and never reads that global; the shipped record table is not involved |
| ledger 64 × 24 at `0x02EC13C0` | **EXERCISED** | the ledger is mapped at exactly that base, stride and count, and compared byte for byte. The region is deliberately truncated one entry short so the last qword read and write finish on the final byte - the only place the 8-byte bound can be wrong |
| completion is a mask test | **EXERCISED** | the return of every call is compared, including repeated calls on an already complete mask |
| elapsed is in **seconds** | NOT EXERCISED | no elapsed value is read or written on this path |
| the three readers are script-only | NOT EXERCISED | a call-graph claim; this suite enters 00306F00 directly and never through a reader |
| the `js` arm is unreachable | NOT EXERCISED | unreachability is a claim about ALL inputs and this suite samples. That the arm never ran in these cases is not evidence that it cannot |
| the ledger is BSS | NOT EXERCISED | a section property of the image, not a behaviour any run can show |
| `00306E60` writes `memberMask`, add/remove by slot, dead bit always cleared | NOT EXERCISED | a different function; only 00306F00 is driven |
| exactly six functions address the ledger | NOT EXERCISED | a call-graph claim |
| `+0xE98`/`+0xE99` have one byte writer | NOT EXERCISED | this suite READS both as unit inputs; the claim is about the writer SET, which no run of one function can establish |
| verb `0x3030` is the add caller | NOT EXERCISED | a caller claim |
| range retire is the remove caller | NOT EXERCISED | a caller claim |
| the reset zeroes both masks | NOT EXERCISED · scope | the reset is a different function and is not driven |
| the reset clears flag **bit 0 only**, preserving bits 1–7 | **EXERCISED** | the FNV-1a digest covers every byte of every region, so a reconstruction that cleared any other bit of the flags byte changes the digest and fails. Exercised FOR THIS PATH: it says what 00306F00 does to the byte, not what the rest of the image does to it |
| no instruction in the image touches any bit of the flags byte but bit 0 | NOT EXERCISED | a whole-image static claim, and a differential harness over one function cannot bear on it either way. It is a census result and has to be re-established by a census; passing this suite is not evidence for it. Recorded here so the distinction from the row above - same byte, same bit, utterly different scope - is not lost |
| bit 47 is touched at four sites only | NOT EXERCISED | a static site count |
| the deferred route inside `003250F0`: `0x2007/8/C/E` → `00307110` | NOT EXERCISED · scope | 003250F0 is not driven; the dispatch callee is a counted stub here |
| ~~`003250F0` has no static caller of any enumerated form~~ **REFUTED 2026-09-16 (FABLE)** | OPEN QUESTION | REFUTED 2026-09-16 by FABLE: 003250F0 IS reached, by `jne` from `002E70A0` - the sweep behind this claim enumerated `E8`, `E9` and both `LEA` encodings and omitted `0F 8x rel32`. Nothing is left to exercise, because the claim is FALSE rather than undriven, which is why this is OPEN QUESTION and not NOT EXERCISED. The "handler table has no reader" inference it briefly rested on was itself refuted (EE-12, 2026-09-19; re-verified 2026-09-22): readers index their own slots, not the base - call [02CA4430]/[02CA4440]/[02CA4470] reach all three handlers. THE PARITY REASON THIS ROW USED TO CARRY WAS TRUE AND IS THE POINT: "a negative over the call graph; no run establishes an absence" is exactly why a differential suite could never have caught this. A static sweep did, by finding the encoding the first sweep had left out. |
| the flag is consumed per frame into table slot 3 | NOT EXERCISED | the per-frame consumer is outside this function |
| no one-shot in helper or caller | NOT EXERCISED · scope | a claim about the caller, which is not driven |
| script-side order `(group, mode)` | NOT EXERCISED | script-side, and section 15 records it as PROBABLE rather than proven |
| the `+0xF6` word is the record's script-assigned entry-group index (the bkei), written by verb `00BE` `setentrygroupall` and zeroed at init | NOT EXERCISED | a provenance claim about which functions write the word - this suite drives the 00306F00 mask path and cannot bear on the writer set |
| group `0` is the not-a-member sentinel — both ledger paths gate on `+0xE98` before indexing, so no group-0 completion can post | NOT EXERCISED | the group!=0 gates live in 00306E60/00306F00's entry block and the corpus census is authored data - the fixture enters mid-function and no run can bear on the corpus side |
| any runtime observation | OPEN QUESTION | none exists |

### `hp_write` — 08-Combat-Formula/CONTRACT-hp-write-and-lethal-transition.md

| claim | status | note |
|---|---|---|
| four parameters, all in registers | **EXERCISED** | the original is called with four and the stack above the shadow space is planted with 0xCD, so a fifth or sixth argument would reach the status change and the kill hook and diverge |
| the outcome branch is on the sign of the delta, not on isHeal | **EXERCISED** | driven at delta 0 with and without bit 5, above the floor and on it; the control that restored the isHeal reading failed on exactly that case |
| the dead event pair is inverted relative to the alive pair | **EXERCISED** | both variants driven on both the alive and the dead path, and all five event ids observed |
| both records are mapped to units and may be null | **EXERCISED** | driven with no source record, with a source record owning no unit, and with no target unit |
| gate 3 skips only the store, and is asked only for a non-positive delta with bit 0 clear | **EXERCISED** | driven refusing at both signs of the delta and with bit 0 set: the publishers are in the trace, the store is not, and on a heal the call itself is absent |
| the store is the only HP write | **EXERCISED** | the record's HP is compared after every command, including the paths that return early |
| the floor is a unit field | **EXERCISED** | driven at a non-zero floor, a negative floor, and with no unit at all |
| damage landing exactly on the floor is death | **EXERCISED** | driven at the floor and one point above it, on a non-zero floor |
| status bit 16 freezes at max(old,1) | **EXERCISED** | driven at old 0, where the cap is 1 and not 0, and at old 150 |
| status bit 28 doubles the cap | **EXERCISED** | driven set and clear, and from the second status word to show the two are OR'd |
| the variant bit comes from the source's buffer | **EXERCISED** | driven with the search failing and at three entry indices with the bit set and clear |
| a group completion suppresses the death event | **EXERCISED** | driven with the completion answering 1, on a plain kill and on a spawn-backed one |
| the spawn counter and the seconds field are written only for a spawn-backed target | **EXERCISED** | driven with the kind byte set and clear, with the unit's record pointer NULL, and with it pointing at a different record than the one the call was given |
| the seconds field is frames divided by (int)(scale × 30) | **EXERCISED** | driven at three scales, including one that halves the divisor and one that doubles it |
| the predicate is the engine's UNIVERSAL downed-combatant test, not a rule with two ends | NOT EXERCISED · scope | a static census over the whole image - 173 instructions mention 0x80000003, about 150 of them in battle, AI, menu, enmity, reward, perception and party code. This pilot drives ONE of those sites, the one inside 00300530, and nothing establishes the other 172 by running them |
| the override is `00377C20 FieldData_GetActiveFieldRecordBit15` | PARTIAL | the pilot reaches the guard, but 00377C20 is a SCRIPTED CALLEE here - a stub is not proof of its native effects. What the suite establishes is that the guard calls it and bails when it returns zero, not what the field record's bit 15 actually is in any session |
| that override returns `0` — deny — whenever the field record table is absent or the index is out of range | PARTIAL | 00377C20 is a scripted callee in this pilot, so the suite shows only that the guard bails on a zero return - not what produces the zero. That the failure path is 0xFFF >> 15, and that 110 functions across 16 subsystems reach it, is read from the bytes and from the field-accessors contract |
| the same 0x80000003 mask with the same bit-15 override guards the gambit condition evaluation | NOT EXERCISED · scope | it is a claim about 00301531, a different function; this pilot executes 00300530 and its thunk and nothing else |
| nothing observed live | OPEN QUESTION | none exists |

### `inventory_query` — 12-Items-Equipment-Shops-License/CONTRACT-inventory-class-storage.md

| claim | status | note |
|---|---|---|
| an encoded id is a class in the top nibble and a twelve-bit index | **EXERCISED** | driven at class 0x0E and 0x0F and at index 0 and 0xFFF, on all three entry points |
| the descriptor table is at 01EEBCC0 with 0x58 bytes per row | **EXERCISED** | sixteen rows are planted with distinguishable arrays, so a wrong stride reads a neighbour |
| the class reader returns the dword at +0x38 and rejects a class above 0x0E | **EXERCISED** | driven on both sides of the bound, with a planted +0x38 that is not the class number |
| neither query bounds the class or the index | **EXERCISED** | class 0x0F is driven through all three, where the reader returns -1 and both queries answer from row 15 instead |
| the packed word is ten bits of total and six of reserved, and kind 0 is their difference | **EXERCISED** | words are planted to make the three answers distinct, including words whose difference is negative - which is what corrected this claim |
| kind 3 of the packed query reads the byte array at +0x20 | **EXERCISED** | the byte array is planted with values that differ from the word array at the same index |
| the bitset is a uint16 array at +0x08 for kinds 0 and 1, a byte array at +0x20 for kind 3 and at +0x30 for kind 4 | **EXERCISED** | driven at indices that cross both a byte and a word boundary, where the two shapes disagree |
| kind 2 and every unhandled kind answer 0, and so does a NULL array pointer | **EXERCISED** | every kind is driven against each of the three pointers nulled in turn |
| the byte-bitset paths carry a signed-division correction the 0xFFF mask makes unreachable | **EXERCISED** | reproduced as written and driven across the byte paths; the mutation campaign then showed all three mutants of the correction compile byte-identical, which is the unreachability |
| the index is rejected against +0x3C as a signed compare, so a class with itemCount 0 rejects every id | NOT EXERCISED | that test is in the validator at 00309F51, which this pilot does not execute |
| +0x10 is an element count, not an item count, and is ceil(+0x3C / 16) for every bitset class | NOT EXERCISED | nothing on the read side consults +0x10; only the clear-all loop does, and it is not run |
| the stored count is clamped to 99 in the writer, not in the field | NOT EXERCISED | the clamp is in the packed mutator 002FD150; this pilot is the read side |
| dispatch is per class through the handler pointer at +0x50, and **SEVEN** of the fifteen rows carry NULL | NOT EXERCISED | the three bodies are called directly here, not through the descriptor. The count itself is read out of .data - the pass that corrected it from four to seven read the table, it did not run it |
| four rows declare items and still have no handler — 9, 10, 13 and 14 | NOT EXERCISED | the same .data read. What the suite DOES exercise is the consequence - a NULL handler pointer answers the default - which is the claim above about kind 2 and unhandled kinds |
| all three storage pointers are NULL in the image and are bound at runtime | NOT EXERCISED | the fixture plants them; who binds them at runtime is the contract's open question |
| any runtime observation | OPEN QUESTION | none exists |

### `lua_header` — 23-Third-Party-Libraries/Lua-Core/CONTRACT-lua-chunk-loader.md

| claim | status | note |
|---|---|---|
| the expected header is 1B 4C 75 61 52 00 01 04 08 04 04 00 19 93 0D 0A 1A 0A | **EXERCISED** | the accepted case drives exactly these bytes, and every single-byte deviation drives a rejection, so any wrong byte in the expected set changes a verdict |
| byte 0 is planted, not read: eighteen are built, seventeen are read | **EXERCISED** | the read LENGTH is compared on every case, and a stream is driven whose first supplied byte is wrong - which must be rejected as `not a`, proving byte 1 IS read and compared while byte 0 is neither |
| all eighteen bytes are compared | **EXERCISED** | a deviation is driven in each of the three compared groups - bytes 0-7, 8-15 and 16-17 - and the last group is reachable only because the tail is compared at all |
| sizeof(lua_Number) in this build is 4, so a stock x64 luac chunk is rejected | **EXERCISED** | byte 10 driven at 8, the value a desktop toolchain emits; it must reject, and specifically as `incompatible` rather than `corrupted` |
| the five rejections are selected by exact byte ranges | **EXERCISED** | each of truncated, not a, version mismatch in, corrupted and incompatible is reached by the range named for it, and `corrupted` is shown to be reachable ONLY by a tail-only difference |
| any runtime observation | OPEN QUESTION | none exists |

### `manager_slot` — 04-Actor-Entity/CONTRACT-manager-slot-entry-tables.md

| claim | status | note |
|---|---|---|
| the 24-byte record stride | **EXERCISED** | every entry index is bound and the whole slot compared, so a wrong stride moves every write |
| the four-entry tables tile 0x110..0x1D0 | **EXERCISED** | binding entry 3 on side A and entry 0 on side B writes adjacent regions; the full dump shows they do not overlap and that nothing lies between them |
| the entry index is rejected by an UNSIGNED compare | **EXERCISED** | driven at 4 and at 0xFFFFFFFF on both sides; a signed test would accept the second |
| bind requires a non-negative record index below the count | **EXERCISED** | driven at -1, at 0 and at the count on both sides, each failing or passing alone. Zero was added after a mutation of the signed guard to `< 1` survived a whole campaign: the boundary the row asserts had no case standing on it |
| the definition pointer must be non-null | **EXERCISED** | driven with each side's pointer null in turn, and it is one of the three cases where the SIDES DIFFER in whether a callee ran |
| both sides compute the SAME value — `(x >= 0) ? x : 0` | **EXERCISED** | the suite drives a negative fifth argument on both sides and compares the whole slot, so a value difference would show. What it CANNOT show is 005C5230 being a three-byte stub - that is read from the bytes, and it is why the two mechanisms agree |
| the two sides validate the record index differently | PARTIAL | both sides are driven at a negative record index and at one past the count, and both refuse - so the BEHAVIOUR is exercised. That A does it in one unsigned compare and B in a sign test plus an unsigned compare is read from the bytes; no observable separates them |
| side A clamps a negative fifth argument and side B resolves it | **EXERCISED** | both driven with the same negative value; the resulting entry +0x04 and the trace differ |
| side B resolves BEFORE validating and side A clamps after | **EXERCISED** | the refused-input cases: neither side writes anything, and only the trace separates them - this row is why the suite compares a trace at all |
| the reverse-lookup subscript is unbounded | **EXERCISED** | a fifth argument large enough to write past the slot, with 64 planted guard bytes compared |
| `entry+0x0C` is the channel playback clock, `entry+0x10` the rate multiplier | NOT EXERCISED | static claim added 2026-09-22 (SWE2-CONTRACT): the consumers are the per-frame ticks 003DA050/003DCFB0 and the cameraratio setters 003DA2D0/003DD1F0, none of which this suite replays - it drives only the eight table operations |
| side A is the camera-shot table, side B the camera-shake table | NOT EXERCISED | static claim added 2026-09-22 (SWE2-CONTRACT): an E8/E9 caller census (13 sites, all verb handlers) and the 0026CE00/0026D3A0 setter bodies - the suite drives the table operations, not the verb dispatch that names the sides |
| `lookupIndex` exceeds 1 in shipped play | NOT EXERCISED | the mechanism half (unbounded subscript) is already EXERCISED by the reverse-lookup row above; the shipped-play half is an authored-script corpus measurement (literal 110; getcamerasubframe returns), which no replay of the eight primitives can produce |
| any runtime observation | OPEN QUESTION | none exists |

### `name_registry` — 15-Input/Input-Name-Registry/CONTRACT-input-name-registry.md

| claim | status | note |
|---|---|---|
| Signature and return convention | **EXERCISED** | node in `rcx`, code in `eax`, on both sides of all 154 cases |
| The three return codes `0x00` / `0x11` / `0x12` | **EXERCISED** | every case compares the code, and the census reaches all three: OK x144, NULL_KEY x1, DUPLICATE x9 |
| Node layout: name `+0x08`, next `+0x10`, value `+0x18`, stride `0x20` | **EXERCISED** | both sides walk the REAL 143-node array out of .data at that stride; a wrong offset mismatches on the first case |
| The comparison is a string comparison, not pointer identity | **EXERCISED** | the injected node whose name is a COPY of `Button_R2` at a different address returns DUPLICATE -- the one case that can distinguish strcmp from pointer equality |
| Insert is push-front, and only on success | **EXERCISED** | the resulting 144-node chain is compared node for node from the head, so both the order and the absence of a link on the failure paths are checked |
| Exactly one function writes each head | NOT EXERCISED | an image-wide census from `globals_index.py`, not a behaviour a differential executes. Its instrument is RIP-relative only and the contract says so |
| The two inserts differ only in the two displacements naming their own head | PARTIAL | the byte comparison and the capstone-resolved targets prove the bytes; `00876C80` is still not EMULATED, but its behaviour is no longer inherited -- integration_name_registry.py rebuilds the key registry's live 97-node list node for node |
| a non-zero `name` pointer is dereferenced with no validity check | NOT EXERCISED | and deliberately so. A case supplying a non-zero unmapped name pointer was written to kill two surviving mutants on this reconstruction's resolve-failure path, and the ORIGINAL faulted under it - emulation error at 008795B3, an unmapped read - so the case was withdrawn. The claim is established by reading 00879574 / 0087957B / 008795A0 / 008795B0 / 008795B3, and by that fault, but this suite does not drive it: a case that takes the original outside its domain measures nothing. The two mutants it would have killed are unkillable by construction - they mutate NameImage_At's bounds check, which is fixture scaffolding with no counterpart in the shipped function |
| Each registry is five paired functions of identical size | NOT EXERCISED | a static enumeration; four of the five entry points are not reconstructed at all |
| The other four are destructor, two finds and an enumerator | NOT EXERCISED | their bodies are read and their semantics recorded, but none is reimplemented, so no case can exercise them -- this is FULL-SUBSYSTEM's whole remaining gap for this pilot |
| 143 channel names, 113 channels, 16 alias groups, 97 key names | **EXERCISED** | the 143 real nodes ARE the input, and the live walk reproduced the grouping independently: the ONLY places consecutive registrations share a value are 11..26, exactly the 16 alias groups, with 113 distinct values across 143 entries |
| The real registration order | **EXERCISED** | recovered from the live chains -- push-front preserves the build order -- and then USED: integration_name_registry.py feeds the game's own order and compares against the game's own list, 0 of 143 and 0 of 97 nodes differing |
| any runtime observation | **EXERCISED** | five, in the contract's section 13, from walk_name_registry.py and integration_name_registry.py |

### `party_slots` — 11-Party/CONTRACT-party-slot-assignment.md

| claim | status | note |
|---|---|---|
| the roster is four qword slots at 0209A1F0 | **EXERCISED** | all four read back after every operation, and a slot past the fourth is driven to show the roster is not written there |
| an actor carries its occupied slot at +0x12, with 0xFF meaning none | **EXERCISED** | driven with the stored byte at 0xFF, at a real slot, and at a value that is out of range but not 0xFF, which takes a different arm of the unsigned bound |
| assigning an actor already in the party vacates its old slot first | **EXERCISED** | driven across pairs of slots, with the old slot compared for NULL and the displaced actor's own two bytes compared |
| the state byte at +0x0F is (slot > 3) + 2 | **EXERCISED** | driven at 0, 3, 4 and 100; a displaced actor gets 3 by the other path and that is compared too |
| the marker at [record+0xC0]+0x152 is raised to 1 before the swap and lowered to 0 after | **EXERCISED** | the trace carries both writes with the record each was applied to, and they are DIFFERENT records whenever the slot changes hands - which a state comparison alone cannot see |
| a NULL marker pointer skips the marker write and the notify | **EXERCISED** | driven with the occupant's +0xC0 set to NULL, on both the raise and the lower |
| the two readers disagree about a negative slot | **EXERCISED** | both driven at -1: the unsigned-bounded reader returns NULL and the sign-testing one goes to the current focus |
| the focus follow-up runs only for a real slot and only when the focus index is zero | **EXERCISED** | driven at both focus values and at a slot past the fourth |
| any runtime observation | OPEN QUESTION | none exists |

### `phyre_header` — 22-Middleware-PhyreEngine/Phyre-Asset-Container/CONTRACT-phyre-cluster-header.md

| claim | status | note |
|---|---|---|
| the header is 84 bytes of 21 `unsigned int` fields | **EXERCISED** | every case hands over exactly 84 bytes and the fields the ladder reads are driven at values a wrong offset reads differently; the FIELD NAMES come from the reflection registrations and are not something a fixture can check |
| the instance-list header is 36 bytes of nine fields | NOT EXERCISED | 0059A3B0 never touches an instance list; the layout is in the type store from its registration |
| exactly 84 bytes are read, through the stream vtable `+0x28` | **EXERCISED** | the scripted read is reached THROUGH the vtable slot the fixture plants, and it is handed the length the original asks for - a different slot or length would never reach the hook |
| `bytesConsumed` advances before the truncation test | **EXERCISED** | driven at 0, 1, 40 and 83 bytes, and the counter is compared as its own observable, so a reimplementation that tests first returns the same 9 and a different counter |
| the truncated code `9` is computed, not a literal | **EXERCISED** | the 9 is compared; that it is COMPUTED from 84 rather than stored is a fact about the instruction encoding, which no comparison of results can distinguish |
| a reversed marker is byte-swapped and re-tested against the same constant | **EXERCISED** | a big-endian header is accepted with outWasByteSwapped set, and the swap COUNT is compared - so being swapped once, re-tested, and later swapped back is measured rather than assumed |
| `PHYR` appears zero times in `.text` | NOT EXERCISED | a whole-image constant census |
| the platform and physics ids are `0x44583131` and `0x424C4C54`, with `0` a wildcard | **EXERCISED** | BOTH LEAVES RUN FOR REAL rather than being answered, and the physics field is driven at Bullet, at 0 and at a third value, so the wildcard is separated from a match |
| both id leaves are called even when `checkPlatform` is false | NOT EXERCISED | every case with checkPlatform false agrees on the result, which is what a caller sees; that the CALLS still happen is a call-graph fact and this suite does not count them |
| the one caller passes `checkPlatform` as a literal `1` | NOT EXERCISED | a fact about 0059E070, which the fixture does not run |
| the caller pre-seeds a valid header before reading over it | **EXERCISED** | the fixture pre-seeds RYHP and 84 exactly as 0059E0D7/0059E0DE do, which is what makes the truncated cases return 9 from a well-formed buffer rather than from stack garbage |
| `m_size` is compared twice, and the second comparison reloads the OUT-PARAMETER so it cannot disagree | **EXERCISED** | THE CASE THAT CORRECTED THE CONTRACT: a big-endian header whose raw m_size is 84. The reconstruction built from the earlier reading returned 0; the original returns 9 with outSize = 0x54000000, and outSize is compared |
| `0059A586`'s `jae 0059A5E0` is unreachable | NOT EXERCISED | it cannot be driven, which is the claim. No case reaches it and none can, because equality is taken at 0059A4E6 on the same value |
| the oversized copy is INLINE and makes no `memcpy` call, while the short path makes exactly one | **EXERCISED** | the memcpy COUNT is compared, and it is what separated the two paths when the reconstruction modelled the inline copy as a call |
| `0017D260` is `_aligned_malloc` and `00584730` is `_aligned_free` | NOT EXERCISED | both are scripted here, and their IDENTITY comes from the import table rather than from any behaviour a fixture could observe - what this suite drives is when they are called and with what |
| `0017D260` sets two argument registers `_aligned_malloc` does not read | NOT EXERCISED · scope | the allocator is scripted, so the registers it sets before its tail jump are never reached; this is a fact about the wrapper body, read statically |
| `r9`'s `+0x08` is the oversized copy's destination | **EXERCISED** | the oversized cases only run at all because the fixture gives r9 a buffer-shaped object; without it they fault at 0059A52E, which is how the role was found |
| `r9` is a stack local of the sole caller, with `r8`'s layout and `r8`'s ownership discipline | NOT EXERCISED | a fact about 0059E070s stack frame, which the fixture does not run - same disposition as the literal-1 claim |
| `r9` is the same TYPE as `r8` (`PhyreNamespaceBuffer`) | NOT EXERCISED | type identity is reflection-registration data; the fixture only needs r9 to be buffer-shaped, it never asks the type store |
| the short path takes `min(84 - m_size, namespaceSize)` and refuses when the surplus exceeds it | **EXERCISED** | driven at exactly equal and one over - m_size 80 against a namespace of 4, 5, 3 and 0 - and the memcpy LENGTH and SOURCE OFFSET are both compared, so the cmovb is measured and not inferred |
| the oversized copy is five `movups` plus one dword, not a dword loop | NOT EXERCISED | the instruction shape is not observable from outside; what IS driven is that it makes no memcpy call, which is the row above |
| the three size paths converge on `0059A6F0` | **EXERCISED** | the namespace reader's CALL COUNT is compared on all three paths, and its result is propagated in one case to show the return value is the reader's |
| `m_size == 84` in 169 of 169 sampled files | NOT EXERCISED | a file-side corpus measurement that ran no code |
| bit 31 of the capacity word is an ownership flag, and a set bit skips the release | **EXERCISED** | driven with the bit set and clear against the same sizes, AND at an ODD capacity - which is what the campaign demanded, because every earlier capacity was even and a mask consulting bit 0 behaved identically |
| a NULL namespace buffer is refused with 6, which is what a zero size against a non-matching capacity produces | **EXERCISED** | driven directly; the buffer's final null-ness is its own observable. FOUND BY THE PILOT - the case faulted on the unmapped release before this branch had ever been reached |
| the namespace reader imposes NO bound: it reads the length it is handed | NOT EXERCISED | read out of 0059A6F0 statically; this suite SCRIPTS that function, so it cannot establish what the real one does with a length |
| a short namespace read returns 9 and byte-swaps anyway | NOT EXERCISED | inside the scripted namespace reader |
| any execution of this ladder, isolated or live | **EXERCISED** | this suite IS that execution for 0059A3B0 and the two id leaves, isolated original-code rather than live |
| the symbolic values of `PResult` | OPEN QUESTION | not established; the numbers are compared as numbers |
| `0063E2E0` walks the descriptor's member list and its base chain, calling `0063CE80` per member | NOT EXERCISED · scope | 0063E2E0 is SWAP_FN, scripted - its internals never run here |
| the descriptor's `+0x38` dword is handed to every member callback | NOT EXERCISED | inside scripted 0063E2E0; the descriptor itself is .bss in the image, the fixture never builds one |
| the descriptor at `02CAA0A0` is built by a CRT STATIC CONSTRUCTOR, `00160210` | NOT EXERCISED | a static-init fact; no CRT constructor runs under the fixture |
| what `0059A6F0` does | OPEN QUESTION | 0059A6F0 is read (section 5) though still scripted here; the contract split the old combined 0063E2E0/0059A6F0 row - 0063E2E0 is now claimed, this stays open |

### `phyre_namespace` — 22-Middleware-PhyreEngine/Phyre-Asset-Container/CONTRACT-phyre-packed-namespace.md

| claim | status | note |
|---|---|---|
| the reader is 116 bytes, reads in one call, and validates nothing | NOT EXERCISED · scope | 0059A6F0 is not driven by this pilot - it needs a stream, and this suite has no scripted callee at all. It is read statically and driven as a scripted callee by the cluster-header pilot |
| it returns only `0` or `9`, and `9` only for a short read | NOT EXERCISED | inside 0059A6F0, which this pilot does not run |
| `bytesConsumed` advances before the test | NOT EXERCISED | inside 0059A6F0 |
| the swap fires even on a short read | NOT EXERCISED | the GATING is 0059A6F0's; what this pilot drives is the swap itself, once it is called |
| the block is a 6-field header, two zero words, three regions and a string pool | **EXERCISED** | every case builds exactly that shape and the whole block is compared, so a region found at the wrong offset differs in bytes; the counts are distinct in each case so no two boundaries coincide |
| `0x20 + 4A + 36B + 24C + D == m_packedNamespaceSize` in 35,984/35,984 shipped files | NOT EXERCISED | a file-side corpus measurement. The cases SATISFY the invariant by construction rather than testing it - section 16 records that as the coverage still missing |
| BOM `0x01020304` in 35,984/35,984; `+0x18` = `+0x1C` = 0 in 35,984/35,984 | NOT EXERCISED | a file-side corpus measurement over the VBF archive - the harness never sees a real file |
| member `w5` is the fixed-array bound | NOT EXERCISED | a meaning, established by the full-archive census - a byte-order transform moves the word without interpreting it |
| class `w7` is a per-class flags word, not per-record noise | NOT EXERCISED | a corpus finding - the transform preserves it regardless |
| class `w4`, `w5`, `w6`, `w8` are zero in all 684,244 shipped records | NOT EXERCISED | a file-side corpus measurement |
| class records are 9 words of 36 bytes | **EXERCISED** | 0059A780 driven alone at several counts with every word distinct, so a stride of 32 or a count of eight words lands on the next record and the bytes show it |
| member records are 6 words of 24 bytes | **EXERCISED** | driven through 0059C180's inline loop, with the member region's words distinct from the class region's so a wrong stride crosses a boundary visibly |
| the type table is a flat `u32` array, and its swap is vectorised | **EXERCISED** | 0059A8B0 driven alone at 0, 1, 2, 3, 7, 8, 9, 15, 16, 17, 31, 32 and 33 - EIGHT cases on the vector path and FOUR on the scalar tail, and the suite refuses to pass without both. Its two shuffle constants are mapped from .rdata, so the vector body really runs |
| the string pool is not swapped | **EXERCISED** | every whole-block case carries a non-empty ASCII pool and the whole buffer is compared, so a routine that touched it would differ in exactly those bytes |
| the swap order is not the layout order | **EXERCISED** | the classes are swapped before the type table, and with distinct region contents a reconstruction that used layout order would still agree - so what this actually establishes is the RESULT, not the order. The order is read from 0059C1D5 and 0059C245 |
| class `w0` is a 1-based parent index, `w2` a name offset, `w3` a member count | NOT EXERCISED | a MEANING, from the source page's corpus. A byte-order transform moves these words without interpreting them and cannot confirm any of it |
| member `w0` name, `w1` type reference, `w2` field offset, `w3` element size, `w4` bit 31 = pointer | NOT EXERCISED | a meaning, as above |
| `sum(class.w3) == nMembers`, members contiguous in class order | NOT EXERCISED | a corpus relationship between fields the transform never reads |
| the namespace's field list agrees with the reflection registrations | NOT EXERCISED | a join between two static sources |
| the swap routine has no bound and faults on counts that do not fit | NOT EXERCISED | OBSERVED here and then WITHDRAWN: the case faulted the original at 0059A790, and a fault cannot be compared against a return value. The observation is in section 10 row 5 |
| class `w7` bit names | OPEN QUESTION | the reader only byte-orders the word; the semantic consumer is the object-binder outside this contract |
| why the namespace carries a byte-order mark nothing reads | OPEN QUESTION | not established |

### `prep_step` — 08-Combat-Formula/CONTRACT-preparation-step-family.md

| claim | status | note |
|---|---|---|
| the family is reached only through the table at 01EFA5C0, from exactly two call sites | NOT EXERCISED · scope | the two dispatchers are out of scope; every member is called directly here |
| the two record arguments are BattleStatsRecord, not BattleUnit | **EXERCISED** | every byte the family reads is driven at a value where a neighbouring offset differs |
| the third argument is real and is read by exactly one member | **EXERCISED** | the result record's +0x1B driven at five values against all sixteen members; only 0038A680 changes behaviour |
| neither dispatcher bounds the slot | NOT EXERCISED · scope | a statement about the dispatchers, which are out of scope |
| the members write only the three scratch words and never through their arguments | **EXERCISED** | both records and the result record are compared after every call |
| **TWO** of the sixteen write only a subset of the three words | **EXERCISED** | the scratch is poisoned before every call, and exactly 0038A9D0 and 0038AA90 come back carrying a poison word |
| the reset zeroes all three and runs before each walk | NOT EXERCISED | 003849B0 is the dispatcher's, not a member's |
| the walk stops as soon as 02AEDFB8 is 1 | NOT EXERCISED · scope | the walk is out of scope |
| the slot comes from a recipe's second list, not from a weapon | NOT EXERCISED | authored data, not reachable from a member |
| recipes 20-29 differ only in this slot | NOT EXERCISED | authored data |
| the defender's +0x30 is read by two slots, not one | **EXERCISED** | the defender's +0x2F and +0x30 are given different values in every fixture, so a member reading the wrong one differs |
| slot 70 makes no defender read at all | **EXERCISED** | 0038A470 driven with the defender's bytes distinct; its defence word is an immediate zero |
| slot 72 is one-sided | **EXERCISED** | 0038A680 driven through both of its forms, and neither reads the defender except for the defence term |
| the read sets are per body in isolation | **EXERCISED** | that is exactly what this suite does: one body per call, nothing else running |
| the sixteen bodies share one template, with six closed forms for the multiplier | **EXERCISED** | every form driven, compared as a bit pattern rather than a decimal |
| the variance gate is 0.01f and is the divisor's ONLY guard | **EXERCISED** | weapon bytes 0, 1, 2, 7, 8 and 0xFF across nine members, with the generator's cursor showing whether a draw was taken |
| the remainder is UNSIGNED, on the raw 32-bit draw | **EXERCISED** | a signed remainder fails on 3 lines - the draws whose tempered word exceeds 0x7FFFFFFF |
| the authored row address is built in THIRTY-TWO-bit arithmetic | **EXERCISED** | a stride-times-index product of 0x100000110, which only this case reaches |
| slot 72's equipment compare is UNSIGNED, and 0x1000 passes whatever the limit is | **EXERCISED** | limits at and above the signed boundary, where a signed compare disagrees on 8 lines, and the exact value 0x1000 against three different limits |
| two members write an IMMEDIATE ZERO to the defence term rather than leaving it | **EXERCISED** | distinguished from the two that leave the word, by the poison |
| 0038A470 draws TWICE against one gate | **EXERCISED** | the generator's cursor moves by two across the call |
| the family's only shared callee is the MT19937 draw | **EXERCISED** | executed on both sides from one planted state, including the twist at 0x270 and an unseeded first draw |
| the null-row path computes the same doomed address on both sides | **EXERCISED** | all six row-reading members with a null registry, and again with a zero resolver base; the fixture maps a page at zero and section 13 says what that does and does not prove |
| the SIMD arm of the generator's twist is NOT executed | NOT EXERCISED | by construction: the image's own CPU-feature value selects the scalar arm |
| nothing observed at runtime | NOT EXERCISED | still true: this pilot is isolated original-code, not a running game |

### `quality_preset` — 19-Save-Load-Settings/Game-Settings-Config/CONTRACT-game-setting-config.md

| claim | status | note |
|---|---|---|
| size `0x65C`, singleton `0x01F82D20`, 1 writer | NOT EXERCISED | both sides are given only the first 31*4 = 0x7C bytes. The object's size, its singleton address and the one-writer census are static facts no case reads |
| 31 settings, offset = index × 4 | **EXERCISED** | 31 contiguous ints compared elementwise -- a wrong stride mismatches |
| key / value-name / matrix / mask tables | PARTIAL | the mask and matrix are the REAL shipped bytes at `00900CC0` and `00900CE0`; the key and value-name tables are never touched on this path |
| preset matrix columns are indexed by Quality | **EXERCISED** | quality drawn from {0,1,2,3,-1,4,7}, so out-of-row indices are compared too |
| construction precedes `main` | NOT EXERCISED | a startup-ordering fact; no per-function differential can reach it -- this is INTEGRATION |
| `FrameLimit` drives the time base | NOT EXERCISED | a different chain (`0022BE18`), not reachable from `001DE4F0` |
| ~~`+0x554` unwritten by config code~~ **withdrawn — the claim was about a field that does not exist** | OPEN QUESTION | withdrawn 2026-09-10, so there is nothing left to exercise. The measurement this row used to carry has moved to the two rows below, under the claims it actually supports |
| `001DE4F0` writes nothing outside the 31 settings | **EXERCISED** | both sides get the WHOLE `0x65C` object, poisoned byte by byte before the call, and the full extent is compared by hash: **0 bytes changed beyond the settings, summed over 600 cases** |
| `iniPath` is `wchar_t[260]` at `+0x450`, 520 bytes, `+0x450`–`+0x657` | PARTIAL | the whole-object comparison does cover `+0x450`..`+0x657` as bytes that must not change, so a reconstruction that wrote into the path buffer here would be caught. The field's WIDTH is a static ABI fact (`008C3008` is `wcscpy_s`) that no case on this entry point reads -- `001DE4F0` never touches the path |
| no separate field exists anywhere in `+0x450`–`+0x657` | NOT EXERCISED | a whole-image displacement fact over five config functions; a differential on `001DE4F0` cannot reach it |
| the `0x65C` block is `malloc`ed, never zeroed | NOT EXERCISED | the harness supplies its own buffer and poisons it deliberately, so it can never observe what the game's allocator returns -- this is INTEGRATION |
| meaning of the three value tables | OPEN QUESTION | not established |
| any runtime observation | OPEN QUESTION | none exists |

### `ramp_channels` — 17-Presentation-Rendering/CONTRACT-authored-command-ramp-channels.md

| claim | status | note |
|---|---|---|
| 160 records of 0xE0 behind a lazily allocated pointer at 02B40528 | **EXERCISED** | the allocator runs against hooks for its three externs; the table extent and the 160-record enable sweep are compared byte for byte |
| set(id, steps, target) writes NOTHING when rec[0x10] != id | **EXERCISED** | poisoned records dumped after refused calls on every channel, including an id whose low byte matches the slot but whose high bits make the full-dword guard fail |
| steps == 0 sets the value immediately and clears the counter, cancelling an in-flight ramp | **EXERCISED** | mid-flight re-sets at several tick depths; the counter and the value are compared bitwise |
| otherwise counter := steps and delta := (target - value) / steps | **EXERCISED** | EXERCISED with a correction the contract should carry: the image computes (target - value) * (1.0f / steps) - a divss for the reciprocal then a mulss - and a literal '/' reimplementation is last-bit wrong. The harness compares bits, so the distinction is measured, not argued |
| the tick advances every enabled, unpaused slot's five channels by value += delta with counter -= 1, in channel order 0, 2, 1, 3, 0x43 | **EXERCISED** | all five channels driven at several counter values across enable/pause/gate combinations; the order is not observable through these fields and is only re-stated, not proven here |
| the fifth channel (+0x43 counter, +0x98 value, +0x9C delta) is advanced by the same tick and no authored-command class here writes it | PARTIAL | the advance of +0x43 is exercised directly; 'no class writes it' is a negative this suite cannot run - it plants the channel rather than searching writers |
| the allocator's lock/alloc(0x8C00)/unlock sequence runs only while the pointer is null, then zeroes the two dwords at 02B40520/24 and sweeps the enable bits | **EXERCISED** | the three externs are hooked and recorded on a NOTABLE'd pointer; the second call is compared too and makes none. Sharpened by the fixture: the second zeroed dword IS the pause gate - 02B40524, not the contract's 02B4052C - so a planted GATE dies on ALLOC |
| the three tick-call-site gates' predicates | NOT EXERCISED | the gate bodies are read whole and their predicates named in the contract; the suite drives the tick's enable/pause/gate matrix but does not construct the gates' own source fields (the pass-enable aux mask, the lazy singleton's +0x118 byte, the manager +0xAA44 dword and the last-request id) |
| the five channels feed `003B62D0` as: ch0 (+0x50/0x54) a heading-rotated 2D offset added to the bone-blended anchor (out+0x50/0x58); ch2 (+0x58/0x5C) the quad extents (out+0x34/0x38); ch1 (+0x70) a rotation offset on the actor heading (out+0x24); ch3 (+0x78) a factor of the out+0x28 product; and +0x43 (+0x98) an eased cross-fade weight (LUT row 5 via 0046FAE0) blending all four toward the +0x80–0x94 snapshot and the anchor between bones +0x3C/+0x3E | NOT EXERCISED | the consumer arithmetic is proven by full disassembly and measured by EXP-108; this suite exercises the producer side (setter/tick fields) and does not build draw records |
| every record byte has a censused accessor or a named disposition | NOT EXERCISED | a static census claim over the 21 table-referencing bodies; the suite's fixture only spans the channel fields it drives |
| the V2 pool's gate cell `02B3F554` is a written mode dword with no reader in any static form | NOT EXERCISED | a static census claim over the sibling 0x70-stride pool's header - a different table entirely; the suite's fixture only spans this pool's channel fields |
| what any channel controls, what the gate is, who assigns rec[0x10], and whether the tick is per-frame | NOT EXERCISED | resolved on the page 2026-09-14/20 (UG-2 gate, UG-4 ticket, UG-5 cadence, 003B62D0 consumer map); none of it is driven by this suite |

### `render_pool` — 17-Presentation-Rendering/CONTRACT-render-record-pool-lifecycle.md

| claim | status | note |
|---|---|---|
| the pool is 160 records of stride 0x740 ahead of the tail block | **EXERCISED** | every record address on both sides is built from the stride, and the 161st allocation is driven |
| the pool's six indices are 32-bit and the record's three links are 16-bit, both using -1 | **EXERCISED** | each index and each link driven at its sentinel and at a real value |
| the narrowing is correct rather than lucky | **EXERCISED** | both lists driven empty, at one element, and at three |
| the 8-byte store in the constructor is not evidence that two fields are one | NOT EXERCISED · scope | the constructor is out of scope; both drivers plant the state it would leave |
| allocation is keyed by name and refuses a duplicate rather than replacing it | **EXERCISED** | a duplicate driven on the active list and on the pending list |
| allocate's two failure returns are indistinguishable to the caller | **EXERCISED** | a duplicate and a full pool both driven, and both answer the same null |
| a newly allocated record is on the PENDING list, invisible to any active walk | **EXERCISED** | the pool image after every allocation shows both lists |
| the free cursor advances to the next record whose state word +0x284 is 0, wrapping at 160 | **EXERCISED** | one blocked record, two consecutive blocked records, and a cursor planted at 159 |
| liveCount == 0 implies nextFreeIndex == 0 | **EXERCISED** | driven through retirement and through release's unlink path, each emptying the pool |
| liveCount counts records on EITHER list, and promotion does not change it | **EXERCISED** | the count is compared across every promotion, including one of three records |
| promotion unlinks each record AND clears both pending ends afterwards | **EXERCISED** | driven at one and three records, and on an already empty pending list |
| promotion sets bit 5 of the tail's flag word | **EXERCISED** | the flag word is compared after every operation |
| retire acts only on actives whose +0x290 has bit 1 set | **EXERCISED** | the head, the middle, the tail, all three and none |
| the lifecycle never reads or writes the tuning fields EXCEPT +0x28 | NOT EXERCISED | the +0x28 read is driven from two planted values; the absence of the others is a negative no run can establish |
| the +0x2C index is a third width again and no lifecycle operation touches it | NOT EXERCISED | a negative, and outside these five entry points |
| the pending walk has no retirement test, and the active walk does | **EXERCISED** | the same marked record driven on each list, through both the look-up and an allocation |
| allocate sets bit 0 of the record's +0x290 and promotion clears it | **EXERCISED** | the record's flag word is compared before and after every promotion |
| a fresh record's links are the RESET's postcondition, not allocate's | **EXERCISED** | the reset's link writes are modelled identically on both sides; without them the first promotion walks into record 0 |
| the free cursor reads +0x284 as a DWORD, starts at the record just taken, wraps at 160 and parks at 0 when the pool fills | **EXERCISED** | a state word of 0x100, which a byte-wide read sees as free, and a full pool |
| promotion stamps the tail's +0x28 into the record's +0x414 and conditionally takes a handle into +0x114 | **EXERCISED** | both answers of the question that gates the handle, with the stamp planted |
| promotion clears flag bit 0 for one callee and restores it whatever the callee did | NOT EXERCISED | the bracket is driven with the bit set and clear, but the oracle never changes it, so the restore is shown preserving and never undoing |
| retirement decrements the count BEFORE the two end fixups, and the fixups compare the record's own id | **EXERCISED** | a planted id that disagrees with the walk leaves the ends alone; the decrement's position is not separately observable from outside |
| retirement frees two handles and drains a child list at +0x08 | **EXERCISED** | each handle driven set and clear; the child loop is entered zero times and cannot be driven from a scripted oracle, which is the finding |
| release does not unlink a live record: it marks it for retirement | **EXERCISED** | both lists, both ends and the count compared across the call |
| release's unlink path is the one for a record that was never promoted | **EXERCISED** | driven at the head and the tail of a two-record pending list |
| release answers 1 for every non-null record, including one that matches neither path | **EXERCISED** | all three answers driven, plus the null |
| release's live path drops two side objects through the resolver pair | **EXERCISED** | each combination of the two oracle answers, at both values of +0x18, with the owner planted behind the resolver |
| what the eleven scripted callees do to a record beyond these fields is NOT established | NOT EXERCISED | by construction: they are the oracles |
| `0051BA80` admits through `0051F080` with `refresh = 0` when the caller's slot is `-1` | NOT EXERCISED | 0051BA80 is the presentation-entry container's admission path, not one of this suite's five pool-lifecycle entry points - nothing here calls it |
| `0051F620` resolves its base by the signed low-2-bit mode of `[rcx+4]` and rebases every linked node's `+0x18` | NOT EXERCISED | the rebase container is a different structure from the 160-record pool; no case reaches 0051F620 or its resolver |
| the rebase walk reads each node's `+0x0C` link AFTER the `003AB7F0` call, with no snapshot | NOT EXERCISED · scope | inside 0051F620, which this suite never runs |

### `reward_award` — 13-Rewards-Progression-Economy/CONTRACT-experience-and-licence-award.md

| claim | status | note |
|---|---|---|
| both functions are pure and write nothing | **EXERCISED** | every record and row is compared after each call and none moves |
| a zero return means both "nothing owed" and "not eligible" | **EXERCISED** | all six refusals driven, each returning the same answer a legitimate zero would |
| the recipient must be kind 0 and the corpse kind 1 | **EXERCISED** | both driven at the wrong kind |
| the status mask 0x80000003 gates both awards | **EXERCISED** | driven from each status word separately, on the recipient and on a walked party member |
| the two id filters are different, and licence is the narrower | **EXERCISED** | both driven at 0, 6, 7, 0x19, 0x1A, 0x1B, 0x27, 0x28 and 0xFF, where they disagree |
| the reward rows supply a per-level multiplier and an addend, both at their +0x34 | **EXERCISED** | driven at values where a swapped row or a byte read gives a different answer |
| the base is the corpse's level minus the byte the rebuild stored at +0x88 | **EXERCISED** | driven at four corpse levels and four +0x88 values, including one above the level |
| both reward row pointers may be NULL and neither function checks them | NOT EXERCISED | a NULL row would fault on both sides rather than compare; the suite drives every other NULL |
| a NULL row comes from an ABSENT descriptor or a failed resolution, not from an out-of-range index | NOT EXERCISED | this pilot drives the two reward COMPUTATIONS; the claim is about the INSTALLER that stores the row pointers, which is EXP-075's subject - the whole 1,808-byte body executed in 14 fixtures with both private guard mutations detected. It corrects this contract's own earlier causal claim, which had attributed the NULL stores to the index bound |
| a zero ENCODED reference decodes to the relocation base, not to NULL | NOT EXERCISED | the decoder is EXP-076's subject, composed with the installer there rather than scripted; this pilot drives the two reward computations and never resolves a reference |
| the stored row pointer is built in 32-BIT arithmetic and zero-extended, so a base above 4 GiB truncates and a non-zero base can store exactly NULL | NOT EXERCISED | same boundary. EXP-076 drives base 0x100000000 with reference 0 and index 0 as its own control and stores a NULL row from a non-zero base |
| three of the four bound guards are UNSIGNED and one is SIGNED, so a zero count is the only case an index passes | NOT EXERCISED | same boundary: the installer, not this pair of functions. `dec ecx` on a count of 0 gives 0xFFFFFFFF, so the three `ja` guards pass any index while the single `jg` compares against -1 and rejects every non-negative one |
| the divided path uses a SIGNED divide over a subtraction that can go negative | **EXERCISED** | driven at a level-0 corpse with +0x88 of 1, where the share comes back negative |
| whether a level-0 unit can be alive at kill time is unknown | OPEN QUESTION | a live observation; nothing offline can settle it |
| the doubling happens after the division, and zero wins over double | **EXERCISED** | driven with each bit alone and with both together, on a divided share |
| either modifier bank carries the effect alone | **EXERCISED** | driven from +0x6B and from +0x7B separately, for both halves |
| licence points are gated globally before any argument is examined | **EXERCISED** | driven with the gate refusing, where nothing else is read |
| the licence award reads +0x2F of both reward rows and doubles on bit 0x10, with no division anywhere | **EXERCISED** | driven at byte values a dword read would not reproduce; the control that divided by 100 failed on 12 lines |
| the divided path's member filter rejects id 0x1A as well as 0x1B-0x27 | **EXERCISED** | driven at 0x19, 0x1A, 0x1B, 0x27 and 0x28, where the divisor changes |
| a kind-1 party member is counted whatever its id | OPEN QUESTION | WITHDRAWN by the contract 2026-09-18 and demoted here rather than re-verdicted. The divided path can only count kind-0 members: BattleUnit_FindByDefinitionSelector (002367A0) compares a BYTE id against word[stats+4], whose high byte is the kind, so a kind-1 record's word is >= 0x100 and cannot match. This pilot PLANTS the member in the fixture, so it drives the two filter arms and never reaches that selector - which is exactly why the claim read EXERCISED here. The planted case below is kept: it still shows the arms test +0x05 first, which is true and is not the withdrawn claim |
| the level operand is the CORPSE's, not the recipient's | **EXERCISED** | every case gives the two different levels; the control reading the recipient's failed on all 265 lines |
| nothing observed at runtime | OPEN QUESTION | none exists |

### `rng_generators` — 21-RNG-And-Determinism/CONTRACT-gameplay-generators.md

| claim | status | note |
|---|---|---|
| the LCG advances three steps per draw | **EXERCISED** | the state word is read back after every single draw and compared; a one-step or two-step reconstruction disagrees on the first one |
| the LCG's XOR assembly and field order | **EXERCISED** | every returned value is compared over seeds chosen to separate the three fields; OR for XOR, or the 11-bit and 10-bit fields swapped, disagrees immediately |
| `0x41C64E6D` and `0x3039` are the ANSI C constants | **EXERCISED** | checked as bytes in the shipped body - three `imul` immediates and three `add` immediates at the six cited addresses - and exercised by every draw |
| the MT's lazy 5489 seed and the flag outside the state | **EXERCISED** | a stream is drawn from with the flag clear and the whole sequence compared against a stream explicitly seeded with 5489; the flag itself is compared after every command |
| seeding leaves the cursor at 624 | **EXERCISED** | `MT_META` after each seed compares the cursor on both sides. This claim was NOT in the contract before this harness; it was read off `00866D98` while building it |
| the tempering masks are the textbook ones, pre-shifted | **EXERCISED** | the two identities are computed from the immediates actually present at `00863C5B` and `00863C67`, and every compared draw runs through them |
| the twist at exactly 624 with `M = 397` | **EXERCISED** | more than two full periods per seed, with all 624 vector words compared after the twist |
| the two twists are one auto-vectorised loop | **EXERCISED** | both shipped paths are run over the same vector by forcing `__isa_available`, and the resulting 624 words and cursor are compared path against path |
| which callers reset the LCG seed through `00328D80` | NOT EXERCISED | closed by a call-site census with a memcpy control, not by this harness - exactly one caller, 00234320 in BattleSystem_InitializeAreaState. A census is not an execution and this row stays unexercised however settled the claim is; what would exercise it is a harness that drives the area-init path, which needs a BattleSystem this one does not build |
| `01FD4A80` is the session frame counter | NOT EXERCISED | closed by a per-body rip-relative census over all 35,713 .pdata bodies: exactly two operands image-wide (inc at 0022A59F in the master dispatcher 0022A580, the *0x258 read at 005843B4), .data uninitialised tail. A census is not an execution; exercising it needs a save-load path this harness does not build |
| no unattributed path reseeds the MT | NOT EXERCISED | a reachability census over every route form (E8/E9, lea, immediate, data pointer slot) for five addresses; by construction nothing in it is drivable |
| the float draw's vftable pair is `MTRand_int32`/`MTRand_closed` | NOT EXERCISED | an RTTI decode of two .rdata vftables plus a disasm match of the shared lazy-seed preamble; the stamps are dead stores no draw compares |

### `save_image` — 19-Save-Load-Settings/CONTRACT-save-image-buffers.md

| claim | status | note |
|---|---|---|
| The image is 0x56690 bytes | **EXERCISED** | a distinct pattern is planted across all four buffers and the copy compared byte for byte; any other length changes either the image digest or the padding line |
| The buffers are 0x566C0 apart | **EXERCISED** | all four buffers are addressed through the shipped stride and digested independently; a wrong stride makes the copy read or write the wrong one |
| The 48 bytes between images are never touched | **EXERCISED** | the padding behind every buffer is compared as its own line before and after each operation - this is the row the suite exists for |
| The clear writes 0x56690 zero bytes to the active buffer | **EXERCISED** | cleared, then the active digest and its padding both compared |
| The getter returns the active buffer | **EXERCISED** | the returned pointer is compared as an offset into the block |
| The copy is inlined, with no copy callee | **EXERCISED** | the trace lists every call the emulated body makes; no copy routine appears in it |
| The copy reads the selector bit first and holds it across the copy | **EXERCISED** | the original's own 00236760 runs over a planted global at both bit values, and the value reaching the submit callee is compared |
| The copy hands the submit callee the buffer and 0x56690 | **EXERCISED** | the trace carries the submit callee's three arguments, the pointer as an offset |
| The clear's tail jump to 0016D6A0 is a bare return | **EXERCISED** | that address is mapped from the image and executed rather than hooked, so a body that was not a bare return would not come back |
| any runtime observation | OPEN QUESTION | none exists |

### `sound_request` — 18-Audio/Audio-Boundary/CONTRACT-sound-request.md

| claim | status | note |
|---|---|---|
| the wrapper is 51 bytes, takes **one** argument through an unwritten `ecx`, and tail-jumps | **EXERCISED** | every wrapper case passes its localIndex in ecx and nothing else; a body that ignored the argument would return the same id for all of them, and the cases drive several |
| the two constants are `0x40` and `0x7F` built by a peephole | **EXERCISED** | the dispatch arguments are compared, so the pair the wrapper injects is observed rather than assumed - and the verb cases drive other values through the same slots |
| the global gate is `*(0x02091098)` and refuses before the lookup | **EXERCISED** | every wrapper case runs at four gate values, and the gate-set cases carry a handle that would otherwise resolve, so a gate read AFTER the lookup would still differ |
| the gate has exactly four references image-wide, one of them a write | NOT EXERCISED | a whole-image census, which a six-function fixture has no way to perform; the source page and an independent controlled scan both establish it |
| the setter is 7 bytes and stores its argument verbatim | NOT EXERCISED · scope | 00249FC0 is not driven; the gate is planted directly, which is what the readers see |
| a script verb reaches the setter, and its argument becomes the gate value | NOT EXERCISED | a reachability claim about the verb table and 00512080, neither of which this fixture has |
| `00271500` is a fourth wrapper with no gate check | **EXERCISED** | THE CENTRAL CASE: every wrapper case runs through both 00249C60 and 00271500 at four gate values, and the suite REFUSES TO PASS unless the two disagree on the gate-set cases |
| six further functions inline the wrapper, none reading the gate | NOT EXERCISED | one of the six (00357040) is driven and its gate-independence is covered; the other five are a call-site census this fixture cannot perform |
| `sebsoundplay_2c1` passes script-chosen pan and volume | **EXERCISED** | 77 verb cases pop pan and volume from a scripted VM stack, and the dispatch arguments are compared - so the values are observed arriving, not inferred |
| pop *n* is argument *5−n* | **EXERCISED** | the scripted pop returns a known sequence, so which popped value reaches which dispatch slot is measured; the ARGUMENT NUMBERING is the calling convention's claim, and what is proved here is only the order the four pops land in |
| `p3` is masked to 7 bits and `p2` only truncated to 8 | **EXERCISED** | driven at 0x00, 0x40, 0x7F, 0x80, 0xFF, 0x100 and 0x1FF on BOTH arguments - 49 combinations - where one mask and one truncation disagree; invisible in the return value and visible only because the dispatch arguments are compared. The SECOND mask at 00210C0C is not run |
| the id's bit 31 is cleared and the selector is hardcoded 0 | **EXERCISED** | the play cases drive ids with bit 31 set and compare the dispatched edx and ecx |
| the second gate returns before dispatch, with **0** rather than `-1` | **EXERCISED** | driven on and off with an id that would otherwise dispatch, and the dispatched FLAG is compared as well as the return value, so 'returned 0' and 'did not dispatch' stay separate |
| the resolver arithmetic is `entry[+8] * 512 + localIndex`, and `entry[+8] == slot` is forced | **EXERCISED** | several slots including 63, several indices, entries whose dword does NOT match the key, and handles with a large high word - the mismatching entry is what separates multiplying the ENTRY from multiplying the slot index |
| the sign test on the entry word is unreachable | NOT EXERCISED | it cannot be driven: the value is zero-extended from a word before the test. The reconstruction writes the branch out and this suite cannot reach it either, which is the honest outcome rather than a pass |
| there are five resolvers over three handles and one table | **EXERCISED** | all four driven against the same planted handles, each at the handle value only IT reads, so a variant reading the wrong handle disagrees rather than refusing alike |
| `003A1070` guards on handle B and reads handle C | **EXERCISED** | driven with handle C valid and handle B at -1, the only shape that can show a guard on a slot the resolver does not read |
| `003A1180` and `003A11F0` differ **only** in the liveness precondition | **EXERCISED** | both driven over the same handles with liveness held and clear, and the suite REFUSES TO PASS unless 003A11F0 survives a hold that 003A1180 refuses |
| the three handles are set by three 83-byte setters and cleared together | NOT EXERCISED · scope | the setters and the teardown are not driven; the handles are planted, which is what the resolvers read |
| `(0x40, 0x7F)` are pan and volume, and pan's field is 0–255 | NOT EXERCISED | the NAMING is a claim about the voice setters at 002256B0 and beyond, which are not here. What this suite drives is the two slots' different WIDTHS, not what they are called |
| the fork is a two-way branch on the selector, and the request path always takes `+8` | NOT EXERCISED | the pilot stops at 001DBDB0 and never runs 00210C00. The selector the request path SENDS is compared - it is one of the dispatch arguments and is 0 in all 89 - but which sub-controller that selects is read, not run |
| `00210C50` is a sibling of the fork, not a request site | NOT EXERCISED · scope | not driven at all; it is reached from 0024A1A0, which this fixture does not run either |
| the singleton is five controllers with real RTTI | NOT EXERCISED | behind the scripted dispatcher |
| a receipt is issued when nothing started | NOT EXERCISED | the receipt is the dispatcher's, and the dispatcher is scripted |
| 100 non-Audio callers and none inside Audio | NOT EXERCISED | a call-site census |
| the table is exactly 64 entries, so the slot is 0..63 and the id space is 15 bits | NOT EXERCISED | a claim about the table's EXTENT, established by reading 003A0C90's walk and its list head. The pilot consumes the number - slot 63 and the 'none' index 64 are both driven - but a fixture cannot measure how much table the process actually owns |
| the `0x40` that evidences the table's length is a not-found sentinel, not a length | NOT EXERCISED | A reading of 003A0C90's 0x40 as a sentinel and of 003A0EA0's 72-bit bitmap, both static. The suite plants entries and resolves them; it never establishes how many rows the table has, and adding a case that assumed 64 would beg the question |
| the gate's two non-script writers are a disable/restore pair | NOT EXERCISED | neither 0027F5D0 nor 002D6F90 is driven; the gate is planted at the value they would write |
| `0024A1A0` is a control entry, not a request site | NOT EXERCISED · scope | not driven: it takes a raw id to a different dispatcher, so the fixture has nothing to compare it against |
| any execution of this path, isolated or live | **EXERCISED** | this suite IS that execution for the six bodies it drives, and it is isolated original-code rather than live |
| why `003A1070` guards on a handle it does not read | OPEN QUESTION | the guard's EXISTENCE is driven here; its reason is not something a fixture can answer |

### `status_write` — 10-Status-Periodic-Terminal/CONTRACT-status-write.md

| claim | status | note |
|---|---|---|
| the seven parameters and their registers | NOT EXERCISED | not this pilot's coverage to claim - EXP-086 executes the shipped 0030E360 with real argument sets (67 cases, 0 mismatches), so the signature was live; the experiment does not report per-parameter observation, so its coverage is recorded, not claimed |
| `adding`, `initialises`, `showReaction`, `extraEffect`, `bit`, `wasPresent` | NOT EXERCISED | not this pilot's coverage to claim - the operation was live under EXP-086 but it does not report per-local observations; recorded, not claimed |
| presence is `+0x3C \ | NOT EXERCISED | not this pilot's coverage to claim - EXP-086's executed confirmations name it directly: "Presence = (+0x3C | +0x64) only", §10 row 8 executed |
| the six modes and their already-in-state refusals | NOT EXERCISED | not this pilot's coverage to claim - EXP-086's executed confirmations name both halves: "Six modes, exactly as §7" and "Already-in-state refusals per mode" |
| the terminal dispatch: 8 targets, one case per status, and which statuses share a case | NOT EXERCISED | not this pilot's coverage to claim - EXP-086 executed the case table at shipped VAs (67 cases, 0 mismatches); four of its targets are presentation |
| Doom has no terminal case | NOT EXERCISED | a property of that dispatch table |
| the beat default's ×30 and the duration default's ×300 are different scales, not a typo in either | PARTIAL | the times 30 is executed - every timer case multiplies by it and five multiplier values are driven. The times 300 is READ, not run: 00387730 is not driven by this pilot |
| the beat default is `row.+0x09 × [01DFE0B4] × 30` | **EXERCISED** | 003876D0 driven over all 32 status ids, seven strides and five multipliers including 0 and -1, with every row byte derived from its OFFSET so a wrong stride, index or displacement lands on a different value |
| the duration default's formula, classes and the ×1.5 | NOT EXERCISED · scope | 00387730 is the duration default and is NOT driven by this pilot - only the beat default 003876D0 is. Section 13 names it as remaining work rather than counting it. Its final scale WAS read statically, 2026-09-12: 00387992 imul eax, eax, 0x12C, times 300 against the beat default's times 30 - the same global, the same shape, 0x60 bytes apart, and an order of magnitude between them |
| the definition record is `0x28` bytes, not `0x10` | NOT EXERCISED | the fixture USES 0x28 as the stride in most cases, which assumes the claim rather than testing it. What is tested is that the stride comes from the table header: seven different strides are driven and each gives a different answer |
| bit 13 of `+0x06` is set on exactly ids 0–16, 29, 31 | NOT EXERCISED | a measurement over the shipped status_data.bin, which this pilot replaces with a synthetic table |
| `+0x08` is a duration on 21 ids and `0xFF` on 11 | NOT EXERCISED | the same shipped-table measurement |
| the cascade masks, including Stone→Petrify and Haste↔Slow | NOT EXERCISED | not this pilot's coverage to claim - EXP-086 measured the shipped masks' cascade behaviour (status 10 clearMask 0x02000000 -> 1 inner call, KO 0x7FFEF57C -> 25, Stone 0x1FFC0004 -> 12; |0x200 suppresses the inner recompute) |
| the result record is `0x148` and lives in the caller's frame | **EXERCISED** | 003848E0's memset covers +0x08..+0x147, and the whole 0x150-byte record is compared, so the extent is measured rather than read off the caller's lea |
| the initialiser leaves `+0x00`–`+0x07` exactly as the caller left them | **EXERCISED** | the record is handed over pre-filled with 0xC7, 0x00 and 0xFF and those eight bytes come back unchanged in each - a fixture handing it zeroed memory could not have shown it |
| the table pointer is resolved and then truncated to 32 bits | **EXERCISED** | two DIFFERENT tables planted, one at the full 0x100500000 and one at the truncated 0x00500000, and the byte returned is the truncated one's. This is the claim in this contract that had never been run |
| `0020E600` ZERO-extends the encoded value | **EXERCISED** | an encoded 0x80000000 over a base of 0x10000 reads 0x80010000, with a different table planted at the sign-extended alternative |
| the timer default faults when the table is absent while the cascade degrades | **EXERCISED** | the timer half only. Page zero is planted, so the case shows it reads [0 + 9] and what it then returns, rather than only that it faults. The cascade side, 0030E686, is still static |
| a resolve that returns zero takes the same unguarded read | **EXERCISED** | the second refusal at 003876EF is driven with its own case and falls through to the same read |
| the party-side shortcut, the gates and the terminal-on-terminal refusal | NOT EXERCISED | not this pilot's coverage to claim - EXP-086's executed confirmations name all three: "Eligibility" (gate1 refuses; gate2 refuses only on terminal bits), "Party-type early path" (party inner, kind 0, type 0x1B-0x27 -> defeat_cleanup before the mask write) and "Existing-terminal gate" (the bit15 predicate blocks) |
| the defeat cleanup, its predicates and the four `02089340` latches | NOT EXERCISED | a different operation entirely |
| the arithmetic half executed in isolation | **EXERCISED** | THIS PILOT IS THAT EXECUTION - 155 cases, 0 mismatches, only memset scripted |
| any runtime observation of this operation, or any execution of `0030E360` | NOT EXERCISED | not this pilot's coverage to claim - EXP-086 executes the shipped 0030E360 at its canonical VA (67 cases, 0 mismatches, a different instrument). What remains open is live observation - section 13's stated class is isolated original-code and the live rung is still queued |
| what the builders write beyond the initialiser | **EXERCISED** | both builders driven over seven status ids and seven counters each, with the whole record and the whole unit compared. This answered SW-2 |
| neither builder writes any byte of the unit | **EXERCISED** | all 0x60 bytes of the unit compared on 98 builder cases |

### `storage_read` — 19-Save-Load-Settings/CONTRACT-storage-read-completion.md

| claim | status | note |
|---|---|---|
| the inner read returns a boolean, not a count | **EXERCISED** | the return is compared bitwise across full, short, at-end, zero and negative counts; a partial count is never returned - 0 or 1 only |
| the wrapper multiplies that boolean by the element size | **EXERCISED** | WRAP returns size on a full read and 0 on anything short, the -4 arm writes the result global and returns it, and a mode-0 size-0 call still lands 0 through 1 * 0 |
| a short read has already written the destination and advanced the cursor | **EXERCISED** | the dest digest shows the front overwritten and the tail stale, and the cursor line advances by the partial count - then a retry resumes mid-buffer rather than restarting |
| the recovery restore copies 0xE240 whole-image bytes and stops before group persistent bank A | **EXERCISED** | the real 002EF640 returns 0x2164280 and the copy lands there; the window digest and the 0x40-byte canary behind it are compared, so a copy one byte longer or shorter shows |
| the same restore copies nothing when the parent pointer is null, and returns normally | **EXERCISED** | RESTORE with the parent cleared changes neither the window nor the canary and produces the same output lines as the armed call |
| the enqueue refuses a queue count of exactly 8, not `>= 8` | NOT EXERCISED · scope | 00582540 is upstream of this suite - the fixture drives the read and restore bodies, not the queue |
| an empty completion underflows the queue count, and the same call's compaction then runs 255 `0x58`-stride shifts | NOT EXERCISED · scope | 00582240's count decrement and shift loop are queue machinery this suite never runs |
| the underflow and the `== 8` refusal compose — `0xFF` passes the `je` and the next enqueue writes slot `0xFF` | NOT EXERCISED | the composition needs both queue bodies driven in sequence; neither runs here |
| packet kind 8's auxiliary input is not clamped | NOT EXERCISED · scope | the 13-kind dispatcher 00582040 is not among this suite's entries |
| the queue compaction shifts `0x58`-stride entries down over the completed front | NOT EXERCISED · scope | inside 00582240, not driven |
| the load pipeline is a 16-state dispatch on `[02B40E14]` | NOT EXERCISED | 003BA7B0's jump table is read statically; the suite drives the read body it dispatches to, not the dispatcher |
| packet-9 acceptance refuses an in-flight chain and a zero length | NOT EXERCISED | 003BB440's two guards are dispatcher-arm behaviour, not exercised |
| packet-9 arms the chain at sub-state 1 with the packet's name, dest and length | NOT EXERCISED | same arm, same reason |
| the PC record is `0x210` of cursor + mode + `wchar_t[260]` path, over a shared byte vector | NOT EXERCISED | 008666B0's allocation shape is read statically; the suite scripts the file layer around the read it drives |
| `00580840` runs `00247510` only on the state-9 success arm, parent = `[rbx+0xC0]` | NOT EXERCISED · scope | the completion dispatcher is upstream of the read body; not driven |
| `00580EB0` is a 15-arm state dispatcher writing `[rbx+0xE9]`; state 9 selects message `0x17` | NOT EXERCISED | 00580EB0 is read statically; the suite's entries never reach it |
| `00583990` resolves result messages through `00D23DA0`, a `{id,kind}` table clamped to 32 entries | NOT EXERCISED · scope | message resolution sits behind the dispatcher, not driven |
| `00580840` is re-entered as the completion callback of packets the machine itself enqueues | NOT EXERCISED | a re-entrancy fact about arms 8/0xB; the dispatcher does not run |
| subtype `0x8001` stamps the selected slot byte at `[02CA99B8]+0x598` and the packet's `+0xEB` | NOT EXERCISED · scope | 0057FE80 is a different dispatch arm; not driven |
| `0057FE80` is a two-level dispatcher — outer `dword[msg]−1` bounded at `0x11`, subtype select nested in outer arm 12 | NOT EXERCISED · scope | the message pump is upstream of the read/restore bodies; not driven |
| subtype `0x12` clears `+0xD0` only when `qword[msg+0x10] == 0xA` | NOT EXERCISED · scope | a subtype arm of 0057FE80; the pump is not driven |
| subtype `0x1D` requires `+0xE0 & 0x10` clear and re-dispatches on `dword[[msg+0x10]]` to `00580A80`/`00580B40`/`00580CD0` | NOT EXERCISED · scope | a subtype arm of 0057FE80; the pump is not driven |
| subtype `0x8000` binds `edi*0xA0 + [+0x1C0]` into `+0xC8` when `*003BB3E0(slot) == 2`, else clears `[+0xC8]+0x100` | NOT EXERCISED · scope | a subtype arm of 0057FE80; the pump is not driven |
| `0x8001`'s tail derives `r8b` ∈ {7,8,9,0xA,0xFF} from `*info`/`[info+4]`/`+0xED`, then transitions to 1 or 0xE | NOT EXERCISED · scope | the commit arm's result-code derivation; the pump is not driven |
| subtype `0x8002` arms `+0xE0` bit 4 and calls `00244F00(rbx)` | NOT EXERCISED · scope | a subtype arm of 0057FE80; the pump is not driven |
| subtypes `0x8100`–`0x8102` re-dispatch on queue state `+0xE9 − 2` through table `0x460800` | NOT EXERCISED · scope | the second nested dispatch of 0057FE80; not driven |
| the `0x8100`–`0x8102` prelude sets `[02CA99E0]+0xCC = 4`, clears `+0xD8`, and runs `0057ED40` | NOT EXERCISED · scope | the same nested dispatch's shared prelude; not driven |
| `0057ED40` collapses `02CA99C0` to head-only when `+0xDC` bit 0 is set, else empties it | NOT EXERCISED · scope | the queue-collapse helper; the queue is not driven |
| outer ids 15 and 18 notify `+0xC0` through `00247510` with messages `0xF`/`0x12` | NOT EXERCISED · scope | outer dispatch arms of 0057FE80; the pump is not driven |
| outer id 14 selects dialog `0xC82`/`0xC84`/`0xC86` by `+0xEA` and `00394450()==3` | NOT EXERCISED · scope | the dialog arm of 0057FE80; the pump is not driven |
| `00582860` is the controller's own dispatcher — outer `dword[msg]−1` bounded at `0x12`, table `0x462F54` | NOT EXERCISED · scope | the controller dispatcher is upstream of the read/restore bodies; not driven |
| `+0x588` is allocated at controller init via `002497E0(2, 0xE240)`, exactly the backup size | NOT EXERCISED · scope | the init arm of 00582860; the allocation never runs in this suite |
| `+0x588` is freed at controller teardown via `003697F0` and nulled, with `+0x590` and the singleton | NOT EXERCISED · scope | the teardown arm of 00582860; not driven |
| `00582860` outer arm 18 is the teardown: persistence restore, normalize/reseed, sub-teardown, frees, singleton clear | NOT EXERCISED · scope | the teardown arm of 00582860; not driven |
| subtype `0x1D` payload-3 arm releases `+0xD8` and transitions to `0xD` in 8 of 13 queue states | NOT EXERCISED · scope | 00580A80 sits behind the 0x1D dispatch; not driven |
| subtype `0x1D` payload-`0xD` arm's `+0xEA==0` path maps `[payload+8]` to a transition or `+0xE0`-flag dispatch | NOT EXERCISED · scope | 00580B40 sits behind the 0x1D dispatch; not driven |
| `00580B40`'s `+0xEA!=0` path computes `(word[+0xF2]+word[+0xF4])*byte[+0xEC]+sbyte[+0xEE]+sbyte[+0xED]` and indexes `+0xEF` | NOT EXERCISED · scope | the scroll-index arm of 00580B40; not driven |
| subtype `0x1D` payload-`0xF` arm releases `+0xD8` then `00581350` releases `02CA99C8`'s `+0xE8` resource and plays a `+0xD0`-selected chime | NOT EXERCISED · scope | 00580CD0/00581350 sit behind the 0x1D dispatch; not driven |
| `00582B2C` is the controller's nested subtype dispatcher — `qword[msg+8]` selects `0xF`/`0x10`/`0x12`/`0x1D`/`>0x1D`, and `0x12` re-dispatches `qword[msg+0x10]` through table `0x462FA0` | NOT EXERCISED · scope | the controller's nested dispatch; not driven |
| the `0x12` payload arms release or clear one controller field apiece | NOT EXERCISED · scope | controller field lifecycle arms; not driven |
| the `0x8001` arm posts two packets — `+0xD0` (cb `00581490`) and `+0xF8` (cb `0057F360`) — then resolves message `0xE` into `+0xF0` and enters state 2 | NOT EXERCISED · scope | controller packet-posting arm; not driven |
| `00583040` self-posts into the queue dispatcher — when `+0xC1==0` it builds `+0xD8` = `00244F50(0x1C8, cb=0057FE80)` | NOT EXERCISED | the controller-to-queue cross-post; neither dispatcher is driven |
| `00583040`'s nested dispatch maps `dword[msg+8]` to `{0,1,2,3,0xFF}` — `1` selects `2` or `0xFF` by `+0xC1` | NOT EXERCISED · scope | 00583040 sits behind the controller's 0x1D arm; not driven |
| `005829C0` is the suspend path: it builds a `0x720` record when `02CA99C0==0` and arms `+0xC4` bit 1 | NOT EXERCISED · scope | controller arm 16; not driven |
| `00582AE9` opens dialog `0x870`/`0x871` by `+0xC1` and self-posts `0x8001` | NOT EXERCISED · scope | controller arm 19; not driven |
| `00581310` releases its argument and, when controller `+0xC4` bit 3 is set, runs `002CC9B0`→`002CC9C0` | NOT EXERCISED · scope | release helper behind the controller arms; not driven |
| `005832B0` builds the `"PS2D"` submission descriptor — memset, magic stamp, bounds, path formatting, three `005837F0` calls | NOT EXERCISED · scope | the save-write descriptor builder; a different entry family |
| `00583700`/`005837F0` write the slot directory and asset names into `controller+0x128`, gated on `02CA99B8` | NOT EXERCISED · scope | path builders; a different entry family |
| `00583930` posts `00244F50(0x5A0, cb=00582860)` carrying `{arg3, arg1!=0, arg2!=0}`; `00583920` returns `[02CA99E8]`; `00583260` posts `00244F50(0x178, cb=0057E4D0)` | NOT EXERCISED · scope | client-facing entry shims; not driven |
| the `005843E0`/`00584210` admission split is `(00394450()==3)` vs `byte[+0x57]&1`, not a `+0x18`/`+0xC4` bit-4 | NOT EXERCISED · scope | the corrected admission pair is save-side stash/restore machinery; not among this suite's entries |
| `00583CB0` backs up `0xE240` bytes from the active header to `[[02CA99B8]+0x588]+0x80` | NOT EXERCISED · scope | the suite drives the restore direction (00583C00) only; the backup half never runs |
| `00582040` admits the front packet through a 13-arm dispatch on `dword[+0xD8]` (table `0x46220C`); arm 1 alone copies packet `+0xE0`/`+0xE8` into queue `+0xC0`/`+0xC8`, so only a kind-1 packet carries its own completion callback and token | NOT EXERCISED · scope | the start dispatcher is upstream of the two driven bodies; no packet is started |
| `00582240` remaps the result two-stage — `dil` defaults to 0 for kinds 1–2 else `003BB420()`, `0017E470()` returns the stored status `[001D50D0()+0x10DC]`, and `(status, kind)` fix-ups override `dil` (status 1 or 3 with kind 7/9 → 8; status 2 with kind ≠4 → 3); `dil==4` zeroes 25 bytes at controller `+0x568`..`+0x580` | NOT EXERCISED · scope | the completion remapper never runs; the suite completes nothing |
| the completion callback runs `+0xC0(kind, dil, +0xC8)` only when `+0xDC` bit 1 is clear | NOT EXERCISED · scope | the suppression flag and callback call live in 00582240, which is never driven |
| whether any shipped caller mishandles either | OPEN QUESTION | no caller is driven; the claim is that the shape invites misreading, which a fixture cannot observe |

### `table_lookup` — 02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md

| claim | status | note |
|---|---|---|
| the stride is a u16 at `+0x08` | **EXERCISED** | driven at strides 0, 1, 0x10, 0x100 and 0x1234, where a byte read or a dword read gives a different row |
| the reference is a dword at `+0x0C` | **EXERCISED** | driven at several references including 0, which makes the resolve unusable |
| 40 registry slots are headers of this shape | NOT EXERCISED | an image-wide census over the other 39 slots; this pilot plants one slot of its own |
| 226 functions perform the lookup | NOT EXERCISED | the same census; one worked instance is executed and the other 225 are not |
| the band is mixed | NOT EXERCISED | a claim about what neighbouring registry slots hold, which nothing here reads |
| the failure path dereferences a null base | **EXERCISED** | driven with a null slot and with an unresolvable reference, over a fixture page at address 0, plus a one-sided probe with no such page where the shipped bytes fault |
| the resolver zero-extends its reference and adds a 64-bit base | **EXERCISED** | driven at references up to 0xFFFFFFFF and at bases above 4 GB, comparing the full 64 bits |
| the encoder subtracts the same global read as a DWORD, so the two are inverses only below 4 GB | **EXERCISED** | driven in both directions at a base of 0x100000000, where the round trip does not return the reference |
| the exact round-trip condition is `((p - base) mod 2^64) < 2^32` | **EXERCISED** | the existing base cases establish the algebra: the encoder reads ECX and the resolver adds a qword, so encode(p) = (uint32)(p - base) and decode(x) = base + zext32(x), BOTH MODULAR. Driven at bases 0, 0x10000000, 0x110000000 and 0xFFFFFFFF against references from 0 to 0xFFFFFFFF. The WRAP WINDOW - a base near 2^64 where the distance wraps - is EXP-076's control, not this pilot's; no case here drives it, and the row's earlier wording was corrected because of exactly that gap |
| the header carries a `uint32` row count at `+0x04`, and nine consumers bound-check on it | NOT EXERCISED | an image-wide census claim - FABLE's J-A run, re-verified 2026-09-20 over 1,799 band loads with three bound-checkers re-read in the image. This pilot drives one lookup; it does not census consumers and its worked instance reads no count |
| `+0x00` is `slotCount` — the index bound of the encoded-pointer array at `+0x04` — and `+0x02` is a reserved header word; headers are not uniform across band families | NOT EXERCISED | an image-wide census claim - function-list census over all 38,161 bodies attributes +0x00 to four bound-guard readers and +0x02 to zero band-header readers; this pilot does not census consumers |
| the initializer retains a backing pointer above 4 GiB in the record's DIRECT fields | NOT EXERCISED · scope | EXP-077's result, not this pilot's - the arena initializer 00369D30 is not driven here; the contract consumes it in section 13 after re-verifying its body hashes against the image |
| what EXP-077 shows about ENCODED links at a high address | OPEN QUESTION | nothing, and EXP-078 is the experiment that drives them - neither is this pilot's; it never reaches the arena |
| the neighbour unlink stores through the DECODER's output, so a high block writes to its truncated low address | NOT EXERCISED · scope | 0036C9D0 is not driven here. This pilot executes the decoder and encoder THEMSELVES, which is where the truncation comes from - but the consequence, a store through the truncated pointer, belongs to the arena and is EXP-078's |
| the failing fields are the neighbour links `+0x0C` / `+0x10`, distinct from the free-list links `+0x04` / `+0x08` | NOT EXERCISED | arena block fields; this pilot drives the authored-table lookup, which has neither |
| a low mirror leaves the mirrored bytes **unchanged** | NOT EXERCISED | EXP-078's intervention, and a limit on ITS claim rather than a behaviour any suite drives |
| a return-value-only comparison passes a broken predecessor link | NOT EXERCISED | a statement ABOUT test design, and one this pilot should heed rather than test: section 16 now says an arena suite must assert links, not returns |
| an unlinked block is tagged `0xFF99` over its header word **only when the caller's `edx` is non-zero** | NOT EXERCISED · scope | read from 0036CA92; the arena is not driven here. The claim was NARROWED on 2026-09-13 (the tag is conditional on edx, not unconditional) and the verdict is carried across unchanged: narrowing what a claim asserts does not change the fact that this harness never drives the arena |
| the `+0x3E` word is a corruption guard every writer stores zero to and every reader compares against zero — nonzero is not a state the code produces | NOT EXERCISED · scope | settled by the type store's guardWord census (OPUS, all 38,161 bodies) and an independent re-read of the five report gates and the writers; the arena is not driven here |
| the free-list links are an encoded doubly-linked chain — `+0x04` is `prev`, `+0x08` is `next` | NOT EXERCISED · scope | a static body-read claim - the two mirror inserters 0036B670/0036B730 were loaded but never reached (EXP-078); the arena is not driven here |
| the STATIC delivery populates 39 of the 47 band slots, through a fully enumerated binding map | NOT EXERCISED | a static plumbing-census claim - delivery stub 00238850 and callback 00236C30's 35 bindings plus four inner-binder slots; this pilot does not drive the STATIC load |
| where the arena actually sits in a running game | OPEN QUESTION | not established, and live |
| the worked instance resolves the same reference TWICE and tests only the first result | **EXERCISED** | the trace carries every resolver call; the control that resolved once failed on 43 lines |
| the row address is built in 32-bit arithmetic and truncates the resolved base | **EXERCISED** | driven at a stride and index whose product is exactly 2^32; the control doing it in 64 bits failed, but only after the harness's row read was widened from a 32-bit address to a 64-bit one, which had been performing the truncation itself |
| the timer multiplies the row byte by the .data dword at 01DFE0B4, which the image holds as 1 | **EXERCISED** | driven at scales 0, 1, 2 and -1, and at the image's own value by a case that runs before any fixture reset |
| nothing observed live | OPEN QUESTION | none exists |

### `target_buffer` — 07-Combat-Action/CONTRACT-battle-target-buffer.md

| claim | status | note |
|---|---|---|
| size 0x208 | **EXERCISED** | all 520 bytes compared on 27 dumps, and the reconstruction asserts the size at COMPILE time too - the +0x01 field is UNALIGNED and a naturally-aligned struct is 0x20A, which would shift every byte the dump compares while leaving both sides self-consistent |
| cap 32 | **EXERCISED** | driven across the whole accepting range and past it, at counts 31, 32, 33, 40 and 100 |
| stride 16 | **EXERCISED** | every entry position in every dump depends on it; a wrong stride moves all 32 |
| count is signed | **EXERCISED** | driven at -1, -2 and -3, where the sign is exactly what puts the write outside the structure; an unsigned count would refuse instead |
| flags bit 0 survives reset | **EXERCISED** | reset driven over five flag patterns from a 0xCD-filled buffer; 518 of the 520 bytes must be zero afterwards and bit 0 must survive |
| flags bit 0 is the `+0xBC0` refresh-skip gate | NOT EXERCISED | static claim added 2026-09-22 (SWE2-CONTRACT): the consumer (00324F32 in 00324F20) and the second setter (00172CA1 in the unit initializer) are perception-cache paths outside this pilot - it drives the three buffer operations on planted buffers, not the refresh gate that reads the flag |
| find returns -1 when absent | **EXERCISED** | driven on a full buffer with an absent actor, and on empty and negative counts |
| find returns the index when present | **EXERCISED** | driven at the first, last and middle entries of a full buffer |
| a consumer relies on the `-1` | NOT EXERCISED | BattleStats_ModifyHPAndProcessLethalState is not run here. What would exercise it is a harness over the HP write, which needs a BattleStats record this one does not build |
| the return cannot distinguish refusal | **EXERCISED** | the accepted 32nd append and the refused 33rd are adjacent cases and both return 32 - and the counts above the cap return themselves, which is where the contract's wording was narrower than the code |
| two instances per unit | **EXERCISED** | a whole 0xF50 unit is planted, 0xCD throughout, with both interior buffers driven at +0x778 and +0xBC0 and the ENTIRE unit compared after each step - so an operation that escaped its own 0x208 shows as a changed byte somewhere it has no business being. The two are driven against each other: entries appended to one are searched for in the other and must not be found, and resetting one must leave the other intact. NEGATIVE CONTROL, and the reason this row is not a green test that proves nothing: rebuilt with /DBU_TB1=0xBC8, moving the second buffer eight bytes, the differential FAILS with two mismatches - exactly the two unit dumps taken after a write to that buffer, while the dump before any write and the one after only buffer-0 writes still agree |
| caller sets | NOT EXERCISED | a census settles it and a census is not an execution |
| nothing runs live | OPEN QUESTION | none exists |

### `transform` — 00-Engine-Core-Runtime/CONTRACT-transform-primitives.md

| claim | status | note |
|---|---|---|
| the point transform's law | **EXERCISED** | 123 point cases, 3 designed and 120 randomised, every one compared against the shipped bytes running at their own virtual address |
| the point's `w` is ignored and replaced by `[01EF93FC]` | **EXERCISED** | driven with distinct in[3] values; the outputs are byte-identical, which is the designed case for this row. The claim text now names the LOAD cell - what the suite exercises is that in[3] does not reach the output; the load itself is read statically |
| every shipped writer of that cell stores `1.0f` | NOT EXERCISED | a static range-aware store census over .text - the harness plants the cell, it does not observe its writers |
| there is no perspective divide | **EXERCISED** | all four components are compared, so a divide on any of them would show |
| the composer computes `b × a` | **EXERCISED** | 123 compose cases, including the designed case that separates the two orders outright rather than merely preferring one |
| the composer is ONLY a matrix multiply — no other path exists in its 567 bytes | **EXERCISED** | all 123 compose cases compare the full 64-byte result, and the shipped body itself was read line by line: one control edge (the row loop), one call (the stack-cookie check), no global but the cookie — there is no other path for a case to miss |
| aliasing is safe on the composer | **EXERCISED** | all three aliasing modes are driven - out distinct, out == a, out == b - and compared against each other and against the shipped result |
| the composer writes exactly 64 bytes | **EXERCISED** | the 16 bytes behind the destination are sentinel-filled and compared; a 65th byte would show |
| the point transform makes four deposits | **EXERCISED** | five buffers are compared per point case - the caller's out AND all four deposits. This is the row the suite exists for: a reconstruction filling only out passes any output test and starves every workbench consumer |
| the accumulator holds the sum WITHOUT the translation row | **EXERCISED** | settled BY the suite rather than assumed: depositing the finished value there - the obvious reading - fails all 123 point cases on that buffer and no other |
| the four deposit slots are SHARED, not owned here | NOT EXERCISED | a writer/reader count over the image. This suite proves these two functions write them; it cannot establish who else does |
| the matrix at `022D91B0` is row-major with translation in row 3 | **EXERCISED** | the law is driven with the four rows set to distinguishable values, so a different convention changes the output on every case |
| the workbench deposit slots are idle at the TITLE SCREEN | NOT EXERCISED | a live observation of the globals. This suite runs offline and neither reproduces nor tests it |
| the deposits are read — by the workbench family, not the callers | NOT EXERCISED | a static census over the image - the harness proves the deposits happen, not who reads them |
| zero caller fns read the deposits as values | NOT EXERCISED | a static caller census - the suite drives the functions, not their callers |
| what the matrix is: the caller's current transform; and who builds the 105 non-global sources: the caller's own object or a fresh composition | NOT EXERCISED | a static per-site producer census over all 116 call sites - the suite drives the two primitives, not their callers' matrix sources |
| any runtime observation of either function EXECUTING | OPEN QUESTION | section 15 records UNKNOWN. The live session observed the state of the globals, not these bodies running |

### `verb_dispatch` — 01-Script-VM-Native-Bridge/Verb-Dispatch/CONTRACT-verb-dispatch-abi.md

| claim | status | note |
|---|---|---|
| the id splits 4/12 with an **arithmetic** shift | NOT EXERCISED | inside 002621D0, which this pilot does not run. The split is read statically; what this pilot drives is what the two halves are then used for |
| the family array is at `0x02B57EF0` and is indexed `[array + family*8]` with a null check | **EXERCISED** | the array is planted at that exact virtual address - the accessors reach it by a hard-coded lea, so the fixture cannot relocate it. A null entry is driven on family 1 and an unset entry on families 2 and 15, and BOTH SIDES of the array are driven at families -1 and 16, where real tables are planted so the case has an answer |
| the bound is `command >= count` against the table's first dword, and failure returns NULL | **EXERCISED** | driven at count-1, count and count+1 for counts 0, 1, 3 and 300, and at the two NEGATIVE counts -1 and 0x80000000 where a signed compare refuses every command and an unsigned one admits every command |
| the record is 32 bytes at `table + 8 + 32*command`, callbacks at `+0x00`/`+0x08`/`+0x18` | **EXERCISED** | all three accessors driven over records whose four slots hold four distinct values, INCLUDING the +0x10 slot the shipped tables leave NULL. Commands 256 and 299 put the third byte of the index in play, and the negative commands settle the reading of `inc rax` |
| the count dword is read as SIGNED | **EXERCISED** | counts of -1 and 0x80000000 are driven against command 0 in all three accessors and return NULL; an unsigned compare would admit every command |
| the bound is one-sided — a negative command passes it and reads BEFORE the table | **EXERCISED** | commands -1 and -2 at count 3, with thirty-two distinct qwords planted immediately before the table so the read has a value to compare rather than a zero. `result` at -1 returns the table's own count word |
| the family array is unbounded in BOTH directions | **EXERCISED** | families -2, -1, 15 and 16 are driven, with real tables planted at the pointer immediately before the array and the pointer immediately after it |
| the accessors write nothing | **EXERCISED** | an FNV-1a over all 64 KB of the window is compared against the original on every accessor case, not only on the initialiser ones |
| `003DC2D0` writes exactly 128 bytes, and its first store is dead | **EXERCISED** | driven twice - over a zeroed window and over one already full of 0xEE - with the whole-window hash compared, so a write outside the 128 bytes differs. That the first store is dead is the campaign's finding: the mutant skipping it compiles to identical code |
| four opcodes, three bytes each, and `0x5E` jumps into `0x5D`'s body | NOT EXERCISED · scope | the interpreter 0025E4C0 is not driven by this pilot |
| the pre-decode ZERO-extends, so the family is `0..15` by construction | NOT EXERCISED | read statically at 0025E5AF. It is the reason the one-sided guard this pilot DID execute is unreachable from bytecode - so the pilot depends on this claim without testing it, which is what this row records |
| the lifecycle, the phase byte and the one-value push rule | NOT EXERCISED · scope | the executor 002621D0 is not driven. This is the half of the contract that stays on static evidence |
| the callback argument registers, and that `poll` takes three | NOT EXERCISED | no callback is called here; the accessors only return their addresses |
| the five tables and their counts; the `+0x10` slot NULL in all 1,960 | NOT EXERCISED | a corpus measurement over the shipped tables, which live in .data and are written at runtime. The fixture deliberately plants that slot NON-NULL instead, so a slot confusion is visible |
| `0016D6A0` stands in for an absent callback | NOT EXERCISED | an identity of the values in the shipped tables, not of the accessor that returns them |
| the stub holds exactly 34 of the 5,880 callback slots across 33 records — 9 `begin`, 0 `poll`, 25 `result`; 18 records are wholly inert | NOT EXERCISED | a corpus measurement over the shipped .data tables, like the count/NULL row above - the fixture plants its own records and cannot bear on what the shipped image ships |
| no shipped caller reaches `002621D0` or an accessor with a non-16-bit id — all three executor calls pass `movzx r9d, bx`; the accessors see only the split halves (`ecx` family, `edx` command & 0xFFF) | NOT EXERCISED | a shipped-call-graph claim; the fixture drives the accessors directly with ids no shipped caller can produce, which is exactly what this census bounds |
| the dispatch half executed in isolation | **EXERCISED** | THIS PILOT IS THAT EXECUTION - 73 cases, 0 mismatches, nothing scripted |
| any execution of the LIFECYCLE half, or any live observation | NOT EXERCISED | not this pilot's coverage to claim - EXP-085 executes the shipped 002621D0 plus four real leaf callees (35 cases, 0 mismatches, 9/9 mutants, a different instrument). What remains open is live observation - section 13's stated class is isolated original-code and the live rung is still queued |
| what the `+0x10` slot was for | NOT EXERCISED | VA-1, and an executed accessor cannot answer it: the slot is never read by any of the three |

### `verb_marshal` — 01-Script-VM-Native-Bridge/Verb-Dispatch/CONTRACT-verb-dispatch-abi.md

| claim | status | note |
|---|---|---|
| the id splits 4/12 with an **arithmetic** shift | NOT EXERCISED | the decoder is not run; the adapters consume the decoded command, not the split |
| the family array is at `0x02B57EF0` and is indexed `[array + family*8]` with a null check | NOT EXERCISED | the accessors are not run; the tables are read from the image, not through the array |
| the bound is `command >= count` against the table's first dword, and failure returns NULL | NOT EXERCISED | no accessor executes |
| the record is 32 bytes at `table + 8 + 32*command`, callbacks at `+0x00`/`+0x08`/`+0x18` | **EXERCISED** | the member set is derived by walking all five tables with exactly this layout - a wrong stride or callback offset lands mid-record and the bytes that follow fail the marshalling grammar instead of executing as adapters |
| the count dword is read as SIGNED | NOT EXERCISED | the walk unpacks it signed (<i) but no bound-checking accessor runs; the claim is about the accessors |
| the bound is one-sided — a negative command passes it and reads BEFORE the table | NOT EXERCISED | no accessor executes |
| the family array is unbounded in BOTH directions | NOT EXERCISED | no accessor executes |
| the accessors write nothing | NOT EXERCISED | the three accessors are not run; this pilot's bodies are the marshalling adapters, which do write - to the VM stack - and those writes are recorded |
| `003DC2D0` writes exactly 128 bytes, and its first store is dead | NOT EXERCISED | the initialiser is not run |
| four opcodes, three bytes each, and `0x5E` jumps into `0x5D`'s body | NOT EXERCISED · scope | the interpreter is not driven |
| the pre-decode ZERO-extends, so the family is `0..15` by construction | NOT EXERCISED | read statically; the tables are taken as fixed addresses |
| the lifecycle, the phase byte and the one-value push rule | PARTIAL | the pushes each adapter makes (pre-native pushes and the result tail) are recorded per member, so the push side is observed; the phase byte and the lifecycle executor 002621D0 are not driven |
| the callback argument registers, and that `poll` takes three | **EXERCISED** | the claim this pilot exists for: rcx/rdx/r8/r9, xmm0-3 and the four stack slots are sampled at every native-call boundary with every inbound register and popped slot distinctly tagged - the per-member arg map is produced by execution, and the three-argument poll shape is visible in it |
| the five tables and their counts; the `+0x10` slot NULL in all 1,960 | PARTIAL | the five counts are consumed to size the walk and every record is iterated; the +0x10 slot is never read, so its NULL-ness is not observed |
| `0016D6A0` stands in for an absent callback | NOT EXERCISED | an identity claim about a value in the tables; this harness enumerates callbacks and executes those passing the grammar - the 3-byte ret does not pass it |
| the stub holds exactly 34 of the 5,880 callback slots across 33 records — 9 `begin`, 0 `poll`, 25 `result`; 18 records are wholly inert | NOT EXERCISED | the walk visits every record but never classifies a callback as the stub - stubbed slots fail the marshalling grammar and are skipped, so the census is not observed |
| no shipped caller reaches `002621D0` or an accessor with a non-16-bit id — all three executor calls pass `movzx r9d, bx`; the accessors see only the split halves (`ecx` family, `edx` command & 0xFFF) | NOT EXERCISED | a shipped-call-graph claim; this pilot executes adapters found by walking the tables, not the interpreter call sites the claim enumerates |
| the dispatch half executed in isolation | NOT EXERCISED | that is diff_verb_dispatch's claim; this pilot executes the marshalling half instead |
| any execution of the LIFECYCLE half, or any live observation | NOT EXERCISED · scope | the executor 002621D0 is not driven and no breakpoint has been taken |
| what the `+0x10` slot was for | NOT EXERCISED | VA-1; no marshal adapter reads that slot, so execution cannot answer it |

### `widget_construct` — 16-UI/Widget-Object-Model/CONTRACT-widget-object.md

| claim | status | note |
|---|---|---|
| handler at `+0x00`, default `005C5230` | **EXERCISED** | cases pass proc `0` and two real procs; `+0x00` is inside the 192 compared bytes, and the null-proc substitution is a path the run actually takes |
| the constructor sends id 1 | **EXERCISED** | the proc is now a RECORDING stub: it captures the object and message pointer it was handed and counts its calls. 320 of 320 cases send exactly ONE message, all 24 bytes are compared, and the two payload qwords are randomised per case so a reconstruction that hardcoded them would fail |
| `+0x18` child / `+0x20` sibling | PARTIAL | both offsets are inside the compared window and must agree after construction; the recursion in `002473B0` that gives them their meaning is never run |
| destroy is two-phase, 15 then 18 | NOT EXERCISED | a different entry point -- this harness constructs only |
| the deferred destroy path `00244DD0` also sends `{15}` — to self via `[rbx]` — but schedules the rest instead of running `{18}`/`00245020` inline, so 15-before-18 holds on both destroy paths | NOT EXERCISED | the deferred destroy arm; this harness constructs only |
| `00244DD0` schedules the deferred completion: `+0x68` message/record pointer, `+0x74` start tick `[0208F570]`, `+0x70` delay = `u16[+2] * 60/1000` (ms→60 Hz ticks), `+0x78`/`+0xB8` timescales | NOT EXERCISED | the deferred scheduler's field writes; this harness constructs only |
| `00244DD0`'s `+0x7C` low-nibble is a mode field: 0/3 schedule, 2 recomputes the deadline, 1 bails before the tail | NOT EXERCISED | the mode dispatch inside the deferred arm; this harness constructs only |
| 297 sites / 267 handlers / 32 ids | NOT EXERCISED | an image-wide census from `widget_messages.py`, not a behaviour any differential executes - renamed from the superseded 280/251 figure the contract struck |
| the pool is 112 × `0x120` | NOT EXERCISED | the pool is allocated at `00244FA4` and `00244FAB`; the constructor is handed a buffer |
| `+0xB4` is a half-rate phase counter: constructor sets `1` under HALFRATE **and** inside the sim tick; the walker `00248030` pins it to `0` outside HALFRATE and increments it under it; `001EDEC0(x)` gates id-2 work on `x` being even | PARTIAL | the constructor half of it is exercised -- `pred_a`/`pred_b` are driven through every combination and `+0xB4` is inside the 192 compared bytes, so a reconstruction that got the AND wrong fails. The walker `00248030` and the `001EDEC0` gate are different entry points this harness never runs |
| the constructor calls the proc **before** writing `+0xB4` | NOT EXERCISED | the recording stub captures the object and message POINTERS and counts calls; it does not snapshot `+0xB4` at call time, so the order of the two effects is not observed. Making it observable needs the stub to read `self+0xB4` when it is called -- the reconstruction's own comment records this as a divergence the caller must repair |
| `002445D0` roots on `dword[arg]==1`: `+0x40 | NOT EXERCISED | 002445D0 is the root-flag setter, a different entry point - this harness constructs only. (The claim string is truncated at the contract row's first `|`; the map key matches what parity_status.py reports.) |
| `00248220` tail-appends on `+0x18`/`+0x20`, sets `child+0x10`=parent, `parent+0x30`++; propagates parent bit 5 through `002463F0`+`002418E0`; `+0x40 \ | NOT EXERCISED | 00248220 is the attach helper, not the constructor. (Truncated claim string, as the tool reports it.) |
| `002463F0` is a pre-order recursive visitor: `call rdx` then `+0x18`/`+0x20` descent | NOT EXERCISED · scope | 002463F0 is the subtree visitor; not among this suite's entries |
| `00247490` prunes subtrees: gate `+0x40` bit 1 **and** bit 0 `!= edx`; flips bit 0, fires `[+0x00]` callback, recurses only on pass | NOT EXERCISED · scope | 00247490 is the gated prune; not among this suite's entries |
| `00582790`'s 12-slot binding is `00249580`: first-fit over `02090790`, 12 × `0x20` slots, bit-0 busy | NOT EXERCISED | the batch-slot allocator is a different subsystem from the widget pool this harness constructs through |

### `workbench_save` — 00-Engine-Core-Runtime/CONTRACT-transform-workbench-save-restore.md

| claim | status | note |
|---|---|---|
| Save is variadic: ecx is the count, pointers in rdx, r8, r9 and then the stack | **EXERCISED** | driven at 1, 2, 3, 4, 5 and 8 items. Three or fewer never leaves the registers, so the counts past three are the ones that exercise the home-area spill and the stack slots |
| Save copies sixteen bytes per pointer | **EXERCISED** | every saved value is compared in full, over a scratch block filled so that neighbouring offsets differ; a 15- or 17-byte copy changes the value or the block |
| Save assigns depth and indexes from zero, so a second Save overwrites the first in place | **EXERCISED** | driven directly: save two rows, save one different row, restore, and compare. This is the contract's sharpest hazard and it is the case the suite was built around |
| a count of zero still assigns depth | **EXERCISED** | the zero case is driven and the depth read back; the shipped body jumps over the loop to the same store |
| Restore writes each saved 16 bytes back through its saved pointer | **EXERCISED** | every case clobbers the scratch block between save and restore, so a restore that did nothing would leave the clobber visible in the block comparison |
| Restore zeroes depth, and is therefore idempotent | **EXERCISED** | restore is driven twice with no save between, and the depth and the whole block are compared after each |
| the depth counter is touched by exactly four instructions image-wide | NOT EXERCISED | an image-wide sweep. A run of these two functions cannot establish what else does or does not reference an address |
| the nine users DO call one another — just never while holding the workbench | NOT EXERCISED | a static measurement over the call graph and every user's Save-to-Restore window: 0044BAC0 transitively reaches six of the other eight, and across all nine held windows there are four calls, none to a user, none to anything reaching one, and no indirect call at all. This pilot drives the pair, not its nine callers |
| four of the nine restore by TAIL JUMP, not by call | NOT EXERCISED | read from the bytes at 0026F413, 003AFFAB, 00431F0A and 0046242E. The pilot calls Save and Restore directly and so exercises neither form of the callers' control flow |
| nesting cannot happen on the direct call graph | NOT EXERCISED | a reachability argument over the edge list, and the contract already records that it holds for DIRECT calls only. No run of this pair reaches it |
| `022D8F0C` is read and written by functions with no relationship to the workbench | NOT EXERCISED | another image-wide sweep, and the contract leaves the question it raises open |
| any runtime observation | OPEN QUESTION | none exists |

## Certification

```text
PARITY CERTIFIED  requires  every APPLICABLE dimension COVERED
                  and       INTEGRATION covered AGAINST THE RUNNING GAME
```

**0 of 45 pilots certified.**

## Per pilot

### `achievement_counters` — entry `00316A50`

- **contract:** `20-Platform-Online-Achievements/CONTRACT-achievement-counters.md`
- **covered:** 5 of 11 — CALCULATION, CONTRACT, EDGE-CASE, STATE-TRANSITION, STRUCTURAL
- **not applicable:** 4 — PRESENTATION, RNG, SERIALIZATION, TIMING

  | not covered | what would cover it |
  |---|---|
  | FULL-SUBSYSTEM | 003165C0 is not reconstructed, and no caller of the update path is |
  | INTEGRATION | the award callee and the chain-walking lookup are answered; nothing here reaches a platform service |

### `actor_pool` — entry `00266AD0`

- **contract:** `04-Actor-Entity/CONTRACT-actor-record-pool-and-region-map.md`
- **covered:** 4 of 11 — CALCULATION, EDGE-CASE, STATE-TRANSITION, STRUCTURAL
- **not applicable:** 4 — PRESENTATION, RNG, SERIALIZATION, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | derived from the map below |
  | FULL-SUBSYSTEM | as above |
  | INTEGRATION | the initialiser 00266530 and the allocator 00267A20 are out of scope; this is the carve alone |

### `angle_wrap` — entry `003A1C50`

- **contract:** `06-Movement-And-Navigation/CONTRACT-facing-and-steering.md`
- **covered:** 3 of 11 — CALCULATION, EDGE-CASE, STRUCTURAL
- **not applicable:** 4 — RNG, SERIALIZATION, STATE-TRANSITION, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | 3 of 7 testable claims exercised, of the contract's 9 section-15 rows (2 record open questions); unexercised: the record is `0x80`, inline, two of them; push/pop are the only slot callers; mode 4 reads the `FrameLimit` base |
  | FULL-SUBSYSTEM | two normalisers of the facing subsystem |
  | INTEGRATION | no real movement update drives either form |
  | PRESENTATION | no character is turned |

### `auto_status` — entry `0030FED0`

- **contract:** `10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md`
- **covered:** 4 of 11 — CALCULATION, EDGE-CASE, STATE-TRANSITION, STRUCTURAL
- **not applicable:** 4 — PRESENTATION, RNG, SERIALIZATION, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | derived from the map below |
  | FULL-SUBSYSTEM | one function of the status family; what a status MEANS is the cascade's contract and is supplied here |
  | INTEGRATION | eight callees are scripted, including the status cascade and the applier, which are subsystems of their own |

### `battle_mode` — entry `0030D9A0`

- **contract:** `00-Engine-Core-Runtime/Battle-Runtime-Mode/CONTRACT-battle-runtime-mode.md`
- **covered:** 4 of 11 — CALCULATION, EDGE-CASE, STATE-TRANSITION, STRUCTURAL
- **not applicable:** 3 — PRESENTATION, RNG, SERIALIZATION

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | derived from CONTRACT_MAP below, not declared |
  | FULL-SUBSYSTEM | two functions of the subsystem, not the setters or the save path |
  | INTEGRATION | the ladder's callee is scripted and its 21 consumers are absent - the mode's meaning is entirely in them |
  | TIMING | nothing here establishes WHEN a consumer asks for the mode; that is the field runtime pass's contract |

### `bazaar` — entry `0030B270`

- **contract:** `12-Items-Equipment-Shops-License/CONTRACT-bazaar-unlock-and-purchase.md`
- **covered:** 4 of 11 — CALCULATION, EDGE-CASE, STATE-TRANSITION, STRUCTURAL
- **not applicable:** 4 — PRESENTATION, RNG, SERIALIZATION, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | derived from the map below |
  | FULL-SUBSYSTEM | the shop UI, the recipe tables and the caller that decides when to refresh are all out of scope |
  | INTEGRATION | three callees are scripted; what they do beyond returning a number is not proved here, and neither is the save round trip FZ-3 asks about - only the arithmetic that makes it hold |

### `binding_publish` — entry `00195DF0`

- **contract:** `15-Input/Binding-Profiles/CONTRACT-binding-profiles.md`
- **covered:** 4 of 11 — CALCULATION, EDGE-CASE, STATE-TRANSITION, STRUCTURAL
- **not applicable:** 4 — PRESENTATION, RNG, SERIALIZATION, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | derived from the map below: two of twelve testable claims are exercised, because the contract covers ten operations and this suite drives one |
  | FULL-SUBSYSTEM | assignment 00198A00 and the translator 00197160 are not reconstructed, which section 16 already says |
  | INTEGRATION | nothing upstream fills 01F80F90 here and nothing downstream reads 01F80130; the operation is driven in isolation |

### `body_pool` — entry `003DA8A0`

- **contract:** `06-Movement-And-Navigation/CONTRACT-movement-body-pool.md`
- **covered:** 4 of 11 — CALCULATION, EDGE-CASE, STATE-TRANSITION, STRUCTURAL
- **not applicable:** 4 — PRESENTATION, RNG, SERIALIZATION, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | derived from the map below: the pool's 128-body EXTENT is computed from an address rather than driven, and a fixture of eight cannot reach it. Every other row is exercised |
  | FULL-SUBSYSTEM | nothing that consumes a body is reconstructed, and the pool is built by this fixture rather than by whatever builds it in the game |
  | INTEGRATION | the two initialisation callees are answered, and 002E3500 - which creates a body FOR a record - is not driven at all |

### `character_publish` — entry `001FB120`

- **contract:** `17-Presentation-Rendering/CONTRACT-character-transform-publish.md`
- **covered:** 5 of 11 — CALCULATION, CONTRACT, EDGE-CASE, STATE-TRANSITION, STRUCTURAL
- **not applicable:** 3 — RNG, SERIALIZATION, TIMING

  | not covered | what would cover it |
  |---|---|
  | FULL-SUBSYSTEM | the reader of the other bank, and whatever flips the parity byte, are outside this operation and are not exercised |
  | INTEGRATION | the accessor 00189120 is answered and no caller is reconstructed; nothing here reaches a renderer |
  | PRESENTATION | nothing is drawn - this writes the bank a renderer would later read |

### `class_descriptor` — entry `0063D550`

- **contract:** `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/CONTRACT-phyre-class-descriptor.md`
- **covered:** 4 of 11 — CALCULATION, EDGE-CASE, STATE-TRANSITION, STRUCTURAL
- **not applicable:** 4 — PRESENTATION, RNG, SERIALIZATION, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | derived from CONTRACT_MAP below, not declared |
  | FULL-SUBSYSTEM | the reset, not the destructor and not the generated families |
  | INTEGRATION | what registers into which list is the whole reflection subsystem |

### `class_descriptor_dtor` — entry `00633390`

- **contract:** `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/CONTRACT-phyre-class-descriptor.md`
- **covered:** 4 of 11 — CALCULATION, EDGE-CASE, STATE-TRANSITION, STRUCTURAL
- **not applicable:** 4 — PRESENTATION, RNG, SERIALIZATION, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | derived from CONTRACT_MAP below, not declared |
  | FULL-SUBSYSTEM | the destructor, not the generated deleting-destructor families |
  | INTEGRATION | what the +0x70 sub-object and the +0x60 handler do is scripted |

### `coast_down` — entry `00424080`

- **contract:** `17-Presentation-Rendering/CONTRACT-coast-down-latch.md`
- **covered:** 4 of 11 — CALCULATION, EDGE-CASE, STATE-TRANSITION, STRUCTURAL
- **not applicable:** 2 — RNG, SERIALIZATION

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | 9 of 10 testable claims exercised, of the contract's 12 section-15 rows (2 record open questions); unexercised: 0020E600's result being dereferenced unchecked, which crashes both sides |
  | FULL-SUBSYSTEM | one operation; the counter's writer at 004256E0 is read but not run, and the render record's other consumers are outside it |
  | INTEGRATION | no caller runs, the record pool is planted, and the tail's two lookups are supplied - so nothing here shows a character gliding |
  | PRESENTATION | this operation is presentation-side and nothing is drawn |
  | TIMING | §9 says the decay is per CALL and so frame-rate dependent by construction. The suite drives calls, so it reproduces the decay but says nothing about how many calls a real frame makes |

### `commit_action` — entry `0030F760`

- **contract:** `07-Combat-Action/CONTRACT-commit-action.md`
- **covered:** 4 of 11 — CALCULATION, EDGE-CASE, STATE-TRANSITION, STRUCTURAL
- **not applicable:** 4 — PRESENTATION, RNG, SERIALIZATION, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | derived from the map below |
  | FULL-SUBSYSTEM | the commit is one of the action family's entry points; the cancel it calls and the resolution that follows are contracts of their own |
  | INTEGRATION | all nine callees are scripted; no real target buffer, no real cancel, and no caller is reconstructed |

### `field_gate` — entry `0025D9E0`

- **contract:** `04-Actor-Entity/CONTRACT-field-runtime-pass.md`
- **covered:** 4 of 11 — CALCULATION, EDGE-CASE, STATE-TRANSITION, STRUCTURAL
- **not applicable:** 3 — PRESENTATION, RNG, SERIALIZATION

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | derived from CONTRACT_MAP below, not declared |
  | FULL-SUBSYSTEM | the first 120 bytes of a 1,297-byte pass |
  | INTEGRATION | the pass itself - the drive loop, the publish, the 49 callees - is not executed |
  | TIMING | the once-per-frame cadence is the caller's, and the pass is not driven across frames |

### `field_music` — entry `003EAA70`

- **contract:** `18-Audio/CONTRACT-field-music-selection.md`
- **covered:** 2 of 11 — CALCULATION, EDGE-CASE
- **not applicable:** 5 — RNG, SERIALIZATION, STATE-TRANSITION, STRUCTURAL, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | 7 of 8 section-15 rows exercised; capturing input bytes does not exercise the table producer, binding or ownership |
  | FULL-SUBSYSTEM | one entry point of field music; the subsystem's entry points are not enumerated |
  | INTEGRATION | EXP-009: the inputs, the table AND THE ORACLE are now the game's own -- 2 distinct inputs captured at its own call site (field 227 progress 68 -> 100; field 253 progress 1580 -> 20), each read from rax at its own ret 126 times, and the reconstruction agrees on both. Native substitution, producer/lifetime, state-transition and scheduling consequences remain unverified; the observations are two input conditions |
  | PRESENTATION | nothing shows the same music would play |

### `field_record` — entry `00377C20`

- **contract:** `03-World-Area-Field/CONTRACT-field-record-accessors.md`
- **covered:** 3 of 11 — CALCULATION, EDGE-CASE, FULL-SUBSYSTEM
- **not applicable:** 6 — PRESENTATION, RNG, SERIALIZATION, STATE-TRANSITION, STRUCTURAL, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | 6 of 7 testable claims exercised, of the contract's 7 section-15 rows (0 record open questions); unexercised: who consumes each accessor - settled by census, which is not an execution |
  | INTEGRATION | the table is PLANTED. Nothing here reads navimapdata.bin and no consumer runs, so this shows the accessors agree - not that a reconstruction would grant the same permissions in a real field |

### `flag_banks` — entry `002EF2B0`

- **contract:** `14-Story-Event-Quest-Hunt/CONTRACT-persistent-flag-banks.md`
- **covered:** 4 of 11 — CALCULATION, EDGE-CASE, STATE-TRANSITION, STRUCTURAL
- **not applicable:** 3 — PRESENTATION, RNG, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | 6 of 10 testable claims exercised, of the contract's 12 section-15 rows (2 record open questions); unexercised: the two routes, re-counted here; the schedule is a parity; new game applies an authored list; the two shipped files and their sizes |
  | FULL-SUBSYSTEM | all 11 bank accessors covered as of 2026-09-08, but the contract enumerates 17 entry points; the gate, threshold schedule, new-game list, reset, event-memory predicate and payload-base helper are not reimplemented |
  | INTEGRATION | no script or event drives these accessors here |
  | SERIALIZATION | the payload IS the save image; no save/load round trip is compared |

### `frame_gate` — entry `0028E290`

- **contract:** `00-Engine-Core-Runtime/CONTRACT-per-frame-update-gate.md`
- **covered:** 4 of 11 — CALCULATION, EDGE-CASE, STATE-TRANSITION, STRUCTURAL
- **not applicable:** 3 — RNG, SERIALIZATION, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | derived from CONTRACT_MAP below, not declared |
  | FULL-SUBSYSTEM | the caller 002507C0 is not reconstructed and nothing writes the enable word - which §9 says nothing in the image does either |
  | INTEGRATION | all twenty-three callees are answered - what they DO is not reproduced, only whether and in what order they run |
  | PRESENTATION | several groups drive presentation work, and none of it happens here |

### `gambit_walk` — entry `00305CC0`

- **contract:** `09-Combat-AI-And-Gambits/CONTRACT-gambit-walk.md`
- **covered:** 3 of 11 — CALCULATION, EDGE-CASE, STATE-TRANSITION
- **not applicable:** 5 — PRESENTATION, RNG, SERIALIZATION, STRUCTURAL, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | 11 of 13 testable claims of the contract's 15 section-15 rows are exercised; the two new 2026-09-22 rows (the <=12 header-byte bound and the record+0x04 bit census) are provable only by writer census and cross-function reads, which a walk replay cannot drive |
  | FULL-SUBSYSTEM | one operation of the gambit subsystem; the evaluation, the enmity input and the 02089340 bit-5 suspension are outside it |
  | INTEGRATION | all three callees are scripted. Nothing here shows what a real evaluation decides or what a real commit does, so this shows the walk is right - not that a gambit would fire |

### `group_completion` — entry `00306F00`

- **contract:** `05-Spawn-Encounter-Lifecycle/CONTRACT-group-completion-and-respawn.md`
- **covered:** 4 of 11 — CALCULATION, EDGE-CASE, STATE-TRANSITION, STRUCTURAL
- **not applicable:** 3 — RNG, SERIALIZATION, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | derived from the map below: two of nineteen testable claims are exercised, because the contract is a subsystem and this is one function of it |
  | FULL-SUBSYSTEM | add, remove, reset and the deferred route are all outside this function and are not driven |
  | INTEGRATION | all four side effects are counted stubs: what they DO is not reproduced, only whether and in what order they fire |
  | PRESENTATION | the presentation event is dispatched to a stub and nothing is shown |

### `hp_write` — entry `00300530`

- **contract:** `08-Combat-Formula/CONTRACT-hp-write-and-lethal-transition.md`
- **covered:** 4 of 11 — CALCULATION, EDGE-CASE, STATE-TRANSITION, STRUCTURAL
- **not applicable:** 3 — RNG, SERIALIZATION, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | derived from the map below |
  | FULL-SUBSYSTEM | the transition is complete but its neighbours are not: the status change 0030E360 and the group completion 00306F00 are contracts of their own and are supplied here |
  | INTEGRATION | all twelve callees are scripted; no real status change, no real group completion, and no caller is reconstructed |
  | PRESENTATION | the reaction, the number and the events are observed as calls, not as anything drawn |

### `inventory_query` — entry `002FD8D0`

- **contract:** `12-Items-Equipment-Shops-License/CONTRACT-inventory-class-storage.md`
- **covered:** 3 of 11 — CALCULATION, EDGE-CASE, STRUCTURAL
- **not applicable:** 5 — PRESENTATION, RNG, SERIALIZATION, STATE-TRANSITION, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | derived from the map below: this pilot executes the three READ entry points and the contract's rows about the mutators, the dispatch pointer and the cap are not reachable from here |
  | FULL-SUBSYSTEM | four of the seven entry points are not executed - both mutators, the clear-all and the plus-or-minus-one entry |
  | INTEGRATION | the descriptor's arrays are planted by this fixture; nothing binds them here and no caller is reconstructed |

### `lua_header` — entry `0082E490`

- **contract:** `23-Third-Party-Libraries/Lua-Core/CONTRACT-lua-chunk-loader.md`
- **covered:** 4 of 11 — CONTRACT, EDGE-CASE, SERIALIZATION, STRUCTURAL
- **not applicable:** 5 — CALCULATION, PRESENTATION, RNG, STATE-TRANSITION, TIMING

  | not covered | what would cover it |
  |---|---|
  | FULL-SUBSYSTEM | one operation of the loader; the fork, the parser and the undumper are not reconstructed |
  | INTEGRATION | the ZIO read is answered and no real chunk is loaded; nothing here reaches luaU_undump or the interpreter |

### `manager_slot` — entry `003DA400`

- **contract:** `04-Actor-Entity/CONTRACT-manager-slot-entry-tables.md`
- **covered:** 4 of 11 — CALCULATION, EDGE-CASE, STATE-TRANSITION, STRUCTURAL
- **not applicable:** 4 — PRESENTATION, RNG, SERIALIZATION, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | derived from CONTRACT_MAP below, not declared |
  | FULL-SUBSYSTEM | seven of the eight entry points; side A's reset resolves its slot through 002640C0 and tail-jumps to 00257830, so it is a different function and is run on the ORIGINAL side only, not reconstructed |
  | INTEGRATION | the definition tables are PLANTED and the three callees are supplied, so nothing here shows what a real bind does to a real slot |

### `name_registry` — entry `00879570`

- **contract:** `15-Input/Input-Name-Registry/CONTRACT-input-name-registry.md`
- **covered:** 4 of 11 — CALCULATION, EDGE-CASE, STATE-TRANSITION, STRUCTURAL
- **not applicable:** 4 — PRESENTATION, RNG, SERIALIZATION, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | 8 of 12 testable claims exercised, of the contract's 12 section-15 rows (0 record open questions); unexercised: Exactly one function writes each head; The two inserts differ only in the two displacements naming their own head; Each registry is five paired functions of identical size; The other four are destructor, two finds and an enumerator |
  | FULL-SUBSYSTEM | 5 of 5 identified, 1 of 5 RECONSTRUCTED. The contract section 6 now ENUMERATES the other four (008794F0/00879600/00879670/00879760 and their key twins) and states the method, which is what this dimension asks for -- they are simply not reconstructed |
  | INTEGRATION | HALF of it now holds -- integration_name_registry.py uses the game's own nodes, at their own addresses, in the game's own recovered order, and compares against the GAME'S OWN list (0 of 143 and 0 of 97 differ). The CALLER is still not the game's: the CRT initialiser sequence is never executed |

### `party_slots` — entry `00269C70`

- **contract:** `11-Party/CONTRACT-party-slot-assignment.md`
- **covered:** 5 of 11 — CALCULATION, CONTRACT, EDGE-CASE, STATE-TRANSITION, STRUCTURAL
- **not applicable:** 4 — PRESENTATION, RNG, SERIALIZATION, TIMING

  | not covered | what would cover it |
  |---|---|
  | FULL-SUBSYSTEM | the roster is planted by this fixture, and the record-init assignment path inside 00266530 is not driven |
  | INTEGRATION | all five callees are answered; nothing here reaches the focus system or whatever consumes the notify |

### `phyre_header` — entry `0059A3B0`

- **contract:** `22-Middleware-PhyreEngine/Phyre-Asset-Container/CONTRACT-phyre-cluster-header.md`
- **covered:** 3 of 11 — EDGE-CASE, SERIALIZATION, STRUCTURAL
- **not applicable:** 5 — CALCULATION, PRESENTATION, RNG, STATE-TRANSITION, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | derived from CONTRACT_MAP below, not declared |
  | FULL-SUBSYSTEM | one function of the loader, not the cluster load |
  | INTEGRATION | the namespace reader and everything downstream of it are scripted |

### `phyre_namespace` — entry `0059C180`

- **contract:** `22-Middleware-PhyreEngine/Phyre-Asset-Container/CONTRACT-phyre-packed-namespace.md`
- **covered:** 4 of 11 — CALCULATION, EDGE-CASE, SERIALIZATION, STRUCTURAL
- **not applicable:** 4 — PRESENTATION, RNG, STATE-TRANSITION, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | derived from CONTRACT_MAP below, not declared |
  | FULL-SUBSYSTEM | the byte-order fixup, not the reader and not the consumers |
  | INTEGRATION | what a consumer does with the decoded schema is not here |

### `prep_step` — entry `0038AAF0`

- **contract:** `08-Combat-Formula/CONTRACT-preparation-step-family.md`
- **covered:** 6 of 11 — CALCULATION, EDGE-CASE, INTEGRATION, RNG, STATE-TRANSITION, STRUCTURAL
- **not applicable:** 3 — PRESENTATION, SERIALIZATION, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | derived from the map below |
  | FULL-SUBSYSTEM | the two dispatchers 003859FF and 003863D0, the recipe lists and the reset at 003849B0 are out of scope; this is the sixteen bodies |

### `quality_preset` — entry `00506A40`

- **contract:** `19-Save-Load-Settings/Game-Settings-Config/CONTRACT-game-setting-config.md`
- **covered:** 4 of 11 — CALCULATION, EDGE-CASE, STATE-TRANSITION, STRUCTURAL
- **not applicable:** 3 — RNG, SERIALIZATION, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | 3 of 7 testable claims exercised, of the contract's 9 section-15 rows (2 record open questions); unexercised: size `0x65C`, singleton `0x01F82D20`, 1 writer; key / value-name / matrix / mask tables; construction precedes `main`; `FrameLimit` drives the time base |
  | FULL-SUBSYSTEM | one entry point of the config subsystem |
  | INTEGRATION | nothing shows when the game calls this, nor that the settings object is in the state assumed |
  | PRESENTATION | no rendered result is compared |

### `ramp_channels` — entry `003B5890`

- **contract:** `17-Presentation-Rendering/CONTRACT-authored-command-ramp-channels.md`
- **covered:** 4 of 11 — CALCULATION, EDGE-CASE, STATE-TRANSITION, STRUCTURAL
- **not applicable:** 3 — RNG, SERIALIZATION, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | derived from the map below |
  | FULL-SUBSYSTEM | as above |
  | INTEGRATION | who calls the setters (the 00417xxx classes), what rec[0x10] is assigned by, and what the channels draw are all open (UG-1..UG-4) |
  | PRESENTATION | what the channels control on screen is not read |

### `render_pool` — entry `004279B0`

- **contract:** `17-Presentation-Rendering/CONTRACT-render-record-pool-lifecycle.md`
- **covered:** 4 of 11 — CALCULATION, EDGE-CASE, STATE-TRANSITION, STRUCTURAL
- **not applicable:** 3 — RNG, SERIALIZATION, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | derived from the map below |
  | FULL-SUBSYSTEM | the constructor 004269A0 is scoped out, and retirement's child loop cannot be driven at all - see the header |
  | INTEGRATION | eleven callees are scripted, and what they do to a record beyond the links this pool reads is not proved here |
  | PRESENTATION | these records are what the renderer draws; nothing here draws |

### `reward_award` — entry `002F8BB0`

- **contract:** `13-Rewards-Progression-Economy/CONTRACT-experience-and-licence-award.md`
- **covered:** 3 of 11 — CALCULATION, EDGE-CASE, STRUCTURAL
- **not applicable:** 5 — PRESENTATION, RNG, SERIALIZATION, STATE-TRANSITION, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | derived from the map below |
  | FULL-SUBSYSTEM | these two compute an amount; who awards it, and the loot and gil paths beside them, are not executed here |
  | INTEGRATION | six callees are scripted, and what any of them decides is open |

### `rng_generators` — entry `00328370`

- **contract:** `21-RNG-And-Determinism/CONTRACT-gameplay-generators.md`
- **covered:** 5 of 11 — CALCULATION, EDGE-CASE, RNG, STATE-TRANSITION, STRUCTURAL
- **not applicable:** 3 — PRESENTATION, SERIALIZATION, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | 8 of 9 testable claims exercised, of the contract's 9 section-15 rows (0 record open questions); unexercised: which callers reset the LCG seed through `00328D80` - settled by census, which is not an execution |
  | FULL-SUBSYSTEM | two of the six RNG families rng-streams.md records; the other four are outside this contract and outside this harness |
  | INTEGRATION | no consumer runs. BattleData_ResolveWeightedId and the weather roll at 0025ACA0 are what turn these numbers into outcomes, and neither is driven here |

### `save_image` — entry `002EF690`

- **contract:** `19-Save-Load-Settings/CONTRACT-save-image-buffers.md`
- **covered:** 6 of 11 — CALCULATION, CONTRACT, EDGE-CASE, SERIALIZATION, STATE-TRANSITION, STRUCTURAL
- **not applicable:** 3 — PRESENTATION, RNG, TIMING

  | not covered | what would cover it |
  |---|---|
  | FULL-SUBSYSTEM | the save path's producer - whatever fills the capture buffer - is outside this family and is not exercised |
  | INTEGRATION | the submit callee 0020E540 is answered, not run, so nothing here reaches a file or a device |

### `sound_request` — entry `00249C60`

- **contract:** `18-Audio/Audio-Boundary/CONTRACT-sound-request.md`
- **covered:** 3 of 11 — CALCULATION, EDGE-CASE, STRUCTURAL
- **not applicable:** 4 — PRESENTATION, RNG, SERIALIZATION, STATE-TRANSITION

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | derived from CONTRACT_MAP below, not declared |
  | FULL-SUBSYSTEM | the request family only - not the voice, the ramp or the banks |
  | INTEGRATION | the five controllers and the bank managers are the subsystem, and the dispatcher is scripted |
  | TIMING | nothing here establishes WHEN a caller asks for a sound |

### `status_write` — entry `003876D0`

- **contract:** `10-Status-Periodic-Terminal/CONTRACT-status-write.md`
- **covered:** 4 of 11 — CALCULATION, EDGE-CASE, STATE-TRANSITION, STRUCTURAL
- **not applicable:** 3 — RNG, SERIALIZATION, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | derived from CONTRACT_MAP below, not declared |
  | FULL-SUBSYSTEM | the arithmetic half only |
  | INTEGRATION | 0030E360 and its fourteen callees are not driven; the cascade and the terminal dispatch are not reached |
  | PRESENTATION | four of the operation's callees are presentation, and none runs |

### `storage_read` — entry `00862590`

- **contract:** `19-Save-Load-Settings/CONTRACT-storage-read-completion.md`
- **covered:** 4 of 11 — CALCULATION, EDGE-CASE, STATE-TRANSITION, STRUCTURAL
- **not applicable:** 4 — PRESENTATION, RNG, SERIALIZATION, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | derived from CONTRACT_MAP below, not declared - the queue, dispatcher and state-machine rows are all upstream of the two bodies this suite drives |
  | FULL-SUBSYSTEM | the seek (008625D0/00866A80), the sub-state chain and the queue compaction named in section 4 are not driven here |
  | INTEGRATION | the storage backend that fills base/end and whoever consumes the result global are outside these three bodies |

### `table_lookup` — entry `0020E600`

- **contract:** `02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md`
- **covered:** 3 of 11 — CALCULATION, EDGE-CASE, STRUCTURAL
- **not applicable:** 5 — PRESENTATION, RNG, SERIALIZATION, STATE-TRANSITION, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | derived from the map below |
  | FULL-SUBSYSTEM | one worked instance of a shape the database cites in at least four other contracts; the others are not executed |
  | INTEGRATION | the registry slot and the base are planted; nothing here shows what fills either at runtime, which is the shape's open question |

### `target_buffer` — entry `00316CD0`

- **contract:** `07-Combat-Action/CONTRACT-battle-target-buffer.md`
- **covered:** 5 of 11 — CALCULATION, EDGE-CASE, FULL-SUBSYSTEM, STATE-TRANSITION, STRUCTURAL
- **not applicable:** 4 — PRESENTATION, RNG, SERIALIZATION, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | derived from the map below |
  | INTEGRATION | no consumer runs. §9's warning is the point: this family is deterministic but its CONTENTS are only as deterministic as the query that filled it, and no query runs here |

### `transform` — entry `00398F90`

- **contract:** `00-Engine-Core-Runtime/CONTRACT-transform-primitives.md`
- **covered:** 3 of 11 — CALCULATION, EDGE-CASE, STRUCTURAL
- **not applicable:** 5 — PRESENTATION, RNG, SERIALIZATION, STATE-TRANSITION, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | derived from the map below: nine of eleven testable claims are exercised. The two that are not are a writer/reader count over the image and a live observation, neither reachable by an offline run |
  | FULL-SUBSYSTEM | the reconstruction takes the workbench as parameters and never writes the globals, so the parameter-to-address mapping - which is the caller's - is not exercised anywhere |
  | INTEGRATION | no caller is reconstructed, and 156 call sites were counted without one being read |

### `verb_dispatch` — entry `003DC270`

- **contract:** `01-Script-VM-Native-Bridge/Verb-Dispatch/CONTRACT-verb-dispatch-abi.md`
- **covered:** 3 of 11 — CALCULATION, EDGE-CASE, STRUCTURAL
- **not applicable:** 4 — PRESENTATION, RNG, SERIALIZATION, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | derived from CONTRACT_MAP below, not declared |
  | FULL-SUBSYSTEM | the dispatch half only - the lifecycle executor is not driven |
  | INTEGRATION | the meaning of this ABI is the 1,960 handlers on the other side of it, and none is called |
  | STATE-TRANSITION | the phase machine belongs to the executor 002621D0, which this pilot does not run |

### `verb_marshal` — entry `0017E7D0`

- **contract:** `01-Script-VM-Native-Bridge/Verb-Dispatch/CONTRACT-verb-dispatch-abi.md`
- **covered:** 5 of 11 — CALCULATION, EDGE-CASE, SERIALIZATION, STATE-TRANSITION, STRUCTURAL
- **not applicable:** 3 — PRESENTATION, RNG, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | derived from CONTRACT_MAP below, not declared |
  | FULL-SUBSYSTEM | the marshalling layer only - the 1,960 native verb bodies behind the adapters are not run |
  | INTEGRATION | the VM primitives are modelled and the native is intercepted at its entry so its argument registers can be sampled - neither side of the boundary executes its own body |

### `widget_construct` — entry `002465F0`

- **contract:** `16-UI/Widget-Object-Model/CONTRACT-widget-object.md`
- **covered:** 3 of 11 — EDGE-CASE, STATE-TRANSITION, STRUCTURAL
- **not applicable:** 4 — CALCULATION, RNG, SERIALIZATION, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | 2 of 6 testable claims exercised, of the contract's 6 section-15 rows (0 record open questions); unexercised: `+0x18` child / `+0x20` sibling; destroy is two-phase, 15 then 18; 280 sites / 251 handlers / 32 ids; the pool is 112 x `0x120` |
  | FULL-SUBSYSTEM | construction only; the message protocol, animation and teardown are not covered |
  | INTEGRATION | the construct message the caller sends is not compared, and no real caller drives this |
  | PRESENTATION | no widget is drawn |

### `workbench_save` — entry `0036D930`

- **contract:** `00-Engine-Core-Runtime/CONTRACT-transform-workbench-save-restore.md`
- **covered:** 4 of 11 — CALCULATION, EDGE-CASE, STATE-TRANSITION, STRUCTURAL
- **not applicable:** 4 — PRESENTATION, RNG, SERIALIZATION, TIMING

  | not covered | what would cover it |
  |---|---|
  | CONTRACT | derived from the map below: the call-graph claims about nesting and the image-wide sweep of the counter are not reachable by a run |
  | FULL-SUBSYSTEM | the workbench's other users - the 249 functions that write the region - are not exercised, and it is their clobbering that gives this pair its purpose |
  | INTEGRATION | no caller is reconstructed; the nine Save callers and the nine Restore callers are not driven |

## What this page does not claim

- **A declaration is a claim, not a measurement.** Nothing here checks that a harness marked `COVERED` actually meets the §3 criterion; the `measured` line only says the harness still runs and still reports zero mismatches.
- **An `EXERCISED` mark is still a human judgement.** It asserts that breaking the claim breaks the test; nothing here mutates the reconstruction to confirm that it would. The claim STRINGS are checked mechanically, the mapping is not.
- **Runtime captures have bounded scope.** Consult each experiment's process/input controls and limitations; the declarations here do not independently verify those captures or promote return-value agreement to integration, scheduling or ownership evidence.
