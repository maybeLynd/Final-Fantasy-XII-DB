# EXP-214 — measure wrappers `2B41F0`/`2B43C0` promoted real

**Status:** complete — **521/521 cases, stable across 3 independent runs,
byte-identical `result.json` (SHA256
`76e775e14bc615ce5ea1efda2e5025d76a81a6c4028388e96a39fe785cca0478`), zero unexpected faults.**
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes executed
under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py` (extends
EXP-192..213; 521 inherited cases, 5 re-fixed for the promotion)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Scope

EXP-213 left the two measure wrappers scripted. Both turned out to be
shallow state-prep bodies that tail into the already-real `2AF340`
evaluator — promoting them moves every measure call inside the
`8`/`>`/`*` deep tails to real shipped execution, including a real
glyph decode pass over the measured strings.

## Bodies promoted real this round

| body | semantics |
|------|-----------|
| `002B41F0` | default-state measurer `(str, flag)` — `861EC0` memsets a `0xD0` template (`rbp+0x40`), writes defaults (`b70=0x80808080`, `w0DC=0x1E`, `f74=1.0`, `bE0=1`, `bDA=0x25`, `bE8=0xFF`, `bDE=8`, `f78`/`f7C=1.0`, `qF8=0x30000`, `d100=0`, `bEE=0xFF`), `bts d84,9` → `39C4A0((d84>>0xB)&1)` → `q[rbp+0xA0]` (lands at `copy+0x60` — the flag-desc slot), NUL-scans `str` → `w[rbp+0xCC]`, copies template → `rsp+0x70`, swaps `q[ctxo+0x10C8]` to `orig_rsp+0x18`, calls **real `2AF340`**(copy, str, &out, 0), restores the cell, `808C40` cookie check, ret `eax` = evaluator count |
| `002B43C0` | caller-state measurer `(state, str, r8b)` — copies `0xD0` from `rcx` → `rsp+0x60` (+`rsp+0x130` second copy), stores `r8b` at `orig_rsp+0x18`, installs that cell into `q[ctxo+0x10C8]`, NUL-scan → `w[rsp+0xEC]`, **real `2AF340`**, restore, cookie, ret (`xmm0` = evaluator leftover width) |

`2B41F0`'s `39C4A0` result supplies `q[copy+0x60]` — the flag-desc
pointer `2B2150` reads at `0x2B22F1`; fixture `s39c4a0_ret="c60"`
makes the promoted walk's heavy-char path resolve exactly like the
state-copied one.

## Call sites now real

- `0x2AD550` / `0x2AD57F` — the `*` icon arm's two suppress-measures
  (`rest[w48]` NUL → `2B43C0(rest)`, restore; `rest[w48+w44]` NUL →
  `2B43C0(rest+w48)`, restore). Both previously returned a planted
  `xmm0`; now they run the full evaluator on the icon blob.
- `0x2ADA3F`, `0x2ADE66`, `0x2ADF5F` — the `*` icon-variant table
  measure (`d[rbx]`-counted `q[rbx+rdx*8+8]` strings) and the `8`/`>`
  resolved-resource measures via `2B41F0`. `2B2970` (pre-publish copy
  helper) was already executing real — unmapped, bounded.

## Corrections of record

- **Stack floor:** real `2B43C0` needs a `0x200` frame; the `*` arm's
  call chain (`2AC5F0` → arm → `2B43C0` → `2AF340` → `2B2150`) bottoms
  out below the harness's old `STACK` base — the deepest nested decode
  cell (`rsp+0x20` ≈ `0x60FE0C8`) was unmapped, silently zeroing the
  decode cursor advance so the loop's next `movzx b[rbx]` read `[0]`.
  Stack map extended 1 MB below `STACK`. Fault evidence: read of addr
  `0`, last block `0x2B22C0` (loop head `movzx ecx,b[rbx]`).
- **Decode counts:** the `*` arm's `2B43C0` calls each walk the
  (possibly suppressed) blob — `f2a`/`f2ac`: call1 sees `'A'`, call2
  sees `rest+w48=""` → 2 decodes total (call1 + nested1); `f2an`:
  call1 suppressed-empty, call2 + nested2 decode `'A'` → 2.
- **`*`-arm suppress order:** suppress `rest[w48]` → `2B43C0(rest)` →
  restore → suppress `rest[w48+w44]` → `2B43C0(rest+w48)` → restore —
  verified against call-arg order, not just the earlier summary.

## Assert updates (existing cases, no count change)

- `c5f0-f38n`/`f3en`: `s2b41f0` → `b41f0` real-entry tag, `s39c4a0_ret
  ="c60"` added (wrapper-built state's flag desc), decode count 1→2,
  `b41f0v` dropped.
- `c5f0-f2a`/`f2ac`/`f2an`: `s2b43c0` → `b43c0`, `f2b43c0` dropped,
  decode counts corrected (2, 2, 2).

## Not claimed

- Live-game reachability (`live_game: false`); runtime tables remain
  fixture-planted (`eac10t`, `ba30t`, `a930m`, `nobj`/`rstr`, `ba00t`).
- `2A9F00` publish, `2AE450` sprite draw, `2AE610`/`2AEB20`/`2B4730`/
  `3A1DB0`/`17FD30`/`2B1ED0` remain scripted boundaries; `808C40`
  cookie check stays a scripted boundary (records args only).
- `39C4A0` font pick stays scripted — its real return feeds the real
  wrapper only the planted flag-desc pointer.
- The `*` icon-fit clamp now consumes a real measured width in `xmm0`
  instead of a stubbed float; variant-table rows (`d[rbx]` count) are
  still fixture state.

## Result hash

`result.json` SHA256 `76e775e14bc615ce5ea1efda2e5025d76a81a6c4028388e96a39fe785cca0478` (identical across 3 runs).
