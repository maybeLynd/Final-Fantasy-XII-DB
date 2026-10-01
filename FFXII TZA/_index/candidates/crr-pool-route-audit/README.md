# CharacterRenderRecord: the pool-route census's rows withdrawn (OPUS, 2026-09-27, BT-2)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

**Question.** db2e18c60 (2026-09-22, "BT-2's bytes were hiding behind a multiply") created CharacterRenderRecord rows
from a pool-route census: the record reached as `idx * 0x740 + [022C6F28]`. That census committed no receipt.
b4b5f347b found two of its rows, `+0x14` / `+0x16`, sitting on other objects. Are the other eleven real?

**Discriminator.** For each cited site, does any definition that reaches the base register come from pool formation?
The analysis is a MAY pass over every path, following copies through registers and stack slots. Where the base is a
function argument, what do the callers pass?

**Result: none of the eleven is on the record.**
- **X:** over all 372 functions that load `022C6F28`, no access in `+0xC..+0xF`, `+0x70..+0x8B` or `+0x230..+0x235`
  has a pool-element receiver on any path.
- **A:** the argument-rooted sites are other objects.
  - `00465CD0`'s receiver is its caller `00465690`'s r14, at all 8 calls. The pool element sat in rdx and is
    overwritten by `mov edx, eax` just before each call.
  - `00524320`'s receiver keeps a pointer at `+0x20` (`mov rsi, [rcx + 0x20]`, then `[rsi + 0x882]`). On the record,
    that position holds instanceKey, a char[32]. The function forms its own pool element separately, in r14.
  - `004256E0` is reached only through two thunks (`00422400` / `00422410`), each referenced once as a table qword. It
    reads its receiver's `+0x31C`, the presentation entry's event word (BT-4).
- **P:** both flow receipts have no access in the spans, and their seeds include pool formation.
- **N (negative control):** the same pass finds 435 pool-element receivers at `+0x284`.

**Cause.** The census treated neither a 32-bit write, which zero-extends, nor any other redefinition as ending a
register's pool value. The same shape is behind `+0x14` / `+0x16`: `add edi, r14d`, `add ecx, ebx`.

**Store change.** The rows go back to DISCOVERED, merged with their DISCOVERED neighbours:
- `+0x0C`, 4 bytes;
- `+0x70`, 32 bytes, absorbing `unobservedSpan008C`;
- `+0x230`, 12 bytes, absorbing `unobservedSpan0236`.

DISCOVERED in the record rises from 162 bytes in 31 spans to 200 bytes in 32.

**Not claimed:** that these bytes are unused. Pointers loaded from memory, spills and return values are not followed.

**Regression S:** fails on the store before the withdrawal and passes after.

**Run receipt.** On 2026-09-27, run verified at fa9602a77:
- `pool_route_audit.py`: X, A, P, N and S PASS, FAILS 0;
- `types_index --validate`: 0 errors, 0 gaps;
- `check_census_widths`: 0 disagreements;
- `check_type_refs`: 0 dangling;
- the CharacterRenderRecord controls: `recut_check.py`, `crr_flow_check.py`, `crr_census_misses.py`,
  `crr_context_ptr.py`, `bt2_name3d4.py`, `bt2_visitors.py`, `hm1_body_bind.py`, `uq194_event_entry.py` and
  `bb4_render_object_per_model.py`, all FAILS 0.

Affected: BT-2 in `_index/OPEN-QUESTIONS.md`.

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` CharacterRenderRecord `+0xC..+0xF`, `+0x70`, `+0x80`, `+0x8A`, `+0x8C`, `+0x230..+0x236` | thirteen rows became three DISCOVERED spans; the old rows are kept in the evidence cells | revised-here |
| `_index/OPEN-QUESTIONS.md` BT-2 | magnitude restated upward | revised-here |
| pages naming the withdrawn field names | none found (grep over `*.md`, `*.py`, `*.tsv`) | agrees |
