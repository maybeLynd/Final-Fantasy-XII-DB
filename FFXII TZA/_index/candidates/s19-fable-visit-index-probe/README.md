# S-19: the separation visit walk indexes by VISITED POSITION, not by body (FABLE, Claude Opus 5.5, 2026-09-25)

**Evidence class: NATIVE-REPLAY (unicorn 2.1.4), `live_game: false`.** The shipped `003DAB50` runs unmodified. The
executable's SHA-256 begins `73461d0896204b1c`. Only its inputs are planted:

- the 128-bit candidate set at `02B57EE0`;
- the visiting body's remembered-pair bitmap at `+0x18`, in a planted 64-byte block;
- a callback, which is a `ret` whose hook records `rdx`, the body pointer it was handed, and returns 1.

The pool `02B4E4C0` is the image's own zero-filled tail, and only the pointer arithmetic is observed. `probe.py` runs
seven cases. `run_output.txt` holds three runs, and they are identical.

## Why it was run

OPUS block 337 corrected P-3's "every remembered bit is visited" to "the walk follows the candidate bits". Reading
the walk to amend P-3 turned up two index counters that do not advance together:

- The body pointer is reset from a per-byte base that advances `0x980` (eight bodies) per candidate byte, including
  zero bytes (`003DAC18`). It does **not** advance past a qword's trailing zero bytes, because the byte loop exits when
  the shifted qword is zero (`003DAC27`), or past an all-zero qword (`003DAB9A`).
- The remembered-bit index `r14d` advances once per inner iteration (`003DAC0B`). A zero byte does not advance it,
  and neither does a byte's run of zero bits above its highest candidate.

The reading predicts a mis-index. This run tests the prediction.

## Results

| case | candidates | remembered before | resolver handed bodies | remembered after |
|---|---|---|---|---|
| control, byte 0 only | 1, 3 | — | 1, 3 | 1, 3 |
| byte 1 only | 9 | — | **9** | **1** |
| bytes 0 and 1 | 1, 9 | — | 1, 9 | 1, **3** |
| qword 1 only | 64 | — | **0** | **0** |
| qword 0 byte 0 and qword 1 | 2, 64 | — | 2, **8** | 2, **3** |
| no candidate | — | 2 | — | 2 |
| byte 1, and a remembered bit | 9 | 2 | 9 | **1**, 2 |

The control is where the two readings agree, and there the mapping is exact. Everywhere else it is not:

1. **The remembered bit is stored at the count of positions visited, not at the body's index.** Candidate 9 alone is
   resolved against body 9, but its bit is set at index 1.
2. **Candidates in the second qword are resolved against the wrong body** unless byte 7 of the first qword holds a
   candidate. Candidate 64 alone is handed body **0**. With candidate 2 in byte 0, candidate 64 is handed body **8**.

## What this does and does not establish

- **Established, on shipped bytes:** the two mappings above, for planted inputs.
- **Bounded consequence, read and not executed:** the resolver re-tests the pair it is handed, so a mis-indexed call
  pushes only if the body it names actually overlaps (the contract's P-4 refusal chain). `003DAAB0` clears every
  candidate bit at or below the visiting body's own index. So byte 0 is empty for any visiting body at index 8 or
  above, and its remembered bits are misplaced. The second-qword mis-pairing needs a body at index 64 or above.
- **Not established:** how many bodies are registered in normal play, and therefore how often each case occurs live.
- **Body indices are handed out in ascending order per area** (read here, not executed). The area initialiser
  re-threads the pool at `00267141`. The thread routine links entry `i` to `i - 1` and `i + 1` for `i = 0..127` and
  sets the free head to 0 (`003DAE3A`–`003DAE9D`). The allocator pops the free head and advances it to the popped
  entry's `+2` link (`003DA8A6`–`003DA903`). Until the first release, the n-th body allocated in an area is
  therefore index `n - 1`, and **the ninth is index 8**, the first whose remembered bits land at the wrong index.
  *How many bodies an area allocates in play is the live question that remains.*
