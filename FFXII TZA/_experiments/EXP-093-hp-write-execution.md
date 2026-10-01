---
experiment: EXP-093
title: HP write and lethal transition under isolated original execution
contract: ../08-Combat-Formula/CONTRACT-hp-write-and-lethal-transition.md
method: B
live_game: false
tool: evidence/hp-write-execution/check.py
---
# EXP-093 — hp-write-execution

**Status:** complete · **64/64 cases, 12/12 mutants, stable across two processes**
**Evidence:** `evidence/hp-write-execution/` (`check.py`, `result.json`, `bodies.json`, `run.log`, `run2.log`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

`CONTRACT-hp-write-and-lethal-transition.md` lists twelve callees as
**scripted oracles** in `Reconstruction/Tests/Differential/diff_hp_write.py`'s
pilot model. This package re-drives `00300530`
(`BattleStats_ModifyHPAndProcessLethalState`) and the `00300520`
absolute-set thunk with every reachable callee executing as shipping bytes
under Unicorn — the whole bounded closure, disclosed stubs only at deep
sinks.

## Executed bodies (real shipping bytes)

64 bodies, spans + sha256 in `bodies.json`. Headline set:

| VA | role |
|---|---|
| `00300530` | the HP write / lethal transition — executed from shipped bytes |
| `00300520` | absolute-set thunk: `edx -= [rcx+0x48]`, tail-jmp `00300530` |
| `0031B860` | unit lookup — scans `[0x208E6A0]` units at `[0x208E688]`, stride `0xF50`, matches `unit+0x698 == rec` |
| `0030B9B0` | gate 1 — `relat` + flag-builder low word + `cgate` low word |
| `0030B8E0` | gate 3 — `cgate` high word (ctx modes 1/2) |
| `00377C20` | active-field bit15 predicate |
| `003283D0` | RX — proximity gate (`002FA3B0` viewer/dist via `003A1920` sqrtf) → record build → `003BBD00` post |
| `003BBD00` | reaction-queue insert — real 64×0x50 slot write through `0028FBE0`/`00506700` + `003EFD00`/`0024A5A0`/`002DD7E0`/`002DD7B0` |
| `0028F1F0` | NB — view scan (`00296280`) → `003F8980` publish (flag clear or indirect callback) |
| `00316D70` | find tbuf |
| `0030E360` | status transition — KO set/clear, real subtree (`003848E0`/`00386A50`/`00386A70`/`003876D0`/`00387730`/`0020E600`/`0016D6A0`) |
| `00469BB0` | kill history — `002FA390`/`002F8E90` kind classify → `0046AB10` 10-entry ring insert with tick dedupe → `00469570` kind lookup |
| `0032A150` | tick getter |
| `00306F00` | group/death — spawn-kind gate, group row `0x2EC13C0`, deadmask/latch, completion path `00307140`→`002E1C20` caps → `00359200`/`00359330`/`0026BD20`, `bset`/`bclr` battle-state bits, own `ev(0x2005)` on completion |
| `003299B0` | event dispatch → `002EB030`/`002EB0D0` real post |
| `001D50D0` | lazy singleton getter — real, returns planted `0x1F81428` fixture (allocator arm bypassed by planting) |
| `0017D470` | context `+0xC20` read thunk |

## Stubbed boundaries (all disclosed)

Patched to `ret`, args logged, controlled returns where the suite needs them:

| VA | role |
|---|---|
| `005369C0` | kill-ledger presentation callback (fired) |
| `003112F0` | ST transition-result applier (never reached — no deferred result) |
| `00300FC0` | KO-arm defeat cleanup (fired) |
| `00312280` | rewards sink (fired) |
| `00301140` | recovery sink (fired) |
| `00300140`/`00307D10` | ST case-4 actions (never reached) |
| `003284D0` | reaction sink (fired) |
| `0030FED0` | post-write recompute (fired) |
| `0046A800` | extra kill-history add (fired) |

IAT thunks `00861EC0` (memset), `00861F14` (sqrtf), `008C3098` slot (rand)
jump to fixture routines; everything else is shipped bytes.

## Findings (corrections to the contract's pilot model)

1. **Ordinary non-lethal damage emits event `0x2005`** — the alive-event
   tail runs on every non-lethal non-positive-delta write, not only on
   kills. Positive heals emit nothing.
2. **The field/status refusal applies for `delta < 0`**, not zero or
   positive deltas: `test r14d` on the raw delta at `0030061C` + `jns`
   skips the `(rec+0x64 | rec+0x3C) & 0x80000003`-gated `00377C20` call at
   `0030062E` whenever delta ≥ 0. `downed-neg-*` reach it (HP unchanged,
   early out at `0030088C`); `downed-pos` bypasses it entirely.
   `downed-zero`'s `field15` trace token fires at a *later* call site of
   the same callee inside the executed closure — `00377C20` is called
   from more than one site and the token does not distinguish them.
3. **Gate-3 refusal suppresses the store and the lethal block but falls
   through to the alive-event tail** — `g3-kill-suppress` still posts
   `0x2005` with HP unchanged.
4. **Monster-band targets (`atype 0x1B..0x27`) take a single
   `ST(rec,src,status=0,mode=-1)` call and skip the normal KO cascade** —
   no KO bit write, no defeat-cleanup chain (`kill-party` vs
   `kill-group-done` traces).
5. **GD completion emits its own `ev(unit, 0x2005)`** — the main body's
   death event is suppressed on that path, GD's is not.
6. **Delta zero on a dead target re-enters the full lethal cascade.**
   Flag bit5 does *not* divert delta-0 to the heal arm: `r12d` is reloaded
   from the delta spill `[rsp+0xB8]` at `0x3006B7` before the gate-3/lethal
   tests, so bit5 feeds only RX's `isHeal` argument.
7. **Floor = `dword[targetUnit+0x48]`** when the lookup succeeds, 0
   otherwise; `floor-exact`/`floor-under` pin the `newHP <= floor`
   comparison.
8. **The reaction-queue insert is real**: `QUEUE+0` = work pointer,
   `QUEUE+0xC` = `0x80808080` sentinel written by `002DD7E0`'s fill, not
   the damage magnitude.
9. **`003F8980` callback ABI**: `(rcx=view, edx=1, r8=&{oldHP,newHP})`.
   No-callback arm clears view bit `+0x26`; `nb-publish`/`nb-callback`
   cover both.
10. **Killer id copies source-unit `+8` → target-unit `+0x30`**;
    spawn-backed targets increment the spawn counter and write the
    tick-derived respawn time; kill-ring dedupes on
    `{kind, tick-window}`.

## Fixture disclosure

Hand-planted: unit table `[0x208E688]`/count `[0x208E6A0]` (stride `0xF50`,
match `+0x698`), context singleton `[0x1F81428]`, field table
`[0x2ADD100]`/index `[0x21654C4]`, battle state `[0x2089340]`, mode/flag
bytes `0x22C2158`/`0x22C2160`, tick `0x208D45C`, queue `0x2B457D0`/cursor
`0x2B443C0`, kill-kind registry `0x2EBF018`/ring `0x2EBB560`/cursor
`0x2EBB54C`, codec base `0x1F83530`, status registry `0x2EBF118` loaded
from shipped `status_data.bin`, group table `0x2EC13C0`, capability table
`0x215F1C0`, suppression `0x22C8000/4`, completion dword `0x209A2C4`,
security cookie `0x1F44830` (top16 zero required), IAT slots.

This is **NATIVE-REPLAY on hand-built fixtures** — not live-game proof.
The object layouts are fixture layouts consistent with the bodies' own
offset arithmetic.

## Mutation campaign

12 mutants, all killed: floor comparison branch, alive event id `0x2005`,
death event id (`0x2007`/`0x2008`), killer-id store, spawn counter
increment, gate-3 invocation, downed mask, RX flag bit, KH inversion,
cap-double mask `bt 0x1C` patched at **both** test sites (`0x30067F`,
`0x3006A1` — patching only one left the mutant alive), freeze mask,
event-suppression bit.

## Unreached scope (hooked, never fired)

- `002E1CA0` — `caprow` `ecx=0` arm (capability clear); GD completion only
  exercises `ecx=1`.
- `00263FF0`, `00263E30` — `idres` sub-arms (class-getter, linked-object).
- Stubs `003112F0`, `00300140`, `00307D10` — never reached (no deferred ST
  result, no case-4 arm in this suite).

## Reproduction

```
python "Database/FFXII TZA/_experiments/evidence/hp-write-execution/check.py"
```

Requires the shipping EXE at the recorded path (hash-asserted) and
`Database/Tools/work/repos-2d/vbf/ps2data/image/ff12/test_battle/in/binaryfile/status_data.bin`.
