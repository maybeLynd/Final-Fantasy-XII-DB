# SWE2-AUDIT-SPEC review: FABLE cloud-drafted F-homing rows (fable-add-motion-skeleton-and-high-model-table-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-ADD-MOTION-SKELETON-AND-HIGH-MODEL-TAB` · Package: `_index/candidates/fable-add-motion-skeleton-and-high-model-table-homing-1003/` · Page: `17-Presentation-Rendering/Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md` (commit `eea05327e`, reviewed at HEAD `db98e3d59`; the package is unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- **Applier.** `interior_applier.py` was re-run fresh without `--apply`. It printed `VERIFY 10 functions, 50 anchors`, `ALREADY`, `FAILS 0`, and wrote nothing. The section is on the page at line 550, and every sentence is on the page verbatim.
- **rows.json.** 10 rows, 50 anchors. Rejected 0, skipped 0, missing 0, corrections 0.
- **Semantic pass.** All 10 rows were read clause by clause against `disr.py` output of the certified image. Every site offset, argument register, stack slot, branch polarity and store was checked.
  - `003418B0`:
    - `cmp byte [r8+8], 0` / `je` returns 0. On word `+0xA` = 0, `002E97C0([r8+4])`.
    - A null result stores `002E9810(002EB540([r8], byte [rdx+0x15]))` to `[r8+4]`, then `00314D40(1)`, and returns 1.
    - A non-null result goes to `002E4C20`. A 0 there takes the same `00314D40(1)` / return-1 path (`je 003418FA`), and a non-zero stores word 1 and returns 0.
    - Word 2 runs the same test and stores word 3.
    - Any other value returns `[rsp+0x40]`, which after `push rdi` / `sub rsp, 0x20` is the entry `r8` home slot. The body writes only the `rcx` home slot. Exact.
  - `00343B00`:
    - Pops at +0x24, +0x2F and +0x39. The second goes to `002E9A60`, then word 0 to `+0xA`.
    - The clamp is `js` to 0, then `cmovg` with 1.
    - `00267310(byte [rdx+0x15])` at +0x64: non-zero gives byte 0 to `+8`. Otherwise the stores go to `[r8]`, `+4`, `+0xC` (the first pop), byte `+9` (clamped) and byte 1 to `+8`.
    - Exact.
  - `00344F00`: the same shape, with one pop at +0x18 and `00267310` at +0x30. Exact.
  - `0034CED0`: pop at +0x10, then `jns` / `00314840` at +0x1B. Pop at +0x25 goes to `0026B750` at +0x2C. Tail `jmp 00314D40` with the kept value. Exact.
  - `00352E40`: pops at +0x10 (`ebx`) and +0x1A, then `002E2560(ecx = second, edx = first)` at +0x23, then tail `00314D40(1)`. Exact.
  - `0036EB70`:
    - The record ranges are `022D9AEC`..`022D9B4C` (0x60/0x18 = 4) and `022D9ABC`..`022D9AEC` (2).
    - Each record gets `movsx [rbx-0xB]`, with +2 unless `cmove` (byte `[rbx-0xA]` zero), then `002DF440`.
    - Then `00369800([rbx])`. The `[rbx]` = 0 store comes after `+4` is read, then `00369800([rbx+4])` and the `+4` = 0 store.
    - Exact.
  - `0050CA40`: pop at +0x13. `jle` keeps a value of 0 or less, else `002E9A60`. The value goes to `[r8]`. `js` skips; otherwise `002EB540(value, byte [rdx+0x15])` goes to qword `r8+8`. Exact.
  - `0050CBD0` / `0050CD80` / `0050CF20`:
    - `cmp dword [r8], 0` / `jl` takes the tail `002E3C20(rdx, 0|1|2, 0)`.
    - Otherwise `002EBC90(rdx, 2|1|3, 1)`, then `002E3110(rdx, 0|1|2, 0, [r8+8])` with `[rsp+0x20]` = 0.
    - All argument values were checked against the `lea r8d, [rdx-1]`, `lea edx, [r8+1]` and `[r8+2]` forms. Exact.
- Limits: body statements only, static evidence. The cloud draft and FABLE's re-read are not independent review; this record is.
