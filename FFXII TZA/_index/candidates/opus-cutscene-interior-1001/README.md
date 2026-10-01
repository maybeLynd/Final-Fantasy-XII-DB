# Interior citations: the cutscene-name-slots page's 47 entry-cited functions (OPUS, 2026-10-01)

The F family counts a function as explained (A) only when a DOCUMENTED page cites an address strictly inside its body.
`99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md` named 47 F-frontier
functions at their entry only (`Tools/work/OPUS/entry_only_by_page.py`). This record reads each one and states what it
does. It follows the pattern of [`opus-mapctrl-interior-1001`](../opus-mapctrl-interior-1001/README.md).

**Method.**
- **Reading.** Each body was read from the certified image with `retool.py dis`.
- **Sentence.** One sentence states what the body does: access and representation only, with no purpose invented beyond
  the bytes.
- **Anchors.** The anchors are the instructions inside the body that do it.
- **Resolved addresses.** Every rip-relative address in a sentence comes from retool's `; ->` annotation: `01DF1030`,
  `01DF0E80`, `01DFE40C`, `01F832B0`, `0208F564`, `0208EC90`, `0208ED58`, `01DFE0B4`, `0208F574`, `0208EA28`, `0208EA40`,
  `01E0C3F0`, `0215E6D0`, `01FD4A64`, `022C6F28`, `01CEBBA8`, `022C7F84`, `022C7F88`, `022CAE95`, `022CBA58` and
  `02B5EA20`.
- **The operand stack.** Many of these are script-verb bodies. "The operand stack" is the VM stack passed in `r9`, read
  through `00267DB0` (a float) and `00267E10` (an int).
- **One row corrected on re-read.** `0034C370`: state 0 writes 1 and falls into the state-1 arm in the same call.

**Verification.** [`cutscene_interior.py`](cutscene_interior.py), with the rows in [`rows.py`](rows.py), re-decodes every
function from the image before writing. Each of the 166 anchors must be an instruction boundary strictly inside its
function's extent (`functions.tsv`) and decode to the recorded mnemonic. Any mismatch writes nothing and FAILS. Run:
[`cutscene_interior.out`](cutscene_interior.out) (47 functions, 166 anchors, FAILS 0). The script is idempotent and
byte-preserving.

**Effect.** All 47 functions measure A afterwards (`check_dispositions.measure_a`); none were skipped. Gates:
- `check_links`: nothing for the page or the record;
- `check_self_contradiction`: nothing for the page;
- `check_consistency`: only the four pre-existing disagreements (`00442460`, `0031B760`, `003A1DB0`, `005CDAA0`);
- `verify_doc_addresses --all`: 0 documents to confirm.

No text-gap rows were needed.

**Limits.** These are body statements, not meanings. The functions callees and tables name stay where the page already
discusses them, or open. `002673D0`'s listed extent (95 B) runs past its `ret` at `002673E8` into the next listed entry
`002673F0`. Its anchors stay in the real body, and the extent is a `functions.tsv` matter, not changed here.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
