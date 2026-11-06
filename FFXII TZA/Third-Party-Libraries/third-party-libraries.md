---
title: "Third-party libraries: which libraries are linked into the executable, how each is identified and versioned, and where each lies"
kind: "reference"
category: "Third-party libraries"
addresses: "0x01CBA5D0, 0x01CDB290, 0x0016F080, 0x01CEB590, 0x01F48940, 0x00D86C00, 0x00791D80, 0x00791E70, 0x00169620, 0x008B7DA0, 0x01F40380, 0x02EA58C0, 0x02EA54F0, 0x0080C5A0, 0x0080C5C0, 0x0087AF40, 0x01CC9F50, 0x01CDA260, 0x01CCA080, 0x00200BF0, 0x00200E60, 0x001FF740, 0x008C5F58, 0x0080E600, 0x002165B0"
---

## What it lists

One row per third-party library compiled into `FFXII_TZA.exe`, in address order: its name, the
version where the binary states one, the text or table that identifies it and where that sits, its
address span, how many functions its member list holds, and what the game uses it for. The data is
[`third-party-libraries.tsv`](third-party-libraries.tsv) beside this page.

Every row is identified by something the library itself put in the image: a version banner, the
library's own C++ namespace in RTTI type names, its default file names or allocator names, or a
constant table and header compare that only that library has.

The list is bounded by a scan of every
section of the image, ASCII and UTF-16, for the markers of other common libraries: libpng, libjpeg,
FreeType, OpenSSL, libcurl, libxml2, expat, TinyXML, pugixml, RapidJSON, cJSON, Theora, Opus, FLAC,
FMOD, Wwise, Bink, Havok, PhysX, Box2D, SDL, LZ4, zstd, LZMA, Boost, protobuf, SQLite and PCRE.
None of them occurs.

Three things are left out on purpose:

- PhyreEngine, the engine the game is built on, which has its own category.
- The Microsoft C/C++ runtime the compiler links in.
- `steam_api64.dll` (`0x01DEC066`), which the game loads as a DLL rather than linking.

No part of libxml2 is linked: `libxml`, `xmlParse`, `xmlFree` and `XML_PARSE` all occur zero times
in the image.

## Columns

| Column | Meaning |
|---|---|
| `library` | the library, and the part of it when the linker placed parts apart |
| `version` | the version the binary states; empty when the image states no version |
| `identified_by` | the text, type names or table that identify the library |
| `identity_address` | where the first of those sits |
| `span` | the address range of the member list, `first-last` inclusive; several ranges are separated by `;` |
| `members` | the number of functions in the member list |
| `members_file` | the member list: one function entry address per line |
| `used_for` | what the game does with the library |

## Data

| Fact | Value |
|---|---|
| libraries | 15 rows: CRI HCA decoder, libvpx (decoder and DSP kernels), libogg (`bitwise.c` and `framing.c`), JsonBox, YEBIS / PPFX, Dear ImGui, Tremor with `vorbisfile`, libwebm `mkvparser`, zlib, Lua, Bullet, libvorbis, EASTL |
| versions stated in text | zlib 1.2.11 (`0x01CC9F50`, `0x01CDA260`), Lua 5.2.1 (`0x01CCA080`), libvpx VP8 decoder 1.6.0 (`0x01CEB698`), CRI HCA decoder 2.05.00 (`0x01CBA5D0`) |
| version from code shape | libvorbis: `_book_maptype1_quantvals` (`0x00882850`) has no guard against zero entries and no overflow test, both added in libvorbis 1.3.6 |
| no version in the image | Bullet, Tremor, libogg, libwebm, JsonBox, Dear ImGui, YEBIS / PPFX, EASTL |
| upstream build dates in text | CRI HCA "Build:Jul 31 2015 16:45:20"; PPFX diagnostics carry "Feb 18 2016" |

The decoders, the post-effect library and the physics and script libraries each have their own page
in this category; the rest of this section covers the three small libraries.

### zlib

The two banners are unreferenced constants, ` inflate 1.2.11 Copyright 1995-2017 Mark Adler `
(`0x01CC9F50`) and ` deflate 1.2.11 Copyright 1995-2017 Jean-loup Gailly and Mark Adler `
(`0x01CDA260`). The linker placed the library in two ranges:

- The inflate side, from `0x0080C5A0`. `0x0080C5A0` is zlib's `uncompress`: it passes the address of
  its source-length argument to `uncompress2` (`0x0080C5C0`, call at `0x0080C5AE`). `inflate` loads
  "incorrect header check" (`0x01CC7C58`) at `0x0080C9AD`.
