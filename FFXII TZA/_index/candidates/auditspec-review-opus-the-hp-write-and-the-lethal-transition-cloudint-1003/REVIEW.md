# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-the-hp-write-and-the-lethal-transition-cloudint-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-HP-WRITE-AND-THE-LETHAL-TRANSITIO-F0145` · reviewed at HEAD `33eb7192f` · Package: `_index/candidates/opus-the-hp-write-and-the-lethal-transition-cloudint-1003/` · Page: `08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh in verify mode (no `--apply`, writes nothing) -> exit 0, `VERIFY 6 functions, 30 anchors` / `ALREADY` / `FAILS 0`. The page block equals `rows.json`.
- `rows.json`: 6 rows, 30 anchors, `mode: interior`; rejected 0, skipped 0, missing 0. There are no homing rows, so the entered_from and host checks do not apply.
- Semantic pass: **all 6 rows** were read clause by clause against the resolved disassembly of the certified image (SHA256 73461D08..., rip targets resolved by `disr.py`). The request asks for at least 15; the package has 6, so all were read. Stack slots, branch and cmov polarity, signedness and argument registers were checked:
  - `00340CB0` / `003421D0`: `o` = `00263F10(rdx)`; the first pop goes to `ebx` (`a`), the second to `eax` (`b`); the tail call is `00473980(rcx = o, edx = b, r8d = a)`. `003421D0` first calls `00267F90(r9, 2)`. Exact.
  - `00343D10`: `003A1920(rcx = 00265060(00264010(a)), rdx = 00265060(00264010(b)))`; the `b` chain's `00265060` runs first, which the sentence does not order and need not. Then a tail jump to `0026B4C0(incoming rcx, xmm1 = result)`. Exact.
  - `00344F80`: the three `00267DB0` results go to `[rsp+0x28]`, `[rsp+0x24]` and `[rsp+0x20]`, i.e. vector `+8`, `+4`, `+0`. `00267DB0` was read and does return its float in `xmm0`. `0026B4C0` is a plain call here, and the cookie is present. Exact.
  - `0034A110`: `a`/`b`/`c` = `edi`/`ebx`/`eax`; the tail call is `004738D0(00263F10(00264010(c)), b, a)`. Exact.
  - `00473980`: `and r9d, 1; shl 0x1c` gives 0x10000000. `bts 0x1d` is kept unless `and al, 2` is zero (`cmove`), and `bts 0x1e` likewise for `edi = r8d & 4`. A null `rcx` gives -1. The tail call is `00329B70(003589B0(rcx), 0, esi = edx, mask)`. Exact.
- Limits hold: body statements only, static evidence. An OPUS self-draft plus OPUS's mechanical check is not independent review; this record is.
