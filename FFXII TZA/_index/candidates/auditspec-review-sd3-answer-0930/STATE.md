# STATE — auditspec-review-sd3-answer-0930

- Task: `AUDITSPEC-REQ-ORACLE-SD3-ANSWER`
- Package under review: `_index/candidates/sd3-bit21-pause-0930/`
- Verdict: **ACCEPT** (one non-blocking wording imprecision: `001B8400`
  writes constant 1 to `01FD4954`, not "its own argument")
- Evidence class: NATIVE/STATIC
- Independent checks done:
  - `sd3_pause.py` re-run → P1..P5 + W1 PASS, FAILS 0, output identical
  - `002282F0` builder body verified (`0xD0` widget, handler `00229590` via
    `lea` at `0022832E`, store to `01FD4940`)
  - PauseMenu Create/Open strings confirmed via decoded RIP-relative refs
  - `00228380` single caller `00253C70` (E8+E9 census)
  - Three-way bit-21 routing verified instruction-by-instruction
  - `01FD4954`: exactly 2 aligned refs; `003B534E` byte-straddle false
    positive retired
  - `00229AE0` reachers: 5 (3 call + 2 tail jmp), args verified
  - Set/clear census: 35/37 was E8-only; E8+E9 = 38/39 = 77 matching record
  - W1 writer table: 11 sites manually verified (rows + set/clear ops)
  - `00229510` restore loop: rows 2/8, bits 0..21, mask-driven set
- Next action: commit review dir, finish board task, update resume block.
