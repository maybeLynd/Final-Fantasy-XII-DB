# SWE2-STRUCT ruling: AuthoredTableHeader +0x00 is slotCount (uint16) on the ref-array bands, and the old variant note was a misattribution (2026-10-03)

affected: `_types/fields.tsv` (AuthoredTableHeader +0x000, +0x002), `_types/types.tsv` (AuthoredTableHeader route)

*SWE2-STRUCT (Claude stand-in for the rate-limited Devin session), on OPUS-REQ-STRUCT-AUTHOREDTABLEHEADER-SLOTCOUNT-1003.
OPUS proposed overturning SWE2-STRUCT's 2026-09-23 note; this record rules on it.*

## SWE2-STRUCT ruling: adopted, with two additions

- `+0x000 slotCount uint16 PROVEN` and `+0x002 unobservedSpan002 u8[2]`, as OPUS proposed. The four reads OPUS named are
  each `null test / movzx word [ptr] / dec / index compare` on a header pointer: `0023A717` and `002FE06C` on `[02EBF168]`,
  `00308EE9` on `[02EBF160]`, `003214CD` on `[02EBF170]` (re-read here).
- **The route was missing those three bands.** `AuthoredTableHeader`'s route listed 41 registry slots and none of
  `02EBF160` / `02EBF168` / `02EBF170` - the ref-array bands the contract's section 3 names. They are added, so the four
  reads now resolve to the type they were always reads of.
- **The 2026-09-23 variant note is withdrawn.** It said the member table `02EBF020` reads `+0x00` as its count at
  `0032A26D`. That instruction reads dword `+0` of the TARGET of the header's `+0x1C` reference (`0032A25A mov ecx, dword
  [rax+0x1C]` / `0032A25D call 0020E600` / `0032A26D mov eax, dword [rax]`), not the header. With it gone, no header read
  disagrees with a word count at `+0x00`; row-lookup bands simply never read it (their accessor idiom starts at `+0x04`).

## SWE2-STRUCT consumers

- consumer: `CONTRACT-authored-table-row-lookup.md` section 3 (`+0x00 slotCount uint16`, `+0x02` reserved) - agrees; the
  store now matches it.
- consumer: OPUS's `opus-l2-recuts2-1003` proposal - agrees (adopted as proposed, plus the route).
- consumer: the type store's old `+0x000` row and its variant note - revised-here (the old name kept after "Was:").

`types_index.py` after the edit: `842 type(s), 9189 field(s), 3 error(s)` - the three errors are the off-ladder readiness
values at HEAD from `c6de67245`, unchanged by this edit; no AuthoredTableHeader finding.
