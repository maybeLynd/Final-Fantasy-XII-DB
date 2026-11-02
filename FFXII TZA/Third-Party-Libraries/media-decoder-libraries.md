---
title: "Media decoder libraries: libwebm, libvpx VP8, libvorbis, Tremor, libogg and the CRI HCA decoder as the game uses them"
kind: "system"
category: "Third-party libraries"
addresses: "0x0067A480, 0x00679A50, 0x00679600, 0x006CCB00, 0x0016F070, 0x01CDB290, 0x01CDB320, 0x0016DEC0, 0x0016DFE0, 0x0016E040, 0x0016DDD0, 0x0016EE70, 0x0016F080, 0x00801210, 0x00803190, 0x008800C0, 0x00882AC0, 0x007F5970, 0x007F6750, 0x007F6280, 0x007F6730, 0x007BA7E0, 0x0017C890, 0x01CEB590, 0x00121DB0, 0x01CBA5D0, 0x01CBA610, 0x00679BF0, 0x006CC6A0, 0x006CC7C0, 0x0016FE80, 0x001294D0, 0x007FF1C0"
---

## What the player sees

The full-motion movies are WebM files: libwebm's `mkvparser` reads the container, libvpx decodes
the VP8 picture and libvorbis the sound track. Music, voices and sound effects come from the sound
banks, whose materials the sound driver decodes with the CRI HCA decoder or, for Ogg Vorbis
material, with Tremor and libogg. None of these libraries is the game's own code; each is linked in
whole or in part as its authors published it.

## How it works

### Opening a movie

`0x0067A480(player, path, flag)` opens a movie for the movie player `0x001B7F30` (call at `0x001B8029`).
It is `PVideoPlaybackWin32`'s open, the class its two thread names carry:

1. It counts the processors in the process affinity mask, or asks `GetSystemInfo` when the mask is
   empty, and builds the VP8 decoder configuration `{threads, 0x780, 0x438}` (1920 x 1080).
2. It starts the VP8 decoder: `0x0016DEC0` (`vpx_codec_dec_init_ver`) with the interface `0x0016F070`
   returns, that configuration, flags 0 and ABI version 10 (call at `0x0067A57D`).
3. It opens the file with the game's own `mkvparser::IMkvReader`, `0x006CCB00`, which reads through the
   engine's file stream (`0x00597930`).
4. It parses the container: the segment is created (`0x00801210`) and loaded (`0x00803190`), and each
   track is read from the track list (`0x008028E0`, `0x008028F0`, `0x00802880`).
5. A track of type 1 becomes the video track (`+0x478`). A track of type 2 becomes the audio track
   (`+0x480`) when its language equals "eng" (`0x00D6CDC0`) exactly as the player's flag `+0x538`
   asks (0 for English, 1 for another language), or when the file has fewer than three tracks.
   The loop does not stop at a match: with three or more tracks, the last audio track that passes
   the language test wins.
6. It reads the video's frame rate (`0x008024F0`, 29.97 when the file gives 0), width (`0x00802A00`),
   height (`0x00802500`) and duration (`0x008020D0`).
7. With an audio track it starts libvorbis (`0x00679A50`); when that fails the movie plays silent.
8. It starts the threads `PVideoPlaybackWin32::_VideoDecodingThread` (`0x0067A230`) and, with audio,
   `PVideoPlaybackWin32::_AudioDecodingThread` (`0x00679A40`).

What the movie files hold is on
[Standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md).

### Reading the movie's blocks

`0x00679ED0` loops until the player's `+0x258` is 1, waiting on the event at `+0x4F8`; while the play
state `+0x268` is 1 or 2 and `+0x25C` is not 2, it runs `0x00679BF0`, which reads the whole file:

1. It sets `+0x25C` to 1 and walks the clusters from the segment's first (`0x008022F0`, next with
   `0x008025B0`) and the blocks of each, stopping early when `+0x268` becomes 3.
2. A block whose track number names no track is skipped after a log line (`0x00D6CDA0`, through `0x0017D280`).
   A failed step to the next block logs "Error parsing next block of cluster" and returns.
3. Video blocks (type 1) always pass. Audio blocks (type 2) pass the same language test the open
   applies: language "eng" (`0x00D6CDC0`) matching flag `+0x538`, or fewer than three tracks.
4. Each frame of a passing block gets a slot in a queue, video at `+0x00` and audio at `+0x150` when
   the movie has an audio track (`+0x480`): `0x006CC6A0` reserves the frame length rounded down to
   16 plus 16 bytes, the reader's slot 0 (`+0x290`) reads the frame into the slot's data, and a
   read that returns 0 commits the slot (`0x006CC710`).
5. At the end it starts again from the first cluster when the byte `+0x26C` is set and the state is
   not 3. Otherwise it stops both queues (`0x006CC670`), sets `+0x25C` to 2 and signals `+0x508`.

### The frame queues

The player holds three `0xA8`-byte ring queues: compressed video at `+0x00`, decoded pictures at
`+0xA8` and compressed audio at `+0x150` (see Layouts). Each entry is a 16-byte header, the slot size
and the data length, followed by the data; an entry takes its slot size plus 16 bytes. One function
per step:

| Function | Step |
|---|---|
| `0x006CC6A0(q, size, length)` | writer: wait for room, write the header at the write offset, return it |
| `0x006CC710` | writer: commit; count the entry, move the write offset, signal the data event |
| `0x006CC4F0` | reader: wait for an entry and return its header |
| `0x006CC550` | reader: release; count it, move the read offset, signal the space event when the writer waits |
| `0x006CC7C0` | the shared wait: blocks on the queue's event (`0x005CD840`) until the end offset fits, wraps it at the capacity, and returns false once the queue is stopped |
| `0x006CC580` | entries waiting: written minus read, 0 while `+0x20` is clear |
| `0x006CC920` | waits on the space event and sets it again; false once the queue is stopped |
| `0x006CC670` | stop: clear `+0x48` and set both events, so every waiter returns |

The video work `0x0067A010` takes each packet from the first queue, passes it to `vpx_codec_decode`
(`0x0016DFE0`), releases it, and copies the three planes of every decoded image (`0x00679570`) into a
reserved slot of the picture queue. While that queue holds more than `+0x2F0` minus 3 pictures it
waits through `0x006CC920`. When the movie closes, `0x0067A9B0` closes the reader with `0x006CCA70`
(`0x0067AA59`), which closes the `0x30`-byte file stream at reader `+0x10` (`0x0059BD80`) and frees it.

### libwebm mkvparser

The container parser is identified by the RTTI of eight `mkvparser::` classes: `IMkvReader`
(`0x01F70C90`), `Track`, `BlockEntry`, `SimpleBlock`, `BlockGroup`, `Track::EOSBlock`, `VideoTrack`
and `AudioTrack` (`0x01F784D8` to `0x01F785F0`). `IMkvReader`'s vtable `0x00D89AE0` has two pure virtual
slots (`0x00861EC6`), which the game's reader fills. The Matroska element IDs are immediates in the
parse code, among them `18538067` Segment (`0x00801391`), `1654AE6B` Tracks, `1F43B675` Cluster (9
places) and `1C53BB6B` Cues (5 places).

Only the parser is linked: the image has no `mkvmuxer` text. The movie player (`0067xxxx`) and the
game's reader are the only game code that calls it.

Two of the parser's larger bodies are outside its member list:

- `0x00806F20`, called from `0x00803190` (`0x008031B5`), parses the segment's headers. It creates the Info
  (`1549A966`) and Tracks (`1654AE6B`) objects, returning -2 when either is already present, and the
  Cues object (`1C53BB6B`) when there is no Cues object.
- `0x00801550`, called from `0x00803230` (`0x0080324D`), loads the next cluster: it sets up the Cues object
  when it meets that element first and parses a Cluster (`1F43B675`).

### libvpx: the VP8 decoder

`0x0016F070` is `lea rax, [0x01CDB290]; ret`, and `0x01CDB290` is libvpx's codec interface, named "WebM
Project VP8 Decoder v1.6.0" (`0x01CEB698`). Its single caller is the movie open (`0x0067A55F`). The
movie player uses four libvpx calls, each a thin wrapper that calls through the interface:

| Function | libvpx call | Calls interface slot | Called from |
|---|---|---|---|
| `0x0016DEC0` | `vpx_codec_dec_init_ver` (ABI 10 required) | `+0x10` init | `0x0067A57D` |
| `0x0016DFE0` | `vpx_codec_decode` | `+0x38` decode | `0x0067A091` |
| `0x0016E040` | `vpx_codec_get_frame` | `+0x40` get frame | `0x0067A0AF`, `0x0067A1C5` |
| `0x0016DDD0` | `vpx_codec_destroy` | `+0x18` destroy | `0x0067AAAB` |

The decoder's SIMD kernels lie before it, from `0x00125740` (`emms; ret`). `0x0016F080` reads the
processor's features with `cpuid` and installs kernels by address (`0x0016F144` to `0x0016F167`:
`0x00126E10`, `0x001260E7`, `0x00127104`, `0x001263AD`).

### Creating the decoder instance

`0x0016F2A0` is libvpx's decoder create. Its one caller is the VP8 decode body `0x0016E4A0`, which calls
it while the dword at `+0x1A8` of its context is 0 and stores the instance at `+0x1B0`. In order:

1. It allocates `0x44A7` bytes, rounds the block up to 32-byte alignment, keeps the raw pointer just
   below it and clears `0x4480` bytes.
2. It arms the error handler: `setjmp` into `+0x1320`, with the armed flag `+0x1318` set to 1.
3. `0x00172C30(+0x12C0)` sets up the common decoder state (below).
4. It sets `+0x4440` to 1 and `+0x34DC` to 0, builds the dequantiser tables (`0x00174540`) and the loop
   filter (`0x00173640`, `0x001735C0` on `+0x1ED0`), clears four 16-byte entries at `+0x2AD0`, and
   disarms the handler.
5. The first instance runs the one-time table setup `0x0016F1F0`, guarded by `0x02EBA2EC`; a later
   instance spins on `Sleep(0)` until that word reads 2.

When the `setjmp` returns non-zero it frees the state with `0x00172750(+0x12C0)` and the block, and
returns 0.

`0x00172C30` (176 bytes, called only at `0x0016F357`) fills the common state: `0x00179B70` stores the
processor count (`GetNativeSystemInfo`, at least 1) at `+0x2228` and the SIMD feature bits from
`cpuid` at `+0x2E70`; it copies default probabilities from `0x01CDBC88` (9 bytes, to `+0x1DC2`),
`0x01CDC058` (4, to `+0x1DCB`), `0x01CDC034` (3, to `+0x1DCF`) and `0x01CDC054` (3, to `+0x1DD2`); it
writes the qword `+0xBC0` = 1 (`0x00172CA1`) and zeroes `+0xBC8`, `+0xC00`, `+0x2224`, `+0x770`,
`+0x1938`, `+0x1944` and `+0x194C`.

### The decoder's memory while a movie plays

