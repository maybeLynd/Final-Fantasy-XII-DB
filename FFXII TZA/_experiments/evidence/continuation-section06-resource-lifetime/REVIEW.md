# SECTION-06 — resource ownership, retention, refresh and disposal

Date: 2026-09-22. **Local production completed and validated; formal independent acceptance pending.**
Base: `FFXII TZA(20260922-211246).zip` plus Updates01–05 in order. This is an edited-database
overlay, not another whole-project audit, numbered experiment or L2 ruling.

## 1. Value and established boundary

This section connects entry setup -> context creation/parser borrowing -> source retention/refresh
-> consumer cleanup -> entry disposal -> actual native allocation release. The original caller,
parser, default payload registration, ticket and indexed-bank helpers, context/instance cleanup,
buffer operations and allocator execute together against controlled synthetic state.

The key distinction is **layer-relative ownership**. A resource entry may own a backing copy while
its effect context borrows interior pointers from it. That context still owns its lookup tables.
A ticket, cache, current-context global and arena membership bit are not interchangeable ownership
handles. Neither a nonzero pointer nor an unchanged address proves the resource remains live.

## 2. Inputs and exactly what is substituted

Original EXE SHA-256:
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.

[Original manifest](original_body_manifest.json) pins **85 selected function bodies**. The historical
Ghidra range exports were reused and decoded; no fresh Ghidra import/current-GN162 completeness is
claimed. Hash agreement establishes byte identity, not complete path coverage. The entire file is
hash-checked before and after execution. No game executable bytes are distributed with this overlay.

The native child maps a private image at its preferred address. It uses the Microsoft x64 ABI,
real arena initialization/allocation/free and synthetic arena backing blocks. This is not OS-level
freeing of those backing maps. The following substitutions/controls are explicit:

| Boundary | Fixture treatment |
|---|---|
| Application `0017D2E0` diagnostic formatter | Writes an empty destination string, records the invocation and returns0. Normal test paths assert no diagnostics after arena setup. Formatting/error rendering are not validated. |
| IAT `008C2A60` memset | Host MS-ABI adapter; original thunk preserved. |
| IAT `008C2A68` memcpy | Host MS-ABI adapter; non-overlapping tested inputs. |
| IAT `008C2F70` strncpy | Bounded MS-ABI implementation used by original name matcher. |
| TEB stack-limit read | Minimal synthetic GS-backed environment for the original stack probe; not a Windows observer or loader. |
| Arenas, slot tables, bank pages and child data | Explicit synthetic initialized state. The code acting on them is original. |
| Movement | Fixture copies source and changes its tagged slot; the original mover is NOT run. The original refresh driver and selected walkers ARE run. |

No resource allocator, destructor, release, cancellation, parser, ticket or bank search/removal is
scripted as a no-op. Some called families see empty children or subtype255 default branches; the
full specialized callees are not certified by the executed default case. The existing-entry branch
of acquisition is executed; the full new-entry/PRF branch is static-only here. The seven service
substitutions used in Update04 are NOT imported into this fixture.

## 3. Concrete findings

**O06-1 — the parser borrows mutable payload, not lookup storage.** The800/A00 ownership bit
selects original input versus separately allocated copy. Original registration writes index/subtype
metadata into the selected payload. The lookup allocations remain owned by the context in both
modes. Unaligned0x2B3 copy rounds down to0x2B0 while the borrowed input still contains all bytes.
This is not a proof that arbitrary malformed lengths cannot overrun a destination: chunk lookahead,
field writes, indices and signed sizes require valid preconditions.

**O06-2 — bulk representation and borrowing are independent.** Byte3 mask1 selects the bulk
run teardown. Only there does byte2 mask4 suppress freeing run+870/+878. Run pointers are cleared
either way, while tables are always released. Nonbulk individual-entry cleanup ignores that borrow
exception. The selector globals remain rebound to an already freed context; tests distinguish that
from the lifetime of a separate surviving context and its source.

**O06-3 — entry-owned backing can be borrowed by an inner context.** Entry mode0 allocates and
copies source; mode1 retains external storage. Type3 uses flags0x0C either way. Exact matched disposal
clears selected render references, cancels the context ticket, tears down the entry and removes
the bank slot. Owned backing is freed DURING per-row teardown, after context destruction and
before bank-slot removal. The mode1 external allocation remains live. This confirms the real release chain previously recorded only statically.

**O06-4 — tickets and instances are generation/owner-selective.** Stale full tickets leave the
slot and context untouched. Cancellation removes only instances whose owner pointer matches,
preserving an interleaved unrelated instance and repairing next/previous links. The two associated
deferred payloads queue once despite the two instance-walk calls. Secondary-ticket recycling clears
its owner relationship without treating static slot memory as a heap allocation. The full deferred
queue and complex nested children are not exercised.

**O06-5 — survival is selective, not a universal clear.** Entry reset preserves cache+38. A
no-match source deletion does not sweep render references. `00409D60` matches one side of the D8/E0
and F0/F8 pairs, whereas `00427B00` matches the other. Both differences are discriminated by fixtures
with contradictory values rather than all-zero inputs. These sites do not enumerate every consumer.

**O06-6 — membership is not reference counting or reclamation.** Tagged acquire/remove and
release/add preserve allocated storage. Two acquires followed by one release already reinsert;
generation mismatch refuses the membership operation. Actual tagged destruction removes the slot
owner and the allocation. Do not call the tree pair two frees, and do not equate raw membership
no-ops with raw source free, which is real `003697F0`.

