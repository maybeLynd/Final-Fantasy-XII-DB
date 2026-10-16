---
title: "Third-party libraries: which libraries are linked into the executable, how each is identified and versioned, and where each lies"
kind: "reference"
category: "Third-party libraries"
addresses: "01CBA5D0, 01CDB290, 0016F080, 01CEB590, 01F48940, 00D86C00, 00791D80, 00791E70, 00169620, 008B7DA0, 01F40380, 02EA58C0, 02EA54F0, 0080C5A0, 0080C5C0, 0087AF40, 01CC9F50, 01CDA260, 01CCA080, 00200BF0, 00200E60, 001FF740, 008C5F58, 0080E600, 002165B0"
---

## What it lists

One row per third-party library compiled into `FFXII_TZA.exe`, in address order: its name, the
version where the binary states one, the text or table that identifies it and where that sits, its
address span, how many functions its member list holds, and what the game uses it for. The data is
`third-party-libraries.tsv` beside this page.

Every row is identified by something the library itself put in the image: a version banner, the
library's own C++ namespace in RTTI type names, its default file names or allocator names, or a
constant table and header compare that only that library has.

The list is bounded by a scan of every
section of the image, ASCII and UTF-16, for the markers of other common libraries: libpng, libjpeg,
FreeType, OpenSSL, libcurl, libxml2, expat, TinyXML, pugixml, RapidJSON, cJSON, Theora, Opus, FLAC,
FMOD, Wwise, Bink, Havok, PhysX, Box2D, SDL, LZ4, zstd, LZMA, Boost, protobuf, SQLite and PCRE. None
of them occurs.

Three things are left out on purpose:

- PhyreEngine, the engine the game is built on, which has its own category.
- The Microsoft C/C++ runtime the compiler links in.
- `steam_api64.dll` (`01DEC066`), which the game loads as a DLL rather than linking.

No part of libxml2 is linked: `libxml`, `xmlParse`, `xmlFree` and `XML_PARSE` all occur zero times
in the image.

## Columns

| Column | Meaning |
|---|---|
| `library` | the library, and the part of it when the linker placed parts apart |
| `version` | the version the binary states; empty when the image carries none |
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
| versions stated in text | zlib 1.2.11 (`01CC9F50`, `01CDA260`), Lua 5.2.1 (`01CCA080`), libvpx VP8 decoder 1.6.0 (`01CEB698`), CRI HCA decoder 2.05.00 (`01CBA5D0`) |
| version from code shape | libvorbis: `_book_maptype1_quantvals` (`00882850`) has no guard against zero entries and no overflow test, both added in libvorbis 1.3.6 |
| no version in the image | Bullet, Tremor, libogg, libwebm, JsonBox, Dear ImGui, YEBIS / PPFX, EASTL |
| upstream build dates in text | CRI HCA "Build:Jul 31 2015 16:45:20"; PPFX diagnostics carry "Feb 18 2016" |

The decoders, the post-effect library and the physics and script libraries each have their own page
in this category; the rest of this section covers the three small libraries.

### zlib

The two banners are unreferenced constants, ` inflate 1.2.11 Copyright 1995-2017 Mark Adler `
(`01CC9F50`) and ` deflate 1.2.11 Copyright 1995-2017 Jean-loup Gailly and Mark Adler `
(`01CDA260`). The linker placed the library in two ranges:

- The inflate side, from `0080C5A0`. `0080C5A0` is zlib's `uncompress`: it passes the address of
  its source-length argument to `uncompress2` (`0080C5C0`, call at `0080C5AE`). `inflate` loads
  "incorrect header check" (`01CC7C58`) at `0080C9AD`.
- The deflate side, from `0087AF40`, which is `compress2`; it hands `deflateInit_` the
  `58`<sub>h</sub>-byte stream size (`0087AF7B`).

The checksum is zlib's table-driven CRC-32: `crc32` (`0080E5F0`) jumps to `crc32_z` (`0080E910`),
which returns 0 for a null buffer and otherwise jumps to `crc32_little` (`0080E600`). That body
reads the table at `01CC7E70` (`00000000`, `77073096`, ...). Its callers are zlib functions of the
second range, `0087BD60` and `0087CA60`.

Only three places outside zlib call it. The archive block reader `0019AA20` and the save reader
(call at `00865DFB`) call `uncompress`; the save writer calls `compress2` (`0086646C`).

### JsonBox

The JSON library is identified by its namespace in three RTTI type names,
`JsonBox::OutputFilter<VSolidusEscaper>`, `<VIndentCanceller>` and `<VIndenter>` (`01F48940`,
`01F48990`, `01F489E0`), and by the parser's error texts at `00904FE8` to `00905038` ("Expected
'\"', got '", "' instead, ignoring it.", "Expected a digit"), which only `002008F0`, `00201890`,
`00201C40` and `00201EB0` load.

This copy keeps its strings and containers in EASTL:

- `001FF740`, the lookup by C string, builds an EASTL string (allocator name "EASTL basic_string")
  from the key and calls the string lookup `001FF6B0`.
- The value parser `00200E60` reads one character and builds an object as an "EASTL map" on `{`
  and an array as an "EASTL vector" on `[`.

`00200BF0(value, path)` is the file reader the game uses: it opens the path through the engine's
file stream (`00597970`), copies the whole file into memory, wraps it in a string stream and parses
it with `00200E60`.

The writer's `SolidusEscaper` filter is `002165B0`. The overflow slot of
`OutputFilter<SolidusEscaper>` (`002016F0`, vtable `00905070` slot 3) passes it the filter's two
state bytes at `+70`<sub>h</sub>, the target stream buffer and the character:

- a `"` not preceded by a backslash toggles the in-string byte;
- a `/` inside a string, not preceded by a backslash, is written as the two characters `\/`, from
  the static string `01FD4058` that the start-up initialiser `0015FEF0` fills;
- an unescaped backslash inside a string sets the escaped byte for the next character; every other
  character clears it. Every character but a replaced `/` is written unchanged (`sputc`).

Every call into JsonBox from outside it comes from the game's JSON readers
(`001C2F50` to `001CCB20`), a few static initialisers and unwind code. What the game reads with it
is on [Standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md).

### Dear ImGui

`00791D80` is Dear ImGui's `ImGuiIO` constructor: it clears `B88`<sub>h</sub> bytes and stores ImGui's
default settings.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `f32[2]` | -1.0, -1.0 | display size, unset |
| `08`<sub>h</sub> | `f32` | 1/60 (`3C888889`<sub>h</sub>) | frame time |
| `0C`<sub>h</sub> | `f32` | 5.0 | ini saving interval |
| `10`<sub>h</sub> | `char*` | "imgui.ini" | `01CB3990` |
| `18`<sub>h</sub> | `char*` | "imgui_log.txt" | `01CB39A0` |
| `20`<sub>h</sub> | `f32` | 0.3 | double-click time |
| `24`<sub>h</sub> | `f32` | 6.0 | double-click distance |
| `78`<sub>h</sub> | `void*` | 02EA54F0 | the default font atlas |
| `80`<sub>h</sub> | `f32` | 1.0 | font scale |
| `A0`<sub>h</sub> | `fn*` | 00796E70 | default platform callback |
| `A8`<sub>h</sub> | `fn*` | 00798D70 | default platform callback |
| `B0`<sub>h</sub> | `fn*` | malloc |  |
| `B8`<sub>h</sub> | `fn*` | free |  |
| `C0`<sub>h</sub> | `fn*` | 00797360 | default platform callback |

The ImGui context is the static object `02EA58C0`:

1. The static initialiser `00169620`, whose pointer is at `008C4910` in the initialiser table, calls
   the context constructor `00791E70` on it and registers `008B7DA0` to run at exit. `00791E70`
   runs `00791D80` on the context's `+08`<sub>h</sub> and `00792090` on its `+B90`<sub>h</sub>.
2. `00169600` registers `008B7D40` at exit for the font atlas `02EA54F0`.
3. At exit `008B7DA0` frees the context's buffers (`00793140`), and `008B7D40` clears the atlas
   (`00795FC0`), both through the free function the context holds.

The pointer `01F40380` holds the context's address. Only ImGui's own functions (`00793140`,
`00795F10`, `00795FC0`, `007960E0`, `00796E70`, `00797360`) and the exit stubs `008B7B30` and
`008B7D40` read it. From outside the four ImGui runs, the only references to the context, the font
atlas or any ImGui function are `00169620` and the exit stubs.

A second ImGui object is built the same way. The initialiser `00169450` (slot `008C48C0`) constructs a
`PImGuiDynamicMesh` at `02EA5850` (`00662A50`, vtable `01CB3950`), and `001694E0` (slot `008C48D0`) builds
a `PDynamicMeshInstance` at `02EA5838` that holds its address (`005DBF60`). The exit stubs `008B7B60` and
`008B7B80` release them, and nothing else refers to either.

So the context is built before `main` and destroyed at exit, and nothing uses it in between: no code
begins an ImGui frame or window. ImGui's own window and identifier literals ("Debug##Default",
"##Tooltip", "#CLIPBOARD", "[Window][") do not occur in the image. The debug menu the game does have
is drawn by its own code, described on [Debug menu](../Engine-Core/debug-menu.md).

## Related

- [Standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md): the JSON
  documents JsonBox reads and the WebM movies the decoders play.
- [Bigfile archive](../Game-Files-And-Data-Tables/bigfile-archive.md): the archive blocks zlib
  inflates.
- [Save file format](../Saving-Loading-And-Settings/save-file-format.md): the zlib and RC4 layers of a
  save file.
- [Sound engine](../Sound-And-Music/sound-engine.md): the sound driver that calls the HCA decoder and Tremor.
- [Debug menu](../Engine-Core/debug-menu.md): the game's own debug overlay.
