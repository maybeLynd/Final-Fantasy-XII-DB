# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-section-002-text-cloudint-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-SECTION-002-TEXT-CLOUDINT-1003-0DCAD` · reviewed at HEAD `33eb7192f` · Package: `_index/candidates/opus-section-002-text-cloudint-1003/` · Page: `25-EBP-Script-Container/Sections/section-002-text.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh in verify mode (no `--apply`, writes nothing) -> exit 0, `VERIFY 2 functions, 9 anchors` / `ALREADY` / `FAILS 0`. The page block equals `rows.json`.
- `rows.json`: 2 rows, 9 anchors, `mode: interior`; rejected 0, skipped 0, missing 0. There are no homing rows, so the entered_from and host checks do not apply.
- Semantic pass: **all 2 rows** were read clause by clause against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). The request asks for at least 15; the package has 2, so all were read. Stack slots, branch and cmov polarity, signedness and argument registers were checked:
  - `002E1D50`: the clamp (`jns`, else 0; `cmovg` to 7), `movsxd`, `imul 0x68` on the `0215F200` base, and the four stores (byte 1 at `+0x3b`, `edx` at `+0x24`, `r8d` at `+0x28`, `r9b` at `+0x39`). Exact.
  - `002E1FD0`: the store itself is right, since every input stores `dl` at `0215F242 + i*0x68`. However, "on both of its paths" and the anchor `002E200B` treat the second store as a live path, and it is not (narrowing below).
- Limits hold: body statements only, static evidence. An OPUS self-draft plus OPUS's mechanical check is not independent review; this record is.

## SWE2-AUDIT-SPEC narrowing (exact wording)

**Narrowing (row `002E1FD0`).** The negative path (`002E1FD9`) stores at `002E1FEE`. The non-negative path clamps with `cmovg` at `002E1FF4`, leaving `ecx` in 0..7, and then `test ecx, ecx; jns 002E1FDB` at `002E1FF7`/`002E1FF9` is always taken, so it rejoins the same store at `002E1FEE`. `002E1FFB`..`002E200E`, including the anchored store `002E200B`, runs only if `ecx` is negative after the clamp, which cannot happen.

A raw image sweep (E8/E9 rel32, `0F 8x`, rel8, rva32, abs64) for targets `002E1FD0`..`002E200E` finds only:

- the call at `0033F9DC` to the entry;
- the two internal `jns`;
- three stray rva32 dwords. `0064F130` points to `002E1FFC`, which is mid-instruction. `01099EAD` and `01DFC59B` are odd-aligned dwords pointing to `002E2000` and are not jump-table slots.

Replacement wording:

> clamps `ecx` to 0..7 (signed) and stores `dl` at byte `0215F242` + `i`*0x68; both entry paths reach the store at `002E1FEE` (the non-negative one through the `jns` at `002E1FF9`), and the second copy of the store at `002E200B` is unreachable (it would need `ecx` negative after the clamp)

Anchors: replace `002E200B` (`mov`, dead) with `002E1FF9` (`jns`), giving `002E1FDD`, `002E1FEE`, `002E1FF4`, `002E1FF9`. The producer applies the narrowing and re-runs the applier.
