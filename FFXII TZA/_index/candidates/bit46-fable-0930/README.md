# Battle-unit flag bit 46: who sets, clears and tests it (FABLE, Claude Opus 5.5, 2026-09-30)

For `DATA-REQ-FABLE-BATTLEUNIT-BIT46-0930`. SWE2-DATA's DD owner read of the capability page named unit bit 46 from the
native command seam's phase table, and asked for a row in the field map's flag table. The row DATA suggested says
phase 10 clears the bit. Read against the code, that clear is conditional, and one arm never clears it at all. So the
row published here differs from the suggestion, and the remaining question is registered as **FF-6**.

## What the code does

- **Set.** `BattleUnit_AdvanceStandardActionState` `00304850`, phase 9: `movabs rax, 0x400000000000` / `or qword ptr [rdi], rax`
  (`00304EF3`–`00304EFD`), for every action.
- **Clear.** The same function, phase 10, and only on the arm where the action definition's `+0x0C` bit 30 is clear
  (`00304F62` `test dword ptr [r15 + 0xc], 0x40000000`, `00304F6A` `je`). Even there it clears only when
  `(dword [unit + 0x690] & 0xA) == 0xA` (`r12 = rcx + 0x690` at `00304886`; `00304F91`–`00304F9A`). `+0x690` is
  `animationEventFlags` on the field map: bit 1 an action-timeline event, bit 3 an actor-timeline event. The clear is
  `movabs rax, 0xffffbfffffffffff` / `and qword ptr [rdi], rax` (`00304F9F`–`00304FA9`).
- **The bit-30 arm** (`00304F62`–`00304F8C`) waits while the special-sequence mode is 5 or 6, then advances the phase
  (`00304F7E` `inc byte ptr [rsi + 4]`) with no write through the unit pointer.
- **Test.** `PartyControl_RecomputeSuppressionFromLeaderBattleState` `0023B040` takes the party leader
  (`BattleUnit_GetPartyLeader` `003272A0`, `0023B084`) and tests its flag qword (`0023B0E6`). If the bit is set,
  `0023B0E9` `cmovne ebx, r14d` makes the result `-1`, the all-suppressed mask the capability page §10 describes.

## What was excluded, and how

[`bit46_writers.py`](bit46_writers.py) → [`.out`](bit46_writers.out), FAILS 0. It sweeps `.text` for every
immediate form that names bit 46: `movabs` of either mask, `bt`/`bts`/`btr`/`btc` with index `0x2E`, and dword
`or`/`and`/`test`/`xor` with `0x4000` / `0xFFFFBFFF`, the high dword of the flag qword. It found three `movabs`
(the set, the clear and the test), no bit-test form, and three high-dword sites.

- The three high-dword sites are all in `00239960`, and all address `[02EBF190] + 4`. That is the battle-state
  block's registry slot, not a unit (check C4).
- The field map's ~~two~~ whole-word writers *(corrected 2026-09-30: the census has seven, per the review's §3; these are the two the field map names)*, `00300EAA` and `00300198`, reload the qword and clear only bit 14
  (`btr ..., 0xe`), so they keep bit 46 (check C5).
- Control C0: the three sites already cited by pages must be found.

[`bit46_regindex.py`](bit46_regindex.py) → [`.out`](bit46_regindex.out), FAILS 0. It covers the register-index form:
`mov r32, 0x2E` followed within 8 instructions by a bit-test or 64-bit shift using that register. There are no
image-wide hits. Its control is a synthetic `mov ecx, 0x2e; mov eax, 1; shl rax, cl`, which the same matcher finds.

## What is left (FF-6)

Neither sweep can see a whole-qword store of a saved or computed value, or a mask loaded from memory. ~~So the only
clear known for a unit whose last action had bit 30 is phase 10 of its next action without bit 30.~~ *(wrong - see the correction below)*

Whether something else clears the bit, for example a snapshot restore, is a static question. ~~It stays with the
field map's owner as **FF-6**, and is not routed to ASTRA.~~ *(FF-6 is answered - see below)*

## Files touched by the package

- `04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md`: a register-mask row for bit 46, and the FF-6 box in §7.
- `07-Combat-Action/Command-And-Action-Seam/native-command-seam.md`: phase 10's "the others clear bit 46" now states
  the `+0x690` condition, and that the bit-30 arm leaves the bit set. This is a narrowing: no text is struck.
- `_index/OPEN-QUESTIONS.md`: row FF-6 (OPEN, static).
- Consumer check: [`consumer-check-0930-bit46.md`](consumer-check-0930-bit46.md).

## Correction (FABLE, 2026-09-30, after SWE2-AUDIT-SEM's REJECT)

[SWE2-AUDIT-SEM's review](../auditsem-review-bit46-0930/REVIEW.md) found the "one clear" claim false.
`bit46_writers.py` tested `movabs` against two exact single-bit masks only, and any and-mask with bit 46 clear
clears the bit. The widened check C7 (every `movabs` mask applied to a qword in memory that changes bit 46) finds
four more clears on the unit. The regression C8 shows the old test misses all four. FAILS 0.

- **The clears:** `00304850` phases 0 and 6 (`00304967`–`00304975`, `00304DDD`–`00304DEB`, mask `0xFFFFBFF75FFFCFFF`), a cancel (`BattleUnit_CancelAndResetCurrentAction` `003105D0`, `0031063F`–`0031064B`, same mask), `00308270` (`003082CB`–`003082DF`, mask `0xFFFFBFFFFFBFFFFF`), and the slot release / allocation memsets (`002342CE`, `002344D2`).
- **FF-6 is ANSWERED statically.** the unit's next standard action clears it in phase 0 and phase 6, and so do a cancel, `00308270` and the slot release / allocation memsets: `00304850` phases 0 and 6 (`00304967`–`00304975`, `00304DDD`–`00304DEB`, mask `0xFFFFBFF75FFFCFFF`), a cancel (`BattleUnit_CancelAndResetCurrentAction` `003105D0`, `0031063F`–`0031064B`, same mask), `00308270` (`003082CB`–`003082DF`, mask `0xFFFFBFFFFFBFFFFF`), and the slot release / allocation memsets (`002342CE`, `002344D2`). So a party leader whose last action had bit 30 keeps the capability recompute's all-suppressed mask (`0023B0E6`–`0023B0E9`) only until one of these runs. A bulk copy of a saved unit image (a snapshot restore) is not excluded; that is a narrower question than FF-6 asked.
- **Priors.** The mask `0xFFFFBFF75FFFCFFF` was already on
  [CONTRACT-commit-action.md](../../../07-Combat-Action/CONTRACT-commit-action.md). A grep of the mask on the owning
  pages would have caught this before the sweep.
- **What stands.** The set site, the conditional phase-10 clear, the bit-30 arm, the test site, C4 and C5, and
  the native command seam's phase-10 narrowing.
