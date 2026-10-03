# SWE2-AUDIT-SPEC review: ASTRA filecache insert-key admission

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the Devin session while it is rate-limited) · 2026-10-03 ·
Task: `ASTRA-REQ-SPEC-FILECACHE-INSERT-KEY-ADMISSION-1002` · Package: `_experiments/evidence/filecache-insert-key-admission/`
(publisher commit `1b2154feb`), image pin `73461d08…21f8`.

## SWE2-AUDIT-SPEC verdict: ACCEPT

Scoped to the package's own stated limits: the result is STATIC_ONLY and conditional on its premises.

## SWE2-AUDIT-SPEC re-derivation from the shipping image (capstone, `disr.py`, not the producer's tools)

- `001D6A20`: `mov ebp,ecx` at `001D6A3D`, the `20C700` receiver call, then `mov edx,ebp` at `001D6A51` into `20B680`.
  `rdx→r8`, `r8d→r9d`, `r9d→[rsp+20h]` (fifth arg). The data, size and kind carriers are distinct. Nothing in the body
  masks or recomputes the key.
- `0020B680`: `mov [rsp+10h],edx` happens before the 7 pushes (56 B) and `sub rsp,40h` (64 B), so the entry home
  `SP+10h` is the current `SP+88h`. The fifth arg is read at `[rsp+0A0h]` (entry `SP+28h`), at `20B70F` and `20B761`.
  The tree walk uses `cmp [rax+20h],ebp / jb` and `cmp ebp,[rbx+20h] / jae`, which is unsigned, full DWORD. The
  existing arm passes `mov edx,ebp` to `20C300` (`20B721`). The new arm passes `lea rdx,[rsp+88h]` to `20B5F0`
  (`20B7D0`). The only own stack writes before that call are `[rsp+30h]` (qword) and `[rsp+90h]` (qword), and neither
  overlaps `88h..8Ch`. The kind arms are 5, 3 and other.
- `0020B5F0`: reads `[rdx]` as a DWORD, compares it unsigned, and copies it to the private pair `[rsp+30h]` with
  `[rsp+38h]=0` (qword). It passes `r9=&pair` to `1AE9B0` and returns `node+28h`. The caller stores the descriptor
  there (`20B7E1`).
- All five 16-byte pair copies follow the same shape: allocator `call [rax+10h]` with `edx=30h`, `add rax,20h / je`
  (null guard), then `movups xmm0,[pair]` and `movups [node+20h],xmm0`. The sites are `1AEA28`, `1AEAA4`, `1AE91A`,
  `1AE95B` and `20BAD1`. The pair register traces to the caller's `r9`: `1AE9B0` has `r14=r9`, passes `r8=r14` into
  `1AE850` (`r15=r8`) and `r9=r14` into `20BA70` (`rbp=r9`).
- `0016D840` (size `214h`): every write is a qword at `+0/+8/+10h` or a byte at `+18h`, so the footprint is `0..19h`.
  The body has no calls, and nothing reaches `node+20h..30h`.

## SWE2-AUDIT-SPEC reproduction (disposable copy at the ASTRA directory depth)

- `prove.py result-02` re-run: exit 0, stdout identical, result **byte-identical** to the retained `result-02.json`.
- `control.py` (controls-02) re-run: exit 0, stdout identical. All five refusals are the same as retained
  (failed or incomplete storage capture, missing `source-02`, failed archived positive, and a coherent balancer
  key-overlap mutation that gives "original byte mismatch"). Each one has its result absent. The controls-02
  receipts differ only in absolute paths and the freeze step's curation.

## SWE2-AUDIT-SPEC limits (unchanged from the package)

- No natural high-bit caller keys.
- No allocator callback, `20C300`/`20B0F0`/lock effects, replacement or lifetime.
- No whole-OV closure.
