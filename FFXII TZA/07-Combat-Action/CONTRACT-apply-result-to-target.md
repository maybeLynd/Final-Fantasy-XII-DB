---
contract: apply a result record to target and source stats using field-specific presence gates and an explicit outer recompute-dirty flag
category: 07-Combat-Action
scope: subsystem
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 07-Combat-Action/applying-a-result-to-a-target.md
entries: ["003112F0", "00311608", "0030E360", "0030E130", "0030FED0", "00300530", "003008A0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: "SECTION-01 re-read the original applier and selected callees; replayed retained EXP-148/149 assertions; executed independent original-CPU controls with disclosed synthetic state and boundary bridges. Not live FF12 or complete callee-graph execution."
last_reviewed: 2026-09-30
review_status: "Production correction; T2 peer review and canonical acceptance remain pending."
previous_review: "OPUS, 2026-09-20: carried page evidence and bounded EXP-060/062 results."
audit:
  passes: 1
  last_pass: 2026-09-30
  last_pass_kind: falsification
  last_pass_state: opus-apply-result-falsification-pass-1
---

# Contract — applying a result to target and source stats

**Current statement, revised by SECTION-01 (2026-09-22).** The earlier survey and
EXP-149 prose disagree in several places. This version resolves those disagreements
against the original instructions, not by preferring the newer document.
[Review, exact supports, controls and remaining limits](../_experiments/evidence/continuation-section01-result-install/REVIEW.md).

Evidence keys: **[page]** = the [mechanism page](applying-a-result-to-a-target.md);
**[EXP-060/062/148/149]** = the respective retained isolated-code experiment;
**[SECTION-01]** = new original-code reading and bounded CPU execution. No key denotes
an independently completed live-game or terminal L2 acceptance.

## 1. Purpose

Consume a result record in a defined order: metadata/events, level and item effects,
status application/removal, parameter copies, numeric target/source effects, status
layers, timers, foe-only adjustments, gil, and an optional **outer recompute**.
Amounts mostly come from upstream, but this routine also performs multiplication,
relative stat arithmetic and gil subtraction. It is not a calculation-free memcpy.

## 2. Interface

```c
// Semantic roles; not a claim that the whole transitive ABI is closed.
void ApplyTargetResult(ResultRecord *record,          // RCX
                       BattleStatsRecord *source,    // RDX, may be null
                       BattleStatsRecord *target,    // R8, may be null on gated paths
                       uint16_t actionId,             // R9W
                       uint32_t callerFlags);         // fifth argument
```

Entry: `003112F0..00311AE7` (2,040 bytes). At `00311321/0031132C`,
`0031B860` maps the **stats-record arguments to owning BattleUnit objects**, not
units to stats. The original resolver compares each unit's `+0x698` pointer with
its input. Large offsets such as `+0xE9A/+0xE60/+0x6A0` below are unit-relative;
`+0x48/+0x64/+0xBC/+0x13C` writes are stats-relative. **[SECTION-01]**

**Dispatch — restored by the owner (OPUS, 2026-09-25).** `00311608`–`00311777` translates record state
into the numeric setters' flag words. Re-read: bit 13 of `d[record+0x2C]` gates an indirect setter call
(`00311744` / `00311748 bt r9d, 0xD`, target chosen by bit 2 at `0031176D`), whose flags are
`(~(f >> 7) & 0x10) | ((f >> 10) & 0x20)` (`00311753`–`0031176A`) — bit 7 enters **inverted**.
**[page, EXP-149, OPUS re-read]** *Owner restatement 2026-09-26 (OPUS), confirming ORACLE's EXP-149 reading.* The whole
dispatch, one gate per setter:
- **Target HP**: bit 8 (`00311610`). The amount is `d[record+0x24]`.
- **Target MP**: bit 14 (`0031166D`). The amount is `w[record+0x2A]`.
- **Secondary resource**: byte `+0x1D` non-zero (`003116A6`) → `BattleStats_ModifySecondaryResource` `00300BC0`.
- **When a source unit is present** (`003116FB`):
  - **Source HP**: bit 7 (`00311703 test dl, dl` / `jns`). The amount is `d[record+0x20]`.
  - **Source MP**: bit 13 (the call above).

So `+0x2C` bit 7 is both the source-HP gate and an inverted input to the source-MP call's flags.

## 3. Types and field-specific absence

`ResultRecord` includes the numeric-selector dword at `+0x2C`, apply/remove masks
at `+0x54/+0x58`, dword parameters at `+0x5C`, signed-word parameters at `+0xDC`,
source/target quantities, layer bytes, timer words and late metadata through `+0x140`.

**There is no universal all-ones neutral encoding.** Masks and numeric-presence bits
must be clear to suppress those paths. The item scalar at `+0x38` is absent when its
**dword** equals `-1` (the dispatched item ID is the low word); layer and level bytes
use `0xFF`; copy/timer words and dwords skip negative values; zero suppresses steal
selectors, the secondary multiplier, effect bytes and gil adjustment. A field-specific
neutral fixture suppresses listed effect dispatch, but metadata still runs and the
owner's transient bits can still be cleared. All-`FF` triggers 64 mask calls in the
independent boundary fixture. **[page, SECTION-01]**

**A zero-filled record is not neutral** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 332, which executed it stub-free ([package](../_index/candidates/s21-opus-replay-applier-stub-free/README.md)); `003114D2`–`003114EB` and `00311781`–`00311819` re-read.)*. The layer bytes are absent only at `0xFF`, and their extent
is exact: `+0x3C`–`+0x3D` (two bytes, the loop at `00311788`, mode 2 with `-1`) and `+0x3E`–`+0x41` (four bytes,
the loop at `003117E4`, mode 0 with `0`). Each non-`0xFF` byte is one `0030E130` call and sets the outer dirty flag.
So a zeroed record makes **six** layer calls and then the outer recompute. The layer calls' flags are likewise
`0x200`, plus `2` from `+0x140` bit 6 in the first loop or bit 7 in the second.

## 4. Preconditions · postconditions · invariants

**I1 — two operations on 32 statuses, not 64 distinct statuses.** `+0x54` dispatches
`0030E360(target, source, bit, duration, word, flags, mode=3)`;
`+0x58` dispatches the same operation with zero parameters and `mode=0`.
The six-mode callee maps 0/1/2 to clear `+0x64/+0x3C/+0x38` and 3/4/5 to set those
words. Callee gates and idempotence still apply. **[page, EXP-149]**
**The flags argument is fixed by the applier, not taken from the caller** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 332, which executed it stub-free ([package](../_index/candidates/s21-opus-replay-applier-stub-free/README.md)); `003114D2`–`003114EB` and `00311781`–`00311819` re-read.)*. Both mask loops pass
`0x200`, plus `2` when a bit of the record's `+0x140` is set: bit 4 for the apply loop, bit 5 for the remove loop
(`((rec[+0x140] & 0x10) | 0x1000) >> 3` and `((rec[+0x140] & 0x20) | 0x2000) >> 4`). `callerFlags` is not
consulted. OPUS's run, with `+0x140` zero, saw exactly `0x200` in both. Bit 9 is the bit with which `0030E130`
suppresses its own recompute (EXP-148). *Whether `0030E360` honours it the same way is not read here.*

