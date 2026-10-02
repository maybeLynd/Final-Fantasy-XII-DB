---
system: The auto-status rebuild
category: 08-Combat-Formula
status: AUDITED
owner_layer: PrimaryOwner:CombatFormula — the status layer it rebuilds is Status_Periodic_Terminal's
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN159 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN159 this document cites none of batch R109's 109; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-12
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: first-read-repos-55
  crossref_clean: true
  reopened_count: 0
---

# The auto-status rebuild

`BattleStats_RecomputeDerivedStateAndAutoStatuses` at **`0030FED0`**, 1,787 bytes. Three documents
leaned on it, and it is the function the result applier calls last **only when something actually
changed.**

## What the player sees

**Your permanent statuses are not stored — they are recomputed from scratch, every time anything
about you changes.** The engine builds the complete set you *should* have from four independent
sources, compares it with the set you *do* have, and applies the difference.

**Four sources feed the desired set:**

| source | what it contributes |
|---|---|
| **actor type** (party side) | two 32-bit masks from a table indexed by the type byte — **64 innate statuses** |
| **the foe table** (foe side) | **128 bits** copied whole from `actor[+0xE80]` |
| **equipment** | **five slots**, each able to grant **one** status |
| **the License board** | every owned node, each able to grant **up to eight** |

> **This is why equipment can grant a permanent status and why removing it takes it away with no
> un-equip logic anywhere.** Nothing is undone; the set is simply rebuilt without it. **The same
> reason equipment stats cannot drift applies to equipment statuses.**

**A License node grants up to eight statuses**, read as eight `u16` at `+0x08 … +0x16` with `0xFFFF`
as the empty slot — and the walk covers **361 board positions** (`< 0x169`).

## The diff, and one function for both directions

The current set is XOR-ed against the desired set into two scratch buffers — **one for what must be
added, one for what must be removed** — and then a single 128-iteration walk issues both:

```c
if (to_remove[i >> 3] & bit) { mode = 3; FUN_0030E130(stats, i, 0, flags); }
if (to_add   [i >> 3] & bit) { mode = 1; FUN_0030E130(stats, i, 0, flags); }
```

> ### CORRECTED 2026-09-10 — the two labels above are swapped
>
> The buffer tested first (`[rsp+0x50]`, `00310357`–`0031035C`) is **`(desired ^ current) & desired`**
> — the bits to **add** — and it goes to mode **3**; the buffer tested second (`[rsp+0x60]`,
> `0031037D`) is `(desired ^ current) & current` — the bits to **remove** — and goes to mode **1**
> (`00310310`–`0031032E` build them: `al = xor & desired` → `+0x50`, `dl = xor & current` → `+0x60`).
> [The two-layer page](../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md)
> reads `0030E130`'s modes from its bytes: **1 clears `+0x78`, 3 sets `+0x78`** (`0030E229`/`0030E202`),
> so the two agree once the labels are put right. Everything else in the snippet stands.

**The same callee, twice, distinguished by a mode written to the stack rather than by the argument
list.** A reader matching on call arguments sees two identical calls.

**And the caller's flags are not the caller's alone:** `param_2 |= 0x202` on entry — **two bits are
forced on for every call this function ever makes**, whichever caller asked.

## The affinity handshake

The elemental affinity bytes `+0x40 … +0x44` exist in **two places** — on the stats record and in the
actor's `+0x6A0` block — and this function reconciles them **in a direction chosen by one bit**:

```asm
                              ; bit 0x80 of [actor+0x6A0][0] SET -> actor wins
00310443  mov   byte ptr [rbx + 0x40], cl        ; block +0x78 -> stats +0x40
00310451  mov   byte ptr [rbx + 0x41], dl
0031045F  mov   byte ptr [rbx + 0x42], cl
0031046D  mov   byte ptr [rbx + 0x43], cl
0031047B  mov   byte ptr [rbx + 0x44], cl
                              ; bit CLEAR -> stats win
00310484  mov   byte ptr [rcx + 0x78], al        ; stats +0x40 -> block +0x78
00310492  mov   byte ptr [rcx + 0x79], al
```

> **That bit is the one the result applier sets** whenever it changes any of those four status bytes.
> **The applier writes the actor block and raises a flag; the rebuild sees the flag and copies the
> other way.** Two functions read independently on two different ticks, meeting on one bit — and
> **without it the rebuild would overwrite every affinity change an action had just made.**

## The derived clamps

- **Status bit 16 switches which field is the cap**, and **status bit 28 doubles it** — the same bit
  that a separate document found selecting a unit-stat amount and doubling it in the periodic tick.
  **Third sighting, same role: bit 28 means double.**
