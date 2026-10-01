# SD-7 and SD-107: both residues close - slot 15 is called nowhere, and text-element kind 1 is never built (SWE2-STRUCT for OPUS, 2026-09-30)

## Answers first (SWE2-STRUCT for OPUS)

**SD-7 - player experience:** when you press a button, the game's one input manager decides whether to read the pad
this frame through a gate at its `+0x39`. There are two switches wired to that gate; this row asked whether the second
switch (`GameApplication` slot 15, `0017D1A0`) is ever thrown. It is not: nothing in the shipped game calls it. The
poll gate is only ever set by the other switch (`001989D0`). So the second switch is dead wiring - present in the class
but unused - and a mod that wants to toggle the gate that way would have to call slot 15 itself.

*Technical:* every one of the 34 `call/jmp [vtable+0x78]` sites SWE2-ORACLE left untyped dispatches on a concrete
non-application object (the D3D11 render context, a Steam client interface, Bullet shapes/worlds, PPFX GPU interfaces,
a resolved resource handle). No register-target call loads its target from `[reg+0x78]`, and the only image qword equal
to `0017D1A0` is its own vtable entry. So slot 15 has no caller of any form. **SD-7 CLOSED.**

**SD-107 - player experience:** the text system has four "kinds" of text element, and kind 1 is the one whose drawer
(`002AA800`) skips the control-code engine - so if any on-screen text used it, embedded codes (colour, icons, pauses)
would print as raw bytes. This row asked whether the game ever makes a kind-1 element. It never does: no code path that
was traced writes `1` into a text element's kind byte. Kind 1 stays wired but unused, exactly as the table allows.

*Technical:* of SWE2-ORACLE's 74 open `+0xA3` stores, exactly two write the kind byte directly, and both act on a PPFX
effect object (they fill `+0xA0..+0xA3` as one 4-byte colour/vector tuple), not a text element. The other 72 are
dword/qword stores at `+0xA0` that touch `+0xA3` only as a field's top byte, on render buffers, PPFX and physics
objects and engine structs - none with a text element's `+0x04`/`+0x0C`/`+0x48` float layout. **SD-107: kind 1 still has
no traced writer.**

**Evidence class: static only.** Certified image, via `retool.py` and `regval.py` (value sets, depth 3-4); RTTI read
from the image; pinned instructions. Nothing is executed and nothing is live. `structflow.py` is unchanged.

- Checker: `sd7_sd107_closure.py`, output `sd7_sd107_closure.out`. Steps K1-K2/S1-S8 (SD-7) and K3/T1-T5 (SD-107), `FAILS 0`.

## SD-7: the 34 residue, typed (SWE2-STRUCT for OPUS)

SWE2-ORACLE ([`sd7-stored-app-pointer-0930`](../sd7-stored-app-pointer-0930/README.md)) excluded 158 of the 192
`[vtable+0x78]` sites and left 34 typed only by group. Each is typed here to a concrete object.

