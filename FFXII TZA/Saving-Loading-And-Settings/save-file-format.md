[Home](../../README.md) / [Saving, loading and settings](README.md) / Save file format

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Save file format: the SAFH container, its zlib and RC4 layers, the save image and its header fields, the four in-memory copies and the format stamps | format | Saving, loading and settings | Saving and loading | What a FFXII_000 save file is from the outside in: the 12-byte SAFH container header, the body that is zlib-compressed and then RC4-encrypted under a key derived from the rotated game title, the 353,936-byte image inside it with its 512-byte header (checksum, gil, play time, slot roster, area, format constants) and payload, the four image buffers the game keeps in memory, the checksum the writer computes, the stamps the loader checks, and what loading an older or edited image does. | 0x008666B0, 0x00866200, 0x00865840, 0x00865D90, 0x002EF640, 0x00583D60, 0x0057E310, 0x003BB220, 0x00253A80, 0x00255260, 0x00233C10, 0x002370C0, 0x00584210, 0x00862A40 |

## What the player sees

A save is one file per slot, FFXII_000 and up, in the game's folder under Documents. It is small on
disk because the game compresses and encrypts a much larger image before writing it.

- The image carries what the slot list shows (the party, their levels and jobs, the leader, the
  play time, the gil and the area) and everything else that persists.
- The game keeps that image in memory while you play and copies it when you save.
- Loading checks a few stamps. An image whose battle-state stamp does not match is not partly
  accepted but rebuilt from scratch. A block that passes is read at this build's layout, and only
  the members' gambit banks are rebuilt from it.

## Where it comes from

The save directory is built by `0x00862A40`: the Documents folder (`SHGetFolderPathW`, CSIDL 5), then
`\My Games\`¹, then `FINAL FANTASY XII THE ZODIAC AGE\`², then, when the
user-id string from `0x001F3ED0` is non-empty, that id and a backslash; the result is kept at
`0x02EAF6E0`, created on first use, and `0x00862A20` returns it. A slot's file name is `FFXII_`³
followed by the three-digit slot number (`sprintf("%s%03d")` in `0x0057E310` and `0x00584610`); the slot icon
assets are named `icon.sys` and `static.ico` by the same formatter.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x01F44D08` |
| ² | `0x01F44D10` |
| ³ | `0x003935C0` |

</details>

`0x00862A20` is called at `0x00408E20` when `0x01E02810` is 0 or above 1000¹, in the `0x01E02810`
branch of the FF12CONFIG loader `0x00408C30`, which does not run in the shipped game ([game
settings](game-settings.md)). The path is built at startup (`0x008624C0`, [startup
constants](../Engine-Core/startup-constants.md)), and the stream opener `0x008624D0`, the delete `0x00862130`
and the name probe `0x008621E0` read `0x02EAF6E0` directly, as the first `%s` of the formats `%s%S` and `%s%S%03d`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00408DCB`-`0x00408DE4` |
| ² | `0x01CCF970`, `0x01CCF980`; `0x00862514`, `0x00862160`, `0x00862241`, `0x00862389` |

</details>

`0x00862A40` keeps a path already at `0x02EAF6E0` while `GetFileAttributesW` reports it as a directory (bit `0x10`);
otherwise it zeroes the `0x200` bytes there and builds the path again¹. It returns with
`0x02EAF6E0` left empty when `SHGetFolderPathW` fails². It joins the pieces with `0x00408ED0`, 256
characters at most, and the formats `%s%s`, `%s%s%s\` and `%s`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00862A62`-`0x00862A96` |
| ² | `0x00862ABC` |
| ³ | `0x00862AE7`, `0x00862B50`, `0x00862B6A`, `0x00862BB1` |

</details>

It creates `Documents\My Games\` and then the final folder with `CreateDirectoryW` when `GetFileAttributesW` does not
report a directory¹; a failed create returns with `0x02EAF6E0` empty.
With a user id the final folder is the id's folder inside `FINAL FANTASY XII THE ZODIAC AGE\`, which itself gets no
create call. Only after the last create does it copy the path to `0x02EAF6E0`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00862AEC`-`0x00862B0F`, `0x00862B6F`-`0x00862B98` |
| ² | `0x00862BB1` |

</details>

