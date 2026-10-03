# SWE2-AUDIT-SPEC review: OPUS member-mode rows, Phyre PRendering module part 1 (opus-member-modules-registered-before-main-phyre-prendering-module-1)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS, not the drafting or checking local agents) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-MEMBER-MODULES-REGISTERED-BEFORE-MAIN-66275` · Package: `_index/candidates/opus-member-modules-registered-before-main-phyre-prendering-module-1/` · Page: `22-Middleware-PhyreEngine/Subsystem-Map/the-fifteen-modules-registered-before-main.md` (commit 83b4566ab)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` re-run fresh without `--apply` -> `VERIFY 34 functions, 165 anchors`, `ALREADY`, `FAILS 0`.
- `rows.json`: 34 rows, 165 anchors, mode `member`, family `Phyre PRendering module`. Rejected 0, missing 0, corrections none. Skipped 2, both "too large for one precise sentence": `005DC8D0` (764 B) and `005DF890` (906 B).
- Semantic pass: **15 of 34 rows**, spread over the package, read clause by clause against `disr.py`-equivalent output of the certified image (same image and extent table), with `.rdata` strings resolved:
  - `005D83E0` exact: the source advances (`add rsi,0x10`) only on the non-null-slot arm.
  - `005D8650` exact: `and esi,0x7fffffff; jbe` skips on a zero count (`and` clears CF). The sizes are 0x2C0 (`imul`) and 0x18 (`lea [rbp*2]; add; shl 3`); `cmovne` sets each count to `n` only when the copy is non-null; the source pointer `rdi` advances only inside the non-null branch.
  - `005D8930` exact: `sub rbx,(byte&1)` clears bit 0; strlen loop then `inc`; `0017D260(len, 2)` and `00861EBA(p, s, len)`; dwords `+0x20..+0x2C`.
  - `005D8BE0` exact: guard `cmp [02CE7960],epoch; jle`; `006B6820` gets rcx = 02CE7900, rdx = 00D40578 "PSceneRenderPassType", r8d 0x20, r9d 8, `[rsp+0x20]` = 006CD4C0 and `[rsp+0x28]` = 005FE160 (fifth and sixth arguments); store of 00D4A918 to 02CE7900; `00808B90(008ACDB0)`; `0080929C`.
  - `005DBE30` exact: `btr esi,0x1f; cmp 1; jbe` and `cmove r8,r14` select the source; the count is re-read from `[rbx]` after `005FEE80`; the four-way free gate (`!= p`, `!= rcx+8`, bit 31 clear, non-null); `p` stored only when `!= rdi`.
  - `005DC8B0` exact.
  - `005DCE30` exact: the zeroing runs on both the freeing path (005DCE92/96) and the skip path (005DCE9C/9E).
  - `005DD670` exact: qword `+0x68` is freed only when non-null with bit 0 clear. `005F02A0` is called without a null test. The four pairs are freed under the bit-31 and null tests, and every pair is zeroed. `+0x10` and `+8` are not zeroed.
  - `005DDE70` exact: callees `005F0520` and `005F03A0`, then the `00616980` loop with stride 0x2C0.
  - `005DE0C0` exact.
  - `005DE3D0` exact: `shl rcx,4` sizes the buffer; the `005F0220` free takes `rcx` = old qword and `edx` = dword AND 0x7FFFFFFF; `n` and `p` are stored on every path.
  - `005DE4F0` exact: `005D83E0` fill, `005F02A0` free.
  - `005DE710` exact: `imul 0x2c0`, `005D88C0` fill, `005F0410` free.
  - `005DE830` exact: `lea [rsi+rsi*2]; shl 3` (0x18), `005D8B00` fill, `005F0520` free.
  - `005DEBA0` exact: `005E2D70(ecx = count AND 0x7FFFFFFF, rdx = source qword)`; the free gate is `!= p`, then bit 31 clear, then non-null; the masked count and `p` are stored before `005DE8C0(rcx+0x38, rdx+0x38)` and byte `+0x48`.
- Signed versus unsigned: every compare in the sample is a zero test or `cmp count,1; jbe` on a count masked to 31 bits ("above 1"), which is sign-neutral. No signed jcc in the sample.
- Batch-wide sentence (shared by the 7 PRendering records of 83b4566ab), checked once: "203 rows … 199 stood, 4 rows were corrected in 6 clauses (signed compares written as above/below)" matches the records. The 7 `rows.json` hold 34 + 30 + 29 + 35 + 32 + 20 + 23 = 203 rows. All 6 correction entries are in `prendering-module-6`, in 4 functions, and all are signed compares. `Tools/work/OPUS/cloud/verify_prendering_1003.json` shows 199 OK and 6 FIX entries in 4 functions.
- Limits hold: body statements only, static evidence; the drafting agent, the second local reader and OPUS's re-read are not independent review, this record is.
