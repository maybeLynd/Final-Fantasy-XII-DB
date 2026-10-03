# SWE2-AUDIT-SPEC review: OPUS engine_explained interior citations (opus-sqex-sd-sound-driver-architecture-ee-1003-2)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-SQEX-SD-SOUND-DRIVER-ARCHITECTURE-EE-2C2B5` · Package: `_index/candidates/opus-sqex-sd-sound-driver-architecture-ee-1003-2/` · Page: `18-Audio/sqex-sd-sound-driver-architecture.md` (commit a19ddeadd)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 3 rows and their 15 anchors are correct against the bytes; no row text changes. The narrowing is to the package README only: it records a spot-check on a function that is not on this page, and one correction bullet is cut off mid-word.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh from the package folder without `--apply` -> `VERIFY 3 functions, 15 anchors`, `ALREADY`, `FAILS 0` (exit 0), the same as the committed `.out`. `git status` on the page and the package was clean afterwards (reviewed at HEAD `f49bb4021`).
- `rows.json`: 3 rows, 15 anchors; rejected 0, skipped 3 (`007B9050`, `007DCE20`, `007DFBB0`, since rowed by `-1003-3`), missing 5.
- Semantic pass: **every row** (3 of 3; fewer than 15 exist) read clause by clause against a full capstone listing of the certified image (SHA256 73461D08...), with rip targets resolved to their sections and IAT names read from the import table:
  - `007AAC80` exact. Record at `01F40410` (`.data`, mutable): `dur` `+0xC` tested by `ucomiss xmm1, 0` / `jne` (`007AAC9F`), so equal or unordered takes `v` = `tgt` `+4`. Otherwise `007A9E50(t/dur, edx = curve dword +0x14)` (`007AACC0`), `* (tgt - cur) + cur`. Stores: `cur` (`007AACE6`), `xmm0` to `tgt`, `xmm1` to `dur`, dword 0 to `+8` and `+0x14`, byte 1 to `+0x18`. Mode `cmp dword +0x1C, 1` / `jne` (flags survive the `mov` stores). `comiss xmm6, v` / `jbe` sends "not above" and unordered to the `+0x24` arm. Rate absolute value by `andps` with `.rdata` mask `00D27AA0` (7FFFFFFF x4). `divss` at `007AAD3A`. `comiss xmm7, d` / `jae` skips the store, so unordered stores (`007AAD76`). `eax` is zeroed at `007AACE4` before every exit, so it returns 0.
  - `007AAD90` exact. The same body over the record at `01F403E0`. Every offset maps: `+0xC` `01F403EC`, `+0x14` `01F403F4`, `+0x18` `01F403F8`, `+0x1C` `01F403FC`, `+0x20` `01F40400`, `+0x24` `01F40404`. Anchors `007AADAF` ucomiss, `007AADD0` call, `007AADF6`/`007AAE86` movss, `007AAE4A` divss.
  - `007E0A40` exact. `test dword [rcx+0x80], 0xFFFFFFFB` / `je` returns -1 (`007E0A4E`, `007E0B4D or eax,-1`). `n` = dword `+0xB0`, `cmp 2` / `jge` (signed). The product is `cmove` 2/4 on `[+0x90]==1`, then `imul` with dword `+0xAC`, then `movsxd`. `div rcx` is unsigned 64-bit on `r8` (`007E0A9E`); `rdx != 0` returns -1. The fifth argument is dword `[rsp+0x60]` = entry `rsp+0x28`. When `n` is 0, `cvtdq2pd` stores a double to `+0x98` (`007E0AC5`). `EnterCriticalSection`/`LeaveCriticalSection` go through IAT `008C20B8`/`008C20C0` on `rcx+0x58`. `k` = (`+0xB4` + re-read `+0xB0`) through `and 0x80000001` with the negative fix-up (signed remainder). The slot is `((k+6)<<5)` = `0xC0+0x20k`, holding `rdx` at `+0` (`007E0B00`), `r8` at `+8`, the dword fifth argument at `+0x10` and `r9` at `+0x18`. `inc dword +0xB0` (`007E0B26`) happens before the leave, and the function returns 0.
  - The README's three corrections did reach the row text: unordered-stores on the final `comiss` (both float rows), and the unsigned `div` with its fault on a zero product (`007E0A40`).
- Anchors: all 15 are strictly inside their bodies, decode to the recorded mnemonic, and sit on the clause they support (the test, compare, call, store or divide named).
- Family-declaring-page rule (progress.py `cite_credits` / `family_rule_inputs`): the SQEX page declares no accepted family. All 3 functions are members of `SQEX SEAD sound library span`, which is declared elsewhere, so on this page the base rule applies: a strictly interior anchor credits `engine_explained`, and none of the bodies is under 128 B. "All 3 rowed functions now measure A" is consistent with the rule in force.
- Limits hold: body statements only, static evidence, no runtime claim. The drafter and the second local agent are not independent review; this record is.

## SWE2-AUDIT-SPEC narrowings

README only (`_index/candidates/opus-sqex-sd-sound-driver-architecture-ee-1003-2/README.md`); `rows.json` row text is unchanged.

1. Paragraph 1, the provenance sentence cites a spot-check on `00713210`. That function belongs to the MSVC ordered-container package and is not on this page; it is template text carried over.
   - Old: "OPUS confirmed a correction at the bytes on a sample (`00713210`: the qword stored is the one at the pointer `00712F60` returns) before applying."
   - New: "OPUS spot-checked the corrections at the bytes before applying (the bullets below name what each re-read found)."
2. The `007E0A40` correction bullet (and the same `why` string in `rows.json` `corrections`) is cut off at "inc inside the loc".
   - Old ending: "with rdx/r8/fifth dword/r9 at +0/+8/+0x10/+0x18, inc inside the loc"
   - New ending: "with rdx/r8/fifth dword/r9 at +0/+8/+0x10/+0x18, inc of dword +0xB0 inside the lock (before LeaveCriticalSection at 007E0B2C)."

Non-blocking: paragraph 1 says "The page named 6 F-frontier functions only at their entry", while the record lists 3 rowed, 3 skipped and 5 missing (`007B8C80`, `007DFE30`, `007E0550`, `007E0650`, `007E0980`). The 6 is the pack size, not the page's count.
