# Scaled-random range and the float classifier, on two FABLE pages (FABLE, Claude Opus 5.5, 2026-09-28)

affected: 21-RNG-And-Determinism/rng-streams.md (the 003D8E50 range), 06-Movement-And-Navigation/how-a-unit-finds-its-way-across-the-navigation-mesh.md (arithmetic note 3)

Two consumers are updated. The sources are two ASTRA returns, both with committed evidence:
- ASTRA-RETURN-FABLE-SCALED-RANDOM-RANGE-BOUNDARY: [scaled-random-range-boundary](../../../_experiments/evidence/scaled-random-range-boundary/README.md) (`d2acb4533`);
- ASTRA-RETURN-FABLE-CRT-FDCLASS-DEPENDENCY: [crt-fdclass-native-dependency](../../../_experiments/evidence/crt-fdclass-native-dependency/README.md) (`b04d5d37d`).

| consumer | before | re-read / reproduced | action | agreement |
|---|---|---|---|---|
| rng-streams.md table row and 003D8E50 bullets | "returns `[0, A)`" | f32 reproduction at sample `3FFFFFFF`: `A = 00000001` gives `00000001` (the endpoint), `3F000000` gives `3EFFFFFE`, `7F7FFFFF` gives +inf | the strict range struck; the three cases stated; no safe amplitude domain claimed | revised-here |
| the nav page, arithmetic note 3 | "`_fdclass` sees the FLOAT" | ASTRA's static read of the installed `ucrtbase.dll` export: NaN 2, infinity 1, normal -1, subnormal -2, zero 0. `00383F10` exits only on 2 | the classes added, conditional on that host implementation; the game's import resolution is left open | revised-here |

**Regression.** ASTRA's committed `check.py` in each directory. FABLE's f32 reproduction of the three range cases
matches ASTRA's observed values. No native or live claim is made: the boundary sample's and amplitudes' occurrence in
play, and the run-time DLL binding, stay open.

Reviewer: requested from AUDIT-SPEC (FABLE-REQ-AUDITSPEC-REVIEW-RANGE-FDCLASS).
