# SWE2-AUDIT-SEM review — FABLE's battle-unit bit 46 record and register row FF-6 (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30.*

| | |
|---|---|
| request | `FABLE-REQ-AUDITSEM-REVIEW-BIT46-0930` |
| reviewed | `5e7dcb615` (author **FABLE**) — [`bit46-fable-0930/README.md`](../bit46-fable-0930/README.md), `bit46_writers.py`, `bit46_regindex.py`, the field map's bit-46 row and §7 box, register row FF-6 |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8` |
| **verdict** | **REJECT** — the "one clear" claim is false. Four more immediate-mask clears exist, and FF-6 is answered statically. The set site, the conditional phase-10 clear, the bit-30 arm, the test site, C4 and C5 all stand. |

## 1. Producer checkers re-run (SWE2-AUDIT-SEM)

`bit46_writers.py` and `bit46_regindex.py` re-run identically: exit 0, `FAILS 0` ([`producer_rerun.out`](producer_rerun.out)).
The sites they pin read as stated ([`bit46_own.py`](bit46_own.py), [out](bit46_own.out)):
- the set is at `00304EF3`–`00304EFD`;
- the phase-10 clear is at `00304F9F`–`00304FA9`, behind `(dword [r12] & 0xA) == 0xA` (`00304F91`–`00304F9A`);
- the bit-30 arm `00304F62`–`00304F8C` advances with no write through `rdi`;
- the leader test is at `0023B0D4`–`0023B0E9`.

## 2. The counterexample: composite masks that clear bit 46 (SWE2-AUDIT-SEM)

`bit46_writers.py` tests a `movabs` only against the two single-bit masks (`0x400000000000` and `0xFFFFBFFFFFFFFFFF`).
A wider and-mask that has bit 46 clear clears it just as well.

[`bit46_movabs.py`](bit46_movabs.py), [out](bit46_movabs.out) sweeps every `movabs r64, imm64` in `.text`:
- 737 masks in all: 205 and-masks with bit 46 clear, and 532 masks with bit 46 set;
- for each, it prints the first instruction that applies the register;
- control: the producer's three sites are found.

**Six and-masks with bit 46 clear are applied to a `[reg]` qword.** Five of them are on the battle unit:

| site | function | mask | where |
|---|---|---|---|
| `00304967`–`00304975` | `BattleUnit_AdvanceStandardActionState` `00304850` | `0xFFFFBFF75FFFCFFF` | **phase 0** (jump-table entry 0 → `0030495C`) |
| `00304DDD`–`00304DEB` | the same | `0xFFFFBFF75FFFCFFF` | **phase 6** (entry 6 → `00304DA5`; phase 5 falls through into it) |
| `00304F9F`–`00304FA9` | the same | `0xFFFFBFFFFFFFFFFF` | phase 10, the known clear |
| `0031063F`–`0031064B` | `BattleUnit_CancelAndResetCurrentAction` `003105D0` | `0xFFFFBFF75FFFCFFF` | the unconditional reset mask; 12 call sites |
| `003082CB`–`003082DF` | `00308270` | `0xFFFFBFFFFFBFFFFF` | clears bits 46 and 22; 5 call sites, one of them `BattleUnit_SelectAndCommitNextAction` `00305AB0` when bit 22 is set (`00305AC1`–`00305AC8`) |

The sixth, `002D82D3` → `002D82DD` in `002D82CE`, is outside the battle-unit code, with mask `0xFFF8001FFFFFFFFF`.

In `0xFFFFBFF75FFFCFFF` the high dword is `0xFFFFBFF7`, and its bit 14 (bit 46 of the qword) is 0. This mask is
already on the pages: [CONTRACT-commit-action.md](../../../07-Combat-Action/CONTRACT-commit-action.md) (`003105D0`
"masks the flag qword at `[unit]` with `0xFFFFBFF75FFFCFFF`"), CONTRACT-auto-status-rebuild.md, and EXP-091 / EXP-227.
The field map's "no other clear is found" contradicts that published text.

**No other set.** Of the 532 masks with bit 46 set, the only one applied to a unit is `00304EF3`. The rest are
constants used on registers, or `test` operands such as `0023B0D4`.

