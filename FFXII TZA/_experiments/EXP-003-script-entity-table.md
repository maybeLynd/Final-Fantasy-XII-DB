---
experiment: EXP-003
title: What is in the script-entity table, which is empty in the file and built at load
status: RUN 2026-09-08 — the empty state established, and a document of mine corrected
contract: none — settles an open question about a table built at load, not a contract claim
tool: Database/Tools/analysis-kit/gfz-scripts/ffxii_runtime.py + runtime_probe.py
method: C - ordinary UI input and read-only process observation
live_game: true
date_designed: 2026-09-08
date_run: 2026-09-08
---

# EXP-003 — the script-entity table, read live

## Question

`ER-1`: what is in the 128-record table at `0x0215FDA0` that the script VM's entity resolver
indexes? It is **8,192 bytes past the end of `.data`'s file image**, so it is empty in the
executable and nothing static can say.

## Initial state

The reference build at the **title screen**, launched by the harness. **No save loaded**, so this
establishes the *empty* state deliberately — the baseline a later field-area read is diffed against.

The launch also confirmed `EO-2`'s fix in practice: the harness reported
*"the launched process exited; adopting pid 35280 (the game restarts itself through Steam)"*.

## Instrumentation

`runtime_probe.py --read`, read-only, with the standing controls (module at `ImageBase`,
`LUAC_TAIL`). The whole 8,192-byte table was read in one call and parsed offline.

## Observed result

**All 128 records are pre-initialised, and every one self-validates.** Applying the resolver's own
rule — `slot = ((u16[+0x24] << 16) | (u16[+0x1A] | 0x8000)) & 0x7FFF`, which must equal the
record's index — **128 of 128 pass**.

**The stamp at `+0x24` is `0` in every record.** One distinct value across the table.

**Only nine byte offsets differ between the 128 records:** `0..3`, `8..11`, and `26`.

```
slot 0   +0x00  00 00 00 00      +0x08  e0 fd 15 02   -> 0x0215FDE0 = slot 1
slot 1   +0x00  a0 fd 15 02      +0x08  20 fe 15 02   -> slot 0, slot 2
slot 127 +0x00  20 1d 16 02      +0x08  00 00 00 00   -> slot 126, and NULL
```

> **`+0x00` is `prev` and `+0x08` is `next`.** The 128 records are chained into a **doubly-linked
> list** — head at slot 0 with a null `prev`, tail at slot 127 with a null `next`. **The entire pool
> is on the free list**, which is exactly what it should look like with no map loaded.

| offset | at the title screen | reading |
|---|---|---|
| `+0x00` | pointer to the previous record | `prev` |
| `+0x08` | pointer to the next record | `next` |
| `+0x1A` | the slot's own index, 0–127 | the handle's low half |
| `+0x1E` | `0xFFFF` in all 128 | uniform, unknown |
| `+0x24` | `0` in all 128 | the handle's high half |
| the other 46 bytes | zero in all 128 | unread |

## What it corrected

**A document committed earlier the same day.**
[How a script names a thing in the world](../01-Script-VM-Native-Bridge/how-a-script-names-a-thing-in-the-world.md)
§3 wrote the placement formula as `rec[+0x04]`, `rec[+0x06]`, `rec[+0x08]` — a name that reads as
the record `002E97C0` returns.

> **It is a different object.** `setuptreasure` decodes the result of `002650B0`, not the entity
> record, and the entity record's `+0x00`/`+0x08` are **linked-list pointers**. The offsets collide;
> the structures do not. **A reimplementer following that naming would have decoded a `prev` pointer
> as a coordinate.**

The same re-reading found a second error: the selector is `args[2]` (`mov r8d, [rbx+8]`), not
`args[1]`. `args[1]` is not read on this path at all.

## Interpretation

**The pool is fixed at 128 records of 64 bytes**, so a map can name **at most 128 entities** — a
hard limit, not a soft one. At the title screen the pool is entirely free and every slot's naive id
`0x8000 | slot` resolves.

> **The check protects nothing yet.** The resolver's compare-before-use is proven from the code, but
> with every stamp at `0` there is no state for it to catch. **Whether `+0x24` ever changes is not
> observed** — one reading, one value — so "generation" remains a reading and is labelled as one.

## Confidence

| claim | confidence | why |
|---|---|---|
| 128 records of 64 bytes at `0x0215FDA0` | **PROVEN** | the resolver's stride and bound, read live |
| all 128 self-validate under the resolver's rule | **PROVEN** | 128 of 128 |
| `+0x00` is `prev`, `+0x08` is `next` | **PROVEN** | slot 0 null-prev, slot 127 null-next, every link lands on an adjacent record |
| the whole pool is free at the title screen | **PROVEN** | the list spans all 128 |
| `+0x24` is a generation that increments | **HYPOTHESIS** | one observation, one value |
| what a record holds with a map loaded | **UNKNOWN** | 46 bytes zero throughout here |

## What this experiment cannot settle

**Anything about a loaded map.** That needs a save loaded, which is the capability the harness does
not yet have — it can launch to the title screen and no further. `ER-1` stays open on that half, and
so does `EQ-1` for the twelve empty st2e slots. **Both want the same missing capability**, which is
the honest next thing to build.

## Related

- [How a script names a thing in the world](../01-Script-VM-Native-Bridge/how-a-script-names-a-thing-in-the-world.md) §4b
- [`../_index/RUNTIME-RESEARCH.md`](../_index/RUNTIME-RESEARCH.md) — the harness and what it still cannot do
- [`EXP-002`](EXP-002-st2e-group-tables.md) — the other table read from the same title screen
