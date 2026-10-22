---
title: "Character render records: the record array, the pool lifecycle, render events and the presentation entries"
kind: "system"
category: "Graphics"
addresses: "0x003325D0, 0x022C6F28, 0x022C6F20, 0x022C6F30, 0x0041E3A0, 0x0041E550, 0x004269A0, 0x00426480, 0x0042FB80, 0x004279B0, 0x004278E0, 0x0041F730, 0x00420480, 0x00428710, 0x00427C90, 0x00429140, 0x004200A0, 0x00426EC0, 0x0042ED60, 0x00332660, 0x003323D0, 0x00426090, 0x00427DE0, 0x00427BD0, 0x00426420, 0x0051F9F0, 0x0051FBB0, 0x0051F6B0, 0x002ED570, 0x00409FE0, 0x0046E4D0, 0x004780C0, 0x0051F240, 0x0051F080, 0x0051F410, 0x0051F190, 0x0051BA40, 0x0051BA80, 0x0051B9F0, 0x0051B970, 0x00424D80, 0x004235C0, 0x0041FCA0, 0x00424230, 0x01F00410, 0x0041CD30, 0x0041CFC0, 0x0041C9A0, 0x00417920, 0x00417110"
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

`0x0041E3A0(root, 10, 10, 5, 5, 0x13, 0x2A00, 0x16000)` points each bank at storage inside the root and
initialises it. It forwards only three of its counts; the reference container always takes 64 nodes.

| Root field offset | Points at | What it holds | Initialiser |
|---|---|---|---|
| `+0xD90` | root `+0x000` | resource entries, `0x50` bytes, 10 chunks of 32 | `0x00409F10` → `0x0051F9F0(bank, 0x50, 5, 10, 0x02B62E40, 0x02B62F80)` |
| `+0xD98` | root `+0x060` | skeleton entries, `0xC0` bytes, 5 chunks of 32 | `0x0046E250` → `0x0051F9F0(bank, 0xC0, 5, 5, 0x02CA61B0, 0x02CA6250)` |
| `+0xDA0` | root `+0x0F0` | render model instances, `0x260` bytes, 5 chunks of 32 | `0x00477EE0` → `0x0051F9F0(bank, 0x260, 5, 5, 0x02CA74A0, 0x02CA7540)` |
| `+0xDA8` | root `+0x160` | presentation-entry references, 64 nodes of `0x30` at root `+0x190` | `0x0051B9D0` → `0x0051F170(container, 0x40, root + 0x190)` |

`0x0041E500(root)` refreshes all four after their storage moves: the resource-entry bank through
`0x00409F70` (with the byte `0x02B62E10` held at 1), the skeleton bank through `0x0046E3E0`, the reference
container through `0x0051B9F0` and the instance bank through `0x00478030`. `0x0041E340`, which `0x003323D0`
runs after the record update, updates the reference container (`0x0051B970`) and then the skeleton
bank (`0x0046E0F0`).

### The chunked banks

The first three banks share one generic container, `0x60` bytes, built by `0x0051F9F0(bank, element
size, shift, chunk count, chunk table, slot table)`. With shift 5 a chunk holds 32 elements. The
initialiser allocates `chunks << shift` elements in one block, stores each chunk's encoded base, and
claims chunk 0 at once (`0x0051F6B0`).

- `0x0051FBB0` takes a slot: it refuses when the used count `+0x58` has reached the capacity `+0x54`,
  finds a chunk with a free slot (`0x0051F7A0`, claiming a new chunk when needed), scans that chunk for a
  slot whose first dword is -1, appends it to the active list (head `+0x40`, tail `+0x44`), and keeps
  the high-water mark in the word `+0x26`.
- `0x002ED570(bank, index)` returns the element: chunk `index >> shift`, offset `(index & mask) × size`,
  or null for a free slot. `0x0051FF30` and `0x00520010` walk the active list with a callback.
- Each bank has its own acquire: `0x00409FE0` for resource entries (it returns an existing entry for the
  same resource, found by `0x0051FE30`, before taking a slot), `0x0046E4D0` for skeleton entries and
  `0x004780C0` for model instances.

A record reaches the banks by index: `+0x18` selects its skeleton entry (`0x00427BD0`, `0x00421FF0`), `+0x64`
its model instance (`0x003E55B0`), `+0x408` its `@FCP` section in the resource-entry bank, and `+0xC4` /
`+0xC8` its presentation entries. Skeleton entry `+0x84` is the bone array, `0x290` bytes per bone with
the bone matrix at `+0x80` (`0x00370F60`); entry `+0xA8` is the owning record's index.

### Skeleton entries: links and the update order

A skeleton entry knows its own index (`+0x04`), the index of the skeleton it hangs from (`+0x08`,
−1 for none) with that entry's encoded address at `+0x0C`, and the index of an entry attached to it
(`+0x10`). The bank keeps an update list at `+0x60` in which a parent always comes before its
children; `0x0046E6F0` rebuilds it after every acquire (`0x0046E4D0`), release and attach.

- `0x0046E6F0` first runs `0x0046E950` on every entry, which clears bit 1 of `+0x00` and forgets a
  parent index whose entry is gone (`+0x08` and the word `+0x14` set to −1). It then appends, pass
  after pass, every entry with a skeleton (`+0xA0`) whose parent is none or already listed
  (`0x00537260`), marking it with bit 1.
- `0x0046E2B0(bank, index)` releases an entry: it clears it (`0x003721E0`), frees its slot (`0x0051FCF0`)
  and rebuilds the list. The record teardown `0x0041E860` calls it for the record's `+0x18`.
- `0x0046E590(bank, child, parent, slot)` attaches one skeleton to another through `0x00370180`, which
  stores the parent's index in the child's `+0x08` and, for slot −1, the child's index in the
  parent's `+0x10` (otherwise the slot in the child's word `+0x14`); it then sets `+0x0C` and
  rebuilds the list. Its caller is `0x004218A0`.
- `0x0046E420(bank, index)` refreshes an entry after its resources change: it re-runs `0x003713C0` on
  the entry and its parent, re-encodes `+0x0C`, and re-runs it on the entry at `+0x10` before
  re-linking that entry's bones (`0x00372F60`). Its callers are `0x003E6F90`, `0x0041D220`, `0x0041D820` and `0x004242B0`.
- `0x0046E3E0`, the refresh after the bank's storage moves, re-encodes every `+0x0C` (`0x0046E910`) and
  re-links every `+0x10` (`0x0046E8D0`). `0x00372F60(entry, other)` points each listed bone of the entry
  that names a bone of the other at that bone (`+0x278`, `+0x27C`).
- `0x0046E8B0(bank, index)` returns the entry, or null for −1.

