---
title: "Texture animation lists: the .ta files that list a map texture's animation frames, how they are read and bound, and what drives the frame"
kind: "format"
category: "Game files and data tables"
addresses: "001A5B30, 001A7A50, 001A7D50, 008F6768, 001A9770, 01F81168, 01F81178, 001A8BA0, 001A9940, 00677030, 0019CE20, 0019CA80, 001A7630, 001A7460, 001807F0, 001E62E0, 002F4520, 00466420, 004678E0, 004668C0, 02EBB6F0, 02EBB6E0"
---

## What the player sees

Flickering fire, moving tree shade, flapping tents and shimmering reflections on a map are pictures
flipped in sequence, not moving geometry. Each `.ta` file names one such texture and its frames; a
map without its list keeps drawing the still picture.

## Where it comes from

The files are in the archive at `gamedata/d3d11/artdata/map/<area>/<map>/<map>_anime_<n>_d3d11.ta`.
When a map's art loads, the map-art routine `001A5B30` zeroes the list counter (context `+0x264`)
and calls `001A7D50`, which builds the name from the prefix
`.\GameData\D3D11\ArtData\map\<area>\<map>\<map>_anime_` (written by `001A7A50` at context `+0x141`),
the counter and `D3D11` with `"%s%d_%s.ta"` (`008F6768`), increments the counter, and files a
whole-file text request whose completion is `001A9770` and whose result lands in `01F81178`. The
map-art context is the object at `01F81168`.

## Layouts

```
<texture path><CR><LF>
<texture path with _pic_1><CR><LF>
...
<texture path with _pic_N><CR><LF>
```

No header, count or version. Each entry is a texture path such as
`/GameData/D3D11/ArtData/map/glf01/glf0102/tex/glf0100_ya_tento04.dds.phyre`. The entry without
`_pic_` is frame 0, the texture the map's materials already use; an entry containing `_pic_N` is
frame N, with N read as the decimal digits after `_pic_`. Line order does not matter.

## Shipped data

| Fact | Value |
|---|---|
| files | 45, over 42 maps; `glf0103`, `glf0104` and `rwg0202` have two lists (0 and 1) |
| list numbers | contiguous from 0 in every map |
| sizes | 158 to 2,672 bytes |
| entries per file | 2 (4 files), 3 (2), 7 (9), 15 (11), 16 (16), 32 (3); 594 in all |
| line endings | CRLF after every entry in all 45, no other whitespace |
| shape | one entry without `_pic_` and `_pic_1` to `_pic_N` contiguous, in all 45 |
| resolution | 98 entries name a shipped file directly, 489 through `phyremaps.txt`, 7 resolve to nothing (the whole of `frs0109`'s list) |
| `phyremaps.txt` | `gamedata/d3d11/artdata/shared/phyremaps.txt`: 47,341 key and value pairs on 94,682 CRLF lines |

## Loader behaviour

- **The chain.** `001A9770` runs when a request completes. When text arrived, it parses it
  (`001A8BA0`), frees it, and requests the next number (`001A7D50`); when none did, it sets the done
  byte context `+0x140`. Lists are therefore read 0, 1, 2 … and the first missing number ends the
  chain, hiding every later one.
- **Frame sets.** `001A8BA0` adds a frame set (a vector of texture pointers, seeded with one null
  frame) to the list at context `+0x120`.
- **Tokens.** It reads each entry with a `%s` scan into a 255-byte buffer and then steps the text by
  the token's length plus 2 from where the scan started, assuming the token began there and ended with a
  two-byte separator: an LF-only file loses the first character of every later entry, and leading
  spaces or tabs shift the next start the same way. Nothing bounds the scan.
- **Remapping.** Each token is looked up in the `phyremaps.txt` map (`001A9940`, built once by
  `00677030`); when found, the value is copied over it, again without a bound. A path or mapped value of
  255 characters or more overruns the buffer and the game aborts on the stack-cookie check. A path not starting with `.` gets one prepended.
- **Binding.** The texture comes from the already loaded asset with that path's hash
  (`0019CE20` → `0019CA80`, then `001A7630`); a texture not loaded for the map binds as a null frame.
  The list loads nothing itself.
- **Frame numbers.** An entry with `_pic_` sets frame N, growing the set to `N + 1`; one without sets
  frame 0. Nothing bounds N.
- **`phyremaps.txt`.** `00677030` reads the whole file, splits it only on CRLF, takes lines as
  alternating key and value, and keeps a pair when both are non-empty; a last line without CRLF, or an
  LF-only file, gives no pairs.

### Switching the frame

`001A7460(context, texture)` returns the frame set whose frame 0 is that texture, once the done byte is
set. `001807F0(object, frame)` calls `001E62E0` when the done byte is set: on first use it finds the
object's `TextureSampler` texture and caches its frame set at `+0x210`, then stores the frame at
`+0x204` and marks `+0x208` when it changed.

The frame comes from the map-draw pass `002F4520(map, ...)`. Its inputs: `v`, the float at `+0x90` of the
object that the pointer at `+0x50` of the id's `0x70`-byte record at `[map + 0x1C0]` points to (0 when that pointer is
null); `w`, the signed word `+4` of the id's `0x30`-byte draw record at `[map + 0x178]` (a `w` above `0x3FFF`, or
negative, skips the record through the unsigned compare at `002F49FD`); and `count`, the dword at `+0` of the
animation table `[r14 + 0x150]`, which holds at `+8` a pointer to its `0x60`-byte entries (`002F4A23`-`002F4A48`).

It computes `frame = trunc(v) - 1` and `i = clamp(frame + w, 0, count - 1)` (`002F4A1B`–`002F4A3F`), and calls
`001807F0(object, frame)` only when entry `i`'s `u16 +0x0C` equals `frame` (`002F4A44`–`002F4A5D`). The pass
clamps and never wraps.

The float is the value of a map animation track bound on channel 9 (`00466420`'s arm at `00466488`
stores the track at `+0x90`). The track's slot is one of the `0x50`-byte records at `[02EBB6F0]`
(count `[02EBB6E0]`): each frame `004678E0(dt)` adds `dt × rate` (`+0x38`) to the step `+0x48` of
every active slot (`+0x4C` bit `0x1`), and `004668C0` sets `t = +0x44 + step` (`0046699D`).

With `lo` = `+0x3C`, `hi` = `+0x40` and `span = hi - lo`: with loop (`+0x4C` bit `0x2`) and
`span >= 1.0` the time becomes `t - span` when `t >= hi` and `t + span` when `t < lo`
(`004669A7`-`004669CA`); otherwise `t >= hi` stores `hi`, `t < lo` stores `lo`, and either sets
bit `0x4` (finished) (`004669D1`-`004669EA`).

The field frame drives `004678E0` through `0036F460`, which hands it the accumulator's growth
([frame update order](../Engine-Core/frame-update-order.md)).

## Modding notes

- Number a map's lists from 0 with no gaps, end every line with CRLF, start no line with whitespace,
  and include frame 0.
- Keep every path, and its `phyremaps.txt` value, under 255 characters.
- Every frame's texture must already be loaded for the map; a `.ta` cannot load textures.
- A logical path that is not shipped needs a `phyremaps.txt` pair, also CRLF-separated.
- Playback speed and looping belong to the map animation slot that drives the frame, not to the list.

## Related

- [Asset header manifests](prefetch-manifests.md): what loads the textures a list binds.
- [File path resolution](file-path-resolution.md): the 33-multiplicative path hash the loaded-asset lookup uses.
- [Map pack (.mpk)](../World-Areas-And-Travel/mpk-map-pack.md): the per-map data pack.
