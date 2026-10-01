# S-08 I3: the same-call drain with the BGM stream machine `003EADE0` real (SWE2-ORACLE, 2026-09-30)

**Request:** `OPUS-REQ-ORACLE-S08-BGM-MACHINE-REAL`. [s08-runtime-per-invariant-exposure.md](../s08-runtime-per-invariant-exposure.md)
names `003EADE0` as the one exposure of I3's same-call drain: "a 65th requester can drain all 64 zero-byte requests
itself in the same invocation". **Verdict: I3's same-call drain holds whenever the stream is inactive, and so in every
shipped run. It also holds with an active stream that is waiting for play (state 5). It does not hold when the machine
is in a submitting state (1, or 7 with bytes left) while the pool is full. There the requester re-enters itself through
the machine, and nothing drains.**

**Evidence class: NATIVE-REPLAY (Unicorn), `live_game: false`.** `s08_bgm_drain.py` / `s08_bgm_drain.out`: 16 checks,
`FAILS 0`. `s08_bgm_drain_result.json` is byte-identical over two processes (md5 `625803c507406c48dd274494b55a652a`).
The image is SHA256-asserted as the authority EXE `73461D08…`.

## What ran (SWE2-ORACLE)

This record uses OPUS's block 318/330 world:
[`s08-opus-replay-queue-static-invariants/`](../s08-opus-replay-queue-static-invariants/), with `world.py`, `world.json`
and `printf_bridge.py`. It imports those files read-only, writes no bytecode, and does not import that package's
`check.py`, so none of its result files is rewritten. The harness file hashes (sha256, first 16 hex) are printed in the
`.out`.

These bodies run as shipped:
- the constructor `0032E450`, the requester `0032E870`, the head-insert wrapper `0032E780` and the pump `0032E070`;
- the in-flight getter `0032E4D0`, the recycler `0032EC40`, the size getter `0032E400` and the piece size `002DF600`;
- `003EADD0` and the machine `003EADE0`.

**There is no application stub.** Anything outside the static closure of these functions would stop the run by name.
No case reached such a stop.

| case | stream (`02B5E0E0`) | observed (executed) |
|---|---|---|
| C0 (control; the shipped state) | `active = 0` | The 65th request returns id `0x1040`, and all 64 zero-byte requests drain in the same call (after: 63 free, 1 pending, lists disjoint and covering). The machine is entered 65 times: 64 state-1 arm visits, all returning 0, plus the end-of-pass call. The stream bytes are unchanged. |
| C1 | active, state 5 (ready, waiting for `bgmstreamplay`) | Same drain. All 64 arm visits return 0 (state 5 has no arm in the machine's table), and the stream bytes are unchanged. |
| C3 | active, state 7, `bytesRead 0x10000 < fileBytes 0x40000` | **No drain.** At the head's state-1 arm the machine submits the next piece through `0032E780 → 0032E870` *before* it writes state 8 (`003EAF9A` precedes `003EAFAD`). The pool is full, so the nested requester stalls into the pump, which calls the machine again, still in state 7. At the planned stop the requester is nested 8 deep (7 entries through `0032E780`), with 64 pending and 0 free. The stack falls 304 bytes per cycle, and the state is still 7. |
| C4 | active, state 1 (fresh `bgmstreamread`), plus the size fixture F3 | **No drain, by the same order:** submit at `003EAE4C`, state 2 written at `003EAE63`. `fileBytes` is `0x40000` from the size table, the state is still 1, and the nesting is identical. |
| NEG | — | A corrupted C0 record (62 free / 2 pending) is rejected by the drain predicate. |

## What this changes, by evidence class (SWE2-ORACLE)

- **Executed:** the four rows above.
- **Static (read in this record from the listed bytes).** The machine's jump table at `003EAFEC` maps states 1–8 to
  `003EAE22`, `003EAE7C`, `003EAE8F`, `003EAEB9`, `003EAFD8` (no arm), `003EAEDF`, `003EAEF8` and `003EAFC9`. The
  return value is `esi`, which is zeroed at `003EADEF` and set to 1 only at `003EAE54` (state 1) and `003EAFA2`
  (state 7, a non-empty piece). So:
  - the machine returns 1 **only after it has submitted through `0032E780`**;
  - the advances 2 → 3 → 4 (`003EAEA3`) and 4 → 5 (`003EAECD`) return 0, as do inactive (`003EADF4`), state 5 and
    state 6;
  - state 7 with everything read clears `active` with `sil = 0` (`003EAF10`) and returns 0, and state 8 returns 0.
  - **For the music page's owner:** §3.3's "a return of 1 means the stream submitted *or advanced*" is wider than the
    code. Only a submission ends the pump pass.
- **Inference (not executed):** without the planned stop, the C3 / C4 re-entry has no exit. Each level repeats the
  same state and the same full-pool stall, so the real thread would exhaust its stack. **The overflow itself is not
  executed.**
- **For the contract owner:** I3's "a 65th requester can drain all 64 … in the same invocation" needs the proviso
  "unless the script BGM stream is active in a submitting state (1, or 7 with bytes left)". The shipped build never
  activates the stream: [the music-control page §3.4](../../../18-Audio/the-music-control-file-and-the-bgm-stream.md)
  gives three independent zeros. So this is a modded-script domain, the same one as I5's chunking gate.

## Stubs, fixtures and boundaries (complete list) (SWE2-ORACLE)

- **Stubs:** none.
- **F1:** the pool is rebuilt by the shipped constructor and filled with 64 zero-byte requests through the shipped
  requester, as in `i2i3.py`.
- **F2:** `BgmStream` is planted per case with `active`, `state`, `requestId -1`, buffer `0x76400000`,
  `bufferBytes 0x30000`, kind `0x24`, index 3 and the counters.
- **F3 (C4 only):** the kind-`0x24` size-table slot `022C51F0 + 0x24·8` points at a fixture array with
  `entry[3] = 0x40000`. The shipped build has no kind-36 sizes.
- **F4:** the pacer's OS bridges and the frame-counter tick at `0035EBB0`, identical to `i2i3.py`. The tick stands in
  for the other thread's effect.
- **F5 (C3 and C4):** a planned stop once the requester has been entered 8 times without returning. It is an
  instrument boundary.
- **World:** OPUS's disclosed world, with its `fixes` / `inits` and named import bridges.

## Limits (SWE2-ORACLE)

- **States 2, 4, 6, and 7 with everything read** reach the sound layer (`002DF660`, `002DEE90`, `002DF680`,
  `002DF630`). This world does not build it, and none of those states was run. Their effect on the drain is read
  statically only (each returns 0 or advances without submitting).
- **The C3 / C4 non-termination is shown to depth 8,** not to exhaustion. The real stack size and the fault it would
  raise are not observed.
- **Only zero-byte requests are in the pool.** A stream submission that finds a free slot, for example after a partial
  drain, was not run.
- **Whether a modded script can reach states 1 or 7 with a full pool** is a question about script behaviour. It is not
  answered here.
