---
title: "Small .bin tables: footstep sounds, controller vibration, battle window sizes, the button legend, quest window texts and summon colours"
kind: "format"
category: "Game files and data tables"
addresses: "00378540, 002E9D90, 00379E90, 0035B3E0, 0035B650, 0035B2F0, 0035AF20, 0035AE30, 0034AC30, 0035C5B0, 0035C3F0, 0027BDE0, 0027DED0, 0029DC90, 0029DA70, 0029DBE0, 0029E330, 00473D20, 00473B90, 00473C90, 003B53C0, 003B5340, 0036FBB0, 0036F9F0, 02ADD0C0, 02EC0B68, 022CA460, 0209C4A0, 02CA6C60, 02AD9B60"
---

## What the player sees

- The footstep sound for each kind of ground, and a second set of footstep sounds on twelve surfaces in
  the weather states that switch it on.
- Controller rumble when an event script asks for it.
- The width and number of visible rows of the battle command lists.
- The strip of button prompts at the bottom of menus, pairing each button with what it does there.
- The message in the quest result window that scripts open.
- The colour shift and full-screen tint while a summon's effect is active.

## Where it comes from

All six are files under `ps2data/image/ff12/` in the archive, reached by resource kind and id through the
path arrays and sized by the [file size tables](file-size-tables-fst.md). Each is requested once and kept.

| File | Kind / id | Copy read | Requester |
|---|---|---|---|
| `common/soundfoottable.bin` | 9 / 9 | the one file | `00378540` |
| `common/eventvib.bin` | 9 / 7 | the one file | `00379E90` |
| `myoshiok/<lang>/bin_menu/menubtlwndinfo.bin` | 7 / `25`<sub>h</sub> | the language's own | `0035C5B0` |
| `myoshiok/<lang>/bin_menu/key_signal_data.bin` | 7 / `24`<sub>h</sub> | the language's own | `0029DC90` |
| `<in or ch>/bin/questbase.bin` | 9 / `21`<sub>h</sub> | `in`, or `ch` for Korean and the two Chinese languages | `00473D20` |
| `common/summoneffectdata.bin` | 9 / `2A`<sub>h</sub> | the one file | `003B53C0` |

"The language's own" means the `us`, `fr`, `de`, `it`, `es`, `kr`, `ch` or `cn` copy, and the `in` copy
for Japanese, UK, ASIA and IN.

- `00378540` requests the footstep table with the completion `00378F80`, which stores the buffer at
  `02ADD0C0`; `00377C10` returns that pointer.
- `0035C5B0` requests the `bwind` file through the menu-set wrapper `00249180` and stores the buffer at
  `022CA460`.
- `0029DC90` requests the `signe` file only while `0209C4A0` is null; its completion `0029DCD0` stores
  the buffer there.
- `00473D20` passes kind 9, id `21`<sub>h</sub> to `0051ED10` and stores the result at `02CA6C60`.
- `00379E90` hands the `VIB0` buffer to `0035B3E0` (through `00379F30`), which publishes it at
  `02EC0B68`.
- `003B53C0` reads `summoneffectdata.bin` straight into the 672-byte `.data` buffer `02AD9B60` with no
  completion callback.

## Layouts

### FOOT: soundfoottable.bin

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `char[8]` | "FOOT01\0\0" | tag, compared by no reader |
| `08`<sub>h</sub> | `u16` | 32 | count: the offset of set B within the byte table |
| `0C`<sub>h</sub> | `u32` | 0 |  |
| `10`<sub>h</sub> | `i8[32]` | set A | sound for surface 0..31 |
| `30`<sub>h</sub> | `i8[32]` | set B | sound for surface 0..31 with the weather variant flag set |

### VIB0: eventvib.bin

```
+0x00  char[4]  "VIB0"         tag, compared by no reader
+0x04  u32      count          patterns
+0x08  u32[count]              offset of each pattern from the file start; rewritten to addresses at load
pattern
+0x00  u16      track 2 start  pair index where the second track begins
+0x02  u16                     not read
+0x04  {u8 duration, u8 level}[]   track 1 begins at pair 0; a duration of 0 ends a track
```

A pair's level ramps to the next pair's level over its duration, so the level byte at `+5 + 2k` is the
start of pair k and the byte at `+7 + 2k` its end.

