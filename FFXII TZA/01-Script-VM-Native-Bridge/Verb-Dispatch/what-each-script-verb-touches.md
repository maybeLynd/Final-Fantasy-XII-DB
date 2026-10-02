---
system: What each script verb touches — the verb-to-subsystem reach map
category: 01-Script-VM-Native-Bridge
status: DOCUMENTED — every register row is closed (owner re-status 2026-09-30, OPUS) — the handler bodies are not read (UQ-57, SUPERSEDED as a duplicate of CY-3, itself SUPERSEDED under the class-1 ruling: this census's declared scope) and depth-2 hops through low-in-degree callees are untrusted (UQ-56, SUPERSEDED as a duplicate of CY-2, NOT A QUESTION under the class-2 ruling); the drift answered 2026-09-30 (RC-21: the rows move with the generator's hash-order tie-break, not with the snapshot; the table is one draw) (status line current 2026-09-30, SWE2-CONTRACT)
note_kind: census
parent: scriptvm-verb-dispatch-and-parameter-encoding.md
owner_layer: PrimaryOwner:Script_VM_Native_Bridge
evidence_tier: 3
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 8 cited function entries, 0 of them among the 109 records that changed GN160 -> GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0), established for this document 2026-09-14 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  project: work/headless_gn160/GFZ_GN160, CHECKPOINT VERIFIED 2026-09-07
last_reviewed: 2026-09-30
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-verb-reach-pass-1 - the method reproduces exactly (1,960 rows and 616 / 851 / 944 labelled at depths 1, 2 and 3) from an independent implementation; the table's unstated counting rule is recovered as one-verb-one-subsystem by most callees, under which the column totals exactly 616 and nine of the fourteen rows reproduce; six subsystems totalling the missing 11 verbs are omitted from the table; Save_Load_Settings does NOT appear from nothing at depth 2; and the five drifting rows drift with a control - the owner-tag claim reads 1,890 of 1,922 now against 1,857 of 1,888 then, so the map is stale against the older GN160 snapshot it names
  last_pass_kind: falsification
  crossref_clean: false
  reopened_count: 0
---

# What each script verb touches

## Scope (SWE2-CONTRACT, 2026-09-30)

A census companion to [the verb dispatch and parameter encoding page](scriptvm-verb-dispatch-and-parameter-encoding.md),
the parent that owns the verb → handler table. This note establishes, for all 1,960 verb ids, **which owning subsystems
each verb's handlers call into** at depths 1–3 of the pack-time call graph, with bridge plumbing discarded. It assigns
ownership to nothing and does not read handler bodies; what a verb *does* is left to its handler and to the parent.

## Findings (SWE2-CONTRACT, 2026-09-30)

- 616 verbs reach a named subsystem at depth 1, 851 at depth 2 and 944 at depth 3; 1,344 rows are blank at depth 1
  (§2; reproduced exactly by an independent implementation, falsification pass 1).
- The blank rows split four ways (CY-1): 1,029 handlers call only bridge plumbing, 218 call nothing, 93 have untagged
  callees, 4 have no handler.
