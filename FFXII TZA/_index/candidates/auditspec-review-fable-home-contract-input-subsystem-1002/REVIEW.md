# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-contract-input-subsystem-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-CONTRACT-INPUT-SUBSYSTEM-1002` · Package: `_index/candidates/fable-home-contract-input-subsystem-1002/` · Page: `15-Input/CONTRACT-input-subsystem.md`

## SWE2-AUDIT-SPEC verdict: REJECT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 1 row, 5 anchors; mechanically rejected 1, skipped 1, missing 0 (README).
- Semantic pass: **the 1 row** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved). Every call offset, compare signedness and branch polarity was checked. The entered_from site `003427F3` was disassembled and confirmed as `call 00361480`. Host fit was checked against every citation of the caller on the page outside the homed section, and the caller and the table were grepped across the database.
- `00361480`: `r8 = 022CB9F0`, `r9d = -5`, `edx` counts 0..3 (`cmp edx, 4; jl`), stride `0x18`. For a non-zero `+0` byte, `movzx eax, byte [r8+1]; cmp eax, ecx; jne`, then a match returns `edx`. For a zero `+0` byte, `cmp r9d, -5; jne` keeps only the first empty index, stored as `not edx`. The fall-through returns `r9d`. The sentence is exact; `~index` for 0..3 can never equal -5, so the two outcomes are distinguishable.
- The sentence, site and anchors are exact. The defect is host fit.

## SWE2-AUDIT-SPEC narrowing / notes

- **`00361480` (entered from `00342770` + 0x83): host-fit defect.** The page cites `00342770` once outside the homed section, in *"Script_VM_Native_Bridge — CLIENT, OUT-OF-SCOPE (65 edges). 56 script-verb bodies, among them `0033F330`, `00342770`, ... call `00267310`..."*. The page files the caller as an out-of-scope script verb, so the section heading (*"called from this page's functions"*) is false for this row. The body searches the four 24-byte audio track slots at `022CB9F0`, which this page does not discuss. `18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md` owns that table (L443 *"`022CB9F0` audio track slots, 4 x 24 B, `+0` state, `+1` key"*, L659) and its two sibling scans, `00360C20` `AudioTrack_FindSlot` and `00361630` `AudioTrack_FindOrReserveSlot`. `00342770` itself calls `00361630` at `003427D6`, just before this site.
  - **Repair:** remove the `00361480` row from this package (and from the section already on the page: the applier prints `ALREADY`). No page reads `00342770` as its own: it is cited only here, in the out-of-scope line. So the row cannot be caller-hosted. Re-home it unchanged through the callee/table stream on `18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md`, next to `00360C20`/`00361630`, or have that page cite `00342770` first and then caller-home it there.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
