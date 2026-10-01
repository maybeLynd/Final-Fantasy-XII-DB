# REVIEW — OPUS-REQ-AUDITSEM-REVIEW-WORLD-LOOT-PASS1 · SWE2-AUDIT-SEM 2026-09-29

Pass: `11e788a3b`, `13-Rewards-Progression-Economy/CONTRACT-world-loot-pickup-pool.md`.
Regression re-run non-author: `falsify_world_loot.py` — W0–W10 all SURVIVE, FAILS 0.
Certified image `73461D08…21F8`.

## Attacks (all three named surfaces)

**1. Register-based writer of node `+0x00` outside the seven entries — fails.**
Every non-rip route into the pool was enumerated: zero imm operands carry a node
address, zero data-section pointers hold one. The only non-rip reachers are:
- `0031B690` — leas `0x2EC138C`/`0x2EC1380`, writes `rbx-8..+8` over
  `0x2EC1384..0x2EC13AC`: entirely **above** HEAD `0x2EC1360` (a different table).
- `00328FF0` — leas `0x2EC1380`, writes `rax+r9*8(+4)` ≥ `0x2EC1380`: above the pool.
- `0035B510` — byte-table sweep `0x2EC0BA1+0x40n`, bound `0x2EC0FA1`; last write
  `0x2EC0F61` < POOL `0x2EC0FA0`. Boundary grazes the pool but never enters it.
- `00319850` — loads HEAD into rbx, **reads** `[rbx]` (slotIndex → arg of
  `002FB310`) and walks `[rbx+0x18]` next-links; no node store — a consumer, not
  a writer (consistent with §6's `002FB150`/nearest-selector note).

So `+0x00` is written only by INIT's rip-relative stores; W2's claim stands.

**2. A third reader of `022C3174` — fails.** Complete rip census reproduces
exactly the three refs W8 reports (`0031842A` imul read, `003184EC` mov 0,
`00319974` inc). Zero leas into it, zero imms carry it, zero data pointers.
Reachable only rip-relative — the census is complete; no third reader exists.

**3. Generator through an indirect call — bounded, fails.** My BFS reproduced the
215-body closure; zero immediate call/jmp escapes outside the function table.
154 indirect sites: **113 are `call/jmp [rip]` IAT slots — zero stored values
resolve into `.text`** (unbound imports cannot enter a gameplay generator); the
`0028F032 jmp rcx` is W6's verified 6-entry table. **41 register-indirect sites**
(vtable-style; concentrated in CRT/handler bodies `005C/007A/007B/007E`, ~13 in
gameplay bodies incl. `00309F30`) cannot be statically resolved — the true
residual. A runtime-filled vtable target could conceivably reach a generator; the
same disclosure class as the corridor closure's bound. Both PRNG cells have zero
rip-relative users in the direct closure.

## Byte-verified anchors

- `003183D0` (`EnemyChain_TryAdvanceRank`): `cmp r10d,eax` threshold gate →
  `test byte[022C3178],1` waive → `lea eax,[r11+1]` (rank+1) →
  `imul eax,[022C3174]` → `sub r10d,eax`; advance path `inc r11d`,
  `mov [022C3174],0`. §6's added paragraph is byte-exact.
- `00319974 inc dword[022C3174]` — sole increment.
- `0028F000` dispatch `lea eax,[rdx-1]/cmp 5/ja` + table ops 4≡5 (`xor edx,edx`
  before `call 003FA820`) per W6.
- Side observation, no conflict: `TryAdvanceRank` itself steps the gameplay LCG
  (`mov [022C256C]` at `00318496`) — outside the 215-body pool closure, so W10 is
  unaffected.

## Verdict

**ACCEPT.** Nothing the contract asserted is false; the added chain-penalty
context is verified byte-exact; the 215-body "no RNG" claim holds with the
41-site indirect bound disclosed. Record of residual scope only — no correction
owed.
