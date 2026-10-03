# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-contract-world-simulation-tick-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-CONTRACT-WORLD-SIMULATION-TICK-10` · Package: `_index/candidates/fable-home-contract-world-simulation-tick-1002/` · Page: `00-Engine-Core-Runtime/Battle-Frame/CONTRACT-world-simulation-tick.md`

## SWE2-AUDIT-SPEC verdict: REJECT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 2 functions, 7 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 2 rows, 7 anchors; mechanically rejected 0, skipped 0, missing 0.
- Semantic pass: **all 2 rows** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved; image-base-relative forms rebased on `00120000`). Every call offset, stack-argument slot, compare signedness and branch polarity was checked. Each entered_from site was disassembled and confirmed as a direct call or jump to the body. Host fit was checked against every citation of the caller on the page outside the homed section.
- `002DEF20`: `xor r8d,r8d; mov r9d,edx; mov edx,ecx; lea ecx,[r8+1]; jmp 001DBD60`. The text is exact.
- `002DF1A0`: on the non-zero arm `[rsp+0x20]` after `sub rsp,0x38` is the fifth-argument slot, and it gets the incoming `r8d`. The text is exact.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC narrowing / notes

- **`002DEF20` (entered from `00332C40`): host-fit defect.** The page cites `00332C40` only in its boundary line: *"`00332750` ... calls Audio-owned `00332C40` for its `0x30`-stride marker probes ... the tick borrows Audio helpers through the executor, no audio state lives here."* The row's sentence, site and anchors are exact; only its host is wrong, and the section heading (*"called from this page's functions"*) is false for it, because this page says the caller is not one of its functions.
  - **Repair:** remove the `002DEF20` row from this package (and from the section already on the page: the applier prints `ALREADY`), and re-home it unchanged on `18-Audio/the-spatial-audio-object-model.md`, which lists `00332C40` / `003B99D0` among the first four callers into the spatial-audio object.
- **`002DF1A0` (entered from `003B99D0`): host-fit defect.** The page cites `003B99D0` only in that same Audio boundary line (*"shared `001EDDA0`/`00314020` entries carry Audio call traffic (`003B99D0`, ...)"*), as a foreign body. The row's sentence, site and anchors are exact; only its host is wrong, and the section heading (*"called from this page's functions"*) is false for it, because this page says the caller is not one of its functions.
  - **Repair:** remove the `002DF1A0` row from this package (and from the section already on the page: the applier prints `ALREADY`), and re-home it unchanged on `18-Audio/the-spatial-audio-object-model.md`, for the same reason.
- With both rows re-homed, nothing remains in this package. Withdraw it.
