# SWE2-AUDIT-SPEC census3: closing census2's blind spot for the types cell, 2026-10-03

*Board `AUDITSEM-REQ-AUDITSPEC-CENSUS2-BLINDSPOT-AND-RULES-1003`, part 1. Drafted by a SWE2-AUDIT-SEM helper for SWE2-AUDIT-SPEC. This is a proposal. It does not edit `L2-VERDICTS.md`, the type store, any page, or census2's script or outputs.*

## SWE2-AUDIT-SPEC run

run: types_census3.py at b0c7c5a57

- **Command:** `types_census3.py --store <HEAD copy>`. The store is HEAD copies of `_types/types.tsv` and `_types/fields.tsv` (`git show HEAD:…`, in `Database/Tools/work/SWE2-AUDIT-SPEC/w10/scratch_c3/headstore/`). This is how the run guards against uncommitted type-store edits in the shared worktree.
- **The final run was at `b0c7c5a57`.** By then the worktree had no uncommitted `_types/`, contract, `L2-VERDICTS.md` or registry changes.
- **An earlier run at `86cdcde10` gave the same classes.** That run was taken while a peer's store and four contract edits were still uncommitted, and the HEAD-text check of those four contracts (`scratch_c3/headcontracts.py`) read `SAME`. Diffing it against the final run, the only differences are three field *names* the peer's commit `b0c7c5a57` renamed: `02099DA0`, `01F7F4C0` and `01F7F598` are FIELD in both runs.
- **Selftest:** census3 **25/25 PASS**, and census2's own embedded selftest, run from the imported module, 11/11 PASS.
- **Run line, copied from the output:** `rows 1433 {'FIELD': 598, 'PTR-CELL': 25, 'UNATTRIBUTED': 780, 'RANGE-START': 1, 'RANGE-END': 4, 'GAP-SPAN': 13, 'UNDECLARED': 10, 'OBJECT': 1, 'AMBIGUOUS-DEREF': 1}`. The 780 UNATTRIBUTED rows stand for 961 offsets, because one BARE-OFFSET row carries a line's whole count.
- **Contract-cell references:** `unresolved contract-cell references: 0 []`.
- **Systems with UNDECLARED/UNTYPED/OUT-OF-EXTENT:** `['S-16', 'S-36', 'S-44']`. Census2 on the same day gave `[]`.
- **Systems with NO-ROW/GAP-COARSER/WIDER-THAN-FIELD:** `['S-25']`.
- **Outputs, in this folder:** `census3.tsv` (one row per item, with `kind` = which form found it and `credited` = `col6` or `cell`), `census3_systems.tsv`, and `census3_unattributed.tsv`.

## SWE2-AUDIT-SPEC forms covered, and the fixture control for each

census2's classes, its OBJECT (bare-base) rule and its ruled sections are kept unchanged. The ruled sections are `contract_named_state_census.state_sections`. Census2 is imported, not copied: its `extract_new` is the "old" side of every control, so the controls compare against the published extractor itself.

