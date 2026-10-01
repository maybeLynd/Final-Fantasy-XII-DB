# SECTION-07 — original source movement and separate consumer refresh

Date: 2026-09-23. **Local production complete and validated; formal independent acceptance pending.**
Apply Update07 after Updates01–06 to the September22 21:12:46 database snapshot. This is an
incremental production overlay, not a new whole-project audit, EXP number, or L2 ruling.

## 1. Scope and value

SECTION-06 moved bytes/slot bindings in fixture code before running original repair. This section
executes the real mover `0036A2A0`, the original exact and adjacent selectors, and both explicit
compaction and the normal failed-allocation fallback. It then executes original demand delivery
and a clearly delimited original combined-refresh window. It connects previously scattered static
observations and corrects the inference that scheduling a child request proves a source moved.

Authoritative EXE SHA-256:
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.

The manifest pins **90 selected bodies**. All selected historical ranges are contiguous and match
their exported body extents. They are rehashed against the EXE; no fresh Ghidra/GN162 import or
instruction-coverage measurement is claimed. Historical names are labels, not semantic evidence.

## 2. What actually executes

The native child uses a private mapped copy of the original image, Microsoft x64 ABI, synthetic
low-address arena backing, synthetic handles/tickets, and default EFX payloads. The original
allocator, free, move, copy-wrapper, parser, ticket, refresh and dirty-delivery code runs.

| Boundary | Exact treatment and limit |
|---|---|
| `0017D2E0` diagnostic formatter | One application substitution: empty output and invocation counter. Normal fixture paths require no diagnostics. Formatting/error handling is not validated. |
| IAT `008C2A60` memset | Host MS-ABI adapter; original thunk remains. |
| IAT `008C2A68` memcpy | Host MS-ABI adapter only for non-overlapping inputs; also records mover-copy entry order. A separate overlapping case stops before copying. |
| IAT `008C2F70` strncpy | Bounded MS-ABI string-copy adapter used in inherited allocator/context scaffolding. |
| Combined driver | Only `0024D565..0024D6A9` is entered with equivalent stack/register setup. An explicit return barrier at `0024D6AA` skips the rest. Five pre-window service calls and subsequent rendering are not tested. |
| Arena backing/TEB | Synthetic maps and a minimal GS-backed stack-limit fixture; not a Windows loader or game observer. |
| Container nodes | Synthetic records for refresh traversal, not original-created heap containers. They are explicitly detached before context destruction. |
| Maintenance, VM and latch consumers | Selected whole bodies statically re-derived, not executed as complete sessions. |

No source mover, allocation/release, tree selection, ticket lookup, or tested repair is replaced by
a no-op. Default/empty specialized child paths are not evidence of every payload variant. The
combined-window boundary is reported separately, not hidden as a whole-function execution.

## 3. Findings and proof boundaries

### M07-1: selection and movement eligibility

`0036AAD0` matches the current free head's payload extent with a higher-address tree member, mask `0x04`
clear. Its remembered smaller candidate is not passed to the mover. `0036ABE0` may select the
physical successor of a hole when allocated and flags masked with6 equal2; that branch does not
require equal size. Native fixtures distinguish exact/nonadjacent, smaller/nonadjacent,
unequal/adjacent, inhibited, unlinked, and lower-address cases.

The tree pair now has an executed movement consumer: unlinking prevents selection, reinsertion
restores it. It remains an idempotent membership operation, not a nesting reference count or a
universal lock. `00369C60(...,0)` can report2 because the exact and adjacent passes each move once.

### M07-2: stable handle, intermediate publication, and allocation extent

The source length is `header+18`, the payload allocation extent. The mover publishes the destination
in the same slot at `0036A364`, frees the old source at `0036A397`, calls the original copy wrapper
at `0036A3A7`, claims the destination at `0036A3BB`, and restores metadata/tree/generation.

At copy entry the adapter independently observes the slot already naming the destination and the
old payload already released. After completion the handle value is stable, its header/generation
match, full tested capacity is preserved and usage accounting is unchanged. This does not prove
atomic publication, callback safety, or OS release of the backing map.

### M07-3: ordinary allocation is an invalidating operation

The pressure fixture fills the original arena, frees two individually0x800-sized holes separated
by the tagged0x400 source, and asks the original allocation front for0xC00 bytes. Its real fallback
moves the earlier source and succeeds. No diagnostic or optional callback fabricates movement.
Existing raw source pointers can therefore go stale during an ordinary allocation call.

### M07-4: movement latch and child-request pending bit are independent

Arena+62 is set by successful explicit/fallback compaction, read by00369CF0, and cleared by003697C0.
The prior field census missed both setting fronts. Original read/clear controls establish the latch;
00332660's conditional0041E500/00426950 calls and subsequent clear are separate static ordering.
A render record's bit27 means a coalesced child-start request, not necessarily a moved arena block.

### M07-5: original demand delivery has success/failure asymmetry

003E6AA0 replaces the packed five-bit index. Later requests overwrite, not append. Negative indices
and11 are rejected by003B3C00;0 returns1 without repair/start;1..10 refresh before attempting start.
The full00427DE0 fixture preserves pending when the binding is-1, but clears it after a bound call
regardless of stale generation, invalid index, or failed start. That is not automatic retry.

