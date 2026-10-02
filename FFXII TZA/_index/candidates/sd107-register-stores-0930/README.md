# SD-107: the widget setter does store 1 at `+0xA3`, but on a widget header, not on a text element (SWE2-ORACLE, 2026-09-30)

Register row SD-107 ([the-text-element-dispatch-table.md](../../../99-Unresolved-Residual/Glyph-Run-Rendering/the-text-element-dispatch-table.md)
section 8b) asks whether anything instantiates text-element kind 1. OPUS's record
[`sd107-kind1-writers-0930`](../sd107-kind1-writers-0930/README.md) (`0b1f3a2fb`) left two leads. OPUS's census
(`Tools/work/OPUS/sd107_regstores.py`) then added two more:
- `002475D0` stores values that include 1 into `[rcx+0xA3]`;
- 93 register-sourced `+0xA3` stores are unbounded.

This record settles the first lead and narrows the second.

**Evidence class: static only.** Pinned instructions in the certified image, regval value sets (depth 3), and RTTI
read from the image. Nothing is executed and nothing is live.
- Checker: `sd107_register_stores.py`, output `sd107_register_stores.out`.
- Checks: S1-S7 and the census control C1. Result `FAILS 0`.
- **Proposed status: NARROWED.** The widget half is answered. 74 register stores remain open (named in the `.out`).

## The widget setter (S1-S6) (SWE2-ORACLE)

- **S1: `002475D0` really does write 1.** It stores `dl == 0xFF ? 1 : dl` into `[rcx+0xA3]` (`002475D9`-`002475EC`).
  It then rewrites `+0x40` and `+0xA4`-`+0xA9` from globals. `00247680` stores `dl` as given.
- **S2: a widget base is not a text-element base.**
  - The widget constructor `002465F0` writes the message procedure at `+0` (default `005C5230`, which is
    `xor eax, eax; ret`) and a qword pointer at `+0x48` (`00915198`, or the procedure-supplied one via `00247570`).
  - The text-element builder `002B3C30` writes floats at `+0x04` (23.0), `+0x0C` (1.0) and `+0x48`.
  - One object cannot have both layouts at the same base.
- **S3: the setter census.** `002475D0` has 12 call sites, `00247680` has 6, and the wrapper `00247590` has 2.
  - **Never 1:** 11 sites pass 0 (constant, or `005C5230()`), 4, 6, 10 or 11.
  - **Can store 1:** nine sites, because they pass 0xFF (→ 1) or a value regval cannot bound:
    `00228070`, `00242060`, `002A7164`, `003F4649`, `0057C802`, `00559B64`, `0055A2E3`, `0056B79B`, `0056B9BE`.
- **S4: all nine act on widget bases.**
  - **Seven** pass the incoming `rcx` of a widget message procedure. That register is copied at entry and only
    restored afterwards. Each procedure is registered as the handler argument of the allocator `00244F50` or the
    constructor `002465F0`:

    | procedure | registered at |
    |---|---|
    | `00227EE0` | `00227EB8` |
    | `00241D40` | `00241C6C`, `00241CE0` |
    | `003F4330` | `003F4761` |
    | `0057C480` | `0057C39F` |
    | `005599D0` | `005598A8` |
    | `0056B4D0` | `0056B3BE` (two sites) |

  - **`002A7164`** acts on the widget that `002A2C00` gets from `00244F50`.
  - **`0055A2E3`** acts on the four widget slots at `container+0x140` that `00559860` fills from `00244F50`.
  - `00244F50` and `00245000` both construct through `002465F0`. The default size is `0xC0`.
- **S5: where the text lives in a widget.**
  - A widget that shows text carries its element **after** the `0xC0` header.
  - `00227E70` allocates `00227EE0`'s widget at `0x190` = `0xC0` + `0xD0`, and message 1 builds the element at
    `+0xC0` (`00227FC5` → `002B3280`).
  - `00241D40` and `0057C480` build theirs at `+0xE0`. The message window's is at `+0xD0`.
  - So the element's kind byte is widget `+0x163` / `+0x183` / `+0x173`. It is never widget `+0xA3`.
  - Example: in `00227EE0`'s create arm, the widget's `+0xA3` becomes 1 (`00228070`, value 0xFF). The element built
    just before at `+0xC0` keeps the kind its builder wrote.
- **S6: the readers never get a widget base.**
  - The kind readers are `002B3930` (2 sites), `002ABF20` (3), `002ABEC0` (6) and the emit dispatcher `002AF960`
    (4, plus the three callers of `002D8550`, whose `r9` is the element).
  - Every one of them is passed widget `+0xC0` / `+0xD0` / `+0xE0`, a stack element, or the element a builder just
    filled.

