# SWE2-AUDIT-SPEC review: ASTRA OV-42 kind/row coherence

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE) · 2026-10-03 ·
Task: `ASTRA-REQ-SPEC-OV42-KIND-ROW-1002` · Package: `_experiments/evidence/ov42-kind-row-coherence/`
(publisher commit `d83287255`), image pin `73461d08…21f8`.

## SWE2-AUDIT-SPEC verdict: ACCEPT

Scoped as written, including ASTRA's own METHOD CORRECTION: the 145-byte suffix `306C5B..306CEC` was already retained
in committed `autoattack-commit-exception/retained/current-row-source-01.json`. The new capture is redundant
coverage, not a new sample. The formula and invariant analysis stand.

## SWE2-AUDIT-SPEC re-derivation from the shipping image

- **`00306BD0`:**
  - Unsigned `div` gives the full 32-bit quotient q (`00306C82`). Then `add eax,-94h / cmp eax,7Fh / ja` (unsigned).
  - The selector bytes at `00306D08` (128 bytes) pick from the 7-entry jump table at `00306CEC`. Both were decoded
    from the image:
    - q 148 → 5;
    - q 149 → 6;
    - q 150..181 and 226..261 → 7;
    - q 182..207 → 3 (default `ebx=3`);
    - **q 208..225 → 4**;
    - q 262..274 → 1;
    - q 275 → 2;
    - everything outside 148..275 → 7.
  - So kind 4 ⇔ q ∈ 208..225. The kind is published to `022C215C` (`00306CDB`).
  - `32FC30`'s RAX is not tested before `32ED70` (`00306C56`→`00306C5B`).
- **Composition with the queue:** the queue uses the low-16 quotient minus 208. If dispatch still uses the published
  kind 4 and the two quotients agree, the queue DWORD is 0..17. Equal row low32, base low32 and positive WORD divisor
  suffice; pointer identity is neither needed nor proved.
- **Countermodels:**
  - q = 511 with kind forced to 4 queues 303.
  - q = 65744 classifies as 7 (it is outside 148..275), yet its low 16 bits are 208, which queues 0.
  - These are mathematical models only.

## SWE2-AUDIT-SPEC reproduction (disposable copy, repository-root cwd)

- `prove.py` (prove-02, `f08e0fd2`) re-run: exit 0, output **byte-identical** to `result-02.json`.
- `control.py` (`e0852be1`) re-run: `control-result-01.json` **byte-identical**. That is one portable valid case
  plus four expected prerequisite failures.

Do not call whole-OV42 impossible. The natural caller, row, owner, descriptor, kind persistence, scheduling and
lifetime stay OPEN.
