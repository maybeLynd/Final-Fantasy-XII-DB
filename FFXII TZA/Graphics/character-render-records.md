---
title: "Character render records: the record array, the pool lifecycle, render events and the presentation entries"
kind: "system"
category: "Graphics"
summary: "The per-actor render record: the 160-record array and its system tail, how a record is allocated, promoted, retired and cleared, the two dirty words and the per-frame walk that services them, the render-event selection and the presentation-entry reference container, how an entry sets up and switches its tracks, and the render resource root with the chunked banks the records point into."
addresses: ["003325D0", "022C6F28", "022C6F20", "022C6F30", "0041E3A0", "0041E550", "004269A0", "00426480", "0042FB80", "004279B0", "004278E0", "0041F730", "00420480", "00428710", "00427C90", "00429140", "004200A0", "00426EC0", "0042ED60", "00332660", "003323D0", "00426090", "00427DE0", "00427BD0", "00426420", "0051F9F0", "0051FBB0", "0051F6B0", "002ED570", "00409FE0", "0046E4D0", "004780C0", "0051F240", "0051F080", "0051F410", "0051F190", "0051BA40", "0051BA80", "0051B9F0", "0051B970", "00424D80", "004235C0", "0041FCA0", "00424230", "01F00410", "0041CD30", "0041CFC0", "0041C9A0", "00417920", "00417110"]
---

# Character render records: the record array, the pool lifecycle, render events and the presentation entries

## What the player sees

Every character model on screen, from the party to an NPC, a monster, a summon or a weapon attached to
a hand, is drawn from one render record. There are 160 of them, allocated once at start-up; a request
for a record past the 160th is refused. The record is where a character's look is kept between frames:
which motion event it is playing, how faded it is, its shadows and its colour. When a scene adds a
character, its record waits one update on a pending list before it is drawn.

## How it works

### The render resource root

`022C6F20` holds the pointer to the render resource root, which is the static block at `022C6F30`
(`003323D0` and `00332660` store `&022C6F30` there each time they run). `003325D0` runs once: it stores its
argument as the root, allocates the record array (`0036A100(0x48930)`, pointer at `022C6F28`), clears
the root's four bank pointers (`0041E550`), builds them (`0041E3A0`), initialises the record system
(`004269A0`) and stores the root's encoded address in the system tail (`00426480`; its first argument,
`0xA0`, is never read).

`0041E3A0(root, 10, 10, 5, 5, 0x13, 0x2A00, 0x16000)` points each bank at storage inside the root and
initialises it. It forwards only three of its counts; the reference container always takes 64 nodes.

| Root field | Points at | What it holds | Initialiser |
|---|---|---|---|
| `+0xD90` | root `+0x000` | resource entries, `0x50` bytes, 10 chunks of 32 | `00409F10` → `0051F9F0(bank, 0x50, 5, 10, 02B62E40, 02B62F80)` |
| `+0xD98` | root `+0x060` | skeleton entries, `0xC0` bytes, 5 chunks of 32 | `0046E250` → `0051F9F0(bank, 0xC0, 5, 5, 02CA61B0, 02CA6250)` |
| `+0xDA0` | root `+0x0F0` | render model instances, `0x260` bytes, 5 chunks of 32 | `00477EE0` → `0051F9F0(bank, 0x260, 5, 5, 02CA74A0, 02CA7540)` |
| `+0xDA8` | root `+0x160` | presentation-entry references, 64 nodes of `0x30` at root `+0x190` | `0051B9D0` → `0051F170(container, 0x40, root + 0x190)` |

`0041E500(root)` refreshes all four after their storage moves: the resource-entry bank through
`00409F70` (with the byte `02B62E10` held at 1), the skeleton bank through `0046E3E0`, the reference
container through `0051B9F0` and the instance bank through `00478030`. `0041E340`, which `003323D0`
runs after the record update, updates the reference container (`0051B970`) and then the skeleton
bank (`0046E0F0`).

### The chunked banks

The first three banks share one generic container, `0x60` bytes, built by `0051F9F0(bank, element
size, shift, chunk count, chunk table, slot table)`. With shift 5 a chunk holds 32 elements. The
initialiser allocates `chunks << shift` elements in one block, stores each chunk's encoded base, and
claims chunk 0 at once (`0051F6B0`).

