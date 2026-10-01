---
system: The all-ones empty convention in index spaces
category: 00-Engine-Core-Runtime
status: AUDITED
owner_layer: CodeDomain — shared; no PrimaryOwner
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
  last_pass_state: opus-all-ones-pass-1
  crossref_clean: true
  reopened_count: 0
---

# The all-ones empty convention in index spaces

> **`0xFF` is this engine's null pointer for a one-byte index, and `0xFFFF` for a two-byte one — and
> the reason is that `0` is a valid index.** A modder who writes zero into a handle field has not
> emptied it; they have pointed it at slot zero.

## 1. What the player sees

Nothing directly — but an edited save or a patched field that uses `0` for "nothing" will silently
select the first party member, the first item, or the first pooled record instead of clearing.

## 2. The reason, from the clearest instance

`RelationLook_RemovePooledRelationRecord` (`00512CD0`) unlinks a record from a doubly-linked list held
in a **pool of 16-byte records** at `02CA81F0`. Its links are **one byte each**:

```asm
00512CD0  cmp   byte ptr [rdx + 0xD], 0xFF   ; prev link -- 0xFF means "none"
00512CE3  movzx eax, byte ptr [rdx + 0xE]    ; next link
00512CE7  cmp   al, 0xFF
00512CEE  shl   rax, 4                       ; index * 16 -> the pooled record
00512CF2  add   rax, r10                     ; + pool base
00512CF5  mov   byte ptr [rax + 0xD], 0xFF   ; new head has no prev
```

**`+0xD` and `+0xE` are prev and next indices into the pool, and `0xFF` is the null link.** The
`shl rax, 4 ; add rax, base` shows the byte is an *index*, not a flag.

> **That is why the sentinel is all-ones rather than zero: index `0` is a real record.** In an index
> space over a pool, zero is an occupant, so the only free value is at the other end of the range.
> **The convention is forced by the representation, not chosen for style.**

## 3. The sightings

Eight independent instances, found by different sessions from different directions, none of which
cited another before this document:

| Field | Width | `0xFF`/`0xFFFF` means | Established in |
|---|---|---|---|
| party configuration selector | 1 | empty slot | [party](../11-Party/active-party-reserve-and-the-moment-the-leader-changes.md) §2 |
| `BattleSlotMap_ResolveMappedBattleSlot` return | 1 | lookup failed | [party](../11-Party/active-party-reserve-and-the-moment-the-leader-changes.md) §2b |
| actor's own party slot at `+0x12` | 1 | unassigned | [party roster](../11-Party/party-roster-and-control-suppression.md) |
| pooled relation record links `+0xD`, `+0xE` | 1 | no prev / no next | §2 |
| adjacent handle pair `+0x695`, `+0x696` | 1 | released | `16-UI` |
| trigger record's flag id | 1 | "set no flag" | `14-Story-Event-Quest-Hunt` |
| equipment slot | **2** | empty | [equipment](../12-Items-Equipment-Shops-License/equipment-slots-and-the-single-stat-rebuild.md) §2 |
| reserved item id `unit + 0xDC8` | **2** | none reserved | [item use](../12-Items-Equipment-Shops-License/using-an-item-is-an-action-that-costs-an-item.md) §3 |

**The two-byte cases follow the same rule at the wider width** — `0xFFFF`, not `0xFF` — which a
"the byte `0xFF` is special" reading does not predict.

> **Corrected 2026-09-13 (§9): it is the maximum of the FIELD WIDTH, not of the index space.**
> The pool in §2 holds **32** records — its initialiser loops `cmp ecx, 0x20` with
> `lea rax, [rax + 0x10]` (`00512F10`–`00512F1F`) — so the live index range is `0`–`31` and the
> sentinel is `255`. A reader who took "maximum of the space" literally would write `31` or `32`
> to empty a slot. **The empty value is the largest the byte can hold, not the largest index.**

## 4. How widespread it is, and the limit of the measurement

An image-wide census of immediate stores and compares:

| | sites | functions |
|---|---:|---:|
| byte field **set** to `0xFF` | 169 | 119 |
| byte field **compared** against `0xFF` | 87 | 65 |
| word field **set** to `0xFFFF` | 22 | 18 |
| word field **compared** against `0xFFFF` | 107 | 49 |

Spread across twelve owner subsystems — `Presentation`, `UI`, `CombatAction`, `ActorEntity`,
`Movement`, `Resource`, `Audio` and more.