The decoder's memory exists only while a movie is open. The movie open creates it, and its close releases it, so the
memory a cutscene movie uses is gone once the movie ends. Offsets below are from the decoder instance unless a line
says otherwise.

- **The codec context, `0x330` bytes.** libvpx's init `0x0016E110` (interface slot `+0x10`) calls `0x0016E070` at
  `0x0016E1B7`. It allocates `0x347` bytes (`0x0016E07E`), aligns the block to 16 bytes and clears `0x330` bytes
  (`0x0016E0A5`). The context keeps the decoder instance at `+0x1B0`.
- **The macroblock decoder, `0x12A0` bytes, at `+0x0000`.** The create sets its block pointers through `0x0016FA40`
  (`0x0016F3E2`), and the decode body refreshes it through `0x0016FB80` before each frame (`0x0016E977`). It holds 25 block
  records of `0x38` bytes from its `+0x860`: 16 luma, 4 + 4 chroma and one second-order block.
- **The common state at `+0x12C0`.** `0x00172C30` fills it (above). Its first `0x160` bytes are the error record the
  create's `setjmp` uses (`+0x1318`, `+0x1320`). In the same state are the loop-filter tables at `+0x1ED0` (`0xD10`
  bytes), the last frame's probabilities at `+0x2C29` and the current frame's at `+0x3082` (`0x459` bytes each), and
  the post-processing state at `+0x34F0` (`0xC40` bytes).
- **The frame buffers.** When a key frame brings a new size, the decode body calls `0x001728C0` (`0x0016E744`). It
  releases the old set through `0x00172750` (`0x001728E5`), then allocates four `0x90`-byte frame records from `+0x1A40`
  through `0x00179C80` (`0x00172963`, loop bound 4 at `0x0017297E`), and two more at `+0x1CA0` (`0x0017299E`) and `+0x1D30`
  (`0x00172AE1`).
- **The mode grid.** The same call allocates `0x4C`-byte records for a grid one record wider and one row taller than
  the frame's macroblocks (`0x00172A3F`-`0x00172A47`). It keeps the block at `+0x1EA8` (`0x00172A73`) and the first visible
  record, one row and one record in, at `+0x1EB0` (`0x00172A9E`).
  `0x00172750` frees it (`0x00172881`) and nulls the pointer (`0x001728A2`).
- **The readers.** The frame decode `0x00175EF0` runs from `0x0016F840` (`0x0016F98E`), which the decode body calls at
  `0x0016EA2D`. It starts the mode reader at `+0x42C0` (`0x00175F32`), and the eight partition readers of `0x30` bytes
  from `+0x4140` through `0x00175A00` (`0x00176BCD`). On a key frame it resets the current probabilities through
  `0x00175CA0` (`0x0017625D`).
- **Post-processing.** Get frame `0x0016EA80` runs the post-processor `0x00177A70` (`0x0016EB25`), which seeds its noise
  through `0x00177850` (`0x00177D86`).
- **Decoder threads.** The decode body starts the threads through `0x00171480` (`0x0016E617`), which allocates one
  `0x18`-byte start record per thread. Each thread has its own macroblock decoder in the array at `[+0x4410]` (count
  `+0x4390`). The decode body copies the current frame record into each one's `+0xE70` (`0x0016E8BF`) and refreshes
  each one through `0x0016FB80` (`0x0016E958`).
- **The close.** `vpx_codec_destroy` `0x0016DDD0` (`0x0067AAAB`) calls interface slot `+0x18`, `0x0016E210`. When
  `+0x4380` is set it stops the threads through `0x00171790` (`0x0016E245`). It frees the thread memory through
  `0x00172160` (`0x0016E24D`) and the frame buffers and mode grid through `0x00172750` (`0x0016E259`). Then it frees the
  instance (`0x0016E262`) and the context (`0x0016E276`) through the CRT free.

### Decoder bodies and kernels outside the member lists

Five bodies the decoder calls are in neither libvpx list:

- `0x0016FE80` and `0x00174790` decode one macroblock, called from `0x00170370` (`0x001709E6`) and
  `0x00175070` (`0x00175572`). Both read the macroblock's mode info through `+0xF00` and, for mode 4,
  predict each 4x4 subblock (`0x001790A0`) before adding its residual.
- `0x001294D0` is VP8's 4x4 inverse transform. It loads the constants 20091 and 35468 (stored as -30068)
  from `0x03001350` and `0x03001340`, and is called from `0x0016FE80` (`0x0017027C`) and `0x00174790`
  (`0x00174B05`).
- `0x00149DC0` and `0x0014A48A` are loop-filter kernels: they take absolute differences between
  neighbouring rows of 16 pixels and keep the larger. The row decoders `0x00170370` (`0x00170FDA`,
  `0x00170F12`) and `0x001738B0` (`0x00173AD8`, `0x00173A2B`) call them.

Five more kernels lie among the others but no instruction and no stored pointer in any section refers
to them:

- `0x001274D0` copies a block 32 bytes wide, four rows per pass.
- `0x00129870` computes three sums of absolute differences of a 16-byte-wide block at offsets 0, 1 and
  2, the operation of an encoder's motion search.
- `0x0012A290` runs a butterfly over eight rows of eight 16-bit values.
- `0x0012B980` and `0x00147B00` are 8x8 transforms built on 14-bit cosine constants: the pairs 15137 and
  6270, 16069 and 3196, 13623 and 9102 (tables from `0x030015A0` and from `0x03001A60`), and 23170, twice
  11585 (`0x03001380`, `0x03001A20`). VP8 itself uses only the 4x4 transform.

