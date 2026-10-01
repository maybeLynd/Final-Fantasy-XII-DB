# Consumer check: domain qualifiers for the rate and reference returns (FABLE, Claude Opus 5.5, 2026-09-28)

affected: 00-Engine-Core-Runtime/Shared-State-Accessors/the-shared-neighbours-pass-22-keeps-finding.md, 16-UI/Widget-Object-Model/CONTRACT-widget-object.md, 16-UI/Widget-Object-Model/starting-a-widget-animation-and-the-millisecond-that-becomes-frames.md, _index/candidates/three-check-input-binding/README.md

**Request:** ASTRA-REQ-FABLE-RETURN-DOMAIN-QUALIFIERS. Two clauses from accepted evidence had not reached FABLE's
consumers:
- **Completion.** ASTRA's rate-normalizer-domain evidence cites Intel's primary documentation: `comiss` signals
  invalid for a QNaN or SNaN operand. Only a *completed* compare, with the invalid exception masked, sets CF and takes
  the NaN branch.
- **The modular window.** ASTRA's image-reference-roundtrip-domain evidence gives the exact predicate
  `(p − B) mod 2^64 < 2^32`.

No run was repeated and no FP or base value was invented. The earlier records stay as published:
[`../fable-returns-0928e/`](../fable-returns-0928e/README.md) and its `three_check.py`, and
[`../three-check-input-binding/`](../three-check-input-binding/README.md) with its outputs.

[`domain_check.py`](domain_check.py) ([output](domain_check.out)) checks two things:
- **W1:** for a base within 4 GiB of the top, the round trip follows the modular predicate and not the interval
  reading (`p = 5` round-trips at `B = 2^64 − 2^31`). For the non-wrapping example base the two readings agree.
- **Q1:** each consumer carries its clause.

The controls (C) are a page copy with the clause removed, and the interval test in place of the modular one; both fail.

| consumer | action | agreement |
|---|---|---|
| shared-neighbours page, the `00229E70` row | completion clause and DAZ added to the 2026-09-28 correction | revised-here |
| shared-neighbours page, the `0020E620` row | the window stated as modular, pointing at §4c, which already gives the predicate | revised-here |
| `CONTRACT-widget-object.md`, the `00229E70` paragraph | completion clause added | revised-here |
| starting-a-widget-animation page, the `00229E70` item | completion clause added | revised-here |
| `three-check-input-binding/README.md` (the bound producer's record) | R1 completion and I1 modular-window qualifiers added as a new section; the published script and output are unchanged | revised-here |
| OPUS's rate-field repair (already consumed at 061f / e867) | not repeated | unchanged |

Still open: the game's MXCSR at `00229E70`, and whether any live base wraps.

Regression: `domain_check.py` (W1, Q1, C). Run verified at 643af80c4: FAILS 0.
