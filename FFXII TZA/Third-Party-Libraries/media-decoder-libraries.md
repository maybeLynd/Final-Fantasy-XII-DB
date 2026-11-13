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

When a movie opens, the game keeps its picture track and the sound track whose language matches the movie player's
English or other-language flag (with fewer than three tracks, any sound track). It then reads the file's blocks into
queues that a picture thread and a sound thread decode separately.

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

The reader and the segment calls of steps 3 and 4:

- `0x006CCB00(reader, path)`, called on the player's `+0x290` (`0x0067A597`), returns -1 for a null path or when the
  reader's `+0x10` already holds a stream (`0x006CCB24`, `0x006CCB29`). It allocates `0x30` bytes through `0x00210EC0`
  (`0x006CCB35`), opens the path in that block with `0x00597930(block, path, 1, 1)` (`0x006CCB53`), keeps the block at
  `+0x10` (`0x006CCB5D`) and returns 1 when it is null.
- It then stores the stream's 32-bit `+0x00`, read by `0x001FDF70`, at `+0x08` (`0x006CCB6E`, `0x006CCB73`) and
  returns 1 when that is 0 and 0 otherwise (`0x006CCB7A`). The open gives up on any result but 0 (`0x0067A59E`).
- `0x00801210(reader, 0, &segment)` (call at `0x0067A5D0`, the segment pointer at the player's `+0x288`) clears the
  segment pointer (`0x00801245`) and returns -1 for a null reader or a negative position (`0x00801226`, `0x0080122F`).
  It asks the reader's slot `+0x08` for the total and available lengths (`0x00801250`) and returns a negative
  status as it is, or -1 when the available length is negative or above a known total (`0x00801284`).
- It walks the top-level elements from the position, reading each ID (`0x00807E20`) and size (`0x00807F30`) with
  their lengths from `0x00802910`. An element other than Segment `18538067` is skipped by its size (`0x008013C8`).
- For such an element a size of all ones, `(1 << 7 * len) - 1` (`0x00801385`-`0x0080138E`), or an end past the
  total returns -2 (`0x0080139D`, `0x008013B7`), as does reaching the total (`0x008012A8`); data not yet in the
  reader returns the position `pos + len` it needs (`0x0080145D`, `0x008013D0`).
- For the Segment it allocates `0xB8` bytes through `0x008098D4` with `0x02EAECF1` (`0x00801418`) and builds the
  segment there with `0x007FFBC0(block, reader, element start, data start, size)` (`0x00801438`), the size being -1
  when it is all ones or runs past the total (`0x008013E8`-`0x00801409`). It stores the segment (`0x00801440`) and
  returns 0, or -1 when the block is null (`0x00801443`-`0x0080144C`).
- `0x00803190(segment)` returns -1 when the segment's `+0xA0` is not null or `+0xB0` or `+0xA8` is not 0
  (`0x00803196`-`0x0080321A`). It parses the headers with `0x00806F20` (`0x008031B5`) and returns a negative result as it
  is and -3 for a positive one (`0x008031C1`). With a null Info `+0x78` or Tracks `+0x80` it returns -2
  (`0x0080320F`).
- Otherwise `0x00803190` calls `0x00803230` until that returns a negative value, which it returns, or 1 or more,
  which returns 0 (`0x008031E0`-`0x00803207`). The open tests neither the result of `0x00801210` nor that of
  `0x00803190`: it reads `+0x288` and goes on (`0x0067A5D5`, `0x0067A5E1`).

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
| `0x006CC6A0(q, size, length)` | writer: wait for room, write the header at the write offset, return it; it passes `0x006CC7C0` the reserved end `+0x18`, the write offset `+0x14`, the size, the read offset `+0x10` and the space event `+0x28` (`0x006CC6D4`), stores `size` at the header's `+0x00` and `length` at its `+0x04` (`0x006CC6E7`, `0x006CC6E9`), and returns 0 when the wait returns false (`0x006CC6DB`, `0x006CC701`) |
| `0x006CC710` | writer: commit; count the entry, move the write offset, signal the data event |
| `0x006CC4F0` | reader: wait for an entry and return its header |
| `0x006CC550` | reader: release; count it, move the read offset, signal the space event when the writer waits |
| `0x006CC7C0` | the shared wait: blocks on the queue's event (`0x005CD840`) until the end offset fits, wraps it at the capacity, and returns false once the queue is stopped. With the arguments (q, end, offset, size, other, event) it stores `*end = offset + size + 16` (`0x006CC7DF`-`0x006CC7EC`); the limit is `*other`, or `*other + capacity` (`+0x4C`) when `offset > *other` (`0x006CC806`-`0x006CC80B`); `*end < limit`, compared unsigned, fits (`0x006CC811`) and returns true after an end that reached the capacity becomes `*end - capacity` (`0x006CC82D`-`0x006CC835`); a slot that does not fit returns false when `+0x48` is clear (`0x006CC825`) and otherwise waits on `event` and tests again (`0x006CC81E`) |
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

The three wrappers check their arguments before they call the interface, and each stores its result at the
context's `+0x10` when the context is not null:

- `0x0016DEC0(context, interface, config, flags, version)` returns 3 for a version other than 10 (`0x0016DECA`) or
  an interface whose `+0x08` is not 5 (`0x0016DEF8`), and 8 for a null context or interface (`0x0016DFB7`).
- It returns 4 when the flags ask for bit `0x10000`, `0x20000` or `0x40000` and the interface's `+0x0C` lacks
  bit `0x40000`, `0x80000` or `0x100000` in turn (`0x0016DF08`-`0x0016DF4A`), or when `+0x0C` lacks bit `0x1`
  (`0x0016DF53`).
- It then clears the context, stores the interface at `+0x08`, its name at `+0x00`, the flags at `+0x20` and the
  configuration at `+0x28` (`0x0016DF64`-`0x0016DF8F`), and calls slot `+0x10` with the context and 0 (`0x0016DF93`).
  A non-zero result copies the first qword of the block at `+0x30` (0 when that is null) to `+0x18` and runs
  `0x0016DDD0` on the context (`0x0016DFA6`-`0x0016DFB0`); the init's result is returned.
- `0x0016DFE0(context, data, size, user, deadline)` returns 8 for a null context, or for a data pointer and size
  of which one is 0 and the other is not (`0x0016DFE9`-`0x0016E00E`); a null pointer with size 0 goes on. It
  returns 1 when the interface `+0x08` or the block `+0x30` is null (`0x0016E030`), and otherwise what slot
  `+0x38` returns, called with the block at `+0x30` and the other four arguments (`0x0016E02A`).
- `0x0016DDD0(context)` returns 8 for a null context (`0x0016DDDE`), and 1 when the interface or the block at
  `+0x30` is null (`0x0016DE12`). Otherwise it calls slot `+0x18` with that block (`0x0016DDF9`), sets `+0x00`,
  `+0x08`, `+0x30` and `+0x10` to 0 and returns 0 (`0x0016DDFE`-`0x0016DE09`).

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
   filter (`0x00173640`, `0x001735C0` on `+0x1ED0`), fills the four 16-byte entries at `+0x2AD0` with the
   bytes 0, 1, 2 and 3, entry k with the byte k (`0x0016F3B0`-`0x0016F3C9`), and disarms the handler.
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
  `0x00172750` frees it (`0x00172897`) and nulls the pointer (`0x001728A2`).
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
- `0x001294D0` is VP8's inverse Walsh-Hadamard transform of the second-order block, called from `0x0016FE80`
  (`0x0017027C`) and `0x00174790` (`0x00174B05`) with the 16 coefficients at the pointer in the caller's `+0xDA8` and
  the output at its `+0x180` (`0x0017026E`, `0x00170275`).
- Its two butterfly passes only add and subtract; each result becomes `(x + 3) >> 3` (`0x00129535`,
  `0x00129567`-`0x00129574`) and is written as a 16-bit word at output `+0x00`, `+0x20` and so on to `+0x1E0`, the
  first word of each of 16 blocks (`0x0012958B`-`0x0012962B`). It loads no constant from memory; the constants
  20091 and 35468 (stored as -30068) at `0x03001350` and `0x03001340` belong to `0x00129640` (below).
- `0x00149DC0` and `0x0014A48A` are loop-filter kernels: they take absolute differences between
  neighbouring rows of 16 pixels and keep the larger. The row decoders `0x00170370` (`0x00170FDA`,
  `0x00170F12`) and `0x001738B0` (`0x00173AD8`, `0x00173A2B`) call them.

The constants 20091 and 35468 (stored as -30068) at `0x03001350` and `0x03001340` are loaded by `0x00129640`
(`0x00129692`, `0x00129685`), the 4x4 inverse transform with add that the unreferenced-kernels table below lists.

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
3. The packet record at `+0x2F8` starts 3 bytes into the data (`0x00679AC2`, `0x00679ACA`) with the data's length
   (`0x00679AD4`), the dword `+0x304` set to 1 and `+0x308`, `+0x310` and `+0x318` set to 0 (`0x00679A98`-`0x00679AB7`).
   After the first header the packet moves on by the returned `n`, after the second by `n + 4`
   (`0x00679ADF`-`0x00679B1C`). Only the third result is tested: a non-zero one returns false at once (`0x00679B24`,
   `0x00679B28`).
4. It starts the synthesis and block state (`0x00881830`, `0x00882200`) and allocates an output buffer
   of 48,000 four-byte samples per channel. When either start returns non-zero it calls
   `0x006CC730(+0x150, 0)` (`0x00679BCC`) and returns false.
5. Otherwise it sets `+0x4F0` to `0x1000` (`0x00679B84`) and sets up the audio queue at `+0x150` with `0x006CC5A0`,
   giving it `0x800000`, `channels * 0x2000` for the channel count at `+0x324`, and the functions held at
   `0x01F2EAA8` and `0x01F2EAB0` (`0x00679B7B`-`0x00679B93`). The buffer is `channels * 48000 * 4` bytes from `0x00584740`
   (`0x00679B98`-`0x00679BA5`), kept at `+0x4E8` and cleared with `memset` (`0x00861EC0`, `0x00679BB9`); it returns true.

`0x008800C0(info, comment, packet)` returns -133 for a null packet (`0x0088020B`). It reads the type byte through
`0x0017CB40` (`0x0088010B`) and six bytes through `0x00880C10` (`0x0088012B`); a signature other than "vorbis" returns
-132 (`0x008801FC`). A header that fails the test of its type, and any other type, returns -133 (`0x008801D0`):

- Type 1 needs the packet's `+0x0C` not 0 and the info's `+0x08` 0 (`0x008801C3`, `0x008801CA`); that field is the
  third value `0x00880720` stores (`0x00880789`). A null codec setup at info `+0x20` returns `-129 + 7` (`0x008801E5`);
  otherwise the result is `r + 7` for the `r` of `0x00880720(info, reader, setup)` with the setup from info `+0x20`
  (`0x008801D7`, `0x008801F2`, `0x008801F7`).
- `0x00880720` stores the two block sizes `1 << e` at the codec setup's `+0x00` and `+0x04` (`0x008807D2`,
  `0x008807E1`).
