# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-spp-map-sound-list-ee-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for Devin; not OPUS, not the drafting cloud session) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-SPP-MAP-SOUND-LIST-EE-1003-0666A` · Package: `_index/candidates/opus-spp-map-sound-list-ee-1003/` · Page: `18-Audio/Sound-Bank-And-Voice-Formats/spp-map-sound-list.md` (commit 81c16b70b)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

The package has 2 rows, fewer than 15, so both were read clause by clause against the full listings. All 10 anchors are correct. `007A7010` is correct as written. `003DF2C0` has every value, callee and store right, but the sentence puts the `003DF360` call, the `+0x18` clear and the byte `+0x10` = 4 store inside the "when the new `+0x18` pointer is non-null with a non-zero word `+0x10`" condition. In the bytes that condition skips only the `0032F3A0` call. The narrowing is wording only.

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh from the package folder without `--apply` (`python -B`). Output: `VERIFY 2 functions, 10 anchors`, `ALREADY`, `FAILS 0`, exit 0. `git status` on the package and the page was clean afterwards (HEAD `b5028e7e9`).
- `rows.json`: 2 rows, 10 anchors; rejected 0, skipped 0, missing 0, corrections 0.
- Semantic pass: **every row** read clause by clause against `disr.py` / `disw.py` output of the certified image (SHA256 73461D08...):
  - `003DF2C0` correct in every value; scope narrowed below. `movsxd rbx, ecx` (`003DF2C6`, the record pointer). `0036B970(rcx = [rbx+0x18], rdx = rsp+0x20, r8d = 2)` (`003DF2D8`); the buffer is read as two qwords `[rsp+0x20]`/`[rsp+0x28]`, so it is 16 bytes. `test eax`/`je` to the return (`003DF2DF`). Stores to `+0x18` (`003DF2E6`) and `+0x20`, then `test rbx`/`je` to the return (`003DF2F6`). The condition: `[rbx+0x18]` null -> `003DF333`, word `[rax+0x10]` == 0 -> `003DF333` (`003DF2FF`, `003DF30B`). Inside it: `ecx` = `movsx` byte `+0x11`; `edx` = `r8d - 10*trunc(r8d/10)` with `r8d` = `movsx` word `[rax+0x12]` (`imul` 0x66666667, `sar 2`, sign fix-up; `003DF316..2B`), a signed remainder; `0032F3A0` (`003DF32E`). **`003DF333` is the join of both outcomes**: `003DF360(ecx = movsx byte +0x11, edx = movsx byte +0x12, r8 = [+0x18], r9 = [+0x20])` (`003DF343`), `[+0x18] = 0`, byte `[+0x10] = 4` (`003DF350`), return. So the `003DF360` call and both stores also run when the pointer is null or its word `+0x10` is zero. The sentence's "and when ... calls `0032F3A0` ..., then calls `003DF360` ..., clears `+0x18`, sets byte `+0x10` to 4" reads as all of them sharing the condition.
  - `007A7010` correct. `[rcx]` == 0 returns 0 (`007A701F`). Type dispatch on `al`: 2 (`007A7034`), 8/9 via `lea ecx,[rax-8]`, `cmp cl,1`, `jbe`, 7 (`007A7048`); anything else returns 0 (`007A7108`). Each type calls its getter and `EnterCriticalSection` (IAT `008C20B8`), then the lookup on a stack copy `[rsp+0x30]` of `[r14]`: 7 = `007BC2A0`/`007BC2B0`, 2 = `007B44B0`/`007B44C0`, 8 = `007B7950`/`007B77E0`, 9 = `007B8050`/`007B7FD0`. State: type 7 through `call [rdx+0x10]` (`007A707C`), others through `call [rdx+0xa8]` (`007A71A8`), 0 when the lookup is null (`007A7074`, `007A71A0`). `LeaveCriticalSection` (IAT `008C20C0`) runs on every path that entered (`007A708D`, `007A70B0`, `007A70D1`, `007A70EF`, `007A71B3`). Type-7 codes: 0 -> 0, 1 -> 1, 3 -> 3, other -> 2. Types 2/8/9: 0 -> 0, 1 -> 1, otherwise `cmp esi,4` / `sete dil` / `lea eax,[rdi+2]` (`007A71C9`): 4 -> 3, other -> 2. All as stated.
- README count sentences checked against `rows.json`: "named 2 F-frontier functions", "2 applied with 10 anchors", "Rejected ... 0", "Skipped ... 0", "Missing: 0" all match.
- Family-declaring-page rule (`progress.family_rule_inputs`, run read-only at HEAD `b5028e7e9`; 331 accepted families, 19 in scope): `003DF2C0` belongs to no accepted family. `007A7010` is a member of `SQEX SEAD sound library span` (letter C), which `18-Audio/sead-function-identification.md` declares, not this page. Neither is in scope here, so the base rule applies to both.
- Limits hold: body statements only, static evidence. The drafting agent's and OPUS's re-reads are not independent review; this record is. The README's gate figures and "measure A" were not re-measured here.

## SWE2-AUDIT-SPEC narrowings

1. `rows.json` row `003DF2C0` (and the page block, re-rendered by `interior_applier.py --apply`):
   - old: ``calls `0032F3A0` with the record's signed byte `+0x11` and the signed remainder of that pointer's signed word `+0x12` divided by 10, then calls `003DF360` with``
   - new: ``calls `0032F3A0` with the record's signed byte `+0x11` and the signed remainder of that pointer's signed word `+0x12` divided by 10; whichever way that test goes, it then calls `003DF360` with``

## SWE2-AUDIT-SPEC advisories (not verdict-bearing)

- The README title and **Limits** say "cloud-drafted" and "A cloud draft is a pointer", while its first paragraph and `rows.json` `session` name `local-ee-drafter-r4` (a local agent, no cloud credit). It is a wording inconsistency only.
