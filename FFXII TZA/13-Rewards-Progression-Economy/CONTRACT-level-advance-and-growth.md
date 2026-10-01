---
contract: Walk a character up to a target level — growth every level, derived state once, the fanfare only if something owns the record
category: 13-Rewards-Progression-Economy
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: 13-Rewards-Progression-Economy/what-happens-when-a-character-levels-up.md
entries: ["0030C650"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's invariants measured from the
    shipping bytes — the loop's single back-edge resolved and every branch target inside the body
    classified as growth, tail or exit; **both descriptor resolves read as separate call sites with
    their null tests located**; the growth-record failure path followed into the four calls that
    dereference it; and **`BattleStats_FindOwningBattleUnit` disassembled in full so its search
    predicate, not an assumption, settles what the second kind test reads**. **This records checks
    performed on that date, not the method of the original derivation**, which is on the level-up
    page; see §15.
last_reviewed: 2026-09-30
audit:
  passes: 1
  last_pass: 2026-09-30
  last_pass_kind: falsification
  last_pass_state: opus-level-advance-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — level advance and growth

> **Authored 2026-09-22 by FABLE.** S-32's binding gap is *"EXP/LP division only, of 5 pages"*. The
> loot rolls (`8cfdf3851`), the gil paths (`68135b186`) and the defeat sequence (`b5289a220`) are
> done; **this takes the level-up, so all five of S-32's pages now carry a contract.**
>
> Written against FRONTIER's adequacy test: *a narrower contract is adequate exactly when the
> system's operations have no cross-operation invariant or ordering it leaves unstated.*
> **[The page](what-happens-when-a-character-levels-up.md) is AUDITED and unusually complete**, so
> this contract deliberately does not restate its mechanism. §4 is the eight invariants that survive
> the page — **`LU-1`, `LU-5`, `LU-6` and `LU-7` are statements the page's own facts imply but its
> text does not make**, and each is named against the page below rather than presented as new
> discovery.

## 1. Purpose

Move a character from the level they are to the level they have earned, applying every stat gain on
the way, and announce it once.

## 2. Interface

`BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` (`0030C650`), **570 B**, 150 instructions, one
`ret` at `0030C889`, and **one loop whose single back-edge is `0030C865 jl 0x30c6a3`** — so the loop
spans almost the whole body, and everything below is inside it unless said otherwise.

`(stats *rcx, int target edx, int flags r8d)`. **Four callers**, per
[the page](what-happens-when-a-character-levels-up.md) §5: the defeat sequence, the result applier
`BattleFormula_ApplyTargetResult`, the unit-initialisation level grower, and the console's *set level
to max*. **None of the four is cited by address here** — each is a hub, and this contract reads none
of their bodies.

## 3. Types

```
stats
  +0x004  u8    the character id -- selects the party-definition row (LU-6)
  +0x005  u8    the record kind; NON-ZERO skips all growth (LU-4) and the fanfare (LU-7)
  +0x008  i32   HP   \  grown by the two level-keyed helpers, which take no growth byte
  +0x00C  i16   MP   /  -- their curve is the 02EBF108 table, and it ROLLS (LU-8)
  +0x010 .. +0x01C  f32[4]  grown by the float helper, which DOES take a growth byte (LU-5)
  +0x1C2  u8    the level -- this function is its writer

growth record = ImageAddress_ResolveRuntimePointer([02EBF130] + 0x0C)
              + u16 stride at [02EBF130] + 0x08  ×  stats[+0x04]
  +0x1F, +0x22, +0x25, +0x28   u8   the four float growth bytes
```

## 4. Preconditions · postconditions · invariants

### The eight cross-operation invariants

**LU-1 — There are THREE guards on 99, and the innermost one can never fire.** The page's evidence
table records *"Cap 99 applied twice"* — the `cmovg` on the target at `0030C682` and the `cmova` per
increment at `0030C7B8`. But **the page's own §11 records a third**, at the top of the loop:
`0030C6CC cmp byte ptr [rdi + 0x1c2], 0x63` / `0030C6D3 jae 0x30c85c`, which skips the entire
iteration once the level is 99. **Every path that reaches the increment has passed that guard**, so
at `0030C7B3 inc eax` the level is at most `0x62` and the result at most `0x63` — and `cmova`, which
fires only above `0x63`, is **unreachable as a clamp**. *The page states both facts, in two sections,
and never joins them; the joined statement is that the shipped binary clamps the level in one place
and defends it in two more.*

**LU-2 — Levelling is MONOTONIC, by two independent guards.** `0030C686 cmp ecx, r14d` / `jge`
returns **without entering the loop at all**, and the loop only ever `inc`s. *A target below the
current level is not an error and not a decrease — it is a no-op.*

**LU-3 — One loop, THREE different cadences, and a port must preserve all three.** Per iteration:
the six growth calls run **every level**. The derived-state rebuild runs **only on the
final level**, gated by `0030C7C1`–`0030C7C7 cmp esi, r14-1`. The presentation — the message poster, then the
three forwarding calls and the two audio calls — also runs **only on the final
level**, and additionally behind the notify flag. *So a four-level gain applies growth four times,
rebuilds derived state once, and plays one fanfare.* **The flag's polarity: bit 1 of `flags` SUPPRESSES
notification** *(2026-09-25, FABLE, Claude Opus 5.5, on [OPUS block 348](../_index/candidates/s32-opus-replay-level-advance/README.md), which executed it with no stub, 5/5; `0030C650`–`0030C6C9` and `0030C7D3`–`0030C7ED` re-read.)*. `0030C660`–`0030C676` computes `notify = ~(flags >> 1) & 1`, so `flags = 0` notifies and
`flags = 2` is silent. It is combined with "final level" at `0030C6A3`–`0030C6C9`.

> **What the first forwarding call does, and the key it carries — added 2026-09-22 (FABLE) on
> `OPUS-REQ-FABLE-WHAT-DOES-THE-7FB0RECORD-KEY-DENOTE`.** OPUS asked what `ManagerSub7FB0Record`'s
> key at `+0xF4` (and `+0xC4` while the embedded widget is live) denotes, noting that its producer
> `002905D0` **has no direct caller** and so its domain could not be read from call sites.
>
> **It has one, and it is this contract's body.** `002905D0` is reached only through the 5-byte
> thunk `0035D8C0`, and that thunk has **exactly one caller image-wide**: `0030C815`, inside
> `LU-3`'s presentation block. There `ecx` is `[r15 + 8]`, where `r15` is the owning battle unit
> `LU-7` resolves — the same `[unit + 8]` the very next call takes as its unit id. **So the key's
> population is BATTLE-UNIT IDS**, and the table is per-unit.
>
> **The producer discards everything else the caller passes.** `002905D0` keeps only `ecx`, loads the
> manager singleton, returns 0 if it is null, and otherwise calls `002966E0(manager + 0x7FB0, 6,
> key, 1)`. *The level and the flags that `LU-3` puts in `r8d` and `edx` at the call site are not
> forwarded; this path carries the unit id and nothing else.*
>
> **The queued value is the constant `1`, and the `-5` is not arithmetic.** `002905EA` sets
> `edx = 6` and `002905F6` computes `lea r9d, [rdx - 5]` — a compiler reusing the register it just
> loaded rather than emitting a second immediate. **The two constants are `6` and `1`, and neither is
> derived from the other in any meaningful sense.**
>
> **The `6` is the RECORD COUNT, not a second key.** `002966E0` sign-extends it and uses it as the
> loop bound with a stride of `0x110` (`00296799`, `002967A0`), and hands it to the lookup
> `00299A30`, which scans that many records — comparing the key against `rec + 0xC4` when a
> per-record liveness predicate returns 1 and against `rec + 0xF4` otherwise. *That reproduces the
> `+0xC4`/`+0xF4` rule from the other side, independently of the structure work.*
>
> **And the queue de-duplicates, which is what makes the answer to "what does the value mean"
> uninteresting in the right way.** Before appending, `002966E0` scans all three slots for the value
> it is about to queue and exits if it is already there (`00296720`–`00296723`). **With exactly one
> producer in the image, queueing exactly one constant, the `uint32[3]` queue can therefore hold at
> most one distinct value, `1`.** So it is a **per-unit one-shot flag**, not a value channel — which
> is consistent with the consumer draining one entry per call and clearing the claim when it empties.
>
> **NOT CLAIMED:** what the flag makes happen. This establishes the key's domain and the value's
> provenance; the consumer's effect is that subsystem's and is not read here.

**LU-4 — The whole growth block is gated on `stats[+0x05]`, and a non-zero kind advances the level
with NO stat change at all.** `0030C6D9 cmp byte ptr [rdi + 5], 0` / `jne 0x30c7a7` jumps **past
every growth call, straight to the level write**. *The same function levels a party member with full
growth and levels anything else by a bare byte increment.* This is the same selector byte
[equipment compatibility](../12-Items-Equipment-Shops-License/CONTRACT-equipment-compatibility.md)
`EQ-6`, [the loot rolls](CONTRACT-loot-rolls-and-the-chain.md) `LC-5` and enmity all branch on.

**LU-5 — The record resolve has TWO failure shapes, and the float growth calls dereference both.**
`0030C6ED` and `0030C6FA` both take `0030C721 xor ebp, ebp`, and the code then **falls into the
growth block regardless**. The HP and MP calls (`0030C730`, `0030C746`) take the level and the
current value, hold no growth byte and survive it; **the four float calls read `byte [rbp + 0x1F]`,
`+0x22`, `+0x25` and `+0x28`** (`0030C757`, `0030C768`, `0030C77E`, `0030C794`). *It does not fail
closed — it fails on the third growth call, after HP and MP have already been written.* The second
shape is `LU-6`'s.

**LU-6 — The null test guards the FIRST resolve; the pointer actually used comes from the SECOND,
untested.** The descriptor is resolved twice with the same key: `0030C6EF`/`0030C6F2` produces a
value that is null-tested at `0030C6F7` and then **discarded**, and `0030C703`/`0030C706` produces
the value that `0030C71D add ebp, eax` actually uses — **with no null test of its own**. *So the
guarded call is not the one whose result is dereferenced.* If the second resolve ever returned null
where the first did not, `ebp` would be `stride × id` — **not a null pointer but a small wild
address**, which `LU-5`'s four reads would then dereference past. *Whether the two calls can disagree
is §14's question; that the guard is on the other one is not.* *§14 answers it (2026-09-26): on one thread they
cannot, since the resolver is pure and nothing between the calls writes. The wild-address case needs a concurrent
writer, or a fixture.*

**LU-7 — The fanfare depends on the record being INSTALLED IN A BATTLE SLOT; none of the mechanics
do.** `0030C6BC` calls `BattleStats_FindOwningBattleUnit` (`0031B860`), which **walks the battle-unit
slots and returns the unit whose `+0x698` equals the argument** (`0031B892 cmp qword ptr
[rax + 0x698], rdi` / `je`) — a linear search, returning **null** when no slot holds this record. The
presentation block then requires that unit: `0030C7ED test r15, r15` / `je` skips everything. *So a
stats record that no battle unit owns still advances its level, still grows every stat and still
rebuilds derived state — ~~and is silent~~.* **Corrected: not fully silent** *(2026-09-25, FABLE, Claude Opus 5.5, on [OPUS block 348](../_index/candidates/s32-opus-replay-level-advance/README.md), which executed it with no stub, 5/5; `0030C650`–`0030C6C9` and `0030C7D3`–`0030C7ED` re-read.)*. The level-up poster
`0046A690`, which posts **event 4** with the record and its new level, is called at `0030C7E4`. That is **before**
the owner test at `0030C7ED`, and it is gated only by notify, final level and kind 0 (`0030C7D3`–`0030C7DF`). With
`flags = 0` and no owning unit, OPUS's run posts event 4. Only the forwarding and audio calls after `0030C7ED`
need the owner. *So an unowned record is silent only when notification is suppressed.*

> **And the kind test inside that block is the SAME BYTE, reached the long way round.** `0030C7F2`
> loads `[r15 + 0x698]`, which the search predicate makes **equal to `rdi` by construction**, so
> `0030C7FE movzx eax, byte ptr [rax + 5]` reads `stats[+0x05]` — the byte already tested at
> `0030C6D9`. *It is not redundant code: it is the test that suppresses the fanfare on the path that
> skipped `0030C7DB`. But it is the same byte, and a port that resolves the owner differently changes
> which byte it is.*

**LU-8 — Levelling is NOT deterministic, and a multi-level gain draws the shared generator once per
level per stat.** Per [the page](what-happens-when-a-character-levels-up.md) §8's answered `UQ-134`,
The two level-keyed helpers each return `value + b + trunc((rng mod trunc(b/5 × 100)) / 100)` — the
table base plus a random bonus below a fifth of it — **whenever `b/5 ≥ 0.01`**, and the roll is
`RNG_MT19937_NextU32_Thunk`. *So HP and MP growth are rolled, not computed; the same kill can level
the same character to the same level with different stats; and because the draws happen inside the
per-level loop (`LU-3`), **the number of draws depends on how many levels were gained at once** —
which is a stream-position effect on every later consumer of that generator, including
[the loot rolls](CONTRACT-loot-rolls-and-the-chain.md).* **Measured** *(2026-09-25, FABLE, Claude Opus 5.5, on [OPUS block 348](../_index/candidates/s32-opus-replay-level-advance/README.md), which executed it with no stub, 5/5; `0030C650`–`0030C6C9` and `0030C7D3`–`0030C7ED` re-read.)*: each level draws the generator
**twice**, once for HP and once for MP, and the four float growths draw nothing. So a *k*-level gain advances the
shared stream by 2*k* for the row measured (party row 0). The same seed reproduced HP / MP exactly.

## 5. State

**Owned:** the level byte and the six stat fields. **Read, never written:** the party-definition
growth row, the record kind byte and the character id. **Advanced as a side effect:** the shared
generator's stream position (`LU-8`).

## 6. Relationships

| | |
|---|---|
| **Called by** | [the defeat sequence](CONTRACT-defeat-rewards-sequence.md) — `DR-3`'s threshold walk hands this the target — and three others (§2) |
| **Rebuilds through** | `BattleStats_RecomputeDerivedStateAndAutoStatuses`, once per call (`LU-3`) |
| **Resolves its owner through** | `BattleStats_FindOwningBattleUnit` (`0031B860`) — `LU-7` |
| **Shares the generator** | [the loot rolls](CONTRACT-loot-rolls-and-the-chain.md) — `LU-8` |
| **Sibling** | [`CONTRACT-experience-and-licence-award.md`](CONTRACT-experience-and-licence-award.md) — S-32's first |

## 7. State transitions

*clamp the target → return if already there → per level: skip if already 99, gate on the kind, grow
six stats, increment and store → on the final level only: rebuild derived state, then announce if the
flag is set and a unit owns the record → repeat.*

## 8. Script · resource · event interactions

The growth row and the HP/MP curve table are authored. The announcement is one row of the documented
post-result event family (event `0x04`, *"… is now level {level}"*), per
[the page](what-happens-when-a-character-levels-up.md) §8.

## 9. Determinism

**Not deterministic** — see `LU-8`. *This corrects the natural assumption: a level-up looks like pure
table arithmetic and is not.* The four float stats **are** deterministic; only HP and MP roll.

## 10. Failure paths and edge conditions

- A target at or below the current level does nothing (`LU-2`).
- At level 99 every iteration is skipped while the loop keeps counting (`LU-1`).
- A non-zero kind byte advances the level and changes no stat (`LU-4`).
- A failed resolve faults on the first float growth call, **after HP and MP have been written**
  (`LU-5`, `LU-6`).
- A record no battle unit owns levels silently (`LU-7`).

## 11. Observable behaviour

Every stat gain, the cap at 99 and the fanfare come out of this one function — and a character who
banks four levels' worth of experience gains them all at once, each with its own roll, but hears one
fanfare and has their derived stats rebuilt only at the end.

## 12. Reproduction formula

Call with a target below the current level and assert **nothing** is written (`LU-2`). Call at level
99 and assert no growth call runs (`LU-1`). Set `stats[+0x05]` non-zero and assert the level moves and
no stat does (`LU-4`). Grant three levels in one call and assert the growth calls run **three times**,
the rebuild **once**, and the generator advances **six** times (`LU-3`, `LU-8`). Detach the stats
record from every battle slot and assert the level still advances and no sound plays (`LU-7`). Force
the second resolve to fail and assert HP and MP are already written when the float call faults
(`LU-5`, `LU-6`).

## 13. Runtime validation

~~**None.** No experiment executes this body. S-32's runtime cell is not addressed by this contract.
*Stated rather than left blank so a CONTRACT READY header is not read as evidence of execution.*~~ **Superseded
2026-09-25:** [OPUS block 348](../_index/candidates/s32-opus-replay-level-advance/README.md) executed `0030C650` with no stub over shipped growth rows and the real gameplay MT
(LU-1 to LU-4, LU-7 and LU-8; 5/5, identical three times). The evidence class is native replay, not live, and
~~LU-5 / LU-6 are not covered~~. *Extended 2026-09-26 (FABLE, Claude Opus 5.5), on
`OPUS-NOTE-FABLE-S32-LU6-RESOLVES-CANNOT-DISAGREE`:* `lu6.py` in the same package (OPUS, no stub, 10/10; re-run by FABLE
2026-09-26, all pass) executes **LU-6** and **LU-5's second shape**.
- **Only the second resolve is null.** The guard passes, and the pointer used is the small wild address `stride × id`
  (`0x180` for 128 × id 3). HP and MP are stored, then the float growth faults past it.
- **Only the first resolve is null.** `0030C6FA` is taken, HP and MP are stored, and the fault comes at `0x1F`.
- The control shows the used pointer is `stride × id + low32(second resolve)`: `0030C71D` is a 32-bit `add ebp, eax`.
**`LU-8`'s draw count is the one clause here that a live test could settle cheaply**, and it is
routed to ASTRA rather than claimed.

## 14. Unresolved

- ~~**Whether the two resolves of `LU-6` can disagree.** `ImageAddress_ResolveRuntimePointer` is not
  read by this contract, so whether it caches, and whether a second call with the same key can return
  null after a first returned non-null, is open. *The structural claim — that the null test guards the
  discarded result — does not depend on the answer.*~~ **Answered 2026-09-26 (FABLE, Claude Opus 5.5): on one thread
  they cannot disagree.** `0020E600` is `mov eax, ecx` / `add rax, [01F83530]` / `ret`. It is pure: it has no cache
  and stores nothing. Between the two calls (`0030C6F7`–`0030C706`) the code only reads: the test, the branch, and the
  reloads of `[02EBF130]` and its `+0xC`. The same key therefore gives the same value. Only a concurrent writer of
  `[02EBF130]`, of that record's `+0xC`, or of `[01F83530]` could make them differ, and no such writer is established.
  (`01F83530` is zero at load, with one undriven store route: see the authored-table contract §7.) The
  "second null, first not" case LU-6 guards against is therefore reachable only through such a writer, or in a
  fixture, as `lu6.py` builds it. The structural claim is unchanged.
- Whether any caller can reach this body with the growth table unresolved (`LU-5`).
- ~~`UQ-134` and `UQ-135` remain open on [the page](what-happens-when-a-character-levels-up.md): the
  names of the four float stats, and which sound slot 7 of the live bank is.~~ *Superseded 2026-09-26 (FABLE, Claude Opus 5.5): both are answered. **UQ-134**: `+0x10` Strength, `+0x14` Magick Power, `+0x18` Vitality, `+0x1C` Speed (from CB-12, 2026-09-14). **UQ-135**: answered by OPUS on 2026-09-15, both halves, and the first half's premise was backwards.*

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| `LU-1` — three guards, the innermost unreachable | `0030C6CC`/`0030C6D3` and `0030C7B3`–`0030C7B8` read together, with **every path into the increment shown to pass the loop-head guard** — the control is that the guard precedes the kind gate at `0030C6D9`, so the `jne` shortcut is also behind it | 1 |
| `LU-2` — monotonicity | `0030C686`/`0030C689` traced to the single `ret`, with the loop's `inc` as the only other level write | 1 |
| `LU-3` — the three cadences | the back-edge `0030C865` resolved to `0030C6A3`, placing growth inside it; `0030C7C1`–`0030C7C7` guarding `0030C7CE`; the same guard reached before the presentation block | 1 |
| `LU-4` — the kind gate | `0030C6D9`/`0030C6DD` traced to `0030C7A7`, which is the level-write block — the control is that it lands *past* every growth call | 1 |
| `LU-5` — the null record | `0030C721` followed into `0030C757` / `0030C768` / `0030C77E` / `0030C794`, with the HP and MP calls shown *not* to use `rbp` | 1 |
| `LU-6` — the guard on the discarded resolve | `0030C6EF`–`0030C706` read as two call sites: the null test at `0030C6F7` follows the first, and `0030C71D` consumes the second | 1 |
| `LU-7` — slot residency, and the same byte | **`0031B860` disassembled in full**: the search predicate `0031B892` is the equality that makes `[r15 + 0x698]` equal `rdi`, and `0031B8A6 xor eax, eax` is the not-found return `0030C7ED` tests | 1 |
| `LU-8` — the roll and the thunk | [the page](what-happens-when-a-character-levels-up.md) §8, `UQ-134` answered 2026-09-11 — **carried, not re-derived**; the per-level position is this contract's, from `LU-3` | 1 |
| the four callers, the flag bit, the event row | [the page](what-happens-when-a-character-levels-up.md) §§5–8, falsified 2026-09-13, audited 2026-09-13 | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on `LU-1` through `LU-8`. **`LU-3` is the one a port
gets wrong for performance**: computing the final level's stats directly, or rebuilding derived state
each iteration, both look like cleanups and both change results — the first because growth compounds
and rolls, the second because it changes nothing observable *except* the generator's position.
**`LU-8` is the one a port gets wrong for tidiness**: HP and MP growth look like table lookups, and
making them pure makes every later draw in the frame land differently. **`LU-7` is the one a port gets
wrong by improving it** — resolving the owner from a back-pointer instead of a slot search makes the
fanfare fire for records the original leaves silent.

## 16a. Crossings into other layers (FABLE, 2026-09-22)

**Only two bodies are cited by address in this contract**: the subject `0030C650`, and
`BattleStats_FindOwningBattleUnit` (`0031B860`), which `LU-7` rests on and which was read in full.
Everything else this function calls or is called by is named by role. *That is deliberate: each of
them is a hub, and a citation imports its whole edge set for a statement this contract does not make.*

- **Rewards_Progression_Economy — internal.** The advance, the loop, the three growth helpers and the
  level byte are this category's own.
- **Status_Periodic_Terminal — SERVICE, and `LU-3` is the statement.**
  `BattleStats_RecomputeDerivedStateAndAutoStatuses` belongs to that layer; **this contract asserts
  only WHEN it is called — once, on the final level — and not what it recomputes or which
  auto-statuses it applies**, neither of which is read here.
- **CombatFormula — SERVICE on the callee side, CLIENT on the caller side.**
  `BattleStats_FindOwningBattleUnit` is that layer's, and `LU-7` reads **its search predicate and its
  not-found return**, which is exactly what the invariant needs. `BattleFormula_ApplyTargetResult` is
  one of the four callers, named only — *what it computes before handing over a target level is that
  layer's, and [the page](what-happens-when-a-character-levels-up.md) §5 already records that it
  passes a literal `0` for the flags.*
- **ActorEntity — MECHANICAL, and it is inside the one body this contract does read.** The slot
  count and slot lookup that `BattleStats_FindOwningBattleUnit` walks belong to that layer. **`LU-7`
  asserts that the search is linear over the slots and returns null when none matches — a property of
  the loop, visible without entering either accessor** — and asserts nothing about what a slot is or
  how the table is maintained.
- **UI — MECHANICAL, and it is a 9-byte predicate inside the two bodies the 7FB0 note reads.**
  Both `002966E0` and `00299A30` call one liveness check that belongs to that layer, and the
  `+0xC4`-versus-`+0xF4` rule turns on its result. **This contract asserts only WHICH FIELD each
  branch compares, which is visible at the two `cmp` instructions without entering the
  predicate** — not what "live" means for the embedded widget, which is that layer's.
- **CombatAction, Movement, Items_Equipment_Shops_License and Party — CLIENTS of that same resolver,
  and this contract makes no claim about any of them.** `BattleStats_FindOwningBattleUnit` is shared:
  bodies across those four layers call it too. *They are reached only because `LU-7` reads the
  resolver, they are not callers of the level advance, and nothing here depends on what they do with
  the unit it returns.*
- **Audio — SERVICE, and the crossing is already documented from the other side.** The two audio
  calls are that layer's; `LU-3` asserts only that they run once per call, on the final level, behind
  the notify flag and `LU-7`'s gate. **What the literals `7`, `0x40` and `0x7F` mean is
  [the sound-request page's](../18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md), and
  the page's §6 already records that join** — this contract does not re-derive it and does not re-open
  `UQ-135`.
- **RNG_Random_Selection — SERVICE, and `LU-8` is the statement.** The generator is that layer's;
  this contract asserts **how many times the level walk draws from it and in what position**, carried
  from the page's answered `UQ-134`, and nothing about the generator itself.
- **Presentation, Gameplay, Spawn_Encounter_Lifecycle, WorldAreaField and
  PlatformOnlineAchievements — MECHANICAL.** They are reached through the presentation chain and
  through the hubs named above, never cited, and never read. *The message poster's event row is
  [the post-result events page's](../07-Combat-Action/Post-Result-Events/the-post-result-events-and-the-battle-message-table.md),
  and ~~`UQ-136` remains open on the page for the middle forwarding call~~ *corrected 2026-09-26 (FABLE): `UQ-136` was
  answered 2026-09-25. The middle forwarding call's `1` is a target count, and `0x71` is the `c_all.efx` effect group
  spawned on the unit (register row).*

> **Dispositioned by name on purpose.** The crossings pre-check credits a layer when its alias
> appears as a whole word anywhere in a document — the defect measured in
> `../_index/candidates/fable-crossings-prose-false-clears.tsv` — so these are discharged by the
> paragraphs above and not by a stray noun. *"Audio", "Party", "Movement" and "Gameplay" in
> particular would otherwise each be cleared by the word alone.*

## Cross-subsystem neighbours — pass 22 (FABLE, 2026-09-29)

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page. Section 16a's heading is numbered, so the crossings gate does not read it; this section names each edge.*

**ActorEntity — SERVICE (2 edges).** `BattleStats_FindOwningBattleUnit` `0031B860` calls `BattleUnit_GetSlotCount` `00236850` and `BattleUnit_GetBySlotIndex` `00236820`. The stats-to-unit lookup the level advance starts from is a scan of the actor layer's unit table; it borrows the table and changes nothing in it.

**Audio — SERVICE (2 edges).** On a level gained, `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650` calls `003A1180` with the sound id 7 and, unless that returns -1, calls `002DF220` with the result and the two values `0x40` and `0x7F`. The level-up plays one fixed sound through the audio layer's resolve-and-play pair; nothing it computes depends on the audio calls.

**CombatAction — CLIENT (4 edges).** `BattleAction_EvaluateTargetPreviews` `00303830`, `BattleAction_EvaluateTargetPreviewRecursive` `00303A00`, `BattleAction_CheckDefinitionCategoryAvailability` `003060E0` and `003879C0` call `0031B860`. The action layer's preview and availability code uses the same stats-to-unit lookup; it does not advance levels.

**CombatFormula — CLIENT and SERVICE (37 edges).** `0030C650` calls `0031B860` and is called by the ordinary applier `BattleFormula_ApplyTargetResult` `003112F0`; `0031B860` is also called by 35 other formula bodies, among them `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30`, `BattleStats_ModifyHPAndProcessLethalState` `00300530`, `BattleFormula_ResolveTargetResult` `00385F60`, `BattleFormula_RollSpecialGuardOutcome` `00387FD0`, `BattleFormula_ApplyPreResolutionTargetGates` `00390AB0` and `BattleFormula_DispatchPostResultEvents` `00469EC0`. A result that carries a level gain reaches the level advance through the applier, and the lookup it uses is the formula layer's common stats-to-unit accessor.

**Items_Equipment_Shops_License — CLIENT (4 edges).** `BattleStats_SetEquipmentSlotByStatsIndex` `0031A410`, `BattleStats_SetEquipmentSlotByMappedId` `0031A510`, `BattleStats_SetEquipmentSlotDirect` `0031A630` and `BattleStats_SetLicenseNodeStateAndApplySideEffects` `00323910` call `0031B860`. Equipment and License writers find the owning unit through the same lookup; they do not take part in the growth computation.

**Movement — CLIENT (2 edges).** `0033CB10` and `0033D890` call `0031B860`. Two locomotion bodies use the stats-to-unit lookup; the level advance does not touch movement.

**Status_Periodic_Terminal — SERVICE and CLIENT (6 edges).** `0030C650` calls `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0`; `0031B860` is called by `BattleUnit_ResolvePeriodicPrimaryResourceRecoveryStep` `002F9400`, `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360`, `BattleStats_RemoveStatusesFromMaskAndRecompute` `0030F690`, `0030FED0` and `BattleFormula_BuildRuntimeCounterPeriodicHpCredit` `00386860`. After a level is gained the derived layer and auto-statuses are recomputed, and the status code shares the stats-to-unit lookup.

**UI — SERVICE (2 edges).** `002966E0` and the record lookup `00299A30` call `00273A20`, a 9-byte test that the record's first qword is non-null. That is the per-record liveness predicate that chooses whether the key is compared against `+0xC4` or `+0xF4` when the UI manager's per-unit record table (keyed by battle-unit id, fed from `LU-3`'s presentation block) is scanned; the UI layer supplies the test and the table, and the growth values are fixed before it runs.

*Added 2026-09-29 (FABLE, pass-22 debt, second pass): the four layers the generator thunk named in `V10` brought in.*

**RNG_Random_Selection - SERVICE (2 edges).** The HP helper `002F9A60` and the MP helper `002F9B20` call `RNG_MT19937_NextU32_Thunk` `00379CD0`, a 5-byte `jmp` into the Mersenne Twister whose state is `02EB3870`. That is `LU-8`'s roll: the level-up HP and MP gains are draws on that MT stream, the generator [which roll is on which generator](../21-RNG-And-Determinism/which-roll-is-on-which-generator.md) lists as number 1.

**CoreRuntimeScheduling, Script_VM_Native_Bridge and WorldAreaField - DEPENDENCY (6 edges, 2 per layer).** The same thunk has other callers, and each draw they make moves the stream the level-up roll reads next:
- CoreRuntimeScheduling: the boot frame modes `0022B6E0` and `0022B7E0` each draw once and throw the value away (`0022B706`, `0022B7EB`), so the stream is already advanced when play starts after a fresh boot ([which roll is on which generator](../21-RNG-And-Determinism/which-roll-is-on-which-generator.md) §5).
- Script_VM_Native_Bridge: the verbs `rand` (`00355140`, pushes a raw draw) and `rand_29` (`00354BF0`, pushes `(draw × n) >> 32` for a popped `n`) let a script draw from the same stream.
- WorldAreaField: the weather pickers `0025ABA0` and `0025ACA0` scale a draw to 0..99 (`0025ABB8`, `0025ACDD`).

This is the mechanism behind `LU-8`'s "depends on the generator's stream position": the gain a unit rolls depends on how many draws the boot modes, scripts, weather and the formula bodies made before it, not on the unit. None of these callers reads or writes the growth tables. Tier 1: the thunk and all six call sites read from the shipping image 2026-09-29 (FABLE); verb names from [the verb table](../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv).

## 17. Related

- [What happens when a character levels up](what-happens-when-a-character-levels-up.md) — the mechanism this contract does not restate
- [Contract — the defeat rewards sequence](CONTRACT-defeat-rewards-sequence.md) — the caller
- [Contract — loot rolls and the chain](CONTRACT-loot-rolls-and-the-chain.md) — `LU-8`'s other consumer of the generator

## Falsification pass 1 — 2026-09-30 (OPUS): all eight invariants survive at their bytes

**Attack.** Each of LU-1 to LU-8, the interface and the note on the first forwarding call was turned into a check at its
instructions. OPUS block 348's execution is carried, not re-run. Script:
`Tools/analysis-kit/gfz-scripts/falsify_level_advance.py`, output `falsify_level_advance.out`, image `73461d08…`,
0 BROKEN, exit 0.

| # | Clause attacked | Result |
|---|---|---|
| V1 | §2 570 B, 150 instructions, one `ret`, one back-edge | **survives**. The extent is 570 B with 150 instructions. The only `ret` is `0030C889`, and the only back-edge `0030C865 jl 0030C6A3` |
| V2 | LU-1 three guards on 99 | **survives**. `0030C682 cmovg r14d, eax`; `0030C6CC cmp byte [rdi + 0x1c2], 0x63` / `0030C6D3 jae 0x30c85c`; `0030C7B3 inc eax` / `0030C7B8 cmova eax, ecx` |
| V3 | LU-2 monotonic | **survives**. `0030C686 cmp ecx, r14d` / `jge 0x30c87f` leaves past the loop. The only level write is `0030C7BB mov [rdi + 0x1c2], al`, and nothing decrements `+0x1C2` |
| V4 | LU-3 notify polarity and the final-level cadence | **survives**. `shr r13d, 1`, `not r13d`, `and r13d, 1` compute `~(flags >> 1) & 1`, and `0030C7C1`–`0030C7C7` is `lea eax, [r14 - 1]` / `cmp esi, eax` / `jne` |
| V5 | LU-4 the kind gate | **survives**. `0030C6D9 cmp byte [rdi + 5], 0` / `jne 0x30c7a7` |
| V6 | LU-5 both failures zero `ebp`, and the float calls read four growth bytes | **survives**. `0030C6ED` and `0030C6FA` both `je 0x30c721` (`xor ebp, ebp`); HP and MP are called at `0030C730` / `0030C746`; `byte [rbp + 0x1f / 0x22 / 0x25 / 0x28]` are read |
| V7 | LU-6 the tested resolve is not the one used | **survives**. The first call's result is tested at `0030C6F7`. The second call's result reaches `0030C71D add ebp, eax` with no test or branch between |
| V8 | LU-7 the owner search, and the poster before the owner test | **survives**. `0030C6BC call 0031B860` (`0031B892 cmp [rax + 0x698], rdi`); `0030C7E4 call 0046A690` precedes `0030C7ED test r15, r15`; `0030C7F2 mov rax, [r15 + 0x698]`, `0030C7FE movzx eax, byte [rax + 5]` |
| V9 | the forwarding call's single route | **survives**, by a raw `E8`/`E9` census (the edge list does not carry thunk jumps). `0035D8C0` has one call site, `0030C815`, and `002905D0` one, the thunk's `jmp`. `002905EA mov edx, 6`, `002905F6 lea r9d, [rdx - 5]`, and the `0x110` stride at `00296799` against the bound `002967A0` |
| V10 | LU-8 HP and MP roll; the float growths do not | **survives**. The HP helper `002F9A60` and the MP helper `002F9B20` reach the generator thunk `00379CD0`. The growth block's only other callee, the float helper `002F9BD0`, does not, within three call levels |

**Verdict.** The contract's eight invariants hold at the instructions they cite. Tier 1 (static).
