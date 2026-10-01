# Interior citations: what-happens-between-two-frames.md's entry-cited functions (OPUS, 2026-10-01)

The page named 42 F-frontier functions only at their entry. OPUS read all 42 from the certified image and anchored 41.
`003ACA60` is skipped: its whole work is the entry instruction `or byte ptr [02B3F520], cl`, so no instruction inside the
body does it, and citing its `ret` would be an empty anchor. It stays in F.

**Method.** The pattern is that of `opus-pfgate-interior-1001`. Each row has one sentence on what the body does (access
and representation, not purpose) and 1-5 interior anchors that do it. Every rip-relative address in a sentence was
resolved by `retool.py`. These include `01F7F50C`, `01FD49E8`, `02064AA0`/`02064AD0`, `01E09F68`, `00914698`,
`02091950`/`0209216A`, `02092730`, `0209A370`-`0209A3C0`, `00917230`, `02F97348`, `022CB114`, `020926C0`,
`02EBEFC0`/`02EBEFD8`/`02EBEFF0`, `02B3F520`, `02B404E0`, `02B40528`, `022C6F28`, `00906A44` and `02EBA4C0`/`02EBA4D0`. Two
are strings: `00908BB8` "AO render" and `00908BC8` "Water effect". Every callee named is a listed function entry, which
was checked.

**Self-correction on re-read.** `0035EDE0` loops over bit positions 0-15 of `edx`; the first draft said "the 16 bits
set".

**Verification.** [`twoframes_interior.py`](twoframes_interior.py) re-decodes every function first. All 129 anchors are
instruction boundaries inside their extents with the recorded mnemonic ([`.out`](twoframes_interior.out): FAILS 0;
idempotent).

**Effect and gates.** All 41 now measure A. Gates on the page:
- `check_links`: nothing new;
- `check_self_contradiction`: nothing for the page;
- `check_consistency`: only the four pre-existing disagreements;
- `verify_doc_addresses --all`: 0 documents to confirm.

**Limits.** These are body statements, not meanings: what the singletons (`0018CA40`, `001A9930`, `00189120`, `00193D50`),
globals and callees are for stays with the page or open. `00863650` / `00863520` are named by address only.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