**I2 — parameter forwarding AND direct copy-through both exist.** Selected apply bits
forward `record+0x5C[i]` and `record+0xDC[i]`. After both mask loops, the original applier
itself copies each nonnegative dword to `target+0xBC+4*i` and each nonnegative signed
word to `target+0x13C+2*i` (`003115B6..00311606`). These copies run even with both masks
zero and do not set the outer dirty flag. Negative values preserve destination bytes;
zero is present. EXP-149's later statement that these are *not direct copies* is rejected.
**[page, SECTION-01]**

**I3 — the outer flag records branch dispatch, NOT confirmed state change.** `r14d` is
assigned 1 immediately after selected E360/E130 calls, without testing a success result
(`0031153F`, `003115A4`, `003117D0`, `0031180C`). Foe stat/effect branches also set it.
An idempotent or rejected status can therefore still lead to the outer recompute.
At `00311AAF..00311AC5`, that call is exactly:
`if (target && !(callerFlags & 0x200) && dirty) 0030FED0(target, 0)`.
Retained idempotent/locked cases and the new no-effect-sink control support this distinction.
**[EXP-149, SECTION-01]**

**I4 — numeric, item, steal, copy-through, timer, gil and transient-marker branches do
not set that outer flag.** A pure numeric result has no **outer-tail** FED0 call. This
is not a ban on FED0 anywhere below the call: a lethal HP write can invoke E360 and
recompute internally, as EXP-149's `ap-lethal` trace demonstrates. Do not infer absence
of visible/UI refresh from the absence of one call site. **[page, EXP-149, SECTION-01]**

**I5 — source and target effects are distinct paths in the same call.** Target HP/MP
presence is `A` bits 8/14; source HP/MP presence is bits 7/13. Null source suppresses
its numeric paths. Source HP passes a null source-context argument to its setter.
Bit 31 is not the source HP presence bit. **[EXP-060/062, SECTION-01]**

**I6 — absolute/delta choices are record bits.** Target HP bit3 selects `00300520`
(absolute-to-delta shim), otherwise `00300530`; target MP bit4 selects `00300C90`,
otherwise `00300CE0`. Source HP/MP absolute choices use bits 1/2 respectively.
Numeric `-1` is a value when the corresponding presence bit is set. **[page, EXP-060]**

**I7 — translate input bits, not shift immediates.** For `A = dword[record+0x2C]`,
HP outgoing bits are target `A19->8, A10->5, !A18->6, !A6->4`;
source `A9->5, !A17->6, !A5->4`. MP outgoing bits are target `A16->5, !A12->4`;
source `A15->5, !A11->4`. There is **no unconditional 0x400 target-HP flag**.
For target HP presence alone the outgoing word is `0x50`; the independent controls
also vary the contributing bits. **[page, EXP-060, SECTION-01]**

**I8 — distinguish stats from their owner on foe paths.** Foe stat adjustments check
`targetStats+5 == 1`. Steal and effect-byte paths require an owning unit whose
`unit->stats` exists and has kind 1. Steal IDs are words at
`unit->p_E60 + 0x32 + 2*i`; availability clears at `unit->spawn + 0x14`. *Sharpened 2026-09-26 (FABLE, Claude Opus 5.5), on `OPUS-NOTE-FABLE-S21-I8-GATE-CLEARS-AVAILABILITY`:* **the
slot clear is made by the gate `00385BA0`, not by the steal loop, and it is not gated on kind 1.** For each non-zero
result byte `+0x34`/`+0x33`/`+0x32`, the gate resolves the target's owning unit (`0031B860`) and ANDs its spawn
`+0x14` with `0xFB`/`0xFD`/`0xFE` (`00385C17`, `00385C41`, `00385C6B`). It checks only that the unit and its spawn
block exist. The applier calls the gate before its steal loop (`0031137A`). The loop runs only for kind 1 and then
finds the bit already clear at its own `btr` (`0031146C`). So a steal byte aimed at a target whose stats are not
kind 1 still consumes the availability, and grants nothing. The kind-1 gate governs the item grant, not the clear.
OPUS executed this stub-free for kind 1 and kind 0 (`candidates/s21-opus-replay-applier-stub-free/i8_foe.py`, case G).
The post-result events page's row for the gate says the same.
Effect bytes modify `spawn+0x7B/0x79/0x78/0x7A` and OR `0x80` into its leading dword.
**[page, EXP-149, SECTION-01]**

## 5. State

The target/source stats records; resolved owners; item and progression state;
spawn-backed foe state; global metadata/event consumers. Parameter arrays are at
stats `+0xBC/+0x13C`; eight timer words at `+0x17C..+0x18A`. Temporary owner `+0xE9A`
bit 3 follows **record `+0x2C` bit19**, bit 2 follows **record `+0x140` bit14**;
the tail clears both. Neither branch sets `r14d`. **[page, SECTION-01]**

## 6. Relationships

`0031B860` resolves owners. `00385BA0` consumes metadata. E360 handles statuses;
E130 handles status layers; FED0 recomputes derived state. Numeric setters, item
writer `003008A0`, level grower `0030C650` and field writer `00316A50` have their
own downstream behavior. EXP-148/149 execute selected original callees, not every
transitive callback. See their explicit boundary lists and the review.

## 7. State transitions

```text
resolve source/target owners; apply caller eligibility gate
consume metadata; set selected transient owner bits
apply requested level changes and item/steal effects
if target stats:
    dispatch apply/remove mask bits; dirty = true for each selected call
    copy nonnegative dword/word parameter arrays, independently of masks
    apply target numeric quantities (do not set dirty)
apply source numeric quantities when source exists (do not set dirty)
if target stats:
    dispatch layer bytes; dirty = true for each selected call
    copy nonnegative timers (do not set dirty)
    process foe relative-stat fields; set dirty for selected fields
process spawn-backed foe effect bytes; set dirty for selected fields
adjust gil; clear transient owner bits
if target && !(callerFlags & 0x200) && dirty: recompute(target, 0)
```

## 8. Script · resource · event interactions

Upstream formula code constructs the result. `00385BA0` can dispatch post-result
events; the item writer crosses into inventory/discovery; level and status callees
can notify other systems. Therefore the earlier claim of no direct event interaction
is too narrow. Metadata and several callbacks are scripted in EXP-149, not closed by it.

