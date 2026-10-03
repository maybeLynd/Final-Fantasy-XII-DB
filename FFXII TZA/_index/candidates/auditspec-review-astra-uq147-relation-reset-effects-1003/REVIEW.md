# SWE2-AUDIT-SPEC review: ASTRA's UQ147 inline-reset versus linked-release effects (uq147-relation-reset-effects)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not ASTRA) · 2026-10-03 · Task: `ASTRA-REQ-SPEC-UQ147-RELATION-RESET-EFFECTS-1003` · Commit reviewed: `e06561376ab111219cef704be4cb1b21bd558230` · Package: `_experiments/evidence/uq147-relation-reset-effects/`

## SWE2-AUDIT-SPEC verdict: ACCEPT

Both leaves do exactly what the result states and nothing more. The capture, the proof and the refusal reproduce. All
three controls refuse.

The ownership consequence is correctly stated as conditional. Resetting a non-empty owner in place discards its links
without reclaiming its nodes, but that is a local effect under a forced premise. It is not evidence that any real caller
does this.

## SWE2-AUDIT-SPEC checks

- `manifest.json` sha256 `982c3630d42738832e0e73b1610de7c9c44a9f190d4e50803ac58dcbda855ae4`, as named.
- The drivers are identical in the package and in ASTRA's working copy: capture `capture-relation-reset-leaves.py`
  (`d1718ca9…`) and producer `prove-relation-reset-effects.py` (`5b616396…`).
- **Reproduced to fresh scratch paths:**
  - The capture exits 0 and is **byte-identical** to `source-relation-reset-leaves-01.json`.
  - The proof exits 0, with stdout `Inline reset != linked-pool release; conditional ownership effect proved without
    live execution.`. It is **byte-identical** to `result-relation-reset-effects-01.json`, and the same run re-derives
    the three `controls` entries.
- **Actual-CLI prerequisite:**
  - The producer re-run with `reviewed-boundaries-failed-prerequisite-01.json` exits 1 with
    `ValueError: successful upstream qualification required` and writes no output file.
  - `actual-prerequisite-control.json` hashes match the files: positive status `b8a8bb24`, positive result `e492dd3a`,
    failure status `573071c8`, failed input `51cfcced`.
  - `freeze-relation-reset-1003.py` L15 requires exit 1, a null exception, the current driver sha and the exact argv.
- **`00512EE0` (15 B, `00512EE0`-`00512EEE`, `int3` at `00512EEF`):**
  - `and byte [rcx+0xF], 0xF0` clears the low flags and keeps the high nibble.
  - `mov word [rcx+0xC], 0xFFFF` sets head and tail to FF.
  - `mov byte [rcx+0xE], 0` zeroes the count.
  - Then `ret`. Nothing else is written.
- **`00512C80` (78 B, `00512C80`-`00512CCD`, `int3` at `00512CCE`):**
  - A head `[rcx+0xC]` of FF jumps straight to the reset (`00512C86` -> `00512CBF`). The global counter is then neither
    read nor written.
  - Otherwise `dl` = byte `02EBA481`, read once (`00512C88`). The loop runs over pool `02CA81F0` + 16·index: `add dl, 0xFF`,
    `and byte [node+0xF], 0xF0`, and next = `[node+0xE]` until FF.
  - `dl` is stored to `02EBA481` once, after the loop (`00512CB9`). This is the cached, non-atomic update, (old - n) mod 256.
  - Then the same three-store reset as `00512EE0`.
  - Write sites `00512CAD/CB9/CBF/CC3/CC9` equal `facts.linked_write_sites`.
- **Absences, read from the bytes:**
  - Neither body writes a node DWORD ID (`+0/+4/+8`), a node link or self-slot byte (`+0xC/+0xD/+0xE`), the cursor
    `02CA83F0` or the high count `02EBA480`.
  - Neither body contains a call, an indirect jump or a heap call.
  - The loop does not bound the index to 32 slots, since any byte below FF is followed. "n <= 32" therefore rests on the
    stated premise of consistent indices 0..31/FF and a finite acyclic list, as the result says.
- **Controls:** each of the three is refused:
  - `drop-pool-release` and `wrong-global-counter`: "linked-release pool/count footprint changed";
  - `reset-pool-write`: "inline reset unexpectedly touches pool or count".
  Two causes share one detector message, which is acceptable because the footprint check covers both the pool store and
  the counter's identity.

## SWE2-AUDIT-SPEC consumer preconditions (for OPUS's ownership contract)

A reconstruction may use the inline reset (`00512EE0`) in place of the linked release (`00512C80`) only when the owner
list is already empty, with head = FF. On a non-empty owner, the inline reset leaves the owned pool rows marked occupied
and leaves `02EBA481` uncounted. Which real callers call which leaf, and in what order, is not settled here. That is
ASTRA's named next discriminator.

## SWE2-AUDIT-SPEC limits

Static Method A; no native or live run. The result's premises and limits stand as written:
- disjoint, valid owner and pool;
- a finite acyclic list;
- no interference with the non-atomic counter update.

These are not established here: initialisation, caller order, ownership uniqueness across owners, reuse, malformed-list
termination, natural KO/Esper113, and the full UQ147 question. This review is distinct from the review of
the native-relation invariant (`86cdcde10`), and it does not accept that one by implication.