- `0x00880720` returns `0x17` for a header it accepts (`0x00880805`), so an accepted first header gives
  `0x17 + 7`, the 30 bytes the open steps over.
- Type 3 needs the info's `+0x08` not 0 and the comment's `+0x18` null (`0x008801A7`, `0x008801AD`) and returns
  what `0x00880540(comment, reader)` returns (`0x008801BC`).
- Type 5 needs the info's `+0x08` not 0 and the comment's `+0x18` not null; a null codec setup returns -129
  (`0x00880177`), and a setup whose `+0x18` is above 0 fails (`0x00880192`). It returns what
  `0x00880230(info, reader)` returns (`0x008801A0`).

The audio thread `0x00679A40` runs `0x00679600`, which decodes packet by packet (`0x008822F0`,
`0x00880DF0`), takes the samples (`0x00880D70`, `0x00880D40`) and writes them as 16-bit sound, logging
"Clipping in frame %ld" when it clips. `0x00679F40`, called from `0x0067A9B0`, releases the decoder
state. Only these three movie-player functions call into libvorbis.

This is the floating-point Vorbis decoder: `0x00882AC0` unpacks codebook floats with mantissa
`& 0x1FFFFF`, exponent `(v >> 21) & 0x3FF` and bias 788 through `ldexp`. A `v` with bit `0x80000000` set
negates the mantissa (`0x00882ADE`, `0x00882AE2`), the call is `ldexp(m, e - 788)` (`0x00882AE9`, `0x00882AEF`), and
the double result is returned as a `float` (`0x00882AF5`). Its
`_book_maptype1_quantvals` (`0x00882850`) has none of the guards libvorbis 1.3.6 added, so the copy
predates 1.3.6.

