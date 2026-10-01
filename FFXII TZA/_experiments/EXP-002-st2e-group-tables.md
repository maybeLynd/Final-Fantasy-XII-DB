---
experiment: EXP-002
title: What is in the st2e group tables, which are null in the file and built at load
status: RUN 2026-09-08 — AY-10 answered; a documented conclusion contradicted
contract: none — this settles an open question, not a contract claim
tool: Database/Tools/analysis-kit/gfz-scripts/ffxii_runtime.py + runtime_probe.py
method: C - ordinary UI input and read-only process observation
live_game: true
date_designed: 2026-09-08
date_run: 2026-09-08
---

# EXP-002 — the st2e group tables, read live

## Question

`AY-10` has been open since 2026-09-02 and is explicitly marked *“a live-memory question, not
static”*: the two group tables at `0x02EC3D80` and `0x02F973C0` are **null in the file and
populated at load**, so nothing static can say what is in them.

## Initial state

The reference build at the **title screen** — no save, no area. The operator confirmed the game
was up and healthy; the harness attached to that process rather than launching its own.

## Instrumentation

`runtime_probe.py --read`, read-only by construction. Controls: module at `ImageBase`, and
`LUAC_TAIL` at `0x01CCD300`. Two further controls were run for this experiment specifically:

- **an offset read** — reading at `table + 8` returns the window shifted by one qword, so the
  reads are position-accurate rather than cached;
- **the arena base at `[0x01F83530]` reads `0`** at the title screen, which matters because
  `ImageAddress_ResolveRuntimePointer` adds it — with a zero base the stored values *are* the
  addresses.

## Observed result

**16 of 28 slots are populated. Every one has magic `st2e`. 3,969 entries in total.**

| slot | pointer | magic | entries | first ids in the block |
|---:|---|---|---:|---|
| 1 | `0x6DDE48C0` | `st2e` | 428 | 10000, 10001, 10002, 10003 |
| 2 | `0x6DDE0A00` | `st2e` | 204 | 20000, 20001, 20002, **20100** |
| 3 | `0x6DDDBA00` | `st2e` | 398 | 30000, 30001, 30002, 30003 |
| 4 | `0x6DDD9340` | `st2e` | 322 | **40000, 40100, 40101, 40102** |
| 5 | `0x6DDDE4C0` | `st2e` | 69 | 50000, **50100, 50101, 50102** |
| 6 | `0x6DDDFA80` | `st2e` | 285 | 60000, 60001, 60002, 60003 |
| 9 | `0x6DDD82C0` | `st2e` | 26 | 90000, 90001, 90002, 90003 |
| 10 | `0x6D795440` | `st2e` | 251 | 100000, 100001, 100002, 100003 |
| 12 | `0x6DDD8500` | `st2e` | 32 | 120000, 120001, 120002, 120003 |
| 13 | `0x6DDD7BC0` | `st2e` | 64 | 130000, 130001, 130002, 130003 |
| 14 | `0x6D78A080` | `st2e` | 512 | 140000, 140001, 140002, 140003 |
| 17 | `0x6D789C80` | `st2e` | 35 | 170000, 170001, 170002, 170003 |
| 18 | `0x6DDE3180` | `st2e` | 457 | 180000, 180001, 180002, 180003 |
| 19 | `0x6DDDE840` | `st2e` | 303 | 190000, 190001, 190002, 190003 |
| 20 | `0x6D792580` | `st2e` | 512 | 200000, 200001, 200002, 200003 |
| 23 | `0x6D743740` | `st2e` | 71 | 230000, 230001, 230002, 230003 |

**Slot `n` holds ids beginning at exactly `n × 10,000` — 16 of 16, no exceptions.**

> ### The `+4` field is the bound the resolver checks
>
> `002F9860` tests `index >= [rax+4]` before indexing. Live, `[rax+4]` is **428** for slot 1 and
> **71** for slot 23 — an entry count, exactly as the resolver's use implies.

## Interpretation — and the contradiction

[The VBF / st2e document](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md)
§9 concluded, from the static reading alone:

> *“`40,000–41,243` falls in the gap between the two pools — above the low pool's 27,999 ceiling
> and below the high pool's 100,000 floor. **This resolver can never return text for a
> `help_action` id.**”*

**Slot 4 exists, and its first ids are `40000, 40100, 40101, 40102`** — the
`40000 + category*100 + slot` shape, sitting in the runtime string table. **The gap does not
exist**, and `help_action` ids are **runtime string ids**, which is `AY-10` answered in the
negative.

### What the live table implies about the two divisors

Both resolvers read **the same two tables** — the displacements `0x2da3d80` and `0x2e773c0` off the
image base appear in `002F9860` and `002F9920` alike, tool-resolved from both bodies. But the table
is indexed such that **slot n starts at n × 10,000**, so:

```
002F9920   id / 10000   ->  slot 4 for id 40000    consistent with the table
002F9860   id /  1000   ->  slot 40 for id 40000   out of range; and for id 10000 it would pick
                                                    slot 10, whose ids start at 100000
```

> **At most one of the two divisors can be indexing this table correctly, and the table says it is
> the ÷ 10,000 one.** What `FUN_002F9860`'s ÷ 1,000 path is *for* is **not established** — it may
> serve a domain below 10,000, or be legacy. **The observation is the table's shape; the
> resolution of the two functions is left open.**

## Confidence

| claim | confidence | why |
|---|---|---|
| 16 of 28 slots populated at the title screen | **PROVEN** | read live, controls passing |
| every populated slot has magic `st2e` | **PROVEN** | 16 of 16 |
| slot `n` holds ids from `n × 10,000` | **PROVEN** | 16 of 16, no exceptions |
| `+4` is the entry count | **PROVEN** | matches the bound `002F9860` tests |
| `help_action` ids are runtime string ids | **PROVEN** | slot 4, first ids `40000, 40100, 40101, 40102` |
| the “gap between the pools” | **CONTRADICTED** | slot 4 exists and is populated |
| what `002F9860`'s ÷ 1,000 divisor serves | **UNKNOWN** | not established |
| the stored values are 32-bit-wide quantities | **PROVEN** | all 16 have a zero high dword |

## What this experiment cannot settle

**The text itself.** Only the group headers and the leading id runs were read; no string was
resolved end to end, so nothing here says what id 40000 *says*.

**Whether 12 empty slots are unused or merely unloaded at the title screen.** A save in a field
area might populate more. `EQ-1`.

## Related

- [The VBF / st2e tables](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md) §9 — the static reading this corrects
- [`../_index/RUNTIME-RESEARCH.md`](../_index/RUNTIME-RESEARCH.md) — the harness and its controls
