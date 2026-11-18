[Home](../../README.md) / [Graphics](README.md) / Skeleton entries and bones

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Skeleton entries and bones: the skeleton entries of render records, the listed bones and their lookups, bone points, the motion bone list and bone-to-bone ties | system | Graphics | Character models / Animation And Motion | The skeleton side of a character render record: the skeleton entries and their links and update order, the bones a skeleton lists and how a bone is looked up, the point a bone gives, the motion bone list a motion binds against, and tying a bone to a bone of another skeleton. | 0x00426090, 0x002ED570, 0x0046E4D0, 0x00424D80, 0x00422310, 0x00422380, 0x004218A0 |

## What the player sees

A character's body follows its skeleton: each bone of the model moves with the motion it plays, and a
sword or a shield stays in the hand because its bones are tied to the hand's bone.

## How it works

### Skeleton entries: links and the update order

A skeleton entry knows its own index (`+0x04`), the index of the skeleton it hangs from (`+0x08`,
−1 for no parent) with that entry's encoded address at `+0x0C`, and the index of an entry attached to it
(`+0x10`). The bank keeps an update list at `+0x60` in which a parent always comes before its
children; `0x0046E6F0` rebuilds it after every acquire (`0x0046E4D0`), release and attach.

- `0x0046E6F0` first runs `0x0046E950` on every entry, which clears bit `0x2` of `+0x00` and forgets a
  parent index whose entry is gone (`+0x08` and the word `+0x14` set to −1). It then appends, pass
  after pass, every entry with a skeleton (`+0xA0`) that has no parent or whose parent is already listed
  (`0x00537260`), marking it with bit `0x2`.
- `0x0046E4D0(bank, …)` acquires an entry: it takes a slot with `0x0051FBB0` and returns -1 when that refuses
  (`0x0046E4F0`-`0x0046E4FE`). Otherwise it clears the entry (`0x003721E0`), builds it with `0x00372820` from its other
  seven arguments, stores the index at `+0x04`, rebuilds the list (`0x0046E6F0`) and returns the index
  (`0x0046E50A`-`0x0046E56C`).
- `0x0046E2B0(bank, index)` releases an entry: it clears it (`0x003721E0`), frees its slot (`0x0051FCF0`)
  and rebuilds the list. The record teardown `0x0041E860` calls it for the record's `+0x18`.
- `0x0046E590(bank, child, parent, slot)` attaches one skeleton to another through `0x00370180`, which
  stores the parent's index in the child's `+0x08` and, for slot −1, the child's index in the
  parent's `+0x10` (otherwise the slot in the child's word `+0x14`); it then sets `+0x0C` and
  rebuilds the list. Its caller is `0x004218A0`.
- `0x004218A0(parent, name, child)` ties nothing when either record has no skeleton entry (`+0x18` -1 or
  `0x002ED570` null; `0x004218CC`-`0x00421940`). It sets the child's word `+0x2F2` to 0 (`0x00421942`); a null name,
  which `0x004215A0` passes for slot `0x7FFF` (`0x0042183D`), sets the child's `+0x284` bit `0x4000000` and `+0x2F2`
  to 1 and ties at bone −1, the whole skeleton (`0x0042194E`-`0x00421964`).
- Any other name takes the bone `0x00372760(parent entry, name)` gives, and a result of −1 ties nothing
  (`0x00421966`-`0x00421979`). `0x004218A0` then calls `0x0046E590` with the bank of the parent's root, the child
  entry's `+0x04`, the parent entry's `+0x04` and the bone, and, when the child's `+0x284` bit `0x4000000` is
  set, `0x003E5D30(child)`, which puts fade channels 0, 1 and 4 back to 1.0 (`0x0042197B`-`0x0042199D`).
