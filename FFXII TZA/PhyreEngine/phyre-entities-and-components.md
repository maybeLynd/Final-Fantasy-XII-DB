---
title: "Phyre entities and components: PEntity, its component list, the world-matrix registry and the hooks that run on loaded components"
kind: "system"
category: "PhyreEngine"
addresses: "006AB7E0, 006AC300, 006ACA70, 006ACAC0, 006ABEC0, 006ABF40, 006AB600, 006ABFA0, 006AB410, 006AADD0, 006AFF00, 006AF4F0, 0069ECE0, 01F2EB40, 01F2EB78, 02E4EAF0, 02E4E720, 0067F6F0"
---

## What the player sees

Nothing directly. An entity is PhyreEngine's container for an object placed in a scene: it owns a
world matrix and a list of components. The engine uses the registry on this page to answer "which
entity does this matrix, or this object, belong to", for example when a physics body reports a
contact.

## How it works

### Entities and components

A `PEntity` (descriptor `02E4EAF0`, `0x38` bytes) holds the first of its components at `+0x00`, its
world matrix at `+0x08` and a node of the world-matrix registry at `+0x10`. A `PComponent`
(descriptor `02E4E720`, `0x18` bytes) holds the next component at `+0x00`, its entity at `+0x08` and
its own class descriptor at `+0x10`. Six classes derive from `PComponent`: `PAnimatableComponent`,
`PInstancesComponent`, `PNameComponent`, `PQuarryComponent`, `PScriptableComponent` and
`PTriggerReceiverComponent`.

The registrar `006AB7E0` publishes the entity's script methods, each as a method record whose
function sits `0x30` bytes in, and the member `m_firstComponent`:

| Method | Function | What it does |
|---|---|---|
| `getComponent` | `006ACA10` | walks the list and returns the first component whose class is the given class or derives from it |
| `getWorldMatrix` | `006B5C70` | returns `+0x08` |
| `setWorldMatrix` | `006ACAC0` | moves the entity in the registry to the new matrix |
| `addComponent` | `006AC300` | adds a component at the front of the list |
| `removeComponent` | `006ACA70` | unlinks a component |
| `FindEntityForWorldMatrix` | `006ABF40` | looks a matrix up in the registry |
| `FindEntityForObj` | `006ABEC0` | finds the matrix of any object, then its entity |

### Adding and removing components

`006AC300(entity, component)` returns 0 at once when the component already belongs to this entity.
It returns `0x12` when the component's class does not derive from `PComponent`, and also when the
entity already has a component whose class is the same as, an ancestor of or a descendant of the new
one's, so an entity holds at most one component of each line of classes. Otherwise it removes the
component from its old entity (`006ACA70`), sets its entity and links it at the front.

`006ACA70(entity, component)` returns 5 when the component belongs to another entity; otherwise it
unlinks it from the list and clears its entity.

### The world-matrix registry

The entities are kept in an ordered tree headed by the six qwords at `01F2EB40` (root at
`01F2EB58`), keyed by world-matrix address. It is the same tree code as the asset-name registry of
the memory page: `0067F700` rebalances after an insert, `0067FE20` erases a node and `0067F6F0`
points a head's three links back at itself.

- `006ACAC0(entity, matrix)` erases the entity's node when it had a matrix, stores the new one and,
  unless that matrix is already registered, inserts the node with the matrix as key and the entity
  as value.
- `006ABF40(matrix)` walks the tree from the root and returns the entity, or null.
- `006ABEC0({object, class})` uses the object itself when its class is `PWorldMatrix` (`02E404B0`)
  or derives from it. Otherwise it looks up the class's `getLocalToWorldMatrix` method
  (`005A7B50`) and calls it through `006AB600`, which calls slot `+0x10` of the handler at the method's
  `+0x28` with the object and takes the matrix from the result. It then looks the matrix up like `006ABF40`.

### Loaded entities and components

Descriptor slot `+0x70` runs on each instance list a cluster load fixes up (the asset-file page). For
these classes it walks the list's objects, using the class's instance size (`+0x38` of the
descriptor) as the stride:

- `PEntity`: `006AB410` passes the list to `006ABFA0`, which inserts every entity with a world matrix
  into the registry, skipping a matrix already present.
- Components: `006AADD0` sets each component's class pointer `+0x10` to the list's descriptor. It is
  slot `+0x70` itself for `PTriggerReceiverComponent` (through `006ADD70`) and is called first by
  the `PAnimatableComponent` hook `005B80E0` (through `005A2610`) and by `006AFF00`.
- `PNameComponent`: `006AFF00` (through `006AFA70`) also links every name component at the front of
  the list headed at `01F2EB78`, through a `{next, previous}` node at `+0x18`.

### Instances components

`006AF4F0(component, &result, class)`, a method that `006AE350` registers for
`PInstancesComponent`, searches the component's array of 16-byte `{object, class}` pairs
(`+0x18` count, `+0x20` data) for the first pair whose class is the given class or derives from it,
and returns that pair. With none, or with a null class, it returns a null object with the `PBase`
descriptor (`02CF8270`, from `006372A0`).

### The object behind a physics body

`0069ECE0(collision object, record)` fills `+0x20` and `+0x28` of a physics callback record with the
gameplay object behind a Bullet collision object and its class: when bit `0x2` of the object's type
word `+0x104` is set, the pointer at `+0x108` with `PPhysicsRigidBody`'s descriptor (`02E48BD0`);
when the type is 4, the same pointer with `PPhysicsCharacterController`'s (`02E47ED0`). A null
pointer leaves both null. The physics functions `006A1A70` and `006A1DD0` call it.

## Layouts

`PEntity` (`0x38` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `void*` | m_firstComponent | first PComponent, or null |
| `08` | `void*` | worldMatrix | PWorldMatrix; the registry key |
| `10` | `void*` | left | registry node |
| `18` | `void*` | right |  |
| `20` | `u64` | parent | parent node; bit 0 is the node colour |
| `28` | `void*` | key | the world matrix again |
| `30` | `void*` | value | this entity |

`PComponent` (`0x18` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `00` | `void*` | next | next component of the entity |
| `08` | `void*` | entity | owning PEntity, or null |
| `10` | `void*` | classDescriptor | set by `006AADD0` on load and checked by `006AC300` |

## State

| Address | What |
|---|---|
| `01F2EB40` | head of the world-matrix registry; root at `01F2EB58` |
| `01F2EB78` | head of the list of loaded `PNameComponent` objects |
| `02E4EAF0` | `PEntity` class descriptor |
| `02E4E720` | `PComponent` class descriptor |

## Modding notes

- An entity accepts one component of each line of classes; adding a second component of a related
  class fails with `0x12` and changes nothing.
- The registry is keyed by the world matrix's address, so two entities sharing one matrix cannot both
  be found; only the first registered is kept.
- Changing an entity's matrix pointer directly leaves the registry pointing at the old matrix; use
  `setWorldMatrix`.

## Related

- [Phyre reflection](phyre-reflection.md): class descriptors, their slots and the instance lists these hooks walk.
- [Phyre asset files](phyre-asset-files.md): the cluster load that calls slot `+0x70`.
- [Memory and allocation](../Compiler-And-C-Runtime/memory-and-allocation.md): the asset-name registry built on the same tree.
- [Phyre Lua bindings](phyre-lua-bindings.md): the script method records these registrations fill.
