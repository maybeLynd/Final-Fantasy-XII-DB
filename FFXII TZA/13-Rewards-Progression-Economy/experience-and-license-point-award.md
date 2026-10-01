---
system: Experience and License Point award
category: 13-Rewards-Progression-Economy
status: PARTIAL — SECTION-03 independent peer acceptance pending (GR-16); reward-row binding lifetime (GR-17) and edge-state reachability (GR-18) open; player view, evidence table and Related added 2026-09-30 (FABLE)
owner_layer: PrimaryOwner:Rewards_Progression_Economy
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: "snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30"
    verified: "re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS"
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-22
audit:
  passes: 1
  last_pass: 2026-09-02
  last_pass_state: falsification-pass
  crossref_clean: false
  reopened_count: 0
production_review:
  section: SECTION-03
  status: locally validated; peer acceptance pending
  scope: original reward consumers, selected caller instructions and retained binding observations
  new_live_session: false

---

# Experience and License Point award

> **SECTION-03 production review, 2026-09-22; independent peer acceptance pending** (registered as GR-16, 2026-09-30).
> Corrected against original EXE instructions, 71 bounded native controls and independent review
> of four retained EXP-081 samples. The historical audit/provenance metadata below/above is not
> a new audit pass. No new live game session or complete defeat-orchestrator execution was performed.
> [Evidence, changed claims and limitations](../_experiments/evidence/continuation-section03-reward-bindings/REVIEW.md).

**Current scope:** original EXP/LP gates and arithmetic are resolved at the bounded consumer level.
Actual retained reward-table contents, producer lifetime and complete in-game payout remain outside
this review. The authoritative detailed interface is the [award contract](CONTRACT-experience-and-licence-award.md).

## 1. What the player sees (FABLE, 2026-09-30)

*(Section added 2026-09-30 (FABLE); the technical summary that used to be §1 follows as §1a.)*

After each kill, every eligible party member gains experience and license points. Experience is **shared**: the
kill's experience is divided evenly, rounding down, among the members who count, which is up to four fighters.
Espers and the chocobo do not count, nor does anyone KO'd, so a smaller party earns more per head. While an Esper is
summoned, the summoner receives the whole amount and no one else receives any. The number the game shows for the
kill is that per-member share, not the total.

License points are **not shared**: every eligible member receives the full amount. Guests earn both. A summoned
Esper earns neither.

Three accessories change what their wearer receives. The Embroidered Tippet doubles experience, the Golden Amulet
doubles license points, and the Firefly reduces experience to zero; with both the Tippet and the Firefly on, the
Firefly wins. Statuses such as Berserk, Bubble or HP Critical change nothing, because the award reads the
equipment effects, not the statuses (§9). What else happens at the kill (gil, levels, the loot, the Cat-ear Hood's
conversion of license points into gil, and New Game Minus) is on
[what happens when an enemy dies](what-happens-when-an-enemy-dies.md).

## 1a. What the computers return (FABLE, 2026-09-30)

These functions **recompute on each call**; they do not store progression. In the shared EXP
branch, the base amount is divided by the passing count among **exactly four lookup slots**.
The caller may iterate a larger candidate list, but it does not turn this divisor into a fifth-slot
loop. Integer remainders are discarded. Recipient-specific doubling/zeroing can change the total,
so total distributed EXP is not invariant under party changes.

LP uses an independent gate and returns its row-derived amount without this divisor. In particular,
**a NULL recipient is accepted by both computers**. NULL does not force the undivided EXP branch.

## 2. Native mechanism

### EXP and LP share some conditions, not their entire gate

