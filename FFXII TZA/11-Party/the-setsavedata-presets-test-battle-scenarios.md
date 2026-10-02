---
system: The SetSaveData presets — fifty scenario rows and 226 party presets that rebuild the party, its gear, gambits, licences and inventory when a script asks for a numbered save-data set
category: 11-Party
status: AUDITED — the last open box, the scenario row's +0x09/+0x0B/+0x0C (unread) and the preset's +3 (the rank byte) (UQ-128), answered 2026-09-17
owner_layer: both
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 18 cited function entries, 0 of them among the 109 records that changed GN160 -> GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0), established for this document 2026-09-14 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
corpus_validated: "the us battle_pack.bin scenario table (directory +0xF4, 50 x 208 B) and party preset table (+0xF0, 226 x 44 B) decoded: every formation slot, item, equipment id and gambit preset resolved through the class tables, 2026-09-11"
last_reviewed: 2026-09-13
registry_slots:
  - "0x02EBF030"
  - "0x02EBF028"
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-setsavedata-pass-1 - both tables re-extracted and their st2e headers declare count and stride themselves (50 x 208, 226 x 44), with the published file offsets being the SECTIONS and the rows starting 0x20 later; the preset censuses, the scenario 1 and 2 controls and preset row 0 all reproduce exactly; CORRECTED: the MP percentage is not always 100 - 220 of 226 are, four are 80 and two are 70; ADDED: the nine non-FFFF LP words are 1000 x8 and 5000 x1, and both tables are byte-identical in all nine languages
  crossref_clean: true
  reopened_count: 0
---

# The SetSaveData presets — fifty scenario rows and 226 party presets that rebuild the party, its gear, gambits, licences and inventory when a script asks for a numbered save-data set

> **A script verb, `btlAtelSetNextSetSaveData(n)`, stores one byte; the next area initialisation
> reads it and, if it is not −1, throws the whole battle state away and rebuilds it from two
> authored tables: scenario row `n` (the nine-slot formation, the gil, up to 64 items with counts)
> and every party preset row whose first byte is `n` (a character's level, five equipment ids, a
> gambit preset, LP, MP percentage).** The fifty scenarios are the *test battle* sets the archive's
> `test_battle` path is named for — scenario 0 is Reks alone, 1 is Vaan alone, 2 is a level-47 Vaan
> with an Artemis Bow, Genji gear and thirty Megalixirs — and the retail executable still carries
> the verb, the tables and the code.

**Corpus validation, before anything else.**