The other kernels from `0x00125770` to `0x00158C97` that are in neither list are not reached either:
no rel32 call, jump or conditional branch in `.text`, no rip-relative operand in any listed function and
no 8-byte pointer in any section has one of them as its target; the four installs at `0x0016F144` to
`0x0016F167` are the only references of their kind.

They are sums of absolute differences, quantizers, 8x8 and 32x32 inverse transforms, intra predictors,
VP8 loop filters, two- and eight-tap filters and sub-pixel variance kernels. Each is listed with its
arguments and what it computes in
[media-decoder-libraries-libvpx-unreferenced-kernels.tsv](media-decoder-libraries-libvpx-unreferenced-kernels.tsv).

### The VP8 control map

The interface's `+0x20` points at the control map `0x01CDB320`, `{u64 id, handler}` pairs ending with
id `0xFFFFFFFF` (`0x01CDB3D0`). The ids are libvpx 1.6.0's VP8 decoder controls:

| Id | Handler | Control |
|---|---|---|
| 1 | `0x0016EC20` | set reference frame |
| 2 | `0x0016ECE0` | copy reference frame |
| 3 | `0x0016EE40` | set post-processing |
| 4 to 7 | `0x0016EE70` | the four debug-display controls; the one shared body is `mov eax, 4; ret`, "incapable" |
| `0x100` | `0x0016EE80` | last reference updates |
| `0x101` | `0x0016EFF0` | frame corrupted |
| `0x102` | `0x0016EEC0` | last reference used |
| `0x103` | `0x0016F030` | set decryptor |

No instruction in the image refers to any of the handlers. `0x0016EC20`, `0x0016ECE0`, `0x0016EE40`,
`0x0016EE80`, `0x0016EFF0`, `0x0016EEC0` and `0x0016F030` appear only in the map. `0x0016EE70` is a body the
linker shares: besides its four map entries (`0x01CDB358`, `0x01CDB368`, `0x01CDB378`, `0x01CDB388`) it is
stored at `0x009010E8`, `0x01CB40B8`, `0x01CCFC10` and `0x01CCFC30`, in other classes' tables.
The movie player calls no control, so the map is linked data that nothing reads.

### libvorbis: the movie's sound

`0x00679A50` starts the decoder for the audio track:

1. It initialises the stream info and comment (`0x00880AF0`, `0x00880BF0`).
2. It reads the track's codec private data (`0x008020C0`) and feeds the three Vorbis header packets in
   it to `0x008800C0`, the header reader, which compares the packet's "vorbis" signature (`0x01CEBB50`,
   at `0x00880134`).
3. It starts the synthesis and block state (`0x00881830`, `0x00882200`) and allocates an output buffer
   of 48,000 four-byte samples per channel.

The audio thread `0x00679A40` runs `0x00679600`, which decodes packet by packet (`0x008822F0`,
`0x00880DF0`), takes the samples (`0x00880D70`, `0x00880D40`) and writes them as 16-bit sound, logging
"Clipping in frame %ld" when it clips. `0x00679F40`, called from `0x0067A9B0`, releases the decoder
state. Only these three movie-player functions call into libvorbis.

This is the floating-point Vorbis decoder: `0x00882AC0` unpacks codebook floats with mantissa
`& 0x1FFFFF`, exponent `(v >> 21) & 0x3FF` and bias 788 through `ldexp`. Its
`_book_maptype1_quantvals` (`0x00882850`) has none of the guards libvorbis 1.3.6 added, so the copy
predates 1.3.6.

Two floor functions: `0x0088DE20`, called by `0x0088DB70`, is `floor0_map_lazy_init`, which builds a window's
map of `blocksizes[W] / 2` linear bins to Bark bins through `atan` (`0x00862064`): `13.1 atan(0.00074 f) +
2.24 atan(1.85e-8 f^2) + 0.0001 f` (the constants at `0x01CEBC40`, `0x01CEBB64`, `0x01CEBC20`, `0x01CEBB58`,
`0x01CEBB60`), capped at the map length less 1 and ended with -1. `0x00894EE0`, called three times by
`0x0088E8C0`, is the encoder's `floor1_fit`: its fit values start at -200 and a post it drops carries bit
`0x8000`.

### CRI HCA decoder: the sound banks

The HCA decoder occupies the start of `.text`, from `0x00121000`. Its banner "HCA Decoder (Float)
Ver.2.05.00 Build:Jul 31 2015 16:45:20" (`0x01CBA5D0`) sits directly before its copyright text
"Copyright (c) 2009-2010 CRI Middleware Co., Ltd." (`0x01CBA610`).

`0x00121DB0` is the decoder's start-up. It counts calls in `0x02EAE0C8`, and on the first it checks
that every character of the copyright text is printable and that its checksum (`0x001248B0`, over
`0x32` bytes) is `0x64F5`; if either fails it loops forever. Only the sound driver (`0x007A0000` to
`0x007F1FFF`) calls the decoder, apart from `0x001243B0`, a three-byte `ret 0` body inside it that the
linker shares with the game's code. The entry points it uses, and the bank materials they decode, are on
[Sound engine](../Sound-And-Music/sound-engine.md).

### Tremor, vorbisfile and libogg: Ogg Vorbis bank material

For an Ogg Vorbis material the sound driver uses Tremor, the integer Vorbis decoder, through its
`vorbisfile` layer:

| Function | vorbisfile call | Body |
|---|---|---|
| `0x007F5970` | `ov_open_callbacks` | `_ov_open1` (`0x007F5580`), then `_ov_open2` (`0x007F5770`) when that succeeds |
| `0x007F59C0` | `ov_pcm_seek` | |
| `0x007F6280` | `ov_pcm_tell` | -131 when the state `+0x80` is below 2, else `+0x78` |
| `0x007F6730` | `ov_raw_tell` | -131 when the state is below 2, else `+0x10` |
| `0x007F6750` | `ov_read` | 16-bit output: each integer sample shifted right by 9 and clipped |
| `0x007F5850` | `ov_clear` | |

Their callers are the driver's voice code: `Voice::Initialize` (`0x007EBAD0`), the feed `0x007EAA60` and
`0x007EA050`. Tremor's own header reader, `vorbis_synthesis_headerin` (`0x007F7FF0`), compares the same "vorbis"
signature (`0x007F807E`) after the packet's type byte and dispatches on that type:

| Type | Accepted when | Unpacker |
|---:|---|---|
| 1 | the packet starts the stream (`+0xC` of the packet) and the info has no channels yet (`+8` is 0) | `0x007F7B70`, the info |
| 3 | the info has channels | `0x007F79C0`, the comment |
| 5 | the info has channels and the comment has a vendor string (`+0x18`) | `0x007F7680`, the codebooks |

A null packet and any other case return -133 (`OV_EBADHEADER`); a wrong signature returns -132 (`OV_ENOTVORBIS`).

Tremor's inverse MDCT works in fixed point, keeping the high 32 bits of each 64-bit product. Its
entry `0x007FF1C0`, called from `0x007FDC60`, rotates the input with the sine and cosine table
`0x01CC4810` and calls `0x007FE530` and `0x007FE0F0`. `0x007FE0F0` reorders the result by bit reversal,
building each index from the nibble table `0x01F41F68`, and rotates again with `0x01CC4810` or, when its step argument is
below 4, `0x01CC5820`. Neither body is in the Tremor member list.

libogg is linked in two parts:

- `framing.c` at `0x007B9D70`: its page seeker `0x007BA7E0` compares the "OggS" capture pattern
  (`0x01CB5780`, at `0x007BA835`) and its checksum code reads the CRC table `0x01CB5380`. Only
  `vorbisfile` calls it.
- `bitwise.c` at `0x0017C890`, the bit reader: `0x0017C890`, `0x0017C9F0` and `0x0017CB40` index the mask
  table `0x01CEB590` (`0, 1, 3, 7, ...`). libvorbis and Tremor call it.

## Layouts

The VP8 codec interface at `0x01CDB290`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | 0x01CEB698 | "WebM Project VP8 Decoder v1.6.0" |
| `+0x08` | `i32` |  | value 5: interface ABI version |
| `+0x0C` | `u32` |  | value `0x140001`: capabilities: decoder, post-processing, input fragments |
| `+0x10` | `void*` | 0x0016E110 | init |
| `+0x18` | `void*` | 0x0016E210 | destroy |
| `+0x20` | `void*` | 0x01CDB320 | control map |
| `+0x28` | `void*` | 0x0016E380 | peek stream info |
| `+0x30` | `void*` | 0x0016E3A0 | get stream info |
| `+0x38` | `void*` | 0x0016E4A0 | decode |
| `+0x40` | `void*` | 0x0016EA80 | get frame |
| `+0x48` | `...` | 0 | every later field, the encoder half among them |

The decoder configuration `0x0067A480` builds on its stack:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | threads | the processor count |
| `+0x04` | `u32` |  | value `0x780`: width, 1920 |
| `+0x08` | `u32` |  | value `0x438`: height, 1080 |

One of the player's three frame queues, as the queue functions use it:

`FrameQueue` (`0xA8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x08` | `u64` | buffer | pointer to the ring storage |
| `+0x10` | `u32` | readOffset | start of the next entry to read |
| `+0x14` | `u32` | writeOffset | start of the next entry to write |
| `+0x18` | `u32` | reservedEnd | end of the slot the writer has reserved |
| `+0x1C` | `u32` | readEnd | end of the entry the reader holds |
| `+0x20` | `u8` | counted | `0x006CC580` returns 0 while clear |
| `+0x28` | `u64` | spaceEvent | event handle; the writer waits on it |
| `+0x38` | `u64` | dataEvent | event handle; the reader waits on it |
| `+0x48` | `u8` | running | cleared by `0x006CC670` |
| `+0x4C` | `u32` | capacity | offsets wrap here |
| `+0x50` | `u32` | readCount | entries released |
| `+0x54` | `u32` | writeCount | entries committed |

`FrameQueueEntry` (`0x10` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | slotSize | data space reserved after the header |
| `+0x04` | `u32` | length | the data length; the data follows the header |

## Shipped data

| Fact | Value |
|---|---|
| libwebm `mkvparser` | `0x007FFBC0` to `0x00808887` and three scattered vtable bodies; 104 functions in [`media-decoder-libraries-libwebm-mkvparser.tsv`](media-decoder-libraries-libwebm-mkvparser.tsv) |
| libvpx VP8 decoder | `0x0016DDD0` to `0x0017C88F`; 116 functions in [`media-decoder-libraries-libvpx-vp8-decoder.tsv`](media-decoder-libraries-libvpx-vp8-decoder.tsv), and the four control handlers the function list does not hold (`0x0016EE40`, `0x0016EE80`, `0x0016EFF0`, `0x0016F030`) in [`media-decoder-libraries-libvpx-vp8-control-handlers.tsv`](media-decoder-libraries-libvpx-vp8-control-handlers.tsv) |
| libvpx kernels | 63 in [`media-decoder-libraries-libvpx-vp8-dsp-kernels.tsv`](media-decoder-libraries-libvpx-vp8-dsp-kernels.tsv), `0x00125740` to `0x00158C09` |
| libvpx kernels nothing reaches | [`media-decoder-libraries-libvpx-unreferenced-kernels.tsv`](media-decoder-libraries-libvpx-unreferenced-kernels.tsv), entries `0x00125770` to `0x00158C97` |
| libvorbis | `0x008800C0` to `0x008958AF`; 121 functions in [`media-decoder-libraries-libvorbis.tsv`](media-decoder-libraries-libvorbis.tsv) |
| CRI HCA decoder | `0x00121000` to `0x0012573F`; 53 functions in [`media-decoder-libraries-cri-hca-decoder.tsv`](media-decoder-libraries-cri-hca-decoder.tsv) |
| Tremor with `vorbisfile` | `0x007F41A0` to `0x007F6FAF` and `0x007F7680` to `0x007FFBBF`; 103 functions in [`media-decoder-libraries-tremor-vorbisfile.tsv`](media-decoder-libraries-tremor-vorbisfile.tsv) |
| libogg | `framing.c` 22 functions in [`media-decoder-libraries-libogg-framing.tsv`](media-decoder-libraries-libogg-framing.tsv); `bitwise.c` 4 in [`media-decoder-libraries-libogg-bitwise.tsv`](media-decoder-libraries-libogg-bitwise.tsv) |
| VP8 decoder fields | the decoder instance and macroblock-decoder field accesses in [`media-decoder-libraries-vp8-decoder-instance-accesses.tsv`](media-decoder-libraries-vp8-decoder-instance-accesses.tsv) and [`media-decoder-libraries-vp8-macroblock-decoder-accesses.tsv`](media-decoder-libraries-vp8-macroblock-decoder-accesses.tsv) |
| encoder text | `mkvmuxer`, "VP8 Encoder" and "VP9" occur zero times |

### Columns of media-decoder-libraries-libwebm-mkvparser.tsv

One row per function, 104 rows in address order.

| Column | Holds |
|---|---|
| `entry` | the function's entry address: 101 from `0x007FFBC0` to `0x00808887` and the three vtable bodies `0x007AD440`, `0x007BD590` and `0x007E3260` |

### Columns of media-decoder-libraries-tremor-vorbisfile.tsv

One row per function, 103 rows in address order.

| Column | Holds |
|---|---|
| `entry` | the function's entry address: 25 from `0x007F41A0` to `0x007F6FAF` and 78 from `0x007F7680` to `0x007FFBBF` |

### Columns of media-decoder-libraries-libvpx-vp8-decoder.tsv

One row per function, 116 rows in address order.

| Column | Holds |
|---|---|
| `entry` | the function's entry address, from `0x0016DDD0` to `0x0017C2F0` |

### Columns of media-decoder-libraries-libvpx-vp8-dsp-kernels.tsv

One row per kernel, 63 rows in address order.

| Column | Holds |
|---|---|
| `entry` | the kernel's entry address, from `0x00125740` to `0x00158C09` |

### Columns of media-decoder-libraries-libvorbis.tsv

One row per function, 121 rows in address order.

| Column | Holds |
|---|---|
| `entry` | the function's entry address, from `0x008800C0` to `0x008955A0` |

### Columns of media-decoder-libraries-cri-hca-decoder.tsv

One row per function, 53 rows in address order.

| Column | Holds |
|---|---|
| `entry` | the function's entry address, from `0x00121000` to `0x00125710` |

### Columns of media-decoder-libraries-libogg-framing.tsv

One row per function, 22 rows in address order.

| Column | Holds |
|---|---|
| `entry` | the function's entry address, from `0x007B9D70` to `0x007BA970` |

### Columns of media-decoder-libraries-libogg-bitwise.tsv

One row per function, 4 rows in address order.

| Column | Holds |
|---|---|
| `entry` | the function's entry address, from `0x0017C890` to `0x0017CB40` |

### Columns of media-decoder-libraries-libvpx-vp8-control-handlers.tsv

One row per control handler, 4 rows, each inside the decoder's span `0x0016DDD0` to `0x0017C88F` between two
functions of the decoder list.

| Column | Holds |
|---|---|
| `member_below` | the nearest function of [`media-decoder-libraries-libvpx-vp8-decoder.tsv`](media-decoder-libraries-libvpx-vp8-decoder.tsv) below the body: `0x0016ECE0` on all 4 rows |
| `member_above` | the nearest function of that list above the body: `0x0016F070` on all 4 rows |
| `refs` | how many places in the image name the body's start address: a call, jump or RIP-relative operand, a call or jump found by scanning the code bytes, an 8-byte relocated pointer, or a 4-byte image offset in a data section (the unwind table `.pdata` is not counted); 1 on all 4 rows |

## State

### The movie open time

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02E3F800` | `u32` | 0 (zero-filled tail of `.data`) | the `GetTickCount` milliseconds when the last movie was opened | `0x0067A480` (`0x0067A4EE`) | no instruction names it |

### HCA decoder start-up counts

`0x00121000` and `0x00124350` are run-once wrappers: each adds 1 to its own count and does its work only on the call
that makes the count 1. `0x00121000` then runs `0x00124350` and the start-up check `0x00121DB0`, which keeps its own count
in `0x02EAE0C8`.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EAE080` | `i32` | 0 (zero-filled tail of `.data`) | the number of calls to `0x00121000` | `0x00121000` (`0x0012100C`) | `0x00121000` (`0x00121004`); `0x001218B0` (`0x001218C2`: it returns 5 unless the count is greater than 0, a signed compare) |
| `0x02EAE0CC` | `i32` | 0 (zero-filled tail of `.data`) | the number of calls to `0x00124350`; the first runs `0x00125250` | `0x00124350` (`0x0012435C`) | `0x00124350` (`0x00124354`) |
| `0x02EAE0D0` | `i32` | 0 (zero-filled tail of `.data`) | raised by 1 on each call of `0x00125250`, which returns the new value | `0x00125250` (`0x00125250`, `inc`) | `0x00125250` (`0x00125256`) |

### A block counter in the Ogg Vorbis decoder

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EAE0D4` | `i32` | 0 (zero-filled tail of `.data`) | after each block it decodes, `0x007FDC60` adds the channel count it has just looped over (`+0x04` of the stream information at `[[block + 0x50] + 0x08]`) | `0x007FDC60` (`0x007FE0B2`, `add`) | no instruction names it |

### libvpx run-once words

Each of these words runs one set-up function once for all decoder instances. A caller that swaps 0 for 1 runs the
function and then raises the word to 2; a caller that finds 1 spins on `Sleep(0)` until it can swap 2 for 2. The
decoder-interface init `0x0016E110` runs `0x0016F080` and `0x00172580` through two of them and then calls `0x00172680`, which
runs its own; the one-time table set-up `0x0016F1F0` runs `0x00172580` and `0x001740A0`.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EBA2E8` | `u32` | 0 (zero-filled tail of `.data`) | run-once word of `0x0016F080`, the processor-feature kernel install | `0x0016E110` (`lock cmpxchg` at `0x0016E12C`, `0x0016E146`, `0x0016E15A`; `lock inc` at `0x0016E13B`) | the same `lock cmpxchg` instructions |
| `0x02EBA2F0` | `u32` | 0 (zero-filled tail of `.data`) | run-once word of `0x00172580` | `0x0016E110` (`0x0016E166`, `0x0016E180`, `0x0016E19A`; `0x0016E175`, `lock inc`); `0x0016F1F0` (`0x0016F214`, `0x0016F22E`, `0x0016F242`; `0x0016F223`, `lock inc`) | the same `lock cmpxchg` instructions |
| `0x02EBA2F4` | `u32` | 0 (zero-filled tail of `.data`) | run-once word inside `0x00172680` | `0x00172680` (`0x0017268E`, `0x00172725`, `0x0017273A`; `0x00172711`, `lock inc`) | the same `lock cmpxchg` instructions |
| `0x02EBA2F8` | `u32` | 0 (zero-filled tail of `.data`) | run-once word of `0x001740A0`, which fills the intra-predictor tables below | `0x0016F1F0` (`0x0016F24E`, `0x0016F268`, `0x0016F27C`; `0x0016F25D`, `lock inc`) | the same `lock cmpxchg` instructions |
| `0x02EBA2E4` | `u32` | 0 (zero-filled tail of `.data`) | 1 once `0x0016F1F0` has run its two set-ups; it skips them while the word is not 0 | `0x0016F1F0` (`0x0016F28B`, 1) | `0x0016F1F0` (`0x0016F1F4`) |

### Intra-predictor tables

`0x001740A0` stores the addresses of the intra-prediction functions in three tables: pairs from `0x02EBA310` to `0x02EBA378` and a third table of ten entries from `0x02EBA380`.

Two decoders index them: the
predictors `0x00174200` (`0x0017426E`-`0x00174275`) and `0x001742D0` (`0x001743F6`-`0x001743FD`) read the entry at
`0x02EBA340` and `0x02EBA348` respectively plus 8 times `+0xF10 * 2 + +0xF14 * 4` of the macroblock decoder, both
flags being 0 or 1, and `0x001790A0`, the subblock predictor, reads the third table through the address it loads at `0x001790DF`. No instruction that names an address reads the first three pairs or an entry of the third table after its first.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EBA310`, `0x02EBA318` | `void*` | 0 (zero-filled tail of `.data`) | first pair: `0x001491A0`, `0x00149160` | `0x001740A0` (`0x001740A7`, `0x00174109`) | no instruction names them |
| `0x02EBA320`, `0x02EBA328` | `void*` | 0 (zero-filled tail of `.data`) | second pair: `0x001492B0`, `0x00149260` | `0x001740A0` (`0x001740B5`, `0x00174117`) | no instruction names them |
| `0x02EBA330`, `0x02EBA338` | `void*` | 0 (zero-filled tail of `.data`) | third pair: `0x00149450`, `0x001493E0` | `0x001740A0` (`0x001740C3`, `0x00174125`) | no instruction names them |
| `0x02EBA340`, `0x02EBA348` | `void*` | 0 (zero-filled tail of `.data`) | the pair taken when `+0xF10` and `+0xF14` are both 0: `0x00148F10`, `0x00148DA0` | `0x001740A0` (`0x001740D1`, `0x00174133`) | `0x00174200` (`0x00174275`, `0x02EBA340` plus the index); `0x001742D0` (`0x001743FD`, `0x02EBA348` plus the index) |
| `0x02EBA350`, `0x02EBA358` | `void*` | 0 (zero-filled tail of `.data`) | the pair taken when only `+0xF10` is 1: `0x00148E50`, `0x00148CB0` | `0x001740A0` (`0x001740DF`, `0x00174141`) | the indexed reads at `0x00174275` and `0x001743FD` |
| `0x02EBA360`, `0x02EBA368` | `void*` | 0 (zero-filled tail of `.data`) | the pair taken when only `+0xF14` is 1: `0x00148EB0`, `0x00148D10` | `0x001740A0` (`0x001740ED`, `0x0017414F`) | the indexed reads at `0x00174275` and `0x001743FD` |
| `0x02EBA370`, `0x02EBA378` | `void*` | 0 (zero-filled tail of `.data`) | the pair taken when both are 1: `0x00148DE0`, `0x00148C40` | `0x001740A0` (`0x001740FB`, `0x0017415D`) | the indexed reads at `0x00174275` and `0x001743FD` |
| `0x02EBA380` | `void*` | 0 (zero-filled tail of `.data`) | third table, entry 0: `0x00148B70` | `0x001740A0` (`0x0017416B`) | `0x001790A0`, through the table address it loads at `0x001790DF` |
| `0x02EBA388` | `void*` | 0 (zero-filled tail of `.data`) | third table, entry 1: `0x00149370` | `0x001740A0` (`0x00174179`) | `0x001790A0`, through the table address it loads at `0x001790DF` |
| `0x02EBA390` | `void*` | 0 (zero-filled tail of `.data`) | third table, entry 2: `0x00179460` | `0x001740A0` (`0x00174187`) | the same |
| `0x02EBA398` | `void*` | 0 (zero-filled tail of `.data`) | third table, entry 3: `0x001793B0` | `0x001740A0` (`0x00174195`) | the same |
| `0x02EBA3A0` | `void*` | 0 (zero-filled tail of `.data`) | third table, entry 4: `0x00179600` | `0x001740A0` (`0x001741A3`) | the same |
| `0x02EBA3A8` | `void*` | 0 (zero-filled tail of `.data`) | third table, entry 5: `0x00179810` | `0x001740A0` (`0x001741B1`) | the same |
| `0x02EBA3B0` | `void*` | 0 (zero-filled tail of `.data`) | third table, entry 6: `0x00179700` | `0x001740A0` (`0x001741BF`) | the same |
| `0x02EBA3B8` | `void*` | 0 (zero-filled tail of `.data`) | third table, entry 7: `0x001794F0` | `0x001740A0` (`0x001741CD`) | the same |
| `0x02EBA3C0` | `void*` | 0 (zero-filled tail of `.data`) | third table, entry 8: the pointer then held at `0x02F974F8` | `0x001740A0` (`0x001741DB`) | the same |
| `0x02EBA3C8` | `void*` | 0 (zero-filled tail of `.data`) | third table, entry 9: `0x00148AF0` | `0x001740A0` (`0x001741E9`) | the same |

### Sub-pixel predictor pointers

`0x0016F080` picks one of two kernels for each pointer by the processor features it reads with `cpuid`
(`0x0016F140`-`0x0016F1D6`); "with the feature" below means bit `0x10` of `r8d` set at `0x0016F140`. `0x00175CA0` copies them into the macroblock decoder's `+0xF98`-`+0xFB0` when the decoder's
`+0x1E88` is 0 (`0x00175DE4`) and copies another set, with `0x02F97510` and `0x02F97528`, otherwise.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02F97520` | `void*` | 0 (zero-filled tail of `.data`) | the first set's pointer for `+0xF98`: `0x00172CE0`, or `0x00173450` with the feature | `0x0016F080` (`0x0016F1AB`) | `0x00175CA0` (`0x00175DED`, to `+0xF98`) |
| `0x02F97508` | `void*` | 0 (zero-filled tail of `.data`) | the first set's pointer for `+0xFA0`: `0x00173040`, or `0x00173360` with the feature | `0x0016F080` (`0x0016F1C4`) | `0x00175CA0` (`0x00175DFB`, to `+0xFA0`) |
| `0x02F97518` | `void*` | 0 (zero-filled tail of `.data`) | the first set's pointer for `+0xFA8`: `0x00172F00`, or `0x00173270` with the feature | `0x0016F080` (`0x0016F1D6`) | `0x00175CA0` (`0x00175E09`, to `+0xFA8`) |
| `0x02F97510` | `void*` | 0 (zero-filled tail of `.data`) | the second set's pointer for `+0xFA8`: `0x001263AD`, or `0x00127104` with the feature | `0x0016F080` (`0x0016F179`) | `0x00175CA0` (`0x00175E3C`, to `+0xFA8`) |
| `0x02F97500` | `void*` | 0 (zero-filled tail of `.data`) | the first set's pointer for `+0xFB0`: `0x00172DC0`, or `0x00173180` with the feature | `0x0016F080` (`0x0016F192`) | `0x00175CA0` (`0x00175E17`, to `+0xFB0` at `0x00175E51`) |

## Modding notes

- A replacement movie must be WebM with a VP8 video track; its sound must be a Vorbis track, since
  the player starts libvorbis and nothing else for audio.
- In a movie with three or more tracks, the audio track is chosen by its language tag: "eng" when
  the player's flag `+0x538` is 0, any other tag when it is 1.
- A movie whose Vorbis headers do not parse plays without sound.
- libvpx 1.6.0, libwebm and the Xiph decoders are published source; the functions on this page follow
  that source, so it can be read in place of decompiled code.
- Changing the CRI copyright text in the image makes the HCA decoder's start-up loop forever.

## Related

- [Standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md): the WebM
  files, their tracks and how the movie player finds them.
- [Sound engine](../Sound-And-Music/sound-engine.md): the sound driver, its codecs and where it calls the
  HCA decoder and Tremor.
- [Sound banks](../Sound-And-Music/sound-banks.md): the bank files whose materials these decoders read.
