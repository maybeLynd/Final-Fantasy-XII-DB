---
title: "Text codes: every control code inside the game's strings, what it does and what follows it"
kind: "reference"
category: "Menus and HUD"
addresses: "0x002AC5F0, 0x002AE334, 0x002AE3FC, 0x002AE370, 0x002AC2F0, 0x003FFDF0, 0x002AEB20, 0x002A8C50"
---

## What it lists

`text-codes.tsv` has one row per control code: the 14 control bytes `0x01`-`0x0E` and the `0x0F` escapes by their
selector character. Each row gives the arm that runs it, its length, what it does, and how many times it appears in
the shipped text of all nine languages.

### How a string is read

The text interpreter `0x002AC5F0` reads a string one unit at a time, until a `00` byte or the painter's terminator word
(`0x002AC663`):

1. A byte `0x01`-`0x0F` is a token. It indexes the 15-entry table at `0x002AE334` (`0x002AC682`-`0x002AC697`).
2. A byte `0x10`-`0x1F` is the lead byte of a two-byte character, and any other byte is a one-byte character
   (`0x002AC2F0`).
3. After a `0x0F`, the next byte is the selector. A selector from `0x20` to `0x70` picks one of 35 arms at `0x002AE370`
   through the byte map at `0x002AE3FC`; any other selector is drawn as a character.

The callers that measure and draw text (`0x002B1FB0`, `0x002B2150`) send every byte below `0x10` to the interpreter.
The pager's markup parser `0x002A8C50` walks the same strings to pace them. It acts on `0x03`, on the choice list
`0x0E` (the option setup at `0x002A9066`) and on the escapes `#`, `-`, `/`, `;`, `p`, `"` and `=`. Its pacing step
(`0x002A9747`) also pauses at `>`, `8`, `.`, `p` and every icon.

### Code lengths

Most escapes read their payload through a small parser. The length of the whole code, with the `0x0F` and the
selector, is:

| Code | Bytes | Parser |
|---|---:|---|
| `0F !` | 2 | none (`0x002AD1E5`) |
| `0F 40`-`0F 6B`, the icons | 3 | `0x002AEB20`, which always returns 2 |
| most escapes | 4 | `0x003FFAB0`, `0x003FFB90`, `0x003FFC60`, `0x003FFDA0`, `0x003FFEE0` |
| `0F 1`, `0F l` | 5 | `0x003FFF10`, `0x003FFCE0` |
| `0F 8`, `0F o` | 4, or 5 when bits 0-2 of the first payload byte are set | `0x003FFB00` |
| `0F )` | 3 + the larger of 1 and bits 0-2 of the first payload byte | `0x003FFBC0` |
| `0F *` | 4 + bits 0-6 of the second payload byte | `0x003FFD70` |

Token `0x08` is 3 bytes (`0x002AD011`), tokens `0x0B`-`0x0D` move nothing (`0x002AC6CA`), and every other token is 1
byte.

The parsers `0x003FFAB0`, `0x003FFB00` and `0x003FFBC0` look their argument up through `0x0039BA00(v)`, which returns the
5-byte record `v & 0x1FF` of the table at `[0x02AEE870]` (`fontpack_it.bin` entry 2), counting from its byte 1, and
record 0 when that is 0.

`0x003937C0(out, size, text)` copies at most `size` - 1 bytes of a string and a terminator: for a template that
starts with `ex` (`0x00364980`) it stops at a zero two-byte unit and writes a two-byte terminator, otherwise it
stops at a zero byte and writes one. The battle log's
`0x00393740` and `0x00408640`, `0x00408700` and `0x00408960` use it.

### Choice lists

Token `0x0E` (`0x002AC825`, parser `0x003FFDF0`) is a choice list. Bits 0-6 of its first byte give the option count;
when bit 0 of the fourth byte is set, a field of one bit per option follows, one byte per seven options. Each option
is a length byte (bits 0-6) and that many bytes of text, which may hold codes of its own. An option whose bit is set
in the text context's mask `+0x84` is left out (`0x002AC957`). The list stops on its own `00`, so a list always ends
its string.

### Tokens

| Token | Does |
|---|---|
| `0x01` | a blank the width of `0x0017F920(0)` (`0x002ACC04`) |
| `0x02` | a line break: the next line is measured, justified and indented by `+0xAA` (`0x002AC6D1`) |
| `0x03` | the page end: the interpreter stops the run (`0x002AC6AE`), and the pager waits for the confirm button (`0x002A8DC7`, `0x002A97CD`-`0x002A9808`) |
| `0x04` | the ordinary space, the width of `0x0017F920(1)` |
| `0x05` | a column mark: a blank of 15 units that records the column widths (`0x002ACCF3`) |
| `0x06` | a blank of 10.0 (`0x008F8180`) |
| `0x07` | a blank of 10 units, or 26 when `0x00254A10` returns 0 and `0x00229E40` returns 7 |
| `0x08`, `0x09` | no effect: the cursor moves 3 or 1 bytes |
| `0x0A` | a right-aligned column: it measures up to the next `0x02` or `0x05` (`0x002ACF10`-`0x002ACF34`) |
| `0x0B`-`0x0D` | no effect: the interpreter returns without moving |
| `0x0E` | a choice list, above |