### Skeleton bones: the listed bones, lookups and the bone-to-bone tie

A skeleton entry's word `+0x9C` is its skeleton kind, 0 or 2 (an `@FTR` node table, see
[model files](model-files-cm-ca.md)), and `+0xA0` the skeleton resource. The bone array `+0x84` holds
`+0x88` bones of `0x290` bytes; after them come `+0x88` u16 slots whose first `+0x8A` list the bones
built from pool values (node flag bit 8), then the extra slots.

- `0x00373DC0(bone)`, from the skeleton builder `0x00372820`, puts a bone at rest: identity at
  `+0x1F0` and `+0x230` (`0x0046D120`), `(0, 0, 0, 1)` at `+0x1A0` and `+0x1C0`, 1.0 at `+0x1E0` to
  `+0x1EC`, the flags `+0x280` cleared, the links `+0x270` to `+0x276` and `+0x27C` set to −1,
  `+0x278` null, byte `+0x28A` = 3, bits 0 and 1 of `+0x28B` set and bit 2 clear.
- `0x00372280(entry)`, from `0x0041CF00`, `0x00422A30` and `0x00424550`, resets each listed bone: it clears bit 4 of `+0x280` and sets `+0x1A0` and `+0x1C0` back to `(0, 0, 0, 1)`.
- `0x00372510(entry)`, from `0x00424D80`, fills the extra slots with `0x7FFF`, as many as the model's
  `@FTR` header word `+0x38` gives, and clears bit 12 of the entry's `+0x00`. `0x00371330(entry, i)` returns
  extra slot `i` of a kind-2 skeleton when `i` is below that count, else 0; `0x0053AB50` calls it.
- `0x003725A0(entry, bone)` holds when the bone is listed. `0x003737C0(entry, key)` returns the first
  node with flag bit 8 whose key (`0x00409250`) matches, and `0x00372760(entry, name)` the record whose
  name at `+0x00` of the `0x4C`-byte kind-0 records matches; both return −1 otherwise.

### Bone points

`0x00421E20(record, point, mode, out)` turns a point id into a matrix. Ids `0x107` and `0x108` stand for
the record's words `+0x2F4` and `+0x2F6`, and `0x300` to `0x3FF` go to `0x003710E0`. Otherwise, with
bit 7 of the skeleton entry's `+0x00` clear, `0x00370E30` finds the bone by the name `0x00422310` gives;
with it set and an id of `0xFF` or more, `0x00370FA0` finds it by the key from `0x00422380`.

Both return null unless the bone is listed. They return the bone matrix (`+0x80`) and write to `out`
that matrix moved to the point `(x, 0, 0, 1)` (`0x0046D0D0`), where x is 0 for mode 0, the node's length
for mode 1 and half of it for mode 2. The length is a value of the bone's `@FTR` node (`0x00373640`,
`0x004092A0`) and 0 for kind 0.

`0x003E5B30(record, n, offset)` supplies the ids `0x300` to `0x3FF`, `n` being the id minus `0x300`. It
returns a bone index and writes an offset `(x, y, z, 1)`:

- for any `n` but `0x0B`, entry `n` of the table of 16-byte entries the record's `@FCP` names at
  its word `+0x0C` (`u16` bone, then the three floats); without that table it returns −1 and a zero
  offset;
- for `0x0B`, when the record's active presentation entry (`0x00422D50`) has its byte `+0x328` set,
  the bone `+0x30` and offset `+0x34` of the block at `+0x30` or `+0x60` of that entry's motion data
  `+0x70` (by bits 0–1 of its `+0x04`), and otherwise bone 0 with the vector `+0x4C` of the rig
  (`0x003E6DA0`).

Two callers take a record's centre point:

- `0x003E4CB0(record, out)`, from the distance fade `0x0042E850` for the reference record, uses the
  first of the `@FCP` bones `+0x3A`, `+0x3C` and `+0x3E` that is set (`0x003710E0`) when the `@FCP`
  version byte is 3 or more, and otherwise point `0x100`, or `0x101` when that fails; without a
  skeleton it writes the identity (`0x0046D110`).
- `0x004221F0(record)` makes the same choice with `+0x3A` alone and returns the matrix; `0x0042E7F0`
  stores it at `+0xF0` of the record's draw object, with the record at `+0xF8` and its index at
  `+0xE0`.

### The motion bone list

Before `0x0041BEE0` binds a motion's bone channels it runs `0x00370BB0`, which lists the skeleton's bones as
12-byte nodes (index, previous, next) in the scratch list at `[0x01EF9438]`, with the head at `+0x00` and
the count at `+0x1804`. Kind 0 lists every record (`0x00370BD0`; with bit 5 of the entry's `+0x00` set
only records whose word `+0x22` is 1 or 7) and kind 2 every node with flag bit 8 (`0x00370CD0`).
`0x00370E00` then claims the node whose key matches each channel, unlinking it (`0x00373540`).

`[0x01EF9438]` normally points at `0x02AD9EC0` (`0x00370DE0`); `0x00426090` and `0x004262E0` point it at
`[0x01FD4A78]` (`0x00370DF0`) for their work and back at the end.

### Tying bones to another skeleton

`0x0046E640(bank, child, parent, slot)` ties a kind-2 skeleton to another (`0x00370390`, which jumps to
`0x00373160`): the child's `+0x08` takes the parent's index, and slot −1 stores the child's index in
the parent's `+0x10` while any other slot goes to the child's word `+0x14`. Every listed child bone
saves its parent link `+0x270` in `+0x28E`. With slot −1, a bone whose node has flag bit 8 and whose
key names a listed bone of the parent is then tied to that bone:

- the parent's bone gets the child bone's address at `+0x278` and its node number at `+0x27C`, so
  motion values written to it also reach the child bone;
- the child bone copies the parent bone's matrices `+0xC0` and `+0x150` (`0x0046D100`) and sets bit 1 of
  `+0x280`;
- when the child bone's parent bone is a root (that bone's saved link is −1), the child bone's
  `+0x270` becomes −1 and `+0x276` takes the parent bone's `+0x270`.

`0x0046E370(bank, child)` undoes it through `0x00370BA0` (kind 2 only) and `0x00373380`: when the parent's
`+0x10` names the child it is set to −1 and every listed parent bone's `+0x278` and `+0x27C` are
cleared; the child's `+0x08` and `+0x14` become −1, its first bone's `+0x1F0` the identity, and each
listed bone clears bit 1 of `+0x280`, takes its parent link back from the node (bits 12 to 23, with
`0xFFF` meaning none) and sets `+0x276` to −1.