- `0051FBB0` takes a slot: it refuses when the used count `+0x58` has reached the capacity `+0x54`,
  finds a chunk with a free slot (`0051F7A0`, claiming a new chunk when needed), scans that chunk for a
  slot whose first dword is -1, appends it to the active list (head `+0x40`, tail `+0x44`), and keeps
  the high-water mark in the word `+0x26`.
- `002ED570(bank, index)` returns the element: chunk `index >> shift`, offset `(index & mask) × size`,
  or null for a free slot. `0051FF30` and `00520010` walk the active list with a callback.
- Each bank has its own acquire: `00409FE0` for resource entries (it returns an existing entry for the
  same resource, found by `0051FE30`, before taking a slot), `0046E4D0` for skeleton entries and
  `004780C0` for model instances.

A record reaches the banks by index: `+0x18` selects its skeleton entry (`00427BD0`, `00421FF0`), `+0x64`
its model instance (`003E55B0`), `+0x408` its `@FCP` section in the resource-entry bank, and `+0xC4` /
`+0xC8` its presentation entries. Skeleton entry `+0x84` is the bone array, `0x290` bytes per bone with
the bone matrix at `+0x80` (`00370F60`); entry `+0xA8` is the owning record's index.

### Allocation

`0042FB80` is the only caller of the allocator. It refuses when the live count is 160, builds the
record's key as the literal `makeid` (`00D12474`) followed by one raw byte, the next-free cursor, and
calls `004279B0(key, name, …)` with the 32-byte name of the current model container (`00409090` on
`003AB7F0()`). It returns the new record's index, or -1.

`004279B0` searches the active list (skipping records with `+0x290` bit 1) and the pending list by key
(`004278E0`), refuses on a match or a full pool, and then:

1. clears the record at the cursor (`0041F730`);
2. appends it to the pending list (tail `+0x10` / `+0x14`, links at record `+0x02` / `+0x04`);
3. writes the record's own index into `+0x00`;
4. runs the initialiser `00420480`;
5. sets `+0x290` bit 0 and increments the live count;
6. advances the cursor to the next record whose `+0x284` is 0, wrapping at 160.

The initialiser ORs `0x2010F9` into `+0x284`, copies the key to `+0x1C` and the model name to `+0x3C`,
sets `+0x284` bit 14 for a name starting `c`, `m`, `n` or `s`, stores the context at `+0x10`, finds the
model's `@FCP` and `@FOR` sections through the resource-entry bank, and picks a per-model float at
`+0x734` from the name (2.0 for `s0011`, for example; 1.0 for a name outside `s`, `m` and `n`).

### Promotion, retirement and clearing

`0042ED60` runs once per frame, from `00332660` at the end of the field frame
([frame update order](../Engine-Core/frame-update-order.md)):

1. it clears tail flag bit 5, runs the active sweep `00427C90` and the promoter `00428710`;
2. when either set bit 5 again, it refreshes the root (`0041E500`), re-binds every active record
   (`0042DA30`) and calls `003697C0(6)`;
3. it runs the dirty-word walk `00427DE0(1)` and the transform commit `00427BD0`.

The promoter takes every pending record in order: it binds the model resources (`0041FCF0`), stamps
`+0x414` from tail `+0x28`, takes a shadow entry into `+0x114` when `003E68E0` allows it
([character lighting and shadows](character-lighting-and-shadows.md)), runs `0042C410` with tail bit 0
held clear, clears `+0x290` bit 0 and moves the record to the end of the active list.

Removal is in two steps. `00429140(record)` is the request:

| Record state | What `00429140` does |
|---|---|
| null | nothing, returns 0 |
| `+0x284` bit 2 set | marks it: `+0x290` bit 1, `+0x2AE` bit 0, clears `+0x108`..`+0x113`, swaps `+0x284` bit 2 for bit 30; clears bit 1 of its presentation entry's `+0x0C` and bit 2 of its skeleton entry |
| bit 2 clear, `+0x290` bit 0 set (still pending) | unlinks it from the pending list, decrements the live count and clears it (`0041F730`) |
| otherwise | nothing |

