# EXP-238 — registered-language resolver `39BAD0` real

**Status:** complete — **542/542 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 `e156ff72` prefix; 542
cases), fault census unchanged at 20** (the same pre-existing
intentional-null fixtures).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..237; no new cases — the `s39bad0` scripted sink now
executes the shipped body; asserts retargeted to the real tag).
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Body promoted real this round

`0039BAD0` (`l39bad0`, ×8) — the registered-language→slot resolver
the display/text family (`3BBD00`, `2BD4D0`, `2B3050` and their
`2B3420`-style siblings at `0x2A549F`/`0x2B3096`/`0x2B540D`/
`0x2B554C`) uses:

```text
rdx = rcx ;  if rcx == 0:              ret 0
for eax = 1 .. 7:                     ; slots 1..7 only — slot 0
    if d[0x2AEE810 + eax*8] == edx:   ret eax
ret 0                                 ; no match
```

The table is the shared 8-slot `0x2AEE810` record area — `39BA30`
indexes the same table by slot for its qword font-record pointers
(`ba30t` fixture), while `39BAD0` matches on each slot's low dword.
It is BSS — the shipped image carries all-zero slots.

## Why a fixture is needed

Six of the eight harness calls used the stub default 0 — matching the
BSS-zero shipped table — but `b3050-arm`/`b3050-alt` planted
`s39bad0_ret=7` to exercise `2B3050`'s system-language arm
(`bl==7` → `bts d[state+0x44], 0xB` + second `39C4A0` call when
`254A10()==0`). With `39BAD0` real, a stub return is no longer
available: the new **`bad0t`** case key writes
`d[0x2AEE810 + i*8] = v` for each `{i: v}` entry, and the two arm
cases plant `bad0t={7: 0x44}` — the caller's `rcx=0x44` now hits slot
7 of the *real scan*, so the language-7 branch runs because the
shipped body computed 7, not because a stub declared it.

Per-case outcomes under the real body:

- `b3050-run` — `rcx=0x44`, no table match → ret 0; no arm. Same
  observable behavior as the stub's default 0.
- `b3050-arm` — `bad0t={7:0x44}` → ret 7; `254A10()==0` (`e2814v=1`)
  → `bts` + second `39C4A0` (real, EXP-218). Pinned: `c4a0` ×2,
  `d[state+0x44]` bit `0xB` set in the copied state.
- `b3050-alt` — `bad0t={7:0x44}` → ret 7; `254A10()!=0` → arm
  suppressed — `c4a0` ×1 only, no `0xB`. The gate, not the scan,
  decides suppression.
- `bd00-t2`/`bd00-t2b25`/`bd00-t2neg`/`bd00-t2pri`/`d4d0-near` —
  `rcx=0` early-out or non-matching values on the BSS-zero table →
  real 0, stub-equivalent.

## Corrections of record

- **Table base corrected before first green run:** the `lea` at
  `0x39BADD` is `rip + 0x2752D2C` computed from `0x39BAE4` →
  `0x2AEE810`, not `0x2B0E810` as first written (0x20000 error).
  Caught by a direct emulation probe: `l39bad0` recorded
  `(rcx=0x44, …)` but returned 0 with the plant landing outside the
  scanned range. Fixture writes confirmed via
  `gm.d(0x2AEE810 + i*8)` post-init.
- Slot 0 is unreachable for matches (eax starts at 1) — a `bad0t`
  plant at `{0: v}` can never be returned; documented so future
  callers don't pin an impossible arm.
- `bad0t` composes with `ba30t`: both write the same 8 slots but no
  case carries both keys; `bad0t` writes only the low dword and
  leaves the high dword for `39BA30`'s pointer reads.
- Assert retargets: `by("s39bad0")` → `byr("l39bad0")`; the SCR
  `s39bad0`/`s39bad0_ret` map entry removed. Zero regression
  failures after the base fix — **542/542**.
- Census: `l39bad0` ×8, stale `s39bad0` ×0.

## Boundaries (unchanged disclosures)

`30E130` (`e130` ×0), `290B90` (`s290b90` ×34), `317E50` (`b7e50`
×0), `20CE60` (`v20ce60` ×0), `427320` (`v427320` ×1), `422C20`
(`v422c20` ×1), `3377C0` (`v3377c0` ×19), `28EF70`/`28EF00`
(×1/×0), `2E9BB0`/`2EC5B0` (×0), `3B02A0`, `46AB10`, `210EC0`,
`1CCB20`, `3180F0`, `319CA0`, `426130` remain scripted.
`live_game: false`.
