---
title: "Character render records: the record array, the pool lifecycle, render events and the presentation entries"
kind: "system"
category: "Graphics"
addresses: "003325D0, 022C6F28, 022C6F20, 022C6F30, 0041E3A0, 0041E550, 004269A0, 00426480, 0042FB80, 004279B0, 004278E0, 0041F730, 00420480, 00428710, 00427C90, 00429140, 004200A0, 00426EC0, 0042ED60, 00332660, 003323D0, 00426090, 00427DE0, 00427BD0, 00426420, 0051F9F0, 0051FBB0, 0051F6B0, 002ED570, 00409FE0, 0046E4D0, 004780C0, 0051F240, 0051F080, 0051F410, 0051F190, 0051BA40, 0051BA80, 0051B9F0, 0051B970, 00424D80, 004235C0, 0041FCA0, 00424230, 01F00410, 0041CD30, 0041CFC0, 0041C9A0, 00417920, 00417110"
---

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
argument as the root, allocates the record array (`0036A100(48930h)`, pointer at `022C6F28`), clears
the root's four bank pointers (`0041E550`), builds them (`0041E3A0`), initialises the record system
(`004269A0`) and stores the root's encoded address in the system tail (`00426480`; its first argument,
`A0`<sub>h</sub>, is never read).

`0041E3A0(root, 10, 10, 5, 5, 13h, 2A00h, 16000h)` points each bank at storage inside the root and
initialises it. It forwards only three of its counts; the reference container always takes 64 nodes.

| Root field offset | Points at | What it holds | Initialiser |
|---|---|---|---|
| `D90`<sub>h</sub> | root `+000`<sub>h</sub> | resource entries, `50`<sub>h</sub> bytes, 10 chunks of 32 | `00409F10` → `0051F9F0(bank, 50h, 5, 10, 02B62E40, 02B62F80)` |
| `D98`<sub>h</sub> | root `+060`<sub>h</sub> | skeleton entries, `C0`<sub>h</sub> bytes, 5 chunks of 32 | `0046E250` → `0051F9F0(bank, C0h, 5, 5, 02CA61B0, 02CA6250)` |
| `DA0`<sub>h</sub> | root `+0F0`<sub>h</sub> | render model instances, `260`<sub>h</sub> bytes, 5 chunks of 32 | `00477EE0` → `0051F9F0(bank, 260h, 5, 5, 02CA74A0, 02CA7540)` |
| `DA8`<sub>h</sub> | root `+160`<sub>h</sub> | presentation-entry references, 64 nodes of `30`<sub>h</sub> at root `+190`<sub>h</sub> | `0051B9D0` → `0051F170(container, 40h, root + 190h)` |

`0041E500(root)` refreshes all four after their storage moves: the resource-entry bank through
`00409F70` (with the byte `02B62E10` held at 1), the skeleton bank through `0046E3E0`, the reference
container through `0051B9F0` and the instance bank through `00478030`. `0041E340`, which `003323D0`
runs after the record update, updates the reference container (`0051B970`) and then the skeleton
bank (`0046E0F0`).

### The chunked banks

The first three banks share one generic container, `60`<sub>h</sub> bytes, built by `0051F9F0(bank, element
size, shift, chunk count, chunk table, slot table)`. With shift 5 a chunk holds 32 elements. The
initialiser allocates `chunks << shift` elements in one block, stores each chunk's encoded base, and
claims chunk 0 at once (`0051F6B0`).

- `0051FBB0` takes a slot: it refuses when the used count `+58`<sub>h</sub> has reached the capacity `+54`<sub>h</sub>,
  finds a chunk with a free slot (`0051F7A0`, claiming a new chunk when needed), scans that chunk for a
  slot whose first dword is -1, appends it to the active list (head `+40`<sub>h</sub>, tail `+44`<sub>h</sub>), and keeps
  the high-water mark in the word `+26`<sub>h</sub>.
- `002ED570(bank, index)` returns the element: chunk `index >> shift`, offset `(index & mask) × size`,
  or null for a free slot. `0051FF30` and `00520010` walk the active list with a callback.
- Each bank has its own acquire: `00409FE0` for resource entries (it returns an existing entry for the
  same resource, found by `0051FE30`, before taking a slot), `0046E4D0` for skeleton entries and
  `004780C0` for model instances.

A record reaches the banks by index: `+18`<sub>h</sub> selects its skeleton entry (`00427BD0`, `00421FF0`), `+64`<sub>h</sub>
its model instance (`003E55B0`), `+408`<sub>h</sub> its `@FCP` section in the resource-entry bank, and `+C4`<sub>h</sub> /
`+C8`<sub>h</sub> its presentation entries. Skeleton entry `+84`<sub>h</sub> is the bone array, `290`<sub>h</sub> bytes per bone with
the bone matrix at `+80`<sub>h</sub> (`00370F60`); entry `+A8`<sub>h</sub> is the owning record's index.

### Skeleton entries: links and the update order

A skeleton entry knows its own index (`+04`<sub>h</sub>), the index of the skeleton it hangs from (`+08`<sub>h</sub>,
−1 for none) with that entry's encoded address at `+0C`<sub>h</sub>, and the index of an entry attached to it
(`+10`<sub>h</sub>). The bank keeps an update list at `+60`<sub>h</sub> in which a parent always comes before its
children; `0046E6F0` rebuilds it after every acquire (`0046E4D0`), release and attach.

- `0046E6F0` first runs `0046E950` on every entry, which clears bit 1 of `+00`<sub>h</sub> and forgets a
  parent index whose entry is gone (`+08`<sub>h</sub> and the word `+14`<sub>h</sub> set to −1). It then appends, pass
  after pass, every entry with a skeleton (`+A0`<sub>h</sub>) whose parent is none or already listed
  (`00537260`), marking it with bit 1.
- `0046E2B0(bank, index)` releases an entry: it clears it (`003721E0`), frees its slot (`0051FCF0`)
  and rebuilds the list. The record teardown `0041E860` calls it for the record's `+18`<sub>h</sub>.
- `0046E590(bank, child, parent, slot)` attaches one skeleton to another through `00370180`, which
  stores the parent's index in the child's `+08`<sub>h</sub> and, for slot −1, the child's index in the
  parent's `+10`<sub>h</sub> (otherwise the slot in the child's word `+14`<sub>h</sub>); it then sets `+0C`<sub>h</sub> and
  rebuilds the list. Its caller is `004218A0`.
- `0046E420(bank, index)` refreshes an entry after its resources change: it re-runs `003713C0` on
  the entry and its parent, re-encodes `+0C`<sub>h</sub>, and re-runs it on the entry at `+10`<sub>h</sub> before
  re-linking that entry's bones (`00372F60`). Its callers are `003E6F90`, `0041D220`, `0041D820` and `004242B0`.
- `0046E3E0`, the refresh after the bank's storage moves, re-encodes every `+0C`<sub>h</sub> (`0046E910`) and
  re-links every `+10`<sub>h</sub> (`0046E8D0`). `00372F60(entry, other)` points each listed bone of the entry
  that names a bone of the other at that bone (`+278`<sub>h</sub>, `+27C`<sub>h</sub>).
