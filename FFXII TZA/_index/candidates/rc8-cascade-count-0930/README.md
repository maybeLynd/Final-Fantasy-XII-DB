# RC-8: only the constructor writes the shadow object's cascade count, so elements 3 to 7 are never counted (ORACLE, 2026-09-30)

Input for `RC-8` ([what the console tunes](../../../00-Engine-Core-Runtime/Developer-Tuning-Console/what-the-console-tunes.md)
section 7, UQ-24's residue). SWE2-CONTRACT registered the row. Static evidence only (shipping image `73461d08…`).
**Verdict: ANSWERED.**

## The question

The shadow object built by `001EF2D0` holds eight `0xD8`-byte cascade elements at `+0x148` and a live count at `+0x13C`.
The constructor sets the count to 3 (`001EF389`), and the cascade loop `001EF6D0` is bounded by it (`001F04DF`). About
sixty other dword writes to some `+0x13C` exist image-wide. Does any of them store this object's count, so that
elements 3 to 7 could be used?

## Method

Two scripts. Both share `memsweep.py` (every function body: the `.pdata` chain roots, plus leaf bodies from
`functions.tsv`) and `img.py`.

**1. `rc8_flow.py`: where the object's pointer goes** (outputs `rc8_flow.out`, `rc8_flow.tsv`, `rc8_escapes.tsv`;
FAILS 0).

This is a forward pointer-flow analysis per function, over its basic-block graph, with the states united at joins.
It tracks which registers and stack slots hold "object + offset". The object is `0xB08` bytes, allocated by
`00210EC0`, and has no vtable: the constructor stores none at `+0`.

- **Seeds.** Seeds are added until nothing new is found:
  - every load of a cell that holds the pointer;
  - the return value at every call or tail jump to a function that returns the pointer;
  - the constructor entered with `rcx` = the object.

  The analysis found the cells and getters itself. Starting from `01F82EA8` and the four get-or-create functions
  `001F0810`, `001F0850`, `001F1590` and `001F1600`, it added:
  - a **second cell, `01F812C8`**, which the static initializer `0015CC00` fills from `001F0850` and the console
    functions `001C3D50` and `001C7940` read;
  - three **getters that return the pointer**: `0015CC00`, `001AC7C0` and `001FB310`.
- **At every instruction:**
  - An access through the pointer is recorded at its object offset. A write whose bytes cover `+0x13C`..`+0x13F` is a
    count write.
  - A call or tail jump that gets the pointer in `rcx`/`rdx`/`r8`/`r9` is followed into the callee.
  - A store of the pointer to memory other than a known cell, a pointer in an outgoing stack argument, or a pointer
    handed to an indirect call is an **escape**. Each escape is listed with the lowest object offset it can carry.
  - Import thunks (`jmp [IAT]`) are named, not followed.
- **Controls.**
  - The constructor's store `001EF389` must be reported as a count write.
  - The cascade loop `001EF6D0` must be reached, and must read object `+0x13C`.

**2. `rc8_census.py`: the census the row asks for** (outputs `rc8_census.out`, `rc8_census.tsv`; FAILS 0).

It lists every instruction image-wide that writes bytes covering `+0x13C` through a non-stack base register, at any
width. Each one is classified against the flow:
- **OBJECT:** the flow saw the object itself as the base at that instruction.
- **REACHED:** the function holds the pointer, but not as this base.
- **UNREACHED:** the pointer never gets there.

Control: `001EF389` must be OBJECT.

## Result

**The pointer reaches 39 functions.** Among them:
- the scene settings path `00186CD0`;
- the render pass list `00187950` → `001F0AD0` → the cascade loop `001EF6D0` → `0018A120` / `00185100` / `001EB4B0`;
- the console dispatcher `001D1660` and the console arm `001D5120` → `001EF520`;
- the console functions that read the second cell, `001C3D50` and `001C7940`;
- `001E2AF0` → `001945B0` → `005C5230`;
- the pairs `003ED190`/`003ED3F0` and `0051DE30`/`0051E170`.

**Exactly one instruction writes the count: the constructor's `mov dword ptr [rbx + 0x13c], 3` (`001EF389`).** No
other code holding the pointer writes any byte of `+0x13C`..`+0x13F`.

**There are 7 escapes, and none can reach the count.** Each carries an address at or above object `+0x148`, the first
cascade element:
- the three virtual calls on elements in `001EF6D0` (`001F0470`, `001F0482`, `001F04A2`), which pass `rcx` = an element;
- the CRT vector constructor `00808FE4`, which the constructor calls for the eight elements (`001EF344`): its element
  store, its element-constructor call and its stack argument.

The two further calls made while a pointer register was live are the import `sqrtf` (`001EB531`, `001F09AC`), which
takes a float.

**The census.** 184 instructions write bytes covering `+0x13C` through a non-stack base. That includes 60 dword stores
at exactly `+0x13C`, the row's "about sixty". Another 98 are frame-based.
- **1 is OBJECT:** `001EF389`.
- **0 are REACHED.**
- **183 are UNREACHED:** they sit in functions the pointer never enters, so each writes a different object.

**So the count stays at the constructor's literal 3 for the life of the process.** The cascade loop runs elements 0 to
2 only. Elements 3 to 7 are constructed, and are copied by the eight-slot copy the page describes, but they are never
counted in. This agrees with W-9: no authored key raises the count, the partition sink rejects indices of 3 or more,
and `mCascadeNumber` is unread.

**How this relates to FABLE's record** ([`rc789-fable-0930/`](../rc789-fable-0930/README.md), RC-8):
- The two records reach the same answer.
- This record covers two routes FABLE's call-hop census did not. FABLE described `01F82EA8` as the object's only
  published location. The second cell `01F812C8` and its two console readers are followed here, and the getter
  `001FB310`'s caller `001F5D70` is seeded.
- This record's flow is not bounded by hop count.

## Not claimed

- **Negative-offset accesses.** The escapes are dismissed on one assumption: code given an element pointer (object
  `+0x148` or more) does not write at a negative offset from it.
- **Non-negative indices.** The element base `object + 0x150 + i*0xD8` is taken as at least `+0x150`, on the
  assumption that `i` is non-negative. The script labels this ASSUMPTION.
- **What the analysis does not model:**
  - copies of the pointer into vector registers (none were flagged);
  - `xchg` (none flagged);
  - flows through memory other than the two cells and stack slots (none were found beyond the listed escapes);
  - code outside the swept bodies.
- **Other means.** A write by a debugger or a mod, or by a bulk copy onto the object from outside the reached set, is
  outside a static census.
- No execution.