- Two further caps (`+0x4C` and `+0x06`) ~~are applied **only when both status layers have bit 7 clear**~~
  ~~(`+0x6C` and `+0x7C` non-negative) — **a single status that suspends two independent clamps.**~~ take their normal cap only when both status layers have bit 7 clear (`+0x6C` and `+0x7C` non-negative); with bit 7 (id 39) set on either, the cap is **0**, so MP and the secondary pool are clamped to 0, not left unclamped *(corrected 2026-10-02, OPUS: checked at `0031050B`–`00310566`, `js` / `jl` selecting `r14d`, zeroed at `0030FF07`; the formula below, `cap = (+0x6C ≥ 0 && +0x7C ≥ 0) ? +0x28 : 0`)*.
- The `+0x06` cap is `+0x28 × +0x37` when the byte multiplier is non-zero, and `+0x28` alone when it
  is — **zero means one, not zero.**

## Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Is the desired set really rebuilt, or merged into the existing one? | **Rebuilt** — the 16-byte buffer is explicitly zeroed at entry, sixteen separate stores, before any source is read. |
| Are add and remove really the same callee? | **Yes**, `0030E130` both times, three instructions apart, with the mode written to a stack slot between them. |
| Is `0x169` a count of board nodes or a byte length? | It bounds a **bit** index (`i >> 3` into the mask at `+0x194`), so it is **361 positions** — consistent with the 368-bit board mask read by the licence check. |
| Does the affinity copy go both ways in one call? | **No — the two directions are the two arms of one branch**, and the bit is tested once. |
| Could `param_2 |= 0x202` be a caller's value that happens to include those bits? | **No** — it is an unconditional `or` on the parameter at entry, before any use. |

~~**What this document does not claim:** what any status id means, what `002FEF30`, `0030E060` or
`0030E360` do, what the actor-type table's two masks contain, which fields `+0x24`/`+0x48`/`+0x4C`/
`+0x06` hold, or why the foe path applies a further 32-bit mask from `actor[+0xE90]` after the diff has
already run.~~

**Narrowed 2026-09-10 (the section below):** the party-side masks are the party definition row's words
`+0x50` / `+0x54`; `0030E060` is read (the `+0x4E` charge count); `+0x24` / `+0x48` are max and current HP
([the HP write](Current-HP/the-hp-write-and-the-lethal-transition.md)), `+0x4C` / `+0x28` live MP and capacity
([where MP comes from](../10-Status-Periodic-Terminal/where-mp-comes-from.md)); the foe path's `+0xE90` mask
is applied through the status write in mode 5 — **as immunities**: mode 5 sets the bit in `+0x38`, which makes an
ordinary add refuse it (corrected 2026-09-15, § below); `0030E360` is [the status write](../10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md).
Still not claimed: what any status id means~~, and the body of `002FEF30`~~ *(answered for the body: where-a-stat-number-comes-from.md and CONTRACT-stat-derivation.md read `002FEF30` whole; 2026-10-02, OPUS)*
([the single stat rebuild](../12-Items-Equipment-Shops-License/equipment-slots-and-the-single-stat-rebuild.md) §7).
## Execution order, cited — 2026-09-10 (FABLE)

`0030FED0(record /*rcx*/, flags /*edx*/)`; **25 call sites in 14 functions** (`check_caller_claims`,
control 632). Every step, in order, with the bytes:

