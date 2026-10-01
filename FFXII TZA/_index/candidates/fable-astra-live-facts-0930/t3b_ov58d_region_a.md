# T3b - OV-5 / OV-8 (d), bounded remainder: load copy, post-load clamp, snapshot restore, controlled sweep

FABLE reader, 2026-09-29. Static only.
- Script: `t3b_regionA.py`, run as `python t3b_regionA.py > t3b_regionA.out`. Result: FAILS 0. The helpers are in `tk.py`.
- Region A is 021B7054..021B781B. That is active image 02164280 + 0x52DD4..0x5359B, or state 021B290C + 0x4748..0x4F0F.
- As asked, the 318-load pointer-flow census was skipped. Its gap still bounds the conclusion (see Limits).

## 1. The load copy: save-file bytes into 02164280
- **The only kind-9 storage packet is built at `0058111E`** in `SaveLoad_ControllerTransitionStateMachine`:
  - `005810BC call 002EF640`: the destination is the active image getter.
  - `005810EA` kind 9; `00581113` +0x48 destination = rsi; `00581117` +0x50 size = 0x56690.
  - The script checks every `SaveStorageQueue_EnqueueOperation` site for a kind-9 immediate: exactly one.
  - The coordinator's "op 9" is this queue kind. `SaveSlotTransaction_StateMachine` 00581DA0 has only ops 1..8 (jump table 00582020). Its op 8 enqueues queue kind 8 at `00581F51`.
- **Dispatch.** Queue table 0058220C, slot 9 is `0058218A`, which calls `003BB440`.
  - That function stores the destination at `003BB477` (02B40EF0) and the size at `003BB47E` (02B40EF8), then arms the pipeline.
- **The read.** Pipeline `003BA7B0`, states 6 and 15, calls `00862590` at `003BA882` / `003BA8AE` with rdx = [02B40EF0] and r8d = [02B40EF8]. That calls `00866A00` at `008625A4`.
- **The byte copy that writes region A is `00866A4D mov byte [r10+rdi], dl`.** It reads each byte at `00866A46` from the backing store `[01F44D40]`, which the open `008666B0` fills.
- The copy covers 0x56690 bytes, the whole image including region A, and it copies without looking at the data.
- Not traced: whether the container transform decodes the file before it reaches the backing store. That changes the encoding, not the fact that file-supplied words land in region A as they are.

## 2. Is there a clamp or re-validation of region A after load?
**No.** The call trees (depth 3) of `00238A80`, `0030B6A0` and the post-load lazy body `00233C10` were scanned for anything that could write region A:
- a reference to the registry;
- a store at displacement 0x4748..0x4F0F;
- a call to the handler, 003008A0, 003047F0, 002370C0, memset/memcpy or the full image resets.

Control: the same scan rooted at `0023AF50` finds 002370C0 and 003008A0.

What the scan found:
- **`0030B6A0` (the rebase)** only rewrites the registry pointer cells (`0030B6CB`/`0030B6DC`/`0030B6ED`). It then clears state +0x57C8..+0x59C7 (`0030B710` loop) and masks bytes at +0x59C8..+0x5A47 (`0030B750`). **It does not touch region A.**
- **`00238A80`'s only entry is `002EF650`** (`jmp` at `002EF67D`). That is the reset compound, which first zeroes the whole image (`002EF663`).
  - So 00238A80 is a reset path. If it ran after a load, it would erase the load rather than validate it.
  - Its tail `00237DF0` re-initialises the inventory: `0023AF50` -> `002370C0` memset, then authored adds through `00300BA0` -> `003008A0` -> the handler.
- **`00233C10`**, when the state pointer is already set, tests the magic `cmp dword [state], 0x5071901` (`00233C4D`).
  - Mismatch: it tail-jumps to `00237DF0` (`00233C59`), which is the same full inventory re-init: zero, then authored contents.
  - Match: the branch `00233C5E`.. touches only state +4, +0x5B00, +0x5B0C and +0x5B0E, then calls 00327F80, 003139A0, 00304770 (+0x5AE0), 002FA230, 002FA260 and 00229ED0. The scan finds no region-A writer shape in any of them.
- **So a loaded image with a valid magic keeps its region-A words exactly as the file supplied them.** The only post-load action on region A is a full zero-and-re-author, and it runs only when the magic is invalid.

## 3. 0030FAA0 (restore) / 0030FBE0 (snapshot)
- **No direct store to region A in either function.**
  - `0030FAA0` has no non-stack store. Besides its calls, it memsets the backup +0x4F84..+0x57BF (`0030FBC7`).
  - `0030FBE0`'s state stores go only to the backup: `0030FC6F` +0x4F84 (copy of +0x4748) and `0030FCCF` +0x5004 (copy of +0x47C8). Its other two stores, `0030FC24`/`0030FC29`, go to a battle-stats record at `[rax+0x5A]`/`[rax+0x62]`, where rax comes from `00320AB0`.
  - Its displacements 0x4748 / 0x47C8 are reads (`0030FC67`, `0030FCC7`).
