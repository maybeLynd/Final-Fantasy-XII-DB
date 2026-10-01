# EXP-226 — per-kind stat accumulator `316A50` family real (`315E90`/`316BF0`/`3166F0`/`3165C0`/`316760`)

**Status:** complete — **542/542 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 `8e870d84` prefix; 542
cases), zero unexpected faults** (the 10 faulted cases are the same
pre-existing intentional-null fixtures that assert the fault).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..225; no new cases — existing fixtures completed to
native depth and asserts retargeted from scripted keys to real tags +
write/notify evidence)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Bodies promoted real this round

`00316A50` (`s6a50`, ×56 — the second-largest scripted call) plus its
native helper cluster; `008632B0` UI sink becomes a *new* scripted
boundary (`b32b0` — its call args were previously invisible inside the
`316A50` stub).

| body | semantics | hits |
|------|-----------|------|
| `00316A50` (`l6a50`) | per-kind stat accumulator `(cl=kind<0x1E, edx=delta)` over shipped kind-desc table `0xD10460` (30×8B: `{b0=mode, b1=slot-off, b2=cmp-mode, d4=cmp-val}`) + msg table `0xD10550`. `mode!=0` → arm-2: `3166F0` get → cmp-mode 0 sat-add (mode2→[0,0x7FFF] u16, mode4→[0,0x7FFFFFFF] u32, else wrap), 3→`bts ebx,delta−0xE2`, 8→skip → `315E90` achieved-gate → `316BF0` write-back. `mode==0` → arm-1: cmp 0→threshold `edi≥3165C0?:d4`, 1→equality, else bail; achieved → set bit + `8632B0` inline. | ×56 |
| `00315E90` (`l5e90`) | achieved-gate: `b[2536A0()+k/8+0x3844]` bit pre-check (set → bail) → jump table `0x316098` over cmp-mode {0→`316760≥3165C0?:d4`, 1→bail, 2→`309EC0` free-count scan over `d4.lo..d4.hi`, 3→popcount `3166F0` ≥ `3165C0?:0x10`, 4→bail, 5→`3160C0`, 6→`3161A0`, 7→rel-ptr `q[0x22C2550]` row `w[d4]` + `315420>0`} → set bit + `8632B0(d[0xD10550+k*4])`. | ×56 |
| `00316BF0` (`l6bf0`) | write-back: `w`/`d[2536A0()+0x384C+b1]` per mode 2/4. | ×56 |
| `003166F0` (`l66f0`) | value getter: kind≥0x1E or mode-0 → −1; mode2→`w[base+0x384C+off]`, mode4→`d[…]`; also called inside `316760`. | ×111 |
| `003165C0` (`l65c0`) | threshold lookup: 4-level relative-word pointer chain from `q[0x22C2550]` (BSS null under fixtures → 0 → callers substitute `d4`/0x10 defaults); `d[r10+4]` bitmask `bt kind` → selects indexed `d[r10+i*4+8]`. | ×55 |
| `00316760` (`l6760`) | value-with-fallback: `3166F0`; −1 → kinds 5/8 special array scan (`282DD0`/`282FA0` over `q[0x209AC30]+0x408`) — unreachable under suite kinds. | ×55 |

## Corrections of record

- **`316A50`'s kind is the low byte `cl`, not `ecx`.** `254EE0`'s
  `mov cl,6|7` patch records rcx=`0x506` in `rargs`, but `movzx esi,cl`
  + `cmp cl,0x1E` route it as kind 6 — confirms EXP-223's reading that
  the patch is byte-local.
- **`315E90` evaluates the achieved-gate on the PRE-WRITE stored
  value** — `316A50` arm-2 calls `315E90` before `316BF0` write-back;
  the gate reads `316760`/`3166F0` (old value), not the new `ebx`.
- **Achieved-bit dedup is real:** the second `316A50(0xB)` in
  `d228-2g` hits the `b[+0x3844+1]&8` early-bail — `l65c0`/`l6760`
  ×55 vs `l5e90` ×56 — and `b32b0` notifies only once per kind per
  case.
- **Kind-table arm-1 bail:** cmp-modes {1,4} are jump-table-reserved
  (`→0x31607d`); kinds with `mode==0` and cmp∈{2,5,6,7} bail in
  `316A50` arm-1 — their `315E90` gates are driven by direct
  `315E90` call sites elsewhere, not by `316A50`.
- `q[0x020927C0]` (returned by `2536A0`) is now **default-planted**
  (`msgtab`, 0x3900) — `316A50` reads `+0x3844`/`+0x384C` unconditionally;
  previously opt-in at 0x3800 for `315820`'s `+0x3404` counter arm.
  Same physical table: member-seen counters + stat slots + achieved
  bits.
- `q[0x22C2550]` (the `3165C0`/`315E90`-mode5/7 threshold descriptor)
  is BSS-null under fixtures → `3165C0`=0 → `d4`/`0x10` defaults —
  disclosed, not live-populated.

## Fixture disclosure

| fixture | maps to | notes |
|---------|---------|-------|
| `msgtab` (now default) | `q[0x020927C0]`, 0x3900 | `+0x3404` msg counters (315820), `+0x3844` achieved-bits, `+0x384C` stat slots |

## Assert upgrades

`by("s6a50")` → `byr("l6a50")` ×13 (same arg slots: rcx=kind,
rdx=delta, r8=caller-computed total). New write/notify evidence on
`d228-e9a8` (kind4 `w[+0x3854]`=1, bit4, `b32b0` msg 5) and `d228-g1`
(kind11 `d[+0x385C]`=10, bit11, msg 13). `b32b0` msg census: {5:24,
9:19, 13:9, 8:2, 10:1} = kind→msg {4→5, 17→9, 11→13, 6→8, 7→10}.

## Scripted boundaries still recorded

`30FED0` (`fed0` ×196), `3105D0` (×28), `2EB0D0` (`kb0d0` ×26),
`319490` (×19), `2E42D0` (×18), `3B02A0`, `46AB10`, `8632B0`
(**new** `b32b0` ×55 — `316A50`/`315E90`'s UI notify sink),
`317ED0`/`3180F0`/`319CA0`, allocators.

## Fault census

10 intentional-null fixture faults, unchanged: `ac80-member-nulld`,
`ac80-foe-nulld`, `ac80-foe-oidx28`, `ac80-foe-globnull`,
`l8b40-nomemt`, `a8ff0-nodesc`, `c650-nolvl`, `u0fc0-norec`,
`l01140-norec`, `d228-globn`.