- `0046E8B0(bank, index)` returns the entry, or null for −1.

### Skeleton bones: the listed bones, lookups and the bone-to-bone tie

A skeleton entry's word `+9C`<sub>h</sub> is its skeleton kind, 0 or 2 (an `@FTR` node table, see
[model files](model-files-cm-ca.md)), and `+A0`<sub>h</sub> the skeleton resource. The bone array `+84`<sub>h</sub> holds
`+88`<sub>h</sub> bones of `290`<sub>h</sub> bytes; after them come `+88`<sub>h</sub> u16 slots whose first `+8A`<sub>h</sub> list the bones
built from pool values (node flag bit 8), then the extra slots.

- `00373DC0(bone)`, from the skeleton builder `00372820`, puts a bone at rest: identity at
  `+1F0`<sub>h</sub> and `+230`<sub>h</sub> (`0046D120`), `(0, 0, 0, 1)` at `+1A0`<sub>h</sub> and `+1C0`<sub>h</sub>, 1.0 at `+1E0`<sub>h</sub> to
  `+1EC`<sub>h</sub>, the flags `+280`<sub>h</sub> cleared, the links `+270`<sub>h</sub> to `+276`<sub>h</sub> and `+27C`<sub>h</sub> set to −1,
  `+278`<sub>h</sub> null, byte `+28A`<sub>h</sub> = 3, bits 0 and 1 of `+28B`<sub>h</sub> set and bit 2 clear.
- `00372280(entry)`, from `0041CF00`, `00422A30` and `00424550`, resets each listed bone: it clears bit 4 of `+280`<sub>h</sub> and sets `+1A0`<sub>h</sub> and `+1C0`<sub>h</sub> back to `(0, 0, 0, 1)`.
- `00372510(entry)`, from `00424D80`, fills the extra slots with `7FFF`<sub>h</sub>, as many as the model's
  `@FTR` header word `+38`<sub>h</sub> gives, and clears bit 12 of the entry's `+00`<sub>h</sub>. `00371330(entry, i)` returns
  extra slot `i` of a kind-2 skeleton when `i` is below that count, else 0; `0053AB50` calls it.
- `003725A0(entry, bone)` holds when the bone is listed. `003737C0(entry, key)` returns the first
  node with flag bit 8 whose key (`00409250`) matches, and `00372760(entry, name)` the record whose
  name at `+00`<sub>h</sub> of the `4C`<sub>h</sub>-byte kind-0 records matches; both return −1 otherwise.

### Bone points

`00421E20(record, point, mode, out)` turns a point id into a matrix. Ids `107`<sub>h</sub> and `108`<sub>h</sub> stand for
the record's words `+2F4`<sub>h</sub> and `+2F6`<sub>h</sub>, and `300`<sub>h</sub> to `3FF`<sub>h</sub> go to `003710E0`. Otherwise, with
bit 7 of the skeleton entry's `+00`<sub>h</sub> clear, `00370E30` finds the bone by the name `00422310` gives;
with it set and an id of `FF`<sub>h</sub> or more, `00370FA0` finds it by the key from `00422380`.

Both return null unless the bone is listed. They return the bone matrix (`+80`<sub>h</sub>) and write to `out`
that matrix moved to the point `(x, 0, 0, 1)` (`0046D0D0`), where x is 0 for mode 0, the node's length
for mode 1 and half of it for mode 2. The length is a value of the bone's `@FTR` node (`00373640`,
`004092A0`) and 0 for kind 0.

`003E5B30(record, n, offset)` supplies the ids `300`<sub>h</sub> to `3FF`<sub>h</sub>, `n` being the id minus `300`<sub>h</sub>. It
returns a bone index and writes an offset `(x, y, z, 1)`:

- for any `n` but `0B`<sub>h</sub>, entry `n` of the table of 16-byte entries the record's `@FCP` names at
  its word `+0C`<sub>h</sub> (`u16` bone, then the three floats); without that table it returns −1 and a zero
  offset;
- for `0B`<sub>h</sub>, when the record's active presentation entry (`00422D50`) has its byte `+328`<sub>h</sub> set,
  the bone `+30`<sub>h</sub> and offset `+34`<sub>h</sub> of the block at `+30`<sub>h</sub> or `+60`<sub>h</sub> of that entry's motion data
  `+70`<sub>h</sub> (by bits 0–1 of its `+04`<sub>h</sub>), and otherwise bone 0 with the vector `+4C`<sub>h</sub> of the rig
  (`003E6DA0`).

Two callers take a record's centre point:

- `003E4CB0(record, out)`, from the distance fade `0042E850` for the reference record, uses the
  first of the `@FCP` bones `+3A`<sub>h</sub>, `+3C`<sub>h</sub> and `+3E`<sub>h</sub> that is set (`003710E0`) when the `@FCP`
  version byte is 3 or more, and otherwise point `100`<sub>h</sub>, or `101`<sub>h</sub> when that fails; without a
  skeleton it writes the identity (`0046D110`).
- `004221F0(record)` makes the same choice with `+3A`<sub>h</sub> alone and returns the matrix; `0042E7F0`
  stores it at `+F0`<sub>h</sub> of the record's draw object, with the record at `+F8`<sub>h</sub> and its index at
  `+E0`<sub>h</sub>.

### The motion bone list

Before `0041BEE0` binds a motion's bone channels it runs `00370BB0`, which lists the skeleton's bones as
12-byte nodes (index, previous, next) in the scratch list at `[01EF9438]`, with the head at `+00`<sub>h</sub> and
the count at `+1804`<sub>h</sub>. Kind 0 lists every record (`00370BD0`; with bit 5 of the entry's `+00`<sub>h</sub> set
only records whose word `+22`<sub>h</sub> is 1 or 7) and kind 2 every node with flag bit 8 (`00370CD0`).
`00370E00` then claims the node whose key matches each channel, unlinking it (`00373540`).

`[01EF9438]` normally points at `02AD9EC0` (`00370DE0`); `00426090` and `004262E0` point it at
`[01FD4A78]` (`00370DF0`) for their work and back at the end.

### Tying bones to another skeleton

`0046E640(bank, child, parent, slot)` ties a kind-2 skeleton to another (`00370390`, which jumps to
`00373160`): the child's `+08`<sub>h</sub> takes the parent's index, and slot −1 stores the child's index in
the parent's `+10`<sub>h</sub> while any other slot goes to the child's word `+14`<sub>h</sub>. Every listed child bone
saves its parent link `+270`<sub>h</sub> in `+28E`<sub>h</sub>. With slot −1, a bone whose node has flag bit 8 and whose
key names a listed bone of the parent is then tied to that bone:

- the parent's bone gets the child bone's address at `+278`<sub>h</sub> and its node number at `+27C`<sub>h</sub>, so
  motion values written to it also reach the child bone;
- the child bone copies the parent bone's matrices `+C0`<sub>h</sub> and `+150`<sub>h</sub> (`0046D100`) and sets bit 1 of
  `+280`<sub>h</sub>;
