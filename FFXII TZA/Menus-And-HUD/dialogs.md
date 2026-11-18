[Home](../../README.md) / [Menus and HUD](README.md) / Confirm windows

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Dialogs: the confirm window behind every yes-or-no question, notice and the item sort, and three single-screen boxes | system | Menus and HUD | How menus work | The shared confirm window and the boxes that sit beside it: who creates the confirm window and with which flags, what each flag bit changes (cancelling, notice mode, timed dismiss, any-button confirm, the header label, the backdrop and the confirm sound), its stages and the answers it posts back, the item screen's sort bar, the Clan Primer's category list with its four records, and the license board's description box. | 0x0057C480, 0x0057C380, 0x002CDF20, 0x002CE370, 0x00566680, 0x0056F810, 0x00556F90, 0x00D23688 |

## What the player sees

- A yes-or-no question, such as buying a license, opens a small window with Yes and No.
- Notices, such as an error or a newly obtained license, open the same window without a choice. How one closes
  depends on its flags (below): an ordinary notice and a tutorial or license announcement stay until the player
  closes them, and some error notices also close by themselves after a few seconds, at any button, or both.
- The item screen's Sort command opens it with the sort options.
- Two more screens have a box of their own: the Clan Primer opens on a list of Hunts, Bestiary, Sky Pirate's Den
  and Traveler's Tips, and the license board chooser shows the name and description of the board under the cursor.

## How it works

### The confirm window

`0x0057C480` is the window's procedure. It is a single instance: building it stores it at the root's `+0x328`¹, and message 18 clears that². Its create record comes from `0x0057C380`, whose three callers
pass fixed flags as the record's `+0x20`, kept at `+0x630`³:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057C4D9` |
| ² | `0x0057CC79` |
| ³ | `0x0057C4E4`-`0x0057C4E8` |

</details>

| Creator | Installed by | Flags | Used for |
|---|---|---|---|
| `0x002CDF20` | `0x002CDEA0` | `0xC812` (`0x002CE086`) | the yes-or-no question: Yes posts `0x8100`, No `0x8101`, No is the default row |
| `0x002CE370` | `0x002CE2F0` | `0x411A`; `0x511A`, `0x1411A`, `0x1511A` for errors; `0x611A` for tutorials and license announcements | the notice: 22 caption cases of a 28-slot switch |
| `0x00566680` | `0x005665B0` | `0x8036` (`0x00566939`) | the item screen's sort picker |

Message 1 copies the caption into a `0x400`-byte buffer at `+0x1B0`¹, measures it and
keeps the width at least `0x60`². A one-line caption, bit `0x20`, is measured by
`0x002B3050` after `0x002B3400` and the stores of `[0x01E0CF90]` at `+0x120` and `[0x01E0CF94]` at `+0x114`³; any other by `0x002B3280` and `0x002B1E20`⁴. With a null caption
pointer the buffer is filled with zeros⁵, the same two calls run, and the width is
twice `[0x01E0CDC0]` and the height 0⁶.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00254F30`, `0x0057C501` |
| ² | `0x0057C5FD`-`0x0057C607` |
| ³ | `0x0057C516`-`0x0057C556` |
| ⁴ | `0x0057C568`-`0x0057C599` |
| ⁵ | `0x0057C5A6`-`0x0057C5AC` |
| ⁶ | `0x0057C5B1`-`0x0057C5F7` |

</details>

It then stores the create record's `+0x10`, the owner, at `+0xC8`¹, its byte `+0x1C` at `+0x634`², the dword `0xFFFF0000` at `+0x636`³, the low byte of the caption height at `+0x635`⁴, 0 in the word `+0x63A`⁵ and the record's `+0x08` at `+0xD0`⁶. In each of
the eight 16-byte option rows at `+0x5B0`-`+0x62F` it clears bit `0x1` of the dword `+0x0C`, the qword `+0x00`
and the word `+0x08`, and leaves the rest of the row⁷.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057C60E` |
| ² | `0x0057C61A` |
| ³ | `0x0057C620` |
| ⁴ | `0x0057C62A` |
| ⁵ | `0x0057C630` |
| ⁶ | `0x0057C63C` |
| ⁷ | `0x0057C643`-`0x0057C6EB` |

