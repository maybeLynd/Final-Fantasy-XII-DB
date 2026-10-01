# Interior citations: the boot page's 45 entry-cited functions (OPUS, 2026-10-01)

**Why.** The F family counts a function as explained (A) only when a DOCUMENTED page cites an address strictly inside its
body. `what-the-engine-fixes-at-boot.md` named 45 F-frontier functions only at their entry
(`Tools/work/OPUS/entry_only_by_page.py`). This record reads each one and states what it does. It is the second
package of the method first used in [`opus-pfgate-interior-1001`](../opus-pfgate-interior-1001/README.md).

**Method (OPUS).**
- Each body was read from the certified image with `Tools/work/OPUS/anchor_prep.py`, which shows the page's context
  beside the disassembly.
- One sentence per function states what the body does: access and representation only, with no purpose invented beyond
  the bytes and the page.
- The 2-4 anchors per row are the instructions inside the body that do it.
- Every rip-relative address in a sentence was resolved by `retool.py`'s annotation, not by hand.
- Callees and imports are named by address only, for example `00863540`, `008636E0`, `00863610`, `00863520` and the
  imports at `008C2F78` / `008C2330`.

**Verification.** [`boot_interior.py`](boot_interior.py) re-decodes every function from the image before writing. Each of
the 161 anchors must be an instruction boundary strictly inside its function's extent (`functions.tsv`) and must decode
to the recorded mnemonic. Any mismatch writes nothing and FAILS. Run: [`boot_interior.out`](boot_interior.out)
(45 functions, 161 anchors, FAILS 0). The script is idempotent and byte-preserving.

**Self-correction before publishing.** A re-read of the sentences against the listings changed three rows:
- `00368C80`: the first draft said it "waits until" the qword `022D7F70` is non-zero. The loop at
  `00368D76`-`00368D81` tests a value read once at `00368D6F` and never re-reads it, so the row now says that.
- `0039CD50` and `003773C0`: "zeroes the fields after it" became the exact resolved addresses, which lie before or beside
  the named field, not after it.

**Effect.** All 45 functions measure A after the edit (`check_dispositions.measure_a`), so the F frontier loses 45.
Gates:
- `check_links`: nothing broken for the page or the record;
- `check_self_contradiction`: nothing for the page;
- `check_consistency`: the same four pre-existing disagreements (`00442460`, `0031B760`, `003A1DB0`, `005CDAA0`).

**Limits.**
- These are body statements, not meanings. What each global, record or callee is for stays where the page discusses it,
  or open.
- Several rows summarise long store sequences by their resolved anchors and ranges rather than listing every store:
  `0026E1D0`, `0035E820`, `0035EC90` and `003ABB60`.
- `0035EC90`'s mode test is stated as "tests bit 13 of a mode-selected dword", without naming the dwords.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
