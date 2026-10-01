# FFXII TZA — Engine Systems Database

A complete, evidence-backed reference to how *Final Fantasy XII: The Zodiac Age* actually
works at the native-code level, written so a modder can open any folder and learn a system
well enough to change it correctly.

**That standard is Level 1 of three.** Since 2026-09-08 the database is also the canonical
specification for reconstructing the game in maintainable source, validated against the original:

| level | bar |
|---|---|
| **L1 MODDING-GRADE** | understand a system well enough to change it correctly — *the original standard, unchanged* |
| **L2 RECONSTRUCTION-GRADE** | L1 plus enough to reproduce the behaviour independently: types, contracts, relationships, runtime evidence |
| **L3 PARITY-CERTIFIED** | implemented independently and compared against the original within stated parity dimensions |

Reconstruction-grade knowledge makes modding **more** powerful, not less relevant. Authority:
[`../../RECONSTRUCTION-CHARTER.md`](../../RECONSTRUCTION-CHARTER.md); the audit that produced the
revision is [`_index/GOAL-REVISION-2026-09-08.md`](_index/GOAL-REVISION-2026-09-08.md).

**Source of truth:** the GFZ/GZF V121 reconstruction of `FFXII_TZA.exe` — 38,161 functions,
Ghidra image base `0x00120000`, authorized binary SHA-256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.

Nothing in this database is allowed to be a guess. See
[`_index/EVIDENCE-STANDARD.md`](_index/EVIDENCE-STANDARD.md).

---

## How to use it

Folders are engine categories. Inside each, folders are **systems**. Inside those, either
more subsystem folders or `.md` files documenting one mechanism each.

Every system document answers the same questions in the same order:

1. **What the player sees** — the in-game behaviour this produces
2. **Native mechanism** — what the code actually does
3. **Key addresses** — entry points, with body size and role
4. **Data structures** — records, offsets, bitfields, tables
5. **Call chain** — the full upstream → downstream order, both directions
6. **Modding notes** — where to intervene, what regenerates itself, what breaks
7. **What is not known** — explicitly, so nothing is silently assumed
8. **Evidence** — how each claim was proved

If a document does not have all eight, it is marked `STUB` or `PARTIAL` and is tracked in
[`_index/OPEN-QUESTIONS.md`](_index/OPEN-QUESTIONS.md).

---

## Start here

**Concurrent researchers:** begin at the [team operating protocol](_index/_inbox/TEAM.md) (eleven fixed identities since 2026-09-13)
and check [current claims](_index/_inbox/TEAM.json) before substantive work.

| Document | Purpose |
|---|---|
| [`_index/COVERAGE.md`](_index/COVERAGE.md) | Live completion ledger — what fraction of the engine is documented |
| [`_index/EVIDENCE-STANDARD.md`](_index/EVIDENCE-STANDARD.md) | What counts as proof, and what is banned |
| [`_index/GLOSSARY.md`](_index/GLOSSARY.md) | BKBI, BattleUnit, ActionDefinition, MapRef, EBP, VBF, Weather Slot, PSM… |
| [`_index/CALL-CHAINS.md`](_index/CALL-CHAINS.md) | Index of documented upstream→downstream chains |
| [`_index/ADDRESS-INDEX.md`](_index/ADDRESS-INDEX.md) | Address → document, generated |
| [`_index/OPEN-QUESTIONS.md`](_index/OPEN-QUESTIONS.md) | Everything not yet explainable. **Target: empty.** |
| [`_templates/SYSTEM.md`](_templates/SYSTEM.md) | The document template |

---

## Categories

Derived from the engine's own taxonomy: the 22 canonical V120 `PrimaryOwner` categories
(who owns a state/resource/lifecycle transaction) plus the V121 `CodeDomain` families
(what mechanism a function implements). Counts are functions carrying that classification.

### Game systems