## 8a. The post-result events: the route, the poster, the ring and the message realiser (FABLE, 2026-10-03)

*Added for SWE2-AUDIT-SPEC's SCOPE-SHORT on S-21 ([`auditspec-l2-expansion-1003`](../_index/candidates/auditspec-l2-expansion-1003/README.md) item 3):
the registry subject names the post-result events and the battle message table, and §8 gave them one sentence. Static
and isolated original-code; every fact below is checked by [`check_s21.py`](../_index/candidates/fable-l2exp-s21-mech-1003/check_s21.py) (FAILS 0). Which event
each result posts, the row texts and the log widget's line lifetime are [the post-result events page](Post-Result-Events/the-post-result-events-and-the-battle-message-table.md)
§2.2, §2.5 and §2.7. The poster's arms were executed earlier with the realiser scripted, in EXP-246 and EXP-249 to
EXP-256 ([the auto-status contract](../10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md) §13bc–§13bm). This section states the contract those
pages leave implicit: the route from this applier, the gates in order, the ring's lifetime and what the realiser
hands on.*

**Interface (FABLE).**

| entry | callers (raw index: E8/E9, 0F 8x, EB/7x, rip-relative, image-base-relative, pointer constants) | role |
|---|---|---|
| `BattleFormula_ApplyResultMetadata` `00385BA0(_, source, target, record)` | one: `0031137A` in this applier, after the eligibility gate `00311354`–`00311367` | dispatches when record byte `+0x1C` is `1` (`00385C6F`) |
| `BattleFormula_DispatchPostResultEvents` `00469EC0(action, source, target, record)` | one: `00385C85` | builds the context, posts 0..n events |
| the poster `0046AB10(stats, event, ctx)` | **48 sites in 18 functions**: the dispatcher (10, with its fragment `00469FE0`) and 17 other posters (38) | gates, ring, realise; **defines no return value** |
| the filter `00469570(event, ctx.q_00, ctx.q_08)` | one: `0046AB65` | visibility verdict |
| the realiser `005369C0(stats, event, ctx)` | one: `0046AC66` | four argument slots, then the formatter `00536410` and the last mile `0035B990` (one caller each, `00536C06` and `00536D79`) |

No pointer constant names any of these entries. Six `.rdata` dwords equal one of their RVAs: five are chained-unwind
parent records and one lies inside an unwind-code array.

**The context the dispatcher builds** (`rbp-0x48`, 0x30 bytes; all ten dispatcher sites pass it):
- `+0x00` source stats, `+0x08` target stats;
- `+0x10` record `+0x08`, `+0x14` `|record +0x24|`, `+0x18` the status (0 unless events `0x18`/`0x1A` set it);
- `+0x1C` the source's level byte `+0x1C2`, `+0x20` record `+0x38`;
- `+0x28` the action id **zero-extended from 16 bits** (`00469EFB`, `00469F33`), and `+0x2C`–`+0x2F` **zero**
  (`00469EF0` clears the qword, and only the low dword is stored).

**Reads and writes.**
- Read: the table pointer `[02EBF018]` (registry slot 7, `battle_message.bin`), its row stride word `+0x08` and its
  rebased row pointer `+0x0C`; the frame base `[01DFE0B4]` (`G`); the raw tick counter `[0208D45C]` through
  `0032A150`; the battle-state word `02089340`; the owning unit's byte `+0x04`.
- Written by the poster: the ten-entry ring `02EBB560` (32 B per entry) and its index `02EBB54C`.
- Written by the filter and the realiser: the owner cell `02EBF188` (each `0031B860` result is stored there).

**Invariant I9 — one route, keyed by the scratch action word.** The applier reaches the events only through
`0031137A` → `00385BA0` → `00385C85` → `00469EC0`. Each link has exactly one caller.
- The dispatch condition is record byte `+0x1C == 1` (`00385C6F`/`00385C73`).
- The action id it passes is `word [02AEDFD4]` (`00385C75`). The gate never reads the `ecx` the applier hands it
  (`00385BC9` overwrites it first), so **the applier's own action argument is not what the events are keyed by**.
  - `02AEDFD4` is written by the preview `00385680` (`003857EC`, `00385806`) and the resolver `00385F60` (`00385FE4`,
    `00385FFB`), and nothing resets it ([the scratch block](../08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md)).
- The dispatcher's posts carry a 16-bit action at `+0x28`, so the poster's cap drops every dispatcher post whose
  action is `0x1FF` or above.
- Their `+0x2C` is 0, so none of them takes the stash arm of I12.
- No path from a dispatcher site reads the poster's `rax`. The one site that falls into the dispatcher's `ret`
  (`0046A617`) returns it through `00385BA0`'s epilogue (`00385C8A`–`00385C99`), which does not read it either.

**Invariant I10 — the poster's gates, in this order, each a silent return** (`0046AB10`):
1. **Cap** — `ctx.dw_28 ≥ 0x1FF`, a **signed** `jge` (`0046AB19`/`0046AB29`). Executed: `0x1FF` is dropped with no ring
   write, while `0x1FE` and `-1` are admitted.
2. **Veto, only when `ctx.q_08` is non-null and `0031B860` finds its owning unit** (`0046AB2F`–`0046AB40`). Then
   `02089340 & 0x3080` drops the post (`0046AB42`), and so does the unit's byte `+4` bit 5 (`0046AB52`).
   - Bits 7, 12 and 13 are set by `00238AE0`, `00238B00` and `00238B20`, the event lock, the definition load in flight
     and the focus condition ([the world-tick page](../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md)'s bit table).
     Area initialisation clears all three (`0023432D`, `and 0xFFFFC01E`).
   - Executed: with each bit set, a post is dropped when the target has a unit, and **admitted when the target has none
     or is null**. So the veto never stops the dispatcher's no-unit world (the page's (c)).
3. **Filter** — `00469570` returns 0 (`0046AB65`/`0046AB6C`).
   - It admits when row byte `+3` is `≥ 0x80` (`004695F9`).
   - Otherwise the **source's** owning unit decides alone, if it has an actor link at `+0x10`: `002FA3B0(link)`
     (`0046963D`). The target is consulted (`0046967E`) only when the source has no unit or no link.
   - With neither, it admits (`00469685`).
   - Executed: a source verdict of 0 drops the post even when the target's verdict is 1.
4. **Rate limit** — only when row byte `+4` bit 0 is set (`0046ABB3`; 28 rows of 102 in `us`).
   - The key is `(word +0, qword +8) == (event, the poster's first argument)`. It is not a context field (`0046ABD4`,
     `0046ABDA`).
   - A live entry suppresses when `(u32)(stamp + 0x1C2 × G) > (u32)now`, an **unsigned** `ja` (`0046ABE6`–`0046ABF5`).
   - Executed with the shipped `us` table, row `0x05`, at G = 1 and G = 2: suppressed at stamp + 0x1C2·G − 1; admitted
     at stamp + 0x1C2·G; admitted for other stats at the same tick.
