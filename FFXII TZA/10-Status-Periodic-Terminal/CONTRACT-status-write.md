---
contract: Change a status on a battle unit and process its side effects
category: 10-Status-Periodic-Terminal
scope: operation
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: Status-Write/the-status-write-and-its-side-effects.md, the-thirty-two-statuses.md, Periodic-Tick/what-the-periodic-tick-does.md
entries: ["0030E360", "003876D0", "00387730", "00386A50", "00386A70", "00300FC0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 104 addresses cited - 6 data, 23 entry, 67 interior, 5 literal, 3 text-data, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
  status_data_sha256: from ps2data/image/ff12/test_battle/in/binaryfile/status_data.bin, 1312 bytes, magic `st2e`
last_reviewed: 2026-09-12
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-status-write-pass-1  # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — change a status on a battle unit and process its side effects

> **Authored 2026-09-12 by OPUS**, answering `FABLE-REQ-OPUS-CONTRACTS-S26-S15-S03`. The
> mechanism was established by FABLE on
> [the status write page](Status-Write/the-status-write-and-its-side-effects.md); this contract
> states it as an implementable interface and **re-derives every load-bearing constant, table and
> extent from the image and the authored file rather than from that page.** Where the re-derivation
> agreed, §15 says so; where it found something the page did not state, the row says that too.

## 1. Purpose

Every status a unit gains or loses in FFXII goes through one operation: the icon that appears, the
Petrify countdown and the statue at the end of it, a character dropping when KO'd and the party
collecting the rewards, Haste cancelling Slow, a Reflect that Slow cannot be cast through. The
operation writes one bit in one of three status words, gives the status its duration and its beat
timer, cancels whatever the status's authored row says it cancels, plays the reaction, and — for the
three statuses that end a unit — runs the defeat path. **Nothing else in the game sets or clears a
status bit.**

## 2. Interface

| | |
|---|---|
| entry point | `0030E360` `BattleStats_ChangeStatusAndProcessSideEffects`, 1,323 B |
| calling convention | Microsoft x64. `rcx`, `rdx`, `r8b`, `r9d`, then three stack arguments. Frame `0x1E0` with a security cookie at `[rsp+0x1D0]` (`0030E368`, `0030E379`) |
| parameters | `0` `rcx` `BattleStatsRecord *target` — required, never tested for null · `1` `rdx` `BattleStatsRecord *source` — **may be null** · `2` `r8b` `uint8 status`, `0..31`; a value above 31 skips only the terminal switch (`0030E737 cmp ecx, 0x1F`), everything before it still runs · `3` `r9d` `int32 paramA`, **negative means "use the authored default"** · `4` `[rsp+0x20]` `int32 paramB`, same convention · `5` `[rsp+0x28]` `uint32 flags` · `6` `[rsp+0x30]` `int32 mode`, `0..5`; above 5 the call returns having done nothing (`0030E4CB`) |
| return type | `void` |
| return semantics | **The operation is silently idempotent.** Every refusal path returns `void`; a caller cannot distinguish "applied" from "refused for any of seven reasons". A reimplementation must not add a status code, and a caller that needs to know must read the mask before and after |
| callbacks / indirect dispatch | the two transition builders are selected by `cmovne` and called through `rax` (`0030E5EA`–`0030E60E`); the terminal case is a two-level jump table (§7); `0046A800` is reached only through a register, so a caller census by direct call misses it. That register call — the extra-effect poster at `0030E727`, gated on the `extraEffect` local `[rsp+0x60]` (`!(flags & 2)`) — loads `rax` with `0016D6A0` at `0030E719` and `cmovne`-replaces it with `0046A800` at `0030E720` when `edi != 0`, `edi` reloaded from `[rsp+0x44]` = `(mode - 3) <=u 1` (`0030E3C2`–`0030E3CB`). **Modes 0, 1, 2 and 5 therefore call `0016D6A0`** — the folded 3-byte `C2 00 00` (`ret 0`) stub, a no-op site in the shipped image; **only modes 3 and 4 — the two "adding" modes — reach the battle-event poster** |

**`flags` bits this operation consumes** (the whole word is forwarded to the applier as its fifth
argument at `0030E62F`):

| bit | mask | effect |
|---:|---|---|
| 0 | `0x001` | skip both eligibility gates |
| 1 | `0x002` | skip the extra effect (`extraEffect = !(flags & 2)`, `0030E3F2`–`0030E400`) |
| 4 | `0x010` | skip the status-applied reaction (`showReaction = !(flags & 0x10)`, `0030E3EF`–`0030E3FC`) |
| 9 | `0x200` | skip the final recompute. **Set on every cascade call the operation makes on itself**, so a cascade never recomputes; also passed as the literal `0x217` by `BattleStats_RemoveStatusesFromMaskAndRecompute` (`0030F721`), which recomputes once itself |

## 3. Types

Physical offsets are kept beside the names. Full layouts are in the type store; the rows this
operation depends on are:

| type | size | the fields this operation touches |
|---|---:|---|
| `BattleStatsRecord` | `0x1C8` | `+0x2C` vitality (u8) · `+0x38` statusWord3 (u32) · `+0x3C` statusWord2 (u32) · `+0x48` currentHp (i32) · `+0x64` statusWord1 (u32) · `+0x68` / `+0x78` the two 16-byte status layers · `+0xBC[32]` statusParameterA (u32) · `+0x13C[32]` statusTimerWord (u16) |
| `BattleResultRecord` | `0x148` | built in the **caller's own stack frame** at `[rsp+0x80]` and cleared with a `0x148` fill (`0030E5D3`, `0030E5DB`); `+0x2C` flags, `+0x24` targetHpValue, `+0x5C[32]` parameterA, `+0xDC[32]` parameterB |
| `StatusDefinitionRecord` | **`0x28`** | `+0x06` class word, **bit 13 = harmful** · `+0x08` base duration, `0xFF` = none · `+0x09` duration unit for the beat timer · `+0x0C` clearMask |
| `BattleUnit` | `0xF50` | `+0x04` kind byte and `+0x05` type byte for the party-side shortcut; `+0xE9A` bits 0 and 1 |

> **`StatusDefinitionRecord` is 0x28 bytes, and the store said `0x10`.** Corrected here from the
> authored file's own header: `status_data.bin` is `1312` bytes, magic `st2e`, count `32` at `+4`,
> **stride `0x28` at `+8`**, rows from `+0x20` — and `0x20 + 32 × 0x28 = 1312` exactly, with no
> slack. Twenty-two of the twenty-four bytes past `+0x10` carry non-zero data in the shipped table,
> so the missing `0x18` is real content, not padding. §2.4a of the status page already referenced a
> `row.+0x20`, which a `0x10` record cannot contain.

**Reaching a definition row at run time** is three steps and a truncation, and the truncation is
part of the contract:

```c
hdr  = *(void **)0x02EBF118;              /* registry slot; null before the table loads */
base = ImageAddress_ResolveRuntimePointer(hdr->offset_0C);   /* 0020E600: zext32(arg) + *(0x01F83530) */
row  = (uint32_t)base + *(uint16_t *)((char *)hdr + 8) * status;   /* 32-BIT add - see below */
```

`0020E600` is three instructions: `mov eax, ecx` / `add rax, [01F83530]` / `ret` — a **32-bit
offset** added to a 64-bit runtime base. Both consumers then truncate the result back to 32 bits
(`0038770E add ecx, eax`; `0030E680 add ecx, eax`), so **the resolved table must lie below 4 GiB**
or every row address is wrong. That is an ABI constraint on the allocator, not a detail.

## 4. Preconditions · postconditions · invariants

**Preconditions.** `target` is a live `BattleStatsRecord`; the operation never null-checks it.
`source` may be null and is only used by the eligibility gates and by the `+0xE9A` markers. `mode`
must be `0..5`. The status definition table must be loaded **if any default is requested** — see
§10, where the absence is a fault rather than a fallback.

**Postconditions on a completed add** (`mode` 3 or 4): the bit is set in the chosen word; on `mode` 3
`+0xBC[s]` and `+0x13C[s]` hold the parameter and beat timer; every status named by the row's
`clearMask` is cleared; the reaction is enqueued unless `flags & 0x10`; the terminal case for that
status has run; and unless `flags & 0x200` the derived-state recompute has run.

**Invariants.**

1. **Presence is the union of two words, never one** — `(+0x3C | +0x64) & (1 << status)`
   (`0030E404`–`0030E41C`). `+0x38` is a third word that gates mode 3 and is *not* part of presence.
   **Across calls the presence word is not this operation's alone** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS blocks 301 and 305; bytes re-read.)*: with no explicit output block, the
   stat rebuild `BattleStats_RebuildEffectiveStatsAndAffinityState` points at `rec + 0x24` and zeroes, then rebuilds, `+0x24`–`+0x47`
   ([the stat-derivation contract](../08-Combat-Formula/CONTRACT-stat-derivation.md)), which includes `+0x3C`.
2. **No side effect fires unless presence changed** (`0030E5B7`–`0030E5CB`). Setting a status in one
   word while the other already holds it writes the bit and fires nothing. **One exception, §10 row 3** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS blocks 301 and 305; bytes re-read.)*:
   adding a terminal status to ~~a party-type unit~~ **a summoned Esper** *(corrected 2026-09-26, FABLE: type `0x1B..0x27` is exactly the thirteen Esper rows of the 40-row party table)* calls the defeat cleanup
   `00300FC0` at `0030E497` **before any mask
   write** and returns. That is a side effect with no presence change at all.
