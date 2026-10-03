---
system: The quest list screen — the main-menu quest viewer, its procedure, its three shared pane children, and the
  load/teardown path
category: 16-UI
status: AUDITED — the +0x100 & 0x3C0 handshake (three pane-ready sub-commands plus the opening bit, then command 0xA) and the forwarded command numbers (unread by the child, one wake-up) resolved 2026-09-18; what each pane draws per row stays as prose residue
owner_layer: CodeDomain:UI (menu screens)
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN161 -> GN162 - REPLACED 2026-09-21 (OPUS), because the snapshot-identity basis this block carried is FALSE at GN162: this document cites record(s) 005771F0, which batch R30 touched. The weaker basis HOLDS and is measured: the advance changed 30 records in comment and tags ONLY - 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten (check_delta_additivity.py GN161 -> PARENT, control passed) - and check_stranded_absence.py, sweeping the GN160 resolved set which strictly CONTAINS all 30, reports no live absence claim on any line of this document
    verified: 52 cited function entries, 0 of them among the 109 records that changed GN160 -> GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0), established for this document 2026-09-14 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: 'procedure membership from the menu screen atlas (../Menu-Screen-Atlas/members/ui_atlas.tsv); every role
    below is read from the function body, not inferred from adjacency; message ids use the decoded dispatch of each
    procedure (../Widget-Object-Model/the-widget-message-protocol.md §4)'
last_reviewed: 2026-09-14
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-14
  last_pass_state: opus-quest-list-pass-1 - nine claims attacked by decoding the image at GN160 and ALL NINE SURVIVED. Both body sizes exact (758 B and 405 B), the dec/cmp 0x11/ja dispatch shape present in its published window, the rel32 table at 005774E8 with default 005774D9 and six live arms at the published addresses, the child's chain answering exactly 1/2/16/18 with the 005C5230 default, the factory called exactly three times, and the screen global claim landing exactly - [rip+0x27324c3] at 0057726E and [rip+0x2733d43] at 005759EE both resolve to 02CA9738. No correction
  crossref_clean: true
  reopened_count: 0
---

# The quest list screen

> **The quest list is one parent widget running three instances of one child pane procedure.** `005771F0` is the
> screen's message handler. On CONSTRUCT it creates three children of the same procedure `00575870` (the factory
> `00575810` passes each its pane index 0/1/2), loads the quest data and pane textures (`00576F50`), and from then on
> talks to the panes only by message records. The panes answer back through `00247510` with `{0x10, pane+3}` /
> `{0x12, pane}` records — the parent clears a child's slot itself only when the child announces its own destruction.

~~**PARTIAL.**~~ **AUDITED.** *(corrected 2026-10-02, OPUS: the front matter says `status: AUDITED`)* Read: the procedure tree, the parent's full message protocol, the child's state machine, and every
subtree member's role with an interior citation. Not read: what each pane draws per row, and the meaning of the
command numbers forwarded to the children (`005770A0` commands 2, 4, 5, 6, 0xA are named by call site, not decoded).

## 1. What the player sees

The clan-primer / quest list in the main menu — the list of accepted hunts and side quests, organised into panes.

## 2. The procedure tree

Atlas rows labelled `quest list` (two procedures; `00575870` is additionally the installed procedure of the three
children):

```
005771F0  quest list            installed by 00577100          subtree 10
  +-- 00575870 (x3)             installed by 00575810 from 005771F0's CONSTRUCT arm
        (one instance per pane index 0,1,2; slots at self+0x108 / +0x110 / +0x118)
```

The atlas's "quest list (child)" row `00575870` (installed by `00575810`) is exactly this pane procedure — a screen
child, not a shared dialog: its only installer is the parent's own factory.

## 3. The parent's message protocol — `005771F0` (758 B)

Dispatch at `005771F6`–`00577219`: `dec eax / cmp eax,0x11 / ja default` into a rel32 table at `005774E8`. Live arms:

| id | arm | what it does |
|---:|---|---|
| 1 CONSTRUCT | `0057721B` | zeroes `+0xC8`–`+0x118`, publishes self to the global at `02CA9738` (`mov [rip+0x27324c3],rbx` at `0057726E`; the factory-built children read it back — `mov rcx,[rip+0x2733d43]` at `005759EE` resolves to the same `02CA9738`), then calls the factory `00575810` three times with `cl = 0,1,2` storing the children at `+0x108`, `+0x110`, `+0x118` (`0057727D`–`005772AD`); calls `00576F50` to load resources; on success calls `00577180` (`005772B4`–`005772C4`). If `msg->a[0] != 0` it starts with `+0x100 = 4` instead of 0 (`00577267`–`0057727D`) — the flag that makes `00576F50` skip the texture block. |
| 2 GEN-RECONCILE | `00577315` | only while `+0x100 & 8` (a child asked for teardown): the cmove chain at `00577326`–`00577353` gates `005777C0` on **all three** child slots `+0x108`/`+0x110`/`+0x118` already being 0 **and** `(+0x100 & 6) != 6` — i.e. teardown waits for the children to have already released themselves; then it clears the `8` flag and calls `00244F00` (the framework's about-to-be-destroyed broadcast). |
| 12 enable | `0057737A` | two sub-commands on `msg->a`: `0x10` switches on `msg->b` 0–5 — arm 0 copies a word from the pane's data record (`[child+0xF0]+0x14` + 2) into pane 2's `+0xCA` and forwards command 4 (`005773A2`–`005773E4`); arms 1–2 forward commands 5 and 6 (`005773EB`, `005773FE`); arms 3–5 set `+0x100` bits `0x80`/`0x100`/`0x200` (`00577411`–`00577429`). When bits `0x3C0` are all set it forwards command `0xA` and clears `0x40` (`00577433`–`0057745A`) — a four-step handshake with the panes. `0x12` clears the child slot indexed by `msg->b` (`00577469`–`005774B6`). |
| 14 opening transition | `005772FC` | `00247870(self, 0)` then `+0x100 \|= 1`. |
| 16 | `005772D1` | no-op while `+0x100 & 1`; clears bit `0x2` if `0x4` set, then `00577180` — the deferred refresh. |
| 18 BEING DESTROYED | `005774B7` | forwards command 2 to the `+0xC0` child and clears the screen global. |
| other | `005774D9` | tail-jumps `005C5230`, the shared unhandled-message stub. |

## 4. The child's state machine — `00575870` (405 B)

Chain dispatch: ids 1, 2, 16, 18, default → `005C5230` (`00575879`–`0057589F`).

- **id 1** (`0057598F`): stores its pane index `msg->a[0]` at `+0xC8` and the parent record `msg->a[1]` at `+0xC0`;
  pane 1 additionally inits `+0xCA = 2`; registers the widget with the global via `00244960`.
- **id 2** (`0057595B`): when `+0xEC & 1` and idle (`+0xC9 == 0`), clears the bit and broadcasts its own teardown
  through `00244F00`.
- **id 16** (`005758C5`): the workhorse. `+0xC9` state 2 → `00575710` builds the pane content; state 3 → frees the
  `+0xF0` record, pops one stacked row (`00575A50` on ~~`self + 0x6A + 6*(+0xD3 - 1)`~~ `self + 0xD4 + 6*(+0xD3 - 1)` *(corrected 2026-10-02, OPUS: `00575870+0xB5`–`00575870+0xBD` form `2 × (0x6A + 3n)`, so `0x6A` is in words)*), then notifies the parent
  `{0x10, pane+3}` via `00247510` (`00575936`–`00575953`).
- **id 18** (`005758A4`): sends `{0x12, pane}` to the parent — the record the parent's id-12/0x12 arm clears its
  slot on.

## 5. Subtree members and their roles

Parent subtree (10 members):

| member | role (interior citation) |
|---|---|
| `005771F0` | the screen handler; §3 |
| `00575810` | child factory — builds the `{0x100, proc, payload}` create record with `lea rdx,[rip+0x21]` = `00575870` as the procedure and `cl` as the pane index (`00575826`, `00575848`), then `00244F50` |
| `00576F50` | resource load — tests resource slots 7/8 (`002F8040`), queues both loads (`002491B0`), then loads six TIM2 indices `{0x228,0x294,0x2CC,0x2F4,0x31C,0x354}` from the word table at `0xD23740` plus `menuquest.dat` (index `0x128`, `0057704A`) via `00249210`, storing handles at `+0xC8`..`+0xF8`; sets `+0x100 \|= 2` on success (`0057706F`) |
| `005770A0` | command forwarder — sends `{0x10, 0, cmd}` to the child's handler through `[rcx]` (`005770C2`–`005770DD`) |
| `00577180` | refresh — `00246AD0` for the opening transition, then sends a 16-byte config record to the `+0xC0` child (`005771B6`–`005771D6`) |
| `005777C0` | resource teardown — frees effect slots 7/8 (`002F83E0`), then six texture handles `+0xC8`..`+0xF0` and `+0xF8` via `003697F0` (`00577821`–`00577862`) |
| `002F8040` | "slot n populated" test against the resource table (`002F8045`–`002F8050`) |
| `002F83E0` | free resource slot n and clear the table entry (`002F83FD`–`002F8402`) |
| `002491B0` | submit a load request — builds a `{0, ?, 0xD0}` record and calls `00244F50`, then `++[rbx+0x18]` (`002491F5`) |
| `00235DC0` | tail-call thunk to `003844F0` (resource release); already in `24-Compiler-And-CRT-Runtime/Thunk-Layer/members/internal-tail-call-forwarders.tsv` |

Child subtree (23 members; only the pane-specific ones are listed separately — the rest are shared text-cache
helpers):

| member | role (interior citation) |
|---|---|
| `00575870` | the pane procedure; §4 |
| `00575640` | pane teardown — frees `+0xF0` (`003697F0`) and the `+0xF8` label (`0039BB60`), then notifies the parent `{0x10, pane+3}` (`005756DE`–`005756FB`) |
| `00575710` | pane content build — resolves the quest record `+0xF8 = menuquest-data + [data+0xC]` (`00575750`–`00575765`), registers its TIM2 (`0039BEC0`), then emits the row text through `0017FA90`/`0017FB70`/`0017F790`/`0017FBE0` (`00575782`–`005757DE`) |
| `00575A10` | clear the pane's `+0xF8` label — `0024A680(obj, 0)`, reset `+0xD0 = 0xFFFF` (`00575A19`–`00575A3C`) |
| `00575A50` | breadcrumb stack — compares the incoming record's kind byte against `+0xD2` and its word against `+0xCC`; pushes `{kind, w1, w2}` onto a 3-deep stack at ~~`+0xD4`/`+0xD6`/`+0x48`~~ `+0xD4` (the kind byte, at a fixed offset), `+0xD6 + 6n` and `+0xD8 + 6n` *(corrected 2026-10-02, OPUS: `00575A50+0x86`–`00575A50+0xB6`; the third word's index is `(n + 0x24) × 6`)* counted by `+0xD3` (`00575AC0`–`00575B0A`) — the drill-down history for quest → target → detail |
| `00575B80` | pane-2 detail row — bounds-checks `+0xCE` inside the record's `{+8 count, +0xA window}`, resolves the row pointer `+0xF0 + 0xC + 4*(idx - [+8])` (`00575BF7`–`00575C04`), and creates a text label via `0024A440` stored at `+0xF8` |
| `00575C30` | pane image load — picks a TIM2 index from the word table at `0xD23730`-region by `msg->kind` (`00575C60`), loads it via `00249580`/`00249210`, sets `+0xC9 = 2`, copies `{kind→+0xD2, w→+0xCC, w→+0xCE}` (`00575CC7`–`00575CE9`) |
| `0024A440` | text-label create — `0024A4E0` then `0024A1D0` (`0024A44A`–`0024A468`) |
| `0039BEC0` | register a TIM2 object into the 8-entry texture-slot table — verifies the `TIM2` magic (`0039BED6`–`0039BEE3`), requires `+0x40 & 0xF == 1`, claims a free slot and calls `0039BF50` (`0039BF10`–`0039BF3B`); returns the slot index |
| `0039BB60`, `0039BF50` | `FontBaseHeight` layout-key readers — already in `../Layout-Parameter-System/members/layout-key-readers.tsv`; `0039BB60` also walks the texture-slot table (`0039BB77`–`0039BB84`) |
| `0017F790`, `0017FA50`, `0017FA90` | text-emit wrappers — resolve the font context via `001B5FB0` then call into the text-object cache (`001B47A0`, `001B5B60`, `001B6350`) |
| `0017FA70`, `0017FB70`, `0017FBC0`, `0017FBE0` | CRT tail-call forwarders — already in `24-Compiler-And-CRT-Runtime/Generated-Families/members/nativeadapter-*tailcall.tsv` |
| `001B47A0`, `001B5330`, `001B6350`, `001B6430`, `001B6510` | the text-object cache — a vector at `+0x250`/`+0x258` of `{ptr}` entries keyed by `{id=+4, kind=+0x10}`; `001B6350` finds-or-allocs (`001BA860` + `00674A00`), `001B47A0` finds-and-assigns, `001B5330` releases, `001B6430`/`001B6510` are find variants (`001B6380`–`001B63F1` is the find loop) |