Two floor functions: `0x0088DE20`, called by `0x0088DB70`, is `floor0_map_lazy_init`, which builds a window's
map of `blocksizes[W] / 2` linear bins to Bark bins through `atan` (`0x00862064`): `13.1 atan(0.00074 f) +
2.24 atan(1.85e-8 f^2) + 0.0001 f` (the constants at `0x01CEBC40`, `0x01CEBB64`, `0x01CEBC20`, `0x01CEBB58`,
`0x01CEBB60`), capped at the map length less 1 and ended with -1. `0x00894EE0`, called three times by
`0x0088E8C0`, is the encoder's `floor1_fit`: its fit values start at -200 and a post it drops carries bit
`0x8000`.

`0x00887630` is `seed_curve` of libvorbis's psychoacoustic model, kept as a body of its own that no call, jump or
stored pointer in the image reaches. With `seed`, `curves`, `amp`, `oc`, `n`, `linesper` and `dBoffset` as the
library names them:

- the curve is `curves[c]`, `c = (int)((amp + dBoffset - 30.0) * 0.1)` held to 0 to 7 (`0x00887649`-`0x00887699`);
- the first seed index is `oc + (curve[0] - 16.0) * linesper - (linesper >> 1)` (`0x008876A1`-`0x008876D3`);
- for each `i` from `(int)curve[0]` up to `(int)curve[1]` it raises `seed[index]` to `amp + curve[i + 2]` when the
  index is above 0 and the sum is larger, then adds `linesper` to the index and stops once the index reaches `n`
  (`0x00887700`-`0x008877E4`, four entries at a time and then one by one).

