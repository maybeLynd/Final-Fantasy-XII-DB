# Audit-spec review: SD-120 — the eight `0050xxxx` binding operations are palette (CLUT) animation effects

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `sd120-binding-ops-0930` (SWE2-ORACLE)
Board task: `ORACLE-REQ-AUDITSPEC-SD120-0930`

## Verdict: ACCEPT

## What was checked

- **Checker re-run.** `python sd120_ops.py` at HEAD: 33 checks, `FAILS 0`, matching the retained
  `sd120_ops.out`. The instrument is execution-based — `sd120_emu.py` runs the shipped bodies in
  Unicorn on controlled memory (image BSS buffers + scratch record page), with only two bridged
  calls (`memcpy` thunk `00861EBA`, `__chkstk` `00808F10`). That is stronger than a static read:
  the M-checks run a Python model against the *native* result over seeded random trials.
- **Non-vacuity.** The record itself documents two first-draft models that failed against the
  native code and were corrected from the code (op7 unmasked lanes 159/300; op1 mode 2 negative
  shifts 10/400). The tail of the fresh run reproduces the same productive corrections: X1
  (allocator `003CCC20` copies 48 bytes, not the page's claimed 32-byte payload), X2 (+0x28/+0x30
  are op-list head/tail *read* by both dispatchers, contra "written only"), X3 (`00431B10`
  zero-extends the speed byte, so the expression path never takes the negative arms).
- **Native spot check.** Independently disassembled `003D2B60` (the repacker) from the certified
  image (`73461D08…`): the n==1 fast path unpacks `movups` lanes and shifts `shr rax, 0x20` /
  `shr r8, 0x20` chain visible — consistent with the claimed per-lane `>> 8` clamp-and-store
  structure (the general n>1 loop is further into the body; execution trials cover it).
- **Scope discipline.** The record honestly separates measurement from interpretation: "lane c is
  byte c … reading the lanes as R,G,B,A is an interpretation" resting on PS2 CSM1 order and op5's
  BT.601 weights; the link to GFZ-named render-model subresource-variant bindings is labelled "the
  page's reading, not a new measurement." No overclaim.
- **Dispatcher claim.** Both byte-opcode dispatchers `003CCF20` / `003CD2C0` mapping opcodes 1–8 to
  the same eight bodies is checked inside the control (D-series) and by the earlier
  `ui_bi17_dispatch.py` record it cites.

## Narrowing / notes

None required. The record's own X-checks already carry the corrections to the host page; the
interpretation caveats are explicit.
