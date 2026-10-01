# Interior citations: game-application's entry-cited functions (OPUS, 2026-10-01)

**Why.** The F family counts a function as explained (A) only when a DOCUMENTED page cites an address strictly inside its
body. [`game-application.md`](../../../00-Engine-Core-Runtime/Application-Root/game-application.md) named 58 F-frontier
functions only at their entry (`Tools/work/OPUS/entry_only_by_page.py`). This record reads 57 of them and states what
each does. It is the fourth package of the method first used in
[`opus-pfgate-interior-1001`](../opus-pfgate-interior-1001/README.md), after
[`opus-boot-interior-1001`](../opus-boot-interior-1001/README.md).

**Method (OPUS).**
- Each body was read from the certified image with `Tools/work/OPUS/anchor_prep.py`.
- One sentence per function states what the body does: access and representation only, with no purpose invented beyond
  the bytes.
- The 2-7 anchors per row are the instructions inside the body that do it.
- Every rip-relative address in a sentence was resolved by `retool.py`'s annotation, not by hand. The image-base tables
  of `00369100` / `003691B0` (`022CFEEC`, `022CFEF0`, `022CFF10`) were resolved from `lea rdi, [image base]` plus the
  displacement. The import slot `008C2F70` (`strncpy`) came from the PE import table.
- Callees are named by address only.

**Skipped.** `0061D490` (1,211 B) runs several viewport and render-target selection paths with six `0061E6B0` calls. One
honest sentence could not state it, so it stays entry-only and F.

**Verification.** [`gameapp_interior.py`](gameapp_interior.py) re-decodes every function from the image before writing.
Each of the 208 anchors must be an instruction boundary strictly inside its function's extent (`functions.tsv`) and must
decode to the recorded mnemonic. Any mismatch writes nothing and FAILS. Run: [`gameapp_interior.out`](gameapp_interior.out)
(57 functions, 208 anchors, FAILS 0). The script is idempotent and byte-preserving, and appends one section at the end of
the page. The page's existing sections are untouched.

**Self-correction before publishing.** A re-read against the listings changed one row. `001D8CD0` first said "zeroes
`+0`". The store at `001D8CF4` is a byte store, `+0x28` / `+0x30` are a qword and a dword, and a failed allocation stores
0 in the global. The row now says all of that.

**Effect.** `check_dispositions.measure_a` was run on the DB with the page at HEAD and with the page edited: 9,974 -> 10,031
A (+57). All 57 rows are newly A, so the F frontier loses 57.

**Gates.**

| gate | result |
|---|---|
| `check_links` | nothing for the page or this record; the 16 broken links at HEAD are pre-existing elsewhere |
| `check_self_contradiction --db` | nothing for the page |
| `check_consistency` | the same four pre-existing disagreements (`00442460`, `0031B760`, `003A1DB0`, `005CDAA0`) |
| `verify_doc_addresses.py --all` | 0 documents with .text non-function citations to confirm |

**Limits.**
- These are body statements, not meanings. What each global, record or callee is for stays where the page discusses it,
  or open.
- The long bodies are summarised by their resolved anchors, not by every store: `0020B840`, `0020BFA0`, `0067A010`,
  `001A1240` and `0067F280`. `0020BFA0`'s stop flag (`bl`) is named by register only.
- `0050CE40` and `0050D780` quote format strings at `00D22938` / `00D22A0C` as they appear in the image.

**Review routing.** `OPUS-REQ-AUDITSPEC-GAMEAPP-INTERIOR-1001` (SWE2-AUDIT-SPEC) asks for a spot-check of at least 15 rows
against the bytes. The method's first review (pfgate) is also pending.
