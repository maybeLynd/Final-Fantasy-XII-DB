---
system: Five small .bin tables - footstep sounds, vibration, button prompts, window sizes, a version stamp
category: 02-Resource-And-Asset-Pipeline
status: DOCUMENTED — UQ-68 answered 2026-09-27 (entry 4 is window kind 5, the Foecraft command's list, which no shipped command list offers; the two numbers read 2026-09-18 as width and rows); UQ-69 answered 2026-09-18 (the key-signal requester and readers found, sections and mask read); UQ-66 and UQ-67 answered 2026-09-17 with the readers found
owner_layer: archive format sheets
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: each file extracted whole from FFXII_TZA.vbf and decoded byte by byte; every offset and
    count cross-checked against the file size, which is the control
last_reviewed: 2026-09-13
archive_formats:
  - "qstd | explained | menuquest.dat (.dat member): {qstd, u32 100, u16 3, u16 count, {u32 textId, u32 payload}[count]} (12 + 66*8 = 540) - (kind 7, 296) request, rows read by the hunt-list owner 0037F4D0 / 0037EDB0 / 0037E8D0, section 12"
  - "QST1 | explained | questbase.bin (.bin member): {QST1, u32 count, u32 entries[count]} (8 + 173*4 = 700) - (kind 9, 0x21) by 0051ED10 into 02CA6C60, read by 00473B90 / 00473C90, section 13"
  - "sign | explained | key_signal_data.bin (.bin member): signe header with three u16 section offsets, sections 0-2 - (kind 7, 0x24) by 0029DC90, read by 0029DA70 / 0029DBE0, sections 6 and UQ-69"
  - "bwin | explained | menubtlwndinfo.bin (.bin member): {bwind, u32 15, {u16 minWidth, u16 rows}[15]} (72 B) - (kind 7, 0x25) by 0035C5B0 into 022CA460, read by 0035C3F0 for 0027DED0, sections 5 and UQ-68"
  - "VIB0 | explained | eventvib.bin (.bin member): {VIB0, u32 count, u32 offsets[count], keyframe-pair records} - (kind 9, 7) by 00379E90, bound by 0035B3E0, evaluated by 0035AF20, sections 4 and UQ-67"
  - "FOOT | explained | soundfoottable.bin (.bin member): {FOOT01, u32 32, pad, u8 setA[32], u8 setB[32]} (80 B) - (kind 9, 9) by 00378540, blob at 02ADD0C0, read by the footstep chooser 002E9D90, sections 2 and UQ-66"
  - "summoneffectdata | explained | summoneffectdata.bin (.bin member; dP<d is record 0's data): 64 x {u8 scaleA[3], u8 scaleB[3] (x 0.01), u8 colour[4]} + 32-byte tail (672 B) - (kind 9, 0x2A) by 003B53C0 straight into .data 02AD9B60, read at 0036FA09-0036FC7B, section 14"
  - "MENU | explained | menu_version.bin (.bin member): the 16-byte ASCII string MENUVER200509150, no structure - kind-7 path index 0x90, no requester found by a whole-image sweep with positive controls and no version compare in the image, section 3"
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_kind: derivation
  last_pass_state: opus-five-bin-1 - the page IS the measurement. Five signatures that no page
    mentioned, decoded from their own bytes. The structural control throughout is that the declared
    counts and offsets must reproduce the file size exactly, and in every case they do - `signe`
    chains three sections end to end at 0xEC and 0x150, `bwind` lands on 72 exactly.
  crossref_clean: false
  reopened_count: 0
---

# Five small `.bin` tables

> The `.bin` signature census found **eleven magics no page mentioned**. Going one level deeper
> found pages for six of them under their *filenames*. **These five had nothing**, and they are
> small enough to decode completely.
>
> **§12 adds the two `.dat` magics** - `hchk` and `qstd` - which had nothing either. **The file
> name stays `five-small-bin-tables` so links and history hold**; the scope is seven formats.

## 1. The control used throughout

Every one of these files declares counts and offsets. **The control is that they must reproduce the
file size exactly** - if a record size is guessed wrong, the arithmetic lands somewhere other than
the end of the file. In all five cases it lands exactly.

## 2. `FOOT` - `soundfoottable.bin`, 80 bytes

```
+0x00  char[8]  "FOOT01\0\0"          tag and version
+0x08  u32      32                     entry count
+0x0C  u32      0                      pad
+0x10  u8[32]   surface -> sound, set A
+0x30  u8[32]   surface -> sound, set B
```

`8 + 4 + 4 + 32 + 32 = 80` exactly.

**Set A is the identity, `0..31`.** Set B remaps ten entries to `32..41`, leaves `10,11,12`
untouched, remaps `13,14` to `42,43`, and leaves `15..31` untouched.

> So there are **two footstep sound sets over 32 surfaces**, and set B differs from set A on
> **twelve** of them. The identity in set A is the tell: this is a remap table, and the default is
> "the surface index *is* the sound index".

**Not claimed:** which sets these are (shoe type, weather, character), and what a surface index
means. Nothing here names them.

## 3. `MENU` - `menu_version.bin`, 16 bytes

```
"MENUVER" "200509150"
```

Seven characters of tag, nine of payload, no terminator, no structure. The payload reads as the
date **2005-09-15** plus one more digit. **A build stamp for the menu data set**, and there is
nothing else in the file.

> Worth its own line because a format census counts it as a format. It is one string, it ships in
> nine locales, and a reconstruction needs to produce it only if something reads it - **which is not
> established here.**

*2026-09-29 (SWE2-DATA, `OPUS-REQ-DATA-BUCKET-MEMBER-FORMATS`): **nothing requests it that a static
sweep can see.*** Its path is kind 7 index `0x90` (indices `0x8F` and `0x91` are empty). No call site
passes the constant pair `(7, 0x90)`, directly or through the menu-set wrappers (controls
`0037870A`, `003EAB73`, `00561663` found); no id register is loaded with `0x90` before a request call
(control: the loop form at `00291CF3`); no stored `(7, 0x90)` pair exists in code or data; the 9,351
prefetch lists never name it; and neither the string `200509150` nor that integer occurs in the
image, so nothing compares a menu version. A kind/id computed at run time at one of the 89
register-held request sites is outside what the sweep can see. Check:
[`b8_menu_version.py`](../../_index/candidates/bucket-members-0929/checks/b8_menu_version.py) (18
checks, FAILS 0; the two copies checked are byte-identical).

## 4. `VIB0` - `eventvib.bin`, 176 bytes

```
+0x00  char[4]  "VIB0"
+0x04  u32      11                     pattern count
+0x08  u32[11]  offsets: 0x34, 0x3E, 0x48 ... 0x98
```

The header is `4 + 4 + 11*4 = 52 = 0x34`, **which is exactly the first offset** - so the records
begin immediately after the table, and the spacing gives a **10-byte record**.

A record, at `0x34`:

```
02 00   01 00   0F   78 00   78 00   01
u16=2   u16=1   u8   u16     u16     u8
```

Across the eleven records the two `u16` fields take `0x78`, `0xA0`, `0xE6`, `0xFF`, `0x8C`, `0xB4`
and are usually **equal to each other**, and the `u8` before them takes `0x0F`, `0x23`, `0x05`.

> **The reading that fits:** two motor intensities (0-255, usually matched) and a duration or
> pattern id. That is what a vibration table looks like and the value ranges support it - **but no
> reader has been found, so the field names are a reading and not a derivation.**
>
> **Superseded 2026-09-17 (FABLE, UQ-67):** the reader is found and the record is `{u16 track2Start, u16, {u8 duration, u8 intensity}[]}`; the `u16` values above are intensity bytes preceded by a zero duration.

**Not claimed:** the last **14 bytes** of the file, after the eleventh record ends at `0xA2`.

## 5. `bwin` - `menubtlwndinfo.bin`, 72 bytes

```
+0x00  char[8]  "bwind\0\0\0"
+0x08  u32      15                     entry count
+0x0C  {u16,u16}[15]
```

`8 + 4 + 15*4 = 72` exactly.

**Fourteen of the fifteen entries are `(10, 8)`. Entry 4 is `(150, 8)`.**

> A fifteen-row table where one row differs is more useful than a uniform one: **whatever entry 4
> is, it is the one battle window with a different first dimension**, and 150-vs-10 is a large
> enough ratio that the field is a size or a count rather than a flag.

**Not claimed:** which window each row is, and what the two numbers measure.

## 6. `sign` - `key_signal_data.bin`, 532 bytes

The richest of the five, and the one whose structure proves itself.

```
+0x00  char[8]  "signe\0\0\0"
+0x08  u16      0x0010     -> section 0
+0x0A  u16      0x00EC     -> section 1
+0x0C  u16      0x0150     -> section 2
+0x0E  u16      0xCCCC     see below
```

Each section is `u32 count` followed by its records:

| section | at | count | record | ends |
|---|---|---:|---|---|
| 0 | `0x010` | 27 | `{u32 textId, u32 buttonMask}` | **`0xEC`** |
| 1 | `0x0EC` | 24 | ~~`{u16, u16}`~~ `{u24 labelTextId, u8 buttonIndex}` *(corrected 2026-10-02, OPUS: `0029DA70+0xAA` takes byte 3 as the index and `0029DA70+0x100` masks the dword `0xFFFFFF`, the answer below)* | **`0x150`** |
| 2 | `0x150` | 19 | ~~`{u16, u16}`~~ `u16[19]` offsets over 8-byte scene records *(corrected 2026-10-02, OPUS: offsets `0x2C` … `0xBC` in the shipped `key_signal_data.bin`, the answer below)* | ~~`0x1A0`~~ `0x214`, the file end |

**Sections 0 and 1 end exactly where the next one begins.** That is not an assumption that happened
to work - `0x10 + 4 + 27*8 = 0xEC` and `0xEC + 4 + 24*4 = 0x150`, both to the byte, which
simultaneously confirms the record widths and the offset table.

**Section 0 is a text id paired with a button mask.** The ids run `0x0002BF4D`..`0x0002BF63`
contiguously; the masks are `0x10, 0x40, 0x80, 0x20, 0x1000, 0x8000, 0x2000, 0x4000, 0x400, 0x100,
0x02, 0x08, 0x200, 0x04, 0x01, 0xA000, 0x300, 0x0C` - **single bits and small combinations**, which
is what a controller button mask looks like. Two entries have mask `0`.

Section 2's pairs are an arithmetic run: `(0x2C,0x34), (0x3C,0x44), (0x4C,0x54)` - **both members
step by 0x10, held 8 apart.**

### ⚠ Two authoring artefacts are shipped in the file

`0xCCCC` at `+0x0E` and `0xCDCD` in the tail are **MSVC's uninitialised-memory fills** - `0xCC` for
stack, `0xCD` for heap. They are not data.

> **This is evidence about the tool, not the format.** The file was written from a struct that was
> not fully initialised, in a debug build, and the padding went to disk. A reconstruction must
> **write something** in those bytes and **must not read them** - and anyone deriving a field from
> `0xCCCC` is deriving a field from the compiler.

**Not claimed:** what sections 1 and 2 hold, what the text ids resolve to, and whether the mask is
XInput, DirectInput or an internal encoding. **No reader has been located for any of the five
files** - this page is the format, not the loader. *(2026-09-17: readers found for `FOOT` and `VIB0`, see UQ-66 and UQ-67; the kind-7 pair remain unread.)* *(2026-09-18: the kind-7 pair's requesters and readers are found too, through the menu-set wrapper `00249210`; see UQ-68 and UQ-69.)*

## 7. What is not known

- [x] ~~The loader for any of these five.~~ **ANSWERED 2026-09-13, §10** - all five are ordinary
      `(kind, id)` resource requests through the documented request path, and every `.fst` size
      matches the extracted file byte for byte. **There is no per-format loader.**
- [x] ~~**UQ-66.** `FOOT`: what distinguishes set A from set B, and what a surface index means.~~
      ***ANSWERED 2026-09-17 (FABLE): the reader is the footstep chooser `002E9D90`; set B is the set the field-environment variant selects, and a surface index is the actor's contact-surface word.** `soundfoottable.bin` is requested as kind 9 id 9 by the map-table requester `WorldAreaField_RequestAuthoredMapTables` (`00378540`, `003788D2`) with the completion `00378F80`, which stores the blob at `02ADD0C0`; the getter `00377C10` returns it and has one caller. There the index is `set + surface`: `set` is the header count (`u16 +8`, 32) when the caller's flag (`r9d`) and the field-environment variant word [`02099DBC`](../../03-World-Area-Field/Weather/weather-slot-state-model.md) are both non-zero, else 0 (`002E9EFC`..`002E9F0E`); `surface` is the signed word `+0x8A` of the actor's sub-object at `[actor+0x138]` (`002E9F29`). The byte at `+0x10 + index` (`002E9F35`) is the bank-local sound, the variant word is added to it again when the flag is set (`002E9FA7`), and `003A1240(bank, index)` turns it into `bankSlot * 512 + index`. So set A is the base set and set B the variant's set, the variant value shifting the sound index as well; a surface index is the value the actor's contact record reports at `+0x8A`, 0..31. Static, bodies read.*
- [x] ~~**UQ-67.** `VIB0`: the 14 trailing bytes, and confirmation that the two `u16`s are motor intensities.~~
      ***ANSWERED 2026-09-17 (FABLE), correcting the record reading: a pattern is two keyframe tracks of {u8 duration, u8 intensity} pairs, not two u16 intensities, and the tail is an unaddressed duplicate.** `eventvib.bin` is requested as kind 9 id 7 by `00379E90` (`00379EFE`) with completion `00379F30`, which hands the blob to `0035B3E0`: it rewrites each of the `count` offsets into a resolved handle through `0020E600`/`0020E620` and publishes the table at `02EC0B68`. A pattern starts through `0035B650(index, flag)`: `0035B2F0` takes one of eight 32-byte slots at `02EC0B80`, storing the record pointer at `+8`, a scale of 1.0 at `+0x10`, the record's `u16 +0` at `+0x16` and the motor selector at `+0x1A`. The evaluator `0035AF20` walks the slots each tick: for the current pair `k` it reads `duration = u8[rec + 4 + 2k]`, `start = u8[rec + 5 + 2k]`, `end = u8[rec + 7 + 2k]` and keeps the largest `start + (end - start) * elapsed / duration`, scaled by `+0x10`, as the motor value at `02EC0B50 + motor * 8` (`0035B013`..`0035B070`); `elapsed` (slot `+0x18`) counts up to `duration`, then the pair index at `+0x14` advances; a second cursor starting at the record's `u16 +0` (`+0x16`) drives the second track (`0035B09B`). So `02 00 01 00 0F 78 00 78 00 01` reads: track 2 begins at pair 2, `u16 +2` (1) is not read in the pass shown, and the pairs are (15, `0x78`), (0, `0x78`), (0, `0x01`); the values the page read as `u16` are intensity bytes preceded by a zero duration. The 14 trailing bytes are `00 AE 00 00` followed by a byte-for-byte copy of the eleventh record; no offset addresses them and the walk stops at `count`, so they are never read. `0035AE30` hands the two motor values to the pad through `0035FED0`. Static, bodies and the extracted file read.*
- [x] **UQ-68.** `bwin`: what entry 4 is, and what the two numbers measure.
      ***NARROWED 2026-09-17 (FABLE): the reader is not locatable by the three methods that found FOOT and VIB0.** No request site passes kind 7 with id 37 as a constant (a forward constant pass over all 124 request sites), no data-section list holding 36 and 37 adjacently is referenced by code, and no code references the file name. The kind-7 requests that exist go through `00365810` over a 12-entry id table at `00D10C98` (ids 130..135, 218..223) and `002C8EE0` over a range from `0x74`, neither of which includes 36 or 37. Entry 4's meaning waits on that reader.*
      ***Two further methods 2026-09-17 (FABLE), both negative.** First, every rip-relative operand in `.text` was censused (166,213 targets) and the data sections were scanned for kind and id together, as u32, u16 and u8 pairs (7, 36) and (7, 37), and for u32 36 and 37 inside one 64-byte window: 60 hits, five of them referenced by code, none a request record. They are a five-to-nine-bit code-length reversal table at `01CDABA0` (its pairs run 0, 64, 32, 96 and so on against 7), an achievements triple list at `009062C8`, a character map at `01DF09D0` and two input-binding blocks at `01F461E0` and `01F46E60`. Second, the kind-7 array itself is referenced by code at one address only, its base from the resource builder `002DF9A0`, whose single caller is `0022A0B0`; no reader takes entry 36 or 37 by a constant offset, and that caller carries no immediate in 0x20..0x40 that could bound a loop over the two ids. What is left is a request whose id is computed, or read from authored data these scans do not decode.*
      ***Named 2026-09-18 (FABLE), from the size table:** kind 7 id 37 is `ps2data/image/ff12/myoshiok/us/bin_menu/menubtlwndinfo.bin` (72 bytes): `FileSizeTable_US.fst` is `u32[41][5000]` by kind and id, its row 7 entry 37 is 72, and exactly one file under the menu root has that size. So `bwin` is *menu battle window info*, a seventy-two-byte table of the battle window, which is what its consumer's name will have to match; the reader is still not located.*
      **Narrowed 2026-09-18 (FABLE): the requester and the reader are found, and the two numbers are read.* The request is `0035C5B0`, which asks `(7, 0x25)` through the menu-set request thunk `00249180` → `00249210` (`0035C5D7`) and stores the returned buffer pointer at `022CA460` (the sibling page [loader-bound-bin-families](loader-bound-bin-families.md) already had this pairing with `mini_guest_face`, `(7, 0x0D)` into `022CA470`); the earlier constant passes missed it because the kind travels in `edx` and the id in `r8d` through two wrappers, not in `ecx` / `edx` at `0032E620`. The reader is `0035C3F0(out, index)`: `out.a = max(entry.a, word[022CA408 + index × 2])`, `out.b = entry.b`. Its only caller `0027BDE0(kind, &a)` picks the entry from the battle-window **kind** through an 18-way table (`0027BE88`): kinds 2–7 → entries 1–6, kind 8 → entry 0, kinds 9–15 → entries 7–13, kinds 16–19 → entry 14. Its only caller in turn, `0027DED0(window, kind)` from `BattleMenu_UpdateCommandSelectionAndDispatch` (`00278BA6`, kind = the menu's word `+0xD8`), writes `a` as the window's **width** (the `+0x1510` object's word `+0xEA`, widened by `01E0C364 − 01E0C354` for kinds 10–14 in mode 4) and `b` as its **row count** (`min(b, +0x500)` into `+0x1528`, multiplied by the row-height word `+0x100` into `+0x9E`). The override words at `022CA408` are the measured text widths of the current language, rebuilt by `00273E30` (2,382 B; the string measurers `0035D330` / `002B58B0` over `002F9860` text) whenever the battle-action presentation toggles bit 0 of `[02EBF190]+0x5B04` (`00306760`, `00313550`, `00313840`, `00254A90`). So **the two numbers are the window's authored minimum width and its row count**, and **entry 4 is the kind-5 battle window**, the only one authored 150 wide by 8 rows; entries 5–14 (`(10, 8)`) are the default. Not established: the kind enumeration's names, so which on-screen window kind 5 is stays open. Static: the request chain, the three bodies, the jump table.*
      ***ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5), static: window kind 5 is the list of battle command 7, Foecraft, and no command list the PC build ships offers command 7.** The window-kind switch `0027E050` indexes its table by kind − 1 (`0027E06B`); kind 5 stores list code `0xB` and sub-selector 7, which the list builder `0031EB20` validates as a class-21 id, a battle command (`0031ED5E`–`0031ED73`). The next-kind function `0027C3D0` gives kind 5 for command 7 only (`0027C532`), and commands 3, 5 and 6 (Items, Summon, Quickening) open kinds 4, 6 and 7, whose sub-selectors are the same commands. The dispatch `002778C0` sends the new kind to itself as message 31, whose arm holds the one store to `+0xD8` (`002791AC`), the word `0027DED0` sizes the window from. But the command lists `0027C3D0` reads are static tables: the top list (`00D10650` / `00D10660`) is Attack, Magicks & Technicks, Mist, Dismiss, Gambits, Items, and the Mist list (`00D1065C`) is Summon, Quickening. So entry 4's `(150, 8)` sizes a window the shipped menus do not open. *Corrects the 2026-09-26 narrowing in the register:* the kind is message 31's payload, not message 1's, and the controller's `+0x61BA` feeds `+0xDC`. [Record and control](../../_index/candidates/uq68-kind5-foecraft/README.md) (9 checks, FAILS 0; bounded by the sender and row-writer censuses there).*
- [x] **UQ-69.** `sign`: sections 1 and 2, and the button-mask encoding.
      ***NARROWED 2026-09-17 (FABLE): as for `bwin`, no requester or reader of kind 7 id 36 is locatable statically** (constant pass over the request sites, adjacency scan of the data sections, name references), so sections 1 and 2 and the mask encoding wait on the menu set's table-driven loader being read.*
      ***As for `bwin`, two further methods 2026-09-17 (FABLE), both negative** (the kind/id record scan with a rip-target census, and constant-entry references into the kind-7 array, which has one code reference, its base from `002DF9A0`); the hits are listed under UQ-68.*
      ***ANSWERED 2026-09-18 (FABLE) — the file is the button legend (the key-signal strip), and all three parts read from its reader.** The request is `0029DC90`: when the pointer `0209C4A0` is still null it asks `(7, 0x24)` through `00249180` → `00249210` (`0029DCBF`) with the completion handler `0029DCD0`, which stores the buffer pointer there. The readers follow the header's three section offsets (`+8`, `+0xA`, `+0xC`). **Section 0** (27 records `{u32 nameTextId, u32 buttonMask}`) is the button table. **Section 1** (24 records) is `{u24 labelTextId, u8 buttonIndex}`, not two `u16`: `0029DA70` takes the record's dword, masks `0xFFFFFF` for the text and takes byte 3 as the index into section 0 (`0029DB1A`, `0029DB6C`–`0029DB70`); the file's values are labels `0xC5A8`… with indices 4–24. **Section 2** (19 records) is a `u16[19]` offset table (`0x2C, 0x34, … 0xBC`, relative to the section) over 8-byte scene records `{u8 sceneId 1–19, u8 a, u8 b, u8 count, {u8 signalIndex, u8 flag}[count]}`; with one pair the second slot is the `0xCDCD` fill the page already flagged, and `0x17C + 19 × 8 = 0x214` is the file's end to the byte. `0029DA70(out, sceneId)` finds the scene by its first byte (`0029DAA0`–`0029DABA`), copies `a`, `b`, `count` to `out[0..2]`, and for each pair fills a 0x18-byte slot: the button's name string and the signal's label string, both through the high-pool text resolver `002F9920` (group = id ÷ 10,000), a word flag `(~(flag << 2)) & 4` and the signal index. `0029E330(sceneId)` builds that legend and `0029DDF0` copies it into the HUD object `[0209C498]+0x158` at `+0xD0` only when it differs; its callers are the menus (`00295D20`, `0029E110`, `002B7B80`, `002BAF80`, `002D5EB0`, `005789D0`). **The mask encoding is the engine's own input-snapshot button word**: `0029DBE0(key)` returns section 0's mask for a key below `0x100`, or for `0x100 + n` the mask of signal n's button, with keys `0x16`, `0x17` and `0x1A` diverted to the runtime words `01E0C2A0` / `01E0C2A4` (`0029DC22`–`0029DC59`; *corrected the same day, FABLE: `0x1A`, not `0x19` — the chain is `sub eax, 0x16`, `sub eax, 1`, `cmp eax, 3`*); every caller tests the result directly against a word of the gameplay input snapshot `02F97360` (`+0x0A` at `0055C810`, `+0x0C` at `002D6237`, `+0x32` at `002BBA5F`), the snapshot [the input stack](../../15-Input/Input-Stack/input-stack-device-channel-and-bindings.md) describes, so it is neither XInput nor DirectInput. Not read: what `a` and `b` of a scene record mean (only scenes 6–9 carry `a = 2`), and the text rows themselves. Static: the request chain and the four bodies; DATA: the `us` file decoded under the reader's layout, which reproduces the offsets and the size exactly.*

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| every layout above | each file extracted whole from the archive and decoded byte by byte | 1 |
| the record widths | the declared counts and offsets reproduce the file size **exactly** in all five cases | 1 |
| `signe` has three chained sections | `0x10 + 4 + 27*8 = 0xEC` and `0xEC + 4 + 24*4 = 0x150`, both to the byte | 1 |
| `0xCCCC` / `0xCDCD` are uninitialised fills | the MSVC debug fill constants, in padding positions | 2 |
| the `VIB0` and `sign` field *meanings* | value ranges only - **a reading, not a derivation** | 5 |

## 10. How each file is requested - `(kind, id)`, settled

*(2026-09-13. Static only. The hunt failed three times first; §10b keeps that record.)*

**All five are ordinary resource requests.** They are reached by `(kind, id)` through the request
path [the `.fst` sheet](../Loose-Files-And-Size-Tables/file-size-tables-fst.md) already documents -
`0032E400` sizes the request, `0032E620` records it, `0032E870` takes a slot. **There is no
per-format loader to find, because there is no per-format loader.**

| file | tag | kind | id | `.fst` size | extracted size |
|---|---|---:|---:|---:|---:|
| `key_signal_data.bin` | `sign` | **7** | **36** | 532 | **532** |
| `menubtlwndinfo.bin` | `bwin` | **7** | **37** | 72 | **72** |
| `menu_version.bin` | `MENU` | **7** | **144** | 16 | **16** |
| `eventvib.bin` | `VIB0` | **9** | **7** | 176 | **176** |
| `soundfoottable.bin` | `FOOT` | **9** | **9** | 80 | **80** |

**Every size matches the byte count of the file extracted from the archive.**

### How it was settled, and why the check is strong

The `.fst` is `u32[41][5000]`. **Inverting it** - searching for the five sizes rather than looking
them up - gives a joint constraint:

- `532` and `72` occur together in **exactly one kind: 7**, at **adjacent ids 36 and 37**.
- `80` and `176` occur together in **exactly one kind: 9**, at ids **9 and 7**.

The independent `.rdata` walk had put `sign`/`bwin` one apart and `FOOT`/`VIB0` two apart. **Two
unrelated instruments agreeing on the spacing** is what makes this more than a coincidence of
sizes, and subtracting `id * 8` from the known slot addresses recovers the array bases the earlier
walks got wrong: **kind 7 at `01E0E530`, kind 9 at `01E0E3B0`.**

Read back at those bases, the arrays are coherent lists - kind 7 is the menu `Bin_Menu` set (538
sized ids), kind 9 the common/global tables (26).

> **The corroboration that settles it is not one of my files.** Kind 9 id 8 is `navimapdata.bin`
> with `.fst` size **3470** - and the field-record-table page **independently derived that same
> 3470** from the file's own geometry, `8 + 3 * 1154`, two days earlier and by a different route.
> A base recovered from my arithmetic landing on somebody else's independently-derived number is a
> check I did not construct.

### Kind 9 is where four more of the worklist live

Reading the kind-9 array out gives, among 26 entries: `map_ref.bin` (id 4, the `MRF.` signature),
`eventvib.bin` (7), `navimapdata.bin` (8, `NAV.`), `soundfoottable.bin` (9),
`mapjumpgroupflagrom.bin` (10, `FLAG`), `charseinfo_*.bin` (12+, `CHSE`).

**So kind 9 is the common/global table set**, and it holds four of the signatures the `.bin` census
listed separately. A reader wanting any of them now has one index rather than a filename.

## 10b. The three instruments that failed first

Kept because the failures were caught by controls and the route that worked was not the route I
predicted.

| attempt | why it failed | the tell |
|---|---|---|
| walk **backwards** from a path slot to find the array start | the arrays are **adjacent in `.rdata`**, so the walk crosses the boundary | none of its three "bases" is among the 35 the installer stores |
| pair each **`lea`** of a source array with the next store | the installer `lea`s **every language's** candidate and stores one | it invented ten "kinds" sharing one slot - more kinds than slots |
| walk **forwards** from each base until a non-pointer | terminates early on nulls | it found **none** of the five |

I recorded that the next attempt should *"read the installer's store loop to recover each array's
length"*. **That is not how it was solved.** Inverting the size table needed no disassembly at all,
and the array bases fell out of the answer rather than being required to reach it.

> **The resume condition I wrote was a worse plan than the one available.** Worth keeping visible:
> a stated next step is a hypothesis about the cheapest route, and it can be wrong in the same way
> any other hypothesis can.

## 12. And the two `.dat` magics - `hchk` and `qstd`

The `.dat` census found four magics: `himg` (309 units), `hdat` (17), `hchk` (6) and `qstd` (1).
The first two are mentioned by two pages each. **These two had nothing.**

### `hchk` - `menuhandbook_knowledge.dat`, 812 bytes

```
+0x00  char[4]  "hchk"
+0x04  u32      0x67 = 103
+0x08  u16      100          <- record count
+0x0A  u16      18
+0x0C  {8 bytes}[100]
```

`12 + 100 * 8 = 812` exactly, and the `100` is the field at `+0x08`.

**The table ships essentially empty.** Every record is `FF FF FF xx FF FF FF FF`, with `xx` = `00`
in the first record and `0x80` in all the rest.

> A 100-entry table whose every entry is `0xFF` is worth recording *as* that. Whatever "knowledge"
> the handbook tracks, **the shipped file grants none of it** - it is the zeroed initial state, and
> a reconstruction that invents content here invents progress the player has not made. The one
> byte that varies, `00` vs `0x80`, is the only structure the file has.

### `qstd` - `menuquest.dat`, 540 bytes

```
+0x00  char[4]  "qstd"
+0x04  u32      0x64 = 100
+0x08  u16      3
+0x0A  u16      66           <- record count
+0x0C  {u32 textId, u32 payload}[66]
```

`12 + 66 * 8 = 540` exactly, and the `66` is the field at `+0x0A`.

**The first word is a text id and the ids run contiguously** - `0x00033450`, `0x00033451`,
`0x00033452`, … after an initial `0x00033550`. The second word is packed: the high byte is `0x40`
for most rows, and the last two rows carry `textId = 0xFFFFFFFF` with a different payload,
~~**which is what a terminator or a default row looks like**~~. *Superseded 2026-09-25 (FABLE, Claude Opus 5.5):*
they are ordinary rows of a third kind, not terminators; see the decode below.

> **The same `+0x08` / `+0x0A` header shape serves both files with the count in a different
> slot** - `hchk` counts at `+0x08`, `qstd` at `+0x0A`. That is worth stating because it means the
> two are *not* one format with a shared header, despite sharing an extension and a directory.

### Both are `(kind, id)` requests, confirmed two ways

| file | tag | kind | id | `.fst` | extracted |
|---|---|---:|---:|---:|---:|
| `menuquest.dat` | `qstd` | **7** | **296** | 540 | **540** |
| `menuhandbook_knowledge.dat` | `hchk` | **7** | **757** | 812 | **812** |

Each size occurs **exactly once** in the whole 205,000-entry table, and **reading the kind-7 array
at `01E0E530 + id * 8` returns the file's own path** - so the size inversion and the array read-back
agree independently.

The neighbours place them: id 297 is `menuquest.nfs`, and ids 756/757/758 are
`menuhandbook_knowledge.bin`, `.dat` and `000.dat`. **A format sheet that names its neighbours has
said where the file sits, not just what it contains.**

**Not claimed:** what the `hchk` record fields mean when they are not `0xFF`; ~~what `qstd`'s packed
second word holds~~; and the `0x67` / `3` / `18` header fields in either file.

**`qstd`'s rows, decoded 2026-09-25 (FABLE, Claude Opus 5.5).** The table is the list behind UI request 19, the
hunt list. The list owner `0037F4D0` loads it into `+0xC8` of the object it publishes at `02AED490`
([ui-request-router.md](../../16-UI/Request-Router/ui-request-router.md) UQ-162).
- **Payload low byte = row kind.** The file has 19 rows of kind 0 (the leading row and 18 more), 45 of kind 1, and
  the final 2 of kind 2.
- **Bits 8-17 = an entry id.** `0037EDB0` matches request 19's parameter against it, and the row builder
  `0037E8D0` reads the same field.
- **Bits 20-29 = an order index.** It equals the row number, with two exceptions: the id-172 row takes 63, and
  the kind-2 rows take 0. Bits 18 and 30 are set on every kind-0 row. No reader of either field is traced here.
- **The text ids resolve against `test_battle/us/binaryfile/questtitle.bin`,** an id-keyed st2e file: an id list
  at `[0x10]` and the string table at `[0x14]`. It was matched by the ids it contains, not through the loader.
  The 45 kind-1 rows are hunt titles, from "A Tingling Toast" to "A Dark Rumor"; 37 are titled and the last 8
  are empty in the US file.
- **The kind-0 and kind-2 rows carry no title.** The kind-0 titles are empty strings. The leading row's id
  `0x33550` has no string in that file. The two kind-2 rows (ids 50 and 51) have no text id at all.

## 13. `QST1` - `questbase.bin`, 700 bytes — 2026-09-16 (SWE2-DATA)

Nine copies, one per language directory (`<locale>\bin\questbase.bin`), **byte-identical** across
all nine (sha `b7f1548a…`). The format closed end-to-end against the shipping executable:

```
+0x00  char[4]  "QST1"
+0x04  u32      173         entry count — 8 + 173*4 = 700 exactly
+0x08  u32[173]  entries:
       bits  0-12   u13  0x2CE = 718 — the same value in all 173 entries
       bits 13-25   u13  sub-index (0,1,2,…; 121 entries carry 0, the rest small values)
       bit  26      flag — set on 50 entries, clear on 123
       bits 27-31   zero in every entry
```

**Request path:** `(kind 9, id 0x21)`, requested by `0051ED10` (called from `00473D33` with
`ecx=9`, `edx=0x21`), buffer published to `02CA6C60`.

**Consumers, decoded in full:**

- `00473B90(idx)` — bounds-checks against the `u32` count at `buf+4`, returns
  `entries[idx] & 0x1FFF` — the constant 718 in the shipped file.
- `00473C90(idx)` — same bounds check, returns `((entries[idx] >> 13) & 0x1FFF) + 0xA000` — a
  text-id in the `0xA000` bank, so the sub-index selects the quest's text record.
- `00473B70` / `00473CC0` walk two sibling globals (`02CA6C68`, `02CA6C70`) — per-slot
  **pointer tables** built post-load: `00473CC0` reads `{u8, u16 self-relative offsets}` records
  where `0x8000`-set offsets are the null sentinel (the same offset-chain encoding `hcom` uses).

**Not claimed:** the meaning of the constant field 718 (every entry shares it — the field exists
and is read, but the shipped data exercises only one value), what flag bit 26 gates, and which
quest slot each index names. No code validates the `QST1` tag — like `mrp`, the loader trusts
the resource id.

## 14. `dP<d` - `summoneffectdata.bin`, 672 bytes — 2026-09-16 (SWE2-DATA)

One file only: `common\summoneffectdata.bin` (sha `7227d863…`). The census marks the leading
bytes **UNDETERMINED**, and the decode keeps it that way:

```
+0x00  char[4]  "dP<d"      no magic check exists in .text — the tag is trusted, not validated
+0x04  …         668 B packed parameter bytes
tail   8 B       zero pad
```

*Superseded 2026-09-29 (below): `dP<d` is not a tag but record 0's first four bytes, and ~~the 668 bytes are~~ the file's 672 bytes, from `+0x00`, are 64 ten-byte records and a 32-byte tail.* *(corrected 2026-10-02, OPUS: 64 · 10 + 32 = 672 = `0x2A0`, the tail at `0x280`)*

~~The payload resists a record-grid reading: an exhaustive stride/offset scan finds no column
constant above 71%, and the value histogram is dominated by `0x64` (36%), `0x80` (16%) and
`0x20` — decimal-looking multiples of 5 and 10 consistent with a **packed parameter stream**
(scaled values or bit/nibble fields), not an aligned record array.~~ *(Superseded 2026-09-29: the grid is 10 bytes, and the percent-like values are the 0.01 scale factors — below.)*

**Request path:** `(kind 9, id 0x2A)`, requested by `003B53C0`, which also initialises the
summon-effect state block at `02B40508`+ (flags/fields cleared by `003B53C4`–`003B5403`). The
owning module is the summon-effect system in `003B4xxx`–`003B6xxx` — it maintains a runtime
instance pool of `0xE0`-byte records × `0xA0` slots at `02B40528` (`003B56D0` walks it by flag
bit `+0x40`). ~~The kind-9 named-object mechanics (`0032E400`→`0032E620`, blob → `02AD9B60`) are
in [the loader-bound `.bin` families](loader-bound-bin-families.md) §3.~~ *(Corrected 2026-09-29: not a named object — the file is read into the `.data` buffer `02AD9B60` itself, with a null callback; below.)*

~~**Disposition: container-level only.** The magic, size, request `(kind, id)` and owning module
are established; the payload's field structure is **not** — no consumer read of a named offset
has been identified, and the byte stream does not self-describe. This is the weakest of the six
sibling results and is recorded as such rather than guessed.~~ *(Superseded 2026-09-29, below.)*

~~**Not claimed:** any field semantics inside the 668-byte payload.~~

### The reader is found, and `dP<d` is data — 2026-09-29 (SWE2-DATA, `OPUS-REQ-DATA-BUCKET-MEMBER-FORMATS`)

*Correction of the two statements above and of the loader-bound page's "17 float records". Check
[`b7_summoneffect.py`](../../_index/candidates/bucket-members-0929/checks/b7_summoneffect.py), 39 checks, FAILS 0 —
it fails on either old reading (it requires ten-byte records and the 0.01-scaled readers).*

The file is read straight into a `.data` buffer, not into an allocated object: `003B53C0` requests
`(9, 0x2A)` (`mov edx, 0x2a` at `003B53CB`, `lea ecx, [rdx-0x21]` = 9, call `0032E400` at
`003B5407`) with `lea r8` = **`02AD9B60`** as the destination (`003B541D`) and a null callback
(`003B5411`), then `0032E620` (`003B5427`). A raw sweep of `02AD9B60`–`02AD9E00` finds 9 references:
that `lea` and 8 reads.

```struct SummonEffectRecord base=file size=0xA
+0x00  u8[3]    scaleA         x 0.01 (constant at 0036FC0A) - read at 0036FC34 / 0036FC28 / 0036FC1F
+0x03  u8[3]    scaleB         x 0.01 - read at 0036FC7B / 0036FC6F / 0036FC66
+0x06  u8[4]    colour         copied four times into 02AE9690.. - read at 0036FAC8 / 0036FAE5 / 0036FB02 / 0036FB1F
```

**64 records** at `+0x000`, indexed by `(byte result of 003B5340) − 1` (`dec eax` / `lea rdx,
[rax+rax*4]` / `[rcx+rdx*2]` at `0036FC19`–`0036FC1B`) with no bound against 64; only records 0–27
differ, and 28–63 are the neutral record (scales 1.00 ×6, colour `80 80 80 20`). Then the tail:

```struct SummonEffectTail base=file+0x280 size=0x20
+0x00  f32      t0             1.01 - read at 0036FA30
+0x04  f32      t1             1.01 - read at 0036FA46
+0x08  f32      t2             1.4 - read at 0036F7AA
+0x0C  f32      t3             0.4 - read at 0036F5AE
+0x10  u32      u0             65300 - read at 0036F583
+0x14  u32      u1             65200 - read at 0036F561, (u1 - u0) split in thirds (0x55555556 at 0036F576)
+0x18  u8[8]    pad            zero - no reference
```

`64·10 + 4·4 + 2·4 + 8 = 672`. So **`dP<d` is `64 50 3C 64` = record 0's scale bytes 1.00, 0.80,
0.60, 1.00** — the classifier's `UNDETERMINED` was right to refuse it as a tag. What the two scale
triples and the colour do on screen is not named here (the colour's `0x80`-maximum channel values
read as PS2-range colour — an inference).


## 11. Related

- [`../../_index/ASSET-FORMATS.md`](../../_index/ASSET-FORMATS.md) §4e - the signature split that produced this worklist
- [`../Loose-Files-And-Size-Tables/file-size-tables-fst.md`](../Loose-Files-And-Size-Tables/file-size-tables-fst.md) - the per-language path arrays these files are reached through

## Crossings into other layers — FINAL-AUDIT pass 22 (OPUS, 2026-09-18, second pass)

**Sixteen edges over four layers, and every one of them arrives through a READER LIST.** §181 and
§185 answer *who reads this table* by naming the bodies that do — `(00306760, 00313550, 00313840,
00254A90)` and `(002BAF80, 002D5EB0, 005789D0)`. **Naming a reader is the whole of the claim**, and
a reader is a whole function with a whole call graph of its own.

| carrier | size | what it drags in |
|---|---:|---|
| `002D5EB0` | 1,821 B | the audio request path, and three combat-action entries |
| `002BAF80` | 4,810 B | one audio request |
| `00306760` | 911 B | a combat-action entry, a combat-formula routine, and a rewards routine |
| `00313550` | 58 B | one Party caller |

**None of Audio, CombatAction, CombatFormula, Rewards or Party is a subject of this page.** The five
bin tables are **data**; the claim these citations support is that a particular body reads a
particular table, and what that body does afterwards belongs to its own layer's pages.

> **The reader-list shape is worth naming because it is cheap to write and expensive to account
> for.** One parenthesis with four addresses in it is four call graphs. It is the same class as
> citing a shared entry — recorded in FINAL-AUDIT-PROTOCOL against
> `static-initialisers-and-teardowns.md` and against this page's own first pass — with the
> difference that here the citation is *deliberately* a list, because a census of readers is what
> the question asked for. **The citations are right and are kept.**

*`00313550` is 58 bytes and still carries an edge: size does not decide fan-out, reachability does.*

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver / encoder fan-out is MECHANICAL.*

**ActorEntity, Presentation and Script_VM_Native_Bridge — CLIENT.** The path family `0032E400` (size) / `0032E620` (request) is also issued by `ActorResource_BeginPrimaryPayloadLoad`, `ActorResource_BeginManagerResourceSetLoad` and a 3,882-byte actor loader, by two Presentation bodies (119 B and 337 B) and by script-verb bodies (75 B and 115 B). The 177-byte Input-filed item-graphics loader is another client.

## Crossings into other layers — FINAL-AUDIT pass 22 (OPUS, 2026-09-18)

Fifteen edges, two layers, and **all of them arrive through functions this page names only in
passing** while answering where a bin table's base or requester is.

**CoreRuntimeScheduling — fourteen edges, none of them this page's business.** The carrier is
`0022A0B0`, a 978-byte **startup sequence** owned by that layer; it is already characterised from
another page as the code that *writes the globals the small scheduling getters read*
([the NPC name dictionary](../../04-Actor-Entity/Actor-Names/the-npc-name-dictionary.md) accounts
for it the same way). A startup body of that size reaches most of the engine — it makes dozens of
direct calls — so citing it at all imports its whole neighbourhood. This page cites it, and two of
its scheduling-layer neighbours, **only to say where a kind-7 array base or a request comes from.**
**Nothing in that layer is owned here, and the bin tables this page documents are data, not
schedule.**

**RNG_Random_Selection — one edge, and it is startup seeding the generator.** The same
`0022A0B0` calls `RNG_MT19937_Seed` (`00379CF0`), a five-byte entry. **Seeding the Mersenne
Twister at startup has nothing to do with the five bin tables**; the edge is on this page only
because the startup sequence is named here.

*Method, consistent with the rest of this pass: citing a shared entry imports every layer it
touches. The citations above are correct and are kept — what was missing was saying which layers
they drag in and why none of them is a claim by this page.*

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Save_Load_Settings — CLIENT.** `FUN_002ef300`, owned by that layer, calls `0032E620` on this page. That caller is a 65-byte slot entry, and the clamp is the fact: the index is held to **`0..0xF` - sixteen slots** - before it is offset by `0x75` and paired with the size `0xE240`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — CLIENT, 66 edges (OPUS, 2026-09-29): the tables are menu data, so their readers are menu code.** The page
names those readers to answer who reads each table, and their menu neighbours come with them:
- the string measurers `0035D330` (18 UI callers) and `002B58B0` (14), which rebuild the text widths at
  `022CA408`, are called by every menu that lays out text;
- the menu-set request thunk `00249180` → `00249210` is also reached from the world-map mesh and menu-package
  loaders (`00561390`, `00562F90`, `003C9950`);
- the key-signal readers `0029DA70` / `0029DBE0` and the six HUD-mask writers (`00295D20`, `0029E110`, `002B7B80`,
  `002BAF80`, `002D5EB0`, `005789D0`) call menu helpers;
- `0027DED0` is called from `BattleMenu_UpdateCommandSelectionAndDispatch`;
- the quest pointer-table walker `00473CC0` and the text resolver `002F9920` have screen callers.

**No menu behaviour is claimed here.** The menus' own pages own it.

**Gameplay — CLIENT, four edges.**
- The measurer `0035D330` and the width rebuilder `00273E30` call `0031C5D0` (8,136 B). That is the encoded-id query
  a text lookup resolves through, owned by `CONTRACT-encoded-id-space-and-class-registry`.
- `00306760` calls `BattleUnit_DispatchActorPresentationEvent`.
- `BattleSystem_ResetRuntimeState` calls `00313840`, one of the presentation-toggle readers.

The gameplay layer's battle runtime owns all four.

**World — MECHANICAL, three edges.** The startup body `0022A0B0` (already accounted above) also calls the area
initialiser `00266D10`. The map-table requester `00378540` sizes and records its request through `0032E400` and
`0032E620`: it is one more issuer of the shared request path, not a world relationship of the tables.

**WorldAreaField — CLIENT, thirteen edges.**
- The request path `0032E400` / `0032E620` is also issued by the field loaders `MapRef_BeginLoadResources`,
  `AreaArd_LoadOrUnloadFieldResource`, `003319D0`, `00378030` and `00379A10`.
- `WorldAreaField_BootMapTables` (`00377CC0`) is the sole caller of `00378540`.
- The HUD-mask writers `002B7B80` / `002BAF80` read `WorldTransition_GetActiveOrPendingFieldId`.
- `002F9920` has two field-side callers (`003C0450`, `00576A50`).

The field's load order is owned by the world area pages; this page claims only that these bodies request or read
the five tables.

*These four entries: tier 2 - ledger names, sizes and `edges.tsv`, roles as this page and the cited pages read
them; no new body read (OPUS, 2026-09-29, pass-22 debt `42a617a9a`).*

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-five-small-bin-tables-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0029DCD0` | 12 B | stores qword `+8` of `rcx` in qword `0209C4A0` | `0029DCD4` |
| `0035B3E0` | 98 B | for each index below dword `+4` of `rcx` (unsigned), replaces the dword at `rcx+8` plus 4 times the index with `0020E620(0020E600(that dword) + the low 32 bits of rcx zero-extended)`; then, also when the count is zero, stores `rcx` in qword `02EC0B68` | `0035B40B`, `0035B410`, `0035B419`, `0035B421`, `0035B430` |
| `0035FED0` | 89 B | clamps `edx` to 0 when negative and to 1 when above 1; returns without work when `ecx` is 2 or more (signed); otherwise, with the record at `022CAE90` plus `ecx` times `0x294`, stores `r8b` at byte `+6` plus `edx` of the record, calls `0035E810` and stores its dword result at `+0x1C` plus `edx` times 4 | `0035FEE3`, `0035FEE9`, `0035FEF8`, `0035FF0C`, `0035FF16` |
| `00379F30` | 7 B | zero-extends `ecx` into `rcx` and tail-jumps `0035B3E0` | `00379F32` |
| `003C9950` | 125 B | calls `00249580` with `rcx` unchanged (result r); when qword `+0xD0` of `rcx` is non-null calls `003697F0` on it; calls `00249210(r, 7, byte +0xC1 plus 0xE, 3)` with fifth (stack) argument 0 and then `00249410(r)`; ORs 8 into dword `+0xC4` and stores qword `+8` of the `00249210` result in qword `+0xD0` | `003C9976`, `003C999B`, `003C99A6`, `003C99AF`, `003C99C0` |

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-03, cloud-drafted)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../../_index/candidates/fable-home-five-small-bin-tables-1003/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
| `0029D4D0` | 114 B | `0029E110` + 0x203 | calls `0029D4D0` + 0x21 with (qword `0209C498` + `0x160`, `0x148`, the address loaded by the `lea` at `0029D4DB`, 0) and the same callee at `0029D4D0` + 0x43 with (qword `0209C498` + `0x2A8`, `0x148`, the same address, 0); then calls `0029D4D0` + 0x56 with (qword `0209C498`, that pointer + `0x160`) and tail-jumps to the same callee at `0029D4D0` + 0x6D with (qword `0209C498`, that pointer + `0x2A8`), re-reading `0209C498` before each call | Interior anchor `0029D4E2`; Interior anchor `0029D4F1`; Interior anchor `0029D513`; Interior anchor `0029D526`; Interior anchor `0029D53D` |
