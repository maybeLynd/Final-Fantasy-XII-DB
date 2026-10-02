---
system: The actor type-id partition and the 13-value band
category: 04-Actor-Entity
status: AUDITED
owner_layer: PrimaryOwner:ActorEntity
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
last_reviewed: 2026-09-03
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-type-id-partition-pass-1
  crossref_clean: false
  reopened_count: 0
---

# The actor type-id partition and the 13-value band

> `record[+4]` is **one type-id number line**, cut into four spans. A unit earns experience, earns
> License Points, can be targeted, or gets its own animation code according to which span it lands
> in — and **the span boundaries are the same everywhere**, inlined at fifty-odd sites rather than
> written once.

**Answers** the battle-record document's open item *"what `unit[4]`'s type ids `0x1B..0x27`
enumerate — the 13-value range that classifies kind 0"*, and the paired question of why `0x1A` is
tested separately.

## 1. What the player sees

Guests fight beside you and never level up. A story character who joins for one dungeon does not
appear in the License menu. Some units cannot be targeted by your gambits at all. None of this is
announced; it is one byte on the record and a handful of range checks.

## 2. The partition, read from the one site that states it whole

Most sites test **one** span and branch. `Reward_ComputeLicensePointsForRecipient` (`002F90C0`) tests
the whole number line, and is the clearest statement in the corpus:

```asm
002F90E2  cmp  byte ptr [rbx+5], al     ; al = 0 -> the record kind must be 0
002F90E5  jne  reject
002F90E7  movzx eax, byte ptr [rbx+4]   ; the type id
002F90EB  cmp  al, 0x1A
002F90ED  je   accept                   ; == 26          -> accept
002F90EF  cmp  al, 6
002F90F1  jbe  accept                   ; <= 6           -> accept
002F90F3  cmp  al, 0x28
002F90F5  jb   reject                   ; 7 .. 39        -> reject
002F90F7  accept:                       ; >= 40          -> accept
```

Combining that with the exhaustive ladder in the Script-VM bridge `FUN_0050FF20`, which classifies a
record into five outcomes:

| `record[+5]` | `record[+4]` | span | Script-VM class | earns LP |
|---|---|---|---|---|
| *no record at all* | — | — | **−2** | — |
| 1 | — | — | **−1** | — |
| 0 | `0x00 – 0x06` | main roster | 0 | **yes** |
| 0 | `0x07 – 0x19` (7–25) | **19 values** | **1** | no |
| 0 | `0x1A` (26) | **a singleton** | **3** | **yes** |
| 0 | `0x1B – 0x27` (27–39) | **the 13-value band** | **2** | no |
| 0 | `≥ 0x28` (40+) | — | 0 | **yes** |

> **The band is not a special case bolted onto a flag byte — it is one span of a partitioned number
> line**, and `0x1A` is a span of exactly one sitting between the other two.

**The partition is necessary but not sufficient for LP.** `002F90C0` does not award once the span
check passes — it goes on to test the merged flag word (§9, 2026-09-13):

```asm
002F90F7  mov  eax, dword ptr [rbx + 0x64]
002F90FA  or   eax, dword ptr [rbx + 0x3c]
002F90FD  test eax, 0x80000003        ; bits 0, 1 and 31
002F9102  jne  reject
```

## 3. The band `0x1B–0x27`: one predicate, twenty-seven copies

A census of every constant tested against a byte loaded from `[reg+4]` across all listed functions
finds **28 sites using `0x1B`**, and **27 of them are byte-for-byte the same predicate**:

```asm
sub al, 0x1b
cmp al, 0xc          ; (type - 27) <= 12   ->  27..39, thirteen values
```

No site uses a different bound — **re-censused image-wide 2026-09-13: 27 sites, every one the `al`
form, every bound `0xC`, in 24 functions** (§9). The 28 sites span **ActorEntity, CombatAction,
CombatFormula, CombatAI, Status, Rewards and the Script-VM bridge** — including
`BattleStats_RebuildEffectiveStatsAndAffinityState`, `BattleFormula_ResolveTargetResult`,
`AiOrder_EvaluateTargetSelector`, `BattleUnit_RunPeriodicCombatMaintenance` and
`BattleAction_CheckDefinitionCategoryAvailability`.

