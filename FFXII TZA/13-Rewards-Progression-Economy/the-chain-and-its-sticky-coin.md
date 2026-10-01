---
system: The chain and its sticky coin
category: 13-Rewards-Progression-Economy
status: AUDITED
owner_layer: PrimaryOwner:Rewards_Progression_Economy
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 5 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-03
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: first-read-repos-55
  crossref_clean: false
  reopened_count: 0
---

# The chain and its sticky coin

`EnemyChain_UpdateOnDefeat` at **`00317ED0`**, 529 bytes. Three documents leaned on it. It is the first
of the three unnamed calls in `BattleUnit_ProcessDefeatRewardsAndRetire`, and it runs **before** any
reward is computed.

## What the player sees

**Kill the same kind of enemy twice in a row and a counter advances. Kill a different kind and it
resets.** The comparison is one byte — `actor + 0x56` against a single global holding the previous
kill's value — so **the whole chain state is "what did I kill last".**

**And on every continued link, one coin is flipped — with a probability that depends on how the last
flip landed.**

```asm
00318034  test byte ptr [0x022C3178], 0x1
0031803B  jz   0x00318045
0031803D  cmp  ecx, 0x28          ; last flip SUCCEEDED
00318040  setge bl                ;   -> succeed on 40..99   = 60 %
00318045  cmp  ecx, 0x5           ; last flip FAILED
00318048  setl  bl                ;   -> succeed on 0..4     =  5 %
```

> **Five percent after a failure, sixty percent after a success** — and the result is written straight
> back into the same bit, so **the next flip's odds are decided by this one.**

**This is not a bonus that accumulates with chain length.** The chain counter and the coin are separate:
the counter grows while the kills match, the coin's odds depend only on **the immediately preceding
flip**. A long chain of failures stays at 5 %; **one success moves it to 60 % and keeps it there until
a failure.**

## The roll is inlined, and it is the loot generator

Three LCG steps, unrolled in place:

```asm
00317FEA  imul eax, ecx, 0x41C64E6D
00318005  add  eax, 0x3039
0031800C  mov  dword ptr [0x022C256C], eax    ; the shared LCG state
```

**Same multiplier, same increment, same state address as the loot draws** — this is one of the seven of
eight draw sites that are **inlined rather than called**, which is why a `call`-keyed census finds one.

**Three advances feed one number**: bits 16–26 of the first state and bits 16–25 of the second and third
are XOR-folded through two 10-bit shifts, then reduced `% 100` by the usual reciprocal.

> **The chain coin and the loot draw share a generator, so they are correlated through the draw
> counter** — exactly as the determinism work established for everything on this LCG. **Reloading a
> save does not reroll either**, because that generator is seeded by a counter, not by the clock.

## Two counters, not one

| global | keyed on | clamp |
|---|---|---:|
| `022C315C` | the chain length, incremented per matching kill | **999**, or **998** when a state predicate holds |
| `022C3160` | a **second** counter keyed on a `u16` at `[actor + 0xE68] + 0x40` | 999 |
| `022C3164` | incremented when the chain **breaks** | 999 |

**The second counter resets independently of the first** — a kill can continue the chain and reset the
finer counter in the same call, because they are keyed on different fields of the same actor.

**And the break path is not a mirror of the continue path.** It reports through a *different* function,
zeroes the chain and two other globals, and **increments the break counter** — so the engine keeps a
record of how many times the chain has been broken, separately from how long it currently is.

## Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Is the 5 % / 60 % split really conditioned on the previous flip? | The tested bit and the written bit are **the same bit of the same global** — `022C3178 & 1` tested at `00318034`, and the flip's result OR-ed back into it before return. |
| Is `0x28` a threshold or an index? | `cmp ecx, 0x28` / `setge` on a value that has just been reduced `% 100`. **A comparison against a modulo-100 result is a percentage.** |
| Is this the same LCG as loot? | **Same multiplier `0x41C64E6D`, same increment `0x3039`, same state address `022C256C`** — three matches, not one. |
| Could the chain key be a unit id rather than a kind? | It is **one byte at `+0x56`**, compared against a single global; a unit id would not survive the unit's death as a comparison target for the next kill. **Stated as a kind on that basis, not proven to be one.** |
| Does chain length feed the coin? | **No.** The length is clamped and reported; the threshold selection reads only the sticky bit. |

