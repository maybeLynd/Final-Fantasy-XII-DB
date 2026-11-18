[Home](../../README.md) / [Game files and data tables](README.md) / Texture animation lists

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Texture animation lists: the .ta files that list a map texture's animation frames, how they are read and bound, and what drives the frame | format | Game files and data tables | Image files | The &lt;map&gt;_anime_&lt;n&gt;_d3d11.ta files: CRLF-separated texture paths naming a texture and its numbered frames, the chain that reads a map's lists in number order until one is missing, the parser that remaps each path through phyremaps.txt and binds it to an already loaded texture, how a material's TextureSampler is switched to the selected frame, how the map animation slot's clock picks the frame, the 45 shipped lists, and the rules a list must follow. | 0x001A5B30, 0x001A7A50, 0x001A7D50, 0x008F6768, 0x001A9770, 0x01F81168, 0x01F81178, 0x001A8BA0, 0x001A9940, 0x00677030, 0x0019CE20, 0x0019CA80, 0x001A7630, 0x001A7460, 0x001807F0, 0x001E62E0, 0x002F4520, 0x00466420, 0x004678E0, 0x004668C0, 0x02EBB6F0, 0x02EBB6E0 |

## What the player sees

Flickering fire, moving tree shade, flapping tents and shimmering reflections on a map are pictures
flipped in sequence, not moving geometry. Each `.ta` file names one such texture and its frames; a
map without its list keeps drawing the still picture.

The list loads no pictures itself: each frame must already be loaded with the map, and a path the archive does not
hold is first renamed through `phyremaps.txt`. Which frame shows comes from one of the map's animation tracks, whose
clock sets the speed and looping.

## Where it comes from

The files are in the archive at `gamedata/d3d11/artdata/map/<area>/<map>/<map>_anime_<n>_d3d11.ta`.
When a map's art loads, the map-art routine `0x001A5B30` zeroes the list counter (context `+0x264`)
and calls `0x001A7D50`, which builds the name from the prefix
`.\GameData\D3D11\ArtData\map\<area>\<map>\<map>_anime_` (written by `0x001A7A50` at context `+0x141`),
the counter and `D3D11` with `"%s%d_%s.ta"`¹, increments the counter, and files a
whole-file text request whose completion is `0x001A9770` and whose result lands in `0x01F81178`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x008F6768` |

</details>

The map-art context is the object kept at `0x01F81168` (stored at `0x001A9922`).

## Layouts

All multi-byte fields are little-endian.

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

<details>
<summary>Show the shipped data</summary>

| Fact | Value |
|---|---|
| files | 45, over 42 maps; `glf0103`, `glf0104` and `rwg0202` have two lists (0 and 1) |
| list numbers | contiguous from 0 in every map |
| sizes | 158 to 2,672 bytes |
| entries per file | 2 (4 files), 3 (2), 7 (9), 15 (11), 16 (16), 32 (3); 594 in all |
| line endings | CRLF after every entry in all 45, no other whitespace |
| shape | one entry without `_pic_` and `_pic_1` to `_pic_N` contiguous, in all 45 |
| resolution | 98 entries name a shipped file directly, 489 through `phyremaps.txt`, 7 resolve to nothing (the whole of `frs0109`'s list); all 489 `phyremaps.txt` values are shipped files |
| every entry | one row each in [`texture-animation-lists-ta-rows.tsv`](texture-animation-lists-ta-rows.tsv), 594 rows: map, list number, line, frame, path, how it resolves and the `phyremaps.txt` value |
| `phyremaps.txt` | `gamedata/d3d11/artdata/shared/phyremaps.txt`: 47,341 key and value pairs on 94,682 CRLF lines |

</details>

## Loader behaviour

- **The chain.** `0x001A9770` runs when a request completes. When text arrived, it parses it
 ¹, frees it and clears `0x01F81178`², and requests the next number
 ³; when no text arrived, it sets the done
  byte context `+0x140`. Lists are therefore read 0, 1, 2 … and the first missing number ends the
  chain, hiding every later one.
- **Frame sets.** `0x001A8BA0` adds a frame set (a vector of texture pointers, seeded with one null
  frame) to the list at context `+0x120`.
- **Tokens.** It reads each entry with a `%s` scan into a 255-byte buffer and then steps the text by
  the token's length plus 2 from where the scan started, assuming the token began there and ended with a
  two-byte separator: an LF-only file loses the first character of every later entry, and leading
  spaces or tabs shift the next start the same way. Nothing bounds the scan.
- **Remapping.** Each token is looked up in the `phyremaps.txt` map (`0x001A9940`, built once by
  `0x00677030`); when found, the value is copied over it, again without a bound. A path or mapped value of
  255 characters or more overruns the buffer and the game aborts on the stack-cookie check. A path not starting with `.` gets one prepended.
- **Binding.** The texture comes from the already loaded asset with that path's hash
  (`0x0019CE20` → `0x0019CA80`, then `0x001A7630`); a texture not loaded for the map binds as a null frame.
  The list loads nothing itself.
- **Lookup.** `0x0019CA80(registry, path)` hashes the path⁴ and, under the registry's lock
 ⁵, finds the tree entry with that hash; it returns the asset at `+8` of the
  entry's record `+0x28` when the record's dword `+4` is at least 1, and null otherwise
 ⁶.
- **Texture.** `0x001A7630(asset)` returns null for a null asset. Otherwise it takes the first object list
  at the asset's `+0x38` whose class (`+0x50`), or a class up its `+0x78` chain, is `PTexture2D`
 ⁷ and whose count `+0x74` is non-zero, and returns null when no list qualifies
 ⁸.
- **Texture object.** From that list's first object `+0x60` it steps by the class size `+0x38` while the
  address equals the current link of the chain that starts at the list's `+0x10`, each step also moving to
  that link's successor `+0`, and returns the address plus the class's offset `+0xF8`
 ⁹.
- **Frame numbers.** An entry with `_pic_` sets frame N, growing the set to `N + 1`; one without sets
  frame 0. Nothing bounds N.
- **`phyremaps.txt`.** `0x00677030` reads the whole file, splits it only on CRLF, takes lines as
  alternating key and value, and keeps a pair when both are non-empty; a last line without CRLF, or an
  LF-only file, gives no pairs.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001A8BA0` |
