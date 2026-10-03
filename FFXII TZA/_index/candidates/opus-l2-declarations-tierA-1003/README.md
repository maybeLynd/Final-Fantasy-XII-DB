# L2 Tier A: five contract-cited statics declared, two rows amended (OPUS, 2026-10-03)

*This continues AUDITSPEC-REQ-OPUS-L2EXP-REPAIRS-1003 item (a) for systems whose types cell was PARTIAL. repos-91, a local
helper, swept every NOT MET or PARTIAL system's contract-cited `.data` / `.bss` addresses against the type store and
drafted a package per gap. A non-drafting verifier re-read every row at the bytes; its fixes are folded in. Three
appliers, each idempotent ([`.out`](apply_decls.out) files beside them):
- [`apply_decls.py`](apply_decls.py) applies [`decls.json`](decls.json);
- [`apply_edits.py`](apply_edits.py) applies [`edits.json`](edits.json).*

## Declared (OPUS)

| type | system | what the bytes show |
|---|---|---|
| InitialPartySelectorTable01EED260 (9 B) | S-28 | an authored table read by `00329CC0`'s loop (byte reads, 9 entries; 0xFF, at most 0x27, other); image values 00 then eight FF |
| UiCanvasSize01E0C1D8 (8 B) | S-36 | the width/height int32 pair: `0024B120` stores 0x780/0x438 (else 0x200/0x1C0); about 330 readers |
| WidgetRateScale01E02820 (4 B) | S-36 | the float `0022A770` copies from `02064AC0`; reset to 1.0 by `00229E70`; read through that getter by eight callers |
| WeaponRecipeBlob (variable) | S-22 | two int32 lists, each ended by -1, read by `00385680` / `00385F60`; all 109 blobs re-parsed (`01EF9530..01EFA5BB`); route SLOTPTR `0x01EF96C0` stride 8 count 109 |
| StaticAiOrderSet (0x50) | S-25 | subgroupCounts u8[32] and AiOrderRecord[2]; the static sets at `01E09350` (set D via BattleUnit `+0x6F0`), `01EEC2D0`, `01EEC320`, `01EEC370`, `01EEC3C0` and `01EEC410`, walked by `00305CC0` and read by `0030BF20` |

**Edits:**
- WidgetMessage gains its static instance at `0x01E0C0F8` (id 0xF; sent by `00244DD0`). The verifier rejected a
  second type for it, because the store adds static instances to the existing layout.
- `WeaponRecipeRef.recipe` becomes `WeaponRecipeBlob*`.

## What the verifier changed (OPUS folded in)

- **WeaponRecipeBlob:** the route is SLOTPTR with stride and count, not PARRAY, and the ctype is `int32[]`.
- **StaticAiOrderSet:** `01EEC2D0`'s evidence is its store to `+0x6F8` at `00311DE1`. Two more instances are added,
  `01EEC3C0` / `01EEC410`, with the same layout, installed as set A by six functions.
- **WidgetRateScale:** all eight getter callers are named; `0032C910` stores the value instead of dividing by it.
- **UiCanvasSize:** the read is `00553CEC movsx`, not the function entry.

## Not declared (OPUS)

- **UiRequestMailbox0215F1A0 (S-36):** FABLE already proposes the same type in `fable-s36-router-repairs-1003`
  (`ac4d56247`), routed to SWE2-STRUCT. The helper's independent draft agrees with it, so OPUS adds nothing over
  FABLE's proposal.
- **S-45 `022C6D18` / `022C6D28` and S-28 `022BE974`:** these appear only in cross-layer notes, not as contract state.
