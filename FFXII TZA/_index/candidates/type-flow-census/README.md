# A per-type flow-aware census, and CPostEffect's resolvable spans re-cut (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

**The instrument.** `type_flow_census.py` generalises the CharacterRenderRecord census (`crr-flow-census/`, 218a9de09) to
any record type, seeded by pointer cells, function entries or a pool.
- It is a must-analysis per function, over the control-flow graph.
- It tracks record + k in registers.
- Argument seeds are propagated to a fixpoint.
- Every `[base + disp]` operand is recorded, with its width and whether it is a read or a write.

**Limits:** it does not follow memory-loaded pointers other than the configured cells, stack spills, or return values.

**CPostEffect.** The seeds are the cell `02EA0B70` and constructor `006FF5D0`'s argument 0, with size `0xD40`.
- The census finds 3,521 accesses in 160 functions, all inside the object.
- It reaches 187 of the 217 DISCOVERED spans. The earlier receiver-fixpoint census had called these "overlapping widths
  … NOT resolved".

**The re-cut** (`cpe_recut.py`, derivation shared by the patch and the check). A span is cut only when all of these hold:
- the census's reads (width ≤ 8) tile the span exactly, without overlap;
- every other access that touches the span starts and ends on those boundaries, so a wider store is a pair or block
  store over whole fields, or else is a 16-byte move;
- each field's type is consistent across its reads (`movss` family → float, `movsx`/`movsxd` → signed).

**Result:**
- 99 spans (758 bytes) become 212 rows: 115 float, 53 uint32, 38 uint8, 6 uint64.
- Every new row cites its read sites and any wider store. What each field holds is not claimed.
- The old row is kept in each new row's evidence cell.
- The remaining 118 DISCOVERED spans stay as they were: reads overlap, reads cover only part of the span, writes only,
  or no access found.

**Check** (`cpe_recut_check.py`):
- P1 positive control: the known glareParam0 readers at `+0x6E4` are found, and every field is in range.
- R1: every re-cut row equals the derived layout.
- S: no re-cut offset is still DISCOVERED.