- when the child bone's parent bone is a root (that bone's saved link is −1), the child bone's
  `+270`<sub>h</sub> becomes −1 and `+276`<sub>h</sub> takes the parent bone's `+270`<sub>h</sub>.

`0046E370(bank, child)` undoes it through `00370BA0` (kind 2 only) and `00373380`: when the parent's
`+10`<sub>h</sub> names the child it is set to −1 and every listed parent bone's `+278`<sub>h</sub> and `+27C`<sub>h</sub> are
cleared; the child's `+08`<sub>h</sub> and `+14`<sub>h</sub> become −1, its first bone's `+1F0`<sub>h</sub> the identity, and each
listed bone clears bit 1 of `+280`<sub>h</sub>, takes its parent link back from the node (bits 12 to 23, with
`FFF`<sub>h</sub> meaning none) and sets `+276`<sub>h</sub> to −1.

`00372610(a, b, c, scale, d)`, called by the final-pose composer `00373860`, multiplies `a`, `b` and
`c` into `02AD9E40` (`00217150`), scales the four rows of that matrix by the four floats of `scale`, and
multiplies the result by `d` into `02AD9E80`.

### Allocation

`0042FB80` is the only caller of the allocator. It refuses when the live count is 160, builds the
record's key as the literal `makeid` (`00D12474`) followed by one raw byte, the next-free cursor, and
calls `004279B0(key, name, …)` with the 32-byte name of the current model container (`00409090` on
`003AB7F0()`). It returns the new record's index, or -1.

`004279B0` searches the active list (skipping records with `+290`<sub>h</sub> bit 1) and the pending list by key
(`004278E0`), refuses on a match or a full pool, and then:

1. clears the record at the cursor (`0041F730`);
2. appends it to the pending list (tail `+10`<sub>h</sub> / `+14`<sub>h</sub>, links at record `+02`<sub>h</sub> / `+04`<sub>h</sub>);
3. writes the record's own index into `+00`<sub>h</sub>;
4. runs the initialiser `00420480`;
5. sets `+290`<sub>h</sub> bit 0 and increments the live count;
6. advances the cursor to the next record whose `+284`<sub>h</sub> is 0, wrapping at 160.

The initialiser ORs `2010F9`<sub>h</sub> into `+284`<sub>h</sub>, copies the key to `+1C`<sub>h</sub> and the model name to `+3C`<sub>h</sub>,
sets `+284`<sub>h</sub> bit 14 for a name starting `c`, `m`, `n` or `s`, stores the context at `+10`<sub>h</sub>, finds the
model's `@FCP` and `@FOR` sections through the resource-entry bank, and picks a per-model float at
`+734`<sub>h</sub> from the name (2.0 for `s0011`, for example; 1.0 for a name outside `s`, `m` and `n`).

### Promotion, retirement and clearing

`0042ED60` runs once per frame, from `00332660` at the end of the field frame
([frame update order](../Engine-Core/frame-update-order.md)):

1. it clears tail flag bit 5, runs the active sweep `00427C90` and the promoter `00428710`;
2. when either set bit 5 again, it refreshes the root (`0041E500`), re-binds every active record
   (`0042DA30`) and calls `003697C0(6)`;
3. it runs the dirty-word walk `00427DE0(1)` and the transform commit `00427BD0`.

The promoter takes every pending record in order: it binds the model resources (`0041FCF0`), stamps
`+414`<sub>h</sub> from tail `+28`<sub>h</sub>, takes a shadow entry into `+114`<sub>h</sub> when `003E68E0` allows it
([character lighting and shadows](character-lighting-and-shadows.md)), runs `0042C410` with tail bit 0
held clear, clears `+290`<sub>h</sub> bit 0 and moves the record to the end of the active list.

Removal is in two steps. `00429140(record)` is the request:

| Record state | What `00429140` does |
|---|---|
| null | nothing, returns 0 |
| `+284`<sub>h</sub> bit 2 set | marks it: `+290`<sub>h</sub> bit 1, `+2AE`<sub>h</sub> bit 0, clears `+108`<sub>h</sub>..`+113`<sub>h</sub>, swaps `+284`<sub>h</sub> bit 2 for bit 30; clears bit 1 of its presentation entry's `+0C`<sub>h</sub> and bit 2 of its skeleton entry |
| bit 2 clear, `+290`<sub>h</sub> bit 0 set (still pending) | unlinks it from the pending list, decrements the live count and clears it (`0041F730`) |
| otherwise | nothing |

