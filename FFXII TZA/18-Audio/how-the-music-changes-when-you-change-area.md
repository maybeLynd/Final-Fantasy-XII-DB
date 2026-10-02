---
system: How the music changes when you change area
category: 18-Audio
status: DOCUMENTED
owner_layer: CodeDomain — Audio boundary
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  parent_tag: GN159
last_reviewed: 2026-09-03
archive_formats:
  - "musicinfo | explained | musicinfo.bin (.bin member): {u8 flags, u8 track} records behind 022CBA50 - loaded by 00360C70, bit 0 read by 00361010, the rest authored-but-unread (UQ-263)"
audit:
  passes: 1
  last_pass: 2026-09-08
  last_pass_state: GN160-xiionline-61-field-track-table
  crossref_clean: false
  reopened_count: 0
---

# How the music changes when you change area

`00261F90` (335 B) was on the *leaned on and never opened* cut with four citing documents, all of them
naming it only as **"the Audio callee"** of the per-frame field pass. It is read here.

**Extent checked**: 93 instructions, ends `ret` at `002620DE`, no `jmp` leaves the extent, no loops.

## 1. What the player sees

You walk through a zone boundary and the music changes — sometimes to the new area's theme, sometimes
to one of two special tracks, and sometimes it does not change at all because your **save file pins
it**. All of that is decided here, in one pass, and the crossfade is one duration and one volume.

## 2. It runs once per transition, and says so with a bit

```asm
00261F96  cmp  dword ptr [rcx + 0x28], 0
00261F9D  jne  return                    ; a mode is already in progress
00261FA3  test byte ptr [rcx + 0x10], 0x40
00261FA7  jne  return                    ; already done
...
002620D5  or   byte ptr [rcx + 0x10], 0x40   ; mark done, on the way out
```

**`context + 0x10` bit `0x40` is a done-latch**, set on the only path that reaches the end. Because the
field pass calls this every frame, **the latch is what makes it a transition handler rather than a
per-frame one** — and nothing in this function clears it.

## 3. Which track: four sources, in priority order

The music block runs only when `context + 0x17` has bit 7 set, and picks an id like this:

```asm
0026200F  call WorldTransition_GetActiveOrPendingFieldId      ; 1. the field id
00262016  call SaveImage_GetPersistentPayloadBase
0026201B  test byte ptr [rax + 0x1063], 0x40
00262024  call SaveImage_GetPersistentPayloadBase
00262029  movzx edi, byte ptr [rax + 0x1534]                  ; 2. a SAVED override
00262034  call 0x3eaa70                                       ; 3. field id -> track id
...
0026204A  call <state thunk>   -> edi = 0x5B                  ; 4. two special tracks
0026205A  call <state thunk>   -> edi = 0x5A
```

> **A byte in the save file can override the area's music.** When `payload + 0x1063` has bit `0x40`
> set, the track comes from `payload + 0x1534` and the field-to-track mapping is skipped entirely.
> **That is a saved piece of audio state, not a setting** — and it is one byte.

Two fixed ids, **`0x5A` and `0x5B`**, are selected by two state predicates when the mapped id is
rejected. **Which state each predicate tests was not followed**; the ids are recorded because they are
the only two literal track numbers in the function.

**A per-track flag table gates the mapped id:**

```asm
00361010:  movsxd rax, ecx
           movzx  eax, byte ptr [rdx + rax*2]    ; table at 022CBA50, stride 2
           and    eax, 1
```

~~**Bit 0 of a two-byte-per-track record decides whether the mapped track is used at all.**~~
**Corrected 2026-09-11: bit 0 exempts the track from the two overrides below.** When it is clear the
mapped id is still used unless one of the two predicates fires (`00262046` `jne` past them; the fall
through at `00262061` keeps `edi`); when it is set both predicates are skipped. The table is
`musicinfo.bin` — see the section *DG-2 answered* at the end of this document.

## 4. The crossfade is one duration and one volume

| constant | where | meaning |
|---|---|---|
| `0x78` = 120 | passed as the duration argument at three sites | a fade length |
| `0x7F` = 127 | hardcoded inside `003614C0`, and passed directly at one site | **full volume** |
| `0x00` | passed where `0x7F` otherwise goes | **silence** |

`0x7F` is the same full-scale value the mixer boundary uses — the volume path divides by 127, so
**`0x7F` is 1.0** — documented in
[`Audio-Boundary/how-a-sound-request-becomes-a-voice.md`](Audio-Boundary/how-a-sound-request-becomes-a-voice.md).
**`0x78` is 120 units of whatever the fader counts**, which this function does not establish; at 60 Hz
it would be two seconds, and that is an inference, not a reading.

The three helpers behind it are small and were read:

| address | body | what it does |
|---|---:|---|
| `002DEC00` | 7 B | returns `dword [0215EF44]` — **the current track id** |
| `002DEE50` | 27 B | if the argument is negative, substitutes the current track; **writes a volume byte to `0215EF4D`** and tail-calls the fader |
| `003614C0` | 28 B | forwards its arguments with **`r9d = 0x7F` hardcoded** — a "start at full volume" wrapper |

**So `0215EF44` is the playing track and `0215EF4D` is its target volume**, and a fade is: set the
byte, let the fader walk it.

## 5. The two outcomes

- **A track was chosen** (`edi >= 0`): `003614C0(id, 0x78, 1)` starts it at full volume. If that
  returns `2`, `002DEE50(current, 0x78, 0x7F)` is also called — **a second fade on the outgoing track**.