</details>

`0x0057C380(record, open)` builds the `0x640`-byte window with `0x00244F50` and returns it from the root's `+0x328`¹. Message 1 ends by opening the window when `open` is non-zero²:
`0x0057CD40` puts it under its `+0xD0`³ and builds the `0x4000` backdrop. The yes-or-no question and the
notice give 1⁴; the sort picker gives 0 and calls `0x0057CD40` itself after it has set the
window's `+0x634` and the list's row⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057C3A6`-`0x0057C3C4` |
| ² | `0x0057C872`-`0x0057C880` |
| ³ | `0x00246AD0` |
| ⁴ | `0x002CE067`, `0x002CE6A7` |
| ⁵ | `0x002D4650`, `0x005669CD` |

</details>

### The flag bits

| Bit | Effect |
|---|---|
| `0x2` | cancellable: cancel posts `0x8102` to the owner (`0x0057CAD1`); without it cancel moves the cursor to the default row when bit `0x8` is clear and does nothing when bit `0x8` is set (`0x0057CAF4`-`0x0057CAF6`) |
| `0x8` | notice: no list is built (`0x0057C6F3`), the pad is read directly, and confirm posts `0x8100` |
| `0x10`, `0x2000` | frame variants 1 and 4 (`0x0057C7EE`-`0x0057C802`) |
| `0x20` | a one-line caption (`0x0057C506`, `0x0057C90F`) |
| `0x800` | the hand cursor stays on the chosen row while the window closes (`0x0057C7CC`) |
| `0x1000` | in notice mode on message 10, once `0x002B3930(+0xE0)` answers 0 and byte `+0x190` is 1 (`0x0057C9A3`-`0x0057C9CB`), the word `+0x63A` counts down by 1 while above 0, and when it is 0 the window sends itself `0x8002`, or `0x8001` with bit `0x10000` (`0x0057C9E1`-`0x0057CA12`); the notice sets 180 |
| `0x4000` | a dimmed backdrop at `+0xD8` (`0x0057CD77`), released on close (`0x0057C34A`) |
| `0x8000` | the header label is `0x4B42` instead of `0x4B48` (`0x0057C93E`) |
| `0x10000` | any button confirms, and the timed close counts as confirm (`0x0057CA09`-`0x0057CA1C`) |
| `0x4`, `0x40`, `0x80`, `0x100`, `0x200`, `0x400` | the confirm sound: the list's sound id becomes `0x37`, `0x19`, `0x18`, 3, 4 or `0x45` (`0x0057CB8F`-`0x0057CBD7`); No plays 3 (`0x0057CB85`) |

### Stages and answers

| Step | What happens | Where in the code |
|---|---|---|
| 1 | Sub-command `0x8000` moves the window through its stages, counted at `+0x637` from 0 up to 3, and, outside notice mode and once the count is not 0, tells the owner the cursor row with `0x8103`. | `0x0057CC62`-`0x0057CC6F`<br>`0x0057CC09`-`0x0057CC5D` |
| 2 | `0x8001` is a pick. In notice mode it posts `0x8100` to the owner, clears bit `0x8` of the window's `+0x40` and answers 0. Otherwise it reads the list's row and its option's flags; a row whose option has bit `0x1` of `+0x0C` clear posts nothing and answers 1. | `0x0057CB16`-`0x0057CB26`, `0x0057CADA`-`0x0057CAEF`<br>`0x0057CB66`-`0x0057CB6F`, `0x0057CBFF` |
| 3 | `0x8002` is cancel: with bit `0x2` it posts `0x8102` and clears bit `0x8` of the window's `+0x40`. Without bit `0x2` it moves the list back when bit `0x8` is clear and does nothing when bit `0x8` is set. | `0x0057CACB`, `0x0057CAD1`-`0x0057CAE9`<br>`0x002D4650`, `0x0057CAFC`-`0x0057CB0A`<br>`0x0057CAF4`-`0x0057CAF6` |
| 4 | Message 10 forwards input to the list unless the window is in notice mode. | `0x0057C9A3` |

For any other row a pick sets the confirm sound when the option's word is `0x8101` or one of the sound
bits of the flag table is set, and makes no sound store otherwise¹; it then posts
the option's word `+0x08` to the owner at `+0xC8`². A reply of 1 answers 1³; any other reply clears bit `0x8` of the window's `+0x40` and answers 0⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057CB75`-`0x0057CBD7` |
| ² | `0x0057CBDE`-`0x0057CBF1` |
| ³ | `0x0057CBFF` |
| ⁴ | `0x0057CBF6`-`0x0057CBF9`, `0x0057CAE9`-`0x0057CAEF` |

