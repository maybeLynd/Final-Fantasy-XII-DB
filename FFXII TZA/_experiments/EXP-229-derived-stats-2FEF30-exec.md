# EXP-229 — derived-stat accumulator `2FEF30` real (+ `2F8E50`/`2F9180` scale leaves)

**Status:** complete — **542/542 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 `85e8d6f9` prefix; 542
cases), fault census unchanged at 20** (the same intentional-null
fixtures; one relocated to its shipped-order address, see below).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..228; no new cases — the `fef30` scripted boundary now
executes the shipped body; asserts retargeted to real stats surface)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Bodies promoted real this round

`002FEF30` (`fef30`, **×195 executed / ×196 call sites** — the
`30FED0` tail callsite and every other caller now run shipped bytes;
the 196th entry, `ac80-member-nulld`, faults mid-body at `0x2FF158` on
its intentional null `MEMD` desc — the tag records on clean exit).
~0x8E0 insns `0x2FEF30..0x2FF810`. This is the **derived-stat rebuild**:
the `rec+0x24..0x47` output block every reader of `d[+0x24]`/`w[+0x28]`/
`b[+0x2A..0x2E]`/`d[+0x38]`/`d[+0x3C]`/`b[+0x40..0x44]` consumes.

| body | semantics | hits |
|------|-----------|------|
| `002FEF30` (`l2fef30`) | **Head/defaults:** `rdx==0` → `31B860(rec)` owner resolve, saves `d[rec+0x3C]` into `rsp+0x68`, sets `rsp+0x64`=1; `r8==0` → source slot array `rbx=rec+0x50`; `rsi==0` → output block `rsi=rec+0x24`; then **zeroes `rec+0x24..0x47`** (0x24 bytes). `rsp+0x3C`=`b[rec+5]` mode; `rsp+0x5C`=1 iff `b[rec+5]==0 && (b[rec+4]-0x1B)<=0xC` (foe-class HP-cap selector). | ×195 |
| | **Foe arm** (`b[rec+5]==0`): `foerow = 20E600(d[FOED+0xC]) + w[FOED+8]*b[rec+4]` → `rsp+0x40` HP acc = `2F8E50(d[rec+8], b[row+0x18], b[row+0x19])`; `rsp+0x28` = `2F9180(w[rec+0xC], b[row+0x1D])` (x*y/100 magic-div); `d[rsi+0x14] |= d[row+0x4C]`, `d[rsi+0x18] |= d[row+0x48]`, `rsp+0x50`=`b[row+0x2A]`; `cvttss2si` of `f[rec+0x10/0x14/0x18/0x1C]` seed the stat accs. | ×187 |
| | **Member arm** (`b[rec+5]==1`): chained growth descs — `r13` = `MEMD` row idx `b[rec+4]`; `rbp` = `q[02EBF148]` row idx `w[r13+0x22]`; `rbx` = `q[02EBF140]` row idx `w[r13+0x24]`; `r11` = `q[02EBF150]` row idx `w[r13+0]` — each `20E600(d[desc+0xC]) + w[desc+8]*idx`. **Level delta** `ecx = b[rec+0x1C2] - b[rec+0x88]` scales the growth fields: `d[rbx+0x20]*delta + d[rbp+0x20]` → HP acc; `w[rbx+0x24]*delta + w[rbp+0x24]` → MP; `b[+0x27..0x2B]*delta + b[rbp+..]` + `w[rec+0x8/0xA/0xC/0xE/0x16]` → STR/MAG/VIT/SPD; `b[rbx+0x26]*delta + b[rbp+0x26] + w[rec+8]` → r12. | ×8 (member cases) |
| | **Equip loop** ×5 over `w[rbx+2i]` (the `r8` source, default `rec+0x50`): `322C50(6,id)` member-range gate → `memt` row → `31E9A0(row)` class dispatch (class 1/2/3 each OR/add a different `b[row+0x18/0x19/0x1A]` accumulator) → `sub = 20E600(d[row+0x28])` item-bonus record: `w[sub]`→HP acc, `w[sub+2]`→MP, `b[sub+4/5]`→r12/r13, `b[sub+6]`→`rsp+0x2C`, `b[sub+7]`→`rsp+0x30`, `d[sub+0xC]`→`or [rsi+0x14]`, `d[sub+8]`→`or [rsi+0x18]`, `b[sub+0x10..0x14]`→`or b[rsi+0x1C..0x20]`. | per-slot |
| | **Status-bit fold:** three loops over shipped `.rdata` index tables `0xD10290`/`0xD102A0`/`0xD102B0` (16/16/12 entries) — `b[table+i]` = `q[02EBF040]` row idx; bit set in `rec+0x68`/`rec+0x78` banks → `row = 20E600(d[sttd+0xC]) + idx*w[sttd+8]` → `w[row+4]` folds into r12/r13/r14 accs. Null `q[02EBF040]` + a set bit → `w[4]` fault (fail-closed). | per-set-bit |
| | **Tail clamps → writes `rsi` block:** `d[rsi]` = HP acc floored at 1, capped `0x270F` (or `0x3B9ACA00` when `rsp+0xD8` flag; second pass `min(0x7FFF)` when `rsp+0x5C`); `w[rsi+4]` MP `[0,0x3E7]`; `b[rsi+6..9]` STR/MAG/VIT/SPD `[0,0x63]`; `b[rsi+0xA]` ≤3. | per-call |
| `002F8E50` (`l2f8e50`) | three-factor scale leaf: `((r8+1)*ecx*edx)/100` via `0x51EB851F` magic-divide. | ×187 |
| `002F9180` (`l2f9180`) | `ecx*edx/100` magic-divide leaf (same constant). | ×187 |