- The deflate side, from `0x0087AF40`, which is `compress2`; it hands `deflateInit_` the
  `0x58`-byte stream size (`0x0087AF7B`).

`0x0080C5C0(dest, destLength, source, sourceLength)` takes both lengths through pointers. A destination length of 0
makes it inflate into a one-byte stack buffer (`0x0080C5F1`, `0x0080C5F3`); otherwise it sets `*destLength` to 0
first (`0x0080C5ED`). It starts the stream with `0x0080E040` (version "1.2.11" at `0x01CC73A4`, size `0x58`,
`0x0080C622`) and returns that result when it is not 0 (`0x0080C629`). Then it calls `0x0080C750` with flush 0 until
the result is not 0 (`0x0080C67F`, `0x0080C688`), refilling the input and output counts from what is left.

Afterwards `0x0080C5C0` sets `*sourceLength -= left + availIn` (`0x0080C6A1`, `0x0080C6A3`), stores the output total
in `*destLength` for a real destination (`0x0080C6B0`) and ends the stream with `0x0080DF00` (`0x0080C6CB`). It
returns 0 for result 1, -3 for result 2, -3 for result -5 when `left + availOut != 0` (`0x0080C6D0`-`0x0080C6ED`;
`left` becomes 1 for the stack buffer once output was produced, `0x0080C6B5`-`0x0080C6C3`), and the result itself
otherwise (`0x0080C6EF`).

`0x0087AF40(dest, destLength, source, sourceLength, level)` sets `*destLength` to 0 (`0x0087AF63`) and starts the
stream with `0x0087C9F0(stream, level, "1.2.11", 0x58)` (`0x0087AF91`), returning a non-zero result as it is
(`0x0087AF98`). It calls `0x0087BD60` until the result is not 0 (`0x0087AFE7`, `0x0087AFF0`), with flush 4 once the
whole source is handed over and 0 before (`0x0087AFD7`-`0x0087AFE3`). It stores the output total in `*destLength`
(`0x0087B005`), ends the stream with `0x0087C6C0` (`0x0087B008`) and returns 0 for result 1, else the result
(`0x0087B00D`).

The checksum is zlib's table-driven CRC-32: `crc32` (`0x0080E5F0`) jumps to `crc32_z` (`0x0080E910`),
which returns 0 for a null buffer and otherwise jumps to `crc32_little` (`0x0080E600`). That body
reads the table at `0x01CC7E70` (`00000000`, `77073096`, ...). Its callers are zlib functions of the
second range, `0x0087BD60` and `0x0087CA60`.

Only three places outside zlib call it. The archive block reader `0x0019AA20` and the save reader
(call at `0x00865DFB`) call `uncompress`; the save writer calls `compress2` (`0x0086646C`).

### JsonBox

The JSON library is identified by its namespace in three RTTI type names,
`JsonBox::OutputFilter<VSolidusEscaper>`, `<VIndentCanceller>` and `<VIndenter>` (`0x01F48940`,
`0x01F48990`, `0x01F489E0`), and by the parser's error texts at `0x00904FE8` to `0x00905038` ("Expected
'\"', got '", "' instead, ignoring it.", "Expected a digit"), which only `0x002008F0`, `0x00201890`,
`0x00201C40` and `0x00201EB0` load.

This copy keeps its strings and containers in EASTL:

- `0x001FF740`, the lookup by C string, builds an EASTL string (allocator name "EASTL basic_string")
  from the key and calls the string lookup `0x001FF6B0`. `0x001FF6B0` first makes a value whose tag is not 3 an
  empty "EASTL map" (`0x001FF6CF`-`0x001FF713`), and `0x001FF4F0` inserts an entry with tag 6 for a key the map lacks
  (`0x001FF5E1`, `0x001FFD40`), so the lookup always returns a value; `0x001FF740` frees its string and returns it.
- The value parser `0x00200E60` reads one character and builds an object as an "EASTL map" on `{`
  and an array as an "EASTL vector" on `[`.

`0x00200BF0(value, path)` is the file reader the game uses: it opens the path through the engine's
file stream (`0x00597970`), copies the whole file into memory, wraps it in a string stream and parses
it with `0x00200E60`.

The writer's `SolidusEscaper` filter is `0x002165B0`. The overflow slot of
`OutputFilter<SolidusEscaper>` (`0x002016F0`, vtable `0x00905070` slot 3) passes it the filter's two
state bytes at `+0x70`, the target stream buffer and the character:

- a `"` not preceded by a backslash toggles the in-string byte;
- a `/` inside a string, not preceded by a backslash, is written as the two characters `\/`, from
  the static string `0x01FD4058` that the start-up initialiser `0x0015FEF0` fills;