</details>

`0x0057C3E0(window, element, row)` is the list's row callback, given in the create record `0x002D14E0` takes¹. While `+0x636` is set it colours the element (`+0x90`) with `0x002DD7E0(6)` when the row's word
`+0x5B8 + 16 x row` equals `+0x638`, else with `0x002DD7E0(2)` unless the row's `+0x5BC` has bit `0x1`, draws
`0x002D8910(element, 0, 0, [window + 16 x (row + 0x5B)], 0)`, and puts the colour back to `0x002DD7E0(0)`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0057C722` |

</details>

`0x00241D40`, installed by `0x00241BF0` and `0x00241C90`, is a second confirm procedure that reads the same layout keys.
Its row callback `0x00241D00` draws Yes (`menu_command.bin` `0x3E8`) on row 0 and No (`0x3E9`) on the other.
`0x00241B40(window)` answers a pick: message 12 with `0x8100` to the owner `+0xD0` for row 0 of the list `+0xC8`
and `0x8101` for any other. `0x00241A70(window)` answers a cancel by the mode byte `+0x3BE`: 1 sends `0x8101`, 2
sends `0x8102`, and 0 moves the list back to the row `+0xC0`¹, first posting `0x8104` to the owner
when `+0x3C4` bit `0x800` is set.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002D4650` |

</details>

`0x002477A0(window, v)`, which `0x00241D40` calls with 4¹, stores `v & 7` in bits `0x70000` of `+0x44` and sets
the two bytes `+0xAC` and `+0xAD` from that field: with its bit `0x4` set, `+0xAD` becomes `0xF9` when bit `0x2` is
set and `+0xAC` becomes `0xF9` when bit `0x1` is set; with bit `0x4` clear, each byte becomes `0xF9` or 6 by its bit.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00242101` |

</details>

Four builders fill the record `0x00241C90` takes and open the window:

- `0x00394380(owner)`, from `0x003939B0`, turns the second draw pass on (`0x00247780(1)`) and opens it with text
  `0x002F9860(0x890)`¹ under the root `[0x0208EA28]`, flags `0x1002` and mode 2.
- `0x003948B0(owner, text, flags, options)` opens it under `[0x0208EA28]` with the options' bits under mask `0x1F`
  (`+0x48`) turned
  into window bits `0x8`, else `0x200` (with the default row from `+0x44`), then `0x10`, `0x800` and `0x400`; flags with
  `& 0xFF0` of `0x70` or `0xD0` give style 1 or 2. `0x0023E020`, `0x0023E560`, `0x00252030`, `0x0057AA00`, `0x00583990`
  and `0x00583FD0` call it.
- `0x003949B0(owner, text, options)` and `0x00394A90` do the same from the options' word `+0x14` (bit `0x4` to
  `0x20`, bit `0x10`
  to `0x8` or else bit `0x8` to `0x200`, bit `0x20` to `0x10`, bit `0x40` to `0x800`, bit `0x80` to `0x100`, bit `0x100` to `0x400`) in
  style 2, under `[0x0208EA28]` or, for `0x00394A90`, the
  root `[0x0208EA50]` (slot 4); `0x00394A90` serves `0x00583FD0`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00394395` |

</details>