## Corrections of record

- **`ac80-member-nulld` fault relocated `0x23ADA8` → `0x2FF158`.** Real
  `2FEF30` runs inside `30C470`→`30FED0`, which precede `23AC80`'s own
  member-arm reads — the shipped order faults the null `MEMD` row at
  `w[r13+0x22]` (`0x2FF158`) first. The prior expectation was stub-era
  ordering (the stubbed `fef30` could not fault).
- **`31B860` pins +1** on `a630r9-off` (1→2), `a630r9-nomatch` (2→3),
  `c650-one` (2→3), `c650-multi` (4→5), `g3910-e5` (2→3): `2FEF30`
  resolves the owner at its head (`0x2FEF73`) on every `rdx==0` call —
  the stub hid it. `a630r9-nomatch` `e6820` 4→6 absorbs the extra
  OBJARR element scan (`objcount=2`).
- **`d[rec+0x3C]` is a rebuilt output field**, not a caller input:
  `a630r9-gate3f`/`a630r9-b2`/`a630r9-rec3c` planted `rec_d={0x3C:1}`
  which the `rec+0x24..0x47` memset defeats. The shipped source is
  `d[foerow+0x48]` (foe arm `or [rsi+0x18]`) — fixtures now plant
  `foe={"w":{0x48:1}}` + `rec_b={4:2}` so `b[rec+4]` resolves the
  planted row. `3243F0`'s `d[q[obj+0x698]+0x64] | d[+0x3C]` → `313F60`
  → `300E40` dispatch chain verified through the real rebuild.
- **`ac80-foe*` ×12 gain one `30E360` call each** (`e360n` key):
  `300530`'s reconcile arm (`0x3007CF`, mode 3, `r9d=-1`) dispatches
  when `d[rec+0x48]` ≤ the saved compare value — with the real
  `d[rec+0x24]` (HP floor 1) in place the stat-decrease notify is the
  shipped path. `f690` still correctly absent (zero dirty mask).

## New fixtures

Four `mkdesc` defaults, all zeroed rows (contributions = 0), each
case-overridable (`"x": None` selects the null-desc fault arm):

- `q[02EBF148]` `d148` — elemb `0x82000`, stride `0x40`, count `0x40`
- `q[02EBF140]` `d140` — elemb `0x83000`, stride `0x40`, count `0x40`
- `q[02EBF150]` `d150` — elemb `0x84000`, stride `0x40`, count `0x40`
- `q[02EBF040]` `sttd` — elemb `0x80000`, stride `0x20`, count `0x100`
  (covers every `b[0xD1029x]` index byte)

## Boundaries (unchanged disclosures)

`0030E130` (`e130`) stays scripted and **fired 0 times** — no fixture
produces a status-bitmap diff, so its add/remove dispatch arms are
disclosed empty-operand. `30C970`, `319420`, `319140`, `8632B0`,
`2EB0D0`, `46AB10`, `426130`/`427320` remain scripted.
`live_game: false` — synthetic fixtures do not establish
initialized-gameplay reachability.

## Regression triage

521/542 first run → 539/542 → **542/542**. 21 failures, all triaged to
shipped-correct causes: 12 e360 reconcile dispatches (now pinned
per-case), 5 `b860`/`e6820` count pins, 3 gate fixtures rerouted
through the real `d[foerow+0x48]` source, 1 fault-address relocation.
No assertion weakened; the `f690`-absence and `c530`/`h0bc0`/`h0ce0`
checks are unchanged.