**These counts are not evidence on their own.** `mov byte [x], 0xFF` is also how one writes a mask or
a signed `-1`, and nothing in a count separates those. The strict test — **a field both written and
compared with the sentinel inside one function** — returns only **six** fields.

| # | function | field |
|--:|---|---|
| 1 | `RelationLook_RemovePooledRelationRecord` `00512CD0` | `+0xD` |
| 2 | `RelationLook_RemovePooledRelationRecord` `00512CD0` | `+0xE` |
| 3 | `00504F00`, the `.fcp` motion-entry loader | `+0xB8` |
| 4 | `00504F00`, the `.fcp` motion-entry loader | `+0xB9` |
| 5 | `BattleAction_UpdateSpecialPresentationSequence` `00306760` | `+0x695` — **alone** |
| 6 | `FUN_004225a0` | `+0x412` |

> **Corrected 2026-09-13 (§9): two adjacent pairs, not three** (~~`+0xD`/`+0xE`, `+0xB8`/`+0xB9`, and
> `+0x695`/`+0x696`~~). `+0x696` is *compared* against `0xFF` at `00306882` but never *written* with
> it in that function — `0030688B` is `mov byte ptr [rbx + 0x696], al`, the handle moving across
> from `+0x695`. It fails the strict test by exactly the asymmetry this section describes. And the
> sixth field, **`+0x412` at `004225A0`, was left out of the count's own description** — it is not an
> index at all (§9).

> **The strict test under-reports by design**, because the normal shape is one function clearing a
> field and a different one checking it. It is reported because six read-and-verified fields support
> the claim better than 256 counted sites, and **the count is given so a reader can see how much is
> being left uncharacterised.**

## 5. Modding notes

**Zero is never "empty" in these fields.** Write `0xFF` to a one-byte handle and `0xFFFF` to a
two-byte one.

**A pooled link is an index, not an offset** — the engine multiplies by the record size (§2), so a
handle value is a slot number.

## 6. What is not known

- **Whether every `0xFF` byte store in §4's 169 is a sentinel.** Certainly not; the count includes
  masks and signed `-1`. This document characterises the convention, not the census.
- [x] ~~**What the `+0x695`/`+0x696` and `+0xB8`/`+0xB9` pairs hold.**~~ **Half answered 2026-09-13
  (OPUS) — and the `+0x695` half was already answered elsewhere while this page recorded it open.**
  [The battle-unit field map](../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md) names them
  **PROVEN**: `+0x695` is `presentationSlot1` and `+0x696` `presentationSlot2`, both
  released through `0030C970` by
  [the commit page](../07-Combat-Action/the-moment-an-action-is-committed.md). **`+0xB8`/`+0xB9` is
  narrowed, not closed:** `00504F00` is the `.fcp` block's motion-entry loader — it "loads all six"
  of `@FMC` / `@FMN` / `@FMW` / `@FRM`, and
  [that sheet](../17-Presentation-Rendering/Model-And-Motion-Formats/fcp-character-parameter-block.md)
  carries the same entries as its own open item. The two open questions are the same question. *(Reconciled 2026-09-30 (FABLE, [record](../_index/candidates/qid-marker-truth-fable-0930/README.md)): that item is UQ-218, ANSWERED 2026-09-30 by SWE2-DATA's pass 18 on the `.fcp` sheet, so this half is no longer open.)*
- **Whether any one-byte index space in this engine uses `0` as its sentinel instead.**
  **Searched 2026-09-13 (§9) — the answer is "80 named candidates, none adjudicated", not "none
  found".** ~~None was found, and no search was run that could prove the absence.~~ A search *can*
  be run: a byte field loaded, scaled and used to address something, and compared against the
  candidate sentinel, with `00512CD0`'s `+0xD`/`+0xE` as the positive control. It returns **22**
  (function, field) pairs for `0xFF` and **80** for `0`. **That is not evidence that `0` is a
  sentinel** — a zero test on an index is usually "is it set" — but the absence is now untested
  rather than unsearchable.

## 7. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| `+0xD`/`+0xE` are pool indices with `0xFF` as null | `00512CD0` decoded: `cmp …,0xFF`, `shl rax,4`, `add rax, pool` | 1 |
| The pool records are 16 bytes | the `shl rax, 4` scaling | 1 |
| Six fields are both written and compared with the sentinel | per-function, per-displacement census | 1 |
| Three of the six are adjacent pairs | their displacements differ by one | 1 |
| The image-wide counts | immediate-store and immediate-compare census over every listed function | 1 |

**Controls.** The §4 counts and the §2 reading are deliberately kept apart: **the counts establish
that the idiom is widespread, the reading establishes what it means, and neither is offered as the
other.** The claim in §3 rests on eight fields each read in their own document, not on the census.

## 8. Related

- [`active-party-reserve-and-the-moment-the-leader-changes.md`](../11-Party/active-party-reserve-and-the-moment-the-leader-changes.md) — two of the eight.
- [`equipment-slots-and-the-single-stat-rebuild.md`](../12-Items-Equipment-Shops-License/equipment-slots-and-the-single-stat-rebuild.md) — the two-byte form.
- [`using-an-item-is-an-action-that-costs-an-item.md`](../12-Items-Equipment-Shops-License/using-an-item-is-an-action-that-costs-an-item.md) — the reserved-item marker.

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run first, per
[`EVIDENCE-STANDARD.md`](../_index/EVIDENCE-STANDARD.md)'s 2026-09-13 amendment. It returned 114
documents on `sentinel`, which is why every claim below names its own address.)*