The procedure registers itself in the table `0x0208EA60` under slot 2 when its creator's root is `[0x0208EA38]`, 4 for `[0x0208EA50]`
and 1 otherwise¹, and clears the slot when it closes². `0x00241A50(slot)` answers
whether one is open; the battle menu asks with 1³ and `0x00228C70` with 2⁴. Its other
callers are `0x0027A353`, also in the battle menu, and `0x00229095`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00241E11`-`0x00241E48` |
| ² | `0x0024257E` |
| ³ | `0x0027C4D2` |
| ⁴ | `0x00228E65` |

</details>

### The item sort bar

`0x00566680` is the sort strip in the item screen, installed by `0x005665B0`. Its message 12¹ takes these
sub-commands:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00566794` |

</details>

| Sub-command | Does |
|---|---|
| `0x8102` | closes the bar (`0x00244F00`) |
| `0x8103` | shows the row's help: "Sort items in default order by category." (`0xCC1`), "Sort by item strength." (`0xCC2`), "Sort by amount." (`0xCC3`) |
| `0x8104`-`0x8106` | the three sorts, Auto-sort (`0x4A8`), By Strength (`0x4A9`) and By Quantity (`0x4AA`): the code minus `0x8103`, 1-3, is stored as the tab's sort through `0x002527B0(7, tab, ...)` (`0x005667DD`), and the code minus `0x8104`, 0-2, is passed to `0x00565CD0` (`0x005667FD`) |

`0x002527B0(7, tab, v)` stores `v` in the byte `+0x70 + tab` of `[0x020927C0]`, the tab clamped to 0-31¹, and `0x002526F0(7, tab, 1)` reads it back². When the bar opens, a stored value
other than 0 puts the cursor on the row whose code is `0x8103` plus that value (`0x005668F7`-`0x00566905`, `0x0057CD00` at
`0x005669A5`, `0x002D4650` at `0x005669C1`); with 0, or when that row is not listed, the cursor starts on row 0³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002527F7`, `0x0025280A` |
| ² | `0x00252763`, `0x00252777` |
| ³ | `0x00566900`, `0x0057CD37` |

</details>

After `0x00565CD0` the sort arm stores 12 in the bar's byte `+0xE2`¹. When the object at
`+0xC0` and its first qword are not null it calls that qword with the object and a record of the dword
`0x11E`, the bar's dword `+0xC8` and the answer of `0x00565CD0`, both sign-extended to qwords²; `0x002527B0` is called with a first argument of 7 before `0x00565CD0`³. It then clears bit `0x8` of the bar's dword `+0x40`⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0056681F` |
| ² | `0x005667E4`-`0x00566838` |
| ³ | `0x005667F1` |
| ⁴ | `0x0056683A` |

</details>

Message 2¹ does nothing while the byte `+0xE2`, read signed, is 0 or less. Otherwise it
takes 1 from the byte, and when that leaves 0 it sets bit `0x8` of `+0x40` and closes the bar with
`0x00244F00`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0056688D` |
| ² | `0x00566894`-`0x005668B1` |

</details>

`0x00565CD0(screen, tab, sort)` sorts the list of the screen's own tab: `0x00252F40` of the list id at
`0x00D23960 + 4 x 0x00564380(screen)`¹. The `tab` argument, which the sort bar's call
(`0x0056680B`, the only direct one) takes from its word `+0xE0`², set from `0x00564380` of the same
pane when the bar opens³, only picks the By Strength comparator⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00565CFE`-`0x00565D15` |
| ² | `0x005667F6` |
| ³ | `0x005668DF`-`0x005668EC` |
| ⁴ | `0x00565D4C`-`0x00565D5D` |

</details>

The sort runs through
`0x00249CE0` with one of five comparators¹, and does nothing for a list of fewer than two items. Each comparator reads the
two items' query records (`0x0035D330(1, id << 16)`,
[item and ability ids](../Engine-Core/item-and-ability-ids.md)) and falls back to the next rule on a tie:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00565D43`-`0x00565D7F` |

</details>

| Sort | Tab | Comparator | Order |
|---|---|---|---|
| Auto-sort | any | `0x002CFFE0` | by `0x002CFDA0` when the first item's class is 6 (`0x002D0000`-`0x002D0015`); otherwise by `+0x30`, then the id |
| By Strength | `0`, `3` | `0x002CFD30` | `+0x58` highest first, then `0x002CFDA0` |
| By Strength | `1` | `0x002CFEE0` | `+0x50`; then for `+0x50` = 2 `+0x58` and `+0x5C`, otherwise `+0x5C` and `+0x60`, highest first; then `0x002D01A0` |
| By Strength | `2` | `0x002D0100` | `+0x5C`, then `+0x60`, highest first, then `0x002CFDA0` |
| By Quantity | any | `0x002D0200` | the count `+0x24` highest first, then `0x002CFFE0` |

By Strength on a tab other than `0` to `3` sorts nothing and returns -1¹, as a list of
fewer than two items does². A sort number other than the three returns 0 unsorted³, and every sort returns 0.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00565D5A`-`0x00565D5F` |
| ² | `0x00565D30`-`0x00565D33` |
| ³ | `0x00565D3E`-`0x00565D41`, `0x00565D9E` |