- **No track was chosen** (`edi < 0`): if something is playing, it is faded to **volume 0** and a
  second call runs; **if nothing is playing, bit 7 of `context + 0x17` is cleared** — the function
  gives up on music for this transition rather than retrying.

## 6. Modding notes

- **`context + 0x10` bit `0x40` is a done-latch.** Clearing it makes the transition handler run again
  on the next frame.
- **The save file can pin the music** — `payload + 0x1063` bit `0x40`, id at `payload + 0x1534`.
- **`0x5A` and `0x5B` are hardcoded track ids** and the only two in this function.
- ~~**`022CBA50` is a per-track flag table, stride 2, bit 0 = usable.** A track whose bit is clear is
  never started by this path.~~ **Corrected 2026-09-11:** `[022CBA50]` points at `musicinfo.bin`
  (256 × `{u8 flags, u8 track}`), and **bit 0 exempts a track from the mode-1 / mode-2 overrides**;
  eighteen shipped tracks carry it. Every track `musicctrl.bin` names has a `.win.mab` file.
- **The fade is `0x78` long and `0x7F` loud**, and both are immediate operands — patchable without
  finding a table.

## 7. What is not known

- [x] ~~What unit `0x78` counts. **Frames is a guess and is not made in this document.**~~ **Answered 2026-09-14 (FABLE)
      for the outgoing-track fade: sixtieths of a second of real time, so `0x78` is 2.0 s.** `002DEE50` →
      `001DBCA0` → the registry's music controller (`00210A50` → `00218E50`) → `00222B70`. That function converts
      the length with `(float)len / 60.0` (`008F6D54`) and the volume with `/ 127.0` (`00906A44`), then calls SEAD's
      `SetVolume` `007A81F0`. SEAD advances every ramp by a `dt` it measures itself. `007A5400` takes
      `QueryPerformanceCounter` (`007AD630`) minus the previous sample, divides by `QueryPerformanceFrequency`
      (`007AD6D0` → `02EAD0C0`), and passes the result to the action consumer `007AB5C0` and the category step
      `007AAEA0` (`007A5452`–`007A54B2`). The divisor is a fixed 60, not the game's frame rate, so the fade lasts
      2 s at any `FrameLimit`. The start call `003614C0(id, 0x78, 1)` passes the same number into `003614E0`, whose
      conversion was not read.
- [x] ~~What the two state predicates behind `0x5A` and `0x5B` test.~~ **ANSWERED 2026-09-11** — the
      [battle runtime mode ladder](../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md):
      `0037C8F0` → `003135C0` is `mode == 1` (flags bit 0, the UI's) → `0x5B`; `0037C860` →
      `00303EC0` is `mode == 2` (flags bit 1) → `0x5A`. Tested only when the mapped track's
      `musicinfo.bin` bit 0 is clear.
- [x] ~~What `003EAA70` (229 B) does to map a field id to a track id.~~ **ANSWERED 2026-09-08 — a
      paged, run-length-compressed table with a per-run threshold ladder on the story progress
      variable.** Base `0x02B5E0D0`, paged by `fieldId / 128`; a run is
      `{u16 start|len, u8 count, u8 default, entry[count]}` with `entry = {u16 threshold, u8 track}`
      and stride `4 + 3*count`; the ladder key is `FieldData_GetVariable0`. Track `0` returns `-1`.
      See the section at the end of this document.
- [x] **UQ-263.** ~~What the other 15 bits of a `022CBA50` entry hold~~ — the record is `musicinfo.bin`'s
      `{u8 flags, u8 track}` (2026-09-11); bits 1, 2 and 7 of the flags byte and the second byte (a
      different track number on eight records: 101→36, 102→61, 104→73, 106→95, 111→44, 112→44,
      114→72, 116→83) have **no reader in the image** — `00361010` is the pointer's only reader.
      `DG-2` carries what they might mean.
      **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): they are authored data this build never reads.** Static.
      - The pointer cell has three non-`lea` accesses in the whole image: the loader's clear, the done callback's
        store, and `00361010`'s load. That reader keeps bit 0 of the first byte and never touches the second.
      - The only `lea`s near the cell resolve to `022CBA51`. That is the end bound of the four-slot track table
        `022CB9F0` (4 × `0x18`, walked from base + 1), not the pointer.
      - `00360C70` hands its buffer to one call, the resource request, as the destination and in the done
        descriptor through which `00360B40` stores it. No other code holds the buffer.

      So the bits and the byte cannot affect play in this build, and their authored meaning is not recoverable
      from it. Control: `_index/candidates/uq263-musicinfo-readers/musicinfo_readers.py`, 7 checks, FAILS 0. The
      census's planted positive is the loader's own clear.
