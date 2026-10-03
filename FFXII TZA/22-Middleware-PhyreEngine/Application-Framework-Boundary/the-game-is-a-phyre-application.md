---
system: The game/middleware boundary — GameApplication is a PhyreEngine application
category: 22-Middleware-PhyreEngine
status: AUDITED
owner_layer: CodeDomain:Phyre.Framework + PrimaryOwner:CoreRuntimeScheduling
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN158 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN158 this document cites none of batch R109's 109; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
audit:
  passes: 1
  last_pass: 2026-09-02
  last_pass_state: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  crossref_clean: true
  reopened_count: 0
---

# The game/middleware boundary — `GameApplication` is a PhyreEngine application

> FFXII does not *use* PhyreEngine. FFXII **is** a PhyreEngine application: `GameApplication`
> derives from `Phyre::PFramework::PApplication`, and the middleware calls the game, not the other
> way round. The frame tick, the archive mount and the input pump are all game code filling in
> middleware slots.

## 1. What the player sees

When you launch FFXII, the thing that puts a window on your screen, notices your controller,
handles alt-tab, and drives one frame after another is **not FFXII's code**. It is Sony's
PhyreEngine framework. FFXII is a *plug-in* to it.

You can see the seam without a disassembler. The window behaves like a generic engine window
rather than a bespoke one. The controller handling knows about DirectInput pads, XInput pads and
**Steam Controllers** as three separate device kinds, because the framework has a class for each.
The game's own data — every texture, model and script — lives in one archive file,
`FFXII_TZA.vbf`, and the game mounts it by answering a question the framework asks at startup:
*"what data do you want?"*

That inversion is the whole point of this page. A modder's instinct is that the game is in charge
and calls the engine when it needs something drawn. **Here it is the reverse.** The framework owns
the loop and asks the game to fill in the blanks — 18 blanks, to be exact, out of 31. The other 13
FFXII leaves to the middleware entirely, and 3 of those are middleware functions that do nothing at
all.

The practical consequence: if you want to run code once per frame, or before the archive is
mounted, or when a controller is plugged in, **there is already a slot for it** and the game has
already filled it in. You do not need to find a loop to hook. You need to find which of the 31
slots you want.

## 2. Native mechanism

### The inheritance, established from the vtables

`GameApplication`'s vtable is at `008C5760` and has **31 slots**.
`Phyre::PFramework::PApplication`'s vtable is at `01CB2508` and has **31 slots**.

Equal slot counts are the first structural fact: a derived class's primary vtable is at least as
long as its base's, and equality means **the game adds no new virtual functions of its own** — it
only overrides. Comparing the two tables slot by slot:

| | slots |
|---|---:|
| **Overridden** — the game supplies a different function | **18** |
| **Inherited** — the slot holds the identical middleware function | **13** |
| of those, inherited slots that are a shared do-nothing stub | 3 |
| **Inherited real implementations** | **10** |

The three stub slots are slots 11 and 27, both `005C5230` (`NativeLeaf.ConstantReturn`), and slot
26, `0016D6A0` — the 3-byte `ret` documented in
[`../../24-Compiler-And-CRT-Runtime/Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md`](../../24-Compiler-And-CRT-Runtime/Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md).
So the middleware ships three virtuals that are empty by default and the game does not fill them.

### The proof that does not depend on RTTI at all: an override calling its base

Slot 6 of `PApplication` is `0079BF70`. Slot 6 of `GameApplication` is `0017CDC0`, whose complete
body is:

```c
void GameApplication_slot6(void *this) {
    FUN_0017d670();          // the game's own pre-step
    FUN_0079BF70(this);      // <- PApplication's slot 6, called directly
}
```

**The game's override calls the exact function that occupies the same slot in the middleware's
vtable.** That is `Derived::F() { extra(); Base::F(); }` compiled — a pattern that is only possible
if `GameApplication` derives from `PApplication`. It needs no RTTI, no destructor chain and no
adjacency; it is one 27-byte body.

Four more overrides tail into `005C5230`, the middleware's own constant-return stub, on their
fall-through paths — the same "do the game's part, then defer" shape.

### The three slots that matter most

**Slot 2 — mount the game's data.** `0017CEB0`, 120 bytes:

```c
undefined8 GameApplication_slot2(App *this, void *a, u32 b) {
    this[0x1130] = a;  this[0x1138] = b;      // remember what the framework handed us
    FUN_0059A770("../../..");                 // set the content root
    FUN_0019B190();
    h = FUN_0019B1F0();
    FUN_0019B070(h, "../FFXII_TZA.vbf");      // MOUNT THE ARCHIVE
    FUN_0017D6B0(b, a);
    FUN_00182F70(this[0xD24], this[0xD28]);
    return 0;
}
```

Two authored strings settle it: the content root `"../../.."` and the archive `"../FFXII_TZA.vbf"`.
**The framework asks; the game answers with its archive.** Everything the game later loads comes
through this one override.

