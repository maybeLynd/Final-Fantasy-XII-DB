---
system: Walking into an authored trigger point
category: 03-World-Area-Field
status: AUDITED
owner_layer: PrimaryOwner:WorldAreaField
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
last_reviewed: 2026-09-03
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: first-read-repos-55
  crossref_clean: true
  reopened_count: 0
---

# Walking into an authored trigger point

`BattleUnit_TryTriggerNearbyAuthoredFieldActivation` at **`002F8060`**, 648 bytes. Eight documents
cited it at its entry; none had opened it.

## What the player sees

**Every field can carry up to 32 invisible authored points. Walk close enough to one and it fires —
once, ever.** The point is removed from the field's live set the moment it triggers, so nothing about
the encounter is repeatable by walking back over the same ground.

**Each point carries two outcome values, and which one you get is a 75 / 25 coin flip** made at the
moment of the trigger — not authored, not seeded by position, drawn when you step on it.

## The trigger test

```asm
002F81D0  divss  xmm0, xmm6            ; authored coordinate / 10.0
002F81EF  call   0x003A1920            ; distance(point, unit)
002F81F4  comiss xmm7, xmm0
002F81F7  jnc    0x002F8218            ; fires when distance <= threshold
```

**Coordinates are authored in tenths and divided by 10 at read time** — two 16-bit values, a
horizontal pair. The threshold is **1.3**.

> **The authored point has no height.** The third component is written **zero** (`002F81C1`,
> `mov dword ptr [rsp+0x44], 0`) while the unit's own position is real in all three. **The unit's
> height therefore counts against the 1.3 budget directly** — a point is harder to reach from above or
> below it, and how much harder is a property of the area's authored ground level, not of the point.

That is a consequence of the code as written, not an inference about intent, and it is the kind of
detail that a distance check summarised as *"within 1.3 units"* would lose.

## The 75 / 25 roll

```asm
002F8218  call   0x00379CD0            ; the draw
002F8220  mov    eax, 0x51EB851F       ; the compiler's  % 100
002F8231  cmp    r8d, 0x4B
002F8235  jnc    0x002F823E
002F8237  movzx  r14d, word ptr [rsi + 0x6]     ; < 75  -> value A
002F823E  movzx  r14d, word ptr [rsi + 0x8]     ; >= 75 -> value B
```

**`0x4B` is 75, and the split is hardcoded in the instruction stream** — not read from the record, not
configurable per point. **The two outcomes are authored; the odds are not.**

This function is one of only **two** in the executable that both draw from the RNG and write a
persistent flag — a bound established independently elsewhere in this database, and this is the one
whose ratio is fixed at 75/25.

## The record, and the once-ever guarantee

| offset | width | use |
|---|---|---|
| `+0x00` | `s16` | first coordinate, tenths |
| `+0x02` | `s16` | second coordinate, tenths |
| `+0x04` | `u8` | **persistent flag id — `0xFF` means "set none"** (`002F8247`) |
| `+0x06` | `u16` | outcome value on the 75 branch |
| `+0x08` | `u16` | outcome value on the 25 branch |

On a hit, in order: **set the persistent flag** if it is not `0xFF` (`0032AD70(id, 1)`), build the
activation from the record (`002FB8C0`), hand the chosen value to the acting unit
(`0046A9D0`), notify with `003EC700(index, 3)`, and then

```c
002FB3B0(0x2EC3EA0, fieldId, mask & ~(1 << index));   // clear this point's bit
break;                                                 // at most one per call
```

**The live set is a 32-bit mask stored per field** in a 12-byte-stride table at `0x2EC3EA0`, found by
scanning for the current field id. **Clearing the bit is what makes the trigger once-only**, and the
`break` means **at most one point can fire per call** even if two overlap.

**The 32-point ceiling is not a coincidence of the data**: the loop bound is `min(count, 0x20)`, and
the live set is exactly 32 bits wide. **The mask is the limit, and the loop was written to respect
it.**

## Who is eligible to trip one

Read from the acting unit's battle record at `+0x698`:

- **bit 26** of `(rec[+0x64] | rec[+0x3C])` must be clear — the same two-word status pair the
  experience split and the periodic tick consult, here at a different bit;
- **bit `0x20` of `rec[+0x6C]` and of `rec[+0x7C]`** must both be clear — the two status layers again;
- `rec[+0x05] != 1`, and when `rec[+0x05] == 0`, `rec[+0x04]` must lie outside `0x1B … 0x27`.

> **That last pair is the same directional byte and the same 13-value band as the experience split**,
> written the same way — `sub 0x1B; cmp 0xC; jbe`. **Two unrelated systems excluding the same band of
> kinds is a fact about the band, and neither function says what it is.**

## Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Is `1.3` a radius or a squared radius? | **Compared against the callee's return directly** (`comiss xmm7, xmm0` at `002F81F4`), with no `sqrt` or squaring between. Whether `003A1920` returns a distance or its square is a property of that function and is **not** established here. |
| Is the 75/25 read from the record? | **No** — `0x4B` is an immediate at `002F8231`. |
| Is `+0x04` a short or a byte? | **Byte**: `movzx eax, byte ptr [rsi+4]` and `cmp al, 0xFF` (`002F8243`). The decompiler renders it as `(char)psVar12[2]`, which is the same byte reached through a `short*` — **and would read as "element 2 of a short array" to anyone quoting the pseudocode.** |
| Could the mask clear be a write to a copy? | It goes through `002FB3B0(table, fieldId, newMask)` — **a setter taking the table base and the field id**, not a local store. Whether it persists across a save is not established here. |
| Does the 32 cap come from the data or the code? | **Both, and they agree**: `min(count, 0x20)` bounds the loop and the live set is 32 bits. |

**What this document does not claim:** what the two outcome values are, what `0046A9D0` does with the
chosen one, what the persistent flag ids mean, what `003EC700`'s second argument `3` selects, or what
the excluded kind band `0x1B … 0x27` contains.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

**Answered from the callee — the falsification table's first attack.** `003A1920` returns a **distance**, not its
square. It computes `(a.x−b.x)² + (a.y−b.y)² + (a.z−b.z)²` (`003A1920`–`003A194C`) and tail-jumps to `sqrtf`
(`003A1950`). So `1.3` is a radius in world units, and the zero height of the authored point counts against it
linearly.

- **Movement — SERVICE shared with its owners.** `003A1920` is Movement's general 3-D distance. It is also called by:
  - `Movement_UpdateSteeringTowardTarget`;
  - `Navigation_TestSegmentAgainstAuxObstaclesXZ`;
  - four unnamed movement bodies of 431–851 bytes.

  The trigger test borrows it. Nothing trigger-specific is in it.
- **Script_VM_Native_Bridge — CLIENT.**
  - Three script-verb bodies (124–165 B) call the same distance.
  - Two tiny verb bodies (25 B and 28 B) reach `PersistentFlag_SetBank512Low` (`0032AD70`). That is the setter a hit
    uses for the record's persistent flag, so scripts can set the same bank.
- **Story_Event_Quest_Hunt — SERVICE.** On a hit, `BattleUnit_TryTriggerNearbyAuthoredFieldAction` (`002F8060`) sets
  the record's persistent flag (`+0x04`, unless `0xFF`) with `PersistentFlag_SetBank512Low`. That is a story-flag side
  effect. The once-ever guarantee itself is still the per-field mask clear described above.
- **ActorEntity — SERVICE.** `002F8060` and `002FB8C0` read unit positions through `Actor_GetWorldPosition`. `002FB8C0`
  also maps a definition selector through `BattleUnit_FindMappedDefinitionSelectorByIndex`.
- **Party — CLIENT.** `PartyFocus_ProcessActorControlPresentati…` calls the distance.
- **Presentation — SERVICE.** `003EC700` indexes the sixteen marker slots through a 38-byte Presentation helper; the
  argument `3` remains unread, as stated above.
- **RNG_Random_Selection - SERVICE (1 edge).** `002F8060` reaches bodies filed to random selection: `00379CD0` - shared machinery across the layer boundary, no shared ownership.
- **Save_Load_Settings - SERVICE (1 edge).** `0032AD70` reaches bodies filed to save/load/settings: `002EF2B0` - shared machinery across the layer boundary, no shared ownership.
- **Status_Periodic_Terminal - CLIENT (2 edges).** `002F8060`, `00379CD0` are also called by bodies filed to status/periodic terminal: `00310DB0`, `00386C70` - shared machinery across the layer boundary, no shared ownership.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatFormula — CLIENT (53 edges, one fan-in).** All 53 edges are CombatFormula bodies calling `00379CD0` on this page: the five-byte thunk onto the CRT's Mersenne Twister that this page documents. `BattleFormula_RollGuardParryMode` is the worked example - it reduces its draw modulo 100 against the threshold at `[02AEDFDC]`. The crossing is **one shared primitive with 53 callers**, not 53 separate relationships, and naming a single body would say less than the count does. Edge count from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**CoreRuntimeScheduling — CLIENT (2 edges, one fan-in).** All 2 edges are CoreRuntimeScheduling bodies calling `00379CD0` on this page: the five-byte thunk onto the CRT's Mersenne Twister that this page documents. `FUN_0022b7e0` is the worked example - it draws once inside a fixed per-frame call sequence before spinning on `[02EBA3F8]`. The crossing is **one shared primitive with 2 callers**, not 2 separate relationships, and naming a single body would say less than the count does. Edge count from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Rewards_Progression_Economy — CLIENT (2 edges, one fan-in).** All 2 edges are Rewards_Progression_Economy bodies calling `00379CD0` on this page: the five-byte thunk onto the CRT's Mersenne Twister that this page documents. `FUN_002f9a60` is the worked example - it draws once while reading the reward table at `[02EBF108]`. The crossing is **one shared primitive with 2 callers**, not 2 separate relationships, and naming a single body would say less than the count does. Edge count from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).
