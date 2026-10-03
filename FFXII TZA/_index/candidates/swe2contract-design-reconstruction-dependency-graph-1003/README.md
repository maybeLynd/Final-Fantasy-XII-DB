# Reconstruction dependency graph: design note (SWE2-CONTRACT, 2026-10-03)

**Request:** FABLE, relaying the user's addendum
`Database/Tools/work/FABLE/FFXII_PROJECT_IMPROVEMENT_ADDENDUM_2026-10-03.md` §4 ("Reconstruction readiness dependency
graph"), with §16 (priority **P2**: it must not delay database completion) and §17 (implementation discipline).
Board task `SWE2CONTRACT-DESIGN-RECON-DEPGRAPH-1003`.
**Author:** a Claude stand-in operating the SWE2-CONTRACT lane while its Devin session was rate-limited.
**Status:** DESIGN NOTE. Nothing here is implemented, and nothing here is a completion metric. Measurements were taken
at HEAD `df9b40bec` against the live call graph (`Database/Tools/work/graph/functions.tsv` sha256 `c0e1de8f650f2e8d…`,
`edges.tsv` `de21ba1bc62d9224…`).

## 1. What already exists (SWE2-CONTRACT, §17 steps 1-3)

There is no dependency graph today. The neighbouring tools answer different questions, so this design **extends
them**:

| existing artifact | what it answers | what it does not |
|---|---|---|
| `_index/RECONSTRUCTION-ROADMAP.md` + `readiness_rank.py` → `_index/READINESS-RANK.tsv` | how close each category is, by preconditions (contracts, types, fields, coverage) | what a category needs first |
| `_index/RECONSTRUCTION-READINESS-GATE.md` | the per-system gate verdicts | ordering between systems |
| `_index/completion-packages/PKG-*.md` | hand-written package records; each has a **dependencies** field ("other packages, contracts or verdict cells relied on, with the scope at which they are accepted", `completion-packages/README.md` §1) | a machine view across packages |
| `audit_crossrefs.py` check 4 + `_index/candidates/neighbour-dispositions.tsv` | every page→layer crossing, dispositioned and **direction-labelled** | an aggregated layer→layer view |
| `knowledge.sqlite` (`knowledge_db.py`) | the joined mirror of the tables below | anything newer than its last build: provenance says 2026-09-25, pinned `ed275f2e9` |

This design adds **one generator** whose output feeds the existing dashboard build and the roadmap. It adds no board,
no dashboard, no scheduler and no gate.

## 2. Evidence sources for edges (SWE2-CONTRACT)

Each source below is already structured and already carries its own provenance. The generator reads the authoritative
file, not the mirror. Where the mirror is used for a join, it calls `knowledge_db.freshness_report` first and emits
`STALE` if any input moved (`_index/DERIVED-DATA.md`, "What readers must do").

| # | source (authoritative file → mirror table) | edge it yields | direction rule |
|---|---|---|---|
| S1 | `Database/Tools/work/graph/edges.tsv` + `functions.tsv` (DumpFullCoverageGraph; gitignored, fingerprinted) → `edges`, `functions` | **call**: caller's layer needs callee's layer | caller → callee. Layer = the `owner` column mapped through `_index/CODEDOMAIN-OWNER-MAP.tsv` (`owner_token` → `category_dir`) |
| S2 | `_index/candidates/neighbour-dispositions.tsv` (3,141 rows: page, far layer, edge count, source, example pair, verdict, note) | **call, dispositioned**: the same crossing as S1, but already read by a lane and labelled | the label is relative to the page. Inbound edges mean the far layer is a **CLIENT** of the page's subject; outbound edges mean the far layer is a **SERVICE** to it (`pass22_neighbour_bullets.py` line 15 and its self-test at line 283). **MECHANICAL** means every edge runs through a named accessor |
| S3 | `_types/field-access-index.tsv` (28,884 rows: type, disp, base, kind, function, site, instruction) joined to `_types/types.tsv` (`category`, `documents`) → `field_access`, `types` | **type-layout**: a function that reads or writes a record needs the layer that owns the record's layout | accessing function's layer → the type's `category` |
| S4 | `01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-dispatch.tsv` (call_id → handler, owner; handler re-derived from the dispatch table) → `script_verbs` | **script-binding**: verb *n* is served by a handler in layer L | script VM → handler layer. Always **sequencing** (§4) |
| S5 | `CONTRACT-*.md` (120 contracts): front matter `category:`, `entries:`, `implements:`; template §3 Types, §5 State (read/written), §6 Relationships, §8 Script · resource · event interactions (`_templates/CONTRACT.md`) → `documents`, `contract_sections`, `citations` | **contract**: a contract's §3/§5 types and §6/§8 cited entries name what it consumes | contract → the owner of each cited entry or type; the citation is the contract line |
| S6 | `_index/completion-packages/PKG-*.md`, the **dependencies** field | **declared**: package → package or contract | as declared. These are already reviewed, so they become hard edges with `evidence_class=declared` |

Not used: folder numbers or folder order (addendum §4 requirement 1); EH funclet edges (CONTRACT template §6 bans them
as semantic evidence; the generator drops callers carrying the EH tag); and any edge whose callee has more than 100
callers. That hub threshold is the one `audit_crossrefs` already measured and uses (`neighbour-dispositions.tsv`
header: p99.9 = 461 callers, 74 functions above 100). Substrate (`22`, `23`, `24`) is kept as nodes but is reported as
a shared base (§5).

## 3. Node set (SWE2-CONTRACT)

**Level 0: category nodes.** One node per category folder. The addendum's node classes map onto the existing folders
as follows. The mapping lives in one small TSV next to the generator, and `CODEDOMAIN-OWNER-MAP.tsv` stays the only
owner→folder map.

| addendum class | node(s) |
|---|---|
| core runtime / scheduling | `00-Engine-Core-Runtime` |
| memory / object / ownership foundations | `00-Engine-Core-Runtime` (Object-Model) and `24-Compiler-And-CRT-Runtime` (Memory-And-Allocation). This is the one class that spans two folders, so it is kept as two nodes plus a recorded grouping, never a merged node |
| resource loading / binding | `02-Resource-And-Asset-Pipeline`; containers `25-EBP-Script-Container` and `26-PKFL-Package-Container` |
| ScriptVM / native bridge | `01-Script-VM-Native-Bridge` |
| actor / entity | `04-Actor-Entity` |
| world / area | `03-World-Area-Field` |
| (spawn lifecycle: a folder with no addendum class) | `05-Spawn-Encounter-Lifecycle` |
| movement / navigation | `06-Movement-And-Navigation` |
| combat action / formulas / AI-Gambits / status-terminal | `07` / `08` / `09` / `10` |
| party / items-equipment-license / rewards-economy / story-quest-hunt | `11` / `12` / `13` / `14` |
| input / UI / rendering-presentation / audio / save-load | `15` / `16` / `17` / `18` / `19` |
| RNG | `21-RNG-And-Determinism` |
| platform / third-party substrate | `20`, `22-Middleware-PhyreEngine`, `23-Third-Party-Libraries`, `24` |
| (none) | `99-Unresolved-Residual` is **not a node**. An edge ending there is reported as `unresolved-endpoint` |

**Level 1: package nodes.** Contracts (`CONTRACT-*.md`) and completion packages (`PKG-*`), each with its level-0 node as
an attribute. Real reconstruction packages are drawn at this level (§5 explains why level 0 cannot draw them).

**Near-end attribution.** 28,752 of the graph's functions have no `owner` (knowledge.sqlite `functions`, 2026-09-25
build). An edge whose near end is unowned may be attributed to a page's category only through an S2 row, because the row
is that page's statement about its own subject. If more than one category claims the same unowned function, the edge
is marked `ambiguous`, kept out of hard edges, and listed as a classification lead for the ledger owner. Example: the
unowned `00263990` (worked example E5) is a subject of S2 rows on three pages in `01`, `04` and `05`
(`neighbour-dispositions.tsv` lines 703, 750 and 2830).