- [x] **UQ-264.** What the non-music path (`context + 0x17` bit 2 clear) does with `0x37C910(1)`.
      *Narrowed 2026-09-14 (FABLE): it starts a scheduled area task, not a music action.* `0037C910(arg)` (108 B):
      1. **Stores the argument** at `02ADD970` and zeroes the task's small state block `02ADD950`–`02ADD968`.
      2. **Takes a free task slot.** `002F16B0` finds the first clear bit of the 32-bit mask `022BE7C0`, sets it, and
         returns record `022BDEC0 + index × 0x48` — a **`ScheduledTaskRecord`** (declared in the store
         2026-09-18: `PARRAY 0x022BDEC0 stride=0x48 count=32`; `+0x00` elapsed/`+0x04` duration ticked by the
         `002F1780` dispatcher, `+0x10` tick / `+0x08` completion callbacks, `+0x1C` stepIncrement, `+0x1E`
         taskTag, `+0x20` dispatchGate).
      3. **Clears two sets of flags.**
         - Bit 4 of byte `+0x19` on all 128 records of the script-entity table `0215FDA0`, walked two records per step.
         - The `+0x40` dword (`liveMaskByEntry`) of the 32 `NameBindingSubRecord`s of `0x120` stride at `02161DA0`, which are the records the area
           flag-mask setter writes.
      4. **Fills the task record**: `+0x00 = 0`, `+0x04 = 10`, `+0x08 = 0`, `+0x10 =` the callback `0037C3F0`,
         `+0x1C = 0` (`0037C95A`–`0037C972`).

      The callback is the eleven-state machine that
      [the ARD loader page](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md)
      records as reading the area trailer's `{selector, mask}` list. So the non-music path schedules
      the per-area actor flag-mask pass. `0037C910` has three callers: `00261F90`, `003473A0` and `00359800`.
      ~~**Not read:** the eleven states themselves, and what argument 1 selects in them.~~

      ***ANSWERED 2026-09-21 (FABLE) — the argument is a pass count, and `1` buys a third source.***
      Read complete over the body's **true** extent (see the note at the end of this item).

      - **`02ADD955` is the pass counter, not the trailer index.** It is zeroed by `0037C910`, incremented
        once per completed pass at `0037C6A6`, and the entry index is the separate dword `02ADD950`.
      - **A pass per source.** The gate at `0037C430` compares it with `2`: on passes **0 and 1** the table
        comes from `003EA650(pass)` — the trailer accessor, which **accepts only 0 and 1** (`003EA654 cmp
        ecx, 1` / `ja` → returns 0), indexes the two-slot carrier table `02B5E0C0` and resolves that
        carrier's `+0x0C` `trailerOff`. On pass **2** it takes the other branch: `00263FF0(0)` is
        `02098E10 + idx × 0x288`, so `rbx` is **manager slot 0's `+0x00` bound payload**, and `ecx` is the
        payload header's dword at `+0x80`, resolved by `0020E600` and added to the payload base.
      - ***And the argument decides whether pass 2 happens at all.*** State 9 loads `2` and `cmove`s `ebp`
        (which the loop head sets to `3`) **when `dword[02ADD970]`, the stored argument, equals 1**
        (`0037C690`–`0037C6A3`). **So `0037C910(1)` means "the two carriers *and* the slot-0 payload's own
        table"**; any other argument means the two carriers only. That is what the non-music path buys.
      - **The table is `{u32 count; struct { u32 id; u32 mask32; } entries[count];}`** — `0037C484` tests
        the count at `+0`, and the entries are read at `+4` and `+8` on a stride of 8.

      **The eleven states**, from the image-base-relative jump table at `0037C6F8`:

      | state | arm | what it does |
      |---:|---|---|
      | 0 | `0037C4CB` | `003601B0(10)` — sets **bit 10** of `022CB720` — then state 1 |
      | 1 | `0037C4E0` | resolves the entry's id through `002E9A60`, **find-or-creates** the name binding with `002EAE20(id, 0)`, stores the handle at `02ADD958`, **pins it** with `002EBD40(handle, 1)`, then state 2 |
      | 2 | `0037C550` | polls `002E4C20(handle)` — `byte[handle+0x18] & 2`, the **ready** bit — and **returns** to be resumed next tick until it is set; then state 3 |
      | 3 | `0037C566` | the entry's `mask32` non-zero → state 4, zero → state 8 |
      | 4 | `0037C59B` | zeroes the bit cursor `02ADD954`; state 5 |
      | 5 | `0037C5AD` | scans the cursor `0..31` with `bt`; on the first **set** bit calls `002EB5D0(handle, bit)` and stores the sub-record at `02ADD960` → state 6; at 32 → state 7 |
      | 6 | `0037C62A` | polls `002E4C30(subrecord, cursor)` and **returns** until it is positive, then `++cursor` and back to state 5 |
      | 7 | `0037C656` | state 8 |
      | 8 | `0037C661` | reads the count, `++`the entry index, loops to state 0 while entries remain, else state 9 |
      | 9 | `0037C689` | resets the entry index, `++`the pass counter, loops to state 0 unless the pass limit is reached |
      | 10 | `0037C6C3` | `003601C0(10)` clears bit 10 of `022CB720`, clears `02ADD968` and `02ADD970`, returns |

      ***And that closes a loop this page had open in two places.*** `002EBD40` is a complete 19-byte
      body — `test rcx,rcx` / `je` / `and byte ptr [rcx+0x19], 0xEF` / `and dl, 1` / `shl dl, 4` /
      `or byte ptr [rcx+0x19], dl` / `ret` — so `002EBD40(handle, 1)` **sets bit 4 of `byte[+0x19]`**, the
      `pinFlags` byte [the naming page](../01-Script-VM-Native-Bridge/how-a-script-names-a-thing-in-the-world.md)
      declares. **Step 3 above clears that same bit on all 128 script-entity records at schedule time.**
      Clear every pin, then re-set exactly the entries the tables name: **the task is a mark-and-sweep
      pin pass**, and the clearing and the setting were recorded in two different sections of this page
      without being joined.

      *That the two touch the **same** records is established rather than assumed, because adjacent
      globals are not evidence.* `002EAE20` find-or-creates by walking the lists at `[0215FD58]` and
      `[0215FD78]` matching `+0x14`, and allocates through `002E25E0`, which pops the free head
      `[0215FD60]`. A sweep of every rip-relative reference to both globals finds the link in
      `002EA320`: `002EA410` does `lea rax, [0215FDA0]` and **the next instruction**, `002EA417`, does
      `mov qword ptr [0215FD60], rax`. **The free pool is the 128-record table**, so a bound entry is
      one of the records step 3 cleared. *(`002E25E0` also masks the new node's `+0x19` with `0xC8`,
      which clears bit 4 — a fresh node starts unpinned.)* *(`002EBD40` is itself absent from `functions.tsv` — the nearest listed entry
      is `002EBD60` — which is the third blind spot in the note below, and the one that carried the
      meaning.)*

      **Two mechanisms worth naming inside that.** *State 1 temporarily swaps the current manager slot*:
      `002640C0` reads `02099D70`, `0026A480` writes it, and the arm saves it, sets it to slot 0, resolves
      the id, and restores it — which matters because `002E9A60` routes an id **≥ `0x1000000`** through
      the *current* slot (`00263F80`) and anything lower straight to `002EB7A0`. *And state 6's wait is
      per sub-record*: `002E4C30` reads `word[rcx+0x1E]` as an index into the **32 `NameBindingSubRecord`s
      of `0x120` stride at `02161DA0`** — the same records step 3 above clears `+0x40` on.

      **What this does not establish.** Static only: which pass a real area load takes, how often the task
      runs, and whether any shipped entry's `mask32` is ever non-zero are not observed here.

      > ***A measurement defect found while reading this, and it is not confined to this function.***
      > `functions.tsv` records `0037C3F0` as **248 bytes**, ending at `0037C4E8`. **Nine of its own eleven
      > arms lie past that**, out to `0037C6C3`, with the jump table at `0037C6F8` — the recorded extent
      > stops at the end of **state 0's arm**, which is where linear decoding after the indirect `jmp rcx`
      > at `0037C4C9` stops being obviously continuous. The region `0037C4E8`–`0037C730` is unlisted. The
      > `SWE2-EC7-45` update on the ARD loader page repeats the 248 figure, and `disr.py` slices its buffer
      > with `funcs[fn]`, so **the tool cannot show a byte past the recorded end**: the table and the
      > reader share one blind spot. Anything keyed on `body_bytes` measured a fifth of this body. Read
      > here with a range disassembler that ignores the table.
      >
      > ***And "not confined to this function" is measured, not asserted.*** Over all **38,161** listed
      > functions, the signature — a body containing an indirect `jmp <reg>` **and** more than 16 bytes
      > of unlisted space before the next listed entry — holds for **457**. The two halves are kept as
      > controls so the figure can be read: **529** functions contain an indirect `jmp` at all, so the
      > decode is working rather than finding nothing, and **1,206** have an unlisted gap, so the gap
      > rule selects rather than matching everything. `0037C3F0` is in the flagged set, which is the
      > positive control. **The signature is suggestive, not proof per case** — a jump table stored
      > after a *complete* body produces exactly the same gap, and some gaps are ordinary data — so what
      > the 457 establish is the size of the population where `body_bytes` cannot be trusted without
      > reading, not 457 truncations. For this one, the truncation is verified directly: nine arms and
      > the table lie past the recorded end.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The done-latch and its two entry guards | `00261F96`–`00261FA7` and `002620D5` | 1 |
