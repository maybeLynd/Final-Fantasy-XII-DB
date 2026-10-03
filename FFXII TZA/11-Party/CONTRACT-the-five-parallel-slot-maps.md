---
contract: Resolve a battle slot through one of five parallel nine-entry maps that are born identical and are not peers afterwards
category: 11-Party
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: 11-Party/the-five-parallel-slot-maps.md
entries: ["0031B9F0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's invariants measured from the
    shipping bytes — the resolver read in full with **both refusal paths traced to the one epilogue
    they share**, the id gate's registry class read at its `lea`, and the refresher's copy order read
    instruction by instruction so that **which map is copied before the clear and which after** is a
    reading rather than an inference. **This records checks performed on that date, not the method of
    the original derivation**, which is on the slot-maps page; see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-slot-maps-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — the five parallel slot maps

> **Authored 2026-09-22 by FABLE.** S-28's binding gap is *"slot assignment only, of 4 pages"*. Two
> of the four are contracted; **this takes the third.**
>
> Written against FRONTIER's adequacy test: *a narrower contract is adequate exactly when the
> system's operations have no cross-operation invariant or ordering it leaves unstated.* A contract
> on the resolver alone would be **inadequate by that test**, because what the resolver returns
> depends on a rewrite performed by a different body in a specific order — which is `SM-5` and
> `SM-6`, and neither is visible from the resolver.

## 1. Purpose

Turn a definition id into a battle slot, through whichever of five parallel maps the caller's class
selects.

## 2. Interface

`BattleSlotMap_ResolveMappedBattleSlot` (`0031B9F0`), **200 B**, `(id in ecx, class in edx)`,
returning a byte. The five maps live in the battle-state block reached through the pointer global
`02EBF190`.

## 3. Types

```
[02EBF190] -> the battle-state block
  +0x5A48  u16[9]   map 0   \
  +0x5A5A  u16[9]   map 1    |  five maps, 0x12 apart, nine u16 selectors each
  +0x5A6C  u16[9]   map 2    |  an empty selector is 0xFFFF
  +0x5A7E  u16[9]   map 3    |
  +0x5A90  u16[9]   map 4   /
  +0x5AA4  u32      the source table's first byte — NOT part of any map (SM-8)   <- corrected 2026-10-02, OPUS - answered: the preferred definition selector, the party leader (the field map's +0x5AA4 row)
```

## 4. Preconditions · postconditions · invariants

### The eight cross-operation invariants

**SM-1 — Five bases exactly `0x12` apart, and the resolver returns only the LOW BYTE of a `u16`
selector.** `0031BA3D movzx eax, byte ptr [rax + rdi*2 + 0x5a90]` is the fifth arm: the index is
scaled by **2**, so the entries are `u16`, but the load is a **byte**. *A reimplementation that
returns the whole selector is wrong wherever the high byte is non-zero, and the maps' empty value
`0xFFFF` makes that byte non-zero on every empty entry.*

**SM-2 — TWO different failures return `0xFF`, through ONE shared epilogue, and nothing tells them
apart.** The id gate at `0031BA0D`/`0031BA0F` **falls through** into `0031BA11 mov al, 0xff`; the
class chain's last test `0031BA34 jne` **jumps backwards to the same instruction**. *So "invalid id"
and "class outside 0–4" are indistinguishable to every caller, and `0xFF` is also a legal low byte
of a selector — the refusal is not reserved.*

**SM-3 — The id gate is registry class `0x17` (23), and it is a LIVE arm.** `0031BA04 lea ecx,
[r8 + 0x17]` then `BattleEncodedId_IsValidForClass`. *That matters because not every arm of that
function is live*: the class whose registry slot is `02EBF0D0` is installed by **nothing** in the
image, so its id range is empty and its arm always refuses
([the registry band ruling](../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md)).
**Class 23's slot is one the binder does install**, so this gate can genuinely both pass and refuse.

**SM-4 — All five maps are born IDENTICAL, by one copy repeated four times.** The initialiser fills
only map 0 — nine entries from an authored byte table — and then copies it as **16 bytes plus a
trailing 2** into maps 1, 2, 3 and 4. *They are not five assignments; they are one assignment and
four duplicates.*
**Born identical, but not necessarily born from the table: the fill is conditional per entry** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 338, which executed it; `00329CF0`–`00329DAE` re-read.)*. For each of
the nine entries of the authored table at `01EED260`:
- **`0xFF` (no member).** After two validity checks, the body releases the member the slot's OLD selector names
  through the definition-runtime release. It writes `0xFFFF` only when that old low byte is `<= 0x27` (`00329D2C`–`00329D32`).
