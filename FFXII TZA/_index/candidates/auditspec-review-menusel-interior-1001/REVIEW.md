# Audit-spec review: OPUS menusel interior citations

Reviewer: SWE2-AUDIT-SPEC · 2026-10-02 · Task: `OPUS-REQ-AUDITSPEC-MENUSEL-INTERIOR-1001` · Package: `_index/candidates/opus-menusel-interior-1001/` · Commit: 20f3f8a2e

## Verdict: ACCEPT-WITH-NARROWING

- `python menusel_interior.py` re-run in place: `VERIFY 27 functions, 109 anchors / ALREADY / FAILS 0` — every anchor is an in-extent instruction boundary decoding to the
  recorded mnemonic; page section already present (`ALREADY`, byte-preserving).
- Semantic sample: 3 rows — `00272180` perspective divide (w = m·v + `+0x3C`, ret `1.0/w`), `0028FEA0` `0209BE80`+`0x8FA0` call pair, `003F6370` full body read.
- Method verdict for all 17 interior packages: `_index/candidates/auditspec-review-interior-method-1001/REVIEW.md`
  (verdict:ACCEPT).
- **Narrowing — one wording defect to repair:** in `003F6370` the sentence says `002EA160(found, rcx + 0x10)` / `002EA0E0(found, rcx)`, but the first argument passed is the re-loaded **id dword** `+0x810`/`+0x814` (`mov ecx, [rbx+0x810]` precedes the call; the `003588B0` result `rax` is only tested). Recommend the row name the id. Every other claim in that row — gating, `00202C90`/`00203080` combine, the `(2.0 - (+0x820 + +0x824)) * 0.75 + 1.5` y-bump (constants verified: `00901B3C`=1.5, `01CEBB70`=0.5, `01CEBC08`=2.0), `00270F50`→`+0x7E0`, the clamped `+0x240+16*i` interpolate into `+0x1C0`, `+0x1C4` += 0.25 — verifies exactly.