The four blank tokens scale with the text size and letter spacing (`0x002ACC97`-`0x002ACCE3`).

### Layout and size escapes

| Escape | Does |
|---|---|
| `0F %`, `0F &`, `0F '` | justify left, right or centre, with a margin (`0x002AD289`, read by `0x002B1F20`) |
| `0F 2` | a tab: 0 stores the pen position, any other value moves to it plus twice the value (`0x002ADC71`-`0x002ADCD0`) |
| `0F 5`, `0F 6` | indent in or out by the value (`0x002ADD19`, `0x002ADD62`) |
| `0F o` | sets the pen's x position (`0x002ADCF8`) |
| `0F <` | shifts the baseline (`0x002AE1C5`) |
| `0F 4` | sets the advance of the next glyph only (`0x002ADD03`) |
| `0F (` | the text size in 24ths (`0x008F3128`) |
| `0F 7` | the text size in percent: `+0x34 = value / 100.0` for the unsigned value byte (`0x008F3134`, `0x002AD394`-`0x002AD3B1`) |
| `0F 3` | separate x and y scales in tenths: `+0x38 = (byte1 & 0x7F) / 10.0` and `+0x3C = (byte2 & 0x7F) / 10.0` (`0x003FFDA0`, called at `0x002ADC5A`-`0x002ADC62`) |
| `0F` space | a fixed advance for marked glyphs, the value over 90 (`0x009166FC`, `0x002AD074`) |
| `0F $` | the letter spacing (`0x002AD252`) |

### Colour, inserts and icons

| Escape | Does |
|---|---|
| `0F )` | the text colour; 0 is the default grey `0x80808080` (`0x002AD3F7`) |
| `0F +` | a render-state byte, sent to the draw packet (`0x002AD821`-`0x002AD86F`) |
| `0F .` | inserts an argument of the message: a string, or a number through `0x002AE610` (`0x002AD8F9`) |
| `0F -` | draws a number with up to 8 digits (`0x002AD8AB`, `0x002AE610`) |
| `0F 8` | inserts the name for a 16-bit id (`0x002639E0`) |
| `0F >` | inserts the name of the speaking character (`0x00263990`) |
| `0F ?` | draws one glyph from three bands of the payload (`0x002AE11A`-`0x002AE177`) |
| `0F 40`-`0F 6B` | an inline icon: the letter picks the sprite; R, S, Z, `[` and `\` follow the controller type (`0x002AEB20`, `0x009165F0`, `0x00916670`) |
| `0F *` | ruby text: a short text drawn at 0.65 of the size (`0x009166F0`), centred above the next bytes (`0x002AD47C`) |
| `0F !` | switches to the alternate font record (`0x002AD151`) |

### Pager escapes

| Escape | Does |
|---|---|
| `0F #` | a page wait: a value of 1 or more waits 30 ticks per unit (pager mode 3), and 0 waits for the confirm button (mode 5, `+0x88` = 10,000); interpreter arm `0x002AD205`-`0x002AD232`, pager arm in `0x002A8C50` |
| `0F -` | the pager sets mode 4 and measures the number (`0x002B35A0`, `0x002B43C0`) |
| `0F /` | the type-out speed (`0x002A91EA`-`0x002A93AE`) |
| `0F "` | the pager's rate value `+0x9E` (`0x002AD1ED`, `0x002A9442`-`0x002A94C1`) |
| `0F ;` | read by the pager at `0x002A94CD` |
| `0F p` | sets pager flag bit 20 (`0x002A9670`-`0x002A96E2`) |
| `0F 9` | sets `+0xA7` and pager flag bit 21 (`0x002AE190`-`0x002AE1A1`) |
| `0F =` | sets `+0xAE` (`0x002AE1DB`, `0x002A96EA`) |
| `0F :` | resets the text state without ending the run (`0x002AE1B1`) |

The escapes `,`, `1`, `l`, `m`, `n` and `V` are read and stepped over with no effect. `0F 0` and `0F _` have no arm,
so the selector is drawn as a character (`0x002ACFC2`).

### Template escapes

