# repos-d2 — spawn placement residue (L-7, L-9, L-10)

Program state: parent `2ed8affb…`, snapshot `46f02e26…`, EXE `73461d08…`, ledger
38,161 / 38,003 / 158. `Verify-GfzCheckpoint.ps1` → `CHECKPOINT VERIFIED` in `proj_hd2` /
`GFZ_HD2` before any reading. No `Apply-*`, no `Pack-*`, no GFZ state written.

Gates run: `verify_doc_addresses.py` ok (both docs), `check_links.py` 952/952,
`check_consistency.py` 0 size / 0 name / 0 caller-count disagreements.

## COVERAGE

**New document** — `05-Spawn-Encounter-Lifecycle/spawn-placement-height-and-authored-tunables.md`
Status `DOCUMENTED`, `audit.passes: 0`, tier 1. All eight sections plus a §10 recording the
adversarial work done during authoring (explicitly *not* claimed as a falsification pass; no
independent party has attacked it and `audit_crossrefs.py` has not been run against it).
133 addresses cited, 40 function entries, 16 data.

**Reopened** — `05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md`
`DOCUMENTED` → `REOPENED`, `reopened_count` 3 → 4. Two of its claims are overturned (below),
three of its open questions close. New §8f carries the correction trail; §2, §4, §6, §7 and the
§8 evidence table are corrected in place. Per the mandatory triggers: an open question closed in
a way that touches it, and two documents made incompatible claims.

Category `05-Spawn-Encounter-Lifecycle` goes 1 → 2 documents.

## OPEN-QUESTIONS

### Closures (existing ids)

- **L-7 CLOSED.** Nothing supplies the Y at generation. `FUN_00319390` writes `[0]` and `[2]`
  only; the caller never initialises `[1]`; the region test ignores it. The height is supplied
  at *activation* by a terrain probe in `SpawnUnit_FinalizeSpawnEntryActivation` (`0023A410`),
  gated on a per-unit definition bit, plus a per-unit vertical offset — and the probe yields
  world `0.0`, not the leader's height, when no surface is found, a failure its caller does not
  check.
- **L-9 CLOSED, and the question's own premise was wrong.** The mask `0x0002200000000000` is
  bits **45 and 49**, not 49 and 53. Bit 49 = set on a unit's first activation; bit 45 = set by
  ScriptVM primitive `0x304D btlAtelCanselInitialSpawnFlag`. One writer each, no clearer, one
  reader.
- **L-10 CLOSED.** `FUN_0023A520` is primitive `0x3053 btlAtelSetupActorStart`. It is **not**
  called by every zone (406 of 828 scripts), but it is called by **every** script that defines a
  unit (400/400) or runs the spawn selector (172/172), always exactly once and first.

### New — please assign real prefixes at merge

| Proposed id | Question | Owner doc |
|---|---|---|
| `PROPOSED-reposd2-1` | What definition byte `+0x18` bits 5 and 6 select. They produce `BattleUnit+0x1F6` values 1, 2, 5, 6, but the only reader of `+0x1F6` in the binary tests bit 3. Dead, or read through a form the census does not cover. | new doc |
| `PROPOSED-reposd2-2` | What the uninitialised candidate Y contains in practice, and whether any shipped enemy definition leaves the probe bit clear. Needs runtime evidence (tier 10) and the definition records, which were not extracted. | new doc |
| `PROPOSED-reposd2-3` | Whether `FUN_0026E3C0` (313 B, Movement) queries collision geometry or a height field, and what its `short` return identifies. | new doc |
| `PROPOSED-reposd2-4` | The remaining 242 records of the `0x30xx` primitive table at `01F281D0`. Ten are mapped. | new doc |
| `PROPOSED-reposd2-5` | `btlAtelSetMapJumoKeep` (`0x306C`, the return-window setter) is called by **no** script in the 828-file corpus, so the 300 s window is always the native default in the shipped game. Whether any non-US-locale or non-`plan_master` script calls it is unmeasured. | new doc |
| `PROPOSED-reposd2-6` | The 287 extracted `.ebp` containers whose first section is not a `0x8000000B` script. | new doc |

`next_question_id.py --list` reports 74 prefixes in use, next free `BW BX BY BZ CA …`.

## AUDIT-LOG

### Corrections to `spawn-placement-and-retirement.md`

**Correction 6 — the minimum-distance flags are bits 45 and 49 (OVERTURNED).**
Was: *"flag bit 49 or bit 53 (`0x2200000000000`)"*. The mask was transcribed correctly and
decomposed wrongly: `0x0002200000000000` is bits 45 and 49; `bit 49 | bit 53` is
`0x0022000000000000`, which appears nowhere in the binary. Proved from the `movabs` bytes at
`0023581D` (`49 ba 00 00 00 00 00 20 02 00`). Reachable because counting nibbles from the left
of a value printed without its leading zeros shifts every index by four. **Lesson: publish a
mask together with the bit list derived from it, so the two check each other.**

**Correction 7 — the keep banks hold 64 entries of 592 bytes, not 296 of 128 (OVERTURNED).**
`0x9400` partitions as 64 × `0x250`. The `0x128`-iteration, 8-`movups` loops are a block copy;
128 is the chunk size, not the stride. Proved from sixteen Spawn/SpawnKeep/SpawnEntry functions
pairing `imul <idx>, 0x250` with `add <reg>, [g_pBtlKeepCharWork1]`, and `0x9400 / 0x250 = 64`
exactly. The independent corroboration was already inside that document: the wipe branch resets
exactly **64** history counters. This is the same defect its own §8e recorded, caught one step
short — §8e retracted the field *names* painted onto the `memcpy` and kept the entry *count* the
same loops implied. **Lesson: a block copy's iteration count gives buffer size ÷ chunk size and
says nothing about record size.** No other conclusion in that document is disturbed.

**Correction 8 — `0031B760` is not a leaf.** It is a 13-byte null guard that tail-jumps to
`ActorWork_GetBattleUnitRaw` (`00263E30`), a 5-byte `mov rax,[rcx+0x30]; ret`. Same thunk-sink
effect as `0023A520`.

### Instrument notes worth keeping

- **Ghidra's graph reports zero callers for `0023A520`; capstone finds the thunk `jmp` at
  `00510710`.** Same disagreement the existing document already recorded. It recurs for
  `00263E30` through `0031B760`.
- **A wrong image base makes an absence claim indistinguishable from a real one.** A first pass
  assumed PE base `0x140000000` and found *zero* references to the primitive handlers; the
  optional header's ImageBase is `0x00120000`, and the same query then found every one. Recorded
  because the failure mode looked exactly like "there is no dispatch table".
- **Positive control on the L-9 absence claim.** Before claiming bits 45/49 are never cleared,
  the identical query was run for **bit 47**, known-cleared by `BattleUnit_ResetStateForReuse`:
  it returned 4 sites including `00236AB1`. The single hit for 45/49 (`002D82DD`) is a
  contiguous 14-bit field clear followed by `shl rax,0x25` — the right *shape* check, not just a
  non-zero count.
- **Limit stated, not papered over.** 387 sixteen-byte zero stores at displacement 0 exist and
  cannot be attributed to a BattleUnit statically, so "no bulk zeroing clears bit 49" is
  *argued* (from `BattleUnit_ResetStateForReuse` masking bit-by-bit) rather than proved.

### On the four gate findings repos-55 reported

- `00267DB0` **78 B was my error and 84 B is right** — I transcribed the neighbouring row
  (`00267E10 VMValueStack_PopInt32CoerceFloat32`, 78 B). Verified independently: the body runs
  `00267DB0..00267E03` = `0x54` = 84. `VMValueStack_PopFloat32Coerce` is also right; all four
  exits set `xmm0` (`movss`, `movd`+`cvtdq2ps`, `xorps`, and the `jle` error path falling into
  the `xorps`), so "Discard" is wrong. Accepted.
- `ICF_FoldedRetStub` for `0016D6A0` — accepted, and the fold explains why five different marker
  primitives share one handler.
