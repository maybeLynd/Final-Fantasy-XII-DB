---
title: "Media decoder libraries: libwebm, libvpx VP8, libvorbis, Tremor, libogg and the CRI HCA decoder as the game uses them"
kind: "system"
category: "Third-party libraries"
summary: "The decoders linked for movies and sound: libwebm's mkvparser and libvpx 1.6.0's VP8 decoder with libvorbis for the WebM movies, opened in one call that picks the video and audio tracks; and the CRI HCA decoder and Tremor with vorbisfile and libogg for the sound driver's bank materials. For each, what identifies it, its span, the entry points the game calls, and the VP8 codec interface with its control map."
addresses: ["0067A480", "00679A50", "00679600", "006CCB00", "0016F070", "01CDB290", "01CDB320", "0016DEC0", "0016DFE0", "0016E040", "0016DDD0", "0016EE70", "0016F080", "00801210", "00803190", "008800C0", "00882AC0", "007F5970", "007F6750", "007F6280", "007F6730", "007BA7E0", "0017C890", "01CEB590", "00121DB0", "01CBA5D0", "01CBA610"]
---

# Media decoder libraries: libwebm, libvpx VP8, libvorbis, Tremor, libogg and the CRI HCA decoder as the game uses them

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
   empty, and builds the VP8 decoder configuration `{threads, 0x780, 0x438}` (1920 x 1080).
2. It starts the VP8 decoder: `0016DEC0` (`vpx_codec_dec_init_ver`) with the interface `0016F070`
   returns, that configuration, flags 0 and ABI version 10 (call at `0067A57D`).
3. It opens the file with the game's own `mkvparser::IMkvReader`, `006CCB00`, which reads through the
   engine's file stream (`00597930`).
4. It parses the container: the segment is created (`00801210`) and loaded (`00803190`), and each
   track is read from the track list (`008028E0`, `008028F0`, `00802880`).
5. A track of type 1 becomes the video track (`+0x478`). A track of type 2 becomes the audio track
   (`+0x480`) when its language equals "eng" (`00D6CDC0`) exactly as the player's flag `+0x538`
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

### libwebm mkvparser

The container parser is identified by the RTTI of eight `mkvparser::` classes: `IMkvReader`
(`01F70C90`), `Track`, `BlockEntry`, `SimpleBlock`, `BlockGroup`, `Track::EOSBlock`, `VideoTrack`
and `AudioTrack` (`01F784D8` to `01F785F0`). `IMkvReader`'s vtable `00D89AE0` has two pure virtual
slots (`00861EC6`), which the game's reader fills. The Matroska element IDs are immediates in the
parse code, among them `18538067` Segment (`00801391`), `1654AE6B` Tracks, `1F43B675` Cluster (9
places) and `1C53BB6B` Cues (5 places).

Only the parser is linked: the image has no `mkvmuxer` text. The movie player (`0067xxxx`) and the
game's reader are the only game code that calls it.

### libvpx: the VP8 decoder

`0016F070` is `lea rax, [01CDB290]; ret`, and `01CDB290` is libvpx's codec interface, named "WebM
Project VP8 Decoder v1.6.0" (`01CEB698`). Its single caller is the movie open (`0067A55F`). The
movie player uses four libvpx calls, each a thin wrapper that calls through the interface:

| Function | libvpx call | Calls interface slot | Called from |
|---|---|---|---|
| `0016DEC0` | `vpx_codec_dec_init_ver` (ABI 10 required) | `+0x10` init | `0067A57D` |
| `0016DFE0` | `vpx_codec_decode` | `+0x38` decode | `0067A091` |
| `0016E040` | `vpx_codec_get_frame` | `+0x40` get frame | `0067A0AF`, `0067A1C5` |
| `0016DDD0` | `vpx_codec_destroy` | `+0x18` destroy | `0067AAAB` |

