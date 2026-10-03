# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-lazy-statics-and-the-one-time-init-lock-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-LAZY-STATICS-AND-THE-ONE-TIME-INI` · Package: `_index/candidates/fable-home-lazy-statics-and-the-one-time-init-lock-1003/` (committed in `5a7a7f97e`, reviewed at HEAD `e0e99b7c6`; the package is unmodified in the working tree) · Page: `24-Compiler-And-CRT-Runtime/Lazy-Static-Initialization/lazy-statics-and-the-one-time-init-lock.md`

## SWE2-AUDIT-SPEC verdict: REJECT

The sentence, site and anchors are exact. **The host is wrong.**

- `001D9F70` is the increment half of a counter pair on the FileCache singleton `[01F82CF0]`. Its decrement twin `001D9F90` is already homed on `17-Presentation-Rendering/Movie-Containers/mh-movie-seek-index.md`.
- This page cites the caller `0017D940` only in a pass-22 cross-subsystem neighbour list ("`0017D940` / `0017D960` are reached from `00212050`", line 796). That list ends with "what each lazily built object is belongs to its owner".
- Nothing about the body is a lazy static or the one-time-init lock, so the section heading ("called from this page's functions") is false for it.

The only row is mis-homed.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 1 functions, 3 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The section heading is at page line 810 and the row (line 816) matches `rows.json` byte for byte.
- **rows.json.** 1 row, 3 anchors. Rejected 0, skipped 0, missing 0.
- **`001D9F70` (0x17 B), read in full.** `cmp edx, 1` / `ja ret` (unsigned) / `movsxd rax, edx` / `lea rcx, [rcx + rax*4]` / `mov eax, 1` / `lock xadd [rcx+0x24], eax` / `ret`. The sentence is exact, and all 3 anchors are on it. On the `ja` path `eax` is whatever the caller left in it, and "returns without a write" does not claim a value.
- **entered_from.** `0017D940` + 0x17 = `0017D957`, a tail `jmp 001D9F70` with `rcx` = `001DADA0()` (an 8-byte getter of `[01F82CF0]`) and `edx` = the caller's `ecx`. It is the only transfer to the body (raw index).
- **What the body is.**
  - `0017D960` is the same code with a tail to `001D9F90`, which decrements the same dword `+0x24 + edx*4` and stamps `+0x8C` from the QPC timer (`mh-movie-seek-index.md`, line 286).
  - `001DADA0()` is the FileCache singleton (`19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md`, line 769).
  - The pair brackets work, for example `001A07B0` on `game-application.md`: "`0017D940(0)` opens the frame ... `0017D960(0)` closes".
- **Host fit.** The page's subject is the `005CD4F0`/`005CD820` flag lock and the one-time-init guard. `0017D940` appears there only as a neighbour reached from `00212050`, and no line on the page reads the FileCache counter. Apart from `_index/ADDRESS-INDEX.md`, no other page cites `001D9F70`.
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC repair

1. Remove the row from this package and from the section already on the page (the applier prints `ALREADY`). With no rows left, remove the section heading, its intro and the table header too.
2. Re-home the row **unchanged** on `00-Engine-Core-Runtime/Application-Root/game-application.md`. That page cites the caller `0017D940` in its own body text: the `001A07B0` paragraph, "`0017D940(0)` opens the frame", line 1747. Optionally, add "(the increment twin of `001D9F90`, which decrements the same dword; both on the FileCache singleton `001DADA0()`)" to the sentence.
