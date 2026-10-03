# SWE2-AUDIT-SPEC review: FABLE homing rows (fable-home-how-the-engine-chooses-3d-or-flat-movem-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOME-HOW-THE-ENGINE-CHOOSES-3D-OR-FLAT` · Package: `_index/candidates/fable-home-how-the-engine-chooses-3d-or-flat-movem-1003/` (committed in `410ec4476`, reviewed at HEAD `f49bb4021`; the package is unmodified in the working tree) · Page: `06-Movement-And-Navigation/Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md`

## SWE2-AUDIT-SPEC verdict: REJECT

All six sentences, sites and anchors are exact. **Two of the six hosts are wrong:**

- `003DB150`. The page mentions its caller `Movement_TransformAndAccumulateCandidate` (`002E54A0`) only inside the falsification-pass account of an address transposition (line 536). That function is owned by `06-Movement-And-Navigation/heading-speed-to-position-delta.md` ("world-context path, step 2", line 255).
- `001AD670`. Its caller `0017F5B0` appears here only as a callee in the `003B7E20` call list, and then under "Shared callees outside the census" (lines 671, 681). The body is a pass over the map-art context `[01F81168]` that runs `001E6480` on each entry, not movement-mode work.

The other four fit: `00262870`'s three callees and the verb tail `003B7510`.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `homing_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 6 functions, 22 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The section heading is at page line 715 and the six rows (lines 721-726) match `rows.json` byte for byte.
- **rows.json.** 6 rows, 22 anchors. Rejected 0, skipped 0, missing 0.
- **The bodies (all read in full; every clause holds).**
  - `001AD670`: `mov [rcx+0x244], dl`, then `001A9930()` at +0xE with `cmp [rax+0x20], ebx` / `jle` (signed). The loop runs `00189120()` at +0x20 then `cmp byte [rax+0x1C], dil` / `setne`, `001A9930()` at +0x2F, `001A7600(obj, flag, i)` at +0x3C, `001E6480(result)` at +0x49 on non-null, `inc` and a re-fetch at +0x50 / `jl`.
  - `00358420`: `00358450(0, 1)` at +0xB, `00358450(1, 0)` at +0x15, then byte `022C7F99` = 0.
  - `003631A0`: `cl` to `022CBA91`, `edx` to `022CBA84`.
  - `00363B20`: `test ecx, ecx` / `mov eax, 0xB4` / `cmovg eax, ecx` (signed) / store `022CBB30`.
  - `003B7510`: count `02EBCAA0`, signed and re-read each pass. The other calls are `00359B80` at +0x3B, `Actor_GetWorldPosition` at +0x56 (record, +4, +8), `00265240` at +0x6A (+0x10, +0x14, +0x18), `002E9BE0` at +0x72 into byte `+0x64`, `00263CC0` at +0x7D into `+0x34`, `00265200` at +0x8A into `+0x24`, and `00263CC0` at +0x97 into `+0x34` again.
  - `003DB150`: three `addss` into `[r8]`. On non-null `rdx`, it copies the sums to `+0x30`/`+0x34`/`+0x38`, copies the second sum to `+0xAC`, and stores `or eax, -1` as a word to `+0x82`.
- **entered_from.** All six are direct transfers at the stated offsets.
  - `0017F5B0` + 0x23 is a tail `jmp`.
  - `00262870` + 0xE, + 0x17 and + 0x1C are calls. `003631A0` and `00363B20` are also reached from `00341460`, `003417C0` and `00341D00`.
  - `003B6F30` + 0x23 is a tail `jmp`, and `003B7080` + 0x28 is a second one.
  - `002E54A0` + 0xD7 is the only caller of `003DB150`.
- **Host fit.**
  - `00262870` has its own row on this page (line 689), which names the 17-byte, 13-byte and 38-byte setters these rows describe. They fit.
  - `003B6F30` is cited in the flag-B writer table (line 461, verb `0x202` `disposepartywithoutcontrol`). `003B7510` is that verb's tail over the party table `02EBCA80` (line 399). It fits.
  - `003DB150` is the defect. It is the position accumulate (`+0x30..+0x38`) of the candidate path, which `heading-speed-to-position-delta.md` reads step by step (lines 241, 255, 406, 515).
  - `001AD670` is the defect. `0017F5B0` is not this page's function, and nothing here reads `+0x244`, `[01F81168]` or `001E6480`. `[01F81168]` is the map-art context (`00-Engine-Core-Runtime/Application-Root/game-application.md` line 496; `02-Resource-And-Asset-Pipeline/Prefetch-And-Json-Data/ta-texture-animation-lists.md` line 157).
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.

## SWE2-AUDIT-SPEC repair

1. Remove the `003DB150` and `001AD670` rows from this package and from the section already on the page (the applier prints `ALREADY`).
2. Re-home `003DB150` **unchanged** on `06-Movement-And-Navigation/heading-speed-to-position-delta.md`, which cites `002E54A0` in its own text.
3. Hold `001AD670`. No page reads its caller `0017F5B0` as a body; the only citations are callee mentions here and in `battle-runtime-mode-ladder.md` line 409. Home the two together. The natural host is `02-Resource-And-Asset-Pipeline/Prefetch-And-Json-Data/ta-texture-animation-lists.md`, which reads the `001A9930()` map-art context the loop walks. `001AD670`'s sentence can be used unchanged once `0017F5B0` is cited there.
4. The other four rows are exact and stay.
