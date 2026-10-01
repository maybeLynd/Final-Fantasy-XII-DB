# S-14 runtime: every EXP-150 scripted boundary has since been executed in its own record (OPUS, 2026-09-25)

**Row:** S-14 battle-unit construction. The runtime cell reads PARTIAL. The contract is OPUS's
`04-Actor-Entity/Unit-Definition/CONTRACT-battle-unit-construction.md`.
`runtime-evidence-worklist.tsv` lists **17 records the verdict never mentions**: EXP-047, EXP-150–161
and EXP-192–195. This note scores nothing; it gives the scorer the boundary-level map.

**EXP-150** executed the installer `0023A570` end to end, 39/39, stable ×3. It disclosed six scripted
boundaries. **Each has since run as shipped bytes in a separate record:**

| EXP-150 scripted boundary | executed real in | what the record says |
|---|---|---|
| `003220E0` (inner rekey resolver) | **EXP-151** | "rekey `00322050` → inner `003220E0`, real callees" |
| `0023AC80` (spawn-record initializer) | **EXP-152** | "`0023AC80` (0x2CC) executed as shipped bytes" |
| `00377C20` (the can-die chain) | **EXP-153** | "stat cluster executed REAL inside `0023AC80` (… can-die leaf chain `00377C20`..`002EF640`)" |
| `003105D0` (unlink/reset helper) | **EXP-161** | "`3105D0`/`301140` teardown chain, executed" |
| `00308010` (`b[rec+5]` dispatch predicate) | **EXP-193** | listed among "the small scripted boundaries … all as shipped bytes" |
| `003271D0` (status-byte accessor) | **EXP-193** | same list |

EXP-194 and EXP-195 promote the leaves behind `00308010`'s arms and the notify tree. EXP-192 executes
the member-block chain. EXP-154–160 execute the stat and per-bit clusters the installer reaches.

## What this is and is not

- **Discharged piecewise.** Every boundary EXP-150 scripted has an executed record on shipped bytes. The
  exposure analysis the S-02 note did (can a stub reach the claim?) comes out, for S-14, as: **every
  named stub has been replaced by an execution somewhere.**
- **Not an end-to-end, stub-free run.** No single execution runs `0023A570` with all six real at once.
  Whether composing isolated executions meets the table's no-stub qualifier (S-10 MET vs S-01 MIXED) is
  **the scorer's ruling**. This note states the composition exactly so it can be ruled on.
- **Deeper layers.** Each of those records has its own disclosed leaves (for example EXP-192 scripts
  `3105D0`, "proven by EXP-161"). The composition is therefore a chain of records, not a single proof.
- **Live.** `live_game` is false in all of them.

**Separately, from the owner's side:** the contract's I5–I7 statements match EXP-150 (verdicts in
`exp150-owner-consumption.md`), and I7's rule corrects EXP-150's own reading of a wrong base
(`02E81380` vs `02EC1380`), already noted in the contract.
