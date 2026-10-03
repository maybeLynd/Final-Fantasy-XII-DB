# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-the-status-write-and-its-side-effects-1002)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-THE-STATUS-WRITE-AND-ITS-SIDE-EFF` · Package: `_index/candidates/fable-home-the-status-write-and-its-side-effects-1002/` · Page: `10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md`

## SWE2-AUDIT-SPEC verdict: REJECT

## SWE2-AUDIT-SPEC checks

- `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 5 functions, 25 anchors` / `ALREADY` / `FAILS 0`. Without `--apply` it only verifies; `ALREADY` means the section is already on the page. It wrote nothing.
- `rows.json`: 5 rows, 25 anchors; mechanically rejected 1, skipped 0, missing 0.
- Semantic pass: **all 5 rows** read clause by clause against the full `disr.py` disassembly of the certified image (rip targets resolved; image-base-relative forms rebased on `00120000`). Every call offset, stack-argument slot, compare signedness and branch polarity was checked. Each entered_from site was disassembled and confirmed as a direct call or jump to the body. Host fit was checked against every citation of the caller on the page outside the homed section.
- `002C7620`: `rcx`'s `+0x18` is read before the unlink, only when `rdx == rcx` (`002C7628`); both neighbour fix-ups are null-guarded and both links are zeroed.
- `002EA1E0`: `shr eax,3; not eax; and eax,1` gives 1 when bit 3 is clear. The `add rcx, [022C6F28]` / `je` is the zero-address test.
- `003F19D0`: `comiss xmm0(cur), xmm1(new)` / `jbe` takes `+0xB0`, so equal and unordered go to `+0xB0`, as stated.
- `0035D570`: signed count test (`jle`) before the scan; `jl` loop.
- `002C7620`, `002EA1E0` and `0035D570` are called from `002C6F70`, which the page reads (*"called by `002C6F70`"*). `003F19D0`'s caller `003F0170` is cited only in passing (as the teardown that the page's `0028EE10` entry runs). That is weak but not disclaimed, so it stands.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC narrowing / notes

- **`00322950` (entered from `002C7660`): host-fit defect.** The page cites `002C7660` once, in *"UI - MECHANICAL ... shared by UI bodies (`002915C0`, `002C7660`, ...) - the command-record constructor and the measure/transform primitives' fan-in, not a UI relationship to the status write"*. The body is an enmity probe: `02089340` bit `0x10`, then `ActorHandle_ResolveRegistryEntryByPackedId` -> `ActorWork_GetBattleUnitRaw` -> `BattleEnmity_AnyAboveThreshold(unit, 0)`, with `sete` (`00322982`). The row's sentence, site and anchors are exact; only its host is wrong, and the section heading (*"called from this page's functions"*) is false for it, because this page says the caller is not one of its functions.
  - **Repair:** remove the `00322950` row from this package (and from the section already on the page: the applier prints `ALREADY`), and re-home it unchanged on `04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md`, which tables `002C7660` as the per-unit overhead-display evaluation. 16-UI/Battle-Hud/the-battle-hud-layout-readers.md, which answers the `002C7660` parent (SD-128), is the alternative.
- The other four rows are exact and stay.