With an empty user id, the first character of the string from `0x001F3ED0()` being 0, the path ends at the game
folder: `Documents\My Games\FINAL FANTASY XII THE ZODIAC AGE\`, the folder string itself ending in the
backslash¹. That folder is then the one created, and the slot
files lie directly in it. A run with no Steam user signed in showed exactly that path at `0x02EAF6E0`
(measured).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00862B15`-`0x00862B36`, `0x00862B57`-`0x00862B6A` |

</details>

The container is read by `0x008666B0(path, mode)`, called from the stream opener `0x008624D0`¹, and written by `0x00866200`, called from `0x008624D0`² and the stream closer
`0x008620E0`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00862543` |
| ² | `0x00862508` |
| ³ | `0x008620F4` |

</details>

## Layouts

All multi-byte fields are little-endian.

### The container on disk

`SaveFileContainer` (`0xC` bytes, offsets from the start of the file):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[4]` | magic | "SAFH"; `0x008666B0` rejects anything else as a container (see Loader behaviour) |
| `+0x04` | `u32` | size | the decoded image size, `0x56690` in this build; must be at most `0x100000` (`0x00866817`) |
| `+0x08` | `u32` |  | rotation 0-31, the key rotation; must be below 32 (`0x00866805`); kept at `0x02EB3868` |

The body from `+0x0C` to the end of the file is the image, compressed with zlib `compress2` at
level 9 (`0x0087AF40`, called from `0x00866200` with level 9) and then encrypted with RC4 by
`0x00865AE0`.

### The key

Both directions derive the key the same way¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00865840` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | `CryptAcquireContextW` with container `RSA_SQEX_FFXII_TZA` and the Microsoft Enhanced Cryptographic Provider v1.0, type 1, retried with `CRYPT_NEWKEYSET`. | `0x008658AF`-`0x008658D6` |
| 2 | `CryptCreateHash(CALG_MD5)` (`0x8003`). |   |
| 3 | The 32-character title `FINAL FANTASY XII THE ZODIAC AGE` is rotated left by the container's rotation (`strncpy` and two `memcpy`, `0x0086592C`-`0x0086595C`) and its 32nd byte set to NUL, so 31 characters are hashed (`CryptHashData`, `0x00865985`). | `0x00865961` |
| 4 | `CryptDeriveKey(CALG_RC4 = 0x6801, flags 0x00800000)`: a 128-bit RC4 key. | `0x008659AF` |
| 5 | `CryptDecrypt` (or `CryptEncrypt`) over the body in 1,000-byte chunks, the last one marked final. | `0x008659C2`-`0x00865A31` |

The writer draws the rotation as `abs(rand()) mod 32`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x008663C5`-`0x008663ED` |

</details>

### The image

`SaveImage` (`0x56690` bytes, offsets from the start of the image):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8[512]` | header | see below |
| `+0x200` | `u8[353424]` | payload | the persistent payload; `0x002EF2B0` returns its address |

The image is 353,936 bytes: the clear `0x002EF5F0` and the boot initialiser `0x002EF650` memset that
many, the copy to the write buffer passes it¹, and the submit records it at its widget's
`+0x100`². That is `+0x30` of the 56-byte descriptor at widget `+0xD0`, which holds
the name from `0x00584610` at `+0x00` and the write buffer at `+0x28`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EF690` |
| ² | `0x0057E310`, `0x0057E42F` |
| ³ | `0x0057E3F2`-`0x0057E423` |

</details>

### The header

