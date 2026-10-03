# SWE2-AUDIT-SPEC review: ASTRA's UQ147 native-relation invariant (uq147-native-relation-invariant)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not ASTRA) · 2026-10-03 · Task: `ASTRA-REQ-SPEC-UQ147-NATIVE-RELATION-INVARIANT-1003` · Commit reviewed: `86cdcde102503c7988c8b95202a629c36021275a` · Package: `_experiments/evidence/uq147-native-relation-invariant/`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The current producer's result reproduces byte for byte. The two bounded bodies have exactly the transfers and persistent
writes the result names. The creation guard and the double-removal exclusion hold at the bytes, and an independent
reducer agrees with them. The four source-record controls and the actual-CLI prerequisite refuse as labelled.

## SWE2-AUDIT-SPEC checks

- `manifest.json` sha256 `e1db8d80874a9a1c9b38948d5a3e56eeff8fe659586a5b094e0628a0fd85ac3c`, as named.
- Producer `prove-native-relation-invariant.py` `769766d3…` is identical in the package and in ASTRA's working copy, and
  matches `prove-native-relation-invariant-02.status.json` (terminal, exit 0). Re-run to a fresh scratch path: exit 0,
  stdout `Closed native cache effects; coherent-state double removal excluded, broken-premise witness retained. No
  native/game execution.`. The output is **byte-identical** to `result-native-relation-invariant-02.json`, and the four
  `controls` entries are re-derived by the same run.
- **Actual-CLI prerequisite:**
  - Re-run of the producer with `reviewed-boundaries-failed-prerequisite-01.json`: exit 1,
    `ValueError: successful upstream qualification required`, no output file. This matches
    `prove-native-relation-refusal-01.status.json` (terminal, exit 1, exception null).
  - `check-native-relation-prerequisite.py` (`82876fb4…`) pins that exact argv and hashes the matching positive status
    and result. A failed wrapper exit alone does not satisfy it.
- **Transfers (raw capstone over the certified image, 00512F30-00513143 and 00512CD0-00512D71):**
  - The only non-return transfers are `00513005 call 0x512cd0` and `00513022 jmp 0x512cd0`, plus two local `jmp`s inside
    00512CD0.
  - There is no indirect call, no import thunk and no heap call. Each body ends in `int3` padding: 00513144 and 00512D72.
- **Persistent writes, counted from the disassembly:**
  - 26 in 00512F30. This excludes the `[rsp+0x30]` rbx spill. The 26 are the cursor `02CA83F0` (×2), the counters
    `02EBA480`/`02EBA481`, node `+0/+4/+8/+D/+E/+F`, the receiver's head/tail/count and `+0/+4/+8/+F`, and one
    `[r10+rdx*8+0xE]`.
  - 11 in 00512CD0.
  - Both sets equal `facts.nonstack_writes` site for site.
- **Creation guard:** on a miss, creation requires `byte [packet+1]==0` (`00512F94/98`) and `dword [packet+4] !=
  dword [packet+0xC]` (`00512F9D/A0`).
- **Matched arm:**
  - The remove call needs flag 1 and `node+8 == packet+0xC` (`00512FF1`-`00513005`).
  - The tail removal needs `packet+4 == packet+0xC` (`0051300D/10`).
  - Otherwise `node+8 = packet+0xC` (`00513027`). This store is also reached after the first removal, as the README
    says.
- **Remover:**
  - It splices the links and the owner head/tail.
  - It runs `and byte [node+0xF],0xF0`.
  - It runs `dec byte [owner+0xE]` and `dec byte [02EBA481]` unconditionally. There is no occupancy test.
  - It never writes node `+0/+4/+8`.
- **"Kind2":**
  - The default arm takes every kind except 1 and 3. The README's call site sets kind = `1 + setne` (`00313C5E/61/63`),
    so it sends only 1 or 2.
  - The limits section excludes "all packet kinds". The label is accurate for this caller.
- **Independent equality reducer** (my own enumeration, not ASTRA's code):
  - All set partitions of the six identities: 203.
  - Under pu~nu, pa~na and nt≁nu there are 10 partitions × 2 flags = 20 coherent cases.
  - None of the 20 reaches both removals, and none breaks the live invariant without a removal.
  - Analytically: merging gives Bell(4)=15, less the Bell(3)=5 partitions with nt~U.
- **Controls:** each of the four is refused by the detector its label names:
  - `reverse-match-target`: coherent double-remove;
  - `ignore-creation-inequality`: creation invariant refuted;
  - `remover-writes-target`: footprint;
  - `native-write-outside-cache`: write envelope.
  They are synthetic source-record mutations, as disclosed.

## SWE2-AUDIT-SPEC limits

Static and conditional (Method A); no native or live run. The README's limits stand as written. These are not
established: live defaults, cache binding, lifetime and reuse, other callers or packet kinds, outside writers to the
counters, corrupted-list termination, and natural reachability of the broken-premise witness. The full UQ147 question stays
open.