| step | site | what |
|---|---|---|
| entry | `0030FEF8`–`0030FF12` | `flags \|= 0x202`; the 16-byte desired set at `[rsp+0x40]` zeroed; null record → straight to the clamps (`0030FF16`) |
| **kind 0: the party row's two masks** | `0030FF1F`–`0030FFD2`, `0030FFD4`–`00310018` | `row = 02EBF130 + stride × record.b_04` — **the party definition row, by the record's own index** (the "actor-type table" above); desired bits 0–31 ← `row.u32_50`, bits 32–63 ← `row.u32_54`, one `bts` per set bit |
| **kind 1: the unit's innate mask** | `0031001A`–`0031006F` | `unit = BattleStats_FindOwningBattleUnit(record)` (`0031B860`); desired bits 0–127 ← `unit + 0xE80` (16 bytes), bit by bit |
| **equipment** | `00310071`–`00310121` | five words at `record + 0x50 … + 0x58`: `BattleEncodedId_IsValidForClass(6, word, 0)` (`00322C50`) → `row = 02EBF0F8 + (word − 0x1000) × stride` (the equipment table; [the id encoding](../12-Items-Equipment-Shops-License/item-id-encoding-and-equipment-compatibility.md)); `0031E9A0(row) == 3` — the runtime category from `BattleDefinition_MapByte9ToRuntimeCategory` (`0031E9F0`, byte `+9` values **19–22** → categories 7–9 → class 3, table at `0031EA74`) — and `row.b_1A ≠ 0xFF` → desired bit `row.b_1A` |
| **licences** | `00310127`–`003102DF` | for node `i < 0x169`: bit `i` of the record's bitmap `+0x194`; `entry = 02EBF038 + i × stride`; `00323890(entry.b_05) == 2` — `003241D0` maps byte `+5` **values 15–18** to groups `0x1B` / `0x1C` (table `00324260`), which the jump table at `003238E4` classes as 2 — then each of the eight words `entry + 8 … + 0x16` that is not `0xFFFF` is a desired bit |
| **the diff** | `003102E5`–`00310336` | `x = desired ^ current(+0x78)`; **add** = `x & desired` → `[rsp+0x50]`; **remove** = `x & current` → `[rsp+0x60]` (see the CORRECTED note above) |
| **apply** | `00310338`–`003103A3` | for `i < 128`: add → `BattleStats_ModifyStatusLayerStateAndProcessSideEffects(record, i, 0, flags, mode 3)` (`0030E130`); remove → the same with mode 1 |
| **the stat rebuild** | `003103A5`–`003103AD` | `BattleStats_RebuildEffectiveStatsAndAffinityState(record, 0, 0)` (`002FEF30`, 2,859 B) — the body [the single stat rebuild](../12-Items-Equipment-Shops-License/equipment-slots-and-the-single-stat-rebuild.md) §6 reads only in part |
| **kind 1: the second foe mask** | `003103B2`–`00310413` | `unit + 0xE90` (u32): for each set bit `s < 32`, **`0030E360(record, 0, s, 0, 0, flags, mode 5)`** — the status write's mode 5. ~~`extraEffect` on add: a foe's authored statuses are *added as statuses*, not just as layer bits~~ **Corrected 2026-09-15 (FABLE):** mode 5 is not an add. The mask-write jump table `0030E88C` sends it to `0030E557`, which **sets the bit in `+0x38`, the immunity word**, and mode 3 refuses any bit set there (`0030E531`; [the definition-record flag pair](../04-Actor-Entity/the-definition-record-flag-pair.md)). The stat rebuild just before it zeroed `+0x38`, so this loop re-installs **a foe's scripted status immunities** on every recompute |
| **kind 1: the affinity handshake** | `00310415`–`003104BC` | `block = unit + 0x6A0` — for a spawn-backed unit this is **the spawn record** ([the unit-definition page](../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md) §2.4); `block.b_00 & 0x80` → `record + 0x40 … + 0x44 ← block + 0x78 … + 0x7C`, else the other way (the section above) |
| **the HP clamp** | `003104BF`–`00310508` | `cap = bit 16 of (+0x64 \| +0x3C) ? max(+0x48, 1) : +0x24 (× 2 on bit 28)`; **only downward**: `if +0x48 > cap: +0x48 = cap` — no HP write, no lethal transition, a bare store |
| **the MP clamp** | `0031050B`–`0031053D` | `cap = (+0x6C ≥ 0 && +0x7C ≥ 0) ? +0x28 : 0`; `if +0x4C > cap: +0x4C = cap` (bare store) |
| **the `+0x06` clamp** | `00310541`–`00310594` | `cap = layers clear ? +0x28 × (+0x37 or 1) : 0`; `if +0x06 > cap: +0x06 = cap` |
| **the charge count** | `00310591`–`0031059C` | `0030E060(record, flags)` (200 B; callers `0030FED0`, `00300BC0`): if `+0x28 > 0`: `n = (+0x37 > 0) ? +0x06 / +0x28 : 0`; **the branch for `flags` bit 1 clear calls `0016D6A0`, which is `ret 0` — a retired hook, and this caller forces bit 1 anyway**; if `(flags & 0x410) == 0x400` and `n` changed: `003283D0(unit, n − old, n > old, 1)` — a presentation request through `003BBD00` with the actor at `unit + 0x10`, `\|Δ\|`, and a byte from the table at `01EED300` (`003283E2`–`00328462`); then **`+0x4E = n`** |
| return | `003105A1`–`003105CA` | `eax = 0`; nothing else is written |

**What the flags do here.** Only three bits are tested inside this function and its `+0x4E` step:
bit 1 (forced on at entry, so the retired hook never runs), `0x10` and `0x400` (the charge
notification fires only for `0x400` without `0x10`). Everything else rides through to the layer
write and the status write. The 25 call sites pass: `0x297` (`SpawnUnit_FinalizeSpawnEntryActivation`,
`0023A502`); `0x200` once and `0` eleven times (`BattleUnit_ExecuteDirectStateCommandOrder`,
`002FDEF7`, `002FE163`–`002FE4D5`); `0` (the level grower `0030C602`, the level-up `0030C7CE`, the
applier `00311AC5`); `0x217` (`0030F735`); **`0x97`** (the three equipment setters `0031A4CA`,
`0031A5ED`, `0031A6D4`, the licence setter `00323B87`, and `00328C66`); and the caller's own flags
from the two status writes and `0030E8F0` (`0030E329`, `0030E828`, `0030E94D`). So the equipment
page's "what `0x97` means": bits `0x80 \| 0x10 \| 4 \| 2 \| 1` — `0x10` suppresses the charge
notification here, and the rest are the layer and status writes' concern.

