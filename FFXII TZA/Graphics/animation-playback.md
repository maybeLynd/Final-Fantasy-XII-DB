---
title: "Animation playback: the player object, track pairing by bone id, the sampler, the skeleton node records, chunk links and the locomotion query"
kind: "system"
category: "Graphics"
addresses: "0x0041F340, 0x0051BA80, 0x0041CB90, 0x0041D220, 0x0041CA70, 0x0041CF00, 0x0041CD30, 0x0041BEE0, 0x0041B550, 0x00370E00, 0x00373540, 0x00418880, 0x003712E0, 0x00372820, 0x00373DC0, 0x00373D00, 0x00373EA0, 0x00373F40, 0x00370390, 0x00373160, 0x003703A0, 0x00373860, 0x00372610, 0x00372280, 0x004256E0, 0x00422D90, 0x004094D0, 0x00409300, 0x0046E640, 0x004219C0, 0x004215A0"
---

## What the player sees

Every character the player sees moving is a skeleton of bones driven by one motion at a time: the
walk or run the locomotion query picks from the character's speed and turn, the attack or hit
motion an event asks for, and the short cross-fade between two of them. Something attached to a
bone, such as a weapon or the high-detail body a story scene swaps in for a party member, follows
that bone. This page describes the objects behind that: the player object that holds the motion,
the bone records it writes, and the links between skeletons.

## How it works

### The player object

The per-character animation player is the `0x3A0`-byte presentation entry, the record that the
reference container on [presentation entries](presentation-entries.md) hands out by id.

Its storage is reserved when a model binds: the model bind `0x0041F340` (from `0x0041FCF0`) lays out in the record's
arena block the skeleton bytes `0x003712E0` sizes, then the `@FCP` section-8 copy at that size (record
`+0x300`, `0x0041F5C1`) in the block `0x003E6D10` sizes (rounded up to 16), then one entry followed by one
`0x108`-byte channel row per `@FTR` node (`0x00409240`), the pair rounded up to 16 (`0x0041F452`-`0x0041F47B`).

- The encoded offsets go to record `+0x480` (the entry) and `+0x484` (its rows). When the model's
  `@FCP` byte `+0x01` is non-zero (`0x003E55F0`) a second entry and row block follow at `+0x488` and
  `+0x48C`, and record `+0x284` bit `0x10000` is set (`0x0041F4A4`-`0x0041F4C7`).
- `0x0051BA80(container, id, …, request)` binds a motion: it builds an entry on its own stack with
  `0x0041CB90` (the defaults) and `0x0041D220` (the request), admits a new id when given −1
  (`0x0051F080`), copies the `0x3A0` bytes into the slot `0x0051F240` resolves (`0x0051BB20`-`0x0051BB7D`),
  re-resolves the copy with `0x0041CA70` and stores the id at `+0x00` (`0x0051BB8B`).
- When the request fails, an entry that already had the id is reset with `0x0041CF00` and the id
  released (`0x0051F190`).
- The request is at least `0x3C` bytes: `+0x00` the motion file, `+0x08` the skeleton bank, `+0x10` the file
  index, `+0x14` the skeleton id, `+0x18` the section name, `+0x20` the motion number, `+0x24` a word,
  `+0x28` the arena handle of the row block, `+0x30` the row offset, `+0x34` a word and `+0x38` a dword.

`0x0041D220(entry, request)` sets bits `0x1` and `0x100000` of `+0x0C`, copies the request fields to `+0x31C`,
`+0x2EC` (the name, `0x00409210`), `+0x330`, `+0x338`, `+0x310`, `+0x318`, `+0x2B0`, `+0x2B8`, `+0x31A`,
`+0x2BE` and `+0x364`, zeroes `+0x2BC` and `+0x32A`, sets the selector kind `+0x2DC` to `0xFF`, finds
the `@FMC` section (`0x434D4640`, else `@FRP` `0x50524640`) by name into `+0x320` and the `@FRM`
payload offsets into `+0x378` and `+0x37C` (−1 without one), runs `0x0041CA70` and refreshes the
skeleton entry (`0x0046E420` of `+0x330`, `+0x338`).

`0x0041CA70(entry)` turns offsets into pointers. Unless `+0x0C` bit `0x20` is set or the index `+0x318` is −1
it resolves the stream `+0x368` (`0x004090D0` of the `+0x320` section with `+0x31A` and `+0x31C & 0xFFF`)
and the motion file's data start `+0x370` (`0x004096C0` with offset 0); either way it then points `+0x18`
at track state `+0x20` (`0x0041CAE8`, where both skips land).

For every track state whose word `+0x0A` is 1 and motion index `+0x50` is not −1 it then resolves
`+0x70` (the record at `+0x54` in the section the first index `+0x50` names, `0x00408F80` with the word
`+0x5C`) and `+0x78` (the data at `+0x58` in the section of the second index `+0x52`)
(`0x0041CB10`-`0x0041CB66`).