**Slot 4 — the frame tick, and the startup latch inside it.** `0017CCD0`, 237 bytes, the largest
override. It reads a `double` at `this+0x48` (the frame's time), pushes it into a subsystem, and
then:

```c
if (this[0x113D] == 0) {          // a one-shot latch, in the tick
    FUN_0017D650();               // first-frame work, exactly once
    this[0x113D] = 1;
}
...
keep_going = FUN_0017D6E0(this[0x48], mode);   // mode 0 or 1 on three paths
return keep_going ? 0 /* via stub 005C5230 */ : 9;
```

*(Corrected 2026-09-14, FABLE: the comment here read "returns 0, 1 or 9". The tick returns only **0** or **9**
(`0017CD71`–`0017CDBC`). The `1` was the mode argument in `edx`, not a return value. See PA-2.)*

So the startup latch is not a separate mechanism — **it is a byte in the application object,
tested on every frame and set on the first one.** Everything gated behind "after the game has
really started" hangs off `this+0x113D`.

**Slot 7 — the input pump.** `0017CE50` reaches `InputManager_GetSingleton()` and drives it, and
falls back to the middleware stub otherwise.

### The overrides are dominated by input

The 18 overrides are one contiguous block of game code, `0017CC70`–`0017D210`, and by
classification:

| what the override is tagged | slots |
|---|---:|
| `Boundary.Input.NativeSupport` | 11 |
| `CoreRuntimeScheduling` (owner) / `Input` (owner) | 3 |
| `Thunk.InternalForwarder` | 2 |
| `CxxObjectLifecycle.DeletingDestructor` | 1 |
| `Boundary.CrossSubsystem.NativeSupport` | 1 |

**Eleven of eighteen are input.** That is what `PApplication` is *for*: it owns the window, the
device enumeration and the per-frame pump, and those are exactly the places a game must supply its
own behaviour.

Slot 0 is the deleting destructor `0017CC70`. ~~It is also the parent function of the `__std_terminate`
unwind funclet at `00861EAE` — so `~GameApplication` is a `noexcept` boundary.~~ *(pass 6, 2026-09-15, OPUS)* **Withdrawn
as evidenced.** The funclet-to-parent link exists only in the exception tables, which are banned as
evidence, and no instruction ties `00861EAE` to `0017CC70`. What remains is a LANGUAGE default,
not an observation of this binary: C++11 destructors are implicitly `noexcept`, so a throw that
escapes one is *expected* to terminate the process. Whether this build does so is not established
here. It is observable live, by throwing from a destructor hook.

### The framework cluster

Twelve vtables sit in `01CB2400`–`01CB2800`, and **all twelve are `Phyre::PFramework`**:

| vtable | class | slots |
|---|---|---:|
| `01CB2430` | `PInputDeviceKeyboard` | 6 |
| `01CB2468` | `PWindowWin32Base` | 2 |
| `01CB2480` | `PWindow` | 2 |
| `01CB2498` | `PApplicationScriptBuffer` | 1 |
| `01CB24A8` | `PApplicationScript` | 1 |
| `01CB24B8` | `PApplicationScriptProxy` | 1 |
| `01CB24C8` | `PInputDevicePad` | 7 |
| `01CB2508` | **`PApplication`** | **31** |
| `01CB2608` | `PApplicationViewport` | 5 |
| `01CB2638` | `PInputDevicePadDirectInput` | 7 |
| `01CB2678` | `PInputDevicePadXInput` | 7 |
| `01CB26B8` | `PInputDevicePadSteamController` | 7 |

Three pad implementations behind one 7-slot `PInputDevicePad` interface is the whole controller
story in one line — **DirectInput, XInput and Steam Controller are three drivers behind one
middleware interface**, and the game sees only the interface.

### Why the subsystem map found no game subsystem calling Phyre

[`../Subsystem-Map/phyre-subsystem-map.md`](../Subsystem-Map/phyre-subsystem-map.md) §11 records,
as a finding, that **no documented game subsystem calls Phyre** — the callers at the seam are 2,904
unowned edges. That measurement is correct and this document explains it: **the top-level control
flow runs the other way.** The framework calls the game through these 18 vtable slots. Looking for
game→Phyre calls at the top level finds nothing because the top level is Phyre→game.

It is not a contradiction of that document; it is the mechanism it was missing. Game code does call
Phyre, in quantity, *below* the entry points — but nothing needs to call Phyre to *start* the frame,
because Phyre starts it.

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `0017CC70` | `GameApplication::~GameApplication` (slot 0) | 92 B | deleting destructor; ~~a `noexcept` boundary~~ (C++ default only, not evidenced here) |
| `0017CEB0` | slot 2 — content root and VBF mount | 120 B | `"../../.."`, `"../FFXII_TZA.vbf"` |
| `0017CF30` | slot 3 — device/viewport setup | 150 B | installs a callback, defers to the stub |
| `0017CCD0` | slot 4 — **the frame tick** | 237 B | frame time at `this+0x48`, startup latch at `this+0x113D` |
| `0017CDC0` | slot 6 — pre-step then **base call** | 27 B | calls `PApplication` slot 6 `0079BF70` directly |
| `0017CE50` | slot 7 — input pump | 87 B | `InputManager_GetSingleton()` |
| `0017D090` · `0017D0C0` · `0017D120` · `0017D1A0` · `0017D210` · `0017D170` · `0017CDF0` · `0017CE20` · `0017D1E0` | slots 8, 9, 10, 15, 16, 22, 23, 24, 25 | 37–81 B | the input-facing overrides |
| `0017CFD0` | slot 21 | 36 B | nullable call-chain tail |
| `0017CDE0` · `0017D160` | slots 5, 14 | 5 B each | forwarding thunks |
| `0079BF70` | `PApplication` slot 6 | — | the base implementation the game calls |
| `005C5230` | `PApplication` shared stub | — | constant return; slots 11 and 27, and four override fall-throughs |
| `0016D6A0` | empty virtual (slot 26) | 3 B | the `ret` shared with the CFG check |

### Data addresses cited by this document

| Address | Name | Kind | Contents |
|---|---|---|---|
| `008C5760` | `GameApplication` vtable | `.rdata` | 31 slots |
| `01CB2508` | `Phyre::PFramework::PApplication` vtable | `.rdata` | 31 slots |
| `01CB2400`–`01CB2800` | the `PFramework` vtable cluster | `.rdata` | 12 vtables |
| `this+0x48` | frame time | `double` in the application object | read by the tick |
| `this+0x113C` | an enable/ready flag | `bool` | gates the tick and the input pump |
| `this+0x113D` | **the startup latch** | `bool` | set on the first tick, never cleared |
| `this+0x1130` / `+0x1138` | framework handles | pointer, `u32` | stored by slot 2 at mount time |

## 4. Data structures and formulas

### The complete 31-slot boundary

```
slot  0  OVERRIDDEN  0017CC70   deleting destructor        (Phyre: 00793EB0)
slot  1  inherited   0079F9E0
slot  2  OVERRIDDEN  0017CEB0   content root + VBF mount   (Phyre: 005C5230 stub)
slot  3  OVERRIDDEN  0017CF30   device/viewport setup      (Phyre: 005C5230 stub)
slot  4  OVERRIDDEN  0017CCD0   FRAME TICK                 (Phyre: 005C5230 stub)
slot  5  OVERRIDDEN  0017CDE0   thunk                      (Phyre: 005C5230 stub)
slot  6  OVERRIDDEN  0017CDC0   pre-step, then calls base  (Phyre: 0079BF70)  <- base call
slot  7  OVERRIDDEN  0017CE50   input pump                 (Phyre: 005C5230 stub)
slot  8  OVERRIDDEN  0017D090                              (Phyre: 005C5230 stub)
slot  9  OVERRIDDEN  0017D0C0                              (Phyre: 007A05D0)
slot 10  OVERRIDDEN  0017D120                              (Phyre: 005C5230 stub)
slot 11  inherited   005C5230   empty virtual
slot 12  inherited   007A0B10
slot 13  inherited   0079F140
slot 14  OVERRIDDEN  0017D160   thunk                      (Phyre: 007A0B40)
slot 15  OVERRIDDEN  0017D1A0                              (Phyre: 005C5230 stub)
slot 16  OVERRIDDEN  0017D210                              (Phyre: 005C5230 stub)
slot 17  inherited   007A0B30
slot 18  inherited   007A1180
slot 19  inherited   007A0AF0
slot 20  inherited   007A0FB0
slot 21  OVERRIDDEN  0017CFD0                              (Phyre: 00657140)
slot 22  OVERRIDDEN  0017D170                              (Phyre: 0016D6A0 empty)
slot 23  OVERRIDDEN  0017CDF0                              (Phyre: 0079D560)
slot 24  OVERRIDDEN  0017CE20                              (Phyre: 0079D5B0)
slot 25  OVERRIDDEN  0017D1E0                              (Phyre: 0016D6A0 empty)
slot 26  inherited   0016D6A0   empty virtual
slot 27  inherited   005C5230   empty virtual
slot 28  inherited   0079C140
slot 29  inherited   007A08A0
slot 30  inherited   0079E880
```

### The startup latch, exactly

```c
// inside the frame tick, slot 4, every frame
if (this->latch /* +0x113D */ == 0) {
    FirstFrameInit();            // 0017D650
    this->latch = 1;
}
```

There is no clear path. Once set, it stays set for the process lifetime.

### The archive mount, exactly

```c
SetContentRoot("../../..");                 // 0059A770
h = OpenArchiveContext();                   // 0019B1F0
MountArchive(h, "../FFXII_TZA.vbf");        // 0019B070
```

## 5. Call chain

```
process start
  -> CRT static initializers (1,172)
  -> main
     -> Phyre::PFramework::PApplication drives everything below
        -> slot 2  GameApplication  : set content root, mount ../FFXII_TZA.vbf
        -> slot 3  GameApplication  : device/viewport setup, install callback
        -> per frame:
             slot 4  GameApplication : FRAME TICK   <- corrected 2026-10-02, OPUS - order is slot 7 (0079C26B) then slot 4 (0079C2D6), then slot 9 (0079C526), the viewports (0079C5FE) and slot 8 (0079C655), once per call of slot 28 0079C140; 0079C140 makes no slot 6 call
                       -> first frame only: FirstFrameInit(), latch this+0x113D
                       -> FUN_0017D6E0(frameTime, mode) -> 0 / 1 / 9   <- corrected 2026-10-02, OPUS - the tick returns 0 (0017CD89, 0017CDA9 -> 005C5230) or 9 (0017CDB2); 0017D6E0 returns 0022A580's eax, 1 at 0022A594 or the mode body's
             slot 7  GameApplication : input pump -> InputManager_GetSingleton()
             slot 6  GameApplication : pre-step -> PApplication::slot6 (0079BF70)
        -> at a rate THIS DOCUMENT DOES NOT ESTABLISH:
             slot 8  GameApplication : THE RENDER PATH -> 00187950, the render pass list
                       (added 2026-09-13. Its base is the empty stub 005C5230, the same
                        one slot 4 overrides, so it IS a framework callback - but nothing
                        here shows it is called once per frame, and it is NOT listed above
                        with the three that are.)
        -> shutdown:
             slot 0  GameApplication : ~GameApplication  (a destructor: noexcept by C++ default, not evidenced here)
```

**Upstream (who causes this):** the PhyreEngine framework. There is no game-side caller of the
frame tick — that is the point.

**Downstream (what this causes):** the archive mount feeds the whole resource pipeline; the tick
feeds every per-frame system; the input pump feeds the input stack.

**Do not confuse with:**

- **Game code calling Phyre.** It does, extensively, below these entry points. The inversion
  described here is about the *top level* only.
- **`Phyre::PFramework::VPApplication`** (`01CB0D98` and friends) — that is the reflected *class
  descriptor* for the application type, not the application vtable. `VP*` names are reflection
  types; see the subsystem map §2.
- **The 145 CFG guard adapters.** ~~Slot 22 and 25 inherit `0016D6A0`~~ `PApplication`'s slots 22 and 25 hold `0016D6A0`, and the game overrides both *(corrected 2026-10-02, OPUS: `008C5760` slot 22 = `0017D170`, slot 25 = `0017D1E0`, against `0016D6A0` at `01CB2508` - the slot table above)*, which is the CFG check
  address only because empty functions were folded onto it.

## 6. Modding notes

- **Best intervention point: pick a slot.** The framework already calls the game 18 different ways.
  Replacing a pointer in the `GameApplication` vtable at `008C5760` is a cleaner hook than
  detouring a function body — it is one 8-byte write, it is per-object-type rather than global, and
  the original is right there to chain to.

- **For "once per frame", slot 4 at `008C5760 + 4*8`.** That is the real frame tick, and it already
  receives the frame's time as a `double` at `this+0x48`.

- **For "before any game data is loaded", slot 2.** It runs before `FFXII_TZA.vbf` is mounted at
  its first instruction and after it at its last. A mod that wants to add or redirect archives has
  a natural place to stand.

- **For "the game has really started", read `this+0x113D`.** One byte, set on the first tick. It is
  a cleaner readiness signal than timing a sleep, and it costs nothing to poll.

- **Chain, do not replace.** Slot 6 shows the engine's own idiom: do your work, then call the
  previous pointer. Four more overrides fall through to the middleware stub. A hook that never
  calls onward will silently disable whatever the middleware did there.

- **Breaks if:** you assume the vtable is writable. It is in `.rdata`; change page protection first.
  And treat `~GameApplication` as terminating on a throw: C++ makes destructors `noexcept` by default,
  so an exception escaping a destructor hook is expected to end the process. That is the language rule,
  not a verified property of this binary *(pass 6, 2026-09-15, OPUS)*.

- **XIIOnline.** The framework boundary is the most stable hook surface in the binary: 31 slots at a
  fixed address in a non-relocated image. It is also where "once per frame, on the main thread,
  after input" is available for free, which is exactly the shape a network tick wants.

- **Mod compatibility.** Two mods can share the vtable if both chain. Two mods that both *replace*
  the same slot will not.

## 7. What is not known

*Ids renumbered `BM-n` → `PA-n` 2026-09-12 (FABLE): the `BM` series was already registered on the
ledger by the animation-channel-binding page; these five were never registered and are now.*

- [x] **PA-1 — ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5): nothing in this build dispatches slots 10, 15, 16, 22, 23 or 24.**
  The application pointer was followed from all its sources:
  - the global;
  - the window procedure's `GetWindowLongPtrA`;
  - the static object;
  - `this` in all 62 methods;
  - its four stores, the script commands among them.
  Every vtable dispatch found hits other slots, and the control finds the four this box names below
  ([record](../../_index/candidates/pa1-application-slot-dispatch/README.md), `pa1_dispatch.py`). *Earlier state, kept:*
  What slots 8, 9, 10, 15, 16, 22, 23, 24 and 25 individually do. All nine are
  overridden and input-tagged; none has been read.
  *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror, PARTLY for slots 10, 15 and 16.* Three slots
  are named by **PhyreEngine's own error strings**. The framework's per-frame update is inherited slot 28 `0079C140`,
  and it logs a named failure after each call: `"App failed during animate"` (`01CB2E58`) after slot 4 (`0079C2D6`),
  `"App failed during resize"` (`01CB30C8`) after slot 9 (`0079C526`), and `"App failed during render"` (`01CB3130`)
  after slot 8 (`0079C655`). Per slot:

  | slot | framework role and call site | what the game's override does |
  |---:|---|---|
  | 8 | **render**, once per frame after the viewport renders (`[viewport]+0x18` over `+0xDC0`, logged as `"viewport render"` `01CB30F8`) | returns at once until the latch `+0x113C` is set, then runs the render pass list `00187950` on the renderer singleton `[01F7F598]` ([game application](../../00-Engine-Core-Runtime/Application-Root/game-application.md) §3) |
  | 9 | **resize**: on the first update (frame counter `+0x64` = 0, `0079C1E2`–`0079C1F1`) and after a screen-mode change refreshes `+0xD24`/`+0xD28` from `01F82D20` (`0079C4CE`–`0079C526`) | copies the app's `+0xD24` / `+0xD28` into the renderer singleton's `+0xAD8` / `+0xADC`, then calls the base resize `007A05D0` (`0017D0C0`–`0017D10C`) |
  | 10 | no framework call site found (see below) | sets byte `+0` of the renderer singleton `[01F7F598]` to 1, then returns 0 through `005C5230` (`0017D120`) |
  | 15 | no framework call site found | stores its byte argument at `InputManager` `+0x39` (`001989D0`), then returns 0 (`0017D1A0`) |
  | 16 | no framework call site found | `00227D40(byte)`: writes the byte to `01FD46DC` and 1 to `01FD46D8` between `0017ED20` and `0017F760`, then returns 0 (`0017D210`) |
  | 22 | — | the **pause flag** setter on the singleton `[01F810F0]` (`001997E0`); its game-side writer is the pause menu ([game application](../../00-Engine-Core-Runtime/Application-Root/game-application.md) §7, BE-2) |
  | 23 / 24 | — | the base's factor `min(short screen side, device +0x184 / +0x188) · 2 / short side` (`0079D560` / `0079D5B0`), times the UI width `0017E440` (console `+0x10D4`, default 640.0) |
  | 25 | called by the device poll `0079D010` (`0079D087`, `0079D107`, `0079D181`) whenever a polled device state byte changes, with `dl` = 0 or 1. The update calls the poll at `0079C260` only when its mode-change flags `+0x1E/+0x1F/+0x20/+0x21/+0x29` are all clear | stores the byte at `InputManager` `+0x38` (`00198E70`, `0017D1E0`) |

  **Still open for slots 10, 15 and 16:** *(answered: see PA-1, ANSWERED 2026-09-27 - nothing in this build dispatches slots 10, 15, 16, 22, 23 or 24; 2026-10-02, OPUS)* neither a displacement scan of the framework range 0x790000 up to 0x7A4400 (exclusive) nor a
  trace of every read of the global application pointer `02EA5368` found a call to them. Those scans cover only direct
  `[vtable + 8·slot]` calls through a register traced from that global, so a call through a copied pointer or from outside
  the range is not excluded.
  **NARROWED 2026-09-27 (OPUS): the two routes the 2026-09-14 scans did not take are now run, and neither calls 10, 15, 16, 22, 23 or 24. (1) The instance getter 00796E20 (mov rax, [02EA5368] / ret) is called from 106 sites image-wide. Following the returned pointer and its vtable at each, calls land on slots 12, 13, 14, 18, 19 and 25 (25 from game code 00197160), which is the positive control, and on none of the six. (2) The framework range 0x790000..0x7A4400 contains no indirect call at +0x50 / +0x78 / +0x80 at all, so no `this`-based call reaches 10 / 15 / 16 from the framework's own methods. The game's overrides of 10 / 15 / 16 (0017D120, 0017D1A0, 0017D210) are referenced only by GameApplication's vtable: no direct call and no other pointer. On every enumerated route the six slots have no caller in this build. Not claimed: a call through a copy of the application pointer held by another object. Control _index/candidates/pa1-slot-callers/pa1_slot_callers.py (C1-C4, FAILS 0).**
