# Interior citations: the-widget-message-protocol.md's entry-cited functions (OPUS, 2026-10-01)

The page named 30 F-frontier functions only at their entry. OPUS read all 30 from the certified image and anchored all 30.

**Method.** The pattern is that of `opus-pfgate-interior-1001`. Each row has one sentence on what the body does (access
and representation, not purpose) and 1-5 interior anchors that do it. Every rip-relative address in a sentence was
resolved by `retool.py`:
- `020927F0`, `0208F570` and `0209BE80`;
- `009170C0` and `0215F200`;
- `02CA8F30` and `0209AC30`;
- `02CA99D0`/`02CA99D8`, `0208EA28` and `02B62D88`;
- `01E0C1D8`/`01E0C1DC`;
- `00D111C0`, the 16 bytes (8, 0, 0, 0), read from the image;
- three callbacks passed by address, `0029A0A0`, `003CB150` and `00405310`, each a listed function entry.

`0027C150`'s 21 cases and `002C9B30`'s 9 cases were read from their jump tables. Each table starts at its body's end.
The table addresses are not cited, so no text-gap row is needed.

**Self-corrections before publishing.**
- `0057E8D0`: an anchor was recorded with the wrong mnemonic. The applier refused it, and it now records `je`.
- `00406A60`, `0057E8D0`, `0057EB30`: these rows first wrote `00244960([0208EA28], rcx)` in a line that also says
  "stores". `check_self_contradiction` read that as a write to `0208EA28`, which the page's line 833 records as never
  written. The rows now say "the qword read from `0208EA28`": the code reads it, it does not write it.

**Verification.** [`widgetmsg_interior.py`](widgetmsg_interior.py) re-decodes every function first. All 134 anchors are
instruction boundaries inside their extents with the recorded mnemonic ([`.out`](widgetmsg_interior.out): FAILS 0;
idempotent; without `--apply` it only verifies).

**Effect and gates.** All 30 now measure A; none remains in the frontier (3,646 after this record). Gates on the page:
- `check_links`: nothing for the page or the record;
- `check_self_contradiction --db`: nothing for the page;
- `check_consistency`: only the four pre-existing disagreements;
- `verify_doc_addresses --all`: 0 documents to confirm.

**Limits.**
- These are body statements, not meanings. Message kinds are stated as the numbers the bodies compare (1, 2, 4, 17,
  18). What each kind means stays with the page.
- `002D1420` and `00407C90` dereference through `rcx` even on their null paths. The rows state the addresses the code
  reads; they do not say whether a caller can pass null.
- `00406A60` (865 B) is summarised per kind, with one anchor per kind's main write or call.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
