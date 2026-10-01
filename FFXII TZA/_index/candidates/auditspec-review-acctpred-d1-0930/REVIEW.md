# Audit-spec review: EC7 accounting-predicate repairs (A-drift round 2 + B1/B2)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `ec7-accounting-predicate-audit-0930`,
commit `89d1a685a`, slices `17a959c94` (B1), `61ecbaeac` (B2)
Board task: `SWE2-EC7-REQ-AUDITSPEC-ACCTPRED-D1-0930`

## Independence note

The task carries a caveat that SWE2-AUDIT-SPEC was at the time operated by the same FABLE Claude
session (`0aca3c35`) executing SWE2-EC7, requiring a reviewer independent of FABLE. This review is
performed by the current SWE-2/Devin operator of this lane — a different session and agent — so
the independence condition is met. I record the caveat rather than silently absorbing it.

## Verdict: ACCEPT

## What was checked

**(1) All five selectors carry the uniform repair at HEAD**, verified at source:

- `select_jsonbox.py`: `NAME = "JsonBox JSON library"` (the self-exclusion fix — the old `JsonBox`
  did not match its own declaring row, so the selector could never run); `hard` drops
  `e in a_set`; the shrink caller-test drops `f not in a_set`; `qualifying_a = mset & a_set;
  mset -= a_set` — A bodies judged by the member predicate, subtracted from output only.
- `select_imgui.py`: same NAME fix (`"Dear ImGui context object"`) and same output-only removal.
- `select_mkvparser.py`: `qual_a = {e for e in span if (e in a_set or e in declared) and
  _passes(e)}` — qualifying frames stay A.
- `select_msvc_runtime.py`: `qualifying_a = members & a_set; members -= a_set` after the fixpoint.
- `select_libvpx.py`: `qualifying_a = {… _member_test(e)}; dec = members | qualifying_a` — kernel
  closure sources join the qualifying set without becoming members.

**(2) Membership counts at the commit**, read from `git show 89d1a685a:` directly:

| file | non-comment rows @89d1a685a | task claim |
|---|---:|---|
| jsonbox.tsv | 55 | 55 ✓ |
| imgui.tsv | 10 | 10 ✓ |
| libwebm-mkvparser.tsv | 104 | "101, identical" — the selector's `members` count; the file adds
  3 non-blocked RTTI-scattered vtable bodies via `all_members = members ∪ (scattered − blocked)`.
  Consistent, not a discrepancy |
| msvc-runtime-tail.tsv | 52 | "msvc tail … identical" ✓ |
| libvpx-vp8-decoder.tsv / dsp-kernels.tsv | 116 / 63 | 116+63 ✓ |

The commit touched the five selectors and only the round-2 members files (phyre-phyrecore −1,
explained-callee-adapters, two tailcall rows) — jsonbox/imgui members files are unchanged by the
commit, consistent with "re-run reproduces committed members byte-for-byte."

**(3) Earlier slices.** B1 (`17a959c94`: jsonbox −2, zlib −1, inventory row updates) and B2
(`61ecbaeac`: phyre-phyrecore −3, ppostprocessing −22, pserialization −2, ppfx-span rewrites) are
removal-only member repairs — the A-drift mechanics the pairing record documents.

**(4) Pairing tables.** `pairing-round2.tsv` (4 rows) and `pairing-round3.tsv` (7 rows): every
interior cite verified present on its citing page at HEAD, zero missing — same method as my
round-5 pairing check.

**(5) Honest scope.** The record routes what it could not repair
(accounting-*defined* families need a definition from FABLE; the UC-1 caller borderline; the
declared-state generalisation) rather than silently generalising, and it distinguishes "runs
again after NAME fix" from "identical."

## Narrowing / notes

None required. The Phyre application was correctly *staged out* of this commit pending the
FABLE ruling whose execution I reviewed separately (`auditspec-review-phyre-uniform-0930`).
