---
experiment: EXP-090
title: Reward gate callees under isolated original execution
contract: ../13-Rewards-Progression-Economy/CONTRACT-experience-and-licence-award.md
method: B
live_game: false
tool: evidence/reward-gate-exec/check.py
---
# EXP-090 — the six scripted reward-gate callees, executed real

**Date:** 2026-09-17 · **Worker:** SWE2-ORACLE · **Method:** B (isolated original-code execution, Unicorn)
**Subject:** the six callees `diff_reward_award.py` supplies as scripted oracles — `0031B860`,
`003135C0`, `00313800`, `00320AB0`, `0031B810`, `00264150` — plus their whole transitive call
surface, and `002F8BB0`/`002F90C0` re-driven with the real callees wired in
**Contract:** `Database/FFXII TZA/13-Rewards-Progression-Economy/CONTRACT-experience-and-licence-award.md`
**Board task:** `SWE2-ORACLE-REWARD-GATE-EXEC`
**Evidence:** `evidence/reward-gate-exec/` (`check.py`, `result.json`, `bodies.json`)

## Result

**104/104 cases pass; 10/10 byte-level mutants detected.** Stable across two full processes.

§14's open question — "what `003135C0`, `00313800`, `0031B860`, `00320AB0` and `00264150`
decide" — is answered by execution. The entire closure runs as shipped bytes: **zero stubs** —
every reached body is shipped code over readable globals; only guest memory content is fixture.

## What each gate decides (all measured, none asserted)

- **`00264150` (LGATE)** — `movsx eax, byte [0209A2A9]` — a pure leaf: the licence gate is one
  **sign-extended** global byte. `lgate-neg` measures the sign extension (`0xFF` → `0xFFFFFFFF`).
- **`0031B860` (FIND)** — resolves a stats-record pointer to its unit: loops `i` over
  `00236850()` (`[0208E6A0]`, a dword count leaf) calling `00236820(i)` (`ecx<0` or
  `ecx > count-1` → 0; else `[0208E688] + i*0xF50`) and comparing `unit+0x698 == arg`. First
  match wins (`find-order`), arg 0 and count 0 return 0.
- **`003135C0` (SINGLE)** — `0030D9A0() == 1`, where `0030D9A0` is a **mode enumerator** over the
  dword at `[[02EBF190]+0x5B04]`: bit3 → 5, bit2 → 4, else `00377C20()` → 3, bit1 → 2, bit0 → 1,
  else 0 — measured per-bit and for every priority pair (`mode-flags-3/C/14/18`). `00377C20` is a
  flagged-record probe: index `003148F0()` (clamp ≥ 0 of `[002164480+0x1044]` = `[021654C4]`),
  bound `[021654D0 ...]` — table `[02ADD100]`, count `+4`, and the entry is read at **three-byte
  stride** (`u16` at `+8+i*3`, flag = bit 15). `idx >= count` returns 0.
- **`00313800` (DESIG)** — byte `[[02EBF190]+0x5AD5]` → `00320890`: `0xFF` → `-1` early; else a
  9-slot scan comparing the **low byte** of each u16 at `FRAME+0x5A48+i*2`; hit → index, miss → -1.
  `desig-hibyte` shows the u16 high byte is ignored.
- **`00320AB0` (RESOLVE)** — `0031B9F0(idx, sel)`: `00322C50(0x17, idx)` bounds the index to
  `0..8` (fail → `0xFF`), then a five-arm select reads byte `FRAME + idx*2 + {5A48, 5A5A, 5A6C,
  5A7E, 5A90}` for `sel` 0–4 (else `0xFF`). `00320AB0` then bounds the byte `<= 0x27` and returns
  `FRAME + 8 + byte*0x1C8` — **a pointer into the stats-record table inside the same struct**.
- **`0031B810` (PARTY)** — `00322C50(0x17, i)`; fail → `ecx=0xFF`, else byte
  `FRAME+i*2+0x5A5A`; tail `002367A0` — which gates the id through `00322C50(2, id)` (bound
  `[[02EBF130]+4]`) and scans units for `word[stats+4] == arg`, with `arg==0xFF` comparing
  `0xFFFF`. `uscan-ff` shows the `0xFF`→`0xFFFF` substitution is real, and `party-gatefail` shows
  a failed slot can still match a stats record whose word `+4` is `0xFFFF` (kind `0xFF`).
- **`00322C50`** — the shared 32-arm bounds dispatcher (image-relative jump table `00323054`):
  returns `low <= ebx <= high-1`; arm 2 supplies `low=0, high=[OBJD+4]`, arm `0x17` supplies
  `0..8`. Kind 0 and kind ≥ 0x21 return 0.

## Structural findings for the contract owner

- **F1 — one struct carries the whole surface.** `[02EBF190]` is simultaneously the record table
  (`+8`, stride `0x1C8`, bound `0x27`), the five 9-entry u16 tables `+0x5A48`–`+0x5A90`, the mode
  flags `+0x5B04` and the designated byte `+0x5AD5`. `00313800`'s scan and `0031B9F0` sel-0 read
  the **same** table (`+0x5A48`).
