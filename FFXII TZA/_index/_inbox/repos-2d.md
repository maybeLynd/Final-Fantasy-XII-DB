# repos-2d — C-9 / C-10 / C-11, then C-12 and the R2 force-fight toggle

Session project: `Tools/work/proj_h2d` (`GFZ_H2D`). Checkpoint verified before any reading:
ledger 38,161 / 38,003 explicit / **158 unresolved** / 99.58596 %, snapshot
`46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2`, embedded EXE
`73461d08…`, residual `c5d4b7f7…`. Read-only throughout — no `Apply-*`, no `Pack-*`.

Scratch and instruments: `Tools/work/repos-2d/` (`sweep.py`, `reach.py`, `argscan.py`,
`dispscan.py`, `gatescan.py`, `filetab.py`, `findptr.py`, `navimap.py`, `statusdef.py`,
`listhelp.py`, `mapnames.py`, `joinmaps.py`, `ff12text.py`). Extracted authored data under
`Tools/work/repos-2d/vbf/`.

## COVERAGE

New document, `03-World-Area-Field`:

- `03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md` — **DOCUMENTED**,
  tier 1, 1 falsification pass recorded in §10, **`crossref_clean: true`** (§11 dispositions every
  finding). All cited addresses resolve; `verify_doc_addresses.py` flags `0030E88B`/`0030E88C` as
  `.text` non-function citations to confirm — correct, they are the tail of `0030E360`'s body and
  the jump table after it, both declared in the data-address block.

Existing document edited (same category, mine):

- `03-World-Area-Field/Field-Record-Table/field-record-bit15-action-permission.md` — §7 rewritten
  (C-9/C-10/C-11 closed with answers + links), §9 gains the new document, a correction note added
  about the **three** status masks, `reopened_count: 0 -> 1`. Status left at `DOCUMENTED`; its own
  falsification pass no longer covers the new material, so it owes a fresh one before `AUDITED`.
  Also **`crossref_clean: false -> true`**, and its C-12 paragraph now names the consumer.

`03-World-Area-Field` document count therefore rises by 1.

## OPEN-QUESTIONS

### Closed

| ID | Resolution |
|---|---|
| **C-9** | **Status ids 0 = KO, 1 = Stone, 31 = "vanished without a trace, cannot be reversed".** The three states a unit never returns from: each runs the same defeat cleanup + `BattleUnit_ProcessDefeatRewardsAndLoot`, and `BattleUnit_RecoverFromTerminalStatusSetIfClear` recovers only when **all three** are clear. Status 1 emits presentation event `0x200C`, status 31 emits `0x200E`, status 0 emits none. Naming carried by four independent cross-checks (§10 of the new document), not by the help text alone. |
| **C-10** | The table is the shipped **`navimapdata.bin`** (magic `NAV\x02`, `u32` count 1154 at `+4`, `8 + 3*1154 == 3470` exact). **193 of 1,154 fields set bit 15**, and they are towns, villages, shop interiors, plazas, aerodromes, airship interiors, story rooms and 23 unnamed system slots. Full run-by-run list with zone names in §4. |
| **C-11** | `flags` bits 0-11 = navigation-map entry id (`0xFFF` = none, returned as `-1`); bits 12-13 = a save-overridable 2-bit selector consumed by primary-resource gain and AI target selection; bit 14 = area-name display; bit 15 = the action-permission override. Third byte: bit 0 = the same safe-area flag for a different consumer set, bits 1-3 authored but read by nothing, bits 4-6 = a per-field **default focus combatant id** consulted only in runtime mode 3 (the mode bit 15 produces) and **`0` on every shipped field**. |

`L-8` (spawn) and the status half of `Z-17` are answered by the same finding — L-8 asks exactly
what C-9 asked. Suggest closing L-8 with a pointer rather than duplicating.

### New (assign real prefixes at merge)

| Proposed ID | Owner document | Question |
|---|---|---|
| `PROPOSED-repos2d-1` | field-record-table-navimapdata.md | Designer name for bit 15 / the safe-area flag. Behaviour proven, label not recovered. |
| `PROPOSED-repos2d-2` | field-record-table-navimapdata.md | Meaning of `flags` bits 12-13 (values 0:945 1:36 2:69 3:104) and of the save override at `payload[0x1062] bit 7` → `payload[0x1063] bits 4-5`. Consumers: `002F91A0`, `002F9240`, `002F9400`, `00301AD0`. |
| `PROPOSED-repos2d-3` | field-record-table-navimapdata.md | Third-byte bits 1-3: authored across 638 fields, read by nothing in this executable. |
| `PROPOSED-repos2d-4` | field-record-table-navimapdata.md | The three resource publishers (`00378B80`, `00378BB0`, `00378F70`) store the delivered pointer **zero-extended from 32 bits**, yet every reader dereferences it as a 64-bit pointer. |
| `PROPOSED-repos2d-5` | field-record-table-navimapdata.md | Which authored action/script/item applies status **31 (Vanished)**. No native call site passes any status id but `0` as a constant. |
| `PROPOSED-repos2d-6` | **ANSWERED — see the follow-up block** | **C-12 remainder.** What the toggle at `DAT_020927E0` actually is. Proven: a two-state value flipped once per input edge (`DAT_020927E4` is the latch), with `DAT_01E0C2B4` a sticky override, forced **off** when the field record's bit 15 is set, handed to `FUN_00252B60` which routes it through the gameplay capability mask (`FUN_002E0FA0`) and `FUN_0035C880(0xC, …)`. Naming it needs 15-Input, which I may not write in. |

### C-12 — substantially closed

`C-12` asked what the "structurally different consumer around `DAT_01E0C2B4` / `DAT_020927E0`"
was. **It is `InputGameplay_ArbitrateDigitalInputAndModalState` (`00253C70`, Input, 1,599 B)**,
which reaches the predicate twice — directly at `00254067` and through the thunk at `00254232` —
making it one of only two functions in the image that use both routes. A full-body sweep for
rip-relative references finds all 4 sites of `DAT_01E0C2B4`, all 5 of `DAT_020927E0` and both of
`DAT_020927E4` **inside that one function** (positive control: the same sweep found all 6 sites of
`DAT_02F97360`, which really is shared). So it is not a separate subsystem — it is one function's
private modal state, and bit 15 forces its toggle off. Mechanism written out in §11 of the new
document. Suggest marking C-12 **partially closed**, with the remainder as
`PROPOSED-repos2d-6` under 15-Input.

## AUDIT-LOG

**repos-2d, 2026-09-02 — C-9/C-10/C-11 block. Five attacks, three landed on my own work.**

1. *"navimapdata.bin is not the table."* Four checks, three able to fail independently: exact
   size arithmetic (`8+3*count == 3470`), the file's `NAV` magic, the **31-slot** distance
   between resource indices 8 and 39 matching the 31-slot distance between `navimapdata.bin` and
   `gramap_weatherinfo.bin` in the executable's path array, and the sibling file parsing exactly
   under the *MWeather* reader this database already documents (`u16` count at `+6` = 776;
   776 × 3 × 9 bits + 8 = 2,627 ≤ 2,628). **Not broken.**
2. *"the status help list is off by one."* **It was** — `listhelp_status.bin`'s block is
   `[count][32 offsets]`, and reading 33 offsets shifts every name by one id. Caught by four
   agreements that all fail under the wrong reading: Petrify/Doom are exactly the ids with a
   non-zero `+9` timer (45, 100); Sap↔Regen and Slow↔Haste clear each other in `status_data.bin`,
   matching their help text's *"Remove by casting …"*; Stone's clear-mask contains Petrify.
   **Broken, corrected, corrected reading survives.**
3. *"planmapname.bin indexes a different id space."* Joining it from where its data appears to
   start gave agreement **0.510** against a stated null of 0.503 — *chance*. Indexing it as the
   engine's own reader `00377B60` does (`u16` at `table + 0x10 + 2*id`) gave **0.951**. My first
   join was wrong by 48 ids and would have published beautiful, wrong zone names.
   **Broken, corrected.**
4. *"the 117/173 pairing statistic is a window artefact."* ±8 → 116, ±25 → 117. **Not broken**,
   and the 55 no-escape sites are a real population (`PartyFollow_SolveFormation` and both reward
   functions are among them).
5. *"`00377BA0` is dead code — zero callers."* Enumerated every route this database knows: direct
   edges, thunks, rip-relative `lea`, 8-byte data pointers, and a `call`/`jmp rel32` instruction
   census with a positive control (80 instructions target `00377C20`). The last route found a
   **tail-call thunk** at `00320160` with four callers in three subsystems. **"Dead code"
   withdrawn before it was written.**

**Instrument note for the fleet.** `edges.tsv` does not carry tail calls: `00320160` is a 5-byte
`jmp rel32` the ledger already names `thunk_FUN_00377ba0`, and its four callers are invisible to a
caller census of the target. This is the same defect class as the `00313F60` thunk finding in the
bit-15 document's own pass 9 — worth a sweep across documents that assert a caller count.

