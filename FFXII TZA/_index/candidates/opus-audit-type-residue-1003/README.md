# OPUS audit: type and field residue under the load-bearing contracts

*Draft for `FABLE-REQ-OPUS-AUDIT-TYPE-RESIDUE-1003` (independent corpus audit 2026-10-03, section 8).
OPUS, 2026-10-03. Not published and not applied: the type store and the contracts are unchanged, and the
routed items below are proposals for their owners.*

## OPUS headline

**No genuinely reconstruction-critical unknown was found in the type residue the load-bearing L2
contracts use.** One **access-layer correction** was found, and whether it matters for reconstruction
waits on one bounded reader census (`SystemStopRecord +0x08`, routed below). Everything else that the
census flags falls into one of the audit's two harmless classes.

| measure | count |
|---|---:|
| type store: types / field rows | **827 / 9,146** (the audit's snapshot figures, reproduced) |
| field rows carrying any residue flag, store-wide | 4,073 of 9,146 |
| load-bearing contracts (registered on, or credited by, a MET system) | 105: **76 L2**, 29 L1 |
| distinct field rows the 76 L2 contracts cite (any tier) | **545** |
| of those, carrying any flag | 95 |
| **core worklist**: L2, tier A or S, flagged RUNG or CONF, not a declared gap row | **54 rows over 8 types** |
| declared gap rows that a contract's own entry functions touch | 1 L2, 1 L1 |
| core rows that are genuinely reconstruction-critical, after reading | **0** |
| rows needing routed work | 1 correction (`SystemStopRecord +0x08`) plus store-hygiene items |

The audit asked that the 9,146 not get a blanket promotion. That is borne out: **of 4,073 flagged rows
store-wide, 95 sit under a load-bearing L2 citation, and none of the 54 core rows is a missing piece of
behaviour.**

## OPUS method

`type_residue_census.py` joins three kinds of contract citation to the `fields.tsv` status columns. Tiers
are strongest first:

- **A (access):** the contract's own `entries:` functions touch the field, per a
  `_types/field-access-index.tsv` row whose `function` is an entry.
- **S (static):** a static address in the contract's Types/State sections resolves into the field. It uses
  `contract_named_state_census.py`'s reader (imported), the denominator SWE2-AUDIT-SEM accepted for the
  `types` cell.
- **R (record):** a contract line names the type and an offset `+0xNN` inside the field. This is line
  co-occurrence and can mis-assign; sample 8 is an example.

A cited row is **flagged** when any of these holds:

- **RUNG:** readiness is DISCOVERED or CLASSIFIED;
- **CONF:** confidence is UNKNOWN;
- **NAME:** the name is a placeholder;
- **GAP:** it is an `unobserved…`/`…Span` row (the same test as `contract_named_state_census.field_at`);
- **CTYPE:** the ctype is empty or contains UNRESOLVED.

**NAME alone is not counted as residue in the core list.** 34 of the 95 flagged L2 rows are TYPE RESOLVED
with a placeholder name, so their representation is known. Two more lists come with it:

- declared **gap rows that an entry function touches**, the one place a gap row can hide behaviour;
- **cited types** whose `types.tsv` readiness is at the lowest rungs.

`fields.tsv`, `types.tsv` and the access index are read with `str.splitlines()`. All three are LF-only
today, but the store has carried mixed line endings.

## OPUS: the 54 core rows, in the audit's three classes

| rows | type (contract, system) | audit class | why |
|---:|---|---|---|
| 36 | `ManagerSub0209BE80_57E0`, `ManagerSub0209BE80_57E0PairRecord`, `ManagerSub0209BE80_8FA0`, each `+0x000`–`+0x0B8` (`CONTRACT-widget-object.md`, S-36) | representation known; semantics carried elsewhere | Embedded **copies of the `Widget` base layout**. Each row's meaning reads "Widget +0xNN". The canonical `Widget` rows at the same offsets are TYPE RESOLVED or SEMANTICALLY IDENTIFIED (for example `+0x44` low word 100, `+0x98`/`+0x9C` transition outputs, `+0xA0` opacity byte, `+0xB4` half-rate phase). The CLASSIFIED rung is the copy's, not the knowledge's. |
| 13 | `EncodedIdQueryRecord` `+0x34`–`+0x60` (`CONTRACT-encoded-id-space-and-class-registry.md`, S-04) | representation known; semantics a declared limit | Tagged per-class output slots of the `0031C5D0` filler. The writer side (which row byte lands where, per class) is recorded in each meaning cell from SECTION-05's full disassembly. The contract's §14 marks "exact downstream meaning of all tagged output slots and strided class10 elements" **SUPERSEDED 2026-09-29 (SWE2-FRONTIER): ruled a declared limit**. The page is REOPENED on OV-5, so this residue is already tracked there. |
| 1 | `AchievementState +0x024` `counterId17` (`CONTRACT-shop-stock-ladders.md`, S-30) | representation known | Its own meaning cell settles it: the counter for achievement id 17, width and offset declared by the descriptor at `00D10460`, and the eleven counters tile the block. The CLASSIFIED rung lags the row. |
| 1 | `BattleFormulaScratch +0x0A4` `targetDefense` (`CONTRACT-formula-step-table.md`, S-22) | representation known | ctype corrected to `float` (22 of 22 accesses are movss-class). The meaning is "the target's defensive stat", and the name was re-established 2026-09-16. The rung lags. |
| 1 | `ManagerSingleton0209BE80 +0xAB30` `embeddedAB30` (`CONTRACT-widget-object.md`, S-36) | representation known | A container row for a **declared union span**. The extent was measured from a memset length (`0x61F0`), and the overlay arm `overlayWidget0720AB30` is TYPE RESOLVED and carries its tag (`+0x10F68` bit `0x2000`). The DISCOVERED rung is the container row's. |
| 1 | `PhyreClassDescriptor +0x0B0` `unidentifiedListB0` (`CONTRACT-phyre-class-descriptor.md`, S-49) | genuine unknown, bounded and registered: **not critical** | A self-initialised circular list head (`00632E0F`). Teardown drains it without freeing (`00633533`). No inserter has been found, and the residue is register row **BL-8**. Init and drain, the two behaviours the descriptor's lifecycle depends on, are specified. If something does insert, a node loses only its membership at teardown, which the contract already states. |
| 1 | `ManagerSub0209BE80_8FA0 +0x040` `flags` (the 13th 8FA0 row) | representation known | Same `Widget` base copy as the 36 above; `Widget +0x40` is SEMANTICALLY IDENTIFIED. |

## OPUS: the one item that needs work — `SystemStopRecord +0x08`

**Found by the gap-touched list, not by the core list:** the core list skips gap rows by construction.

- **The type row** (`SystemStopRecord +0x08 unobserved08 u8[8]`, DISCOVERED/UNKNOWN) says *"Reached only
  as the high half of the combined record's 16-byte copy."*
- **The contract** (`00-Engine-Core-Runtime/System-Stop-Registry/CONTRACT-system-stop-registry.md` §14)
  says *"The remaining bytes — `+0x08` qword and `+0x15`–`+0x17` — are still unobserved."*
- **The bytes say otherwise.** The contract's own entry `00227680` ("build one id's records", a 28-case
  switch) **stores that qword directly, in both records**:
  - on entry, `00227686 xor eax, eax` / `00227698 mov qword ptr [rdx + 8], rax` and
    `002276A2 mov qword ptr [r8 + 8], rax` write 0;
  - in five switch arms, `002277A1`, `0022793E`, `00227C0E`, `00227C46` and `00227C82` write
    `mov qword ptr [rdx + 8], 0xffffffffffffffff`. Where read (`002277B0`, `0022794D`), each is followed by
    the same store to `[rbx + 8]`, with `rbx = r8` from `0022769C`.