### bwind: menubtlwndinfo.bin

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `char[8]` | "bwind\0\0\0" | tag, compared by no reader |
| `08`<sub>h</sub> | `u32` | count | 15 |
| `0C`<sub>h</sub> | `{u16` | width, | u16 rows}[count] |

### signe: key_signal_data.bin

```
+0x00  char[8]  "signe\0\0\0"  tag, compared by no reader
+0x08  u16      offset of section 0 (buttons)
+0x0A  u16      offset of section 1 (signals)
+0x0C  u16      offset of section 2 (scenes)
+0x0E  u16      not read
section 0      u32 count, then {u32 name text id, u32 button mask}[count]
section 1      u32 count, then u32[count]: bits 0-23 label text id, bits 24-31 button (section 0 index)
section 2      u32 count, then u16 offset[count] from the section start to each scene
scene          u8 scene id, u8 a, u8 b, u8 n, then {u8 signal (section 1 index), u8 flag}[n]
```

### QST1: questbase.bin

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `char[4]` | "QST1" | tag, compared by no reader |
| `04`<sub>h</sub> | `i32` | count |  |
| `08`<sub>h</sub> | `u32[count]` | bits 0-12 value A, bits 13-25 text index, bit 26 flag, bits 27-31 zero |  |

### summoneffectdata.bin

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `000`<sub>h</sub> | `record[64]` | 10 bytes each, indexed by the active summon effect minus 1 |  |
| `000`<sub>h</sub> | `u8[3]` | scale A, red, green, blue, in hundredths |  |
| `003`<sub>h</sub> | `u8[3]` | scale B, in hundredths |  |
| `006`<sub>h</sub> | `u8[4]` | colour of the full-screen tint |  |
| `280`<sub>h</sub> | `f32` | copied to 02AE9660 | +`284`<sub>h</sub> f32  copied to `02AE9664` |
| `288`<sub>h</sub> | `f32` | tint size factor (02AE9650 and scaled copies) |  |
| `28C`<sub>h</sub> | `f32` | copied to 02AE9668 |  |
| `290`<sub>h</sub> | `u32, +294h u32` | two words whose difference is split in thirds for the tint's layers |  |
| `298`<sub>h</sub> | `u8[8]` | zero |  |

The file has no tag: its first four bytes `64 50 3C 64` are record 0's scale bytes.

## Shipped data

Measured over every copy in the archive.

| Fact | Value |
|---|---|
| `soundfoottable.bin` | 80 bytes, one copy; set A is 0 to 31 in order; set B gives 32 to 41 for surfaces 0 to 9, 42 and 43 for surfaces 13 and 14, and repeats set A elsewhere |
| `eventvib.bin` | 176 bytes, one copy; 11 patterns of 10 bytes from `34`<sub>h</sub>, then 14 bytes no offset reaches: `00 AE 00 00` and a copy of pattern 10 |
| `eventvib.bin` patterns | each is one ramp on track 1: duration 15 (patterns 0-2, 6), 35 (3-5, 7) or 5 (8-10), level 120 to 255, flat except pattern 1 (155 to 160); track 2 starts at pair 2, whose duration is 0, in all eleven |
| `menubtlwndinfo.bin` | 72 bytes, nine identical copies; entry 4 is width 150, rows 8; the other 14 are width 10, rows 8 |
| `key_signal_data.bin` | 532 bytes, nine identical copies; sections at `10`<sub>h</sub>, `EC`<sub>h</sub> and `150`<sub>h</sub> with 27, 24 and 19 records; the word at `+0E`<sub>h</sub> is `CCCC`<sub>h</sub> |
| `key_signal_data.bin` sections | button text ids `2BF4D`<sub>h</sub> onward with masks of one or two bits (five masks 0); scene ids 1 to 19, 14 scenes with one signal and 5 with two; `a` is 2 on scenes 6 to 9 and 0 elsewhere, `b` is 0 on all; the last two bytes, after scene 19, are `CD CD` |
| `questbase.bin` | 700 bytes, nine identical copies; 173 entries; value A is 718 in every entry; the text index is non-zero on 52 entries (1-6, 9 and 128-172), each equal to its entry number; bit 26 is set on entries 0 to 49 |
| `summoneffectdata.bin` | 672 bytes, one copy; records 0 to 27 differ, records 28 to 63 are all scales 100 and colour `80 80 80 20` |
| `summoneffectdata.bin` tail | 1.01, 1.01, 1.4, 0.4, 65,300 and 65,200 |

