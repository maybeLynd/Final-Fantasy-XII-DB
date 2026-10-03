# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-static-initialization-order-and-injectio-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-STATIC-INITIALIZATION-ORDER-AND-INJEC-ADAB7` · Package: `_index/candidates/opus-static-initialization-order-and-injectio-ee-1003/` · Page: `24-Compiler-And-CRT-Runtime/Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 1 row(s), 5 anchors. **Every row** read clause by clause against raw capstone output of the whole body in the certified image (SHA256 73461D08...); every relative call resolved:
  - `00808C90` exact: CRT thunks resolved from the PE import table - `0086200A` _set_app_type, `0086202E` _set_fmode, `0086204C` __p__commode, `00861FE0` _configure_narrow_argv, `00862010` __setusermatherr, `00862040` _configthreadlocale, `00861FE6` _initialize_narrow_environment; the `00808988(1)` al test to `0080996C(7)`; the non-zero `_configure_narrow_argv` path to `00808D40 mov ecx, 7`; the two `0016D6A0` calls with no argument set up; 0 returned.
- Limits hold: body statements only, static evidence; the draft and OPUS's re-read are not independent review, this record is.
