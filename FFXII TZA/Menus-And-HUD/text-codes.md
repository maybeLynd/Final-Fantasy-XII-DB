---
title: "Text codes: every control code inside the game's strings, what it does and what follows it"
kind: "reference"
category: "Menus and HUD"
addresses: "002AC5F0, 002AE334, 002AE3FC, 002AE370, 002AC2F0, 003FFDF0, 002AEB20, 002A8C50"
---

## What it lists

`text-codes.tsv` has one row per control code: the 14 control bytes `01`<sub>h</sub>-`0E`<sub>h</sub> and the `0F`<sub>h</sub> escapes by their
selector character. Each row gives the arm that runs it, its length, what it does, and how many times it appears in
the shipped text of all nine languages.

### How a string is read

The text interpreter `002AC5F0` reads a string one unit at a time, until a `00` byte or the painter's terminator word
(`002AC663`):

1. A byte `01`<sub>h</sub>-`0F`<sub>h</sub> is a token. It indexes the 15-entry table at `002AE334` (`002AC682`-`002AC697`).
2. A byte `10`<sub>h</sub>-`1F`<sub>h</sub> is the lead byte of a two-byte character, and any other byte is a one-byte character
   (`002AC2F0`).
3. After a `0F`<sub>h</sub>, the next byte is the selector. A selector from `20`<sub>h</sub> to `70`<sub>h</sub> picks one of 35 arms at `002AE370`
   through the byte map at `002AE3FC`; any other selector is drawn as a character.

The callers that measure and draw text (`002B1FB0`, `002B2150`) send every byte below `10`<sub>h</sub> to the interpreter.
The pager's markup parser `002A8C50` walks the same strings to pace them. It acts on `03`<sub>h</sub>, on the choice list
`0E`<sub>h</sub> (the option setup at `002A9066`) and on the escapes `#`, `-`, `/`, `;`, `p`, `"` and `=`. Its pacing step
(`002A9747`) also pauses at `>`, `8`, `.`, `p` and every icon.

### Code lengths

Most escapes read their payload through a small parser. The length of the whole code, with the `0F`<sub>h</sub> and the
selector, is:

| Code | Bytes | Parser |
|---|---:|---|
| `0F !` | 2 | none (`002AD1E5`) |
| `0F 40`-`0F 6B`, the icons | 3 | `002AEB20`, which always returns 2 |
| most escapes | 4 | `003FFAB0`, `003FFB90`, `003FFC60`, `003FFDA0`, `003FFEE0` |
| `0F 1`, `0F l` | 5 | `003FFF10`, `003FFCE0` |
| `0F 8`, `0F o` | 4, or 5 when bits 0-2 of the first payload byte are set | `003FFB00` |
| `0F )` | 3 + the larger of 1 and bits 0-2 of the first payload byte | `003FFBC0` |
| `0F *` | 4 + bits 0-6 of the second payload byte | `003FFD70` |

Token `08`<sub>h</sub> is 3 bytes (`002AD011`), tokens `0B`<sub>h</sub>-`0D`<sub>h</sub> move nothing (`002AC6CA`), and every other token is 1
byte.

The parsers `003FFAB0`, `003FFB00` and `003FFBC0` look their argument up through `0039BA00(v)`, which returns the
5-byte record `v & 1FFh` of the table at `[02AEE870]` (`fontpack_it.bin` entry 2), counting from its byte 1, and
record 0 when that is 0.

`003937C0(out, size, text)` copies at most `size` - 1 bytes of a string and a terminator: for a template that
starts with `ex` (`00364980`) it stops at a zero two-byte unit and writes a two-byte terminator, otherwise it
stops at a zero byte and writes one. The battle log's
`00393740` and `00408640`, `00408700` and `00408960` use it.

### Choice lists

Token `0E`<sub>h</sub> (`002AC825`, parser `003FFDF0`) is a choice list. Bits 0-6 of its first byte give the option count;
when bit 0 of the fourth byte is set, a field of one bit per option follows, one byte per seven options. Each option
is a length byte (bits 0-6) and that many bytes of text, which may hold codes of its own. An option whose bit is set
in the text context's mask `+84`<sub>h</sub> is left out (`002AC957`). The list stops on its own `00`, so a list always ends
its string.

### Tokens

