# RC-20: the script verbs the four Movement-filed float pushers serve (ORACLE, 2026-09-30)

## The question

RC-20 (registered 2026-09-30 by SWE2-CONTRACT from the pass-22 crossing on
`01-Script-VM-Native-Bridge/Party-Presentation-Verbs/the-party-standard-motion-verbs.md`): which script verbs do the
four Movement-filed bodies (88 to 233 B) that call `VMValueStack_PushFloat32Bits` (`00267F60`) serve?

## Method

[`rc20_verbs.py`](rc20_verbs.py), output [`rc20_verbs.out`](rc20_verbs.out). Static, shipping image `73461d08...`
(helpers: `../rc8-cascade-count-0930/img.py`).

1. Every raw `E8`/`E9` rel32 hit on `00267F60` in `.text`, kept only when it decodes as that call or jmp inside its
   `.pdata` chain-root function. The owner column of `Tools/work/graph/functions.tsv` gives the Movement-filed set.
2. Every route into each body: decoded callers and tail-jumps, 5-byte jmp thunks with or without a `.pdata` entry
   (followed transitively), and every qword in `.data`/`.rdata` equal to a body or a thunk.
3. The family tables are derived from `VMNativeCommandDispatch_InitializeFamilyTables` (`003DC2D0`): the default
   table is written into all 16 family slots, and families 0, 3, 5 and 7 are then overridden. Every slot of every
   record (`table + 8 + 32*N`: +0 begin, +8 poll, +0x10 unused, +0x18 result) is matched against step 2.
4. Verb names come from the authored ff12-script catalog (`CScriptContainerInitializers.cpp`), keyed by call id.

Controls, all PASS:

| control | what it checks |
|---|---|
| C1 | the Movement-filed callers are exactly four, sized 88 to 233 B (the crossing's own statement) |
| C2 | the decoded caller set of `00267F60` equals the `edges.tsv` caller set (38 functions, 58 sites) |
| C3 | family 0 resolves to `01EED700` (the dispatch page) |
| C4 | call id `0x0001`'s result slot is `0034EBC0`, catalog name `setpos` (`scriptvm-dispatch.tsv`) |
| C5 | the `.pdata`-less thunk `0033F850` (jmp `00349680`) is found |

## Result

**ANSWERED.** The four bodies are `begin` callbacks of seven family-0 movement verbs, and nothing else reaches them:

| body | size | verbs (call id, slot) |
|---|---|---|
| `003548B0` | 88 B | `rcmove` (`0x003E`, begin), `cmove` (`0x0059`, begin) |
| `003488B0` | 101 B | `rmove` (`0x0042`, begin), `move` (`0x005D`, begin) |
| `00349680` | 117 B | `ramove` (`0x04CE`, begin); `amove` (`0x04D2`, begin) through the thunk `0033F850` |
| `00345430` | 233 B | `ucmove` (`0x009A`, begin) |

- The only data references to the bodies and the thunk are those seven begin slots.
- No code calls or tail-jumps into any of them.
- No other family table holds them.

**What they push.** Each begin callback fetches one float, pushes it onto the script value stack with `00267F60`, and
then hands the stack to `VM_ActorSteerToPosition` (`00357A20`):
- `003548B0` tail-jumps to it (`00354903`).
- `003488B0` calls it and tail-jumps to `0026C120(actor, 2)` (`003488EF`, `00348910`).
- `00349680` calls it, then calls `00263F40` and `002EB430`, and tail-jumps to `0026C120(actor, 2)` (`003496BF`-`003496F0`).
- The float comes from `002640E0`: the acting actor's movement context (`[actor+0xB8]`) at `+0xE0`, or 0.0 when the
  actor is not kind 3 (`002640E4`-`002640F5`).
- `ucmove` (`00345430`) first resolves the party's current focus actor (`003590D0` then `003588B0`). It pushes
  `003590B0`'s value, which is `([022C7FF0] + 0.0 + [022C7FF4]) * [01CEBB70]`, and then calls `00357A20`.
- `ucmove` then finishes through `0026C120` and tail-jumps to `00269D80`. When there is no focus actor, it pops the
  arguments and returns (`003454F3`-`00345514`).

This matches the generated family "NativeAdapter.FloatFetchPushForward"
(`24-Compiler-And-CRT-Runtime/Generated-Families/members/nativeadapter-floatfetchpushforward.tsv`), which lists
`003548B0` among its members. The verb table TSV (`scriptvm-verb-table.tsv`) already records the same seven begin
columns, and this record re-derives them from the image.

## Not claimed

- **What the pushed float means.** Movement-context `+0xE0` has one displacement reader (`002640E0`) and no
  displacement writer in the movement-context census. The globals `022C7FF0`/`022C7FF4` were not typed.
- What `00357A20` does with it (presumably a speed or radius operand of the steer). The verb names come from the
  community catalog, not from the image.