`0x0041CF00(entry)`, from `0x0051BA40` and `0x0051BA80`, is the reset: every track state gets `+0x00` −1,
`+0x04` 0, `+0x08` to `+0x17` zero, the words `+0x18` 0 and `+0x1A` 30, `+0x20` 30.0, `+0x48` 0,
`+0x50` and `+0x52` −1, `+0x60` 0, `+0x68` −1, `+0x70` and `+0x78` 0, its cursor `+0x8C` back to its
start `+0x88` and bit `0x80` of `+0x96` cleared (`0x0041CF22`-`0x0041CF82`). With `+0x0C` bit `0x1000` set it clears
the bones' second set first (`0x002ED570` of `+0x330`, `+0x338`, then `0x00372280`) and clears the bit; then `0x0041CB90` restores the entry defaults listed in the layout below.

The entry is run every frame by the per-entry update `0x0041C410` through the walker `0x0041DA90`,
which calls the sampler `0x00418880` (both on [presentation entries](presentation-entries.md)); its
track states are set up by `0x0041CD30` and swapped by the [authored commands](authored-presentation-commands.md).
It lives as long as the record's arena block; the id goes back through `0x0051F190`.

### Track pairing by bone id

`0x0041BEE0(entry, state, state, file; motion index, word, name, word, pointer, bound id, layer,
dword)` binds a motion into a track state. It finds the sections by tag and the state's name
`+0x24`: `@FMN` (`0x4E4D4640`), else `@FRP` (`0x50524640`), into `+0x54`, and `@FMW` (`0x574D4640`)
into `+0x58` (`0x00409A30`, `0x0041BFE7`-`0x0041C027`).

It lists the skeleton's bones in the scratch list (`0x00370BB0`, see
[the motion bone list](skeleton-entries-and-bones.md#the-motion-bone-list)), resolves the pair
(`0x0041B4E0`), resolves the row block (`0x003AB7F0` of entry `+0x2B0` plus `+0x2B8`) and zeroes the
row count `+0x2BC` (`0x0041C03B`-`0x0041C06A`).

It then walks the `@FMN` records from the start `0x00409190` gives, each record's length being bits
`0x7E00` of its word `+2` (`0x0041C15C`-`0x0041C168`), and for each:

- For a kind-2 skeleton (dword `+0x9C` = 2) `0x00370E00(skeleton, record word +0)` claims the listed
  bone with flag bit `0x100` whose key (`0x00409250`) equals the record's bone id and unlinks it (`0x00373540`,
  `0x003735AF`); for any other kind it returns −1, so no record gets a row (`0x0041C0A6`-`0x0041C0B3`).
- With a layer other than −1 the bone's byte `+0x283` must equal it (`0x0041C0B9`-`0x0041C0D2`).
- Bit `0x2` of the bone's byte `+0x28B` becomes the inverse of (its own bit `0x1` xor bit `0x2` of byte `+0x28A`),
  and its bit `0x1` becomes bit `0x2` of `+0x28A` (`0x0041C0E2`-`0x0041C11C`).
- `0x0041B550(row, @FMN section, record, bone, @FMW data, the bind's last argument)` fills row number `+0x2BC` of the
  block with the record's channels (on [model effects](model-effects-and-motion-commands.md#reading-the-channels)),
  and the count goes up (`0x0041C126`-`0x0041C155`).

After the walk the state's `+0x1C` becomes `(duration − [0x01DFE0BC]) / duration` for a non-zero
duration (`0x0041C1AA`-`0x0041C1C8`), and `0x0041C260` keeps the current rotations for a blend when
`+0x96` bit `0x10` is set.

### The sampler