- `0x0046E420(bank, index)` refreshes an entry after its resources change: it re-runs `0x003713C0` on
  the entry and its parent, re-encodes `+0x0C`, and re-runs it on the entry at `+0x10` before
  re-linking that entry's bones (`0x00372F60`). Its callers are `0x003E6F90`, `0x0041D220`, `0x0041D820` and `0x004242B0`.
- `0x0046E3E0`, the refresh after the bank's storage moves, re-encodes every `+0x0C` (`0x0046E910`) and
  re-links every `+0x10` (`0x0046E8D0`). `0x00372F60(entry, other)` points each listed bone of the entry
  that names a bone of the other at that bone (`+0x278`, `+0x27C`).
- `0x0046E8B0(bank, index)` returns the entry, or null for −1.

### Skeleton bones: the listed bones, lookups and the bone-to-bone tie

A skeleton entry's dword `+0x9C` is its skeleton kind, 0 or 2 (an `@FTR` node table, see
[model files](model-files-cm-ca.md)), and `+0xA0` the skeleton resource. The bone array `+0x84` holds
`+0x88` bones of `0x290` bytes; after them come `+0x88` u16 slots whose first `+0x8A` list the bones
built from pool values (node flag bit `0x100`), then the extra slots.

- `0x00373DC0(bone)`, from the skeleton builder `0x00372820`, puts a bone at rest: identity at
  `+0x1F0` and `+0x230` (`0x0046D120`), `(0, 0, 0, 1)` at `+0x1A0` and `+0x1C0`, 1.0 at `+0x1E0` to
  `+0x1EC`, the flags `+0x280` cleared, the links `+0x270` to `+0x276` and `+0x27C` set to −1,
  `+0x278` null, byte `+0x28A` = 3, bits `0x1` and `0x2` of `+0x28B` set and bit `0x4` clear.
- `0x00372280(entry)`, from `0x0041CF00`, `0x00422A30` and `0x00424550`, resets each listed bone: it clears bit `0x10` of `+0x280` and sets `+0x1A0` and `+0x1C0` back to `(0, 0, 0, 1)`.
- `0x00372510(entry)`, from `0x00424D80`, fills the extra slots with `0x7FFF`, as many as the model's
  `@FTR` header word `+0x38` gives, and clears bit `0x1000` of the entry's `+0x00`. `0x00371330(entry, i)` returns
  extra slot `i` of a kind-2 skeleton when `i` is below that count, else 0; `0x0053AB50` calls it.
- `0x003725A0(entry, bone)` holds when the bone is listed. `0x003737C0(entry, key)` returns the first
  node with flag bit `0x100` whose key (`0x00409250`) matches, and `0x00372760(entry, name)` the record whose
  name at `+0x00` of the `0x4C`-byte kind-0 records matches; both return −1 otherwise.

### Bone points

`0x00421E20(record, point, mode, out)` turns a point id into a matrix. It returns null when the record's model id
`+0x18` is −1 or has no `0x002ED570` entry (`0x00421E49`-`0x00421E77`). Ids `0x107` and `0x108` stand for the record's
words `+0x2F4` and `+0x2F6`, and `0x300` to `0x3FF` go to `0x003710E0` with the bone and offset `0x003E5B30` gives,
returning `out` itself, or null when `0x003E5B30` gives `0xFFFF` or `0x003710E0` returns null
(`0x00421EA1`-`0x00421F38`).

With bit `0x80` of the skeleton entry's `+0x00` set and an id below `0xFF` (a signed compare, so `0x8000` and
above too), `0x003E5AD0` takes the bone from the record's `@FCP` at `+0x400`: the word at
`@FCP + [@FCP + 2] + 0x14C + id × 2`, the id signed, for an id below `0x20`, and none otherwise. `0x004220F0` hands
it to `0x003710E0` with the point (0, 0, 0, 1) and returns what that returns; no `@FCP` or no bone returns null
(`0x00421F40`-`0x00421F99`).

