# SECTION-03 — retained reward bindings and original EXP/LP consumers

Date: 2026-09-22. Status: **production completed and locally validated; formal peer acceptance pending**.
This is actual canonical-database production, not a new experiment number or a terminal L2 ruling.
Apply Update03 after Update02 and Update01 to the September22 21:12:46 uploaded snapshot.

## 1. Scope and provenance

The original executable is pinned to SHA-256:

`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.

The package independently consumes retained EXP-081 bindings, re-derives the original EXP and LP
consumer rules, and propagates the consequences into the two contracts and three mechanism pages.
Selected installer, caller, gil-setter and notifier instructions are separately checked statically.
The original historical experiment programs, raw records and earlier review receipts are unchanged.
No new live FF12 process was started. No current Ghidra import, full old Unicorn campaign,
whole defeat-orchestrator execution, or formal peer/terminal acceptance is claimed.

`original_body_manifest.json` identifies **24** selected original ranges and two data spans.
Nineteen ranges are the existing EXP-090 reward/gate closure. The additional five are the installer,
address decoder, defeat caller, gil setter and gil notifier, inspected statically, not all executed
by this package. Body-hash agreement establishes byte identity, not semantic correctness of every
instruction or current Ghidra population completeness.

`input_manifest.json` pins fifteen unchanged input files. The original observer and past checkers
are inputs, not automatically accepted proof; the new byte reduction is independently implemented.

## 2. Retained observations — what is and is not captured

The independent reducer verifies **88 spans in four samples** from historical PID 30640:
two completed-load-popup samples and two field samples. Every span's bytes, declared size and
SHA-256 reconcile. The reducer directly checks read addresses, matching before/after binding
bytes, stats slices, enemy definition-row offsets and selectors. It does not simply trust the old
observer's stability booleans. The original 26-file restore and process-exit records are consistent;
these are retained receipts, not a new restoration or new health check.

At the completed-load popup both reward registry slots are zero and the capture has no units
satisfying occupied + actor + stats bindings. In each field sample the active slots are 0, 4, 5 and
7. The kind-zero unit's reward pointers are zero; the three kind-one units have nonzero pairs.

| Slot | Base selector / pointer | Per-level selector / pointer |
|---|---|---|
| 4 | `6 / 67483D90` | `4 / 67484050` |
| 5 | `5 / 67483D58` | `3 / 67484018` |
| 7 | `0 / 67483C40` | `0 / 67483F70` |

Registry words are `67483C20` (base, from slot `02EBF148`) and `67483F50` (per-level, from
`02EBF140`). The retained relocation word is zero. Kind-one working stats match their primary
keep-entry slices at `+0x80`; they are not the authored definition rows pointed to at unit `+0xE60`.

**Neither reward header nor required reward-row prefix was captured anywhere in these spans.**
The index-zero pointers happen to be descriptor+0x20, and address/selector differences fit stride
0x38. This is **conditional consistency with an affine row model**, not an actual read of header
count/stride/encoded base. It does not recover coefficient values, prove continuous lifetime,
show the installer running, observe a death, or establish a displayed award.

Stable sequential brackets cannot exclude an intermediate rebind to the same value. Zero registry
slots at a load popup do not prove a reached NULL-row defeat path. Those limitations are explicit
in the contract rather than silently converted into semantic completion.

### Independent retained-record controls

Ten deliberately corrupted variants are rejected: changed reward pointer across the bracket;
wrong registry address; wrong stats address; altered stats bytes with an updated digest;
misaligned authored-definition pointer; empty field-sample population; duplicate sample identity;
false observer stability flag; fabricated purported reward bytes; and inconsistent restore records.
Hash-consistent content mutations test the semantics of the reducer, not merely hash rejection.

Separately, the old `retained-reward-bindings/check.py --mutations` output exactly matches its
preserved `observation.json`, including its four historical negative controls. This is a replay
of that checker, not ten-plus-four new independent game experiments.

## 3. Consumer corrections established by original-code execution

### R03-1: NULL does not bypass EXP division

Both computers admit a NULL recipient. EXP still chooses its mode. Shared-mode EXP counts exactly
four original roster lookups and divides by the positive count. With raw EXP 19 and two members,
NULL returns 9, not 19. A doubled nonnull recipient gets 18 while NULL remains 9. Designated-mode
NULL returns 19. NULL skips recipient checks, designation equality and effect modifiers; it does
not force single-recipient mode or bypass subject validation.

The caller zeroes ECX at `003124BC/003124C6` for the two computers and applies caps plus a separate
field-flag EXP suppression before `0028FB80`. The earlier "NULL means undivided screen total"
conclusion is false. The new proof concerns original call inputs and computed returns, not a fresh
rendered number or complete progression transaction.

### R03-2: EXP and LP do not have the same gate

EXP requires an owning BattleUnit for a nonnull kind-zero recipient. LP never performs that lookup.
The synthetic orphan-stats control gets EXP 0 and LP 19. LP has its own signed-byte global gate
before all pointer dereferences and admits recipient IDs 0..6, 0x1A, or >=0x28. It has no EXP
roster divisor or designated-mode restriction. Shared mask equality is not proof of shared code:
editing the action gate will not automatically patch these independent tests.

### R03-3: recipient admission is not divisor admission

Kind-zero ID 0x1A is admitted as an EXP/LP recipient but excluded from the EXP divisor. An ordinary
byte selector cannot match a kind-one stats identity. Nevertheless, 0xFF has a 0xFFFF sentinel
comparison; with descriptor count 256 and a matching synthetic stats identity the original lookup
can return and count it. This refutes the universal "only kind zero can ever count" wording while
preserving ordinary kind-one exclusion. Normal-game reachability of that synthetic sentinel state
is not established. Repeated lookup slots need not be distinct records in synthetic states.

### R03-4: arithmetic and absent-row paths are independent facts

EXP loads DWORD coefficients at row+0x34, wraps at 32-bit width, then uses signed truncating
division. LP loads unsigned BYTE coefficients at +0x2F: 0xFE means 254. Both read actual level and
baseline bytes, not a hardcoded baseline1. Negative synthetic inputs, wrap, second-bank effects,
zero-after-double priority, and no-row paths are tested explicitly.

A zero shared roster returns EXP 0 before reward-row reads. When formula reads are reached,
NULL multiplier or base rows fault at address0x34 (EXP) or0x2F (LP). Those fault checks execute in
isolated children; they are not crashes induced in FF12. Earlier valid gates can avoid the access.
The full synthetic data region is unchanged after normal consumer calls.

### R03-5: row-production checks are separate from retained row observations

The kind-one installer reads selectors from enemy row+0x22/+0x24. Each descriptor supplies encoded
base at+0x0C and stride u16 at+8. `0020E600` adds the zero-extended encoded value to the relocation
base. The stores at `0023A9A5/0023A9F4` use a 32-bit multiply/add before storing a zero-extended
QWORD pointer. Descriptor absence, decoded zero and arithmetic wrap-to-zero must not be conflated.
This is static original-code verification, not proof that the sampled session used specific header
contents. Installation is not transactional; earlier reset/rekey effects are documented in Update01.

## 4. Caller gil correction, statically derived only

The defeat caller floors `old + award` to zero before calling `00254EE0`, then sends
`requested - old` to `00469E80`. The setter meters `requested - current` before applying its own
upper cap. With the same old balance at both reads, the arithmetic differences agree; the upper
cap does not by itself make them different. Both can exceed the actual stored gain.

For old 99,999,995 and award 10: requested 100,000,005; both differences 10; stored gain 4.
For old 5 and award -10: requested 0; the setter meters a spend 5 and the notifier receives -5.
`00469E80` posts only positive deltas; it is not a second persistent ledger.

The notifier clears six QWORDs beginning at current RSP+0x20. Its DWORD delta at RSP+0x30 is
**payload+0x10**, not payload+0x30. Prior prose counted seven QWORDs and confused the stack-frame
base with the payload pointer. Whole-original-body disassembly establishes the corrected count,
offset and positive-only branch. No subscriber census or whole gil execution is newly performed.

The equal-difference reasoning assumes no intervening balance change between the relevant reads;
it is not a global non-reentrancy/concurrency proof. Other inherited defeat/growth/event/drop
findings are retained as existing work and not self-recertified by this section.

## 5. Native fixture and falsification

The reproduction runs full original reward bodies and their original gate callees from a private
mapped image at the preferred base, using GCC's Microsoft x64 ABI. The data is synthetic.
**Zero application callees are scripted or stubbed.** Not every instruction of the selected helper
bodies is reached. No Windows import, game startup or observer deployment is attempted.

**71/71 controls pass**, and an identical second baseline confirms repeatability. The retained
case JSON names every control. Six private-image variants fail their intended assertion:

| Variant | Intended discriminator |
|---|---|
| Skip signed EXP division | NULL EXP with two passing roster slots |
| Sign-extend LP coefficient | Unsigned 0xFE row byte |
| Widen EXP doubling mask | Unrelated bit0 must not double EXP |
| Walk only three roster slots | Four-slot NULL EXP count |
| Ignore missing EXP owner | Orphan recipient EXP must be rejected |
| Ignore global LP gate | Gate must reject before award/pointer use |

These mutants alter only the child process's private mapped bytes. The original EXE and all pinned
historical inputs are verified unchanged before and after the run. This is impacted mutation work;
the project's full mutation campaign is neither run nor claimed.

## 6. Canonical changes and acceptance

Eight existing files change: two reward contracts, three reward mechanism pages, EXP-081 and
EXP-090 interpretation notes, and the external continuation handoff. No types/fields.tsv, TEAM,
L2 verdict, global completion dashboard, reconstructed implementation, or historical raw output
is modified. There are no file deletions.

The two mechanism pages with demonstrably false current claims are marked REOPENED rather than
carrying AUDITED as acceptance of this rewrite. Their prior audit dates/counts remain history.
The already-PARTIAL award page remains PARTIAL with exact remaining obligations. Touched
colon-bearing provenance values are quoted for strict YAML without changing their text.

The producer-side and capture omissions remain explicitly open. A formal peer may accept, narrow,
or reject individual production claims; this package does not close another agent's TEAM task or
self-award an S-32 L2/terminal verdict. The next independent production package is the known widget
receiver/census defect, not a repeat of these already-tested reward gates.

## 7. Reproduction

From this evidence directory, an agent with Python 3.10+, Linux x86-64 and GCC can run:

```sh
python run_review.py --exe /absolute/path/FFXII_TZA.exe \
  --database '/absolute/path/FFXII TZA' --output /absolute/path/new-empty-results
```

The original EXE and unchanged historical inputs must already exist. Nothing is downloaded.
An incompatible image, altered input, compiler warning, missing original fixture, mismatched
baseline, wrong mutant failure, or nonempty output directory is an explicit failure.
No user command is needed to install the copy-and-merge overlay. This native test is not a Windows
runtime test and must not be used to infer game-session safety.

## 8. Evidence index

- [Original body manifest](original_body_manifest.json), [original disassembly](original_disassembly.txt)
- [Pinned historical inputs](input_manifest.json)
- [Independent retained reducer](review_retained.py)
- [Native source](native_controls.c), [reproduction driver](run_review.py)
- [Run summary](results/summary.json), [71 named cases](results/native_baseline.json)
- [Repeated baseline](results/native_repeat.json), [code mutants](results/code_mutations.json)
- [Raw reduction](results/independent_retained_review.json), [negative controls](results/retained_negative_controls.json)
- [Historical checker replay](results/historical_checker_replay.json)
- [Content validation](results/content_validation.json), [overlay tests](results/overlay_checker_controls.json)
- [Claim/evidence map](claim_matrix.tsv), [exact canonical diff](canonical_changes.diff)
- [File manifest](PATCH_MANIFEST.json), [optional read-only preflight](verify_overlay.py)
