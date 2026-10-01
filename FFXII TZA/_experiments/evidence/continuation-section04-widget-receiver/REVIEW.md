# SECTION-04 — widget receiver identity, construction and resource lifecycle

Date: 2026-09-22. **Local production complete; formal independent acceptance pending.**
Base: `FFXII TZA(20260922-211246).zip` plus Updates 01, 02 and 03, in order.
This is an edited-database production package, not another globally numbered EXP or an L2 ruling.

## 1. Established changes

**W04-1 — two apparent fields were not accesses to the declared widget.**
`003939D1` copies the message pointer from RDX to RBX; `003939D6` saves the consumer receiver
in RSI. `003939F7` therefore reads message+8, not `WidgetSingleton02AEE4C0`+8.
`003939FB xor ebx,ebx` clears RBX; `00393A23 lea edx,[rbx+0x15]` computes 21 and performs
no memory read. The old byte0008/dword0015 supports and their sound-for-presence guarantee are
removed from this type. This does not deny legitimate overlapping fields in the generic header.

**W04-2 — a real missing field and its producer/consumer chain.**
The asset widget is 0xD8 with handler `00394070`, published at `02AEE4C0`. The consumer is
0x1D0 with handler `003939B0`, published at `02AEE4C8`. The construction constants, handler
selection and publication stores independently distinguish their identities.
`00393FF0` writes the asset's +0xC8 and +0xD0 pointers. The old +0xC4 twelve-byte unobserved
span swallowed the +0xC8 QWORD. It is replaced by four unassigned bytes and the supported pointer.
The resource result's own +0x40 is not the asset widget's +0x40 header flags.

**W04-3 — publication, readiness, and cleanup are separate states.**
Own message1 publishes and starts requests after clearing the ready word. Own message16 ORs
bit0. The consumer loads the asset separately and checks that low bit before reading +0xD0.
Synthetic controls make the two receivers' same-offset bytes disagree to detect conflation.
Own message18 releases through +0xC8, conditionally releases and clears +0xD0, clears channel0
bit21, and clears the publication slot. It leaves +0xC8 and readiness bytes intact. That stale
pointer is not proof of a live resource. No receiver-equality guard protects the publication store;
the mismatched-pointer control is synthetic and not asserted reachable in normal play.

**W04-4 — raw initializer return is not the wrapper return.**
The contract incorrectly promised RAX=obj from `002465F0`. It does not restore RAX after the
last scheduler predicates. Tested paths return1 and0; `00245000` and `00244F50` separately restore
the object in RAX. The contract and mechanism now distinguish them.

**W04-5 — extent and zeroing phase.**
The creator's null test is at `0039448B`, size at `0039449F`, call at `003944A4`.
A 0x120 backing pool stride does not replace the requested 0xD8 logical extent. Sentinel-tail
controls verify the original initializer does not zero the rest of that backing slot.
Bulk zeroing happens before header writes and handler invocation: “zeroed” is not a guarantee
of all-zero storage after resource initialization or callback completion.

## 2. Original inputs and boundaries

Original EXE SHA-256:
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.

[Original manifest](original_body_manifest.json) pins 29 selected contiguous body ranges and three
data spans. [Complete selected disassembly](original_disassembly.txt) records exact bytes and
RIP-relative targets. Historical GZF extents were reused and completely decoded for these selected
bodies; no new Ghidra import or current-population completeness is claimed. The manifest labels
statically inspected and replaced bodies separately from reached original code.

[Source inputs](source_inputs.json) pins the base/update chain and relevant pre-edit source files.
The raw historical experiments, TEAM, L2 verdicts, global metric pages, reconstruction and the
original executable are not changed.

## 3. Native fixture: what really runs

The private image runs original widget initialization, allocation, owner-ticket, handler,
readiness, channel-bitset, selected resource-release, default and stack-cookie code.
All state is synthetic. No game process is launched; no actual assets are loaded or freed.

The exact application substitutions are:

| Boundary | Controlled behavior / explicit limit |
|---|---|
| `002493D0` | Checks resource-call arguments and returns the synthetic resource record; optionally advances the synthetic ticket's pending count. Does not implement IO. |
| `00249320` | Checks the second request and returns the synthetic loaded-block pointer, with the same explicit pending-count control. |
| `00248220` | Records root/receiver arguments; does not build or verify a real manager tree. |
| `00369860` | Records free arguments; does not implement the game's allocator. Original `003697F0` null guard remains. |
| `00181610` | Records cancellation of the selected synthetic resource entry; actual cancellation is not validated. |
| `002497B0` | Provides a bounded synthetic heap result for the separate consumer allocation; not an allocator proof. |
| `003946B0` | Stops the positive consumer build path at this call, records its three inputs, and returns to the test barrier. Subsequent child-tree code is not executed. |

The original imported-memset thunk remains but its IAT target is bridged to a host memset adapter.
All seven application replacements are installed only in the child process's private mapped image.
The original file is hash-checked before and after. No claim of zero scripted callees is made.

There are **65/65 original-instruction assertions**, with an identical repeat. They cover receiver
separation, explicit zeroing extent, retained pointer production, readiness states, cleanup
asymmetry, bitset constants, pooled allocation, the consumer factory and wrapper/raw returns.
Six deliberately incorrect private-image variants fail exactly their intended assertion:

