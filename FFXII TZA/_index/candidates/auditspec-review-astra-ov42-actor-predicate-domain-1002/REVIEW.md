# SWE2-AUDIT-SPEC review: ASTRA OV-42 actor predicate domain

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session) · 2026-10-03 ·
Task: `ASTRA-REQ-SPEC-OV42-ACTOR-PREDICATE-DOMAIN-1002` · Package: `_experiments/evidence/ov42-actor-predicate-domain/`
(publisher commit `2b341ca3a`), image pin `73461d08…21f8`.

## SWE2-AUDIT-SPEC verdict: ACCEPT

Scoped as written. A normal zero return implies class-20 acceptance of the low-16 ID. With an initialized, stable
count of 543 that bounds the ID to 0..542, which still includes 511..534. It is not a zero-return feasibility proof.

## SWE2-AUDIT-SPEC re-derivation from the shipping image

- `002FFCF0` (`BattleAction_CheckActionAvailabilityReason`) does `movzx ebx,cx` and later `r14d = bx`. It calls
  `322C50(ecx = r8+13h = 14h, edx = r14d)` with `r8d=1` (`002FFD75..002FFD8B`). A zero result returns 4, so every
  later zero return has passed the class-20 check.
- `00322C50` class 20: the image-base-relative table at `00323054`, index 19, decoded from the image, gives
  `00322F72`.
  - That arm reads only `[02EBF138]+4` (the count), with lower bound 0, and accepts `0 <= id <= count-1`
    (`0032302E..0032303B`).
  - It never reads R8.
- RDI is loaded once as `q[unit+698h]` (`002FFD05`) and passed unchanged as RDX to `306480` (`002FFE97`).
- The category byte `[rdi+5]` (`002FFDAE`) belongs to that same record.

## SWE2-AUDIT-SPEC reproduction (disposable copy, repository-root cwd)

- `prove.py` (proof-03) re-run: exit 0, stdout identical, output **byte-identical** to `result-02.json`.
- `control.py` re-run: exit 0. The three CLI refusals (missing CFG, wrong CFG interface, missing class contract)
  are identical, each with its result absent.

Other classes, natural queue, all writers, loader/IO, owner and whole-OV42 stay OPEN.
