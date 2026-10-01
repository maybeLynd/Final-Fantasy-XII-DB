---
experiment: EXP-150
title: Battle-unit construction — installer 0023A570 executed end-to-end
  with the REAL callee layer (reset 00236A60 and helpers, rekey 00322050,
  resolver 0020E600, spawn fetch 00236100, blob walker 002B58B0, tracked
  update 00328FF0, validator 00322C50, engaged arms 002FED60/002FEDC0),
  closing EXP-075's nine-stub gap
contract: ../04-Actor-Entity/Unit-Definition/CONTRACT-battle-unit-construction.md
method: B
live_game: false
tool: evidence/battle-unit-construct-exec/check.py
---
# EXP-150 — battle-unit construction: installer + real callees

> **SECTION-01 correction/consumption (2026-09-22):** the 39 retained cases include
> three private guard mutants; this full Unicorn campaign was not rerun. New original-CPU
> controls reject the former bit42, wrong tracked-base, and heavy pulse-writer claims.
> Raw case IDs are preserved: `in-member` is class1/enemy and `in-foe` is class0/party.
> Original producer code/results remain unchanged; its wrong-address observation and
> nondiscriminating bit assertion are explicitly pending repair/rerun, not accepted
> supports. See [review](evidence/continuation-section01-result-install/REVIEW.md).

**Contract:** `../04-Actor-Entity/Unit-Definition/CONTRACT-battle-unit-construction.md`
**Scope:** the full installer `0023A570` (1808 bytes) plus its real callee
layer — selected formerly stubbed callees executed as shipped bytes, with remaining boundaries listed below.
**Method:** NATIVE-REPLAY — shipped bytes under Unicorn; fixtures are
disclosed MODEL-PROVEN plantings of BSS/descriptor state. No EXE bytes
modified except the three disclosed per-case guard mutants (private
copies, sensitivity controls).
**Harness:** `evidence/battle-unit-construct-exec/check.py`
**Result:** `evidence/battle-unit-construct-exec/result.json` —
39/39 cases, 0 faults, stable across 3 processes.

Scripted boundaries (entry-intercepted, args + stack dwords recorded,
disclosed): `00377C20` (can-die, via `00313F60`), `003271D0` (class
getter behind `00304630`), `00308010` (engaged predicate inside
`00237040`), `003220E0` (rekey inner resolver — deep global deps),
`003105D0` (reset's bit4 helper), `0023AC80` (spawn-record init —
self-modifying-byte region, not executable standalone).
`00861EC0` (memset) is implemented in the hook.

Everything else on the install path runs **real**: `00236A60` (reset),
`00316D30`, `00320450`, `003839F0`, `003839C0`, `003176C0`,
`00322050`, `0020E600`, `00236100`, `002B58B0`, `00328FF0`,
`00254A40`, `00322C50` (+cls-2 arm through the real jump table),
`00237040`, `002FED60`, `002FEDC0`, `002ECF10`, `002FEAB0`,
`00303EC0`, `0030D9A0`, `00304630`.

## 00236A60 — reset `(rcx=unit)` — now executed, not stubbed

Driven against all-`0xA5` dirty memory (`rs-plain`/`rs-b10`/`rs-mask`).
Executed field effects:

- `b[unit]&0x10` → `3105D0` (scripted).
- `w[+0x695]=0xFFFF`, `b[+0x694]=0xFF`.
- **Combined flag mask (observed on all-ones input):**
  `q[0] &= 0xFFEF7FB9FFE7B0E1` — i.e. `q &= 0xFFFF7FFDFFE7FFFD` then
  `d[0] &= 0xFFFFB0E3` plus additional `+4`-dword clears; `d[4]`
  alone resolves to `0xFFEF7FB9`.
- Zeroed: `+0x698`, `+0xE60`, `+0xE68`, `+0x6A0`, `+0x2C`, `+0x24`,
  `+0xEA8`, `+0xEA4`, `+0xE54`, `+0xDD0`, `+0x5C`, `+0x70`, `+0x710`,
  `+0x760`, `+0xB90`, `+0x100`, `+0x680`.