## Loader behaviour

### Footsteps

`002E9D90(actor, kind, sound, useVariant)` picks an actor's sound in slot `kind` (0 to 2). For kind 1,
the footstep, with a non-negative `useVariant`:

1. The surface is the signed word `+8A`<sub>h</sub> of the record at `[[actor′ + C0h] + 138h]`, where `actor′` is
   the actor the sound resolves to (`00263F40`).
2. When `useVariant` is non-zero and the weather variant flag `02099DBC` (0 or 1, set from
   `map_ref.bin` for the current weather slot; see [weather](../World-Areas-And-Travel/weather.md)) is
   non-zero, the table index is the count word `+08`<sub>h</sub> plus the surface and the sound starts at −1;
   otherwise the index is the surface and the sound starts at 0.
3. The signed byte at `+10h + index` is added. With `useVariant` set, the flag is added again, so with
   the flag at 1 the sound is set B's entry and with the flag at 0 set A's.
4. `003A1240(bank, sound)` checks the actor's bank handle for the slot against its record at
   `02AEEDC8` and returns `bank slot × 512 + sound`, or −1 for a stale handle.

When the table is not loaded, the sound is the surface plus 32 − flag, plus the flag again: surface + 32
with the flag set, the surface itself without it. Nothing bounds the surface against 32.

### Vibration patterns

- **Binding.** `0035B3E0` replaces each offset with an address handle (`0020E600` / `0020E620` over the
  buffer's low 32 bits) and stores the buffer at `02EC0B68`.
- **Starting.** The script verb `vibplay` (`23D`<sub>h</sub>, native `0034AC30`) passes its argument to
  `0035B650(pattern, 2)` when `00267310` returns 0 for the calling actor's byte `+15`<sub>h</sub>. `0035B650`
  returns unless the pattern is below the count.
- **The slot.** `0035B2F0` takes a free 32-byte slot from the list at `02EC0B60`: state 1, record at
  `+8`, scale 1.0 at `+10`<sub>h</sub>, track 1 at pair 0, track 2 at the record's `u16 +0`, pad 0. `0035B650`
  records the handle in one of eight entries at `022C8030` and arms the slot: state 2, or 4 when the
  mask `02EC0B40` blocks it.
- **Stepping.** `0035AF20` adds 10,000 × the time base `01DFE0BC` (1.0 at 30 fps, 0.5 at 60 fps) to the
  accumulator `022C8050` and runs one step per 10,000. Each step clears the output pair at `02EC0B50`.
- **Levels.** In a step, each track of a playing slot whose pair has a non-zero duration writes
  `(start + (end − start) × elapsed / duration) × scale` when larger than the value already there
  (track 1 to `02EC0B50`, track 2 to `02EC0B54`) and advances; a slot whose two tracks have both reached
  a zero duration goes to state 4.
- **Output.** `0035AE30` sends the two values to pad 0 through `0035FED0` (track 1 to actuator 1,
  track 2 to actuator 0) when the vibration switch `02EC0B3C` is on, and zero otherwise; it then frees
  every listed slot in state 4.

### Battle window sizes

`0035C3F0(out, entry)` returns the entry's width, raised to the measured text width `022CA408[entry]`
when that is larger, and its row count. `0027BDE0(kind, out)` maps the battle window kind to the
entry: kinds 2 to 7 to entries 1 to 6, kinds 9 to 15 to entries 7 to 13, kinds 16 to 19 to entry 14,
anything else to entry 0. Nothing bounds the entry against the file's count.

`0027DED0(menu, kind)` sizes the open list: the width goes to the list object's word `+EA`<sub>h</sub> (widened by
`01E0C364 − 01E0C354` for kinds 10 to 14 in mode 4), the visible rows are the table's rows clamped to the
list length `+500`<sub>h</sub> and to at least 1 (byte `+1528`<sub>h</sub>), and the height is rows × the row height word
`+100`<sub>h</sub>. Entry 4, the only wide one, is window kind 5: `0027E050` opens kind 5 as the command-list
window with sub-selector 7, beside kinds 4, 6 and 7 with sub-selectors 3, 5 and 6.

