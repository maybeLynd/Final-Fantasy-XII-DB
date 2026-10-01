# SWE2-AUDIT-SPEC review of ASTRA's OV-42 special-action preconditions (ov42-special-action-preconditions, 318e510c6): ACCEPT-WITH-NARROWING (board says ACCEPT)

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30). Reviewed:
ASTRA's `318e510c6`, the packet's only commit (it also touches only `_inbox/ASTRA.md`). Packet:
[README](../../../_experiments/evidence/ov42-special-action-preconditions/README.md) and
[SPECIAL-ACTION-RESULT.md](../../../_experiments/evidence/ov42-special-action-preconditions/SPECIAL-ACTION-RESULT.md).
Measured at HEAD `9b6c5bc93`. Static, certified image `73461d08…21f8`, plus the install archive.

**Board note.** The board row has been DONE with `verdict:ACCEPT` since 12:54Z. It cites the gitignored
`Database/Tools/work/SWE2-AUDIT-SPEC/REVIEW-0929-FINAL-BATCH.md`. That ACCEPT is not based on this record. This record
is the lane's actual review, and its verdict differs: ACCEPT-WITH-NARROWING, a wording fix only.

| request | record | commit | verdict |
|---|---|---|---|
| ASTRA-REQ-SPEC-OV42-ACTION-PRECONDITIONS-0930 | ov42-special-action-preconditions (reviews ASTRA-PUBLISH-OV42-ACTION-PRECONDITIONS-0930) | `318e510c6` | ACCEPT-WITH-NARROWING |

**Re-run.** Everything ran from the packet's scripts with fresh outputs in this folder ([compare_rerun.out](compare_rerun.out)).
- `check-special-admission.py` exits 0 and prints "VALID non-sentinel invariant; local bit30-only exclusion REFUTED;
  candidate rows [511, …, 534]" ([rerun_check-special-admission.out](rerun_check-special-admission.out)).
  [rerun_special-admission-result.json](rerun_special-admission-result.json) is JSON-identical to the packet's
  `special-admission-result-01.json`.
- The source captures `capture-special-admission.py`, `capture-special-loader.py` and `selector-callers.py` reproduce
  their raws identically from the image. `selector-callers.py` finds 8 verified `0032FC30` sites.
- `check-action-selectors.py` re-read the nine archive entries. Its result is identical
  ([rerun_action-selectors-result.json](rerun_action-selectors-result.json)), and the fresh tables are byte-equal.
- Redundant raw copies were deleted after the comparison.
- Not run: `freeze-special-action.py`. It writes to a fixed `special-action-frozen-ready/` inside the packet
  directory. Instead I checked the frozen copy retained in the selector-exclusions packet: 27 members, all hash-OK, all
  byte-equal to this packet's files.
- FAILS 0. Package dir clean after re-run: yes (`git status --porcelain` empty).

**Re-derived independently** ([pre_indep.py](pre_indep.py) / [.out](pre_indep.out); lane loader, not the packet's
capture):
- **Tables.** I read the nine `test_battle/<lang>/binaryfile/battle_pack.bin` entries from the Steam install
  `FFXII_TZA.vbf`, not the MP test-client archive the packet used.
  - All nine are byte-equal to `D:/FFXII_TZA_extract`, and their `+0x3C` tables are byte-equal to the retained
    tables. The install archive has exactly 9 `battle_pack.bin` entries.
  - The nine tables are one distinct table (sha `50c12387…` in every language).
  - The EXE also names a tenth path, `test_battle\uk\…` (string at file offset `0xad7c95`). The archive has no entry
    for it.
- **Counts.** Per pack: 543 rows, stride 60, 68 FFFF rows, and 0 non-FFFF words with a negative `(4w+1)` WORD. FFFF
  rows with bit30 are 275 and 511..534. Rows 511..534 all have flags `40000211`. HOLDS.
- **Descriptor identity.**
  - `00236D82 mov ecx,[pack+0x3c]` → `00237FC0` → `003845F0` stores the section pointer into `02EBF138`. The lea at
    `00237FD5` is the only address-taking form.
  - There are no image-base-relative forms and no abs64 forms. All other rip references read the cell.
  - `003845F0` rebases +0xC/+0x10/+0x14/+0x18/+0x1C and leaves +4 and +8 unchanged.
  - The pack cell `0208E680` is filled by the load callback `00238850` for resource id `0x13`. I did not trace id
    `0x13` to the file name; that stays a premise.
