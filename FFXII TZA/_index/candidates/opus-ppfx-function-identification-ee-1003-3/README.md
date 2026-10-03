# Interior citations, cloud-drafted: ppfx-function-identification.md's entry-cited functions (OPUS, 2026-10-03)

The page named 6 F-frontier functions only at their entry. A local drafting agent (local-ee-drafter, no cloud credit) drafted one sentence and 1-5 interior anchors per function from OPUS's annotated disassembly pack (`cloud-input/f-interior/` in the private snapshot repo). OPUS checked every row mechanically with `interior_ingest.py` and re-read every sentence against the bytes before applying.

**Rows.** 6 applied with 30 anchors. Rejected by the mechanical check: 0. Skipped by the session: 0. Missing: 0.

**OPUS corrections on re-read.**

- `00721030`: byte re-read by a non-drafting agent: Read-before-call ordering: for each q the body loads qword [01F3BA68] once into rbp at 00721168, before the first 006DA8A0 call (which receives that value), and passes the same register to the second call; the draft's text implies a fresh read per call. Everything else verified: qword [o+0x28] kept in r15 before 007271C0(o); 32-byte copy after the call; flag mapping (bit 0x100, 0x4000, 0x100000, 0x200000, 0x1000000, 0x2000000, 0x10000000 to 0x10000000, 0x1200000, 0x1000, 0x2000, 0x10000, 0x240000, 0x1000000); jns selections of w/h, jg signed tests, 8-qword scan of 02EA18C0; tail jmp 00727170(o, kept qword).
- `007226E0`: byte re-read by a non-drafting agent: Address form: the listing reaches both tables only as image-base displacements (lea rsi, 00120000 then +0x2D818C0 and +0x1E1CB18); 01F3CB18 is named bare, without the base + displacement form the row uses for 02EA18C0, so the named address does not appear in the listing. Logic verified: frame (rsp = rsp0-0x78: 5th float [rsp+0xA0], 6th dword [rsp+0xA8], 7th qword [rsp+0xB0]); bt edx,0x14 + jae to the 02EA18B1 test; 00722C80(r9, xmm1 = 5th, r8d = 6th, r9 = 7th, stack 0) with cmovs; i zero-extended (mov r11d, ecx); 0071FD40 fourteen-argument list matches stack slots 0x20-0x68; bl = 1 only when bit 0x100000 is set, so the table entries are zeroed when it is
- `00722C80`: byte re-read by a non-drafting agent: Sign extension: the slot index dword [o+0xA0] is read with movsxd (sign-extended) at 00722DAF, while c is loaded with a 32-bit mov (zero-extended) and used as an unsigned index at 00722DBE; the draft states neither. Rest verified: 02EA18B1 zero path with jb 1 log gates and 0x8000FFFF; first-non-null chain over 02EA18C0..02EA18F8 leaves o = 0, k = 0 when all are null and nothing tests o; bit 0x80000000 test and qword compare against 0; clears 01F3CB18..01F3CB30, 02EA18C0..02EA1900, byte 02EA18B1, dword 02EA1908; returns 0.
- `007897D0`: byte re-read by a non-drafting agent: Read-before-call ordering and shift wording: qword [01F3BA68] is loaded into rbx at 00789860, before the 00715C70(e+8) call, and that value is passed to 006DA8A0; both counts are formed with sar 3 (arithmetic shift, floor) and the loop compares only the low dword (signed jl). Rest verified: null rdx gives 0x80070057; qword +0xE0 = rdx, inc dword [rdx+8], three qwords zeroed; array qword +0xC8 re-read for the entry and for nulling it; +0xD0 = +0xC8; dword +0xBC from qword +0xE0 re-read; returns 0.
- `007906C0`: byte re-read by a non-drafting agent: Read-before-call ordering: on the negative path qword [01F3BA68] is loaded into rdi at 0079073E, before the null test and before o's vtable slot +0 call, and that value goes to 006DA8A0. Rest verified: 006DA880(qword [01F3BA68], 0x180, 00E1FCA0 = '..\src\GPU\TinyEffect\TinyEffect.cpp', 0x2A5E, 0); o becomes 0078B9D0's return or 0; 0078D7E0(o, rcx, rdx, movzx r8b) with no null test; slot +0 with edx = 0; returns 0 on the negative path, else o.

**Verification.** [`interior_applier.py`](interior_applier.py) reads [`rows.json`](rows.json) and re-decodes every function first. Every anchor is an instruction boundary inside its extent with the recorded mnemonic ([`.out`](interior_applier.out): FAILS 0; idempotent).

**Effect and gates.** All 6 rowed functions now measure A. On the page: `check_links` 0, `check_self_contradiction --db` 0, `check_consistency` 0 disagreements naming this page (tree total 3), `verify_doc_addresses --all` 0 REVIEW on this page (tree total 2).

**Limits.** Body statements, not meanings. A cloud draft is a pointer, not evidence: what stands here is OPUS's re-read. The session's agreement with OPUS is not independent review.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
