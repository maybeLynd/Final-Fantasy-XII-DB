# Correction: the `003EEEC0` interior row's state numbers (FABLE, 2026-10-03)

*FABLE, on SWE2-AUDIT-SPEC's REJECT of one row in `FABLE-REQ-AUDITSPEC-FABLE-UI-LAYOUT-PARAMETERS-AND-EDITOR-SCHEMA-CLOUDINT-1002`
(wave 5, published at `1f3005688`).* The cloud draft said byte `+0xC8` state "3 calls `003EEEC0`+0xB4 with `rcx`".
FABLE's own re-read passed it, and that was wrong.

**At the bytes.** The byte `+0xC8` dispatch runs as follows:
- `test ecx, ecx` / `je` (state 0);
- `sub ecx, 1` / `je` (state 1);
- `sub ecx, 1` / `je` (state 2, which stores 3);
- `cmp ecx, 2` / `jne` to the common `return 0`, at `003EEEC0`+0xA8.

After the two subtractions ECX holds state − 2, so the `+0xB4` call runs for state **4**. State 3, like 5 and above,
returns 0 without a call. AUDIT-SPEC's reading is correct.

**Edit.** In FABLE's interior table on
[ui-layout-parameters-and-editor-schema](../../../16-UI/Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md),
the clause is struck and replaced: "4 calls `003EEEC0`+0xB4 with `rcx`, and 3 or any other value returns 0". The other
clauses of the row and the page's other ten rows were accepted as exact.

**Lesson recorded.** In a re-read, count the `sub` steps of a decrement chain before naming the state a `cmp` matches.

## Consumer check (FABLE)

affected: `Database/FFXII TZA/16-UI/Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md`

- consumer: the ui-layout page's FABLE interior table: revised-here.
- consumer: the AUDIT-SPEC review record for this package: superseded by this correction (no other page cites the
  clause).

run: check.py at e548b7679 - executed regression over the byte +0xC8 dispatch (function offsets +0x93 .. +0xB4): states reaching the +0xB4 call = {4}; control with the `sub` steps ignored (the miscount) = {2}; FAILS 0
