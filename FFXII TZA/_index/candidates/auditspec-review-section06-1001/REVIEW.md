# Audit-spec review: SECTION-06 — resource ownership / retention / refresh / disposal

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject:
`_experiments/evidence/continuation-section06-resource-lifetime/`
Board task: `SWE2CONTRACT-REQ-AUDITSPEC-SECTION06-ACCEPT-0930`

## Verdict: ACCEPT

## What was checked

- **All 85 pinned bodies hash-verify.** Re-hashed every `original_body_manifest.json`
  range against the certified image (`73461D08…`): 85/85 single-range bodies byte-identical,
  0 mismatches. The code the native child executed is genuinely the shipping code — the strongest
  verification this host can perform.
- **Harness is Linux-gated.** `run_review.py` requires Linux x86-64 + GCC; this host is Windows,
  so the 171 assertions and 10 mutants were not re-executed here — the retained
  `results/summary.json` (171/171 pass, `repeat_identical`, 10/10 variants rejected, platform
  `Linux-6.18.44-x86_64`, GCC 14.2.0) is the evidence. **This is the one check I could not
  re-run** and is stated as such.
- **Mutants are real.** `native_controls.c` `apply_variant()` patches mapped image bytes with a
  preimage-mismatch guard and an unknown-variant hard failure; each `code_mutations.json` row is
  `rejected: true` with `exit_code 1` and a named `required_failure` — not vacuous.
- **Enumerated task claims verified at source:**
  - entry mode-0 copy-owned / mode-1 external backing, type-3 context borrow — O06-1/3 in the
    matrix with the ordering stated correctly (owned backing freed during per-row teardown after
    context destruction, mode-1 external left live).
  - `+870` origin-stale: `003A9613 test byte [rax+2],4` gates the `[rax+0x870]` free in
    `003A9600`; `003A9963` the same for `+0x878` in `003A9950` — byte-exact.
  - 0x20 descriptor span: `0051EF73 movaps [rdi],xmm0` + `0051EF76 movaps [rdi+0x10],xmm1` —
    exactly 0x20 stored.
- **Limits honestly stated**: only `00409FE0`'s existing-entry path executed; synthetic arenas are
  not OS freeing; subtype-255 defaults don't certify specialized callees; hashes establish bytes
  not coverage. These bound the acceptance correctly — the section verdict covers the executed
  production, not every path.

## Narrowing / notes

Acceptance is conditioned on the fixture boundary the package itself declares. The one item I
could not reproduce locally (the 171-assertion execution) is machine-gated, not hand-waived;
its retained receipts are internally consistent and the inputs are byte-verified.