The tested failed start has no group/default mode and returns0, yet original refresh already repaired
the moved source's context/table/container. The test does not execute a successfully constructed
complex child effect. A successful zero-index result proves neither repair nor source lifetime.

### M07-6: additional combined refresh, not a universal dirty-only schedule

The combined original window at0024D565 follows02091108/+348 when its argument is0. Two containers
sharing one context both get their+390 base repaired, while the shared lookup shifts only once.
Nonzero argument and nonborrow context controls skip repair. The tested stale run origin survives.

The preceding and following services are excluded by a declared entry/exit boundary. This is not
whole-function0024D540 parity or live frame scheduling. The old same-frame/next-step claim is
withdrawn; source movement, demand delivery and combined-walk refresh are distinct operations.

### M07-7: actual overlapping-copy import boundary

A0x100 hole followed by a0x400 movable source reaches copy destination805307328, source805307648,
length1024. These ranges overlap. The separate process stops at import entry after recording the
slot/publication facts. It does not copy, retry, or claim successful final movement. Windows CRT
behavior needs exact dependency evidence; substituting host memmove would conceal the question.

## 4. Validation and falsification

**123/123 named assertions pass**, with an identical repeat. Counts are assertions over fixtures,
not123 distinct game states. Fourteen assertions belong to the combined-window fixture, which also
uses real allocation/setup/teardown around that window. One separate overlapping-copy boundary
observation is not counted as a successful payload-move test.

Ten deliberately incorrect private-image variants each fail exactly their intended assertion:

| Variant | Required discriminator |
|---|---|
| Skip original payload copy | Full source allocation must survive at destination. |
| Skip slot-generation synchronization | Slot/header generation must agree. |
| Test wrong inhibit mask | Inhibited member must stay put. |
| Skip context repair | Actual moved source must become the context base. |
| Admit index11 | Rejected index must not refresh. |
| Let index0 run refresh/start | Zero has its original success-without-work behavior. |
| Keep old packed index bits | Later request must replace earlier index. |
| Keep delivered pending bit | Bound stale request must retire its bit. |
| Skip combined container-base store | First container must have the new base. |
| Skip public movement-latch store | Completed move must set the latch. |

Only affected mutations run. EXE bytes on disk are hashed before/after. All compiled binaries live
in temporary directories and are not shipped. The source contains explicit fixture controls and
is portable to the tested Linux/GCC setting, not proof of Windows runtime deployment.

A development fixture initially left host-backed test containers in the destruction-owned global
list and faulted during cleanup. The final fixture explicitly detaches those test records before
context destruction, which is the correct boundary for a refresh-only container fixture. That
setup failure is not interpreted as an FF12 defect or hidden as successful container destruction.

## 5. Canonical changes and remaining obligations

Seven existing files change: two resource contracts, the Section06 mechanism, memory overview,
two type-store files, and the continuation handoff. One new mechanism page specifies the actual
producer-to-consumer interface. Only two type rows and four field rows are edited; no rows are
added/removed and unrelated TSV lines remain byte-identical. Type-wide readiness is not promoted.

The allocator overview is REOPENED for the new interpretation; historical audit receipts remain
history. Only touched malformed provenance scalars are quoted without changing their values.
Historical experiments, previous production evidence, TEAM, L2, global dashboards and reconstruction
remain untouched. Local validation is not independent peer acceptance.

Still required: external source owners and reload/pin discipline, actual deployed overlapping-copy
behavior, nonempty specialized consumer repairs, and whole scheduling/reentrancy where relevant.
Those are not waived by a stable handle or a locally passing fixture.

## 6. Reproduction and installation

On Linux x86-64 with Python3.10+ and GCC, from this evidence directory:

```sh
python run_review.py --exe /absolute/path/FFXII_TZA.exe --output /absolute/path/new-results
```

The authorized EXE is required; nothing is downloaded. Wrong image/body bytes, compiler diagnostics,
nonempty output, unexpected faults, changed repeats or a mutant failing the wrong assertion reject
the run. The native test needs only the standard library/GCC; content validation additionally uses
PyYAML. Existing external Tools links are identified, not asserted to be shipped or validated.

Apply Update07 after Updates01–06. Merge the ZIP's FFXII TZA folder into its existing parent,
back up matching files, and merge newer local edits rather than overwriting them blindly. The
optional verify_overlay.py is read-only; no commands are required for ordinary copy-and-merge.

## Evidence index

- [Native source](native_controls.c), [driver](run_review.py)
- [Original ranges](original_body_manifest.json), [original disassembly](original_disassembly.txt)
- [Summary](results/summary.json), [body verification](results/body_verification.json)
- [Baseline](results/native_baseline.json), [repeat](results/native_repeat.json), [mutations](results/code_mutations.json)
- [Overlap boundary](results/overlap_import_boundary.json), [claim map](claim_matrix.tsv)
- [Before/after rows](canonical_row_changes.json), [preimages](canonical_preimages.json), [input chain](source_inputs.json)
- [Canonical diff](canonical_changes.diff), [content checks](results/content_validation.json), [overlay controls](results/overlay_checker_controls.json)
- [Patch manifest](PATCH_MANIFEST.json), [read-only preflight](verify_overlay.py)
