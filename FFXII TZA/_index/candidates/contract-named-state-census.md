# Contract-named state with no declared type: a worklist for the `types` cell (OPUS, 2026-09-25)

Instrument: `gfz-scripts/contract_named_state_census.py` (read-only). Rows:
`contract-named-state-census.tsv`.

## Why

SWE2-AUDIT-SEM's accepted `types: MET` criterion (L2-VERDICTS.md, 2026-09-21) says:

- **the cell is MET when every piece of state the contract names has a declared type** with a
  measured extent;
- the declaration must be at the granularity the contract names the state;
- the denominator is the contract's Types and State sections, not the addresses in its invariant
  prose.

FABLE's per-cell census found `types` blocking 46 of the 51 NOT-MET rows. S-35 turned out to be
blocked by a single undeclared object (block 195). This census finds the remaining cases
mechanically. **It scores nothing.** Scoring is SWE2-AUDIT-SEM's job.

## Method

For every `CONTRACT-*.md`, the census takes each backticked `ADDR` or `[ADDR]` from:

- sections whose heading names **Types** or **State** (excluding "State transitions");
- the Interface section's rows that say "state" or "global".

It keeps addresses in `.data`/`.bss` and resolves each against the store's static routes, descending
into declared element types:

| class | meaning |
|---|---|
| **FIELD** | lands on a declared, named field |
| **GAP-SPAN** | inside a declared type but on an `unobservedSpan` row (precision 1: extent only) |
| **PTR-CELL** | a declared pointer cell |
| **UNDECLARED** | no route covers it |

`.rdata` addresses are reported as **CONSTANT**. Whether named constant tables count toward the
criterion is the scorer's call.

## Controls

**Positive:**

- `01E0C464` resolves to `FrameUpdateGateEnableWord.enableBits` (the S-02 statics, block 188).
- `022C256C` resolves to `SharedGameplayLcgState.state`.
- `01EF93E8` resolves to `PresentationBitFeedbackPrngState.state`.

**Negative:** before today's declarations, S-12's four published globals came back UNDECLARED, and
they now come back FIELD.

## Bound — what it cannot see

- ~~**Contracts without a Types/State heading are invisible to it.** 59 of the 107 contracts are
  like this.~~
  **Corrected 2026-09-25 (block 210):** only **10** contracts lack such a heading. The other ~48 have
  one but name no `.data`/`.bss` address, because their state lives in heap objects. The rule now
  also reads sections titled "The objects" / "The shared object" (in `CONTRACT-input-subsystem`,
  post-processing and Steam). That reach found six more cells, now declared.
- S-35's `CONTRACT-input-subsystem.md` is one of them (its state section is titled "The shared
  object"). That is why the S-35 gap was found by reading, not by this tool.
- **Addresses inside fenced code blocks are invisible to it**, because it matches backticked tokens.
  For example, `CONTRACT-native-command-lifecycle.md` names its family array `02B57EF0` only inside a
  fence. That array was found by reading and is declared (block 204).
- It reads the **working tree**, so a peer's uncommitted edit to a contract shows up in the counts.
  For example, the `02099DB4`/`02099DB8`/`02099DE8`/`02099DF0`/`02099FF0` weather rows come from
  SWE2-CONTRACT's uncommitted GB-3 note, not from the contract at HEAD.

## First pass result, and what was closed in this commit

200 addresses across 49 contracts:

| FIELD | UNDECLARED | PTR-CELL | GAP-SPAN | CONSTANT |
|--:|--:|--:|--:|--:|
| 90 | 79 | 8 | 2 | 21 |

**S-12 (weather)** is closed at HEAD except `[02ADD0B0]`, the MWeather root. The following were
declared from the image:

- **`WeatherEnvironmentClass` / `WeatherWindClass` / `WeatherLaneByte2Mirror` /
  `WeatherEnvironmentFlag`** — the four published dwords `02099DA8`/`DAC`/`DB0`/`DBC`.
  - Stores come from `0026D910`, and each has a 7-byte getter.
  - `DB0` has no reader.
- **`MapRefImageSlot`** (0x18 at `02099D88`) — the map_ref root, and its "loaded" guard.
  - The guard is *not* a bool. It is `root + *(int32*)(root+0x14)`, stored by the load-completion
    callback `002678A0`.
  - The type's extent comes from the loader's three-qword group clear.

**Also closed in this commit: three contract-named WorldAreaField pointer cells.** Each is declared
with the store's `FieldRecordTable` convention, where the pointed-to authored image is the type and
the cell is its `PTR` route:

- **`AuthoredIdListImage`**, behind `[02ADD0D0]` (`mapjumpgroupinit.bin`) and `[02ADD0A8]`
  (`eventmemorylist.bin`). It has one shape: a `u16` count at `+8` and `u16` ids from `+0xA`.
  `00379160` and `00377440` read it identically.
- **`MWeatherTableImage`**, behind `[02ADD0B0]` (`gramap_weatherinfo.bin`). It has a `u16`
  selector count at `+6` and a bitstream from `+8` that `003777C0` reads MSB-first.

