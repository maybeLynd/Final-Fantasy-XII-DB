---
contract: Choose a field's environment variant and publish it — a once-consumed latch and a banded preset
category: 03-World-Area-Field
scope: subsystem
readiness: CONTRACT READY
confidence: PROVEN
implements: choosing-the-field-environment-variant.md
entries: ["0026D910"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's invariants re-measured from
    the shipping bytes — the body's extent and instruction count, its terminating tail call with the
    four argument registers zeroed before it, the latch's set and release sites, the clamp, and every
    rip-relative global access classified as read or write. **This records checks performed on that
    date, not the method of the original derivation**, which is on the variant page; see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-env-variant-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — the field environment variant

> **Authored 2026-09-22 by FABLE.** S-11's gap was *"1 of 3 pages by subject"*. The trigger points
> were taken at commit `963fa2583`; **this takes the environment variant**, so all three of S-11's
> pages now have a contract.
>
> Written against FRONTIER's adequacy test: *a narrower contract is adequate exactly when the
> system's operations have no cross-operation invariant or ordering it leaves unstated.* §4 is six
> such invariants, and the first is about where this function **ends**.

## 1. Purpose

Pick which of three environment variants a field uses, and publish the result for the presentation
side to read *(answered: and for the combat side, which reads `02099DA8` and `02099DAC` through `00263E10` / `00263E20` — CONTRACT-weather.md §5; 2026-10-02, OPUS)*.

## 2. Interface

| | |
|---|---|
| **Entry** | `WorldField_InitializeCurrentFieldRuntimeParameters` (`0026D910`), **418 bytes, 111 instructions** |
| **Table** | the loaded `map_ref.bin` image at `02099D88`, addressed entirely by header offsets |
| **Exit** | a **tail call** to `002E3D40` (EV-1) |

## 3. Types

```
map_ref header
  +0x04   records array      the field's row is records + fieldId*8
  +0x08   16-byte-stride block
  +0x10   lookup array A
  +0x18   lookup array B

field row (8 bytes)
  +0x00   u16   carried forward into 00377850
  +0x02   s16   selects the 16-byte block entry, offset by (selector + 1) * 4
```

## 4. Preconditions · postconditions · invariants

### The six cross-operation invariants

**EV-1 — This function ENDS at `0026DAAD`, and everything a decompiler shows after that belongs to
someone else.** The body terminates `jmp 0x2e3d40` — a **tail call** to a separate 116-byte function
— and **all four argument registers are zeroed immediately before it** (`0026DA8B`–`0026DA90`), so
the callee receives `(0, 0, 0, 0)` at *this* site.

> **The constants in the trig block a decompilation attributes to this function are the callee's, and
> they are not flowing out of the field setup — they cannot be, because the arguments are zero.** *A
> tail call is a call; a decompiler renders it as a body, and a body is what a reader believes.* ~~The~~
> ~~variant page records this as the **fourth** distinct way this executable's decompiled output has~~
> ~~misdescribed a function boundary, and the only one of the four that is about the body rather than~~
> ~~the return.~~ *(answered: the variant page struck that count on 2026-09-30 — the three earlier cases are not cited, so it has no anchor; 2026-10-02, OPUS)*

**EV-2 — Three states, from a clamp.** `selector = clamp(count − 1, 0, 2)` (`0026D943 cmovg`), so the
domain is exactly `{0, 1, 2}` however large the count.

**EV-3 — The selector is ~~latched, and the latch is FIRST-WRITER-WINS and released on exit~~ gated by a skip flag that this body only clears.**
`0026D951` tests `[ctx + 0x1061]`; only when it is clear does `0026D95E` write the selector to
`[ctx + 0x1060]`. At the end, `0026DA92` clears `[ctx + 0x1061]` to zero. *~~So the selector written by~~
~~whoever got there first is consumed exactly once per pass, and a second caller within the same pass~~
~~publishes the first caller's choice.~~* *(corrected 2026-10-02, OPUS: the body never sets `+0x1061` - its setters are `0026D8F0` (`0026D8F9`) and `00268320` (`0026836C`), and a save-lifecycle function stores `dil` there (FABLE's record readiness-apply-fable-1002). So with the flag set, the first call publishes the slot already in `+0x1060` and consumes the flag, and a second call in the same pass writes its own selector unless a setter runs between them; with the flag clear, every call writes its own.)*

