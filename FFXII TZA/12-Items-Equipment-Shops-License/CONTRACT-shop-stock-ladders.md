---
contract: Choose how far up a shop's stock ladder the player has climbed — once, by pointer, with the last line as the floor
category: 12-Items-Equipment-Shops-License
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: 12-Items-Equipment-Shops-License/the-shop-table-and-its-stock-gates.md
entries: ["002FAD40", "002FA920", "002FAE40", "002536F0", "00315390"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's invariants measured from the
    shipping bytes — the gate walk disassembled in full and **every one of its exits traced to the
    value left in its return register**, the listing's match against the gate's result read at its
    instruction, the two operand-query call sites compared argument by argument, and the callers of
    the gate and of the rank computation censused image-wide. **This records checks performed on
    that date, not the method of the original derivation**, which is on the shop-table page; see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-shop-ladders-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — shop stock ladders

> **Authored 2026-09-22 by FABLE.** S-30's binding gap is *"bazaar unlock contracted; stock ladders
> are not"* — its one contract,
> [`CONTRACT-bazaar-unlock-and-purchase.md`](CONTRACT-bazaar-unlock-and-purchase.md), covers the
> bazaar. **This takes the stock ladders.**
>
> Written against FRONTIER's adequacy test: *a narrower contract is adequate exactly when the
> system's operations have no cross-operation invariant or ordering it leaves unstated.* The gate and
> the listing are **one operation split across two functions** — SG-1, SG-2 and SG-4 are facts about
> what the second is guaranteed to find, and neither body states them alone.
>
> **The shop-table page is unusually complete** and this contract does not re-derive it. Four of the
> seven invariants below were nonetheless unstated anywhere: nothing in the database cited
> `002FADC3`, `002FAD75`, `002FADBF`, `002FAABF` or `002FAAC4`.

## 1. Purpose

Decide which line of a shop's authored ladder the player has reached, and list everything from there
down.

## 2. Interface

| | body | size |
|---|---|---:|
| **the gate** | `002FAD40` | 251 B, **exactly one caller** |
| the listing | `002FA920` | 676 B |
| the row's name id | `002FAE40` | — |
| the clan rank, truncated | `002536F0` | **17 B** — `movzx eax, al` over the rank |
| the clan rank | `00315390` | —, **3 callers** |

## 3. Types

```
shop table   registry slot 02EBF158, three levels, each {u32 tag, u16 stride, u16 count, u32 data}
  row[i]     8 B   {u32 nameId, u32 section}          tag 0x64
    entry[j] 8 B   {u8 gateKind, u8 operandIndex,     tag 0x164
                    u16 threshold, u32 list}
      id[k]  2 B   an encoded item id                 tag 0x264

gateKind  0  always passes
          1  operand query, element = entry[+1]
          2  operand query, element FORCED to 0 -- entry[+1] is dead (SG-4)
          3  clan rank >= threshold
      other  the entry is SKIPPED (SG-5)
```

## 4. Preconditions · postconditions · invariants

### The seven cross-operation invariants

**SG-1 — The gate is evaluated exactly ONCE per listing, and its result travels as a POINTER.**
`002FAD40` has **one call site in the whole image** (`002FA9AE`), and it returns the chosen *entry
address*, not an index (`002FAE2D mov rax, rbx`). The listing stores it (`002FA9B3`) and then walks
the entries matching by **pointer identity** — `002FAABF cmp rsi, qword ptr [rsp + 0x30]` /
`002FAAC4 jne` — setting a *reached* flag and copying every id from that entry onward. **No gate is
consulted a second time.** *So a ladder is cumulative downward, the authored ORDER is the whole
meaning, and an entry's threshold is dead once any earlier entry has been chosen — which is why
[row 24's](the-shop-table-and-its-stock-gates.md) twenty-three later gates never fire.*

**SG-2 — When NO entry's gate passes, the walk returns the LAST entry — not nothing.** `rbx` is
loaded with the current entry's address on every iteration (`002FADBF`) and is what the function
returns at **every** exit, including the loop-exhausted one at `002FAD75`. Only a section whose count
is zero returns null, because `rbx` is still the `002FAD4F xor ebx, ebx` initial value. *The floor of
a ladder is therefore structural, not authored: the last line is offered whether or not its own gate
passes. ~~The 56 rows that end in an ungated entry make this invisible~~, and a reimplementation that
returns "no entry" on an all-gated row empties a shop the original still stocks.* **On the shipped table, 46 rows
end in a line that always passes, and 11 rows fall through to their last line** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 324, which ran the gate over all 57 shipped rows ([package](../_index/candidates/s30-opus-replay-shop-ladders/README.md)); `00315390`, its rung table and the operand helper's selector-3 arm re-read.)*. Of the 46, 43 end in
kind 0. Rows 17 and 18 end in `k2@0`, which passes while the story word is below `0x8000` (§10). Row 2 ends in
`k3@1`, which the clan rank's floor of 1 always passes. The 11 are rows 21, 22, 26, 27, 43, 44, 48, 49, 51, 54, 55 (§14).

**SG-3 — The count fails closed and the entry pointer does not.** A section that will not resolve
yields count `0` (`002FAD71 xor ecx, ecx`) and the loop exits cleanly. But a section whose *data*
pointer will not resolve takes `002FADC3 xor ebx, ebx`, and **the very next instruction dereferences
it** — `002FADC5 movzx eax, byte ptr [rbx]`. *Two failures of the same kind, one guarded and one not,
in one function.*

**SG-4 — Gate kinds 1 and 2 are the SAME query and differ in exactly one argument.** Both call
`AiTargetSelector_ResolveOperandValue` with `ecx = 3` and `edx = 0`; kind 1 passes the entry's own
byte as the element (`002FADD0 movzx r8d, byte ptr [rbx + 1]`), kind 2 **forces it to zero**
(`002FADFA xor r8d, r8d`). *So kind 2 is kind 1 specialised to element 0, and an entry authored as
kind 2 carries a dead `operandIndex` byte* — which matters because the shipped table, per
[the page](the-shop-table-and-its-stock-gates.md) §2.4, uses only element 0.

**SG-5 — The kinds are a fall-through chain over a RE-READ byte, and an unknown kind skips the entry
rather than failing the shop.** `002FADC5`, `002FADEE` and `002FAE0F` each read `[rbx]` again. A
value outside `0..3` matches no test and falls to `002FAE21 inc esi`. *A corrupt or future gate kind
silently drops one line and leaves the rest of the ladder working.*

**SG-6 — The clan rank has NO storage; every consumer recomputes it.** `00315390` has **3 call
sites**: the shop's 17-byte truncating thunk `002536F0`, the handbook screen's pane-1 leaf
helper `0056F470` (identified 2026-09-23 — it feeds the rank to display helper `00394850`), and
`SaveImage_FinalizeHeaderAndChecksum`. *(That finalizer's own addresses are deliberately not cited:
it is a hub, and the claim here is carried entirely by the caller census of the rank.)* *The rank written into a save header is a
snapshot of a function, not a field — so the shop gate and the save file can never disagree, and
editing the rank in a save changes nothing the gate will see.* The thunk also **narrows the rank to a
byte** (`002536F9 movzx eax, al`) before it is compared.

**SG-7 — The loop re-resolves everything, and forms the entry address with a 32-bit add.** The
section pointer `[rdi + 4]` is passed to `ImageAddress_ResolveRuntimePointer` **six times per
entry**, and the count is re-read at the top of every pass (`002FAD56`–`002FAD6B`), so **the loop
bound is not snapshotted**. The address itself is built by `002FADB0 mov rbx, rax` — a 64-bit
resolved base — followed by `002FADBF add ebx, ecx`, **a 32-bit add that discards the high half**.
*Recorded as measured: it constrains where the resolved table may live, and this contract does not
establish that the constraint is ever approached.*

## 5. State

**Owned:** nothing. Both bodies are pure over the loaded table. **Read, never written:** the three
levels behind `02EBF158`, the kind-3 operand bank, and the clan-rank inputs. **Written:** only the
caller's `out` array, by the listing.

## 6. Relationships

| | |
|---|---|
| **Sibling** | [`CONTRACT-bazaar-unlock-and-purchase.md`](CONTRACT-bazaar-unlock-and-purchase.md) — S-30's contracted half, and **mode 2 of the same listing function** |
| **Consumes** | the kind-3 authored-operand bank — [the save payload map](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md) §2.2 |
| **Shares a computation** | `SaveImage_FinalizeHeaderAndChecksum`, which recomputes the same rank (SG-6) |
| **Names** | the row's first word is a dictionary name id — [the NPC-name dictionary](../04-Actor-Entity/Actor-Names/the-npc-name-dictionary.md); **not re-derived here** |

## 7. State transitions

None; the subsystem holds no state. Per listing: *resolve the section → walk entries in authored
order → first passing gate, else the last entry (SG-2) → match by pointer → copy every id of the
requested category from there onward.*

## 8. Script · resource · event interactions

The whole table is authored in `battle_pack.bin` and rebased once at bind time. Which field a row
stands in is authored by `setshopname` in the field scripts, censused on
[the page](the-shop-table-and-its-stock-gates.md) §7 and not re-derived here.

## 9. Determinism

Deterministic. No generator is drawn. The gate's inputs — the operand bank and the clan rank — are
both derived from saved progress, so one save yields one ladder position.

## 10. Failure paths and edge conditions

- An empty section returns null (SG-2).
- An unresolvable section data pointer **faults** rather than returning nothing (SG-3).
- A gate kind outside `0..3` skips its entry (SG-5).
- A negative operand value fails every threshold: the compares are signed (`jge`) against a
  zero-extended `u16` (`002FADE4`, `002FAE05`, `002FAE19`). **The story operand can be negative** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 324, which ran the gate over all 57 shipped rows ([package](../_index/candidates/s30-opus-replay-shop-ladders/README.md)); `00315390`, its rung table and the operand helper's selector-3 arm re-read.)*: kind 2's
  selector-3 arm sign-extends the 16-bit story word (`movsx ecx, ax` in the operand helper's selector-3 arm). So a story word of `0x8000` or more
  fails even a `k2@0` gate.

## 11. Observable behaviour

A shop's stock grows as the story advances, and it grows by *revealing earlier lines*, never by
swapping one list for another. The clan shop adds exactly one line per rank.

## 12. Reproduction formula

Author a section whose every entry is gated above the player's progress and assert the shop still
offers the **last** line (SG-2) — an implementation returning "none" is wrong here and right
nowhere. Author an entry of kind 2 with a non-zero `operandIndex` and assert it is ignored (SG-4).
Author a gate kind of `4` and assert exactly that entry vanishes (SG-5) ~~.~~ **when the walk reaches it.**
If a line above it passes, the walk stops there. The listing then copies every line from that one to the end,
and the unknown line's ids are among them *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 324, which ran the gate over all 57 shipped rows ([package](../_index/candidates/s30-opus-replay-shop-ladders/README.md)); `00315390`, its rung table and the operand helper's selector-3 arm re-read.)*. Change the rank in a save
header and assert the shop is unmoved (SG-6).

## 13. Runtime validation

~~**None.** No experiment executes these bodies.~~ **Superseded** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 324, which ran the gate over all 57 shipped rows ([package](../_index/candidates/s30-opus-replay-shop-ladders/README.md)); `00315390`, its rung table and the operand helper's selector-3 arm re-read.)*: OPUS block 324 ran the gate, the
listing and the clan rank as shipped code over the shipped table. SG-1 to SG-7 held, and SG-2 held over all 57 rows. S-30's runtime cell is not addressed by this contract.
*Stated rather than left blank so a CONTRACT READY header is not read as evidence of execution.*

## 14. Unresolved

- [x] ~~Whether any shipped row is all-gated, which is the only condition under which SG-2 is
      observable.~~ **CLOSED 2026-09-23 (SWE2-CONTRACT), by direct table scan.** Re-running the
      row/entry decode over `battle_pack.bin` (directory `+0xA0`, 57 rows, 267 entries —
      matching the page's census to the entry) gives **14 rows with no kind-0 entry**:
      2, 17, 18, 21, 22, 26, 27, 43, 44, 48, 49, 51, 54, 55. Two of those end in `k2@0`, and
      kind 2 passes when the story counter `≥ threshold` (`002FAE05`–`002FAE0D`,
      `cmp value, threshold; jge → return entry`), so a `0` threshold is an always-pass tail —
      rows 17 and 18 are *effectively* ungated. ~~**The other 12 are truly all-gated**: row 2
      (the Clan Provisioner — twelve kind-3 gates at ranks 12…1, all fail below rank 1), and~~
      **The other ~~12~~ 11 are truly all-gated: row 2 is not** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 324, which ran the gate over all 57 shipped rows ([package](../_index/candidates/s30-opus-replay-shop-ladders/README.md)); `00315390`, its rung table and the operand helper's selector-3 arm re-read.)*. `00315390` never returns below 1: rung 1
      of its table at `00D105D0` is `{0, 0, 0}`, and the loop's fall-through stores `1` (`003153E1`). So row 2's `k3@1`
      tail always passes, like rows 17 and 18's `k2@0`. The 11 are rows 21, 22, 26, 27, 43, 44, 48, 49, 51, 54, 55 (all kind-2,
      minimum gates 500–3,250).
      **SG-2 is therefore observable in normal play**: opening any of these shops before its
      lowest gate returns the last entry's stock — e.g. rows 43/44/51 fail open into their
      `@500` tail before story progress 500. Whether each shop's *field* is reachable that
      early is the same runtime-placement caveat UQ-133 already records for row 24.
- [x] ~~Whether gate kind 1 is used by any shipped row.~~ **CLOSED 2026-09-23 (SWE2-CONTRACT):
      zero kind-1 entries in the shipped table** — the independent rescan reproduces the page's
      census exactly (kind 0 on 45 entries, 2 on 210, 3 on 12; `operandIndex` 0 everywhere).
      The kind-1 arm itself is now fully decoded (`002FADCC`–`002FADEC`): it calls
      `00321190(3, 0, entry.operandIndex, &out)` — the same helper and the same
      `out ≥ threshold` test as kind 2, differing only in that kind 2 hardcodes `r8=0` and kind
      1 passes the entry's `operandIndex` byte. Since every shipped `operandIndex` is 0 anyway,
      kind 1 would behave identically to kind 2 even if it were used — it is a dead arm over
      live data, not a missing feature.
- ~~What the second caller of `00315390` is for (SG-6 counts it and does not read it).~~
  **CLOSED 2026-09-23 (SWE2-CONTRACT): it is the handbook screen's clan-rank pane.** The
  unaccounted call site is `0056F482` inside `0056F470` — the leaf helper the pane-1 construct
  `0056F410` installs ([the-handbook-screen](../16-UI/Handbook/the-handbook-screen.md) §members).
  The body fetches the recomputed rank (`movzx ebx, al`), passes it to display helper
  `00394850` (`rcx` = the pane context, `edx = 0xD`, `r9d = 2`, stack args 3 and the rank), and
  returns it onward — a UI read, same as the save-header snapshot: the rank is recomputed for
  the handbook pane, never stored. SG-6's claim is unchanged and now complete: the three
  consumers are the shop thunk `002536F0`, the save finalizer `00583D60`, and the handbook
  pane `0056F470`.

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| SG-1 — one evaluation, carried by pointer | `002FAD40` censused image-wide — **1 call site in 1 function** — and `002FA9AE`/`002FA9B3`/`002FAABF`/`002FAAC4` read in order | 1 |
| SG-2 — the last-entry fallback | **every exit of `002FAD40` traced to the value in `rbx`**: `002FAD4F` sets it to 0, `002FADBF` sets it per entry, `002FAD75` leaves the loop with the last one, `002FAE2D` returns it | 1 |
| SG-3 — the asymmetric failure | `002FAD71` against `002FADC3`/`002FADC5`, the two resolve failures compared side by side | 1 |
| SG-4 — one differing argument | `002FADD0`–`002FADDF` and `002FADF3`–`002FAE00` compared register by register | 1 |
| SG-5 — the fall-through and the skip | `002FADC5`, `002FADEE`, `002FAE0F`, `002FAE21` | 1 |
| SG-6 — the rank is recomputed | `00315390` censused image-wide — **3 call sites** — and `002536F0` disassembled in full (17 B); all three sites resolved 2026-09-23: `002536F4`, `00583F2A` (save-header `+0x44`), `0056F482` (handbook pane-1 helper `0056F470` → `00394850`) | 1 |
| SG-7 — the re-resolves and the 32-bit add | the six `[rdi + 4]` resolves counted in one iteration; `002FADB0` against `002FADBF` | 1 |
| the three-level table, the rank ladder and the shipped shapes | [the shop-table page](the-shop-table-and-its-stock-gates.md) §§2.1–2.6, falsified 2026-09-13 | 1 |
| shipped gate-kind census: kind 0 on 45 entries, 2 on 210, 3 on 12, **kind 1 on none**; `operandIndex` 0 everywhere | independent rescan of `battle_pack.bin` dir `+0xA0`, 57 rows × 267 entries, 2026-09-23 | 1 |
| 14 rows carry no kind-0 entry; rows 17/18 end in always-pass `k2@0`; ~~the other **12 are truly all-gated** (row 2 clan rank ≥ 1;~~ **11 are truly all-gated** (21, 22, 26, 27, 43, 44, 48, 49, 51, 54, 55 story-gated, minima 500–3,250); row 2's `k3@1` always passes (`00315390` ≥ 1, `003153E1`; corrected 2026-09-25 on OPUS block 324) | per-row gate-kind enumeration of the same scan | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on SG-1 through SG-7. **SG-2 is the one to copy
before anything else**: returning "no entry" when no gate passes is the obvious design, it is wrong,
and the divergence is invisible on the ~~45~~ **46** rows whose last entry always passes (SG-2's count as corrected on 2026-09-25; propagated here 2026-09-29, OPUS falsification pass 1) — but **observable
on the ~~12~~ **11** truly all-gated rows** (§14; corrected 2026-09-25 on OPUS block 324), where the original keeps the last line stocked and the
wrong port shows an empty shop. Exactly the kind of defect that ships.

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **Items_Equipment_Shops_License — internal.** The gate, the listing and the name accessor are this
  category's own.
- **Save_Load_Settings — SERVICE, and SG-6 is the statement.** The rank computation is shared with
  the save header's finalizer; this contract asserts that they recompute one value and nothing about
  the finalizer's own behaviour.
- **CombatAI — SERVICE.** The operand resolver kinds 1 and 2 call belongs to that layer; SG-4 is
  about which arguments each call passes, not about the resolver.
- **PlatformOnlineAchievements — SERVICE, and SG-6 is the statement.** The clan-rank computation and
  its two counters belong to that layer — [the achievement-counters
  contract](../20-Platform-Online-Achievements/CONTRACT-achievement-counters.md) records them as
  *named and bounded*. **This contract asserts only that the rank has no storage and is recomputed by
  each of its three callers**, not what the counters count.
- **UI — MECHANICAL, and the fan-in is SG-1's setting.** The shop menu is a caller of the listing;
  **the gate has one caller and the listing has several**, which is why the gate can be evaluated
  once and the ladder position carried as a pointer. *No menu address is cited: the claim is about
  the gate's caller count, not about any menu.*
- **Every other layer reached is MECHANICAL**, through these bodies' own callees. *Their addresses
  are deliberately not cited: each is a hub, and naming one imports its whole edge set.*

## 17. Related

- [The shop table and its stock gates](the-shop-table-and-its-stock-gates.md) — the mechanism
- [Contract — the bazaar unlock and purchase](CONTRACT-bazaar-unlock-and-purchase.md) — S-30's contracted half
- [Contract — equipment compatibility](CONTRACT-equipment-compatibility.md) — the id space the lists carry

`00316480` (289 B) is the offset-chain scan `00315390` runs on `022C2550`'s blob: `[rdx+8]` chains `word` offsets twice into a counted table (`word[+2]` rows), and the loop re-walks the chain per index, compares `dil` against `word[rcx+2]`, and runs `0046B1A0`/`0046B240`/`0046B180` on the match classes - the clan rank's per-tier sheet lookup over the menuhandbook relocation format.

Interior anchor `0031652D` (function `00316480`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-EC7-169, 2026-09-23)

**CombatAI — MECHANICAL (SWE2-EC7-169, 4 edges).** `0046B180`/`0046B1A0`/`0046B240` —
the clan-rank scan's class helpers — are called by `00321190` of that layer, and
`002FAD40`->`00321190` rides the same edge; shared-helper fan-in, not an AI
relationship of the ladder.

**PlatformOnlineAchievements — MECHANICAL (SWE2-EC7-169, 7 edges).** The clan-rank
chain — `002536F0`->`00315390`->`00316480`/`00316670`, plus `00316480`'s calls into
`0046B180`/`0046B1A0` — touches that layer's bodies; the ladder itself stays
shop-owned.

**Presentation — MECHANICAL (SWE2-EC7-169, 1 edge).** `0046B1A0` is called by
`00578450` of that layer — one fan-in edge.

**Save_Load_Settings — MECHANICAL (SWE2-EC7-169, 4 edges).** `0046B180`/`0046B1A0`/
`0046B240` call `002EF2B0` of that layer, and `00315390` is called by `00583D60` —
shared-helper fan-in both ways.

**Script_VM_Native_Bridge — MECHANICAL (SWE2-EC7-169, 4 edges).** `0046B180`/
`0046B1A0`/`0046B240` are called by `00351F90`/`0033FAA0`/`0033F6E0`, and `002FAE40`
by `0034C170` — script-bridge fan-in.
- **CombatAction - CLIENT (2 edges).** `00321190` is also called by bodies filed to combat action: `002FE660`, `00312170` - shared machinery across the layer boundary, no shared ownership.
- **Party - SERVICE (1 edge).** `00583D60` reaches bodies filed to party: `003271D0` - shared machinery across the layer boundary, no shared ownership.
- **Story_Event_Quest_Hunt - SERVICE (1 edge).** `00583D60` reaches bodies filed to story/event: `0032A8A0` - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT and SERVICE (2 edges).** `002FA920` is also called by bodies filed to UI: `0057CF20` (Shop); `00394850` reaches bodies filed to UI: `0029F6E0` (NumericDisplay) - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - SERVICE (2 edges).** `00583D60` reaches bodies filed to WorldAreaField (world area): `00264F90`, `003148F0` - shared machinery across the layer boundary, no shared ownership.

## Falsification pass 1 — 2026-09-29 (OPUS): every invariant survives; §16 caught up with SG-2's count

**Attack.** SG-1 to SG-7, §2's sizes, §10's compares and §14's rank floor became checks at their instructions. The call
censuses of the gate and the rank are image-wide. Script: `Tools/analysis-kit/gfz-scripts/falsify_shop_ladders.py`, output
`falsify_shop_ladders.out`, image `73461d08…`, 0 BROKEN. The shipped-table census (57 rows, 267 entries) is carried from
OPUS block 324 and SWE2-CONTRACT's rescan.

| # | Clause attacked | Result |
|---|---|---|
| G0 | §2 | **survives**: 251 / 676 / 17 B |
| G1 | SG-1 | **survives**: one call site image-wide (`002FA9AE`); `mov rax, rbx` returned; stored to `[rsp+0x30]` and matched by pointer at `002FAABF` |
| G2 | SG-2 | **survives**: five jumps (exhausted, kind 0, three `jge`) reach the one epilogue that returns `rbx`; one `ret`, no other exit |
| G3 | SG-3 | **survives**: count `xor ecx, ecx` against `xor ebx, ebx` then `movzx eax, byte ptr [rbx]` |
| G4 | SG-4 | **survives**: the two argument set-ups differ in exactly one instruction, `movzx r8d, byte [rbx+1]` against `xor r8d, r8d` |
| G5 | SG-5 | **survives**: three reads of `[rbx]`; an unknown kind reaches `inc esi` |
| G6 | SG-6 | **survives**: `00315390` has exactly three call sites (`002536F4`, `0056F482`, `00583F2A`); `movzx eax, al` |
| G7 | SG-7 | **survives**: six `[rdi + 4]` resolves per pass, the first the loop-top count; `mov rbx, rax` / `add ebx, ecx` |
| G8 | §10 | **survives**: `movzx` of the `u16` threshold and `jge` at all three |
| G9 | §14 | **survives**: rungs 12 → 1 at 8 bytes from `00D1062D`; rung 1 is `{0, 0, 0}`; the fall-through stores 1 |

**Propagated:** §16 said the divergence is invisible on "the 45 rows whose last entry always passes". SG-2's
correction of 2026-09-25 (11 all-gated rows of 57) makes that 46. There is no new contradiction: the finding is OPUS
block 324's.
