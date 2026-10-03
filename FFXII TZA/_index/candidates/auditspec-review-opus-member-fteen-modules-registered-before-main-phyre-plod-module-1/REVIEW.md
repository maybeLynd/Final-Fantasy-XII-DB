# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PLOD module (opus-member-fteen-modules-registered-before-main-phyre-plod-module-1)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-FTEEN-MODULES-REGISTERED-BEFORE-MAIN` · Package: `_index/candidates/opus-member-fteen-modules-registered-before-main-phyre-plod-module-1/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 399ce7caf)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 28 functions, 139 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 28 rows, mode `member`, family `Phyre PLOD module`; rejected 0, skipped 0, missing 0; one correction (`006C7B90`).
- Correction checked at the bytes: `006C7B90` 006C7C26 `mov rax,[rax+0x38]` then 006C7C2F `mov [rax+0x28],r11` - the zeroed qword is `+0x28` of the object at qword `[q+0x38]`, as the corrected row says.
- Semantic pass: **21 of 28 rows** read clause by clause against `disr.py` output of the certified image (field and type names resolved from `.rdata`). All 21 exact:
  - `006C4860` (byte 01F2CDF0 gate, vtable `+8` of 01F2D680 with that object, the two `006388C0` registrations, `006C5FF0`, `006C5A50`, returns 0).
  - `006C4E20` (null destination skipped without advancing the source: the `je` to 006C4E98 bypasses `add rsi,0x38`; `006C5020(dst+8, src+8)`, dwords `+0x18/+0x1C`, `006C50D0(dst+0x20, src+0x20)`).
  - `006C50D0`, `006C5420` (dword `[rcx]` zeroed first in `006C50D0` only; count above 1 is `cmp 1; jbe` unsigned; re-read of `[rcx]` after the call; free gate not-p / not-inline / bit 31 clear / non-null; store of `p` skipped when it is `rcx+8`).
  - `006C5180` (FLT_MAX / -FLT_MAX triples, `+0x28`=0 then `+0x20`=1, `qword [rcx+0x34]` = 0x447A0000 giving `+0x34`/`+0x38`, 01F323A8 / 01F323F0, `+0x50`, `+0x58`, byte `+0x60`=1).
  - `006C5200`, `006C5320` (masked count above 1, unsigned, for the free in `006C5320`; both fields zeroed on every path).
  - `006C53A0`, `006C59D0` (`0017D260(n*0x38, 8)`; `006C7340(p + r8d*0x38, ecx - r8d)`).
  - `006C5A50`: all ten names confirmed (`m_levels` ... `getLocalToWorldMatrix`); stack args of the `00632A10` call (0x50, 0, 3, 8) and each `00632960` call (n, f, 0, 0 with f = 2 for the two enum types); qword 02E5B2A0 = 00D85EA0; method records 02E5B5B0 / 02E5B610 with `00632FB0(M, 02E5AE00, name, 0)`, `M+0x28`=0, the tail link at `qword [M+0x10] + 0x90` gated by `qword [M+0x18]` non-null and `005A7A40` returning 0; the unguarded `M+0x30/+0x38` = 00D86390/006C7B90 and 00D863C0/006C7780 and `M+0x28` = `M+0x30`; tail `jmp 00639450`.
  - `006C68B0`, `006C6970` (byte 02E5ACF0 set only by `006C68B0`; return 7 via `lea eax,[rbx+7]` with `rbx`=0; slices of `k` dwords / `k` 0xC-byte entries; qword store 0x3F800000 then dword `+8` = 4).
  - `006C7340` (element base `rax-0x28`; qword at `+0x1C` = 0x461C4000 giving `+0x1C`/`+0x20`; qword `+0x28` = 0x3F800000; `+0x30` = 4; `+0x20` = 1 last).
  - `006C73C0`, `006C7780`, `006C79C0`, `006C7B90`, `006C7C60` (free gate old != rdx, bit 31 clear, non-null; stores on both paths).
  - `006C7DC0` (`test r8d,r8d; jns`: the 5 return is a signed test; count `r8d OR 0x80000000` via `bts`, 1 for the inline copy).
  - `006D94E0` (`006B6820(02EA06E0, 'PLODMetricType', 0x18, 8, 00876870, 006D9710)` with the last two at `[rsp+0x20/0x28]`), `006D9600`.
- Advisory, not a defect: in `006C68B0` and `006C6970`, "at most 1" is an unsigned test (`cmp esi,1; jbe`, 006C68D4 / 006C698D), so a `k` with bit 31 set does not take the early return. OPUS may add "(unsigned)" later.
- Rows not sampled (7): `006C5580`, `006C54D0`, `006C5FF0`, `006D9710`, `006D98D0`, `006D99F0`, `006D9B00`. Each repeats a shape that passed above (`006C5420`, `006C5A50`, `006D94E0`/`006D9600`), or the string-list lookup that passed as `006D5AF0` in the PDynamicGeometry record of this batch.
- Limits hold: body statements only, static evidence. The drafting agent, the second local reader and OPUS's re-read are not independent review; this record is.
- Batch-wide sentence, not this record's rows: the README's "262 stood, 10 clauses in 8 functions were corrected" (shared by all 11 records of 399ce7caf) does not match the `rows.json` corrections, which total 12 entries in 10 functions across the 11 records. The narrowing is recorded once, in `auditspec-review-opus-phyre-members-399ce7caf`.
