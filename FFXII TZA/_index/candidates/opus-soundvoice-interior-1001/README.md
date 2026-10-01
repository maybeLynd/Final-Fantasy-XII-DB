# Interior citations: how-a-sound-request-becomes-a-voice.md's entry-cited functions (OPUS, 2026-10-01)

The page named 42 F-frontier functions only at their entry. OPUS read all 42 from the certified image and anchored all 42;
none is skipped (no body's whole work is its entry instruction).

**Method.** The pattern is that of `opus-pfgate-interior-1001`. Each row has one sentence on what the body does (access
and representation, not purpose) and 1-5 interior anchors that do it. Every rip-relative address in a sentence was
resolved by `retool.py`:
- data: `01F81300`, `02F97390`/`02F97392`/`02F97394`, `0215EF44`, `0215EF4D`, `022CB9F0`;
- vtables and tables: `009059D8`, `00907910`, `00907880`;
- import slots: `008C2A40`, `008C2618`, `008C2DA8`;
- the string at `008F6820`, "vector<T> too long".

**Self-correction on re-read.**
- `002086D0`: the first draft's "0 when that is the end" was ambiguous. It now says the function returns 0 when the
  cursor plus 1 equals the end qword.
- `0020B680`: the first draft named `005CD820` only on the miss path. Both paths call it. The tree is now described by
  its header and its root.
- `0020C300`: the kinds that set words `+0xC`/`+0xE` are values of the fifth argument, which the draft did not say.

**Verification.** [`soundvoice_interior.py`](soundvoice_interior.py) re-decodes every function first. All 179 anchors are
instruction boundaries inside their extents with the recorded mnemonic ([`.out`](soundvoice_interior.out): FAILS 0;
idempotent; without `--apply` it only verifies).

**Effect and gates.** All 42 now measure A; none remains in the frontier (3,760 after this record). Gates on the page:
- `check_links`: nothing for the page or the record;
- `check_self_contradiction --db`: nothing for the page;
- `check_consistency`: only the four pre-existing disagreements (`00442460`, `0031B760`, `003A1DB0`, `005CDAA0`);
- `verify_doc_addresses --all`: 0 documents to confirm, so no text-gap rows are needed.

**Limits.** These are body statements, not meanings. What the singletons, globals and callees are for stays with the
page, or stays open. This covers `00193D50`, `0016D6A0`, `005CD4F0`/`005CD820`, `001BA860`, `00217A60`, `001DBB50`-`001DBDB0`
and `003603C0`. The three import slots are named by address only. In `00360C20`, the first-empty-slot value the loop
records never reaches the return value. `00222200` ends its non-slot-8 path with a store to address 0; the sentence
states that, and does not say why.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