| Token | Does |
|---|---|
| `01`<sub>h</sub> | a blank the width of `0017F920(0)` (`002ACC04`) |
| `02`<sub>h</sub> | a line break: the next line is measured, justified and indented by `+AA`<sub>h</sub> (`002AC6D1`) |
| `03`<sub>h</sub> | the page end: the interpreter stops the run (`002AC6AE`), and the pager waits for the confirm button (`002A8DC7`, `002A97CD`-`002A9808`) |
| `04`<sub>h</sub> | the ordinary space, the width of `0017F920(1)` |
| `05`<sub>h</sub> | a column mark: a blank of 15 units that records the column widths (`002ACCF3`) |
| `06`<sub>h</sub> | a blank of 10.0 (`008F8180`) |
| `07`<sub>h</sub> | a blank of 10 units, or 26 when `00254A10` returns 0 and `00229E40` returns 7 |
| `08`<sub>h</sub>, `09`<sub>h</sub> | no effect: the cursor moves 3 or 1 bytes |
| `0A`<sub>h</sub> | a right-aligned column: it measures up to the next `02`<sub>h</sub> or `05`<sub>h</sub> (`002ACF10`-`002ACF34`) |
| `0B`<sub>h</sub>-`0D`<sub>h</sub> | no effect: the interpreter returns without moving |
| `0E`<sub>h</sub> | a choice list, above |

The four blank tokens scale with the text size and letter spacing (`002ACC97`-`002ACCE3`).

### Layout and size escapes

| Escape | Does |
|---|---|
| `0F %`, `0F &`, `0F '` | justify left, right or centre, with a margin (`002AD289`, read by `002B1F20`) |
| `0F 2` | a tab: 0 stores the pen position, any other value moves to it plus twice the value (`002ADC71`-`002ADCD0`) |
| `0F 5`, `0F 6` | indent in or out by the value (`002ADD19`, `002ADD62`) |
| `0F o` | sets the pen's x position (`002ADCF8`) |
| `0F <` | shifts the baseline (`002AE1C5`) |
| `0F 4` | sets the advance of the next glyph only (`002ADD03`) |
| `0F (` | the text size in 24ths (`008F3128`) |
| `0F 7` | the text size in percent: `+34h = value / 100.0` for the unsigned value byte (`008F3134`, `002AD394`-`002AD3B1`) |
| `0F 3` | separate x and y scales in tenths: `+38h = (byte1 & 7Fh) / 10.0` and `+3Ch = (byte2 & 7Fh) / 10.0` (`003FFDA0`, called at `002ADC5A`-`002ADC62`) |
| `0F` space | a fixed advance for marked glyphs, the value over 90 (`009166FC`, `002AD074`) |
| `0F $` | the letter spacing (`002AD252`) |

### Colour, inserts and icons

| Escape | Does |
|---|---|
| `0F )` | the text colour; 0 is the default grey `80808080`<sub>h</sub> (`002AD3F7`) |
| `0F +` | a render-state byte, sent to the draw packet (`002AD821`-`002AD86F`) |
| `0F .` | inserts an argument of the message: a string, or a number through `002AE610` (`002AD8F9`) |
| `0F -` | draws a number with up to 8 digits (`002AD8AB`, `002AE610`) |
| `0F 8` | inserts the name for a 16-bit id (`002639E0`) |
| `0F >` | inserts the name of the speaking character (`00263990`) |
| `0F ?` | draws one glyph from three bands of the payload (`002AE11A`-`002AE177`) |
| `0F 40`-`0F 6B` | an inline icon: the letter picks the sprite; R, S, Z, `[` and `\` follow the controller type (`002AEB20`, `009165F0`, `00916670`) |
| `0F *` | ruby text: a short text drawn at 0.65 of the size (`009166F0`), centred above the next bytes (`002AD47C`) |
| `0F !` | switches to the alternate font record (`002AD151`) |

### Pager escapes

| Escape | Does |
|---|---|
| `0F #` | a page wait: a value of 1 or more waits 30 ticks per unit (pager mode 3), and 0 waits for the confirm button (mode 5, `+88`<sub>h</sub> = 10,000); interpreter arm `002AD205`-`002AD232`, pager arm in `002A8C50` |
| `0F -` | the pager sets mode 4 and measures the number (`002B35A0`, `002B43C0`) |
| `0F /` | the type-out speed (`002A91EA`-`002A93AE`) |
| `0F "` | the pager's rate value `+9E`<sub>h</sub> (`002AD1ED`, `002A9442`-`002A94C1`) |
| `0F ;` | read by the pager at `002A94CD` |
| `0F p` | sets pager flag bit 20 (`002A9670`-`002A96E2`) |
| `0F 9` | sets `+A7`<sub>h</sub> and pager flag bit 21 (`002AE190`-`002AE1A1`) |
| `0F =` | sets `+AE`<sub>h</sub> (`002AE1DB`, `002A96EA`) |
| `0F :` | resets the text state without ending the run (`002AE1B1`) |