| Condition | EXP `002F8BB0` | LP `002F90C0` |
|---|---|---|
| NULL recipient | Accepted; recipient checks/modifiers skipped | Accepted after the global LP gate |
| Nonnull recipient kind | Must be 0 | Must be 0 |
| Recipient identity | Excludes `0x1B..0x27` (`002F8BF2`–`002F8BFA`); owning-unit lookup must succeed (`002F8BDE`–`002F8BE6`) | Admits `0..6`, `0x1A`, `>=0x28` (`002F90E7`–`002F90F5`); no owning-unit lookup |
| Recipient status | `(u32[+0x3C] OR u32[+0x64]) & 0x80000003` must be zero | Same mask (`002F90F7`–`002F90FD`) |
| Subject | Nonnull unit, nonnull stats at `+0x698`, stats kind 1 | Same |
| Additional gate | Current mode chooses shared vs designated EXP | Signed byte `0209A2A9` gate, before pointer reads |
| Division | Shared branch only, including NULL-recipient calls | None |

A synthetic ownerless kind-0 recipient returns EXP 0 but LP 19 under the same valid subject/row
fixture. The mask's equality with an action-side constant does **not** mean patching one code site
changes the other. Status words `+0x3C/+0x64` are also distinct from effect layers beginning at
`+0x68/+0x78`; see the [stats map](../08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md).

### Mode and membership

`003135C0` selects the designated-recipient EXP branch when nonzero. For a nonnull recipient the
resolved designated stats must equal the recipient. A NULL recipient skips that equality check.
Both calls still follow the current mode; NULL in shared mode still traverses the four member slots.
LP never calls the designated-mode or roster-divisor chain.

The ordinary member-byte lookup excludes kind-1 stats, and the filter excludes kind-0 ID `0x1A`
as well as `0x1B..0x27`. But "only kind 0 can ever count" is too strong: the `0xFF` selector
sentinel can select a `0xFFFF` stats identity when the descriptor admits it. One synthetic
original-code control establishes that exception, not shipped-game reachability of such a record.
The prior game-language interpretation (summoner/Esper/mount) is retained in the linked sources;
this update's native tests establish the numeric rules rather than recertifying all authored names.

## 3. Key addresses

| Address | Bounded role established here |
|---|---|
| `002F8BB0` | EXP computer, 430 original bytes; full original gate/lookup closure in native tests |
| `002F90C0` | LP computer, 179 original bytes; no owner lookup/division |
| `0031B860` | EXP recipient-to-unit finder |
| `003135C0` / `00313800` | Mode selection / designated-index lookup |
| `0031B810` / `002367A0` | Four-slot selector and original definition lookup |
| `00320AB0` | Designated mapped-stats resolver |
| `00312280` | Defeat caller; NULL argument, caps and presentation branch inspected statically |
| `0028FB80` | Presentation call boundary; no new rendering observation |

*Retained from the pre-SECTION-03 page (FABLE, Claude Opus 5.5, 2026-09-25; every address re-read against the image today).* The designated index is `00313800`: the battle-state byte `+0x5AD5` mapped through `00320890` (tail jump `0031380E`). `00320AB0(index, 1)` resolves it through `0031B9F0` (`00320AB4`) and returns `[base] + 8 + slot × 0x1C8` for slot ≤ `0x27`, else null (`00320AB9`–`00320AD9`). A nonnull recipient that is not that record takes `002F8C53 cmp rdi, rax` / `002F8C56 jne` to the zero return. HEAD read this mode as the Esper summon and the designated record as the summoner; the prose above leaves that naming to the linked sources, and this paragraph does not re-assert it. The other HEAD table rows: the gil pair `GameState_GetGil` `00253690` / `GameState_SetGil` `00254EE0` (the defeat path's gil award, the sixth invariant of the [defeat contract](CONTRACT-defeat-rewards-sequence.md) *(reworded 2026-09-30 (FABLE): the text cited that invariant by its contract label, which is not a register id and failed `documented_rule.py`'s unknown-id check)*); `0028FB80` calls `00289D00` twice, `r9d = 0` (`0028FBA7`) then `r9d = 1`, the EXP and LP presentation arms; and `LicenseData_BuildPrerequisiteNodeMaskForRequirement` `002F8FA0`, ~~not read here~~ *which is not part of the award (reconciled 2026-09-30 (FABLE)): its one direct caller is the licence prerequisite test, and it is read on [the licence-check page](../12-Items-Equipment-Shops-License/license-check-what-the-board-actually-tests.md).*