> **One predicate, inlined twenty-seven times, and never once with a different bound.** A category
> this widely consulted and this consistently written is authored, not incidental — but it is also
> a category with **no function of its own**, which is why it never acquired a name.

**Band members earn no experience.** `Reward_ComputeExperienceForRecipient` (`002F8BB0`) returns
zero for them before it reaches the engine-wide functional-status rule:

```c
if (recipient[5] != 0) return 0;
if ((uint8)(recipient[4] - 0x1B) <= 0xC) return 0;         // the band earns nothing
if ((recipient[0x64] | recipient[0x3C]) & 0x80000003) return 0;
```

That second test is the `0x80000003` rule already documented three times over
([`party-roster-and-control-suppression.md`](../../11-Party/party-roster-and-control-suppression.md) §2);
**the band exclusion sits in front of it and is a separate rule.**

## 4. `0x1A` is tested separately because it is a different reason

Two tests where one would do, and the two do not agree:

| Site | the band `0x1B–0x27` | `0x1A` |
|---|---|---|
| `Reward_ComputeExperienceForRecipient` — recipient count | **excluded** | **excluded** |
| `Reward_ComputeLicensePointsForRecipient` | **rejected** | **accepted** |

In the experience counting loop the two tests jump to the *same* target, so both are skipped:

```asm
002F8CC5  sub al, 0x1b
002F8CC7  cmp al, 0xc
002F8CC9  jbe 0x2f8ce0        ; band -> do not count
002F8CD8  cmp byte ptr [rcx+4], 0x1a
002F8CDC  je  0x2f8ce0        ; and 26 -> do not count, by a SEPARATE test
```

Had `0x1A` belonged to the band, the author would have written `(type - 0x1A) <= 0xD` — fourteen
values, one test. **They did not, and §2 shows why: `0x1A` earns License Points and the band does
not.** The two constants coincide in one consequence and diverge in another.

> **Two tests where one would do is two different reasons** — and here both reasons are visible.
> A single widened range would have been smaller code and a silent behaviour change.

`0x1A` appears at **7 sites**: the two reward functions, `BattleUnit_AdvanceExtendedActionState`,
`BattleUnit_UpdateEngagementStateFlag`, `BattleTarget_ComputeUnitEligibilityMask`, `FUN_0031FDA0`,
and the Script-VM bridge — against the band's 28. **It is a narrower category, not a smaller one.**

## 5. The one site that indexes the band instead of testing it

`BattleSpecialSequence_DeriveActionPresentationCode` (`00309230`) is the 28th site, and it is the
only one that uses the band as an **index**:

```c
if (actionRow != table(02EBF138)[0x113])      // one specific action id
    return actionRow[0x24];                    // ordinary: the row's own code
else
    return code13[ record[4] - 0x1B ];         // this action: per-type code
```

The 13-entry table is built on the stack from three 16-byte `.rdata` constants plus a literal, and
its contents are an exact arithmetic progression:

```
type 0x1B -> 42     0x1F -> 54     0x23 -> 66     0x27 -> 78
     0x1C -> 45     0x20 -> 57     0x24 -> 69
     0x1D -> 48     0x21 -> 60     0x25 -> 72        code = 42 + 3 * (type - 0x1B)
     0x1E -> 51     0x22 -> 63     0x26 -> 75
```

**Stride three.** Each of the thirteen types owns a block of three consecutive presentation codes,
and the table hands out the first of each block. **Thirteen types × three variants = thirty-nine
codes, 42 through 80.**

> The progression is the finding. A hand-authored lookup would not be arithmetic; **this table exists
> because the codes are laid out three-per-type somewhere else**, and it is the cheapest way to reach
> the first of each block.

Action id `0x113` is one of the two ids that a global gate elsewhere admits when it refuses all
others — see
[`battle-command-availability-and-reason-codes.md`](../../07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md).

## 6. The `7–25` span is the party layer's guest range

