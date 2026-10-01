# XIIOnline — Master Multiplayer Roadmap
**General scope, grouping, and sequencing reference — 2026-08-28**

## Purpose

This is the high-level master roadmap for turning **Final Fantasy XII: The Zodiac Age** into a persistent multiplayer game through XIIOnline.

It is intentionally **not an implementation specification**. It records:

- everything that will or may need multiplayer work;
- which systems should be tackled together because their native/state infrastructure overlaps;
- a sensible order for tackling them;
- which later features may mostly fall out of earlier foundational work;
- FFXII-specific systems that must not be forgotten;
- broad current maturity so unfinished work is not confused with work starting from zero.

The architecture and exact order may change whenever stronger Ghidra, runtime, ff12-script/EBP/VBF, LiveLab, GFZ, or other native evidence reveals that several systems share a better seam.

---

# 1. End Goal

XIIOnline should ultimately provide a **persistent shared FFXII world** in which multiple players can:

- join and leave independently;
- reconnect without becoming a new logical player;
- occupy the same or different zones;
- see and interact with one another;
- see the same authoritative world population and state;
- fight the same enemies and observe coherent combat;
- share appropriate enemy lifecycle, NPC, treasure, quest, world, and progression state;
- enter an already-running session and reconstruct its current state;
- preserve native FFXII behavior wherever practical;
- remain compatible with other mods as far as reasonably possible;
- detect and repair disagreement instead of assuming synchronization can never fail.

The server should preserve authoritative shared-world truth while clients should continue using their own native FFXII engine to realize that truth wherever possible.

---

# 2. Recommended Major Programs and Order

1. **Persistent World Realization**
2. **Enemy Lifecycle + LOS / Full-Map Visibility**
3. **Combat and Consequences**
4. **Actor / AI / Navigation / Action Runtime**
5. **Player / Party Runtime Completion**
6. **Persistent World Interactions**
7. **World Script / NPC / Quest / Hunt / Environmental State**
8. **Rewards / Inventory / Economy / Character Progression**
9. **Zone / Session Persistence + True Drop-In/Drop-Out**
10. **Save / Recovery / Game-Over Semantics**
11. **Special FFXII Sequences**
12. **Multiplayer UI / Menus / Cutscenes / Time Model / Presentation**
13. **Whole-Game Integration, Compatibility, Reconciliation, and Certification**

These are overlapping workstreams, not hard walls. If a later system uses the same native seam or authority model as current work, pull it forward rather than duplicating research.

---

# 3. Program A — Persistent World Realization

## Main goal

Make clients agree about **what world entities logically exist** while letting FFXII's own engine realize them locally.

## Enemy population scope

- spawn-controller identity;
- controller members;
- authoritative member selection;
- generation/incarnation identity;
- missing enemy realization;
- wrong/contradictory sibling detection;
- correction of wrong realizations;
- native realization verification;
- ownership and authority;
- controller/member turnover;
- retirement/rematerialization;
- death-driven lifecycle state;
- multi-client population convergence;
- late realization when joining an existing zone;
- duplicate/impossible realization prevention.

## Current maturity

This is already one of XIIOnline's most advanced areas.

Existing progress includes:

- substantial canonical enemy identity/authority infrastructure;
- live-proven missing-enemy LiveAuthoritativeBirthReplay at canary scope;
- member/generation evidence;
- native realization through each client's own game engine;
- wrong/contradictory realization correction in active development;
- substantial enemy lifecycle/respawn research and partial live proof.

## Reuse potential

The same general identity/lifecycle/reconciliation model may later simplify:

- NPC existence;
- scripted world actors;
- guests/summons;
- treasure/interactable existence;
- late-join reconstruction;
- generic missing/matching/stale/contradictory classification.

**Important:** authoritative identity is not a species count. The multiplayer system should reason about controller/member/generation identity, not merely "three cactoids and one wolf."

---

# 4. Program B — Enemy Lifecycle + LOS / Full-Map Visibility

This should stay adjacent to Program A because both operate around spawn-controller lifecycle.

## Scope