## 4. Data structures and formulas

Let `level = u8[subject.stats+0x1C2]`, `baseline = u8[subject.stats+0x88]`,
`baseRow = ptr[subject+0xE70]`, and `perLevelRow = ptr[subject+0xE78]`.

```text
rawEXP = signed32((level - baseline) * u32[perLevelRow+0x34] + u32[baseRow+0x34])
EXP = rawEXP                         in the designated branch
EXP = signed_trunc(rawEXP / n)       in the shared branch, n > 0
EXP = 0                             in the shared branch, n == 0
rawLP = (level - baseline) * u8[perLevelRow+0x2F] + u8[baseRow+0x2F]
```

EXP arithmetic wraps at 32-bit machine width before signed division. Negative division truncates
toward zero. LP coefficient loads are unsigned bytes. The consumers read the **current baseline**;
a cited initializer supplying 1 is not an invariant enforced by either reward computer. That initializer is the enemy branch of `BattleStats_InitializeDefinitionRecord`: `0023AD37` sets `edx = 1`, it reaches `r8d` at `0023AD8B`, and the grower stores it at `+0x88` (`0030C4B1`) *(address restored 2026-09-25, FABLE, Claude Opus 5.5)*.

For nonnull recipients, either effect-bank byte `+0x6B/+0x7B` bit `0x08` doubles EXP; bit `0x20`
then zeros it. LP doubles on bit `0x10` and has no corresponding zero-bit branch. NULL skips all
these recipient modifiers. *(Anchors added 2026-09-30 (FABLE): EXP `002F8D21`–`002F8D24` (NULL skip), `002F8D26`–`002F8D34`
(double), `002F8D36`–`002F8D40` (zero, tested after the doubling); LP `002F9146`–`002F9149` (NULL skip),
`002F914B`–`002F9157` (double). In layer-bit terms, `+0x6B` bits 3 / 4 / 5 are effect ids 27 / 28 / 29, §9.)*
Reached reward rows are dereferenced without row-null checks; earlier
rejections can avoid them, so not every call with null rows faults.

## 5. Call chain and presentation

```text
defeat caller
  -> per candidate: EXP and LP computers -> caller clamps/writes progression
  -> EXP(NULL, subject) -> still mode-dependent, divided in shared mode
  -> LP(NULL, subject)  -> unmodified and undivided by this computer
  -> separate caps and field-flag EXP suppression -> presentation call
```

For raw EXP/LP 19 with two passing members, the computers return `EXP(NULL)=9`, `LP(NULL)=19`.
An EXP-doubled recipient gets 18; NULL gets 9, not 19. With the designated mode selected,
`EXP(NULL)=19`. These are native synthetic calls plus statically checked caller arguments, **not
new observed floating numbers in the game**. See the [defeat contract](CONTRACT-defeat-rewards-sequence.md).

## 6. Retained reward bindings and modding boundaries

Independent review of EXP-081 validates 88 retained spans in four samples. The two field samples
have matching reward registry words and three stable pairs of unit reward pointers. Their spacing
is consistent with a `0x38` stride and `descriptor+0x20` index-zero address, but **neither the
reward headers nor required row prefixes were captured**. No actual XP/LP coefficient, drop,
award, or row lifetime can be derived from those missing bytes.

The enemy stats records in that observation are embedded working records, not authored definition
rows. Modifying one should not be confused with editing the other's reward row. The producer's
pointer construction and consumers' field accesses are separately verified original-code facts.

For original-game edits, keep the EXP/LP gates distinct, preserve signed arithmetic and effect-bank
order, and do not add a null-recipient division bypass. A multiplayer authority must likewise
specify which observed mode and member state feed each computation; these consumers take no atomic
snapshot of the entire party. No network implementation is part of this update.