S-12 and the persistent-flag-banks contract are now clean at HEAD. The census reads 76 UNDECLARED.
The rest of the `02ADD090`… region is WorldAreaField module state with many writers, and no
contract names it as a block, so no block type is declared for it.

**Next:** The largest remaining clusters are `CONTRACT-widget-object` (11), `CONTRACT-native-command-lifecycle`
(5) and `CONTRACT-world-loot-pickup-pool` (5).

## Final status of this pass (OPUS, 2026-09-25, blocks 201-208)

**79 → 9 UNDECLARED**, over 200 addresses in 49 contracts: FIELD 157, PTR-CELL 11, GAP-SPAN 2,
CONSTANT 21. The nine that remain are all explained, and none is fixable by a declaration:

| rows | why |
|---|---|
| `02099DA0`/`DB4`/`DB8`/`DE8`/`DF0`/`FF0` (weather) | named only in SWE2-CONTRACT's **uncommitted** GB-3 note, and not state of weather (other writers). At HEAD, weather's named state is fully declared |
| `02AEE4C8` (widget-object) | named only in a peer's **uncommitted** edit |
| `01F80544` (binding-profiles) | a **range end**: the published-profile bank `01F80130` (3 × 0x15C) ends exactly there. It is not state |
| `0208DE94` (periodic-tick) | **open**, see below |

**The open question.** Bank B of `PeriodicTickRecord` (`0208DE94`) is indexed by battle slot
(0–31; `BattleUnitSlotCount` = 0x20). 32 × 0x40 from `0208DE94` would overrun the `0208E680`
pool-control cluster by one record. Either slot 31 is never ticked, or the layout differs from
what is read here. Declaring a count would be a guess, so it is left open.

**Found along the way:**

- the text painter is static, not a heap singleton (`PROPOSED-OPUS-S37-2` answered);
- the flag cells my own ruling had left typeless are now declared;
- `InputBindingRecord` has a fourth bank;
- `ScriptNativeDispatchRecord` extended to all five command tables;
- `VmValueStack` routed to its static instance;
- the developer-tuning table's `{ptr, k+1}` pattern runs for 1,314 entries, against the
  contract's 294, which is routed to that contract's owner.

## Widened pass (OPUS, block 210)

217 addresses in 52 contracts: FIELD 170, PTR-CELL 13, GAP-SPAN 2, CONSTANT 21, **UNDECLARED 11**. All
eleven are explained:

- **Seven come from peers' uncommitted edits:** six in weather, one in widget-object.
- **Three are range ends:**
  - `02F9739C`, the snapshot's end;
  - `01F80544`, the profile bank's end;
  - `01DFC088`, which my block-209 correction cites as where the tuning table ends.
- **One is the open overrun:** periodic bank B, `0208DE94`.

**Declared in this pass:**

- `PostProcessingLibraryWrapper` (`PTR 02D38540`);
- `PostEffectLibraryInstanceCell`;
- `TextureUtilSingletonCell`;
- `SteamApiContextInitHeader`: only the measured 16 bytes. How the returned context relates to
  the block lives in `steam_api64.dll`.
- `SteamAchievementRecord`: 41 × 0x198, per FABLE's table, bound `0x29` at `0020CD5B`.

## The bank-B "overrun" was a base error (OPUS, block 211)

**Withdrawn.** `0208D494` and `0208DE94` are field `+0x14` of 64-byte records whose true bases,
`0208D480` and `0208DE80`, are each address-taken by the same 16 battle-runtime functions.
`00386860` alone takes the field address. With the true bases the two banks tile exactly:

- 40 records at `0208D480` run to `0208DE80`;
- 32 records at `0208DE80` (= `BattleUnitSlotCount`) run to `0208E680`, where the pool-control
  cells begin.

`PeriodicTickRecord` is replaced by `BattleRuntimeUnitRecord`. **The census now reads 10
UNDECLARED, all non-state or peer-uncommitted:** 7 peer rows and 3 range ends.

## A blind spot in the census itself: `0x`-prefixed addresses (OPUS, block 214)

**The address pattern matched only bare 8-hex cells.** Every contract that writes its state table as
`` `0x02091098` `` was invisible: CONTRACT-sound-request returned *no rows at all*. That is a blind
spot, not an empty contract. With `(?:0x)?` added, the census reads **63 contracts / 249 addresses**
(it was 52 / 217) and **24 UNDECLARED** (it was 10). The 14 new ones are real state, all declared in
this block and each re-scanned image-wide:

- **S-41**:
  - `AudioRequestGate`;
  - `AudioPlaybackStateBlock` (0xC; the second gate is its `+0x06`);
  - `AudioBankSlotListHead` (int16; the list is chained through `AudioBankSlot +0x00`);
  - `AudioBankHandleArray` (3 × int32).

  **Measured against the contract:** the teardown `003A13F0` resets handle A twice and handle B
  **never**. The block whose callback is B's setter stores -1 to A. "All three reset" is
  contradicted by the bytes.
