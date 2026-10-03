---
system: The selection the menu publishes
category: 16-UI
status: DOCUMENTED — the three functions hold one object type and 0209BE80 is the per-frame update gate's singleton slot (SWE2-DATA); what the +0x2FE0 value names (SD-124) and what +0x2FF0 bit 0x4000 means (SD-125: the dispatcher's open window is kind 1, the top command list; FABLE, reviewed ACCEPT-WITH-NARROWING by SWE2-AUDIT-SEM, C1 and N1 applied) are answered; the dispatch jump table (0027E384, twenty command kinds) walked 2026-09-18 and 0027E530 identified as one of its five installed procedures (owner re-status 2026-10-01, OPUS; documented_rule READY)   # <- corrected 2026-10-02, OPUS - six installed procedures, not five: 0027E050's lea sites name 00276BE0, 0027D240, 0027CE70, 0027D5C0, 0027E530 and 0027BC10
owner_layer: PrimaryOwner:UI
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 113 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-03
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: pair-frontier-repos-55
  crossref_clean: false
  reopened_count: 0
---

# The selection the menu publishes

**A pair-census row: `+0x2FE0`, fourteen sites across three functions**, two of them documented in
different places and **no document citing both.**

## One dword, written by the menu and read as a handle

```asm
; BattleMenu_UpdateCommandSelectionAndDispatch — the only writer among the documented pair
0027812E  mov  word ptr [rsi + 0xde], dx
00278135  mov  dword ptr [r15 + 0x2fe0], edi
0027813C  call 0x0028F800
00278146  call 0x00296AF0                  ; the same value passed on

; the force-fight reader
00276FC5  mov  ecx, dword ptr [rdi + 0x2fe0]
00276FCB  call 0x002732E0                  ; -> an object pointer
00276FD8  test dword ptr [rdi + 0x2ff0], 0x4000
```

> **In both readers the field is not used as a number — it is handed straight to a resolver.** The menu
> **writes** it and immediately passes the same register onward; force-fight **reads** it and resolves
> it before doing anything else.

**Nine of the fourteen sites are in the menu dispatcher and only one of those is a write**, so **the
menu reads its own published selection far more often than it changes it.** *(Anchored 2026-09-30, SWE2-DATA: `_index/candidates/dd-data-3-0930/ui_2fe0_sites.py` S1 lists the fourteen. `002778C0` reads at `00277CD8`, `00278022`, `002782B5`, `00278870`, `002789DD`, `00278F72`, `002793B3` and `00279CB3`, and writes at `00278135`; `00279E20` writes at `0027A5A1` and reads at `0027A5C9`, `0027A647` and `0027A6D8`; `00276D30` reads at `00276FC5`. The census covers these three functions.)*

**A third function** (`00279E20`, undocumented) **also writes it and then reads it three times** — so
**the menu dispatcher is not the only writer**, and the field is not owned by one screen. *(Anchored 2026-09-30, SWE2-DATA: `00279E20` is the handler of a `0x61F0`-byte parent that builds its `0x3010`-byte children in place at `+0xC0` with handler `00276D30` (`0027A402`, `0027A42D`), and its write stores the parent's `+0x61BC` into each child's `+0x2FE0` (`0027A59B`–`0027A5A1`; [the widget-constructor page](Widget-Object-Model/the-widget-constructor-and-object-sizes.md) §3). The third writer seeds the selection when the menu is built.)*

## What the pair shows that neither function does

**Force-fight has a document. The menu dispatcher has two.** *None of the three mentions this field.*

> **From inside the menu it looks like a scratch variable; from inside force-fight it looks like an
> input that arrives from somewhere.** **The channel is only visible from the address.**

**And a neighbouring flags dword is tested immediately after the resolve** — `+0x2FF0` against
`0x4000` — so **the selection and a condition on it live sixteen bytes apart** and are read together.

## The reader `00276D30`, decoded (SWE2-FRONTIER, switch-families package)

The "force-fight reader" above is the **battle-menu widget's 53-id message procedure**
(2849 B): `msg+0` id − 1 bounded `≤ 0x34` dispatches through a byte map (`00277880`) into RVA
table `00277854`, site `00276D79`); ten ids carry real arms and the remaining 43 share
the `00277828` default tail. The `+0x2FE0` read at `00276FC5` sits in the **id-2 arm**, which
is ~~the command-confirm path~~ the menu's per-frame message-2 arm (`00276D30+0x270`) *(corrected 2026-10-02, OPUS: message 2 is the generation reconcile, `00248030+0xBF`, which reaches every widget once `00250540+0x4D` has flipped the parity for the pass)*:

```
00276FA0  001EDEC0([+0xB4]) gate → +0x2FF0 bit 8 early-out →
          resolve +0x2FE0 via 002732E0 → r12
          00253BA0()  force-fight effective flag → r14d
          +0x2FF0 & 0x4000 → cmovne forces r14d = 1
          00254500() / 00254550(+0x2FF0 low byte) / 002878A0() / 00228480() gates
          r12 byte & 9 gate → +0x2FF0 bit 0x11 veto
          accept:  or dword [+0x2FF0], 0x200           (0027704E)
```

The other nine handled ids:

| msg id | arm | calls |
|---|---|---|
| 1 | `00276D85` | `00247570` (string arg), `00245000`, `00244960`, `00247930` — init |
| 4 | `00277329` | `002D8BB0`, `0029F5D0` ×5, `00229DF0`, `00229E70` — the largest arm (~1.2 KB) |
| 6 | `00276E14` | leaf (17 B) |
| 15 | `00276E25` | `00368A50`, `00290CD0` ×2, `003C94F0` ×2, `0035C080`, `002907F0`, `00275440` |
| 18 | `00276F27` | `0028F800`, `00296B80`, `00275440` ×2 |
| 21 | `00276EEA` | indirect `call rax` — a vtable-style call |
| 39 | `002770AB` | `00275440`, `0035BB50`, `0035C430`, `0020E620` |
| 46 | `0027780D` | leaf (27 B) |
| 53 | `00277058` | `00244F00` — mark-delete |

The per-helper bodies inside the arms are named by call site only — not read in this pass.

## Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Is `+0x2FE0` a handle or a plain integer? | **Both readers pass it to a resolver as the first argument before using it.** Its numeric value is never compared or arithmetic'd at these sites. |
| Is the menu the owner? | **No** — a third function writes it too. **Two writers, three readers, one field.** |
| Do the three functions hold the same object type? | ~~**Not established.**~~ The displacement and width agree across all fourteen sites; ~~**no site was found that converts between the bases.**~~ *(Corrected 2026-09-30, SWE2-DATA: yes, one `0x3010`-byte command-menu widget. `00276D30` is its handler and reads its own `+0x2FE0`. `00279E20` writes it on each child it builds. `002778C0` is the handler of the `0x2DC0`-byte widget that `00276D30` builds in place at its own `+0x220` (`00276DC0`–`00276DE6`), and it reaches `+0x2FE0` through `[widget+0xD0]` (`002778EF`), which its id-1 arm fills from the construction message with the parent's pointer (`00277925`–`00277931`). Control `_index/candidates/dd-data-3-0930/ui_2fe0_sites.py` S3, S4.)* |
| Could the write at `00278135` be initialising rather than publishing? | It stores a register that is **passed to the next call unchanged**, so the value is live at the write, not a reset. |

**What this document does not claim:** what `002732E0` resolves the handle to, what `0028F800` and
`00296AF0` do with it, what `+0x2FF0` bit `0x4000` means, or what the third writer is for.
*(Reconciled 2026-09-30, SWE2-DATA: `002732E0` is the four-slot find. It returns the record among `0035BB20(0..3)` whose `+4` equals the handle ([the layout-parameter page](Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md), EC7-76). `0028F800` returns `[[0209BE80] + 0x10F78]` and does not take the handle; `00296AF0` is the resolve-and-flag both writers call ([the gil page](../13-Rewards-Progression-Economy/gil-storage-clamp-and-every-path-that-moves-it.md), EC7-101). The third writer is the construction seed above. Still open: which records `0035BB20` returns, and so what the value names (`SD-124`), and what bit `0x4000` means (`SD-125`).)*

## The `002778C0` exclusive subtree — the dispatcher's 39 helpers (SWE2-FRONTIER, exclusive-subtrees package)

The exclusive-callee census assigns 39 frontier functions to
`BattleMenu_UpdateCommandSelectionAndDispatch`. All signature-swept 2026-09-15 (`bshape.py`):

| cluster | members | role |
|---|---|---|
| `0209BE80` singleton accessors | `0028EA20`, `0028EA90`, `0028FEA0` (`002BE020`), `00290470`, `00290520`, `00290590`, `002905B0`, `00290B70`, `00290C60`, `0028F9E0`, `002911D0` (324 B — also `002713B0`/`003F3580`/`00273A30`/`0024A5A0`/`003F3510`/`003F34D0`, plus `01E0C1E0`) | 17–38 B field getters/setters on the menu widget block at `0209BE80`; `002911D0` is the cluster's one real body |
| menu-state pair | `00272250`, `002722A0` (`00183280`), `00273850` | `00272180` + ~~the `01E0C1D8`/`01E0C1DC` state cells — menu-mode read/write~~ the screen width and height `01E0C1D8`/`01E0C1DC` — a projection to screen coordinates *(corrected 2026-10-02, OPUS: `00272250+0xE`–`00272250+0x3B` compute `((v − 0x8000) >> 4)` plus half the width or height)* |
| dispatch arms | `0027E050` (820 B — own jump table at `0027E384`; `0027E530` is a procedure it installs, see below), `0027B430` (`00275440` ×4 + `0027C730`/`0027D740`/`00244F00`/`00249C60`), `0027B880` (646 B — the heaviest arm: `0035D330`/`00290C60`/`00290C80`/`0028E840`/`003C93E0`/`0035C150` ×3–4 each), `0027C3D0` (717 B — `00311CD0` ×3 + `00241A50`/`00272EE0`/`00309B40`/`00311AF0`/`00273270`), `0027CD00` (`02AEDDB0` + `00273710`/`002713E0`/`002722A0`/`003678F0`/`00181630`/`002752E0`/`00368940`/`00368360`), `0027BED0` (`02AEDDB0` + `002E9D10` ×2 + `00203080`/`002703F0`/`00272250`/`00273850`), `0027C280`, `0027D330` (`002737B0`/`003588B0`/`00263C20`), `0027D480` (`0035D330`/`002B58B0`/`003EE8C0`, `01CEB638`), `0027DC10`, `0027DE30`, `0027BD80` | the per-command bodies behind the dispatcher's table — `02AEDDB0` (the camera/scene block) appears in two of them |
| icon/entry helpers | `003F3510` (`00275550`/`00272F30`), `003F34D0`, `003F3580`, `003F3660` (`00271140`), `00321060` (`003588B0`/`00263E30`/`0031AA30`), `003EEA00` (`0029CD00`, `00D11108`) | entry/icon resolution the arms call |
| leaves | `00273600`, `00274BA0`, `00274BD0` (`call rax` thunk), `002737B0` (`0035BB60` ×2/`0035BB00`), `00296570`, `00296ED0`, `002BE270` | small bodies, mostly single-purpose |

~~Not established: what object `0209BE80` is beyond "the battle-menu widget block".~~ *(Corrected 2026-09-30, SWE2-DATA: `0209BE80` is a pointer slot, not the block itself. `0028F8B0` allocates a `0x10FD0`-byte object through `00271420` and stores it there (`0028F8CA`–`0028F8D4`), and `0028F2F0` releases it and stores the slot again (`0028F554`). It is the singleton that [the per-frame update gate contract](../00-Engine-Core-Runtime/CONTRACT-per-frame-update-gate.md) maps.)*

**The jump table, walked 2026-09-18 (FABLE) — and the premise corrected.** `0027E050`'s table is at **`0027E384`** (`0027E085`–`0027E096`, ~~twenty dwords for command kinds 0–19~~ twenty dwords for kinds 1–20, indexed by kind − 1 at `0027E06B`; corrected 2026-09-27); `0027E530` is not a table but a 634-byte **procedure** that cases 15–18 install. Every case does the same three things to the battle-menu window: stores a **kind code** at `+0x4C0`, a **sub-selector** at `+0x4D4`, and a **sub-window procedure** into `[+0x1510]+0x120` (`0027E2F0`). ~~The pairing: kinds 0 and 2 → codes 6 and 9, procedure `00276BE0`; kind 1 → code 8, `0027D240`; kinds 3, 4, 5, 6, 7 → code `0xB` with sub-selectors 3, 7, 5, 6, `0xD`, and kinds 9–13 (sub-selector kind − 10 at `+0x4D8`), 14 (sub-selector 2) and 19 (sub-selector `0x14`) → code `0xB`, all `0027CE70`; kinds 15–18 → code from the four-entry table `01E0C394` (0, `0x10`, `0xD`, `0xF`) with the caller's word in `+0x4DC`, procedure `0027D5C0` when the code is `0xF` (kind 18) else `0027E530`; kind 8 → code `0x18`, `0027BC10`.~~ *Corrected 2026-09-27 (FABLE, Claude Opus 5.5): the pairing above was read by kind, but the index is kind − 1.* The pairing: kinds 1 and 3 → codes 6 and 9, procedure `00276BE0`; kind 2 → code 8, `0027D240`; kinds 4, 5, 6, 7, 8 → code `0xB` with sub-selectors 3, 7, 5, 6, `0xD`, and kinds 10–14 (sub-selector 1, with kind − 10 at `+0x4D8`), 15 (sub-selector 2) and 20 (sub-selector `0x14`) → code `0xB`, all `0027CE70`; kinds 16–19 → code from the four-entry table `01E0C394` (0, `0x10`, `0xD`, `0xF`) with the caller's word in `+0x4DC`, procedure `0027D5C0` when the code is `0xF` (kind 19) else `0027E530`; kind 9 → code `0x18`, `0027BC10`. The sub-selector is a battle command (class 21): kind 4 is the Items list, 5 Foecraft, 6 Summon, 7 Quickening, 8 Gambits ([UQ-68 record](../_index/candidates/uq68-kind5-foecraft/README.md)). The common tail copies the word `+0x153A` into `+0x4C4`, calls `BattleMenu_BuildCommandEntryList` `0031EB20` on `+0x4C0`, `0027BB70` for the `0027E530` path, `00250270`, and tail-calls `0027DED0(window, kind)` (`0027E37F`) — the window sizing from `menubtlwndinfo.bin` on [the five small bin tables](../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/five-small-bin-tables.md), UQ-68. So the `0027xxxx` arms in the table above (`0027B430`, `0027B880`, `0027C3D0`) are **not** this table's targets: the edge list shows all three, like `0027E050` itself, called by `BattleMenu_UpdateCommandSelectionAndDispatch` `002778C0`. Static: the table read from the image, every case block decoded.

## Template sections (SWE2-DATA, 2026-09-30)

**What the player sees.** When the player confirms a command in the battle menu, the selected entry is published as a handle in the command-menu widget, and the confirm path resolves it before it issues the command (the id-2 arm above).

**Key addresses.**

| address | what |
|---|---|
| `00276D30` | the command-menu widget's message procedure (`0x3010`-byte widget) |
| `002778C0` | the dispatcher widget's procedure (`0x2DC0` bytes, built at the menu widget's `+0x220`) |
| `00279E20` | the `0x61F0`-byte parent's procedure; builds the menu widgets and seeds `+0x2FE0` |
| `002732E0` | the four-slot find the confirm path resolves the handle with |
| `0209BE80` | the pointer slot of the `0x10FD0`-byte singleton |

