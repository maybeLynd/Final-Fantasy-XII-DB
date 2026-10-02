---
system: How a presentation entry picks its track - the 0xA0-byte tracks of a character's authored command stream, their start cursor, and the two commands that switch between them
category: 17-Presentation-Rendering
status: DOCUMENTED
owner_layer: PrimaryOwner:Presentation
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: six bodies disassembled from the authority image and read whole, 2026-09-19 - the track initialiser 0041CD30,
    the reset 0041CFC0, the track finder 0041C9A0, the class 0x01 and class 0x0B command callbacks 00417920 and 00417110,
    and the dirty-mark helper 0041CEC0; field offsets are the ones those bodies read and write, nothing is taken from a
    decompiler's structure guess
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-presentation-track-falsification-pass-1
  note: written by FABLE for FRONTIER-REQ-FABLE-LAST-96-UNCITED-BODIES; static throughout. Scope is track SELECTION only.
    What a track does once it runs - the command interpreter, the states of word +4, who starts a pending track - is not
    on this page and is named as not read; pending first review
---

# How a presentation entry picks its track

A character's render record owns a **presentation entry**: the player of that character's authored command stream
([the authored presentation-command handlers](../Authored-Commands/the-authored-presentation-command-handlers.md)).
The stream is not one script but several - **tracks** - and the entry keeps a small array of track states so that one
can run while another is being brought in. This page is how a track state is set up, how the entry is reset, and the
two authored commands that change which track plays.

## 1. The pieces

**The entry** (fields these six bodies touch):

| entry field | what it is |
|---|---|
| `+0x0C` | flag dword. Bit 6 *a switch may be taken now*, bit 7 *a switch was asked for and is waiting*, bit 9 *dirty*, bit 12 *tracks start flagged `0x20`*, bit 13 copied to the record by the selector command, bit 14 cleared by it, bit 18 *ignore selector commands* |
| `+0x18`, `+0x20` | the **primary** track's state and its stream index |
| `+0x26` | the stream index last chosen by a selector command |
| `+0x28` | how many track states the entry has (signed word) |
| `+0x30` | the track states, `0xA0` bytes each |
| `+0x2C0`, `+0x31C` | the two arguments of the global dirty callback |
| `+0x2DA`, `+0x2DC` | selector argument (word) and **selector kind** (byte; `0xFF` = none) |
| `+0x2E0` | the owning render record |
| `+0x2E8` | bit 2 *a transition snapshot is held* |
| `+0x368` | the authored stream: track count at `+0x0C`, first track header at `+0x30` |
| `+0x380`, `+0x384` | the transition snapshot (section 3) |
| `+0x388` | the track currently playing |

**A track header in the stream:** byte `+0` a kind (`1` = primary), byte `+3` the number of commands, word `+4` the
header-to-next-header distance, commands from `+6`. A command's length is `word[+2] >> 6`.

**A track state (`0xA0` bytes):** `+0x00` an id (-1 = none), `+0x04` a state word, `+0x80` **which stream track this is**,
`+0x84` the header's offset in the stream, `+0x88` the **start cursor**, `+0x8C` the **cursor**, `+0x90` the offset of a
marker command (-1 = none), `+0x94` the last selector choice (`0xFF` = none), `+0x95` *active*, `+0x96` a flag word (bit 0
*primary*, bit 1 *pending*, bits 2 and 7 cleared by a reset, bit 4 *take a snapshot*, bit 5 from entry bit 12), `+0x98`,
`+0x9C` two floats the snapshot copies. Defaults everywhere else: `+0x18` = `0x1E0000`, `+0x20` = 30.0, the two words
at `+0x50` = -1, `+0x68` = -1.

## 2. Setting a track up - `0041CD30(entry, state, index)`

Refuses an index at or past the stream's track count. Otherwise it **walks** to the header - from the first header,
`index` times, each step adding the header's own word `+4` - writes the defaults, and records `+0x80 = index`.
**The track becomes the primary** (entry `+0x18` / `+0x20`, flag bit 0, active) when its header's kind byte is 1 *or the
stream has only one track.*

**The start cursor skips a preamble.** It scans the header's commands for one whose first word is `0xFFFF`. With no
marker the start cursor is the first command (`header + 6`). With a marker, `+0x90` is the marker's offset and **the
start cursor is the command after it**. The cursor starts equal to the start cursor.

