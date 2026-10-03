---
id: ui-message-window-layout-readers
title: The message-window layout-key readers — MsgWin, NobuMessage, MessageLine, TalkingMessage, ActiveLog, HelpMessage, AutoWindow
status: DOCUMENTED — 00556F90's id-2 arm read 2026-09-18: the message text comes from the low-pool rows 0x3ED + page (title) and 0x838 + page (body, wrapped into three 256-byte lines by 002B5730)
evidence_tier: 1
tags: [ui, menu-screens, message-windows, layout-keys]
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  snapshot_basis: GN160's snapshot by pairing, not by a separate verification - the document already names GN160 as its gzf_sha256 and b57264ba IS GN160's annotation snapshot, recorded in GfzEnv.ps1's lineage and in every other GN160-stamped document. Added 2026-09-15 (OPUS) to complete the block, not to assert a check nobody ran. This page's 2026-09-14 falsification pass is separately image-derived: every cited instruction was read from the authorized EXE.
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN160 -> GN161 - the records this document rests on are unchanged except for `002A4430`, `002A86A0`, `002B2DF0`, `002D66D0`, which gained a plate comment and CodeDomain tags in batch R109 and lost nothing; voided by any delta that removes or rewrites a comment, tag, name, prototype or body range; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-14
audit:
  passes: 1
  last_pass: 2026-09-14
  last_pass_state: OPUS-eleven-of-twelve-instructions-exact-one-address-off-by-four-installations-censused
  last_pass_kind: attack
  crossref_clean: false
  reopened_count: 0
addresses:
  - "002A6190"
  - "002A86A0"
  - "002A3960"
  - "002BE4F0"
  - "002BF690"
  - "002D66D0"
  - "0035E070"
---

# The message-window layout-key readers

**Status:** ~~PARTIAL~~ DOCUMENTED *(corrected 2026-10-02, OPUS: the front matter says `status: DOCUMENTED`)* — this page documents where each `uisize.json` key of the message families lands
at its native use site (the LAYOUT-KEY-READERS package). It is *not* a full decode of the message
windows: the procedures' dispatch arms and the `0xC0368C`-family lookup tables are the parts still
open (see the shared-dialogs page's "Not yet established" for `00556F90`'s id-2 arm). The text
control-code interpreter `002AC5F0` — which several readers below feed — is documented separately on
[the text-control-code page](../Text-And-Number-Rendering/the-text-control-code-language.md).

The message system is layered: **`002A2C00`** is the geometry/install hub — it installs the big
message proc **`002A6190`** P (ids 1–4, 10, 12, 15, 18, 21) and is itself reached from
`002A3090`→`00474100` (the `TalkingMessage`/`NobuMsg` window) and from `00556F90`'s subtree via the
`002AC5F0`→`002B5730` chain. **`002A86A0`** P is the log pane — `002A8220` `lea`s it at `002A8377`.
The battle log (**`002BE4F0`** P, `00253780` family) and the standalone help/auto windows
(**`002BF690`** P, **`002D66D0`** P, **`0035E070`** P) share the same key families.