- native realization/retirement radius behavior;
- full-map or extended-range enemy visibility;
- seeing distant friends fighting;
- spawn-controller cycling;
- retire/rematerialize transitions;
- death/respawn;
- native respawn eligibility/timers;
- composition changes caused by normal controller cycling;
- actor-budget/cap implications;
- safe hidden lifecycle turnover;
- rare/conditional enemy eligibility preservation;
- behavior when multiple connected players can observe the same controller region.

## Compatibility objective

Prefer preserving the **inner EBP/native spawn and respawn rules**.

Rare-enemy HP/weather/flag/chain/script conditions and other mods' EBP changes should continue to decide actual eligibility.

XIIOnline should preferably alter the higher-level **permission/range/lifecycle gate** controlling when native spawn-controller logic is allowed to cycle, rather than replacing spawn logic itself.

## What this may also solve

- enemy map-wide persistence;
- distant-combat visibility;
- native spawn compatibility;
- safe controller turnover;
- parts of late-join enemy reconstruction;
- shared observer handling.

---

# 5. Program C — Combat and Consequences

Once clients agree **which actors exist**, they need to agree **what happened to them**.

## Shared combat state may include

- HP/MP;
- damage;
- healing;
- criticals;
- misses/evades/blocks where applicable;
- elemental results;
- buffs/debuffs;
- status effects;
- periodic effects;
- KO;
- revive;
- lethal/defeat state;
- death attribution;
- authoritative enemy death;
- interruptions/cancels;
- nested effects;
- combat-triggered script consequences.

## Actor types

Build broadly enough for:

- players;
- party characters;
- enemies;
- bosses;
- guests;
- Espers/summons;
- NPC combatants where relevant.

## Existing maturity

Combat/HP work has prior experiments and partial infrastructure, but it is not yet at the certification level of enemy realization.

## Reuse potential

A strong authoritative action/result model could cover much of:

- enemy damage;
- player damage;
- healing;
- magic;
- items;
- statuses;
- lethal state;
- steals;
- poaches;
- reward triggers;
- normal boss combat.

---

# 6. Program D — Actor, AI, Navigation, and Action Runtime

Develop alongside Combat because AI, targeting, and combat actions overlap.

## Scope

- position;
- movement;
- navigation;
- facing;
- target;
- aggro;
- leash behavior;
- action selection;
- action phases;
- cast/charge state;
- animation;
- reactions;
- flee/return behavior;
- scripted AI actions;
- remote presentation of actions.

Enemy logical existence is currently further along than enemy movement synchronization. Final multiplayer needs both.

## Reuse potential

A common actor-state runtime may serve:

- remote players;
- enemies;
- NPCs;
- guests;
- summons;
- other moving world actors.

Avoid separate replication stacks for every actor category if native structures allow a common layer.

---

# 7. Program E — Player / Party Runtime Completion

Remote player puppets already have substantial working movement/visibility/animation infrastructure. This work finishes the gameplay model around them.

## Player runtime

- remote visibility;
- movement;
- position;
- facing;
- animations;
- actions;
- combat participation;
- loading/transition state;
- remote HP/status presentation.

## Party runtime

- persistent player identity;
- player-to-character assignment;
- active/reserve party members;
- party leader;
- persistent party-slot ownership;
- disconnect vacancy/reservation;
- reconnect reclaim of the same logical slot;
- no accidental fifth/new slot;
- party changes while connected;
- guest interactions;
- AI-controlled vs human-controlled party members;
- KO/revive participation.

---

# 8. Program F — Actions, Targeting, and Gambits

This should overlap with Actor/AI and Combat.

## Actions

- Attack;
- Magicks;
- Technicks;
- Items;
- targeting;
- action queues;
- cast/charge timing;
- interruption;
- cancellation;
- execution;
- result;
- animation/effect presentation.

## Gambits

Do not assume Gambits require a separate multiplayer engine.

If the authoritative character can still use FFXII's native Gambit evaluator and XIIOnline synchronizes the resulting target/action/consequence, much Gambit multiplayer behavior may be covered automatically.

This should be proven, not assumed.

## Shared action pipeline may serve

- human commands;
- Gambit commands;
- enemy AI actions;
- guest actions;
- scripted combat actions.

---

# 9. Program G — Persistent World Interactions