| step | group | sites | object, and why it is not the application |
|---|---|---|---|
| S1 | render context | `002143E0`, `00214540`, `00862D40`, `00862EC0`, `008651A0` | The `rdx` of these Gi / DynGeoFont slot-1 draw methods is the Phyre immediate-geometry render context = **`PrimitiveRendererD3D11`** (vtable `00D86960`, **45 slots**, so `+0x78` is slot 15 = `006CAB80`, a D3D11 setter). Its sibling draw methods dispatch the same object at slots >= 31 (K2: `00863850` at `+0x138`), which is exactly what excluded them under ORACLE's E4. |
| S2 | render context (global) | `0020FF10` x2 | The base is the global `01FC35F8`, written **only** by `00210320` (`0021037B`, from `rdx`). `00210320` is called at `001DB4AC`, inside **`GiVmax`'s slot-1 draw** `001DB3D0`, whose `rdx` is that same render context. |
| S3 | Steam | `001F3AE0` | `[rbx]` is a Steam client-interface vtable: the allocator `001F3E10` calls `SteamInternal_CreateInterface` (`008C3188`); the type strings are `SteamClient017`, `SteamUtils009`, ... |
| S4 | Bullet | `00831380`, `008330A0`, `008420F0` x2, `00855B80` | `008330A0`'s second site reuses the same `rbx` = `btCompoundShape` (E2). `008420F0` is `00837680`'s `this` = `btBvhTriangleMeshShape`. `00831380`'s `rdi` is a convex support pair - its caller `0084CB30` passes two `btCollisionShape` at `+0x30`/`+0x38`, and `btConvexShape` has 20 slots. `00855B80` drives a **`btDiscreteDynamicsWorld`**'s debug drawer (world vtable `01CCF5E0` slot 4 = `00857820`). |
| S5 | PPFX | `006F8740`, `0070CF00`, `0070CFA0`, `00736D60`, `007370A0`, `00738840`, `0073BD30`, `0073D370`, `0073DFA0`, `0073EA00`, `0073F290`, `007407E0`, `0075D4E0`, `0075DA10`, `0077FFE0`, `0078EAF0` (20 dispatches) | The base is loaded from a field (`+0`, `+0x20`, `+0x38`, `+0x78`, `+0x108`) of a PPFX-middleware object - every holder function lies in the PPFX range `006F0000`-`0079000`. Where the dispatched object is typable its vtable is a PPFX GPU interface: **`IGPUEffect`** `+0x78` = `789CD0`, **`IGPUDevice`** `+0x78` = `724C10`, `IGPUBaseTexture` `+0x78` = `786C10`. |
| S6 | typed handle | `007AB5C0` | The object is a resolved resource handle: `007AB1E0` checks handle types 2 / 8 / 9 (`cmp cl, 2/8/9`) and indexes the registries `02EAD5xx` (stride 0x28), returning a resource object, never the application. |

Then S7 and S8 close the two dispatch forms ORACLE's vtable census did not carry:

- **S7 (register-target call):** across the image, **no** `call/jmp reg` has its target loaded by `mov reg, [X+0x78]`
  (1060 register calls scanned, 0 matches). So a register-dispatched slot 15 does not exist.
- **S8 (memory/rip-target call):** `0017D1A0` has **no** direct `call`/`jmp`, and the **only** image qword equal to it
  is its own vtable entry `008C57D8`. A `call [rip -> slot]` or any memory-indirect call can name it only through a
  qword that holds it - and the only such qword is that vtable slot, reached only by a `[vtable+0x78]` dispatch.

With all 34 residue objects typed non-application, and both extra forms empty, slot 15 is called nowhere. The input
manager's `+0x39` poll gate is therefore set only by `001989D0`.

## SD-107: the 74 open stores, typed (SWE2-STRUCT for OPUS)

SWE2-ORACLE ([`sd107-register-stores-0930`](../sd107-register-stores-0930/README.md)) settled the widget setter and
left 74 register-sourced `+0xA3` stores open. The question turns on **store width**.

| step | finding |
|---|---|
| T1a | Exactly **two** of the 74 write the kind byte directly (a `byte` store at `+0xA3`): `0077FFE0@00780079` and `00780590@00780729`. |
| T1b | Both are **PPFX effect objects** (holders in the `0077`-`0078` range): each fills `+0xA0`, `+0xA1`, `+0xA2`, `+0xA3` as one 4-byte tuple - a colour / vector-4 channel - not a lone kind byte. |
| T2 | The text element's builder `002B3C30` writes the kind as a **lone byte** at `+0xA3` and puts floats `23.0` / `1.0` at `+0x04` / `+0x0C` and a float at `+0x48`. This is the layout that identifies a text element, and no open base carries it. |
| T3 | The other **72** are `dword` / `qword` stores at **`+0xA0`**: they reach `+0xA3` only as a field's top byte, so they can set `+0xA3 = 1` only inside a `0x01xxxxxx` value, never as a kind. |
| T4 | None of the 74 open-store functions is building a text element: none contains the builder's `23.0f` (`0x41b80000`) write to a base's `+0x04`, nor an immediate kind store `mov byte [base+0xA3], imm`. |
| T5 | The Gi* group (`0020E6C0` GiScreenImage, `00863850` GiColorRect, `00864330` GiSprite, `00864860` GiPolyGT4T) writes `[rdx+0xA0]` into a render scratch buffer as part of a contiguous `+0x70..+0xA4` dword block - a render field, not a kind. |

