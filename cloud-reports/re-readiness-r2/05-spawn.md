# Reconstruction readiness, pass 2 — `FFXII TZA/05-Spawn-Encounter-Lifecycle/` (slug `05-spawn`)

| | |
|---|---|
| Stream | R2 (reconstruction readiness, pass 2), per [`docs/cloud-briefs/re-readiness-r2.md`](../../docs/cloud-briefs/re-readiness-r2.md), part A |
| Pass 1 | [`cloud-reports/re-readiness/05-spawn.md`](../re-readiness/05-spawn.md), snapshot `4da4b9d0`, 2026-10-02 |
| This pass | snapshot `b23bdddd` (synced from XIIOnline `f9d9053b9`), 2026-10-03 |
| Working for | FABLE |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every verdict quotes or cites a page line; no executable, Ghidra or live game was used. |

## Citation form

`ABBR:line` is a line of the page **in this snapshot** (line numbers moved since pass 1; every cite below was re-taken).
Paths are relative to `FFXII TZA/05-Spawn-Encounter-Lifecycle/` unless they start with `../`.

| abbr | page |
|---|---|
| README | `README.md` |
| SPR | `spawn-placement-and-retirement.md` |
| HT | `spawn-placement-height-and-authored-tunables.md` |
| WHY | `why-the-enemies-you-killed-come-back.md` |
| C-SP | `CONTRACT-spawn-placement.md` |
| C-GC | `CONTRACT-group-completion-and-respawn.md` |
| GC | `Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md` |
| FM | `Spawn-Record/the-spawn-keep-entry-field-map.md` |
| OQ | `../_index/OPEN-QUESTIONS.md` (the register) |
| TICK | `../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md` |
| S16 | `../25-EBP-Script-Container/Sections/section-016.md` |
| RNG | `../21-RNG-And-Determinism/rng-streams.md` |
| ENM | `../09-Combat-AI-And-Gambits/CONTRACT-enmity.md` |
| UDEF | `../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md` |
| BUFM | `../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md` |
| KIND | `../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md` |
| HEAD | `../06-Movement-And-Navigation/heading-speed-to-position-delta.md` |
| SET | `../19-Save-Load-Settings/Game-Settings-Config/the-settings-command-table.md` |
| BSB | `../11-Party/Battle-State-Block/the-battle-state-block-field-map.md` |
| CONV | `../01-Script-VM-Native-Bridge/Spawn-Verbs/the-script-to-native-calling-convention.md` |

**What changed since pass 1.** `git diff 4da4b9d0 HEAD` over the folder is +471 / −102 lines in all eight pages, almost all of
it OPUS's dated corrections of 2026-10-02 (which settle most of pass 1's §2.3 contradictions) and two new contract sections of
2026-10-03: C-SP §7a "Range retirement, the return window and the keep-bank rotation" (`C-SP:146-417`) and C-GC §10a "The
cooldown clock across a runtime reset and a load" (`C-GC:419-509`). No register row owned by this folder changed state.

**How verdicts were chosen.**
- Pass 1 scoped "not stated" to the eight pages of this folder. Where the answer was already on another page **before** pass 1
  (checked with `git show 4da4b9d0:<page>`), the item is **WRONG-IN-PASS-1** if that page answers it whole, and **NARROWED**
  if it answers part; either way the folder still lacks the pointer, which the row says.
- A "field written but left unexplained" whose page already states it is never read is **WRONG-IN-PASS-1**: a port needs the
  write, not a purpose.

## 1. Summary

| pass-1 group | items | CLOSED | NARROWED | OPEN | WRONG-IN-PASS-1 |
|---|---:|---:|---:|---:|---:|
| §2.1 open items the pages list | 14 | 0 | 3 | 11 | 0 |
| §2.2 structural gaps G1–G16 | 16 | 1 | 7 | 4 | 4 |
| §2.2 fields written but unexplained (F1–F9) | 9 | 0 | 1 | 1 | 7 |
| §2.3 A, value-changing contradictions | 18 | 17 | 1 | 0 | 0 |
| §2.3 B, counts and sizes | 5 | 3 | 0 | 2 | 0 |
| §2.3 C, stale claims, banners, names | 25 | 19 | 0 | 4 | 2 |
| **total** | **87** | **40** | **12** | **22** | **13** |

**New gaps (§3): 12** — DOC 7, STATIC 3, DATA 1, RUNTIME 1.

**Open and narrowed items by class** (the 34 OPEN or NARROWED pass-1 items, by what is still missing): RUNTIME 6
(§2.1 items 1–5, and 8's live half is not claimed), STATIC 17, DATA 3, DOC 8. Each row in §2 gives its class.

**Rating: NOT YET → NOT YET**, but narrower. Pass 1 rated two parts MOSTLY (the group ledger; the keep entry and bank rotation)
and placement-and-retirement NOT YET. Now **retirement** has a contract section with offsets, writers, both senses and executed
cases (C-SP §7a), and the clock's advance is stated, so three of four parts are MOSTLY. **Placement** alone keeps the system
at NOT YET: the region containment test `002374E0`, the selector's lane-and-candidate loop and the two undescribed selectors
(G2, G3, G5). See §4.