| The save override and its gate | `0026201B` `test [rax+0x1063], 0x40`, `00262029` `movzx [rax+0x1534]` | 1 |
| `0x5A` / `0x5B` are the only literal track ids | `00262053` and `00262063`, and no other literal reaches `edi` | 1 |
| The per-track flag table and its stride; bit 0 skips the two overrides rather than gating the track | complete body of `00361010` — `movzx [rdx + rax*2]`, `and 1`; `00262041`–`00262068` (`jne` past both predicates, fall-through keeps `edi`) | 1 |
| `0215EF44` is the current track, `0215EF4D` its volume byte | complete bodies of `002DEC00` and `002DEE50` | 1 |
| `0x7F` is hardcoded inside the start wrapper | complete body of `003614C0` — `mov r9d, 0x7f` | 1 |
| Failure clears bit 7 rather than retrying | `00262097` `and byte ptr [rbx+0x17], 0x7f` | 1 |

**Control.** The absence claim is *"no other literal track id appears"*. The same reading positively
finds `0x5A` and `0x5B` and every other immediate in the body (`0x78`, `0x7F`, `0x40`, `0x80`, `1`,
`4`), so the zero is a measurement over a fully decoded 93-instruction function.

## 9. Related

- [`Audio-Boundary/how-a-sound-request-becomes-a-voice.md`](Audio-Boundary/how-a-sound-request-becomes-a-voice.md)
  — the mixer boundary where `0x7F` is shown to be full scale
- [`../04-Actor-Entity/the-field-runtime-pass.md`](../04-Actor-Entity/the-field-runtime-pass.md)
  — the per-frame pass that calls this every frame, and against which the done-latch is the guard

## The field → track table, read — 2026-09-08

**`003EAA70` (229 B) is decoded**, and it answers the question this document opened with from the
data side: **why the music in an area changes as the story advances.**

### What a player hears

**Every area has a list of tracks, not one track**, and which one plays is chosen by **how far the
story has got**. The same field, entered at two points in the game, plays different music — and that
is not scripted per visit; it is a small authored ladder attached to the area itself.

**An area with nothing on its ladder is silent** rather than falling back to something generic.

### The table

Base `0x02B5E0D0`. `[+0x04]` is the **highest field id** the table covers; anything above it returns
**−1** immediately.

**It is paged by 128 field ids:**

```c
if (fieldId > table[1]) return -1;
page = fieldId / 128;                      /* sar 7, with the +0x7F negative rounding */
run  = (u8 *)table[2 + page];              /* dword at +0x08 + 4*page */
if (run == NULL) return -1;
```

