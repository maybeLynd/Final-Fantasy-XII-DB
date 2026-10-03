---
system: The authored presentation-command handler family — the 00520xxx band and its two-level dispatch
category: 17-Presentation-Rendering
status: "DOCUMENTED — every register row is closed (owner re-status 2026-10-01, OPUS; documented_rule READY): GI-15 answered 2026-10-01 (OPUS, static - every per-site helper read, see the GI-15 section; what remains is content, not code; review requested from SWE2-AUDIT-SEM). History: PARTIAL on GI-15 from 2026-10-01 (SWE2-FRONTIER, on SWE2-AUDIT-SEM's REJECT of c97af7156, record dd-restatus-gi-0930). GI-7 answered 2026-09-29 (FABLE), review (FABLE-REQ-AUDITSEM-REVIEW-GI7, ACCEPT, d998217e2). Was PARTIAL on: residue registered as GI-7
owner_layer: PrimaryOwner:Presentation
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: registration sites read in the shipping image 2026-09-17 (SWE2-FRONTIER) — all 25
    CharacterRenderSystem_Initialize registrations re-derived instruction-exact, the invoker idiom
    verified at two slots (0x13 and 0x34), the registrar body read end to end.
last_reviewed: 2026-09-17
audit:
  passes: 1
  last_pass: 2026-09-17
  last_pass_state: falsification-pass
  crossref_clean: false
  reopened_count: 0
---

# The authored presentation-command handlers

**Twenty-eight bodies at `00520010`–`00520E90`, 3,695 bytes, one family:** the handlers for the
authored presentation commands a scene's embedded record streams onto a character render record.
Twenty-five of them have no direct caller anywhere — each is reached only through its slot in the
`02CA4410` handler bank.

## 1. What an authored command is

A presentation command is a small authored record inside the embedded-record stream a map pack or
scene lays down. Three drains walk that stream —
`PresentationEmbeddedRecord_UpdateCurrentState` (`0041DA90`),
`PresentationEmbeddedRecord_ExecuteCommandStreamUntilThreshold` (`0041E000`), and
`PresentationEmbeddedRecord_ExecuteDeferredCommandSubset` (`0041E1D0`) — reading command records at
`[arg2+0x368] + [arg1+0x90] + 4`. The command id is `word[record] & 0x7F`, clamped to `0x4B`
(`0041DB1D`–`0041DB4B`).

## 2. The dispatch route is two tables deep

```
command record
    |  id = word[rec] & 0x7F, clamp 0x4B
    v
01EFFAF0[id]            16-byte record { invoker, flag dword } — generated 0x20-byte thunk per id
    |  invoker: rax = [02CA4410 + id*8]; test rax,rax; je ret
    |           rdx = rcx (command record); rcx = [r8 + 0x2E0] (the render record); jmp rax
    v
02CA4410[id]            75-slot handler bank, qword per id
    v
0052xxxx handler        handler(render_record, command_record)
```

Each invoker embeds **its own absolute slot address** (`00417530` loads `02CA44A8` = `02CA4410 +
0x13*8`; `004177B0` loads `02CA45B0` = `+0x34*8`). That is why a rip-relative sweep for the table
base finds "no reader": no body ever forms `02CA4410` — every reader names `02CA4410 + id*8`
directly. The unowned-code census's residual warning — "a dispatcher forming the table address some
other way is invisible to a rip-relative sweep" — is resolved by exactly this: the readers are
one generated thunk per id, and the census instrument counted them under their own addresses.

`handler(render_record, command_record)` — `rcx` is the render record (`[stream arg2 + 0x2E0]`),
`rdx` the command record. Handlers write the render record's `+0x290`/`+0x294` dirty words directly
and read the command payload from `+2` (subtype at `+2`/`+3`, parameters from `+4`).

Ids with no generated invoker point at `0016D6A0` — the shared `ret 0` — so an unregistered command
is a no-op; slots `0x49`–`0x4B` are **NULL** and a record carrying one would `call 0` (the producers
presumably never emit them). A nonzero flag byte at `01EFFAF0` record `+8` suppresses the call on
the record-flags `0x10|0x14` path (`0041DB13`–`0041DB3D`).

## 3. Who fills the bank

`0041D6C0(id, fn)` is the registrar — `movsxd rax, ecx; mov [02CA4410 + rax*8], rdx`, nine bytes.
`0041D6D0` is the same for the second bank `02CA4670`, and `0041D6E0` stores a single context
pointer at `02CA4668`. `0041CCA0` clears both `0x258`-byte banks at init.

`CharacterRenderSystem_Initialize` (`004269A0`) — after walking the `022C6F28` manager array
(`0xA0` records × `0x740`, `0041F730` per record) and storing the context pointer — registers
**24 handlers into bank A**, one `lea rdx,[handler]; lea ecx,[id]; call 0041D6C0` triple each
(`00426A2B`–`00426B84`; `rdi` is the `0xA0` loop counter that has just reached zero, so each
`[rdi+N]` is the literal id `N`). The *first* triple of the run is the exception: `00426A12`
loads `00520C50` with id `rdi+5` but calls **`0041D6D0`** — the initializer's one bank-B
registration, which is why `00417C60`'s bespoke invoker reads `02CA4698` (bank-B slot 5) for it
(§6). Corrected per AUDITSEM-CONTRA-FRONTIER-AUTHCMD-BANKB, verified against the body
2026-09-17.

| id | handler | role (read in body) |
|---:|---|---|
| 0x05 | `00520C50` | **bank B** — registered via `0041D6D0` at `00426A1C`; calls `0046CBA0` — **a character sound** *(FABLE 2026-09-20)*: word `+2` = `mode << 12 \| type`, to the record's sound emitter `+0x5F0`; [how an animation makes a sound](../../18-Audio/how-an-animation-makes-a-sound.md) |
| 0x11 | `00520160` | 23 B — **trails on / off** *(FABLE 2026-09-19)*: stores the command's byte `+2` at record `+0x3D0` and raises bit 24 of `+0x294`; the dirty pass then builds or switches off the record's [bone trails](../Character-Render-Records/the-bone-trails.md) |
| 0x12 | `005207C0` | `RelationLook_SetTrackingEnabled` — `003E6DA0`/`003E29F0` pair |
| 0x13 | `00520430` | flag work on `+0x290`, `+0x3F4`–`+0x3F6`; `00429500`,`004288B0`,`0042B580` — **store the controller switch and broadcast it across the render hierarchy** *(FABLE 2026-09-20, below)*: three arms by `byte+2 & 0xB9`, `+0x290` bit 9 held as a re-entrancy guard; 5,805 authored in the `.ca` containers *(scope named 2026-10-02, OPUS: 17,416 in all 62,208 blocks, 11,611 of them in event blocks - the census section below)*, all three arms used |
| 0x14 | `00520E70` | ~~posts deferred work via `00426870`~~ — **`00426870` is an immediate hierarchy broadcast, not a deferral** *(FABLE 2026-09-20, below)*: it applies `00521050` to the record's entity and its sub-tree, filtered on `word[entity+0x2F2]`; 7,193 authored, event blocks only, `word+4` only ever 2 or 3 |
| 0x15 | `00520740` | 58 B — touches `+0x3D1` — **draw / sheathe: re-attach the record's children** *(FABLE 2026-09-20)*: byte `+2` to bits 0-2, byte `+3` to bits 3-5, dirty bit 23; the dirty pass runs `00429760` (204 B, read whole), which re-attaches child `+0x2C8` with attachment mode 1 when the first field is non-zero and mode 0 when it is zero, and child `+0x2CA` by the second ([the FCP block](../Model-And-Motion-Formats/fcp-character-parameter-block.md), section 3). Authored only in `active` (field set, 609) and `deact` (field clear, 609) blocks; [tally](../../_experiments/evidence/reattach-and-rotator-reset-commands/census.out.txt) |
| 0x16 | `00520BD0` | `0042B550`; flag pair `+0x3D2`/`+0x3D3`, `+0x3F8` — **bind the model's sub-resource variants of slot *n*** *(FABLE 2026-09-20, below)*: word `+2` is an enable bit plus an 8-bit variant index, word `+4` the value; 329 authored in the `.ca` containers *(scope named 2026-10-02, OPUS: 373 in all blocks, 44 of them in event blocks - the census section below)*, all `enable=1` / `value=0xFFFF` |
| 0x18 | `00520C80` | `00421E20` + `003B0C50`; `+0x60`/`+0x90` fields — **the footstep effect** *(FABLE 2026-09-20; `003B0C50`, 656 B, read whole)*: refused under the record test the footstep sound uses; the movement body's ground type (0..18) picks the effect through the table at `003B0EE0` - `0x64` for types 0-3, 7, 9, 13, 14; `0x65` for 4; `0x66` for 5; `0x67` for 11, 12, 15, with a depth float when the body reports one; `0x94` for 16 and 18; none for 6, 8, 10, 17 - which is spawned on the record, tinted by the ambient colour times the record's own (`003B0D92`..`003B0E67`) and given the command's byte `+2` plus one as a sub-index. That byte is 0 on 14,299 commands and 1 on 13,923 - the shape of left and right, as a reading. [How an animation makes a sound](../../18-Audio/how-an-animation-makes-a-sound.md) §4 is its audible half |
| 0x19 | `00520CE0` | 32 B — calls `0046CC70` (interior read 2026-09-17, SWE2-FRONTIER: 1,069 B — `00237420` first at [`0046CCAE`](../../_index/ADDRESS-INDEX.md), `004FE270`/`00421E20`/`002EDBD0` ×2) |
| 0x1A | `00520C10` | `00422D50` + `003E6340`; `+0x30`/`+0x370` — **move and turn toward the target along profile *n*** *(FABLE 2026-09-20)*: word `+2` is the mode - an index into the profile table of the container's `@FRM` entry, or `0x16` for the record's own profile; 12,876 authored, in `attack`, `avoid`, `magic`, `ability`; [how an animation moves and turns a character](../../06-Movement-And-Navigation/how-an-animation-moves-and-turns-a-character-toward-its-target.md) |
| 0x1D | `00520D30` | **pose-sequencer event** *(FABLE 2026-09-19)*: byte `+2` low nibble = event, high nibble = record filter against `+0x413` + 1, byte `+3` = choice (`0xFF` random), through `003E7450`; `0xFD` sets `+0x4B7` bit 6, `0xFE` calls `00428B30`, `0xFF` stores byte `+3` in the model instance's `+0xB8` and calls the variant setter `00477610`, which cannot store - [the pose sequencer](../Model-And-Motion-Formats/the-pose-sequencer.md) §4b. (`003E55B0` resolves the instance.) |
| 0x1E | `00520DF0` | 50 B — `003E6A20`; `+0x413` |
| 0x1F | `00520140` | 23 B — tail-calls `003E6710` |
| 0x20 | `005207A0` | 23 B — touches `+0x2F4` — **alias bone `0x107` to its alternate slot** *(FABLE 2026-09-20)*: the special-bone resolver substitutes this word for bone id `0x107` (`00421E7D`..`00421E8E`), and ids `0x300`+ are FCP attachment slots; default `0x303`, restored by the record reset and by every render-event selection; this command stores `0x303 + (word != 0)`. **148 authored, every one carrying word `0x1`**, spread over **148 distinct id-named monster blocks - exactly one command each** ([tally](../../_experiments/evidence/alias-bone-slot-commands/census.out.txt)) |
| 0x21 | `00520780` | 23 B — touches `+0x2F6` — **alias bone `0x108` to its alternate slot** *(FABLE 2026-09-20)*: as `0x20`, default `0x305`, stores `0x305 + (word != 0)` (`00421E90`..`00421E9A`). **613 authored, every one carrying word `0x1`**, in exactly four block names - `item` 206, `field_item` 206, `throw` 168, `steal` 33 ([tally](../../_experiments/evidence/alias-bone-slot-commands/census.out.txt)) |
| 0x23 | `00520180` | 47 B — `004293C0`; `+0x20`/`+0x40` |
| 0x24 | `005201B0` | id→record lookups `0020E600`×3 + `002ED570`; interior loop-head `005201DD`→`005201F0` — **ramp a rotator's speed** *(FABLE 2026-09-20; read whole, with `003DFE70`, 171 B)*: word `+2` the rotator index, word `+4` the ramp in frames (0 = at once), float `+8` the target angular speed; the entry's counter `+0x10` and acceleration `+0x14` are what [the rig](../Character-Render-Records/the-rig-of-seventeen-controllers.md)'s rotator update consumes. Word `+6` with bits 7 and 6 sends the call to controller 5 instead (48 of 1,493 authored); [tally](../../_experiments/evidence/rotator-ramp-command/census.out.txt) |
| 0x25 | `00520320` | same `0020E600`/`002ED570` lookup family; loop-head `0052034D`→`00520360` — **rotator back to its default speed** *(FABLE 2026-09-20; with `003DFF20`, 178 B, read whole)*: the sibling of `0x24` - target = the entry's default `+0xC`, ramp = word `+4` frames; 740 authored, 701 over 30 frames; [tally](../../_experiments/evidence/reattach-and-rotator-reset-commands/census.out.txt) |
| 0x28 | `00520720` | 22 B — tail-calls `003E6AA0` — **post request lane `dword+4` to the bound effect instance** *(SWE2-DATA 2026-09-30, UQ-218 pass 15)*: `003E6AA0` writes `obj+0x304` bits 27–31 + dirty bit 27; dirty pass `00427DE0` → `003B3C00` range-checks `0..10` → `0024FE70` reads the effect definition `[[ctx+0x130]+0x80]`'s 11-entry map `byte[def+0xA+lane]` → `dword[def+0x2C+4·map]` → `0020E600` → `00333280` child spawn (lane at `child+0x11`). 115 authored: `{1: 112}` in 4 monster files, `{10: 3}` in `m1143_10` — per-effect lanes, not a global enum ([residue record](../../_index/candidates/uq218-cm-entry-residues/README.md)) |
| 0x29 | `00520D00` | 37 B — calls `0046CC70` — **a footstep** *(FABLE 2026-09-20)*: sound type 1 with the volume in word `+2` (128 = full); [how an animation makes a sound](../../18-Audio/how-an-animation-makes-a-sound.md) |
| 0x2A | `005206B0` | `003E7140` then CFG guard `00808C40` — **take a pooled, generation-tagged handle for a three-float request** *(FABLE 2026-09-20, below)*: a two-slot current/previous ring at `+0x44C`/`+0x448`; 7,183 authored, four distinct float triples, both words always zero |
| 0x2F | `00520E30` | `0042EF90`; `+0x20`/`+0x28`/`+0x1AF` — **send presentation event `word+2 | 0x2000` to the child sub-tree** *(FABLE 2026-09-20, below)*: 30 authored, all `npc`, all the same event `0x203D` |
| 0x34 | `00520800` | the largest (811 B): `003AFD30`/`003B6930`/`003AFC10`; ~~`+0x1C`–`+0x28` state~~ the shadow object's `+0x1C`... state *(corrected 2026-10-02, OPUS: `00520800`+0x50 loads the record's `+0x118` handle, +0x5E `call 003AFC10` resolves the shadow slot, and the stores go through its result, e.g. +0xA8 `mov byte ptr [rdx + 0x1c], al`)* — **the shadow command** *(FABLE 2026-09-20, below)*: `byte+2 = 0xFF` toggles the shadow pools globally, otherwise a **one-hot** sub-dispatch of eight arms over the record's shadow object; 9,540 authored, all eight arms used, the default arm never |
| 0x3F | `00520510` | 147 B — ~~posts deferred work via~~ **broadcasts through** `00426870` (*corrected 2026-09-20, see `0x14`*) — **a directed sway** *(FABLE 2026-09-20)*: on a root record only, posts `00520E90` across the hierarchy, which hands the rig's controller 0 ~~a preset (word `+2`; 0 = off), a direction (floats `+4`..`+0xC`), an id and a flag (word `+0x10`)~~ a bone (word `+2`), a direction (floats `+4`..`+0xC`), a preset (word `+0x10` masked `0xFFF`; 0 = off) and a flag (word `+0x10` bit 15) *(corrected 2026-10-02, OPUS: `00520510`+0x18 reads `word [r8 + 0x10]` and `00520510`+0x23 `word [rdx + 2]`; the GI-15 section)*; 3,108 authored, in the casting blocks - [the oscillators](../Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md), last section |
| 0x48 | `005205B0` | `0020E600`/`002ED570` lookups + `00372800`/`00426870` — **command `0x3F` with its target resolved by NAME** *(FABLE 2026-09-20, below)*: same precondition, same block, same broadcast, same body `00520E90`; 5,771 authored, event blocks only |

