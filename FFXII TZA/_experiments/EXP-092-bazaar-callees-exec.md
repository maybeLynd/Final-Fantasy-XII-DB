---
experiment: EXP-092
title: Bazaar callees under isolated original execution
contract: ../12-Items-Equipment-Shops-License/CONTRACT-bazaar-unlock-and-purchase.md
method: B
live_game: false
tool: evidence/bazaar-callees-exec/check.py
---
# EXP-092 — bazaar callee execution

**Status:** complete · **80/80 cases, 11/11 mutants, stable across two processes**
**Evidence:** `evidence/bazaar-callees-exec/` (`check.py`, `result.json`, `bodies.json`, `run2.log`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

`CONTRACT-bazaar-unlock-and-purchase.md` §13's pilot ran the four bazaar
entries under `Reconstruction/Tests/Differential/diff_bazaar.py` with three
callees supplied as **scripted oracles**: the gate `00322C50`, the tally
op `003008A0`, and the class record's `+0x50` handler. Its UNKNOWN row: what
those callees do is *not* established. This package re-drives all four
entries with every reachable callee executing as shipping bytes under
Unicorn — zero stubs.

## Executed bodies (real shipping bytes)

16 bodies, spans + sha256 in `bodies.json`:

| VA | role |
|---|---|
| `0030B180` | purchase — gate `00322C50(0x12,id)` → row resolve → flag `&= ~2` → three `003008A0(loot,0,1,3)` calls |
| `0030B270` | refresh — per-row predicate, two inlined `+0x50(edx=3)` calls + `0030ADC0` for loot 3 → flag `|= 3` |
| `0030B570` | script-set — nibble `0xD000` → `00322C50(1,id)` → row `+0x14` bit1 gate → flag rewrite |
| `0030ADC0` | tally query — sentinels/bounds → `jmp [fam+0x50]` with `edx=3` |
| `00322C50` | kind dispatcher — `(ecx-1)` indexes jump table `0x323054`; `edx` is the tested value |
| `00309440` | class-number read — `fam[id>>12]+0x38` lo dword |
| `003008A0` | id op — sentinel/bounds → `famd(id,r9)` pre-read → `[fam+0x48]` handler |
| `00309F30` | famd — bounds → `edx==4` → `002FD970`; else `jmp [fam+0x50]` |
| `002FD8D0` | fam0/1/2 `+0x50` reader — four edx arms |
| `002FD970` | bitset reader (`edx==4` arm target) |
| `002FD150` | fam0/1/2 `+0x48` writer — r9 arms 0/1/2 u16 packed, 3 byte |
| `002FD780` | fam13 `+0x48` — gated `r8==0 && r9==1`, else returns 0 |
| `002FD880` | fam14 `+0x48` — gated same; calls `00254EE0(00253690()+idx*edx)` |
| `0020E600` | RVA→ptr — `ecx + [0x1F83530]` |
| `00253690` | `[[0x2092758]+8]` read (bank) |
| `00254EE0` | clamped bank write to `[0x2092758]+8`, `00316A50` only on nonzero delta |

**Stubbed:** none. No IAT call is reached on these paths.
**Deliberately unreached (hooked, never fired):** `002FD420` (fam3+ `+0x48`
bitset acquire — loot ids scoped to fam1), `00316A50` (bank-delta notify —
`sg-fame-bank` uses `idx=0` → delta 0), `0031EA90`.

## Findings (corrections to the contract's pilot model)

1. **The refresh query is a byte, not the u16 tally.** `+0x50` arm map:
   `edx=0` → `(w&0x3FF) − (w>>0xA)`; `edx=1` → `w&0x3FF`; `edx=2` → `w>>0xA`;
   `edx=3` → `byte[[fam+0x20] + idx]`. Refresh and `0030ADC0` both use `edx=3`
   — they read the **byte table** `fam+0x20`, the same bytes purchase zeroes.
   The u16 table `fam+8` is only touched by the `edx∈{0,1,2}` arms and by the
   `+0x48` r9∈{0,1,2} writes.
2. **Purchase's tally write is a byte-table absolute zero** — `003008A0` with
   `r8=1, r9=3` lands on `002FD150`'s byte arm: `byte[fam+0x20+idx] = 0`
   (absolute, clamped `0..0x63` on nonzero deltas). Three `idop` calls per
   purchase, one per loot slot `row+0x16/+0x1A/+0x1E`.
3. **`003008A0` r9==1 u16 arm clamps UP to hi6**, not to it from above:
   `new_low10 < hi6` → writes `hi6`; `new ≥ hi6` → writes `min(new, 0x63)`.
   Absolute mode (`r8≠0`) follows the same rule with `edx` replacing
   `low10+edx`.
4. **`00309F30` shares `003008A0`'s sentinel logic** — `0xFFFF` and nibble
   `>0xE` return `−1`, not 0 (measured: `famd-sentinel`, `famd-highnib`).
   `0030ADC0` returns `−1` for the same inputs.
5. **`00322C50` kind 1 is a class-number indirection**: `00309440` reads
   `fam[id>>12]+0x38` (lo dword = class number: fam1→`6`, fam13→`0x12`,
   fam14→`0x13`) and re-dispatches. So `0030B570`'s `bound(1, id)` on a
   `0xD000` id lands on the same arm-`0x12` goods window as the purchase gate;
   `0xE000` lands on arm `0x13` (`[0xE000, 0xEFFF)`).
6. **Arm-`0x12` bound is `[0xD000, 0xD000 + [[0x2EBF058]+4])`** — the live
   registry row count, not a constant. Empty registry (`reg=0` → bound fails)
   is a clean reject; a null *row* (empty RVA + zero `0020E600` base) is an
   unguarded `word[0+0x16]` / `byte[0+0x14]` fault — measured, kept as
   `expect_fault` cases.
7. **Script-set (`0030B570`) requires `id&0xF000 == 0xD000` before the gate**;
   flag byte update is `(old & ~2) | ((edx&1) << 1)` — bit0 untouched, gated
   on row `+0x14` bit1.
8. **Sequence semantics:** refresh sets bits `0|1` together; purchase clears
   bit1 **and** zeroes the sold bytes — so a repeatable row re-runs the full
   predicate post-purchase (queries fire, byte tallies now 0 → fails) while a
   one-time row skips at clause 1 with no queries. Trace counts distinguish
   the two (`seq-repeat`: 7 `r50a`; `seq-one-time-trace`: 6).
9. **fam14 `+0x48` (`002FD880`) is the gil-bank write**: gated
   `r8==0 && r9==1` → `00254EE0([[0x2092758]+8] + (id&0xFFF)*edx)`, clamped
   `[0, 0x5F5E0FF]`; `00316A50` notify fires only on nonzero delta.
10. **fam13 `+0x48` (`002FD780`) unpacks the goods row's own loot slots** —
    gated `r8==0 && r9==1`, per-loot `003008A0` calls. Purchase's `r8=1,r9=3`
    call shape fails that gate and returns 0 — verified, no side effects.

## Fixture disclosure

Planted: `[0x2EBF058]` registry object (`+4` count, `+8` stride, `+0xC` RVA),
`[0x2EBF190]` flag array (`byte + idx + 0x59C8`), `[0x1F83530]` `0020E600`
base, `[0x2092758]` bank object (`+8`), fam0/1/2 `+8`/`+0x20` data pointers
(runtime-null in the shipped image — the family table's counts and fnptrs
are shipped constants). All state below 4 GiB per the body's 32-bit row
pointer arithmetic (`imul ebx`; `add ebx, eax`).

## Mutation campaign

11 mutants, all detected: arm-`0x12` bound low, purchase gate kind,
`00309440` nibble bound, refresh `or 3`, purchase `and 0xFD`, threshold
`jl`, script-set nibble, script-set row-gate imm, `+0x50` `0x3FF` mask,
`+0x48` written clamp constant, all-zero-threshold `je`.

## Scope limits

- `002FD420` (fam3+ `+0x48` bitset acquire/release) and its callbacks
  `00325F40`/`0046A630` were not exercised — loot ids were scoped to fam1.
- `00316A50` (bank-delta notify) unreached — `sg-fame-bank` keeps delta 0.
- The flag array's *meaning* beyond bits 0/1 at `+idx+0x59C8` is fixture
  layout, not measured game layout.
- Live-process confirmation of the same constants remains ASTRA's lane.
