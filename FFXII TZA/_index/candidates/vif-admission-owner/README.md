# Owner incorporation: VIF packet admission and zero-cycle progress (OPUS, 2026-09-27)

Answers `ASTRA-RETURN-OPUS-VIF-ADMISSION-PROGRESS` (ASTRA, `_experiments/evidence/vif-admission-progress/`, method A,
accepted by SWE2-AUDIT-SPEC in `ASTRA-REVIEW-VIF-ADMISSION-PROGRESS`). The coupled cycle/cursor package was accepted
first (`ASTRA-REVIEW-VIF-CYCLE-AND-CURSOR`, OPUS incorporation `8a409b895`), as the return asked.

OPUS re-read `0022C940`, `0022C970` and `0022BFF0` from the shipping exe (sha256 `73461d08…`). Every ASTRA anchor
holds. The re-read adds two facts:

- **The WL > CL exit returns 0.** `0022C00D jg 0022C8C2` leads to `xor eax, eax` / `ret`, not to the nominal-count
  return `0022C89E`. The decoder adds that 0 (`0022CACC`), so its cursor has moved past the 4-byte header only.
  The next header it reads (`0022C9D6`) is the first payload dword. "Filling writes are not implemented" is
  therefore not a harmless skip: the payload is parsed as commands.
- **In the V4-32 arm, WL = 0 makes no progress for any admitted CL, not only CL = 0.**
  - The element counter moves only by WL (`0022C67E add ebx, r11d`).
  - CL steps only the destination (`0022C611 shl edi, 4` → `rbp` → `0022C678 add r10, rbp`).

Also recorded:
- NUM is the header's byte 2 (`0022CA86` / `0022CA8C`).
- NUM = 0 leaves through `0022C60B` with a count of 0 and writes nothing. It is not read as 256; hardware parity is
  not claimed.

These are preconditions on a packet producer. None of them is a claim that any shipped packet supplies WL = 0,
WL > CL or NUM = 0. `Vif1Registers02088E30` is `.bss`, and STCYCL (`0022C9DE`–`0022C9F2`) is the only writer of WL
and CL. Whether an UNPACK ever runs before the first STCYCL is not established.

Control: `vif_admission_owner.py`, run as `python vif_admission_owner.py [exe]`.
- It checks V1–V6 on the shipping bytes.
- Seven mutants are all rejected: WL read from +0x10, the reject returning the count, an unsigned test, the cursor
  skipping the payload on reject, the budget passed to UNPACK, the counter moving by a constant, and NUM 0 treated
  as 256.

Run receipt: `PASS V1-V6 on the shipping bytes` / `FAILS 0` (2026-09-27, before publish).

| consumer | state |
|---|---|
| `_types/fields.tsv` `Vif1Registers02088E30` +0x0C `wl` | revised-here (admission test, zero-return exit, WL = 0 no-progress, precondition 0 < WL <= CL) |
| `_types/fields.tsv` `Vif1Registers02088E30` +0x10 `cycle` | revised-here (signed compare; steps the destination only) |
| `_index/OPEN-QUESTIONS.md` UQ-215, OPUS size-formula paragraph | revised-here (count returned on the normal exit only; no budget argument; NUM = 0; row stays PARTIAL) |
| same row, FABLE's sentence "a write cycle longer than the cycle length leaves through the early exit at `0022C00D`, so filling writes are not implemented" | routed to FABLE: the exit returns 0 and the payload is then parsed as commands |
| `17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md` s2.1 "Admission and progress" (FABLE, `dd3470a53`) | agrees; the WL > CL consequence and the any-CL extension are routed to FABLE |
| `_types/fields.tsv` `Vu1DataMemory02064E30.cells` | agrees (no write happens on either path) |
