# SWE2-AUDIT-SPEC review: OPUS cloud-drafted interior citations (opus-the-music-control-file-and-the-bgm-strea-ee-1003-2)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-THE-MUSIC-CONTROL-FILE-AND-THE-BGM-ST-67E5A` · Package: `_index/candidates/opus-the-music-control-file-and-the-bgm-strea-ee-1003-2/` · Page: `18-Audio/the-music-control-file-and-the-bgm-stream.md` (commit 81c16b70b)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 2 functions, 10 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 2 rows, 10 anchors; rejected 0, missing 0.
- Semantic pass: **every row** read clause by clause against a full linear decode of the certified image (SHA256 73461D08..., capstone, function-list extents):
  - `00220600` exact (161 B): `cmp dword [rcx+0x48], 0` / `jbe` (`00220620`) to `xor eax, eax`, so a zero count returns 0. Node `rbx` = qword `rcx+0x30`; `rsi` = node qword `+0x20`, also saved at `[rsp+0x50]`; `dec dword [rcx+0x48]` (`0022062F`); `0016D6D0(node)`; `0016DA60(node, rcx+0x28)`; `lea rcx, [rdi+0x50]` then `call [[rcx]+0x18]` with `rdx` = node, `r8d` = 0x28 (`00220656`), so the object is embedded at `+0x50`, as the row's "the object at `rcx+0x50`" says; `00199DB0(rcx+0x58, &[rsp+0x28], &saved, movzx byte saved)` (`0022066D`); `rsi` null -> `xor eax, eax`, else `00225830(rsi)` (`0022067F`), and its full `rax` is returned. The value passed on is the register copy `rsi`, not a re-read of the slot `00199DB0` received, so "the saved qword" is exact.
  - `007A7010` exact (474 B): qword `[rcx]` zero -> returns that zero `rax` (`007A7021`). Low byte: `cmp al, 2` / `je`; `lea ecx, [rax-8]` / `cmp cl, 1` / `jbe` (8 or 9, unsigned); `cmp al, 7` / `jne` -> `xor eax, eax` return. The pairs are as stated: 7 `007BC2A0`/`007BC2B0`, 2 `007B44B0`/`007B44C0`, 8 `007B7950`/`007B77E0`, 9 `007B8050`/`007B7FD0`. The lock goes through `call [008C20B8]` and comes back through `call [008C20C0]` (both .rdata IAT slots) on every path past the getter: four exits for type 7, one for the others. The handle is copied to `[rsp+0x30]` and `rcx` = its address. Type 7: vtable `+0x10`, result 0 -> 0, 1 -> 1, 3 -> 3, else `edi` = 2; null lookup -> `edi` = 0. Types 2/8/9: vtable `+0xA8` (`007A71A8`), null lookup leaves `esi` = 0; 0 -> 0, 1 -> 1, else `sete dil` on `esi == 4` (`007A71C9`) with `rdi` zeroed at `007A711B`, then `lea eax, [rdi+2]` -> 3 or 2.
  - Anchors: all ten are instruction boundaries strictly inside their bodies and decode to the recorded mnemonics.
- Limits hold: body statements only, static evidence; the cloud draft and OPUS's re-read are not independent review, this record is.
