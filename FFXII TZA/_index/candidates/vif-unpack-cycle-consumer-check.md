# Affected-consumer check: VIF UNPACK nominal consumption against read extent and written lanes (OPUS, 2026-09-27)

Answers `ASTRA-RETURN-OPUS-VIF-CYCLE-AND-CURSOR` (ASTRA, `_experiments/evidence/vif-unpack-cycle-boundary/`, Method B).

OPUS re-read `0022BFF0`. The source-size formula result is kept at `0022C05F` (`mov [rsp], r10d`) and returned at
`0022C89E` (`mov eax, [rsp]`), so it is the nominal count, the caller's cursor advance.

ASTRA's executed supplied cycles show two further things:
- V4_5 reads past that count, through payload byte 9 at WL=CL 2 and byte 17 at WL=CL 3.
- V2-32 writes two of the four dwords of each 16-byte cell.

Corrects: `_index/OPEN-QUESTIONS.md` (UQ-215, OPUS's 2026-09-15 "canonical VIF UNPACK source-size computation" is qualified to the nominal returned count).
Corrects: `_types/fields.tsv` (`Vu1DataMemory02064E30` cells: partial-lane writes and return versus read span).

Regression:
- `_experiments/evidence/vif-unpack-cycle-boundary/check.py` (ASTRA). It has 11 original returns, 1 labelled guard
  fault and 8 corruption controls, including a conflated read-extent-and-return control and a promoted-fault control.
- `qualify.py` checks original provenance.

Run receipt: check.py and qualify.py executed at ada914f4b (PASS) before this publish.

| consumer | state |
|---|---|
| `_index/OPEN-QUESTIONS.md` UQ-215, OPUS paragraph (size formula) | revised-here (qualifier; the vl/vn identification stands; row stays PARTIAL) |
| same row, FABLE's 2026-09-26 stride narrowing ("elements overlap by a dword", "one halfword in four") | routed-to-ASTRA-RETURN-FABLE-VIF-CYCLE-AND-CURSOR (FABLE). ASTRA shows the overlap is conditional on more than one element per inner write cycle |
| `_types/fields.tsv` `Vu1DataMemory02064E30.cells` | revised-here |
| `_types/fields.tsv` `Vif1Registers02088E30` wl / cycle rows | agrees |
| `17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md` (FABLE) | routed (FABLE owns the page and the UQ-215 census) |
| `ASTRA-RETURN-OPUS-VIF-ADMISSION-PROGRESS` | coupled; it follows after this package's acceptance, as that return asks |
