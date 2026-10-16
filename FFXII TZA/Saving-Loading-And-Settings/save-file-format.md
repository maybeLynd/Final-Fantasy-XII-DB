---
title: "Save file format: the SAFH container, its zlib and RC4 layers, the save image and its header fields, the four in-memory copies and the format stamps"
kind: "format"
category: "Saving, loading and settings"
addresses: "008666B0, 00866200, 00865840, 00865D90, 002EF640, 00583D60, 0057E310, 003BB220, 00253A80, 00255260, 00233C10, 002370C0, 00584210, 00862A40"
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

The save directory is built by `00862A40`: the Documents folder (`SHGetFolderPathW`, CSIDL 5), then
`\My Games\` (`01F44D08`), then `FINAL FANTASY XII THE ZODIAC AGE` (`01F44D10`), then, when the
user-id string from `001F3ED0` is non-empty, that id and a backslash; the result is kept at
`02EAF6E0`, created on first use, and `00862A20` returns it. A slot's file name is `FFXII_` (`003935C0`)
followed by the three-digit slot number (`sprintf("%s%03d")` in `0057E310` and `00584610`); the slot icon
assets are named `icon.sys` and `static.ico` by the same formatter.

The container is read by `008666B0(path, mode)`, called from the stream opener `008624D0`
(`00862543`), and written by `00866200`, called from `008624D0` (`00862508`) and the stream closer
`008620E0` (`008620F4`).

## Layouts

### The container on disk

`SaveFileContainer` (`0xC` bytes, offsets from the start of the file):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u8[4]` | magic | "SAFH"; `008666B0` rejects anything else as a container (see Loader behaviour) |
| `04` | `u32` | size | the decoded image size, `0x56690` in this build; must be at most `0x100000` (`00866817`) |
| `08` | `u32` | rotation 0-31, the key rotation; must be below 32 (00866805); kept at 02EB3868 |  |

The body from `+0x0C` to the end of the file is the image, compressed with zlib `compress2` at
level 9 (`0087AF40`, called from `00866200` with level 9) and then encrypted with RC4 by
`00865AE0`.

### The key

Both directions derive the key the same way (`00865840`):

1. `CryptAcquireContextW` with container `RSA_SQEX_FFXII_TZA` and the Microsoft Enhanced
   Cryptographic Provider v1.0, type 1, retried with `CRYPT_NEWKEYSET` (`008658AF`-`008658D6`).
2. `CryptCreateHash(CALG_MD5)` (`0x8003`).
3. The 32-character title `FINAL FANTASY XII THE ZODIAC AGE` is rotated left by the container's
   rotation (`strncpy` and two `memcpy`, `0086592C`-`0086595C`) and its 32nd byte set to NUL
   (`00865961`), so 31 characters are hashed (`CryptHashData`, `00865985`).
4. `CryptDeriveKey(CALG_RC4 = 0x6801, flags 0x00800000)`: a 128-bit RC4 key (`008659AF`).
5. `CryptDecrypt` (or `CryptEncrypt`) over the body in 1,000-byte chunks, the last one marked
   final (`008659C2`-`00865A31`).

The writer draws the rotation as `abs(rand()) mod 32` (`008663C5`-`008663ED`).

### The image

`SaveImage` (`0x56690` bytes, offsets from the start of the image):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `000` | `u8[512]` | header | see below |
| `200` | `u8[353424]` | payload | the persistent payload; `002EF2B0` returns its address |

The image is 353,936 bytes: the clear `002EF5F0` and the boot initialiser `002EF650` memset that
many, the copy to the write buffer passes it (`002EF690`), and the submit records it at the
descriptor's `+0x100` (`0057E310`).

### The header

