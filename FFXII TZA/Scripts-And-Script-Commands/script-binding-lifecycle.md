---
title: "Script binding lifecycle: a model binding from the script that names it to its release and the slot's reuse"
kind: "lifecycle"
category: "Scripts and script commands"
addresses: "0x002EB540, 0x002EAE20, 0x002E25E0, 0x002E6700, 0x002EAD50, 0x002E4D20, 0x002EA6E0, 0x002E28E0, 0x002E3110, 0x002EAEB0, 0x002E65A0, 0x002E9360, 0x002E6D60"
---

## What the player sees

When a scene gives a character a different body or hands an actor a prop, the scene can pause a moment while the
model loads. When nothing uses the model any more it is unloaded, and a later scene that names it loads it again.

## Stages

1. **Find or create.** A bind verb names a bound id. `0x002EB540` or `0x002EAE20` finds its entry on the live or the
   requested list, or pops a free one (`0x002E25E0`) onto the requested list, and sets the caller's holder bit
   ([script name bindings](script-name-bindings.md#find-or-create-holders-and-the-reference-count)).
2. **Load.** The request pump `0x002E6700` sizes the model's file, takes a buffer and files the read (`0x002EAD50`);
   the entry moves to the live list ([script name bindings](script-name-bindings.md#loading-an-entry)).
3. **Ready.** The completion `0x002E4D20` registers the model with the render system, and `0x002EA6E0` loads up to
   three sub-resources; when they are in, the ready bit is set, which every wait tests
   ([script name bindings](script-name-bindings.md#loading-an-entry)).
4. **Held.** The bind `0x002E28E0` and the attach `0x002E3110` each add a reference
   ([script name bindings](script-name-bindings.md#the-bind-what-binding-a-model-to-an-actor-does),
   [script name bindings](script-name-bindings.md#the-attach-slots)).
5. **Let go.** When the holders and references are gone and the entry is not pinned, the re-lister `0x002EAEB0` moves
   it to the retired list, or, while it is still loading, marks the release to happen when the load completes
   ([script name bindings](script-name-bindings.md#find-or-create-holders-and-the-reference-count)).
6. **Freed.** The per-frame binding update `0x002E65A0` releases retired entries from the oldest: `0x002E9360` queues
   the entry's lanes for unload, releases its sub-resources and buffer, and pushes the entry on the free list
   ([script name bindings](script-name-bindings.md#the-per-frame-binding-update)).
7. **Under memory pressure.** When an allocation in arena 6 or 10 fails, `0x002E6D60` unloads one queued lane and
   releases the oldest retired entry before the arena compacts and retries
   ([script name bindings](script-name-bindings.md#the-per-frame-binding-update),
   [resource arena and relocation](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md)).
8. **Reuse.** The stamp rises when the entry is retired and again when it is freed, so a handle given out before
   stops resolving ([script name bindings](script-name-bindings.md#the-handle-one-number-checked-before-use),
   [identifier spaces](../Engine-Core/identifier-spaces.md)).

## Across transitions

- **An area unload** runs the per-frame binding update itself (`0x002628B0` is one of its callers), so retired
  entries are freed as the zone goes ([script name bindings](script-name-bindings.md#the-per-frame-binding-update),
  [changing areas](../World-Areas-And-Travel/changing-areas.md)).
- **A pinned entry** (pin bit `0x1` or `0x2`) is never released: its count is clamped to 0 instead
  ([script name bindings](script-name-bindings.md#find-or-create-holders-and-the-reference-count)).
- **A retired entry whose buffer handle is 0** is not passed to `0x002E9360`; it ends on no list and its slot stays
  lost until the binding table is set up again
  ([script name bindings](script-name-bindings.md#the-per-frame-binding-update)).
- **The 129th binding** at once has no free entry, and both finders write through the null pointer
  ([native limits](../Engine-Core/native-limits.md)).

## Related

- [Script name bindings](script-name-bindings.md): the binding table in full.
- [Model asset list](../Graphics/model-asset-list.md): what a bound id names.
- [Character render records](../Graphics/character-render-records.md): where the bound model is drawn from.
