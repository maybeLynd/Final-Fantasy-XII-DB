---
title: "Media decoder libraries: libwebm, libvpx VP8, libvorbis, Tremor, libogg and the CRI HCA decoder as the game uses them"
kind: "system"
category: "Third-party libraries"
addresses: "0067A480, 00679A50, 00679600, 006CCB00, 0016F070, 01CDB290, 01CDB320, 0016DEC0, 0016DFE0, 0016E040, 0016DDD0, 0016EE70, 0016F080, 00801210, 00803190, 008800C0, 00882AC0, 007F5970, 007F6750, 007F6280, 007F6730, 007BA7E0, 0017C890, 01CEB590, 00121DB0, 01CBA5D0, 01CBA610, 00679BF0, 006CC6A0, 006CC7C0, 0016FE80, 001294D0, 007FF1C0"
---

## What the player sees

The full-motion movies are WebM files: libwebm's `mkvparser` reads the container, libvpx decodes
the VP8 picture and libvorbis the sound track. Music, voices and sound effects come from the sound
banks, whose materials the sound driver decodes with the CRI HCA decoder or, for Ogg Vorbis
material, with Tremor and libogg. None of these libraries is the game's own code; each is linked in
whole or in part as its authors published it.

## How it works

### Opening a movie

`0067A480(player, path, flag)` opens a movie for the movie player `001B7F30` (call at `001B8029`).
It is `PVideoPlaybackWin32`'s open, the class its two thread names carry:

1. It counts the processors in the process affinity mask, or asks `GetSystemInfo` when the mask is
   empty, and builds the VP8 decoder configuration `{threads, 780h, 438h}` (1920 x 1080).
2. It starts the VP8 decoder: `0016DEC0` (`vpx_codec_dec_init_ver`) with the interface `0016F070`
   returns, that configuration, flags 0 and ABI version 10 (call at `0067A57D`).
3. It opens the file with the game's own `mkvparser::IMkvReader`, `006CCB00`, which reads through the
   engine's file stream (`00597930`).
4. It parses the container: the segment is created (`00801210`) and loaded (`00803190`), and each
   track is read from the track list (`008028E0`, `008028F0`, `00802880`).
5. A track of type 1 becomes the video track (`+478`<sub>h</sub>). A track of type 2 becomes the audio track
   (`+480`<sub>h</sub>) when its language equals "eng" (`00D6CDC0`) exactly as the player's flag `+538`<sub>h</sub>
   asks (0 for English, 1 for another language), or when the file has fewer than three tracks.
   The loop does not stop at a match: with three or more tracks, the last audio track that passes
   the language test wins.
6. It reads the video's frame rate (`008024F0`, 29.97 when the file gives 0), width (`00802A00`),
   height (`00802500`) and duration (`008020D0`).
7. With an audio track it starts libvorbis (`00679A50`); when that fails the movie plays silent.
8. It starts the threads `PVideoPlaybackWin32::_VideoDecodingThread` (`0067A230`) and, with audio,
   `PVideoPlaybackWin32::_AudioDecodingThread` (`00679A40`).

What the movie files hold is on
[Standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md).

### Reading the movie's blocks

`00679ED0` loops until the player's `+258`<sub>h</sub> is 1, waiting on the event at `+4F8`<sub>h</sub>; while the play
state `+268`<sub>h</sub> is 1 or 2 and `+25C`<sub>h</sub> is not 2, it runs `00679BF0`, which reads the whole file:

1. It sets `+25C`<sub>h</sub> to 1 and walks the clusters from the segment's first (`008022F0`, next with
   `008025B0`) and the blocks of each, stopping early when `+268`<sub>h</sub> becomes 3.
2. A block whose track number names no track is skipped after a log line (`00D6CDA0`, through `0017D280`).
   A failed step to the next block logs "Error parsing next block of cluster" and returns.
3. Video blocks (type 1) always pass. Audio blocks (type 2) pass the same language test the open
   applies: language "eng" (`00D6CDC0`) matching flag `+538`<sub>h</sub>, or fewer than three tracks.
