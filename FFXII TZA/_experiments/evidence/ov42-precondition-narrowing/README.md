# OV-42 action preconditions: returned-review qualification and producer repair

This additive record qualifies immutable `ov42-special-action-preconditions`
(`318e510c6692309620b468b4d6101582072d8019`). The independent review at
`_index/candidates/auditspec-review-astra-ov42-action-preconditions-0930/REVIEW.md`
(`2e88eceef`) is **ACCEPT-WITH-NARROWING**. Its committed record controls that
scope; the older board ACCEPT referencing a gitignored batch is not a substitute.
This new repair is producer-validated and awaits its own independent review.

Question: which conditional source statements survive that review, and can the
default semantic checker distinguish verified shipping code from retained text
whose bytes/kind/branch no longer match? Method A is sufficient. All propositions
here concern retained authored values or bounded original code. No game session,
native/emulated execution, fresh archive extraction, or reviewer census is needed.

## Corrected model

- The special identity row is **0x113 (decimal 275)**. `003092B4` constructs
  `base + 0x113*stride` for the row-pointer comparison. That arm substitutes the
  actor-type stack-table entry for `word[row+0x24]`. Decimal 113 is a different
  non-sentinel row. The actor-type/table bound remains a premise.
- Rows **511–534 are decimal** and lie above 0xF1. The local refusal of rows
  **0xD0–0xF1** at `0030CEFE` applies only to the DWORD mode value 5 or 6 read
  from `022C2160`. This follows unsigned modulo-32 `(mode-5)<=1`; it is not an
  unconditional id exclusion or an observation of the current game mode.
- At the `00306BDA` read, mode must be 0, or 1 with the same owner read from
  `022C2168`, to pass the prefix. It then publishes mode 1 and owner, calls
  `0032F6E0(3)`, and requires a normally returned zero before reaching
  `00309230` at `00306C4D`. Mode 2 is written before that selector call. These
  ordered reads/writes and call do not establish atomicity or omitted callee
  effects. The group argument is shipping **`00306C0A mov ebx,3`**, transferred
  through `00306C54` to `0032FC30`.
- The retained non-FFFF table predicate proves the **sign of the narrowed
  WORD** `(4*w+1) mod 65536`. It is not a full-index bound, native load success,
  initialized content, or a safety guarantee. The reviewer independently found
  ten distinct non-FFFF words >=0x8000, full indices 131101–131629, and no bit30
  on their rows. Those counts and the reviewer's executions are external
  corroboration, not new experiments performed for this package.
- The original bit30-only exclusion hypothesis remains refuted by ordinary
  FFFF rows 511–534. Natural selection, initialized row/codec identity,
  metadata/size/FST success and owner/native submission remain unproved.

## Actual producer repair and controls

`check-special-admission.py` now calls `qualify-special-admission-source.py`
**by default**, before its table predicate. The gate hashes the actual shipping
EXE (`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`,
base 0x120000), compares every retained range byte to it, and invokes the reviewed
`validate-title-source-annotations.py` using Capstone 5.0.7 and the actual shared
`reg_tracking.py` adapter. It also pins the mode/owner branches and group-3
witness. Original ranges, captures and the central access-role policy are unchanged.

The one complete positive rerun is required because that producer changed. It
reuses the same nine retained tables and verifies the same bounded predicate; it
is not a new archive census, additional live evidence, or independent acceptance.
`special-admission-result-02.json` preserves source validation and corrected limits.

The actual CLI controls reproduce **three old false acceptances**: altered kind
bytes with stale text, coherent kind 3→5, and a coherent mode-range branch reversal.
The fixed default refuses all three. It also refuses failed role controls and a
labelled non-image reference fixture. All five fixed invocations terminate nonzero
with the expected error and **no semantic result**. The old accepted synthetic
results are defect evidence only. A self-consistent annotation is not shipping
identity. Controls are synthetic inputs, not original-code executions.

Reproduce in this directory with the project's existing Python:

    python check-special-admission.py special-admission-raw-01.json action-selectors-01/result.json action-selectors-01/tables NEW_RESULT.json
    python control-special-admission-source.py NEW_CONTROLS_DIRECTORY

Existing paths must stay immutable. The actual central adapter remains a required
repository dependency; its copied receipt is not used to replace it. The pinned
original image is read from the repository, never altered.

## Impact and consumption

The impact receipt identifies exact textual references and hashes. The original
packet and its nested copies in `action-selector-local-exclusions` retain the old
checker/wording and require this qualification when those statements are used.
The reviewer independently reproduced their real captures from the shipping image;
these concrete checker defects therefore downgrade their *general checker assurance*,
not that byte agreement or every downstream semantic claim. Category, fallback,
class20 and FST packets retain their separately reviewed scopes. The canonical
index/source capture/access-role adapter is not reported regressed.

FABLE's existing action-preconditions consumer is the semantic destination; its
task is still pending independently of DONE review rows. Use the narrowed review
and this additive correction when incorporating those exact claims. Do not infer
full OV-42 or OV-21 closure. New repair acceptance requires the assigned non-author
review of this actual default invocation, not only old packet integrity.

Cleanup: all bounded child scripts are terminal, no PC/game controls or native
instruments were started, and no saves/configuration/reference image were written.
Original source/driver/table identities are preserved in the input/cleanup receipts.
The menu setup allowance remains spent with extension unapproved; EXP-127 remains
INVALID_POST_TRACE. Full L1+L2 goal remains ACTIVE/NOT_MET.

Reusable lesson: pin the actual kind-producing instruction and byte provenance
before a downstream WORD predicate. Preserve modulo width, radix, conditional
state reads and omitted-call limits in result prose. Do not repeat a settled
table survey to answer natural action reachability. The next useful question must
name a still-unresolved producer or state invariant and its canonical consumer.