`0x00893E80` is `floor1_unpack` of libvorbis's `floor1.c`, slot 1 of the floor 1 function table `0x01CEB098`. It
allocates the `0x460`-byte floor description with `calloc` (`0x00893EBE`), uses the answer without testing it
(`0x00893EC3`-`0x00893ED1`), and reads it from the packet with
`oggpack_read` (`0x0017CB40`):

- 5 bits, the partition count at `+0x00`; then 4 bits for each partition, its class at `+0x04 + 4i`
  (`0x00893EDB`-`0x00893F26`);
- for each class up to the highest one a partition names: 3 bits plus 1, the dimension at `+0x80`; 2 bits, the
  subclass bits at `+0xC0`; when those are not 0, 8 bits, the class book at `+0x100`; then one value for each
  subclass, 8 bits less 1: the subclass books, in the class's `0x20`-byte row from `+0x140`. The subclasses
  number 1 shifted left by the subclass bits (`0x00893F60`-`0x0089401C`);
- 2 bits plus 1, the multiplier at `+0x340`; 4 bits, the range bits (`0x00894027`-`0x00894047`);
- for each partition, as many values of range bits each as its class's dimension: the posts from `+0x34C`
  (`0x0089406C`-`0x0089411C`). `+0x344` is 0 and `+0x348` is 1 shifted left by the range bits (`0x00894133`-`0x00894140`).

It refuses a negative class, subclass bits, range bits or post (`0x00893F11`, `0x00893F83`, `0x00894050`, `0x008940CE`).
It refuses a negative class book (`0x00893F9E`), a stored subclass book below -1 (`0x00893FD1`), and either book
when it is not below the book count, the dword `+0x18` of the setup block at `+0x20` of its first argument
(`0x00893FA6`-`0x00893FAA`, `0x00893FDA`-`0x00893FDE`). It refuses more than 63 posts
(`0x00894093`) and a post that is not below the value stored at `+0x348` (`0x008940D4`).

It also refuses two equal posts: it sorts pointers to the posts and to the two fixed values with `qsort`
(`0x00894248`, comparator `0x008942D0`) and compares neighbours (`0x00894260`-`0x0089426E`). On a refusal it zero-fills
the block, frees it and returns 0; otherwise it returns the block (`0x00894278`-`0x00894296`).

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

The count is raised on every call (`0x00121DBC`), and the checks run only when the new count is 1 (`0x00121DC2`).
The text at `0x01CBA610` is 50 bytes: a newline, the 48 characters and a newline. The loop tests characters 1 to
48 with the signed compares `c >= 0x20` and `c < 0x7F` (`0x00121DD7`, `0x00121DDF`, bound `0x31` at `0x00121DE6`), so
the two newlines are not tested; a failing character jumps to the `jmp` to itself at `0x00121E10`.

The checksum call is `0x001248B0(0, text, 0x32)` (`0x00121DF2`), a table-driven 16-bit CRC over all 50 bytes: each
step is `crc = (crc << 8) ^ table[(crc >> 8) ^ byte]` with the table at `0x01CBAC80` (`0x001248B5`-`0x001248DD`),
starting from the first argument. A result other than `0x64F5` stops at the `jmp` to itself at `0x00121E01`.

When both checks pass it calls `0x00124350` (`0x00121E03`). Its only caller `0x00121000` (`0x0012101C`) has already run
`0x00124350` (`0x00121017`), so this call only raises that count `0x02EAE0CC` to 2. Every return gives 0 (`0x00121E08`).

### Tremor, vorbisfile and libogg: Ogg Vorbis bank material

For an Ogg Vorbis material the sound driver uses Tremor, the integer Vorbis decoder, through its
`vorbisfile` layer:

| Function | vorbisfile call | Body |
|---|---|---|
| `0x007F5970` | `ov_open_callbacks` | `_ov_open1` (`0x007F5580`), then `_ov_open2` (`0x007F5770`) when that succeeds |
| `0x007F59C0` | `ov_pcm_seek` | |
| `0x007F6280` | `ov_pcm_tell` | -131 when the state `+0x80` is below 2, else `+0x78` |
| `0x007F6730` | `ov_raw_tell` | -131 when the state is below 2, else `+0x10` |
| `0x007F6750` | `ov_read` | 16-bit output: each integer sample shifted right by 9 and clipped; -131 when the state `+0x80` is below 2 (`0x007F6779`); at state 4 it takes the decoded samples (`0x007F8EE0`, `0x007F67A5`); at another state, or with 0 samples, it fetches the next packet (`0x007F4710`, `0x007F67BE`) and returns 0 at the stream's end, -2 (`0x007F67C3`, `0x007F691B`), and any other result of 0 or below as it is (`0x007F67D0`); a negative sample count is returned as it is (`0x007F67E2`); the count is cut to `bytes / (2 * channels)` (`0x007F6825`-`0x007F682C`), with the channels from the info at `+0x68`, indexed by the link `+0x88` when `+0x08` is set and the state is 3 or more (`0x007F67E8`-`0x007F681A`); channel `i` goes to the bytes from `2 * i` at a stride of `2 * channels`, clipped to -32768 to 32767 (`0x007F6870`-`0x007F68AA`); it then consumes the samples (`0x007F8F60`, `0x007F68E3`), adds them to `+0x78` (`0x007F68E8`), stores the link `+0x88` through the fourth argument when it is not null (`0x007F68FC`) and returns `samples * channels * 2` bytes (`0x007F6900`, `0x007F6908`) |
| `0x007F5850` | `ov_clear` | |

`0x007F41A0` is `_bisect_forward_serialno` of Tremor's `vorbisfile.c`, the recursive search for the place where
each logical stream of a chained file starts. Its arguments are the file, `begin`, `searched`, `end`, the end
granule position, the end serial number, the current link's serial list with its count, and the link index m.
`0x007F5420` calls it (`0x007F551F`) and it calls itself for the next link (`0x007F45D7`).

When the end serial number is in the list, the link is the last one (`0x007F41F4`-`0x007F420F`):

- unless the end serial number already is the stream serial `+0x200` (`0x007F423E`), it steps back with
  `0x007F5020` until that reports the stream serial, storing each answer in the offset `+0x10`
  (`0x007F4250`-`0x007F427D`);
- before each such call it stores the stream serial in its end serial number argument (`0x007F4254`), and
  `0x007F5020` is given the addresses of that argument and of the end granule position: it writes the granule
  position of each page that carries the stored stream serial and keeps that page (`0x007F5120`-`0x007F5130`);
- a page whose serial number is not in the list drops the kept page (`0x007F5133`-`0x007F5151`), and when it
  ends after reading a page with no page kept (`0x007F5171`-`0x007F518A`) it writes the serial number and granule
  position of the last page it read (`0x007F519C`-`0x007F519F`); its two error answers (`0x007F50B6`, `0x007F5181`)
  write nothing;
- it sets the link count `+0x40` to m + 1, frees the arrays `+0x48`, `+0x58` and `+0x50`, and allocates the
  offsets `+0x48` with one entry more than the links, 8 bytes each, the serial numbers `+0x58`, 4 bytes a link,
  the data offsets `+0x50`, 8 bytes a link, and the PCM lengths `+0x60`, 16 bytes a link; the info array `+0x68`
  is resized to `0x28` bytes a link and the comment array `+0x70` to `0x20` (`0x007F4283`-`0x007F433A`);
- the old `+0x60` array is not freed before its pointer is replaced (`0x007F433A`);
- it stores `end` in entry m + 1 of the offsets, `begin` in entry m and the end granule position, as the step
  back left it, in entry 2m + 1 of the PCM lengths, and returns 0 (`0x007F433E`-`0x007F4367`).

Otherwise it bisects while `searched` is below the end of the range (`0x007F421A`, `0x007F44E0`):

- the probe is `searched` itself when fewer than `0x400` bytes remain, else the midpoint
  (`0x007F4224`-`0x007F4381`);
- when the offset `+0x10` is not the probe it seeks: with no data source it returns -129; with no seek callback
  `+0x2F8`, or a callback answer of -1, it returns -128; else it stores the offset and resets the sync state
  `+0x20` with `0x007BA950` (`0x007F4389`-`0x007F43D3`);
- it takes the next page with `0x007BA7E0` on the sync state; a negative answer skips that many bytes
  (`0x007F43E0`-`0x007F43F7`);
- with no whole page yet it reads `0x400` bytes through the read callback `+0x2F0` into the buffer `0x007BA6A0`
  gives and reports them with `0x007BA970`; a missing callback, a negative read, or a read of 0 with `errno` set
  returns -128 (`0x007F43FB`-`0x007F446E`). It clears `errno` first (`0x007F4401`); a null data source, or a read of
  0 with `errno` still clear, is the end of the data (`0x007F4411`, `0x007F4470`);
- a page that is found moves the offset `+0x10` on by the page's length, and a page that began at offset
  -128 returns -128 (`0x007F4477`-`0x007F4488`);
- a page whose serial number (`0x007BA0D0`) is in the list moves `searched` up to the offset after that page
  (`0x007F4493`-`0x007F44B4`, `0x007F469E`-`0x007F46AB`);