## 7. What is not known

- [x] ~~The full payout arithmetic — several operands unresolved.~~ **N-1 ANSWERED 2026-09-12
      (FABLE):** one expression on both paths (§9), `+0x88` the current baseline byte (the cited initializer path supplies 1), the divisor the four slot-map members minus Espers and the Chocobo, the
      undivided path the Esper summon's summoner (§2).
- [x] ~~What triggers the **×2** bonus and what triggers the **zero** case.~~ **N-2 ANSWERED
      2026-09-12 (FABLE):** effect ids 27 / 28 / 29 in either layer — *Doubles EXP earned*, *Doubles
      license points earned*, *Reduces EXP earned to 0* by the shipped help texts — granted by the
      Embroidered Tippet, the Golden Amulet and the Firefly (§9).
- [x] ~~Whether `+0x3C`/`+0x64` here are the same layers as BKBI `+0x68`/`+0x78`, or a different
      structure.~~ **N-3 ANSWERED 2026-09-12 (FABLE):** the reward gate and the action gate read
      **literally the same two `u32` status words** of the stats record (`+0x3C | +0x64`); `+0x68`
      / `+0x78` are the 16-byte effect layers, a different pair the formula merge reads (§2).
- [x] ~~Meaning of `recipient[5]` and the `recipient[4] - 0x1B > 0x0C` range test.~~ **N-4 ANSWERED
      2026-09-11:** `recipient[5]` is the definition table (0 party, 1 enemy) and `recipient[4]` the row
      in it, so for a nonnull recipient EXP first requires kind 0 and an owner, then excludes rows `27`–`39` — **the thirteen
      Espers** ([the kind page](../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md) AL-2,
      decoded from the party table's name references). A summoned Esper earns no EXP or LP; a guest does.
- [x] ~~What `wDefinitionSelector[+1] == 1` selects — which foes award anything at all. **N-5.**~~
      **ANSWERED 2026-09-12 (FABLE) by cross-reference:** `wDefinitionSelector` is the stats
      record's `u16` at `+4` — the unit's definition id — and its high byte `+5` is the **kind byte**:
      `1` = the unit was built by the **enemy path** from the enemy definition table `02EBF120`,
      `0` = the party path from `02EBF130` ([the unit-definition page](../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md) §2.1, `0023A626`–`0023A641`). So "foes that
      award anything" are exactly the units built from the enemy table; the recipient side tests
      the same byte for `0` (`002F90E2`) and a party type byte `+4` of `≤ 6`, `0x1A` or `≥ 0x28`
      (`002F90E7`–`002F90F5`).
- [x] ~~Which party member `BattleStats_GetByMappedBattleSlot(slot, 1)` distinguishes.~~ **N-6
      ANSWERED 2026-09-12 (FABLE): the summoner** — the query runs only in mode 1 (an Esper summon),
      `00313800` maps the block's `+0x5AD5` to its party-configuration index, and the whole EXP base
      goes to that nonnull member while a different nonnull recipient gets 0; a NULL recipient
      bypasses only this comparison. LP has no corresponding mode branch (§2).
- [x] ~~Gil award — `GameState_Get/SetGil` are in the corpus but unread.~~ **N-7 ANSWERED
      2026-09-03** — see [`gil-storage-clamp-and-every-path-that-moves-it.md`](gil-storage-clamp-and-every-path-that-moves-it.md):
      one setter, 13 direct callers, 5 owners, and the clamp `[0, 99,999,999]` lives in the
      setter so every path inherits it.

*§8's residual, mirrored here with its dispositions 2026-09-30 (FABLE):*

- [x] **Section 03's independent peer acceptance** (**GR-16.**) The production review that §§1–8 rest on has the
      owner's review ([`section03-owner-review.md`](../_index/candidates/section03-owner-review.md)) and no auditor
      verdict. *(GR-16 answered 2026-10-01: SWE2-AUDIT-SEM's independent review `f41194772`, [record](../../_index/candidates/auditsem-review-section03-1001/REVIEW.md), ACCEPT-WITH-NARROWING; register restated by OPUS for SWE2-DATA.)*
- [x] **Reward-row binding lifetime** (**GR-17.**) A unit caches its two reward-row pointers once, at install
      (`+0xE70` / `+0xE78`; [the defeat contract](CONTRACT-defeat-rewards-sequence.md) §3). Whether the tables they
      point into can be rebound or released before that unit's defeat is not read. *(Answered 2026-09-30, SWE2-ORACLE for OPUS `3613e9cdb`; register row GR-17, records [`gr17-reward-table-lifetime-0930`](../_index/candidates/gr17-reward-table-lifetime-0930/README.md) and [`gr17-effect-residue-0930`](../_index/candidates/gr17-effect-residue-0930/README.md): along direct control flow there is no window. Only manager-0 actors own battle units, and every free of the reward tables is followed in the same call by manager 0's unload, whose whole-record memsets zero `+0xE70` / `+0xE78`; the one data-gated chain is closed by the shipped effect data. Indirect dispatch during teardown is not followed.)*
- [ ] **Reachability of the synthetic edge states** (**GR-18.**) *(narrowed 2026-09-30, OPUS `8fdc9abe5`, record [`gr18-reward-edge-reachability-0930`](../_index/candidates/gr18-reward-edge-reachability-0930/README.md): three of the four cannot occur with shipped data; the high relocation base stays open as a runtime fact - whether the `.ard` buffer can be placed at or above 4 GB)*: zero-count or missing reward descriptors, high
      relocation bases, level-zero rewards, and the `0xFF` selector matching a `0xFFFF` stats identity. Section 03
      executed each of them, but none is shown to occur in a shipped game.
- [x] **Retained reward header/row bytes** — **not a question about the game.** The shipped rows' contents are decoded
      statically on [how a unit is built](../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md)
      (base rows EXP 0–27,404, LP 0–255, gil 0–297; per-level rows LP 0 on every row). EXP-081 only failed to retain
      the bytes of the rows it bound.
- [x] **Full payout / event behaviour** — **read statically** on [what happens when an enemy dies](what-happens-when-an-enemy-dies.md):
      the whole defeat body, the caps, the level walk, gil, the achievement counters and the New Game Minus flag. No
      live payout was captured. The claims are tier-1 static, so a live capture would re-observe them; none is queued.


## 8. Evidence and remaining scope

[SECTION-03 review](../_experiments/evidence/continuation-section03-reward-bindings/REVIEW.md) pins 24 original bodies, independently reviews 88 retained spans,
and records 71 bounded native controls, six rejected code variants and ten corrupted-record
controls. The old retained checker also reproduces its preserved output and four historical
controls. No current Ghidra re-import, full EXP-090 campaign, fresh live session, or formal peer
acceptance is claimed.

**Still PARTIAL:** actual retained reward header/row bytes and lifetime, full payout/event behavior,
and initialized-game reachability of synthetic edge states are not supplied by these observations.
That is a real residual, not missing arithmetic placeholders. *(Dispositioned item by item in §7, 2026-09-30
(FABLE): lifetime is GR-17, reachability is GR-18, and the other two are answered or are not questions.)*

| Claim | Evidence | Tier |
|---|---|---:|
| EXP computer: gates, arithmetic, four-slot divisor, modes, modifiers | `002F8BB0` read whole; the claim table in [the function note](how-experience-is-computed-and-divided.md) | 1 |
| LP computer: global gate, identity ranges, byte rows, doubling on `0x10` | `002F90C0` read whole; `002F90D0`–`002F90D7`, `002F90E7`–`002F90F5`, `002F912B`–`002F9144`, `002F914B`–`002F9157` | 1 |
| the reward gate and the action gate read the same two status words | `002F8C00`–`002F8C0B`, `002F90F7`–`002F90FD` (N-3) | 1 |
| the designated index and its record | `00313800` (tail jump `0031380E`), `00320AB0` (`00320AB4`–`00320AD9`) | 1 |
| the baseline is whatever `+0x88` holds; the enemy initializer supplies 1 | `0023AD37`, `0023AD8B`, `0030C4B1` | 1 |
| numeric behaviour under synthetic states | SECTION-03's 71 native controls on the original instructions; six code mutants rejected | 1 (executed) |
| effect ids 27 / 28 / 29, their texts and their three accessories | augment rows 27–29, `listhelp_ability.bin` 130027–130029, the 557-row equipment census (§9) | 9 |
| retained EXP-081 bindings, with no row bytes captured | SECTION-03's independent reduction of 88 retained spans | 10 |

## 9. Historical shipped effect-name investigation (retained, not newly recertified)

The following 2026-09-12 asset/name research is preserved from the supplied source. SECTION-03
checks the consumer bits and widths, but does not rerun the full asset census or verify every name.

**In play**, these three bits are the machinery behind the game's EXP-doubling, LP-doubling and
no-EXP effects. ~~That correspondence is an **inference** from the arithmetic — nothing here names an
item~~ **Named 2026-09-12 (FABLE) from the shipped data.** Byte 3, bits 3 / 4 / 5 of a 128-bit
layer are **effect ids 27, 28 and 29**, and the augment table (`02EBF040`, rows 27–29, `nameId`
13027–13029) points them at `listhelp_ability.bin` strings 130027–130029: **27 *"Doubles EXP
earned"*, 28 *"Doubles license points earned"*, 29 *"Reduces EXP earned to ‹0›"*** (the last glyph,
`0x85`, lies outside the decoded letter/digit rows; the code writes 0; [the battle text banks](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md) §5.1 for the
resolver). **Who grants them:** the derived layer is rebuilt from the equipment table's augment byte
`+0x1A` on rows the rebuild's category gate admits (byte `+9` in 19–22, [the auto-status rebuild](../08-Combat-Formula/the-auto-status-rebuild.md)) — and over
all 557 shipped rows those are exactly **`0x1168` Embroidered Tippet (27), `0x116F` Golden Amulet
(28) and `0x1171` Firefly (29)**, all byte-9 = 21. Two more rows carry the byte values but not the
category (`0x105C` Ras Algethi, 29, byte-9 = 9; `0x10A6` Nightmare, 27, byte-9 = 2) and are not read
by the rebuild; ~~whether `+0x1A` means the same thing on a weapon row is not established~~ *it does not (answered
2026-09-30 (FABLE) by cross-reference): on a weapon row the byte is the equipment-comparison metric, which
`Equipment_ComputeComparisonMetricWithCompatiblePartner` reads at `002F7D28` and adds to the ammunition row's `+0x1A`
for a ranged weapon ([item ids and equipment compatibility](../12-Items-Equipment-Shops-License/item-id-encoding-and-equipment-compatibility.md))*. No
category-15 licence node carries any of the three (their id set is 5, 8, 9, 10, 11, 20, 21, 23, 30,
86, 103), and the mutable layer's authored feeders — the result record's `+0x3C` / `+0x3D` and the
direct-state orders, whose ids are a five-bit parameter plus `0x2E` or `0x6E` — cannot name 27–29
either. **The status-namespace aliases do not fire here:** this function reads the *layers*
(`+0x6B` / `+0x7B`), not the status words `+0x3C` / `+0x64` that Berserk (27), Bubble (28) and
HP Critical (29) live in, so — unlike the formula context, which ORs the words in
(`00384808`–`00384818`, [the two-layer model](../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md)) — a Berserk recipient earns no bonus and an HP-Critical one
loses nothing. ~~Live confirmation queued: a Berserk / Bubble / HP-Critical member without the
accessory should show unchanged EXP and LP.~~ *Corrected 2026-09-30 (FABLE): no live check is queued. No experiment
and no ASTRA-QUEUE item names it, and none is needed: the claim is tier-1 static, since `002F8D26`–`002F8D3E` and
`002F914B`–`002F9155` read only the layer bytes `+0x6B` / `+0x7B`, never `+0x3C` / `+0x64`. A live run with such a
member would re-observe that reading, not settle anything.*


