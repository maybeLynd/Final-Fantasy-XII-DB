# SWE2-AUDIT-SPEC review: ASTRA OV-42 sequence-queue source

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session) · 2026-10-03 ·
Task: `ASTRA-REQ-SPEC-OV42-SEQUENCE-QUEUE-1002` · Package: `_experiments/evidence/ov42-sequence-queue-source/`
(publisher commit `0c4215736`), image pin `73461d08…21f8`.

## SWE2-AUDIT-SPEC verdict: ACCEPT

`003068D4` does **not** locally exclude 511..534. Under a coherent row, base and stride, the supplied IDs 511 and 534
compute 303 and 326.

## SWE2-AUDIT-SPEC re-derivation from the shipping image

- **`00306760`:** incoming RDX goes to RDI (`00306775`). The six-arm switch on `022C215C`-1 (table `00306AF0`,
  decoded) sends only kind 4 (`00306848`) to the queue store.
- **Kind-4 path** (sweep: no `edi` write before `003068A7`):
  - `20E600([02EBF138]+0Ch)` gives the base, then `sub edi,eax` (low32 mod 2³²).
  - The divisor is `movzx word [02EBF138]+8`, read a second time from the descriptor. It is unsigned and there
    is no zero-divisor guard.
  - `div ecx` gives the full quotient. Then the `AX == FFFFh` test gives -1; otherwise `movzx ax` and `-208`.
  - The result is stored at `003068D4` into `022C2178`.
- **Arithmetic:** 511−208 = 303 and 534−208 = 326. No equality between the construction and queue bindings is
  assumed.

## SWE2-AUDIT-SPEC reproduction (disposable copy, repository-root cwd)

- `prove.py` (prove-04, `b07bf14e`) re-run: exit 0, output **byte-identical** to `result-03.json`.
- control-02 (`control.py`, `f4be90ac`) re-run: `control-result-01.json` **byte-identical**. Its four CLI refusals
  are failed extent with output present, failed capture exit, missing data status and missing table data.
- control-01 (history driver) re-runs to exit 1, as recorded, with no credit.

Kind-to-row, caller and owner coherence, native effects, descriptor binding, scheduling, lifetime and the natural
queue stay OPEN. This is consistent with the separately reviewed quotient-bound packet (`5cf0bc196`).
