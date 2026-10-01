# REVIEW: sd181-sp1-loader-0930

- **Package:** `sd181-sp1-loader-0930` (OPUS, commit `2e1bb015e`)
- **Task:** `OPUS-REQ-AUDITSPEC-SD181-0930`
- **Reviewer:** SWE2-AUDIT-SPEC (independent of OPUS author maybeLynd)
- **Verdict: ACCEPT**

## Controls re-run

`sd181_check.py` re-executed (`rerun_sd181_check.out`): L1–L5 PASS, `FAILS 0`, output
text-identical to the committed `.out` (CRLF only). Package dir clean after re-run.

## Independent verification (capstone on the certified image, sha `73461d08…21f8`)

Every L1–L5 anchor independently re-derived — not merely the packaged check:

- **L1** — `003780B1 lea rax,[rip+0xb08] → 00378BC0` confirmed. Image-wide reference census
  (desync-resyncing linear sweep over .text + qword scan over all sections): **the lea is the
  only reference** — zero rel32/jcc calls, zero data/DIR64 pointers to `00378BC0`.
- **L2** — `00378BDD lea rdx,[rsp+0x20]; mov eax,0xfffffffc; mov r8d,0x20; and rcx,rax; and
  ebx,3; call 0036B970` — verified instruction-for-instruction: `0036B970(block & ~3,
  rsp+0x20, 0x20)` builds the 32-slot table.
- **L3** — `00378E95 mov rcx,[rsp+0xa0]` (= slots[16]: rsp+0x20 + 16×8) → `00378E9D mov
  [rip+0x27641bc],rcx → 02ADD060`, unconditional; `test rcx,rcx; je` / `bts eax,7` marks bit 7
  only when non-null. Verified: **no rsp modification and no other `[rsp+0xa0]` write** between
  `00378BF3` and `00378E95` — the stored value is genuinely slots[16].
- **L4** — control confirmed: slots[24] (`r11=0x120000` indexed form `[r9+r11+0x29BD010]`)
  lands at `02ADD010`.
- **L5** — independent resync sweep for all rip-relative refs to `02ADD060`: **exactly 4** —
  `00378E9D` store (00378BC0), `003782D3`/`003782E4` read+clear (teardown `00378230`), and
  `003775EE mov rcx,[rip]` → `call 003635C0` (reader `003775D0`). Zero image-base-disp
  (`0x29BD060`) forms; zero stored data pointers to `02ADD060` in any section. Matches L5
  exactly: writers = loader + teardown, sole reader = `003775D0`.

## Limits

- The region `02ACAE00..02AD239F` as a whole has no direct rip/immediate addressing — access is
  via runtime-computed pointers, so the completeness argument for other table rows rests on the
  slot-table structure, not an enumerated pointer census. Static only.

**Verdict: ACCEPT** — all five claims independently reproduced on the certified image.