</details>

`0x002CFDA0` orders by `+0x38`, then `+0x30`, then the id, and `0x002D01A0` by `+0x30`, then the id, all lowest first.

`0x002D0070` and `0x002CFE40` are `0x002CFFE0` and `0x002CFDA0` for rows that carry the item id in the word `+8`
instead of `+0`. `0x002C38B0`¹ and `0x002C4720`²
pass `0x002D0070` to `0x00249CE0`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002C3AF8` |
| ² | `0x002C4947`, `0x002C4AF7`, `0x002C4E4E`, `0x002C4FCB` |

</details>

Auto-sort is always offered; the other two rows depend on `0x00564380`.

Message 18¹ clears the row highlights with `0x00567690`². When the qword
`+0xE0` of the object at its `+0xC0` is not 0 it calls `0x00295D50(1)`³. When the
qword `+0x1E0` of the object at its `+0xD0` is not 0 it calls `0x00291D70(0)` and then `0x00291D80(p, 0)`, p
being the qword `+0x18` of that `+0x1E0` object⁴. It then sets the parent's
sort-changed bit, `+0x180 |= 0x40000000`, the parent being the object at `+0xC0`⁵, and clears the root's `+0x2F0`⁶.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x005666D4` |
| ² | `0x005666D4`-`0x005666FA` |
| ³ | `0x005666FF`-`0x00566715` |
| ⁴ | `0x0056671A`-`0x00566746` |
| ⁵ | `0x0056674B`-`0x00566752` |
| ⁶ | `0x0056675C`-`0x00566765` |

</details>

Message 15¹ hands its
window, the object at `+0xD8`, to `0x0057C340` when it is not null and then clears `+0xD8`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00566771` |
| ² | `0x00566771`-`0x00566788` |

</details>

That window is the one `0x0057C380` returned to the picker¹. `0x0057C340` returns at once
for a null window². When the window's dword `+0x630` has bit `0x4000` it calls
`0x002CCB30(word [[window + 0x48] + 0x16])` and zeroes the window's own `+0xD8`³; in
every case it then releases the window with `0x00244F00`⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00566941`-`0x0056694D` |
| ² | `0x0057C340`-`0x0057C343` |
| ³ | `0x0057C34A`-`0x0057C366` |
| ⁴ | `0x0057C371`-`0x0057C374` |

</details>

`0x002CCB30(value)` returns at once when the layer kept at `[[0x0209AC30] + 0x298]` is null or bit `0x20` of
the layer's dword `+0x7C` is set¹. Otherwise the value, compared signed
as a dword, acts first. 0 or less changes nothing². `0x1000` or more clears bit
`0x800` of `+0x7C` and sets bit `0x10000` of the layer's dword `+0x40`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002CCB30`-`0x002CCB4B`, `0x002CCB95` |
| ² | `0x002CCB4D`-`0x002CCB4F` |
| ³ | `0x002CCB51`-`0x002CCB65` |

</details>

