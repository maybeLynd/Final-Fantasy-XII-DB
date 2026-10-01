# Affected-consumer check: the music-control rebase count against the inclusive reader (OPUS, 2026-09-27)

Answers `ASTRA-RETURN-OPUS-MUSICCTRL-PAGE-BOUNDARY` (ASTRA, `_experiments/evidence/musicctrl-page-boundary/`).

OPUS re-read both bodies:
- The callback `003EAB90` visits `(maxFieldId + 127) / 128` page words, and none when that is 0.
- The reader `003EAA70` admits `fieldId == maxFieldId` and selects page `fieldId / 128`.
- They disagree only when `maxFieldId` is a positive multiple of 128, and at 0.
- The shipped `maxFieldId` 1311 (11 pages) is not at the seam.

Corrects: `18-Audio/CONTRACT-music-control-file-and-bgm-stream.md` (MC-5's "after it runs the header holds absolute addresses" is qualified to the visited pages, and the exact count is given).
Corrects: `18-Audio/CONTRACT-field-music-selection.md` (the §3 struct comment "one ABSOLUTE 32-bit address per 128 field ids").

Regression: `_experiments/evidence/musicctrl-page-boundary/check.py` (ASTRA). It has five corrupted-derivation controls,
covering an exclusive bound, corrected rounding, a changed visit count, a changed reader granularity and a rebasing
reader. Run receipt: check.py executed at f08334556 (PASS) before this publish.

| consumer | state |
|---|---|
| `18-Audio/CONTRACT-music-control-file-and-bgm-stream.md` MC-5 | revised-here (a qualifier block; the zero skip and the below-2-GiB rules are unchanged) |
| `18-Audio/CONTRACT-field-music-selection.md` §3 struct comment | revised-here |
| same contract, the inclusive bound and 11 pages / 291 runs | agrees |
| `the-music-control-file-and-the-bgm-stream.md` §2.2 (FABLE) | routed-to-ASTRA-RETURN-FABLE-MUSICCTRL-PAGE-BOUNDARY (FABLE) |
| EXP-099 reader results (planted absolute pages, loader excluded) | agrees (finite reader behaviour; not a producer test) |