`SaveImageHeader` (`0x200` bytes, offsets from the start of the image):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | checksum | in the file: CRC-32 of image[`0x08`, `0xE200`) (`0x0057E3BF`); the finaliser writes its complement here first (`0x00583FA1`) |
| `+0x04` | `u32` | one | 1 in the written image (`0x0057E3C7`); neither the slot scan nor a load reads it back |
| `+0x08` | `i32` | gil | written by `0x00254EE0` (`0x00254F1F`), read by `0x00253690` |
| `+0x0C` | `u32` | walked | walked-distance total mirrored from the battle block by `0x00254E80` (`0x00254E90`) |
| `+0x10` | `u64` | ticks | play clock, 60 Hz ticks, added by `0x00254CC0`; its bound is the sign-extended immediate `0xFFFFFFFF80BEFBFF` compared unsigned (`0x00254CF1`, `0x00254D30`-`0x00254D33`), so it never fires |
| `+0x18` | `u16` | hours | (ticks / 216000) mod 10000, by `0x00254CC0` (`0x00254DB5`) |
| `+0x1A` | `u8` | minutes | (ticks / 3600) mod 60, by `0x00254CC0` |
| `+0x1B` | `u8` | seconds | (ticks / 60) mod 60, by `0x00254CC0` |
| `+0x1C` | `u8[4]` | pad | not written by the enumerated writers |
| `+0x20` | `u8[28]` | roster | seven 4-byte entries, `0x00583D60`: character id, level, jobs (high and low nibble), flags; unused entries start with `0xFF` |
| `+0x3C` | `u32` | esper | the summoned Esper's character row: `0x003200A0` sets its flag bit `0x1` when summon mode is on (block `+0x5B04` bit `0x1`, `0x003135E0`) and copies the row byte block `+0x5AD4` (`0x003137E0`); `0x00583D60` stores it, else `0xFF` (`0x00583F08`-`0x00583F0D`); the slot pane's ESPER row shows its name when it is not `0xFF` (`0x0057EFE0`, `0x0057F0CC`) |
| `+0x40` | `u32` | counter | counter kind `0x11` (`0x003166F0`) when story flag `0x400B` is set, else untouched |
| `+0x44` | `u32` | clanrank | `0x00315390`() when story flag `0x400B` is set, else 0 |
| `+0x48` | `u32` | maparea | the World Map area of the field's persistence group: `0x00254380`(`0x00264F90`(field)), the group's area byte in the map file (not the group itself, nor the field) |
| `+0x4C` | `u32` | field | the active or pending field id (`0x003148F0`) |
| `+0x50` | `u32` |  | savecount `0x00583D60`'s second argument (the controller's `+0xD0`); in the written image the save counter `0x02CA99B4`, saturating at `0xFFFFFFFF` (`0x0057E3CE`-`0x0057E3DD`) |
| `+0x54` | `u8` | slot | `0x00583D60`'s first argument: the save slot (controller `+0xCD` from `0x00581DA0` at `0x00581EE7`; 0 from `0x005844A0` at `0x005844BE`) |
| `+0x55` | `u8[2]` | pad2 | not written by the enumerated writers |
| `+0x57` | `u8` | flags | bit `0x1` from `0x00236760` (Trial Mode stash pending), bit `0x2` from `0x00236740` (New Game+), bit `0x4` from `0x00236780` (New Game-) (`0x00583F5A`-`0x00583F7D`) |
| `+0x58` | `u32` | date | constant `0x20050223`, written by `0x00253A80` and never read |
| `+0x5C` | `u32` |  | clearsize constant `0x1538`, the size `0x002EF2DD` clears at payload +0 |
| `+0x60` | `u32` | stamp | constant `0x05071901`, the party block's stamp |
| `+0x64` | `u32` |  | blocksize constant `0x7410`, the party block's size |
| `+0x68` | `u32` | magic2 | `0x0131F3EA`, tested by `0x00255260` |
| `+0x6C` | `u32` | size2 | `0x4818`, tested by `0x00255260`; the image-backed state block's size |
| `+0x70` | `u8[36]` | stash | the mode-3 stash: `+0x70` ticks, `+0x78` hours, `+0x7A` minutes, `+0x7B` seconds, `+0x7C` walked (`0x00320D50`), `+0x80` to `+0x93` the five dwords of the world-transition record (`0x00584210`; the last stored at `0x005842B1` and read back at `0x0058435C`) |
| `+0x94` | `u8[364]` | rest | zeroed by the image clears; not written by the enumerated writers |

`0x00320D50` answers the walked distance `cvttss2si([+0x5AC8]) + [+0x5ACC]` from the battle block `[0x02EBF190]`: the
float `+0x5AC8` made an integer, with the dword `+0x5ACC` added¹. `0x00329E40(value)` re-seats
it: it stores the value at `+0x5ACC` and 0 at `+0x5AC8`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00320D57`-`0x00320D5F` |
| ² | `0x00329E47`-`0x00329E54` |

</details>

The roster loop¹ walks party pages 0-8 from `0x00282DF0(page)`, skips a page
whose word `+0x60` is negative or whose flag bit `0x2` is set, and writes for each page `{+0x60 low
byte, +0xBA, +0x86 << 4 | +0x87, flags}` with flag bit `0x1` when the page is the leader², bit `0x2` when the page's dword `+0` has bit `0x400`; the page with flag bit `0x2` is written
last with flag bit `0x4`, and each entry from there up to seven gets `0xFF` in its first byte only, the other
three bytes left as they were³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00583DC2`-`0x00583EEB` |
| ² | `0x003271D0` |
| ³ | `0x00583EE0` |