### Prior conclusion corrected in SECTION-03

The old page said "nothing was contradicted" while retaining an incorrect nonnull gate, shared
EXP/LP ownership test, universal undivided-display inference and constant-total claim. Those
conclusions are superseded by §§1–8 and the canonical contract. The historical audit count is
preserved as history; it does not certify these new edits.

## 10. Related (FABLE, 2026-09-30)

*(Added 2026-09-30 (FABLE).)*

- [How experience is computed and divided](how-experience-is-computed-and-divided.md) — the function note for the
  experience computer `002F8BB0` (this page is its parent)
- [What happens when an enemy dies](what-happens-when-an-enemy-dies.md) — the defeat sequence that calls both
  computers, with the caps, the level walk, gil, the LP-to-gil effect and New Game Minus
- [Award contract](CONTRACT-experience-and-licence-award.md) — the detailed interface
- [Defeat-rewards contract](CONTRACT-defeat-rewards-sequence.md) — the invariants of the calling body
- [How a battle unit is built](../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md) — the reward rows and the experience curve
- [The auto-status rebuild](../08-Combat-Formula/the-auto-status-rebuild.md) — how equipment sets the effect layers the modifiers read

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL and recorded in the registry.*

`BattleUnit_FindMappedDefinitionSelectorByIndex` (`0031B810`) and the 24-byte mode test `003135C0` are shared lookups:

