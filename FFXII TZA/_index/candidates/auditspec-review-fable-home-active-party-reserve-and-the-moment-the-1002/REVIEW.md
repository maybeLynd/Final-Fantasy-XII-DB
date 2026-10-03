# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-active-party-reserve-and-the-moment-the-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-ACTIVE-PARTY-RESERVE-AND-THE-MOME` · Package: `_index/candidates/fable-home-active-party-reserve-and-the-moment-the-1002/` · Page: `11-Party/active-party-reserve-and-the-moment-the-leader-changes.md`

## SWE2-AUDIT-SPEC verdict: REJECT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 1 functions, 2 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 1 row, 2 anchors; mechanically rejected 0, skipped 0, missing 0.
- Semantic pass: **the 1 row** read clause by clause against the full `disr.py` disassembly of the certified image. The entered_from site was disassembled and confirmed as a direct call to the body. Host fit was checked against every citation of the caller on the page outside the homed section.
- `0036F510` (18 B): `sub rsp, 0x28` / `call 003820C0` (`0036F514`) / `add rsp, 0x28` / `jmp 0026EB30` (`0036F51D`). The sentence is exact. `0022A770` + 0x12F = `0022A89F call 0x36f510`, confirmed.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC narrowing / notes

- **`0036F510` (entered from `0022A770`): host-fit defect.** The page cites `0022A770` twice outside the homed section, both times as an outside caller:
  - L458 names it as one of "the per-mode frame bodies", one of the seven sites of the commit thunk `00358BB0`.
  - L615 records its single `00324510` call (`0022AE6F`).

  The page never treats the field-frame body as one of its functions. The homed body is frame work with nothing to do with the party: `003820C0` is a 2,125-byte camera/frame body (`00229D20`, the `02AED4E0`/`02AED540` float cells), and `0026EB30` is a float/angle routine over `0209A2E0`. The section heading, *"called from this page's functions"*, is false for this row. The sentence, site and anchors are exact; only the host is wrong.
  - **Repair:** remove the `0036F510` row from this package, and from the section already on the page (the applier prints `ALREADY`). Re-home it unchanged on `00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md`. That page owns `0022A770` ("The `0022A770` exclusive subtree — the field frame's helper set", L479), and it already binds the neighbouring callees from the same call run: `0037D4C0` (`0022A89A`, L1902), `00256F60` (`0022A8A4`, L1914) and `0036F530` (`0022A8AE`, L1166).
