# S-14 runtime: per-invariant stub exposure for EXP-150 (OPUS, 2026-09-25)

**Row:** S-14 battle-unit construction. AUDIT-SEM re-scored the runtime cell **MIXED** on 2026-09-25, with the
qualifier *"no per-invariant stub-exposure analysis yet, the analysis that lifted S-01 to MET and held S-02 at
MIXED"*. This note supplies that analysis. It scores nothing.

The contract is `04-Actor-Entity/Unit-Definition/CONTRACT-battle-unit-construction.md`, with invariants I1–I8.
The executing record is **EXP-150** (installer `0023A570`, 39/39, stable ×3, NATIVE-REPLAY). It scripts six
callees:

| # | callee | role |
|---|---|---|
| 1 | `003220E0` | rekey inner resolver |
| 2 | `0023AC80` | spawn-record init |
| 3 | `00377C20` | can-die, via `00313F60` |
| 4 | `003105D0` | reset's bit-4 helper |
| 5 | `00308010` | engaged predicate, inside `00237040` |
| 6 | `003271D0` | class getter, behind `00304630` |

`s14-runtime-boundaries-discharged.md` already shows that each of the six runs as shipped bytes in its own record
(EXP-151, 152, 153, 161, 193, 193). This note asks the other question: **for each invariant, can a scripted
callee reach what the invariant claims?**

**The binding-gap cell ("the reset is a stub") is stale.** EXP-150 executes the reset `00236A60` as shipped bytes
(its section "00236A60 — reset — now executed, not stubbed"). Only the reset's optional bit-4 helper `003105D0` is
scripted.

## Method (bounds stated)

The method has three parts:
1. **Instruction order in the installer** (`disasm_fn.py 0x0023A570`), to place every call relative to the
   instructions each invariant is about.
2. **An image-wide direct-reference census** (`data_xref_scan.py` over `Tools/work/graph/functions.tsv`, control
   `02EBF130`) of the invariants' global state, split into writes and `lea`s.
3. **The static callee closure** of each scripted callee (`Tools/work/graph/edges.tsv`, direct calls only), used to
   ask whether any function that writes the state is reachable from a stub.

The closures are coarse (`0023AC80`: 2,181 functions; `003105D0`: 988). A hit only says "statically reachable",
never "executed". The standard caveats stand: indirect calls and pointer-based access are outside the census.

**Scripts** (scratch, reproducible):
- `s14_exposure.py` (closures × referencers);
- `s14_paths.py` (shortest call paths);
- `s14_writes.py` (write / `lea` census).

### Installer call order

| order | call site | callee | scripted callee reached |
|---|---|---|---|
| 1 | `0023A5B0` | reset `00236A60` | `003105D0` when `b[unit]&0x10` |
| 2 | `0023A5CD`–`0023A5E2` | `00303EC0`, `00304630` ×2 (selected-teardown bypass) | `003271D0` |
| 3 | `0023A60A` | rekey `00322050` | `003220E0` |
| — | **`0023A633`** | class ≥ 2: `and [unit], ~bit26`, return 0 | none (no call follows) |
| 4 | `0023A776` | `00236100` (spawn lookup) | — |
| 5 | `0023A7A9` | **spawn init on `spawn+0x80`** | `0023AC80` |
| — | `0023A7AE`–`0023A838` | steal bits (+0x14), counter read-modify-write | none |
| 6 | `0023AA04` | `00328FF0` (tracked-HP registration) | — |
| 7 | `0023AC1C` | `00237040` | `00308010` |
| 8 | `0023AC24` | `002FEAB0` (pulse reset) | — |
| 9 | `0023AC42` | `00313F60` | `00377C20` |
| — | **`0023AC4B`**, `0023AC52`, `0023AC56` | terminal `and ~bit26`, `or 2`; success `or 4` | none (no call follows) |

### Who writes the invariants' state (image-wide)

| state | writers | in a scripted callee's closure? |
|---|---|---|
| master enable `02089300` | `002368D0`, `00236A40` | **no** |
| authored slots `02EBF120`, `130`, `140`, `148`, `150`, `168` | no direct stores; `lea`s only in the loaders `0023A160` / `00236C30` | **no** |
| battle-state block `02EBF190` (class-0 stats base) | `00233C10`, `00238A80` | **no**; every stub-closure access is a read |
| spawn-counter table `02089340+0x4014` | `lea` of the base in `0023A570` and `002376F0`; `lea` of `0208D354` in `00233780` | only by **re-entering the installer**: `0023AC80 → 0031A630 → 00324470 → 00300E40 → 0023A570` |
| tracked-HP table `02EC1380` | `003221B0` (header); `00328FF0` / `0031B690` (via `lea`) | only by the same re-entry, `… → 0023A570 → 00328FF0` |

