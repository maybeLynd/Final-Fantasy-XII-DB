---
system: The save's version stamps, and what loading normalises
category: 19-Save-Load-Settings
status: DOCUMENTED — every register row is closed (owner re-status 2026-09-30, OPUS): what the stamp digits mean (SD-41) is OUT OF EVIDENCE BOUNDARY, no labelled source exists in the image (§6); whether the header copies are compared (SD-42) answered 2026-09-30, no field read; the payload interior (UQ-271, SUPERSEDED as a duplicate of V-1) is mapped in the parent by V-1, ANSWERED 2026-09-27; V-3 (the header map) and V-6 (the fourth buffer) answered there 2026-09-11 and 2026-09-12
owner_layer: PrimaryOwner:Save_Load_Settings
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  parent_tag: GN159
last_reviewed: 2026-09-30
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-save-version-stamps-pass-1
  crossref_clean: false
  reopened_count: 0
---

# The save's version stamps, and what loading normalises

> **Answers `V-2`.** The two constants are **magics, not versions** — the only comparison in the image
> is an equality test. A save whose stamp differs is not migrated; the block it stamps is
> **reinitialised from scratch**.

~~**PARTIAL.**~~ **DOCUMENTED.** *(corrected 2026-10-02, OPUS: the front matter says `status: DOCUMENTED`)* *(DOCUMENTED since 2026-09-30, OPUS: SD-41 is closed OUT OF EVIDENCE BOUNDARY and SD-42 answered, §6.)* The two stamps, their single writer, the equality comparison and the load-normalise call
sequence are read at tier 1. ~~**The payload interior and the header map remain open**~~ *(Corrected 2026-09-30, SWE2-DATA: the header map is
`V-3` and the payload interior `V-1`, both answered; `UQ-271` is SUPERSEDED as V-1's duplicate)* (the checksum is answered, V-4) in
[the parent document](save-image-buffers-header-and-payload.md).

## 1. What the player sees

A save that loads or does not. There is no "this save is from an older version, converting…" path in
this engine — §2 is why.

## 2. `V-2`: both constants are magics

`0x20050223` and `0x05071901` are each returned by a six-byte getter, and both getters have **exactly
one caller**:

| Constant | Getter | Called by |
|---|---|---|
| `0x20050223` | `SaveImage_GetHeaderDword58Constant` (`002EF2A0`) | `SaveRuntime_InitializeHeaderAndImageBackedState` |
| `0x05071901` | `SaveImage_GetHeaderDword60Constant` (`00235E90`) | the same function |

So both are **written into the save header at initialisation** — header dwords `+0x58` and `+0x60` by
their names — by one function and nothing else.

**`0x05071901` has a second life.** It also stamps the head of a large runtime block, and that is
where the only comparison lives:

```asm
00233C4D  cmp dword ptr [rax], 0x5071901
00233C53  je  0x233C5E                     ; matched -> proceed
00233C55  jmp 0x237DF0                     ; otherwise -> the reinitialise path
```

> **The comparison is `je`. There is no `jb`, `ja` or subtraction against either constant anywhere in
> the image.** A value only ever tested for exact equality is a **magic**, whatever its digits spell —
> and these spell dates (`2005-02-23`, `05-07-19-01`) in packed decimal, which is a plausible reading
> of the digits and **not** what decides the mechanism.

**The modding consequence follows from the comparison, not from the name.** An edited save whose stamp
does not match is not upgraded and not partially accepted; **the block is zeroed and rebuilt** (§3).

## 3. What the stamp guards: a 29,712-byte runtime state block

`FUN_002370C0` is the initialiser on the mismatch path:

```c
memset([02EBF190], 0, 0x7410);        // 29,712 bytes
[02EBF190][0] = 0x05071901;           // the stamp goes at offset 0
FUN_003047F0();
// then region fills, beginning at offset 0x5A48 with 0xFFFF
```

And `FUN_00233C10` is the guard. ~~If the block pointer is null it is allocated at
`SaveImage_GetActiveRuntimeBuffer() + 0x4E68C` and initialised~~ *(corrected 2026-09-13, FABLE, on ASTRA's
[spawn page §22.4](../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md): nothing is allocated)* —
if `02EBF190` is null it is **bound** to `SaveImage_GetActiveRuntimeBuffer() + 0x4E68C` (`00233C25`–`00233C33`), the
inventory class descriptors are rebased (`0030B6A0`), and **`BattleSystem_ResetRuntimeState` `00237DF0` runs twice** —
a call and then a tail call (`00233C3F`, `00233C48`). If it exists, **its first dword is compared against the stamp**
(`00233C4D`): a mismatch tail-calls `00237DF0` once (`00233C59`); a match keeps the block and instead syncs its `+4`
bit 12 with `02089344` bit 0 (clearing that bit and `+0x5B00`/`+0x5B0C`/`+0x5B0E` when it was set), then rebuilds
the gambit order sets and resets several battle subsystems (`00233C65`–`00233CD6`). **`00237DF0` is the
reinitialise:** it calls `Inventory_InitializePrimaryStateFromAuthoredTable` `0023AF50` (`00237DF6`), which calls
`002370C0` — the 29,712-byte zero and stamp — at `0023AF56`. Callers of the guard: the area controller's
header-valid branch (`002803B8`), `00285E60` (the load's restore mark, `00285E86`), `0036FCC0`, `00394130`; `002370C0`'s
other direct caller is `00239960` (`002399E9`).

**That block is the one the party layer lives in.** Offsets `+0x5A48` and `+0x5A7E` inside it are the
party-configuration arrays documented in
[`active-party-reserve-and-the-moment-the-leader-changes.md`](../../11-Party/active-party-reserve-and-the-moment-the-leader-changes.md) §2 —
the same base pointer, `02EBF190`, and the same `0x5A48` the initialiser fills.

> **So the stamp is not decoration on a header; it gates whether the party roster, the reserve and
> everything else in 29,712 bytes survive a load or are wiped.** A one-dword mismatch discards all of
> it.

## 4. What loading normalises

`SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` (`00584210`, 456 B) is the load path's normalise
step, called once from `SaveLoad_ControllerLifecycleHandler` (`00582860`). **Read to its ret
2026-09-11 (FABLE-NORM1)** — the call list below was its skeleton; the body is two paths and a
reseed.

**The discriminator.** `00394450` returns the byte at `02AEE4D8` — a **load mode** a script sets:
verb `0x7067` (family 7, index `0x67`, no catalog name) pops one int and stores it through
`00510970` → `00394630` (`00510974`–`00510983`, `00394630`). The header byte `+0x57` bit 0 is the
**stash flag**. With `mode = 02AEE4D8` and `flag = header.b_57 & 1` (`0058422F`–`0058424F`):

| path | condition | what it does (buffer = `SaveImage_GetActiveRuntimeBuffer` (`002EF640`), payload = buffer `+0x200`) |
|---|---|---|
| **stash** | `mode == 3 && !flag` | header `+0x70` ← `+0x10` (qword), `+0x78` ← `+0x18` (word), `+0x7A` / `+0x7B` ← `+0x1A` / `+0x1B` (`00584255`–`00584270`); `+0x7C` ← `00320D50()` — the battle-state block's accumulator total (`+0x5AC8` + `+0x5ACC`); header `+0x80`–`+0x90` ← the world-transition record payload `+0x1044`–`+0x1054` (buffer `+0x1244`–`+0x1254`, `0058427B`–`005842B1`); then payload `+0x1048` = 0, block `+0x5B04` bit 0 cleared, header `+0x10` (qword) and `+0x18` (a **dword** — `+0x1A` / `+0x1B` go with it, `005842CF`) zeroed, `00322200()` zeroes the accumulator, header `+0x0C` = 0 (**not stashed** — the restore puts the accumulator total from `+0x7C` there, not this value), and `WorldTransition_SetActiveOrPendingFieldId` (`00314DC0`) `(0x483)` (`005842B7`–`005842DF`) |
| **restore** | `mode != 3 && flag` | the reverse: header `+0x10` / `+0x18` / `+0x1A` / `+0x1B` ← `+0x70`–`+0x7B`, `+0x0C` ← `+0x7C` and `00329E40(+0x7C)` re-seats the accumulator (`005842F9`–`00584320`); payload `+0x1044`–`+0x1054` ← header `+0x80`–`+0x90` (`00584325`–`00584362`); `WorldPersistence_ImportGroupPersistentBank` (`00269A20`) `(buffer + 0xE240)` — payload `+0xE040`, bank A (`00584368`); the flag cleared (`0058436D`); `SaveTransitionMetadata_RestoreFromRecord` (`002EF410`) `(buffer + 0x4E660)` — payload `+0x4E460` (`00584378`); `01E0C3EC = 0`; block `+0x5B04` bit 0 cleared; `0023A390(0)` clears block `+4` bit 12 — the persistence-pair selector (`0058437D`–`00584393`) |
| neither | otherwise | nothing moved |

Both paths then run `00316810` [PlatformOnlineAchievements] and **reseed**: `RNG_MT19937_Seed`
(`00379CF0`) with `(((u32)_time64 + 0x2B5A5) × 0x21 + (_time64 >> 32)) & 0x7FFFFFFF`, **and only
then** `+ 0x258 × [01FD4A80]` — the `btr ecx, 31` at `005843BE` precedes the timer add at
`005843C2`, so the clock term is confined below `0x80000000` and the final seed is not
(`0058439F`–`005843D3`; [the generator page](../../21-RNG-And-Determinism/which-roll-is-on-which-generator.md)
§5). ASTRA's [EXP-056](../../_experiments/EXP-056-save-normalize-roundtrip.md) executed the 456
bytes in isolation with every callee stubbed: twelve cases reproduce the copies, the widths and this
seed, and a mutant that masks after the sum is rejected by the high-timer case.

> **Loading is not restoring.** The field id is set, the flag bank is imported, and **the RNG is
> deliberately given a fresh clock-derived seed**, which is why reloading a save rerolls combat
> outcomes. And the stash is a **conditional** round trip: what mode 3 puts into header
> `+0x70`–`+0x90` — the header's `+0x10`–`+0x1B`, the accumulator and the transition record — comes
> back on the next non-3 load **only if the flag is set**, with field `0x483` standing in between
> (`FV-1`: mode 3 is the title's Trial Mode load route, §7); header `+0x0C` comes back as the stashed accumulator total,
> not as what it held.

**The flag that admits the restore is not set here.** `00584210` only *clears* header `+0x57` bit 0
(`0058436D`); nothing in the stash path sets it, so a mode-3 load followed by a non-3 load with the
same buffer restores nothing (EXP-056's carried-buffer control). The writer is the save-time
finaliser: `SaveImage_FinalizeHeaderAndChecksum` (`00583D60`) ors bit 0 into `+0x57` when
`00236760()` — the battle-state block's `+4` bit 12, the persistence-pair selector — is non-zero
(`00583F5A`–`00583F63`; bit 2 from `00236780`, block `+4` bit 14, at `00583F70`). Bit 12 is set by
the script: verb `0x308D` (family 3, index `0x8D`, no catalog name) pops one int (`0050F500` →
`00267E10`) and hands it to `0023A390`, which ors or clears `0x1000` in block `+4` (`0023A39B` /
`0023A3A3`); `00233C10` also writes the bit from `02089344` bit 0 ([the payload map](the-save-payload-field-map.md),
FG-4). The restore path's `0023A390(0)` (`00584393`) is what stops the next save from re-arming the
flag. This chain is read statically; no live save-then-load transition is claimed, and EXP-056's
flag intervention stands in for the finaliser, not for the game.

## 5. Key addresses

| Address | Name | Role |
|---|---|---|
| `002EF2A0` | `SaveImage_GetHeaderDword58Constant` | returns `0x20050223` |
| `00235E90` | `SaveImage_GetHeaderDword60Constant` | returns `0x05071901` |
| `00253A80` | `SaveRuntime_InitializeHeaderAndImageBackedState` | the **only** caller of both |
| `00233C10` | — | the guard: bind-or-verify the battle-state block; null or mismatch → `00237DF0` reinitialise |
| `002370C0` | — | zero 29,712 bytes and stamp offset 0 |
| `00584210` | `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` | the load normalise sequence (§4) |
| `00394450` / `00394630` | the load-mode byte `02AEE4D8`, read / written (the writer's only caller is the verb `0x7067` handler `00510970`) |
| `00320D50` / `00322200` / `00329E40` | the battle-state block's accumulator (`+0x5AC8` / `+0x5ACC`): total / zero / set |
| `0023A390` | block `+4` bit 12 set / clear — the persistence-pair selector |
| `0050F500` | verb `0x308D`'s handler: pops one int into `0023A390` — the script-side arm of the stash flag |
| `00236760` | reads block `+4` bit 12 — what the finaliser tests before setting the stash flag |
| `00583D60` | `SaveImage_FinalizeHeaderAndChecksum` — sets header `+0x57` bit 0 at `00583F63` when bit 12 is set |
| `00582860` | `SaveLoad_ControllerLifecycleHandler` — the normaliser's only caller |
| `02EBF190` | — | the runtime state block; party configuration at `+0x5A48` / `+0x5A7E` |

## 5b. Call chain (SWE2-DATA, 2026-09-30)

*Added 2026-09-30 (SWE2-DATA, DD owner read). Every edge below is a raw call site checked by
[`sv_callchain.py`](../../_index/candidates/dd-data-0930/sv_callchain.py) (16 checks, FAILS 0; control: the
finaliser's call of the persistent-flag gate at `00583F17`).*

**Load.**
```
SaveLoad_ControllerLifecycleHandler 00582860
  -> 00238A30(mode == 3)           00582CC8 / 00582CDE   the load-mode bit, 02089344 bit 0 (FV-2)
  -> 00285E60(-1)                   00582CD0 / 00582CE6   the load's restore mark
       -> 00233C10                  00285E86              the guard: bind the block, compare the stamp (§3)
            -> 00237DF0             00233C3F / 00233C48 / 00233C59   reinitialise (null or mismatch)
                 -> 0023AF50        00237DF6
                      -> 002370C0   0023AF56              zero 29,712 bytes, stamp offset 0
  -> 00584210                       00582EBA              the normaliser (§4); its only caller
```

**Save.**
```
SaveRuntime_InitializeHeaderAndImageBackedState 00253A80
  -> 002EF2A0                       00253AAC              header +0x58 constant; the only caller
  -> 00235E90                       00253ACA              header +0x60 constant; the only caller
SaveImage_FinalizeHeaderAndChecksum 00583D60
  -> 00236760                       00583F5A              block +4 bit 12 -> header +0x57 bit 0 (§4)
```

The guard's complete raw caller set is the four callers §3 lists.

## 5c. Modding notes (SWE2-DATA, 2026-09-30)

*Added 2026-09-30 (SWE2-DATA); each note restates a fact read above.*
- **The stamp that matters is the block's, not the header's.** A save whose battle-state block (buffer `+0x4E68C`)
  does not start with `0x05071901` loses the whole 29,712-byte block on load: the party configuration, the reserve and
  every field of [the block field map](../../11-Party/Battle-State-Block/the-battle-state-block-field-map.md) are reset
  (§3). No read of the header copies at `+0x58` / `+0x60` was found (`SD-42`).
- **Header `+0x57` bit 0 arms a restore.** A save carrying it has its stashed play clock, accumulator and transition
  record (`+0x70`–`+0x90`) put back on the next load that is not mode 3 (§4).
- **Reloading rerolls.** The normaliser reseeds the generator from the clock on every load (§4), so a reloaded save does
  not replay the same combat outcomes. **XIIOnline:** two clients loading the same save get different seeds.

## 6. What is not known

- **What the digits mean.** `2005-02-23` and `05-07-19-01` are a reading of the packed decimal, not a
  finding; nothing in the image labels either. Registered as `SD-41`. **Closed OUT OF EVIDENCE BOUNDARY
  (2026-09-30, SWE2-DATA, reviewed ACCEPT by SWE2-AUDIT-SPEC):** a negative search finds no labelled source. Both values
  are only stored, returned and equality-tested, never masked, split or formatted, and no string spells either as a
  date. So the date reading stays an interpretation the program neither confirms nor refutes; this page states it as
  that and claims no more.
- **Whether the two constants are ever compared at all** as header fields `+0x58`/`+0x60`. Only the
  runtime-block copy of `0x05071901` has a comparison; **the header dwords are written and no read of
  them was found**, which is an absence over the function list, not a proof. Registered as `SD-42`. *(Answered
  2026-09-30, OPUS, register-tracked census: no field read. The header copies are written by `00253A80` and moved only
  inside whole-block copies; the sole comparison is the runtime block's copy, §2.)*
- ~~**The four unread steps** of the normalise sequence (§4).~~ Read 2026-09-11 (§4).
- ~~**What load mode 3 is** — the value verb `0x7067` writes to `02AEE4D8`, and why the stash path
  parks the save on field `0x483`.~~ **FV-1 ANSWERED 2026-09-13 (FABLE), at the script level:** the only scripts that call verb `0x7067` are the title scripts `ttl_a01` (function `ロード画面起動`, "start the load screen") and `ttl_c01`, both right before `openfullscreenmenu_48d(0x8005, 1)`: title command status **1** selects mode **2**, and every other status that reaches the load screen — in `ttl_a01` that is command **5**, handled in the same `case 1: case 5:` arm — selects mode **3**. A mode-3 load stashes the save's location and sets field `0x483`, and `0x483` is compared with `nowmap()` by exactly the 100 `tri_*` scripts (the trial-director actor) and by no other of the 1,114. So mode 3 is the title's second load route, which drops a loaded save into the first field the Trial Mode scripts handle; mode 2 is the ordinary load. The stash-flag verb `0x308D` is called by no shipped `us` script (control: its neighbour `0x308C`, 854 calls), so the restore path's flag can only come from `00233C10`'s write (FG-4). Not established: the menu label of title command 5 (static text was not tied to it) and a live mode-3 load. Census:
  [`load-mode-script-uses`](../../_experiments/evidence/load-mode-script-uses/census.out.txt).
- ~~**What the header's `+0x0C`, `+0x10`–`+0x1B` and the stash `+0x70`–`+0x90` hold** beyond the
  round trip read here, and what `02089344` bit 0 means for the pair selector. **FV-2** (was
  mislabelled `V-11`).~~ **FV-2 ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5).**
  - **The header fields** were already mapped by [the save page](save-image-buffers-header-and-payload.md)
    §4, and this page now points there:
    - `+0x0C` is the walked-distance total. `00254E80` stores `00320D50()` there (`00254E90`), which is
      the battle-state block's `(int)+0x5AC8 + +0x5ACC`; this is why the restore puts the stashed
      total back into it.
    - `+0x10`–`+0x1B` is the play clock: the tick qword and its hours, minutes and seconds (`00254CC0`).
    - `+0x70`–`+0x90` is the mode-3 stash of those two, plus the world-transition record.
  - **`02089344` bit 0 means "this load came through load mode 3"** (the Trial Mode route, `FV-1`).
    - `SaveLoad_ControllerLifecycleHandler` sets it to `00394450() == 3`: `00238A30(1)` at `00582CC8`,
      else `00238A30(0)` at `00582CDE`. It then calls `00285E60(-1)`, which runs `00233C10`.
    - For a runtime block carrying the magic `0x5071901`, `00233C10` copies the bit into block `+4`
      bit 12 (`or 0x1000` at `00233C6E`, else `and ~0x1000` at `00233CA6`).
    - When the bit is set, `00233C10` also clears it (`00233C7C`) and zeroes the block's `+0x5B0C` word,
      `+0x5B0E` byte and `+0x5B00` dword.
    - Block `+4` bit 12 is what the save finaliser writes to header `+0x57` bit 0 (`00583F63`), the
      stash flag the restore path tests. **So a mode-3 load arms the restore for the next save.**
    - The image has one other writer: family-3 verb `0x308F`, whose result callback `0050F5A0` is
      `00238A30(1)`. The verb table puts it at `[01F281B0 + 0x20n + 0x20]`, and
      `scriptvm-verb-table.tsv` agrees. **No shipped script calls it.**
    - [`load_route_verb_census.py`](members/load_route_verb_census.py) walked all 10,036 script images
      in every language (27,623,415 call-family sites). It found 0 sites for `0x308F`, and 0 for
      `0x308D` / `0x308E` (block `+4` bit 12 set and read). Its control, `0x7067`, is found in
      `ttl_a01` and `ttl_c01`.
  - **The two sibling bits** belong to title scripts. They are set by `btlAtelResetNgPlus` `0x308A`
    (bit 1, `ttl_b01`) and `btlAtelResetNgMinus` `0x308B` (bit 2, `ttl_d01`), one site per language copy.
  - **Not established:** a live mode-3 load.
- ~~**What the rest of the 29,712-byte block holds** beyond the party configuration.~~ *(Corrected 2026-09-30, SWE2-DATA: mapped field by field on
  [the battle-state block field map](../../11-Party/Battle-State-Block/the-battle-state-block-field-map.md), AUDITED.)*
- ~~`V-3`, `V-6` and the payload interior — all still open in the parent document (the checksum, `V-4`, is answered there).~~ *Updated 2026-09-18 (FABLE): `V-3` (every header offset a reached writer touches) and `V-6` (the fourth buffer's writer, reached through a thunk) are answered in the parent and the register; only the payload interior (`UQ-271`) stays open there.* *(2026-09-30, OPUS: that too is closed. `UQ-271` is SUPERSEDED as a duplicate of `V-1`, which is ANSWERED 2026-09-27.)*

## 7. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Both constants come from six-byte getters with one caller each | the getters decoded; direct-and-thunk caller census | 1 |
| The only comparison is an equality test | image-wide immediate sweep: 3 sites for `0x05071901`, 1 for `0x20050223`; the sole `cmp` is at `00233C4D` followed by `je` | 1 |
| The stamped block is 29,712 bytes | `mov r8d, 0x7410` into the zeroing call at `002370D3` | 1 |
| The stamp is written at offset 0 | `mov dword ptr [rax], 0x5071901` at `002370DF` | 1 |
| The block is the party layer's | the same `02EBF190` base and the same `0x5A48` offset the initialiser fills | 1 |
| The normalise sequence | every direct call in `00584210` resolved in address order | 1 |
| The two paths and the stash | `0058422F`–`00584393` read to the ret; the mode byte's writer census (`00394630`, one caller `00510970`, verb `0x7067`) | 1 |
| The copy widths, the four mode / flag paths, the seed's mask-then-add order | EXP-056: twelve isolated-execution cases over the 456 bytes with every callee a no-effect stub; the after-the-sum mask mutant rejected | isolated original code |
| The stash flag's writer and the script arm | `00583F5A`–`00583F63` (finaliser), `00236760`, `0050F500` → `0023A390`, verb table row `308D`; `00584393` clears bit 12 on restore | 1 |

**Controls.** *"There is no ordered comparison"* is a measurement over an **immediate sweep of the
whole function list**, which found every occurrence of both constants — three and one — and each was
read. The sweep would have reported a `cmp`/`sub` against either value in any function; it reported
one, and that one is followed by `je`.

**The reading of the digits as dates is labelled as a reading and kept out of the mechanism.** The
behaviour — equality, therefore magic — does not depend on it, which is why §2 states the comparison
first and the digits second.

## 8. Related

- [`save-image-buffers-header-and-payload.md`](save-image-buffers-header-and-payload.md) — the header, the four buffers and the payload map; this document answers its `V-2`.
- [`persistent-flag-banks.md`](../../14-Story-Event-Quest-Hunt/persistent-flag-banks.md) — the banks the normalise step imports.
- [`active-party-reserve-and-the-moment-the-leader-changes.md`](../../11-Party/active-party-reserve-and-the-moment-the-leader-changes.md) — the party configuration inside the stamped block.
- [`which-roll-is-on-which-generator.md`](../../21-RNG-And-Determinism/which-roll-is-on-which-generator.md) — the reseed that ends the normalise sequence.

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run first, per
[`EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md)'s 2026-09-13 amendment.)*

Both getters are exactly what §2 says — **six bytes each**, and nothing but the constant:

```asm
002EF2A0  mov eax, 0x20050223 / ret
00235E90  mov eax, 0x5071901  / ret
```

and **each has exactly one caller, the same one** — `00253A80`
`SaveRuntime_InitializeHeaderAndImageBackedState`. The control passes: the same census gives
`memcpy` **362** callers, so "one caller" is a measurement and not a silent scan.

§2's central claim holds too. The one comparison in the image is:

```asm
00233C4D  cmp dword ptr [rax], 0x5071901
00233C53  je  0x233c5e                    ; equal -> carry on
00233C59  jmp 0x237df0                    ; differ -> the other path
```

**An equality test, and nothing ordered** — there is no `jl`, `jg` or subtraction anywhere near it.

### ⚠ The getter is not the only way the stamp reaches memory

Censusing both constants as instruction immediates across every function body finds **four sites**,
and one of them is a **second writer** of `0x05071901` that never touches the getter:

```asm
002370CD  mov  r8d, 0x7410
002370D3  call 0x861ec0                   ; memset - 0x7410 bytes
002370D8  mov  rax, qword ptr […]
002370DF  mov  dword ptr [rax], 0x5071901  ; the stamp, written inline
```

So §2's *"both are written into the save header at initialisation"* names one route; **`002370C0`
zeroes a `0x7410`-byte block and stamps it directly.** A reader tracing the constant through
`00235E90`'s single caller would not find this site, and it is the one that reinitialises.

### ⚠ The two stamps are not symmetric — only one is ever checked

| constant | immediates in the whole image | compared? |
|---|---|---|
| `0x05071901` | **3** — the getter, the inline writer, **and one `cmp`** | **yes**, once |
| `0x20050223` | **1** — its own getter, and nothing else | **never** |

`0x20050223` occurs **exactly once in the executable**, in the six bytes of
`SaveImage_GetHeaderDword58Constant`. The only way any code can hold that value is to call that
getter, and its **only caller is the initialiser** — so **no comparison anywhere in the image can
test a value against it.**

> §2 answers `V-2` with *"both constants are magics, not versions — the only comparison in the image
> is an equality test."* That is right about `+0x60` and **vacuously** right about `+0x58`: there is
> no comparison of it at all. **The `+0x58` stamp is written and never read back**, which for a
> modder is a sharper fact than "it is a magic" — editing it cannot make a save fail to load, and
> editing `+0x60` can.

### ➕ Added 2026-09-13 (OPUS): their two neighbours are sizes, and one of them dates the format

The header writes four constants, not two. `00253A80` calls four getters in a row
(`00253AAC`–`00253AE5`) and stores them at `+0x58`, `+0x5C`, `+0x60`, `+0x64`; §2 places the first
and third. The same immediate census places the other two:

| constant | header | immediates in `.text` | what the second one is |
|---|---|---|---|
| `0x00001538` | `+0x5C` | **2** — the getter `002EF290` and `002EF2DD` | `memset(activeBuffer + 0x200, 0, 0x1538)` — the size of the region cleared at buffer `+0x200` |
| `0x00007410` | `+0x64` | **2** — the getter `00235E80` and `002370CD` | `memset([02EBF190], 0, 0x7410)` — **the size of the battle-state block** §2's magic stamps |

Neither is compared anywhere, so the asymmetry above widens: of the four, only `+0x60` is ever read
back. But `+0x64` still carries information a `cmp` would not — **it records the block's size at the
time the image was written.** The sixteen development saves in
[the katano development saves](katano-debug-savedata.md) carry `0x5A70` = 23,152 there
against the shipped `0x7410` = 29,712, and the
[block field map](../../11-Party/Battle-State-Block/the-battle-state-block-field-map.md)'s
last touched fields (`+0x5B00`–`+0x5B0E`) lie past that older end. **So a save's `+0x64` dates its
format even though nothing checks it** — and because the magic at `+0x60` did not change when the
size did, `00233C4D` cannot tell the two layouts apart.

*(2026-09-30, SWE2-DATA: the paragraph below is dated 2026-09-13; since then §3 names the block, §4 is read to its ret
and `V-3` answers the header map.)*
**Not claimed:** which block `00233C10` and `002370C0` belong to ~~, and what `0x237DF0` does on the
mismatch path,~~ *(`00237DF0` read 2026-09-13 — §3: it reaches `002370C0` through `0023AF50`)* were **not** read — the reinitialise-from-scratch behaviour §2 states is taken as
given. §4's normalise sequence and the open header map are untouched. Nothing was executed or
observed live.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL.*

- **Items_Equipment_Shops_License — SERVICE.**
  - The guard `00233C10` rebases inventory class descriptors.
  - `BattleSystem_ResetRuntimeState` initialises inventory from the authored table
    (`Inventory_InitializePrimaryStateFromAuthoredTable`, which calls `002370C0`).
  - The preset apply `00239960` mutates item channels (`Inventory_MutateEncodedItemPrimaryChannelMod…`) and sets licence
    nodes and equipment slots directly. `BattleStats_InitializeDefinitionRecord` (`0023AC80`) sets licence nodes and
    equipment slots too.

  These functions rebuild inventory and equipment state. This page's first-bind distinction applies to the reset
  path.
- **Input — CLIENT and SERVICE.** `InputGameplay_ArbitrateDigitalInputAndModalS…` reads the flag getter `00236760`, and
  `SaveLoad_ControllerLifecycleHandler` (`00582860`) calls a 21-byte Input-filed helper.
- **CoreRuntimeScheduling — SERVICE and MECHANICAL.**
  - The MT seed thunk `00379CF0` is called by the 978-byte boot initialiser, which is the constant seed beside this
    page's clock reseed.
  - `00394130` and `00582860` call a 40-byte core helper.
  - `00233C10` and `00237DF0` read 7- and 11-byte getters.
  - The resolver reads are MECHANICAL.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Story_Event_Quest_Hunt — SERVICE.** `SaveImage_FinalizeHeaderAndChecksum` calls `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate`, so writing the header consults a persistent story flag gate. ~~Which flag it asks for is not read here.~~ *(Corrected 2026-09-30, SWE2-DATA: the parent's §8c reads the call — id `0x400B`, bit 14 selects the authored threshold schedule, index 11 (`V-5`); it is not a flag read.)*

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatFormula — CLIENT.** `FUN_0038ebe0`, owned by that layer, calls `00320D50` on this page. That caller is a 349-byte row-timing computation on the same two definition tables: it demands **bit 0 of the row's `byte[+0x12]`**, then divides a counter by 1,000 before indexing the `0x1C8`-byte records; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Gameplay — CLIENT.** `BattleSystem_ResetRuntimeState`, owned by that layer, calls `0023AF50` on this page. That caller is the runtime reset: it walks **40 records of `0x1C8` bytes** from `[02EBF190] + 8` and resets each through `0023AC80`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Rewards_Progression_Economy — CLIENT.** `BattleUnit_ProcessDefeatRewardsAndLoot`, owned by that layer, calls `00236780` on this page. That caller is defeat-and-loot processing, which reads the defeated unit's `+0x698` block, needs `byte[+5] == 1`, and is suppressed entirely by bit 3 of `byte[+0xE9A]`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (FABLE, Claude Opus 5.5, 2026-09-25)

These two paragraphs cover only the edges that the `FV-2` answer in §6 brings in, by citing
`00254E80`, `SaveLoad_ControllerLifecycleHandler` and `00233C10`. They name those edges and do not
say what the far-end bodies do.

**PlatformOnlineAchievements — PEER.** `00254E80`, the walked-distance mirror into header `+0x0C`, is
also called from that layer (`003162E0`, `00316760`). This page relies only on the mirror's own store
(`00254E90`). The normalise step's call into that layer (`00316810`) is the one §4 already names.

**UI — PEER.** Three UI edges come in:
- `00254E80` has a UI caller, `00281AE0`.
- `SaveLoad_ControllerLifecycleHandler` calls into the UI layer at `002814E0`.
- The runtime reset `00237DF0`, which `00233C10` calls, reaches `00313840`.

This page uses those bodies only for the bit-0 path, and it disposes of none of those UI calls.