The active sweep `00427C90` then retires every active record with `+0x290` bit 1: it unlinks it,
decrements the count (resetting the cursor to 0 at a count of 0), runs `0042F4C0`, detaches every
child (`00426EC0`), frees the two shadow entries (`003B6000`, `003AFBE0`) and tears the record down
(`004200A0`, which frees the record's buffers and its CharacterRenderObject, then clears the record).

The clear `0041F730` zeroes all `0x740` bytes and writes the defaults: word `+0x00` = -1, links -1,
fade channels at 1.0 (`003E5D00` for channels 0 to 9), colours `+0x210` and `+0x220` at 1.0.

### Parents and children

A record can be attached to another: word `+0x06` is the parent index, `+0x08` the first child and
`+0x0A` the next sibling. `00426EC0` unlinks a child from its parent's chain. Walks that need the
hierarchy go through `00425FB0(root callback, child callback, …)`, which runs the first callback on
each active record without a parent and the second on its descendants (`0042EF90`).

### The dirty words

Requests reach a record as bits in two dwords, `+0x290` and `+0x294`. `00427DE0(flag)` services them
in five walks of the active list, in fixed order, skipping records with `+0x284` bit 30:

1. `+0x290` bits 29, 30, 2, 3, 25, then one of 19, 18 or 20, then 23, 24, 12, 22, and `+0x294` bit 26;
2. `+0x290` bits 9, 10, 17, 11;
3. `+0x290` bits 26, 28, 31 and 9, and `+0x294` bits 0 to 8, 10 to 20, 22 and 23, some of them in
   else-if chains;
4. `+0x290` bits 4, 5, 6, 21, 27, 13, 14, 15, 16 and `+0x294` bits 24, 27;
5. a record with `+0x290` bit 1 clear gets `+0x284` bit 30 cleared and, when `flag` is set, `+0x304`
   bit 14 cleared and `+0x120`..`+0x128` copied to `+0x250`..`+0x258`; one with bit 1 set runs
   `0042F4C0` again when bit 20 is set.

Most handlers clear their bit after the call; some leave it for a later frame. With `flag` set, work
on a record also raises `+0x294` bit 25 on the top of its parent chain, and `00427BD0` then composes
that root's model transform (`00420A40`). `00426090` calls `00427DE0(0)` inside each simulation step
(from `003323D0`); `0042ED60` calls it with 1 at the end of the frame. Each bit's test site, handler
and setters are in
[the dirty-bit table](character-render-records-dirty-bits.tsv).

### The system tail

The `0x130` bytes after the records, at `022C6F28 + 0x48800`:

```
+0x00  i32  active list head (-1 empty)
+0x04  i32  active list tail
+0x08  i32  next-free cursor
+0x0C  i32  live count (the allocator refuses at 160)
+0x10  i32  pending list head
+0x14  i32  pending list tail
+0x18  u32  flags: bit 0 distance cull on, bit 2 set with bit 0 at start-up,
            bit 4 viewer-inside fade on, bit 5 active list changed
+0x1C  f32  distance at which the distance fade starts (34.0)
+0x24  f32  distance fade range (4.0)
+0x28  f32  1/6, copied to each promoted record's +0x414
+0x2C  u16  reference record for the distance fade, 0xFFFF for none
+0x30  u32  the render root, encoded (00426480)
+0x42  u8   1: the per-record shadow walk 00426420 runs
+0x43  u8   0: same walk, must be 0
```

`004269A0` writes these defaults and `0042ED30` puts `+0x18` bits 0 and 2 and `+0x1C`..`+0x28` back.
`00426090` stores `+0x2C` each step from the party-focus actor (`003590D0`, `002E9B80`). Every access
is in [the tail access table](character-render-records-character-render-system-tail-accesses.tsv).

### Render events

A record plays motion events. Word `+0xCC` is the current event, `+0x60` the previous one, word `+0xCE`
an alternate whose presentation entry is `+0xC8`; the current entry is `+0xC4`. An event word keeps a
kind in bits 12 to 15 and an index in bits 0 to 11.

`00424D80(record, resource, source, event, …, selector)` starts an event. A kinded event must pass
`004235C0(record, event, selector)`. The stream is the resource's own entry in the resource-entry bank
or, failing that, the model's `@FCM`, `@FRP` or `@FMN` section (`00409FA0`); the entry is admitted by
`0051BA80`, its id stored in `+0xC4`, the event in `+0xCC` and the old event in `+0x60`.

`004235C0` returns 1 (allow) unless all of these hold:

- the record has a current entry;
- after normalising (kind 3 to `0x2036`; kind 4 to `0x2035` or `0x2036` by index; kind 5 to `0x203E`)
  both events are of kind 1 or 2, kind 1 needing `+0x284` bit 31 set and kind 2 needing bit 28 clear;
- the pair is not index `0x3D` on both sides;
- selector 0 with a lower priority for the candidate and `00424230` returning 0, or selector 2 with a
  lower priority for the candidate. Every other selector allows.

Priorities are signed bytes at `01F00410 + (event & 0xFFF)`; the first `0x49` bytes hold values 0 to 4.
`00424230` returns 1 without an entry, otherwise bit 12 of the entry's `+0x2C8` (`0041C760`).
`0041FCA0` returns `+0xCE` when `+0xC8` is valid and `004235C0(record, +0xCE, +0xCC)` allows, else
`+0xCC`.

### The presentation-entry reference container

The container at root `+0x160` maps an entry id to a `0x3A0`-byte presentation entry. A node is `0x30`
bytes: `+0x00` state (bit 0 used, bit 1 refresh on lookup), `+0x04` id, `+0x08` / `+0x0C` previous and
next id, `+0x10` source, `+0x18` cached pointer, `+0x20` 32-bit offset.

- `0051F240(container, id)` takes the table by the container's mode (`+0x04` low two bits: 1 direct,
  0 through `003AB7F0`, anything else returns 0), indexes it by `id & 0xFFFF`, and when node bit 1 is
  set rebuilds `+0x18` as the sign-extended 32-bit sum of the resolved source and the offset.