### The quoted evidence reproduces, instruction for instruction

Every one of §2's six lines is at the address §2 gives it, with the operands §2 gives it — decoded
from the shipped image, not copied from the page.

| §2 says | measured |
|---|---|
| `00512CD0  cmp byte ptr [rdx + 0xD], 0xFF` | identical |
| `00512CE3  movzx eax, byte ptr [rdx + 0xE]` | identical |
| `00512CE7  cmp al, 0xFF` | identical |
| `00512CEE  shl rax, 4` | identical |
| `00512CF2  add rax, r10` | identical |
| `00512CF5  mov byte ptr [rax + 0xD], 0xFF` | identical |

And the pool base the page asserts is *provable* from an instruction the page does not quote:
`00512CD4  lea r10, [rip + 0x2795515]` resolves to **`02CA81F0`**.

### And all four census rows reproduce exactly

| §4 row | page | measured |
|---|--:|--:|
| byte **set** to `0xFF` | 169 / 119 | **169 / 119** |
| byte **compared** against `0xFF` | 87 / 65 | **87 / 65** |
| word **set** to `0xFFFF` | 22 / 18 | **22 / 18** |
| word **compared** against `0xFFFF` | 107 / 49 | **107 / 49** |

**The recipe is recovered and is worth stating, because §4 does not:** over every listed function
body, a `mov` or `cmp` whose destination is a **memory operand whose base is not `rip`** and whose
source is the sentinel immediate. Excluding `rip`-relative destinations is what makes the numbers
come out — they drop 18 byte-set and 9 word-set sites — and it is the right choice, because a global
is not a field. It is a scope, though, and an unstated one.

### ⚠ Two adjacent pairs, not three — and a sixth field the page never names

The strict test returns exactly **six** (function, displacement) pairs, as §4 says. They are not the
six §4 describes:

| # | function | field | |
|--:|---|---|---|
| 1 | `RelationLook_RemovePooledRelationRecord` `00512CD0` | `+0xD` | *adjacent, and both pass* |
| 2 | `RelationLook_RemovePooledRelationRecord` `00512CD0` | `+0xE` | |
| 3 | `00504F00` | `+0xB8` | *adjacent, and both pass* |
| 4 | `00504F00` | `+0xB9` | |
| 5 | `BattleAction_UpdateSpecialPresentationSequence` `00306760` | `+0x695` | **alone** |
| 6 | `FUN_004225a0` | `+0x412` | **not named anywhere in the database** |

`+0x696` is compared against `0xFF` at `00306882` — but the store beside it is
`0030688B  mov byte ptr [rbx + 0x696], al`, **the handle moving across from `+0x695`**, not a
release:

```asm
00306877  movzx eax, byte ptr [rbx + 0x695]
0030687E  cmp   al, 0xFF
00306880  je    0x306898                     ; nothing in the first slot -> skip
00306882  cmp   byte ptr [rbx + 0x696], 0xFF
00306889  jne   0x306898                     ; second slot occupied -> skip
0030688B  mov   byte ptr [rbx + 0x696], al   ; hand the handle across
00306891  mov   byte ptr [rbx + 0x695], 0xFF ; and empty the first
```

So `+0x696` fails the strict test **by exactly the write-here / check-there asymmetry §4 describes**,
which is a better illustration of the section's own point than the claimed third pair was.

### ⚠ The sixth strict field is a countdown, not an index

