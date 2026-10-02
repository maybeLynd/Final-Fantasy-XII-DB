---
contract: decide whether a unit is licensed for an action - three exits before any board is read, a bitmask overlap for ordinary actions, and a counted gate for Quickenings
category: 12-Items-Equipment-Shops-License
scope: subsystem
level: L2
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 12-Items-Equipment-Shops-License/license-check-what-the-board-actually-tests.md
entries: ["00323EC0", "00323BB0", "00324020", "0030A330"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: assembled 2026-09-20 from the page's reading with site citations. ALL FOUR BODIES WERE
    THEN RE-DERIVED FROM THE SHIPPING IMAGE ON 2026-09-21 (OPUS) - 00323EC0, 00323BB0, 00324020 and
    0030A330 read instruction by instruction, plus the validator 00322C50. I1, I3, I4, I5 and §10's
    edge all survive; the RECEIVER did not, see §3. EXECUTED SINCE: EXP-140 (0d068c953) and the
    shipped-table replay, see §13. Falsification pass 1 (2026-09-29, OPUS) at the end of this page.
last_reviewed: 2026-09-29
audit:
  by: OPUS
  date: 2026-09-21
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-license-check-falsification-pass-1
---

# Contract — the licence check

> **Provenance, stated once.** **[page]** marks what is carried from
> [the licence-check page](license-check-what-the-board-actually-tests.md). **[live]** marks what
> only a running game settles. ~~**There is no execution marker in this contract, because there is no
> executed evidence** — §13.~~ *Struck 2026-09-29 (OPUS, falsification pass 1): EXP-140 and the shipped-table
> replay executed it; §13 cites both.*

## 1. Purpose

Before a character may cast a spell, use a technick or equip a weapon, the game asks whether that
character has bought the licence for it. This is the function that answers, and most of the time it
answers **without reading the board at all**.

## 2. Interface

| | |
|---|---|
| ask | `BattleStats_HasRequiredLicenseForAction(RCX = statsRecord, EDX = actionId)` (`00323EC0`) — **non-zero means licensed** |
| bounds check | `BattleEncodedId_IsValidForClass(ECX = 0x14, EDX = actionId)` (`00322C50`) |
| ordinary actions | `BattleStats_HasLicensePrerequisiteForRequirement(RCX = statsRecord, EDX = 1, R8D = actionId)` (`00323BB0`) |
| requirement mask | `LicenseData_BuildPrerequisiteNodeMaskForRequirement(ECX = 1, EDX = actionId16, R8 = out[0x2E])` (`002F8FA0`) |
| Quickening count | `BattleStats_CountLicenseBits00To17(RCX = statsRecord)` (`00324020`) |
| slot-row search | `0030A330(RCX = row, DX = actionId16)` → `0, 1, 2`, or **3** when absent or the row is null |

> **SIGNATURES RE-DERIVED 2026-09-21 (OPUS).** The page gave names; these are the registers.
> **Three of them carry facts the contract did not record.** `00323BB0` takes a SECOND PARAMETER
> that ~~the only caller fixes at **1**~~ this contract's caller fixes at **1** (`mov edx, 1` at `00323FE6`) and that becomes the first
> argument of the mask builder - so the builder is selecting *something* by kind and the licence
> path only ever asks for kind 1. *Corrected 2026-09-29 (OPUS, falsification pass 1, `CON-159`): `00323BB0` has a
> second entrant, the equipment check `00323C60`, which passes kind **0**. The kind selects licence records by the
> class of their byte `+5`: 0 for equipment, 1 for actions.* `0030A330` takes the action id **truncated to 16 bits**
> (`movzx edx, bx`). And `00323EC0` zeroes `R8D` before calling the validator, which looks like a
> third argument and is not: `00322C50` never reads the incoming `R8D`, and the `xor r8d, r8d` is
> there so the class can be materialised as `lea ecx, [r8 + 0x14]` in three bytes.
>
> **The validator, read at `00322C50`:** the class must be **1..32** (`lea eax, [rcx-1]` /
> `cmp eax, 0x1f` / `ja`), and dispatch is a **jump table at image + `0x203054` indexed by
> class - 1**. Class `0x14` is in range.

## 3. Types

**The owned-licence bitmask is 46 bytes at `statsRecord + 0x194`** — `_types` declares it
`licenceOwnedBits`, `uint8[46]`, ~~**node ids 0..360, so 361 of the 368 bits are spoken for**~~ ~~**the boards use node ids 0..360, but the node table holds 360 records, ids 0..359, so 360 bits can be granted**; bit 360 is set only by a save image that already carries it *(corrected 2026-10-02, OPUS: license-board-grid-format.md §2.3, `32 + 360 * 24 = 8672` on the four shipped `license_data.bin` copies; license-check-what-the-board-actually-tests.md §11)*~~ **node ids 0..360, so 361 of the 368 bits are spoken for**: the node table the game loads holds 361 records, ids 0..360, and node 360 passes the range check; the square is refused with reason 8 until presence bit `0xC01F` is set *(corrected 2026-10-02, OPUS: the same-day correction struck here was wrong - the node table the game checks is `02EBF038`, bound only by `00236C30` at `00236D5C`–`00236D67` from the `battle_pack.bin` blob (`0208E680`) directory `+0x34`, an `st2e` table of 361 records of 24 bytes in all nine language copies; `00322C50` reads its count `[02EBF038]+4` (`00322FCB`–`00322FD9`); the `license_data.bin` path strings `00A400B8` and `00C19F18` have no code reference, so the standalone 360-record files are not what the game loads; the 360 records are the standalone file's; the `0xC01F` test is at `00323E88`, license-check-what-the-board-actually-tests.md the section "13. Buying a licence square: 00323D10")*. The
requirement mask built per action has the same `0x2E`-byte shape.

> **THE RECEIVER IS THE `BattleStatsRecord`, AND THIS CONTRACT SAID OTHERWISE — corrected
> 2026-09-21 (OPUS) from the bodies.** §4's I1 called argument 1 `unit` and this section routed the
> mask through *"the `BattleStatsRecord` behind unit `+0x698`"*. **There is no `+0x698` dereference
> anywhere in `00323EC0` or `00323BB0`.** One pointer arrives in `RCX` and everything is read off
> it: `byte [rsi+5]` and `byte [rsi+4]` in the entry, and `byte [rbx + rax + 0x194]` in the
> prerequisite test, where `rbx` is that same argument. **`_types` declares all three of those
> offsets on `BattleStatsRecord`** — `+0x004 definitionRowIndex`, `+0x005 kindByte`,
> `+0x194 licenceOwnedBits` — and the function's own name is `BattleStats_…`.
>
> **The 2026-09-11 correction was right about the OBJECT and this contract then mislabelled the
> ARGUMENT**, which reads as a second object hop that the code does not perform. A reimplementation
> following §4 literally would take a unit, dereference `+0x698`, and then look for the kind and
> slot bytes on the wrong side of that hop.
>
> **`368 bits, one per board node` is also withdrawn.** 46 bytes is 368 bits, but `_types` bounds
> the node ids at 0..360. The seven-bit remainder is not claimed as anything.

## 4. Preconditions · postconditions · invariants

**I1 — ~~THREE~~ FOUR EXITS BEFORE ANY BOARD DATA IS TOUCHED** (one unlicensed, three licensed; counted 2026-09-29, OPUS), in order **[page]**:

```c
// rec is the BattleStatsRecord, NOT a BattleUnit - see section 3 and CON-144.
if (BattleEncodedId_IsValidForClass(0x14, actionId) == 0) return 0;  // 00323ED6
if (rec == NULL)  return 1;                                          // 00323EEA
if (rec[5] != 0)  return 1;   // kindByte:           00323EF3
if (rec[4] > 6)   return 1;   // +0x004, see CON-145: 00323EFF, UNSIGNED, so 0..6 pass
```

**I2 — THE LICENCE SYSTEM APPLIES ONLY TO RECORD KIND 0 WITH SLOT ≤ 6. Everything else is licensed
for everything**, returned before a single node is read. **The board is not a property of the
ability; it is a property of being a licensed party member** — ~~guests and non-party units do not~~
~~*fail* this check, they never reach it~~ **[page]**; non-party units and guests 7–16 never reach it, but the guest row 6, Reks, does: the test is the type id `+4` ≤ 6 *(corrected 2026-10-02, OPUS: checked at `00323EFF`; §10, "slot 6 included")*.

**I3 — a per-action escape hatch.** `row = decode(*(02EBF138) + 0x0C) + u16(*(02EBF138) + 0x08) * actionId`
— **a descriptor, not an array; see §15**, and the sum is formed **in 32 bits** (`imul ecx, ebx` / `add ecx, eax`,
`00323F43`; pass 1, 2026-09-29), so the decoded base loses its upper half; **bit `0x2000` at `+0x2C`
means "no licence required"**. The test is **16-bit**, so it is bit 5 of the byte at `+0x2D`, and
**98 of the 543 shipped rows set it** **[page]**.

**I4 — THE GENERAL TEST IS AN OR ACROSS NODES, NOT AN AND.** A 46-byte requirement mask is built and
AND-ed byte-wise against the owned mask; **any single overlapping bit licenses the action**, and the
loop **returns on the first non-zero byte**. So an ability appearing in four board squares is
unlocked by whichever square was bought, and **there is no notion of a required square**.
~~**The early exit is semantically load-bearing, not an optimisation**~~ **[page]**. *Withdrawn 2026-09-29 (OPUS,
falsification pass 1, `CON-160`): nothing after the loop writes, calls or computes. The two exits load the constants
1 and 0, so the answer is the OR of all 46 byte-ANDs whether or not the loop stops early. The early exit is an
optimisation.*

**I5 — QUICKENINGS ARE COUNTED, NOT MATCHED.** Action ids **`0xD0`–`0xE1`** (18 ids) never reach I4:

```c
// Both tables are DESCRIPTORS: u16 stride at +0x08, ENCODED pointer at +0x0C (decode = 0020E600).
row = decode(*(02EBF130) + 0x0C) + u16(*(02EBF130) + 0x08) * rec[4];  // by rec[4], not by action
idx = 0030A330(row, (uint16)actionId);   // matches BYTES at row+4/+5/+6; 3 if absent/null
n   = popcount(rec[0x194] bits 0..17);   // 00324020: 3 passes x 6 bits
return (int)idx < (int)n;                // setl - SIGNED
```

Each party slot names **three** action ids, and the *k*-th is available once the unit owns at least
*k + 1* of bits 0–17 — *"you have unlocked two Quickenings, so you may use the first two"* **[page]**.

## 5. State

`02EBF138` the action-row table (543 rows), `02EBF130` the party table indexed by slot, and the
owned mask at `statsRecord + 0x194`.

## 6. Relationships

`BattleEncodedId_IsValidForClass(0x14, …)` is the bounds check of I1 — the same validator S-04's
contract governs, here called with class `0x14`. The requirement mask is built by
`LicenseData_BuildPrerequisiteNodeMaskForRequirement` **[page]**.

## 7. State transitions

None — the check is a pure query. It mutates nothing.

## 8. Script · resource · event interactions

The action rows and the board grid are **authored data**; the grid format has its own page and
loader contract **[page]**.

## 9. Determinism

**Fully deterministic.** No RNG, no time, no frame state. The same unit and action always answer the
same way.

## 10. Failure paths and edge conditions

* **Invalid action id** → `0` (the only path that returns *unlicensed* without consulting anything).
* **A NULL-DECODING ACTION ROW FAULTS AT `00323F52` — the fault is real, the trigger recorded here
  was not.** Found 2026-09-21 (OPUS) by re-deriving `00323EC0`; **corrected the same day by EXP-140
  (SWE2-ORACLE, `0d068c953`), which executed the shipped bytes instead of reasoning about them.**
  * *What stands:* the null test at `00323F17`/`00323F27` chooses *which* pointer is dereferenced,
    not *whether* one is. Both failing branches reach `00323F4A` `mov rcx, rdi` with `rdi` zeroed at
    `00323F15`, falling into `00323F52` `test word ptr [rcx + 0x2c], ax`. EXP-140 reproduced exactly
    that fault — `memr 0x2C,2` at `0x323F52`, with `RAX = 0x2000` left stale — so the read of address
    `0x2C` is confirmed on bytes, register residue and all.
  * *What was wrong:* **nulling the table pointer at `02EBF138` cannot reach it.** The class-`0x14`
    validator arm at `00322F72` reads **that same cell** — the action-table descriptor itself, bound
    `d[desc+4]` — and rejects the id first, returning `0` before I3 ever runs (`m-nulla` → 0, no
    fault). The contract had the validator consulting a separate class-specific count source; it does
    not.
  * *What actually reaches it:* the descriptor **non-null** with an `enc` that decodes to a null or
    low row. `m-nullrow` plants `enc = −BASEP`, so `decode` yields `rax = 2^32` — non-null, passing
    every guard — while the row base truncates to `0`. **The guard tests the descriptor; the faulting
    dereference uses a row decoded from it, and those are different things.**
  * *Still not claimed:* that either state occurs in a running game. Whether `enc` can decode this way
    at a licence check is a lifetime question this contract does not settle.
* **A null PARTY descriptor is safe by construction** (EXP-140 `m-nullp`): `prow = 0` takes ROWSRCH's
  null-row arm, which returns idx `3`, and `3` is then compared against the count exactly like any
  absent action. No fault, and no special case is needed in a reimplementation.
* **Null stats record, non-zero kind, `+0x004` > 6** → `1`, licensed (I2).
* **`0x2000` set** → `1` (I3).
* **AN OVER-PERMISSION EDGE AT I5 — NO LONGER UNRESOLVED; EXP-140 SETTLED IT ON BYTES.**
  `0030A330` returns **3** when the action is not among the slot's three, and the comparison against
  the Quickening count is a **signed `setl`**, so `idx < n`. Executed: a count of **4 licenses an
  absent Quickening row** (`m-qabsent4` → 1) and a count of **3 denies it** (`m-qabsent3x` → 0).
  The edge is therefore not a possibility but a demonstrated behaviour of the shipped code, and a
  reimplementation reproduces it only by keeping the comparison signed and the sentinel at 3.
  *What remains open is narrower than before:* whether a party member can actually reach a count of
  4 or more depends on what bits 0–17 are, which is still unestablished — see §14.
  **On shipped data the edge crosses characters** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 326, which executed the check over the shipped licence, ability and party-slot tables; [its package](../_index/candidates/s31-opus-replay-licence-check-shipped/README.md) was read.)*. Party slots 0–5 each name three Quickening ids.
  Together the six rows cover `0xD0`–`0xE1` exactly, and slot 6's row is `00 00 00`. So a Quickening from another
  slot's row is absent from this slot's row, and `0030A330` returns 3 for it. The id is refused while 3 of bits
  0–17 are owned and **licensed once 4 are**, for every slot, slot 6 included. Slot 6 is licensed for all 18 at
  4 bits. *Whether one record can own 4 of those bits is a question about the board-purchase rules, which these
  tables do not hold. It stays open.*
* **I5 PRECEDES I4 UNCONDITIONALLY** (EXP-140 `m-qflank` → 0): for ids `0xD0`–`0xE1` an owned I4
  licence **cannot** rescue an absent Quickening row. The ordering is load-bearing, not incidental.

## 11. Observable behaviour

A party member cannot use what they have not bought; everyone else can use everything. Quickenings
appear in order as the count rises.

## 12. Reproduction formula

Implement I1's exits **in order and before anything else** — most calls never get past them.
Implement I4 as a byte-wise AND whose answer is **any non-zero byte**. An early return on the first one is
allowed, and so is a full mask compare: the observable behaviour is identical. *(2026-09-29, OPUS: I4's
"load-bearing" wording is withdrawn, `CON-160`.)* What must not happen is an AND across all nodes, which would
require every square. Implement I5 as `idx < n`
**including the `idx = 3` case**, rather than "reject unknown ids" — that difference is exactly the
edge in §10.

## 13. Runtime validation

**EXECUTED — [EXP-140](../_experiments/EXP-140-license-check-exec.md)** (SWE2-ORACLE, `0d068c953`;
57/57 functional + 35/35 mutants on shipped bytes over disclosed BSS-planted descriptor fixtures;
bounded-predicate evidence, **no initialised-gameplay reachability claim**). Its six findings are
consumed by the owner, 2026-09-25 (OPUS): the signed-`setl` over-permission edge, I5 before I4, the
corrected null trigger and the null-party safety are recorded in §10; the POPCNT walk (bits 0..17
only) in §14; and the BUILDER here, **re-read statically and agreeing**:

* **`LicenseData_BuildPrerequisiteNodeMaskForRequirement` `002F8FA0`** first ~~**zeroes the caller's
  buffer**~~ **clears `(n + 7) >> 3` bytes of it** — `00861EC0(buf, 0, (n + 7) >> 3)` at `002F8FE0`, `n = d[desc + 4]` — then loops `i` from
  0 while `i < n`, the bound signed (`002F8FFF jle`, `002F9090 jge`), so `n ≤ 0` builds ~~an all-zero
  mask~~ a mask with no bit set.
  *Qualified 2026-09-27 (OPUS, on ASTRA's license-builder-clear-boundary): the clear size is computed before the signed gate and in 32 bits - `002F8FD3 lea r8d, [rax+7]`, then `002F8FD9 shr r8, 3` on the zero-extended value - so the gate cannot vouch for it. Executed on supplied descriptor counts: 0 clears 0 bytes and 8 clears 1; `FFFFFFF9` (signed −7) wraps to a 0-byte clear; `FFFFFFF8` (signed −8) requests 536,870,911 bytes and the run stops at the scripted clear's entry, before any write or the loop test. So the builder guarantees only `(n + 7) >> 3` cleared bytes for `0 ≤ n`, and a caller must supply `n` with `(n + 7) >> 3` no larger than its buffer. A zero count leaves the caller's bytes as they were; the **46-byte guarantee on the normal path is the caller's**: `00323BB0` zeroes five qwords, a dword and a word at `rsp+0x20`..`0x4D` (`00323BD4`..`00323BF5`) before calling the builder at `00323BFC`. What loader validation keeps a shipped `n` in range is not established here; EXP-140's normal predicate and absent-action edge are unchanged. Control: `_experiments/evidence/license-builder-clear-boundary/check.py` (ASTRA; 7 rejecting counterexamples).* Each row **reloads the descriptor** (`002F9092`) and computes `row = decode(enc) +
  u16[desc + 8] * i` **in 32 bits** (`002F903C imul ebx, edi` / `002F903F add ebx, eax`), classifies
  `b[row + 5]` through `00323890` against its first argument, scans **eight `u16` requirement slots
  at `row + 8`** for its second, and on the first match `bts`-sets bit `i` of the buffer
  (`002F9082`) and counts it. **Returns the match count** (`ebp`).
* **Static only, not executed:** when the row decodes to null the builder sets `ebx = 0`
  (`002F9043`) and still reads `byte ptr [rbx + 5]` — the same *guard on the descriptor, dereference
  of the decoded row* shape as §10's `00323F52` fault. A null **descriptor** is safe (`n` becomes 0
  at `002F8FF7` and the loop never runs).

*The section's former text — "NONE. Nothing in this subsystem has been executed" — is superseded;
it stood beside §10's executed results and contradicted them.*

> *HISTORICAL (superseded 2026-09-25 by EXP-140 above; kept as the record of why the run was asked for):*
> **STILL NONE AFTER 2026-09-21 (OPUS), and the distinction matters.** Every body is now read from
> the shipping image rather than carried from a page, which raises the evidence from *one reading,
> restated* to *two independent readings that agree*. **It is still static evidence.** Reading an
> instruction is not running it, this row stays `nothing executed`, and
> `OPUS-REQ-ASTRA-S31-LICENCE-CHECK-ISOLATED-RUN` stays the open request. What re-derivation did
> buy is that the isolated run now has exact register signatures to drive and a named null path to
> probe.

*HISTORICAL:* ~~This makes the contract the second `nothing executed` one in the database, after S-33's.~~ It is
written anyway: withholding a correct contract to protect a gate row would be the wrong trade, and
the scoring tension that creates was already raised with FRONTIER when S-33 became the first.

*HISTORICAL — the request below was answered by SWE2-ORACLE's EXP-140, not by ASTRA:* **The fixable part is routed, not lamented.** These bodies are unusually good isolated-execution
candidates — `00323BB0` is short enough to quote whole, `00324020` is an unrolled popcount,
`0030A330` searches three bytes — so an isolated run is requested as
`OPUS-REQ-ASTRA-S31-LICENCE-CHECK-ISOLATED-RUN`. **§10's over-permission edge is the case to drive
first.**

## 14. Unresolved

* ~~**Whether bits 0–17 are exclusively the Quickening squares** — the mechanism is read, **the
  meaning of the bit range is not** **[page]**.~~ **PARTIAL: the data answer is yes, within the licence tables**
  *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 326, which executed the check over the shipped licence, ability and party-slot tables; [its package](../_index/candidates/s31-opus-replay-licence-check-shipped/README.md) was read.)*. Licence records 0–17 are a block of 18 kind-19 records that list no id. The kind-1 mask builder,
  run over all 543 ability ids, never sets any of those bits. Party-slot rows 0–5 name exactly the 18 Quickening
  ids `0xD0`–`0xE1`. So in those tables, bits 0–17 do nothing except feed `00324020`'s count, and there are as many
  of them as there are Quickenings. *Still open: whether any other code reads those bits, since no image-wide reader
  census of the licence word was run, and whether the board can grant four of them to one record (§10).*
* ~~**What happens when the Quickening count exceeds 3** (§10).~~ **ANSWERED on bytes by EXP-140
  (`0d068c953`): a count of 4 licenses an absent row, 3 denies it — the comparison is a signed
  `setl`.** What remains unresolved is only whether such a count is *reachable*, which still turns on
  the bit range's meaning above.
* ~~**Nothing is executed** (§13), so every invariant here is a reading.~~ **Superseded 2026-09-21:**
  EXP-140 executed the shipped bytes — 57/57 functional and 35/35 mutants over disclosed BSS-planted
  descriptor fixtures. **The bound is what that evidence is, not how much of it there is:** it is
  bounded-predicate evidence over planted fixtures, so it establishes what the code DOES with a given
  state and claims nothing about which states an initialised game reaches. §10's two reachability
  caveats stand unchanged.
* **No live evidence** **[live]**.

## 15. Evidence

~~Entirely the page's reading~~ *(struck 2026-09-29: §13's executed evidence and the re-derivation below are not the
page's)* The page's reading, including its correction that the mask lives on the **stats record**
and not the unit **[page]**. This contract's contribution is I1–I5 stated as a contract, §10's
identification of the `idx = 3` over-permission edge as a *named unresolved condition* rather than a
footnote, and §12's three "implement it this way" notes.


> **INDEPENDENT RE-DERIVATION, 2026-09-21 (OPUS).** The four entries plus the validator `00322C50`
> were read instruction by instruction. **What was confirmed, and it is most of the contract:**
> I1's four exits in that order with those return values; I3's `test word ptr [row+0x2c], 0x2000`
> at `00323F52`; I4's `0x2E`-byte loop at `00323C10`-`00323C2B`, byte-wise `test` with a return on
> the first non-zero byte, against `+0x194`; I5's range as `lea eax, [rbx-0xd0]` / `cmp eax, 0x11`
> / `ja`, so `0xD0`..`0xE1` inclusive; and `idx < n` as `cmp ebx, eax` / **`setl`**, which is a
> **signed** comparison.
>
> **`00324020` is not "an unrolled popcount" - it is a loop of three passes over six bits**, which
> is how the count is pinned to exactly bits 0..17 from the instructions rather than from the name.
> `lea edi, [r9+3]` sets the trip count to 3 and `sub rdi, 1` / `jne 00324040` closes it; each pass
> tests six consecutive bit indices `[r11-2 .. r11+3]` with `rol dl, 1` walking the mask and
> `shr rcx, 3` selecting the byte. **18 bits, and the byte base is `rbx + 0x194` - the same
> receiver.**
>
> **`0030A330`'s three ids are BYTES.** It reads `movzx ecx, byte ptr [rax + r9 + 4]` for
> `rax` in `0..2`, so the slot row's three action ids live at **`+0x04`, `+0x05`, `+0x06`, one byte
> each**, and compares them 16-bit against the id. The absent case loads `0xFFFF`, which no
> byte-sourced id can equal - that is *why* the function returns 3 rather than a false match.
>
> **BOTH TABLES ARE DESCRIPTORS, NOT ARRAYS**, and this is the structural fact the contract was
> missing. `02EBF138` and `02EBF130` each hold a **`uint16` element stride at `+0x08`** and an
> **encoded pointer at `+0x0C`** decoded by `0020E600` (`x + qword[01F83530]`, the engine-wide
> convention). A row is `decode(desc+0x0C) + stride * index` - `imul ecx, ebx` at `00323F43` for
> the action table and `imul ecx, edx` at `00323FAF` for the party table. **`table(02EBF138)[id]`
> as written in §4 is not an addressing mode the image has**, and a reimplementation that treats
> either symbol as the base of a flat array reads the wrong memory.
>
> **The requirement mask is a caller-zeroed stack buffer.** `00323BB0` clears all `0x2E` bytes
> field by field (`00323BD4`-`00323BF5`: five qwords, a dword and a word) *before* calling the
> builder. **The builder may therefore write sparsely**, and a reimplementation that hands it
> uninitialised storage is wrong in a way that only shows up on nodes the builder does not touch.
## 16. Parity plan

Drive the three exits of I1 first and assert the **return value and that no board read occurred** —
most calls end there, so a reimplementation that reads the board anyway is wrong even when it
answers correctly. Then I4 with an ability in several squares, owning each square in turn. Then I5
across counts 0–4 **including an action absent from the slot's three at count 4**, which is §10's
edge. **Do not build the parity fixture from this contract alone** — nothing in it is executed, so
the fixture and the contract would share any error. *(2026-09-29, OPUS: the reason is now out of date, because EXP-140
executed it. The advice stands: build the fixture from the shipped bytes and EXP-140's harness, not from this prose.)*

## Falsification pass 1 — 2026-09-29 (OPUS): two clauses refuted, one formula made exact, four currency lines struck

**Attack.** Every clause of §2-§4, §7 and §9 was turned into a check that fails if the shipping image says otherwise. The
checks decode every listed body in `.text`, so the caller counts and the reference census are whole-image, not local. Script:
`Tools/analysis-kit/gfz-scripts/falsify_license_check.py`, output `falsify_license_check.out`, image `73461d08…`, 0 BROKEN.

| # | Clause attacked | Killer | Result |
|---|---|---|---|
| L0 | §2 class `0x14`, validator range 1..32, jump table at image + `0x203054`, incoming `R8D` unused | another class, range or table, or a read of `r8` before a write | **survives**; the validator's first touch of `r8` is the write at `00322E65` |
| L1 | I1's exits and their order | a reordered test or a signed slot compare | **survives**, but there are **four** exits, not three (below) |
| L2 | I3's escape bit and row formula | another bit, width or offset | **survives, made exact**: the row sum is formed in **32 bits** (below) |
| L3 | I5's range, the party row, the byte search, the signed gate | another range, width or sentinel | **survives**; the party-row sum is 32-bit as well |
| L4 | §15's three passes of six bits | another trip count or stride | **survives** |
| L5 | §2 "the only caller fixes [the kind] at **1**" | a second entrant | **REFUTED** (below) |
| L6 | I4 "the early exit is semantically load-bearing, not an optimisation" | a write, call or computed value after the loop | **REFUTED** (below) |
| L7 | §7 "mutates nothing", §9 "fully deterministic" | another write site, or a global the closure reads that something writes | **survives** (below) |
| L8 | context for §14 | none; this is a count | 00324020 is called at 13 sites in 7 functions |

* **L5: `00323BB0` has two entrants, and the kind is 0 or 1.** Both entrants are tail jumps:
  * `00323EC0` enters at `00323FFD` with `mov edx, 1`;
  * `BattleStats_HasRequiredLicenseForEquipment` (`00323C60`) enters at `00323CF7` with `xor edx, edx`, the item id in
    `r8d`.

  The mask builder `002F8FA0` has one caller, `00323BB0`. It keeps the kind in `r12d` (`002F8FC8`) and compares it with
  `00323890`'s class of each licence row's byte `+5` (`002F9045`-`002F9051`). So the builder selects licence records by
  **requirement kind: 0 for equipment, 1 for actions**. The action path only ever asks for kind 1, as §2 says. It is not the
  only path. The equipment check has its own escape, a bit test `test byte ptr [row + 7], 0x10` on the equipment row
  `id - 0x1000` (`00323CD0`-`00323CDF`). That check belongs to
  [the equipment-compatibility contract](CONTRACT-equipment-compatibility.md), not this one.
* **L6: the early exit is an optimisation.** After the builder returns, `00323BB0` writes no memory and calls only
  `__security_check_cookie`. Its two exits load the constants `1` (`00323C42`) and `0` (`00323C2D`). The value returned is
  therefore "some byte of `owned & required` is non-zero", whether the loop stops at the first such byte or runs to `0x2E`.
  §12 already said *"the observable behaviour is identical"*. I4's sentence contradicted it and is withdrawn. A
  reimplementation may compare the whole mask.
* **L1/L2/L3: precision.**
  * I1 has **four** exits: one unlicensed (the validator) and three licensed (null record, kind byte, slot byte).
  * Both row addresses are summed in 32 bits: `imul ecx, ebx` / `add ecx, eax` at `00323F43` for the action row, and
    `imul ecx, edx` / `add ecx, eax` at `00323FAF` for the party row. The result is zero-extended into `rcx`, so the decoded
    base loses its upper 32 bits. This is why EXP-140's `m-nullrow` could fault with a non-null decode: `rax = 2^32`
    truncates to row `0`. A 64-bit reimplementation that keeps the full pointer takes a different path for any decoded base
    at or above 4 GiB.
* **L7: pure, deterministic, and one scratch buffer.**
  * The closure of `00323EC0` is 16 functions. Five of them are the GS-failure helpers.
  * Outside those helpers, the one memory write is `002F9085`, the builder setting a bit in the caller's stack buffer
    (`r15` = the caller's `r8`), plus the builder's `memset` of the same buffer.
  * The globals it reads, beside 28 descriptor cells and the image-base tables, are:
    * the decode base `01F83530`;
    * the class table `01EEBCF8` (`ItemClassDescriptor`);
    * the GS cookie `01F44830`;
    * `memset`'s import slot.
  * No listed body writes the first two RIP-relatively, and the cookie is written only by CRT start-up (`00809B8C`).
  * No RNG cell and no time import is reached.
* **L8: for §14's open reader question.** The Quickening counter is not private to this check. `00324020` is called at 13
  sites in 7 functions, including `BattleSpecialSequence_BuildRandomizedCandidateActions` (7 sites),
  `BattleStats_SetLicenseNodeStateAndApplySideEffects`, `BattleStats_CheckLicenseNodeAcquireReason` and
  `BattleStats_ComputeLicenseDerivedRank`. So other code does read bits 0-17, as a count. What those readers do with it is
  not claimed here.
* **Currency.** These lines predate EXP-140 and are struck or rewritten here:
  * the provenance note "no executed evidence";
  * the frontmatter's "NOTHING HERE IS EXECUTED";
  * §15's "Entirely the page's reading";
  * §16's "nothing in it is executed".

  EXP-140 (`0d068c953`) and the shipped-table replay (`s31-opus-replay-licence-check-shipped`) are the executed evidence.

Consumer record: [`_index/candidates/license-check-falsification-pass-1-0929/`](../_index/candidates/license-check-falsification-pass-1-0929/README.md).
Contradictions: `CON-159` (the only caller), `CON-160` (the load-bearing exit).

## Cross-subsystem neighbours — SWE2-EC7 (pass-22 dispositions)

- **ActorEntity - CLIENT (5 edges).** `00322C50` is also called by bodies filed to ActorEntity: `002367A0`, `0023A570`, `0031B810` - shared machinery across the layer boundary, no shared ownership.
- **CombatAI - CLIENT (10 edges).** `00322C50` is also called by bodies filed to combat AI: `00301AD0`, `003215C0`, `00321630` - shared machinery across the layer boundary, no shared ownership.
- **CombatAction - CLIENT (11 edges).** `00322C50` is also called by bodies filed to combat action: `002FFCF0`, `003060E0`, `00309300` - shared machinery across the layer boundary, no shared ownership.
- **CombatFormula - CLIENT (1 edge).** `00322C50` is also called by bodies filed to combat formula: `002FEF30` - shared machinery across the layer boundary, no shared ownership.
- **Gameplay - CLIENT and SERVICE (5 edges).** `00322C50`, `00323890` are also called by bodies filed to Gameplay: `0031B9F0` (Combat), `0031C5D0` (BattleEncodedId); `00323C60` reaches bodies filed to Gameplay: `00322C50` (Combat) - shared machinery across the layer boundary, no shared ownership.
- **Movement - CLIENT (2 edges).** `00322C50` is also called by bodies filed to movement: `0031BAC0`, `00326BB0` - shared machinery across the layer boundary, no shared ownership.
- **Party - CLIENT (9 edges).** `00322C50` is also called by bodies filed to party: `003170E0`, `0031AC00`, `0031B510` - shared machinery across the layer boundary, no shared ownership.
- **Status_Periodic_Terminal - CLIENT (4 edges).** `00322C50`, `00323890` are also called by bodies filed to status/periodic terminal: `0030E130`, `0030FED0`, `00310DB0` - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT (1 edge).** `00322C50` is also called by bodies filed to UI: `0031EB20` - shared machinery across the layer boundary, no shared ownership.