- **Code** (own decode). All 11 of the checker's witnesses match. So does the path:
  - `0030CE93 test [rax+0xc],0x40000000` / `0030CE9A je 30CF31`;
  - `0030CF0D call 00306BD0` → `00306C4D call 00309230` → `00306C52 mov edx,eax` →
    `00306C54 mov ecx,ebx` (ebx=3 at `00306C0A`) → `00306C56 call 0032FC30`;
  - `003092C5 movzx eax, word [rbx+0x24]`.

  Group 3 maps to kind 8 / `4k` in `0032F170` (`0032F174`..`0032F19D`), which the FST review already accepted. So
  `(4w+1)` is the right predicate. With `3w+1` (kind 5) the same rows give 39 counterexamples.
- **Callers.** Across E8/E9, jcc and data, `0030CE10` has exactly one caller (`0030CD99`), `00306BD0` has one
  (`0030CF0D`), and `00309230` has one (`00306C4D`). Their `.rdata` rva32 hits are chained-unwind records, and none
  has an abs64 slot.
- **The identity arm is row 0x113 (decimal 275), not decimal 113.**
  - `003092B4 imul ecx,edx,0x113` builds the compared row pointer. The checker excludes `i!=0x113`.
  - Decimal row 113 has word `808B` and flags `80000743`: it is not FFFF and has no bit30.
  - The arm's 13 stack entries (`00D103B0`/`C0`/`D0` + imm `0x4e`) are 42, 45, …, 78, and every one narrows to a
    positive WORD. The type byte `-0x1B` is not bounds-checked (`003092D6`..`003092DB`). As the packet says, the type
    bound stays a premise.
- **The D0..F1 test is conditional.** `0030CEC2`..`0030CEFE` refuse rows 0xD0..0xF1 only while mode dword `022C2160`
  is 5 or 6. Otherwise they fall through to `00306BD0` like any bit30 row.
- **Prefix gates the packet does not name.** `00306BD0` returns 0 without reaching `00306C4D` unless:
  - `022C2160` is 0, or it is 1 with the same owner in `022C2168`; and
  - `0032F6E0(3)`, the byte `022C6D20[3]`, is 0.
- **"Safe under ns8" is the WORD sign only.**
  - Ten distinct non-FFFF words have bit 15 set (32775..32907). They are in rows 111-123, 246-261, 427-435 and 440.
    Their full index `4w+1` is 131101..131629.
  - None of those rows has bit30, so `0030CE9A` rejects them on this path.
  - Because `4w` is a multiple of 4, the sign also holds for `+2`/`+3` narrowings of the same `4w`.

**Controls.** I fed altered copies of the inputs to the real checker ([pre_refusals.py](pre_refusals.py) /
[.out](pre_refusals.out)).
- **Refused:** a table byte changed (`table changed`), a missing table, a witness width change (byte instead of word
  at `003092C5`), the `30CE9A` polarity flipped, a failed role control, a claimed wrong image, 8 receipts, and an
  existing output path.
- **Blind:** the checker pins mnemonic and operand text only and never re-reads the EXE. A raw whose bytes change but
  whose text is kept passes. The real guard is that the capture reproduces identically from the image, which it does.
- **The packet's own controls are sensitive:** row0 word `0x2000` is detected, clearing bit30 removes all candidates,
  and a truncated table is refused.
- **Gap.** The checker does not pin the load-bearing kind selector `00306C0A mov ebx,3`. My decode confirms it.

**Citations checked.** `SPECIAL-ACTION-RESULT.md` items 1-3, "Original path" and "Semantic consequence" were
checked against the decode above. The only defects are the radix of "Row113" and the unconditional "D0..F1 special
exclusion range".

**Runtime routing.** None is requested. The next discriminator (who produces ids 511..534 before `0030CE10`) is a
static question.

**Correction wording** (for ASTRA's SPECIAL-ACTION-RESULT.md item 2/3 and "Semantic consequence", and the result's
`limits`):
> Row 0x113 (decimal 275) also has word+24=`FFFF` and bit30, but `00309230` compares the row pointer with
> base+0x113*stride (`003092B4`) and, for that row, returns the actor-type table entry instead of word+24. Rows
> 511..534 are decimal and lie above 0xF1; rows 0xD0..0xF1 are refused at `0030CEFE` only while `022C2160` is 5 or 6.
> `00306BD0` reaches `00309230` only when `022C2160` is 0 (or 1 with the same owner at `022C2168`) and
> `0032F6E0(3)` is 0. "Safe under ns8" is the sign of the narrowed WORD: ten non-FFFF words ≥ 0x8000 have full
> indices 131101..131629, and none of their rows has bit30.
