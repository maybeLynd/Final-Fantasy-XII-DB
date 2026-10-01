---
experiment: EXP-140
title: licence-check execution — the S31 family (00323EC0 /
  00323BB0 / 00324020 / 0030A330) executes native under Unicorn
  through the real validator, decoder, builder and both
  classification chains; the Quickening absent-row edge is
  confirmed on shipping bytes
contract: 12-Items-Equipment-Shops-License/CONTRACT-license-check.md
  (ASTRA-TRANSFER-ORACLE-S31-LICENCE; original request
  OPUS-REQ-ASTRA-S31-LICENCE-CHECK-ISOLATED-RUN)
method: B
live_game: false
tool: evidence/license-check-exec/check.py
---
# EXP-140 — license-check-exec

**Status:** complete · **57/57 functional cases, 35/35 byte-precise
mutants killed, stable across three processes**
**Evidence:** `evidence/license-check-exec/` (`check.py`,
`result.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base
`0x120000`

## Objective

Isolated original-code run of the S31 licence-check family,
transferred from ASTRA. Execute the shipped bodies, distinguish the
absent-action / index-3 edge from ordinary controls, preserve
mask-construction boundaries, and return original behaviour to
OPUS. Per the transfer: a supplied mask exercises the bounded
predicate only — it cannot establish that initialized gameplay
reaches that mask or that bits 0..17 carry the presumed meaning.

## Body census — all real

| VA | role | span |
|---|---|---|
| `00323EC0` | MAIN `BattleStats_HasRequiredLicenseForAction` | real |
| `00323BB0` | PREREQ — mask build + 46-byte AND scan | real |
| `00324020` | POPCNT — bits 0..17 of `rec+0x194` | real |
| `0030A330` | ROWSRCH — 3-byte row search | real |
| `00322C50` | VALID — class dispatcher, class-0x14 arm | real |
| `0020E600` | DECODE — `ecx + q[0x1F83530]` | real |
| `002F8FA0` | BUILDER — node-table walk + mask write | real |
| `00323890` | CLS1 — kind byte → licence class {0..3,−1} | real |
| `003241D0` | CLS2 — kind byte → `0x15+remap` or 0 | real |
| `00861EC0` | memset IAT thunk → planted host `memset` | real thunk, scripted import |
| `00808C40` | `__security_check_cookie` | real (shipped cookie) |

Scripted boundary — exactly one: `memset` itself, reached through
the real thunk `jmp q[IAT 0x8C2A60]` onto a planted host
trampoline (`MSET`); host memsets guest memory and records
`memset:dst:val:n` in the trace. Everything else — the descriptor
walk, both jump-table classifiers, the pointer decoder, the
cookie check, all bit logic — executes as shipped bytes.

## Findings verified on native bytes

**The absent-action edge is real.** `ROWSRCH` returns 3 when the
action id is absent from the party row's three byte slots
(`row+4/+5/+6`) or when the row pointer is null (`cx` defaults
`0xFFFF`). MAIN's I5 compares `idx < n` with **`setl` (signed)**,
where `n` = popcount of licence bits 0..17:

- absent id + count 4 → `3 < 4` → **1 (licensed)** — the
  over-permission edge the contract predicted;
- absent id + count 3 → `3 < 3` → **0** — the boundary;
- absent id + count 9 → 1; present id at slot 2 + count 3 → 1;
  slot 2 + count 2 → 0.

**I5 precedes I4 unconditionally.** A unit owning an I4 licence
for `0xE1` but failing the I5 count still gets 0 (`m-qflank`) —
the Quickening range check runs first and never falls through to
the general test.

**POPCNT is a 3-pass × 6-bit walk, not a popcount intrinsic.**
`dl` is set once (`mov dl,1`) outside the loop and `rol`'d per
test; `r11` walks 2, 8, 14 → bit indices 0..17 exactly; bits ≥18
never participate (`m-qhi`, `d-popover`).

**BUILDER is genuinely iterative:** reloads the node-table
descriptor per row, decodes the row pointer (`decode(enc) +
stride·i`, truncated to 32 bits via `add ebx,eax`), classifies
`b[row+5]` through the CLS1→CLS2 chain, scans eight `u16`
requirement slots at `row+8`, and `bts`-sets bit `i` of the
caller buffer on first match. Return = match count (`ebp`).
`n` is signed-compared (`jle`/`jge`) — `n≤0` skips the loop.

**Descriptor semantics corrected on bytes.** The contract's
validator section implies a class-0x14-specific count source;
natively the arm at `0x322F72` reads **`q[0x2EBF138]` — the
action-table descriptor itself**, and the bound is `d[desc+4]`
(the action-row count). MAIN's I3 then uses `w[desc+8]` (stride)
and `d[desc+0xC]` (encoded row pointer) from the same descriptor.

**Reachability corollary — the null action-descriptor deref is
unreachable through MAIN.** §10's null-deref worry (`test
w[rcx+0x2C]` on a null row) cannot be reached by nulling the
descriptor: VALID reads the same cell first and rejects the id,
returning 0 before I3 executes (`m-nulla` → 0, no fault). The
deref path needs the descriptor non-null with an `enc` that
decodes to a null/low row — `m-nullrow` plants `enc = −BASEP`
(`decode` → `rax = 2^32`, non-null, but the row base truncates to
0) and the native body faults `memr 0x2C,2` at `0x323F52` with
`RAX = 0x2000` stale — confirming both the fault and the exact
register residue.

**Null party descriptor is safe by construction** (`m-nullp`):
`prow = 0` → ROWSRCH's null-row arm → idx 3 → compared against
the count like any absent action.

## Fixture disclosure

All four descriptor cells are BSS (ship 0); the harness plants:

- `q[0x1F83530]` = `BASEP` (guest heap `0x40030000`) — the decode
  pool base;
- `q[0x2EBF138]` → planted action descriptor `{count=0x220,
  stride=0x40, enc=0x400}`;
- `q[0x2EBF130]` → planted party descriptor `{stride=0x20,
  enc=0x1000}`;
- `q[0x2EBF038]` → planted node-table descriptor `{n, stride=0x20,
  enc=0x2000}`;
- the BASE pool image: action flag words at `row+0x2C`, party
  action-id triples at `row+4..6`, node rows `{kind@+5,
  req-ids@+8..+0x15}`;
- a planted `BattleStatsRecord` at `REC` (`b[+4]`=slot,
  `b[+5]`=kind, 46-byte owned mask at `+0x194`).

These are **synthetic supplied masks and tables** — they exercise
the bounded predicates on real code but say nothing about
initialized gameplay reachability, the real node-table contents,
or the meaning of bits 0..17. MODEL-PROVEN-tier fixtures on
native bodies; the executed *control flow, field offsets, compare
shapes and fault residues* are original behaviour.

## Cases (57)

- **I1 exits:** invalid id, null record → 1, kind≠0 → 1,
  slot >6 → 1 (both `7` and `0xFF` — unsigned `ja`).
- **I3:** flag `0x2000` set → 1; flag `0x1000` (wrong bit) →
  falls to I4; null action desc → 0 via validator (see above);
  null row via `enc=−BASEP` → `memr 0x2C,2` fault.
- **I4:** overlap at bit 3 / bit 5 / byte 45 → 1; empty mask,
  wrong-kind-only nodes, unrelated owned bit → 0.
- **I5:** present ids at slots 0..2 with counts 0..4 (the full
  absent-idx3 vs count-3/count-4 boundary); party slot 1 row;
  bits ≥18 ignored; boundary ids `0xD0`/`0xE1` in-range, `0xE2`
  ordinary; I5-beats-I4 flank.
- **Direct bodies:** POPCNT counts 0/1/13/18-cap; ROWSRCH slots
  0/2/3 + null row; VALID ok/boundary/hi/cls0/cls33/null-desc/
  stride-0; DECODE; BUILDER kind-1, kind-2, no-match, slot-7-only
  req; CLS1 arms for kinds 9/14/15/30/0/40; PREREQ direct;
  byte-45-only overlap (46-byte scan is load-bearing).

## Mutants (35, all killed)

Gate and bound mutations across every body — exit predicates
(`jne↔je`, `ja↔jbe`, imm bounds `6`/`0x11`/`0x1F`/`0x1D`/`9`/`3`/
`8`/`0x2E`), flag constants (`0x2000`, `0xFFFF`), row/slot/field
offsets (`+4↔+5`, `+5↔+6`, `+8↔+9`, `+0x194→+0x195`), the `setl`
→`setge` signedness flip, the `lea ecx-1`→`-2` class shift,
`add -0x15`→`-0x14` remap shift, `r11+=6`→`+5` pass stride,
`and eax,7`→`&6` bit mask, `mov eax,edx`→`edx,eax` kind save,
and `REX 48→4C` on the decode `add`. Seven first-pass candidates
proved equivalent (e.g. the AND-bound mutation is invisible when
no overlap lives in byte 45 — hence `d-prereq46`; the
`r11`-stride mutation cancels on a symmetric mask — hence
`d-pop1`) and were re-aimed at distinguishing states rather than
declared.

## Limitations

- Synthetic descriptors/masks/tables: the bounded predicates are
  proven on original bytes; the real table contents, real mask
  population, and bits-0..17 semantics remain fixture-tier.
- Only the class-`0x14` validator arm is modeled; other classes
  dispatch to real arms (the model flags `unmodeled-arm` if a
  mutant reaches one — that itself kills such mutants).
- `memset` is host-scripted via the real IAT thunk (disclosed);
  `__security_check_cookie` executes real with the shipped cookie.
- The ROWSRCH `rax > 2` inner guard is dead under the `jl 3` loop
  bound — modeled as equivalent single-counter iteration.

## Evidence tier

**NATIVE-REPLAY-adjacent**: original shipped bytes executed under
Unicorn on disclosed synthetic state. Fixture content is
MODEL-PROVEN; the executed instruction stream, branch outcomes,
memory effects and fault residues are native authority for the
bounded inputs supplied. Not engine-in-loop; no claim that
initialized gameplay drives these inputs.

## Owner qualification - clear size, loop gate and entry alignment (SWE2-ORACLE, 2026-09-30)

Answers `ASTRA-RETURN-ORACLE-LICENSE-BOUNDARY-WITNESS`. The owner consumes ASTRA's scoped boundary
(`66dd3771a`, `_experiments/evidence/license-builder-clear-boundary/`). Independent review is DONE
(`ASTRA-REVIEW-LICENSE-CLEAR-BOUNDARY`), and OPUS and FABLE have consumed it (`8a409b895`, `75445081d`). Its 57 cases
and 35 mutants were not replayed.
- **The clear precedes the signed loop gate.** `002F8FD3` computes `lea r8d, [rax+7]` (32-bit wrap, zero-extended),
  `002F8FD9` shifts it right by 3, and `002F8FE0` calls the clear. Only then does `002F8FFC` / `002F8FFF`
  (`test r14d` / `jle`) gate the loop. A non-positive signed count is therefore not evidence that no clear was
  requested: a raw `0xFFFFFFF8` asks for `0x1FFFFFFF` bytes.
- **Physical zeroing is the caller's, not the builder's.** A count of 0 is a zero-byte logical mask. The 46 bytes a
  caller sees zeroed are zeroed by the caller `00323BB0` before the call (five qwords, a dword and a word at
  `stack+0x20..0x4D`).
- **Entry alignment of this harness.** `run_one` enters with `RSP = STACK + 0x80000`, so `RSP % 16 = 0` at the first
  instruction. The Win64 convention is 8. ASTRA's witness uses 8 and reproduces this record's normal-predicate
  results. This record's cases are not re-certified for alignment-sensitive paths. None faulted.
- **What stands.** The normal predicate and the absent-action edge.