4. Each frame of a passing block gets a slot in a queue, video at `+00`<sub>h</sub> and audio at `+150`<sub>h</sub> when
   the movie has an audio track (`+480`<sub>h</sub>): `006CC6A0` reserves the frame length rounded down to
   16 plus 16 bytes, the reader's slot 0 (`+290`<sub>h</sub>) reads the frame into the slot's data, and a
   read that returns 0 commits the slot (`006CC710`).
5. At the end it starts again from the first cluster when the byte `+26C`<sub>h</sub> is set and the state is
   not 3. Otherwise it stops both queues (`006CC670`), sets `+25C`<sub>h</sub> to 2 and signals `+508`<sub>h</sub>.

### The frame queues

The player holds three `A8`<sub>h</sub>-byte ring queues: compressed video at `+00`<sub>h</sub>, decoded pictures at
`+A8`<sub>h</sub> and compressed audio at `+150`<sub>h</sub> (see Layouts). Each entry is a 16-byte header, the slot size
and the data length, followed by the data; an entry takes its slot size plus 16 bytes. One function
per step:

| Function | Step |
|---|---|
| `006CC6A0(q, size, length)` | writer: wait for room, write the header at the write offset, return it |
| `006CC710` | writer: commit; count the entry, move the write offset, signal the data event |
| `006CC4F0` | reader: wait for an entry and return its header |
| `006CC550` | reader: release; count it, move the read offset, signal the space event when the writer waits |
| `006CC7C0` | the shared wait: blocks on the queue's event (`005CD840`) until the end offset fits, wraps it at the capacity, and returns false once the queue is stopped |
| `006CC580` | entries waiting: written minus read, 0 while `+20`<sub>h</sub> is clear |
| `006CC920` | waits on the space event and sets it again; false once the queue is stopped |
| `006CC670` | stop: clear `+48`<sub>h</sub> and set both events, so every waiter returns |

The video work `0067A010` takes each packet from the first queue, passes it to `vpx_codec_decode`
(`0016DFE0`), releases it, and copies the three planes of every decoded image (`00679570`) into a
reserved slot of the picture queue. While that queue holds more than `+2F0`<sub>h</sub> minus 3 pictures it
waits through `006CC920`. When the movie closes, `0067A9B0` closes the reader with `006CCA70`
(`0067AA59`), which closes the `30`<sub>h</sub>-byte file stream at reader `+10`<sub>h</sub> (`0059BD80`) and frees it.

### libwebm mkvparser

The container parser is identified by the RTTI of eight `mkvparser::` classes: `IMkvReader`
(`01F70C90`), `Track`, `BlockEntry`, `SimpleBlock`, `BlockGroup`, `Track::EOSBlock`, `VideoTrack`
and `AudioTrack` (`01F784D8` to `01F785F0`). `IMkvReader`'s vtable `00D89AE0` has two pure virtual
slots (`00861EC6`), which the game's reader fills. The Matroska element IDs are immediates in the
parse code, among them `18538067` Segment (`00801391`), `1654AE6B` Tracks, `1F43B675` Cluster (9
places) and `1C53BB6B` Cues (5 places).

Only the parser is linked: the image has no `mkvmuxer` text. The movie player (`0067xxxx`) and the
game's reader are the only game code that calls it.

Two of the parser's larger bodies are outside its member list:

- `00806F20`, called from `00803190` (`008031B5`), parses the segment's headers. It creates the Info
  (`1549A966`) and Tracks (`1654AE6B`) objects, returning -2 when either is already present, and the
  Cues object (`1C53BB6B`) when there is none yet.
- `00801550`, called from `00803230` (`0080324D`), loads the next cluster: it sets up the Cues object
  when it meets that element first and parses a Cluster (`1F43B675`).

### libvpx: the VP8 decoder

`0016F070` is `lea rax, [01CDB290]; ret`, and `01CDB290` is libvpx's codec interface, named "WebM
Project VP8 Decoder v1.6.0" (`01CEB698`). Its single caller is the movie open (`0067A55F`). The
movie player uses four libvpx calls, each a thin wrapper that calls through the interface:

| Function | libvpx call | Calls interface slot | Called from |
|---|---|---|---|
| `0016DEC0` | `vpx_codec_dec_init_ver` (ABI 10 required) | `+10`<sub>h</sub> init | `0067A57D` |
| `0016DFE0` | `vpx_codec_decode` | `+38`<sub>h</sub> decode | `0067A091` |
| `0016E040` | `vpx_codec_get_frame` | `+40`<sub>h</sub> get frame | `0067A0AF`, `0067A1C5` |
| `0016DDD0` | `vpx_codec_destroy` | `+18`<sub>h</sub> destroy | `0067AAAB` |

The decoder's SIMD kernels lie before it, from `00125740` (`emms; ret`). `0016F080` reads the
processor's features with `cpuid` and installs kernels by address (`0016F144` to `0016F167`:
`00126E10`, `001260E7`, `00127104`, `001263AD`).

### Decoder bodies and kernels outside the member lists

Five bodies the decoder calls are in neither libvpx list:

- `0016FE80` and `00174790` decode one macroblock, called from `00170370` (`001709E6`) and
  `00175070` (`00175572`). Both read the macroblock's mode info through `+F00`<sub>h</sub> and, for mode 4,
  predict each 4x4 subblock (`001790A0`) before adding its residual.
- `001294D0` is VP8's 4x4 inverse transform. It loads the constants 20091 and 35468 (stored as -30068)
  from `03001350` and `03001340`, and is called from `0016FE80` (`0017027C`) and `00174790`
  (`00174B05`).
- `00149DC0` and `0014A48A` are loop-filter kernels: they take absolute differences between
  neighbouring rows of 16 pixels and keep the larger. The row decoders `00170370` (`00170FDA`,
  `00170F12`) and `001738B0` (`00173AD8`, `00173A2B`) call them.

Five more kernels lie among the others but no instruction and no stored pointer in any section refers
to them:

- `001274D0` copies a block 32 bytes wide, four rows per pass.
- `00129870` computes three sums of absolute differences of a 16-byte-wide block at offsets 0, 1 and
  2, the operation of an encoder's motion search.
- `0012A290` runs a butterfly over eight rows of eight 16-bit values.
- `0012B980` and `00147B00` are 8x8 transforms built on 14-bit cosine constants: the pairs 15137 and
  6270, 16069 and 3196, 13623 and 9102 (tables from `030015A0` and from `03001A60`), and 23170, twice
  11585 (`03001380`, `03001A20`). VP8 itself uses only the 4x4 transform.

### The VP8 control map

The interface's `+20`<sub>h</sub> points at the control map `01CDB320`, `{u64 id, handler}` pairs ending with
id `FFFFFFFF`<sub>h</sub> (`01CDB3D0`). The ids are libvpx 1.6.0's VP8 decoder controls:

| Id | Handler | Control |
|---|---|---|
| 1 | `0016EC20` | set reference frame |
| 2 | `0016ECE0` | copy reference frame |
| 3 | `0016EE40` | set post-processing |
| 4 to 7 | `0016EE70` | the four debug-display controls; the one shared body is `mov eax, 4; ret`, "incapable" |
| `100`<sub>h</sub> | `0016EE80` | last reference updates |
| `101`<sub>h</sub> | `0016EFF0` | frame corrupted |
| `102`<sub>h</sub> | `0016EEC0` | last reference used |
| `103`<sub>h</sub> | `0016F030` | set decryptor |

No instruction in the image refers to any of the handlers. `0016EC20`, `0016ECE0`, `0016EE40`,
`0016EE80`, `0016EFF0`, `0016EEC0` and `0016F030` appear only in the map. `0016EE70` is a body the
linker shares: besides its four map entries (`01CDB358`, `01CDB368`, `01CDB378`, `01CDB388`) it is
stored at `009010E8`, `01CB40B8`, `01CCFC10` and `01CCFC30`, in other classes' tables.
The movie player calls no control, so the map is linked data that nothing reads.

### libvorbis: the movie's sound

`00679A50` starts the decoder for the audio track:

1. It initialises the stream info and comment (`00880AF0`, `00880BF0`).
2. It reads the track's codec private data (`008020C0`) and feeds the three Vorbis header packets in
   it to `008800C0`, the header reader, which compares the packet's "vorbis" signature (`01CEBB50`,
   at `00880134`).
3. It starts the synthesis and block state (`00881830`, `00882200`) and allocates an output buffer
   of 48,000 four-byte samples per channel.

