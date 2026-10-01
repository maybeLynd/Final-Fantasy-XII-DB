# SECTION-10 — nonempty PRF registration and specialized relocation

Date:2026-09-23. **Local production complete and validated; formal independent acceptance pending.**
Apply Update10 AFTER Updates01–09 to `FFXII TZA(20260922-211246).zip`.
This is an edited-database overlay, not a numbered EXP, accepted L2 ruling or live game observation.

## 1. Why this section

Section09 deliberately stopped at plain-header registration. This section supplies nonempty PRF0/1
containers, follows the full original registration function, and reaches an actual specialized
A00 subtype0 relocation path rather than the earlier default-subtype no-op. It then moves the
allocation with the original compactor, repairs the nested fields with original code, and disposes
of the context and backing according to their distinct owners.

## 2. Provenance and execution limits

Authorized EXE SHA-256:
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.

[Original manifest](original_body_manifest.json) pins114 selected contiguous historical function
ranges and3 dispatch/signature data spans. Selected bytes are verified against the original image.
[Disassembly](original_disassembly.txt) covers those complete ranges;307 static selected transfers
are in [direct-call supports](direct_call_supports.tsv). These counts are neither dynamic traversal
counts nor instruction/branch coverage. No new Ghidra/current-GN162 import is claimed.

The child maps a private original PE image, uses GCC's Microsoft x64 ABI, and supplies synthetic
arenas, resource-bank pages, source bytes, metadata, configuration strings and ticket slots.

| Boundary | Exact treatment |
|---|---|
| `0017D2E0` diagnostic formatter | Empty destination and invocation counter, inherited from the arena fixture. Diagnostic formatting is not validated. |
| IAT `008C2A60` memset | Host MS-ABI adapter, original thunk retained. |
| IAT `008C2A68` memcpy | Host MS-ABI adapter, NONOVERLAPPING inputs only; overlap explicitly rejects the fixture. |
| IAT `008C2F70` strncpy | Bounded MS-ABI copy; original normalizer and matching logic execute. |
| GS-backed stack limit | Minimal synthetic stack-probe environment, not a Windows loader or observer. |
| Optional configuration | A valid table pointer contains a string that makes original `001D6EC0`/`001A09E0` return NULL. `.cm` entry lookup, strstr/scanf and priority override do not run. |
| Authored inputs | Constructed bounded PRF/EFX fixtures, not captured or exhaustively censused game assets. |

No parser, specialized relocation, registration, ticket allocation, compactor, refresh, or tested
teardown is replaced with a no-op. The original code takes selected real branches. No actual IO,
rendering, complete child effects, Windows overlap-copy result or game-session health is inferred.

## 3. Findings

### N10-1: table-relative discovery and distinct outputs

Magic `0x50524640` has bytes `@FRP`; prior handoffs call this PRF. `00409780` searches the root
before children. Version0 uses DWORD offsets at+30, version1 at+40 and skips zero entries. The
fixed table base is added, not the location of the individual offset slot. A sparse second slot
keeps authored index1. Unsupported versions yield no match.

A matching PRF root has offset0 but index-1; matching a plain root sets both0. Therefore a negative
index does not prove the offset lookup failed. `00409A60` zero-pads root and child names IN the
source before copying or borrowing. Query normalization uses shared scratch `02B62E20`. These
operations assume readable terminated names and valid offsets/counts; malformed-asset safety and
thread-safe/reentrant scratch use are not proven.

### N10-2: the FEF discovery offset is not the parser offset

`00409FE0` finds a named `@FEF` section and tests only whether the returned offset is -1. It then
uses the last five root-name bytes to index a configuration-string table. Valid name formatting,
readability and indexing are caller obligations in this branch, not independently validated here.
The current file selector flows through `002E9770` -> `002E98F0` -> `002DF960`. Its size is rounded
up to64 for the tested positive values; the DWORD at `source+roundedSize-4` supplies the effect
parser offset at `0040A16F`.

The fixtures make search offset0x100 disagree with parser offset0x300 or0x700. Both select the
metadata-designated payload. Replacing the load with constant0x100 fails the expected assertion.
The selected source representation may be a tagged external handle or the entry-owned copy.

### N10-3: specialization writes the selected backing

Type3 creation runs `003B38B0` and the original parser. A nonempty A00 record uses lookup index1
and subtype0; `003A9A70` writes identity fields, then original `005004C0` dispatches to `00500470`.
Its four `004304F0` calls adjust eight nonzero DWORD fields at record+00/+04, +10/+14, +20/+24,
+30/+34 using the real decoder/encoder. The A00 table is context+850, distinct from800's+848.

With a retained tagged source, those writes change external backing. With mode0, they change the
owned copy while the original payload offsets remain unchanged. Name padding was already mutated
in the input in both modes. A returned bank index does not imply immutable input.

### N10-4: bank admission, ticket creation and parsing are separate successes

A missing same-name `@FEF` leaves a valid bank entry without a ticket. Exhausting the ticket free
list leaves a valid bank entry with ticket0. An invalid effect signature can leave an allocated
context and valid ticket but no parsed lookup record. Cleanup of these selected states is tested.
These are synthetic controls, not reported normal-game bugs or proof of arbitrary failure recovery.
Optional priority/config parsing remains outside this section.

