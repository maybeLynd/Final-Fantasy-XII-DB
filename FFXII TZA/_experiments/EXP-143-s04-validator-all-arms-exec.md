---
experiment: EXP-143
title: S-04 validator executed across all thirty-two class arms —
  00322C50 under Unicorn with LOW-1/LOW/HIGH/HIGH+1 probes per
  class; every arm confirms the inclusive-signed shared tail,
  LOW/HIGH recorded from emulated registers at 0032302E, and the
  class-1 two-level nibble dispatch positively identified per
  arm executed
contract: 00-Engine-Core-Runtime/CONTRACT-encoded-id-space-and-class-registry.md
requests:
  - FABLE-REQ-ORACLE-S04-VALIDATOR-ALL-THIRTY-TWO-CLASS-ARMS
method: B
live_game: false
tool: evidence/s04-validator-arms/check.py
---
# EXP-143 — s04-validator-arms

**Status:** complete · **producer counter 173, zero reported failures, historical stability ×3**
**Evidence:** `evidence/s04-validator-arms/` (`check.py`,
`result.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base
`0x120000`

## SECTION-05 retained review and counting correction

The original `check.py` and `result.json` are unchanged. Its `summary.cases=173` is155 direct
class2..32 probe entries plus18 outer class1 groups. The retained result actually contains246
traced probe records (including28 unplanted and63 nested class1 probes) and four further
summary-only returns. These are not all separately numbered producer cases and are not new runs.
An independent reducer verifies their signed bounds, original32-entry jump table and15 registry
class words; eight corrupted variants are rejected. The current query/rebase section adds its own
bounded200 native assertions, separately counted. See
[Section05](evidence/continuation-section05-encoded-query/REVIEW.md).

## Objective

Execute `00322C50` (`ecx`=class, `edx`=id) across **all 32 class
arms** — the last unexecuted cell in S-04's runtime row. Per
class record the arm taken, the LOW/HIGH bounds **as observed in
registers at the shared tail** `0032302E`, and accept/reject at
`LOW-1`, `LOW`, `HIGH`, `HIGH+1`, plus a signed-negative probe.
This supersedes the "arm 6 of 32 only" state (EXP-100) and the
"2 of 32" state (adding EXP-140's class-0x14 arm).

## Mechanism confirmed on shipped bytes

`00322C50`: `a = cls-1; a > 0x1F → 0`; `jmp jtab[0x323054 + a·4]
+ 0x120000`. Every arm converges on the tail:

```text
0032302A/2C  ecx = HIGH+1 (arm-supplied), edx = LOW (arm-supplied)
0032302E     cmp ebx, edx     ; jl  -> 0   (SIGNED)
00323036     lea eax,[rcx-1]  ; HIGH = ecx-1
00323039     cmp ebx, eax     ; jg  -> 0   (SIGNED)
00323041     mov eax, 1
```

**Verdict: `LOW ≤ id ≤ HIGH`, inclusive, signed — verified by
execution on all 32 classes** (`[0,1,1,0]` at the four
boundaries, plus `0` at a negative probe everywhere).

## Per-class executed table (planted count `0x40`)

| cls | arm | kind | cell(s) | LOW | HIGH | verdicts |
|---|---|---|---|---|---|---|
| 2 | `322C9A` | desc | `2EBF130` | 0 | 63 | 0 1 1 0 |
| 3 | `322CB4` | desc | `2EBF120` | 0 | 63 | 0 1 1 0 |
| 4 | `322CCE` | desc | `2EBF150` | 0 | 63 | 0 1 1 0 |
| 5 | `322CE8` | desc | `2EBF100` | 0 | 63 | 0 1 1 0 |
| 6 | `322D02` | bias | `2EBF0F8` | `0x1000` | `0x103F` | 0 1 1 0 |
| 7 | `322D2C` | bias | `2EBF098` | `0x2000` | `0x203F` | 0 1 1 0 |
| 8 | `322D56` | bias | `2EBF0F0` | `0x3000` | `0x303F` | 0 1 1 0 |
| 9 | `322D80` | bias | `2EBF0E8` | `0x4000` | `0x403F` | 0 1 1 0 |
| 10 | `322DAA` | bias | `2EBF0E0` | `0x5000` | `0x503F` | 0 1 1 0 |
| 11 | `322DD4` | bias | `2EBF0D8` | `0x6000` | `0x603F` | 0 1 1 0 |
| 12 | `322DFE` | bias | `2EBF0D0` | `0x7000` | `0x703F` | 0 1 1 0 |
| 13 | `322E28` | **sum4** | `2EBF090/088/080/078` | `0x8000` | `0x8000+Σ−1` | 0 1 1 0 |
| 14 | `322E91` | bias | `2EBF070` | `0x9000` | `0x903F` | 0 1 1 0 |
| 15 | `322EBB` | bias | `2EBF068` | `0xA000` | `0xA03F` | 0 1 1 0 |
| 16 | `322EE5` | bias | `2EBF060` | `0xB000` | `0xB03F` | 0 1 1 0 |
| 17 | `322F0F` | bias | `2EBF0C8` | `0xC000` | `0xC03F` | 0 1 1 0 |
| 18 | `322F39` | bias | `2EBF058` | `0xD000` | `0xD03F` | 0 1 1 0 |
| 19 | `322F63` | **const** | — | `0xE000` | **`0xEFFE`** | 0 1 1 0 |
| 20 | `322F72` | desc | `2EBF138` | 0 | 63 | 0 1 1 0 |
| 21 | `322F8C` | desc | `2EBF128` | 0 | 63 | 0 1 1 0 |
| 22 | `322FA6` | **const** | — | 0 | 3 | 0 1 1 0 |
| 23 | `322FAF` | **const** | — | 0 | 8 | 0 1 1 0 |
| 24 | `322FB8` | desc | `2EBF110` | 0 | 63 | 0 1 1 0 |
| 25 | `322FCB` | desc | `2EBF038` | 0 | 63 | 0 1 1 0 |
| 26 | `322FDE` | desc | `2EBF118` | 0 | 63 | 0 1 1 0 |
| 27 | `322FF1` | desc | `2EBF050` | 0 | 63 | 0 1 1 0 |
| 28 | `323004` | desc | `2EBF0B0` | 0 | 63 | 0 1 1 0 |
| 29 | `323017` | desc | `2EBF040` | 0 | 63 | 0 1 1 0 |
| 30 | `322EBB` | bias | `2EBF068` | `0xA000` | `0xA03F` | 0 1 1 0 |
| 31 | `322EBB` | bias | `2EBF068` | `0xA000` | `0xA03F` | 0 1 1 0 |
| 32 | `322FCB` | desc | `2EBF038` | 0 | 63 | 0 1 1 0 |

LOW/HIGH above are the **observed** tail registers (`edx`,
`ecx−1`), not a static reading.

## Findings

- **Inclusive-signed confirmed on all 32 arms.** An
  the disassembly establishes signed comparisons. Negative rejection under these nonnegative
  fixture bounds does not alone distinguish every unsigned implementation. A correct unbiased
  index/count form can express a range; using raw biased IDs as zero-based indices cannot.
- **Bias `(cls−5)·0x1000` confirmed for cls 6–18** — observed
  LOW matches the nibble layout exactly: the top nibble of an id
  in the `0x1000–0xDFFF` band is class MINUS FIVE, not class itself.
- **cls 19 constant is `[0xE000, 0xEFFE]`**, not `0xEFFF` —
  `ecx=0xEFFF` makes `HIGH = ecx−1`. `0xEFFF` rejects, executed.
  The contract's old §6 prose ("0xE000–0xEFFF") was off by one and is corrected by SECTION-05;
  interestingly the nibble table's authored count for row `0xE`
  is 4095 → `0xE000+4095−1 = 0xEFFE`, so `0xEFFF` was never a
  valid id.
- **cls 13 sums four descriptors.** `Σ = 3+5+7+11 = 26` →
  HIGH `0x8019` accepted, `0x801A` rejected. With one descriptor
  left null the sum drops to 23 → `0x8016` accepted, `0x8017`
  rejected: **a missing descriptor contributes 0, it does not
  void the range** (unlike single-descriptor arms, where null →
  empty range → all-reject).
- **Descriptor-absent = shipped BSS state.** Every descriptor
  cell (`0x2EBF038`–`0x2EBF150`) lives past `.data`'s raw size —
  runtime-populated. Probed unplanted: all 28 descriptor-reading
  class cases (including shared-arm aliases) reject mid-range ids; constants and cls 1 unaffected.
- **cls 30/31 alias the cls-15 arm** (`322EBB`, bias `0xA000`),
  **cls 32 aliases cls-25** (`322FCB`). Executed under their own
  class numbers — same arm, same bounds.
- **cls 0 / cls 33+** reject before any arm (`a > 0x1F`).

## Class 1 — two-level dispatch, positively identified

`322C7E`: `movzx ecx,bx` → `00309440` → `nibble = id16 >> 12`;
`nibble > 0xE → −1` → reject; else `d[0x1EEBCF8 + nibble·0x58]`
= subclass → `dec` → re-dispatch through the **same** jump
table under the **same 32-bit id**. The shipped table maps
nibble `n → n+5` (subclasses 5–19).

Every nibble executed with the mapper result AND the actual arm
address recorded:

| nibble | sub | arm | bounds under plant | L−1 | L | H | H+1 |
|---|---|---|---|---|---|---|---|
| 0 | 5 | `322CE8` | `[0,63]` | 0 | 1 | 1 | 0 |
| 1 | 6 | `322D02` | `[0x1000,0x103F]` | 0 | 1 | 1 | 0 |
| 2 | 7 | `322D2C` | `[0x2000,0x203F]` | 0 | 1 | 1 | 0 |
| 3 | 8 | `322D56` | `[0x3000,0x303F]` | 0 | 1 | 1 | 0 |
| 4 | 9 | `322D80` | `[0x4000,0x403F]` | 0 | 1 | 1 | 0 |
| 5 | 10 | `322DAA` | `[0x5000,0x503F]` | 0 | 1 | 1 | 0 |
| 6 | 11 | `322DD4` | `[0x6000,0x603F]` | 0 | 1 | 1 | 0 |
| 7 | 12 | `322DFE` | `[0x7000,0x703F]` | 0 | 1 | 1 | 0 |
| 8 | 13 | `322E28` | `[0x8000,0x80FF]` (Σ=4·N) | 0 | 1 | 1 | 0 |
| 9 | 14 | `322E91` | `[0x9000,0x903F]` | 0 | 1 | 1 | 0 |
| A | 15 | `322EBB` | `[0xA000,0xA03F]` | 0 | 1 | 1 | 0 |
| B | 16 | `322EE5` | `[0xB000,0xB03F]` | 0 | 1 | 1 | 0 |
| C | 17 | `322F0F` | `[0xC000,0xC03F]` | 0 | 1 | 1 | 0 |
| D | 18 | `322F39` | `[0xD000,0xD03F]` | 0 | 1 | 1 | 0 |
| E | 19 | `322F63` | `[0xE000,0xEFFE]` | 0 | 1 | 1 | 0 |
| F | −1 | none | reject | — | — | — | — |

Cross-boundary probes land in the **neighboring** subclass arm
(e.g. `0x7FFF` → subclass 12's arm `322DFE`, rejected there) —
the arm-hit record proves which subclass executed, a positive
identification rather than a plausibility check. `0x11000` maps
via low16 nibble → subclass 6 but the **full** id is range-
checked → reject. `−1` and `0xF000` → mapper `−1` → reject.

The mapper uses the PRE-BIASED base `01EEBCF8`, equal to the full descriptor base
`01EEBCC0 + 0x38`. Therefore its `rec+0` and the contract's descriptor+0x38 name
the SAME class word; the former claim that the contract read the wrong field is withdrawn.
The next DWORD is the full descriptor's +0x3C count.

## Scripted-boundary disclosure

- Descriptor buffers are synthetic: a pointer cell in BSS → a
  heap fixture `{0x77×4, count@+4, …}`. Counts are runtime data;
  `0x40` (and `3/5/7/11` for the sum arm) are fixture values, so
  the reported HIGHs are **shape-verified bounds under a known
  count**, not deployment counts.
- The class-1 nibble table (`0x1EEBCF8`) is shipped `.data`
  read natively, not a fixture.
- No imports execute; the validator and `00309440` are pure
  leaf code.
- Evidence class: **NATIVE-REPLAY** over shipped bytes with
  MODEL-PROVEN descriptor fixtures. No initialized-gameplay
  reachability claim.
