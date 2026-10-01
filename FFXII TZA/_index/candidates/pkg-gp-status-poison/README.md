# PKG-GP-STATUS-POISON evidence (FABLE, Claude Opus 5.5, 2026-09-29)

The package record is [`PKG-GP-STATUS-POISON`](../../completion-packages/PKG-GP-STATUS-POISON.md). Its locators come from an
explorer pass. Each item here is re-checked from the image before it is stated.

## Q7: a Poison tick can KO its target

[`poison_ko.py`](poison_ko.py) runs A, S, H and M: FAILS 0 ([output](poison_ko.out)). Static.

- **A.** The Poison arm (`00386D9B`–`00386E39`):
  - sets flag A `|= 0x140`;
  - computes the share as `trunc(base / 16)`, where the base is max HP (doubled under Bubble), or `max(current HP, 1)`
    under Disease;
  - uses −1 when the share is ≤ 0;
  - adds the negated share to the HP accumulator `+0x24`, and sets flag C `|= 0x4000`.
- **S.** The applier's HP step (`00311608`–`00311668`) runs on `+0x2C` bit 8. For `0x140` it derives HP-write flags `0x40`,
  and uses the delta writer.
- **H.** The HP write clamps the new HP to the unit floor (`0030064C`) and tests for death against the same floor
  (`0030078B`).
- **M.** The model gives shares −62 / −125 / −2 / −1. HP 40 of 1,000 is lethal; HP 100 of 1,000 leaves 38. The model rejects
  "a tick leaves 1 HP".

The claim is stated on the status-write page (`10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md`),
after the stage-2 table. It is an addition, and nothing on that page said otherwise.

**consumer:** EZ-6 and FA-4 (a Poison-tick kill credits rewards when the Poison was applied by the party) agree: they presume
exactly this kill. The HP-write page §2.2–§2.5 agrees and is unchanged. The periodic-tick contract states no KO rule, and it
agrees.

**Not claimed:**
- the eligibility gates' outcome for a particular unit;
- any live observation. The replay of the arm is requested from OPUS as FABLE-REQ-OPUS-POISON-ARM-REPLAY (Q6).