(The `02089340` dword itself, a flag word, *is* written inside `0023AC80`'s closure, by `00238A60`, `00238AE0`,
`00238B70` and `00300FC0`. No invariant reads that word; I6's counter is at +0x4014.)

## Per invariant

| inv. | claim | can a scripted callee reach it? | owner reading |
|---|---|---|---|
| **I1** | class ≥ 2 clears bit26 and returns 0; the terminal arm clears bit26 then sets bit1; success sets bit2 | **Arm contents:** no. The masks are the last writes and no call follows either site. **Arm selection:** when stats `(+0x64 \| +0x3C) & 0x80000003` is non-zero, the terminal arm is taken iff `00313F60` returns 0. That return comes from scripted `00377C20`. | **contents not reachable; selection exposed at `00377C20`**. EXP-153 runs `00377C20` real (a 4-leaf chain, with the can-die cells `021654C4`/`02ADD100` fixture-planted). Its veto cases (`f690-bit0-candie`) are `0030F690`'s call, not the installer's `00313F60` path. |
| **I2** | reset precedes the master-enable rejection; the flag mask conjunction | **Ordering:** no (`0023A5B0` then `0023A5B5`); no stub closure writes `02089300`. **Mask:** `003105D0` runs inside the reset when bit 4 is set. The measured `0xFFEF7FB9FFE7B0E1` has it bridged. | **ordering not reachable; the mask is exposed to `003105D0` on the bit-4 path only.** The contract already states this bound. `003105D0` is executed in EXP-161. |
| **I3** | rekey before the class dispatch; class 2 can rekey then fail; the wrapper clears `+0xEA4/+0xEA8` and stores the handle at `+8` | **Order and failure:** no. Rekey (`0023A60A`) precedes the `0023A633` arm. **The stored handle's value** is `003220E0`'s return. | **structure not reachable; the handle value is scripted.** `003220E0` is executed in EXP-151. |
| **I4** | class fixes the stats location: class 0 at `q[02EBF190]+8+row*0x1C8`, class 1 at `spawn+0x80`; party has no spawn | No for the location. `02EBF190`'s writers are outside every closure, and `spawn+0x80` is address arithmetic. `0023AC80` initialises the **contents** at `spawn+0x80`. | **location not reachable; class-1 contents come from the scripted initializer** (EXP-152 runs it). |
| **I5** | unsigned count−1 guards; signed `jg` on the `+0x50` join | No. The guard counts are read from the authored slots, and nothing in any closure stores to them. | **not reachable** |
| **I6** | init, steal setup and counting sit inside one `byte[spawn]&5 == 0` gate; count increments or wraps at the cap | **Gate:** tested once (`0023A791`); the block runs straight through with no re-test after `0023AC80`. **Counter:** the read (`0023A80C`) and write (`0023A838`) have only the real `00254A40` between them. `0023AC80` runs before the read. It reaches the table only by re-entering the installer, which changes the start value, not the relation. | **not reachable for the claimed relation**; the start value is fixture-planted (and re-entry is static reachability only). |
| **I7** | `00328FF0` writes `{slot, code}` into `02EC1380` only when `(code ≠ 0 \|\| slot < 0) && row < 2` | No for the installer's call (`0023AA04`, real). The table's other writer inside any closure is again the installer itself, via re-entry. | **not reachable.** An install that re-enters the installer through spawn init would register through the same rule. |
| **I8** | pulse reset `002FEAB0` zeroes only the qword at `+0xEAC`; class float paths differ | No. `002FEAB0` runs real; the float conversions are body-local reads of the class record. | **not reachable** |

## What this means for the cell (for the scorer, not scored here)

- **Every I1–I8 claim about the installer's own effects is out of the scripted callees' reach**, on the bounded
  method above.
- **The exposure is four named value/selection points:**
  1. I1's terminal-arm **selection** (`00377C20`);
  2. I2's **mask conjunction** on the bit-4 path (`003105D0`);
  3. I3's **handle value** (`003220E0`);
  4. I4's class-1 **stats contents** (`0023AC80`).

  Each of the four callees is executed real in its own record (153, 161, 151, 152).
- **Compared with S-02**, whose one exposure (`0026A5F0`) had no execution: S-14's exposures are all covered by
  separate executions. None of them is covered by one stub-free run of `0023A570`.
- **What would close it without composition:** one EXP-150 run with `00377C20` real (I1 selection, the only
  exposure that decides control flow inside the installer), then `003105D0` real (the I2 mask). The other two are
  values the contract does not claim.

**Scorer's call:** whether piecewise execution meets the table's no-stub qualifier (S-10 MET, S-01 MIXED).