- [x] **PA-2** — The meaning of the frame tick's return codes `0`, `1` and `9`.
  *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror — **the premise was wrong: there is no 1**.* The
  tick `0017CCD0` returns **0** when the game step `0017D6E0` returns non-zero (a tail jump into the `xor eax, eax; ret`
  stub `005C5230`, `0017CD7F` / `0017CDA1`), and **9** when it returns zero (`0017CDB2`). `0017D6E0` returns the result of
  the frame entry `0022A490` (`0017D7ED`–`0017D7F2`, `0017D85D`). The framework treats any non-zero animate result as a stop:
  it logs `"App failed during animate"` and returns the code (`0079C2DB`–`0079C2F9`). **9 is the framework's own stop
  code:** the update returns 9 before calling any slot when its quit byte `+0x69` is set (`0079C1D0`–`0079C1DB`). The `1`
  was the mode argument the tick passes in `edx`.
- [x] **PA-3** — What `this+0x113C` gates. It is tested by both the tick and the input pump before
  they do anything, so it is a readiness or focus flag, but which is not established.
  *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror:* **readiness, not focus.** It has one writer
  and three readers image-wide ([game application](../../00-Engine-Core-Runtime/Application-Root/game-application.md) §2).
  The writer `0017D000` sets it last (`0017D074`), after building the game's render setup: it calls `0017D4C0` with what
  slot 2 stored at `+0x1130` / `+0x1138`, allocates the 0x80-byte object at `01F7E340` (`0018A840`), and calls `00189000`
  with the app's width and height. Nothing clears it. The three readers are animate, input and render (`0017CCD6`, `0017CE77`,
  `0017D094`). A focus flag would need a clearing writer, and there is none.