The Script-VM ladder tests `(type - 7) <= 0x12` — **selectors 7 through 25** — which is
*character-for-character* the predicate `PartyConfiguration_IsSelector07To25` applies to a party
configuration selector
([`active-party-reserve-and-the-moment-the-leader-changes.md`](../../11-Party/active-party-reserve-and-the-moment-the-leader-changes.md) §3).

**The same 19-value span, the same test, at two layers**: the party layer uses it to decide which add
path a character takes, and the battle record uses it to classify a unit at runtime. That is strong
evidence the two fields share a numbering space — **but it is not proof they are the same field**,
and no site has been read that copies one into the other. **Recorded as a correspondence, not an
identity.**

## 7. Key addresses

| Address | Name | Role |
|---|---|---|
| `002F90C0` | `Reward_ComputeLicensePointsForRecipient` | states the whole partition (§2) |
| `002F8BB0` | `Reward_ComputeExperienceForRecipient` | band and `0x1A` excluded separately (§4) |
| `0050FF20` | *(unnamed, Script-VM bridge)* | the five-way ladder (§2) |
| `00309230` | `BattleSpecialSequence_DeriveActionPresentationCode` | indexes the band (§5) |
| `002FEF30` | `BattleStats_RebuildEffectiveStatsAndAffinityState` | a band gate in its prologue |
| `00385F60` | `BattleFormula_ResolveTargetResult` | a band gate |
| `00301AD0` | `AiOrder_EvaluateTargetSelector` | a band gate |
| `0030B7F0` | `BattleTarget_ComputeUnitEligibilityMask` | a `0x1A` gate |
| `00D103B0` | — | the 13-entry presentation table (three 16-byte constants) |

## 8. Data structures and formulas

```
battle record
  +0x04  uint8  type id   -- partitioned: 0..6 | 7..25 | 26 | 27..39 | 40+
  +0x05  uint8  kind byte -- 0 and 1 both observed; the partition applies only to kind 0
  +0x3C, +0x64            -- the two status words of the 0x80000003 functional rule

band membership  :  (uint8)(type - 0x1B) <= 0x0C          27 identical inlined copies
guest span       :  (uint8)(type - 0x07) <= 0x12          shared with the party layer
presentation code:  42 + 3 * (type - 0x1B)                for action id 0x113 only
```

## 9. What is not known

- ~~**What the four spans are called.** The behaviour of each is measured; **no string, table name or
  debug label ties any span to a player-facing concept**, and this document deliberately does not
  guess. The obvious reading of "13" is left unwritten for that reason.~~ **Named 2026-09-11 from the
  party table's own text references (§12):** the main roster, the guests, the Chocobo, the thirteen
  Espers.
- ~~**Whether `record[+4]` and the party configuration selector are the same number.** §6 gives a
  correspondence and explicitly stops there.~~ **Narrowed 2026-09-11 (§12):** `record[+4]` is the
  party-table row the installer's selector names, and the party selector's `7`–`25` span is exactly
  the table's guest and unnamed rows; only the copy site is unread.
- **What the three codes per type in §5 select** — the block of three is inferred from the stride,
  and the consumer of codes 42–80 is not read.
- ~~**What span `≥ 0x28` (40+) contains**, which the LP path accepts along with the main roster.~~ **Nothing ships there** — the party table has 40 rows (§12).
- ~~**Whether kind values other than 0 and 1 exist** — still the parent document's open item.~~ *(answered: AL-4, 2026-09-12 — `{0, 1}`, from the writer; battle-record-kind-byte.md §7; 2026-10-02, OPUS)*
- **`FUN_0050FF20` has zero callers** in the function list; as a Script-VM bridge it is presumably
  reached through a dispatch table that was not traced.

## 12. Extension 2026-09-11 — the spans named from the party table (FABLE)

The number this page partitions is the **row index of the party definition table** — registry slot
`02EBF130`, `battle_pack.bin`'s directory entry at the blob's `+0x44`, 40 rows × 128 bytes — and
the table's rows name themselves through their `+0x30` text references
([the battle text banks](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md) §5).
`BattleStats_InitializeDefinitionRecord` stores the selector it receives whole into the record's
`+4` word — low byte the row, high byte the table (`0023AC9E`–`0023ACB2`, `0023AD8E`) — so
`record[+4]` *is* a party-table row number for kind 0. Read against the data:

| span | rows | what the rows are |
|---|---|---|
| main roster (`0x00`–`0x06`) | 0–6 | Vaan, Ashe, Fran, Balthier, Basch, Penelo — and **row 6, Reks**: the prologue's playable is counted with the roster and earns LP |
| the `7–25` guest span (§6) | 7–16 named, 17–25 "No name" | Amalia, three Basch variants, Lamont, two Vosslers, Larsa, two Reddases; nine unnamed rows |
| `0x1A` (§4) | 26 | **Chocobo** — the one mount, tested apart from the band because it earns LP |
| **the 13-value band** | 27–39 | **the thirteen Espers**: Belias, Mateus, Adrammelech, Hashmal, Cúchulainn, Famfrit, Zalera, Shemhazai, Chaos, Zeromus, Exodus, Ultima, Zodiark — the summons that earn nothing |
| `≥ 0x28` (40+) | — | **no such row ships**: the table has 40 rows, so the LP path's acceptance of this span is dead in the shipped data |

Row byte `+0x2B` follows the same partition — 13 for every human row, 30 for the Chocobo, 20 for
every Esper — which is the authored class the spans encode; its consumer is not read here. On the
§6 correspondence: `record[+4]` is now known to be a row of this table, and the party layer's
`7`–`25` selector span is exactly the table's guest and unnamed rows, so the two numberings agree
row for row on the data; a site copying the party selector into `record[+4]` is still unread, so
the identity stays a data-backed correspondence.
## 10. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The partition boundaries 6 / 7–39 / 26 / 40 | `002F90E2`–`002F90F7` decoded in full | 1 |
| The five-way class ladder | `0050FF20` decoded in full, both branch targets read | 1 |
| 28 band sites, 27 with an identical bound | census of every constant tested against `[reg+4]`, then each site's following `cmp` decoded | 1 |
| The band earns no EXP | `002F8BF2`–`002F8BFA`, before the status rule | 1 |
| `0x1A` excluded from the EXP count by a separate test | `002F8CD8` jumping to the band's own target | 1 |
| `0x1A` accepted for LP | `002F90EB` / `je accept` | 1 |
| 7 sites test `0x1A` | the corrected census (below) | 1 |
| The 13-entry table and its stride | the three `.rdata` constants read from the image plus the literal `0x4E` | 1 |
| `7..25` is tested identically at both layers | `sub al,7 ; cmp al,0x12` in `0050FF87` and in `00322350` | 1 |

**Controls, and a defect in this document's own instrument.** The census keyed on
`mov reg, [reg+4]` followed by an immediate comparison. **That form misses `cmp byte ptr [reg+4],
imm`, which never loads into a register** — and the very site that motivated the block, the `0x1A`
test in the experience split, is written that way. The first run reported **1** site for `0x1A`; with
direct memory-immediate compares included it reports **7**.

> **Sevenfold.** This is the fifth instance in this session of the same failure — a scanner keyed on
> the encoding it expected, reporting an absence that was an artifact. The band's count of 28 was
> unaffected because every band site happens to use the register form, **which is luck, not
> validation.**

The absence claim *"no site uses a different bound"* is a measurement: the same pass decodes each
site's following instruction and reports its immediate, and 27 of 28 returned `0xC` with the 28th
returning no comparison at all (it indexes instead).

One decode was discarded: reading `002F90C0`'s body from an arbitrary offset produced
`test dword ptr [rcx + 0x48000000], ecx`, which is not code; the region was re-read from a known
instruction boundary before anything here was written.

`check_already_answered.py` was run for these addresses and terms before the block was started.

## 11. Related

- [`battle-record-kind-byte.md`](battle-record-kind-byte.md) — the parent document, whose open item on the `0x1B..0x27` range this answers.
- [`battleunit-slot-pool-and-actor-class.md`](../battleunit-slot-pool-and-actor-class.md) — the 32-slot pool and the separate three-bit actor class.
- [`active-party-reserve-and-the-moment-the-leader-changes.md`](../../11-Party/active-party-reserve-and-the-moment-the-leader-changes.md) — the `7–25` span at the party layer.
- [`experience-and-license-point-award.md`](../../13-Rewards-Progression-Economy/experience-and-license-point-award.md) — the two reward functions read here.
- [`license-check-what-the-board-actually-tests.md`](../../12-Items-Equipment-Shops-License/license-check-what-the-board-actually-tests.md) — the kind byte's other role.

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

