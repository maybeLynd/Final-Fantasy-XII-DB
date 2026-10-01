# S-47: the overlapping-copy import boundary, executed in the CRT the game binds (OPUS, 2026-09-26)

**Evidence class:** native execution of the dependency's exact code on the host CPU. The game image itself is **not**
executed here; SECTION-07's run supplies the arguments. `live_game: false`.

**The exposure being closed.** [`../s47-runtime-per-invariant-exposure.md`](../s47-runtime-per-invariant-exposure.md)
(RL-8) and SECTION-07 M07-7 both record it: *"the shipped mover hands overlapping ranges to the CRT `memcpy` import,
and what the CRT does with them is not established."*
- M07-7's shape: destination `0x300003C0`, source `0x30000500`, length `0x400`. That is a `0x100` hole before a
  `0x400` source, so the two ranges overlap.
- SECTION-07 stopped at the import entry: *"substituting host memmove would conceal the question."*

Nothing is substituted here. The routine that runs is the routine the game binds.

## What was run

`check.py`:

1. **The import.** The authority image (SHA `73461d08…`) imports `memcpy` from `VCRUNTIME140.dll` at IAT `008C2A68`
   (and `memmove` at `008C2A40`).
   - The image's directory ships **no** `vcruntime140*.dll`. The application directory is searched first and has none,
     so the loader binds the host's System32 copy.
2. **The DLL's bytes.** `C:\Windows\System32\vcruntime140.dll` is FileVersion **14.51.36247.0**, SHA-256
   `d1f4225d…c9ce7`.
   - The Python runtime has its own `vcruntime140.dll` loaded, so the file is loaded from a byte-identical copy under
     another name. That guarantees the System32 bytes run.
   - Before anything runs, the mapped `.text` (122,299 bytes) is compared with the file, rebased to the load address,
     and it is equal.
3. **Static.** The `memcpy` export (RVA `1F020`) is one instruction, `e9 dbeaffff`, which is `jmp` to `memmove`'s entry
   (`1DB00`). **In this CRT, `memcpy` is `memmove`.**
4. **Executed.** The `memcpy` export is called through ctypes on the host CPU: the DLL's own code, not an emulation.
   - **The dispatch.** `memmove` reads two globals of its own: the ISA level `[1DC51 → 26088]` and the "favor" bits
     `[1DC80 → 26374]`. The DLL's own initialisation sets both from CPUID; the host values are 5 and 2.
   - **Every path is run.** Each path is forced by writing those globals, and they are restored afterwards. The paths
     are the host values, plus ISA ∈ {0, 1, 2, 3, 5} × favor ∈ {0, 2}. Together they reach the jump table
     (≤ 0xF bytes), the two-xmm copy (≤ 0x20), the SSE and AVX forward paths, the `rep movsb` path
     (0x2000 < len ≤ 0x180000 when the copies are ≥ 64 bytes apart), and the backward path `1E0A0` (upward overlap).
   - **The matrix.**
     - Lengths: 1–0x40, `7F`/`80`/`81`, `FF`/`100`/`101`, `1FF`, `3FF`/`400`/`401`, `1000`, `2000`/`2001`, `4000`,
       `10000`, `180000`/`180001`.
     - Distances: 1, 3, 8, `10`, `1F`, `20`, `3F`, `40`, `41`, `100`, `140`.
     - Misalignment 0 or 5, and both directions.
   - **The check.** The destination must hold the source's **original** bytes (memmove semantics). The return value and
     every byte of the 4 MiB arena around the copy are checked.

**8 / 8 cases pass, and `result.json` is byte-identical over two runs** (md5 `456ab2c59970d3b6f2c43721e89ba651`).