| | |
|---|---|
| tables | `battle_pack.bin` directory `+0xF4` → registry slot `02EBF030`, `st2e` **50 × 208 B** (section at `0x292E0`, **rows at `0x29300`** — the `st2e` header is `0x20` bytes and declares the count and stride itself, §10); directory `+0xF0` → slot `02EBF028`, **226 × 44 B** (section `0x26BE0`, rows `0x26C00`) |
| resolved | every formation byte through the party table (bank 8), every item and equipment id through the class tables of [the encoded-id space page](../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md) §2.5, every gambit preset id as a class-10 id (`0x5000` + row) |
| positive controls | scenario 0 = *Reks* alone (the prologue's party); 1 = *Vaan* alone with 150 gil; 2 = Vaan, then Ashe, Fran, Balthier, Basch, Penelo in slots 4–8, 500 gil, Megalixir × 30, Hi-Potion × 10 …; preset row 0 = scenario 2, slot 0 (Vaan), level 47, Artemis Bow / Parallel Arrows / Genji Helm / Genji Armor / Bangle, gambit preset `0x500B` |
| censuses | preset rows exist for scenarios 2–49 (none for 0 and 1); 217 of 226 presets carry LP `0xFFFF` ~~(the licence-mask path)~~ (no licence grant), 9 carry a number *(corrected 2026-10-02, OPUS: `00239C4F cmp word ptr [rbp + 0x20], r13w` with `r13w = 0xFFFF` (`00239A8C`, `00239B64`), then `00239C54 jne 0x239ce1`, the board loop — it runs when LP is NOT `0xFFFF`; an LP of `0xFFFF` takes `0016D6A0`, a bare `ret 0`)* — **`1000` in eight rows and `5000` in one**; ~~every row's MP percentage is 100~~ **220 of 226 are 100, four are 80 and two are 70** (corrected §10) |

---

## 1. What the player sees

Nothing, in the shipped game, unless a script calls the verb: these are developer test sets~~, and~~
~~no shipped event needs to~~ *(answered: two shipped scripts call it — `naf_b04` selects set 1 and `evt_t0505` cycles sets 0–3, §7 FZ-5; 2026-10-02, OPUS)*. What they *are* is a complete recipe for putting a party into a known
state — which is exactly what a modder, a test harness or a reconstruction wants, and the engine
executes it on the next area initialisation.

## 2. Native mechanism

### 2.1 The byte, its verb, and where it is kept

`btlAtelSetNextSetSaveData` (verb `302B`, `0050F810`) pops an integer and stores its low byte at
**`0208D455`** (`0050F81C`); `btlAtelGetNextSetSaveData` (`302C`, `0050F830`) reads it back.
`BattleStorage_InitializeWorkArrays` writes it at storage initialisation (`00236A04`), `0023A110(cl)`
sets it for `00394130`, and the world-transition snapshot carries it across a field transition
(`WorldTransitionSnapshot_CapturePersistencePairForActiveSlot` stores it into the metadata record
at `005845BB`, the restore writes it back at `00584482`). The byte sits next to the spawn-history
bank byte `0208D454`.

### 2.2 The apply — `00239960`, from `BattleSystem_InitializeAreaState`

`00239960` reads the byte into `r12d` (`00239966`); a value other than −1 is copied to `0208D456`
and the byte is reset to −1 (`00239975`–`0023997B`) — **a set is applied once**. −2 short-circuits
to `BattleSystem_ResetRuntimeState`; a negative value returns; a value at or past the scenario
count returns (`002399BB`). Otherwise, in order:

1. **the block is reset** (`002370C0`, `002399E9`), with bits 12, 13 and 14 of the state block's
   flag dword carried across the reset (`002399F5`–`00239A45`) and two deferred requests — bits 1
   and 2 of the dword at `02089344`, the battle-state word's neighbour — folded into bits 13 and 14
   and cleared (`00239A45`–`00239A85`);
2. `003183A0` clears a four-qword record; **all forty party stats records are re-initialised**
   from party-table rows 0 … 39 (`BattleStats_InitializeDefinitionRecord(record i, i)`,
   `00239AA0`–`00239ACE`);
3. **the scenario row** `R = 02EBF030[n]`: **gil** `= R.u16[+0xE]` (`GameState_SetGilClampedNonnegative`,
   `00239B11`–`00239B1D`); `003047F0` zeroes every inventory region A through the class descriptors
   and compacts (`00253480`); then **64 items** — `R.u16[+0x10 + 2i]` with count `R.u8[+0x90 + i]`,
   each non-`0xFFFF` id with a non-zero count granted through
   `Inventory_MutateEncodedItemPrimaryChannelMode1` (`00239B33`–`00239B5F`);
4. **every party preset row** `P` of `02EBF028` whose byte 0 equals `n` (`00239BBC`–`00239BC3`):
   the stats record by battle slot `P.u8[1]` (`BattleStats_GetByBattleSlotIndex`), the level
   grower to `P.u8[2]` (`0030C470`), record `+0x20 = P.u8[3]`, the gambit preset `P.u16[+0xE]`
   (`GambitConfig_LoadAuthoredPresetAndRebuildRuntimeOrders`), the LP block `+0x190`–`+0x1C1`
   zeroed and LP set to `P.u16[+0x20]` (`00323790`); if the slot is one of the six main members
   (`≤ 6`) and that LP word is `0xFFFF`, `0016D6A0` is called with the record (`00239C49`–`00239C5D`);
   the five equipment slots from `P.u16[+4 … +0xC]` (`BattleStats_SetEquipmentSlotDirect(record, k,
   id)`, `00239C62`–`00239CBF`); then MP: when the record's `+0x6C` and `+0x7C` are non-negative,
   `+0x4C = (+0x28 × P.u8[+0x28]) / 100` — **the MP percentage** (`00239CC4`–`00239D7F`);
   otherwise (LP word not `0xFFFF`) the **licence board**: every node row of `02EBF038` whose byte
   `+7` has bit `slot` set is granted through `BattleStats_SetLicenseNodeStateAndApplySideEffects`
   (`00239CE1`–`00239D63`); finally record flag bit 2 is set or cleared from bit 0 of the byte
   *at `P + 0x2C`* — which, with a 44-byte stride, is the *next* row's scenario byte (`00239D83`–`00239D94`);
5. **the formation**: the nine bytes `R.u8[0 … 8]` go to
   `PartyConfiguration_SetDefinitionSelectorForIndex(i, byte, 3)` (`00239DC0`–`00239DD9`),
   `00327870(R.u8[+0xA])` selects through the state block's `+0x5A48` selectors, and `002CFD10(−1)`
   closes.

### 2.3 The two rows

**Scenario row** (`02EBF030`, 208 B): `+0x00 u8 slot[9]` (party-table row per formation slot,
`0xFF` empty), `+0x09 u8`, `+0x0A u8` (the selector passed to `00327870`), `+0x0B u8`, `+0x0C u16`,
`+0x0E u16 gil`, `+0x10 u16 item[64]`, `+0x90 u8 count[64]`. Shipped: scenario 0 *Reks / — …*, 0
gil, no items; 1 *Vaan*, 150 gil; 2 *Vaan, —, —, —, Ashe, Fran, Balthier, Basch, Penelo*, 500 gil,
Megalixir × 30, Hi-Potion × 10, Phoenix Down × 10, Remedy × 10, Elixir × 55, Hero's Blade × 10 …; 3
adds *Larsa*; 10 *Vaan* and *Reddas*; 20 and 49 carry gil `0xFFFF` (65,535 after the zero-extend)
and a magick list (Curaga / Curaja, Expose, …).

**Party preset row** (`02EBF028`, 44 B): `+0 u8 scenario`, `+1 u8 battleSlot`, `+2 u8 level`,
`+3 u8` (→ record `+0x20`), `+4 u16 equipment[5]` (weapon, off-hand, head, body, accessory),
`+0xE u16 gambitPreset` (`0x5000` + row), `+0x10 … +0x1F` zero in every row, `+0x20 u16 lp`
(~~`0xFFFF` = grant the board's per-slot mask instead~~ any value but `0xFFFF` grants the board's per-slot mask, for battle slots ≤ 6 *(corrected 2026-10-02, OPUS: `00239C49`–`00239C54`)*), `+0x22 … +0x27` zero, `+0x28 u8 mpPercent`
~~(100 in every row)~~ (100 in 220 rows, 80 in four and 70 in two *(corrected 2026-10-02, OPUS: re-read from the shipped `battle_pack.bin` directory `+0xF0`, bound to `02EBF028` at `00236FBC`–`00236FCA`; §10)*). Shipped: 226 rows for scenarios 2–49, two to seven rows each — scenario 2 gives
Vaan level 47 with Artemis Bow, Parallel Arrows, Genji Helm, Genji Armor and a Bangle and Ashe,
Fran and Balthier level 51 with Onion Arrows and a Battle Harness; scenario 3 is a level-99 set with
Genji Gloves; scenario 4 a level-20 Vaan with a Longsword; scenario 38 a level-12 Fran with an Aevis
Killer.

### 2.4 What this settles elsewhere

- The `test_battle` path of `battle_pack.bin` is these sets: the *tables* the shipped game uses
  (party, action, status, bazaar …) live in the same pack and are byte-identical across languages;
  the scenarios are the reason the pack is called what it is.
- **The starting inventory grant table `02EBF048` is empty because the scenarios carry their own
  inventories** (step 3) — the encoded-id page's FY-7 question on that table.
- **The licence board's row byte `+7` is a per-slot mask** the preset path grants from — a second
  reader of that byte beside the board itself.

## 3. Key addresses

| Address | Role |
|---|---|
| `0208D455` | the pending set byte, −1 when none |
| `0050F810` / `0050F830` | `btlAtelSetNextSetSaveData` / `…Get…` (verbs `302B` / `302C`) |
| `00239960` | the apply, from `BattleSystem_InitializeAreaState` |
| `02EBF030` | the scenario table, 50 × 208 |
| `02EBF028` | the party preset table, 226 × 44 |
| `0023A110` | sets the byte for `00394130` |
| `00327870` | the formation selector step |
| `003047F0` | clears every inventory region before the scenario's items |

## 4. Data structures and formulas

```
byte 0208D455: -1 none ; n >= 0 apply scenario n once at the next area initialisation ; -2 reset only

ScenarioRow (208 B):   u8 slot[9] ; u8 ; u8 selector ; u8 ; u16 ; u16 gil ; u16 item[64] ; u8 count[64]
PartyPresetRow (44 B): u8 scenario ; u8 battleSlot ; u8 level ; u8 field20 ; u16 equip[5] ; u16 gambitPreset ;
                       u8 zero[16] ; u16 lp (0xFFFF = board mask) ; u8 zero[6] ; u8 mpPercent ; u8 zero[3]   <- corrected 2026-10-02, OPUS - the board mask is granted when lp != 0xFFFF and the slot is <= 6 (00239C49-00239C54)
MP after apply = maxMP (+0x28) * mpPercent / 100            (record +0x6C, +0x7C >= 0)
licence grant   = every 02EBF038 row with (row[+7] >> battleSlot) & 1, when lp == 0xFFFF   <- corrected 2026-10-02, OPUS - when lp != 0xFFFF and battleSlot <= 6 (00239C49 cmp r14d, 6 / jg; 00239C4F / 00239C54 jne 00239CE1)
```

## 5. Call chain

```
script: btlAtelSetNextSetSaveData(n) -> 0208D455 = n
area load: BattleSystem_InitializeAreaState -> 00239960
  -> reset block ; 40 x BattleStats_InitializeDefinitionRecord
  -> gil ; 003047F0 ; 64 x Inventory_MutateEncodedItemPrimaryChannelMode1
  -> per preset: level grower ; gambit preset ; LP or licence mask ; 5 x SetEquipmentSlotDirect ; MP %
  -> 9 x PartyConfiguration_SetDefinitionSelectorForIndex ; 00327870 ; 002CFD10(-1)
```

## 6. Modding notes

- **A complete party state is one scenario row plus its preset rows**, and the verb is live in the
  retail executable: a script that calls `btlAtelSetNextSetSaveData(n)` before a field transition
  gets scenario `n` applied on arrival — formation, gil, inventory, levels, gear, gambits, licences.
- **The apply is destructive**: the block is reset and every inventory region zeroed before the
  scenario's items are granted; nothing of the previous state survives except state flag bits
  12–14.
- **Presets are keyed by scenario byte, not by row order**; adding a character to scenario `n`
  is a new 44-byte row with byte 0 = `n`.
- ~~The MP percentage is the only per-preset number every shipped row leaves at 100.~~ The MP percentage is 100 in 220 of the 226 shipped rows; four are 80 and two are 70 *(corrected 2026-10-02, OPUS: §10, re-read from the shipped `battle_pack.bin`)*.

## 7. What is not known

- [x] ~~**Who reaches `00394130`**, the second setter of the byte~~ *(box left for the ledger mirror (FZ-5), 2026-09-14 FABLE: the row's own text is answered, ~~its verdict cell still OPEN~~)* *(answered: the register row's verdict cell reads ANSWERED, verdict set 2026-09-14; 2026-10-02, OPUS)* **— answered 2026-09-11:** the
      script verb `fsttl_newgamestart` (`705D`, thunk `00512130` → `00394640`), which, when no such task
      exists (`02AEE4D0 == 0`, `00394640`–`00394648`), registers `00394130` as the proc of a kind-`0xF0`
      task through the widget factory `00244F50` (`0039464A`–`00394659`); the proc validates the
      active save image (`SaveImage_ValidateRuntimeFormatHeader`, `003941DC`), resets it when invalid
      (`SaveRuntime_ResetActiveImageAndRebindState`, `003941E5`) or binds it (`00233C10`, `00394222`),
      and sets the byte on the way ([the verb table](../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv)). **Answered 2026-09-11 — two of the 1,115 `us` scripts call it.** A byte walk for the four
      call opcodes (`0x58`, `0x59`, `0x5D`, `0x5E`) followed by the id `0x302B` finds six sites, every
      one `CALLPOPA` and every one preceded by the verb's single int push (`0x4F imm16`) or a variable
      push: `plan_map/naf_b/naf_b04/global/naf_b04.ebp` at `0x1CF4` pushing **1**, and
      `event/evt_t/evt_t0505/evt_t0505.ebp` at `0x8159`, `0x816E`, `0x8399`, `0x85B0` pushing 3, 2, 0
      and 0, and at `0x8144` after a variable push (`0x48 0xDD`). So the set-save-data path is not
      test-only: the field script of `naf_b04` selects set 1 — whose scenario row exists but has no
      preset rows — and the event `evt_t0505` cycles sets 0–3. (The walk is a byte scan aligned by
      the preceding three-byte pushes, not a full disassembly.) **FZ-5.**
- [x] ~~**UQ-128.** The scenario row's `+0x09`, `+0x0B` and `+0x0C` fields, zero in every shipped row, and the~~
      preset's `+3` field. *(A companion of FZ-5, not FZ-5's own question; own id from the register pass 2026-09-14.)*
      ***ANSWERED 2026-09-17 (FABLE): the three scenario bytes have no reader in this build, and the preset's `+3` is the stats record's rank byte.** The scenario table descriptor `02EBF030` is referenced by exactly two functions: the pack registration `00236C30`, which hands the slot to `003845F0` with the pack index `[0208E680]+0xF4` (`00236FA2`..`00236FB0`), and the applier `00239960`. The applier's row reads are the nine slot bytes, the selector `+0x0A` (`00239DDB`, to `00327870`), the gil word `+0x0E` (`00239B11`) and the item and count arrays from `+0x10` and `+0x90`; nothing reads `+0x09`, `+0x0B` or `+0x0C`. Its `+0xC` reads are the descriptor's row count through `0020E600` (`00239ADC`, `00239AF0`, `00239B8A`, `00239D02`) and the preset row's accessory word (`00239CB0`), not the scenario row. Three authored bytes that every row leaves at zero and no code loads are padding the authoring format carried. The preset's `+3` is stored as a byte at the member's stats record `+0x20` (`00239BF2`..`00239BF6`) right after `0030C470` has grown the record to the preset's level, and that offset is the rank byte [the stats record page](../08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md) maps, the one the party arm of the unit builder sets to the larger of row byte 46 and the licence-derived rank. A preset therefore writes the member's rank directly. Static, descriptor reference census and applier body read.*