**Data structure.**

```
command-menu widget (0x3010 B, handler 00276D30)
  +0x0220  the 0x2DC0-byte dispatcher widget (handler 002778C0), built in place; it ends at +0x2FE0
  +0x2FE0  u32  the published selection handle
  +0x2FF0  u32  flags: bit 8 early-out, 0x200 set on accept, 0x4000 = the dispatcher's open window is kind 1, the top command list (set by 002778C0's message-31 arm; the id-2 arm reads it as force-fight on)
dispatcher widget (0x2DC0 B, handler 002778C0)
  +0x00D0  pointer to the command-menu widget, from the construction message +8
parent (0x61F0 B, handler 00279E20)
  +0x00C0  the command-menu widgets, 0x3010 B each, built in place
  +0x61BC  the value seeded into each child's +0x2FE0
```

**Call chain.** `00279E20` → `00245000` (`0027A42D`) builds the menu widget → `00276D30` → `00245000` (`00276DE6`) builds the dispatcher widget → `002778C0`. Confirm: `00276D30` id 2 → `002732E0`.

**Modding notes.** The selection is one dword at `+0x2FE0` of the command-menu widget; a patch that changes what it names must keep `002732E0`'s match against the record `+4` in step.

**Evidence.**

| claim | evidence | tier |
|---|---|---|
| fourteen sites, writers and readers | `_index/candidates/dd-data-3-0930/ui_2fe0_sites.py` S1, C1 | 1 |
| one object type across the three functions | `ui_2fe0_sites.py` S3, S4, C2 | 1 |
| `0209BE80` is the singleton slot | `0028F8CA`–`0028F8D4`, `0028F554` | 1 |