- any other page, and the end of the data, moves the range end down to the probe; a page that was found also
  sets `next` to its own offset when that is not negative (`0x007F44C2`-`0x007F44E3`). A page that began at a
  negative offset other than -128 skips the serial test and is handled as any other page (`0x007F448A`).

After the loop it sets the offset to `next` and steps back with `0x007F5020` for the previous link's last granule
position (`0x007F44F5`-`0x007F452D`). The step back runs at least once: the test ahead of it compares a value
with itself plus 1 (`0x007F44F5`-`0x007F44FE`).

Here and in the last-link path the answer of `0x007F5020` goes into the offset `+0x10` untested (`0x007F4526`,
`0x007F4276`), also when it is one of its error answers -128 and -129 (`0x007F50A5`, `0x007F50AC`).

It seeks to `next` with `0x007F57E0` when the offset moved, and reads the next
link's headers with `0x007F4A80` into a local info block, a local comment block and a new serial list
(`0x007F452F`-`0x007F4576`).

It takes the stream serial `+0x200`, the data offset `+0x10` and the first PCM offset from `0x007F51C0`, and calls
itself with `next`, the offset, the same end values, the new list and m + 1 (`0x007F457C`-`0x007F45D7`). A non-zero
answer of `0x007F57E0`, of `0x007F4A80` or of the call to itself is returned as it is (`0x007F46B4`); a serial list
that `0x007F4A80` has filled by then is not freed. The answer of `0x007F51C0` is not tested (`0x007F45B0`).

On the way back it frees the new serial list and fills entry m + 1 of the offsets, serial numbers, data offsets,
the `0x28`-byte info block and the `0x20`-byte comment block (`0x007F45E7`-`0x007F465A`). Entry 2m + 1 of the PCM
lengths takes the previous link's last granule position and entry 2m + 2 the first PCM offset, which is also
taken off entry 2m + 3 (`0x007F465F`-`0x007F468C`).

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
- `bitwise.c` at `0x0017C890`, the bit reader and writer: `0x0017C890`, `0x0017C9F0` and `0x0017CB40` index the mask
  table `0x01CEB590` (`0, 1, 3, 7, ...`). libvorbis and Tremor call it.

`0x007BA7E0(sync, page)` returns 0 when the sync state's `+0x08` has bit `0x80000000` set (`0x007BA7FF`), and when
fewer than 27 bytes, or fewer than the header and body the header announces, are buffered (`0x007BA82E`,
`0x007BA84C`, `0x007BA883`). It keeps the header length `27 + segments` in `+0x18` and the lacing values' total in
`+0x1C` (`0x007BA845`-`0x007BA877`). It checks the CRC through `0x007B9F80` with the page's CRC field zeroed
(`0x007BA891`, `0x007BA8B6`); `0x007B9F80` reads the table at `0x007B9F9D`.

A call that finds `+0x18` non-zero, the state a return of 0 at `0x007BA883` leaves, makes no 27-byte test,
pattern compare or lacing count and goes straight to the test of header plus body (`0x007BA828`-`0x007BA82C`,
`0x007BA87B`).

A wrong CRC first puts the CRC field back (`0x007BA8C0`). Then a wrong CRC or capture pattern clears `+0x18` and
`+0x1C` and looks for the next "O" with `memchr` (`0x007BA8C3`-`0x007BA8D6`). It moves `+0x10` there, or to the
end of the data, and returns the negative count of bytes skipped (`0x007BA8E8`-`0x007BA8F2`). A good page fills
`page` when it is not null (header, header length, body, body length; `0x007BA902`-`0x007BA91A`), moves `+0x10` on
by the page length, clears `+0x14`, `+0x18` and `+0x1C`, and returns the page length (`0x007BA91E`-`0x007BA92B`).

`0x0017C890(buffer, value, bits)` is the writer `oggpack_write`. Its error path frees the buffer `+0x08` with
`free` when it is not null and zeroes the 32-byte state (`0x0017C9B8`-`0x0017C9D4`); a `bits` above 32, compared
unsigned, takes it (`0x0017C8A7`). When `endbyte >= storage - 4` for the end byte `+0x00` and the storage `+0x18`
(`0x0017C8B6`), it returns at once for a null `+0x10` (`0x0017C8BA`), takes the error path for a storage above
`0x7FFFFEFF` (`0x0017C8C5`), and otherwise grows the buffer with `realloc` to `storage + 0x100` (`0x0017C8DE`).

