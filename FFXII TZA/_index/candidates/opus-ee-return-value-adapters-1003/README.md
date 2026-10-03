# Per-member rows for the DF-4 return-value adapters: the getter each calls and the reflected type it serves (OPUS, 2026-10-03)

The [return-value adapter page](../../../24-Compiler-And-CRT-Runtime/Generated-Adapters/the-return-value-adapter-family.md)
declares DF-4 with 402 members and explains its 26-byte shape once. This record adds one row for each of 394 members.
The format follows SWE2-AUDIT-SPEC's per-member ruling (`202e59a0a`):
- **The anchor** is the adapter's only `call`, its distinguishing instruction.
- **The member-specific values** are two:
  - the getter the call targets (no two rows share one);
  - the reflected type T: the template argument of every `PClassDescriptor*<T>` vtable that holds the adapter at slot
    5, read from that vtable's MSVC RTTI type descriptor in the image. All such vtables must agree.
- **Template types** (`PArray<...>`, `PSharray<...>`) are given as their exact decorated argument from the image, not a
  hand demangling.
- **The getter** is printed as a bare address, not a citation. A getter is explained, or not, on its own page, and
  only the adapter's interior anchor counts here.

**No rows:**
- Eight DF-4 members, listed with their reasons in [`excluded.tsv`](excluded.tsv):
  - five are not a single direct call;
  - three sit in vtables that do not name one template type.
- The 46 DF-1 members. Their bodies are identical, so nothing distinguishes one member from another.

## Verified

- [`fam_rows.py`](fam_rows.py) `check` re-derives every row from the certified image: 402 members, 394 rows, and 8
  declared exclusions that must still be refused. FAILS 0 ([`fam_rows_check.out`](fam_rows_check.out)).
  - The controls (a swapped target and a moved anchor) are refused.
  - Every anchor lies strictly inside its body's census extent.
- `fam_rows.py apply` is idempotent.
- Gates on the page: `nb_page` adds nothing; `check_links` 0, `verify_doc_addresses` 0, `check_consistency` 0;
  `check_self_contradiction --db` clean.

## Effect

engine_explained moves from 18,158 to 18,545 of 35,065 (51.78% to 52.89%; `Tools/work/OPUS/ee_gap.py`, which
reproduces progress.py's numerator). Seven of the 394 members were already explained.