- Sentinels: `d[+0x74]=-1`, `w[+0xDC8]=0xFFFF`, `w[+0x55]=0xFFFF`,
  `w[+0x52]=0`, `b[+0x54]=0xFF`, `w[+0x714]=0xFFFF`,
  `w[+0x758]=0xFFFF`, `d[+0x774]=-1`.
- `316D30`: `b[+0xBC0] |= 1`, `memset(+0xBC0, 0, 0x208)` preserving
  bit0 (`bc0` ends `0x01`), `w[+0xBC1]=0`.
- `320450`: reads `q[+0x698]` object float then clears `+0x70`.
- `861EC0(+0x80, 0, 0x610)` — memset hook; call site recorded.
- `3839F0(+0x200)`: 128×`0xFF` from `+0x210` (`b210`/`b28f` observed).
- `3839C0(+0x200)`: `w[+0x20C]=w[+0x20E]=0xFFFF`.
- `3176C0` (tail jmp): clears 32 dwords `+0xDD4..+0xE53`.

## Installer `0023A570` — executed semantics, corrections vs EXP-075

**Confirmed by execution:**

- Entry reads old kind: `ebx = b[unit]&4 ? w[q[unit+0x698]+4] : 0xFFFF`.
- Master enable gate `d[02089300]` aborts after reset (`in-enable-off`
  runs reset then returns 0).
- Member path requires `q[0]` bit26 (`in-nobit26` rejects).
- Base/level guards are **unsigned `ja` on `count-1`** — count 0
  underflows to `0xFFFFFFFF` and admits every index, null descriptors
  (`ecx=0→-1`) do the same; row pointer stores 0 only when the desc
  cell itself is null (`in-base/level-null`, `e70/e78==0`).
- Order guard is **signed `jg`** on `w[desc+0]`-indexed count — null
  order descriptor rejects where base/level pass (`in-order-null`,
  `in-order-oob`).
- `sel` byte0 = table index, byte1 = mode; `esi==1` enemy, `esi==0`
  party, otherwise **bit26** cleared + ret 0.
- `322C50(cls=2, idx, 1)` foe validation through the real jump table
  (`in-foe-badcls` idx 9 > count-1 7 rejects).

**Corrections the stubs hid:**

- **Outside the selected-teardown bypass, nonzero `sel` byte1 selects rekey
  `00322050` before class dispatch** — including the tested `esi>=2` failure exit (`in-mode2` rekeys then returns 0). It clears
  `d[+0xEA4]`, `b[+0xEA8]`, stores `3220E0(q[+0x10])` → `d[+8]`
  (inner resolver scripted).
- **The whole spawn-setup block** — `0023AC80` init, the
  `w[def+0x32/34/36]!=0xFFFF → b[spawn+0x14]` flag bits, and the
  tracked-count update — is inside the `b[spawn]&5==0` arm
  (`jne 0x23a84a` skips all of it). Already-initialized spawn records
  never recount (`in-tracked`/`in-tracked-cap` needed a fresh spawn).
- **Tracked counter** (fresh spawn, `b[def+2]!=0xFF`): row =
  `(cls<<6)+slot` words at `02089340+0x4014`; `b[spawn+0x12]=old`;
  new = `old+1` unless `old >= 254A40()` cap (`0x34`), then wraps to 1
  (executed: `0x10→0x11`, `0x34→1`).
- **`00328FF0` writes only when `(edx!=0 or r8d<0) and ecx<2`**
  (`00328FFE`–`00329011`, per the EXP-150 owner consumption) — i.e. at
  this call site when `b[def+3]&3` (kind) is nonzero, since the movzx'd
  `b[unit+0xEA9]` arg can never be negative and `i` is fixed 0.
  `in-member` (kind 0) executes the call
  real and stores nothing; `in-bit43` (kind 1) stores
  `d[02EC1380+row*24]=r8d`, `+4=edx`. **The producer's
  `trktab` observation reads `02E81380`, not the real table, and its case checker does
  not assert those observations. The write/address claim is established instead by
  SECTION-01's independent original-body controls.**
