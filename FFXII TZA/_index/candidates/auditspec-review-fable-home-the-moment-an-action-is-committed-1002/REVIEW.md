# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-the-moment-an-action-is-committed-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-THE-MOMENT-AN-ACTION-IS-COMMITTED` · Package: `_index/candidates/fable-home-the-moment-an-action-is-committed-1002/` · Page: `07-Combat-Action/the-moment-an-action-is-committed.md`

## SWE2-AUDIT-SPEC verdict: REJECT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 1 row, 5 anchors; mechanically rejected 0, skipped 0, missing 0.
- Semantic pass: **the 1 row** read clause by clause against the full `disr.py` disassembly of the certified image. Every call offset and branch polarity was checked. The entered_from site `00310A67` was disassembled and confirmed as `call 00310D30` (with `rcx = r12`, `xmm1 = xmm6`). Host fit was checked against every citation of the caller on the page outside the homed section, and the caller was grepped across the database.
- `00310D30`: `rdi = rcx`, `xmm6 = xmm1`. Then `call 00327270` (+0x15) with the incoming registers, and `test rax, rax; je` to return. On the returned pointer it calls `0026B0C0` (+0x33) with `xmm1/xmm2/xmm3 = [rdi]/[rdi+4]/[rdi+8]`, then `Actor_SetDesiredMovementHeading` (+0x3E) and `Actor_SetFacingHeading_Variant1` (+0x49), each with `xmm1 = xmm6`. Exact. The sentence's `rcx+0x0`/`+0x4`/`+0x8` means the incoming `rcx` (`rdi`); at the call `rcx` holds the returned pointer. Writing "incoming `rcx`" would remove that ambiguity. This is not a defect.
- The sentence, site and anchors are exact. The defect is host fit.

## SWE2-AUDIT-SPEC narrowing / notes

- **`00310D30` (entered from `00310920` + 0x147): host-fit defect.** The page cites `00310920` once outside the homed section, inside the *"Movement — CLIENT and SERVICE (35 edges)"* neighbours paragraph: *"`0025B470`, `0026C3E0`, `002E28E0`, `00310920` and `00313670` call `00377C20`"*. That files it as a Movement-layer body calling a shared predicate, not one of this page's functions. The section heading (*"called from this page's functions"*) is false for this row. The body publishes a position triple and two headings, which is not this page's subject.
  - **Repair:** remove the row from this package (and from the section already on the page: the applier prints `ALREADY`), and re-home it unchanged on `06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md`. That page reads `00310920` as the facing-publish record loop (L880 *"facing publish, record loop `00310B00`, `00310BB1`, `00310CA6` (`00310920`, caller `0037D000`) `xmm6` — caller argument"*, L909, L918), which is what this body does with the same `xmm6` heading.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
