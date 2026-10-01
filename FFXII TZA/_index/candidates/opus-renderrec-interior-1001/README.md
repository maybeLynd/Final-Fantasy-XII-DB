# Interior citations: the-character-render-record-array.md's entry-cited functions (OPUS, 2026-10-01)

The page named 27 F-frontier functions only at their entry. OPUS read all 27 from the certified image and anchored all 27.

**Method.** The pattern is that of `opus-pfgate-interior-1001`. Each row has one sentence on what the body does (access
and representation, not purpose) and 1-5 interior anchors that do it. Every rip-relative address in a sentence was
resolved by `retool.py`:
- `01F82D60`, `008A6C70`, `02B40528`;
- `022C6F20`, `022C6F28`, `022C6F30`;
- `01CEBBA8`, the float 1.0.

The three strings `00332510` passes to `001EB150` were read from the image:
- `00D10A38` "display character : preprocessing";
- `00D10A80` "display character : draw objects";
- `00D10AA8` "display character : after emission".

**Verification.** [`renderrec_interior.py`](renderrec_interior.py) re-decodes every function first. All 96 anchors are
instruction boundaries inside their extents with the recorded mnemonic ([`.out`](renderrec_interior.out): FAILS 0;
idempotent; without `--apply` it only verifies).

**Effect and gates.** All 27 now measure A; none remains in the frontier (3,701 after this record). Gates on the page:
- `check_links`: nothing for the page or the record;
- `check_self_contradiction --db`: nothing for the page;
- `check_consistency`: only the four pre-existing disagreements;
- `verify_doc_addresses --all`: 0 documents to confirm.

**Limits.**
- These are body statements, not meanings. What the flag bits of dwords `+0x290`, `+0x294` and `+0x304` mean stays with
  the page.
- `00427300` and `004278B0` have one interior anchor each, because their first write is the entry instruction.
- `00504740` forms an address from a 32-bit sum of two dwords. The row states that literally and does not claim why.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
