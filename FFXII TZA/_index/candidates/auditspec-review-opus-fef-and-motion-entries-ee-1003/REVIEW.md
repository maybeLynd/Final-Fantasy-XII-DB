# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-fef-and-motion-entries-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-FEF-AND-MOTION-ENTRIES-EE-1003-0BF8C` · Package: `_index/candidates/opus-fef-and-motion-entries-ee-1003/` (reviewed at HEAD `a028be1b9`) · Page: `17-Presentation-Rendering/Model-And-Motion-Formats/fef-and-motion-entries.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 1 row. It was read clause by clause against a raw capstone decode of the certified image. This session checked the image hash: SHA256 `73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`. The row holds as written. No narrowing is needed.

## SWE2-AUDIT-SPEC checks

- **Applier dry check.** `interior_applier.py` was invoked from the package directory with the venv python and without `--apply`. It printed `VERIFY 1 functions, 5 anchors` / `ALREADY` / `FAILS 0` and exited 0. The row is already in the page block `## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)`, line 1033 (heading at line 1029).
- **Counts.** 1 row, 5 anchors. The listing (`00319E40`-`00319F40`, function-table size 0x101) ends in `ret` followed by int3 padding.

Per row:

- **`00319E40`**: exact.
  - `00319E4B`-`00319E55`: cookie `01F44830` XOR `rsp` stored at `rsp+0xA0`; `00319F25`-`00319F30` reload it, XOR `rsp`, and call `00808C40`. `00808C40` was read: it is `__security_check_cookie` in the function table and starts `cmp rcx, [01F44830]`.
  - `00319E5D`/`00319E60`/`00319E65`: `o` = `rcx`, `v` = `eax` of `0030CA50(o)`.
  - `00319E68`-`00319E6E`: `lea ecx,[rax+1]`, `cmp ecx,1`, `jbe` (unsigned) to the epilogue, so `v` = 0 or -1 returns.
  - `00319E88`/`00319E8F` and `00319ED4`/`00319EDB`: `i` compared against dword `[o+0x77C]` with `jle`/`jl` (signed), the dword re-read on each pass.
  - `00319EAA`/`00319EB1`/`00319ED0`: `p` = qword `[o+0x780+16i]` (`rdi` steps by 0x10). `00319EB4`/`00319EB7` skip null `p`; `00319EB9` `e` = `00263E30(p)`; `00319EBE`/`00319EC1` skip null `e`.
  - `00319EC3`-`00319ECA`: dword `[e+8]` appended at `rsi` (from `rsp+0x20`, step 4), `n` = `ebp` incremented. The array spans `rsp+0x20` up to the cookie at `rsp+0xA0`, 0x80 bytes = 32 dwords. No instruction compares `ebp` or `rsi` against a bound; the only loop exits are the `i` compares above.
  - `00319EED`-`00319EFF`: `n` = 0 skips; otherwise `002EAD00(dword [o+8], n, rsp+0x20, v)`.
  - `00319F04`-`00319F10`: `00237420()`, nonzero calls `0024ED50(v)`. `00237420` was read: it takes no register argument (`xor eax,eax`, `cmp [02089350],rax`, `setne al`, `ret`), so the empty argument list holds.

**1 of 1 exact.** All 5 anchors were checked.

## SWE2-AUDIT-SPEC limits

- Body statements were checked against the bytes. Meanings were not reviewed.
- Callee behaviour was read only where the row depends on it: `00808C40` (cookie check) and `00237420` (arity). Callees the row names only as calls are opaque here: `0030CA50`, `00263E30`, `002EAD00` and `0024ED50`.
- "No bound on the count" is a body statement: the 32-dword array can overflow if dword `[o+0x77C]` exceeds 32 with non-null entries. Whether any caller lets that happen was not reviewed.
- This review is a non-author read. It does not replace a live check of any behaviour.