## 3. Resetting - `0041CFC0(entry)`

**First a snapshot.** If the track currently playing is active, has flag bit 4, the entry's bit 12 is clear and the
track's float `+0x98` is in `[0, 0.99)`, the entry keeps that float and `+0x9C` at `+0x380` / `+0x384` and raises bit 2 of
`+0x2E8` - *a transition was under way; remember how far it had got.* Then "currently playing" is cleared and **every
track state** is rewound: cursor back to the start cursor, flag bits 2 and 7 dropped, *active* set from flag bit 0 - so
**only the primary survives a reset as active** - the last selector choice forgotten, the defaults rewritten. The stream
offsets (`+0x80`..`+0x90`) are kept.

## 4. Finding a state for a track - `0041C9A0(entry, index)`

Looks only at states 1 and up - **state 0 is never handed out.** A state already holding that stream index is wiped to
defaults and returned; otherwise the first inactive state is returned as it is; otherwise null.

## 5. Command class `0x01`: play track *n* - `00417920(command, current state, entry)`

The command's word `+2` is `track << 4 | mode`. Nothing happens if the current state already plays that track.

| mode | behaviour |
|---|---|
| 0 | **switch now**: take a state (section 4), mark it *pending* with the new track and rewind its cursor. Then retire the current one, unless it plays track 0: with an id, its flag bit 2 is dropped and its state word becomes 2; without one it simply goes inactive |
| 1 | the same, **but only if the current state's word is already 2** |
| 2 | **switch when allowed**: if entry bit 6 is up, take a state and mark it pending, drop entry bits 6 and 7, and wipe the current state in place; otherwise raise entry bit 7 and wait |

## 6. Command class `0x0B`: let a selector choose - `00417110(command, current state, entry)`

Ignored when entry bit 18 is up or the entry has no selector (kind `0xFF`). The command carries a count (low byte of word
`+4`) and that many track numbers from `+6`.

1. **Ask the selector.** The entry's selector kind indexes a table of selector objects at `[02CA4668]`; the object's
   first method is called with the entry, after the command's `word[+2] >> 4` has been left in entry `+0x2DA`. It returns
   a **choice** in the low word and an **addend** in the high word; -1 means no choice. The result is stored in the record
   (`+0x6DC`, with entry bit 13 in `+0x6D8`).
2. **Attached characters copy their parent's choice.** If the record has flag bit 27 and a parent (word `+6`), the selector
   is *not* asked: the choice is read from the parent record's byte `+0x4B8`, `+0x4B9`, `+0x4BA` or `+0x4BB` - for selector
   kinds 0, 2, `0x0A` and `0x10` - where the parent's own run of this command cached it (low 6 bits the choice, bit 6 the
   high half's bit 0). Any other selector kind is asked as in step 1. **So an attached model follows its parent's choice
   instead of making its own** - whatever the selector's rule is, the two stay on the same variant. *What kinds of model
   carry flag bit 27 was not established here.*
3. **Switch if it changed.** A choice at or past the count, or equal to the state's last choice (`+0x94`), does nothing.
   Otherwise every *other* active, non-primary state is wiped, and a class `0x01` command is **synthesised** - header
   `0x0201`, track = `table[choice] + addend`, mode = the low 4 bits of this command's word `+2` - and handed to section
   5. The choice is remembered, entry bit 14 is cleared, and the chosen track number goes to entry `+0x26`.

## 6a. Command class `0x0A`: choose the selector - `00418600`

`00418600` (69 B, read whole) is where the selector kind of section 6 comes from. It copies command bytes `+2`..`+5`
into the entry's `+0x2DC`..`+0x2DF` - **the selector kind and three more selector bytes** - sets the current state's
word `+4` to 1, raises bit 1 of the state's word `+8`, and copies entry dword `+0x340` into state `+0x20`. *What the
three other bytes mean is the selector objects' business, which this page does not read.*

## 7. The dirty mark - `0041CEC0(entry)`

`0041CEC0` (63 B, read whole) calls the global callback at `[02CA4470]`, when one is installed, with the entry's `+0x2C0` and the address of `+0x31C`,
then raises entry bit 9 either way.

