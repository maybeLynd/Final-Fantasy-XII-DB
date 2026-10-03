# SWE2-AUDIT-SPEC review: OPUS interior rows (opus-the-music-control-file-and-the-bgm-strea-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-MUSIC-CONTROL-FILE-AND-THE-BGM-STREA-EE` · Package: `_index/candidates/opus-the-music-control-file-and-the-bgm-strea-ee-1003/` (request at `693d650d4`, reviewed at HEAD `8fabf1300`) · Page: `18-Audio/the-music-control-file-and-the-bgm-stream.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

All 3 rows were checked clause by clause against the bytes; the package has fewer than 15 rows. 3 of 3 are exact.

## SWE2-AUDIT-SPEC checks

- **Applier re-run (verify only).** `interior_applier.py` without `--apply` writes nothing. Run under the analysis venv with `-B`: `VERIFY 3 functions, 15 anchors` / `ALREADY` / `FAILS 0`, identical to the committed `.out`.
- **Live page.** Each function has exactly one interior-table row. Its text equals `rows.json` byte for byte, and all of its anchors appear in the row.
- **Anchors.** All 15 are instruction boundaries with the recorded mnemonic. Each lies on its clause.

| fn | verdict | decisive bytes |
|---|---|---|
| `003BA5F0` | exact | Dword `02B40E14` (`003BA5F4`). State 0 → 1 there, 0 to `02B40EC0` (`003BA660`..`003BA66C`). State 1 → `00862130(movzx byte [02B40E20], lea 02B40E3E)`, then 0xc (`003BA63E`..`003BA651`). State 12 (`sub 1`; `cmp 0xb`) → `lea eax,[rcx+4]`; `test eax,0xfffffffb` (`003BA608`/`003BA60B`), which is zero only for `ecx` ∈ {0, −4}. Then: zero qword `02B40E14` and dword `02B40E10` (`003BA62C`/`003BA633`); else 9 to dword `02B40E18`, then zero qword `02B40E10` (`003BA614`/`003BA61E`). That qword spans `E10`..`E17`, so it does not overwrite the 9. Other states `jne` → return (`003BA606`). |
| `007A7A20` | exact | `[rcx]`==0 → 0x82000000 (`007A7A4A`..`007A7A4F`). `al`==2 or (`al`−8) ≤ 1 unsigned (`007A7A59`..`007A7A63`) → `007AB460(rsp+0x20)` with a `js` pass-through (`007A7AAE`/`007A7AB5`), then 0xd / `[rcx]` / `xmm1` / `r8d` at `p`, `p+8`, `p+0x10` and `p+0x14` (`007A7ABC`..`007A7ADD`), and `007AB550(p)` returned (`007A7AE5`). `al`==7 → `007BAD60(rsp+0x20)` with `js` (`007A7A6E`/`007A7A75`), 0x10 / `[rcx]` / `xmm1` (`007A7A7C`..`007A7A93`), `007BAE50(p)` (`007A7A9D`). Other → −1 (`007A7AA4`). Cookie `00808C40`. |
| `007A88F0` | exact | `movzx ebp,dl` (`007A88FF`) leaves `rcx`/`rdx` intact for `007B24F0` (`007A8905`). `h`→import `008C20B8` (`007A8910`). Stack copy of `[rcx]` → `007B2470` (`007A8916`..`007A8923`). Null → `008C20C0(h)`, 0 (`007A892D`..`007A8936`). Else `007D0A10(rax)` (`007A8950`), `008C20C0(h)` (`007A895A`), and with `bpl` ≠ 0 returns `ebx` = the `007D0A10` result (`007A8960`..`007A8967`). Else loop: `008C20B8`/`007B2470`/`008C20C0` (`007A8969`..`007A898A`), and while non-null `008C21B0(1)` (`007A8995`/`007A899A`) and repeat (`007A89A0`..`007A89CA`), returning 0 (`007A89CC`). |

## SWE2-AUDIT-SPEC narrowing / notes

- Non-blocking (`007A7A20`): "the returned record `p`" means the pointer the callee stores to its out argument `rsp+0x20`, which the body reloads at `007A7A77`/`007A7AB7`. `eax` from the callee is the status that the `js` tests, not `p`. The sentence's own "calls `007AB460(rsp+0x20)` and, if that is not negative" already gives this reading. An optional clarification is "of the record `p` that call leaves at `rsp+0x20`".
- README "Missing: 2" (`007A7010`, `007A87C0`) is outside this spot-check.