`0x00372610(a, b, c, scale, d)`, called by the final-pose composer `0x00373860`, multiplies `a`, `b` and
`c` into `0x02AD9E40` (`0x00217150`), scales the four rows of that matrix by the four floats of `scale`, and
multiplies the result by `d` into `0x02AD9E80`.

### Allocation

`0x0042FB80` is the only caller of the allocator. It refuses when the live count is 160, builds the
record's key as the literal `makeid` (`0x00D12474`) followed by one raw byte, the next-free cursor, and
calls `0x004279B0(key, name, …)` with the 32-byte name of the current model container (`0x00409090` on
`0x003AB7F0()`). It returns the new record's index, or -1.

`0x004279B0` searches the active list (skipping records with `+0x290` bit 1) and the pending list by key
(`0x004278E0`), refuses on a match or a full pool, and then:

1. clears the record at the cursor (`0x0041F730`);
2. appends it to the pending list (tail `+0x10` / `+0x14`, links at record `+0x02` / `+0x04`);
3. writes the record's own index into `+0x00`;
4. runs the initialiser `0x00420480`;
5. sets `+0x290` bit 0 and increments the live count;
6. advances the cursor to the next record whose `+0x284` is 0, wrapping at 160.

The initialiser ORs `0x2010F9` into `+0x284`, copies the key to `+0x1C` and the model name to `+0x3C`,
sets `+0x284` bit 14 for a name starting `c`, `m`, `n` or `s`, stores the context at `+0x10`, finds the
model's `@FCP` and `@FOR` sections through the resource-entry bank, and picks a per-model float at
`+0x734` from the name (2.0 for `s0011`, for example; 1.0 for a name outside `s`, `m` and `n`).

### Promotion, retirement and clearing

`0x0042ED60` runs once per frame, from `0x00332660` at the end of the field frame
([frame update order](../Engine-Core/frame-update-order.md)):

1. it clears tail flag bit 5, runs the active sweep `0x00427C90` and the promoter `0x00428710`;
2. when either set bit 5 again, it refreshes the root (`0x0041E500`), re-binds every active record
   (`0x0042DA30`) and calls `0x003697C0(6)`;
3. it runs the dirty-word walk `0x00427DE0(1)` and the transform commit `0x00427BD0`.

The promoter takes every pending record in order: it binds the model resources (`0x0041FCF0`), stamps
`+0x414` from tail `+0x28`, takes a shadow entry into `+0x114` when `0x003E68E0` allows it
([character lighting and shadows](character-lighting-and-shadows.md)), runs `0x0042C410` with tail bit 0
held clear, clears `+0x290` bit 0 and moves the record to the end of the active list.

Removal is in two steps. `0x00429140(record)` is the request:

| Record state | What `0x00429140` does |
|---|---|
| null | nothing, returns 0 |
| `+0x284` bit 2 set | marks it: `+0x290` bit 1, `+0x2AE` bit 0, clears `+0x108`..`+0x113`, swaps `+0x284` bit 2 for bit 30; clears bit 1 of its presentation entry's `+0x0C` and bit 2 of its skeleton entry |
| bit 2 clear, `+0x290` bit 0 set (still pending) | unlinks it from the pending list, decrements the live count and clears it (`0x0041F730`) |
| otherwise | nothing |

The active sweep `0x00427C90` then retires every active record with `+0x290` bit 1: it unlinks it,
decrements the count (resetting the cursor to 0 at a count of 0), runs `0x0042F4C0`, detaches every
child (`0x00426EC0`), frees the two shadow entries (`0x003B6000`, `0x003AFBE0`) and tears the record down
(`0x004200A0`, which frees the record's buffers and its CharacterRenderObject, then clears the record).

The clear `0x0041F730` zeroes all `0x740` bytes and writes the defaults: word `+0x00` = -1, links -1,
fade channels at 1.0 (`0x003E5D00` for channels 0 to 9), colours `+0x210` and `+0x220` at 1.0.

### Parents and children

A record can be attached to another: word `+0x06` is the parent index, `+0x08` the first child and
`+0x0A` the next sibling. `0x00426EC0` unlinks a child from its parent's chain. Walks that need the
hierarchy go through `0x00425FB0(root callback, child callback, …)`, which runs the first callback on
each active record without a parent and the second on its descendants (`0x0042EF90`).

Many setters broadcast a value the same way: they apply it to the record and its first child, then
hand a small per-record body and an argument block to `0x0042EF90` for the rest of the tree.

Most bodies first ask `0x00426220(record, source)` and skip the record when it answers true: a record other
than the source is skipped when its `+0x284` bit 26 is clear and its word `+0x2F8` is −1; a record
with bit 27 and an event below `0x1000` (`+0xCC`) is skipped when `0x004232D0` returns 0; otherwise a
record whose name `+0x3C` starts with `h` is kept only when its next five characters equal the
source's first five, and any other record is skipped when the source's name starts with `b`.

| Body | Broadcast | What the body does to each record |
|---|---|---|
| `0x0042BDD0` | `0x00425E70` | `0x003E6770(record, arg +0x38)` |
| `0x0042D810` | `0x00428B30` | copies bit 3 of the argument's byte `+0x60` into bit 3 of `+0x4B7` |
| `0x0042D9C0` | `0x00426650` | when `0x00421D70(record, word +0x1C)` finds a bone, stores the record at `+0x20`, the bone at `+0x28` and 1 at `+0x18` of the argument (a search) |
| `0x0042DA00` | `0x00426770` | the same search through `0x00421E20` with the word `+0x08`, dword `+0x0C` and pointer `+0x10`, storing the result at `+0x10` |
| `0x0042DE50` | `0x00429D40` | `0x0041FBF0(record, arg +0x38)`, then `0x00421030` |
| `0x0042DE90` | `0x00426FA0` | sets bit 20 of `+0x284` and clears bit 6 of `+0xC0` |
| `0x0042DEC0` | `0x00429E50` | `0x00422DF0`; with the argument's `+0x6C` set, also bit 17 of the `+0x0C` of the entry `0x00422D50` returns |
| `0x0042DFC0` | `0x00427100` | calls `0x00422EB0`, except on a child whose `+0x2F2` is not 1, whose `+0x2F8` is −1 and whose `+0x284` bit 27 is clear; a record without a parent stores the result, or 0, at the argument's `+0x58` |
| `0x0042E050`, `0x0042E170`, `0x0042E1B0` | `0x0042A180`, `0x0042AA10`, `0x0042AB20` | the float `+0x28` through `0x00425510`, `0x00423A60` or `0x00423AB0` |
| `0x0042E090` | `0x0042A290` | `0x00423570(record, arg +0x24)` |
| `0x0042E130` | `0x0042A890` | below `0x1000` in word `+0x3FA`, `0x0041FC80`; then `0x00423A10` |
| `0x0042E300` | `0x0042AC30` | copies word `+0x20` to `+0x3FA` when `+0x2F2` is non-zero (no filter) |
| `0x0042E320`, `0x0042E350`, `0x0042E4B0` | `0x0042AE00`, `0x0042AF10`, `0x0042A580` | on a record without a parent or whose `+0x2F2` is 1, call the bare `ret` `0x0016D6A0`; `0x0042E4B0` also stores 0 at the argument's `+0x58` for a record without a parent |
| `0x0042E440` | `0x0042A390`, `0x0042B130`, `0x0042B270` | `0x00424010` with the three floats `+0x2C`–`+0x34` |
| `0x0042E4F0` | `0x00428CD0` | `0x00504D20` on the record's model row (`0x003E55B0`) with dword `+0x20` |
| `0x0042E530`, `0x0042E540` | `0x0042B690`, `0x0042B770` | `0x00420D80` or `0x00420E70` with dword `+0x74` (no filter) |
| `0x0042E610`, `0x0042E650` | `0x0042B850`; `0x0042B970`, `0x0042BA90` | `0x00420F50` or `0x00420EA0` with dword `+0x38` |
| `0x0042E750`, `0x0042E7A0` | `0x0042BCB0`, `0x00429020` | set bit 21 of `+0x284` when `+0x38` is non-zero, or bit 12 when it is 1 |

`0x00426500`, from `0x00332440`, is one such walk: `0x00425FB0(0x0042D7A0, 0x0042CF70, records)`.

A record keeps two attached children by id: word `+0x2C8` for the child whose slot byte `+0x6A0`
is below `0x16`, and `+0x2CA` for the child of slot `0x16`. Unless `+0x40B` bit 4 is set, the event
start `0x00424D80` re-places both through `0x0041F010(record, child)`, which `0x004215A0` also calls:

1. it stores a slot below `0x16` at `+0x40C`, and takes the mode from the low two bits of `+0x40B`
   (0 while `+0x284` bit 27 is set) into bits 2–3 of `+0x40B`; modes 2 and 3 go straight to step 6;
2. in mode 0, when the record's `@FCP` section 3 (`0x003E5CD0`) names a bone for the slot (word table
   at its start), it ties the child to that bone with `0x004211B0`, which links the two skeletons
   with `0x0046E640` when the child's skeleton entry has bit 7 of its first byte and sets the child's
   parent word `+0x06`;