**What is not known.**

- [x] Which records `0035BB20` returns for slots 0 to 3, and so what entity the `+0x2FE0` value names (`002732E0` matches it against their `+4`). **SD-124** (SWE2-DATA, 2026-09-30). *(Answered 2026-09-30, FABLE, [record](../_index/candidates/sd124-125-menu-fable-0930/README.md): `0035BB20(k)` returns `022C8080 + k x 0xC0` below the count `022C8064`: the k-th member slot the battle-menu walk `0035BC50` accepted, whose `+4` is the member's packed actor handle. The walk fills each slot through `00320040(2, k, slot)`, which resolves index k in slot-map class 2 (battle-state block `+0x5A6C`) through `BattleSlotMap_ResolveMappedBattleSlot` `0031B9F0` and admits a character id of at most `0x27` whose class-`0x17` check passes; class 2 is passed by no other constant site (`class2_census.py`, FAILS 0). So `+0x2FE0` names one of the up to four party characters in the battle command menu's member map.)*
- [x] What `+0x2FF0` bit `0x4000` means and who sets it: the confirm arm forces the force-fight flag to 1 when it is set. **SD-125** (SWE2-DATA, 2026-09-30). *(Narrowed 2026-09-30, FABLE for SWE2-DATA, on the [batch-3 review](../_index/candidates/auditsem-review-dd-owner-read-3-0930/REVIEW.md): the only writer of bit `0x4000` is `BattleMenu_UpdateCommandSelectionAndDispatch` `002778C0`: at `002795AE` it compares the message's first parameter with 1 (`r12` is the message pointer, the procedure's second argument from `002778EC`; `rdi` = 1 from ~~`00278A5B` /~~ `002791A7`, the only ~~definitions~~ definition reaching there *(struck 2026-09-30, FABLE: an instrument artefact - the 8-entry table at `00278D86` was read past its bound into `00279E04`)*), sets the bit when they are equal (`002795B5`) and clears it otherwise (`002795C2`); ~~the reaching paths are message arm 2 (GENERATION RECONCILE) and private arm 31~~ the reaching path is private arm 31 only *(struck 2026-09-30, FABLE: the arm-2 path was the same instrument artefact; `sd125_senders.py` P2, P5b)* (`sd125_reachdef.py`); ~~`00279E20` rewrites the whole dword at construction;~~ *(struck 2026-10-01, OPUS, on SWE2-AUDIT-SEM's N1, [review](../_index/candidates/auditsem-review-sd125-128-0930/REVIEW.md): `00279E20`'s stores there are merges plus a byte store; the bit starts clear because the constructor `002465F0` memsets the whole `0x3010`-byte object first, `00246626`, F3)* which sender passes parameter 1, and so the bit's meaning in play, is open.)* *(Answered 2026-09-30, FABLE, [record](../_index/candidates/sd125-sd128-fable-0930/README.md): bit `0x4000` = the dispatcher's open window is kind 1, the top command list (list code 6); set and cleared only by `002778C0`'s message-31 arm, the "open window kind k" message, by k = 1; sent by the controller `00279E20` when it opens the menu (kind = its word `+0x61B8`) and by the dispatcher itself (current kind, Back, next kind). ~~The menu's per-frame id-2 arm reads it as force-fight on, so while the party is fleeing the menu closes itself unless the top list is showing.~~)* *(Narrowed 2026-10-01, OPUS, on SWE2-AUDIT-SEM's C1, [review](../_index/candidates/auditsem-review-sd125-128-0930/REVIEW.md), which accepts the answer and completes the writer census, 72 `+0x2FF0` sites:)* In play: the menu's per-frame message-2 arm (`00276FA0`) treats a set bit as force-fight on (`00276FF2`). Once its `001EDEC0(menu+0xB4)` gate passes and `+0x2FF0` bit 8 is clear, an effective flag of 0 (FLEEING) with the bit clear closes the menu (`0027704E`: bit `0x200` + `00244F00`). With the bit set, the menu applies its ordinary not-fleeing close rules instead. So while fleeing, the command menu closes itself unless the top list is showing; on the top list it stays subject to the usual close conditions.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Status_Periodic_Terminal — CLIENT.** `BattleFormula_BuildRuntimeCounterPeriodicHpCredit` calls a cited function.
- **WorldAreaField - CLIENT and SERVICE (7 edges).** `00228480` is called by bodies filed to WorldAreaField: World_UpdateSimulationTick (`00314020`); `0022A770`, MainLoop_UpdateAndRenderFrame (`0022B8C0`), `0022BC20`, `002B7B80` (+2 more) reach bodies filed to WorldAreaField: FieldData_GetActiveFieldRecordBit15 (`00313F60`), World_UpdateSimulationTick (`00314020`), WorldTransition_GetActiveOrPendingFieldId (`003148F0`) - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - MECHANICAL (2 edges).** both edges are script-VM bodies (`0033F310`, `00357450`) calling `WorldTransition_GetActiveOrPendingFieldId` (`003148F0`) - accessor fan-in.
- **Spawn_Encounter_Lifecycle - MECHANICAL (3 edges).** all 3 edges are spawn-lifecycle bodies calling the shared accessors `00313F60`/`003148F0` - fan-in, not a per-caller relationship.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Combat — CLIENT.** `FUN_003206e0`, owned by that layer, calls `00263E30` on this page. That caller is a 176-byte routine behind the same `byte[02089340] & 0x10` gate, resolving through `003588B0`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatAI — CLIENT.** `BattleUnit_RebuildPerceptionCandidateCache`, owned by that layer, calls `00263E30` on this page. That caller is the cache re-form, and it fixes the block's size: when the generation check does not short-loop it, it **zeroes `0x208` bytes at `+0xBC0`** before refilling them; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatFormula — SERVICE.** `00309B40` on this page calls `BattleStats_GetByBattleSlotIndex`, owned by that layer. What it reaches is the 33-byte unmapped twin of the slot accessor: the index is rejected above `0x27` and the rest index `[02EBF190] + 8` at a stride of `0x1C8`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Party — CLIENT (10 edges through 7 of this page's functions).** The Party layer reaches this page at `00263E30`, `0022A770`, `0022B8C0`, `0022BC20` and 3 more. `BattleUnit_ResolveByFocusHandle` is the worked example, read in full - it is a 42-byte resolver gated on bit 4 of `byte[02089340]`: it takes the focus handle through `003588B0` and tail-jumps to `00263E30`; **3 of the 6 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Resource — SERVICE.** `002911D0` on this page calls `FUN_0024a5a0`, owned by that layer. What it reaches is a 75-byte walk of the entries at `0208F580`, testing bit 5 of `byte[+0x38]`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Presentation — CLIENT (SWE2-CONTRACT 2026-09-15, 50 edges).** The menu's published selection is consumed across
the render layer: `Presentation.TargetLine.Runtime` `00291320` reaches `0024A5A0`/`00271140`/
`00273A30`/`00275550` (4 edges); the input-consumer state machines `002BAF80`/`002B7B80` reach
`001EDEC0`/`00249C60`/`00275440`; `003F1A60`/`003F5100`/`003F6370`/`003F7200` share `00203080`/
`002703F0`/`002E9D10`; `00506700` shares `0024A5A0`/`002B58B0`/`0035D330`; `00183280` is reached by
`00559540`/`0057A1F0`/`00561BE0`/`003F1530`; ShaderMaterial `00366B80` shares `001EDEC0`/`0024A5A0`.
The selection is published precisely so these bodies can consume it — the crossing is the menu's
whole contract.

