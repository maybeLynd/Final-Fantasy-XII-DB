# SWE2-AUDIT-SPEC review: ASTRA filecache zero-handle return

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session) · 2026-10-03 ·
Task: `ASTRA-REQ-SPEC-FILECACHE-ZERO-HANDLE-RETURN-1002` · Package: `_experiments/evidence/filecache-zero-handle-return/`
(publisher commit `5b659b28d`), image pin `73461d08…21f8`.

## SWE2-AUDIT-SPEC verdict: ACCEPT

Scoped as written. There is no leak, natural heap failure, later read fault, lifetime or all-writer conclusion, and
the PE malloc import is a declaration, not a live binding.

## SWE2-AUDIT-SPEC re-derivation from the shipping image

- `0020C300`:
  - `inc dword [rcx+88h]` (`0020C328`) runs unconditionally at entry.
  - Every kind arm then does `inc byte [node+10h]` through `20B5F0` (`0020C354`, `0020C38B`, `0020C3F8`).
  - All of this happens before `call 210EC0` with `ecx=10h` (`0020C400`).
  - A NULL result jumps to `xor eax,eax` (`0020C423`), skipping constructor `217A60`. Nothing undoes the counter or
    byte increments.
- `00210EC0` → `jmp 85E730` → `jmp [rip+64409h]` = IAT `008C2B40` (the malloc import).
- Resolver `0059EE90`: the lookup result is stored as a QWORD at `record+20h` (`0059EFEA`). Only `js` (negative)
  takes the archive fallback. A zero result follows the cache path and returns status 0 (`0059EFF1..0059EFFB`).

## SWE2-AUDIT-SPEC reproduction (disposable copy, repository-root cwd)

- `prove.py` (prove-02, current driver `3d016099`) re-run with no argument: exit 0, stdout identical, output
  **byte-identical** to the retained `result-01.json`, which is the file that driver writes by default.
- `control.py` re-run: exit 0. All five cases are identical to retained: failed cookie capture, missing cookie
  source, failed source qualification, missing retained lookup, and a coherent inverse-NULL-branch mutation that
  gives "original byte mismatch".