Before a template is drawn, the formatter `0x002B49F0(size, out, template, args, typed)` copies it into `out` and fills
some escapes from its arguments. It is reached through `0x002B4090` and `0x002B40C0`. Without `typed` it takes the
arguments in order, eight bytes each; with `typed` each escape names an entry of an array of `0x10`-byte arguments,
type 1 a number and type 2 a string (for example `0x002B4ADA`-`0x002B4AFF`).

`0x002B40C0` first scans the template with `0x002B4810(template, slots)` (`0x002B4108`), which types the argument slots the
escapes name, stepping by `0x002B1FB0` lengths and switching on the byte after each `0F` (table `0x002B4990`, index bytes
`0x002B49A8`): `-` (`0x003FFC60`) and `l` (`0x003FFCE0`) set `slots + 8 + 16 x slot` to 1, `1` (`0x003FFF10`) and `m`
(`0x003FFB90`) set it to 2, the slot being the byte the parser returns; `+` and `,` (`0x003FFAB0`) set the next qword of
the list at `slots + 0x88` (16-byte stride) to 1. Every other code does nothing.

| Escape | Becomes |
|---|---|
| `0F +` | `0F + 81` and the argument's byte, a render-state code |
| `0F ,` | the 7-byte colour code `0F )` of the argument's RGBA |
| `0F -` | the number in glyph codes (`0x002B3770`) |
| `0F 1` | the string argument, padded with `0x01` blanks to the escape's minimum length; with a field width w it sits between a tab code `0F 2` that stores the pen position and one that moves to it plus 2 x w |
| `0F l` | with `typed`: a number, or for 1 the string argument's variant (`0x002B58B0`) |
| `0F m` | with `typed`: a word row's singular, or for a count above 1 its plural (below) |
| `0F n` | with `typed`: variant `k + 2` of a word row; for language ids 1-6 and 9 (`0x00254A10` answers 0) its first letter is capitalised when nothing has been written before it |

Any other unit is copied. A result that does not fit ends `out` at `size - 1` and returns `0xFFFF` (`0x002B51C3`).
`0x002B58B0(row, k)` returns string `k` of a word row ([battle text tables](../Game-Files-And-Data-Tables/battle-text-tables.md)).

`0x002B4550(size, out, row)` builds a plural: string 1 of the row is the plural template and string 0 the base word.
Token `0x08` with a two-byte count `& 0x7FFF` copies that many bytes of the base word, token `0x09` the whole word, and
anything else is copied (`0x002B45E3`-`0x002B46A2`).

`0x002B3770(size, out, &pos, value, digits, pad, fullwidth, space)` writes a number with `0x003EFD00` and turns each digit
into the font's glyph code through the font sheet's first character map, or the second with `fullwidth`; a digit the
map gives 0 becomes the blank token 7, or 1 with `fullwidth`, and `space` adds a final `0x04` ([Fonts](fonts.md)).

Three writers build codes for menu strings:

- `0x002AB870(size, out, rgba)` writes the colour code `0F )`, 8 bytes with its terminator, the same encoding as the
  `0F ,` arm;
- `0x002AC2C0(n)` returns the static code `0F ? 81 n` at `0x01E0CDFC`;
- `0x002B5240(record)` copies a string, replacing each `0F 8` with the name it stands for (`0x002639E0`), and
  `0x002B5680(size, out, in)` copies one without its line breaks `0x02` and baseline codes `0F <`.

### Two-byte number templates

Some screens fill a template of two-byte units that starts with the bytes `ex`. `0x00365B30(size, out,
template, args)` forwards to `0x00365B50`, which copies the 4-byte head and then each unit. A unit `{` followed
by `i` is a 4-unit escape whose low bytes give a field width and flags. It takes the next 8-byte argument as
an integer and writes it through `0x00365E50`.

`0x00365E50(out, value, width, zeros, length)` writes the digits as units `'0'` + d. With a width it pads them
on the left with `0x01` blanks; with `zeros` it starts with `0x02`, pads with `'0'` units and marks the first
significant digit with `0x03`. It returns the digit count and the byte length through `length`.

`0x0029CC00(id, n)` fills the template of text id with n (at least 0) into the next of eight 32-byte buffers
at `0x0209C390`, rotating through `0x01E0C560`, and `0x0029CC70(out, id, n)` into the caller's buffer; an id below
100,000 is read with `0x002F9860`, a larger one with `0x002F9920(id - 100000)`. `0x0029CB80(id, arg)` does the same
with the formatter `0x002B4090` instead; the magick and equipment description builders use it.

`0x00365B50` returns the length written plus 2, or 0 when the template lacks the head or the result does not
fit. Its callers include `0x0029FF60`, `0x002D66D0`, `0x002D7A90`, `0x00407450`, `0x00407720` and `0x0055BAC0`.

### Description lines