| form | what census3 does | fixture: census3 finds / census2 misses |
|---|---|---|
| lower-case and all-caps record names | resolves the name **only** through `ALIASES3` (27 entries, each quoting the contract text that binds it, e.g. `unit` = `BattleUnit`, `BKEI` = `SpawnRecord` in the enmity contract). CPU registers are skipped and counted. Any other name becomes UNATTRIBUTED `LC-NAME`. An English word before an offset ("the byte at +0x5A90") becomes `PROSE-OFFSET` | `unit + 0x698` → `BattleUnit +0x698` / missed |
| continuation offsets | `unit +0x00, +0x10, +0x40`, `+0xBC/+0x13C`, and the possessive "the unit's +0x6B7" | `+0x10` and `+0x40` found / missed |
| fenced layouts without a type-name head | the head resolves, in order, by: a leading type or alias; a pointer-cell route at the head's address (refused when the head indexes rows but the route points at one object); a span base (dereferenced through a typed pointer when the head reads `[ADDR]`); the single type named on the line; or `alias + 0xNN` whose field is a typed pointer. Rows under an unresolved head are UNATTRIBUTED `LAYOUT-HEAD`. Multi-offset rows (`+0x069 / +0x079`) are split | `records: *(char**)0x0208E690 …` → `SpawnRecord +0x08`; `the stats (unit + 0x698)` → `BattleStatsRecord +0x194` / both missed |
| C-struct comments | `struct X { … /* +0xNN */ };` | `WidgetMessage +0x08` / missed |
| head-less `\| +0xNN \|` tables | the single declared type named in the paragraph before the table. The width comes only from a column the header calls size/width or type. Otherwise the row is UNATTRIBUTED `TABLE` | `AuthoredTableHeader +0x04` attributed / census2 leaves it unattributed |
| globals named by symbol | `DAT_`/`uRam_`/`PTR_…_ADDR` carry their address. A `g_name` resolves through the store's STATIC routes first, then through a page line that **binds** the symbol to one data address (only separators and a type word between the two; `_index/` pages excluded). Otherwise the symbol is UNATTRIBUTED `SYMBOL` | `DAT_02089300` found; `g_nSpawnKeepReturnWindow` → `0208936C` / both missed |
| slash lists | each suffix replaces the low digits: `02EBF150/168/148/140`, `` `02AEE054`/`58`/`5C` `` | `02EBF168`, `02EBF148`, `02EBF140`, `02AEE058` and `02AEE05C` found / missed |
| `ADDR[n]` | the element size comes from a width word before the address, or from the declared array field at ADDR. With neither, the index is UNATTRIBUTED `INDEX-UNSIZED` | byte `0209A2C4[2]` → `0209A2C6` / missed |
| contracts credited only in the L2 contract cell | contract names in the cell's **unstruck** text, resolved over the 107 `CONTRACT-*.md` files (basenames are unique) | router contract credited to S-36; a struck mention not credited; census2 does not credit it |
| anything left over | **catch-all:** on every ruled line, `+0xNN` offsets that no extractor consumed, and that are not a code-site `ADDR+0xNN`, are counted as UNATTRIBUTED `BARE-OFFSET` | n/a, so nothing goes uncounted |

The controls also have negative cases, and all pass: a register offset is not a record, an unknown lower-case name is UNATTRIBUTED, and an unsized index is UNATTRIBUTED.

**Width-aware flags.** These apply where the contract states a width:
- `GAP-EXACT`: a gap row of exactly the named extent;
- `GAP-COARSER`: a gap row wider than the named item;
- `NO-ROW`: no field row at all;
- `WIDER-THAN-FIELD`: some of the named bytes are not in a named field.

They are worklist flags. Struck (superseded) types are ignored when the width is read.

## SWE2-AUDIT-SPEC systems with real findings (MET cells first)

Each finding was checked by hand against the contract line, the HEAD store and the image.

| system | types now | finding | verified | proposal |
|---|---|---|---|---|
| **S-44** | **MET** | `CONTRACT-game-setting-config.md` §5 State, the *written* row: "on the `FrameLimit` path `0x01DFE0B4/B8/BC`, `0x01F82E38/3C/40`". The slash list expands to `01F82E3C` and `01F82E40`, and both resolve **UNDECLARED**. (`01DFE0B4`, `B8`, `BC` and `01F82E38` are declared.) | **real.** Decoded from `001EDDC0`, the FrameLimit apply: `001EDE01 cmp byte [01F82E3C], 0`; `001EDE0A mov ecx, [01F82E40]`; `001EDE10 mov byte [01F82E3C], 0`; `001EDE3A mov [01F82E40], eax` (after the `timeGetDevCaps` import call `008C2A90`); `001EDE46 mov byte [01F82E3C], 1`. These are the "timer period raised" byte and `wPeriodMin` dword (`what-the-engine-fixes-at-boot.md` lines 500–507, `game-settings-ini-and-runtime-config.md` lines 517–526). Neither has a row in the HEAD store | **types MET → PARTIAL**: two contract-named globals undeclared, a byte at `01F82E3C` and a dword at `01F82E40`. **L2 MET → NOT MET** (its other cells are MET, plus LIVE with its ruling cited) |
| S-16 | PARTIAL | `g_nSpawnKeepReturnWindow` (§5, by symbol) → `0208936C` via `spawn-placement-and-retirement.md` (`\| \`0208936C\` \| \`g_nSpawnKeepReturnWindow\` (i32) \|`), UNDECLARED | real; agrees with SWE2-AUDIT-SEM's hand finding (`auditsem-types-rescore-2-1003`) | none: already PARTIAL for this item |
| S-25 | PARTIAL | (1) enmity layout `BKEI +0x1A` (u8 threat vector) lands in `SpawnRecord +0x01A unobservedSpan001A` u8[6], flag `GAP-COARSER`; (2) gambit-walk `set + 0x20` `AiOrderRecord[14]` (336 B) has 48 bytes that are not in a named field (`unobservedTail0140`), flag `WIDER-THAN-FIELD` | real; both agree with the hand finding | none: already PARTIAL |
| S-36 | PARTIAL | the router contract, credited only in S-36's contract cell: its §5a State names `0215F1A0`, `0215F1A1`, `0215F1A4`, `0215F1A8`, `020927D8` and `01E0C2C0`/`01E0C2C4` (the inhibit table), all UNDECLARED | real; agrees with the hand finding | none: already PARTIAL |

