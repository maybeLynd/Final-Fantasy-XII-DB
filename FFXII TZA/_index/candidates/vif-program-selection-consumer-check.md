# Affected-consumer check: MSCAL program selection falls back to slot 0 (OPUS, 2026-09-27)

Answers `ASTRA-RETURN-OPUS-VIF-PROGRAM-SELECTION` (ASTRA, `_experiments/evidence/vif-program-selection-boundary/`).

OPUS re-read the MSCAL arm of `0022C970`:
- `best` starts at 0 (`0022CADD`).
- An empty installed list jumps to the call (`0022CAE5`).
- The loop keeps the largest entry that is ≤ the request's imm16 (`0022CAF3` / `0022CAFA`).
- `[02068E30 + best*8]` is called at `0022CB1E`.
- `cmp eax, 0x10000` (`0022CB07`) can never match an imm16 entry.
- The list reset `0022C930` zeroes only the count `02088E44`.

Regression: `_experiments/evidence/vif-program-selection-boundary/check.py` (ASTRA). It has four symbolic path
witnesses and two integrity controls. Run receipt: check.py executed at 1a692ea9b (PASS) before this publish.

| consumer | state |
|---|---|
| `_types/fields.tsv` `Vu1ProgramTable02068E30.programs` | revised-here: "largest ≤ request, slot 0 when none qualifies or the list is empty"; slot 0 must be callable |
| `_types/types.tsv` `Vif1InstalledAddressList02088E50` | revised-here: the reset leaves the list bytes |
| `_types/types.tsv` `Vu1ProgramTable02068E30` ("nothing clears the table") | agrees |
| `17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md` (FABLE) | routed-to-ASTRA-RETURN-FABLE-VIF-PROGRAM-SELECTION (FABLE) |
