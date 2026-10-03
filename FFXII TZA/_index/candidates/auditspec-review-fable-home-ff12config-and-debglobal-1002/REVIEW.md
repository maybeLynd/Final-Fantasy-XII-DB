# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-ff12config-and-debglobal-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-FF12CONFIG-AND-DEBGLOBAL-1002` · Package: `_index/candidates/fable-home-ff12config-and-debglobal-1002/` · Page: `19-Save-Load-Settings/Game-Settings-Config/ff12config-and-debglobal.md`

## SWE2-AUDIT-SPEC verdict: REJECT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 1 functions, 4 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 1 row, 4 anchors; mechanically rejected 1, skipped 0, missing 0 (README; FABLE's correction added the folded-stub clause).
- Semantic pass: **the 1 row** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved). Branch and `cmov` polarity were checked. The entered_from site `0050C8C4` was disassembled and confirmed as `jmp 00314D60` (a tail jump, after `mov ecx, 1`). Host fit was checked against every citation of the caller on the page outside the homed section, and the caller was grepped across the database.
- `00314D60`: `mov ebx, ecx`; `call 005C5230` at +0x8; `xor edx, edx; test eax, eax; cmovne edx, ebx`; `mov [022C2540], edx`. The polarity is as stated (`ecx` on non-zero, 0 on zero). `005C5230` reads `xor eax, eax; ret` in the image, so the stored value is always 0. Exact.
- The sentence, site and anchors are exact. The defect is host fit.

## SWE2-AUDIT-SPEC narrowing / notes

- **`00314D60` (entered from `0050C8A0` + 0x24): host-fit defect.** The page cites `0050C8A0` once outside the homed section, in the neighbours line *"Script_VM_Native_Bridge - CLIENT and SERVICE (11 edges). `0032FC30`, `00314440`, `00408EC0` are also called by bodies filed to script VM / native bridge: `0034B650`, `00355350`, `0050C8A0` (+7 more) ... shared machinery across the layer boundary, no shared ownership."* The page files the caller as a script-VM body. It is: `VMValueStack_PopInt32CoerceFloat32`, then `WorldTransition_RequestFieldTransition(eax, 0, 0, 0)`, then a tail jump to this body with `ecx = 1`. The page never reads it as its own. `022C2540` appears nowhere on the page outside the homed row. The section heading (*"called from this page's functions"*) is false for this row.
  - **Repair:** remove the row from this package (and from the section already on the page). No page reads `0050C8A0` as its own: it is cited only in this neighbours line. The natural home is `01-Script-VM-Native-Bridge/verbs-that-only-wait-and-verbs-that-do-nothing.md`. That page reads the sibling setter `00314D40` (`disposesummon` calls `00314D40(1)`, L247/L293) and the folded stub `005C5230`, and this body is exactly a verb effect folded to a constant. Re-home the row unchanged there through the non-caller stream, or once that page cites `0050C8A0`.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