**EV-4 — The variant is an index INTO THE ROW, not a separate table.** The field's row is
`records + fieldId*8`; its `+2` selects an entry in the 16-byte block **offset by
`(selector + 1) * 4`**. *There is no per-variant table to find; the three variants are three
positions inside one row, which is why a search for a variant table finds nothing.*

**EV-5 — One published global is a three-state BAND compressed from an arbitrary count.** `02099DAC`
is `0` when `00377850(rowU16, selector + 1)` returns zero, and otherwise **`(result > 3) + 1`** —
so `1` or `2`. *A function returning a count is being read as a band, and the bands are not equal in
width*: by cross-reference the underlying value is the 3-bit weather preset, so the bands are preset
0, presets 1–3, and presets 4–7.

**EV-6 — One global is pre-zeroed at entry and the others are not.** `02099DBC` is written twice, the
first time at `0026D946` — **before any lookup** — so a failed lookup leaves it zero rather than
stale. `02099DA8`, `02099DAC` and `02099DB0` have no such pre-clear. *Three of the four published
globals can therefore retain a previous field's value if their write is skipped; one cannot, and that
asymmetry is deliberate enough to be written down.* **Executed** *(2026-09-25, FABLE, Claude Opus 5.5, on [OPUS block 352](../_index/candidates/s11-opus-replay-environment-variant/README.md))*: a field entered before its table is loaded publishes a zero terrain byte `02099DBC` beside **the previous
field's** environment class, weather band and lane byte. The only branches that skip the three writes test the
table pointer `[02099D88]` and its loaded guard `[02099D90]` (`0026D9C6`, `0026D9D3`), plus two computed-pointer
null tests. No row of the shipped `map_ref.bin` has a negative block index, so the row path cannot skip, and the
stale case needs an unloaded table.

> *(Resolved 2026-09-29 by falsification pass 1: the fifth global is the selector byte `021654E0`; see the pass section.)*
> **A count this contract does not reconcile.** The variant page says the function publishes **five**
> globals; a sweep of every **rip-relative** access in the body finds **four written** —
> `02099DA8`, `02099DAC`, `02099DB0`, `02099DBC` — plus two read-only (`02099D88`, `02099D90`). **A
> fifth global written through a register base would not appear in that sweep**, so this is a
> difference in method, not a refutation, and it is recorded rather than resolved.

## 5. State

**Owned:** the four published globals and the `[ctx + 0x1060]` / `[ctx + 0x1061]` selector-and-latch
pair. **Read, never written:** the `map_ref` image at `02099D88` and the second global `02099D90`.
**Handed on:** control, to `002E3D40` with zero arguments.

## 6. Relationships

| | |
|---|---|
| **Sibling** | [`CONTRACT-authored-trigger-points.md`](CONTRACT-authored-trigger-points.md) — S-11's second page |
| **Sibling** | [`CONTRACT-field-record-accessors.md`](CONTRACT-field-record-accessors.md) — S-11's first |
| **Downstream** | `002E3D40`, the weather-to-presentation refresh, which this contract does not claim |

## 7. State transitions

