[Home](../../README.md) / [Graphics](README.md) / Effect file list

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Effect file list: every effect file the game requests, by kind and id, with the actions, script verbs and models that use it and what it holds | reference | Graphics | Visual effects / Effect Files | All 2,051 effect files (.efx) the executable names, decoded row by row: the resource kind and id, the path and language folder, the size and whether the archive ships it, which voice and text languages use the copy, the event effect number and variant, what loads instead when the file is missing, the actions, script verbs, start-up builder or models that request it, and the chunk counts with their texture records. | 0x002DF9A0, 0x002FC860, 0x002FCFF0, 0x002DEBB0, 0x002DDE20, 0x0030A190, 0x00328360, 0x0042FCE0, 0x002FCBF0, 0x003B2310, 0x0036E320, 0x003576D0, 0x003B0660, 0x0019FFD0, 0x001A09E0 |

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
   `0x002DDE20` answers 0 when the pointer `0x0215E6E0` is null (`0x002DDE27`-`0x002DDE36`).
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
    49-51 with the id as a constant: the kind-7 requests are `0x00291C80` (ids `0x98` to `0xA1`,
    `0x00291CA1`-`0x00291D12`) and `0x002C8EE0` (ids `0x74` and `0x75`, `0x002C8F18`-`0x002C901C`), neither
    reading its argument, `0x0039C3F0` (id `0xD5`) and the font loaders.
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

