# EXP-217 — measure/skip helper `2B1FB0` promoted real

**Status:** complete — **525/525 cases, stable across 3 independent runs,
byte-identical `result.json` (SHA256
`9ba88990fa371111f6f282ff1a1071ff5ba0a4353996ee4a45eb04992f1efcf1`),
zero unexpected faults.**
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..216; 523 inherited cases + 2 new direct-entry cases)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Scope

`2B1FB0` was unmapped (never stubbed — none of its seven callers sit on
the current harness paths). Static analysis showed it fully bounded:
all callees already mapped (`861EC0` memset hook, `s39c4a0` font pick,
`s2ac2f0` decode stub, real `2AC5F0`, `808C40` cookie). Two
direct-entry cases cover both dispatch sides.

## Body promoted real this round

| body | semantics |
|------|-----------|
| `002B1FB0` | measure/skip helper — `861EC0` memset of a `0xD0` local state + default field writes (`w+0x9C=0x1E`, `f+0xB4`/`+0xB8`/`+0xBC`=1.0, `b+0xA0`=1, `b+0x9A`=0x25, `b+0xA8`=0xFF, `b+0x9E`=8, `q+0x88`=0x30000, `d+0x44 |= 0x200`), `39C4A0((d44>>0xB)&1)` font pick → `q[rbp-0x60]` (stored, unread on this path), cursor cell `q[rsp+0x28]=arg`, then `b[arg]` dispatch: `>0xF` → `2AC2F0(state,&cell,0)` decode; `<=0xF` → real `2AC5F0(state,&cell,&rsp+0x30,&rsp+0x20)` control-code interpreter; returns `d[rsp+0x28] - arg` = bytes consumed |

## Call sites (static)

`0x2B20FB`, `0x2B45E3`, `0x2B4857`, `0x2B4A6A`, `0x2B52B3`,
`0x2B555E`, `0x2B56B4` — none reachable from the current harness's
executed bodies, so coverage is via the two direct-entry cases.

## Verified outputs (asserted)

- `b1fb0-c5` (`b[str]=0x0F`, kind `'m'`): real `2AC5F0` runs on the
  memset local state — no e312 fixtures needed because `'m'` is the
  pure `3FFB90` skip arm — `l3fb90` called with `arg=nstr+1`,
  consumed return = 4.
- `b1fb0-dec` (`b[str]=0x41 > 0xF`): `s2ac2f0` decode-stub path,
  advance 3 → consumed return = 3, `2AC5F0` not taken.

## Corrections of record

- `2B1FB0`'s `39C4A0` return is **stored but never dereferenced** on
  either dispatch side — unlike `2AE610`/`2B41F0`, this body needs no
  `s39c4a0_ret` fixture.
- The helper's cursor cell is `q[rsp+0x28]`, initialised to the arg
  pointer, and the return is a **dword** subtract of the low 32 bits —
  consumed length, not a pointer.

## Still scripted / not claimed

`2AFDC0` render submit, `17FC90`/`17F7C0` emit internals (deep
`1B5FA0`/`1Exxxx`/`18xxxx`/`2DD8xx` render leaves), `2AEB20` nested
catch-all (`1E0C10`/`2AB8F0`/`2DDC50`/`180150`/`228480`/`2441E0`
chain), `17Fxxx` font shims, `39C4A0`, `2AC2F0`, `808C40`. No live-game
claim — `NATIVE-REPLAY`, `live_game: false`.

## Verification

`python check.py` → 525/525 pass, zero unexpected faults; three
independent runs → byte-identical `result.json` SHA256
`9ba88990fa371111f6f282ff1a1071ff5ba0a4353996ee4a45eb04992f1efcf1`.