| reader (→ owner) | keys | what the values do at the use site |
|---|---|---|
| `002A2C00` (hub; installs `002A6190`, →`002A3090`→`00474100`) | `TalkingMessageOffsetX/Y`, `MaskBottomBlackBandH`, `FontBaseWidth`, `MessageLineWordCount` | `TalkingMessage` offsets `add`ed into the rect origin `[rbp-0x58]`/`[rbp-0x54]` (`002A2DC4`, `002A2DCD`); `MaskBottomBlackBandH` `sub`ed from the frame bottom then `cmp` — the letterbox clamp (`002A2E38`); `FontBaseWidth`/`WordCount` → `movd`+`cvtdq2ps` floats for the measure pass (`002A2E97`, `002A2EA6`) |
| `002A6190` P (the message window) | — | ~~reads no key directly~~ reads three keys itself — `MessageWinMaskBottom` (`002A6190+0x234`), `MsgWinSignalOffsetY` (`002A6190+0x400`) and `MessageWinMaskTop` (`002A6190+0x738`) *(corrected 2026-10-02, OPUS: the `layout-key-readers.tsv` rows, each read at the bytes)*; its helpers `002A4170`/`002A4430`/`002A7F70`/`002A8100`/`002A8220` feed it (below) |
| `002A4170` (→`002A6190`) | `MsgWinCaptionBaseOffsetX/Y`, `SystemWindowCaptionOffsetX/Y`, `NobuMessageItemGetOffsetY` | caption bases → `xmm7`/`xmm0`/`xmm6`/`xmm1` floats — the caption draw origin (`002A41F5`, `002A4230`, `002A43A9`, `002A43DC`); `ItemGetOffsetY` → `ebx` — the "item get" line's Y (`002A434D`) |
| `002A4430` (→`002A6190`) | `MsgWinLogCursorOffsetX/Y`, `MsgWinSelectCursorOffsetY`, `FontBaseWidth`, `MessageLineWordCount` | cursor offsets and font metrics → `xmm` registers for the log/select cursor floats (`002A467A`, `002A4682`, `002A463C`, `002A4694`); `LogCursorOffsetY` `sub`ed from `r8d` (`002A46E4`) |
| `002A7F70` (→`002A6190`; also an installer of `002A86A0`) | `MsgWinSignalLeftOffset` | `ecx − key − eax` — the left "more" signal's X from the window edge (`002A803C`) |
| `002A8100` (→`002A6190`; installs `002A86A0`) | `MsgWinLogSignalPosX`, `MsgWinLogSignalPosY` | → `[rsp+0x20]`/`[rsp+0x2C]` — the log-window signal sprite position (`002A8145`, `002A8150`) |
| `002A8220` (→`002A6190`; `lea rdx, 002A86A0` at `002A8377` — *`002A837B` until 2026-09-14; that address is four bytes into the instruction's `disp32`*) | `MsgWinSignalRightOffset` | `ecx − key` — the right signal's X (`002A8371`) |
| `002A86A0` P (the message-log pane) | `MsgWinSignalOffsetY`, `MsgWinLogUpCursorOffset`, `MsgWinLogDownCursorOffset`, `MsgWinLogUpDownCursorOffsetX`, `FontBaseHeight` | `SignalOffsetY` `sub`ed → `[r14+0x9A]` (`002A8716`); up/down cursor offsets → `r8d`/`edx` draw args (`002A89CF`, `002A89D9`, `002A8A01`); `FontBaseHeight` → `ecx` row pitch (`002A8A25`) |
| `002A3960` P (message-window child, installed by `002A70B0`) | `MessageWinMaskTop` | `edx + key` — the top mask line added to the text Y (`002A3D5B`) |
| `002A6C40` (→`002A2C00`) | `MessageWinMaskBottom`, `MessageWinMaskTop` | `eax = 448 − new height − MaskBottom` → `[rsi+4]` — the window's Y (the gap to the screen bottom, not a skew field; `002A6E43`); `ax − MaskTop` → `[rcx+0x9A]` word (`002A6E51`) |
| `002A70B0` (→`002A2C00`; installs `002A3960`) | `NobuMsgWindowShapeBackOffset_X/Y/W/H`, `FontBaseWidth`, `MessageWinMaskBottom`, `MessageLineWordCount` | the four `ShapeBack` words → `[rsp+0x22..0x26]` — the backing-shape rect (`002A716E`–`002A719A`); `FontBaseWidth`/`WordCount` → floats (`002A7259`, `002A7274`); `[rdi+4] = 448 − height `[rdi+0xC]` − MaskBottom` → the window's Y word (`002A72EA`) |
| `002A5590` (→`002A6A80`→`002A2C00`) | `NobuMessageSelectLF` | `eax − key + ebx` — the select line-feed adjust (`002A581C`) |
| `002B2DF0` (→`002AC5F0`→`002B5730`→`00556F90`) | `FontBaseWidth`, `NobuMessageSelectLF` | `FontBaseWidth` doubled `add eax,eax` (`002B3015`); `SelectLF` → `xmm0` float (`002B2F5D`) |
| `002B2C50` (→`002AC5F0`→`002B5730`→`00556F90`) | `FontBaseWidth` | `eax` doubled → `cvtdq2ps` — char-width measure inside the control-code walk (`002B2C7F`) |
| `0035E070` P (message window, installed by `0035DF40`) | `FontBaseWidth` | `(FontBaseWidth + 2) × 0x19` — the window's column pitch (`0035E3FE`) |
| `002BDCE0` (→`0028E220`→`0035C630`→`00253780`, the battle log) | `ActiveLogMoveY`, `ActiveLogDispHelpMoveY`, `FontBaseHeight` | `MoveY` → `edi` scroll base (`002BDE0A`); `DispHelpMoveY` added to `ecx`/`cx` — the help-line Y (`002BDE5C`); `FontBaseHeight` ×3 via `lea ecx,[rax+rax*2]` — three-line block height (`002BDED1`) |
| `002BE4F0` P (battle log) | `ActiveLogMoveY`, `ActiveLogDispHelpMoveY`, `FontBaseHeight` | `MoveY` → `ebp` (`002BE586`); `DispHelpMoveY` → `ecx`/`edx` (`002BE5DA`); `FontBaseHeight` → `eax` pitch (`002BE553`) |
| `002BF230` (→`002BE4F0`) | `ActiveLogMessageOffsetX` | `edx + key` → `002D8650` — the log message's X (`002BF36D`) |
| `002BF690` P (help message) | `HelpMessageMoveY` | `ecx` = key → `002BED00` — the help text's Y (`002BF77A`) |
| `002D66D0` P (auto window) | `AutoWindowFontOffsetX`, `AutoWindowFontOffsetY` | `edx`/`r8d` → the auto-prompt's text origin (`002D68D3`, `002D68CC`) |

## What is not known

- The dispatch interiors of `002A6190` (ids 1–4, 10, 12, 15, 18, 21) beyond the layout reads above.
- Which of the `MsgWin…` windows is which on-screen surface (the game shows several message-window
  shapes — caption, select, log, item-get — and the key names track the shapes, not the screens).
- `00227EE0` P (`GeneralFrame`/`MessageLine`/`NobuMessage` keys per the atlas, ids 1, 2, 4) reads
  its frame keys through the `002475D0`/`00247680` helpers documented on
  [the shared-dialogs page](../Shared-Dialogs/the-shared-dialog-widgets.md), not directly.

## Falsification pass — 2026-09-14 (OPUS)

This page had no falsification pass and was the last of three documents in the database without one.
Its claims are checkable to the instruction, so the attack was to go to the cited addresses in the
shipping bytes, and then to ask how the seven `P` procedures are reached at all.

### Twelve cited instructions attacked, eleven exact, one off by four bytes

| cited | claimed | at that address |
|---|---|---|
| `002A2DC4` | offsets `add`ed into `[rbp-0x58]` | `mov eax, [0209C4B0]`, `add [rbp-0x58], eax` |
| `002A803C` | `ecx − key − eax` | `sub ecx, [01E0CDD4]`, `sub ecx, eax` |
| `002A8371` | `ecx − key` | `sub ecx, [01E0CDD0]` |
| `002A3D5B` | `edx + key` | `add edx, [01E0CDA4]` |
| `002A6E43` | `eax − MessageWinMaskBottom` → `[rsi+4]` (window Y = 448 − height − bottom gap) | `sub eax, [01E0CDA8]`, `mov [rsi+4], eax` |
| `002A6E51` | `ax − MaskTop` → word | `sub ax, word [01E0CDA4]` |
| `002B3015` | `FontBaseWidth` doubled | `mov eax, [01E0CDC0]`, `add eax, eax` |
| `002B2C7F` | `eax` doubled → `cvtdq2ps` | `mov eax, [01E0CDC0]`, `add eax, eax` |
| `0035E3FE` | `(FontBaseWidth + 2) × 0x19` | `mov eax, [01E0CDC0]`, `add eax, 2` |
| `002BF36D` | `edx + key` | `add edx, [01E0CE9C]` |
| `002D68D3` | `edx` ← key | `mov edx, [0209E670]` |
| `002A837B` | `lea rdx, 002A86A0` | **not an instruction boundary** — see below |

**The one correction.** `002A837B` disassembles as `add eax, [rax]`, which is the middle of
something else. The instruction is real and does exactly what the page says, but it **begins at
`002A8377`**: `lea rdx, [rip + 0x322]` → `002A86A0`, seven bytes, followed by `sub ecx, eax` at
`002A837E`. The cited address landed four bytes inside its own instruction, in the `disp32`. The
claim survives; its coordinate did not.

### How the seven `P` procedures are reached — and this page's own sentence corrected a neighbour

None of the seven has a caller in `edges.tsv`, which is expected: a widget procedure is installed,
not called. Three mechanisms account for all of them, and this page already named the third one.

| procedure | stored 32-bit RVA (excl. **all** unwind data) | `E8`/`E9 rel32` | rip-relative `lea` |
|---|---|---:|---|
| `002A6190` | **none** ~~2~~ | 0 | `002A2C10` |
| `002A3960` | **none** ~~2~~ | 0 | `002A7390` |
| `0035E070` | **none** ~~2~~ | 0 | `0035DFC5` |
| `002BE4F0` | **none** ~~2~~ | 0 | `002BDE78` |
| `002D66D0` | **none** ~~2~~ | 0 | `002D7B7C` |
| `002A86A0` | **none** | 0 | `002A8071`, `002A8191`, `002A8377` |
| `002BF690` | **none** | 0 | `002BF604` |

> **Corrected 2026-09-16 (FABLE) — `FINAL-AUDIT-PROTOCOL` pass 6, and the table is stronger for it.**
> The header said *"excl. `.pdata`"*. That exclusion is **true and incomplete**: `.pdata` holds one
> copy of a function's unwind records and a second lives in `.rdata`, **chained** behind an
> `UNWIND_INFO` whose flags carry `UNW_FLAG_CHAININFO`. **All ten addresses this column listed were
> fields of those records**, and each record's `Begin` is **the procedure in its own row** — so they
> were never references to these procedures, they were the procedures' own unwind metadata.
> The same correction was made to
> [the battle-hud layout readers](../Battle-Hud/the-battle-hud-layout-readers.md) the same day, from
> the same table shape and the same header.
>
> **What it does to the finding: it simplifies it.** The section opens *"Three mechanisms account for
> all of them"*. With the column emptied, **all seven procedures have zero stored RVAs and zero
> `rel32`, and every one has a rip-relative `lea`** — so it is **one mechanism, uniformly**, and the
> paragraph below already shows every `lea` matching an installer this page names. The five that
> looked different from the last two were not different.
>
> **The addresses are removed rather than struck.** The evidence checker cannot tell an address cited
> *as* evidence from one cited as an example of what does not count, so discussing a banned address
> must not look like using one; the counts keep their old values struck instead.

**Every `lea` site matches the installer this page names.** `002A2C10` is inside `002A2C00`, the hub
the page says installs `002A6190`. `002A7390` is inside `002A70B0`, which the page says installs
`002A3960`. `0035DFC5` is inside `0035DF40`, `002BDE78` inside `002BDCE0`. The two procedures with no
stored RVA — `002A86A0` and `002BF690` — are reached **only** by `lea`, which is why nothing points at
them from data.

**This page corrected the sibling page's falsification pass.** The attack on
[the battle-HUD readers](../Battle-Hud/the-battle-hud-layout-readers.md) looked for stored RVAs and
`rel32` only, reported three readers as having no reference of either kind, and wrote that up as a
finding. It was this page's `lea rdx, 002A86A0` sentence that named the missing mechanism; adding
`REX.W 8D /r mod=00 rm=101` to the scan found all three installed, and the finding was withdrawn
before it was published. **The scan had a positive control for calls and none for installations**,
which is the whole of the mistake.

**What this does not establish.** Three mechanisms explain all seven here and all nine there. A
target computed by arithmetic from a base, or an entry held as an offset rather than an RVA, would
still be invisible to this scan — a fourth mechanism is not ruled out, it is simply not needed.

## The id-2 arm of `00556F90`, read 2026-09-18 (FABLE) — how the message text is fed

`00556F90` dispatches on the message id (`00556F9D`–`00556FB0`: 1 → `00557087`, 2 → `00556FC8`, `0x12` → `005571AF`, anything else to the default `005C5230`). The id-2 arm compares the **requested page** byte `+0x3D1` with the **shown page** byte `+0x3D2` and returns at once when they agree. Otherwise it resolves two low-pool text rows through `002F9860`: **`0x3ED + page`** is the title, stored as the string pointer at the child object's `+0x18` (`[+0x60] + 0x20`) with its encoded image address at `+0x20` (`00556FF6`–`00557006`); **`0x838 + page`** is the body, which a three-pass loop wraps into **three 256-byte lines** at `+0xD0`, `+0x1D0` and `+0x2D0` — each pass clears the line, calls `002B5730(256, line, text)` and advances the source by the count it returns (`00557030`–`00557061`). It then latches `+0x3D2 = +0x3D1` (`00557074`) and returns 0. So the message window's text is not pushed to it: the arm pulls a title row and a body row by page number from the low text pool and re-wraps the body itself. Static: the arm decoded in full.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

- **CoreRuntimeScheduling — MECHANICAL (5 edges).** `RuntimePointer_EncodeImageAddress` (`0020E620`, 2), `001EDEC0`, `ImageAddress_ResolveRuntimePointer` (`0020E600`) and `00229E40` are the shared pointer/address helpers every UI body carries. Fan-in, not a scheduling relationship.
- **Audio — MECHANICAL (3 edges).** `002A3960`, `002A6190` and `002A70B0` each call `00249C60`, the shared Audio helper the shared-neighbours page measures at 99 callers. One accessor, not three relationships.
- **Resource — SERVICE (2 edges).** `00253780` calls `00249580` and `00249180` — the resource fetch behind the message-window content path. The crossing is those two calls, not shared ownership.
- **Gameplay — SERVICE (1 edge).** `0035E070` calls `0031C5D0` (BattleEncodedId definition-resolution validation) — a single shared-helper call.
- **Save_Load_Settings / SaveLoad — MECHANICAL (5 edges).** `SaveLoad_ControllerLifecycleHandler` calls `001EDEC0`; `SaveLoad_ControllerTransitionStateMachine`, `00581350` and `005819A0` call `00249C60`; `00582790` calls `00249580` — the save layer consumes the same pointer/audio/resource helpers this page's readers use. Fan-in, not a save relationship.
- **Rewards_Progression_Economy — MECHANICAL (1 edge).** `EnemyChain_UpdateOnDefeat` calls `00229E40`, the shared helper cited above. Single shared-helper caller.
- **Input — MECHANICAL (1 edge).** `00247950`, a shared helper this page's readers call, is consulted by that layer. Fan-in, not an input relationship.
- **ActorEntity — MECHANICAL (1 edge).** `00203170`, the shared rect-build helper this page's `002D8550` calls, is also called by `003F1E90`. Single shared-helper caller.
- **Movement — MECHANICAL (20 edges).** `00203170` again — the same rect-build helper is consulted by twenty Movement bodies (`0022EF20`, `00230790`, `0026EB30`, `00334220`, +16 more). Fan-in to one accessor, not a movement relationship.
- **Script_VM_Native_Bridge - CLIENT (5 edges).** `00203170`, `00229E40`, Inventory_GrantEncodedLootItem (`00300B80`), `0035DF40` are called by bodies filed to Script_VM_Native_Bridge: `0033FED0`, `0034BA00`, `00356160`, `0050FAF0` - shared machinery across the layer boundary, no shared ownership.

*(SWE2-CONTRACT 2026-09-15 — edge counts from `edges.tsv`; helper identities from `functions.tsv`. SWE2-EC7 2026-09-20 — `00203170` fan-in entries appended.)*

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Presentation — CLIENT and SERVICE, 16 edges.** Cited readers are called by Presentation bodies, among them the two `0xBC08` map-screen pages and bodies of 1,420, 1,422 and 2,882 bytes. They call `RenderCommand_SubmitCurrentBufferAndSwap` and two larger Presentation bodies (1,363 and 6,441 bytes).

**Items_Equipment_Shops_License — SERVICE (SWE2-EC7-168, 1 edge).** `002A5330` — the typed
getter this page measured — calls `00300B80` on the items layer. Consultation, not shared
ownership. Edge list from `edges.tsv`.

## SWE2-EC7-38 update (2026-09-19) - `002A6A80`

`002A6A80` (447 B) is a message-window layout reader - `01E0C1D8`/`01E0C1DC`, `0039C480` pair plus `002AC2B0`/`002B39D0`/`002B32C0`/`002A5590`/`00247810`. Interior anchor `002A6AA1` (a `0039C480` call).

## SWE2-EC7-39 update (2026-09-19) - `00474100`

`00474100` (404 B) is the `TalkingMessage`/`NobuMsg` endpoint the page names - `0208EA28`/`02CA6C78`, `002A27C0`/`00245020`/`001829C0`/`00244960`/`00247950`/`00861EBA`/`0039C480`. Interior anchor `00474133` (a `002A27C0` call).

## SWE2-EC7-59 update (2026-09-19) - `002B39D0`

`002B39D0` (164 B) is a message-window layout reader - `00861ED2` single call. Interior anchor `002B3A44` (a `00861ED2` call).


## SWE2-EC7-99 update (2026-09-20) - `002D8550` measured

`002D8550` (245 B) is the modulated-quad publish
`00227EE0` calls: the record's RGBA bytes at `+0x90`
through `+0x93` scale by `word[+0x5A]` in 128ths (`imul` +
`sar 7`) and land at `+0x94` and `r9+0x30`, `00203170`
builds the rect on the stack, the two integer extents
convert to floats at `+0x60`/`+0x64` for `00397910`, and
the out record takes `qword[+0xB8] = 0x3001` with `+0x20`
pointing at the staged rect before `002AF960` submits -
the colour-scaled quad write message windows run per
pane.
Interior anchor `002D860E` (the `0x3001` stamp).

## SWE2-EC7-100 update (2026-09-20) - `002BFB40` measured

`002BFB40` (471 B) is the banked-slot fill `002BF4F0` and
`002BF690` call: a stale `+0x4D8` pointer migrates to
`+0x4E0`, `rbp = rcx+0xD8 + byte[+0x4E8] * 0x100` selects
one of four `0x100` banks, `00273A20` gates (a miss runs
`00245020` and returns 0), the bank index advances mod 4,
two `0029CD90` measures stage `+0x20`..`+0x30` fields on
`rsi` (`setg` bound, `+0x10FC`/`+0x10FE` cleared), and
`00245000` posts the bank through `00244960` before
`+0x4F0` takes `[rsi+0x10]` - the rotating-bank publish
the window readers run.
Interior anchor `002BFC25` (the first `0029CD90` call).

## SWE2-EC7-101 update (2026-09-20) - `002ABEC0` + `002A8550` + `002A3730` measured

`002ABEC0` (83 B) is the gated dispatch `00227EE0`,
`00241D40`, `002A3730`, `002A7720` and `0057C480` call:
`byte[+0xAC] == 1` or a nonzero `dword[01E0CDC8]` lets
the `002ABF20` sequence run - `0209CC40` `+0x10D8` pen
store, `0209CC48` clear, `byte[+0xA3]`-keyed `009164C8`
vtable jump with `edx = 0` - otherwise it returns - the
enable-check the window arms gate their dispatch on.
Interior anchor `002ABEFD` (the vtable index).

`002A8550` (285 B) is the ten-arm picker `002A7F70` and
`002A8220` call: `ecx - 1` bounds an image-relative jump
table (`002A8670`) whose arms set an `edx` count and a
`ebx` pick, `0029DA70` builds the entry list, the
`ebx`-th `24`-stride entry's `+0x48` string is compared
against `002AC280`'s first word (a `003FFAB0` skip walks
past the name on a match), `002F9860(0x467C)` fetches
the row, `002B4090` formats `0x80` bytes into the stack
record and `002B3050` resolves it to `word[+0x34]` -
the pick-format-resolve chain the readers expose as an
id lookup.
Interior anchor `002A8580` (the jump-table load).

