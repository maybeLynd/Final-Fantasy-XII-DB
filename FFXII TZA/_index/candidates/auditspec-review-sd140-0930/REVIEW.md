# Audit-spec review: SD-140 — vertex-prep kernel (+0x28 per-corner RGBA8, +0x2C ST pairs)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `sd140-vertex-prep-kernel-0930` (SWE2-ORACLE)
Board task: `ORACLE-REQ-AUDITSPEC-SD140-0930`

## Verdict: ACCEPT

## What was checked

- **Checker re-run.** `python sd140_kernel.py` at HEAD: `CHECKS 23`, `FAILS 0`, matching the
  retained `sd140_kernel.out`. Same Unicorn-on-certified-image methodology as SD-120: shipped
  bodies execute against controlled memory; a Python model is checked against native results.
- **Productive corrections survive.** The run tail reproduces X3 (`0043D8F0`/`0043E440`/`0043DB90`
  + `0043DF80` are n-gon primitive builders for `00438860`'s clipped polygons) and X4 (the +0x40
  colour is `param[+0x40] = 0026EE00(instance+0x240, …)` with `param = [01FD4A78] + 0x800` — stated
  as "a precision, not a code conflict").
- **Claim shape.** The RESULT line bounds itself precisely: +0x28 entries are per-corner RGBA8
  vertex colours modulated by `min(255, e*c >> 7)` after `00433830`'s rounded blend lerp, then
  re-modulated per pass by the pass colour; +0x2C pairs are per-corner texture coordinates handled
  as GS STQ with `S = (u+ou)*Q` and `U = S/Q` in textured builders. This is a mechanism-level
  answer, not a label — the level SD-140's row needed.
- **Native spot check.** `00432300` disassembled from the certified image: the body is the
  SSE-dense modulation path the record describes (byte extracts via `psrldq` lane peels feeding
  byte stores to the draw parameter block) — consistent with the claimed structure; per-trial
  numeric equality is carried by the Unicorn M-checks rather than eyeballing.

## Narrowing / notes

None required.
