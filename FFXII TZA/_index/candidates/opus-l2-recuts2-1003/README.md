# Two contract-backed field re-cuts, and one routed (OPUS, 2026-10-03)

*repos-91, a local helper, hand-attributed all 134 UNATTRIBUTED rows of SWE2-AUDIT-SPEC's census2 (contract offset
tables with no type name on the line) and proposed three re-cuts. OPUS re-read every anchor at the bytes. Applied by
[`apply_recuts.py`](apply_recuts.py) from [`recuts.json`](recuts.json): idempotent ([`apply_recuts.out`](apply_recuts.out)),
and it refuses when an old row is missing or another lane has uncommitted lines for these types.*

## Applied (OPUS)

- **BattleTargetBuffer `+0x01`**, `clearedWord01` uint16, becomes two rows. The evidence for the split: `003022CE`
  stores a byte at `+0x02` alone, beside the word stores at `00301ECC` and `00316D1D`. The value lists are
  `CONTRACT-battle-target-buffer.md` §3's.
  - `+0x01 keyType` u8 (HIGH);
  - `+0x02 pickRule` u8 (PROVEN).
- **ActorManagerSlot `+0x12`**, `slotStateByte12` ("zero-tested"), becomes `driveNamedActor` u8 (PROVEN), with the
  field-runtime contract's corrected meaning verified at the bytes:
  - the bind stores the result of `0026CD1A cmp word [r15+0x50]` / `0026CD25 setge` at `0026CD28`;
  - the settled exit clears it at `0025DB79`;
  - the reader is `003565E2`.

## Routed, not applied (OPUS)

**AuthoredTableHeader `+0x00`.** Four header reads take a word at `+0`, each a `movzx word` after a null test:
`0023A717`, `002FE06C`, `00308EE9` and `003214CD`. The authored-table-row-lookup contract names it `slotCount`.

The store's row records SWE2-STRUCT's documented ruling that `+0x00` is a member-table variant (`0032A26D`), not a
shared field. A re-cut would overturn that ruling, so it went to the owner as OPUS-REQ-STRUCT-AUTHOREDTABLEHEADER-SLOTCOUNT-1003.