</details>

The third byte is stored as a byte, so it holds `(+0x86 << 4) & 0xF0` ORed with the whole byte `+0x87`¹. Of several pages with flag bit `0x2` only the last is kept². Its entry's bit
`0x2` is not taken from that page: the test reads the page pointer left by the loop's last call, `0x00282DF0(8)`, so
the bit is set when page 8's word `+0x60` is not negative and its dword `+0` has bit `0x400`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00583DF1`-`0x00583E01` |
| ² | `0x00583DD8` |
| ³ | `0x00583E70`-`0x00583E7F` |

</details>

The loop does not stop at seven entries: an eighth would land on `+0x3C`, which the Esper store overwrites¹, and a ninth on `+0x40`, which the counter store overwrites only when story flag `0x400B` is set². The flags byte `+0x57` is only ORed³, so a bit already set in
the destination stays set. The clan rank at `+0x44` is the low byte of `0x00315390()`⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00583F0D` |
| ² | `0x00583F27` |
| ³ | `0x00583F63`, `0x00583F70`, `0x00583F7D` |
| ⁴ | `0x00583F2F` |

</details>

### The checksum

`0x003BB220(data, length)` is the reflected CRC-32: state `0xFFFFFFFF`, eight shift-and-xor steps
per byte with `0xEDB88320`, final complement; a non-positive length returns 0 without reading.

- The finaliser `0x00583D60` feeds it the active image's `+8` for `0xE1F8` bytes (`0x00583F81`-`0x00583F92`,
  always the active buffer even when its destination is the capture buffer), and stores the result
  at the destination's `+0xE200` and its complement at `+0x00`¹.
- The submit `0x0057E310` recomputes it over the same bytes of the active buffer and stores the plain
  value at the written image's `+0x00`².
- Nothing on the load path recomputes or compares it: the function's only callers are those two
 ³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00583F99`-`0x00583FA1` |
| ² | `0x0057E3A9`-`0x0057E3BF` |
| ³ | `0x00583F92`, `0x0057E3BA` |

</details>

### The four image buffers

| Buffer | Address | Accessor | Role |
|---|---|---|---|
| active | `0x02164280` | `0x002EF640` | the live image, updated while playing |
| capture | `0x021BA940` | `0x002EF620` | the finaliser's destination when it is told to write there |
| write | `0x02211000` | `0x002EF630` | what the file write reads; filled from the capture buffer by `0x0057E310` (`0xACD` 128-byte blocks plus 16) and by `0x002EF690` |
| backup | `0x022676C0` | - (no accessor function) | a copy of the active buffer made by `0x002EF570` |

The buffers are `0x566C0` apart, 48 bytes more than the image.

### What lives inside the image

| Image offset | Payload offset | Content |
|---|---|---|
| `+0x01244` | `+0x1044` | the active or pending area id (`0x00584210` stashes the five dwords `+0x1244` to `+0x1257` and stores `0x483` here through `0x00314DC0`, `0x005842D7`-`0x005842DF`) |
| `+0x02200` | `+0x2000` | the copy of the party block head that `0x00235AF0` compares |
| `+0x08200` | `+0x8000` | the image-backed state block, `0x4818` bytes, bound to `0x020927C0` by `0x00253970`; its `+0x47E8` (image `+0xC9E8`) mirrors the play clock |
| `+0x4E68C` | `+0x4E48C` | the party block, 29,712 bytes, bound to `0x02EBF190` by `0x00233C10` (`0x00233C25`-`0x00233C33`) |
| `+0x0E200` | `+0xE000` | the finaliser's checksum copy |

## Loader behaviour

### Reading the container

`0x008666B0` reads the whole file and branches on its first four bytes:

- Not `SAFH` (or shorter than 5 bytes): the file is treated as a raw image and copied byte for
  byte into the stream buffer `0x01F44D40` (`0x008666B0`, the first branch). A plain decoded image is
  therefore accepted as a save.
- `SAFH` but shorter than 13 bytes: nothing is read.
- `SAFH`: `+0x08` must be below 32 and `+0x04` at most `0x100000`¹;
  `0x00865D90` decrypts² and inflates (`0x0080C5A0`, zlib `uncompress`) and the result's
  length must equal `+0x04`³; the image is then copied into the stream.
