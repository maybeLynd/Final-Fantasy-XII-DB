# Interior citations: the per-frame update gate contract's 41 entry-cited functions (OPUS, 2026-10-01)

**Why.** The F family counts a function as explained (A) only when a DOCUMENTED page cites an address strictly inside its
body. On 2026-10-01, 2,351 of the 4,345 F-frontier functions were already named by a DOCUMENTED page at their entry only
(`Tools/work/OPUS/entry_only_by_page.py`). This contract named 41 such functions. This record reads each one and states
what it does.

**Method (OPUS).**
- **Reading.** Each body was read from the certified image (`Tools/work/OPUS/anchor_prep.py` prints the page's context
  beside the disassembly).
- **Sentence.** One sentence states what the body does: access and representation only. No purpose is invented beyond
  what the bytes and the page support.
- **Anchors.** The anchors are the instructions inside the body that do it.
- **Resolved addresses.** Every rip-relative address in a sentence was resolved by `retool.py` (for example `0209BE80`,
  `02089340`, `02ADD930`-`02ADD932`, `02B45970`, `02B476B0`/`02B476E4`, `00D11D80`, `02092730`, `02AD9B50`, `022C6F28`,
  `002E60F0`, `002985D0`).

**Verification.** [`pfgate_interior.py`](pfgate_interior.py) re-decodes every function from the image before writing.
Each of the 122 anchors must be an instruction boundary strictly inside its function's extent (`functions.tsv`) and must
decode to the recorded mnemonic. Any mismatch writes nothing and FAILS. Run: [`pfgate_interior.out`](pfgate_interior.out)
(41 functions, 122 anchors, FAILS 0). The script is idempotent and byte-preserving.

**Self-correction before publishing.** The first draft said `003F7CC0` "sets floats at `+0x1A4`..`+0x1BC`". The body
writes 0.21 at `+0x1A4`, 0.2 at `+0x1AC` and 127.0 at `+0x1B0` and `+0x1B4`. At `+0x1B8` it does a qword store of 127.0,
so `+0x1BC` gets 0. The row states that.

**Effect.** All 41 functions measure A after the edit (`check_dispositions.measure_a`; F frontier minus 41). Gates on the
page:
- `check_links`: no broken link;
- `check_self_contradiction`: nothing for the page;
- `check_consistency`: the same four pre-existing disagreements, none on this page.

**Limits.** These are body statements, not meanings. What each record, global or callee is for stays where the page
already discusses it, or open. Two callees are described by their position only: `00861EC0` (called with a pointer, 0
and a length) and the math imports `00861F08` / `00861F0E`. They are not named here.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 anchors and their sentences, read against the bytes.
