# Consumer check: 21-RNG contradictions from a local reconstruction-readiness pass, OPUS's share settled on the pages (OPUS, 2026-10-02)

Board task OPUS-RE-READINESS-RNG-1002: stream R run locally. A read-only reader mapped `21-RNG-And-Determinism/`
(rated MOSTLY; the map is filed in the RE repo as `docs/readiness/21-rng.md`). It found 23 contradictions; the 11
value-changing ones were each decided at the image. OPUS re-read items 1, 3, 4, 7 and 8 at the bytes before any edit,
and every new value the drafted edits introduced:

- the image holds at least eight generators; the eighth is the PPFX xorshift128 `0074BDE0` (`sar 8` at `0074C0BD`);
- 67 functions draw from the gameplay MT cursor, because the camera-shake sampler `0037D1F0` draws through
  `00379CE0`;
- `00863C80` draws without calling `00863BF0`, so a hook on `00863BF0` misses camera shake;
- the graphics twist `0018EE20` keeps bits 31 and 0 of `mt[i]`, pairs with `[+0x634]` then `[-0x38C]`, sets its
  cursor `+0x9C0` and count `+0x9C8`, and has no ISA test;
- `DAT_02089300` is cleared once at boot (`0022A41A`) and set once in boot frame mode 0 (`0022B77C`).

A second read-only pass drafted 63 strike edits (`apply_21rng.py`). FABLE is working again (user, 2026-10-02), so
OPUS applies only the 20 edits on its own pages (`apply_by_owner.py OPUS`). The other 43 are routed as requests:
- 41 on FABLE-led pages;
- 1 on SWE2-FRONTIER's parity-table row;
- 1 on SWE2-EC7's graphics-twist line.

Each lane runs `apply_by_owner.py <name>`.

- **Affected:** 21-RNG-And-Determinism/CONTRACT-gameplay-generators.md, 21-RNG-And-Determinism/CONTRACT-which-generator-serves-which-roll.md, 21-RNG-And-Determinism/README.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the two OPUS-led CONTRACT pages and the README | revised-here |
  | `rng-streams.md` and `which-roll-is-on-which-generator.md` (FABLE-led) | routed-to-FABLE (request with `apply_by_owner.py FABLE`, 41 edits) |
  | the `00863C80` row of the gameplay contract's parity table | routed-to-SWE2-FRONTIER (request with `apply_by_owner.py SWE2-FRONTIER`, 1 edit) |
  | the graphics-twist line of `which-roll-is-on-which-generator.md` (EC7-49 batch 17) | routed-to-SWE2-EC7 (request with `apply_by_owner.py SWE2-EC7`, 1 edit) |
  | RE repo `docs/readiness/21-rng.md` | routed-to-OPUS (filed from this commit) |
  | the structural gaps (the CRT `rand()` seed rule and thread map, 11 of the LCG's 15 callers' reductions, the Bullet solver LCG, the noise texel mapping) | routed-to-OPUS (later reads) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-rng-readiness-fixes-1002/rng_check.py, verified at 6bf16816b: 24 instructions decode as cited and `0018EE20`-`0018EEDF` has no rip-relative operand, FAILS 0 ([`rng_check.out`](rng_check.out)). `apply_by_owner.py OPUS` re-runs as ALREADY (20), FAILS 0.
