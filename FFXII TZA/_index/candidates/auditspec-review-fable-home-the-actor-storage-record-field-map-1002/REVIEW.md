# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-the-actor-storage-record-field-map-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-THE-ACTOR-STORAGE-RECORD-FIELD-MA` · Package: `_index/candidates/fable-home-the-actor-storage-record-field-map-1002/` · Page: `04-Actor-Entity/Actor-Storage-Record/the-actor-storage-record-field-map.md`

## SWE2-AUDIT-SPEC verdict: REJECT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 4 functions, 20 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 4 rows, 20 anchors; mechanically rejected 0, skipped 0, missing 0.
- Semantic pass: **all 4 rows** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved; image-base-relative forms rebased on `00120000`). Every call offset, stack-argument slot, compare signedness and branch polarity was checked. Each entered_from site was disassembled and confirmed as a direct call or jump to the body. Host fit was checked against every citation of the caller on the page outside the homed section.
- `002E4F40`: the null-`rcx` path goes through `002E4F5C` (`xor eax, eax; test rax, rax; je` to return 0). The `0xFFFF`, zero-sum and `+0x284 == 0` cases skip only the `00427300` call and still return 1. Exact.
- `002E9560`: 0.0 on the null and -1 paths, 30.0 (`008F8D80` = 0x41F00000) on the `0xFFFF`, zero-sum and zero-`+0x284` paths, and otherwise a tail-jump to `00423280`. Exact.
- `002E9C60`: 9 x 32 = 0x120 stride from `02161DA0`; `bt eax, edx` takes the register bit offset modulo 32. Exact.
- `00198730`: exact (`test al, 1`, `and al, 0xFE`, byte `+0x3B = 1`).
- Host: `002693D0` and `002E6BD0` are field-map accessor rows on the page, so those three rows fit.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC narrowing / notes

- **`00198730` (entered from `00182D60`): host-fit defect.** The page cites `00182D60` once, in a boundary-edge list (*"`00182D40`/`00182D60`/`00182DA0` (6 edges); `InputGameplay_ArbitrateDigitalInputAndModalState` ..."*). `00182D60` is `InputManager_GetSingleton()` followed by `jmp 00198730`, so the body's `rcx` is the input manager, not an actor storage record. Its bytes `+0x3A`/`+0x3B` are not fields of this page's record. The row's sentence, site and anchors are exact; only its host is wrong, and the section heading (*"called from this page's functions"*) is false for it, because this page says the caller is not one of its functions.
  - **Repair:** remove the `00198730` row from this package (and from the section already on the page: the applier prints `ALREADY`), and re-home it unchanged on `00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md`, which reads `00182D60` as one of the per-id side calls of the system-stop record write.
- The other three rows are exact and stay.
