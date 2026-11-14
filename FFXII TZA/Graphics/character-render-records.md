---
title: "Character render records: the record array, the pool lifecycle, parents and attachment, and render events"
kind: "system"
category: "Graphics"
addresses: "0x003325D0, 0x022C6F28, 0x022C6F20, 0x022C6F30, 0x0041E3A0, 0x0041E550, 0x004269A0, 0x00426480, 0x0042FB80, 0x004279B0, 0x004278E0, 0x0041F730, 0x00420480, 0x00428710, 0x00427C90, 0x00429140, 0x004200A0, 0x00426EC0, 0x0042ED60, 0x00332660, 0x003323D0, 0x00426090, 0x00427DE0, 0x00427BD0, 0x00426420, 0x0051F9F0, 0x0051FBB0, 0x0051F6B0, 0x002ED570, 0x00409FE0, 0x0046E4D0, 0x004780C0, 0x0051BA80, 0x0051B9F0, 0x0051B970, 0x00424D80, 0x004235C0, 0x0041FCA0, 0x00424230, 0x01F00410, 0x0041CFC0, 0x004215A0, 0x0042F880, 0x0042F310, 0x0042F3B0, 0x00422310, 0x00422380, 0x01EFFFB0, 0x01F00060, 0x004219C0, 0x004218A0"
---

## What the player sees

Every character model on screen, from the party to an NPC, a monster, a summon or a weapon attached to
a hand, is drawn from one render record. There are 160 of them, allocated once at start-up; a request
for a record past the 160th is refused. The record is where a character's look is kept between frames:
which motion event it is playing, how faded it is, its shadows and its colour. When a scene adds a
character, its record waits one update on a pending list before it is drawn.

## How it works

### The render resource root

`0x022C6F20` holds the pointer to the render resource root, which is the static block at `0x022C6F30`
(`0x003323D0` and `0x00332660` store `&0x022C6F30` there each time they run). `0x003325D0` runs once: it stores its
argument as the root, allocates the record array (`0x0036A100(0x48930)`, pointer at `0x022C6F28`), clears
the root's four bank pointers (`0x0041E550`), builds them (`0x0041E3A0`), initialises the record system
(`0x004269A0`) and stores the root's encoded address in the system tail (`0x00426480`; its first argument,
`0xA0`, is never read).

`0x003325D0` allocates the record array under arena 6: `0x0036C1D0(6, 6)` before `0x0036A100` and `0x0036C140` after it
(`0x003325E2`-`0x003325F8`). `0x003323D0` runs `0x004262E0` on the record array, `0x00426560`, the record step `0x00426090`,
`0x0041E340(root)`, `0x00425E10` on the record array and `0x004288E0`, and ends with a tail jump to `0x00428F80`
(`0x003323D4`-`0x00332419`).

`0x00332660` refreshes the root (`0x0041E500`), runs `0x00426950` and calls `0x003697C0(6)` only when `0x00369CF0(6)` is
non-zero (`0x00332684`-`0x0033269F`). It then runs `0x004262E0` on the record array it read on entry and ends with a
tail jump to `0x0042ED60` (`0x003326A4`-`0x003326B6`).

`0x0041E3A0(root, 10, 10, 5, 5, 0x13, 0x2A00, 0x16000)` points each bank at storage inside the root and
initialises it. It forwards only three of its counts; the reference container always takes 64 nodes.

In order (`0x0041E3B4`-`0x0041E484`):

