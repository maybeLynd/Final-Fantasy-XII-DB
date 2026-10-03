# S-22 step table: ST-4's "ONLY channel" and the stale §13 (FABLE, 2026-10-03)

*FABLE, on SWE2-AUDIT-SPEC's L2 expansion ([`auditspec-l2-expansion-1003`](../auditspec-l2-expansion-1003/README.md),
"Repair requests filed": FABLE gets "S-22 ST-4 / WE-2", with stale §13s as SF-4a). The defect is from the sample
([`auditspec-l2-sample-1003`](../auditspec-l2-sample-1003/README.md), S-22 row 3, and SF-4a). STAGED: this package
edits no tracked file, and `apply.py` was run as a dry run only.*

This is one of three S-22 packages, one per contract:
- this one: `CONTRACT-formula-step-table.md`, covering ST-4 and §13;
- [`fable-l2exp-s22-envscaling-1003`](../fable-l2exp-s22-envscaling-1003/README.md): the environmental element scaling
  §13;
- [`fable-l2exp-s22-recipes-1003`](../fable-l2exp-s22-recipes-1003/README.md): the weapon recipes §13.

## Finding 1, ST-4 (FABLE)

**Verified at the bytes and by execution. The audit is right.** §3 calls `02AEE054`/`58`/`5C` "the ONLY channel
between steps". ST-4 says the steps "communicate only through the scratch record", and §5 makes that record "the
three scratch words". In fact:

- **Slot 21 (`00388F20`) writes the hit chance `02AEDFE0`.** It stores at `00388F37` (constant 100 when context
  `+0x1C` bit 2 is set) and at `00388FA1` (row `+0x12` − target `+0x2C` + source `+0x2B`).
- **Slot 40 (`00389670`) reads that cell.** At `0038968D` it compares it with its MT19937 draw mod 100. On a miss it
  sets `02AEDFBC` (`00389696`) and `02AEDFB8` (`003896A0`), and the loop stops at `003863D7`.
- **`02AEDFE0` is `BattleFormulaScratch +0x28 hitChance`.** The store declares the record at `02AEDFB8`, 0xA8 bytes
  long, and the three words are its `+0x9C`/`+0xA0`/`+0xA4`.
- **A census of the 152 target bodies, own bodies only and callees not followed, finds 15 cross-step cells.** Each
  is written by one step and read by a different step, and 12 of them lie outside the three words: `+00 +0C +10 +14
  +18 +20 +24 +28 +30 +34 +38 +3C`. **No cell outside the block** passes between step bodies.
- **Executed.** Under unicorn 2.1.4 the shipped bytes run at their own addresses with no stub; MT19937 runs for real
  from its lazy 5489 seed. In both runs the three words are 0 before slot 40.
  - Slot 40 alone ends the recipe (`rollOver` 1, `failed` 1).
  - Slot 21 then slot 40 does not (`rollOver` 0).
  - So a hand-off outside the three words changes the outcome.

**What stands.**
- "No arguments and no return values" is right in the sense the contract needs. The loop reloads the same three
  arguments before every call (`003863C5`–`003863CD`), and `rax` is overwritten (`003863C0`) or unread on the exit
  path (`003863E8`–`003863F8`).
- "One shared scratch record" in the front matter and the preamble stands once the record is the 0xA8 block.
- The ORDER-is-semantics conclusion stands, and is stronger for it.

## Finding 2, §13 (FABLE)

**The audit is right: §13 reads "None. No experiment executes this dispatch", and three recorded replays execute
it.** I re-ran all three OPUS packages from temp copies at HEAD under unicorn 2.1.4 (`C:\Python314`). Every result
file reproduced byte-identically:

| package | result | md5 |
|---|---|---|
| `s22-opus-replay-steps-and-element-scaling` (09-25) | 9/9 | `result.json` `99336e05…` |
| `s22-opus-replay-recipe-resolver` (09-25) | `check.py` | `result.json` `a226db98…` |
| `s22-opus-replay-recipe-resolver` (09-26) | `we1.py` 4/4 | `we1_result.json` `5680857b…` |
| `s22-opus-replay-severe-weather-gate` (09-26) | 5/5 | `result.json` `867bbaf3…` |

The new §13 cites each package for what it asserts and marks two things as recorded only: the early stop, and the
slot-21 → slot-40 order in recipe 14. It names the corrected ST-4's hand-off as executed only in this package's
isolated check, and says plainly that no package pins unicorn and nothing has been observed in a running game.

## Staged edits (FABLE)

There are five strike-and-replace edits; [`edits.json`](edits.json) holds the exact strings. Each OLD string occurs
exactly once at HEAD.