- [x] ~~**UQ-129.** Whether the read at `P + 0x2C` — the next row's scenario byte, bit 0 — is intended.~~
  **NO ADMISSIBLE SOURCE** (2026-09-14, FABLE; EVIDENCE-STANDARD addendum 2026-09-15bk): what the read does is exact.
  It sets or clears stats flag bit 2, the flag that keeps a party unit off its issued-command gambit set
  ([UQ-123](../09-Combat-AI-And-Gambits/which-gambit-set-fires-and-how-a-command-switches-it.md)). Whether reading the
  next row was intended is intent.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| the verb stores the byte; the getter reads it | `0050F814`–`0050F81C`; `0050F830`; verbs `302B` / `302C` in [the verb table](../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv) | 1 |
| the apply's gate, one-shot reset, and −2 | `00239966`–`00239996` | 1 |
| the block reset with bits 12–14 carried, the forty records | `002399E9`–`00239ACE` | 1 |
| gil, region clear, 64 items | `00239B11`–`00239B5F`; `003047F0`–`0030483D` | 1 |
| the preset loop: level, gambit, LP / licence mask, equipment, MP percentage, flag bit 2 | `00239B70`–`00239D9A` | 1 |
| the formation and the tail | `00239DC0`–`00239DE8` | 1 |
| the byte's other writers and its transit through the transition snapshot | a whole-image rip-relative census of `0208D455`–`0208D456`, 2026-09-11 | 1 |
| every decoded value of the two tables | the `us` sections at `0x292E0` and `0x26BE0`, resolved through the class tables | data |