- **The three name disagreements had a different cause than diagnosed.** They were not a
  `Spawn_` → `VM_Spawn` convention drift. The primitive-map table had a *handler* address in one
  column and a *different function's* name in the next, and `check_consistency.py`'s
  `` `ADDR` | `Name` `` pattern correctly pairs across that cell boundary. Both statements were
  true in context and the pairing was still wrong to a mechanical reader — and to a human
  scanning the table. Fixed by giving the native-target column its own address, so every name
  now sits beside the address it belongs to; the table is more useful for it. Flagging the cause
  because "a correction is a sweep, not an edit" would not have caught this one: there was no
  earlier statement left behind to sweep, only a two-address row.
- **`check_consistency.py` now runs in my routine** alongside `check_links` and
  `verify_doc_addresses`. It was the cheap catch I skipped.

## CALL-CHAINS / ADDRESS-INDEX

New cross-subsystem transitions, both directions:

```
Script (authored .ebp)  ->  Spawn
  btlAtelSetupActorStart (0x3053) -> thunk_FUN_0023a520 (00510710) -> FUN_0023A520 (0023A520)
  btlAtelDecideEntryPointAuto (0x301A) -> VM_Spawn_SelectAutomaticEntry (0050F520)
        -> Spawn_SelectAndPrepareAutomaticEntry (00235720)     [the ONLY caller]
  btlAtelCanselInitialSpawnFlag (0x304D) -> FUN_005102D0 -> sets BattleUnit flag bit 45

ActorEntity -> Spawn        BattleUnit_ActivateAppliedDefinitionRuntime (00233AD0)
                              sets qwUnitFlags bit 49; clears bit 26
                            FUN_00239E10 (00239E10) writes BattleUnit +0x1F6 and +0x188

Spawn -> Movement           SpawnUnit_FinalizeSpawnEntryActivation (0023A410)
                              -> FUN_003208C0 (003208C0) -> FUN_0026E3C0 (0026E3C0)   height
                              -> BattleUnit_PublishLocomotionPosition (00300310)      placement
                            OWNER NOTE: Movement owns the placement transaction;
                            Spawn owns the decision to place. Not caller inheritance.

Spawn -> WorldAreaField     FieldRegion_ContainsWorldPosition (002374E0)
                              -> Vector3_RotateTranslatedXZOffsetByEncodedAngle (00325EA0)
```

Addresses to add to `ADDRESS-INDEX.md` (all resolve, extents from the fresh graph):

| Address | Name | Body | Note |
|---|---|---:|---|
| `0023A410` | `SpawnUnit_FinalizeSpawnEntryActivation` | 270 B | the height source; ends in the placement call |
| `003208C0` | `FUN_003208c0` | 119 B | ground probe; `0.0` on miss; return value discarded by its caller |
| `0026E3C0` | `FUN_0026e3c0` | 313 B | the field surface query it wraps |
| `00319390` | `FUN_00319390` | 139 B | polar offset; writes `[0]` and `[2]` only |
| `00325EA0` | `Vector3_RotateTranslatedXZOffsetByEncodedAngle` | 152 B | XZ only |
| `00233AD0` | `BattleUnit_ActivateAppliedDefinitionRuntime` | 316 B | sole writer of unit flag bit 49 |
| `00239E10` | `FUN_00239e10` | 594 B | sole writer of `BattleUnit +0x1F6` / `+0x188` |
| `005102D0` | `FUN_005102d0` | 35 B | primitive `0x304D`; sole writer of unit flag bit 45 |
| `00263E30` | `ActorWork_GetBattleUnitRaw` | 5 B | the leaf behind `0031B760` |
| `002D81D0` | `FUN_002d81d0` | 478 B | discriminated false positive: 14-bit field packer at bits 37–50 |

Data addresses (for the data section of the index, not the function index):

| Address | What |
|---|---|
| `01F281D0` | ScriptVM `0x30xx` primitive table — 252 records × `0x20`, handler at `+0x00`, index = opcode low byte |
| `01F004E0` | 32,768-entry sine table, `table[i] = sin(2πi/32768)`, `table[0x2000] = 1.0` |
| `009146EC` / `F0` / `F4` | `39.0` / `42.0` / `43.0` — the constants `btlAtelSetupActorStart` installs |
| `00D10820` / `00D10828` | `+32768.0` / `-32768.0` — sine-table index scales |

## For the coordinator — things that may belong to other sessions

- **`21-RNG-And-Determinism`**: unchanged from the existing document's note, but now with a
  count — area-mode placement draws the shared LCG twice per attempt, and 146 zones set the
  attempt limit to **3**, not the default 1, so the draw count per candidate is up to 6 in a
  third of spawn-capable zones.
- **Anyone documenting the ScriptVM dispatch**: the `0x30xx` group's table location, record
  shape and index rule are established here (§2e), with ten handler↔name pairs.
- **Anyone documenting `_guard_check_icall` / the ICF fold**: five spawn marker primitives
  (`0x3054`–`0x3058`) point at `0016D6A0`, which is a data point for the "~273 folded bodies"
  census — these five reach it as *table records*, not as call sites.
- **XIIOnline / multiplayer**: the placement Y comes from a local terrain query and the
  candidate Y is uninitialised stack, so two clients cannot agree on spawn height even with a
  synchronised LCG. Bit 49 is per-client activation history, so two clients can also disagree
  about whether the minimum distance applies to the same unit. Any shared spawn model must
  transmit the resolved position after `SpawnUnit_FinalizeSpawnEntryActivation`.

---

# repos-d2 — falsification pass 7 on `vbf-archive-and-st2e-tables.md`

Assigned by repos-55. Independent: I did not write the document, and I had already built the VBF
extraction corpus, so the archive claims were **re-measured from the archive** rather than re-read.
Program state as above; `CHECKPOINT VERIFIED` before any reading.

## AUDIT-LOG

**Status `DOCUMENTED` → `REOPENED`, `passes` 6 → 7, `reopened_count` 0 → 1.** New §11 records the
pass; §6's overturned claim is marked in place.

### The kill — §6's "complete authored-data table set" is 82 entries, not 40

The path pool at `0x01E4D830` does not end at slot 40. Slot 40 is an **interior NULL**; entries
continue unbroken to slot 82, closed by a double NULL at 83/84. Three independent confirmations:

1. Direct read: slot 41 is `attribute_data.bin`, slot 82 is `board_12.bin`.
2. **The loader's own boundaries.** `FUN_002DF9A0` forms exactly five `lea` targets into the pool —
   slots **0, 84, 128, 450, 1640**. The next base it registers after 0 is **84**. The forty-entry
   boundary is not a boundary the loader recognises.
3. The `ch` block at `0x01E6BB40` reproduces the identical layout including the NULL at 40 and the
   double NULL at 83/84 — the interior NULL is authored and repeated, not incidental.

**The document contradicts itself, and it survived six passes.** Five files it analyses in detail sit
outside the set it calls complete: `attribute_data.bin` (slot 41, §2), `listhelp_action.bin` (47, §2
+ §4 "the missing half" + §9), `listhelp_status.bin` (49, §9), `ability_data.bin` (58, §2),
`word.bin` (61, the whole of §7).

**Transferable lesson.** A NULL in a pointer array reads as a terminator, and reading it that way
produced a list that was *correct on every element it contained*. **A truncation correct on all its
members looks exactly like a complete list** — nothing inside the forty is wrong, so checking them
surfaces nothing. What exposes it is asking what the **consumer** treats as the boundary. *Do not
infer an array's extent from its contents when the code that walks it is available.*

### What was attacked and held

| Claim | Result |
|---|---|
| Archive 31,196,932,183 B, `SRYK`, 89,414 entries | **SURVIVED exactly** (index re-parsed independently) |
| The four top-level counts | **SURVIVED**, and they sum to 89,414 with no remainder |
| All six extension counts | **SURVIVED**, all six |
| §5 the two path literals at `00A42148` / `00C1BFF8` | **SURVIVED** |
| §5 "nothing in `.text` references them" | **SURVIVED on a wider population** — 38,161 bodies not 34,270, and `movabs` immediates as well as `lea` |
| §6 the forty entries and their order | **SURVIVED**, name by name, `action_data` at 14 |
| §6 "repeated per language" | **SURVIVED** |
| §8 "no function references both registries" | **SURVIVED**, intersection empty |
| §9 resolver constants | **SURVIVED byte for byte** |

### The positive control §5 lacked

