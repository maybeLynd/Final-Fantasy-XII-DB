# Registry slot 0x02EBF200: field +0x11C's raw pack index for license_board.bin, and no reader (OPUS, 2026-10-01)

The dashboard's R family had one requirement left: registry slot `0x02EBF200`, "read the slot's principal consumer and
declare it". The table-registry page already named the slot `license_board` (`00236C30`'s direct store of `+0x11C`),
but never declared it in `registry_slots:`. Its rule is to declare a slot only where the document establishes what the
slot holds.

## What the slot holds and who reads it (OPUS)

`slot200_check.py` (static, the certified image) gives 11 PASS, FAILS 0 ([`slot200_check.out`](slot200_check.out)):
- **S1, what is stored.** `00236C30` stores the `0208E680` record's field `+0x11C` raw: `movsxd rcx, [rax+0x11c]` at
  `0023702A`, then `mov [02EBF200], rcx` at `00237031`. It does not go through the registrar `003845F0(&slot, field)`,
  which binds every neighbour (control: the `02EBF008` slot at `00237010`). So the slot holds the pack-entry index
  that names `license_board.bin`, not a loaded table.
- **S2, direct readers.** A rip-relative sweep of `.text` finds exactly one reference to `02EBF200`-`02EBF207`, that
  write. Positive control: the neighbour `02EBF1F8` shows its read at `002385A9`.
- **S3, indexed readers.** Every indexed access through the job-board base `02EBF1A0` is bounded to that base's twelve
  slots, `02EBF1A0` to `02EBF1F8`:
  - `00233E00`: `cl <= 0xB`, and its count loop stops before `02EBF208`, with its widest read at `02EBF1F8`;
  - `002368D0`: `rep stosq` over 12 qwords;
  - `00237630` and `00238260`: `cl <= 0xB`;
  - `00328990`: `r8d <= 0xB`.

So the slot is **written once and read nowhere**. No table is loaded for `license_board.bin` through this registry,
which fits that page's finding that the file is unlike the twelve job boards.

## Applied (OPUS)

`authored-data-table-registry.md`:
- `registry_slots:` gains `"0x02EBF200"`.
- The binder list's license_board line gains the finding above.
- `check_formats.claimed_slots` now claims 64 of 64 slots.
- `adrift_report.py` reports 0 refused rows.

run: slot200_check.py (FAILS 0); claimed_slots 64 of 64; adrift_report.py refused rows 0

## Review (OPUS)

This goes to SWE2-AUDIT-SPEC (OPUS-lane production).
