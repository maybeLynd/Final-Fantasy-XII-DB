# AUDIT-SEM review — eleven-request wave (2026-09-29)

Board revision claimed at ~38924; requests 38925–38944. Identity `SWE2-AUDIT-SEM`. Certified image
SHA-256 `73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`; canonical VAs include the
`0x120000` base. Each item: producer checker reproduced `FAILS 0`, then independently byte-verified.

---

## FABLE-REQ-AUDITSEM-REVIEW-HP-LETHAL-1 — ACCEPT

`hp_lethal_checks.py` → `FAILS 0`. Independent verification on the shipping image:

- `0030E360` reaches the stat recompute through `0030E828` — verified.
- `00310508` stores the recomputed HP at `[rbx + 0x48]` — byte-verified.
- `00469BB0` builds a zeroed context (`+0x08 = target`) and posts event `0x10` through `0046AB10` —
  byte-verified.
- Post-drop boundary `003125B4`: after the drop placement, `00312280` contains only
  `call 0x317090` and the stack-cookie check `call 0x808c40`. No unit-retirement call follows. The
  full function has other calls earlier — the claim is scoped to the post-drop region and that scope
  is exact.
- Achievement chain `00317090` → `00253770` (kind `0x11`) → `00316A50` — verified.
- No revive-on-KO status among the 32 statuses — checker control reproduced.

## FABLE-REQ-AUDITSEM-REVIEW-HP-LETHAL-2 — ACCEPT (one noted elision)

- `atype 0x1B–0x27` = the thirteen Esper rows of the 40-row party table — confirmed by the corrected
  contract l.380 (`08-Combat-Formula/CONTRACT-hp-write-and-lethal-transition.md`, OPUS edit
  `96272843d`) and independently by the same contract's `00469BB0` paragraph ("an Esper
  (party-table type ids `0x1B`–`0x27`)").
- Residual "Monster-band" wording: the live contract carries the correction as struck text with the
  new text inline — the correct way to record it. The only unstruck occurrences are inside dated
  `_experiments/` snapshots (EXP-093 evidence, both the live and `retained/` copies), which are
  historical records and must not be rewritten.
- Rewards step 6 (`13-Rewards-Progression-Economy/what-happens-when-an-enemy-dies.md` l.56–59): the
  old "Retire the unit" is struck; the replacement describes the achievement counter `0x11` feed
  (`00317090` → `00316A50`) and "nothing here removes the body" — matching the byte-verified tail.
  Noted elision (not a defect): the arrow compresses `00253770` out of `00317090 → 00253770 →
  00316A50`; the endpoints and the `0x11` kind are correct.

## FABLE-REQ-AUDITSEM-REVIEW-SPAWN-RESPAWN-1 — ACCEPT

`respawn_checks.py` / `teardown.py` → `FAILS 0`. Byte-verified:

- `00235720` reads record fields `+0x0A`, `+0x08`, `+0x10`, `+0x0C`; the re-admit comparison is
  `sub ecx, dword ptr [r14 + 0xc]` / `movzx eax, word ptr [r14 + 0x10]` / `cmp ecx, eax` / `jb`
  reject — elapsed ≥ cooldown re-admits. This refutes the contract's old "no native code reads"
  wording, as the package claims.
- `002395A0` writes `+0x10`, `+0x0C`, `+0x08`, `+0x0A` — verified.
- `00234200` teardown gate (bit 33 + bit 34 + presentation state < 3, or no handle); timeline kinds
  6 and 4 set bit 34 — checker-reproduced.
- `0025B225` is the sole E8 caller of `00234200` — my own rel32 census agrees.
- Struck text in the contract is genuinely old text; corrections carry dates and citations.

## FABLE-REQ-AUDITSEM-REVIEW-UQ218-SELECTOR-CRITERIA — ACCEPT

`selector_criteria.py` → `FAILS 0` (N Q K1 K2 Y). Independent `.rdata` constant resolution for
`00422870` — computing RIP targets as `instruction_end + displacement` (an earlier scan that omitted
the instruction length produced garbage; corrected):

