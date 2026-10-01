# CharacterRenderRecord +0x10 is an 8-byte pointer (OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

**Question.** `+0x10` was declared `encodedContextPtr`, `uint32`, 4 bytes, but one site reads it as a qword.
`OPUS-ADJUDICATE-THREE-WIDTH-DISAGREEMENTS-FOUND-BY-BLINDSPOT-12` ruled on 2026-09-21: "a lone outlier; the declared
uint32 stands". That ruling weighed the one qword read against the dword reads and never looked at the writer.

**Discriminator.** How wide is the store, and what do the narrow reads do with the value?

**Evidence** (`crr_context_ptr.py`):
- **W1–W3: the writer.** `00420480` stores `+0x10` once, as a qword (`0042055B`, rbx = r9). Its sole caller, `004279B0`,
  passes r9 = the return of `0020E600`, which is `mov eax, ecx; add rax, qword [01F83530]` — a 64-bit pointer.
- **R1: the wide reader.** `0042DA5C` reads the qword and dereferences it at once (`+0xD90`).
- **R2: the narrow readers.** All 145 dword reads in the flow receipt load ecx and pass it straight to `0020E600`. They
  re-resolve the low half. This is exact while the base `01F83530` is zero, which is its load-time value.
- **P: the upper half.** In both flow receipts, nothing receiver-proven touches `+0x14..+0x17` except the two qwords.
- **X: the removed rows.** The `+0x14 word0014` and `+0x16 word0016` rows came from the 2026-09-22 pool-route census
  (db2e18c60). All seven of their sites are in `0053AB50`. Reaching definitions put every one on another object:
  - a 0x30-stride table returned by `00521290` / `005212E0`;
  - a 32-bit base walked at 0xE0;
  - a 32-bit `add edi, r14d`;
  - a stack buffer.

  That census carried a pool-formed register past its redefinition.
- **N: negative control.** The same analysis ties `0053AC2E`'s `+0x284` read to the pool formation `0053AC27`.

**Regression S.** It fails on the store at HEAD (`+0x10` 4 bytes, rows at `+0x14` / `+0x16`) and passes after.

**Not claimed:**
- what the pointer points at;
- whether `01F83530` can ever hold a base at or above 4 GiB, in which case the narrow readers would lose the high half.
  That stays a runtime question in `CONTRACT-encoded-id-space-and-class-registry.md`.

The name `encodedContextPtr` is kept, because this correction is about representation. The meaning cell no longer says
the pointer is "not used directly".

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` CharacterRenderRecord `+0x10` | width 4 → 8, `uint32` → `void*`; the old row is kept in the evidence cell | revised-here |
| `_types/fields.tsv` CharacterRenderRecord `+0x14`, `+0x16` | removed; both rows are kept verbatim in `+0x10`'s evidence | revised-here |
| `_index/ABSENCE-CLAIM-GATE.md` blind-spot-12 bullet (OPUS) | re-adjudication noted under the bullet | revised-here |
| `17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md` line `+0x010 u32` | routed to the page owner | routed |

**Run receipt.** `crr_context_ptr.py` on 2026-09-27:
- on HEAD's store: FAIL S only;
- on the patched store: PASS W1–W3, R1, R2, P, X, N and S.

The other checks on the patched store:
- `types_index --validate`: 0 errors, 0 gaps;
- `check_census_widths`: 0 disagreements, with `+0x10` listed as a stated WIDTH-DELIBERATE row;
- `check_type_refs`: 0 dangling.