§2's ladder reproduces **instruction for instruction at every address it quotes** — `002F90E2`,
`E5`, `E7`, `EB`, `ED`, `EF`, `F1`, `F3`, `F5` — including the annotation that is easiest to get
wrong: `cmp byte ptr [rbx+5], al` really does test against **zero**, because `al` survives
`test eax, eax` / `jne` on the previous call's result.

`FUN_0050FF20` reproduces too, and its spans are exactly as tabulated: `sub al, 0x1b` / `cmp al,
0xc` for the band, and `sub al, 7` / `cmp al, 0x12` for the nineteen (`7 … 7 + 18 = 25`).

### The predicate census, re-run over the whole image

Scanning every function body for `sub <r>, 0x1B` followed within three instructions by `cmp <r>, N`:

| | |
|---|---:|
| sites | **27** |
| distinct functions | 24 |
| bounds used | **`0xC` × 27** — nothing else |
| register forms | **`al` × 27** — nothing else |

Owners: CombatAction 6, CombatFormula 5, ActorEntity 3, Rewards 2, Status 2, CombatAI 1,
Script-VM bridge 1, unowned 7 — the seven §3 names, and **all five functions it names by name are in
the census**.

*Method note:* §3's own figure of **28 sites** counts "every constant tested against a byte loaded
from `[reg+4]`", which is a wider net than the predicate. A re-implementation of that narrower
criterion found only one of them, so **it is my instrument that is under-powered and the 28 is not
challenged** — register liveness across a call is exactly what it fails to follow. The 28th site was
reached another way, below.

### ⚠ The 28th site is the one place the thirteen are not interchangeable

`BattleSpecialSequence_DeriveActionPresentationCode` (`00309230`, 199 B) is the site that uses
`0x1B` differently, and the difference is not the bound — **it uses `type − 0x1B` as an index**:

```asm
003092CB  mov   rax, qword ptr [rdi + 0x698]
003092D2  movzx eax, byte ptr [rax + 4]        ; the type id
003092D6  sub   eax, 0x1b                      ; the band offset
003092D9  cdqe
003092DB  mov   eax, dword ptr [rsp + rax*4 + 0x20]   ; a THIRTEEN-entry table
```

The table is materialised inline at the top of the function — three 16-byte constants and a
literal, `4 + 4 + 4 + 1 = 13` dwords:

```asm
00309249  movdqa xmm0, [00D103B0]  -> [rsp+0x20]     ; entries 0-3
0030925E  movdqa xmm1, [00D103C0]  -> [rsp+0x30]     ; entries 4-7
00309274  movdqa xmm0, [00D103D0]  -> [rsp+0x40]     ; entries 8-11
00309266  mov dword ptr [rsp+0x50], 0x4E            ; entry 12
```

| type | `0x1B` | `0x1C` | `0x1D` | `0x1E` | `0x1F` | `0x20` | `0x21` | `0x22` | `0x23` | `0x24` | `0x25` | `0x26` | `0x27` |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| **code** | 42 | 45 | 48 | 51 | 54 | 57 | 60 | 63 | 66 | 69 | 72 | 75 | 78 |

**Thirteen distinct codes, and they are an exact arithmetic progression: `code = 3 × (type − 13)`.**

> §3's headline — *one predicate, twenty-seven copies* — is right about the twenty-seven, and the
> twenty-eighth is the interesting one. **Twenty-seven sites treat the band as one class; this one
> distinguishes every member of it.** The stride of **3** says each type owns a *run of three*
> consecutive codes rather than a single one, so the presentation space is 39 wide, not 13.

*(The compiler wrote the progression out as a constant table rather than computing it, so the table
is not evidence of authored per-type data — only that the thirteen are told apart here.)*

### ⚠ Two outcomes the tables omit

