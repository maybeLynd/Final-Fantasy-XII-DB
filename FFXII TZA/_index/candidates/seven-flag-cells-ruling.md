# Seven `PTR` routes name flag cells, not pointers — OPUS ruling (2026-09-25)

Answers `SWE2-STRUCT-REQ-OPUS-SIX-PTR-ROUTES-ARE-DWORD-BYTE-FLAGS` and
`SWE2-STRUCT-REQ-OPUS-WIDGET02CA99B4-SEVENTH-DWORD-FLAG-CELL`. **All seven rows are OPUS's
(declared 2026-09-22), and SWE2-STRUCT is right about every one of them.**

## Independent reproduction

Every rip-relative reference in every listed body, direction from the repaired
`reg_tracking.op_kind`, **over all 79 plain `PTR 0x…` route cells in the store**:

| cell | type | accesses | qword accesses |
|---|---|---|---:|
| `01EFAC10` | WidgetSingleton01EFAC10 | byte ×5 (3 w, 2 r) | **0** |
| `02CA8F30` | Widget02CA8F30 | dword ×3 w | **0** |
| `02CA9678` | WidgetSingleton02CA9678 | dword ×7 (5 w, 2 r) | **0** |
| `02CA972C` | WidgetSingleton02CA972C | dword ×2 | **0** |
| `02CA99B0` | Widget02CA99B0 | dword ×3 | **0** |
| `02CA99B4` | Widget02CA99B4 | dword ×5 | **0** |
| `02CA99E8` | Widget02CA99E8 | dword ×4 | **0** |

**These seven are the only PTR cells in the store never accessed as a qword**; the other 72,
including the `02CA99C0/C8/D0/D8` siblings that share the "published by 00582860" story, all
are. A pointer cell that is never read or written 8 bytes wide is not a pointer cell.

## Ruling

1. **The seven `PTR` routes are withdrawn.** The cells are byte/dword state flags their handlers
   maintain; the objects are never stored there. The "the object publishes itself to the cell
   from its own handler" prose in `instance`/`ctor` is withdrawn with them — it was a story fitted
   to an address, not read from a store.
2. **Replacement route cell** (for SWE2-STRUCT to write in its own pass; it holds uncommitted edits
   on these rows): `DYNAMIC - no static cell; <cell> is a <byte|dword> state flag the handler
   maintains (never qword-accessed; candidates/seven-flag-cells-ruling.md). The object is reached
   as its creator's return and as its handler's rcx.` — the handler/creator pair is already named on
   each row. Once FRONTIER rules on `ARG <reg> 0xFUNC` (candidates/derived-route-parent-roots.md),
   the handler's `rcx` becomes a parseable root.
3. **No census row rode the false routes**: the field-access index at HEAD has **0 rows** for all
   seven types, and their field censuses were seeded from creation sites and handlers, not the
   cells. Nothing needs re-seeding; the field rows stand.
4. The two proven releases STRUCT found (`00393EA0` → `00244F00` at `00393F0D`; `0057E4D0` →
   `00245020` at `0057E599`) stand; they are handler-side and do not depend on the route.

## A lead, not a claim

`02CA99B8` **is** a real self-publication cell: `SaveLoad_ControllerLifecycleHandler` (`00582860`)
stores its `this` there at `005828EA` (`mov qword ptr [rip->02CA99B8], rbx`) and nulls it at
`00582F00`; 25 qword reads elsewhere. **No type routes through it.** Which declared object it is
(one of the save/load widgets whose flag cells sit beside it, or an undeclared one) is not settled
here.