- **Movement — CLIENT.** `0031B810` is read by `PartyFollow_SolveFormation` and two locomotion bodies (181 B and
  1,028 B). `003135C0` is read by `PartyFollow_SolveFormation` and a 668-byte body.
  The battle runtime mode (`0030D9A0`) is also read by `BattleRuntime_GetModeDependentBaseDistance` and a 448-byte
  locomotion helper.
- **PlatformOnlineAchievements — SERVICE.** `GameState_SetGil` calls the achievement counter updater (counters 6 and 7),
  so any gil these paths move advances an achievement counter.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CombatFormula — CLIENT and SERVICE.** Cited functions are called by `BattleFormula_ApplyTargetResult` (2), `BattleStats_GetByMappedBattleSlot` and a 298-byte formula body. They call `BattleStats_GetByMappedBattleSlot` and `BattleStats_FindOwningBattleUnit`.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAI — CLIENT.** `AiOrder_EvaluateTargetSelector`, owned by that layer, calls `0031B810` on this page. That caller is the selector evaluation, 6,963 bytes of it: it indexes its table at a **six-byte stride** and takes a word at `+6`, two bytes at `+8` and `+9` and a signed word at `+0xA` before deciding anything; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**ActorEntity — SERVICE and CLIENT (8 edges).** `Reward_ComputeExperienceForRecipient` `002F8BB0` calls the roster lookup `BattleUnit_FindMappedDefinitionSelectorByIndex` `0031B810`, which calls `BattleUnit_FindByDefinitionSelector` `002367A0`; `BattleStats_FindOwningBattleUnit` `0031B860` calls `BattleUnit_GetSlotCount` `00236850` and `BattleUnit_GetBySlotIndex` `00236820`; the presentation arm `00289D00` calls `ActorHandle_ResolveRegistryEntryByPackedId` `003588B0`; `BattleUnit_ProcessDefeatRewardsAndLoot` `00312280` calls `Actor_GetWorldPosition` `00265020`; and `BattleGroup_RefreshFourActorDefinitions` `003266C0` calls the designated-index lookup `00313800`. The award finds its recipients through the actor layer's unit table and selector lookups, the EXP/LP presentation resolves the recipient's actor handle, and the defeat path reads the defeated unit's world position for its next step; the actor layer holds the units and computes nothing of the award.