Build generic shared infrastructure for objects players can consume, activate, open, trigger, or change.

## Candidate systems

- treasure chests;
- dropped loot entities;
- doors;
- gates;
- switches;
- levers;
- traps;
- save/teleport crystals;
- environmental mechanisms;
- one-shot objects;
- NPC interactions;
- scripted interactables.

## Generic properties

- identity;
- available/used state;
- trigger actor;
- resulting world state;
- resulting reward;
- persistence;
- late-join representation.

## Useful separation

**Treasure/drop world existence** belongs here.

**Reward/inventory consequence** belongs in Program I.

This prevents treasure and drops from becoming bespoke networking stacks.

---

# 10. Program H — World Script / NPC / Quest / Hunt / Environmental State

Much of FFXII is driven by flags, counters, script state, and native eligibility. Research these together.

## Potential state

- flags;
- counters;
- script variables;
- quest stages;
- hunt acceptance/completion;
- marks;
- Trophy Rare Game;
- Clan/Centurio state;
- NPC availability;
- doors/gates unlocked by progression;
- weather;
- environmental transitions;
- boss/event stages;
- story-related zone changes;
- conditional spawn inputs.

## NPCs

NPC work overlaps Program D:

- existence;
- movement;
- script state;
- dialogue availability;
- interaction ownership;
- quest state;
- escort/combat state where applicable.

## Hunts and rare enemies

Prefer:

shared progression/state  
→ native eligibility logic  
→ native spawn controller  
→ shared enemy realization  
→ shared combat/death  
→ shared reward/progression.

If that holds, XIIOnline does not need a separate "multiplayer hunt engine" or "rare enemy spawning engine."

## Large reuse opportunity

A carefully classified shared world/script-state framework may cover much of:

- quests;
- hunts;
- Rare Game;
- NPC state;
- doors/switches;
- weather;
- boss stages;
- scripted environmental changes.

Do not blindly synchronize every global variable; classify semantic state and ownership.

---

# 11. Program I — Rewards / Inventory / Economy / Character Progression

Do this after Combat and World Interaction provide authoritative triggers.

## Rewards

- XP;
- LP;
- gil;
- loot;
- enemy drops;
- steals;
- poaches;
- chain state;
- rare drops;
- hunt rewards;
- quest rewards;
- boss rewards.

## Character/player progression

- inventory;
- equipment;
- weapons;
- armor;
- accessories;
- ammunition where relevant;
- licenses;
- abilities;
- stats;
- character-specific progression.

## Economy

- shops;
- buying/selling;
- Bazaar unlocks;
- Bazaar purchases;
- service NPCs;
- other economy progression.

## Policy question

Each category needs a deliberate multiplayer ownership model:

- server/session shared;
- individual player;
- character-specific;
- party-wide;
- hybrid.

Do this systematically rather than feature by feature.

---

# 12. Program J — Zone / Session Persistence + True Drop-In/Drop-Out

This is mostly an integration outcome of previous work, not one isolated feature.

## Requirements

- join an already-running server;
- leave independently;
- world continues;
- no requirement for simultaneous client startup;
- late join gets current world;
- authority handoff;
- stale-connection fencing;
- safe reconnect with a new connection instance;
- persistent player identity;
- persistent/reclaimable party slot;
- world authority survives changing participant sets.

## Multi-zone behavior

Eventually support:

- players in different zones;
- one player transitioning while another remains active;
- different loaded maps at once;
- logical zone persistence while unobserved;
- reconstruction when someone returns;
- zone-specific authority.

If every prior subsystem supports persistent IDs, generations, snapshots, late join, reconnect fencing, and authority handoff, final drop-in/drop-out should mostly become integration/certification.

---

# 13. Program K — Save / Load / Recovery / Game-Over Semantics

FFXII assumes a single local save, so multiplayer needs an explicit policy.

## Questions

- What belongs to server world persistence?
- What belongs to an individual player's save?
- What is party-wide?
- What happens when local save state disagrees with the live server?
- How is server/session state persisted?
- How is reconnect different from loading?
- What does whole-party defeat mean?
- Can one player reload while others continue?
- How do save/teleport crystals fit?
- How are rollback, duplication, stale resurrection, and reward duplication prevented?
- How does crash/restart recovery work?