`SaveImageHeader` (`0x200` bytes, offsets from the start of the image):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `u32` | checksum | in the file: CRC-32 of image[`0x08`, `0xE200`) (`0057E3BF`); the finaliser writes its complement here first (`00583FA1`) |
| `04` | `u32` | one | 1 in the written image (`0057E3C7`) |
| `08` | `i32` | gil | written by `00254EE0` (`00254F1F`), read by `00253690` |
| `0C` | `u32` | walked | walked-distance total mirrored from the battle block by `00254E80` (`00254E90`) |
| `10` | `u64` | ticks | play clock, 60 Hz ticks, added by `00254CC0`; its bound is the sign-extended immediate `0xFFFFFFFF80BEFBFF` compared unsigned (`00254CF1`, `00254D30`-`00254D33`), so it never fires |
| `18` | `u16` | hours | (ticks / 216000) mod 10000, by `00254CC0` (`00254DB5`) |
| `1A` | `u8` | minutes | (ticks / 3600) mod 60, by `00254CC0` |
| `1B` | `u8` | seconds | (ticks / 60) mod 60, by `00254CC0` |
| `1C` | `u8[4]` | pad | not written by the enumerated writers |
| `20` | `u8[28] roster` | seven 4-byte entries, 00583D60: character id, level, jobs (high and low nibble), flags; unused entries start with 0xFF |  |
| `3C` | `u32` | esper | the summoned Esper's character row: `003200A0` sets its flag bit 0 when summon mode is on (block +`0x5B04` bit 0, `003135E0`) and copies the row byte block +`0x5AD4` (`003137E0`); `00583D60` stores it, else `0xFF` (`00583F08`-`00583F0D`); the slot pane's ESPER row shows its name when it is not `0xFF` (`0057EFE0`, `0057F0CC`) |
| `40` | `u32` | counter | counter kind `0x11` (`003166F0`) when story flag `0x400B` is set, else untouched |
| `44` | `u32` | clanrank | `00315390`() when story flag `0x400B` is set, else 0 |
| `48` | `u32` | mapgroup | the area's map persistence group: `00254380`(`00264F90`(areaId)) |
| `4C` | `u32` | area | the active or pending area id (`003148F0`) |
| `50` | `u32` | savecount 00583D60's second argument (the controller's +0xD0); in the written image the save counter 02CA99B4, saturating at 0xFFFFFFFF (0057E3CE-0057E3DD) |  |
| `54` | `u8` | slot | `00583D60`'s first argument: the save slot (controller +`0xCD` from `00581DA0` at `00581EE7`; 0 from `005844A0` at `005844BE`) |
| `55` | `u8[2]` | pad2 | not written by the enumerated writers |
| `57` | `u8` | flags | bit 0 from `00236760` (stash pending), bit 1 from `00236740`, bit 2 from `00236780` (`00583F5A`-`00583F7D`) |
| `58` | `u32` | date | constant `0x20050223`, written by `00253A80` and never read |
| `5C` | `u32` | clearsize constant 0x1538, the size 002EF2DD clears at payload +0 |  |
| `60` | `u32` | stamp | constant `0x05071901`, the battle-state block's stamp |
| `64` | `u32` | blocksize constant 0x7410, the battle-state block's size |  |
| `68` | `u32` | magic2 | `0x0131F3EA`, tested by `00255260` |
| `6C` | `u32` | size2 | `0x4818`, tested by `00255260`; the image-backed state block's size |
| `70` | `u8[32] stash` | the mode-3 stash: +0x70 ticks, +0x78 hours, +0x7A minutes, +0x7B seconds, +0x7C walked, +0x80 five dwords of the world-transition record (00584210) |  |
| `90` | `u8[368] rest` | zeroed by the image clears; not written by the enumerated writers |  |

The roster loop (`00583DC2`-`00583EEB`) walks party pages 0-8 from `00282DF0(page)`, skips a page
whose word `+0x60` is negative or whose flag bit 1 is set, and writes for each page `{+0x60 low
byte, +0xBA, +0x86 << 4 | +0x87, flags}` with flag bit 0 when the page is the leader
(`003271D0`), bit 1 when the page's dword `+0` has bit 10; the page with flag bit 1 is written
last with flag bit 2, and entries up to seven are filled with `0xFF`.