- an unescaped backslash inside a string sets the escaped byte for the next character; every other
  character clears it. Every character but a replaced `/` is written unchanged (`sputc`). The filter
  returns what `sputc` returns (`0x00216641`), and 0 after a replaced `/` (`0x0021661E`, `0x00216649`).

Every call into JsonBox from outside it comes from the game's JSON readers
(`0x001C2F50` to `0x001CCB20`), a few static initialisers and unwind code. What the game reads with it
is on [Standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md).

### Dear ImGui

`0x00791D80` is Dear ImGui's `ImGuiIO` constructor: it clears `0xB88` bytes and stores ImGui's
default settings.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `f32[2]` | -1.0, -1.0 | display size, unset |
| `+0x008` | `f32` | 1/60 (0x3C888889) | frame time |
| `+0x00C` | `f32` |  | value 5.0: ini saving interval |
| `+0x010` | `char*` |  | value "imgui.ini": `0x01CB3990` |
| `+0x018` | `char*` |  | value "imgui_log.txt": `0x01CB39A0` |
| `+0x020` | `f32` |  | value 0.3: double-click time |
| `+0x024` | `f32` |  | value 6.0: double-click distance |
| `+0x078` | `void*` | 0x02EA54F0 | the default font atlas |
| `+0x080` | `f32` |  | value 1.0: font scale |
| `+0x0A0` | `fn*` | 0x00796E70 | default platform callback |
| `+0x0A8` | `fn*` | 0x00798D70 | default platform callback |
| `+0x0B0` | `fn*` | malloc |  |
| `+0x0B8` | `fn*` | free |  |
| `+0x0C0` | `fn*` |  | value `0x00797360`: default platform callback |
| `+0x0D0` | `f32[2]` | -1.0, -1.0 | mouse position, unset (`0x00791E0D`) |
| `+0x310` | `f32[2]` | -1.0, -1.0 | previous mouse position, unset (`0x00791E4B`) |

The ImGui context is the static object `0x02EA58C0`:

1. The static initialiser `0x00169620`, whose pointer is at `0x008C4910` in the initialiser table, calls
   the context constructor `0x00791E70` on it and registers `0x008B7DA0` to run at exit. `0x00791E70`
   runs `0x00791D80` on the context's `+0x08` and `0x00792090` on its `+0xB90`.
2. `0x00169600` registers `0x008B7D40` at exit for the font atlas `0x02EA54F0`.
3. At exit `0x008B7DA0` frees the context's buffers (`0x00793140`), and `0x008B7D40` clears the atlas
   (`0x00795FC0`), both through the free function the context holds.

Besides the two constructor calls, `0x00791E70` writes only the context's own fields, and every store is 0 but
two: -1 at `+0xE7C` (`0x00791FB8`) and 2 at `+0x38D4` (`0x00792062`). The zero stores include the byte `+0x00`
(`0x00791F88`) and three `memset` ranges through `0x00861EC0`: `0x24E0` bytes from `+0xFA8` (`0x00791F4B`), `0x400`
from `+0x34B0` (`0x00792032`) and `0x1E0` from `+0x38D8` (`0x00792072`). It returns the context (`0x00792077`).

The pointer `0x01F40380` holds the context's address. Only ImGui's own functions (`0x00793140`,
`0x00795F10`, `0x00795FC0`, `0x007960E0`, `0x00796E70`, `0x00797360`) and the exit stubs `0x008B7B30` and
`0x008B7D40` read it. From outside the four ImGui runs, the only references to the context, the font
atlas or any ImGui function are `0x00169620` and the exit stubs.

A second ImGui object is built the same way. The initialiser `0x00169450` (slot `0x008C48C0`) constructs a
`PImGuiDynamicMesh` at `0x02EA5850` (`0x00662A50`, vtable `0x01CB3950`), and `0x001694E0` (slot `0x008C48D0`) builds
a `PDynamicMeshInstance` at `0x02EA5838` that holds its address (`0x005DBF60`). The exit stubs `0x008B7B60` and
`0x008B7B80` release them, and nothing else refers to either.

So the context is built before `main` and destroyed at exit, and nothing uses it in between: no code
begins an ImGui frame or window. ImGui's own window and identifier literals ("Debug##Default",
"##Tooltip", "#CLIPBOARD", "[Window][") do not occur in the image. The debug menu the game does have
is drawn by its own code, described on [Debug menu](../Engine-Core/debug-menu.md).

