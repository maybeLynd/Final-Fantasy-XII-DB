---
title: "Save file format: the SAFH container, its zlib and RC4 layers, the save image and its header fields, the four in-memory copies and the format stamps"
kind: "format"
category: "Saving, loading and settings"
addresses: "0x008666B0, 0x00866200, 0x00865840, 0x00865D90, 0x002EF640, 0x00583D60, 0x0057E310, 0x003BB220, 0x00253A80, 0x00255260, 0x00233C10, 0x002370C0, 0x00584210, 0x00862A40"
---

## What the player sees

A save is one file per slot, FFXII_000 and up, in the game's folder under Documents. It is small on
disk because the game compresses and encrypts a much larger image before writing it.

- The image carries what the slot list shows (the party, their levels and jobs, the leader, the
  play time, the gil and the area) and everything else that persists.
- The game keeps that image in memory while you play and copies it when you save.
- Loading checks a few stamps. An image whose battle-state stamp does not match is not partly
  accepted but rebuilt from scratch; a save written by an older build with a smaller battle block
  loads with its party records migrated.

## Where it comes from

The save directory is built by `0x00862A40`: the Documents folder (`SHGetFolderPathW`, CSIDL 5), then
`\My Games\` (`0x01F44D08`), then `FINAL FANTASY XII THE ZODIAC AGE` (`0x01F44D10`), then, when the
user-id string from `0x001F3ED0` is non-empty, that id and a backslash; the result is kept at
`0x02EAF6E0`, created on first use, and `0x00862A20` returns it. A slot's file name is `FFXII_` (`0x003935C0`)
followed by the three-digit slot number (`sprintf("%s%03d")` in `0x0057E310` and `0x00584610`); the slot icon
assets are named `icon.sys` and `static.ico` by the same formatter.

The container is read by `0x008666B0(path, mode)`, called from the stream opener `0x008624D0`
(`0x00862543`), and written by `0x00866200`, called from `0x008624D0` (`0x00862508`) and the stream closer
`0x008620E0` (`0x008620F4`).

## Layouts

All multi-byte fields are little-endian.

### The container on disk

`SaveFileContainer` (`0xC` bytes, offsets from the start of the file):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[4]` | magic | "SAFH"; `0x008666B0` rejects anything else as a container (see Loader behaviour) |
| `+0x04` | `u32` | size | the decoded image size, `0x56690` in this build; must be at most `0x100000` (`0x00866817`) |
| `+0x08` | `u32` | rotation 0-31, the key rotation; must be below 32 (0x00866805); kept at 0x02EB3868 |  |

The body from `+0x0C` to the end of the file is the image, compressed with zlib `compress2` at
level 9 (`0x0087AF40`, called from `0x00866200` with level 9) and then encrypted with RC4 by
`0x00865AE0`.

### The key

Both directions derive the key the same way (`0x00865840`):

1. `CryptAcquireContextW` with container `RSA_SQEX_FFXII_TZA` and the Microsoft Enhanced
   Cryptographic Provider v1.0, type 1, retried with `CRYPT_NEWKEYSET` (`0x008658AF`-`0x008658D6`).
2. `CryptCreateHash(CALG_MD5)` (`0x8003`).
3. The 32-character title `FINAL FANTASY XII THE ZODIAC AGE` is rotated left by the container's
   rotation (`strncpy` and two `memcpy`, `0x0086592C`-`0x0086595C`) and its 32nd byte set to NUL
   (`0x00865961`), so 31 characters are hashed (`CryptHashData`, `0x00865985`).
4. `CryptDeriveKey(CALG_RC4 = 0x6801, flags 0x00800000)`: a 128-bit RC4 key (`0x008659AF`).
5. `CryptDecrypt` (or `CryptEncrypt`) over the body in 1,000-byte chunks, the last one marked
   final (`0x008659C2`-`0x00865A31`).

The writer draws the rotation as `abs(rand()) mod 32` (`0x008663C5`-`0x008663ED`).

### The image

