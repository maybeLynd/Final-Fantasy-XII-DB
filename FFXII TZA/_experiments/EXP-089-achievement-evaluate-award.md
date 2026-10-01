---
experiment: EXP-089
title: Achievement evaluate, award and fire helper under isolated original execution
contract: ../20-Platform-Online-Achievements/CONTRACT-achievement-counters.md
method: B
live_game: false
tool: evidence/achievement-evaluate-award/check.py
# Transcribed from this record's own prose header by OPUS 2026-09-16; status and dates
# are SWE2-ORACLE's to state and are deliberately left absent.
---
# EXP-089 — achievement evaluate+award and fire-helper execution

**Date:** 2026-09-15 · **Worker:** SWE2-ORACLE · **Method:** B (isolated original-code execution, Unicorn)
**Subject:** evaluate+award `00315E90`, fire helper `003165C0`, plus the whole bounded call surface
**Contract:** `Database/FFXII TZA/20-Platform-Online-Achievements/CONTRACT-achievement-counters.md`
**Board task:** `SWE2-ORACLE-ACHIEVEMENT-EXEC`
**Evidence:** `evidence/achievement-evaluate-award/` (`check.py`, `result.json`, `bodies.json`)

## Result

**54/54 cases pass; 9/9 byte-level mutants detected.** Stable across two full processes.

The contract's §13 differential harness ran `003166F0` read, `00316A50` update and `00316BF0`
store, but deliberately skipped `00315E90` (evaluate+award, eight-arm descriptor-mode dispatch)
and `003165C0` (fire-helper chain walk) as "testing something else". This package executes both as
shipped bytes at canonical VAs, together with 27 further real bodies covering every callee either
function can reach. Only three effects are stubbed, all disclosed: IAT `008C3190` (the platform
name→object getter inside `0020CE60`), the planted object's two vtable slots `+0x38`/`+0x50`, and
the fam3 data pointer (`001EEBCC0` entry `+8`) which is zero in the shipped image — the family
table's counts (`+0x3C`) and resolver fnptrs (`+0x50`) are shipped constants, so the `jmp [entry+0x50]`
dispatch and the fam3 resolver `002FD970` run **real**.

## Executed confirmations

- **Evaluate gating, in order**: `id >= 0x1F` rejected before any call (`eval-id31-bound`,
  trace = `[eval]`); awarded-bit test reads `saveBase+0x3844` once via `002536A0` and exits on a
  set bit (`eval-awarded-early`, trace = `[eval, savebase]`); mode = descriptor byte `+2` of the
  shipped table `00D10460`; dispatch via the shipped jump table `00316098` (base-relative dwords).
- **Modes 1 and 4 are dead eval arms** — the jump table sends both straight to the epilogue.
  Shipped descriptor id 19 is mode 1: with every threshold resource maxed it still cannot award
  through `00315E90` (`eval-m1-dead`, `eval-mode1-dead-patched`, `eval-mode4-dead-patched`).
- **Mode-0 arm** (`eval-m0-*`): `fire(id)` → `cmovnz` fallback to descriptor param →
  `lookup(id)` → `read(id)` → `counter >= threshold` → award. Traces measure the exact call
  order `fire→lookup→read`.
- **Mode-2 arm is a range scan** (`eval-m2-*`): descriptor param packs `lo16 | hi16<<16`; the arm
  iterates `bx = lo..hi-1` calling `00309EC0(bx)` and requires **all** to return nonzero. For id 9
  (param `0x30513000`) that is exactly 81 calls `0x3000..0x3050` — matching shipped fam3 count
  `0x51`. First zero aborts the scan (`eval-m2-one-missing`: 17 calls). The resolver sees the full
  16-bit sub-id in `ecx`, `edx=0` (`eval-m2-idx-arg`).
- **`00309EC0` sentinel vs OOB split measured**: `(cx & 0xF000) > 0xE000` or `cx == 0xFFFF` returns
  `-1` → counts as **present** (`eval-m2-sentinel-pass`: 8 sentinel ids, zero resolver calls,
  award code 6). Index `> count-1` returns **0** → fails (`eval-m2-oob-fail`: the `0x52`nd call
  reaches `00309EC0` but never the resolver). These are opposite signs through the same `test
  eax,eax` — a reconstruction that treats "out of table" uniformly will mismatch.
