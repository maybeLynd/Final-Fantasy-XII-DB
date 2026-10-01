# PA-1 — nothing in this build dispatches application slots 10, 15, 16, 22, 23 or 24

FABLE, Claude Opus 5.5, 2026-09-27. **NATIVE/STATIC. Nothing was executed.** Control: `pa1_dispatch.py` (4 checks,
FAILS 0).

**The question.** PA-1 asks what the framework calls `PApplication` slots 10, 15, 16, 22, 23 and 24 for. Every
override body is read ([the Phyre application page](../../../22-Middleware-PhyreEngine/Application-Framework-Boundary/the-game-is-a-phyre-application.md)
§7). What was missing is the call site. The 2026-09-14 scan found none for 10, 15 and 16, but it covered only calls
through a register traced from the global `02EA5368` inside the framework range. A copied pointer, or a caller
outside that range, was not excluded.

**The answer: none of the six is dispatched in this build, by any route the pointer takes.** The application object
was followed from every source the image gives it. The tracker follows it through register copies and stack spills,
and into callees that receive it as an argument, to depth 4. It records every call or jump through its vtable.
- **The sources:**
  - the global `02EA5368` (published at `00792550`);
  - the window procedure's `GetWindowLongPtrA` result;
  - the static `GameApplication` object `01F7E350`;
  - `this` in all 62 methods of the two application vtables.
- **What it finds.** Dispatches of slots 1–9, 14, 17, 20, 25 and 30 (P1). That includes every framework call site the
  page already names, for slots 4, 8, 9 and 25, as the control. Slots 10, 15, 16, 22, 23 and 24 are dispatched
  nowhere (P2).
- **Where the pointer is stored (P3).** It escapes into memory in exactly four places:
  - the global;
  - a callback record whose callback (`0017D150` → `0017D000`) makes no virtual call;
  - `PApplicationScriptProxy` `+0x38`, twice. The script-command dispatch passes that copy to the 15 commands
    `007A0180` registers (`Frames`, `RenderFrame`, `Keypress` and the rest). Their virtual calls use only offsets
    `0x38`, `0x40` and `0xE0`: slots 7, 8 and 28.
- **The indexed indirect calls in the framework** (`0079A206`, `0079BE77`, `0079BF34`) are that same command-table
  dispatch: stride `0x50`, handler at `+0`.
- **One false lead, excluded (P4).** Three null-checked vcall thunks at exactly the offsets `+0x78`, `+0xB0` and
  `+0xB8` sit beside the application code (`0017F160`, `0017F1B0`, `0017F170`). Their one caller, `0053AB50`, passes
  `[r12+0x6B8]`, a `CharacterRenderObject`, not the application.

**So what they are for is what their bodies do, and nothing calls them.** The overrides are read on the page:
- slot 10 sets byte `+0` of the renderer;
- slot 15 stores its byte at `InputManager` `+0x39`;
- slot 16 writes `01FD46DC` / `01FD46D8`;
- slot 22 is the pause-flag setter (whose game-side writer calls it directly, not through the vtable);
- slots 23 and 24 return the two UI scale factors.

These are framework hooks this build defines and never invokes through the application's vtable. Whether the PS2 or
another platform's framework calls them is outside this image.