`SaveImage` (`0x56690` bytes, offsets from the start of the image):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u8[512]` | header | see below |
| `+0x200` | `u8[353424]` | payload | the persistent payload; `0x002EF2B0` returns its address |

The image is 353,936 bytes: the clear `0x002EF5F0` and the boot initialiser `0x002EF650` memset that
many, the copy to the write buffer passes it (`0x002EF690`), and the submit records it at the
descriptor's `+0x100` (`0x0057E310`).

### The header

`SaveImageHeader` (`0x200` bytes, offsets from the start of the image):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | checksum | in the file: CRC-32 of image[`0x08`, `0xE200`) (`0x0057E3BF`); the finaliser writes its complement here first (`0x00583FA1`) |
| `+0x04` | `u32` | one | 1 in the written image (`0x0057E3C7`) |
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
| `+0x48` | `u32` | mapgroup | the area's map persistence group: `0x00254380`(`0x00264F90`(areaId)) |
| `+0x4C` | `u32` | area | the active or pending area id (`0x003148F0`) |
| `+0x50` | `u32` | savecount 0x00583D60's second argument (the controller's +0xD0); in the written image the save counter 0x02CA99B4, saturating at 0xFFFFFFFF (0x0057E3CE-0x0057E3DD) |  |
| `+0x54` | `u8` | slot | `0x00583D60`'s first argument: the save slot (controller `+0xCD` from `0x00581DA0` at `0x00581EE7`; 0 from `0x005844A0` at `0x005844BE`) |
| `+0x55` | `u8[2]` | pad2 | not written by the enumerated writers |
| `+0x57` | `u8` | flags | bit `0x1` from `0x00236760` (Trial Mode stash pending), bit `0x2` from `0x00236740` (New Game+), bit `0x4` from `0x00236780` (New Game-) (`0x00583F5A`-`0x00583F7D`) |
| `+0x58` | `u32` | date | constant `0x20050223`, written by `0x00253A80` and never read |
| `+0x5C` | `u32` | clearsize constant 0x1538, the size 0x002EF2DD clears at payload +0 |  |
| `+0x60` | `u32` | stamp | constant `0x05071901`, the battle-state block's stamp |
| `+0x64` | `u32` | blocksize constant 0x7410, the battle-state block's size |  |
| `+0x68` | `u32` | magic2 | `0x0131F3EA`, tested by `0x00255260` |
| `+0x6C` | `u32` | size2 | `0x4818`, tested by `0x00255260`; the image-backed state block's size |
| `+0x70` | `u8[36]` | stash | the mode-3 stash: `+0x70` ticks, `+0x78` hours, `+0x7A` minutes, `+0x7B` seconds, `+0x7C` walked (`0x00320D50`), `+0x80` to `+0x93` the five dwords of the world-transition record (`0x00584210`; the last stored at `0x005842B1` and read back at `0x0058435C`) |
| `+0x94` | `u8[364]` | rest | zeroed by the image clears; not written by the enumerated writers |

The roster loop (`0x00583DC2`-`0x00583EEB`) walks party pages 0-8 from `0x00282DF0(page)`, skips a page
whose word `+0x60` is negative or whose flag bit `0x2` is set, and writes for each page `{+0x60 low
byte, +0xBA, +0x86 << 4 | +0x87, flags}` with flag bit `0x1` when the page is the leader
(`0x003271D0`), bit `0x2` when the page's dword `+0` has bit `0x400`; the page with flag bit `0x2` is written
last with flag bit `0x4`, and entries up to seven are filled with `0xFF`.

### The checksum

`0x003BB220(data, length)` is the reflected CRC-32: state `0xFFFFFFFF`, eight shift-and-xor steps
per byte with `0xEDB88320`, final complement; a non-positive length returns 0 without reading.

- The finaliser `0x00583D60` feeds it the active image's `+8` for `0xE1F8` bytes (`0x00583F81`-`0x00583F92`,
  always the active buffer even when its destination is the capture buffer), and stores the result
  at the destination's `+0xE200` and its complement at `+0x00` (`0x00583F99`-`0x00583FA1`).
- The submit `0x0057E310` recomputes it over the same bytes of the active buffer and stores the plain
  value at the written image's `+0x00` (`0x0057E3A9`-`0x0057E3BF`).
- Nothing on the load path recomputes or compares it: the function's only callers are those two
  (`0x00583F92`, `0x0057E3BA`).

### The four image buffers

| Buffer | Address | Accessor | Role |
|---|---|---|---|
| active | `0x02164280` | `0x002EF640` | the live image, updated while playing |
| capture | `0x021BA940` | `0x002EF620` | the finaliser's destination when it is told to write there |
| write | `0x02211000` | `0x002EF630` | what the file write reads; filled from the capture buffer by `0x0057E310` (`0xACD` 128-byte blocks plus 16) and by `0x002EF690` |
| backup | `0x022676C0` | none | a copy of the active buffer made by `0x002EF570` |

The buffers are `0x566C0` apart, 48 bytes more than the image.

### What lives inside the image

| Image offset | Payload offset | Content |
|---|---|---|
| `+0x01244` | `+0x1044` | the active or pending area id (`0x00584210` stashes the five dwords `+0x1244` to `+0x1257` and stores `0x483` here through `0x00314DC0`, `0x005842D7`-`0x005842DF`) |
| `+0x02200` | `+0x2000` | the copy of the battle-state block head that `0x00235AF0` compares |
| `+0x08200` | `+0x8000` | the image-backed state block, `0x4818` bytes, bound to `0x020927C0` by `0x00253970`; its `+0x47E8` (image `+0xC9E8`) mirrors the play clock |
| `+0x4E68C` | `+0x4E48C` | the battle-state block, 29,712 bytes, bound to `0x02EBF190` by `0x00233C10` (`0x00233C25`-`0x00233C33`) |
| `+0x0E200` | `+0xE000` | the finaliser's checksum copy |

## Loader behaviour

### Reading the container

`0x008666B0` reads the whole file and branches on its first four bytes:

- Not `SAFH` (or shorter than 5 bytes): the file is treated as a raw image and copied byte for
  byte into the stream buffer `0x01F44D40` (`0x008666B0`, the first branch). A plain decoded image is
  therefore accepted as a save.
- `SAFH` but shorter than 13 bytes: nothing is read.
- `SAFH`: `+0x08` must be below 32 and `+0x04` at most `0x100000` (`0x00866805`, `0x00866817`);
  `0x00865D90` decrypts (`0x00865840`) and inflates (`0x0080C5A0`, zlib `uncompress`) and the result's
  length must equal `+0x04` (`0x00866866`-`0x0086686D`); the image is then copied into the stream.

### Writing the container

`0x00866200` writes `{ "SAFH", length, rotation }`, compresses the stream with `compress2` level 9,
encrypts, and writes to a temporary file `sav_tmp` in the Windows temp directory. When the slot
file exists and the flag `0x02B40E04` is set, the previous save is first copied to `sav_org` (the
flag is then cleared); the temporary file is copied over the slot's file (`CopyFileW`), and on
failure `sav_org` is copied back when one was made, else the slot file is removed.

"When one was made" is a word that outlives the save. `0x00866200` loads it (`0x00866593`) and zeroes it only while
`0x02B40E04` is set (`0x00866599`-`0x008665A9`); with the flag clear it keeps whatever an earlier save left there. So a
failed copy after a save without the flag can restore the `sav_org` of an earlier save:

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EB386C` | `i32` | 0 (zero-filled tail of `.data`) | non-zero when the `sav_org` copy succeeded | `0x00866200`: its old value, or 0 while `0x02B40E04` is set (`0x008665A9`); the `CopyFileW` result of the backup (`0x008665CD`) | `0x00866200`: `0x00866593`; `0x008665F3`, after a failed copy, to choose between copying `sav_org` back and removing the slot file |

