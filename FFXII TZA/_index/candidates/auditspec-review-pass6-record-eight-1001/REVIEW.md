# Audit-spec review: the eight pass-6 signatures recorded (SWE2-AUDIT-SPEC, 2026-10-02)

Task: `OPUS-REQ-AUDITSPEC-RECORD-EIGHT-PASS6-SIGNATURES-1001` · Commit under review: `ea843abb8`
(context: `dispositions.py` now requires a signed `check_banned_evidence` row to name a durable review in its
`review_record` column; FRONTIER's ruling 3 on `1e76d4dae` named these eight rows as signed-by-me without one.)

This file is the durable review record for those eight rows. Each section re-verifies the flagged line(s) at HEAD
and states why the FALSE-POSITIVE reading holds. `check_banned_evidence.py --list` re-run 2026-10-02: the eight
rows were NOT APPLIED (signed, no record) before this commit.

## CONTRACT-transform-primitives.md

Flagged: line 366 — "inside `.pdata`-bounded bodies, 16-byte slot span, writes = the memory operand in
destination". The `.pdata` chain is used as the census's *population/boundary descriptor* (which bodies the write
sweep covers), not as unwind evidence for any behaviour claim. FALSE-POSITIVE holds.

## vtable-method-index.md

Flagged: line 2649 — the `Unwind@`/`Catch_All@` funclet labels named while stating the rows below sum to the
subtracted population; and line 5148 — "for the base-class unwind", plain English for the EH hierarchy. Both are
names/labels or descriptive prose; no runtime claim is derived from unwind data. FALSE-POSITIVE holds.

## how-the-prefetch-manifests-are-read.md

Flagged: line 330 — the `0019AEE0` five-slot resolver sentence, whose offending clause is "`01CCCC50` unwinds the
first call's handle": `unwind` is the English verb for releasing a handle, not `.pdata` unwind data. FALSE-POSITIVE
holds.

## the-battle-unit-field-map.md

Flagged: line 1309 — "the 33 bytes are its first unwind fragment, the five-register prologue — 2026-09-29, OPUS,
`CON-173`". This is a *correction* that refuses the earlier misread: it records that unwind data was misused and
struck. FALSE-POSITIVE holds.

## party-roster-and-control-suppression.md

Flagged: line 701 — the `001889C0` field-set sentence; the offending clause "`0016D6A0` unwinding both locals" uses
`unwinding` as the English verb for releasing locals/handles. FALSE-POSITIVE holds.

## ui-request-router.md

Flagged: line 531 — "an address-taken scan. That scan's only hits are `.pdata`, the hook's verb ..." — the page
states the scan found only `.pdata` records and excluded them: the ban applied, not broken. FALSE-POSITIVE holds.

## image-hardening-cfg-aslr-dep-and-stack-cookies.md

Flagged: eight lines (214, 453, 542, 557, 608, 734, 798, 812) — PE section tables naming the `.pdata` extent, a
descriptive "EH unwind funclets" count row, the `__ArrayUnwind` symbol name, a permission map line, a link to
EVIDENCE-STANDARD, and "lands 1.1 MB short of `.reloc`, inside `.pdata`" describing a boundary arithmetic
observation. All descriptive: the page *documents* the hardening structures; no claim is *proved by* unwind data.
FALSE-POSITIVE holds.

## auditsem-review-rc-residue-0930/REVIEW.md

Flagged: line 72 — my own review record's sentence "callees, `.pdata` chain fragments followed; none stores over
`rcx + 4`/`+5`". The review describes following `.pdata` fragments as *extents* to bound a store census — a
placement fact about where bodies end, not unwind semantics as evidence. FALSE-POSITIVE holds.

## Drift note

The same run reports `text-gap-append-0930/README.md` LAPSED (evidence `94053302…` → `dd112027…`): my earlier
signature there lapsed because the page moved; a re-verdict request for it is already routed to OPUS (drift
request filed 2026-10-01). It is not part of these eight rows.
