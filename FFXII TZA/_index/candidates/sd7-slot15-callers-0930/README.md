# SD-7: who calls `GameApplication` slot 15 (`0017D1A0`)? (OPUS, 2026-09-30)

Register row SD-7 was registered by SWE2-DATA (`f7a3292bd`, input-stack-device-channel-and-bindings.md). Slot 15
forwards its byte argument to `001989D0`, the only other setter of the input manager's `+0x39` poll gate, and "the
caller of slot 15 is not identified". This record is static, over the certified image, with no execution and no live
run. Script: `sd7_slot15_callers.py`, output `sd7_slot15_callers.out`, control W PASS.

## Result (OPUS): narrowed, not closed

**No caller of slot 15 is found on any route by which code reaches the application. The Phyre framework cannot call it,
and nothing names the function except its own vtable entry.**

| test | result |
|---|---|
| vtable entries | `008C5760` + `0x78` = `0017D1A0`. The base vtable `01CB2508` has the shared stub `005C5230` at slot 15, so the framework's own class defines nothing there. |
| direct `call` / `jmp` to `0017D1A0` | none |
| aligned qwords in the image equal to `0017D1A0` | one: `008C57D8`, the vtable entry itself |
| any `call` / `jmp [reg + 0x78]` inside the Phyre framework range `00790000`–`007A8000` | **none**. The framework's application loop, window procedure and platform layer never dispatch through `+0x78` on any object. |
| every route the census follows to the application (below): slot calls reached | slots 1, 2, 3, 4, 5, 6, 7, 8, 9, 14, 17, 20, 25, 30 (callers in `out`) — **slot 15: none** |

The routes, each seeded as the object APP:
- **The static object:** the application lives at `01F7E350`. `0015BC40` constructs it there: `00792350`, then vtable
  `008C5760` stored at `0015BC61`.
- **The framework pointer:** the global `02EA5368`, stored by the base constructor at `00792550`. The window procedure's
  own slot calls go through it (`0079914C` slot 14, `007993ED` slot 20).
- **The window data:** `GetWindowLongPtrA` (import `008C2880`) results, from every caller (`00798FF0`, `007A03D0`,
  `007A04F0`), and `WM_CREATE`'s `lpCreateParams` in the window procedure. Both are taken as APP, an over-approximation.
- **The class itself:** `rcx` on entry to every method of the `GameApplication` vtable (30 methods).

Control W: the window procedure's documented calls to slots 14, 17 and 20 (`0079914C`, `007995C2` / `00799611`,
`007993ED`) are found.

## What remains (OPUS)

- **Holders the census does not follow:** 26 escapes of the application pointer into memory. These are back-pointers
  in the application's own sub-objects (`005DC1C0`, `005DC2F0`, `00607E20`, `006331A0`, `00874350`), a Phyre platform
  object's `+0x38` (`00792760`, `0079F150`), a game object reached from `[01F810F8]` (`0017CF30`), and two unknown
  destinations (`00796E30`). A game-side function that loads the application back from one of these and calls slot 15
  would not be seen.
- **Indirect calls receiving the application as an argument:** 34, listed in `out`.
- **All `+0x78` dispatch sites in the image:** 192, in 114 functions, all outside the framework range. None of them is
  on a route above. Each would have to be tied to its object's class to close SD-7 from this side.

So SD-7 is narrowed to one question: does game code call slot 15 through a stored application pointer? The framework,
the window procedure and the application's own methods do not.

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's
page.