## The foe's two masks are written by script verbs — 2026-09-10 (FABLE)

A from-entry displacement sweep for `+0xE80` / `+0xE90` (control: this function's own reads at
`00310047` / `003103E0`) finds three battle-unit writers — the reset `BattleUnit_ResetStateForReuse`
(`00236A60`, zeroes both at `00236B19`–`00236B2E`) and two `ActorEntity` functions that are the
tails of two script verbs of family 3:

| verb | handler | native | what it writes |
|---|---|---|---|
| **`0x3000` `btlAtelSetAbility(a, b)`** | `00510440` (67 B) | `002390B0` (190 B) | **`unit + 0xE80`**, the 128-bit innate source this function copies whole. Two `VMValueStack_PopInt32CoerceFloat32` (`00267E10`) pops — the first lands in `edx`, the second in `r8d` (`00510458`–`0051046A`), so **the last value the script pushed is the first native argument** ([the calling convention](../01-Script-VM-Native-Bridge/Spawn-Verbs/the-script-to-native-calling-convention.md)). `002390B0` resolves the unit with `ActorWork_GetBattleUnit` (`0031B760`), zeroes the 16 bytes (`002390D8`–`002390DF`), then for `k = 63 … 32` with a bit rolling from 0: **`r8d` bit *j* sets status bit `31 − j`, `edx` bit *j* sets status bit `63 − j`** (`002390F0`–`00239161`) — **both words are bit-reversed on the way in**, so the authored word's bit 0 is the highest id of its half. Only ids 0–63 can be innate; bits 64–127 of `+0xE80` are never set here. |
| **`0x3002` `btlAtelSetStatus(t)`** | `005103B0` (63 B) | `002394C0` (222 B) | one int pop → `002650B0(002640C0(), ctx, value)` resolves it to **a script-data pointer** (`005103C7`–`005103D5`; the same resolver [the naming page](../01-Script-VM-Native-Bridge/how-a-script-names-a-thing-in-the-world.md) leaves open); `002394C0` reads **32 two-bit codes** from the 8 bytes it points at (`code = (table[s >> 2] >> (2 × (s & 3))) & 3`, `00239504`–`00239527`): **3 → bit `s` of `unit + 0xE90`** (`00239538`), ~~re-added as a status~~ **made an immunity** (`+0x38`) by this function's mode-5 pass on every recompute (corrected 2026-09-15); and, **only while the spawn record is fresh** (`(*(u32*)(unit + 0x6A0)) & 5 == 0`, `002394DF`–`002394F9`): **2 → `BattleStats_AddStatusMode3(stats, 0, s, −1, −1, 0x297)`** (`0030EAE0`, `00239556`–`00239577`) once; **1 → the same, on a coin flip** (`RNG_SharedGameplayLCG_NextU32`, `00328370`, bit 0; `00239547`–`0023954F`); 0 → nothing. `+0xE90` is zeroed first (`002394FC`). |

So **a foe's innate augments and its authored statuses are not in the enemy definition row at all —
they are set by its AI script**, in the `btlAtel` family that also carries the group flag verb
`0x3030`. A reimplementation that reads the `.ard` row for them finds nothing; the words live in the
`.ebp`. `FC-1` is answered by this section; what remains of it is the spawn record's `+0x78`–`+0x7C`
and byte-0 bit 7 (moved to `FC-2`).

> **Corrected 2026-09-15 (FABLE): code 3 is an immunity, not a permanent status.** The mode-5 pass that reads
> `+0xE90` writes the immunity word `+0x38` (the kind-1 row above). The shipped tables agree:
> `work/FABLE/drift4/uq84_script_status_codes.py` resolved all 6,746 `btlAtelSetStatus` calls in the decompiled `us`
> corpus. Each argument is a scope-3 reference into the script's `.src.data`; none failed to resolve. The code shapes:
> - **Code 3 is never given to KO or Stone (0, 1).** It is given to X-Zone (31), Libra (30) and Bubble (28) in every
>   one of the 6,205 non-empty tables, and to Lure (17) in 6,178. Those are statuses a foe is made proof against, not
>   ones it carries.
> - **Codes 1 and 2**, the one-time adds at spawn through mode 3, occur only on Sleep, Confuse (4, 5), Protect …
>   Regen (18–25) and Berserk (27). Those are the foe's starting statuses.
> A foe's scripted **starting** statuses are therefore codes 1 / 2, and its scripted **immunities** are code 3.

## What is not known

- [x] ~~**What writes the foe's two masks** `unit + 0xE80` (128 bits, the innate layer source) and~~
  ~~`unit + 0xE90` (32 bits, added as statuses in mode 5) — the spawn path is the candidate, and the~~
  ~~spawn record's `+0x78`–`+0x7C` affinity bytes and `+0` bit 7 are the other side of the handshake.~~
  **FC-1** — ANSWERED 2026-09-10: the script verbs `btlAtelSetAbility` (`0x3000` → `002390B0`) and
  `btlAtelSetStatus` (`0x3002` → `002394C0`); the section above. The spawn record's affinity bytes
  and dirty bit are `FC-2`.
