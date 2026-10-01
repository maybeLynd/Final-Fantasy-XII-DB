# Interior citations: the-time-stop-and-system-stop-registry.md's entry-cited functions (OPUS, 2026-10-01)

The page named 26 F-frontier functions only at their entry. OPUS read all 26 from the certified image and anchored all 26.

**Method.** The pattern is that of `opus-pfgate-interior-1001`. Each row has one sentence on what the body does (access
and representation, not purpose) and 1-5 interior anchors that do it. Every rip-relative address in a sentence was
resolved by `retool.py`:
- `0208E680`, `01E0C2B0` and `01E0CF98`;
- `0215F1B2`, `0215F1B3` and `0215F1D0`;
- `02EC0B40`, and the 32 entries of 0x20 bytes from `02EC0B81` (loop bounds `02EC0F81` / `02EC0FA1`);
- `02ADB6D0`, `02ADB6D8`, `02ADB6E0` and `02ADB720`;
- `02EC07F4`/`02EC07F8`, `009155F0`, `022C6F28` and `02CA8420`.

The constants were read from the image: `01CEBC9C` is -1.0, `01CEBBA8` is 1.0 and `00D11104` is 1/255.

**Verification.** [`timestop_interior.py`](timestop_interior.py) re-decodes every function first. All 107 anchors are
instruction boundaries inside their extents with the recorded mnemonic ([`.out`](timestop_interior.out): FAILS 0;
idempotent; without `--apply` it only verifies).

**Effect and gates.** All 26 now measure A; none remains in the frontier (3,620 after this record). Gates on the page:
- `check_links`: nothing for the page or the record;
- `check_self_contradiction --db`: nothing for the page;
- `check_consistency`: only the four pre-existing disagreements;
- `verify_doc_addresses --all`: 0 documents to confirm.

**Limits.**
- These are body statements, not meanings.
- `003756B0` (578 B) and `00424A40` (510 B) are summarised at the level of their fields and calls. The individual bit
  fields `003756B0` packs into its descriptor qword are not enumerated.
- `002547C0` has one interior anchor, its tail jump, because its store is the entry instruction.
- `002DF640` stores `r8d` through a compare and `cmovne`, which store `r8d` on both paths. The row states this literally.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