- **F2 — ordinary byte selectors exclude kind-1 members, but the universal kind-0 claim is withdrawn.**
  `0031B810` feeds a byte selector to the word-identity lookup. An ordinary byte cannot match
  a kind-1 identity. However the already-recorded `0xFF`→`0xFFFF` substitution admits a kind-FF
  identity when the descriptor's bound permits it. SECTION-03 supplies a count-256 synthetic
  fixture exercising that real path, so "only kind 0 can ever count" overstates the proof.
  This does not establish that initialized gameplay creates a valid kind-FF unit.
- **F3 — divided-path member filter measured against real records**: skip if mask
  `(0x64|0x3C)&0x80000003`, or kind0 with `id==0x1A` or `id∈0x1B..0x27`; `n==0` returns 0 before
  the signed `idiv` (`xp-div-0/1/2`, `xp-div-skip-1a`, `xp-div-count-19`, `xp-div-masked`,
  `xp-div-neg` — `-10/2 = -5` carried signed).
- **F4 — single-mode path**: if `003135C0` is true, a **nonnull** recipient must equal
  `00320AB0(00313800(),1)` (`xp-desig-mismatch` → 0). NULL skips this comparison, but in shared
  mode a NULL call still runs the four-slot divisor; NULL does not select the mode.
- **F5 — LP asymmetry confirmed under real gates**: `002F90C0` doubles on modifier bit `0x10`
  (either bank) and has **no zeroing clause** — XP's bit `0x20` → 0 has no LP counterpart
  (`lp-mod-20` still returns the award). LP's id filter admits `{≤6, 0x1A, ≥0x28}` — measured at
  every boundary (`lp-id-06/07/1a/27/28`).
- **F6 — call order is evidence**: `xp-single-hit` trace =
  `xp → find → (ucount,uget)×2 → single → mode → flag77 → idxget → ef2b0 → ef640 → desig → dscan
  → resolve → b9f0 → bound` — FIND runs before SINGLE; the mode enumerator consults `00377C20`
  even when bits 0/1 will decide.

## Mutation campaign (10/10 detected)

| mutant | site | effect measured |
|---|---|---|
| find compare `+0x698` → `+0x699` | 0031B895 | stats pointer never matches → 0 |
| single `cmp eax,1` → `2` | 003135CD | mode 1 no longer selects the designated path |
| mode bit3 test `8` → `0x10` | 0030D9B3 | flag bit3 falls through to flagfn/bit arms → 0 |
| desig scan bound `9` → `8` | 003208B5 | slot-8 hit becomes -1 |
| `0031B9F0` sel-1 offset `0x5A5A` → `0x5A5B` | 0031BA8F | reads the u16 high byte → 0 |
| dispatcher arm-`0x17` bound `9` → `8` | 00322FB0 | index 8 rejected |
| unit scan `word[+4]` → `[+5]` | 002367E2 | id byte never matches → 0 |
| XP mask `0x80000003` → `0x80000002` | 002F8C07 | bit-0-masked recipient now passes |
| member loop bound `4` → `3` | 002F8CE4 | slot 3 never counted |
| LP id admit `0x1A` → `0x1B` | 002F90EC | id 0x1A rejected, 0x1B admitted |

## Deviations and limits (disclosed)

- **Zero stubs** — the entire reachable closure is shipped code. Fixture content only: the
  `[02EBF190]` struct (records, tables, mode flags, designated byte), the unit array and count,
  the flag table `[02ADD100]`, the arm-2 bound object `[02EBF130]`, the two in-image cells
  `[021654C4]` (index) and `[0209A2A9]` (licence byte).
- All global addresses re-derived programmatically from rip-relative operands — not from prose.
- The record `+0x34`/`+0x2F` reward fields are fixture rows; `002F8BB0`'s call-surface past the
  six gates (e.g. the row producers for `+0xE70/+0xE78`) is out of scope — supplied as row
  pointers in the unit fixture.
- Isolated original-code evidence under Unicorn; no NATIVE-REPLAY or live claims. `00322C50`
  arms other than 2 and `0x17`, and its arm-1 re-dispatch via `00309440`, are present but not
  exercised by these call sites.

## Kill set

Every mutant diverged on observable state: the find compare offset, the single-mode compare, the
mode bit tests, the desig scan bound, the table-select displacement, the dispatcher constant, the
unit-scan field offset, the XP mask, the member loop bound, and the LP id admit.

## SECTION-03 independent production review — 2026-09-22

[Retained bindings and consumers](evidence/continuation-section03-reward-bindings/REVIEW.md)
adds 71 native synthetic original-code controls and six deliberately incorrect private-image
variants. It independently verifies the 19-body reward/gate closure and selected producer/caller
bodies, but does **not** rerun this original 104-case/10-mutant Unicorn campaign. Its program,
raw result files and original case receipts remain unchanged.

The corrected current contract distinguishes EXP's owning-unit check from LP's lack of that
check, shared NULL EXP division, separate LP global/id gates, unsigned LP coefficients and
modifier order. Historical campaign counts above remain historical, not new certification.
Peer acceptance of the production changes is pending; no live game run is claimed.