## 6. Controls and limits

- The parent's live id set `{1,2,12,14,16,18}` reproduces the atlas's `message_ids` column exactly; the table's other
  12 rows are dead (all point at the default arm).
- `menuquest.dat` (constant-request index `0x128`) is the same file the
  [request census](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md)
  attributes to this code path — the screen reads the authored quest list, it does not generate it.
- The three children are **one procedure instantiated three times**, distinguished by the pane index byte written at
  `+0xC8` during CONSTRUCT — they are screen children of `005771F0`, not shared dialogs: `00575870`'s only installer
  is `00575810`, which runs only inside this screen's CONSTRUCT arm.
- ~~Not resolved: the semantics of forwarded commands 4/5/6/0xA, what the `+0x100 & 0x3C0` handshake waits for, and the~~
  ~~  pane-side meaning of `+0xC9` states 2 and 3 beyond "content ready" / "row popped".~~
  **Resolved 2026-09-18 (FABLE) — both halves, from the two bodies.** *The handshake:* inside the parent's id-12 arm the sub-command `0x10` switches on `msg->b`: arms 0–2 forward commands 4, 5 and 6 to the `+0xC0` child (`005773DD`–`0057740A`), and arms 3, 4 and 5 **set bits `0x80`, `0x100` and `0x200` of `+0x100`** (`00577411`–`00577429`); every arm then falls into one test — `+0x100 & 0x3C0 == 0x3C0` (`00577433`–`00577443`) — and only when all four bits are up (bit `0x40`, set ~~by the opening path~~ by `005776D0`, whose only caller is `0056F2A0` *(corrected 2026-10-02, OPUS: `005776D0+0x20`–`005776D0+0x28` `and eax, 0xFFFFFC7F` / `or eax, 0x40`, which also clears the three arm bits)*, plus the three arm bits) does it forward **command `0xA`** to the child and clear bit `0x40` (`00577449`–`0057745A`). So the handshake waits for the three *pane-ready* sub-commands 3, 4, 5 after the opening, and `0xA` is the *all panes ready* command that fires once per opening. *The forwarded numbers:* the child procedure `00575870` never reads them — its id-16 arm (`005758C5`–`0057595B`) consults only its own `+0xC9` state (2 → build content via `00575710`, 3 → free the `+0xF0` record and pop a stacked row) and the message's third dword is dropped — so 4, 5, 6 and `0xA` are one wake-up at the receiver; they distinguish the parent's arms, not the child's behaviour. Static: both arms decoded.

## Falsification pass

**Pass 1 — 2026-09-14 (OPUS).** Attacked at parent `GN160` (`fa0db293…`), EXE `73461d08…`, decoding
with capstone. Instrument: `Tools/work/OPUS/falsify_questlist.py`. **Nine claims attacked, nine
survived. No correction.**

