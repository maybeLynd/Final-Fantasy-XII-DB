# Per-member rows for the 319 PInputs semantic-name initialisers: which node and name each registers (OPUS, 2026-10-03)

The [input-name registry page](../../../15-Input/Input-Name-Registry/the-input-name-registry-and-channel-aliases.md)
declares the C family `PInputs semantic-name-registry initialisers` (319 members). Its shared 32-byte shape was
explained once, and no member was explained individually. This record adds one row per member. The format follows
SWE2-AUDIT-SPEC's engine_explained ruling on per-member rows (`202e59a0a`, made on the PObjectAccessor package):
- a row anchors the member's **distinguishing instruction**, the `lea rcx, [node]` at + 0x4;
- it states the **member-specific value**: the node, and the name at the node's qword `+0x8`, which is the key the
  registry insert compares;
- rows are grouped by the insert they call: channel 143, key 97, joypad button 44, type 25, axis 10;
- the shared shape is stated once in the lead and earns nothing.

## Verified

- [`fam_rows.py`](fam_rows.py) `check` derives all 319 rows from the certified image and compares them with
  [`rows.tsv`](rows.tsv), row by row: 319 / 319, FAILS 0.
  - A member whose body leaves the 32-byte form is refused.
  - So is a node, name or anchor that differs.
  - Two controls are refused: a swapped node and a moved anchor.
  - Every anchor lies strictly inside its body's census extent.
- `fam_rows.py apply` is idempotent (ALREADY on a second run).
- Gates on the page: `nb_page` adds nothing; `check_links` 0, `verify_doc_addresses` 0, `check_consistency` 0;
  `check_self_contradiction --db` clean.

## Effect

engine_explained moves from 17,841 to 18,158 of 35,065 (50.88% to 51.78%), measured with
`Tools/work/OPUS/ee_gap.py`, which reproduces progress.py's numerator exactly. Two members were already explained.

## Open conditions of the ruling

- **Condition 1:** OPUS is the page lead.
- **Condition 2:** this checker covers all 319 members, FAILS 0.
- **Condition 3:** progress.py should print engine_explained with and without template-family member rows. That is a
  progress.py change, and it is routed to the scorer's owner rather than made here.