## 4. Edge schema (SWE2-CONTRACT)

One row per (from, to, kind, basis) at each level, aggregated from function- or type-level evidence:

| column | meaning |
|---|---|
| `from` | the **dependent** node (it needs `to`) |
| `to` | the prerequisite node |
| `kind` | `hard`: `from` cannot be reconstructed faithfully without `to`'s contract (or a stub written to it). `sequencing`: building `to` first is convenient, but `from` can be built and tested without it |
| `basis` | `call` / `call-dispositioned` / `type-layout` / `script-binding` / `contract` / `declared` |
| `evidence_class` | the addendum's §0 vocabulary: `static` for S1-S5 (shipping-byte instruments), `declared` for S6, and `live` or `isolated-original-code` only where a cited record says so. Never summed across classes |
| `tier` | the tier the source states (S2 notes say "tier 1 (body read)" or "tier 2: ledger names…"); blank when the source states none |
| `count` | the number of underlying function- or type-level facts. Reported, **never** used as a classifier (§5) |
| `representative` | one concrete fact, e.g. `00427320 -> 002ED570 call at 00427481` |
| `citation` | `path:line` of the source row or page line at the pinned commit, plus the input fingerprint |
| `flags` | `owner-conflict` (ledger owner ≠ the category of the page that claims the function), `ambiguous`, `unresolved-endpoint`, `substrate` |

