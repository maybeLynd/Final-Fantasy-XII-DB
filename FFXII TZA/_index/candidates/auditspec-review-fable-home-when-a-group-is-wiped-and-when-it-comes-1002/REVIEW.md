# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-when-a-group-is-wiped-and-when-it-comes-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-WHEN-A-GROUP-IS-WIPED-AND-WHEN-IT` · Package: `_index/candidates/fable-home-when-a-group-is-wiped-and-when-it-comes-1002/` · Page: `05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md`

## SWE2-AUDIT-SPEC verdict: REJECT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 5 functions, 20 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 5 rows, 20 anchors; mechanically rejected 0, skipped 0, missing 0.
- Semantic pass: **all 5 rows** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved; image-base-relative forms rebased on `00120000`). Every call offset, stack-argument slot, compare signedness and branch polarity was checked. Each entered_from site was disassembled and confirmed as a direct call or jump to the body. Host fit was checked against every citation of the caller on the page outside the homed section.
- `002FB250`: the ten byte stores are `022BE7F0`, `022BE810`, ... `022BE910` (stride 0x20, 0x120/0x20 + 1 = 10).
- `003C94A0`: `test dword [rax], 0x8000` / `jne` to the plain return, then `cmp [rax+4], ecx(=[rax+8])` / `jne` to the `003C93E0` tail-jump; the null and equal paths both reach the `02B47730` `+0xC8` store.
- `0028FE40` is entered through the 5-byte thunk `0035C150` (`jmp 0028FE40`); the page cites `0035C150` inside `003C8B70`'s call sequence, so that host fit holds. `002739B0` and `003C94A0` are called from `003C8B70` (`003C8F3F`, `003C90BB`), which the page reads, so they fit too.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC narrowing / notes

- **`002FB250` (entered from `00319B10`): host-fit defect.** The page cites `00319B10` (`Loot_InitializeWorldPickupPool`) once, in the boundary line *"`002342F0`, `00234590` reach bodies filed to rewards/progression: `00319B10`, `00319600` - shared machinery across the layer boundary, no shared ownership"*. The body, named `LootPresence_ClearAllSlots` in the function list, zeroes ten bytes at stride 0x20 (`002FB250`..`002FB28F`). The pool initialiser reaches it by a tail-jump at `00319C8E`. The row's sentence, site and anchors are exact; only its host is wrong, and the section heading (*"called from this page's functions"*) is false for it, because this page says the caller is not one of its functions.
  - **Repair:** remove the `002FB250` row from this package (and from the section already on the page: the applier prints `ALREADY`), and re-home it unchanged on `13-Rewards-Progression-Economy/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md`, which tables `00319B10` as `Loot_InitializeWorldPickupPool` (387 B).
- **`00363B00` (entered from `0026C5D0`): host-fit defect.** The page cites `0026C5D0` once, and only to say a primitive is *not* group code: *"All three have other callers (`0026C5D0`; `00359A30`, `0035A6F0`, `0035AB20`), so they are shared event-lock primitives, not group-specific."* The body stores `cl` into `022CBA9A` and, for `ecx == 1`, copies 16 bytes to `022CBB10` and `xmm2` to `022CBAAC` (`00363B00`..`00363B16`). No other line of this page cites those cells. The row's sentence, site and anchors are exact; only its host is wrong, and the section heading (*"called from this page's functions"*) is false for it, because this page says the caller is not one of its functions.
  - **Repair:** remove the `00363B00` row from this package (and from the section already on the page: the applier prints `ALREADY`), and re-home it unchanged on `00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md`, which tables `0026C5D0` as the handler of verbs `ucon` / `ucon_4a5`.
- The other three rows (`002739B0`, `0028FE40`, `003C94A0`) are exact and fit their host; they need no change.