| claim | the killer | result |
|---|---|---|
| `005771F0` is **758 B**, `00575870` is **405 B** | the census giving a different length | **survived** — both exact |
| the dispatch at `005771F6`–`00577219` is `dec eax / cmp eax,0x11 / ja default` | any of the three absent from that window | **survived** — all three, in 10 instructions |
| the rel32 table is at `005774E8`, default `005774D9` | a different table or default | **survived** |
| the live arms are ids 1, 2, 12, 14, 16, 18 at the published addresses | any other id reaching a real arm, or an arm elsewhere | **survived** — six for six, everything else defaults |
| `00575870` chain-dispatches 1, 2, 16, 18, default `005C5230` | any other id answered | **survived** |
| id-1 calls the factory `00575810` **three** times | a different count | **survived** — `00577283`, `00577294`, `005772A5` |
| `0057726E` `mov [rip+0x27324c3],rbx` and `005759EE` `mov rcx,[rip+0x2733d43]` both resolve to `02CA9738` | either resolving elsewhere, or the two not meeting | **survived** — both land on `02CA9738` |

> **The last one is why this page was worth attacking.** It states **two different displacements**,
> written at **two different instruction addresses**, in **two different functions**, and claims they
> meet at one global — the parent publishing itself where the factory-built children read it back.
> **A single mistyped hex digit in either displacement, or either address, and they would not meet.**
> They meet exactly.