*Qualified 2026-09-27 (FABLE, Claude Opus 5.5), on `ASTRA-RETURN-FABLE-MUSICCTRL-PAGE-BOUNDARY`: `fieldId` equal to
`table[1]` is accepted. When `table[1]` is a multiple of 128, 0 included, that id selects a page word the load callback
never rebased. See [the control-file page](the-music-control-file-and-the-bgm-stream.md) §2.2; the shipped 1311 is
unaffected.*

**Each page is a chain of runs**, each covering a contiguous span of field ids:

```
run + 0x00   u16   packed   -> start = packed & 0x7FF   (11 bits)
                               len   = packed >> 11     (5 bits)
run + 0x02   u8    count    -> number of ladder entries
run + 0x03   u8    default  -> track id when no entry matches
run + 0x04   entry[count]   -> { u16 threshold, u8 trackId }, 3 bytes each

next run = run + 4 + 3 * count
```

Walking the chain:

```c
for (;;) {
    start = packed & 0x7FF;  len = packed >> 11;
    if (start > fieldId)          return -1;   /* runs are ordered; overshot */
    if (start + len >= fieldId)   break;       /* this run covers it */
    run += 4 + 3 * count;
}
```

> **An 11-bit start and a 5-bit length in one `u16`** — so a run covers at most 32 consecutive field
> ids, and field ids are bounded at 2,047 by the encoding. **The 1,154 fields the navimap table
> counts fit inside that.**

### The ladder — and the key is the story progress variable

Inside the matching run:

```c
track = run[3];                                  /* the default */
p = run + 4;
for (i = 0; i < count; i++, p += 3) {
    threshold = p[0] | (p[1] << 8);
    if (progress <= threshold) break;            /* stop at the first threshold not passed */
    track = p[2];                                /* otherwise take this entry and keep going */
}
return (track == 0) ? -1 : track;
```

where

```c
progress = (s16)FieldData_GetVariable0();        /* 00265270 */
```

> **`FieldData_GetVariable0` is the story progress variable this database already documents** —
> [`../14-Story-Event-Quest-Hunt/persistent-flag-banks.md`](../14-Story-Event-Quest-Hunt/persistent-flag-banks.md)
> reads it as *"the first `u16` of the current field's authored variable block, or 0 when the block is
> absent"*, and records the **same threshold-ladder idiom** — authored `u16` thresholds compared
> against it in order.
>
> **So the music table and the persistent flag banks are driven by one number, through one shape.**
> Neither document knew about the other; the join is the finding, not the ladder.

**The value is fetched once, before the table is even bounds-checked** (`003EAA78`, the first call in
the function), and sign-extended to 16 bits at `003EAB10` — so a progress value above `0x7FFF` reads
as negative and matches no threshold, leaving the default.

**Track id `0` means "no music"**, converted to `-1` on the way out by a `cmove`. It is not a valid
track that happens to be silent — the caller gets the same `-1` as an unmapped field.

### Modding notes

- **To change what plays in an area you edit its run**, not a global list: find the page
  `fieldId / 128`, walk to the run whose `start … start+len` covers the field, and either change
  `run[3]` (the default) or an entry's `trackId` byte.
- **Entries are ordered by threshold and the walk takes the last one passed.** Inserting an entry out
  of order silently changes every field in the run, because the loop stops at the first threshold the
  progress variable has *not* passed.
- **A run covers at most 32 field ids** — the length field is 5 bits. Widening a run past that is not
  possible without splitting it.
- **Setting a track id to 0 mutes the area** rather than falling back to a default.
- **The whole map is keyed on one `u16` per field.** Anything that changes that variable changes the
  music, which is why the same area sounds different after a story beat.

### What is still not known

- [x] ~~**Where the table at `0x02B5E0D0` comes from** — whether it is built at load from an archive
  file or is static image data. Nothing here writes it.~~ **ANSWERED 2026-09-11** — the shipped file
  `in/common/musicctrl.bin`, kind 9 index 32, loaded whole through the request queue at boot and
  rebased in place; [the music-control page](the-music-control-file-and-the-bgm-stream.md) §2. `DG-1`.
- [x] ~~**What a track id indexes.** The function returns a number; **which sound bank or stream list it
  selects is not established here.**~~ `DG-2` **ANSWERED 2026-09-11** in the section *DG-2 answered* at the end of this
  document: the id names `musicNNN.win.mab`. *(Box ticked 2026-09-14, FABLE; the answer had landed without it.)*
- [x] ~~Whether any shipped run actually uses more than one ladder entry, or whether the ladder is a
  facility the authored data barely exercises — **a census of the shipped table would settle it, and
  it has not been run.**~~ **ANSWERED 2026-09-11** — 48 of the file's 291 runs carry a ladder, 133
  rungs, up to six on one run; [the music-control page](the-music-control-file-and-the-bgm-stream.md) §2.3. `DG-3`.

### ⚠ Correction and `DG-1`, 2026-09-08 — the base address, and where the table comes from

**The base address published above was wrong when first written: `0x02BDE0D0`. It is `0x02B5E0D0`.**
Two digits transposed while computing the RIP-relative target by hand from
`mov r8, qword ptr [rip + 0x277364c]` at `003EAA7D`. Recomputed from the bytes:
`0x003EAA84 + 0x0277364C = 0x02B5E0D0`. **Corrected in every place it appeared.**