- `0x00865D90(out, &len, data, size)` gets `+0x04` as `len`, the bytes from `+0x0C` and the file size less 12,
  `size - 12`⁴. It decrypts with `0x00865840` into a scratch block of `len` bytes from
  `_aligned_malloc` with alignment 16⁵, and inflates only when the decrypt answers
  non-zero⁶.
- A non-zero `uncompress` result makes `0x00865D90` answer 0; success stores the inflated length through `&len`
  and answers 1⁷. The scratch block is freed with `_aligned_free` on every path
 ⁸.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00866805`, `0x00866817` |
| ² | `0x00865840` |
| ³ | `0x00866866`-`0x0086686D` |
| ⁴ | `0x00866843`-`0x0086685D` |
| ⁵ | `0x00865DBB`-`0x00865DD9` |
| ⁶ | `0x00865DE3` |
| ⁷ | `0x00865DFB`-`0x00865E0E` |
| ⁸ | `0x00865E13` |

</details>

### Writing the container

`0x00866200` writes `{ "SAFH", length, rotation }`, compresses the stream with `compress2` level 9, encrypts, and writes
to a temporary file `sav_tmp` in the Windows temp directory. When the slot file exists and the flag `0x02B40E04` is set,
the flag is cleared¹ and the previous save is then copied to `sav_org`; on the other path the flag is
cleared at `0x008665D9`. The temporary file is copied over the slot's file (`CopyFileW`), and on failure `sav_org` is
copied back when one was made, else the slot file is removed.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x008665B7` |

</details>

"When one was made" is a word that outlives the save. `0x00866200` loads it¹ and zeroes it only while
`0x02B40E04` is set²; with the flag clear it keeps whatever an earlier save left there. So a
failed copy after a save without the flag can restore the `sav_org` of an earlier save:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00866593` |
| ² | `0x00866599`-`0x008665A9` |

</details>

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EB386C` | `i32` | 0 (zero-filled tail of `.data`) | non-zero when the `sav_org` copy succeeded | `0x00866200`: its old value, or 0 while `0x02B40E04` is set (`0x008665A9`); the `CopyFileW` result of the backup (`0x008665CD`) | `0x00866200`: `0x00866593`; `0x008665F3`, after a failed copy, to choose between copying `sav_org` back and removing the slot file |

The two paths are the temp directory (`GetTempPathW`, 260 characters) joined with the wide names at `0x01CCFD70` and
`0x01CCFD80` by `0x008656B0(out, directory, name)`, which appends the name to the directory string¹ and moves
the result into `out`². Nothing else enters either path³:
there is no per-process or per-slot part, and every save uses the same two files.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00865FF0` |
| ² | `0x008662C3`, `0x00866328` |
| ³ | `0x00866248`-`0x00866268`, `0x0086626C` |

</details>

The slot file's path is the object's `+0x08`, the wide copy of the path that `0x008666B0(path, mode)` keeps there¹; `0x00866200` uses it at `0x0086635A`, `0x00866579`, `0x008665BD`, `0x008665E2`, `0x008665FE` and
`0x0086660D`. All three `CopyFileW` calls pass `bFailIfExists` 0, and the copy of `sav_org` back over the slot file is
at `0x00866605`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00866730`-`0x0086673F` |

</details>

`0x00866200` answers 0 or -1¹. Its argument is the open file's object at `0x02EAF8E8`, which both
callers pass²:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00866672`, `0x0086652A` |
| ² | `0x00862508`, `0x008620F4` |

</details>
- 0 at once, writing nothing, when the object's dword `+4`, the `mode` that `0x008666B0(path, mode)` keeps there
 ¹, is not 0 (`0x0086623F`-`0x00866242`, to `0x00866663`; `esi` is 0 from `0x00866238`-`0x0086623D`).
- -1 when `_wfopen_s`² cannot open `sav_tmp` (`0x00866396`-`0x0086639E`, to `0x008664D4`; `edi` is -1 from
  `0x00866272`).
- 0 when `compress2`³ fails⁴ or `0x00865AE0` answers 0⁵: the
  test at `0x008664AE`-`0x008664B3` falls through, `sav_tmp` is closed by `fclose`⁶ with only its
  12-byte header written by `fwrite`⁷, and `edi` becomes 0⁸. The slot
  file is not written, and the 0 is the same answer as a save that succeeds.
- -1 when the body's `fwrite`⁹ writes fewer bytes than the encrypted length (`0x00866547`-`0x00866555`,
  `0x0086656A`, to `0x00866619`): nothing is copied and the slot file keeps the previous save. The header's `fwrite` has
  no test of its result.
- -1 when the backup `CopyFileW`¹⁰ to `sav_org` fails (`0x008665C7`-`0x008665D7`, to `0x00866617`; on success the
  test at `0x008665D3`-`0x008665D5` goes on to the copy over the slot): the slot file keeps the previous save.
- -1 after a failed `CopyFileW`¹¹ over the slot (`0x008665E9`-`0x008665F1`, then `0x00866617`), and 0 when that
  copy succeeds.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00866726` |
