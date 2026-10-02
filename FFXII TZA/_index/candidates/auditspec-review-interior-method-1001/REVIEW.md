# Audit-spec review: the OPUS interior-citation method (FRONTIER method verdict)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `FRONTIER-REQ-SPEC-INTERIOR-METHOD-VERDICT-1001`
Scope: the 17 `opus-*-interior-1001` packages (commit range through `787271b18`), 729 entry-only F functions, one method.

## Verdict: ACCEPT

The method — one access/representation sentence per function plus machine-verified interior anchors — meets the
explanation bar and may be scaled to the remaining entry-only frontier.

## What was independently checked

- **Mechanical layer (all 17 packages):** each package's `*_interior.py` was re-run in place; every one prints
  `ALREADY` (byte-preserving, the sections are in the pages) and `FAILS 0`. Totals reproduced: 729 functions,
  ~2,162 anchors; every anchor is an instruction boundary strictly inside its `functions.tsv` extent decoding to
  the recorded mnemonic. The checker cannot see the sentences — that is the stated division and it is honest.
- **Semantic layer (sample of 34 rows across all 17 packages):** each sampled body was disassembled fresh from the
  certified image (sha `73461D08…721F8`) and read against its sentence — including every rip-relative address the
  sentence names. Spot rows: pfgate `00272710`, `0028CA30`, `003F80D0`, `003C5400`, `00505500`, `00272F30`,
  `00289970`; boot `0017D990`, `0036D260`, `00863610`; console `0015CC00`, `001C0630`, `005DDDB0`; cutscene
  `00197790`, `003413E0`, `003EB720`; fef `0024D330`, `00417A80`, `00521000`; gameapp `001850B0`, `001BDA50`,
  `008B1C00`; inputstack `0017D3E0`, `006223D0`, `007927C0`; lu `0024E210`, `003A2B60`, `005375B0`; mapctrl
  `001806F0`, `003CD5D0`, `00291D90`; menusel `00272180`, `0028FEA0`, `003F6370`; renderrec `0015CC90`,
  `00427300`, `0051F020`; settings `00181390`, `002DE080`, `0046DB10`; soundvoice `0015CAF0`, `00210C50`,
  `00360C20`; timestop `0017F250`, `0034BB80`, `0051CDC0`; twoframes `0017F070`, `0033FA20`, `00504490`;
  widgetmsg `001E9F00`, `002D1420`, `0057EB30`; worldtick `0017DFC0`, `0035B5D0`, `00797A20`.
- **33 of 34 sampled sentences verified exactly**, including constants (the `00901B3C`=1.5 × `01CEBB70`=0.5 fold
  in menusel `003F6370` really is "times 0.75 plus 1.5") and the documented "address 0 when rcx is null" quirk in
  widgetmsg `002D1420`. Sentences stay at access/representation level; no purpose is invented.

## Finding (recorded, does not block the method)

- **menusel `003F6370`:** the sentence says `002EA160(found, rcx + 0x10)` and `002EA0E0(found, rcx)`. The first
  argument actually passed is the re-loaded **id dword** `+0x810` / `+0x814`, not the `003588B0` result `rax`
  (`mov ecx, [rbx+0x810]` precedes the call; `rax` is only tested). The same applies at `003F63D4`. Recommend the
  row be corrected to name the id, e.g. "the +0x810/+0x814 id". The gating, callees, arg2 and all later claims in
  that row verify exactly.

## Limits

- 34 of 729 rows were read semantically; rows not sampled carry the anchor-checker guarantee plus this method
  verdict, not a per-row semantic audit. When scaling, keep a non-author spot-check cadence — this sample's hit
  rate (1 loose arg-name in 34) is the empirically observed defect class the checker cannot catch.
- The verdict covers the method and these 17 packages only; it does not vouch for any future page produced by it
  without the same anchor verification plus spot-check.
