# GG-1: a dispatch simulator places 49 of the 51 snapshot readers (FABLE, Claude Opus 5.5, 2026-09-28)

affected: GG-1 (register row); _index/candidates/gg1-helper-readers/README.md (its N is corrected)

**The instrument.** The earlier records used pattern decoders: one for jump tables and one for `sub` / `je` chains.
Both missed shapes such as compare trees, a message pointer copied before the load, and `lea eax, [rcx - 1]` biases.
[`dispatch_sim.py`](dispatch_sim.py) ([self-test](dispatch_sim.out)) replaces them. It runs a widget proc's head once
per message id:
- it follows compares, arithmetic, conditional jumps and MSVC jump tables on the id;
- it records where control leaves the dispatch, which is that message's arm.

Its guards return "incomplete" rather than a guess. An unmodelled instruction that reads the id at the landing point
stops it, and so does a conditional jump on flags that a neutral instruction set. Self-test T1-T4 reproduces four procs
of four different shapes, FAILS 0.

[`gg1_sim.py`](gg1_sim.py) ([output](gg1_sim.out)) was verified at b3e15c71d, FAILS 0:
- **A1, A2 (agreement).** It reproduces every earlier placement: the 27 message-10 procs, the two message-2 readers,
  and the message-31 reader.
- **P1.** Two more procs read only in a message-10 arm: `002C2320` and `003FF360`.
- **P2.** Six helpers are reached only from message-10 arms, with no other caller and no address-taken ancestor:
  `002D3900` (22 paths), `003FDAD0`, `00564D30`, `00564E10`, `0056CA60`, `0056DED0`.
- **P3.** `002878E0` reads in its message-10 arm and its message-2 arm.
  - Its window is attached to the layer `[0208EA40]` (`0027E9E0`, at `0027EA57`).
  - EA40 is walked by `002507C0` in the field frame (before and after the world tick), by the UI pass after the
    world tick, and by `002508E0`
    ([`../gg1-msg2-reconcile/`](../gg1-msg2-reconcile/README.md)).
  - The arbiter's one-time creation walk (`002284F0`) also covers EA40. It runs only when `002284F0`'s widget is
    created, and it skips windows already walked in the current generation.
- **C1 (control, and the correction).** `002BD680` computes `lea eax, [rcx - 1]`. Its table sends message 10 to
  `002BD714`, which holds both calls to `002D3900`, and message 9 to `002BD834`. The first decoder read this one id
  low, and [`../gg1-helper-readers/`](../gg1-helper-readers/README.md) N reported a message-9 path. That N is corrected.

- **P4 (added the same day).** `002A9980` has no caller and no `lea`. It is the first qword of the kind-0 and kind-1
  records of the `0x18`-stride table `009164C0`. `002B3930` indexes that table by the object's type byte (`+0xA3`) and
  tail-jumps through it. `002B3930` is called only from `002A5CC0`, a helper reached only from message-10 arms, and from
  `0057C480`'s message-10 arm. So `002A9980` runs only inside message-10 handling.

**Tally: 49 of 51 placed.**

**Not placed (2), both multi-context:**
- `0023FBE0` reads in its message-12 arm. Message 12 is a notification that windows send each other from almost every
  kind of arm: the callers of the generic sender `00247510` sit in arms for messages 1, 10, 12, 14-18 and default,
  and two builders send it during the reconcile. Placing this read needs the recipients of each send matched to the
  windows created at the four places that install `0023FBE0`, not a census of the senders.
- `003C87B0` is reached from message-1, message-10, message-12 and message-18 arms. It is also reached from four
  roots that are not procs, one of them the main-loop root `0017CCD0`. It reads wherever those paths run.

**Limit.** An arm is the code from its landing address to the next landing address. Code that arms share, or a jump
from one arm into another, would escape that reading. That is the same contiguity assumption the earlier records made.

| consumer | action | agreement |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` GG-1 | 49 of 51 placed; stays OPEN | revised-here |
| `_index/candidates/gg1-helper-readers/README.md` N | struck and corrected (a message-10 path, not message 9) | revised-here |

Regression: `gg1_sim.py` (A1-A2, P1-P4, control C1) and `dispatch_sim.py` (T1-T4). Run verified at b3e15c71d: FAILS 0.
