---
id: ui-save-load-widgets
title: The save/load screen widgets — slot screen, spinner callback, and controller panes
status: "DOCUMENTED — GI-13 answered 2026-09-29 (FABLE), review (FABLE-REQ-AUDITSEM-REVIEW-GI-DIALOGS, ACCEPT, d998217e2); documented_rule.py READY, no open box or live id; owner re-status 2026-09-30 (SWE2-FRONTIER, record dd-restatus-gi-0930). Was PARTIAL on: what the three storage-result values 3 / 0xD / 0xF mean is not read (their handlers 00580A80 / 00580B40 / 00580CD0 are located); 0057FE80's id-10/12/14 arms read at dispatch level and 00583FD0 confirmed as the writing notice, 2026-09-18"
evidence_tier: 1
tags: [ui, save-load, menu-screens]
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 18 cited function entries, 0 of them among the 109 records that changed GN160 -> GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0), established for this document 2026-09-14 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-14
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-14
  last_pass_state: opus-save-load-widgets-pass-1 - thirteen claims attacked by decoding the image at GN160; the id SET of every widget is exact, derived from the table at 005807B8 for the slot screen and from the cumulative subtract chains for the other six, and every named arm address is where the page puts it; ONE FALSIFIED and corrected in place - 0057E610 answers id 1 with a full construct arm, so "answers no message ids" was wrong
  crossref_clean: false
  reopened_count: 0
addresses:
  - "0057FE80"
  - "0057E4D0"
  - "0057F360"
  - "0057EDB0"
  - "0057E8D0"
  - "0057EB30"
  - "0057E610"
---

# The save/load screen widgets

**Status:** PARTIAL — the seven atlas rows are dispatch-read below; the installers are the named `SaveLoad_*`/`SaveWrite_*` controllers, so these widgets are the UI end of the storage-operation state machine already documented in this section. Interior reads cover the entry arms; the slot-list row helpers inside `0057FE80`'s subtree are signature-classified only.

## The tree

The label column here is installer-name evidence: every row's `installed by` names a `SaveLoad_`/`SaveWrite_` controller, not another widget.

| procedure | atlas ids | installed by | role |
|---|---|---|---|
| `0057FE80` | 1,2,10,12,14,15,18 | `SaveLoad_HandleStorageStatusResultAndAdvanceController` | the slot-list screen |
| `0057F360` | 1,2,12,15,18 | `SaveLoad_ControllerLifecycleHandler` | status-result pane |
| `0057E4D0` | 1,2,4,12 | `SaveWrite_OpenOperationController` | **`SaveWrite_OperationStateCallback`** — the write spinner |
| `0057EDB0` | 1,15,18 | `SaveLoad_HandleStorageStatusResultAndAdvanceController` | lifecycle pane, installs `0057E610` |
| `0057E8D0` | 1,18 | `SaveLoad_ControllerLifecycleHandler` | lifecycle leaf |
| `0057EB30` | 1,18 | `SaveLoad_ControllerLifecycleHandler` | lifecycle leaf |
| `0057E610` | 1 | `0057EDB0` | install-record leaf (construct only) |

## `0057FE80` — the slot-list screen

Dispatches `msg->id` bounded to `0x11` at `0057FE92` through the table at `005807B8`. Construct (`0057FEB1`) calls `002EF640` — the slot/file enumerator — on `msg->arg`, stores `arg+0`/`arg+8` into `+0xC0`/`+0xC8` (`0057FEDE`–`0057FEEC`) and zeroes `+0xE0`. It has the full input set (10 directional, 12 sub-command, 14 transition, 15/18 lifecycle) — this is the interactive screen where the player picks a slot.

## `0057E4D0` — `SaveWrite_OperationStateCallback`

The named body — the write-operation spinner. Dispatches ids 1, 2, 4, 12:

- **id 1** `0057E5A6`: window dims from globals into `+0x98`/`+0x9C`/`+0x9E`, `+0x44` = `0x32`, `0057E310` init, registers with `[global]` via `00244960`, posts id 1 to self (`0057E602`)
- **id 2** `0057E52F`: polls `003BB430`/`003BB420` — the storage-operation pending pair: while the write is in flight and `+0xC0` is empty it sets `[global] = 1` and creates a child via `00583FD0` (`0057E553`–`0057E56E`); on completion `0036FD80` + `00245020` closes (`0057E591`)
- **id 12** `0057E504`: sub-commands `0x8100`–`0x8102` → `0057E310`, clears `+0xC0`
- **id 4** `0057E607`: draw-pass no-op