**The hard/sequencing rule**, per fact and never by count:
- **hard:** an S1 or S2 outbound (SERVICE) call to a non-accessor body; an S3 read or write of a field the type's owner
  documents; an S5 §3/§5 type or §6 entry; an S6 declared dependency.
- **sequencing:** an S2 **MECHANICAL** fact (a named shared accessor, which a reconstruction inlines or reuses); an S4
  script binding (the interpreter is reconstructable without the handler; only that verb's integration needs it); an
  indirect dispatch or callback, where the prerequisite's registration point has to exist before integration but its
  behaviour does not.
- An S2 **CLIENT** label is not a new edge. It is the same crossing seen from the other page, so it confirms the reverse
  edge's direction and is used only as a cross-check.

## 5. Why level 0 cannot draw packages, and what can (SWE2-CONTRACT)

Measured with S1 only (owned ends only, EH not yet filtered, hubs above 100 callers excluded): **2,614 cross-category
call edges over 210 directed category pairs**, across 22 nodes (21 folders, plus the owner token
`Story_Event_Quest_Hunt`, which has no row in the owner map and so stands as its own node; see §10). The strongly connected components depend entirely on an arbitrary count
cut:

| cut: keep a category pair if it has ≥ N calls | the largest SCC |
|---|---|
| N = 3 | **19 of 22 nodes**: everything except `02`, `18` and `21` |
| N = 3, dropping `01`'s outbound edges (verb handlers) | 17 nodes; `01` falls out |
| N = 10 | 9 nodes: `00 01 03 04 05 06 07 11 17` |
| N = 25 | two pairs: `04 06 11` and `00 17` |

So a count threshold invents structure, which is exactly what §4 forbids, and raw calls make the whole game one
cluster. The design therefore:
1. **classifies each fact** as hard or sequencing (§4) before aggregating, and drops sequencing facts from the
   component computation;
2. treats `00`, `22`, `23` and `24` as a **shared base layer** that every package may depend on. They are reported, not
   used to merge components;
3. **condenses SCCs** on the hard subgraph. Each SCC that remains is a **co-reconstruction cluster**: its members are
   built together or against each other's contracts as stubs. That is a finding to show, not a defect to hide;
4. emits **topological layers** of the condensation as the integration order, and **weakly connected components**
   (base layer excluded) as candidate independent packages;
5. draws packages at **level 1**. A contract's hard edges come from its own §3/§5/§6 citations (S5), which are far
   sparser than a whole category's call surface. A completion package inherits its declared S6 edges.

## 6. Outputs (SWE2-CONTRACT)

- `_index/reconstruction-dependency-graph.tsv`: the §4 rows, levels 0 and 1, sorted. Header comments carry the input
  fingerprints, the generator's sha256 and `built_at`, the same shape as knowledge.sqlite `provenance`.
- `_index/reconstruction-dependency-graph.json`: nodes (with READINESS-RANK signals and level-1 package stage attached
  read-only), edges, SCCs, layers and components. This file is the **generation input** for the existing dashboard build:
  "ready now" means every hard prerequisite meets the readiness the user chooses at authorization, then come "blocked
  by", "prerequisite chain" and "integration order". It is consumed after DB readiness (addendum §4 "Dashboard use");
  before then, it is a planning view only.
- No page edits. The roadmap may link the TSV; it does not copy numbers from it.

## 7. Checks (SWE2-CONTRACT)

The generator's self-test and output gate:
- **C1, no folder-order edges.** No edge is derived from folder numbers. A mutation test renumbers two folders in a
  fixture and asserts the edge set does not change.
- **C2, every edge cited.** Each row's `citation` resolves to an existing path and line at the pinned commit, and the
  cited line contains the `representative` addresses. Rows from S1 cite the fingerprinted `edges.tsv` row.
- **C3, the direction self-test.** A fixture with one inbound and one outbound S2 row yields exactly one hard edge,
  in the outbound direction (mirrors `pass22_neighbour_bullets.py`'s label self-test).
- **C4, classifier sensitivity.** A fixture whose only fact is MECHANICAL yields no hard edge; flipping it to SERVICE
  yields one. This is a control the defect would move (a count-based classifier fails it).
- **C5, freshness.** If any input fingerprint differs from the recorded one, the output says `STALE` and names the
  moved inputs, per `DERIVED-DATA.md`.
- **C6, no silent attribution.** `owner-conflict` and `ambiguous` rows are listed. They are never dropped and never
  resolved by the generator.

## 8. Worked example: five real facts, verified (SWE2-CONTRACT)

Each fact was checked against the shipping executable with `disasm_fn.py` (or a direct read of the dispatch slot) and
against the cited row at HEAD `df9b40bec`.

| # | from → to | kind / basis | fact | citation |
|---|---|---|---|---|
| E1 | `08-Combat-Formula` → `10-Status-Periodic-Terminal` | hard / type-layout | `BattleFormula_BuildCandidateStatusMask` `003851F0` (owner CombatFormula) reads `StatusDefinitionRecord +0x06` (`classWord`) at `0038540C`: `test word ptr [rcx + 6], r14w` (bytes `66 44 85 71 06`) | `_types/field-access-index.tsv:24985`; type `_types/types.tsv:236` (category `10-…`, documents `CONTRACT-status-write.md`); field `_types/fields.tsv:2400` |
| E2 | `07-Combat-Action` → `02-Resource-And-Asset-Pipeline` | hard / type-layout | `BattleAction_ComputeChargeLimitTicks` `002F8410` (owner CombatAction) reads `AuthoredTableHeader +0x04` (`recordCount`) at `002F8432`: `mov ecx, dword ptr [r8 + 4]` | `field-access-index.tsv:2096`; `types.tsv:208` (documents `authored-data-table-registry.md`); `fields.tsv:253` |
| E3 | `06-Movement-And-Navigation` → `04-Actor-Entity` | hard / type-layout | `FUN_00310920` (owner Movement) read-modify-writes `BattleUnit +0x000` (`unitFlags`) at `00310AF1`: `or qword ptr [rdi], 0x4000000` | `field-access-index.tsv:4872`; `types.tsv:192` (documents `battleunit-slot-pool-and-actor-class.md`); `fields.tsv:458` |
| E4 | `17-Presentation-Rendering` (ledger) or `07-Combat-Action` (page) → `02-Resource-And-Asset-Pipeline` | hard / call-dispositioned, **flag `owner-conflict`** | `00427320` calls `ResourceTable_ResolveEntryByIndex` `002ED570` at `00427481`. The S2 row labels it SERVICE (outbound). The ledger files `00427320` to Presentation, while the citing page treats it as a battle-action handler reached from the dispatch ("The dispatch owns the handler") | `neighbour-dispositions.tsv:826`; `07-Combat-Action/Action-Dispatch/battle-action-handler-table.md:701-703` |
| E5 | `05-Spawn-Encounter-Lifecycle` (page-attributed; also claimed by `01` and `04`) → `14-Story-Event-Quest-Hunt` | hard / call-dispositioned, **flag `ambiguous`** | the unowned `00263990` calls `PersistentFlag_QueryBank2048` `0032A930` at `002639BA` (SERVICE, tier 1, body read) | `neighbour-dispositions.tsv:750` (and 703, 2830); `05-…/Spawn-Record/the-spawn-keep-entry-field-map.md:417` |

Two contrasting facts that must **not** become hard edges:
- **Sequencing / script-binding:** verb `0001` `setpos` is served by `FUN_0034EBC0` (owner Movement). The handler pointer
  read from the dispatch slot at `01EED740` (table `01EED700`, record stride 0x20) is `0034EBC0`
  (`scriptvm-dispatch.tsv:121`). The interpreter does not need Movement; only the verb's integration does.
- **Sequencing / MECHANICAL:** `FUN_002B58F0` calls `ImageAddress_ResolveRuntimePointer` `0020E600` (owner
  CoreRuntimeScheduling, 10 bytes). The S2 row says "SERVICE, mechanical: 15 edges decode via …"
  (`neighbour-dispositions.tsv:854`). That is a shared accessor, not a prerequisite on core runtime.

E4 and E5 show why §3's attribution rules and §7 C6 exist: the plain owner join would have produced `17 → 02` without
comment and missed `05 → 14` entirely.

## 9. Non-goals (SWE2-CONTRACT)

- Not a completion metric, not part of `goal_gate.py`, and no input to DB_GOAL or to any L1/L2 verdict.
- Not a schedule. It does not assign work and does not touch the board.
- No new dashboard, board, scheduler or completion policy. The JSON feeds the existing atomic dashboard build.
- No ownership changes. `owner-conflict` and `ambiguous` rows go to the ledger owner as leads, and the generator
  never re-files a function.
- No L3 work. Using the graph for reconstruction waits for the user's authorization (addendum §0).
- No edges from prose that is not a template section or a labelled S2 row, and none from folder order.

## 10. Known gaps found while designing (SWE2-CONTRACT)

- `CODEDOMAIN-OWNER-MAP.tsv` has no row for the owner token `Story_Event_Quest_Hunt`, which 15 functions in the live
  `functions.tsv` carry. Until it is mapped, those ends are `unresolved-endpoint`. Owner of the map: SWE2-EC7.
- S5 parsing depends on contracts using the template's section numbers; contracts on an older layout supply only their
  front-matter `entries:`. The generator should report per contract which sections it read.
- knowledge.sqlite was last built 2026-09-25 (`ed275f2e9`). A mirror-based run reports STALE until it is rebuilt.

## 11. Minimal generator, if built (SWE2-CONTRACT)

Proposed home: `Database/Tools/analysis-kit/gfz-scripts/recon_depgraph.py` with `test_recon_depgraph.py` (C1-C6 on
fixtures). Read S1-S4 and S6 first; S5 is the last increment. It reuses `kit_paths`, `knowledge_db.freshness_report`
and the S2 label semantics of `pass22_neighbour_bullets.py`, imported rather than copied, so the label rule cannot
drift.
