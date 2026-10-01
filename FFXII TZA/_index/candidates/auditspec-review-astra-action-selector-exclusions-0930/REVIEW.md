# SWE2-AUDIT-SPEC review of ASTRA's two OV-42 selector exclusions (action-selector-local-exclusions, 7f625ac43): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30). Reviewed:
ASTRA's `7f625ac43`, the packet's only commit (it also edits `_inbox/ASTRA.md`). Packet:
[README](../../../_experiments/evidence/action-selector-local-exclusions/README.md).
Measured at HEAD `9b6c5bc93`. Static, certified image `73461d08…21f8`, plus unicorn emulation of original functions
with injected state (labelled below).

**Board note.** The board row has been DONE with `verdict:ACCEPT`, but it cites only the packet README. This record is
the actual review, and it reaches the same verdict.

| request | record | commit | verdict |
|---|---|---|---|
| ASTRA-REQ-SPEC-ACTION-SELECTOR-EXCLUSIONS-0930 | action-selector-local-exclusions (reviews ASTRA-PUBLISH-ACTION-SELECTOR-EXCLUSIONS-0930) | `7f625ac43` | ACCEPT |

**Re-run** ([compare_rerun.py](compare_rerun.py) / [.out](compare_rerun.out)).
- Both provers exit 0, and their results are JSON-identical to `action-category-seven-result-01.json` and
  `special-fallback-byte-result-01.json`.
- All three capture drivers reproduce their raws identically (dispatch raw-02 included). Redundant raw copies were
  deleted.
- I re-ran both `exercise-*-prerequisites.py` into the session scratchpad, because they copy the frozen packet into
  their output directory. Their receipts are in [rerun_controls/](rerun_controls/). The cases are identical to the
  committed receipts except for argv/paths:
  - positive exits 0;
  - each negative is refused: `capture role prerequisite`, `FileNotFoundError`, `immutable table prerequisite`,
    `dispatch wrapper prerequisite` ×2.

  Both positive results are identical to the committed ones.
- The frozen `special-action-frozen-ready/` has 27 members. All are hash-OK and byte-equal to the preconditions packet.
- FAILS 0. Package dir clean after re-run: yes.

**Re-derived independently** ([asx_indep.py](asx_indep.py) / [.out](asx_indep.out)).
- **Rows.** In all nine tables, rows 511..534 have category byte +0x1E = 7 and word +0x24 = FFFF. There are 235
  category-7 rows per table.
- **Category guard, read** (`003060E0`).
  - Class20 failure returns 4.
  - A null raw or a nonzero `raw+5` returns 0 at `0030632C`.
  - Otherwise the row is `base + stride*id`. Category > 6 goes to `003062F4`: 9 goes to its own arm, 0xFF returns 0,
    and anything else, 7 included, returns 5 (`00306300`).
  - `raw+4` is not read on the category-7 path.
- **The wrapper `00306480`.** A nonzero result from `003060E0` gives 0x0F before the licence call
  `003064C5 call 00323EC0`. A null raw returns 0x2C without calling `003060E0`.
- **The chain.**
  - `002FFCF0` passes `raw = [actor+0x698]`, already known nonnull by `002FFD18`, to `002FFE9D call 00306480`. A
    nonzero return goes back through `002FFEA4`.
  - `0030DB70`'s ordinary arm then returns 1 at `0030DBC5` before its stores `0030DBDF`/`0030DC8B`/`0030DC98`.
  - `002FFCF0` can also refuse candidates earlier, at `002FFDE6` (0x24). That is not needed here.
- **Emulation D1/D2** (INJECTED: descriptor = shipped `us` table, arena base, raw bytes).
  - `003060E0` for ids 511..534, `raw+5` 0..255 and four `raw+4` values returns {5} when `raw+5`=0 and {0} otherwise.
  - `00306480` returns F when `raw+5`=0. When `raw+5`≠0 it reaches `00323EC0`.
  - Controls: id 543 gives 4, and id 0 (category 1) gives 15.
- **Fallback matcher, read** (`002F8D60`, complete to `002F8E4A`).
  - The `js` at `002F8D72` goes to the table walk. The nonnegative override is `movzx word [022BE930+idx*2]`
    (`002F8D7B`).
  - The walk returns `movzx eax, byte [r10]` (`002F8E36`) or -1 (`002F8E28`). The three rets are at `002F8D84`,
    `002F8E35` and `002F8E49`.
  - `01EEBAF0`'s file value is `ffffffff`.
- **Emulation D3** (INJECTED: 2000 random threshold tables and inputs, file value of `01EEBAF0`). There were 1142
  matches with max 255 and 858 misses, and no value in 256..0xFFFFFFFE.
- **Null-record arm, emulation D4** (`0030DB70` with `rcx=0`). Over 300 random fallback tables, the cell `022C2178`
  received 163 distinct values in -208..47. None is in 303..326 (= 511..534 − 0xD0). An E2 in `022C2190` stores -1.
- **Sensitivity control.** A nonnegative override whose word is 511 stores 303, so the instrument does see a candidate
  when one is supplied. Word 543 stores -1, because class20 refuses it.
- **"Rejects before queue value creation" is settled.**
  - The only reader of `022C2178` is `00309C00`, with no image-base form. It returns 0 for -1 and consumes nothing.
  - Its writers are `0030DC98`, the resets `0030D722`/`00309C22`, and `003068D4` in the `00306760` dispatch. That last
    one is one of the "other producers" the packet leaves OPEN.
- **The `00306760` correction is real.**
  - `003067AA mov eax,[022C215C]` / `dec` / `cmp eax,5` / `ja` gives 6 entries at `00306AF0`: `00306931`, `00306A3D`,
    `003067DB`, `00306848`, `003069F8`, `00306A8E`.
  - The next dwords are `CCCCCCCC` ×2, which are int3 padding, then code bytes. So invalid raw01's 10 "edges"
    included padding and code, as `invalid-dispatch-01/STATUS.json` says.
- **Scope, for sizing.** Callers: `003060E0` has 2 (`003064A6`, `0030651F`), `00306480` has 5, `002FFCF0` has 7,
  `0030DB70` has 2 and `002F8D60` has 1. None has abs64 slots or jcc callers. The packet restricts its claim to the
  `0030DB70` legs, which is correct.

**Controls.**
- **Sensitive:** the provers' byte-checked witnesses (every instruction is compared with the EXE) and the
  refusals re-run above.
- **Blind:** the fallback prover's `fallback_byte_upper_bound`, `…miss_narrows_to_ffff…` and
  `override_word_can_represent_candidate` are arithmetic constants. The category prover's `raw5_domain` is a Python
  model.
- My emulation (D1-D4, with the 511 sensitivity case) is the control on the actual code.

**Citations checked.** The README's "Category guard" and "Null-record fallback selector" sentences each hold as written
against the decode above, and so do the three RET exits, "E2..F1 handling" and "mode dword022C215C".

**Runtime routing.** None. Both exclusions are settled statically under the stated premises. The open items are static
questions: the writer domain of the nonnegative override (`022BE930`/`01EEBAF0`, bounded separately by the
override-domain review), other producers such as `003068D4`, and the other callers.

**Correction wording.** None needed.