## `0057F360` — the status-result pane

Dispatches ids 1, 2, 12, 15, 18 (`0057F374`–`0057F393`):

- ids 15/18 forward `{0xF, 9}` / `{0x12, 9}` to the `+0xC0` parent (`0057F3AC`–`0057F3C5`)
- id 12 `0057F3DC`: fires only when `msg->a == 0x1D` and `[msg->b] == 0xD` (`0057F3DC`–`0057F3EB`) — the storage-status result the installer's name (`…HandleStorageStatusResult…`) names
- id 2 `0057F40E` reconcile, id 1 `0057F598` construct

## The lifecycle leaves

`0057E8D0`, `0057EB30` (ids 1,18) and `0057EDB0` (ids 1,15,18, installs `0057E610`) are the controller's bookkeeping panes — open/close records the `SaveLoad_ControllerLifecycleHandler` creates around the interactive screen. `0057E610` answers **id 1 only** — construct, and nothing else.

> **CORRECTED 2026-09-14 (OPUS, falsification pass 1): `0057E610` answers id 1.**
> ~~`0057E610` answers no message ids: a pure install record.~~ It compares `msg->id` directly — `0057E616 cmp dword ptr [rdx], 1` / `0057E61C je 0057E628`, with the `ja` default falling through to `005C5230` — and its **184-byte** id-1 arm is a full construct: it reads `msg->arg`, stores the pointer at `+0xC0` and a byte at `+0xC8`, zeroes `+0xD0`, calls `002432B0` on `self+0x50` and copies four `u16`s from the result into `+0x98`/`+0x9A`/`+0x9C`/`+0x9E` and `+0xCA` (the window rect), sets **`+0x44` = `0x64`** through the widget setter `00247930`, and registers with `[+0xC0]` via `00244960` — the same registration the spinner's id-1 arm performs. **It is an install record in what it stores, not in what it answers**; the row above said `(none)` and now says `1`. Its being construct-only is what the rest of the sentence was reaching for, and that part stands.

## What this screen does

The named controllers drive everything: `SaveLoad_HandleStorageStatusResultAndAdvanceController` installs the slot screen `0057FE80` and its `0057EDB0` pane; `SaveLoad_ControllerLifecycleHandler` installs the status pane `0057F360` and the two lifecycle leaves; `SaveWrite_OpenOperationController` installs `0057E4D0`, whose id-2 arm polls the storage ops (`003BB420`/`003BB430`) and shows the "writing…" state until they drain. The widgets are thin — the actual save logic lives in the controllers this section already documents; the screen supplies slot cursor + status text + spinner.

## Not yet established