The initialisers write these fields of the two statics directly:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EA5510` | `u8[16]` | 0 (zero-filled tail of `.data`) | `+0x20`-`+0x2F` of the font atlas `0x02EA54F0`, zeroed by the initialiser that registers the atlas's exit stub | `0x00169600` (`0x00169614`, one 16-byte store of 0.0 floats) | no instruction names it |
| `0x02EA5870` | `u32` | 0 (zero-filled tail of `.data`) | `+0x20` of the `PImGuiDynamicMesh` `0x02EA5850`: the count word of its array, `0x80000001`, one element the array does not own | `0x00169450` (`0x001694BD`) | `0x00169450` (`0x0016949D`, bit `0x80000000` tested before an old buffer is freed) |
| `0x02EA5878` | `void*` | 0 (zero-filled tail of `.data`) | `+0x28`: the array's buffer, the object's own `0x02EA5888`; `0x00169450` frees a different buffer through `0x00584730` when bit `0x80000000` of the count is clear | `0x00169450` (`0x001694B6`) | `0x00169450` (`0x0016948A`, compared with `0x02EA5888`, whose address it loads at `0x00169491`) |
| `0x02EA5888` | `u64` | 0 (zero-filled tail of `.data`) | `+0x38`: the first qword of the array's one element, 0 | `0x00169450` (`0x0016947C`) | no instruction names it |
| `0x02EA5890` | `u64` | 0 (zero-filled tail of `.data`) | `+0x40`: the second qword of that element, 0 | `0x00169450` (`0x00169483`) | no instruction names it |

The exit stub `0x008B7B60` puts back the vtable `0x01CB3950` and passes the object to `0x00663080`, and `0x008B7D40` passes
the atlas to `0x00795FC0`; neither stub names one of these fields.

### The clipboard copy and the solidus string

`0x00796E70` is Dear ImGui's default clipboard-text getter: `0x00791D80` stores its address at `ImGuiIO` `+0xA0`
(`0x00791DFC`). Each call:

1. frees the previous copy through the context's free function (`[0x01F40380] + 0xC0`, `0x00796E87`) and clears
   `0x02EACD78` (`0x00796E8D`);
2. opens the clipboard and takes its `CF_UNICODETEXT` (13) data with `OpenClipboard`, `GetClipboardData` and
   `GlobalLock`, and returns 0 when either of the first two fails;
3. allocates the text's UTF-8 length plus one through the context's allocator (`[0x01F40380] + 0xB8`, `0x00796F69`),
   stores the block in `0x02EACD78` (`0x00796F78`) and converts the text into it (`0x00797210`);
4. unlocks and closes the clipboard and returns `0x02EACD78` (`0x00796F9B`).

The `\/` that `SolidusEscaper` writes is the static string at `0x01FD4058`. `0x002165B0` passes its `begin` and
`end - begin`, computed on the low 32 bits (`0x00216604`, `0x0021660E`, `0x00216615`), to `sputn`.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EACD78` | `void*` | 0 (zero-filled tail of `.data`) | the UTF-8 copy of the clipboard text that `0x00796E70` returns; 0 when there is no copy | `0x00796E70`: 0 after the free (`0x00796E8D`), the new block (`0x00796F78`) | `0x00796E70`: the test before the free (`0x00796E74`) and the return value (`0x00796F9B`) |
| `0x01FD4060` | `void*` | 0 (zero-filled tail of `.data`) | `end` of the `\/` string `0x01FD4058` | its initialiser `0x0015FEF0` (`0x0015FF23`, `0x0015FF6E`, `0x0015FF9C`, `0x0015FFC0`) | `0x002165B0` (`0x00216604`, the low 4 bytes) |
| `0x01FD4068` | `void*` | 0 (zero-filled tail of `.data`) | `capacityEnd` of the `\/` string `0x01FD4058` | `0x0015FEF0` (`0x0015FF0E`, `0x0015FF7E`, `0x0015FFA3`) | its `atexit` destructor `0x008A8000` (`0x008A800D`) |

No other instruction reaches these globals: no other RIP-relative, image-base-relative or disp32 reference names
them, and no section holds a pointer to them. The other fields of the static strings are on
[EASTL strings and containers](eastl-strings-and-containers.md).

## Related

- [Standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md): the JSON
  documents JsonBox reads and the WebM movies the decoders play.
- [Bigfile archive](../Game-Files-And-Data-Tables/bigfile-archive.md): the archive blocks zlib
  inflates.
- [Save file format](../Saving-Loading-And-Settings/save-file-format.md): the zlib and RC4 layers of a
  save file.
- [Sound engine](../Sound-And-Music/sound-engine.md): the sound driver that calls the HCA decoder and Tremor.
- [Debug menu](../Engine-Core/debug-menu.md): the game's own debug overlay.