### The checksum

`003BB220(data, length)` is the reflected CRC-32: state `0xFFFFFFFF`, eight shift-and-xor steps
per byte with `0xEDB88320`, final complement; a non-positive length returns 0 without reading.

- The finaliser `00583D60` feeds it the active image's `+8` for `0xE1F8` bytes (`00583F81`-`00583F92`,
  always the active buffer even when its destination is the capture buffer), and stores the result
  at the destination's `+0xE200` and its complement at `+0x00` (`00583F99`-`00583FA1`).
- The submit `0057E310` recomputes it over the same bytes of the active buffer and stores the plain
  value at the written image's `+0x00` (`0057E3A9`-`0057E3BF`).
- Nothing on the load path recomputes or compares it: the function's only callers are those two
  (`00583F92`, `0057E3BA`).

### The four image buffers

| Buffer | Address | Accessor | Role |
|---|---|---|---|
| active | `02164280` | `002EF640` | the live image, updated while playing |
| capture | `021BA940` | `002EF620` | the finaliser's destination when it is told to write there |
| write | `02211000` | `002EF630` | what the file write reads; filled from the capture buffer by `0057E310` (`0xACD` 128-byte blocks plus 16) and by `002EF690` |
| backup | `022676C0` | none | a copy of the active buffer made by `002EF570` |

The buffers are `0x566C0` apart, 48 bytes more than the image.

### What lives inside the image

| Image offset | Payload offset | Content |
|---|---|---|
| `+0x1244` | `+0x1044` | the active or pending area id (`00584210` stashes `+0x1244`-`+0x1254`) |
| `+0x2200` | `+0x2000` | the copy of the battle-state block head that `00235AF0` compares |
| `+0x8200` | `+0x8000` | the image-backed state block, `0x4818` bytes, bound to `020927C0` by `00253970`; its `+0x47E8` (image `+0xC9E8`) mirrors the play clock |
| `+0x4E68C` | `+0x4E48C` | the battle-state block, 29,712 bytes, bound to `02EBF190` by `00233C10` (`00233C25`-`00233C33`) |
| `+0xE200` | `+0xE000` | the finaliser's checksum copy |

## Loader behaviour

### Reading the container

`008666B0` reads the whole file and branches on its first four bytes:

- Not `SAFH` (or shorter than 5 bytes): the file is treated as a raw image and copied byte for
  byte into the stream buffer `01F44D40` (`008666B0`, the first branch). A plain decoded image is
  therefore accepted as a save.
- `SAFH` but shorter than 13 bytes: nothing is read.
- `SAFH`: `+0x08` must be below 32 and `+0x04` at most `0x100000` (`00866805`, `00866817`);
  `00865D90` decrypts (`00865840`) and inflates (`0080C5A0`, zlib `uncompress`) and the result's
  length must equal `+0x04` (`00866866`-`0086686D`); the image is then copied into the stream.

### Writing the container

`00866200` writes `{ "SAFH", length, rotation }`, compresses the stream with `compress2` level 9,
encrypts, and writes to a temporary file `sav_tmp` in the Windows temp directory. When the slot
file exists and the flag `02B40E04` is set, the previous save is first copied to `sav_org` (the
flag is then cleared); the temporary file is copied over the slot's file (`CopyFileW`), and on
failure `sav_org` is copied back when one was made, else the slot file is removed.

The two paths are the temp directory (`GetTempPathW`, 260 characters) joined with the wide names at `01CCFD70`
and `01CCFD80` by `008656B0(out, directory, name)`, which appends the name to the directory string
(`00865FF0`) and moves the result into `out` (`008662C3`, `00866328`).

### What a load checks

1. `00255260(header + 0x68)`: when the pair is not both zero, `+0x68` must be `0x0131F3EA` and
   `+0x6C` must be `0x4818`, else the header is invalid.
