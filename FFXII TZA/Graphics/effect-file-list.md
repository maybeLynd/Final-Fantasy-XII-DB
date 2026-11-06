---
title: "Effect file list: every effect file the game requests, by kind and id, with the actions, script verbs and models that use it and what it holds"
kind: "reference"
category: "Graphics"
addresses: "0x002DF9A0, 0x002FC860, 0x002FCFF0, 0x002DEBB0, 0x002DDE20, 0x0030A190, 0x00328360, 0x0042FCE0, 0x002FCBF0, 0x003B2310, 0x0036E320, 0x003576D0, 0x003B0660, 0x0019FFD0, 0x001A09E0"
---

## What it lists

[`effect-file-list.tsv`](effect-file-list.tsv) holds one line for each effect file the executable names: 2,051 rows over the
3,288 `.efx` files the archive ships under `ps2data/effect_finish/<folder>/`. A row is a resource kind
and id ([File size tables](../Game-Files-And-Data-Tables/file-size-tables-fst.md)), or a model
name for the character effects, which no kind names. The chunk layout the contents columns read is
on [Effect files](effect-files-efx-efb.md).

| Group | Rows | Shipped files | What they are |
|---|---:|---:|---|
| kind 10 | 3 | 2 | `c_all.efx`, the common bank every effect context can use, and `m_all.efx`; the third entry is the size-table path template `0x002DF9A0` formats, not an effect |
| kind 7, ids 49-51 | 3 | 3 | the menu banks `m_all.efx`, `m_all2.efx`, `m_all3.efx`, one copy per text language |
| kind 11 | 512 | 366 | the magic effects `m0000`-`m0511`, played with English voices |
| kind 38 | 512 | 366 | the same ids played with Japanese voices |
| kind 12 | 896 | 534 | the event effects a zone script loads by number: `e` 0-511 (ids 0-511), `l` 0-63 (ids 512-575) and `q` 0-319 (ids 576-895); ids 677 and 678 (`q0101`, `q0102`) are named by the JP, KR, CH, ASIA, IN and CN arrays and are empty in the US, FR, DE, IT, ES and UK ones |
| character effects | 125 | 125 | `h0001`-`h0125` in `jp/chara`, bound to 144 model names: 82 monsters (`m`), 27 NPCs (`n`), 9 gadgets (`g`) and 26 summons (`s`); 14 of the files serve more than one model |

Kinds 10, 11 and 38 use one path array for every language. Kind 12's array differs by text
language: 314 of the 534 shipped event effects have per-language copies (`us`, `fr`, `de`, `it`, `es`,
`kr`, `ch`, `cn`), the other 220 are the `jp` file for everyone, and the `text_languages` column lists
which copy each locale id takes. The magic effects are chosen by the voice language instead: the
kind-11 array names `us` copies for 43 ids (the 18 Quickening cinematics 120-137 among them) and `uk`
copies for 8, while kind 38 names `jp` copies for those 43 and keeps the same `uk` and `in` copies.

### Where the values come from

The columns come from the path arrays, the US size table, the archive index and the files:

1. The path arrays: `0x002DF9A0` installs one array per kind at `0x0215F000 + 8 x kind`, then a switch
   on the locale id replaces kind 12's (and kind 7's) with the language's own; the arrays of every
   locale id 0 to 11, named `JP US FR DE IT ES UK KR CH ASIA IN CN` as the size-table loader names
   them, are listed. Entry n of an array is the path of id n.
2. The size is the US `FileSizeTable_US.fst` entry `kind x 5000 + id`; `ships` is whether the archive
   index names the path; the contents come from the extracted file.
3. The contents: a walk of the chunk stream from `+0x10` (length `+0x00`, type `+0x06`) counts the
   chunks by type, the `0xB00` records by kind (`+0x0E`) and the element types of the `0xA00`
   records (`+0x0E`), and lists each kind-`0x52` texture record that is not empty: width and height
   from the payload words `+0x08` and `+0x0A`, the format from the low six bits of its first byte and
   the palette count from byte `+0x02`, as `0x00500C00` reads them.
4. The actions: `0x0030CBE0` runs every frame and asks `0x0030A190(row)` for the effect to load: the
   row's `+0x24`, or its cinematic id `+0x28` for rows `0xD0`-`0xF1` (the Quickenings and
   Concurrences) while the battle state `0x022C2160` is 5 or 6; `0xFFFF`, bit `0x8000` or flag `+0x0C` bit `0x40000000`
   give no effect (`0x0030A213`-`0x0030A238`).
