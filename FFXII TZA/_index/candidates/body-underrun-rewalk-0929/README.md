# Consumer check: the body underrun re-walk (OPUS, 2026-09-29; falsification pass 2 on the-bodies-the-list-cuts-short)

corrects: 99-Unresolved-Residual/Unlisted-Code/the-bodies-the-list-cuts-short.md (177 -> 164 truncated bodies, 2,564 -> 1,486 bytes, 19 -> 12 tables; the fourteen "misclassified" blocks reclassified)

## What was corrected

The 2026-09-21 walk read 13 terminated bodies as continuing:
- it tested for the mnemonic `ret` and so walked past `repz ret`;
- it let an indirect `jmp [mem]` fall through;
- it did not stop at calls to `noreturn` functions;
- it decoded jump-table data after the dispatch as code.

The re-walk reproduces 164 of the 177 and finds no new truncation. Of the fourteen "misclassified" blocks, five are real
tails (already covered by the band's extensions), three are held rows, one is a jump table, two are called import thunks
(correctly admitted) and three are unreferenced. No population row is wrong. The old list
(`listed-bodies-with-code-past-body-bytes.tsv`) is kept unchanged as the first run's raw result.

## Current consumers

- consumer: the-bodies-the-list-cuts-short.md: revised-here (the headline, histogram, four largest, section 3 and the
  tooling paragraph). The page stays PARTIAL on the 159 unapplied extensions (routed-to-OPUS-REQ-FRONTIER-EXTENT-ERRATA-UNDERRUN-159).
- consumer: _index/candidates/uc1-held-rows-opus/README.md agrees: the held switch tables are data, not body.
- consumer: _index/candidates/uc1-extent-collision-consumer-check.md agrees: `007C2A29` is a real tail, extended by the band.
- consumer: _index/FUNCTION-EXTENT-ERRATA.tsv is not changed here; the 159 rows are prepared in
  `underrun-errata-rows-0929.tsv` for FRONTIER to apply (routed-to-OPUS-REQ-FRONTIER-EXTENT-ERRATA-UNDERRUN-159).

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/check_body_underruns.py`, with three controls:
- `0037C3F0` truncated (FABLE's case);
- `00148F10` not truncated (`repz ret`);
- `00862022` not truncated (a `jmp [mem]` thunk).

A walk that reads `repz ret` as not-ret, or lets `jmp [mem]` fall through, fails the second and third.

run: verified at 022860d96 (controls PASS; 164 truncated, 1,486 bytes, 12 with a table), against the certified image `73461d08…`.