**Not attacked by this pass:** the arm interiors — the four-step `0x3C0` handshake inside id 12, the
cmove chain gating teardown in id 2, and the resource indices `00576F50` loads, all of which the page
cites but this pass did not re-derive.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**ActorEntity — CLIENT (6 edges through 5 of this page's functions).** The ActorEntity layer reaches this page at `002B7B80`, `0017F790`, `0017FA50`, `0017FB70` and 1 more. `Actor_GetWorldPosition` is the worked example, read in full - it is the position read, gated on the kind bits: `byte[+3] >> 5` has to be 1 or 3, and then the three floats at `[actor + 0xB8]` `+0`/`+4`/`+8` go to the caller's three out-params - anything else gets zeros rather than an error; **1 of the 5 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Audio — CLIENT.** `FUN_002120e0`, owned by that layer, calls `001BA860` on this page. That caller is a 79-byte locked query: it takes the lock at `[obj + 0x130]`, asks the sub-object at `+0x70` for its answer, and releases the lock before returning it unchanged; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Input — CLIENT.** `FUN_00291d90`, owned by that layer, calls `0024A440` on this page. That caller is a 625-byte screen-message handler: message 1 registers the screen at `[0209AC30] + 0x300`, message 2 dispatches on the nibble at `(dword[+0x168] >> 16) & 0xF`, and message `0x10` clears that registration; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**World — CLIENT.** `FUN_003c63a0`, owned by that layer, calls `0024A680` on this page. That caller is a 122-byte swap of the object held at `[02B457F0]`: it releases the previous one, takes the replacement at size `0x200`, and caches `word[+0x14]` and `word[+0x16]` of the new object's `+0x20` block into `[02B457F8]` and `[02B457FC]`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Presentation — CLIENT and SERVICE (SWE2-CONTRACT 2026-09-15, 17 edges).** The quest list binds its
effect fonts through the render layer — `001B4590`
(`Presentation.EffectFont.LoadedFontVariantBindingAndSlotRegistration`) is called by `001B47A0`/
`001B6510`, and `0017F790`/`0017FA50`/`0017FBE0` reach the EffectFont native-support helpers
`001B47A0`/`001B5B60`/`001B5330`; `0024A1D0` calls the five asset-materialization helpers
`00181190`/`00181250`/`00181520`/`00180E70`/`00181000`. Caller-side, the selection state machine
`00579420` drives `00247510`/`00247870`, `002BAF80`/`002B7B80` drive `00249580`, ScreenCapture
`002D2DB0` calls `00247510`, and `001BA860` is reached by `001BB920`/`001BB2B0`. The screen lives
inside the font-and-widget draw pass — the crossing is its rendering, not a second owner.

**Platform — MECHANICAL (SWE2-EC7-41, 6 edges).** `0016D6D0`, called by this page's `001B5B60`
section body, is also called by six Platform-filed bodies; the crossing is shared-helper fan-in,
not that this page owns anything in that layer.


**CombatAI — MECHANICAL (SWE2-EC7-156, 1 edge).** `00301AD0` of that layer calls `00309EC0`, the shared helper batch-121's `003C06E0` also consults — fan-in, not a shared responsibility.
**CombatAction — CLIENT (SWE2-EC7-156, 4 edges).** `00317BC0`/`00317C80` call `00309EC0`, `002F8060`/`002FA74x` call `003148F0` — the combat-action layer consults this page's shared helpers.
**Gameplay — CLIENT and SERVICE (SWE2-EC7-156, 4 edges).** `002543F0` calls `00309EC0` of that layer, `0031C5D0` calls `00309EC0` in return, and batch-121's `003C06E0`/`003C18A0` reach it too — shared-helper exchange, not a second owner.
**Items_Equipment_Shops_License — MECHANICAL (SWE2-EC7-156, 1 edge).** `00317930` of that layer calls `00309EC0` — shared-helper fan-in.

## SWE2-EC7-41 update (2026-09-19) - `001B5B60`

`001B5B60` (346 B) is a quest-list body - `01F811F8`, `005CD4F0`/`00199DB0`/`0016D6D0`/`0016DA60`/`005CD820`/`001E9A30`. Interior anchor `001B5BCD` (a `005CD4F0` call).

## SWE2-EC7-49 update (2026-09-19) - `001B5330`

`001B5330` (190 B) is a body - `008C2A40` import call only. Interior anchor `001B5383` (the import call).

## SWE2-EC7-49 update (2026-09-19) - `001B47A0`

`001B47A0` (186 B) is a body - `001B4590` plus a `008C2A40` import call. Interior anchor `001B47FF` (the `001B4590` call).

## SWE2-EC7-57 update (2026-09-19) - `001E9A30`

`001E9A30` (170 B) is a quest-list body - `0016D6D0`/`0016DA60`/`002124C0` plus one vcall. Interior anchor `001E9A73` (a `0016D6D0` call).


## SWE2-EC7-85 update (2026-09-20) - `00402490` + `00403330` measured

`00402490` (383 B) is the caret/scroll updater the screen callers
run: `[r14+8]`/`[+0x10]`/`[+0x18]` each register through
`0020E620(0)` into the three `[global+0x60]`-chained elements;
`[rbx+0x18]` resolves `0020E600` -> `0029CD00` to accumulate the
scroll delta, the `+0xC`/`+0xCC`/`+0xCE` words rewrite, `rdi+8`
bit 0 tracks the `[r14+0x10]` arm, and the tail reads
`byte[[rbx+0x20] + rdx*8 + 7]` into `[rbx+0x39]` with `word[+0xA]`
taking the index.
Interior anchor `00402511` (the `0029CD00` call).

`00403330` (65 B) is the progress stepper the same callers run:
`[rcx+0x10]` gains `max(6, (0x100 - [+0x10]) * 2/3)` via
`0x2AAAAAAAB` magic, clamps at `0x100`, and returns whether it
reached `0x100` - call-free.
Interior anchor `00403357` (the `+0x10` add).

## SWE2-EC7-86 update (2026-09-20) - `00402250` two-stage pair lookup measured

`00402250` (113 B) is the keyed pair fetch the quest-list callers
run: `003BE2D0(word[r8+0x1C])` resolves the row (null -> 0), then
`003DFB50(row, r9d, [rsp+0x50])` resolves the sub-record (null ->
0); on success `movsx word[+4]` is stored to `[rdi]` and `movsx
word[+6]` to `[rbx]` before returning 1.
Interior anchor `00402293` (the `003DFB50` second-stage resolve).

## SWE2-EC7-88 update (2026-09-20) - `003C2200` + `003BE680` measured

`003C2200` (14 B) is the thin forward the quest-list callers
run: `003C26C0([02B457E0], ecx)` - the shared table and the
index, nothing more.
Interior anchor `003C2209` (the `003C26C0` tail).

`003BE680` (122 B) is the two-level word fetch over
`[02B457E0+0xE0]`: `byte[+9]` bounds `ecx` into a
`word`-relative block, `byte+byte[+1]` selects the 24-stride
element at `+4`, and `byte[+2]` strides 20 into the final
record - returning `word[rdx]` and optionally writing
`word[+2]`/`word[+4]` to the `rdx`/`r8` out-pointers.
Interior anchor `003BE6DE` (the `word[+2]` out write).

## SWE2-EC7-100 update (2026-09-20) - `002B7460` + `002B66E0` + `002B6310` measured

`002B7460` (215 B) is the record build `002B7B80` and
`002BAF80` call: `+0xBBC0` clears, an `0x480` stack record
is zeroed by `00861EC0`, `003BE3A0` fills it for
`word[+0x138]`/`word[+0xBBE0]` mode 2, and each `0x30`-
stride result entry gains `(word[+0x13A] & 8) << 0xC`;
`00402D20` on `rbx+0xB140` registers the product into
`+0xBBC0`, and a `+0xBBE0 == 6` tail runs `00402BF0` on
it - the build-and-register the list's refresh issues.
Interior anchor `002B74E0` (the per-entry `or` loop).

`002B66E0` (624 B) is the bounded-position solver the same
pair call: `dword[+0x118]` is pinned to `0x100` for the
duration of `00403550` (saved and restored), the
`0x51EB851F` (/100) scalings of `word[+0xBBD8]` and
`word[+0xBBDA]` by `[+0xD4]` offset `+0xC8`/`+0xCC`
origins into the measure, `00274790` intersects the
`+0xBBEC`/`+0xBBEE`-halved `+-0x20` box, and a four-side
overflow clamp against `+0xF8`..`+0x104` bounds sets
flag bits 1/2/4/8 - both x-sides clamped recentres x, both
y-sides recentres y, and `/3` (`0x2AAAAAAB`) of the
residual delta, `+-1` minimum, updates `+0xC8`/`+0xCC` -
the drag/scroll constraint solve the list applies.
Interior anchor `002B6884` (the first bound compare).

`002B6310` (59 B) is the two-stage resolve the same pair
call: `cx == 0xFFFF` yields 0, otherwise `003C02B0` maps
`zx(cx)` to a stack record whose `word[+2]` feeds
`003BF6C0`, and `byte[+1]` of the second record is the
answer - the id-to-record-to-byte chain the list shares.
Interior anchor `002B6332` (the second-stage fetch).

## SWE2-EC7-101 update (2026-09-20) - `003BE3A0` measured

`003BE3A0` (734 B) is the counted-record enumerator
`002B7460` wraps for `word[+0x138]`/`word[+0xBBE0]` mode:
the `02B457E0` global's `+0xD0` flag word gates bit 12
(`esi` in `{0xD, 0x2F}` arms bits 13/14, `+0xD0` always
gains `0x1000`, bit `0x800` is managed around two
`003C1A20` record fills), `byte[+0xCA]` takes the mode
byte, and when the `[+0xE8]` list's `word[+8]`-count
bounds an `esi`-indexed `+4+rsi*8` entry with a nonzero
`+1` byte a second `003C1A20` runs under `0x800` - then a
`r12d`-count loop runs `003C2320` per `0x30`-stride record
with the `0x18`-stride inputs, subtracts the out-pair
into `+0`/`+2`/`+0x14`/`+0x16` (and `+0x1C`/`+0x1E` when
the input dword is zero), and mode 6 adds the
`003BD9F0`/`00473CC0` resolve that installs `[rsp+0x30]`
at `+0xC` or clears `+0x18` bit 0 - the two-pass
build-and-transform the list's record fill drives.
Interior anchor `003BE530` (the record loop head).

## SWE2-EC7-103 update (2026-09-20) - `00271CB0` measured

`00271CB0` (256 B) is the running min/max fold
`002B7B80` and `002BAF80` call: over `r8d`
`0x8`-stride word-quad records starting at
`rdx + 0xA`, each iteration unpacks the previous
quad (`movsx` halves of `rax`/`rcx`), min-folds
x/y into `eax`/`ecx` and max-folds into
`edx`/`r8d`, and the packed `{min, max}` qword
pair is stored to `[r14]` - the bounding-extent
reduce the list builds run.
Interior anchor `00271CF0` (the loop head).

`003C2320` (925 B) is the fill body `003BE3A0` runs: `00377B60`, `003C0380`, `003BF5E0`, `003BF9A0`, `0032A8A0` x2, `003BE700`, `003BDDE0` x2, `00377A40`, `002F9860`, `002F9920` x2, `003C05F0` x2, `003BE810` and `003BE950` walk and fill the list records - the quest-list's per-entry emit.

Interior anchor `003C258B` (function `003C2320`).

`003BDDE0` (524 B) is the per-entry emit `003C2320` calls twice: the `rip`-relative global at `rip+0x27879E0` supplies the object whose `+0xE0` qword is walked, `byte[rcx+9]` keys the step, and `003BF430` x2, `003C0D30` x3, `003BE1E0` plus `003C0340` x2 fill the record fields under a `dword[rsp+0x20]` zero test - the quest-list entry's field-fill helper.

Interior anchor `003BDE36` (function `003BDDE0`).

`003C05F0` (232 B) is the per-entry emit `003C2320` calls twice alongside `003C02B0`/`003C0450`: `00264790`, `003148F0`, `003C0380`, `002543F0` then `003C15B0`, `003C12B0`, `003C1680` run the record's tail fields - the quest-list entry's closing stage; `003148F0` and `002543F0` are shared helpers that movement, combat action, gameplay and spawn encounter lifecycle callers also reach, so their presence here is the list borrowing the shared layer, not the list owning it.

Interior anchor `003C0662` (function `003C05F0`).

`003BE1E0` (228 B) is the single-callee helper `003BDDE0`, `003BED70`, `003C12B0` and `003C1A20` all run: one `003BDFF0` call does the record step - the quest-list family's shared leaf, called from four of the page's bodies.

Interior anchor `003BE1FD` (function `003BE1E0`).

`003C1A20` (848 B) is the fill body `003BE3A0` runs beside `003C2320`: `003C0340` x2, `003BF430` x3, `003C18A0`, `003C0F70`, `003BE1E0`, `003C0380` and `003BF5E0` walk and fill the entry records - the quest-list's second per-entry emit, one of `003BE1E0`'s four callers.

Interior anchor `003C1AA9` (function `003C1A20`).

`003BE950` (759 B) is the per-entry emit `003C2320` calls: `0037EB70` x2, `0029CD00` x2, `00202C90`, `003BCBA0`, `003C0380`, `003BF5E0`, `002F9920` and `003BD6F0` fill the record under the cookie check - the quest-list entry's detail stage.

Interior anchor `003BE9AE` (function `003BE950`).

`003C12B0` (755 B) is the entry helper `003BF7C0`, `003C0450`, `003C05F0` and `003C0D70` call: `0032A8A0`, `002543F0`, then `003C0340` x2, `003BF430` x3, `003C18A0`, `003C0F70`, `003BE1E0`, `003C0380`, `003BF5E0` - the record's shared mid-stage, one of `003BE1E0`'s four drivers.

Interior anchor `003C12FC` (function `003C12B0`).

`003BDFF0` (493 B) is the scan `003BCDE0` and `003BE1E0` call: `003C0340` gates, then `edi` walks `003BF430(esi, edi, out)` entries over `02B457E0`, each result's `dword[+0x10] >> 2 & 0xF` tests against `r15d` and `003C06E0`/`003C0D30` run on a hit - the list's entry filter.

Interior anchor `003BE010` (function `003BDFF0`).

`003C0D30` (61 B) is the dispatch shim `003BDDE0`/`003BDFF0` call: `003BF430(ecx, out [rsp+0x40])` resolves an entry, null-outs, and the out-dword selects the tail-jump - 0 to `003C18A0`, nonzero to `003C0F70` - the list's two-arm entry dispatch.

Interior anchor `003C0D3D` (function `003C0D30`).

`003C06E0` (96 B) is the flag classifier `003BCBA0`/`003BDFF0`/`003C1180` call: `word[rcx+0xE] == 0xFFFF` returns 1, `dword[rax+0x10] & 0xFC0` set runs `00309EC0(0)` and returns `0x8|0x10` or `|1`, else `0032A8A0(cx)` returns `0x2|0x4` or `|1` - the list's entry-kind word builder.

Interior anchor `003C070A` (function `003C06E0`).

`003BF9A0` (438 B) is the row flag setter `003C2320` calls: `00264790` counts, `003BCBA0` evaluates, and when `word[rcx+0xC]` equals the count the result gets `bts edi, 8`; `02B457E0`'s `dword[+0xD0]` bit 8 gates the loop, and `003BC260`/`00473BB0`/`00377A40`/`003C17E0` run the per-row arms - the list's flag-propagation pass.

Interior anchor `003BF9CF` (function `003BF9A0`).

`003C26C0` (430 B) is the two-slot match `003C2200` calls (sibling of `003C1F00`): `rcx+0x120`'s two `0xA8`-stride entries are scanned for `byte[+0x10] == dl`, and `0024A9E0`/`0017D2E0`/`0024A480` run on the hit - the screen's paired-record selector.

Interior anchor `003C27A9` (function `003C26C0`).

`0024A480` (96 B) is the packed-field writer `003C26C0`/`003C63A0` call: `0024A4E0` resolves the slot, a stack arg `< 0x4000` packs `arg << 0x12` into `dword[rbx+0x38]`'s high bits (`& 0x3FFFF` keeps the low), `qword[rbx+0x28]` takes `r9`, and `0024A1D0` commits - the screen's slot-field write.

Interior anchor `0024A49E` (function `0024A480`).

`0024A9E0` (30 B) is the call-free stride walker `003C26C0`/`002509D0` call: `rax = rcx + 0x10`, `word[rcx+6] > edx > 0` bounds, then `rax += dword[rax]` `edx` times - the skip-list's n-th element address.

Interior anchor `0024A9F2` (function `0024A9E0`).

`003C1680` (350 B) is the list walker `003C05F0` calls: `[02B457E0 + 0xE0]` chain, `byte[+9]` bounds `edi`, `word[rsi + r8]` offset table at `r8 + edi*2 + 0xA`, `byte[rdx] + byte[rdx + 1]` must be nonzero - a second pass over the same shape follows - the quest list's entry fetch.

Interior anchor `003C16F0` (function `003C1680`).

`003C17E0` (183 B) is the indexed fetch `003C1680`/`003BF9A0` call: `003779F0` count <= 0 returns 1; `[02B457E0 + 0xE8]` + `word[+0xA]` roots the table, `word[rcx]` bounds `r8d`, `rdi = rcx + 2 + r8*2` is the entry, then `003C0380`/`003C1070` resolve it - the quest row's second-hop lookup.

Interior anchor `003C17E8` (function `003C17E0`).

`003C1070` (261 B) is the resolve-verify `003C17E0`/`003C1180`/`003BCBA0` call: `rax = [02B457E0]`, `r8 = [rax + 0xE0]` is a two-level table - `byte[r8 + 9]` bounds `r9d`, the `word[r8 + r9*2 + 0xA]` + `r8` hop reaches a sub-record, then `byte[r8] + byte[rcx + 1]` x3 scales and `byte[r8 + 2]` strides `rcx*20` deeper; `00264790` runs, `003148F0` re-fetches the count when `eax <= 0`, and a `rbx`-walked word-pair array compares `word[rbx] == ebp`, `word[rbx + 2] == eax` to answer 1 or 0 - the quest row's match verdict.

Interior anchor `003C1118` (function `003C1070`).

`003BE810` (317 B) is the unique-byte collector `003C2320` calls: `byte[rbp+rcx+8]` (`r8b` = rbp) is the candidate - `0xFF` writes `dword[r9]=1` and returns `0xFF`; otherwise it dedups into the `rsp+0x40` byte list (`edx` counts mismatches; `edx >= r9d` keeps it), then `003BCBA0`/`003BDDE0` resolve the byte against the list and `00808C40` guards - the screen's distinct-entry enumeration.

Interior anchor `003BE881` (function `003BE810`).

`003BD9F0` (309 B) is the row probe `003BE3A0` calls on the `02B457E0` table: `dword[+0xD0]` requires bit8 ~~set and bit9 clear~~ and bit9 both set *(corrected 2026-10-02, OPUS: `003BD9F0+0x3F` `bt eax, 8`, `003BD9F0+0x4C` `bt eax, 9` / `003BD9F0+0x50` `jae` to the 0 return)* else 0; `003BC260` returns the kind, then `byte[+0xCB]` rows iterate through `00473BB0(0, i, kind, rsp+0x20)` and keep the rows where `dword[+0x20]==1`, `dword[+0x34]` nonzero and `dword[+0x2C]==r14w` - the screen's indexed entry enumeration beside `003C1070`'s two-level lookup.

Interior anchor `003BDA7C` (function `003BD9F0`).

`003BE700` (271 B) is the span locator `003C2320`'s per-entry fill runs: `ebx` must index under `byte[[02B457E0 + 0xE0] + 9]` entries and `word[rax + ebx x 2 + 0xA]` relocates the outer record; `r10d` walks the `[byte[rdx], byte[rdx] + byte[rdx+1])` span while the `r9`-derived byte pair re-validates the range per level, and each live index tests `byte[base + 4 + r10d x 24 + 0x11] == ebp` for the `r10d` return - `-1` on exhaustion; the quest list's packed-index point query.

Interior anchor `003BE760` (function `003BE700`).

`003C15B0` (207 B) is the match scan `003C05F0` runs: `02B457E0`'s `+0xD0` bits 8 set / 9 clear gate the body, `003BC260` resolves the working record, then a `+0xCB`-counted loop `00473BB0`s each slot and any `+0x20 == 1` result is `003C0380`-checked against `edi` - the 'find entry matching this id' pass

Interior anchor `003C15FF` (function `003C15B0`).

`002D1750` (200 B) is the flag-dispatched position emit `002D2DB0` runs on a selected entry: bit 0x20000 of `[rcx+0xE0]` centres a `00243030` write (`(r9 + width)/2` against globals `01E0CF70`/`0209E658`), bit 18 writes `00244070` at `[rbx+0xFA] + arg` against `01E0CF74`, and bit 0x100000 repeats that write with flag 1 against `01E0CF78` - the three x-placement rules for the row

Interior anchor `002D179C` (function `002D1750`).

`00243030` (295 B) is the glyph-quad builder `002D1750` calls per emitted entry: `(0208F570 & 0x3F) >> 2 & 7` picks an animation sub-table inside `[0208EA90]+0x20 +0x30`, whose `+0x14`-counted 8-byte entries supply the quad (`+0`/`+2` u16 corner, `+4` low-12 width / high-12 height, `+7` palette index via the `+0x12` byte table) written into `[rbx+0x5C]`; then `esi -= (e[4]>>1 & 0x7FF)`, `edi -= (e[4]>>0xD & 0x7FF)` feed `002D8CB0`, with `002D8BB0(1)` before and `002D8BB0(0)` after when `ebp == 0`

Interior anchor `0024308D` (function `00243030`).

`00403550` (165 B) is the rect rescale `002B66E0` runs per row: after `00401FD0`, all four s16 lanes at `[rsi]`/`+2`/`+4`/`+6` are scaled by the `xmm1` factor and truncated - `+4`/`+6` additionally biased `-0x18`, `+0`/`+2` biased by `bx+0xC`/`di+0xC`

Interior anchor `0040356A` (function `00403550`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22, FRONTIER's debt (SWE2-FRONTIER, 2026-09-30)

*Added 2026-09-30 (SWE2-FRONTIER, `SWE2-FRONTIER-PASS22-DEBT-OWN`, batch 2): the layers pass 22 still reported for this page. Every edge was listed in full and the cited function's body was read.*

**Save_Load_Settings — CLIENT and DEPENDENCY (19 edges).** The save controllers use the widget helpers this page's panes also use: `00247510` sends a widget message: it builds a kind-`0xC` message carrying the caller's two arguments and calls the handler at `[obj+0]` when the object and handler are non-null (six callers, `0057E950` to `00582860`); `00247870(w, on)` sets or clears bit 1 of the widget flags at `+0x40`, and refreshes the widget through its layout routine when bit `0x20` is set (five callers, among them `SaveWrite_OperationStateCallback` `0057E4D0` and `SaveStorageQueue_ControllerStateHandler` `005823B0`); and `00244960(parent, child)` attaches the child only when the child's parent link at `+0x10` is empty. It tail-calls the list append, which links the child after the parent's last child and bumps the count at `+0x30` (four callers). In the other direction, the field-id getter `WorldTransition_GetActiveOrPendingFieldId` (`003148F0`) reads the dword at `+0x1044` of `SaveImage_GetPersistentPayloadBase` (`002EF2B0`), clamping negatives to 0. `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` (`0032A8A0`) reads the same persistent payload. `SaveImage_FinalizeHeaderAndChecksum` (`00583D60`) calls both while it writes the header. So the quest list and the save header read one field id and one flag store out of the save image; this page only reads them.

**SaveLoad — CLIENT (2 edges).** `00582790` claims a slot through `00249580` (first free entry of a 12-entry, 32-byte table, argument stored at `+8`) and loads through `00249210`, the same loader this page's panes use for `menuquest.dat`. It shares the tables and nothing else.

**Movement — CLIENT (3 edges).** `0033A720`, `003ED190` and `003ED3F0` call the field-id getter `003148F0`: movement bodies asking which field is active or pending. That is the same read the quest-list emit does, and it shares nothing else with this screen.

**Spawn_Encounter_Lifecycle — CLIENT (1 edge).** `SpawnKeep_RotatePersistenceBanksForAreaTransition` (`00233780`) calls `003148F0` to learn the field it is rotating banks for. It is the same read, and it has no role in the quest list.

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-the-quest-list-screen-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `001B6430` | 61 B | scans the qword pointers from qword `rcx+0x250` up to qword `rcx+0x258` (stride 8) and stores to qword `rcx+0x270` the first pointed-to entry whose dword `+4` equals `edx` and whose byte `+0x10` is non-zero, or 0 when none matches | `001B643E`, `001B6446`, `001B644C`, `001B6459`, `001B6461` |
| `001B6510` | 80 B | gets an entry from `001BA860(rcx+0x190)`, zeroes its qword `+8`, dwords `+4` and `+0x14` and bytes `+0` and `+0x10`, stores `(dword rcx+0 shifted left 5) + edx` to its dword `+0x18`, and tail-jumps `001B4590(rcx, entry)` | `001B6526`, `001B6530`, `001B653D`, `001B654D`, `001B655B` |
| `00274790` | 31 B | swaps dwords `rcx+0` and `rcx+4` when the first is greater (signed), then swaps dwords `rcx+8` and `rcx+0xC` under the same test | `00274795`, `00274799`, `0027479B`, `002747A4`, `002747A8` |
| `00402BF0` | 52 B | returns when `rcx` is null; otherwise walks the list from `rcx` through qword `+0x60` links and, for every node whose byte `+2` is 1, clears bits 1 and 2 (AND `0xFFF9`) and then sets bits 0 and 3 (OR 9) of word `+0x4E`, stores `0x3F800000` to dword `+0x38` and `0x80` to word `+0x4C` | `00402C00`, `00402C06`, `00402C0A`, `00402C0F`, `00402C16` |