5. `0x00328360` passes the id to `0x0042FCE0`, which counts the start and calls `0x002FCBF0(id)`; that
   stores it at `+0x20` of a load record and runs `0x002FC860`. Effect programs load another effect
   the same way (`0x003B8670`, opcode `0x21`).
6. The magic kind: `0x002FC860` asks `0x002DEBB0`, which is 1 while bit `0x400` of the options record
   `*0x0215E6E0 + 4` is clear (`0x002DDE20`), the English voice setting ([Voices](../Sound-And-Music/voices.md)):
   kind `0x0B` then, kind `0x26` with Japanese voices.
7. It sizes the id (`0x0032E400`) and, when there is no file, loads id 120 for ids 120-137, id 138
   for 138-153 and id 0 otherwise (`0x002FC8E4`-`0x002FC911`), then requests it (`0x0032E620`, completion
   `0x002FC830`). `0x002FCFF0` sizes all 512 ids in the same kind into the load-cost table `0x02EC19C0`,
   storing each size as it comes, without the fallback (`0x002FD015`-`0x002FD02F`).
8. The event effects: the verbs `effectread` `0x0DB` and `effectread_e0` `0x0E0` pass variant 0,
   `locationeffectread` `0x127` and `0x128` variant 1, `questeffectread` `0x1DA` and `0x1DB` variant
   2 (`0x0034BC90`, `0x0034B880`, `0x0034C430`, `0x0034C0F0`, `0x0034CB80`, `0x0034C820`) to `0x003576D0`.
9. `0x003576D0` calls `0x0036E320(manager, slot, number, variant)`, where variant 1 adds `0x1000` and
   variant 2 `0x2000` to the number (`0x0036E351`-`0x0036E36D`). `0x003B2310` turns that into the id:
   `0x1000` becomes number + `0x200`, `0x2000` number + `0x240`, bit `0x8000` gives `0x1FF`, and number
   `0xC3` gives `0x1FE` with Japanese voices (`0x003B2343`-`0x003B2391`).
10. `0x003B2310` then sizes kind `0x0C`, falls back to `0x200` or `0x240` for the two variants when
    there is no file (`0x003B23B0`-`0x003B23C7`), and requests it (completion `0x003B22D0`).
11. The common bank: the type-5 context builder `0x003B0660`, run at start-up by `0x00259180`, sizes and
    requests kind 10 id 0 (`0x003B06E5`, `0x003B070D`). No site requests kind 10 id 1 or kind 7 ids
    49-51 with the id as a constant: the kind-7 requests are `0x00291C80`, which takes its id from `+0x98`
    of its argument, `0x002C8EE0`, from `+0x74`, `0x0039C3F0` (id `0xD5`) and the font loaders.
12. The character effects: `0x0019FFD0`, run once from `0x001A0AF0` (`0x0019F620`), stores 125 paths into
    144 slots of the `0x28000`-entry table at `+0x228` of its object; `0x001A09E0` reads the slot
    `letter x 0x500 + number` for a model name `<letter><number>` (`0x001A0A74`-`0x001A0A7F`), for
    `0x001A0CF0`, `0x001A0E50` and `0x001D6EC0`. The row's `requested_by` names those models.

In step 4, `0x0030A190(row)` answers -1 for a null row (`0x0030A199`). It takes the row's number in the
action table as the row's distance from the decoded base divided by the row size word, `n = (row - b) / w`,
with `T = [0x02EBF138]`, the decoded base `b = 0x0020E600([T + 0x0C])` and the size word `w = [T + 0x08]`, a 32-bit
unsigned `div` (`0x0030A1A2`-`0x0030A1F1`).

The cinematic id `+0x28` of rows `0xD0`-`0xF1` is returned untested while the battle state is 5 or 6:
`[row + 0x28]` when `n >= 0xD0`, `n <= 0xF1` and `[0x022C2160] - 5 <= 1` unsigned (`0x0030A1CB`-`0x0030A209`). The
three tests turn only the row's `+0x24` into -1: with `r = [row + 0x24]`, the answer is -1 when `r == 0xFFFF`,
when `[row + 0x0C] & 0x40000000` is non-zero or when `(int16)r < 0`, and `r` otherwise (`0x0030A213`-`0x0030A238`).