- `r8` is a `SystemStopRecord`: the same function stores the start flag at `00227680+0x30`
  `mov [r8+0x14], r9b`, which the contract already cites.
- The access index carries the six `rdx` stores and **no direct reader** of `+0x08`. The only reads are
  the 16-byte `movups` copies at `00226603`/`00226624`, which the row's own evidence cell cites.
- Read with retool `site` on 2026-10-03. Bit values are not asserted beyond the stores shown.
- **Not a new discovery; a lag.** The page's own access artifact,
  `00-Engine-Core-Runtime/System-Stop-Registry/system-stop-record-accesses.tsv` (rows for `002277A1` and
  `0022793E`, route-seeded), already lists these stores. The row's meaning cell and the contract's §14
  were never brought into line with it.

**What is known and what is not.** The representation is known: a qword the builder writes as 0 or
all-ones, per id, in two records. The high half travels in a 16-byte copy. What is not known is whether
anything reads it after that copy. If a reader exists, a reimplementation of `00227680` that leaves
`+0x08` alone diverges; if none exists, the row is harmless.

**Classification: an access-layer correction, plus one bounded census.** It is not shown to be
reconstruction-critical.

- **Type row, SWE2-STRUCT:** replace "reached only as the high half…" with the builder's stores. It stays
  `u8[8]` or becomes `uint64` at the owner's choice. Meaning is not asserted.
