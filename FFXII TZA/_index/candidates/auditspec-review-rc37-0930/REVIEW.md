# SWE2-AUDIT-SPEC review of RC-37 (rc37-refused-read-0930, OPUS, b2320ed29): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75, 2026-09-30). Author: OPUS. Reviewed commit
`b2320ed29`, read beside SWE2-DATA's independent `79e70e154` (`rc28-callback-0930`), and against the RC-37 register row
as SWE2-CONTRACT wrote it (`7fa0f7d33`). Static, the certified image.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-RC37-0930 | [rc37-refused-read-0930](../rc37-refused-read-0930/README.md) | `b2320ed29` | ACCEPT |

**Re-run.** `rc37_refused_read.py` exits 0 and prints FAILS 0. [`rerun_rc37_refused_read.out`](rerun_rc37_refused_read.out)
is identical to the committed output (CR ignored). SWE2-DATA's `rc28c_callback.py` also re-runs identical
([`rerun_rc28c_callback.out`](rerun_rc28c_callback.out)). Both record directories stayed clean.

**Re-derived independently** ([`rc37_indep.py`](rc37_indep.py) / [`rc37_indep.out`](rc37_indep.out); raw `.text` sweeps
through `tk.py` and the raw call index, not the author's pins):

- **Status-slot census (F5), in every addressing form.** `0215EFF4` has 6 rip-relative references and 0 raw-only ones:
  4 `lea` that take its address (`002DF719`, `002DF75F` in `002DF6C0`; `002DF808`, `002DF838` in `002DF780`) and
  2 dword reads (`0046DFE7` in `0046DFE0`, `0046E0E0`). It has 0 image-base-relative references and 0 relocated
  pointers. The pointer global `01F82CC0` has 4 rip references: a read and a clear in `001D6D70`, and stores in
  `001D6D90` and `001D6FB0`. It has 0 image-base-relative references and 0 relocs. So the slot is written only through
  that pointer, as F5 says. The seven owning functions match the record exactly.
- **One issuer.** In the raw call index, `002DF780` has one caller (`0046E030`), and `0046E030` and `002DF6C0` each have
  one caller, the pump `0032E070`. Nothing outside the queue issues a read that could put −1 into the slot while the
  refused request sits in state 3. The one-at-a-time premise therefore holds for every issuer of this slot.
- **The error helper (F6).** `0032E382 cmp dword [rcx+0x28], -1` / `0032E386 jne` skips the call unless the byte count
  is −1. Then `0032E38C xor r8d, r8d` / `0032E392 call rax` on `+0x40`, as stated.
- **The callback (F8).** The whole `00364380` body is 7 instructions: load `[022CBE00]`, null test, `1 << cl`,
  `or [rdx+0x240]`, `ret`. No operand names `r8`.
- **The boot case.** `0215EFF4` lies in `.data` past SizeOfRawData (`.data` raw size `0x18e400`, virtual `0x11a7530`),
  so it starts at 0.

**Where the two records differ, and the row.** OPUS leaves the −1 allocation open. SWE2-DATA says `0036BC60` clamps it
to 0. I confirm the clamp: `0036BC89 xor eax, eax` / `test edx, edx` / `cmovns eax, edx`, then round up to 64, so the
size is 0. `002497E0` → `0036A100` → `0036BC60` (`0036A11F`), and `00249810` → `0036A190` → `0036A1A0` → `0036BC60`
(`0036A1C9`). The register row already carries this reconciliation, and its remaining limit (what a 0-byte request
returns, including the retry `0036BFE0`) is correct. This is a difference in how far each record went, not a
contradiction.

**Controls.**
- F1-F8 are byte pins. They catch a wrong address or instruction but not a missing path. The negatives rest on F5
  (reproduced above in all three addressing forms) and on the issuer count (above). Neither is in the author's script
  as a control that could fail.
- C1 (the kind-`0xFF` branch tests its submit result) is a contrast, not a sensitivity control. It shows the untested
  kind-7 branch is specific, but it could not catch a misread of that branch. The 0-byte fact is the reason the
  answer does not depend on the allocator.

**Note for the row owner (SWE2-CONTRACT), optional, not a defect.** OPUS's premise, "the request ahead left state 3
with the slot not −1", does not cover a refused request issued before any read. The zero-initialised slot covers that
case, and SWE2-DATA's record already states it. Suggested wording after "as the previous read left it (not −1)":
"; before any read it is 0, the slot being in `.data`'s zero-initialised tail".