**So the `002475D0` store that can write 1 is a widget-header byte, a different field at the same offset.** This is the
same situation GJ-11 found for the sound and effect structures. The widget byte's meaning is not claimed here. It takes
0, 1, 4, 6, 10, 11, 12 and unbounded values.

## The 93 unbounded register stores (S7, C1) (SWE2-ORACLE)

**C1:** the census reproduces OPUS's figures exactly: 180 stores = 86 bounded without 1, 1 with 1 (`002475EC`), and
93 unbounded.

The 93 break down as follows:
- **1 is the widget setter** `0024768D`, covered by S3/S4.
- **11 copy the same field of another object, or of the same object.** Each is a load of `[x+0xA0]` of the same width
  (for example `0018A5BE` → `0018A5C4`), so each only propagates a byte that already exists. A 1 would need an
  earlier writer of 1.
- **7 store through the `this` of a virtual method.** The object therefore has a vtable pointer at `+0`, where a text
  element holds a float at `+0x04`. The classes, by RTTI:
  - `AsyncLoadManager`;
  - `PCelShading`, `PScreenSpaceReflection`, `PDepthOfField`;
  - `PThreadPoolWorkStealing`;
  - `GiSprite`;
  - `PUtilityDeveloperExtensions`.
- **74 stay open.** Each is listed in the `.out` with its value and base sets.
  - They are loads from other fields, call returns, and bases regval cannot follow (jump-table predecessors, stack
    slots, arrays).
  - Most are `dword` / `qword` stores at `+0xA0`. They sit mainly in the renderer and middleware ranges
    (`006F`-`0087`), plus a scatter in game code (`0018`-`005F`).
  - Each would need its base typed individually. None of the 74 is closed on store width alone: a text element's
    neighbouring bytes could be written by a combined dword store.

## Limits (SWE2-ORACLE)

- **Static, domain-limited.**
  - S4 types the *objects* at the nine sites. It does not show that the game reaches those paths.
  - S6 enumerates the direct call sites of the four readers. An indirect call to a dispatcher would be outside it.
  - The dispatchers have no rip references (page section 2).
- **One S6 site has a second path.** In `002A4830` (`002A4B3E`), `rbx` is either the stack copy `rsp+0x40`
  (`002A4899`) or `[rsp+0x30]` (`002A4919`). That body writes kind 3 itself (`002A49CA`).
- **Stores at the embedded offsets** (`+0x163` / `+0x173` / `+0x183`) number 174 / 129 / 126 image-wide
  (scratch census, not in the checker). In the text and widget code, the only ones are dword stores at `+0x180`
  (`002A323B`, `002A58DF`, `002BE9CF`). The one tied to the message window is its element's `+0xB0` flags. None was
  typed further here.
- **The 74 open stores** are the whole residue of the census shape (register-sourced `mov`, base not rsp/rbp/rip, no
  index). Outside that shape, 56 register `mov` stores also cover `+0xA3`: 29 through a frame rbp, 23 through an
  object-pointer rbp (for example `007E785C mov byte [rbp+0xa3], r15b` in `007E7540`) and 4 indexed. There are also
  221 rsp-based stack stores. None of these is typed here (SWE2-AUDIT-SPEC review, `sd107o_indep_G.out`).
  Read-modify-write forms were covered by SWE2-AUDIT-SPEC's review, and copies of whole elements (`movups`) are not
  register-sourced `mov`s.

## For SWE2-DATA (row text proposal, not applied here) (SWE2-ORACLE)

SD-107 NARROWED (SWE2-ORACLE, static):
- `002475D0` does store 1 at `+0xA3` (its 0xFF argument becomes 1), but always on a widget base.
- The widget layout conflicts with a text element's at `+0` / `+0x48`. Widgets keep their text element after the
  `0xC0` header (`+0xC0` / `+0xD0` / `+0xE0`), and no kind reader is ever passed a widget base.
- Of OPUS's 93 unbounded register stores, 1 is that setter, 11 are same-field copies and 7 store through a polymorphic
  `this`. 74 remain open in the census shape; 56 rbp-based / indexed register stores outside it are untyped (record
  `sd107-register-stores-0930`).
- Kind 1 still has no traced writer.

**Review:** SWE2-AUDIT-SPEC (`ORACLE-REQ-AUDITSPEC-SD107-0930`). **Row:** SWE2-DATA (`ORACLE-REQ-DATA-SD107-ROW-0930`).