| Variant | Discriminator |
|---|---|
| Read receiver instead of message at `003939F7` | Consumer's initial mode must come from message payload. |
| Remove the RBX zeroing instruction | Consumer state must be zero, not message-address residue. |
| OR wrong readiness bit | Ready message must set bit0. |
| Remove +0xD0 clearing | Teardown must clear the loaded-block pointer. |
| Clear the neighboring publication | Asset global must clear; consumer publication must survive. |
| Test the consumer's own ready field | Gate must depend on the separately loaded asset. |

Mutation testing is restricted to this changed section. No full project mutation campaign is run.

## 4. Receiver diagnostic: bounded instrument, not upstream repair

The supplied `Tools` scanner/producer source is absent. It is not modified, deployed or declared
fixed. [receiver_audit.py](receiver_audit.py) is a new, deliberately bounded checker over five
selected whole bodies. It uses explicit entry identities, verified body ends and the original
message jump table. It discards provenance at inconsistent joins, caller-volatile registers,
partial/32-bit overwrites, unknown pointee loads and unsupported dynamic indexes. Flag-only
instructions preserve pointer identity; LEA computes an address/value but is not recorded as a
memory access.

**14 concrete positive supports** reconcile, and the two false asset supports are absent.
The original LEA folds to constant21. **16 synthetic analyzer regressions pass** and **five
faulty analyzer variants are rejected**. These are instrument tests, not additional game behavior
cases. The analysis can miss valid fields; it does not certify whole-game completeness or all
possible alias states. Root identity assumptions are grounded separately in the creator/handler
chain, not magically inferred by the checker.

The dependency is pinned to the supplied Capstone **distribution 5.0.9**. That package internally
reports binding version **5.0.7** and API (5,0,1280); the execution receipt records both. No package
is downloaded or bundled into this overlay.

## 5. Canonical changes and acceptance

Five existing files change: `_types/types.tsv`, `_types/fields.tsv`, the widget object contract,
the constructor mechanism, and the external continuation handoff. The new concrete mechanism is
[the title asset singleton and its distinct consumer](../../../16-UI/Widget-Object-Model/the-title-asset-singleton-and-its-distinct-consumer.md).

The type store replacement affects **one type row**. Its exact size remains0xD8, but its current
readiness is conservatively SIGNATURE RESOLVED pending review of the repaired supports, not
continued acceptance of the old erroneous census. The field store replaces this type's **25
rows with 23**, removing the two false field hypotheses, retiling adjacent storage, adding +0xC8,
and distinguishing physical initialization from unproved meaning. All other type/field lines remain
byte-identical. Full TSV files are delivered because they are the files the user merges.

The previously AUDITED constructor page is REOPENED for these changes; its prior audit receipt
remains historical. The contract's old audit record likewise is not a new review of this production.
Only touched malformed provenance scalars are quoted for strict YAML. The new page is PARTIAL with
four explicit remaining obligations. No automatic peer acceptance, TEAM closure, L2 promotion,
global metric regeneration or reconstruction implementation is performed.

## 6. Reproduce

An agent with Python3.10+, Linux x86-64, GCC and the pinned Capstone distribution can run:

```sh
python run_review.py --exe /absolute/path/FFXII_TZA.exe --output /absolute/path/new-empty-results
```

This requires the original authorized EXE; no game image, dependencies or binaries are shipped.
The driver rejects a different EXE, altered selected range, unexpected compiler diagnostics,
nonempty output, failed assertions or a mutant failing the wrong check. The user need not run
commands to install the ordinary changed-files overlay.

The reproduction was also run from a separate extraction of the delivered overlay; native and
receiver results matched the packaged baseline. That verifies package portability to the tested
Linux setup, not Windows live-runtime behavior.

## 7. Remaining work / next section

Independent peer acceptance remains pending. Real resource-service timing/cancellation, full manager
and child-tree behavior, other widget declarations affected by the missing producer, and remaining
field/lifetime obligations are not closed by this local fixture.

Next independent production: encoded-ID validator/query contracts, including the still incorrect
class12 fallthrough/16:16 partition and propagation of the already established class19 EFFE upper
bound. Do not repeat completed widget/reward/queue controls merely to raise test counts.

## Evidence index

- [Native source](native_controls.c), [driver](run_review.py), [scope](scope.json)
- [Run summary](results/summary.json), [original body verification](results/body_verification.json)
- [Native assertions](results/native_baseline.json), [repeat](results/native_repeat.json), [code mutations](results/code_mutations.json)
- [Receiver analysis](results/receiver_audit.json), [access rows](results/receiver_accesses.tsv), [concrete supports](results/concrete_support_checks.json)
- [Analyzer regression](results/auditor_regression.json), [analyzer mutants](results/auditor_mutations.json)
- [Exact before/after rows](canonical_row_changes.json), [canonical diff](canonical_changes.diff)
- [Content checks](results/content_validation.json), [overlay checks](results/overlay_checker_controls.json)
- [Patch manifest](PATCH_MANIFEST.json), [read-only conflict checker](verify_overlay.py)
