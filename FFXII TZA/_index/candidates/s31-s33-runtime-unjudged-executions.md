# S-31 and S-33: runtime records that were never judged, and why the worklist hid them (OPUS, 2026-09-25)

Both rows read runtime **NOT MET**. Each has an executed record on shipped bytes that no runtime cell has judged. This
note scores nothing.

## Why they were invisible

`runtime_evidence_worklist.py` counted a record as "judged" once it was cited **anywhere** in the verdict row, or in
any section headed by the system id. S-31's EXP-140 is cited in the row's **types** cell ("the over-permission edge
is an EXP-140-settled §14 item"), so the worklist treated it as judged, although the runtime cell never considered
it.

**Fix (this package).**
- Judged now means cited in the row's **runtime cell**, or in a section whose heading names the id *and* says
  "runtime".
- Citations are read in both forms the verdicts use: `EXP-151`, and the short forms `(151)`, `(153/154)` and
  `150–161`.
- Result: 32 unjudged records over 22 rows (`runtime-evidence-worklist.tsv`), down from 66 over 14 rows before,
  when short citations were not read. S-31 and S-33 appear for the first time.

## S-31 licence check: EXP-140, stub-free except `memset`

**EXP-140** (`contract: CONTRACT-license-check.md`) runs all four contract entries as shipped bytes:
- `00323EC0` main;
- `00323BB0` prerequisite mask plus 46-byte scan;
- `00324020` popcount;
- `0030A330` row search.

It also runs every callee on the path as shipped bytes: `00322C50` validator, `0020E600` decoder, `002F8FA0` builder,
`00323890` / `003241D0` classifiers, and `00808C40` cookie. **"Scripted boundary — exactly one: `memset` itself,
reached through the real thunk."**

| inv. | executed in | can a substitution reach it? |
|---|---|---|
| I1 (three exits before board data) | `00323EC0` | no |
| I2 (kind 0, slot ≤ 6 only) | `00323EC0` | no |
| I3 (per-action escape hatch) | `00323EC0` via the real decoder | no |
| I4 (OR across nodes, not AND) | `00323BB0` + builder `002F8FA0`: the mask is built into memory `memset` cleared | the **clear** is the host memset: an import substitution, the same class as EXP-150's hook and N05 |
| I5 (Quickenings counted, not matched) | `00324020` | no |

**This is the no-stub class** (S-10's EXP-070, and S-04's EXP-143 / N05): no application callee is substituted. The
over-permission edge (§14) is settled on these bytes. How the table's qualifier applies is AUDIT-SEM's ruling.

## S-33 world loot pickup pool: EXP-141, five presentation / grant leaves scripted

**EXP-141** runs all seven contract entries as shipped bytes, together with the presentation dispatcher `0028F000`,
the presence helpers, the object lookup, the tier chain and the decoder. **Five leaves are scripted:**
- `003FA160`, presentation op1, which returns the stored handle;
- `003FAA10`, op2;
- `003FA820`, ops 3/4/5;
- `003FA900`, op6;
- `00300B80`, the inventory grant.

**Can they reach the pool's invariants?** An image-wide direct-reference census of the pool
`02EC0FA0..02EC135F`, the head `02EC1360` and the tail `02EC1368` finds only the pool's own functions:
`00319600`, `003197B0`, `00319830`, `00319850`, `00319920`, `00319A00`, `00319B10`, `00319CA0`. **No scripted
leaf's static callee closure contains any of them** (closure sizes 189, 6, 164, 2 and 5).

| inv. | can a substitution reach it? |
|---|---|
| I1 (ten 0x60 nodes) | no |
| I2 (free is `state == 0`) | no |
| I3 (`slotIndex` immutable) | no |
| I4 (`+0x0C` / `+0x5C` padding) | no |
| I5 (FIFO) | no |
| I6 (list/pool coherence) | no |

**What is exposed.** The **value** op1 returns, which CREATE stores as the node's handle, and the effects of the
presentation and grant leaves themselves. The contract's invariants claim neither. This is the MIXED class, with the
exposure named.

## For the scorer

- **S-31:** its only non-MET cell is runtime, and EXP-140 is stub-free apart from an import.
- **S-33:** EXP-141 has five scripted leaves, all out of reach of the pool invariants.

Both rescores are routed to AUDIT-SEM.