- **`003165C0` fire helper, all paths**: 4-hop chain of u16 relative offsets starting at
  `[0022C2550]+8`; each hop adds the offset to the **low 32 bits** of the current node address and
  fails on a zero sum (measured: `fire-wrap-guard` wraps `0xFFFF0001+0xFFFF` to 0, `fire-root-neg8`
  wraps the root itself). Mask at terminal `+4`, `id >= 0x20` rejected, `bt` on the mask, then a
  `rol`-loop computes rank = `popcount(mask & ((1<<id)-1))` and returns `dword [term+8 + rank*4]`
  (`fire-rank0/1`, `fire-id31`, `fire-bit-clear`, `fire-mask-0`).
- **Update ordering — the contract's call-order claim measured**: kind≠0 path runs
  `read → add → eval → store`; evaluate observes the **pre-add** counter, so a threshold-crossing
  add defers the award by one update (`upd-order-first`: +5 to counter 0, no award, 5 stored;
  `upd-order-real`: the *next* update's eval sees 15 ≥ 10 and awards).
- **Update add rules by kind**: kind2 saturates at `0x7FFF` (`upd-sat-word`), kind4 at
  `0x7FFFFFFF`, negative sums clamp to 0 (`upd-neg-clamp`), mode 3 does `bts counter,
  amount-0xE2` (`upd-m3-bts` → word `0x0008`), **mode 8 reads the counter then skips eval and
  store entirely** (`upd-mode8-skip`, trace = `[update, read, savebase]`).
- **kind==0 update is a separate inline award dispatch** — it never touches counters or `00315E90`:
  mode 0 → `fire(id)` else param fallback, `amount >= thr` → award (`upd-kind0-mode0`,
  `upd-kind0-mode0-below`); mode 1 → `amount == param` → award (`upd-kind0-m1-eq`: id 19 awards
  code 17 through update at amount `0xD07F` even though the eval arm is dead); other modes → out.
- **Bounds differ between the pair**: evaluate admits `id < 0x1F`, update admits `id < 0x1E`.
  id 30 dispatches inside evaluate on the award-code table's bytes (descriptor table ends at id
  29): it reads kind 1 / mode 0 from `01 00 00 00` and fails at `read` returning -1
  (`eval-id30-alias`).
- **Award tail, end to end**: success sets the awarded bit via two `002536A0` calls (`bts` on
  `saveBase+0x3844`), loads award code from shipped table `00D10550[id]`, calls `008632B0` →
  `0020CE00` platform object → `0020CE60`. With `pobj+0x18` set the write performs two name
  lookups (IAT stub) and two vtable calls (`+0x38`, `+0x50`) — order measured
  `nameobj→vt_238→nameobj→vt_250` (`award-obj-flag`). Null platform object: the save-side bit is
  still set, `awardtail` returns after the first `pobjget` (`award-null-pobj`).
- **lookup**: id 5 → `read` first, then `savebase→playrefresh→secs→playtime` refresh order
  measured (`lookup-id5-playtime`: 3600.0+7 → 3607 written to `[002092758]+0xC`); id 8 →
  inventory average requiring **≥6** qualifying items of avg byte `+0xBA` (`lookup-id8-*`: 5
  items → 0 not the average, 9 items → 9 slot scans → 5); kind0 → -1 (`lookup-kind0-neg1`).
- **Mode-3 arm** calls `fire`+`read` directly (no `lookup`): popcount of the counter word's low 16
  vs threshold (`eval-m3-popcount`, `eval-m3-below`, `eval-m3-fire-threshold`).
- **Mode-5/6/7 arms** (`eval-m5/6/7-*`): record at chain-root `+8` for mode 5, one link hop for
  mode 6, three for mode 7; mode 5 counts save-record popcounts per set bit through `00255120`;
  mode 7 selects an entry by param and tests `huntmark(entry) - 1 > 0` — mark 1 fails, mark 3
  passes (`eval-m7-fail`/`eval-m7-pass`).