- [x] ~~**What the five affinity bytes** `record + 0x40 … + 0x44` **mean and who reads them** beyond the
  applier's write and this copy — and who else touches their persistent home, spawn record
  `+0x78`–`+0x7C`, and its byte-0 bit 7. **FC-2.**~~ **ANSWERED 2026-09-10 by reference:** weak ×2 / absorb / resist ×0.5 /
  immune / the source's ×1.5 ([elemental affinity](elemental-affinity-and-the-five-bytes.md)), persisted at spawn record
  `+0x78`–`+0x7C` with the dirty bit in flags bit 7. *(Ticked 2026-09-14, FABLE: the register's `FC-2` verdict answers this box; the page box had been left open.)*
- [x] **FC-3.** **What `003283D0`'s request is on screen** — the `003BBD00` message with the `01EED300` byte
  (index `2 × sign \| 1`, `+ 4` for a non-party or non-mode-3 unit, `00328430`–`0032845E`), and what
  `002FA3B0` gates it on. **FC-3.** *Narrowed 2026-09-12 (FABLE):* the gate is "within 24 units of the
  party leader" and the byte is one of eight reaction kinds — here lane 1 (MP / charges), gain or loss,
  party or foe ([the HP write](Current-HP/the-hp-write-and-the-lethal-transition.md) §2.4, `EY-5`). The
  request is a `0x50`-byte entry `{actor, amount, type 0, kind}` placed in the 64-slot presentation
  ring `02B457D0` (cursor `02B443C0`) with a screen lane chosen from the other live entries for that
  actor and a randomised offset from the `00D11600` pair table (`003BBDB0`–`003BBF58`). ~~What draws the
  ring is the residue.~~
  **ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5): a floating decimal number over the unit, the charge gain or loss.**
  - **The entry holds the number as text.** The entry builder `00506700` copies the request's type byte `+0xC` to
    entry `+0x3C` (`0050673F`–`00506743`). For type 0 (`0050674A` → `00506834`) it formats the request's amount
    `+8` as decimal ASCII into entry `+0x40` through `003EFD00`, which divides by ten through `0x66666667`, and
    stores the length at `+0x3F` (`00506850`–`0050685A`).
  - **Each frame the ring is aged, then drawn.**
    - The tick `003BBA60`, from the frame tail, runs `00505500` on every live slot. A type-0 or type-1 entry
      advances its counter `+0x38` by `+0x3A` and is freed once that counter passes `0x25`. The tick also ramps
      the layer alpha `01EFE320` by ±0.2 towards the `01EFE31D` bit-1 state.
    - The sweep `003BBB60` hands each non-status entry to `00505560`, which jumps through the type table
      `00D22790`: type 0 → `00505E00`, type 1 → `00505570`, type 2 → the no-op, because type 2 is the status
      label the billboard pass draws.
  - **`00505E00` draws the digits.** It resolves the actor handle, takes the actor's world position and
    projects it through `02AED5F0`. Then, for each character of the `+0x40` string, `char − '0'` indexes a
    glyph rectangle `{u, v, w, h}` in a sprite table (`00506180`–`005061C6`). The digits are coloured by the
    entry's bytes `+0xC`–`+0xE`, and the kind byte `+0x3D` selects the style.
  - **So this is the floating number.** Here it is the lane-1 (MP / charges) gain or loss that `EY-5` names.
    It shows as a number rising off the unit for about `0x25 / +0x3A` frames. Only units within the leader
    range the gate allows get one.
  - **Static only;** no frame was observed.