`FUN_004225a0` is 144 bytes and `+0x412` is its whole subject:

```asm
004225B5  cmp   byte ptr [rdi + 0x412], 0xFF   ; expired / not running?
004225C3  movsx ebx, byte ptr [rcx + 0x2DD]    ;   low bound
004225CA  call  qword ptr [rip + 0x4A0AC8]     ;   a draw
004225D0  movsx r8d, byte ptr [rsi + 0x2DE]    ;   high bound
004225E1  idiv  r8d                            ;   draw mod (high - low + 1)
004225F5  imul  ecx, eax                       ;   times a global scale
004225F8  mov   byte ptr [rdi + 0x412], cl     ;   re-seed
004225FE  movzx eax, byte ptr [rdi + 0x412]
0042260A  test  al, al
0042260E  mov   byte ptr [rdi + 0x412], 0xFF   ; reached zero -> empty again, return 1
00422620  dec   al
00422622  mov   byte ptr [rdi + 0x412], al     ; otherwise tick down, return 0
```

**One of the six fields that carry this document's strongest evidence is a timer.** That does not
weaken the convention — it widens it, and it corrects the title's framing. The reason §2 gives is
that *index `0` is a real record*; the general form is that **every value the field's live range can
take already means something, so "empty" has to sit outside that range**. A countdown satisfies it
for the same reason an index does: `0` means *fires now*, so `0` cannot also mean *not running*.
**`0xFF` is not an index convention. It is an out-of-band convention that index spaces are one case
of.**

### ⚠ "Maximum of the space" is the maximum of the field width

The pool's initialiser settles the size the whole §2 argument rests on:

```asm
00512F10  and   byte ptr [rax], 0xF0     ; clear the kind nibble of record n
00512F13  mov   byte ptr [rax - 3], cl   ; +0xC = n, the record's own slot number
00512F16  lea   rax, [rax + 0x10]        ; 16-byte stride
00512F1C  cmp   ecx, 0x20                ; 32 records
```

**The pool is 32 records of 16 bytes, `02CA81F0`–`02CA83EF`.** So the live index range is `0`–`31`
and the sentinel is `255`: the empty value is the largest the *byte* can hold, not the largest
*index*. §3 is corrected accordingly — a modder who read "maximum of the space" literally would
write `31`.

### What the pooled record is (returned to the database)

`+0xC` was unread by this page and is the field that makes §2's unlink work:

| offset | width | meaning | evidence |
|---|---|---|---|
| `+0x4` | 4 | the key the applier matches an event against | `00512F87  cmp dword ptr [rbx + 4], eax` |
| `+0xC` | 1 | **the record's own slot number**, written `0`–`31` once at init | `00512F13` |
| `+0xD` | 1 | prev, `0xFF` = none | §2 |
| `+0xE` | 1 | next, `0xFF` = none | §2 |
| `+0xF` | 1 | low nibble = kind; `0` = free | `00512F10`, `00512D62  and byte ptr [r8 + 0xF], 0xF0`, `00512F7E  and al, 0xF` |

The five users of the pool are `00512C80`, `00512CD0`, `00512D80`, `00512EF0` and `00512F30` —
nothing else in the image addresses it. The list head is **not** in the pool: the remover's first
argument holds head at `+0xC`, tail at `+0xD` and a live count at `+0xE`
(`00512D67  dec byte ptr [r9 + 0xE]`), beside two global counter bytes at `02EBA480` / `02EBA481`.

### §6's third unknown, searched — with a control, and with the control's first answer thrown away

The discriminator this page itself names for "the byte is an index, not a flag" is that **the value
is scaled**. So: a byte field loaded via `movzx`/`movsx`, scaled (`shl 1..6`, `add r,r`, or used as a
memory index with scale ≥ 2), then *used to address something*, and compared against the candidate
sentinel in the same function.

| sentinel | (function, field) pairs | functions |
|---|--:|--:|
| `0xFF` | 22 | 16 |
| **`0`** | **80** | **73** |

> **The first version of this instrument returned zero for the control and I did not report its
> numbers.** It missed `00512CD0` `+0xD`/`+0xE` twice over: it only accepted `cmp` against the
> *field*, where `00512CE7` compares the *register*; and it treated `00512CEB  movzx eax, al` as a
> redefinition that killed the chain. Fixed, the control returns both fields, which is the only
> reason the `0` column above means anything.
>
> A second version counted bare `imul` as scaling and reported 109. Its most promising candidate —
> `InputControl_NormalizeAnalogAndComputeTransitions` `0035F760`, three *adjacent* byte fields
> `+0x5D`/`+0x5E`/`+0x5F` each tested against zero — is `imul r14d ; shr 8`: **fixed-point analog
> scaling, not indexing.** `imul` was dropped and the addressing requirement added.

