# Runtime worklist triage: the 32 records no runtime cell has judged (OPUS, 2026-09-25, block 258)

The corrected `runtime_evidence_worklist.py` (block 257: runtime-cell citations only, short citation forms read) lists
**32 unjudged records over 22 rows** (`runtime-evidence-worklist.tsv`). This triage gives the scorer each record's
class and what it bears on. It scores nothing.

## Records that bear on a NOT MET row

| row | record | class | reading |
|---|---|---|---|
| **S-31** | EXP-140 | replay; only an import (`memset`) substituted | every entry and callee runs as shipped bytes; runtime is S-31's only non-MET cell (`s31-s33-runtime-unjudged-executions.md`) |
| **S-33** | EXP-141 | replay; 5 leaves scripted | none of the 5 reaches the pool's I1–I6 (same note) |
| **S-22** | EXP-111 | replay; **no calls, no scripted boundary** (8/8, 20/20 mutants, ×3) | executes the MT19937 twist `00866B90` (`CONTRACT-preparation-step-family.md`). It is **one primitive of one of S-22's four contracts**, so it is evidence, not coverage |
| S-18 | EXP-132 | replay; `contract: none` (consumer anchor) | the nav consumer chain; `s51-runtime-per-invariant-exposure.md` maps its residue |

## Live records not yet judged

| row | record | what it observes | bears on the row's gap? |
|---|---|---|---|
| **S-17** | EXP-019 | pre-kill group registration (member mask 1, dead mask 0) | **No.** The approach failed and the party leader was knocked out before any grouped enemy died. The record says it gives "no test of the last-kill completion flag", so S-17's gap ("the completion transition itself has no live capture") **stands** |
| S-13 | EXP-026 | the kind-3 actor region map across a zone transition | contract `CONTRACT-actor-record-pool-and-region-map.md`; not analysed here |
| S-16, S-43 | EXP-080 | an older-format save loaded to Southgate | `contract: none`; bounded save/load evidence |
| S-09 | EXP-002, EXP-079 | st2e group tables; arena placement | EXP-079's contract is S-47's arena, not S-09's |
| S-32 | EXP-081 | initialized BattleUnit bindings | `s32-runtime-per-invariant-exposure.md`: bindings, not reward contents |
| S-44 | EXP-001 | FrameLimit drives the time base | S-44's runtime is already LIVE |

## Replay records already analysed in OPUS notes

| record | row | note |
|---|---|---|
| EXP-076, EXP-081 | S-09 / S-32 | `s32-runtime-per-invariant-exposure.md` |
| EXP-077 | S-09 | `s47-runtime-per-invariant-exposure.md` |
| EXP-093 | S-03 | `s21-runtime-per-invariant-exposure.md` |
| EXP-100 | S-04 | `s04-runtime-per-invariant-exposure.md` |
| EXP-128 | S-08 | `s08-runtime-per-invariant-exposure.md` |
| EXP-075 | S-14 | `s32-runtime-per-invariant-exposure.md`: its 9 stubs are the installer callees EXP-150 runs real |
| EXP-070 | S-46 | the S-10 no-stub precedent (`s02-runtime-rejudged-against-exp191.md`, `s04-runtime-stub-free-execution.md`) |

**Not analysed by OPUS** (other owners' contracts):
- EXP-078 (S-09);
- EXP-011, EXP-014 (S-17);
- EXP-098, EXP-099 (S-42);
- EXP-041 (S-44);
- EXP-113, EXP-114 (S-48);
- EXP-085 (S-07);
- EXP-049 (S-15);
- EXP-060 (S-21, the hp-write contract);
- EXP-068 (S-36).

**A caution for the worklist.** It maps records to rows through the contracts a row cites. So a record can appear on
a row whose own contract it does not execute: EXP-076, 077, 078 and 079 appear on S-09 through its contract list.
Such an entry shows that the row's contracts cite the record, not that the record is that row's evidence.
