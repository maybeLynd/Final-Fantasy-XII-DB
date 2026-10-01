# Interior citations: input-stack-device-channel-and-bindings.md's entry-cited functions (OPUS, 2026-10-01)

The page named 32 F-frontier functions only at their entry. OPUS read all 32 from the certified image and anchored all 32.

**Method.** The pattern is that of `opus-pfgate-interior-1001`. Each row has one sentence on what the body does (access
and representation, not purpose) and 1-5 interior anchors that do it. Every rip-relative address in a sentence was
resolved by `retool.py`:
- `022CA5C4`/`022CA5D0`;
- `01F2DEF0`/`01F2DEF8`;
- `01F2ED08`;
- `01F401E8`/`01F401F0`;
- `01CB23C0`/`01CB2430`;
- `00D11104`, the float 1/255, read from the image;
- two strings, `00D4A760` "RenderThread" and `00D4A770` "Render thread running without initialize".

`0061C150`'s eight cases were read from its jump table. The table's address is not cited, so no text-gap row is needed.

**Verification.** [`inputstack_interior.py`](inputstack_interior.py) re-decodes every function first. All 136 anchors are
instruction boundaries inside their extents with the recorded mnemonic ([`.out`](inputstack_interior.out): FAILS 0;
idempotent; without `--apply` it only verifies).

**Effect and gates.** All 32 now measure A; none remains in the frontier (3,728 after this record). Gates on the page:
- `check_links`: nothing for the page or the record;
- `check_self_contradiction --db`: nothing for the page;
- `check_consistency`: only the four pre-existing disagreements;
- `verify_doc_addresses --all`: 0 documents to confirm.

**Limits.**
- These are body statements, not meanings. The virtual calls through qword `+0x110` are named by their slot offset only.
  The slot offsets match a D3D11 device-context layout, for example `+0x108` with three arguments, but no interface is
  claimed here.
- `006106A0`'s strings name a render thread although the page is about input. The row states what the body does and
  leaves the page's placement of it to its owner.
- `0061D490` (1,211 B) is summarised at the level of its fields and calls. Its two per-kind acceptance paths are anchored
  at one write each.

## Review (OPUS)

A non-author spot-check goes to SWE2-AUDIT-SPEC: at least 15 rows read against the bytes.