3. still in mode 0, it copies the slot's offset (section `+0x240 + 12 × slot`) to the child's
   `+0x130` with 1.0 at `+0x13C`, and stores at `+0x150` the record's three scales (`+0x160`,
   `+0x260` and `+0x26C`) times the slot's scale at section `+0x40 + 12 × slot`;
4. in mode 1, or without a section bone, it ties the child to the record's bone for the child's
   `@FCP` word `+0x36` (`0x003E5AD0`, bone 0 when there is none) and, when the section exists, zeroes
   the offset and the scale;
5. with a section, it writes the slot's value at `+0x1C0 + 4 × slot` to the child's `+0x170`,
   `+0x174` and `+0x178`, and 1.0 at `+0x15C` and `+0x17C`;
6. it stores the child's id at `+0x2C8` or `+0x2CA`.

Small record setters beside them: `0x00420CF0(record, x, y, z)` keeps the angles `+0x120`–`+0x128` at
`+0x250`–`+0x258` and stores the new ones, and `0x00420F20(record, x, y, z)` stores `+0x140`–`+0x148`;
both set the fourth float to 1.0 and clear `+0x284` bit 9. `0x00421010(record, on)` sets or clears
`+0x284` bit 3 and calls `0x00421030`; `0x004209A0` clears bit 27 and sets bit 26. `0x00421CD0` returns the
first of the `@FCP` bones for special ids `0x104` to `0x106` that is set, or 0 (always 0 below
`@FCP` version 3).

`0x00422D90` finds the `@FRM` entry (`0x4D524640`) of the record's container and returns its payload;
`0x00422E40` is `0x00424870(…, 1)`; `0x00424280` wraps an angle in degrees into −180 to 180; `0x0042FCB0`
counts `0x02CA4EDC` up, for `0x002EAD00`.

`0x00424870(record, frames, mode)` starts a transition of the current entry `+0xC4` into its motion.
It runs `0x0041CFC0`, hands the three floats `+0x2B0` to `+0x2B8` to `0x0041D7E0` and sets them to −1,
restarts the entry (`0x0041D110` when its `+0x24` is 1, otherwise `+0x0C` bit `0x2`, `+0x24` = 1 and
`0x0041D790`), sets bit `0x800` of `+0x0C` (and `0x20000` for mode 1), stores `1 / frames` at
`+0x354`, clears bit `0x100` when `+0x344` is −1, and calls `0x00423AB0(record, +0x2BC)`.

With
`+0x284` bit 20 set or 0 frames it instead stops the alternate entry `+0xC8` (`+0x0C` bit `0x2`,
`0x0041D790`) after `0x00426FA0` and returns `0x00424C40(record)`.

`0x00424A40` is the same without `0x0041CFC0` and returns 0 at once when the current entry's `+0x24` is
already 1. The child callback `0x0042DF10`, from `0x00429F70`, uses them on a child record that has no
event of its own for the parent's event (`0x0041E5B0`): `0x00422E40` for a child whose `+0xCC` is below
`0x1000`, otherwise `0x00422E50`, which first stops the child's alternate entry and then calls
`0x00424A40(child, frames, 1)`.

`0x00423510(record, resource)` returns the payload of the resource's `@FRM` (`0x00408F90`, `0x00408F80`)
plus the dword at its `+0x0C`, or 0 when the section is missing or that dword is 0; `0x003E6070`
reads three floats there.

### The dirty words

Requests reach a record as bits in two dwords, `+0x290` and `+0x294`. `0x00427DE0(flag)` services them
in five walks of the active list, in fixed order, skipping records with `+0x284` bit 30:

1. `+0x290` bits 29, 30, 2, 3, 25, then one of 19, 18 or 20, then 23, 24, 12, 22, and `+0x294` bit 26;
2. `+0x290` bits 9, 10, 17, 11;
3. `+0x290` bits 26, 28, 31 and 9, and `+0x294` bits 0 to 8, 10 to 20, 22 and 23, some of them in
   else-if chains;
4. `+0x290` bits 4, 5, 6, 21, 27, 13, 14, 15, 16 and `+0x294` bits 24, 27;
5. a record with `+0x290` bit 1 clear gets `+0x284` bit 30 cleared and, when `flag` is set, `+0x304`
   bit 14 cleared and `+0x120`..`+0x128` copied to `+0x250`..`+0x258`; one with bit 1 set runs
   `0x0042F4C0` again when bit 20 is set.

