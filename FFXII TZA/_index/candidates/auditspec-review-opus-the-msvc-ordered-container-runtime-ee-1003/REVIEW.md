# SWE2-AUDIT-SPEC review: OPUS interior rows (opus-the-msvc-ordered-container-runtime-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-MSVC-ORDERED-CONTAINER-RUNTIME-EE-1003` · Package: `_index/candidates/opus-the-msvc-ordered-container-runtime-ee-1003/` (request at `693d650d4`, reviewed at HEAD `8fabf1300`) · Page: `24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/the-msvc-ordered-container-runtime.md`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The package has 10 rows, fewer than the 15 the request asks for, so all 10 were read clause by clause against the bytes. All 10 are correct, and so are their 50 anchors. No row changes.

## SWE2-AUDIT-SPEC checks

- **Applier re-run (verify only).** `interior_applier.py` was run without `--apply` (it writes only with `--apply`), from the package directory, under the analysis venv python with `-B`. Output: `VERIFY 10 functions, 50 anchors` / `ALREADY` / `FAILS 0`, exit 0. This matches the committed `.out`. `git status` on the page and the package was clean afterwards.
- **Page text.** Each row's `text` appears verbatim on the page (10 of 10).
- **Anchors.** Every anchor is an instruction boundary in its function's disr listing, has the recorded mnemonic, and sits on the clause it supports. Every listing ends at `ret` at the census size, so none is cut.
- **The five range-erase rows share one sentence.** `00714CE0` was read in full (below).
  - The other four were compared with it by a capstone listing over 0xDA bytes, with branch targets made relative to the function and external call targets named.
  - All have 65 instructions. The only differences are the external call targets:

| fn | call at +0x27 (whole-tree clear) | call at +0xB8 (node erase) |
|---|---|---|
| `00714CE0` | `00714B60` | `00714DC0` |
| `00715110` | `00714BE0` | `00714DC0` |
| `007151F0` | `00714C60` | `00714DC0` |
| `0071F4B0` | `0071F3A0` | `0071F590` |
| `0079B930` | `0079B0D0` | `0079BA10` |

  Each row names exactly its own two targets. The anchors sit at +0x1D, +0x27, +0x50, +0xB8 and +0xD1 in every member.

- **Rows, clause by clause:**

| fn | verdict | decisive instructions |
|---|---|---|
| `0070E520` | correct | `cmp byte [rcx],0` / `je` at `0070E524`. On the non-zero path, `cmp dword [01F3BA80],1` / `jb` and the same for `01F3BA90`, so both must be non-zero. Then `006DF480(00D95EA8, edx=0x72bb)`, then `006DF480(00D95EF0)` with edx not reloaded. Returns `0x80004005`. Zero path: rdi = rcx+0xa8, head = `[rdi]`, start at the head's `+8`. Loop `0070E583`: `cmp [rcx+0x20],rdx` / `jae` records the node and goes `+0`, otherwise goes `+0x10`; the walk stops at byte `+0x19` ≠ 0. `0070E59B..A6`: if the node is the head or `rdx < key`, it becomes the head, and the head path returns `0x80070057`. Found: a non-null `[rbx+0x28]` gets `call [vtbl+8]`, then `00714DC0(rdi, rsp+0x30, rbx)`, and the function returns 0. |
| `00714CE0` | correct | `cmp r8,[head]` / `cmp r9,head` at `00714CFD/D02`. At the `00714D07` call to `00714B60`, rcx, rdx, r8 and r9 still hold the incoming values. Then `[rdi] = [[rbx]]+0` (rdi = rdx). Otherwise `cmp r8,r9` / `je` before the first iteration. Byte `+0x19` of the current node is checked at `00714D30`; when set, the home slot `[rsp+0x40]` (= the r8 home) keeps its value. Successor: leftmost through `+0` of the `+0x10` subtree (`00714D3A..5C`), or else the ancestor walk through `+8` while the node is that parent's `+0x10` (`00714D63..88`). In both walks a node with byte `+0x19` set stops the walk. The ancestor walk records that stopping node, which is the head/end. Then `00714DC0(rcx, rsp+0x30, current)` and `cmp r8,[rsp+0x48]` (r9 home). It finishes with `[rdi] = r8` and returns rdi. |
| `00715110`, `007151F0`, `0071F4B0`, `0079B930` | correct | Same form as `00714CE0`, with the callee pairs in the table above. |
| `0071CD10` | correct | rsp = r11 - 0xc8. The 16-byte `movdqa` from `00D9B600` goes to `rsp+0x30`; dwords 1 go to `rsp+0x40/44`. The three strings: capacity 0xf at `r11-0x68/-0x48/-0x28` = `rsp+0x60/0x80/0xa0`, length 0 at `rsp+0x58/0x78/0x98`, zero byte at `rsp+0x48/0x68/0x88`. Each is +0x18/+0x10/+0 of `rsp+0x48`, `rsp+0x68` and `rsp+0x88`. Qwords `[rcx+0x50]` and `[rcx+0x48]` are zeroed. `0071D170(rcx, rsp+0x30)`, `jne`, then `0071D9E0(rbx, rsp+0x30)`, `jne`. Dword copies 0x3c→0x4c, 0x40→0x50, 0x44→0x54. Always `0071EF10(rsp+0x30)`; returns edi (0, or the first non-zero result). Cookie at `0071CDE6`. |
| `0071E340` | correct | At the call to `0071F180`, rcx, rdx, r8 and r9 are the incoming values (rsi only copies r8). Word `[rax+0x18]` = 0. `test rbx,rbx` on `p+0x20`. rdx = `[rsi]` = qword `[r8]`. Capacity 0xf at `+0x18`, length 0 at `+0x10`, zero byte. `001A4C90(rcx=p+0x20)`. Then the same three stores at `p+0x40`. Returns rdi = p. |
| `0071EE70` | correct | String at `rcx+0x20`: `cmp [rcx+0x38],0x10` / `jb`. When it is not below, `001DFA10(rdi, [rdi], cap+1)`. Then capacity 0xf, length 0, zero byte. The same for the string at rcx (`[rbx+0x18]`). The byte store goes through the `cap>=0x10` re-test, which is false after cap = 0xf, so it lands in the inline buffer. |
| `0071F3A0` | correct | rsi = root = `[[rcx]+8]`. Loop while byte `+0x19` = 0: `0071F1E0(rdi, [rbx+0x10])`, rbx = `[rbx]`, `0071EE70(rsi+0x20)`, `00210EB0(rsi)`. After the loop the head's `+8`, `+0` and `+0x10` are set to the head in that order, and qword `[rdi+8]` = 0. |

## SWE2-AUDIT-SPEC narrowing / notes

No narrowing. Non-blocking:

- In the shared range-erase sentence, "a node whose byte `+0x19` is non-zero ending each walk" does not say whether the stopping node is the one recorded. In the leftmost walk the last real node is recorded. In the ancestor walk the stopping node itself (the head, i.e. `end()`) is recorded (`00714D88`). This is the standard successor, so the sentence is not false. A reader who wants the exact rule needs that distinction.