> **The instrument caught it, not a re-reading.** A cross-reference scan for the wrong address
> returned **zero references** while its control passed — and a table the mapper demonstrably loads
> cannot have zero references. **The contradiction was the signal**; trusting the scan over my own
> arithmetic is what found it.

### `DG-1` answered — built at load from a resource, not static image data

`0x02B5E0D0` lies **past `.data`'s raw content** (raw 1,631,232 bytes against 18,511,152 virtual), so
it is zero at load and filled at runtime. The correct-address scan finds **4 references in 3
functions**, and one of them writes:

```asm
003EAB60  sub  rsp, 0x28
003EAB64  mov  edx, 0x20                 ; element size 0x20
003EAB69  lea  r8,  [003EAB90]           ; an associated handler
003EAB70  lea  ecx, [rdx - 0x17]         ; = 9, the resource selector
003EAB73  call 0x51ED10                  ; FUN_0051ed10, tagged FFXII.ResourceDataLoading
003EAB78  mov  qword ptr [02B5E0D0], rax ; install the result
```

**So the field → track map is fetched as resource `9`, element size `0x20`, through the
resource-loading path** — it is **not** in the executable.

> **A modder edits a data file, not the binary.** Which archive entry resource 9 resolves to is **not
> established here** — `0051ED10` (153 B) is unread. `DG-4`.

`003EAB60` is **not** a CRT static initialiser, has no direct `call` sites and is not stored in any
data table, so **what triggers the load is unestablished**. `DG-5`.

**`DG-3` cannot be answered from the image at all** — the shipped runs are in the resource, not the
binary, so the question of whether any run uses more than one ladder entry needs the extracted file.

### ⚠ Correction, 2026-09-08 — "resource 9" was an over-reading; 9 is a size-table id

**Published in the section above:** *"the field → track map is fetched as resource `9`, element size
`0x20`, through the resource-loading path"* and *"a modder edits a data file, not the binary."*

**Following the chain one hop further shows the first half is wrong.**

`0051ED10` (153 B) begins by calling `0032E400(9, 0x20)`, and that function is a **size lookup**:

```c
if (selector == 0xFF) size = -1;
else {
    table = ((void **)0x022C51F0)[selector];       /* a table of tables, selector < 0xFF */
    if (table && index < 0x400) return table[index];   /* dword, returned as-is */
    size = FUN_0046DE70();                        /* the default */
}
if (size > 0) size = (size + 0x3F) & ~0x3F;       /* round up to 64 */
return size;
```

**So `9` selects a size table and `0x20` indexes it** — the pair yields a **byte count**, not a file.
`0051ED10` then passes that to `0036A190` (10 B, `Runtime.MemoryAllocatorSupport`) to obtain a
pointer, and on to `0032E620` (340 B) with the selector, index, pointer and size.

> **What is established:** `0x02B5E0D0` holds a pointer to memory **allocated** at a size drawn from
> table 9 index 0x20, and it is BSS, so it is not in the executable.
>
> **What is not established, and what the earlier text asserted anyway:** that the contents come from
> an archive file. **The `FFXII.ResourceDataLoading` tag on `0051ED10` is a ledger claim, and I
> promoted it to "fetched as resource 9" without reading past it.** `0032E620` (340 B) is where the
> buffer is populated and it is **unread** — so *whether a modder edits a file at all* is open again.
>
> **The tag was not wrong; my sentence was.** "Resource data loading" is a fair description of a
> function that sizes and allocates a resource buffer. The error was reading a category name as a
> mechanism.

`DG-4` is therefore **not** answered by naming an archive entry — the question is now: **what fills
the buffer?** `0032E620`. And a new one: **what is the table of size tables at `0x022C51F0`**, which
serves at least three callers and up to 255 selectors of 1,024 entries each. `DG-6`. *Answered 2026-09-13:* it is the resource system's per-kind **size-override** array, and the 256-pointer array at `022C51F0` is **never filled in this build**. Its only references are the resource initialiser `0032EA90`, which zeroes all 256 qwords (`0x20` iterations of 8 stores, `0032EAB1`–`0032EAD8`), and the two size readers `0032E400` and `0032EB40`, which fall back to the `.fst` table (`002DF960`) whenever the pointer is null. Controls: the RIP scan that finds those three sites finds no other; no absolute displacement and no data qword addresses the array. So every request size comes from the `.fst`, and the pointer path — which skips the round-up to 64 — is dormant ([the `.fst` page](../02-Resource-And-Asset-Pipeline/Loose-Files-And-Size-Tables/file-size-tables-fst.md)).

### `DG-4` pushed one hop further, 2026-09-08 — still no file, and a state block

`0032E620` (340 B), the function that receives the allocated buffer, was read as far as its gate:

```c
g_currentSelector = selector;        /* 0x022C51D8 */
g_currentIndex    = index;           /* 0x022C51DC */
if (index < 0) return -1;
if (!FUN_003EB0D0()) goto alternate; /* 0x0032E742 */
/* then a 0x28-byte descriptor is copied in from the caller's stack struct */
```

**`FUN_003EB0D0` (41 B) is a presence check**, not a loader:

```asm
003EB0D2  lea  rax, [02B5E111]      ; a byte inside a 0x38-stride entry
003EB0E0  cmp  byte ptr [rax], 0
003EB0E3  jne  -> return 1
003EB0E7  add  rax, 0x38            ; but the loop bound is 1 iteration
003EB0EB  cmp  ecx, 1 / jl
003EB0F0  xor  eax, eax / ret
```

**The loop is written to walk a `0x38`-stride array and bounded to exactly one entry** — so it reads
as a generalisation that was never used, or an array that shrank to one.