Most handlers clear their bit after the call; some leave it for a later frame. With `flag` set, work
on a record also raises `+0x294` bit 25 on the top of its parent chain, and `0x00427BD0` then composes
that root's model transform (`0x00420A40`). `0x00426090` calls `0x00427DE0(0)` inside each simulation step
(from `0x003323D0`); `0x0042ED60` calls it with 1 at the end of the frame. Each bit's test site, handler
and setters are in
[the dirty-bit table](character-render-records-dirty-bits.tsv).

### The system tail

The `0x130` bytes after the records, at `0x022C6F28 + 0x48800`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `i32` | active list head (-1 empty) |  |
| `+0x04` | `i32` | active list tail |  |
| `+0x08` | `i32` | next-free cursor |  |
| `+0x0C` | `i32` | live count (the allocator refuses at 160) |  |
| `+0x10` | `i32` | pending list head |  |
| `+0x14` | `i32` | pending list tail |  |
| `+0x18` | `u32` | flags: bit 0 distance cull on, bit 2 set with bit 0 at start-up, | bit 4 viewer-inside fade on, bit 5 active list changed |
| `+0x1C` | `f32` | distance at which the distance fade starts (34.0) |  |
| `+0x24` | `f32` | distance fade range (4.0) |  |
| `+0x28` | `f32` | 1/6, copied to each promoted record's +0x414 |  |
| `+0x2C` | `u16` | reference record for the distance fade, 0xFFFF for none |  |
| `+0x30` | `u32` | the render root, encoded (0x00426480) |  |
| `+0x42` | `u8` | 1: the per-record shadow walk 0x00426420 runs |  |
| `+0x43` | `u8` | 0: same walk, must be 0 |  |

`0x004269A0` writes these defaults and `0x0042ED30` puts `+0x18` bits 0 and 2 and `+0x1C`..`+0x28` back.
`0x00426090` stores `+0x2C` each step from the party-focus actor (`0x003590D0`, `0x002E9B80`). Every access
is in [the tail access table](character-render-records-character-render-system-tail-accesses.tsv).

### Render events

A record plays motion events. Word `+0xCC` is the current event, `+0x60` the previous one, word `+0xCE`
an alternate whose presentation entry is `+0xC8`; the current entry is `+0xC4`. An event word keeps a
kind in bits 12 to 15 and an index in bits 0 to 11.

`0x00424D80(record, resource, source, event, …, selector)` starts an event. A kinded event must pass
`0x004235C0(record, event, selector)`. The stream is the resource's own entry in the resource-entry bank
or, failing that, the model's `@FCM`, `@FRP` or `@FMN` section (`0x00409FA0`); the entry is admitted by
`0x0051BA80`, its id stored in `+0xC4`, the event in `+0xCC` and the old event in `+0x60`.

`0x004235C0` returns 1 (allow) unless all of these hold:

- the record has a current entry;
- after normalising (kind 3 to `0x2036`; kind 4 to `0x2035` or `0x2036` by index; kind 5 to `0x203E`)
  both events are of kind 1 or 2, kind 1 needing `+0x284` bit 31 set and kind 2 needing bit 28 clear;
- the pair is not index `0x3D` on both sides;
- selector 0 with a lower priority for the candidate and `0x00424230` returning 0, or selector 2 with a
  lower priority for the candidate. Every other selector allows.

Priorities are signed bytes at `0x01F00410 + (event & 0xFFF)`; the first `0x49` bytes hold values 0 to 4.
`0x00424230` returns 1 without an entry, otherwise bit 12 of the entry's `+0x2C8` (`0x0041C760`).
`0x0041FCA0` returns `+0xCE` when `+0xC8` is valid and `0x004235C0(record, +0xCE, +0xCC)` allows, else
`+0xCC`.

### Posting an event

`0x00427320(record, event)` posts an event. Before choosing a source it refreshes the dword `+0x110`
from the battle view of the record's actor `+0x108` (`0x00420890`: `0x002ED500` with selector `0x80` for
events `0x2005`, `0x2037` and `0x2039` to `0x203C`, `0x100` for the others; for `0x203A` a first query with
`0x800` whose bit 36 makes it call `0x003B4930`).

`0x00423790(record, event, last)` then decides
whether the event may follow the last posted one, the word `+0x3B4`, with the normalising and priorities of
`0x004235C0` and without its selector rule; a last event without a kind refuses every event, and a
refusal ends the post.

The event's kind picks the source resource `+0x390`:

| Kind | Source |
|---:|---|
| 0 | the registered script motion slot that bits 20–23 (area slot) and 16–19 (slot) name (`0x003DD740`, state 4 only); `0x00423230` then clears bit 12 of the current entry's `+0x2C8` |
| 1, 2 | `+0x430`, or `+0x42C` by the low two bits of `+0x40B` |
| 3, 4 | `+0x430` (kind 3; `0x302F` and `0x3009` as kinds 1 and 2) or `+0x42C` (kind 4) |
| 5 | `+0x42C` while `0x00423170` holds; otherwise the skill-motion cache entry for the actor's model and the index (`0x003DC7D0`, `0x003DCA00`), or `+0x42C` with `+0x3B4` set to `0x203D` when there is none |

`0x004230A0(record, event)` then refuses kinded events of index `0x37` while the character object's byte `+0xB4` is 0
and `0x39` and `0x3A` while its `+0xAC` is 2, which clears the source. `0x00422FD0(record, resource,
event)`, asked by `0x00423B10`, holds when `+0x284` bit 16 is set and the resource's entry for the
event index (index 0 for kind 5, `0x00408F80`) has bit 16 or 17 of its `+0x04`.

`motionplay_bb(motion, frames)` (`0x00BB`, `0x003DD8D0`) and `puppetmotionplay_41f` (`0x041F`,
`0x003DD980`, for a puppet) post a kind-0 event: a motion id whose top byte is `0x10` to `0x1F` names
slot `top − 0x10` of the script's area slot. They act only when that slot is registered and pass the
event `(area << 4 | slot) << 16 | (motion & 0xFFFFFF)` with the frame count to `0x002EB080` or `0x002EB0D0`; the actor
form also stores the slot at actor `+0xF5`.

### The skill-motion cache