`002A3730` (220 B) is the mode-gated refresh `002A2C00`,
`002A3250` and `002A38C0` call: `dword[+0x44] & 0x180000`
must equal `0x180000` to enter; `byte[+0x3C5]` arms to
`0x80`, a six-arm jump table on `byte[+0x180] - 1` loops
`002ABEC0` dispatches (one arm sets `word[+0x158] = 1`
first) or `002B3950`/`0016D6A0(0x40000)` exits, and a
nonzero `esi` afterwards runs `002A36A0` - the
state-byte loop the window refresh drives.
Interior anchor `002A3790` (the dispatch loop head).

`002A5CC0` (638 B) is the layout recompute the message-window proc `002A6190` calls: `002D3900` on `[rcx+0xC0]` then `002B3930` on `rdi = rcx+0xD0`, whose result bit 0 is rewritten into `+0x3E8` bit 0x200000; `byte[+0x3C5]` gates `+0xB0` bit 0x80000000, `+0x3E8 & 0x101000` against the `+0xB0` byte selects the `002B28B0`/`002A69E0`/`002B28F0`/`00249C60`/`002A27C0`/`002A5020`/`002B1E20` arms - the window's state-driven relayout.

Interior anchor `002A5CE5` (function `002A5CC0`).

`002B3930` (32 B) is the byte-indexed dispatch the relayout `002A5CC0` and `0057C480` call: `movsx byte[rcx+0xA3]` x3 selects one of the `009164C0` table's three-pointer rows and a non-null slot is tail-jumped - the control's three-way handler switch.