**A sibling, command class `0x06` - `00417CC0` (58 B, read whole).** It calls a second global callback, `[02CA4440]`,
when one is installed - with the entry's `+0x2C0` and the command itself - and then sets bit 6 of the entry's qword
`+0x2C8` either way. *~~Who installs the two callbacks was not read.~~* *(answered: see render-event-selection-evidence.md - the installer that page names registers both through `0041D6C0` (`02CA4410 + id*8`): id 6 `002E7090` into `02CA4440` and id 0xC `002E70A0` into `02CA4470`; 2026-10-02, OPUS; installer named by role here, FABLE, so the far-end address stays on the page that reads it)*

## 7a. Two neighbouring commands that act on the same fields, read whole

**Class `0x03`, a timed hold - `00417A80` (72 B).** On the **primary** track it does one thing: raises entry flag bit
3. On any other track it copies the state's word `+0x14` to `+0x18`, raises state flag bit 6, and - only while the
state's countdown word `+0x5E` is still -1 - arms it with the command's word `+2` **multiplied by the frames-per-tick
word `01DFE0B4`**; a command value of -1 is stored as -1. *What counts `+0x5E` down was not read.*

**Class `0x08`, start a blend - `00417D00` (219 B).** Ignored while entry bit 17 or bit 14 is up. It sets bit 0 of entry
`+0x2E8` from command byte `+3`, then reads command byte `+2` as a **frame count**: `0xFF` raises bit 1 of `+0x2E8` and
zeroes the factor; 0 zeroes it; `n` stores **`1 / (n + 1)`** as the per-frame factor at entry `+0x354` and clears bit
1. Then it raises entry bit 11, stores `0x10` at `+0x358`, and - when entry bit 13 is up - raises bit 14, **which is
what makes it ignore itself until the selector command of section 6 clears bit 14 again.** Last, when entry `+0x338`
is not -1, it resolves that resource entry (table at `+0x330`) and clears bit 10 of its first dword. *The snapshot of
section 3 raises bit 2 of the same `+0x2E8`; what reads the three bits and the factor was not read.*

## 7b. Who updates the entries - `0051B970`

`0051B970` (96 B, read whole) updates the presentation entries of one container in **three passes**. Each pass is one
walk of the container's active entries through the same iterator. The first walk uses one callback; the second and
third use another, with the global phase word `02CA83F4` set to 1 for the second walk and 2 for the third, and put
back to 0 afterwards. *Neither callback was read. Their labels say the first takes the entries whose flag bit 12 is
set and the second the ones where it is clear - which would make bit 12, met twice on this page, "update me in the
first pass". That is a lead from a label, not a reading.*

## 8. What a reimplementation must keep

- The start cursor is **after** the `0xFFFF` marker: a track's preamble runs once, at set-up, not on every rewind.
- A reset leaves only the primary active, and keeps a snapshot of an interrupted transition.
- Mode 2 of "play track" is deferred: the request waits in entry bit 7 until something raises bit 6.
- Attached records never roll their own selector; they read the parent's cached byte.

**Not read:** the command interpreter that advances a cursor; what starts a *pending* state; the meanings of the state
word's values beyond "2 is tested by mode 1"; ~~the selector objects behind `[02CA4668]`~~ *(answered: see the handler page's `0x09` section - the pointer is a table of `0x30` entries of `{1, cell}`, stored by `0041D6E0`; 2026-10-02, OPUS)*; who raises entry bit 6.

| body | anchors |
|---|---|
| `0041CD30` track set-up (357 B) | `0041CD34`, `0041CD4B`, `0041CD61`, `0041CD75`, `0041CDC8`, `0041CDCF`, `0041CDE4`, `0041CDEA`, `0041CDF1`, `0041CE08`, `0041CE1C`, `0041CE25`, `0041CE37`, `0041CE3D`, `0041CE48`, `0041CE51`, `0041CE6A`, `0041CE7B` |
| `0041CFC0` reset (325 B) | `0041CFC7`, `0041CFD3`, `0041CFDC`, `0041CFE5`, `0041CFEE`, `0041CFFE`, `0041D00B`, `0041D012`, `0041D030`, `0041D037`, `0041D060`, `0041D06C`, `0041D079`, `0041D07F`, `0041D0EF` |
| `0041C9A0` state finder (203 B) | `0041C9A6`, `0041C9AB`, `0041C9C3`, `0041C9CB`, `0041C9E0`, `0041C9FF`, `0041CA0A`, `0041CA5C` |
| `00417920` class `0x01` (349 B) | `0041792F`, `00417943`, `0041794F`, `00417959`, `00417963`, `0041796D`, `00417978`, `00417987`, `00417995`, `004179D5`, `004179EB`, `00417A03`, `00417A0D`, `00417A19`, `00417A27`, `00417A33`, `00417A3C`, `00417A52`, `00417A66` |
| `00417110` class `0x0B` (703 B) | `0041711A`, `00417138`, `00417152`, `0041715E`, `00417173`, `0041718A`, `0041719E`, `004171A7`, `004171D4`, `004171E7`, `004171FA`, `00417207`, `0041721F`, `00417235`, `00417262`, `0041726B`, `0041728D`, `00417296`, `004172C0`, `004172CE`, `004172EB`, `0041735C`, `00417390`, `0041739A`, `004173AB` |

