# SWE2-AUDIT-SPEC review: ASTRA OV-16 actor-directory kind proof (asp_a03 actor 25)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session) · 2026-10-03 ·
Task: `ASTRA-REQ-SPEC-OV16-ACTOR-KIND-1002` · Package: `_experiments/evidence/actor-directory-kind-proof/`
(publisher commit `317ebd1b8`), image pin `73461d08…21f8`.

## SWE2-AUDIT-SPEC verdict: ACCEPT

The counts and the ordinal select the row. The scriptType label does not. This closes the unread source/data
premise only.

## SWE2-AUDIT-SPEC re-derivation

**Data**, read independently from the retained `asp_a03-US-original-01.ebp` (80,000 bytes, section at +80h):

- The type-count table at section `+730h` is the WORD count 8, then the WORDs 9, 11, 0, 0, 0, 4, 72, 0.
- The prefix sums 9 / 20 / 20 / 20 / 20 / 24 / 96 put row 6 at ordinals 24..95.
- The directory entry for actor 25 is at section `+D2A4h` = `CDF0h + 4 + 48×25`, so version 11 uses stride 48.
- Its WORD `+4` is 6.

**Code:**

- `00266BD0` selects on `byte +3 & 1Fh` through the table at `00266C30`, decoded from the image.
  - Rows 5 and 6 reach `00266C0E`, which writes `dword [+1Ch] = 30004h` (`00266C12`), setting bits 2, 16 and 17.
  - Row 7 writes `34C85h`.
- The stamped byte for row 6 / kind 3 is `66h`: low 5 bits 6, top 3 bits 3.
- The six later direct initializer masks listed in `result-02.json` (`FFFFDEFF`, `|4`, `&~4`, `|400h`, `&~4`,
  `&~400h`) all preserve bits 16 and 17.

## SWE2-AUDIT-SPEC reproduction (disposable copy, repository-root cwd)

- `prove.py` (prove-03, `01096b3d`) re-run: exit 0, output **byte-identical** to `result-02.json`.
- control-02 (`control.py`, `b471d875`) re-run: `control-result-02.json` **byte-identical**.
- control-01 (`history/control-01-before-coherent-store-mutation.py`) re-runs to exit 1, as recorded. It is
  retained without PASS credit.

Transitive callbacks, the tail `266ACA → 3DB280`, final live flags, natural scene timing, cancel/reentry and
whole-OV16 stay OPEN.