## 9. Related

- [`the-encoded-id-space-and-the-query-record.md`](../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md) — the inventory regions the apply clears, the class tables the ids resolve through.
- [`the-battle-state-block-field-map.md`](Battle-State-Block/the-battle-state-block-field-map.md) — the block that is reset.
- [`how-a-battle-unit-is-built-from-its-definition.md`](../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md) — the definition records the forty re-initialisations fill.
- [`the-world-tick-and-the-field-frame.md`](../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md) — the state flag dword whose bits 12–14 survive.
- [`the-save-payload-field-map.md`](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md) — the transition metadata record the byte rides in.

## 10. Falsification pass 1 — 2026-09-13 (OPUS)

*(Static only — both tables re-extracted from the shipped archive, read never written. Nothing
executed.)*

### ✔ The tables declare themselves, and the censuses mostly reproduce

Both sections open with an **`st2e` header that states its own geometry**, so the shapes are the
file's declaration rather than an inference:

| | directory | section | header says | rows begin |
|---|---|---|---|---|
| scenarios | `+0xF4` | `000292E0`–`0002BBA8` | **count 50, stride 208** | `00029300` |
| presets | `+0xF0` | `00026BE0`–`000292E0` | **count 226, stride 44** | `00026C00` |

**The published file offsets are the *sections*; the rows start 32 bytes later.** A reader who
seeks to `0x292E0` and reads 208 bytes gets the header plus five sixths of scenario 0.