- Handler owner tags are uninformative: all but about 31 of the rows that carry one read `Script_VM_Native_Bridge`
  (§2; 1,857 of 1,888 at the page's snapshot, 1,890 of 1,922 at the current one).
- Filtering callees by in-degree lifts agreement with the control from 65 % to 71 % (§2).
- `shape` means "has a `begin`", so 77 verbs labelled durative finish in one call (CY-4).
- The depth-1 table is reproducible in method and stale in detail: five of its fourteen rows drift at the current *(answered: RC-21, 2026-09-30 — the rows do not drift with the snapshot; the generator breaks ties in hash-seed order; 2026-10-02, OPUS)*
  snapshot (§8) — RC-21.

> A zone script calls verbs by name — `setpos`, `bgmstreamplay`, `movesync`. **This is the map from
> those names to the part of the engine each one actually drives**, built from the call graph rather
> than from the name.
>
> **It covers 616 of the 1,960 verbs, and it is a lead, not a verdict.** ~~`status: PARTIAL` is the~~ *(corrected 2026-10-02, OPUS: the front matter says `status: DOCUMENTED`, every register row closed 2026-09-30)*
> ~~honest state.~~

## 1. What the player sees

Nothing — this is a map for people writing or reading zone scripts.

FFXII's cutscenes and field events are authored as scripts made of about two thousand verbs. **The
names tell you a lot and mislead you sometimes.** `musicfadeout` sounds like a screen effect and is
audio; `getpos` sounds like movement and only reads the actor; `fadein` looks self-explanatory and
reaches into resource loading.

For anyone editing a script, the useful question is not what a verb is called but **which engine
system it will disturb** — because that is what decides whether a change is safe, and what else might
move when it runs.

## 2. Native mechanism

### What this map is, and what it is emphatically not

**This is a statement about call-graph edges. It assigns ownership to nothing.**

This database's standing rule is that **ownership is never inferred from a caller**. Nothing here
does that: every handler in this table is already owned by the Script/VM bridge, and that fact is
what makes the handler's own owner tag useless — **1,857 of the 1,888 rows carrying one just say
`Script_VM_Native_Bridge`**. What is reported instead is *which owning subsystems a verb's handlers
call into*, which is a property of the edges, not a claim about who owns anything.

### Method

For every row of [`scriptvm-verb-table.tsv`](scriptvm-verb-table.tsv), the `begin`, `poll` and
`result` handler addresses are taken as seeds; their direct callees are looked up in the pack-time
call graph; and each callee's owner tag is read from `functions.tsv`. Bridge-owned callees are
discarded — they are the plumbing every verb uses. **The rest is the verb's reach.**

### The map, at depth 1

**616 of 1,960 verbs reach a named non-bridge subsystem through a direct call.**

| subsystem | verbs |
|---|---:|
| Movement | 182 |
| ActorEntity | 142 |
| Party | 51 |
| Presentation | 42 |
| Audio | 36 |
| Input | 35 |
| Spawn_Encounter_Lifecycle | 31 |
| WorldAreaField | 29 |
| Story_Event_Quest_Hunt | 21 |
| CoreRuntimeScheduling | 11 |
| UI | 8 |
| CombatFormula | 7 |
| Resource | 6 |
| Rewards_Progression_Economy | 4 |
| *(six more, 11 verbs, omitted — §8)* | |

> **Movement and ActorEntity together are 324 of 616 — more than half.** A zone script is
> overwhelmingly a machine for putting bodies in places and asking them questions.

### Depth is not free

| depth | verbs labelled | what appears |
|---:|---:|---|
| 1 | 616 | — |
| 2 | 851 | `Save_Load_Settings` rises to **28** — ~~from nothing~~ **from 1 at depth 1**, §8 |
| 3 | 944 | `Save_Load_Settings` **61**, `CoreRuntimeScheduling` 11 → 40 |

> **A subsystem that appears only at depth 2 or 3 is the signature of a shared helper, not of a verb
> that touches it.** No script verb "does save/load"; the transitive closure simply reaches the
> settings code through common utilities. **Depth 1 is the instrument; deeper hops measure the
> engine's connectedness instead.** The map published here is depth 1 only.

### Discounting the helpers everything calls

A callee with hundreds of callers says nothing about any one of them. Capping the callee's in-degree:

| filter | verbs labelled | control agreement |
|---|---:|---:|
| none | 616 | 65 % |
| in-degree ≤ 50 | 566 | 70 % |
| **in-degree ≤ 20** | **458** | **71 %** |
| in-degree ≤ 10 | 425 | 72 % |
| in-degree ≤ 5 | 350 | 69 % |

**The gain is real but modest — 65 % to 71 % — which is itself the finding: the shared-helper problem
exists and does not dominate.** The deliverable table carries both the unfiltered and the
in-degree ≤ 20 reach, so a reader can see when a label depends on the filter.

### The control, and why it is not a scoreboard

Verb names that unambiguously imply a subsystem (`move`, `walk`, `turn`, `pos`, `bgm`, `voice`,
`sound`, `camera`, `fade`, `party`, `member`) were scored against the depth-1 reach:

**118 agree · 53 disagree · 242 name a subsystem but reach nothing.**

**Reading the 53 disagreements is more useful than the ratio, because most of them favour the graph:**

| verb | name suggests | reach says | which is right |
|---|---|---|---|
| `musicfadeout_231` | Presentation *(my `fade` keyword)* | **Audio** | the reach |
| `getpos_12a` | Movement | **ActorEntity** | the reach — a getter reads an actor, it does not move one |
| `ucsetpos` | Movement | **ActorEntity** | the reach |
| `getmapjumpposbyindex` | Movement | **WorldAreaField** | the reach — it queries the map |
| `fadein` | Presentation | **Resource** | **the name** — see below |

> **So the control mostly measures how crude a keyword is.** That is worth saying plainly rather than
> quoting 69 % as an accuracy figure: **the instrument and the control disagree most often where the
> control is wrong.**

### ⚠ Where the map is wrong, with a worked case

**`fadein` (`0x00B8`, result handler `00355EB0`) is labelled `Resource`.** Its callees are
`00183070`, `001D6C20`, the two value-stack helpers, and `002EFA70`. The label comes entirely from
**`001D6C20` — a 21-byte function tagged `FFXII.ResourceDataLoading`.**

**A 21-byte callee is an accessor, not a subsystem.** The fade is not a resource operation; the
handler happens to ask a resource-side accessor one question.

> **This is the failure mode of the whole map in one row: a small shared helper drags a verb into its
> owner's column.** The in-degree filter catches the worst of it and does not catch this one.
> **Treat a single-hit label as a lead to check, never as an answer** — the deliverable table prints
> the hit counts so a `Resource:1` can be told from a `Movement:3`.

### What is not covered

**1,344 of 1,960 verbs reach nothing nameable at depth 1**, and **`CY-1` has since split that silence
four ways** — see the refinement in
[`scriptvm-verb-dispatch-and-parameter-encoding.md`](scriptvm-verb-dispatch-and-parameter-encoding.md):

| cause | verbs |
|---|---:|
| **every tagged callee is bridge-owned** | **1,029** |
| handler calls nothing — the body is inline | 218 |
| every callee is untagged | 93 |
| no handler at all | 4 |

> **The dominant cause is not a tagging gap.** 1,029 handlers call only the value stack, the scratch
> block and the coercion helpers, and do their real work in their own instructions. **Only 93 verbs
> would be recovered by a naming pass; for the 1,029 the map cannot be extended by any amount of graph
> work, and reading the handler is the only route.**

*Re-counted at GN161, 2026-09-14 (FABLE). This settles the census review in `FRONTIER-REQ-FABLE-PROVENANCE-TRANSFER-GN161`.*
- **The split holds at GN161.** `check_verb_shape_slots.py` on the repacked GN161 graph gives the same five figures:
  - 616 labelled;
  - 1,029 bridge-owned;
  - 218 inline;
  - 93 untagged;
  - 4 with no handler.
- **The 93 are the same verbs as on the 2 September graph**, with the same 126 callees.
- **"Untagged" here means no owner tag.** The rule reads only `PrimaryOwner` and `FFXII.` tags. All 126 callees already carried a `CodeDomain` tag on the 2 September graph, and none of their tag sets changed between that graph and GN161.
- **R109's 109 new tags therefore cannot move this figure.**

**The map's silence is not evidence that a verb touches nothing.**

## 3. Key addresses

| address | what |
|---|---|
| `002621D0` | `VMNativeCommand_ExecuteLifecycle` — the dispatcher whose three slots seed every row |
| `003DC270` / `003DC240` / `003DC2A0` | the begin / poll / result callback accessors |
| `00355EB0` | `fadein`'s result handler — the worked mislabel above |
| `001D6C20` | the 21-byte `ResourceDataLoading` accessor that mislabels it |

## 4. Modding notes

- **[`scriptvm-verb-reach.tsv`](scriptvm-verb-reach.tsv) is the deliverable** — 1,960 rows of
  `call_id, verb, shape, reach_all, reach_filtered, top`, with hit counts.
- **Read the count, not just the name.** `Movement:3` is a verb that calls into movement three
  different ways; `Resource:1` is one edge and may be an accessor.
- **A blank row means the map could not see anything, not that the verb is inert.** 1,344 rows are
  blank.
- **Use it to find the neighbours of a change.** If you are editing what `setpos` does, the verbs
  whose reach is also `Movement` are the ones that may share the code you are about to touch.
- **Do not use it to decide what a verb is for.** For that, read the handler — the table gives you
  its address.

## 5. What is not known

- [x] ~~What the 1,344 unlabelled verbs touch, and the split between thin handlers and untagged
  callees.~~ **`CY-1` ANSWERED 2026-09-08 — split four ways, and the dominant cause is not a tagging
  gap:** 1,029 handlers call **only bridge plumbing**, 218 call nothing at all (inline bodies), **93**
  have untagged callees, 4 have no handler. **Only the 93 would be fixed by a naming pass; for the
  1,029, reading the handler is the only route.** See the refinement in
  [`scriptvm-verb-dispatch-and-parameter-encoding.md`](scriptvm-verb-dispatch-and-parameter-encoding.md).
- [x] **UQ-56.** **Whether a depth-2 hop through a *low* in-degree callee is trustworthy**, which would extend *(closed — the register row is WITHDRAWN.)* *(Register wording since: SUPERSEDED as a duplicate; pointer 2026-09-30, SWE2-CONTRACT.)*
  the map without importing the shared-helper noise that plain depth 2 does. `CY-2`.
- [x] **UQ-57.** The handler bodies themselves. **Not one is read here** — this document is built entirely from *(closed — the register row is WITHDRAWN.)* *(Register wording since: SUPERSEDED as a duplicate; pointer 2026-09-30, SWE2-CONTRACT.)*
  the call graph and owner tags, which is why its tier is 3 ~~and its status `PARTIAL`~~ *(corrected 2026-10-02, OPUS: the front matter says `status: DOCUMENTED`)*. `CY-3`.
- [x] ~~Whether any verb's reach contradicts the arity or shape already recorded in
  `scriptvm-verb-table.tsv`.~~ **`CY-4` ANSWERED 2026-09-08 — no contradiction, and the join found
  something better:** `shape` means *"has a `begin`"*, so **77 verbs labelled `durative` have no
  `poll` and finish in one call**. That is why `rmove` needs `movesync`. Two verbs labelled
  `instantaneous` carry a `poll` and can block (`CZ-1`).

## 6. Evidence

| claim | evidence | tier |
|---|---|---|
| Handler owner tags are uninformative | 1,857 of 1,888 rows read `Script_VM_Native_Bridge` | 1 |
| 616 verbs reach a named subsystem at depth 1 | census over the pack-time call graph and owner tags | 3 |
| The depth-1 distribution | same census | 3 |
| `Save_Load_Settings` appears ~~only at depth ≥ 2~~ at depth 1 once and rises from depth 2 *(corrected 2026-10-02, OPUS: §2's corrected depth table: from 1 at depth 1)* | the three-depth comparison | 3 |
| In-degree filtering lifts agreement 65 % → 71 % | the control re-run at five caps | 3 |
| `fadein` is mislabelled via a 21-byte accessor | its callee list, and `001D6C20`'s size and tag | 1 |
| **Any individual row** | **a lead from the call graph — no handler body was read** | 3 |

*Evidence rows added 2026-09-30 (SWE2-CONTRACT):*

| claim | evidence | tier |
|---|---|---|
| The method reproduces exactly (1,960 rows; 616 / 851 / 944 at depths 1–3) | falsification pass 1's independent implementation | 3 |
| Five of fourteen depth-1 rows drift at the current snapshot *(answered: RC-21 — they do not; a hash-seed draw of the same census; 2026-10-02, OPUS)* | falsification pass 1, the owner-tag control drifting the same way | 3 |
| `fadein` reaches resource loading (§1's example) | its row in [`scriptvm-verb-reach.tsv`](scriptvm-verb-reach.tsv) (`Resource:1`); through the 21-byte `001D6C20` (§2's worked case) | 1 |
| §1's other two examples, `musicfadeout` (audio) and `getpos` (reads only the actor) | **not anchored by this census:** both rows are blank at depth 1 in the TSV (checked 2026-09-30; `getpos_12a` reaches `ActorEntity:1`). They rest on the handler names and are not re-derived here | 3 (names only) |

## 7. Related

- [`scriptvm-verb-dispatch-and-parameter-encoding.md`](scriptvm-verb-dispatch-and-parameter-encoding.md)
  — the id → handler table this map is keyed on, and the arity work.
- [`../Native-Command-Lifecycle/native-command-lifecycle.md`](../Native-Command-Lifecycle/native-command-lifecycle.md)
  — the begin/poll/result dispatcher that supplies the three seed addresses.
- [`../verbs-that-only-wait-and-verbs-that-do-nothing.md`](../verbs-that-only-wait-and-verbs-that-do-nothing.md)
  — the verbs with no handlers at all, which are necessarily blank here.
- [`../Interpreter-Core/worldactor-scriptvm-interpreter.md`](../Interpreter-Core/worldactor-scriptvm-interpreter.md)
  — the interpreter that reaches the dispatcher.

## 8. Falsification pass 1 — 2026-09-13 (OPUS)

*(Static only — the method re-implemented from §2's own description against the current
`functions.tsv` and `edges.tsv`. Nothing executed.)*

### ✔ The method reproduces exactly

Seeds taken from `begin` / `poll` / `result`, direct callees from the pack-time call graph, owner
tags from `functions.tsv`, bridge-owned callees discarded — nothing else:

| | page | measured |
|---|---:|---:|
| verb rows | 1,960 | **1,960** |
| labelled at depth 1 | **616** | **616** |
| labelled at depth 2 | **851** | **851** |
| labelled at depth 3 | **944** | **944** |

**All three depth totals, to the number**, from an independent implementation. Whatever else moves,
the method is reproducible.

### ✔ The table's counting rule, recovered

§2 never says how a verb reaching two subsystems is counted, and the rule matters: counted under
*every* subsystem it reaches, the fourteen rows would total **687**; the published rows total
**605**. Neither is 616.

The rule is **one verb, one subsystem — the one its handlers call into most**. Under that rule the
column totals **exactly 616**, and **nine of the fourteen rows reproduce exactly**: Presentation 42,
Audio 36, Input 35, Spawn 31, Story 21, CoreRuntimeScheduling 11, UI 8, CombatFormula 7,
Rewards 4 — and **Movement 182**, the largest row of all.

**The table is therefore a partition of the 616, with rows left out.** Six subsystems are reached at
depth 1 and absent from it, and they account for exactly the missing **11**: 616 − 605.

| omitted subsystem | verbs (partition) |
|---|---:|
| `CombatAction` | 3 |
| `RNG_Random_Selection` | 2 |
| `CombatAI` | 2 |
| `Items_Equipment_Shops_License` | 2 |
| `Save_Load_Settings` | 1 |
| `PlatformOnlineAchievements` | 1 |

### ✖ Corrected: `Save_Load_Settings` does not appear "from nothing"

§*Depth is not free* reads *"`Save_Load_Settings` appears from nothing at 28"* at depth 2, and the
paragraph after it turns that into an argument: *"a subsystem that appears only at depth 2 or 3 is
the signature of a shared helper."* **It is reached at depth 1** — by one verb under the partition,
two under any-subsystem counting. The rise from 1 to 28 to 61 still says what the paragraph wants it
to say; "from nothing" does not.

### ○ Five rows drift, and the drift has a control

Five of the fourteen do not reproduce under the recovered rule: ActorEntity **162** against 142,
Party **37** against 51, WorldAreaField **26** against 29, Resource **4** against 6, Rewards
**3** against 4. The page does not state its tie-break or its weighting, so those five cannot be
decided from the page.

**But the drift is measured, not guessed.** §2's own control claim — *"1,857 of the 1,888 rows
carrying one just say `Script_VM_Native_Bridge`"* — now reads **1,890 of 1,922**: the same shape
(a remainder of 32 against 31) with both totals about 34 higher. This page's `verified_against`
names `gzf_sha256: fa0db29…` and `project: work/headless_gn160/GFZ_GN160`, the **older** snapshot;
the pages audited this month carry `fb9b5e7…`. **The reach map is reproducible in method and stale
in detail, and the owner-tag row drifts the same way and by about the same amount** — which is what
a newer owner census, not a different method, looks like.

> **The right fix is a regeneration, not an edit.** Nothing here rewrites the fourteen numbers,
> because rewriting them would silently replace one snapshot's census with another's inside a page
> that states which snapshot it used.

- [x] **RC-21.** The depth-1, depth-2 and depth-3 per-subsystem counts at the current certified snapshot, regenerated
  with the stated counting rule and tie-break, beside the GN160 table this page keeps as history (five of fourteen
  depth-1 rows drift: ActorEntity, Party, WorldAreaField, Resource, Rewards). Registered 2026-09-30 (SWE2-CONTRACT);
  a static re-run of §2's method.
  *Applied 2026-09-30 (records) RC-21:* **ANSWERED 2026-09-30 (static; ORACLE's record `_index/candidates/rc21-verb-reach-regen-0930/`, commit `1e4537034`), and the premise is corrected: the five rows do not drift with the snapshot.** The generator breaks ties in Python set-hash order, so the GN160 table is one hash-seed draw of the same census: across 100 seeds the depth-1 partition always totals 616 while nine rows move within ranges (Movement 181–190, ActorEntity 135–154, Party 37–52, WorldAreaField 26–32, Resource 4–9, …), every published value is among the draws, and the old and current snapshots give identical labels. ORACLE's record breaks ties alphabetically and publishes each subsystem's range. *The §2 table is kept as written (this page is not this lane's to regenerate); its fourteen numbers are one draw, and the ranges are the record's.*

**Not claimed.** The depth-2 and depth-3 per-subsystem tables were **not** re-derived row by row,
only their totals. The tie-break the page used. Whether any individual verb's attribution is right —
this pass tested the census, not the semantics. Nothing was executed.

## The `00183070` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00183070` (17 B) — singleton forwarder: `call 001D8A60` then tail `jmp
001D8770` on the returned object (`00183074`/`00183080`).

| member | role | interior |
| --- | --- | --- |
| `001D8770` (26 B) | state reset — `dword[+8] = 0`; when `byte[+0x24]` is clear sets it and zeroes `dword[+0x20]`/`byte[+0x1D]` (`001D8775`/`001D877A`) | [`001D8775`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `001D8A60` (the singleton getter).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-CONTRACT)

- **ActorEntity — CLIENT and SERVICE (3 edges).** 2 inbound (ActorEntity bodies `ActorManager_RunFieldRuntimePass` (0025D9E0) call page-cited `00183070`, `002EFA70`); 1 outbound (page-cited `VMNativeCommand_ExecuteLifecycle` (002621D0) call ActorEntity bodies `ActorManager_GetRecordByOrdinal` (00358940)). Substantive edges include `00183070` is called by `ActorManager_RunFieldRuntimePass` (0025D9E0); `002EFA70` is called by `ActorManager_RunFieldRuntimePass` (0025D9E0); the remaining edges run through shared helpers the page cites.
- **CoreRuntimeScheduling — CLIENT (1 edge).** 1 inbound (CoreRuntimeScheduling bodies `0017D6E0` call page-cited `001D8A60`). Substantive edges include `001D8A60` is called by `0017D6E0`.
- **Presentation — CLIENT (1 edge).** 1 inbound (Presentation bodies `001D7A20` call page-cited `001D8A60`). Substantive edges include `001D8A60` is called by `001D7A20`.
- **Resource — SERVICE (3 edges).** 3 outbound (page-cited `001D6C20`, `00355EB0` call Resource bodies `001DADA0`, `001DA080`, `001D6C20`). Substantive edges include `001D6C20` calls `001DADA0`; `001D6C20` calls `001DA080`; `00355EB0` calls `001D6C20`.
- **SaveLoad — CLIENT (1 edge).** 1 inbound (SaveLoad bodies `00280140` call page-cited `002EFA70`). Substantive edges include `002EFA70` is called by `00280140`.
- **UI — CLIENT (1 edge).** 1 inbound (UI bodies `0027EFA0` call page-cited `002EFA70`). Substantive edges include `002EFA70` is called by `0027EFA0`.
- **WorldAreaField — CLIENT (3 edges).** 3 inbound (WorldAreaField bodies `WorldTransition_StageFieldTransition` (003145E0), `WorldTransition_RequeueCurrentFieldForRestore` (00314530), `WorldTransition_RequestFieldTransition` (00314440) call page-cited `002EFA70`). Substantive edges include `002EFA70` is called by `WorldTransition_StageFieldTransition` (003145E0); `002EFA70` is called by `WorldTransition_RequeueCurrentFieldForRestore` (00314530); `002EFA70` is called by `WorldTransition_RequestFieldTransition` (00314440).
