# RC-37: a refused `.btm` read completes as if it ran (OPUS, 2026-09-30)

Register row RC-37 (registered by SWE2-CONTRACT from SWE2-DATA's round-2 record, `39d08c02f` §3 (2)). Static, the
certified image; no original-code execution, no live run. Checker: `rc37_refused_read.py` (output
`rc37_refused_read.out`, FAILS 0). Every fact below is an exact instruction the script re-reads.

## The answer (OPUS)

**The KR / CN staff roll does not wait. The refused request completes through the queue's normal completion paths, and
the `.btm` callback sets its ready bit. The roll then draws from a sheet buffer that no read ever filled.**

The chain:

1. **The refusal is invisible to the queue.** The kind-7 issue wrapper `0046E030` calls `002DF780` and then returns 1
   whatever `002DF780` returned (`0046E03E`, `0046E043`). `002DF780` refuses an id whose file-size entry is −1 by
   jumping to its epilogue (`002DF7B0`/`002DF7B9` → `002DF85D`). There it returns 0 and writes nothing.
   Only its accepted paths hand the reader the status slot `0215EFF4` (`002DF808`, `002DF838`). (F1, F2)
2. **The pump takes the refused issue as issued.** State 1 with kind ≠ 0xFF calls the wrapper at `0032E0F1` and sets
   state 2 without a test (`0032E0FF`); state 2 sets state 3 (`0032E15A`). (F3)
   - Control C1: the kind-0xFF branch *does* test its submit result (`0032E116`/`0032E118`, re-visit the head).
     So the missing test is a property of this branch, not of the reader.
3. **State 3 reads a status nobody refreshed.**
   - The request is busy only while `[0215EFF4] == −1` (`0046DFE0`); otherwise it goes to state 5, or 6 if the status
     is negative (`0032E19C`–`0032E1A8`). (F4)
   - The slot is written only by the readers' submit, which stores −1 through the pointer `002DF780`/`002DF6C0`
     pass (`001D6DD4`, `001D6FF4`), and by their completion job `001D6D70`. The job stores the worker's result once,
     then clears the stored pointer (`001D6D7C`, `001D6D7E`).
   - A census of every rip-relative reference to the slot and to the pointer global `01F82CC0` finds them only in
     those seven functions. (F5)
   - The queue issues one read at a time. The request ahead of the `.btm` one left state 3 only with the slot ≠ −1,
     and nothing has written the slot since. So the `.btm` request finds it ≠ −1.
4. **Both outcomes call the callback.** The request's byte count is the size query's −1 (`0032E400` returns it
   unrounded, `0032E43D`; `003658A4` passes it as the count), and its callback is `00364380` (`00365837`). (F7)
   - State 5 runs the done helper `0032E330`, which always calls the callback, success flag 1.
   - State 6 runs the error helper `0032E370`, which calls it (flag 0) exactly when the byte count is −1 — this
     request's count. (F6)
   - A chunked request (the `003EB0D0` gate) takes the same two helpers: remaining −1 minus count −1 is 0, then done.
5. **The callback ignores the flag.** `00364380` sets bit `slot` of `[[022CBE00] + 0x240]` whenever the `.btm` object
   exists, and never reads its success argument (F8).

## Limits (OPUS)

- **The sheet's contents.** `00365810` allocates the sheet with the −1 size through `002497E0` / `00249810` (the pool
  allocators `0036A100` / `0036A190`). What those return for a −1 request (null, a pool block, or a failure), and so
  what the draw reads, is not established here. RC-37's question (wait, or draw without a sheet) does not depend on
  it; what the player sees does.
- **The worker's result code** (`ecx` into `001D6D70`) is not traced. The argument above needs only that the previous
  request left state 3, which requires the slot ≠ −1 then.
- Static only. This does not show that a KR / CN build reaches the staff roll, or what the screen shows.

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review).

**Independent agreement (OPUS, 2026-09-30).** SWE2-DATA's `79e70e154` answered the same question as its RC-28 leftover:
"a refused .btm request still fires 00364380". It was derived separately from this record. The two agree; any detail
where they differ should be kept as a contradiction when the row is written.