**Gameplay — SERVICE and CLIENT (8 edges).** `002367A0`, `0031B810` and `BattleSlotMap_ResolveMappedBattleSlot` `0031B9F0` call `BattleEncodedId_IsValidForClass` `00322C50`; `BattleStats_GetByMappedBattleSlot` `00320AB0` calls `0031B9F0`; the mode selector `003135C0` calls `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` `0030D9A0` and returns 1 exactly when it answers 1; `00312B40` calls `002367A0`; `00234150` and `BattleUnit_CollectMappedFourSlotUnitsByFlags` `0030A8A0` call `0031B810`. The shared/designated EXP choice is the battle-mode answer, and the recipient lookups validate encoded ids and map slots through the domain's shared helpers, which other slot code also calls.

**Party — CLIENT (4 edges).** `PartyFocus_SelectAndRequestDefaultActor` `00326500` and `PartyConfiguration_ReconcileRuntimeRosterFirstThreeFromRequestedSelectors` `00328DB0` call `002367A0`; `PartyControl_RecomputeSuppressionFromLeaderBattleState` `0023B040` calls `003135C0`; `00304180` calls `00320AB0`. The party code asks the same selector lookup, mode question and slot mapping the award asks; it reads them and does not award anything.

**Presentation — SERVICE and CLIENT (4 edges).** `00312280` calls `Reward_PublishExpLpPresentation` `0028FB80`, which calls `00289D00` (twice, once for the EXP arm and once for the LP arm); `PartyCombat_UpdateStanceState` `00307E70` and `BattleUnit_BroadcastPartyCombatTargetRelation` `00313B30` call `0031B810`. The award publishes its EXP and LP values to the presentation layer after it has computed them, and stance and target-relation code reuse the roster lookup.

