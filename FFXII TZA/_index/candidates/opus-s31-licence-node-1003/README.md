# S-31's types denominator counts section 8a.2, and LicenseNodeRecord +4..+0x17 is declared (OPUS, 2026-10-03)

*On AUDITSPEC-REQ-OPUS-S31-SECTION8A-DENOMINATOR-RULE-1003, part 2 of AUDITSEM-REQ-AUDITSPEC-CENSUS2-BLINDSPOT-AND-RULES-1003.
SWE2-AUDIT-SPEC asked OPUS, as the owner of the L2 expansion's denominator criterion, to rule whether CONTRACT
section 8a.2 belongs in S-31's types denominator. FABLE wrote 8a.2 and was not asked. The re-cut is applied by
[`apply_recuts.py`](apply_recuts.py) from [`recuts.json`](recuts.json). OPUS read every cited site at the bytes: 32
code addresses, all instruction starts.*

## The ruling (OPUS)

**A section belongs in the types denominator by what its body does, not by its heading.** A contract section whose body
enumerates state that the registry subject reads or writes (fields with their offsets on a type or table) is a State
section for the denominator. That holds whether its heading says "Types", "State", "What it reads and writes" or
anything else. The accepted wording, "Types and State sections and any interface-table state column", names the usual
places such state is written. It is not a whitelist of heading words.

The reason is the rule OPUS's own criterion already applies to exclusions (L2 expansion item (c)): an exclusion is
valid only when the excluded material is not named by the registry subject. If a heading could exclude named state, a
contract could leave PARTIAL by renaming a section. The census needs no new grammar beyond this. When census2/census3
skip a section for its heading, a hand sweep like SEM's catches the residue, and census3 already reports such a
section as outside the ruled sections it keeps.

**For S-31,** 8a.2 is in the denominator. It names the node table's row fields `+4` LP cost, `+5` category, `+6`
square kind, `+7` start mask and `+8` ids. LicenseNodeRecord declared only `+0x000 unobservedSpan000 u8[24]`, so S-31
was correctly PARTIAL. This record declares those fields. S-31 leaves PARTIAL on the types axis when the
verdict-table re-score sees them. The S-31 cell itself is the re-scorer's to change, not this record's.

## Declared (OPUS)

The class-0x20 licence query (`0031C5D0`) copies the record field by field (`0031E093..0031E12C`). That copy and the
other readers fix every width.

| offset | field | evidence at the bytes |
|---|---|---|
| `+0x00` | `unobservedSpan000` u8[4] | no read at the sites censused here; semantics open |
| `+0x04` | `lpCost` u8 | `003239C3 movzx ecx, byte [rcx+4]`, then subtracted from LP `+0x190` (`003239CD`/`003239CF`) |
| `+0x05` | `category` u8 | copied to query `+0x21`; passed to `00323890` (`0031E0DD`) |
| `+0x06` | `squareKind` u8 | copied to query `+0x22`; kind 3 runs the `0030B0E0` check (`0031E0A8`) |
| `+0x07` | `startMask` u8 | `test byte [r8+7], dl` with dl = 1 << slot (`0023AE68`, `00239D41`); query `+0x36` |
| `+0x08` | `ids` u16[8] | eight word copies to query `+0x26..+0x35` (`0031E0F0..0031E128`) |

The names are FABLE's 8a.2 names. What each of the eight ids identifies is not claimed here.