- [x] **PA-4** — Whether `PApplication` itself derives from further Phyre bases (`PBase`,
  `PMemoryBase` have been asserted by a peer session but are not verified here).
  *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror:* **yes — `PApplication : PBase : PMemoryBase`,
  single non-virtual inheritance.** It is read from the RTTI class hierarchy descriptors, not from the peer's assertion.
  `PApplication`'s (`01CEC0B0`) lists three classes with contained-base counts 2 / 1 / 0, and `GameApplication`'s
  (`01CEC020`) lists four with counts 3 / 2 / 1 / 0. All attributes are `0x40`, and `pdisp` is -1 throughout (no virtual
  bases). `PBase` and `PMemoryBase` have `mdisp` 8: their subobject sits 8 bytes in, after the vtable pointer.
  Instrument: [`members/rtti_bcd.py`](members/rtti_bcd.py); the global-pointer trace is [`members/global_vcalls.py`](members/global_vcalls.py).
- [x] **PA-5** — What the 13 inherited slots do, i.e. what behaviour FFXII takes from the
  middleware unchanged.
  *Narrowed 2026-09-14 (FABLE):* **slot 28 `0079C140` is the framework's per-frame update**, and the game inherits it
  unchanged. In order, it refreshes the window size when byte `+0x20` is set (`0079C167`–`0079C1C3`), returns 9 on the quit byte,
  runs slot 9 on the first frame, calls slot 30 when `+0xD98` is set (`0079C22B`–`0079C23A`), polls devices, then calls
  slot 7 (input, `0079C26B`), slot 4 (animate, `0079C2D6`), slot 9 again after a screen-mode change (`0079C526`), each
  viewport's render (`0079C5FE`) and slot 8 (render, `0079C655`). It runs the full-screen / window switch in between
  (its `"[Screen Mode]"` log strings, `01CB2E88`–`01CB3070`), and a non-zero result from any slot ends the frame. The
  run loop `00796490` calls it (`00796613`). Slots 11, 26 and 27 are the empty stubs. Slots 1, 12, 13, 17–20, 29 and
  30 ~~are not read~~ *(answered: see the ANSWERED 2026-09-26 block below - every inherited slot now has a behaviour; 2026-10-02, OPUS)*. Three more slots are called from the **framework's window procedure `00798FF0`**. It dispatches
  `msg − 1` through the table `00799788` (`007990D5`–`007990FD`); the import names below are from the import directory:
  - **slot 14** in the `WM_CREATE` arm, called with 1 when `GetForegroundWindow` (`008C2800`) returns the new window, which
    also sets the foreground byte `02EA5213` (`0079912E`–`0079914C`). The game overrides it with a thunk to the
    middleware's own slot-14 function `007A0B40` (`0017D160`). The input backend refreshes the same byte by the same test
    (`007A30AE`–`007A30C4`);
  - **slot 17** (inherited `007A0B30`) around a non-client mouse press. On `WM_NCLBUTTONDOWN` / `WM_NCRBUTTONDOWN` it is
    called with 1, and a thread mouse hook is installed (`SetWindowsHookExW` `008C2858` with id 7, `WH_MOUSE`, procedure
    `00798F80`; `007995A7`–`007995EC`). On `WM_NCLBUTTONUP` / `WM_NCRBUTTONUP` it is called with 0 and the hook removed
    (`UnhookWindowsHookEx` `008C2850`; `007995F8`–`0079962D`);
  - **slot 20** (inherited `007A0FB0`) on `WM_MOVE`, with no argument (`007993E3`–`007993ED`).

  Slot 1 is called once from `007980A0` (`00798542`), which is unread.

  **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): every inherited slot now has a behaviour.** The 2026-09-16 reading
  (below, *The seven unread inherited slots*) found that slots 12, 13, 18 and 19 only record a request. Their consumers
  are all in slot 28's per-frame update:
  - **Slot 12 (flag `+0x20`, mode byte `+0xD20`) is the screen-mode change.** It goes full screen when `+0xD20` is set
    and windowed otherwise, at the resolution in `+0xD24` / `+0xD28`, through the device's mode setter (`0079C3A6`–`0079C4C9`).
    When the switch reports success, the update sets `+0x1E` and `+0x23`. A failed full-screen switch logs *"Return
    to Window Mode"* and makes a window-mode fallback call.
  - **Slot 19 (flag `+0x22`) is a re-check of the monitor's mode**: *"Main Screen change"*, *"Monitor no change"*,
    *"Reset Screen Mode"* (`0079C30F`–`0079C39E`). Slot 19 skips one request after a successful switch, because
    `+0x23` is set then.
  - **Slot 13 (flag `+0x21`, argument `+0x26`) is the focus callback.** A two-way helper calls `ShowWindow` with 9 (restore)
    when the argument is set and 6 (minimise) otherwise, logging *"FocusCallBack RESTORE"* / *"MINMIZE"*
    (`0079C56C`–`0079C57B`).
  - **Slot 18 (flag `+0x29`, `+0x2C` / `+0x30`) is a resize** through the device's resize call with `+0x2C` and `+0x30`
    (`0079C57F`–`0079C5C8`).

  Read to their ends, slots 29 and 30 are the framework's **input playback and recording**:
  - **Slot 29** `007A08A0` returns 9 when `+0x69` is set. On its first call it runs slot 9 (vtable `+0x48`). It then
    counts frames at `+0x64` and hands off to the playback reader, whose commands are *"Frames"* and whose
    error is *"Unrecognised command %s(%s)"*.
  - **Slot 30** `0079E880` is called by slot 28 when `+0xD98` holds a stream, and returns `0x13` when it does not. For
    each input whose state changed, it formats one line `"%d:%s:%s:+:%d"`, frame number first, into a 255-byte buffer
    (`0079E9DB`–`0079EA03`). It hands that line and its length to `0059F450`, which writes through the stream's slot
    `+0x28` and advances its position (`0079EA1A`–`0079EA24`).

  So FFXII takes three things from the middleware unchanged: window-mode and focus changes deferred to the next
  frame, the frame loop itself, and an input record-and-playback facility. Control:
  `_index/candidates/pa5-inherited-slots/inherited_slots.py` (7 checks).

## 7a. Crossings into other subsystems — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

The framework boundary is where the game's other layers are first reached. The functions this page cites therefore
carry edges into five other subsystems, and each is named here with what the edge is.

### `007980A0` — the framework's start-up and message loop

**`007980A0` is the framework's start-up and message-loop body, and PA-5's *"unread"* is lifted for it.** `WinMain`
`007A3770` calls it under the crash-dump filter
([what the game asks Windows for](../../24-Compiler-And-CRT-Runtime/Runtime-Service-Surface/what-the-game-asks-windows-for.md)).
It runs these steps, in order:

1. `SetUnhandledExceptionFilter`, `ImmDisableIME` and `CoInitializeEx`.
2. **PlatformOnlineAchievements:** `SteamInternal_ContextInit`, then `SteamAPI_Init`. It then runs `0020CD30` and
   `008655E0` (`SteamAPI_RegisterCallback`), and finally `SteamAPI_RestartAppIfNecessary`, which is followed by `exit`
   when a restart is due (`00798116`–`0079814B`).
3. `007A0810`, a thread-safe static accessor for the object at `02EACC90`. That object's constructor, `008653B0`,
   registers four more Steam callbacks.