Reproducing exactly: preset rows for **scenarios 2–49 and none for 0 or 1**; **LP `0xFFFF` in 217 of
226**; scenario 1 one slot and **150 gil**; scenario 2 slots `0, –, –, –, 1, 2, 3, 4, 5` and
**500 gil**, with **id `0x15` × 30** and **id `0x01` × 10** among its twenty stocked entries; preset
row 0 = **scenario 2, slot 0, level 47, gambit preset `0x500B`**, five equipment ids and LP `0xFFFF`.

### ✖ Corrected: the MP percentage is not always 100

The corpus row states *"every row's MP percentage is 100"*. Measured over all 226:

| value | rows |
|---:|---:|
| 100 | **220** |
| 80 | **4** |
| 70 | **2** |

**Six rows are not 100.** The field is the one §2.2 step 4 uses as `+0x4C = (+0x28 × P.u8[+0x28]) / 100`,
so those six start their character below full MP on purpose — which is the sort of thing a test set
exists to do, and a census that says "every" hides it.

### ✔ Added: the nine LP numbers, and nine languages

The nine non-`0xFFFF` LP words are **`1000` in eight rows and `5000` in one** — the page counts them
and does not name them.

And both tables are **byte-identical in all nine languages**: one SHA-256 each across
`ch cn de es fr in it kr us`, at nine different file offsets. The page's `corpus_validated` line
covers the `us` copy.

