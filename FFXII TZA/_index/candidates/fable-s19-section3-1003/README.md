# S-19 separation contract, section 3: OPUS's five points read at the bytes (FABLE, 2026-10-03)

*Answers `OPUS-REQ-FABLE-S19-SEPARATION-CONTRACT-1003`, routed from OPUS's re-cut of the MovementBody rows
([record](../opus-l2-s19-recut-1003/README.md), [`s19_recut.json`](../opus-l2-s19-recut-1003/s19_recut.json)). Section 3
of [`CONTRACT-separation-pass.md`](../../../06-Movement-And-Navigation/CONTRACT-separation-pass.md) is mine. I read each
point at the instruction sites, and I ran a whole-image census of the fields before writing any "only" or "never".*

| point | field | OPUS says | FABLE's verdict |
|---|---|---|---|
| 1 | `+0x120` | a u32 cell set, not u128 | **right** |
| 2 | `+0xE8` | the partner's increment, squared, overwritten per contact | **right**, and it has one reader, which OPUS did not list |
| 3 | `+0x08` | f32, not "?" | **right** |
| 4 | `+0x104` | never accessed alone, so its role is not forced | **partly right**: true inside the pass, false image-wide |
| 5 | `+0xEE` | "immovable" is a label; the byte marks "this body took the whole share" | **right** |

The staged edit is [`apply.py`](apply.py), shown in [`apply_dryrun.out`](apply_dryrun.out). It makes five strike-and-replace
edits in the contract's section 3 and three in my pool page, which restates two of the old readings. The checks are in
[`check.py`](check.py), with output in [`check.out`](check.out).

## How FABLE read the fields: a census first (FABLE)

`check.py` part A walks every function unit in the image: each `.pdata` root with its chained entries, plus the leaf runs
between them, split at `int3`. It follows a body pointer from four sources:

- the pool base `02B4E4C0` combined with an index times `0x130`;
- a qword load from `[X + 0x138]`, where `X` was loaded from `[Y + 0xC0]` (the actor's secondary context) in the same
  function;
- the allocator's return value;
- the two arguments of the resolver callback, which the visit calls through a register.

A fixpoint then follows every callee that receives a body-derived pointer, with its offset. That is how the cell routine
called at `003DB020`+0x48 shows up with its `rcx` at body `+0x120`. Within a function the pass runs forward in address
order and takes the union at branch targets.

**What it found** (copied from `check.out`): `units 36732; self-seeded 142; records 789 in 131 functions; body-chain
(pool/ctx138/cb/ret/arg) records 418 in 73 functions`.

**The census control passes.** It reaches one known site for each source class and each corrected field: `003DA98E`,
`0026861A`, `002E5227`, `002E53B4`, `002E53F1`, `00315263`, `00315303`, `0031533F`, `003DACAF`, `003DB078` and
`0046AF4A`.

**Excluded loads.** A `+0x138` load whose base is not a secondary context (`p138`) is held apart. Fourteen such roots
reach the corrected offsets. Each one is dispositioned in `check.out` by where its base register comes from:

- four are frame pointers (`lea rbp` off the stack pointer, directly or through `mov rax, rsp`);
- two are a global object of the item code;
- two are a widget pointer table with sibling slots at `+0x128` / `+0x130` / `+0x138`;
- six are the map-screen, license-board and SEAD sound-driver objects, or a stub's `rdx`.

Their accesses would contradict the body layout in any case: qword reads of `+0x08`, integer `and`/`or` on `+0x08`, and
qword pointers at `+0xE8` and `+0x100`.

**Where the census stops.** A body pointer reaches non-stack memory in only two places:

- the creator's store into the context (`002E3546`);
- the placement-list links of body `+0x30`, written by `003DB0D0`.

The second is the `0xB0`-byte placement record `+0x30`..`+0xDF`, which the allocator clears (`003DA947`, `003DA94D`). It
ends before every field corrected here.

**Residue.** The census does not follow a body pointer that reaches a function through some other memory cell or another
indirect call. So "the one reader" below means the one reader this census finds.

## Point 1: `+0x120` is a u32 cell set (FABLE): OPUS is right

- **Registration reads it as a dword.** `003DB020` passes `lea rcx, [rdi + 0x120]` to the cell routine (`003DB052`,
  `call` at `003DB020`+0x48). It then reads `mov edx, dword ptr [rdi + 0x120]` (`003DB078`) and walks it one bit at a
  time: `test dl, 1` / `or [rcx], r8` / `add rcx, 0x10` / `shr edx, 1` / `jne` (`003DB0A3`–`003DB0B1`). Each bit
  selects one 16-byte mask at `02B57CE0` (`lea` at `003DB094`).
- **The walk reads it as a dword too.** `mov ecx, dword ptr [rbx + 0x120]` (`003DACAF`) is the cell argument of the
  pair set (`003DACB8`).
- **The census agrees.** Every body-chain read of `+0x120` is 4 bytes. The cell routine writes the cell set as a dword
  (`0046AE0A` = -1, `0046AF3F` computed), or zeroes all 16 bytes as two qwords (`0046ADA3`, `0046ADA6`).
- **What else is in the 16 bytes.** `+0x124` is a dword written at `0046AF4A`, with no body-chain reader. `+0x128` and
  `+0x12C` are f32: written by `movss` at `0046AF59` / `0046AF65`, and read by `movss` at `003DACC8` / `003DACBD`, which
  hands them to the visit (`003DACD3`).
- **Control.** The u128 reading would need a read wider than a dword somewhere in `+0x120`..`+0x12F`, or a 64-bit
  shift in the walk. Neither exists. A copy with `003DB078` re-pointed at `+0x124` fails the new check.

## Point 2: `+0xE8` is the partner's increment, squared (FABLE): OPUS is right, and the field has a reader

- **Which body is which.** The resolver's prologue fixes `rdi = B` and `rbx = A` (`00314F72`, `00314F75`).
- **What the tail writes.** `check.py` runs the contact tail (`003152B2`–`00315372`) on scalar floats. At `w` = 0.3:
  - A's increment is (0.21, -0.12) and B's is (-0.49, 0.28);
  - B's `+0xE8` becomes 0.0585 = 0.21² + 0.12², which is **A's** increment, written at `00315303`;
  - A's `+0xE8` becomes 0.3185, which is **B's** increment, written at `0031533F`.
- **Overwritten, not accumulated.** Both stores are `movss`, and the earlier values (123, 456) are gone. The resolver
  never reads `+0xE8`.
- **The reader OPUS did not list.** `002E5380`, the contract's own consumer, loads it at `002E53B4` and compares it with
  0.0. When `+0xEC` is set, `+0xE8` is 0 and `+0xEE` is non-zero, it sets `+0xEF` to 1 (`002E53CF`); otherwise it sets
  `+0xEF` to 0 (`002E53D8`). A zero partner increment is exactly the case where this body took the whole push.
- **Control.** The old reading, "the body's own push length" or a running sum, fails at `w` = 0.3. A copy whose
  `00315303` store is re-based on `rbx` fails the new check.

## Point 3: `+0x08` is f32 (FABLE): OPUS is right

The census lists five body-chain accesses:

- the resolver's two reads, `movss` at `00315017` / `0031502A`;
- the two copies of the context's weight, `movss` at `0026861A` / `0026DAFE`;
- the allocator's dword store of the bits of 1.0 (`003DA98E`).

None of them is an integer operation. A copy where `00315017` is made a `movsd` fails the new check.

## Point 4: `+0x104` is push y, the middle component (FABLE): OPUS is only partly right

- **Inside the separation pass, OPUS is right.** The six bodies, and the share helper `00314E10`, touch `+0x104` only as
  the high half of the qword zero at `+0x100` (`003DA9F2`). The census finds no other write anywhere: the allocator's
  two qword zeros (`003DA97A`, `003DA9B9`) are the rest. So the field is always 0, as UQ-105 on the pool page says.
- **Image-wide, the claim does not hold.** `002E5380` reads `+0x104` **alone**, as f32: `movss xmm1, dword ptr [rdx +
  0x104]` (`002E53F1`). It adds it to `[r9 + 4]` (`002E53F9`, `002E53FF`), the middle float of the candidate delta.
  x goes to `[r9]` (`002E53DF`) and z to `[r9 + 8]` (`002E5405`). So the bytes do force both its type and its role:
  f32 push y.
- **The contract's wording was also loose.** "(third component)" meant the third push component. If it is read as
  vector index 2, it is wrong: that slot is `+0x108`.
- **Controls.** OPUS's "never accessed alone", taken image-wide, fails at `002E53F1`. The index-2 reading fails at
  `002E53F9`. A copy with `002E53F1` re-pointed at `+0x10C` fails the new check.
- **Wording.** `+0x104  f32  ~~(third component)~~ push y`. A continuation line says it is written only as the high half
  of the qword zero, so it is always 0. It also says the pass never touches it alone, and that `002E5380` reads it alone
  into the delta's middle float.

## Point 5: `+0xEE` marks the body that took the whole push (FABLE): OPUS is right

- **How the arm is chosen.** The share `w` is compared with `xmm7` = 0 (`00315249`; `xorps` at `00314F94`, not written
  again on the path) and with `xmm12` = 1.0 (`0031526C`; loaded at `00315055`).
- **When `w` = 0.** The arm marks **B** (`00315263`, `mov byte ptr [rdi + 0xee], 1`). In the tail run, only B's
  increment is non-zero: (-0.7, 0.4).
- **When `w` = 1.** The arm marks **A** (`00315287`), and only A's increment is non-zero.
- **When they share.** Both markers are cleared (`003152A4`, `003152AB`). The partner that took none keeps whatever
  value it had.
- **The reader.** It is the same `002E53C6` test as in point 2.
- **Why "immovable" is the wrong word.** It names the partner, not the marked body. The share comes from per-pair
  weights and masks (`00314E10`), not from a body property.
- **Control.** The old reading, "the marked body is the one that does not move", fails at `w` = 0. A copy whose
  `00315263` store is re-based on `rbx` fails the new check.

## What apply.py stages (FABLE)

Every struck span is the page's own text at HEAD, and part C of `check.py` checks this. Every address inserted lies in a
function the page already cites: `00314F50`, `00314E10`, `002E5380`, `003DA9F0`, `003DAC70` and `003DB020`. The cell
routine is cited only as `003DB020`+0x48, so the neighbour gate gains no edge.

**Contract section 3:**

- `+0x08 ~~?~~ f32`
- `+0xE8 ~~squared push length~~` → the squared length of the increment the latest push-mode contact gave the OTHER
  body. It is overwritten, not accumulated, and its one reader is `002E5380`.
- `+0xEE ~~immovable-contact marker~~` → sole-share marker. It is 1 on the body that took the whole push, 0 when the two
  bodies share, and left unchanged on the partner. Its reader is `002E5380`.
- `+0x104 ~~(third component)~~` → push y, with its writers and its one reader.
- `+0x120 ~~u128~~ u32` → one bit per mask, with what the rest of the 16 bytes hold.

**The pool page:**

- §2.7: `~~marks one body immovable~~` → it gives one body the whole separation and sets that body's `+0xEE`.
- §2.7: `~~the squared length~~` → of the increment just given to the OTHER body.
- §4: `~~pushLengthSq~~ partnerPushSqLength`.

`apply.py` refuses a page whose content differs from HEAD, keeps line endings, is idempotent, and is staged as a dry run
only.

## Consumer check (FABLE)

affected: Database/FFXII TZA/06-Movement-And-Navigation/CONTRACT-separation-pass.md
affected: Database/FFXII TZA/06-Movement-And-Navigation/the-movement-body-pool-and-the-separation-pass.md

**The contract:**

- **§3 `+0x08`, `+0xE8`, `+0xEE`, `+0x104`, `+0x120`:** revised-here.
- **P-6** ("`003DA9F0` then zeroes `+0x100`, `+0x104`, `+0x108`, `+0xE8`, `+0xEC`, `+0xED` and `+0xEE`"; the consumer
  "adds the accumulators into the candidate delta"): agrees. The consumer's add is the `+0x104` read of point 4.
- **P-7's table and its 2026-09-22 correction note** ("each immovable case advances exactly one `+0xED` and sets that
  same body's `+0xEE`"): agrees. "Immovable case" names the `w` ∈ {0, 1} outcome, and the note puts `+0xEE` on the body
  whose `+0xED` advances. That is the body that took the whole push (`00315263`, `00315287`).
- **§5's ownership lines** (`+0xE8` owned by the pass; "`+0x120`, the body's cell bits, written by registration"):
  agrees. The cell bits are the dword.
- **Falsification pass 1, rows S5 and S7:** agrees.

**The pool page:**

- **§2.7, "0 or 1 marks one body immovable":** revised-here. It put the mark on the body that stays.
- **§2.7, "with `+0xE8` the squared length":** revised-here.
- **§4 layout, `+0x0E8 f32 pushLengthSq`:** revised-here.
- **§4 layout, `+0x0EE u8 partnerImmovable`:** agrees. It is the same fact seen from the other body: the partner took
  none.
- **§4 layout, `+0x104 f32 pushY`, `+0x120 u32 cellBits` and `+0x008 f32 weight`:** agrees.
- **The intro and §6 ("a mask bit `00314E10` honours makes a body immovable; the other body takes the whole
  separation"):** agrees. This is about the share, and the other body is the marked one.
- **§2.8 and UQ-105** ("adds `+0x100`, `+0x104` and `+0x108` to the candidate delta"; "always adds 0"): agrees. This is
  the image-wide read that limits point 4.

**Other pages and the type store:**

- **The heading-speed page in category 06** (the "`+0xE8/0xEC/0xEE/0xEF`, `+0x100..+0x108`" block, "used only when
  Prepare is called with mode != 0"): agrees. It names the fields without giving them a meaning. A peer has an
  uncommitted hunk on that page, and it is not touched here.
- **OPUS's re-cut record** ("the pass never touches it alone"): agrees, as a statement about the pass.
- **The MovementBody rows of the type store:** routed-to-OPUS (OPUS/STRUCT own the store). Six rows need changes:
  - **`+0x0EF`:** "no access found besides the allocation qword" is false. There are five byte writers: `002E53CF` and
    `002E53D8` in `002E5380`, `002E5289` in `002E5180`, `0025D56F`, and `0026B0A1`.
  - **`+0x104`:** "no other access in the separation pass … type not forced" should cite the read at `002E53F1`. That
    read forces f32 and the middle component.
  - **`+0x0E8`:** should add its reader, `002E53B4`.
  - **`+0x0EE`:** should add its reader, `002E53C6`. Its "the contract calls it the immovable-contact marker" goes stale
    when this applies.
  - **`+0x124`:** it is written, at `0046AF4A`.
  - **`+0x128` / `+0x12C`:** they are f32.

  OPUS's record already notes the last two.

run: check.py at b5028e7e9 (FAILS 0; census control, 14 excluded roots dispositioned, five NEW/OLD/MUTANT triples, citation pre-check)