3. **Every mode refuses when the bit is already in the requested state**, so re-applying is a no-op
   ~~and a "refresh" is impossible without removing first.~~ **for this operation.** *(Scoped 2026-09-29, FABLE, Claude
   Opus 5.5, `_index/candidates/pkg-gp-status-poison/refresh.py` G A I C D.)* A refresh does happen one level up, for
   fourteen statuses. The candidate resolver lets an already-present status through only when its definition row's
   word `+6` has bit 5. Those statuses are Stop, Sleep, Confuse, Lure, Protect, Shell, Haste, Bravery, Faith, Reflect,
   Vanish, Regen, Float and Bubble. For them, the add operation writes the default duration and beat into the result
   record. The result applier then calls this operation, which refuses, but the applier's copy-through step still
   installs those timers. So re-casting Haste on a hasted target restarts its duration. Poison, whose bit 5 is clear, is
   skipped as "no effect", and its timers are left unchanged.
4. **The cascade cannot recurse indefinitely**: each cascade call is a *clear* (`mode 0`), and a
   clear of an absent status is refused by invariant 3 before it can cascade again.
5. The operation **never allocates**. Its result record is a stack block that dies with the frame.

## 5. State

| | fields / globals | evidence |
|---|---|---|
| read | `target +0x38 / +0x3C / +0x64 / +0x2C / +0x48`, unit `+0x04 / +0x05`, `*0x02EBF118` and its row, `*0x01DFE0B4` (the timer scale), `*0x01F83530` (the runtime base) | `0030E404`, `0030E478`, `0030E645`, `00387718` |
| written | `target +0x38 / +0x3C / +0x64`, `target +0xBC[s]` — **32 dwords**, `target +0x13C[s]` — **32 words**, unit `+0xE9A` bits 0–1, and — only through the defeat path — `0x02089340` bits `0x100 / 0x200 / 0x400 / 0x800` | `0030E4EA`–`0030E55A`, `0030E594`, `0030E5AF`, `0030E7B7`, `003010xx` |
| allocated | nothing | — |
| deallocated | nothing | — |

> **The two per-status array widths are established by the index scale, not assumed from the store.**
> `0030E594 mov dword [rsi + rdx*4 + 0xBC]` and `0030E5AF mov word [rsi + rcx*2 + 0x13C]` carry the
> **same index** in `rdx` / `rcx`, so the scales `*4` and `*2` are the strides, and each store fills
> its own stride exactly. A store width alone would not have settled this — a byte written into a
> dword slot looks identical at the instruction. It is the **shared index against two different
> scales** that fixes `+0xBC` at 32 dwords and `+0x13C` at 32 words, and that arithmetic is what
> makes §10 row 9a's overrun exact rather than approximate.

## 6. Relationships

**Callers: 14 sites in 10 functions**, including `BattleStats_ModifyHPAndProcessLethalState` (the KO
add and its removal), `BattleFormula_ApplyTargetResult`'s two mask loops, the two mode wrappers
`0030E990` / `0030EAE0`, `BattleStats_RemoveStatusesFromMaskAndRecompute`,
`BattleStats_RecomputeDerivedStateAndAutoStatuses`, and **itself**, for the cascade.

> **`0031B860` IS CALLED TWICE, AND SOURCE COMES FIRST.** `0030E381 mov rsi, rcx` keeps the
> **target** record; `0030E389 mov rcx, rdx` loads the **source**; `0030E39A` resolves the source and
> parks it at `[rsp+0x68]`; only then does `0030E39F mov rcx, rsi` / `0030E3A7` resolve the target
> into `rbx`. Its return is consumed as the `BattleUnit` pointer. **The resolve order above is OPUS's
> own reading of the image; that the gates then take `(target-unit, source-unit)` is `EXP-086`'s
> measurement and is NOT independently re-derived here** — the distinction is kept because this
> contract has twice been wrong by restating someone's result as if it were read. A reimplementation
> that resolves in written order, or that
> passes the units the way the records arrive, inverts both gates — and because `source` may legally
> be null (§4) the inversion shows up as a *missing* refusal rather than a crash.

**Callees that matter to a reimplementation:** `0031B860` (record → unit), `0030B9B0` / `0030B8E0`
(the two eligibility gates), `00387730` / `003876D0` (the two defaults), `00386A50` / `00386A70`
(the transition builders), ~~`003112F0` (the applier),~~ `003284D0` (the reaction), `0046A800` (the
extra effect, statuses 1 and 31 only), `00300FC0` (defeat cleanup), `00312280` (rewards),
`00301140` (recover), `0030FED0` (the recompute).

