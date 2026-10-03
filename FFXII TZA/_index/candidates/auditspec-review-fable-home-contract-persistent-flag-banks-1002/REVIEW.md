# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-contract-persistent-flag-banks-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-CONTRACT-PERSISTENT-FLAG-BANKS-10` · Package: `_index/candidates/fable-home-contract-persistent-flag-banks-1002/` · Page: `14-Story-Event-Quest-Hunt/CONTRACT-persistent-flag-banks.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 1 row, 5 anchors; mechanically rejected 2, skipped 0, missing 0.
- Semantic pass: **the 1 row** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved; image-base-relative forms rebased on `00120000`). Every call offset, stack-argument slot, compare signedness and branch polarity was checked. Each entered_from site was disassembled and confirmed as a direct call or jump to the body. Host fit was checked against every citation of the caller on the page outside the homed section.
- `002A3210`: `((r9d << 18) ^ d) & 0x40000 ^ d` puts bit 0 of `r9d` into bit 18, then `bts 0x11` sets bit 17. The byte stores go to `+0x174` (`dl`) and `+0x175` (`r8b`), and the dword is written back at `002A323B`.
- Host: `002E16B0` is cited as a bank client (*"the message-window opener `002E16B0` (`SetBank2048(actor +0x102, 1)`)"*). The body sets message-window fields, not a bank. That is weak, but the page treats the caller as a participant, so it stands.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