## Findings

- **F1 — "dead" mode 1 is only dead in evaluate.** `00315E90`'s jump table sends modes 1 and 4 to
  the epilogue unconditionally, but `00316A50`'s kind==0 dispatch implements mode 1 as
  `amount == param → award`. Shipped id 19 (kind0, mode1, param `0xD07F`) is awardable exclusively
  through the update path. Any contract wording like "mode 1 cannot award" must be scoped to the
  evaluator.
- **F2 — the two bounds differ.** Evaluate rejects `id >= 0x1F`; update rejects `id >= 0x1E`. id 30
  can be *evaluated* (dispatching on descriptor-table overrun — the award-code dwords at
  `00D10550` alias as kind/mode bytes) but can never be *updated*.
- **F3 — `00309EC0` distinguishes two "miss" shapes with opposite signs.** Sentinel ids
  (`cx==0xFFFF`, family nibble `> 0xE`) return -1 = present; in-family index overflow returns 0 =
  absent. The mode-2 scan therefore fails on index overrun but silently accepts sentinel ids.
- **F4 — the fire-helper chain is 32-bit truncated.** Every hop computes `low32(node) + u16` and
  rejects on a zero sum; the chain physically cannot address above 4 GiB and has a deliberate
  wrap-guard, not a pointer-width bug.
- **F5 — mode 8 in update still performs the counter read** before skipping eval+store — the skip
  is post-read, observable if the read has side effects (id 5/id 8 refreshes).
- **F6 — family table `001EEBCC0` is half-shipped, half-runtime.** Counts (`+0x3C`) and resolver
  fnptrs (`+0x50`) are shipped constants; the data pointers (`+8`, `+0x20`, `+0x30`) are zero on
  disk and must be runtime-initialised — planted here as a disclosed fixture.

## Mutation campaign (9/9 detected)

| mutant | site | effect measured |
|---|---|---|
| eval bound `0x1F` → `0x1E` | 00315E92 | id 30 now rejected at entry |
| awarded-bit `jne` → `je` | 00315EE0 | unawarded id early-returns; awarded id would proceed |
| jump-table bound `7` → `3` | 00315F05 | mode-5 descriptor reaches only `[eval, savebase]` — no arm executes |
| mode-0 `jl` → `jle` | 00315F3C | counter == threshold no longer awards |
| mode-3 popcount loop `16` → `8` | 00315FCA | high-byte set bits stop counting → threshold miss |
| fire id bound `0x20` → `0x10` | 00316601 | id 16 rejected (returns 0) |
| id-8 item minimum `6` → `5` | 003167DB | 5 qualifying items now produce the average |
| update mode-3 `bts` base `0xE2` → `0xE0` | 00316B75 | sets bit 5 instead of 3 → word `0x0020` |
| word saturation `0x7FFF` → `0x7FFE` | 00316B97 | stored value saturates at `0x7FFE` |

## Deviations and limits (disclosed)

- **Three stubs only**: IAT `008C3190` returns a planted object (the real name→object subsystem is
  not exercised); the planted object's vtable `+0x38`/`+0x50` log and return 1 (real platform-side
  effects not proven); fam3 `+8` bitset pointer is planted (runtime-initialised in the live game).
- **Synthetic fixtures** for the save image, playtime/frame structs, inventory, u16 table, chain
  structures, and platform object. All address constants were re-derived from rip-relative
  operands in the shipped bodies, not from the contract's prose — two contract-adjacent addresses
  in earlier notes were off (`0x22C2550` root, `0x1EEBCC0` family table) and are corrected by this
  execution.
- **id 30 descriptor aliasing** reads the shipped award-code table as a descriptor — behaviour
  measured on real bytes, not interpreted.
- Isolated original-code evidence under Unicorn; no NATIVE-REPLAY or live claims. The achievement
  platform layer (real Steam/platform call effects) is out of scope by construction.

## Kill set

Every mutant diverged on observable state: entry bounds (both functions), the awarded-bit branch,
the jump-table bound, the mode-0 compare, the mode-3 popcount width, the fire id bound, the id-8
minimum, the mode-3 bts base, and the word-saturation constant.