> ~~**`003112F0` IS STRUCK FROM THIS LIST: IT CAN NEVER FIRE THROUGH `0030E360`.**~~ **`003112F0` stays on this list: it fires through `0030E360` for exactly one transition, removing status 28 with a non-zero `+0x48`** *(corrected 2026-10-02, OPUS: for id `0x1C` with `[rsi+0x48]` non-zero, `00386A70` returns at `00386AC2` without reaching `00386AC3`, so bit 0 stays set and `0030E610` lets `0030E638 call 003112F0` run; §13's builder table gives the same mask, `0x109`)*. Refuted by
> [`EXP-086`](../_experiments/EXP-086-status-write-execution.md) — **zero calls across all 67 cases**
> — and verified independently by OPUS from the authority image, because a reimplementer told to
> reproduce a callee that cannot be reached would be reproducing nothing:
>
> ```
> 0038498D  or   dword [rbx+0x2C], 1            003848E0 SETS the gate bit
> 00386A66  and  dword [rbx+0x2C], 0xFFFFFFFE   builder A CLEARS it
> 00386AC3  and  dword [rdi+0x2C], 0xFFFFFFFE   builder B CLEARS it, except for status 28 with +0x48 non-zero, which returns at 00386AC2 first (corrected 2026-10-02, OPUS)
> ```
>
> ~~**Both builders clear the one bit the setter sets**, and every path to the applier runs through a
> builder, so the gate is closed before it is ever tested. **A static call graph shows the edge and
> the edge is dead**~~ Both builders clear the bit on every path but one: the remove builder leaves it set for status 28 with a non-zero `+0x48`, so the gate is open for that removal and the edge is live *(corrected 2026-10-02, OPUS: `00386A94`–`00386AC2`, `0030E610`–`0030E638`)* — which is exactly the class this contract's §13 exists to catch and exactly
> what an execution finds that a reading does not. The function is real and does real work for
> *other* callers (§17 records its audio and its stolen-item grant); ~~what is false is listing it
> among the callees a reimplementation of **this** operation must provide.~~ a reimplementation of **this** operation must provide it for the status-28 removal *(corrected 2026-10-02, OPUS: see the correction above)*.

## 7. State transitions

**The mask write is six modes over three words**, and each refuses when the bit is already in the
requested state:

| mode | word | direction | extra refusal |
|---:|---|---|---|
| 0 | `+0x64` | clear | — |
| 1 | `+0x3C` | clear | — |
| 2 | `+0x38` | clear | — |
| 3 | `+0x64` | set | also refuses when the bit is set in `+0x38` (`0030E531`) |
| 4 | `+0x3C` | set | — |
| 5 | `+0x38` | set | — |
| >5 | — | — | returns immediately (`0030E4CB`) |

`adding = (mode == 3 || mode == 4)` (`0030E3C2` `lea ecx,[rdx-3]` / `cmp ecx,1` / `setbe`);
`initialises = (mode == 0 || mode == 3)` (`0030E3CF`–`0030E3E0`) and only those two write the
per-status arrays.

**The terminal switch** is a two-level table, decoded here from the image rather than copied: the
byte table at `0030E8C4` holds one case index per status, and the dword table at `0030E8A4` holds
eight image-base-relative targets (`0030E740`–`0030E759`, base `rdx = 0x00120000`).

| case | target | statuses | what it does |
|---:|---|---|---|
| 0 | `0030E80A` | **0** KO | add → defeat cleanup + `BattleUnit_ProcessDefeatRewardsAndLoot`; remove → recover |
| 1 | `0030E850` | **1** Stone | add → event `0x200C`, then cleanup + rewards; remove → recover |
| 6 | `0030E85E` | **31** ~~Vanished~~ X-Zone *(corrected 2026-10-02, OPUS: id 31 is X-Zone in the thirty-two statuses §2; "Vanish" is id 24, Invisible)* | add → event `0x200E`, then the same; remove → recover |
| 2 | `0030E7DD` | **2** Petrify | unit `+0xE9A` bit 1 := `adding && source is a kind-0 record` |
| 5 | `0030E7B3` | **8** Poison | unit `+0xE9A` bit 0 := the same predicate |
| 3 | `0030E75B` | **4** Sleep | event `0x2001`, on add and on remove alike |
| 4 | `0030E770` | **5** Confuse, **27** Berserk | `BattleUnit_ResetActionControlForStatusTransition`, then `BattleUnit_UpdateEngagementStateFlag` |
| 7 | `0030E816` | the other 24 | ~~nothing~~ the shared tail only: `0030FED0` unless `flags` bit 9 *(corrected 2026-10-02, OPUS: `0030E816`–`0030E828`; §15a)* |

> **Doom (6) has no terminal case**, though it ends the unit. It reaches KO through the periodic
> tick's countdown instead, never through this switch — a distinction a reimplementation that
> equates "terminal status" with "terminal case" will get wrong. The three statuses the *gates*
> treat as terminal are the mask `0x80000003` — KO, Stone and Vanished — which is a third, narrower
> set than either.

## 8. Script · resource · event interactions

**`status_data.bin`** (`ps2data/image/ff12/test_battle/in/binaryfile/`, 1,312 B, magic `st2e`),
behind registry slot `0x02EBF118`, decides what this operation does for each status. The shipped
table, decoded whole:

| column | what the code does with it | the shipped values |
|---|---|---|
| `+0x06` bit 13 | selects the Vitality direction in the default duration | set on exactly ids **0–16, 29, 31** — the harmful class |
| `+0x08` | base duration; `0xFF` means the status never expires | a duration on **21** ids, `0xFF` on **11** — ids 0, 1, 2, 6, 7, 9, 10, 11, 16, 29, 31 |
| `+0x09` | the beat unit, scaled to `+0x13C[s]` | non-zero on five only: Petrify 45, Doom 100, Poison 120, Sap 1, Regen 15 |
| `+0x0C` | the cascade: statuses this one clears | non-zero on **eight** ids: KO clears 25 statuses, Vanished 29, Stone 12, and five single-target rows — Stop→Lure, Sap→Regen, Regen→Sap, Slow→Haste, Haste→Slow |

Events `0x200C` (Stone) and `0x200E` (Vanished) go to `BattleUnit_DispatchActorPresentationEvent`;
`0046A800` posts `0x12` and `0x11` for the same two through the battle event poster.

## 9. Determinism

**No RNG here.** The operation draws nothing. The status *system* draws once — Regen's per-beat heal
uses `RNG_MT19937_NextU32` in the tick's stage 2 — and that is the tick's contract, not this one.

**Ordering.** Called from the applier's two mask loops, from the HP write's lethal transition~~, and
from the tick~~ *(corrected 2026-10-02, OPUS: `00310DB0` has no call to `0030E360`; the two meet only at `003112F0`, CONTRACT-periodic-tick.md §6, and §6's caller list here has no tick)*. Within the operation the order is fixed and observable: mask → arrays → presence test
→ result record → applier → cascade → reaction → extra effect → terminal case → recompute. **The
cascade runs before the reaction**, so a cascaded removal's own effects land first.

**Threading.** Single-threaded battle update; nothing here synchronises.

## 10. Failure paths and edge conditions

| # | condition | result |
|---:|---|---|
| 1 | `flags` bit 0 clear and `BattleTarget_HasLow16EligibilitySuppression` non-zero | refuse, silently |
| 2 | adding, bit 0 clear, `HasHigh16EligibilitySuppression` non-zero, **and the status is terminal** (`bit & 0x80000003`) | refuse |
| 3 | adding a terminal status to ~~a **party-type** unit~~ **an Esper** (kind `+5 == 0`, type `+4` in `0x1B..0x27`, the thirteen Esper rows) | **defeat cleanup only, and return** — the masks are never touched, ~~which is why a party member's KO posts no rewards~~ so a summoned Esper's KO posts no rewards. *Corrected 2026-09-26 (FABLE): a party member (row 0, rows `0x1A` / `0x28`) takes the full path of reaction, defeat and rewards; `s26-opus-replay-status-write/row3.py` E1/E2.* |
| 4 | adding a terminal status to a unit that already has one, without `FieldData_GetActiveFieldRecordBit15` | refuse |
| 5 | `mode > 5` | return |
| 6 | the bit is already in the requested state | refuse |
| 7 | mode 3 and the bit is set in `+0x38` | refuse |
| 8 | presence unchanged across the write | the bit is written and **no side effect runs** |
| 9 | `status > 31` | the terminal switch is skipped (`0030E737 cmp ecx, 0x1F` / `ja`), and **everything before it still runs against the WRONG BIT**: `0030E410 shl edi, cl` masks the count to five bits, so a status of 32 builds KO's bit and writes it. **The bit is masked to five bits and the ARRAY INDEX IS NOT** — see the row below. No caller passes one *(two sites bounded 2026-10-01, OPUS, on ASTRA's `ov58d-order-switch/`, ACCEPT by SWE2-AUDIT-SPEC, `_index/candidates/auditspec-review-astra-ov58d-order-switch-1001/`, re-read by OPUS: in the order handler `002FDDA0` the first switch sends messages `0x4051`-`0x4070` to `002FDF18`, whose `lea r8d, [rdx - 0x51]` makes the status byte 0..31 for the call at `002FDF40` (mode 3, both params -1), and `0x4071`-`0x4090` to `002FDF5A`, whose `lea r8d, [rdx - 0x71]` does the same for `002FDF79` (mode 0, params 0); target and source are both the unit's `+0x698`. `0x4049` / `0x404A` take selector 1 to `002FDE7B`, which stores `dl - 0x48` to the unit's `+0x54`, sets `+0x6B4` = 2 and returns 1 without a call, so they never reach either site. Other callers' domains, and natural reachability of these messages, are not established by this)*; a reimplementation that range-checks here would not be reproducing the original |
| 9a | `status == 32` **and** `mode == 3` | **both per-status writes land outside their own array.** The index comes from `0030E588 movzx edx, byte ptr [rsp + 0x40]`, the raw status byte, with no five-bit mask anywhere on that path. `0030E594 mov dword [rsi + rdx*4 + 0xBC]` puts `paramA[32]` at `+0xBC + 0x80` = **`+0x13C`, which is `timer[0]`**, and `0030E5AF mov word [rsi + rcx*2 + 0x13C]` puts `timer[32]` at **`+0x17C`, one entry past the timer array**. The two arrays are adjacent and differently scaled, so the overrun of the first is exactly the head of the second |
| 10 | **the definition table is not loaded and a default is requested** | **BOTH DEFAULTS FAULT, AT TWO DIFFERENT ADDRESSES.** `003876D0` (the `paramB` short timer, taken when `paramB < 0`): `003876E2` and `003876EF` jump to `00387712 xor ecx, ecx`, and `00387714 movzx eax, byte ptr [rcx + 9]` reads virtual address **`9`**. `00387730` (the `paramA` duration, taken when `paramA < 0`): `0038776C` jumps to `003877A3 mov rcx, rbx` with `rbx` zeroed at `00387767`, and `003877A6 cmp byte ptr [rcx + 8], 0xFF` reads virtual address **`8`**. Neither is a fallback; each is a null dereference on the "no table" path, and **a reimplementation that gives them a shared guard is reproducing neither** |
| 10a | the table is not loaded, a `paramA` default is requested, **and the status is 2 or 6** | **no fault — these two never reach the table.** `00387740 cmp r8d, 2` / `jne` and `00387756 cmp edi, 6` / `je` both land on `00387746 mov eax, 0xB` and return, **before** `0038775B` loads the registry slot at all. Petrify and Doom take a hardcoded `0xB` whether or not `status_data.bin` exists, which is why row 10's fault is not reachable for the only two statuses whose counter the player can actually read |

> ~~**Row 10 is a difference between two siblings that read the same table.** The cascade's own read~~
> ~~of the same slot guards properly: `0030E64F` and `0030E65C` jump to `0030E686 xor edx, edx`,~~
> ~~giving an empty clear mask and no dereference. **Same table, same two null checks, one path~~
> ~~degrades and the other faults.**~~ A reimplementation that "helpfully" returns 0 from the timer
> default is not reproducing the original; one that faults is. Whether the path is reachable in a
> shipped session is `SW-1`.
>
> **REFUTED 2026-09-16 by `EXP-086` (SWE2-ORACLE, isolated original-code execution, 67 cases, 9/9
> mutants), verified independently by OPUS from the authority image. THERE IS NO DIFFERENCE BETWEEN
> THE SIBLINGS — BOTH FAULT, AND THE CONTRAST THIS NOTE WAS BUILT ON DOES NOT EXIST.** The cascade
> does not degrade:
>
> ```
> 0030E684  jmp  0030E68A            <- the fall-through lands on the SAME instruction
> 0030E686  xor  edx, edx
> 0030E688  mov  ecx, edx            <- ecx = 0, and a 32-bit write CLEARS the upper half of rcx
> 0030E68A  mov  eax, dword [rcx+0xC]  <- read at virtual address 0xC. Fault.
> ```
>
> `0030E686` is two instructions, not one, and the second is what this note missed: the zero reaches
> `rcx` and there is no guard between it and the dereference. **The "empty clear mask" never
> happens** — nothing consumes a mask before the read faults. It is a null dereference on the "no
> table" path exactly as row 10 describes for the timer default, for both the registry-null and the
> resolved-base-null cases.
>
> **WHAT THE ERROR WAS, because it is a class and not a slip:** this note read the `jcc` TARGET and
> stopped there. `xor edx, edx` at the target genuinely looks like a safe degradation, and it is —
> until the next instruction moves it into the register the dereference uses. **A jump target is not
> a basic block**, and reading the first instruction of one is the same mistake as reading a store
> width and calling it a field width. Row 10 stands, unchanged and now unexceptional.

## 11. Observable behaviour

From outside, without a debugger: the status icon; the Petrify/Doom counter, which the display shows
as `+0xBC[s] − 1`; a character dropping and the party collecting rewards (foe) or not (~~party-side~~ a summoned Esper; a party member takes the full path of reaction, defeat and rewards, §10 row 3 *(corrected 2026-10-02, OPUS)*);
Haste and Slow cancelling each other; ~~a status refusing to refresh when re-cast~~ a re-cast restarting the
duration of the fourteen refreshable statuses (invariant 3) and doing nothing to the others, Poison among them. In memory:
`target +0x38 / +0x3C / +0x64`, `+0xBC[32]`, `+0x13C[32]`, unit `+0xE9A` bits 0–1, and
`0x02089340`'s four defeat latches.

## 12. Reproduction formula

```c
adding      = (mode == 3 || mode == 4);
initialises = (mode == 0 || mode == 3);
bit         = 1u << status;
wasPresent  = ((target->w_3C | target->w_64) & bit) != 0;

if (!(flags & 1)) {
    if (Low16Suppression(targetUnit, sourceUnit))                       return;
    if (adding && High16Suppression(...) && (bit & 0x80000003u))        return;
}
if (adding) {
    if (unit->kind == 0 && unit->type >= 0x1B && unit->type <= 0x27 && (bit & 0x80000003u)) {
        DefeatCleanup(unit, 0);                                          return;   /* party side */
    }
    if ((bit & 0x80000003u) && ((target->w_3C | target->w_64) & 0x80000003u)
        && !FieldRecordBit15())                                          return;
}
switch (mode) { /* 0,1,2 clear +0x64,+0x3C,+0x38 ; 3,4,5 set them ;
                   every case returns if the bit is already in that state;
                   mode 3 also returns if (target->w_38 & bit) ; default: return */ }

if (initialises) {
    target->parameterA[status] = (paramA >= 0) ? paramA : DefaultDuration(0, target, status);
    target->timerWord[status]  = (paramB >= 0) ? paramB : DefaultBeat(status);
}
if ((((target->w_3C | target->w_64) & bit) != 0) == wasPresent)          return;   /* nothing fires */

uint8_t rec[0x148];  memset(rec, 0, 0x148);
(adding ? BuildAdd : BuildRemove)(target, status, rec);
if (rec.flags_2C & 1) ApplyTargetResult(rec, NULL, target, 0xFFFF, flags);
if (adding)
    for (i = 0; i < 32; i++)
        if (statusRow(status)->clearMask & (1u << i))
            ChangeStatus(target, source, i, 0, 0, flags | 0x200, /*mode*/ 0);
if (adding && !(flags & 0x10) && targetUnit) EnqueueStatusReaction(targetUnit, status);
if (!(flags & 2))                            ExtraEffect(target, status);   /* ids 1 and 31 only */
if (targetUnit && status <= 31)              TerminalCase[byteTable[status]](...);
if (!(flags & 0x200))                        RecomputeDerivedStateAndAutoStatuses(target, flags);
```

**The two defaults, with real constants:**

```c
DefaultBeat(s)  = statusRow(s)->durationUnit /* +0x09 */ * (*(uint32_t *)0x01DFE0B4) * 30;

DefaultDuration(_, target, s):
    if (s == 2 || s == 6)             return 11;              /* Petrify / Doom: a COUNT */
    row = statusRow(s);
    if (row->base /* +0x08 */ == 0xFF) return 0;
    vit = target ? target->vitality /* +0x2C */ : 0;
    if (row->cls /* +0x06 */ & 0x2000) v = trunc(2.0*row->base - row->base*vit/100.0);
    else {                             v = trunc(row->base + row->base*vit/100.0);
                                       if (effect 30 in either layer) v = trunc(v * 1.5); }
    return (*(uint32_t *)0x01DFE0B4) * v * 300;
```

`*(0x01DFE0B4)` is the frame base — 1 at 30 fps, 2 at 60 — so the parameter is `v × 300`
frame-units at 30 fps and the beat is `row.+0x09 × 30`.

## 13. Runtime validation

**Evidence class: isolated original-code. There is still no live evidence.** ~~for the ARITHMETIC
half only ... and the operation `0030E360` itself is still unexecuted.~~

> **CORRECTED 2026-09-16 (OPUS). `0030E360` WAS EXECUTED ON 2026-09-13 AND THIS SECTION WENT ON
> CALLING IT UNEXECUTED.** [`EXP-086`](../_experiments/EXP-086-status-write-execution.md)
> (SWE2-ORACLE, method B, isolated original-code under Unicorn against the shipping EXE) takes
> `0030E360 BattleStats_ChangeStatusAndProcessSideEffects` as its subject — **the exact function
> this sentence called unexecuted** — and reports **67/67 cases pass, 9/9 byte-level mutants
> detected**.
>
> Found by `check_experiments.py`, which lists EXP-086 under **NOT CITED — a RUN experiment its
> contract never names** *and exits 0*, so nothing had to look. The missing back-link was not a
> broken hyperlink; it was hiding a claim the corpus had already refuted. Four contracts were in
> this state at the same HEAD.
>
> **Isolated original-code is not live evidence**, and this correction does not move that rung: the
> operation ran under a fixture, not in a game.

| what | pilot | cases | mismatches |
|---|---|---:|---:|
| the record initialiser, both transition builders, the timer default and the pointer resolver — `003848E0`, `00386A50`, `00386A70`, `003876D0`, `0020E600` | [`diff_status_write.py`](../../../Reconstruction/Tests/Differential/diff_status_write.py) — the **41st** | 155 | **0** |
| the operation `0030E360`, the cascade, the terminal dispatch | [`EXP-086`](../_experiments/EXP-086-status-write-execution.md) — isolated original-code, Unicorn ~~—~~ | 67 | **0** (9/9 mutants detected) ~~**not executed**~~ |

~~**Only `memset` is scripted.**~~ **Not only `memset`** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS blocks 301 and 305; bytes re-read.)*. EXP-086 itself records that **fourteen deep
side-effect callees are `ret`-stubbed** at their real entries, and that the unit lookup `0031B860` is stubbed, so
the unit-versus-null distinction is fixture input. The sentences below describe the `memset` import, which is
one of those scripted pieces; "everything else runs" holds only for the operation's own body. `003848E0` reaches `memset` through the IAT thunk at `00861EC0`, whose slot
`008C2A60` is `VCRUNTIME140.dll!memset` — **an import, so its body is not in the shipped image** and
no fixture can run it from there. Everything else runs, `0020E600` included. The suite compares all
`0x150` bytes of the record, all `0x60` bytes of the unit, and the returned value.

### What execution measured

**Nothing here was refuted.** The static reading held everywhere the pilot reached, so what follows
is measurement rather than correction — and three of these were claims no run had ever touched.

| what | measured |
|---|---|
| **§15's truncation claim, executed at last** | with the image base at `0x100000000` and the encoded pointer `0x00500000`, two DIFFERENT tables were planted — one at the full `0x100500000`, one at the truncated `0x00500000`. **The byte that came back is the truncated table's.** The `add ecx, eax` at `0038770E` decides the address |
| the resolve **zero-extends** | an encoded `0x80000000` over a base of `0x10000` reads `0x80010000`, not a sign-extended address nearly 2 GB below it. `0020E600`'s `mov eax, ecx` is what does it |
| **§10 row 10, and it is sharper than "it faults"** | with the handle NULL the function reads **`[0 + 9]`** and returns that byte × the multiplier × 30. Over a page whose byte 9 is `9`, it returned **270**. The second refusal — a resolve that returns zero — takes the **same** read |
| the record's extent, and its first eight bytes | the `memset` covers `+0x08`–`+0x147`, so **`0x148` is confirmed by execution**. `+0x00`–`+0x07` come back **exactly as the caller left them** — a fixture handing the initialiser zeroed memory could never have shown that |
| the row index is unguarded in **both** directions | status id `-1` read the marker planted one row **before** the table; ids past the planted rows read on |
| a timer default can be **negative** | a multiplier of `-1` returned `-4380`. The product is signed throughout |
| **the two defaults differ by a factor of TEN** | `003876D0` ends `0038771F imul eax, eax, 0x1E`; `00387730` ends `00387992 imul eax, eax, 0x12C`. Both read the same global `[01DFE0B4]`, both take a status id, and they sit `0x60` bytes apart — **checked 2026-09-12 because the pilot drove one of them and the register's `FA-1` had answered the other** |

### `EXP-086`'s remaining findings, consumed 2026-09-17 (OPUS)

The two **refuted** findings went first, because they made this contract *wrong* rather than
incomplete: the null-table cascade (§10, `74a19fe0`) and the struck applier `003112F0` (§6,
`a8a29b0f`). These seven are the rest. **Every row marked *re-derived* was disassembled from the
authority image by OPUS before it was written down** — not to doubt the pilot, but because a contract
that restates a result it cannot check has no way to notice when the result is about a different
population, which is the failure this corpus has corrected eight times today.

| # | finding | status here |
|---:|---|---|
| 3 | the two defaults fault at **different** virtual addresses — `8` for `00387730`, `9` for `003876D0` | **re-derived**, and written into §10 rows 10 and 10a. The re-derivation added something the finding did not state: statuses **2 and 6 return `0xB` before the table is touched**, so the `paramA` fault is unreachable for exactly the two statuses whose counter is on screen |
| 4 | measured defaults against the real `status_data.bin` | **re-derived as formulas**, below |
| 5 | `0031B860` runs on **source** then **target**; its return is the `BattleUnit` | **re-derived** (the resolve order) and written into §6; the gate argument order is carried as the pilot's measurement, not as a reading |
| 6 | `__security_check_cookie` additionally requires the cookie's **top 16 bits to be zero** | **re-derived.** `00808C4A rol rcx, 0x10` then `00808C4E test cx, 0xFFFF` tests what were the high 16 bits; non-zero falls to the failure path at `00809654`. The shipped cookie `00002B992DDFA232` satisfies it, so **a fixture that plants a cookie with any high bit set fails the epilogue for a reason that has nothing to do with this operation** |
| 7 | presence is `(+0x3C \| +0x64)` **only**, so a `+0x38` write fires nothing | **re-derived**, and it is stronger than invariant 1 implied: modes 2 and 5 write `+0x38` at `0030E564` and then fall straight into the same presence test at `0030E5B7`–`0030E5BD`, which reads only the other two words. The write **lands**, presence is unchanged, and the operation returns through the early exit. A reimplementation that treats `+0x38` as a third presence word fires side effects the original never fires |
| 8 | status 32 writes KO's bit and overruns both per-status arrays | **re-derived**, and written into §10 rows 9 and 9a with the exact landing offsets |
| 9 | the row-4 predicate: `dword[unit]` bit 24 **denies**; `word[+0x714] > 0x21E` skips the `byte[+0x6B4] >= 9` check; `== 0x113` denies | **carried, NOT re-derived.** It lives inside `FieldData_GetActiveFieldRecordBit15`, a different function with its own contract, and OPUS did not open it. Recorded here as the pilot's measurement so §10 row 4 stops reading as an opaque call, and flagged so nobody cites it as this contract's own reading |

**The measured defaults, as formulas rather than as one status's numbers.** `003876D0` is fully
determined by the image: `00387714` reads `byte[row + 9]` — the beat unit §8 already documents —
`00387718 imul eax, [01DFE0B4]` and `0038771F imul eax, eax, 0x1E` finish it, so

```
paramB default = statusRow[+0x09] * [01DFE0B4] * 30
```

which is exactly what the pilot measured. `00387730` is the longer one: the `0x2000` bit tested at
`00387806 test word [rcx + 6], ax` selects the Vitality-scaled float path, the vitality byte is
`003877BA movzx r14d, byte [rsi + 0x2C]`, and the divisor is the `.rdata` constant at `0x8F3134`.
The pilot's **status 8 paramA = 90000** is the shipped table's `duration 50` through that path.

> **THE SINGLE NUMBER IS NOT THE FINDING AND MUST NOT BECOME THE CITATION.** `90000` is one status's
> value under one shipped table; the reproducible facts are the **path selector**, the **operand
> addresses** and the **two multipliers**. This contract has already been burned once by an exact
> number that proved a structure it did not prove — `0x2300 = 560 × 16` was a GS cookie offset, not a
> record count — and a default quoted without its divisor is the same shape of citation.

### `SW-2` is answered — what the builders write beyond the initialiser

| | `00386A50` (apply) | `00386A70` (remove) |
|---|---|---|
| the `+0x2C` mask | clears bit 0, always | status 28 **with a non-zero `+0x48`**: ORs `0x108` — and **leaves bit 0 set, so the mask is `0x109`**, the initialiser having set it. Otherwise clears bit 0, giving `0` |
| `+0x24` | never written | that arm only: `(unit[+0x48] + 1) / 2`, **rounding toward zero** |
| the status id | **not read at all** | read, and compared against 28 |
| the unit | **not written** | **not written** |

Measured halvings: `1 → 1`, `2 → 1`, `7 → 4`, `-1 → 0`, `-7 → -3`, and `0x7FFFFFFF → -1073741824`,
because `inc eax` overflows before the shift. A reconstruction using an arithmetic shift alone
differs on every negative counter.

> **"Neither builder writes the unit" was a claim until 98 cases compared all `0x60` bytes of it.**
> That is the cheapest kind of check to leave out and the kind a reader most reasonably assumes.

**Mutation campaign: 98 points — 77 KILLED, 18 SURVIVED,
3 EQUIVALENT, 0 TIMEOUT, 0 INVALID. Status `FAIL`.** Three earlier
runs are kept beside it, and the reason they are worth keeping is that **every INVALID in them was
the instrument's fault, not the reconstruction's**: the harness crashed on the driver's own refusal
word, the driver aborted instead of reporting a case whose memory it could not plant, and it printed
hex *and then* the refusal word so the field parsed as neither. Twelve mutants that had plainly
broken the reconstruction were scored unevaluable. Fixing the instrument took INVALID from 7 to 0
and KILLED from 68 to 77.

### Every non-kill, adjudicated

- **2 are kind A, provable equivalences**, and both say something about the original. Growing
  the initialiser's fill loop by one iteration writes `0xFFFF` over two places that already hold
  `0xFFFF`. And changing the remove side's `0x108` to `0x109` cannot be seen **because bit 0 is
  already set** — which is exactly why the measured mask is `0x109`.
- **15 are kind B, the fixture's address-space model**, which the originals have no counterpart
  for at all: the values it returns when it refuses a read, its capacity, its overlap check, and its
  two write widths. Most are unkillable by construction — any case that makes the model refuse is
  **already** a mismatch, so the case that would kill them cannot exist. The two write widths have a
  structural reason instead: `003848E0` memsets `+0x08`–`+0x147` in one call and every field it
  later writes lies inside that range, so **no region boundary can touch a write's last byte without
  splitting the memset**.
- **1 is kind C, undefined behaviour**: a `memcpy` of nine bytes into an eight-byte object.
- **3 EQUIVALENT** compiled to byte-identical code — two `memcpy` widths and a shift
  count of 32, which x86 masks to 31.
- **Two survivors were killed by driving the fixture's own edge**: a rows buffer that ends
  immediately after the timer byte, and a table handle described as two adjacent regions with the
  boundary immediately after its stride field. **A bound no case touches is a bound nothing checks**,
  including one the fixture added itself.

**No kind D remains.**

Receipts: `Database/Tools/work/OPUS/litsuffix/status_write`, `status_write2`, `status_write3` and
`status_write4` (ignored path), and the counts row in
[`MUTATION-CAMPAIGNS.md`](../../../Reconstruction/MUTATION-CAMPAIGNS.md).

**The live half stays queued, and none of it has been performed.** The three observations that would
move it, each with the state it needs: (a) cast Slow on a Hasted character and read `+0x3C`/`+0x64`
before and after, which settles the cascade end to end; (b) read `+0xBC[2]` on a Petrified unit
across ticks and confirm the displayed counter is `value − 1`; (c) KO a party member and a foe in the
same battle and compare `0x02089340`.

## 14. Unresolved

1. **`SW-1` — is §10 row 10 reachable in a shipped session?** The timer default faults when the
   status table is not loaded. Nothing establishes whether a status can be applied before the table
   loads. *Resolved by*: a breakpoint on `003876D0` with `*0x02EBF118` null, or a static proof that
   every caller runs after the table load.
2. ~~**`SW-2`**~~ — **ANSWERED 2026-09-12 by the 41st pilot**, and the answer is in §13: the apply
   side clears bit 0 of `+0x2C` and does nothing else; the remove side's status-28 arm sets `0x108`
   over an already-set bit 0 and writes the halved counter to `+0x24`. Neither writes the unit.
   **What is still not established is what the mask BITS mean** — `0x108` names two bits whose
   consumers are not identified, and that is now carried by `SW-3`'s neighbourhood rather than by
   this item.
3. **`SW-3` — the 24 bytes of `StatusDefinitionRecord` past `+0x10`**, 22 of which carry data in the
   shipped table. ~~Only `+0x20` has a known consumer (calculator slot 118's exclusion test).~~ *(answered: see the-thirty-two-statuses.md §4 — the query arm copies `+0x10`, `+0x26`, `+0x27` and `+0x13` into its record, and `+0x02` and `+0x24` are read too; `+0x20` remains calculator slot 118's exclusion test; 2026-10-02, OPUS)*
4. **`SW-4` — what `0046AB10` does with codes `0x12` and `0x11`** beyond posting the event.
   **Widened 2026-09-12**: `0046AB10` is also reached from `004697C0`, whose three callers are the
   action lifecycle — `BattleUnit_TrySelectAndCommitAiOrderFromSet`, `BattleUnit_AdvanceActionState`
   and `BattleAction_CheckAndHandleExecutionTimeout`.
   [The gambit walk](../09-Combat-AI-And-Gambits/CONTRACT-gambit-walk.md) §14 carried `004697C0` as
   its own unidentified callee. **The two open questions are about one posting path**, and answering
   either needs the same reading.

## 15. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| the seven parameters and their registers | `0030E360`–`0030E3AC` read; the two stack arguments at `[rsp+0x228]` and `[rsp+0x230]` | 1 | PROVEN |
| `adding`, `initialises`, `showReaction`, `extraEffect`, `bit`, `wasPresent` | re-derived independently 2026-09-12 from `0030E3BB`–`0030E41C`; agrees with the page's §2.1 table in all six rows | 1 | PROVEN |
| presence is `+0x3C \| +0x64`, and `+0x38` is not part of it | `0030E404`–`0030E407`, `0030E5B7` | 1 | PROVEN |
| the six modes and their already-in-state refusals | the page's §2.3, from the jump table at `0030E88C`; not re-derived here | 1 | PROVEN |
| the terminal dispatch: 8 targets, one case per status, and which statuses share a case | **decoded from the image by this contract** — byte table `0030E8C4`, dword table `0030E8A4`, base `0x00120000` from `0030E740`; every one of the 32 entries resolved. Agrees with the page's §2.7 exactly | 1 | PROVEN |
| Doom has no terminal case | the same decode: id 6 → case 7 → `0030E816`, the do-nothing target | 1 | PROVEN  **§15a, 2026-09-12 — the mapping is confirmed and the phrase is not.** `0030E816` is **not a do-nothing target**: it is the **shared tail every one of the eight cases reaches** — case 0 falls through into it, cases 1–6 `jmp` to it, and case 7 *is* it — and it runs `bt eax, 9` on the sixth parameter and, when that bit is **clear**, calls `0030FED0 BattleStats_RecomputeDerivedStateAndAutoStatuses` (1,787 B, this subsystem). What case 7 lacks is a **status-specific body**, which is what this claim means and all it should be read as saying |
| **the beat default's ×30 and the duration default's ×300 are different scales, not a typo in either** | **re-read 2026-09-12**: `0038771F imul eax, eax, 0x1E` against `00387992 imul eax, eax, 0x12C`, both over the same `[01DFE0B4]`. `FA-1` in the register answers `00387730` at ×300 and this table answers `003876D0` at ×30; **both are correct** | 1 | PROVEN |
| the beat default is `row.+0x09 × [01DFE0B4] × 30` | `003876D0`–`00387727` read whole 2026-09-12: `movzx eax,[rcx+9]`, `imul eax,[01DFE0B4]`, `imul eax,eax,0x1E` | 1 | PROVEN |
| the duration default's formula, classes and the ×1.5 | the page's §2.4a, from `00387740`–`00387992`. **The head is re-derived here** — `00387740 cmp r8d,2` / `00387756 cmp edi,6` → `mov eax,0xB`, so the constant 11 for ids 2 and 6 is confirmed; the Vitality arms are not re-read | 1 | PROVEN |
| the definition record is `0x28` bytes, not `0x10` | `status_data.bin` header: stride `0x28` at `+8`, count 32 at `+4`, rows at `+0x20`, and `0x20 + 32 × 0x28 = 1312` = the file size, exactly. **Corrects the type store** | 1 (corpus) | PROVEN |
| bit 13 of `+0x06` is set on exactly ids 0–16, 29, 31 | **all 32 rows decoded and the predicate checked**; the page's claim holds | 1 (corpus) | PROVEN |
| `+0x08` is a duration on 21 ids and `0xFF` on 11 | the same decode; the eleven are 0, 1, 2, 6, 7, 9, 10, 11, 16, 29, 31 | 1 (corpus) | PROVEN |
| the cascade masks, including Stone→Petrify and Haste↔Slow | the same decode: **eight** rows carry a non-zero `+0x0C` — ids 0, 1, 3, 10, 15, 20, 25 and 31. I wrote seven first and the count is from the decode, not the prose | 1 (corpus) | PROVEN  **§15a: re-decoded from the shipped file and the eight are complete — ids 0, 1, 3, 10, 15, 20, 25, 31**, masks `7FFEF57C`, `1FFC0004`, `00020000`, `02000000`, `00100000`, `00008000`, `00000400`, `7FFFFFFC` |
| the result record is `0x148` and lives in the caller's frame | `0030E5D3 lea rcx,[rsp+0x80]`, `0030E5DB mov r8d,0x148`, and the `0x1E0` frame with its cookie at `+0x1D0`. **Corrects the type store**. **EXECUTED**: `003848E0`'s memset covers `+0x08`–`+0x147` | 1 | PROVEN |
| **the initialiser leaves `+0x00`–`+0x07` exactly as the caller left them** | **EXECUTED**: the record is handed over pre-filled with `0xC7`, `0x00` and `0xFF`, and those eight bytes come back unchanged in each | 1 | PROVEN |
| the table pointer is resolved and then truncated to 32 bits | **EXECUTED**: two different tables planted, one at the full `0x100500000` and one at the truncated `0x00500000`, and the byte returned is the truncated one's. Read statically at `0038770E` and `0030E680` | 1 | PROVEN |
| **`0020E600` ZERO-extends the encoded value** | **EXECUTED**: an encoded `0x80000000` over a base of `0x10000` reads `0x80010000`, not an address 2 GB below it. `mov eax, ecx` before the 64-bit add | 1 | PROVEN |
| the timer default faults when the table is absent ~~while the cascade degrades~~ and so does the cascade (`0030E686`–`0030E68A`) *(corrected 2026-10-02, OPUS: §10's REFUTED note of 2026-09-16)* | **EXECUTED** on the timer side: with the handle NULL it reads **`[0 + 9]`** — address nine, not "somewhere invalid" — and returns that byte × multiplier × 30. `0030E686` is still static | 1 | PROVEN |
| **a resolve that returns zero takes the same unguarded read** | **EXECUTED**: the second refusal at `003876EF` also falls through to `00387714` with `rcx` zero | 1 | PROVEN |
| the ~~party-side~~ Esper shortcut *(corrected 2026-10-02, OPUS: §10 row 3)*, the gates and the terminal-on-terminal refusal | the page's §2.2, `0030E424`–`0030E49C` | 1 | PROVEN |
| the defeat cleanup, its predicates and the four `02089340` latches | the page's §2.7 and §2.7a | 1 | PROVEN |
| the arithmetic half executed in isolation | **EXECUTED**: `diff_status_write.py`, the 41st pilot — 155 cases, 0 mismatches, ~~only `memset` scripted~~ not only `memset` scripted *(corrected 2026-10-02, OPUS: §13, 2026-09-25)* | 1 | PROVEN |
| any runtime observation of this operation, or any execution of `0030E360` | EXECUTED by [`EXP-086`](../_experiments/EXP-086-status-write-execution.md) - the shipped `0030E360` at its canonical VA, 67 cases, 0 mismatches, 9/9 mutants; the live-observation alternative remains open (§13's stated class is isolated original-code) | isolated original-code | PROVEN |
| what the builders write beyond the initialiser | **EXECUTED, and `SW-2` is answered**: the apply side clears bit 0 of `+0x2C` and writes nothing else, reading neither the status id nor the unit; the remove side ORs `0x108` for status 28 with a non-zero `+0x48` — leaving the mask at `0x109` — and writes `(counter + 1) / 2` rounding toward zero into `+0x24` | 1 | PROVEN |
| **neither builder writes any byte of the unit** | **EXECUTED**: all `0x60` bytes compared on 98 builder cases | 1 | PROVEN |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

### The authored decode, re-run from the shipped file

`status_data.bin` re-decoded **at a stride read from its own header**, not at an assumed one — so a
wrong header would have collapsed the rest rather than silently re-cutting the rows:

| claim | measured |
|---|---|
| record `0x28`, count 32, rows at `+0x20`, `0x20 + 32×0x28 = 1312` | header says `count=32`, `stride=0x28`; **1312 = the file size** |
| bit 13 of `+0x06` set on **exactly** ids 0–16, 29, 31 | **19 ids, exactly that set** |
| `+0x08` is `0xFF` on 11 ids and a duration on 21 | **0, 1, 2, 6, 7, 9, 10, 11, 16, 29, 31** — the eleven, exactly; 21 durations |
| **eight** rows carry a non-zero `+0x0C` | **8 — ids 0, 1, 3, 10, 15, 20, 25, 31** |

The cascade row had elided its last two ids behind an ellipsis; they are **25 and 31**, and the eight
masks are now recorded beside them. File `1312 B`, `st2e`, sha256 `c5ea6807f40789f6…`.

### The terminal dispatch, re-decoded from the image

Byte table `0030E8C4` (32 entries), dword table `0030E8A4`, base `0x00120000`. **8 distinct case
indices, maximum index 7, so the dword table needs exactly 8 entries** — the count and the maximum
agree, which is the check a two-level table needs and the place an off-by-one would show:

| case | target | statuses |
|---|---|---|
| 0 | `0030E80A` | 0 |
| 1 | `0030E850` | 1 |
| 2 | `0030E7DD` | 2 |
| 3 | `0030E75B` | 4 |
| 4 | `0030E770` | 5, 27 |
| 5 | `0030E7B3` | 8 |
| 6 | `0030E85E` | 31 |
| 7 | `0030E816` | **24 statuses** — 3, 6, 7, 9–26, 28, 29, 30 |

Doom (id 6) → case 7 → `0030E816`, exactly as claimed.

### Corrected: `0030E816` is the shared tail, not a do-nothing target

```asm
0030E816  mov  eax, [rsp+0x228]   ; the sixth parameter
0030E81D  bt   eax, 9
0030E821  jb   0030E82D           ; bit 9 SET -> skip
0030E823  mov  edx, eax
0030E825  mov  rcx, rsi
0030E828  call 0030FED0           ; BattleStats_RecomputeDerivedStateAndAutoStatuses, 1787 B
0030E82D  ...                     ; stack cookie, epilogue, ret
```

**Every case reaches it.** Case 0 is twelve bytes and **falls through** into it; cases 2–6 `jmp
0030E816`; case 1 jumps into case 6's body and arrives the same way; case 7 *is* it.

> **Why the phrase matters.** A reconstruction reading *"case 7 → the do-nothing target"* would
> implement case 7 as a no-op and **lose the derived-state and auto-status recompute for every
> status**, not just for the 24 that share case 7. The claim itself — *Doom has no terminal case* —
> is right: what case 7 lacks is a **status-specific body**. The target it names is not idle.

**The join, closed 2026-09-12.** `0030FED0` is the subject of [`CONTRACT-auto-status-rebuild.md`](CONTRACT-auto-status-rebuild.md), whose own §15a reads
this edge from the other side: it is 1 of **22 call sites in 12 functions**, and that contract
calls `0030E360` and `0030E130` **back** to apply each changed status bit. **The two operations
call each other, and neither document recorded the return edge until now.**

**Not claimed:** `0030FED0`'s own behaviour is not established *here*, only that this tail calls it
under `bt eax, 9` clear. No live observation and no new execution; §13 unchanged and unaffected.

## 16. Parity plan

**Testable offline, and named in §13:** `CALCULATION` (both defaults over all 32 authored rows),
`STRUCTURAL` (the record layouts and the `0x28` stride), `STATE-TRANSITION` (six modes × already-in-
state), `EDGE-CASE` (every refusal in §10, including the fault).

**Not testable offline, and why — stated rather than left blank:** `TIMING` (nothing here establishes
when the applier or the tick calls it), `PRESENTATION` (the reaction and the two events are
enqueues into systems this contract does not model), `INTEGRATION` (the cascade calls the operation
on itself and the terminal case calls the reward path; a fixture that scripts those has not tested
them), `RNG` (none drawn here), `SERIALIZATION` (none), `FULL SUBSYSTEM` (no).

## 17. Related

- [`Status-Write/the-status-write-and-its-side-effects.md`](Status-Write/the-status-write-and-its-side-effects.md) — the mechanism this contract formalises.
- [`Periodic-Tick/what-the-periodic-tick-does.md`](Periodic-Tick/what-the-periodic-tick-does.md) — stage 2, the only consumer of the two arrays this operation writes.
- [`the-thirty-two-statuses.md`](the-thirty-two-statuses.md) — the id-to-name bridge used in §7 and §8.
- [`CONTRACT-auto-status-rebuild.md`](CONTRACT-auto-status-rebuild.md) — the recompute this operation ends with.
- [`../08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md`](../08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md) — the KO add and remove this operation receives.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

- **Audio.** `BattleFormula_ApplyTargetResult` (`003112F0`) plays its hit sound directly through the sound resolver
  and player: record `+0x140` bit 14 → sound `0x34` with `(0x40, 0x7F)`
  ([applying a result to a target](../07-Combat-Action/applying-a-result-to-a-target.md); `003113A0`–`003113BA`). It
  does not go through the gated wrapper, and its body never reads the global sound gate `02091098`.
- **Items_Equipment_Shops_License.**
  - `003112F0` grants a stolen item through `Inventory_ModifyEncodedItemAndUpdateDiscoveryState`.
  - The recompute this operation ends with (`0030FED0`) and the owner lookup `0031B860` are also driven by the equipment
    setters and the licence-node setter ([the auto-status rebuild](CONTRACT-auto-status-rebuild.md), crossings).
- **Gameplay.**
  - `00300FC0` reads the battle runtime mode through `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15`.
  - `00301140` and `0030E360` raise presentation events through `BattleUnit_DispatchActorPresentationEvent`.
  - `0030E360` updates `BattleUnit_UpdateEngagementStateFlag`.
  - `0030E130` and `0030FED0` call `BattleEncodedId_IsValidForClass`.
- **Movement.**
  - `00300FC0` sets the unit's movement speed (`Actor_SetMovementSpeed`).
  - `00301140` calls a 448-byte locomotion helper that reads the battle runtime mode and the actor's world
    position.
  - `00312280` calls a 148-byte helper that resolves the party focus actor.
  - Two locomotion bodies look up stats owners through `0031B860`.
  - The battle event poster `0046AB10` (`SW-4`) is also called by a Movement-filed body.
- **PlatformOnlineAchievements.** `BattleUnit_ProcessDefeatRewardsAndLoot` (`00312280`) fires achievement counter 11
  with the licence points and counter 4 through its defeat wrapper
  ([the achievement catalogue](../20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md) AB-7).
  A lethal status write therefore reaches the achievement counters through the defeat path.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CoreRuntimeScheduling — SERVICE.** `00301140` on this page calls `GameClock_GetRawTickCounter`, owned by that layer. What it reaches is **seven bytes** returning the counter at `[0208D45C]`, with no scaling of any kind; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**CombatAI — SERVICE and CLIENT (4 edges).** The defeat-condition check `00300FC0` calls `BattleEnmity_PropagateToPerceivingFoes` `003219D0`; the layer function `BattleStats_ModifyStatusLayerStateAndProcessSideEffects` `0030E130` calls `GambitConfig_AdjustAvailableEntryCountByStatsRecord` `003279B0`; `AiOrder_EvaluateTargetSelector` `00301AD0` calls the eligibility gate `BattleTarget_HasLow16EligibilitySuppression` `0030B9B0`; and `BattleUnit_TrySelectAndCommitAiOrderFromSet` `00305CC0` calls the posting path `004697C0`. The status write's side effects reach the AI twice (a removal can spread enmity to the foes that perceive the unit, and a layer bit can change how many gambit entries are available), the AI's target selector shares this contract's eligibility gate, and one of the three action-lifecycle callers of the `004697C0` posting path (SW-4) is the AI's order commit.

**CombatFormula — CLIENT and SERVICE (71 edges).** The result sink `BattleFormula_ApplyTargetResult` `003112F0` calls the status write `BattleStats_ChangeStatusAndProcessSideEffects` `0030E360`, `0030E130` and the recompute `BattleStats_RecomputeDerivedStateAndAutoStatuses` `0030FED0` (which runs `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30`), and `0030E360` and `0030E130` call the sink back with the results they build through `BattleFormula_BuildInactiveStatusTransitionResult` `00386A50`, `BattleFormula_BuildConditionalStatusHpTransitionResult` `00386A70` and `BattleFormula_BuildRandomElementStatusTransitionResult` `00386AE0`; the result initialiser `BattleFormula_InitializeResultRecord` `003848E0` serves those builders and `BattleFormula_EvaluateTargetPreview` `00385680` and `BattleFormula_ResolveTargetResult` `00385F60`; the HP write `BattleStats_ModifyHPAndProcessLethalState` `00300530` calls `0030E360` and the gates `BattleTarget_HasHigh16EligibilitySuppression` `0030B8E0` and `0030B9B0`, and `003112F0` also calls `0030B9B0`; the sink calls `BattleStats_SetCurrentHP` `00300520`, `00300530`, `BattleStats_ModifySecondaryResource` `00300BC0`, `BattleStats_SetPrimaryResourceAbsolute` `00300C90`, `BattleStats_ModifyPrimaryResource` `00300CE0` and `BattleFormula_ApplyResultMetadata` `00385BA0`; `BattleFormula_AppendStatusAddOperation` `00387BB0` calls the default status-parameter helpers `BattleStatus_ComputeDefaultShortTimer` `003876D0` and `BattleStatus_ComputeDefaultDwordParameter` `00387730`, and `0038FCE0` calls `00387730`; `BattleFormula_DispatchPostResultEvents` `00469EC0` calls the poster `0046AB10`; the defeat arm `BattleUnit_ProcessDefeatRewardsAndLoot` `00312280` calls `BattleStats_GetByMappedBattleSlot` `00320AB0`; and the owner resolver `BattleStats_FindOwningBattleUnit` `0031B860` is called by 35 formula bodies such as `BattleFormula_BuildEvaluationContext` `003847C0` and `BattleFormula_RollAndStoreComboCount` `00388660`. The formula layer's sink applies a result's status masks through this contract's write, the write returns its own HP and transition results through that layer's result records and sink, and the rest is shared use of the owner resolver, the result initialiser and the parameter defaults.

**Rewards_Progression_Economy — SERVICE and CLIENT (17 edges).** `0030E360` calls `00312280`, which calls `GameState_GetGil` `00253690`, `GameState_SetGil` `00254EE0`, `Reward_ComputeExperienceForRecipient` `002F8BB0`, `002F8F20`, `Reward_ComputeLicensePointsForRecipient` `002F90C0`, `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650`, `EnemyChain_UpdateOnDefeat` `00317ED0`, `Loot_RollDropEntries` `003180F0` and `Loot_CreateWorldPickup` `00319CA0`; `003112F0` calls the gil pair and `0030C650`; `0030C650` and the level-set `0030C470` call `0030FED0`; and `002F8BB0` and `0030C650` call `0031B860`. A KO written through this contract's terminal dispatch starts the defeat rewards, and a level change calls back into the recompute this contract lists.

**Spawn_Encounter_Lifecycle — CLIENT (1 edge).** `SpawnUnit_FinalizeSpawnEntryActivation` `0023A410` calls `0030FED0`. A newly activated spawn gets its auto-statuses from the recompute.
