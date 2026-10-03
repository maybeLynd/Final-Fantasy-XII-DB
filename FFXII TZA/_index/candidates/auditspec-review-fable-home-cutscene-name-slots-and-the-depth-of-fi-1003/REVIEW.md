# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-cutscene-name-slots-and-the-depth-of-fi-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-CUTSCENE-NAME-SLOTS-AND-THE-DEPTH` · Package: `_index/candidates/fable-home-cutscene-name-slots-and-the-depth-of-fi-1003/` (committed in `410ec4476`, reviewed at HEAD `f49bb4021`; the package is unmodified in the working tree) · Page: `99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The one row is exact against the bytes.

- The host is defensible on data. The page decodes the VIF1 UNPACK header `0x6C0D800010000000` and names its four writers in an immediate census, `00271760` among them (line 1444).
- The body fills the payload that `00271760` writes right after that header (`rcx` = header + 0x10).

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The section heading is at page line 1844 and the row (line 1850) matches `rows.json` byte for byte.
- **rows.json.** 1 row, 5 anchors. Rejected 1 (`002EC960`, "already cited by" this page; the page does cite it), skipped 0, missing 0.
- **`00276190` (0x85 B).**
  - Four `mov dword [rcx+0x80..0x8C], 0x44FFF000` (2047.0) and four `0x3F800000` stores at `+0xC0..0xCC`.
  - `00202C70(rcx+0x40, 02AEDDB0)` at +0x6B, then a tail `jmp 00202C70` at +0x80 with `(rcx, rdx)`, `rdx` restored from `rbx`.
  - Exact.
- **entered_from.** `00271760` + 0x24 = `00271784`, `call 00276190`, with `rcx = rdx + 0x10`. It is the only caller (raw index). `00271760` then writes the header words `0x10000000` ×3 / `0x6C0D8000` at `+0..+0xC` of that block (`0027179D`-`002717B6`). This is the census line on this page.
- **Host fit.** The caller is cited as one of the four writers of the header that this page's emitter `002DC290` also writes. The body writes that header's payload, so this page explains its data. Apart from `_index/ADDRESS-INDEX.md`, no other page cites `00276190`.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC advisories (not defects)

- `00271760` itself is not read as a body on any page. Its only caller is the settings-menu plate draw `003F6850` (`19-Save-Load-Settings/Game-Settings-Config/the-settings-command-table.md`, line 883: "`00271760` draws from `[rbp+0x30]` through the staged matrix"). When `00271760` is homed, this row could move with it. A pointer from the row to that page would help now.
- `00202C70` is the 4x4 copy behind `Matrix4x4f_Copy` (`0046D100`). Naming it would read better than "the same callee".
