---
experiment: EXP-151
title: Rekey inner resolver — 00322050 -> 003220E0 executed with the
  REAL callee layer (id compose 003589B0, generation bump 002659D0,
  slot-occupant search 00327150, id->object resolve 003588B0 + leaves
  00263FF0/00236850/00236820/00263E30), closing EXP-150's last
  scripted boundary on the rekey path
contract: ../04-Actor-Entity/Unit-Definition/CONTRACT-battle-unit-construction.md
method: B
live_game: false
tool: evidence/rekey-inner-exec/check.py
---
# EXP-151 — rekey `00322050` -> inner `003220E0`, real callees

**Contract:** `../04-Actor-Entity/Unit-Definition/CONTRACT-battle-unit-construction.md`
**Scope:** `00322050` (rekey wrapper, 0x2C) and `003220E0` (inner
resolver, 0xAF) executed as shipped bytes, with every callee real
except the disclosed notify boundary.
**Method:** NATIVE-REPLAY — shipped bytes under Unicorn; fixtures are
disclosed MODEL-PROVEN plantings of `.data` globals (`02EBF190`,
`02089340`, `02098E10`, `0208E688`/`0208E6A0`) and heap blocks. No EXE
bytes modified.
**Harness:** `evidence/rekey-inner-exec/check.py`
**Result:** `evidence/rekey-inner-exec/result.json` — 24/24 cases,
stable across 3 processes.

Scripted boundary (entry-intercepted, args recorded, disclosed):
`00326500` — the notification dispatcher at the tail (calls
`00311E20`/`00326620`/`0030D9A0`/`00377C70`, a separate
package-sized surface).

Everything else runs **real**: `00322050`, `003220E0`, `003589B0`,
`002659D0`, `00327150`, `003588B0`, `00263FF0`, `00236850`,
`00236820`, `00263E30`.

## Executed semantics

### `00322050` rekey `(rcx=unit)`

`d[unit+0xEA4]=0`; `b[unit+0xEA8]=0`; `d[unit+8] = 3220E0(q[unit+0x10])`.
Executed end-to-end (`50-basic`/`50-full`): the clears land **before**
the inner call — `50-null10` (null `q[+0x10]`) proves ordering: both
clears observed, then the inner faults.

### `003220E0` inner `(rcx=obj)` — the generation-bump rekey

1. `esi = obj ? 3589B0(obj) : 0` — the OLD composite id.
   `3589B0` = `((w[+0x16]&0x7FF)<<4 | (b[+0x15]&0xF))<<16 | w[0]`
   — i.e. `gen<<20 | cls<<16 | idx`.
2. `2659D0(rbx)` — `w[+0x16] = (w[+0x16]+1)&0x7FF`, `cmove` to 1 when
   the wrap yields 0. **No null guard** — `3220E0(0)` faults on the
   `w[0x16]` read (`e0-null`, `50-null10`; fault addr `0x16`,
   PC `002659D0`).
3. `ebx = rbx ? 3589B0(rbx) : 0` — the NEW id (bumped generation).
4. `327150()` — slot-occupant search: `idx = b[q[02EBF190]+0x5AA4]`,
   reject `idx > 0x27`; `rdi = glob+8+idx*0x1C8`; scan the object
   array `q[0208E688] + i*0xF50` (`i < d[0208E6A0]` via `236820`
   bounds `0<=i<=count-1`); first row whose `q[row+0x698] == rdi`
   wins, else 0. **No glob guard** — null `q[02EBF190]` faults on
   `b[0x5AA4]` (`e0-glob-null`, PC `0032715D`).
5. `edi = occ ? d[occ+8] : 0`; **`esi != edi` → return `ebx`** — the
   slot doesn't hold our old id, nothing else runs
   (`e0-basic`, `e0-slot-oob`, `e0-occ-mismatch`, `mut-occ-id`).
6. On match, the store+notify **always** run — `b[02089340]&0x10`
   gates only the resolve, not the store:
   - flag clear → `eax=0xFF` directly (`e0-occ-hit-flagclear`
     executed: `d[glob+0x5AA4]=0xFF`, notify fired, no resolve).
   - flag set → `3588B0(ebx)` resolve → `q[r+0x30]` (263E30) →
     `q[r2+0x698]` → `b[r3+4]`; any null stage → `0xFF`.
7. `d[q[02EBF190]+0x5AA4] = eax` — **DWORD store**: the index byte
   plus three zeroed bytes above it.
8. `326500()` notify (scripted).
9. Return `ebx` — always the new id.

### `003588B0` resolve `(ecx=id)` — executed

`id==0`→0. Decode `gen=(id>>20)&0x7FF`, `cls=(id>>16)&0xF`,
`idx=id&0xFFFF`. `cls>=5`→0 (`e0-occ-hit-clsge5`). Else
`row = 02098E10 + cls*0x288` (`263FF0`); `arr = q[row+8]`; guards in
order: `arr!=0`, `q[row]!=0`, `idx < d[row+0x20]`, `b[row+0x10]&1`,
`idx < d[arr]`; then `o = q[arr+idx*8+8]`; return `o` iff
`w[o+0x16]==gen` else 0. Every guard and the generation check were
exercised to both outcomes (`e0-res-*`, `mut-gen-off`).

## Case inventory (24)

- Fault proofs — `e0-null` (null arg → `2659D0` `w[0x16]` fault),
  `50-null10` (wrapper clears `+0xEA4`/`+0xEA8` then the same fault),
  `e0-glob-null` (null `q[02EBF190]` → `327150` `b[0x5AA4]` fault).
- Basic path — `e0-basic` (ret = bumped id `0x1110002`),
  `e0-genwrap` (`0x7FF`→gen 1), `50-basic` (wrapper stores
  `d[unit+8]`).
- Occupant search — `e0-slot-oob` (`idx 0x28 > 0x27` rejects even
  with a planted match), `e0-slot-edge` (`idx 0x27` admits),
  `e0-occ-mismatch`/`mut-occ-id` (occupant `d[+8]` != old id →
  early ret).
- Store block — `e0-occ-hit-flagclear` (flag 0 → `0xFF` + notify,
  resolve skipped), `e0-occ-hit-clsge5` (cls 6 → `0xFF`),
  `e0-res-arrnull`/`-rownull`/`-oob`/`-flag0`/`-arrcnt`/`-elemnull`/
  `-genmm` (each `3588B0` guard → `0xFF`), `e0-res-q30null`/
  `-q698null` (downstream nulls → `0xFF`), `e0-full`/`50-full`
  (resolved `b[r3+4]=0x2A` stored, notify recorded).

## Boundaries / caveats

- Fixture `.data` plantings (context table, class table, object
  array, flag byte) are MODEL-PROVEN inputs driving NATIVE-REPLAY;
  no claim of live-game reachability.
- `00326500` notify internals not covered (scripted boundary).
- `326500`'s `d[glob+0x5AA4]` dword store also clears bytes
  `+0x5AA5..+0x5AA7` — executed fact, noted for downstream readers
  of that qword region.

## Reproduce

```powershell
python "Database/FFXII TZA/_experiments/evidence/rekey-inner-exec/check.py"
```

Requires the shipping EXE at its recorded path (SHA-256 verified
in-harness: `73461D08…721F8`).