§5's "a scan finds zero references" had **no control recorded**. One was run in the same pass against
`009146B8` (`btlKeepCharWork1`, known referenced): it returns 1 code reference at `0023694B`. The
instrument fires on exactly the form the absence rests on. Shape-checked too: the two paths carry 6
and 3 **data** pointers and zero code references; the control carries 1 code reference and zero data
pointers — opposites. And the pointer at `0x01E4D8A0` is pool slot **14**, confirming both the pool
base and `action_data`'s index from the string side rather than the array side.

### A miscount of my own, chased not reported

My census returned 3 functions referencing `0x0215F000` against the document's 4. I checked the
missing one instead of filing a disagreement: `FUN_002DF780` takes `lea rax,[rip+0x1E7F7E5]` =
**`0x0215EFF4`, twelve bytes below the base I scanned from**. **The document is right and my window
was too narrow**; the same edge explains 449 vs 450 at the other registry. A count disagreement is a
question about two populations before it is a finding about either.

## OPEN-QUESTIONS (new, from this pass)

| Proposed id | Question |
|---|---|
| `PROPOSED-reposd2-7` | What the pool at `0x01E4D830` holds beyond the 82-entry battle/menu region. It runs for thousands of slots; the loader registers bases at 0, 84, 128, 450, 1640, and the later regions hold `.nmb` and `.ebp` paths keyed by **map codes** (`tst_a`, `bts_a`, `e00_a`), not languages. |
| `PROPOSED-reposd2-8` | Whether the interior NULL at slot 40 is a sub-group boundary used above this loader, or padding. It is reproduced identically in every language block, so it is authored. |
| `PROPOSED-reposd2-9` | The three dwords at `0x0215EFF4`, immediately below the `0x0215F000` directory, whose address `FUN_002DF780` takes — an unread header on the loader directory. |

## For the coordinator

- **Check [`authored-data-table-registry.md`](../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md)** — if it cites "40 authored tables" from this document it inherits the error.
- **AY-6 is unaffected.** The `action_data.bin` → slot `0x02EBF138` lead rests on the path literal
  and the count match; neither was disturbed, and §8's disjointness (which explains why the loader
  side cannot settle it) survived.
- **`check_consistency.py` reports 5 FRONTMATTER audit gaps in other sessions' documents** —
  `passes > 0` with `last_pass_state` absent, in `vtable-method-index.md`,
  `generated-float-table-builders.md`, `dyngeo-instance-family.md`,
  `audio-bank-and-controller-family.md` and `the-largest-unclassified-functions.md`. Not mine to
  edit. Given you have just had to lower `audit_coverage` for counting claimed rather than recorded
  passes, these five are exactly that shape: a pass count with no state naming what it ran against.
- Size / name / caller-count disagreements are **0**; links 970/970.

---

# repos-d2 — falsification pass 2 on `the-largest-unclassified-functions.md` §§12–15

Assigned by repos-55. Pass 1 (repos-9e) read §12–§15 and explicitly did not attack them.
Program state as above; `CHECKPOINT VERIFIED` before any reading. Every listing re-disassembled
from the authorized EXE; every RIP target resolved arithmetically.

**Frontmatter:** `passes` 11 → 12, `falsification_passes` 1 → 2, `last_falsification_by` repos-d2,
`falsification_result` records both passes. Added the missing `last_pass_state` (the checker's
FRONTMATTER audit gap for this document) — supplied by actually re-verifying, not to make the gate
green. Gaps now 2, both in other sessions' documents.

## AUDIT-LOG — 5 overturned, 7 survived

### Overturned

1. **§14's tag-0 arm has the polarity backwards.** `0036DF80` is
   `cmp [slot+4],0` / `je` **skip** / `jmp 003B27A0`. The handler is reached when the tag is
   **non-zero**; tag 0 means *no handler*. The tag-3 accessor `0036E5E0` uses `jne` and fires on
   `== 3` — **the two arms differ in polarity and were read as if they matched.**
2. **The tag-0 table is 32 entries, not 11.** `003B27A0` walks base `02EBE5E0` to end `02EBEBE0`
   at stride `0x30`: `0x600 / 0x30 = 32`. §14 *correctly states* that the `0xB` is a bound on the
   second argument and then titles the subsection "an 11-entry table". **The document contained the
   observation that refutes its own figure.**
3. **§13's central absence claim is false.** *"No writer anywhere in `.text` — all 16 only read"*,
   and *"built at run time through a computed pointer rather than a literal address"*. Eight of the
   sixteen write through a register `lea`-d from the **literal** base `022D94B0`. `0036E320` is a
   constructor (writes `+0x00`, `+0x04`, `+0x08`, zeroes `+0x10`); `0036E540` writes the tag.
   **§12's own matrix setter `0039AF70` writes the region through literal RIP addresses — this
   document disproved the claim one section earlier than it made it.**
4. **Tag value 2 exists and the tag is a lifecycle state.** `0036E540`: if `tag == 1`, query
   `FUN_0024DE70(payload)`, and on a result of 2 or 3 **write `tag = 2`**. §13 said 2 "is not
   tested, which is a gap rather than evidence of absence" — it is never tested and it *is*
   written, as a transition out of 1. §14's "real type discriminator" framing is incomplete.
5. **§13's accessor row for `0036E460` mis-records its test.** It is
   `cmp dword ptr [rax+rcx*8], 0` — the **payload `u32` at `+0`**, not the `u16` tag at `+4`.

### Survived

| Claim | Result |
|---|---|
| §12: **267** functions touch `022D8F00`–`022D9500` | **SURVIVED exactly**, 315 distinct addresses |
| §12: `003970A0` / `0039AF70` getter+setter, 4×4 matrix at `022D91B0` | **SURVIVED byte for byte** — 44 B each, four `movups` at `0x10` stride, exact inverses |
| §12: descriptor table 32 × 24 B, `u16` tag at `+4`, clamp `0x1F` | **SURVIVED**, verified in three accessors |
| §13: **16** functions reference the table | **SURVIVED** — see the miscount note |
| §14: the whole tag-3 reading incl. `[rsp+0x32]` for key B | **SURVIVED entirely** |
| §15: BI-10 — item ids ≠ tag-3 handles | **SURVIVED** |
| §15: `ActorHandle_ResolveRegistryEntryByPackedId` at `0x14`; `0024E210` tagged `PackedIdBucketRegistry` | **SURVIVED, both** |

**§14's tag-3 reading is also strengthened**: key A is the **low 16 bits of the handle itself**
(`r8d` takes the original id at `0024FDAB`, before the shift), and the bucket table is at
**`0x020910F0`** — an address §14 does not give. Its abridged listing omits `movzx ecx, al` at
`0024FDB5`, which is what makes the nibble the index; abridged, not wrong.

### Not reproducible as stated

**§15's shift census.** The predicate says *"a small `CMP`"* and never defines "small". With
`imm <= 0x20` the same sweep returns **59 sites in 47 functions** against the published **29 in 19**.
Not a refutation — without the threshold neither figure is checkable. The conclusions survive, but
the *exclusivity* of the `0024Cxxx`–`0024Fxxx` cluster does not: under the wider predicate 11 of 18
`0x1C` sites fall in `0024xxxx` and seven do not. **A census is a claim about a predicate; publish
the predicate.**

### A miscount of my own, chased rather than reported

I counted **13** functions referencing `022D94B0` against the document's **16**. Widening the window
from the base address to the table's full **768-byte extent** (32 × 24) gives **16**, matching: three
functions (`0036DE20`, `0036DF30`, `0036E5A0`) reach it at a non-zero offset. The document is right;
my window was one address wide. **Second pass running where a count disagreement resolved into a
population difference — this is now an expectation, not a surprise.**

### What was tried and failed to break anything

- Widened the 267-function census to all 38,161 ledger bodies: reproduced exactly.
- Tried to make the 4×4 matrix four unrelated globals: the setter is the byte-exact inverse of the
  getter over the same four addresses in the same order.
- Tried to find a fourth tag arm by reading `0036E500` and `0036E5A0` in full: neither tests the
  tag; no new arm.
- No banned evidence. Address adjacency available and refused: the `02EBE5E0` table sits near the
  `02EBF008` content registry documented elsewhere and **no relationship is claimed**.