The audio thread `00679A40` runs `00679600`, which decodes packet by packet (`008822F0`,
`00880DF0`), takes the samples (`00880D70`, `00880D40`) and writes them as 16-bit sound, logging
"Clipping in frame %ld" when it clips. `00679F40`, called from `0067A9B0`, releases the decoder
state. Only these three movie-player functions call into libvorbis.

This is the floating-point Vorbis decoder: `00882AC0` unpacks codebook floats with mantissa
`& 1FFFFFh`, exponent `(v >> 21) & 3FFh` and bias 788 through `ldexp`. Its
`_book_maptype1_quantvals` (`00882850`) has none of the guards libvorbis 1.3.6 added, so the copy
predates 1.3.6.

### CRI HCA decoder: the sound banks

The HCA decoder occupies the start of `.text`, from `00121000`. Its banner "HCA Decoder (Float)
Ver.2.05.00 Build:Jul 31 2015 16:45:20" (`01CBA5D0`) sits directly before its copyright text
"Copyright (c) 2009-2010 CRI Middleware Co., Ltd." (`01CBA610`).

`00121DB0` is the decoder's start-up. It counts calls in `02EAE0C8`, and on the first it checks
that every character of the copyright text is printable and that its checksum (`001248B0`, over
`32`<sub>h</sub> bytes) is `64F5`<sub>h</sub>; if either fails it loops forever. Only the sound driver (`007A0000` to
`007F1FFF`) calls the decoder, apart from `001243B0`, a three-byte `ret 0` body inside it that the
linker shares with the game's code. The entry points it uses, and the bank materials they decode, are on
[Sound engine](../Sound-And-Music/sound-engine.md).

### Tremor, vorbisfile and libogg: Ogg Vorbis bank material

For an Ogg Vorbis material the sound driver uses Tremor, the integer Vorbis decoder, through its
`vorbisfile` layer:

| Function | vorbisfile call | Body |
|---|---|---|
| `007F5970` | `ov_open_callbacks` | `_ov_open1` (`007F5580`), then `_ov_open2` (`007F5770`) when that succeeds |
| `007F59C0` | `ov_pcm_seek` | |
| `007F6280` | `ov_pcm_tell` | -131 when the state `+80`<sub>h</sub> is below 2, else `+78`<sub>h</sub> |
| `007F6730` | `ov_raw_tell` | -131 when the state is below 2, else `+10`<sub>h</sub> |
| `007F6750` | `ov_read` | 16-bit output: each integer sample shifted right by 9 and clipped |
| `007F5850` | `ov_clear` | |

Their callers are the driver's voice code: `Voice::Initialize` (`007EBAD0`), the feed `007EAA60` and
`007EA050`. Tremor's own header reader compares the same "vorbis" signature (`007F807E`).

Tremor's inverse MDCT works in fixed point, keeping the high 32 bits of each 64-bit product. Its
entry `007FF1C0`, called from `007FDC60`, rotates the input with the sine and cosine table
`01CC4810` and calls `007FE530` and `007FE0F0`. `007FE0F0` reorders the result by bit reversal,
building each index from the nibble table `01F41F68`, and rotates again with `01CC4810` or, when its step argument is
below 4, `01CC5820`. Neither body is in the Tremor member list.

libogg is linked in two parts:

- `framing.c` at `007B9D70`: its page seeker `007BA7E0` compares the "OggS" capture pattern
  (`01CB5780`, at `007BA835`) and its checksum code reads the CRC table `01CB5380`. Only
  `vorbisfile` calls it.
- `bitwise.c` at `0017C890`, the bit reader: `0017C890`, `0017C9F0` and `0017CB40` index the mask
  table `01CEB590` (`0, 1, 3, 7, ...`). libvorbis and Tremor call it.

## Layouts

The VP8 codec interface at `01CDB290`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `void*` | 01CEB698 | "WebM Project VP8 Decoder v1.6.0" |
| `08`<sub>h</sub> | `i32` | 5 | interface ABI version |
| `0C`<sub>h</sub> | `u32` | `140001`<sub>h</sub> | capabilities: decoder, post-processing, input fragments |
| `10`<sub>h</sub> | `void*` | 0016E110 | init |
| `18`<sub>h</sub> | `void*` | 0016E210 | destroy |
| `20`<sub>h</sub> | `void*` | 01CDB320 | control map |
| `28`<sub>h</sub> | `void*` | 0016E380 | peek stream info |
| `30`<sub>h</sub> | `void*` | 0016E3A0 | get stream info |
| `38`<sub>h</sub> | `void*` | 0016E4A0 | decode |
| `40`<sub>h</sub> | `void*` | 0016EA80 | get frame |
| `48`<sub>h</sub> | `...` | 0 | every later field, the encoder half among them |