**80 candidates is not a finding that `0` is used as an empty marker**; none has been adjudicated,
and the one candidate that was is a false positive. It is a finding about §6: the absence is
**untested**, not unsearchable.

### The widths the census does not reach

§3 argues from one width to the next. The same recipe at four and eight bytes:

| width | set (sites / functions) | compared (sites / functions) |
|---|--:|--:|
| 1 | 169 / 119 | 87 / 65 |
| 2 | 22 / 18 | 107 / 49 |
| **4** | **569 / 378** | **394 / 287** |
| **8** | **247 / 130** | **14 / 12** |

And the widths do not behave alike. There are **zero** `rip`-relative `cmp byte, 0xFF` and **zero**
`rip`-relative `cmp word, 0xFFFF` sites in the image — against **1,738** `rip`-relative
`cmp dword, -1`. At four and eight bytes the idiom is several times more common and *far* less
separable from a signed `-1` return, which is a good reason to scope this page at one and two bytes
and no reason to leave the scope unsaid.

**The strict test finds no two-byte field at all** — 0 pairs, against 6 at one byte. §3's two-byte
half rests entirely on its two cited documents, and both still say what §3 says they say. One of
them records its check in *register* form (`mov eax, 0xFFFF ; cmp si, ax`), a shape this
memory-operand census cannot see — so §4's two halves are not measuring the same population.

### Two peer-owned corrections, routed and not applied

1. **`0030688B` is mis-transcribed** in
   [the commit page](../07-Combat-Action/the-moment-an-action-is-committed.md) as
   `mov byte ptr [rbx + 0x696], 0xff`. It is `mov byte ptr [rbx + 0x696], al`, and the error inverts
   the meaning: the code *fills* the second slot from the first, it does not release it. The
   neighbouring citation `003066E4  mov byte ptr [rbx + 0x696], 0xFF` **is** correct — it is in a
   different function, `FUN_003065d0`.
2. **`00512F53`–`00512F8A` is not a table match.**
   [The group-completion page](../05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md)
   describes `RelationLook_ApplyRelationEvent` there as matching "the event against a 32-entry table
   at `02CA81F0`". **The 32 is right** — proved above, from the initialiser, which that page does not
   cite — but those instructions load a **list head** from `[r11 + 0xC]` and walk `+0xE` next-links to
   `0xFF` (`00512F53`, `00512F70`–`00512F92`). They visit only the records on one list and have no
   bound at all.

**Not claimed.** The other six of §3's eight sightings were not re-derived from the image; the two
two-byte ones were re-read in their own documents only. The 80 zero-sentinel candidates are
unadjudicated. What `+0xB8`/`+0xB9` and `+0x412` *hold* is still unread — `+0x412`'s behaviour is
read, its subject is not. Nothing was executed and nothing was observed live.