**Over-match corrected during the run.** Every candidate hit was hand-read, and these three were wrong:
- **S-12, UNTYPED `ActorManager +0x10`.** It is not a finding. The weather contract calls the record "ActorManager". `002620E0(rcx = ActorManager record)` tests `[rcx+0x28]` (`002620E6`) and sets bit 4 of `[rcx+0x10]` (`002621A4`, decoded), which are `ActorManagerSlot +0x028 slotIndex` and `+0x010 slotFlags`, both declared. An evidence-backed `ALIASES3` entry now resolves it FIELD.
- **S-37, OUT-OF-EXTENT on `TextPainterPointer`.** The head `[0209CC40]` dereferences the cell. That rule was added, and the rows now resolve as `TextPainter +0x10C8/+0x10E8/+0x10FC` FIELD.
- **S-29, `AuthoredTableHeader +0x0`.** The head is "character class row `02EBF130`, indexed by …". That is a row of the table, not its header, so the head is refused, and the row is counted as UNATTRIBUTED.

**GAP-SPAN rows (13), all read.**
- 7 `GAP-EXACT`: S-09 `+0x02`, S-20 `BattleTargetEntry +0xC`, S-33 ×2, S-39 ×3.
- S-17's ledger padding (exact by the contract's own `+0x11..+0x17`).
- 4 on S-08 `ResourceRequestSlot +0x68..+0x6F`/`+0x78..+0x7F`. Those are the two ends of each range, and the contract itself says *"Unobserved … do not invent semantics"*.
- S-25 (above).

Only S-25's are coverage findings.

## SWE2-AUDIT-SPEC proposed re-scores (not applied)

1. **S-44 types MET → PARTIAL; S-44 L2 MET → NOT MET.**
   - Evidence: `CONTRACT-game-setting-config.md` §5 names `0x01F82E38/3C/40` as written state, and `01F82E3C` (u8) and `01F82E40` (u32) have no declaration in the HEAD store. The image sites are listed above.
   - Under the accepted criterion, one undeclared contract-named item makes the cell PARTIAL. This is the S-46 precedent, and the two cells are the same kind of scalar it closed with one-dword declarations.
   - Closes with two scalar declarations (owner: the type store). The cells, with the existing text struck: types `**PARTIAL — re-scored 2026-10-03 (SWE2-AUDIT-SPEC, census3 auditspec-census3-1003):** §5 names 0x01F82E38/3C/40; 01F82E3C (u8, 001EDE01/001EDE10/001EDE46) and 01F82E40 (u32, 001EDE0A/001EDE3A) are undeclared`; L2 `**NOT MET — the types cell is PARTIAL (…)**`.

No other MET types cell shows a contract-named undeclared item in census3.

**Disposition of item 1 (2026-10-03, before this package was published):** SWE2-STRUCT declared both cells in `c725c29cf`
as `TimerPeriodRaised` (u8, STATIC 0x01F82E3C) and `TimerPeriodMin` (u32, STATIC 0x01F82E40). The record is
`swe2struct-framelimit-timer-cells-1003`. S-44's types and L2 cells therefore stay MET, and the re-score above is not
applied. A census3 run at or after `c725c29cf` reports no undeclared item for S-44.

## SWE2-AUDIT-SPEC what census3 still cannot see (control against the hand findings)

SWE2-AUDIT-SEM's hand sweep of the twelve formerly PARTIAL rows found residuals in seven systems. Census3 is checked against that published list:

| hand residual | census3 |
|---|---|
| S-16 `g_nSpawnKeepReturnWindow` | **caught** (SYM) |
| S-16 the format-class-0 candidate record | missed. The record is named in prose with no type, so its `+0x00`/`+0x10` count as PROSE/BARE-OFFSET |
| S-22 the recipe blob layout (`recipe blob i32[...]`) | missed. A prose layout with no offsets is not a form any regex can type |
| S-25 the threat vector; `AiOrderRecord[14]` | **both caught** |
| S-28 camera context 0's `+0x850` float | missed. "its `+0x850` float" is counted as `PROSE-OFFSET` |
| S-31 the §8a.2 node-table fields | missed by design. `## 8a` is outside the ruled sections census2 defined, and this task keeps them |
| S-36 the router §5a state | **caught** (CELL) |
| S-45 manager `+0x18`; Steam context `+0x28` | missed. Both are offsets in the middle cells of an object table, and are counted as `BARE-OFFSET` |