### N10-5: reuse is not reinitialization or re-registration

A same-key registration returns the original bank entry, preserves its ticket and already-fixed
fields, and allocates no second context. After disposal, explicitly registering the same mutated
external source again runs fixup again and adds the record base again modulo32 in the tested fields.
Disposal does not reconstruct the original relative offsets. This is a caller reuse/fresh-data
precondition, not a claim that shipped callers necessarily perform this unsafe synthetic sequence.

### N10-6: original relocation reaches nested specialized fields

The original compactor moves a registered nonempty source into a separated matching hole. After
movement the context base, lookup and nested encoded words still name the old address. Original
`003B3480` -> `0024D970` -> `003A9BA0` invokes `005004C0` at the new record before publishing the
updated lookup. It repairs the context and the eight tested encoded fields. The repeat sees an
unchanged base and does not apply delta twice. Record index/subtype remain intact.

The borrowed run origin stays stale. Actual context disposal frees its tables; the external backing
is still allocated until the separate owner release. This closes one nonempty subtype path, not all
specialized record families, child rendering or cross-thread scheduling.

### N10-7: NULL has arithmetic causes as well as explicit guards

`004096C0` explicitly guards null entry and offset-1, but those are not the only NULL outcomes.
Unsupported mode+offset0 returns0. A valid cached base0xFFFFFFF0 plus offset0x10 also returns0 after
32-bit wrapping. The current contract's 'everything else returns a pointer' claim was false.
The formula remains `sext32(low32(base)+u32(offset))`, without a base-validity check.

## 4. Validation and falsification

**159/159 named assertions pass**, with an identical separate-process repeat. This is an assertion
count across bounded fixtures, not159 unique mechanisms or exhaustive branches. The eight affected
private-image variants each fail precisely the required discriminator:

| Variant | Expected rejection |
|---|---|
| PRF1 return uses+30 instead of+40 | `prf1_effect_section_offset` |
| Skip version0 child padding | `prf0_normalizes_child_padding` |
| Use search offset instead of footer-derived offset | `registration0_ticket_uses_metadata_not_section_offset` |
| Skip specialized first pointer pair | `registration0_specialized_nonzero_relocations` |
| Skip context destruction | `registration0_context_reclaimed` |
| Ignore existing bank match | `registration0_same_key_returns_existing_index` |
| Skip nested specialized refresh | `refresh_relocates_specialized_first_word` |
| Skip ticket publication | `registration0_ticket_generation` |

Only impacted mutations run. The original executable is unchanged; variants patch private child
memory only. The driver rejects compiler diagnostics, wrong images/ranges, unexpected faults,
nonidentical repeats or a variant failing the wrong assertion. Binaries exist only temporarily.

A development assertion initially used context+848 for the A00 lookup. Checking the original global
bindings showed the actual table at+850; the fixture was corrected before validation. This was a
fixture expectation error, not an FF12 fault, and is recorded rather than hidden as a game finding.

## 5. Canonical production and remaining boundaries

Six existing Markdown files change: section-addressing contract and mechanism, resource-input
ownership contract, EFX-rebase contract, owner lifetime mechanism and external handoff. One new
mechanism explains this complete bounded path. No TSV, original experiment, raw capture, TEAM,
L2 verdict, global completion score, reconstruction source or prior section evidence is changed.
The former AUDITED section page is REOPENED; its old audit counters remain historical. Touched
colon-bearing provenance scalars are quoted without changing their values. Local validation is
not independent peer acceptance or whole-system L2 completion.

Next: a concrete held-state1 dispatcher/outer terminal-error recovery caller, and caller policy
for fresh versus already-relocated input. Other subtypes and optional configuration should be
investigated when their actual consumers require them, not as blind enumeration. Real IO scheduling,
callback reuse, malformed-asset safety and the Windows overlap-copy boundary remain separately open.

## 6. Reproduce and install

From this evidence directory on Linux x86-64 with Python3.10+ and GCC:

```sh
python run_review.py --exe /absolute/path/FFXII_TZA.exe --output /absolute/path/new-results
```

The output directory must not exist. No dependencies are downloaded. This is not a Windows or live
game experiment. Optional document/link validation uses PyYAML; installation requires no commands.
Apply AFTER Updates01–09. Merge the ZIP's FFXII TZA folder into its existing parent; never delete the
whole database or nest the folder inside itself. Back up changed files; newer local versions require
a merge, not blind replacement. `verify_overlay.py` is an optional read-only preflight.

## Evidence index

- [Manifest](original_body_manifest.json), [disassembly](original_disassembly.txt), [static transfers](direct_call_supports.tsv)
- [Native source](native_controls.c), [driver](run_review.py), [mutants](variant_plan.json)
- [Summary](results/summary.json), [baseline](results/native_baseline.json), [repeat](results/native_repeat.json), [mutations](results/code_mutations.json)
- [Claims](claim_matrix.tsv), [preimages](canonical_preimages.json), [diff](canonical_changes.diff), [input chain](source_inputs.json)
- [Content checks](results/content_validation.json), [overlay controls](results/overlay_checker_controls.json), [unchanged files](results/unchanged_files.json)
- [Patch manifest](PATCH_MANIFEST.json), [read-only checker](verify_overlay.py)
