# SECTION-05 — encoded-ID registry and reusable query mechanism

Date: 2026-09-22. **Local production completed and validated; formal independent acceptance pending.**
Apply Update05 after Updates01–04 to `FFXII TZA(20260922-211246).zip`.
This is production of canonical database knowledge, not a new numbered EXP or a terminal L2 verdict.

## 1. Why this section

This package advances the complete registry-initialization -> request-class -> validator -> row/text/
inventory query -> reusable-output path. It consumes existing all-class validator evidence rather
than generating another duplicate validator campaign. Selected branches are still bounded: it is
not full inventory mutation, asset loading, live menu behavior or whole-world reconstruction.

The authoritative image is SHA-256:

`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.

The [manifest](original_body_manifest.json) pins19 selected bodies and9 data spans. Their original
bytes are verified before execution; historical Ghidra names are not semantic conclusions. Historical
contiguous extents were checked/decoded; no new Ghidra import or current population certificate is
claimed. The original executable and historical EXP-143 program/result are unchanged after tests.

## 2. Established registry behavior

`00309440` reads class at full-record+38, using prebiased base01EEBCF8. The full table begins
01EEBCC0: these are the same storage, not competing layouts. Its fifteen shipped classes are5..19,
so class=nibble+5. The instruction interpretation that says the nibble IS class is incorrect.

`0030B6A0` tests QWORD offsets00/18/28, loads only their lowDWORD, adds low32(state), and stores
zero-extended pointers08/20/30. Zero offsets leave old pointer lanes intact. A high-half-only offset
still passes the test. Native high/low-alias mappings and wrapping offsets discriminate these rules.

The function computes all15 exclusive prefix sums at+40. The source image has zeros there; their
prefix meaning is computed, not established by row0's coincidentally matching authored zero.
Counts sum6892 in the shipped registry. Overflow wraps32.

Rebase then zeroes exactly512 bytes from state+57C8 and ANDs128 bytes from state+59C8 withF8. That
reset uses the full64 state pointer, unlike the truncated resolved lanes. Repeating rebase recomputes
and resets again. Calling it merely to 'update pointers' can therefore change derived state.

The fixture executes original inventory mode0/1 handlers: packed available=low10-high6, total=low10;
bitset classes have different storage interpretation. Four shipped classes have a mutation handler
but no query handler. A zero query result is not proof their mutation path is inert.

## 3. Validator evidence is existing, and its scopes are distinct

EXP-143 already exercises all32 validator classes with its own fixtures. The previous current
contract's '31 of32 arms unexecuted' text was stale. This section independently parses retained
records, original32-entry jump targets, and the15 shipped mapper words. It does not run the old
Unicorn driver or certify original observer instrumentation from trace consistency alone.

The retained data contain246 traced probe records and4 additional untraced summary returns.
Its producer reports173 because it counts155 direct probes plus18 outer class1 case groups, omitting
nested/unplanted granularity. The original number/program/result are preserved; explanatory text now
calls it a mixed outer-container counter, not173 uniform experiments. Eight deliberately corrupted
record variants are rejected by the new independent reducer.

Class19 accepts E000..EFFE. Its upper rejection atEFFF is propagated. Signed comparisons are visible
in the original tail; rejection of -1 with nonnegative fixture ranges alone is not a universal
signed-versus-unsigned discriminator. Class13 sums4 descriptors; an absent descriptor contributes0.

## 4. Tag-selected input, partial success and interface-specific failure

The filler uses WORD+6 for1,5..11,13..18,30,31; DWORD+4 for2..4,19..29,32. Class12 immediately
returns-2 and reads neither. Its branch jumps to the epilogue rather than falling through into the
next arm. Thus an exhaustive16/16 input partition is false. The error and redispatch paths belong in
the interface specification, not outside the census.

Class1 writes its derived tag and redispatches WITHOUT converting the input. A WORD E000 does not
become a correct DWORD E000 merely because the derived class is19. The synthetic id-form case
therefore returns-2; a correctly formed direct DWORD class19 E000 returns-1.

Direct fill clears only name+18 at entry. Early refusal preserves the rest (except an earlier
class1 rewrite). Classes4/22/23 can succeed with only this name clear. Each wrapper writes its own
static request, calls fill, and zeroes all0x98 bytes only for a negative result, then returns its
record pointer either way. Successful calls preserve fields not assigned by that class.

Both static buffers, peer-buffer isolation, failure clearing and subsequent-success aliasing are
checked against sentinel bytes. The query is not a pure function of ID: old record contents and
current descriptor/inventory/text state are inputs. Reentrant or thread-safe use is not established.

## 5. Concrete false absence proofs corrected

**Byte54 has an original RMW writer.** Equipment row+7 bit1 replaces record+54 bit0 through
0031CA42 XOR /0031CA45 AND /0031CA47 memory XOR, preserving upper7bits. Ignoring RMW in a scanner
produced the incorrect no-writer conclusion. Both set/clear controls and category variation detect it.

**Class10 writes beyond the old tail boundary.** The loop0031CF60 writes12 DWORDs at+38+8*k,
ending+90..93. The four-byte gaps and+94..97 are preserved. It also writes empty-string pointers08/10
and zeroQWORDs20/28. A full0x98 comparison rejects a six-iteration mutant; prefix-only checking would
miss the omitted tail writes. The strided element meaning remains unresolved.

**+08 is not an unaccessed slot.** Action20, command21 and school24 write text pointers there;
class10 writes the static empty string. A historical consumer census failing to see a reader cannot
prove that a producer does not write the field.

Other exact producer corrections include action bits sourced from DWORD(row+0C), BYTE+30 width,
conditional action24/28 preservation, licence WORD+2A from row+0C, class32-only BYTE+36, status
low5bit RMW preservation, class15/30 first triple versus31 second triple, and the class11 lookup
index row+10 rather than row+3. The old broad table is replaced with a current bounded class table.

## 6. Availability, ownership and unusual inputs

Returned name/description pointers reference separate text storage. The fixture runs the actual
nested pointer reads and description resolver, but does not prove allocation lifetime across reload.
A missing text bank can produce successful nullname. Class2 can tolerate a decoded zero row base
on its name path; valid-count classes5/6 instead fault at row+0A/+12 when row base is zero.
Those faults are expected only inside isolated children, with address/PC receipts checked.

The general decoder uses a full64 base. Subsequent row-index arithmetic can truncate the high half;
a4GiB-offset fixture reaches the existing low-alias row. This is not a claim the game actually loads
that way. Pointer-field width and arithmetic width must be represented separately.

Key-item class13 selects three fixed intervals:8000..803F,8040..805F,8060..81FF. The six endpoints
select the expected rows. A synthetic nonzero fourth descriptor admits8200 through the validator,
but fill returns0 retaining old table-derived fields while assigning its sentinel/query outputs.
No initialized-game reachability is inferred from that experiment.

## 7. Native controls and mutation scope

Original filler/validator/wrappers/rebase plus reached application callees run in a private mapped
image at its preferred base. **There are zero application-callee substitutions.** Only the imported
memset IAT target is bridged to a host memset using the Microsoft x64 ABI; the original thunk remains.
All state/data are fixtures. No game startup, Windows loader, observer deployment or live IO occurs.

**200 named assertions pass; an identical second run passes.** Several assertions summarize loops
(all45 registry lanes,15 prefixes or28 equipment category inputs), so this is an assertion count,
not a count of unique game states or exhaustive branch coverage. All32 query classes have one baseline
snapshot; selected edge/output branches receive additional controls. Snapshot value differences
are not labeled complete write traces.

Seven deliberately incorrect private-image variants each fail exactly the intended assertion:

| Variant | Required discriminator |
|---|---|
| Remove equipment RMW | Set bit54 from row bit while preserving upper bits |
| Class10 only six iterations | Full0x98 sentinel comparison |
| Rebase using full64 addition | High state versus low32 pointer lanes |
| Failure clear only0x64 bytes | Complete wrapper erasure |
| Remove F8 reset mask | Preserve only intended high bits in128 bytes |
| Widen class19 by one | EFFF must reject |
| Clear description instead of name | Direct early-refusal footprint |

Only mutations impacted by this section run. The project's full campaign is not run or claimed.
The actual corrupted-state decoder controls are independently implemented, not merely a replay of a
producer's pass/fail booleans. Full old campaigns and formal independent acceptance remain separate.

## 8. Canonical propagation

Seven existing files change: the S04 contract, two existing mechanism/registry pages, EXP-143 prose,
two type-store files and the external handoff. One new mechanism page specifies the whole interface.
Only ItemClassDescriptor and EncodedIdQueryRecord rows change. Two type rows remain two; their43
combined field rows become55 because the false52-byte unwritten tail becomes explicit four-byte
strided elements/gaps. Unrelated rows remain byte-identical. Complete TSV files are included because
the user replaces files, not isolated rows.

The query type stays SIGNATURE RESOLVED; no semantic completion is awarded to unexplained strided
outputs. Corrected pages are REOPENED, with prior audit receipts retained as history. Their touched
colon-bearing provenance values are quoted for strict YAML without changing historical text.

No TEAM task, L2 cell, completion percentage, reconstruction source, historical raw capture or
producer program is modified. Peer acceptance must independently accept/narrow/reject these claims.
A successful packet is not accepted completion of the whole database or all S04 obligations.

## 9. Reproduction and deployment

An agent with Python3.10+, Linux x86-64 and GCC can run from this evidence directory:

```sh
python run_review.py --exe /absolute/path/FFXII_TZA.exe \
  --database '/absolute/path/FFXII TZA' --output /absolute/path/new-results-directory