Kind-5 motions are files read on demand into 16 entries of `0x14` bytes at `0x02B57F70`, with at most
four 32 KiB units in use. `0x003DCBC0`, from the area initialiser `0x00266D10`, numbers the entries, empties
the 16-entry size cache at `0x02B580B0` and requests the table file tagged `PCSkill` (kind 9, file 5).

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
- Filing takes the first free entry (`0x003DC380`); with none it releases the idle ready entries
  (`0x003DC6A0`) and tries again. A new entry has one user and state 1, and the idle entries are
  released when all held units exceed 4. With `file` 0 the cache stays as it is:
  0x80000002 says the entry exists or could be filed; `0x003DC410` is that test, `0x003DCCF0` the request.
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
(the request) and `0x00325A00` (the release). The code at `0x003DC420`, which no instruction reaches, empties the size cache and releases
the idle entries.

### The presentation-entry reference container

The container at root `+0x160` maps an entry id to a `0x3A0`-byte presentation entry. A node is `0x30`
bytes: `+0x00` state (bit 0 used, bit 1 refresh on lookup), `+0x04` id, `+0x08` / `+0x0C` previous and
next id, `+0x10` source, `+0x18` cached pointer, `+0x20` 32-bit offset.

- `0x0051F240(container, id)` takes the table by the container's mode (`+0x04` low two bits: 1 direct,
  0 through `0x003AB7F0`, anything else returns 0), indexes it by `id & 0xFFFF`, and when node bit 1 is
  set rebuilds `+0x18` as the sign-extended 32-bit sum of the resolved source and the offset.
- `0x0051F080` admits: `0x0051F410` takes the cursor slot, the id is `slot | 0x10000`, and the node joins
  the active list. The high half never changes, so a reused slot gets the same id.

- The container's own list helpers: `0x0051F2F0`, run by the initialiser `0x0051F170`, clears every node
  (state 0, id and links −1, source, pointer and offset 0); `0x0051F380`, run by `0x0051F080`, appends
  an id at the tail (head `+0x1C`, tail `+0x20`); `0x0051F4C0`, run by `0x0051F190`, unlinks one; and
  `0x0051F150`, used by `0x0051BA80`, returns the cursor `+0x18` while the used count `+0x14` is below
  the capacity `+0x10`, else −10.

- `0x0051BA80(container, id, source, offset, …)` builds a payload on the stack (`0x0041CB90`, `0x0041D220`),
  admits a node when `id` is -1, copies the payload in, rebuilds its pointers (`0x0041CA70`) and writes the
  id into its first dword; if the payload build fails it releases the existing entry and returns -1.
- `0x0051BA40` releases: it resets the entry (`0x0041CF00`) and clears the node (`0x0051F190`) without
  comparing ids.
- `0x0051B9F0` rebuilds every active node's cached pointer (`0x0051F620`) and every payload (`0x0041CA70`).
- `0x0051B970` updates the entries in three walks: entries with `+0x0C` bit 12 set first (`0x0051BBE0`),
  then twice the others (`0x0051BBF0`) with the phase word `0x02CA83F4` at 1 and then 2.

### How an entry picks its track

An entry plays an authored stream (`+0x368`) made of tracks. It keeps `+0x28` track states of `0xA0`
bytes from `+0x30`; the playing one is `+0x388`. The command handlers are on
[authored presentation commands](authored-presentation-commands.md).

- `0x0041CD30(entry, state, n)` sets up track `n`: it walks the headers (each header's word `+4` is the
  distance to the next), writes the state defaults, and makes the track primary (entry `+0x18` /
  `+0x20`, state flag bit 0, active) when its kind byte is 1 or the stream has one track. Its start
  cursor `+0x88` is the first command, or the command after a `0xFFFF` marker when the track has one.
- `0x0041CFC0(entry)` resets: it keeps a snapshot of an interrupted transition (`+0x380`, `+0x384`, entry
  `+0x2E8` bit 2), rewinds every state's cursor to its start, and leaves only the primary active.
- `0x0041C9A0(entry, n)` hands out a state other than state 0: one already holding track `n` (wiped), else
  the first inactive one.
- Command class `0x01` (`0x00417920`) switches to a track at once (mode 0), only when the current state's
  word is 2 (mode 1), or when entry `+0x0C` bit 6 allows (mode 2, otherwise it raises bit 7 and waits).
- Command class `0x0B` (`0x00417110`) asks the selector `[0x02CA4668]` (entry kind `+0x2DC`) for a choice
  and plays `table[choice] + addend` through class `0x01`. A record with `+0x284` bit 27 and a parent
  reads the parent's cached choice (`+0x4B8`..`+0x4BB` for selector kinds 0, 2, `0x0A`, `0x10`) instead.

### The choice selectors

`0x004269A0` installs the selector table `0x01F000A0` with `0x0041D6E0`: 48 kinds of `0x10` bytes, a
count and a pointer to a handler list, of which `0x00417110` calls the first handler with the stream.
The authored command `0x00` also ends with kind `0x2F`'s handler. Every kind not listed returns 0
(`0x005C5230`); the handlers read the stream's render record `+0x2E0`:

| Kind | Handler | Choice |
|---|---|---|
| `0x00`, `0x0A`, `0x0B` | `0x004223F0`, `0x00422400`, `0x00422410` | jumps to the locomotion selector `0x004256E0` with 0, 1 or 2 |
| `0x01` | `0x00422420` | a counter in byte `+0x40E`: at 0 it draws a random 0–4 (`0x003A6E60(5)`) into `+0x411`, returns it and starts counting at `[0x01DFE0B4]`; at `11 × [0x01DFE0B4]`, when the query `0x0041F2F0(record, 0x20)` reports bit `0x4`, it adds 5 to `+0x411` and returns that; otherwise it counts up to at most 100 and returns −1 |
| `0x02` | `0x00422500` | the byte `+0x410`, chosen once while it is −1 from the bits of `0x0041F2F0(record, 0x30)`: bit `0x2` counts `+0x40E` up (back to `[0x01DFE0B4]` past three times that) and chooses 0; otherwise 1 with bit `0x4`, else 2, and `+0x40E` is cleared |
| `0x04` | `0x00660570` | −1 |
| `0x10` | `0x004225A0` | counts down `+0x412`, armed while it is −1 with `(rand() % (b - a + 1) + a - 1) x [0x01DFE0B4]` for the stream's bytes `a` = `+0x2DD` and `b` = `+0x2DE` (`0x004225C3`-`0x004225F8`), and chooses 1 when it reaches 0, setting it back to −1 |
| `0x20` | `0x00422630` | 0 when the point from `0x0041F2F0(record, 4)` lies within ±90° of the record's heading (`0x00424370`: `atan2` of x and z in the record's own frame), else 1 |
| `0x21` | `0x004226C0` | with `d` the angle from `0x00424370` times 57.295776: 0 for `-60 <= d <= 60`, else 1 for `d > 0` and 2 for `d <= 0`; plus 3 when `0x003A6E60(2)` is non-zero (`0x004226FF`-`0x00422742`) |
| `0x22` | `0x00422760` | 1 when the vertical angle to the point (`0x00424460`) is negative |
| `0x23` | `0x004227D0` | 0 within ±60°, else 2 or 3 by side |
| `0x24` | `0x00422870` | the quarter the point lies in (0 ahead, 1 at 45°–135°, 2 at −45° to −135°, 3 behind) in record byte `+0x2AF`, plus 4 on a random half |
| `0x25` | `0x00422940` | from the angle to the record that the look controller's source names (`0x003E2CD0`): 0 between −90° and 0°, 1 at −90° or less, 2 above 90°, 3 between 0° and 90°; 0 without a source |
| `0x2F` | `0x00422A10` | clears the word `+0x456` and sets byte `+0x2AF` to −1, returning −1 |

