# SWE2-AUDIT-SPEC review: OPUS homing rows (opus-how-the-engine-chooses-3d-or-flat-moveme-homing-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-HOW-THE-ENGINE-CHOOSES-3D-OR-FLAT-MOVEME-HO` · Package: `_index/candidates/opus-how-the-engine-chooses-3d-or-flat-moveme-homing-1002/` · Page: `06-Movement-And-Navigation/Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh (verify mode) -> exit 0, `VERIFY 2 functions, 10 anchors / ALREADY / FAILS 0`.
- `rows.json`: 2 rows, 10 anchors; rejected 0, missing 0.
- **Entry.** The class file's direct callers were checked at the bytes. `0034EB30` + 0x0 is `jmp 0x3b79d0` (a 5-byte thunk). `003B8140` + 0xC and `003B8170` + 0xC are each `call 0x3b7d80`. A raw census finds no other branch site.
- **Host fit.** `003B79D0` calls `0017F5B0` and `002EB030`. `003B7D80` calls `00263F40` and `0026B720`. The page documents all four, so the homing premise holds.
- **Semantic pass, all 2 rows.** Both exact.
  - `003B79D0`: the `cmp [022BE970],0` / `je` gate around `0017F5B0(1)`; the count `02EBCBC0` is tested `jle`, then re-read at `003B7A13` only after a call; `002EB030(entry, 0x1049)` runs on non-null entries.
  - `003B7D80`: the count `02EBCC60` is compared signed (`jle`/`jl`) and re-read each pass; the record lookup is the direct call at +0x3C (`003B7DBC call 0x359b80`); on a non-null record, `0026B720(rbp, [rax+0x10], [rax+0x14], [rax+0x18])`, where `rbp` = `00263F40(entry)`.

## SWE2-AUDIT-SPEC narrowing / notes

- Note, not a defect (`003B7D80`): `00263F40(entry)` is called at `003B7DB1` for **every** non-null entry, before the lookup and not only when a record is found. The row's nested form leaves that order implicit. `00263F40` is a resolver: `cmp byte [rcx+0x18],1`, then `003587C0`, then `cmovne`. It writes no memory, so no stated fact is false.