- [x] **FC-4.** **What the four licence groups** `003241D0` produces (`0x15`–`0x1E` from byte `+5` values 1–20 and 30;
  21–29 map to 0) **and the nine equipment categories** of `0031E9F0` **are called** —
  the class 3 / group 2 that grant statuses are located, the rest are not named. **FC-4.**
  **ANSWERED 2026-09-15 (FABLE).** The two jump tables were decoded from the image, then cross-tabulated against the
  authored rows that feed them in the `us` battle pack, with names read through the text banks. Nothing was executed.
  **`003241D0` produces ten groups, not four**, and the licence-board node names say what each is:
  - **Correction to the question:** the ten groups are `0x15`–`0x1E`. No node carries byte `+5` in 21–29, so the zero arm
    is unreached in the shipped board.

  | group | byte `+5` | nodes | what the nodes are |
  |---|---|---:|---|
  | `0x15` | 1 / 2 / 3 | 104 | weapons (1: Swords, Greatswords, Katana, Spears, Bows, Axes & Hammers; 2: Rods, Staves, Maces, Measures; 3: Daggers, Ninja Swords, Poles, Guns, Crossbows, Hand-bombs; plus single-weapon nodes) |
  | `0x16` | 4 / 5 / 6 | 39 | armour: Heavy (with Genji), Mystic, Light |
  | `0x17` | 7 | 10 | shields |
  | `0x18` | 8 | 23 | accessories (with Ribbon) |
  | `0x19` | 9–13 | 42 | magicks: White, Black, Time, then two mixed tiers (White / Green / Black and Arcane / Black / Time) |
  | `0x1A` | 14 | 24 | technicks (Steal, Libra, First Aid … Gil Toss) |
  | `0x1B` | 15 / 16 / 17 | 76 | augments: single named ones (Warmage … Brawler); the three-node lores and passives (Shield Block, Channeling, Swiftness, Potion / Ether / Phoenix / Remedy Lore); Battle Lore, Magick Lore and the HP nodes |
  | `0x1C` | 18 | 11 | Gambit Slot ×10 and Essentials |
  | `0x1D` | 19 / 20 | 31 | Quickening ×18; the thirteen espers |
  | `0x1E` | 30 | 1 | Second Board |

  **`0031E9F0`'s input byte `+9` is the authored equipment category id.** The 27 values carry the names
  [the category table](../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md) (class 28) gives them,
  and the named rows agree: 18 is shields, 19 helms and 23 arrows, while unnamed rows are "NOT USED" or reserve. The
  function folds those ids
  into nine runtime categories:

  | runtime | category ids → names | rows |
  |---:|---|---:|
  | 1 | 0 Unarmed | 68 (mostly reserve) |
  | 2 | 1 Sword (1H), 10 Axe, 11 Hammer, 12 Dagger, 15 Mace, 16 Measure | 96 |
  | 3 | 2 Sword (2H), 3 Katana, 4 Ninja Sword, 5 Spear, 6 Pole, 13 Rod, 14 Staff | 95 |
  | 4 | 7 Bow, 8 Crossbow, 9 Gun, 17 Hand-bomb | 49 |
  | 5 | 23 Arrows, 24 Bolts, 25 Shot, 26 Incendiaries | 35 |
  | 6 | 18 Shield | 33 |
  | 7 | 19 Helm | 60 |
  | 8 | 20 Chest | 73 |
  | 9 | 21 Accessory, 22 (unused) | 48 |

  - **Not claimed:** why weapons split between runtime 2 and 3. The member lists are read; the rule a consumer applies
    to that split is not.

## Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| The four desired-set sources and their tables | `0030FF1F`–`003102DF` | 1 | PROVEN |
| The diff buffers and which mode each takes | `00310310`–`0031032E`, `00310357`–`00310396`; `0030E202`, `0030E229` | 1 | PROVEN |
| The foe path's `+0xE90` bits installed in mode 5, which is the immunity word `+0x38` (corrected 2026-09-15) | `003103E0`–`00310409`; jump table `0030E88C` entry 5 → `0030E557`; the refusal at `0030E531` | 1 | PROVEN |
| The three clamps are bare downward stores | `003104BF`–`00310594` | 1 | PROVEN |
| `0016D6A0` is `ret 0`; the notification's flag test | `0016D6A0`; `0030E0C6`–`0030E102` | 1 | PROVEN |
| The two classifier tables | `00324260` (30 bytes) → `00324234`; `0031EA74` (27 bytes) → `0031EA50`; decoded from the image | 1 | PROVEN |
| The two mask writers and the reset, and nothing else on battle units | displacement sweep `+0xE80`/`+0xE90`, control `003103E0`; `002390B0`, `002394C0`, `00236A60` read; verb rows `0x3000`/`0x3002` in `scriptvm-verb-table.tsv` | 1 | PROVEN |
| 25 call sites in 14 functions, and their flag constants | `check_caller_claims --addr`, control 632; a from-entry scan of each caller's last `edx` write | 1 | PROVEN |

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL and recorded in the registry.*

**Movement — CLIENT and SERVICE.**

- `BattleUnit_ResetStateForReuse` (`00236A60`) resets the unit's path through `Navigation_ResetPathPredecessors` and a
  33-byte helper.
- `ActorWork_GetBattleUnit` is read by the random-yaw helper (182 B).
- That same helper and the randomised avoidance body (237 B) draw the shared gameplay LCG `00328370`, which is the
  stream [which roll](../21-RNG-And-Determinism/which-roll-is-on-which-generator.md) §3 now lists.
