---
system: The event slot panel and its live feeder
category: 00-Engine-Core-Runtime
status: DOCUMENTED — every register row is closed: RC-5 ruled ANSWERED 2026-10-02 (OPUS's non-author
  ruling `67f9e40e1` on FABLE's consolidation — every stored value is an authored constant or a
  per-session player input with a static domain). Earlier "dead feeder" verdict retracted (producers
  reachable through 5-byte thunk hops, 2026-09-25, SWE2-DATA on FABLE counter-evidence); falsification
  pass 1 corrected one reachability row and one count (CON-185); section 6's residue answered from
  existing pages 2026-09-30. Stated limit, kept as a live-game observation not a static gap: which
  retail states run the §3 routes (the `evctrl`/`ctrl` debug controllers' retail reachability).
  (owner re-status 2026-10-02, SWE2-CONTRACT on FABLE's prechecks — documented_rule READY,
  adrift_predict HITS 0, audit_crossrefs 0 findings on this page)
owner_layer: CodeDomain:DeveloperConsole; no PrimaryOwner
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: "full-body disassembly of 0020A800/0020AC30/0020AF10 plus the thunk pair
    001EC660/001EC6A0 and their caller sites (0032FD64, 0026B775, 00354B6D, 00354EDA) —
    thunk hops confirmed with raw E8/E9 index over the shipping image; flag consumers
    confirmed inside 0025DF00 at 0025E0F0/0025E100"
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-event-slot-panel-falsification-pass-1
---

# The event slot panel and its live feeder

The developer menu can display a small panel of five **event asset slots** — each slot holds a
name such as `sum_…`, `spc_…` or `…0001…`, plus a count of queued events. **The feeder is reachable from
retail code** by static routes (§3): it classifies the `plan_master\<locale>\event\` paths the manager
resource-set load hands it, and a per-actor script driver consults the classification flags to decide whether
a wait slot parks. *Static routes do not show that every retail state executes them. That is a live question.*

> **Behaviour corrections (2026-09-25, FABLE, Claude Opus 5.5), re-read from the bytes.** Four statements of the
> repair below were wrong, and the positive caller routes it added stand unchanged:
> 1. The `0001` test lives **inside** the `sum_` arm, not in its absence, and `spc_` is the alternative to `sum_`.
>    So the two flags mean `sum_` + `0001` and `spc_` without `sum_`.
> 2. `001C5750` does not normalise a filename. It **reads the cutscene's JSON settings**: it loads
>    `JsonData/CutScenes/<name>.json` and applies `Common.mDofFocusDistance` and `Common.mDofApertureFnumber`
>    to the depth-of-field object.
> 3. Both `[rax+0x18]` calls **free temporary string storage** on the local strings' allocator, as
>    `(allocator, pointer, size)`. They do not load an asset.
> 4. A setter call with the **same name** as the slot's current one is not a no-op. The entry has already
>    cleared both flags, and the early return leaves them cleared. The setter and the pusher also treat the
>    index marker differently (§3).
>
> [The cutscene name-slot page](../../99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md)
> already had points 1 and 2 right.
>
> **Regression, from original-code replay, bounded:** `members/event_slot_setter_replay.py` (with its `.json`). It
> runs the shipped `0020AC30` and `0020AF10`, and `0020A760` for real. It stubs only the path regex, the text
> extractor, the EASTL string plumbing, memcmp, the JSON reader (it records the argument) and the notifier. **8/8
> cases hold:**
> - `sum_a0001` sets `01F832E8` and reads `sum_a0001.json`;
> - `n0001` sets nothing;
> - `spc_z0000` sets `01F832E9`;
> - `sum_x0000` reads its JSON and sets nothing;
> - `sum_spc_0001` sets only `01F832E8`;
> - a same-name repeat leaves both flags at 0 and reads nothing;
> - after a push to slot 2, `01DFE40C` stays 2;
> - a push of event −1 is refused, and the marker is left at 1.
>
> The mutants `0020AD3F je → jne` (the `sum_` branch) and `0020ACD2 je → jne` (the same-name exit) each fail their
> cases. Two runs gave byte-identical output. This is not live; which names retail feeds is not measured.

> **Correction (2026-09-25).** An earlier revision of this page called the feeder dead: it found
> **0** E8/E9 callers, **0** memory-operand references and **0** embedded pointers to
> `0020AC30`/`0020AF10` in the shipping image and concluded "unreachable". That census missed
> **thunk hops** — the producers are reached through `jmp` stubs (`001EC660`, `001EC6A0`) that the
> instrumented call graph does not follow into the far body. FABLE's `rawcalls.py` E8/E9 index
> found all four caller sites; each has been re-verified against the binary for this revision.

## 1. What the player sees

Nothing directly — the panel itself lives inside the developer console, which retail never opens.
But the mechanism it displays is reachable from retail code: setting a slot's name records it and
sets the two flags for `sum_…0001` and `spc_` names; a `sum_` name also applies that cutscene's
depth-of-field settings. The flags are read by the per-actor script driver's wait-park gate. *Which
retail states actually run these routes is not established.*

## 2. The slot table

Three parallel arrays of five elements each, plus two classification flags and an in-call index
marker:

| address | extent | contents |
|---|---|---|
| `01F832B0` | 5 × dword | per-slot pending-event counter |
| `01F832C4` | dword | cleared by the pusher each push *(answered: see the note below, `001EC690` also increments it; 2026-10-02, OPUS)* |
| `01F832C8` | `std::string` (0x20) | "current" name — copied from the slot record on every push |
| `01F832E8` | byte | set when the name contains `sum_` **and** `0001` (read via getter `0020AA40`); cleared at every setter entry |
| `01F832E9` | byte | set when the name contains `spc_` and **not** `sum_` (read via getter `0020AA30`); cleared at every setter entry |
| `01F832F0` | 5 × 0x20 | per-slot `std::string` — the classified event-path name |
| `01F83390` | 5 × 0x20 | per-slot `std::vector<int>` — queued event ids |
| `01DFE40C` | dword | index marker. The **setter** sets it and restores −1 on every exit; the **pusher** sets it and **leaves it set**; `001EC680` sets it to the slot, or −1 above 4 |

## 3. The producer pair — reachable through thunks

**`0020AC30(index, path)` — the name-classifying setter** (572 B; GFZ tag
`CutsceneAssetSlot.NameClassifyingSetter`):

1. Stores `index` to `01DFE40C`, clears both flag bytes, rejects `index > 4`.
2. `0020A800(path)` validates the path with a **`std::regex`** built from the literal at
   `00905958`: `(.*)(\\plan_master\\([a-zA-Z]+)\\event\\)(.*)` — a Windows-style path containing
   `\plan_master\<NAME>\event\`. No match → bail. The `[a-zA-Z]+` group is the **locale**
   (`us`, `kr`, `ch`, `cn`, `jp`, `in`, …), not a dev machine name: the image's own
   resource-path tables (`002DF980(kind,id)` → `g_pathTables` at `0215F000`) carry ~13,800
   `plan_master\<letters>\event\` strings in backslash form, and for the kinds the loader
   feeds (kind 8, rows `4*id`) the US table alone carries 284 such paths including 39 `sum_`,
   15 `0001` and one `spc_`.
3. `0020AA50` extracts the matched text into a local string. **If it equals the slot's stored name, the
   body returns at once** (`0020ACD2`). Both flags were already cleared at entry, so a repeated same-name call
   **clears the classification** and does nothing else. If the slot's pending counter is nonzero,
   `0020A760(index)` clears the previous state first: the current-name string, the slot's name, its event
   vector and its counter. The new name is then assigned into `01F832F0 + index*0x20`. *(FABLE, Claude Opus 5.5, 2026-09-25, re-read from the bytes.)*
4. Name classification, by substring (names shorter than 4 skip it):
   - **`sum_`** present → build `<name>.json` (`008FB2B4`) and call **`001C5750`, which reads the cutscene's JSON
     settings**. It loads `JsonData/CutScenes/<name>.json` and applies `Common.mDofFocusDistance` and
     `Common.mDofApertureFnumber` through `00194250` on the object at `[01F81300]`. The `[rax+0x18]` call that
     follows **frees the temporary `.json` string** (`0020AD8D`–`0020AD9A`). Then, **inside this arm**, **`0001`**
     present → set flag `01F832E8` (`0020ADB1`–`0020ADD6`).
   - **`sum_` absent** → **`spc_`** present → set flag `01F832E9` (`0020ADDF`–`0020AE16`).
   - On every path that built it, the final `[rax+0x18]` call **frees the local copy of the extracted name**
     (`0020AE34`–`0020AE44`). Neither virtual call loads anything. *(FABLE, Claude Opus 5.5, 2026-09-25, re-read from the bytes.)*
5. `01DFE40C` is restored to −1 on every exit path.

**`0020AF10(index, event_id)` — the event pusher** (203 B): copies the slot name into the
"current" string `01F832C8`, stores `index` to `01DFE40C`, `push_back`s `event_id` into the
slot's vector `01F83390 + index*0x20`, clears `01F832C4`, increments the counter
`01F832B0[index]`, then notifies a waiter via `00189120` + `0016D6A0`. **Its marker behaviour differs from the
setter's** *(FABLE, Claude Opus 5.5, 2026-09-25, re-read from the bytes.)*:
- The name copy happens **before** the bound check (`0020AF4A`–`0020AF56`, then `cmp edi, 4` at `0020AF61`).
- The pusher refuses an index above 4, an `event_id` of −1, and an empty slot name.
- It **never restores** `01DFE40C`. The marker stays at the pushed slot, and that is the value `001EC560` later
  probes.

**Reachability — the producers are live.** Both are reached through 5-byte `jmp` thunks that the
graph's caller columns do not follow:

| thunk | target | called at | context |
|---|---|---|---|
| `001EC660` | `0020AC30` | `0032FD64` in `ActorResource_BeginManagerResourceSetLoad` (`0032FCA0`) | per manager-slot loop: `ecx` = manager index (`edi`), `rdx` = `002DF980(kind, ebp)` — a path-table asset path; gated by `0032E400` existence check (`eax > 0` to proceed) |
| `001EC6A0` | `0020AF10` | `0026B775` in `0026B750`; `00354B6D` in `00354B20`; `00354EDA` in `00354E80` | `ecx` = slot (`[rax+0x28]`/`ebx`), `edx` = event id (`ebx`); ~~each site first calls `001EC680` = `min(slot,4); [01DFE40C] = slot`~~ **the two eventplay sites (`00354B63`, `00354ED0`) first call `001EC680`, which stores the slot, or -1 above 4 (`cmova`), in `01DFE40C`; `0026B750` calls the thunk directly, with `ecx` = `[[02099D70] + 0x28]` (corrected 2026-09-29, OPUS falsification pass 1, `CON-185`)** |

So the earlier "the feeder only ever made sense against a dev filesystem" claim is retracted:
the classifier runs on real retail loads, against the image's own path tables.

## 4. The live consumer side

The slot table's readers are reachable — and the flags' consumers are **not console-only**:

- `001CD0E0`, the console row renderer, reads `01F832B0` at ~~three~~ **four** sites (corrected 2026-09-29, OPUS falsification pass 1, `CON-185`: `001CD26E`, `001CD375`, `001CD3AC`, `001CD865`, each image-base-relative) — this is the panel.
- `001EC560` probes `[01DFE40C] ≤ 4 → 01F832B0[index]`, nonzero runs `00265680`.
- `001EC5C0` / `001EC5E0` call the flag getters `0020AA30` / `0020AA40`; `00180120` runs the
  `001EC5C0() && 001EC560()` conjunction as one arm at `00229A53`.
- **The per-actor script driver `0025DF00` calls both flag getters** at `0025E0F0`
  (`001EC5C0`, gated by `[r15+0x28]−1 ≤ 1` after `00357760`/`001ED130` checks) and `0025E100`
  (`001EC5E0`, when `[r15+0x28] == 3`) — an unfinished interpreter run consults the `0001`/`spc_`
  classification to decide whether the actor's wait slot parks.
- `001EC4B0` (three callers) reaches the eviction helper `0020A760`.
- `001D0190` and `001D0390`/`001D5260`/`001D5520` write/read the counters on the display side. *(Narrowed 2026-09-30, SWE2-CONTRACT: a census in both addressing forms finds the display side reading only — `001CD0E0` ×4 and `001D0190` ×1 — and no direct access from `001D0390`/`001D5260`/`001D5520`; the one counter write outside eviction is `0020AF10`'s `inc`. See the evidence table's last row.)*

## 5. What `sum_` / `spc_` / `0001` select

The classification is a **name-prefix dispatch** over the captured `<NAME>`:

- `sum_…` — the setter reads `JsonData/CutScenes/<name>.json` and applies its depth-of-field focus distance
  and aperture. **Within `sum_`**, a name containing `0001` sets flag byte `01F832E8`. All seven shipped `sum_`
  names on [the name-slot page](../../99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md)
  are `sum_<letter>0001`.
- `spc_…` — tested only when `sum_` is absent: flag byte `01F832E9`.
- `…0001…` without `sum_` sets **nothing**. *(Corrected 2026-09-25, FABLE: the repair said the reverse.)*

The flags are read both by console arms and by the script driver's wait-park gate (§4).

## 6. Residual unknowns

- ~~The interface behind the `[rax+0x18]` virtual calls is not followed.~~ It is the local strings' allocator,
  and both calls free temporary storage (§3, 2026-09-25).
- What `0025E0F0`/`0025E100`'s gate does for actors of manager kinds 1/2/3 beyond wait parking.
  *Answered (2026-09-30 pointer, SWE2-CONTRACT):* nothing beyond it. The gate decides whether an actor's script
  yields for the frame after the VM runs a step: a `spc_` bank's flag B suppresses one stop condition in world states
  1–2, and a `sum_…0001` bank's flag A enables one in state 3 (UQ-246, ANSWERED 2026-09-15, on
  [how a sound request becomes a voice](../../18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md);
  [the cutscene name-slot page](../../99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md)
  §10–§11). The consumer set is closed: seven call sites in four functions, `00180120`, `0025DF00`, `0034CF90`,
  `0034D790`, all read (UQ-336, ANSWERED 2026-09-15). Tier 1.
- Which retail states execute the static routes of §3, and with which names. ~~That is live.~~ *Not declared
  live (2026-09-30, SWE2-CONTRACT): the names and ids are first a static question, RC-5.*
- [x] **RC-5.** *(ticked 2026-10-02, FABLE: the register row was ruled ANSWERED at `67f9e40e1`, OPUS's non-author ruling - every stored value is an authored constant or a per-session player input with a static domain)* Which names and event ids the event-slot routes of §3 store: which `(kind, id)` path the manager
  resource-set load hands the setter through `0032FD64` in `ActorResource_BeginManagerResourceSetLoad`, and which
  event ids the pusher sites `0026B775`, `00354B6D` and `00354EDA` pass. Static first: the path comes from
  `002DF980(kind, id)` with the manager's own kind and index, and the pushes from event-play verbs and their
  operands, both of which original code and authored scripts can bound. Only the part those cannot settle would go
  to ASTRA, stated then. Registered 2026-09-30 (SWE2-CONTRACT).
  **Narrowed 2026-09-30 (static; SWE2-CONTRACT on ORACLE's record
  [`rc5-event-slot-routes-0930`](../../_index/candidates/rc5-event-slot-routes-0930/README.md), commit b6d40efbd):**
  - **Names.** `0032FCA0(m, s)` picks kind 8 row `4*s` for managers 1–3 (329 event-script paths, set ids 30–740, the
    same in all 13 region arms), kind 5 row `3*s` for manager 0 (709 `plan_map` global scripts, none matching the
    `\event\` regex, so slot 0's name is never set), and kind 1 for manager 4, which no caller passes. The stored name is
    the file stem: 13 are `sum_<x>0001` (flag A), 1 is `spc_z0000` (set id 210, flag B), 26 are other `sum_` names
    (JSON, no flag), 289 set nothing. No constant authored set id selects a `sum_` or `spc_` name.
  - **Event ids.** `00354B6D` (`eventplay_ec`) and `00354EDA` (`eventplay`) always pass −1, which the pusher refuses
    after copying the name and setting the marker, so they never queue an id. `0026B775` passes the scene id of
    `startscene` / `startscene_4b3`, queued only for a script running in manager 1–3 whose slot holds a kind-8 name;
    26,073 of 29,502 event-script `startscene` sites and 1,215 of 1,260 `startscene_4b3` sites pass constants.
  - Controls: `rc5_paths.py`, `rc5_verbs.py` (the `0x11B` site count reproduces the committed census, 34,125),
    `rc5_join.py`; FAILS 0. Tier 1 + authored data.
  - **Residue (still RC-5), narrowed 2026-09-30 (SWE2-CONTRACT on FABLE's dataflow record
    [`rc5-operand-dataflow-fable-0929`](../../_index/candidates/rc5-operand-dataflow-fable-0929/README.md), `63f4b8f89`):**
    of the 386 variable scene-id operands, **346 are exact constants** (`rc5_constprop.tsv`, all sites reached); the
    open residue is the **40 `startscene` sites in 8 event scripts whose value depends on authored request order**
    (request-entered functions stepping the counter — further static work, not live-only). Of the 19 `eventread_e8`
    set ids, 13 read never-stored un-aliased zero arrays (set id 0) and **6 stay unbounded**. ~~The authored `+0x24`
    word~~ enumerated from the nine action tables (flag-A `sum_<x>0001` ids → one bit-30 row's `+0x24`, rows 183–207;
    `spc_z0000` → 34 rows; plus 355, 0, FFFF). ~~`debug_eventload`~~ all 274 sites constant. ~~Which region arm is
    live~~ the boot language, changing no answer (ORACLE). Nothing here goes to ASTRA: all remaining items are static.
  - *Round 3 (records) RC-5:* **NARROWED again 2026-09-30 (SWE2-CONTRACT, `_index/candidates/swe2contract-rc-round3-0930/`, on SWE2-ORACLE's independent record [`rc5b-event-slot-residue-0930`](../../_index/candidates/rc5b-event-slot-residue-0930/README.md), `be7c6fcd6`, four scripts FAILS 0):** flag A is reached through the 13 Esper summon action rows (183–207, `+0x0C` bit 30, `+0x24` = the `sum_<x>0001` set ids; `0030CE10` → `00306BD0`); all 274 `debug_eventload` operands are constant (274 counts archive paths including locale copies; deduplicated by content they are 137 calls); the region arm changes no answer. The variable operands are bounded, assuming each increment runs once per pass (no loop check was run): the `startscene` counters lie in per-file intervals (at most 0–102; the exact value at a site is fixed by the straight-line order of resets and increments on the event's path); `startscene_4b3` 1–67; `summoneventread` is `choice + 39` / `choice + 57` on two `evctrl.ebp` menus, so 40–68; the `eventread_e8` array reads clamp their index and return initialiser elements. **The one value no build fact fixes:** `evctrl.ebp`'s `event_menu` passes the number the player types at its debug prompt (message `0x12`, accepted when 1 to 9999) as an `eventread_e8` set id. ORACLE's array bound supersedes the round-2 "6 `eventread_e8` arrays stay unbounded"; its counter intervals bound, and do not fix, FABLE's 40 request-order `startscene` sites. Limits ORACLE states: no loop analysis for the counter intervals; retail reachability of the `evctrl` / `ctrl` debug controllers. **Proposed disposition, for a non-author reviewer:** ANSWERED — the routes store names and ids from enumerated or bounded domains, and the remaining value is a per-session player input whose domain (1–9999) is itself the static answer. Not self-closed. Reviewed ACCEPT-WITH-NARROWING by SWE2-AUDIT-SPEC ([`auditspec-review-rc4-5-25-30-0930`](../../_index/candidates/auditspec-review-rc4-5-25-30-0930/REVIEW.md), `ccd10c206`; its two wording narrowings are applied here); the reviewer did not rule on the ANSWERED proposal.
- What the DOF object at `[01F81300]` does with the two values beyond `00194250`'s store.
  *Answered (2026-09-30 pointer, SWE2-CONTRACT):* `[01F81300]` is the `0x4A8`-byte render-parameter block
  `PostProcessParamContext` (the same object as `[01F7F5F0]`, `0015CAF0`). `00194250` stores `+0x110` (enable),
  `+0x114` (focus distance), `+0x118` (aperture f-number), `+0x11C` and `+0x120` (35.0); the frame build `0018EEE0`
  copies them into the post-process frame parameters `+0x20`..`+0x2C`, and step 7 hands them to the depth-of-field
  library, which divides the lens length by 1000 and skips every lens setting when the enable is 0
  ([the post-processing contract](../../17-Presentation-Rendering/Post-Processing/CONTRACT-post-processing-subsystem.md)
  §4 and §4a; [the render command list](../../17-Presentation-Rendering/Render-Command-List/the-ordered-render-command-list.md)'s
  field census). Tier 1. What the picture looks like is not claimed.
- A live read of the `01F832F0` names after an event map load would pin the populated values. *(One possible
  observation for RC-5 above, if its static half leaves anything open.)*
- `00265680` (run when a slot reports pending events) is unexamined.
  *Answered (2026-09-30 pointer, SWE2-CONTRACT):* it is read. It requires manager slot 0 live with `+0x10` bit 7 and
  `+0x11` bit 0 clear, every live slot's `+0x17` bits 0–1 set (`002656C0`–`002656DF`), no entry of the eight
  `0x68`-byte records at `0215F200` flagged at `+0x38`/`+0x3E` bit 7 (`002E0540`), and then `00265720()`; ~~it is one of~~
  ~~the field frame's three entry gates~~ it is not a gate itself but the test inside the third gate `001EC560` (called at `001EC560+0x20`; the field frame `0022A770` calls its gates `001800E0`, `001800C0`, `001EC560` at `0022A770+0x449`, `+0x452`, `+0x45B`) *(corrected 2026-10-02, OPUS: read at those calls)* ([the world tick and the field frame](../Battle-Frame/the-world-tick-and-the-field-frame.md),
  "The three entry gates" row, tier 1).

## Key addresses (SWE2-CONTRACT, 2026-09-30)

| Address | Working name | Body | Role |
|---|---|---:|---|
| `0020AC30` | name-classifying setter | 572 B | `(index, path)`: clears both flags, validates, stores the name, classifies `sum_` / `spc_` / `0001` |
| `0020AF10` | event pusher | 203 B | `(index, event_id)`: queues the id, bumps the slot counter, leaves the marker set |
| `0020A800` | path validator | 554 B | the `std::regex` over `\plan_master\<locale>\event\` |
| `0020AA50` | match extractor | 476 B | copies the matched text into a local string |
| `0020A760` | slot eviction | 146 B | clears a slot's name, vector and counter |
| `001EC660` / `001EC6A0` | the two thunks | 5 B each | `jmp 0020AC30` / `jmp 0020AF10` |
| `001EC680` | marker setter | 16 B | slot, or −1 above 4, into `01DFE40C` |
| `001EC560` | pending probe | 59 B | `01F832B0[marker] != 0` and ~~`00265680()`~~ `00265680() == 0` *(corrected 2026-10-02, OPUS: `001EC560+0x25`–`+0x2A`, `test eax, eax` then `je` to the 1 result)* |
| `0020AA30` / `0020AA40` | flag getters | 8 B each | flag B `01F832E9` / flag A `01F832E8` |
| `001EC5C0` / `001EC5E0` | flag wrappers | 17 B each | the getters' only callers |
| `001C5750` | cutscene JSON reader | 467 B | applies `mDofFocusDistance` / `mDofApertureFnumber` |
| `0032FCA0` | `ActorResource_BeginManagerResourceSetLoad` | 936 B | calls the setter at `0032FD64` |
| `0025DF00` | `WorldActor_UpdateRuntimeAndScriptExecutionState` | 1,228 B | reads both flags at `0025E0F0` / `0025E100` |
| `001CD0E0` | console row renderer | 11,276 B | draws the panel |
| `00265680` | manager-slot readiness ~~gate~~ test | 149 B | ~~one of the field frame's entry gates~~ the test inside gate `001EC560` *(corrected 2026-10-02, OPUS: `001EC560+0x20`)* |

## Call chain (SWE2-CONTRACT, 2026-09-30)

```
manager resource-set load 0032FCA0
  -> 0032FD64 call 001EC660 -> 0020AC30 (index = manager slot, path = 002DF980(kind, id))   <- THIS SYSTEM (names)
       -> 0020A800 regex, 0020AA50 extract, 0020A760 evict, 001C5750 (sum_ names)
event play 00354B20 / 00354E80, and 0026B750
  -> 001EC680 (marker; the two eventplay sites only) -> 001EC6A0 -> 0020AF10 (slot, event id)  <- THIS SYSTEM (queue)
readers
  -> 0025DF00 per-actor driver: 001EC5C0 / 001EC5E0 -> flags -> whether the actor's script yields (UQ-246)
  -> 00180120 and the field frame's gates: 001EC560 -> 01F832B0[marker], 00265680
  -> 001CD0E0 the console panel
```

**Upstream (who causes this):** loading a manager's resource set (names) and the script's event-play verbs (queue).

**Downstream (what this causes):** a `sum_` name applies its cutscene's depth-of-field settings; the two flags change
when an actor's script yields; a pending slot takes part in the field frame's gate.

**Do not confuse with:** [the cutscene name slots](../../99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md),
which decodes the same arrays from the cutscene side, and the console's own tuning block.

## Modding notes (SWE2-CONTRACT, 2026-09-30)

- **Best intervention point:** the authored event file names. The classification is by substring, so a file renamed
  to or away from `sum_…0001` or `spc_` changes the flags the per-actor driver reads.
- **Breaks if:** a name is re-set to the same value: the setter clears both flags on entry and returns early, so the
  classification is lost until a different name is set (§3, point 4 of the behaviour corrections).
- **Regenerates itself:** the marker `01DFE40C` is restored to −1 by the setter but left set by the pusher.
- **Multiplayer / XIIOnline:** the slots are local state derived from what each client loads; they are not an
  authority.

## Evidence — claims, evidence and tier (SWE2-CONTRACT, 2026-09-30)

| Claim | Evidence | Tier |
|---|---|---|
| Both producers are reachable, through `001EC660` / `001EC6A0` | raw E8/E9 index (`rawcalls.py`) and falsification pass 1 S1 | 1 |
| The setter's order: flags cleared, same-name exit, eviction, `sum_` → flag A inside its arm, `spc_` only without `sum_`, one −1 restore | falsification pass 1 S2; `members/event_slot_setter_replay.py` 8 of 8 on shipped bytes | 1 + isolated original-code execution |
| The pusher copies the name before the bound check and never restores the marker | falsification pass 1 S3; the same replay | 1 + isolated original-code execution |
| The flag consumer set is closed | UQ-336 and UQ-246, three scans | 1 |
| `[01F81300]` is the render-parameter block and the two values reach the depth-of-field library | the post-processing contract §4/§4a; the render command list's field census | 1 |
| `00265680`'s conditions | the world tick page's entry-gate row | 1 |
| ~13,800 `plan_master\<letters>\event\` paths, 284 in the US kind-8 rows, 39 `sum_` | stated in §3 from the 2026-09-25 repair; the census that produced it is not retained | not stated — unanchored |
| The counters are touched on the display side by `001D0190`, `001D0390`, `001D5260`, `001D5520` (§4) | not re-derived. A rip-relative census on 2026-09-30 (`_index/candidates/swe2contract-ddres-b1-0930/rip_refs_01F832B0.out`) finds the array's base taken by `001CC600`, `001CC800`, `001CC920` and the probes, and none of those four; they may reach it through the image-base-relative form `001CD0E0` uses, which that census cannot see. **Answered 2026-09-30 (SWE2-CONTRACT, on SWE2-AUDIT-SPEC's review of batch 1; `_index/candidates/swe2contract-ddres-b4-0930/counter_access.py`, both addressing forms, controls C1/C2 pass):** the display side only reads the counters, through the image-base-relative form: `001CD0E0` four reads (`001CD26E`, `001CD375`, `001CD3AC`, `001CD865`) and `001D0190` one `cmp` at `001D01EE`; `001D0390`, `001D5260` and `001D5520` have no direct access (a pointer handed to them is outside this sweep). The other image-base-relative accesses are the queue side: `0020AC30` `cmp` at `0020ACD8` and the event pusher `0020AF10` `inc` at `0020AFB4`. | 1 — the claim holds for `001D0190` (a read) and not, in either addressing form, for the other three (answered 2026-09-30) |

*The last row's "no direct access" is bounded by its census: a pointer to the counters handed to one of the three is outside it, and the row claims no more than that.*
*`01F832C4` has one more writer than §2 lists: `001EC690` increments it (`001EC690`, same census).*

## Related (SWE2-CONTRACT, 2026-09-30)

- [the cutscene name slots and the depth-of-field sidecar](../../99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md) — the same arrays and flags from the cutscene side.
- [the post-processing contract](../../17-Presentation-Rendering/Post-Processing/CONTRACT-post-processing-subsystem.md) — where the depth-of-field values go.
- [the world tick and the field frame](../Battle-Frame/the-world-tick-and-the-field-frame.md) — the entry gates that read the pending probe.

## 7. Methodology note

The four-instrument census (E8/E9 caller columns, memory-operand scan, raw qword/dword image
scan, plus thunk-hop enumeration) is blind to **`jmp`-stub reachability**: `001EC660`/`001EC6A0`
appear as the direct E8 targets in callers, and the hop to the far body lives only in the thunk's
5-byte tail. Reachability verdicts from this census must either follow thunks (as
`rawcalls.py` does) or state the limitation. This was the second corrective of that class in the
graph tooling.

## Cross-subsystem neighbours — SWE2-EC7 (pass-22 dispositions)

- **ActorEntity - SERVICE (21 edges).** `0025DF00` reaches bodies filed to ActorEntity: `00359B80`, `003DB2A0`, `003DB550` - shared machinery across the layer boundary, no shared ownership.
- **Audio - SERVICE (1 edge).** `001CD0E0` reaches bodies filed to audio: `002DEBA0` - shared machinery across the layer boundary, no shared ownership.
- **Input - CLIENT (2 edges).** `00265680` is also called by bodies filed to input: `00253C70`, `002E09A0` (CommandGateBoundarySupport) - shared machinery across the layer boundary, no shared ownership.
- **Movement - CLIENT and SERVICE (10 edges).** `001EC5C0`, `001EC5E0`, `001ED130` are also called by bodies filed to movement: `0025DF00`; `0025DF00` reaches bodies filed to movement: `0026D6F0` - shared machinery across the layer boundary, no shared ownership.
- **Party - CLIENT (2 edges).** `00265680` is also called by bodies filed to party: `00358CB0`, `00358F90` - shared machinery across the layer boundary, no shared ownership.
- **PlatformOnlineAchievements - SERVICE (1 edge).** `001CD0E0` reaches bodies filed to PlatformOnlineAchievements: `003166F0` - shared machinery across the layer boundary, no shared ownership.
- **Presentation - CLIENT and SERVICE (25 edges).** `00194250` is also called by bodies filed to presentation: `001C3D50` (Rendering), `001C5750` (Rendering), `001C7940` (Rendering); `00180120` reaches bodies filed to presentation: `001EC560` (Cutscene) - shared machinery across the layer boundary, no shared ownership.
- **Resource - CLIENT and SERVICE (17 edges).** `001C5750`, `0020A760`, `0020A800` are also called by bodies filed to resource: `0020AC30` (CutsceneAssetSlot); `001CD0E0` reaches bodies filed to resource: `0020C700` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (22 edges).** `001EC4B0`, `001EC5C0` are also called by bodies filed to script VM / native bridge: `00350960`, `00356D40`, `0034CF90` - shared machinery across the layer boundary, no shared ownership.
- **Status_Periodic_Terminal - CLIENT (1 edge).** `00265680` is also called by bodies filed to status/periodic terminal: `00310DB0` - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT (1 edge).** `00265680` is also called by bodies filed to UI: `00279E20` - shared machinery across the layer boundary, no shared ownership.
- **World - CLIENT (1 edge).** `0032E400` is also called by bodies filed to World: `00378540` (Area) - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT and SERVICE (11 edges).** `001EC560` is also called by bodies filed to WorldAreaField (world area): `001EDCD0` (AuthoredPresentationCondition); `001CD0E0`, `001ED130` reach bodies filed to WorldAreaField (world area): `00265270`, `00314910` - shared machinery across the layer boundary, no shared ownership.
- **CombatAction — CLIENT and SERVICE (4 edges).** 2 inbound (CombatAction bodies `BattleAction_TryEnterGlobalSpecialSequence` (0030CE10), `0030CBE0` call page-cited `BattleAction_InitializeGlobalSpecialSequenceMode` (00306BD0), `BattleAction_TryEnterGlobalSpecialSequence` (0030CE10)); 2 outbound (page-cited `BattleAction_InitializeGlobalSpecialSequenceMode` (00306BD0), `BattleAction_TryEnterGlobalSpecialSequence` (0030CE10) call CombatAction bodies `BattleSpecialSequence_DeriveActionPresentationCode` (00309230), `BattleAction_InitializeGlobalSpecialSequenceMode` (00306BD0)).
## Falsification pass 1 — 2026-09-29 (OPUS): the producers, the setter and the pusher survive; one reachability row and one count do not

**Attack.** Sections 2 to 4 were turned into checks at their instructions. Every caller and thunk hop the page states
was re-counted with a raw E8/E9 sweep. The panel's reads were searched for both RIP-relative and image-base-relative
forms. Script: `Tools/analysis-kit/gfz-scripts/falsify_event_slot_panel.py`, output `falsify_event_slot_panel.out`,
image `73461d08…`, 0 BROKEN, exit 0. FABLE's original-code replay is carried, not re-run. Section 6's open items stay
open.

| # | Clause attacked | Result |
|---|---|---|
| S5 | the pusher row: "each site first calls `001EC680` = `min(slot,4); [01DFE40C] = slot`" | **refuted** (`CON-185`). `001EC680` stores the slot, or -1 above 4, and only `00354B63` / `00354ED0` call it. `0026B750` calls the thunk directly |
| S6 | section 4: "reads `01F832B0` at three sites" | **refuted** (`CON-185`): four base-relative reads |
| S0 | sizes | **survives**: all seven |
| S1 | the thunk routes and the regex | **survives**: `001EC660` has one site, `001EC6A0` three; the literal is as quoted |
| S2 | the setter | **survives**: flags cleared first; the same-name exit; the eviction; `sum_` → `01F832E8` inside its arm; `spc_` only without `sum_`; one `ret`, after the single -1 restore |
| S3 | the pusher | **survives**: the name is copied before the bound check; the -1 and empty-name refusals; the marker is never restored |
| S4 | section 4's consumers | **survives**: the driver's two flag reads, `00180120` at `00229A53`, `001EC4B0`'s three callers |

Corrected in place: the pusher row and the read count. The consumer record is
`_index/candidates/event-slot-panel-falsification-pass-1-0929/`.