1 to `0xFFF` keeps the `+0x7C` bits under mask `0x3FF7FF`, adds the value's low word shifted left by 22
as a dword, so that only the value's bits under mask `0x3FF` are kept, and sets bit `0x800`¹. In all three cases `0x002CCB30` then loads the layer pointer again and jumps to
`0x00244F00` with it².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002CCB6B`-`0x002CCB7F` |
| ² | `0x002CCB82`-`0x002CCB90` |

</details>

### The Clan Primer's category list

`0x0056F810` is installed only by `0x00574D00`, from the Clan Primer's back panel `0x00574E80`. It lists four records of the
table at `0x00D23688`, filtered by unlock¹. Its message table at `0x0056FA80` serves ids 1, 10, 12, 14, 15 and 18,
and every other id goes to the default `0x0056FA73`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0056F750` |

</details>

| Record | Label | Help | Opens kind |
|---:|---|---|---:|
| 0 | Hunts | "Hunt information and progress." | 6 |
| 1 | Bestiary | "Insights on foes you have defeated." | 5 |
| 2 | Sky Pirate's Den | "What will it take to fill the den?" | 7 |
| 3 | Traveler's Tips | "Hints for the wary adventurer." | 4 |

A record is 6 bytes (below). A pick posts its kind to the parent with `0x8001`¹. Records 4-11 hold the page titles of the eight Clan Primer page kinds: 4-7 point at
labels `0x1B58`-`0x1B5B`, which are empty, and 8-11 reuse the four labels above.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0056F96A`-`0x0056F9B5` |

</details>

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | label | label text |
| `+0x02` | `u16` | help | help text |
| `+0x04` | `u8` | kind | posted to the parent on a pick |
| `+0x05` | `u8` | flag | - |

The messages `0x0056F810` serves:

- 1 keeps the message's `+0x08` as the parent at `+0xC0` and its `+0x10` at `+0x170`, clears `+0xC8` and the list
  `+0x168`, sets the picked record `+0xCC` to `0xFF`, builds the rows with `0x0056F5F0`, clears bit `0x800` of `+0x40`
  and gives the list priority `0x63`¹².
- 14 sets bit `0x1` of `+0xC8`, refreshes the badges³, shows the help line of the cursor's row
 ⁴, posts `0xE` with 3 to the parent⁵ and takes the focus⁶
 ⁷.
- 10 runs the row list `+0x168` when there is one⁸.
- 12 with `0x8000` shows the help line of the row it names while bit `0x1` of `+0xC8` is set
 ⁹. With `0x8002` it posts `0x8002` with 3 to the parent and calls `0x002CC9C0(0xC8)`
 ¹⁰. Any other sub-code returns 0.
- 12 with `0x8001` is the pick: the row's record number goes to `+0xCC`, a number of 4 or more reads record 0, and a
  kind of `0xFF` posts nothing and returns 1¹¹.
- 15 clears the help line (`0x00291D80(0, 0)`), clears bit `0x1` of `+0xC8` and posts `0xF` with 3
 ¹².
- 18 saves the cursor row's record number in bank 6 (`0x002527B0(6, 3, record)`) and posts `0x12` with 3
 ¹³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00247930` |
| ² | `0x0056F83C`-`0x0056F87C` |
| ³ | `0x0056FAD0` |
| ⁴ | `0x00291D80` |
| ⁵ | `0x00247510` |
| ⁶ | `0x002470D0` |
| ⁷ | `0x0056F889`-`0x0056F8F9` |
| ⁸ | `0x002D3900`, `0x0056F906`-`0x0056F916` |
| ⁹ | `0x0056F9C2`-`0x0056F9E5` |
| ¹⁰ | `0x0056F943`-`0x0056F95D` |
| ¹¹ | `0x0056F96A`-`0x0056F99F` |
| ¹² | `0x0056F9F2`-`0x0056FA07`, `0x0056FA59`-`0x0056FA66` |
| ¹³ | `0x0056FA09`-`0x0056FA66` |

</details>

Every other id goes to `0x005C5230`, which returns 0, and every handled message returns 0 apart from that pick.

### The license board's description box