| case | observed |
|---|---|
| `import_is_VCRUNTIME140_memcpy_at_008C2A68_and_no_app_local_copy` | IAT `008C2A68` = `VCRUNTIME140.dll!memcpy`; there is no app-local CRT |
| `loaded_code_is_the_System32_file` | the mapped `.text` equals the file |
| `memcpy_export_is_one_jmp_to_memmove` | `1F020: jmp 1DB00` |
| `M07_7_shape_copies_as_memmove_on_every_path` | distance `0x140`, length `0x400`, with both addresses at M07-7's own residues mod 0x40 (`0x3C0` → `0x00`, `0x500` → `0x00`). On all 11 paths the destination holds the original source bytes |
| `matrix_every_copy_is_memmove_on_every_path` | **39,215 copies, 0 failures** |
| `dispatch_globals_restored` | the host values are back |
| `control_checker_catches_a_forward_copier_on_upward_overlap` | the same checker, handed a plain forward byte copier, **fails** it on an upward overlap (length 0x40, distance 8) and passes it downward. So the checker discriminates |
| `census_every_x64_copy_exports_memcpy_as_memmove` | a static census of every x64 `vcruntime140.dll` on the host (Program Files ×2, System32, D:, depth ≤ 6) found **41 distinct copies, versions 14.00.23506 to 14.51.36250**. In **22** (14.00–14.36), `memcpy` and `memmove` are the **same export RVA**. In **19** (14.40–14.51), `memcpy` is a one-instruction `jmp` to `memmove` |

## M07-7 carried past the import: `overlap_complete.py`

SECTION-07's harness (ORACLE, `native_controls.c`) runs the original mover `00369C60` natively on Linux over a private
image. For an overlapping copy, its memcpy adapter refuses to emulate the CRT and stops (M07-7).

**What this driver changes.** It verifies that file by SHA-256 (`c24a9fd9…`) and **never modifies it**. It builds a
**patched copy** in a temporary directory, with exactly two textual replacements (each asserted to match once) and one
appended case:
- **R1:** the overlap branch of the adapter performs the copy with memmove semantics, in a new mode `overlap-complete`.
  That is what `check.py` measured for the bound CRT. In the control mode `overlap-complete-backward`, it copies byte by
  byte **backward**. Every other mode keeps ORACLE's behaviour.
- **R2:** `main()` dispatches the two new modes.
- **The appended case** `overlap_complete()` takes M07-7's layout (a `0x100` hole, a `0x400` source, no barrier) through
  the **real compactor**, then asserts `exact_move`'s whole post-state plus the overlap.

It is compiled in WSL with ORACLE's own flags (gcc 11.4.0, `-std=c11 -O2 -Wall -Wextra -Werror -fPIE -pie`, no
diagnostics).

**5 / 5 cases pass, and `overlap_result.json` is byte-identical over two runs** (md5 `b979a5597f90f2aaf3f1a9279a0a9a9e`).

| case | observed |
|---|---|
| `oracle_baseline_unchanged_on_patched_copy_123_checks` | ORACLE's baseline on the patched copy: **123 checks, 0 failures** |
| `oracle_overlap_boundary_unchanged` | `overlap-boundary` still stops at the import with destination `0x300003C0`, source `0x30000500`, length `0x400`, exactly as ORACLE recorded |
| `overlap_complete_every_assertion_passes` | **23 / 23.** The source is at `0x30000500` and **one move** lands it at `0x300003C0`, `0x140` lower (hole plus header). The copy is observed once, and **it overlaps**. **The full payload is preserved.** Also preserved or updated: the size `0x400`, the live handle slot, slot header = new − 0x40, the header backlink, the generation pair (changed, same handle), tree membership, accounting (1152), the compaction-change mark and the movement latch. The slot is published and the old block freed before the copy. The stable handle resolves the new source, cleanup accounting is 0, and there are no diagnostics |
| `overlap_complete_repeat_identical` | a second run gives the same record |
| `control_backward_copier_fails_exactly_the_payload_assertion` | with a backward copier the run fails **exactly** `overlap_mover_preserves_full_payload`, and all 22 other assertions still pass. So the overlap is real, and the payload check discriminates |

## What this closes, and what it does not

- **Closed, for the bound CRT:** a mover that hands overlapping ranges to `memcpy` gets `memmove`'s result. That holds
  in either direction and on every dispatch path this CPU or any other could select. It is executed for 14.51.36247.0,
  the CRT the game binds on this host. **M07-7's movement completes past the import** with the whole `exact_move`
  post-state (`overlap_complete.py`).
- **Generality (static):** across every x64 VCRUNTIME140 version found (14.00–14.51), the `memcpy` export *is* the
  `memmove` code, as the same entry or a single `jmp`. Only 14.51.36247.0's `memmove` is executed. For the others the
  identity is byte-read, and their `memmove` is not run.
- **Not closed:** a host whose VCRUNTIME140 is a version outside this census; a live game.
- **For the contract** (`CONTRACT-resource-input-ownership.md`, FABLE's): §13 says memcpy is *"bridged"* in the
  SECTION-06 runs. This package executes the real import for the overlap case. Routed to FABLE.