## Cross-subsystem neighbours

None named. The selector objects and the global dirty callback are reached through pointers and are not identified
here.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**Resource — SERVICE and MECHANICAL (7 edges).** The class-`0x08` body `PresentationAuthoredCommand_Class08_UpdatePresentationTimingAndFactor` (`00417D00`) makes its single call to `ResourceTable_ResolveEntryByIndex` (`002ED570`), the paged resource-table lookup (a 16-byte slot, a 32-byte group selected by the index shifted right by the table's `+0x4C`, a `-1` slot resolving to 0); the other six edges are that lookup's resource-side callers `00409CA0`, `00409D60`, `00409F50`, `00409FE0`, `0046E1B0` and `ResourceTable_ResolveEntryBySignedIndex16` (`004780B0`). Starting a blend resolves one resource entry through the engine's shared table lookup, which the resource layer's own entry helpers call too; nothing about track selection lives in that layer.

## SWE2-EC7-60 update (2026-09-19) - `00417D00`

`00417D00` (219 B) is the class-`0x08` start-a-blend body the presentation-entry page names - `002ED570` single call plus `01CEBBA8`. Interior anchor `00417DC6` (a `002ED570` call).

## Falsification pass 1 — 2026-09-29 (OPUS): every section survives

**Attack.** Sections 2 to 7b and the SWE2-EC7-60 note became checks against the eleven bodies' own instructions.
Script: `Tools/analysis-kit/gfz-scripts/falsify_presentation_track.py`, output `falsify_presentation_track.out`, image
`73461d08…`, 0 BROKEN, exit 0. The page's "not read" items stay as the page states them.

| # | Clause attacked | Result |
|---|---|---|
| T0 | sizes | **survives**: all eleven |
| T1 | section 2 | **survives**: the count bound, the header walk by word `+4`, `+0x80 = index`, primary when kind 1 or one track, the `0xFFFF` marker scan |
| T2 | section 4 | **survives**: the finder starts at `+0xD0` (state 1) with stride `0xA0`, so state 0 is never handed out |
| T3 | section 5 | **survives**: track `>> 4`, mode `& 0xF`, and the state-word-2 test of mode 1 |
| T4 | section 6 | **survives**: entry bit 18 (`0x40000`), the `0xFF` kind, table `[02CA4668]`, the parent's cached bytes `+0x4B8`..`+0x4BB` (read, and written by this command), header `0x0201` |
| T5 | section 6a | **survives**: bytes `+2`..`+5` into `+0x2DC`..`+0x2DF`, state word 1, `+8` bit 1, `+0x340` into `+0x20` |
| T6 | section 7 | **survives**: the `[02CA4470]` callback with `+0x2C0` / `&+0x31C`, and bit 9 on both paths; the class-0x06 sibling's `[02CA4440]` and `+0x2C8` |
| T7 | section 7a | **survives**: `01DFE0B4` in the timed hold; the blend factor at `+0x354` and `0x10` at `+0x358` |
| T8 | section 7b | **survives**: phase word 1, 2, then 0 |
| T9 | the EC7-60 note | **survives**: one call, `002ED570` at `00417DC6`, and the `01CEBBA8` constant |

No correction.

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-how-a-presentation-entry-picks-its-track-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0051B970` | 96 B | calls `0051F580(rcx, 0051BBE0, rcx)`, then sets dword `02CA83F4` to 1 and calls `0051F580(rcx, 0051BBF0, rcx)`, then sets it to 2 and calls `0051F580(rcx, 0051BBF0, rcx)` again, and finally sets dword `02CA83F4` to 0 | `0051B983`, `0051B98B`, `0051B9A7`, `0051B9BB`, `0051B9C0` |