A failed `realloc` takes the error path (`0x0017C8E7`); a good one updates `+0x18`, `+0x08` and `+0x10`
(`0x0017C8ED`-`0x0017C8FE`). It masks the value with `mask[bits]` (`0x0017C90D`), ORs `value << endbit` into the byte
at `+0x10` (`0x0017C91B`) and writes one more byte for each of 8, 16, 24 and 32 that `n = endbit + bits` reaches
(`0x0017C932`-`0x0017C98B`; the fifth byte is 0 when the end bit is 0). It then adds `n / 8` to `+0x00` and `+0x10`
and keeps `n & 7` in the end bit `+0x04` (`0x0017C98F`-`0x0017C9A5`).

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
| libwebm `mkvparser` | `0x007FFBC0` to `0x008087C3` and three scattered vtable bodies; 104 functions in [`media-decoder-libraries-libwebm-mkvparser.tsv`](media-decoder-libraries-libwebm-mkvparser.tsv) |
| libvpx VP8 decoder | `0x0016DDD0` to `0x0017C88F`; 116 functions in [`media-decoder-libraries-libvpx-vp8-decoder.tsv`](media-decoder-libraries-libvpx-vp8-decoder.tsv), and the four control handlers the function list does not hold (`0x0016EE40`, `0x0016EE80`, `0x0016EFF0`, `0x0016F030`) in [`media-decoder-libraries-libvpx-vp8-control-handlers.tsv`](media-decoder-libraries-libvpx-vp8-control-handlers.tsv) |
| libvpx kernels | 63 in [`media-decoder-libraries-libvpx-vp8-dsp-kernels.tsv`](media-decoder-libraries-libvpx-vp8-dsp-kernels.tsv), `0x00125740` to `0x00158C09` |
| libvpx kernels nothing reaches | [`media-decoder-libraries-libvpx-unreferenced-kernels.tsv`](media-decoder-libraries-libvpx-unreferenced-kernels.tsv), entries `0x00125770` to `0x00158C97` |
| libvorbis | `0x008800C0` to `0x008958AF`; 124 functions in [`media-decoder-libraries-libvorbis.tsv`](media-decoder-libraries-libvorbis.tsv) |
| CRI HCA decoder | `0x00121000` to `0x0012573F`; 53 functions in [`media-decoder-libraries-cri-hca-decoder.tsv`](media-decoder-libraries-cri-hca-decoder.tsv) |
| Tremor with `vorbisfile` | `0x007F41A0` to `0x007F6FAF` and `0x007F7680` to `0x007FFBBF`; 107 functions in [`media-decoder-libraries-tremor-vorbisfile.tsv`](media-decoder-libraries-tremor-vorbisfile.tsv) |
| libogg | `framing.c` 22 functions in [`media-decoder-libraries-libogg-framing.tsv`](media-decoder-libraries-libogg-framing.tsv); `bitwise.c` 4 in [`media-decoder-libraries-libogg-bitwise.tsv`](media-decoder-libraries-libogg-bitwise.tsv) |
| VP8 decoder fields | the decoder instance and macroblock-decoder field accesses in [`media-decoder-libraries-vp8-decoder-instance-accesses.tsv`](media-decoder-libraries-vp8-decoder-instance-accesses.tsv) and [`media-decoder-libraries-vp8-macroblock-decoder-accesses.tsv`](media-decoder-libraries-vp8-macroblock-decoder-accesses.tsv) |
| encoder text | `mkvmuxer`, "VP8 Encoder" and "VP9" occur zero times |

### Columns of media-decoder-libraries-libwebm-mkvparser.tsv

One row per function, 104 rows in address order.

| Column | Holds |
|---|---|
| `entry` | the function's entry address: 101 from `0x007FFBC0` to `0x00808770` and the three vtable bodies `0x007AD440`, `0x007BD590` and `0x007E3260` |

### Columns of media-decoder-libraries-tremor-vorbisfile.tsv

One row per function, 107 rows in address order.

| Column | Holds |
|---|---|
| `entry` | the function's entry address: 26 from `0x007F41A0` to `0x007F6FAF` and 81 from `0x007F7680` to `0x007FFBBF` |

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

One row per function, 124 rows in address order.

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
| `refs` | how many places in the image name the body's start address: a call, jump or RIP-relative operand, a call or jump byte sequence in the code that targets it, an 8-byte relocated pointer, or a 4-byte image offset in a data section (the unwind table `.pdata` is not counted); 1 on all 4 rows |

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
flags being 0 or 1, and `0x001790A0`, the subblock predictor, reads the third table through the address it loads at
`0x001790DF`.

