# REVIEW — OPUS-REQ-AUDITSEM-REVIEW-ACTOR-REQUEST-PASS1 · SWE2-AUDIT-SEM 2026-09-29

Pass: `dde44728a`, actor-request page (A0–A5 survive + detached-list bound added).
Regression re-run non-author: `falsify_actor_request.py` — FAILS 0.
Certified image `73461D08…21F8`.

## Walk byte-verified (`003DC050`)

`movzx r9d,byte[rcx+0x61]` head; `movzx r11d,byte[rcx+0x89]` bound; entries
`[rcx+0xA0]` + idx*0x14 (`lea rcx,[r9+r9*4]` → `rax+rcx*4`); key dword `+0xC`,
sbyte `+2`, next byte `+0`. `cmp r10d,r11d; jg out` before each hop+`inc r10d` →
head plus ≤ r11d+1 hops = **r11d+2 entries max**, matching the pass's bound.

## The named attack — can a well-formed list exceed `+0x89`+2?

**No, structurally.** `+0x89` is not a counter managed beside the list — it is
the pool's own capacity, written by the same initializer that links the free
list: `003DB580` does `mov byte[rcx+0x89],r8b` and its loop `cmp ecx,r8d`
links exactly `r8` 0x14-byte entries. A detached chain is built exclusively
from those pool entries (byte-indexed, 0xFF sentinel), so no well-formed list
can hold more than `r8` entries — and `r8 ≤ +0x89`+2 covers it with slack.
Truncation check: the sole caller `002667D7` passes `r8d = ebp` ∈ {8, 10}
(`mov ebp,8` / `mov ebp,0xA` after `sub edx,1; je`), so `r8b` never truncates.

## Verdict

**ACCEPT.** The added bound is byte-exact and conservative; the list cannot
exceed the pool the bound counts, so no notification is ever missed by it.
