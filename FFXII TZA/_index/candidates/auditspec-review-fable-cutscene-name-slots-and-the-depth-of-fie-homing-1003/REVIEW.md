# SWE2-AUDIT-SPEC review: FABLE cloud-drafted interior citations (fable-cutscene-name-slots-and-the-depth-of-fie-homing-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-CUTSCENE-NAME-SLOTS-AND-THE-DEPTH-OF-F` · Package: `_index/candidates/fable-cutscene-name-slots-and-the-depth-of-fie-homing-1003/` · Page: `99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md` (commit eea05327e; reviewed at HEAD f8b2904c0, package and page unchanged since and unmodified in the working tree)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh without `--apply`. It printed `VERIFY 16 functions, 79 anchors`, `ALREADY` and `FAILS 0`. The committed `.out` is the pre-apply `DRY` run with the same counts.
- `rows.json`: 16 rows and 79 anchors, `mode: homing`. Rejected 0, skipped 0, missing 0, corrections 0. All 16 rows are on the page at lines 1858–1873 (heading at line 1852), byte for byte.
- Semantic pass: **all 16 rows** (above the 15 asked) were read clause by clause against `disr.py` output of the certified image (SHA256 73461D08...).
  - **`001B5610`: exact.**
    - `001BA860(rcx+0xd0, rdx)` (+0x29) gives P. `[P+0x20]` = 0. When `rdx != P` it calls `001A5760(P, [rdx], [rdx+8])` (`001B5659`). Then `[P+0x28]` = 0.
    - Q = `001A0A90(001A1220())` (+0x5D / +0x55), and Q gets dword 4, `001B5FE0`, P and byte 0 at `+0`, `+8`, `+0x10`, `+0x18`.
    - Then `001B31E0(rsp+0x28, rdx, [01DF6E08])` (`001B569D`), and `[008C3038](Q+0x20, 0x100, [L])` (`001B56B1` = +0xA1).
    - Q+0x120 and Q+0x128 receive the addresses P+0x20 and P+0x28.
    - Then `001A0BB0(001A1220(), Q, 0)` (+0xB5 / +0xC3).
    - The two releases use the `jle` (signed) "above 1" test and a null test, calling `[[obj]+0x18](obj, [+0], low dword)` with obj = `L+0x18`, then `rdx+0x18` (`001B572A`).
  - **`0033FFC0` and `0034A290`: exact.** The site +0x9 is called with the registers untouched (`VM_ActorSteerToPosition` / `VM_ActorSteerTowardActor`). Then `002EB430(00263F40(rdx))`, then the tail jump at +0x2B (`0026C120`) with `rcx = rdx`, `edx = 2`.
  - **`00348580`: exact.**
    - a and b are the +0x16 and +0x21 results (`00267DB0`, `rcx = r9` each), and id = `00267E10(r9)`. Then `0016D6A0(id)` and `003EB720(id)`, and a null result returns.
    - `comiss a, 0.0` / `jb` skips when a is below 0 or unordered. That is "not below 0.0 (ordered)". Then a = `maxss(b, a)` (`003485D4`, `xmm0 = b`).
    - Then +0x61 (`002EC9C0`) with b and +0x6C (`002EC900`) with a, each in `xmm1`.
  - **`00348A90`: exact.** It is guarded on non-null, then calls +0x40 (`002ECCB0`) with `maxss(0.0, a)` (`xmm1` = 0 as the destination).
  - **`003490F0`: exact.** There is no null check. `mulss a, 002E95B0(P)` (+0x37), then the tail jump at +0x50 (`002E4FE0`).
  - **`00349460`, `003498D0`: exact.** The tail jumps are at +0x26 (`002E4330`) and at +0x24 (call) / +0x31 (`002EC630`).
  - **`0034B0A0`, `0034CCF0`: exact.** Two pops (v = `edi`, then id), then the tail jumps at +0x3E (`002ED3F0` / `002ED3A0`) with `edx = v`.
  - **`0034B710`, `0034BAB0`, `0034D2B0`, `0034D640`: exact.** `00267F90(r9, 1)` (`mov edx, 1`) or `(r9, 0)` (`xor edx, edx`), then the two pops, then the tail jumps at +0x4B, +0x48, +0x4B and +0x48.
  - **`0034BF40`, `0034C900`: exact.** A null-guarded call at +0x39 (`002EC6A0` / `002EC890`) with `edx = v`.
- Advisory (not a defect): in the four push-then-pop rows, `00267F90` is `VMValueStack_PushInt32`, and it pushes only while the count `[rcx]` is below 0x3F (`00267F93 jge`). So v is the constant just pushed (1 or 0) unless the stack was already full. Saying "v (the pushed 1/0)" would make those rows read as the constant they are.
- Advisory (not a defect): in `001B5610`, "stores `P+0x20` and `P+0x28` at qwords `Q+0x120` and `Q+0x128`" means the addresses (`mov [rbx+0x120], r14` with `r14 = rax+0x20`). Add "the addresses" to rule out reading them as the qwords there.
- Limits hold: body statements only, static evidence. The cloud draft and FABLE's re-read are not independent review; this record is.