- **Contract §14, FABLE (author, `3d654bb7d`):** strike "still unobserved" for `+0x08` and name the
  stores. Then run the reader census on the 16-byte copy's destination; that census decides criticality.

The second gap-touched row (`MovementContext +0x0E8`, L1 `CONTRACT-actor-record-pool-and-region-map.md`)
is **not** a counter-claim. Its one access is `addr` kind, `00266B26 lea r8, [rax + 0x80]`, the region map
carving an interior pointer. It is not a read or write of the gap bytes.

## OPUS: sampled reads against the contract text (12)

| # | field | contract | reading |
|---:|---|---|---|
| 1 | `EncodedIdQueryRecord +0x3C`…`+0x60` | encoded-id-space | Per-class writer views; downstream meaning a ruled declared limit (§14, FRONTIER 2026-09-29). The contract also states the observable consequence: a class10 fill's stale `+0x5C` is visible to the `002CFF45` diff loop. |
| 2 | `ManagerSub0209BE80_57E0 +0x044` | widget-object | Meaning "Widget +0x44; masked with `and … 0xfff8ffff`". The canonical `Widget +0x44` is TYPE RESOLVED. |
| 3 | `AchievementState +0x024` | shop-stock-ladders | Meaning settled in the row; the rung lags. |
| 4 | `BattleFormulaScratch +0x0A4` | formula-step-table / preparation-step-family | float, the target's defensive stat. `CONTRACT-preparation-step-family.md` §14 records slot 70 storing an immediate `0` to `02AEE05C` (= base `02AEDFB8` + `0xA4`). Consistent with the row. |
| 5 | `ManagerSingleton0209BE80 +0xAB30` | widget-object | A union container with a measured extent; the arm is TYPE RESOLVED. |
| 6 | `PhyreClassDescriptor +0x0B0` | phyre-class-descriptor | Inserter unknown, registered as BL-8. Lifecycle specified. |
| 7 | `SystemStopRecord +0x08` | system-stop-registry | **Correction.** Written by entry `00227680`, see above. |
| 8 | `BattleUnit +0x080` `embeddedBlock0080` | corridor-query-family (tier R) | **Tier-R noise.** The contract cites `+0x80` as the base of an interior pointer (`*(agent+0x108)` = `BattleUnit + 0x80`). The fields it reads through it, `+0x18C`/`+0x190`/`+0x1F4`, are SEMANTICALLY IDENTIFIED (`collisionExtentA`/`B`, `placementMode`). |
| 9 | `GameSettingConfig +0x07C` `valueTableA` | game-setting-config (tier R) | 81 `int32` copied verbatim from `.rdata 01DFDA10` on the no-settings-file branch only. **No reader in the image.** A reimplementation copies the table; its meaning is irrelevant to behaviour. |
| 10 | `BgmStream +0x031` `streamActive` | resource-request-queue (tier R) | Behaviour stated in the row (`003EB0D0` returns 1 if any record's `+0x31` is non-zero, which picks the chunked path) and executed both ways in EXP-146. Only the rung lags. |
| 11 | `MovementContext +0x0E8` | actor-record-pool (L1, gap-touched) | `addr` access only (`lea`), not a byte access. Harmless. |
| 12 | type `RenderResourceEntry` (DISCOVERED at type level) | resource-input-ownership | The fields the contract uses are SIGNATURE RESOLVED or SEMANTICALLY IDENTIFIED (`kind`, `reference`, `resolvedCache`, `sourceSize`, `effectTicket`). Its `unobserved*` words are opaque spans. The type-level rung lags its fields. |

## OPUS: proposed owners

| item | owner | what |
|---|---|---|
| `SystemStopRecord +0x08` row | **SWE2-STRUCT** | access-layer correction: the builder `00227680` stores it (0 at entry; all-ones in five arms), in records A and B |
| `CONTRACT-system-stop-registry.md` §14 | **FABLE** (contract author) | strike "still unobserved" for `+0x08`; reader census on the 16-byte copy's destination decides criticality |
| 37 `Widget`-base copy rows on `…_57E0`, `…_57E0PairRecord`, `…_8FA0` | **SWE2-STRUCT** (hygiene, not blocking) | point each copy row at its `Widget` base row, or lift the rung with it. Note the copies disagree on representation: `_8FA0 +0x098`/`+0x09C` are `uint32` and `+0x0A1` is `uint16`, where `_57E0` has `int16[2]`/`uint8[2]` and `Widget` has `int16`/`uint8` |
| rung-lag rows (`AchievementState +0x024`, `BattleFormulaScratch +0x0A4`, `BgmStream +0x031`, `ManagerSingleton0209BE80 +0xAB30`, type `RenderResourceEntry`) | **SWE2-STRUCT** (hygiene, not blocking) | readiness lags a meaning or extent already in the row |
| `PhyreClassDescriptor +0x0B0` | **OPUS** (BL-8 is already OPUS's register row) | no new work; the census confirms the residue is registered |
| `EncodedIdQueryRecord` tagged slots | none new | declared limit already ruled; tracked under the REOPENED page's OV-5 |

The ten cited types at the lowest rungs are listed in the `.out`. Each was checked only as far as the
contract's use of it; none is used beyond fields that are resolved or a declared opaque span. That is a
reading from the core and sample lists, not a separate pass.

## OPUS: how to re-run

```
python -B "Database/FFXII TZA/_index/candidates/opus-audit-type-residue-1003/type_residue_census.py" > type_residue_census.out
python -B "Database/FFXII TZA/_index/candidates/opus-audit-type-residue-1003/type_residue_census.py" --rows flagged_rows.tsv
```

The script is read-only and takes about 50 s, almost all of it the sibling census's `git log` dates. It
imports two scripts rather than copying them:

- `../opus-audit-l1-contracts-1003/l1_contract_census.py`, for the contract set, MET systems and front matter;
- `Tools/analysis-kit/gfz-scripts/contract_named_state_census.py`, for the tier-S resolution.

`type_residue_census.out` is the run behind this README.

## OPUS: limits

- **Tier A is only as wide as `field-access-index.tsv`**, which covers 205 of 827 types and one base
  register per access. It shows the `rdx`-based stores of `00227680`, not the `r8`/`rbx` ones; those were
  read from the bytes.
- **Tier R is line co-occurrence** (sample 8). Rows reached only through R were read, not trusted.
- **"Not critical" is a reading of the 54 core rows and 12 samples**, not a proof over all 95 flagged rows.
  The other 41 are 34 TYPE RESOLVED placeholder-name rows, plus tier-R and gap rows whose flags are listed
  in the `.out` (`--rows` writes them all).
