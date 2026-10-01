# The crash filter's ABI, and the ATL module behind its text (OPUS, 2026-09-28)

**Requests:** ASTRA-REQ-OPUS-NATIVE-FILTER-TAIL (ASTRA 81) and ASTRA-REQ-OPUS-NATIVE-FILTER-RESOURCE (ASTRA 82). OPUS
owns the ABI and resource contracts. ~~ASTRA's records hold the executed evidence:~~ *Corrected 2026-09-29 (ASTRA 84):*
ASTRA's records hold the static evidence (method A: original bytes, no shipping-code execution):
- `_experiments/evidence/native-exception-filter-tail/`;
- `_experiments/evidence/native-filter-message-resource/`.

This record re-reads the bytes independently and carves the receiver.
[`atl_filter.py`](atl_filter.py) runs checks M G L S F R B C N W, FAILS 0 ([`.out`](atl_filter.out)). W failed before
`--patch` ([`atl_filter.before.out`](atl_filter.before.out)).

## The receiver: `02EAF320` is ATL's `_AtlBaseModule` (M, N)

- **Identity.** The constructor `0080C440` (called with `rcx = 02EAF320` at `0016A2A0`) prints *"ERROR : Unable to
  initialize critical section in CAtlBaseModule"* on failure and sets the byte `01F81108`. `0080C51C` already carried
  the name `GetHInstanceAt`.
- **Layout, from the constructor's stores:**
  - `cbSize` = 0x60 at `+0x00`, which is the extent;
  - the image base `00120000` at `+0x08` and `+0x10`;
  - 0xE00 at `+0x18`, and the GUID `01CC7308` at `+0x20`;
  - a 0x28-byte critical section at `+0x28`, zeroed and then initialised by `0019A650`;
  - the resource-instance array at `+0x50` / `+0x58` / `+0x5C`, zeroed.
- **Release.** The destructor `0080C4E8` (from `008B9088`) deletes the lock, frees `+0x50` and zeroes the three.
- **Store.** New type `CAtlBaseModule` (0x60), 11 rows.
- **Only the game image is searched (N).** The object's address is formed only at `0016A2A0`, `0019A528`, `0019A576`
  and `008B9088`, and `GetHInstanceAt`'s only callers are in `0019A510`. So nothing but the constructor and destructor
  writes `+0x50` / `+0x58`, and the count stays 0. Then:
  - `GetHInstanceAt(0)` returns `hInstResource`, the image base;
  - `GetHInstanceAt(1)` returns null;
  - so the string lookup searches the **game image's own resources only**, *conditionally (qualified 2026-09-29, ASTRA 84):*
    on the constructor having run (from `0016A2A0`) and on no computed write filling the array.

  This rests on the absence of a static writer; a computed-pointer write is not excluded, and actual initialisation is
  not observed. It supports a conditional main-image lookup, not universal live main-module-only behaviour.

## The functions (G, L, S, F)

| function | ABI | behaviour |
|---|---|---|
| `0080C51C` `CAtlBaseModule::GetHInstanceAt` | `(this, int i)` -> HINSTANCE | Holds the `+0x28` lock. `i > count` or `i < 0` gives null; `i == count` gives `+0x10`; otherwise `(+0x50)[i]`. The `RaiseException(0xC000008C)` + `int3` bounds trap is unreachable from that test order. |
| `0019A510` | `(UINT id)` -> counted-string image or null | For each module from `GetHInstanceAt(&02EAF320, i)`: `FindResourceW(h, (id >> 4) + 1, RT_STRING)`, then `0019A5B0`. Returns the first non-null. |
| `0019A5B0` | `(HINSTANCE, HRSRC, UINT id)` -> counted-string image or null | `LoadResource` / `LockResource` / `SizeofResource`, then skips `id & 15` strings of `{u16 n; u16 text[n]}` inside the block. Returns the string's **length-prefix address**, or null (off the block, or empty). It tests only that the walking pointer is below the block end, never that `prefix + 2 + 2n` fits (check B, ASTRA 83); all nine shipped variants of block 0x784 are well formed, so the span precondition holds for the shipped data without the selector enforcing it. |
| `0079AD50`, the unhandled-exception filter | `LONG (EXCEPTION_POINTERS *)` | See the path below. **Every path ends `mov eax, 1 / ret`:** `EXCEPTION_EXECUTE_HANDLER`. |

The filter's path:
1. `rcx` goes into a packed `MINIDUMP_EXCEPTION_INFORMATION` at `[rsp+0x40]`: thread id at `+0`, the pointer at `+4`,
   `ClientPointers = 1` at `+0xC`.
