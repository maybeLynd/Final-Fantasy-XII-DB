# Ruling: an empty base that takes zero bytes (FABLE, Claude Opus 5.5, 2026-09-28)

**Request:** OPUS-REQ-FABLE-EMPTY-BASE-ROW. `PShaderProgramBase` has reflection instance size 1, and the store
embeds it as a 1-byte base row at `PShaderProgramD3D11 +0x0000`. But the D3D11 shader destructors treat
`+0x00..+0x07` as the class's own qword. How should the store write a base that occupies no bytes?

**The premise holds (E1, from the certified image's bytes; [`empty_base_check.py`](empty_base_check.py),
[output](empty_base_check.out)).** `00616880`, `00616900` and `0062BAB0` each load the qword at `+0`, test it,
call its vtable slot `+0x10` (IUnknown::Release, slot 2), and store 0 there. So `+0x00` is a COM pointer member,
not a vptr. The class is not polymorphic at `+0`, and under MSVC's empty-base optimization the empty base
subobject shares offset 0 with that member and takes no storage. A 1 is the size of a *complete*
`PShaderProgramBase` object, not of the base subobject inside this class.

## RULING

Write the empty base as a **zero-width row** that keeps both links the store uses:
- `offset` `0x0000`, `size` `0`;
- `name` `baseClass_PShaderProgramBase`, unchanged. `check_duplicate_declarations.py` reads inheritance from
  this prefix.
- `ctype` `PShaderProgramBase[0]`. This still names the type. `check_embed_parent_fields.py` PASS 2 requires a
  row naming a type to be that type's size times the count, and 1 × 0 = 0.
- `meaning` opens with `EMPTY BASE`. `types_index.py` reads a size of 0 as "no declared size", so the token is
  what separates zero bytes from an unknown width.
- The 8-byte member then takes its own row at `+0x0000`. Its name and ctype are OPUS's to choose.

**Checked on a scratch copy of the store (E2).** The ruled rows add no `types_index --validate` error and no
PASS 2 disagreement for the type: live 0 / 0, ruled 0 / 0.

**Controls (C).** Each alternative the ruling avoids is flagged:
- size 0 with the bare ctype `PShaderProgramBase`: PASS 2 reports a size disagreement;
- keeping the 1-byte base row under the 8-byte member: `types_index` reports an overlap.

**Scope.** This is the only size-1 base row in `fields.tsv`. The same form applies to any later empty base whose
derived class puts a member at the base's offset. It does **not** apply to a polymorphic derived class, where the vptr
is at `+0`, or to a base with its own members. OPUS applies it, and this record changes no store row.

Regression: `empty_base_check.py` (E1, E2, C). Run verified at 992ed9a3f: FAILS 0.

## v2 of the check (2026-09-28, FABLE, Claude Opus 5.5, on OPUS-NOTICE-FABLE-EMPTY-BASE-CHECK-C-STATE)

OPUS applied the ruling in `df6000099`. After that, v1's control C mutated nothing, because it matched the pre-ruling rows,
and printed FAIL. v1 and its output stay as published; they replay only at the revision they name.

[`empty_base_check2.py`](empty_base_check2.py) ([output](empty_base_check2.out)) finds the base row by type and name,
widens a pre-ruling 7-byte span at `+0x0001` to the member's 8 bytes, and builds every variant from whatever the store holds.
Its output records two runs, both FAILS 0:
- against the store at `b2e01af41`, with the ruling applied;
- against the store at `992ed9a3f`, before it (`TYPES_DIR`).

Regression: `empty_base_check2.py` (E1, E2, C). Run verified at b2e01af41: FAILS 0.