The decoder configuration `0067A480` builds on its stack:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | threads | the processor count |
| `04`<sub>h</sub> | `u32` | `780`<sub>h</sub> | width, 1920 |
| `08`<sub>h</sub> | `u32` | `438`<sub>h</sub> | height, 1080 |

One of the player's three frame queues, as the queue functions use it:

`FrameQueue` (`A8`<sub>h</sub> bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `08`<sub>h</sub> | `u64` | buffer | pointer to the ring storage |
| `10`<sub>h</sub> | `u32` | readOffset | start of the next entry to read |
| `14`<sub>h</sub> | `u32` | writeOffset | start of the next entry to write |
| `18`<sub>h</sub> | `u32` | reservedEnd | end of the slot the writer has reserved |
| `1C`<sub>h</sub> | `u32` | readEnd | end of the entry the reader holds |
| `20`<sub>h</sub> | `u8` | counted | `006CC580` returns 0 while clear |
| `28`<sub>h</sub> | `u64` | spaceEvent | event handle; the writer waits on it |
| `38`<sub>h</sub> | `u64` | dataEvent | event handle; the reader waits on it |
| `48`<sub>h</sub> | `u8` | running | cleared by `006CC670` |
| `4C`<sub>h</sub> | `u32` | capacity | offsets wrap here |
| `50`<sub>h</sub> | `u32` | readCount | entries released |
| `54`<sub>h</sub> | `u32` | writeCount | entries committed |

`FrameQueueEntry` (`10`<sub>h</sub> bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | slotSize | data space reserved after the header |
| `04`<sub>h</sub> | `u32` | length | the data length; the data follows the header |

## Shipped data

| Fact | Value |
|---|---|
| libwebm `mkvparser` | `007FFBC0` to `00808887` and three scattered vtable bodies; 104 functions in `media-decoder-libraries-libwebm-mkvparser.tsv` |
| libvpx VP8 decoder | `0016DDD0` to `0017C88F`; 116 functions in `media-decoder-libraries-libvpx-vp8-decoder.tsv`, and the four control handlers the function list does not hold (`0016EE40`, `0016EE80`, `0016EFF0`, `0016F030`) in `media-decoder-libraries-libvpx-vp8-control-handlers.tsv` |
| libvpx kernels | 63 in `media-decoder-libraries-libvpx-vp8-dsp-kernels.tsv`, `00125740` to `00158C09` |
| libvorbis | `008800C0` to `008958AF`; 115 functions in `media-decoder-libraries-libvorbis.tsv` |
| CRI HCA decoder | `00121000` to `0012573F`; 53 functions in `media-decoder-libraries-cri-hca-decoder.tsv` |
| Tremor with `vorbisfile` | `007F41A0` to `007F6FAF` and `007F7680` to `007FFBBF`; 99 functions in `media-decoder-libraries-tremor-vorbisfile.tsv` |
| libogg | `framing.c` 22 functions in `media-decoder-libraries-libogg-framing.tsv`; `bitwise.c` 4 in `media-decoder-libraries-libogg-bitwise.tsv` |
| VP8 decoder fields | the decoder instance and macroblock-decoder field accesses in `media-decoder-libraries-vp8-decoder-instance-accesses.tsv` and `media-decoder-libraries-vp8-macroblock-decoder-accesses.tsv` |
| encoder text | `mkvmuxer`, "VP8 Encoder" and "VP9" occur zero times |

## Modding notes

- A replacement movie must be WebM with a VP8 video track; its sound must be a Vorbis track, since
  the player starts libvorbis and nothing else for audio.
- In a movie with three or more tracks, the audio track is chosen by its language tag: "eng" when
  the player's flag `+538`<sub>h</sub> is 0, any other tag when it is 1.
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