- Two locomotion bodies use `BattleStats_FindOwningBattleUnit`, and two call the id-validity query.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Rewards_Progression_Economy — SERVICE.** `0030E360` on this page calls `BattleUnit_ProcessDefeatRewardsAndLoot`, owned by that layer. What it reaches is defeat-and-loot processing, which reads the defeated unit's `+0x698` block, needs `byte[+5] == 1`, and is suppressed entirely by bit 3 of `byte[+0xE9A]`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatAI — CLIENT (SWE2-CONTRACT 2026-09-15, 19 edges).** `0030E130` calls
`GambitConfig_AdjustAvailableEntryCountByStatsRecord` — the rebuild tells the gambit layer its
available entries changed. The other 18 edges are caller fan-in: `AiOrder_EvaluateAndResolveActionTarget`,
`AiOrder_EvaluateTargetSelector`, `AiOrder_SelectFinalTargetFromCandidates`,
`AiOrder_BuildCandidateTargetBufferFromStoredRangeAndStatus`, `BattleUnit_SelectAiOrderSetVariantFromAuthoredUnit`
share `0031B760`/`00328370`; the `BattleEnmity_*` family and
`GambitConfig_LoadAuthoredPresetAndRebuildRuntimeOrders` share `00322C50`. One real service call
plus shared-resolver fan-in.

## SWE2-EC7-25 update (2026-09-18) — `0031E9A0` kind-to-band mapper

`0031E9A0` (68 B) maps `0031E9F0`'s kind byte to a band: `<= 0` returns 0,
`<= 5` returns 1, `== 6` returns 2, `7..9` returns 3 — the priority ladder
the rebuild pass orders by. Interior anchor `0031E9A4` (the kind call).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (FABLE, Claude Opus 5.5, 2026-09-25)

These paragraphs cover only the edges that the `FC-3` answer brings in by citing the presentation ring's
builder, tick and draw (`00506700`, `003BBA60`, `003BBB60`, `00505500`, `00505560`, `00505E00`,
`00505570`) and the number formatter `003EFD00`. Each layer's other edges into this page are not
dispositioned here, although the gate credits the layer name for all of them.

**Presentation — PROVIDER.** The recompute's request is drawn by the ring code: `003283D0` → `003BBD00` →
`00506700` builds the entry, `003BBA60` ages it and `003BBB60` → `00505560` → `00505E00` draws it. This
page relies on them for what the request shows. It does not describe the ring's other producers.

**UI — PEER.** `003EFD00`, the integer-to-decimal formatter the entry builder uses, is shared with UI code
(`002AE610`). Only its decimal output matters here.

**Resource — CLIENT, at one remove.** For type 0 the entry builder calls `0024A5A0` with `[01E0C1E8]` and stores the
result at entry `+0x30` (`00506864`–`00506869`). What that pointer is was not read, and nothing here relies on it.

**ActorEntity — PEER.** The entry builder encodes the actor handle through the actor registry, and the draw
resolves it back. This page claims nothing about the registry.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**Items_Equipment_Shops_License — CLIENT (23 edges).** `BattleStats_SetEquipmentSlotByStatsIndex` `0031A410`, `BattleStats_SetEquipmentSlotByMappedId` `0031A510`, `BattleStats_SetEquipmentSlotDirect` `0031A630` and `BattleStats_SetLicenseNodeStateAndApplySideEffects` `00323910` call the recompute `0030FED0` and the owner resolver `BattleStats_FindOwningBattleUnit` `0031B860`; `Equipment_EvaluateCandidateLoadoutAndBuildDerivedStats` `0030A4E0` calls `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30`; `LicenseData_BuildPrerequisiteNodeMaskForRequirement` `002F8FA0` calls the licence-node class query `00323890`; and 13 equipment, licence and inventory bodies call the id validator `BattleEncodedId_IsValidForClass` `00322C50`, among them `Equipment_CheckItemEligibleForSlot` `00317930`, `BattleStats_HasRequiredLicenseForEquipment` `00323C60`, `BattleStats_CheckLicenseNodeAcquireReason` `00323D10` and `InventoryDerivedIndex_UpdateOnPresenceTransition` `00325F40`. Setting an equipment slot or a licence node re-runs this rebuild through `0030FED0`, the loadout preview rebuilds effective stats through the same function, and the rest is shared use of the id validator and of the node-class query the licence row of the execution-order table reads.

**Party — CLIENT and SERVICE (13 edges).** The FC-3 gate `002FA3B0` calls `BattleUnit_GetPartyLeader` `003272A0`; `00328BD0`, which clears a member's equipment, calls `0030FED0`; `0030BEB0` calls `ActorWork_GetBattleUnit` `0031B760`; `BattleUnit_SeedPartyCombatStanceRecheckTimer` `003081E0` calls `RNG_SharedGameplayLCG_NextU32` `00328370`; and nine roster and focus bodies call `00322C50`, among them `PartyConfiguration_AddSelector07To25ToAvailablePrimaryIndex` `003170E0`, `PartyFocus_SelectAndRequestDefaultActor` `00326500`, `PartyConfiguration_ReconcileRuntimeRosterFirstThreeFromRequestedSelectors` `00328DB0` and `PartyConfiguration_SetDefinitionSelectorForIndex` `00329080`. The recompute's reaction request is gated on distance from the party leader (FC-3), a roster change that strips equipment re-runs the rebuild, and the remaining edges are the party code's use of the unit accessor, the shared gameplay LCG and the id validator.