- **A member id.** It is activated and written only when valid and `<= 0x27`.
- **Anything else.** The entry is skipped: a failed validity check, a stale old selector above `0x27`, or an id
  above `0x27`.

A skipped slot keeps its old selector, and the copy then carries it into maps 1–4. *Over a zeroed region the maps
are born from the table exactly as stated above. Over a region holding a stale selector above `0x27`, that
selector survives into all five.*

**SM-5 — They diverge in exactly one body, and the ORDER of its copies is the whole invariant.**
`BattleGroup_RefreshFourActorDefinitions` (`003266C0`) takes map 0's base and works through it:

| step | instructions | effect |
|---|---|---|
| copy map 0 → map 1 | `00326714`–`0032671B` | map 1 = map 0 |
| copy map 0 → **map 3** | `00326720`–`00326724` | **map 3 = map 0, taken BEFORE the clear** |
| clear map 1's tail | `00326728`–`00326730` | `[4..7]` set to `0xFFFF` by **one qword store**, `[8]` written separately |
| copy map 1 → maps 2 and 4 | `00326735`–`0032674B` | **maps 2 and 4 inherit the CLEARED map 1** |

> ~~**So after a refresh the five are two groups, not five variants: map 3 still equals map 0, while
> maps 2 and 4 equal the cleared map 1.**~~ **After the ordered copies map 3 equals map 0 and maps 2 and 4 equal the
> cleared map 1. The refresh is not over there** (2026-09-29, OPUS falsification pass 1, `CON-169`): the body then switches on
> `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` (`0032674F`).
>
> | mode | arm | what it does to the grouping |
> |---|---|---|
> | 0, or anything above 5 | `00326A34` | nothing; the two groups stand |
> | 1 | `003269D2` | rewrites entries of maps 1, 2 and 4 among `[0..3]` |
> | 2 | `00326991` | rewrites `[0..3]` of maps 1 and 2 and entry 3 of map 4; map 1 and map 4 entry 3 become `0x1A` |
> | 3 | `003268F3` | **restores map 4 from the copy taken before the refresh** (`003268FD`), then rewrites `[0..3]` of maps 1 and 2 and one entry of map 4 |
> | 4 | `0032683F` | rewrites `[0..3]` of maps 1, 2 and 4 |
> | 5 | `00326783` | **restores map 4 from the copy taken before the refresh** (`003267F3`), then rewrites `[0..3]` of maps 1 and 2 |
>
> **What holds in every mode:**
> - map 3 equals map 0, because no store after `00326724` reaches it;
> - maps 1 and 2 hold `0xFFFF` in `[4..8]`, because every mode arm writes only `[0..3]`.
>
> Map 4 holds `0xFFFF` in `[4..8]` in modes 0, 1, 2 and 4. In modes 3 and 5 it keeps whatever it held before the
> refresh. No store after the arms rejoin at `00326A34` touches the maps. *A port that copies map 0 into all four and then clears 1,
> 2 and 4 produces the same bytes today and is wrong about the mechanism — it would diverge the
> moment the cleared value or the cleared range changed, and it gets map 3 right only by accident.*

**SM-6 — The five are NOT peers.** Map 0 is the **live party configuration** — `[0..3]` active,
`[4..8]` available — addressed by the block reset and the `PartyConfiguration_*` family. Maps 1–4 are
**battle mappings derived from it**. *Class 0 of the resolver therefore returns the low byte of a
live party selector, and classes 1–4 return bytes of a derived copy.*