**Script_VM_Native_Bridge — CLIENT (7 edges).** `0050FD00`, `0050FD50`, `0050FDD0`, `0050FE20`, `0050FE80`, `0050FED0` and `0050FF20` call `00320AB0`. `0050FD00` (read) pops a slot index, fetches the mapped stats record and pushes its byte `+4`, and the six siblings are the same stats-by-slot verb family named from the census; scripts read the records the award writes.

**Spawn_Encounter_Lifecycle — CLIENT (2 edges).** `Spawn_ValidateCandidateDistanceToPlayers` `00234DA0` and `SpawnLifecycle_CheckAndRetireByNativeRange` `002350C0` call `0031B810`. The spawn layer uses the roster lookup to find the players for its distance tests; it shares a helper with the award and nothing else.

**Status_Periodic_Terminal — CLIENT (7 edges).** `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360` calls `00312280`; `0031B860` is also called by `BattleUnit_ResolvePeriodicPrimaryResourceRecoveryStep` `002F9400`, `0030E360`, `BattleStats_RemoveStatusesFromMaskAndRecompute` `0030F690`, `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` and `BattleFormula_BuildRuntimeCounterPeriodicHpCredit` `00386860`; `BattleUnit_RunPeriodicCombatMaintenance` `00310DB0` calls `00320AB0`. A status change's side-effect processing is what calls the defeat-reward path, and the status code shares the stats-to-unit and slot lookups.

**UI — CLIENT (1 edge).** `BattleMenu_BuildCommandEntryList` `0031EB20` calls `003135C0`. The battle menu asks the same shared-versus-designated mode question when it builds its entries; it does not change the award.

**WorldAreaField — SERVICE and CLIENT (2 edges).** `00312280` calls `FieldData_GetActiveFieldRecordBit15` `00377C20`, and `BattleSystem_RunFieldFrameOrchestrator` `00234590` calls `003135C0`. The defeat path consults the area's action-permission bit, and the field frame asks the mode question each frame; the field layer supplies one bit and owns nothing in the award.