**What `0028EF00` and `0028EF70` present (added 2026-09-19, FABLE; five bodies read whole): the chain counter on the
HUD.** `0028EF00(count, level)` (79 B) is one arm's post - it resets the HUD object's chain flags `+0x7C7C` to
bits 3 and 0 and stores the pending count at `+0x7C78` and the level word at `+0x7C82`; `0028EF70(count, flag,
level)` (70 B) is the other arm's, which keeps the flags and sets bit 1 from its second argument; `0028EF50(level)` (29 B) raises flag bit 2. The counter widget sits in
the HUD sub-object at `+0x57E0`: its member `003F9F40` compares the pending word with the last one shown and calls
`003F9E50(widget, count, playSound)` (229 B), which hides on 0, **does not show a count of 1 while the state
predicate `00229E40` holds**, and otherwise stores the count at the widget's `+0xC8` and draws **`min(count, 999)`
in three digits** - an unsigned compare - with sound `0x30` when asked. While bit 1 of the widget's flags `+0xC4` is
up the number is redrawn every frame in a pulsing grey. *What flag bits 1 and 2 of `+0x7C7C` mean on screen was not
established.* Interior: `0028EF07`, `0028EF18`, `0028EF39`, `0028EF47`; `0028EF7F`, `0028EF93`, `0028EFA9`;
`003F9E6F`, `003F9E84`, `003F9EC0`, `003F9EEC`, `003F9F06`, `003F9F0D`, `003F9F1B`.

**What this document does not claim:** ~~what `0028EF70` and `0028EF00` present,~~ what `003183D0` does,
what the `u16` at `[actor + 0xE68] + 0x40` identifies, what the state predicate at `00229E40`
distinguishes (it changes a clamp from 999 to 998 and adds 1 to a reported length), or what the coin's
success actually causes — **this function computes and reports it; the consequence is elsewhere.**

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL and recorded in the registry.*

**Answered from elsewhere — the "state predicate at `00229E40`" this page leaves open.** `00229E40` returns
`[01E02814]`. That global has **one RIP-relative writer**: the boot initialiser stores into it (`0022A0CB`) the result of
the language-code mapper, which maps the configured language code (`jp en fr de it es kr ch cn`) to the locale id
([language selection and locale ids](../19-Save-Load-Settings/Language-And-Locale/language-selection-and-locale-ids.md)).
**The chain's 999 / 998 clamp and its +1 on the reported length therefore depend on the locale.** The companion
test `00229E50` returns 0 for locale ids 0, 6, 7, 8, 10 and 11 (mask `0xD81`). Which clamp belongs to which locale is
for the locale page to state; this note only names the input.

- **Presentation — CLIENT.** Three Presentation bodies (610, 896 and 6,441 bytes) read the same locale getter.
- **Script_VM_Native_Bridge — CLIENT.** Two script-verb bodies (37 B and 47 B) read it.

Both are locale reads, not chain state.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**UI — CLIENT (1 edges, one fan-in).** All 1 edges are UI bodies reaching `00229E40` on this page. `FUN_0028aaa0` is the worked example - it is a 1,692-byte routine in a `0xD0`-byte frame with a stack cookie and two preserved SSE registers. The crossing is **one shared subject with 1 callers on that layer**, not 1 separate relationships. Edge count from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Core runtime scheduling - SERVICE (added 2026-09-19, FABLE).** The counter's display routine `003F9E50`, named on this
page since today, asks the scheduling layer's seven-byte state predicate `00229E40` whether to suppress a count of 1 -
the same predicate the chain update itself consults. A shared getter; nothing of the chain is owned there.
