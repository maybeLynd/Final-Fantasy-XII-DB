# AR-5 — no vtable slot can be shown dead from the image alone

FABLE, Claude Opus 5.5, 2026-09-27. **NATIVE/STATIC. Nothing was executed.** Control: `ar5_dispatch.py` (4 checks,
FAILS 0).

**The question.** AR-5 asks whether any of the 7,185 table-reachable functions are dead vtable slots, never
dispatched at runtime. On 2026-09-16 I proposed a static half:
- count the slot indices that fixed-slot calls name;
- call the slots outside that set statically never dispatched.

**The result.** This package runs that census, and a second sound criterion, over every RTTI vtable. Neither marks
any slot dead.

- **A1, the population.** The 2,286 RTTI vtables (`rtti-class-vtables.tsv`), each walked while its qwords point into
  `.text`, hold 25,801 slots. They cover 6,886 distinct functions, at slot indices 0–76.
- **A2, every index is named.** Every slot index 0–76 is named by at least one fixed-slot dispatch,
  `call` or `jmp qword ptr [reg + 8k]`.
  - The 2026-09-16 count covered `call` only (6,070 sites, 87 indices) and saw gaps at 59, 63 and 73. Those three are
    tail dispatches through `jmp`: `00616E1B` `jmp [rax + 0x1d8]`, `00616E4B` `jmp [rax + 0x1f8]` and `00726F4E`
    `jmp [rax + 0x248]`.
  - The "long run from 77" of unnamed indices holds no slot, because no RTTI vtable is longer than 77 entries.
  - **So the index census cannot mark any slot dead.** A slot is dispatchable whenever some site names its index and
    the receiver can be of its class.
- **A3, every class is constructed.** A class whose vtable nothing installs would have dead slots. That does not
  happen here.
  - Every vtable address but three is referenced by code, through a rip operand or an image-base-relative
    displacement.
  - The three are referenced from data: `AdapterInfoBase` `00906868`, a Phyre `PClassDataMemberDynamicType`
    `00D58468`, and `SoundObjectManagerCallbackHandler` `01CB4328`.
- **A4, the other forms.** Two further kinds of indirect call exist:
  - 14 sites through an indexed or two-register address, for example `00179125`, `002AFCB1` and `003859FF`;
  - 24 calls through a pointer held in a stack slot.

  Neither can narrow the dispatched set further, since A2 already names every index.

**What would decide it, and why neither route is cheap.**
- **Statically.** A slot is dead only if no dispatch site that names its index can receive an object of a class
  holding that function at that index. That needs the receiver's possible classes at each of the ~6,270 fixed-slot
  sites: a points-to (type-flow) analysis over the whole image. No instrument here does that, and none is proposed in
  this record.
- **At runtime.** An observation can show a slot *is* dispatched, but never that it is not. "Never dispatched at
  runtime" is not a claim any capture can settle.

**The controls.**
- A2 must find the index-59 tail dispatch at `00616E1B`. This control is sensitive to the defect the 2026-09-16 count
  had: dropping the `jmp` form turns A2 into FAIL with 59, 63 and 73 unnamed.
- A3 must find the code reference to `PMotionBlur`'s vtable `00D62170`, which was decoded by hand.
