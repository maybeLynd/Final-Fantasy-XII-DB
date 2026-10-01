# S-33 runtime: per-invariant stub exposure for EXP-141 (OPUS, 2026-09-25, block 309)

**Row:** S-33, world loot pickups. The runtime cell reads **NOT MET** and the binding gap "runtime evidence".
- `CONTRACT-world-loot-pickup-pool.md` §13a (FABLE) records that **EXP-141 executes all five ops** of the contract as
  shipped bytes: 68 / 68 functional cases, 57 / 57 mutants killed, stable over three processes.
- What the row lacked is the analysis that lifted S-01: whether any of EXP-141's substitutions can reach an invariant.
- This note supplies it and scores nothing. Static probe: `candidates/s33-probes/s33_leaf_reach.py` (+ `.out.txt`).

## What ran real and what was substituted (EXP-141 §"Body census")

**Real, as shipped bytes:**
- the five entries `00319B10` / `00319CA0` / `00319600` / `00319920` / `003197B0` and both wrappers;
- the drop-tier classifier `00319A20` → `0031E9F0`;
- **the presentation dispatcher `0028F000`**;
- the presence helpers `002FB250` / `002FB2A0` / `002FB2D0`;
- the object lookups `0028EFE0` → `003FA730` and `0028EFC0` → `003FA6E0`;
- `00202C90`, `0020E600`, `0016D6A0`, and `00808C40` with the shipped cookie.

**Substituted: five application stubs** (scripted leaves, reached through the real dispatcher and traced at the call
boundary):

| leaf | role | reached from |
|---|---|---|
| `003FA160` | op 1 | create |
| `003FAA10` | op 2 | tick, blink |
| `003FA820` | ops 3 / 4 / 5 | collect, remove / despawn / eviction |
| `003FA900` | op 6 | not reached by the pool |
| `00300B80` | the inventory grant | collect |

Fixtures: the pool, the drop descriptor and rows, and the object manager.

## Can a substitution reach pool state? The static bound (probe)

For each leaf, over its whole static closure (`edges.tsv` direct edges):

| leaf | closure | references to pool / list / presence / counter globals | calls back into a pool function or a node-pointer reader (`00319850`, `002FB150`) |
|---|---:|---:|---|
| `003FA160` op 1 | 189 | **0** | none |
| `003FAA10` op 2 | 6 | **0** | none |
| `003FA820` ops 3 / 4 / 5 | 164 | **0** | none |
| `003FA900` op 6 | 2 | **0** | none |
| `00300B80` grant | 5 | **0** | none |

- **Globals checked:** the nodes `02EC0FA0`–`02EC135F`, head / tail `02EC1360` / `02EC1368`, the presence table
  `022BE7F0 + i·0x20`, and the counter `022C3174`. Every RIP-relative and absolute operand and immediate was checked.
- **No leaf is handed a pool pointer.** At every dispatcher call site the arguments are `ecx = [node+0x58]` (the
  handle, a value) and `r8 = rsp+0x20` (a stack payload); the grant gets `(itemId, quantity, 1)`. Since the pool is a
  static array and no closure takes its address, **a leaf cannot write pool state**.
- **Return values, at every call site in the pool bodies:**

  | call site | leaf | is the return read? |
  |---|---|---|
  | `003196C9` | op 4 | **no**; next is `mov ecx,[rbx]` → `002FB2A0` |
  | `00319732` | op 2 | **no**; `jmp 0031977A`, which reloads `rbx` |
  | `003199BF`, `003197FE` | op 3 | **no** |
  | `00319D24` | op 5 | **no** |
  | `00319965` | grant | **no**; the loop advances |
  | `00319E00` | op 1 | **yes**: `mov [rbx+0x58], eax`, **the only place a scripted return enters pool state** |

## Per invariant

| contract item | executed by EXP-141 | can a substitution reach it? |
|---|---|---|
| **I1** ten nodes of `0x60` | init, the create scan | **no**: body-local constants |
| **I2** free ⇔ `state == 0` | scan; every retire | **no**: the retire zeroes `state` after the leaf, whose return is unread and whose closure never touches the pool |
| **I3** `slotIndex` immutable | init; reuse after eviction | **no** (probe: no leaf references the nodes) |
| **I4** `+0x0C` / `+0x5C` padding | the write paths | **no**: an image-wide measurement, not an execution claim |
| **I5** FIFO: append at the tail, evict the head | `c-evict` | **no**. The op-5 leaf runs mid-eviction, before the relink, but it has no path back into the pool and no pool reference |
| **I6** on the list ⇔ `state != 0` | every path | **no** (same bound) |
| §7 state 1 → 2 | tick | **no**: `0028EFE0` / `003FA730` run real over the fixture manager |
| §7 blink 2–6 and expiry 7 (`stamp + 1800`) | tick | **no**: the op-2 / op-4 returns are unread; the arithmetic is real |
| §7 "at most one retirement per tick" | `t-despawn-mid`, `t-despawn-tail` | **no**: the retire's own `next = 0` ends the walk |
| create's postcondition: the op-1 return is stored at `+0x58` | create | **the store: no. The VALUE: yes, stub-supplied.** The handle EXP-141 observes is the scripted `003FA160`'s return. The contract's reading of it as a truncated object pointer (UQ-137, the `< 4 GB` requirement) rests on the lookup side, which ran real (`003FA730` compares against it), not on the producer |
| collect grants, then the counter, then op 3 | `g-collect` | **arguments and order: no.** The grant's inventory effect is the stub's; that belongs to the inventory contracts, not this one |
| §10 the op 4 / op 5 payload is uninitialised | tick despawn, eviction | **no**: the real dispatcher ignores the payload for ops 4 / 5 (`xor edx, edx`), so the residue never reaches a leaf |

## Findings

1. **§10's short-drop-buffer bullet is contradicted statically, and §11 with it.** §10 says "the grant loop stops at
   the first `itemId == 0xFFFF` … entries past the sentinel are copied and never read". §11 says it "grants every
   entry before the sentinel". The collect loop (`00319943`–`00319972`) runs **all seven entries** (`esi = 7`); `cmp
   ax, 0xFFFF / je 0031996A` **skips only that entry**. So entries after a `0xFFFF` are granted, and an all-zero entry
   is granted as `00300B80(0, 0, 1)`. EXP-141's `g-collect` shows the latter: four `0:0` grants.
2. **One stub-supplied value:** the `+0x58` handle (above). Everything else in the contract is outside every stub's
   reach.
3. **Stale texts:** the gap "runtime evidence" and the NOT MET cell predate §13a's citation of EXP-141.

## For the scorer

- **Application stubs:** five leaves. Four have unread returns and no reach into the pool. The fifth (op 1)
  supplies the stored handle.
- **Exposure:** only create's `+0x58` value. I1–I6 and the §7 transitions are not reachable.
- `live_game: false`. UQ-137 (live) is untouched.
