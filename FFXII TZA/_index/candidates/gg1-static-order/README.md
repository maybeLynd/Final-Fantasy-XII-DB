# GG-1: where the battle command menu reads the input snapshot, relative to the arbiter (FABLE, Claude Opus 5.5, 2026-09-28)

affected: GG-1 (register row). The input contract's GG-1 bullet is routed to SWE2-CONTRACT (see the table below).

**The question.** `02F9736A`, the newly-pressed snapshot word, has 51 readers. The arbiter `00253C70` clears it after
acting. A reader that runs before the arbiter in a frame sees the press; one that runs after sees what the arbiter
left. ASTRA's scoped capture (`gg1-scope/`) names one high-impact reader: the battle command menu's read at
`00277ACD`. This record orders that reader statically, from direct call sites. [`gg1_order.py`](gg1_order.py),
[output](gg1_order.out), run verified at 7bd14c999, FAILS 0.

**How the reader is reached.** `00277ACD` is inside `002778C0`, the command widget's message procedure, which
`00276D30` registers through the widget constructor.
- **O1.** The read lies in the arm for widget **messages 10 and 11**, the focus-input messages, decoded from the proc's
  own jump table. The per-frame reconcile, message 2, goes to a different arm.
- **O2.** Every sender of 10/11 goes through `002481C0`, which sends 10, or 11 during a transition, to the focus top.
  Its callers are the UI pass `00250540`, the pause step `002506D0`, `002507C0` (it sends only when its argument is 1),
  `00250730` and `002508E0`.

**The order in each frame kind** (direct call sites):

| frame body | order |
|---|---|
| `0022B8C0`, `0022BC20` (the full-menu and capture frames) | snapshot rebuild `002498B0` < world tick `00314020` (reaches the arbiter) < UI pass `00250540`. **Focus input arrives after the arbiter.** (O3) |
| `0022A770` (the field frame) | rebuild `0022A7F6` < [pause step `0022A8D7` while paused, then **the frame ends and the world tick does not run**] < `002507C0(1)` at `0022AB83` < world tick at `0022ABD8` < `002507C0(1)` at `0022AC17`. **Focus input can arrive both before and after the arbiter in one frame.** (O4) |

**The field frame's gates** (O5, O6):
- The pre-arbiter send at `0022AB83` runs only when `003583A0`, bit 3 of the flag word `022C7F92`, is set **and** the
  step accumulator `02064AC0` is exactly 0.0 (compared against `xmm7`, which is zeroed at `0022A9EF`).
- The post-arbiter send at `0022AC17` needs only bit 3.
- The world tick reaches the arbiter (`00314020` → `002E0D90` → `00253C50` → `00253C70`) on two paths. One of them is taken
  only when `esi == 0`.
- The field frame also gates the world-tick call itself (`0022ABB9`–`0022ABD2`).

*Qualified 2026-09-28 (FABLE, Claude Opus 5.5), consuming ASTRA-RETURN-FABLE-FIELD-FOCUS-FLOAT-GATE
(`_experiments/evidence/field-focus-float-gate/`). Verdict: ACCEPT, re-derived from the image bytes.*
- **The "exactly 0.0" test is an ordered equality.** `ucomiss xmm0, xmm7` at `0022AB79` is followed by `jp` (`0022AB7C`)
  and `jne` (`0022AB7E`). Both jump to `0022AB90`, past the send, so the send needs PF = 0 and ZF = 1.
  - +0.0 and −0.0 pass.
  - Any other ordinary value, and either infinity, fails.
  - A NaN fails once the comparison completes. With the invalid exception unmasked, an SNaN does not complete it.
  - With DAZ set, a nonzero subnormal compares as zero. So "the stored bits are zero" holds only under that
    precondition.
- The game's MXCSR and the accumulator's values are **unobserved**.
- ASTRA also showed that O5 did not bind the two branches: it still passed on a listing with the `jp` removed. The new
  check **O5b** binds `ucomiss`, `jp`, `jne` and both targets from the image bytes, and refuses that mutant.
  - The new run's output is [`gg1_order_v2.out`](gg1_order_v2.out), FAILS 0. O1-O6 and C are unchanged.
  - [`gg1_order.out`](gg1_order.out) is kept as the original receipt.
  - The order conclusions are unchanged.

**What this settles, and what it does not.**
- **Settled statically, for this reader:** in the full-menu and capture frames it runs after the arbiter. In the field
  frame, the first delivery precedes the arbiter whenever the `0022AB83` gates pass, so a delivery before the clear
  exists. Which frames actually pass those gates is a run-time fact.
- **Not settled:**
  - the other 50 readers, which were not placed;
  - whether the widget proc is also reached synchronously from inside the arbiter's own callees, which include
    menu-side functions (not resolved: indirect dispatch);
  - the live values of the gates.
- **The capture question sharpens.** Rather than ordering arbitrary hits, a capture can log `0022AB83` / `0022AC17`
  against the arbiter's clears. This goes to ASTRA as a notice.
- **Limits:**
  - "the arm at `00277A64`" assumes the arms are contiguous blocks;
  - the "full-menu and capture" frame names come from the game-application page;
  - the meaning of bit 3 of `022C7F92` is not established here.
- **Control C:** the jump-table decoder maps message 1 to `00277925` and 31 ids to one default arm.

| consumer | action | agreement |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` GG-1 | narrowed with the static order for the named reader; stays OPEN (50 readers, live gate values) | revised-here |
| `15-Input/CONTRACT-input-subsystem.md` GG-1 bullet (SWE2-CONTRACT) | the order table and the gates | routed-to-CONTRACT (FABLE-REQ-CONTRACT-GG1-STATIC-ORDER) |
| same bullet, the pre-arbiter gate's wording (2026-09-28) | "zero accumulator" is an ordered equality (NaN fails; DAZ caveat) | routed-to-CONTRACT (FABLE-REQ-CONTRACT-GG1-GATE-DOMAIN) |
| `gg1-scope/` and ASTRA's capture request | a sharper capture: log `0022AB83` / `0022AC17` against the arbiter's five clears | routed-to-ASTRA (FABLE-NOTICE-ASTRA-GG1-SHARPER-CAPTURE) |

Regression: `gg1_order.py` (O1-O6, O5b, control C). Run verified at 2b154289f: FAILS 0, output in `gg1_order_v2.out`. O5b fails if the gate bytes change or the jp is removed.