Save/load UI/native research already exists, but full multiplayer save semantics remain a later integration area.

---

# 14. Program L — Special FFXII Sequences

Handle after generic actor/action/combat/world infrastructure is strong.

## Explicitly remember

- Quickenings / Mist chains;
- Espers;
- guest characters;
- scripted boss phases;
- cinematic combat;
- special battle transitions;
- temporary party/control changes;
- scripted invulnerability/phase rules;
- sequence-specific cameras/locks;
- encounters that suspend normal gameplay rules.

Most should reuse existing multiplayer foundations; only genuinely exceptional behavior should get bespoke handling.

---

# 15. Program M — Multiplayer UI / Menus / Cutscenes / Time Model / Presentation

Underlying state authority should come first, but final multiplayer needs coherent presentation and control behavior.

## Multiplayer UI

- player names/markers;
- player identity;
- remote HP/MP/status;
- party ownership/control;
- targeting feedback;
- interaction feedback;
- connection/session state;
- join/leave/reconnect feedback;
- multiplayer settings;
- useful sync/desync indicators.

## Menu/time semantics

FFXII's single-player assumptions need explicit multiplayer behavior:

- Active vs Wait;
- menus during another player's combat;
- pause behavior;
- equipment changes while others remain active;
- Gambit changes;
- inventory use;
- targeting menus;
- full-screen menus;
- map screens.

## Cutscenes/events

- trigger ownership;
- whether everyone sees them;
- players in different areas;
- skip behavior;
- control locking;
- resulting world flags;
- preventing duplicate event application.

## Presentation

- remote attack animations;
- spells/VFX;
- enemy actions;
- status effects;
- sounds;
- impacts;
- deaths;
- distant combat.

Existing UI/presentation research should be reused.

---

# 16. Cross-Cutting Foundation — Reconciliation / Self-Healing

This should become a reusable pattern for every synchronized system.

For any state:

1. identify canonical truth;
2. observe local/native truth;
3. classify matching / missing / stale / contradictory / unknown;
4. choose the highest-level native-coherent correction;
5. change only what is necessary;
6. verify native readback;
7. preserve evidence;
8. leave unrelated state untouched.

Enemy realization is the first major prototype for this pattern.

Later it may apply to:

- NPCs;
- world actors;
- treasure/interactables;
- quest/world state;
- party state;
- combat state;
- other divergent native state.

---

# 17. Cross-Cutting Foundation — Networking / Authority / Identity / Security

Relevant throughout the project:

- dedicated server authority;
- connection-instance identity;
- persistent player identity;
- stale packet fencing;
- ownership terms/epochs;
- authority handoff;
- reconnect;
- late join;
- ordering/reliability;
- idempotency;
- generation/version fencing;
- protocol/version compatibility;
- malformed/impossible state rejection;
- trust boundaries;
- inventory/progression security;
- anti-cheat concerns;
- latency handling;
- prediction/interpolation where appropriate;
- distribution/session connectivity needs.

Do not rebuild these separately for every feature.

---

# 18. Cross-Cutting Foundation — RNG / Determinism

Potential RNG-sensitive areas:

- spawn-member selection;
- enemy level/base variation;
- combat RNG;
- drops;
- steals;
- treasure;
- AI choices;
- rare eligibility;
- weather;
- script outcomes.

Not every RNG stream needs lockstep.

Per system, determine whether the correct model is:

- synchronize authoritative outcomes;
- synchronize RNG/seed state;
- deterministic replay;
- or allow native realization after a server-authoritative decision.

---

# 19. Cross-Cutting Foundation — Mod Compatibility

Consider compatibility during every workstream.

General preference:

**preserve native/modded inner decision logic and alter only the multiplayer-relevant authority/permission boundary when possible.**

Enemy spawning is the model:

- keep EBP spawn/respawn/rare eligibility logic;
- alter the outer lifecycle/range permission needed for multiplayer behavior.

Carry this philosophy into:

- spawn mods;
- AI mods;
- combat/difficulty mods;
- loot/progression mods;
- equipment/license mods;
- UI mods;
- script/event mods.