| ² | `0x001A9793`, `0x001A979F` |
| ³ | `0x001A7D50` |
| ⁴ | `0x00674A00` |
| ⁵ | `0x005CD4F0`, `0x005CD820` |
| ⁶ | `0x0019CAB0`-`0x0019CAF6` |
| ⁷ | `0x02CBB900` |
| ⁸ | `0x001A7639`-`0x001A768D` |
| ⁹ | `0x001A7693`-`0x001A76BC` |

</details>

### Switching the frame

`0x001A7460(context, texture)` returns the frame set whose frame 0 is that texture, once the done byte is
set; it returns 0 while the done byte is clear or when no `0x20`-byte set record from `+0x120` to `+0x128`
matches¹. `0x001807F0(object, frame)` calls `0x001E62E0` when the done byte is set: on
first use it finds the object's `TextureSampler` texture and caches its frame set at `+0x210`, then stores
the frame at `+0x204` and marks `+0x208` when it changed.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001A7469`, `0x001A7491` |

</details>

- **The texture.** `0x001E62E0` takes the first entry of the array at `+0x20` of `[[object + 0x18]]`: the
  qword at `+0x08` for a count of 1, the first qword `+0x08` points to for more¹.
  It looks `TextureSampler` up in the entry's `+0x00`² and reads the entry's parameter block
  `+0x08`. With a count of 0 the texture is null³.
- **Faults.** A parameter whose offset word `+0x10` is below 4, or whose end (word `+0x12` & `0x1FFF` plus
  the offset) passes the block's dword `+0`, makes it read through a null pointer and fault
 ⁴; a missing parameter faults on the null descriptor⁵. Otherwise the
  texture is the qword at the block plus the offset plus `0x10`⁶.
- **No set.** With no matching set `+0x210` stays null, `0x001E62E0` stores nothing and searches again on the
  next call⁷. The frame's range test only feeds the no-op `0x0016D6A0`
 ⁸, so any frame, negative or past the set, is stored at `+0x204`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x001E6313`-`0x001E6331` |
| ² | `0x0018D240` |
| ³ | `0x001E6380` |
| ⁴ | `0x001E635A`-`0x001E636E` |
| ⁵ | `0x001E6347` |
| ⁶ | `0x001E637A` |
| ⁷ | `0x001E6393`, `0x001E63B6` |
| ⁸ | `0x001E63B8`-`0x001E63D2` |

</details>

The frame comes from the map-draw pass `0x002F4520(map, ...)`. Its inputs:

- `v`, the float that the pointer at `+0x90` of the object points to (`0x002F4A0F`, `0x002F4A1B`; 0 when that pointer
  is null, `0x002F4A21`), where the object is the one the pointer at `+0x50` of the id's `0x70`-byte record at
  `[map + 0x1C0]` points to¹;
- `w`, the signed word `+4` of the id's `0x30`-byte draw record at `[map + 0x178]`; a `w` above `0x3FFF`, or
  negative, skips the frame step through the unsigned compare at `0x002F49FD`, and so does a null object pointer
 ²;
- `count`, the dword at `+0` of the animation table `[r14 + 0x150]`, which holds at `+8` a pointer to its
  `0x60`-byte entries³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002F499F` |
| ² | `0x002F4A0D` |
| ³ | `0x002F4A23`-`0x002F4A48` |

</details>

It computes `frame = trunc(v) - 1` and `i = clamp(frame + w, 0, count - 1)`¹, and calls
`0x001807F0(o, frame)` only when entry `i`'s `u16 +0x0C` equals `frame`². The pass
clamps and never wraps.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002F4A1B`-`0x002F4A3F` |
| ² | `0x002F4A44`-`0x002F4A5D` |