**SM-7 — ~~Map 0 has writers that do NOT touch maps 1–4, so the derived maps are STALE until the
refresher runs.~~ A removal rebuilds all five maps before it returns, except when a 32-entry pool is full** *(2026-09-25, FABLE, Claude Opus 5.5, on [OPUS block 340](../_index/candidates/s28-opus-replay-slot-map-writers/README.md), which executed both removers; the reconcile body's tail and its pooled-task route re-read.)*
~~The two selector-removal bodies range-check a member id (`≤ 6` party,
`7…0x19` guest), scan map 0's nine entries for a matching low byte and clear that slot to `0xFFFF`.
**They rewrite map 0 only.** *So between a removal and the next refresh, a class-2 or class-4 lookup
returns a slot for a member map 0 no longer lists — which is a real intermediate state and not a
race, because both happen on the same thread.*~~ The two selector-removal bodies range-check a member id (`≤ 6`
party, `7…0x19` guest) and find its slot in map 0. The remover then works in this order:
1. It copies the map to the staging pair at `022C2580` and clears the slot to `0xFFFF` **there**.
2. It releases the member.
3. It calls `PartyConfiguration_ReconcileRosterFromCurrentSelectors(0)`. That body compacts the staged selectors
   and writes map 0 back through the per-index setter. Removing member 2 from `0..6` gives
   `0, 1, 3, FFFF, 4, 5, 6`, so the active part closes up.
4. With argument 0, the reconcile body skips its direct refresher call (it tests the complement of bit 0) and
   calls a pooled-task helper instead. That helper takes a slot from a 32-entry pool (bitmask `022BE7C0`). When it
   gets one, it tail-jumps into a three-call tail whose middle call is the refresher `003266C0`. So maps 1–4 are
   rebuilt in the same call.

OPUS measured the whole sequence for both removers. **No stale window follows a removal.** *Read here and not
executed: when all 32 pool slots are taken, the helper returns without the tail-jump. Map 0 is then rewritten and
maps 1–4 are not, which is the stale state this invariant used to describe, now reachable only on that path.*

**SM-8 — `+0x5AA4` is adjacent and is not a map.** It is a `u32` holding the source table's first
byte. *It sits immediately past map 4's eighteen bytes and a census over the five ranges will pick
it up; it belongs to none of them.*

## 5. State

**Owned:** nothing — the maps live in the battle-state block, which is part of the save image.
**Read:** all five, by class. **Written:** map 0 by the party family and by the initialiser; maps 1–4 ~~only by the
refresher~~ by the initialiser's copy (`SM-4`) and by the refresher, whose mode arms also write them (`SM-5`, `CON-169`).

## 6. Relationships

| | |
|---|---|
| **Sibling** | [`CONTRACT-party-slot-assignment.md`](CONTRACT-party-slot-assignment.md) — S-28's first |
| **Sibling** | [`CONTRACT-party-focus-and-control-suppression.md`](CONTRACT-party-focus-and-control-suppression.md) — S-28's second |
| **Diverged by** | `BattleGroup_RefreshFourActorDefinitions` (`003266C0`) — `SM-5` |
| **Gated by** | `BattleEncodedId_IsValidForClass`, class 23 — `SM-3`. *Named, not cited: it is a hub and this contract reads only its call site.* |
| **Structure owned by** | [the battle state block field map](Battle-State-Block/the-battle-state-block-field-map.md) — S-28's fourth page, uncontracted, and this document does not claim it |

## 7. State transitions

*initialise map 0 → duplicate into 1, 2, 3, 4 (all identical) → refresh: 0→1, 0→3, clear 1's tail,
1→2, 1→4, then the mode's rewrite of maps 1, 2 and 4 (`SM-5`, `CON-169`) → resolve by class.* Map 0 may be rewritten by the party family at any point, which moves
the maps out of the relation `SM-5` established until the next refresh (`SM-7`). *(A removal refreshes in the
same call; SM-7, corrected 2026-09-25.)*

## 8. Script · resource · event interactions

The initial map comes from an authored byte table. The refresher's per-mode rewrite is keyed by the
battle runtime mode, read through `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15`.

## 9. Determinism

Deterministic. No generator is drawn.

## 10. Failure paths and edge conditions

- An invalid id and a class outside 0–4 both return `0xFF`, indistinguishably (`SM-2`).
- `0xFF` is also a legal low byte, so the refusal is not a reserved value (`SM-2`).
- ~~A removal leaves maps 1–4 stale until the refresher runs (`SM-7`).~~ A removal leaves maps 1–4 stale only
  when the pooled-task helper's 32-entry pool is full (`SM-7`, corrected 2026-09-25 on OPUS block 340).

## 11. Observable behaviour

None directly. This is the table behind "which character is in which battle slot", and the visible
consequence of getting `SM-5` wrong is a party member appearing in the wrong slot in one battle mode
and not another.

## 12. Reproduction formula

Resolve with a class of 5 and with an invalid id and assert **both** return `0xFF` (`SM-2`). Fill map
0, run the refresher, and assert **map 3 equals map 0 while maps 2 and 4 have `0xFFFF` in `[4..7]`**
(`SM-5`) **in mode 0**. In modes 3 and 5, assert instead that map 4 keeps its pre-refresh bytes in `[4..8]`; in
every mode, map 3 equals map 0 (`CON-169`). ~~Remove a member and assert map 0 changed and maps 1–4 did not (`SM-7`).~~ Remove a member and assert that all
five maps changed and that map 0's active part closed up. Then fill the pooled-task helper's pool (`022BE7C0`) and
assert that maps 1–4 do not change (`SM-7`, corrected 2026-09-25). Read entry `[8]` of
a map with a high byte set and assert the resolver returns only the low byte (`SM-1`).

## 13. Runtime validation

~~**None.** No experiment executes this body.~~ *(answered: the resolver is not executed, but the initialiser and both removers were — OPUS blocks 338 and 340, SM-4 and SM-7; 2026-10-02, OPUS)* S-28's runtime cell is not addressed by this contract.
*Stated rather than left blank so a CONTRACT READY header is not read as evidence of execution.*

## 14. Unresolved

- **Corrected (2026-09-29, OPUS falsification pass 1, `CON-170`).** Two statements in this item are wrong.
  - The table is `01EED260`, not `0x01EC9260`: `00329CE1` and `00329DBB` both address it.
  - Maps 1–4 are not "frozen snapshots" that "receive bytes nowhere else" and stay "permanently identical to
    each other". The refresher `003266C0` writes all four (`SM-5`): map 3 then differs from maps 1, 2 and 4.
    The census missed it because the refresher addresses the maps through `rdi = [02EBF190] + 0x5A48`
    (`003266C8`, `003266D4`). Its stores are small displacements from `rdi`, not `+0x5A4x` displacements from the
    block.

  The call-site census of the classes below is not affected.
- ~~**What the five classes MEAN.**~~ — **resolved 2026-09-23 (SWE2-CONTRACT) at the mechanism level:
  class 0 is the live map and classes 1–4 are four frozen snapshots of it.** The writer census
  proves the asymmetry: `00329CC0` rebuilds **map 0** slot-by-slot from the authored selector
  table at ~~`0x01EC9260`~~ `01EED260` *(corrected 2026-10-02, OPUS: `00329CE1`, `00329DBB`; nothing references `01EC9260` — the item above)* (nine slots, each gated through `00322C50` kinds `0x17`/`2`, resolving
  `block[0x5A48 + i*2]` selectors into `id*0x1C8` unit records), then writes `block+0x5AA4` and
  copies map 0 **verbatim into maps 1, 2, 3 and 4** (`movups` + word-tail sweep at
  `00329DF6`–`00329E27`). The only other map write is ~~`003290BD`~~ `00329080` *(corrected 2026-10-02, OPUS: `003290BD` is an instruction inside `00329080`; its stores are `00329122` and `00329176`)*, which mutates **map 0 only**
  (indexed `[block + i*2 + 0x5A48]` selector stores at `00329122`/`00329176`). So through every
  displacement-addressed route maps 1–4 ~~receive bytes nowhere else — they are the same snapshot~~
  ~~taken at the last refresh, permanently identical to each other, diverging from map 0 only when~~
  ~~`003290BD` runs (the `003266DB` caveat is item 2's).~~ *(corrected 2026-10-02, OPUS: the refresher `003266C0` writes maps 1–4 through `rdi` and its mode arms make them differ — SM-5, CON-169, CON-170)* Call-site census: literal classes
  used are **0** (`0030FD44`'s `xor`, `002738B8`'s), **1** (direct `0030A707`, plus
  `002F8C4E`/`0030C337`/~~`00311A17`~~ the status function's call *(corrected 2026-10-02, OPUS; address in FABLE's record readiness-apply-fable-1002)*), **2** (one site, `0035BDBE`), and **3** (the dominant class —
  ~19 sites *(corrected 2026-10-02, OPUS: 24 — 20 through `00320AB0`, one of them after `0050FF39 mov ebx, 3`, and 4 through `00320040`)* through wrappers `00320AB0`/`00320040`, which forward `edx`/`ecx` respectively);
  **class 4 has no literal call site** — reachable only through computed `edx` at `0030A804` ~~and~~
  ~~the `0050FD1A` family~~ *(corrected 2026-10-02, OPUS: `0050FD15 mov edx, 3` and its siblings pass class 3)*. What the class byte *is* semantically (which roster generation a caller
  intends) stays open — but structurally classes 1–4 read the same frozen bytes.
- ~~Whether any write reaches maps 1–4 through a computed pointer.~~ — **answered (2026-09-29, OPUS falsification pass 1, `CON-170`):
  yes, and it is the refresher itself. `003266DB` is not a separate handler.**
  - It is an instruction inside `003266C0` (`mov [rsp + 0x68], r12`), and no branch in the image targets it.
  - The two `.rdata` records naming it are unwind metadata, not a dispatch table. `.pdata` splits the
    refresher's shrink-wrapped prologue into fragments `003266CF`–`003266DB` and `003266DB`–`00326A40`. Each
    fragment's UNWIND_INFO carries the chain flag and chains back, through `003266CF`, to `003266C0`.
  - The "caller-supplied record" is the block's own maps, because `rdi` is loaded from `02EBF190` before
    `003266DB`.

  The runtime-identity residual below does not exist.
  ~~**bounded 2026-09-23
  (SWE2-CONTRACT): the route exists in exactly one body, and whether it ever targets the block
  is the residual.**~~ A whole-`.pdata` census of displacement-addressed writes in `[0x5A48,
  0x5AA4)` finds exactly **two** writers: `00329CC0`'s unindexed `movups` sweep into all of maps
  1–4, and ~~`003290BD`'s~~ `00329080`'s indexed writes into map 0 only. ~~But one registered handler escapes that~~
  ~~census: `003266DB` (dispatched via `.rdata` records — two identical `{rva32, aux}` slots — no~~
  ~~direct caller) shuffles a **caller-supplied five-map record** with the identical `0x12` stride~~
  ~~layout (`[rdi]`→`[rdi+0x12]`, `[rdi]`→`[rdi+0x36]`, `[rdi+0x12]`→`[rdi+0x24]`/`+0x48`) while~~
  ~~reading the *block's* map-0/`+0x5AA4` through `*(02EBF190)`. If the dispatch machinery ever~~
  ~~hands it `block+0x5A48`, its writes land in the block's maps 1–4 — the computed-pointer write~~
  ~~the item asks about. What record the dispatch hands it is a runtime-identity question the image~~
  ~~does not answer.~~ *(corrected 2026-10-02, OPUS: `003266DB` is `mov qword ptr [rsp + 0x68], r12` inside `003266C0`, the `.rdata` records are its unwind data, and `003290BD` is an instruction inside `00329080` — the answer above, CON-170)* Everything else is closed: all indexed `[reg + i*2 + 0x5A4x]` writes land in
  map 0, and all map-1–4 reads are `movzx`/`cmp`.

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| `SM-1` — `u16` stride, byte load | `0031BA3D` read at the instruction: index scaled by 2, load size 1 | 1 |
| `SM-2` — one shared refusal | `0031BA0F` traced as a fallthrough into `0031BA11`, and `0031BA34` as a backward jump to the same instruction | 1 |
| `SM-3` — class 23, and the arm is live | `0031BA04` read at its `lea`; the liveness from this session's measurement that the binder installs class 23's slot and installs nothing into `02EBF0D0` | 1 |
| `SM-5` — the copy order | `00326714`–`0032674B` read in sequence, with the clear at `00326728` shown to fall **between** the map-3 copy and the map-2/4 copies | 1 |
| `SM-4`, `SM-6`, `SM-7`, `SM-8` | [the slot-maps page](the-five-parallel-slot-maps.md), falsified 2026-09-03 and corrected 2026-09-14 | 1 |
| ~~maps 1–4 are verbatim snapshots of map 0, refreshed by `00329CC0` and otherwise unwritten~~ **corrected: `00329CC0` copies map 0 into maps 1–4, and the refresher `003266C0` then rewrites them (`CON-170`; `falsify_slot_maps.py` K1, K2)** | writer census over all `.pdata` bodies 2026-09-23: `00329CC0` copies map 0 into maps 1–4 at `00329DF6`–`00329E27` after rebuilding map 0 from the selector table ~~`0x01EC9260`~~ `01EED260`; ~~`003290BD`~~ `00329080` writes map 0 only; ~~`003266DB` (dispatch-registered, no direct caller) writes a same-layout record through caller-supplied `rdi`~~ *(corrected 2026-10-02, OPUS: `00329CE1`/`00329DBB` address `01EED260`; `003290BD` and `003266DB` are instructions inside `00329080` and `003266C0` — CON-170)* | 1 |
| literal resolver classes are {0,1,2,3}; class 4 has no literal call site | call-graph census of `0031B9F0` and its three wrappers (`0031FE70`/`00320040` swap ecx↔edx; `00320AB0` forwards unchanged): class 3 dominant (~19 sites *(corrected 2026-10-02, OPUS: 24 constant sites, and class 4's one computed site is `0030A804`, of 32)*), class 1 ×4, class 0 ×2, class 2 ×1 (`0035BDBE`); class 4 only via computed `edx` | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on `SM-1` through `SM-8`. **`SM-5` is the one a port
gets wrong while producing identical bytes**: copying map 0 into all four and then clearing 1, 2 and
4 agrees today and encodes the wrong mechanism. **`SM-1` is the one that bites immediately** — an
empty selector is `0xFFFF`, so returning the `u16` instead of its low byte changes every empty
answer. **`SM-2` is the one that looks like a bug and is not**: collapsing the two failures into
distinct codes is tidier and observably different.

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **Party — internal.** The five maps, the resolver and the refresher's copy order are this
  category's own.
- **CombatFormula — SERVICE, and `SM-3` is the statement.** `BattleEncodedId_IsValidForClass` is that
  layer's, and is **named rather than cited by address** because this contract reads its call site and
  not its body; this contract asserts **which registry class the gate names and that the class's slot is
  installed**, both visible at the call site and from the binder, and asserts nothing about how the
  validity test works.
- **Battle_Runtime_Mode — SERVICE.** The refresher keys its per-mode rewrite on that layer's mode
  accessor. **`SM-5` asserts the copy ORDER, which is complete before the mode is consulted**
  (`0032674F` follows `0032674B`), so nothing here depends on what the mode means.
- **Gameplay, Movement and CombatAction — MECHANICAL, and they arrive through the refresher's own callees.**
  `003266C0` is cited because `SM-5` is a reading of its instructions; the bodies it calls are those
  layers' and none of them is read here. **`SM-5` asserts the ORDER of four copies and one clear,
  which is settled before the first of those callees runs** (`0032674F` follows `0032674B`).
- **Every other layer reached is MECHANICAL**, through these bodies' own callees. *Their addresses
  are deliberately not cited: the party family and the block reset are hubs, and naming one imports
  its whole edge set for a statement `SM-6` already makes by name.*

> **Dispositioned by name on purpose.** The crossings pre-check credits a layer when its alias
> appears as a whole word anywhere in a document — the defect measured in
> `../_index/candidates/fable-crossings-prose-false-clears.tsv` — so these are discharged by the
> paragraphs above and not by a stray noun. *"Party" in particular would otherwise be cleared by the
> word alone.*

## 17. Related

- [The five parallel slot maps](the-five-parallel-slot-maps.md) — the mechanism
- [Contract — party slot assignment](CONTRACT-party-slot-assignment.md) — S-28's first
- [Contract — party focus and control suppression](CONTRACT-party-focus-and-control-suppression.md) — S-28's second

## Cross-subsystem neighbours — SWE2-EC7 (pass-22 dispositions)

- **ActorEntity - CLIENT (9 edges).** `00322C50` is also called by bodies filed to ActorEntity: `002367A0`, `0023A570`, `0031B810` - shared machinery across the layer boundary, no shared ownership.
- **CombatAI - CLIENT (10 edges).** `00322C50` is also called by bodies filed to combat AI: `00301AD0`, `003215C0`, `00321630` - shared machinery across the layer boundary, no shared ownership.
- **CombatAction - CLIENT (9 edges).** `00320AB0`, `00322C50` are also called by bodies filed to combat action: `0030D160`, `002FFCF0`, `003060E0` - shared machinery across the layer boundary, no shared ownership.
- **CombatFormula - CLIENT (2 edges).** `0031B9F0`, `00322C50` are also called by bodies filed to combat formula: `00320AB0`, `002FEF30` - shared machinery across the layer boundary, no shared ownership.
- **Gameplay - SERVICE (12 edges).** `0031B9F0`, `0031FE70`, `00320040` reach bodies filed to Gameplay: `00322C50` (Combat), `0031B9F0` (Combat) - shared machinery across the layer boundary, no shared ownership.
- **Input - CLIENT (1 edge).** `00320040` is also called by bodies filed to input: `00253C70` - shared machinery across the layer boundary, no shared ownership.
- **Items_Equipment_Shops_License - CLIENT (18 edges).** `00320AB0` is also called by bodies filed to items/equipment: `002F9F20`, `0030A4E0`, `0030FAA0` - shared machinery across the layer boundary, no shared ownership.
- **Movement - CLIENT and SERVICE (3 edges).** `00322C50` is also called by bodies filed to movement: `0031BAC0`, `00326BB0`; `003266C0` reaches bodies filed to movement: `00311E20` - shared machinery across the layer boundary, no shared ownership.
- **Rewards_Progression_Economy - CLIENT (2 edges).** `00320AB0` is also called by bodies filed to rewards/progression: `002F8BB0`, `00312280` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (7 edges).** `00320AB0` is also called by bodies filed to script VM / native bridge: `0050FD00`, `0050FD50`, `0050FDD0` - shared machinery across the layer boundary, no shared ownership.
- **Status_Periodic_Terminal - CLIENT (4 edges).** `00320AB0`, `00322C50` are also called by bodies filed to status/periodic terminal: `00310DB0`, `0030E130`, `0030FED0` - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT (3 edges).** `0031FE70`, `00320040`, `00322C50` are also called by bodies filed to UI: `00273880`, `0035BC50`, `0031EB20` - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - SERVICE (4 edges).** `003266C0`, `00329CC0` reach bodies filed to WorldAreaField (world area): `00313F60`, `00377C20`, `00377C70` - shared machinery across the layer boundary, no shared ownership.

## Falsification pass 1 — 2026-09-29 (OPUS): the resolver and initialiser survive; two corrections to the refresher's reading

**Attack.** SM-1 to SM-5 and SM-8 became checks at their instructions. §14's two resolved items were checked against the
refresher and the unwind tables. Script: `Tools/analysis-kit/gfz-scripts/falsify_slot_maps.py`, output
`falsify_slot_maps.out`, image `73461d08…`, 0 BROKEN. SM-7 is carried from OPUS block 340's execution, and the class
call-site census is carried.

| # | Clause attacked | Result |
|---|---|---|
| K1 | §14 item 2: `003266DB` is a dispatched handler on a caller-supplied record | **refuted** (`CON-170`): an instruction inside `003266C0`, no branch to it, its `.pdata` fragment chains back to `003266C0`, and `rdi` is `[02EBF190] + 0x5A48` |
| K2 | SM-5: after a refresh, map 3 = map 0 and maps 2, 4 = the cleared map 1 | **refuted outside mode 0** (`CON-169`): mode arms rewrite maps 1, 2 and 4; modes 3 and 5 restore map 4's pre-refresh bytes; map 3 is untouched in every mode, and nothing after `00326A34` writes a map |
| K3 | §14 item 1: the table is `0x01EC9260` | **refuted** (`CON-170`): `00329CC0` addresses only `01EED260` |
| S1 | SM-1 | **survives**: five byte loads at `+0x5A48`/`5A`/`6C`/`7E`/`90`, index scaled by 2 |
| S2 | SM-2 | **survives**: `0031BA0F jne` past `0031BA11 mov al, 0xff`; `0031BA34 jne 0x31ba11` |
| S3 | SM-3, §2 | **survives**: 200 B; `lea ecx, [r8 + 0x17]` with `r8d = 0` |
| S4 | SM-4 | **survives**: both `0x27` gates; the 16 + 2 copy into maps 1–4 |
| S5 | SM-5's copy order | **survives**: 0→1, 0→3, clear 1, 1→2, 1→4 |
| S6 | SM-8 | **survives**: the table's first byte stored as a u32 at `+0x5AA4` |

Corrected in place: the SM-5 box and §§5, 7, 12, 14 and 15, plus one locator in `CONTRACT-battle-runtime-mode.md`. The
consumer record is `_index/candidates/slot-maps-falsification-pass-1-0929/`.

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-02, cloud-drafted)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../_index/candidates/fable-home-contract-the-five-parallel-slot-maps-1002/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
| `00273800` | 78 B | `0035BC50` + 0x375 | issues the call at `00273800` + 0x12 for indices 0 to 3 and, at the first non-null result whose dword `+4` equals `ecx`, returns 1 when bit 3 (`0x8`) of that record's byte `+0` is clear and 0 when it is set; when no index matches it returns 0 | Interior anchor `00273812`; Interior anchor `0027381C`; Interior anchor `00273823`; Interior anchor `00273828`; Interior anchor `00273845` |
