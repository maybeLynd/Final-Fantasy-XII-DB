# SWE2-AUDIT-SPEC review — OPUS DD owner re-status batch 2 (`e696ef86e`)

Task: `OPUS-REQ-AUDITSPEC-DD-1599-B-0930`. Pages: `save-image-buffers-header-and-payload.md`,
`the-shared-drawing-context.md` (PARTIAL → DOCUMENTED).

## Verdict: ACCEPT

## Verification

**save-image-buffers-header-and-payload.md**

- Status line is current: DOCUMENTED, cites SD-40 answered 2026-09-30, keeps UQ-271's SUPERSEDED
  pointer (duplicate of V-1, ANSWERED 2026-09-27) ✓
- The backing record `sd40-42-header-readers-0930` exists and states the claimed answer: no
  instruction reads header dwords `0x12`/`0x13` (bytes `+0x48`/`+0x4C`) or the stamp copies as
  fields. It already carried an SWE2-AUDIT-SPEC narrowing pass
  (`auditspec-review-sd-readers-0930`) — the answer was reviewer-checked, not self-asserted ✓
- §5 call chain: `003BB9B0` "(unread)" → "(read under FV-3, §7)" correction present at line 302;
  the §7 finaliser/`+0xD8` correction also present (line 324) ✓
- Stale "open" lines were annotated with dated corrections, not silently deleted ✓

**the-shared-drawing-context.md**

- Status line names SD-103/104/105 answered 2026-09-30 ✓
- Records exist and were previously reviewed on this lane: `sd103-104-context-rows-0930` at
  `c2b5b9927` — ACCEPT (`auditspec-review-sd103-104-0930`); `sd105-reveal-inputs-0930` at
  `f2f55938a` — ACCEPT-WITH-NARROWING (`auditspec-review-sd105-0930`) ✓
- The §3a mechanism claim is arithmetically correct: row builder `002432B0` writes via
  `ctx + 24 × row`; third qword = row base +0x10; 24·174+0x10 = `0x1060`, 24·175+0x10 = `0x1078`,
  24·176+0x10 = `0x1090` — matching SD-103's three pointer slots, and correctly explaining why a
  fixed-displacement census could not see them ✓

## Scope note

No new native measurement was claimed or needed — this is status currency over
already-reviewed answers. Both pages' claims are tier-cited to named records.