Before the jump `0x0050F070` calls `0x0016D6A0`, a bare return, three times, with 7, `0xC`
and `0xB` (`0x0050F074`-`0x0050F08D`).

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
| `load_weight` | for kinds 11 and 38, the id's weight in the battle effect limits of 24 and 36 ([Effect file loading](effect-file-loading.md)): the low five bits of its byte at `0x01EEBB10` (`0x002FC200`), 0 for ids 401-511. All 401 source bytes have their top three bits clear, so the value is also the byte |
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

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x0032E400` is called by `0x0032FCA0`, `0x00330310`, `0x003306E0`; `0x0032E520` is called by `0x002628B0`;
  `0x0032E620` is called by `0x0032FCA0`, `0x00330310`; `0x003B8670` calls `0x00265020`, `0x0026A430`, `0x002EB740`, `0x003588B0`.
- Actor entity: those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md),
  [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md),
  [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md),
  [force fight mode](../Engine-Core/force-fight-mode.md).
- Actor entity: and on [debug menu](../Engine-Core/debug-menu.md),
  [party verbs](../Scripts-And-Script-Commands/party-verbs.md),
  [ko and game over](../Status-Effects-And-KO/ko-and-game-over.md).
- Audio: `0x002DDE20` is called by `0x002DF460`, `0x002DF4D0`; `0x002DEBB0` is called by `0x003E9B10`, `0x003E9C10`, `0x003EA430`,
  `0x003EA540`; `0x002DF070` calls `0x001DBE60`; `0x002DF070` is called by `0x003635E0`; `0x003B8670` calls `0x002DF660`,
  `0x003B3EA0`, `0x003B99D0`; `0x00504060` calls `0x002DF070`, `0x003D7CE0`, `0x003D7F30`.
- Audio: those functions are documented on [animation sounds](../Sound-And-Music/animation-sounds.md),
  [audio manager](../Sound-And-Music/audio-manager.md), [voices](../Sound-And-Music/voices.md),
  [mpk map pack](../World-Areas-And-Travel/mpk-map-pack.md),
  [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md).
- Audio: and on [character effects](character-effects.md),
  [effect anchors and targets](effect-anchors-and-targets.md), [sound banks](../Sound-And-Music/sound-banks.md).
- Combat action: `0x0030A190` is called by `0x0030C890`, `0x0030CBE0`; `0x0030CBE0` calls `0x00306B10`, `0x003098D0`, `0x0030A190`,
  `0x0030C890`, `0x0030CE10`; `0x00328360` is called by `0x0030CBE0`; `0x0032E520` is called by `0x002FC3C0`.
- Combat action: those functions are documented on [action phases](../Battle-Actions/action-phases.md),
  [frame update order](../Engine-Core/frame-update-order.md),
  [action definition row](../Battle-Actions/action-definition-row.md),
  [battle units](../Characters-And-Objects/battle-units.md).
- Combat action: and on
  [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md).
- Core runtime: `0x00259180` is called by `0x0022A0B0`; `0x002DF9A0` is called by `0x0022A0B0`; `0x0032E520` is called by
  `0x0022B6E0`, `0x0022B7E0`; `0x003B8670` calls `0x001EDDA0`.
- Core runtime: those functions are documented on [game application](../Engine-Core/game-application.md),
  [frame update order](../Engine-Core/frame-update-order.md),
  [global state accessors](../Engine-Core/global-state-accessors.md).
- Gameplay: `0x0030CBE0` calls `0x00322C50`; those functions are documented on
  [identifier spaces](../Engine-Core/identifier-spaces.md).
- Input: `0x00267310` is called by `0x002E09A0`; `0x0032E620` is called by `0x00291C80`; those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md),
  [startup constants](../Engine-Core/startup-constants.md).
- Movement: `0x00267310` is called by `0x002E45E0`, `0x002E5750`; `0x003B8670` calls `0x0024B6F0`, `0x0024C6B0`, `0x0024C870`,
  `0x0024F9B0`, `0x00265200`, `0x0026AF80`, `0x0026B5A0`.
- Movement: those functions are documented on
  [facing and steering](../Movement-And-Pathfinding/facing-and-steering.md),
  [time stop and freeze](../Engine-Core/time-stop-and-freeze.md),
  [heading speed to position delta](../Movement-And-Pathfinding/heading-speed-to-position-delta.md).
- Movement: and on [effect anchors and targets](effect-anchors-and-targets.md),
  [party control modes](../Engine-Core/party-control-modes.md),
  [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md).
- Party: `0x0030CBE0` calls `0x0031B7E0`; those functions are documented on
  [identifier spaces](../Engine-Core/identifier-spaces.md).
- Platform: `0x001A0AF0` calls `0x005CD0A0`; those functions are documented on
  [game application](../Engine-Core/game-application.md).
- Resource: `0x0019F620` calls `0x0019F490`; `0x0019F620` is called by `0x001A11B0`; `0x001A09E0` is called by `0x001A0CF0`,
  `0x001A0E50`, `0x001D6EC0`; `0x001A0AF0` calls `0x0019FFD0`, `0x001A1050`; `0x001A0AF0` is called by `0x0019F620`; `0x001A0CF0`
  calls `0x00597970`, `0x00598100`, `0x0059BD40`, `0x0059D920`, `0x0059F4A0`, `0x0059FBA0`; `0x001A0E50` calls `0x00597970`,
  `0x00598100`, `0x0059BD40`, `0x0059D900`, `0x0059F4A0`, `0x0059FBA0`.
- Resource: `0x001D6EC0` calls `0x001A1220`; `0x001D6EC0` is called by `0x002DF8E0`, `0x00409FE0`; `0x00291C80` calls `0x0032E620`;
  `0x002C8EE0` calls `0x0032E620`; `0x002FC860` calls `0x0032E400`, `0x0032E620`; `0x002FCFF0` calls `0x0032E400`; `0x0032E400` is
  called by `0x00249210`, `0x0024AC30`, `0x00259DF0`, `0x00379E90`, `0x00384420`, `0x0039C3F0`, `0x003EADE0`, `0x0051ED10`; `0x0032E520`
  calls `0x0032E070`, `0x0046DFE0`.
- Resource: `0x0032E520` is called by `0x0024AC30`; `0x0032E620` calls `0x0032E870`; `0x0032E620` is called by `0x00249210`,
  `0x0024AC30`, `0x00259DF0`, `0x00324510`, `0x0032EB40`, `0x00379E90`, `0x00384420`, `0x0039C3F0`, `0x0051ED10`; `0x0039C3F0` calls
  `0x0032E400`, `0x0032E620`; `0x003B0660` calls `0x0032E400`, `0x0032E520`, `0x0032E620`; `0x003B2310` calls `0x0032E400`,
  `0x0032E620`.
- Resource: those functions are documented on
  [async load manager](../Game-Files-And-Data-Tables/async-load-manager.md),
  [game application](../Engine-Core/game-application.md),
  [resource ownership and disposal](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md).
- Resource: and on [file path resolution](../Game-Files-And-Data-Tables/file-path-resolution.md),
  [bigfile archive](../Game-Files-And-Data-Tables/bigfile-archive.md),
  [debug menu](../Engine-Core/debug-menu.md),
  [startup constants](../Engine-Core/startup-constants.md).
- Resource: and on [battle text tables](../Game-Files-And-Data-Tables/battle-text-tables.md),
  [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md),
  [authored data tables](../Game-Files-And-Data-Tables/authored-data-tables.md).
- Resource: and on [frame update order](../Engine-Core/frame-update-order.md),
  [ard area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md).
- Save load settings: `0x0032E620` is called by `0x002EF300`; those functions are documented on
  [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md).
- Script VM: `0x00267310` is called by `0x0033F330`, `0x00340260`, `0x00340FA0`, `0x00341590`, `0x00341710`, `0x00341F50`,
  `0x00342770`, `0x003428C0`, `0x00342F80`, `0x003435C0`, `0x003436B0`, `0x00343A30`; `0x00267310` is also called by `0x00343B00`,
  `0x00343C60`, `0x00343F10`, `0x00344340`, `0x003445E0`, `0x00344660`, `0x00344F00`, `0x00345010`, `0x00345930`, `0x00345B60`,
  `0x00346260`, `0x00346C00`.
- Script VM: `0x00267310` is also called by `0x00347B00`, `0x003486A0`, `0x0034A1D0`, `0x0034A530`, `0x0034A600`, `0x0034AB50`,
  `0x0034AC30`, `0x0034B3C0`, `0x0034B7C0`, `0x0034BBD0`, `0x0034C210`, `0x0034C570`; `0x00267310` is also called by `0x0034CA40`,
  `0x0034DCC0`, `0x0034E630`, `0x0034E8B0`, `0x0034EE40`, `0x0034EF60`, `0x00350700`, `0x00350EC0`, `0x00353260`, `0x00353D90`,
  `0x00354300`, `0x00354800`.
- Script VM: `0x00267310` is also called by `0x003549D0`, `0x00355160`, `0x00355300`, `0x003563D0`, `0x00356990`, `0x00357040`,
  `0x003576D0`, `0x003581B0`; `0x002DEBB0` is called by `0x0034B650`; `0x00314D40` is called by `0x0033F330`, `0x003409F0`,
  `0x00340FA0`, `0x00341710`, `0x00341840`, `0x003418B0`, `0x00341F90`, `0x00342770`, `0x00342F50`, `0x00344200`, `0x00344660`,
  `0x00345250`.
- Script VM: `0x00314D40` is also called by `0x003453D0`, `0x00346020`, `0x003466A0`, `0x00346AA0`, `0x003473A0`, `0x00347660`,
  `0x00347C60`, `0x00348870`, `0x003491B0`, `0x003492A0`, `0x003499C0`, `0x00349A30`; `0x00314D40` is also called by `0x0034A300`,
  `0x0034B120`, `0x0034B8D0`, `0x0034C320`, `0x0034CED0`, `0x0034D740`, `0x0034D8B0`, `0x0034E1F0`, `0x0034E3E0`, `0x0034E8B0`,
  `0x0034EE40`, `0x0034F770`.
- Script VM: `0x00314D40` is also called by `0x0034FB20`, `0x0034FE80`, `0x003523B0`, `0x00352E40`, `0x00353080`, `0x00353590`,
  `0x00353720`, `0x003541B0`, `0x00354690`, `0x00354920`, `0x00354A40`, `0x003550F0`; `0x00314D40` is also called by `0x00356050`,
  `0x00357300`, `0x003576D0`, `0x0050CB00`, `0x0050D0C0`, `0x0050D540`, `0x0050D710`, `0x0050E1E0`, `0x0050EA80`; `0x0032E400` is called
  by `0x0050DF70`.
- Script VM: `0x0032E520` is called by `0x0034DB30`, `0x0050D0C0`, `0x0050D9A0`, `0x0050E1E0`; `0x0032E620` is called by
  `0x0050DFE0`; `0x0034B880` calls `0x00267F90`, `0x003576D0`; `0x0034BC90` calls `0x00267E10`, `0x00267F90`, `0x003576D0`; `0x0034C0F0`
  calls `0x00267F90`, `0x003576D0`; `0x0034C430` calls `0x00267E10`, `0x00267F90`, `0x003576D0`; `0x0034C820` calls `0x00267F90`,
  `0x003576D0`.
- Script VM: `0x0034CB80` calls `0x00267E10`, `0x00267F90`, `0x003576D0`; `0x003576D0` calls `0x00267E10`; `0x003576D0` is called by
  `0x0034B880`, `0x0034BC90`, `0x0034C0F0`, `0x0034C430`, `0x0034C820`, `0x0034CB80`; `0x0036E320` is called by `0x003576D0`.
- Script VM: those functions are documented on
  [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md),
  [music table](../Sound-And-Music/music-table.md), [actor managers](../Characters-And-Objects/actor-managers.md),
  [effect files efx efb](effect-files-efx-efb.md), [music](../Sound-And-Music/music.md).
- Script VM: and on [script screen effects](script-screen-effects.md), [scripted camera](scripted-camera.md),
  [map sounds](../Sound-And-Music/map-sounds.md), [pkfl packages](../PKFL-Package-Files/pkfl-packages.md),
  [mpk map pack](../World-Areas-And-Travel/mpk-map-pack.md).
- Script VM: and on [small bin tables](../Game-Files-And-Data-Tables/small-bin-tables.md),
  [vibration](../Controls-And-Input/vibration.md),
  [character se tables chse](../Game-Files-And-Data-Tables/character-se-tables-chse.md),
  [native commands](../Scripts-And-Script-Commands/native-commands.md).
- Script VM: and on [voices](../Sound-And-Music/voices.md),
  [graphics settings](../Engine-Core/graphics-settings.md),
  [time stop and freeze](../Engine-Core/time-stop-and-freeze.md),
  [sound effects](../Sound-And-Music/sound-effects.md), [effects on actors and scripts](effects-on-actors-and-scripts.md).
- Script VM: and on [actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md),
  [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md),
  [ard area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md).
- Script VM: and on [chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md),
  [action phases](../Battle-Actions/action-phases.md),
  [resource ownership and disposal](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md),
  [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md).
- Script VM: and on [party verbs](../Scripts-And-Script-Commands/party-verbs.md),
  [party control modes](../Engine-Core/party-control-modes.md),
  [verb table](../Scripts-And-Script-Commands/verb-table.md),
  [event scenes](../Scripts-And-Script-Commands/event-scenes.md).
- Script VM: and on [ebp script container](../EBP-Script-Files/ebp-script-container.md),
  [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md),
  [debug menu](../Engine-Core/debug-menu.md).
- Script VM: and on [frame update order](../Engine-Core/frame-update-order.md),
  [force fight mode](../Engine-Core/force-fight-mode.md).
- UI: `0x002C8EE0` is called by `0x00253780`; those functions are documented on
  [as7 menu graphics](../Game-Files-And-Data-Tables/as7-menu-graphics.md).
- World area: `0x00314D40` is called by `0x00266D10`; `0x0032E400` is called by `0x00378540`; `0x0032E620` is called by
  `0x00378540`; those functions are documented on [force fight mode](../Engine-Core/force-fight-mode.md),
  [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md).
- World area: `0x00267310` is called by `0x00314020`; `0x0030CBE0` is called by `0x00234590`; `0x0032E400` is called by
  `0x00268750`, `0x003319D0`, `0x00378030`, `0x00379A10`, `0x003EA820`; `0x0032E520` is called by `0x003145E0`; `0x0032E620` is called
  by `0x00268750`, `0x00378030`, `0x003EA820`.
- World area: those functions are documented on [debug logging](../Engine-Core/debug-logging.md),
  [force fight mode](../Engine-Core/force-fight-mode.md),
  [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md),
  [frame update order](../Engine-Core/frame-update-order.md).
- World area: and on
  [resource arena and relocation](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md),
  [standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md),
  [item and ability ids](../Engine-Core/item-and-ability-ids.md); and on
  [changing areas](../World-Areas-And-Travel/changing-areas.md).