4. `0079FA00` builds `My Games\FINAL FANTASY XII THE ZODIAC AGE\<SteamID64>\`. It uses `SHGetFolderPathW`,
   `CreateDirectoryW` and the Steam-id string helper `001F3ED0`
   ([keymap.ini](../../15-Input/Binding-Profiles/keymap-ini-file-format-and-default-controls.md)).
5. `GameSettingConfig_InitDefaultsAndPath` and `GameSettingConfig_LoadOrCreateFile`, then the Steam language query
   `007A0C60`.
6. **Platform:** the resource lookup `0019A510` (`FindResourceW`), called twice before and twice after the
   single-instance mutex (`CreateMutexW` and `GetLastError`, with the two `MessageBoxW` exits).
7. The command line: `CommandLineToArgvW`, then `WideCharToMultiByte`.
8. Slot 1 (`00798542`).
9. **Platform:** `007979B0` (`GetSystemInfo`, `GetProcessAffinityMask`).
10. The module-init walker `005A08E0` ([the fifteen modules](../Subsystem-Map/the-fifteen-modules-registered-before-main.md)).
11. The `GetMessageW` / `TranslateMessage` / `DispatchMessageW` loop, bracketed by `SetThreadExecutionState`.

Teardown mirrors the start-up. It unregisters the Steam callbacks through `0020CD80` and `00865660`
(`SteamAPI_UnregisterCallback`), then calls `CoUninitialize` and the module shutdown walker `005A0840`. A separate tail
runs after `SwitchToThisWindow`: it builds a command line from `GetModuleFileNameA` and calls `CreateProcessA` and
`ExitProcess`. Which condition takes that tail is not read.

### The window procedure `00798FF0`

The window procedure reaches **Platform** `0079E700`, which resolves `OpenDesktopA` from `user32.dll` through
`LoadLibraryA` / `GetProcAddress`. It also calls `0019A510`. It reaches **PlatformOnlineAchievements** through
`007A0810`, the same Steam callback-object accessor.

### Slot 16 and `0017ED20`

`0017ED20` initialises the Phyre platform synchronisation object at `01F7F510` on first use, through **Platform**
`005CD0A0`, which reaches `CreateEventA` via `005CD0E0`. It then tail-jumps to `005CD370`. Slot 16's store sits between
`0017ED20` and `0017F760`, as the PA-1 table records.

### The game side of the frame

The frame adapter `0017D6E0` pumps the per-frame singleton set
([game application](../../00-Engine-Core-Runtime/Application-Root/game-application.md) BE-6). The ledger files most of
those updates under **Presentation**:

- the renderer singleton's update `00189CE0`;
- the pending-completion queue `001BDAC0`;
- the 1,828-byte update `001BC190`, which names `sphere_m_%d.dds.phyre` and `sphere_n.dds.phyre`;
- `001CC600`;
- the `"%d, %s"` formatter called at `0017D82C`.

It also calls the `MultipleDebugDisplay` update `001C2F50`, which is filed under **Developer**.

### Render slots and setup

- **Slot 8, `0017D090`.** Its render pass list `00187950` calls **Presentation** `00187550`, which writes
  `/capture.tga` through `fopen` / `fwrite`, and `0018B100`.
- **Slot 3, `0017CF30`.** It calls **Presentation** `0018D850`, the builder the graphics noise texture is reached from
  ([rng-streams](../../21-RNG-And-Determinism/rng-streams.md)).
- **The 0x80-byte object `0018A840`.** It calls **Presentation** `0061D9C0` (`PSamplerState`).

### The two **Audio** edges are a ledger defect

Slot 3 and the render pass list both call `00182E80`, and those are the two **Audio** edges. `00182E80` is a 41-byte
getter that returns `0x438` (1080) when `001DDAB0` yields nothing, and otherwise tail-calls `002256A0` on
`001DDAB0`'s result. It is one of the seven `PrimaryOwner:Audio` rows that the GFZ's own `SUPERSEDES` / `RECLASSIFY`
markers retract ([intentionally ownerless functions](../../00-Engine-Core-Runtime/Ownership-Boundary/intentionally-ownerless-functions-and-shared-scratch.md)),
so the label is not an audio dependency.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| `GameApplication` vtable at `008C5760`, 31 slots | recovered RTTI vtable table, `Tools/work/rtti/vtables.tsv` | 4 |
| `PApplication` vtable at `01CB2508`, 31 slots | same | 4 |
| 18 overridden, 13 inherited | slot-by-slot comparison of the two tables | 4 |
| 3 of the 13 are empty virtuals | slots 11, 27 target `005C5230` (constant return) and slot 26 targets `0016D6A0` (3-byte `ret`) | 1 |
| **An override calls its base** | complete body of `0017CDC0`: calls `0079BF70`, which is `PApplication` slot 6 | 1 |
| Slot 2 mounts `FFXII_TZA.vbf` | complete body of `0017CEB0` with the authored strings `"../../.."` and `"../FFXII_TZA.vbf"` | 1 + 2 |
| Slot 4 is the frame tick and carries the startup latch | complete body of `0017CCD0`: frame time at `this+0x48`, one-shot latch at `this+0x113D` | 1 |
| Slot 7 is the input pump | complete body of `0017CE50` reaching `InputManager_GetSingleton()` | 1 |
| 11 of 18 overrides are input-tagged | the V121 classification of each override target | 11 |
| Twelve `PFramework` vtables in `01CB2400`–`01CB2800`, including three pad drivers | the recovered vtable table, filtered by address range | 4 |
| ~~`~GameApplication` is a `noexcept` boundary~~ | ~~`0017CC70` is the declared parent of the `__std_terminate` unwind funclet `00861EAE`~~ withdrawn: an exception-table relation, banned as evidence *(pass 6, 2026-09-15, OPUS)* | — |

### What was inherited from a peer session, and what was re-derived

`repos-46` established the inheritance from a destructor-chain argument and an RTTI `mdisp = 0`.
**None of that is relied on here.** Every claim above was re-derived independently: the vtable
comparison from the recovered table, and the base-call proof from a function body that needs no
RTTI at all. Where the two agree, the agreement is worth something precisely because the routes
are different.

**One number did not reproduce.** The peer reported "18 of 31 virtuals supplied, 10 inherited". I
get **18 overridden and 13 inherited**, and 18 + 13 = 31 exactly, so 13 is the arithmetically
complete count. The difference reconciles cleanly rather than contradicting: **three of the 13
inherited slots hold do-nothing stubs** — two `005C5230` constant-returns and one `0016D6A0`
3-byte `ret` — so "10 inherited *implementations*" and "13 inherited *slots*" are both true of
different things. Recorded because a reader comparing the two documents would otherwise see a
discrepancy and have no way to resolve it.

~~`PApplication : PBase : PMemoryBase` is **not** verified here and is carried as BM-4.~~ **Corrected 2026-09-22 (FABLE): wrong id, and no longer true.** The id is **`PA-4`** — `BM-4` is the animation-channel-to-shader-parameter question and has nothing to do with this chain — and **`PA-4` is ANSWERED on this page (§7, 2026-09-14): `PApplication : PBase : PMemoryBase`, single non-virtual inheritance, read from the RTTI hierarchy descriptors.**

### The killer observation, and what happened when it was sought

**The claim most likely to be false is the inheritance itself** — two vtables with the same slot
count could be unrelated classes that happen to expose the same number of virtuals. The killer:
find the two tables sharing *no* function, which would mean no inheritance.

They share **13 of 31 targets outright**, and one of the 18 differing slots calls the other table's
function for the same slot. Coincidence is not available: an unrelated class cannot hold thirteen
identical function pointers at identical indices, and cannot have its slot-6 body call the other
class's slot-6 body.

**A second attack, on the direction of the relationship.** If `PApplication` derived from
`GameApplication` rather than the reverse, the shared pointers would look the same. It does not:
`0017CDC0` (game) calls `0079BF70` (Phyre), not the other way round, and a base cannot call its
derived class's override by direct address.

## 9. Related

- [`../Subsystem-Map/phyre-subsystem-map.md`](../Subsystem-Map/phyre-subsystem-map.md) — the
  tier-4 identity map; its §11 finding that no game subsystem calls Phyre is explained here.
- [`member-registration-and-the-recovered-field-schema.md`](../Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md) —
  the same boundary seen from reflection: which methods are published to script and which stay
  native.
- [`../../24-Compiler-And-CRT-Runtime/Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md`](../../24-Compiler-And-CRT-Runtime/Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md) —
  `0016D6A0`, and the `__std_terminate` funclet whose parent is slot 0.
- [`../../15-Input/Input-Stack/input-stack-device-channel-and-bindings.md`](../../15-Input/Input-Stack/input-stack-device-channel-and-bindings.md) —
  what the input pump feeds.
- [`../README.md`](../README.md) — category index.

## 10. Falsification pass — 2026-09-02

Against snapshot `46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2`.

**Attacked: the inheritance.** Killer: two vtables sharing no function. **Survived** — 13 of 31
targets are identical and slot 6's override calls the base's slot 6.

**Attacked: the direction.** Killer: the base calling the derived. **Survived** — the call goes
game → Phyre by direct address, which only works downward.

**Attacked: the peer's numbers, rather than inheriting them.** "10 inherited" does not reproduce;
the count is 13, and the difference is exactly the three do-nothing stub slots. Recorded in §8 as
a reconciliation, not as a contradiction, because both statements are true of different things.

**Attacked: "the frame tick is the frame tick."** Killer: it being an unrelated per-call handler.
It reads a `double` at `this+0x48`, contains a one-shot latch, and returns a small status code —
all three are what a tick looks like and none is what an initialiser looks like. Held, but the
identification rests on shape rather than on a caller, since **the caller is inside PhyreEngine and
was not read** *(answered: see PA-5 - the framework's per-frame update, inherited slot 28 `0079C140`, calls slot 4 at `0079C2D6`; 2026-10-02, OPUS)*. Stated as such.

**Not attempted, and therefore not claimed:** reading `PApplication`'s own body to confirm it calls
these slots in the order this document implies; and any runtime observation. ~~the `PBase` / `PMemoryBase` chain above `PApplication`, which is BM-4.~~ **Corrected 2026-09-22 (FABLE): that chain IS claimed — it is `PA-4`, answered in §7 from the RTTI hierarchy descriptors, and `BM-4` was the wrong id for it.**

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Save_Load_Settings — SERVICE.** `007980A0` on this page calls `FUN_001de050`, owned by that layer. What it reaches is a 293-byte initialiser that stamps `word[+0x658]` with `0x0101`, `dword[+0x44C]` with 1 and `byte[+0x65A]` with 1 before doing anything else; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Resource — shared helpers (SWE2-EC7 batch-147).** The `00792F10` entry's member helpers `005CC8A0` (member ctor at `+0x20`) and `005CD0A0` (final pass on the same member) are shared leaves whose callers live mostly in that layer (`00165F80`, `0019F490`, `0019F620`, `001D9400`, `0020B150`, `0020B2E0`, `00677450`) - resource code borrowing the same helpers; nothing on this page owns resource state.
- **CoreRuntimeScheduling - CLIENT and SERVICE (33 edges).** `0017D4C0`, `0017D650`, `0017D670`, `0017D6E0` (+11 more) are called by bodies filed to CoreRuntimeScheduling: `0017CCD0`, `0017CDC0`, `0017D000`, `0017D6E0`; `0017CCD0`, `0017CDC0`, `0017D000`, `0017D4C0` (+6 more) reach bodies filed to CoreRuntimeScheduling: `0017D4C0`, `0017D670`, `0017D6E0`, `0017D980` (+13 more) - shared machinery across the layer boundary, no shared ownership.
- **Input - CLIENT and SERVICE (42 edges).** `001989D0`, `00198E70`, `001F3ED0`, `0059F450` (+13 more) are called by bodies filed to Input: `0017D1E0`, InputManager_BuildKeymapPath (`00197EE0`), `001E0FB0`, `001E1100` (+8 more); `0017CDC0`, `0017CDF0`, `0017CE20`, `0017CE50` (+11 more) reach bodies filed to Input: `001967D0`, InputManager_CreateSingleton (`00198750`), InputManager_GetSingleton (`00198790`), `001989D0` (+13 more) - shared machinery across the layer boundary, no shared ownership.

## The seven unread inherited slots (FABLE, 2026-09-16)

**THE SEVEN ARE READ - 2026-09-16 (FABLE), and four of them share one convention.** **Four slots are the same shape: record the request, store the arguments, return 0.** **Slot 12** `007A0B10` (17 B) sets `byte[this+0x20] = 1` and `byte[this+0x1E] = 1`, then stores its argument at `byte[this+0xD20]`. **Slot 13** `0079F140` (10 B) sets `byte[this+0x21] = 1` and stores its argument at `byte[this+0x26]`. **Slot 18** `007A1180` (14 B) sets `byte[this+0x29] = 1` and stores **two** arguments at `dword[this+0x2C]` and `dword[this+0x30]`. **Slot 19** `007A0AF0` (17 B) is the consume side of the same idea: if `byte[this+0x23]` is zero it sets `byte[this+0x22] = 1`, otherwise it clears `byte[this+0x23]`. **So what FFXII takes unchanged here is a DEFERRED-REQUEST convention.** None of the four does the thing asked of it. Each sets a distinct flag byte - `0x20`, `0x21`, `0x29`, `0x22` - parks the parameters beside it, and returns success immediately. **The work happens later, wherever those flags are consumed.** That is a real behavioural inheritance rather than a list of addresses: **the game's application object answers *yes, noted* and defers**, because the framework's own implementation does. **Slot 1** `0079F9E0` (31 B) is different and simpler: a **composite initialiser**, four straight calls to `007943E0`, `00794E80`, `00795590`, `00795320`, then `xor eax, eax` and return. **`007943E0` (2,717 B) read 2026-09-17 (SWE2-FRONTIER): it is the application's script-method registration pass** — an unrolled battery of ~13 bindings, each a `cmp dword[02EAC3x0]` guard + `008092FC` register + name string (`GetApplicationForScript` `00794452`, `getWidth` `0079451C`, `getHeight` `007945E6`, `getTotalElapsedTime` `007946A9`, `getElapsedTime` `00794773`, `getFrameCount` `00794836`, `getWorld` `00794900`, `getInput` `007949CA`, `getInputMapper` `00794A94`, `getViewportCount` `00794B5E`, `getViewport` `00794C21`, `setCamera` `00794CEB`, `getDebugUtils` `00794DB5`) + `00632FB0` bind into record cells at `02EAC3A0`–`02EAC460`, each record carrying a vtable (`01CB3A28`, RTTI `01D3E828`) and its handler pointer (e.g. `00796E30` at `007944DA`). **`00794E80` (1,173 B) read the same day (SWE2-FRONTIER): the second of the four, same shape — `006388C0` registration at [`00794EAA`](../../_index/ADDRESS-INDEX.md), `008092FC`/`0080929C`/`00808B90` driver thunks ×5, display-side names `getAspect`/`getHeight`/`getWidth`.** **Slots 29 and 30 return framework status codes**: `007A08A0` (65 B) returns **9** when `byte[this+0x69]` is set before testing `dword[this+0x64]`; `0079E880` (792 B) returns **`0x13`** when `qword[this+0xD98]` is null. **A non-zero return here is a Phyre status, not a value** - which is why the four request-recorders all end `xor eax, eax`. **And the 13 inherited slots reproduce exactly**: 1, 11, 12, 13, 17, 18, 19, 20, 26, 27, 28, 29, 30, confirmed by comparing `GameApplication`'s vtable at `008C5760` against `PApplication`'s at `01CB2508` entry by entry. Slots 11 and 27 are `005C5230` and slot 26 is `_guard_check_icall` - **the three the page calls *empty*, which is right: they are the framework's own no-op and guard stubs, inherited because there was nothing to override.** *Partial reads, stated.* **Slots 29 and 30 are read at their prologues only** - the precondition and its status code - not to their ends; slot 30 is 792 bytes. And I have the flag offsets the four recorders write, **not their consumers**, so *the work happens later* is the shape of the convention and not a traced path.
*Completed 2026-09-26 (FABLE, Claude Opus 5.5): the four consumers are traced and slots 29 and 30 are read to their ends
(PA-5, §7).*

## Interior citation — frontier hub `006388C0` (2026-09-17, SWE2-EC7)

`006388C0` — 254 B, 16 A-measured callers at census; the `00794E80` path's "006388C0 registration"
call. Interior verified: it is a name-intern into the reflection registry. `rsi = [rcx+0x30]` is
the name; `call 00637440` fetches the registry object; the loop at
[`00638920`](../../_index/ADDRESS-INDEX.md)–`00638932` hashes the string as
`h = h*0x21 + (c & 0x1F)` seeded `0x7B5` (a case-folding djb2 variant — `&0x1F` strips the ASCII
case/upper bit); `call 006311D0(registry, &hash)` probes; on miss `call 0067F700(registry,
rbp+8)` inserts. Returns `sete` — true when the interned lookup/call succeeded.

NOT claimed: whether `+0x30`'s string is the class name or the member name at this call depth.


### Interior citation — frontier hub `0019A510` (2026-09-18, SWE2-EC7)

`0019A510` — 148 B, 5 callers, `FindResourceW` loop: for each class index
`1..N` it formats `"class%d"` through `0080C51C`, calls the `008C2108` IAT
slot with `(module, name, 6)` at [`0019A558`](../../_index/ADDRESS-INDEX.md),
and hands hits to `0019A5B0` — stopping at the first null result and
returning the last hit.
## SWE2-EC7-35 update (2026-09-19) - `0079E880`

`0079E880` (792 B) is ~~the INPUT-section config parser~~ *(corrected 2026-09-26, FABLE, Claude Opus 5.5, PA-5: the
input **recorder**, slot 30; it formats `"%d:%s:%s:+:%d"` lines and writes them to the `+0xD98` stream, and parses
nothing)* - `"IK"`/`"KB"`/`"INPUT"` magic constants and `"%d:%s:%s"` format strings, `0059F450`/`0019C5D0` triples plus `00873C40`/`00873C50`. Interior anchor `0079E992` (a `0059F450` call).

## SWE2-EC7-39 update (2026-09-19) - `0018A840`

`0018A840` (412 B) is the 0x80-byte object the page names - `01F82D20`, the `001DE540` SIMD leaf plus `0085E730`/`00615CD0`/`0061D9C0` (`PSamplerState`). Interior anchor `0018A86D` (the `001DE540` call).

## SWE2-EC7-39 update (2026-09-19) - `00187550`

`00187550` (395 B) is the `/capture.tga` screenshot writer - `01F44830`, `00186820` triple plus `008C2F40`/`008C2EF8`/`008C2F00` thunks and `00210EB0`/`00808C40`. Interior anchor `00187597` (an `008C2EF8` thunk call).

## SWE2-EC7-40 update (2026-09-19) - `0079E700`

`0079E700` (383 B) is a Phyre desktop body - the `01CB34C8`..`01CB3508`/`02EACD48`..`02EACD70` import block, `"CloseDesktop"`/`"Default"`/`"OpenDesktopA"`/`"SwitchDesktop"` strings, `008C2130` thunk triple plus `008092FC`/`0080929C` pairs and `02EACD70`/`02EACD68` imports. Interior anchor `0079E78F` (a `02EACD70` import call).

## SWE2-EC7-46 update (2026-09-19) - `008653B0`

`008653B0` (224 B) is the `02EACC90` singleton constructor - `008C3180` import calls x4, no direct calls. Interior anchor `008653E2` (the first import call).

## SWE2-EC7-51 update (2026-09-19) - `006311D0`

`006311D0` (177 B) is `PType_LookupByHashThenString` - call-free ordered-tree walk on `[rcx+0x18]` links: `u32` hash compare at `[r8+0x20]`, `strcmp` on a tie (the member-registration page files the complete body; this page names the call site). Interior anchor `00631200` (the walk loop head).

## SWE2-EC7-59 update (2026-09-19) - `0019A5B0`

`0019A5B0` (159 B) is an indirect-only string/alloc chain - `008C20E8`/`008C20F0`/`008C20F8` import calls, `and edi,0xF` bound fill loop. Interior anchor `0019A5EB` (the `008C20F0` call).


## SWE2-EC7-67 update - `007A0810`

`007A0810` (129 B) is the Steam callback-object static accessor - `008092FC`/`00808B90`/`0080929C` guard helpers, constructs `008653B0` into `02EACC90` (`02EAED3C`/`02EACD20`). Interior anchor `007A0849` (a `008092FC` call).

## SWE2-EC7-67 update - `008655E0`

`008655E0` (128 B) is the `SteamAPI_RegisterCallback` stub - `00210EC0` plus `call [008C3180]` (`01CCFCA0`/`02EB3860`, RTTI `01D499B0`). Interior anchor `008655F8` (a `00210EC0` call).

## SWE2-EC7-78 update (2026-09-20) - `007A0A80` startup toggle measured

`007A0A80` (104 B) is the `02EACD30` startup record setter:
`0079ED60(cl)` runs first, `02EACD30` gets `0x18`, the `008C2830`
CRT entry runs; then `bl != 0 && 02EACD34 == 0` calls `008C28C0(1)`
and sets `01F3DA06 = 1`, while `bl == 0 && 02EACD34 & 1` calls
`008C28C0(0)` and clears it - a one-way init/deinit switch driven by
the flag byte.
Interior anchor `007A0A95` (the `0x18` store).

## SWE2-EC7-80 update (2026-09-20) - `0059F450` vtable-gated add measured

`0059F450` (58 B) is the gated accumulator the Phyre callers run:
`call [rcx][0]+0x28` vets the object; a true return adds `r8d` to
`[rbx+0x18]` and returns 0, a false return gives 9.
Interior anchor `0059F463` (the virtual call).

## SWE2-EC7-111 update (2026-09-20) - `0019EB00` measured

`0019EB00` (89 B) is the
all-armed predicate
`001A9ED0`, `001BB120`,
`001BC190` and `001C0DD0`
run: `rdx` non-null and
`byte[rdx + 0x128]` armed
admit the scan, then every
8-byte element in the
`[+0x100]..[+0x108]` vector
must have `byte[elem + 2]`
nonzero - the first clear
byte short-circuits to 0, a
clean sweep answers 1.
Interior anchor `0019EB30`
(the element-fetch loop head).

## SWE2-EC7-112 update (2026-09-20) - `00873C50` measured

`00873C50` (27 B) is the
tagged-count vector index
`0079A120` and `0079E880`
run: `dword[rcx]` with bit 31
stripped is the bound, `edx`
inside it answers
`qword[[+8] + edx * 8]`,
outside answers 0 - the same
bit-31 capacity-tag
convention as `0060DF70`.
Interior anchor `00873C66`
(the indexed fetch).

`00873C40` (15 B) is the
packed-pointer decode
`0079A120` and `0079E880`
run beside it:
`byte[rcx + 8] & 1` is the
flag bit living under
`qword[+8]`'s low bit, and
the return is the pointer
minus that bit - alignment
makes the steal possible.
Interior anchor `00873C4B`
(the flag-strip subtract).

## SWE2-EC7-114 update (2026-09-21) - `007A3980` / `007A07C0` / `0079ED60` measured

`007A3980` (49 B) is the
six-way vtable install
`00793750`, `007980A0` and
`008A56A0` run on a new
object: the `01CB3EF8`
table (RTTI `01D3EEA8`,
slot 0 `007A39C0`) lands at
`+0x38`, `+0x58`, `+0x78`,
`+0x90`, `+0xB0` and `+0xC8`
while `qword[+0x30]` zeroes -
one interface stamped onto
six embedded sub-objects.
Interior anchor `007A398F`
(the first install).

`007A07C0` (74 B) is the
packed-field call `00798FF0`
runs: `005CD4F0` on the
`+0x20` block, then
`dword[+0x1C]` takes
`(edx << 0x10) | r8d` and
the tail jumps `005CD820`
on the same block - two
16-bit halves packed into
one field between the
helper pair.
Interior anchor `007A07EE`
(the `+0x1C` packed store).

`0079ED60` (110 B) is the
`02EA5248` window-state
refresh `007A0A80` calls:
on `cl == 0` the IAT imports
`008C29A0` and `008C28A0`
twice fill a stack rect/
point pair, then `008C28A8`
consumes them; on `cl != 0`
it runs `008C28A8(0)` alone -
one conditional read-apply
sequence over the same
global handle.
Interior anchor `0079ED87`
(the first `008C29A0` call).

## SWE2-EC7-115 update (2026-09-21) - `0079EC80` / `0079B190` / `0079B160` measured

`0079EC80` (214 B) is the
window z-order init
`00798FF0` and `007A3EE0`
run on `02EA5248`: IAT
`008C2800`/`008C2868`/
`008C21D8` fetch handles,
`008C2958` runs once, then
`008C2918` twice - first
with `rdx = -1`, then
`rdx = -2` (the
topmost/not-topmost
insert-after constants) -
before `008C28E0`, a second
`008C2958`, and a
`008C28E8` tail with
`edx = 1`. The
show-and-unraise sequence.
Interior anchor `0079ECEF`
(the first `008C2918` call).

`0079B190` (78 B) is the
paired window message
`00798FF0` runs: if
`0079EDD0([02EA5368])`
answers nonzero,
`005CDAA0(3, 01CB3340)`
logs, then IAT `008C28D8`
on `02EA5248` with
`rdx = [rcx+0x10]` and a
`008C2930` tail - a
send-then-post pair on the
window object.
Interior anchor `0079B1C5`
(the `008C28D8` call).

`0079B160` (43 B) sets
`byte[[02EA5368]+0x69] = 1`
and, when `byte[rcx+0x18]`
is clear, computes
`007A4190()` and tails
`007A42D0(result)` - a
flag-set plus conditional
dispatch on the
`02EA5368` object.
Interior anchor `0079B175`
(the `007A4190` call).

## SWE2-EC7-122 update (2026-09-21) - `006278B0` and `00624960` measured

`006278B0` (797 B) is the
renderer recreate
`007A05D0`/`006234A0`
call. `0017ECE0` and
`00180170` read the
environment, `+0x18A8`
takes `8 / count` when the
flagged path allows;
`+0x118` null exits 0x15.
`+0x110`'s
`vtable[+0x108]` stops the
old device, `0062B890`
drains `+0x480` and
`+0x4D0`, then `+0x118`'s
`vtable[+0x68]` recreates
with `+0x130`/`+0x148` and
the caller's `r15`/`r14`
dims; `vtable[+0x48]`
queries GUID `00D55438`
into the `+0x1A8` slot,
`+0x170` takes `02CF7480`,
`+0x198`/`+0x19C` copy
`+0x200`/`+0x204`;
`00620F60` rebuilds both
lists, `0060DD70(+0x2F8)`
re-routes and `+0x310`
clears bit 1 before
`00610990`; `0061D3D0`
then `00607D10` on
`+0x520` and `+0x548`
finish, with the new dims
stored at `+0x120`/`+0x124`.
Interior anchor `0062799B`
(the `vtable[+0x68]`
create).

`00624960` (32 B) is the
dims getter: `+0x120` to
`[rdx]`, `+0x124` to
`[r8]`, and `3 * +0x120`
to `[r9]` - the vertex
count triple the caller
wants alongside the two
dims `006278B0` writes.
Interior anchor `00624977`
(the `lea` of the triple).

## SWE2-EC7-123 update (2026-09-21) - the `005FD050`-device UAV/SRV array creators and the `00620F60` getters measured

The four flag-gated array
creators `00620630` and
`00620250` call all share one
shape: `005FD050` returns the
context whose `+0x108` is the
device object; the record's
`+0x30`/`+0x38` count
(bit-31 cleared) drives a
loop over inline-or-heap
records; each iteration calls
the device's
`vtable[+0x40]` (UAV) or
`vtable[+0x38]` (SRV) with
the record's `+0x10`/`+8`
out-field and a descriptor,
then `0061C550` names the
created view. `00620E10`
(333 B): `+0x98` bit-7 gate,
0x40-stride `+0x30` records,
`"PCubeMap_UAV"`. `00620CB0`
(340 B): `+0x80` bit-7 gate,
0x28-stride `+0x38` records,
`"PTexture3D_UAV"`.
`0061FC50` (333 B): `+0x98`
bit-3 gate, 0x40-stride
`+0x30` records,
`"PCubeMap_SRV"`. `0061FAF0`
(340 B): `+0x80` bit-3 gate,
0x28-stride `+0x38` records,
`"PTexture3D_SRV"`. A
negative create exits 9.
Interior anchor `00620F1E`
(the `PCubeMap_UAV` naming
call); interior anchor
`00620DC5` (the
`PTexture3D_UAV` naming
call); interior anchor
`0061FD5E` (the
`PCubeMap_SRV` naming call);
interior anchor `0061FC05`
(the `PTexture3D_SRV` naming
call).

The four getters `00620F60`
and `00622BA0` call are the
inline-or-heap vector
accessors on the same record
layout: `+0x30`/`+0x38` hold
the count with bit 31 as the
heap flag (`btr`), `edx` is
bound-checked against it, and
when count > 1 the element
comes from the `+0x38`/`+0x40`
heap array else the inline
slot at the same offset.
`00624270` (67 B): 0x58
records, returns `+8`.
`00624130` (71 B): 0x40
records, returns `+0`.
`006240E0` (65 B): 0x28
records on `+0x38`/`+0x40`,
returns `+0`. `00624090`
(65 B): 0x58 records,
returns `+0`. All return 0
out of range.
Interior anchor `00624292`
(`00624270`'s record fetch);
interior anchor `00624155`
(`00624130`'s shifted
fetch); interior anchor
`00624102` (`006240E0`'s
`*5*8` fetch);
interior anchor `006240B2`
(`00624090`'s `+0` fetch).

`00607D10` (12 B) is the
three-field setter
`006278B0` runs on `+0x520`
and `+0x548` at the end of
the recreate: `+0x18 = edx`,
`+0x1C = r8d`, `+0x20 = r9`.
Interior anchor `00607D17`
(the `+0x20` store).

## SWE2-EC7-124 update (2026-09-21) - `006105F0` and `00610420` measured

`006105F0` (52 B) is the
single-buffer release
`0079EDD0` runs: when
`[rcx]` is nonzero and not
bit-31-flagged and `+8`
holds a pointer, `00584730`
frees it; both fields are
cleared either way.
Interior anchor `00610611`
(the `00584730` free).

`00610420` (177 B) is the
state reset `0079EDD0`/
`008ADDE0` run: gated on
`+0x28` being 1 (after
`00610210` leaves it), it
sets `+0x28 = 2`, runs
`00609720`, `005CD330` and
`005C5230`, clears `+0x18`,
then 256 iterations of
`005CD700` clear the
`+0x40`+`i*0x28` records'
`+8` bytes, and two more
`005CD700` runs on
`+0x2840`/`+0x2850` clear
`+0x2848`/`+0x2858`.
Interior anchor `00610488`
(the per-record clear).

## SWE2-EC7-125 update (2026-09-21) - the atomic slot-claim measured

`00606600` (127 B) is the
lock-free slot claim
`00610210` uses: it reads
the 16-bit occupancy mask
at `+0x28A0`, picks the
lowest free bit with
`~mask & (mask+1)` (giving
up past bit 15), and tries
to claim it with a
`lock cmpxchg` - retrying
the whole pick on
contention. The claimed bit
index selects a record at
`+0x2860 + log2(bit)*0x10`;
if the record's `+8` byte is
still clear it runs
`005CD0E0` once and stamps
the byte, then `005CD500`
hands the record out. The
loop repeats until a claim
sticks. Interior anchor
`0060662F` (the
`lock cmpxchg`).

`00792F10` (306 B) is the priority and working-set tuner the start-up `007980A0` constructs early: after a normal object head (vtable `01CB2468`, arg2 stored at `+8`, member ctors `005CC8A0` at `+0x20` and `007A3810` at `+0x48`) it calls `GetCurrentProcess` and applies `SetPriorityClass` with `0x8000` (~~HIGH_PRIORITY_CLASS~~ `ABOVE_NORMAL_PRIORITY_CLASS` *(corrected 2026-10-02, OPUS: `00792F80 mov edx, 0x8000` before the call at `00792F85`; the Windows SDK defines `0x8000` as `ABOVE_NORMAL_PRIORITY_CLASS`, `HIGH_PRIORITY_CLASS` is `0x80`)*), fills a `GetSystemInfo` block and a 0x40-byte `GlobalMemoryStatusEx` report, reads the current working set through `GetProcessWorkingSetSize`, and when both bounds differ from -1 applies `SetProcessWorkingSetSize` with min = `dwPageSize * 50` (or the queried min when the query fails) and max = `ullTotalPhys - dwPageSize*512 - 1`; a final `005CD0A0` pass on the `+0x20` member completes the object.

Interior anchor `00792FBC` (function `00792F10`).

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-the-game-is-a-phyre-application-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00186820` | 30 B | returns `0x870` when byte `+0xDB8` of `rcx` is non-zero or dword `+0xC30` equals 3; otherwise returns dword `+0xADC` | `00186827`, `0018682C`, `0018682E`, `00186835`, `00186837` |
| `0020CD30` | 77 B | when qword `01F83450` is null, calls `00210EC0(0x80)` and, when that is non-null, `0020C730(result, 01DFE410, 0x29)`, then stores the last result (null when `00210EC0` returned null) to `01F83450`; when `01F83450` is already non-null it does nothing | `0020CD45`, `0020CD4C`, `0020CD59`, `0020CD6B`, `0020CD71` |
| `00793750` | 54 B | stores `01CB2468` to qword `[rcx]`, then calls `005CD6D0(rcx + 0x20)` and `007A3980(rcx + 0x48)` | `00793762`, `00793769`, `00793770`, `0079377A` |
| `00796E30` | 52 B | stores qword `02EA5368` plus 8 to qword `[rcx]` (0 when `02EA5368` is null) and qword `01F40120` (`0x02EA5660` in the image) to qword `+8`, and returns `rcx` | `00796E3A`, `00796E43`, `00796E47`, `00796E4A`, `00796E59` |
| `00798F80` | 105 B | when `ecx` is 0, `rdx` is `0x202` and byte `02EA5244` is non-zero, calls the import at `008C2820` with qword `02EA5248`, `0xA2`, 0, 0; then on every path tail-jumps through the import at `008C2848` with qword `02EA5258`, the incoming `ecx`, `rdx` and `r8` | `00798F99`, `00798FA2`, `00798FAA`, `00798FBE`, `00798FE2` |
| `0079F140` | 10 B | stores 1 to byte `+0x21` and `dl` to byte `+0x26` of `rcx` and returns 0 | `0079F144`, `0079F146` |
| `0079F9E0` | 31 B | calls `007943E0`, `00794E80`, `00795590` and `00795320` in that order (the first with the incoming registers, none with arguments set here) and returns 0 | `0079F9E4`, `0079F9E9`, `0079F9EE`, `0079F9F3`, `0079F9F8` |
| `007A0AF0` | 17 B | when byte `+0x23` of `rcx` is 0 stores 1 to byte `+0x22`, otherwise stores 0 to byte `+0x23`; returns 0 on both paths | `007A0AF2`, `007A0AF5`, `007A0AF7`, `007A0AFC` |
| `007A0B10` | 17 B | stores 1 to bytes `+0x20` and `+0x1E` of `rcx` and `dl` to byte `+0xD20`, and returns 0 | `007A0B14`, `007A0B16`, `007A0B1A` |
| `007A0B30` | 6 B | stores `dl` to byte `+0x28` of `rcx` and returns 0 | `007A0B33` |
| `007A0FB0` | 7 B | stores 1 to byte `+0x24` of `rcx` and returns 0 | `007A0FB4` |
| `007A1180` | 14 B | stores 1 to byte `+0x29` of `rcx`, `edx` to dword `+0x2C` and `r8d` to dword `+0x30`, and returns 0 | `007A1184`, `007A1186`, `007A1189` |

`001BF2E0` (1476 B) is the EASTL `basic_string` setup `001C0DD0` runs at the framework boundary: the `"EASTL basic_string"` type name feeds `001EDF00`, `008C2A40` CRT slots run, and `001A52A0`/`001A9E50`/`001A5760` build and compare name strings against the `".."`/`"color."` rdata constants around `008F9A54` before a `[rax+0x18]` vcall - the string-typed record construction the application root hands its subsystems.

Interior anchor `001BF666` (function `001BF2E0`).