| ² | `0x008C2E00` |
| ³ | `0x0087AF40` |
| ⁴ | `0x0086646C`-`0x0086647A` |
| ⁵ | `0x00866493`-`0x00866498` |
| ⁶ | `0x008C2F00`, `0x008664C2` |
| ⁷ | `0x008C2F40`, `0x008663FB` |
| ⁸ | `0x008664D0`-`0x008664D2` |
| ⁹ | `0x008C2F40` |
| ¹⁰ | `0x008C23E8` |
| ¹¹ | `0x008C23E8` |

</details>

Every answer but the first comes after `SetFileAttributesW`¹ has set the attributes of the slot file,
`sav_tmp` and `sav_org` to 0², which runs before `sav_tmp` is opened. No exit
removes `sav_tmp`: the one `_wremove`³ is of the slot file.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x008C23F8` |
| ² | `0x0086636B`, `0x00866376`, `0x00866381` |
| ³ | `0x008C2B08`, `0x00866611` |

</details>

### What a load checks

| Step | What happens | Where in the code |
|---|---|---|
| 1 | `0x00255260(header + 0x68)`: when the pair is not both zero, `+0x68` must be `0x0131F3EA` and `+0x6C` must be `0x4818`, else the header is invalid. |   |
| 2 | `0x00235AF0` (the prelude of the guard `0x00233C10`, `0x00233C14`) compares the block at `0x02EBF190` with the image's copy at `+0x2200`: its first two dwords, its byte `+0x5B42` and its word `+0x5B12`.<br>• On any difference the 40 members' gambit banks are rebuilt: three `0x34`-byte banks per member at block `+0x5B10 + k × 0x9C` ([gambits](../Enemy-AI-And-Gambits/gambits.md)).<br>• The selected bank `+0x7370 + 4k` is set to 0.<br>• Bank 0 is copied from the selected bank the member record keeps (block `+0x90 + k × 0x1C8`, `0x34` bytes), which `0x00234ED0` stores there before each capture ([save data fields](save-data-fields.md)).<br>• Banks 1 and 2 are filled from the gambit preset the member's party table row names (word `+0x14` of `[0x02EBF130]`, a row of `[0x02EBF0E0]` at id `0x5000` + row). Each filled slot's bit is set in the bank's `+0x30`, and byte `+0x32` is taken from the record's `+0xBA`.<br>• `0x002EF4A0` first copies `0x6000` bytes from `0x02166480` to `0x021B290C`, `0xC0` passes of `0x80` bytes. | `0x00235B83`-`0x00235D7E`<br>`0x002EF4A7`, `0x002EF500` |
| 3 | `0x00233C10`: with no block bound, it binds `0x02EBF190` to the active image `+0x4E68C`, rebases the inventory descriptors and runs the battle reset `0x00237DF0` twice. With a block, the first dword must equal `0x05071901`; otherwise `0x00237DF0` runs, which reaches `0x002370C0`: the block is zeroed, stamped, and its seats at `+0x5A48` filled with `0xFFFF`.<br>• `0x002370C0` fills only map 0's nine seats, the words `+0x5A48`-`+0x5A58`, empties the inventory lists with `0x003047F0` and clears the dwords `+0x5AC8` and `+0x5ACC`, the walked distance (`0x00237118`-`0x0023712E`; [Party data](../Party/party-data.md)).<br>• With the magic in place it sets bit `0x1000` of the flag dword `+0x04` when bit `0x1` of `0x02089344` is set, clearing that bit and zeroing the dword `+0x5B00`, the word `+0x5B0C` and the byte `+0x5B0E`; otherwise it clears bit `0x1000`.<br>• It then rebuilds the gambit order sets, clears bit `0x2` of the word `+0x5AD0` (`0x003139A0(0)`) and bit `0x1` of the dword `+0x5AE0` (`0x00304770(0)`), empties the trap ring `0x02EC3EA0` and the presence ledger `0x02EC3E60`, sets the speed index `0x01FD4A98` to 0 (`0x00229ED0(0)`, `0x00233CD1`) and stores 0 at `0x0208E6B4`. | `0x0030B6A0`<br>`0x00233C3F`, `0x00233C48`<br>`0x00233C4D`<br>`0x00233C59`<br>`0x002370C0`<br>`0x002370EA`-`0x00237116`<br>`0x002370E5`<br>`0x00233C65`-`0x00233CA6`<br>`0x00327F80`, `0x00233CAD`<br>`0x002FA230`<br>`0x002FA260`<br>`0x00233CD6` |
| 4 | `0x00584210`, called from the load lifecycle `0x00582860`, handles the stash:<br>• load mode `0x00394450()` = 3 with header flag bit `0x1` clear:<br>• the play clock `+0x10` to `+0x1B` is copied to `+0x70` to `+0x7B`, the walked total `0x00320D50()` to `+0x7C`, and the five transition dwords `+0x1244` to `+0x1257` to `+0x80` to `+0x93`;<br>• the entrance word `+0x1248` is then zeroed, bit `0x1` of the battle block's `+0x5B04` is cleared, the tick count and the hours, minutes and seconds dword are zeroed, `0x00322200` zeroes the walked pair at the battle block's `+0x5AC8` and `+0x5ACC`, and the header's walked mirror `+0x0C` is zeroed;<br>• `0x00314DC0` stores `0x483` as the destination field `+0x1244`; the previous field, previous entrance and mode words `+0x124C` to `+0x1257` keep their values;<br>• any other mode with flag bit `0x1` set:<br>• the stash is restored: `+0x70` to `+0x7B` back to `+0x10` to `+0x1B`, `+0x7C` to the walked mirror `+0x0C`, and `+0x80` to `+0x93` back to `+0x1244` to `+0x1257`;<br>• `0x00329E40(walked)` re-seats the accumulator, `0x00269A20(image + 0xE240)` and `0x002EF410(image + 0x4E660)` run, the flag is cleared, `0x01E0C3EC` is zeroed, bit `0x1` of the battle block's `+0x5B04` is cleared and `0x0023A390(0)` clears the block's `+4` bit `0x1000`.<br>• load mode 3 with the flag set, and any other mode with it clear, run neither path.<br>• Both paths, and the two combinations that skip them, then call `0x00316810` (`0x00584398`, [achievements](../Steam-And-Achievements/achievements.md)) and reseed the gameplay generator from the clock (see the [random number generators page](../Random-Numbers/random-number-generators.md)). | `0x00582EBA`<br>`0x00584255`-`0x005842B1`<br>`0x005842B7`<br>`0x005842BD`-`0x005842C4`<br>`0x005842CB`, `0x005842CF`<br>`0x005842D2`<br>`0x005842DC`<br>`0x005842D7`-`0x005842DF`<br>`0x005842F9`-`0x00584362`<br>`0x0058436D`<br>`0x0058437D`-`0x0058438C`<br>`0x0058424F`, `0x005842F3` |

### What is initialised at boot

`0x002EF650` clears the active image, calls `0x00253A80` and `0x002EF2D0`, then `0x00238A80`. `0x00253A80`
zeroes the two state blocks (`[0x02092758]`, `0x58` bytes; `[0x020927C0]`, `0x4818` bytes) and writes
the six header constants at `+0x58`-`+0x6C` from their getters¹ and literals². It runs `0x00253240(i, 1)` for the twelve
inventory classes³, installs the in-game options defaults with `0x002DDE60`⁴ and zeroes four ranges of the block (`0x00253B2F`-`0x00253B84`,
[save data fields](save-data-fields.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EF2A0`, `0x002EF290`, `0x00235E90`, `0x00235E80` |
| ² | `0x00253AED`, `0x00253AFB` |
| ³ | `0x00253B02`-`0x00253B13` |
| ⁴ | `0x00253B2A` |