The escapes `,`, `1`, `l`, `m`, `n` and `V` are read and stepped over with no effect. `0F 0` and `0F _` have no arm,
so the selector is drawn as a character (`002ACFC2`).

### Template escapes

Before a template is drawn, the formatter `002B49F0(size, out, template, args, typed)` copies it into `out` and fills
some escapes from its arguments. It is reached through `002B4090` and `002B40C0`. Without `typed` it takes the
arguments in order, eight bytes each; with `typed` each escape names an entry of an array of `10`<sub>h</sub>-byte arguments,
type 1 a number and type 2 a string (for example `002B4ADA`-`002B4AFF`).

| Escape | Becomes |
|---|---|
| `0F +` | `0F + 81` and the argument's byte, a render-state code |
| `0F ,` | the 7-byte colour code `0F )` of the argument's RGBA |
| `0F -` | the number in glyph codes (`002B3770`) |
| `0F 1` | the string argument, padded with `01`<sub>h</sub> blanks to the escape's minimum length; with a field width w it sits between a tab code `0F 2` that stores the pen position and one that moves to it plus 2 x w |
| `0F l` | with `typed`: a number, or for 1 the string argument's variant (`002B58B0`) |
| `0F m` | with `typed`: a word row's singular, or for a count above 1 its plural (below) |
| `0F n` | with `typed`: variant `k + 2` of a word row; for language ids 1-6 and 9 (`00254A10` answers 0) its first letter is capitalised when nothing has been written before it |

Any other unit is copied. A result that does not fit ends `out` at `size - 1` and returns `FFFF`<sub>h</sub> (`002B51C3`).
`002B58B0(row, k)` returns string `k` of a word row ([battle text tables](../Game-Files-And-Data-Tables/battle-text-tables.md)).

`002B4550(size, out, row)` builds a plural: string 1 of the row is the plural template and string 0 the base word.
Token `08`<sub>h</sub> with a two-byte count `& 7FFFh` copies that many bytes of the base word, token `09`<sub>h</sub> the whole word, and
anything else is copied (`002B45E3`-`002B46A2`).

`002B3770(size, out, &pos, value, digits, pad, fullwidth, space)` writes a number with `003EFD00` and turns each digit
into the font's glyph code through the font sheet's first character map, or the second with `fullwidth`; a digit the
map gives 0 becomes the blank token 7, or 1 with `fullwidth`, and `space` adds a final `04`<sub>h</sub> ([Fonts](fonts.md)).

Three writers build codes for menu strings:

- `002AB870(size, out, rgba)` writes the colour code `0F )`, 8 bytes with its terminator, the same encoding as the
  `0F ,` arm;
- `002AC2C0(n)` returns the static code `0F ? 81 n` at `01E0CDFC`;
- `002B5240(record)` copies a string, replacing each `0F 8` with the name it stands for (`002639E0`), and
  `002B5680(size, out, in)` copies one without its line breaks `02`<sub>h</sub> and baseline codes `0F <`.

### Two-byte number templates

Some screens fill a template of two-byte units that starts with the bytes `ex`. `00365B30(size, out,
template, args)` forwards to `00365B50`, which copies the 4-byte head and then each unit. A unit `{` followed
by `i` is a 4-unit escape whose low bytes give a field width and flags. It takes the next 8-byte argument as
an integer and writes it through `00365E50`.

`00365E50(out, value, width, zeros, length)` writes the digits as units `'0'` + d. With a width it pads them
on the left with `01`<sub>h</sub> blanks; with `zeros` it starts with `02`<sub>h</sub>, pads with `'0'` units and marks the first
significant digit with `03`<sub>h</sub>. It returns the digit count and the byte length through `length`.