The active sweep `00427C90` then retires every active record with `+290`<sub>h</sub> bit 1: it unlinks it,
decrements the count (resetting the cursor to 0 at a count of 0), runs `0042F4C0`, detaches every
child (`00426EC0`), frees the two shadow entries (`003B6000`, `003AFBE0`) and tears the record down
(`004200A0`, which frees the record's buffers and its CharacterRenderObject, then clears the record).

The clear `0041F730` zeroes all `740`<sub>h</sub> bytes and writes the defaults: word `+00`<sub>h</sub> = -1, links -1,
fade channels at 1.0 (`003E5D00` for channels 0 to 9), colours `+210`<sub>h</sub> and `+220`<sub>h</sub> at 1.0.

### Parents and children

A record can be attached to another: word `+06`<sub>h</sub> is the parent index, `+08`<sub>h</sub> the first child and
`+0A`<sub>h</sub> the next sibling. `00426EC0` unlinks a child from its parent's chain. Walks that need the
hierarchy go through `00425FB0(root callback, child callback, …)`, which runs the first callback on
each active record without a parent and the second on its descendants (`0042EF90`).

Many setters broadcast a value the same way: they apply it to the record and its first child, then
hand a small per-record body and an argument block to `0042EF90` for the rest of the tree.

Most bodies first ask `00426220(record, source)` and skip the record when it answers true: a record other
than the source is skipped when its `+284`<sub>h</sub> bit 26 is clear and its word `+2F8`<sub>h</sub> is −1; a record
with bit 27 and an event below `1000`<sub>h</sub> (`+CC`<sub>h</sub>) is skipped when `004232D0` returns 0; otherwise a
record whose name `+3C`<sub>h</sub> starts with `h` is kept only when its next five characters equal the
source's first five, and any other record is skipped when the source's name starts with `b`.

| Body | Broadcast | What the body does to each record |
|---|---|---|
| `0042BDD0` | `00425E70` | `003E6770(record, arg +38h)` |
| `0042D810` | `00428B30` | copies bit 3 of the argument's byte `+60`<sub>h</sub> into bit 3 of `+4B7`<sub>h</sub> |
| `0042D9C0` | `00426650` | when `00421D70(record, word +1Ch)` finds a bone, stores the record at `+20`<sub>h</sub>, the bone at `+28`<sub>h</sub> and 1 at `+18`<sub>h</sub> of the argument (a search) |
| `0042DA00` | `00426770` | the same search through `00421E20` with the word `+08`<sub>h</sub>, dword `+0C`<sub>h</sub> and pointer `+10`<sub>h</sub>, storing the result at `+10`<sub>h</sub> |
| `0042DE50` | `00429D40` | `0041FBF0(record, arg +38h)`, then `00421030` |
| `0042DE90` | `00426FA0` | sets bit 20 of `+284`<sub>h</sub> and clears bit 6 of `+C0`<sub>h</sub> |
| `0042DEC0` | `00429E50` | `00422DF0`; with the argument's `+6C`<sub>h</sub> set, also bit 17 of the `+0C`<sub>h</sub> of the entry `00422D50` returns |
| `0042DFC0` | `00427100` | calls `00422EB0`, except on a child whose `+2F2`<sub>h</sub> is not 1, whose `+2F8`<sub>h</sub> is −1 and whose `+284`<sub>h</sub> bit 27 is clear; a record without a parent stores the result, or 0, at the argument's `+58`<sub>h</sub> |
| `0042E050`, `0042E170`, `0042E1B0` | `0042A180`, `0042AA10`, `0042AB20` | the float `+28`<sub>h</sub> through `00425510`, `00423A60` or `00423AB0` |
| `0042E090` | `0042A290` | `00423570(record, arg +24h)` |
| `0042E130` | `0042A890` | below `1000`<sub>h</sub> in word `+3FA`<sub>h</sub>, `0041FC80`; then `00423A10` |
| `0042E300` | `0042AC30` | copies word `+20`<sub>h</sub> to `+3FA`<sub>h</sub> when `+2F2`<sub>h</sub> is non-zero (no filter) |
| `0042E320`, `0042E350`, `0042E4B0` | `0042AE00`, `0042AF10`, `0042A580` | on a record without a parent or whose `+2F2`<sub>h</sub> is 1, call the bare `ret` `0016D6A0`; `0042E4B0` also stores 0 at the argument's `+58`<sub>h</sub> for a record without a parent |
| `0042E440` | `0042A390`, `0042B130`, `0042B270` | `00424010` with the three floats `+2C`<sub>h</sub>–`+34`<sub>h</sub> |
| `0042E4F0` | `00428CD0` | `00504D20` on the record's model row (`003E55B0`) with dword `+20`<sub>h</sub> |
| `0042E530`, `0042E540` | `0042B690`, `0042B770` | `00420D80` or `00420E70` with dword `+74`<sub>h</sub> (no filter) |
| `0042E610`, `0042E650` | `0042B850`; `0042B970`, `0042BA90` | `00420F50` or `00420EA0` with dword `+38`<sub>h</sub> |
| `0042E750`, `0042E7A0` | `0042BCB0`, `00429020` | set bit 21 of `+284`<sub>h</sub> when `+38`<sub>h</sub> is non-zero, or bit 12 when it is 1 |

`00426500`, from `00332440`, is one such walk: `00425FB0(0042D7A0, 0042CF70, records)`.

A record keeps two attached children by id: word `+2C8`<sub>h</sub> for the child whose slot byte `+6A0`<sub>h</sub>
is below `16`<sub>h</sub>, and `+2CA`<sub>h</sub> for the child of slot `16`<sub>h</sub>. Unless `+40B`<sub>h</sub> bit 4 is set, the event
start `00424D80` re-places both through `0041F010(record, child)`, which `004215A0` also calls:

1. it stores a slot below `16`<sub>h</sub> at `+40C`<sub>h</sub>, and takes the mode from the low two bits of `+40B`<sub>h</sub>
   (0 while `+284`<sub>h</sub> bit 27 is set) into bits 2–3 of `+40B`<sub>h</sub>; modes 2 and 3 go straight to step 6;
2. in mode 0, when the record's `@FCP` section 3 (`003E5CD0`) names a bone for the slot (word table
   at its start), it ties the child to that bone with `004211B0`, which links the two skeletons
   with `0046E640` when the child's skeleton entry has bit 7 of its first byte and sets the child's
   parent word `+06`<sub>h</sub>;
3. still in mode 0, it copies the slot's offset (section `+240h + 12 × slot`) to the child's
   `+130`<sub>h</sub> with 1.0 at `+13C`<sub>h</sub>, and stores at `+150`<sub>h</sub> the record's three scales (`+160`<sub>h</sub>,
   `+260`<sub>h</sub> and `+26C`<sub>h</sub>) times the slot's scale at section `+40h + 12 × slot`;
4. in mode 1, or without a section bone, it ties the child to the record's bone for the child's
   `@FCP` word `+36`<sub>h</sub> (`003E5AD0`, bone 0 when there is none) and, when the section exists, zeroes
   the offset and the scale;
5. with a section, it writes the slot's value at `+1C0h + 4 × slot` to the child's `+170`<sub>h</sub>,
   `+174`<sub>h</sub> and `+178`<sub>h</sub>, and 1.0 at `+15C`<sub>h</sub> and `+17C`<sub>h</sub>;
6. it stores the child's id at `+2C8`<sub>h</sub> or `+2CA`<sub>h</sub>.

Small record setters beside them: `00420CF0(record, x, y, z)` keeps the angles `+120`<sub>h</sub>–`+128`<sub>h</sub> at
`+250`<sub>h</sub>–`+258`<sub>h</sub> and stores the new ones, and `00420F20(record, x, y, z)` stores `+140`<sub>h</sub>–`+148`<sub>h</sub>;
both set the fourth float to 1.0 and clear `+284`<sub>h</sub> bit 9. `00421010(record, on)` sets or clears
`+284`<sub>h</sub> bit 3 and calls `00421030`; `004209A0` clears bit 27 and sets bit 26. `00421CD0` returns the
first of the `@FCP` bones for special ids `104`<sub>h</sub> to `106`<sub>h</sub> that is set, or 0 (always 0 below
`@FCP` version 3).

`00422D90` finds the `@FRM` entry (`4D524640`<sub>h</sub>) of the record's container and returns its payload;
`00422E40` is `00424870(…, 1)`; `00424280` wraps an angle in degrees into −180 to 180; `0042FCB0`
counts `02CA4EDC` up, for `002EAD00`.

`00424870(record, frames, mode)` starts a transition of the current entry `+C4`<sub>h</sub> into its motion.
It runs `0041CFC0`, hands the three floats `+2B0`<sub>h</sub> to `+2B8`<sub>h</sub> to `0041D7E0` and sets them to −1,
restarts the entry (`0041D110` when its `+24`<sub>h</sub> is 1, otherwise `+0C`<sub>h</sub> bit `2`<sub>h</sub>, `+24`<sub>h</sub> = 1 and
`0041D790`), sets bit `800`<sub>h</sub> of `+0C`<sub>h</sub> (and `20000`<sub>h</sub> for mode 1), stores `1 / frames` at
`+354`<sub>h</sub>, clears bit `100`<sub>h</sub> when `+344`<sub>h</sub> is −1, and calls `00423AB0(record, +2BCh)`.

With
`+284`<sub>h</sub> bit 20 set or 0 frames it instead stops the alternate entry `+C8`<sub>h</sub> (`+0C`<sub>h</sub> bit `2`<sub>h</sub>,
`0041D790`) after `00426FA0` and returns `00424C40(record)`.

`00424A40` is the same without `0041CFC0` and returns 0 at once when the current entry's `+24`<sub>h</sub> is
already 1. The child callback `0042DF10`, from `00429F70`, uses them on a child record that has no
event of its own for the parent's event (`0041E5B0`): `00422E40` for a child whose `+CC`<sub>h</sub> is below
`1000`<sub>h</sub>, otherwise `00422E50`, which first stops the child's alternate entry and then calls
`00424A40(child, frames, 1)`.