Otherwise, with bit `0x80` of the skeleton entry's `+0x00` clear, `0x00370E30` finds the bone by the name
`0x00422310` gives; with it set and an id from `0xFF` up to `0x7FFF` (the signed compare), `0x00370FA0` finds it by
the key from `0x00422380`.

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
  `+0x70` (by the bits under mask `0x3` of its `+0x04`), and otherwise bone 0 with the vector `+0x4C` of the rig
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

Before `0x0041BEE0` binds a motion's bone channels it runs `0x00370BB0`, which lists the skeleton's bones as 12-byte nodes
(index, previous, next) in the scratch list at `[0x01EF9438]`, with the head at `+0x00` and the count at `+0x1804`. Kind
0 lists every record (`0x00370BD0`; with bit `0x20` of the entry's `+0x00` set only records whose word `+0x22` is 1 or
7) and kind 2 every node with flag bit `0x100` (`0x00370CD0`). For kind 2, `0x00370E00` then claims the node whose key
matches each channel, unlinking it (`0x00373540`). For any other kind it answers -1 and `0x0041BEE0` skips the channel.

`[0x01EF9438]` normally points at `0x02AD9EC0` (`0x00370DE0`); `0x00426090` and `0x004262E0` point it at
`[0x01FD4A78]` (`0x00370DF0`) for their work and back at the end.

### Tying bones to another skeleton

`0x0046E640(bank, child, parent, slot)` ties a kind-2 skeleton to another (`0x00370390`, which jumps to
`0x00373160`), which does nothing when the child's `+0xA0` decodes to null (`0x00373181`): the child's `+0x08` takes the
parent's index, and slot −1 stores the child's index in
the parent's `+0x10` while any other slot goes to the child's word `+0x14`.

Every listed child bone
saves its parent link `+0x270` in `+0x28E`. With slot −1 and a parent of kind 2 (`0x0037326A`; any other kind ties no
bone), a bone whose node has flag bit `0x100` and whose
key names a listed bone of the parent is then tied to that bone:

- the parent's bone gets the child bone's address at `+0x278` and its node number at `+0x27C`, so
  motion values written to it also reach the child bone;
- the child bone copies the parent bone's matrices `+0xC0` and `+0x150` (`0x0046D100`) and sets bit `0x2` of
  `+0x280`;
- when the child bone's parent bone is a root (that bone's saved link is −1), the child bone's
  `+0x270` becomes −1 and `+0x276` takes the parent bone's `+0x270`.

`0x0046E370(bank, child)` undoes it through `0x00370BA0` (kind 2 only) and `0x00373380`: when the parent's
`+0x10` names the child it is set to −1 and every listed parent bone's `+0x278` and `+0x27C` are
cleared; the child's `+0x08` and `+0x14` become −1, its first bone's `+0x1F0` the identity, and each
listed bone clears bit `0x2` of `+0x280`, takes its parent link back from the node (mask `0xFFF000`, with
`0xFFF` meaning no parent) and sets `+0x276` to −1.

`0x00372610(a, b, c, scale, d)`, called by the final-pose composer `0x00373860`, multiplies `a`, `b` and
`c` into `0x02AD9E40` (`0x00217150`), `[0x02AD9E40] = (a × b) × c` (`0x0037266C`, `0x00372680`), scales the four rows
of a copy of that matrix by the four floats of `scale`, row i × `scale[i]` (`0x00202FE0`, `0x00372685`-`0x003726D7`),
and multiplies the result by `d` into `0x02AD9E80`, `[0x02AD9E80] = t × d` with t that scaled copy (`0x003726EB`).

## Layouts

The access tables beside this page list every instruction found touching each structure:

- [the skeleton bank](character-render-records-render-stride-c0-bank-accesses.tsv) and
  [a skeleton entry](character-render-records-skeleton-entry-accesses.tsv), the element `0x002ED570` returns from it.

## Related