2. `00235AF0` (the prelude of the guard `00233C10`, `00233C14`) compares the block at `02EBF190`
   with the image's copy at `+0x2200`: its first two dwords, its byte `+0x5B42` and its word
   `+0x5B12`.
   - On any difference the 40 party records are rebuilt at block `+0x5B10` (stride `0x9C`) from
     the older layout at block `+0x90` (stride `0x1C8`), with the job and licence entries re-read
     from the character table `[02EBF130]` and the table `[02EBF0E0]`.
   - `002EF4A0` first copies `0xC00` bytes from `02166480` to `021B290C`.
3. `00233C10`: with no block bound, it binds `02EBF190` to the active image `+0x4E68C`, rebases the
   inventory descriptors (`0030B6A0`) and runs the battle reset `00237DF0` twice (`00233C3F`,
   `00233C48`). With a block, the first dword must equal `0x05071901` (`00233C4D`); otherwise
   `00237DF0` runs (`00233C59`), which reaches `002370C0`: the block is zeroed, stamped, and its
   party arrays at `+0x5A48` filled with `0xFFFF` (`002370C0`).
4. `00584210`, called from the load lifecycle `00582860` (`00582EBA`), handles the stash:
   - load mode `00394450()` = 3 with header flag bit 0 clear: the play clock, the walked total
     and the five transition dwords are stashed at `+0x70`-`+0x90` and cleared, and field
     `0x483` is requested (`00314DC0`);
   - any other mode with flag bit 0 set: the stash is restored, `00329E40(walked)` re-seats the
     accumulator, `00269A20(image + 0xE240)` and `002EF410(image + 0x4E660)` run, the flag is
     cleared, `01E0C3EC` is zeroed and `0023A390(0)` clears the block's `+4` bit 12.
   - Both paths clear bit 0 of the battle block's `+0x5B04`.
   - Both paths then reseed the gameplay generator from the clock (see the
     [random number generators page](../Random-Numbers/random-number-generators.md)).

### What is initialised at boot

`002EF650` clears the active image, calls `00253A80` and `002EF2D0`, then `00238A80`. `00253A80`
zeroes the two state blocks (`[02092758]`, `0x58` bytes; `[020927C0]`, `0x4818` bytes) and writes
the six header constants at `+0x58`-`+0x6C` from their getters (`002EF2A0`, `002EF290`, `00235E90`,
`00235E80`) and literals (`00253AED`, `00253AFB`). The debug verb `0x209C` loads development slot
images (`002EF300`: slot clamped to 0-15, resource kind 1, index `0x75 + slot`, `0xE240` bytes into
the active buffer).

## Modding notes

- A save editor must decrypt and inflate the body before any offset applies; file offset `0x1244`
  is not the area id, image offset `0x1244` is. A raw decoded image written back without the
  container is accepted by the reader.
- Editing `+0x58`, `+0x5C` or `+0x64` cannot make a save fail to load through the functions on
  this page: none of them reads those three back (`002EF2D0` clears `0x1538` bytes from the
  getter's value, not from the header). `+0x60` is compared only inside the battle block at image
  `+0x4E68C`, and a mismatch there rebuilds the block.
- The checksum is not verified on load, so an edited image needs no checksum fix.
- The image size is this build's: the reader honours `+0x04`, and the party-record migration in
  `00235AF0` is what accepts an older block layout.

## Related

- [Languages: the Language setting, the nine language codes, the locale id each maps to, the data folder it selects, the Windows-locale default, and the confirm and cancel buttons](languages.md)
- [Random number generators: the gameplay Mersenne Twister, the shared gameplay LCG, the graphics-noise Mersenne Twister, the C runtime rand, the presentation bit-feedback generator, the counter hash and the PPFX xorshift, with their constants, seeds and states](../Random-Numbers/random-number-generators.md)
- [Gil: storage, the gil cap, every way gil changes, and the Plunderer and Spendthrift counters](../Rewards-EXP-Gil-And-Loot/gil.md)
