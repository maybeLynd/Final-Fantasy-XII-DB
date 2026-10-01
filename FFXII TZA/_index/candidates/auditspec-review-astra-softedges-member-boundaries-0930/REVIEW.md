# SWE2-AUDIT-SPEC review of ASTRA phyretext-member-boundaries (7a524fda9): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75, 2026-09-30). Reviewed: ASTRA's packet
`_experiments/evidence/phyretext-member-boundaries/` at `7a524fda9`, Method A (static only), three bounded source
claims. EXE `73461D08…21F8`. Everything below was read from the EXE directly (`mb_exe.py` via tk.py and pefile), not
from the packet's captures.

| request | reviewed task | commit | verdict |
|---|---|---|---|
| ASTRA-REQ-SPEC-SOFTEDGES-MEMBER-BOUNDARIES-0930 | ASTRA-PUBLISH-SOFTEDGES-MEMBER-BOUNDARIES-0930 | `7a524fda9` | ACCEPT (the three bounded claims; no installed-array, initialization, cleanup or lifetime acceptance) |

**Clause by clause** (from `mb_exe.out`, `mb_resolver_tail.out`, `mb_controls.out`)

- *`005EEDAF` literal m_els.* In registration `005EEB20`: `005EEDAF lea r9` -> `00D32DC0` "m_els". It is passed
  with `rcx` = `02CEA610` (a zero-initialised .data tail cell) into `00632A10`.
- *Native registration `005EEDCC`/`005EEDF6`.* `005EEDCC lea rax` -> `00D4BD30` (.rdata), stored by `005EEDD3` to
  [`02CEA610`], the metadata object. `005EEDEF lea rax` -> `0060F280`, stored by `005EEDF6` to [`02CEA680`], which is
  metadata+0x70. The qword at `00D4BD30`+0x40 is `0060F3D0` (slot 8 of the table).
- *Dispatcher `0060F3D0`..`0060F3F1` (33 B, listed size 33).* `mov rax, [rcx+0x70]`. If it is null, `mov eax, 0x15; ret`
  (21). Otherwise `r8d <- r9d`, `rdx <- r8`, `rcx <- rdx`, `jmp rax`. So there are two exits, and the callee gets
  RCX = the supplied object, RDX = the supplied source and R8D = the count, the dispatcher's own arguments 2-4 shifted
  down by one. It adds no member-offset or class-F4 displacement. It reaches `0060F280` only while metadata+0x70 still
  holds the registered value; mutation/lifetime is not observed (as the packet says).
- *Callback `0060F280` (16 B) and XOR suppression.* `sub rsp,0x28; call 0060EFE0; xor eax,eax; add rsp,0x28; ret`, so
  the inner status is overwritten with 0.
- *Negative signed count -> 5, no write.* `0060EFE0`: after register moves only, `test r8d,r8d; jns`. On the negative
  path: `mov eax, 5`, restore, `ret`. The only stores before it are the rbx/rsi spills into the caller's home area, with
  no array read or write. On the nonnegative path, old [rcx+8] differs from source and bit 31 of [rcx] is clear, so it
  calls `005F03A0`; then `bts ebx,0x1f`, `[rdi+8] = source`, `[rdi] = count|0x80000000`, `xor eax,eax`. A negative
  count thus yields outer 0 with no array write, as claimed.
- *`0059EC40` seven-fragment continuation.* pefile's .pdata has 7 contiguous entries `0059EC40..0059EC53`,
  `..0059EC5B`, `..0059EC77`, `..0059ECCC`, `..0059ECF2`, `..0059ED0B`, `..0059ED61`. The first is primary (flags 0)
  and the other six carry UNW_FLAG_CHAININFO back to earlier fragments; the next entry, `0059ED70`, is a separate
  function. Past `0059ED61` there is only the `0059ED52` xor-eax zero exit and its epilogue, so the body is complete.
- *EAX modulo 32, then 64-bit add.* `0059ED1C ebx = [child+0xF4]` (guarded by the null test at `0059ED17`),
  `0059ED33 eax = [parent+0xF4]`, `0059ED39 sub ebx, eax`, `0059ED3B add dword [r12], r14d` (the residual, modulo 32),
  `0059ED3F lea eax, [rdx+rbx]` (32-bit destination, zero-extended), `0059ED42 add rax, r13` (64-bit). So the return
  is (object + zext32(memberNativeOffset + childF4 - parentF4)) mod 2^64. The packet's example gives delta
  0xFFFFFFF8, not -8. That is an ISA-width fact, not a claim that those values occur.

**Re-run.** `check-softedges-member-boundaries.py <packet> <fresh>`: exit 0. The result equals
`softedges-member-boundaries-result-02.json` exactly (`rerun_check.out`, `rerun-result.json`). The packet dir was clean
before and after.

**Controls** (`mb_controls.py`; all on disposable copies under C:\t\auditspec, since removed)

- The packet's three refusals reproduce:
  - missing callback source (exit 1; an uncaught FileNotFoundError, no result);
  - continuation missing its last range ("normal resolver continuation unverified/incomplete");
  - callback `xor eax,eax` -> 2-byte NOP with the span hash recomputed ("status propagation changed").
- Also refused: dispatcher null return 0x15 -> 0x16 with the hash recomputed ("dispatcher boundary changed"), and the
  `0059ED3F` args text changed from eax to rax.
- Checker limit. All 313 instructions in the four retained captures match the EXE bytes and a fresh capstone decode,
  and the checker's two hard-coded byte strings equal the EXE. So the claims stand on the shipped bytes. But the
  checker ties only those two ranges and the three registration `lea` displacements to bytes. Two bytes-only mutations
  pass it (exit 0, result written) while the text is kept and the span hash recomputed:
  - the width-bearing `0059ED42 add rax, r13` -> `add eax, r13d`;
  - `0060EFFD mov eax, 5` -> `mov eax, 0`.

  The span hash is computed from the same file, so it does not bind to the EXE. The README's hash-updated refusal is
  accurate for the callback range only.

**Suggested limit wording for ASTRA (optional; the claims need no correction).** "The checker verifies exact bytes
only for the dispatcher/callback ranges and the three registration displacements. The resolver width (`0059ED3F` /
`0059ED42`) and the `0060EFE0` negative-count exit are checked as recorded instruction text, and the span hashes are
self-computed. Matching the captures to the EXE is a separate step (done in auditspec-review-astra-softedges-member-
boundaries-0930)."

**Not reviewed** (per the request): installed arrays, natural initialization, `005F03A0` cleanup effects, aliases,
lifetime, loaded-resource binding, key 22/27 terminal-member reach and class censuses.