`0x00556F90` shows text only and answers messages 1 and 2; its message-18 arm returns 0, as its default does. Its one installer `0x00556EC0` is called only from the
license board chooser `0x00557DB0`¹. The chooser writes the board number to `+0x3D1` on each
cursor step². Message 2 writes the board's name, `menu_command.bin` `0x3ED` plus the board ("White Mage"
for board 0), as the header, and its description, `menu_message.bin` `0x838` plus the board, split into three lines
at `+0xD0` by `0x002B5730`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00557E76`, `0x00557EE5` |
| ² | `0x00558549` |

</details>

Message 2 does nothing while `+0x3D1` equals `+0x3D2`, the board last written, and stores the board in `+0x3D2`
after writing it¹. The header's `+0x20` takes `0x0020E620(0)`², and each of the three lines is cleared to `0x100` zero bytes before `0x002B5730` copies
into it³. Both arms return 0.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00556FC8`-`0x00556FD5`, `0x00557074` |
| ² | `0x00557001`-`0x00557006` |
| ³ | `0x00557030`-`0x0055705A` |

</details>

Message 1 builds the box¹. It takes its rect from `0x002432B0` with layout 2 of
`[[0x0209AC30] + 0x98]` into `+0x98`-`+0x9E`, installs the descriptor `0x00D23030`², keeps the creation
block's first qword at `+0xC8` and its byte `+0x08` at `+0x3D0`, and makes `0x00556F50` the row callback `+0x120` of
the list `[[[+0x60] + 0x28] + 0x18]`, kept at `+0xC0`, with the box at the list's `+0xD8`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00557087`-`0x005571AA` |
| ² | `0x00247570` |

</details>

It then clears the list's `+0xE0` bit `0x200000`, calls `0x002D45C0(list, 0)`, clears bit `0x8000000` and restarts
the pulse¹. A `+0x3D0` of `0xFF` becomes 0; `+0x3D1` takes it and `+0x3D2` becomes `0xFF`, so the next
message 2 writes. Last it clears bit `0x1` of `[[+0x60] + 0x18] + 0x08`, gives the box priority `0x5F`² and puts it in the second draw pass (`0x00247730(box, 1)`).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002445C0` |
| ² | `0x00247930` |

</details>

## State

<details>
<summary>Show the state it keeps</summary>

The table `0x0208EA60` holds one 8-byte window pointer per slot. `0x00241D40` stores itself at the slot it picked¹ and clears it when it closes², both through the slot index.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00241E48` |
| ² | `0x0024257E` |

</details>

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x0208EA68` | `void*` | 0 (zero-filled tail) | slot 1: the second confirm window opened under a root other than `[0x0208EA38]` and `[0x0208EA50]`, 0 when no such window is open | `0x00241D40`: the window (`0x00241E48`), 0 when it closes (`0x0024257E`); `0x002419B0`, 0 after it closes the window (`0x00241A04`, `0x00241A31`) | `0x002419B0` (`0x002419B6`); `0x00241A50(slot)` (`0x00241A5C`), with 1 from the battle menu (`0x0027C4D2`) and with a variable slot from `0x0027A353` and `0x00229095` |

`0x002419B0`, run by `0x0035BB70` at the field set-up and teardown¹, closes the slot-1 window unless its
`+0x7C` bit `0x20` is set: it hides it² when bits `0x1` and `0x20` of `+0x40` are set, and otherwise sends it message 15³ and releases it⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0035BB99` |
| ² | `0x00244DD0` |
| ³ | `0x00915058` |
| ⁴ | `0x00245020` |

</details>

No other instruction reaches `0x0208EA68`. The table's address is taken only by `0x00241A50`.

</details>

## Modding notes

- A new yes-or-no question goes through `0x002CDF20`'s flags `0xC812`; a notice through `0x002CE370`.
- Removing `0x2` makes a question impossible to cancel; adding `0x10000` lets any button confirm.
- The Clan Primer menu's labels, help lines and the page kind each option opens are the four records at `0x00D23688`.

## Related

- [Menus](menus.md) - how the screens that raise these dialogs open.
- [License board](../Items-Equipment-Shops-And-Licenses/license-board.md) - the board the question and the description box serve.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 1 call with 1 other topic</summary>

**Saving, loading and settings** (explained on [resource arena and relocation](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00245020`](widgets.md) (on widgets) | is called by | [`0x00280140`](../Items-Equipment-Shops-And-Licenses/bazaar.md) (on bazaar) |

</details>

---

[← Menu lists](menu-lists.md) | [Message windows →](message-windows.md)
