# SWE2-AUDIT-SPEC review: FABLE interior citations (fable-how-a-path-is-resolved-to-bytes-cloudint-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not FABLE, not the drafting cloud session) · 2026-10-03 · Task: `FABLE-REQ-AUDITSPEC-FABLE-HOW-A-PATH-IS-RESOLVED-TO-BYTES-CLOUDI` · Package: `_index/candidates/fable-how-a-path-is-resolved-to-bytes-cloudint-1003/` (asked at `208c17694`, reviewed at HEAD `33eb7192f`; the package is unmodified in the working tree) · Page: `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/how-a-path-is-resolved-to-bytes.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

All 4 rows (fewer than 15, so all were read) are exact against the full listings, clause by clause, including the stack-argument slot, compare signedness and the tree-descent polarity.

## SWE2-AUDIT-SPEC checks

- **Applier re-run.** `interior_applier.py` was re-run fresh from the package directory with the analysis venv python. It exited 0 and printed `VERIFY 4 functions, 16 anchors` / `ALREADY` / `FAILS 0`. It wrote nothing. The section is on the page at line 553, and its 4 rows match `rows.json`.
- **FABLE's four corrections** change only the site form (`FN+0xNN` to `` `FN` + 0xNN ``). The content is unchanged.
- **`001D6B70` (0x1B B).** `call 001DADA0` at +0x4. No argument register is written before it. Then `xor ecx, ecx / cmp byte [rax+0x88], cl / setne cl / mov eax, ecx`. Exact.
- **`001D6D20` (0x4F B):**
  - The incoming `rcx`, `edx`, `r8` and `r9` are saved to `rbp`, `esi`, `rdi` and `rbx`. Then `call 0020C700` at +0x1F, with no argument register written.
  - Then `rcx` = the result, `[rsp+0x20]` = `rbx` (incoming `r9`, the fifth argument slot), `r9` = `rdi` (incoming `r8`), `r8d` = `esi` (incoming `edx`, 32-bit), `rdx` = `rbp` (incoming `rcx`), and `call 0020C1B0`. Its `rax` is returned.
  - Exact.
- **`001DB050` (0x18A B):**
  - The loop runs while `rbp < 0x18`, with `rbp` += 6 and `rdi` += 6 per pass. That is four names from `01DFCFE8`, which reads `c1004\0c1005\0c1006\0c1019\0` in the image.
  - `memset(rsp+0x20, 0, 0x100)` at +0x4D. A strcpy loop copies `01DFD010` = `PS2Data\obj_finish\in\chara\c10\`, a strcat loop appends the name, and the word at `008FB2B0` (`5C 00`) is stored at the end (`001DB115`).
  - `rax` = strlen(`rsi` = incoming `rdx`) and `rbx` = strlen(built). `cmp rax, rbx / jbe` skips to the next name, so the second step happens only when the string is longer (unsigned).
  - The second step: `memset(rsp+0x120, 0, 0x100)` at +0xFE, then `call [008C2F70]` at +0x111 with (second buffer, `rsi`, `rbx`).
  - The byte-compare loop runs until a difference or a zero in the second buffer. On equality it jumps to `001DB1D3` (`mov eax, 1`). After four passes it falls through to `xor eax, eax`.
  - `rcx` is first written at `001DB092` and never read before that.
  - Exact.
- **`001F47D0` (0x6D B):**
  - `r10` = `rcx+8` (sentinel). The first node is `[r10+0x18]` = `[rcx+0x20]`. The key is `r8` = `[rdx]`, `r9` = `[rdx+8]`.
  - The `jl` / `jg` / `jge` compares are signed.
  - Node less than key gives `eax = 0xFFFFFFFF`, then `shr rax, 0x1F` = 1, then `[node+8]`. Node greater gives `eax = 1`, then 0, then `[node+0]`.
  - On equality of both qwords the body reaches `001F4821`: `rax = node+0x28` (non-null), `rdx = [node+0x28]`, `jmp 001F4250` at +0x64, with `rcx` untouched.
  - When the sentinel is reached, `rdx = r11 = 0`. `cmove` gives 0, and the body returns 0.
  - Exact.
- **Anchors.** All 16 decode to the recorded mnemonic and sit on the instructions their sentence describes.
- **Page fit.** All four are cited by entry in the page's main sections: §5 line 177 (`001D6D20`), §6 line 373 and the R8 falsification (`001F47D0`), and the §8 selector discussion, lines 439-450 (`001D6B70`, `001DB050`). Interior citations belong here.
- **Note (non-blocking, page prose outside this package).** Line 450 says `001D6B70` "returns byte `+0x88`", and line 439 says "`001D6B70()` is positive". The body returns the normalised 0/1 of that byte (`setne`), as this package's row says. Line 450 could read "returns whether byte `+0x88` ... is non-zero".
- Limits: body statements only, static evidence. A cloud draft plus FABLE's re-read is not independent review; this record is.