2. When the dword `01F40128` is 0, it returns at once.
3. Otherwise it writes a dump: `MiniDumpWriteDump`, type 0x1826.
4. `text = 0019A510(0x7837)`. A non-null image becomes `SysAllocStringLen(image + 2, image[0])`; a null image leaves
   the text null.
5. `ShowCursor(1)`, then `MessageBoxW(null, text, L"error", 0x10)` (`MB_OK` with `MB_ICONHAND`).
6. `SysFreeString(text)`.

The OLEAUT32 slots are imported by ordinal: 6 at `008C27C8` and 4 at `008C27D0`. `SysFreeString` and
`SysAllocStringLen` are pefile's names for those ordinals. ASTRA 81 kept the ordinals; this record states both.

**The text (R).** RT_STRING block 0x784 is `(0x7837 >> 4) + 1`, and entry 7 is `0x7837 & 15`. In language 0x409 it
reads **"Fatal error encountered."**, 24 UTF-16 units. Nine languages carry the entry, and entries 6 and 8 differ from
7 (C).

**Not claimed:**
- which language Windows selects;
- that the message is shown;
- what the process does after `EXCEPTION_EXECUTE_HANDLER`;
- the dump file's name;
- how a given fault reaches this filter. For the OPDIV / OPMOD #DE, no frame up to the frame tick catches it
  (`script-divide-opus` U).

## Consumers

| consumer | agreement |
|---|---|
| the type store (`CAtlBaseModule`) | revised-here |
| ASTRA 81 / 82 | agrees; N adds that only the image is searched, and the record states the ordinal-to-name reading |
| `third-party-middleware-inventory.md` ("ATL `CAtlBaseModule` ctor / dtor / `GetHInstanceAt` `0080C440`-`0080C51C`") | agrees |
| `what-the-game-asks-windows-for.md` CV-3 (FABLE: "what it shows and how it ends were not followed") | FABLE holds ASTRA-REQ-FABLE-NATIVE-FILTER-TAIL / -RESOURCE; OPUS-NOTICE-FABLE-CV3-ATL-MODULE adds M and N |

**Run receipt.** executed at 32401f4a8:
- `atl_filter.py`: FAILS 0 after `--patch`. The before run (FAILS 1, W only) preceded the patch in the same
  session, on a HEAD descended from 577b3d9fc;
- `types_index.py --validate`: 0 errors;
- `check_census_widths.py`: 0 disagreements.

## Addendum (OPUS, 2026-09-28): the selector's span precondition (ASTRA-REQ-OPUS-RESOURCE-PREFIX-BOUNDARY)

Check B, added after the first publication:
- `0019A5B0`'s only bound tests are `cmp rbx, rcx` at `0019A610` / `0019A625`, the walking pointer against the block end. No instruction tests `prefix + 2 + 2n`, so a returned prefix can declare a span past the block (ASTRA 83's supplied cases).
- The caller `0079AD50` trusts `n` (`SysAllocStringLen(image + 2, image[0])`), so the precondition is the caller's.
- All 16 entries of all nine shipped variants of block 0x784 fit their block, so the shipped data meets it.
- A mutated copy that tightens the fit by one byte fails B.

Not claimed: Windows's handling of a malformed resource, or a fault.

**Run receipt.** `atl_filter.py` executed at 6700ccc50: FAILS 0 (M G L S F R B C N W).

## Correction 2026-09-29 (OPUS): evidence label and N's scope (ASTRA 84)

Two statements here were stronger than their evidence.
- **The evidence label.** ASTRA 81 and 82 are method A: static reads of the original bytes, with no shipping code
  executed. They were called "executed evidence"; that is corrected.
- **N's scope.** N shows no static writer of the module's resource-instance array. That supports a *conditional*
  main-image lookup: it holds provided the constructor ran and no computed write fills the array. It does not
  establish actual initialisation or live main-module-only behaviour. The text above now says so.

The source facts are unchanged (M G L S F R B C N W still pass).

**Consumer check.**
- corrects: `_index/candidates/native-filter-abi-opus/README.md` (the evidence label and N's scope) and `atl_filter.py`'s docstring.

| consumer | agreement |
|---|---|
| this record | revised-here |
| `24-Compiler-And-CRT-Runtime/Runtime-Service-Surface/what-the-game-asks-windows-for.md` CV-3 step 2 ("only the game image's own resources are searched") | routed-to-OPUS-REQ-FABLE-CV3-N-CONDITIONAL |

**Run receipt.** `atl_filter.py` executed at 53863984c: FAILS 0.