The two paths are the temp directory (`GetTempPathW`, 260 characters) joined with the wide names at `0x01CCFD70`
and `0x01CCFD80` by `0x008656B0(out, directory, name)`, which appends the name to the directory string
(`0x00865FF0`) and moves the result into `out` (`0x008662C3`, `0x00866328`).

### What a load checks

1. `0x00255260(header + 0x68)`: when the pair is not both zero, `+0x68` must be `0x0131F3EA` and
   `+0x6C` must be `0x4818`, else the header is invalid.
2. `0x00235AF0` (the prelude of the guard `0x00233C10`, `0x00233C14`) compares the block at `0x02EBF190`
   with the image's copy at `+0x2200`: its first two dwords, its byte `+0x5B42` and its word
   `+0x5B12`.
   - On any difference the 40 members' gambit banks are rebuilt (`0x00235B83`-`0x00235D7E`): three `0x34`-byte banks
     per member at block `+0x5B10 + k × 0x9C` ([gambits](../Enemy-AI-And-Gambits/gambits.md)).
     - The selected bank `+0x7370 + 4k` is set to 0.
     - Bank 0 is copied from the member record's older gambit block (block `+0x90 + k × 0x1C8`, `0x34` bytes).
     - Banks 1 and 2 are filled from the gambit preset the member's party table row names (word `+0x14` of
       `[0x02EBF130]`, a row of `[0x02EBF0E0]` at id `0x5000` + row). Each filled slot's bit is set in the bank's
       `+0x30`, and byte `+0x32` is taken from the record's `+0xBA`.
   - `0x002EF4A0` first copies `0xC00` bytes from `0x02166480` to `0x021B290C`.