### A note on §2.2's last step

*"record flag bit 2 is set or cleared from bit 0 of the byte at `P + 0x2C` — which, with a 44-byte
stride, is the next row's scenario byte"* is **arithmetically exact**: `0x2C` is 44, so `P + 0x2C` is
the next row's byte 0. It is worth keeping the consequence in view — **the last of the 226 rows reads
past the table**, into whatever follows the section, and the header says the rows end at `000292D8`
with the section ending `000292E0`, so those eight bytes are what the last row reads.

**Not claimed.** The apply path `00239960` was **not re-read** — §2.2 stands as written, including the
bound check, the reset-bit carrying and the licence-mask arm. The item and equipment ids were **not
re-resolved through the class tables**; this pass measured the table geometry and the censuses over
it. Nothing was executed.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL and recorded in the registry.*

**Rewards_Progression_Economy — SERVICE.**

- The preset applier `00239960` sets gil through `GameState_SetGilClampedNonnegative` and calls the 432-byte level-rank
  function.
- That function (`0030C470`) is also called by a 488-byte rewards body, and it calls a 122-byte helper and
  `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth`.

**A preset sets gil and levels characters through the ordinary level-up path**, so growth rolls draw the gameplay MT
as a normal level-up does.
- **CombatAI - CLIENT and SERVICE (4 edges).** `003845F0` is also called by bodies filed to combat AI: `00238880`; `00233C10`, `00236C30`, `00239960` reach bodies filed to combat AI: `00327F80`, `00238880`, `00327CB0` - shared machinery across the layer boundary, no shared ownership.
- **Items - SERVICE (1 edge).** `00236C30` reaches bodies filed to items: `00238660` (BattleData) - shared machinery across the layer boundary, no shared ownership.
- **Items_Equipment_Shops_License - CLIENT and SERVICE (6 edges).** `002370C0` is also called by bodies filed to items/equipment: `0023AF50`; `00233C10`, `00239960` reach bodies filed to items/equipment: `0030B6A0`, `00300BA0`, `0031A630` - shared machinery across the layer boundary, no shared ownership.
- **SaveLoad - CLIENT (2 edges).** `00233C10`, `002CFD10` are also called by bodies filed to SaveLoad (save/load settings): `00280140` (RuntimeLifecycleSupport) - shared machinery across the layer boundary, no shared ownership.
- **Save_Load_Settings - SERVICE (5 edges).** `00233C10`, `00253480`, `00394130` reach bodies filed to save/load/settings: `002EF640`, `00253240`, `00255260` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - SERVICE (1 edge).** `0050F810` reaches bodies filed to script VM / native bridge: `00267E10` - shared machinery across the layer boundary, no shared ownership.
- **Spawn_Encounter_Lifecycle - CLIENT (1 edge).** `0030C470` is also called by bodies filed to spawn/encounter lifecycle: `002398F0` - shared machinery across the layer boundary, no shared ownership.
- **Status_Periodic_Terminal - SERVICE (2 edges).** `0030C470` reaches bodies filed to status/periodic terminal: `0030F690`, `0030FED0` - shared machinery across the layer boundary, no shared ownership.
- **World - CLIENT and SERVICE (3 edges).** `003845F0` is also called by bodies filed to World: `00238640` (Area), `003847B0` (Area); `00236C30` reaches bodies filed to World: `003847B0` (Area) - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT and SERVICE (12 edges).** `00236C30`, `00239960` are also called by bodies filed to WorldAreaField (world area): `00238850`, `002342F0`; `00236C30` reaches bodies filed to WorldAreaField (world area): `003845F0`, `003846F0` - shared machinery across the layer boundary, no shared ownership.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — SERVICE.** Cited functions call a 7-byte core getter and a 40-byte core helper.

