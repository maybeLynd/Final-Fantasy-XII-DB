# Audit-spec section acceptance: SECTION-07 + SECTION-10

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Task `OPUS-REQ-AUDITSPEC-SECTION07-10-ACCEPT-1001`
Subject: `60379fcbd`; owner review `sections06-07-10-efx-owner-review.md` (conditional:
the trigger survives, the requester census does not — restore before publication).

## Verdict: ACCEPT

## Condition check — the requester census is restored at HEAD

`CONTRACT-efx-source-rebase.md` carries all 17 demanded tokens: the runtime-mode binding family
`003B4B60`/`003B5520`, `003B8260`'s element-kind dispatch with `jmp rcx` at `003B879B` and the
`0x3B994C` byte map, request sites `003B846F`/`003B855C`, the mount path `002E73C0` +
`002E73FA`/`002E743E`, `003A3FD0(-1)`→`003326C0`, `003B50D0`/`003B5660`/`003B56C1`, command 0x28
`00520720`, delivery `0042865B`.

## Byte-verified anchors (certified image)

`003B8790` computes `ecx = dword[r11 + rax*4 + 0x299854]` then `add rcx, r11 / jmp rcx` — the
element-kind dispatch is a case-offset table, exactly the mechanism the census describes.
`003E6AA0`/`003B3C00` demand-pair restatement present per the owner's keep-list.

## Scope note

SECTION-06 of the same merge was ACCEPTed separately (`auditspec-review-section06-1001`).
This verdict covers SECTION-07 and SECTION-10 only.