*(Pass 22 adjacency, 2026-09-14: `00306760` — the all-ones probe's context — calls **rewards**
`0030C470` and **gameplay** `003299B0` (2 edges). The convention is checked by code that also
drives reward and gameplay updates; the edges locate the probe inside that caller's work, they do
not change what the convention is.)*

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Spawn_Encounter_Lifecycle — CLIENT.** `SpawnGroup_RecordMemberDeathAndHandleCompletion` and a 110-byte spawn body call functions this page cites.
- **Status_Periodic_Terminal — CLIENT and SERVICE.** Cited functions are called by `BattleStats_ChangeStatusAndProcessSideEffects` and `BattleUnit_RecoverFromTerminalStatusSetIfClear`. They call `BattleStats_RemoveStatusesFromMaskAndRecompute` and `BattleStats_RecomputeDerivedStateAndAutoStatuses`.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAI — CLIENT.** `BattleUnit_UpdateCombatFrame`, owned by that layer, calls `003299B0` on this page. That caller is the per-unit combat frame step, behind `byte[02089340] & 0x20`: it tests the unit's stats record for bit 4 of the OR-ed `+0x3C`/`+0x64` pair - the **sixth** entry point on that pair - and on the retire path appends `dword[unit+8]` to a **64-entry ring** at `022BE984` whose index at `byte[022BE981]` wraps with `& 0x3F`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatFormula — SERVICE.** `0030C470` on this page calls `BattleStats_ReconcileResourcesToEffectiveCapacity`, owned by that layer. What it reaches is the resource reconciliation: the effective value is `word[+0x28]` when `byte[+0x6C]` is non-negative and `byte[+0x7C]` is not below zero, and zero otherwise, compared against `word[+0x4C]`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Input — CLIENT (2 edges, one fan-in).** All 2 edges are Input bodies reaching `0035F760` on this page. `InputControl_FilterTransitionMaskWithRepeat` is the worked example - it is the repeat filter over two parallel `word[+4 + index*2]` buffers, carrying `0x10` and `8` as its two thresholds. The crossing is **one shared subject with 2 callers on that layer**, not 2 separate relationships. Edge count from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).
- **ActorEntity — CLIENT and SERVICE (5 edges).** 1 inbound (ActorEntity bodies `BattleUnit_ActivateAppliedDefinitionRuntime` (00233AD0) call page-cited `BattleUnit_DispatchActorPresentationEvent` (003299B0)); 4 outbound (page-cited `BattleAction_UpdateSpecialPresentationSequence` (00306760), `002E9B80` call ActorEntity bodies `ActorHandle_ResolveRegistryEntryByPackedId` (003588B0), `00332130`, `BattleUnit_GetBySlotIndex` (00236820)). Substantive edges include `BattleAction_UpdateSpecialPresentationSequence` (00306760) calls `00332130`; `BattleUnit_DispatchActorPresentationEvent` (003299B0) is called by `BattleUnit_ActivateAppliedDefinitionRuntime` (00233AD0); the remaining edges run through shared helpers the page cites.
- **Items_Equipment_Shops_License — SERVICE (1 edge).** 1 outbound (page-cited `0030C470` call Items_Equipment_Shops_License bodies `BattleStats_ComputeLicenseDerivedRank` (00324100)). Substantive edges include `0030C470` calls `BattleStats_ComputeLicenseDerivedRank` (00324100).
- **Movement — CLIENT (1 edge).** 1 inbound (Movement bodies `00313500` call page-cited `BattleUnit_DispatchActorPresentationEvent` (003299B0)). Substantive edges include `BattleUnit_DispatchActorPresentationEvent` (003299B0) is called by `00313500`.
- **Party — MECHANICAL (1 edge).** 1 call from page-cited bodies into shared Party plumbing (`BattleUnit_ResolveByFocusHandle` (0031B7E0)) - the helpers' general call surface, not a Party relationship of this page's subjects.
- **Presentation — CLIENT and SERVICE (25 edges).** 23 inbound (Presentation bodies `RelationLook_ResolveRelationPair` (00512D80), `0024E2F0`, `CharacterRenderSystem_UpdateLODAndRenderState` (004264A0) call page-cited `002E9B80`, `00512C80`, `RelationLook_RemovePooledRelationRecord` (00512CD0)); 2 outbound (page-cited `RelationLook_ResolveRelationPair` (00512D80), `RelationLook_ApplyRelationEvent` (00512F30) call Presentation bodies `RelationLook_RemovePooledRelationRecord` (00512CD0)). Substantive edges include `00512C80` is called by `004215A0`; `00512C80` is called by `CharacterRenderRecord_TeardownAndReset` (004200A0); `RelationLook_RemovePooledRelationRecord` (00512CD0) is called by `RelationLook_ResolveRelationPair` (00512D80); `RelationLook_RemovePooledRelationRecord` (00512CD0) is called by `RelationLook_ApplyRelationEvent` (00512F30); the remaining edges run through shared helpers the page cites.
- **UI — SERVICE (1 edge).** 1 outbound (page-cited `BattleAction_UpdateSpecialPresentationSequence` (00306760) call UI bodies `0035C620`). Substantive edges include `BattleAction_UpdateSpecialPresentationSequence` (00306760) calls `0035C620`.
- **WorldAreaField — CLIENT (1 edge).** 1 inbound (WorldAreaField bodies `BattleSystem_RunFieldFrameOrchestrator` (00234590) call page-cited `003065D0`). Substantive edges include `003065D0` is called by `BattleSystem_RunFieldFrameOrchestrator` (00234590).
## SWE2-EC7-42 update (2026-09-19) - `00512D80`

`00512D80` (320 B) is an all-ones-convention body - `022C6F28`/`02CA81F0`, `002E9B80` quintuple plus `00512CD0`. Interior anchor `00512DB7` (an `002E9B80` call).
