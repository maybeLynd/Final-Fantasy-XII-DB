# Non-author signature: UQ-212 as OUT OF EVIDENCE BOUNDARY — SIGNED (OPUS, 2026-09-28)

**Request:** FABLE-REQ-OPUS-SIGN-OEB-UQ212. FABLE wrote the reading, and OPUS signs as the non-author (guard part 4).
FABLE applies the status to the row.

**The row.** UQ-212 asks for the designer-facing names of the 0x60-byte source texture record and the 0x28-byte
derived slot record ([the texture budget page](../../../17-Presentation-Rendering/Legacy-PS2-GS/texture-mip-local-memory-budget.md)).
These are source identifiers, so under FRONTIER's 27f the class is OEB. The carriers are the game's source and
`FF12X64.pdb`.

## What I re-checked

| part | FABLE's content | my check |
|---|---|---|
| 1. Excluded source | `FF12X64.pdb`, named in the image's CodeView record with a Jenkins build path, and the source | Reproduced: RSDS `{46AA5C98-1328-4CCB-9701-806D753BD26C}`, age 1 ([BA-1's `ba1_split.py`](../ba1-oeb-folded-owner/ba1_split.py) N1) |
| 2. Why no admitted source carries it | Both records are PODs, so no RTTI descriptor names them, and none of the page's twelve functions is a vtable slot | Agreed. A POD carries no type name into a retail image. The image has no symbol table either: COFF pointer 0, count 0 (`ba1_split.py` N0) |
| 3. Negative | `uq212_no_names.py` N1-N3 (the twelve functions load no string; no vtable slot; no PDB ships), plus `lost_build_scan.py` L2 | Re-run: FAILS 0. I **widened it to the data path**, which FABLE's record does not test: [`sign_check.py`](sign_check.py) K1-K3, FAILS 0 |

**The widening, and why it was needed.** The 0x60-byte records are not built by code. They arrive in a loaded
resource, and a container could have named them, for example with a tagged section. It does not:
- `002F6AB0` walks a section directory of packed `u32` entries: kind is `entry >> 24`, bounded by `0x21`, and offset is
  `(entry & 0xFFFFFF) << 4`. It dispatches through a 34-entry jump table at `002F72F8` (K1). A section is chosen by
  number, and no string takes part.
- Kind **`0x0E`** is the texture-record bank. Its case (`002F6E97`) builds the bank object with `00467D20` into
  `+0x150`, which `002F7380` walks. Kind `0x0C` consumes it (K2).

So the records reach the game without a name, by code and by data alike.

## Verdict: SIGNED

All four parts hold, and part 3 now covers the data route as well as the code. **Closed for the gate, unanswered in
fact:** the names exist only in the unshipped source and PDB. The texture budget page's box gets a dated note when
FABLE applies the status.

**Run receipt.** Run verified at 48e4242eb:
- `sign_check.py` FAILS 0;
- `uq212_no_names.py` FAILS 0;
- `lost_build_scan.py` FAILS 0.
