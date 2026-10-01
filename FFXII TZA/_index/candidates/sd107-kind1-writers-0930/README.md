# SD-107: the only store of 1 at `+0xA3` is a sound object's, and no traced element gets kind 1 (OPUS, 2026-09-30)

Register row SD-107 was registered by SWE2-DATA ([the-text-element-dispatch-table.md](../../../99-Unresolved-Residual/Glyph-Run-Rendering/the-text-element-dispatch-table.md)
section 8b). It asks whether anything instantiates text-element kind 1, whose emitter `002AA800` does not call the
control-code engine. `GJ-11` found that the cluster's plain byte writes to `+0xA3` store only 0, 2 and 3. A writer
outside the cluster, or a non-plain write of 1, was not ruled out.

This record is static. The checker is `sd107_kind1.py` (output `sd107_kind1.out`, `FAILS 0`). It sweeps every one of
the `pe` module's 38,161 bodies for stores of any width (byte to ymm) whose range covers `+0xA3` off a non-stack
base. **Status proposed: NARROWED** (see Limits).

## What the image shows (OPUS)

- **K1: one constant store of 1, anywhere.** 552 object stores cover `+0xA3`. Of every store with an immediate value,
  exactly one puts 1 into that byte: `007E7401 mov byte ptr [rcx + 0xa3], 1`. No wider constant store (word, dword,
  qword at `+0xA0`, `+0x9C`…) carries a 1 in that byte.
- **K2: that store is a sound object's.**
  - `007E73F0` writes three position floats (`+0x48`–`+0x50`) and then that byte.
  - It is called only from `007BFD00`, a sound-trigger parameter operation (the position one, per
    [sound-trigger](../../../18-Audio/Sound-Selection/sound-trigger.md)).
  - The object `007BFD00` passes is the return of `007B5070`, the sound-handle resolver. That resolver checks handle
    type 3 and indexes the table `02EAD610` (stride 0x28, live bit `+0x1C`, object `+0x20`).
  - So the object is a resolved sound handle, not a text element. This agrees with GJ-11's ownership reading, and
    now rests on the call chain as well.
- **K3: the text cluster writes no 1.** The neighbourhood is 174 bodies: the builders, dispatchers, emitters,
  handlers and the wrapper `002B32D0`, plus one hop of callers and callees. The only object stores covering `+0xA3`
  there are:
  - the four known kind writes (3 at `002A49CA`, 2 at `002B3470`, 0 at `002B3C40` and `002B3D78`);
  - one frame slot of `002B41F0` (below).
- **K4: stack elements keep their kind.** Eight builder calls construct an element in the caller's frame. In none of
  the eight holders does any store cover that element's kind byte (frame offset + 0xA3) apart from the builder.
- **K5: a ninth element, built without a builder.** `002B41F0` zero-fills a frame element (`memset(rbp+0x40, 0, 0xD0)`,
  covering `rbp+0xE3`) and fills its `+0x60` from `0039C4A0` as `002B3400` does. Nothing stores its kind byte, so it is
  kind 0.

**So:** no code path traced here writes 1 into a text element's kind, and the one instruction that stores 1 at
`+0xA3` acts on a sound object. Kind 1 (`002AA800`, the control-code-free emitter) stays wired but uninstantiated in
everything read.

**For modding:** a mod that wants control-code-free text would have to set `+0xA3 = 1` itself. The table and the
emitter already support it.

## Limits (OPUS)

- **Register-valued stores outside the neighbourhood.** They are classed by displacement only, and their values are
  not traced. 552 object stores cover `+0xA3`, most of them on unrelated structures at the same offset (GJ-11's five
  owner domains).
- **Elements embedded in containers.** For example, `+0x1550` of `0027AD70`'s object, `+0x60` of `00550A00`'s and
  `+0xE0` of `005528C0` / `0057C480`'s. They are written through their container at displacement `K + 0xA3`. Such
  stores are covered only where the container code sits in the neighbourhood.
- **Pointer-passed elements.** The builders' `mov rcx, reg` callers are not followed back to their allocation.
- **Copies.** A whole-element copy from a kind-1 source would need a kind-1 source first.
- **Static only.**

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's page.