- `004228AF movss xmm2, [rip+0x8efb85]` → `00D1243C` = **−45.0**
- `004228BA mulss xmm1, [rip+0x8eef1e]` → `00D117E0` = **57.295776** (180/π, rad→deg)
- `004228C9 movss xmm0, [rip+0x4e061f]` → `00902EF0` = **45.0**
- `004228E0 movss xmm0, [rip+0x8efb50]` → `00D12438` = **135.0**
- `004228FB comiss xmm1, [rip+0x8efb42]` → `00D12444` = **−135.0**

Heading × 57.2958 → banded against ±45/±135 into `[rbx+0x2AF]` — the Y-band model confirmed.
`00422420` inspected: `+0x40E` gate byte, `imul` frame-limit path, `+0x411` store, counter capped at
0x64 — consistent with kind-1 draw-range/frame-limit semantics and the `0x0B` skip on `-1`.

## FABLE-REQ-AUDITSEM-REVIEW-UQ218-RESIDUE — ACCEPT

All four scripts rerun: `authoring.py`, `residue.py`, `arm0_census.py`, `classifier.py` → `FAILS 0`.
Independent checks:

- **W (byte order):** both `@FMW` arms read `movzx [rax+r8+2]; shl ax,8` (high byte from `p+2+2i`)
  OR'd with `[r8+p+1+2i]` (low byte) — `0041B412`/`0041B41F` (arm 0) and `0041B7C6`/`0041B7D3` (arm 1)
  byte-verified. The value is **little-endian s16**: low address holds the low byte. The page's
  "s16 big-endian" wording is correctly rejected.
- **E:** `0041F6FB mov edx,[rax+0x44]` reads ticket `+0x44` → `call 003B3550` — verified; five
  readers stand (`0040A1B3`, `00409CFD`, `00409EB8`, `0041F6FB`, `005049B3`).
- **S:** `00373B58 lea r9,[rbx+0x100]` byte-verified inside `00373860`; sole E8 caller census →
  `003705BA` only.
- **A/V:** `+0x31A`/`+0x31C` descriptor→actor wiring and `+0x413` (`stdmotionvariation`, shl 3 /
  shr mirror) checker-verified.
- Unpinned readings remain labelled readings, not promotions.

## FRONTIER-REQ-AUDITSEM-REVIEW-0928G — ACCEPT

`sn1_q3_pagemap.py` → `FAILS 0` (M1 M2 X C). Independent discriminator: rebuilt instruction starts
by **walking the `.ebp` bytes** (`starts[i]` script base, `oplen` = 1 for `0x03–0x47`, 3 for
`0x48–0x63`) instead of trusting q0's flag byte, then recomputed
`map[k] = bisect_left(starts, 32k) − 1`:

- **49 of 50 scopes match exactly.** The single mismatch is `evctrl` scope 1 — the package's own
  disclosed anomaly (its last instruction lies 143 bytes beyond the script's span, per
  `sn1_q0_domain.py` check R; there the q0 extent itself must supply codeEnd). The map law
  `E = 1 + floor((q0len−1)/32)`, `-1` for page zero, zero padding — exact where derivable.
- q2 mirror `{ceil(icount/32); byte of instruction 32j}` reproduced.
- Formula without `-1` matched zero scopes; listA/listB padding absorbs a pad zero on exactly the
  three predicted scopes including `btlctrl sc19`.
- X's semantic meaning correctly left open (`btlctrl` sc18/sc19 identical maps, X = 1/2).

## FRONTIER-REQ-AUDITSEM-REVIEW-0928N — ACCEPT

`t0_scope.py` → `FAILS 0`. Independent recount with my own `.dbg`/`.ebp` parser:

- T0/operand counts `ctrl 56, btlctrl 92, evctrl 115, mapctrl 127` — equal in all four modules.
- T2 route: **106 covered = 71 single + 35 multi, 0 shifted, 0 other; 284 none** — independently
  recounted from raw T2 pairs (11,661 total pairs; T2 records carry only 1- or 2-name lists).
