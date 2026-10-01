# Interior citations: the largest-unclassified page's 46 entry-cited functions (OPUS, 2026-10-01)

**Why.** The F family counts a function as explained (A) only when a DOCUMENTED page cites an address strictly inside
its body. `99-Unresolved-Residual/Largest-Unclassified-Code/the-largest-unclassified-functions.md` named 46 F-frontier
functions at their entry only (list: `Tools/work/OPUS/entry_only_by_page.py`).

**Method.** This is the pattern of `opus-mapctrl-interior-1001`.
- **Reading.** Each body was read by hand from the certified image (`retool.py dis`, over the `functions.tsv` extent).
- **Sentence.** One sentence per function states what the body does: access and representation, not purpose.
- **Anchors.** Two to five anchors per function are the instructions inside the body that do it.
- **Addresses.** Every rip-relative address in a sentence is the one `retool.py`'s `; ->` annotation printed. These
  include `020910F0`, `022BDEB8`, `02EC3D60`, `02EC19C0`/`02EC19C4`, `02EC32E0`, `02EC3D7D`, `022D94B0`/`022D94B4`,
  `02AEECB0`, `02AEE900`, `022D8F30`, `022D92E0`/`022D92F0`, `02EBEF70`, `02EBEC00`-`02EBEF60`, `02EBE5E0`-`02EBEBE0`,
  `02B404C8`/`02B404C1`, `02B47730`, `02B47790`/`02B47798`, `02B5D0B0`, `02CA8450`/`02CA8458` and `008F4438`.
- **Tables after a body.** The jump and index tables just past `0024E210`, `003AA470` and `003B0AD0` are not named, so
  no text-gap citation is needed.
- **Skipped.** Nothing.

**Self-correction before publishing.** Re-reading the sentences against the listings changed three rows:
- `003B4A50`: for kind 2, sub-kind 1 tests `0024E2F0`, 2 tests `0024E6D0`, 3 passes on either, and any other sub-kind
  fails; the stop is at a byte `+0x2C` below the smallest seen so far.
- `0034EF60`: while waiting it returns 1 without the `0053DD10` test.
- `00346AA0`: wording only.
The first run refused `00504610` for a `|` in its sentence; the OR is now spelled out.

**Verification.** [`lu_interior.py`](lu_interior.py) re-decodes each function before writing. Each of the 159
anchors must be an instruction boundary strictly inside its function (`functions.tsv` extent) and must decode to the
recorded mnemonic ([`lu_interior.out`](lu_interior.out): 46 functions, 159 anchors, FAILS 0; a second run reads
ALREADY).

**Effect.** All 46 functions now measure A (0 before); the A total went 10,155 -> 10,201. Gates:
- `check_links`: nothing for the page or the record;
- `check_self_contradiction`: nothing for the page;
- `check_consistency`: only the four pre-existing disagreements (`00442460`, `0031B760`, `003A1DB0`, `005CDAA0`);
- `verify_doc_addresses --all`: 0 documents to confirm.

The page's other sections are untouched.

**Limits.** These are body statements, not meanings. Callees are named by address only. Where a selector maps to a
bit or return value through a jump table (`0024E210`, `003B0AD0`), the sentence states the set of outcomes, not each
case's mapping.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC (`OPUS-REQ-AUDITSPEC-LU-INTERIOR-1001`): at least 15 rows read
against the bytes, including `003AA470`, `003B4A50` and `00504610`.
