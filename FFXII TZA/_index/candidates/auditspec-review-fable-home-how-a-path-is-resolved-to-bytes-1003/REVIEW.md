# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-how-a-path-is-resolved-to-bytes-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-HOW-A-PATH-IS-RESOLVED-TO-BYTES-1` · Package: `_index/candidates/fable-home-how-a-path-is-resolved-to-bytes-1003/` (committed in `60f3e63b3`, reviewed at HEAD `33eb7192f`; the package is unmodified in the working tree) · Page: `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/how-a-path-is-resolved-to-bytes.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The one row is exact against the bytes, including the fall-through value on the last path. The site is a direct tail jump to the body. The host is the right one: the page's own slot table names the caller as the class's slot 6.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The row is on the page at line 570, identical to `rows.json`.
- **`0059FD10` (0x89 B), read in full against `disr.py`:**
  - `ebx` = `edx`, the return value when the call succeeded. Each path then does `xor eax, eax / cmp r8d, -1 / cmovne eax, ebx`, so the result is 0 when the call's 32-bit return is -1 and `edx` otherwise.
  - **Path 1:** when `[rcx+0x10]` is non-null, `call 00215220` at +0x1A (`0059FD2A`) with that qword, `rdx` and `r8d` = 1.
  - **Path 2:** when `[rcx+8]` is not -1 (a full 64-bit `cmp rax, -1` at `0059FD49`), `call [008C2150]` at +0x4B (`0059FD5B`), an import thunk, with that qword, `rdx`, `r8d` = 0 and `r9d` = 1.
  - **Path 3:** `test rcx, rcx / jle` at `0059FD7A` is a signed test. When `[rcx+0x20]` > 0, `call 001D6CE0` at +0x72 (`0059FD82`) with that qword, `rdx` and 1.
  - **Path 3 when the guard fails:** `r8d` still holds the -1 set by `or r8d, 0xFFFFFFFF` at `0059FD45`, so `cmovne` does not move and `eax` = 0. "When it is 0 or less it returns 0 without a call" is exact.
  - All 5 anchors (`call`, `cmp`, `call`, `jle`, `cmovne`) sit on these instructions.
- **entered_from.** `0059FDA0` + 0x4 = `0059FDA4`, `jmp 0059FD10`, after `add rcx, 0x20`.
- **Host fit.**
  - The page cites `0059FDA0` in §2 "What the seven slots do", as slot 6 of the stream class ("**Seek** on the buffer backing"). That is a body statement in the page's main scope, not a neighbour or boundary line.
  - Since the caller adds 0x20, the body's `+0x10` / `+0x8` / `+0x20` are the stream's `+0x30` buffer, `+0x28` handle and `+0x40` backing. §2 describes exactly these three backings for slot 5 (Read), so the body belongs with this page.
- **Duplicate citation (non-blocking).**
  - OPUS's later commit `399ce7caf` (02:40, after this package's `60f3e63b3` at 02:24) also states `0059FD10` and `0059FDA0` on `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (lines 772-773, PSerialization member list).
  - The two statements agree: OPUS names the import as `SetFilePointer`.
  - The body was a frontier body when FABLE homed it, so this is a collision between two correct rows, not a defect of this package. This page is the better semantic host. No change is required. The member-list row can stay as the family statement.
- **Notes (non-blocking).**
  - The page's slot-6 label "**Seek** on the buffer backing" (§2, line 69, not part of this package) is narrower than the body: it seeks through whichever of the three backings is present, in the order buffer, handle, `+0x40`.
  - Suggest that the page owner change it to "**Seek** through the first available backing (buffer, handle, `+0x40`), relative to the current position".
  - The row could add "(the stream's `+0x30` / `+0x28` / `+0x40`; `0059FDA0` adds 0x20)", so readers can map its offsets onto §2.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
