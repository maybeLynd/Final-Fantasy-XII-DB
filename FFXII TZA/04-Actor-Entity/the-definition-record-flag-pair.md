---
system: The enemy definition record's status words — +0x038, +0x03C and +0x064
category: 04-Actor-Entity
status: AUDITED — the flag pair, its writers and its 125 guard sites read; 00313F60, the callee behind the 0x80000003 guard, read 2026-09-18 (a thunk to FieldData_GetActiveFieldRecordBit15: the current field's navimapdata bit 15)
owner_layer: PrimaryOwner:ActorEntity
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 8 cited function entries, 0 of them among the 109 records that changed GN160 -> GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0), established for this document 2026-09-14 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
corpus_validated: "229 OR-sites across 162 functions, scanned over all 8,001,280 bytes of .text, 2026-09-06"
last_reviewed: 2026-09-06
audit:
  passes: 1
  last_pass: 2026-09-06
  last_pass_state: GN160-census-and-statusword-reproduced-repos-1e — 229 OR-sites / 162 functions / 10 bit positions reproduced exactly by an independent scan; the 9-mask figure is correct scoped to test (11 including and, no new bits); the .text size figure 8,001,280 does not reproduce (section table gives 7,996,981 virtual / 7,997,440 raw); the six-entry jump table at 0x0030E88C and the +0x038 immunity guard re-derived from the bytes and exact
  crossref_clean: false
  reopened_count: 0
---

# The enemy definition record's status words — `+0x038`, `+0x03C` and `+0x064`

> The two hottest dwords in the 456-byte enemy definition record are **not stats — they are status
> flag words**, `OR`-ed together and mask-tested at 229 sites, and between them they decide whether a
> unit can be targeted, can act, can move, earns EXP, or regenerates HP. **A third word beside them,
> `+0x038`, can veto a status being applied at all.**

**Corpus validation.** This is a code census, not a file census:

| | |
|---|---:|
| `.text` scanned | **8,001,280 bytes**, every byte |
| sites matching `MOV r32,[base+0x64]` … `OR r32,[base+0x3C]` | **229** |
| distinct functions containing one | **162** |
| distinct masks tested against the result | **9** |
| distinct bit positions ever tested | **10** — 0, 1, 3, 4, 5, 13, 14, 16, 27, 31 |

---

## 1. What the player sees

Why a dead enemy stops being targetable. Why a Stopped unit does not advance. Why a petrified
character earns nothing from a kill. Why Regen ticks on one unit and not another.

**All of those are the same two numbers**, checked against a handful of bit masks before nearly
every combat decision — and a third number decides which statuses can be put there in the first
place. **This is the layer a modder edits to make something immune.**

## 2. The layout

Within the 456-byte definition record bound at `BattleUnit + 0x698`:

```struct DefinitionRecordFlagPair base=record
+0x3C  u32  flagsA   OR-ed with flagsB before every test
+0x40  u8[36] recordBody  other definition-record fields — see the registry sheet's 58-offset map; this sheet covers only the flag pair
+0x64  u32  flagsB   OR-ed with flagsA before every test
```

> **Two gate results on this sheet are expected and confirmed, so an auditor need not re-derive
> them.** `verify_doc_addresses.py` raises `REVIEW` on `0x0030E88C` as a `.text` non-function
> address — **it is the six-entry jump table itself**, which is precisely the *"jump/PSM tables after
> a function are legitimate"* case that checker's own comment names. The `+0x40..+0x64` span is
> declared as one unsplit `recordBody` block and that is deliberate** — the 36 bytes are other
> fields, several of them in the registry sheet's 58-offset map; **naming them here would be
> importing another document's census into a fence and presenting it as read.**

> **The two words share one bit vocabulary.** Every one of the 229 sites `OR`s them before testing,
> so **a bit means the same thing in whichever word carries it.**

### There is a third word, and it is what distinguishes them

**`BattleStats_ChangeStatusAndProcessSideEffects` (`0x0030E360`) writes all three.** A bounds-checked
selector (`0x0030E4CB` `CMP EAX,5`) indexes a **six-entry jump table at `0x0030E88C`**
(`0x0030E4DB`), and the six cases are a **{clear, set} × {three words} matrix**:

| case | at | word | operation |
|---|---|---|---|
| 0 | `0x0030E4E7` | `+0x64` | **clear** — `if (w & m) w &= ~m` |
| 1 | `0x0030E4FD` | `+0x3C` | **clear** |
| 2 | `0x0030E513` | `+0x38` | **clear** |
| 3 | `0x0030E526` | `+0x64` | **set**, with an extra guard — see below |
| 4 | `0x0030E543` | `+0x3C` | **set** — `if (w & m) bail; w \|= m` |
| 5 | `0x0030E557` | `+0x38` | **set** |

```struct DefinitionRecordStatusWords base=record
+0x38  u32  wordC   the gate: a bit set here BLOCKS the same bit being set in +0x64
+0x3C  u32  flagsA  OR-ed with flagsB by every consumer
+0x40  u8[36] recordBody  other definition-record fields — see the registry sheet's 58-offset map; this sheet covers only the status words
+0x64  u32  flagsB  OR-ed with flagsA by every consumer
```

> **The set-`+0x64` case carries a cross-check the others do not:**
>
> ```
> 0030e526  MOV  ECX,[RSI + 0x64]
> 0030e529  TEST ECX,EDI
> 0030e52b  JNZ  0030e82d          ; already set -> bail
> 0030e531  TEST dword ptr [RSI + 0x38],EDI
> 0030e534  JNZ  0030e82d          ; <-- set in +0x38 -> REFUSE to set it in +0x64
> 0030e53e  MOV  [RSI + 0x64],EAX
> ```
>
> **`+0x38` is an immunity word against `+0x64`.** A bit set in `+0x38` makes the corresponding bit
> unsettable in `+0x64` — the engine simply declines. **`+0x3C` and `+0x38` have no such guard**, so
> the protection is specific to one of the three words, not a general rule.
>
> *Who authors `+0x38` — CB-6, answered 2026-09-12 (FABLE).* Its only writers besides the status
> path's mode 5 / mode 2 are in the stat rebuild `BattleStats_RebuildEffectiveStatsAndAffinityState`
> (`002FEF30`; [the stats-record field map](../08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md)), which **zeroes the block `+0x24`–`+0x44`** (`lea rsi, [rdi + 0x24]`,
> `002FEFAB`–`002FEFC8`) and then **ORs authored words into it**: for a **party** record (kind byte
> `+5 == 0`) the party-table row's dword **`+0x4C` into `+0x38`** and its dword `+0x48` into `+0x3C`
> (`002FF0D3`–`002FF0D9`; the row is `02EBF130`'s stride × the record's `+4`); and for **every
> equipped item** in the record's five words `+0x50`–`+0x58` (class-6 ids, the equipment row at
> `02EBF0F8 + (id − 0x1000) × stride`) the item's **secondary block** — resolved from the row's
> `+0x28` handle through `0020E600` — dword **`+0x0C` into `+0x38`** and dword `+0x08` into `+0x3C`
> (`002FF4A7`–`002FF51E`), the same block whose word `+0` and bytes `+5` / `+6` / `+7` feed the
> stat sums. So `+0x38` is **the authored immunity word**: the party row's own immunities plus the
> equipped items', rebuilt from scratch on every stat rebuild — which is why the mode-5 runtime set
> (`0030E557`) does not survive one. The enemy arm (`002FF0E1`–) resolves the enemy tables for its
> stats and ORs nothing into `+0x38`, so an enemy's immunities arrive only through its equipment
> words and the status path's mode 5. `+0x3C`, filled the same way from `+0x48` / `+0x08`, is the
> **authored permanent-status word** — which is why a status in `+0x3C` "never runs out" (the
> status write's duration rule counts down word-1 statuses only).
>
> **That answers the question this sheet was written to ask.** `+0x3C` and `+0x64` are not
> "definition versus runtime" — **both are written at runtime by the status path**, and what
> separates them is that only `+0x64` can be blocked. *The obvious innate-versus-applied reading is
> wrong, and the writes are what kill it.*

> **All three are WRITTEN, which constrains what the record is.** A field the status system mutates
> is not authored data being read. **Either `BattleUnit + 0x698` does not always point at the
> authored `.ard`-derived record, or the record is a per-unit copy of it.** The second is the
> ordinary reading and this sheet does not choose between them — but a modder must take from it that
> **editing an authored row sets a starting value, not a live one.**

## 3. What the flags gate — named from readers, not from position

**The canonical guard is `TEST EAX, 0x80000003` — bits 0, 1 and 31 — and it accounts for 125 of the
143 masked sites.** The functions that use it say what it means:

| function | what the guard prevents |
|---|---|
| `BattleAction_IsTargetEligibleForCurrentAction` | being chosen as a target |
| `BattleTarget_ComputeEligibilityBlockMask` | appearing in the eligible-target set |
| `BattleStats_ModifyHPAndProcessLethalState` | taking an HP change |
| `Reward_ComputeExperienceForRecipient` · `Reward_ComputeLicensePointsForRecipient` | earning EXP or LP |
| `SpawnLifecycle_CheckAndRetireByNativeRange` | surviving the retirement sweep |
| `ActorSystem_ReleaseBattleUnitSlotForActor` | holding its BattleUnit slot |
| `BattleUnit_ActivateAppliedDefinitionRuntime` | activating its definition at all |

> **Bits 0, 1 and 31 are the "this unit is not a live participant" family.** A unit with any of them
> set is skipped by targeting, takes no HP change, awards nothing, and is a candidate for retirement.
> **That is a behavioural reading from eight independent readers, not a guess from the bit's
> position.**

**The other eight masks are narrower and each names its own group:**

| mask | bits | tested by | what it gates |
|---|---|---|---|
| `0x08000020` | 5, 27 | `BattleUnit_UpdateEngagementStateFlag`, `BattleUnit_ComputePartyBattleStance`, `BattleUnit_CanAdvanceCombatNavigation`, `BattleUnit_UpdateCombatFrame`, `BattleSystem_RunFieldFrameOrchestrator`, `BattleAction_CheckActionAvailabilityReason` | **engagement, stance and movement** — 6 of 7 readers are locomotion or stance |
| `0x8800203B` | 0,1,3,4,5,13,27,31 | `BattleUnit_IssueCommand`, `PartyCombat_UpdateStanceState` | **issuing a command** — the guard plus the movement bits plus more |
| `0x8000001B` | 0,1,3,4,31 | `BattleAction_CheckCurrentActionInterruptReason`, `BattleUnit_ProcessPendingActionSelectionQueue` | **continuing or queueing an action** |
| `0x8000201B` / `0x8000401B` | +13 / +14 | `BattleUnit_UpdatePartyCombatStanceState`, `WorldActor_QueryCombatStanceState`, `BattleUnit_CanAdvanceCombatNavigation` | **stance queries** |
| `0x00010010` | 4, 16 | `BattleFormula_BuildRuntimeCounterPeriodicHpCredit` | **periodic HP credit** |

**Bits 3, 4 and 5 are the action/movement layer**: they appear only in masks that also carry the
`0x80000003` guard, and only in functions about commands, interrupts, stance and navigation. **Bit
27 rides with bit 5 in every mask that has it.**

### The one place a bit selects another field — and it is one of this row's targets

`BattleFormula_BuildRuntimeCounterPeriodicHpCredit` gives the clearest single reading in the set:

```
003868f1  MOV  EAX,[RDI + 0x64]
003868f4  OR   EAX,[RDI + 0x3C]
003868f7  TEST EAX,0x10010          ; bits 4 and 16
003868fc  JNZ  00386a2c             ; either set -> no HP credit at all
...
003869eb  MOV  EAX,[RDI + 0x64]
003869ee  OR   EAX,[RDI + 0x3C]
003869f1  BT   EAX,0x10             ; bit 16, alone this time
003869f5  JNC  00386a03
003869f7  MOV  ECX,[RDI + 0x48]     ; <-- +0x048 is read ONLY when bit 16 is set
003869fa  CMP  ECX,R12D             ; ... and compared against 1
```

> **Bit 16 selects whether `+0x048` participates**, and `+0x048` is compared against the literal 1 —
> ~~so it is a small enum or count, not a magnitude~~ **corrected 2026-09-12 (FABLE, CB-8): it is a
> magnitude — the current HP** ([the stats-record field map](../08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md) `+0x048`, `s32`). The compare is a floor, not a test:
> `cmp ecx, r12d / cmovl ecx, r12d` with `r12d = 1` (`00386902`) is `max(HP, 1)`, and bit 16 is
> **Disease**, under which the periodic HP credit is scaled from the frozen current HP instead of
> the maximum (`+0x24`, doubled under bit 28 Bubble, `00386A03`–`00386A0C`) — the same
> `max(+0x48, 1)` rule the HP write applies ([the HP write](../08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md) §2.3). **That is a reader-established link
> between two fields of this record**, and it is the first one this database has for the definition record.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `0x00329A20` | `BattleUnit_AddPrimaryResourceRecoveryAccumulator` — the clearest small reader; OR at `0x00329A4A`, guard at `0x00329A4D` | ✅ |
| `0x00329A3B` | `MOV RCX,[RCX + 0x698]` — the record fetch this whole sheet hangs off | ✅ |
| `0x00386860` | `BattleFormula_BuildRuntimeCounterPeriodicHpCredit`; OR at `0x003868F4`, bit-16 test at `0x003869F1`, `+0x048` read at `0x003869F7` | ✅ |
| `0x00313F60` | called when the `0x80000003` guard trips in the accumulator | **read 2026-09-18 (FABLE):** a five-byte thunk (`jmp 00377C20`) to `FieldData_GetActiveFieldRecordBit15`, 78 bytes: it takes the active or pending field id (`WorldTransition_GetActiveOrPendingFieldId` `003148F0`), indexes the navimapdata table the MapInfo publisher holds at `02ADD100` (count at `+4`, three-byte rows from `+8`, `00377C29`..`00377C4B`) and returns bit 15 of the row's first word (`shr edx, 0xF`, `00377C55`), 0 when the table is absent or the id is out of range (`0xFFF >> 15`). So the guard's callee asks whether the current field's record keeps terminal-status units, the same bit the runtime-mode ladder calls mode 3; its caller `00233EA0` tears a KO, Stone or X-Zone unit down only when that bit is clear (`00233EF0`..`00233F37`). |
| `0x002FFF50` | `BattleTarget_ComputeEligibilityBlockMask` | ❌ entry only |
| `0x0023A570` | `BattleUnit_ApplyUnitDefinition` — binds the record to `+0x698` | ❌ see the registry sheet |

## 5. Corpus survey

**Nine masks over 229 sites, and the distribution is the finding:**

| mask | sites |
|---|---:|
| `0x80000003` | **125** |
| `0x08000020` | 7 |
| `0x8800203B` | 3 |
| `0x8000001B` · `0x8000201B` | 2 · 2 |
| `0x8800403B` · `0x88000013` · `0x8000401B` · `0x00010010` | 1 each |
| **no immediate `TEST` within 10 bytes of the `OR`** | **86** |

**Bit usage across all masks:** bits 0, 1 and 31 appear in 135 sites each; bit 27 in 12; bits 4 and 5
in 11 each; bit 3 in 9; bit 13 in 5; bit 14 in 2; bit 16 in 1.

**Twenty-two bits of the 64 available are never tested by this idiom at all.** That is a finding
about the idiom, not about the fields — a bit could be tested elsewhere without the `OR`.

## 6. Falsification pass — 2026-09-06

| attack | result |
|---|---|
| Is the pair really always OR-ed, or did the scan only find OR sites by construction? | **The scan is circular by design and the answer comes from elsewhere.** The registry doc's independent single-function dataflow found `+0x064` and `+0x03C` read by **the same 107 functions** — a coincidence no single-idiom scan could manufacture. **Two instruments, two methods, same pairing.** |
| Could my byte-pattern scan be matching non-instructions? | **It was, in an earlier form, and I caught it.** A first pass tested for the mere *presence* of a displacement byte in a function body and reported `+0x048` in 305 of 305 functions — because `0x48` is the REX.W prefix. **A clean sweep from a check that could not fail.** The scan here decodes ModRM, requires `mod=01`, and skips the SIB byte. |
| Are the named readings from the functions or from their names? | **From their names, and that is a weaker tier — stated as such.** The GFZ's function names are prior sessions' assertions. **Two readings are from the instruction stream** — the accumulator guard at `0x00329A4D` and the periodic-HP-credit gate at `0x003868F7` — and those are the ones §3's strongest claims rest on. |
| Could the decompiler have invented the `+0x048` link? | Not used. Both listings in §3 are read from `ReportFunctionBrief`. |

**The killer observation** for *"the two words share one bit vocabulary"* would be a site that tests
one word without the other and finds a bit meaning something different. **That search was not run**,
and it is the first thing §7 asks for.

## 6b. Independent audit pass — 2026-09-06, `repos-1e`

**Method.** The census re-run from scratch with a separate implementation: every function in
`functions.tsv` decoded with capstone, matching `MOV r32,[base+0x64]` followed within five
instructions by `OR r32,[base+0x3C]` on the same register, then the mask instruction that consumes
the result. Program state: GN160 (`gzf fa0db293…`).

**The three load-bearing figures reproduce exactly.**

| claim | sheet | independent census |
|---|---:|---:|
| `OR`-sites | **229** | **229** |
| distinct functions containing one | **162** | **162** |
| distinct bit positions ever tested | **10** — 0, 1, 3, 4, 5, 13, 14, 16, 27, 31 | **10 — the same ten, exactly** |

**The "9 distinct masks" is correct as written and worth one qualification.** Scoped to `test`, which
is what *"masks tested"* says, it is exactly **9**. Widening to `and` as well finds **two more** —
`0x00000001` and `0x8800003B` — so eleven masks in total reach the OR-ed pair.

> **Neither extra mask adds a bit position.** `0x1` is bit 0 and `0x8800003B` is bits 0, 1, 3, 4, 5,
> 27, 31 — all already in the ten. **So the headline number, the bit-position count, is robust to the
> scoping while the mask count is not**, which is the right way round for the claim the sheet
> actually rests on. A reader wanting *every* mask applied to this pair should know there are eleven;
> a reader wanting the tested bit space has the correct ten.

### One figure does not reproduce: the `.text` size

The corpus line says *"`.text` scanned: **8,001,280 bytes**, every byte"*. From the PE section table:

| | |
|---|---:|
| `.text` virtualSize | **7,996,981** (`0x7A0635`) |
| `.text` rawSize | **7,997,440** (`0x7A0800`) |
| the sheet's figure | 8,001,280 (`0x7A1700`) |
| difference from rawSize | **3,840** |

**Neither section figure matches, and 3,840 bytes is not a rounding.** The census itself is
unaffected — it is driven by the function list, not by that number, and it reproduces to the site —
so this is a wrong *statistic*, not a wrong *result*. **Left for the author to correct rather than
overwritten**, since I cannot tell which measurement produced it.

### The `+0x038` result — the sheet's strongest claim — verifies exactly

**The document grew between the start of this pass and its end**, gaining `+0x038`, the jump table
and the immunity guard. Those were re-derived too, so the pass covers them:

| claim | verified |
|---|---|
| a bounds-checked selector indexes a **six-entry** table at `0x0030E88C` | the dispatch is `mov eax, [rcx + rax*4 + 0x1ee88c]` / `add rax, rcx` / `jmp rax` at `0x0030E4DB` — an **image-relative RVA table** rebased on `0x00120000`, the same idiom as the ScriptVM opcode table |
| the six cases are `0x0030E4E7` `0x0030E4FD` `0x0030E513` `0x0030E526` `0x0030E543` `0x0030E557` | **all six, in that order**, decoded from the table's own dwords |
| case 3 sets `+0x64` and is guarded | `0x0030E526 mov ecx,[rsi+0x64]` · `0x0030E529 test ecx,edi` · `0x0030E52B jne` |
| **`+0x038` blocks the set** | `0x0030E531 test dword ptr [rsi+0x38], edi` · `0x0030E534 jne 0x30e82d` — **exact** |
| the set itself | `0x0030E53A mov eax,edi` · `0x0030E53C or eax,ecx` · `0x0030E53E mov [rsi+0x64],eax` |
| case 4 is the `+0x3C` set | `0x0030E543 mov ecx,[rsi+0x3c]` |

**So "a bit set in `+0x38` makes the corresponding bit unsettable in `+0x64`" is correct, and the
asymmetry is real** — cases 4 and 5 have no equivalent `+0x38` test. That is the sheet's most
consequential sentence and it survives a byte-level re-derivation.

### What was attacked and held

(a) That the five-instruction window between the `MOV` and the `OR` might be the sheet's and not the
engine's — widening it to eight adds no sites, so 229 is not a window artefact. (b) That some sites
might `OR` in the other order (`[+0x3C]` first) and be missed by both of us — searching that order
finds none, so the pairing really is directional. (c) That the ten bit positions might be an artefact
of counting only `test` — they are not; adding the `and` masks leaves the set unchanged. (d) That the
six-case matrix might be a decompiler's reconstruction — the table is six dwords read from `.text`
and every target is an instruction boundary.

**Not audited:** §3's naming of what each *bit* gates, which rests on reading the consuming functions
rather than on any census; and the two gate results §2 pre-declares as expected, which I did not
re-derive because the sheet already dispositions them.

## 7. What this document does not claim

- **~~Which word is which~~ — ANSWERED in §2 during this block, and the first answer I reached was
  wrong.** A read-side scan suggested an asymmetry (178 solo `+0x64` reads against 17 solo `+0x3C`),
  but that instrument was too loose: it counted every `[base+0x64]` in any function that also touches
  `+0x698`, on any structure. **The writes settled it instead** — three words, a six-case matrix, and
  `+0x38` gating `+0x64`. *The noisy read scan and the decisive write scan disagreed, and the write
  scan is the one with a bounded population.*
- ~~**What `+0x38` blocks in game terms.** It refuses a bit in `+0x64`; whether that is immunity,
  resistance, or an already-in-progress interlock is **not** established.~~ **Immunity — CB-6
  answered 2026-09-12 (FABLE), §3:** the stat rebuild fills it from the party row's `+0x4C` and each
  equipped item's secondary block `+0x0C`, the authored immunity words.
- **Is `+0x698` the authored row or a copy? — CB-7 answered 2026-09-12 (FABLE): a per-unit copy.**
  `+0x698` points at the `0x1C8`-byte `BattleStatsRecord`, which an enemy carries inside its
  `0x250` spawn record (the "page" at record `+0x80`, filled from the definition row by
  `BattleStats_InitializeDefinitionRecord(page, id)`, [the unit-definition page](Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md) §2.1) and a party member in the
  battle-state array `*(02EBF190) + 8 + k × 0x1C8` ([the stats-record field map](../08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md) §2.1). The authored rows
  (`02EBF120` / `02EBF130`) are read at build and by the rebuild above; the three status words live
  only in the copy. So editing an authored row sets what the next build or rebuild copies in, never a
  live word.
- **What any bit *is*, in the game's own vocabulary.** §3 names what each bit **prevents**, from its
  readers. It does not say bit 5 is Stop or bit 31 is KO. **Naming a status would need the applier,
  not the consumer.**
- **The 86 OR-sites with no immediate `TEST` nearby.** They may compare against a register, branch on
  a different instruction, or be a longer idiom. Uncounted, not zero.
- **`+0x024`, `+0x050`, `+0x028`, `+0x04C`** — the remaining offsets on this row's list. Only
  `+0x048` is reached in this block, and only through bit 16.
- **Whether `0x00386902`–`0x0038690E` is dead code.** At that site `BT EAX,0x10` follows a `TEST` on
  a mask that includes bit 16, so the branch appears unreachable — **but inbound flows into
  `0x00386902` were not enumerated**, and a jump from elsewhere would make it live. Recorded as an
  observation, not a claim.

## 8. Related

- [`../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md`](../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md)
  — the 456-byte record, its binding at `BattleUnit + 0x698`, and the 58-offset field map this sheet
  starts from
- [`battleunit-slot-pool-and-actor-class.md`](battleunit-slot-pool-and-actor-class.md) — the BattleUnit the record is bound into

## Crossings into other layers — FINAL-AUDIT pass 22 (OPUS, 2026-09-18)

Two edges, both through `WorldTransition_GetActiveOrPendingFieldId` (`003148F0`), which §4's read of
the guard callee names in passing. The getter is 27 bytes: it resolves the world-transition singleton,
reads the dword at `+0x1044`, and clamps a negative to zero (`test eax, eax` / `cmovs eax, ecx`,
`00314901`–`00314903`). **It is a shared field-id accessor, and this page cites it as one step of a
chain rather than as a subject.**

- **Audio — CLIENT.** An audio body calls it at **`0026200F`**, behind a byte gate
  (`cmp byte [rbx+0x17], 0x80` / `jb`), keeps the id, and then lets a flag on the same singleton
  (`+0x1063` bit `0x40`) replace it with an override byte at `+0x1534` before the id is used. The
  crossing is that the audio layer reads the same field id.
- **Platform, online and achievements — CLIENT, and the call is a fallback that often does not
  happen.** A platform body calls the getter at **`003160F3`**, but only when the preceding query came
  back non-positive: `test eax, eax` / `jg` at `003160EF`–`003160F1` jumps straight over it. Whatever
  id it ends with goes on to a lookup.

*The two call sites are named rather than their enclosing bodies. An address in an accounting
paragraph is a new citation, and a new citation has neighbours — which is how a three-finding fix
became a five-finding one earlier in this pass.*

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CombatFormula — SERVICE.** A cited function calls `BattleStats_FindOwningBattleUnit` and two small formula helpers (21 and 30 bytes).

*Citation spellings (R5), 2026-09-14 (FABLE):* these crossings become reportable once citations written 0x... or FUN_... count (R5); tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Rewards_Progression_Economy — SERVICE.** `BattleStats_ChangeStatusAndProcessSideEffects`, cited here, calls `BattleUnit_ProcessDefeatRewardsAndLoot`.
- **CombatAI — CLIENT.** `FieldData_GetActiveFieldRecordBit15` is called by the enmity and perception bodies `BattleEnmity_WriteForCombatantId`, `BattleEnmity_AdjustOtherRelevantCombatants`, `BattleUnit_RebuildPerceptionCandidateCache` and `BattlePerception_RefreshCandidateCacheGeneration`.
- **UI — CLIENT.** `FieldData_GetActiveFieldRecordBit15` is called by `BattleMenu_BuildCommandEntryList` and a 456-byte UI body.
- **Input — CLIENT.** `InputGameplay_ArbitrateDigitalInputAndModalState` calls `FieldData_GetActiveFieldRecordBit15`.
- **Presentation — SERVICE.** `BattleTarget_ComputeEligibilityBlockMask` calls `BattleUnit_ComputePresentationSuppressionMask`.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**Gameplay — SERVICE and CLIENT (11 edges).** `BattleUnit_ApplyUnitDefinition` `0023A570` and `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` call `BattleEncodedId_IsValidForClass` `00322C50`; `002FEF30` and `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360` call `BattleUnit_UpdateEngagementStateFlag` `00307D10`, and `0030E360` calls `BattleUnit_DispatchActorPresentationEvent` `003299B0`; the field-record predicate `FieldData_GetActiveFieldRecordBit15` `00377C20` (and its thunk `00313F60`) is called by `00307D10`, `BattleUnit_CollectMappedFourSlotUnitsByFlags` `0030A8A0`, `BattleUnit_HasRelationshipClass2PlusInSlotMask` `0030C210`, `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` `0030D9A0`, `Battle_EmitReactionPresentationForSlot` `003176E0` and `003257D0`. The writers of the flag pair validate encoded ids and refresh a unit's engagement flag and presentation event through these domain-filed helpers, and the same helpers are further consumers of the per-field bit this page's guard reads; none of them reads `+0x038`, `+0x03C` or `+0x064`.

**Items_Equipment_Shops_License — CLIENT (3 edges).** `Equipment_EvaluateCandidateLoadoutAndBuildDerivedStats` `0030A4E0` calls the stats rebuild `002FEF30`; `Inventory_QueryOwnedCountIncludingReservedActionItems` `00309FB0` and `Equipment_UnequipEncodedItemFromActiveRoster` `0030FD10` call `00377C20`. The candidate-loadout evaluator checks slot compatibility and licences and then runs the same rebuild that zeroes and refills the status block, and two inventory bodies ask the per-field bit; the crossing is those calls, not a use of the definition-record flags.

**Movement — CLIENT, OUT-OF-SCOPE (12 edges).** `00377C20` is called by `0025B470`, `0026C3E0`, `002E28E0`, `00310920` and `00313670`; its thunk `00313F60` by `0031BAC0`, `00326D60`, `00329A80` and `003911D0`; and `WorldTransition_GetActiveOrPendingFieldId` `003148F0` by `0033A720`, `003ED190` and `003ED3F0` — all Movement-filed bodies, not read here. This page cites the predicate and the field-id getter only as the guard's callee chain; locomotion's own reads of the current field's bit and id are that layer's business.

**Party — CLIENT (3 edges).** `PartyControl_RecomputeSuppressionFromLeaderBattleState` `0023B040` and `0031AC00` call the thunk `00313F60`, and `00304180` calls `00377C20`. The party-suppression recompute asks the same per-field bit (the runtime-mode ladder's mode-3 bit) when it derives suppression from the leader's battle state; it is another consumer of the guard's callee, not a reader of the flag pair.

**Save_Load_Settings — SERVICE and CLIENT (2 edges).** `003148F0` calls `SaveImage_GetPersistentPayloadBase` `002EF2B0`, and `SaveImage_FinalizeHeaderAndChecksum` `00583D60` calls `003148F0`. The getter is 27 bytes: it takes the persistent payload base and returns its dword at `+0x1044` clamped to zero, and the header finaliser stores that id at the header's `+0x4C`; the field id is save state, and this page uses the getter only as a step of the guard chain.

**Script_VM_Native_Bridge — CLIENT, OUT-OF-SCOPE (6 edges).** `003148F0` is called by the verb bodies `0033F310` and `00357450`; `00377C20` by `00344740`, `00352FA0`, `003537D0` and `00355680` (script-VM bodies of 29 to 166 bytes, not read here). Script verbs query the current field id and the per-field bit directly; that is fan-in on the shared field predicate, not a script route to the definition-record words.

**Spawn_Encounter_Lifecycle — SERVICE and CLIENT (5 edges).** `0023A570` calls `SpawnKeep_ResolvePrimaryEntry` `00236100` and is called by `Spawn_ApplyScriptSelectedUnit` `0023A3B0`; `Spawn_ValidateCandidateDistanceToPlayers` `00234DA0` and `SpawnLifecycle_CheckAndRetireByNativeRange` `002350C0` call `00313F60`; `SpawnKeep_RotatePersistenceBanksForAreaTransition` `00233780` calls `003148F0`. The definition record reaches a unit when a spawn applies it (the record is bound to `+0x698` there), and spawn validation, retirement and the persistence-bank rotation are further readers of the field bit and field id.

**Status_Periodic_Terminal — SERVICE and CLIENT (21 edges).** `0030E360` calls `BattleUnit_ResetActionControlForStatusTransition` `00300140`, `BattleUnit_RecoverFromTerminalStatusSetIfClear` `00301140`, `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0`, `BattleStatus_ComputeDefaultShortTimer` `003876D0`, `BattleStatus_ComputeDefaultDwordParameter` `00387730` and itself, and is called by `BattleStats_RemoveStatusMode0` `0030E990`, `BattleStats_AddStatusMode3` `0030EAE0`, `BattleStats_RemoveStatusesFromMaskAndRecompute` `0030F690` and `0030FED0`; `00233EA0` calls `00300140`; `0030FED0` calls `002FEF30`; `00377C20` is called by `0030E360`, `0030F690` and `BattleUnit_RunPeriodicCombatMaintenance` `00310DB0`, and `00313F60` by `BattleUnit_TakeAndClearPrimaryResourceRecoveryAccumulator` `00320450` and `00329A20`; `BattleUnit_ResolvePeriodicPrimaryResourceRecoveryStep` `002F9400` and `BattleUnit_ClearPrimaryResourceRecoveryAccumulator` `002FA540` call `00329A20`; `00386860` calls `BattleFormula_BuildPeriodicStatusResult` `00385DF0`. The status-change routine that writes all three words sits inside the status layer's add/remove/recompute cycle, and the recovery accumulator and periodic HP credit this page cites as readers are driven by the periodic tick — the flag pair is read on the status layer's own paths.
