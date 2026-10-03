# Per-member rows for the PDataMemberMetadata static teardowns: which reflected data member each destroys (OPUS, 2026-10-03)

The [class-descriptor page](../../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md)
declares the C family `PDataMemberMetadata static teardowns` (853 members). This record gives one row to each of 803.

**Form.** Every member is the same 12 bytes: `lea rcx, [X]`, then a tail jump to a `PClassDataMember` destructor
helper:
- `00633240`;
- or 006332A0, for members registered through the array constructor.

Members differ only at the first instruction. Under the family sentence OPUS adopted (`opus-ee-rulings-1003`), the
anchor is therefore the entry `lea`.

**Values, from the image.**
- **X**, the static object.
- **The data member X describes.** It comes from the one registration that loads X with `lea rcx, [X]` immediately
  before a call to a data-member constructor (`00632960`, or the array form `00632A10`). That registration is decoded
  from its function's own entry.
  - The `lea r9` there is the member's name.
  - An immediate `mov dword ptr [rsp + 0x20]` is its offset. It is given as "passed in a register" otherwise.
- **The constructor call site**, printed as a bare address, not a citation.

**No rows.** 50 members have no unique named registration. They are listed in [`excluded.tsv`](excluded.tsv), and
the checker fails if any of them starts deriving.

## Verified

- [`fam_rows.py`](fam_rows.py) `check`: 853 members, 803 rows, 50 declared exclusions, FAILS 0
  ([`fam_rows_check.out`](fam_rows_check.out)).
  - The controls (a swapped value and a moved anchor) are refused.
  - Every anchor lies inside its body's extent; `entry_anchor` is set in [`spec.json`](spec.json).
- `apply` is idempotent.
- Gates on the page: `nb_page` adds nothing; `check_links` 0, `verify_doc_addresses` 0, `check_consistency` 0;
  `check_self_contradiction --db` clean.

## Effect

engine_explained moves from 18,545 to 19,344 of 35,065 (52.89% to 55.17%, `Tools/work/OPUS/ee_gap.py`). Four members
were already counted. These are 12-byte bodies, so under the base rule their entry cites already counted by size. Under
the adopted family sentence, they count because each row is checker-backed and states the member's own value.