### Button legend

- **Masks.** `0029DBE0(key)` returns section 0's button mask for a key below the button count, and for
  `100h + n` the mask of the button signal n names. A key of `16`<sub>h</sub> or `1A`<sub>h</sub>, or a signal naming
  button `16`<sub>h</sub> or `1A`<sub>h</sub>, returns the word `01E0C2A0`; `17`<sub>h</sub> returns `01E0C2A4`; a key at or past
  the button count returns 0.
- **Mask range.** `100h + n` for `n` at or past the signal count also returns 0; only a valid signal's
  out-of-range button clamps to the last button.
- **Scenes.** `0029DA70(out, scene)` finds the scene whose first byte matches, copies `a`, `b` and `n`
  to `out[0..2]`, and fills one `18`<sub>h</sub>-byte slot per pair from `out + 8`: the button's name and the
  signal's label as strings from the text resolver `002F9920`, the word `(~(flag << 2)) & 4` and the
  signal index. A scene id with no scene reads from address 1 and faults.
- **Showing.** `0029E330(scene)` builds the legend and `0029DDF0` copies it into the HUD object
  `[0209C498] + 158h` at `+D0`<sub>h</sub> only when it differs. Its callers are menu screens (`00295D20`,
  `0029E110`, `002B7B80`, `002BAF80`, `002D5EB0`, `005789D0`).

### Quest window texts

`00473C90(n)` returns `A000h +` entry n's text index, and `00473B90(n)` entry n's value A; both return
−1 when n is not below the count, with a signed compare. The begin native of the script verb
`questresultwindow` (`37C`<sub>h</sub>, `00344C60`) falls back to entry 0 on −1 and opens the window with that
text id through `00290130`. Value A is read by `queststartwindow`'s begin `003456E0` and by the
hunt-list row builder `0037E8D0`, which stores it in the row.

### Summon colours

`003B5340` returns the active summon effect (1-based) from the two 8-byte state entries at `02B40508`
and `02B40510` (`+0` effect, `+1` priority, `+2` state, 1 = active, `+4` actor, −1 none): the active
entry with the higher priority byte, the first on a tie, or 0 when none is active or bit 0 or 1 of
`02B40518` is set; `003B53C0` clears both entries before the read.

- `0036FBB0` turns record `effect − 1`'s scale A into the floats at `0209A3C0`..`0209A3C8` and scale B into `0209A3D0`..`0209A3D8` (each byte × 0.01), or sets all six to
  1.0 when no effect is active.
- `0036F9F0` copies the record's colour into the tint packet at `02AE9690` and its copies, with the tail
  floats at `+280`<sub>h</sub> and `+284`<sub>h</sub>, sets a 256 × 224 rectangle and submits the packet through
  `003A35E0`; `0036F550` builds the layered form from the tail fields at `+288`<sub>h</sub> to `+294`<sub>h</sub>.

Nothing bounds the effect against 64.

## Modding notes

- No reader checks a tag, so the first bytes can be anything; `summoneffectdata.bin` has none.
- `soundfoottable.bin`: keep the count word at 32 unless set B moves; a surface above 31 reads past the
  set it indexes.
- `eventvib.bin`: end each track with a zero-duration pair; levels are bytes, durations count steps of the
  accumulator. A pattern number at or past the count is ignored.
- `menubtlwndinfo.bin`: keep at least 15 entries; the window-kind map reaches entry 14.
- `key_signal_data.bin`: every scene id a menu asks for must exist, or the game faults; keep the three
  section offsets in the header in step with the sections.
- `questbase.bin`: the window text id is `A000h +` the text index, at most `1FFF`<sub>h</sub>.
- `summoneffectdata.bin`: the file must be exactly 672 bytes, the size of its fixed buffer; scales are
  hundredths.

## Related

- [File size tables](file-size-tables-fst.md): the kind and id sizes these requests use.
- [File requests and the read queue](file-requests-and-the-read-queue.md): the request path.
- [Battle and menu text tables](battle-text-tables.md): the text ids the legend and quest windows resolve.
- [Weather](../World-Areas-And-Travel/weather.md): the variant flag that selects footstep set B.
- [The .bin families under ps2data](ps2data-bin-families.md): every other `.bin` family.