</details>

`o` is not the object that holds the float but the entry `0x00180320(id)` returns¹: the qword at index
`id × 2 + s` of the array `+0x88` of the map-art context `0x001A9930()`², where `s` is 1 when byte
`+0x1C` of the render manager `0x00189120()` is non-zero, or 0 when that array is null or `id` is not below its
count `+0x20`. A null `o` skips the item's whole draw³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002F49E3` |
| ² | `0x001A7600` |
| ³ | `0x002F49EF` |

</details>

The float is the value of a map animation track bound on channel 9 (`0x00466420`'s arm at `0x00466488`
stores the track at `+0x90`: the pointer to the track's value it is given, as a qword; a channel above 20
binds nothing, `0x00466423`). The track's slot is one of the `0x50`-byte records at `[0x02EBB6F0]`
(count `[0x02EBB6E0]`): each frame `0x004678E0(dt)` adds `dt × rate` (`+0x38`) to the step `+0x48` of
every active slot (`+0x4C` bit `0x1`), and `0x004668C0` sets `t = +0x44 + step`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0046699D` |

</details>

- **No chunk.** `0x004678E0` and `0x004668C0` do nothing while the map's animation chunk `0x02EBB6F8` is null
 ¹.
- **Which slots.** `0x004668C0` updates an active slot only when its bit `0x8` is set or its step's absolute
  value is above 0.001²; it clears bits `0x4` and `0x8` before it moves the time
 ³.
- **Sampling.** After the loop or clamp below it samples the slot's tracks⁴ and targets
 ⁵, unless the clip's group word `+0x2A` is above `0x100` with its bit in the hidden-model set
  `0x0026E5F0`⁶. It zeroes the step of every slot, updated or not⁷.
- **The hidden test in detail.** The answer of `0x0026E5F0` is fetched once, before the slot loop
 ⁸. The group word is compared signed with `0x100`⁹, so a group of
  `0x8000` or more is sampled without the test. For a group above `0x100` the mask is
  `1 << ((group - 0x100) & 31)`, sign-extended to 64 bits and tested against the whole answer
 ¹⁰.
- **The two lists.** The tracks are the `0x18`-byte entries at the slot's `+0x20`, counted by its word
  `+0x30`; the targets are the `0x130`-byte entries at `+0x28`, counted by its word `+0x32`. Both counts
  are read signed and again after each call. The calls are `0x00466240(slot, track, index)` and
  `0x00466550(slot, target)`¹¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x004678E0`-`0x004678EB`, `0x004668C4`-`0x004668CC` |
| ² | `0x00466965`-`0x0046697B` |
| ³ | `0x00466981`-`0x00466996` |
| ⁴ | `0x00466240` |
| ⁵ | `0x00466550` |
| ⁶ | `0x004669ED`-`0x00466A6E` |
| ⁷ | `0x00466A72` |
| ⁸ | `0x004668E4` |
| ⁹ | `0x004669F5`-`0x004669F9` |
| ¹⁰ | `0x004669FB`-`0x00466A0D` |
| ¹¹ | `0x00466A0F`-`0x00466A6E` |

</details>

With `lo` = `+0x3C`, `hi` = `+0x40` and `span = hi - lo`: with loop (`+0x4C` bit `0x2`) and
`span >= 1.0` the time becomes `t - span` when `t >= hi` and `t + span` when `t < lo`¹; otherwise `t >= hi` stores `hi`, `t < lo` stores `lo`, and either sets
bit `0x4` (finished)².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x004669A7`-`0x004669CA` |
| ² | `0x004669D1`-`0x004669EA` |

</details>

The field frame drives `0x004678E0` through `0x0036F460`, which hands it the accumulator's growth
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

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 6 calls with 2 other topics</summary>

**Controls and input** (explained on [screen mode and aspect](../Graphics/screen-mode-and-aspect.md), [phyre application](../PhyreEngine/phyre-application.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x005CD4F0`](../Engine-Core/call-signatures.md) (on call signatures) | is called by | [`0x0079C140`](../PhyreEngine/phyre-application.md) (on phyre application)<br>[`0x007A0340`](../PhyreEngine/phyre-application.md) (on phyre application) |
| [`0x005CD820`](../PhyreEngine/phyre-asset-files.md) (on phyre asset files) | is called by | [`0x0079C140`](../PhyreEngine/phyre-application.md) (on phyre application)<br>[`0x007A0340`](../PhyreEngine/phyre-application.md) (on phyre application) |

**Platform** (explained on [debug menu](../Engine-Core/debug-menu.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x005CD4F0`](../Engine-Core/call-signatures.md) (on call signatures) | is called by | [`0x0019CC50`](../Engine-Core/debug-menu.md) (on debug menu) |
| [`0x005CD820`](../PhyreEngine/phyre-asset-files.md) (on phyre asset files) | is called by | [`0x0019CC50`](../Engine-Core/debug-menu.md) (on debug menu) |

</details>
