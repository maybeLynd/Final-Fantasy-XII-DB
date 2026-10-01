# T4 - DESCRIPTOR-LISTS (BL-8): inverted inserter census for PClassDescriptor +0x60 and +0xB0

FABLE reader, 2026-09-29. Static only.
- Script: `t4_desc_inserters.py`, run as `python t4_desc_inserters.py > t4_desc_inserters.out`. Helpers are in `tk.py`.
- Static descriptor seeds: `_index/candidates/bl8-b0-nas-review-opus/descriptor-statics.txt` (315 objects).
- I read BL-8 first. The routes already closed are the displacement census, the tag reconstruction, the parent-pairing census, three insert shapes (2026-09-25), the sentinel-walk census, and OPUS's `b0_head_stores.py` / receiver-typed census.

## Method: search by what an insert must do, not by where it writes
Every insertion into a circular doubly-linked sentinel list, in either direction, makes the same two stores:
- `[N + a] = H`, the head's address into the node;
- `[H + b] = N`, the node's address into the head;
- with a, b in {0, 8} and N != H.

How the census applies this:
- It decodes every listed function linearly and gives each register write a version number; a call clobbers the volatile registers.
- A value is either a register version or, when the register came from `lea rip`, an absolute address. rip-relative stores target absolute addresses.
- It looks for every pair of stores with that signature.
- It then classifies the head H by how it was formed: `lea [B+D]` (inline insert at list offset D), an absolute address (static head), an unmodified entry argument (a **head-insert helper**), or a load from memory (unlink or relink, counted only).

Three further passes:
- **Helper resolution.** For every detected helper, each raw E8/E9 call site is resolved for the head argument.
- **Forward value census.** Every `lea r, [B + D]` whose register value is stored to memory other than its own self-link (a head address that escapes), or is passed at a helper's head argument.
- **Static initialisation.** Every DIR64 relocation whose value is S+0x60/+0x68/+0xB0/+0xB8 for a static descriptor S.

Typing a static head: the object must be one of the 315 static descriptors, or an object with inline static inserts at two or more of its filled lists (+0x80, +0x90, +0xA0).

## Positive controls (all found; see the .out file)
- **Known inserter on a list of the same shape, inline:** `0062EFD0`, the +0x80 data-member insert. Its pair `0062F051` / `0062F059` is found.
- **Known rip-formed inserter:** `00635980` into PNamespace's descriptor +0xA0 (head 02CF8A20, stores `006359FB` / `00635A13`). The same function's +0x90 insert (02CF8A10) is found too, and PNamespace 02CF8980 is typed as descriptor-shaped.
- **Known head-insert helper:** `006B67D0`, the annotation add, is detected with its head in rcx. All 70 of its call sites resolve to an absolute head.
- **Counts agree with the published census:**
  - register-formed pairs at +0x90: 206 (in 44 functions), against 205 published;
  - at +0xA0: 11 (in 8 functions), against 11 published;
  - at +0x80: 1 (0062EFD0).
  - The forward value census at +0x90 finds 212 sites in 50 functions.

## Results
- **Pairs by head class:** load 908, lea 259, static-head 469, helper 39, call 25, other 10.
- **Inline register-formed inserts with D = +0x60, +0x68, +0xB0 or +0xB8: 0.** The D values found are 0x8, 0x10, 0x18, 0x28, 0x38, 0x50, 0x80, 0x90, 0xA0, 0xD0 and 0x1A8.
- **Static (rip-formed) heads at +0x60/+0x68/+0xB0/+0xB8 of a descriptor-typed object: 0.**
- **Helpers: 15.** Their call-site heads:
  - `006B67D0`: 70 of 70 sites resolve to absolute heads, none at +0x60/+0xB0 of a typed descriptor. BL-8 records all 70 as data-member +0x38.
  - The other 14 helpers resolve to `[rbp-0x18]`, `[rsp+0x20]`, `[rsi+0x118]`, `[r15-0x10]` and absolute 02EBB6A0. None is +0x60 or +0xB0.
  - **21 of their call sites stay unresolved** within a 30-instruction backward slice ('?' or a head loaded from memory). They are in 001BC950, 001D9FD0, 00217F10/002181A0/00218380/0021CE30, 002E65A0/002E6D60/002E6A80, 002E3DC0..002EEB20, 002EB5E0, 003EB190/003EB6C0/0050E370, 00714DC0/0071F590 and 0079BA10. None is in the reflection band 0059xxxx..006Bxxxx.
- **Forward value census:** 4 sites at +0x60 and 5 at +0xB0, **all read, none a descriptor**:

| site | what the base is |
|---|---|
| `001B6CE0` (`001B6D0A`), `0060DF70` (`0060E3DD`) | cursor `{owner, …, &owner+0x60}`. Owner's `[+0]` is read as a dword count with bit 31 as a flag (`0060DF88`/`0060DF8F`); a descriptor's `+0` is a vtable |
| `001D9FD0` (`001DA02D` -> helper `001DA0F0`) | a Resource-band object (+0x30/+0x38 queue fields), with the `cmp [rdi], rdi` empty test at `001DA008` |
| `0041E3A0` (`0041E3E5`) | `RenderResourceRoot`, its own +0x60 stored at +0xD98; the object is larger than a 0x140 descriptor |
| `001A5B30` (`001A5B92`) | stack local; the object also has +0x448 |
| `00602EA0`, `0060B980` | already ruled out by OPUS's negative 1 (stack frame; object read at +0x220) |
| `0079AF20` (`0079AFE7`) | an object reached through list 01F401E8 with node at +8. It sets its own +0x58/+0x60 as internal pointers, which would clobber a descriptor's +0x50 registry node |
| `0081EAA0` (`0081EAFC`) | **Lua 5.1 `luaF_findupval`**: walks the null-terminated open-upvalue list at L+0x60, allocates type 10 / 0x28 bytes (`0081EADB`/`0081EAE8`, UpVal), and links it into `g->uvhead` at `global_State + 0xB0` (rdi = `[L+0x18]`, `l_G`) |

- **DIR64 relocs to static descriptor +0x60/+0x68/+0xB0/+0xB8: 0.** This route has **no positive control**: the same test at +0x80/+0x90/+0xA0 also returns 0, because the static records are linked at run time. So this zero proves nothing.

## Conclusion
**Nothing in the listed code inserts into a PClassDescriptor's +0x60 or +0xB0 list.** This holds for:
- inline register-formed inserts;
- inline rip-formed inserts on typed static descriptors;
- all 70 calls of the one head-insert helper that serves the reflection band;
- every head address at +0x60/+0xB0 that escapes to memory.

The same instrument finds the known inserts of the +0x80, +0x90 and +0xA0 lists, and the rip-formed insert into PNamespace's +0xA0 and +0x90. This agrees with BL-8's current disposition, and it closes the route BL-8 listed as not swept: "other head-insert helpers".

## Limits
- 21 call sites of 14 non-reflection helpers have heads the slice could not resolve. They are outside the reflection band but not proven non-descriptor.
- A head address held in memory and reloaded more than 40 instructions after its `lea`, or formed by arithmetic other than `lea`/`add`, is not followed.
- Only code in the function list is covered; the pair search does not use the raw .text sweep.
- Static typing relies on the 315-object list plus the two-filled-lists rule. A static descriptor with neither is untyped. The 315 list overlaps none of the 4 objects that have rip-formed inserts, because those descriptors link through constructor arguments.
- The live head read on loaded-field descriptors (BL-8's closing step) remains the stronger test.