`00423510(record, resource)` returns the payload of the resource's `@FRM` (`00408F90`, `00408F80`)
plus the dword at its `+0C`<sub>h</sub>, or 0 when the section is missing or that dword is 0; `003E6070`
reads three floats there.

### The dirty words

Requests reach a record as bits in two dwords, `+290`<sub>h</sub> and `+294`<sub>h</sub>. `00427DE0(flag)` services them
in five walks of the active list, in fixed order, skipping records with `+284`<sub>h</sub> bit 30:

1. `+290`<sub>h</sub> bits 29, 30, 2, 3, 25, then one of 19, 18 or 20, then 23, 24, 12, 22, and `+294`<sub>h</sub> bit 26;
2. `+290`<sub>h</sub> bits 9, 10, 17, 11;
3. `+290`<sub>h</sub> bits 26, 28, 31 and 9, and `+294`<sub>h</sub> bits 0 to 8, 10 to 20, 22 and 23, some of them in
   else-if chains;
4. `+290`<sub>h</sub> bits 4, 5, 6, 21, 27, 13, 14, 15, 16 and `+294`<sub>h</sub> bits 24, 27;
5. a record with `+290`<sub>h</sub> bit 1 clear gets `+284`<sub>h</sub> bit 30 cleared and, when `flag` is set, `+304`<sub>h</sub>
   bit 14 cleared and `+120`<sub>h</sub>..`+128`<sub>h</sub> copied to `+250`<sub>h</sub>..`+258`<sub>h</sub>; one with bit 1 set runs
   `0042F4C0` again when bit 20 is set.

Most handlers clear their bit after the call; some leave it for a later frame. With `flag` set, work
on a record also raises `+294`<sub>h</sub> bit 25 on the top of its parent chain, and `00427BD0` then composes
that root's model transform (`00420A40`). `00426090` calls `00427DE0(0)` inside each simulation step
(from `003323D0`); `0042ED60` calls it with 1 at the end of the frame. Each bit's test site, handler
and setters are in
[the dirty-bit table](character-render-records-dirty-bits.tsv).

### The system tail

The `130`<sub>h</sub> bytes after the records, at `022C6F28 + 48800h`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `i32` | active list head (-1 empty) |  |
| `04`<sub>h</sub> | `i32` | active list tail |  |
| `08`<sub>h</sub> | `i32` | next-free cursor |  |
| `0C`<sub>h</sub> | `i32` | live count (the allocator refuses at 160) |  |
| `10`<sub>h</sub> | `i32` | pending list head |  |
| `14`<sub>h</sub> | `i32` | pending list tail |  |
| `18`<sub>h</sub> | `u32` | flags: bit 0 distance cull on, bit 2 set with bit 0 at start-up, | bit 4 viewer-inside fade on, bit 5 active list changed |
| `1C`<sub>h</sub> | `f32` | distance at which the distance fade starts (34.0) |  |
| `24`<sub>h</sub> | `f32` | distance fade range (4.0) |  |
| `28`<sub>h</sub> | `f32` | 1/6, copied to each promoted record's `+414`<sub>h</sub> |  |
| `2C`<sub>h</sub> | `u16` | reference record for the distance fade, `FFFF`<sub>h</sub> for none |  |
| `30`<sub>h</sub> | `u32` | the render root, encoded (00426480) |  |
| `42`<sub>h</sub> | `u8` | 1: the per-record shadow walk 00426420 runs |  |
| `43`<sub>h</sub> | `u8` | 0: same walk, must be 0 |  |

`004269A0` writes these defaults and `0042ED30` puts `+18`<sub>h</sub> bits 0 and 2 and `+1C`<sub>h</sub>..`+28`<sub>h</sub> back.
`00426090` stores `+2C`<sub>h</sub> each step from the party-focus actor (`003590D0`, `002E9B80`). Every access
is in [the tail access table](character-render-records-character-render-system-tail-accesses.tsv).

### Render events

A record plays motion events. Word `+CC`<sub>h</sub> is the current event, `+60`<sub>h</sub> the previous one, word `+CE`<sub>h</sub>
an alternate whose presentation entry is `+C8`<sub>h</sub>; the current entry is `+C4`<sub>h</sub>. An event word keeps a
kind in bits 12 to 15 and an index in bits 0 to 11.

`00424D80(record, resource, source, event, …, selector)` starts an event. A kinded event must pass
`004235C0(record, event, selector)`. The stream is the resource's own entry in the resource-entry bank
or, failing that, the model's `@FCM`, `@FRP` or `@FMN` section (`00409FA0`); the entry is admitted by
`0051BA80`, its id stored in `+C4`<sub>h</sub>, the event in `+CC`<sub>h</sub> and the old event in `+60`<sub>h</sub>.

`004235C0` returns 1 (allow) unless all of these hold:

- the record has a current entry;
- after normalising (kind 3 to `2036`<sub>h</sub>; kind 4 to `2035`<sub>h</sub> or `2036`<sub>h</sub> by index; kind 5 to `203E`<sub>h</sub>)
  both events are of kind 1 or 2, kind 1 needing `+284`<sub>h</sub> bit 31 set and kind 2 needing bit 28 clear;
- the pair is not index `3D`<sub>h</sub> on both sides;
- selector 0 with a lower priority for the candidate and `00424230` returning 0, or selector 2 with a
  lower priority for the candidate. Every other selector allows.

Priorities are signed bytes at `01F00410 + (event & FFFh)`; the first `49`<sub>h</sub> bytes hold values 0 to 4.
`00424230` returns 1 without an entry, otherwise bit 12 of the entry's `+2C8`<sub>h</sub> (`0041C760`).
`0041FCA0` returns `+CE`<sub>h</sub> when `+C8`<sub>h</sub> is valid and `004235C0(record, +CEh, +CCh)` allows, else
`+CC`<sub>h</sub>.

### Posting an event

`00427320(record, event)` posts an event. Before choosing a source it refreshes the dword `+110`<sub>h</sub>
from the battle view of the record's actor `+108`<sub>h</sub> (`00420890`: `002ED500` with selector `80`<sub>h</sub> for
events `2005`<sub>h</sub>, `2037`<sub>h</sub> and `2039`<sub>h</sub> to `203C`<sub>h</sub>, `100`<sub>h</sub> for the others; for `203A`<sub>h</sub> a first query with
`800`<sub>h</sub> whose bit 36 makes it call `003B4930`).

`00423790(record, event, last)` then decides
whether the event may follow the last posted one, the word `+3B4`<sub>h</sub>, with the normalising and priorities of
`004235C0` and without its selector rule; a last event without a kind refuses every event, and a
refusal ends the post.

The event's kind picks the source resource `+390`<sub>h</sub>:

| Kind | Source |
|---:|---|
| 0 | the registered script motion slot that bits 20–23 (area slot) and 16–19 (slot) name (`003DD740`, state 4 only); `00423230` then clears bit 12 of the current entry's `+2C8`<sub>h</sub> |
| 1, 2 | `+430`<sub>h</sub>, or `+42C`<sub>h</sub> by the low two bits of `+40B`<sub>h</sub> |
| 3, 4 | `+430`<sub>h</sub> (kind 3; `302F`<sub>h</sub> and `3009`<sub>h</sub> as kinds 1 and 2) or `+42C`<sub>h</sub> (kind 4) |
| 5 | `+42C`<sub>h</sub> while `00423170` holds; otherwise the skill-motion cache entry for the actor's model and the index (`003DC7D0`, `003DCA00`), or `+42C`<sub>h</sub> with `+3B4`<sub>h</sub> set to `203D`<sub>h</sub> when there is none |

`004230A0(record, event)` then refuses kinded events of index `37`<sub>h</sub> while the character object's byte `+B4`<sub>h</sub> is 0
and `39`<sub>h</sub> and `3A`<sub>h</sub> while its `+AC`<sub>h</sub> is 2, which clears the source. `00422FD0(record, resource,
event)`, asked by `00423B10`, holds when `+284`<sub>h</sub> bit 16 is set and the resource's entry for the
event index (index 0 for kind 5, `00408F80`) has bit 16 or 17 of its `+04`<sub>h</sub>.

`motionplay_bb(motion, frames)` (`00BB`<sub>h</sub>, `003DD8D0`) and `puppetmotionplay_41f` (`041F`<sub>h</sub>,
`003DD980`, for a puppet) post a kind-0 event: a motion id whose top byte is `10`<sub>h</sub> to `1F`<sub>h</sub> names
slot `top − 10h` of the script's area slot. They act only when that slot is registered and pass the
event `(area << 4 | slot) << 16 | (motion & FFFFFFh)` with the frame count to `002EB080` or `002EB0D0`; the actor
form also stores the slot at actor `+F5`<sub>h</sub>.

### The skill-motion cache

Kind-5 motions are files read on demand into 16 entries of `14`<sub>h</sub> bytes at `02B57F70`, with at most
four 32 KiB units in use. `003DCBC0`, from the area initialiser `00266D10`, numbers the entries, empties
the 16-entry size cache at `02B580B0` and requests the table file tagged `PCSkill` (kind 9, file 5).

