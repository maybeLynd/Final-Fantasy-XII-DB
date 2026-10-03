# SWE2-AUDIT-SPEC review: OPUS interior rows (opus-contract-ppfx-effect-creation-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-CONTRACT-PPFX-EFFECT-CREATION-EE-1003` · Package: `_index/candidates/opus-contract-ppfx-effect-creation-ee-1003/` (request at `693d650d4`, reviewed at HEAD `8fabf1300`) · Page: `17-Presentation-Rendering/Post-Processing/CONTRACT-ppfx-effect-creation.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 3 rows. The request asks for at least 15 rows, so all 3 were checked. Each was checked clause by clause against an independent decode (`disr.py`) and raw `.rdata` string reads (`disw.py`). Every clause holds, and every anchor is an instruction boundary inside its body with the recorded mnemonic. No row changes.

## SWE2-AUDIT-SPEC checks

- **Applier re-run (verify-only).** I read the source first: without `--apply` it writes nothing. `interior_applier.py -B` printed `VERIFY 3 functions, 15 anchors` / `ALREADY` / `FAILS 0`, exit 0. The page is clean in the working tree and holds the 2026-10-03 block at `HEAD`, so the page text equals `rows.json`.
- **Extents.** All three listings end in `ret`, with every branch target inside and no jump table.

| fn | verdict | decisive bytes |
|---|---|---|
| `00719380` | exact | `007193AE`-`007193BA`: when `[rcx]==0`, `00715A00(rdx, r8)`. `007193C2`-`007193CF`: when `[r8]==0`, `00715A00(rdx, rcx)`. `007193D7`-`007193E8`: `r8d=[r8]+[rcx]`, `r9d=-1`, `rdx=[rcx+8]` into `007158B0(rsp+0x30, ...)`. `007193EE`-`00719400`: `memcpy([rsp+0x38]+sext [rcx], [r8+8], sext [r8])`. `0071940D` is `00715A00(rdx, rsp+0x30)`. `0071941A`-`00719436`: the saved `[rsp+0x38]` is compared with `02EA1720` and with null, then `006DA8A0([01F3BA68], p-8)`. `0071943C` `mov rax,rbx` is on every path. |
| `0071B3C0` | exact | Unsigned split at `0071B3C8` (`cmp 0x80004005; ja/je`). The string reads are `00D9B0A0` "S_OK", `0B0A8` "S_FALSE", `0B0D0` "E_NOTIMPL", `0B0B8` "E_ABORT", `0B0B0` "E_FAIL", `0B0C0` "E_UNEXPECTED", `0B0E0` "E_OUTOFMEMORY" and `0B0F0` "E_INVALIDARG", each on its stated code. Fallback: `0071B451` calls `0071B1B0(ecx)` with ecx unchanged. `0071B45B`-`0071B45F` call `0071B1B0(-ecx)` (`neg ebx`). `0071B469` returns `00D9B100` "Unknown Error Code". A non-null result returns through `0071B48A`. |
| `0072EB20` | exact | `0072EB5A` is `007157A0(rsp+0x20, r8)`. `0072EB60`-`0072EB6B` is `00715CC0(rsp+0x20, [rsp+0x20]-1)`. `0072EB76`/`0072EB78` `test ebp,ebp; jle` skip the loop for a non-positive count. `0072EB80`-`0072EB96`: `sprintf(rsp+0x40, 00D9F5A4 "%s%d", [rsp+0x28], i)` with `i` pre-incremented from 0, so 1..n. `0072EBA6` `call [vtbl+0x60]`(obj, rsp+0x40). `0072EBA9` stores the dword to `[rbx]`. `0072EBB7` `call [vtbl+0xc8]`(obj, result) runs when the result is non-zero. `0072EBC0`/`0072EBC2` `jns`, then store 0 on negative. `0072EBC5` advances by 4. `0072EBD2` is `00715C70(rsp+0x20)`. `0072EBE4` is the cookie check `00808C40`. `0072EBD7` returns 0. |

**3 of 3 exact.** All 15 anchors were checked against the decode.

## SWE2-AUDIT-SPEC narrowing / notes

No narrowing.

Notes (non-blocking):
- `00719380`: the free test uses the local pointer read at `007193F4`, before `00715A00` runs. I read `00715A00`, and it copies its source (`00715A3E`-`00715A8B`, with a fresh allocation through `006DA880`). It does not move from it. So "`[rsp+0x38]`" still names the same value at the test, and the row's wording is exact.