- `0051F080` admits: `0051F410` takes the cursor slot, the id is `slot | 0x10000`, and the node joins
  the active list. The high half never changes, so a reused slot gets the same id.
- `0051BA80(container, id, source, offset, …)` builds a payload on the stack (`0041CB90`, `0041D220`),
  admits a node when `id` is -1, copies the payload in, rebuilds its pointers (`0041CA70`) and writes the
  id into its first dword; if the payload build fails it releases the existing entry and returns -1.
- `0051BA40` releases: it resets the entry (`0041CF00`) and clears the node (`0051F190`) without
  comparing ids.
- `0051B9F0` rebuilds every active node's cached pointer (`0051F620`) and every payload (`0041CA70`).
- `0051B970` updates the entries in three walks: entries with `+0x0C` bit 12 set first (`0051BBE0`),
  then twice the others (`0051BBF0`) with the phase word `02CA83F4` at 1 and then 2.

### How an entry picks its track

An entry plays an authored stream (`+0x368`) made of tracks. It keeps `+0x28` track states of `0xA0`
bytes from `+0x30`; the playing one is `+0x388`. The command handlers are on
[authored presentation commands](authored-presentation-commands.md).

- `0041CD30(entry, state, n)` sets up track `n`: it walks the headers (each header's word `+4` is the
  distance to the next), writes the state defaults, and makes the track primary (entry `+0x18` /
  `+0x20`, state flag bit 0, active) when its kind byte is 1 or the stream has one track. Its start
  cursor `+0x88` is the first command, or the command after a `0xFFFF` marker when the track has one.
- `0041CFC0(entry)` resets: it keeps a snapshot of an interrupted transition (`+0x380`, `+0x384`, entry
  `+0x2E8` bit 2), rewinds every state's cursor to its start, and leaves only the primary active.
- `0041C9A0(entry, n)` hands out a state other than state 0: one already holding track `n` (wiped), else
  the first inactive one.
- Command class `0x01` (`00417920`) switches to a track at once (mode 0), only when the current state's
  word is 2 (mode 1), or when entry `+0x0C` bit 6 allows (mode 2, otherwise it raises bit 7 and waits).
- Command class `0x0B` (`00417110`) asks the selector `[02CA4668]` (entry kind `+0x2DC`) for a choice
  and plays `table[choice] + addend` through class `0x01`. A record with `+0x284` bit 27 and a parent
  reads the parent's cached choice (`+0x4B8`..`+0x4BB` for selector kinds 0, 2, `0x0A`, `0x10`) instead.