In step 5, `0x002FCBF0(id)` works under arena 8 (`0x0036C1D0(8, 10)` at `0x002FCC04`, `0x0036C140`). It returns 0
when the free list `0x02EC3D70` is empty (`0x002FCC13`). Otherwise it moves the first free record to the tail
of the active list `0x02EC3D60` / `0x02EC3D68` (links `+0x28` and `+0x30`, `0x002FCC15`-`0x002FCC56`).

It then raises the serial `0x02EC3D78` and puts `serial << 6` into the handle bits under mask `0x0FFFFFC0`,
clears the low five bits of `+0x23` and the context `+0x08`, and stores the id at `+0x20`
(`0x002FCC5A`-`0x002FCC7F`). It returns the handle `+0x00` after `0x002FC860` (`0x002FCCA7`). `0x002FC860` answers 1
on every path (`0x002FC876`, `0x002FC991`), so the branch that clears the state on 0 (`0x002FCC8C`) is never taken.

`0x002FC860(record)` first reads `0x02EC3D7C`: while a read runs it sets the state's low nibble to 1 and
returns 1 (`0x002FC866`-`0x002FC884`). Otherwise it keeps the size at `+0x1C`. With the load-cost table set
(`0x02EC3D7D`) it takes the size from `0x02EC19C0 + 8 x id`, and a size of 0 or less loads id 0 with entry 0's
size instead of the 120 and 138 ranges (`0x002FC8AD`-`0x002FC8C6`).

It then requests the id in kind `0x0B` or `0x26` into the buffer `[0x01FD4A30]`, with the record's handle
and the completion `0x002FC830`, stores the request at `+0x18`, sets state 2 and `0x02EC3D7C` to 1, and returns
1 (`0x002FC928`-`0x002FC996`).

`0x002FCFF0` asks `0x0032E400` for ids 0 to 511 in kind `0x0B`, or `0x26` when `0x002DEBB0()` is 0, stores
each answer at `0x02EC19C0 + 8 x id` and then sets `0x02EC3D7D` (`0x002FD015`-`0x002FD04A`). Its one caller is
the stub `0x0036DDB0`, the tail of `0x0050F070` (`0x0050F096`), the result callback of the debug verb
`debug_efffilesizecache` (`0x2062`), which only the developer menu script `bin/ctrl` calls
([Script verb table](../Scripts-And-Script-Commands/verb-table.md)).

In step 9, `0x003576D0` pops three values with `0x00267E10`, the variant, the number and the slot in that
order, and takes the first argument of `0x0036E320` from `+0x28` of `0x002640C0()` (`0x003576F3`-`0x00357717`).
It skips the call while the skip byte of the calling actor's manager (its byte `+0x15`) is set
(`0x00267310`, `0x0035771B`-`0x00357722`), and ends with `0x00314D40(1)` on both paths (`0x00357734`-`0x00357753`).

`0x0036E320(manager, slot, number, variant)` clamps the slot to 0-31, `s = slot < 0 ? 0 : slot > 31 ? 31 : slot`
(`0x0036E32C`-`0x0036E33D`), and works on the record `0x022D94B0 + 0x18 x s` (`0x0036E342`-`0x0036E34D`). It adds
`variant == 1 ? 0x1000 : variant == 2 ? 0x2000 : 0` to the number, so any variant other than 1 and 2 adds 0
(`0x0036E351`-`0x0036E36D`).

A record whose word `+4` is set is left as it is. Otherwise it clears `+0x10`, stores the handle
`0x003B1A80(number, slot)` at `+0x00` and the manager's low byte at `+0x08`, and sets `+4` to 1 when the handle is
non-zero (`0x0036E370`-`0x0036E396`).
The handle call takes the slot as passed, not the clamped `s`; `0x003B1A80` keeps `slot & 0x3F` of it (`0x003B1ADC`).

`0x003B2310(entry)` waits while another load runs (`0x02EBEBE4`): it sets the entry's state `+0x1C` to 1 and
returns 1 (`0x003B2316`-`0x003B2333`). Otherwise it writes the id back to `+0x04`. Only the two variants fall
back: any other number without a file returns 0 (`0x003B244F`), and a fallback is sized again until it
answers a size (`0x003B23CE`-`0x003B23E1`).

