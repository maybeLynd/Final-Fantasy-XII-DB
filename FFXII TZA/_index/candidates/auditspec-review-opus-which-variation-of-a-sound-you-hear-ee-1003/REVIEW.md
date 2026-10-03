# SWE2-AUDIT-SPEC review: OPUS interior rows (opus-which-variation-of-a-sound-you-hear-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-WHICH-VARIATION-OF-A-SOUND-YOU-HEAR-EE-1003` · Package: `_index/candidates/opus-which-variation-of-a-sound-you-hear-ee-1003/` (request at `693d650d4`, reviewed at HEAD `8fabf1300`) · Page: `18-Audio/which-variation-of-a-sound-you-hear.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

All 4 rows were checked clause by clause against the bytes; the package has fewer than 15 rows. 4 of 4 are exact.

## SWE2-AUDIT-SPEC checks

- **Applier re-run (verify only).** `interior_applier.py` without `--apply` writes nothing. Run under the analysis venv with `-B`: `VERIFY 4 functions, 20 anchors` / `ALREADY` / `FAILS 0`, identical to the committed `.out`.
- **Live page.** Each function has exactly one interior-table row. Its text equals `rows.json` byte for byte, and all of its anchors appear in the row.
- **Anchors.** All 20 are instruction boundaries with the recorded mnemonic. Each lies on its clause.

| fn | verdict | decisive bytes |
|---|---|---|
| `007BFBA0` | exact | The flag is set by a one-iteration byte scan of `[rcx+0x3f8]` (`007BFBB6`..`007BFBC6`): `bpl`=1 when non-zero (`007BFBCD`), else 0 (`007BFBC8`). Signed count `cmp [rcx+0x4c],0`/`jle` (`007BFBD0`) and re-tested `jl` (`007BFC0A`). Qwords from `rcx+0x400`, stride 8 (`007BFBDA`, `007BFC06`). Stack copy plus `007B5070(&slot)` (`007BFBE1`..`007BFBEE`). Non-null → `007E73C0(rax, edx = movzx bpl)` (`007BFBF8`..`007BFBFF`). |
| `007BFC30` | exact | `ucomiss [+0x2bc]`, 0 (`007BFC45`): equal → `[+0x2b4]` (`007BFC52`); else `007A9E50([+0x2b8]/[+0x2bc], edx=[+0x2c4])` (`007BFC5C`..`007BFC6E`) ×(`[+0x2b4]`−`[+0x2b0]`)+`[+0x2b0]` (`007BFC73`..`007BFC8A`). Same loop shape (`007BFC94`..`007BFCDB`). `007E73D0(rax, xmm1=value)` (`007BFCC7`..`007BFCCD`). |
| `007BFD00` | exact | vcall `[rax+0xe0]` with `rdx`=`rsp+0x30`, `r8`=`rsp+0x2c`, `r9`=`rsp+0x28` (`007BFD1C`..`007BFD2E`). Loop `007BFD36`..`007BFD8A`. `xmm1`=`[rsp+0x30]`, `xmm2`=`[rsp+0x2c]`, `xmm3`=`[rsp+0x28]` (`007BFD67`..`007BFD76`), then `007E73F0` (`007BFD7C`), so the out-slot order matches. Cookie `00808C40` (`007BFD99`). |
| `007BFEB0` | exact | `movsxd r15,edx` (`007BFEBB`). Record = `rcx`+idx·0x30+0x250 (`lea rbx,[r15+r15*2]`; `add rbx,rbx`; `·8`): `+0xc`→`0x25c` (`007BFF11`/`007BFF1A`), `+0x4`→`0x254`, `+0x8`→`0x258`, `+0x14`→`0x264`, `+0`→`0x250` (`007BFF1F`..`007BFF60`). The value is computed inside the loop, only after a non-null lookup (`007BFF05`/`007BFF08`). `007E7430(rax, edx=r15d, xmm2)` (`007BFF64`..`007BFF6A`). |

## SWE2-AUDIT-SPEC narrowing / notes

None blocking. As on the sibling packages, "equals 0.0" (`ucomiss`/`jne`) also sends a NaN down the "equals" arm, and no correction is asked for.
