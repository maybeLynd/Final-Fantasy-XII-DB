# Phyre virtual destroy slots: consumer check (OPUS, 2026-09-28)

**Corrects:** `_types/types.tsv` (24 `dtor` cells) and `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md` (the two `+0x58` form tables). Both were written by OPUS in d8eb6b94e (2026-09-19).

**Refuted claim:** every class destroyed through a vtable is destroyed through **slot 0** (`mov rax,[rcx] ; call [rax]`).

**Replacement:** the thunk calls `call [rax + 8k]` on the object at `this - 8`, with a slot that depends on the thunk:

| thunk | slot | cells |
|---|--:|--:|
| `0063FC60` | 0 | 87 |
| `0068C4E0` | 3 | 23 (the physics shapes) |
| `00680910` | 2 | 1 (`PScheduler`) |

## Consumers (OPUS, 2026-09-28)

| consumer | state |
|---|---|
| consumer `_types/types.tsv`: 24 `dtor` cells naming `0068C4E0` or `00680910` | revised-here (struck `slot ~~0~~ 3` / `~~0~~ 2`, each citing the check) |
| consumer `_types/types.tsv`: 87 `dtor` cells naming `0063FC60` | agrees (slot 0 is right for that thunk) |
| consumer `class-descriptor-and-metadata-system.md`: the `+0x58` form table row | revised-here |
| consumer `class-descriptor-and-metadata-system.md`: the RTTI cross-tabulation row | revised-here |
| consumer `Tools/analysis-kit/gfz-scripts/gen_phyre_descriptor_vtables.py`: its docstring form table | revised-here |
| consumer `members/phyre-class-descriptor-vtable.tsv`: `s58_form = virtual` with the thunk address and no slot | agrees (states no slot) |

A search of the database's `.md`, `.tsv` and `.py` files for `0068C4E0` / `00680910` finds only these consumers, plus address lists that state no slot: `ADDRESS-INDEX.md`, `ba1_split.tsv`, `uncited_functions.tsv` and a UC-1 projection.

**Regression:** `_index/candidates/phyre-virtual-destroy-slot/virtual_slot.py`.

- V derives each thunk's slot from its call displacement.
- S fails while any `virtual` cell states a slot its thunk does not call, or while the page or the docstring still gives slot 0 for all 111. Before the patch S failed with 24 wrong; after it, FAILS 0.
- Verified at e389f34b5 plus this publish's working tree (`virtual_slot.out`).
