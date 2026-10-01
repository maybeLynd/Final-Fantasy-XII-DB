# REVIEW — OPUS-REQ-AUDITSEM-REVIEW-CON-167-MOVEMENT-PASSES · SWE2-AUDIT-SEM 2026-09-29

Passes: `82abaac96` (CON-167), `342564b94` (three movement passes).
Regressions re-run non-author: falsify_heading_delta / falsify_turn_limiter /
falsify_separation / falsify_nav_search — FAILS 0 each. Image `73461D08…21F8`.

## Separation attacks — both fail

**Mode-0 writes no body state.** The mode arg arrives in `r8d` → `esi`
(`00314F6F`). Every body-write arm is gated: `00315255`/`0031527B`/
`00315292` each `test esi,esi; je 00315377`. The mode-0 target `00315377`
writes only `movss [r15],xmm4` — the caller's output buffer — then exits at
`0031537C`/`0031515E`. The push writes (`+0xE8`, `+0xEC`, `+0xED`, `+0xEE`,
`+0x100`, `+0x108` at `0031525D`–`00315369`) sit past the mode gates only.

**Vertical test is a refusal.** `003150CA comiss xmm1,xmm0` /
`003150CD ja 0031515C` and `003150D3`/`003150DB ja 0031515C` — both jumps land
on `0031515C xor eax,eax` + epilogue = the no-contact exit, not an alternate
contact rule. (+0xE4 = vertical offset, +0xE0 = span — matches the claim.)

## CON-167 delta writes — byte-verified

`002E43E6 movss dword[rdi+0xF8],xmm0` (post-`003A1D30`) and
`002E445C movss dword[rdi+0xF8],xmm3` (behind `jbe` skip) — the delta body
does write the movement block's `+0xF8` at both sites.

## Verdict

**ACCEPT** — the CON-167 correction and all three movement passes survive
independent attack.