</details>

The debug verb `0x209C` loads development slot
images (`0x002EF300`: slot clamped to 0-15, resource kind 1, index `0x75 + slot`, `0xE240` bytes into
the active buffer).

The slot images ship as `ps2data/image/ff12/katano/ff12savedata00.sav` to `ff12savedata15.sav`: the file
size tables size kind 1 ids 117 to 132 at exactly these files' sizes in order (57,864 bytes for 00 to 03, 49,664
for 04 to 06 and 15, 22,016 for 07 to 14), and give those ids no path in this build.

`0x002EF300` reads them (kind 1, index `0x75` + slot), and its one caller is `debug_loadjfdata` (verb `0x209C`, `0x0050D9A0`), which
none of the 1,114 US scripts calls. Replacing a `.sav` here changes nothing in the US game.

`0x0050D9A0` takes the slot from `0x00267E10(fourth argument)`¹. It calls `0x00254CB0(1)` and
`0x00266D00()` before the read `0x002EF300(slot)`, `0x0032E520(0)` and `0x00254CB0(0)` after it, then `0x0036FCC0()` and
`0x0026B8E0(i)` for i = 0 to 3².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0050D9A6`-`0x0050D9B3` |
| ² | `0x0050D9B5`-`0x0050D9EC` |

</details>

[`slot-image-regions.tsv`](slot-image-regions.tsv) gives every region of the sixteen images, one row per file, with its
value and the instructions that identify it. Kind A (00 to 03) has its block at `0x2200` with member records of `0x1C4`
bytes, kind B (04 to 06 and 15) at `0x2200` with `0x190`, kind C (07 to 14) at `0x15F4` with `0x140`. The table
identifies 29.37% of kind A's bytes, 17.22% of B's and 32.11% of C's; 70.08%, 77.31% and 50.74% are zero in every
file of the kind.

### Columns of slot-image-regions.tsv

| Column | Holds |
|---|---|
| `nonzero_bytes` | the number of the region's bytes that are not zero in that file, from 0 to `size` (3,814 at most); 0 on 7,181 of the 12,320 rows |
| `evidence` | how the region is identified: `zero in every file of the kind` on the 5,432 rows of regions that are zero in all files of their kind; otherwise the instructions that write or read the field and the checks its value passes in the shipped files, marked `(holds in this record)` where the check is made for that record |

## Modding notes

- A save editor must decrypt and inflate the body before any offset applies; file offset `0x1244`
  is not the area id, image offset `0x1244` is. A raw decoded image written back without the
  container is accepted by the reader.
- Editing `+0x58`, `+0x5C` or `+0x64` cannot make a save fail to load through the functions on
  this page: none of them reads those three back (`0x002EF2D0` clears `0x1538` bytes from the
  getter's value, not from the header). `+0x60` is compared only inside the battle block at image
  `+0x4E68C`, and a mismatch there rebuilds the block.
- The checksum is not verified on load, so an edited image needs no checksum fix.
- The image size is this build's: the reader honours `+0x04`. `0x00235AF0` rebuilds only the gambit
  banks and reads the 40 member records at this build's `0x1C8`-byte stride¹, so a block
  with shorter records is read further off for each later member.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00235D67` |

