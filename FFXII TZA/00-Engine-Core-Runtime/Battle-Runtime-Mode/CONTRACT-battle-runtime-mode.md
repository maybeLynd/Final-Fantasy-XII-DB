---
contract: Reduce the battle runtime to a mode 0..5, and the four authorities that set it
category: 00-Engine-Core-Runtime
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: battle-runtime-mode-ladder.md
entries: ["0030D9A0", "00377C20", "00303EE0", "00303D90", "003135E0", "00313550", "003072E0", "00307240", "003072A0", "00307200", "0030DA10"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 59 addresses cited - 2 data, 33 entry, 24 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-12
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-battle-runtime-mode-pass-1  # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — the battle runtime mode ladder, and who is allowed to set it

> **Authored 2026-09-12 by OPUS**, answering the third item of
> `FABLE-REQ-OPUS-CONTRACTS-S26-S15-S03`. The mechanism, the four authorities and the mode names are
> FABLE's, on [the ladder page](battle-runtime-mode-ladder.md). What this adds is the interface, the
> state, the transitions and the failure paths as an implementable unit — with the ladder and its
> callee **re-read from the image** rather than taken from the page.
>
> **Two of that page's own statements are stale and are routed rather than repeated here:**
> `OPUS-CONTRA-LADDER-LABELS` (its hierarchy diagram still says *UI* and *combat / audio* where §2b
> retracted both in favour of **the summon** and **the chocobo**) and `OPUS-CONTRA-LADDER-STATUS`
> (its `PARTIAL` summary says modes 0, 1 and 2 are unnamed, while §2c names 1 and 2 and every box in
> its §7 is now ticked). **This contract states the §2b/§2c facts.**

## 1. Purpose

Six numbers decide who owns the party. A running cutscene script outranks the zone's authored data,
which outranks the chocobo you are riding, which outranks the Esper you summoned. Twenty-one call
sites across party control, input arbitration, unit definition and presentation branch on the
answer, and **none of them knows why** — they ask for a number. When your controls lock up as the
leader falls, when an area behaves as though nothing is happening, when a cutscene takes the party
away from you: one function returned a different number.

## 2. Interface

| | |
|---|---|
| entry point | `0030D9A0` `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15`, **5 decision points yielding 6 modes** (§15a — was "6 tests"), no arguments |
| calling convention | Microsoft x64, `void` in, `uint32_t` in `eax`. Reserves `0x28` of shadow space because it calls |
| parameters | none. **Every input is global state** — that is the contract's whole difficulty |
| return | `0..5`, and the value is a *priority*, not a bitmask. Two conditions can hold at once and only the higher is reported |
| the four setters | `00307200` bit 3 · `00307240` bit 2 · `00303D90` bit 1 · `00313550` bit 0 |
| the four bit getters | `003072A0` bit 3 · `003072E0` bit 2 · `00303EE0` bit 1 · `003135E0` bit 0 |
| the two mode getters | `003072C0` returns `ladder() == 4`, `00307280` returns `ladder() == 5` |
| the reset | `0030DA10` zeroes `+0x5B04` **and** `+0x5B08` |

**`00303EC0` is the shape almost every consumer uses**: a four-line wrapper returning
`ladder() == 2`, with 6 direct callers and 15 more through a thunk — 21 in total — plus `00313DB0`,
which tests `== 2` **inline and without the wrapper**. A reimplementation that exposes only the
wrapper loses the site that does not use it.

## 3. Types and state

| location | width | meaning |
|---|---|---|
| `*(void **)0x02EBF190` | 8 | the `BattleSystemState` block — a **runtime state block, not an authored table**, and the single registry slot that broke the authored-table document's *"every authored number"* claim |
| `state + 0x5B04` | 4 | **the mode flags word.** Only bits 0–3 are consulted |
| `state + 0x5B08` | 4 | cleared with it by the reset; not read by the ladder |
| `state + 0x5AE0` | ~~8~~ 4 *(corrected 2026-10-02, OPUS: every access is a dword or a byte, e.g. `00304060+0xD1` `or dword [rax+0x5AE0], 1`, `00304440+0xB` `test byte [rax+0x5AE0], 1`; never a qword)* | the special-sequence word; bit 1 and bits 2–3 are touched by the bit-1 setter |
| `state + 0x5AE4` | 4 | float, written `0x43340000` = **180.0f** when the chocobo bit is set — the ride time |
| `state + 0x5AEC` | 4 | zeroed when the chocobo bit is cleared |
| `*(void **)0x02ADD100` | 8 | the field-record table the bit-15 predicate reads; `+0x04` is its count |

**The flags word is not transient and that is part of the contract.**
`SaveTransitionMetadata_CaptureToRecord` (`002EF3C0`) writes it to `rec+0x28`, alongside
~~`state+0x5AD0..+0x5AEF` at `rec+0x08..+0x27`~~ **`state+0x5AE0..+0x5AEF` at `rec+0x08` and `state+0x5AD0..+0x5ADF` at
`rec+0x18`** — the two 16-byte halves are stored in the opposite order to the state *(corrected 2026-09-26, OPUS, by
execution: `candidates/s03-opus-replay-mode-setters/`, case S)*, and `SaveTransitionMetadata_RestoreFromRecord`
(`002EF410`) puts it back — the `+0x5AE0` half and the flags word always, the `+0x5AD0` half **only when `rec+0x18` bit 1
is set** (`002EF43B`). **The mode survives an area transition and a save**, so a reimplementation
that rebuilds it from live conditions on load will diverge the first time a cutscene saves.

## 4. Preconditions · postconditions · invariants

**Preconditions.** `*(0x02EBF190)` is non-null — the ladder **does not check it** and dereferences
it at `0030D9A4`/`0030D9AB` before any test. The field-record table may be null; that path is
handled (§10).

**Postconditions.** None — the ladder writes nothing. The setters each write one bit and, for bit 1,
a documented side-effect set (§7).

**Invariants.**

1. **Priority, not membership.** `flags = 0b1111` returns 5, not four modes. Every consumer testing
   `== 2` is silently false whenever a higher condition holds, and that is the mechanism behind
   *"per-area waivable"* control suppression — **not** a parallel exemption check.
2. **Exactly four bits are read**, in the order 3, 2, (field bit 15), 1, 0. Bits 4–31 of the word are
   never consulted by this function.
3. **Mode 3 has no bit in this word at all.** It comes from authored area data, and it sits *above*
   mode 2 — which is the entire reason one authored bit can pre-empt a runtime condition.
4. **The two script-set modes are unreachable from gameplay code**: every caller of their four
   accessors is the script VM bridge, and each is reached **through a jump thunk**, so a
   direct-caller census sees zero and concludes "dead". It did, once, and was wrong.

## 5. Relationships

**Callers of the ladder:** ~~`PartyControl_RecomputeSuppressionFromLeaderBattleState` (`0023B040`),~~
~~`InputGameplay_ArbitrateDigitalInputAndModalState` (`00253C70`), `BattleUnit_ApplyUnitDefinition`~~
~~(`0023A570`),~~ `BattleGroup_RefreshFourActorDefinitions` (`003266C0`), ~~`00235EA0`, `00320230`,~~
~~`0035BC50`,~~ `00313DB0` (inline), and the two mode getters. *(corrected 2026-10-02, OPUS: `0023B040`, `00253C70`, `0023A570`, `00235EA0`, `00320230` and `0035BC50` call the wrapper `00303EC0`, which calls the ladder at `00303EC0+0x4` and answers `mode == 2`; the ladder's own 22 direct call sites are in 21 functions from `002FFCF0` to `003266C0`)*

**Callee:** `FieldData_GetActiveFieldRecordBit15` (`00377C20`), which itself calls `003148F0` —
whose result is used as the row index and whose body is **not read here** — and reads the table
at `02ADD100`.

**Crossing layers, accounted.** The ladder's neighbourhood is not confined to this category:
**Movement** asks and answers on 13 edges (`0030D9A0` is also called by `00309AE0`/`00311F70`,
`0023B040`/`00313DB0` by `00234520`, and `003266C0`/`003135C0` reach the `00311E20`/`0033CA00`
locomotion family — a mode change moves or immobilises actors); **spawn**-lifecycle code calls
`0023A570` from `0023A3B0` and is called back through `00236100`, with `003148F0` called by
`00233780` (encounter/field-index plumbing, 3 edges); **items/equipment** bodies `00309FB0` and
`0030FD10` call `00377C20` (2 edges), as does **economy** code `00312280` (1 edge) — the field-bit
predicate is consulted well outside party control; and **platform**/achievements `003160C0` calls
`003148F0` once for the same field index. None of these changes the contract; they state who the
mode word is load-bearing for.

## 6. State transitions

| from | to | condition | authority |
|---|---|---|---|
| any | 5 | bit 3 set | script VM — `seteventparty2mode` (`0x0514`, 1 arg) → `00351E50` → `00307200` |
| any but 5 | 4 | bit 2 set | script VM — `seteventpartymode` (`0x050F`, 1 arg) → `00351B40` → `00307240` |
| any but 5, 4 | 3 | the active field record's bit 15 | **authored area data** — no setter, no verb |
| any but 5, 4, 3 | 2 | bit 1 set | **the chocobo** — `ridechocobo` / `getoffchocobo` / `setchocobomode`, the mount block of the presentation sequence (`00306A13`), the ride's end (`00304680`) |
| any but 5, 4, 3, 2 | 1 | bit 0 set | **the summon** — `summonread` / `summontopartyread` / `btlAtelSetSummonMode`, the summon presentation (`00306946` sets, `00306A7E` clears), `00313840` clears |
| any | 0 | none of the above | — |

> **The two labels this table does not use.** The page's hierarchy diagram calls bit 1
> *combat / audio* and bit 0 *UI*. Those are the owning **category** of the functions, not what
> drives the bits, and §2b retracts them explicitly. `OPUS-CONTRA-LADDER-LABELS`.

**Modes 4 and 5 differ in exactly one place.** Of the 21 callers only
`BattleGroup_RefreshFourActorDefinitions` has separate arms: both rewrite the battle slot map
(~~`+0x5A58`, four 18-byte entries~~ the four mapping-class tables at `+0x5A5A`/`+0x5A6C`/`+0x5A7E`/`+0x5A90`, nine u16 each, classes 1–4 of `0031B9F0`; entries 0, 1, 3 below are classes 1, 2, 4 — corrected 2026-09-14) to the leader alone, but **mode 4 writes entries 0, 1 and 3**
while **mode 5 writes 0 and 1 and restores entry 3** to what it held before the refresh. Entry 2
keeps all nine selectors in both. That is the whole native distinction.

## 7. The setters' side effects, which are not symmetric

`00303D90(on)` — the chocobo bit — does far more than flip it, and **only when the bit actually
changes**:

```c
if (((flags >> 1) & 1) != on) {
    if (on)  { flags |= 2;  state[0x5AE0] |= 0xC;  state[0x5AE4] = 0x43340000f /* 180.0 */; return; }
    flags &= ~2;
    actor3 = PartyRoster_GetActorBySlot(3);       /* the fourth slot - the guest's */
    FUN_002E73C0(actor3, 3);
    state[0x5AEC] = 0;
    if (state[0x5AE0] & 2) { if (actor3) thunk_FUN_002EB030(actor3, 0x2001); /* toggle bit 1 */ }
}
```

**Enabling and disabling are not mirror images**: enabling writes two fields and returns; disabling
touches the party roster, a third field and conditionally posts an event. A reimplementation that
models the setter as `flags = (flags & ~2) | (on << 1)` loses the ride timer, the guest slot and the
event.

The bit-2 and bit-3 setters are the plain shape — write the bit, **write nothing when it already
equals the argument**. *The bit-0 setter `00313550` is not quite plain (added 2026-09-26, OPUS, by execution): after its one
write it **tail-jumps to `0035C620`** with `edx` = the new flags word; when the bit already equals the argument it writes
nothing and does not jump.*

## 8. Script · resource · event interactions

Six verbs in one contiguous dispatch block, each **arity-verified** against the handler rather than
trusted from the index: `seteventpartymode` `0x050F` (1 arg), `geteventpartymode` `0x0510` (0),
`geteventpartymodebit` `0x0513` (0), `seteventparty2mode` `0x0514` (1), `geteventparty2mode` `0x0515`
(0), `geteventparty2modebit` `0x0516` (0). The `set…` handlers contain exactly one
`VMValueStack_PopInt32CoerceFloat32`; the `…bit` handlers exactly one `VMResult_WriteInt32`.

**Bits 0 and 1 have verbs too** — `summonread`, `summontopartyread`, `btlAtelSetSummonMode`,
`ridechocobo`, `getoffchocobo`, `setchocobomode` — reached through thunks.

> **`geteventpartymode` and its `…bit` sibling can disagree, and only in one direction.** The mode
> getter returns `ladder() == 4`, so it is **0 while bit 3 is also set**, because 5 outranks 4. The
> bit getter returns the raw bit. `geteventparty2mode` and its bit variant can never differ, since
> nothing outranks 5.

**Authored:** the field record's bit 15, one per area. No script sets it.

## 9. Determinism

No RNG, no timing, no allocation, no thread interaction. The ladder is a pure function of two
globals — which is exactly why it is a good reconstruction target and a poor live-observation
target: **nothing about it varies, so a capture that shows mode 2 shows only that bit 1 was set.**

## 10. Failure paths and edge conditions

| # | condition | result |
|---:|---|---|
| 1 | `*(0x02EBF190)` is null | **faults.** `0030D9AB` dereferences it with no test |
| 2 | the field-record table `*(0x02ADD100)` is null | handled: `00377C33` jumps to `00377C5F`, which computes `0xFFF >> 15` = **0**. The constant is written as a shift rather than as a zero |
| 3 | the active field index is at or past the table's count (`+0x04`) | the same path, the same 0 — an **unsigned** compare at `00377C39`, so a negative index is also out of range |
| 4 | bits 4–31 of the flags word set | ignored entirely |
| 5 | several bits set at once | the highest wins, silently. There is no way for a consumer to learn that a lower condition also held |
| 6 | a setter called with the value the bit already has | writes nothing — including, for bit 1, none of the side effects in §7 |

> **Row 2 is worth keeping as written.** `mov edx, 0xfff / shr edx, 0xf` is a compiler's way of
> saying zero, and a reader who rewrites it as `return 0` is right about the value and has thrown
> away the evidence that this is the *table-absent* path and not a fifth mode.

## 11. Observable behaviour

In memory: `state + 0x5B04`'s low nibble, and `state + 0x5AE4` holding `180.0f` during a chocobo
ride. In play: control suppression that does or does not bite as the leader falls; input
arbitration; a cutscene taking the party; an area where none of it applies. In a save: the flags
word at `rec + 0x28` of the transition record, which is where the mode is when the game is not
running.

## 12. Reproduction formula

```c
uint32_t BattleRuntime_GetMode(void)
{
    uint32_t flags = *(uint32_t *)((char *)*(void **)0x02EBF190 + 0x5B04);  /* no null check */
    if (flags & 8) return 5;
    if (flags & 4) return 4;
    if (FieldData_GetActiveFieldRecordBit15()) return 3;
    if (flags & 2) return 2;
    return flags & 1;
}

int FieldData_GetActiveFieldRecordBit15(void)
{
    int      idx = call_003148F0();                   /* the active field index; body not read */
    uint8_t *tbl = *(uint8_t **)0x02ADD100;
    if (!tbl || (uint32_t)idx >= *(uint32_t *)(tbl + 4)) return 0;   /* written as 0xFFF >> 15 */
    uint8_t *row = tbl + 8 + (size_t)idx * 3;         /* data at +8, THREE bytes per row */
    return (((uint32_t)row[1] << 8) + row[0]) >> 15;  /* a LE u16 at the row's own +0 */
}
```

**The stride is 3 and the table's data starts at `+8`**, and both come out of one addressing idiom
rather than from a layout document. `00377C3B movsxd rcx, eax` sign-extends the index;
`00377C3E lea rax, [r8 + rcx*2]` makes `tbl + 2·idx`; `00377C42 movzx edx, byte [rcx + rax + 9]`
adds `rcx` **a second time**, giving `tbl + 3·idx + 9`. Split that as `(tbl + 8) + 3·idx + 1` and
the shape appears: an 8-byte header whose `+0x04` is the count, then 3-byte rows, with the flag as
bit 15 of the row's first two bytes — `00377C50 shl edx,8` / `add edx,ecx` / `shr edx,0xf`.

> **Written as `tbl + 3·idx` with fields at `+8` and `+9` the arithmetic is identical and the
> layout is wrong**, because rows three bytes apart cannot each own a byte at `+8`. This is the
> same `*2`-plus-`*1` idiom the manager-slot tables use to express 24 as `*3` then `*8`, and the
> same way to misread it.

## 13. Runtime validation

**Evidence class: isolated original-code. Live capture: still absent, and that is the gate this
subsystem fails.**

**Executed 2026-09-12** by [`diff_battle_mode.py`](../../../../Reconstruction/Tests/Differential/diff_battle_mode.py)
against [`battle_mode.c`](../../../../Reconstruction/Game/Core/battle_mode.c) — the thirty-fourth
pilot, and the one this contract's own §13 designed. **55 comparisons, 0 mismatches** against the
shipped bytes at their real virtual addresses under Unicorn.

| what ran | cases |
|---|---:|
| the ladder `0030D9A0`, all 16 flag nibbles × both callee answers | 32 |
| the ladder with bits 4–31 set and a zero nibble, and with every bit set | 10 |
| the predicate `00377C20` over real bytes: bit 15 set and clear at three in-range indices | 6 |
| the predicate at `index == count`, `count + 1`, `-1`, a null slot, a null-and-empty slot, a table with no rows | 7 |

**All six modes are reached** — 0×5, 1×1, 2×2, 3×8, 4×8, 5×18 — and the suite **refuses to report a
pass if fewer than six occur**, because a run that never reaches a mode has not measured the
priority order it claims to. It also refuses if either scripted callee never fires.

**Mutation campaign: 26 points — 18 KILLED, 5 EQUIVALENT, 1 SURVIVED, 2 INVALID. Verdict
`FAIL_INCOMPLETE`,** and both non-kills are adjudicated rather than excused:

- **The survivor is provably equivalent.** `packed = (row[1] << 8) + row[0]` mutated to use
  `row[1]` twice cannot change `packed >> 15`: `row[1] << 8` has bits 0–7 clear and `row[0] ≤ 0xFF`
  occupies only those bits, **so the addition cannot carry into bit 15** and the result is always
  bit 7 of `row[1]`. **That is a fact about the original too** — it computes a full `u16` with
  `shl edx,8 / add edx,ecx` and then uses only the top bit, so **the row's low byte is dead for this
  purpose.**
- **The two INVALIDs are undefined behaviour.** Both mutate `t->bytes == 0` so that a **null** table
  is treated as present; the next statement adds 8 to it. The driver faults, no comparison happens,
  and the instrument records that rather than calling it a kill.

> **One case was written wrong and the campaign caught it**, which is the point of running one.
> `(uint32_t)index >= t->count` mutated to `>` **survived the first run** even though the cases
> drive `index == count` — because the row past the bound was left unseeded, so the mutant read
> zeros and answered `0` exactly as the original does by refusing. The table in memory is larger
> than its declared count, so seeding that row is legitimate, and with it seeded the mutant dies.
> **A case can drive exactly the boundary it was written for and still not depend on it.**

**What this does NOT establish.** ~~The ladder's callee is **scripted** on the ladder side — answered
with 0 or 1 rather than executed — and the predicate is driven separately against its own real
bytes. **A scripted callee is not a proved one**, so what is established is each function, not their
composition.~~ **That residual is discharged — 2026-09-18, §13a.** Nothing here touches the four
setters, the save round trip, or the 21 consumers, and no live capture exists.

### 13a. The composition, executed end to end — 2026-09-18 (OPUS, consuming SWE2-ORACLE's EXP-098)

**The residual this section stated is discharged.** EXP-098 ran `0030D9A0` → `00377C20` → `003148F0`
→ `002EF2B0` → `002EF640` with **zero scripted boundaries**, 19/19 cases and 10/10 mutants killed
across two processes. **The composition behaves as the sum of its proved parts**, which is a result
and not a formality: it is the outcome this contract could not assume.

All eight findings were re-read from the shipping bytes before being accepted here. They hold, and
three of them are sharper in the instructions than in the record.

- **The mode ladder is 105 bytes and tests `cl`, not the dword.** `0030D9B1 test cl, 8` → 5;
  `0030D9C0 test cl, 4` → 4; `0030D9CF call 00377C20`, non-zero → 3; then `0030D9EF test cl, 2` → 2;
  else `0030D9FE movzx eax, cl` / `and eax, 1`. **So finding 8's "high flag bits are ignored" is
  stronger than stated: bits 8 and above are not ignored by a mask, they are never loaded** — every
  test is on the low byte.
- **The re-read is real and it is a re-read of both.** `0030D9E2` reloads the state pointer from the
  same rip-relative slot and `0030D9E9` re-reads `[rax + 0x5B04]`, so the bits `2` and `1` arms see
  flags fetched *after* the predicate call rather than the copy taken before it.
- **The row test is `shr edx, 0xf` at `00377C55`, and the row is three bytes.** `00377C3E lea rax,
  [r8 + rcx*2]` with a further `+rcx` in the operand gives a **3-byte stride** from `+8`; the byte at
  `+9` is shifted left 8 and added to the byte at `+8` (`00377C42`–`00377C53`), and bit 15 of that
  pair is the answer. **A reimplementation that reads a `u16` at a 2-byte stride gets the right
  answer for row 0 and the wrong one for every other row.**
- **The refusal arm builds its zero the long way.** `00377C5F mov edx, 0xfff` / `shr edx, 0xf` — a
  null table or an out-of-range index answers 0 through the same shift rather than by a separate
  path, which is why the callee has exactly one return value shape.
- **The negative-index clamp is in `003148F0`, not in the ladder.** `00314901 test eax, eax` /
  `00314903 cmovs eax, ecx` with `ecx` zeroed at `003148F9`, so an index of `-1` reads **row 0**
  rather than refusing. `m-cmovs` leaves it unclamped and the unsigned `jae` at `00377C39` then
  refuses — the two behaviours differ, and only the first is the shipped one.

**What is still not established, and it is unchanged:** ~~the four setters, the save round trip,~~ the 21
consumers, and every live-only item in the paragraph above. EXP-098 discloses the mode setters as not
exercised, and this contract does not promote them.

**The setters, the reset, the getters and the save round trip are executed since (2026-09-26, OPUS,
`candidates/s03-opus-replay-mode-setters/`, NATIVE-REPLAY, no application stub, 10/10, identical ×2):** the ladder over all 16
low-nibble values with bits 4–31 set and clear (invariants 1/2); the bit-3/bit-2 setters (one write, none when equal); the bit-0
setter (one write, then the tail call to `0035C620`, a recorded boundary); the chocobo setter §7 (enable: flags `|= 2`,
`+0x5AE0 |= 0xC`, `+0x5AE4 = 180.0f`, nothing else; disable: flags `&= ~2`, `002E73C0(slot-3 actor, 3)`, `+0x5AEC = 0`; the
`002EB030` post was not reached — roster slot 3 is empty in this world); the reset (`+0x5B04` and `+0x5B08`); the bit and
mode getters; and the save pair (§3 above, corrected).

**Also executed (2026-09-26, OPUS), in the same directory with no application stub:**
- **`c7.py`, 4/4: §7's disable arm.** With `+0x5AE0` bit 1 set and roster slot 3 filled, the setter calls
  `002E73C0(actor3, 3)` and then `00329A10` → `002EB030(actor3, 0x2001)`. It clears `+0x5AE0` bit 1 and keeps the
  word's other bits.
  - With slot 3 empty, there is no post, but bit 1 is still cleared: the toggle lies outside the actor test.
  - With bit 1 clear, there is neither a post nor a change.
  - The test uses the value read at `00303E03`, before the roster calls. The toggle is an XOR on the current word
    (`00303E55`–`00303E71`).
- **`m45.py`, 3/3: §6's "modes 4 and 5 differ in exactly one place".** `003266C0` under ladder 4 rewrites tables
  `+0x5A5A`, `+0x5A6C` and `+0x5A90` to the leader alone, at the leader's position. Under ladder 5 it writes the first
  two identically and restores `+0x5A90` to its prior content. `+0x5A7E` holds the base nine in both. **The two runs
  differ in `+0x5A90` only.**
- **`consumers.py`, 3/3: invariant 1's mechanism** on `0023B040`, the consumer the pre-emption drives.
  - With ladder 2, `00303EC0` returns 1 and the leader-derived path (`003272A0` onward) never runs.
  - With the chocobo bit still set under a higher condition (ladders 4 and 5), `00303EC0` returns 0 and that path runs.
  - This world has no leader, so the emitted values coincide; the cases show the path.

*One reading note, the same convention as EXP-093's: the mutant table's `0x30D9B3`, `0x30D9B7`,
`0x30D9C2`, `0x30DA03` and `0x377C57` are **immediate bytes**, not instruction boundaries — the
instructions are at `0x30D9B1`, `0x30D9B6`, `0x30D9C0`, `0x30DA01` and `0x377C55`. Correct for a
byte-patching harness to name; a trap for anyone who disassembles there.*

**The live half, queued with the state it needs:** read `state + 0x5B04` while riding a chocobo and
confirm bit 1; read it during a cutscene and confirm bit 2 or 3; read `state + 0x5AE4` on mounting
and confirm `180.0f`. **One attach answers all three, and none has been performed.**

Receipts: `Database/Tools/work/OPUS/litsuffix/battle_mode` and `battle_mode2` (ignored path).

## 14. Unresolved

*Renumbered 2026-09-14 (FABLE, `OPUS-REQ-FABLE-QUESTION-ID-INTEGRITY`): these ids were `BM-1`…`BM-3`, which the question register already uses for different questions (PhyreEngine animation-channel questions). The register keeps its ids; this list moved, and the rows are registered under the new ids.*

1. ~~**`RMD-1`** — which of entry 3's readers an event script actually relies on, which is what makes
   mode 4 and mode 5 different in play rather than in the slot map. `0031B950`,
   `BattleSlotMap_ResolveMappedBattleSlot` and five more read it; none is read.~~
   **ANSWERED 2026-09-22 (SWE2-CONTRACT) — the reader is the party-read-in state machine
   `0037B4D0`, reached from the `partyallread` / `partyallread2` / `summonread` verb tasks.**
   Entry 3 is the class-4 map at `+0x5A90` (nine u16). Its full reader set, re-censused by
   displacement (`+0x5A90`, 8 sites): the resolver arm `0031BA3D` in `0031B9F0` (edx=4 — **no
   literal class-4 call site exists**; every one of the 31 resolver sites passes 0–3 or a
   register), the sibling resolver `0031B950` (`0031B981`, reached only from the mode-2
   pair-1 hooks `0031B950`'s callers `00304060`/`00304140` — `call rax` slots 10/11 of the
   `01EECFC0` hook table fired by the mode-change dispatcher `0030D8B0`), the writer-side
   compare `00326916` inside ~~`003266DB`~~ the refresher `003266C0`'s mode-3 arm (`003266DB` is an unwind-fragment
   boundary inside it, `CON-170`), the init write `00329E20`, and the three consumers
   below.
   - **`0037B4D0` reads entry 3 at 14 sites** — `0031C250` ×4 (`0037B59F`, `0037B824`,
     `0037BD75`, `0037BDDC`), `0031BEC0`→`0031C0F0` ×9, `00320170`→`00320230` ×1
     (`0037BC29`). `0031C250(rdi=actor)` scans slots 0–3 through `00263750`, and on the slot
     holding the actor returns `byte[state + slot*2 + 0x5A90]` (`0031C2C7`) — the class-4
     mapped row for that actor's slot, `0xFFFF` on `0xFF`. The machine uses it to resolve
     which definition row a slot's actor reads in as.
   - **Verb reachability** (all documented in the party-read page, re-verified in the call
     graph): `partyallread` `0x3EB` begin `0034CCD0` → `0037C980`, `partyallread2` `0x46F`
     begin `0034D8B0` → `0037CA00`, `summonread` `0x203` result `0034E1F0` → `0037CA80`;
     all three install the `0037C730` task that walks slots through `0037B4D0` — and the
     same task calls `00233AA0`, the ordered toggle that runs `0030D8B0(1)`. The reconcile
     path (`PartyConfiguration_SetSelectorsAndReconcileRoster` `003273D0` → `0037CA80`) and
     `0037C1A0` reach the machine without a verb.
   - **The in-play difference:** after `seteventpartymode` (mode 4), `003266C0` rewrote
     `+0x5A90` so the class-4 resolutions the read-in machine makes return the leader's row
     for the slots it touches — the read-in resolves to the leader where the map was
     rewritten. After `seteventparty2mode` (mode 5), the same verbs run but `+0x5A90` was
     restored on entry, so the machine resolves each slot's own actor — the party's
     presentation set survives while maps 1–2 still point at the leader.
   - Secondary consumers, not verb-driven: `0035A490`/`0035AD40` (init/unload rebuilds ←
     `0025AFC0`/`00261F90`/`002628B0`) read it via `0031C470`, `00320230`, `0031C0E0`×4.
   - **Residual:** the 14 read sites each feed a different machine state; which specific
     visible outcome each drives (guest slot hidden vs leader duplicated) is inferred from
     the map's role, not observed per-site.
2. ~~**`RMD-2`** — whether `*(0x02EBF190)` can be null at any point where a consumer calls the ladder.~~
   §10 row 1 is a fault, not a fallback, and nothing establishes reachability.
   **ANSWERED to the static limit 2026-09-21 (SWE2-CONTRACT) — the null window exists but is
   bounded to pre-boot-transition, and no consumer sits inside it:**
   - `02EBF190` is **BSS** — it lies in the uninitialised gap between `.data` (ends
     `0x1E58000`) and `.pdata` (`0x2E7A000`), so the image supplies `0`. Null is the initial
     state, not a reachable later one.
   - There are **two writers image-wide** (corrected 2026-09-22 — the earlier "exactly one"
     missed the lazy path): `00238A92` inside `00238A80` (unconditional), and `00233C33`
     inside the lazy initializer `00233C10` — `mov rax,[02EBF190]; test; jne skip;
     call 002EF640; add rax,0x4E68C; mov [02EBF190],rax` — which fills the same cell with
     the same value on first use. **Both** store `SaveImage_GetActiveBuffer() + 0x4E68C` —
     i.e. the constant `021B290C`. No store of NULL exists anywhere; once either runs, the
     pointer can never be null again. (The pointee is an interior offset of the save working
     buffer — the same `B = 021B290C` base the bazaar flag/counter block is documented
     against — so the "BattleSystemState block" is save-image-resident, not heap state.)
   - `00238A80` runs only at the **tail of `002EF650`** — the save-image init that memsets the
     payload and applies the authored flag lists (`002EF2D0`→`00379160`). `002EF650` has three
     live call sites: the mode-0 boot frame `0022B6E0` (inside the `0209273C == 5` advance
     block — the boot→mode-1 transition) and `00280140` (`0028037B`); the `003941E5`/
     `003942F2` sites sit in a fully orphaned body. The lazy `00233C10` has four callers —
     `00280140` (`002803B8`, *after* its own `002EF650`), `00285E60`, `0036FCC0`, `00394130`
     — and is **not** among `0022B6E0`'s pre-init calls.
   - The ladder `0030D9A0` has **~~20~~ 22 call sites, all in the `0x2FF…0x326` battle cluster** *(corrected 2026-10-02, OPUS: 22 direct `call` sites in 21 functions, `00326500` twice)* —
     none inside the mode-0 frame's fixed call list. For a null fault, a consumer would have
     to run before the boot transition completes.
   - **CLOSED 2026-09-22 (SWE2-CONTRACT) — no consumer can call the ladder while the pointer
     is null.** The residual above is resolved by the master-state dispatch, not just by
     reachability:
     - `0022A580` is the per-frame master tick; `0022A685` jump-table-dispatches on
       `byte[02064AD3]` (0–6, default→`0022A770`). State 0's arm is exactly `0022B6E0`.
       Every non-zero writer of `02064AD3` sits inside a state arm (1–5 or >6) or is
       `0022B74E` in the boot frame itself — `0022A1A0` only resets it to 0.
     - `0022B74E mov byte [02064AD3],1` is the **first instruction of the `0209273C==5`
       block**, 15 instructions before `call 002EF650` (`0022B78B`) — leaving state 0 is
       impossible without executing the init in the same tick. The 7 intervening calls are
       inside the verified-clean pre-init set below.
     - Reader census re-derived fresh: **131** reader functions (the row below's "125" was
       stale). Cut-closures over the E8/E9 call graph: PE entry `00808EE4` with the tick
       cut → 621 functions, **0 readers, 0 ladder callers**; `0022B6E0`'s 17 pre-init calls
       → 1,482-function closure, **0 readers**; `00394130`'s 5 pre-init calls → 53
       functions, 0 readers (moot — see next bullet).
     - `00394130` is **fully orphaned** — zero callers, zero stored pointers, zero `lea`
       materializations image-wide. Its two `002EF650` sites are dead code.
     - `00280140`'s 30 pre-init calls reach **6 readers including the ladder itself**
       (e.g. `002801C4→…→00303EC0→0030D9A0`) — a genuine static pre-init path. It is
       temporally excluded: `00280140` is a message-`0xD8` handler registered by
       `00244F50` from `00280A00` (`lea` at `00280A85`), reached only via
       `00254B50 ← 00253C50/00254B40/002E09A0 ← 00314020 ←` state arms `0022B8C0` (~~2~~ 3),
       `0022BC20` (~~3~~ 5), `0022A770` (2 and >6) *(corrected 2026-10-02, OPUS: the seven-entry table `0022A580+0x119` reads sends 2 and anything above 6 to `0022A770`, 3 to `0022B8C0` and 5 to `0022BC20`)* — **all post-state-0**, so the handler cannot even
       be registered while `02064AD3==0`, and registration precedes dispatch.
     - **Residual (honest boundary):** the proof covers the single-threaded frame
       sequence. Worker threads exist (the boot frame itself spin-waits on `02EBA3F8`
       at `0022B720`); a thread-entry-point census against the 20 ladder call sites was
       not enumerated. All 20 sites are battle-cluster frame work, so a threaded caller
       would itself have to be state-gated battle code — expected impossible, not proven.
3. ~~**`RMD-3`** — what `FUN_002E73C0(actor3, 3)` does to the guest slot when the chocobo bit clears.~~
   **ANSWERED 2026-09-15 (OPUS) — it does nothing to the guest slot, because it writes nothing at all.**
   All **65 bytes** were read end to end and the body contains **zero store instructions**. The mnemonic
   census is 4 `je`, 3 `cmp`, 2 `test`, 1 each of `ret`, `movzx`, `movsx`, `mov` (a load), `jne`, `jl`,
   `imul`, `add` — nothing writes memory. It is a **guard chain ending in a conditional tail call**:
   
   ```asm
   002E73C0  test rcx, rcx                  ; no actor          -> ret
   002E73C5  mov  rax, [rcx + 0xC0]         ; no render record  -> ret
   002E73D1  cmp  dword [rax], 0 / jl       ; negative          -> ret
   002E73D6  movzx ecx, word [rax] / cmp -1 ; index 0xFFFF      -> ret
   002E73E3  imul rcx, rax, 0x740           ; index * stride
   002E73EA  add  rcx, [022C6F28]           ; + array base      -> ret if zero
   002E73F3  cmp  dword [rcx + 0x284], 0
   002E73FA  jne  0x3E6AA0                  ; TAIL CALL, not a call
   002E7400  ret
   ```
   
   The `0x740` stride and the base `022C6F28` are the **160-record Presentation array** already
   documented under `K-10`, so this resolves the actor's render record in that array and hands off.
   **Any effect on the slot belongs to `003E6AA0`**, which the ladder page already reads as a
   presentation request of sub-resource 3 on the mount's render object — and it is reached only when
   `[record + 0x284]` is non-zero, which is the gate this question's "when the chocobo bit clears"
   phrasing was reaching for.
   
   *Not claimed:* what `[record + 0x284]` is. It gates the hand-off and is read nowhere here.

## 15. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| the ladder's six tests, their order, and the two early returns | **re-read from the image 2026-09-12**: `0030D9A0`–`0030D9E9`, `test cl,8` / `test cl,4` / `call 00377C20` / `test cl,2` / `and eax,1`. Agrees with the page's C exactly | 1 | PROVEN  **§15a: the ORDER is exact; the two counts are not.** The body holds **four `test` instructions** and **five decision points** (the fifth is `0030DA01 and eax, 1`), with **four** early returns. **Six is the number of MODES**, 0–5 — and *two* is the number of returns taken **before** the `call 00377C20`, which is the reading that holds |
| the flags word is `*(0x02EBF190) + 0x5B04` | `0030D9A4` `mov rax,[rip→02EBF190]`, `0030D9AB` `mov ecx,[rax+0x5B04]`, and the same pair again at `0030D9E2` | 1 | PROVEN |
| the ladder does not null-check the state pointer | there is no `test rax,rax` between the load `0030D9A4` and the use `0030D9AB` (same shape at `0030D9E2`/`0030D9E9`) | 1 | PROVEN |
| the table-absent path returns 0, written as `0xFFF >> 15` | **re-read 2026-09-12**: `00377C5F mov edx,0xfff` / `shr edx,0xf` | 1 | PROVEN |
| the bound is unsigned, the row stride is 3, and the data starts at `+8` | `00377C39 jae` against `[r8+4]`; `00377C3E lea rax,[r8+rcx*2]` then `00377C42 movzx edx,[rcx+rax+9]` adds `rcx` twice, giving `tbl + 3·idx + 9` = `(tbl+8) + 3·idx + 1`; the flag is `shl 8` / `add` / `shr 0xf` over that row's two bytes | 1 | PROVEN |
| bit 0 is the summon and bit 1 the chocobo | the page's §2b/§2c, from the verbs and their setters. **Not re-derived here**, and the page's own hierarchy diagram still disagrees — `OPUS-CONTRA-LADDER-LABELS` | 1 | PROVEN |
| modes 4 and 5 are script-set and reachable only through thunks | the page's §2b thunk chains, with the corrected caller census | 1 | PROVEN |
| the six verbs and their arities | the dispatch table (`00914794` is the `0x050F` entry) plus a handler-side arity check — the lone `00267E10` call at `00351B47`/`00351E57` in the two `set…` handlers | 1 | PROVEN |
| `geteventpartymode` returns `ladder() == 4`, so it is 0 while bit 3 is set | the page's §7, from `003072C0` / `00307280` | 1 | PROVEN |
| the mode survives a transition and a save | `002EF3C0` writes `+0x5B04` to `rec+0x28`; `002EF410` restores | 1 | PROVEN |
| the chocobo setter's asymmetric side effects | the page's §"Bit 1 has a getter and a setter" | 1 | PROVEN |
| mode 4 writes slot-map entries 0, 1 and 3 and mode 5 restores entry 3 | the page's §7, from `003266C0` at `00326756`–`003268EE` | 1 | PROVEN |
| `*(0x02EBF190)` can be null only before the first save-image init — the slot is BSS-zero, the two writers `00238A92` (unconditional, `002EF650` tail) and `00233C33` (lazy fill in `00233C10`) both store the constant `021B290C` (`SaveImage_GetActiveBuffer()+0x4E68C`), and **no consumer can call the ladder while it is null**: the master tick `0022A580` dispatches on `byte[02064AD3]`, state 0 is exactly the boot frame `0022B6E0`, and the state-0 exit write `0022B74E` is the first instruction of the `0209273C==5` block that ends with `call 002EF650` (`0022B78B`) — leaving state 0 requires running the init in the same tick | rip-rel census over `.text`: **131** reader functions, two stores (`00238A92`, `00233C33`); `002EF650` called from `0022B78B` and `0028037B` (the `003941E5`/`003942F2` sites are in a fully orphaned body). Cut-closures 2026-09-22: PE entry with tick cut → 621 fns, 0 readers; `0022B6E0` pre-init → 1,482 fns, 0 readers; `00280140` pre-init → 1,827 fns, 6 readers incl. the ladder, but `00280140` is message-`0xD8` handler registered only via `00314020` ← state arms {2,3,>6} — unregistrable during the null window. Residual: thread-entry census not enumerated | 1 (static) | PROVEN (single-threaded frame sequence; thread-side bounded but unenumerated) |
| any execution of this operation, isolated or live | **none**; §13 | none | UNKNOWN |
| which entry-3 reader an event script relies on | the party-read-in machine `0037B4D0`, at 14 sites via `0031C250`/`0031BEC0`/`00320170` — installed by `partyallread` `0x3EB`, `partyallread2` `0x46F`, `summonread` `0x203` through `0037C980`/`0037CA00`/`0037CA80` → `0037C730`; mode 4's `+0x5A90` rewrite makes the machine's slot→row resolutions return the leader, mode 5's restore preserves them — §14 item 1, 2026-09-22 | 1 (static) | PROVEN (per-site visible outcome inferred, not observed) |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

### Corrected: six is the number of modes, not of tests

`0030D9A0` is 105 bytes and reads whole as a **priority cascade with five decision points**, not six
tests:

| # | decision | yields |
|---|---|---|
| 1 | `0030D9B1 test cl, 8` | **5** |
| 2 | `0030D9C0 test cl, 4` | **4** |
| 3 | `0030D9CF call 00377C20` / `0030D9D4 test eax, eax` | **3** |
| 4 | `0030D9EF test cl, 2` | **2** |
| 5 | `0030D9FE movzx eax, cl` / `0030DA01 **and eax, 1**` | **1 or 0** |

**Four `test` instructions; the fifth decision is an `and`.** Six is the count of *outcomes* — modes
0 through 5 — and §2's "6 tests" reads the result column as though it were the test column. A
reconstruction implementing "six tests" adds a branch the engine does not have.

**"Two early returns" is four**, unless it means *"two that return before the `call`"* — which is
true and is the useful distinction, since modes 5 and 4 are decided without ever consulting the field
bit. The row now says which.

### Confirmed exactly

| claim | image |
|---|---|
| the flags word is `*(02EBF190) + 0x5B04` | `0030D9A4 mov rax, [rip → 02EBF190]` / `0030D9AB mov ecx, [rax+0x5B04]` — **and the identical pair again at `0030D9E2`/`0030D9E9`**, so the word is re-read after the call rather than cached |
| **the ladder does not null-check the state pointer** | both loads are followed **immediately** by the dereference, nothing between |
| the table-absent path is `0xFFF >> 15` | `00377C5F mov edx, 0xfff` / `00377C64 shr edx, 0xf` |
| the bound is unsigned, stride 3, data at `+8` | `00377C39 **jae**`, then `00377C3B movsxd rcx, eax` / `00377C3E lea rax, [r8 + rcx*2]` |

> **A trap I walked into and backed out of.** My first detector flagged `0030D9D4 test eax, eax` as a
> null check and made the "no null-check" claim look false. It is not a pointer test at all — it
> tests **the return value of `call 00377C20`**. The claim is about the state pointer from
> `02EBF190`, and *that* is never tested. **A register name is not a value's identity**, which is the
> same lesson as `r8` ceasing to be the third argument two contracts ago.

The `0xFFF >> 15` here is the same failure value the [field record
accessors](../../03-World-Area-Field/CONTRACT-field-record-accessors.md) pass established as
*"permission denied"* — so **when the field table is absent, this ladder cannot return 3**, and falls
through to the chocobo and summon bits.

**Not claimed:** nothing here is executed or observed live. (`RMD-1` has since been answered —
§14 item 1; the sentence above predates the strike.)

## 16. Parity plan

**Constructed and run, 2026-09-12** — `CALCULATION`, `STRUCTURAL` and `STATE-TRANSITION` are
`COVERED` by `diff_battle_mode.py`, and `EDGE-CASE` with them. §10 row 1 (the unchecked state
pointer) is the one edge **not** driven: it faults the original rather than comparing, which is the
behaviour and not a result.

**The four setters are still not driven**, so `STATE-TRANSITION` covers the ladder's own transitions
and not the writes that cause them — the contract's §7 table is half-tested, and the half that is
tested is the half this pilot claims.

**Not constructible offline, and why:** `TIMING` — nothing here establishes *when* a consumer asks;
`INTEGRATION` — the 21 consumers are the whole point and a fixture that scripts them has not tested
them; `PRESENTATION`; `RNG` and `SERIALIZATION` — none drawn, none parsed, though the save round trip
in §3 would be a `SERIALIZATION` case if the transition record were modelled; `FULL SUBSYSTEM` — no.

**The dimension this contract most wants and cannot have offline is `INTEGRATION`**, because the
ladder's meaning is entirely in its consumers: a number nobody asks for has no behaviour.

## 17. Related

- [`battle-runtime-mode-ladder.md`](battle-runtime-mode-ladder.md) — the mechanism this formalises,
  and the two stale statements routed as `OPUS-CONTRA-LADDER-LABELS` / `OPUS-CONTRA-LADDER-STATUS`.
- [`../../11-Party/party-roster-and-control-suppression.md`](../../11-Party/party-roster-and-control-suppression.md)
  — the consumer whose *"per-area waivable"* behaviour is this ladder's priority pre-emption.
- [`../../11-Party/Battle-State-Block/the-battle-state-block-field-map.md`](../../11-Party/Battle-State-Block/the-battle-state-block-field-map.md)
  — the block the flags word lives in, and the slot map modes 4 and 5 rewrite.
- [`../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md`](../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md)
  — §8b, where `02EBF190` is established as a state block rather than an authored table.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**ActorEntity — CLIENT (31 edges through 17 of this page's functions).** The ActorEntity layer reaches this page at `0023A570`, `003266C0`, `00311E20`, `0023A3B0` and 13 more. `BattleUnit_ResetStateForReuse` is the worked example, read in full - it is the reuse reset, and it states the unit's sentinels: `word[+0x695]` becomes `0xFFFF`, `byte[+0x694]` becomes `0xFF`, `dword[+4]` is masked with `0xFFEFFFBB`, and the `+0xBC0` candidate block is cleared; **12 of the 20 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatAI — CLIENT.** `AiOrder_EvaluateAndResolveActionTarget`, owned by that layer, calls `00377C20` on this page. That caller is the order evaluation: a `0xAB8`-byte frame with a stack cookie that writes a resolved id into the caller's word - `0xFFFF` for none - and refuses entirely while `byte[02089340] & 0x20` is set; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatFormula — SERVICE.** `0023A570` on this page calls `BattleStats_InitializeDefinitionRecord`, owned by that layer. What it reaches is the `0x1C8`-byte record initialiser, and it states the sentinels: `qword[+0x50]` becomes `-1`, `word[+0x58]` and `word[+0x1C3]` become `0xFFFF` and `byte[+0x1C5]` becomes `0xFF`, after which the definition id's **high byte** selects which authored table its low byte indexes; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Gameplay — SERVICE and CLIENT.** `0031C2F0`'s class-0 lane gates on `00322C50` (`BattleEncodedId_IsValidForClass`), a gameplay-domain predicate that the same layer's `0031B9F0`/`0031C5D0` also call — the page consults the layer's validity check, the layer drives it; not a shared responsibility.

**Party — CLIENT.** `00322C50`, cited here as `0031C2F0`'s class-0 gate, is called across the party layer (`00326500`, `0031B510`, `00321100`, `00329080`, `003170E0`, `0031AC00`, `00320800`, `00328DB0`, `003287A0`).

**Status — CLIENT.** The status layer's `00310DB0`, `0030E130` and `0030FED0` call `00322C50` — the same predicate, reached from that layer's bodies.

**UI — CLIENT.** `0031EB20` on the UI layer calls `00322C50`.
- **Audio — CLIENT and SERVICE (15 edges).** 4 inbound (Audio bodies `00261F90` call page-cited `SaveImage_GetPersistentPayloadBase` (002EF2B0), `WorldTransition_GetActiveOrPendingFieldId` (003148F0), `0035A490`); 11 outbound (page-cited `00261F90`, `002628B0`, `World_UpdateSimulationTick` (00314020) call Audio bodies `0036F460`, `00360D30`, `002DEE50`). Substantive edges include `0022A770` calls `0036F460`; `00261F90` calls `00360D30`; `00261F90` calls `002DEE50`; `00261F90` calls `00361170`; the remaining edges run through shared helpers the page cites.
- **Input — CLIENT and SERVICE (51 edges).** 7 inbound (Input bodies `InputGameplay_ArbitrateDigitalInputAndModalState` (00253C70), `002E09A0`, `00226BE0` call page-cited `00254B50`, `PartyRoster_GetActorBySlot` (00263750), `00303EC0`); 44 outbound (page-cited `0022A770`, `MainLoop_UpdateAndRenderFrame` (0022B8C0), `0022BC20` call Input bodies `InputControl_SetOneShotFrameCallback` (0035E9A0), `InputGameplay_RebuildFrameSnapshotFromChannelHistory` (002498B0), `0017DE60`). Substantive edges include `0022A580` calls `InputControl_QueueWorkerDeadlineAndMarkDirty` (0035E9B0); `0022A580` calls `00360080`; `0022A770` calls `InputControl_SetOneShotFrameCallback` (0035E9A0); `0022A770` calls `InputGameplay_GetRemappedHistoryMask04` (0036FF70); the remaining edges run through shared helpers the page cites.
- **InputGameplay — CLIENT and SERVICE (2 edges).** 1 inbound (InputGameplay bodies `00313A00` call page-cited `FieldData_GetActiveFieldRecordBit15` (00377C20)); 1 outbound (page-cited `00313DB0` call InputGameplay bodies `00313A00`). Substantive edges include `00313DB0` calls `00313A00`; `FieldData_GetActiveFieldRecordBit15` (00377C20) is called by `00313A00`.
- **Presentation — CLIENT and SERVICE (55 edges).** 12 inbound (Presentation bodies `BattleUnit_ComputePresentationSuppressionMask` (003125E0), `003C4070`, `002BAF80` call page-cited `FieldData_GetActiveFieldRecordBit15` (00377C20), `003E6AA0`, `WorldTransition_GetActiveOrPendingFieldId` (003148F0)); 43 outbound (page-cited `0022A770`, `MainLoop_UpdateAndRenderFrame` (0022B8C0), `0022BC20` call Presentation bodies `002E65A0`, `GraphicsSync_WaitBackendState100ClearAndResetSharedState` (0036F2F0), `GraphicsSync_ClearSharedCommandStateBits` (0036F2C0)). Substantive edges include `0022A770` calls `00376470`; `0022A770` calls `002E65A0`; `0022A770` calls `001EC560`; `0022A770` calls `0037D4C0`; the remaining edges run through shared helpers the page cites.
- **RNG_Random_Selection — MECHANICAL (1 edge).** 1 call from page-cited bodies into shared RNG_Random_Selection plumbing (`RNG_MT19937_NextU32_Thunk` (00379CD0)) - the helpers' general call surface, not a RNG_Random_Selection relationship of this page's subjects.
- **Resource — SERVICE (6 edges).** 6 outbound (page-cited `0022A770`, `0022B6E0`, `MainLoop_UpdateAndRenderFrame` (0022B8C0) call Resource bodies `00324510`, `0032E520`, `0032E4D0`). Substantive edges include `0022A770` calls `00324510`; `0022B6E0` calls `0032E520`; `MainLoop_UpdateAndRenderFrame` (0022B8C0) calls `00324510`; `0022BC20` calls `00324510`.
- **SaveLoad — CLIENT (4 edges).** 4 inbound (SaveLoad bodies `00280140` call page-cited `00233C10`, `SaveImage_GetPersistentPayloadBase` (002EF2B0), `SaveImage_GetActiveRuntimeBuffer` (002EF640)). Substantive edges include `00233C10` is called by `00280140`; `SaveRuntime_ResetActiveImageAndRebindState` (002EF650) is called by `00280140`; the remaining edges run through shared helpers the page cites.
- **Save_Load_Settings — CLIENT and SERVICE (42 edges).** 24 inbound (Save_Load_Settings bodies `SaveRuntime_ResetActiveImageAndRebindState` (002EF650), `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` (00584210), `SaveImage_FinalizeHeaderAndChecksum` (00583D60) call page-cited `SaveImage_GetActiveRuntimeBuffer` (002EF640), `SaveRuntime_RebindImageBackedGameplayState` (00238A80), `00285E60`); 18 outbound (page-cited `00280140`, `SaveRuntime_ResetActiveImageAndRebindState` (002EF650), `00394130` call Save_Load_Settings bodies `SaveImage_GetActiveRuntimeBuffer` (002EF640), `SaveImage_GetPersistentPayloadBase` (002EF2B0), `SaveRuntime_ResetActiveImageAndRebindState` (002EF650)). Substantive edges include `0022B6E0` calls `SaveRuntime_ResetActiveImageAndRebindState` (002EF650); `SaveRuntime_RebindImageBackedGameplayState` (00238A80) is called by `SaveRuntime_ResetActiveImageAndRebindState` (002EF650); `00280140` calls `SaveRuntime_ResetActiveImageAndRebindState` (002EF650); `00280140` calls `SaveImage_ValidateRuntimeFormatHeader` (00255260); the remaining edges run through shared helpers the page cites.
- **Script_VM_Native_Bridge — CLIENT and SERVICE (48 edges).** 46 inbound (Script_VM_Native_Bridge bodies `00352FA0`, `00344740`, `003537D0` call page-cited `PartyRoster_GetActorBySlot` (00263750), `BattleStats_GetByMappedBattleSlot` (00320AB0), `FieldData_GetActiveFieldRecordBit15` (00377C20)); 2 outbound (page-cited `00351B40`, `00351E50` call Script_VM_Native_Bridge bodies `VMValueStack_PopInt32CoerceFloat32` (00267E10)). Substantive edges include `Spawn_ApplyScriptSelectedUnit` (0023A3B0) is called by `VM_Spawn_ApplySelectedUnit` (00510160); `PartyRoster_GetActorBySlot` (00263750) is called by `00342250`; `PartyRoster_GetActorBySlot` (00263750) is called by `00350050`; `PartyRoster_GetActorBySlot` (00263750) is called by `00352FA0`; the remaining edges run through shared helpers the page cites.
- **Story_Event_Quest_Hunt — CLIENT and SERVICE (15 edges).** 12 inbound (Story_Event_Quest_Hunt bodies `PersistentFlag_QueryBank64B` (0032AA00), `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` (0032A8A0), `PersistentFlag_QueryBank64A` (0032A9A0) call page-cited `SaveImage_GetPersistentPayloadBase` (002EF2B0)); 3 outbound (page-cited `InputGameplay_ArbitrateDigitalInputAndModalState` (00253C70), `002EF2D0`, `PersistentFlag_ApplyAuthoredInitialPrimarySet` (00379160) call Story_Event_Quest_Hunt bodies `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` (0032A8A0), `PersistentFlag_ApplyAuthoredInitialPrimarySet` (00379160), `PersistentFlag_SetPrimary` (0032AB60)). Substantive edges include `002EF2D0` calls `PersistentFlag_ApplyAuthoredInitialPrimarySet` (00379160); `PersistentFlag_ApplyAuthoredInitialPrimarySet` (00379160) calls `PersistentFlag_SetPrimary` (0032AB60); the remaining edges run through shared helpers the page cites.
- **World — CLIENT and SERVICE (2 edges).** 1 inbound (World bodies `00266D10` call page-cited `002EF2D0`); 1 outbound (page-cited `World_UpdateSimulationTick` (00314020) call World bodies `002623A0`). Substantive edges include `002EF2D0` is called by `00266D10`; `World_UpdateSimulationTick` (00314020) calls `002623A0`.
- **WorldAreaField — CLIENT and SERVICE (88 edges).** 48 inbound (WorldAreaField bodies `World_UpdateSimulationTick` (00314020), `BattleSystem_RunFieldFrameOrchestrator` (00234590), `BattleSystem_InitializeAreaState` (002342F0) call page-cited `SaveImage_GetPersistentPayloadBase` (002EF2B0), `WorldTransition_GetActiveOrPendingFieldId` (003148F0), `SaveImage_GetActiveRuntimeBuffer` (002EF640)); 40 outbound (page-cited `00394130`, `InputGameplay_ArbitrateDigitalInputAndModalState` (00253C70), `002628B0` call WorldAreaField bodies `FieldData_GetActiveFieldRecordBit15` (00377C20), `WorldTransition_GetActiveOrPendingFieldId` (003148F0), `FieldData_GetActiveFieldRecordBit15` (00313F60)). Substantive edges include `0022A770` calls `World_UpdateSimulationTick` (00314020); `0022B6E0` calls `003318C0`; `MainLoop_UpdateAndRenderFrame` (0022B8C0) calls `World_UpdateSimulationTick` (00314020); `0022BC20` calls `World_UpdateSimulationTick` (00314020); the remaining edges run through shared helpers the page cites.
- **Script_VM_Native_Bridge — CLIENT and SERVICE (48 edges).** 46 inbound (Script_VM_Native_Bridge bodies `00352FA0`, `00344740`, `003537D0` call page-cited `PartyRoster_GetActorBySlot` (00263750), `BattleStats_GetByMappedBattleSlot` (00320AB0), `FieldData_GetActiveFieldRecordBit15` (00377C20)); 2 outbound (page-cited `00351B40`, `00351E50` call Script_VM_Native_Bridge bodies `VMValueStack_PopInt32CoerceFloat32` (00267E10)). Substantive edges include `Spawn_ApplyScriptSelectedUnit` (0023A3B0) is called by `VM_Spawn_ApplySelectedUnit` (00510160); `PartyRoster_GetActorBySlot` (00263750) is called by `00342250`; `PartyRoster_GetActorBySlot` (00263750) is called by `00350050`; `PartyRoster_GetActorBySlot` (00263750) is called by `00352FA0`; the remaining edges run through shared helpers the page cites.
## The `0031B950` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`0031B950` (~103 B) — `movsxd rbx, ecx`; `r8d = 0`, `edx = ebx`, `ecx =
r8 + 0x17` index clamp (`0031B956`/`0031B95E`).

| member | role | interior |
| --- | --- | --- |
| `0031B8E0` | same clamp shape — `ecx = r8 + 2` (`0031B8E9`/`0031B8ED`) | [`0031B8E9`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.


## Interior citation — frontier hub `003135C0` (2026-09-18, SWE2-EC7)

`003135C0` — 24 B, 7 callers; the "mode == 1" predicate on
`BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` (`0030D9A0`). Interior verified:
`call 0030D9A0` at [`003135C4`](../../_index/ADDRESS-INDEX.md), `cmp eax, 1; sete` —
the field/runtime ladder's mode-1 test, one instruction of policy over the shared getter.


### Interior citation — frontier hub `002E73C0` (2026-09-18, SWE2-EC7)

`002E73C0` — 65 B, 6 callers. The context-to-render-record resolve idiom:
`[rcx+0xC0]` null-gate, `dword[rax] < 0` and `word[rax] == -1` sentinel checks,
`imul rcx, rax, 0x740` ([`002E73E3`](../../_index/ADDRESS-INDEX.md)) into the
`0x740`-stride render-record array, and only when the record's `[+0x284]` word is
zero does it tail `003E6AA0`. The consumer never sees a sentinel or an occupied
record.
## SWE2-EC7-45 update (2026-09-19) - `0030FD10`

`0030FD10` (245 B) is an items-side body - `0031A630`/`00320AB0`/`00324380`/`00377C20` (the field-bit callee the page names). Interior anchor `0030FD44` (a `0031A630` call).

## SWE2-EC7-88 update (2026-09-20) - `003BFDF0` count-gated category read measured

`003BFDF0` (29 B) is the two-source count the battle-mode
callers run: `00264790()` supplies the count unless it is
non-positive, where `003148F0()` substitutes; the result then
tails `003C0380` for the category byte the `02B457E0` queries
all consume.
Interior anchor `003BFE08` (the `003C0380` tail).

`0031C2F0` (380 B) is the two-tier `cx`-keyed lookup: `cx == 0xFFFF` returns -1; high byte 0 gates on `00322C50(2, low)` then returns `dword[02EBF130-row + 0x70]`; high byte 1 bounds the low byte against `02EBF120`'s `+4` count, reads its `+8`-stride byte, bounds that against `02EBF150`'s count and returns the `+8`-stride dword - the runtime-mode id resolver the mode contract and ARD loader share.

Interior anchor `0031C354` (function `0031C2F0`).