3. `0x00233C10`: with no block bound, it binds `0x02EBF190` to the active image `+0x4E68C`, rebases the
   inventory descriptors (`0x0030B6A0`) and runs the battle reset `0x00237DF0` twice (`0x00233C3F`,
   `0x00233C48`). With a block, the first dword must equal `0x05071901` (`0x00233C4D`); otherwise
   `0x00237DF0` runs (`0x00233C59`), which reaches `0x002370C0`: the block is zeroed, stamped, and its
   party arrays at `+0x5A48` filled with `0xFFFF` (`0x002370C0`).
4. `0x00584210`, called from the load lifecycle `0x00582860` (`0x00582EBA`), handles the stash:
   - load mode `0x00394450()` = 3 with header flag bit `0x1` clear:
     - the play clock `+0x10` to `+0x1B` is copied to `+0x70` to `+0x7B`, the walked total
       `0x00320D50()` to `+0x7C`, and the five transition dwords `+0x1244` to `+0x1257` to `+0x80` to
       `+0x93` (`0x00584255`-`0x005842B1`);
     - the entrance word `+0x1248` is then zeroed (`0x005842B7`), bit `0x1` of the battle block's `+0x5B04` is
       cleared (`0x005842BD`-`0x005842C4`), the tick count and the hours, minutes
       and seconds dword are zeroed (`0x005842CB`, `0x005842CF`), `0x00322200` zeroes the walked pair at the
       battle block's `+0x5AC8` and `+0x5ACC` (`0x005842D2`), and the header's walked mirror `+0x0C` is
       zeroed (`0x005842DC`);
     - `0x00314DC0` stores `0x483` as the destination field `+0x1244` (`0x005842D7`-`0x005842DF`); the
       previous field, previous entrance and mode words `+0x124C` to `+0x1257` keep their values;
   - any other mode with flag bit `0x1` set: the stash is restored, `0x00329E40(walked)` re-seats the
     accumulator, `0x00269A20(image + 0xE240)` and `0x002EF410(image + 0x4E660)` run, the flag is
     cleared, `0x01E0C3EC` is zeroed, bit `0x1` of the battle block's `+0x5B04` is cleared
     (`0x0058437D`-`0x0058438C`) and `0x0023A390(0)` clears the block's `+4` bit `0x1000`.
   - Both paths then reseed the gameplay generator from the clock (see the
     [random number generators page](../Random-Numbers/random-number-generators.md)).

### What is initialised at boot

`0x002EF650` clears the active image, calls `0x00253A80` and `0x002EF2D0`, then `0x00238A80`. `0x00253A80`
zeroes the two state blocks (`[0x02092758]`, `0x58` bytes; `[0x020927C0]`, `0x4818` bytes) and writes
the six header constants at `+0x58`-`+0x6C` from their getters (`0x002EF2A0`, `0x002EF290`, `0x00235E90`,
`0x00235E80`) and literals (`0x00253AED`, `0x00253AFB`). The debug verb `0x209C` loads development slot
images (`0x002EF300`: slot clamped to 0-15, resource kind 1, index `0x75 + slot`, `0xE240` bytes into
the active buffer).

## Modding notes

- A save editor must decrypt and inflate the body before any offset applies; file offset `0x1244`
  is not the area id, image offset `0x1244` is. A raw decoded image written back without the
  container is accepted by the reader.
- Editing `+0x58`, `+0x5C` or `+0x64` cannot make a save fail to load through the functions on
  this page: none of them reads those three back (`0x002EF2D0` clears `0x1538` bytes from the
  getter's value, not from the header). `+0x60` is compared only inside the battle block at image
  `+0x4E68C`, and a mismatch there rebuilds the block.
- The checksum is not verified on load, so an edited image needs no checksum fix.
- The image size is this build's: the reader honours `+0x04`, and the party-record migration in
  `0x00235AF0` is what accepts an older block layout.

## Related

- [Languages: the Language setting, the nine language codes, the locale id each maps to, the data folder it selects, the Windows-locale default, and the confirm and cancel buttons](languages.md)
- [Random number generators: the gameplay Mersenne Twister, the shared gameplay LCG, the graphics-noise Mersenne Twister, the C runtime rand, the presentation bit-feedback generator, the counter hash and the PPFX xorshift, with their constants, seeds and states](../Random-Numbers/random-number-generators.md)
- [Gil: storage, the gil cap, every way gil changes, and the Plunderer and Spendthrift counters](../Rewards-EXP-Gil-And-Loot/gil.md)
