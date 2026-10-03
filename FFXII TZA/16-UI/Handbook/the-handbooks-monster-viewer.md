---
system: The handbook's monster viewer, end to end - from a MonsterId entry of the gallery file to a model that is never culled and is drawn only in the menu frame
category: 16-UI
status: AUDITED
owner_layer: PrimaryOwner:UI
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the open and close wrappers 001846F0 and 001846B0, the viewer singleton's three methods 001EB7B0, 001EB9C0 and
    001EB940, the staged loader 002EE430 with its request 002EE9C0, close 002EEB20, hand-over 002EED80 and per-tick tail
    002EF050, and the model-instance container pass 00477F20 with its two callbacks disassembled from the authority
    image and read whole, 2026-09-19; the entry reader 001C6320 read at its head, its tail and every call in between
    (the light arithmetic 001C65A0..001C6940 by its calls only); its forty key strings read out of the image
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-monster-viewer-falsification-pass-1
  crossref_clean: true
  reopened_count: 0
  note: written by FABLE. Started from two of FRONTIER's uncited bodies (004781E0, 004781A0) and one flag nobody had
    named (render record +0x6E0). Static. Corrects the 2026-09-12 Y-7 answer of mine that the gallery file's reader was
    "not found", and answers the settings page's residue "what that handle is". Not read - the pane's own drawing of
    the viewer, the camera and light setters, the motion binders of loader states 6 and 7; pending first review  promoted: 2026-10-01 DOCUMENTED -> AUDITED by SWE2-AUDIT-SPEC (FRONTIER eligibility census sweep): falsification record opus-monster-viewer-falsification-pass-1; audit_crossrefs at HEAD reports 0 unresolved findings; cross-subsystem neighbours dispositioned in their section; killer observations recorded in the pass; promoter is not the last substantive author (last substantive commit: OPUS)
---

# The handbook's monster viewer, end to end

Open a bestiary page in the handbook and a monster stands there, lit, posed, holding its weapon. Five things the
database already knew separately turn out to be one mechanism:

- the gallery file with its 384 `MonsterId` entries
  ([UI layout parameters](../Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md), Y-7 - *"the readers
  are not found"*);
- a 2,261-byte "monster-record property fill" with those key names in it;
- a handle the settings page could not identify, whose "open" byte feeds the half-rate predicates
  ([game settings](../../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md));
- a render-record field, `+0x6E0`, that cancels all three cull tests
  ([how a character fades](../../17-Presentation-Rendering/Character-Render-Records/how-a-character-fades-the-ten-channels.md));
- and a frame mode, 3, that the world-tick page calls *the full-menu frame*.

## 1. Opening - the pane, `001846F0` (75 B), `001EB7B0` (79 B), `001EB9C0` (114 B)

The handbook text pane opens the viewer when a page's **kind byte is 5**, passing the page's 16-bit **monster index**.
`001846F0` saves the cubemap intensity (`02CB8138`) and sets it to 0 - **the viewer turns environment reflections off
while it is up** - then hands the index to the viewer singleton (`01F82E18`, `0x2E0` bytes). `001EB7B0` stores the index at
`+0x11C`, closes any model already open, and falls into `001EB9C0`, which:

1. calls the entry reader (section 2) and gets back the **model id**;
2. if that differs from the one open (`+0x120`), asks the staged loader (section 3) for it - model id, **mode 1**,
   the entry's weapon ids (`+0x124`, count `+0x12C`) - and keeps the returned slot at `+0x130`;
3. raises the byte **`+0x118` - "the viewer has a model open"**. That byte is the state behind the settings page's
   half-rate predicates, and it is what the loader asks before handing a finished model over (section 3).

`001846B0` is the way out: `001EB940` closes the slot, clears `+0x118`, and the cubemap intensity is restored.

## 2. The entry reader - `001C6320` (2,261 B)

**This is the reader of `monstergallery.json`'s keys** - the parsed tree lives in the object at `01F81308`. It formats
`MonsterId%d` from the singleton's `+0x11C`, fetches that node, and returns -1 if there is none. Then, key by key, it
reads an int or a float and pushes it into the singleton. **Nine keys fall back to the `Common` node when the entry
lacks them** - `eyeVfxZBias`, `lightAmbientA`, `variation`, `clut`, `motionRate`, `bgColorR`, `bgColorG`, `bgColorB`,
`drawBgColor` - and the rest are read from the entry alone. The keys:

`monsterWeaponIndex`, `monsterWeaponIndex2` (weapon slots 0 and 1; the second only if present), `motionIndex`,
`motionRepeatFrame`, `motionRate`, `xOffset`, `yOffset`, `modelScale`, `cameraPitch` (`+0x240`), `cameraYaw` (`+0x244`),
`cameraFov`, `eyeVfxZBias`, `variation`, `clut`, the ambient light (`lightAmbientIntensity`, `R`, `G`, `B`, `A`), two
directional lights (`light1/2ColorIntensity`, `ColorR/G/B`, `DirX/Y/Z`), `bgColorR` / `G` / `B` (`+0x260`..`+0x268`),
`drawBgColor` (`+0x26C`) - and last **`monsterModelId`, which is the return value**.

## 3. The staged loader - `002EE430` (1,390 B) and its four companions

One model is loaded at a time, across frames, by a state machine on the global `01EEBAA8` (**8 = idle**). The world
tick runs it every tick; `002EE9C0` (343 B) files a request - **one active and one pending**, `0x30` bytes each at
`02164210` - and returns one of **ten slots** (`01EEBAB0`, a render-record index per slot, -1 = free).

| state | what happens |
|---:|---|
| 0 | the body model's resource is requested |
| 1 | when it is loaded: a character render record is created for it and stored in the slot; in mode 1 **the record's `+0x6E0` is set to 1** |
| 2 → 3 | first attachment, if any: the weapon id is resolved - an equipment id goes through the equipment row's model field `+0x30`, a raw resource id (bits `0x770000`) is used as is - requested, and when loaded attached to the body record (its record kept at `02164220`, flagged the same way) |
| 4 → 5 | second attachment, the same (`02164224`) |
| 6 → 7 | the motion set that goes with the weapon is looked up, loaded and bound to the body record |
| 8 | idle: `002EED80` (290 B) runs once per finished load |

`002EED80` is where the pane and the loader meet again. **In mode 1 it first asks whether the viewer is still open**
(the `+0x118` byte): if the player has already turned the page, the slot is closed at once. If a pending request is
waiting for a different model, the finished one is closed, the pending request becomes the active one and the machine
restarts at 0. Otherwise the record index is handed to the viewer singleton, which is what the pane then draws.

`002EEB20` (416 B) closes a slot - only while the machine is idle: it frees the body record and each attachment record
and drops each resource's use count (`+0x1C`), releasing a resource nobody else holds.

`002EF050` (165 B) is the per-tick tail: every slot whose record has **`+0x6E0` = 0** has the angle at its `+0x124` advanced by a ~~fixed~~
step (`0215FD40`) *(corrected 2026-10-02, OPUS: not a constant — `0215FD40` lies past the image's file data and has no direct writer; its only references are the reads `002EEED0` and `002EF050+0x45`)* and wrapped at 2π - **a turntable**. Mode-1 models are exempt: the handbook poses
its monsters by the file's `cameraYaw`. *No requester of mode 0 was found in the image - `001EB9C0` is the loader's only
caller and passes 1 - so the turntable is dead in this build.*

## 4. What `+0x6E0` does to drawing

So `+0x6E0` means **"this record belongs to the monster viewer"**, and it has three readers:

1. the distance fade and cull: a viewer model **cancels all three cull tests** (the fade page);
2. the turntable above;
3. **the model-instance container pass `00477F20` (261 B)**, which decides per instance whether to draw:

   | frame mode (`02064AD3`) | drawn when the owner record's `+0x6E0` is |
   |---|---|
   | 3 - the full-menu frame | **1** |
   | anything else | **0** |

   **In the menu only the viewer's model is drawn; in the world it never is.** That is the whole isolation between the
   bestiary monster and the field behind the menu: one flag, tested against the frame mode.

The pass itself, in its mode 0 (container byte `+0x62`): every active entry is inserted by the callback `004781E0`
(138 B) into a singly linked list **sorted ascending by the entry's key `+4`** (head at container `+0x60`, next index at
entry `+2`; an entry goes after its equals), and the list is then walked in that order, stamping each entry's `+0xB2`
from container `+0x66` and applying the gate above. In mode 1 the callback `004781A0` (59 B) instead queues each active
entry into the sorted display list with key `+4 >> 4` - **and the draw callback it queues is the image's folded empty
function**, so that path draws nothing in this build.

## 5. What a reimplementation must keep

- A bestiary page of kind 5 names a `MonsterId`; nine of its keys fall back to `Common` (section 2).
- Loading is asynchronous, one model at a time, with one request of look-ahead; a model whose page has been left is
  discarded on arrival rather than shown.
- Viewer models are never distance- or frustum-culled, are drawn only in frame mode 3, and ordinary models are not
  drawn in frame mode 3 by this pass.
- Reflections are off while the viewer is open.

**Not read:** how the pane draws the record it is handed; the singleton's camera, light and offset setters; loader
states 6 and 7's motion binders; what else, if anything, draws ordinary characters under the menu frame.

## Evidence

| body | interior anchors |
|---|---|
| `002EE430` staged loader (1,390 B) | `002EE43D`, `002EE454`, `002EE485`, `002EE4BB`, `002EE4D9`, `002EE568`, `002EE586`, `002EE5A2`, `002EE5E6`, `002EE5F0`, `002EE64A`, `002EE650`, `002EE69C`, `002EE6A7`, `002EE6CA`, `002EE6FE`, `002EE71A`, `002EE734`, `002EE74D`, `002EE7BE`, `002EE815`, `002EE831`, `002EE88B`, `002EE8A6`, `002EE8B8`, `002EE906`, `002EE941`, `002EE959`, `002EE95E`, `002EE975`, `002EE98A` |
| `002EE9C0` request (343 B) | `002EE9EA`, `002EE9FE`, `002EEA27`, `002EEA45`, `002EEA60`, `002EEA84`, `002EEAB3`, `002EEAD0`, `002EEAE5`, `002EEAF5` |
| `002EEB20` close (416 B) | `002EEB24`, `002EEB4C`, `002EEB59`, `002EEB60`, `002EEB75`, `002EEB88`, `002EEB93`, `002EEBC3`, `002EEC11`, `002EEC19`, `002EEC65`, `002EEC8B`, `002EECAB` |
| `002EED80` hand-over (290 B) | `002EED84`, `002EEDA9`, `002EEDB8`, `002EEDD3`, `002EEDE6`, `002EEDF9`, `002EEE58`, `002EEE5E`, `002EEE87`, `002EEE93` |
| `002EF050` per-tick tail (165 B) | `002EF066`, `002EF087`, `002EF08C`, `002EF09D`, `002EF0A8`, `002EF0CE` |
| `001C6320` entry reader (2,261 B) | `001C6357`, `001C635C`, `001C6393`, `001C63A6`, `001C63B1`, `001C6402`, `001C6444`, `001C6465`, `001C6486`, `001C650F`, `001C652E`, `001C656C`, `001C659B`, `001C694D`, `001C6AC1`, `001C6B61`, `001C6BBA`, `001C6BC8` |
| `00477F20` container pass (261 B) | `00477F43`, `00477F57`, `00477F6E`, `00477F78`, `00477F7F`, `00477FA6`, `00477FB5`, `00477FD0`, `00477FE0`, `00477FFA`, `00478006`, `0047800B` |
| `004781E0` sorted insert (138 B) | `004781F4`, `00478205`, `00478209`, `00478218`, `00478220`, `0047823A`, `00478244` |

Under 128 bytes, read whole: `001846F0`, `001846B0`, `001EB7B0`, `001EB9C0`, `001EB940`, `002EF010` (the gate's read of
`+0x6E0`), `004781A0`. The key strings are at `008FB3E0`..`008FB658` (`MonsterId%d` first, `monsterModelId` last) and
`Common` at `008FA3CC`. Jump table of the loader: `002EE9A0`, eight arms.

## Cross-subsystem neighbours

**Presentation - SERVICE.** `00477F20`, `004781E0` and `004781A0` are Presentation-layer bodies: the container pass and
its callbacks. This page reads them for the one test they make on the viewer's flag; the render record, its creation
and its attachment calls are the Presentation layer's, described by role.

**Developer - FILING (crossing).** The entry reader `001C6320` is filed under the Developer layer in the function
graph, although what it reads is the shipped `monstergallery` data for the shipped handbook; the viewer's fill routine
`001EB9C0` calls it. The edge is recorded because both are cited here; the filing looks like a mislabel and is left to
the layer's owner.

**Core runtime scheduling - SERVICE.** The open and close wrappers call one scheduling-layer routine before touching
the viewer, and the container pass reads the frame-mode byte through that layer's eight-byte getter
([the shared neighbours](../../00-Engine-Core-Runtime/Shared-State-Accessors/the-shared-neighbours-pass-22-keeps-finding.md)).
By role.

**World / Area / Field - CLIENT.** The loader's tick is called from the world simulation tick every frame; the crossing
is that call, and nothing about the world is read by it.

**Resource - SERVICE.** The loader requests model resources and releases them through the Resource layer's table,
by role.

**Items, equipment - SERVICE.** A weapon id that is an equipment id is turned into a model through the equipment row's
model field; the equipment table is that layer's.

**ActorEntity - MECHANICAL (SWE2-EC7-97, 1 edge).** `002EC6B0` — a caller this page's
`002EDE20`/`002EDD20` section names — is itself reached through `0037B4D0` on the ActorEntity
layer. Shared-caller fan-in; no ActorEntity relationship to the viewer.

**Movement - MECHANICAL (SWE2-EC7-97, 1 edge).** The same `002EC6B0` is reached through
`002E28E0` on the Movement layer. Shared-caller fan-in; no Movement relationship to the viewer.

**Script_VM_Native_Bridge - MECHANICAL (SWE2-EC7-97, 2 edges).** The same `002EC6B0` is reached
through `0034B120` and `0050D660` on that layer. Shared-caller fan-in; no bridge relationship
to the viewer.

## SWE2-EC7-81 update (2026-09-20) - `00537B10` parameter-pair setter measured

`00537B10` (141 B) is the `(ecx, edx)`-armed writer on the
`02EBA460`/`02EBA468`/`02EBA464`/`02EBA46C` globals: `(0,0)` folds
`022D8EAC * 022D8EB4 * 12` into `02EBA460`, `(0,1)` forces
`0x3C0000` into `02EBA468`, `(1,0)` stores `r9d` to `02EBA464`,
`(1,1)` selects `r8d` else `02EBA468` into `02EBA46C` - the viewer's
scale/dimension pair the `00477F20` caller writes.
Interior anchor `00537B44` (the `imul` fold).

## SWE2-EC7-86 update (2026-09-20) - `003EC580` gated slot lookup measured

`003EC580` (40 B) is the indexed slot fetch the monster-viewer
callers run: `-1` yields 0; otherwise `index*0x740 + [022C6F28]`
locates the slot and `dword[+0x284]` must be non-zero - the
occupied-row guard on the 0x740-stride table.
Interior anchor `003EC59D` (the `+0x284` occupancy test).

## SWE2-EC7-97 update (2026-09-20) - `002EDE20` + `002EDD20` measured

`002EDE20` (68 B) and `002EDD20` (68 B) are the twin field
writers `002EC6B0` and `002EE430` call: the same `word != -1` /
`0x740`-stride / `+0x284 != 0` resolve, then `0020E620(rdx)`
lands in `+0x430` (first) or `+0x42C` (second) - the paired
dword writes the viewer's fetch path applies.
Interior anchors `002EDE4F` and `002EDD4F` (the `0020E620`
calls).

## Falsification pass 1 — 2026-09-29 (OPUS): every section tested survives; four additions

**Attack.** Sections 1, 3 and 4 were turned into checks at their instructions. The competing case was "some other
requester uses mode 0", since the turntable depends on it. Script: `Tools/analysis-kit/gfz-scripts/falsify_monster_viewer.py`,
output `falsify_monster_viewer.out`, image `73461d08…`, 0 BROKEN, exit 0.

| # | Clause attacked | Result |
|---|---|---|
| M0 | sizes | **survives**: all ten |
| M1 | section 1: reflections off while open | **survives**. Both wrappers also call `0018CCF0` on the object `0018CA40` returns: with 0 on open, 1 on close. What it toggles was not read |
| M2 | section 1: open and request | **survives, with an addition.** The request passes two more words, `+0x138` and `+0x13C`. It is filed only when the model id differs from `+0x120`, and only then is `+0x118` raised. **An index with no `MonsterId` entry returns -1, equals the closed `+0x120`, and loads nothing**: the viewer stays closed |
| M3 | section 3: "no requester of mode 0" | **survives** (the competing case fails). One call edge reaches `002EE9C0` (`001EBA05`, `edx` 1), and no data reference names it |
| M4 | section 3: mode-1 records flagged | **survives**. `+0x6E0 = 1` at three sites: the body and both attachments |
| M5 | section 3: the turntable | **survives, with an addition.** The step `0215FD40` is **not a constant**. It sits in uninitialised data, and its only rip-relative accesses are two reads: the getter `002EEED0` and this tail. No rip-relative writer exists. So it reads 0.0 unless a computed-address store sets it. With mode 0 never requested, the turntable is dead either way |
| M6 | section 4: the container pass and its gate | **survives, with an addition.** The owner record (entry `+0x40`) is dereferenced at `+0xA8` with **no null guard**. An active entry whose owner index is -1 would read address `0xA8`. So the pass assumes every active entry has an owner |
| M7 | section 4: mode 1 | **survives**: key `+4 >> 4`, draw callback `0016D6A0` |