`0029CC00(id, n)` fills the template of text id with n (at least 0) into the next of eight 32-byte buffers
at `0209C390`, rotating through `01E0C560`, and `0029CC70(out, id, n)` into the caller's buffer; an id below
100,000 is read with `002F9860`, a larger one with `002F9920(id - 100000)`. `0029CB80(id, arg)` does the same
with the formatter `002B4090` instead; the magick and equipment description builders use it.

`00365B50` returns the length written plus 2, or 0 when the template lacks the head or the result does not
fit. Its callers include `0029FF60`, `002D66D0`, `002D7A90`, `00407450`, `00407720` and `0055BAC0`.

### Description lines

`00292B70(out, entry)` writes the description line of a list entry, `{kind, id in the high word}`, into a
`1F8`<sub>h</sub>-byte buffer. It takes the kind's template from `00295C20`, runs the kind's handler from the 16-entry
table `01E0C490`, closes the gaps in the argument list and formats it (`002B4090`). The shops (`0057BEE0`), the
equip list (`003FCEE0`), `00293170` and `00564430` call it.

Three kinds are narrowed first:

- kind 3, equipment: ammunition (`002CCA00`) becomes 2; otherwise the row's `+4C`<sub>h</sub> gives 1 for 0, 3 for 1,
  4 for 2 and 3, and 5 for 4, the mapping `00292F60` also gives the equip menu (`003FF920`);
- kind 6 with an id from `4000`<sub>h</sub> to `4017`<sub>h</sub> (`002CCB00`) becomes 7;
- kind 10 needs an id from `8060`<sub>h</sub> to `81FF`<sub>h</sub>.

| Kind | Handler | What it reads |
|---|---|---|
| 1 to 5 | `00295900`, `00295390`, `00294B50`, `00293FE0`, `00293310` | equipment by slot: weapon, ammunition, off hand, head and body, accessory |
| 6 | `00294860` | a magick: class 8, its action row (class 20), the school name (class 24), the action's `+24`<sub>h</sub>, a text from `4B27`<sub>h</sub> plus the lowest set bit of the action's byte `+30`<sub>h</sub> (`232D`<sub>h</sub> when it is 0), and `002960B0` |
| 7 | `002957C0` | a technick: class 9 and its action row's description, and `002960B0` |
| 8 | `00293E10` | an item: class 5 and its action row's description, with the same `4B27`<sub>h</sub> text |
| 9, 10, 12, 14, 15 | `00293F40`, `00294AB0`, `00295720`, `002956B0`, `002947F0` | the description `+10`<sub>h</sub> of class 7, 13, 11, 26 or 18: loot, key items, gambit conditions, statuses, bazaar goods |

`00293CE0(list, bits, text, count, n, flag)` adds to an argument list a text `4B27`<sub>h</sub> + b for each set bit b
of a byte, with `text` before or after them depending on the language (`00254A10`, `00264150`); the kind 3, 4
and 5 handlers use it.

### Codes no shipped text uses

Over every string of the nine languages, these never appear:

- the tokens `06`<sub>h</sub>, `07`<sub>h</sub>, `0B`<sub>h</sub>, `0C`<sub>h</sub> and `0D`<sub>h</sub>;
- the escapes `"`, `#`, `0`, `6`, `:`, `V` and `_`;
- the icon letters `\`, `]`, `b`, `d`, `f`, `h`, `i` and `j`.

The page wait `0F #` is therefore never used; every shipped wait for the confirm button comes from `03`<sub>h</sub>.

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
The 14,652 credits strings in `menu03.bin` are UTF-16 (tag `ex00`, written by `00365660`) and hold no codes. Event
script section 2 holds 949,262 of the 1,083,172 codes other than the space in the `total` column (87.6%).

Sixteen strings in `evt_t0080.ebp` and `evt_t0086.ebp` of the `ch`, `cn`, `in` and `kr` trees hold choice lists
whose option lengths do not fit the 7-bit field. The interpreter masks the length the same way (`002AC946`), so it
reads past those options; their codes are counted separately.

## Columns

| Column | Meaning |
|---|---|
| `code` | the token byte, or `0F` and the selector byte |
| `char` | the selector as a character; `space` and `quote` stand for `20`<sub>h</sub> and `22`<sub>h</sub> |
| `arm` | the address the jump table sends the code to |
| `parser` | the payload parser the arm calls, or `none` |
| `bytes` | the whole code's length, `0F`<sub>h</sub> and selector included |
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