```

The output directory must not already exist. Original EXE and unchanged EXP-143 inputs are required.
Nothing is downloaded. A wrong image, altered historical input, compiler warning, unexpected fault,
nonmatching repeat or wrong mutant failure rejects reproduction. Compiled files exist only in a
temporary build directory and are not distributed in the overlay.

No user commands are needed to apply the ZIP. Merge its FFXII TZA folder into the parent of the
existing database folder AFTER Update04. Back up matching files first; newer local edits need an
actual merge. The optional verify_overlay.py only checks hashes and never changes the target.

## 10. Remaining obligations and next work

Complete downstream class-specific meanings, wrapper caller/reentrancy contracts, string/resource
lifetime and real reachability of unusual fixture states are not closed here. These are explicit
remaining mechanisms/evidence needs, not inferred unused bytes. The next high-value architectural
section is the real resource ownership/retention/release chain, using the queue/widget knowledge
already established rather than repeating these query controls.

## Evidence index

- [Original ranges](original_body_manifest.json), [disassembly](original_disassembly.txt), [registry](shipped_registry.tsv)
- [Native source](native_controls.c), [driver](run_review.py), [retained reviewer](review_retained.py)
- [Summary](results/summary.json), [native baseline](results/native_baseline.json), [repeat](results/native_repeat.json)
- [Code variants](results/code_mutations.json), [body identity](results/body_verification.json)
- [Retained review](results/independent_retained_review.json), [corruptions](results/retained_negative_controls.json)
- [Class snapshots](class_baseline_records.tsv), [claim map](claim_matrix.tsv)
- [Before/after rows](canonical_row_changes.json), [canonical diff](canonical_changes.diff)
- [Source identities](source_inputs.json), [historical inputs](input_manifest.json)
- [Content validation](results/content_validation.json), [overlay controls](results/overlay_checker_controls.json)
- [Patch manifest](PATCH_MANIFEST.json), [read-only overlay check](verify_overlay.py)
