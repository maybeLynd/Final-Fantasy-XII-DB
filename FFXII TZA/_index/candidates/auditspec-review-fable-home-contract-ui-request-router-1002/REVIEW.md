# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-contract-ui-request-router-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-CONTRACT-UI-REQUEST-ROUTER-1002` · Package: `_index/candidates/fable-home-contract-ui-request-router-1002/` · Page: `16-UI/CONTRACT-ui-request-router.md`

## SWE2-AUDIT-SPEC verdict: REJECT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 3 functions, 15 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 3 rows, 15 anchors; mechanically rejected 0, skipped 0, missing 0.
- Semantic pass: **all 3 rows** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved; image-base-relative forms rebased on `00120000`). Every call offset, stack-argument slot, compare signedness and branch polarity was checked. Each entered_from site was disassembled and confirmed as a direct call or jump to the body. Host fit was checked against every citation of the caller on the page outside the homed section.
- `0037E8A0`: `movzx eax, word [rdx+0xA]; cmp ecx, eax; jge` is the signed bound. The `01CEB638` return is shared by the null and out-of-range paths; the tail `jmp 002F9920` takes `ecx = [rdx+0xC+ecx*8]`.
- `0037F3B0`: pair `[rsp+0x20]` = 0x10000 and `[rsp+0x28]` = `rcx`; block `[rsp+0x30]` 0, `[rsp+0x38]` &pair, `[rsp+0x40]` 0; `00244F50(0x5F0, 0037F4D0, &block)`. Both exits pass through `__security_check_cookie`.
- `003EBD70`: the text is exact (the `02B5EC60` store precedes the `02B5EC68` null test; four trailing qword zeroes; `xor eax, eax` return).
- Host: `003F4E70` is the page's message handler (R-4), so `0037E8A0` and `0037F3B0` fit.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC narrowing / notes

- **`003EBD70` (entered from `002628B0`): host-fit defect.** The page cites `002628B0` once, in *"ActorEntity - SERVICE ... `00252DE0`/`0026A5F0`/`0026DB30` answer callers like `002628B0`/... - actor-side bodies consume the router's request helpers; service crossing, not ownership"*. `002628B0` is the area unload (site `00262A7D`), and the body clears the `02B5EC60`..`02B5EC88` block, which this page does not discuss. The row's sentence, site and anchors are exact; only its host is wrong, and the section heading (*"called from this page's functions"*) is false for it, because this page says the caller is not one of its functions.
  - **Repair:** remove the `003EBD70` row from this package (and from the section already on the page: the applier prints `ALREADY`), and re-home it unchanged on `00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md`, which reads `002628B0` as the unload it calls for each set bit (04-Actor-Entity/CONTRACT-field-runtime-pass.md, which anchors the unload, is the alternative).
- The `0037E8A0` and `0037F3B0` rows are exact and stay.
