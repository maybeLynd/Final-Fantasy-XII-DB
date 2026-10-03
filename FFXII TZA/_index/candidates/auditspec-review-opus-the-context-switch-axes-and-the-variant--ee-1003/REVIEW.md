# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-the-context-switch-axes-and-the-variant--ee-1003)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-CONTEXT-SWITCH-AXES-AND-THE-VARIA-FA1E9` · Package: `_index/candidates/opus-the-context-switch-axes-and-the-variant--ee-1003/` · Page: `22-Middleware-PhyreEngine/Shader-Variant-Selection/the-context-switch-axes-and-the-variant-key.md` (commit b0c7c5a57)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply`, from the package folder -> `VERIFY 2 functions, 10 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 2 rows, 10 anchors; rejected 0, skipped 0, missing 1 (`006B9630`, not rowed). Both row sentences and anchor lists are present verbatim on the page at HEAD.
- Semantic pass: **every row** read clause by clause against a full linear capstone decode of the certified image (SHA256 73461D08...), extents from the function list (`006B8D20` 0x84 B, `006B8F70` 0xDE B; both bodies decode exactly):
  - `006B8D20` exact: `r10` = qword `[rcx+8]`; null -> `lea eax, [r10+0x11]` = 0x11 (`006B8D30`). Head = qword `[02E522D0]` (.data, mutable; `006B8D3D`); node string = qword `[n+8]`; byte loop `movzx edx, [rax]` / `movzx ecx, [rax+r8]` with `r8` = `r10 - rax` (`006B8D60`/`006B8D63`), exits on a difference or on the terminator; equal -> `mov eax, 0x12` (`006B8D96`); next = qword `[n+0x10]` (`006B8D77`). No match (or empty list) -> `[r11+0x10]` = old head `rbx` (`006B8D80`), `[02E522D0]` = `rcx` (`006B8D8A`), returns 0.
  - `006B8F70` exact: count loop over qword `+0x10` from `[02E522D0]` (`006B8F95`); `cmp ebx, [rdx]` / `je 006B9017` goes straight to the copy loop (`006B8FA5`). Non-zero count: `0017D260(count << 3, 8)` (`rcx` = `r14` = count*8, `edx` = 8; `006B8FBC`); null with a non-zero count -> `006B9047` `mov eax, 0xd`; non-null -> `rep stosq` of count qwords (`006B8FDE`). Free gate: old `[rsi+8]` != new (`006B8FF0`), sign bit of dword `[rsi]` clear (`shr eax, 0x1f` / `not al` / `test al, 1`), non-null -> `call 00584730` (`006B9005`). Stores `[rsi+8]` = new (0 for a zero count, `rbp` = 0) and dword `[rsi]` = count; copy loop writes each node pointer to consecutive qwords from `[rsi+8]` (`006B9020`), returns 0 (`006B9030`).
  - Anchors: all 10 are instruction boundaries strictly inside their bodies and decode to the recorded mnemonics.
- Limits hold: body statements only, static evidence; the cloud draft and OPUS's re-read are not independent review, this record is.
