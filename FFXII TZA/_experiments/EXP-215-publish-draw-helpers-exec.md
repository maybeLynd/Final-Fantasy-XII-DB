# EXP-215 — publish/draw helper chain `2A9F00`/`2AE610`/`2AE450`/`39BB00` promoted real

**Status:** complete — **521/521 cases, stable across 3 independent runs,
byte-identical `result.json` (SHA256
`6a5b2d66885cef5bb47706c91391ae3f1fd4b80c582fb121278a10c0909be307`),
zero unexpected faults.**
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..214; 521 inherited cases, 3 re-fixed for the promotion)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Scope

EXP-214 left the whole publish side scripted: every measure tail ended
at the `s2a9f00` boundary and the `-`/`?` arm helpers were stub returns.
This round promotes the four bounded bodies at the top of that tail —
the `?`-arm sprite draw, the `-`-arm decoration measure/publish, and the
glyph-run publisher both of them (and the `8`/`>`/`*` arms) share.

## Bodies promoted real this round

| body | semantics |
|------|-----------|
| `0039BB00` | mode dispatch leaf — `ecx==1` → `q[0208EA90]`, `ecx==2` → `q[q[0209AC30]+0x338]`, else → `q[0208EAA8]` (BSS singletons) |
| `002AE450` | `?`-arm sprite/icon draw — `39BB00(mode=r9d)` → sprite table → `q[tab+0x20]` record (+0x30 base): `w[+0x10]` blob offset, word-pair table at `+0x14` indexed `[arg5>>8]` then `+(arg5&0xFF)`, `d[blob + (pair + param)*8 + 4]` = metric dword (bits 0..11 → `f[0209CC60]` × `f34*f38`; bits 12..23 → `f[0209CC64]` × `f34*f3C`; lo-scaled + `f4C` → `f[0209CC68]`), `movsx(bAB)+movsx(b44)` advance × scale → `xmm6`, `bl` flag bits 1/2/4/8 gate const adds (bit 8 gated on `254A10()`), `bA9` hi metric override → `f[0209CC64]`, then `2AFDC0` render submit |
| `002AE610` | `-`-arm decoration measure+publish — `0xD0` state copy, `39C4A0((d44>>0xB)&1)` font pick (record `r15` — **both paths** read `d[r15+0x14]`/`w[r15+0x20]`/`d[r15+0x18]`), `17F940` font-ctx save, `3FFC60` re-parse of the `-` param bytes, `b[ctxo+0x10FC]==2` flag, `d[e312+0x44]&0x800`-gated deep measure (`20E600(d[r15+0x14])` glyph row, `d[*r9] = min(bA1,bA2)`, `q[0209C598]` reset, `2AC2F0` decode loop, `17F880` height, `3EFD00` digit format, `2A9F00` publish), `808C40` cookie |
| `002A9F00` | glyph-run publisher — `0x70`+`0x80` state copies into frame; ctx48==0 fast path skips the glyph loop; else per-glyph: `d[ctxo+0x10DC]` countdown, `f[ctxo+0x10E4]` accumulate, `d[ctxo+0x10D8]` dec, real `2AC2F0` decode, `20E600(d[rdi+0xC])` glyph table row, `17F8C0` codepoint→glyph remap, `d[rec+idx*8]` flag word (`0x80000000` → `b[ctxo+0x10FC]=1`, else `=2`), `d[rdi]&0x18000`/`d[rbp+0x10]`-bit21 → `254A10` gate + `b[rip+0x66C3BD + movsx(b[rbp+7])]` colour-class table, writes quad-command records into `q[0209CC50]` display-list cursor (`q[+0]=encoded cmd`, `q[+8]=6`, `q[+0x18]=8`, coords/metrics into `+0x10`,`+0x14`,`+0x20`,`+0x24`,`+0x30..`), `17FC90` quad build, `17F7C0` emit, `d[ctxo+0x10D4]>=0x14` → `2B4730` batch flush, real `2AC5F0` re-interpretation of `0x0F`-control bytes found mid-string (subs `<=0x3E`/`==0x70` gate via `bt rsi,rax`) |

## Call sites now real

- `0x2AD728` — the `*` icon arm's publish (ctx48-gated): `2A9F00(
  rbp-0x70 copy, &rsp+0x60 cursor = rest, rbp+0x70 float out, ...)`.
  Icon-fit clamp math above it (`w[rbp+0x1C] = min(ecx, f10E4·w1C/
  w10D8-ratio)`) now feeds a real publisher.
- `0x2ADABA` — the `*` arm's per-icon-variant publish inside the
  `2B2970` loop (`q[rsp+0x68] = q[vartab+idx*8+8]` variant string).
- `0x2ADFED` — the `8`/`>` resolved-resource publish.
- `0x2AD8EB` — the `-` arm's `2AE610` tail (the `f2d` path).
- `?` arm — `2AE450` sprite draw (`f3f`).

## New fixtures (disclosed)

- `sprt=[idx,lo,hi]` — plants `q[0208EA90]`/`q[0208EAA8]` → sprite
  table → `q[tab+0x20]` record, metric dword at `rec+0x34+idx*8`.
- `q[0209CC50]` — display-list write cursor, always planted
  (0x2000 buffer at +0x10 so `2B4730`'s `rdx-0x10` header write would
  stay in-bounds).

## New scripted boundaries (disclosed)

- `0x2AFDC0` — `?` draw's render submit (`s2afdc0`).
- `0x17FC90` — `2A9F00`'s glyph-quad builder (`s17fc90`).
- `0x17F7C0` — `2A9F00`'s glyph emit (`s17f7c0`).

## Corrections of record

- The `-` arm (`f2d`) always runs `2AE610`'s font-pick — **both** the
  `d44&0x800` deep path and the early path read `d[r15+0x14]`/
  `d[r15+0x18]`, so `s39c4a0_ret="c60"` is required unconditionally.
- The real `2A9F00` consumes its own `2AC2F0` decode per glyph inside
  the publish loop — `f2ac`'s `c2f0` sequence grew 2→3 entries.
- Unicorn's fault-hook RIP can land mid-translation-block (observed
  up to -0x380 bytes early); identify faulting instructions by the
  `ibs` byte pattern at RIP, not by file disasm at the reported VA.
- `2AE450` metric mapping (verified by assert): `f[0209CC60]` = lo12 ×
  `f34*f38`, `f[0209CC64]` = hi12 × `f34*f3C`, `f[0209CC68]` =
  lo-scaled + `f4C`.

## Still scripted / not claimed

`2B4730`/`3A1DB0` (display-list append — needs `q[0209CC48]` ctx48 +
`q[0209E5A0]` cmd-buffer globals; derefs them unconditionally), `2AE450`'s
`2AFDC0` submit internals, `17FC90`/`17F7C0` emit internals, `2AEB20`
nested catch-all, `2B1FB0`, `17FD30`/`2B1ED0`/`17F880`/`17F850`/`17FA10`/
`17FB00`/`17F920`/`17F9C0`/`17F940`/`17FAE0`/`17F8C0` font shims,
`39C4A0`, `2AC2F0` decoder, `808C40` cookie. No live-game claim —
`NATIVE-REPLAY`, `live_game: false`, fixture-planted tables throughout.

## Verification

`python check.py` → 521/521 pass, zero unexpected faults; three
independent runs → byte-identical `result.json` SHA256
`6a5b2d66885cef5bb47706c91391ae3f1fd4b80c582fb121278a10c0909be307`.