**Run receipt:**
- FAILS 2 (R1, S) on the store before the re-cut.
- FAILS 0 after it, tested on a copy (2026-09-27).
- `types_index --validate` on the copy: 0 errors, 0 gaps.

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` CPostEffect, 99 DISCOVERED spans | re-cut into 212 read-side rows; the old rows are kept in the evidence cells | revised-here |
| CPostEffect's named rows (FABLE's S-40 glare ruling) | untouched | agrees |

## Nine more types (OPUS, 2026-09-27)

**The census now takes two more seed kinds.** Both are in `type_flow_census.py`:
- `STATIC=ADDR`: an image static. Every rip-relative operand inside `[ADDR, ADDR+TYPE_SIZE)` is a field access, and a
  `lea` gives base + k.
- `GETTERS=FUNC,..`: a singleton accessor. A call to one of these functions leaves base + 0 in `rax`.

**Generic tools:**
- `recut.py` generalises `cpe_recut.py`. It provides `run_census`, `spans_of(fields, TYPE)` and the same `derive`
  rule.
- `recut_check.py TYPE KEY=VAL...` runs:
  - P1, a positive control: the census hits at least min(5, all) of the type's already-declared rows, and at least 95%
    of the recorded fields fall inside the object. A seed that does not reach the object FAILS here.
  - R1, the layout match.
  - S, no re-cut offset left DISCOVERED.

  It writes `flow-<TYPE>.tsv`.
- The patch is `Tools/work/OPUS/recut/patch.py TYPE CENSUS_TSV KEY=VAL...`. It keeps a span's old name when the span
  resolves to a single field of its own width.
- Every new row is marked `FLOW RE-CUT 2026-09-27` and carries `WAS SPAN 0x.. n name` in its evidence.

| type | seeds | spans → rows (bytes) | P1 declared rows hit |
|---|---|---|---|
| Vu1RegisterBank02064B00 | STATIC 02064B00 | 17 → 35 (124) | 4 of 4 |
| ManagerSingleton0209BE80 | CELLS 0209BE80 | 11 → 11 (48) | 28 of 39 |
| LegacyPs2GsTextureContext | CELLS 0209A670 | 3 → 3 (20) | 11 of 33 |
| GlyphRunWidget1498 | CELLS 02CA8A80 | 2 → 2 (6) | 13 of 32 |
| ShadowSettings01F82EA8 | CELLS 01F82EA8, 01F812C8; GETTERS 001F0850 | 5 → 10 (44) | 15 of 15 |
| BootSingleton01F7F598 | CELLS 01F7F598; GETTERS 00189120 | 6 → 7 (28) | 39 of 50 |
| MapPackSlotPointers02ADCFE0 | STATIC 02ADCFE0 | 5 → 5 (40) | 11 of 11 |
| MapPackBindState02ADD0D8 | STATIC 02ADD0D8 | 8 → 8 (23) | 2 of 2 |
| HandleSlotListState02B404C0 | STATIC 02B404C0 | 1 → 1 (1) | 5 of 5 |

In total, 58 spans (334 bytes) become 82 rows. Width and type come from the read side. What each field holds is not
claimed.

**Held out, with the reason:**
- **BootSingleton01F7F598 with the cell alone** hit 1 of 50 declared rows, so P1 FAILS. The singleton is read through
  its accessor `00189120`; with that getter the census hits 39 of 50.
- **SummonEffectState02B40508** has no declared row to act as a positive control.
- **RampChannelRecord** has accesses outside the 0xE0 record, so it is an array. *(2026-09-28: re-cut separately with a pool seed, the allocator's walk and the two unlisted setters - `../ramp-channel-recut/`.)*
- **PpfxInitDescriptor**: CPostEffect's cell `02EA0B70` is not its seed.
- **DeveloperConsoleSettings01F81428**: with its getter `001D50D0` it resolves no span.
- **Manager0209AC60, BattleUnit, PApplication and EeVu0RegisterBank**: the census resolves nothing for them.

**Run receipt:**
- Each type FAILS R1/S on the store before its re-cut (P1 PASS).
- FAILS 0 on a scratch copy after the re-cut.
- The same check re-run on the live store after the apply.
- `check_census_widths` then found one new disagreement: BootSingleton `+0xDA0`, declared 4, against the constructor's
  8-wide `mov qword ptr [rdi + 0xda0], rsi` (`00185019`). The flow census does not reach the constructor. That store is
  a pair store over the two new 4-byte fields `+0xDA0` and `+0xDA4`, which the re-cut rule allows. The two rows cite it,
  and `+0xDA0` carries the checker's `WIDTH DELIBERATE` exemption with that reason. The checker is back to its 3
  pre-existing mismatches.
- **Limit, stated:** a store the flow census does not reach is checked only where a type has a registered census. Of
  these nine types, only BootSingleton has one.
- Also re-run after the tool change: `cpe_recut_check.py` passes with FAILS 0, and its `cpe-flow-accesses.tsv` is
  byte-identical.

## Tail calls (OPUS, 2026-09-27, later)

**The gap.** A `jmp` to another function's entry is a tail call, and its callee receives the caller's argument
registers. The census treated it as the end of the block, so a record handed on through a thunk was lost. Found on
CharacterRenderRecord `+0x68C`, whose read is reached only through such a thunk:
- `003E5810` does `lea r8, [rbx + 0x680]` and calls `0046D0C0`;
- `0046D0C0` is `jmp 00202B70`;
- `00202B70` calls `00217060`, which reads `[r8 + 0xC]` as a float.

**The change.** `type_flow_census.py` now adds argument seeds at such a `jmp`, exactly as it does at a `call`.

**Re-run of every dependent check with the changed tool:**
- `cpe_recut_check.py`: FAILS 0. The census grows from 3,521 to 3,692 rows, and the 212 re-cut rows still match.
- The nine types' `recut_check.py`: FAILS 0 each.
- CharacterRenderRecord: 2,889 → 3,213 accesses.

**Result for CharacterRenderRecord, under the read-side rule:**
- One span re-cuts: `+0x68C`, a float. It is named `auxTransform2Lane3` by position, beside lanes 0–2 of the `+0x680`
  vec4, with the chain cited.
- `embeddedBlock0650` gains three dword stores in `00512F30`, reached with `rec + 0x650` through the stub `003E6B50` and
  from `003E6C8A`. Reads cover only its `+8`, so it stays DISCOVERED with the stores cited.
- The `+0x610` / `+0x620` hits are 16-byte block copies. They are carried, not cut.

**Tried and not adopted:** return-value propagation (a function whose every `ret` carries base + k). For
CharacterRenderRecord it found 3 getters and 9 accesses, and no span it would resolve.

## Interior sub-objects, and receipts that review runs cannot overwrite (OPUS, 2026-09-27, later)

**`SHIFT=N`.** Several DISCOVERED-heavy types are interior sub-objects of a type that already has a census: the
ManagerSingleton0209BE80 interiors at `+0x57E0` / `+0x8FA0` / `+0xAB30`, and PpfxInitDescriptor at CPostEffect `+0x210`.
With `SHIFT`, every seed names the PARENT and gives base − N, so fields come out relative to the sub-object. Under
`SHIFT`, `recut_check` P1 rests on the declared-row hits alone: the parent's other fields fall outside the sub-object by
design, so the range test is void there. Negative fields are written as `-0x…`.

**Receipts.**
- `recut_check.py` and `cpe_recut_check.py` now write their census to a temporary file by default. They write the
  tracked `flow-<TYPE>.tsv` / `cpe-flow-accesses.tsv` only with `--receipt`.
- **Why.** Between a check and a commit (8eb8957c2), a review re-run rewrote receipts in the shared tree.
  HandleSlotListState's committed receipt had 268 rows, although the tool and that very check produce 36 (the check had
  printed "36 of 36 fields in range"). The store rows were never affected, because R1 re-derives the layout from a
  fresh census and not from the file. Every receipt was regenerated and compared (see the commit that carries this
  note), and the wrong ones are replaced.
- **Rule:** reviewers run the checks without `--receipt`.

**Tried and held out (2026-09-27, later), each by its own P1:**
- **MapScreenPage.** Seeds CELLS 0209E5C0, 0209E5F0 and 02B47760 with SHIFT 0x1B0 hit 1 of 6 declared rows. Pages are
  reached through page pointers, not the containers' cells.
- **BattleMenuChildWidget1620.** Seed CELLS 0209BE80 with SHIFT 0xAF00, the nesting path the types table gives, hits 0
  of 10.
- **Manager0209AC60.** Seeds STATIC plus CELLS 0209AC30 reach it (136 of 181), but no span tiles.

**The census cache is now a bounded LRU.** Pass 1 disassembles every body, and an unbounded cache of detailed
instructions grew past 9 GB on the wider seeds. Output is unchanged: HandleSlotListState and CharacterRenderRecord
regenerate byte-identical.

**BattleUnit (2026-09-27).** Nothing in the image indexes the pool inline: the only `imul …, 0xF50` sits inside the
accessor `BattleUnit_GetBySlotIndex` `00236820`, which returns the pointer. So the census reaches the record only
through its accessors, passed as GETTERS: `00236820`, `00263E30` / `0031B760` (the actor record's `+0x30`), and
`002367A0`, `0031B770`, `0031B7E0`, `0031B860`, `00321170` and `003272A0`. Each was checked to return through the pool
formation or through a call to one of the first three.
- P1 hits 137 of 146 declared rows, and 1,853 of 1,854 fields are in range.
- Result: one span re-cut, `+0x154` uint32 (`00312AC5`, whose receiver is compared against a BattleUnit returned by
  `0031B7E0`).
- The other 30 DISCOVERED spans (401 bytes) have no tiling reads although the record is well reached. That bounds
  BattleUnit's residue.

## Static record arrays: `ARRAYS=ADDR:COUNT[,..]` (OPUS, 2026-09-27)

**What the seed does.** A rip-relative operand inside `[ADDR, ADDR + COUNT·TYPE_SIZE)` is field `(t − ADDR) mod
TYPE_SIZE`. A `lea` of the base gives a token that counts as 0 for field accesses and as the pool base for index
formation. Only when ARRAYS is set, `[base + index + disp]` on a pool/scaled pair is also recorded. Without ARRAYS, the
output is byte-identical to before.

**Result: no store change.** Sixteen ARRAY-declared types were run (dry run; `recut_check` P1 decides whether the seed
reaches the record).

Reached, with **no span that tiles**, so the DISCOVERED residue has no read-side cut:

| type | declared rows hit |
|---|---|
| MovementBody | 48 of 48 |
| ActorManagerSlot | 45 of 58 |
| UnitStatusView | 35 of 36 |
| ItemClassDescriptor | 12 of 12 |
| PartyFormationSlot | 8 of 8 |
| WorldLootPickupNode | 5 of 7 |
| WorldLootPresenceRecord | 2 of 2 |
| InputBindingRecord | 2 of 2 |
| SpawnGroupLedger | 3 of 3 (range test 12 of 21) |

**Not reached through the array**, by P1 — the array is not their main access route:
- BattleRuntimeUnitRecord: 2 of 9;
- ChunkedSlotBankEntry: 1 of 4;
- PageRecord022D94B0: 2 of 4;
- NameBindingEntry: 6 of 17;
- ChunkedSlotEntry: 1 of 3;
- SteamAchievementRecord: 1 of 5;
- InventoryCategoryListDescriptor: 1 of 2.

**Also run, no store change (2026-09-27):**
- **EeVu0RegisterBank** (STATIC 022D8F10): 58 of 60 declared rows and 16,136 fields reached, no span tiles.
- **PApplication** (STATIC 01F7E350 plus CELLS 02EA5368): 73 of 76 reached, no span tiles.
- **EncodedIdQueryRecord** (its two statics given as single-element ARRAYS): 4 of 14, not reached through the statics.

**Across all the well-reached types above, the DISCOVERED residue has no read that tiles it.** What remains in them
is bytes that are written-only, carried or untouched. That is a bound on the residue, not a meaning.

## Declared type against the read instruction family: `typing_check.py` (OPUS, 2026-09-27)

**What it checks.** For every type with a receipt, it takes each non-DISCOVERED 4-byte row and the census reads
starting at that offset.

**T1, a regression.** No row declared as a non-float scalar may be read ONLY by scalar-single float instructions,
counting at least two reads.

**What it found.** 45 CPostEffect rows failed. Their `uint32` came from the 2026-09-25 receiver-fixpoint census, which
typed by width alone. Every one of their reads is `movss` / `mulss` / other scalar-single float instructions; for
example `+0x5A8` is read 40 times, all `movss`. The rows are retyped to `float`, and each row's evidence keeps the old
type and the read count. T1 fails on the store before the retype and passes after it.

**Not judged:**
- a float copied only as bits through a general register;
- the CharacterRenderRecord 8-byte resource references read 4 bytes wide, which is the documented reference/displacement
  idiom.

## A re-cut that went stale: S2, and BootSingleton's second pass (OPUS, 2026-09-27, night)

**What went wrong.** BootSingleton01F7F598 was re-cut (4048f4980) before its `GETTERS=00189120` seed existed. The seeded
census that FLOW-RECUT-9's review ran later resolves five more DISCOVERED spans. `recut_check.py` still passed: its S
check covers only the offsets already re-cut, so a re-cut gone stale was invisible. `patch.py` refused a second pass,
because its guard was per type.

**The mechanism, closed.** `recut_check.py` gains **S2: no DISCOVERED span of the type is still re-cuttable by the
census**. It FAILS on the store before this change, naming `+0xCD4/1, +0xD10/1, +0xDB9/2, +0xDC4/2, +0xDC8/4`. The OPUS
work-area `patch.py` is now idempotent per span.

**The store.** The five spans become seven read-side rows (`+0xDB9` / `+0xDBA` and `+0xDC4` / `+0xDC5` split into
bytes). By hand, the constructor's 8-byte `ctorZeroQwordDBC` becomes:
- `+0xDBC` `accumulatorDBC` uint32: `add dword [rcx + 0xdbc]` at `00185A80`, read, copied to `+0xDC0` and reset at
  `00185D80` / `00187950`;
- `+0xDC0`: written only, so it stays DISCOVERED.

`+0xDB9`, `+0xDBC` and `+0xDC4` carry a WIDTH DELIBERATE reason: the registered census sees only the constructor's
pair stores.

**Sweep.** Every flow receipt beside this file was run through `derive`. Only BootSingleton had stale re-cuts.

**Run receipt.** Run verified at 6802d66d5:
- `recut_check.py BootSingleton01F7F598 CELLS=01F7F598 GETTERS=00189120 TYPE_SIZE=0xDD8`: P1, R1, S, S2 PASS, FAILS 0
  (S2 FAILS before the change);
- `types_index --validate`: 0 errors, 0 gaps;
- `check_census_widths`: 0 disagreements;
- `typing_check.py`: FAILS 0.

## Image statics swept; StickBasis022C7FA0 re-cut (OPUS, 2026-09-27, night)

**The sweep.** Four image statics were run through `STATIC` / `CELLS` seeds and `derive`:
- Manager0209AC60: 2,510 DISCOVERED bytes; 136 of 181 declared rows hit;
- TextPainter: 707 bytes; 22 of 26 hit;
- AppBootStatic01F7F480: 67 bytes; 48 of 48 hit;
- StickBasis022C7FA0.

Only StickBasis resolves anything. The other three's DISCOVERED spans are untouched by any access that tiles them.

**StickBasis022C7FA0.** Every row was DISCOVERED. Three are re-cut:
- `+0x0` state uint32;
- `+0x8` float08 float;
- `+0xC` float0C float, **retyped from int32 and renamed from dword0C**: both of its reads are `subss` / `addss`
  (`004744FC`, `00474563`), and the int32 came from a `mov dword 0` initialiser.

`+0x4` (written once, `0x12` at init) and the `+0x10` basis block stay DISCOVERED: the basis reads skip `+0x24` and
`+0x2C`, so they do not tile it.

**P1 generalised.** A type with no declared row has nothing else to hit, so P1 falls back to the store's row starts of
any status, still excluding rows this re-cut made. Before this, `recut_check.py` could not certify a type whose rows
were all DISCOVERED.

**Run receipt.** Run verified at 75be4d3b8:
- `recut_check.py StickBasis022C7FA0 STATIC=022C7FA0 TYPE_SIZE=0x30`: P1, R1, S, S2 PASS, FAILS 0 (R1, S and S2 fail
  before the change); its receipt is `flow-StickBasis022C7FA0.tsv`;
- the BootSingleton check still FAILS 0;
- `types_index --validate`: 0 errors, 0 gaps;
- `check_census_widths`: 0 disagreements;
- `typing_check.py`: FAILS 0.

## Seven more image statics re-cut; pointer ctypes kept (OPUS, 2026-09-27, late night)

**The sweep.** Every image-static type with DISCOVERED bytes and a stated address in `.data` / `.bss` was run through a
`STATIC=` census and `derive`: 26 types in all. Seven have spans the census now resolves, 12 rows in all:

| type | rows |
|---|---|
| EffectDrawListHeader02F8F2C0 | `+0x40` workBuffer, kept `u8*` |
| OwnedObjectPtr022C8058 | `+0x0` object, kept `void*` |
| PartyFocusOverrideCells022C7FEC | `+0x4` / `+0x8`, **retyped uint32 -> float and renamed dword4 / dword8 -> float4 / float8**: every read is a float instruction |
| PhyreClassDescriptor | `+0xF0` uint32 |
| RenderPassStateBytes022C7F98 | `+0x1` int8 |
| ScriptStepGates022C7F80 | `+0x0` uint32 |
| SummonEffectState02B40508 | `+0x2`, `+0x9`, `+0xA`, `+0x10` uint8 |

**Tool changes:**
- *Pointer ctypes kept.* A qword read cannot tell a pointer from an integer. The work-area `patch.py` keeps a declared
  pointer ctype where `derive` says uint64, and R1 accepts that pairing.
- *Renames follow the type.* A `dwordN` read only as float becomes `floatN`.
- *P1 for a type re-cut whole.* OwnedObjectPtr's one row is itself re-cut, so there is nothing else to hit. P1 then
  rests on the census reaching the object entirely in range.

**Run receipt.** Run verified at ba1cd9b8b:
- `recut_check.py` for each of the seven: P1, R1, S, S2 PASS, FAILS 0 (S2 FAILS on every one before); receipts
  `flow-<type>.tsv`;
- BootSingleton and StickBasis re-run FAILS 0;
- `types_index --validate`: 0 errors, 0 gaps;
- `check_census_widths`: 0 disagreements;
- `check_type_refs`: 0 dangling;
- `typing_check.py`: FAILS 0.

## Access labels from the shared policy (OPUS, 2026-09-27, OPUS-PUB-TFC-ACCESS-POLICY)

**Why.** [`access-flag-producers`](../access-flag-producers/README.md) (6b6a423db) moved four producers from capstone
5.0.7's raw operand flags to `reg_tracking.op_kind`. It reported this census as a fifth reader of raw flags, and
CPostEffect's `006FF784` came from it. This section is that repair, measured.

**The change** is in `type_flow_census.py`:
- memory operands are labelled by `_acc()`, which maps `RT.op_kind(ins, op, oi)`: `r`, `w`, `rw` becomes `wr`, `addr`
  is left to the caller's `lea` path, and `?` stays `?`;
- `nop` and `prefetch*` carry no memory operand;
- `reg_tracking` is imported from `Tools/analysis-kit/gfz-scripts`.

Nothing else changed: the seeds, the flow, the widths and the derive are the same.

**What moved in the receipts.** Every receipt was regenerated with `--receipt`, by the author:
- 2,007 `movups` stores changed from `r` to `w`;
- 20 `nop dword ptr [rax]` padding rows were dropped;
- nothing else changed, and 12 receipts are byte-identical.

| receipt | rows | changes |
|---|---|---|
| `flow-BattleUnit.tsv` | 1,854 -> 1,854 | `movups` r->w 40 |
| `flow-BootSingleton01F7F598.tsv` | 894 -> 894 | `movups` r->w 12 |
| `flow-CharacterRenderRecord.tsv` | 3,213 -> 3,212 | `nop` dropped 1, `movups` r->w 22 |
| `flow-ManagerSingleton0209BE80.tsv` and its three `SHIFT` interiors | 1,284 -> 1,281 each | `nop` dropped 3, `movups` r->w 10, each |
| `flow-PhyreClassDescriptor.tsv` | 146 -> 145 | `nop` dropped 1 |
| `flow-PpfxInitDescriptor.tsv` and `cpe-flow-accesses.tsv` | 3,692 -> 3,689 each | `nop` dropped 3, `movups` r->w 60, each |
| `flow-Vu1RegisterBank02064B00.tsv` | 26,545 -> 26,545 | `movups` r->w 1,773 |

**What that does to the store: nothing new to correct.** This was checked, not assumed.
- **The derive never saw a `movups`.** A re-cut field needs a read of width 8 or less, and every changed `movups` row is
  16 bytes wide.
- **Only two dropped `nop` sites are cited anywhere in `_types/fields.tsv`.** Of the 20 dropped rows (width 4), those
  two are the same site, `006FF784`: CPostEffect `+0x3B8` and its PpfxInitDescriptor alias `+0x1A8`. The CPostEffect
  row was already corrected in 6b6a423db. No PpfxInitDescriptor row exists at `+0x1A8`.
- **No row quotes a changed direction pair from these receipts.** For every row of these types, an `rN wN` pair
  recomputed at its offset from the old and new receipts was compared with the pairs the row quotes. Three
  CPostEffect rows (`+0x378`, `+0x388`, `+0x398`) quote `r2 w1`, which the old receipt also gives at those offsets.
  The quote sits in their WAS SPAN history, though: it was written by `census_receiver_fixpoint` on 2026-09-25 from a
  different site set. Their live text ("read ... at 1 site; also written inside a wider pair / block store") is right
  under the new labels.
- **CPostEffect `+0x7D8` (`mixed7D8`) is unchanged.** Its dropped `nop` (`0070FF23`) leaves only 8-byte writes there,
  and the census still has no read to type it from. Its row cites the other producer.

**Run receipt.** Run verified at 46b96cdae:
- all 23 recorded `recut_check.py` invocations FAILS 0, with and without `--receipt`;
- `cpe_recut_check.py --receipt` FAILS 0 (3,689 rows; 212 re-cut rows match; none still DISCOVERED).

## Register kills from the shared policy (OPUS, 2026-09-28)

`type_flow_census.py`'s generic register kill now uses `reg_tracking.written`, replacing capstone's `regs_access()`.
`written` folds sub-registers and corrects capstone's implicit-write defects for `cmpxchg`, `cdq` and `test`. This
completes the census's move onto the shared policy; the memory labels moved in e90e6c0b3.

**Measured:**
- all 23 recorded `recut_check.py` invocations and `cpe_recut_check.py` give FAILS 0;
- every receipt regenerated with `--receipt` is **byte-identical** to the committed one.

The change fixes the method and alters no output. It is part of
[`owned-producers-access-policy`](../owned-producers-access-policy/README.md).

**Run receipt.** Run verified at e779af776.

## CPostEffect partial re-cut: reads that cover part of a span (OPUS, 2026-09-28)

**The misleading claim.** Fifty CPostEffect rows read "mixed ... overlapping widths [1, 4, 8] - one field or several
NOT resolved". The flow census's reads settle every width they cover. `cpe_recut.py` left these rows alone only
because its rule needs the reads to tile the *whole* span, and each of these spans has unread bytes.
For example, `+0x990` is a `float` read by `movss` and a byte at `+0x994`, with `+0x995..+0x997` never read.

**The rule** ([`cpe_partial_recut.py`](cpe_partial_recut.py), shared by the patch and the check). A span qualifies
when:
- its reads (8 bytes or less) do not overlap;
- every other access touching it is a 16-byte move, or starts and ends on the new boundaries, which makes it a block
  store over whole fields, the gaps included;
- no access reaches outside it.

Fields get their type from their reads (`cpe_recut.ctype`). **Unread bytes stay DISCOVERED** as
`unobservedSpanXXX` rows, and nothing unread is typed.

**Controls (C1).** Overlapping reads (`+0x730`) are rejected, and so is a write crossing a boundary (`+0xAFC`:
`00704A19` writes 4 bytes at `+0xB00`). Fully tiled spans stay with `cpe_recut.py`.

**The earlier instrument's 8-byte hits** (`census_receiver_fixpoint`, 2026-09-25) were checked:
- `006FF808` at `+0xCA8` is in the flow census, as a block store over the whole span;
- `006FF790`, which that instrument attributed to `+0x410`, the flow census places at `+0x3B8`.

**Result.** 50 spans are re-cut. CPostEffect goes from 91 to **94** DISCOVERED rows. The count does not fall because
the unread remainders are now separate, honest rows. TYPE RESOLVED rises to 580. Each new row keeps its old span
verbatim in a `WAS` history.

**Regressions, at a68a949c1.**
- `cpe_partial_recut.py`: FAILS 0 (C1, S). S FAILED before the patch.
- `types_index.py --validate`: 8346 fields, 0 errors, 0 gaps.
- `check_census_widths.py`: 0 disagreements.
- `check_type_refs.py`: 0 dangling.
- `cpe_recut_check.py`: FAILS 0.
- The matrix-array checks, both parts: FAILS 0.

## Two residual CPostEffect rows (OPUS, 2026-09-28)

[`cpe_residual_two.py`](cpe_residual_two.py) T1 / T2 / C / S, FAILS 0 (S failed before the patch).

- **+0x600 becomes +0x600 float and +0x604 float.** The two `movss` reads tile the span. Every other access lies on
  the new boundaries: a `movss` store, one qword store over both, and 16-byte moves that end or start at +0x604. This
  is `cpe_recut.py`'s full-tile case, which never reached this span.
- **+0x5A0 becomes +0x5A0 u8[4] DISCOVERED and +0x5A4 float.** +0x5A4 is read by `comiss` and `movss`, plus one plain
  `mov`. The partial re-cut rejected it as "conflicting read types" because it typed that `mov` as uint32. A plain move
  carries width only (the rule of `ramp-channel-recut/`), so the typed reads decide. +0x5A0 is written only.
- **Controls, still 'mixed':** +0x730 (a dword also read as two words) and +0x20C (a dword also read at its top byte).
  18 CPostEffect "mixed" rows remain; they are overlapping reads, write-only spans or 8-byte `movsd` pair copies.