- [Character render records](character-render-records.md): the record array, its lifecycle and render events.
- [Presentation entries](presentation-entries.md): the reference container and the per-entry update.
- [Model files (.cm, .ca)](model-files-cm-ca.md): the `@FTR` skeleton the entries are built from.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Audio: `0x00421E20` is called by `0x00332C40`, `0x003B99D0`; those functions are documented on
  [animation sounds](../Sound-And-Music/animation-sounds.md), [effect anchors and targets](effect-anchors-and-targets.md).
- Core runtime: `0x0053AB50` calls `0x001EDE70`; those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md).
- Movement: `0x00202FE0` is called by `0x00334220`, `0x00334E00`, `0x00335B60`, `0x00335E50`, `0x00336E40`, `0x00338490`,
  `0x00339F00`, `0x0033A3D0`, `0x0033BAA0`, `0x0033CC80`, `0x0033D890`, `0x0033DFD0`.
- Movement: those functions are documented on [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md),
  [spawn record fields](../Enemy-Spawning/spawn-record-fields.md),
  [bestiary](../Enemy-Spawning/bestiary.md).
- Party: `0x00426090` calls `0x003590D0`; those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md).
- Resource: `0x002ED570` is called by `0x00409CA0`, `0x00409D60`, `0x00409F50`, `0x00409FE0`, `0x0046E1B0`, `0x004780B0`; `0x00371330`
  calls `0x004096C0`, `0x00409F50`; `0x003713C0` calls `0x004096C0`, `0x00409F50`; `0x00372510` calls `0x004096C0`, `0x00409F50`;
  `0x00372820` calls `0x004096C0`, `0x00409A30`, `0x00409F50`; `0x003E4CB0` calls `0x002ED570`; `0x003E6DA0` calls `0x002ED570`;
  `0x003E6F90` calls `0x002ED570`.
- Resource: `0x0041BEE0` calls `0x002ED570`, `0x00409A30`, `0x00409F50`; `0x0041CF00` calls `0x002ED570`; `0x0041D220` calls
  `0x002ED570`, `0x00409210`, `0x00409660`, `0x00409A30`, `0x00409F50`; `0x004215A0` calls `0x002ED570`; `0x004218A0` calls
  `0x002ED570`; `0x00421E20` calls `0x002ED570`; `0x004221F0` calls `0x002ED570`; `0x00422A30` calls `0x002ED570`, `0x00409F50`;
  `0x004242B0` calls `0x002ED570`.
- Resource: `0x00424550` calls `0x002ED570`, `0x00409090`, `0x00409FA0`; `0x00424D80` calls `0x00409090`, `0x00409210`, `0x00409FA0`,
  `0x00409FD0`; `0x0046E2B0` calls `0x002ED570`, `0x0051FCF0`; `0x0046E370` calls `0x002ED570`; `0x0046E3E0` calls `0x0051FF30`;
  `0x0046E420` calls `0x002ED570`; `0x0046E4D0` calls `0x002ED570`, `0x0051FBB0`; `0x0046E590` calls `0x002ED570`; `0x0046E640` calls
  `0x002ED570`; `0x0046E6F0` calls `0x002ED570`.
- Resource: `0x0046E8B0` calls `0x002ED570`; `0x0046E8D0` calls `0x002ED570`; `0x0046E910` calls `0x002ED570`; `0x0046E950` calls
  `0x002ED570`; `0x0051FBB0` is called by `0x00409FE0`; `0x0051FCF0` is called by `0x00409CA0`, `0x00409D60`.
- Resource: those functions are documented on
  [resource ownership and disposal](../Game-Files-And-Data-Tables/resource-ownership-and-disposal.md),
  [resource lifecycle](../Game-Files-And-Data-Tables/resource-lifecycle.md),
  [resource sections](../Game-Files-And-Data-Tables/resource-sections.md).
- Resource: and on [character render records](character-render-records.md),
  [native limits](../Engine-Core/native-limits.md),
  [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md).
