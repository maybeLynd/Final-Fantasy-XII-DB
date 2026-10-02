# Audit-spec review: DD-OWNER-B23 — native-command-lifecycle REOPENED → DOCUMENTED (commit 8f5f0e785)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-DD-OWNER-B23-1001` · Record: `_index/candidates/opus-dd-restatus-23-1001/`

## Verdict: ACCEPT

## What was checked

- **ORACLE's two RC-17 corrections independently byte-verified** on the certified image:
  - `00360880`: `ebx` = 1, loop while `ebx <= 3`; reads each manager's mask `dword[022CB9C4 + 4*(m-1)]`
    (`lea rdi` resolves to `022CB9C4`); `bt eax, ecx` scans bits 0–7 (`003608A0`–`003608AA`); the first set
    bit jumps to `003608B0` and calls `00360710` **once per manager** — not once per set bit. Correction holds.
  - `003604A0`: `movsxd` both args, `rcx = (n + 8m) << 1`, returns `dword[022CB738 + rcx*8]` =
    `[022CB738 + (n + 8m)*16]` — the begun word. Correction holds.
- **Status flip justified:** AO-1, AO-4, OV-15 and RC-17 are all answered in the register; the SECTION-11 trigger
  was accepted by a non-author review on 2026-09-29.
- **A-drift pairing verified:** `scriptvm-verb-adapter-callbacks.tsv` loses exactly the `00353A10` / `00353E20`
  rows (1032→1030), and the native-command-lifecycle page now cites both functions with full interior semantics
  (lines 574/585: the `eventreadsync_ea`/`eventsync_ee` operand-taking form vs the zero-operand copy, clamp
  `clamp(n+1, 1, 3)`). The map-ctrl page carries the corrected `00360880` line with a dated OPUS note.
- **`restatus23.py` re-run:** three edits ALREADY; **one refusal** — the strike-through edit fails its
  exact-match because FABLE's own adjudication restate (`a8aed6ca9`) extended that sentence afterward
  (`(the pause-menu skip confirm writes it through 00228C70 → 00285EA0); ... (restated 2026-10-01 on FABLE's
  adjudication)`). The intended outcome is nonetheless present at HEAD: the pending marker is struck and the
  adjudication note sits on the page. Benign precondition drift, not a missing edit.
- `documented_rule.out` reproduces READY 1 of 1.

## Notes

- The RC-17 register row still reads "FABLE adjudication pending" — OPUS correctly deferred it: the register
  carries another lane's uncommitted RT-1..RT-15 edit; not a defect of this batch.