### Consequences

- **BI-8 changes shape.** No longer "what fills a table nothing writes" — the table is built by its
  own accessor family in `.text`, constructor `0036E320`. The open part is what the payload denotes.
- **§13's generalisation should not be reused.** *"In a region where the data cannot be read
  statically, the accessors are the schema"* is a good heuristic that was over-stated into "nothing
  writes the region". The accessors **are** the schema **and** several are writers; reading only
  the readers produced the error.
- **`0024DE70` is a new lead** — the query driving the tag 1 → 2 transition, and itself a `0x1C`
  packed-id site.

## OPEN-QUESTIONS

No new ids proposed. BI-8's shape is amended in place (§13, §14, §21).

## For the coordinator

- `verify_doc_addresses` returns **REVIEW** on this document for two `.text` non-function addresses,
  `003CD298` and `003CD570`. **Pre-existing**, from §10's `003CD840` read — not introduced by this
  pass. They look like jump tables after a function; worth confirming in context.
- Links 975/975; size / name / caller-count disagreements 0. Remaining FRONTMATTER gaps: 2, both in
  other sessions' documents (`generated-float-table-builders.md`,
  `audio-bank-and-controller-family.md`).

---

# repos-d2 — falsification pass 1 on `generated-float-table-builders.md`

Confirmed unattacked before starting: the frontmatter itself said so (`last_pass_state: null` with a
note). Program state as above; `CHECKPOINT VERIFIED` before any reading. **6 overturned, 11 survived.**
Frontmatter: `passes` 1 → 2, `falsification_passes` 1, `last_pass_state` supplied.

## AUDIT-LOG

### Overturned

1. **66 objects, not 75.** `0037DF90` issues 26 calls into the region, `0037E0F0` issues 40 (of 48):
   **26 + 40 = 66 pairs, 66 distinct data pointers, 65 distinct builders** (hub builder sets
   disjoint; one builder appears twice within hub 2). **The document's own two per-hub numbers do
   not sum to its own total** — this is not a population question. 75 had propagated into §1, §2, §4
   and BH-1.
2. **The builders are not 522 KB.** They total **32,848 bytes**. The transitive closure from them
   reaches **66 of 197** functions and 32,854 bytes — **6.3 %** of 522,045. The 522 KB is the
   address range, not the startup work.
3. **§6's "everything in this region is downstream of one call" is false** — 131 of 197 are not. Its
   other half, *"nothing else reaches the builders except the two hubs"*, is **exactly right**: zero
   other callers.
4. **None of the six profiled "largest builders" is a builder.** Not one is called by either hub;
   all six are among the 131 the chain never reaches. The real builders are 44–2,250 B.
5. **The builders are not float code.** Across all 65: 4,518 instructions, **83 % `mov`**, **1 %**
   touch xmm/ymm, and **39 scalar + 25 packed float ops in total**. The profiled non-builders run
   42–73 % xmm with hundreds of `movss`/`mulss` each. The heading *"the code is scalar float math"*
   is true of the six measured and false of the builders.
6. **The values are not computed, and they are in the file.** `00485390` read directly:
   `memset(obj, 0, 0xDC0)` — the object size as an immediate — then a long run of
   `mov [obj+off], imm`, with `0x3f800000` (1.0f) stored as an **integer** immediate. §1 said *"the
   data has no file image at all, so every value in it is computed rather than read."* **The first
   clause is right and the inference is wrong**: the values are in `.text`, as operands. *"No file
   image" was measured on the destination and asserted about the source.*

**This is the pass's most useful result: BH-1 becomes a static question.** Each builder's `memset`
immediate gives its object's size (`0xDC0` = 3,520 — the largest gap the document already observed),
and the store run gives the contents. **The 66 objects are decodable from the executable.**

### Survived

197 functions / 522,045 bytes (exact) · hub counts 26 and 40 (exact) · 65 distinct routines (exact) ·
data targets `02ADEF40`–`02AED330` (exact) · gap values 336/400/304/16/3520 (all five occur) ·
**142 sites / 45 distinct callers from outside** (exact, on the stated population) · nothing but the
hubs calls the builders (zero others) · `0017D000` +31/+41/+59/+111 call targets and the +116 latch
write (all five exact) · targets beyond `.data`'s raw extent (`va2off` → `None`, re-derived) · the
six profiled functions' sizes (all six exact) · **"the 25 largest reference zero strings"** — 0 hits,
with a control (`BattleStorage_InitializeWorkArrays`) returning 4.

### Did not reproduce, conclusion unaffected

`.data` quoted as *"virtual 01DF0000 + 011A7530, raw only 002893F0"*. Virtual base and size exact;
the raw figure is not — the section's raw size is `0x0018E400` at file offset `0x01CCE600`. The
conclusion was re-verified independently and holds.

### A count disagreement chased rather than reported — third time

First census: 487 sites from 88 callers against the document's 142 / 45. §3 says *"Reach from
**outside**"*; restricting to callers outside `00480000`–`00500000` gives **142 / 45**, exact. The
other 345 are intra-region. **Third pass running with the same resolution.** The same discipline is
why finding 1 *is* reported: there the document's own numbers contradict its own total.

### Tried and failed to break anything

Recomputed the region census independently (exact) · attacked the gap list, which looked like the
first five in order and is not — but all five values occur, so the claim holds and **a false finding
was avoided by checking first** · searched for a builder called from outside the hubs (zero) · ran a
positive control before accepting the strings absence · no banned evidence; the builder set is
defined by *being called from the hubs*, never by lying in the address range.

### Consequences

- **BH-1: "not established" → "extractable."** A decoder over the 65 builders' immediate stores
  yields all 66 objects statically. Highest-value follow-up in this document.
- **BH-2 narrows** to what the stored constants mean; the form is now known.
- **BH-4 answered in part**: the region is **not** startup-only — 131 functions are entered by 142
  outside call sites, and only 6.3 % of its bytes belong to startup construction.
- **The document's title should be revisited.** "Generated float table builders" names a
  characterisation this pass overturned: the builders are generated *table writers*, and the float
  code in the range is something the startup chain does not call.

## For the coordinator

`FRONTMATTER audit gaps` is now **0** — this was the last of the five I flagged two blocks ago.
Links 988/988; size/name/caller-count disagreements 0; `verify_doc_addresses` ok.

---

# repos-d2 — the `01F26xxx` ScriptVM cluster: all five command tables enumerated

Assigned by repos-55. Program state as above; `CHECKPOINT VERIFIED` before any reading.
**Not a falsification pass** — a closure. Written into
`01-Script-VM-Native-Bridge/scriptvm-native-dispatch-table.md` §14, plus a self-correction to my own
spawn document.

## COVERAGE / CALL-CHAINS

**The extent came from the bound the code enforces, not from a walk.** All three accessors
(`003DC270` begin, `003DC240` poll, `003DC2A0` result) do `cmp edx, dword ptr [rcx]` against the
table's **own first dword** before indexing. `VMNativeCommandDispatch_InitializeFamilyTables`
(`003DC2D0`, 89 B) `rep stosq`s the default over 16 slots at `02B57EF0`, then overrides `+0x00`,
`+0x18`, `+0x28`, `+0x38` — families **0, 3, 5, 7**.

| family | base | records | id range | non-null `.text` callbacks |
|---:|---|---:|---|---:|
| 0 | `01EED700` | 1,496 | `0x0000`–`0x05D7` | 1,741 |
| 3 | `01F281B0` | **147** | `0x3000`–`0x3092` | 153 |
| 5 | `01F29418` | **1** | `0x5000` | 2 |
| 7 | `01F29440` | **104** | `0x7000`–`0x7067` | 131 |
| 1,2,4,6,8–15 | `01F26720` (shared) | **212** | `0xN000`–`0xN0D3` | 250 |
| | | **1,960** | | **2,277** |

**1,960 matches the total that document already stated**, reached from five independent counts.

**The four tables abut exactly** — the default's records end at `01F281A8` and family 3's base is
`01F281B0`; family 3 ends at `01F29418`, which *is* family 5's base; family 5 ends at `01F29440`,
which *is* family 7's base. **No gap, no terminator, no padding.** That is why a contents walk cannot
find their edges, and why only the record counts separate them.

