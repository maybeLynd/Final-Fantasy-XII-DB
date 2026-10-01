# Consumer check: page sizes that are a chained function's first fragment, and the catalogue's short tails (OPUS, 2026-09-29)

corrects: 04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md (003204E0 ~33 B -> 255 B: CON-173)
corrects: 18-Audio/Sound-Bank-And-Voice-Formats/seb-se-block-index.md (0030C650 63 B -> 570 B: CON-173)

## Why this sweep

Two corrections today came from reading a shrink-wrapped function's first `.pdata` fragment as the whole function:
- CON-170: `003266DB`, taken for "a dispatched handler";
- CON-172: `002E45E0`, taken for "a 40-byte leaf".

`fragment_size_sweep.py` looks for the same shape across the corpus: a page cites a function next to a byte size that
equals its first fragment, not its catalogue size. `sweep.tsv` holds its 15 hits.

| hits | disposition |
|---|---|
| 3 in the heading-delta contract, 1 in `_inbox/ASTRA.md` | the struck/corrected text of CON-172, and ASTRA's report of it |
| 4 x `0032E620` (75 B) | false positive: 75 B is a script-verb caller's size on the same line |
| `00399110` (16 B) | false positive: "16-byte records" |
| EXP-061 `0030E060` (57 B) | false positive: the record says the first unwind entry covers only 57 bytes, on purpose |
| widget page `00248220` (85 B) | already corrected on the page on 2026-09-15 (190 B) |
| `OPEN-QUESTIONS.md` UQ-185 `00248220` (85 B) | **stale** (OPUS's own 2026-09-15 answer). Deferred: the register is claimed by SWE2-DATA right now |
| `003204E0` (~33 B) | **corrected**, CON-173: 255 B |
| `0030C650` (63 B) | **corrected**, CON-173: 570 B; its cited calls are at `0030C836`/`0030C84B` and stand |
| `00729A3A` (98 B) | a chained fragment of `00729920`. It resolves the unclassified orphan on the unlisted-code page (FABLE's section); sent to FABLE, not edited here |

## The catalogue's short tails (measured, not corrected here)

- **270 catalogue functions end before their own chained unwind fragments do**, 16,361 bytes in all. Every chain is
  contiguous: 3,828 chained roots, 0 non-contiguous.
- Of those bytes, 51 lie in some population body or funclet and 154 in held rows. **16,156 lie in no body**, so the
  executable view counts them as UNKNOWN.
- Every function-bounded census skips them.
- Example: `00729920` is catalogued at 189 B. Its three chained fragments run to `00729A9C`, and hold its switch's default
  arm and both of its `ret`s.

FABLE's 2026-09-13 vote (`OPUS-REQ-DENOMINATOR-UNLISTED-CODE`) says under-sized tails extend their listed entries. These
270 are that class, measured by the linker's own chains. Changing the population or the catalogue is a counting-rule
change, and accepted UC-1 extents are not OPUS's to move alone. It is routed as `OPUS-REQ-FRONTIER-CATALOGUE-CHAINED-TAILS`.

**Today's counts over the tails.** `tail-recheck.txt` decodes all 270 tails from their own fragment boundaries (2,753
instructions). It finds no call, jump or RIP reference to any target counted in today's passes: slot maps, party focus,
battle state block, equipment compatibility, shop ladders, heading delta. Those counts stand.

## Current consumers

- consumer: [the-battle-unit-field-map.md](../../../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md): revised-here.
- consumer: [seb-se-block-index.md](../../../18-Audio/Sound-Bank-And-Voice-Formats/seb-se-block-index.md): revised-here.
- consumer: `_index/CONTRADICTIONS.tsv`: revised-here (`CON-173`).
- consumer: `_index/OPEN-QUESTIONS.md` UQ-185: not yet revised (claimed by SWE2-DATA); OPUS will correct 85 B -> 190 B once free.

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/fragment_size_sweep.py` - a finder, not a gate. It still reports the 15 lines, because
struck-through old sizes match too; the table above adjudicates each one. A NEW hit, not in that table, is a new instance of
the class.
regression: `Database/Tools/analysis-kit/gfz-scripts/catalogue_tail_census.py` - lists the 270 tails and re-runs named targets over them.

run: verified at f3f933297 against the certified image `73461d08…`.