**Script_VM_Native_Bridge — CLIENT and SERVICE (34 edges).** The `btlAtelSetAbility` handler `00510440` calls `002390B0`, and the `btlAtelSetStatus` handler `005103B0` calls `002394C0`; both handlers pop their arguments with `VMValueStack_PopInt32CoerceFloat32` `00267E10`; `005102D0` calls `0031B760`; and 29 verb handlers call the script-data resolver `002650B0`, among them `VM_Spawn_SetLaneCandidateTable` `005105A0`, `VM_Spawn_SetEntryMapAndResetTransientEntries` `00510620`, `VM_Spawn_InitializeKeepEntriesFromDefinition` `005106D0`, `0033F100` and `0050E060`. A foe's innate-augment word `+0xE80` and authored-status word `+0xE90` are written by two script verbs of the `btlAtel` family, as the section on the foe's two masks shows; the other edges are the verb layer's shared resolver that turns a script integer into a script-data pointer, and a unit lookup.

**Spawn_Encounter_Lifecycle — CLIENT (30 edges).** `SpawnUnit_FinalizeSpawnEntryActivation` `0023A410` calls `0030FED0`; 24 spawn bodies call `0031B760`, among them `SpawnLifecycle_CheckAndRetireByNativeRange` `002350C0`, `Spawn_SelectAndPrepareAutomaticEntry` `00235720`, `SpawnEntry_GetDeathCount` `00235F50` and `SpawnUnit_SetEntryMapAndResetTransientEntries` `0023A2E0`; and `Spawn_TrySelectCandidatePosition` `00234AF0`, `Spawn_PrepareRandomCandidateForCurrentEntry` `002355A0`, `SpawnPoint_GeneratePositionFromAuthoredRegion` `00236450`, `SpawnKeep_InitializeEntriesFromDefinitionTable` `002395A0` and `002398F0` call `00328370`. Spawn activation runs the rebuild once for the new unit; the rest is the spawn code resolving units through the same accessor and drawing from the same gameplay LCG.

**WorldAreaField — SERVICE (1 edge).** The status write `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360` calls `FieldData_GetActiveFieldRecordBit15` `00377C20`. The status write consults the active field record's action-permission bit; the rebuild itself does not read the field.

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../_index/candidates/opus-the-auto-status-rebuild-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0030BEB0` | 63 B | calls `0031B760(rcx)` with the incoming `rcx` and returns 0 when the result is null, when bit 3 of its dword `+0` is clear, when its qword `+0x698` is null or when byte `+5` of that object is non-zero; otherwise returns the inverse of bit 23 of the dword `+0` | `0030BEB4`, `0030BEC3`, `0030BEC7`, `0030BED3`, `0030BEDE` |
| `003241D0` | 100 B | returns 0 when `ecx - 1` is above 0x1D (unsigned); otherwise indexes a byte table after the body by `ecx - 1` and dispatches through a jump table, which (decoded from the bytes) give: `ecx` 1 to 3 returns 0x15, 4 to 6 0x16, 7 0x17, 8 0x18, 9 to 13 0x19, 14 0x1A, 15 to 17 0x1B, 18 0x1C, 19 and 20 0x1D, 30 0x1E, and 21 to 29 return 0 | `003241D2`, `003241D5`, `003241E1`, `003241F3`, `00324231` |
| `0033F100` | 77 B | calls `002640C0` with the incoming registers, pops a value with `00267E10(r9)`, resolves `002650B0(002640C0 result, rdx, value)` and tail-jumps `003E92F0(002640C0 result, resolved pointer)` | `0033F115`, `0033F120`, `0033F12E`, `0033F148` |
| `00505560` | 16 B | tail-jumps through the eight-byte entry, indexed by the sign-extended byte `+0x3C` of `rcx`, of the code-pointer table at `00D22790`, with `rcx`, `r8` and `r9` as passed in and `rdx` overwritten with the table base | `00505565`, `0050556C` |
| `0050E060` | 232 B | calls `002640C0` with the incoming registers and zeroes three stack floats; when `PartyFocus_GetCurrentPackedActorHandle()` is non-zero calls `Actor_GetWorldPosition(003588B0(that value), &float0, &float1, &float2)`; then resolves three pointers with `002650B0(002640C0 result, rcx, 00267E10(r9))` in turn and stores float0 through the third, float1 through the second and float2 through the first | `0050E0A0`, `0050E0C2`, `0050E0D8`, `0050E11F`, `0050E138` |
| `005105A0` | 63 B | pops a value with `00267E10(r9)`, resolves `002650B0(002640C0(), rdx, value)` and tail-jumps `002393E0(rdx, resolved pointer)` | `005105B0`, `005105B7`, `005105C5`, `005105DA` |
| `005106D0` | 60 B | pops a value with `00267E10(r9)`, resolves `002650B0(002640C0(), rdx, value)` and tail-jumps `002395A0(resolved pointer)` | `005106E0`, `005106E7`, `005106F5`, `00510707` |