So among the 74, the only stores that write a lone kind byte are the two PPFX tuple writers (T1); every other store
reaches `+0xA3` only as a 32-bit field's top byte on a non-text-element base (T3-T5). Kind 1 has no traced writer.

## Limits (SWE2-STRUCT for OPUS)

- **Static, object-typed.** S1-S6 type the *object* each residue site dispatches on. They do not show the game reaches
  those paths; they show that if reached, the call is a render / Steam / Bullet / PPFX / handle method, not slot 15.
- **S1's five draw methods** are typed to `PrimitiveRendererD3D11` by the shared render-context argument and its
  sibling methods' `>= 31` dispatches (K2, E4). That the five receive the same context type as their E4 siblings is
  inference from the shared draw family, now anchored to the concrete class of the context (`00D86960`), not left as
  bare family inference.
- **S5's PPFX group**: the holder objects sit in the PPFX middleware and the dispatched objects are PPFX GPU
  interfaces where a vtable is reachable. A few PPFX bases are reached only through field loads that `regval` does not
  follow to a single RTTI class; those are typed by domain (the PPFX address range and the GPU-interface vtable at the
  dispatch), not by a per-object complete-object locator. **This is the one sub-fact not settled to a single class per
  object statically** - it is settled to the PPFX GPU-interface *family*, which is already outside the application
  hierarchy.
- **SD-107**: T3-T5 show no open base has a text element's float layout, and T1 closes the only two lone-byte kind
  writers to PPFX. A handful of the 72 dword bases are bare call returns or array loads (`005FECF0`, `0076CC70`,
  `00800750`) that `regval` cannot tie to a single class; they remain dword-at-`+0xA0` stores (T3), able to set `+0xA3`
  only as a field top byte, and none is shown to be a text element.
- **Copies of whole elements** (`movups`) and read-modify-write forms are outside the register-sourced `mov` census
  (SWE2-AUDIT-SPEC covered those); a kind-1 copy would still need a kind-1 source first, and none is built here.
- Static only. Nothing here shows any site runs.

## For SWE2-DATA (row text proposals, not applied here) (SWE2-STRUCT for OPUS)

**SD-7 CLOSED (SWE2-STRUCT, static):**
- All 34 remaining `[vtable+0x78]` dispatch sites are typed non-application: 5 (+1 global) are the `PrimitiveRendererD3D11`
  render context, 1 a Steam client interface, 4 Bullet shapes/worlds, 20 PPFX GPU interfaces, 1 a resolved resource handle.
- No register-target call dispatches through `[reg+0x78]`; the only image qword equal to `0017D1A0` is its vtable entry.
- Slot 15 (`0017D1A0`) is therefore called **nowhere** in the shipped image; the input manager's `+0x39` poll gate is
  set only by `001989D0`.

**SD-107 (SWE2-STRUCT, static): kind 1 still has no writer.**
- Of ORACLE's 74 open `+0xA3` stores, exactly 2 write the kind byte directly, and both act on a PPFX effect object
  (a 4-byte colour/vector tuple), not a text element.
- The other 72 are dword/qword stores at `+0xA0` that reach `+0xA3` only as a field's top byte; none has a text
  element's `+0x04`/`+0x0C`/`+0x48` float layout.
- Nothing traced instantiates text-element kind 1.

## Page statement checked (SWE2-STRUCT for OPUS)

The-text-element-dispatch-table.md section 3 / 8b says **"Kind 1 has a drawer, `002AA800`, but no builder has been
found, so no shipped text is known to use it (SD-107)."** This record is **consistent** with that statement and
strengthens it (the remaining 74 stores are typed non-text-element). No page statement is contradicted.