- **The restore reaches region A only through the handler.**
  - It calls `003008A0` with edx = the full backed-up word (movsx, `0030FAE7` / `0030FB37`), r8d = 0 and r9d = 1.
  - `003008A0` bounds `id & 0xFFF` against descriptor +0x3C (`00300920`..`00300927`), then calls `[descriptor+0x48]` (`00300943`/`00300960`), passing r8d/r9d/edx through.
  - Rows 0, 1 and 2 (classes 5, 6, 7) hold `002FD150` at +0x48 in the file (reloc slots 01EEBD08, 01EEBD60, 01EEBDB8). No rip-relative store into the registry exists, and the rebase writes only +08/+20/+30/+40.
  - In the handler, r9d = 1 is the channel-1 arm `002FD2AD`, and r8d = 0 means relative. The new total is clamped to [reserved, 99] (`002FD2E9`/`002FD2EC`, `002FD2F5`/`002FD2FA`). Only the low 10 bits are stored (`002FD30B`..`002FD31A`).
  - A backed-up word that carries reserved bits becomes a large (or, with bit 15 set, negative) delta. It saturates at 99 (or at reserved), but it **cannot create reserved > total**.
- The snapshot's own calls use r8d = 1 (absolute), r9d = 1 and edx = 0, so the total is set to max(0, reserved). That is clamped too.

## 4. Controlled sweep of region A
| sweep | result | control |
|---|---|---|
| image-base-relative disp 0x2097054..0x209781B, any base or index | **0** (and 0 unverified byte matches) | `002DF7BF [r15+rbx*8+0x203f000]` found (PASS) |
| image-base-relative into the whole image 02164280..021BA90F | 0, so no in-block control exists | the out-of-block control above |
| rip-relative accesses overlapping region A | 0 | the same detector found the six references in T1 |
| absolute-VA forms | 0 | `001A14E6` imm32 found |
| stored qword pointers into region A | 0 | vtable 01CB2508 (T1/T2) |
| bulk control | `002370D3` memset([02EBF190] = image+0x4E68C, 0, 0x7410) covers image 0x4E68C..0x55A9C, which contains region A (PASS) | - |

## Conclusion
**Region A is written by:**
- the packed handler `002FD150`, which clamps (`002FD298`, `002FD31A`, `002FD3F1`), including every call routed through `003008A0` such as the snapshot restore `0030FAA0`;
- the zeroing loop `0030482A` (in `003047F0`);
- the state memset `002370D3` (in `002370C0`);
- the full-image memsets `002EF603` and `002EF663`;
- **the save-load byte copy `00866A4D`** (kind-9 packet from `0058111E`, via `003BB440` -> `003BA7B0` -> `00862590` -> `00866A00`).
- *(added 2026-09-30, FABLE, on SWE2-AUDIT-SEM's contradiction and OPUS's census [`ov58d-pointer-flow-0930`](../ov58d-pointer-flow-0930/README.md), `a67cad059`:)* **the post-load mirror copy `002EF4A0`** (`00233C10` -> `00235AF0`), which copies the mirror `02166480` (image + `0x2200`, `0x6000` bytes) over the state `021B290C` on every post-load. The mirror is filled only by the state-to-mirror copies `00229B40` / `005844A0` (`0xC0` x `0x80` from image + `0x4E68C`), the whole-image zero fills `002EF5F0` / `002EF650`, and the save file's own bytes. The controller backup `00583CB0` / restore `00583C00` (buffer `[02CA99B8]` + `0x588`, `0xE240` bytes, allocated by `00582860`) carries the image head.

Of these, the only writer that can store an arbitrary word is the save-load copy. Nothing re-validates region A after a load whose magic is valid. ~~**So over-reservation (high6 > low10) can enter only through save-file bytes, loaded by `00866A4D`.**~~ *(corrected 2026-09-30, FABLE, on the census above:)* **So over-reservation enters region A only from save-file bytes, by the file's region-A words or its mirror words through `002EF4A0`; the unbounded indexed-writer residue is routed to SWE2-STRUCT and is a limit of this claim.** In-game mutation always goes through the clamp or writes 0.

## Limits
- The 318-load / getter pointer-flow census (T3 gap 1) was not run. A writer that reaches region A through a pointer passed along an unfollowed path is not excluded.
- The sweeps above exclude every direct addressing form. The bulk table resolves only part of the 1,622 bulk sites.
- The handler itself does not bound `id & 0xFFF`; `003008A0` does. A direct handler caller with an out-of-range index would write a neighbouring word, but still with clamp semantics.
- The post-load scan is depth 3 and linear. It cannot see what the file transform in `008666B0` does to the bytes.