*count → clamp → latch if free → resolve the row → publish → release the latch → tail-call.* The
~~latch transitions `free → held → free` within one call.~~ flag is only cleared here (`0026DA92`); it is set outside the body *(corrected 2026-10-02, OPUS: the body never sets `+0x1061` - its setters are `0026D8F0` (`0026D8F9`) and `00268320` (`0026836C`), and a save-lifecycle function stores `dil` there (FABLE's record readiness-apply-fable-1002); EV-3)*.

## 8. Script · resource · event interactions

`map_ref.bin` is authored (kind 9, id 4). Every access to it is through header offsets, so the file's
layout is self-describing and nothing here hardcodes a record address.

## 9. Determinism

Deterministic. No generator is drawn.

## 10. Failure paths and edge conditions

- A selected byte out of range skips the `02099DA8` write, leaving the previous field's value (EV-6).
- A latch already held means this call publishes someone else's selector (EV-3).
- `00377850` returning zero gives band `0` rather than no write (EV-5).

## 11. Observable behaviour

A field looks different depending on which of three variants it is entered with; the choice is made
once per pass and the same for everything that reads it afterwards.

## 12. Reproduction formula

~~Call twice within one pass with different counts and assert the second publishes the **first's**~~
~~selector (EV-3).~~ Set `+0x1061`, call twice within one pass with different counts, and assert the first publishes the slot already stored and the second its own selector (EV-3) *(corrected 2026-10-02, OPUS: `0026D951` / `0026D957` skip the `0026D95E` store only while the flag is set, and `0026DA92` clears it)*. Assert the body's last instruction is `jmp 002E3D40` with `rcx`, `rdx`, `r8`, `r9`
all zero (EV-1). Drive `00377850` to return 3 and 4 and assert `02099DAC` is `1` then `2` (EV-5).

## 13. Runtime validation

~~**None.** No experiment executes this body. S-11's runtime cell is not addressed by this contract.
*Stated rather than left blank so a CONTRACT READY header is not read as evidence of execution.*~~ **Superseded
2026-09-25:** OPUS blocks 303 and [OPUS block 352](../_index/candidates/s11-opus-replay-environment-variant/README.md) executed this body. EV-1 is measured, since the tail call receives
`rcx = rdx = r8 = r9 = 0` at `002E3D40`, and EV-6 is measured with its consequence. The evidence class is native
replay, not live.

## 14. Unresolved

- ~~What the five globals feed — published here, consumed elsewhere.~~ *(answered: the four globals' readers are censused in CONTRACT-weather.md §5 — `00263E10`, `00263E20`, `00264D50`, and none found for `02099DB0`; choosing-the-field-environment-variant.md, reconciled 2026-09-30; 2026-10-02, OPUS)*
- ~~What the three variants mean to a player; three states exist and nothing names them.~~ *(answered: the selector is the field's weather slot — choosing-the-field-environment-variant.md and CONTRACT-weather.md §1; 2026-10-02, OPUS)*
- ~~The four-versus-five count of EV-6's note.~~ **Answered 2026-09-29 (OPUS, pass 1):** the fifth is the selector byte `021654E0` (`[ctx+0x1060]`, `ctx = 02164480`).

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| EV-1 — the tail call and the zeroed arguments | the body's last eight instructions read in order; `002E3D40` confirmed as its own 116-byte entry in the function table | 1 |
| EV-2, EV-3 — the clamp and the latch | `0026D943`, `0026D951`, `0026D95E`, `0026DA92` read at their addresses | 1 |
| EV-6 — the pre-zero and the asymmetry | every rip-relative access in the body classified read/write and ordered by address; `02099DBC`'s first write precedes every lookup | 1 |
| EV-4, EV-5's banding, and the weather cross-reference | [the variant page](choosing-the-field-environment-variant.md), and the MWeather page it cites | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on EV-1 through EV-6. **EV-1 is the one to get right
before writing any of it**: a port built from decompiler output will attach up to 116 bytes of another
function's behaviour to this one, with constants that cannot be reached from here.

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **WorldAreaField — internal.** The body is this category's own.
- **Presentation — SERVICE, but only through the tail call.** `002E3D40` is the weather-to-presentation
  refresh; this contract hands control to it and asserts nothing about it beyond the zero arguments.
- **Save_Load_Settings — MECHANICAL.** One callee of this body belongs to that layer. The variant
  selector is latched per pass (EV-3) and published to globals; ~~**whether any of it reaches the save~~
  ~~image is not established here**, and this edge is not evidence that it does.~~ *(answered: the selector is the persistent payload byte `+0x1060`, `021654E0` — this contract's falsification pass V5 and CONTRACT-weather.md §3 — so it is in the save image; 2026-10-02, OPUS)*
- **Every other layer reached is MECHANICAL**, through this body's own callees. *Their addresses are
  deliberately not cited: each is a hub, and naming one imports its whole edge set.*

## 17. Related

- [Choosing the field environment variant](choosing-the-field-environment-variant.md) — the mechanism
- [Contract — authored trigger points](CONTRACT-authored-trigger-points.md) — S-11's second page
- [Contract — field record accessors](CONTRACT-field-record-accessors.md) — S-11's first

## Cross-subsystem neighbours — SWE2-EC7 (pass-22 dispositions)

- **Presentation - SERVICE (1 edge).** `002E3D40` reaches bodies filed to presentation: `0040AAD0` - shared machinery across the layer boundary, no shared ownership.
- **Save_Load_Settings - SERVICE (1 edge).** `0026D910` reaches bodies filed to save/load/settings: `002EF2B0` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (3 edges).** `0026D910`, `002E3D40` are also called by bodies filed to script VM / native bridge: `003565C0`, `0034B6C0`, `0034BD10` - shared machinery across the layer boundary, no shared ownership.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**ActorEntity — CLIENT, MECHANICAL (3 edges).** `ActorManager_RunFieldRuntimePass` (`0025D9E0`), the area unload path `002628B0` and `ActorManager_BindLoadedDefinitionPayload` (`0026C8C0`) call `SaveImage_GetPersistentPayloadBase` (`002EF2B0`), the 20-byte getter that returns the constant `02164280` plus `0x200` and through which the variant body reaches its selector `+0x1060` and latch `+0x1061` (falsification pass, V5). They are other users of the same persistent save payload (the field pass reads an override id from it, the bind caches its address); the getter is an address constant, so the edge shares the save block, not the environment variant.

**Audio — CLIENT, MECHANICAL (1 edge).** `00261F90`, a 335-byte Audio-filed body, calls `002EF2B0` on its field-change branch: it tests bit `0x40` of payload byte `+0x1063` and, when set, takes the id stored at payload `+0x1534` instead of looking one up from the field id (read to that point only). It is another consumer of the persistent payload through the same address getter, not a reader of this contract's variant selector.

**Story_Event_Quest_Hunt — CLIENT, MECHANICAL (12 edges).** The twelve persistent-flag accessors call `002EF2B0`: the queries `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` (`0032A8A0`), `PersistentFlag_QueryBank2048` (`0032A930`), `PersistentFlag_QueryBank64A` (`0032A9A0`), `PersistentFlag_QueryBank64B` (`0032AA00`), `PersistentFlag_QueryBank512Low` (`0032AA60`), `PersistentFlag_QueryBank512High` (`0032AAD0`) and the matching setters `PersistentFlag_SetPrimary` (`0032AB60`), `PersistentFlag_SetBank2048` (`0032ABF0`), `PersistentFlag_SetBank64A` (`0032AC70`), `PersistentFlag_SetBank64B` (`0032ACF0`), `PersistentFlag_SetBank512Low` (`0032AD70`) and `PersistentFlag_SetBank512High` (`0032ADF0`). The story flag banks live in the same persistent payload as the variant selector, so the flag accessors and the variant body share the base getter; neither reads the other's bytes.

## Falsification pass 1 — 2026-09-29 (OPUS): every invariant survives; the four-versus-five count resolved

**Attack.** EV-1 to EV-6 became checks at their instructions, and a full write census of the body settles EV-6's open note.
Script: `Tools/analysis-kit/gfz-scripts/falsify_env_variant.py`, output `falsify_env_variant.out`, image `73461d08…`,
0 BROKEN.

| # | Clause attacked | Result |
|---|---|---|
| V0 | EV-1 | **survives**: 111 instructions ending `jmp 0x2e3d40` at `0026DAAD`, after zeroing `rcx`, `rdx`, `r8` and `r9` |
| V1 | EV-2 | **survives**: `clamp(count − 1, 0, 2)` |
| V2 | EV-3 | **survives**: the `+0x1061` test guards the `+0x1060` write; `0026DA92` clears `+0x1061` |
| V3 | EV-5 | **survives**: `cmp ecx, 4 / setge / inc` into `02099DAC`, and 0 when the lookup returns 0 |
| V4 | EV-6 | **survives**: `02099DBC` is zeroed at `0026D946`, before any lookup |
| V5 | EV-6's unreconciled count | **resolved** (below) |

* **The fifth global is the selector byte.** The body writes exactly six global cells:
  * four RIP-relative: `02099DA8`, `02099DAC`, `02099DB0` and `02099DBC`;
  * two through `002EF2B0`, which returns the constant `02164280 + 0x200`: the selector at `+0x1060`, which is
    **`021654E0`**, and the latch at `+0x1061`, which is **`021654E1`**.

  So the page's "five published globals" are the four plus the selector. The latch is control state, not a published
  value, and the RIP-relative sweep missed both because they are written through a register. It is a difference of
  method, as the note suspected, now closed.

No correction.