Each predictor takes that index while its own mode byte is 0: for `0x00174200` byte `+0` of what the macroblock
decoder's `+0xF00` points to (`0x00174238`, `0x00174254`), for `0x001742D0` byte `+1` (`0x00174317`, `0x001743DC`). With a
non-zero mode byte m, `0x00174200` reads `[0x02EBA300 + m * 0x10]` (`0x0017427F`-`0x0017428C`) and `0x001742D0` reads
`[0x02EBA308 + m * 0x10]` (`0x00174407`-`0x00174414`), which for m = 1, 2 and 3 are the first three pairs. No instruction
that names an address reads an entry of the third table after its first.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EBA310`, `0x02EBA318` | `void*` | 0 (zero-filled tail of `.data`) | first pair: `0x001491A0`, `0x00149160` | `0x001740A0` (`0x001740A7`, `0x00174109`) | `0x00174200` (`0x0017428C`, `0x02EBA310`, for mode byte 1); `0x001742D0` (`0x00174414`, `0x02EBA318`, for mode byte 1) |
| `0x02EBA320`, `0x02EBA328` | `void*` | 0 (zero-filled tail of `.data`) | second pair: `0x001492B0`, `0x00149260` | `0x001740A0` (`0x001740B5`, `0x00174117`) | `0x00174200` (`0x0017428C`, `0x02EBA320`, for mode byte 2); `0x001742D0` (`0x00174414`, `0x02EBA328`, for mode byte 2) |
| `0x02EBA330`, `0x02EBA338` | `void*` | 0 (zero-filled tail of `.data`) | third pair: `0x00149450`, `0x001493E0` | `0x001740A0` (`0x001740C3`, `0x00174125`) | `0x00174200` (`0x0017428C`, `0x02EBA330`, for mode byte 3); `0x001742D0` (`0x00174414`, `0x02EBA338`, for mode byte 3) |
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

`0x0016F080` runs `cpuid` leaf 0, and when the highest leaf is 0 it uses no feature (`0x0016F08F`-`0x0016F094`).
Otherwise leaf 1 gives a mask: `0x1`, `0x2` and `0x4` for `edx` bits `0x800000`, `0x2000000` and `0x4000000`,
and `0x8`, `0x10` and `0x20` for `ecx` bits `0x1`, `0x200` and `0x80000` (`0x0016F0AA`-`0x0016F0FB`).

`0x40` joins the mask when `ecx` holds both `0x8000000` and `0x10000000` and `xgetbv` reports both bits of
`0x6` (`0x0016F0FE`-`0x0016F125`), and after that `0x80` when the highest leaf is 7 or more and leaf 7 reports
`ebx` bit `0x20` (`0x0016F129`-`0x0016F13B`). `and r8d, 0x10` at `0x0016F140` keeps only the `0x10` from `ecx` bit
`0x200` (SSSE3), so that one bit decides all six pointers, `0x02F97528` among them (`0x0016F159`).

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02F97520` | `void*` | 0 (zero-filled tail of `.data`) | the first set's pointer for `+0xF98`: `0x00172CE0`, or `0x00173450` with the feature | `0x0016F080` (`0x0016F1AB`) | `0x00175CA0` (`0x00175DED`, to `+0xF98`) |
| `0x02F97508` | `void*` | 0 (zero-filled tail of `.data`) | the first set's pointer for `+0xFA0`: `0x00173040`, or `0x00173360` with the feature | `0x0016F080` (`0x0016F1C4`) | `0x00175CA0` (`0x00175DFB`, to `+0xFA0`) |
| `0x02F97518` | `void*` | 0 (zero-filled tail of `.data`) | the first set's pointer for `+0xFA8`: `0x00172F00`, or `0x00173270` with the feature | `0x0016F080` (`0x0016F1D6`) | `0x00175CA0` (`0x00175E09`, to `+0xFA8`) |
| `0x02F97510` | `void*` | 0 (zero-filled tail of `.data`) | the second set's pointer for `+0xFA8`: `0x001263AD`, or `0x00127104` with the feature | `0x0016F080` (`0x0016F179`) | `0x00175CA0` (`0x00175E3C`, to `+0xFA8`) |
| `0x02F97500` | `void*` | 0 (zero-filled tail of `.data`) | the first set's pointer for `+0xFB0`: `0x00172DC0`, or `0x00173180` with the feature | `0x0016F080` (`0x0016F192`) | `0x00175CA0` (`0x00175E17`, to `+0xFB0` at `0x00175E51`) |
| `0x02F97528` | `void*` | 0 (zero-filled tail of `.data`) | the second set's pointer for `+0xFB0`: `0x001260E7`, or `0x00126E10` with the feature | `0x0016F080` (`0x0016F159`) | `0x00175CA0` (`0x00175E4A`, to `+0xFB0` at `0x00175E51`) |

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

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Application: `0x00584740` is called by `0x001A98B0`; those functions are documented on
  [game application](../Engine-Core/game-application.md).
- Platform: `0x00584740` is called by `0x00650D40`; those functions are documented on
  [phyre post effect classes](../PhyreEngine/phyre-post-effect-classes.md).
- Presentation: `0x001FDF70` is called by `0x00193AD0`, `0x001B4590`; those functions are documented on
  [tim2 images](../Game-Files-And-Data-Tables/tim2-images.md).
