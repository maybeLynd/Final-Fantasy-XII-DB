# Audit-spec section acceptance: SECTION-08 + SECTION-09

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Task `OPUS-REQ-AUDITSPEC-SECTION08-09-ACCEPT-1001`
Subject: `bc74b44a8`; owner review `sections02-08-09-queue-owner-review.md` (conditional:
accept corrections, restore three dropped facts).

## Verdict: ACCEPT

## Condition check — all three dropped facts restored at HEAD

`CONTRACT-resource-request-queue.md`: the asking form `0032E520(1)` at the boot modes
(`00379E30` cited), the staged-selection push `0036C1F0` (EXP-146's disclosure), and the
initialisation read-layer reset `0032EA90` → `003EB050` — all present.

## Byte-verified anchors (certified image)

**Q5** `0032E8DD/E1/E5`: `mov r8,[rcx+0x10]`, `mov r9,[rcx+0x18]`, `mov r11d,[rcx+8]` — the
requester copies the descriptor's callbacks and argument verbatim ✓
**Q7** `0032E924`: `and eax,0x3F` / `0032E927 shl ecx,6` / `0032E92A add eax,ecx` —
id = `(counter << 6) + (slot & 0x3F)` in 32 bits ✓

## Scope note

SECTION-02 of the same merge was ACCEPTed earlier (`auditspec-review-section02-0930`). Q1–Q4,
Q6, Q8–Q9 and O08-1..6 stand at the sections' stated fixture scope, per the owner review's
not-re-derived list.
