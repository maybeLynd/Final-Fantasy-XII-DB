---
system: Active party, reserve, and the moment the leader changes
category: 11-Party
status: AUDITED — both items that kept it PARTIAL are answered: camera record 2 is the ordinary field camera, on screen whenever no event camera (records 3-7) is active (GR-10, 2026-09-30, OPUS) and nothing reads the unwritten part of camera context 0's `+0x6F0` block as values (GR-11, 2026-09-30, OPUS) (owner re-status 2026-10-01, OPUS; documented_rule READY)
owner_layer: PrimaryOwner:Party
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
  parent_tag: GN159
last_reviewed: 2026-09-30
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-active-party-and-leader-change-pass-1
  crossref_clean: true
  reopened_count: 0
  promoted: 2026-10-01 DOCUMENTED -> AUDITED by SWE2-AUDIT-SPEC (FRONTIER eligibility census sweep): falsification record opus-active-party-and-leader-change-pass-1; audit_crossrefs at HEAD reports 0 unresolved findings; cross-subsystem neighbours dispositioned in their section; killer observations recorded in the pass; promoter is not the last substantive author (last substantive commit: OPUS)
---

# Active party, reserve, and the moment the leader changes

> **There is no leader.** There is a 32-bit handle, and whoever it points at is the leader — derived
> fresh on every one of twenty-five call sites, never stored, never announced. Changing leader is a
> *request* that some later commit point applies.

**Answers `O-5`** ("whether reserve/inactive party members live in a separate structure") — they do,
in the same array, at indices `4..8`.

## 1. What the player sees

Four slots you can fill, a bench you swap from, and guests who join without taking a bench place.
Switch who you are controlling and the others immediately follow the new leader — no transition, no
pause, no moment where the formation is confused about whom to follow.

That last one is a consequence of §4: nothing has to be told.

## 2. The configuration array — nine slots, four of them active

`PartyConfiguration_CollectRuntimeRosterSelectors0To3` (`0031B510`) and
`PartyConfiguration_FindAvailableNonRosterIndex4To8` (`00321100`) read the same array from opposite
ends:

```c
base = [02EBF190];
// roster:     indices 0..3, byte at base + 0x5A7E + index*2
// non-roster: indices 4..8, byte at base + 0x5A86 + (index-4)*2
```

`0x5A86 − 0x5A7E = 8 = 4 × 2`, so **it is one nine-entry array of two-byte records with the selector
in the first byte**, split by convention:

| indices | role | count |
|---|---|---|
| **0 – 3** | the **active roster** | 4 |
| **4 – 8** | the **reserve** | 5 |

**`0xFF` in the selector byte means the slot is empty**, and both functions test exactly that. ~~An
index is also skipped if `BattleEncodedId_IsValidForClass(0x17, index)` fails~~ *Corrected 2026-09-30 (FABLE):
only the roster read skips an index that fails `BattleEncodedId_IsValidForClass(0x17, index)` (`0031B553`/`0031B555`);
the reserve probe takes the same branch as its `0xFF` hit (`0032112E`/`00321130` and `00321139`/`0032113D`, both to
`00321158`) and returns that index, so there the check ends the search rather than skipping* — the same shared
validator the License check uses with class `0x14` for actions and `1` for equipment
([`license-check-what-the-board-actually-tests.md`](../12-Items-Equipment-Shops-License/license-check-what-the-board-actually-tests.md) §3).
**Class `0x17` is the party-configuration index class**, which is the third observed class and the
strongest evidence yet that `00322C50` is a per-class id validator rather than a single gate.

> **The reserve is not a separate structure. It is the same array past index 3** — which is why a
> swap is an index change and needs no allocation, and why the roster and the bench can never
> disagree about who is where.

> **CORRECTED 2026-09-03 — `+0x5A7E` is one of five parallel maps, not the only one.**
> `BattleSlotMap_ResolveMappedBattleSlot` (`0031B9F0`) selects a base by a **class** argument:
> `0x5A48`, `0x5A5A`, `0x5A6C`, **`0x5A7E`**, `0x5A90` — **five bases exactly `0x12` apart**, nine
> two-byte slots each, and all five validated against the same class-`0x17` id check. **This section
> read class 3.** The roster/reserve split above is correct *within* that map, and it is not the
> whole structure. See
> [`the-five-parallel-slot-maps.md`](the-five-parallel-slot-maps.md), which established the resolver
> and the fact that the initialiser fills only `+0x5A48` and copies it verbatim into the other four.
>
> **Nothing pointed from here to the other four**, which is why the reading looked complete: five
> functions touch this structure and no document cited two of them.

## 2b. Which of the five maps is which — three named, two unreached

Added 2026-09-03, after the correction above. `BattleSlotMap_ResolveMappedBattleSlot` takes the class
as its second argument, so **censusing that argument names the maps by what asks for them.** The
resolver has only four direct callers, three of which are thin wrappers that pass the class through;
scanning the wrappers' own call sites gives **31 sites, 23 of them passing a constant**:

