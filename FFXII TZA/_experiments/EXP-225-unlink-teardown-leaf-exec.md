# EXP-225 — unlink/teardown leaf family real (`2ECF10`/`313F60`/`17FD30`/`2699D0`/`2ECEC0` + `1E9D20`/`2EB430`/`3AEEF0` tails)

**Status:** complete — **542/542 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 `9ed60fb8` prefix; 542
cases), zero unexpected faults** (the 10 faulted cases are the same
pre-existing intentional-null fixtures that assert the fault).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..224; +1 case `u43f0-ec` for the `2ECEC0`→`3AEEF0`
chain-clear arm; `s17fd30` `on_code` shim removed)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Bodies promoted real this round

The unlink/teardown leaf family reached by `003243F0` and `0031A630`
(EXP-224): five scripted entries removed from SCR plus the `s17fd30`
`on_code` shim; nine REAL tags added (`0x377C20` already carried
`cd7c20` — kept, not duplicated).

| body | semantics | hits |
|------|-----------|------|
| `002ECF10` (`l2ecf10`) | unlink leaf `(obj, kind)`: null `q[obj+0xC0]` early-out matches fixture layout; `b[obj]&0x40` arm tail-jumps `426130`→`427320` (heavy chain — never triggered under these fixtures, stays scripted). | ×17 |
| `00313F60` (`l313f60`) | **thunk `jmp 0x377C20`** — not a separate body; both `l313f60` and `cd7c20` trace per call. | ×9 |
| `00377C20` (`cd7c20`, pre-existing tag) | can-use flag: `eax = 3148F0()` (=`d[0x21654C4]` clamped via `2EF2B0` static — BSS zero → row 0), then `w[q[0x2ADD100]+8+eax*3] >> 0xF`. Driven by the existing `cd_words`/`cd_count`/`cd_idx` fixtures (`q[0x2ADD100]` desc). | ×101 |
| `0017FD30` (`l17fd30`) | flag→0/1 wrapper → `1E9D20`. | ×19 |
| `001E9D20` (`l1e9d20`) | map-find + set on the `q[0x1F811F8]` device singleton (`dev1` fixture, 0x2800 bytes). **Null-map early-out also zeroes `dev1+0..+0x24`** — the stub-era shim skipped this; all-zero writes are net-no-op under fixtures. | ×19 |
| `002699D0` (`l2699d0`) | tail-jumps `2EB430`. | ×18 |
| `002EB430` (`l2eb430`) | teardown writes: `b[obj+0xD] &= 0xFE`, `b[obj+0xF5] = 0xFF`, `d[obj+0xEC] = 0`, `d[obj+0xF0] = 0x1001`; calls `2EB0D0` (`kb0d0`, scripted boundary ×26) only when `b[obj+0x18]==1`. | ×18 |
| `002ECEC0` (`l2ecec0`) | element teardown `(rec/idx)`: resolves element `q[0x22C6F28] + idx*0x740` (`ecarr` fixture); `d[elem+0x284]!=0` arm → `3AEEF0(elem+0x550)`. | ×19 |
| `003AEEF0` (`l3aeef0`) | bounded node-chain clear: walks `next` at `node+0x48` (marker at `node+0`), zeroes head/next fields. New `u43f0-ec` case exercises it through `3243F0`→`2ECEC0` with two planted chain nodes. | ×1 |

## Corrections of record

- **`3243F0`'s `300E40` gate is `d[q[obj+0x698]+0x64] & 0x80000003`,
  then `313F60` ret, then `byte[obj]&2`** — the stub-era
  `rec_d={0x3C:1}` modeled a fiction; the actual flag word lives on the
  *linked object* at `+0x64` (`obj698` fixture already targets it,
  `recd={0x64:..}`/`rec_d={0x64:..}`).
- **`313F60`'s return is `377C20`'s table bit15.** Default
  `cd_words=[0x8000]*8` → ret 1 → `300E40`-skip arm; the stub-era
  default ret was 0. Cases that need the run arm now explicitly plant
  `cd_words=[0]` (`u43f0-3f`, `a630r9-rec3c`, `u0fc0-s400`,
  `d4da0-gate`); the three ret-1 cases need nothing (the default is
  already all-set). An initial `f60d` fixture duplicated the existing
  `cd_words` mechanism and was removed before landing.
- **`0x377C20` already carried the REAL tag `cd7c20`** (EXP-era
  accessor). Adding a second tag silently overwrote it and broke
  `tcount("cd7c20")`/`"cd7c20" in trace` asserts in
  `f690-*`/`s8130-b16clr`/`d228-gflg*` — resolved by keeping `cd7c20`.
- `cd_idx` defaults to `d[0x21654C4]` = BSS zero → row 0 of the table.
- Regression arc: 9 failures → all classified as fixture-polarity
  (`cd_words` default) + the duplicate-tag collision — none weakened.

## Fixture disclosure

| fixture | maps to | notes |
|---------|---------|-------|
| `cd_words`/`cd_count`/`cd_idx` (existing) | `q[0x2ADD100]` desc: count `+4`, u16 rows `+8+i*3` | pre-existing; default `[0x8000]*8` |
| `objc0` (new) | `d[objent+0xC0]` link-element idx | null → early-out |
| `ecarr` (new) | `q[0x22C6F28]` element array, stride `0x740` | `d`/`q` fields, `chain` nodes |
| `dev1` (existing) | `q[0x1F811F8]` device singleton, 0x2800 | null map → `1E9D20` early-out path |

`ecarr` rows: `{"elems": n, "rows": {i: {"d"|"q"|"chain": {off:
[marker...]}}}}` — chain nodes get marker at `+0`, `next` at `+0x48`,
wired for `3AEEF0`'s walk.

## Scripted boundaries still recorded

`30FED0` (`fed0` ×196), `316A50` (×56), `3105D0` (×28), `2EB0D0`
(`kb0d0` ×26 — the `2EB430` sink), `319490` (×19), `2E42D0` (×18),
`3B02A0` (×14), `46AB10` (×12), `2ECF10`'s `0x40` arm → `426130`/
`427320`, `3105D0`'s chain, `2ECA00` callers, allocators.

## Fault census

10 intentional-null fixture faults, unchanged: `ac80-member-nulld`,
`ac80-foe-nulld`, `ac80-foe-oidx28`, `ac80-foe-globnull`,
`l8b40-nomemt`, `a8ff0-nodesc`, `c650-nolvl`, `u0fc0-norec`,
`l01140-norec`, `d228-globn`.