It then requests the id in kind `0x0C` into the buffer `[0x01FD4A30]`, which it keeps at `+0x28`, with the
entry's id and the completion `0x003B22D0`. It stores the request at `+0x18`, sets state 2 and `0x02EBEBE4`
to 1, and returns 1 (`0x003B23E3`-`0x003B2442`).

In step 11, `0x003B0660` works under arena 8, pushed twice and popped twice (`0x003B0671`, `0x003B06DB`,
`0x003B0752`, `0x003B075F`). It first zeroes `+0x00`, `+0x08` and `+0x11` and the low three bits of `+0x13`
of the 36 request entries at `0x02EBEC00`, clears bit `0x1` of `0x02EBEF68` and the qword `0x02EBEF60`, and
frees the instances of kinds 5, 6 and 9 (`0x0024C460`, `0x003B0676`-`0x003B06CE`).

When kind 10 id 0 has a size, `0x003B0660` reads it into `[0x01FD4A30]` without a request record and waits
for the read (`0x0032E520(0)`). It then builds the type-5 context from a zeroed `0x890`-byte template
(`0x0024B3A0`) and parses the stream (`0x003EDAD0`, `0x003B0712`-`0x003B0745`). With a size of 0 or less it goes
straight to the pops (`0x003B06EC`).

## Columns

| Column | Meaning |
|---|---|
| `kind`, `id` | the resource kind and id; `chara` and the lowest table slot for a character effect |
| `file`, `group`, `path`, `folder` | the file name, its `effect_finish` sub-folder (`common`, `menu`, `magic`, `event`, `chara`), the path as the executable writes it, and its language folder |
| `size`, `ships`, `archive_size` | the US size-table entry (empty when there is no entry), whether the archive holds the file, and the archive record's size |
| `voice_language` | which voice setting loads this kind: English (kind 11) or Japanese (kind 38); `any` otherwise |
| `text_languages` | for kinds 12 and 7, the folder each text language's array names for this id, grouped by folder; `jp: all` when every language takes the `jp` file |
| `effect_number` | for kind 12, the script's effect number and variant letter: `e n`, `l n` or `q n` |
| `fallback` | what loads when the file is missing: the substitute magic id, `l0000` or `q0000`, or a failed request |
| `requested_by` | the actions whose effect id or cinematic id is this id, the verbs and variant for an event effect, the start-up builder for the common bank, or the models bound to a character effect |
| `chunks` | the chunk counts by type, then the `0xB00` record counts by kind |
| `elements` | the `0xA00` element records by element type ([Effect element types](effect-element-types.md)) |
| `textures` | the count of kind-`0x52` texture records, then each as `width x height`, `f` format and `p` palette count |
| `sep_banks` | the six-digit sound banks the file's `SeSep` records name (in its mode-1 kind-`0x57` sound records, which `0x00504060` walks with `0x002DF070` when the record's id is first registered in `0x02EBBA00`), in order; a bank the archive lacks is marked |
| `explanation` | a one-line summary of the row |

## Related

- [Effect files (.efx, .efb): the effect containers, their chunk streams, the record kinds and the map effect bank](effect-files-efx-efb.md)
- [Effect element types: the handlers of every element type, what the verified types draw or change, and the kind-0x54 mesh record](effect-element-types.md)
- [Effect element runtime: instances, emitters and elements, the per-step update, birth, release, child spawns and timeline tracks](effect-element-runtime.md)
- [Effect file loading: the battle effect slots, the loaded-file queue, filing, sharing and releasing, and the battle effect program's state](effect-file-loading.md)
- [Action list: every attack, magick, technick, item use, summon, Quickening, Concurrence, Foecraft move and trap with its cost, power, element, statuses, area and texts](../Battle-Actions/action-list.md)
- [Action phases: delay, charge time, approach, execution and the end of a battle action](../Battle-Actions/action-phases.md)
- [File size tables: the per-language .fst that sizes every file by resource kind and id](../Game-Files-And-Data-Tables/file-size-tables-fst.md)
- [Voices: the voice packs a cutscene loads, the sixty-four voice slots, the English or Japanese choice, and the verbs that play, stop and pan a line](../Sound-And-Music/voices.md)
- [Script verb table: every call id with its name, callbacks, shape, argument count, what it reaches and how often the US scripts use it](../Scripts-And-Script-Commands/verb-table.md)