**A sixth Script-VM class, `−2`.** `0050FF4D mov ebx, 0xfffffffe` fires when the record lookup
(`00320AB0`) returns NULL — before `record[+5]` is read at all. §2's table starts at
`record[+5] = 1 → −1`, so a caller reading it would map "no record" onto "kind 1". Added.

**The LP rule is the partition *and* a flag gate.** §2 presents `002F90C0`'s span ladder as the
rule, but the function continues past where the excerpt stops:
`(record.+0x64 | record.+0x3C) & 0x80000003` must be **zero** — bits 0, 1 and 31. Passing the span
check is necessary, not sufficient. That `+0x64 | +0x3C` pair is the same merged flag word
[the evaluation context](../../08-Combat-Formula/Evaluation-Context/the-evaluation-context-field-map.md)
builds into its `+0x04` and `+0x08`; **whether it is the same record type is not established here.**

**Not claimed:** §3's 28-site figure and its owner attribution were taken as given, for the reason in
the method note. ~~What the thirteen types *are*, and~~ What a presentation code selects ~~, are~~ is untouched *(answered in part: §12 names the thirteen types — the Espers; 2026-10-02, OPUS)*.
Nothing was executed or observed live.

## SWE2-EC7-48 update (2026-09-19) - `00309230`

`00309230` (199 B) is `BattleSpecialSequence_DeriveActionPresentationCode` - `0020E600`/`00808C40`; indexes the 13-value band. Interior anchor `00309290` (a `0020E600` call).

## Cross-subsystem neighbours — pass 22 (FABLE, 2026-09-29)

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

*The subjects here are the sites where the type-id partition is inlined. They are the band gates `AiOrder_EvaluateTargetSelector` `00301AD0`, `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30` and `BattleFormula_ResolveTargetResult` `00385F60`, the `0x1A` gate `BattleTarget_ComputeUnitEligibilityMask` `0030B7F0` and the band indexer `00309230`. The rest are the two reward functions `002F8BB0` and `002F90C0`, the Script-VM ladder `0050FF20`, the `7..25` test `PartyConfiguration_IsSelector07To25` `00322350` and the mapped-slot getter `00320AB0`. This page's claim is the range test inside each of them. The far ends below are those functions' other callers and callees, which run whatever span the unit is in.*

**CombatAI — SERVICE (8 edges).** The target selector `00301AD0`, one of the band gates, is called by `AiOrder_EvaluateAndResolveActionTarget` `003014C0`. It calls seven AI helpers: `AiOrder_ComputeBoundedSelectorScalar` `00308C20`, `BattleTarget_MatchesRelationMode` `0030BD00`, `BattleTarget_ComputeSurfaceDistanceBetweenUnits` `0031E6F0`, `BattleTarget_ComputeSurfaceDistanceToPosition` `0031E760`, `AiTargetSelector_ResolveOperandValue` `00321190`, `BattleEnmity_ReadForCombatantId` `003215C0` and `BattleEnmity_GetHighestRelevant` `00321630`. The band gate is one early test in the gambit target selector. The distance, enmity and relation helpers it goes on to call are the selector's own AI machinery and do not look at the type id.

**CombatAction — CLIENT and SERVICE (13 edges).** Three action bodies call the formula resolve `00385F60`: `Battle_ProcessActionTarget` `00307300`, `BattleAction_ResolveSpecialSequenceTargets` `0030EC00` and `BattleUnit_HandleActorTimelineEvent` `00319F50`. `BattleAction_InitializeGlobalSpecialSequenceMode` `00306BD0` calls the band indexer `00309230` (§5). `Battle_BuildActionTargetSet` `0030D160` calls `00320AB0`. The `0x1A` gate `0030B7F0` is called by the suppression tests `0030B8E0`, `BattleTarget_HasContextSuppression` `0030B950` and `0030B9B0`. `00301AD0` calls `BattleAction_GetSubtype3Field22OrFFFF` `003093D0`, `BattleTarget_ClassifyRelationshipClass` `0030AB40`, `0030B9B0` and `BattleAction_ComputeActiveTargetStatusIntersection` `0031C500`, and the stats rebuild `002FEF30` calls the unlink `003105D0`. The action layer's target-set, special-sequence and eligibility code reaches the inlined partition tests. That is how the partition makes some units untargetable and gives band members their own presentation code.