---

# 20. Cross-Cutting Foundation — Native Fidelity / Reverse Engineering

Every workstream may discover a better native seam.

Relevant evidence sources include:

- Ghidra;
- GFZ;
- ff12-script;
- EBP/VBF/script analysis;
- LiveLab;
- runtime telemetry;
- native tests;
- existing XIIOnline evidence;
- external modding research.

Prefer high-level native calls/state transitions when they give better downstream native coherence than direct writes or duplicated engine logic.

This roadmap does not freeze implementation seams.

---

# 21. Cross-Cutting Foundation — Logging / Evidence / Testing / Certification

Every system should have enough evidence to prove multiplayer correctness.

Include as appropriate:

- focused telemetry;
- event-proportional rather than frame-spam logging;
- deterministic reducers;
- unit/static tests;
- runtime tests;
- mutation/adversarial tests;
- real linked multiplayer testing;
- 2/3/4-client tests;
- failure paths;
- late join;
- reconnect;
- authority handoff;
- disagreement/correction;
- exact binary/protocol identity;
- provenance/hashes;
- clean deployment state.

Short certification runs should not naturally generate multi-gigabyte logs, but deep diagnostic modes should remain available.

---

# 22. Features Likely to Be Mostly Covered by Other Work

## Gambits
Potentially mostly covered by character authority + native Gambit evaluation + action/target synchronization + combat consequences.

## Hunts
Potentially mostly covered by world/quest state + native eligibility + enemy realization + combat/death + rewards.

## Rare enemies
Potentially mostly covered by native eligibility preservation + world conditions + persistent spawn-controller realization.

## Moving NPCs
May reuse actor movement/state + world-script state + generic entity realization.

## Guests
May reuse player/party actor infrastructure + AI/action runtime + combat + world progression.

## Bosses
Normal portions may reuse entity lifecycle + AI/action + combat + world-script state. Only exceptional phases/sequences may need bespoke work.

## Treasure
Split into interactable state + reward/inventory result.

## Drops
Split into world-entity realization + pickup/reward result.

## Drop-in/drop-out
Should emerge from persistent identity + snapshots/rehydration + authority handoff + reconnect fencing across every subsystem.

## Multiplayer UI
Much of it can become a consumer of authoritative state once that state already exists.

---

# 23. Broad Current Maturity Snapshot

| Area | Broad state |
|---|---|
| Remote player visibility/movement/animations | Substantial working foundation |
| Enemy canonical identity/authority | Advanced |
| Missing enemy realization | Live-proven at canary scope |
| Wrong/contradictory enemy correction | Active development |
| Enemy generation/lifecycle | Advanced; still being hardened |
| Native enemy respawn | Partially researched/live-proven; full integration remains |
| LOS/full-map enemy visibility | Designed direction / upcoming implementation |
| Enemy HP/combat | Partial |
| Player combat state | Partial |
| Enemy movement/AI sync | Major future completion area |
| Persistent player/party identity | Strong design + partial infrastructure |
| Drop-in/drop-out | Strong requirements/architecture; incomplete integration |
| Treasure/interactables | Mostly future |
| NPC/world actors | Mostly future |
| Quest/world progression | Mostly future |
| Rewards/inventory/economy | Future/partial depending on subsystem |
| Save/recovery semantics | Future integration |
| UI/presentation | Partial research/infrastructure; broad completion later |
| Special FFXII sequences | Mostly later integration/certification |

Update this only when milestones actually change; distinguish implementation, static proof, and live proof.

---

# 24. Practical Sequence From the Current Frontier

## Phase 1 — Finish shared enemy existence
Missing + contradictory realizations, member/generation correctness, multi-client convergence, lifecycle safety.

**Outcome:** every client agrees which enemies logically exist.

## Phase 2 — Finish enemy lifecycle + LOS
Full/extended visibility, native controller cycling, death/respawn integration, multiple-observer safety, conditional eligibility preservation.

**Outcome:** enemies remain visible as intended while native lifecycle remains correct.

## Phase 3 — Shared combat consequences
Damage, HP, statuses, death, revive, core results.

**Outcome:** every client agrees what happened to combatants.