`0x00424460(matrix, point)` turns the point into the record's own frame (the matrix at `+0x180`) and
takes `atan2` of its y and z.

### The per-entry update

`0x0041C410(entry)`, from `0x0041D820`, `0x00422EB0` and `0x002EE3E0`, runs an entry only when its record's
`+0x6E0` is 1 in main-loop state 3 (`0x00229EA0`) or 0 in any other state, the entry's `+0x0C` has
bit 1 set and bits 18 and 23 clear, the speed `+0x340` is non-zero, and the status table entry
`0x003E7D10(+0x6A4, 3)` is 0 or the record's `+0xC0` bit 6 is clear. In phase 1 of `0x02CA83F4` it runs
only records with `+0x284` bit 27 and no parent, and in phase 2 it skips those.

- In state word `+0x24` = 1 with `+0x0C` bit 3 and `+0x2C8` bit 12 set, it resets the entry
  (`0x0041CFC0`), clears `+0x2C8` bit 12 and `+0x0C` bit 9 and, for a positive
  `+0x348`, seeks there (`0x0041D820`) and sets `+0x24` to 0 when `+0x348` equals `+0x34C`, else 1.
  With only `+0x2C8` bit 12 set and `+0x348` not −1 it sets `+0x24` to 2.
- With the record's `+0x4B7` bit 4 set it picks the locomotion mode (`0x004255B0`).
- It runs every track state through the walker `0x0041DA90`, then calls `0x0041DD40` on states 1 and up
  until a pass finds none to act on, sets `+0x0C` bit 8, and copies whether `0x003E7D10(+0x6A4, 3)` is
  non-zero into the record's `+0xC0` bit 6.

`0x004255B0` gives controller 5 (`0x003E4890` → `0x0051A920`) a mode from the record's speed `+0x23C`
(taken as 0 while `+0x62C` bit 0 is set or `0x003AEF20(+0x550)` reports): 0 below the walk threshold
`0x003E58B0` (the scale times an `@FCP` value, 0.013333 without one), 2 at or above `+0x420`, and
otherwise 1 when the move direction `+0x244` is within 45° of the facing `+0x124`, 3 from 45° to
135°, 4 from −45° to −135°, and 5 behind.

`0x004256E0(entry, mode)` is the full locomotion selector; motion commands `0x00`, `0x0A` and `0x0B` jump to it with
mode 0, 1 and 2. It reads the entry's render record (`+0x2E0`), takes the speed `+0x23C` as 0 in the same two
cases as `0x004255B0`, and turns headings into degrees wrapped to ±180. The turn is the facing `+0x124` minus
`+0x254`, taken as 0 unless the entry's `+0x31C` top nibble is 2. It picks a state:

| State | When |
|---|---|
| 14 | the actor is asleep: `0x003E7D10(+0x6A4, 4)`, the status-visual record's Sleep dword `+0xD0` |
| 0 | below the walk threshold `0x003E58B0` and the turn is 0 or under `[0x01DFE0BC]` degrees either way |
| 6, 7 | below the walk threshold with a larger turn: 7 when section 9's `+0xA4` (`0x003E5EA0`) is set and the turn times `[0x01DFE0B8]` reaches its `+0xA8` (`0x003E5C90`) in degrees, else 6 |
| 1, 3, 4, 5 | below the run threshold `+0x420`: as `0x004255B0`, 1 within 45° of the facing, 3 from 45° to 135°, 4 from −45° to −135°, 5 behind |
| 2, 10, 9, 11 | at or above `+0x420`: 2, or, when the record has a target record (`0x00512EC0(+0x650)`) and bit `0x20` is set in byte `+0x3C` of the record `0x002ED500(+0x108, 0x1000, out)` fills, the angle to that target (`0x00424370`, `0x00424280`): 2 within 45°, 10 from 45° to 135°, 9 from −45° to −135°, 11 behind |

A model can lack a state. Through `0x004FE2F0` the selector reads one byte per direction from dword `0x30` of the
model's `@FCP` section 9 (ids `0x63070F30`, `0x62070E30`, `0x61070D30`, `0x60070C30`; payload version 7 or later,
else the default 0) and byte 3 of dword `0x2D` (`0x63070B2D`) for state 7, and falls back:

| States | Property | 0 | 1 | 2 or more |
|---|---|---|---|---|
| 1, 2 | `0x63070F30` | 0, and the mode goes to controller 5 (`0x003E4890`) | kept | kept |
| 3, 4 | `0x62070E30` | 0, and the mode goes to controller 5 | 1 | kept |
| 9, 10 | `0x62070E30` | 0 | 2 | kept |
| 5 | `0x61070D30` | 0 | 1 | kept |
| 11 | `0x61070D30` | 2 | 2 | kept |
| 7 | `0x63070B2D` | 0 | 1 | kept |
| 6 | `0x60070C30` | 0 | 1 | 2: 1 when the low six bits of byte `+2` of the actor's resource block (`0x00422D90` of entry `+0x310`, `+0x318`) are below 16; 3 and 5 kept; 4: 1 when those bits are non-zero |

Over the 1,066 shipped models the forward byte is 0 in 626 (343 of them by default), 1 in 129, 2 in 10 and 3 in
301; the sideways and backward bytes are 0, 1 or 2; the turn byte runs 0 to 5 (`fcp_locomotion_props.py`).

The selector then sets the entry's `+0x0C` bit 13. In mode 1, and in mode 2 when `0x002ED530` answers for the
record's actor (`+0x108`), it times the states with two byte counters in 30 fps frames (`[0x01DFE0B4]`, 1 at 30
fps, 2 at 60):

- Walking (1, 3, 4, 5) counts `+0x456` up to 90 frames, starting it at 30 when the previous state `+0x2A0` was 0.
  Below 3 frames it keeps the previous state, so a change of gait waits a tenth of a second; a previous state 15
  becomes 0.
