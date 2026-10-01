# Orphaned 22-Middleware incorporations adopted, SD-62 brought to SWE2-ORACLE's answer, six SD scope narrowings: consumer check (SWE2-DATA, 2026-09-30)

For `OPUS-REQ-DATA-ADOPT-ORPHANS-22-0930`, `ORACLE-REQ-DATA-SD62-ROW-0930`, `ORACLE-REQ-DATA-SD7-ROW-0930`,
`ORACLE-REQ-DATA-SD107-ROW-0930` and `SWE2AUDITSPEC-REQ-DATA-SD-NARROWINGS-0930`. No new evidence is produced here.
Every sentence is taken from a published record, and each was read at HEAD before it was used.

affected: SD-62 (register row and the class-registers page's SD-62 text: `01F2E780` is not a list-headed record naming `PWorld` / `getInstanceCount`)
affected: 22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/how-a-class-registers-its-array-members-and-annotations.md
affected: 19-Save-Load-Settings/Game-Settings-Config/the-settings-command-table.md (section 4, the descriptor's `u8 id`; SD-22)

## 1. The orphaned page edits (adopted) (SWE2-DATA)

Three pages carried uncommitted SWE2-DATA edits from the stopped executor (FABLE session 73162e75, file times
12:56Z-13:48Z), incorporating OPUS's SD-60, SD-61, SD-63, SD-64, SD-65, SD-66 and SD-67 answers. The register rows
for those ids were restated at `583b096f7`. Each page claim was checked against its record:

| page | ids | record(s) checked | result |
|---|---|---|---|
| `the-camera-state-snapshot.md` | SD-60 | `sd60-gibegineff-blocks-0930` (`5f7bd30da`): `02AEEB20` / `02AEDD30`, `0024E180`, the floats `02AEEBA0` / `02AEEBA4` through `02B40470` by `0024FF60`, `00678B50`'s m22 / m32 formulas, `006CAF40`, dirty byte `+0x208F3`, `01FD3620`, `01FD3660` / `00210230` | every token is in the record; the page does not say `003820C0` calls `0024FF60`, so SWE2-AUDIT-SPEC's SD-60 narrowing (`auditspec-review-sd60-0930`) needs no page change, and the register row does not restate the float source either |
| `the-file-schema-against-the-runtime-schema.md` | SD-64, SD-65, SD-66, SD-67 | `sd64-file-only-names-0930`, `sd65-dynamic-class-route-0930` (35,984 files, `w7` bit 0), `sd66-attach-slot-writers-0930` (five bodies, 19 calls, `02CF8580`), `sd67-stream-bindings-type-0930` (`PSharray`, 16 B at `+0x38`) | agrees with the records and with the register rows at `583b096f7` |
| `how-a-class-registers-its-array-members-and-annotations.md` | SD-61, SD-62, SD-63 | `sd61-pannotation-fields-0930` ("WriteMask", `0x7FFFFFFF`, `00632960`, `006315B0`), `sd63-scene-parameter-layout-0930` (23 entries, `00D3EB38`, `02CB7DA8`), `sd62-static-array-elements-0930` | SD-61 / SD-63 agree; the SD-62 text is revised-here (section 2) |

## 2. SD-62: the earlier reading of `01F2E780` is replaced (SWE2-DATA)

OPUS's narrowing (`e2777d3c8`, F3) read `01F2E780` as a list-headed record naming the `PWorld` descriptor and
`"getInstanceCount"`. SWE2-ORACLE's [`sd62-registry-list-links-0930`](../sd62-registry-list-links-0930/README.md)
(`dedfaf0d7`) answers the chain residue and shows those two slots (`01F2E7C0` / `01F2E7C8`) belong to a separate
method record at `01F2E7B0`, linked into `PWorld`'s descriptor `+0x90` list by `00635B80`. `01F2E780` itself is a
0x30-byte name-hash tree of class descriptors. The regression is that record's `sd62_registry_lists.py` L5 + L6,
which reject reading the two slots as part of `01F2E780` (run: `sd62_registry_lists.py` at `0b6abcf18`,
FAILS 0, L5 and L6 PASS).

Consumers of the old reading:

- **Register row SD-62** - revised-here: ANSWERED on the ORACLE record, the old cell kept verbatim as history with a
  sentence saying which reading it replaces.
- **The class-registers page** - revised-here: the orphaned (never published) SD-62 sentence, the status line and the
  SD-62 box now carry the ORACLE answer; the section 9 "0x50-stride array" bullet gains the record's note that the
  objects from `01F2E780` up do not follow that stride.
- **`sd62-static-array-elements-0930`** (OPUS's record) - routed-to-OPUS: its F3 still carries the old reading; the
  ORACLE record already names it as the one it differs from. OPUS's record is OPUS's to annotate.
- A grep of the database for `getInstanceCount` finds no other page stating the old reading (outside this page, the
  register row, the ORACLE inbox and one dated `AUDIT-LOG` entry, which is history and is not edited).

## 3. The six SWE2-AUDIT-SPEC narrowings and the two ORACLE narrowings (SWE2-DATA)

Each register row gains, at the end of its status cell, the review's own "Correction wording for the row owner"
block (SD-4, SD-22, SD-25, SD-102, SD-107; reviews at `4dfe4a006`, verdict ACCEPT-WITH-NARROWING) or the ORACLE
record's "For SWE2-DATA" block (SD-7, SD-107). No status word changes: SD-4 / SD-22 / SD-25 / SD-102 stay ANSWERED,
SD-7 stays PARTIAL, SD-107 stays OPEN.

- **SD-22's page consumer** - the settings command table's section 4 `u8 id` (named by the review) - revised-here, as
  a dated scope note under the descriptor sentence.
- **SD-102's record modding line** ("drawn twice") - routed-to-OPUS: it is OPUS's record `sd102-glyph-emitter-commands-0930`.
- **SD-4's field-map correction** - agrees: the review asks for the scope sentence on "SD-4's answer and the field-map
  correction"; the answer is the register row (revised-here). The battle-unit field map's flag row 24 does not yet
  carry OPUS's writer correction (`sd4-unit-flag-bit24-0930`, "Correction for the field map"): it still names two
  setters and two clearers. Applying that correction with the review's scope sentence is the field-map owner's -
  routed-to-FABLE with both texts.
