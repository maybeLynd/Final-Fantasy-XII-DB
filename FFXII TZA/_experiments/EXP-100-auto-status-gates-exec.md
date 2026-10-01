---
experiment: EXP-100
title: Auto-status gate chain under isolated original execution
contract: ../10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md
method: B
live_game: false
tool: evidence/auto-status-gates-exec/check.py
---
# EXP-100 — auto-status-gates-exec

**Status:** complete · **40/40 cases, 13/13 mutants, stable across two processes**
**Evidence:** `evidence/auto-status-gates-exec/` (`check.py`,
`result.json`, `bodies.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

`CONTRACT-auto-status-rebuild.md`'s pilot (`diff_auto_status.py`) fed oracle
*answers* to `0030FED0` (auto-status rebuild, 1787 B): the validity
dispatcher, the equipment-kind gate and the licence gate were all scripted
returns. This experiment re-runs the subject with the whole gate/classifier
chain executing from shipped bytes, so *which* equipment types and licence
rows contribute status bits is measured, not asserted. The heavier
behavioural callees remain entry-stubbed with their arguments captured —
the same disclosed boundary the pilot drew, minus the gates.

| VA | role | execution |
|---|---|---|
| `0030FED0` | auto-status rebuild subject | **real** |
| `0020E600` | authored-row resolver | **real** |
| `00322C50` | validity dispatcher (arm 6 = equipment id range) | **real** |
| `0031E9A0` | equipment gate (class → {0,1,2,3}) | **real** |
| `0031E9F0` | equipment classifier (row+9 → class) | **real** |
| `00323890` | licence gate (class → {0,1,2,3,−1}) | **real** |
| `003241D0` | licence classifier (byte → class 0x15–0x1E) | **real** |
| `00808C40` | stack-cookie check tail | **real** |
| `0031B860` | FIND: record → battle unit | stubbed, returns planted unit/0 |
| `0030E130` | APPLY: status write (mode 3 add / 1 remove) | stubbed, bit+mode captured |
| `0030E360` | CASCADE: unit-mask status write (mode 5) | stubbed, args captured (body executed in EXP-086) |
| `002FEF30` | NOTIFY: once per run | stubbed |
| `0030E060` | TAIL: final recompute | stubbed, flags captured |

Trace: `F` find, `V<arm>:<id>=<r>` validity, `E<t9>=<g>` equipment gate,
`L<b5>=<g>` licence gate, `A<bit>+<mode>` apply, `C<bit>:<a5>:<flags>:<a7>`
cascade, `N` notify, `T<flags>` tail. Observables also include hp `+0x48`,
mp `+0x4C`, w6 `+0x06`, the exchanged 5-byte block `rec+0x40..44` /
`spawn+0x78..7C`, and prior `+0x78[16]`.

## Executed bodies

8 real bodies, spans + sha256 in `bodies.json` (jump-table arms are inside
the spans — the walker seeds dispatch-table targets):

| VA | span | role |
|---|---|---|
| `0030FED0` | 1787 B | subject |
| `0020E600` | 10 B | resolver |
| `00322C50` | 1025 B | validity dispatcher (32 arms + shared tail) |
| `0031E9A0` | 68 B | equipment gate |
| `0031E9F0` | 93 B | equipment classifier |
| `00323890` | 83 B | licence gate |
| `003241D0` | 100 B | licence classifier |
| `00808C40` | 34 B | cookie check |

## Fixture surface

- `BASE_AT = [0x1F83530]` → `IMG32` arena; table slots `0x2EBF130`
  (definition), `0x2EBF0F8` (equipment), `0x2EBF038` (licence) each hold a
  header `{pad, count@+4, stride u16@+8, rows@+0xC}` resolved by
  `0020E600`.
- Definition rows at `rows + idx*0x40`; acc masks at `row+0x50` (bits
  0–31) and `row+0x54` (bits 32–63).
- Equipment rows at `rows + (id−0x1000)*0x20`; classifier byte `row+9`,
  status bit index `row+0x1A`.
- Licence rows at `rows + id*0x20`; kind byte `row+5`, eight grant u16s at
  `row+8..+0x16`.
- Owned-licence bitmap `rec+0x194[46]` (bit `id%8` of byte `id/8`);
  equipment ids u16 `rec+0x50+2k` for k<5; kind `rec+5`; prior mask
  `rec+0x78[16]` (note `rec+0x7C` is also the deny-gate byte — it sits
  *inside* the prior block).
- Unit: `FIND` → planted `UNIT`; mask `unit+0xE80[16]` feeds the kind-1
  accumulate; cascade source `unit+0xE90` dword; spawn pointer
  `unit+0x6A0` → flag `spawn+0` bit `0x80` selects copy direction of the
  `+0x78` 5-byte block.

## Findings (native-verified)

1. **Equipment validity is arm 6 of `00322C50`**: `id ∈ [0x1000,
   0x1000 + [tab+4])` over the table at `[0x2EBF0F8]`, with the shared
   tail doing a signed `jl` lower bound and `jg` upper bound (`m-val-*`
   mutants all killed; `m-val-jl` diverges on all 40 cases).
2. **Only equipment gate 3 contributes.** The classifier maps `row+9 ≤
   0x1A` through a byte table + jump table to classes 1–9; the gate maps
   class ≤0→0, 1–5→1, 6→2, 7–9→3, and the subject bits `acc[row+0x1A]`
   only when the gate answers **3** (`eq-gate*`/`eq-cls5` cases;
   `m-eq-cmp3` flips the compare to 2 and gate-2 rows start
   contributing). Status byte `0xFF` is a no-op sentinel
   (`eq-ff-sentinel`).
3. **The licence gate receives the row's `+5` byte, not the row pointer
   or the licence id** — `L` tokens for three different owned ids print
   the same planted byte (`lic-multi`). `003241D0` classifies
   `(b−1) ≤ 0x1D` to classes `0x15–0x1E`; `00323890` maps `class−0x15 ≤
   9` to gates {0,1,2,3}, else −1. **Only gate 2 contributes** (classes
   0x1A–0x1C, i.e. `row+5` bytes 15–18 in the measured table):
   `m-lic-cmp2` promotes gate-1 rows.
4. **The licence walk is `id = 0..360` inclusive over the owned bitmap**
   — id 361 is never probed (`lic-id-361-unseen`), unowned ids produce no
   `L` call at all, and an absent licence table still calls the gate once
   per owned id with byte 0 → −1 (`lic-null-table`).
5. **Kind byte `rec+5` selects the halves**: kind 0 takes the
   definition-row mask path (`def-*`); kind 1 runs the unit-mask
   accumulate + cascade + spawn exchange (`k1-*`). `m-kind1` flipping the
   skip diverges on 33 cases. Both kinds run the equipment loop and
   licence walk — they are not kind-gated.
6. **The diff is acc vs `prior[16]` at `rec+0x78`**: adds call APPLY
   mode 3, removals mode 1 (`diff-add-rem`, `diff-all-rem`). The subject
   itself does not write `+0x78` back (`der` observable stays the planted
   prior).
7. **Spawn exchange is 5 bytes, direction selected by `spawn+0 & 0x80`**:
   set → `spawn+0x78..7C → rec+0x40..44`, clear → the reverse
   (`k1-spawn-in`/`k1-spawn-out`); no spawn pointer → no copy
   (`k1-no-spawn`).
8. **Clamps:** hp capped at `maxhp` (`pres64|pres3c` bit 28 doubles the
   cap, bit 16 freezes it entirely); mp and the `+0x06` word are capped at
   `sx16(rec+0x28)` (the word cap additionally multiplies by `rec+0x37`,
   with `0x37==0` behaving as ×1) — and either deny byte (`rec+0x6C` or
   `rec+0x7C` bit 7) forces both caps to 0.
9. **Flags `| 0x202` propagate** into APPLY/CASCADE/TAIL argument words
   (`flags-flow` with `0xFFFF` → `C…:ffff:5`, `Tffff`).
10. **`rcx=0` record is survivable on this fixture** — all reads hit the
    mapped zero page: five `V6:0=0`, no applies, `N`, `T202`. This says
    the code path contains no null check before the equipment loop; it
    does **not** prove the shipped context ever passes null.

## Mutants (13/13 killed)

| mutant | site | semantic |
|---|---|---|
| `m-val-base` | `0x322D0A` | arm-6 base `0x1000`→`0x1001`: id `0x1000` invalid |
| `m-val-hi` | `0x322D16` | arm-6 `lea +0x1000`→`+0x0FFF`: last id excluded |
| `m-val-jl` | `0x323030` | tail `jl`→`jge`: every id fails lower bound |
| `m-val-jg` | `0x32303B` | tail `jg`→`jle`: every id fails upper bound |
| `m-eq-bnd` | `0x31E9F6` | eq class bound `0x1A`→`0x10` |
| `m-eq-cmp5` | `0x31E9AF` | gate `cmp 5`→`4`: class 5 falls through |
| `m-eq-sub7` | `0x31E9B9` | gate `add −7`→`−8`: class-7 window shifts |
| `m-lic-bnd` | `0x3241D4` | lic class bound `0x1D`→`0x0E` |
| `m-lic-dec` | `0x3241D0` | `dec ecx`→`inc ecx`: class lookup shifts one |
| `m-lic-add` | `0x32389B` | gate `add −0x15`→`−0x14`: window shifts |
| `m-lic-cmp2` | `0x31019D` | subject lic `cmp 2`→`1`: gate-1 rows contribute |
| `m-eq-cmp3` | `0x3100EC` | subject eq `cmp 3`→`2`: gate-2 rows contribute |
| `m-kind1` | `0x31001F` | kind≠1 skip→`je`: kind-0 runs unit-mask loop |

## Not exercised (disclosed, not claimed)

- FIND/APPLY/CASCADE/NOTIFY/TAIL bodies — stubbed at entry with args
  captured (CASCADE's body was executed in EXP-086; the rest remain
  oracles).
- The callers of `0030FED0`, the authored table file loaders, and the
  unit/spawn record producers — all inputs arrive as planted fixtures.
- No live process; table memory is a synthetic `IMG32` arena outside the
  image extent (`BASE_AT` is pointed at it).

## Harness notes

- The pilot's oracle answers implied licence ids 15–18 → gate 2; running
  the real chain confirmed the gate input is the row `+5` byte — the
  subject reads it, `00323890` never touches the row itself.
- Win64 stack args are read at callee `rsp+0x28/0x30/0x38` (caller's
  `+0x20/0x28/0x30`) — the first draft read one slot too low and saw
  mode 0.
- `rec+0x7C` is both the mp/w6 deny byte and byte 4 of the `prior` block —
  a real layout overlap, modelled as such (it produces eight removals in
  `clamp-mp-deny7c`).
- `IMG32` must live outside the `0x120000–0x2F800000` mapped image; it
  sits at `0x50000000`.
- Body-span walker seeds jump-table targets: `0x322C50` measures 1025 B
  through the 32-arm dispatch and shared tail; `0031E9A0`/`0031E9F0` are
  disjoint (68/93 B) — `call` targets are not continuations.