`0x00418880(entry, state, state)`, called by the walker only when the state's word `+0x0A` is 1
(`0x0041DBD7`-`0x0041DBED`), is described on [model effects](model-effects-and-motion-commands.md#applying-a-frame),
with [the blend](model-effects-and-motion-commands.md#blending-into-a-new-motion). What it touches
of the objects here:

- it runs for a state with `+0x08` bit `0x2` set (`0x004188FE`), and takes the skeleton entry from
  the state's bank and id (`0x0046E8B0` of `+0x60`, `+0x68`) and the bones from that entry's `+0x84`;
- from the presentation entry it takes the rows (`+0x2B0`, `+0x2B8`), the ease
  words `+0x358` and `+0x35A` for the blend weight, and the name `+0x2EC` and the block `+0x2E0` for
  its special cases;
- into a bone it writes `+0x190` (`0x00418650`), `+0x1B0` (`0x00418700`) and `+0x1D0` (`0x004186A0`, skipped
  for a tied bone), or `+0x1A0`, `+0x1C0` and `+0x1E0` when the state's `+0x96` bit `0x20` is set (the writers
  add 16 × that bit, `0x004189DA`-`0x004189DE`); on that branch it also turns `+0x1A0` into a quaternion and
  sets bit `0x10` of `+0x280` (`0x00418E5F`, `0x00419CAC`);
- it rebuilds `+0xC0`, `+0xF0` and `+0x100` in place (`0x00418F37`-`0x00418F83`) and clears bit `0x1` of `+0x28A`
  of every bone it samples whose byte is non-zero (`0x00418AD7`, `0x004194B7`); a bone whose byte is 0 takes
  its rest pose instead (`0x0041D6F0`).

### The node records and the attach tree

A skeleton entry's `+0x84` is the encoded address of its node array, `+0x88` nodes of `0x290`
bytes, then the u16 slots (`+0x8A` of them list the pool-built nodes). `0x003712E0` sizes it and
`0x00372820` builds it from the model's `@FTR` ([model files](model-files-cm-ca.md#ftr-the-skeleton)).
`0x00372820` copies the `@FTR` header's dword `+0x04`, the kind, to entry `+0x9C` and branches on it
(`0x003729DD`-`0x003729F7`): kind 2 runs the loop below, kind 0 its own loop further down.

For a kind-2 skeleton it first writes the identity into node 0's `+0x80` (`0x00372A44`) and clears the
skeleton's byte `+0xA7` (`0x00372A50`). For each node (`0x00372A80`-`0x00372CA8`):

- A node whose record has flag bit `0x100` (`0x100`) starts with `0x00373DC0`: identity at `+0x1F0` and
  `+0x230`, `(0, 0, 0, 1)` at `+0x1A0` and `+0x1C0`, 1.0 at `+0x1E0`-`+0x1EC`, `+0x280` 0, bit `0x1` of
  `+0x282` and bit `0x4` of `+0x28B` cleared, `+0x278` the encoded null, the links `+0x270`-`+0x276` and
  `+0x27C` −1, bits `0x1` and `0x2` of `+0x28B` set, `+0x283` 0 and `+0x28A` 3.
- For that node `0x00409300` then reads, with record bit `0x200000`, the pool translation (bits 23-25) and
  rotation (bits 26-28) into `+0xF0` and `+0xC0`, else writes the identity over `+0xC0`-`+0xFF`
  (`0x00409428`); `0x004094D0` puts the pool matrix into `+0x150` (sixteen pool dwords with record bit `0x200000`,
  else the identity `0x01F204E0` through `0x0046D110`).
- Any other node gets the short init: identity at `+0x1F0` and `+0x230`, `+0x280` 0, `+0x278` the
  encoded null, `+0x27C`, `+0x270`, `+0x274`, `+0x272` and `+0x276` −1 (`0x00372AAA`-`0x00372AED`).
- Both then store the node's own encoded address at `+0x284`, set bit `0x4` of `+0x280`, write the
  index at `+0x27E` and the parent from record bits `0xFFF000` (`0xFFF` → −1) at `+0x270`
  (`0x00372AFB`-`0x00372B34`). With a parent, the node becomes its first child `+0x274` when that is −1,
  else it is inserted after the first child in the sibling chain `+0x272` (`0x00372B5C`-`0x00372B99`);
  without one it joins node 0's chain (`0x00372B45`-`0x00372B53`).
- A flag-bit-8 node then copies `+0xF0` to `+0x1B0` and `+0x130`, gets 1.0 at `+0x100`-`+0x10C`,
  `+0x140`-`+0x14C`, `+0x19C`, `+0x1AC`, `+0x1CC` and `+0x1D0`-`+0x1DC`, and is listed in the next
  u16 slot (`0x00372BA1`-`0x00372C97`); any other node gets none of that.

For a kind-0 skeleton (`0x4C`-byte records from `+0x30`, `0x00372CE4`-`0x00372E7E`) every node gets
`0x00373DC0` (`0x00372CEB`), bit `0x4` of `+0x280`, its index at `+0x27E` and its parent from the record's
word `+0x20` (`0x00372D22`), the same chaining (`0x00372D50`-`0x00372D90`; node 0's chain at
`0x00372D37`-`0x00372D46`), `0x00409300`, the translation copy and the 1.0 stores; it writes neither
`+0x284` nor `+0x150`, and sets the listed count `+0x8A` to 0 (`0x00372EC4`).

After the loop a kind-2 skeleton runs `0x00373D00` and a kind-0 skeleton `0x00373D00` then `0x00373EA0`
(`0x00372E84`-`0x00372EE2`). `0x00373D00` writes the rest pose of each listed bone: its parent's `+0x80`
(node 0's `+0x1F0` for a root) times its own `+0xC0` (`0x00202D70`); `0x00373EA0` writes the inverse of
that `+0x80` into `+0x150` (`0x00202D50` → `0x00217610`), the bind-pose inverse the composer applies
last.

Both loop over the listed count `+0x8A` (`0x00373D44`, `0x00373EE4`), which the kind-0 path has just
set to 0, so at build time neither writes anything for a kind-0 skeleton; a kind-2 skeleton takes
`+0x150` from the pool or the identity.

The links form two trees. The parent link `+0x270` and the sibling and first-child links `+0x272`
and `+0x274` describe the model's own hierarchy; only the builder reads `+0x272` and `+0x274`, while chaining
(`0x00372B45`, `0x00372B67`, `0x00372B8A`, `0x00372D37`, `0x00372D5B`, `0x00372D80`): among the 71 functions that
carry the immediate `0x290`, no other function reads either. The composer walks the parent link alone.

The second tree crosses skeletons: `+0x276` names a bone of the parent skeleton for a root bone,
and `+0x278` with `+0x27C` names the tied child bone; `0x00372F60`, from the entry refresh `0x0046E420` and
the bank's re-link `0x0046E8D0`, rewrites `+0x278` from `+0x27C` (`0x00372FCD`-`0x00372FEF`).

`0x00373F40(entry, parent entry)`, from `0x0042E550` and `0x0046E0F0`, places an attached
skeleton: with a slot `+0x14`, node 0's `+0x1F0` becomes the parent's slot bone `+0x80` (the
parent's node 0 `+0x1F0` for slot 0) times the entry's own `+0x40` (`0x00373FB3`-`0x00373FE1`); then
every root bone with a `+0x276` copies that parent bone's `+0x80` into its `+0x1F0` (`0x00373FF0`-`0x0037402E`).

`0x00372280(entry)`, which the player's `0x0041CF00` runs under `+0x0C` bit `0x1000`, clears the second set on
every listed bone: bit `0x10` of `+0x280`, and `+0x1A0`, `+0x1C0` back to `(0, 0, 0, 1)`. `0x0041D4D0` is its
counterpart: it sets or clears `+0x0C` bit `0x1000` together with bit `0x20` of every state's `+0x96`
(`0x0041D4D9`-`0x0041D554`).

### Composing the pose

`0x003703A0(entry)` is the skeleton-entry update (from `0x004242B0` and `0x0046E0F0`). It allocates two
per-bone arrays on its stack (`0x00370438`-`0x0037045E`), builds the record's mapping table `+0x6D0` when it
is null and both the record and the skeleton named by entry `+0x0C` have a `skeletonmapping.bin` table
(`+0x6B8`, `0x003704C2`-`0x003705AC`; [add-motion tables](add-motion-tables.md#skeletonmappingbin)), then
calls the final-pose composer `0x00373860` once (`0x003705BA`) and sets bit `0x800` of the entry's `+0x00`.

`0x00373860(entry, out pointers, out scales)` first applies the add-motion tracks (`0x003714A0`),
then for each listed bone (`0x00373970`-`0x00373CA3`):

- stores at `+0x284` the encoded address of the bone's skinning slot: `+0x00` when the skeleton's
  byte `+0xA7` has 1 in its low nibble, else `+0x40` (`0x0037397B`-`0x00373998`);
- takes its source matrix: the parent's `+0x80` (`+0x270`), else the `+0x276` bone's `+0x80` in the
  parent skeleton that entry `+0x0C` names, else node 0's `+0x1F0` (`0x0037399E`-`0x003739DD`);
- with `+0x280` bit `0x10` set takes the second-set path (the `+0x96` bit-5 set): `+0x1A0`
  as a matrix (`0x00477130`) times `+0xC0`, the translation `+0xF0` plus `+0x1C0` (`0x00202B10`), the scale `+0x100` times `+0x1E0`
  (`0x00202D80`), then `+0x230`, the source, the row scales and `+0x150` (`0x003739EA`-`0x00373B51`);
  otherwise `0x00372610(source, +0xC0, +0x230, +0x100, +0x150)`
  ([the tie](skeleton-entries-and-bones.md#tying-bones-to-another-skeleton));
- copies `0x02AD9E40`, the product before `+0x150`, into `+0x80`, and `0x02AD9E80`, the product with
  `+0x150`, into the slot `+0x284` names (`0x00373B8A`-`0x00373BB8`);
- when the record's add-motion state `+0x6C8` is 2 and its `+0x6D0` table maps the bone to a
  partner bone, the bone's `+0x80` and its skinning slot are overwritten with that partner bone's
  `+0x80` and the matrix its `+0x284` names (`0x00373BC6`-`0x00373C4F`).

Each bone's `+0x80` address and its 16-byte scale (`+0x100`, or `+0x100` × `+0x1E0` with lane 3 from
`+0x10C` on the second-set path) go to the two out arrays (`0x00373C6F`-`0x00373C8F`), and at the end the
skeleton's byte `+0xA7` gets 1 in its high nibble (`0x00373CA9`-`0x00373CB1`). So `+0x80` is the matrix
children chain from and lookups return, and `+0x00` / `+0x40` are the two skinning slots, the current
one named by `+0x284`.

### Chunk links and the two-chunk party member

`0x00370390(child, parent, slot)` is the chunk link: it jumps to `0x00373160` only for a kind-2 skeleton
(dword `+0x9C` = 2, the `@FTR` kind the builder copied) and returns otherwise. `0x0046E640(bank, child, parent, slot)` reaches it to tie one
skeleton's bones to another's by key; the tie, the saved parent link `+0x28E` (`0x00373244`), the root
test on it (`0x003732CB`) and the undo are on [skeleton entries](skeleton-entries-and-bones.md#tying-bones-to-another-skeleton).

Values the channel writers store into a tied parent bone are stored into the child bone at `+0x278`
as well (`0x00418679`, `0x00418729`, `0x004186D9`), and the composer takes a tied root's source from the parent skeleton through `+0x276`.

A party member in a story scene can be two chunks: the bound model and a second skeleton tied to
it. A child record attached with code `0x7FFF` goes through `0x004215A0` to `0x004219C0(parent, −1,
child)` (`0x0042164D`-`0x00421661`), and `0x004219C0` ties the skeletons with `0x0046E640` (`0x00421AC1`). The
skeleton-entry update builds `+0x6D0` when the record and the skeleton named by `+0x0C` both have a
`skeletonmapping.bin` table (`+0x6B8`), and the composer uses it only while `+0x6C8` is 2.

Equipment goes the same way: `0x0041F010` ties a child to a bone through `0x004211B0`, which calls
`0x0046E640` (`0x00421255`) when the child's skeleton entry has bit `0x80` of its first byte (`0x00421237`).

### The locomotion query and its model gates

`0x004256E0(entry, mode)` is the locomotion selector; its states, thresholds and the `@FCP` section-9
bytes it reads through `0x004FE2F0` are tabled on
[presentation entries](presentation-entries.md#the-per-entry-update). The objects it reads are the
entry's render record `+0x2E0` (speed, facing, run threshold) and the entry's motion number `+0x31C`.
Two gates in the model decide the fallback:

- The `@FCP` gate: each direction byte comes from dword `0x30` of section 9 (ids `0x63070F30`,
  `0x62070E30`, `0x61070D30`, `0x60070C30`), read by `0x004FE2F0` on the record (`0x00425A28`-`0x00425AF1`),
  and state 7 reads byte 3 of dword `0x2D` (`0x63070B2D`, `0x00425BA9`); a payload older than version 7
  answers 0.
- The `@FRM` gate, the jump-table case for state 6 (`0x00425D60` entry 5): the query resolves the motion
  file `+0x310` and index `+0x318` (`0x00425AC2`-`0x00425AD9`), and `0x00422D90`
  resolves the block (`0x003AB7F0`), finds the `@FRM` section (`0x4D524640`) and returns its payload at
  `+0x30` (`0x00422DAB`-`0x00422DCC`); when the `0x60070C30` byte is 2, 3 or 4, the low six bits of byte
  `+2` there decide the fallback (`0x00425B0E`-`0x00425B3D`).

The query then sets bit `0x2000` of the entry's `+0x0C` (`0x00425B55`), applies the mode (mode 2 only when
the record's `+0x108` object passes `0x002ED530`, `0x00425B5D`-`0x00425B84`) and returns the state in its
low word (`0x00425D0C`-`0x00425D11`).

## Layouts

### The presentation entry (0x3A0 bytes)

Defaults are the constructor `0x0041CB90`'s unless a site is named. Four track states of `0xA0` bytes
fill `+0x30` to `+0x2AF`.

| Offset | Type | Field |
|---|---|---|
| `+0x000` | `i32` | the entry's id, −1 until `0x0051BA80` stores it (`0x0051BB8B`) |
| `+0x004` | `i32` | −1 |
| `+0x008` | `i32` | −1 |
| `+0x00C` | `u32` | flags: bit `0x1` and bit `0x100000` set by `0x0041D220`; bit `0x20` skips the section resolve in `0x0041CA70`; bit `0x1000` asks `0x0041CF00` for the second-set clear; bit `0x2000` set by the locomotion query; bit `0x8000000` set and bits `0x40000` and `0x10000000` tested by the sampler (`0x00419243`, `0x004191CD`, `0x00419179`); bits 1, 3, 6-9, 14, 17, 18, 23 on [presentation entries](presentation-entries.md) and [authored commands](authored-presentation-commands.md) |
| `+0x010` | `u8[8]` | not touched by the routines on this page |
| `+0x018` | `void*` | the current track state, `+0x30 + 0xA0 × +0x20` (`0x0041CAE8`-`0x0041CAFD`) |
| `+0x020` | `i32` | the current track state's number |
| `+0x024` | `u32` | zeroed with `+0x20`; the state word the per-entry update keeps |
| `+0x028` | `i16` | track state count |
| `+0x02A` | `u16` | 0 |
| `+0x02C` | `u8[4]` | not touched by the routines on this page |
| `+0x030` | `track state × 4` | the track states, `0xA0` bytes each |
| `+0x2B0` | `u64` | arena handle of the channel-row block (request `+0x28`) |
| `+0x2B8` | `u32` | offset of the rows in that block (request `+0x30`) |
| `+0x2BC` | `u16` | row count, rebuilt by every bind |
| `+0x2BE` | `u16` | request `+0x34` |
| `+0x2C0` | `void*` | the actor the bank-A invokers pass (`0x0041CEC0`) |
| `+0x2C8` | `u32` | flags the commands and walker set (bits `0x10`, `0x20`, `0x40`, `0x1000`) |
| `+0x2CC` | `u32` | zeroed with `+0x2C8` |
| `+0x2D0` | `u64` | zeroed; not read by the routines on this page |
| `+0x2D8` | `u16` | −1 |
| `+0x2DA` | `u8[2]` | not touched by the routines on this page |
| `+0x2DC` | `u8` | selector kind, `0xFF` until command `0x0A` copies one |
| `+0x2DD` | `u8[3]` | the selector's bytes, from command `0x0A` |
| `+0x2E0` | `void*` | the character render record |
| `+0x2E8` | `u32` | flags; bits 0–2 cleared by the constructor, bits `0x1` and `0x2` armed by the blend command `0x08` |
| `+0x2EC` | `u8[36]` | the section name text (`0x00409210`), looked up with the tags |
| `+0x310` | `void*` | the motion file |
| `+0x318` | `u16` | index in the file, −1 for none |
| `+0x31A` | `u16` | request `+0x24` (the record's signed byte `+0x413`) |
| `+0x31C` | `u16` | the motion number; its top nibble is the kind the query tests |
| `+0x31E` | `u8[2]` | not touched by the routines on this page |
| `+0x320` | `u32` | offset of the `@FMC` (else `@FRP`) section |
| `+0x324` | `u16` | the motion number playing, −1 at reset; `+0x326` the previous (command `0x00`) |
| `+0x328` | `u8` | zeroed as a dword; `u8[3]` follows |
| `+0x32A` | `u16` | 0 |
| `+0x32C` | `u8[4]` | not touched by the routines on this page |
| `+0x330` | `void*` | the skeleton bank (request `+0x08`) |
| `+0x338` | `i32` | the skeleton entry id (request `+0x14`), −1 for none |
| `+0x33C` | `u32` | set with `+0x0C` bit `0x1000` by `0x0041D4D0` |
| `+0x340` | `f32` | `[0x01DFE0BC] × [0x008F8D80]` at reset; the per-entry update runs only while it is non-zero; not read by the sampler, which steps by `+0x20` / `+0x1A` and the two constants themselves |
| `+0x344` | `f32[3]` | the time window `0x0041D7E0` stores, −1.0 at reset |
| `+0x350` | `u32` | zeroed |
| `+0x354` | `f32` | blend step (command `0x08`) |
| `+0x358` | `u16` | ease word, `0x10` at reset; `+0x35A` the second ease word, 0 |
| `+0x35C` | `i32` | the ramp handle, −1 |
| `+0x360` | `i32` | −1 |
| `+0x364` | `u32` | request `+0x38` |
| `+0x368` | `void*` | the command stream |
| `+0x370` | `void*` | the motion file's data start (`0x004096C0` with offset 0); `+0x378` is added to it (`0x0041D470`-`0x0041D478`) |
| `+0x378` | `u32` | `@FRM` payload offset, −1 without one; `+0x37C` its second region |
| `+0x380` | `f32` | snapshot of an interrupted transition; `+0x384` its second value, 50.0 when armed |
| `+0x388` | `void*` | the playing track state |
| `+0x390` | `u8[16]` | not touched by the routines on this page |

### A track state (0xA0 bytes)

Set up by `0x0041CD30` and the bind `0x0041BEE0`; the reset values are `0x0041CF00`'s.

| Offset | Type | Field |
|---|---|---|
| `+0x00` | `i32` | −1 at reset |
| `+0x04` | `u16` | 0 at reset |
| `+0x06` | `u8[2]` | zeroed with `+0x04` |
| `+0x08` | `u16` | flags: bit `0x2` playing (the sampler's test), `0x6` at bind |
| `+0x0A` | `u16` | 1 when `+0x54` / `+0x58` are offsets to resolve (`0x0041CA70`), 0 otherwise |
| `+0x0C` | `f32` | the frame |
| `+0x10` | `u32` | zeroed |
| `+0x14` | `u16` | zeroed |
| `+0x16` | `u16` | the motion's duration in frames |
| `+0x18` | `u16` | the frame a state goes to past the end: 0 with `+0x96` bit `0x40` (loop), else the duration (hold) (`0x0041C193`-`0x0041C1A3`, `0x00419263`); 0 at reset |
| `+0x1A` | `u16` | 30 at reset |
| `+0x1C` | `f32` | `(duration − step) / duration` |
| `+0x20` | `f32` | 30.0 at reset |
| `+0x24` | `u8[32]` | the section name the bind looks up |
| `+0x44` | `u8[4]` | not touched by the routines on this page |
| `+0x48` | `void*` | the motion file |
| `+0x50` | `u16` | motion index, −1 at reset; `+0x52` the second index, −1 |
| `+0x54` | `u32` | `@FMN` (or `@FRP`) offset |
| `+0x58` | `u32` | `@FMW` offset |
| `+0x5C` | `u16` | the record word the resolve passes |
| `+0x5E` | `u16` | loop count (`0x00418750`, `0x0041883B`-`0x00418863`), −1 for no limit |
| `+0x60` | `void*` | the skeleton bank |
| `+0x68` | `u32` | the bound skeleton entry id, −1 at reset |
| `+0x6C` | `u8[4]` | not touched by the routines on this page |
| `+0x70` | `void*` | the `@FMN` record (resolved) |
| `+0x78` | `void*` | the `@FMW` data (resolved) |
| `+0x80` | `u32` | track number |
| `+0x84` | `u32` | track header offset |
| `+0x88` | `u32` | start cursor (the first command, or the one after a `0xFFFF` marker) |
| `+0x8C` | `u32` | cursor, back to `+0x88` at reset |
| `+0x90` | `i32` | marker, −1 for none |
| `+0x94` | `u8` | `0xFF` |
| `+0x95` | `u8` | 1 for the primary track |
| `+0x96` | `u16` | flags: bit `0x1` active, bit `0x4` finish, bit `0x10` blend, bit `0x20` the second set (`0x0041D4D0`), bit `0x40` makes the bind set `+0x18` to 0, bit `0x80` cleared at reset |
| `+0x98` | `f32` | progress |
| `+0x9C` | `f32` | rate |

### A channel row (0x108 bytes)

Built by `0x0041B550`; the slot fields are on [model effects](model-effects-and-motion-commands.md#stepping-a-channel).

| Offset | Type | Field |
|---|---|---|
| `+0x000` | `slot × 9` | nine `0x1C`-byte channel slots: `+0x00` `i16` the value `0x0041B650` is given, `+0x04` frame (`0xFFFF` for a single key or no data), `+0x06` next frame, `+0x08` previous value, `+0x0C` next value, `+0x10` frame cursor, `+0x16` value cursor |
| `+0x0FC` | `u32` | the record's offset from the `@FMN` section (`0x0041B582`-`0x0041B594`) |
| `+0x100` | `u16` | bone index |
| `+0x102` | `u16` | single-key mask, bit `7 + k` for channel `k` |
| `+0x104` | `u8[4]` | not touched by the routines on this page |

### A skeleton node (0x290 bytes)

Writers are the builder `0x00372820` (B), the initialiser `0x00373DC0` (I), the set reset `0x00372280`
(R), the composer `0x00373860` (C), the sampler `0x00418880` (S), the chunk link `0x00373160` (L) and the
placement `0x00373F40` (P).

| Offset | Type | Field |
|---|---|---|
| `+0x000` | `u8[64]` | skinning matrix slot A, written by C when byte `+0xA7` of the skeleton has 1 in its low nibble |
| `+0x040` | `u8[64]` | skinning matrix slot B, written by C otherwise; the slot in use is named by `+0x284` |
| `+0x080` | `u8[64]` | the bone matrix: rest pose from `0x00373D00`, each frame from C; the source of child bones; what bone lookups return |
| `+0x0C0` | `u8[48]` | the pose block: rotation from the pool (`0x00409300`) or the template `0x02CA43D0` (`0x0041D180`), written by S and the add-motion tracks |
| `+0x0F0` | `f32[4]` | translation (x, y, z from the pool; w 1.0 at `+0xFC`), written by S |
| `+0x100` | `f32[4]` | scale, 1.0 from B, rebuilt by S (`0x00418F83`); C multiplies it by `+0x1E0` on the second-set path |
| `+0x110` | `f32[4]` | quaternion the blend keeps ([model effects](model-effects-and-motion-commands.md#blending-into-a-new-motion)) |
| `+0x120` | `f32[4]` | the rotation `0x0041C260` keeps from `+0xC0` |
| `+0x130` | `u8[32]` | copy of `+0xF0`-`+0x10F` (B; `0x0041C260`) |
| `+0x150` | `u8[64]` | the bind-pose inverse: the pool matrix with record bit `0x200000`, else `0x01F204E0`; `0x00373EA0` would write the inverse rest pose for a kind-0 skeleton but runs over the listed count, 0 at build time; the last factor of C |
| `+0x190` | `f32[3]` | the three angles the add-motion tracks write ([add-motion tables](add-motion-tables.md#applying-a-track)), `+0x19C` 1.0 |
| `+0x1A0` | `f32[4]` | the second rotation set, `(0, 0, 0, 1)` from I and R; S writes it with `+0x96` bit `0x20` and turns it into a quaternion; C reads it on the second-set path |
| `+0x1B0` | `f32[4]` | translation copy from B, written by `0x00418700` |
| `+0x1C0` | `f32[4]` | the second translation set, `(0, 0, 0, 1)` from I and R, written by S with `+0x96` bit `0x20`, added to `+0xF0` by C |
| `+0x1D0` | `f32[4]` | 1.0 from B; written by `0x004186A0` (not for a tied bone), read by S |
| `+0x1E0` | `f32[4]` | the second scale set, 1.0 from I, written by S with `+0x96` bit `0x20`; C multiplies `+0x100` by it |
| `+0x1F0` | `u8[64]` | identity from B and I; on node 0 the skeleton's root matrix (P writes it for an attached skeleton; C and `0x00373D00` read it); P copies the parent bone's `+0x80` here for a tied root |
| `+0x230` | `u8[64]` | identity from B and I; a factor of both paths of C |
| `+0x270` | `i16` | parent node, −1 for a root (B from record bits `0xFFF000`, or the record word `+0x20` for kind 0; L, `0x00370180`, `0x00370890` and `0x00373380`) |
| `+0x272` | `i16` | next sibling (B; read only by B, `0x00372B8A`, `0x00372D80`) |
| `+0x274` | `i16` | first child (B; read only by B, `0x00372B67`, `0x00372D5B`) |
| `+0x276` | `i16` | parent bone in the parent skeleton for a tied root, −1 otherwise (L, `0x00370180`, `0x00370890`, `0x00373380`; read by C and P) |
| `+0x278` | `u32` | encoded address of the tied child bone, null otherwise (L, `0x00370180`, `0x00370890`, `0x00373380`, `0x00372F60`); the channel writers `0x00418650`, `0x00418700` and `0x004186A0` store into it too |
| `+0x27C` | `i16` | the tied child bone's node number (L, `0x00370180`, `0x00370890`, `0x00373380`, I); read by `0x00372F60` to re-point `+0x278` |
| `+0x27E` | `i16` | the node's own index |
| `+0x280` | `u16` | flags: bit `0x2` tied child (L), bit `0x4` set by B, bit `0x10` the second-set path of C, set by S with `+0x96` bit `0x20` and cleared by R and `0x0041C200` |
| `+0x282` | `u8` | bit `0x1` cleared by I (a word write) |
| `+0x283` | `u8` | layer, 0 from I; a bind with a layer takes only matching bones |
| `+0x284` | `u32` | encoded address: the node itself from B, then the skinning slot C chose; read by C's partner copy and the oscillator apply (`0x0040EC53`-`0x0040EC94`) |
| `+0x288` | `u8[2]` | not touched by the routines on this page |
| `+0x28A` | `u8` | 3 from I; bit `0x1` cleared by S on every bone it samples whose byte is non-zero (a bone at 0 takes its rest pose), bit `0x2` set by the oscillator apply `0x0040ED90`; the bind reads both bits |
| `+0x28B` | `u8` | bits `0x1` and `0x2` set and bit `0x4` clear from I; the bind rewrites bits `0x1` and `0x2`; bit `0x2` marks a bone the blend cross-fades (`0x00418E74`); bit `0x4` makes `0x0041D6F0` take the whole rest pose (`0x0041D73C`) and is cleared by `0x0040ED90` |
| `+0x28C` | `u8[2]` | not touched by the routines on this page |
| `+0x28E` | `i16` | the parent link saved by L, tested by L's root handling |

## State

- `[0x01EF9438]`, normally `0x02AD9EC0`: the scratch bone list the bind claims bones from.
- `0x02AD9E40` and `0x02AD9E80`: the composer's two product matrices, copied into `+0x80` and the skinning slot.
- `0x01F204E0`: the identity matrix `0x0046D110` copies into a pool node's `+0x150` without record bit `0x200000`.
- `0x02CA43D0`: the 48-byte pose template `0x0041D180` copies into `+0xC0`.
- `0x01DFE0BC` and `0x008F8D80`: the frame constant and rate whose product is the entry's step `+0x340`.

## Related

- [Presentation entries](presentation-entries.md): the reference container, the track pick, the selectors and the per-entry update.
- [Authored presentation commands](authored-presentation-commands.md): the command handlers that switch tracks and arm blends.
- [Model effects and motion commands](model-effects-and-motion-commands.md): `@FMN`, `@FMW`, the channels, stepping, applying a frame and the blend.
- [Skeleton entries and bones](skeleton-entries-and-bones.md): skeleton entries, bone lookups, the motion bone list and the tie.
- [Model files](model-files-cm-ca.md): `@FTR`, the node records and the pool.
- [Add-motion tables](add-motion-tables.md): the angle tracks at `+0x190` and `skeletonmapping.bin`.
- [Model oscillators and the pose sequencer](model-oscillators-and-pose-sequencer.md): the sway written into `+0x80` and the `+0x28A` bit it sets.
- [Character render records](character-render-records.md): the attach slots and the equipment tie.