1. It zeroes the four bank pointers and runs the bone-trail pool set-up `0x0051C270`
   ([bone trails](bone-trails.md#the-pool)).
2. It points the banks at the root and runs `0x00409F80`, which fills the `@FEF` path table with `0x0040A230`
   ([model effects](model-effects-and-motion-commands.md#the-fef-path-table)) and then resets the first bank's
   descriptor, the root itself, with a tail jump to `0x0051FB70` (`0x00409F8D`).
3. It resets the descriptors of the other three banks (`0x0046E4B0`, `0x00478040`, `0x0051BA20`) and forgets the
   texture slot cache (`0x00521300`).
4. It runs the four initialisers below, and last allocates that cache with `0x005211F0`
   ([model files](model-files-cm-ca.md#the-texture-slot-cache)).

| Root field offset | Points at | What it holds | Initialiser |
|---|---|---|---|
| `+0xD90` | root `+0x000` | render resource entries, `0x50` bytes, 10 chunks of 32 | `0x00409F10` → `0x0051F9F0(bank, 0x50, 5, 10, 0x02B62E40, 0x02B62F80)` |
| `+0xD98` | root `+0x060` | skeleton entries, `0xC0` bytes, 5 chunks of 32 | `0x0046E250` → `0x0051F9F0(bank, 0xC0, 5, 5, 0x02CA61B0, 0x02CA6250)` |
| `+0xDA0` | root `+0x0F0` | render model instances, `0x260` bytes, 5 chunks of 32 | `0x00477EE0` → `0x0051F9F0(bank, 0x260, 5, 5, 0x02CA74A0, 0x02CA7540)` |
| `+0xDA8` | root `+0x160` | presentation-entry references, 64 nodes of `0x30` at root `+0x190` | `0x0051B9D0` → `0x0051F170(container, 0x40, root + 0x190)` |

`0x0041E500(root)` refreshes all four after their storage moves: the [render resource bank](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md#the-render-resource-bank) through
`0x00409F70` (with the byte `0x02B62E10` held at 1), the skeleton bank through `0x0046E3E0`, the reference
container through `0x0051B9F0` and the instance bank through `0x00478030`. `0x0041E340`, which `0x003323D0`
runs after the record update, updates the reference container (`0x0051B970`) and then the skeleton
bank (`0x0046E0F0`).

### The chunked banks

The first three banks share one generic container, `0x60` bytes, built by `0x0051F9F0(bank, element
size, shift, chunk count, chunk table, slot table)`. With shift 5 a chunk holds 32 elements. The
initialiser allocates `chunks << shift` elements in one block, stores each chunk's encoded base, and
claims chunk 0 at once (`0x0051F6B0`).

`0x0051F6B0(bank)` returns -1 when the chunks in use, word `+0x22`, have reached the chunk count `+0x24`
(`0x0051F6CA`). Otherwise it looks from the cursor word `+0x20` for a chunk-table entry (`0x20` bytes at `+0x10`,
re-resolved with `0x003AB7F0` from `+0x08` when that is set) whose first dword is -1, stepping the cursor past used
entries and wrapping it at the count, and returns -1 when every entry is used (`0x0051F6F0`-`0x0051F738`).

`0x0051F6B0` writes the chunk's index into that dword, links the entry at the tail of the chunk list (head `+0x18`,
tail `+0x1C`; entry `+0x04` previous, `+0x08` next), counts it in `+0x22` and returns the index
(`0x0051F73D`-`0x0051F785`).

- `0x0051FBB0` takes a slot: it refuses when the used count `+0x58` has reached the capacity `+0x54`,
  finds a chunk with a free slot (`0x0051F7A0`, claiming a new chunk when needed), scans that chunk for a
  slot whose first dword is -1, appends it to the active list (head `+0x40`, tail `+0x44`), and keeps
  the high-water mark in the word `+0x26`.
- `0x0051FBB0(bank)` returns -1 on that refusal (`0x0051FBC5`-`0x0051FBCA`) and when `0x0051F7A0` returns null
  (`0x0051FBE6`-`0x0051FBE8`). The scan starts at the chunk's cursor `+0x18`, slot `(chunk index << shift) + cursor`,
  steps the cursor on, back to the chunk's first slot at the chunk size, and looks at no more than one chunk's
  slots, 16-byte entries at `+0x38`, re-resolved with `0x003AB7F0` from `+0x30` when that is set
  (`0x0051FC09`-`0x0051FC6F`).
- It counts the slot in the chunk's `+0x14` and the bank's `+0x58`, writes the slot's index into its first
  dword, links it after the old tail (the tail entry's `+0x08` next, the slot's `+0x04` previous; the head
  `+0x40` too when it is -1), raises the word `+0x26` to the used count when it is lower and returns the index
  (`0x0051FC71`-`0x0051FCD3`).
- `0x002ED570(bank, index)` returns the element: chunk `index >> shift`, offset `(index & mask) × size`,
  or null for a free slot. `0x0051FF30` and `0x00520010` walk the active list with a callback.
- Each bank has its own acquire: `0x00409FE0` for render resource entries (it returns an existing entry for the
  same resource, found by `0x0051FE30`, before taking a slot), `0x0046E4D0` for skeleton entries and
  `0x004780C0` for model instances.

A record reaches the banks by index: `+0x18` selects its skeleton entry (`0x00427BD0`, `0x00421FF0`), `+0x64`
its model instance (`0x003E55B0`), `+0x408` its `@FCP` section in the render resource bank, and `+0xC4` /
`+0xC8` its presentation entries. Skeleton entry `+0x84` is the bone array, `0x290` bytes per bone with
the bone matrix at `+0x80` (`0x00370F60`); entry `+0xA8` is the owning record's index.

### Allocation

`0x0042FB80` is the only caller of the allocator. It refuses when the live count is 160, builds the
record's key as the literal `makeid` (`0x00D12474`) followed by one raw byte, the next-free cursor, and
calls `0x004279B0(key, name, …)` with the 32-byte name of the current model container (`0x00409090` on
`0x003AB7F0()`). It returns the new record's index, or -1.

`0x0042FB80(handle, variant, colour)` hands its first argument to `0x003AB7F0` and returns -1 when no container
resolves (`0x0042FBDA`-`0x0042FBE2`) or the live count `+0x4880C` is 160 or more (`0x0042FC08`-`0x0042FC12`). The cursor
byte `+0x48808` is appended as a one-character string, so a cursor of 0 leaves the key `makeid`
(`0x0042FC14`-`0x0042FC5E`). The variant and the colour are `0x004279B0`'s third and fourth arguments
(`0x0042FC60`-`0x0042FC70`), and the index is the signed word `+0x00` of the record it returns, -1 when it returns
null (`0x0042FC75`-`0x0042FC7F`).

`0x004279B0` searches the active list (skipping records with `+0x290` bit `0x2`) and the pending list by key
(`0x004278E0`), refuses on a match or a full pool by returning null (`0x004279D7`-`0x004279F3`), and then:

1. clears the record at the cursor (`0x0041F730`);
2. appends it to the pending list (tail `+0x10` / `+0x14`, links at record `+0x02` / `+0x04`);
3. writes the record's own index into `+0x00`;
4. runs the initialiser `0x00420480` with the key, the name, the tail's `+0x30` decoded by `0x0020E600`, the variant
   and the colour (`0x00427A50`-`0x00427A71`);
5. sets `+0x290` bit `0x1` and increments the live count;
6. advances the cursor to the next record whose `+0x284` is 0, wrapping at 160, or sets it to 0 when the live
   count has reached 160 (`0x00427A85`-`0x00427ADA`).

It returns the record (`0x00427ADC`).

The initialiser ORs `0x2010F9` into `+0x284`, copies the key to `+0x1C` and the model name to `+0x3C`,
sets `+0x284` bit `0x4000` for a name starting `c`, `m`, `n` or `s`, stores the context at `+0x10`, finds the
model's `@FCP` and `@FOR` sections through the render resource bank, and picks a per-model float at
`+0x734` from the name (2.0 for `s0011`, for example; 1.0 for a name outside `s`, `m` and `n`).

### Promotion, retirement and clearing

`0x0042ED60` runs once per frame, from `0x00332660` at the end of the field frame
([frame update order](../Engine-Core/frame-update-order.md)):

1. it clears tail flag bit `0x20`, runs the active sweep `0x00427C90` and the promoter `0x00428710`;
2. when either set bit `0x20` again, it refreshes the root (`0x0041E500`), re-binds every active record
   (`0x0042DA30`) and calls `0x003697C0(6)`;
3. it runs the dirty-word walk `0x00427DE0(1)` and the transform commit `0x00427BD0`.

The promoter takes every pending record in order: it binds the model resources (`0x0041FCF0`), stamps
`+0x414` from tail `+0x28`, takes a shadow entry into `+0x114` when `0x003E68E0` allows it
([character lighting and shadows](character-lighting-and-shadows.md)), runs `0x0042C410` with tail bit `0x1`
held clear, clears `+0x290` bit `0x1` and moves the record to the end of the active list.

The shadow entry is `0x003B56D0` of the record's index (`0x00428782`-`0x0042878A`). `0x0042C410` gets the record and the
record array, and tail bit `0x1` goes back to its earlier value after it (`0x00428790`-`0x004287B7`). Each move sets
tail flag bit `0x20` (`0x00428863`). The promoter reads the next pending index before the work, and at the end
sets the pending head and tail to -1, also when the list was empty (`0x0042888C`-`0x00428893`).

Removal is in two steps. `0x00429140(record)` is the request:

| Record state | What `0x00429140` does |
|---|---|
| null | nothing, returns 0 |
| `+0x284` bit `0x4` set | marks it: `+0x290` bit `0x2`, `+0x2AE` bit `0x1`, clears `+0x108`..`+0x113`, swaps `+0x284` bit `0x4` for bit `0x40000000`; clears bit `0x2` of its presentation entry's `+0x0C` and bit `0x4` of its skeleton entry, each when it exists, and stores the encoded null (`0x0020E620(0)`) at that skeleton entry's `+0xA0` (`0x0042916F`-`0x004291F3`); returns 1 |
| bit `0x4` clear, `+0x290` bit `0x1` set (still pending) | unlinks it from the pending list, decrements the live count (resetting the cursor to 0 at a count of 0, `0x0042927D`-`0x00429288`) and clears it (`0x0041F730`); returns 1 |
| otherwise | nothing, returns 1 (`0x00429296`) |

The active sweep `0x00427C90` then retires every active record with `+0x290` bit `0x2`: it unlinks it,
decrements the count (resetting the cursor to 0 at a count of 0), runs `0x0042F4C0`, detaches every
child (`0x00426EC0`), frees the two shadow entries (`0x003B6000`, `0x003AFBE0`) and tears the record down
(`0x004200A0`, which frees the record's buffers and returns its CharacterRenderObject, then clears the record).

The sweep detaches the first child `+0x08` until that word is -1 (`0x00427D5E`-`0x00427D8B`), frees a shadow entry
only when its handle, `+0x114` or `+0x118`, is non-zero (`0x00427D8D`-`0x00427DA6`), and sets tail flag bit `0x20`
for each record it retires (`0x00427DB3`).

`0x004200A0` runs `0x0046C240` on the sound emitter `+0x5F0`, `0x0041E860` on the record, `0x003AEF30` on the
tween object `+0x550`, `0x003E69A0` (which hands the handles `+0x448` and `+0x44C` to `0x003D8300` when they are
non-zero) and `0x00512C80` on `+0x650` (`0x004200AD`-`0x004200DC`). It hands the dword `+0x64C` to `0x0024CFF0`, which
ends a running effect job, when it is non-zero and zeroes it (`0x004200E1`-`0x004200F2`).

`0x0041E860(record)` runs in this order: `0x0042F190(+0x270)` when the dword is not 0; for
each of the four dwords at `+0x438` that is not `0xFFFF`, `0x0051BC10` on it and then
`0xFFFF` stored; `0x00422C20(record)`; the skeleton entry `+0x18`, when not -1, released
with `0x0046E2B0`, whose first argument is the qword `+0xD98` of the answer of
`0x0020E600(+0x10)` (`0x0041E877`-`0x0041E8D2`).

It then walks the eight words at `+0x90` and gives each to `0x00478070`, with the qword
`+0xDA0` of the answer of `0x0020E600(+0x10)` as first argument, stopping at the first
that is `0xFFFF` (`0x0041E8D7`-`0x0041E909`); sets the word `+0x64` to `0xFFFF`; runs
`0x00477640(+0x450)` and `0x003B3300(+0x288)` when the dword is not -1; sets `+0x18` to -1;
and ends in a jump to `0x003AB7C0` with the answer of `0x0020E600(+0x2FC)`
(`0x0041E90B`-`0x0041E957`).

`0x004200A0` returns the CharacterRenderObject `+0x6B8` to its manager with `0x0017F100`, which skips a null object,
and zeroes `+0x6B8` (`0x004200F8`-`0x0042010B`). It frees each of the buffers `+0x6C0`, `+0x6D0`, `+0x6F8`, `+0x700`,
`+0x708`, `+0x710`, `+0x720` and `+0x728` that is set with `_aligned_free` (`0x0019C570`) and zeroes it, zeroes
`+0x6E8` and `+0x6F0` (`0x00420104`-`0x004201D5`), and ends with a tail jump to the clear `0x0041F730` (`0x004201E6`).

The clear `0x0041F730` zeroes all `0x740` bytes and writes the defaults: word `+0x00` = -1, links -1,
fade channels at 1.0 (`0x003E5D00` for channels 0 to 9), colours `+0x210` and `+0x220` at 1.0.

### Parents and children

A record can be attached to another: word `+0x06` is the parent index, `+0x08` the first child and
`+0x0A` the next sibling. `0x00426EC0` unlinks a child from its parent's chain. Walks that need the
hierarchy go through `0x00425FB0(root callback, child callback, …)`, which runs the first callback on
each active record without a parent and the second on its descendants (`0x0042EF90`).

`0x00426EC0(child)` does nothing when the child's `+0x06` is -1 (`0x00426EC7`). Otherwise it replaces the child's
index in the parent's `+0x08`, or in the `+0x0A` of the sibling before it, with the child's `+0x0A`, and sets the
child's `+0x06` and `+0x0A` to -1 (`0x00426EFD`-`0x00426F97`). A parent or sibling whose `+0x284` is 0, or a chain
that ends without reaching the child, leaves the chain as it is, and only the child's two words are cleared.

Many setters broadcast a value the same way: they apply it to the record and its first child, then
hand a small per-record body and an argument block to `0x0042EF90` for the rest of the tree.

Most bodies first ask `0x00426220(record, source)` and skip the record when it answers true: a record other than the
source is skipped when its `+0x284` bit `0x4000000` is clear and its word `+0x2F8` is −1; a record with bit
`0x8000000` and an event below `0x1000` (`+0xCC`) is skipped when `0x004232D0` returns 0; past those tests the source
itself is kept, a record whose name `+0x3C` starts with `h` is kept only when its next five characters equal the
source's first five, and any other record is skipped when the source's name starts with `b`.

| Body | Broadcast | What the body does to each record |
|---|---|---|
| `0x0042BDD0` | `0x00425E70` | `0x003E6770(record, arg +0x38)` |
| `0x0042D810` | `0x00428B30` | copies bit `0x8` of the argument's byte `+0x60` into bit `0x8` of `+0x4B7` |
| `0x0042D9C0` | `0x00426650` | when `0x00421D70(record, word +0x1C)` finds a bone, stores the record at `+0x20`, the bone at `+0x28` and 1 at `+0x18` of the argument (a search) |
| `0x0042DA00` | `0x00426770` | the same search through `0x00421E20` with the word `+0x08`, dword `+0x0C` and pointer `+0x10`, storing the result at `+0x10` |
| `0x0042DE50` | `0x00429D40` | `0x0041FBF0(record, arg +0x38)`, then `0x00421030` |
| `0x0042DE90` | `0x00426FA0` | sets bit `0x100000` of `+0x284` and clears bit `0x40` of `+0xC0` |
| `0x0042DEC0` | `0x00429E50` | `0x00422DF0`; with the argument's `+0x6C` set, also bit `0x20000` of the `+0x0C` of the entry `0x00422D50` returns |
| `0x0042DFC0` | `0x00427100` | calls `0x00422EB0`, except on a child whose `+0x2F2` is not 1, whose `+0x2F8` is −1 and whose `+0x284` bit `0x8000000` is clear; a record without a parent stores the result, or 0, at the argument's `+0x58` |
| `0x0042E050`, `0x0042E170`, `0x0042E1B0` | `0x0042A180`, `0x0042AA10`, `0x0042AB20` | the float `+0x28` through `0x00425510`, `0x00423A60` or `0x00423AB0` |
| `0x0042E090` | `0x0042A290` | `0x00423570(record, arg +0x24)` |
| `0x0042E130` | `0x0042A890` | below `0x1000` in word `+0x3FA`, `0x0041FC80`; then `0x00423A10` |
| `0x0042E300` | `0x0042AC30` | copies word `+0x20` to `+0x3FA` when `+0x2F2` is non-zero (no filter); `0x0042AC30` reaches this only when the answer it kept is not negative (`0x0042AD38`-`0x0042AD3A`): it stores the record's word `+0x3B4` at the record's `+0x3FA` (`0x0042AD47`-`0x0042AD4E`) and, only with the record's dword `+0x6C8` equal to 1 and a word `+0x08` other than `0xFFFF`, gives the copy of `+0x3B4` it took at `0x0042ACCE`-`0x0042ACD5` (the word `+0x20` the body copies) to the named record's `+0x3FA` when that record's `+0x2F2` is not 0 (`0x0042AD82`); with or without that store it hands the body to `0x0042EF90` for the named record's words `+0x08` and `+0x0A`, each when not `0xFFFF` (`0x0042AD9F`, `0x0042ADBA`). The copy is taken before the first pass, `0x0042E1F0` on the named record (`0x0042ACFD`) and `0x0042EF90` with `0x0042E1F0` for its words `+0x08` and `+0x0A` (`0x0042AD18`, `0x0042AD33`; `0x0042ACD9`-`0x0042AD33`), in which `0x004292B0`, called by `0x0042E1F0` with the record as its second argument (`0x0042E20E`-`0x0042E215`), can change the record's `+0x3B4` from `0x104A` to `0x103D` (`0x004292F7`-`0x004292FC`), so the two stored words can differ |
| `0x0042E320`, `0x0042E350`, `0x0042E4B0` | `0x0042AE00`, `0x0042AF10`, `0x0042A580` | on a record without a parent or whose `+0x2F2` is 1, call the bare `ret` `0x0016D6A0`; `0x0042E4B0` also stores 0 at the argument's `+0x58` for a record without a parent |
| `0x0042E440` | `0x0042A390`, `0x0042B130`, `0x0042B270` | `0x00424010` with the three floats `+0x2C`–`+0x34` |
| `0x0042E4F0` | `0x00428CD0` | `0x00504D20` on the record's model row (`0x003E55B0`) with dword `+0x20` |
| `0x0042E530`, `0x0042E540` | `0x0042B690`, `0x0042B770` | `0x00420D80` or `0x00420E70` with dword `+0x74` (no filter) |
| `0x0042E610`, `0x0042E650` | `0x0042B850`; `0x0042B970`, `0x0042BA90` | `0x00420F50` or `0x00420EA0` with dword `+0x38` |
| `0x0042E750`, `0x0042E7A0` | `0x0042BCB0`, `0x00429020` | set bit `0x200000` of `+0x284` when `+0x38` is non-zero and clear it when it is 0 (`0x0042E772`, `0x0042E787`), or set bit `0x1000` when it is 1 and clear it otherwise (`0x0042E7C3`, `0x0042E7D8`) |

`0x00426500`, from `0x00332440`, is one such walk: `0x00425FB0(0x0042D7A0, 0x0042CF70, records)`.

A record keeps two attached children by id: word `+0x2C8` for the child whose slot byte `+0x6A0` is below `0x16`, and
`+0x2CA` for the child of slot `0x16`. The event start `0x00424D80` clears `+0x40B` bit `0x10` and leaves the children
in place when the low two bits of `+0x40B` equal its bits under mask `0xC`. Otherwise it sets bit `0x10` for an event
of kind 0, or of kind 3 or 4 with number `0x35` or `0x36`, and leaves them in place for those as well. For any other
event it re-places both through `0x0041F010(record, child)`, which `0x004215A0` also calls:

1. it stores a slot below `0x16` at `+0x40C`, and takes the mode from the low two bits of `+0x40B`
   (0 while `+0x284` bit `0x8000000` is set) into the bits under mask `0xC` of `+0x40B` (`0x0041F080`-`0x0041F09A`);
   modes 2 and 3 go straight to step 6;
2. in mode 0, when the record's `@FCP` section 3 (`0x003E5CD0`) names a bone for the slot (word table
   at its start), it ties the child to that bone with `0x004211B0`, which links the two skeletons
   with `0x0046E640` when the child's skeleton entry has bit `0x80` of its first byte and sets the child's
   parent word `+0x06`;
3. still in mode 0, it copies the slot's angles (section `+0x240 + 12 × slot`) to the child's
   `+0x130` with 1.0 at `+0x13C`, and stores at `+0x150` the record's three scales (`+0x160`,
   `+0x260` and `+0x26C`) times the slot's position at section `+0x40 + 12 × slot`;
4. in mode 1, or without a section bone, it ties the child to the record's bone for the child's
   `@FCP` word `+0x36` (`0x003E5AD0`, bone 0 when it names no bone) and, when the section exists, zeroes
   the angles and the position;
5. with a section, it writes the slot's scale at `+0x1C0 + 4 × slot` to the child's `+0x170`,
   `+0x174` and `+0x178`, and 1.0 at `+0x15C` and `+0x17C`;
6. it stores the child's id at `+0x2C8` or `+0x2CA`.

`0x00420A40` builds the child's local matrix from what these steps stored: the rotation from the angles `+0x130` through
`0x0046D380` (`0x00420AF5`-`0x00420B02`), `+0x170` to `+0x178` on its diagonal (`0x00420AB9`-`0x00420AF0`) and
`+0x150` to `+0x158` as its translation (`0x00420B18`-`0x00420B3A`).

[`model-files-cm-ca-fcp-attachment-slots.tsv`](model-files-cm-ca-fcp-attachment-slots.tsv) lists section 3 of all 603
models that have it, 32 slots each. A child's slot is byte `+0x38` of its own `@FCP` payload (`0x00420601`); shipped
values run up to 31, and 41 models hold 23 or more. The section is 960 bytes, read by `0x0041EE40` and `0x0041F010`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `u16[32]` |  | bone, `0xFFFF` for none |
| `+0x040` | `f32[3][32]` | position |  |
| `+0x1C0` | `f32[32]` | scale |  |
| `+0x240` | `f32[3][32]` | angles |  |

A slot with bone `0xFFFF` takes the fallback of step 4, and its scale is still written. 2,746 slots name a bone below
the model's `@FTR` node count and 16,497 name none.

The other 53, all in seven models under `high/`, name a bone at or past that count. The bone becomes the child
skeleton's word `+0x14` (`0x003731F7`), and `0x00373F40` indexes the parent's `0x290`-byte node records with it without
testing the count (`0x00373FC5`-`0x00373FD7`). The table is produced by
`Database/Tools/catalogues/fcp_attachment_slots.py`.

Small record setters beside them: `0x00420CF0(record, x, y, z)` keeps the angles `+0x120`–`+0x128` at
`+0x250`–`+0x258` and stores the new ones, and `0x00420F20(record, x, y, z)` stores `+0x140`–`+0x148`;
both set the fourth float to 1.0 and clear `+0x284` bit `0x200`. `0x00421010(record, on)` sets or clears
`+0x284` bit `0x8` and calls `0x00421030`; `0x004209A0` clears bit `0x8000000` and sets bit `0x4000000`. `0x00421CD0` returns the
first of the `@FCP` bones for special ids `0x104` to `0x106` that is set, or 0 (always 0 below
`@FCP` version 3).

`0x00422D90(file, index)` resolves the block with `0x003AB7F0`, finds its `@FRM` entry (`0x4D524640`, `0x00408F90`) and
returns the payload at `+0x30` of the address `0x00408F80` gives, cut to 32 bits and sign-extended
(`0x00422DC5`-`0x00422DCC`), or 0 when the block is null or has no `@FRM` entry (`0x00422DA1`, `0x00422DBE`).

`0x00422E40` is `0x00424870(…, 1)`; `0x00424280` wraps an angle in degrees into −180 to 180; `0x0042FCB0` counts
`0x02CA4EDC` up, for `0x002EAD00`.

`0x00424870(record, frames, mode)` starts a transition of the current entry `+0xC4` into its motion.
It runs `0x0041CFC0`, hands the three floats `+0x2B0` to `+0x2B8` to `0x0041D7E0` and sets them to −1,
restarts the entry (`0x0041D110` when its `+0x24` is 1, otherwise `+0x0C` bit `0x2`, `+0x24` = 1 and
`0x0041D790`), sets bit `0x800` of `+0x0C` (and `0x20000` for mode 1), stores `1 / frames` at
`+0x354`, clears bit `0x100` when `+0x344` is −1, and calls `0x00423AB0(record, +0x2BC)`.

With
`+0x284` bit `0x100000` set or 0 frames it instead stops the alternate entry `+0xC8` (`+0x0C` bit `0x2`,
`0x0041D790`) after `0x00426FA0` and returns `0x00424C40(record)`.

`0x00424A40` is the same without `0x0041CFC0` and returns 0 at once when the current entry's `+0x24` is already 1. The
child callback `0x0042DF10`, from `0x00429F70`, does nothing for a child that `0x00426220(child, parent)` refuses. A child
with `+0x06` not −1, `+0x2F2` not 0 and `+0x2F8` not −1 looks up its own event for the parent's event (`0x0041E5B0`) and
goes to `0x00423FC0` when it has one. Every other child takes `0x00422E40` when its `+0xCC` is below `0x1000`, otherwise
`0x00422E50`, which first stops the child's alternate entry and then calls `0x00424A40(child, frames, 1)`.

`0x00423510(record, resource)` returns the payload of the resource's `@FRM` (`0x00408F90`, `0x00408F80`)
plus the dword at its `+0x0C`, or 0 when the section is missing or that dword is 0; `0x003E6070`
reads three floats there.

### Attaching a record: the pending tie and the slot table

A tie is requested by `0x0042F310` or `0x0042F3B0` (`(child, parent, slot)`;
[chocobos](../World-Areas-And-Travel/chocobos-and-airships.md) has the actor-level caller). Both return at once when
either id is -1 (`0x0042F314`, `0x0042F31E`, `0x0042F3B4`, `0x0042F3CF`). An id's record is `[0x022C6F28] + 0x740 × id`, taken
as null when its `+0x284` is 0; a null parent faults on the read of its `+0x284` (`0x0042F347`, `0x0042F3FD`). A parent
with `+0x284` bit `0x4` set also gets `+0x284` bit `0x40000000` (`0x0042F34E`-`0x0042F356`, `0x0042F404`-`0x0042F40C`).

`0x0042F3B0` takes three vectors after the slot and hands them to the child record before it tests the child for null:
the fourth argument to `0x00420CF0`, the fifth to `0x00420F20` and the sixth to `0x00420D50` (`0x0042F41A`-`0x0042F47D`), so a
null child faults in `0x00420CF0`. `0x00420D50(record, x, y, z)` stores the scales `+0x160`-`+0x168` with 1.0 at `+0x16C`
and clears `+0x284` bit `0x200`, as the setters `0x00420CF0` and `0x00420F20` above do. `0x0042F310` skips a null child
(`0x0042F37D`).

They store the parent's id at the child's `+0x3CE`, the slot at `+0x3CC`, set `+0x290` bit `0x80000` and clear
its bits `0x40000` and `0x100000` (`0x0042F382`-`0x0042F3A0`, `0x0042F487`-`0x0042F4A4`). The
request service `0x00427DE0` sees the bit (`0x00427F44`-`0x00427F53`) and runs `0x0042F880`. That
function hands the parent, the slot and the child to `0x004215A0` (`0x0042FA1C`-`0x0042FA29`), which picks the path
by bit `0x80` of the child's skeleton entry (`0x00421649`) and resolves the slot in the parent:

| Slot | Skeleton with keyed bones (entry `+0x00` bit `0x80` set) | Skeleton with named bones (bit `0x80` clear) |
|---|---|---|
| `0x7FFF` | the whole skeleton (`0x004219C0` with key −1, `0x00421661`-`0x0042166A`) | no name |
| `0x10A` | `0x0041F010(parent, child)` (`0x004216F7`-`0x00421707`) | the name `0x00422310` gives |
| `0x102`, `0x103` | as slots 2 and 3 | the name `0x00422310` gives |
| below `0x100` | the bone `0x003E5AD0` gives for the slot as a special id, tied with `0x0046E640`; bone key `0x1E` when it gives `0xFFFF` (`0x00421738`-`0x00421768`) | entry `slot` of the name table `0x01EFFFB0` (`0x00422347`) |
| other | the key `0x00422380` gives (`0x0042176A`-`0x0042177A`) | the name `0x00422310` gives |

A keyed tie goes through `0x004219C0(parent, key, child)` and a named one through `0x004218A0(parent, name, child)`
(`0x00421841`-`0x00421852`). Afterwards the child's word `+0x06` is the parent's id and `+0x2F0` the slot
(`0x00421861`-`0x00421868`).

`0x004219C0` ties nothing when either record has no skeleton entry (`0x004219E4`-`0x00421A60`). With key −1 it sets the
child's `+0x284` bit `0x4000000` and `+0x2F2` to 1 (`+0x2F2` is 0 otherwise) and ties the whole skeleton at slot
−1 (`0x00421A62`-`0x00421A7E`); another key is looked up with `0x00372800` and retried as `0x1E`, and when both give −1
it ties nothing (`0x00421A87`-`0x00421AB1`). After `0x0046E640` a child with bit `0x4000000` set gets `0x003E5D30`, fade
channels 0, 1 and 4 back to 1.0 (`0x00421AC6`-`0x00421AD5`).

`0x0042F880` returns without a tie, so `+0x290` bit `0x80000` stays set for the next pass, when the child's `+0x3CE`
is -1, the parent record is null or either record's model instance (`0x002ED570` of `+0x18`) is null
(`0x0042F889`-`0x0042F93E`), and when a piece (kind `0x1C` or above) in slot `0x10A` has a parent whose word `+0x2C8`
is -1 (`0x0042F956`-`0x0042F97C`). For such a piece whose `+0x2C8` record (`0x003326C0`) has a kind of `0x11` to
`0x15`, that record takes the parent's place (`0x0042F982`-`0x0042F9CD`).

When that `+0x2C8` record's `+0x284` is 0, `0x003326C0` answers 0, and the kind read `0x003E5CF0` reads byte
`+0x6A0` through it with no null test (`0x0042F98A`).

Before the tie it calls `0x0020E600` with the dword at `[0x022C6F28] + 0x48830` and leaves the result unused
(`0x0042F944`-`0x0042F951`). A child whose word `+0x06` is not the new parent's id and whose own record is live gets
`0x004288B0(child, -1)` (`0x0042F9D0`-`0x0042FA01`), and a child with a parent (`+0x06` not -1) gets bit `0x40` of
`+0x3D1` and `0x0042F4C0` (`0x0042FA06`-`0x0042FA17`).

After `0x004215A0` it sets channel 1 to 0 for a hidden piece ([character fades](character-fades.md),
`0x0042FA2E`-`0x0042FA3E`). For slot `0x7FFF` it stores `0x00421CD0(parent)` at `+0xB6` of the child's model instance
(`0x003E55B0`) and runs `0x004780B0` on the parent unit's `+0xDA0` for each of the parent's `+0xC2` words at `+0x90`
(`0x0042FA43`-`0x0042FAA6`). It ends by storing the parent's id at the child's `+0x06` and the parent's `+0x18` at
`+0x2C4`, clearing `+0x290` bit `0x80000` and calling `0x00426E40(parent, child)` (`0x0042FAA8`-`0x0042FAC8`).

On a keyed skeleton, slot 15 is the ride (`0x0042177F`-`0x0042180D`); the named path skips this. It sets the parent's `+0x284` bit `0x8000000` and the child's bits `0x4000000` and `0x8000000`,
and bit `0x40` of `+0x4B7` on both. It runs `0x0041CFC0` on both records' active presentation entries (`0x00422D50`), loads
the child's angles `+0x120` from `0x02064AB0`, and calls `0x00512C80` on the child's `+0x650`. When the child has an
attached child at `+0x2C8`, it re-places that child through `0x0041F010`.

The two tables are 22 entries long, one per slot below `0x16`: string pointers and `s16` keys.

| Slot | Bone name (`0x01EFFFB0`) | Key (`0x01F00060`) |
|---|---|---|
| 0, 2 | `n_buki_r` | `0xBA` |
| 1, 3 | `n_buki_l` | `0xB3` |
| 4 | `j_sebo_b` | `0x01` |
| 5 | `j_kosi` | `0x1B` |
| 6-11 | `j_asi_a_l` | `0x16` |
| 12, 13 | `j_kao` | `0x03` |
| 14 | `__not att` | no key (−1) |
| 15 | `n_hara` | `0x1E` |
| 16 | `model` | `0x1D` |
| 17 | `j_kaochild_s` | `0x02` |
| 18 | `j_blade` | `0x65E` |
| 19 | `n_grip` | `0x656` |
| 20 | `child_e` | no key (−1) |
| 21 | `automax` | `0x1D` |

The point ids `0x100` and up name bones directly. For `0x00422310` and `0x00422380`:

| Point id | Name | Key |
|---|---|---|
| `0x100` | `n_hara` | `0x1E` |
| `0x101` | `model` | `0x1D` |
| `0x109` | `__naiyo__` | `0x1D00` |
| `0x200` | `j_blade` | `0x65E` |
| `0x201` | `n_grip` | `0x656` |
| `0x1000` | `j_kao` | `0x03` |
| any other id of `0x100` or more | `__naiyo__` (`0x00D12428`) | no key (`0xFFFF`) |

So a weapon's blade and grip are the bones keyed `0x65E` and `0x656`, named `j_blade` and `n_grip`. A rider sits on
`n_hara`, key `0x1E`, unless the mount's model has its own bone for special id 15.

### The dirty words

Requests reach a record as bits in two dwords, `+0x290` and `+0x294`. `0x00427DE0(flag)` services them
in five walks of the active list, in fixed order, skipping records with `+0x284` bit `0x40000000`:

1. `+0x290` bits `0x20000000`, `0x40000000`, `0x4`, `0x8`, `0x2000000`, then one of `0x80000`, `0x40000` or `0x100000`, then `0x800000`, `0x1000000`, `0x1000`, `0x400000`, and `+0x294` bit `0x4000000`;
2. `+0x290` bits `0x200`, `0x400`, `0x20000`, `0x800`;
3. `+0x290` bits `0x4000000`, `0x10000000`, `0x80000000` and `0x200`, and `+0x294` bits under mask `0xDFFDFF`, some of them in
   else-if chains;
4. `+0x290` bits `0x10`, `0x20`, `0x40`, `0x200000`, `0x8000000`, `0x2000`, `0x4000`, `0x8000`, `0x10000` and `+0x294` bits `0x1000000`, `0x8000000`;
5. a record with `+0x290` bit `0x2` clear gets `+0x284` bit `0x40000000` cleared and, when `flag` is set, `+0x304`
   bit `0x4000` cleared and `+0x120`..`+0x128` copied to `+0x250`..`+0x258`; one with bit `0x2` set runs
   `0x0042F4C0` again when bit `0x100000` is set.

Most handlers clear their bit after the call; some leave it for a later frame.

Sixteen of the tested bits have no setter, so their tests fail on every record: no instruction in the executable
sets `+0x290` bits `0x4`, `0x20`, `0x40000`, `0x1000000` or `0x80000000`, or `+0x294` bits `0x1`, `0x2`, `0x10`,
`0x40`, `0x400`, `0x800`, `0x4000`, `0x20000`, `0x40000`, `0x80000` or `0x100000`.

There are 313 stores whose operand lies at `+0x290` to `+0x297` and 5 wider stores from `+0x28C`:
they set other bits or write other structures, and `0x0041F730` zeroes each record when it is built. The one setter
of `+0x294` bit `0x2000` is `0x004278D0` (`or 0x2000`). `0x002EB4A0` jumps to it when the record's `+0x284` is not 0;
the `motiontrigger` script verb reaches it that way, through its result callback `0x00343A20`, and so do
`0x003057D0`, `0x0030BC40` and `0x00325260`.

With `flag` set, work
on a record also raises `+0x294` bit `0x2000000` on the top of its parent chain, and `0x00427BD0` then composes
that root's model transform (`0x00420A40`), except while the root's `+0x284` bit `0x200` is set, when `0x00420A40`
composes nothing (`0x00420A5F`-`0x00420A6F`) and the bit is consumed all the same. `0x00426090` calls `0x00427DE0(0)` inside each simulation step
(from `0x003323D0`); `0x0042ED60` calls it with 1 at the end of the frame. Each bit's test site, handler
and setters are in
[the dirty-bit table](character-render-records-dirty-bits.tsv).

`0x00427BD0` takes only active records without a parent (`+0x06` -1) that have `+0x294` bit `0x2000000`
(`0x00427C00`-`0x00427C11`). It clears the bit and calls `0x00420A40(record, 0)` (which returns at once while `+0x284`
bit `0x200` is set, `0x00420A6F`), then `0x00373030` with the record's
skeleton entry and `record + 0x180` when that entry exists, and then `0x00428E70(record)` (`0x00427C13`-`0x00427C61`).

`0x00426090` points the bone scratch list at `[0x01FD4A78]` (`0x00370DF0`), stores the tail's `+0x2C` (see the system
tail), copies `[0x022C6F28]` into `0x02EBB740` with 0 in `0x02EBB748`, and calls the bare `ret` `0x0016D6A0`,
`0x00427DE0(0)` and `0x0042F030` (`0x00426094`-`0x004260EE`). It then walks the hierarchy with
`0x00425FB0(0x0042C410, 0x0042C8F0, records)`, points the list back (`0x00370DE0`), runs `0x003B5890` and `0x003AF460`, and
ends with a tail jump to `0x0017E7D0` (`0x004260F3`-`0x00426120`).

### Columns of character-render-records-dirty-bits.tsv

One row per bit test in `0x00427DE0`, 57 rows; `pass` is the walk (1 to 5) and `bit` the bit's value in the
dword `word` (`0x1` to `0x80000000`).

| Column | Holds |
|---|---|
| `clear_kind` | who clears the bit: `processor` when `0x00427DE0` clears it itself after the handler returns (40 rows); `handler` when the handler clears it in its own body (11 rows); `inline` when `0x00427DE0` does the work in its own body with no handler call (2 rows); `consume` when there is no handler (`handlers` is `-`) and `0x00427DE0` only clears the bit with `btr` (2 rows); `kept` on the pass-5 row for bit `0x100000`, where the handler `0x0042F4C0` runs again and leaves the bit set; `n/a` on the last row, bit `0x2000000` of `+0x294`, which `0x00427DE0` sets rather than tests |
| `clear_site` | the address of the instruction that clears the bit: an `and` of the word with the bit's inverse mask, inside `0x00427DE0` for `processor` and `inline` rows and inside the handler for `handler` rows; for `consume` rows the store of the `btr` result, with the `btr` address in brackets when it differs; `self` when the handler clears it at more than one place; `consumed by 0x00427BD0` on the last row; `-` on the two pass-5 rows, which clear nothing |
| `set_by` | the functions that set the bit, each followed by the instruction that does it (`or` with the bit's value, or `bts` and a store) and, after `<-`, the functions that call that setter; a group writer clears other bits of the same word in the same instruction, listed in brackets; 16 rows state that no instruction in the executable sets the bit, with the code it rests on (every store at `+0x290` to `+0x297`, the wider stores from `+0x28C`, and the constructor `0x0041F730`, which zeroes the record) and, on some rows, the code that clears the bit; the row for `+0x294` bit `0x2000` names its one setter, `0x004278D0`, which `0x002EB4A0` jumps to when the record's `+0x284` is not 0 (`0x002EB4DA`), and the callers of `0x002EB4A0` |
| `rebuilds` | what the handler or inline block does to the record: the functions it calls, the fields it copies or writes, and the bits it re-arms, with the instruction addresses |

### The system tail

The `0x130` bytes after the records, at `0x022C6F28 + 0x48800`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` |  | active list head (-1 empty) |
| `+0x04` | `i32` |  | active list tail |
| `+0x08` | `i32` |  | next-free cursor |
| `+0x0C` | `i32` |  | live count (the allocator refuses at 160) |
| `+0x10` | `i32` |  | pending list head |
| `+0x14` | `i32` |  | pending list tail |
| `+0x18` | `u32` |  | flags: bit `0x1` distance cull on, bit `0x4` set with bit `0x1` at start-up, bit `0x10` viewer-inside fade on, bit `0x20` active list changed |
| `+0x1C` | `f32` |  | distance at which the distance fade starts (34.0) |
| `+0x24` | `f32` |  | distance fade range (4.0) |
| `+0x28` | `f32` |  | 1/6, copied to each promoted record's `+0x414` |
| `+0x2C` | `u16` |  | reference record for the distance fade, `0xFFFF` for no record |
| `+0x30` | `u32` |  | the render root, encoded (`0x00426480`) |
| `+0x42` | `u8` |  | 1: the per-record shadow walk `0x00426420` runs |
| `+0x43` | `u8` |  | 0: same walk, must be 0 |

`0x004269A0` writes these defaults and `0x0042ED30` puts `+0x18` bits `0x1` and `0x4` and `+0x1C`..`+0x28` back.
`0x00426090` stores `+0x2C` each step from the party-focus actor (`0x003590D0`, `0x002E9B80`), or `0xFFFF` when
`0x003590D0` returns 0 (`0x00426099`-`0x004260C3`). Every access
is in [the tail access table](character-render-records-character-render-system-tail-accesses.tsv).

### Render events

A record plays motion events. Word `+0xCC` is the current event, `+0x60` the previous one, word `+0xCE`
an alternate whose presentation entry is `+0xC8`; the current entry is `+0xC4`. An event word keeps a
kind in the bits under mask `0xF000` and an index in the bits under mask `0xFFF`.

`0x00424D80(record, resource, source, event, …, selector)` starts an event. A kinded event must pass `0x004235C0(record,
event, selector)`. The stream is the resource's own entry in the render resource bank or, failing that, the model's
`@FMC`, `@FRP` or `@FMN` section (`0x00409FA0`); the entry is admitted by `0x0051BA80`, its id stored in `+0xC4`, the
event in `+0xCC` and the old event in `+0x60`.

`0x004235C0` returns 1 (allow) unless all of these hold:

- the record has a current entry: `+0xC4` is not -1 and `0x0051B9E0`, a jump to `0x0051F240`, finds it in the
  reference container `+0xDA8` of the root that `+0x10` encodes (`0x004235D9`-`0x00423613`);
- after normalising (kind 3 to `0x2036`; kind 4 to `0x2035` or `0x2036` by index; kind 5 to `0x203E`)
  both events are of kind 1 or 2, kind 1 needing `+0x284` bit `0x80000000` set and kind 2 needing bit `0x10000000` clear;
- the pair is not index `0x3D` on both sides;
- selector 0 with a lower priority for the candidate and `0x00424230` returning 0, or selector 2 with a
  lower priority for the candidate. Every other selector allows.

Priorities are signed bytes at `0x01F00410 + (event & 0xFFF)`; the first `0x49` bytes hold values 0 to 4.
`0x00424230` returns 1 without an entry, otherwise bit `0x1000` of the entry's `+0x2C8` (`0x0041C760`).

The two events `0x004235C0` compares are the candidate, its second argument, and the record's current event
`+0xCC` (`0x00423605`). The `0x3D` test reads the index of `+0xCC` before normalising and that of the normalised
candidate (`0x004236F7`-`0x0042370B`), so a current event of kind 3, 4 or 5 with index `0x3D` beside a candidate of
index `0x3D` allows. The priorities compared are those of the normalised indices, as signed bytes
(`0x0042372F`-`0x00423770`).

`0x0041FCA0` returns `+0xCE` when `+0xC8` is valid and `0x004235C0(record, +0xCE, +0xCC)` allows, else
`+0xCC`. Valid means not -1 (`0x0041FCA6`), and both words are returned sign-extended. The call always
allows: its third argument is `0x004235C0`'s selector, and `+0xCC` is also the current event it compares, so the
selectors 0 and 2, the only ones that can refuse, come with a current event of kind 0, which allows
(`0x0041FCB2`-`0x0041FCC1`, `0x0042370D`-`0x00423727`). `0x0041FCA0` therefore returns `+0xCE` whenever `+0xC8` is not -1.

### Posting an event

`0x00427320(record, event)` posts an event. Before choosing a source it refreshes the dword `+0x110`
from the battle view of the record's actor `+0x108` (`0x00420890`: `0x002ED500` with selector `0x80` for
events `0x2005`, `0x2037` and `0x2039` to `0x203C`, `0x100` for the others; for `0x203A` a first query with
`0x800` into a 64-byte result, whose byte `+0x3C` bit `0x10` makes it call `0x003B4930` before the `0x80` query
(`0x004208FC`-`0x00420926`).

`0x00423790(record, event, last)` then decides
whether the event may follow the last posted one, the word `+0x3B4`, with the normalising and priorities of
`0x004235C0` and without its selector rule; a last event without a kind refuses every event, and a
refusal ends the post.

The event's kind picks the source resource `+0x390`:

| Kind | Source |
|---:|---|
| 0 | the registered script motion slot that the bits under mask `0xF00000` (manager slot) and `0xF0000` (slot) name (`0x003DD740`, state 4 only); `0x00423230` then clears bit `0x1000` of the current entry's `+0x2C8` |
| 1, 2 | `+0x430`, or `+0x42C` by the low two bits of `+0x40B` |
| 3, 4 | `+0x430` (kind 3; `0x302F` and `0x3009` as kinds 1 and 2) or `+0x42C` (kind 4) |
| 5 | `+0x42C` while `0x00423170` holds; otherwise the skill-motion cache entry for the actor's model and the index (`0x003DC7D0`, `0x003DCA00`), or `+0x42C` with `+0x3B4` set to `0x203D` when there is no cache entry |

`0x004230A0(record, event)` then refuses kinded events of index `0x37` while the character object's byte `+0xB4` is 0
and `0x39` and `0x3A` while its `+0xAC` is 2, which clears the source. `0x00422FD0(record, resource,
event)`, asked by `0x00423B10`, holds when `+0x284` bit `0x10000` is set and the resource's entry for the
event index (index 0 for kind 5, `0x00408F80`) has bit `0x10000` or `0x20000` of its `+0x04`.

`motionplay_bb(motion, frames)` (`0x00BB`, `0x0034AB50`, through `0x003DD8D0`) and `puppetmotionplay_41f` (`0x041F`,
`0x00347B00`, through `0x003DD980`, for a puppet) post a kind-0 event: a motion id whose top byte is `0x10` to `0x1F`
names slot `top − 0x10` of the script's manager slot.

They act only when the skip byte of the actor's manager is clear (byte `+0x15` of the script context is the
manager index, `0x0034AB8E`; `0x00267310` returns the byte `[0x02099011 + 0x288 × index]`) and that slot is registered,
and pass the event
`((area << 4) | slot) << 16 | (motion & 0xFFFFFF)`, an OR (`0x003DD949`-`0x003DD954`, `0x003DD9E1`-`0x003DD9F4`), with the
frame count to `0x002EB080` or `0x002EB0D0`; the actor form also stores the slot at actor `+0xF5`.

### The skill-motion cache

Kind-5 motions are files read on demand into 16 entries of `0x14` bytes at `0x02B57F70`, with at most
four 32 KiB units in use. `0x003DCBC0`, from the start-up initialiser `0x00266D10`, numbers the entries, empties
the 16-entry size cache at `0x02B580B0` and requests the table file tagged `PCSkill` (kind 9, file 5: `in/common/pc_skillmotion.bin`, or the `ch` copy for
Korean and the two Chinese languages, 544 bytes; its 33 records are on
[area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md)).

`SkillMotionEntry` (`0x14` bytes, offsets from the start of the 0x02B57F70+0x14*i):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | block | the read block, registered with the render system |
| `+0x04` | `i16` | users |  |
| `+0x06` | `u8` | state | 0 free, 1 queued, 2 reading, 3 ready, 4 releasing |
| `+0x07` | `u8` | units | 32 KiB units of the file |
| `+0x08` | `u32` | id | i \| `0x10` \| serial << 4 |
| `+0x0C` | `u32` | model |  |
| `+0x10` | `u16` | motion |  |
| `+0x12` | `u8` | class | weapon class |
| `+0x13` | `u8` | index | i |

- `0x003DCD00(actor, motion, class, file)` returns 0x80000000 while `0x002E80B0(actor)` is non-zero.
  An entry for the model, motion and class in states 1 to 3 gains a user and its id is returned.
  Otherwise the size comes from `0x003DC8D0` (0x80000001 when it fails), rounded up to units, and the
  entry is filed only if the units of entries with users plus the new ones stay within 4.
- Filing takes the first free entry (`0x003DC380`); with no free entry it releases the idle ready entries
  (`0x003DC6A0`) and tries again. A new entry has one user and state 1, and the idle entries are
  released when all held units exceed 4. With `file` 0 the cache stays as it is:
  0x80000002 says the entry exists or could be filed; `0x003DC410` is that test, `0x003DCCF0` the request.
- `0x003DCD00` answers 0 for a null actor or a negative class (`0x003DCD22`-`0x003DCD2E`), for
  a model id `0x002E96B0(actor)` of 0 or less (`0x003DCD51`), when the units would go above 4
  (`0x003DCE38`-`0x003DCE3E`) and when no entry is free after the release (`0x003DCE79`). The
  units are counted only when the dword `0x003DC8D0` writes through its fourth argument is
  0; otherwise the entry is filed with 0 units (`0x003DCE0D`-`0x003DCE22`).
- `0x003DC780(id)` drops a user; an entry of 0 units that reaches no users in state 3 is released at
  once. `0x003DC6A0` releases every ready entry without users: state 4, and `0x10` added to the id.
- `0x003DC4A0`, from `0x002E65A0` in the field frame `0x0022A770`, works only after a change (`0x02B58170`): it unregisters
  and frees every releasing entry's block (`0x0041E490`, `0x00369800`) and frees the entry, then starts
  each queued one (`0x003DC5B0`): a block in arena 6 and a read of the file `0x003DCA30` names, whose
  completion `0x003DC340` sets state 3 and registers the block (`0x0041E580`).
- `0x003DC7D0(actor, index)` finds a ready entry for the actor's model and motion, matching the class
  too when `0x00322710` holds, and `0x003DCA00(id)` returns its block; `0x003DCB90(id)` returns the state.

`debug_registskillmotion` (`0x2079`, `0x0050CE70`) and `debug_disposeskillmotion` (`0x207B`,
`0x0050CFB0`) reach the request and the release; the battle code uses `0x00325A20` (the test), `0x00325B40`
(the request) and `0x00325A00` (the release). `debug_clearskillmotioncache` (`0x20A4`) runs the code at
`0x003DC420`: its handler `0x0050DF50` is a tail jump there. That code empties the size cache and releases the idle
entries.

## Layouts

The record is `0x740` bytes; the array is 160 of them, `0x48800` bytes, then the tail. These fields
are the ones the functions on this page use:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `i16` |  | own index, -1 when free |
| `+0x002` | `i16` |  | previous record in its list |
| `+0x004` | `i16` |  | next record in its list |
| `+0x006` | `i16` |  | parent record, -1 for a root |
| `+0x008` | `i16` |  | first child |
| `+0x00A` | `i16` |  | next sibling |
| `+0x010` | `u64` |  | context (the render root), stored by the initialiser |
| `+0x018` | `i32` |  | skeleton entry index (root `+0xD98`) |
| `+0x01C` | `char[32]` |  | key, "makeid" and one byte |
| `+0x03C` | `char[32]` |  | model name |
| `+0x060` | `i16` |  | previous event |
| `+0x064` | `i16` |  | model instance index (root `+0xDA0`) |
| `+0x0C0` | `u8` |  | shadow kind (mask `0x18`), scripted shadow LOD (bit `0x2`), scripted shadow alpha (bit `0x4`) |
| `+0x0C4` | `i32` |  | current presentation entry id |
| `+0x0C8` | `i32` |  | alternate presentation entry id |
| `+0x0CC` | `i16` |  | current event |
| `+0x0CE` | `i16` |  | alternate event |
| `+0x114` | `u32` |  | shadow entry handle (pool at `0x02B40528`) |
| `+0x118` | `u32` |  | shadow entry handle (pool at `0x02B3F570`) |
| `+0x210` | `f32[4]` |  | colour, 1.0 after a clear |
| `+0x220` | `f32[4]` |  | second colour, 1.0 after a clear |
| `+0x284` | `u32` |  | state flags (bit `0x4000` character-model directory, bit `0x40000000` skipped by the dirty walk) |
| `+0x290` | `u32` |  | dirty word 1 |
| `+0x294` | `u32` |  | dirty word 2 |
| `+0x400` | `void*` |  | the model's @FCP data |
| `+0x408` | `i16` |  | @FCP section index |
| `+0x414` | `f32` |  | 1/6, from the tail at promotion |
| `+0x4C0` | `u8[10][8]` |  | fade channels, 8 bytes each (character-fades.md) |
| `+0x610` | `f32[4]` |  | live heading, speed, accumulator, flags (the coast-down latch) |
| `+0x620` | `f32[4]` |  | cached heading, speed, accumulator, latch word |
| `+0x6B0` | `i32` |  | render-object key |
| `+0x6B8` | `void*` | CharacterRenderObject | (character-render-object.md) |

The access tables beside this page list every instruction found touching each structure. In the record table and
the tail table, a row whose `route` is `seed` is in a function that loaded the record array's pointer at
`0x022C6F28` itself, and a row whose `route` is `argN+0xK<F@S` is in a function a record was passed to:

- [the record](character-render-records-character-render-record-accesses.tsv);
- [the root](character-render-records-render-resource-root-accesses.tsv);
- [a render resource entry](character-render-records-render-resource-entry-accesses.tsv) and
  [the render resource bank](character-render-records-render-resource-entry-bank-accesses.tsv);
- [the instance bank's chunk entries](character-render-records-chunked-slot-bank-entry-accesses.tsv) and
  [slot entries](character-render-records-chunked-slot-entry-accesses.tsv).

The record bytes between the fields the store names, by range; `+0x411` and `+0x5F1` have readers:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x062` | `u8[2]` | span0062 | the two bytes between the previous event +0x60 and the model instance index +0x64 |
| `+0x066` | `u8[2]` | span0066 | the two bytes between the model instance index +0x64 and the resource reference +0x68 |
| `+0x0D4` | `u8[4]` | span00D4 | the four bytes between the byte +0xD3 and the resource reference +0xD8; the walks of the eight-word table +0x90 in 0x0042F4C0, 0x0042F6C0 and 0x0042F880 (count: the word +0xC2, compared at 0x0042F5DC) address it only as word 34 of that table (0x0042F5FD, 0x0042F818, 0x0042FA88) |
| `+0x0EC` | `u8[4]` | span00EC | the four bytes between the signed resource displacement +0xE8 (-1 for no resource) and the resource reference +0xF0 |
| `+0x104` | `u8[4]` | span0104 | the four bytes between the second signed resource displacement +0x100 and the bound source pointer +0x108 |
| `+0x11C` | `u8[4]` | span011C | the four bytes between the tween entry index +0x118 and the rotation's x angle +0x120 |
| `+0x24E` | `u8[2]` | span024E | the two bytes between the word +0x24C and the previous rotation x angle +0x250 |
| `+0x298` | `u8[8]` | span0298 | the eight bytes between the dirty mask +0x294 and the kind selector +0x2A0 |
| `+0x2CC` | `u8[4]` | span02CC | the four bytes between the word +0x2CA and the projected origin +0x2D0 |
| `+0x38C` | `u8[4]` | span038C | the four bytes between the pending colour's blue +0x388 and the dword +0x390 |
| `+0x3F5` | `u8[3]` | span03F5 | the three bytes between the state byte +0x3F4 and the word +0x3F8 |
| `+0x411` | `i8` | randomChoice | the random choice of the presentation-entry selector kind 0x01: 0x00422420 draws 0 to 4 with 0x003A6E60(5) into it when the counter +0x40E is 0, `+0x411 = 0x003A6E60(5)` (0x0042243C-0x00422451), and, at 11 times [0x01DFE0B4] (`+0x40E == 11 × [0x01DFE0B4]`, 0x0042247A-0x00422484) with bit 0x4 from 0x0041F2F0(record, 0x20), adds 5, `+0x411 += 5` (0x004224A1); it returns the value as the choice (0x00422464, 0x004224AE) |
| `+0x458` | `u8[40]` | span0458 | the 40 bytes between the stop-frame counter +0x457 and the dword band +0x480-+0x48C |
| `+0x490` | `u8[12]` | span0490 | the twelve bytes between the dword band +0x480-+0x48C and the level-of-detail view scale +0x49C (reset to 1.0) |
| `+0x57C` | `u8[4]` | span057C | the four bytes after member +0x28 of the embedded tween object at +0x550, before the parameter tag +0x580 |
| `+0x5CC` | `u8[4]` | span05CC | the four bytes after the parameter block +0x580-+0x5C8, before the 16-byte block +0x5D0 |
| `+0x5F1` | `u8[3]` | span05F1 | bytes 1 to 3 of the record's sound emitter +0x5F0; the low four bits of byte +0x5F1 keep the emitter's last random variation: 0x0046C250, which 0x0046CC70 calls with the emitter (0x0046CD9A-0x0046CD9D), draws 0x003A6E60(3), steps it down (to 2 below 0) when it equals the kept value, and stores it back (0x0046C2F6-0x0046C323, 0x0046C337-0x0046C360) |
| `+0x5FC` | `u8[4]` | span05FC | bytes +0x0C to +0x0F of the sound emitter +0x5F0, between its dword +0x08 (+0x5F8) and its pointer +0x10 (+0x600) |
| `+0x60E` | `u8[2]` | span060E | the two bytes between the emitter's word +0x60C and the live heading +0x610 |
| `+0x61E` | `u8[2]` | span061E | the upper two bytes of the flags lane +0x61C of the live block +0x610-+0x61F (heading, speed, accumulator, flags); 0x00424080 copies the whole block to the cached block +0x620 (0x00424182-0x00424185) |
| `+0x62E` | `u8[2]` | span062E | the upper two bytes of the latch-word lane +0x62C of the cached block +0x620-+0x62F; written by 0x00424080's 16-byte copy from the live block (0x00424185) |
| `+0x66E` | `u8[2]` | span066E | the two bytes between the flag byte +0x66D and the first auxiliary transform +0x670 |
| `+0x6A1` | `u8[3]` | span06A1 | the three bytes between the state byte +0x6A0 and the phase dword +0x6A4 |
| `+0x6AC` | `u8[4]` | span06AC | the four bytes between the interpolation counter +0x6A8 and the dword +0x6B0 |
| `+0x6B4` | `u8[4]` | span06B4 | the four bytes between the dword +0x6B0 and the first bound resource pointer +0x6B8 |
| `+0x6CC` | `u8[4]` | span06CC | the four bytes between the add-motion binding state +0x6C8 and the bound resource pointer +0x6D0 |
| `+0x6E4` | `u8[4]` | span06E4 | the four bytes between the dword +0x6E0 and the add-motion binding pair +0x6E8/+0x6F0 |
| `+0x71C` | `u8[4]` | span071C | the four bytes between the dword +0x718 and the bound resource pointer +0x720 |

## State

- The record array, the tail and the four banks live for the whole run; nothing frees them.

- `0x02EBB740` (`ptr`) and `0x02EBB748` (`u32`), both 0 at start (zero-filled tail of `.data`): the simulation step
  `0x00426090` (`0x004260D1`, `0x004260D8`) and the frame end `0x0042ED60` (`0x0042ED6D`, `0x0042ED74`) copy the record array's
  base `[0x022C6F28]` into `0x02EBB740` and store 0 in `0x02EBB748` before their dirty-word walks `0x00427DE0`. No other
  RIP-relative, image-base-relative or address-forming reference names either word.

## Modding notes

- The pool size is the allocation size `0x48930` in `0x003325D0`; the tail is addressed at fixed offsets
  from `0x022C6F28` (`+0x48800` and on) in every consumer, so a larger pool means moving all of them.
- A record is not drawn the frame it is allocated; it is promoted at the end of the frame.
- A record's key byte is the cursor at allocation, which is the record's own index, so the key is not
  a model name; look records up by `+0x3C` instead.
- The event priority table at `0x01F00410` is indexed by the event's low twelve bits with no bound.
  From byte `0x50` on the table holds other data (`0x10`, `0xFF`, `0x80`), so an event index of `0x50` or
  more reads priorities such as -1 or -128.

## Related

- [Skeleton entries and bones](skeleton-entries-and-bones.md): the skeleton entries, bones, bone points and ties.
- [Presentation entries](presentation-entries.md): the reference container and the per-entry update.
- [CharacterRenderObject](character-render-object.md): the draw object a record owns.
- [Character fades](character-fades.md): the fade channels at `+0x4C0` and the coast-down latch.
- [Character lighting and shadows](character-lighting-and-shadows.md): the two shadow pools.
- [Authored presentation commands](authored-presentation-commands.md): the command handlers.
- [Frame update order](../Engine-Core/frame-update-order.md): where `0x003323D0` and `0x00332660` run.
- [Global state accessors](../Engine-Core/global-state-accessors.md): the encoded pointers
  `0x0020E600` / `0x0020E620`.
- [Resource ownership and disposal](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md):
  `0x003AB7F0`, which resolves a container's table.