**O06-7 — equal-key reuse and source movement are distinct.** The original tag/name lookup
returns an existing entry unchanged despite a different incoming source size/payload. Direct buffer
resize instead replaces and releases its backing, copies old CAPACITY rather than only used bytes,
and does not fix outside pointers. Re-parsing one existing context similarly overwrites its copy
pointer without releasing the old run; that synthetic use is NOT asserted to be a shipped leak.

**O06-8 — there is a separate refresh path, but it does not rewrite every field.** After a
SIMULATED tagged-slot move, original `003B3480`/`0024D970` update the full source base and tested
lookup pointer. An unchanged repeat does not double-apply. The old run origin remains stale.
This refutes “every derived pointer is repaired,” but does not prove a use-after-free in FF12: the
borrowed destructor does not free that origin. Real mover scheduling/reentrancy remains unproved.

**O06-9 — the0x1C buffer extent was based on an incomplete access census.** Two actual MOVAPS
stores in `0051EEB0` transfer0x20 bytes. Parent+2C is the opaque copied tail, not a separately
established control member. The local temporary leaves its padding uninitialized, so the knowledge
record asserts transferred storage and no stable value/meaning. Per-row teardown is real00409730,
contradicting the prior dtor “none per row” conclusion. The bank slot itself is not individually freed.

## 4. Native validation and falsification

**171/171 named original-instruction assertions pass**, with an identical second run.
The ten targeted private-image variants fail exactly the intended discriminator:

| Variant | Required rejecting assertion |
|---|---|
| Borrow tests wrong mask | Borrow must retain the exact input-run address. |
| Skip owned-run free | Owned copied run must no longer be allocated. |
| Skip table free | Context arena usage must return to zero. |
| Copy unrounded length | Three unaligned tail bytes must not be copied. |
| Ignore ticket-generation comparison | Stale ID must preserve the slot. |
| Compare wrong side of render pair | Matched source clearing must remove the intended pair. |
| Skip old-buffer release | Resize must free the old allocation. |
| Skip context cancellation | Entry deletion must reclaim its associated context. |
| Ignore tree-membership removal | Acquire must actually unlink the member. |
| Skip context rebase | New source base must be published through original repair. |

Only impacted mutations run. This is not a full project mutation campaign. Repeated assertion
counts are not separate experiments and selected-body hashes are not instruction-coverage receipts.

## 5. Canonical production and preserved uncertainty

Seven existing files change: the ownership/tree/rebase contracts, the lifetime mechanism, the two
type-store files and the external continuation handoff. One new mechanism page explains the whole
bounded lifetime. Three type rows and21 existing field rows change; one parent gap is removed and
one opaque child tail is added. Combined target field-row count remains41. All unrelated TSV lines
are byte-identical; the complete TSV files are shipped so ordinary file replacement works.

Only the touched malformed provenance scalar is quoted for strict YAML without changing its text.
Historical audit counters are not reset or silently treated as new acceptance. Type readiness is
not promoted. The new page remains PARTIAL. Historical input scripts/results, TEAM, L2 verdicts,
completion dashboards, reconstruction source, game image and prior section evidence are untouched.
Formal peer acceptance remains pending; completed local production is not database certification.

The remaining high-value boundary is the ORIGINAL movement producer and consumer refresh schedule,
then external-owner release callers and nonempty specialized children. The query's borrowed text
pointers are not automatically assigned this resource owner merely because both contain pointers.

## 6. Reproduce and apply

From this evidence directory, on Linux x86-64 with Python3.10+ and GCC:

```sh
python run_review.py --exe /absolute/path/FFXII_TZA.exe --output /absolute/path/new-results
```

No dependencies are downloaded. The driver rejects a wrong image/range, compiler diagnostics,
nonempty output, unexpected fault, failed assertion, changed repeat or mutant failing the wrong
check. Binaries live in a temporary directory, not in this ZIP. A live Windows/game session is not
substituted by this fixture. An additional content checker verifies the delivered canonical records and database-local links.
Its PyYAML dependency is used only for content validation, not the native reproduction. An inherited
link to `Tools/analysis-kit/gfz-scripts/falsify_efx_rebase.py` lies outside this database export and
is recorded as unavailable, not silently declared validated.

Apply the changed-files overlay AFTER Updates01–05. Merge its `FFXII TZA` into the parent of the
existing folder; do not nest/delete/replace the entire directory. Back up touched files. A newer
local edit is a merge conflict, not permission to overwrite it. `verify_overlay.py --target <DB>`
is an optional read-only preflight; no user command is required for ordinary copy-and-merge.

## Evidence index

- [Original ranges](original_body_manifest.json), [disassembly](original_disassembly.txt)
- [Native source](native_controls.c), [reproduction driver](run_review.py)
- [Baseline](results/native_baseline.json), [repeat](results/native_repeat.json), [variants](results/code_mutations.json)
- [Summary](results/summary.json), [claim map](claim_matrix.tsv)
- [Exact row changes](canonical_row_changes.json), [canonical preimages](canonical_preimages.json)
- [Content validation](results/content_validation.json), [overlay controls](results/overlay_checker_controls.json)
- [Canonical diff](canonical_changes.diff), [patch manifest](PATCH_MANIFEST.json), [input chain](source_inputs.json)
