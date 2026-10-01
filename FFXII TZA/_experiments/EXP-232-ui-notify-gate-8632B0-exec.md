# EXP-232 — UI notify gate `8632B0` + singleton getter `20CE00` real

**Status:** complete — **542/542 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 `deb5a557` prefix; 542
cases), fault census unchanged at 20** (the same pre-existing
intentional-null fixtures).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..231; no new cases — the `b32b0` scripted sink now
executes the shipped gate; asserts retargeted to the real tag).
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Bodies promoted real this round

| body | semantics | hits |
|------|-----------|------|
| `008632B0` (`l32b0`) | UI message notify thunk, `ecx`=msgid: `20CE00()` singleton → null → ret; else `20CE60(ctx, msgid)` tail dispatch. | ×55 |
| `0020CE00` (`l20ce00`) | singleton getter — `return q[0x1F83450]` (2 insns). | ×55 |

`8632B0`'s six callers are the `316xxx` stat-family gates
(`0x316078`/`0x316403`/`0x31646D`/`0x316AEA`/`0x316B47`) plus
`0x352262`; the ×55 calls ride the EXP-226 `316A50` accumulator's
achieved-bit notify (msgs 5 and 13 pinned in `d228-*`).

## `20CE60` — the disclosed scripted boundary (`v20ce60`, ×0)

`0020CE60`(ctx, msgid): `imul msgid,0x198` row into `q[ctx+8]`,
dedupes on `b[row+0x190]` (sets it + `d[+0x194]`=0), then when
`b[ctx+0x18]` is armed, forwards `q[row+8]` through two manager
objects' vtables (`call [vt+0x38]` / `jmp [vt+0x50]` on
`q[obj+0x28]`). Sole caller in the image is `8632B0`'s tail jmp, so
the interception is exactly scoped. Promoting it needs a UiManager
fixture (0x198-stride slot array + armed `+0x18` + two live vtable
objects) — left as a boundary a future fixture can surface.

## New fixture

`q[0x1F83450]` planted 0 in the default fixture block — the pre-init
singleton state. The shipped `.data` file bytes at `0x1F83450` are
stale non-pointer data (`0x01C32BC8_0005F876` dword pair); init code
publishes the real object at runtime. Left unplanted, a real
`8632B0` would dispatch `20CE60` into a non-canonical pointer and
fault — null is the honest replay state and turns the gate into a
verified no-op.

## Corrections of record

Assert retargets only — `by("b32b0")` → `byr("l32b0")` (rcx=msgid):
`d228-e9a8` pins msgid 5 and now also `v20ce60` ×0; `d228-norow2`
pins msgid 13 present. Zero regression failures — the stub and the
real gate are observably identical on the null singleton.

## Boundaries (unchanged disclosures)

`30E130` (`e130`, ×0), `290B90` (`s290b90` ×34), `317E50` (`b7e50`
×0), `2EB0D0` (`kb0d0` ×26), `319490`, `2E42D0`, `46AB10`,
`426130`/`427320` remain scripted; `v20ce60` added (×0).
`live_game: false`.

## Regression triage

**542/542 first run — zero regressions.** The promoted gate is
observably identical to the stub under the null singleton; the only
changes needed were the two `by`→`byr` retargets.
