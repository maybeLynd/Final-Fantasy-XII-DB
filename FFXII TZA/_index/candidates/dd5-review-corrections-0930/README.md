# Batch-5 review corrections (page side) and the FINAL-AUDIT pass-4 `001DF240` sentence (SWE2-DATA, 2026-09-30)

affected: 06-Movement-And-Navigation/clamping-a-point-into-a-volume.md, 06-Movement-And-Navigation/Movement-Mode-Selection/setting-the-movement-mode-and-which-way-a-character-turns.md, 19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md

run: at 878251fc8: dd5_sem.py, FAILS 0 (SWE2-AUDIT-SEM's review script, re-run from the repository root).

`AUDITSEM-REQ-DATA-DD-OWNER-READ-5-ROWS-0930`, per
[`auditsem-review-dd-owner-read-5-0930/REVIEW.md`](../auditsem-review-dd-owner-read-5-0930/REVIEW.md) section 5:

- **C1 (clamping page).** Batch 5 struck "they are `.data` addresses, not immediates" and called `01EF93F0` /
  `01EF93FC` "the clamp constants". The struck clause was true. The cell is `.data`: the x and w lanes of the software
  `vf00` image, which `00363FD0` loads live. Its three writers `0036D9A8`, `0036D9E8` and `0036DD87` all store
  `[0, 0, 0, 1]`. The body text and the Key addresses row are corrected with dated notes linking
  `CONTRACT-transform-primitives` §15b.
- **N2 (clamping page).** "Heard as where a sound comes from" is now labelled an inference from the ledger's Audio
  filing of `003631B0`, `00361810`, `003638B0` and `00362850`. The bodies after the clamp are unread (`SD-180`).
- **C2 (movement-mode page).** The §10 note now states the full condition for the non-zero second argument, with both
  predicates read. What stays open is what a tween node's byte `+1` means, which matches `SD-190`'s row.
- **C3 / N1.** `SD-181` and `SD-180` already carry these in the register (`86bfa9b1a`). The pages do not contradict
  them.

`OPUS-REQ-DATA-PASS4-001DF240-0930`: `audit_crossrefs.py`'s CLASSIFICATION rule matches "still unresolved" within 400
characters after an address on the same line. On the settings page, line ~992 said the three tables' "meaning is still
unresolved" in the `001DF240` row. It now reads "not yet established", with a dated note that `001DF240` itself is
classified to Save_Load_Settings. The rule's regex finds no match left on the page.

## Consumer check

| consumer | disposition |
|---|---|
| the three pages above | revised-here |
| `00-Engine-Core-Runtime/CONTRACT-transform-primitives` §15b (the `vf00` cell is `.data`, not a constant) | agrees |
| OPEN-QUESTIONS `SD-180`, `SD-181`, `SD-190` (restated at `86bfa9b1a`) | agrees |