Interior anchor `002B393C` (function `002B3930`).

`002A5020` (783 B) is the per-item emit the relayout `002A5CC0` and the re-query arm `002A5F40` call: cookie frame, `0017F880` supplies the time float, `byte[r13+0x3C2]` bounds the loop which stages the `rcx+0xD0` 0x80-byte record onto the stack, then `002B2880`/`002B28F0`/`002B2930`/`00808C40` paint each entry - the window's list painter.

Interior anchor `002A5168` (function `002A5020`).

`002A5F40` (588 B) is the re-query arm the message proc `002A6190` runs: `002B2880`/`002A69E0` read `0209C630`, `word[02F9736A] & 01E0C2A4` and `0209C618 & 3` gate a second `002B27E0`/`002A69E0` pair on `rdi+0xD0`, `+0x3E8` loses 0x500 and gains 0x200, `(byte[+0x180]-2) & ~2` swaps `+0x180`/`+0x181`, `byte[+0x3D6]`/`dword[+0x3D8]` reset and `00249C60(3)` arms - the proc's mode refresh.

Interior anchor `002A5F9D` (function `002A5F40`).

`002A69E0` (157 B) is the scroll-step arm the relayout `002A5CC0` and re-query `002A5F40` call: `+0x3E8` bit 0x100000 gates, `0017F880`'s float x3 is clamped against `edx`, `+0x3D0` detects change, `+0x80 & 2` gates again, then `00247260(rdi, movsx word[+0x9C], esi, 2, 0x96, 1)` fires and `word[+0x164]`/`+0x166` store - the window's page step.

