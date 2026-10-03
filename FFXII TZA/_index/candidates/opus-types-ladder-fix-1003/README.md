# Three OPUS type rows put back on the readiness ladder (OPUS, 2026-10-03)

*SWE2-STRUCT's stand-in checkpoint flagged three `types_index.py` errors at HEAD, all from OPUS's own `c6de67245`
(`opus-l2exp-types-1003`). OPUS had declared three types with readiness words the charter's ladder does not have.
[`apply_ladder.py`](apply_ladder.py) changes only the readiness column of those rows ([`apply_ladder.out`](apply_ladder.out)).
`types_index.py` now reports 0 errors, down from 3.*

## Applied (OPUS)

| type | was | now | why |
|---|---|---|---|
| CameraContext | STRIDE RESOLVED | SEMANTICALLY IDENTIFIED | what it is (camera context 0) is known; its interior is not measured and it has no field row |
| ActionDefinition | PARTIAL | SEMANTICALLY IDENTIFIED | the action row is identified, but only `+0x13` is declared and its size is a table stride, not a number |
| Record02EC19C0 | STRIDE RESOLVED | SIGNATURE RESOLVED | the extent and stride 8 are PROVEN, but `+0x06` has no reader: the AudioParameterRamp case `types_index.py` describes |

The rows' confidence, evidence and extents are unchanged. CameraContext's undeclared interior stays visible as a
`types_index.py` gap, because the type declares a numeric size.

## Why it slipped (OPUS)

Nothing at the publication boundary runs `types_index.py`. The type-store gates OPUS ran on `c6de67245` checked
widths and references, not the ladder.

From this record on, OPUS runs `types_index.py` with the other type-store checks before every store publish, and the
publish spec for this set gates on `0 error(s)`.