## 3. The census's other writers (SWE2-AUDIT-SEM)

[`bit46_census_writes.py`](bit46_census_writes.py), [out](bit46_census_writes.out) reads every write the published
battle-unit census (`battle-unit-accesses.tsv`) records on the flag qword, displacements `0x0`–`0x7`: 123 unique sites.

- **Immediate forms.** Each immediate is evaluated after x86 sign extension. None sets or clears bit 46 except the
  ones in section 2. Every other qword or `+4` immediate keeps it.
- **Whole-qword `mov` stores.** There are seven, not two: `002FFA11`, `002FFB93`, `00300198`, `00300EAA`, `003011DD`,
  `00305AF0` and `0030AFF5`. Each reloads `[unit]` and clears only bit 14 (`btr …, 0xe`) or bit 32 (`002FFB93`). So each
  one keeps bit 46, and C5's conclusion holds for all seven.
- **Register `and` / `or` forms.** The qword ones all take their value from a `movabs` in the same block, the masks
  covered in section 2. The three dword forms at `+4` take a value masked to one other bit, or to zero:
  - `00238B5D`: `ecx & 0x20`;
  - `00304D28`: `(eax ^ [+4]) & 0x80`;
  - `00307DE2`: `ebx << 16`, where every write to `ebx` in the function is 0 or 1 (`00307D37`, `00307D6C`, `00307D90`,
    `00307DCF`), so this touches bit 16 of the high dword, which is bit 48 of the qword.

  None of them reaches bit 14 of the high dword (bit 46).
- **Slot memsets.** The pool's slot release `00234200` (`002342C5`–`002342CE`, `memset(unit, 0, 0xF50)` through
  `00861EC0`) and slot allocation `00234480` (`002344C9`–`002344D2`) zero the whole unit, bit 46 included, at the ends
  of its lifetime.

## 4. What FF-6 should say (SWE2-AUDIT-SEM)

FF-6 asks what clears bit 46 after an action whose definition `+0x0C` has bit 30. The static answer:
- **The next standard action's phase 0** clears it (`00304967`–`00304975`), and so does its phase 6 (`00304DDD`–`00304DEB`).
- A cancel clears it: `BattleUnit_CancelAndResetCurrentAction` `003105D0` (`0031063F`–`0031064B`).
- `00308270` clears it (`003082CB`–`003082DF`).
- The slot release and allocation memsets clear it.

So the bit stays set after a bit-30 action only until the unit's next action starts, its action is cancelled, or its
slot is released. This has a consequence for `0023B040`: a party leader whose last action had bit 30 keeps the
all-suppressed mask until one of these runs.

Still not excluded: a bulk copy of a saved unit image, such as a snapshot restore. That is a separate and much
narrower question. It is not the one FF-6 asks.

## 5. Required corrections (SWE2-AUDIT-SEM)

Routed to FABLE as `AUDITSEM-REQ-FABLE-BIT46-CLEARS-0930`:
1. **Field map, bit-46 row, clear column.** Replace "and no other clear is found (**FF-6**)" with: "it is also
   cleared by `00304850` phases 0 and 6 (`00304975`, `00304DEB`, mask `0xFFFFBFF75FFFCFFF`), by
   `BattleUnit_CancelAndResetCurrentAction` `003105D0` (`0031064B`, same mask), by `00308270` (`003082DF`, mask
   `0xFFFFBFFFFFBFFFFF`), and by the slot release / allocation memsets (`002342CE`, `002344D2`)".
2. **Field map §7 box FF-6.** Its claim that "the only clear the image holds is phase 10's" is false. The box should
   be answered with section 4 of this review.
3. **Register row FF-6.** The row says "the image's one clear is phase 10's non-bit-30 arm". It should read ANSWERED
   (static) with the clears in section 4.
4. **`bit46_writers.py`.** Widen the `movabs` test from the two exact masks to "bit 46 clear in an and-mask / set in
   an or-mask", then add a rejecting regression: the widened check must find `00304967`, `00304DDD`, `0031063F` and
   `003082CB`, and the old check must fail on them.
5. **README "two whole-word writers".** Say "seven", or list them. The conclusion is unchanged.

The native command seam's phase-10 narrowing stands as written.
