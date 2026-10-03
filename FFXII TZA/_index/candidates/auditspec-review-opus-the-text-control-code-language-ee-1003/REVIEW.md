# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-text-control-code-language-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-TEXT-CONTROL-CODE-LANGUAGE-EE-100-69E66` · Package: `_index/candidates/opus-the-text-control-code-language-ee-1003/` · Page: `16-UI/Text-And-Number-Rendering/the-text-control-code-language.md` (commit 6a9eb7555)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 1 functions, 5 anchors / ALREADY / FAILS 0` (exit 0).
- `rows.json`: 1 row(s), 5 anchors; rejected 0, missing 0; the README's count sentence matches.
- Semantic pass: **every row** read clause by clause against `disr.py` output of the certified image (SHA256 73461D08...):
  - `002B5240` exact: null `rcx` returns (`002B5243`); `dword [o+0x28]` = 0x80808080 (`002B526F`); null source `[o+8]` or destination `[o]` returns; the bound test is the source offset plus the token length `002B1FB0(token)` against the signed word `[o+0x20]` (`002B52C4 jg`), which empties the destination and zeroes word `+0x22` (`002B537E`-`002B5388`); a `0x0F, 0x38` token takes `003FFB00(token+1, &word)` and `002639E0(word)` and copies its `strlen` with `memcpy` (`002B5317`), a null string ending the copy (`002B52F7`); other tokens `memcpy` their n bytes; the loop runs while the next source byte is non-zero (an empty source skips straight to the terminator, `002B529B`); terminator and `word +0x22` = length + 1 (`002B5352`/`002B5356`).
- Advisory, not a defect: the README title says "cloud-drafted" while the drafting session it names is a local agent.
- Limits hold: body statements only, static evidence; the draft and OPUS's re-read are not independent review, this record is.