- No duplicate descriptor values among covered entries — descriptor→index attribution unambiguous.
- CP932: 94 T0 names carry bytes ≥0x80, but all comparisons are decode-invariant (same decoder both
  sides) — the latin-1 decode cannot fold or alias names; classification is equality-safe.
- "Not claimed" scope in the docstring is honest: operand→T0 binding unproven for the 284,
  compiler rule and live values unclaimed.

## FRONTIER-REQ-AUDITSEM-REVIEW-SN1-62 — ACCEPT

`t0_attribution.py` → `FAILS 0`. Prerequisite refusal exercised directly:

- `python t0_attribution.py /nonexistent-dir` → `FAIL P prerequisite sn1_neither_partition.py:
  sn1_variable_binding.py exit 1 …`, `FAILS 1` — the fail-closed chain carries the reason through
  three prerequisite levels (this is the repaired `sn1_prereq.run` interface I reviewed and
  accepted at `0b26f50c4`).
- 62-descriptor run `0A03..0A40`, 188 A/E records on 36 tags, 26 multi-operand tags, 97/188 with
  T0 name on ≥2 lines — all reproduced by the checker output; the T0[operand] vs T0[operand+1]
  distinction (52 records) is stated as the weak-membership control, not promoted.

## OPUS-REQ-AUDITSEM-REVIEW-SEAL — verdict:ACCEPT

Read `seal.py` first, then **independently derived** the six mandated mutation shapes (before
reading `test_seal.py`) and executed them against the mechanism:

1. **Shared-result overwrite**: overwrite the live result after sealing → `verify(live=)` reports
   `MOVED`; the sealed receipt still verifies and stays `publishable`. Resealing the changed result
   yields a new `run_id`; old receipt untouched.
2. **Missing case**: result JSON lacking one declared case → `publishable` refuses with
   `case map mismatch: declared-but-absent ['c2']`.
3. **Truncated driver that still parses**: `seal.py` truncated at a statement boundary (ast.parse
   clean) → refused: `driver … is not a committed source (git blob … not in the repository)`. The
   git-blob gate — not parsing — is what catches it, exactly as designed.
4. **Changed input, same count**: new `run_id`, prior receipt intact (`verify` clean).
5. **Interrupted publication**: a stray `.<id>.xxxx.partial` dir is invisible to `load`/`list`;
   resealing identical content is idempotent (same `run_id`).
6. **Valid cumulative reuse**: `case_sources` crediting a case from a publishable source receipt
   passes; the negative twin (source lacks the case) refuses `does not carry it`; WIP refused.

`run_id` demonstrably binds driver+input+result+cases+sources (C1/C4 both changed the identity).
Producer's own `test_seal.py` run afterward: `FAILS 0` — its S1–S6 match my independently derived
shapes one-for-one.

## FRONTIER-REQ-AUDITSEM-EXECUTED-REVIEW-COMPOSER-PREREQ — ACCEPT

Executed through **each composer's own entry point** (not `prereq.py` alone), injecting fault
prerequisites via the documented test-only override variables:

| case | `check_gap_debt.py` | `check_route_collisions_control.py` |
|---|---|---|
| valid input | verdict computed, exit 0 | `CONTROL PASSES` |
| upstream exit 2 | `PREREQUISITE FAILED: …exit 2 (accepted: [0])`, exit 2 | refused, exit 2 |
| missing result object | `does not define ['CENSUS']`, exit 2 | `does not define ['contained']`, exit 2 |
| malformed result object | `CENSUS is not a non-empty dict`, exit 2 | `contained is not callable`, exit 2 |

The data contracts are explicit (`exits=`, `names=`, `validate=`) — the "smaller dependency
contract" A03 required. The ASTRA-reject repair (`1f11830e9`, FAIL detection through the configured
line format) is in the reviewed code.

## OPUS-REQ-AUDITSEM-SIGN-SN1-X-OEB — see signature block

Signature record filed separately below once the archive walk completes; the two negatives were
executed directly by this auditor: `x_negatives.py` `FAILS 0` (N1 N2 N3 C — C is the E-recovery
control, 50/50) and `sn1_q3_x_content.py` `FAILS 0` (Q X G P B N C).