## Phase 4 — Actor / AI / Action convergence
Movement, targets, actions, animations, AI state, queues, Gambits.

**Outcome:** clients agree what actors are doing.

## Phase 5 — Player / Party gameplay completion
Player combat, character control, party slots, KO/revive, guests/AI ownership, reconnect identity.

**Outcome:** remote players are full gameplay participants, not merely puppets.

## Phase 6 — Shared world interactions
Treasure, drops, doors, switches, traps, crystals, mechanisms.

**Outcome:** players interact with one shared physical world.

## Phase 7 — World scripts / NPCs / quests / hunts / environment
Shared script/world state and systems built on it.

**Outcome:** players share one evolving scripted world.

## Phase 8 — Rewards and progression
XP/LP, loot/gil, chain state, inventory, equipment, licenses, shops/Bazaar, reward policy.

**Outcome:** multiplayer gameplay produces coherent persistent progression.

## Phase 9 — True session persistence / multi-zone
Late join, reconnect, authority handoff, different zones, empty-zone persistence.

**Outcome:** the world exists independently of any one client.

## Phase 10 — Save / recovery model
Server persistence, player saves, reload, game over, crash recovery, rollback safety.

**Outcome:** multiplayer progress survives real-world interruption safely.

## Phase 11 — Special FFXII systems
Quickenings/Mist, Espers, guests, exceptional bosses, scripted/cinematic battle behavior.

**Outcome:** exceptional FFXII systems work correctly in multiplayer.

## Phase 12 — UI / menus / cutscenes / presentation / time model
Multiplayer UI, Active/Wait, pause/menu semantics, cutscenes, VFX/audio, session UX.

**Outcome:** multiplayer is usable and understandable, not merely synchronized underneath.

## Phase 13 — Whole-game hardening
Full-playthrough testing, 2/3/4 clients, drop-in/out, reconnect, multi-zone, bad networks, mod compatibility, save/recovery, stress, long sessions, desync injection/reconciliation, performance/regression.

**Outcome:** XIIOnline is resilient enough to play FFXII as multiplayer.

---

# 25. Permanent Scope Checklist

These categories should never disappear from the project roadmap even if deferred:

- persistent server/world authority;
- changing participant sets;
- exact player identity;
- persistent party slots;
- stale-connection fencing;
- late join/reconnect;
- multi-zone play;
- empty-zone persistence;
- spawn-controller identity;
- enemy generation/incarnation;
- missing/wrong realization correction;
- enemy lifecycle/respawn;
- LOS/full-map realization;
- enemy AI/movement;
- combat/results;
- actions/targeting;
- Gambits;
- player/party combat;
- treasure/interactables;
- NPCs;
- world flags/scripts;
- quests;
- hunts;
- Rare Game;
- weather/environment;
- loot/rewards;
- chain state;
- XP/LP/gil;
- inventory;
- equipment;
- licenses;
- shops/Bazaar;
- bosses;
- Quickenings/Mist;
- Espers;
- guests;
- cutscenes;
- menus;
- Active/Wait/pause semantics;
- save/load;
- game over;
- crash/recovery;
- UI/presentation;
- audio/VFX;
- RNG/determinism decisions;
- mod compatibility;
- reconciliation/self-healing;
- logging/evidence;
- real multiplayer certification.

---

# 26. How to Use This Document

This is a **scope and sequencing reference**, not a requirement that every heading become its own implementation project.

As XIIOnline develops:

- combine work whenever systems share native structures or authority models;
- reuse earlier foundations aggressively;
- do not duplicate FFXII logic unnecessarily;
- prefer native outcomes and state transitions;
- allow later features to become consumers of already-authoritative state;
- update groupings when reverse engineering proves a better structure;
- distinguish **implemented**, **partially implemented**, **statically proven**, and **live proven**;
- never treat one canary as proof of adjacent lifecycle cases;
- judge success by whole-game multiplayer behavior.

The overall progression is:

**shared existence**  
→ **shared behavior**  
→ **shared consequences**  
→ **shared progression**  
→ **shared persistence**  
→ **shared presentation / whole-game integration**.

That is the general path from the current persistent-world work to a complete XIIOnline multiplayer conversion.