Those addresses sit in one block:

| address | what |
|---|---|
| `0x02B5E0D0` | the field → track table pointer |
| `0x02B5E0E8` | another pointer, read by `003EB100` — *the BGM stream descriptor's buffer (`02B5E0E0 + 0x08`), DG-7* |
| `0x02B5E111` | the byte `003EB0D0` tests — *the descriptor's `+0x31` active flag, DG-7* |
| `0x022C51D8` / `0x022C51DC` | current selector / index, **`0x18` before the size-table array** |

> **Nothing in `0051ED10`, `0032E400`, `0032E620` or `003EB0D0` touches a file.** The chain so far
> sizes, allocates, records the selector and index in globals, and gates on a presence flag.
>
> **So the retracted claim stays retracted and is not replaced by its opposite:** it is *not*
> established that the map comes from a file, and it is *not* established that it does not. Four
> functions in, the file has not appeared — which is worth stating precisely because the temptation
> after a retraction is to assert the reverse.

The remainder of `0032E620` past the descriptor copy, and the `0x0032E742` alternate path, are
**unread**.

### `DG-1`, `DG-4` and `DG-5` answered — 2026-09-11: the file is `musicctrl.bin`, and the fifth function touches it

The four functions read above do not touch a file because **the fifth does**: `0032E620` queues the
read, and the request pump issues it against the archive. The chain, complete:

```
0022A0B0 (boot fixer) -> 00379D20 -> jmp 003EAB60 -> 0051ED10(9, 0x20, 003EAB90)
    0032E400(9, 0x20)   the .fst size of  ps2data/image/ff12/in/common/musicctrl.bin  (path array 01EBF740 entry 32)
    0036A190(size)      a block on heap 5, returned at once and stored at 02B5E0D0
    0032E620(...)       the request; on delivery 0032E330 calls 0051EDB0, which jumps to 003EAB90
003EAB90                page words += (u32)block  -> the absolute 32-bit page addresses the reader dereferences
```

`003EAB60` had "no direct call sites" because `00379D20` reaches it with a **tail jump**. The
"read layer" `003EB0D0` gates in `0032E620` is the script BGM stream's active flag, and the
`0x28`-byte descriptor copy is the **chunked** path taken only while such a stream is active — never
in the shipped build. The extracted file walked page by page has **291 runs**, not the 316 EXP-008
counted from a walk without page bounds. All of it, with the file's census and the stream's verbs and
machine, is on [the music-control page](the-music-control-file-and-the-bgm-stream.md).
### `DG-2` answered — 2026-09-11: a track id names `musicNNN.win.mab`, and the flag table is `musicinfo.bin`

**What a track id selects.** The id the ladder returns is the key of the **four-slot track table**
at `022CB9F0` and the number in the music bank's file name:

```
musicplay / musicread (verbs 022B / 0229)          the transition handler 00261F90
   -> AudioTrack_FindSlot 00360C20 (key == id)        -> 003614C0(id, 0x78, 1)
   -> AudioTrack_FindOrReserveSlot 00361630(id)       state 3, key = id, +0x14 = 002DEC70(id), state 4
        -> 002DEC70 -> 001DBB80 -> AudioRegistry_Get 00210B30 -> 00210980 (Music controller, manager +0)
             -> 00218B70(controller, id): a bank object whose +0x50 == id, else vtable +0x30 allocates one
                  -> 00222740(bank, id, …): +0x50 = id, sprintf(buf, "%s%03d%s", *(char **)01E027D8, id, ".win.mab")
                        = PS2Data/sound/music/magi_data/win/music<id>.win.mab   (prefix at 009088E0)
```

So **track 61 is `music061.win.mab`**, and there is no indirection: `musicctrl.bin`'s 69 non-zero
track values all have a file in the archive (116 `music*.win.mab` files: 7, 15–92, 94–116, 200–213),
and the two override ids `0x5A` / `0x5B` are `music090` / `music091`. The PS2-era kind-31 path array
`music000.bgm`–`music255.bgm` (`01E46400`, 256 entries) is dead in this build: its size table has
no entry, so the request issuer refuses it, and the Music controller never asks for it.

**The "per-track flag table" is a file, and its bit means the opposite of what §3 first said.**
`00360C70` (from the boot initialiser `00266D10`) sizes `0032E400(9, 6)` — kind 9 index 6 is
`PS2Data\image\ff12\in\common\musicinfo.bin` — allocates the block on heap 5 and queues it through
`0032E620` with `00360B40` as the done callback, which stores the delivered block at `022CBA50`
(`00360B42`). The file is 512 bytes: **256 records of `{u8 flags, u8 track}`**. `00361010(id)`
returns `flags & 1`, and the transition handler uses a set bit to **skip both runtime-mode
overrides** (`00262046` `jne 00262068`); a clear bit lets `mode == 1` substitute `0x5B` and
`mode == 2` substitute `0x5A`, and otherwise the mapped track still plays. Eighteen tracks carry the
bit (10, 11, 33, 36, 51, 69, 70, 71, 95, 96, 97, 101, 102, 113, 205, 206, 207, 213); the two
override tracks themselves do not. The flags byte takes the values 0, 1, 2, 3, 4, 6, 7 and 0x80, and
the second byte repeats the index except on eight records — neither the other bits nor the second
byte has a reader anywhere in the image (`00361010` is the only reader of the pointer; the control is
that the same scan finds it).

**For a modder:** the bank a track plays is `music<id>.win.mab`; to give an area a new piece, add a
file under a free id and name that id in `musicctrl.bin`; to stop the UI or combat mode from
replacing an area's music with track 91 / 90, set bit 0 of its `musicinfo.bin` record.

