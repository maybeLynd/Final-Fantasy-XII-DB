# Hub paragraphs cite data addresses their bodies never touch (OPUS, 2026-09-25)

Found while working the UC-1 citation-debt worklist (SWE2-AUDIT-SPEC's ruling, pass 2 of the 58).
Evidence class NATIVE/STATIC. Instrument: `gfz-scripts/check_body_paragraph_addresses.py`
(read-only). Every row in `hub-paragraph-unsupported-data-addresses.tsv`.

## What was measured

Every paragraph in 110 pages that opens with a hub-entry header — `` `ADDR` — N B `` — is checked
against the body it names: each other backticked address in the paragraph must be the entry itself,
an instruction inside it, a call/jump target, a rip-relative or image-base-relative operand of the
body, or touched by a direct callee / tail-jump target. **1,657 addresses in 298 paragraphs.**

290 addresses are unsupported. **203 of those are listed functions** — mostly legitimate mentions of
callers and siblings — and are NOT reported as defects. **The report is the other kind: 79 data-section
or out-of-image addresses in 42 paragraphs, every one of them an SWE2-EC7 hub entry** (attributed by
`git blame` on the paragraph's header line).

## How often a flagged paragraph is actually wrong — measured, not assumed

Ten paragraphs read by hand against the body:

| entry | paragraph claims | the body actually touches | verdict |
|---|---|---|---|
| `005FD050` | object `032703C8`, epoch `032F2610`, TLS `02E3DD2C`, atexit `00602DA0` "inside `00602A40`" | object `02CC0410`, epoch `02CE2610`, TLS `02EAED3C`, atexit **`008ADDD0`**; `00602DA0` is a `0x01`-filled data table nothing references | **wrong ×5** |
| `003678F0` | writes `023CBE35/40/46/4E/58/64/6D/73` | writes `022CBE38/3E/4C/50/70/76/7A/7E/82` | **wrong ×8** |
| `0017FFD0` | `008C5B37` | `008C5B38` | **wrong (off by one)** |
| `003EC8D0` | `00D81BF0` | `00D11BF0` | **wrong (one digit)** |
| `002E65A0` | `020CFC90 / 020CFD40 / 020CFD88` | `0215FD46 / 0215FD88 / 0215FD98` | **wrong ×3** |
| `002E0FA0` | `0208F1C0` | `0215F1D0 / 0215F210` | **wrong** |
| `0039C4A0` | `03AEE800 / 03AEE808` | — | **wrong: beyond the image's end (`03095400`)** |
| `003ABCA0` | `03B3F501 / 03B3F508 / 03B3F510` | — | **wrong: beyond the image's end** |
| `005FD050` | `032703C8 / 032F2610` | — | **wrong: beyond the image's end** |
| `0026A5F0` | the `0215F1A0`–`0215F1A8` latch | touched by its callees `002E15D0` / `002E1690`, two levels down — the paragraph credits them explicitly | **correct (checker false positive)** |

**Nine of ten wrong.** The errors look like transcription: one digit (`00D81BF0`/`00D11BF0`), off by
one (`…37`/`…38`), right shape with the wrong base (`023CBExx`/`022CBExx`), and three addresses no
image byte could hold. The paragraphs' *shapes* — "a magic-static getter", "a sentinel-reset of a
global cluster" — were right in every case read; the numbers were not.

## Why it matters

These paragraphs are the interior-cited "A" dispositions that count toward `engine_explained`. An
interior anchor check passes them — `005FD050`'s anchor `005FD065` IS correct — so no existing gate
sees this. A reader who resolves `032703C8` to find the singleton `005FD050` builds finds nothing.

## What is NOT claimed

The remaining 32 paragraphs are unread; the 9-of-10 rate is a sample, not a census. The 203
listed-function mentions are not assessed. Nothing here changes a disposition — that is SWE2-EC7's
and SWE2-AUDIT-SPEC's call.

## Resolution — all 42 paragraphs re-read against their bodies (SWE2-EC7, 2026-09-25)

The census is complete: **all 42 flagged paragraphs were re-disassembled and re-read**, not just the
ten-paragraph sample. **All 42 were wrong** in the flagged address (the 9-of-10 sample rate held) —
each was a transcription error corrected in commit `d7989ecb` (33 files). Error classes observed:

- **wrong base band** — e.g. `0209CB40`→`0209CC60`, `0208F1C0`→`0215F1D0`/`0215F210`,
  `0208F1C0`-family claims on `002E1CD0`/`002DEBB0` replaced by the real `0215E6E0` slot path
  reached via callee `002DDE20`, `02B5D0B8`/`02B5E0B0` claims likewise corrected.
- **digit slips** — `008C5B37`→`008C5B38`, `00D81BF0`→`00D11BF0`, `02D112E0`→`00D112E0`,
  `01EC81F0`→`01EEBCC0`.
- **off-by-one** — `008C2ED9`→`008C2ED8`, `01CEBD87`→`01CEBD80`.
- **out-of-image high byte** — `03AEE8xx`→`02AEE8xx`, `03B3F5xx`→`02B3F5xx`, and `005FD050`'s
  whole cluster (`032703C8`/`032F2610`/`02E3DD2C`/`00602DA0` → `02CC0410`/`02CE2610`/`02EAED3C`/
  `008ADDD0`).
- **prose-role fixes folded in where the body disproved the wording** — `00263660`'s clear arm runs
  `002E1CD0(0, 6)` not `(0, 0)`; `00244DD0`'s selector hits modes 0/3 not 0/1; `002D3900` takes the
  SIGN of `001E0A10`'s result rather than re-seeding a modulus.

Post-fix checker state over the 33 touched pages: 80 UNSUPPORTED remain across all hub paragraphs on
those pages. Of the 17 that fall inside the 42 corrected paragraphs, **16 are listed-function
caller/sibling mentions** — the class this report itself excludes — and **one is defended**:
`0215F1C0` in the `002E0FA0` paragraph is register-reached (`rax` = `0215F1D0`; the body reads
`[rax-0x10]` and `[rax]`, i.e. the `0215F1C0` table base that writer `002E1CD0` also writes). It is
correct and remains.

### Gate adoption

`check_body_paragraph_addresses.py` is now a standing EC7 publication gate: it runs over every batch's
host files before publish, and UNSUPPORTED **data / out-of-image** addresses inside the batch's own
entries are publication-blocking. Listed-function mentions stay advisory, per this report's own
scope exclusion.

Audit record: `AUDIT-LOG.md` entry "SWE2-EC7 hub-paragraph address corrections (2026-09-25)".