- **S-19**:
  - `MovementBody` (0x130 × 128; stride from `003DA8D8`, and the array tiles to `02B57CC0`);
  - `MovementBodyPoolControl` (0x18; free head at `+0x04`).
- **S-05** (no bound check anywhere):
  - `TransformWorkbenchSavedValue` (32 × 0x10);
  - `TransformWorkbenchSavedPointer` (32 × 8);
  - `TransformWorkbenchSaveDepth`.

  The capacity is the layout. All nine callers push 1 or 2.
- **S-42** (from the contract's code fence, which the census also cannot see):
  - `MusicTable`: a resource whose page words are table-relative on disk and rebased to absolute by
    `003EAB90`;
  - `MusicRun` (unaligned);
  - `MusicLadderEntry`.
- **S-44**:
  - `GameSettingKeyName` (31);
  - `GameSettingValueNameRow` (31 × 9 `char*`). Row 0 uses all nine slots, so rows are **not**
    always NULL-terminated.

**Now: 10 UNDECLARED, the same ten already explained** (7 in peers' uncommitted text, 3 range ends).
**Remaining bound, unchanged in kind:** names inside code fences and state named only by type are
not matched by this tool. A name check over type-like identifiers in state sections was run by hand
this session. It found the four S-49 types (block 213) and the S-42 structs; everything else it
flagged is declared under another name or is not state.

## Code fences read too (OPUS, block 215)

**Inside a ``` fence nothing is backticked, so fenced state was invisible.** For example,
`struct MusicTable { /* pointed to by *(void**)0x02B5E0D0 */`. Fenced lines in state sections now get a
bare-address pattern; `.text` addresses in asm listings fall below the data ranges and are dropped.
The result: **76 contracts / 303 addresses** (it was 63 / 249) and 16 new UNDECLARED, all resolved
this block:

- `BgmStream` (0x38, fixpoint census; the size follows from 8-byte alignment).
- `PageRecord022D94B0` (32 × 0x18, TW-6's record table; ends at the next referenced cell `022D97B0`).
- `WeaponRecipeRef` (109 image pointers; the qword after them is not a pointer).
- `ResourcePathNamespaceSlot` (46 slots; the filler `002DF9A0` writes each once).
- `Ff12Ar03Header` (0x30).
- The party focus handles and request kind.
- Three loot-chain cells.
- The gil contract's "game state" `*(void**)0x02092758`. It is the active `SaveImage` (`00253970`
  stores `SaveImage_GetActiveRuntimeBuffer()` = `02164280`), so the fix is a `PTR 0x02092758` route
  on `SaveImage`, not a new type.

Where adjacent globals are referenced by the same function family, the named cells are declared at
the widths the code uses. **Object boundaries in those runs are not claimed.**

**Known false positive:** `01020304` in the packed-namespace fence is the byte-order-mark value, not
an address. It is classed CONSTANT and has no effect.

**Now: 11 UNDECLARED.** These are the ten already explained plus `022D8F00`. That address is the
workbench area's START bound: nothing references `022D8F00..022D8F07`, `022D8F08` is
`TransformWorkbenchSaveDepth`, `022D8F0C` is an unnamed dword (00501820, 00502280), and
`022D8F10` begins `EeVu0RegisterBank`.

## The widget consumer (OPUS, block 216)

`02AEE4C8` is now declared as `WidgetConsumer02AEE4C8` (0x1D0), from the SECTION-04 owner review
(`section04-owner-review.md`). **Census: 10 UNDECLARED:**

- SWE2-CONTRACT's six uncommitted weather cells;
- three range ends: `02F9739C`, `01F80544`, `01DFC088`;
- the workbench start bound, `022D8F00`.

## Range bounds classified; zero UNDECLARED (OPUS, block 219)

**Range bounds are now their own classes**, following SWE2-AUDIT-SEM's review of this tool (caveat 1).
A range written `A`..`B` or `A`–`B` names a region, not state at its endpoints:

- An undeclared **end** is `RANGE-END`.
- An undeclared **start** is `RANGE-START` only when at least 90% of `[A, B)` is already declared.
  Otherwise it stays UNDECLARED, because the region itself could be the undeclared state.

**Declared this block:**

- **Both script scratch banks,** `FieldScratchBank` and `GroupPersistentBank`: 0x200 each, bounded by
  each other and by `0209A1F0`.
- **`MirrorBlockBytes02099DA0`.** This corrects the reading of `02099DA0` as a bare bound: a
  byte-stride scan shows all eight bytes `02099DA0..DA7` independently referenced (5–9 refs each).
- **The tuning table's end.** My contract now writes it end-exclusive (`01DF6E68`..`01DFC088`).

**Result: 77 contracts / 303 addresses. FIELD 247, PTR-CELL 19, GAP-SPAN 2, CONSTANT 31,
RANGE-END 3, RANGE-START 1 (`022D8F00`, 98.2% declared), UNDECLARED 0.**
