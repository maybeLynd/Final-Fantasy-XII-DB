# SWE2-AUDIT-SPEC review: FABLE `0015B820` correction

Reviewer: SWE2-AUDIT-SPEC (Devin session) · 2026-10-03 ·
Task: `FABLE-REQ-AUDITSPEC-CORR-0015B820-1003` · Package:
`_index/candidates/fable-corr-0015b820-1003/` · Affected page:
`24-Compiler-And-CRT-Runtime/Runtime-Service-Surface/what-the-game-asks-windows-for.md` ·
Repair commit `6f0b95508`, image pin `73461d08…21f8`.

## SWE2-AUDIT-SPEC verdict: ACCEPT

The repair is byte-exact and the page edit lands it correctly. The original REJECT is upheld and resolved.

## SWE2-AUDIT-SPEC re-derivation from the shipping image

`0015B820`+0xC9 .. +0xE6 re-decoded on the certified image:

- `+0xBB` `lea rdx, [rip+0x1B6B316]` resolves to `01CC6BF8` (the `".dll"` string).
- `+0xC9` `call 00861F20` (the suffix compare) — target confirmed.
- `+0xCE` `test eax, eax` / `+0xD0` `je 0015B90E` — the branch is taken when the compare returns **0**
  (suffix IS `".dll"`), skipping the try.
- The try itself is gated by `call [rip+0x7667B0]` = `008C20A8` with `test eax,eax` / `jne` skip — the
  row's "each try only when a fresh `008C20A8()` is 0" is also correct.
- `+0xDC` `lea rdx, [rip+0x1B6B2E5]` → `01CC6BE8`; `mov rcx, rsi`; `+0xE6` `call 0015A9B0` — the try is
  `0015A9B0(rsi, 01CC6BE8)` exactly as the row states.

So the first try runs when the compare is **non-zero** — the corrected wording. My original reading (and the
REJECT) is confirmed right.

## SWE2-AUDIT-SPEC page check

The row on the page at HEAD carries `is non-zero` with `~~0~~` struck through and the correction note
attributing the change to this REJECT (`6f0b95508`, working tree clean for the page). The other eight rows
were previously accepted and are untouched by the correction.

## SWE2-AUDIT-SPEC limits

Static byte verification of the named range plus the page-diff check only. No runtime, no caller census;
the remainder of the `0015B820` row was not re-audited beyond the corrected clause.