**CombatFormula — CLIENT and SERVICE (16 edges).** The formula resolve `00385F60` calls seven formula bodies, among them `BattleFormula_BuildEvaluationContext` `003847C0`, `BattleFormula_InitializeResultRecord` `003848E0` and `BattleFormula_ApplyTargetStatusActionPostModifiers` `00390F20`. It is called by `BattleFormula_QueryResolvedScalarPreview` `00308B90`. `002F8BB0` and `002FEF30` resolve through `BattleStats_FindOwningBattleUnit` `0031B860`, and `002FEF30` also calls `002F8E50` and `002F9180`. `002F8BB0` and `0050FF20` read the mapped-slot getter `00320AB0`. `BattleStats_ModifySecondaryResource` `00300BC0` and `BattleStats_ModifyPrimaryResource` `00300CE0` call the `0x1A` gate `0030B7F0`. The band gate sits at the front of the damage resolve and the stats rebuild. Every other call listed here is ordinary formula machinery running after the gate has passed.

**Gameplay — SERVICE (8 edges).** `00301AD0` calls `BattleEncodedId_DispatchQueryMode0Value` `00309EC0`, `BattleTargetBuffer_ResetPreservingFlag0` `00316CF0`, `BattleDefinition_GetRuntimeCategoryBySelector` `0031EA90`, `BattleUnit_GetPrimaryFormulaResourceByte26` `00321320` and `BattleEncodedId_IsValidForClass` `00322C50`. `002FEF30` calls `BattleUnit_UpdateEngagementStateFlag` `00307D10` and `00322C50`, and `00320AB0` calls `BattleSlotMap_ResolveMappedBattleSlot` `0031B9F0`. These are Gameplay-filed battle helpers for id validation, slot mapping, runtime category and the target buffer, and the gate sites call them. The getter's NULL for an unmapped slot, which §2's table begins from, comes from that slot map.

**Items_Equipment_Shops_License — CLIENT (6 edges).** `Equipment_EvaluateCandidateLoadoutAndBuildDerivedStats` `0030A4E0` calls the stats rebuild `002FEF30`. It and four more items bodies read the mapped-slot getter `00320AB0`: `Equipment_BuildRecommendedLoadoutForMappedStats` `002F9F20`, `InventoryEquipment_RestoreTemporarySnapshotAndClearBackup` `0030FAA0`, `InventoryEquipment_SnapshotAndClearTemporaryState` `0030FBE0` and `Equipment_UnequipEncodedItemFromActiveRoster` `0030FD10`. The candidate-loadout evaluation recomputes stats through a band-gated rebuild, and the loadout bodies fetch the record through the same getter. The partition affects them only through that gate.

**Party — SERVICE and CLIENT (7 edges).** `00301AD0` calls `BattleUnit_ResolveByFocusHandle` `0031B7E0`, `BattleUnit_GetPartyLeader` `003272A0` and `PartyFocus_IsCurrentPackedActorHandle` `003273B0`. `00304180` reads `00320AB0`. Three party verbs call the `7..25` test `00322350` (§6): `VMPartyCommand_MoveSelector00To06OutOfRuntimeRosterWhenMultiple` `00350160`, `VMPartyCommand_DemoteOtherRuntimeRosterSelectors` `00350CD0` and `VMPartyCommand_RemoveSelector07To25` `00352AF0`. The `7..25` span is the party layer's guest range, tested identically there and in the Script-VM ladder, and the party verbs are what act on it.

**Presentation — SERVICE (1 edge).** `00301AD0` calls `BattleUnit_TestActorViewFrustumAtCurrentPosition` `00322360`. The target selector also asks whether a candidate is on screen, which is a view test that is independent of the type-id span.

**Rewards_Progression_Economy — CLIENT (4 edges).** `BattleUnit_ProcessDefeatRewardsAndLoot` `00312280` calls `Reward_ComputeExperienceForRecipient` `002F8BB0` and `Reward_ComputeLicensePointsForRecipient` `002F90C0`, and `002F8BB0` and `00312280` read `00320AB0`. The defeat path is where §2 and §4's rules pay out. Band members earn no experience, `0x1A` earns LP but no experience, and the reward functions this page reads are that path's recipients test.