**Movement — MECHANICAL (SWE2-CONTRACT 2026-09-15, 36 edges).** All 36 edges are Movement bodies
(`PartyFollow_SolveFormation`, `0033C310`, `BattleLocomotion_SamplePointAlongCurrentPath`,
`BattleLocomotion_BuildSolverContext`, `BattleLocomotion_ResolveTargetSpacingAndAvoidance`,
`Navigation_CheckParallelClearanceRoutesXZ`, ~25 more) sharing `00203080`/`00263C20`/`00263E30`.
Pure shared-accessor fan-in.

**ActorEntity — CLIENT and SERVICE (SWE2-CONTRACT 2026-09-15, 25 edges).** Six of the page's subjects
(`002713E0`/`00272F30`/`00273270`/`0027D330`/`002E9D10`/`00321060`) call
`ActorHandle_ResolveRegistryEntryByPackedId` `003588B0` — the menu resolves the actor its selection
names; `0027D330`/`0031AA30` call `ActorRuntime_GetClassNibble` `00263C20`. The remaining ~15 edges
are ActorEntity bodies (`BattleGroup_RefreshFourActorDefinitions`, `ActorWork_GetBattleUnit`,
`ActorSystem_ReleaseBattleUnitSlotForActor`, `ActorEntity.StateInterpolation` `003F1E90`,
`RuntimeListMaintenance` `00400AC0`, …) sharing `00263E30`/`00263C20`/`002713E0`/`00275550`. The
handle-resolution calls are the real crossing; the callers are fan-in.

**CombatAction — SERVICE (SWE2-CONTRACT 2026-09-15, 11 edges).** `002778C0` and `0027C3D0` call
`BattleUnit_IssueCommandByFocusHandlesWithOptionalPartyFanout` and `BattleUnit_IssueCommandByFocusHandles`
— the published selection is issued as a command through these (4 edges); `00311CD0` shares
`002778C0`/`0027C3D0`; `BattleTarget_ClassifyRelationshipClass` shares `00263C20`;
`BattleUnit_HandleActorTimelineEvent`/`BattleUnit_HandleActionTimelineEvent`/`00317E60`/`00319090`/
`Battle_ProcessActionTargetEntry` share `00263E30`; `00328530` shares `0031AA30`. Selection-to-command
is the crossing this page exists for.