Interior anchor `002A6A5A` (function `002A69E0`).

`002A6F80` (301 B) is the tick accumulator `002A2C00` calls: `rdx` out takes `+0x14`/`+0x18` = `0xC8`; `rcx`'s `byte[+0x180]` swaps into `+0x181` and clears; `byte[+0x3BB]==3` runs `0039C4A0((+0x114>>0xB)&1)`, subtracts `01E0C1D8 - [rdi+8]` into `rdi`, adds `(5 - byte[+0x3B9]) x 0017F880`'s float to `rdi+4`, then scans `0209C4D0`..`0209C510` for a record equal to `rbx` or flagged `+0x3E8 & 0x2000` - the window's per-frame cost step.

Interior anchor `002A6FDD` (function `002A6F80`).

`002A5330` (300 B) is the typed getter `002A2C00` calls: `0039BB20` returns the record array and `ecx` clamps to `[0, dword[rax])`; `byte[rec+0xB]-1` selects five arms - `0035D330` lookups `(0xD, word[+6]<<0x10)`, `(2, word[+6])`, `(0x14, word[+6])` then `002B58B0` on `[rax+0x18]` produce the value - the window's per-kind field read.

Interior anchor `002A53AD` (function `002A5330`).

`00242970` (272 B) is the packed-record read `002A4170` runs on the caption geometry: `0039BB00`'s object gives `rbx = [+0x20] + 0x30`, `word[+0x10]` relocates the entry base and `word[rbx + word[+0x14] x 2 + 0x20] + edi` selects the 8-stride record; `dword[+4]` splits into two 12-bit fields (`& 0xFFF` low, `>> 0xC` high) staged at `rsp+0x60`, `byte[+7]`'s high nibble indexes `[+0x20]+0x30`'s `word[+0x12]`-offset byte table plus the low nibble into `byte[r14+0x5C]`; `002D8BB0` frames it, `002D8CB0(r14, r15, &pair, ebp - low, (esi - high) >> 1)` consumes the centred extents, and `002D8BB0` closes - the caption-offset half of the message window's draw origin.

