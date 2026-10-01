# Interior citations: fef-and-motion-entries.md's entry-cited functions (OPUS, 2026-10-01)

The page named 36 F-frontier functions only at their entry. OPUS read all 36 from the certified image and anchored all 36.

**Method.** The pattern is that of `opus-pfgate-interior-1001`. Each row has one sentence on what the body does (access
and representation, not purpose) and 1-5 interior anchors that do it. Every rip-relative address in a sentence was
resolved by `retool.py`:
- `02F97340` and `0209A2A0`;
- `02B3F570` and `02B40528`;
- `01DFE0B4` (read as a dword, a word and a byte by different functions) and `01DFE0BC`;
- `02CA4438` and `02CA4698`;
- `01CEBBA8`, the float 1.0;
- `00D117B0`, the float 0.166667, read from the image.

**Verification.** [`fef_interior.py`](fef_interior.py) re-decodes every function first. All 151 anchors are instruction
boundaries inside their extents with the recorded mnemonic ([`.out`](fef_interior.out): FAILS 0; idempotent; without
`--apply` it only verifies).

**Effect and gates.** All 36 now measure A; none remains in the frontier. Gates on the page:
- `check_links`: nothing for the page or the record;
- `check_self_contradiction --db`: nothing for the page;
- `check_consistency`: only the four pre-existing disagreements;
- `verify_doc_addresses --all`: 0 documents to confirm.

**Limits.**
- These are body statements, not meanings. What the records, flags and callees are for stays with the page, or stays
  open.
- `00409190` adds its offset to the sign-extended low dword of `rcx`, and the row states exactly that. Whether the caller
  passes a pointer or an integer there is not claimed.
- The four ramp writers (`00418650`, `004186A0`, `00418700`, and the `+0x190`/`+0x1B0`/`+0x1D0` arrays) are described
  by their indexing only.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