**The id encoding, proven from the consumer.** `VMNativeCommand_ExecuteLifecycle` (`002621D0`,
461 B) is the sole caller of all three accessors and splits the id before calling:
`sar r12d, 0xc` / `and r15d, 0xfff` — **`family = id >> 12`, `index = id & 0xFFF`**, a 4-bit family
and a 12-bit index. Independent confirmation from the other end: authored primitive `0x3053` →
family 3 index `0x53`, result callback `thunk_FUN_0023a520`, which my spawn block reached from the
script side without knowing this frame.

### The 501-slot cluster is resolved

The census's 734 uncovered `.data` slots, **501 ScriptVM-owned around `01F26xxx`**, "consistent with
the four further ScriptVM tables" — **they are those tables.** The default + 3 + 5 + 7 hold **536
non-null `.text` pointers, 500 of them `Script_VM_Native_Bridge`-owned** against the census's 501: a
one-slot **attribution** difference, not an extent difference. The ~233-slot genuinely undocumented
remainder is unaffected.

## AUDIT-LOG — a correction to my own earlier work

**`spawn-placement-height-and-authored-tunables.md` §2e was wrong twice, in the two classes I have
spent this session finding in other people's documents.**

1. **Extent inferred from contents when the consumer states it.** I wrote *"the primitive table lives
   at `01F281D0`, 252 records of `0x20`"*. `01F281D0` is not a base — it is `01F281B0 + 0x20`, the
   result-callback **column**. The count is the dword at `01F281B0` and is **147**. My 252 came from
   walking while entries looked like code-or-null, which ran **105 records past the end** into the
   abutting family 5 and 7 tables. I wrote the rule *"do not infer an array's extent from its
   contents when the code that walks it is available"* and had already broken it two blocks earlier.
2. **A frame one column off** — the same defect §12 of the dispatch document records for family 0.
   Records are three callbacks (`begin +8`, `poll +16`, `result +32`); every handler I named is a
   **result** callback with `begin` and `poll` null.

**No mapping changes.** The highest index I used is `0x06C`, well inside 147, and all nine were
re-verified in the correct frame. Both corrections are recorded in place in that document.

## For the coordinator

- I added §14 to `scriptvm-native-dispatch-table.md` (outside my assigned category, on your
  assignment of this block). It does not touch that document's existing sections.
- A process note worth having: **two of my patch scripts leaked Python string delimiters into
  published markdown** when I mixed `'''` and `"""` conventions in one file. Caught by reading the
  rendered output, not by the gates — `check_links`, `verify_doc_addresses` and
  `check_consistency` all passed with `''' + EM + u'''` sitting in the prose. **A grep for
  `+ EM + u` across the database is now zero**, and it is a cheap standing check for anyone
  generating markdown from a script.
- Links 992/992; size/name/caller-count 0; frontmatter gaps 0.

---

# repos-d2 — the remainder recounted: 198, not ~233

Written into `99-Unresolved-Residual/Unowned-Code-Census/why-the-unowned-code-has-no-owner.md` §17.
`passes` 8 → 9. Program state as before; `CHECKPOINT VERIFIED`.

## COVERAGE

**§16's five-condition test reproduces exactly** — re-implemented independently:
`DIR64` relocations **114,962** (doc: 114,962), certified `.data` slots **3,015** (doc: 3,015).

| span | slots |
|---|---:|
| ScriptVM family 0 · battle action · combat formula | 1,740 · 340 · 202 |
| **ScriptVM default / family 3 / family 5 / family 7** (new) | **250 · 153 · 2 · 130** |
| inside a documented span | **2,817** |
| **REMAINDER** | **198** |

**The remainder is 198, not ~233 — and that is not an arithmetic correction.** 535 slots acquired a
home, 34 more than the 501 the estimate anticipated.

**Why the estimate undershot.** It subtracted by **target ownership** where the remainder's own
definition subtracts by **span membership**. Those four tables hold 35 callbacks pointing at
functions owned by other subsystems or by nobody. **An owner-keyed estimate of a span-keyed quantity
is systematically low, and it is low by exactly the cross-subsystem callbacks** — the interesting
part of any dispatch table.

**The staleness property, stated in the document** at your suggestion: a remainder is defined by a
subtraction, so it goes stale on *another session's success* rather than on new evidence, and nothing
in the figure announces it. §17 publishes the seven spans it was subtracted from and the date.

## AUDIT-LOG

### The remainder is mostly not loose slots

113 contiguous runs, but **contiguity is the wrong shape**: the large groups are strided records with
non-adjacent pointer fields, so run analysis fragments one table into many two-slot runs.

**The eight two-slot `Items` runs are one table**, and its consumer states the bound:
`InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState` (`0030B6A0`) walks
`lea r8,[01EEBCC0]` … `lea rbx,[01EEC1E8]` … `add r8,0x58` / `cmp r8,rbx`.
`0x528 / 0x58 = 15` exactly — **fifteen inventory class descriptors of 88 bytes**. The rebaser also
gives the record layout free: three rebased offset→pointer fields (`+0x00/+0x08`, `+0x18/+0x20`,
`+0x28/+0x30`), an element count at `+0x3c`, a running cumulative index at `+0x40`, and the two
callbacks at **`+0x48` (mutate)** and **`+0x50` (query)** — the slots this census counted. The pairs
are `InventoryPackedCountClass_*` and `InventoryBitsetClass_*`: **two storage classes shared across
fifteen descriptors**, which is why the same addresses repeat.

A second strided family at `01F32150`, stride `0x80`, with five per-record accessors at
`008B75A0`–`008B75E0`. **Extent not established and not claimed.**

### Survived, plus one run §16 did not list

All six of §16's runs reproduce exactly, including the two CRT-allocator runs. **A seventh is larger
than two it lists and is absent**: `01F41E60`, **6 slots, all Audio**, 56 bytes before the 26-slot
Audio run — almost certainly the same structure, i.e. the fragmentation effect again rather than a
find.

Remainder targets by owner: 111 unowned, 41 Presentation, 22 Audio, 20 Items, 2 ScriptVM, 1 Platform,
1 Party. **38 slots hold `ICF_FoldedRetStub`** as a null placeholder (§16 reports 58 across the
wider 734).

**The genuinely uncharacterised part is well under 198**: the descriptors (≤30), allocators (8),
folded stubs (38) and the Audio pair (32) are accounted for by shape. The residue is the **88
single-slot runs**.

## For the coordinator

- Gates: links 1011/1011, size/name/caller-count 0, frontmatter gaps 0,
  `check_generator_artifacts.py --db` → **no generator artifacts in published prose**.
- A transient NAME disagreement appeared on one run and was gone on the next — another session was
  mid-write. Worth knowing the gates are not atomic against concurrent edits; a single red result
  during parallel work should be re-run before it is believed.

---

# repos-d2 — `01F32xxx` closed: a name-keyed registry, not an array

Census document §18. `passes` 9 → 10. Gates: links 1012/1012, size/name/caller-count 0,
frontmatter gaps 0, `check_generator_artifacts` clean.

## COVERAGE / CALL-CHAINS

**The hypothesis I published before starting was wrong, and the shape was wrong.** There is no
array and no stride. The five two-slot runs at `01F32150`+ are the `+0x40`/`+0x48` fields of five
individually declared descriptors at `01F32110 + k*0x80`, and each begins with a `char *` name:

| base | name | `+0x40` | `+0x48` |
|---|---|---|---|
| `01F32110` | `Skin` | `006D5CC0` | `006D5DF0` |
| `01F32190` | `SkinLocal` | `006D5B60` | `006D5DF0` |
| `01F32210` | `SkinLocalTangent` | `006D5B60` | `006D63D0` |
| `01F32290` | `SkinVertex` | `006D5CC0` | `006D6AC0` |
| `01F32310` | `SkinVertexLocal` | `006D5B60` | `006D6AC0` |

**Five named skinning variants** — the mesh-deformation paths. The two callbacks are **orthogonal
discriminators**, readable from the sharing alone: `+0x40` selects space (`006D5B60` for every
`…Local`, `006D5CC0` otherwise), `+0x48` selects output kind (`006D5DF0` plain / `006D63D0` tangent
/ `006D6AC0` vertex). Five of six combinations exist.