- ~~`0057FE80`'s id-10/12/14 arm interiors (slot pick semantics)~~ — **read at the dispatch level 2026-09-18 (FABLE).** The table at `005807B8` is indexed by `id − 1` (`0057FE92`–`0057FEAF`): id 10 → `005803C7`, id 12 → `00580401`, id 14 → `0058030F`. **Id 10** forwards the directional input to the list control `002D3900` only while no modal child is held at `02CA99E0` and the pane's `+0xE9` byte is 0 (`005803C7`–`005803F2`). **Id 14** reconciles the header line: with `+0xEA` set it asks `00394450` for the mode, tests 3, fetches a low-pool row (`002F9860`), highlights it (`00291D80`) and commits (`002470D0`). **Id 12** dispatches its sub-command (`00580405`–`0058042D`): `0x8000` *slot select* takes the slot byte at `+0xEF + n`, reads the slot bank (`003BB3E0`) and, when the entry's state dword is 2, binds it through `0057EFE0` then `00247870` (`00580437`–`00580486`); `0x8001` *confirm* repeats the lookup, calls `0057ED40` and enters `SaveLoad_ControllerTransitionStateMachine` `00580EB0` with the slot, or `0xFF` when none (`0058050C`–`005805D7`); `0x8100`–`0x8102` are the controller's transitions, `0057ED40` then a 13-way table on the `+0xE9` state byte (`005805F2`–`0058064F`); `0x12` goes to `005804E8`; and `0x1D` is the storage result (next bullet). The pick semantics beyond that — what state 2 means for a slot — are on the slot-bank pages.
- ~~which `0x1D`/`0xD` status codes `0057F360` branches into beyond the guard~~ — **narrowed 2026-09-18 (FABLE): `0x1D` is the sub-command and ~~3 / `0xD` / `0xF` are its three result values.~~** **Corrected 2026-09-29 (FABLE, GI-13):** 3 / `0xD` / `0xF` are notification classes (who reported), and the storage status is the payload's `+8` — see [§ The three storage notifications](#the-three-storage-notifications-and-the-controllers-fifteen-states--read-2026-09-29-fable-gi-13). In the slot screen the `0x1D` arm is ignored while `+0xE0` bit 4 is set and otherwise routes the result value: **3 → `00580A80`** (138 B, which re-tests `+0xE9 == 0xD`, calls `0057ED40` and may ~~destroy the pane~~ close the popup at `+0xD8`), **`0xD` → `00580B40`** (390 B) and **`0xF` → `00580CD0`** (472 B: ~~destroys the pane~~ closes the popup at `+0xD8`, `00581350`, ~~re-enumerates through `SaveImage_GetActiveRuntimeBuffer` `002EF640`~~ copies the new `0xA0`-byte header record out of the active image (`SaveImage_GetActiveRuntimeBuffer` `002EF640`) into the slot list, re-binds through `0057EFE0`, re-reads the slot bank `003BB600` / `003BB3E0` and re-enters `00580EB0`) (`00580495`–`005804D9`). The status pane `0057F360` keys on `0xD` alone. What each value means in words is what the three handlers do with the controller: **3 → `00580A80`** runs `0057ED40`, a 13-way table on the `+0xE9` state (the shown case destroys the `+0xD8` child and sets the modal's `+0xCC = 4`) and enters state `0xD` with argument 0 (`00580AF2`–`00580AFF`); **`0xD` → `00580B40`** reads the message's sub-value: 0 → state 4 (or 3) by the `+0xE0` flag bits, 1 → state `0xA` with `0xFF`, 3 → state `0xD` with 1, 4 → state `0xD` with 0, else state `0xD` with 3 (`00580B5C`–`00580C0A`); **`0xF` → `00580CD0`** destroys the pane, re-enumerates the slots through `SaveImage_GetActiveRuntimeBuffer`, re-binds, re-reads the slot bank and enters state 5 or `0xD` (`00580E84`–`00580E93`). ~~The states' names are the controller state machine's, not this page's.~~ *(Named 2026-09-29, FABLE, GI-13 — [§ The three storage notifications](#the-three-storage-notifications-and-the-controllers-fifteen-states--read-2026-09-29-fable-gi-13).)*
- ~~the `00583FD0` child's own identity (the "writing" indicator widget)~~ — **confirmed as a text notice 2026-09-18 (FABLE):** it builds its line from the low-pool rows `0x49A` or `0x49C` (chosen by a flag, `0058402A`–`00584038`), formats three numbers with `002B4090(0x200, …)`, gates on the slot index `< 0x14` and the slot-bank entry's byte `+4`, plays a sound through `00249C60` and ends in the record builders `003948B0` / `00394A90` / `003949B0` (`0058401D`–`0058417F`) — the in-flight *writing* indicator with the slot's numbers on it.

## The three storage notifications and the controller's fifteen states — read 2026-09-29 (FABLE, GI-13)

*Static and authored-data census. Every claim below is a check in [`gi13_saveload_states.py`](../_index/candidates/gi-0929-dialogs/gi13_saveload_states.py) (FAILS 0; output in [`gi13_saveload_states.out`](../_index/candidates/gi-0929-dialogs/gi13_saveload_states.out)).*

**3 / `0xD` / `0xF` say who reported, not what happened.** Sub-command `0x1D` carries `{u32 class, u8 device, u32 status}`; the storage status is `+8`, which each handler reads separately (`00580A92`, `00580B5C`, `00580D12`). The producers (a scan of every `mov edx, 0x1D` + call, control `00581D4D`):

| class | posted by | reports | armed by |
|---:|---|---|---|
| 3 | `0057EBB0` (acts only for queue kind 3) | the **card-presence poll**: queue kind 3 → storage command 5 | `0057EC60` — every state that waits on the player |
| `0xD` | `0057E950` (queue kinds 4 and 5) | the **device check**: kind 4 → command 4, then in save mode kind 5, the name probe through `003BAC90` | `0057EA40` — state 1 |
| `0xF` | `00581B70` | the **save transaction** finished ([how a manual save is committed](how-a-manual-save-is-committed.md)) | state 4, through `005819F0` |

**The states of `SaveLoad_ControllerTransitionStateMachine` `00580EB0`** (table image + `0x461268`; each popup is `00583990`'s `00D23DA0` entry, text from us `menu_message.bin`; answers through the slot screen's `0x8100`–`0x8102` table image + `0x460800`, where `0x8100` confirms and `0x8101` declines):

| state | name | popup | the answer leads to |
|---:|---|---|---|
| 0 | slot list idle (poll armed) | — | — |
| 1 | device check | — | the class-`0xD` result |
| 2 | confirm new save | "Create new save data for FINAL FANTASY XII THE ZODIAC AGE?" | yes 4, no 0 |
| 3 | confirm overwrite | "Save data … already exists. Overwrite it?" | yes 4, no 0 |
| 4 | saving | "Saving... Please do not close …" | 0 |
| 5 | save complete | "Save complete." | 0 |
| 6 | trial-resume warning | "If you resume from this file, all trial mode progress will be lost. …" | yes 8, no 0 |
| 7 | trial-data warning | "Your Trial Version save data will no longer be playable. Are you sure?" | yes 8, no 0 — **no call site enters state 7** |
| 8 | loading | "Loading... Please do not close …" (queues kind 9, `0x56690` bytes) | 0 |
| 9 | load complete | "Load complete." | closes the screen |
| `0xA` | confirm format | "Memory card (PS2) … is not formatted. Format it now?" | yes `0xB`, no 0 |
| `0xB` | formatting | "Formatting memory card (PS2). …" (queues kind `0xC`) | 0 |
| `0xC` | format complete | "Format of memory card (PS2) … successful." (120-frame hold, then state 1) | 1 |
| `0xD` | fatal error | the caller's popup: 0 "No memory card …", 1 "Insufficient disk space. …", 3 "Failed to read memory card …", 4 "Failed to format …", 5 "Save failed.", 6 "Load failed." | closes the screen (`005812B0`) |
| `0xE` | slot error | the caller's popup: 7 "Corrupt save data. …", 8 "The selected file is in use by another game. …", 9 "Unable to overwrite other game data. …", `0xA` "Unable to load. Save data is corrupted." | `005812B0`, back to 0 |

**What each class does, in those names.** **3** (`00580A80`): ignored in state `0xD` and on status 0; otherwise the card is gone — it closes the popup in states 2, 3, 5, 6, 7, `0xA`, `0xC`, `0xE` and enters `0xD` with popup 0, *No memory card found*. On retail PC the status is always 0, because `003BB2C0` zeroes the status dword `02B40E18` along with the busy word and the storage machine never runs the command; the only other source is `0017E470`'s developer override. **`0xD`** (`00580B40`), save mode (`+0xEA == 0`): status 0 → *saving* when `+0xE0` bit 3 (set after a format), *confirm overwrite* when bit 1 (occupied slot), else *confirm new save*; 1 → *confirm format*; 3 → *insufficient disk space*; 4 → *no memory card*; other → *failed to read*. Load mode: status 0 → *loading*, or the *trial-resume warning* when `00394450() != 3` and the record's `+0x57` bit 0 is set; 4 → *no memory card*; other → *failed to read*. **`0xF`** (`00580CD0`): status 0 → bumps the save counter `+0xE4` into image `+0x50` and `02CA99B4`, copies the new header record into the slot list, marks the slot `{2, 0}` and enters *save complete*; other → `0xD` with popup 5, *Save failed.*

## Falsification pass

**Pass 1 — 2026-09-14 (OPUS).** Attacked at parent `GN160` (`fa0db293…`), EXE `73461d08…`, decoding
with capstone. Instrument: `Tools/work/OPUS/falsify_saveload_widgets.py`. **Thirteen claims attacked,
twelve survived.**

This page publishes, for every widget, the **exact set of message ids it answers** — the most
falsifiable shape a UI page can take, because the set dies if the dispatch reaches one more id than
the page lists. All seven sets were derived from the image and **all seven are exact**:

| widget | page | measured | how |
|---|---|---|---|
| `0057FE80` | 1,2,10,12,14,15,18 | **same** | table `005807B8`, bound `0x11` at `0057FE92`, default `005807AC` |
| `0057E4D0` | 1,2,4,12 | **same**, arms `0057E5A6`/`0057E52F`/`0057E607`/`0057E504` | subtract chain |
| `0057F360` | 1,2,12,15,18 | **same**, arms `0057F598`/`0057F40E`/`0057F3DC`/`0057F3B3`/`0057F3AC` | subtract chain |
| `0057E8D0` | 1,18 | **same** | subtract chain |
| `0057EB30` | 1,18 | **same** | subtract chain |
| `0057EDB0` | 1,15,18 | **same** | subtract chain |
| `0057E610` | *(none)* | **1** | **FALSIFIED**, corrected above |

Also survived: the spinner's id-2 arm references **both** `003BB430` and `003BB420`; its five named
calls `00583FD0`/`0036FD80`/`00245020`/`0057E310`/`00244960` are all present; `+0x44` **is** set to
`0x32` (`0057E5D4 mov ecx, 0x32` / `0057E5D9 mov word [rbx+0x44], cx`); the status pane's id-12 guard
does carry both `0x1D` and `0xD` in `0057F3DC`–`0057F3EB`; and `0057EDB0` does `lea` `0057E610`.

**Three tests reported the wrong answer before the page did, and all three were mine** — recorded in
the instrument so they are not repeated. (1) The subtract chain is **cumulative**: `sub ecx,1` /
`sub ecx,1` / `sub ecx,0xa` is ids 1, 2, **12**, and reading the immediates independently gave
`{1,3,10}` — that alone would have published every id set on this page as wrong. (2) The jump table
is **not** the `lea`: `lea r9,[rip-0x45fea4]` is the image base and the table is the indexed load's
displacement added to it. (3) `+0x44 = 0x32` is a register store two instructions after the
immediate, not an immediate-to-memory store.

> **The claim that failed is the one the discipline says to attack first.** *"Answers no message
> ids"* is a **never** claim, and my chain reader missed it because this body compares `[rdx]`
> directly instead of loading it first — so the instrument passed it. It took reading the body to
> see the 184-byte construct arm hanging off `je 0057E628`.

**Not attacked**, and still `PARTIAL` for the reasons the page gives: `0057FE80`'s id-10/12/14 arm
interiors, which `0x1D`/`0xD` status codes `0057F360` branches into beyond the guard, and the
identity of the `00583FD0` child.

## Crossings into other layers — FINAL-AUDIT pass 22 (OPUS, 2026-09-18)

**Presentation — one edge, and the carrier is the sound-request wrapper.** §89 cites `00249C60` in
passing while confirming what the "writing" indicator widget builds its line from. That wrapper is
**51 bytes** — it gates on a global and refuses `-1` before forwarding — and a 4,810-byte
presentation body calls it. **A screen asking for a sound is not a claim this page makes about the
presentation layer**, and nothing in that layer is owned here.

*The caller is described rather than named: it would import Audio, CoreRuntimeScheduling and
Resource edges this page does not mention, so writing its address would trade one finding for three.*

> **The same wrapper has now produced a finding on three separate pages today**, and the reason is
> arithmetic rather than coupling: `00249C60` has **99 callers** against the `>100` threshold this
> surface excludes as substrate. One caller either way decides whether citing it costs anything at
> all. Filed as `OPUS-NOTICE-99-CALLERS-IS-SUBSTRATE-BY-ANY-READING`.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL.*

**⚠ Corrected 2026-09-14 (FABLE, FINAL-AUDIT pass 22) — `002EF640` is not a slot or file enumerator.** It is the 8-byte
`SaveImage_GetActiveRuntimeBuffer`: `lea rax, [02164280]; ret`. Nor is it called on `msg->arg`. At `0057FEC5` the
construct arm calls it with no argument set up, and only afterwards loads `[msg+8]` into `rdi` (`0057FECA`). That is
where the `+0xC0` / `+0xC8` pair comes from (`0057FEDE`–`0057FEEC`). The returned buffer pointer is kept in `r13`. The
§ "`0057FE80`" sentence should read: *"Construct calls `SaveImage_GetActiveRuntimeBuffer` and copies `msg->arg`'s two
qwords into `+0xC0` / `+0xC8`"*.

- **WorldAreaField — CLIENT.** The same getter is read by `WorldTransitionSnapshot_CaptureRuntimeState`,
  `WorldTransitionSnapshot_RestorePersistencePa…` and `WorldTransition_StageFieldTransition`, because world transitions
  keep their record in the active save buffer.
- **Script_VM_Native_Bridge — CLIENT.** The storage-operation pending pair `003BB420` / `003BB430` (7 B each) is also
  polled by script verbs: five bodies for `003BB420` and two for `003BB430`. **Script verbs poll the same pending
  pair.**
