# REVIEW — OPUS-REQ-AUDITSEM-REVIEW-PARTY-PASSES-0929 · SWE2-AUDIT-SEM 2026-09-29

Passes: `9ede80afb`, `978cd5250` — three 11-Party contracts.
Regressions re-run non-author: falsify_slot_maps / falsify_party_focus /
falsify_battle_state_block — FAILS 0 each. Certified image `73461D08…21F8`.

## CON-169 (SM-5 mode-0-only) — attack fails

`003266C0` calls `0030D9A0` at `0032674F` and cascades `sub eax,1; je` arms:
modes 1→3269D2, 2→326991, 3→3268F3, 4→32683F, 5→326783; fall-through 326A34
is the mode-0 path. Map-4 restores from the pre-refresh copy at `003268FD`
(mode 3, `movups [rdi+0x48]` from `rsp+0x20` saved at `00326709`) and
`003267F3` (mode 5). The "holds only in mode 0" correction is structurally
exact.

## CON-170 (003266DB not a handler) — attack fails

`003266DB` is `mov qword[rsp+0x68],r12` — an ordinary instruction 0x1B into
`003266C0`'s prologue. `rdi = [rip+0x2b98ac1] + 0x5A48` = `[02EBF190]+0x5A48`
verified. The alleged handler table `01EC9260` holds code-VAs spaced 0x1020
(chained UNWIND_INFO); the real table is `01EED260` (0xFF00FF… then a
mode→index byte table). Correction exact.

## CON-171 (binder = 00237DF0) — attack fails

Binder `00233C10` branches only to `00237DF0` (`00233C3F call`,
`00233C48 jmp`, `00233C59 jmp`) — never `002370C0`. `00237DF0`'s first call
is `0023AF50` (`00237DF6`), whose first call is `002370C0` (`0023AF56`);
`00329CC0` runs at `00237E41`. `002370C0`'s only other caller is
`00239960` at `002399E9` (the scenario arm). Byte-exact.

## Verdict

**ACCEPT** — all three corrections stand; the surviving passes' census
claims (S6, F8's 8-access/3-writer census, B5) reproduce non-author.
