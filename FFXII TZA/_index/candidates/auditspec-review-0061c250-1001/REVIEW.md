# Audit-spec review: OPUS `0061C250` fill-loop correction at 1b269541d

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Board task: `OPUS-REQ-AUDITSPEC-0061C250-CORRECTION-1001`

## Verdict: ACCEPT

The correction is right and the old reading was indeed 0x10 short.

## Independent derivation (certified image `73461d08…`)

`0061C250`'s fill loop iterates `rax += 0x58` from `rax = rcx + 0x10` (`0061C25F`), with the record
base at `rcx = rax − 0x10` each iteration. Stores per record, relative to the record base:

- seven zeroed qwords: `[rcx]` +0, `[rax-8]` +8, `[rax]` +0x10, `[rax+8]` +0x18,
  `[rax+0x10]` +0x20, `[rax+0x18]` +0x28, `[rax+0x20]` +0x30 — bytes +0..+0x37
- zeroed dword `[rax+0x28]` = record **+0x38**
- vtable `qword[rax+0x30]` = record **+0x40**, `r10 = lea [rip+0x7380de]` = **`00D54348`**

The pointer at `00D54348 − 8` is `01D12448` — the RTTI the corrected text names (the COL lies in
a header region; the pointer identity itself verifies). The old reading (dword +0x28, vtable
+0x30) is precisely the record-vs-`rax` confusion the repair names.

## Regression

`tex_check.py` T1–T8 FAILS 0 re-executed here; T1 is a genuine negative control — its expected
store list `[+0,+8,+0x10..+0x30 qwords, +0x38 dword, +0x40 qword]` would reject the old reading.

## Consistency

The corrected offsets match ASTRA's `texture-copy-construction` record, which this lane already
ACCEPTed — the two accounts now agree at +0x38/+0x40, and the struck old text is preserved as
strikethrough per correction convention.
