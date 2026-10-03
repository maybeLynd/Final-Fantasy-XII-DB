# SWE2-AUDIT-SPEC review: ASTRA OV-42 slot-ID producer

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session) · 2026-10-03 ·
Task: `ASTRA-REQ-SPEC-OV42-SLOT-ID-1002` · Package: `_experiments/evidence/ov42-slot-id-producer/`
(publisher commit `0ada51452`), image pin `73461d08…21f8`.

## SWE2-AUDIT-SPEC verdict: ACCEPT

Local slot admission does **not** exclude IDs 511..534.

## SWE2-AUDIT-SPEC re-derivation from the shipping image

- **`0030D070` (`BattleAction_AllocatePresentationSlot`):**
  - Scans 32 slots of 30h bytes at `022C17B0` for WORD `+1Ch` == `FFFFh`.
  - The incoming DX appears only as `movzx r10d,dx` and the final `mov word [rcx+1Ch],r10w` (`0030D14F`). There is
    no ID or category check and no native call.
  - When all 32 slots are full it returns `AL=FFh` (`0030D0BA`) with no own non-frame write.
  - The `0030D14F` store belongs to `30D070`, not to `30CFB0`.
- **Wrapper `0030CFB0`:**
  - `movzx ebx,r8w` passes the ID to `30D070` as EDX; ESI (identity) goes as ECX; the result AL is stored to
    `unit+4`.
  - The existing-unit gate (`byte [rcx+4] != FFh` skips) is preserved.
  - So is the bit-30 / `022C2158` bit-1 gate: when the row flag `+0Ch` bit 30 is set and the ID is outside
    D0h..F1h (or the mode is not 5/6), a set bit 1 skips; otherwise it ORs 2 and allocates.
- **Supplied `FFFF`:** it would leave the slot looking free even though the other fields were written, as the
  package says. Natural FFFF, reuse and list consequences stay OPEN.

## SWE2-AUDIT-SPEC reproduction (disposable copy, repository-root cwd)

- `prove.py` re-run: exit 0, output **byte-identical** to `result-01.json`.
- `control.py` re-run: `control-result-01.json` **byte-identical**. Its three CLI refusals are missing capture
  status, failed capture exit and missing retained source.