## Crossings into other layers — FINAL-AUDIT pass 22 (OPUS, 2026-09-18)

**Resource — this page is the CALLER.** `00236C30` calls `003843F0` at **`00236C6B`**. The callee
is a 36-byte fixed-argument wrapper — it plants `4` and `6` in the stack slots and `4` in `r9d`
(`003843F4`–`00384402`) and tail-calls through — so the crossing carries **constants chosen here**,
not a value from the resource layer. **This page consults it and owns nothing in it.**

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAction — CLIENT.** `BattleAction_UpdateSpecialPresentationSequence`, owned by that layer, calls `0030C470` on this page. That caller is a 911-byte sequence step that swaps the sentinel pair `byte[+0x694]` / `byte[+0x695]`, issues a `0x2001`-style order when the action's `byte[+0x1C]` is `8`, and then dispatches on `[022C215C] - 1` **bounded at 5**; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — CLIENT.** `FUN_0035c560`, owned by that layer, calls `00253480` on this page. That caller is a 68-byte reset that sizes its own block: **`0x23C8` bytes at `022C8060`** are zeroed, bit 5 of `[022C83E8]` is set, and the object built after it is stored at `[022C83B8]`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatFormula — MECHANICAL (SWE2-CONTRACT 2026-09-15, 6 edges).** The preset bodies share the page's cited
stats-resolver accessors with `BattleFormula_*`/`BattleStats_*` callers — fan-in, not a formula
relationship.

**Presentation — MECHANICAL (SWE2-EC7 batch 27, 1 edge).** `00579420` — the quest-list selection
state machine — calls `002527B0`, the first stage of this page's `002CFD10` preset compose. Shared
callee fan-in, not a UI relationship the preset layer owns.

## SWE2-EC7-27 update (2026-09-18) — `002CFD10` two-stage party compose

`002CFD10` (28 B) calls `002527B0(6, 4, 0)` then tail-jumps `0028E880`
— the fixed-selector compose the preset scenarios issue as
`002CFD10(-1)`. Interior anchor `002CFD1E` (the `002527B0` call).