| Folder | Engine category | Functions |
|---|---|---:|
| `00-Engine-Core-Runtime` | CoreRuntimeScheduling — main loop, frame, scheduling, singletons | 73 |
| `01-Script-VM-Native-Bridge` | ScriptVM natives, `.ebp` bytecode, authored call catalog | 1,900 |
| `02-Resource-And-Asset-Pipeline` | Resource load/bind/publish, async slots, VBF/EBP containers | 572 |
| `03-World-Area-Field` | Zones, field runtime, MapRef, **Weather**, environment | 108 |
| `04-Actor-Entity` | Actor identity, registry, ActorManager, entity lists | 235 |
| `05-Spawn-Encounter-Lifecycle` | Spawn controllers, members, respawn, eligibility | 52 |
| `06-Movement-And-Navigation` | Locomotion, pathing, navmesh, field-resource banks | 485 |
| `07-Combat-Action` | BattleUnit commands, action commit, phases, presentation slots | 134 |
| `08-Combat-Formula` | Damage/accuracy recipes, elements, weather & terrain scaling | 198 |
| `09-Combat-AI-And-Gambits` | Enemy AI, Gambit evaluation, target selection | 43 |
| `10-Status-Periodic-Terminal` | Status effects, augments, periodic ticks, KO/death | 24 |
| `11-Party` | Party composition, leader, focus, slots, guests | 79 |
| `12-Items-Equipment-Shops-License` | Inventory, equipment, augments, License Board, shops | 70 |
| `13-Rewards-Progression-Economy` | XP/LP/gil, drops, steals, poach, chains, bazaar | 38 |
| `14-Story-Event-Quest-Hunt` | Flags, quest stages, hunts, marks, event triggers | 15 |
| `15-Input` | Pad arbitration, DecideButton, modal state, capability policy | 1,047 |
| `16-UI` | Screens, request router, menus, HUD, lists | 544 |
| `17-Presentation-Rendering` | Rendering, effects, cameras, CharacterRender, **Legacy PS2 GS/VIF** | 1,564 |
| `18-Audio` | SQEX sound, ambient pools, streams | 2,064 |
| `19-Save-Load-Settings` | SaveImage persistent payload, settings serializer | 87 |
| `20-Platform-Online-Achievements` | Windows platform, graphics device, achievements | 59 |
| `21-RNG-And-Determinism` | Gameplay MT19937 vs shared procedural render PRNG | 18 |

### Engine substrate

| Folder | Engine category | Functions |
|---|---|---:|
| `22-Middleware-PhyreEngine` | Sony PhyreEngine — rendering, reflection, physics, ~2,350 RTTI classes | 6,768 |
| `23-Third-Party-Libraries` | Bullet, Lua, EASTL, WebM/MKV/Vorbis, zlib, math | ~1,000 |
| `24-Compiler-And-CRT-Runtime` | MSVC CRT, EH/unwind, thunks, CFG, generated C++ | ~5,150 |
| `99-Unresolved-Residual` | Functions with no classification yet. **Target: 0.** | **0** at the certified GN162 parent ~~30 (GN161)~~ — *see Status below; the figure is reached but the gate is not sealed* |

**Every count in these two tables except the `99-Unresolved-Residual` row is the 2026-09-08 figure and has not been re-derived since.** The certified ledger header does not break out per-folder totals, so they are left dated rather than estimated.

Category totals overlap by design — `PrimaryOwner` and `CodeDomain` are orthogonal layers
and a function may carry one of each. Cross-layer overlap in the ledger sense stays **0**.

---

## Status

| | |
|---|---|
| Engine classified (GFZ ledger) | **38,161 / 38,161 = 100.00000 %** — certified GN162 parent, `V121_COVERAGE internal=38161 owner=9409 finalNo=585 codeDomain=28167 overlap=0 explicit=38161 unresolved=0` *(was 38,131 = 99.92139 % at GN161 earlier on 2026-09-16, and 38,001 = 99.58072 % when this page was written, 2026-09-08)* |
| Engine *documented here* | see [`_index/COVERAGE.md`](_index/COVERAGE.md) |
| Unresolved functions | **0** at the certified **GN162** parent ~~30 (GN161)~~ *(160 on 2026-09-08)*. **The figure is reached and the residual gate is SEALED — 2026-09-16, and only because a third party reproduced it.** SWE2-EC7 applied all 30 validated rows, and **SWE2-AUDIT-SEM independently re-certified from its own fresh import**: snapshot `16a2a832…` byte-exact, `embedded_exe.bin` = the authorized `73461d08…21f8`, residual file empty, ledger `100.00000 %` reproduced, 30/30 applied domains exact. OPUS verified those artifacts directly rather than reading the checkpoint note. ~~Stage 4 has not landed~~ — **the figure was true for days before it was sealed, and the difference was never the number but who had reproduced it**: OPUS proposed the domains and EC7 applied them, so a seal signed by either would have been the author certifying the author. See [`_index/PROGRAM-STATE.md`](_index/PROGRAM-STATE.md) and [the residual list](99-Unresolved-Residual/residual-30-GN161.tsv) |
| Open questions | see [`_index/OPEN-QUESTIONS.md`](_index/OPEN-QUESTIONS.md) |

Classification is not documentation. A function tagged
`NativeRoutine.BoundedLoop.DirectCallOnly` is *accounted for* but not *understood* — roughly
11,800 functions carry generic shape classes like that. Reaching 100 % on the GFZ ledger is
the floor for this database, not the goal.

**The goal is that nothing in this engine is unexplained.**
