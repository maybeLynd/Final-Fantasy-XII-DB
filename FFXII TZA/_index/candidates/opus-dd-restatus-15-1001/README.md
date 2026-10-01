# DD owner re-status, batch 15: the input-stack and text-element pages to DOCUMENTED, A-drift paired (OPUS, 2026-10-01)

SD-7 and SD-107 were restated ANSWERED in the register on 2026-10-01: OPUS applied `restate_gr_batch.py` for SWE2-DATA
while FABLE is inactive, as the user authorized. OPUS then ticked the two page boxes for SWE2-DATA, citing record
`sd7-sd107-closure-0930` (`59ec09a95`). SWE2-CONTRACT's DD batch 19 (`48557d9d2`) had already carried each page's residue
prose. `documented_rule.py` gives **TALLY READY=2 of 2** ([`documented_rule.out`](documented_rule.out)).

## Applied (OPUS)

| page | status |
|---|---|
| `15-Input/Input-Stack/input-stack-device-channel-and-bindings.md` | PARTIAL -> DOCUMENTED |
| `99-Unresolved-Residual/Glyph-Run-Rendering/the-text-element-dispatch-table.md` | PARTIAL -> DOCUMENTED |

Only the front-matter status line changes, plus the two ticked boxes. Neither page is REOPENED, so the falsification-pass
condition does not apply.

## A-drift, paired in the same publish (OPUS)

`adrift_report.py` named three refused rows after the edit. `exact_remove.py` from EC7's pairing record took out the
four A members, and the dated row notes come from `round6_notes.py`:
- SQEX SEAD sound library span: 1123 -> 1122, `007E73F0`, made A by the text-element page `@007E7401`.
- PPFX post-effect library: 1600 -> 1598, `0077FFE0` (`@00780079`) and `00780590` (`@00780729`), made A by the
  text-element page.
- NativeAdapter.DoubleCallResultTailCallSavedThis: 4 -> 3, `001E09B0`, made A by the input-stack page `@001E09B9`.

The removals were applied on the live tree, whose family files were clean. The SEAD and PPFX selectors were not re-run
(round 5 showed `select_ppfx.py` reproducing exact removal); that check is routed to SWE2-EC7. After the removals,
`adrift_report.py` reports 0 refused rows.

run: documented_rule.py READY 2 of 2; adrift_report.py refused rows 0 (FAILS 0)

## Review (OPUS)

The owner read goes to SWE2-AUDIT-SPEC. The pairing is noted to SWE2-EC7.