Interior anchor `00242A5A` (function `00242970`).

`00242870` (252 B) is the sibling packed-record read `002A4170` runs through `0035D3D0`'s object: same `[+0x20] + 0x30` header, `word[+0x14]`-indexed select plus `word[+0x10]`-rebased `x 8` records, three u16s staged and the `+4` dword split `& 0xFFF`/`>> 0xC`, `002D8BB0`/`002D8CB0` framing and consuming - the `r9d`-indexed half of the same layout-row reader `00242970` documents.

Interior anchor `00242894` (function `00242870`).

`002A30B0` (243 B) is the slot-tag populate `002A2C00` runs: `[rcx+0x1B0]` non-null and `edx <= 0x1F` gate, the `x16` slot at `rcx+0x1B8` receives `{[rbx], [rbx+8]}` from the `[r9 + rdx*8]` pair, and `eax <= 0xF` dispatches the `001831A4` jump table - arms write tag `0`/`1`/`2` with payloads of raw `r8d`, `00253710(ecx)`, or `0035D330` -> `[rax+0x18]` -> `002B58B0`, and out-of-range zeroes the pair - the message-window cell writer.

Interior anchor `002A313F` (function `002A30B0`).

`002B3A80` (158 B) is the delimiter-bounded token search: `strlen(rdx)` is taken once, `rcx` is walked byte-wise until `r8b`; each position whose first byte matches and whose remaining length exceeds the needle's runs `00861ED2` for the full compare, and a hit returns the position pointer - the terminator-aware substring scan the input and message-window callers share.

Interior anchor `002B3AE4` (function `002B3A80`).
