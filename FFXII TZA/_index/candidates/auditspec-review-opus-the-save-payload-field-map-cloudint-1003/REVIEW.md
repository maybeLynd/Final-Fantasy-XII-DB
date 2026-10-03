# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-save-payload-field-map-cloudint-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-SAVE-PAYLOAD-FIELD-MAP-CLOUDINT-1-FC4D1` · reviewed at HEAD `33eb7192f` · Package: `_index/candidates/opus-the-save-payload-field-map-cloudint-1003/` · Page: `19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh in verify mode (no `--apply`, writes nothing) -> exit 0, `VERIFY 7 functions, 33 anchors` / `ALREADY` / `FAILS 0`. The page block equals `rows.json`.
- `rows.json`: 7 rows, 33 anchors, `mode: interior`; rejected 0, skipped 0, missing 0. There are no homing rows, so the entered_from and host checks do not apply.
- Semantic pass: **all 7 rows** were read clause by clause against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). The request asks for at least 15; the package has 7, so all were read. Stack slots, branch and cmov polarity, signedness and argument registers were checked:
  - `002E13C0`: the jump table was read raw at `002E1428` (10 dword offsets rebased on `00120000`): 0 -> `002E13E1` (0), 1 -> `002E13E6` (1), 2 -> `002E13EE` (9), 3..7 -> `002E13F6`..`002E1416` (0x12..0x16), 8 -> `002E1423` (the default arm, 0x1D), 9 -> `002E141E` (0x1E). `cmp ecx, 9; ja` is unsigned. Exact.
  - `00264870`: the three zero-returns (bit test on `02098E20`, null `02098E10`, null first `0020E600`), the second `0020E600` call `movsxd`-added to the qword, `cmp edi, [rcx]; jge` (signed, `ecx` sign-extended) and `b + 4 + ecx*0x10`. Exact.
  - `0026ABA0` (`jge` signed on 0x100), `003F6FD0` (`test dx, ax` with 0xfffb; 4 when the word is 1, else 3), `00473B90` (`cmp [t+4], ecx; jle` to -1, AND 0x1FFF) and `00862930` (four `mulss` by 16.0 at `01CEBC84`, `.rdata`, `cvttss2si`): exact.
  - `00249080`: the call, the signed `test rbx, rbx; jle` count guard, the per-entry `sub 0x8000` / `sar 4` and the `divss` / `cvttss2si` / `sar 1` order are exact. The two cells it reads are not constants (narrowing below).
- Limits hold: body statements only, static evidence. An OPUS self-draft plus OPUS's mechanical check is not independent review; this record is.

## SWE2-AUDIT-SPEC narrowing (exact wording)

**Narrowing (row `00249080`).** `01E0C1D8` and `01E0C1DC` are `.data` dwords, and `0024B120` writes them: 0x780 / 0x438 when its `ecx` is non-zero (`0024B124`, `0024B12E`), 0x200 / 0x1C0 when it is zero (`0024B139`, `0024B143`). The row states the image values as if they were the operands. A rip sweep of `.text` found these two stores as the only writers. Replacement wording:

- "plus the truncated 0x200 (`01E0C1D8`, as a float) / `00183280()` shifted right 1" -> "plus the truncated float of dword `01E0C1D8` (re-read for each entry; 0x200 in the image, set to 0x780 or 0x200 by `0024B120`) / `00183280()`, shifted right 1"
- "plus dword `01E0C1DC` (0x1C0) shifted right 1" -> "plus dword `01E0C1DC` (0x1C0 in the image, set to 0x438 or 0x1C0 by `0024B120`) shifted right 1"

Everything else in the row stands. The producer applies the narrowing.