**Caller-count arithmetic, four questions four answers** (per the coordinator's caution):
`00377C20` has **65 distinct direct callers** in the graph; **110 distinct functions** reach it
counting the `00313F60` thunk route; **80 `call`/`jmp rel32` instructions** in the image target it
directly; **117 of 173** `0x80000003` test instructions sit within a few instructions of a call to
it or its thunk. This document states which it means at each use.

### Corrections owed by documents I may not edit

1. **`10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md`** and every
   document printing the `0x80000003` gate: there are **three** 32-bit status masks per combatant,
   not two — `+0x38`, `+0x3C`, `+0x64` — selected by a six-way operation mode read from the jump
   table at `00120000 + 0x1EE88C` in `0030E360`:

   | mode | 0 | 1 | 2 | 3 | 4 | 5 |
   |---|---|---|---|---|---|---|
   | field | `+0x64` clear | `+0x3C` clear | `+0x38` clear | `+0x64` set | `+0x3C` set | `+0x38` set |

   The gate ORs `+0x3C | +0x64` and **ignores `+0x38`**, so every published expression is still
   correct; the *description* of the two fields as "the two effect layers" is not. They are also a
   different structure from the 128-bit layers at `+0x68`/`+0x78` that document owns.

2. The GFZ's typed names map as **`dwStatusMaskMode0_3` = `+0x64`**, **`dwStatusMaskMode1_4` =
   `+0x3C`**, `dwStatusMaskMode2_5` = `+0x38`. Several documents print the first two the other way
   round. Harmless to the expressions (they are OR'd), wrong as a layout claim — and
   `check_layout_units.py` will not catch it because the offsets are real byte displacements.

3. `13-Rewards-Progression-Economy/experience-and-license-point-award.md` and
   `05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md` describe the mask as
   "status conditions". They can now say **KO / Stone / Vanished**, which makes the reward rule
   read as the design it is: *a defeated, petrified or vanished character earns nothing.*

### Reusable findings the fleet does not appear to have

- **The FFXII authored-text charset**, derived in-file and proven twice:
  `'A' = 0x20`, `'a' = 0x3A`, space `0x04`, digits `0x85`-`0x8E`, `_` `0xA3`, `-` `0xA5`,
  `,` `0xA7`, `.` `0xA8`, `'` `0xAC`, quotes `0xAE`/`0xAF`. Proof: the Doom help string reads
  *"will be KO'd when the count reaches 0"*, and map codes decode as `rbn_z01`, `alc_z01`.
  Decoder: `Tools/work/repos-2d/ff12text.py`. This unlocks every `st2e` list file —
  `listhelp_*`, `menu_*`, `help_*`, `word.bin`, `questtitle.bin`.
- **The `st2e` container format**: `magic 'st2e' | u32 count | u32 stride | u32 dataOffset |
  … | u32 ids[count] @0x20 | block@(u32 at +0x14): count, hdr, blobSize, then offsets`.
  `status_data.bin` (count 32, stride 40, data at `+0x20`, 1,312 bytes exact) is the table the
  engine indexes through `DAT_02EBF118`. `Tools/work/repos-2d/statusdef.py` parses it and prints
  each status's default timer and its **clear-on-apply mask** — the authored "applying X removes
  Y" table for all 32 statuses.
- **The `PLMN` format** (`planmapname.bin`): `u16` offset table at `+0x10`, absolute string
  offsets, `count` at `+4` field names followed by `count2` at `+8` **area** names (1312 + 59 =
  1371, the header's third field). Three native readers confirm it: `00377B60`, `00377870`,
  `003778B0`. This is a field id → English zone name table for the whole game.
- **The executable's file table**: a `.data` array of `PS2Data\…` path pointers indexed by the
  same `(kind, index)` pair the resource request API takes, matching the shipped
  `FileSizeTables\FileSizeTable_*.fst`. `Tools/work/repos-2d/filetab.py` /`findptr.py` resolve
  either direction. This is how an authored resource name in the executable is turned into a real
  file in the VBF, and it should generalise to every other `Resource_SubmitRequest` call site.
- Selective VBF extraction without unpacking 31 GB: `D:\FFXII MP Mod\exports\vbf_extract.py`
  (already on this machine, MD5-verified per file).

## CALL-CHAINS / ADDRESS-INDEX

New entries for `ADDRESS-INDEX.md` (all verified as function entries against
`Tools/work/graph_gn/functions.tsv`):

| Address | Working name | Doc |
|---|---|---|
| `00377480` | `FieldRecord_GetBit15ByFieldId` | field-record-table-navimapdata.md |
| `003779F0` | `FieldRecord_GetNavigationMapIdByFieldId` | " |
| `00377A40` | `FieldRecord_GetBit14ByFieldId` | " |
| `00377BA0` | `FieldRecord_GetBits12To13OrSaveOverride` | " |
| `00320160` | `thunk_FUN_00377ba0` *(ledger name)* | " |
| `00377700` | `FieldRecord_GetThirdByteBit0Inverted` | " |
| `00377C70` | `FieldRecord_GetDefaultFocusCombatantId` | " |
| `00378540` | `WorldAreaField_RequestAuthoredMapTables` | " |
| `00377CC0` | `WorldAreaField_BootMapTables` | " |
| `00378B80` / `00378BB0` / `00378F70` | resource publishers for `02ADD100` / `02ADD0F8` / `02ADD0B0` | " |
| `00377B60` / `00377870` / `003778B0` | `PLMN` field-name / area-name readers | " |
| `0032E400` / `0032E620` | `Resource_GetFileSizeByKindAndIndex` / `Resource_SubmitRequest` | " |
| `00314A60` / `00314AA0` / `00314AC0` | save-payload flag getters `0x1062.0`, `0x1062.7`, `0x1063.4-5` | " |

New cross-subsystem chains for `CALL-CHAINS.md`:

```
authored navimapdata.bin
  -> 00377CC0 -> 00378540 -> Resource_SubmitRequest(9,8) -> 00378B80 -> DAT_02ADD100   [WorldAreaField OWNER]
     -> 00377C20 / 00313F60 -> 15 subsystems                      (the 0x80000003 waiver)
     -> 0030D9A0 mode 3 -> 00326500 -> 00377C70                   (default focus combatant)
     -> 00377700 -> 6 ActorEntity/Movement consumers              (third-byte bit 0)
     -> 003779F0 -> UI + 003160C0 achievements seen-map bitmap    (navigation-map id)
     -> 00320160 (tail-call thunk) -> 00377BA0 -> CombatAction / Status / CombatAI
                                                                  (primary-resource gain, AI targeting)

HP reaches 0
  -> 00300530 BattleStats_ModifyHPAndProcessLethalState
     -> 0030E360 (status id 0, add-mode 3)                        [Status OWNER]
        -> 00300FC0 defeat cleanup -> 00312280 rewards + loot     [Rewards]
   status 1 (Stone) and 31 (Vanished) enter the same path, plus 003299B0 events 0x200C / 0x200E
   removal of any -> 00301140, which recovers only when all three are clear
```

## Not done / left for whoever picks this up

- `audit_crossrefs.py` not run against the new document (`crossref_clean: false`).
- No runtime observation was taken; the third-byte bits 4-6 modding advice is marked untested.
- The 59 **area** names in `planmapname.bin` are not joined to fields — that needs the area-id
  space behind `MapRef_GetPersistenceGroupId` (`00264F90`).
- `C-12` (the `DAT_01E0C2B4` / `DAT_020927E0` consumer) untouched.

---

# Follow-up block: C-12 remainder, and two closures in 00-Engine-Core-Runtime

New document, `15-Input` (category assigned by the coordinator for this task):

- `15-Input/Modal-Toggles/r2-force-fight-toggle.md` — **PARTIAL** (deliberately: §7's first entry
  is what the mode looks like on screen, left UNKNOWN rather than labelled), tier 1,
  `crossref_clean: true` (§10 dispositions all 9 first-pass findings), `audit.passes: 0`.
  52 addresses cited, all resolve (37 entries, 13 data, 2 interior).

Document counts rise by **1 in `03-World-Area-Field`** and **1 in `15-Input`**.

**Pre-existing, not mine:** auditing all of `15-Input` reports **20 findings across 5 documents**;
my document contributes **0**. The other 20 belong to the four documents already there, untouched.

## What was learned

**The R2 button toggles force fight mode, and the field record's town bit pins it.**

`PROPOSED-repos2d-6` asked what the toggle at `DAT_020927E0` is. Answered by following the output
rather than guessing at the input:

1. **The input is R2.** `FUN_0017DE10` calls `GetBinding(profile 0, group 0, slot 9)` — the read
   surface `00197710` that `keymap-ini-file-format-and-default-controls.md` documents. The name
   table at `01DF11E0` gives group 0 slot 9 = **`R2`**, and that document's own finding — *the
   name's index is the slot's index* — is what makes this a lookup, not an inference.
2. **The output is force fight mode.** `FUN_00252C80` writes `01E0C2B8`, the flag
   `00-Engine-Core-Runtime/Force-Fight-Mode/force-fight-mode.md` already documents from the game's
   own script verb `setforcefightmode`.
3. **The polarity is inverted, and worth stating loudly.** `state == 0` *sets* the flag (subject to
   the feature enable); `state != 0` *clears* it. So the button's job in the field is to **clear**
   force fight mode, and a town restores the engine's default. That document already warns about
   its predicate's polarity; this is a second inversion one level up.
4. **The pin has two independent routes** — the release path's direct `FieldRecordBit15()` test,
   and capability policy row 2 bit 10, which the same bit drives. That is why holding the button
   does not defeat it.

## OPEN-QUESTIONS — two closures in a category I do not own

**I have not edited `force-fight-mode.md`.** Both closures are filed here for its owner.

| ID | Resolution |
|---|---|
| **AN-2** | *"What `FUN_00252C80` does with the flag."* It is the **applier of the R2 modal toggle**. Complete 134-byte body in the new document §2e: it refuses entirely when `flag == 0` and either `003603B0()` or `003603C0()` is non-zero; refuses when the flag already holds the requested state and `flag == 0`; otherwise stores `state == 0 ? (enable ? 1 : 0) : 0`. |
| **AN-5** | *"Whether the flag can be 1 while `FUN_003BA2E0` is false — the setter cannot produce it, the second writer might."* **It cannot.** The final store is `enable ? 1 : 0`, exactly like the setter's. The only window is *inside* the call to `003BA2E0` itself, between the transient `1` and the final store — and that function reads only its two byte globals, never the flag. No consumer on this thread observes it. Cross-thread observability is not establishable statically and is carried as a new unknown. |

Also worth correcting gently in that document: its `00252C80` row says **"unread"**, and its
`00253B90` row says **"15 consumers"**. The second is right as a count of **call sites**; the
distinct-function count is **13** (7 direct + 6 through thunk `0030C0D0`), the difference being
that `BattleLocomotion_ComputeStepDistance` calls it more than once. Its own falsification pass
already says "8 direct E8 sites" — sites, not callers. Both numbers are correct and answer
different questions; the new document states which it means.

### New questions

| Proposed ID | Owner document | Question |
|---|---|---|
| `PROPOSED-repos2d-7` | r2-force-fight-toggle.md | **What the mode looks like on screen.** The output is identified; no player-facing description has been established from the binary or authored data. Left UNKNOWN deliberately — the FFXII-shaped candidates (minimap, fast-forward, stance) are exactly the suggestive-evidence trap. |
| `PROPOSED-repos2d-8` | r2-force-fight-toggle.md | What sound id `0x52` is — acquired by `00366870` while the toggle is `1`, released by `003667E0`. Needs the `sead` bank data. |
| `PROPOSED-repos2d-9` | r2-force-fight-toggle.md | What `022CB728` / `022CB726` are — the two refusal predicates `003603B0` / `003603C0`. |
| `PROPOSED-repos2d-10` | r2-force-fight-toggle.md | What `DAT_020927CC` is — a third override in the applier. |
| `PROPOSED-repos2d-11` | force-fight-mode.md (AN-5 remainder) | Whether the one-instruction window where `01E0C2B8` is `1` with the enable false is observable from another thread. |

## AUDIT-LOG

**repos-2d, 2026-09-02 — C-12 remainder.**

**Method note worth keeping: I followed the output, not the input.** The naming question was "what
is this toggle?", and the tempting route was to reason from R2 to a plausible FFXII feature. The
route that worked was the opposite — chase the value into `FUN_00252C80`, find it writing a global
the database had already named from the game's own script vocabulary, and let the name come back up
the chain. **The button was the last thing identified, not the first.**

**One claim was checked before publication and survived.** The whole R2 finding rests on `00197710`
being `GetBinding(mgr, profile, group, slot)`. Rather than take the keymap document's signature on
trust, its complete 99-byte body was re-derived: `r8b` selects one of three tables at `+0x00` /
`+0x40` / `+0x60` off base `01F80F90`, `dl` scales by `0x1C` dwords, `r9b` indexes. That matches
the document's independently derived signature and its worked example `GetBinding(0, 2, 0)` =
`Speed1`. Had it not matched, "slot 9 = R2" would have been wrong and everything above it with it.

**Four body sizes were wrong in my first draft** — `00198790` (8 B, not 20), `0079E6A0` (44 B, not
91), `00266D10` (1,185 B, not 3,349), `0050C910` (23 B, not 47) — caught by checking each row
against `functions.tsv` before publishing rather than by BODY DRIFT afterwards. Two of those also
have real ledger names I was not using: `InputManager_GetSingleton` and
`InputBackend_IsControlCode28To283ActiveForBank`. The second is informative on its own — it
confirms the call is a control-code active test.

**Hub import is much larger for a document that cites hubs deliberately.** This one drew **9**
first-pass findings from four cited hubs. Dispositioning them meant enumerating `00253B90`'s
13-function census inline, because `force-fight-mode.md` gives the count and the method but not the
enumeration — pointing at it would have been a deferral, which the standard distinguishes from a
disposition. The field-record predicate *could* be deferred, because that census really is written
down.

## CALL-CHAINS / ADDRESS-INDEX

| Address | Working name | Doc |
|---|---|---|
| `0017DE10` | `R2_IsActive` | r2-force-fight-toggle.md |
| `00252B60` | `ForceFightToggle_ApplyWithCapabilityGates` | " |
| `00252C80` | `ForceFightMode_SecondWriter` — **closes AN-2** | " |
| `003BA300` / `003BA310` | force-fight enable-byte setters | " |
| `0035C6F0` / `0035C880` | UI mode-register read / masked write (`022C83EC`) | " |
| `00366870` / `003667E0` | repeating-sound acquire / release | " |

```
R2 held (binding group 0 slot 9)
  -> 00253C70  InputGameplay_ArbitrateDigitalInputAndModalState        [Input OWNER]
     -> 0017DE10 -> 00197710 GetBinding(0,0,9)
     -> 00377C20 FieldData_GetActiveFieldRecordBit15  (direct AND via thunk 00313F60)
     -> 00252B60 -> 002E0FA0 capability policy bits 6/9/10
                 -> 00366870 | 003667E0  sound id 0x52
                 -> 00252C80 -> 01E0C2B8 force fight mode              [OWNER transition]
                                -> 003BA2E0 enable (02B4053C / 02B4053D)
                                -> 13 distinct readers, 15 call sites (Movement 5, CombatAction 2, ...)
```

---

# Follow-up block: the 20 pre-existing `15-Input` crossref findings

**20 → 0 across all five documents in the category.** Two independent runs agree, per the inbox
README's new rule that a single gate result is not evidence. `check_links` green (all relative
links resolve), `check_names` 0 TRUNCATED, `verify_doc_addresses` reports **ok** for all five.

Three documents carried findings — the "5 documents" in the audit line is the scan count, not the
finding count. `binding-profiles-remapping-and-control-state.md` had none.

## What the findings actually were

**Eight of the twenty were one substrate citation.** `input-stack-device-channel-and-bindings.md`
cites `0016D6A0`, which is `_guard_check_icall` — the CFG check stub, with **2,479 distinct callers
across 16 owner subsystems**, because every indirect call in the image passes through it. The
Audio (135 edges), Application, Combat Action, Developer, Items, Movement and Rewards findings, and
most of the Actor/Entity and World ones, are all callers of that stub. **None is an input
relationship**; enumerating them would say only that the executable uses CFG.

**One was a real presentation defect and is fixed.** `keymap-…-default-controls.md` cited
`01DF1470` in its *data* table with the size written as a bare `16 B`, in the same column position
the function table uses for a body extent — so the checker read it as "this is a function with a
16-byte body", which is the false claim the template warns a data row must not make. The document's
content was right; every sibling row in the same table already writes the shape first
(`` `u32[35]`, 140 B ``, `3 × 0x40 B`). The row now matches its own table's convention.

**Two were worth explaining rather than dismissing:**

- **Save/Load/Settings is a second writer of the capability policy table.** `capability-inhibition-policy.md`
  §2 says "different engine subsystems own different rows" and then documents only row 2.
  `SaveStorageQueue_ControllerStateHandler` (`005823B0`) and `SaveLoad_ControllerLifecycleHandler`
  (`00582860`) call **both** primitives — `002E1C20` to set and `002E1CA0` to clear. Two handlers
  named for controller state and controller lifecycle, which is exactly what a save system needs a
  capability row for: a controller disconnect or a save in progress must inhibit player operations.
  **Which row and bit is not established.** A backward register-liveness census over all 72 call
  sites of the two primitives returns **14 CONST, 24 DYNAMIC, 34 UNKNOWN** for the row argument;
  all four Save/Load sites land in the DYNAMIC/UNKNOWN buckets, one computing the row as
  `add rax, rcx`. The instrument abstains rather than guessing — filed as `PROPOSED-repos2d-12`.
- **Party reads the raw analog input history.** `0035EEB0` `InputControl_GetHistoryAnalogByteByIndex`
  ← `003594E0` (Party), with `PartyControl_ComputeAnalogMovementScale` doing the same job on the
  other side. So the input stack's history buffer is not consumed only by Input, and a change to
  its format would surface as a movement bug rather than an input one.

**The rest were large host functions cited for one edge each** — `0022A770` (core runtime
scheduling, 2,001 B) accounting for 11 Presentation edges plus Audio, Resource and Steam;
`002778C0` `BattleMenu_UpdateCommandSelectionAndDispatch` (UI, 9,374 B) accounting for Audio and
two Combat Action edges; `0022A0B0` (978 B) for its Actor/Entity and World callees. Each is
dispositioned as irrelevant **with the reason stated**, not waved away.

## Three things you will want

**1. The checker's alias table has a third mismatch, and this one is not the derived-form fix.**
`PlatformOnlineAchievements` is the ledger's owner string; the curated alias key is
`"Platform/Online/Achievements"`. `doc_accounts_for` normalises both by replacing `/` and space
with `_`, giving `platformonlineachievements` from the ledger and `platform_online_achievements`
from the curated key — **they do not match**, so the curated aliases (`platform`, `achievements`)
never apply and the fallback accepts only the concatenated spelling. A document that writes
"Platform/Online/Achievements" in prose is still reported as ignoring it. That is what happened to
my first disposition pass, and it is the same family as the two you already fixed.

**2. `crossref_clean` had drifted in both directions, and nothing machine-checks it.** Before this
pass: `capability-inhibition-policy.md` claimed **true** while carrying 3 findings, and
`input-stack-device-channel-and-bindings.md` claimed **true** while carrying 10.
`binding-profiles-remapping-and-control-state.md` claimed **false** with 0. All four are now set to
what the checker actually reports. This is the rule the evidence standard states for COVERAGE —
*a hand-maintained summary of machine-checkable facts must be machine-checked* — applied to a field
that has no checker. `check_coverage.py` verifies document counts; nothing verifies this flag, and
it is the flag the AUDITED bar depends on.

**3. My own first disposition pass created two new findings**, which is the hub rule biting the
person invoking it. Citing `ActorHandle_ResolveRegistryEntryByPackedId` by address in a one-line
aside imported its census — **180 callers across 11 owners**, larger than any of the three hubs
`cross-subsystem-accessor-hubs.md` enumerates. I removed the hex and kept the name: the claim did
not need the address, and the address would have needed a census. That reasoning is written into the
disposition so the next reader sees why the name appears without a citation.

## Not mine, flagged not touched

`verify_doc_addresses --all` reports one **`unwind-BANNED`** citation, in
`99-Unresolved-Residual/the-unresolved-158.md`. The document is marked `ok` and is *about* the
residual — where, as the evidence standard records, 366 of 382 incoming data references are banned
EH metadata — so citing one as an example is plausibly deliberate. Worth its owner's glance; I have
not touched it and am not claiming a defect.

## New question

| Proposed ID | Owner document | Question |
|---|---|---|
| `PROPOSED-repos2d-12` | capability-inhibition-policy.md | Which policy row and bit the two Save/Load controller handlers set and clear. Block-local liveness cannot recover them (one site computes the row as `add rax, rcx`); it needs either a data-flow pass or the handlers read properly. |

## Files changed

| File | Change |
|---|---|
| `15-Input/Input-Stack/input-stack-device-channel-and-bindings.md` | added a disposition section (10 findings) |
| `15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md` | added a disposition section (3 findings), including the Save/Load second-writer finding |
| `15-Input/Binding-Profiles/keymap-ini-file-format-and-default-controls.md` | added a disposition section (7 findings); reformatted the `01DF1470` data row; `crossref_clean` false → true |
| `15-Input/Binding-Profiles/binding-profiles-remapping-and-control-state.md` | `crossref_clean` false → true (0 findings, no other change) |

Every added section is headed and dated as an audit disposition by `repos-2d`, so each document's
owner can see exactly what was added and by whom. **No existing claim in any of the four was
altered** — the only edit to existing text is the `01DF1470` size cell.

---

# Follow-up block: PROPOSED-repos2d-12, and a correction to my own C-9 evidence

## CORRECTION FIRST — my census tool produced two confident wrong values, and C-9 cited them

**`argscan.py` determined which registers an instruction writes from capstone's `regs_access()`.
For `lea` that is inverted:**

```
lea edx, [rdi + 0x15]     ->   capstone: written = ['rdi'],  read = ['edx']
```

Destination and base swapped. A backward liveness walk therefore stepped straight **past** every
`lea` write and reported whatever earlier instruction it found — as a **CONST**, not an abstention.
The failure mode is the worst kind: a confident wrong value, not a missing one.

**What it corrupted.** `field-record-table-navimapdata.md` §8 published *"4 CONST (all 0) and 13
UNKNOWN — no other constant status id is passed anywhere in the executable."* Two of those four
were false: the real arguments are `lea r8d, [rdx - 0x51]` and `lea r8d, [rdx - 0x71]`.

**Corrected census** (tool fixed to derive `lea` destinations from operands, never from
`regs_access()`; every constant then re-read from the encoding by hand):

| | first run | corrected |
|---|---|---|
| CONST | 4 (all `0`) | **6** — ids `0`, `0`, `4`, `5`, `24`, `31` |
| DYNAMIC | 0 | 9 |
| UNKNOWN | 13 | 2 |

| Site | Encoding | Id | Caller |
|---|---|---:|---|
| `0030077A` / `003007CF` | `xor r8d, r8d` | 0 | `BattleStats_ModifyHPAndProcessLethalState` |
| `0030EB8D` | `mov r8b, 4` | 4 | `BattleSpecialSequence_CommitAccumulatedTargetHp` |
| `0030EBB7` | `mov r8b, 5` | 5 | same |
| `00304A76` | `mov r8b, 0x18` | 24 | `BattleUnit_AdvanceStandardActionState` |
| `0023437E` | `mov r8b, 0x1F` | 31 | `BattleSystem_InitializeAreaState`, through the **remove** wrapper |

**The correction strengthens C-9.** Four of the six ids now carry a native behavioural check
against the help text used to name them, and all four agree:

- **4 = Sleep**, **5 = Confuse** — both cleared where a special sequence commits accumulated damage.
  Damage waking a sleeping or confused unit.
- **24 = Invisible** — touched as a standard action advances. Acting breaking invisibility.
- **31 = Vanished** — *removed* when an area initialises. Clearing an irreversible removal state at
  area load, which is the only sane time to clear it.

None was sought; each fell out of the corrected census, and the naming in §2d predates all of them.

**What died:** "status 0 is the only status id any native call site passes as a constant."
**What survived:** no native site *adds* status 1 or 31 by constant — which is the claim §2d rests
on. Status 1 has no native constant site at all; the single constant use of 31 is a removal.

**Bonus, now proven rather than repeated.** The two mis-read sites are the authored direct-command
bridge: `BattleUnit_ExecuteDirectStateCommandOrder` computes `statusId = command - 0x51` on the add
path and `command - 0x71` on the remove path. The GFZ comment asserted a `0x4051..0x4070` /
`0x4071..0x4090` command family; that arithmetic is now read from the binary.

The document's §8 carries the full correction trail with the cause.

## PROPOSED-repos2d-12 answered: Save/Load owns row 1, bit 21

All four Save/Load call sites write **row 1, bit 21** — two set, two clear:

| Site | Encoding | Row | Bit |
|---|---|---:|---:|
| `005823F8` (clear) / `0058252C` (set) | `xor edi,edi` … `lea edx,[rdi+0x15]` / `lea ecx,[rdi+1]` | 1 | 21 |
| `005828B4` (set) / `00582F1B` (clear) | `mov edx,0x15` / `lea ecx,[rdx-0x14]` | 1 | 21 |

The second handler computes the row *from* the bit (`row = bit - 20`); the first passes both as
offsets from a zeroed register. Different idioms, same pair.

**Confirmed independently from the consumer side.** `00229AF0` (Audio) reads the aggregate, tests
bit 21, and on that path calls `002E1020(1)` — a 14-byte per-row reader over the same table at
`0215F1C0`. **A consumer that sees bit 21 goes on to read row 1.** Writer and consumer agree on the
row and can fail independently.

What the bit *does* is not established: bit 21 has no entry in the `01E0C2C0` UI-request
projection, so it is consumed directly rather than by refusing a UI request. The two handlers are
named for controller state and controller lifecycle, which is consistent with an inhibition raised
while a save is in progress or a controller is lost — but the document does not claim behaviour
from names. Carried as `PROPOSED-repos2d-13`.

## New questions

| Proposed ID | Owner document | Question |
|---|---|---|
| `PROPOSED-repos2d-13` | capability-inhibition-policy.md | What policy row 1 bit 21 actually inhibits. No UI-request projection; consumed directly by `00229AF0` (Audio) and `00228380` (called only by the Input arbiter). |

## AUDIT-LOG

**repos-2d, 2026-09-03 — an instrument of mine produced confident wrong values, and a published
document cited them.**

The rule this database already has is *verify the attack instrument before believing its result*.
This is the same rule for a **measuring** instrument, and the tell was available and I did not look
for it: a liveness walk that reports **CONST** should be able to name the instruction it stopped
on, and I printed that field (`at`) without ever checking that the instruction it named actually
wrote the register. It did not — it named an earlier `xor` that the walk should never have reached.

**What caught it was a disagreement, not a review.** The Save/Load census printed
`CONST 0` for a site whose disassembly, read for a different purpose, plainly showed
`lea edx, [rdi + 0x15]`. Two readings of the same site, one from a tool and one from the bytes.

**Two corollaries worth keeping:**

1. **A discriminator with an abstention bucket can still lie** — the abstention protects against
   *unknown*, not against *wrong*. Six of my seventeen verdicts were UNKNOWN and that felt like
   honesty; two of the four confident ones were false.
2. **`regs_access()` is a claim about an instruction, not the instruction.** Same shape as the
   database's rule that a decompiler's symbol is a claim about the bytes. Anything in this toolkit
   that walks registers should derive `lea` destinations from operands.

`Tools/work/repos-2d/argscan.py` is fixed and carries the defect in its docstring so the next
reader of that file sees why the code looks the way it does.

---

# Follow-up block: the 21 `03-World-Area-Field` crossref findings

**21 → 0 across all eight documents.** Two runs agree. `check_links` 176 files / 1,031 links all
resolve; `verify_doc_addresses --all` clean across 95 documents, no GHOST, no BODY DRIFT.

Unlike `15-Input`, **none of these was substrate** — the fix for that landed first and the count
was stable at 21 before I started.

## A name recovered from the game's own vocabulary

The README's two Script VM findings are not neighbours to dismiss. `002E3D40`, which the README
lists as *"field runtime parameter derivation (zero-mode path)"*, has exactly two Script VM
callers, and they are **authored verbs that name it**:

| Call id | Verb | Args | Handler | Arity check |
|---|---|---:|---|---|
| `0x0481` | **`setmapwind`** | 3 | `0034B6C0` | **3** `VMValueStack_PopInt32CoerceFloat32` calls, then `jmp 002E3D40` with `mode = 1` |
| `0x0482` | **`defaultmapwind`** | 0 | `0034BD10` | **0** pops; zeroes all four arguments and `jmp 002E3D40` |

So `002E3D40(mode, a, b, c)` is the engine's **map wind** entry point: mode 1 with three script
arguments sets it, mode 0 resets it to the field default. **That is what the README's "zero-mode
path" is** — the default-wind call, which the weather apply path tail-enters when a field's
environment is materialised.

Both bindings are arity-verified against the dispatch catalog, which is the bar the Script VM
category requires before a verb binding counts as fact. The name comes from authored script
vocabulary, not from a reading of the body — the same route that named `setforcefightmode`.

## The RNG finding was the documentation being right in the wrong words

Five findings named `RNG_Random_Selection`, from `RNG_MT19937_NextU32_Thunk`. The Weather
transition roll is not an unaccounted relationship — it is the subject of
`weather-probability-and-transition-roll.md`, which names **MT19937 thirteen times**.

The audit could not see it because **those documents never write the word "random"**; they use the
engine's algorithm name. The alias list for that owner is `random` / `selection`, and:

> the one Weather document containing the word "selection" — `weather-slot-state-model.md`, once,
> in an unrelated sentence — is the one Weather document with **no** RNG finding.

That is a natural experiment, not a theory. `MT19937` and `RNG` belong in that owner's aliases.

## A fifth alias case, and this one is structural

The two `SaveLoad` findings are not the `Save_Load_Settings` vocabulary problem. `00280140` has
**no `PrimaryOwner`**, so `subsystem_of` falls back to its `CodeDomain` family head — and the
CodeDomain taxonomy spells it **`SaveLoad`** where the owner taxonomy spells it
`Save_Load_Settings`. The ledger contains only the latter (87 functions); the former exists only as
a domain path.

**The checker can report a subsystem under either taxonomy, but its alias table only knows one of
them.** This is not one bad row — it will recur for every unowned neighbour whose CodeDomain family
head differs in spelling from its PrimaryOwner counterpart.

## The census-once pattern, with its own counter-example

Six documents describe one system from different angles and therefore cite the same field-frame
neighbourhood. The standard's rule is to state a census once and defer to it, never to duplicate
it across six files. So:

- `weather-apply-and-environment-materialization.md` carries the full census — the image-address
  resolver's **815 callers across 18 owners**, the field-frame routines and their Audio/Party
  callees, the field-id accessor deferred by reference to the hub document that does enumerate it,
  and the Save/Load persistence path.
- The other five documents carry a short disposition naming the subsystems and pointing at it.

**And the counter-example is in the same pass.** `mweather-resource-format.md`'s disposition
referenced the image-address resolver **by address** — 815 callers — and the category went from
**5 findings to 10**, pulling in Actor/Entity, Audio, Combat AI and Combat Action. Removing the hex
and keeping the name took it to **0**. The enumerating document is protected by its own census;
the referencing document must not re-cite the address.

## AUDIT-LOG

**repos-2d, 2026-09-03 — 03-World-Area-Field disposition pass.**

**I made the same mistake twice inside one pass, and the second time was in the paragraph warning
against it.** The first mweather disposition was shared boilerplate that named the field-id
accessor; that document had never cited it, and naming it drew three Movement and five UI findings
that did not exist before. I replaced it with text that cited the image-address resolver by
address — 815 callers — and doubled the category's finding count. Both fixes were the same:
**name the function, do not cite the hex.**

The rule is one this database already has — *citing a hub imports its whole neighbourhood* — but
the corollary is worth stating separately because it is what I kept getting wrong:

> **A reference to a census someone else holds is not a citation. Write the name, not the address —
> the address is a commitment to account for everything it drags in.**

Boilerplate is the specific hazard: shared disposition text makes the *same* commitments in every
document it is pasted into, including documents that never made them.

## New question

| Proposed ID | Owner document | Question |
|---|---|---|
| `PROPOSED-repos2d-14` | 03-World-Area-Field/README.md | What `setmapwind`'s three arguments are. The handler pops three ints and passes them as `(mode=1, a, b, c)` to the map-wind entry point; MWeather's own packed record carries an azimuth sector and an elevation class, so the shapes are suggestive and unproven. |

## Files changed

| File | Change |
|---|---|
| `Weather/weather-apply-and-environment-materialization.md` | full field-frame census + Save/Load taxonomy note |
| `Weather/weather-probability-and-transition-roll.md` | disposition by reference |
| `Weather/weather-slot-state-model.md` | disposition by reference + Save/Load taxonomy note |
| `Weather/mweather-resource-format.md` | own disposition (runtime infrastructure), no hub citation |
| `Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md` | disposition by reference |
| `README.md` | Script VM disposition **and** the `setmapwind` / `defaultmapwind` naming |

No existing claim in any of the six was altered; every section is headed and dated as an audit
disposition by `repos-2d`.

---

# Follow-up block: PROPOSED-repos2d-14 — `setmapwind`'s three arguments

## Answer

```
setmapwind(elevation, azimuth, preset)
```

**The order is the reverse of the one the field layout suggests**, which is why this needed
deriving rather than assuming. `mweather-resource-format.md` §4 lists the packed fields as preset
(offset 0), azimuth (offset 3), elevation (offset 7); a reader carrying that order into the verb
would write `setmapwind(preset, azimuth, elevation)` and be exactly backwards.

## How it was settled

`002E3D40(mode, A, B, C)` is a **two-source multiplexer** in front of the Presentation backend
init. It loads `ebp = A, esi = B, eax = C`, and **when `mode == 0` it overwrites all three from the
three MWeather extractors** before tail-jumping to `0040AAD0(ecx = ebp, edx = esi, r8d = eax)`:

| Handler pop | `002E3D40` param | Register | Reaches `0040AAD0` as | Mode 0 fills it from | Therefore |
|---|---|---|---|---|---|
| pop 1 = `paramType[0]` | `C` (`r9d`) | `eax` | 3rd (`r8d`) | `003777B0`, offset 7 width 2 | **elevation class** |
| pop 2 = `paramType[1]` | `B` (`r8d`) | `esi` | 2nd (`edx`) | `003777A0`, offset 3 width 4 | **azimuth sector** |
| pop 3 = `paramType[2]` | `A` (`edx`) | `ebp` | 1st (`ecx`) | `00377850`, offset 0 width 3 | **backend preset** |

**The mode-0 path is what makes this proof rather than inference.** The same three registers are
filled from the table in one mode and from the script in the other, feeding one consumer — so the
script arguments *are* the packed fields, and the register each travels in says which.

The pop-to-parameter direction is the convention already proved in the Script VM document's §4.4
(*"the catalog's `paramType[0]` is the first value the handler pops"*), established there against a
five-argument verb whose shape makes a wrong convention obvious. I did not re-derive it; I used it
and cited it.

## A caveat closed on the way

`mweather-resource-format.md` §9 records that only the first extractor's width survived
decompilation, and that *"the widths 4 and 2 are inferred from the offsets being 3 and 7 with a
9-bit total, not read directly."* They are readable: **each wrapper computes its offset from its
width**, so the encoding states both.

```asm
00377850   mov r9d, 3    xor r8d, r8d         ; width 3, offset 0        preset
003777A0   mov r9d, 4    lea r8d, [r9 - 1]    ; width 4, offset 4-1 = 3  azimuth
003777B0   mov r9d, 2    lea r8d, [r9 + 5]    ; width 2, offset 2+5 = 7  elevation
```

Widths **3, 4, 2**, offsets **0, 3, 7**, summing to the documented 9 bits. The earlier inference was
correct and is no longer an inference — a tier upgrade, not a correction.

## Modding consequence

`setmapwind` overrides all three fields for as long as the script leaves them set;
`defaultmapwind` restores them from the record for the **current** field and Weather Slot. A zone
script that sets wind and never resets it therefore keeps its override across a Weather Slot change
that would otherwise have re-read the table.

## AUDIT-LOG

**repos-2d, 2026-09-03 — PROPOSED-repos2d-14.**

**The suggestive shape was right about the fields and wrong about the order.** MWeather's record
carries an azimuth sector and an elevation class, and those really are two of the three arguments —
so a guess would have looked confirmed on inspection while being reversed. What separated them was
not more evidence about the fields but a different *kind* of evidence: the register each value
travels in, and a documented convention for which pop is which parameter.

**Method that worked, and is reusable:** when one function serves a value from two sources under a
mode flag, the mode that reads the *known* source labels the registers for the mode that reads the
unknown one. `002E3D40` mode 0 reads the documented table; mode 1 reads the script. Same registers,
same consumer.

**No new findings created.** Every hub in this chain was named rather than cited by address — the
field-id accessor, the Weather Slot getter — after the two boilerplate mistakes in the previous
block. `audit_crossrefs` on the category: **0**, unchanged from before this section was written.

## Files changed

| File | Change |
|---|---|
| `Weather/mweather-resource-format.md` | new § *The script interface: `setmapwind` and `defaultmapwind`*; §9's width caveat closed |
| `README.md` | one line pointing at the argument order |

---

# Follow-up block: falsification pass on `keymap-ini-file-format-and-default-controls.md`

**First pass on a 1,005-line document that had never been attacked.** `audit.passes` 0 → 1,
recorded against snapshot `46f02e26…`. **Status deliberately left `DOCUMENTED`, not `AUDITED`** —
see the closing note in §10.

**Disclosure, stated in the pass itself:** this session used the document twice as a *source* — the
binding lookup that identified R2, and its "the name's index is the slot's index" rule. One part
was verified at the time (`00197710`'s body); **the rest was accepted**. The pass attacks the
accepted parts first, which is the only reason it is worth anything.

## Survived

**"Name index == slot index" — the load-bearing claim, now proven rather than inferred.** §8 cited
the parser's paired increments. Re-reading the whole loop proves two things the increments alone do
not: the slot counter is **explicitly reset to zero per group** (`mov esi, 0` at `0019850A`), and
the loop-back target is the dispatch at `0x198486`, **not** the group-counter initialisation at
`0x19847C` — so `mov r15d, esi` runs exactly once, when `esi` is 0. Both pointers start at index 0
in every group and advance one entry per iteration.

**"Profiles 2 and 3 are range-checked by nothing"** — the document's most consequential defect
claim. `r11` is loaded once with `01F80F94`, the outer pass re-executes `mov rax, r11`, and `r11`
is never modified: three identical passes over profile 1. Survives. The pseudocode also collapses
two *different* encodings of the same bound (`(v-1) > 0x97` and `v <= 0 || v >= 0x99`); they are
equivalent, and collapsing them is correct.

**The uniqueness validator, instruction for instruction** — including the `test ecx, ecx` that
excludes 0 from duplicate detection, and the inner scan running to the end of the **whole** 84-dword
array, which is what makes §1's *"one key may only mean one thing across all three layouts"* true.

**Three absence claims**, on an instrument with a working control. The document records that a
linear `.text` sweep failed here, missing `01DF11E0` at `0019847F`; a per-function-entry sweep
resynchronises and **finds it**. With the control firing: `008F3160` has 0 references,
`01F80FF4/F8/FC` have 0, and `[Button]`/`[Setting]`/`[Mouse]` return 0 in ASCII and UTF-16 while
`[Keyboard` returns exactly the cited hit. `Keyboard1` as a whole literal also returns 0, which
independently corroborates that the writer *composes* the section header.

**The caller counts, now checked against the thunk route** — the defect that produced two wrong
answers elsewhere in this database. Positive control: `FieldData_GetActiveFieldRecordBit15`,
80 sites / 66 distinct, matching its own document. `GetBinding` has **0 thunks, 6 distinct
callers** (the document's "six callers" survives); the three `IsL2Held`/`IsR2Held`/`IsWalkModeKeyHeld`
predicates have exactly one caller each and no thunk route.

## Corrected

**`001E0BD0` "10 call sites" → 10 distinct callers, 15 call sites.** `002B5C90` calls it six times;
the other nine call it once. Both numbers are right about different populations and the document
stated the one it had not measured — the edge-count-versus-call-site rule, again.

**"The only reader that reaches group 2" is true only of binding getters.** As literally worded it
is false, and **the document's own §4 is the evidence**: the uniqueness validator reads all 84
dwords, group 2 included, and the writer reads them to emit them. The intended sense — the only
path by which a group-2 key reaches a consumer — is right, and is what §8's evidence actually
enumerates. Qualified in both places.

**Why that one was worth chasing rather than waving through:** group 2 is reached as
`01F80F90 + 0x60`, *not* by referencing `01F80FF0` — so a second group-2 reader would be invisible
to the very test §8 cites. What closes it is the base's own reference list: 8 sites across 6
functions, all Input, each accounted for. No seventh reader exists.

## Population note, recorded so nobody "fixes" it

§8 reports **7** references to `01F80FF0` from `DumpDataXrefs.java`; a rip-relative operand sweep
finds **5**. The difference is the computed accesses Ghidra resolves to the symbol — including
`MOV EAX,[RAX+RDX*4+0x60]`, which is not a reference to `01F80FF0` in the encoding at all. **Both
counts are correct for their instrument.**

## Why not `AUDITED`

Criteria 7-9 are met: pass recorded against a named state, `audit_crossrefs` clean, every
cross-subsystem neighbour dispositioned (done in the earlier `15-Input` block). **Criterion 10 is
not** — three areas are listed under *What was not attacked*, chiefly the tier-10 rows that rest on
the `keymap.ini` on this machine, which I did not re-read from disk. A second pass covering those
closes it. Claiming `AUDITED` with a non-empty not-attacked list would be the status equivalent of
softening a claim until the tool goes quiet.

## AUDIT-LOG

**repos-2d, 2026-09-03 — first falsification pass on the keymap document.**

**The pass found two defects and both were population errors, not reading errors** — a call-site
count that was a caller count, and a "only reader" that was "only binding getter". Neither changes
a mechanism; both change what a reader would conclude about scope. This document's *mechanics* are
unusually solid: every instruction-level claim I re-derived came back exact, including two the
author flagged as hard (the collapsed bound idioms, the parser's paired increments).

**The instrument note in §8 was worth its space.** The document records that a linear sweep
returned 0 for every global including one it could prove was referenced, and that the author
switched instruments rather than believing the zero. That note is what told me which instrument to
use for the absence claims, and my per-function-entry sweep found the reference the linear one
missed. **A recorded instrument failure is reusable; a silently corrected one is not.**

---

# Follow-up block: pass 2 closes the keymap document to `AUDITED`

**Band worked, as requested:** `00195xxx`-`00198xxx`, `0017Dxxx`-`0017Exxx`, `001DFA70`,
`001EDDC0`, `0022A4F0`, `00229Exxx`/`00239790`, `003594E0`; data `01DF09C0`/`01DF0Axx`/`01DF13E0`/
`01DF1470`/`01F45700`/`01F80Fxx`/`00908BA8`/`01DFE0Bx`; plus the on-disk `keymap.ini` and
`GameSetting.ini`. No overlap with the three bands you named.

**`status: DOCUMENTED` → `AUDITED`, `audit.passes` 1 → 2.** All three areas §10 listed as *not
attacked* were attacked. Nothing overturned.

## The file on disk — and an artefact nobody planted

There are **two** copies, and they are **byte-identical**:

```
…\FINAL FANTASY XII THE ZODIAC AGE\keymap.ini                    699 B
…\FINAL FANTASY XII THE ZODIAC AGE\76561198045890736\keymap.ini  699 B
```

§2 says the path carries a `<SteamID64>` component; §8 says *"the id component is empty when Steam
is not initialised."* **The two files are that tier-1 guard observed from disk** — the same build
wrote the same content down both paths. That corroboration was not sought and could not have been
constructed.

Everything else reproduces: 699 bytes, 87 lines, **zero** `0x0D` bytes, the exact opening bytes,
`Circle` as the 14th line of `[Keyboard1]`, and a three-way comparison of all **84** values (file vs
image tables vs §4's decoded table) with **0 mismatches**, zeros and profile 3's `Circle=1`/`Cross=3`
included. The `{kind, 4, codeA, codeB}` layout is confirmed from the records themselves.

**Testability caveat worth carrying:** this only works because the file here is unmodified. On a
machine where the player has rebound anything the claim becomes *untestable*, not false — someone
re-running it elsewhere should not report a defect.

## `PInputKeySemantic` — and a control that matters more than the result

Re-parsed rather than inherited: record is `{u64 value, u64 typeRef, u64 namePtr, u64 0}`,
**95 records, 123 down to 29, strictly descending by one**. All **28 of 28** shipped codes resolve
through `PInputKeySemantic - 1` with names matching §4 exactly.

**The control is the finding.** Resolving *without* the `-1` still hits **27 of 28** — a
coverage-based test cannot separate the hypotheses. What separates them is semantics:

| slot | code | `code + 1` | `code` |
|---|---:|---|---|
| `LX_N` | 28 | **`Key_A`** | *(nothing)* |
| `LX_P` | 31 | **`Key_D`** | `Key_C` |
| `LY_N` | 50 | **`Key_W`** | `Key_V` |
| `LY_P` | 46 | **`Key_S`** | `Key_R` |

One yields WASD; the other yields C, V, R and a hole. §4's worked check was the right
discriminator and is now shown to be the **only** one available.

## The chains, end to end

Speed table raw-reads `(1.0, 2.0, 4.0)`. `0017DEA0` reads `GetBinding(0, 2, 0/1/2)` and calls
`00239790` with `ecx` = **1, 2, 4**, all three paths testing and setting the one latch `01F7F4E9`.
`00239790`'s toggle-off comparisons are exact. `003594E0`'s walk toggle is exact — `sete al` on
`g_walk == 0`, guarded by latch `022C7FF9`, rising edge only.

Worth stating because two numbering schemes meet: the **argument** is 1/2/4, `g_speedMode` holds
**0/1/2** (the table index), which is why the comparisons read `1` and `2`.

Four more rows attacked in passing — the swap predicate `001DFA70` (exact), the confirm/cancel
`cmove` exchange in `0022A4F0` (exact), the reserved list (**exactly 35 dwords**), the frame-base
globals and **all three stores inside `001EDDC0`** on the `ecx != 0` branch — the claim carrying
**Z-10** and **K-8** elsewhere — and the path builder's three mkdir pairs plus the Steam id call.

## Second population note

§8's census gives `01DFE0B8` **46 reads / 1 write**; an operand sweep finds **46 sites total**
(45 reads + the `movss` write). The same sweep matches §8 **exactly** on the other two globals
(212 = 211+1, 183 = 182+1), so it is a **single-site instrument difference on one global**, not
systematic — and the load-bearing part is confirmed by reading the function. Same handling as the
`01F80FF0` note: two instruments, both correct for what they count, recorded so nobody reconciles
them by editing.

## Why `AUDITED` is honest here, with the residue named

§11 states coverage plainly. **Not** directly re-derived, and corroborated only through their
output: the parser's two grammar micro-claims, the writer's emission loop, and the publishers'
read/write sets. The 87-line file with its exact section order and 84 matching values *is* what
those three produce, so they are observed end to end — but none was read instruction by instruction
in either pass. Naming them is the difference between an audited document and a stamped one.

## AUDIT-LOG

**repos-2d, 2026-09-03 — second pass, keymap document closed.**

**The most valuable thing in this pass was a control, not a result.** The `PInputKeySemantic -1`
claim was already believed and already true; what the pass adds is that **the obvious way to check
it does not work** — 27 of 28 codes resolve under the wrong hypothesis too. Anyone re-verifying by
counting hits would have confirmed it for the wrong reason and been right by luck. The check that
works is reading four names and noticing they spell a movement layout.

**And the strongest corroboration of the pass was an accident of the filesystem** — two
byte-identical `keymap.ini` files, one with the Steam id component and one without, which is a
tier-1 branch condition left lying on disk. Nothing about the pass design produced it; it was
found by looking where the document said the file lives.

---

# Follow-up block: falsification pass on `what-the-engine-calls-to-make-a-sound.md`

**Band worked:** `00249Cxx`, `002DExxx`/`002DFxxx`, `003A11xx`, `00267330`, `007AD450`. No overlap
with `002D8xxx`/`0036xxxx`, `022D8xxx`, `0069Fxxx`/`0083xxxx`-`0085Exxx` — I cite the R2 document's
sound acquirer by **description** rather than address for exactly that reason.

`audit.passes` 0 → 1. **Status stays `PARTIAL`** — §7 carries three genuine unknowns.

**Disclosure:** this session cited this document's chain in the R2 toggle document, so this is an
audit of a document I have leaned on. **It corrected mine as well as this one.**

## Survived

**Every caller count, including against the thunk route** — the class that produced two wrong
answers earlier tonight. `00249C60` **99 callers, zero Audio-owned** (unowned 67, UI 29, Save/Load
3); `00249CA0` **6**; `002DF220` **9 total, 4 Audio** → the stated 5 external + 4 internal;
`002DEC00` **16 total, 4 Audio** → 12 external; `007AD450` **98, all Audio**. No thunks on any.
The external/internal split is applied consistently, which is what makes them reproducible.

**The resolver.** `shl edx, 9` then `add edx, ebx` — `bankSlot*512 + localIndex`, exact — with the
`-1` refusal and the world-live precondition both as described. And §2's claim that the wrapper
never writes `ECX` before the call, so the caller's index passes straight through, is visible in
the body.

**The gate is genuinely ahead of resolution**, so it suppresses the lookup and not just playback.

## Corrected — `0x7F` is not a literal at any call site

§2: *"The values are not derived from anything at the call site; **they are literals compiled in**."*

```asm
00249C77  mov  edx, 0x40          ; the pan IS an immediate
00249C7E  lea  r8d, [rdx + 0x3f]  ; the volume is COMPUTED: pan + 0x3F
```

`00249CA0` uses the same idiom, and so do four of the five other resolvable direct callers of
`002DF220`. **Not one call site in the image passes `0x7F` as an immediate.**

It matters because §6 offers this call site as an intervention point: **a modder searching for a
`0x7F` immediate near the play call will not find one**, and patching the pan silently moves the
volume with it, because the volume is derived from the pan register.

## Refined — the constants are the wrappers' convention, not the play call's signature

The fifth direct caller, `00357040` (Script VM / native bridge), passes `mov r8d, r15d` — a
**variable** volume. §2's claim is correctly scoped to the wrappers, but §6 warns only that not
every sound passes through `002DF220`; the sharper point is that **even the sounds that do do not
all carry the same volume.**

## Population note — 206 measured against a stated 211

§2 quotes the companion: *"66 of the 211 call sites load that index as an immediate in `0x0A`-`0x6C`."*
Measured over the stated population `00249C60` (192 sites) + `00249CA0` (14) = **206**: 157 CONST,
47 DYNAMIC, 2 UNKNOWN, **63** in range. Differences of 5 and 3.

My instrument counts direct `call`/`jmp` immediates inside bodies bounded by the next function
entry — blind to indirect calls, and able to truncate a body that overruns. **Not comparable
without the companion's definition of the 211**, so recorded rather than reconciled. The shape of
the finding is unaffected.

## The pass corrected the auditor's document

`003A1180` has 8 callers and one is the R2 toggle's repeating-sound acquirer, which my document
described as acquiring *"sound id `0x52`"*. **It is a bank-local index, not an id** — the resolver
returns `bankSlot*512 + index`. `PROPOSED-repos2d-8` understated the work: identifying the sound
needs the **runtime bank slot** as well as the `sead` data. Corrected at three sites in
`r2-force-fight-toggle.md`, with the reason and the source of the correction recorded.

**Second time an audit of a neighbour has corrected my own work** — the first was the stale
cross-reference in the keymap document. Both were found by auditing outward, neither by re-reading
my own text.

## AUDIT-LOG

**repos-2d, 2026-09-03 — audio boundary pass.**

**I imported two large gameplay neighbourhoods into an audio document while writing the pass, for a
third time, and caught it on the gate.** The paragraph naming four callers of `002DF220` was
*illustrative* — the census point stands without any of them — and citing `003112F0` (2,040 B) and
`0030C650` pulled Combat Formula and Combat Action edges into 18-Audio. Rewritten to name them by
owner; findings on that document dropped from 14 to 5 across the folder.

> **An illustration is not worth a citation.** A citation commits the document to accounting for
> everything the address drags in; an example that could be replaced by a count never earns that.

**And the one citation I kept, I kept on purpose and dispositioned:** `00267330`, the world-live
precondition, because the *"refused unless the world runtime is live"* claim cannot be checked
without it.

**Scope honesty:** this document was `crossref_clean: false` before the pass and still is. Its own
§2/§4/§7 citations carry unaccounted **Movement**, **Platform**, **Party** and **Resource**
neighbours. Dispositioning those is a separate job and I did not do it — it is available as a
follow-up, and the pass says so in the document rather than leaving the state ambiguous.

---

# Follow-up block: the surviving cross-document finding, resolved

**Band worked:** `00312730` and the image-wide `[X+0x698]` / `[reg+5]` census. No writes outside
the one corrected line in `06-Movement-And-Navigation/Battle-Locomotion/`.

## The verdict: the claim is true, the citation could not support it, and it now carries its own evidence

`battle-locomotion-steering-and-recovery.md` §8 asserted *"`BattleLocomotion_DecodeOrderGoal` is one
of the 82 functions testing that byte"* and cited `battle-record-kind-byte.md`.

**True of the binary.** Hand-read at `003127E7`:

```asm
003127D7  mov  rax, qword ptr [rdi + 0x698]   ; the record view
003127DE  test rax, rax
003127E1  je   0x312ad4                       ; null -> bail
003127E7  cmp  byte ptr [rax + 5], 1          ; the kind byte, against 1
003127EB  jne  0x312ad4
```

The load is three instructions before the compare, same basic block, no intervening write — the
tightest possible form of the cited document's own criterion.

**And the checker was right anyway.** The target states a **cardinality** ("104 sites across 82
functions") and never enumerates its members, so it cannot support a **membership** claim about any
particular function. The claim needed the site, not the count. Corrected in place, with the reason
and the route recorded.

## Bonus: the target's census independently reproduced

I rebuilt the census from the target's own stated criterion — every `cmp`/`test` against `record[5]`
where the register was loaded from `[X + 0x698]` and **still live** at the compare:

| | sites | functions | subsystems |
|---|---:|---:|---:|
| `battle-record-kind-byte.md` states | 104 | **82** | **11** |
| independent rebuild, strict | 107 | **82** | **11** |
| same rebuild, loose filter | 115 | 85 | 11 |

**The function count and the subsystem count reproduce exactly**, from an instrument built from the
prose rather than from their code. The 3-site difference is on the finer figure and is consistent
with my linear scan not modelling branches. The loose row is included because it shows what the
filter is worth: the document's point that the filter is load-bearing is correct, and an unfiltered
`[reg+5]` scan gives 258 sites across 187 functions.

**Two things for the coordinator to place**, both in `04-Actor-Entity`, which I was not assigned:

1. That corroboration is worth recording in the target — an independent rebuild agreeing exactly on
   82 / 11 is stronger evidence than the original census alone.
2. **The structural gap the checker actually found.** The target gives a count and never enumerates,
   so **no membership claim can ever cite it**. Either it should carry the member list (82 rows), or
   documents naming a member must cite the site as this one now does. That is a real documentation
   gap and it will recur.

## A second capstone defect, same class as the first

While rebuilding the census my strict filter returned **0 sites** — including for the site I had
just read by hand. The cause:

```
test rax, rax             ->  capstone regs_access(): written = ['rax']
cmp  byte [rax + 5], 1    ->  capstone regs_access(): written = ['rax']
```

**`cmp` and `test` are reported as writing their read operands.** In a liveness walk that kills the
register at the very instruction that guards the load, so the compare is never attributed.

This is the second instance of the defect I logged this morning (`lea` reporting destination and
base inverted). `written_regs` now special-cases both, and the comment in the file says why.

**I re-ran the published C-9 status-id census against the fixed helper: unchanged — 6 CONST, 9
DYNAMIC, 2 UNKNOWN, histogram `0×2, 4, 5, 24, 31`.** The defect could only convert CONST into
DYNAMIC, never the reverse, and no `cmp`/`test` on the argument register happened to sit between a
write and a call in those 17 sites. **Verified rather than assumed**, because that census is
published and I had already corrected it once.

## AUDIT-LOG

**repos-2d, 2026-09-03 — the surviving cross-document claim.**

**I hit my own documented instrument defect again, because I wrote fresh code instead of reusing
the fixed helper.** The evidence standard already carries *"reuse the tool"* — I had a corrected
`written_regs` sitting in the same directory and wrote a raw `regs_access()` loop anyway, then spent
two runs debugging a zero that my own docstring predicted.

And the sharper half:

> **Fixing one instance of an instrument defect is not fixing the class.** `lea` was patched this
> morning with a comment explaining the inversion. The same function's `cmp`/`test` behaviour was
> left on the default path, and it was wrong in exactly the same way. A defect found in one opcode
> is a reason to audit the instrument's model of *every* opcode it special-cases nothing for.

**What the zero did right:** it was a *loud* wrong answer — 0 sites including a site I had already
read by hand — rather than a plausible one. A quiet 104 would have been indistinguishable from
success.

---

# Follow-up block: first pass on `the-282-command-parameter-console.md`

**Band worked:** `001D1660`-`001D4C19` (the console body, its arms and the table at `001D4C1C`),
`008F30E8` / `009002BC` / `009002F4` / `01CEBBA8` / `01CEBC9C` in the float pool, and
`Tools/work/repos-d2/console_arms.tsv` **read-only** — I rebuilt my own extraction rather than
touching another session's.

`audit.passes` 0 → 1. Status stays `PARTIAL`. The document honestly declares
`crossref_clean: false` and has 6 findings; dispositioning those is a separate job and I did not
do it.

## Verdict for the slice hold: CONFIRMED — release it, with a changed row shape

`repos-d2`'s resolution is **independently confirmed** and my pass adds the piece their method
could not reach.

**Confirmed, instruction for instruction.** They report `addss +0.01` x58, `subss +0.01` x30,
`addss -0.01` x28 from a constant census over the function body. Walking the dispatch table and
attributing to arms, I measure **the same three cells exactly** — 58 / 30 / 28. Two instruments
that share no code and no method: theirs counts constant references, mine walks 282 table entries
into 227 arms.

**And the sign composes, as they state:** negative if the mnemonic is `subss` **or** the constant is
itself negative. My original hypothesis — sign from the operation, value from `.rdata` — was half
right in the way that matters: the two sources **compose**, neither overrides.

**What their census could not reach, and this pass supplies:** 58/58 is **58 ARMS**, not 58
raise-commands and 58 lower-commands.

```
step magnitude 0.01 -> 58 arms      0.03 -> 3 arms
               0.02 -> 11 arms      1.0  -> 2 arms
               0.05 -> 10 arms      0.005556 -> 1 arm
               0.1  -> 9 arms       0.5  -> 1 arm
               0.001 -> 7 arms      TOTAL 102 arms
```

Each arm carries the step **and its inverse**. A constant census cannot distinguish "58 arms that
each go both ways" from "58 up and 58 down"; only the table walk can. This is the per-arm
attribution the hold was waiting on.

**The magnitude is the property of the arm. The sign is not.** Which is exactly the row shape the
work order has already moved to.

## The extraction defect, for the record

`console_arms.tsv`'s step column is wrong about **direction, for all 102 stepping arms, in the same
direction**.

The cause is exact. **Every stepping arm contains both a `subss` and an `addss` against the same
constant**, and the extractor records one step per arm, taking the first — which is always the
`subss`. Its counts are precisely the negative half of the true distribution:

```
TSV   : -0.01 x58, -0.02 x11, -0.05 x10, -0.1 x9, -0.001 x7, -0.03 x3, ... and NO positives
actual: +/-0.01 x58 each, +/-0.02 x11 each, +/-0.05 x10 each, +/-0.1 x9 each,
        +/-0.001 x7 each, +/-0.03 x3 each, +/-1.0 x2 each, +/-0.005556, +/-0.5
        102 POSITIVE, 102 NEGATIVE — exactly symmetric
```

The values are real and the arms are correctly identified. **A slice reading that column will
describe every tunable parameter as decrement-only.**

## The finding behind the defect: every stepping arm is bidirectional

```asm
001D1FB0  movss xmm0, [02CB8140]      ; the parameter
001D1FB8  test  bl, bl                ; <- a direction flag, in a register
001D1FBA  je    0x1d1fd1
001D1FBC  subss xmm0, [008F30E8]      ; 0.05  -> decrement
001D1FC4  movss [02CB8140], xmm0
001D1FCC  jmp   0x1d4bfa
001D1FD1  addss xmm0, [008F30E8]      ; the SAME 0.05 -> increment
001D1FD9  movss [02CB8140], xmm0
```

**102 of 102** have this shape — a `test` on a register flag, then both branches. Not one arm steps
in a single direction.

So the console is **one command id per tunable parameter, with direction supplied as a second
input**. §1 said *"each one adds or subtracts a fixed step"*, which a reader takes as separate
raise/lower commands. It is now corrected in §1 and §2 — and the corrected reading fits §1's own
"hold a button and watch the value creep" better than the original did: **holding it the other way
walks the value back.**

## Corrected — `001D4BFA` is the shared epilogue

§2 introduces it as the do-nothing arm that 56 ids point at. The 56 is right, but **212 of the 226
real arms jump to it when they finish**. It is the function's common tail; a reader told only that
it is the no-op target will misread 212 jumps as 212 commands doing nothing.

## Reconciled — 102 against the TSV's 110, with complementary blind spots

My set is a strict **subset**: 102 in both, **0** found by me and not by the TSV. The 8 remaining
`nudge` arms are real and my rule could not see them:

- `001D1867` picks the sign by loading `+1.0` or `-1.0` **into the register**, then does one
  `addss` against the *parameter* — step in the register, parameter in memory, the reverse of the
  common shape. A rip-relative-constant rule is structurally blind to it.
- `001D3CBD` **computes** its step: an int divided by 5 through the magic-number sequence,
  converted to float, scaled by `0.002`. A scaled step, arguably a third category.

**Each extractor is blind to what the other catches**; together they account for all 110. That is
worth more than either count alone.

## Population note

§2's ranked constant list (`0.01 x88`, `-0.01 x28`) counts **references to `.rdata` floats**; my
table counts **steps applied**. Different populations — one arm references its constant twice, once
per branch. The `-0.01` pool entry being referenced 28 times is consistent with the `001D1867`
shape (sign in the constant), not with 28 decrement-only commands.

## Reproduced exactly

282 table entries, 227 distinct targets, 56 ids at `001D4BFA`, all targets inside the body. The
document's structural counts are sound.

## New open item

What supplies the direction flag. The register differs between arms (`bl`, `sil`), so it is an
argument to the console rather than a global; this pass did not trace the caller.

## AUDIT-LOG

**repos-2d, 2026-09-03 — first pass on a document I did not write, chosen for the extraction.**

**I picked this over an arm slice because the slice would have consumed the defect.** Nine sessions
were about to build on a column whose own author had flagged it, and the flag understated it: not
"some rows may be mis-signed" but *every stepping arm recorded in one direction only*.

> **An extraction feeding N downstream consumers should be attacked before the first consumer, not
> after the Nth.** The cost of attacking it is one session; the cost of not attacking it is nine
> slices that all say "decrement-only" and agree with each other.

**And the defect was invisible from inside the data.** 58 rows of `-0.01` with no `+0.01` looks like
a finding about the console — developers who only ever tuned downward — rather than a fact about
the extractor. What made it visible was asking whether the *artefact* made sense as a *tool*: a
console with a command to lower a value and none to raise it is not usable, so either the data or
the reading had to be wrong.

---

**repos-2d, 2026-09-03 — slice E (ids 140–171) delivered, and the console turns out to name itself.**

**The row labels were in the image the whole time.** The console's row renderer (`001CD0E0`) prints
`"%s%s%f"` with the label taken from `[ctx + id*8 + 0x130]`, and `FUN_001d0390` fills that array one
`lea`+`mov` at a time, so `id = (disp − 0x130) / 8`. **293 labels, ids 1–294, zero collisions, zero
non-conforming stores.** Every id with an action arm has a name. Slices A–D reported bare addresses
because an arm never names its field — **but the arm was never the only place to look.**

> **A target that cannot be named from the arm may still be named one table away.** The rule "name
> the target, not the arm" was right; what it needed was a second table, not a better reading of the
> first.

**Alignment was proven, not assumed** — four independent checks (the dispatcher's own `add r9d,-0xC`;
id 103 "Camera Over Write (O to capture)" against slice C's capture behaviour; the clamped Ambient
pairs in both C and E; the stride-12 stat array at ids 247–258) plus a cross-source control against
the 21 config-key names in `what-the-console-tunes.md`: **20 arm-bearing pairs, 0 contradictions.**

**Slice E broke the arm shape three ways**, and the first is the important one: **21 of 27 float arms
never execute `subss`.** Both branches are `addss`; the direction is which constant is loaded, and
the "down" constant is a stored **negative** (`009002F4` = −0.01). A `subss`-keyed classifier finds no
decrement in them; a mnemonic-signed one reads two increments. **Concentrated in slices D (25) and E
(21) and absent from A, B and C** — so it was invisible until a slice that contained it was read.

**Two errors, both recorded in the document because they shaped the method.** Merging three
constructors into one offset map gave "Map BGNPC Fresnel **Enabled** = 3.9" for a one-byte boolean —
**the width is what caught it**, and the wrong answer was only detectable because a boolean cannot be
3.9. And a linear `.text` scan produced a consumer that disassembled as `jnp`/`rol` from a
mid-instruction offset. **An unbounded scan buys you completeness and sells you false positives; both
halves have to be paid for.**

**The "56 do-nothing arms" number covers three different outcomes.** The console has two tables —
action (282, base 12) and render (294, base 1) — and crossing them over all 294 ids gives 226 live,
**38 that still display a live value** (they became read-outs: Current LP, the twelve character
stats), **12 labelled buttons with the action removed**, and **6 that draw `"  (EMPTY)  "`**.

> **Unreachable in one table says nothing about how the other table draws you.** A census taken over
> the action table alone cannot see the distinction, and the distinction is the whole finding.

---

**repos-2d, 2026-09-03 — slice H (ids 236–267) delivered. A falsifiable prediction was put to me and it failed; the rule behind it got stronger.**

**Slice I predicted that properties 11, 14, 16, 19, 20 and 21 of the `01F82D20` object would be found
in H.** H holds none of them: its only two arms touching that object read `+0x08` and never call the
property setter at all. Scanning **all 282 ids** instead of one slice: **14 and 16 exist — in slices E
and D** (id 166 "Use soft particle" passes `edx=0xE` for field `+0x38`, and `0x38/4 = 14`), and
**11, 19, 20, 21 are reached by no arm anywhere.**

> **The prediction was wrong about where and right about what.** That is the more useful outcome:
> success would have confirmed a rule two slices already agreed on, while the failure separates
> *"H has not been read yet"* from *"no arm anywhere touches these"* — they are four fields the
> console simply does not expose, not a gap in the numbering.

The rule `property == offset/4` now stands at **14 agreements, 0 disagreements, across four slices**,
and two of those agreements were extracted before the rule existed to be confirmed.

**The cross-arm check reproduced slice I exactly once the denominator matched.** I first reported 21;
slice I said 14. Both are right: **21 jump sites, 14 distinct arms** — five arms contain more than one
such jump. **A disagreement between two careful counts is usually a disagreement about the
population.** And the tail set is more structured than "`001D4BFA` plus `001D4B59`": `001D4B49` is a
**single arm entered at three different offsets** as a shared epilogue.

**H's 18 do-nothing arms are the strongest case yet that the number means three things.** 15 still
draw a live value, 3 are label-only, **0 draw `(EMPTY)`**. A slice-local reading would report a menu
page of dead rows; what is there is **a working character inspector with its editing removed.**

**Two more instances of the same instrument defect, making four in this block.** My property scan
keyed on `mov edx, imm` and missed `lea edx,[rsi+imm]`; the fix then still missed it because
`xor esi,esi` names `esi` while the `lea` base reads `rsi`. Each reported an absence that was an
artifact of the encoding it demanded — after `subss` and `movss`, the pattern is not a coincidence:

> **Check what your classifier requires, not only what it matches.** An extractor keyed on the common
> encoding of a thing will report the absence of the thing, confidently, with a clean-looking zero.

---

**repos-2d, 2026-09-03 — new block. Two documents in 12 and 13; `N-7` is closable and `AI-8` gains a confirmation.**

**`check_already_answered.py` earned its place on the first run.** It surfaced `AI-8`, which already
records **gil as a flagged inference** for the third execution-resource pool. I had just proved it
from the other end and would have written it up as a discovery.

> **The check does not only stop duplicate work — it changes the register of a true finding.** §5 of
> the gil document is written as *"confirming a flagged inference"*, and `AI-8` keeps the question.

It also showed `BattleStats_HasRequiredLicenseForAction` was **named and cited but never read**: the
availability document had located it and stopped. **Located is not read**, and the gap between them
was the whole assignment.

**What the License board actually tests, and the answer is an overlap, not a lookup.** The unit
carries a **46-byte / 368-bit mask at `unit + 0x194`, one bit per board node**. An action's
requirement mask is built by **scanning every node** for one whose category matches and whose
eight-id list contains the action. The test returns on the **first overlapping byte**.

> **Any single owned node licenses the ability.** That is why an ability can appear in four squares
> and be unlocked by whichever you bought — the engine needs no special case, the bits simply OR.
> The loop's early exit is semantics, not optimisation.

Three units are licensed *without touching the board*: record kind != 0, party slot > 6, or the
action's own `0x2000` flag. **The board is a property of being a licensed party member, not of the
ability.** Quickenings (`0xD0`–`0xE1`) bypass all of it and are gated on a **popcount** instead — a
count, not a match.

**Gil: one setter, thirteen callers, and the clamp lives in the setter.** Every path — chest, shop,
defeat, battle cost, console — inherits `[0, 99999999]` for free, and every write is metered to a
statistics counter as a side effect. **The delta is measured before the clamp**, so the meter and the
balance can disagree by construction.

**One caveat I could have hidden and did not.** `mov cl, 6` leaves the upper bytes of `ecx` holding
the new gil value, so the callee receives `(newValue & 0xFFFFFF00) | 6`. Correct if it reads `cl`, a
defect if it reads `ecx`. **I did not read that function, so the document says which question is
open rather than guessing the answer.**

**repos-2d, 2026-09-03 — all four questions of the items/rewards block answered. Two of them by finding the system does not exist.**

**"How are equipment stat contributions applied and re-applied?" — they are never applied.** Equipping
writes a `uint16` into a slot at `stats + 0x50 + slot*2` and, **only if the array actually changed**,
throws the whole effective-stat state away and rebuilds it. 14 triggers across 7 owners reach that
rebuild — equip, **buying a License square**, status change, level, spawn, an action's result — and
**not one of them adjusts a stat.**

> **There is no un-apply step because there is nothing to undo.** A hundred weapon swaps cannot drift,
> and the equip menu's projected numbers are exact because the preview calls **the same rebuild** —
> there is no second implementation to disagree with the first.

**"How is an item's effect resolved when used?" — there is no item-effect system.** A Potion is an
ordinary action row whose category byte `+0x1E` is 3 and whose `+0x22` names the item it costs. The
effect resolves through the same pipeline as a spell.

> The engine never asks *what does this item do*. It asks *what does this action do*, and **item is a
> property of how the action is paid for, not of what it does.**

**Both answers have the same shape, and it is worth naming.** The question presupposed a subsystem;
the finding was that the behaviour is a **property of a generic system**. Twice in one block I went
looking for a mechanism and the result was *"that mechanism is one field on a table everything else
already uses."*

**One byte turned out to gate two systems that look unrelated.** `record[5]` — the battle-record kind
byte, reached through `unit + 0x698` — decides both whether the **License board applies** and whether
the **item/gil resource step runs at all.** Enemies do not spend items because the engine **skips the
resource step**, not because they have an empty bag.

> **The kind byte is the engine's answer to "is this one of the player's characters?", and it is
> reused wherever that question decides behaviour.** Three documents in this block cite it; none
> re-derived it.

**And the equipment document is PARTIAL on purpose.** The rebuild is 2,859 bytes and I read its
prologue and base-stat entry, not its contribution formula. **The architecture is the answer to the
question I was asked; the formula is a different document**, and saying so beats implying I read it.

---

**repos-2d, 2026-09-03 — `11-Party`. `O-5` answered, and a census that was wrong by exactly one function.**

**The reserve is not a separate structure — it is the same array past index 3.** Nine 2-byte records;
**indices 0–3 the active roster, 4–8 the reserve**, `0xFF` empty. A swap is an index change, which is
why the roster and the bench can never disagree about who is where.

**Members and guests are two disjoint selector ranges**, 0–6 and 7–25, with two add functions that
accept one range each and place their entry at different ends. **The split is arithmetic, not a
flag** — and it is the party-layer half of the thing the License work found from the other side:
a guest never reaches the board check because the battle layer exits early on the record kind byte.

> **The party layer decides who is a member; the battle layer then never has to ask.**

**There is no leader.** `022C7FE0` is a handle and whoever it points at is the leader, derived fresh
by 25 callers — nine of them in Movement. Changing it is a **request** (`022C7FE4` + a kind byte) that
a later **commit** applies, tearing down the outgoing actor by one of two paths. **Nothing is
notified**: no callback list, no dirty flag. That is why the formation never lags a frame.

**The finding I would have missed, and how.** My function-bounded sweep found three writers of the
handle and none that could set request kind `2` — so the commit's `cmp … 2` looked like dead code.
An unbounded `.text` scan found a **tenth site inside a 27-byte function absent from
`functions.tsv`**, and that function is the *only* writer of kind 2.

> **A caller census is bounded by its function list. This one was wrong by exactly one function, and
> the missing function was the only writer of the value in question.**

The same run produced a false positive (a float read decoded mid-instruction), which is the standing
price: completeness bought with candidates that must each be decoded before they are believed.

**And the address checker independently confirmed it.** `verify_doc_addresses` flagged all five
instruction addresses as *non-function* — correct, and for the same reason the census missed them.

> **Two instruments reporting the same gap is evidence, not two problems.** I dispositioned the flag
> rather than clearing it, because removing the citation would delete the only record of the only
> writer of kind 2.

---

**repos-2d, 2026-09-03 — `04-Actor-Entity`. The band is answered, and I did not name it.**

**`record[+4]` is one type-id number line cut into four spans**, not a flag byte with a special case:
`0..6` | `7..25` | **`26`** | `27..39` | `40+`. One site states the whole partition
(`Reward_ComputeLicensePointsForRecipient`) and a Script-VM bridge classifies a record into five
outcomes using all of it.

**The band `0x1B..0x27` is one predicate inlined 27 times** — `(type - 0x1B) <= 0xC`, never once with
a different bound, across seven subsystems. **A category consulted that widely with no function of
its own is why it never acquired a name.**

**"Two tests where one would do is two different reasons" — confirmed, and both reasons are visible.**
`0x1A` is excluded from the experience recipient count *alongside* the band, and **accepted for
License Points alongside the main roster.** Had it belonged to the band, `(type - 0x1A) <= 0xD` would
have been smaller code and a silent behaviour change.

**The 28th band site indexes instead of testing**, and its 13-entry table is an exact arithmetic
progression: `code = 42 + 3*(type - 0x1B)`. **Stride three — each type owns a block of three.** The
progression is the finding: a hand-authored lookup would not be arithmetic, so **the table exists
because the codes are laid out three-per-type somewhere else.**

**And the `7..25` span is character-for-character the party layer's guest predicate.** Same test, two
layers. **Recorded as a correspondence, not an identity** — no site has been read that copies one
field into the other.

**What I did not write.** A thirteen-value category in this game has an obvious name. **Nothing in
the corpus ties any span to a player-facing concept** — no string, no table name, no label — so §9
says the spans are unnamed and leaves the guess unwritten.

> **The measurement was easy and the temptation was the whole test.** Naming it would have cost
> nothing today and been unfalsifiable forever.

**Fifth instance of the same instrument defect, and the worst ratio yet.** My census keyed on
`mov reg, [reg+4]` and missed `cmp byte ptr [reg+4], imm` — which is exactly how the site that
motivated the block is written. First run: **1** site for `0x1A`. Corrected: **7**.

> The band's 28 was unaffected because every band site happens to use the register form. **That is
> luck, not validation**, and the document says so.

---

**repos-2d, 2026-09-03 — `21-RNG-And-Determinism`. Four generators, and three of my own checks failed together.**

**The correlation answer is a clean pair of opposites.** Combat rolls (MT19937, 66 consumers, 53 in
CombatFormula) and loot rolls (the shared LCG) are on **different generators with disjoint state** —
they cannot be correlated by anything a player does. But **loot, the enemy chain and weighted action
selection share one LCG state**, so every draw by any of them moves the others along.

**Seven of the eight LCG draw sites are inlined.** A census keyed on `call` sees one. I censused the
**multiplier constant** instead: 24 instruction sites, three per draw, and **every one reads the same
state global**.

**What reseeds each, which is where the interesting asymmetry lives:**

- **LCG** — a plain counter, post-incremented once per battle-area init. **Two instructions in the
  whole image touch that counter.** Nothing clock-derived, nothing restored from a save.
- **MT** — the constant `4537` at boot, and on **save load** a seed computed from **`_time64`**.

> **"Deterministic from boot" and "deterministic across a reload" are different claims, and only the
> first is true.** Reloading rerolls the combat outcomes and does not reseed the loot stream.

**The correction that matters more than the finding.** My first draft was going to say the MT is
never explicitly seeded. **Three checks agreed on zero**: a caller census, an unbounded scan for `E8`
call encodings, and a scan for 8-byte pointers to the seeder.

All three were wrong together. The seeder is reached through a `jmp` thunk, **and the name is
attached to the thunk rather than the body**, so the call graph indexes callers under the thunk.

> **Three methods that share an assumption are one method.** Each asked *"what calls the body"*, and
> the honest answer was that nothing does — the thunk *jumps* to it. **Independence has to be
> independence of the question, not just of the technique.**

Following the thunk found **two** callers, and the second — the save-load reseed — is the more
interesting of the two. It would have been missed entirely, and the document would have claimed a
determinism property the engine does not have.

---

**repos-2d, 2026-09-03 — `02-Resource-And-Asset-Pipeline`. The archive is called a BigFile, and its index is MD5-verified.**

**The container format, read from the engine rather than from a tool.** `fopen("rb")` — CRT stdio, not
Win32 — magic `SRYK`, an index-size dword, then **the last sixteen bytes of a 31 GB file** read
separately, then the **whole index in one `fread` from offset 0**, then `fclose`, then six CryptoAPI
calls hashing the index with **`CALG_MD5`**.

> **The digest covers the index and nothing else.** Replacing an entry's payload in place — same
> offset, same length — leaves the digest valid. **Changing the index in any way breaks it, and the
> failure is at open, not at use.** That is a consequence of *where* the hash is taken, not of a
> stated policy, and it is the practical rule for repacking.

**The engine's own word for the format is in its error string: `"BigFile head wrong!"`.**

**The instrument that made this cheap was the import boundary.** I mapped every IAT slot to
`dll!name` and censused **indirect calls through the slot address**.

> **Keying on the slot is immune to both hazards that bit me tonight** — a thunk cannot hide a call
> that goes through the slot, and no naming convention is required. The residual gap is a pointer
> copied out of the slot into a register, and §8 says so rather than claiming a guarantee.

That gave the whole byte-delivery surface as a measurement: **three `ReadFile` sites, all `Resource`;
17 `fread`; and no memory-mapped path at all** — neither `CreateFileMapping` nor `MapViewOfFile`
appears among the imports, which is a **directory-level** negative needing no call-site search.

**What is cached is the index, not the file.** `fclose` runs inside the opener, before verification.

**And one thing I read but did not follow.** The six CryptoAPI calls are present and their arguments
are decoded — but I did not follow the comparison that consumes `HP_HASHVAL` to its branch. §7 says
**"the check is present; its consequence is assumed, not read"** rather than asserting the game
refuses to boot.

---

**repos-2d, 2026-09-03 — `16-UI`. Three measured negatives, two request submitters, and no document.**

**The text path is not reachable from the import boundary, and now that is measured rather than
assumed.** All four font drawers — `002AC5F0` (7,489 B), `002AAE40`, `002AF960`, `003649A0` — call
**zero imports** and reference **zero strings directly**, and every caller of every one of them is an
unnamed, unowned residual.

> **Three cheap discriminators, all negative.** That does not identify the functions, but it closes
> three approaches, and closing an approach is worth reporting: the slot-keyed census that worked on
> the resource pipeline **cannot** reach this cluster, because the cluster never touches the OS.

**Why the router's request identities have stalled.** The ids are **computed, not literal**: three
call sites into the router and eight into the mailbox, and not one passes a constant in the obvious
form. That is the reason the open items sit at "identity of requests 4, 6–13, 15–20, 22–24" — the
information was never in the argument as written.

**Sixth instance of the encoding hazard, this time in a shared instrument.** `argscan.py` resolved
`lea r,[0+disp]` but not `lea r,[zeroed_reg+disp]`, so `xor edx,edx ; lea ecx,[rdx+0xB]` — the
constant **11** — reported DYNAMIC. Fixed; the same census now returns **3 CONST where it returned
none**: requests **2** and **3** from input arbitration, request **11** from a UI function.

**And I did not produce a document for this block.** Two recovered submitters and three negatives are
an amendment, not a system.

> **Padding three probes into a document would have been the easy call and the wrong one.** The block
> needs a call-graph walk into the residual cluster, which is a different size of job than a probe,
> and saying so is more useful than a thin page that looks like coverage.

---

**repos-2d, 2026-09-03 — the residual-cluster walk. The way in was the data, not the code.**

**Every code-side route into the cluster is closed, and I closed them by measurement**: no imports, no
direct strings, only the shared `"display : draw Font"` scope within two calls, and no named caller
anywhere. So I stopped looking at code and looked for **a pointer to the function instead**.

`002AAE40` has zero callers and **exactly one pointer in the image**. Immediately after it sits
`1, 10, 100, … 100000000` — **the powers of ten** — and immediately before it, six function pointers.

> **A function nothing calls is still a function something references.** The entry point to the whole
> cluster was a table sitting between a run of handlers and a decimal-magnitude table.

**The architecture: two kinds × three operations**, selected by **one signed byte at `obj[0xA3]`**,
with three dispatchers that do nothing but index and tail-jump — one of them guarded by
`obj[0xAC]==1` or a global. **The selector is never bounds-checked.**

**And two of the three columns identify themselves from what their handlers touch:** column 0's
handler takes the address of the powers-of-ten table (**numeric**), column 1's is a direct caller of
the 7,489-byte font drawer (**text**). **Both are shared by both kinds; only column 2 differs** — and
column 2 is the one column no dispatcher was found to reach.

**A correction worth keeping.** My pointer scan reported a decimal offset; I converted it to hex
wrongly **twice** and dumped the wrong neighbourhood twice before noticing the value at the address
was not the value the scan claimed.

> **An instrument that computes an address should be made to read it back.** The check costs one line
> and converts a silent arithmetic error into an assertion. The scan now verifies every hit through
> the VA it reports.

**Still open, and narrowed rather than closed:** which text each drawer draws. `002AC5F0` is entered
from column 1 for *both* kinds and from column 2 of kind 0 — **so it is not specific to one kind**,
which is consistent with it being the largest of the four and the one six functions call.

---

**repos-2d, 2026-09-03 — second cluster block. I corrected my own table, and it turned a curiosity into 4 KB of dead code.**

**My first document said the table had two rows. It has four.** I had read it to the last non-null
entry before the gap and stopped.

> **Reading a table to its last non-null entry is not reading the table.** The null rows are part of
> it — they are *why* every dispatcher null-tests the loaded pointer — and the orphan function of my
> own section 2, `002AAE40`, turned out to be **kind 3, column 2**, sitting inside the rows I had not
> read.

Corrected in place with the original claim quoted.

**And the correction produced the block's real finding.** Nothing indexes column 2, so a column-2
handler can only be reached by a direct call. Tested with **unbounded** scans — every `E8` and `E9`
displacement in `.text`, every verified 8-byte pointer in every non-`.text` section:

| column-2 handler | E8 | E9 | pointers |
|---|---:|---:|---|
| `002A9F00` (kind 0) — **control** | **8** | 0 | its table slot |
| `002AA800` (kind 1) | **0** | **0** | its table slot |
| `002AAE40` (kind 3) | **0** | **0** | its table slot |

> **4,038 bytes of code that nothing in the image can reach.** Their only reference is a table slot
> no code indexes.

**The control is what makes it a measurement rather than a silence.** `002A9F00` is in the *same
column of the same table* and the same scan finds eight calls to it — it survives because it is also
called directly, which makes its table slot redundant rather than load-bearing.

> **A zero from an instrument reporting eight for a sibling in the identical position is evidence.**

**And I did not name the kinds.** Ten byte-writes to `+0xA3` exist image-wide; four are in this
cluster's neighbourhood and write 0, 0, 2 and 3 — **the writer of 1 is in `Audio`, which may be a
different structure at the same offset.** Offset coincidence across unrelated objects is exactly what
the `[reg+4]` census taught, so the document says *not resolved, and not assumed*.

---

**repos-2d, 2026-09-03 — third cluster block. I probed tractability instead of guessing at it.**

**Asked to judge which open items were reachable, I measured rather than estimated.** *Why column 2
exists* is a "why" and unanswerable from a binary. *The kind identities* lead deeper into unnamed
residuals. *What `[0209CC40]` is* had **one writer against 121 readers** — so that was the tractable
one, and the probe took two commands.

**The context is a static 4,360-byte struct at `0209D490`**, zeroed once, published once, never
reallocated, **with no vtable** — consistent with the cluster dispatching through a hand-rolled table
rather than virtual calls. **25 offsets are touched, and they are the last sixty bytes**, after three
pointer slots that are read and never written.

**`+0x10D8` is the field the dispatchers publish into** — so that field is how a per-element value
reaches a handler that is never given the element.

**The part I want kept is the negative I refused to make.** My scanner tracks a register inside one
function; it cannot cross a call. The front 4,192 bytes are untouched by every function that loads
the pointer — **and the pointer is passed as argument 1 at nine sites to seven functions**, including
the one carrying the `"display : draw Font"` scope.

> **The measured statement is "not accessed here". The unmeasured one would have been "not
> accessed".** One is a field map with a stated edge; the other is a claim about 4 KB of a struct
> that an instrument of this shape has no standing to make.

Both absences are in the document and **labelled with different strengths**: zero indexed accesses is
a counter that would have reported non-zero; the 4 KB is scoped, with the nine call sites given so a
reader can size the gap themselves.

---

**repos-2d, 2026-09-03 — fourth block. The block's premise dissolved, and the instrument that created it was mine.**

**The fourth block was to be "the callee side". There is no callee side.**

My §5 claim — *the context pointer is passed as argument 1 at nine sites to seven functions* — was
**wholly an artifact**. The tracker followed a register but walked instructions **linearly, ignoring
control flow**, so at a jump target it carried a value that every real path had killed. Made
block-aware, the same census returns **zero**.

> **A register-tracking instrument that does not model control flow is not conservative; it is
> wrong.** It does not under-report, it **invents** — and all nine inventions looked like ordinary
> call sites at real addresses.

**What caught it was reading one of them.** At `002ADBFD` the three instructions before the call set
`r9`, `r8` and `rdx` and are reached by a branch; `rcx` is never set on that path. And the seven
"callees", read in full, are **three-byte sequence decoders** — they read `[rcx+1]`, `[rcx+2]` and
return the constant 3.

> **The callees made no sense as callees.** That is a cheaper signal than any checker, and it is
> available to anyone who reads what an instrument hands them instead of tabulating it.

**The field map was rebuilt with the same fix and its shape did not move** — same three pointer slots,
same tail block, one spurious offset removed and counts adjusted. **A conclusion that survives the
correction of its own evidence was resting on the structure, not the counts.**

**And the refusal survived its evidence.** I had declined to claim the front 4 KB was unused *because
callees might use it*. That reason is now withdrawn — and the refusal still stands, because the
corrected tracker under-reports by construction.

> **The reason to refuse a claim changed; the refusal did not. A negative that only holds while one
> particular support holds was never worth making.**

**The cluster is finished.** What remains is an object identification I have no route to and a "why"
the binary cannot answer. **Declaring that is the deliverable, not a fifth block.**

---

**repos-2d, 2026-09-03 — `14-Story-Event-Quest-Hunt`. `AA-6` and `AA-7` answered; the second is a negative with a positive half.**

**Before the block: I audited my own published census against the fabrication hazard.** `argscan` was
already block-aware; **`field4.py` — which produced the actor-entity band census — was not.** Patched
and re-run: **0x1A still 7 sites, 0x1B still 28, same owner distribution.** The published claim
survives, and now it has been *checked* rather than assumed.

**`AA-6`: two event-memory lookups, different shapes, both at actor bind.** One is a linear `uint16`
id search (count `+8`, entries from `+0xA`); the other is **directly indexed by the definition id**
into 3-byte records (count `+4`, records from `+8`).

> **One asks "is this id in a list?", the other asks "what does this id's record say?"** A list that
> grows and a table sized to the id space are different kinds of memory, and the engine consults both
> before binding an actor.

**`AA-7`: there is no hunt or bestiary system to ask about.** Zero `bestiary` strings in 48 MB. The
three hunt-like hits are **a typo in a network log (`ServerShuntdown`), an achievement title
(`Hunter Extraordinaire`), and my own debug-menu label (`Set clan point`)**. Two functions in the
whole image carry the `Story_Event_Quest_Hunt` owner.

> **Every string hit was read rather than counted.** A count would have reported *"hunt: 1"* and been
> misleading in the opposite direction — the one match is not a hunt system, it is a misspelling.

**And the negative has a positive half, which is what makes it an answer rather than a shrug.** The
native surface is six flag banks with a uniform VM query/setter per bank, two event-memory lookups,
and a ~20-kind statistics counter. **A hunt is a flag convention plus a counter, authored in script
over that surface** — the fourth time this run that "where is the X system" resolved to *"one field
on a table everything else already uses."*

---

**repos-2d, 2026-09-03 — closed my own thread, then `19-Save-Load-Settings`. `V-2` answered by the comparison, not the digits.**

**First, the debt.** `0025A990`/`0025AA30` read in full: they are the same routine over different
globals — free-if-held, then allocate **1 MiB (tag 13)** and **100 KiB (tag 14)** from pool 5. Both
pointers are touched only by `ActorEntity` code, so they are **actor-payload buffers**.

> **So the two "event memory" lookups gate memory, not story state.** The engine asks whether a
> definition id is already known and, if not, **makes room for it**. The name says `EventMemory_*` and
> carries the Story owner; **the only call site reads as buffer lifetime management, and the behaviour
> is what I reported.** That makes the `AA-7` negative stronger, not weaker.

**`V-2`: both constants are magics, not versions.** `0x20050223` and `0x05071901` each come from a
six-byte getter with exactly one caller, written into the save header at init. An immediate sweep
found **every** occurrence — three and one — and **the only comparison in the image is `cmp` followed
by `je`.**

> **A value only ever tested for exact equality is a magic, whatever its digits spell.** They spell
> dates in packed decimal; that is a reading of the digits and **not** what decides the mechanism, so
> §2 states the comparison first and the digits second.

**And the stamp is load-bearing.** It guards a **29,712-byte runtime state block** that is zeroed and
re-stamped on mismatch — and that block is where the **party roster and reserve live**, at the same
`+0x5A48`/`+0x5A7E` I mapped two blocks ago. **A one-dword mismatch discards all of it.**

**"What loading normalises" is answerable concretely:** nine steps, five named — restore the active
field id, **import the persistent flag bank**, restore transition metadata, touch achievements, and
**reseed the RNG from `_time64`**.

> **Loading is not restoring.** The named steps *import*, *restore* and *reseed* rather than copy.

---

**repos-2d, 2026-09-03 — the five-map correction verified, accepted, and extended.**

**Verified before accepting.** I read `BattleSlotMap_ResolveMappedBattleSlot` myself: five bases at
`0x5A48`, `0x5A5A`, `0x5A6C`, `0x5A7E`, `0x5A90` — **exactly `0x12` apart**, all behind the same
class-`0x17` id check, all read as a **byte at a two-byte stride**. The correction is right.

**My §2 read class 3 and presented it as the structure.** Corrected in place with the scope of the
original claim stated: the roster/reserve split is correct *within* that map and is not the whole
thing.

> **Nothing pointed from my site to the other four.** Five functions touch this structure and no
> document cited two of them — which is why a correct reading looked complete.

**Then I named the classes, because the resolver takes the class as an argument.** Four direct
callers, three of them thin pass-through wrappers; scanning the wrappers' own sites gives **31 call
sites, 23 passing a constant**:

- **class 0 = `0x5A48`** — `Equipment_UnequipEncodedItemFrom***ActiveRoster***`, and **the only map
  the initialiser fills**. Two independent reasons pointing the same way.
- **class 1 = `0x5A5A`** — EXP recipients and periodic combat maintenance: the combat-processing set.
- **class 3 = `0x5A7E`** — fourteen sites across equipment, targeting, defeat rewards, party and the
  script VM: the general gameplay map.

> **Five maps are one roster and four views of it that are allowed to drift.** The initialiser makes
> them identical; **what makes them diverge is not in anything I read**, and the document says so.

**Classes 2 and 4: unreached, not absent.** Eight sites pass the class through from their own caller,
so a constant could exist one level up. **"No site passes 2 or 4 directly" is weaker than "nothing
uses them"**, and it is written as the former.

---

**repos-2d, 2026-09-03 — the divergence negative: nearly wrong, then supported three different ways.**

**The displacement census and my `lea` scan both missed the actual access form.** The five map bases
are used as **bare immediates** — `mov esi, 0x5A5A` then `movzx eax, byte [rsi + ptr]` — which is
neither a displacement nor a `lea`. Seven such sites exist for map 1 alone, in `Party`, `Movement`
and `ActorEntity` functions, one named `...ReconcileRuntimeRosterFirstThreeFromRequestedSelectors`.

> **Eighth instance of the family, and it briefly falsified a negative we were both about to
> publish.** I read one of the sites before reporting: it is a **read**, not a write.

**A third scan, keyed on the register holding the immediate, settled it: 6 reads of map 1, 2 of map 3,
zero writes to maps 1-4.** Map 0's only two writes are `0xFFFF` fill loops in two initialisers, both
read to confirm.

> **Three instruments asking three different questions — what writes offset N, does a pointer escape,
> is a base held in a register — and one answer.** A negative is only as strong as the variety of
> questions that failed to overturn it.

**And the third instrument cut both ways, which is the lesson worth keeping.** Run **block-aware** it
returned **zero accesses** — including one I had already read by eye, because the base register is
loop-invariant and survives a branch the conservative version resets at. Run **permissively** it found
the real accesses, and every hit was read before being counted.

> **For a negative, use the instrument that cannot invent. For a search, use the one that cannot miss,
> and read everything it returns.** The conservative version omits as badly as the linear one invents,
> and not saying which is in use is how a zero becomes a claim.

---

**repos-2d, 2026-09-03 — the encoded-id class registry. Four documents were each holding one row of a table none of them could see.**

**Your open item — "a class number is an identity, not a description" — was answerable from the
validator rather than from any caller.** `BattleEncodedId_IsValidForClass` dispatches on `class - 1`
through a **32-entry jump table**, so the whole mapping is one extraction.

> **Class 4 is `02EBF150`** — your address this tick.

**Two independent confirmations of existing documents, reached from the opposite direction.** Class
**20** resolves to `02EBF138`, the same action table my License document reads from the consumer side;
class **23** has a **literal bound of 9**, and my party document independently found **nine**
configuration slots. Neither shares code with the validator.

**And one correction to my own work, of a kind no call site could reveal.** My License document
recorded class **1** as the equipment class, because equipment passes 1. **Class 1 names no class at
all** — its arm derives a class from the id and re-enters the switch.

> **A call site only shows the number going in.** "Equipment passes class 1" is true and
> "class 1 is the equipment class" is false, and the difference is invisible from every caller.

**Three of the thirty-two arms consult no table** — the dynamic one, a **range** check
(`0xE000`-`0xEFFF`), and a **literal bound**. So *"the class picks a table"* is the rule, not the
definition, and an extractor assuming a descriptor per class would be wrong three times. Mine reports
them as "no global read" rather than misfiling them, which is why they were noticed.

---

**repos-2d, 2026-09-03 — descriptors named: 14 of 25, and the eleven that will not name themselves.**

**A descriptor carries no identity; the functions that walk its rows do.** One pass collecting every
rip-relative reference per descriptor, keeping the *named* referrers:

- **class 20 → action definitions** (128 refs, the most-referenced table in the game)
- **class 6 → equipment definitions** (42) · **class 2 → character growth** (23)
- **class 26 → status definitions** (18) · **class 29 → status auxiliary/timers** (15)
- **class 25 → License board nodes** (15) · **class 11 → gambit definitions**, **10 → gambit presets**
- **classes 14, 15, 18 → item classes `0x9`, `0xA`, `0xD`**
- **classes 3 and 4 → two unit-definition tables**, both read by `BattleUnit_ApplyUnitDefinition`

**Eleven have no named referrer at all** — every function touching them is `FUN_xxxxxxxx`. The method
cannot name them and the document says so rather than reaching for a plausible label.

> **Three classes line up with the item-id top nibble** — 14/15/18 against `InventoryBundleClass09`,
> `0A`, `0D`. **Recorded as a correspondence across two numbering schemes, not an identity**: no code
> was read that converts one into the other. That is the fourth time tonight I have declined to
> upgrade a numeric coincidence, and the reasoning is the same each time.

**And I labelled the epistemic status of the whole table rather than just its rows.** These names are
**inferences from referrer names**, not decodes of table contents; the referrer *sets* are tier-1
measurements. **A row with one named referrer is weaker than a row with fifty, so the count is a
column.**

> **Naming a table by its consumers is a different act from reading it**, and a registry that does not
> say which it did would be read as the stronger one.

---

**repos-2d, 2026-09-03 — the eleven "unnamed" classes named, by discovering they have no specialised consumer.**

**All eleven are referenced by the same two functions and nothing else** — the **authored-table
loader** (`FUN_00236C30`, which calls `AreaData_BindAndRebaseSectionDescriptor` **33 times** across
**36 descriptors**) and one **generic per-class query** (`FUN_0031C5D0`, 8 KB, resolving runtime
pointers **168 times** and validating **26 classes**).

> **"No named referrer" was a statement about this database's naming; the engine's answer is "generic
> access only."** The fourteen nameable classes have those two referrers *as well* — what makes them
> nameable is the specialised consumers they have **in addition**.

That converts eleven blanks into a **positive structural claim**, and it is a better result than
eleven names would have been.

**And class 12 has neither.** Its descriptor is referenced by **the validator alone** — the loader
does not bind it, the generic query does not reach it. **One of thirty-two classes has no consumer of
any kind.**

**The loader is also the caller `authored-data-table-registry.md` already records as populating the
slots at area load.** That document reached it from the resource side; I reached it from the class
side.

> **Two documents, one function, neither citing the other — the same shape as the four documents each
> holding one row of the class table.** The fix is the same one I proposed and it would have worked
> here too: **cite the registry, not the number.**

---

**repos-2d, 2026-09-03 — I claimed "all 93 from one function" and it was 84/9. Caught by a peer's cross-check.**

**The disagreement was real and I was the one who was wrong.** repos-55 said the instruction at
`001C978E` falls in `001C7940`; my message said all 93 references came from `001C3D50`. Checking
rather than defending: `001C3D50` **ends at `001C4F4F`**, nowhere near, and the true split is
**84 in `001C7940`, 9 in `001C3D50`.**

**How the error happened, which is the transferable part.** My summary line counted the **owner**
column — `{'(none)': 93}` — and I read it as a function count because **the eight rows I printed
happened all to be in `001C3D50`.**

> **A summary line that aggregates one column will be read as aggregating the column you had in mind.**
> Print the discriminator you intend to claim, and read more rows than the ones that agree with you.

**The corrected version is the better finding.** 84/9 across **exactly the two scene-config loaders
the frame document already names** is more informative than "all from one", and it also shows
`ShadowValueB` has **three** references — so **a census of a name counts lookups, not settings.**

**What survived unchanged:** 93 references, **all 93 on a string start, zero mid-string, no pointer
array anywhere**. The region cannot be indexed and nothing indexes it, so **an address that looks like
a table base is a specific datum** — which is what settled the peer's open item without needing their
arm at all.

> **The claim that was checkable survived; the claim I had not checked did not.** Both were in the
> same message, and only one of them was a measurement.

---

**repos-2d, 2026-09-03 — the all-ones convention, and the reason behind it.**

**Eight sightings across two sessions, none citing another** — party selectors, the slot resolver's
failure return, the actor's own slot field, pooled list links, an adjacent handle pair, a trigger
record's flag id, and two **two-byte** cases using `0xFFFF`.

**The reason came from the clearest instance rather than the count.**
`RelationLook_RemovePooledRelationRecord` unlinks a record whose `+0xD`/`+0xE` are **one-byte prev and
next indices** into a 16-byte-record pool — `shl rax,4 ; add rax, base` proves they are indices — and
`0xFF` is the null link.

> **That is why the sentinel is all-ones and not zero: index `0` is a real record.** In an index space
> over a pool, zero is an occupant, so the only free value is the other end of the range. **The
> convention is forced by the representation, not chosen for style** — and the two-byte cases using
> `0xFFFF` rather than `0xFF` is what that prediction requires and a "the byte 0xFF is special"
> reading does not.

**And I kept the census and the reading apart on purpose.** 169 byte-stores and 87 compares establish
that the idiom is widespread; they establish nothing about meaning, because `mov byte [x],0xFF` is
also a mask or a signed `-1`.

> **The strict test — a field both written and compared inside one function — returns six.** Three are
> **adjacent byte pairs**, one of them the `+0x695`/`+0x696` a peer had just found from the cancel
> path. **Two directions, one pair.**

**The count is published anyway, with its limit stated**, so a reader can see how much is left
uncharacterised rather than inferring that 256 sites were verified. **Six read fields support the
claim better than 256 counted ones, and saying which is which is the whole difference.**

---

**repos-2d, 2026-09-03 — ran the new checker against my own 16 documents; three failed, worst was the reference document.**

**Applied it immediately rather than noting it**, as with the fabrication audit. Three flagged:
**class registry 22, party 11, RNG 8.**

> **The registry was the worst, and that is the sharpest possible version of the defect: a document
> whose entire purpose is reachability, naming twenty-three functions and citing none of them.** Its
> §5b table said "named by `Equipment_SelectPreferredCandidateByAuthoredStats`" and a reader could not
> get from that to an address.

All three now clear.

**And the fix introduced its own error, which is the part worth recording.** I anchored
programmatically to avoid transcription slips — and the blanket pass wrote addresses **into the Key
addresses tables, where the address column already carried them**, producing rows like
`| 00863BF0 | RNG_MT19937_NextU32 (00863BF0) |`.

**Worse, one row got the wrong address.** `RNG_MT19937_Seed` names **two** functions — the thunk
`00379CF0` and the body `00863D30` — so my name→address map kept whichever came last, and the thunk's
row was annotated with the body's address.

> **That same name collision bit me twice tonight in two different ways**: first as *"zero callers"*
> when I queried the body while the call graph indexed the thunk, and now as a wrong anchor. **A name
> that maps to two addresses will fail differently in every tool that assumes it maps to one.**

**Caught by reading the output of my own fix.** Seventeen redundant anchors stripped, and the wrong
one with them.

> **A fix applied to a checker's finding is output like any other, and needs the same reading.** I ran
> a bulk edit to avoid one class of error and introduced another; only looking at the result
> separated them.

---

**repos-2d, 2026-09-03 — anchored nine of twenty in a document I did not write, and left eleven visible.**

**First, a factual correction: the top three flagged documents are not mine.** `rng-streams.md`,
`battle-record-kind-byte.md` and `authored-data-table-registry.md` are all dated **2026-09-02** — they
are the documents I *built on*. That **supports** the coordinator's own reading that the gap sits in
work predating the convention.

**I took `rng-streams.md` because its subject is one I independently re-derived** — the LCG draw
sites, the state setter, the area-init seed counter, the MT thunk. **Nine names anchored with
addresses I measured myself.**

**Eleven left unanchored on purpose.** `BattleLocomotion_*`, `LuaMath_Random*`,
`RNG_D_Phyre_GenerateRandomFloat01` and the rest were **not read by me**, and `functions.tsv` would
have supplied every one of them in a single pass.

> **An address supplied from a name lookup is a transcription, not a citation.** A bulk anchor would
> have cleared the checker and asserted eleven readings nobody had made — **the checker would have
> gone quiet and the document would have become less honest.**

The document now says which nine and why the eleven are missing, so the gap stays visible instead of
being papered over by the tool that found it.

> **A checker measures what it can see. Satisfying it is not the same as fixing what it points at**,
> and the difference is exactly the eleven names I could have anchored in one command.

---

**repos-2d, 2026-09-03 — took the AMBIGUOUS row: 57 duplicated names, and the ambiguity is mechanical.**

**Fifty-seven names in the image are carried by more than one function.** Classified by disassembling
every short entry and testing whether its first instruction is a `jmp` to another member of its own
name group:

- **53 are thunk + body** (48 pairs, 3 triples, one four, one five)
- **1 is a thunk chain** — a thunk whose target is another thunk
- **3 are genuinely distinct bodies**, and **all three are compiler artifacts**:
  `scalar_deleting_destructor` (one per class), `malloc`, and
  `scheduler_resource_allocation_error` (**eight identical 47-byte throw helpers**)

> **No engine function shares a name with a different engine function.** Every other collision is a
> name and its own thunk — so the ambiguity is a property of the linker, not the naming, and it is
> resolvable without judgement.

**And the resolution depends on the question, which is exactly where my two failures came from:**

| question | resolve to |
|---|---|
| what calls this? | the **thunk** — the body may have **zero** direct callers |
| what does it do? | the **body** |
| what do I cite? | the **body**, unless the claim is about the thunk |
| is it reachable? | the **union**, followed transitively — a chain exists |

> **A name is not an address in this corpus.** A tool that resolves one to the other silently has
> answered a different question than the one it was asked — which is why one collision produced a
> false *"zero callers"* and a wrong anchor in the same night.

**Modding consequence:** for 53 names, *"hook the function"* is ambiguous until the group is resolved
— a hook on the body misses everything routed through the thunk.

**Follow-up, same tick — the caller-census exposure has a number: 30 of 53.**

repos-55 broadcast that *every caller census in this database has the same exposure unless it follows
thunks*. That was checkable, so I checked it: counting direct callers of both entries in all 53
thunk/body groups, **30 bodies have ZERO direct callers while their thunk has some.**

> **`RNG_MT19937_Seed` was not a special case — it is one of thirty.** The others include
> `WorldTransition_RequeueCurrentFieldForRestore`, all four
> `InputGameplay_GetActorStateAwareRemappedMask*` variants, and `SaveImage_BackupActiveRuntimeBuffer`.

**A zero from a caller census on one of those thirty is not evidence of anything** — it is the shape
of the question, and **it is indistinguishable from a real absence**, which is what makes it dangerous
rather than merely inconvenient.

> **Any claim of the form "N callers" for a name in this class has to say which entry it counted.**

A warning is a thing to remember; **30 of 53 is a thing to check against.**

**Follow-up: my own census was keyed on the name, and the hazard is not name-shaped.**

I ran the review repos-55 identified — every caller-count claim in the corpus naming an ambiguous
function — and **found one of my own wrong**: `gil-storage…` published *"19 callers"* for
`GameState_GetGil`. The body has 19; **three more functions reach it only through the thunk, with zero
overlap. The figure is 22**, and `CombatFormula` rises from 1 to 3. Corrected.

**Then I checked whether "duplicated names" was even the right population. It is not.**

- **750** listed functions have a short `jmp` thunk aimed at them
- only **58** of those thunks share the target's name — the set my census found
- **692** have a differently-named thunk, **invisible to any name-keyed census**
- of the 325 whose thunks carry callers: **140 targets return zero** from a body census, **185
  silently undercount**

> **The hazard is thunks, not duplicated names — and only 8% of thunks share their target's name.** A
> census keyed on the name found the name-shaped subset of a thunk-shaped problem, **which is the exact
> failure the document was written to describe, committed by the document itself.**

**Both of my failures land in the corrected population:** the false zero is one of the 140, the gil
undercount one of the 185. **30 of 53 was a true number about the wrong denominator.**

> **A zero looks like an absence; an undercount looks like a number.** The second is worse, and it is
> the larger population.

**Follow-up: checked my thunk census against the undefined-bytes blind spot. 750 is a lower bound, by about 2%.**

repos-55 warned that `search_instructions` cannot see undefined bytes. **Mine did not use that tool —
it walked `functions.tsv` — which has the same blind spot in a different shape:** a thunk in the
509,214 bytes between listed bodies is in neither.

Scanning all **33,346 gap regions** for a five-byte `E9` landing on a listed function:

- **255** hits
- **17 isolated** (padding both sides) — genuine standalone thunks, reaching **16** targets
- **238 embedded** — tails of unlisted code, not thunks

> **750 should be read as at least 766.** The undercount is real and small — and worth stating
> precisely **because the raw hit count would have suggested 34%.**

**The isolation test is the whole difference.** An `E9` in unlisted bytes is far more often the tail of
a function Ghidra never defined than a stub; only padding on both sides makes it standalone.

> **Counting the 255 would have inflated my own correction fifteenfold** — a wrong number published in
> the act of correcting a wrong number. The test that prevented it cost one comparison per hit.

**And the 238 are their own small finding:** real code exists in the gaps and ends in jumps, which is
what a 92.91% function-list coverage figure means concretely rather than as a percentage.