## Layouts

The record is `0x740` bytes; the array is 160 of them, `0x48800` bytes, then the tail. These fields
are the ones the functions on this page use:

```
+0x000  i16  own index, -1 when free
+0x002  i16  previous record in its list
+0x004  i16  next record in its list
+0x006  i16  parent record, -1 for a root
+0x008  i16  first child
+0x00A  i16  next sibling
+0x010  u64  context (the render root), stored by the initialiser
+0x018  i32  skeleton entry index (root +0xD98)
+0x01C  char[32]  key, "makeid" and one byte
+0x03C  char[32]  model name
+0x060  i16  previous event
+0x064  i16  model instance index (root +0xDA0)
+0x0C0  u8   shadow kind (bits 3-4), scripted shadow LOD (bit 1), scripted shadow alpha (bit 2)
+0x0C4  i32  current presentation entry id
+0x0C8  i32  alternate presentation entry id
+0x0CC  i16  current event
+0x0CE  i16  alternate event
+0x114  u32  shadow entry handle (pool at 02B40528)
+0x118  u32  shadow entry handle (pool at 02B3F570)
+0x210  f32[4]  colour, 1.0 after a clear
+0x220  f32[4]  second colour, 1.0 after a clear
+0x284  u32  state flags (bit 14 character-model directory, bit 30 skipped by the dirty walk)
+0x290  u32  dirty word 1
+0x294  u32  dirty word 2
+0x400  ptr  the model's @FCP data
+0x408  i16  @FCP section index
+0x414  f32  1/6, from the tail at promotion
+0x4C0  8 B x 10  fade channels (character-fades.md)
+0x610  f32 x 4  live heading, speed, accumulator, flags (the coast-down latch)
+0x620  f32 x 4  cached heading, speed, accumulator, latch word
+0x6B0  i32  render-object key
+0x6B8  ptr  CharacterRenderObject (character-render-object.md)
```

The access tables beside this page list every instruction found touching each structure:

- [the record](character-render-records-character-render-record-accesses.tsv);
- [the root](character-render-records-render-resource-root-accesses.tsv);
- [a resource entry](character-render-records-render-resource-entry-accesses.tsv) and
  [the resource-entry bank](character-render-records-render-resource-entry-bank-accesses.tsv);
- [the skeleton bank](character-render-records-render-stride-c0-bank-accesses.tsv) and
  [a skeleton entry](character-render-records-skeleton-entry-accesses.tsv), the element `002ED570` returns from it;
- [the instance bank's chunk entries](character-render-records-chunked-slot-bank-entry-accesses.tsv) and
  [slot entries](character-render-records-chunked-slot-entry-accesses.tsv);
- [the reference container](character-render-records-presentation-entry-reference-container-accesses.tsv).

## State

- The record array, the tail and the four banks live for the whole run; nothing frees them.
- A presentation-entry id carries no generation: a stale id names whatever now occupies its slot.

## Modding notes

- The pool size is the allocation size `0x48930` in `003325D0`; the tail is addressed at fixed offsets
  from `022C6F28` (`+0x48800` and on) in every consumer, so a larger pool means moving all of them.
- A record is not drawn the frame it is allocated; it is promoted at the end of the frame.
- A record's key byte is the cursor at allocation, which is the record's own index, so the key is not
  a model name; look records up by `+0x3C` instead.
- The event priority table at `01F00410` is indexed by the event's low twelve bits with no bound.
  From byte `0x50` on the table holds other data (`0x10`, `0xFF`, `0x80`), so an event index of `0x50` or
  more reads priorities such as -1 or -128.

## Related

- [CharacterRenderObject](character-render-object.md): the draw object a record owns.
- [Character fades](character-fades.md): the fade channels at `+0x4C0` and the coast-down latch.
- [Character lighting and shadows](character-lighting-and-shadows.md): the two shadow pools.
- [Authored presentation commands](authored-presentation-commands.md): the command handlers.
- [Frame update order](../Engine-Core/frame-update-order.md): where `003323D0` and `00332660` run.
- [Global state accessors](../Engine-Core/global-state-accessors.md): the encoded pointers
  `0020E600` / `0020E620`.
- [Resource ownership and disposal](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md):
  `003AB7F0`, which resolves a container's table.
