# S-28 runtime: per-invariant stub exposure for EXP-051 (OPUS, 2026-09-25, block 301)

*Drafted by a delegated OPUS pass and reviewed before publication (block 301): its concrete address claims were spot-checked against the image; see the block-301 inbox entry for which.*

**Row:** S-28 party roster and leader change. Runtime **MIXED** — *"EXP-051 executes the deferred focus publication
(recording stubs, labeled interventions) under isolated original-code replay … no per-invariant stub-exposure
analysis yet"*. Binding gap: *"types PARTIAL and nothing executed — runtime is ASTRA/ORACLE's gap; the contract no
longer binds it"*. Contracts (column 6 of `important-subsystems.tsv`), all under `11-Party/`:
`CONTRACT-party-slot-assignment.md` (one invariant, the slot ↔ `+0x12` bijection),
`CONTRACT-party-focus-and-control-suppression.md` (PF-1..PF-8), `CONTRACT-the-five-parallel-slot-maps.md`
(SM-1..SM-8) and `Battle-State-Block/CONTRACT-battle-state-block.md` (BS-1..BS-5). Evidence class: isolated
original-code replay (Unicorn, `live_game: false`). This note scores nothing.

**Which contract the record belongs to.** EXP-051's front matter reads `contract: none - Deferred focus commit
00358BC0 is outside the existing party-slot assignment contract`. That was true at recovery (2026-09-12). It is
stale now: `CONTRACT-party-focus-and-control-suppression.md` lists `00358BC0` as its first entry and cites EXP-051
in PF-5 and §13. The record executes nothing from the other three contracts.

## Substitutions per record

Read from `_experiments/evidence/EXP-051-focus-commit-reentrancy/check.py`: `STUBS`, the `step` hook, and the
`mutant` path.

| record | runs as shipped | substituted |
|---|---|---|
| **EXP-051** (`evidence/EXP-051-focus-commit-reentrancy/check.py`) | `00358BC0` whole, all 156 B through the `ret` at `00358C5B` (extracted from the certified EXE; hash-checked) | **Application stubs** (the hook pops the return address; `rax` is set; `rcx` is clobbered to `0xBADF00D`): `003588B0` handle resolver (returns a fixed `ACTOR` for the old handle, or for the new one only when `new_actor`; otherwise 0), `00358B40` clear-current, `00259800` preparation, `0025A680` / `0025A690` teardown thunks. **Omitted tail:** `002681D0` is never executed; the run stops on arrival and logs `rcx`. **Fixtures:** one `0xA5`-patterned page holding current `022C7FE0`, pending `022C7FE4` and kind `022C7FF8`. **Controlled interventions** (labelled in `result.json`): a teardown stub writes pending (+ kind 1); `00259800` writes kind 2 or 0. **Mutant:** the 6-byte pending re-read at `00358C24` is NOPped. **No import bridges** |

## What each stub's real body can do (static, shipped image)

| stub | real body's writes / calls | reach into the focus block |
|---|---|---|
| `003588B0` | no non-stack stores in its body; calls `00263FF0` (not read) | none known. It returns the actor pointer that the commit tests at `00358C46` |
| `00358B40` | **stores 0 to current at `00358B6B`** (one of PF-1's three writers); calls `002671F0`, `003588B0`, `0025D650`, `0026D6D0`, `002EC5B0`; tail-jumps `002681D0` on the **old** actor | current only, and the commit overwrites it at `00358C2F` in the same call. Its direct-call closure (11 functions) reaches neither pending writer |
| `00259800` | a 5-instruction leaf: `mov dword [0x860·ecx + 02098574], 0`, `ret` | **none.** Called with `ecx = 0`, it can only zero `02098574`. The two "preparation changes kind" interventions model a behaviour this callee does not have |
| `0025A680` / `0025A690` | thunks into `0025A6A0` (calls `00259510`, `0025A180`, `003D9B80`) | none by direct calls. The pending handle's only writers image-wide are `003594B0` (request) and `003590E0` (reset); the kind byte's are `00358BC0`, `003590E0`, `003594B0`, plus `003594C0`, which is outside the function list (`data_xref_scan.py`, control `022C7FE0` = 18 refs). None of them is in the teardown's direct closure. Indirect calls not covered |

## Per invariant

| invariant | executed by | can a substitution reach it? |
|---|---|---|
| focus **PF-1** three writers of `022C7FE0`, one installs from outside | census (static). EXP-051 executes one writer (`00358C2F`); a second (`00358B6B`, inside `00358B40`) is stubbed | n/a, a static census claim. The stubbed writer's store is overwritten at `00358C2F` within the same call |
| **PF-2** encapsulation by address | census (static) | n/a |
| **PF-3** the change is deferred; only `debug_setpc` (`0050C610`) collapses it | **not executed**: the requester `003594B0` and `0050C610` do not run; pending is planted | coverage, not exposure |
| **PF-4** a commit that changes nothing still stores, clears kind, resolves and tail-calls | EXP-051 "current equals pending" and "equal handles, nonnull new resolution": store `00358C2F` and clear `00358C35` observed as original writes; the run arrives at `002681D0` with the actor argument | **Store, clear, resolve call: no** — body-local, and no stub precedes them on the equal path (`00358BE4 je 00358C2F`). **The tail call** is conditional on the resolver's return (`00358C46`/`00358C49`), and that return comes from stubbed `003588B0`. This selects tail-call vs return on both the equal and the changed paths alike, so it does not bear on "skips only the teardown". `002681D0` itself is not executed |
| **PF-5** the pending handle is re-read after the teardown; consumed (kind cleared) before resolve and push | EXP-051: all ten controls, the `0xBADF00D` volatile clobber, and the NOP mutant at `00358C24` (detected) | **no** — the order is body instructions. The teardown-replaces-pending case is a **fixture intervention** that tests the caller's response, and the real teardown's direct closure contains no pending writer. PF-5's second consequence ("anything the final push calls may request a fresh change without being clobbered") needs `002681D0`, which is **not executed** |
| **PF-6** kind selects exactly one call at the end of one shared body; kind 2 = summon | **selection executed**: `00358C01`/`00358C05` pick `0025A680` vs `0025A690` for old-zero, kind 1 and kind 2 | **selection: no** (body-local reads of `ebx` and the kind byte; the "preparation changes kind" intervention shows the read is the late one at `00358C05`). **Not executed:** the shared body `0025A6A0` (its single flag test at `0025A800` and `003D9B80`) is behind the stubbed thunks, and the kind-2 writer `003594C0` does not run. Coverage, not exposure |
| **PF-7** suppression mask `0x8800403B` vs `0x8800003B` | **not executed**: no record runs `0023B040` (the contract's §13 says so) | coverage, not exposure |
| **PF-8** triple `+0x698` load, double null check | not executed | coverage, not exposure |
| slot-assignment **invariant** (`roster[i]` ↔ record `+0x12`; bulk clears break it) | **not by EXP-051.** The contract's §13 cites the differential pilot `diff_party_slots.py` (runs `00269C70`, `00263750`, `00263770`; 173 commands, 0 mismatches). That is not an EXP record and is not named in the cell; its substitutions were **not read** | coverage by this row's record: none |
| slot maps **SM-1..SM-8** | not executed (the contract's §13: "None") | coverage, not exposure |
| battle-state block **BS-1..BS-5** | not executed (the contract's §13: "None") | coverage, not exposure |

## Findings and contradictions

- **The binding-gap cell is stale on both halves.** "types PARTIAL": the types cell reads MET (re-scored
  2026-09-25). "nothing executed": the runtime cell names EXP-051, which executes `00358BC0` as shipped.
- **EXP-051's `contract: none` front matter is stale**, as above; it now belongs to
  `CONTRACT-party-focus-and-control-suppression.md`.
- **Two of the ten controls test a counterfactual.** "Preparation changes kind to 2" and "to 0" give `00259800` a
  write it cannot make: its shipped body zeroes one dword at `02098574` and nothing else. The record labels them
  interventions ("they do not prove any native callee actually does so"). This note adds that the named callee
  provably does not. The teardown-replacement cases are likewise unsupported by any pending writer in the
  teardown's direct-call closure. That is static, and indirect calls are not covered.

## For the scorer

- EXP-051 substitutes **5 application stubs**, **1 omitted tail** (`002681D0`), **fixtures** (the focus page) and
  **labelled interventions**. There are **no import bridges**.
- **Exposure on executed focus invariants:**
  - PF-4 and PF-5's ordering claims and PF-6's selection: **no substitution reaches the asserted order or value.**
  - The resolver stub's return decides only whether the tail call is reached.
  - The stubbed `00358B40`'s store to current is overwritten in the same call.
- **Unexecuted:**
  - PF-3, PF-5's push consequence, PF-6's shared teardown body, PF-7 and PF-8;
  - all of slot-assignment, SM-1..SM-8 and BS-1..BS-5.
  - This is coverage, not exposure. Three of the row's four contracts have no execution in the cell's record.
- Not read: `00263FF0` (under the resolver), the teardown's indirect calls, `diff_party_slots.py`'s substitutions.
- `live_game` is false.