**The registrar is the schema, since there is no loop.** `FUN_006D5A60` (132 B, via
`thunk_006D5A50`) is a linked-list insert keyed on the name: refuse if `name` is null (`0x11`),
refuse on duplicate name (`0x12`), else `record->next = head; head = record`. Head at `02E9FD60`.
Record is `{char *name; Record *next; …}` — **the registry never learns a record's size**, which is
why records of two sizes go through it and why "stride" was the wrong question.

**Extent established by enumerating registration sites:** `FUN_006C45F0` performs **14**
registrations; `FUN_006C4750` performs the matching 14 unregistrations via `FUN_006D6F90`. Nine of
the fourteen are a different record type at `02E9FEF0 + k*0xD0`.

### Why only five of fourteen reached the census

`.data`'s raw extent ends at `01F7E400`. The five `Skin*` records are **below** it — statically
initialised, relocated, file-backed — so their callbacks satisfy §16's five-condition test. The nine
are **above** it in the zero-filled tail: no file image, no relocations, names null in the file,
built at run time.

**A run appearing in the remainder may be a fragment of a population mostly invisible to the test.**
That is a different situation from a run being the whole of something small, and it is worth knowing
before anyone treats a remainder run as a complete object.

## AUDIT-LOG — an instrument defect of my own

My registration-site scan counted `call` and reported **13** sites. The fourteenth is a **tail
jump** — `lea rcx,[01F32310]` / `add rsp,0x28` / `jmp 0x6d5a50` at `006C4734`. What exposed it was
the *names*: four `Skin*` variants with an obvious fifth missing.

**Third time tonight the tail-call-as-sink effect has cost something** — after Ghidra's graph
reporting zero callers for `0023A520`, and `00263E30` under-reported through its guard `0031B760`.
I wrote both of those up as other tools' blind spots and then built the same one into a scan of my
own. **A census of call sites that does not count tail jumps is not a census of call sites**, and
knowing that in the abstract did not help.

Same lesson as the family-3 overrun, now with a second instance: **a rule I have just published
protects the work in front of me and nothing else.** What caught it here was a semantic regularity
in the data — a naming series with a hole — not the rule.

---

# repos-d2 — the 88 single-slot runs: an artifact, not a population

Census document §19. `passes` 10 → 11. Gates: links 1019/1019, size/name/caller-count 0,
frontmatter gaps 0, generator-artifacts clean.

## AUDIT-LOG — my own §17 residue claim overturned

§17 said the residue was *"the 88 single-slot runs — where a slot really is a lone callback rather
than a fragmented table."* **Wrong, and the error was in the instrument that produced it.**

Runs were grouped by **contiguity** (8 bytes apart). **A table whose record contributes exactly one
pointer can never produce a contiguous run** — consecutive pointers are one *stride* apart, not 8 —
so every such table shatters into as many "single-slot runs" as it has records.

Regrouping the same 198 slots into **arithmetic progressions of ≥3**:

| | contiguity | progression |
|---|---:|---:|
| groups | 113 | **34** |
| slots grouped | — | **179** |
| **truly isolated** | *"88"* | **19** |

Largest: `01EFFAF0`–`01EFFF70` stride `0x10`, **73 slots**, `PresentationAuthoredCommand_Class*`.
Then Audio at `01F41E68` (16 @ `0x10`), `01F003A8` (13 @ 8), `01EECFE0` (12 @ 8), `01E0C498`
(10 @ 8), Audio `01F41E60` (9 @ `0x20`), the §17 inventory descriptors (13 @ `0x58`/`0xB0`), the §18
`Skin*` descriptors (10 @ `0x80`), and the two allocator runs.

**The §17 and §18 tables reappear here as "singletons" wherever a record's second callback is null** —
the same fragmentation seen from the other end.

## COVERAGE — the largest group closed

`PresentationEmbeddedRecord_ExecuteCommand` (`0041E000`) states the bound:

```asm
0041E097  lea r13, [rip -> 01EFFAF0]        ; base, hoisted out of the loop
0041E0C6  and eax, 0x7f                     ; index masked -> 128 RECORDS
0041E0C9  shl rax, 4                        ; stride 16
0041E0CD  cmp byte ptr [rax + r13 + 8], 0   ; +0x08 enable byte
0041E117  call qword ptr [r9 + r13]         ; +0x00 handler
```

**A 128-record authored-command table at `01EFFAF0`**, `0x10` per record, handler at `+0x00`, enable
byte at `+0x08`, index **masked rather than validated** — the same clamp-don't-check pattern this
database records at `022D94B0`. Span `01EFFAF0`–`01F002F0`. Other consumers:
`PresentationEmbeddedRecord_UpdateCurrent` (`0041DA90`), `..._ExecuteDeferred` (`0041E1D0`). Only 73
of 128 records hold a certified pointer; the rest are null or `ICF_FoldedRetStub`.

## The transferable point

> **A grouping rule is a hypothesis about the data's shape, and reporting its output as a population
> asserts that hypothesis.** "88 single-slot runs" reads as a fact about the engine and was a fact
> about `step == 8`.

The check is cheap and I had not run it on my own figure: **regroup under a different rule and see
whether the population survives.** It did not — 88 became 19. This is the third time a run-boundary
assumption has produced a false population in this document's history (nulls, then stride, now
adjacency), and the first where the fragmenting instrument was mine.

**The remainder is a floor on structures, not a count of loose pointers.** Nine tables account for
179 of 198; the honest uncharacterised residue is **19 slots**, and even those are not established as
lone callbacks — only as slots this grouping could not place.

---

# repos-d2 — the grouping-rule sweep: not clean, and the defect is section-specific

Requested by repos-55 after §19. **The sweep is a prose+binary audit, no document edited yet** —
the at-risk claims belong to other sessions and one is being actively worked, so this is reported
before anyone builds on it.

## The sweep

Scanning all published documents for **partition-dependent** population claims (numbers of runs /
clusters / groups / islands — where a different grouping rule changes the number) gives **46 hits**.
I deliberately excluded selection-dependent counts (callers, sites, slots): those are the already-named
"publish the predicate" defect, not this one.

> **Note on my own instrument:** a first pass counted 754 "unstated" claims by including selection
> nouns. That was my regex asserting a hypothesis — "31 vtable slots" is structural, not a partition
> choice. Narrowing to genuinely partition-dependent nouns took it to 46. **The over-broad version
> would have been the sixth checker tonight to manufacture findings from its own pattern
> assumptions.**

## The measurement — and it is section-specific

Certified, relocated function-pointer slots, grouped two ways:

| section | slots | contiguity (step 8) | arithmetic progression | singletons surviving |
|---|---:|---|---|---:|
| `.rdata` | 27,202 | 2,465 runs / **404** single | 2,849 groups / **482** single | **119 %** |
| `.data` | 3,015 | 1,977 runs / **1,678** single | 574 groups / **316** single | **19 %** |

**In `.data`, contiguity inflates the single-slot population 5.3×.** In `.rdata` it does not — the
dominant structure there is vtables, which genuinely *are* contiguous pointer arrays, so contiguity
is the right rule and regrouping makes it slightly worse.

**So the defect is not "contiguity is wrong". It is "contiguity is wrong for `.data`."** `.rdata`
holds arrays of pointers; `.data` holds records with a pointer field. The same rule is correct in
one and 5× wrong in the other.

> **I nearly published the mixed figure.** My first run combined both sections and reported "36 % of
> singletons survive" — a single number averaged over two populations with **opposite** behaviour.
> That is the same defect I have spent the night finding, committed one probe before writing it up.
> The per-section split is the measurement; the combined number is meaningless.

**The `.data` figure of 1,977 runs is the census document's own** — §16's *"1,959 of 1,977 runs
uncited"*. Under progression the same slots form **574** groups.

## Claims to re-derive, in priority order

1. **`why-the-unowned-code-has-no-owner.md` §16-ish, the `.rdata` residue: "266 slots form 192 runs,
   166 of them single slots."** A session is **working this now**. It is `.rdata`, so by the table
   above it is the *safe* section — but 166 of 192 being single is far above the `.rdata` base rate
   (404 of 2,465), which suggests this particular residue behaves like `.data`. **Worth one regroup
   before anything is built on it.**
