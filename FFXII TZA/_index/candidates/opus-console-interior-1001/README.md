# Interior citations: what-the-console-tunes.md's entry-cited functions (OPUS, 2026-10-01)

The page named 35 F-frontier functions only at their entry. OPUS read all 35 from the certified image and anchored all 35.

**Method.** The pattern is that of `opus-pfgate-interior-1001`. Each row has one sentence on what the body does (access
and representation, not purpose) and 1-5 interior anchors that do it. Every rip-relative address in a sentence was
resolved by `retool.py`: `01F812C8`, `01DF0010`/`01DF0018`, `01F7F53C`, `02CB8138`, `01DFE190`/`01DFE194`, `02CB8154`,
`01F82D20`, `01E0CF88`, `0209E65C`, `022BE7D8`/`022BE7DC`, `01EEBAE0`/`01EEBAE4`. `00308E80`'s two tables are image-base
relative (`lea rdx, [00120000]`): `022C24E0` and `01EEC268`. Its fallback `00D10394` is the string "Nobody". The constants
were read from the image:
- `008F9558`: double 0.001;
- `008FCCA0`: floats (1, 0, 0, 1);
- `008FCC94`: 3.14159;
- `008F3138`: 180.0;
- `01CEBDA0`: the sign mask;
- `01CEBBA8`: 1.0.

**Self-correction on re-read.**
- `0017E7A0`: the first draft said it "wraps into 0..2". In fact a negative sum is stored as 2 and a sum above 2 as 0.
- `00182E10`: the first draft left out its guard. It calls only when `001DDAB0()` is non-null.

**Verification.** [`console_interior.py`](console_interior.py) re-decodes every function first. All 114 anchors are
instruction boundaries inside their extents with the recorded mnemonic ([`.out`](console_interior.out): FAILS 0;
idempotent; without `--apply` it only verifies).

**Effect and gates.** All 35 now measure A; none remains in the frontier (3,874 after this record). Gates on the page:
- `check_links`: nothing for the page or the record;
- `check_self_contradiction --db`: nothing for the page;
- `check_consistency`: only the four pre-existing disagreements;
- `verify_doc_addresses --all`: 0 documents to confirm.

**Limits.** These are body statements, not meanings. What the singletons (`001F0850`, `0018CA40`, `001EBA40`,
`001DDAB0`, `00796E20`, `00210B30`), the globals and the callees are for stays with the page, or stays open.
`00861EC0`, `007A4380`/`007A4C70`/`007A45C0` and `001243B0` are named by address only. `002F1CD0` and `002F4510` have
one interior anchor each: the second store, because the first store is their entry instruction.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
