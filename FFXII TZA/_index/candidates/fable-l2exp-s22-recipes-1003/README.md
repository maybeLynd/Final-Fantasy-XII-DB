# S-22 weapon recipes: the stale §13 (FABLE, 2026-10-03)

*FABLE, on SWE2-AUDIT-SPEC's L2 expansion ([`auditspec-l2-expansion-1003`](../auditspec-l2-expansion-1003/README.md):
the stale §13s, carried from the sample's SF-4a). STAGED: this package edits no tracked file, and `apply.py` was run as
a dry run only. It is one of three S-22 packages; the step-table package
[`fable-l2exp-s22-1003`](../fable-l2exp-s22-1003/README.md) carries ST-4.*

## Finding (FABLE)

**The audit is right.** §13 of `CONTRACT-weapon-recipes.md` reads "**None.** No experiment executes this resolver".
The contract's own RW-2 text already cites OPUS block 316 as having executed the cut-short ("on OPUS block 316, which
executed it"), so the page contradicts itself.

I re-ran both packages from temp copies at HEAD under unicorn 2.1.4. Every result file reproduced byte-identically:
`a226db98…` (`check.py`), `5680857b…` (`we1.py`) and `867bbaf3…` (severe-weather gate).

**At the bytes:** the replay hooks `003863D0`, `call [rbx+rax*8+0x1DDA5C0]`. That site lies in the resolver
`00385F60`, whose chained `.pdata` runs `00385F60-003860B2`, `003860B2-00386225`, `00386225-00386242` and
`00386242-0038685E`. Every entry chains to `00385F60`.

**What each package asserts, read from the records:**

- **`s22-opus-replay-recipe-resolver` (09-25):**
  - RW-1 and the decode of RW-2/RW-4 are static, read from the mapped image.
  - **The RW-2 committed-list-only case is asserted.** Recipe 39 calls no step, and 74, 90, 5 and 4 call exactly
    their second lists.
  - **The cut-short is recorded, not asserted.** The case is a literal `True`, which is DATA's RW-2 point. The
    record shows recipe 6 calling `[3, 4]` of 7 slots and recipe 2 calling `[20, 30, 32, 40]` of 5, each stopping
    at the first `[02AEDFB8] = 1`. `check_s22_recipes.py` asserts that from the record, for every completed run.
  - **Recipe 25 (bow) is not covered.** It stops in its first committed slot, 29, at an unplanted read of `0x1C`, so
    no weapon family's committed run executes.
- **`s22-opus-replay-severe-weather-gate` (09-26) asserts RW-5 on steps 35/36.** With `+0x1A` bit `0x04` clear and
  class 2, a hit chance of 100 becomes 80 and 50. Every other combination leaves it unchanged, and no other bit of
  `+0x18..+0x1B` gates it.

**Static only:**
- the skip-entirely arm (`00386249`–`003862AE`);
- the recipe taken from the equipped item (`0038618B`–`00386210`);
- the effects of the post-loop `00390F20`.

## Staged edit (FABLE)

There is one strike-and-replace, **E1**, on §13. It strikes the whole "**None.** … *Stated rather than left blank …*"
paragraph and replaces it with:
- the evidence class;
- both packages with their dates and md5s;
- what is asserted: RW-2's committed-list rule and RW-5;
- what is recorded only: the cut-short, now asserted from the record by this package's check;
- what is not covered: recipe 25 and every weapon family's committed run;
- what is static: the skip arm, the equipped-item recipe and `00390F20`;
- the package's addressing note on "merged bit 2". That bit is byte `+0x1A` bit `0x04`, which is bit 18 of a dword
  at `+0x18`.

It closes with "Nothing here has been observed in a running game", followed by the stamp. The exact strings are in
[`edits.json`](edits.json).

## Check (FABLE)

[`check_s22_recipes.py`](check_s22_recipes.py) → [`check_s22_recipes.out`](check_s22_recipes.out): **12 PASS,
FAILS 0**.

- **S1:** the hook site lies in the resolver's chained `.pdata`.
- **The record.**
  - R1: RW-1 and the RW-2/RW-4 decode (static).
  - R2: the committed-list case is asserted in the package.
  - R3: asserted here, every completed run calls its second list up to the first step that sets the flag.
  - R4: the package's early-exit case is a literal pass.
  - R5: recipe 25 is not covered.
  - R6: RW-5's six conditions per step.
- **Controls.**
  - **C1 (sensitivity, stale text).** "No experiment executes this resolver" is FALSE: steps are called through
    `003863D0` in 7 of 8 recorded cases.
  - **C2 (sensitivity, reading).** "The committed path runs every slot" predicts the full list for recipes 6 and 2,
    and it is FALSE: 2 of 7 and 4 of 5.
- **Re-runs, RR ×3.** Each replay is re-run from a temp copy, and its md5 equals both the committed file and the
  recorded value.

## Apply (FABLE)

[`apply.py`](apply.py), dry run → [`apply_dryrun.out`](apply_dryrun.out): E1 PASS, anchored once, **FAILS 0**.
- The page is **clean** in the shared tree.
- `apply.py` refuses `--apply` on a dirty page, keeps CRLF/LF, and is idempotent.

**Contract owner:**
- FABLE authored it (`2f6354549`, 2026-09-22) and added the 09-25 cut-short paragraph.
- OPUS ran falsification pass 1 (`abc1a9b94`) and made the 10-02 RW-2 correction.
- The front matter names no lead.

## Consumer check (FABLE)

affected: Database/FFXII TZA/08-Combat-Formula/CONTRACT-weapon-recipes.md

- consumer: 08-Combat-Formula/CONTRACT-weapon-recipes.md §13: revised-here
- consumer: 08-Combat-Formula/CONTRACT-weapon-recipes.md RW-2 cut-short paragraph ("on OPUS block 316, which executed it"): agrees
- consumer: _index/L2-VERDICTS.md S-22 row, runtime cell ("RW-5 gate … executed"; the `loop_early_exit_observed` case is a literal pass): routed-to-SWE2-DATA
- consumer: _index/candidates/s22-opus-replay-recipe-resolver/README.md ("`CONTRACT-weapon-recipes.md` §13 reads 'None'", a dated premise; the early-exit case should become an assertion, as item 4 says): routed-to-OPUS
- consumer: _index/candidates/auditspec-l2-sample-1003/README.md SF-4a: agrees

run: check_s22_recipes.py at 1e18553b0 (FAILS 0, 12 PASS: bytes, record, controls C1/C2, three replay re-runs); apply.py dry run at 1e18553b0 (FAILS 0)
