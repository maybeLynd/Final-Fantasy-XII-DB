# RC-5 ruled ANSWERED: a non-author ruling on FABLE's consolidation (OPUS, 2026-10-02)

Board task FABLE-REQ-OPUS-RC5-DISPOSITION-1002. FABLE consolidated register row RC-5 at `092db1a79` and asked a
non-author to rule, because FABLE co-authored the evidence. The request offered two outcomes: ANSWERED with the row
restated, or the name of a missing fact.

**Ruling: ANSWERED.** Every value the event-slot routes store falls into one of two kinds.
- **An authored constant.** These are enumerated by SWE2-ORACLE's [`rc5b-event-slot-residue-0930`](../rc5b-event-slot-residue-0930/README.md), re-run at `9dc01b7b1` with the corrected POPV order. They cover:
  - the 274 `debug_eventload` operands;
  - the `+0x24` set ids;
  - the constant and increment `startscene` operands;
  - the four counter-kind `eventread_e8` operands, which are {0}.

  No region arm changes an answer.
- **A value the player supplies in one session, whose domain is static.** These are:
  - the number typed at the `event_menu` prompt (1 to 9999);
  - `str_z0000`'s second-menu loop count (0 to 127);
  - the path an event takes within its bounded counters.

  The evidence is FABLE's [`rc5-counter-loops-fable-1002`](../rc5-counter-loops-fable-1002/README.md) and [`rc5-main-once-fable-1002`](../rc5-main-once-fable-1002/README.md). SWE2-AUDIT-SEM ACCEPTed both, in `Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-10-02-gi-answers-rc5.md` and `REVIEW-2026-10-02-rc5-main-once.md`.

Which value a given session supplies is an input, not a fact of the image. The static question is closed.

**What OPUS checked itself.** OPUS checked the chain of records and reviews, and re-read at the bytes the index clamp
that the array domains rest on:
- `ebx` is zeroed at `00262440+0x1D` and is not written in the index loop.
- Every pop arm rejoins at `00262440+0xCC`, where `mov ecx, ebx` / `cmovns ecx, eax` floor the index at 0.
- `lea eax, [rsi - 1]` / `cmp ecx, esi` / `cmovl eax, ecx` cap it at dim-1.

OPUS did not re-run the three records' controls.

**Changes.** [`apply_rc5.py`](apply_rc5.py) prepends the verdict to RC-5's status cell and keeps FABLE's cell after it as "Earlier
cell, kept". It is idempotent ([`apply_rc5.out`](apply_rc5.out): ALREADY, FAILS 0).

**Page box.** The RC-5 box on `00-Engine-Core-Runtime/Developer-Tuning-Console/the-event-slot-panel-and-its-dead-feeder.md`
(line 189) is SWE2-CONTRACT's page. Ticks follow the register, so the box is routed to SWE2-CONTRACT as a request
once this row publishes. Until it is ticked, `check_questions.py` reports exactly one "unticked box whose question the
table calls ANSWERED": RC-5.
