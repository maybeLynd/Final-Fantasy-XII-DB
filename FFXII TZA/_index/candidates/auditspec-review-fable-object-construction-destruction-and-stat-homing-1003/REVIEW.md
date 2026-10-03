# SWE2-AUDIT-SPEC review: FABLE cloud-drafted F-homing rows (fable-object-construction-destruction-and-stat-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-OBJECT-CONSTRUCTION-DESTRUCTION-AND-ST` · Package: `_index/candidates/fable-object-construction-destruction-and-stat-homing-1003/` · Page: `24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/object-construction-destruction-and-static-lifetime.md` (commit `b7c6eb07d`, reviewed at HEAD `81a9fa56d`; the package is unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- **Applier.** `interior_applier.py` was re-run fresh without `--apply`. It printed `VERIFY 4 functions, 17 anchors`, `ALREADY`, `FAILS 0`, and wrote nothing. The section is on the page at line 1145, and every sentence is on the page verbatim.
- **rows.json.** 4 rows, 17 anchors. Rejected 0, skipped 0, missing 0. 2 FABLE corrections, both confirmed against the bytes:
  - `0019B2F0`: `0019B340` loads the array pointer from `+0x10`, and `0019B381` passes the address of the local `rsp+0x58` copy of `01F81148`.
  - `008A4BAB`: `008A4BC1` is a `nop` inside the extent.
- **Semantic pass.** All 4 rows were read clause by clause against `disr.py` output of the certified image.
  - `0019B2F0`:
    - The import at +0x23 is called with `(rsp+0x50, 0)`, and `01F81148` is copied to `rsp+0x58`. The import at +0x3D is called with qword `[008C25A8]`.
    - `cmp rdi, [rax+0x18]` / `jae` is an unsigned bound. The array pointer comes from `[[rcx+8]+0x10]`.
    - The retry through the import at +0x6B is gated on byte `+0x24`. Then the local copy is used. Then the import at +0x96 is called with `(&local, rcx)`.
    - A result of `cmp rax, -1` throws through `_CxxThrowException(&{008F3618, 008F3628 "bad cast", 0}, 01DEAAA0)`.
    - Otherwise the local goes to `01F81148`, then `call [vtbl+8]` and `_Facet_Register` (`00808850`).
    - Every exit that does not throw reaches the import at +0xF6 on `rsp+0x50`, with `rax` = the pointer.
    - Exact.
  - `001DE200`:
    - d = `movsxd [[rcx-0x88]+4]`. The stores are `00901090` to `[rcx+d-0x88]`, d−0x88 to dword `[rcx+d-0x8C]` and `00900F20` to `[rcx-0x80]`.
    - Then `001DF8C0(rcx-0x80)`, the import at +0x59 with `rcx-0x80`, and the tail `jmp` through the import at +0x6D with `rcx-0x78`.
    - Exact.
  - `008A4BAB`: `mov rbp, rdx`, then `_CxxThrowException(0, 0)`, then `nop`. Exact.
  - `008B90A0`:
    - `01CCF348` goes to `02EAF400`. `0085E710([02EAF620])` runs only when that qword is non-null and byte `02EAF628` is non-zero.
    - Then byte `02EAF628` = 1, qword `02EAF620` = 0, qword `02EAF614` = 0, and `00839FD0(02EAF400)` at +0x5E.
    - Exact.
- **Note (not a defect).** `001DE200` reads `[rcx-0x88]` and its `+4` again before the second store. The sentence's single d is right whenever the first store does not overwrite the table pointer, which needs d ≠ 0.
- Limits: body statements only, static evidence. The cloud draft and FABLE's re-read are not independent review; this record is.