| class | base | passed by | reading |
|---:|---|---|---|
| **0** | `0x5A48` | `Equipment_UnequipEncodedItemFromActiveRoster` (`0030FD10`) | **the active roster** — and the only map the initialiser fills, the source the other four are copied from |
| **1** | `0x5A5A` | `Reward_ComputeExperienceForRecipient` (`002F8BB0`), `BattleUnit_RunPeriodicCombatMaintenance` (`00310DB0`), two more | **the combat-processing set** — who earns and who is serviced each tick |
| **3** | `0x5A7E` | **fourteen sites**: equipment evaluation and snapshots, `Battle_BuildActionTargetSet` (`0030D160`), `BattleUnit_ProcessDefeatRewardsAndLoot` (`00312280`), a `Party` function, the script-VM bridge | **the general gameplay map** — the one §2 reads |
| 2 | `0x5A6C` | the battle-menu member walk `0035BC50` (`0035BDB9` `mov ecx, 2`), through the wrapper `00320040`, which takes the class FIRST (`0032004F` / `00320051` swap it into the resolver's second argument) | ~~**no constant-passing site found**~~ **the battle command menu's member map** *(corrected 2026-09-30, FABLE, [record](../_index/candidates/sd124-125-menu-fable-0930/README.md), `class2_census.py`: the wrapper's swapped argument order hid the only constant-class-2 site; its other four callers pass class 3)* |
| 4 | `0x5A90` | — | **no constant-passing site found** |

**Class 0 naming itself is the strongest of the three**: its single caller is
`Equipment_UnequipEncodedItemFrom*ActiveRoster*`, and class 0's base is exactly the map the
initialiser populates before copying it into the other four.

> **The five maps are one roster and four copies of it.** Class 0 is what the party *is*; classes 1
> and 3 are what combat and gameplay *ask for*.

**CORRECTED 2026-09-03.** This paragraph first called maps 1–4 *"four views allowed to drift"*. A
displacement census over the five 18-byte ranges found **66 sites, 60 reads and 6 writes** — and
**only map 0 has a writer besides the initialiser** (`00329080`), which fits class 0 being the map the
initialiser fills before duplicating. **Nothing was found that writes maps 1–4 after the copy**, so
"allowed to drift" asserted a freedom the evidence does not show.

**That census is displacement-addressed**, so a pointer taken into a map and stored through would not
appear in it. Two further scans were run to close the gap, each asking a **different question**:

| instrument | question | result |
|---|---|---|
| displacement census | what writes offset N? | maps 1–4: initialiser only |
| base-keyed scan incl. `lea` | does a pointer into the range escape? | **0 `lea` into any of the five ranges** |
| register-held-offset scan | is a base loaded as a bare immediate and indexed? | **6 reads of map 1, 2 of map 3, 0 writes to maps 1–4**; map 0's only two writes are both `0xFFFF` fill loops in initialisers |

The third was necessary: the bases *are* used as bare immediates (`mov esi, 0x5A5A` then
`movzx eax, byte [rsi + base]`), a form **neither of the first two can see**.

> **Three instruments, three different questions, one answer: nothing writes maps 1–4 after the
> copy.** That is worth more than three runs of one instrument — a negative is only as strong as the
> variety of questions that failed to overturn it.

**A note on the third instrument, because it cut both ways.** Run block-aware it returned **zero
accesses**, including one this session had already read by eye — the base register is loop-invariant
and survives a branch the conservative version resets at. Run permissively it found the real
accesses, and **every hit was read before being counted**.

> **For a negative, use the instrument that cannot invent; for a search, use the one that cannot
> miss, and read everything it returns.** The conservative version omits as badly as the linear one
> invents, and choosing between them without saying which is in use is how a zero becomes a claim.

**Classes 2 and 4 are unreached, not absent.** Eight of the 31 sites pass the class through from their
own caller, so a constant for either could exist one level further up; the census establishes that
**no site passes 2 or 4 directly**, which is weaker than "nothing uses them" and is stated as such.

## 3. Members and guests are two selector ranges, and they enter at different ends

```c
PartyConfiguration_IsSelector07To25(sel)  ->  (uint8)(sel - 7) <= 0x12     // selectors 7..25
```

Two add functions accept **disjoint** ranges and place their entry differently:

| Function | Accepts | Placement |
|---|---|---|
| `003172E0` `PartyConfiguration_AddSelector00To06ToAvailableIndex4To8` | selectors **0–6** | an available index in **4–8**, via `00321100` |
| `003170E0` `PartyConfiguration_AddSelector07To25ToAvailablePrimaryIndex` | selectors **7–25** | ~~an available **primary** index~~ the first free roster index of **3, 2, 1** — never 0 (§9, 2026-09-30) |

Both begin with the same nine-entry **dedup scan** over `base + 0x5A48` (stride 2): if the selector is
already present anywhere in the configuration, the add **fails**. Nobody can be in the party twice.

> **A recruitable character joins the bench; a guest does not.** The split is a property of the
> selector's numeric range, not of a flag on the character — 0–6 and 7–25 are two populations the
> engine keeps apart by arithmetic.

This is the party-layer half of a distinction the License work found from the other side: a guest
**never reaches** the License board check, because that check exits early for any unit whose battle
record kind byte is non-zero. **The party layer decides who is a member; the battle layer then never
has to ask.**

## 4. The leader is a handle, and changing it is a two-step

Three globals carry the entire mechanism:

```
022C7FE0   uint32   the CURRENT focus handle  -- the leader
022C7FE4   uint32   the PENDING handle        -- a requested change
022C7FF8   uint8    the request kind          -- 0 = nothing pending
```

**`BattleUnit_GetPartyLeader` (`003272A0`) stores nothing.** It reads the handle, resolves it through
the actor registry, and validates:

```c
h = PartyFocus_GetCurrentPackedActorHandle();     // return DAT_022C7FE0
if (!(DAT_02089340 & 0x10))          return NULL;
e = ActorHandle_ResolveRegistryEntryByPackedId(h);
if (!e) return NULL;
u = ActorWork_GetBattleUnitRaw(e);
if (!u || !(u[0] & 8))               return NULL;
return u;
```

It has **25 callers across 6 owners, nine of them in Movement** — including
`PartyFollow_SolveFormation` (`00338490`) and `PartyFollow_LookupDestination` (`00339A60`). **The party follows the leader by
asking who the leader is, every time.**

### Requesting

`PartyFocus_RequestPackedActorHandle` (`003594B0`) is the only requester, and it is three
instructions:

```c
DAT_022C7FE4 = handle;      // pending
DAT_022C7FF8 = 1;           // a request is now pending
```

### Committing — this is the moment

`PartyFocus_CommitPendingPackedActorHandle` (`00358BC0`):

```c
if (DAT_022C7FF8 == 0) return;                    // nothing pending
pending = DAT_022C7FE4;
current = DAT_022C7FE0;
if (current != pending) {
    old = ResolveRegistryEntryByPackedId(current);
    PartyFocus_ClearCurrentActorIfEligible();
    FUN_00259800(0);
    if (current != 0 && DAT_022C7FF8 != 2)  FUN_0025A680(old, 0);   // one teardown
    else                                    FUN_0025A690(old, 0);   // the other
    pending = DAT_022C7FE4;                       // re-read after the teardown
}
DAT_022C7FE0 = pending;                           // <-- the leader changes HERE
DAT_022C7FF8 = 0;                                 // request consumed
newEntry = ResolveRegistryEntryByPackedId(pending);
if (newEntry) { ... }
```

Four things worth stating plainly:

- **The change is deferred.** Requesting does not change the leader; a later commit does. Anything
  reading `BattleUnit_GetPartyLeader` between the two sees the *old* leader.
- **The pending handle is re-read after the teardown**, so a teardown that itself requests a
  different focus wins.
- **The request kind selects between two teardown paths** — `2` takes the alternate.
- **No observer is notified — but both actors are pushed.** The commit's own body has no callback
  list, dirty flag or event, and every consumer examined derives the leader on demand. Its callees
  do act, though (read 2026-09-11, ASTRA-REQ-FABLE-FOCUS-COMMIT): `PartyFocus_ClearCurrentActorIfEligible`
  zeroes the current handle `022C7FE0` (`00358B6B`) and gives the *outgoing* actor
  `Actor_StopRequestedMovement` (`0026D6D0`), `002EC5B0(actor, 0)` and `002681D0` (`00358B7A`–
  `00358B98`); the two "teardowns" are one function, `0025A6A0(actor, 0, kind != 2 ? 1 : 0)`, which
  ~~snapshots a 0x90-byte block of the manager's `0x860`-stride record from `+0x7A0` to `+0x6F0`
  (`0025A6CB`–`0025A743`, the rest unread)~~ *corrected 2026-09-30 (FABLE), body read whole: re-seats camera
  context 0, one of two `0x860`-byte camera contexts rather than a manager record, and its `+0x7A0` to `+0x6F0` copy is
  `0xB0` bytes (`0025A6FC`–`0025A763`), not `0x90` — §9 gives the five steps*; and the *incoming* actor gets `002681D0` → `002681E0`, a
  locomotion-mode push for kind-3 actors driven by the secondary context's byte `+0x152`
  (`002681E9`–`00268245`). ~~which is why the formation never lags a frame behind~~ — the change
  waits for the commit, and whether the formation sees it in the same frame depends on where the
  commit runs, ~~which §9 leaves open~~ *which §9 answers (2026-09-18): once a frame, from whichever of the three mode
  frame bodies runs, so a read of the leader after that call sees the new one and a read before it the old*. ASTRA's [EXP-051](../_experiments/EXP-051-focus-commit-reentrancy.md)
  executed the commit's body with the callees controlled — the pending handle re-read after the
  teardown, the kind read after the preparation, a kind cleared after entry not aborting, and the
  order current-store → kind-clear → resolve → `002681D0` — ten cases and one detected omission;
  isolated execution, no live timing.

> **Leadership is not a property anyone owns; it is a question everyone asks.** The same shape the
> battle-group layer shows, where a unit is its group's leader when its own id equals its group id
> — no "is leader" flag exists there either.

### Who can set request kind 2 — and a census that could not see it

The five sites my function-bounded sweep found never write `2`: `RequestPackedActorHandle` writes
`1`, `ResetState` zeroes everything, `Commit` clears to `0`. **An unbounded `.text` scan found a
tenth site my census had no way to reach** — a 27-byte function at **`003594C0` that is absent from
the function list**:

```asm
003594C0  movzx edx, byte ptr [022C7FF8]
003594C7  test  dl, dl
003594C9  movzx eax, cl
003594CF  cmovne r8d, eax                  ; only if a request is already pending
003594D3  mov   byte ptr [022C7FF8], r8b
```

**It upgrades the kind of an already-pending request and does nothing otherwise.** That is the only
path to kind `2`. *Its caller (added 2026-09-30, FABLE): a 10-byte thunk that loads `2` and jumps here, whose only
reference is the result slot of script verb `0x205` `changetosummonparty` ([the focus contract](CONTRACT-party-focus-and-control-suppression.md), PF-6, re-checked
against the raw call index today: one `jmp` site, no call). Shipped scripts call that verb 13 times, in 13 of the
1,114 decompiled scripts, so kind `2` is reached in the shipped game: a change to the summon party.*

> A caller census is bounded by its function list. **This one was wrong by one function, and the
> missing function was the only writer of the value in question.** The unbounded scan that found it
> also produced a false positive in the same run (`003590C3`, a float read mid-instruction), which is
> the price: completeness bought with candidates that must each be decoded before they are believed.

## 5. Key addresses

| Address | Name | Role |
|---|---|---|
| `003272A0` | `BattleUnit_GetPartyLeader` | derives the leader from the handle (§4) |
| `003590D0` | `PartyFocus_GetCurrentPackedActorHandle` | `return DAT_022C7FE0` |
| `003594B0` | `PartyFocus_RequestPackedActorHandle` | the only requester |
| `00358BC0` | `PartyFocus_CommitPendingPackedActorHandle` | **the change happens here** |
| `003594C0` | *(unnamed, absent from the function list)* | the only writer of request kind `2` |
| `00358B40` | `PartyFocus_ClearCurrentActorIfEligible` | releases the outgoing leader |
| `003590E0` | `PartyFocus_ResetState` | zeroes the whole focus block |
| `00359410` | `PartyFocus_SetSecondaryPackedActorHandle` | a **secondary** focus at `022C7FE8` |
| `003593A0` | `PartyFocus_SetTemporaryControlledActorOverride` | a temporary override |
| `0031B510` | `PartyConfiguration_CollectRuntimeRosterSelectors0To3` | roster read (§2) |
| `00321100` | `PartyConfiguration_FindAvailableNonRosterIndex4To8` | reserve allocation (§2) |
| `00322350` | `PartyConfiguration_IsSelector07To25` | the guest range test (§3) |
| `003172E0` / `003170E0` | `PartyConfiguration_AddSelector…` | the two add paths (§3) |
| `02EBF190` | — | party configuration table handle |
| `022C7FE0` / `022C7FE4` / `022C7FF8` | — | current / pending / request kind |

## 6. Data structures and formulas

```
[02EBF190] + 0x5A48   map 0: the party configuration, nine 2-byte records, selector in byte 0,
                        0xFF = empty; index 0..3 active roster, 4..8 reserve;
                        the two add paths scan it for duplicates
[02EBF190] + 0x5A7E   map 3: a battle mapping rebuilt from map 0, same layout; the roster
                        and reserve queries of section 2 read this copy
                        (maps 1, 2 and 4 at +0x5A5A, +0x5A6C, +0x5A90: section 2b)

selector 0..6    a recruitable member  -> placed at an index in 4..8
selector 7..25   a guest               -> placed at a "primary" index

022C7FE0  current focus handle = THE LEADER
022C7FE4  pending focus handle
022C7FF8  request kind: 0 none, 1 normal, 2 alternate teardown
022C7FE8  secondary focus handle
```

*Corrected 2026-09-30 (FABLE): this block named `+0x5A7E` as the configuration and `+0x5A48` as "a parallel
nine-entry, 2-byte array scanned for de-duplication on add". §2's 2026-09-03 correction, §2b and
[the five parallel slot maps](the-five-parallel-slot-maps.md) (its 2026-09-14 correction) already have map 0 at `+0x5A48` as the configuration and map 3 as a copy
rebuilt from it; the block now says the same.*

The active roster also exists as **four actor pointers at `0209A1F0`**, with each actor carrying its
own slot at `+0x12` (`0xFF` unassigned) — established in
[`party-roster-and-control-suppression.md`](party-roster-and-control-suppression.md), not
re-derived here. **The roster is four slots, not three**, in both representations.

## 7. Call chain

```
something requests a leader change
  -> PartyFocus_RequestPackedActorHandle (003594B0)      pending = h, kind = 1
     [optionally  003594C0                               kind = 2, if already pending;
                                                         from verb changetosummonparty's result]
  ...
  -> PartyFocus_CommitPendingPackedActorHandle (00358BC0)
       -> ActorHandle_ResolveRegistryEntryByPackedId     the outgoing leader
       -> PartyFocus_ClearCurrentActorIfEligible
       -> 0025A680 or 0025A690                           teardown, chosen by kind
       -> DAT_022C7FE0 = pending
consumers, every frame, on demand:
  BattleUnit_GetPartyLeader (003272A0)  <- 25 callers, 9 in Movement
```

## 8. Modding notes

**To change the leader, write the pending handle and set the kind — do not write `022C7FE0`.**
Writing the current handle directly skips the outgoing actor's teardown, which the commit is there to
perform.

**To put someone on the bench, find a free index in 4–8** (`0xFF` selector) rather than shifting the
array; nothing depends on the reserve being packed.

**Selector range decides member-versus-guest.** Renumbering a character across the 6/7 boundary
changes which add path accepts them and where they land.

## 8a. The non-guest collector and four small bodies around it (read whole 2026-09-19, FABLE)

*The script's side of these - the eight asynchronous party verbs, what each begin does and the poll they share - is
on [how a script changes the battle party](../01-Script-VM-Native-Bridge/Party-Presentation-Verbs/how-a-script-changes-the-battle-party.md).*

| body | what it does |
|---|---|
| `00320800` (144 B) | the **whole-array** counterpart of `0031B510`: for slots 0..8 it requires a valid class-`0x17` id, reads the selector byte at `+0x5A7E + 2 x slot`, and **keeps it when it is not a guest** - 6 or below, or `0x1A`..`0xFE` (so `0xFF` is dropped too; `cmp cl, 6` / `jbe` at `00320852`/`00320855`, then `lea eax, [rcx-0x1A]` / `cmp al, 0xE4` / `ja` at `00320857`–`0032085C`) - writing the kept selectors as dwords to the caller's buffer up to the caller's limit, and returning how many |
| `00359C00` (93 B) | calls it with a limit of nine and returns a **bit mask**, bit *selector* set for each one kept |
| `00359BA0` (93 B) | the same mask over `0031B510`'s four roster slots |
| `00352AF0` (57 B) | script-side: pops one integer, calls a notifier with the constant `0x13`, and tail-calls the remover `003288F0` **only when the selector is a guest** (`00322350`) - a main character cannot be removed through it. ~~It has no call site and no address-taking instruction in `.text`; how it is reached was not established~~ *Found the same day: it is the **begin callback of script verb `0x35C` `removeguestbattlemember`** in the dispatch table, read by the accessor frame - [the dispatch table](../01-Script-VM-Native-Bridge/scriptvm-native-dispatch-table.md). A table pointer is neither a call site nor a `lea`* |
| `003596B0` (24 B) | returns 1 unless a status query (`00324360`, itself a boolean of `0037CB50`) answers exactly 1. ~~*Its label says "async mutation pending"; what `0037CB50` reports was not read, so the polarity is stated, not the meaning*~~ *Carried here 2026-09-30 (FABLE): `0037CB50` is the end test of the party read-in task ([how a script changes the battle party](../01-Script-VM-Native-Bridge/Party-Presentation-Verbs/how-a-script-changes-the-battle-party.md) §4) - 1 when no task exists or its slot cursor has left the roster - so this returns 1 while the read-in is still rebuilding the roster, and the label fits* |

*A debug verb on the same module (added 2026-09-19, FABLE): `0050D2F0` (23 B, read whole) is `result(0x32)` of the
default dispatch table, which the bundled catalogue names `debug_setdebugpc` - it encodes the script's own actor as a
packed handle and tail-jumps into the focus's temporary controlled-actor override.*

## 8b. The secondary focus is the intervention camera's target (2026-09-19, FABLE; two bodies read whole)

`022C7FE8`, the secondary focus, has a script-side writer. **`00353530` (86 B) is the result callback of script verb
`0x2B9`, which the bundled catalogue names `setinterventioncamera`** (located by the accessor frame of
[the dispatch table](../01-Script-VM-Native-Bridge/scriptvm-native-dispatch-table.md)). It pops the actor index, then
the on flag. Flag non-zero: index to actor, actor to packed handle, handle to the setter; flag zero: the setter is
called with 0.

**The setter `00359410` (154 B).**

| call | what it does, in order |
|---|---|
| non-zero handle | a camera-side call with `(2, 1)`; **if the handle differs from the stored one**, resolve the actor and make two more camera-side calls with it; **if nothing was stored and the new handle is the leader** (`022C7FE0`), one further call; store the handle |
| zero | **if the stored handle equals the leader**, the matching call; the first camera-side routine with `(2, 0)`; store 0 |

So the leader is a special case on both sides: pointing the intervention camera at the character the player already
controls takes a different path from pointing it at anyone else. **In the 1,114 decompiled scripts the verb is called
38 times in 19 scripts - `(0, 0)` 19 times and `(1, n)` 19 times, with `n` = 1 thirteen times and 18, 22, 24, 39.**
~~*The five routines it calls (`0025xxxx`) were not read - "camera-side" is taken from the verb's name, not from them -
so what is done with the target is still open.*~~ **Read 2026-09-30 (FABLE): the five are camera routines, and the
target gets a camera context of its own.** The camera keeps two `0x860`-byte contexts at `02097D20` ([the loader-bound families](../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/loader-bound-bin-families.md): each
embeds the behind-camera object at `+0x10`, two `0xB0` pose blocks at `+0x6F0` / `+0x7A0` and their blend factor at
`+0x850`), and the camera-record stack at `02097300` ([the scripted camera player](../17-Presentation-Rendering/Scripted-Camera/the-scripted-camera-player.md), §3) holds eight `0x110`-byte records, of which a
kind-1 record follows the context its `+0xF4` names (`CameraSystem_SelectAndPublishActiveView`, `00259916`–`00259921`).

| call site in `00359410` | what it does |
|---|---|
| `00359424` (target set) / `00359499` (cleared) | record 2's context index `+0xF4` becomes 1 / 0; on a change, that context's dword `+0x854` is zeroed |
| `00359447` | zeroes context 1's dword `+0x854` |
| `00359454` | the teardown's normal entry on context 1 with the new target: the same re-seat §9 reads for context 0 |
| `00359470` | nothing was stored and the target is the leader: all `0x860` bytes of context 0 copied over context 1 |
| `0035948F` | clearing, and the stored target was the leader: context 1 copied back over context 0 |

So an intervention target gives camera record 2 its own context, seeded from the target (or copied from the leader's
context when the target is the leader), and clearing it hands record 2 back to context 0. When record 2 is the view
on screen is decided by the stack's active mask `02098DEC` and the record's kind, which this page does not follow:
GR-10. *(Answered 2026-09-30, OPUS `0b6abcf18`; register row GR-10, record [`gr10-camera-record-2-0930`](../_index/candidates/gr10-camera-record-2-0930/README.md): record 2 is the ordinary field camera, refreshed every tick, and only event cameras (records 3-7) outrank it; the intervention target is on screen from `setinterventioncamera(1, n)` until the verb's clear or a manager-0 unload, whenever no event camera is active.)*

## 9. What is not known

- ~~**What the parallel array at `+0x5A48` holds.** It is nine 2-byte records scanned by selector on
  add, while the roster/reserve queries read `+0x5A7E`. `0x5A7E − 0x5A48 = 0x36 = 3 × 18`, which is
  consistent with three more nine-entry arrays between them — **an observation, not a finding.**~~ **Answered, carried
  here 2026-09-30 (FABLE):** `+0x5A48` is **map 0, the party configuration itself** (`[0..3]` active, `[4..8]`
  reserve), and `+0x5A7E` is map 3, a battle mapping rebuilt from it; the `0x36` between them is maps 0, 1 and 2.
  §2's correction, §2b and [the five parallel slot maps](the-five-parallel-slot-maps.md) (2026-09-14 correction) establish it; §6 now says the same.
- ~~**Where the "primary index" for guests is** — `003170E0`'s placement path past the dedup scan is
  not read.~~ **Answered 2026-09-30 (FABLE), `003170E0` read whole (211 B):** past the duplicate scan over map 0
  (`00317100`–`00317113`) it walks roster indices **3, 2, 1** of map 3 from the top (`0031711A` `mov ebx, 3`;
  `00317124` base `0x5A84` = `0x5A7E` + 3 × 2; `0031714F`–`00317157` down while `ebx > 0`) and takes the first whose
  selector is `0xFF` (`00317149`/`0031714D`; a failed class-`0x17` check takes the same branch, `00317140`). None free
  returns -1 (`0031715E`). **Index 0 is never offered to a guest.** The index and the selector then
  go by tail jump (`003171AE`, final argument 1) to `PartyConfiguration_SetEmptyIndexSelector`, which writes the
  selector into a staging copy of map 0 only where that entry is `0xFFFF` and then runs the roster reconcile.
- **What `022C7FE8` (secondary focus) and `022C7FEC`, `022C8000`, `022C8004[4]` are for.** *All four answered
  2026-09-19 (FABLE): `022C8000` is the movement STOP word and `022C8004`..`022C8007` are four owner bytes of steering
  locks - [the movement locks](party-roster-and-control-suppression.md), last section.
  The same section names the other two: `022C7FE8` is the intervention camera's subject (`setinterventioncamera`)
  and `022C7FEC` a debug player-character override that no shipped script sets.*
- ~~**What `0025A6A0`'s snapshot is for** — the two teardown stubs differ only in its third argument
  (`1` / `0`, `0025A680` / `0025A690`); the 0x90-byte copy and the rest of the 395-byte body past
  `0025A743` are unread, so what kind `2` actually changes is still that.~~ **Answered 2026-09-30 (FABLE), body read
  whole (395 B):** it **re-seats camera context 0** (§8b) on the outgoing actor, in five steps: (1) the two pose blocks
  interpolated at the current factor into a local that the second interpolation overwrites before anything reads it
  (`0025A6F7`, `0025A777`); (2) the `+0x7A0` block copied over `+0x6F0`, `0xB0` bytes (`0025A6FC`–`0025A763`); (3) the
  context install from the actor (call `0025A76A`; [the focus contract](CONTRACT-party-focus-and-control-suppression.md) describes it: `0xB0` bytes from the actor's `+0xC0`
  record's `+0x138` **pointer** points to (`[[[actor+0xC0]+0x138]+0x30..+0xDF]`) into `+0x7A0`, word `+0x690` set to 4 *(wording corrected 2026-09-30, FABLE, on SWE2-AUDIT-SEM's [review](../_index/candidates/auditsem-review-dd-gameplay-0930/REVIEW.md) N2; record [`dd-gameplay-corrections-fable-0930`](../_index/candidates/dd-gameplay-corrections-fable-0930/README.md))*; a null actor, which is the no-previous-leader case,
  installs nothing); (4) the factor forced to `1.0` (`0025A77F`), the blocks interpolated again (`0025A78D`) and the
  local copied over `+0x6F0` (`0025A792`–`0025A7F9`), of which the interpolator writes only a position and a heading,
  `0x20` bytes; (5) on the alternate path only, the reset of the context's behind-camera object at `+0x10`
  (`0025A800`–`0025A809`). **So what kind `2` changes is exactly step 5:** a change to the summon party (§4) also resets
  the behind-camera object; a normal change keeps it. ~~What the installed block holds, and whether~~ Whether anything reads the
  `0x90` bytes of `+0x6F0` that step 4 fills from unwritten local space is GR-11. *(Narrowed 2026-09-30, FABLE, [record](../_index/candidates/gr19-gr11-placement-fable-0930/README.md): the first question is answered: `[actor+0xC0]` is the movement context and its `+0x138` the movement body (pool `02B4E4C0`), and `0025A180` copies that body's **placement record**, `+0x30`..`+0xDF` (position, orientation, the derived positions, displacement, cell and attribute words, flags, the radii and height copies, the inner shape, the ground heights, the requested speed; [the movement body](../06-Movement-And-Navigation/the-movement-body-pool-and-the-separation-pass.md) section 4), into the context's `+0x7A0`. Its writers are the movement body's. A sweep (`gr11_pose_readers.py`) finds no direct read of contexts 0 / 1's `+0x710`..`+0x79F`; the only direct reference, the loop `00259620`, rewrites the whole `+0x6F0` block and reads only its first `0x20` bytes. Open: whether a function handed a context pointer reads the `0x90` bytes of `+0x6F0` that the final copy fills from unwritten local space.)* **GR-11 ANSWERED 2026-09-30 (OPUS `59ec09a95`, [record](../_index/candidates/gr11-camera-context-0930/README.md); register restated 2026-10-01):** nothing reads them as values - the interpolator `00259510` and the field-tick blend `00259620` read the pose blocks only at `+0x00`..`+0x1F`, and `00259620` and the teardown `0025A6A0` rewrite `+0x6F0` whole, so `+0x710`..`+0x79F` hold stack residue no code reads (SWE2-AUDIT-SEM's F4 closes the handed-pointer path through `00259510` independently, `auditsem-review-gr19-gr11-0930`).
- ~~**Who calls the commit**, and how often — the timing of "later" in §4 is not established.~~ **ANSWERED 2026-09-18 (FABLE), statically.** `00358BC0` has no direct caller: its only reference in the image is the five-byte thunk `00358BB0` (`jmp 00358BC0`), and that thunk is called from seven sites and referenced by nothing else (no `lea`, no data pointer). Three are the per-mode frame bodies, one call each per frame: `0022A770` (`0022AE3C`), `MainLoop_UpdateAndRenderFrame` `0022B8C0` (`0022BAF9`) and `0022BC20` (`0022BD49`), all three dispatched from `0022A580`; so "later" is the same frame's commit point, once a frame. The other four are the actor system's manager initialisation `0026CE60` (`0026D2CF`, run by the drain `0025BFB0` and by `0032F1B0`), the field runtime pass helper `0025C830` (`0025D424`, from `0025C170`), `0026C3E0` (`0026C5A3`, from `0026C3B0` / `0026C3C0` / `0026C5C0`) and the script verb `debug_setpc` (`0x2021`), whose handler `PartyRoster_AssignActorAndCommitFocusWhenEligible` `0050C610` commits at `0050C64B` right after assigning; that verb has no `us` script use. Static, the call graph and a reference sweep.
- ~~**What `DAT_02089340 & 0x10` gates** in `BattleUnit_GetPartyLeader`; `O-3` already asks about bit
  `0x40` of the same word.~~ **Answered, carried here 2026-09-30 (FABLE):** bit 4 is **"the area's battle state is
  live"** — set by the area-state initialiser, cleared by the area-teardown reset, and tested at fifty sites that all
  answer "nothing" while it is clear ([the world tick](../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md) §2.5, row 4, gives the set and clear instructions). Here it is the
  test at `003272A9`: outside a live area there is no leader. (`O-3`, about bit `0x40`, is ANSWERED: a treasure is
  being opened.)
- ~~The remainder of `PartyRoster_AssignActorToSlot` (`00269C70`) — **`O-6`, still open.**~~ **O-6 ANSWERED 2026-09-12 in the register, carried here 2026-09-18 (FABLE):** after the eviction and clear, `roster[slot] = actor`, `+0x12 = slot`, `+0x0F = 2` (slots 0..3) or `3`, the new occupant's `+0x152 = 0` and notice, then a focus request through `PartyFocus_RequestPackedActorHandle` when no focus handle is set (`00269CE1`..`00269D41`; the party contract §7 reads the same).

## 10. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Nine 2-byte records; 0–3 roster, 4–8 reserve | `0031B510` loop `cmp ebx,4`, base `0x5A7E`, stride 2; `00321100` loop `cmp ebx,9` from base `0x5A86` | 1 |
| `0xFF` is the empty selector | `cmp byte …, 0xFF ; je` in both | 1 |
| Party-configuration class is `0x17` | `lea ecx,[r8+0x17]` before `call 0x322C50` in both | 1 |
| Guests are selectors 7–25 | `sub cl,7 ; cmp cl,0x12 ; setbe` in `00322350`, and the same test opening `003170E0` | 1 |
| Members are 0–6 and go to indices 4–8 | `cmp cl,6 ; jbe` in `003172E0`, then `call 0x321100` | 1 |
| Add is rejected if the selector already exists | the nine-entry scan at `+0x5A48` then `jns` to the failure return | 1 |
| The leader is `DAT_022C7FE0`, derived not stored | `003590D0` is two instructions; `003272A0` resolves it per call | 1 |
| 25 callers of `BattleUnit_GetPartyLeader`, 9 in Movement | direct-and-thunk caller census | 1 |
| Exactly three in-census writers of the handle | rip-relative sweep over the function list | 1 |
| `003594C0` is the only writer of kind `2` | unbounded `.text` scan, then the function decoded from its first byte | 1 |
| The commit re-reads the pending handle after teardown | `mov ecx,[022C7FE4]` at `00358C24`, after the teardown calls | 1 |
| `00320800` keeps a selector of 6 or below, or `0x1A`..`0xFE` (added 2026-09-30) | `00320852`/`00320855`, `00320857`–`0032085C` | 1 |
| The reserve probe returns an index that fails the class check (corrected 2026-09-30) | `0032112E`/`00321130` → `00321158`; the roster read skips instead, `0031B553`/`0031B555` | 1 |
| A guest takes the first free roster index of 3, 2, 1, never 0 (2026-09-30) | `003170E0` read whole: `0031711A`, `00317124`, `00317149`/`0031714D`, `0031714F`–`00317157`, tail `003171AE` | 1 |
| `0025A6A0` re-seats camera context 0; kind 2 adds only the behind-camera reset (2026-09-30) | body read whole, anchors in §9; the context's layout from the loader-bound families page; the install and interpolator bodies read whole today | 1 |
| The secondary focus drives camera record 2 and context 1 (2026-09-30) | `00359410` and its five callees read whole, §8b's table; the kind-1 arm `00259916`–`00259921` | 1 |
| Kind 2 is reached from `changetosummonparty` in shipped scripts (2026-09-30) | the focus contract PF-6; raw call index (one `jmp` site into `003594C0`); `grep -F "changetosummonparty("` over the 1,114 decompiled `us` scripts: 13 calls in 13 files | 1 |
| Bit `0x10` of `02089340` is the area-battle-state-live bit (carried 2026-09-30) | `003272A9`; the world tick §2.5, row 4 | 1 |

**Controls.** The claim *"nothing is notified on a leader change"* is bounded by what was read: the
commit's body contains no callback list, dirty flag or event dispatch, and every consumer examined
derives the leader on demand. It is **not** a claim that no consumer caches it elsewhere. *One consumer that
keeps its own copy is known (noted 2026-09-30, FABLE): the render layer writes the focus actor's slot into its own
record from the getter each time it runs (the Presentation crossing at the end of this page), so it too derives the
leader rather than being told.*

The count of handle writers is stated twice on purpose — **three within the function-list census,
four in reality** — because the difference is the finding in §4, not a correction to be tidied away.

`check_already_answered.py` was run before this document was started and returned *"no existing
coverage found — the block is new"* for the `PartyConfiguration` addresses.

**Address review flags — dispositioned.** `verify_doc_addresses` reports five `.text` non-function
addresses: `003594C0`, `003594C7`, `003594C9`, `003594CF`, `003594D3`. **All five are the unlisted
function of §4 and its instructions**, and the flag is correct: they are not function entries
*because the function list does not contain this function*. The bytes are real code — decoded from
`003594C0`, a clean `movzx / test / movzx / cmovne / mov / ret` ending in `int3` padding, entered by
nothing else in range.

> **The checker and the census fail here for the same reason, and that agreement is the evidence.**
> A flag saying "this is not a function" and a census that could not see the writer are two
> instruments reporting the same gap in the function list, not two separate problems. The finding is
> kept as a citation with this disposition rather than removed to clear the flag — **removing it
> would delete the only record of the only writer of request kind `2`.**

## 11. Related

- [`party-roster-and-control-suppression.md`](party-roster-and-control-suppression.md) — the four-pointer roster, the actor's own slot field, and control suppression; this document answers its `O-5`.
- [`license-check-what-the-board-actually-tests.md`](../12-Items-Equipment-Shops-License/license-check-what-the-board-actually-tests.md) — the shared class validator, and where the member/guest split is consumed.
- [`battleunit-slot-pool-and-actor-class.md`](../04-Actor-Entity/battleunit-slot-pool-and-actor-class.md) — the 32-slot battle pool party, guests and enemies all draw from.

## Falsification pass 1 — 2026-09-13 (OPUS)

| claim | measured |
|---|---|
| the five bases `0x5A48`, `0x5A5A`, `0x5A6C`, `0x5A7E`, `0x5A90`, exactly `0x12` apart | **all five appear in `0031B9F0`**, and all four gaps are **`0x12`** |
| `0x5A86 − 0x5A7E = 8 = 4 × 2` | exact, and each function uses **only its own** displacement — `0031B510` sees `0x5A7E`, `00321100` sees `0x5A86`, neither sees the other |
| every name in §5's table | **16 of 16** match `functions.tsv`, including both `AddSelector…` names in full and `00322C50` as `BattleEncodedId_IsValidForClass` |
| `003590D0` is `return DAT_022C7FE0` | `mov eax, dword ptr [rip…]` → `022C7FE0`, then `ret` — two instructions |
| `003594C0` is **absent from the function list** | **confirmed absent**, and it is 27 bytes as § says |

### The stride is the array, so the five maps are contiguous

`0x12` = 18 = **9 slots × 2 bytes** — the distance between consecutive bases is exactly the size of
one map. So the five are not five arrays *somewhere* `0x12` apart; they are **one contiguous 90-byte
block of 45 two-byte slots**, `+0x5A48` through `+0x5AA1`, with no padding anywhere in it.

That is the check that turns "five bases `0x12` apart, nine slots each" from two independent numbers
into a layout: if the stride exceeded the content there would be gaps, and if it fell short the maps
would overlap. It does neither.

### Why the census could not see `003594C0`, concretely

§ says the function is "absent from the function list" and draws the right lesson. The shape of the
hole is worth recording:

```
003594B0  PartyFocus_RequestPackedActorHandle   14 bytes, ends at 003594BD
003594BE  int3  int3                            padding
003594C0  <the kind-upgrade function>           27 bytes, ends at 003594DA
003594DB  int3 x5                               padding
003594E0  PartyControl_BuildAnalogMovementVectorFromInputHistory   the next listed entry
```

**It sits in a 34-byte gap between two listed entries, bracketed by `int3` on both sides** — a
complete, padded, ordinary function that the list simply does not contain. Not an alignment artefact,
not a fragment of its neighbour: `003594B0` ends nine bytes before it starts.

*(`progress.py` reports the same shape in aggregate: the function list covers 92.91 % of its own
span, with 31,933 regions and 568,793 bytes between listed bodies. This is one of those regions, and
it held the only writer of the value § was looking for.)*

### The elided instruction is the one that carries "does nothing otherwise"

§'s excerpt runs `003594C9` → `003594CF`, skipping one instruction:

```asm
003594C9  movzx  eax, cl
003594CC  mov    r8d, edx        ; <- elided in the excerpt
003594CF  cmovne r8d, eax
003594D3  mov    byte ptr [022C7FF8], r8b
```

`cmovne` overwrites `r8d` only when the kind is non-zero, so on the zero path the store writes back
**whatever `r8d` already held** — and `mov r8d, edx` is what puts the *current* kind there. Without
it the zero path would store an undefined register. **The instruction the excerpt omits is precisely
the one that makes "and does nothing otherwise" true**, which is worth having in the listing of a
function whose whole point is that conditional.

**Not claimed:** nothing here was executed or observed live. ~~Who calls `003594C0`, and therefore
whether `2` ever actually reaches it, is not established here~~ *Answered 2026-09-30 (FABLE): the verb
`changetosummonparty`'s result callback, which shipped scripts call 13 times (§4)* — § reaches "the only path to kind 2"
by exhausting the *writers*, which is a different and weaker statement than showing a caller passes
`2`. §§2b, 3 and 4's commit sequence were not re-derived.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL and recorded in the registry.*

- **Spawn_Encounter_Lifecycle — CLIENT.** `BattleUnit_GetPartyLeader` (`003272A0`) is read by
  `Spawn_TrySelectCandidatePosition` and `SpawnLifecycle_CheckAndRetireByNativeRange`. So those two spawn functions follow
  whoever is leader at the moment they run.
- **Audio — CLIENT.** `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`) is read by a 1,036-byte Audio-filed body.
  That body converts the focus actor's world position with `atan2f`, which reads as positional sound placement. ~~The
  body is not read.~~ *It is the audio listener update, read on [the world tick](../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md) §7 (EX-3): it resolves the focus actor,
  reads the camera matrix, forms the offset and its `atan2f` heading, and writes the listener block (carried here
  2026-09-30, FABLE).*
- **PlatformOnlineAchievements — SERVICE.** `BattleUnit_ProcessDefeatRewardsAndLoot` (`00312280`) calls the achievement
  counter updater (counters 11 and 4,
  [the achievement catalogue](../20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md) AB-7).
- **Gameplay - SERVICE (18 edges).** `0030D160`, `00310DB0` reach bodies filed to Gameplay: `00316CD0` (Combat), `00316CF0` (Combat), `00316D70` (Combat) - shared machinery across the layer boundary, no shared ownership.
- **Items_Equipment_Shops_License - CLIENT and SERVICE (14 edges).** `00322C50` is also called by bodies filed to items/equipment: `003096F0`, `0030B180`, `0030B4B0`; `0030FD10` reaches bodies filed to items/equipment: `0031A630` - shared machinery across the layer boundary, no shared ownership.
- **Movement - CLIENT and SERVICE (66 edges).** `002681D0` is also called by bodies filed to movement: `002E3500`; `0022B8C0`, `0022BC20` reach bodies filed to movement: `00263560`, `0037CF00` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (40 edges).** `0026C3B0`, `0026C5C0`, `0026D6D0` are also called by bodies filed to script VM / native bridge: `00346D80`, `00352560`, `00347090` - shared machinery across the layer boundary, no shared ownership.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Status_Periodic_Terminal — CLIENT and SERVICE.** Cited party functions are called by `BattleUnit_RunPeriodicCombatMaintenance` (2), `BattleStats_ChangeStatusAndProcessSideEffects`, `BattleStats_RecomputeDerivedStateAndAutoStatuses` and `BattleStats_ModifyStatusLayerStateAndProcessSideEffects`. They call `BattleUnit_ResolvePeriodicPrimaryResourceRecoveryStep` and `BattleFormula_BuildPeriodicStatusResult`.

## Crossings into other layers — FINAL-AUDIT pass 22 (OPUS, 2026-09-18)

**Resource — this page is the CALLER, three edges into one entry.** The three bodies this page
cites each call `00324510` exactly once: `0022A770` at `0022AE6F`,
`MainLoop_UpdateAndRenderFrame` (`0022B8C0`) at `0022BAEF`, and `0022BC20` at `0022BD3F`.

**One entry, three callers, and the callee decides nothing about the party.** `00324510` opens by
loading the mode dword at `022C27A0` and switching on it — `sub ecx, 1` / `je`, `sub ecx, 1` / `je`,
`cmp ecx, 1` / `jne` (`00324516`–`00324529`) — so what it does is chosen by a global mode, not by
anything the caller passes. That one of the three callers is the frame loop itself makes the shape
plain: **this is a per-frame resource step the loop and its two siblings drive, and the party
reserve is not its subject.**

**This page owns nothing in Resource.** The crossing is that the bodies documented here call into
it, which is the direction worth stating: the page is consulted by nobody in that layer.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Input — SERVICE.** `003594E0` on this page calls `FUN_0017dfc0`, owned by that layer. What it reaches is a 67-byte query that takes the singleton's `[+0xDF8]` member and asks with the constants **2 and 3** before folding the answer; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Rewards_Progression_Economy — CLIENT (15 edges through 4 of this page's functions).** The Rewards_Progression_Economy layer reaches this page at `00312280`, `00310DB0`, `00320AB0`, `002F8BB0`. `Reward_ComputeExperienceForRecipient` is the worked example, read in full - it is the experience computation for one recipient: it needs `byte[rec+5] == 0` and takes its context from `0031B860`; **5 of the 13 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — CLIENT.** `BattleMenu_BuildCommandEntryList`, owned by that layer, calls `00322C50` on this page. That caller is the command-list build, and the ceiling is in the first instruction: the menu kind is bounded at **`0x22`** into a jump table, after which `dword[+0x40]` is zeroed and `dword[+0x44]` set to `-1` before any entry is written; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatFormula — SERVICE (SWE2-CONTRACT 2026-09-15, 12 edges).** The leader-change path drives the stats layer:
`00310DB0` calls `BattleFormula_ResolveTargetResult`, `BattleFormula_ApplyTargetResult`,
`BattleStats_ModifyPrimaryResource` and `BattleStats_GetOwningActorHandle`; `002F8BB0` calls
`BattleStats_FindOwningBattleUnit`; `BattleStats_GetByMappedBattleSlot` `00320AB0` trades calls
with six of the page's bodies; `00322C50` is shared with `BattleStats_RebuildEffectiveStatsAndAffinityState`.
A real consumption crossing — the roster change reseats battle stats through these calls.

**CombatAI — CLIENT and MECHANICAL (SWE2-CONTRACT 2026-09-15, 12 edges).** `00310DB0` calls
`BattleEnmity_UpdatePeriodicDecay` (leader change decays enmity); the other 11 edges are the
`BattleEnmity_*` family and `AiOrder_EvaluateTargetSelector`/`GambitConfig_*` sharing `00322C50`/
`003272A0`. One real call plus fan-in.

**Presentation — SERVICE on twelve edges, CLIENT on one (13 edges; the accessor and two callers read
in full).** Twelve of the thirteen are one function: `PartyFocus_GetCurrentPackedActorHandle` on this
page, which is **two instructions** — `mov eax, [022C7FE0] / ret`. Twelve presentation bodies read
it, and two of them show what for. `RenderSystem_UpdateCharacterRecords` and
`CharacterRenderSystem_UpdateLODAndRenderState` are the same six lines each: call the accessor, and
if it answers **zero** write `-1` into `word[[022C6F28] + 0x4882C]`, otherwise convert the handle
through `002E9B80` and write that instead. So the render layer keeps its own copy of who the party
is focused on, and **a zero handle is stored as `0xFFFF`, not as zero** — the render record has no
"nobody" that looks like slot 0. The remaining ten callers are the rest of that layer reading the
same global through the same two instructions.

The one edge in the other direction is `BattleUnit_ProcessDefeatRewardsAndLoot` calling
`Reward_PublishExpLpPresentation`, which needs the HUD object at `[0209BE80]` and works its
`+0x5380` sub-object; it does nothing at all if that object is null.

So the crossing is **one shared read with twelve callers on that layer**, not twelve relationships,
plus one publish. Edge count from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).
