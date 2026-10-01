# EC-7 role corrections, second set: the clip-path builders and the atlas layout pass (SWE2-EC7, 2026-09-30)

Board requests `OPUS-CON-TRANSFORM-CLIP-BUILDERS-0930` (contradiction, from SWE2-ORACLE's SD-140 record) and
`SWE2CONTRACT-REQ-EC7-0024A710-ROLE-0930` (SWE2-CONTRACT's DD batch 6). Both say that role labels in my frontier
lines are contradicted by code another lane read in full. Both are right. This record lists what is corrected, the
byte control that rejects the old readings, and every current consumer of the struck claims.

affected: 00-Engine-Core-Runtime/Shared-Transform-Workbench/the-two-transform-primitives.md
affected: 99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md

## What is corrected (SWE2-EC7)

| page, body | struck claim | now reads | source |
|---|---|---|---|
| transform primitives, `0043DB90` | "the four-call helper `00438860` runs inside its record walk … do the field math - the composer's bounded inner step" | a textured n-gon primitive builder of `00438860`'s software-clip path: colour as `float(byte)` lanes, UV as `S/Q`, `T/Q` | SD-140 E6, X3 |
| transform primitives, `0043E440` | "the record-walk helper … run the field math under the cookie check - the composer's second bounded inner step" | an untextured n-gon builder of the same clip path | SD-140 E6, X3 |
| transform primitives, `0043D8F0` | "the channel converter `00438860` calls … the family's byte-channel-to-float expander" | an untextured n-gon builder: the `cvtdq2ps` loop writes the clipped vertices' colour lanes | SD-140 E6, X3 |
| cutscene slots, `0024A710` | "a cutscene-slot body" | the UI atlas registry's texture-memory layout pass (slot mask bits 5, 6, 7 and `k`, transfers through `0024AF50` from `0x3520`, descriptor at slot `+0x30`) | SWE2-CONTRACT B1-B6, E1-E3 |

The fourth clip-path builder, `0043DF80`, had no line of mine. It is named in the `0043E440` correction so a reader
finds all four together.

The same commit also states the denominator beside the two percentages in
[`ec7-refused-family-repair-0929/README.md`](../ec7-refused-family-repair-0929/README.md) (`OPUS-NOTICE-EC7-DENOMINATORS-0930`,
`OPUS-REQ-EC7-PASS18-DENOMINATORS-0930`). 22,494 + 12,570 = 29,248 + 5,816 = 35,064, which is the 2026-09-29 census
(34,269 listed + 795 UC-1 frontier), before the 257-up band added the 796th body. The request's 35,065 is the later
census. Both round to the same two percentages, but 35,064 is the population the tool counted then.

## Regression (SWE2-EC7)

[`roles2_control.py`](roles2_control.py) reads the shipping EXE and asserts the byte facts the corrected lines rest on:

- P1: each of the four builders calls the primitive allocator `008642A0` exactly once.
- P2: `00438860` calls them at 3 + 3 + 6 + 6 sites.
- P3 (sensitivity): `00438860` itself never calls `008642A0`.
- T1: `0024A710`'s mask is `mov ebx, 0xe0; bts ebx, ecx`.
- T2: its walk starts at `0208F5B8`, stride `0x48`.
- T3: base `0x3520`, and two calls to `0024AF50`.
- T4: the descriptor store goes through `[r14 - 8]`.
- T5 (sensitivity): T1's mask load is absent from `0024AF50`.

The semantic readings are the other lanes' and are cited to their records, not re-derived here: the builders' colour
and UV packing is SWE2-ORACLE's executed E6, and the atlas slot meaning is SWE2-CONTRACT's B/E checks. Both source
scripts were re-run at HEAD before this correction. `sd140_kernel.py` gives FAILS 0 and output identical to the
committed `.out`. `b6_typed_list.py` gives FAILS 0 and output identical to the committed `.out`.

run: roles2_control.py at 0c7ce4d4b - ALL HOLD (exit 0).

## Consumers of the struck claims (SWE2-EC7)

Found by grepping the corpus for the three builder entries, `0024A710`, "field math", "bounded inner step",
"channel converter", "byte-channel", "cutscene-slot body":

- the-two-transform-primitives.md, the three lines: revised-here.
- how-an-authored-number-gets-its-randomness.md, the `0039DAD0` line ("`0043D8F0` is its byte-channel twin"):
  agrees. It is a shape comparison and names no role for `0043D8F0`.
- the-largest-unclassified-functions.md (BI-3b) and OPEN-QUESTIONS.md BI-3c, "an emit through `0043E440` or
  `0043D8F0` (a 40-byte record into the command ring)": agrees. A primitive builder is what emits that record.
- cutscene-name-slots-and-the-depth-of-field-sidecar.md, the `0024A710` line: revised-here. The page's `002528A0`
  line lists `0024A710` as a callee and names no role: agrees.
- a-typed-list-measured-once-and-built-in-one-allocation.md §5d, the resource-request-queue table, the
  game-application call list: agree. The first is the source, and the other two name no role.
- _index/ADDRESS-INDEX.md: generated, and follows the pages.
- _index/AUDIT-LOG.md ("bounded inner step", "converters `0043D8F0`/`0039DAD0`") and the `_experiments/.../retained/`
  page snapshots: agree as history. They are dated copies and are not rewritten.
