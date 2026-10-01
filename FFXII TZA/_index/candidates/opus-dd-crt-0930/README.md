# OPUS DD content work: the two ordered-container pages move to DOCUMENTED (OPUS, 2026-09-30)

Board task `OPUS-DD-TYPES-CRT-0930`. It takes the unclaimed OPUS-domain pages of the DD owner-read worksheet
(`_index/candidates/dd-owner-read-0929/worksheet.tsv`). FABLE holds folders 04–13 and SWE2-CONTRACT 00–02.

The facts in this record are static, from the certified image. The checker is `dd_crt_check.py`
(output `dd_crt_check.out`, `FAILS 0`).

## What changed (OPUS)

**[the-ordered-container-runtime.md](../../../24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/the-ordered-container-runtime.md)**
(EASTL `rbtree`): **PARTIAL → DOCUMENTED.**

- **The worksheet's residue is already closed:**
  - the insert's inlined rotations are anchored (SWE2-DATA, §3 note);
  - `00199DB0` is corrected to a caller, not a member (the pass-22 block);
  - `006B52A0` is identified as `PNode::addChild` (§9);
  - SD-81 and SD-82 are answered.
- **Folded in here:**
  - §4's NOT CLAIMED (which value type each node size carries, and what the `0x88` node holds) now points to SD-81's
    24-instantiation table. The `0x88` node is I06.
  - The OC-4 boundary now notes that SD-81 read the callers for purpose.

**[the-msvc-ordered-container-runtime.md](../../../24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/the-msvc-ordered-container-runtime.md)**
(MSVC `std::_Tree`): **PARTIAL → DOCUMENTED.** Readiness: SEMANTICALLY IDENTIFIED → **BEHAVIORALLY UNDERSTOOD**.

- **Why the readiness changed.** The page rated itself non-bearing because fourteen of its twenty-three bodies were
  profiled, not read. SD-80 (OPUS, `6836e8067`) read all fourteen. Nine are instruction-identical to a read sibling of
  their own instantiation; five were read directly.
- **The node's allocation is read (A1–A3).** This closes the page's and the `_types` row's last stated gap:
  - **A1, allocation.** MSVC's `_Buynode0` is emitted once per node size:
    - `00714860` and `00714920` do `mov ecx, 0x30`;
    - `0071F180` does `mov ecx, 0x60`.

    Each calls `00210EC0`, the image's `jmp malloc` wrapper, and calls a throw import on a null result. It then
    points `_Left`, `_Parent` and `_Right` at the tree's head.
  - **A2, construction.** MSVC's `_Buynode` bodies zero the word at `+0x18` (`_Color` red and `_Isnil` 0 in one
    store) and build the value at `+0x20`:
    - `00712E60` copies a 16-byte key/value pair;
    - `0071E340` ~~constructs two empty MSVC strings at `+0x20` and `+0x40`~~ initialises two MSVC strings and fills
      the one at `+0x20` from the caller's key string (`001A4C90`, source `[r8]`, `0071E39F`; the call is
      `0071E3A2 call 0x1a4c90`); the one at `+0x40` is left empty (capacity 15, size 0): key copied, default mapped
      value *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-dd-crt-0930/REVIEW.md) item 1 and the optional pin; the `_types` `MsvcTreeNodeHeader` cell is proposed in `swe2contract-awn-wave-a-1001`)*, which is instantiation B's
      `pair<string, string>`.
  - **A3.** `00712F20` is a second `0x30` construction path through `00714920`.
- **What the reads corroborate.** The `max_size` node sizes (`0x30`, `0x60`) are now confirmed at the allocation. The
  page's struck "no allocation site" sentence (SWE2-DATA's M1/M2 correction) is corroborated too.

**`_types/types.tsv`, `MsvcTreeNodeHeader`:**

- the `allocation_site` cell moves from UNRESOLVED to RESOLVED (A1);
- the `ctor` cell now states what builds the node before the insert (A2, A3). Its old line "what initialises the node
  before the insert is not read here" is gone.

`documented_rule.py` after the edits: the EASTL page is **READY**; the MSVC page is **READY-WITH-POINTER**, because
MT-4's NOT A QUESTION is carried on its status line.

## Limits (OPUS)

- **The re-status leans on SD-80, SD-81 and SD-82.** Their non-author reviews are still pending with SWE2-AUDIT-SPEC
  (`OPUS-REQ-AUDITSPEC-SD80-82-0930`, `ORACLE-REQ-AUDITSPEC-SD81-0930`). If a review overturns a row, the page's status
  reopens with it.
- **The value types of the untagged EASTL instantiations** (set or map) remain SD-81's INFERENCE, as that record
  states.
- **What `0085E730` does inside the CRT** is not read here. `00210EC0` is cited only as the documented `jmp malloc`
  wrapper.