2. **`rtti-vtable-object-model.md`: "3,639 of the 3,953 unnamed runs are a single slot — 92.1 % of
   the runs, 58.5 % of the slots."** Its population is "pointer runs in data carrying no locator",
   i.e. deliberately the non-vtable remainder — **precisely the population where contiguity fails.**
   I did not reproduce their exact figure because their population excludes locator-backed runs and
   mine does not, so **I make no claim about 3,639 being wrong** — only that the instrument that
   produced it has a measured 5.3× singleton-inflation on the closest population I can rebuild.
3. **`the-unresolved-158.md`: "14 connected clusters plus 109 singletons."** A *connectivity* rule,
   not contiguity — a different hypothesis, and not covered by this measurement. Flagged as
   unchecked rather than at risk.

## The general result

**The sweep did not come back clean.** The answer to "was this document unlucky, or is the practice
unsound?" is **neither, exactly**: the practice is sound where the data is arrays and unsound where
the data is records, and **nothing in the phrase "N single-slot runs" says which you have**.

The cheap standing check, now measured rather than asserted: **regroup under a second rule; if the
population moves by more than a little, the first rule was a hypothesis about the data's shape.**

---

# repos-d2 — item 2 settled: AS-4's figures reproduce, its inference fails in `.data`

`rtti-vtable-object-model.md` §8 (AS-4). **Reported, not corrected** — not my document.

## The population reproduces to the decimal

