# S-22 environmental element scaling: the stale §13 (FABLE, 2026-10-03)

*FABLE, on SWE2-AUDIT-SPEC's L2 expansion ([`auditspec-l2-expansion-1003`](../auditspec-l2-expansion-1003/README.md):
stale §13s under SF-4a of the sample, plus item 4's S-22 WE-2 row, "check for a driving case"). STAGED: this package
edits no tracked file, and `apply.py` was run as a dry run only. It is one of three S-22 packages; the step-table
package [`fable-l2exp-s22-1003`](../fable-l2exp-s22-1003/README.md) carries ST-4.*

## Finding (FABLE)

**The audit is right.** §13 of `CONTRACT-environmental-element-scaling.md` reads "**None.** No experiment executes
these four bodies", yet the stage `0038B220` and its three getters (`00263E10`, `00263E20`, `00263DD0`, each behind
its thunk) run in a recorded native replay. Two more packages cover WE-1 and WE-3. I re-ran all three from temp copies
at HEAD under unicorn 2.1.4, and every result file reproduced byte-identically: `99336e05…`, `a226db98…` /
`5680857b…` and `867bbaf3…`.

**What each covers, read from the records rather than the READMEs:**

- **`s22-opus-replay-steps-and-element-scaling`** (09-25):
  - **WE-4/WE-5 are asserted.** Bit 16 at `+0x6A`, at `+0x7A`, or at the caster's `+0x1C` skips everything.
  - **WE-6 is asserted only as a write-set bound:** `02AEE054` plus the qword `02EBF188`.
  - **The 288-combination rule table is RECORDED, not asserted.** The case's pass flag is the write-set bound.
- **`we1.py`** (09-26, 4/4) covers WE-1's order (94 immediately before 95 in recipes 7, 63, 83, 105, 106) and its
  read site (both stages read `+0x13`). **Its action row plants only `+0x08`** (`rows[0x20 * action_id + 8] = rid` is
  the only row write), so `+0x13` is 0 and no element rule fires on that path. That is the sample's SF-3, confirmed.
- **`s22-opus-replay-severe-weather-gate`** (09-26) asserts WE-3's consumer side: `00263E20` returns `[02099DAC]`
  verbatim for 0, 1, 2 and 5.

**Item 4's open question, answered: the replay DOES drive the shared multiply in WE-2's 10-02 correction.**

- **At the bytes,** the Lightning rule (`test byte [rcx+0x13], 2` at `0038B3E1`) has ONE `mulss` (`0038B420`). The
  environment test jumps to it (`0038B3F6 je 0038B418`), and the terrain test falls into it (`0038B416 jne` past).
- **In the recorded table,** the cells where an environment rule and a terrain rule of one element both hold read
  **1.2, never 1.44**: Lightning e0/t0 (all MWeather), Ice e2/t2, Earth e1/t1, and Water e3/t0 at MWeather 0 and 1.
- **Composition across different rules still multiplies:** Water e3/w2/t0 and Fire e0/w2/t0 read 0.6.
- **So WE-2's corrected text is executed and recorded, but not asserted by the package.** `check_s22_envscaling.py`
  asserts those cells from the record. Whether that earns runtime credit is SWE2-DATA's call.

## Staged edit (FABLE)

There is one strike-and-replace, **E1**, on §13. It strikes the whole "**None.** … *Stated rather than left blank …*"
paragraph and replaces it with:
- the evidence class (NATIVE-REPLAY, `live_game: false`);
- each package with its date and md5;
- what is asserted (WE-4/WE-5, the WE-6 bound, WE-3's consumer side);
- what is recorded only (the WE-2 table, including the 1.2 shared cells), and the `we1.py` caveat that the
  composition of the two stages is not executed;
- what is static (WE-3's banding, which belongs to the publisher, and §14's question on WE-4).

It closes with "Nothing here has been observed in a running game", followed by the stamp. The exact strings are in
[`edits.json`](edits.json).

## Check (FABLE)

[`check_s22_envscaling.py`](check_s22_envscaling.py) → [`check_s22_envscaling.out`](check_s22_envscaling.out):
**16 PASS, FAILS 0**.

- **Static and table.**
  - S1: one `mulss` serves both tests.
  - S2: the shared cells read 1.2.
  - S3: different rules still compose (0.6).
- **The record.**
  - W1, W2: WE-4/5 and the WE-6 bound are asserted.
  - W3: the table covers six elements.
  - W4: the table is recorded, not asserted.
  - W5: `we1` plants only `+0x08`.
  - W6: `we1` 4/4, `live_game` false.
  - W7: the WE-3 getter.
- **Controls.**
  - **C1 (sensitivity).** The old "multiplied in sequence" reading predicts 1.44 in the shared cells, and it is
    FALSE.
  - **C2 (sensitivity, stale text).** "No experiment executes these four bodies" is FALSE. The package calls
    `ESCALE = 0x38B220` and records writes, and the environment, the terrain and the MWeather class each change the
    recorded factor on their own, so all three getters are live.
- **Re-runs, RR ×4.** Each replay is re-run from a temp copy, and its md5 equals both the committed file and the
  recorded value.

## Apply (FABLE)

[`apply.py`](apply.py), dry run → [`apply_dryrun.out`](apply_dryrun.out): E1 PASS, anchored once, **FAILS 0**.
- The page is **clean** in the shared tree.
- `apply.py` refuses `--apply` on a dirty page, keeps CRLF/LF, and is idempotent.

**Contract owner:**
- FABLE authored it (`361c6b228`, 2026-09-22) and added the rule table (`a089d9a48`, 2026-09-25).
- OPUS ran falsification pass 1 (`abc1a9b94`) and made the WE-2 correction (`56d353a3a`).
- The front matter names no lead.

**Noticed, not drafted (FABLE's own, a follow-up):** §14 still lists "The step table and the ranged-weapon recipes,
S-22's other two uncontracted pages", but both are contracted (`8854f5fb9`, `2f6354549`).

## Consumer check (FABLE)

affected: Database/FFXII TZA/08-Combat-Formula/CONTRACT-environmental-element-scaling.md

- consumer: 08-Combat-Formula/CONTRACT-environmental-element-scaling.md §13: revised-here
- consumer: 08-Combat-Formula/CONTRACT-environmental-element-scaling.md WE-2 ("an environment rule and a terrain rule for the same element share one multiply", OPUS 10-02): agrees (S1 at the bytes, S2 in the record)
- consumer: _index/L2-VERDICTS.md S-22 row, runtime cell ("WE-1 stage order executed"; WE-2's shared multiply is recorded, not asserted; `we1.py`'s `+0x13` reads 0): routed-to-SWE2-DATA
- consumer: _index/candidates/auditspec-l2-expansion-1003/item4.md S-22 WE-2 row ("DATA to check whether a replay case drives the shared multiply"): routed-to-SWE2-DATA (answered here: driven and recorded, cells listed)
- consumer: _index/candidates/s22-opus-replay-steps-and-element-scaling/README.md "What the execution adds" item 1 ("WE-2's 'three independent inputs, multiplied in sequence' holds"), which its own table contradicts at the shared cells: routed-to-OPUS
- consumer: _index/candidates/auditspec-l2-sample-1003/README.md SF-3 (`we1.py` reads a zero `+0x13`) and SF-4a (§13 "None"): agrees

run: check_s22_envscaling.py at 1e18553b0 (FAILS 0, 16 PASS: bytes, record, controls C1/C2, four replay re-runs); apply.py dry run at 1e18553b0 (FAILS 0)