| id | where | struck | replaced by |
|---|---|---|---|
| E1 | §3 types fence | "the shared scratch record — the ONLY channel between steps (ST-4)" | the three words as `+0x9C/+0xA0/+0xA4` of `BattleFormulaScratch` `02AEDFB8` (0xA8), "one of 15 cross-step cells of the block, not the only one" |
| E2 | ST-4's bold lead | "The steps share NO arguments and NO return values; they communicate only through the scratch record, so the ORDER in the recipe is the semantics." | no argument or return value hands over (the loop's reload, `rax` unread); the channel is the whole block; the census figure; the slot 21 → slot 40 example with addresses |
| E3 | §5 | "the three scratch words (`ST-4`)" | the block, with the three words as its preparation-to-finalize part, plus `02AEDFE0` and `02AEDFB8` |
| E4 | §7 | "There is no other channel and no return path (`ST-4`)." | no return path; the channel is the block; `02AEDFB8 == 1` ends the list at `003863D7` |
| E5 | §13 | the whole "**None.** …" paragraph | the replay record above, with evidence class, dates, md5s, what is asserted, what is recorded only, and what is static |

The falsification-pass F3 row ("ST-4 survives") is a dated record of what that pass tested, which was the 60–79
band's writes. It is left as written.

## Check (FABLE)

[`check_s22.py`](check_s22.py) → [`check_s22.out`](check_s22.out): **22 PASS, FAILS 0**.

- **Static.**
  - S1: the table slots.
  - S2 ×5: the instruction forms at the five sites.
  - S3: the loop's argument reload; `rax` is overwritten or unread.
  - S4, S5: the store's record and its fields.
- **Census.** N0 (152 targets), N1 (15 / 12), N2 (`+0x28` and `+0x00` among them), N3 (nothing outside the
  block).
- **Executed.** X1 (slot 21 writes 100), X2 (the three words are equal before slot 40 in both runs), X3 (the
  outcome differs).
- **Controls.**
  - **C1 (sensitivity).** The old reading predicts the same slot-40 outcome with or without slot 21. That
    prediction comes out FALSE, `(0, 0)` vs `(1, 1)`.
  - **C2 (positive).** The census finds the three words themselves.
- **Re-runs, RR ×4.** Each replay is re-run from a temp copy, and its md5 equals both the committed file and the
  recorded value.

## Apply (FABLE)

[`apply.py`](apply.py), dry run → [`apply_dryrun.out`](apply_dryrun.out): E1–E5 PASS, each anchored once,
**FAILS 0**.
- The page is **clean** in the shared tree, so the dry run read the working tree.
- `apply.py` refuses `--apply` on a dirty page, keeps CRLF/LF, and is idempotent. This was tested on a scratch copy:
  the second run reported SKIP ×5.

**Contract owner:**
- FABLE authored it (`8854f5fb9`, 2026-09-22).
- OPUS ran falsification pass 1 (`28b695117`) and made the 10-01/10-02 corrections.
- The front matter names no lead.

**Noticed, not drafted (FABLE's own, a follow-up):** §6 still lists "the ranged-weapon recipe page — S-22's fourth,
not claimed here" as uncontracted, but `CONTRACT-weapon-recipes.md` exists (`2f6354549`).

## Consumer check (FABLE)

affected: Database/FFXII TZA/08-Combat-Formula/CONTRACT-formula-step-table.md

- consumer: 08-Combat-Formula/CONTRACT-formula-step-table.md §3, ST-4, §5, §7, §13: revised-here
- consumer: 08-Combat-Formula/CONTRACT-formula-step-table.md front matter `contract:` and preamble ("communicate only through one shared scratch record"): agrees (the record is the 0xA8 block; N3 finds no cross-step cell outside it)
- consumer: 08-Combat-Formula/CONTRACT-preparation-step-family.md L119 and L449 ("the three scratch words, and nothing else", said of the sixteen 60–79 members' writes): agrees
- consumer: _index/PARITY-STATUS.md L708 (the preparation members write only the three words): agrees
- consumer: 08-Combat-Formula/Step-Table/combat-formula-step-table.md §3 L328 (`02AEE054`–`5C` as "the shared scratch record the steps read and write"): routed-to-FABLE
- consumer: _index/L2-VERDICTS.md S-22 row, runtime cell ("ST-1/2/6 static-ruled"; the corrected ST-4's hand-off is executed only in this package's isolated check): routed-to-SWE2-DATA
- consumer: _index/candidates/auditspec-l2-sample-1003/README.md S-22 row 3 (ST-4 false at `00388FA1`/`0038968D`): agrees
- consumer: _index/candidates/s22-opus-replay-steps-and-element-scaling/README.md ("`CONTRACT-formula-step-table.md` §13 … read 'None'", a dated premise): agrees

run: check_s22.py at 1e18553b0 (FAILS 0, 22 PASS: static, census, unicorn 2.1.4 execution, controls C1/C2, four replay re-runs); apply.py dry run at 1e18553b0 (FAILS 0)