Rebuilt under AS-4's own definition — contiguous runs of function pointers in data whose first slot
is **not** preceded by an MSVC RTTI Complete Object Locator, tested structurally (`signature == 1`
and `pSelf` RVA equal to the locator's own RVA), no relocation requirement:

| | AS-4 | rebuilt |
|---|---:|---:|
| unnamed runs | 3,953 | **3,957** |
| single-slot runs | 3,639 | **3,643** |
| share of runs | 92.1 % | **92.1 %** |
| share of slots | 58.5 % | **58.5 %** |

Four runs apart on 3,957 (0.1 %), both derived percentages identical. **The population is the same
population**, so what follows is about the same numbers AS-4 reports.

## Regrouped: the figure holds, the inference does not

| section | unnamed slots | contiguity | regrouped | singletons surviving |
|---|---:|---|---|---:|
| `.rdata` | 3,202 | 1,976 runs / **1,963** single | 1,836 groups / **1,807** single | **92 %** |
| `.data` | 3,015 | 1,977 runs / **1,678** single | 572 groups / **301** single | **18 %** |
| `_RDATA` | 8 | 4 / 2 | 4 / 2 | 100 % |
| **total** | 6,225 | 3,957 / **3,643** | 2,412 / **2,110** | **58 %** |

**AS-4's count is correct and its conclusion is half wrong.** §8 says *"a one-slot run is an
individual stored function pointer — a callback registered in a global or a struct field — not a
table."*

- **In `.rdata` that holds** — 92 % of its singletons survive regrouping.
- **In `.data` it fails** — 82 % of its singletons are members of arithmetic progressions of three
  or more, i.e. rows of strided tables.

**1,533 of the 3,643 (42 %) are not individual stored pointers**, and essentially all of the failure
is on the `.data` side. Identifiable `.data` tables recovered from the singleton population include
`CombatAction` runs at stride `0x18`/`0x30` (96, 48, 37 slots), the `Presentation` authored-command
table at `01EFFAF0` stride `0x10` (73), and several `Script_VM_Native_Bridge` progressions.

## A limit on my own instrument, stated

My regrouping is **greedy longest-progression**, and that is itself a hypothesis. In a dense region
it can merge slots from *different* structures into one spurious progression — two of the listed
`Script_VM_Native_Bridge` progressions (stride `0xC0` and `0xA0`) span the command tables I
enumerated in §14, which are `0x20`-stride records with three pointer fields; a long `0xA0`
progression across them is an artifact of the search, not a table.

**So `301` is a lower bound on the true `.data` singleton count, not a measurement.** The honest
statement is that the true figure lies between **301 and 1,678**, and that the direction is not in
doubt: contiguity over-counts singletons in `.data` by a large factor. **Reporting the collapsed
number as if it were exact would repeat the defect this sweep exists to find.**

## Recommendation for that document's owner

The AS-4 numbers need no correction. **The sentence that needs qualifying is the inference**, and
the qualification is one clause: *"in `.rdata`, where the unnamed runs are genuinely individual
pointers; in `.data` most are rows of strided tables."* The `.rdata`/`.data` split is the whole
finding and it is cheap to re-derive.

---

# repos-d2 — item 3 closed: the 158's clustering survives, but 109 overstates isolation

`the-unresolved-158.md` §10. **Reported, not corrected.** My own flag, now discharged.

## The rule was stated, so the test is whether the population survives a defensible alternative

§10 states it plainly: *"treating the 158 as a graph in which an edge exists when one unresolved
function calls another."* Residual list from my own verified checkpoint, 158 addresses, SHA
`c5d4b7f7…` matching the certified value.

| rule | clusters of 2+ | singletons | largest |
|---|---:|---:|---:|
| **A** — call only, residual-internal *(theirs)* | **14** | **109** | **13** |
| **B** — call **or tail `jmp`**, residual-internal | 14 | 109 | 13 |
| **C** — shares a callee of fan-in ≤5, or a caller | 24 | **71** | 11 |
| C at fan-in cap 10 / 25 | 21 / 13 | 56 / 42 | 34 / 76 |

**Rule A reproduces exactly.** And **rule B gives the identical partition** — I expected the
tail-call defect that has bitten me three times tonight to apply here, and **it does not**. No
residual reaches another residual by tail jump. That is a real survival, tested for the specific
reason it was likely.

**So this is not the contiguity case.** "109 singletons" is not an artifact: 109 residuals genuinely
neither call nor are called by another residual.

## But it overstates isolation, and the attack order is blind in one direction

Rule C is a different defensible question — *"are these used together?"* rather than *"do these call
each other?"* — and it is hub-sensitive, so I swept the cap rather than picking one. At a
conservative cap of 5, **only 71 of the 158 are isolated, not 109**, and **six sibling clusters of
3+ members contain functions no call cluster holds**:

| funcs | bytes | members the call rule sees as singletons |
|---:|---:|---|
| 11 | 8,428 | `002B6DB0` `003BDDE0` `003BDFF0` `003BE950` `003BED70` `004027D0` `00402F00` `004044D0` |
| 7 | 5,668 | `00565A00` `00571F60` `0057D620` |
| 5 | 3,842 | `003FD360` `003FDFE0` `00564780` `0056E880` |
| 4 | 3,635 | `001D72F0` `001D76A0` `001D7A20` `001D7DD0` — **zero overlap with any call cluster** |
| 3 | 1,606 | `003BA7B0` `003BA990` `003BAC90` |

**The 13-function cluster is corroborated, not undermined.** Rule C independently produces a
10-function cluster sharing **8** members with it — two different rules agreeing on the same core is
support for the reading that has already been acted on.

**The two clusters already read were sound targets.** The ranking is correct *within* the call rule;
what it cannot see is groups whose members share callees without calling each other. The
`001D72F0`–`001D7DD0` group is the clearest example: four consecutively-addressed residuals,
3,635 bytes, invisible to rule A and to any address-adjacency argument, connected by shared callees.

## Three items, three different outcomes

Worth recording together, because the sweep's value was in the *differences*:

| item | outcome |
|---|---|
| `.data` run analysis (mine) | **collapsed** — 88 singletons → 19 |
| AS-4's 3,953 runs | **split** — sound in `.rdata`, fails in `.data` |
| the 158's clustering | **survives** — reproduces, and survives the variant most likely to break it |

**A sweep that returned the same verdict three times would have been measuring the sweep.**

---

# repos-d2 — the four-residual group read: one family, and the sibling rule is vindicated

`001D72F0` · `001D76A0` · `001D7A20` · `001D7DD0` — 937 / 885 / 932 / 881 B, all untagged, all
`owner = -`. **Document-ready section below; not placed, because `the-unresolved-158.md` is actively
navigated and its §11 is another session's read.**

## The verdict I pre-committed to being able to give

I said before starting that "the sibling rule grouped a compilation artifact" was a possible result.
**It is not the result.** The four share a mechanism visible in the bodies, not merely a helper set:

Each one, in the same order:

```c
ctx = GetGlobalContext();          // 001B1C00 -> pointer at 01F811E8; 56 callers image-wide
ResetDrawState(ctx);               // 001B1910 -> memset(ctx+0x3930, 0, 0x178); ctx[0x3A4C] = 0x80
ctx = GetGlobalContext();  SetB(ctx, 0x3001);   // 001B22E0 -> ctx[0x3A70] = v
ctx = GetGlobalContext();  SetA(ctx, 0x44);     // 001B22D0 -> ctx[0x3A68] = v
ctx = GetGlobalContext();  ... 001B22F0, 001B2490, 001B2410, 001B06D0, 001B03D0
```

**Same-translation-unit is insufficient as an explanation.** It would account for shared helpers; it
would not account for four functions driving one global context through an identical reset-then-set
sequence with a systematic polarity discriminator.

## The discriminator

| function | `0x3001` / `0x44` pair | polarity passed to the setter family |
|---|---|---|
| `001D72F0` | set | **+1** |
| `001D76A0` | set | **+1** |
| `001D7DD0` | set | **+1** |
| `001D7A20` | **skipped** | **−1** |

Three enable variants and one restore/disable variant — the same shape as the `Skin*` family in §18,
and recovered the same way: from which values repeat, without reading the setters' callees.

## What the bodies compute

Packed-field unpacking and rect arithmetic, from a record reached at `[arg+0x70]`, `[arg+0x78]`,
`[arg+0x80]`:

```c
w = (u32)rec[4];  x = w & 0xFFF;  y = (w >> 12) & 0xFFF;   // a packed 12:12 coordinate pair
right  = (s16)hdr[4] + (u16)hdr[8];                        // x + width
bottom = (s16)hdr[6] + (u16)hdr[0xA];                      // y + height
```

## Call chain, and what it does NOT establish

Each of the four has exactly one caller. `001D7280` calls `001D72F0` and **tail-jumps** to
`001D7DD0`; `001829C0` tail-jumps to `001D76A0`; `001D8AB0` calls `001D7A20`.

`001D7280` calls **`SaveloadManager_GetSingleton`** and **`SaveWrite_GetBusyFlag`** immediately
before invoking two of the four.

> **That names one caller's business, not the four functions'.** The save evidence attaches to
> `001D7280`; the context getter `001B1C00` has **56 callers image-wide**, so the context is shared
> infrastructure rather than save-specific, and inheriting an owner downward from a caller is banned
> here anyway. **The honest statement is that one of the three entry points consults save-busy state
> before drawing.**

A 3-hop upward trace from all three entry points returns **zero named ancestors** — the whole
`00182xxx` / `001D7xxx` / `001D8xxx` neighbourhood is unnamed, and there are no strings in any of the
four or in any shared helper.

## Not established

- **What they draw.** The state-set sequence and rect arithmetic are a drawing shape; nothing names
  the surface, the primitive or the content.
- **Ownership.** Untagged, and the only domain hint is one caller's callees.

## Shared callee list, confirmed by reading (for the board)

All four call: `001B03D0` `001B06D0` `001B1620` `001B1910` `001B1C00` `001B2410` `001B2490`
`001FBD80` `001FBE30` `001FBE50` `00808C40`. Three of four also call `001B22D0` `001B22E0`
`001B22F0` — the fourth is `001D7A20`, which skips them, and **that skip is the finding**, not a gap
in the data.

**One correction to the handover data:** the earlier callee lists included `001D7C21`, `001D7C62`,
`001D7FB1` — these are **mid-function addresses inside the group's own bodies**, picked up because
the edge scan counted `jmp` as a call edge and local branches look identical to tail calls. They are
not callees. The same `jmp`-as-edge choice is what correctly caught `001D7280`'s tail jump to
`001D7DD0`, so the rule earns its keep; it just needs an "is this a function entry" filter.

---

# repos-d2 — triage of the 97 proposed questions

**No `_index/*.md` edited** — this is the triage, for you to merge.

## Closed by work done during this run, and never linked to it

**Five, and four are the same story:** `repos-46` staged them as proposals; I closed three of them
hours later without ever seeing the proposals, because they had not reached `OPEN-QUESTIONS.md`.

| id | verdict |
|---|---|
| `PROPOSED-repos46-4` (L-7) | **CLOSED.** Nothing supplies the Y at generation. `FUN_00319390` writes `[0]`/`[2]` only; the height is a terrain probe in `SpawnUnit_FinalizeSpawnEntryActivation` (`0023A410`), gated on definition byte `+0x18` bit 4, yielding world `0.0` on probe failure. |
| `PROPOSED-repos46-6` (L-9) | **CLOSED, and the question's premise was wrong.** The mask `0x0002200000000000` is bits **45 and 49**, not 49 and 53. Bit 49 = set on first activation; bit 45 = set by ScriptVM primitive `0x304D btlAtelCanselInitialSpawnFlag`. |
| `PROPOSED-repos46-7` (L-10) | **CLOSED.** Not every zone — 406 of 828 scripts — but all 400 that define a unit and all 172 that run the spawn selector, always once and first. |
| `PROPOSED-repos46-2` (K-7) | **CLOSED.** `how-the-engine-chooses-3d-or-flat-movement.md` §2 gives both selectors' exact bit arithmetic, and I re-derived both bodies in its falsification pass. |
| `PROPOSED-repos46-9` (K-10) | **SATISFIED.** The character render record array document exists and now carries `passes: 1`. |

**`PROPOSED-repos46-5` (L-8) remains genuinely open** — the `0x80000003` status mask. I read it four
times in different documents this run and never established what it *means*.

## Rows that are answers, not questions

`PROPOSED-repos2d-6`, `PROPOSED-reposec-3` (its own text reads *"ANSWERED, completely"*),
`PROPOSED-reposec-5` (*"Restated … it is a record header, not a standalone constant"*), plus the two
you already identified (`repos2d-12`, `repos9e-13`). **Six of 97 are answers wearing question rows.**

## Premise corrected by later work, still open

| id | correction |
|---|---|
| `PROPOSED-reposd2-4` | "the remaining **242** records of the `0x30xx` table" — family 3 has **147** records, not 252. The real remainder is **137 of 147**. My own error, corrected in the dispatch document §14. |
| `PROPOSED-reposd2-8` | Half answered: the interior NULL at slot 40 is **not** a boundary the loader recognises — `FUN_002DF9A0` registers its next base at slot **84**. Whether anything *above* the loader uses it is still open. |

## Verified open — checked this run and deliberately not closed

This is a different state from `untriaged` and worth recording as one: somebody looked.

- `PROPOSED-repos9e-2` (shadow offsets), `-3` (`{i}` payload), `-4` (glyph `+0x04`) — **named
  explicitly as not-cleared** in my batch-A verdict on the glyph document.
- `PROPOSED-repos94-1` — which destructors folded onto `0016D6A0`. My thunk pass established the ICF
  fold and its scale; *which source destructors* is not recoverable from the fold. Confirmed open.

## One duplicate pair

`PROPOSED-reposec-1` and `PROPOSED-reposec-13` are the **same question** — why `02064AC4` shows five
writes and one read. `-1`'s captured text is truncated (`3` \| Why …`), which is probably why it
survived as a separate row.

## Sixteen rows whose captured text is not the question

`repos2d-6` · `repos78-3` · `repos78-6` · `repos94-18` · `repos94-19` · `repos9e-8` · `-9` · `-10` ·
`-11` · `-12` · `-13` · `-14` · `-17` · `reposd2-5` · `reposec-5` · `reposec-1`

Mostly the merge capturing the sentence that *announced* the id rather than the question — thirteen
of the sixteen contain their own id. `repos9e-17`'s entire text is `` (`PROPOSED-repos9e-17`). ``

**And a note on how I got that number.** I wrote a classifier for it, which said **30**. Tightened
it, and it said **29** — the same wrong answer, because both versions counted a leading
`document.md |` prefix as a fragment. The right answer is **16** and I got it by reading all 93
lines. **Third instrument of mine tonight to assert its own hypothesis**, and the cheapest fix was
to stop using one on a 93-row list.