`0x00292B70(out, entry)` writes the description line of a list entry, `{kind, id in the high word}`, into a
`0x1F8`-byte buffer. It takes the kind's template from `0x00295C20`, runs the kind's handler from the 16-entry
table `0x01E0C490`, closes the gaps in the argument list and formats it (`0x002B4090`). The shops (`0x0057BEE0`), the
equip list (`0x003FCEE0`), `0x00293170` and `0x00564430` call it.

Three kinds are narrowed first:

- kind 3, equipment: ammunition (`0x002CCA00`) becomes 2; otherwise the row's `+0x4C` gives 1 for 0, 3 for 1,
  4 for 2 and 3, and 5 for 4, the mapping `0x00292F60` also gives the equip menu (`0x003FF920`);
- kind 6 with an id from `0x4000` to `0x4017` (`0x002CCB00`) becomes 7;
- kind 10 needs an id from `0x8060` to `0x81FF`.

| Kind | Handler | What it reads |
|---|---|---|
| 1 to 5 | `0x00295900`, `0x00295390`, `0x00294B50`, `0x00293FE0`, `0x00293310` | equipment by slot: weapon, ammunition, off hand, head and body, accessory |
| 6 | `0x00294860` | a magick: class 8, its action row (class 20), the school name (class 24), the action's `+0x24`, a text from `0x4B27` plus the lowest set bit of the action's byte `+0x30` (`0x232D` when it is 0), and `0x002960B0` |
| 7 | `0x002957C0` | a technick: class 9 and its action row's description, and `0x002960B0` |
| 8 | `0x00293E10` | an item: class 5 and its action row's description, with the same `0x4B27` text |
| 9, 10, 12, 14, 15 | `0x00293F40`, `0x00294AB0`, `0x00295720`, `0x002956B0`, `0x002947F0` | the description `+0x10` of class 7, 13, 11, 26 or 18: loot, key items, gambit conditions, statuses, bazaar goods |

`0x00293CE0(list, bits, text, count, n, flag)` adds to an argument list a text `0x4B27` + b for each set bit b
of a byte, with `text` before or after them depending on the language (`0x00254A10`, `0x00264150`); the kind 3, 4
and 5 handlers use it.

### Codes no shipped text uses

Over every string of the nine languages, these never appear:

- the tokens `0x06`, `0x07`, `0x0B`, `0x0C` and `0x0D`;
- the escapes `"`, `#`, `0`, `6`, `:`, `V` and `_`;
- the icon letters `\`, `]`, `b`, `d`, `f`, `h`, `i` and `j`.

The page wait `0F #` is therefore never used; every shipped wait for the confirm button comes from `0x03`.

### The text the counts cover

The counts walk every string from its start with the lengths above, stepping into ruby text and choice-list options,
in all nine language trees under `ps2data`:

| Source | Strings |
|---|---:|
| `st2e` string tables | 24,469 |
| `st2e` tables inside `.ard` files | 324 |
| `word.bin` | 44,680 |
| `hdat` records | 11,916 |
| event script text, section 2 | 156,337 |
| event script text, section 3 | 20,818 |
| `.msb` files | 388 |
| `npcdic.bin` | 20,538 |

Every walk ends on its terminator followed only by zero bytes. The copies inside `battle_pack.bin` are counted once.
The 14,652 credits strings in `menu03.bin` are UTF-16 (tag `ex00`, written by `0x00365660`) and hold no codes. Event
script section 2 holds 949,262 of the 1,083,172 codes other than the space in the `total` column (87.6%).

Sixteen strings in `evt_t0080.ebp` and `evt_t0086.ebp` of the `ch`, `cn`, `in` and `kr` trees hold choice lists
whose option lengths do not fit the 7-bit field. The interpreter masks the length the same way (`0x002AC946`), so it
reads past those options; their codes are counted separately.

## Columns

| Column | Meaning |
|---|---|
| `code` | the token byte, or `0F` and the selector byte |
| `char` | the selector as a character; `space` and `quote` stand for `0x20` and `0x22` |
| `arm` | the address the jump table sends the code to |
| `parser` | the payload parser the arm calls, or `none` |
| `bytes` | the whole code's length, `0x0F` and selector included |
| `does` | what the arm does, with its addresses |
| `st2e` to `npcdic` | the count in each text source, as in the table above |
| `total` | the count over all sources and languages |
| `of_which_nested` | how many of those sit inside ruby text or a choice-list option |
| `in_malformed_lists` | codes inside the 16 strings with malformed choice lists, not in `total` |
| `languages_with_any` | how many of the nine languages use it |
| `per_language` | the count per language tree |

## Related

- [Dialogs](dialogs.md) - the message boxes that show this text.
- [Menus](menus.md) - the screens whose labels hold these codes.
- [Controllers](../Controls-And-Input/controllers.md) - the controller type the button icons follow.