The chain above through `00222740` and the manager layout is [the bank-family
page](Audio-Bank-And-Controller-Family/audio-bank-and-controller-family.md)'s; the slot table is
[the sound-request page](Audio-Boundary/how-a-sound-request-becomes-a-voice.md)'s.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL.*

- **Party and Gameplay — CLIENT and SERVICE.** The two mode tests this page cites, `00303EC0` and `003135C0`, wrap
  `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` and are also asked by
  `PartyControl_RecomputeSuppressionFromLeaderBattleState`. **Party-control suppression and area music read the same
  battle-mode test.** `003135C0` is also read by `PartyFollow_SolveFormation` and a 668-byte body (**Movement**), and
  `00303EC0` by `InputGameplay_ArbitrateDigitalInputAndModalS…` (**Input**).
- **Input and PlatformOnlineAchievements — CLIENT.** `FieldData_GetVariable0` is read by input arbitration and by two
  achievement-side bodies.
- **Initialisers — SERVICE.**
  - The boot initialiser `0022A0B0` calls the 119-byte **Input** initialiser and the **Presentation** loaders
    `AddMotion_LoadSkeletonMapping` / `AddMotion_LoadHighModelReplace`.
  - The area initialiser `00266D10` calls the unread 1,936-byte **Input** body, three **Movement** helpers,
    `CameraSystem_InitializeRecords` and a 271-byte Presentation body.
- **Presentation — MECHANICAL.** The arena entry `0036A190` has 17 Presentation callers. The file-request family (`0032E400` size probe, `0032E620` request, `0032E520`, `0032E4D0`, `0032E070`) is shared: its **Presentation** callers (119 B and 337 B bodies), the **Input**-filed item-graphics loader (177 B) and script-verb bodies are CLIENTS, not audio dependencies.
- **Items_Equipment_Shops_License and Movement — MECHANICAL.** The owner lookup `0031B860` is shared with the equipment
  and licence setters and two locomotion bodies.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — CLIENT.** The music table's boot chain is core-driven. The start-up subtree's root calls the music loader's entry and the actor-system initialiser, and a file-request helper is called by the two boot-mode bodies (255 and 219 bytes). `FieldData_GetVariable0` is called by a 2,232-byte core body.
- **Status_Periodic_Terminal — CLIENT.** `BattleStats_FindOwningBattleUnit` is also called by five status bodies, including `BattleStats_RecomputeDerivedStateAndAutoStatuses`, `BattleStats_ChangeStatusAndProcessSideEffects` and `BattleUnit_ResolvePeriodicPrimaryResourceRecoveryStep`. It is a shared unit lookup, not a music function.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAction — CLIENT.** `BattleAction_EvaluateTargetPreviews`, owned by that layer, calls `0031B860` on this page. That caller is the preview sweep over `byte[+0x6B6]`, in a `0x198`-byte frame with a stack cookie; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatFormula — CLIENT (35 edges, one fan-in).** All 35 edges are CombatFormula bodies calling `0031B860` on this page: the reverse lookup from a stats record to its owning battle unit that this page documents. `BattleFormula_RollGuardParryMode` is the worked example - it needs the owning unit before it can test bit 23 of its `dword[+0]`. The crossing is **one shared primitive with 35 callers**, not 35 separate relationships, and naming a single body would say less than the count does. Edge count from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**RNG_Random_Selection — SERVICE.** `0022A0B0` on this page calls `RNG_MT19937_Seed`, owned by that layer. What it reaches is a five-byte thunk - `jmp 00863D30` - onto the CRT's Mersenne Twister seed; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Rewards_Progression_Economy — CLIENT.** `Reward_ComputeExperienceForRecipient`, owned by that layer, calls `003135C0` on this page. That caller is the experience computation for one recipient: it needs `byte[rec+5] == 0` and takes its context from `0031B860`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).


### Interior citation — frontier hub `00361010` (2026-09-18, SWE2-EC7)

`00361010` — 30 B, 5 callers: the pointer's only reader, as named above —
`ecx >= 0` and ~~`[022DBA50]`~~ `[022CBA50]` *(typo corrected 2026-10-01, OPUS; `00361014`)* live, then `movzx eax, byte[rdx + rcx*2] & 1` at
[`00361023`](../_index/ADDRESS-INDEX.md); every other case returns 0. The
per-area flag bit the music switch tests.

## SWE2-EC7-25 update (2026-09-18) — `0032E4D0` handle-validity predicate

`0032E4D0` (66 B) answers "is `ecx` a live handle": `-1` and `0` fail
(`0` also pings `0016D6A0`), otherwise the `(ecx & 0x3F) << 7` slot in
`022C31C0` must echo `ecx` at `+0x64` with `byte[+0x20]` non-zero —
the generation-and-occupied test the music-request callers run before
trusting an id. Interior anchor `0032E4ED` (the `+0x64` compare).

## SWE2-EC7-42 update (2026-09-19) - `003614E0`

`003614E0` (309 B) is a music-change body - `022CBA58`/`022CBA60`, `002DEC00`/`00360D70`/`002F16B0` pair/`003601B0`. Interior anchor `003614FF` (a `002DEC00` call).

## SWE2-EC7-43 update (2026-09-19) - `002F1780`

`002F1780` (286 B) is a music-area-change body - `022BDED0`/`022BE7C0` slot-table walk (0x48 stride, `rol ebp` bitmask rotate), two `call rax` vcalls on `[rbx-0x10]` objects. Interior anchor `002F1814` (the first `call rax`).
