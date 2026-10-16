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

`SaveFileContainer` (`C`<sub>h</sub> bytes, offsets from the start of the file):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u8[4]` | magic | "SAFH"; `008666B0` rejects anything else as a container (see Loader behaviour) |
| `04`<sub>h</sub> | `u32` | size | the decoded image size, `56690`<sub>h</sub> in this build; must be at most `100000`<sub>h</sub> (`00866817`) |
| `08`<sub>h</sub> | `u32` | rotation 0-31, the key rotation; must be below 32 (00866805); kept at 02EB3868 |  |

The body from `+0C`<sub>h</sub> to the end of the file is the image, compressed with zlib `compress2` at
level 9 (`0087AF40`, called from `00866200` with level 9) and then encrypted with RC4 by
`00865AE0`.

### The key

Both directions derive the key the same way (`00865840`):

1. `CryptAcquireContextW` with container `RSA_SQEX_FFXII_TZA` and the Microsoft Enhanced
   Cryptographic Provider v1.0, type 1, retried with `CRYPT_NEWKEYSET` (`008658AF`-`008658D6`).
2. `CryptCreateHash(CALG_MD5)` (`8003`<sub>h</sub>).
3. The 32-character title `FINAL FANTASY XII THE ZODIAC AGE` is rotated left by the container's
   rotation (`strncpy` and two `memcpy`, `0086592C`-`0086595C`) and its 32nd byte set to NUL
   (`00865961`), so 31 characters are hashed (`CryptHashData`, `00865985`).
4. `CryptDeriveKey(CALG_RC4 = 6801h, flags 00800000h)`: a 128-bit RC4 key (`008659AF`).
5. `CryptDecrypt` (or `CryptEncrypt`) over the body in 1,000-byte chunks, the last one marked
   final (`008659C2`-`00865A31`).

The writer draws the rotation as `abs(rand()) mod 32` (`008663C5`-`008663ED`).

### The image

`SaveImage` (`56690`<sub>h</sub> bytes, offsets from the start of the image):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `000`<sub>h</sub> | `u8[512]` | header | see below |
| `200`<sub>h</sub> | `u8[353424]` | payload | the persistent payload; `002EF2B0` returns its address |

The image is 353,936 bytes: the clear `002EF5F0` and the boot initialiser `002EF650` memset that
many, the copy to the write buffer passes it (`002EF690`), and the submit records it at the
descriptor's `+100`<sub>h</sub> (`0057E310`).

### The header

`SaveImageHeader` (`200`<sub>h</sub> bytes, offsets from the start of the image):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | checksum | in the file: CRC-32 of image[`08`<sub>h</sub>, `E200`<sub>h</sub>) (`0057E3BF`); the finaliser writes its complement here first (`00583FA1`) |
| `04`<sub>h</sub> | `u32` | one | 1 in the written image (`0057E3C7`) |
| `08`<sub>h</sub> | `i32` | gil | written by `00254EE0` (`00254F1F`), read by `00253690` |
| `0C`<sub>h</sub> | `u32` | walked | walked-distance total mirrored from the battle block by `00254E80` (`00254E90`) |
| `10`<sub>h</sub> | `u64` | ticks | play clock, 60 Hz ticks, added by `00254CC0`; its bound is the sign-extended immediate `FFFFFFFF80BEFBFF`<sub>h</sub> compared unsigned (`00254CF1`, `00254D30`-`00254D33`), so it never fires |
| `18`<sub>h</sub> | `u16` | hours | (ticks / 216000) mod 10000, by `00254CC0` (`00254DB5`) |
| `1A`<sub>h</sub> | `u8` | minutes | (ticks / 3600) mod 60, by `00254CC0` |
| `1B`<sub>h</sub> | `u8` | seconds | (ticks / 60) mod 60, by `00254CC0` |
| `1C`<sub>h</sub> | `u8[4]` | pad | not written by the enumerated writers |
| `20`<sub>h</sub> | `u8[28] roster` | seven 4-byte entries, 00583D60: character id, level, jobs (high and low nibble), flags; unused entries start with `FF`<sub>h</sub> |  |
| `3C`<sub>h</sub> | `u32` | esper | the summoned Esper's character row: `003200A0` sets its flag bit 0 when summon mode is on (block +`5B04`<sub>h</sub> bit 0, `003135E0`) and copies the row byte block +`5AD4`<sub>h</sub> (`003137E0`); `00583D60` stores it, else `FF`<sub>h</sub> (`00583F08`-`00583F0D`); the slot pane's ESPER row shows its name when it is not `FF`<sub>h</sub> (`0057EFE0`, `0057F0CC`) |
| `40`<sub>h</sub> | `u32` | counter | counter kind `11`<sub>h</sub> (`003166F0`) when story flag `400B`<sub>h</sub> is set, else untouched |
| `44`<sub>h</sub> | `u32` | clanrank | `00315390`() when story flag `400B`<sub>h</sub> is set, else 0 |
| `48`<sub>h</sub> | `u32` | mapgroup | the area's map persistence group: `00254380`(`00264F90`(areaId)) |
| `4C`<sub>h</sub> | `u32` | area | the active or pending area id (`003148F0`) |
| `50`<sub>h</sub> | `u32` | savecount 00583D60's second argument (the controller's `+D0`<sub>h</sub>); in the written image the save counter 02CA99B4, saturating at `FFFFFFFF`<sub>h</sub> (0057E3CE-0057E3DD) |  |
| `54`<sub>h</sub> | `u8` | slot | `00583D60`'s first argument: the save slot (controller +`CD`<sub>h</sub> from `00581DA0` at `00581EE7`; 0 from `005844A0` at `005844BE`) |
| `55`<sub>h</sub> | `u8[2]` | pad2 | not written by the enumerated writers |
| `57`<sub>h</sub> | `u8` | flags | bit 0 from `00236760` (stash pending), bit 1 from `00236740`, bit 2 from `00236780` (`00583F5A`-`00583F7D`) |
| `58`<sub>h</sub> | `u32` | date | constant `20050223`<sub>h</sub>, written by `00253A80` and never read |
| `5C`<sub>h</sub> | `u32` | clearsize constant `1538`<sub>h</sub>, the size 002EF2DD clears at payload +0 |  |
| `60`<sub>h</sub> | `u32` | stamp | constant `05071901`<sub>h</sub>, the battle-state block's stamp |
| `64`<sub>h</sub> | `u32` | blocksize constant `7410`<sub>h</sub>, the battle-state block's size |  |
| `68`<sub>h</sub> | `u32` | magic2 | `0131F3EA`<sub>h</sub>, tested by `00255260` |
| `6C`<sub>h</sub> | `u32` | size2 | `4818`<sub>h</sub>, tested by `00255260`; the image-backed state block's size |
| `70`<sub>h</sub> | `u8[32] stash` | the mode-3 stash: `+70`<sub>h</sub> ticks, `+78`<sub>h</sub> hours, `+7A`<sub>h</sub> minutes, `+7B`<sub>h</sub> seconds, `+7C`<sub>h</sub> walked, `+80`<sub>h</sub> five dwords of the world-transition record (00584210) |  |
| `90`<sub>h</sub> | `u8[368] rest` | zeroed by the image clears; not written by the enumerated writers |  |

The roster loop (`00583DC2`-`00583EEB`) walks party pages 0-8 from `00282DF0(page)`, skips a page
whose word `+60`<sub>h</sub> is negative or whose flag bit 1 is set, and writes for each page `{+60h low
byte, +BAh, +86h << 4 | +87h, flags}` with flag bit 0 when the page is the leader
(`003271D0`), bit 1 when the page's dword `+0` has bit 10; the page with flag bit 1 is written
last with flag bit 2, and entries up to seven are filled with `FF`<sub>h</sub>.

### The checksum

`003BB220(data, length)` is the reflected CRC-32: state `FFFFFFFF`<sub>h</sub>, eight shift-and-xor steps
per byte with `EDB88320`<sub>h</sub>, final complement; a non-positive length returns 0 without reading.

- The finaliser `00583D60` feeds it the active image's `+8` for `E1F8`<sub>h</sub> bytes (`00583F81`-`00583F92`,
  always the active buffer even when its destination is the capture buffer), and stores the result
  at the destination's `+E200`<sub>h</sub> and its complement at `+00`<sub>h</sub> (`00583F99`-`00583FA1`).
- The submit `0057E310` recomputes it over the same bytes of the active buffer and stores the plain
  value at the written image's `+00`<sub>h</sub> (`0057E3A9`-`0057E3BF`).
- Nothing on the load path recomputes or compares it: the function's only callers are those two
  (`00583F92`, `0057E3BA`).

### The four image buffers

| Buffer | Address | Accessor | Role |
|---|---|---|---|
| active | `02164280` | `002EF640` | the live image, updated while playing |
| capture | `021BA940` | `002EF620` | the finaliser's destination when it is told to write there |
| write | `02211000` | `002EF630` | what the file write reads; filled from the capture buffer by `0057E310` (`ACD`<sub>h</sub> 128-byte blocks plus 16) and by `002EF690` |
| backup | `022676C0` | none | a copy of the active buffer made by `002EF570` |

The buffers are `566C0`<sub>h</sub> apart, 48 bytes more than the image.

### What lives inside the image

| Image offset | Payload offset | Content |
|---|---|---|
| `01244`<sub>h</sub> | `+1044`<sub>h</sub> | the active or pending area id (`00584210` stashes `+1244`<sub>h</sub>-`+1254`<sub>h</sub>) |
| `02200`<sub>h</sub> | `+2000`<sub>h</sub> | the copy of the battle-state block head that `00235AF0` compares |
| `08200`<sub>h</sub> | `+8000`<sub>h</sub> | the image-backed state block, `4818`<sub>h</sub> bytes, bound to `020927C0` by `00253970`; its `+47E8`<sub>h</sub> (image `+C9E8`<sub>h</sub>) mirrors the play clock |
| `4E68C`<sub>h</sub> | `+4E48C`<sub>h</sub> | the battle-state block, 29,712 bytes, bound to `02EBF190` by `00233C10` (`00233C25`-`00233C33`) |
| `0E200`<sub>h</sub> | `+E000`<sub>h</sub> | the finaliser's checksum copy |

## Loader behaviour

### Reading the container

`008666B0` reads the whole file and branches on its first four bytes:

- Not `SAFH` (or shorter than 5 bytes): the file is treated as a raw image and copied byte for
  byte into the stream buffer `01F44D40` (`008666B0`, the first branch). A plain decoded image is
  therefore accepted as a save.
- `SAFH` but shorter than 13 bytes: nothing is read.
- `SAFH`: `+08`<sub>h</sub> must be below 32 and `+04`<sub>h</sub> at most `100000`<sub>h</sub> (`00866805`, `00866817`);
  `00865D90` decrypts (`00865840`) and inflates (`0080C5A0`, zlib `uncompress`) and the result's
  length must equal `+04`<sub>h</sub> (`00866866`-`0086686D`); the image is then copied into the stream.

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

1. `00255260(header + 68h)`: when the pair is not both zero, `+68`<sub>h</sub> must be `0131F3EA`<sub>h</sub> and
   `+6C`<sub>h</sub> must be `4818`<sub>h</sub>, else the header is invalid.
2. `00235AF0` (the prelude of the guard `00233C10`, `00233C14`) compares the block at `02EBF190`
   with the image's copy at `+2200`<sub>h</sub>: its first two dwords, its byte `+5B42`<sub>h</sub> and its word
   `+5B12`<sub>h</sub>.
   - On any difference the 40 party records are rebuilt at block `+5B10`<sub>h</sub> (stride `9C`<sub>h</sub>) from
     the older layout at block `+90`<sub>h</sub> (stride `1C8`<sub>h</sub>), with the job and licence entries re-read
     from the character table `[02EBF130]` and the table `[02EBF0E0]`.
   - `002EF4A0` first copies `C00`<sub>h</sub> bytes from `02166480` to `021B290C`.
3. `00233C10`: with no block bound, it binds `02EBF190` to the active image `+4E68C`<sub>h</sub>, rebases the
   inventory descriptors (`0030B6A0`) and runs the battle reset `00237DF0` twice (`00233C3F`,
   `00233C48`). With a block, the first dword must equal `05071901`<sub>h</sub> (`00233C4D`); otherwise
   `00237DF0` runs (`00233C59`), which reaches `002370C0`: the block is zeroed, stamped, and its
   party arrays at `+5A48`<sub>h</sub> filled with `FFFF`<sub>h</sub> (`002370C0`).
4. `00584210`, called from the load lifecycle `00582860` (`00582EBA`), handles the stash:
   - load mode `00394450()` = 3 with header flag bit 0 clear: the play clock, the walked total
     and the five transition dwords are stashed at `+70`<sub>h</sub>-`+90`<sub>h</sub> and cleared, and field
     `483`<sub>h</sub> is requested (`00314DC0`);
   - any other mode with flag bit 0 set: the stash is restored, `00329E40(walked)` re-seats the
     accumulator, `00269A20(image + E240h)` and `002EF410(image + 4E660h)` run, the flag is
     cleared, `01E0C3EC` is zeroed and `0023A390(0)` clears the block's `+4` bit 12.
   - Both paths clear bit 0 of the battle block's `+5B04`<sub>h</sub>.
   - Both paths then reseed the gameplay generator from the clock (see the
     [random number generators page](../Random-Numbers/random-number-generators.md)).

### What is initialised at boot

`002EF650` clears the active image, calls `00253A80` and `002EF2D0`, then `00238A80`. `00253A80`
zeroes the two state blocks (`[02092758]`, `58`<sub>h</sub> bytes; `[020927C0]`, `4818`<sub>h</sub> bytes) and writes
the six header constants at `+58`<sub>h</sub>-`+6C`<sub>h</sub> from their getters (`002EF2A0`, `002EF290`, `00235E90`,
`00235E80`) and literals (`00253AED`, `00253AFB`). The debug verb `209C`<sub>h</sub> loads development slot
images (`002EF300`: slot clamped to 0-15, resource kind 1, index `75h + slot`, `E240`<sub>h</sub> bytes into
the active buffer).

## Modding notes

- A save editor must decrypt and inflate the body before any offset applies; file offset `1244`<sub>h</sub>
  is not the area id, image offset `1244`<sub>h</sub> is. A raw decoded image written back without the
  container is accepted by the reader.
- Editing `+58`<sub>h</sub>, `+5C`<sub>h</sub> or `+64`<sub>h</sub> cannot make a save fail to load through the functions on
  this page: none of them reads those three back (`002EF2D0` clears `1538`<sub>h</sub> bytes from the
  getter's value, not from the header). `+60`<sub>h</sub> is compared only inside the battle block at image
  `+4E68C`<sub>h</sub>, and a mismatch there rebuilds the block.
- The checksum is not verified on load, so an edited image needs no checksum fix.
- The image size is this build's: the reader honours `+04`<sub>h</sub>, and the party-record migration in
  `00235AF0` is what accepts an older block layout.

## Related

- [Languages: the Language setting, the nine language codes, the locale id each maps to, the data folder it selects, the Windows-locale default, and the confirm and cancel buttons](languages.md)
- [Random number generators: the gameplay Mersenne Twister, the shared gameplay LCG, the graphics-noise Mersenne Twister, the C runtime rand, the presentation bit-feedback generator, the counter hash and the PPFX xorshift, with their constants, seeds and states](../Random-Numbers/random-number-generators.md)
- [Gil: storage, the gil cap, every way gil changes, and the Plunderer and Spendthrift counters](../Rewards-EXP-Gil-And-Loot/gil.md)
