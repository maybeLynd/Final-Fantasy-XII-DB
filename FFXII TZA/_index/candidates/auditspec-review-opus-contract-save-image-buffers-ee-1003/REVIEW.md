# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-contract-save-image-buffers-ee-1003)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-CONTRACT-SAVE-IMAGE-BUFFERS-EE-1003-A93B3` · Package: `_index/candidates/opus-contract-save-image-buffers-ee-1003/` · Page: `19-Save-Load-Settings/CONTRACT-save-image-buffers.md` (commit 6a9eb7555)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 3 functions, 15 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 3 rows, 15 anchors; rejected 0, missing 0; mode `ee`, no family (the family-declaring-page rule does not apply).
- Semantic pass: **every row** (3 of 3) read clause by clause against a capstone decode of the certified image (SHA256 73461D08...). Each extent is one .pdata entry equal to the kit's function size.
  - `005FCF20` (129 B) exact:
    - The epoch is `gs:[0x58]`[dword `02EAED3C`] + 4.
    - At `cmp [02CC0400], eax` / `jle` (signed) the code enters `008092FC(&guard)` and re-tests -1.
    - It then calls `005CC8A0(02CC03D8)`, `00808B90(008ACDA0)` and `0080929C`.
    - Both paths return `02CC03D8` (`mov rax, rbx` / `lea rax`).
  - `00622010` (460 B) exact:
    - `E` selection uses `btr eax, 0x1f`; `cmp 1` / `jbe` (unsigned above 1), then nonzero, then 0.
    - The slot index is `mov eax, edx` (zero-extended) and `imul r14, rax, 0x58`, with `p` = `[r14+E+0x28]`.
    - `n` is `shr eax, 1; test al, 1` (the 0x2 bit), then `cmovb` against 0xB (unsigned min). `d` = `[005FD050()+0x110]`.
    - The loop runs `l` = 0..`n` inclusive (`inc ebp; cmp ebp, r13d; jbe`, so `n`+1 calls).
    - Each call is to `[[d]+0x180]` with `rcx` = `d`, `rdx` = `[r14+E]`, `r8d` = `l`, `r9d` = 0, `[rsp+0x20]` = `p`, `[rsp+0x28]` = `((dword [f+0x14]*w')*k) >> 3` and `[rsp+0x30]` = 0. The 4-alignment and `k` = 4 apply under `test byte [f+0x18], 1`.
    - `p` += `(dword [f+0x14]*w'*h') >> 3`, with no `k`: 32-bit `imul`s, zero-extended, then `shr rax, 3`.
    - `w` and `h` are halved with a floor of 1 (`cmova`).
    - After the loop, only when the masked count == 1 (`jne` skips), it calls `00584730([E+idx*0x58+0x28])` and stores qword 0 there.
    - No return value is set.
  - `007A05D0` (485 B) exact:
    - `s` = `rsp+0x80` (`00615BC0`), and `a`/`b`/`c` = `rsp+0x88`/`0x90`/`0x98`. These are the incoming home slots, still the stack, so "stack object" holds.
    - The equality test of `+0xD24`/`+0xD28` against `a`/`b` leads to `007A0790`, which calls `001825A0()` and sets `esi` = 0.
    - Next comes `006278B0(00624670(&s), +0xD24, +0xD28)`; a nonzero result goes to the exit.
    - `005CDAA0(ecx = 0+2, 01CB3160 '======== Call resize w = %d,h = %d =======\n' .rdata, +0xD24, +0xD28)`.
    - Then `0060F6B0(rcx+0xE8, 0, 0, +0xD24, +0xD28, 0)`; a nonzero result goes to the exit.
    - The loop test is `test [+0xDB8], 0x7fffffff` / `jbe` (skips the loop at a masked 0), and the loop runs while `i` < the masked count (unsigned). `t` = `[[+0xDC0]+8i]`.
    - When both `[t+0x2C]` and `[t+0x30]` are nonzero, there are four `imul`-then-`div dword` steps (`xor edx, edx`; unsigned). The results stay in registers and are never stored to `t`.
    - It calls `007A10A0(t, x, y, w, h)` (`edx`, `r8d`, `r9d`, `[rsp+0x20]`), then `[[t]+0x20](t)`; a nonzero result goes to the exit.
    - Every path passes `00616700(&s)` at `007A0797` before `ret`.
  - All 15 anchors (`005FCF4A` cmp, `005FCF59` / `005FCF71` / `005FCF7D` / `005FCF8A` call; `00622055` imul, `0062207B` call, `006220FD` call, `00622139` add, `00622190` call; `007A05F3` call, `007A0663` call, `007A06B0` call, `007A070A` div, `007A0760` call) are strictly inside their extents with those mnemonics.
- Both OPUS corrections (signed guard test; no write-back to `t` and the masked-0 path) are in the applied sentences and match the bytes.
- Limits hold: body statements only, static evidence. OPUS's re-read is not independent review; this record is.
