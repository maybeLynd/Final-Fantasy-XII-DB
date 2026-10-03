# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-contract-render-record-pool-lifecycle-ee-1003)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-CONTRACT-RENDER-RECORD-POOL-LIFECYCLE-1F125` · Package: `_index/candidates/opus-contract-render-record-pool-lifecycle-ee-1003/` · Page: `17-Presentation-Rendering/CONTRACT-render-record-pool-lifecycle.md` (commit b0c7c5a57)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply`, from the package folder -> `VERIFY 2 functions, 10 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 2 rows, 10 anchors; rejected 0, skipped 2 (`006515C0`, `00659EC0`, too large), missing 0; one recorded OPUS correction (`0065CD60`, sign of the `+0x270` difference), which the shipped sentence carries. Both sentences and anchor lists are present verbatim on the page at HEAD.
- Semantic pass: **every row** read clause by clause against a full linear capstone decode of the certified image (SHA256 73461D08...), extents from the function list (`0018BE70` 0x90 B, `0065CD60` 0x49D B; both decode exactly):
  - `0018BE70` exact: `0085E730(ecx = 0x18, edx = 0, r8d = -1)` (`0018BE90`); non-null -> `001F19E0(rax)` (`0018BEA7`), else `xor ebx, ebx`. Append: `cmp [rdi+8], [rdi+0x10]` / `jae` (unsigned "below"), end += 8 (`0018BEC6`), store skipped on a null old end (`test rdx, rdx`); full -> `001AB570(rcx = v, rdx = old end, r8 = &o)` (`0018BEDC`) and `o` re-read from `[rsp+0x40]`. Tail: `0018AFF0(rcx = 0018B4E0(), rdx = o)` by `jmp` (`0018BEFB`).
  - `0065CD60` exact: `00861EBA` is the `memcpy` import thunk. Per descriptor: `B` = `[[rbx+0x58]+8]` re-read per item; dest `B` + `movzx word [d+0x10]`, length `word [d+0x12] AND 0x1FFF` (`edi` = 0x1FFF); `cmp ecx, [r9]` / `ja` (unsigned) and `cmp dx, 4` / `jb` both reach `0065CF1E` `mov eax, 3`. `f` = `[o+0x84]`, `a` = (1.0 from `01CEBBA8` .rdata - `[o+0x88]`) * `f`; sources `+0x210` `a`, `+0x218` `a`*`a` (`mulss xmm6, xmm6`), `+0x220` `f` (`[rsp+0x78]`), `+0x228` `f`*`f`; `+0x230`..`+0x250` pass `lea r10, [rbx+0x8C/0x90/0xA0/0xB0/0xC0]` with `test r10, r10` -> `0065CF14` `mov eax, 1`; `+0x270` block `[rsp+0x20..0x2C]` = (`[o+0xDC]`, `[o+0xE0]`, `[o+0xE0]` - `[o+0xDC]` (`subss xmm1, xmm0` at `0065D16C`), 1.0 / difference (`divss` at `0065D180`)); `+0x258`/`+0x260`/`+0x268`/`+0x278` call `0060E7A0(rcx = B, rdx = d, r8 = o+0xC4/0xC8/0xCC/0xE4)` and return a non-zero `eax`; `xor eax, eax` at `0065D1DD`.
  - Anchors: all 10 are instruction boundaries strictly inside their bodies and decode to the recorded mnemonics.
- Limits hold: body statements only, static evidence; the drafter and OPUS's re-read are not independent review, this record is.