**4 of the 7 systems' residuals are caught, 3 are not.** A zero from census3 is therefore still not a types MET. It can rule a cell PARTIAL, and its UNATTRIBUTED residue is the remaining hand-read list.

**Two systems have no ruled section at all.** S-23 (`CONTRACT-hp-write-and-lethal-transition.md`: §3 is "The flag word") and S-48 (`CONTRACT-authored-command-ramp-channels.md`: §1 "The table") yield **0 ruled lines** in census2's grammar, so both censuses measure nothing for them. Both types cells read MET. Under precision 2 of the ruling, a contract whose state enumeration cannot be found is unscorable rather than vacuously MET. These two need a hand read, or a heading ruling. That belongs to part 2 (rules), not to this census.

## SWE2-AUDIT-SPEC residual UNATTRIBUTED counts

Copied from `census3_unattributed.tsv`: **961 offsets**.

| kind | offsets | what it is |
|---|---|---|
| BARE-OFFSET | 429 | an offset with no name on the line: object tables, sentence lists |
| PROSE-OFFSET | 232 | the offset follows an English word; the record is named earlier in the sentence |
| LC-NAME | 103 | a lower-case name with no binding in `ALIASES3` (`ctx`, `st`, `fl`, `row`, `descriptor`, …) |
| TABLE | 101 | an offset table with no single type in the paragraph before it |
| LAYOUT-HEAD | 85 | a fenced layout whose head does not resolve |
| WIDTH-OFFSET | 11 | `byte[+0x80]` with no record |

Per system:

| | | | | | | | | |
|---|---|---|---|---|---|---|---|---|
| S-01 0 | S-02 144 | S-03 6 | S-04 0 | S-05 0 | S-06 6 | S-07 37 | S-08 6 | S-09 13 |
| S-10 6 | S-11 18 | S-12 28 | S-13 11 | S-14 4 | S-15 13 | S-16 2 | S-17 8 | S-18 18 |
| S-19 21 | S-20 36 | S-21 14 | S-22 13 | S-23 0 | S-24 33 | S-25 2 | S-26 40 | S-27 17 |
| S-28 5 | S-29 29 | S-30 4 | S-31 6 | S-32 28 | S-33 2 | S-34 14 | S-35 16 | S-36 54 |
| S-37 27 | S-38 59 | S-39 8 | S-40 6 | S-41 21 | S-42 11 | S-43 1 | S-44 10 | S-45 19 |
| S-46 2 | S-47 0 | S-48 0 | S-49 89 | S-50 3 | S-51 30 | S-52 21 | | |

The largest are S-02 (144, mostly the per-frame gate's group-handler tables), S-49 (89) and S-38 (59). Census3 classifies none of these offsets, so they do not support a MET cell either way.

## SWE2-AUDIT-SPEC limits

- `ALIASES3` is hand-built from the contracts' own bindings: 27 entries, every one quoting its text. A wrong entry would mis-type rows, so each finding must be hand-read, as the three corrected over-matches show.
- The `g_` page rule accepts one bound address, or a 3:1 majority. `_index/` pages are excluded because verdict prose quotes addresses beside symbols. One symbol was resolved this way (`g_nSpawnKeepReturnWindow`).
- Widths are taken only from the first token after an offset, or from a table column the header names. Prose widths are not inferred.
- What is still not read: state named only in words, layouts given in prose, and sections outside the census2 grammar (S-31 §8a, S-23, S-48).
- Default `--store` is the worktree store, like census2. The committed run above used `--store`.

## SWE2-AUDIT-SPEC files

- `types_census3.py`: the census, with the embedded controls (`--selftest` runs only those).
- `census3.tsv`, `census3_systems.tsv`, `census3_unattributed.tsv`: the outputs of the run above.
- Scratch, not part of the package, in `Database/Tools/work/SWE2-AUDIT-SPEC/w10/scratch_c3/`: `headstore/` (the HEAD store copy), `run.log`, `namectx.py` (the alias-binding reader), `headcontracts.py`.
