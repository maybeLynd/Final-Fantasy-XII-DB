---
contract: Fetch an area's `.ard` by namespace and index, and bind its sections into the battle registry
category: 02-Resource-And-Asset-Pipeline
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md
entries: ["00264ED0", "003EA6E0", "003EA820", "003EA710", "002DF980"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's invariants re-measured from
    the shipping bytes — the resolver read in full, the namespace constant and the doubled index read
    at their instructions, and the category-setter calls counted in both the loader and the binder.
    **This records checks performed on that date, not the method of the original derivation**, which
    is on the loader page and carries its own falsification pass and independent audit; see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-ard-binder-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — the `.ard` area binder

> **Authored 2026-09-22 by FABLE.** S-09's binding gap named three things and said one was
> contracted. [`CONTRACT-resource-section-addressing.md`](CONTRACT-resource-section-addressing.md)
> (commit `234a410df`) took section addressing; **this takes the `.ard` binder**, so the row's gap is
> discharged without waiting on a ruling about partial coverage.
>
> Written against FRONTIER's adequacy test: *a narrower contract is adequate exactly when the
> system's operations have no cross-operation invariant or ordering it leaves unstated.* §4 is seven
> such invariants, and the last is an ownership fact about five registry slots written from two
> different bodies.

## 1. Purpose

Get the current area's authored battle data into the five registry slots the battle systems read.

## 2. Interface

| | body | size |
|---|---|---:|
| field id → area index | `MapRef_GetAreaArdFieldResourceIndex` (`00264ED0`) | 49 B |
| refresh, skipping if already loaded | `AreaArd_RefreshForMapRefField` (`003EA6E0`) | 43 B |
| **the reader** | `AreaArd_LoadOrUnloadFieldResource` (`003EA820`) | 476 B |
| **the binder** (read-completion callback) | `AreaArd_BindLoadedRootAndBattleSections` (`003EA710`) | 267 B |
| path resolver | `002DF980` | **22 B** |

## 3. Types

```
Ff12Ar03Header   (file base, 0x30 bytes)
  +0x00  char[8]  'FF12AR03'      never read by the loader
  +0x0C  u32      trailer offset   read by 003EA650, NOT by the loader
  +0x10 .. +0x2C  u32[8]           the slot directory — 0 means absent (AB-5)

path tables: a table-of-tables at 0215F000; namespace 21 is 0215F0A8
```

## 4. Preconditions · postconditions · invariants

### The seven cross-operation invariants

**AB-1 — `.ard` is never opened by name; it is `(namespace 21, index 2 × areaIndex)`.** Read at the
instructions: `003EA840 mov ecx, 0x15` is the namespace (21), and `003EA845 lea esi, [r14 + r14]`
is the doubled area index. *The filename never enters the request.*

**AB-2 — The path resolver is 22 bytes and validates NOTHING.**

```asm
002DF980  movsxd rax, ecx                      ; namespace
002DF983  lea    r8,  [rip + 0x1e7f676]        ; the table-of-tables
002DF98A  movsxd rcx, edx                      ; index
002DF98D  mov    rax, qword ptr [r8 + rax*8]   ; table = pathTables[namespace]
002DF991  mov    rax, qword ptr [rax + rcx*8]  ; return table[index]
002DF995  ret
```

**Two dependent loads, no bounds check on either index and no null test on the intermediate table.**
*This is the same shape as section addressing's RA-4 in the sibling contract: the resource layer
does not fail closed, and a caller supplying a bad namespace gets a dereference rather than an
error.*

**AB-3 — The `.fpk` sibling is the odd index, so the "record" and the "array" are the same bytes.**
`003EA852 lea r8d, [rsi + 1]` requests `2i + 1`. **The path table is a flat `char*[]` at 8-byte
stride**; what a file-corpus reader sees as a 16-byte `{ardPath, fpkPath}` record is indices `2i` and
`2i+1` of one array. *Two descriptions, one allocation — and a reimplementation that builds records
will index them right and lay them out wrong.*

**AB-4 — The parity rule is proved from the arrays, not assumed from the arithmetic.** Both arrays
installable at namespace 21 begin with **24 NULL qwords**, so any head-only inspection sees nothing
and a walk stopping at the first NULL measures the distance to a hole. Walked in full: **215 `.ard`
at even indices and 215 `.fpk` at odd, in each array, with zero crossovers either way**, and all 430
`.ard` strings in the executable reachable at even indices. *This is the loader page's measurement,
re-taken there within a derived extent after an arbitrary scan window had got it wrong — **where an
array ends is not observable from the array**.*

**AB-5 — The header is an eight-slot directory, and `slot0` is always `0x30` for a structural
reason.** `+0x10`..`+0x2C`, `0` means absent, and slots 3 and 4 are empty in all 166 areas. `slot0`
is `0x30` in all 166 because **it is simultaneously the first block's offset and the header's
length** — the directory ends where the first block begins. *Numbering only the six fields the loader
reads hides that slots 3 and 4 exist; the page carries that correction and this contract keeps the
directory numbering.*

**AB-6 — The directory holds IMAGE ADDRESSES, not plain offsets**, which is why the binder resolves
each one through `ImageAddress_ResolveRuntimePointer` before use — nine such calls in `003EA710`,
interleaved with its category writes.

~~**AB-7 — The same five registry categories are written from TWO bodies, and only one of them resolves first.** The binder `003EA710` calls `BattleData_SetAreaArdSectionCategory` **five times**, each after resolving an image address (AB-6). The reader `003EA820` calls the same setter **ten times, in two groups of five** (`003EA8AD`–`003EA8D5` and `003EA8E5`–`003EA90D`), around two calls to `003DCF00`, **without resolving anything** — it is `LoadOrUnload`, and the two groups are the two directions. *So the five slots have two writers with different preconditions, and an implementation that puts the binding only in the completion callback will never clear them.*~~

> **CORRECTED 2026-09-25 (FABLE, Claude Opus 5.5), on SWE2-AUDIT-SEM's return of this contract (2026-09-22): the census above was false.** Re-derived from the image, the corrected invariant follows. The struck text is kept as history.

**AB-7 — The five registry categories have one setter and three clearers, and only the setter resolves anything.**
- **The binder `003EA710`** (the read's completion callback) resolves nine image addresses (AB-6). It sets categories **0, 1, 2** unconditionally from directory entries `+0x10`, `+0x14`, `+0x18` (`003EA76A`–`003EA784`). It sets categories **3 and 4** from `+0x24` / `+0x28` **only when that entry resolves non-zero, and to 0 otherwise** (`003EA7AD`–`003EA7FA`). It hands `slot7` (`+0x2C`, or 0) to `003DCF00`, then records the file buffer at `02B5E0C0`.
- **The reader `AreaArd_LoadOrUnloadFieldResource` `003EA820`** never sets a category. It makes **15** calls, in **three groups of five, every one `(N, 0)`**:
  1. on a load when a previous buffer exists: free it, reset `02B5E0C0` / `02B5E0B8`, call `003DCF00`, clear (`003EA8AD`–`003EA8D5`);
  2. on **every** load: `003DCF00(0)`, clear (`003EA8E5`–`003EA90D`), then allocate and submit the read with the binder as its completion;
  3. on an unload (no file, size ≤ 0) when a buffer exists: free, reset, `003DCF00`, clear (`003EA9B7`–`003EA9DF`).
- **So every load clears all five before the read is even submitted, and a reload clears them twice.** Between the clear and the completion, the categories read as 0.
- An implementation that binds only in the completion callback leaves stale pointers in the unload case (group 3). One that binds on submit reads unloaded memory.

## 5. State

**Owned:** the five battle registry categories, set by the binder and cleared by the reader's three groups (AB-7, corrected 2026-09-25). **Read, never
written:** the path tables, the header directory, and the file's blocks. **Not read at all:** the
magic at `+0x00` and the trailer offset at `+0x0C` — the latter has a reader elsewhere (`003EA650`)
but not on this path.

## 6. Relationships

| | |
|---|---|
| **Sibling** | [`CONTRACT-resource-section-addressing.md`](CONTRACT-resource-section-addressing.md) — S-09's other half, sharing AB-2's does-not-fail-closed shape |
| **Sibling** | [`CONTRACT-authored-table-row-lookup.md`](CONTRACT-authored-table-row-lookup.md) — what reads the rows once bound |
| **Downstream** | the battle systems that read the five categories |

## 7. State transitions

*field id → area index (`00264ED0`) → refresh, skipped if loaded and not forced (`003EA6E0`) →
size and read request at `(21, 2i)` with the sibling at `2i+1` → completion → bind (AB-6, AB-7).*
~~Unload runs the second group of AB-7's setters in the reader itself.~~ Every load clears the five categories (group 2) before submitting, a reload also runs group 1, and an unload runs group 3 (AB-7, corrected 2026-09-25).

## 8. Script · resource · event interactions

The `.ard` files and the path tables are authored; the path table installed at namespace 21 is chosen
**per locale** by a `switch` on locale id, so which of the two arrays is live is a locale fact.

## 9. Determinism

Deterministic given the area index and the locale. No generator is drawn.

## 10. Failure paths and edge conditions

- A bad namespace or index is **not** detected (AB-2).
- A directory slot of `0` means the section is absent; slots 3 and 4 are always `0`.
- `AreaArd_RefreshForMapRefField` skips entirely when the area is already loaded and the force flag
  is clear — so a stale binding persists until something forces it.

## 11. Observable behaviour

Walking into a new area replaces the authored battle data for that area; walking back into one
already loaded replaces nothing.

## 12. Reproduction formula

Assert the request is `(21, 2i)` and the sibling `(21, 2i+1)` for a known area index. Walk the
namespace-21 array in full and assert 215 `.ard` at even indices and zero at odd (AB-4) — **not from
the head, which is 24 NULLs**. Count the category-setter calls in both bodies and assert five and ten
(AB-7).

## 13. Runtime validation

**S-09's row records live placement proven**, and that evidence is the loader page's; none of it is
re-claimed here, and no experiment executes these five bodies. *Stated rather than left blank so a
CONTRACT READY header is not read as evidence of execution of this contract's own bodies.*

## 14. Unresolved

- ~~What the trailer at `+0x0C` holds, given the loader never reads it.~~ **Answered 2026-09-27 (OPUS, `CC-5`);
  carried here (FABLE, Claude Opus 5.5, 2026-09-26, on OPUS-REQ-FABLE-ARD-TRAILER-READ-BY-NOTHING-PROSE):** `{u32 count; {u32 key; u32 mask}[count]}`, read through the root accessor by the
  per-name flag-mask walkers rather than by the loader; the `CC-5` row of [the register](../_index/OPEN-QUESTIONS.md).
- ~~What `003DCF00` does between AB-7's two groups, and what `slot7` — the one non-battle slot — feeds
  it.~~ **Answered 2026-09-25 (FABLE, Claude Opus 5.5):** `003DCF00` is `mov [02B58178], rcx; ret`. `02B58178` is one of the three runtime motion-index tables (`{u32 model, u16 class, u16 motion, u16 index}` rows) that `003DCA30` consults to choose a `.ca` motion file ([the table registry page](authored-data-table-registry.md), `02EBF178` neighbourhood). So `slot7` is the area's class-keyed motion index. *Still open:* at `003EA8A4` and `003EA9AE` no instruction sets `rcx` after the preceding free call, so the value stored there depends on what `003697F0` leaves in `rcx`.
- Which caller sets the force flag the refresh's skip depends on (§10).

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| AB-1 — namespace and doubled index | `003EA840 mov ecx, 0x15` and `003EA845 lea esi, [r14 + r14]` read at their addresses | 1 |
| AB-2 — 22 bytes, no validation | the resolver disassembled in full; two dependent loads and a `ret` | 1 |
| AB-3 — the odd sibling | `003EA852 lea r8d, [rsi + 1]` | 1 |
| AB-6, AB-7 — one setter, three clearers | ~~**five** in `003EA710` … **ten in two groups of five** in `003EA820` with none~~ **Corrected 2026-09-25:** `003EA710` makes five setter calls: 0–2 unconditional, 3–4 conditional (0 when absent), with nine `ImageAddress_ResolveRuntimePointer`. `003EA820` makes **15**, all `(N, 0)`, in three groups on three branches, and three `003DCF00` calls | 1 |
| AB-4, AB-5 and the corpus figures | [the loader page](VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md), which carries its own falsification pass (2026-09-04) and an independent audit (2026-09-05) | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on AB-1 through AB-7. **AB-7 is the one to test
first**: putting the binding only in the completion callback is the natural design and leaves the
five slots uncleared on unload. *(Corrected AB-7:* the shipped reader also clears them on every load before submitting, so a test should check they read 0 between submit and completion.)

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **Resource — internal.** The reader, binder and resolver are this category's own.
- **CombatFormula / battle data — SERVICE.** `BattleData_SetAreaArdSectionCategory` is the sink AB-7
  is about; the dependency is this contract's subject and is stated in §4 and §6.
- **ActorEntity, Presentation, WorldAreaField — MECHANICAL, and their presence is AB-2's point.**
  Each appears only as another *caller of the 22-byte path resolver* `002DF980`. **That resolver is
  the engine's generic `(namespace, index)` lookup**, so its callers are everyone who loads anything
  — which is exactly why AB-2's absence of bounds checking is worth stating: it is not this
  subsystem's private helper.
- **Every other layer reached is MECHANICAL**, through the reader's own callees — the allocator, the
  resource read and the image-address resolver. *Their addresses beyond those named above are
  deliberately not cited: each is a hub, and naming one imports its whole edge set.*

## 17. Related

- [How the `.ard` loader binds area battle data](VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md) — the mechanism
- [Contract — resource section addressing](CONTRACT-resource-section-addressing.md) — S-09's other half
- [The authored-data table registry](authored-data-table-registry.md)

## Falsification pass 1 — 2026-09-29 (OPUS): every invariant survives, and AB-4 reproduces from the image

**Attack.** AB-1 to AB-4, AB-6, AB-7 (as corrected on 2026-09-25) and §2's sizes became checks. AB-4 was re-measured from the
two installed arrays, not carried. Script: `Tools/analysis-kit/gfz-scripts/falsify_ard_binder.py`, output
`falsify_ard_binder.out`, image `73461d08…`, 0 BROKEN, exit 0. AB-5 is a file-corpus fact and is carried from the loader
page.

| # | Clause attacked | Result |
|---|---|---|
| D0 | §2 | **survives**: 49 / 43 / 476 / 267 / 22 B |
| D1 | AB-1 | **survives**: `mov ecx, 0x15`, `lea esi, [r14 + r14]`; the size query and the request both use `(21, 2i)` |
| D2 | AB-2 | **survives**: exactly the six quoted instructions |
| D3 | AB-3 | **survives**: `lea r8d, [rsi + 1]` into `0032EB40` |
| D4 | AB-4 | **survives, re-measured**: the only stores to `0215F0A8` are `002DFA9E` → `01EDC280` and `002DFE66` → `01E0CFA0`; in 642 slots each array starts at index 24 with 215 `.ard` even and 215 `.fpk` odd and no crossover; all 430 `.ard` strings in `.rdata` are reached |
| D5 | AB-6 | **survives**: nine resolves in the binder |
| D6 | AB-7 as corrected | **survives**: five setter calls in the binder (3 and 4 set to 0 on a null resolve); fifteen `(N, 0)` clears in three groups in the reader |

No correction.

## Cross-subsystem neighbours — pass 22 (FABLE, 2026-09-29)

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page. Section 16a's heading is numbered, so the crossings gate does not read it; this section names each edge.*

**ActorEntity — CLIENT, MECHANICAL (2 edges).** `ActorResource_BeginManagerResourceSetLoad` (`0032FCA0`) calls the 22-byte path resolver `002DF980`, and `ActorResource_BeginPrimaryPayloadLoad` (`00330310`) calls the read request `0032EB40` - the same request the reader `003EA820` submits with the `.fpk` sibling index (AB-3). The actor layer's resource loads use the engine's generic `(namespace, index)` lookup and read submission; nothing of the `.ard` binding reaches them.

**Presentation — CLIENT, MECHANICAL (1 edge).** `001BB2B0`, the character asset-header path builder (it formats `./GameData/%s/ArtData/chr/%s_%s.ah`), calls the path resolver `002DF980`. It is one more caller of AB-2's unchecked lookup, which is why AB-2 treats the resolver as shared machinery rather than this contract's helper.

**WorldAreaField — SERVICE and CLIENT, mostly internal (14 edges).** Four of this contract's own bodies are filed to that layer, so eleven edges are the contract calling itself: `AreaArd_RefreshForMapRefField` (`003EA6E0`) calls `MapRef_GetAreaArdFieldResourceIndex` (`00264ED0`) and `AreaArd_LoadOrUnloadFieldResource` (`003EA820`); `003EA820` and `AreaArd_BindLoadedRootAndBattleSections` (`003EA710`) call `BattleData_SetAreaArdSectionCategory` (`0023A160`) and `003DCF00`, an 8-byte body that stores its argument into the motion-index table pointer `02B58178` (the `.ard` slot 7 of AB-7); `003EA820` calls the read request `0032EB40`. From outside the contract, `WorldSimulation_ProcessDeferredModeRequest` (`0032FC30`) calls the refresh `003EA6E0`; `003EA6B0`, a 43-byte reset that sets `02B5E0B8` to -1, zeroes the buffer record at `02B5E0C0` and calls `003DCF00` with 0, is the third caller of that store; and the map-name setter `00379A10` calls the path resolver `002DF980`. The binder is filed to the world layer although this contract sits in the resource folder, so the edges are its own call chain plus the world simulation's deferred mode request that starts a refresh and one more world-side user of the resolver.