- **Engaged dispatch arms** are `002FED60`/`002FEDC0`, both real:
  engaged sets `d[unit] |= 0x800000`; not-engaged clears bit23 and
  `d[+4] &= 0xFFFEF9FF`. Both zero `d[+0xDCC]` and store
  `q[+0x6E8] = 0x1EEC3C0` when `b[q[+0x698]+5]==0` else `0x1EEC410`,
  then tail `002ECF10(q[+0x10], engaged?1:0, 0)` — early-ret on the
  null `+0xC0` chain in the fixture (real).
- `002B58B0` — the former "unread resolver" — is a **string/blob
  walker**: null → 0; `b[rcx]!=0 || b[rcx+1]!=0` → `rcx`; else
  returns `rcx+2` advanced through `edx` zero-terminated strings.
- `002FEAB0` is the original ten-byte pulse reset: `xor eax,eax;
  mov qword [rcx+0xEAC],rax; ret`. It clears `+0xEAC/+0xEB0`, not
  `+0x2E0..0x2EC`. The previous heavy-float interpretation is withdrawn;
  the retained `in-member` assertion already checks `qeac == 0`.
- Class1/enemy path `f[+0x6C] = float(b[classRecord+0x27])`; the ×1.5
  scale is class0/party only (`f6c = 45*1.5` in the locally named `in-foe`).
- Exact `0020E600` token order observed (member path, 14 calls):
  `def, def, memb, memb, def, def, pool-elem, def, blob-elem,
  order-elem, base, base, level, level` — each desc resolve is a
  gate+recompute pair.

## Case inventory (39)

- `rs-plain`/`rs-b10`/`rs-mask` — reset alone on dirty memory:
  every listed field + masks + helper trace + both memsets.
- `in-member` — full member path, field list + call/trace fidelity.
- Guard matrix — `in-base-eq/-zero/-ffff-bad/-ffff-ok/-null`,
  `in-level-eq/-zero/-ffff-bad/-ffff-ok/-null`, `in-both-bad`,
  `in-order-null/-oob`, `in-def-oob`, `in-mem-oob`, `in-enable-off`.
- Path coverage — `in-nobit26`, `in-mode2`, `in-spawn-bad/-init`,
  `in-spawnflags`, `in-tracked/-cap`, `in-bit43/-b`, `in-ko/-cantdie`,
  `in-engaged`, `in-foe`, `in-foe-badcls`, `in-foe-rekey`,
  `in-select-eq`.
- Mutants — `mu-base-ja-jb`, `mu-level-ja-jb`, `mu-order-jg-jle`
  (patched private copies flip the boundary guard to acceptance —
  the harness is sensitive to shipped control flow).

## Boundaries / caveats

- Fixture records (unit, descs, spawn table, member/foe rows) are
  synthetic plantings — MODEL-PROVEN inputs driving NATIVE-REPLAY
  execution; no claim of live-game reachability.
- `003220E0`, `00313F60→77C20`, `00308010`, `003271D0`, `003105D0`,
  `0023AC80` are scripted boundaries — their internals are not
  covered here.
- The reset mask constant `0xFFEF7FB9FFE7B0E1` is the observed
  conjunction of all flag ops on all-ones input — finer per-instruction
  attribution is in the harness trace.

## Reproduce

```powershell
python "Database/FFXII TZA/_experiments/evidence/battle-unit-construct-exec/check.py"
```

Requires the shipping EXE at its recorded path (SHA-256 verified
in-harness: `73461D08…721F8`).

## Producer-check limitations retained after SECTION-01

The `BIT42` assertions do not test the shipped clear mask, and the invalid-class
fixture starts with that bit zero. Both `0023A633` and common terminal `0023AC4B`
clear bit26. New controls seed bits26/42 together and discriminate the result.
The `trktab` capture uses the wrong address and is not asserted by the producer.
These issues do not discard correctly supported reset/guard/engagement observations,
but 39 passing case labels do not certify these two former prose claims.