5. **Record and realise** — slot `[02EBB54C]` is overwritten whole: `{event, now, stats}`, with `+0x10`/`+0x18` zero
   (`0046AC00`–`0046AC3B`). The index becomes `(i + 1) mod 10` (`0046AC40`–`0046AC5D`), and `005369C0(stats, event, ctx)`
   is called (`0046AC66`).

The exits do not set `rax`. EXP-252 pinned the veto exit returning the owner row; on a suppress `rax` is the tick.

**Invariant I11 — one ring for every admitted post; its epoch is the area, not the clock.**
- **Every admitted post takes a slot, rate-limited or not.** So a limited row's stamp lives only until ten more posts
  land. Executed: after ten unlimited posts, row `0x05` repeats for the same stats 100 ticks after its stamp.
- **The ring is reset in one place.** The leaf `004696A0` is branch-free. It sets event `0xFFFF`, stats 0, tick 0 and
  word `+0x18` 0 in all ten entries, and sets the index to 0 (41 rip-relative stores).
  - Its only caller is `0033A380` (`0033A3B0`), whose only caller is `00234463` in area initialisation `002342F0`.
  - No other instruction writes the ring or its index except the poster's.
- **The tick counter has its own reset.** `0032A160` stores 0 through `00237DF0`, on four routes
  ([S-17's package](../_index/candidates/fable-l2exp-s17-mech-1003/README.md), K1–K3).
  - Only the area-initialisation route (`00234349`, byte `0208D455 == -2`) is followed by the ring reset in the same
    body (`00234349` → `00234463`: forward branches and one counted loop).
  - After a counter restart without a ring reset, a kept stamp `T` suppresses a repeat of its `(event, stats)` until
    the new clock reaches `T + 0x1C2·G`.
  - Executed: stamp 5000, counter restarted to 10. The repeat is suppressed at 10 and at 5449, and admitted at 5450.
    After `004696A0`, it is admitted at 10.

**Invariant I12 — the realiser reads four kind bytes of the row and hands on a fixed request.**
- **The row address is `rebase(+0x0C) + event × stride` in 32-bit arithmetic**, with no bound against the row count
  `+0x04`: poster `0046ABA6`–`0046ABAD`, filter `004695BD`–`004695C4`, realiser `00536A86`–`00536A97`. The only compare
  on the event is the ring key (`0046ABDD`).
- **The slots and their kinds.** Slots 0–2 take their kind from row bytes `+0`–`+2`, and slot 3 from `+5`
  (`00536A58`/`00536A5C`). The 9-entry table at `00536DA8` (`dec eax; cmp eax, 8; ja`, `00536AFE`–`00536B15`) maps:
  - kind 1 → the source's name word (`00536310`) and its letter byte;
  - kind 2 → the target's name word and letter byte;
  - kinds 3–9 → ctx `+0x10` / `+0x14` / `+0x18` / `+0x1C` / `+0x20` / `+0x28` / `+0x24`;
  - kind 0 and kinds ≥ 10 → 0 (`00536BA1`).

  The letter byte comes from `00263A10`, only for stats with byte `+5` set whose unit has an actor link.
  Executed over shipped row `0x18` (`02 05`) and synthetic rows covering every kind.
- **The id word** is the event's low 15 bits, plus bit 15 = `002FA390(stats)` (`005369F0`–`00536A45`).
  - Bits 16–31 of that dword are never initialised by `005369C0`: it reads the stack slot before any store. Executed
    with a patterned stack, they come back as the pattern.
  - `00536410` masks them away (`00536448`–`0053645B`).
- **The request to `0035B990`** (0x38 bytes, executed):

  | offset | value |
  |---|---|
  | `+0x00` | `7` |
  | `+0x08` / `+0x10` | source / target display name from `00536280`, or 0 when that side has no unit with an actor link |
  | `+0x18` / `+0x19` | the letter bytes |
  | `+0x1A` | ctx word `+0x28` |
  | `+0x1C` | ctx word `+0x14` |
  | `+0x1F` | the category `(row[3] >> 2) & 0x1F` |
  | `+0x20` | `-1` |
  | `+0x28` | the `0x180`-byte text `00536410` wrote |
  | `+0x30` | ctx word `+0x2C` |
  | `+0x32` | `1` exactly for events `0x24` / `0x25` (`00536C7C`–`00536C84`) |

- **The last mile.** `0035B990`, executed:
  - **word `+0x30` non-zero selects the stash**: the text is copied to `[022CA430] + 0x568` (`0x180` bytes), and
    there is **no HUD line**;
  - **otherwise `0028E110(text, +0x1F, 0, 0)` is always called**. `00254A10() == 0` together with `+0x32` gates only
    the strip-and-measure step (`0035BA0F`–`0035BA65`), never the post.
  - So every dispatcher post that passes I10 reaches the HUD log.

**Failure paths (FABLE).**
- **An unbound table faults.** With `[02EBF018]` null (or its rebase null), the filter skips the row test, but the
  poster's row pointer becomes 0 (`0046ABB1`). If the filter admits, `test byte [rcx+4]` reads address 4. Executed: an
  unmapped read at `0046ABB3`. A post before slot 7 is bound must therefore be refused by the filter, or it crashes.
- **An event id past the table reads the next bytes as a row.** No literal id at the 48 sites exceeds `0x4D`, and the
  computed ones top out at `0x62` (`0x5D + n`, the page §2.7). The 100-row `ch` / `cn` / `in` / `kr` tables therefore cover every
  posted id. Their rows 0–99 differ from `us` only in kind bytes, not in layout.
- **Suppression is silent** at every gate. No caller learns that a line was dropped, and none reads `rax`.
- **A row address above 4 GB** cannot be formed (I12). A reimplementation that keeps 64-bit row pointers is a widening,
  not a behaviour the image has.
- **A reimplementation** that keys the events on the applier's action argument, vetoes unit-less targets, consults the
  target when the source has a verdict, compares the window signed, or gives rate-limited rows a private ring changes
  which battle lines the player sees.

**Evidence class (FABLE).**
- **Static:** K1–K5 of `check_s21.py`. That covers the raw index in every form, chained-`.pdata` roots, the route,
  the context, the body reads, the ring writers, and the reset chain.
- **Isolated original code, under Unicorn 2.1.4:**
  - K6 runs `0046AB10`, `00469570`, `0020E600`, `0032A150` and `004696A0` real. `0031B860`, `002FA3B0` and
    `005369C0` are answered by hooks, and the table is the shipped `us` `battle_message.bin` (102 × 8 B), rebased as
    `003845F0` does;
  - K7 runs `005369C0` real with its ten callees hooked;
  - K8 runs `0035B990` real with its seven callees hooked.
- **Sensitivity controls.** Four byte mutations each turn a check to FAIL: `jge`→`jg` at `0046AB29`, bit 1 at
  `0046ABB3`, bound 7 at `00536B00`, and `je`→`jne` at `0035B9CB`. So does one mutated claim ("the `0x3080` veto drops
  every post").
- **Live: none.** The page's `FL-2` live read is ASTRA-QUEUE AQ-16.
- **Not traced:**
  - whether every counter restart is followed by an area initialisation before the next post;
  - which of the 17 other posters set ctx `+0x2C`. `0046AA70` stores `edx` there (`0046AABC`) before its gil post;
  - the engines' escape grammar;
  - `00536410`'s text.

### Crossings into other layers (FABLE, 2026-10-03)

*The edges this section's citations add, each with what crosses it.*

- **Save/Load/Settings — CLIENT and SERVICE (2 edges).**
  - The tick counter's reset `00237DF0` is reached from the save-image rebind
    `SaveRuntime_RebindImageBackedGameplayState` `00238A80` (`00238AA2`). It is one of the four counter-restart routes
    that I11 names, and not the area-initialisation route that is followed by the ring reset `004696A0`.
  - The locale gate `00254A10`, which returns 1 when `00229E40()` is 0, 7, 8, 10 or 11 (`00254A19`–`00254A28`,
    mask `0xD81`), is also called by `SaveSlotMetadata_BuildSubmissionDescriptor` `005832B0` (`00583358`). It is a
    shared locale getter. §8a cites it only as the strip-and-measure gate in `0035B990`.

  The message ring's epoch depends on a save-path reset. The locale answer is shared. The ownership is not shared.

## 9. Determinism

The applier has no direct random-draw instruction/call identified in this body.
**The record alone is not sufficient state.** Its outcome also depends on source,
target and owners, descriptor/global state, eligibility and downstream callback results.
No universal determinism of the transitive call graph is asserted here.

## 10. Failure paths and edge conditions

Caller flag bit0 bypasses the initial eligibility call; otherwise nonzero rejection
returns before metadata. Stats, owner and spawn availability gate different blocks.
Callee refusal/idempotence does not undo the applier's branch-selected dirty flag.
Caller bit9 suppresses this outer recompute, not arbitrary nested side effects.
All-ones data is not a valid substitute for an initialized neutral result.

## 11. Observable behaviour

One record can change both combatants, dispatch statuses, copy parameters even without
status masks, consume steal slots, and affect metadata/events. Actual player-visible
presentation, initialized-game reachability and session health are not validated by
these isolated controls. Do not equate an absent outer FED0 call with no UI change.

## 12. Reproduction formula

Implement field-specific presence, exact argument roles and execution order. Preserve
I2's copies independently of status calls, I3's branch-selected dirty flag, and I7's bit
translation. Distinguish outer-tail recompute from recomputes inside numeric/status
callees. Keep synthetic-fixture assumptions out of the reconstructed game specification.

## 13. Validation and adjudication

EXP-060 covers the numeric dispatch with five stubbed setters (22 retained controls).
EXP-062 composes copy-out, dispatch and native MP behavior with an injected bridge
(nine retained cases). Their contribution remains **bounded caller/composition evidence**,
not execution of the whole apply graph; their historical primary contract metadata is
not silently reassigned.

EXP-148 retains 43 passing cases for the five formerly undecoded callees. EXP-149 retains
36 passing whole-applier cases with more original callees. SECTION-01 replays all **79
stored output assertions**, verifies selected source bodies, and adds separate native
controls. The original Unicorn executions and the claimed three-process stability were
**not rerun here**. Retained assertions passing does not validate every prose claim.

Disposition: **incorporate with corrections/narrowing**, specifically I2/I3/I4/I7 and input
roles. Preserve accepted original-code effects, but withhold complete recursive/notify
semantics, live-game reachability, and whole-system L2 acceptance. Nested re-entry was not
driven by the retained thunks; the harness's entry shortcut also precedes its nominal
nested-entry intercept, so that intercept must not be assumed tested. Full details and
new test results are in [SECTION-01](../_experiments/evidence/continuation-section01-result-install/REVIEW.md).

### Executed specifics restored by the owner (OPUS, 2026-09-25)

The rewrite kept EXP-148/149's case counts but dropped what they executed. Restored here, each re-read
statically where noted (`_index/candidates/exp148-owner-consumption.md`, `exp149-owner-consumption.md`);
where SECTION-01's narrowing above differs, **the narrowing governs**.

* **`0030E130`** takes a mode in its fifth argument and decodes it into two flags: `(mode − 2) ≤ 1`, i.e. modes 2 and 3
  (`0030E178`–`0030E18C`), and `(mode & ~2) == 0`, i.e. modes 0 and 2 (`0030E18F`–`0030E199`). They choose between the
  two `bts` paths (`0030E20E`, `0030E223`) and the two `btr` paths (`0030E235`, `0030E24A`) on the status bit, and the
  modes 0 and 2 flag also gates the auxiliary update `0030EA40` (`0030E251`). The id is first checked against class 29
  (`0030E1DE`, `BattleEncodedId_IsValidForClass(0x1D, …)`). *(Owner confirmation 2026-09-26, OPUS, of ORACLE's EXP-148
  four-mode reading.)* It calls `0030FED0(target, flags)` only when flags bit 9 is clear (`0030E31C bt r12d, 9`).
  **`0030FED0`** builds a 128-bit status bitmap from the record's `+0x50`/`+0x54` (or the member's
  `+0xE80` bitfield, `00310047`), folds equipment slots, dispatches `0030E130(unit, bit, 0, flags|0x202,
  mode 3)` per set bit (`0030FEFB or r15d, 0x202`) — the `|0x200` is the anti-recursion suppressor the
  caller-side `!(flags & 0x200)` gate complements — and calls `0030E360` per set bit of `member+0xE90`.
  Its null guard is partial: a null unit still dereferences `+0x50` in the equipment loop. **[EXP-148]**
* **`0030C650`** is the level-set/growth writer: level clamped at 99 (`0030C6CC`, `0030C7B5`), per-level
  stat folds `002F9A60` / `002F9B20` / `002F9BD0`, and a last-iteration `0030FED0(unit, 0)` (`0030C7CE`)
  plus a licence-notify chain. **[EXP-148]**
* **`003008A0`** is the item write: rejects `0xFFFF` / `0x1000` / above-`0xE000`-class / out-of-bounds ids
  with −1; the unlock-flag ORs into `d[q[02EBF190]+4]` fire only when `r9d == 1`, the raw resolver
  `00309F30` returned ≤ 0 and the effective result is > 0 (`00300968`–`0030097C`); by category
  `id >> 12`: 3 → `|= 0x01`, 4 → `|= 0x40`, 12 with id `0xC000..0xC011` → `|= 0x80`,
  `0xC012..0xC01E` → `|= 0x100` (`003009C1`–`003009F7`). **[EXP-148, OPUS re-read]**
* **`00316A50`** is a two-path field writer driven by the `00D10460` descriptor table (8-byte
  descriptors at `[image base + i*8 + 0xBF0460]`): threshold-gated bit-set, or read-modify-write with
  `0x7FFF` / `0x7FFFFFFF` clamps or a plain add. **[EXP-148]**
* **Lethal chain, executed end to end:** HP delta → `00377C20` can-die consult → `0030E360(bit0, mode 3)`
  → `d64 |= 1` (KO is bit 0 of `d64`); killer id `d[tgtRec+0x30] = d[srcRec+8]`; member kill counter
  `w[flagobj+8]++`; the `00312280` arm (bit 0's arm; `003299B0` is bit 3's); the credit chain
  `0032A150` / `00306F00` / `003299B0`. Revive (positive delta at 0 HP) → `0030E360(bit0, mode 0)` clears
  `d64`. **[EXP-149]**
* **Steal:** the item words are read through the pointer `q[unit+0xE60]` as words, `0xFFFF` skipped,
  each passed to `003008A0` with `r9d = 1` (`00311435`–`00311457`); each stolen slot `btr`s
  `b[flagobj+0x14]`. **[EXP-149, OPUS re-read]**
* **`0030E360` arguments:** per set bit `i` of `d[rec+0x54]`, `d[rec+0x5C+4i]` and sign-extended
  `w[rec+0xDC+2i]` are arguments with mode 3 (`00311510`–`0031153A`) — not direct copies. **[EXP-149,
  OPUS re-read]**

## 14. Remaining questions

* Required initialized-game observations and callback-dependent reachability.
* Semantics of scripted metadata/notify/eligibility boundaries not established by these fixtures.
  *(Restored by the owner, OPUS, 2026-09-25: the scripted surfaces are `0031B860`, `003165C0`, the `00315E90`/`00316BF0` write-back pair, the notify thunks, `00309F30` and nested `0030E360` — cited at the boundary, not executed inside it. **[EXP-148]**)*
* Recursive/nested applier behavior; recorded thunks leave its trigger clear.
* Authored origin/availability of the steal IDs where not already established elsewhere.
* Formal peer acceptance and evidence-link instrument disposition. A source correction is
  not an automatic TEAM task closure or joint L2 pass.

## 15. Evidence

[Mechanism page](applying-a-result-to-a-target.md) ·
[EXP-060](../_experiments/EXP-060-result-numeric-dispatch.md) ·
[EXP-062](../_experiments/EXP-062-mp-composition.md) ·
[EXP-148](../_experiments/EXP-148-apply-result-callees-exec.md) ·
[EXP-149](../_experiments/EXP-149-apply-result-whole-exec.md) ·
[SECTION-01 controls and provenance](../_experiments/evidence/continuation-section01-result-install/REVIEW.md).

## 16. Parity plan

Test neutral field-specific payloads versus all-ones data; independent array copies
with both masks clear; negative versus zero parameters; selected-but-refused statuses;
caller-bit9 suppression; target/source presence and flag translations; pure numeric
outer-tail absence versus a lethal path's nested recompute. Qualify every substituted
boundary. These are database-falsification probes, not a requirement to complete L3
implementation before finishing the L1+L2 database.

## Cross-subsystem neighbours — pass 22 (FABLE, 2026-09-29)

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**ActorEntity — SERVICE and CLIENT (7 edges).** The status write `0030E360` calls the defeat-condition check `00300FC0`; the defeat arm `00312280` calls `Actor_GetWorldPosition` `00265020` for the victim's position; the owner resolver `0031B860` walks the unit table through `BattleUnit_GetBySlotIndex` `00236820` and `BattleUnit_GetSlotCount` `00236850`. In the other direction `BattleUnit_ActivateAppliedDefinitionRuntime` `00233AD0` calls the presentation-event dispatcher `003299B0`, and `0025C830` and `BattleGroup_RefreshFourActorDefinitions` `003266C0` call the field predicate `00377C20`. The apply path uses the actor layer's unit table and position getter and, on a KO, raises its focus-lost / party-down / roster-down latches (`00300FC0`); the three actor callers use the dispatcher and the predicate for their own activation and group-refresh work, not for applying a result.

**Audio — SERVICE (4 edges).** The applier `003112F0` and the level grower `0030C650` both call `Audio_ResolveBankLocalId_WorldLive` `003A1180` and then `Audio_PlayResolvedSound` `002DF220`. That is the two-call sound request of the audio boundary: the applier plays sound `0x34` when record `+0x140` bit 14 is set (skipped when the resolve returns `-1`), and the level grower plays the level-up fanfare at bank-local slot 7.

**CombatAI — SERVICE and CLIENT (5 edges).** The layer write `0030E130` calls `GambitConfig_AdjustAvailableEntryCountByStatsRecord` `003279B0`; `BattleUnit_UpdateCombatFrame` `00308610` calls the dispatcher `003299B0`; `AiOrder_EvaluateAndResolveActionTarget` `003014C0`, `AiOrder_EvaluateTargetSelector` `00301AD0` and `BattleUnit_SelectAndCommitNextAction` `00305AB0` call the field predicate `00377C20`. When the changed layer id is in `0x68`–`0x71` and the record is kind 0, `0030E130` adds or removes one available gambit slot through `003279B0` (three per-member count bytes at `+0x5B42` of the game-state block, stride `0x34`, each clamped to 0–12); the AI callers consult the predicate and the dispatcher for their own action selection and are not part of this contract.

**CombatFormula — SERVICE and CLIENT (85 edges).** These are the apply path's own numeric bodies. The applier `003112F0` calls the HP setters `00300520` / `00300530`, the resource setters `00300BC0`, `00300C90` and `00300CE0`, the resolver `0031B860` and the metadata gate `00385BA0`; the status write `0030E360` builds a 0x148-byte transition result with `00386A50` or `00386A70` and applies it through `003112F0`, and `0030E130` does the same with `00386AE0`; the recompute `0030FED0` calls `BattleStats_RebuildEffectiveStatsAndAffinityState` `002FEF30`; the defeat arm `00312280` calls `BattleStats_GetByMappedBattleSlot` `00320AB0`. The resolver `0031B860` has 35 callers in that layer - besides the apply-path bodies above, among them `BattleFormula_ResolveTargetResult` `00385F60`, `BattleFormula_EvaluateTargetPreview` `00385680`, `BattleFormula_RollAndStoreComboCount` `00388660` and `BattleFormula_DispatchPostResultEvents` `00469EC0`. The contract's subjects are filed to the formula layer themselves, so these edges are the apply chain's internal calls plus the resolver's other callers, each of which maps a stats record to its owning battle unit exactly as the applier does.

**CoreRuntimeScheduling — MECHANICAL (1 edge).** The HP setter `00300530` calls `GameClock_GetRawTickCounter` `0032A150` once, right after the member kill counter is incremented, and stores the tick divided by 30 into the member's flag object `+0xC`: a clock read that time-stamps the kill.

**Gameplay — SERVICE and CLIENT (13 edges).** The HP setter `00300530` calls `BattleTargetBuffer_FindActorWorkIndex` `00316D70` and the dispatcher `003299B0`; `00306F00` and `0030E360` also call `003299B0`, and `0030E360` calls `BattleUnit_UpdateEngagementStateFlag` `00307D10`; `0030E130` and `0030FED0` call `BattleEncodedId_IsValidForClass` `00322C50`; `00315E90` calls `BattleEncodedId_DispatchQueryMode0Value` `00309EC0`; `Battle_EmitReactionPresentationForSlot` `003176E0` calls `003299B0`; `00307D10`, `BattleUnit_CollectMappedFourSlotUnitsByFlags` `0030A8A0`, `BattleUnit_HasRelationshipClass2PlusInSlotMask` `0030C210` and `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` `0030D9A0` call `00377C20`. Gameplay is the census's domain label for ownerless combat helpers: the apply path calls them as utilities (the encoded-id class test, the target-buffer find, the presentation-event bridge, the engagement flag), and the four predicate callers read field bit 15 for their own gates.

**Input and InputGameplay — CLIENT, OUT-OF-SCOPE (2 edges).** `InputGameplay_ArbitrateDigitalInputAndModalState` `00253C70` and the capability / UI-request inhibit reconciliation `00313A00` call the field predicate `00377C20`. This contract cites the predicate only as the lethal chain's can-die consult; the input arbiter and the inhibit reconciliation read the same per-area bit for their own permission tests.

**Items_Equipment_Shops_License — SERVICE and CLIENT (26 edges).** The applier `003112F0` calls the item writer `003008A0`, which calls `Inventory_QueryEncodedItemStateByClass` `00309F30` (itself calling `InventoryBitsetClass_QueryState` `002FD970`). `003008A0` is also called by twelve other inventory bodies, among them `Shop_CommitPurchaseItemAndGil` `002FEEB0`, `Shop_CommitSaleItemAndGil` `00310870`, `Inventory_GrantEncodedLootItem` `00300B80` and the bundle appliers `002FD530`, `002FD640` and `002FD780`. The equipment and licence setters `BattleStats_SetEquipmentSlotDirect` `0031A630`, `0031A410`, `0031A510` and `BattleStats_SetLicenseNodeStateAndApplySideEffects` `00323910` call both the recompute `0030FED0` and the resolver `0031B860`; `00309FB0` and `0030FD10` call `00377C20`. `003008A0` is the one inventory write that every item path shares, and the applier reaches it only for steal and item effects; the equipment and licence setters call the same recompute this page describes after they change a slot or a node.

**Movement — CLIENT and SERVICE (9 edges).** The defeat arm `00312280` calls `00319490`, which decides whether a loot bundle may spawn at the victim position by passing it, with the party focus actor, to a movement-side query. `00313500` calls `003299B0`; the locomotion bodies `0033CB10` and `0033D890` call the resolver `0031B860`; `0025B470`, `0026C3E0`, `002E28E0`, `00310920` and `00313670` call the field predicate `00377C20`. Apart from the loot-placement check, these are movement bodies that use the same shared resolver, dispatcher and predicate for their own locomotion work.

**Party — CLIENT (3 edges).** The stats reset support `00328BD0` calls the recompute `0030FED0`; `BattleUnit_SeedPartyCombatStanceRecheckTimer` `003081E0` calls the tick getter `0032A150`; the main-member collector `00304180` calls `00377C20`. Each is a party body using a shared helper this page cites (the recompute after a reset, the clock for a stance timer, bit 15 while collecting members) and none takes part in applying a result.

**PlatformOnlineAchievements — SERVICE (19 edges).** The defeat arm `00312280` calls the achievement counter update `00316A50`; the rest are that family's own calls: the evaluator `00315E90` reaches `00315420`, `003160C0`, `003161A0`, the fire helper `003165C0`, the read `003166F0`, `00316760` and `008632B0`; `00316A50` calls `00315E90`, `003165C0`, `003166F0`, the store `00316BF0` and `008632B0`; `00316930` and `003162E0` are further callers of `00315E90` and `003165C0`. The crossing is that combat results bump achievement counters through `00316A50`; the page cites the family only at that boundary, and the counters' behaviour is the achievement-counter contract's.

**Presentation — SERVICE and CLIENT (7 edges).** The defeat arm `00312280` calls `Reward_PublishExpLpPresentation` `0028FB80`, which posts the EXP / LP floating text. `PartyCombat_UpdateStanceState` `00307E70` and `BattleUnit_ComputePartyBattleStance` `00308130` call the tick getter `0032A150`; `00307E70`, `BattleUnit_ComputePresentationSuppressionMask` `003125E0`, `BattleUnit_BroadcastPartyCombatTargetRelation` `00313B30` and `AddMotion_ApplyBonePose` `003714A0` call the field predicate `00377C20`. Only the floating-text publish is part of the defeat path; the others use the clock and the per-area bit for their own stance and presentation decisions.

**RNG_Random_Selection — SERVICE (2 edges).** The per-level stat folds `002F9A60` and `002F9B20`, called by the level grower `0030C650`, each call `RNG_MT19937_NextU32_Thunk` `00379CD0`: level-up growth draws from the shared Mersenne Twister, so a level change applied by a result is not a pure function of the record.

**Rewards_Progression_Economy — SERVICE and CLIENT (28 edges).** The applier `003112F0` calls `GameState_GetGil` `00253690`, `GameState_SetGil` `00254EE0` and the level grower `0030C650`; `0030C650` calls the stat folds `002F9A60`, `002F9B20` and `002F9BD0` and is also called by `0030C470` and by the defeat arm `00312280`; `00312280` calls `Reward_ComputeExperienceForRecipient` `002F8BB0`, `Reward_ComputeLicensePointsForRecipient` `002F90C0`, `002F8F20`, `EnemyChain_UpdateOnDefeat` `00317ED0`, `Loot_RollDropEntries` `003180F0` and `Loot_CreateWorldPickup` `00319CA0`; the status write `0030E360` reaches `00312280` on a KO. The apply path hands off to the rewards layer at three points - the gil adjustment, a record's level change, and the KO arm that pays EXP / LP, advances the chain and rolls loot.

**Script_VM_Native_Bridge — CLIENT, OUT-OF-SCOPE (4 edges).** The script-side bodies `00344740`, `00352FA0`, `003537D0` and `00355680` call the field predicate `00377C20`. Scripts read the same per-area bit through their own verbs; this contract cites the predicate only inside the lethal chain.

**Spawn_Encounter_Lifecycle — SERVICE and CLIENT (9 edges).** On a kill the HP setter `00300530` calls `SpawnGroup_RecordMemberDeathAndHandleCompletion` `00306F00`, which calls `SpawnLaneMap_ResolveBkeiIndex` `002360D0` and the dispatcher `003299B0`. `Spawn_SetAllSpawnBackedUnitsCurrentHPZero` `002352E0` and `SpawnUnit_FinalizeSpawnEntryActivation` `0023A410` call the absolute HP setter `00300520`, and `0023A410` also calls the recompute `0030FED0`; `SpawnKeep_RotatePersistenceBanksForAreaTransition` `00233780`, `Spawn_SelectAndPrepareAutomaticEntry` `00235720` and `SpawnEntry_GetElapsedTicksSinceLastDeath` `00235FB0` call the tick getter `0032A150`. The lethal chain reports each foe death to its spawn group (the credit chain this page names), and the spawn layer uses the same HP setter and recompute when it activates or zeroes spawn-backed units.

**Status_Periodic_Terminal — SERVICE and CLIENT (47 edges).** This page's status subjects are filed to that layer: `0030E360`, `0030E130`, `0030EA40` and `0030FED0` call one another and `BattleUnit_ResetActionControlForStatusTransition` `00300140`, `BattleUnit_RecoverFromTerminalStatusSetIfClear` `00301140`, `BattleStatus_ComputeDefaultShortTimer` `003876D0`, `BattleStatus_ComputeDefaultDwordParameter` `00387730` and `BattleStatus_ComputeDefaultAuxiliaryTimer` `00387020`, and they are called by the add / remove helpers `0030E990`, `0030EAE0`, `0030F690`, `0030E8F0` and `0030E970`. `BattleUnit_RunPeriodicCombatMaintenance` `00310DB0` calls the applier `003112F0` and the resource setter `00300CE0`, which itself calls `BattleUnit_ClearPrimaryResourceRecoveryAccumulator` `002FA540`; `002F9400` and `00386860` call the resolver `0031B860`; `00301140`, `00310DB0` and `BattleFormula_ApplyGlobalPeriodicDrainModes` `00385CA0` call the tick getter `0032A150`. The applier delegates every status and layer change to the status layer's writers, and the periodic tick is a second caller of the same applier and setters.

**WorldAreaField — SERVICE and CLIENT (6 edges).** `00300530`, `0030E360` and `00312280` call `FieldData_GetActiveFieldRecordBit15` `00377C20`, which calls `WorldTransition_GetActiveOrPendingFieldId` `003148F0`; `BattleSystem_InitializeAreaState` `002342F0` calls `00377C20` and `BattleSystem_RunFieldFrameOrchestrator` `00234590` calls the tick getter `0032A150`. The lethal chain asks the current area's record whether its action-permission override is set (the can-die consult), and the world layer's area setup and field frame call the same two shared getters for their own purposes.

## Falsification pass 1 — 2026-09-30 (OPUS): every clause tested survives

**Attack.** The contract's addressed clauses were turned into checks at their instructions: §2's entry and dispatch,
I1's mask loops and flags, I2's copy-through, I3's dirty flag and outer recompute, §3's layer loops, I6's setter pairs,
I8's availability clear and I7's absent `0x400`. SECTION-01 and OPUS block 332 are carried, not re-run. Script:
`Tools/analysis-kit/gfz-scripts/falsify_apply_result.py`, output `falsify_apply_result.out`, image `73461d08…`,
0 BROKEN, exit 0.

| # | Clause attacked | Result |
|---|---|---|
| A1 | §2 2,040 bytes; owners resolved at `00311321` / `0031132C` | **survives**. Both are `call 0031B860` |
| A2 | §2 the numeric dispatch and the source-MP flags | **survives**. The gates are `bt ecx, 8` (`00311610`), `bt ecx, 0xe` (`0031166D`), `byte [rbx + 0x1d]` (`003116A6`, then `00300BC0` at `003116E0`), `test rcx, rcx` (`003116FB`), `test dl, dl` (`00311703`) and `bt r9d, 0xd` (`00311748`). The flags are built as `shr 7`, `not`, `and 0x10`, `shr 0xa`, `and 0x20`, `or` |
| A3 | I1 the two mask loops: mode 3 and mode 0, flags (`x & 0x10` with `0x1000` set) `>> 3` and (`x & 0x20` with `0x2000` set) `>> 4` | **survives**. The mode argument is `3` at `0031153A` and `r13d` = 0 at `0031159F`. The flags are built at `003114D2`–`003114EE` with `bts eax, 0xc` and `bts ecx, 0xd` for the `0x1000` / `0x2000` bits |
| A4 | I2 the copy-through to `target + 0xBC + 4i` and `target + 0x13C + 2i` | **survives**. `r9 = target − record`, the cursor runs from `record + 0x5C`, and the store `[r9 + rcx + 0x60]` lands at `target + 0xBC + 4i` for `0x20` entries, skipping negatives. The words run from `record + 0xDC` through `[rax + r9 + 0x60]` to `target + 0x13C + 2i` |
| A5 | I3 the dirty flag and the outer recompute | **survives**. `mov r14d, 1` at `0031153F`, `003115A4`, `003117D0` and `0031180C`, with no result test. `[rsp + 0x44] = (callerFlags >> 9) & 1` (`00311344`–`00311350`). The tail tests the target, that local and `r14d`, then calls `0030FED0` with `edx = 0` |
| A6 | §3 the two layer loops call `0030E130` | **survives** (`003117CB`, `00311807`) |
| A7 | I6 the absolute/delta pairs | **survives**. All four setters, `00300520` / `00300530` and `00300C90` / `00300CE0`, are loaded by `lea` and called through the selected register |
| A8 | I8 the gate clears availability; the steal loop finds it clear | **survives**. `and byte [rax + 0x14], 0xfb / 0xfd / 0xfe` at `00385C17`, `00385C41` and `00385C6B`; `0031137A call 00385BA0`; `0031146C btr` |
| A9 | I7 no unconditional `0x400` in the target-HP flags | **survives**. There is no `0x400` immediate in `00311610`–`0031166D` |

**Verdict.** The contract's addressed clauses hold; several are compiled in forms the prose does not show (`bts` setting the
`0x1000` / `0x2000` bits, and base-difference addressing for the copy-through). Tier 1 (static).