`SkillMotionEntry` (`14`<sub>h</sub> bytes, offsets from the start of the 02B57F70+`14`<sub>h</sub>*i):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00`<sub>h</sub> | `u32` | block | the read block, registered with the render system |
| `04`<sub>h</sub> | `i16` | users |  |
| `06`<sub>h</sub> | `u8` | state | 0 free, 1 queued, 2 reading, 3 ready, 4 releasing |
| `07`<sub>h</sub> | `u8` | units | 32 KiB units of the file |
| `08`<sub>h</sub> | `u32` | id | i \| `10`<sub>h</sub> \| serial << 4 |
| `0C`<sub>h</sub> | `u32` | model |  |
| `10`<sub>h</sub> | `u16` | motion |  |
| `12`<sub>h</sub> | `u8` | class | weapon class |
| `13`<sub>h</sub> | `u8` | index | i |

- `003DCD00(actor, motion, class, file)` returns `80000000`<sub>h</sub> while `002E80B0(actor)` is non-zero.
  An entry for the model, motion and class in states 1 to 3 gains a user and its id is returned.
  Otherwise the size comes from `003DC8D0` (`80000001`<sub>h</sub> when it fails), rounded up to units, and the
  entry is filed only if the units of entries with users plus the new ones stay within 4.
- Filing takes the first free entry (`003DC380`); with none it releases the idle ready entries
  (`003DC6A0`) and tries again. A new entry has one user and state 1, and the idle entries are
  released when all held units exceed 4. With `file` 0 the cache stays as it is:
  `80000002`<sub>h</sub> says the entry exists or could be filed; `003DC410` is that test, `003DCCF0` the request.
- `003DC780(id)` drops a user; an entry of 0 units that reaches no users in state 3 is released at
  once. `003DC6A0` releases every ready entry without users: state 4, and `10`<sub>h</sub> added to the id.
- `003DC4A0`, from `002E65A0` in the field frame `0022A770`, works only after a change (`02B58170`): it unregisters
  and frees every releasing entry's block (`0041E490`, `00369800`) and frees the entry, then starts
  each queued one (`003DC5B0`): a block in arena 6 and a read of the file `003DCA30` names, whose
  completion `003DC340` sets state 3 and registers the block (`0041E580`).
- `003DC7D0(actor, index)` finds a ready entry for the actor's model and motion, matching the class
  too when `00322710` holds, and `003DCA00(id)` returns its block; `003DCB90(id)` returns the state.

`debug_registskillmotion` (`2079`<sub>h</sub>, `0050CE70`) and `debug_disposeskillmotion` (`207B`<sub>h</sub>,
`0050CFB0`) reach the request and the release; the battle code uses `00325A20` (the test), `00325B40`
(the request) and `00325A00` (the release). The code at `003DC420`, which no instruction reaches, empties the size cache and releases
the idle entries.

### The presentation-entry reference container

The container at root `+160`<sub>h</sub> maps an entry id to a `3A0`<sub>h</sub>-byte presentation entry. A node is `30`<sub>h</sub>
bytes: `+00`<sub>h</sub> state (bit 0 used, bit 1 refresh on lookup), `+04`<sub>h</sub> id, `+08`<sub>h</sub> / `+0C`<sub>h</sub> previous and
next id, `+10`<sub>h</sub> source, `+18`<sub>h</sub> cached pointer, `+20`<sub>h</sub> 32-bit offset.

- `0051F240(container, id)` takes the table by the container's mode (`+04`<sub>h</sub> low two bits: 1 direct,
  0 through `003AB7F0`, anything else returns 0), indexes it by `id & FFFFh`, and when node bit 1 is
  set rebuilds `+18`<sub>h</sub> as the sign-extended 32-bit sum of the resolved source and the offset.
- `0051F080` admits: `0051F410` takes the cursor slot, the id is `slot | 10000h`, and the node joins
  the active list. The high half never changes, so a reused slot gets the same id.

- The container's own list helpers: `0051F2F0`, run by the initialiser `0051F170`, clears every node
  (state 0, id and links −1, source, pointer and offset 0); `0051F380`, run by `0051F080`, appends
  an id at the tail (head `+1C`<sub>h</sub>, tail `+20`<sub>h</sub>); `0051F4C0`, run by `0051F190`, unlinks one; and
  `0051F150`, used by `0051BA80`, returns the cursor `+18`<sub>h</sub> while the used count `+14`<sub>h</sub> is below
  the capacity `+10`<sub>h</sub>, else −10.

- `0051BA80(container, id, source, offset, …)` builds a payload on the stack (`0041CB90`, `0041D220`),
  admits a node when `id` is -1, copies the payload in, rebuilds its pointers (`0041CA70`) and writes the
  id into its first dword; if the payload build fails it releases the existing entry and returns -1.
- `0051BA40` releases: it resets the entry (`0041CF00`) and clears the node (`0051F190`) without
  comparing ids.
- `0051B9F0` rebuilds every active node's cached pointer (`0051F620`) and every payload (`0041CA70`).
- `0051B970` updates the entries in three walks: entries with `+0C`<sub>h</sub> bit 12 set first (`0051BBE0`),
  then twice the others (`0051BBF0`) with the phase word `02CA83F4` at 1 and then 2.

### How an entry picks its track

An entry plays an authored stream (`+368`<sub>h</sub>) made of tracks. It keeps `+28`<sub>h</sub> track states of `A0`<sub>h</sub>
bytes from `+30`<sub>h</sub>; the playing one is `+388`<sub>h</sub>. The command handlers are on
[authored presentation commands](authored-presentation-commands.md).

- `0041CD30(entry, state, n)` sets up track `n`: it walks the headers (each header's word `+4` is the
  distance to the next), writes the state defaults, and makes the track primary (entry `+18`<sub>h</sub> /
  `+20`<sub>h</sub>, state flag bit 0, active) when its kind byte is 1 or the stream has one track. Its start
  cursor `+88`<sub>h</sub> is the first command, or the command after a `FFFF`<sub>h</sub> marker when the track has one.
- `0041CFC0(entry)` resets: it keeps a snapshot of an interrupted transition (`+380`<sub>h</sub>, `+384`<sub>h</sub>, entry
  `+2E8`<sub>h</sub> bit 2), rewinds every state's cursor to its start, and leaves only the primary active.
- `0041C9A0(entry, n)` hands out a state other than state 0: one already holding track `n` (wiped), else
  the first inactive one.
- Command class `01`<sub>h</sub> (`00417920`) switches to a track at once (mode 0), only when the current state's
  word is 2 (mode 1), or when entry `+0C`<sub>h</sub> bit 6 allows (mode 2, otherwise it raises bit 7 and waits).
- Command class `0B`<sub>h</sub> (`00417110`) asks the selector `[02CA4668]` (entry kind `+2DC`<sub>h</sub>) for a choice
  and plays `table[choice] + addend` through class `01`<sub>h</sub>. A record with `+284`<sub>h</sub> bit 27 and a parent
  reads the parent's cached choice (`+4B8`<sub>h</sub>..`+4BB`<sub>h</sub> for selector kinds 0, 2, `0A`<sub>h</sub>, `10`<sub>h</sub>) instead.

### The choice selectors

`004269A0` installs the selector table `01F000A0` with `0041D6E0`: 48 kinds of `10`<sub>h</sub> bytes, a
count and a pointer to a handler list, of which `00417110` calls the first handler with the stream.
The authored command `00`<sub>h</sub> also ends with kind `2F`<sub>h</sub>'s handler. Every kind not listed returns 0
(`005C5230`); the handlers read the stream's render record `+2E0`<sub>h</sub>:

| Kind | Handler | Choice |
|---|---|---|
| `00`<sub>h</sub>, `0A`<sub>h</sub>, `0B`<sub>h</sub> | `004223F0`, `00422400`, `00422410` | jumps to the locomotion selector `004256E0` with 0, 1 or 2 |
| `01`<sub>h</sub> | `00422420` | a counter in byte `+40E`<sub>h</sub>: at 0 it draws a random 0–4 (`003A6E60(5)`) into `+411`<sub>h</sub>, returns it and starts counting at `[01DFE0B4]`; at `11 × [01DFE0B4]`, when the query `0041F2F0(record, 20h)` reports bit `4`<sub>h</sub>, it adds 5 to `+411`<sub>h</sub> and returns that; otherwise it counts up to at most 100 and returns −1 |
| `02`<sub>h</sub> | `00422500` | the byte `+410`<sub>h</sub>, chosen once while it is −1 from the bits of `0041F2F0(record, 30h)`: bit `2`<sub>h</sub> counts `+40E`<sub>h</sub> up (back to `[01DFE0B4]` past three times that) and chooses 0; otherwise 1 with bit `4`<sub>h</sub>, else 2, and `+40E`<sub>h</sub> is cleared |
| `04`<sub>h</sub> | `00660570` | −1 |
| `10`<sub>h</sub> | `004225A0` | counts down `+412`<sub>h</sub>, armed with a random value from the stream's byte `+2DD`<sub>h</sub> − 1 to `+2DE`<sub>h</sub> − 1 (times `[01DFE0B4]`), and chooses 1 when it reaches 0 |
| `20`<sub>h</sub> | `00422630` | 0 when the point from `0041F2F0(record, 4)` lies within ±90° of the record's heading (`00424370`: `atan2` of x and z in the record's own frame), else 1 |
| `21`<sub>h</sub> | `004226C0` | 0 within ±60°, else 1 or 2 by side; plus 3 on a random half (`003A6E60(2)`) |
| `22`<sub>h</sub> | `00422760` | 1 when the vertical angle to the point (`00424460`) is negative |
| `23`<sub>h</sub> | `004227D0` | 0 within ±60°, else 2 or 3 by side |
| `24`<sub>h</sub> | `00422870` | the quarter the point lies in (0 ahead, 1 at 45°–135°, 2 at −45° to −135°, 3 behind) in record byte `+2AF`<sub>h</sub>, plus 4 on a random half |
| `25`<sub>h</sub> | `00422940` | from the angle to the record that the look controller's source names (`003E2CD0`): 0 between −90° and 0°, 1 at −90° or less, 2 above 90°, 3 between 0° and 90°; 0 without a source |
| `2F`<sub>h</sub> | `00422A10` | clears the word `+456`<sub>h</sub> and sets byte `+2AF`<sub>h</sub> to −1, returning −1 |

`00424460(matrix, point)` turns the point into the record's own frame (the matrix at `+180`<sub>h</sub>) and
takes `atan2` of its y and z.

### The per-entry update

`0041C410(entry)`, from `0041D820`, `00422EB0` and `002EE3E0`, runs an entry only when its record's
`+6E0`<sub>h</sub> is 1 in main-loop state 3 (`00229EA0`) or 0 in any other state, the entry's `+0C`<sub>h</sub> has
bit 1 set and bits 18 and 23 clear, the speed `+340`<sub>h</sub> is non-zero, and the status table entry
`003E7D10(+6A4h, 3)` is 0 or the record's `+C0`<sub>h</sub> bit 6 is clear. In phase 1 of `02CA83F4` it runs
only records with `+284`<sub>h</sub> bit 27 and no parent, and in phase 2 it skips those.

- In state word `+24`<sub>h</sub> = 1 with `+0C`<sub>h</sub> bit 3 and `+2C8`<sub>h</sub> bit 12 set, it resets the entry
  (`0041CFC0`), clears `+2C8`<sub>h</sub> bit 12 and `+0C`<sub>h</sub> bit 9 and, for a positive
  `+348`<sub>h</sub>, seeks there (`0041D820`) and sets `+24`<sub>h</sub> to 0 when `+348`<sub>h</sub> equals `+34C`<sub>h</sub>, else 1.
  With only `+2C8`<sub>h</sub> bit 12 set and `+348`<sub>h</sub> not −1 it sets `+24`<sub>h</sub> to 2.
- With the record's `+4B7`<sub>h</sub> bit 4 set it picks the locomotion mode (`004255B0`).
- It runs every track state through the walker `0041DA90`, then calls `0041DD40` on states 1 and up
  until a pass finds none to act on, sets `+0C`<sub>h</sub> bit 8, and copies whether `003E7D10(+6A4h, 3)` is
  non-zero into the record's `+C0`<sub>h</sub> bit 6.

`004255B0` gives controller 5 (`003E4890` → `0051A920`) a mode from the record's speed `+23C`<sub>h</sub>
(taken as 0 while `+62C`<sub>h</sub> bit 0 is set or `003AEF20(+550h)` reports): 0 below the walk threshold
`003E58B0` (the scale times an `@FCP` value, 0.013333 without one), 2 at or above `+420`<sub>h</sub>, and
otherwise 1 when the move direction `+244`<sub>h</sub> is within 45° of the facing `+124`<sub>h</sub>, 3 from 45° to
135°, 4 from −45° to −135°, and 5 behind.

Smaller entry helpers:

- `0041D7E0(entry, start, end, limit)` stores the time window `+344`<sub>h</sub>, `+348`<sub>h</sub>, `+34C`<sub>h</sub>, pulling
  `+344`<sub>h</sub> down to the limit when both are set and the limit is smaller.
- `0041D110(entry)` resets, clears `+2C8`<sub>h</sub> bit 12, seeks to `+344`<sub>h</sub> when it is set (with `+0C`<sub>h</sub>
  bit 28 raised around the call) and sets `+24`<sub>h</sub> to 1.
- `0041D4D0(entry, on)` sets or clears `+0C`<sub>h</sub> bit 12, `+33C`<sub>h</sub>, and bit 5 of every state's word
  `+96`<sub>h</sub>.
- `0041CEC0(entry)` calls bank-A slot `0C`<sub>h</sub> (`[02CA4470]`) with the actor `+2C0`<sub>h</sub> and `+31C`<sub>h</sub> and
  sets `+0C`<sub>h</sub> bit 9, as the walker does at a motion's end.
- `0041C970(entry, n)` returns the state playing track `n` (state `+80`<sub>h</sub>); `0041C720(entry)` returns
  whether the state playing the entry's track `+26`<sub>h</sub> has byte `+95`<sub>h</sub> equal to 1; `0041C6B0(entry)`
  returns `+0C`<sub>h</sub> bit 15. `0041C3A0` is an empty function that `00423280` calls.

- `0041C770(entry)`, for `00423380`, returns the dword `+0C`<sub>h</sub> of the first state after state 0
  whose byte `+95`<sub>h</sub> is 1, or 0.

## Layouts

The record is `740`<sub>h</sub> bytes; the array is 160 of them, `48800`<sub>h</sub> bytes, then the tail. These fields
are the ones the functions on this page use:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `000`<sub>h</sub> | `i16` | own index, -1 when free |  |
| `002`<sub>h</sub> | `i16` | previous record in its list |  |
| `004`<sub>h</sub> | `i16` | next record in its list |  |
| `006`<sub>h</sub> | `i16` | parent record, -1 for a root |  |
| `008`<sub>h</sub> | `i16` | first child |  |
| `00A`<sub>h</sub> | `i16` | next sibling |  |
| `010`<sub>h</sub> | `u64` | context (the render root), stored by the initialiser |  |
| `018`<sub>h</sub> | `i32` | skeleton entry index (root `+D98`<sub>h</sub>) |  |
| `01C`<sub>h</sub> | `char[32]` | key, "makeid" and one byte |  |
| `03C`<sub>h</sub> | `char[32]` | model name |  |
| `060`<sub>h</sub> | `i16` | previous event |  |
| `064`<sub>h</sub> | `i16` | model instance index (root `+DA0`<sub>h</sub>) |  |
| `0C0`<sub>h</sub> | `u8` | shadow kind (bits 3-4), scripted shadow LOD (bit 1), scripted shadow alpha (bit 2) |  |
| `0C4`<sub>h</sub> | `i32` | current presentation entry id |  |
| `0C8`<sub>h</sub> | `i32` | alternate presentation entry id |  |
| `0CC`<sub>h</sub> | `i16` | current event |  |
| `0CE`<sub>h</sub> | `i16` | alternate event |  |
| `114`<sub>h</sub> | `u32` | shadow entry handle (pool at 02B40528) |  |
| `118`<sub>h</sub> | `u32` | shadow entry handle (pool at 02B3F570) |  |
| `210`<sub>h</sub> | `f32[4]` | colour, 1.0 after a clear |  |
| `220`<sub>h</sub> | `f32[4]` | second colour, 1.0 after a clear |  |
| `284`<sub>h</sub> | `u32` | state flags (bit 14 character-model directory, bit 30 skipped by the dirty walk) |  |
| `290`<sub>h</sub> | `u32` | dirty word 1 |  |
| `294`<sub>h</sub> | `u32` | dirty word 2 |  |
| `400`<sub>h</sub> | `void*` | the model's @FCP data |  |
| `408`<sub>h</sub> | `i16` | @FCP section index |  |
| `414`<sub>h</sub> | `f32` | 1/6, from the tail at promotion |  |
| `4C0`<sub>h</sub> | `8 B x 10` | fade channels (character-fades.md) |  |
| `610`<sub>h</sub> | `f32 x 4` | live heading, speed, accumulator, flags (the coast-down latch) |  |
| `620`<sub>h</sub> | `f32 x 4` | cached heading, speed, accumulator, latch word |  |
| `6B0`<sub>h</sub> | `i32` | render-object key |  |
| `6B8`<sub>h</sub> | `void*` | CharacterRenderObject (character-render-object.md) |  |

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

- The pool size is the allocation size `48930`<sub>h</sub> in `003325D0`; the tail is addressed at fixed offsets
  from `022C6F28` (`+48800`<sub>h</sub> and on) in every consumer, so a larger pool means moving all of them.
- A record is not drawn the frame it is allocated; it is promoted at the end of the frame.
- A record's key byte is the cursor at allocation, which is the record's own index, so the key is not
  a model name; look records up by `+3C`<sub>h</sub> instead.
- The event priority table at `01F00410` is indexed by the event's low twelve bits with no bound.
  From byte `50`<sub>h</sub> on the table holds other data (`10`<sub>h</sub>, `FF`<sub>h</sub>, `80`<sub>h</sub>), so an event index of `50`<sub>h</sub> or
  more reads priorities such as -1 or -128.

## Related

- [CharacterRenderObject](character-render-object.md): the draw object a record owns.
- [Character fades](character-fades.md): the fade channels at `+4C0`<sub>h</sub> and the coast-down latch.
- [Character lighting and shadows](character-lighting-and-shadows.md): the two shadow pools.
- [Authored presentation commands](authored-presentation-commands.md): the command handlers.
- [Frame update order](../Engine-Core/frame-update-order.md): where `003323D0` and `00332660` run.
- [Global state accessors](../Engine-Core/global-state-accessors.md): the encoded pointers
  `0020E600` / `0020E620`.
- [Resource ownership and disposal](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md):
  `003AB7F0`, which resolves a container's table.
