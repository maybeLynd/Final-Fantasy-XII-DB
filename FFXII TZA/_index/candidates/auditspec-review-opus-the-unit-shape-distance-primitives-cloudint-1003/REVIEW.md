# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-unit-shape-distance-primitives-cloudint-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-UNIT-SHAPE-DISTANCE-PRIMITIVES-CL-1AA01` · reviewed at HEAD `33eb7192f` · Package: `_index/candidates/opus-the-unit-shape-distance-primitives-cloudint-1003/` · Page: `06-Movement-And-Navigation/the-unit-shape-distance-primitives.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh in verify mode (no `--apply`, writes nothing) -> exit 0, `VERIFY 4 functions, 20 anchors` / `ALREADY` / `FAILS 0`. The page block equals `rows.json`.
- `rows.json`: 4 rows, 20 anchors, `mode: interior`; rejected 0, skipped 0, missing 0. There are no homing rows, so the entered_from and host checks do not apply.
- Semantic pass: **all 4 rows** were read clause by clause against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). The request asks for at least 15; the package has 4, so all were read. Stack slots, branch and cmov polarity, signedness and argument registers were checked:
  - `0022CF50`: `f` = `[rcx+0x10]` + `movsx dx` << 5. The current vertex is word `[rdi]` (stepping from `f+0x10`), the next is word `f+0x10 + 2*table[k]`, and the table runs `00908DE8`..`00908DF4` (`.rdata`, 3 dwords). `e` = next - this, with the fourth dword taken from the next vertex; `d` = point - this, with the fourth dword from the point. The call is `00202E10(rsp+0x40, rsp+0x30, rsp+0x20)` = `(&o, &e, &d)`. `comiss xmm6(0), dot; ja` returns 0 when the dot is below 0. The cookie and `00808C40` are present. Exact.
  - `0022E6D0`: `n` = `[r8]`, `p` = `[r8+8]`, `sqrtf(dot(rdx, rdx))`, `(rcx - p).n / rdx.n`, sign flip by `xorps` with `01CEBDA0` (0x80000000), then the product. Exact.
  - `0022EAC0` (read in full): `r9` is set to (0, 0, 0, 1.0); the next corner is (`i`+1) mod 3 via the 0x55555556 reciprocal; `e`/`d` are formed as above. The first negative `dot(N, o)` (`ja`) goes to the `0x400`-at-`f+0x1c` and `esi == 2` early 0. `len` = `sqrtf(e.e)` and `t` = `e.d / len`. `comiss t, 0; jbe` keeps `d`; `comiss len, t; jbe` subtracts `e` whole; otherwise it subtracts `e*t/len`. The face word `f+0x16+i*2` is skipped on `js`. `N` is scaled by `sqrtf(|diff|^2) * 1.0 / sqrtf(N.N)`, float `f+0xc` goes to `+0xc`, and the result is 1. Exact.
  - `0046BF60`: exact.
- Limits hold: body statements only, static evidence. An OPUS self-draft plus OPUS's mechanical check is not independent review; this record is.