**Script_VM_Native_Bridge — CLIENT and SERVICE (14 edges).** Seven verb bodies read the mapped-slot getter `00320AB0`, `0050FD00` to `0050FF20` among them. Five more call `00322350`: `0034E7D0`, `00351A40`, `00352190`, `00353460` and `00353CB0`. The ladder `0050FF20` itself pops its argument through `VMValueStack_PopNumericDiscard` `00267DB0` and returns its class through `VMResult_WriteInt32` `0026B4E0`. Script reads the partition through the five-way ladder (classes −2, −1, 0, 1, 2 and 3) and the guest-range test. The bridge only reports the span to script and cannot change it.

**Status_Periodic_Terminal — CLIENT (4 edges).** `BattleUnit_RunPeriodicCombatMaintenance` `00310DB0` calls `0030B7F0`, `00320AB0` and `00385F60`, and `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` calls `002FEF30`. The periodic tick is itself one of §3's band-gate sites and also reaches the other gates through these calls, and the status recompute re-runs the band-gated stats rebuild.

**WorldAreaField — SERVICE (2 edges).** `00301AD0` calls `FieldData_GetFormat0RecordVectorByIndex` `00320940` and the bit-15 predicate `FieldData_GetActiveFieldRecordBit15` `00377C20`. The target selector reads a field record vector and the area's action-permission bit next to its band test, but the field data does not change the type-id span.

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-actor-type-id-partition-and-the-13-value-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00322350` | 12 B | subtracts 7 from the byte `cl` and returns 1 when the result is at most `0x12` unsigned (byte values 7 to 25), else 0 | `00322352`, `00322355`, `00322358` |
| `0034E7D0` | 211 B | pops three values through `00267E10(r9)`, ORing bit v into a mask for each non-negative value v and counting those for which `00322350(v)` is non-zero; starts a budget at 3 when none counted, else at 4 minus the count; when `00359C00()` lacks any mask bit it tail-jumps `0026B4E0(rcx, 0)`; otherwise it subtracts the number of set bits among the 32 of `0035A050(00359BA0() OR mask)` from the budget and tail-jumps `0026B4E0(rcx, 1 when the result is non-negative, else 0)` | `0034E814`, `0034E82B`, `0034E83C`, `0034E865`, `0034E89E` |
| `00350160` | 98 B | pops a value through `00267E10(r9)` and calls `003601B0(0x13)`; when `00322350(low byte)` returns 0 and `0031B510(stack buffer, 4)` returns more than 1 (signed) it calls `003286E0(low byte)`; otherwise returns without that call | `00350178`, `00350184`, `0035018C`, `003501A2`, `003501AA` |
| `00351A40` | 81 B | pops two values a then b through `00267E10(r9)` and calls `003601B0(0x13)`; when `00322350(low byte of b)` returns 0 it calls `00328FB0(low byte of b, 1 when a is non-zero else 0)`, otherwise it returns without that call | `00351A50`, `00351A5A`, `00351A66`, `00351A6E`, `00351A81` |
| `00352190` | 94 B | pops a value through `00267E10(r9)`; for indices 0 to 3 calls `0026DC40(p, 0)` on each non-null `p = 00263750(index)`; calls `003601B0(0x13)` and, when `00322350(low byte of the value)` is non-zero, `003170E0(low byte)` | `003521A8`, `003521B7`, `003521BE`, `003521D1`, `003521DE` |
| `00352AF0` | 57 B | pops a value through `00267E10(r9)` and calls `003601B0(0x13)`; when `00322350(low byte)` is non-zero it tail-jumps `003288F0(low byte)`, otherwise returns | `00352AF9`, `00352B05`, `00352B0D`, `00352B14`, `00352B1E` |
| `00353CB0` | 69 B | pops a value through `00267E10(r9)` and tail-jumps `0026B4E0(rcx, r)` where r is `003596D0(value)` when `00322350(low byte)` is non-zero and `00359740(value)` when it is zero | `00353CC0`, `00353CCA`, `00353CD5`, `00353CDC`, `00353CF0` |