</details>

## Related

- [Saving and loading: the save slots and their files, the save screen's states, the six-step save transaction, the storage queue, the file layer's read and write rules, the area-change autosave and what a load runs](saving-and-loading.md)
- [Save data fields: the regions of the save payload, who writes and reads each, and the access table](save-data-fields.md)
- [Languages: the Language setting, the nine language codes, the locale id each maps to, the data folder it selects, the Windows-locale default, and the confirm and cancel buttons](languages.md)
- [Random number generators: the gameplay Mersenne Twister, the shared gameplay LCG, the graphics-noise Mersenne Twister, the C runtime rand, the presentation bit-feedback generator, the emulated VU1 generator, the counter hash and the PPFX xorshift, with their constants, seeds and states](../Random-Numbers/random-number-generators.md)
- [Gil: storage, the gil cap, every way gil changes, and the Plunderer and Spendthrift counters](../Rewards-EXP-Gil-And-Loot/gil.md)
- [`save-image-accesses.tsv`](save-image-accesses.tsv): every access through a register holding the address
  of one of the four image buffers¹ or loaded from `[0x02092758]`, one
  row per instruction (689 rows).
- [`save-header-accesses.tsv`](save-header-accesses.tsv): every access to the header fields at the start of
  the image (`+0x0` to `+0xB0`), one row per instruction, by 25 functions (199 rows). Its columns are those of the
  access tables on [Save data fields](save-data-fields.md#related), with `disp` measured from the start of the image;
  17 of its sites are also rows of `save-image-accesses.tsv`, with the same offset, kind and instruction.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x02164280`, `0x021BA940`, `0x02211000`, `0x022676C0` |

</details>

---

[← Loading a save](loading-a-save.md) | [Save data fields →](save-data-fields.md)