- Running (2, 9 to 11) counts `+0x457` up to 90 frames.
- Standing (0) after at least 30 frames of running becomes 8, the stop; a previous 8 stays while `0x0041C720`
  reports its motion still on byte `+0x95` = 1. States 0, 6 to 8 and above 11 clear both counters.

`0x002ED530(actor)` is 0 without an actor. While the field is live (the cached copy `0x02099DE0` of `0x00265680`,
which `0x00265760` reads) it is `0x0030BEB0`: for a party-side battle unit (stats `+0x05` = 0) with unit flag bit 3
set, the inverse of unit flag bit 23, else 0. Otherwise it is bit 1 of the presentation record's byte `+0x29`
when its bit 0 is set, else 0 (`0x002637D0`).

The state is stored at `+0x2A0`. Mode 0 returns 9 to 11 as 8 to 10 and 14 as 11; mode 1 returns 14 as 12; mode
2 returns every state from 9 one lower, and 8 as 12 and 2 as 11 when `0x002ED530` answers, else 8 as 0. The
return value's low word is the state; its high word is 1 minus a flag that is the record's `+0x418` bit 0, set
for states 0 and 14, and for 6 and 7 whether the turn is positive.

Smaller entry helpers:

- `0x0041D7E0(entry, start, end, limit)` stores the time window `+0x344`, `+0x348`, `+0x34C`, pulling
  `+0x344` down to the limit when both are set and the limit is smaller.
- `0x0041D110(entry)` resets, clears `+0x2C8` bit 12, seeks to `+0x344` when it is set (with `+0x0C`
  bit 28 raised around the call) and sets `+0x24` to 1.
- `0x0041D4D0(entry, on)` sets or clears `+0x0C` bit 12, `+0x33C`, and bit 5 of every state's word
  `+0x96`.
- `0x0041CEC0(entry)` calls bank-A slot `0x0C` (`[0x02CA4470]`) with the actor `+0x2C0` and `+0x31C` and
  sets `+0x0C` bit 9, as the walker does at a motion's end.
- `0x0041C970(entry, n)` returns the state playing track `n` (state `+0x80`); `0x0041C720(entry)` returns
  whether the state playing the entry's track `+0x26` has byte `+0x95` equal to 1; `0x0041C6B0(entry)`
  returns `+0x0C` bit 15. `0x0041C3A0` is an empty function that `0x00423280` calls.

- `0x0041C770(entry)`, for `0x00423380`, returns the dword `+0x0C` of the first state after state 0
  whose byte `+0x95` is 1, or 0.

## Layouts

The record is `0x740` bytes; the array is 160 of them, `0x48800` bytes, then the tail. These fields
are the ones the functions on this page use:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x000` | `i16` | own index, -1 when free |  |
| `+0x002` | `i16` | previous record in its list |  |
| `+0x004` | `i16` | next record in its list |  |
| `+0x006` | `i16` | parent record, -1 for a root |  |
| `+0x008` | `i16` | first child |  |
| `+0x00A` | `i16` | next sibling |  |
| `+0x010` | `u64` | context (the render root), stored by the initialiser |  |
| `+0x018` | `i32` | skeleton entry index (root +0xD98) |  |
| `+0x01C` | `char[32]` | key, "makeid" and one byte |  |
| `+0x03C` | `char[32]` | model name |  |
| `+0x060` | `i16` | previous event |  |
| `+0x064` | `i16` | model instance index (root +0xDA0) |  |
| `+0x0C0` | `u8` | shadow kind (bits 3-4), scripted shadow LOD (bit 1), scripted shadow alpha (bit 2) |  |
| `+0x0C4` | `i32` | current presentation entry id |  |
| `+0x0C8` | `i32` | alternate presentation entry id |  |
| `+0x0CC` | `i16` | current event |  |
| `+0x0CE` | `i16` | alternate event |  |
| `+0x114` | `u32` | shadow entry handle (pool at 0x02B40528) |  |
| `+0x118` | `u32` | shadow entry handle (pool at 0x02B3F570) |  |
| `+0x210` | `f32[4]` | colour, 1.0 after a clear |  |
| `+0x220` | `f32[4]` | second colour, 1.0 after a clear |  |
| `+0x284` | `u32` | state flags (bit 14 character-model directory, bit 30 skipped by the dirty walk) |  |
| `+0x290` | `u32` | dirty word 1 |  |
| `+0x294` | `u32` | dirty word 2 |  |
| `+0x400` | `void*` | the model's @FCP data |  |
| `+0x408` | `i16` | @FCP section index |  |
| `+0x414` | `f32` | 1/6, from the tail at promotion |  |
| `+0x4C0` | `8 B x 10` | fade channels (character-fades.md) |  |
| `+0x610` | `f32 x 4` | live heading, speed, accumulator, flags (the coast-down latch) |  |
| `+0x620` | `f32 x 4` | cached heading, speed, accumulator, latch word |  |
| `+0x6B0` | `i32` | render-object key |  |
| `+0x6B8` | `void*` | CharacterRenderObject (character-render-object.md) |  |

The access tables beside this page list every instruction found touching each structure:

- [the record](character-render-records-character-render-record-accesses.tsv);
- [the root](character-render-records-render-resource-root-accesses.tsv);
- [a resource entry](character-render-records-render-resource-entry-accesses.tsv) and
  [the resource-entry bank](character-render-records-render-resource-entry-bank-accesses.tsv);
- [the skeleton bank](character-render-records-render-stride-c0-bank-accesses.tsv) and
  [a skeleton entry](character-render-records-skeleton-entry-accesses.tsv), the element `0x002ED570` returns from it;
- [the instance bank's chunk entries](character-render-records-chunked-slot-bank-entry-accesses.tsv) and
  [slot entries](character-render-records-chunked-slot-entry-accesses.tsv);
- [the reference container](character-render-records-presentation-entry-reference-container-accesses.tsv).

## State

- The record array, the tail and the four banks live for the whole run; nothing frees them.
- A presentation-entry id carries no generation: a stale id names whatever now occupies its slot.

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

- [CharacterRenderObject](character-render-object.md): the draw object a record owns.
- [Character fades](character-fades.md): the fade channels at `+0x4C0` and the coast-down latch.
- [Character lighting and shadows](character-lighting-and-shadows.md): the two shadow pools.
- [Authored presentation commands](authored-presentation-commands.md): the command handlers.
- [Frame update order](../Engine-Core/frame-update-order.md): where `0x003323D0` and `0x00332660` run.
- [Global state accessors](../Engine-Core/global-state-accessors.md): the encoded pointers
  `0x0020E600` / `0x0020E620`.
- [Resource ownership and disposal](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md):
  `0x003AB7F0`, which resolves a container's table.