**Save_Load_Settings — MECHANICAL (SWE2-CONTRACT 2026-09-15, 9 edges).** `SaveLoad_ControllerLifecycleHandler`
shares `001EDEC0`/`00244960`/`003678F0` (3 edges); `SaveSlotScan_ControllerCallback`,
`SaveWrite_OperationStateCallback`, `SaveStorageQueue_ControllerStateHandler` share `00244960`;
`005819A0`/`SaveLoad_ControllerTransitionStateMachine`/`00581350` share `00249C60`. The save/load
controller drives the same widget helpers the menu uses — shared-widget fan-in.

**CoreRuntimeScheduling — MECHANICAL (SWE2-CONTRACT 2026-09-15, 9 edges).** `00276D30` calls `0020E620`/`00229DF0`/
`001EDEC0`/`00229E70`; `002878A0` is reached by `0022A770`/`0022BC20`/`0022B8C0`; `0031AA30` calls
`0020E600`. Frame-tick and fixup helpers.

## Interior citations for the entry-cited functions (OPUS, 2026-10-01)

*Functions this page named only at their entry. Each was read from the certified image; the sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Verified by [`menusel_interior.py`](../_index/candidates/opus-menusel-interior-1001/menusel_interior.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00272180` | 197 B | calls `00202C50(&v, rdx, r8)` with the matrix at `rdx` and the vector at `r8`, divides v's x, y and z by w = matrix floats `+0xC`, `+0x1C`, `+0x2C` dotted with the vector plus `+0x3C`, stores w as v's fourth float, calls `00862930(rcx, &v)` and returns 1.0 (`01CEBBA8`) divided by w | `002721AA`, `002721C5`, `002721F5`, `0027221F`, `00272223` |
| `00272250` | 68 B | calls `00272180`, then rewrites dword `+0` as ((value - 0x8000) >> 4) plus dword `01E0C1D8` >> 1 and dword `+4` as ((value - 0x8000) >> 4) plus dword `01E0C1DC` >> 1 (arithmetic shifts) | `00272259`, `00272269`, `00272277`, `0027227F`, `0027228B` |
| `002722A0` | 112 B | calls `00272180` and keeps its float result; rewrites dword `+0` as ((value - 0x8000) >> 4) plus ((int)(dword `01E0C1D8` as a float divided by `00183280()`) >> 1) and dword `+4` as ((value - 0x8000) >> 4) plus dword `01E0C1DC` >> 1; returns the kept float | `002722B3`, `002722C6`, `002722DF`, `002722FB`, `00272307` |
| `002737B0` | 74 B | returns 1 when `0035BB00(i)` equals `ecx` for some i below `0035BB60()`, else 0 | `002737BE`, `002737C9`, `002737CE`, `002737EA` |
| `00273850` | 33 B | returns 1 when `ecx` is in 0 to dword `01E0C1D8` - 1 and `edx` is in 0 to dword `01E0C1DC` - 1 (signed), else 0 | `00273852`, `00273858`, `00273860`, `00273868` |
| `00274BA0` | 45 B | appends the node `rdx` at the end of the chain linked through qword `+0x18` from `rcx`: clears `rdx`'s `+0x18`, points the last node's `+0x18` at it and stores the last node in `rdx`'s `+0x10` | `00274BB3`, `00274BBC`, `00274BC4`, `00274BC8` |
| `0027BC10` | 355 B | when dword `+0x500` is 0 or negative, sets qword `+0x1578` to `002F9860(0x7D2)`, byte `+0x90` of `rdx` to (int)(sinf(dword `0208F570` * 3.14159 / 30) * 32 + 96) (`01CEBC50`, `008F8D80`, `009159F8`, `00915BA0`; `00861F0E` jumps to the `sinf` import), word `+0x91` to 0x3030 and byte `+0x93` to 0x80, and tail-calls `002D8650(rdx, 0, 0, rcx + 0x1550)`. Otherwise, for entry `r8d` of the 8-byte entries at `+0x510`: sets word `+0x5A` of `rdx` to 0x40 when bit 0 of the entry's byte `+2` is set, else 0x80; sets qword `+0x1578` to `002F9860(0x404)` when the entry's word is 0xFFFF, else to `002B58B0(qword +0x18 of 0035D380(1, word), 0)` and, when word `+0x1538` equals that word, byte `+0x15EF` to 6; calls `002D8650` the same way, then restores byte `+0x15EF` and word `+0x5A` | `0027BC1A`, `0027BC58`, `0027BC91`, `0027BCDF`, `0027BD33` |
| `0027BD80` | 91 B | calls `0031AB80(rcx, 0, dx, &rec)` and returns float `+0x10` of rec when the call is not negative and rec's dword `+8` is 1, else 0.0 | `0027BD97`, `0027BD9E`, `0027BDBC`, `0027BDC3` |
| `0027D240` | 232 B | when dword `+0x500` is 0 or negative, sets qword `+0x1578` to `002F9860(0x7D2)` and byte `+0x90` of `rdx` to (int)(sinf(dword `0208F570` * 3.14159 / 30) * 32 + 96) (`01CEBC50`, `008F8D80`, `009159F8`, `00915BA0`; `00861F0E` jumps to the `sinf` import), word `+0x91` to 0x3030 and byte `+0x93` to 0x80. Otherwise, for entry `r8d` of the 8-byte entries at `+0x510`: sets word `+0x5A` of `rdx` to 0x40 when bit 1 of the entry's byte `+3` is set, else 0x80, and qword `+0x1578` to `002B58B0(qword +0x18 of 0035D330(k, the entry's word), 0)` with k = 0x18 when bit 2 of byte `+3` is set, else 0x15. Both paths tail-call `002D8650(rdx, 0, 0, rcx + 0x1550)` | `0027D24A`, `0027D288`, `0027D2C7`, `0027D2F3`, `0027D323` |
| `0027D5C0` | 310 B | when dword `+0x500` is 0, sets qword `+0x1578` to `002F9860(0x7D1)`, byte `+0x90` of `rdx` to (int)(sinf(dword `0208F570` * 3.14159 / 30) * 32 + 96) (`01CEBC50`, `008F8D80`, `009159F8`, `00915BA0`; `00861F0E` jumps to the `sinf` import), word `+0x91` to 0x3030 and byte `+0x93` to 0x80, and tail-calls `002D8650(rdx, 0, 0, rcx + 0x1550)`. Otherwise, for entry `r8d` of the 8-byte entries at `+0x510`: calls `0031C5D0` on a stack record {2, the entry's dword}, sets word `+0x5A` of `rdx` to 0x40 when bit 1 of the entry's byte `+4` is set, sets qword `+0x1578` to `002B58B0(record qword +0x18, 0)`, calls `002D8650` the same way and restores word `+0x5A` | `0027D5CD`, `0027D5E5`, `0027D68E`, `0027D6B9`, `0027D6E1` |
| `0027E530` | 634 B | does nothing when bit 15 of dword `+0x1528` is set. When dword `+0x500` is 0 or negative, sets qword `+0x1578` to `002F9860(0x7D1)`, byte `+0x90` of `rdx` to (int)(sinf(dword `0208F570` * 3.14159 / 30) * 32 + 96) (`01CEBC50`, `008F8D80`, `009159F8`, `00915BA0`; `00861F0E` jumps to the `sinf` import), word `+0x91` to 0x3030 and byte `+0x93` to 0x80, and calls `002D8650(rdx, 0, 0, rcx + 0x1550)`. Otherwise, for entry `r8d` of the 8-byte entries at `+0x510`: sets word `+0x5A` of `rdx` to 0x40 when bit 1 of the entry's byte `+4` is set, sets qword `+0x1578` to `00272CB0(the entry's dword)` and calls `002D8650`; when n = `00272C80(the entry's dword)` is positive, formats n into a stack buffer with `0024ABE0(buf, 0x20, n, 0)`, points `+0x1578` at the buffer (one byte in when `00254A10()` is 0), measures text with `0029CD00` and draws with `002D8690`. Every path restores word `+0x5A` and zeroes dword `+0x159C` | `0027E54B`, `0027E59E`, `0027E626`, `0027E650`, `0027E765` |
| `0028EA20` | 17 B | tail-calls `002911D0(qword 0209BE80, ecx, r8, edx)` | `0028EA23`, `0028EA25`, `0028EA2C` |
| `0028F9E0` | 22 B | returns 1 when word `+0x850` at the zero-extended low dword of `rcx` is 1 or 2, else 0 | `0028F9E2`, `0028F9EB`, `0028F9F2` |
| `0028FEA0` | 88 B | returns 0 when qword `0209BE80` is null; otherwise calls `002BE020` on `[0209BE80] + 0x8FA0` and tail-calls `002BE1A0(that, ecx, 0, edx)` | `0028FEAE`, `0028FEC7`, `0028FECE`, `0028FEF3` |
| `00290520` | 28 B | returns 3 when qword `+0x10F78` of `[0209BE80]` is null, else tail-jumps to `00296570` on it | `00290527`, `00290533`, `00290537` |
| `002905B0` | 38 B | tail-jumps to `002969D0(qword +0x10F78 of [0209BE80], ecx)` when that qword is non-null, else returns | `002905B7`, `002905B9`, `002905C3` |
| `00290B70` | 25 B | sets word `+0x850` at the zero-extended low dword of `rcx` to 3 when it is 2 | `00290B72`, `00290B81` |
| `00290C60` | 27 B | when qword `0209BE80` is non-null, tail-jumps to `002BE270(it + 0x8FA0, ecx)` | `00290C62`, `00290C6E`, `00290C75` |
| `00296570` | 16 B | returns byte `+0xB43`, or 0 when `rcx` is null | `00296575`, `00296578` |
| `00296ED0` | 115 B | for a non-null `rcx`: when bit 8 of word `+0xB4A` is set and `edx` is 0, clears bits 0-2 and 7 of word `+0x318 + 0x160*i` for each i below byte `+0xB42`; then clears bit 8 of `+0xB4A` and sets it again when `edx` is non-zero | `00296EDE`, `00296F05`, `00296F24`, `00296F3B` |
| `00321060` | 118 B | when bit 4 of byte `02089340` is set and `00263E30(003588B0(ecx))` is non-null, calls `0031AA30(it, 0, word +0x714, &rec)`, stores rec's dwords `+0` and `+4` through `rdx` and `r8` when they are non-null, and returns that call's result; otherwise returns -1 | `0032106A`, `00321086`, `003210A2`, `003210B0`, `003210C8` |
| `00357450` | 36 B | tail-calls `0026B4E0(rcx, 00264F90(003148F0(rcx)))` | `00357459`, `00357460`, `0035746F` |
| `003F34D0` | 56 B | appends the node `rdx` at the end of the chain linked through qword `+0x70` from `rcx`, storing the previous last node in `rdx`'s `+0x78`, and returns `rcx`; with `rcx` null returns `rdx` | `003F34D8`, `003F34F3`, `003F34FC`, `003F3503` |
| `003F3510` | 107 B | calls `00275550(rcx, 0x80, r8, r9)`, stores the sixth (float) argument in float `+0x64`, the fifth in dword `+0x6C` and `00272F30(fifth)` in float `+0x60`, then tail-calls `003F3660(rcx, rdx, r9d, r8)` | `003F3535`, `003F3544`, `003F3549`, `003F354C`, `003F3576` |
| `003F3580` | 26 B | returns the first node on the chain linked through qword `+0x70` from `rcx` whose dword `+0x6C` equals `edx`, or 0 | `003F3585`, `003F358A`, `003F3593`, `003F3596` |
| `003F3660` | 169 B | sets bit 0 of dword `+0x50`, stores `r8d` in dword `+0x48` and `rdx` in qword `+0x40`; calls `00271140(&v, r9, qword [rdx+0x30] + ((2*r8d sign-extended) << 37))` and stores v's floats `+8`, `+0xC`, `+0`, `+4` in floats `+0x20`, `+0x24`, `+0x28`, `+0x2C`; zeroes dword `+0x4C` and sets floats `+0x10`, `+0x14`, `+0x18` to 255.0, `+0x1C` to 127.0 and `+0x30` to 0.25 | `003F3675`, `003F3690`, `003F369B`, `003F36AC`, `003F36D3` |
| `003F6370` | 592 B | when dwords `+0x810` and `+0x814` are non-zero and `003588B0` finds them, calls `002EA160(found, rcx + 0x10)` and `002EA0E0(found, rcx)`; combines the vectors at `+0` and `+0x10` with `00203080` and, when `002703F0` of the result is at least 1.0 (`01CEBBA8`), passes it through `00202DE0` and `00203030`, otherwise copies it to `022D9240` and `022D9260`, 1.0 to `022D925C` and three stack floats to `022D9250`-`022D9258`; after `00202B10` adds (2.0 minus floats `+0x820` and `+0x824`) times 0.75 plus 1.5 to its y (`01CEBC08`, `00901B3C`, `01CEBB70`); stores `00270F50(rcx + 0x240, ..., 3)` in dword `+0x7E0`, interpolates between the 16-byte entries `rcx + 0x240 + 16*(i-1)` and `+ 16*i` (i from (1.0 minus float `+0x838`) times the count minus one, each clamped) into `+0x1C0` with `00275490`, and adds 0.25 (`01CEBB68`) to float `+0x1C4` | `003F63B2`, `003F6400`, `003F648E`, `003F6512`, `003F6580` |

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../_index/candidates/opus-the-selection-the-menu-publishes-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00203030` | 77 B | multiplies each of the four floats at `rdx` `+0`..`+0xC` by the float third argument `xmm2`, stores the four products as one 16-byte block at `rcx`, then overwrites float `+0xC` of `rcx` with the unscaled float `+0xC` of `rdx` | `0020303A`, `00203050`, `0020306B`, `0020306E`, `00203073` |

## Homed bodies re-homed here for host fit (FABLE, 2026-10-03; move drafted by OPUS)

*Each body below was homed on another page by FABLE's homing stream (cloud-drafted, FABLE-verified). SWE2-AUDIT-SPEC reviewed its sentence, site and anchors exact, and rejected only the host: that page cites the caller as a foreign or boundary mention (commit `4522aeff6`). The row is moved here because this page cites the caller in its own text. The sentence is unchanged except where `moves.json` records a bits-as-values edit. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Verified by [`move_rows.py`](../_index/candidates/opus-fable-home-host-moves-1003/move_rows.py): every site transfers to its function, this page cites the caller outside this section, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors | moved from |
|---|---|---|---|---|---|
| `00273800` | 78 B | `0035BC50` + 0x375 | issues the call at `00273800` + 0x12 for indices 0 to 3 and, at the first non-null result whose dword `+4` equals `ecx`, returns 1 when bit `0x8` of that record's byte `+0` is clear and 0 when it is set; when no index matches it returns 0 | Interior anchor `00273812`; Interior anchor `0027381C`; Interior anchor `00273823`; Interior anchor `00273828`; Interior anchor `00273845` | [CONTRACT-the-five-parallel-slot-maps](../11-Party/CONTRACT-the-five-parallel-slot-maps.md) |

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-03, cloud-drafted)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../_index/candidates/fable-home-the-selection-the-menu-publishes-1003/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
| `0039C100` | 18 B | `0027E530` + 0x188 | reads the sign-extended dword `02AEE894` and returns the dword at index that value of the dword array at `02AEE898` (`02AEE898 + value*4`), with no bounds check | Interior anchor `0039C107`; Interior anchor `0039C10E` |
| `0039C120` | 36 B | `0027E530` + 0x196 | clamps `ecx` to the range 1 to 0x1A (signed: values below 1 become 1, values above 0x1A become 0x1A) and returns the dword at index `clamped - 1` of the dword array at `02AEE898` | Interior anchor `0039C127`; Interior anchor `0039C131`; Interior anchor `0039C134`; Interior anchor `0039C140` |