The decoder's SIMD kernels lie before it, from `00125740` (`emms; ret`). `0016F080` reads the
processor's features with `cpuid` and installs kernels by address (`0016F144` to `0016F167`:
`00126E10`, `001260E7`, `00127104`, `001263AD`).

### The VP8 control map

The interface's `+0x20` points at the control map `01CDB320`, `{u64 id, handler}` pairs ending with
id `0xFFFFFFFF` (`01CDB3D0`). The ids are libvpx 1.6.0's VP8 decoder controls:

| Id | Handler | Control |
|---|---|---|
| 1 | `0016EC20` | set reference frame |
| 2 | `0016ECE0` | copy reference frame |
| 3 | `0016EE40` | set post-processing |
| 4 to 7 | `0016EE70` | the four debug-display controls; the one shared body is `mov eax, 4; ret`, "incapable" |
| `0x100` | `0016EE80` | last reference updates |
| `0x101` | `0016EFF0` | frame corrupted |
| `0x102` | `0016EEC0` | last reference used |
| `0x103` | `0016F030` | set decryptor |

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
`& 0x1FFFFF`, exponent `(v >> 21) & 0x3FF` and bias 788 through `ldexp`. Its
`_book_maptype1_quantvals` (`00882850`) has none of the guards libvorbis 1.3.6 added, so the copy
predates 1.3.6.

### CRI HCA decoder: the sound banks

The HCA decoder occupies the start of `.text`, from `00121000`. Its banner "HCA Decoder (Float)
Ver.2.05.00 Build:Jul 31 2015 16:45:20" (`01CBA5D0`) sits directly before its copyright text
"Copyright (c) 2009-2010 CRI Middleware Co., Ltd." (`01CBA610`).

`00121DB0` is the decoder's start-up. It counts calls in `02EAE0C8`, and on the first it checks
that every character of the copyright text is printable and that its checksum (`001248B0`, over
`0x32` bytes) is `0x64F5`; if either fails it loops forever. Only the sound driver (`007A0000` to
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
| `007F6280` | `ov_pcm_tell` | -131 when the state `+0x80` is below 2, else `+0x78` |
| `007F6730` | `ov_raw_tell` | -131 when the state is below 2, else `+0x10` |
| `007F6750` | `ov_read` | 16-bit output: each integer sample shifted right by 9 and clipped |
| `007F5850` | `ov_clear` | |

Their callers are the driver's voice code: `Voice::Initialize` (`007EBAD0`), the feed `007EAA60` and
`007EA050`. Tremor's own header reader compares the same "vorbis" signature (`007F807E`).

libogg is linked in two parts:

- `framing.c` at `007B9D70`: its page seeker `007BA7E0` compares the "OggS" capture pattern
  (`01CB5780`, at `007BA835`) and its checksum code reads the CRC table `01CB5380`. Only
  `vorbisfile` calls it.
- `bitwise.c` at `0017C890`, the bit reader: `0017C890`, `0017C9F0` and `0017CB40` index the mask
  table `01CEB590` (`0, 1, 3, 7, ...`). libvorbis and Tremor call it.

## Layouts

The VP8 codec interface at `01CDB290`:

```
+0x00  ptr    01CEB698   "WebM Project VP8 Decoder v1.6.0"
+0x08  i32    5          interface ABI version
+0x0C  u32    0x140001   capabilities: decoder, post-processing, input fragments
+0x10  ptr    0016E110   init
+0x18  ptr    0016E210   destroy
+0x20  ptr    01CDB320   control map
+0x28  ptr    0016E380   peek stream info
+0x30  ptr    0016E3A0   get stream info
+0x38  ptr    0016E4A0   decode
+0x40  ptr    0016EA80   get frame
+0x48  ...    0          every later field, the encoder half among them
```

The decoder configuration `0067A480` builds on its stack:

```
+0x00  u32    threads    the processor count
+0x04  u32    0x780      width, 1920
+0x08  u32    0x438      height, 1080
```

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
