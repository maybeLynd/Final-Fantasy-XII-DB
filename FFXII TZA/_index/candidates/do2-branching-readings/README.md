# DO-2 — every branching verb-handler body, read

FABLE, Claude Opus 5.5, 2026-09-27. **NATIVE/STATIC. Nothing was executed.**
Readings: `do2-branching-readings.tsv` (293 rows). Control: `do2_readings.py` (5 checks, FAILS 0).

**The population.** DO-2 names 293 bodies:
- the 173 branching primary handlers in `scriptvm-verb-shapes.tsv`;
- the 120 branching secondary-slot bodies in `members/dispatch-secondary-handler-shapes.tsv`, counted by OPUS on
  2026-09-22.

Each gets one row, with these columns:
- the verbs or slots the body serves;
- the arguments it pops;
- every conditional branch, as *site: what is tested → what each side does*;
- a one-sentence reading;
- its callees;
- a confidence.

The calling convention used throughout is `CONTRACT-verb-dispatch-abi.md`'s: `rcx` issuer, `rdx` target actor, `r8`
the command's 16-byte scratch, `r9` the value stack.

**How the rows were made, and what checks them.**
- **Drafting.** Two subagent passes (Claude Opus 5.5, under FABLE) drafted the rows, one half each. Callees are named
  only from the listing, `functions.tsv` working names, or a page that names the address; otherwise the address stands
  alone.
- **The control.** It re-derives from the executable everything in a row that the bytes decide: the branch count and
  exact condition sites (D2), the callee set (D3), and the pop sequence (D4). It passes all 293 rows.
- **The prose.** The meaning of each condition, which no script can check, was read against the disassembly by FABLE
  for six bodies: `0034EBC0` setpos (including the argument order into `0026AF80` / `0026B0C0`), `0034D620` aask,
  `0033FF40` geteventspace, the 12-branch state machine `0034DB30`, `003409F0` and `0034D790`. All six agree.

**What the reading turned up.**
- **Dead arms.** 15 bodies branch on `005C5230` (always 0) or `0053DD10` (always 1), so one arm can never run. Each
  row says which.
- **No effect.** Two bodies (`00348A00`, `00349000`, the `setgaugeraceiconpos` pair) only pass their arguments to the
  `ret 0` stub.
- **Round trips.** Several bodies push a constant and pop it straight back, so they consume no script argument. The
  rows state this literally.
- **Unwritten stack slots.** Three bodies read a stack slot they never write:
  - `003409F0` and `003418B0` return the caller's `r8` home slot when their phase word is neither 0 nor 2.
  - `0034D790` reads a fifth stack argument. The lifecycle executor gives that argument (the actor manager,
    `002622C4`–`002622CD`) to `begin` only. If this body is called in another slot, the value is whatever the
    executor's frame holds there.

  In each case the body is fully read; the value is simply not defined by the code.
- **A jump table.** `00354230` dispatches through a six-entry table (`003542A0`), read from the image: entries 0–1
  load a signed byte, 2–3 a signed word, 4–5 a dword.

**Not claimed.** What the unnamed callees do, beyond their names where a page gives them. DO-2 asked for the branching
bodies to be read. Their callees are each read on their own pages or are the frontier those pages track.