The boot-time request-ring seeder `002EA320` (and its sibling `002EA5F0`, which re-registers the
same five) puts **five more handlers into bank A** in the same id space — id 4 → `002E70C0`,
id 5 → `0016D6A0` (the shared bare `ret`: an explicit empty handler), id 6 → `002E7090`,
id 0x0C → `002E70A0`, id 0x26 → `002E7080` — and two into the separate `022D7FD0` record array via
`0036C5A0(id≤0xE, fn)` (writes `fn` at `record + id*0xA8 + 0xA0`): id 6 and id 0x0A, both
`002E6D60`. The `002E70xx`/`002E6D60` family opens with the same `test …/jz` state-flag gate.

## 4. The three band members the table does not dispatch

| body | reach | role |
|---|---|---|
| `00520100` | called by `PresentationEmbeddedRecord_ActivatePendingState` (`0041DD40`) | submit wrapper: if `word[rcx+6] == -1` it ~~posts `00520E90` through the deferred-work poster `00426870`~~ applies `00520E90` at once through `00426870` *(corrected 2026-10-02, OPUS: `00426870`+0x33 `call rsi` applies the callback to the record at once and +0x4A `call 0042EF90` walks its children - this page's own 2026-09-20 correction, `00426870` defers nothing)*, record packed on the stack |
| `00520E90` | the ~~posted~~ callback `00426870` applies | ~~deferred worker~~ per-record callback *(corrected 2026-10-02, OPUS: `00426870` calls it at once, `00426870`+0x33)*: resolves `0020E600` (runtime pointer) + `002ED570` (resource-table entry by index) against `dword[rcx+0x18]`/`dword[rcx+0x10]`, security-cookie frame, 361 B |
| `00520010` | called by `0046E3E0`, `0046E6F0`, `RenderModelInstanceContainer_ProcessActiveEntries` (`00477F20`) | shared helper, not a command handler: iterates on `dword[rcx+0x40]` as an index (−1 = done), resolving `0020E600` + `003AB7F0` per step |

`00426870` — ~~the deferred-work poster~~ the apply-and-recurse helper *(corrected 2026-10-02, OPUS: `00426870`+0x33 `call rsi` applies the callback to the record at once and +0x4A `call 0042EF90` walks its children - this page's own 2026-09-20 correction, `00426870` defers nothing)* — is called by `00520100`, by `003E6A60`, and by three of the
handlers themselves (`00520E70`, `00520510`, `005205B0`): the family both consumes deferred work and
produces it.

## 5. What the commands do to the record

The handler family is the write side of *authored presentation state*: flag words `+0x290`/`+0x294`
(the render record's dirty channels), state bytes `+0x3D0`–`+0x3F8` and `+0x413`/`+0x4B7`, the
`+0x30`/`+0x370`/`+0x60`/`+0x90` fields several handlers touch, and — through `00520800` — the
~~`+0x1C`–`+0x28` block~~ shadow object's `+0x1C`... block, not the record's *(corrected 2026-10-02, OPUS: `00520800`+0x5E `call 003AFC10`, then stores through its result)*. Four of the classes (`0x0D`–`0x10`, registered elsewhere) drive the five
per-slot ramp channels covered by
[the authored-command ramp contract](../CONTRACT-authored-command-ramp-channels.md); the 25 ids here
(24 bank-A + 1 bank-B) are the rest of the authored vocabulary — visibility/tracking flags,
lookup-and-bind commands, and the ~~deferred~~ resource-bind pair (applied at once through `00426870` *(corrected 2026-10-02, OPUS: `00426870`+0x33 `call rsi`)*).

## 6. Residuals

- **Per-command semantics.** The table above is reach + touched fields, not named operations;
  naming each id's presentation meaning is semantic work (queued for independent review where a
  body's role is ambiguous).
- ~~**Bank B** (`02CA4670`, via `0041D6D0`) is registered by the same mechanism but its consumer side
  is not yet traced to a drain.~~ **Traced 2026-09-29 (FABLE, GI-7) - bank B is a one-slot bank for
  command 5.** `0041D6D0` has one caller, `CharacterRenderSystem_Initialize` at `00426A1C`, which
  registers slot 5 only (`00520C50`, the character sound - the id-5 row of the table above). Nothing
  else touches the bank: the only other references are the boot clear in `0041CCA0` and one read, the
  id-5 invoker `00417C60` loading `02CA4698` (rip-relative census of `02CA4668`..`02CA48C8`; no
  image-base-relative access - [`bank_b_check.py`](../../_index/candidates/gi7-bank-b-0929/bank_b_check.py) B1-B5; bank A is never read by index - every bank-A read is a fixed slot in a
  generated invoker, so no bank-A id can run into bank B). So the drain is the ordinary one: the three
  stream drains reach pair-table slot 5 (`01EFFAF0` + 5 x 16 = `{00417C60, flag 1}`), and `00417C60`
  calls bank-A slot 5 with the entry's owner `+0x2C0`, then bank-B slot 5 with the render record
  `+0x2E0`, then raises bit 5 of the stream's `+0x2C8`. Bank-A slot 5 is the empty stub `0016D6A0` in
  both actor-side registrars (`002EA320` at `002EA492`, `002EA5F0` at `002EA5FB`), so on PC **command 5
  is the character sound and nothing else**; the second bank exists to give id 5 a render-side handler
  beside the actor-side one, and the actor side is empty.
- ~~**The bespoke invokers** — `00417AD0` (id 4, switches on `byte[record+2]` over 12 cases),
  `00417C60` (id 5, reads bank B slot `02CA4698`), `00417DE0` (id `0x2C`, interprets the record
  itself, writes `+0x358`/`+0x35A`/`+0xC`) — mean ids 4, 5 and `0x2C` carry per-id semantics in the
  dispatch layer itself.~~ **Named (GI-7, 2026-09-29, pointing to sections already on this page):**
  id 4 is the action-timeline event routed to the battle unit's handler, subtypes 0-9 reaching it
  ("Where the commands are authored"); id 5 is the character sound (bank B, above); id `0x2C` is the
  blend-in rule keyed on the motion being left ("The commands that run the motion itself").
- The `00520xxx` bodies at ~~`00521000`+~~ `005210F0`+ *(corrected 2026-10-02, OPUS: `00521000` and `00521050` are the per-node bodies the `0x2F` and `0x14` handlers post, `00520E30`+0x1A and `00520E70`+0xA `lea`)* (handle-table allocate/resolve/release, `005210F0`/
  `005212E0`/`00521250`) are a *different* family — the 256-entry × 48-byte handle table at
  `02CA8450` — recorded here only to bound the band.

*Cross-reference: the dispatch route's table record and the NOCALLER-INSTALLERS census this resolves
live in
[render-event-selection-evidence](../Character-Render-Records/render-event-selection-evidence.md)
§"The `02CA4410`/`02CA4670` handler arrays", whose per-id table this page re-verified.*

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (2026-09-17, SWE2-FRONTIER)

Six labels, all through shared helpers or the seeders this page names — no handler here owns work in
another layer:

- **ActorEntity — CLIENT.** `002368D0`, owned by that layer, calls `002EA5F0` — the sibling
  re-registrar this page names beside the `002EA320` boot seeder. The crossing is an actor-layer
  body re-arming the registration pair, not shared ownership.
- **Audio — SHARED HELPER + DESCENT.** `00332C40` and `003B99D0`, owned by that layer, call
  `00421E20` — the presentation helper handler `0x18` (`00520C80`) also invokes; the helper is
  shared, not audio-owned. In the other direction `0046CC70` (the common callee of handlers `0x19`
  and `0x29`) itself calls `002DEE80`, `00361BF0` and `003590D0` — the handlers' work descends into
  the audio layer's function; the command triggers an audio action, which is the crossing's purpose.
- **CoreRuntimeScheduling — DESCENT.** `00477F20`
  (`RenderModelInstanceContainer_ProcessActiveEntries`, the helper's third caller) calls `00229EA0`
  — the render-list walk reaches into the scheduler layer beneath it.
- **Movement — CLIENT.** `002E3110`, owned by that layer, calls `004288B0` — the helper handler
  `0x13` (`00520430`) invokes for its flag work; a movement-layer body shares it.
- **Party — DESCENT.** covered by the Audio bullet above — `0046CC70` → `003590D0` is the same
  callee descending to a second layer (party-side state read inside the triggered action).
- **World — CLIENT.** `00266D10`, owned by that layer, calls `002EA320` — the boot-time request-ring
  seeder this page names; the world layer re-seeds through it.
- **CombatAction - CLIENT and SERVICE (8 edges).** PartyFocus_GetCurrentPackedActorHandle (`003590D0`) is called by bodies filed to CombatAction: `00317E60`, `00319090`; BattleStorage_InitializeWorkArrays (`002368D0`), BattleUnit_HandleReactionAnimationEvent (`003250F0`), BattleUnit_HandleActionTimelineEvent (`00325260`) reach bodies filed to CombatAction: `00306BA0`, `003082F0`, `0030CA50`, BattleAction_ResetPresentationSlotPool (`0030CF40`) (+2 more) - shared machinery across the layer boundary, no shared ownership.
- **Gameplay - CLIENT and SERVICE (2 edges).** PartyFocus_GetCurrentPackedActorHandle (`003590D0`) is called by bodies filed to Gameplay: `0031ADB0`; BattleUnit_HandleActionTimelineEvent (`00325260`) reaches bodies filed to Gameplay: `003257D0` - shared machinery across the layer boundary, no shared ownership.
- **Resource - CLIENT and SERVICE (65 edges).** ResourceTable_ResolveEntryByIndex (`002ED570`), `003AB7F0`, `004090D0` are called by bodies filed to Resource: ResourceTable_ResolveEntryByIndex (`002ED570`), `00408F80`, ResourceEntry_GetResolvedBasePointer (`00409600`), ResourceEntry_FindSectionIndexAndOffset (`00409780`) (+12 more); BattleStorage_InitializeWorkArrays (`002368D0`), CharacterRenderRecord_RefreshFCPPayloadByRecordId (`002EDBD0`), `00373060`, CharacterRenderRecord_ResolveModelInstance (`003E55B0`) (+23 more) reach bodies filed to Resource: ResourceTable_ResolveEntryByIndex (`002ED570`), `003843F0`, `00408F80`, `004090D0` (+11 more) - shared machinery across the layer boundary, no shared ownership.
- **Spawn_Encounter_Lifecycle - SERVICE (1 edge).** BattleUnit_HandleReactionAnimationEvent (`003250F0`) reaches bodies filed to Spawn_Encounter_Lifecycle: SpawnGroup_MarkCompletionPendingAfterReaction (`00307110`) - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (5 edges).** Bodies filed to Script_VM_Native_Bridge call two shared helpers on this page's edges: `00340700` and `0034D120` call `0026A430` (the ActorEntity-filed helper the command-2/6 effect-handle row names), and `003476B0`, `0034E0E0` call `002E9830` (the object-type query the footstep reader `003B0C50` runs) - client calls on shared helpers across the layer boundary, no shared ownership.

## Where the commands are authored, and which are never authored (FABLE, 2026-09-19)

*Static plus one data census. Read whole: the child selector `004090D0`, the stream-pointer rebuild `0041CA70`
(`0041CA88`..`0041CAD2`), the drain's command loop `0041DAF1`..`0041DB81` and its two end-of-track sites
`0041DC34`..`0041DCA0` and `0041DCBC`..`0041DD1F`, the class `0x04` invoker `00417AD0` with its twelve-entry jump table
at `00417C2C`. Answers ASTRA's `ASTRA-REQ-FABLE-EE12-POST-READER-RESIDUAL`.*

**The stream is a named block of the character's animation container.** A presentation entry keeps a resource handle
(`+0x310`), a section index (`+0x318`), a group and a child number (`+0x31A`, `+0x31C & 0xFFF`) and a section offset
(`+0x320`); `0041CA70` resolves the section and asks the `@FRP` child selector for that child, and the pointer it gets
back is the entry's `+0x368`. On disk that child is an **`@FMC` block** inside a **`.ca` file**: name at `+0x10`
(`ready`, `attack`, `magic`, `knockback_l`, `dead` ...), track count at `+0x0C`, first track header at `+0x30` - the
layout [the track page](../Character-Render-Records/how-a-presentation-entry-picks-its-track.md) reads from the other
side. A track's groups are `u16 time key, u16 (length << 6 | count)`; a command is `u16 (length << 7 | id)` followed
by its payload, which is what the drain's `shr eax, 7` at `0041DB6F` and `and eax, 0x3F` at `0041DB7C` walk. Event
scenes carry the same blocks inside their `.mot` files (`mc_0`, `mc_1` ...), and 209 sit in model files.

**Parsed out of every block in the game the format holds exactly**
([`census.py`](../../_experiments/evidence/authored-command-census/census.py),
[output](../../_experiments/evidence/authored-command-census/census.out.txt)): 3,164 containers, **62,208 blocks,
172,552 tracks, 640,217 groups, 2,348,027 commands**, every track ending where its header says and every group ending
where its length says, no command id above `0x48`. The output lists, per id, how many commands, in how many blocks, in
which folders and under which block names - the quickest way to see what an id is *for*.

| id | commands | where | consistent with |
|---|---:|---|---|
| `0x04` | 27,631 | `attack`, `magic`, `item`, `ev_door`, `ability` | the battle unit's action-timeline event (below) |
| `0x06` | 7,008 | `magic`, `item`, `ev_treasure`, `throw`, `ability` - exactly one per block | the second battle guard (below) |
| `0x11` | 10,617 | `attack`, `field_attack`; byte `+2` = 1 on 4,254 and 0 on 6,363 | [bone trails](../Character-Render-Records/the-bone-trails.md) on and off |
| `0x1D` | 11,245 | `ready`, `knockback_l`, `dead`, the event blocks | [the pose sequencer](../Model-And-Motion-Formats/the-pose-sequencer.md)'s events 0, 1, 2 |
| `0x0D`, `0x0E`, `0x0F`, `0x2C` | 417,549 / 325,965 / 445,335 / 387,789 | every kind of block | the bulk of all authored commands |
| `0x14`, `0x48` | 7,193 / 5,771 | **event blocks only** | cutscene-only commands |
| `0x23` | 261 | **model files only** - `weapon_active`, `weapon_deact`, `weapon_shot` | weapon-model commands |

**41 of the 76 ids `0x00`..`0x4B` are never authored anywhere**, among them **`0x0C`** and **`0x1F`** (the census
output lists them all). **The code and the data agree on which.** The invoker table `01EFFAF0`, read out of the
image, holds the shared bare `ret` for 33 ids and a null for `0x49`..`0x4B`; **all 36 are among the 41**, and no id
with an empty invoker is authored even once in 2.3 million commands - a prediction the data could have refuted. The
other five - `0x08`, `0x19`, `0x1E`, `0x1F`, `0x26` - have working invokers and handlers that no shipped block ever
calls: `0x1E` is the pose sequencer's reset and `0x1F` the switch for the FCP section 8 objects.

**The three battle handlers, settled.** [EE-12](../../_index/OPEN-QUESTIONS.md) asked whether `00325260`, `00325090`
and `003250F0` ever execute, found their guards registered in this bank at ids `4`, `6` and `0x0C`, and asked for a
runtime watch. The data and the dispatch code answer it:

- **Id `4` - `002E70C0` -> `00325260`, the action-timeline event.** The class `0x04` invoker `00417AD0` calls the
  registered handler, with the entry's owner `+0x2C0` and the command record, for subtype byte `+2` = **0, 3 and
  5..9** as authored; for **1** four times, with the subtype replaced by `0x80`, `0x81`, `0x82`, `0x83`
  (`00417B27`..`00417B80`); for **2** and **4** after raising entry flag `0x200000` or `0x8000`. Subtypes **10, 11**
  only set bits 1 and 0 of record byte `+0x419`, and **12** runs a record query; none of the three reaches the
  handler. Authored counts by subtype: 7,656 / 2,559 / 2,283 / 2,559 / 3,169 / 220 / 622 / 622 / 622 / 80 / 1,256 /
  1,050 / 4,933. **So 20,392 authored commands (subtypes 0 to 9), in the attack, magic, item and ability animations of
  2,613 containers, are routed to the battle unit's timeline handler.** This is how an attack animation's timing reaches the battle
  system; ~~what each subtype means to the handler is the battle side's and was not read here (GI-15).~~ Each subtype's arm in `00325260` is now read (the GI-15 section, OPUS 2026-10-01).
- **Id `6` - `002E7090` -> `00325090`.** 7,008 authored commands, one per block, in the same animation families.
- **Id `0x0C` - `002E70A0` -> `003250F0` - is not a command class at all.** No block authors it, and no generated
  invoker reads its slot. Slot `02CA4470` is read by the **engine**, at three places: the two end-of-track sites of
  the drain and the track-switch helper `0041CEC0`. When the playhead passes the end of the current track the drain
  marks the state finished, runs the remaining commands, and - if entry flag bit 20 is set, bits 9 and 29 are clear,
  and not (bit 4 set while the id's flag byte `01EFFBB8` is 1, which it is) - calls the slot with
  `(entry +0x2C0, &entry +0x31C)` and sets bit 9 so that it happens once. **`003250F0` is the battle unit being told
  "your animation finished" or "your track was switched".**

None of the three needs a breakpoint to show it can run. What a live session could still add is ordinary
confirmation, not discovery; `FABLE-REQ-ASTRA-HANDLERS` is withdrawn as answered.

**Resource - SERVICE (crossing).** The section resolve and the child selector belong to the resource layer
([resource section addressing](../../02-Resource-And-Asset-Pipeline/resource-section-addressing.md)); used by result.
**Combat action - CLIENT (crossing).** The three guards and the handlers behind them are the battle unit's; this page
only shows how they are reached. The two handlers named have callees of their own in the **Gameplay** and
**Spawn / encounter** layers; citing the handlers imports those edges, and nothing here depends on them.
## The commands that run the motion itself: `0x00`, `0x03`, `0x08`, `0x2C` (FABLE, 2026-09-20)

*Four invokers that never reach a handler bank - they act on the presentation entry and the playing state directly.
All four read whole; one census. This narrows §6's "per-command semantics" residual; the sound commands are on
[their own page](../../18-Audio/how-an-animation-makes-a-sound.md).*

| id | invoker | what it does |
|---|---|---|
| `0x00` | `00417810` (258 B) | **Begin.** Exactly one per block. Moves the entry's current motion number `+0x324` to *previous* `+0x326` and stores the new one (kept only when its class nibble is 1 or 2, else `0xFFFF`; with no previous, previous becomes current); zeroes the state's frame; the signed word `+2` is an **explicit end frame** - negative means none (`+0x16` / `+0x18` = `0x7FFF`), otherwise `+0x16` = `+0x18` = `n - 1`, state flag bit 2 and a normalised step at `+0x1C`; sets the state playing (`+4` = 1), copies the entry's speed `+0x340`, clears the entry's finished mark (flag bit 9 - the bit the end-of-track callback sets, above) and tail-calls the play method of the selector table |
| `0x03` | `00417A80` (72 B) | **Hold here.** If the command's state is the entry's current one it only raises entry flag bit 3. Otherwise the state's end frame becomes its current frame, state flag `0x40` goes up, and a hold counter `+0x5E` is loaded - once - with word `+2` times the frame-rate word ~~(or 1 when the word is -1)~~ (times 1 instead when the word is -1, so -1 stays -1) *(corrected 2026-10-02, OPUS: `00417A80`+0x38 `cmove cx, r8w` replaces the multiplier, not the value, before `00417A80`+0x40 `imul ecx, eax`)* |
| `0x2C` | `00417DE0` (345 B) | **Blend-in rule, by where you came from.** Ignored under entry flags `0x24000`. Word `+2` is the motion being *left*: it must equal the entry's previous motion number (12 bits) or be `0xFFFF` for *any*; then a list of byte pairs from `+8` (count at `+7`) is matched against entry byte `+0x329`. A match has a rank - 1 *any*, 2 wildcard pair, 3 exact pair - and is applied only if it is at least the rank already held (`+0x32A`), so **the most specific rule authored for a transition wins, whatever the order**. Applying it: blend rate `+0x354` = `1 / byte +4` (0 = cut; `0xFF` = raise the no-blend flag, bit 1 of `+0x2E8`), `+0x358` = the low seven bits of byte `+5`, sign-extended, `+0x35A` = byte `+6`, bit 0 of `+0x2E8` = bit 7 of byte `+5`; entry flag bit 11 up (and bit 14 when bit 13 is) |
| `0x08` | `00417D00` (219 B) | **Default blend.** The same fields with no *from* test - rate `1 / (byte +2 + 1)`, `+0x358` = `0x10` - skipped under entry flag bits 17 or 14. **Never authored** |

**What the files hold** ([`census.py`](../../_experiments/evidence/motion-control-commands/census.py),
[output](../../_experiments/evidence/motion-control-commands/census.out.txt), the 31,942 blocks of the animation
containers): exactly one `0x00` in every block - it is the block's first command in 30,003 of them (what precedes it in the rest was
not tallied); its end-frame word is negative in 31,320 blocks and 1-30 in the other 622, so
an explicit end is the exception and the motion data normally sets the length. All 6,432 `0x03` carry -1. Of 387,757
`0x2C`: every *from* word is `0xFFFF` (25,163) or fits in twelve bits - a wider word would have contradicted the reading and
there is none; every one carries exactly one pair and is long enough for it; blend lengths of 15, 10 and 20 frames lead,
and 32,426 ask for no blend at all. **The *from* word is a slot number of the character's own motion library**: all 362,594 of them name an occupied slot of
the same version-1 container ([the container page](../Model-And-Motion-Formats/frp-object-container.md) §9). **235,944 of them are in the monsters' containers** - a monster's `ready` block is largely a table of
"coming from motion *x*, blend over *n* frames".

*(Superseded 2026-09-20 by the section below, which reads the invoker whole.)* *Read but not written up here: `0x09` (invoker 00417F40, 1,717 B - only its first 0x140 bytes read, so written without code marks) looks its payload up as
the **name of an `@FMN` section** of the entry's resource, the bone-motion child that sits beside each `@FMC` block in
the container - 108,511 authored, one or two per block. ~~What it does with the section was not read (GI-15).~~ The `0x09` section below reads it (GI-15, OPUS 2026-10-01).*
## Command `0x34` is the shadow command (FABLE, Claude Opus 5, 2026-09-20)

**`byte[cmd + 2] == 0xFF` is a global toggle, and it is a pair this database already knows.**

```asm
0052080F  cmp byte ptr [rdx + 3], 0
00520815  mov ecx, 1    ; call 003AFD30 ; mov ecx, 4 ; call 003B6930      <- byte+3 != 0
00520834  xor ecx, ecx  ; call 003AFD30 ; mov ecx, 6 ; call 003B6930      <- byte+3 == 0
```

Both take a **constant, not the record**. `003AFD30(1)` together with `003B6930(4)` is exactly the pair
[the world tick and the field frame](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md)
records in the field-frame reset sequence, and
[the ownerless-functions page](../../00-Engine-Core-Runtime/Ownership-Boundary/intentionally-ownerless-functions-and-shared-scratch.md)
names the two as **the shadow pools of `BT-1`**. So the `0xFF` arm turns shadows on and off for everything, from an
authored animation command.

**Otherwise it is a one-hot sub-dispatch over the record's shadow object.** The object comes from
`003AFC10(dword[rec + 0x118])` — absent, and the command does nothing — and the selector is `byte[cmd + 2] - 1`
against a **128-wide byte table at `00520B50`**. Decoded, that table has **nine** slots, and the eight that are not
the default sit at exactly the **one-hot** values:

| `byte + 2` | arm | what it writes on the shadow object |
|---:|---|---|
| `0x01` | `005208A4` | `byte[+0x1C]` = `byte+3`; ~~when that is 0 or 1, also a float from `dword[cmd + 4]`~~ a ramp - the float `dword[cmd + 4]` is used in every case: set at once when `byte+3` is 0 or 1, else approached over `byte+3` steps *(corrected 2026-10-01, OPUS: the GI-15 section)* |
| `0x02` | `005208F2` | `byte[+0x1D]`, same shape |
| `0x04` | `00520940` | `byte[+0x1E]`, same shape |
| `0x08` | `0052098E` | `byte[+0x1F]` low bits — `and 0xF2` then `or 2` |
| `0x10` | `005209BA` | `byte[+0x1F]` high nibble — `and 0x0F` then `or 0x20` |
| `0x20` | `005209E6` | `byte[+0x54]`, the mode-plus-float shape |
| `0x40` | `00520A34` | `byte[+0x55]`, the same |
| `0x80` | `00520A82` | a switch of its own on `byte+3` |
| everything else | `00520B20` | the default — **never reached, see below** |

*Five arms share one shape* — a mode byte with an optional float — *two pack bitfields into the single byte `+0x1F`,
and one is a nested switch.*

### What is authored (FABLE)

| | |
|---|---|
| `0x34` commands | **9,540** — 9,512 in event blocks, 28 in containers |
| distinct `(byte+2, byte+3)` | **31** |
| the eight one-hot arms | **all authored**, and evenly: 844 to 1,018 commands each |
| the `0xFF` global arm | **28** commands — 19 with `byte+3 = 1`, 9 with `0` |
| any other `byte+2` | **none** |

So **the 120-wide default arm is dead in shipped data**, every real arm is live, and the global shadow toggle is
authored 28 times across the game.

~~**Not read here (GI-15):** the seven arms past their first store; the `0x80` arm's nested switch; what `003AFC10` builds;
which of `+0x1C`–`+0x55` mean what to the shadow pools.~~ *(read 2026-10-01, OPUS: the GI-15 section at the end of this page)*

## Command `0x48` is command `0x3F` with its target named (FABLE, Claude Opus 5, 2026-09-20)

*The last bank-A handler read here, and it is a command already on this page seen from the other side. The draft of
this section claimed `0x3F` acts on one record while `0x48` broadcasts; reading `00520510` through refuted that —
**both broadcast, identically** — and the real difference is narrower and more interesting.*

**Everything is shared.** Both handlers require `word[rec + 6] == 0xFFFF` (`00520514`, `005205F9`); both build the
same `0x20`-byte block — the record at `+0`, the command's three dwords from `+4`/`+8`/`+0xC` at `+8`/`+0xC`/`+0x10`,
~~an index at `+0x14`, `word+2 & 0xFFF` at `+0x16`, `word+2 >> 15` at `+0x18`~~ a bone at `+0x14`, a preset at `+0x16` and a flag at `+0x18`, filled from different words by the two commands *(corrected 2026-10-01, OPUS: the GI-15 section)*; and both call
**`00426870(word[rec + 0], 00520E90, block)`** — the entity and its whole sub-tree, through the helper corrected in
`0x14`'s section — with `00520E90`, the sway-oscillator configurator of the `0x3F` row above.

**One field is filled two ways.**

| | `0x3F` (`00520510`) | `0x48` (`005205B0`) |
|---|---|---|
| the block's `+0x14` index | ~~`word[cmd + 0x10] & 0xFFF`, **used directly**, zeroed when it equals the masked `word+2`~~ `word[cmd + 2]`, **used directly**; `word[cmd + 0x10]` fills the preset `+0x16`, zeroed when `word[cmd + 2]` is `0xFFFF` (`00520560`–`00520567`) *(corrected 2026-10-01, OPUS: the GI-15 section)* | the low word of `dword[cmd + 0x10]` passed to **`00372800(resource, key)`** as a **name key**, `0xFFFF` back zeroing ~~the field~~ the preset `+0x16`, which comes from `word[cmd + 2]` *(corrected 2026-10-01, OPUS: the GI-15 section)* (`00520630`, `0052065E`–`00520663`) |
| the resource | not needed | resolved first (`dword[+0x18]` through the `+0xD98` table), and the command aborts without it |

~~That is the whole difference: **one addresses the oscillator by index, the other by name.**~~ The difference: `0x3F` gives the bone by index and the preset from `word+0x10`; `0x48` finds the bone by name key and takes the preset from `word+2`, which is 0 (sway off) in 5,167 of 5,771 *(corrected 2026-10-01, OPUS: the GI-15 section)*.

### What is authored (FABLE)

Both passes, with **both** published totals as controls — `0x3F` 3,108 and `0x48` 5,771, both reproducing:

| | `0x3F` | `0x48` |
|---|---|---|
| commands | 3,108 | 5,771 |
| corpus | **containers only** | **event blocks only** |
| distinct `(word+2 & 0xFFF, word+2 >> 15, word+0x10)` | **3** | **30** |
| the target field | `4`, `5` or `6` | **`29` in every one** — one name key |
| `word+2 & 0xFFF` | `0` always | `0` on 5,167 of 5,771; else `4`, `5`, `6` … |

**Neither command appears in the other's corpus.** So this is one mechanism with two front doors, split cleanly by
authoring context: inside an animation container the oscillator is addressed by index, inside an event block by name
— which is what an event needs, since it is authored against models it does not own.

~~**Not read here (GI-15):** `00372800`'s lookup beyond its `0xFFFF` contract; what name key `29` is; why `0x3F` zeroes its
index when it matches the masked `word+2`.~~ *(read 2026-10-01, OPUS: the GI-15 section at the end of this page)*

## Command `0x2F`: one presentation event, pushed down the child sub-tree (FABLE, Claude Opus 5, 2026-09-20)

**The handler forces bit 13, which is the event base.**

```asm
00520E34  movsx eax, word ptr [rdx + 2]      ; the authored word, sign-extended
00520E3D  bts   eax, 0xD                     ; | 0x2000
00520E41  mov   qword ptr [rsp + 0x28], rcx  ; block +8 = the record
00520E46  movzx ecx, word ptr [rcx + 8]      ; the record's CHILD index
00520E51  mov   dword ptr [rsp + 0x20], eax  ; block +0 = the value
00520E55  call  CharacterRenderHierarchy_TraverseIndexDepthFirst
```

Two things follow. The traversal starts at **`word[rec + 8]`**, the child — the record's own entity is not visited.
And the block is the same two-field shape command `0x13` passes, which **settles what `0x13`'s section left open**:
**`+0` is the parameter and `+8` the record**.

**Per node, `00521000` (75 B) does three things.** It skips a node whose `word[+0x2F8]` is `0xFFFF`; it **copies bits
0-1 of `byte[+0x40B]` from the owning record onto the node** (`r8 = (owner ^ node) & 3` then `node ^= r8`, the
copy-these-bits idiom) — the bits
[the fade channels page](../Character-Render-Records/how-a-character-fades-the-ten-channels.md) ties to channel 1's
ramp; and it sends the event with `00427320(node, value)` before tail-jumping `004272E0(node)`.

**Both callees are already named elsewhere.** `00427320` is **the render record's event receiver** —
[the battle-unit field map](../../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md) reads it calling
`00420890(record, event)` to pull a presentation view from the unit — which is what makes the forced bit 13 an
**event id in the `0x2000` range** rather than a flag. `004272E0` (21 B) clears a mask of `+0x294` and leaves bit 5,
one of the `+0x294` setters
[the render-record array page](../Character-Render-Records/the-character-render-record-array.md) lists.

### What is authored (FABLE)

| | |
|---|---|
| `0x2F` commands | **30** — the rarest command read here |
| where | **`npc` blocks only** (`n1009_60_0600`, `n1018_60_0600`, `n1018_60_0703` …) |
| `word + 2` | **`0x3D` in every one** — so the event is always **`0x203D`** |

Cross-checked against the published census's own row for `0x2F`: 30 commands, in 30 blocks, in 30 files, all `npc`.
*So this is a single-purpose command: one event, one authoring context, thirty uses.*

**What event `0x203D` does, read 2026-09-20.** It reaches the table. `00427320` filters a few events by name
(`0x2007`, `0x2008`, `0x200C`, `0x200E` via the `0xA3` bit mask, and `0x4035`/`0x4036`) and handles `0x2005` and
`0x2006` in arms of its own; everything else — `0x203D` among them — falls through to a **common join** at
`004274B6`, which calls `00420890(record, event)` unless `+0x284` bit 27 is up with `word[+6] != 0xFFFF`, and then
`00423790(record, event, word[+0x3B4])`.

Inside `00420890` the index is `event − 0x2005` bounded at `0x37`, so the table covers **`0x2005`–`0x203C`** and
**`0x203D` is one past it**. That is not a no-op: the out-of-range path *is* the selector-`0x100` path —
`002ED500(unit, 0x100, out)` then `record[+0x110] = out[+0x30]` (`00420928`–`00420942`), the presentation event
parameter [the battle-unit field map](../../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md) documents. So
this command's one authored event asks the unit for a presentation view and stores its `+0x30`.

**And `word[+0x2F8]`, the field this command's per-node body skips on, read the same day.** It is half of a pair with
`word[+0x2FA]`, and both writers agree: `0041FCF0` and `00420480` each set `word[+0x2F8] = word[+0x408]` — the
record's requested id — and `0041FCF0` then looks up the **`@FMC`** section by tag and name
(`0x434D4640`, `ResourceEntry_FindSectionIndexByTagAndName`) into `word[+0x2FA]`, **invalidating both back to `-1`
when that lookup fails** (`0041FE57`–`0041FE97`). `CharacterRenderRecord_ResetDefaults` clears it.

`@FMC` is the **authored command block itself** — the stream every command on this page comes from. So
`word[+0x2F8] == 0xFFFF` means *this record has no command block*, and that is exactly why `0x2F` skips such a node:
there is no command stream there to affect.

~~**Not read here (GI-15):** `00423790`.~~ *(read 2026-10-01, OPUS: the GI-15 section at the end of this page)*

## `word[record + 0x2F2]`: the field two commands key on marks a **substitute** record (FABLE, Claude Opus 5, 2026-09-20)

*Command `0x13` refuses outright while it is non-zero; command `0x14` runs a node only when it equals bit 0 of the
command's `word + 4`. Both were read above without knowing what it is. A complete displacement census — **35 accesses
image-wide** — settles it.*

**It is two-valued, and it has exactly two writers.** Every one of the 33 reading sites is a `cmp` against **0 or 1**.
The writers are `004218A0` and `004219C0`, a pair with the same shape — in `004218A0`:

```asm
00421942  mov word ptr [rbx + 0x2F2], di      ; di = 0 (xor edi, edi at 004218E7 / 00421901)
00421949  test r12, r12                       ; r12 = the lookup KEY argument
0042194C  jne  00421966
0042194E  or   dword ptr [rbx + 0x284], 0x4000000
00421958  mov  eax, 1
0042195D  mov  word ptr [rbx + 0x2F2], ax     ; = 1
```

So the field is **0 by default**, and it is set to **1 — together with `+0x284` bit 26 — exactly when the record is
built with no key**. ~~That is a placeholder: the record exists, but nothing was resolved for it.~~ That is attach code `0x7FFF`, the whole-skeleton bind; the bind still runs, with bone -1 *(corrected 2026-10-01, OPUS: the GI-15 section)*.

~~**Leaving that state restores three fades.**~~ *(Corrected 2026-10-01, OPUS: both paths reach the bit-26 test, and the no-key path has just set bit 26, so `003E5D30` runs on that path itself; nothing read clears bit 26 - the GI-15 section.)* On the other branch the key is resolved
(`00372760(resource, key)` → a `u16` index, `-1` aborting), and then:

```asm
0042198E  test dword ptr [rbx + 0x284], 0x4000000
00421998  je   ...
0042199A  mov  rcx, rbx
0042199D  call 003E5D30
```

`003E5D30` (34 B) is three stores: `qword[+0x4C0] = qword[+0x4C8] = qword[+0x4E0] = 0x1000`. In the fade channels'
4.12 fixed point that is **1.0 with the step and remaining words zeroed** — the setter's own shape — so **channels 0,
1 and 4** (distance fade, attached-piece visibility, viewer-inside fade, per
[how a character fades the ten channels](../Character-Render-Records/how-a-character-fades-the-ten-channels.md)) snap
to fully opaque when a record stops being a substitute.

**What that makes of the two commands.** `0x13` declines to touch a substitute at all. `0x14`'s filter is a
**substitute-versus-real selector**, and the census shows the event blocks address **both** sides deliberately: bit 0
set on 6,164 commands and clear on 1,029.

~~**Not read here (GI-15):** `004219C0`, the sibling writer, beyond confirming its two stores match; what the key argument
*names*; `00372760` and `0046E590` beyond their return contracts.~~ *(read 2026-10-01, OPUS: the GI-15 section at the end of this page)*

## Command `0x14`: a filtered hierarchy broadcast - and `00426870` is not a deferral (FABLE, Claude Opus 5, 2026-09-20)

**First, a correction to this page's own row.** It read *"posts deferred work via `00426870`"*. `00426870` (90 B)
defers nothing:

```asm
00426870  cmp  cx, -1              ; the entity index; 0xFFFF -> return
0042688F  imul rbx, rax, 0x740     ; R = [022C6F28] + idx * 0x740
004268A3  call rsi                 ; fn(R, arg)            <- immediate
004268A5  movzx ecx, word [rbx+8]  ; the child index
004268BA  call CharacterRenderHierarchy_TraverseIndexDepthFirst(R, fn, arg)
```

It is the **one-node-plus-sub-tree broadcast helper** — the simpler sibling of `00429500`, which command `0x13` uses
and which additionally follows `word[+0xA]` and double-calls. Command `0x48` uses this same helper, so that row
inherits the correction.

**The handler is one call.** `00520E70` (32 B) passes `word[rec + 0]`, the body `00521050`, and the command pointer.

**The per-node body `00521050` (154 B) is a filter and a dispatch.**

1. Resolve the entity's resource: `dword[+0x18]` is an index into the table at
   `ImageAddress_ResolveRuntimePointer(dword[+0x10]) + 0xD98`, through `ResourceTable_ResolveEntryByIndex`. Absent →
   this node is skipped.
2. **The entity filter:** `(word[cmd + 4] & 1)` must equal `word[entity + 0x2F2]`, or the node is skipped
   (`00521090`–`005210A0`). *That is the same field command `0x13` refuses on while it is non-zero* — so `+0x2F2`
   is a per-entity side or slot number that both commands key on, one as a gate and one as a selector.
3. **The index:** with `word[cmd + 4] & 2` set, `005048A0(entity, ((word[cmd+4] & 0xFFFC) << 14) | word[cmd+2])`
   resolves it and a return of `-1` skips the node; otherwise the index is `(i16)word[cmd + 2]` directly.
4. `00373060(resource, index, word[cmd + 6])`.

### What is authored (FABLE)

Both corpus passes, with the published per-id totals as controls (see the correction under `0x13`):

| | |
|---|---|
| `0x14` commands | **7,193** — **event blocks only**, none in a container or a model file |
| `word + 4` | exactly **two values**: **3** on 6,164 and **2** on 1,029 |
| so bit 1 (the lookup path) | **set in all 7,193** — the direct `(i16)word+2` path is **never authored** |
| bit 0 (the entity filter) | 1 on 6,164, 0 on 1,029 — both sides of `+0x2F2` are addressed |
| distinct `(word+2, word+4, word+6)` tuples | **3,269** — the widest spread of any command read here, consistent with a per-scene id |

**And the packing is inert in the shipped data.** `word+4 & 0xFFFC` is `0` for both authored values, so the "packed
id" reduces to plain `word[cmd + 2]` every time. The lookup `005048A0` is nevertheless always used, and it can return
`-1`, which drops that node silently — so the one failure this command can have in practice is a resource id that the
entity's own table does not carry.

~~**Not read here (GI-15):** `00373060` (read only for its shape — it resolves two image pointers and indexes a `0x292`-stride
table) and `005048A0` beyond its `-1` contract; what `word[+0x2F2]` *is*, beyond being the field `0x13` gates on and
`0x14` filters by.~~ *(read 2026-10-01, OPUS: the GI-15 section at the end of this page)*

## Command `0x13`: store the switch, then broadcast it across the hierarchy (FABLE, Claude Opus 5, 2026-09-20)

**It refuses outright while `word[rec + 0x2F2]` is non-zero** (`00520436`) — the first thing the handler does, before
looking at the command at all.

**Then it splits three ways on `byte[cmd + 2] & 0xB9`.** *(`0xB9` is ~~`1000 1001 1`~~ `1011 1001` *(corrected 2026-10-02, OPUS: `0xB9` = 128 + 32 + 16 + 8 + 1)* — bits 0, 3, 4, 5 and 7; the mask
is what classifies, and the unmasked byte is what is stored.)*

| arm | taken when | what it does |
|---|---|---|
| **store and broadcast** | the class is anything but `0x80` | `+0x290` **bit 9 set**, `byte+2` → `+0x3F4`, `byte+3` → `+0x3F5`, `word+4` → `+0x3F6`, `00429500(rec, 1)`, then **bit 9 cleared** (`005204A3`–`005204D6`) |
| **class `0x80`** | `byte+2 & 0xB9 == 0x80` | `004288B0(rec, (i8)byte+3)` then `0042B580(rec)`, and `+0x290` **bit 10** cleared (`005204E8`–`005204F9`) |
| **no command at all** | the handler is entered with a null command pointer | bails when `+0x290` bit 9 is already up *and* the stored `byte[+0x3F4] & 0xB9 == 0x10`; otherwise sets bit 9, stores the default `0x11` into `+0x3F4`, `00429500(rec, 1)`, clears bit 9 (`0052044C`–`00520487`) |

**`+0x290` bit 9 is a re-entrancy guard, not a dirty bit.** It is set immediately before `00429500` and cleared
immediately after, on both storing arms — and the command-less arm *tests* it on entry. That is the shape of a
"broadcast in progress" latch, and it explains the `or ..., 0x200` sites elsewhere in the record band.

**`00429500` is the broadcast.** It resolves `word[rec + 0]` into the `0x740`-stride entity array at `[022C6F28]`
and calls `0042BED0` on that entity; then follows the entity's `word[+8]` to a second one and calls `0042BED0` again;
then, for each of `word[+8]` and `word[+0xA]` that is not `0xFFFF`, walks the sub-tree with
`CharacterRenderHierarchy_TraverseIndexDepthFirst(node, 0042BED0, block)`. So one authored command reaches **the
record's entity, its child, and both sub-trees depth-first**. The block it passes carries the render record at its
`+8` (`0042951F`, read back at `0042BF0F`); ~~*its `+0` was not traced*~~ — the two dwords written near the prologue
land in a different local, which is worth saying because the obvious reading is that they are the block.
**`+0` is settled by command `0x2F` below: it is the parameter**, and the block is a `{value, record}` pair shared by
both broadcasts.

**`0042BED0` is not re-derived here.** It is the controller-11 flag dispatcher already read on
[the rig of seventeen controllers](../Character-Render-Records/the-rig-of-seventeen-controllers.md) (1,163 B, first
third read; SWE2-EC7-52). This section adds only how a command reaches it and how widely.

### What is authored (FABLE)

Census of every `.ca` container, `@FMC` walk, control reproducing the published **12,876** `0x1A` commands exactly:

| classifier `byte+2 & 0xB9` | commands |
|---:|---:|
| `0x08` | **6,300** — the largest |
| `0x00` | 4,838 |
| `0x20` | 4,263 |
| `0x10` | 939 |
| `0x80` | **921** — the second arm |
| `0x01` | 147 |
| `0x09`, `0x11` | 4 each |
| **total** | **17,416** — 5,805 in containers and **11,611 in event blocks** — in **164** distinct `(byte+2, byte+3, word+4)` tuples |

**All three arms are authored** — unlike `0x16`, whose census leaves two arms unreached. And the class the
command-less arm checks for, `0x10`, is a real authored class with 939 uses, so that bail-out is reachable rather
than defensive.

> ### Corrected within the day, and why the control did not catch it (FABLE)
>
> *This table first read **5,805** commands in **46** tuples, with classes `0x00` 4,657, `0x10` 687, `0x20` 253,
> `0x01` 146 and `0x80` 62.* The script walked only `ps2data/obj_finish/*.ca`. The authored-command census this page
> already cites makes **two** passes — the `.ca` containers, then the event `.mot` and model `.cm` blocks — and
> `0x13` is authored **11,611 times in event blocks**, two thirds of its population. **The missing class is the
> point**: `0x08`, with 6,300 uses, is the command's *largest* class and did not appear in the container-only list at
> all, so the first table was not merely short, it was qualitatively incomplete.
>
> **The control passed anyway, and could not have failed.** It was "reproduce the published 12,876 commands of
> `0x1A`" — and `0x1A` happens to be authored **only** in containers, so a container-only walk reproduces it exactly.
> *A control has to be sensitive to the defect it is there to catch.* The re-run uses the published **per-id totals**
> instead — `0x13` 17,416, `0x14` 7,193, `0x16` 373, `0x1A` 12,876, `0x2A` 7,183 — and reproduces the census's own
> **2,348,027 commands in 62,208 blocks**, which no container-only walk can.
>
> **What the correction leaves standing:** every qualitative claim in this section and in `0x16`'s, and **`0x2A`'s
> numbers unchanged** — 7,183 in four float triples, because that command *is* container-only. The counts that moved
> are `0x16` (329 → 373) and `0x13` (5,805 → 17,416).

**The class-`0x80` arm's pair, read 2026-09-20.** `004288B0(record, delta)` is 40 bytes whole: it raises
`+0x290` **bit 10** — the very bit this arm clears afterwards, so the arm applies its change and then marks it
handled — and then either, for `delta == -1`, raises `+0x284` bit 17 and sets `byte[+0x40A] = 0`, or otherwise
**adds `delta` to `byte[+0x40A]`**. `0042B580(record)` forces `byte[+0x3F4] = 0x80` — the class — and then broadcasts
`0042BED0` over the entity and its children exactly as `00429500` does. *So the arm adjusts a counter at `+0x40A` and
re-applies the record with its class pinned to `0x80`.*

**And the census says only one of the two paths is used from here:** all **921** class-`0x80` commands carry
`byte+3 = 0xFF`, so from this command `004288B0` always takes the **reset** branch — `byte[+0x40A] = 0` plus
`+0x284` bit 17 — and never the add. The add path has eight other callers outside this page's subject.

~~**Not read here (GI-15):** what `word[+0x2F2]` counts~~ *(read 2026-10-01, OPUS: a 0/1 flag, not a count - the GI-15 section)* ~~; the block's `+0`~~ (settled under `0x2F`).

## Command `0x2A`: a pooled, generation-tagged handle, two at a time (FABLE, Claude Opus 5, 2026-09-20)

**The handler is a marshaller.** `005206B0` (102 B) passes the command's three floats at `+8`, `+0xC`, `+0x10` in
`xmm1`–`xmm3` and its two words at `+2` and `+4` as the fifth and sixth arguments of `003E7140`.

**`003E7140` (198 B) was unread. It is a two-slot ring.**

```asm
003E716F  mov  ecx, dword ptr [rcx + 0x448]   ; the PREVIOUS handle
003E717D  je   ...                            ; if non-zero:
003E717F  call 003D8300                       ;   release it
003E7184  mov  eax, dword ptr [rbx + 0x44C]   ; the CURRENT handle
003E7191  mov  dword ptr [rbx + 0x448], eax   ;   becomes the previous
   ... builds a 32-byte request: the three floats at +0, +4, +8; a flag byte
       (old bits 6-7 kept, bit 6 forced); byte +0xE = 2; a word at +0x10 that
       is the sixth argument when it is below 4 and 0 otherwise ...
003E71D5  call 003D7FF0
003E71DA  mov  dword ptr [rbx + 0x44C], eax   ; the new handle
```

So the record holds **two** of these at once, and **every third start releases the oldest**. Nothing else in the
record is touched.

**The allocator is generation-tagged.** `003D7FF0` walks a **32-entry pool of `0x60`-byte slots at `02B4D7D0`** for
the first with `dword[+4] == 0`, bumps the live count at `02B4D7A0` and a monotone counter at `02B4D7A4` that wraps
to `1` at `0xFFFFFF`, and writes the slot's key as

```
dword[slot + 4] = (generation << 8) | slotIndex
```

— **which is the value it returns**, and therefore what `+0x44C` holds: a handle that stops matching its slot once
the slot is reused, which is what makes the two-slot release safe. The request's 32 bytes are copied into
`slot + 0x30` and `slot + 0x40`.

**Both failure paths return 0, and the record stores that as if it were a handle.** `003D7FF0` refuses when the
request's `byte +0xE` is 2 *and* the gate at `02B4D7A2` is non-zero — and the caller sets `byte +0xE = 2`
unconditionally, so that gate alone can suppress every one of these — and it refuses again when all 32 slots are
busy. In both cases `+0x44C` receives `0`; the next start then finds a zero in `+0x448` and skips the release, so a
refusal costs the effect, not the ring's consistency.

### What is authored (FABLE)

Census of every `.ca` container, `@FMC` walk, control reproducing the published **12,876** `0x1A` commands exactly:

| | |
|---|---|
| `0x2A` commands | **7,183** |
| command size | **20 bytes in all of them** |
| word `+2` and word `+4` | **0 in all of them** — so the sixth argument is always 0 and the request's word `+0x10` always 0 |
| distinct float triples | **four**: `(0.7, 0.7, 1.3)` ×3,264, `(0.4, 0.4, 1.1)` ×2,735, `(0.2, 0.2, 0.8)` ×1,026, `(5.0, 5.0, 5.0)` ×158 |
| corpus | **containers only** — no event block authors this command |

*Re-run over both passes and unchanged* (see the correction under `0x13`): this command is authored only in `.ca`
containers, so the container-only figure was already the whole population.

Three of the four have **x equal to y** with a different z, and the fourth is uniform. *That is the shape of a
scale, not of a position offset* — ~~but nothing read here consumes the floats, so they are recorded as three floats~~ *(2026-10-01, OPUS: they are the camera-shake source's intensity, time rate and radius scale - the GI-15 section)* and earlier they were recorded as three floats
with four authored values and no name.

~~**Not read here (GI-15):** what the pool's slots are for (`003D8300`, the release, and the slot's own `+0x30`/`+0x40` were
read only for their shape); the `02B4D7A2` gate; the table at `02B4E3D0` the kind-2 path indexes with the request's
clamped word.~~ *(read 2026-10-01, OPUS: the GI-15 section at the end of this page)*

## Command `0x16`: bind the model's sub-resource variants - and the two arms nothing authors (FABLE, Claude Opus 5, 2026-09-20)

**The handler is a field split.** `00520BD0` (52 B) takes the authored word at `+2` apart and keeps the result on the
record:

```asm
00520BD4  movzx eax, byte ptr [rdx + 2] ; and al, 1
00520BDA  mov   byte ptr [rcx + 0x3D2], al      ; the ENABLE bit  = word+2 bit 0
00520BE0  movzx eax, word ptr [rdx + 2] ; shr ax, 1
00520BE7  mov   byte ptr [rcx + 0x3D3], al      ; the VARIANT index = word+2 bits 1..8
00520BED  movzx eax, word ptr [rdx + 4]
00520BF1  mov   word  ptr [rcx + 0x3F8], ax     ; the VALUE
00520BF8  call  0042B550
```

**`0042B550` (33 B) is the applier, and it was unread.** It reads the three fields straight back and tail-jumps on
the enable bit: set → `CharacterRenderRecord_EnsureModelSubresourceVariantBindings` (`003E7210`), clear →
`CharacterRenderRecord_RemoveModelSubresourceVariantBindings` (`003E69E0`), both with
`(record, byte[+0x3D3], word[+0x3F8])`. Both resolve the model through
`CharacterRenderRecord_ResolveModelInstance` first, and a **value of `0xFFFF`** sends `003E7210` down a different
path that walks the table at `qword[record + 0x400]` (`word[+0xA]` entries) instead of binding one variant.

**The three fields are remembered, not scratch.** `0042B550` has exactly one caller — this handler — but the fields
have a second *reader*: `RenderRecords_ProcessDirtyState` at `00427FDC`–`00427FFE` tests **bit 24 (`0x1000000`) of
`+0x290`**, and when it is up re-applies the identical three fields through the identical two callees, then clears
the bit. *A caller census would have called this a one-shot; a reader census does not.*

### What is authored, and what is not (FABLE)

Census of every `.ca` container under `ps2data/obj_finish`, walking the `@FMC` stream, with the published **12,876**
`0x1A` commands as its control (reproduced exactly):

| | |
|---|---|
| `0x16` commands | **373** — 329 in containers, **44 in event blocks** |
| enable bit | **1 in all 373** — never 0 |
| value word | **`0xFFFF` in all 373** — never a single variant |
| variant index | only **0** (127), **3** (69), **4** (69), **5** (69), **1** (39) |
| distinct (enable, variant, value) triples | **5** |

> *Corrected within the day (FABLE): this table first read 329, 121/34/58/58/58. The first run of the script walked
> only `ps2data/obj_finish/*.ca` and never made the second pass over event `.mot` and model `.cm` blocks. **Every
> qualitative statement below survives the correction** — all 373 are `enable=1` with `value=0xFFFF`, in the same five
> triples — but the counts were container-only. See the note under `0x13`.*

So the command is authored in exactly one shape — *"bind all variants of slot n"* — and **two of the handler's three
interesting branches are never reached from shipped data**: the unbind arm `003E69E0`, and the single-variant path
inside `003E7210`. The equal counts on 3, 4 and 5 — 69 each over the full corpus, as they were 58 each over the
containers alone — suggest a fixed trio authored together; that was not checked container by container.

**And the re-apply arm may be dead too.** Bit 24 of `+0x290` is **tested** by the dirty pass and has **no `or`
setter anywhere**: of the 111 writes to that word, none carries the immediate `0x1000000`, and there are **zero**
register-sourced `or`s into it. Only a wholesale `mov dword` could raise it — there are 34, three of them in the
render-record band (`00426E20`, `0042F250`, `0042F310`) — and those were **not traced**. Until one is, the honest
statement is that the bit has no additive setter, not that nothing sets it.

~~**Not read here (GI-15):** what a "sub-resource variant" is on the model side (`RenderModelInstance_RemoveSubresourceVariantBinding`
`00504610` and the `003E7210` table walk were read only for their shape); which slot each of the five indices is.~~ *(read 2026-10-01, OPUS: the GI-15 section at the end of this page)*

## Command `0x09`: play this bone motion - and where the blend rule is spent (FABLE, 2026-09-20)

*The invoker `00417F40` (1,717 B) read whole; one census. Completes the motion-control set above - this is the command
that consumes what `0x2C` prepared.*

**1. Find the motion.** The payload from `+2` is a **name**. It is looked up as an `@FMN` section of the entry's
resource (`00417FF3`..`00418006`); if this section does not hold it the whole resource is searched for it
(`0041800C`..`00418057`), and the section pointer falls back to the `@FRP` tag (`004180A7`..`004180D2`). When the
stream header's byte `+4` has bit 0 or 1 the payload is instead a word - half of it, plus the entry's `+0x2A`, is a
child index (`0041805C`..`00418087`). No motion, no effect.

**2. Reset the playing state** (`004180DA`..`00418114`): frame and ids to -1 or 0, `+0x18` = `0x1E0000`, `+0x20` = 30.0.

**3. Decide the blend** - one of five, in this order:

| when | blend |
|---|---|
| entry flag bit 12 | none; the state's flag `0x10` and entry bits 11 and 24 are cleared |
| record `+0x4B7` bit 6 - the bit command `0x1D`'s arm `0xFD` sets ([the pose sequencer](../Model-And-Motion-Formats/the-pose-sequencer.md) §4b) | **cut**: the bit is consumed and the rate is 0. So `0x1D 0xFD` means *"the next motion starts without a blend"* |
| entry flag bit 11 - a `0x2C` rule matched | the rule's rate stands; if the entry's `+0x2E8` has bits 1 and 2 both up the rate is recomputed from `+0x380` / `+0x384` (a remaining-time blend, capped at 50 frames) |
| no rule, and flags `0x5004000` clear, and this is not the same motion on the same track as before | **the default: six frames** (`+0x354` = 1/6, `+0x358` = 1) - except that leaving library slot `0x3D` under entry flag bit 25 cuts |
| otherwise | cut |

It then starts the blend (`00418167`) and **clears entry flags 11, 13, 14 and 24-26** (`0041816C`): a blend rule is
spent by the first motion that starts after it.

**4. Configure what rides on the motion.** For a header whose bits 24-25 are 2 the entry's attached object record gets
bit 1 of its `+0xA6` from header byte `+0x5C` bit 0, and its controller object (`+0x94`) is configured from the
header - a mode (low three bits of byte `+0xBE`, or `+0xEE` for type 1, whose bit 7 also goes to record `+0x66D`
bit 0), a vector pair and two float pairs (`0041830E`..`004183B2`, `004183EE`..`00418493`). Type 1 also hands six
floats and a count to the ramp-channel object `+0x35C`
([the ramp channels](../CONTRACT-authored-command-ramp-channels.md)). ~~*The four controller calls were read by argument only; what the controller is was not established here.*~~
***Corrected 2026-09-20 (FABLE): it was established, on another page, and I did not look.** The object at `+0x94` is
[the rig of seventeen controllers](../Character-Render-Records/the-rig-of-seventeen-controllers.md), and the routines
called here resolve `[rig + 8]` - **controller 2, the look controller** (two of the four, 003E2D20 and 003E2EA0,
read at their heads for this and so written without code marks: the first stores the mode at the controller's byte `+6`, the second copies one dword per element at
a `0x60` stride). So every bone motion's header re-tunes the look controller when the motion starts.*

**5. Bind the weights.** For a type-1 motion the invoker finds the `@FMW` section **with the motion's own name**
(`004184AB`..`004184FB`) and, when header bits 4-5 are 1, binds motion, weights and the entry's tables in one
ten-argument call (`0041850F`..`00418561`).

> **What that ten-argument call is — `0041BEE0`, read 2026-09-20 (FABLE, Claude Opus 5).** It does three things.
>
> **It fills a binding record** (the third argument): `-1` into `dword[+0]`, `word[+0x50]`, `word[+0x52]` and
> `dword[+0x68]` and zeroes into `+4`, `+8`, `+0x10`, `+0x48`, `+0x60`, `+0x70`, `+0x78` first; then the kind
> `0x10006` at `+8`, the defaults `0x1E0000` at `+0x18` and `30.0f` at `+0x20`, **32 bytes of name** at `+0x24` from
> its seventh argument, and the rest of its arguments at `+0x48`, `+0x50`, `+0x52`, `+0x5C`, `+0x60` and `+0x68` —
> the last a resource index that `ResourceTable_ResolveEntryByIndex` turns into the entry it then works on.
>
> **It finds the sections by tag and name**, three calls to `ResourceEntry_FindSectionOffsetByTagAndName` with the
> name at `+0x24`:
>
> | tag | constant | into |
> |---|---|---|
> | `@FMN` | `0x4E4D4640` | `dword[+0x54]` |
> | `@FRP` | `0x50524640` | **the same field**, only when `@FMN` came back `-1` |
> | `@FMW` | `0x574D4640` | `dword[+0x58]` |
>
> *The `@FRP` fallback is new here* — step 5 above describes the `@FMW` lookup only, and the census that backs it
> counts `@FMW`s. **What falls back is the `@FMN` side**, so a motion whose container has no `@FMN` binds against the
> `@FRP` root instead.
>
> **It walks the bone list and marks the bones.** Over `dword[arg4 + 0xC]` entries of a **variable-stride** list —
> each entry's next is `+ ((word[entry + 2] >> 9) & 0x3F)` — it resolves the entry's `word[+0]` to a bone index
> through `00370E00`, skips `-1`, optionally requires `byte[bone × 0x290 + 0x283]` to equal an **eleventh** argument,
> then toggles bit 1 of `byte[bone × 0x290 + 0x28B]` against a parity with `+0x28A` and copies `+0x28A` bit 1 into
> its bit 0. For each bone it emits a **`0x108`-byte per-bone binding** through `0041B550`, at
> `base + word[record + 0x2BC] × 0x108`, and **increments `word[record + 0x2BC]`** — which is therefore the count of
> bound bones.
>
> **The per-bone binding it emits, read 2026-09-20.** `0041B550` (247 B) writes `word[+0x100]` from its `r9`
> argument and `dword[+0xFC]` as a delta, then loops **nine times at stride `0x1C` from `+8`** with a mask register
> that **doubles each iteration** — `1, 2, 4 … 0x100`. That bit is tested against `word[entry + 2]` and against the
> binding header's `@FMN` offset at `+0x54` to decide the slot: either **empty** (`word` `-1`, null `qword`) or
> built by `0041B650(slot, …, word[list], …)`. When that returns 1 the mask bit is **shifted left 7 and ORed into
> `word[+0x102]`**, so `+0x102` is a **per-slot success mask** in bits 7 and up.
>
> ~~*Not resolved:* the exact boundary between the nine `0x1C` slots and the header words.~~ **Resolved the same
> day by reading `0041B650`.** It writes `word[slot+0]`, `word[slot+0x10]`, `dword[slot+0x12]`, `word[slot+0x16]`
> and `dword[slot+0x18]`, so the slot runs to `+0x1C` and **the stride is the slot size**. The apparent overlap was
> mine: the caller's `rbx` points at **`slot + 8`**, not at the slot, so its empty-slot writes at `rbx-4` and `rbx`
> are `slot+4` and `slot+8`, and **the nine slots start at record `+0`, not `+8`**. The record therefore **tiles
> exactly**:
>
> | | |
> |---|---|
> | `+0x00`–`+0xFB` | nine slots of `0x1C` |
> | `+0xFC` | `dword`, the delta |
> | `+0x100` | `word`, the `r9` id |
> | `+0x102` | `word`, the per-slot success mask (bits 7+) |
>
> — `0x104` used inside the `0x108` stride, with no overlap at all.
>
> ~~*Not read (GI-15):* `0041B650`, `00409190` and `003AB7F0`, and the tail past the loop.~~ *(read 2026-10-01, OPUS: the GI-15 section at the end of this page)*

**6. Finish:** previous motion := current, entry `+0x328` := the state's track byte, state flag bit 2 := header byte
`+0x24` bit 0 (or the index payload's bit 0), `+0x2E8` bits 1-2 cleared, state playing at the entry's speed.

**What the files hold** ([`census.py`](../../_experiments/evidence/fmn-header-and-weights/census.py),
[output](../../_experiments/evidence/fmn-header-and-weights/census.out.txt)): all 18,303 bone motions are type 1 with
bits 4-5 = 1 and bits 24-25 = 2 - two values of the header dword, `0x02001111` (13,966) and `0x02001011` (4,337) - so
every branch the invoker has for other types is unused by shipped data; **every one of the 18,303 has an `@FMW` of the
same name in its own container**, which is the lookup step 5 makes; header byte `+0x24` bit 0 is set on 713.

`003E3460` (258 B) is the `+0x28`/`+0x2C` pair arm `00417F40` runs on the command record: each target float is compared against the `0020E600`-resolved record's current `+0x28`/`+0x2C`, and on difference `+0x48`/`+0x4C` receive `(target - current) * 0.125` (`01DFE0BC`'s 1.0f x `00915508`'s 0x3E000000) while `byte[+0x3A]`/`+0x3B` get `01DFE0B4 << 3` - the per-channel rate-and-flag commit the pair write performs.

Interior anchor `003E347E` (function `003E3460`).

`003E3590` (258 B) is the sibling arm on `+0x20`/`+0x24`: identical structure - compare against the resolved record, write `(target - current) * 0.125` into `+0x40`/`+0x44`, stamp `byte[+0x38]`/`+0x39` with `01DFE0B4 << 3` - the second float pair of the same commit.

Interior anchor `003E35AE` (function `003E3590`).

## Commands `0x01`, `0x0A`/`0x0B` and `0x28`: play a track, choose a track, set a 5-bit request (FABLE, Claude Opus 5.5, 2026-09-28)

*Static from the certified image, plus one census of the animation and model containers' `@FMC` blocks (32,151
blocks, 0 grammar violations, 33 ids used).
[`fmc_opcodes.py`](../../_index/candidates/uq218-fmc-opcode-crosswalk/fmc_opcodes.py) T, A, P1–P3, C, FAILS 0. These
were the used ids whose meaning no section had read; the crosswalk in the same record lists where each of the other 29 is
read.*

**`0x01` - play track *n* of this block** (`00417920`, 349 B). Word `+2` is `{mode:4, n:12}`.
- If the current state already plays *n* (`+0x80 == n`), nothing happens.
- **Mode 0** starts *n* in a parallel state slot. `0041C9A0` finds the slot: the one already playing *n*, else the first
  free one (`+0x95 == 0`), searching slots 1 to count − 1 at stride `0xA0`.
- **Mode 1** does the same, but only once the current state's `+4` is 2.
- **Mode 2** replaces the current state in place when entry flag `0x40` (`+0xC`) is up; otherwise it raises entry flag
  `0x80` as a pending request.
- Any other mode does nothing.

Authored modes: 0 (26,026), 1 (36,362), 2 (2,492), and no other. Many sit in the `0xFFFF`-keyed group that runs at the end
of a track, so "at the end, go on to track *n*" is the common use.

**`0x0A` then `0x0B` - choose the next track** (`00418600`, `00417110`).
- `0x0A` stores its four operand bytes at entry `+0x2DC`–`+0x2DF` and marks the current state: `+4 = 1`, `+8 |= 2`,
  `+0x20 =` entry `+0x340`.
- `0x0B` reads `+0x2DC` as a **selector kind** (`0xFF` = none, and nothing happens under entry flag `0x40000`). It calls the
  selector reached through the context pointer at `02CA4668` (`[ctx + kind·16 + 8]`), which returns an index *i* in its low
  half and an offset in its high half.
- For kinds 0, 2, `0xA` and `0x10`, when the render record has flag `0x8000000`, the result is also kept in record bytes
  `+0x4B8`–`+0x4BB`, one per kind.
- If *i* is below byte `+4` (the list length) and differs from the state's last choice (`+0x94`), `0x0B` resets the idle
  state slots. It then plays track `word[+6 + 2i]` + offset through `0x01`'s own handler (called at `00417390`) and
  records *i* in `+0x94` and the track in entry `+0x26`.

The files hold the pair exactly as the code expects. Every one of the 6,726 `0x0B` commands comes right after a `0x0A` in
the same group, and each is `6 + 2 · count` bytes long: its track list. A `4 + 2 · count` layout fits none of them. ~~**What
each selector kind chooses by** is the selector's own business and was not read.~~

**The selectors** *(added 2026-09-28, FABLE, Claude Opus 5.5;
[`selector_kinds.py`](../../_index/candidates/uq218-fmc-selector-kinds/selector_kinds.py) S1–S4, C, FAILS 0).*
`CharacterRenderSystem_Initialize` passes the `.data` table `01F000A0` to the context registrar, so the pointer at
`02CA4668` is that table: `0x30` entries of `{1, cell}`, kind *k*'s selector being the function in the cell.
- Kinds `0`, `1`, `2`, `4`, `0xA`, `0xB`, `0x10`, `0x20`–`0x25` and `0x2F` have their own selector. Every other kind
  returns 0.
- The archive authors ten kinds: `0` (782), `1` (450), `2` (643), `0xA` (700), `0xB` (7), `0x10` (1,831), `0x20` (1,746),
  `0x21` (56), `0x24` (507) and `0x25` (4).
- **Kind `0x10` is a random countdown**, read whole (`004225A0`):
  - It draws `n = (lo − 1 + rand() mod (hi − lo + 1)) × frameLimit`, where `lo` and `hi` are `0x0A`'s operand bytes
    `+3`/`+4` and `frameLimit` is `01DFE0B4` (1 at 30 fps, 2 at 60 fps), so the wait is the same in real time.
  - It then returns 0 and counts down, and returns 1 when the count is spent, then draws again.
  - Authored ranges are (2, 4), (4, 6), (1, 2) and (6, 12), all with `lo ≤ hi`.

  With (2, 4), for example, the choice stays on list entry 0 for 1 to 3 passes (times `frameLimit`), then takes entry 1.
- Kinds `0`, `0xA` and `0xB` share one classifier, called with argument 0, 1 or 2 (the record names it). Kinds `0x20`, `0x21`, `0x24` and `0x25`
  are the angle-window family: each computes the heading to a queried point with the steering contract's yaw-to-point.
  Kinds `1` and `2` keep a counter at record `+0x40E`.

~~**What those other kinds decide by is not read**: the classifier only in part, and the points and flags kinds `2` and
`0x20` query come back from the battle unit's view request, not read here.~~ *Read 2026-09-29 (FABLE, Claude Opus 5.5;
[`criteria.md`](../../_index/candidates/uq218-fmc-selector-kinds/criteria.md), `selector_criteria.py` N, Q, K1, K2, Y, FAILS
0), except the classifier:*
- **`-1` means "no change".** `0x0B` skips when a selector returns −1 (`00417262`).
- **Two flags from the battle unit's view request** drive kinds 1 and 2:
  - *the combo may continue* (the combo predicate the force-fight page reads);
  - *the primary target evaded or absorbed the unit's last action with no knockback*: result kinds 1–4 (band A or B evade,
    plain or with parry) or 7 (absorbed by a defensive layer).
- **Kind `1`, a random variant with an "evaded" twin.**
  - The first call draws *r* in 0..4 from the shared bounded draw and plays list entry *r*.
  - About ten passes later (the counter is tested at 11 × `frameLimit`, having started at `frameLimit`), if the target evaded
    or absorbed, it plays entry *r* + 5.
  - Otherwise it returns −1.
- **Kind `2`, a sticky follow-up.** It decides once:
  - entry 0 if the combo may continue;
  - otherwise entry 1 if the target evaded or absorbed;
  - otherwise entry 2.
- **The yaw family** measures the yaw to the queried target in degrees:
  - `0x20`: entry 0 within ±90° (the target is in front), else entry 1.
  - `0x21`: entry 0 within ±60°, else 1 or 2 by the yaw's sign. A coin adds 3, so each band has two variants.
  - `0x24`: four quadrants at ±45° and ±135° (0 front, 1 and 2 the sides, 3 behind), kept in record `+0x2AF`. A coin adds 4.
    Quadrant 3 is what makes a later command `0x1A` in mode `0x0A` turn the long way round
    ([how an animation moves and turns a character](../../06-Movement-And-Navigation/how-an-animation-moves-and-turns-a-character-toward-its-target.md)).
  - `0x25`: four quadrants at 0° and ±90°, measured toward the actor named by record `+0x18`; entry 0 if that actor does not
    resolve.

~~**Still open:** kinds `0`, `0xA` and `0xB`, the locomotion classifier. In outline, it compares the facing with a target
heading and the speed with the record's thresholds, returns bands 0–`0xE`, and checks each band against the model's
available motions, falling back when one is missing. Each band's meaning is not read.~~ **Kinds `0`, `0xA` and `0xB`, the
locomotion classifier** *(read 2026-09-29, FABLE, Claude Opus 5.5;
[`classifier.md`](../../_index/candidates/uq218-fmc-selector-kinds/classifier.md), `classifier.py` B, F, R, FAILS 0).* It
always chooses; it never returns −1.
- **Override:** band `0xE` when the render-pool slot's field says so.
- **Below the model's speed threshold:** band 0 when the last turn (facing minus the previous facing) is within ±1.0° at
  30 fps (±0.5° at 60). Otherwise band 6, or 7 when the turn reaches the model's turn angle; the track offset is the turn's
  sign.
- **Middle speed:** the movement heading against the facing. Within ±45° gives 1, 45°–135° gives 3, −135°–−45° gives 4,
  and anything beyond gives 5.
- **At or above the record's run threshold:** band 2. With a focused target, the target's bearing gives 2, `0xA`, 9 or
  `0xB` by the same windows.
- **The model check:** before a band is used, a model (FCP) property says whether the model has that motion. If it does
  not, a simpler band stands in.
- **Renumbering:** the command's argument (0, 1, 2 for kinds 0, `0xA`, `0xB`) renumbers the fast bands and `0xE` into its
  own list.

Idle, turn, walk-direction, run and face-target is how the geometry reads; ~~the band names themselves are inference —
though the `.ca` `@FMN` name bands are authored as the locomotion set (`idle`, `walk_f`, `run`, `walk_l`, `walk_r`,
`walk_b`, `stp`, `run_l`, `run_r` in `_l`/`_r` pairs, e.g. `c1004_23.ca` slots 80–96), a positional match for the band
families and the hi16 track offset (folded into
[fef-and-motion-entries.md](../Model-And-Motion-Formats/fef-and-motion-entries.md) 2026-09-29, still not a code-proven
band→name binding).~~ **The binding is a code path** *(2026-09-30, SWE2-DATA pass 18,
`_index/candidates/uq218-pass18-0930/`; applied by FABLE, who re-ran `band_names.py`, FAILS 0)*:
- op `0x0B` (`00417110`) plays `@FMC` record `list[result & 0xFFFF] + (result >> 16)` (`00417367`); the record index is
  stamped by `0041CD30`;
- that record's op `0x09` names the `@FMN`.

Over 1,489 authored selectors:
- band 1 = `walk_f`, 2 = `run`, 3 = `walk_l`, 4 = `walk_r`, 5 = `walk_b`;
- 6 = `trn`, 7 = `hi_trn`, 8 = `stp`;
- 9 / 10 = `run_l` / `run_r` (kind `0xA`);
- the last band = `sleep`.

The hi16 offset picks the start foot.

~~**Still open:** which yaw sign is the character's left.~~ **A positive yaw delta is the character's left** *(same
record)*:
- heading − facing in (45, 135] (band 3) binds `walk_l` in both selector sets (287 and 281 records) and `walk_r` never;
- a non-negative turn binds `trn_l` (226; `trn_r` 0).

`band_names.py` checks both: S0/S1/T, FAILS 0. ~~Where the kind-1 and kind-2 state bytes are reset~~ — resolved
2026-09-29 (SWE2-DATA): the bytes live in the `0x740`-record at `qword[ctx+0x2E0]` (pool `0xA0 × 0x740` at
~~`[02B3EF28]`~~ `[022C6F28]` *(corrected 2026-10-02, OPUS: `02B3EF28` has no reference in the image; the pool pointer is `022C6F28`, read by the pool init at `004269A0`+0xF)*); record init `0041F730` zeroes `+0x40E`/`+0x411` and sets `+0x410`/`+0x412`/`+0x2AF` = `0xFF`, and the
`@FMC`-bind site `004252A7` re-arms `+0x40E` = 0 / `+0x412` = `0xFF` on every new motion block. `+0x410`/`+0x411` have
no external writer, so a decided kind-2 stick survives a rebind until the record is re-initialised (full bodies and
the writer sweep in
[`criteria.md`](../../_index/candidates/uq218-fmc-selector-kinds/criteria.md)). No rip-relative store writes the
dispatch table; that sweep does find the frame-limit writer, but it cannot see image-base-relative stores.

**`0x28` - a 5-bit request to the effect side** (`00520720`, bank A). The handler passes the dword at `+4` to the
render-record setter `003E6AA0`. That setter writes the value into bits 27–31 of the record's `+0x304` and raises dirty
bit 27 of `+0x294`. The dirty pass then hands the value, together with the record's `+0x288` handle, to the effect-side
processor ([dirty-bits.tsv](../Character-Render-Records/members/dirty-bits.tsv), row `+0x294` bit 27). Authored values
are 1 (112) and 10 (3). ~~What those two values select was not read~~ — resolved to mechanism 2026-09-29 (SWE2-DATA):
`003B3C00` range-checks the lane `0..10` against the `0x38`-stride handle table `02E9D480` and calls
`0024FE70(effectCtx, lane)`, which reads `def = [[ctx+0x130]+0x80]` — `byte[def+0xA+lane]` selects
`dword[def+0x2C+4·map]`, a resource id resolved by `0020E600` and spawned by `00333280(childObj, id, lane)` into the
object's 16-slot child table (lane stamped at `child+0x11`). Lane 0 is no request; the lane indexes the bound
effect's own authored request map, so `1`/`10` are per-effect ports, not global semantics.

**Presentation - effect side (crossing).** `0x28`'s value is consumed by the dirty-bit processor, whose callees belong
to the effect runtime. This section cites it by role and depends only on the setter's write, which was read whole.

## GI-15: the per-site helpers read (OPUS, 2026-10-01)

Static, from the shipping image; a read-only reader pass, checked at the bytes by OPUS (control `gi15_check.py` in
`_index/candidates/opus-gi15-helpers-1001/`). One item per "not read" site above.

**`0x34`, the shadow object.** `003AFC10(h)` returns slot `02B3F570 + (h & 0xFF) * 0x70` when the slot's `+4` equals
`h`, else null. Arms `0x01`, `0x02`, `0x04`, `0x20` and `0x40` are linear ramps, each a count byte, a value and a rate:

| arm | count | value | rate |
|---|---|---|---|
| `0x01` | `+0x1C` | `+0x24` | `+0x2C` |
| `0x02` | `+0x1D` | `+0x28` | `+0x30` |
| `0x04` | `+0x1E` | `+0x34` | `+0x38` |
| `0x20` | `+0x54` | `+0x3C` | `+0x48` |
| `0x40` | `+0x55` | `+0x44` | `+0x4C` |

With `n = byte+3`, the float `dword[cmd + 4]` is always used. When `n <= 1` the value takes it at once and the count
becomes 0. Otherwise `rate = (float - value) / n` and `count = n`. `0x08` sets `+0x1F`'s low nibble to 2 (`byte+3`
non-zero) or 1. `0x10` sets its high nibble to `0x20` or `0x10`. The `0x80` arm switches on `byte+3`:
- 1: `+0x40 = float`;
- 2: `+0x58 |= 2` and word `+0x56` = `0x40`, `0x80` or `0x100` for a float up to 1.5, up to 2.5, or above;
- 4: `+0x58 |= 1` and `+0x50 = float`;
- other values: nothing.

The ramps are stepped by the tick `003AF460` / `003AFB30`
([CONTRACT-authored-command-ramp-channels.md](../CONTRACT-authored-command-ramp-channels.md)). The allocator `003AF340`
sets `+0x1F = 0x11` and the three first values to 1.0. Across the pool `02B3F550`-`02B40370`, no function other than
the tick and the two resets reads these fields. **In static code the pool is write-only**, as `02B3F554` already is,
so what the values do on screen is not established here.

**`0x3F` / `0x48`, `00372800` and key 29.** `00372800` returns -1 unless the resource's `@FTR` entry is of kind 2
(`+0x9C`); otherwise it tail-jumps to `003737C0`. That search returns the first record whose key (`00409250`: word
`+8` when flags bit 30 is set, else link bits 0-11) equals the argument **and whose flags bit 8 is set**; otherwise it
returns `0xFFFF`. The block's `+0x14` is the **bone** the sway hangs on. `00520E90` hands it to `0040ABF0`, which
stores it at oscillator `+0x3C`, and the heavy stage `0040FF30` reads that bone's `0x290`-stride record, and its `+0x284` matrix handle, from `+0x3C`. `+0x16` is the
**preset**: `0040ABF0` stores it at `+0x3E`, and preset 0 skips the set-up. So name key 29 names a skeleton bone of
each model; which bone is per-model data. The corrected field sources:

| | `0x3F` (`00520510`) | `0x48` (`005205B0`) |
|---|---|---|
| `+0x14` bone | `word[cmd + 2]`, used directly (0 in every shipped command) | `00372800(resource, low word of dword[cmd + 0x10])` |
| `+0x16` preset | `word[cmd + 0x10] & 0xFFF` (4, 5 or 6 as authored) | `word[cmd + 2] & 0xFFF` (0 in 5,167 of 5,771) |
| `+0x18` flag | `word[cmd + 0x10] >> 15` | `word[cmd + 2] >> 15` |
| preset zeroed | when `word[cmd + 2]` is `0xFFFF` | when the lookup returns `0xFFFF` |

In both commands "no bone" forces preset 0, which leaves the sway off.

**`00423790`.** This is the reaction-eligibility predicate (`004274E4` is its one call). A non-zero third argument
(`word[rec + 0x3B4]`) whose kind nibble is 0 refuses. No pending record admits. Both ids are then normalised and
kind-tested. The result compares their priorities, `prio[arg & 0xFFF] <= prio[candidate & 0xFFF]`, in the byte map
**`01F00410`**. For `0x203D`, `prio` is 3.

**`004219C0`, the key, `00372760` and `0046E590`.** `004219C0(parent, key, child)` mirrors `004218A0`:
- `key == -1` sets `+0x284` bit 26 and `+0x2F2 = 1`.
- Otherwise `00372800(parent resource, key)` runs, retried once with key `0x1E`, and the bind aborts if both miss.
- It then binds through `0046E640`, the twin of `0046E590` that calls `00370390` instead of `00370180`.

The key is a bone: a C-string bone name for `004218A0` (compared by `00372760`) and a numeric `@FTR` key for
`004219C0`. `004215A0` passes no key for attach code `0x7FFF`, and a looked-up key for the others. `00372760` reads
the kind-0 layout (names at `+0x30`, stride `0x4C`) without testing `+0x9C`. Whether its by-name path ever matches on
the shipped kind-2 `@FTR` data is not established.

**`word[+0x2F2]`, `00373060` and `005048A0`.** `+0x2F2` is a 0/1 flag, set to 1 only by the no-key path of the two
binders. That path is attach code `0x7FFF`, the whole-skeleton bind. The bind still runs then, with bone -1.
`00373060` and `005048A0` are read whole on
[ftr-node-table.md](../Model-And-Motion-Formats/ftr-node-table.md) and
[fdm-and-for-entries.md](../Model-And-Motion-Formats/fdm-and-for-entries.md).

**`0x2A`, the pool, its gate and its table.** The pool is the camera-shake source pool of
[the-element-types-40-42-a0-ab-d0-d1.md](../Effect-File-Formats/the-element-types-40-42-a0-ab-d0-d1.md) (`0x42`). So the
command's three floats are its intensity, time rate and radius scale.
- `003D8300` checks the handle, decrements the live count `02B4D7A0`, clears `+4` and unlinks the slot.
- The gate `02B4D7A2` refuses kind-2 requests in `003D7FF0`. It is set by `003D8D60` (thunk `002EA880`) from the
  script verb `0x4A0` (`deny_char_camerashake`, handler `003517C0`), and cleared by the area unload `002628B0` and
  by init `003D8C30`.
- `003D8C30` fills `02B4E3D0` with four `.data` blocks, `01EFE3A0` / `01EFE520` / `01EFE6A0` / `01EFE820`. They are
  byte-identical: radius 25.0, duration 22.0. The kind-2 path clamps its index to 3 and uses block `+0x80` as the
  shake group.

**`0x16`, the sub-resource variant.** The variant is an `@FCT` palette binding
([fte-fct-texture-colour-tables.md](../Model-And-Motion-Formats/fte-fct-texture-colour-tables.md), `00504D30`).
`003E7210`'s table is the FCP block's section 5 (the word at `[record + 0x400] + 0x0A`). Each listed record takes the
palette resource id at its `+4`. The five authored indices are palette records of the 7 models whose FCP carries
section 5. Which palette each one is, is content.

**`0x09`, the tail.** `0041B650`, `00409190` and `003AB7F0` are read on
[fef-and-motion-entries.md](../Model-And-Motion-Formats/fef-and-motion-entries.md) and
[resource-section-addressing.md](../../02-Resource-And-Asset-Pipeline/resource-section-addressing.md). Past the loop,
`0041BEE0` sets the binding record:
- `+0x14 = 0`;
- `+0x16` = the `@FMN` entry's duration `word[+0x50]`;
- `+0x18` = the same, or 0 when the caller's byte `+0x96` bit 6 is set;
- `+0x1C = (duration - [01DFE0BC]) / duration`, or 0 for a zero duration.

It then calls `0041C260`. A resource index of -1 skips straight to that call.

**Ids 4 and 6.** `00325090` (id 6) never reads the command. For a unit with `+0x698` (and field bit 15 when the unit
is KO, Stone or X-Zone), it calls `00319E40`, which hands the target buffer's ids and the current action-stage handle
to `002EAD00`. Id 4's `00325260` maps the subtype (tables `0032574C` / `00325720`) to an arm:

| subtype | arm |
|---|---|
| 0 | `003191B0` per matching target |
| 2, 6 | the effect handle through `002EACD0`, `0026A430`, `0033CB10` |
| 3 | `003257D0(1)` |
| 4 | `002EB4A0`, then `+0x690 \|= 2` |
| 5 | `002FD0C0(handle, byte+3)` |
| 9 | unit `\|= 0x80000` |
| 7, 8 | nothing (`return 1`) |
| `0x80`-`0x83` (from 1) | `003257D0` with classes 2, 3 then `0xA`, 4, 5 |

`003257D0(class)` emits the reaction (`003176E0`) of every target entry whose code equals the class. The classes are
the evade / parry codes of the formula scratch block's §2.6. Subtype 1 therefore shows every evade and parry
reaction, and 3 the band-C evades.

**Not established here:** what the shadow pool's values do on screen; which bone key 29 or `0x1E` is in each model;
what subtypes 2/6, 4, 5 and 9 look like, and why 7 and 8 are authored at all; which palettes the 7 section-5 models
carry; whether `004218A0`'s by-name lookup matches on kind-2 data. All are content or live questions, not code.

`003B0C50` (655 B) is the type-dispatched row reader `00520C80` consults: `022C6F28` resolves the `0x740` segment row by id, `rbx+0x108`'s movement body is asked for its ground type (-1 falls out), the 19-arm RVA table `003B0EE0` jumps on the type (`003B0D09`), arms select constants `0x64`..`0x67`/`0x94` and the body's depth flag (bit 3 of its `+0x90` word) and depth float (`+0xC0`) feed xmm6 - the per-type parameter fetch the authored handlers apply.

Interior anchor `003B0DD2` (function `003B0C50`).
