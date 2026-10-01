---
system: GameApplication — the application root, the VBF mount, and the startup latch
category: 00-Engine-Core-Runtime
status: AUDITED
evidence_tier: 1
owner_layer: CodeDomain — CoreRuntimeScheduling and neighbours; no PrimaryOwner
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN161 -> GN162 - REPLACED 2026-09-21 (OPUS), because the snapshot-identity basis this block carried is FALSE at GN162: this document cites record(s) 001D72F0 001D7A20 0024B580, which batch R30 touched. The weaker basis HOLDS and is measured: the advance changed 30 records in comment and tags ONLY - 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten (check_delta_additivity.py GN161 -> PARENT, control passed) - and check_stranded_absence.py, sweeping the GN160 resolved set which strictly CONTAINS all 30, reports no live absence claim on any line of this document
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
audit:
  passes: 4
  last_pass: 2026-09-02
  last_pass_state: be6-naming-repos-46
  crossref_clean: true
---

# GameApplication

**The root object of the running game** — a vtable of 31 slots at `0x008C5760`, an object of
**exactly `0x1140` = 4,416 bytes**, and **a PhyreEngine framework class underneath it**:

```
GameApplication  :  Phyre::PFramework::PApplication  :  Phyre::PBase  :  Phyre::PMemoryBase
```

FFXII's application root is a **PhyreEngine application** — the game supplies 18 of the 31 virtual
methods and inherits the other 10 from the middleware. §11.

*(This headline first read "an object of at least `0x1140` bytes, and **no deleting destructor at
all**, because the application is never deleted." Slot 0 is a deleting destructor and it states the
size. §10.)*

## 1. What the player sees

**The moment the game finds its data.**

Slot 2 is where FFXII opens `FFXII_TZA.vbf` — the single archive holding essentially every asset in
the game. Everything a player ever sees comes through that mount, and it happens once, here, at
startup.

And a few instructions later a single byte is set that the rest of the application waits on. **Three
of `GameApplication`'s vtable entry points check that byte in their first few instructions and return
if it is clear.** Before it is set the application object exists but does nothing; after it is set it
never goes back. That byte is the boundary between "the process is running" and "the game is running".

## 2. Native mechanism

### The archive mount (slot 2)

```
0017CEB0   120 bytes
   references  '../FFXII_TZA.vbf'
   references  '../../..'
   touches     +0xD24, +0xD28, +0x1130, +0x1138
```

A 120-byte method holding a relative archive path and a three-level parent traversal — the game
locates its archive relative to the executable rather than from a configured root.

### The startup latch at `+0x113C`

Enumerated across **the whole image**, not just this class's methods:

```
W  0017D074   inside 0017D000, +116 bytes in    mov byte ptr [rbx + 0x113c], 1
R  0017CCD6   inside 0017CCD0, +6   bytes in    cmp byte ptr [rcx + 0x113c], 0     (slot 4)
R  0017CE77   inside 0017CE50, +39  bytes in    cmp byte ptr [rbx + 0x113c], 0     (slot 7)
R  0017D094   inside 0017D090, +4   bytes in    cmp byte ptr [rcx + 0x113c], 0     (slot 8)
```

**One writer, three readers, image-wide.** It is set to 1 and never cleared, and every read sits at
the head of its method. **A one-way "initialised" latch**, established from access asymmetry and
position — not from its offset, its neighbours, or any name.

This is the **second** independent instance of this exact idiom found in the game's own classes; the
first is `CharacterRenderObject`'s `+0x4B4`
([character render object](../../17-Presentation-Rendering/Character-Rendering/character-render-object.md)).
Two unrelated classes, the same pattern: **one write at the end of setup, every read at method entry.**

### `+0x113D` is a different thing that looks the same

```
R  0017CD1E   inside 0017CCD0, +78 bytes in     cmp byte ptr [rbx + 0x113d], 0
W  0017CD31   inside 0017CCD0, +97 bytes in     mov byte ptr [rbx + 0x113d], 1
```

**Both accesses are inside slot 4**, read then set, nineteen bytes apart. Same idiom, **different
scope**: this is a run-once guard local to one method, not a class-level state flag. The adjacent
offset invites conflating the two; the access sets say they are unrelated.

## 3. Key addresses

**The vtable is at `0x008C5760`.** The document did not state it until §10; every row below is read
from it.

| slot | address | note |
|---:|---|---|
| 0 | `0017CC70` | **scalar deleting destructor** — states the object size, §4 |
| 2 | `0017CEB0` | **VBF archive mount** — `'../FFXII_TZA.vbf'` |
| 4 | `0017CCD0` | largest slot (237 B), `CoreRuntimeScheduling` — **the frame tick**, §5 |
| 5 | `0017CDE0` | 5-byte thunk to the `xor eax,eax ; ret` stub — an **explicitly empty override** |
| 7 | `0017CE50` | reads the latch; calls `InputManager_GetSingleton` |
| 8 | `0017D090` | reads the latch — and **everything reachable below it is the render path**: its only callee is the render pass list `00187950`, whose scopes are `"update shadowmap"`, `"Post Process : color correction"`, `"resolve render targets as default"` ([what the console tunes](../Developer-Tuning-Console/what-the-console-tunes.md) §7). `PApplication`'s own slot 8 is the empty stub `005C5230`, so this is a **framework callback the game overrides**, exactly as slot 4 is (2026-09-13) |
| 21/22 | `0017CFD0` / `0017D170` | a matched pair |
| 23/24 | `0017CDF0` / `0017CE20` | a matched pair |
| — | `0017D000` | **the only writer of the latch** |

*(Slot 5 was published as `0017CE40`, which is not a function — it is a mid-body address inside slot
24. Slots 23/24 were published as `0079D560`/`0079D5B0`, which are slots 23 and 24 of the **base
class's** vtable, not of this one. §10.)*

| | |
|---|---|
| vtable slots | 31 — **18 overridden, 10 inherited from the base at `0x01CB2508`, 3 shared stubs** |
| highest field observed | `+0x113D` (the guard byte in §2) |
| object size | **`0x1140` = 4,416 bytes, stated by slot 0** |

## 4. Data structures and formulas

### The object is exactly `0x1140` bytes, and slot 0 says so

Slot 0 is a textbook MSVC scalar deleting destructor:

```asm
0017CC89  lea   rax, [rip + 0x748ad0]      ; -> 008C5760, this class's vtable
0017CC90  mov   qword ptr [rcx], rax       ; re-install it, then destroy members/base
0017CC93  call  0x793250                   ; the BASE destructor - installs 01CB2508 at [rcx]
0017CC99  test  dil, 1                     ; bit 0: "delete this"
0017CC9D  je    0x17ccbe                   ; clear -> just return this
0017CC9F  test  dil, 4                     ; bit 2: use the sized form
0017CCA3  jne   0x17ccb0
0017CCA5  mov   rcx, rbx
0017CCA8  call  0x584730                   ; operator delete(this)
0017CCAE  jmp   0x17ccbe
0017CCB0  mov   edx, 0x1140                ; <<< the size
0017CCB5  mov   rcx, rbx
0017CCB8  call  0x16d6a0                   ; operator delete(this, 0x1140)
```

**`mov edx, 0x1140` is the size operand of the sized `operator delete`.** The compiler emitted the
object's size, so it is *stated by the code*, not merely bounded from below — and it happens to equal
the previously published lower bound exactly. **`0x1140` = 4,416 bytes. BE-4 answered.**

**A caution about the callee, not the size.** `0x0016D6A0` is three bytes — `ret 0` — with **2,479 distinct callers (2,867 call sites; 2,511 functions reference it at all, 1,515 of those through data pointer slots)
callers**. It is an `/OPT:ICF` fold: a stubbed sized-delete and a stubbed CFG check are both a bare
`ret`, so the linker merged them and the name Ghidra shows reflects one of its roles, not this one.
**Nothing about the callee is claimed here.** The size immediate is emitted by the compiler at the
call site and is independent of what the target turned out to be folded with.

### `GameApplication` has a base class

`0x00793250`, called from slot 0 immediately after this class's vtable is installed, writes
**`0x01CB2508`** into `[this + 0]`. Installing a *different* vtable at offset 0 during destruction is
what a base-class destructor does, so **`0x01CB2508` is the vtable of `GameApplication`'s base**.

That vtable also has **31 slots**, and **all 10 of the non-stub slots this class does not override
appear in it at exactly the same slot index** — 1, 12, 13, 17, 18, 19, 20, 28, 29, 30. Identical
indices across two vtables is the signature of **inheritance**; `/OPT:ICF` folding would place a
shared body at arbitrary, unrelated indices. **BE-3 is answered in substance:** those slots are not
"folded and invisible", they are inherited and fully visible in the base vtable.

**The base is `Phyre::PFramework::PApplication`** — read from the RTTI complete-object-locator at
`0x01CB2508 - 8`. The full chain, from `GameApplication`'s own class-hierarchy descriptor:

| base | `mdisp` | meaning |
|---|---:|---|
| `.?AVPApplication@PFramework@Phyre@@` | **0** | the primary base — which is why its vtable is the one installed at `[this + 0]` |
| `.?AVPBase@Phyre@@` | 8 | a second subobject at offset 8 |
| `.?AVPMemoryBase@Phyre@@` | 8 | its base in turn |

`mdisp = 0` for `PApplication` independently confirms the destructor-chain reading above: a primary
base at offset 0 is exactly the one whose vtable a base destructor writes to `[this]`.

**The `.rdata` neighbourhood is not "input devices" — it is the PhyreEngine framework's own vtable
region**, and the input-device classes are siblings in it rather than relatives:

```
01CB2430  Phyre::PFramework::PInputDeviceKeyboard
01CB2468  Phyre::PFramework::PWindowWin32Base
01CB2480  Phyre::PFramework::PWindow
01CB2498  Phyre::PFramework::PApplicationScriptBuffer
01CB24A8  Phyre::PFramework::PApplicationScript
01CB24B8  Phyre::PFramework::PApplicationScriptProxy
01CB24C8  Phyre::PFramework::PInputDevicePad
01CB2508  Phyre::PFramework::PApplication          <- GameApplication's base
01CB2608  Phyre::PFramework::PApplicationViewport
01CB2638  Phyre::PFramework::PInputDevicePadDirectInput
01CB2678  Phyre::PFramework::PInputDevicePadXInput
01CB26B8  Phyre::PFramework::PInputDevicePadSteamController
```

**BE-5 answered.** The 10 inherited slots are `PApplication`'s own implementations that
`GameApplication` does not override.

## 5. Call chain

```
startup
   -> slot 2   0017CEB0   mount ../FFXII_TZA.vbf   ('../../..' + '../FFXII_TZA.vbf')
   -> ...
   -> 0017D000            mov byte [this+0x113c], 1     <- the latch closes
   then, each gated on +0x113c:
      slot 4  0017CCD0    the frame tick
      slot 7  0017CE50    -> InputManager_GetSingleton
      slot 8  0017D090
```

### What slot 4 drives — BE-1

```
slot 4  0017CCD0
   |  if (this[0x113C] == 0) tail-jump to the empty stub          <- the latch gate
   |  dt = (float)(double) this[0x48]                             <- a double: the frame delta
   |  ... publish dt through a singleton pair, read a mode byte
   |  if (this[0x113D] == 0) { call 0017D650; this[0x113D] = 1; } <- the run-once guard
   +-> 0017D6E0   (404 B, CoreRuntimeScheduling)   called on ALL THREE paths, with
       |                                            this[0x48] in xmm0 and a mode in edx
       +-> 37 callees: 16 are 8-10 byte singleton getters, each followed by a
           substantial update body. The one named pair proves the shape:
              001C18E0  SaveloadManager_GetSingleton          (8 B)
              001C1910  SaveloadManager_ProcessPendingCaptureCopy (43 B)
   |  return value nonzero -> continue; zero -> return 9
```

**Slot 4 is the frame tick**, and `0x0017D6E0` is the per-frame pump: *for each subsystem, fetch its
singleton and advance it.* The `SaveloadManager` pair is the only one whose functions carry recovered
names, and it is enough to identify the pattern the other fifteen follow.

## 6. Modding notes

- **`+0x113C` gates three entry points.** Anything driving `GameApplication` externally before that
  byte is set will find those methods return immediately.
- **Slot 5 is deliberately empty**, not missing — a 5-byte thunk into the shared `xor eax,eax ; ret`
  stub. Do not read it as an unimplemented hook.
- **The archive path is relative** (`'../FFXII_TZA.vbf'` plus `'../../..'`), so anything relocating
  the executable relative to the archive breaks the mount.

## 7. What is not known

- [x] ~~**What slot 4 actually schedules.**~~ **BE-1 ANSWERED** — it gates on the latch, takes a
      double frame delta from `this + 0x48`, and calls `0x0017D6E0` (404 B, `CoreRuntimeScheduling`)
      on all three of its paths. That function has **37 callees, 16 of them 8-10 byte singleton
      getters** each paired with a substantial update body — a per-frame subsystem pump. The named
      pair `SaveloadManager_GetSingleton` / `SaveloadManager_ProcessPendingCaptureCopy` fixes the
      pattern. §5.
- [x] Slots 21/22 and 23/24. Matched pairs — **"focus gained/lost" is a shape, not a finding**, and is
      not asserted. **The addresses in §3 were wrong until §10**; the real pairs are
      `0017CFD0`/`0017D170` and `0017CDF0`/`0017CE20`. **Re-tested 2026-09-12 (FABLE) on the corrected
      addresses — the shared-target claim holds for both pairs, and the pairs are not alike:**
      slots 21/22 both resolve the singleton `001997D0` (`[01F810F0]`, 8 B) and hand it to
      `00199780(obj)` (4 B) and `001997E0(obj, byte)` (3 B) respectively — a getter and a one-byte
      setter on one object; slots 23/24 both return an Input float (`0079D560` / `0079D5B0`, 69 B
      each) multiplied by `0017E440` — the console block's dword `+0x10D4` as a float, or a
      constant when no console ([the console page](../Developer-Tuning-Console/the-282-command-parameter-console.md)) — two axes under one tunable scale. **BE-2 ANSWERED 2026-09-12 (FABLE).**
      *The byte is the pause flag.* Its writer is the pause-menu handler `00229590` (registered as a
      callback by `002282F0` at `0022832E`; its own debug prints are `"PauseMenu Create\n"` and
      `"PauseMenu Open\n"`, `0022995A` / `00229864`): the open path sets it through the app's wrapper
      `0017E720(1)` (`002298C1`) beside `Audio_SetGroupMask(0x3F, 1, 1)` ([the audio boundary page](../../18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md)),
      `00183200(1)`, `00182FF0(1)` and `00181E10(1)`, and the close path clears it (`002297B0`,
      `0017E720(0)`) after clearing capability-policy row 15 bits 0, 9 and 20. Its readers, all through
      the getter `0017E4E0`: the frame dispatcher's prologue `0022A580` mirrors it into `02F974A0`
      every frame (`0022A67A`; the `mov [rip+0x2D6CE20], eax` resolves to `02F974A0`,
      not `02D914A0` as first recorded); the field frame `0022A770` (`0022A8CA`), while it is set, runs the
      pause step `002506D0` and only its `"[PS2]process camera"` / `"CAMERA"` section before ending
      the frame (`0022A8D7`–`0022A994`); `00250540`, called by the full-menu and capture frames of
      [the between-two-frames page](../../22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md), runs the same step (`00250570`); and the two render passes `001D72F0` (from the
      render pass list `00187950` through `001D7280`) and `001D7A20` (from the slot-4 pump through
      `001D8AB0`) return at once while it is set (`001D7326`, `001D7A63`).
      *The floats are two backend coordinates.* `0079D560` / `0079D5B0` read the input manager
      ([the binding-profiles page](../../15-Input/Binding-Profiles/binding-profiles-remapping-and-control-state.md) — `[02EA5368]`; the object `00792350` constructs with the label
      `PhyreFrameworkApplication`) and return `2 × min(v, s) / s`, with `s = min(+0xD24, +0xD28)` —
      the window size, `1280 × 720` from the constructor (`00792459`), rewritten by the screen-mode
      routine `0079C140` from `GetSystemMetrics` — and `v` the backend's (`+0xDF8`) dword `+0x184` /
      `+0x188`; the app's slots then multiply by the console's `+0x10D4` or **640.0** (`008C5A98`),
      so a coordinate equal to the short side reads 1280. The pair is zeroed by `00798000`, which
      parses a `"%d,%d"` string into the backend's `+0x178` / `+0x17C` and raises its bytes `+0x170`
      and `+0x177` before calling the app's slot 7, and is copied whole by `007939A0` (`00793B88`);
      what the pair is *named* (a pointer position is the shape) is not established.
- [x] ~~**13 of the 31 slots are folded** with other classes and absent from this analysis entirely.~~
      **BE-3 ANSWERED in substance** — 10 of the 13 are **inherited** from the base class whose vtable
      is at `0x01CB2508`, at identical slot indices, and are fully visible there. Only 3 are genuine
      `/OPT:ICF` stubs (`005C5230` twice, `0016D6A0` once). What the base class *is* remains open, and
      is carried below.
- [x] ~~The object's true size.~~ **BE-4 ANSWERED — exactly `0x1140` = 4,416 bytes**, stated by the
      sized `operator delete` in slot 0. §4.
- [x] ~~**BE-5.** What the base class at vtable `0x01CB2508` is.~~ **ANSWERED —
      `Phyre::PFramework::PApplication`**, with `Phyre::PBase` and `Phyre::PMemoryBase` above it.
      The `.rdata` neighbourhood is the PhyreEngine framework's vtable region; the input-device
      classes are siblings, not relatives. §4, §11.
- [x] **BE-6 — ~~partly~~ answered 2026-09-27.** The tick pumps **13 lazily-constructed singletons**, not 16.
      **Six are named** — `AsyncJobManager`, `AsyncLoadManager`, `Phyre::PCameraPerspective`,
      `SaveloadManager`, `MultipleDebugDisplay` from RTTI, and **`ScreenImage`** from an authored
      profiler label — and **all thirteen are characterised** by what their update does. The
      remaining seven are non-polymorphic, carry no label, and defeated seven further instruments
      tested against known controls; they need runtime or authored evidence from outside the
      executable. §11.
      *Narrowed (FABLE, Claude Opus 5.5, 2026-09-26): two of the seven now have roles read from code, though still no class
      names.*
      - **`01F81248` is the `CharacterRenderObject` recycle pool.** The acquire and release wrappers hand it to
        the pool's acquire and release. Its update counts each released object down for three frames, then calls
        its slot 3 until it returns true, and marks every active object's `+0x4B5`.
      - **`01F81240` is the character model asset cache.** The `.ah` loaders fill its id map, using the format
        `./GameData/%s/ArtData/chr/%s_%s.ah`.
      *ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5): all 13 have a role read from code. The last five are the frame-end command-list teardown,
      the procedural-texture context, the renderer, the one-byte pause flag (BE-2) and the map-art context. The seven
      non-polymorphic ones carry no class name in the image, and none is claimed.
      [Record](../../_index/candidates/be6-two-pump-singletons/README-all-roles.md), `be6_all_roles.py` FAILS 0.*

      See [the render-object page](../../17-Presentation-Rendering/Character-Rendering/character-render-object.md) (BB-4) and the control [`be6_two_singletons.py`](../../_index/candidates/be6-two-pump-singletons/be6_two_singletons.py) (3 checks, FAILS 0). Five remain uncharacterised by role.

## 8. Evidence

**Tier 1**, and a **two-session result**: the analysis is peer session repos-39's, independently
re-verified here before publication.

| claim | re-verified result |
|---|---|
| slot 2 references the VBF archive | **exact** — `'../FFXII_TZA.vbf'` and `'../../..'`, 120 B method |
| `+0x113C` is a one-way latch | **exact** — **1 write, 3 reads, image-wide**, reads at +6, +39, +4 bytes into their methods |
| `+0x113D` is a method-local guard | **exact** — write and read **both inside slot 4**, 19 bytes apart |

**The latch finding is image-wide, not class-scoped.** The enumeration disassembled every function in
`.text` and matched the offset, so "one writer" means one in the whole executable — the strong form of
the claim, and the only form that supports calling it a latch.

~~**What is deliberately not claimed.** That slot 4 is the frame tick. It is the largest slot, it is
tagged `CoreRuntimeScheduling`, and it is gated by the startup latch — all consistent, none
conclusive, and **the body was not followed into what it schedules**. **BE-1** holds that open rather
than letting three consistent signals stand in for a traced call.~~ *Superseded 2026-09-26 (FABLE, Claude Opus 5.5): **BE-1** was answered on 2026-09-02. Slot 4 is the frame tick: it gates on the startup latch and calls the per-frame subsystem pump on all three exit paths (§5, §7 and §10 of this page).*

## 10. Falsification pass 1 - 2026-09-02

**Program state:** parent `2ed8affb...`, snapshot `46f02e26...`, embedded EXE `73461d08...`, ledger
38,161 / 38,003 / 158, verified before any reading.
**Instruments:** the vtable located and read **directly out of the PE image** (found by searching for
slot 2's address as a qword, then confirmed by four independently documented slots landing on their
stated indices); capstone over the class's method bodies with clamped extents; a displacement scan
for `+0x113C` and `+0x113D` across all 38,161 function bodies; a qword-reference census over the
whole image for each of the 31 slot pointers.

### Killer observations named, and hunted

| Claim | What would kill it | Result |
|---|---|---|
| 31 vtable slots | a 32nd function pointer | **SURVIVED.** Slot 31 onward is the ASCII `'../../..'`. |
| 18 uniquely owned, 13 folded | a different split | **SURVIVED exactly**, 18/13, by image-wide reference count. |
| `+0x113C` is a one-way latch: 1 write, 3 reads, image-wide | a second writer, or a read not at method head | **SURVIVED exactly** — and no other structure in the binary has a field at that offset, so the claim needs no type-scoping caveat. |
| the read/write byte offsets +116, +6, +39, +4 | any being different | **SURVIVED, all four exact.** |
| `+0x113D` is a method-local guard | an access outside slot 4 | **SURVIVED.** 2 accesses, both in slot 4, 19 bytes apart. |
| slot 2 mounts the VBF | the strings not being there | **SURVIVED.** `'../../..'` at `008C5858`, `'../FFXII_TZA.vbf'` at `008C5868`. |
| slot 5 is an explicitly empty override | it not being a thunk to a `ret` stub | **SURVIVED in substance, address wrong.** |
| **`GameApplication` has no deleting destructor** | slot 0 being one | **OVERTURNED.** |
| **its size is a lower bound, not stated by the code** | a sized `operator delete` | **OVERTURNED.** |
| **slot 5 = `0017CE40`** | the address not being a function | **OVERTURNED - a ghost address.** |
| **slots 23/24 = `0079D560`/`0079D5B0`** | those being in another vtable | **OVERTURNED.** |
| **highest field observed `+0x1138`** | a higher field | **OVERTURNED - by this document's own §2.** |
| **13 slots "folded and invisible here"** | them being visible somewhere | **OVERTURNED - 10 are inherited.** |
| BE-1: what slot 4 schedules | following it | **ANSWERED.** |

### The six overturns

**1. There is a deleting destructor, and it states the size.** §4 argued that the application root is
never deleted, so no sized `operator delete` exists to state its size. Slot 0 is a scalar deleting
destructor of the standard MSVC shape, and its sized-delete path carries **`mov edx, 0x1140`**. The
object is exactly **4,416 bytes**. The reasoning that produced the wrong claim was sound and the
premise was simply not checked: *the application is never deleted* is probably true at runtime, but a
C++ compiler emits the deleting destructor for any polymorphic class regardless of whether the
program ever calls it. **"This never happens at runtime" does not predict "the code is not there."**

**2. Slot 5's address is a ghost.** `0017CE40` is not a function; it is a **mid-body address inside
slot 24** (`0017CE20`, 39 bytes, spanning `0017CE20`-`0017CE47`). The real slot 5 is `0017CDE0`. The
*claim* about slot 5 — a 5-byte thunk into a `xor eax,eax ; ret`-class stub — is correct of the real
address, so this is a citation error rather than a reading error.

**3 and 4. Slots 23/24 came from a different vtable, and that explains the folding claim too.**
`0079D560` and `0079D5B0` sit at `0x01CB25C0` and `0x01CB25C8`, which are **slots 23 and 24 of the
vtable at `0x01CB2508`** — the base class's. The slot *numbers* were right; the vtable was not.

That single mix-up explains the "13 folded" reading as well. Ten of this class's thirteen
non-overridden slots appear in that base vtable **at identical indices**, which is inheritance, not
folding. Reading some rows from the derived vtable and some from the base makes the inherited slots
look like they belong to unrelated classes.

**5. `+0x1138` is not the highest field, and §2 already said so.** §2 documents `+0x113C` and
`+0x113D` at length; §3 then states the highest field observed is `+0x1138`. **The document
contradicted itself in two sections a reader would not compare** - the third instance of that exact
shape found today, after `character-render-object.md`'s *12 of 12 / 13 reads* and the ScriptVM
interpreter's *ANSWERED / not established*. In this case the contradiction was load-bearing: the
`≥ 0x1140` bound was derived from `+0x1138`, and `+0x113D` gives the same bound only by coincidence
of alignment.

**6. BE-1 answered.** Slot 4 gates on the latch, converts a double at `this + 0x48` to a float,
publishes it, runs a one-shot initialiser behind `+0x113D`, and then calls `0x0017D6E0` on **all
three** of its exit paths with that double in `xmm0` and a mode selector in `edx`. `0x0017D6E0` is
404 bytes, tagged `CoreRuntimeScheduling`, and has **37 callees of which 16 are 8-10 byte accessors**,
each paired with a substantial update body. `SaveloadManager_GetSingleton` /
`SaveloadManager_ProcessPendingCaptureCopy` is the one pair whose names are recovered and it fixes the
pattern for the rest. **Slot 4 is the frame tick and `0x0017D6E0` is the per-frame subsystem pump.**

### A bounded negative, for the argument-passing workbench

`repos-f1` proved a shared-memory argument-passing area at `0x022D91B0` with 152 owned writers, and
asked whether this document's scheduler reaches it. **It does not, at one hop or two.**

```
functions touching 022D91B0..+0x400        : 247
slot 4 (0017CCD0) among them               : no
its target 0017D6E0 among them             : no
any of the 22 GameApplication vtable bodies: no
the tick's 37 hop-1 callees   n them       : none
the tick's 109 hop-2 callees  n them       : none
```

**The two documents should not cite each other on this basis.** If the workbench is reached from the
application root at all, it is deeper than two calls, and nothing here establishes that it is.

### What was tried and failed to break it

- **Located the vtable independently** rather than taking any slot address on trust — searched the
  image for slot 2's address as a qword, found exactly one occurrence, and confirmed the base by
  checking that four separately documented slots (2, 4, 7, 8) land on their stated indices. That is
  what made the two bad rows visible: they did *not* land.
- **Attacked the latch as possibly type-ambiguous.** `+0x4B4` in `character-render-object.md` needed a
  caveat because 33 functions touch that offset on unrelated structures. `+0x113C` has **four
  accesses in the whole binary and no other user at all**, so the image-wide claim is clean as stated.
- **Checked the sized-delete callee before believing the size.** `0x0016D6A0` is a 3-byte `ret` with
  2,479 distinct callers (2,867 call sites; 2,511 functions reference it at all, 1,515 of those through data pointer slots) - an ICF fold, and worthless as evidence about deletion. The **size immediate** is
  emitted at the call site by the compiler and does not depend on it. Claiming the size while
  claiming nothing about the callee is the correct split.
- **Re-checked for banned evidence.** No `.pdata`, `.xdata`, unwind or EH reasoning appears here. The
  RTTI complete-object-locator pointers at `vtable - 8` were read to confirm vtable boundaries and
  support no semantic claim.

### Status

**Six claims overturned, BE-1, BE-3 and BE-4 answered, BE-5 and BE-6 opened**, and the latch finding -
the document's centrepiece - survived every attack exactly, including the byte offsets. The
structural counts (31 slots, 18/13) survived exactly. **This document has now had its first
falsification pass.**

## 11. BE-5 and BE-6 - 2026-09-02

**Program state:** as §10. **Instruments:** MSVC RTTI read directly out of the image — complete-object
locators at `vtable - 8`, type descriptors, and class-hierarchy descriptors — plus the singleton
census from §10's tooling.

### BE-5 — the base class, and what the neighbourhood meant

`0x01CB2508 - 8` is a complete-object locator whose type descriptor reads
**`.?AVPApplication@PFramework@Phyre@@`**. `GameApplication`'s own class-hierarchy descriptor lists
three bases — `PApplication` at `mdisp 0`, then `Phyre::PBase` and `Phyre::PMemoryBase` at `mdisp 8`.

**Two independent derivations agree.** §10 concluded from the *destructor chain* that `0x01CB2508`
is the primary base's vtable, because `0x00793250` writes it to `[this + 0]`. RTTI says `mdisp = 0`,
which means exactly that. Neither derivation used the other.

**The neighbourhood question is settled, and the answer is the second of the two hypotheses.** Naming
every vtable in `0x01CB2400`–`0x01CB2800` gives twelve classes and **all twelve are
`Phyre::PFramework`** — the window, the viewport, the application-script trio, and five input-device
classes including a `PInputDevicePadSteamController`. So the base is a **generic middleware framework
object**, and the input devices sit beside it because they are framework classes too, not because
they share ancestry with the application root.

**What this makes `GameApplication`:** the game's own subclass of PhyreEngine's application class,
supplying 18 of 31 virtual methods and inheriting 10. The frame tick, the VBF mount and the startup
latch documented above are all **game code overriding middleware entry points**.

### BE-6 — the per-frame subsystem set

Slot 4's pump (`0x0017D6E0`) fetches and advances **13** lazily-constructed singletons. Each follows
one shape: a global pointer, an `Ensure` function that allocates a fixed size and constructs on first
use, and an 8-byte getter the tick calls.

| global | `Ensure` | update | size | identity | evidence |
|---|---|---|---:|---|---|
| `01F810F8` | `0019A0A0` | — | `0x158` | **`AsyncJobManager`** | RTTI |
| `01F81160` | `001A11B0` | `001A1310` | — | **`AsyncLoadManager`** | RTTI |
| `01F81218` | `001B7EE0` | `001B8400` | `0xBB8` | **`Phyre::PCameraPerspective`** | RTTI |
| `01F81260` | `001C18A0` | `001C1910` | `0xA78` | **`SaveloadManager`** | RTTI |
| `01F81270` | `001C2F00` | `001C2F50` | `0x4670` | **`MultipleDebugDisplay`** | RTTI |
| `01F82CE0` | `001D8CD0` | `001D9080` | `0x38` | **`ScreenImage`** — the screen fade | **authored label** |
| `01F7F598` | `00189000` | `00189CE0` + `00189570` | `0xDD8` | unnamed — pumped **three times** per tick, the only one that is; *role (FABLE, Claude Opus 5.5, 2026-09-27, [record](../../_index/candidates/be6-two-pump-singletons/README-all-roles.md)): **the renderer**: its accessor has 117 callers, and render slot 8 runs the render pass list on it* | — |
| `01F81248` | `001BDA50` | `001BDAC0` | `0x108` | unnamed — a **pending-completion queue**; *role (FABLE, Claude Opus 5.5, 2026-09-26): the `CharacterRenderObject` recycle pool — the queue is its released objects, expired after a three-frame count by their slot 3* | code (BB-4) |
| `01F82D30` | `001E0550` | `001E0590` | — | unnamed — an **end-of-frame reset**; *role (FABLE, Claude Opus 5.5, 2026-09-27, [record](../../_index/candidates/be6-two-pump-singletons/README-all-roles.md)): **the frame-end command-list teardown**: two latch bytes, not an object; its update clears the ordered command list, then flushes the vector that owns it* | — |
| `01F81258` | `001C0D40` | `001C0DD0` | `0x1B8` | unnamed — a **one-shot latch**; *role (FABLE, Claude Opus 5.5, 2026-09-27, [record](../../_index/candidates/be6-two-pump-singletons/README-all-roles.md)): **the procedural-texture context**, built with the `proceduralTexture_%s.ah` path and set up once, when its request reports loaded* | — |
| `01F81240` | `001BBFC0` | `001BC190` | `0x238` | unnamed — largest update body (1,828 B); *role (FABLE, Claude Opus 5.5, 2026-09-26): the character model asset cache — an id-keyed map of `.ah`-loaded model entries whose `+0x2A0` is the model resource key* | code (BB-4) |
| `01F81168` | `001A98B0` | `001A9ED0` | ~~`0xA0`~~ **`0x520`** | the map-art (`.ta` texture-animation) context — corrected 2026-09-14, see below | — |
| `01F810F0` | `00199790` | — | — | unnamed; *role (FABLE, Claude Opus 5.5, 2026-09-27, [record](../../_index/candidates/be6-two-pump-singletons/README-all-roles.md)): **the one-byte pause flag** (BE-2): application slots 21 and 22 are its getter and setter, and the pause menu writes it* | — |

### `ScreenImage` — the screen fade

`0x01F82CE0`'s update carries an **authored profiler scope label**:

```c
FUN_001eb150("ScreenImage");    // the same scope-push that pushes the
FUN_001d8bb0(this);             // "display character : ..." labels
FUN_001eb110();
```

and the body is a fade ramp:

```
if (this[0x00] == 0) return;                 // disabled -> nothing
this[0x04]++                                 // a frame counter
mode = this[0x10]
if (mode == 0)  this[0x1C] += this[0x20]     // fade one way
if (mode == 1)  this[0x1C] -= this[0x20]     // fade the other
this[0x0C]++
if (mode == 0 && this[0x0C] >= this[0x14] && this[0x1C] > threshold)
        this[0x1C] = 255.0                   // clamp
```

`Ensure` constructs it with `this[0x00] = 0` (disabled) and `this[0x10] = 3` — a mode the update
ignores, i.e. idle. **A level ramping between 0 and 255 at a per-frame step, with an up mode and a
down mode**, is a screen fade: this is the object behind the screen going to and from black on area
transitions and event boundaries.

### The behavioural characterisations

- **`01F7F598`** is pumped **three times in one tick** — once early, then twice more with two
  different update bodies (`00189CE0`, 1,083 B and `00189570`, 577 B). Nothing else in the set is
  pumped more than once, so its ordering relative to the others is load-bearing.
- **`01F81248`** walks an intrusive doubly-linked list, calls the **virtual method at `vtable+0x18`**
  on each node's object, and unlinks the nodes that return non-zero — a **pending-completion queue**
  polled once per frame. It is gated off entirely while `FUN_0017d980()` is non-zero.
- **`01F82D30`**'s update fetches several *other* singletons, calls a finish function on each, and
  then zeroes two bytes of its own state — an **end-of-frame reset**, which is consistent with it
  being the last getter called in the tick.
- **`01F81258`** does its work once, behind a condition, and sets a byte so it never runs again — a
  **one-shot latch** rather than a per-frame update.

**Positive control.** `SaveloadManager` was already named in the ledger, and the method recovered it
from the global alone — the same route, run blind, returns the known answer. That is why the other
four are reported.

**One candidate was rejected.** `01F81168` initially resolved to `.?AVallocator@eastl@@`. Its
`Ensure` allocates `0xA0` bytes and calls an EASTL container constructor, so the allocator vtable is
**construction machinery the constructor touched, not the class of the object stored in the global**.
Reading a vtable within one hop of an allocation is not the same as reading *the* object's vtable,
and the control is what made the difference visible: had `SaveloadManager` also returned a container
type, the method would have been unusable.

> **Corrected 2026-09-14 (FABLE): `0xA0` is not the size of the `01F81168` object.** `001A98B0` builds **two**
> objects. First it allocates `0xA0` bytes (`001A98DB`), constructs them with `00633040`, whose base `00633070`
> passes the name string `PInstanceList` (`00D58650`), and stores the pointer at **`01F81170`** (`001A98FC`).
> Then it allocates **`0x520`** bytes (`001A9903`), constructs them with `001A2130`, which names EASTL strings
> (`008F6600`), and stores that pointer at **`01F81168`** (`001A9922`). The rejection above still stands: the
> container vtable belonged to construction machinery. But the size belonged to the neighbouring global. The
> `0x520` object is the map-art context that
> [the `.ta` texture-animation lists](../../02-Resource-And-Asset-Pipeline/Prefetch-And-Json-Data/ta-texture-animation-lists.md)
> reads at `+0x120`–`+0x264`, offsets a 160-byte object could not hold.

**Eight of the thirteen have no vtable at all**, so RTTI cannot name them. **Eight further
instruments were tried against the five known answers as controls, and seven failed:**

| instrument | result against the known singletons |
|---|---|
| strings referenced by `Ensure`/update, depth 1 | returns EASTL allocator tags or nothing — **fails** |
| named callees of the update, depth 1 | 1 of 3 gives a thematic hint, 2 give nothing — **fails** |
| named callees of the update, depth 2 | returns **`vpx_codec_destroy` for a camera** — **actively misleading** |
| named callers of the getter | 1 of 3 gives a thematic hint — **fails** |
| named functions touching the global | only the already-named ones — **circular** |
| an allocator tag string at the `Ensure` | none of them passes one — **fails** |
| a master function walking the singleton block | no such function exists — **fails** |
| **authored profiler scope labels** | **works, and named one** |

The seventh row is the one that mattered. `FUN_001EB150` is the engine's **named-scope push** — the
same function that pushes the `"display character : …"` labels — and a scope name wrapped around a
subsystem's per-frame update is that subsystem naming itself. **Only one of the thirteen carries
one**, which is the correct shape for the instrument: a scan that returned a label for all thirteen
would have been reporting its own noise.

**Six of thirteen are now named and all thirteen are characterised.** The remaining seven need
runtime evidence or authored data outside the executable. ~~**BE-6 stays open for those seven.**~~ *Their roles were read
from code on 2026-09-26/27 (the BE-6 box, 2026-09-27 (FABLE, Claude Opus 5.5)); what the image cannot give is a class name for the seven
non-polymorphic ones, and none is claimed.*

### Propagation

`GameApplication` being a `Phyre::PFramework::PApplication` subclass is a fact about the boundary
between the game and its middleware, and the PhyreEngine documents in
[`../../22-Middleware-PhyreEngine/`](../../22-Middleware-PhyreEngine/) do not currently say that the
application root is one of theirs. **They should reopen to absorb it**, along with the twelve-class
`PFramework` vtable cluster enumerated above.

## The `008C5760` vtable's no-caller members, bound — 2026-09-14 (NOCALLER-INSTALLERS)

Thirteen of this vtable's overridden slots have no direct `E8`/`E9` caller — the framework dispatches
them through the table. Each is bound below with its slot and one interior instruction.

| slot | address | role | interior |
|---:|---|---|---|
| 2 | `0017CEB0` | the VBF mount — loads the `'../FFXII_TZA.vbf'` strings at `008C5858`/`008C5868` and drives `0059A770`/`0019B190` | `0017CED3` |
| 3 | `0017CF30` | gathers the framework singletons: `00796E20` then `00182E80`/`00182EB0` pair results kept for the tail | `0017CF47` |
| 4 | `0017CCD0` | the frame tick — `0018A620`/`0018A670`/`0018A7D0` scheduling calls, then `0017D650` | `0017CCF9` |
| 6 | `0017CDC0` | `0017D670` on self, then tail-jumps the base's `0079BF70` | `0017CDC9` |
| 7 | `0017CE50` | latch-read then `00228480`/`00198790`/`001967D0`/`00194AF0` — the input-path poll | `0017CE59` |
| 8 | `0017D090` | render-path entry — `00189120` guard then the pass list `00187950` | `0017D0A4` |
| 9 | `0017D0C0` | double `00189120` lookup; pushes `this+0xD24`/`+0xD28` into the shared object's `+0xAD8`/`+0xADC` | `0017D0D8` |
| 10 | `0017D120` | `00189120` lookup then `byte [rax] = 1` — a one-flag request; tails the empty stub | `0017D138` |
| 15 | `0017D1A0` | `00198790` lookup, forwards the byte arg to `001989D0`, tails the empty stub | `0017D1C5` |
| 16 | `0017D210` | calls `00227D40` with the byte arg, then tails the empty stub | `0017D222` |
| 22 | `0017D170` | `001997D0` lookup twice, forwards the byte arg to `001997E0` | `0017D18E` |
| 23 | `0017CDF0` | returns `0079D560()` × `0017E440()` — a product of two float getters | `0017CE06` |
| 25 | `0017D1E0` | `00198790` lookup ×2, forwards the byte arg to `00198E70` | `0017D1FE` |

Slots 9/10 are the same `00189120`-lookup pattern as slot 8 but for a different subsystem object;
15/22/25 are one-line forwarders that hand a byte argument through a `00198790`- or
`001997D0`-family lookup into the callee, and 16 forwards its byte arg to `00227D40`. They are listed here so each no-caller member carries a
stated role — the page's §3 table stays the semantic summary.

## The `0017D000` exclusive subtree — the startup manager-init burst (SWE2-FRONTIER, thunk-roots addendum)

The exclusive-callee census roots `0017D150` — a tail-call thunk — at its target `0017D000` (the
latch writer, §5) and assigns it **114 frontier functions** in the `0x17xxxx`–`0x20xxxx` band, the
application's boot-time manager-initialisation tree. Signature-swept 2026-09-15 (`bshape.py` plus a
store-target extract on every small body); roles below are instruction shapes and call/global
targets, measured — the singleton names are *not* claimed beyond what the global and the ctor reach.

`0017D000` itself allocates an `0x80` record into `[01F7E340]`, then calls three bodies before
latching `+0x113C`: **`0017D4C0`** (387 B — the init burst proper: stores five globals
`01F7F4C0`/`C8`/`D0`/`D8`/`E0`, allocates `0x10`, then ~35 init calls in sequence — every
ensure-stub and constructor below), **`0018A840`** (412 B — `malloc` + the `001DE540` SIMD leaf +
`00615CD0`/`0061D9C0`, refs `01F82D20`), and **`00189000`** (131 B — allocates `0xDD8` into
`[01F7F598]`, calls `00184F20`).

| cluster | members | role |
|---|---|---|
| render-subsystem branch | `00184F20` (335 B — `00184CE0` ×2 + `0062DD10` ×2 + `00186CD0`), `00184CE0` (377 B — SceneCamera-tagged), `00188640` (225 B — fixed-16B-vector reserve/relocate, two indirect calls) | the `00189000` object's setup — camera pair + the subsystem fill below |
| subsystem fill | `00186CD0` (1,240 B — 56 calls: `001EE040` ×14, `00182E80` ×11, `00182EB0` ×11, `00796E20` ×4, plus `001F0810` lazy-allocator, `001C3760`, `00188640`, `005C5230`) | a repeated (helper-pair ×11 + getter ×14) register sequence — installs ~30 subsystem records under the `189000` object |
| ensure-singleton stubs | `0018AD00` (`008C5F58` ref + `001EDF00`), `0018B480` →`[01F7F5E0]`, `0018C9E0` →`[01F7F5E8]` (alloc `0x20`), `00194AB0` →`[01F7FFD8]`, `00198750` →`[01F7FFE0]` (alloc `0x40`, ctor `00195060`), `00199790` →`[01F810F0]` (the BE-2 focus singleton's global), `001A11B0` →`[01F81160]` (alloc **`0x140228`** ≈ 1.31 MB — the largest single boot allocation), `001A98B0` →`[01F81170]`/`68` (alloc `0x520`, ctor `001A2130`), `001AD3E0` →`[01F811C8]` (alloc `0x258`, ctor `001AA9E0`), `001B1BA0` →`[01F811E8]` (alloc `0x4300`, ctor `001ADD30`), `001B5F10` →`[01F81200]`/`F8` (alloc `0x2380`, ctor `001B3940` + `001E71B0`), `001B6BC0` →`[01F81210]`, `001BDA50` →`[01F81248]` (alloc `0x108`, ctor `001BC9D0`), `001C0D40` →`[01F81258]` (alloc `0x1B8`, ctor `001BE730`), `001C18A0` →`[01F81260]` (alloc `0xA78`, ctor `001C0E20`), `001C1940` →`[01F81268]` (ctor `001D5090`), `001D62D0` →`[01F82C80]` (alloc **`0xF778`** ≈ 63 KB, float-preset fields `0.2`/`-0.8`/`0.04`/`0.8`/`0.7`), `001D6990` →`[01F82CB8]`, `001D8150` →`[01F82CD0]` (alloc `0x90`), `001D89D0` →`[01F82CD8]`, `001D8CD0` →`[01F82CE0]` (alloc `0x38`), `001DB1E0` (36 B, →`[01F82CF8]`), `001DB500` →`[01F82D00]` (alloc `0x20`, ctor `001A1420`) | the shared shape `cmp [G],0 → jne done → alloc → ctor → store [G]`: lazy-create for one global each — nearly all route the allocation through `00210EC0` (`jmp malloc`); `001A11B0` is the exception, calling `00584740` for its 1.31 MB record. The globals form a contiguous **manager-pointer block `01F7F4C0`–`01F82D00`**; each `0016D6A0` call is the folded-empty stub (a no-op site in the shipped image) |
| input cluster (`0019xxxx`) | `00195060` (153 B — drives `00197EE0`/`00198000`/`00196550` + three more), `00196550` (135 B leaf, `01DF13E0`/`01F80F90` refs), `00197EE0` (273 B — input-boundary helper `001F3EA0` ×4 + `00194EF0` ×4 + `001F3ED0` achievements), `00198000` (1,644 B — `memset` + **~30 vtable installs** `008C26xx` — the input manager's object ctor), `0019F060`/`0019F0D0`/`0019F190`/`0019F250`/`0019F300`/`0019F3E0` (111–222 B leaf helpers, `[r9+0x10]`/`[r9+0x18]` indirect calls), `0019FC30` (926 B — calls the six leaves ×8), `0019FFD0` (2,010 B — **interior read 2026-09-17:** NOT input — the **`effect_finish` path-table initializer**: `memset` ×2 then 125 `PS2Data\effect_finish\jp\chara\hNNNN.efx` path pointers written as a flat qword array `[rbx+0x115750]`–`[+0x11FB20]`; the strings sit at 0x30 pitch in `.rdata` from `008F4710`, first store's `lea` at [`001A0020`](../../_index/ADDRESS-INDEX.md)) | the input subsystem's construction — singleton `00198750`→`00195060` reaches all of it |
| `001EDF00`-apply bodies | `0019F490`, `0019F620` (207 B — `005CC8A0` ×3 + `001EDF00` ×2), `001A1500` (467 B), `001AA9E0` (619 B — `001EDF00` ×5 + `0019C5D0` ×5), `001ADBA0`, `001ADD30` (728 B — `001EDF00` ×12), `001B33A0`, `001B3480`, `001B3540`/`001B36D0` (387 B twins), `001B3940` (424 B — `001EDF00` ×8 + the twins), `001B4140` (856 B — `001B33A0` ×4 + `001B3480` ×2), `001B9CF0` (137 B) | the sead container/string apply shape (`001EDF00` + `005CC8A0` + `005CD0A0` + `00199DB0`) — category/record registration; `001EDF00` carries the `V93_SaveLoadSettingsCategoryParse` tag |
| manager/object constructors | `001A2130` (1,564 B — `001EDF00` ×17 + `001A94F0`/`001A95C0`/`001A9050`, vtables `008F6500`/`008F6600`), `001A3930`/`001A3A90`/`001A44F0` (342/330/155 B — `0016D840` red-black-insert users), `001A9050` (612 B — `001D6F20`/`1D6EE0`/`1D6FA0`/`1D6E80` field quad + `001A3A90`), `001A94F0`/`001A95C0` (198/234 B leaf pair), `001AF000` (678 B — `001ADAB0` ×4 + `0021A920` ×2 + `001AE4B0` ×2 + `001FB460` ×2), `001B0640` (129 B), `001B07A0` (627 B), `001B14E0` (159 B — same `1D6Exx` quad + `001B07A0`), `001B1580` (32 B → `001B1630` + `001AF470`), `001B1630` (281 B — ten-helper fan-out), `001B1750` (165 B → `001B14E0` + `001B1800`), `001B1800` (268 B), `001B1B10` (135 B), `001B3E80` (689 B leaf, IND pair), `001B4860` (196 B), `001B5D60` (114 B → `001B3E80`), `001B5DE0` (292 B), `001B6C50` (138 B — `001B7CE0` ×2), `001B72B0` (981 B — `00671B10` ×4 + `0017D260`/`00671690`/`00674230`/`0066F970`/`00671B30`/`00674610` ×2 each — the Phyre render-block-binding init), `001B7850` (1,166 B — **triad shape**: `0060DD70`/`00610990`/`00625F00`/`005CDAA0`/`00628100`/`0018D240`/`001B81B0` each ×3 — three sibling sub-objects; interior verified 2026-09-17, SWE2-FRONTIER — the siblings are the `YChannel`/`UChannel`/`VChannel` strings, `0061D9C0` first at [`001B78C9`](../../_index/ADDRESS-INDEX.md)), `001BA210` (404 B), `001BB920` (1,248 B — `001EDF00` ×6 + `0017D2E0` sprintf ×3 + `001BA210`/`001BA860` ×2; interior verified 2026-09-17, SWE2-FRONTIER — `chr/%s_%s.ah` + `chr_shadow` ArtData path strings, first call [`001BB96D`](../../_index/ADDRESS-INDEX.md)), `001BC9D0` (693 B — `0061D9C0` ×4 + `001EDF00` ×3), `001BE730` (403 B), `001C0E20` (130 B), `001C1810` (142 B), `001C3760` (1,220 B — `001FF740` ×14 + `00200BE0` ×11 + `00202880` ×8 — render-support fill), `001EEC80` (499 B — ten-helper fan-out + `008F6574`), `001F0570` (57 B — `001DE5A0` ×2 over `01F82D20`) | the substantial bodies the ensure-stubs and orchestrators call — each builds one manager/record |
| leaves and small helpers | `00194AA0` (14 B), `001A08F0` (100 B → `0019F190`), `001A0AF0` (182 B), `001A1050` (222 B — `0019F060` + IND), `001A1130` (116 B → `0019FC30`), `001A14E0` (28 B → `001A1420`), `001A16E0` (31 B → `001A1500`), `001A17D0` (18 B, `008F5F28` vtable ref), `001ACF10` (110 B — `001EE040` ×2 + `02CF76E8`/`02CF79C0`), `001AD510` (153 B leaf), `001AD8E0` (125 B → `001AE4B0`), `001AD960` (330 B — `001AF2B0`/`001AE6B0` + IND), `001ADAB0`/`001ADB30` (127/108 B → `0021A920`), `001AF470` (3,179 B — **no calls**: ~227 `lea`/`mov` pairs installing `.rdata` pointers into `[rcx+0x3B00]`+ — a descriptor/handler-table fill), `001B24D0` (94 B leaf), `001B3290`/`001B3320` (130/113 B → `001A5760`), `001B80C0` (56 B leaf, bitfield-state shape), `001C1710` (10 B leaf), `001D5600` (17 B leaf), `00200B30` (18 B, `01F83288` ref), `0022A4B0` (58 B — `0016D6A0` ×5 + `00291C80`/`0053DD10`/`00563520`/`00556500`), `00291C80` (177 B — `0024AB90`/`00249810`/`0032E620`, `0209BEA0`), `00292260` (95 B — `002F8040` ×3 + `002491B0` ×2), `00563520` (42 B — `002486B0` + `00292260`) | small clears, wrappers, and the pointer-table installer |

The subtree's shape is the init half of BE-6's pump: what the per-frame `0017D6E0` advances at
runtime, `0017D4C0` constructs at boot — ~23 ensure-stubs populating the contiguous global block,
then the constructors that fill them. `0022A0B0` (the boot subtree root, documented on
[what-the-engine-fixes-at-boot](../what-the-engine-fixes-at-boot.md)) appears *inside* `0017D4C0`'s
call sequence — application setup calls back into the boot layer rather than the reverse.

## The `001BBFC0` exclusive subtree — all 13 members bound (SWE2-FRONTIER, followup queue)

`001BBFC0` is the `Ensure` for **`01F81240`** — the still-unnamed `0x238` singleton whose update
`001BC190` is the pump's largest body (§"What slot 4 drives"). The exclusive-callee census assigns
it **13 frontier functions**, all in the `001B8xxx`–`001BBxxx` band: the singleton's private
record-container layer plus one shader request. Interior cites are one instruction inside each
declared extent (`interior_cite.py scan`; no boundary crossings).

| cluster | members | role | interior |
|---|---|---|---|
| record ctor | `001B9370` (417 B), `001B9260` (258 B) | `001B9370` is the `0x238` object's constructor: six `001EDF00` allocator fetches, container init `001B8E90`, `00220760`/`00861EC0`, and it issues the shader request `001BB190`. `001B9260` is the `0x2A8` element's default ctor — own vtable store, `001EDF00` ×2, `00861EC0` ×2 | `001B938B` / `001B927D` |
| element copy | `001B90F0` (368 B), `001B8950` (372 B), `001B8810` (311 B) | the `0x2A8` record's copy-ctor (own vtable, `+0x8`/`+0x48`/`+0xA0` fields, string copy `001B9020`), the per-element copy loop (`001B9970`), and the vector copy-assign inner loop | `001B90FA` / `001B8964` / `001B8840` |
| vector range ops | `001B8600` (523 B), `001B8AD0` (486 B), `001B8CC0` (453 B), `001BA470` (742 B) | stride-`0x2A8` move/copy range, two fill/fill_n loops over `001B9020` string copies, and `001BA470` — the composite vector-assign that drives all five | `001B8640` / `001B8AF8` / `001B8CEA` / `001BA485` |
| container init | `001B8E90` (390 B) | the `001EDF00`-apply shape (×4) + `005CC8A0`/`00199DB0`/`005CD0A0`, then `001BBE00` — EASTL `vector`/`set` asserts | `001B8EB5` |
| bulk fill + sweep | `001BBE00` (316 B), `001BA990` (157 B) | `001BBE00` fills `[begin,end)` with the `0x606060…` 8-byte pattern then runs `001B9260`/`001BA470`/`001BA990`; `001BA990` sweeps a list calling `vtable[0]` on each node | `001BBE40` / `001BA9BD` |
| asset request | `001BB190` (276 B) | formats `"./GameData/%s/ArtData/shaders/anisolighting.dds.phyre"` (`0017D2E0`) and runs the `0019CE20`/`0019CB20`/`0063DA50`/`0063B010` request chain — the one concrete asset the singleton loads; `02CBB900` involved | `001BB1BE` |

The subtree says more about the unnamed singleton than §"What slot 4 drives" had: it owns a
vector of polymorphic `0x2A8` records, it bulk-patterns a buffer at init, and — the strongest
identity hint yet — its constructor requests the **`anisolighting`** Phyre shader. The
`0x238`-byte object is a render-side record manager; the aniso-lighting request narrows which
side, but the name stays unclaimed.


## The `00229590` exclusive subtree — all 8 members bound (SWE2-FRONTIER, followup queue)

`00229590` is the **PauseMenu message handler** named in the pause-flag paragraph above
(command-id dispatch on `[rdx]`: ids 1, 2, 4, 0xF, plus a `005C5230` default arm; the
`"PauseMenu Create
"` / `"PauseMenu Open
"` prints sit in the id-2/id-4 arms). The
exclusive-callee census assigns it **8 frontier functions** — the small bool-setter adapters the
open/close arms use to write the pause flag and its three neighbours. Every member was
disassembled from the shipping image; interior cites are one instruction inside each extent.

| member | role | interior |
|---|---|---|
| `0017E720` (32 B) | **the pause-flag setter** — bool-normalises `ecx`, fetches the `[01F810F0]` singleton via `001997D0`, writes the byte through `001997E0`. The open arm's `0017E720(1)` / close arm's `0017E720(0)` calls (`002298C1` / `002297B0`) | [`0017E72B`](../../_index/ADDRESS-INDEX.md) |
| `00183200` (50 B) | sets byte `+0` of the lazy 3-byte singleton `0018A7D0` (`[01F7F5D8]`), and clears the word at `+1` when the value is 0 — via `0018A820` | [`00183208`](../../_index/ADDRESS-INDEX.md) |
| `00182FF0` (50 B) | sets byte `+2` of the same `0018A7D0` singleton — via `0018A830` | [`00182FF8`](../../_index/ADDRESS-INDEX.md) |
| `0018A820` (13 B) | `[rcx]=dl`; when `dl==0` also writes word `[rcx+1]=0` — a flag-plus-shadow setter | [`0018A820`](../../_index/ADDRESS-INDEX.md) |
| `0018A830` (4 B) | `[rcx+2]=dl` — the second flag byte | [`0018A830`](../../_index/ADDRESS-INDEX.md) |
| `00181E10` (32 B) | bool-normalises `ecx`, fetches the lazy `0x2E0` singleton `001EBA40` (`[01F82E18]`), tails `001EBC70` | [`00181E1B`](../../_index/ADDRESS-INDEX.md) |
| `001EBC70` (60 B) | writes `[rcx+0x26E]=dl` on the `0x2E0` object; when its `+0x134` index is not `-1`, forwards the value to `002EF250(index, flag)`, which sets/clears bit `0x800000` on the resolved record — an entity-level show/hide toggle (the `dl==0` arm is skipped while `[rcx+0x26D]` holds) | [`001EBC8F`](../../_index/ADDRESS-INDEX.md) |
| `00180120` (39 B) | a two-predicate conjunction — `001EC5C0()` (`movzx` of `0020AA30()`) **and** `001EC560()` (mode-indexed probe: `[01DFE40C]` ≤ 4 indexes `01F832B0[]`, nonzero runs `00265680`); run by one arm at `00229A53` | [`0018012D`](../../_index/ADDRESS-INDEX.md) |

The `0018A7D0` singleton (3 bytes: a flag, a word shadow, a second flag) and the `0x2E0` object
(lazy `00210EC0` + `001EB190` ctor) sit just below the pause flag in the menu's write set — the
handler's open arm touches all four in one run. What `0018A7D0`'s pair gates, and which
subsystem `001EBA40` belongs to, the bodies do not name.


## The `0022A580` exclusive subtree — all 8 members bound (SWE2-FRONTIER, followup queue)

`0022A580` is the **frame dispatcher's prologue** (465 B): the pause-flag mirror §"slots 21/22"
names, the mode-change detect on `02064AD3`, the worker-deadline enqueue + drain the input-stack
page's poll chain hangs from, and the mode-jump dispatch into the six frame bodies
(`0022B6E0`/`0022B7E0`/`0022B8C0`/`0022BC20`/`0022AF50`+`001E0580`/`0022B000`+`001E0580`/
`0022A770`). The exclusive census assigns it **8 frontier functions** — the input-worker queue
machinery plus two config readers. Every member was disassembled from the shipping image;
interior cites are one instruction inside each extent.

| member | role | interior |
|---|---|---|
| `0035E9B0` `InputControl_QueueWorkerDeadlineAndMarkDirty` (60 B) | stores `xmm0` into the `022CA640[idx]` deadline ring, `00863800([022CA610])` releases the worker semaphore, `idx=(idx+1)&0xFF` at `022CA638`, tails `0035FF80` | [`0035E9C1`](../../_index/ADDRESS-INDEX.md) |
| `0035FF80` (11 B) | `[022CAE80]=1` — the queue-dirty flag `00360080` tests | [`0035FF80`](../../_index/ADDRESS-INDEX.md) |
| `00360080` (53 B) | when `022CAE80` is set: `n=00184950()`, loops `00369170` n times — the per-frame queue drain | [`003600A0`](../../_index/ADDRESS-INDEX.md) |
| `00369170` (25 B) | `00369080()` then `00863650([022D7F90])` — one drain step | [`00369174`](../../_index/ADDRESS-INDEX.md) |
| `00369080` (104 B) | pops count `022D7FB4`, spins on `022D7F70`, runs `00863520(entry,0x24)` then `00863520(entry,0x22)` — two engine ops per queued entry | [`003690C0`](../../_index/ADDRESS-INDEX.md) |
| `0035E9F0` (14 B) | `rcx=[022CA618]`, `edx=0`, tails `00863690` — a zero-arg engine call on the worker object | [`0035E9F9`](../../_index/ADDRESS-INDEX.md) |
| `00184AD0` (18 B) | `movzx [001C18E0() +0x41]` — a config-byte reader run first in the prologue | [`00184AD4`](../../_index/ADDRESS-INDEX.md) |
| `001E0560` (29 B) | sticky latch: `al=[01F82D30]`; when `[01F82D31]` is set the stored byte is forced to 1 — run by two of the dispatch arms | [`001E056C`](../../_index/ADDRESS-INDEX.md) |

Two corrections land with the census. First, the pause-flag mirror at `0022A67A` writes
**`02F974A0`**, not `02D914A0` — the `mov [rip+0x2D6CE20], eax` resolves to `02F974A0` in the
shipping image (the slots-21/22 paragraph above is corrected accordingly). Second,
`0035E9B0`'s ledger name understates the pair: the deadline enqueue and the dirty-mark are the
*same* call — `0035FF80` is its tail, not a separate step.

## The `001B7EE0` exclusive subtree — all 5 members bound (SWE2-FRONTIER, followup queue)

`001B7EE0` is the BE-6 slot's `Ensure` for **`Phyre::PCameraPerspective`** — the table's
"lazy allocator" shape confirmed from the shipping image: it probes the singleton cell
`[01F81218]`, and when null runs `00210EC0(0xBB8)` then the object ctor `001B6D90` and
stores the result back at `001B7F14`. It owns **5 frontier functions**; every member was
disassembled and each interior cite sits inside its declared extent.

| member | role | interior |
|---|---|---|
| `001B6D90` (264 B) | the `PCameraPerspective` ctor: zero/`-1` scalar head, `+0xC`/`+0x28` = `1.0f`, `+0x2C` = `0x100`; `00633040(+0x30)`, `00615CD0(+0xD8)`, `006160B0` on `+0x108`/`+0x290`/`+0x418`; then the `+0x5A0` embedded sub-object — `00184E60(+0x5A8)`, vtable `008C5D68` at `+0x5A0`, `+0x668`/`+0x674` = `1.0f`, **`+0x670` = `3F490FDB` (π/4 — the default perspective FOV)**, `00189C20(+0x5A0)`; tail `006791B0(+0x678)` | [`001B6DD1`](../../_index/ADDRESS-INDEX.md) |
| `006791B0` (267 B) | the camera's `+0x678` sub-object ctor: three `006CC350` children at `+0`/`+0xA8`/`+0x150` (0xA8 stride), three `005CC900` children at `+0x1F8`/`+0x218`/`+0x238` each followed by a zeroed flag byte, `006CC960(+0x290)`, `00679130(+0x488)`, two `00874D60` children at `+0x4F8`/`+0x508`, then a `+0x258`–`+0x538` zero tail | [`00679224`](../../_index/ADDRESS-INDEX.md) |
| `006CC350` (180 B) | 0xA8-stride child ctor: vtable `00D89A80` at `+0`, `00874D60` on `+0x28`/`+0x38`, `+0x58` = `00584730` (a release-callback slot), `00808FE4(+0x60, 0x20, 2, 006CC330)` — a 2-slot container of 0x20-byte elements with an element init callback — then `0018B320(+0x60, 4)`/`0018B320(+0x80, 4)` reserve-4 on two lists | [`006CC3C6`](../../_index/ADDRESS-INDEX.md) |
| `006CC960` (22 B) | leaf ctor: vtable `00D89B00` at `+0`, `+0x10` = 0 | [`006CC967`](../../_index/ADDRESS-INDEX.md) |
| `00679130` (120 B) | the `+0x488` child ctor: vtable `00D6CD90` at `+0`, `00874D60` on `+0x30`/`+0x48`, then a paired enable pattern — `005CD0E0(+0x30, 1)` sets flag `+0x38`, `005CD0E0(+0x48, 0)` sets flag `+0x50` | [`0067915E`](../../_index/ADDRESS-INDEX.md) |

`00210EC0` (the singleton allocator), `00633040`, `00615CD0`, `006160B0`, `00184E60`,
`00189C20`, `005CC900`, `00874D60`, `00808FE4`, `0018B320`, `005CD0E0` and `00584730`
are shared callees with other callers — deliberately not census members.

## 9. Related

- [`../Object-Model/vtable-method-index.md`](../Object-Model/vtable-method-index.md) — the index this
  class was selected from, and the object-size census across the whole game-specific set.
- [`../../17-Presentation-Rendering/Character-Rendering/character-render-object.md`](../../17-Presentation-Rendering/Character-Rendering/character-render-object.md)
  — the other class carrying the same one-way latch idiom.
- [`../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md`](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md)
  — the archive format this slot mounts.
- [`../../22-Middleware-PhyreEngine/`](../../22-Middleware-PhyreEngine/) — `GameApplication` derives
  from `Phyre::PFramework::PApplication`; §11 enumerates the twelve-class framework vtable cluster.

## Interior citations — entry-only-large pass (2026-09-14, SWE2-FRONTIER)

This document named these bodies only at their entries. Each interior address was read in the
shipping image; the notes say what the instruction does, not yet the body's full role.

| body | interior cite | what is there |
|---|---|---|
| `00187950` | `00187A7A` | `mov dword ptr [rip+…], …` — writes `01DF0900` inside the render pass list this page's §3 slot 8 names |
| `001BC190` | `001BC536` | `movss xmm0, dword ptr [rip+…]` — loads the `01CEBBA8` float constant near the tail of this `0017D980`-calling body |
| `0079C140` | `0079C276` | `mov dword ptr [rip+…], eax` — writes `02EAC980`, a two-field block (`+0` count, `+4` float) the body fills between `005CD4F0` and `0079EBA0` calls |
| `00189CE0` | `00189D4C` | `call _Init_thread_header` — TLS-init bracket around a `0018A620` call run; also writes `02EAED3C` |
| `001C2F50` | `001C30B2` | `mov dword ptr [rip+…], …` — writes `01F81278` after storing `r15` to `01DF6E38`; five distinct `001FExxx`/`00200xxx` callees |

*(Pass 22 adjacency, 2026-09-14: the application root's init path crosses into the layers it
brings up — `0022A0B0`, the startup chain's second hub, calls **actor** `002368D0` and **rng**
`00379CF0`; `0022A770` calls **party** `00358BB0`; and `0032E620` is called by **actor** bodies
`0032FCA0`/`00330310` — 5 edges. Root code that initialises the actor store, party state and the
random stream necessarily lands in their layers; the direction is init-out, not ownership-in.)*

*(Pass 22 live-graph completion, 2026-09-15: the init path's reach continues — `002368D0`
calls `Movement` `00383A20` and `CombatAction` `0030CF40`, and `00358BB0` is called by
`Movement` `0026C3E0` (3 edges). Startup code initialises locomotion and combat state on the
way through; init-out, not ownership-in.)*

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Developer — CLIENT and SERVICE, not read.** Two cited functions are called by Developer-labelled bodies (2,261 and 1,046 bytes), and one cited function calls the 1,046-byte one. Which developer facility those bodies are is not read here.
- **CombatFormula — MECHANICAL (SWE2-EC7-97, 2 edges).** `00319F50` — the tail target this page's
  `002EB740` section names — calls `00300520` and `00385F60` on the CombatFormula layer.
  Shared-helper fan-out; no CombatFormula relationship to the application root.
- **Gameplay — MECHANICAL (SWE2-EC7-97, 2 edges).** The same `00319F50` calls `00316D70` and
  `003176E0` on the Gameplay layer. Shared-helper fan-out; no Gameplay relationship to the
  application root.


**Audio — CLIENT (SWE2-EC7-162, 173 edges).** The application's subjects are consulted by the
Audio layer (`0016D6D0` is called by `002187D0`/`002199C0`/`00219D80`/`0021AF80` there) - the app
root's helpers fan into the audio path; consultation, not shared ownership.

**Input — CLIENT (SWE2-EC7-162, 222 edges).** `0017CDC0`/`0017CDF0`/`0017CE20`/`0017CE50` call
Input-layer bodies `0079BF70`/`0079D560`/`0079D5B0`/`001967D0` - the application reads input
state through its own subjects; consultation, not shared ownership.

**Presentation — CLIENT (SWE2-EC7-162, 763 edges).** `0016D680` and neighbours are called by the
Presentation layer (`00183A00`/`00183C60`/`00183EE0`/`001946xx`) - the app root is the layer's
widest client surface; no shared ownership.

**Resource — CLIENT (SWE2-EC7-162, 419 edges).** `0016D6D0`/`0016D720` are called by
Resource-layer bodies `0020B840`/`0020BFA0`/`006761F0`/`00676000` - the application's load path
is consulted from the resource side; consultation only.

**Platform and PlatformOnlineAchievements — shared helpers.** The `00676BD0` id-map entry names CRT/runtime-support callees (`008092FC`/`0080929C` TLS once-init, `00808B90` atexit registration, `001A5630` string construction, `00861ED2` compare, plus the `0016D6D0`/`0016DA60` freelist pair this page already cites) whose remaining call traffic comes from Platform and PlatformOnlineAchievements bootstrap bodies (`007A0810`, `007A0C60`, `001F3ED0`, `0079FA00`, `0019CC50`, `001B1960`) - the registry borrows shared utility code; no Platform or achievements responsibility moves here.

**World_Area_Field — CLIENT (shared-callee edges, SWE2-EC7-189).** The format dispatcher `001CD0E0` and the `0017D280`/`001EC560`/`001D5520` helpers this page names are also consulted by the world-area field layer (`00265270`/`00314910` callees, `00314020`-family callers). The crossing is that layer calling shared primitives this page happens to host, not shared responsibility. Edge list from `edges.tsv`.
- **CombatAction — SERVICE (4 edges).** 4 outbound (page-cited `BattleUnit_HandleActorTimelineEvent` (00319F50), `BattleStorage_InitializeWorkArrays` (002368D0), `ActorTimeline_DispatchEventToBattleUnit` (002EB740) call CombatAction bodies `BattleAction_ResetPresentationSlotPool` (0030CF40), `BattleUnit_HandleActorTimelineEvent` (00319F50), `00306BB0`). Substantive edges include `BattleStorage_InitializeWorkArrays` (002368D0) calls `BattleAction_ResetPresentationSlotPool` (0030CF40); the remaining edges run through shared helpers the page cites.
- **Movement — CLIENT and SERVICE (33 edges).** 19 inbound (Movement bodies `0026C3E0`, `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00), `PartyFollow_SolveFormation` (00338490) call page-cited `002324F0`, `0026E500`, `0026C3E0`); 14 outbound (page-cited `003B8670`, `MainLoop_UpdateAndRenderFrame` (0022B8C0), `0022FFE0` call Movement bodies `00263560`, `0037CF00`, `002324F0`). Substantive edges include `001EC5C0` is called by `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00); `MainLoop_UpdateAndRenderFrame` (0022B8C0) calls `00263560`; `MainLoop_UpdateAndRenderFrame` (0022B8C0) calls `0037CF00`; `0022BC20` calls `00263560`; the remaining edges run through shared helpers the page cites.
- **Script_VM_Native_Bridge — CLIENT (45 edges).** 45 inbound (Script_VM_Native_Bridge bodies `0050D240`, `0050D780`, `0050CE40` call page-cited `0017D280`, `InputDevice_QueryAvailabilityState_Always1` (0053DD10), `001EC5C0`). Substantive edges include `001EC5C0` is called by `0034CF90`; `001EC5C0` is called by `0034D790`; `00265680` is called by `00343690`; `0032E620` is called by `0050DFE0`; the remaining edges run through shared helpers the page cites.
- **Status_Periodic_Terminal — CLIENT (1 edge).** 1 inbound (Status_Periodic_Terminal bodies `BattleUnit_RunPeriodicCombatMaintenance` (00310DB0) call page-cited `00265680`). Substantive edges include `00265680` is called by `BattleUnit_RunPeriodicCombatMaintenance` (00310DB0).
- **StoryEvent — CLIENT (1 edge).** 1 inbound (StoryEvent bodies `001ED240` call page-cited `001EC560`). Substantive edges include `001EC560` is called by `001ED240`.
- **UI — CLIENT and SERVICE (38 edges).** 36 inbound (UI bodies `002A0440`, `0018EEE0`, `00253780` call page-cited `00249410`, `00202C70`, `00181890`); 2 outbound (page-cited `0022A770`, `00250540` call UI bodies `00254E50`, `00367200`). Substantive edges include `00228480` is called by `00276D30`; `0022A770` calls `00254E50`; `002491B0` is called by `00253780`; `00249810` is called by `00247AE0`; the remaining edges run through shared helpers the page cites.
- **Script_VM_Native_Bridge — CLIENT (45 edges).** 45 inbound (Script_VM_Native_Bridge bodies `0050D240`, `0050D780`, `0050CE40` call page-cited `0017D280`, `InputDevice_QueryAvailabilityState_Always1` (0053DD10), `001EC5C0`). Substantive edges include `001EC5C0` is called by `0034CF90`; `001EC5C0` is called by `0034D790`; `00265680` is called by `00343690`; `0032E620` is called by `0050DFE0`; the remaining edges run through shared helpers the page cites.
## The `001D7A20` exclusive subtree — all 4 members bound (SWE2-FRONTIER, followup queue)

`001D7A20` (932 B) is the four-quad screen-setup battery — the body §"render pass"
names as running "from the slot-4 pump through" the pass list. It snapshots a 2×2
integer grid from `rdi` (`word[+0]`/`word[+2]` added into the split halves,
`001D7AE4`–`001D7B31`), `001FBE30`/`001FBD80` bracket a mode check (`001D7B35`–
`001D7B44`), then `001B1910` and member `001D8600` configure the field object
(`001D7B49`–`001D7B59`). A `0x30`-stride four-record array is built at `rsp+0x70`:
each record's float pair is `grid − gated × float[01DEBBB8] + float[01D52F30]`
where the gated constant is chosen by the `001B1620()`-then-`+0x3A98`-clear test —
the exact predicate members `001D70D0`/`001D7110` wrap standalone — with fixed
`+0x4 = 0`, `+0x8 = 1.0f`, `+0xC`/`+0x10`/`+0x14 = 0x7F`, `+0x18 = [001D8A60()+0x28]`,
`+0x24 = 1` (`001D7C00`–`001D7CD2`). When `0018A7D0()`'s first byte is clear,
`001D8790` runs over the first record (`001D7D46`–`001D7D57`); all four records then
apply through `001B06D0` and `001B03D0` finalises (`001D7D5C`–`001D7D83`).

| member | role | interior |
| --- | --- | --- |
| `001D70D0` (53 B) | gated float getter — `001B1620()` passes and `[001B1C00()+0x3A98]` clear → `float[008C5B58]`, else `float[008C5B44]` | [`001D70EB`](../../_index/ADDRESS-INDEX.md) |
| `001D7110` (53 B) | the second getter — same gate, `float[008C5B5C]` / `float[008C5B48]` | [`001D712B`](../../_index/ADDRESS-INDEX.md) |
| `001D8600` (83 B) | field-object mode set — `001B22E0(obj, 0x3001)`, `001B22D0(obj, 0x44)`, `001B22F0(obj, 1, 1, 0, 0, 0)` on `001B1C00()`'s return | [`001D8611`](../../_index/ADDRESS-INDEX.md) |
| `001D8790` (569 B) | the corner transform — `001D8210` thrice for the grid halves, `001D7110`/`001D70D0` for the gated scales, CRT `00861F0E`/`00861F08` trig with a sign-mask flip at `01DEBDA0`, then a 4-iteration loop building corner positions centred on the halved grid (`001D88A0` onward) | [`001D8839`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `001B1620`/`001B1C00` (the gate + object fetch),
`001B1910`/`001B22E0`/`001B22D0`/`001B22F0`/`001B2490`/`001B2410` (the field-object
setters), `001D8A60`/`001D8210` (accessors), `0018A7D0`, `001B06D0`/`001B03D0` (the
apply pair), `001FBE30`/`001FBD80`/`001FBE50` (the mode bracket), the CRT trig and
`00808C40`. What the four `0x30` records *are* — the geometry they describe — is
upstream of this subtree; `001B06D0` is shared.

## The `001C2F00`/`001D72F0` exclusive-subtree pair — both roots bound (SWE2-FRONTIER, followup queue)

`001C2F00` — lazy singleton alloc: `qword[01F81270]` null →
`00210EC0(0x4670)` (`001C2F17`/`001C2F1C`) then `001C1D40` on the
result (`001C2F2B`). The `0x4670` size and the member's `008F9DC8`
vtable (slot 0 = `001C2670`, the deleting dtor bound earlier) close the
`MultipleDebugDisplay` triangle: ctor `001C1D40`, dtor `001C2670`,
alloc-site `001C2F00`.

| member | role | interior |
| --- | --- | --- |
| `001C1D40` | `MultipleDebugDisplay` ctor — installs `008F9DC8` under EH guard (`001C1D5D`/`001C1D64`) | [`001C1D5D`](../../_index/ADDRESS-INDEX.md) |

`001D72F0` (~450 B) — application op opening on `001997D0` with a `0x1C0`
frame (`001D7319`).

| member | role | interior |
| --- | --- | --- |
| `00252840` | autosave-window trigger — `00583920` gate → `001EB150("display AutoSave Window")`, `001FBD80(1)`, `0017FC50`, `0039BDA0` (`0025284D`/`00252868`) | [`0025284D`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00210EC0`, `001997D0`, `00583920`,
`001EB150`, `001FBD80`, `0017FC50`, `0039BDA0`.

## The `007939A0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`007939A0` (~234 B) — `rbx`-save body that reads `rax = [rdx]` at
`007939AA` and copies the application-record span this page describes
(`+0x177` tail, copied whole at `00793B88`).

| member | role | interior |
| --- | --- | --- |
| `00793DA0` | copy/clone body | [`00793DA0`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## Interior citation — frontier hub `005CDAA0` (2026-09-17, SWE2-EC7)

`005CDAA0` — 239 B, 77 frontier callers at census (the settings-init band calls it six times).
Interior verified: [`005CDAAB`](../../_index/ADDRESS-INDEX.md) sits in the entry block that reserves
a 0x4050-byte frame under `_chkstk` (`00808F10`) and installs the stack cookie — the entry of the
**formatted log call** that
[the formatted-log-call-and-its-level-gate page](../Diagnostics-Logging/the-formatted-log-call-and-its-level-gate.md)
decoded end to end: `__stdio_common_vsprintf` into a `0x4000` stack buffer, then the
`_Init_thread_epoch` check on the TLS slot at `gs:[0x58]`-indexed `[+4]` vs guard `02CB6158`,
one-time sink init `005CDA30` under `_Init_thread_header`/`footer` (`008092FC`/`0080929C`), then
emit through sink vtable slot 1 (`call [rax+8]`, channel in `edx`, buffer in `r8`). The epoch
compare is the magic-static guard, **not** a level gate — the page's §9 correction stands.

NOT claimed: which class implements the sink (the diagnostics page's open question).

## Interior citation — frontier hub `001A5760` (2026-09-17, SWE2-EC7)

`001A5760` — 154 B, 10 A-measured callers at census; the helper `001B3290`/`001B3320` forward
into. Interior verified: it is the string insert/replace half of the assign family
(`001A4BF0` grows, this inserts in place). When the `[rdx,r8)` span fits the `{begin,end}`
capacity at `[rcx]` it `memmove`s the tail aside via the `008C2A40` IAT slot
([`001A5792`](../../_index/ADDRESS-INDEX.md)) and advances `end`; otherwise it spills to the grow
path through `001A52A0`. Returns the container in `rax`.

## Interior citation — frontier hub `001A52A0` (2026-09-18, SWE2-EC7)

`001A52A0` — 332 B, 8 A-measured callers; the insert-at-position the console path above
returns through. Interior verified: a byte-container `{begin@0, cur@8, capEnd@0x10,
allocator@0x18}` with 32-bit offset fields; `insert(rdx=pos, r8=end)` no-ops on empty range
(`001A53E0`). When `cur-begin-1 + (end-pos)` exceeds capacity, `newcap = max(2*cap, needed)+1`
with a floor of 8 (`001A52EA`–`001A5304`), the allocator's vtable `+0x10` supplies the new
buffer at [`001A530F`](../../_index/ADDRESS-INDEX.md), head and inserted ranges copy via the `008C2A40`-table
indirect moves (`001A5325`/`001A533A`), old storage frees through slot `+0x18`, and the
triple rewrites at `001A537F`–`001A538E`. The in-place arm memmoves the tail up
(`001A53B1`), plants the byte, bumps `cur` by the insert length.


## Interior citation — frontier hubs `001BA860`, `001D6F20`, `0017F370` (2026-09-18, SWE2-EC7)

`001BA860` — 168 B, 6 A-measured callers; a locked deferred-list drain. Interior verified: when
`[rcx+0xB8]` is set it takes the `005CD4F0` lock on `rcx+0x90` (`001BA876`–`001BA87D`), then while
`[+0x48]` is nonzero it pops the `[+0x30]`-headed list by `[+0x20]` links, decrements the count
(`001BA899`), runs `0016D6D0` + `0016DA60` per node ([`001BA8A1`/`001BA8AD`](../../_index/ADDRESS-INDEX.md))
and issues the vcall `[+0x50]->[+0x18]` with `r8d = 0x28` (`001BA8C3`).

`001D6F20` — 122 B, 6 A-measured callers; the `0x30`-record factory paired with `001D6E80`'s
teardown. Interior verified: `operator new(0x30)` via `00210EC0` (`001D6F34`), `00597930`
constructs with `(rdi, setne(edx!=0), 1)` ([`001D6F4D`](../../_index/ADDRESS-INDEX.md)),
`0059D900` validates; on failure it unwinds through `0016D6A0` + `free`/`00809950` (`001D6F7A`)
and returns NULL.

`0017F370` — 50 B, 6 A-measured callers; an on/off publish adapter. Interior verified:
`0018CA40()` supplies the shared object twice (`0017F378`, `0017F387`); the `ecx` arg becomes
`setne` boolean `edx` ([`0017F384`](../../_index/ADDRESS-INDEX.md)); tail-jmp `0018BAB0` at
`0017F397`. No state kept.


## Interior citation — frontier hubs `00199DB0`, `005CD0A0`, `00616700` (2026-09-18, SWE2-EC7)

`00199DB0` — 341 B, 45 callers (5 A-measured); the ordered-map emplace the `0016D840`
red-black users listed above all funnel through. Interior verified: descent by
`key < [node+0x20]` picking `[+8]`/`[+0]` children (`00199DF0`–`00199E0C`), `0016D720` steps to
the in-order predecessor for the equal-key check ([`00199E23`](../../_index/ADDRESS-INDEX.md)),
the `[+0x30]` allocator's slot-`0x10` vcall makes the `0x28` node (`00199E70`/`00199EB0`),
`0016D840` links and rebalances ([`00199E8E`/`00199ECE`](../../_index/ADDRESS-INDEX.md)),
`[+0x28]` counts, and the result is the `{iterator, inserted}` pair at `[rsi]`/`[rsi+8]`.

`005CD0A0` — 63 B, 32 callers (5 A-measured); the armed-once init gate. Interior verified:
`byte [rcx] == 0` required (`005CD0A6`), `005CD0E0(rcx+8, 1)` does the work
([`005CD0BC`](../../_index/ADDRESS-INDEX.md)), `[+0x10] = 1` marks the attempt, and only a zero
return flips `[rcx]` to 1 (`005CD0CE`). Failed inits stay armed for retry.

`00616700` — 59 B, 21 callers (5 A-measured); another `_Init_thread`-epoch guard, sibling of
`005CDAA0` documented above. Interior verified: `005FCF20()` returns the TLS object
(`00616704`/`00616727`), `00225690` reads the epoch state and `== 1` gates the `005FD050`
singleton touch ([`00616721`](../../_index/ADDRESS-INDEX.md)), then `005CD7D0` runs on the TLS
object every call (`00616730`). The `0xFFFFFFFFFFFFFFFE` local at `00616704` is the epoch
sentinel the guard compares against.


## Interior citation — frontier hubs `0016D6A0`, `005C5230`, `0053DD10` (2026-09-18, SWE2-EC7)

`0016D6A0` — 3 B, the `ret 0` folded leaf this page already cautions about (2,479 callers;
1,515 via data slots). Interior verified at [`0016D6A2`](../../_index/ADDRESS-INDEX.md): the
whole body is `c2 00 00` — stdcall-style `ret 0`, ignoring every argument. That is why
`/OPT:ICF` folded it across dozens of distinct sources: any empty thiscall-shaped destructor
or no-op callback collapses onto it.

`005C5230` — 3 B, 358 callers; `PApplication` slot-8's empty override noted above.
Interior verified: `xor eax, eax; ret` ([`005C5232`](../../_index/ADDRESS-INDEX.md)) — a
constant-0 default arm, the "framework callback the game overrides" claim confirmed in bytes.

`0053DD10` — 6 B, 34 callers; `InputDevice_QueryAvailabilityState_Always1`.
Interior verified: `mov eax, 1; ret` ([`0053DD15`](../../_index/ADDRESS-INDEX.md)) — the name
is literal: the availability query is hard-wired true.

## Interior citation — frontier hub `0061D9C0` (2026-09-18, SWE2-EC7)

`0061D9C0` — 535 B, 12 callers; the effect-font materialisation consumer. Guarded on
`[rcx+0x20] == 0`, it pulls the `005FD050` magic-static singleton, requires `[+0x108]`
present, then decodes the packed record bytes `[rbx+0..4]` into the odd ladder of
`sub edx, r8d` case-tests (`0061DA55`–`0061DAE8`), scales three byte channels and a
`[+0x10]` byte by the float constant at `00D11104`
(`cvtdq2ps`/`mulss` at `0061DB32`–`0061DB67`), and virtual-calls `[rax+0xB8]` on the
singleton's `[+0x108]` object ([`0061DB77`](../../_index/ADDRESS-INDEX.md)) with the staged
parameter block. On success (`eax >= 0`) it re-invokes `0061C550` against `[rbx+0x20]` with
the `00D36620` "PSamplerState" literal and sets `[rbx+0x1C] |= 0x80`; any earlier exit
returns `0xE`.


### Interior citation — frontier hub `0018A7D0` (2026-09-18, SWE2-EC7)

`0018A7D0` — 67 B, 6 callers: the lazy 3-byte singleton behind `00183200` /
`00182FF0` above. When `[01F7F5D8]` is null it calls `00210EC0(3)`, and on a
successful allocation writes `word[rax] = 0`, `byte[rax+2] = 0`
([`0018A7F2`](../../_index/ADDRESS-INDEX.md)) before publishing the pointer — the
three flag bytes the setters write `+0`/`+1`/`+2` on. A failed allocation leaves
the global null, so every call site re-attempts.

### Interior citation — frontier hub `005CC8A0` (2026-09-18, SWE2-EC7)

`005CC8A0` — 25 B, 35 callers. Read from the shipping image: a 0x28-byte record
zero-initialiser — `byte[rcx]=0`, `qword[rcx+8]=0`, `byte[+0x10]=0`,
`dword[+0x18]=0`, `dword[+0x20]=0`, `dword[+0x24]=0`
([`005CC8A5`](../../_index/ADDRESS-INDEX.md)) — returning `rcx`. The shared
clear-on-alloc leaf the constructor cluster calls.

### Interior citation — frontier hub `001BA910` (2026-09-18, SWE2-EC7)

`001BA910` — 119 B, 7 callers (`001B9260`, `001BC190` cluster above): the
intrusive-list teardown — walks the `[rcx+0x18]` chain calling `001BA760` then
each node's vtable `+0x18` slot with `(node, 0x58)` at
[`001BA950`](../../_index/ADDRESS-INDEX.md); afterward `[rbx+0x10]`/`+0x18`
re-form the empty list head and `+0x20`/`+0x28` zero. The destroy half of the
container pair the ctor cluster allocates.
## SWE2-EC7-18 update (2026-05-15) — `001B2410` field-object record swap + `00249810` arg-setup

`001B2410` (117 B) is the field-object parameter commit this page's group lists: `[rcx+0x3930]=edx` and `[rcx+0x3934]=r8d` (`001B2416`/`001B241F`), then `r9==0` writes `[rcx+0x3938]=0` while a non-null `r9` is formatted into `+0x3938` by `0017D2E0` (`001B243E`), and six stack-passed values `[rsp+0x50]`..`[rsp+0x78]` land at `+0x3AA0`, `+0x3A38`, `+0x3A3C`, `+0x3A40`, `+0x3A44`, `+0x3A48` (`001B2443`..`001B2479`) — the (id, kind, name, six-params) record fill the container runs when a field object is (re)parameterized.

`00249810` (42 B) is the three-call allocation wrapper the pkfl page shows as `00249810(2, result)`: `ebx=edx` saves the argument, `0036C1D0` runs with `edx=0xC` (`0024981D`), `0036A190` runs on the saved `ecx` (`00249824`) into `rbx`, `0036C140` finishes (`0024982C`), returning `rbx` — the kind-`0xC` `0036xxxx` allocate/resolve pair this page's group calls during container init.

## SWE2-EC7-19 update (2026-05-15) — `00874D60` one-qword null initializer

`00874D60` (11 B) is the smallest child-ctor helper the camera/ctor cluster uses: `mov qword ptr [rcx],0` + `mov rax,rcx` + `ret` — a pointer-field null initializer the cluster's ctor rows (`006791B0`, `006CC350`, `00679130` above) invoke on their `+0x28`/`+0x38`/`+0x30`/`+0x48`/`+0x4F8`/`+0x508` slots, consistent with those rows naming it as the slot-zeroing child.

## SWE2-EC7-29 update (2026-09-18) — `00874D60` single-qword null init

`00874D60` (11 B) is the zero-init child the ctor tables above name for
the `+0x130`/`+0x28`/`+0x38`/`+0x30`/`+0x48`/`+0x4F8`/`+0x508` slots:
`mov qword[rcx],0; mov rax,rcx; ret` — a single-qword null
initialisation returning its argument, the smallest constructor the
sub-object ctors share. Interior anchor `00874D67` (the
`mov rax, rcx` return).

## 160 bytes of `BootSingleton01F7F598` were unobserved only because the census stopped at a call (2026-09-18, OPUS)

`singleton_field_scan.py` censuses this singleton by tainting the register its pointer slot
`01F7F598` is loaded into, and against the type store it reported **0 offsets inside any
unobserved span** — the layout looked settled as far as that instrument could see. It also said,
in its own closing line, exactly why that was a floor: *"the taint does not enter callees, does
not survive a call."*

It does not, and almost nothing reaches this object that way. **Only four bodies in the image
reference the slot at all** — `001862B0`, `00187950`, `00189000`, and `00189120`, which is eight
bytes of `mov rax, qword ptr [rip->01F7F598]; ret`. **That accessor is how the rest of the engine
gets the singleton**, and it has **117 callers**. Seeding from those callers with the accessor's
**return value** tainted, then closing over every handoff that passes the object itself in `rcx`,
gives **175 proved member bodies** — and two spans the store carried as unobserved are not.

| span | was | now |
|---|---|---|
| `+0xAE4` | 332 B, `unobservedSpan0AE4` | **18 declared offsets, 128 B**; 204 B still gap |
| `+0xCDC` | 52 B, `unobservedSpan0CDC` | **6 declared offsets, 32 B**; 20 B still gap |

**160 bytes move from UNKNOWN to TYPE RESOLVED**, and this type goes from 569 unknown bytes
(16.1 %) to 409 (11.5 %). Store-wide: 64,593 → 64,433. **The UNKNOWN row count goes UP, 363 → 370**,
because two gap spans became nine smaller ones — the row count rising while the byte count falls
is the correct shape here, and counting rows alone would read it as a regression.

### Why these are fields and not an unrolled copy

That question has to be asked every time now: a block copy reports a perfectly regular stride and
has twice been read into this corpus as a lattice of fields that does not exist. Four things say
these are not that.

- **Every offset carries exactly one width.** No offset shows a 4-byte and an 8-byte access, which
  is the signature a coarse store over sub-fields produces.
- **Many are touched by several different functions** — `+0xB50` by seven, `+0xB08` by five,
  `+0xB58` by four. An unrolled copy lives in one body.
- **Five are indexed**, `[reg + reg*8 + disp]` at `+0xB08`, `+0xB48`, `+0xB50`, `+0xB90` and
  `+0xBE0`. Those are array bases; each is declared as **element 0 with its extent explicitly not
  established**, because the access fixes the stride and says nothing about the count.
- **The two coherent groups run in opposite directions.** `+0xAE4`–`+0xAF0` are four `i32` *loaded*
  into `edx`/`r8d`/`r9d`/`eax` at `00188ACD`–`00188AE1`; `+0xD00`–`+0xD0C` are four `f32` *stored*
  from `xmm9`/`xmm8`/`xmm7`/`xmm6` at `00185D01`–`00185D1B`. A copy loop is one direction.

Every width is taken from its own access instruction, never from the next offset, and **no meaning
is claimed for any of the 24 rows** — none carries arithmetic or a comparison that would narrow it.
The remaining 224 bytes stay declared gaps rather than being absorbed to make the layout look
finished.

**What this says about the instrument, not just the type.** The gap was never in the corpus; it was
in the seeding. A singleton reached through a one-instruction accessor is invisible to a scan that
looks for slot loads, and *four* bodies load this slot against *117* that call the accessor. The
same shape has now cost three findings — `CharacterRenderObject`'s constructor was not a vtable
slot, `BattleUnit` had a third accessor nobody had seeded, and this. **Enumerate every way the
object can be obtained before believing any census of it.**
## SWE2-EC7-31 update (2026-09-18) — `0024B4F0` dual-bank teardown (via `0022A770`/`0022B8C0`/`0022BC20`)

`0024B4F0` (137 B) — reached through `0022A770`, `0022B8C0` and
`0022BC20` — is the paired array release the shutdown paths share:
every live element of the `02091150` pointer bank
(`edi < word[02092168]`) goes through `003697F0`, every element of
the `02091950` bank (`edi < word[0209216A]`) through `00182CA0`,
both counts reset to 0, and a tail `jmp 0024B580` finishes — the
two banks emptied with different per-element releasers. Interior
anchor `0024B548` (the `call 00182CA0` second sweep).
## SWE2-EC7-32 update (2026-09-18) — `001B9020` list-container ctor + `001B2490` `+0x3A60` setter + `0019A000`/`00199F10` locked pool ops (via `0017CF30`/`001A9ED0`)

`001B9020` (201 B) is the list-container constructor the init
census counts: the `+8` triple zeroes, `001EDF00(+0x30, src+0x30)`
copies the string member, `+8` self-links, then — when `src+0x18`
is live — `001B9B80` deep-clones the source list into `rbx+0x18`
and the head/tail pointers are fixed to the clone's extremes;
`+0x28` copies through. Interior anchor `001B9083` (the `call
001B9B80` deep copy).

`001B2490` (20 B) is the table setter the init rows reach:
`dword[rcx+0x3A60] = 008F80F8[edx]` — a `movsxd`-indexed dword
from the `008F80F8` table straight into the context's `+0x3A60`
slot. Interior anchor `001B249D` (the `+0x3A60` store).

`0019A000` (145 B) and `00199F10` (79 B) — reached through
`0017CF30`, `001A9ED0` and `001B82F0` — are the locked pool
siblings: `0019A000` takes `005CD4F0(&obj+0x28)`, allocates 0x18
through `[obj+0x60]`'s `+0x10` vfunc, splices the node after the
`[obj+0x50]` head (four pointer writes), and releases via
`005CD820`; `00199F10` is the same lock shape around
`001BA860(&obj+0x90)` — lock, pool-alloc, unlock, return node.
Interior anchors `0019A04E` (the `[rax+0x10]` vfunc alloc) and
`00199F40` (the `001BA860` locked alloc).

## SWE2-EC7-33 update (2026-09-19) - `001B72B0`

`001B72B0` (981 B) is the Phyre render-block-binding init the census row names - the `YChannel`/`UChannel`/`VChannel` triad strings, 4 `00671B10` calls plus `00628100`/`00625F00`/`00610990`/`0060DD70`/`005CDAA0`/`001B81B0`/`0018D240` three each (three sibling sub-objects). Interior anchor `001B73E2` (a `00671B10` call).

## SWE2-EC7-34 update (2026-09-19) - `0019FC30`

`0019FC30` (926 B) is a 0x80-stride record-range pass - the `[rcx+8]`..`[rcx+0x10]` span walked in 0x80 steps with the `0x6666666666666667` divide-by-ten index magic, 4 `0019F300` calls plus `0019F250`/`0019FFB6`/`0019F3E0`/`0019F0D0`. Interior anchor `0019FD5D` (an `0019F300` call).

## SWE2-EC7-34 update (2026-09-19) - `001B4140`

`001B4140` (856 B) is an EH-framed string-record builder - `0xfffffffffffffffe` frame state, `001EDF00` copies plus the `001B33A0`/`001B3480`/`001A5760`/`001B4480`/`001B439C`/`001B431E` family. Interior anchor `001B41C1` (an `001EDF00` copy).

## SWE2-EC7-35 update (2026-09-19) - `001ADD30`

`001ADD30` (728 B) is an EASTL string builder - `008F4120`/`008F6600` allocators, the `02EBA2E0`/`02EBA2E1` empty-string sentinel, twelve `001EDF00` copies plus `001FB360`/`001ADBA0`. Interior anchor `001ADD61` (an `001EDF00` call).

## SWE2-EC7-35 update (2026-09-19) - `001BC9D0`

`001BC9D0` (693 B) is a string/record builder - `008C5F58`/`008F4120`/`008F6600`, a two-arm branch through `0018D0F0`/`001BCC90`, `0061D9C0`/`001EDF00`/`00808FE4`/`0060B720`/`001DE540`/`0018B320`. Interior anchor `001BCA09` (a `0061D9C0` call).

## SWE2-EC7-35 update (2026-09-19) - `001B3E80`

`001B3E80` (689 B) is the call-free CRT deque insert - `[rcx+8]`..`[rcx+0x10]` range in 32-byte elements (`sar 5` count), `movups` pair copies shifting the tail. Interior anchor `001B3EB9` (the `movups` element load).

## SWE2-EC7-36 update (2026-09-19) - `001AF000`

`001AF000` (678 B) is an application record body - `001ADAB0`/`0021A920`/`001FB460`/`001AE4B0`/`001ADB30` plus more `001Axxxx` calls. Interior anchor `001AF05F` (an `001ADAB0` call).

## SWE2-EC7-36 update (2026-09-19) - `001B07A0`

`001B07A0` (627 B) is an application string body - `008C2A40`/`008C2F78`/`008C3018`/`008F3F58` rdata run, `00861EC0`/`001EDF00` pairs plus `00809728`/`00808C40`/`001AB6B0`. Interior anchor `001B07F2` (an `00861EC0` call).

## SWE2-EC7-36 update (2026-09-19) - `001AA9E0`

`001AA9E0` (619 B) is an EASTL string builder - `008F4120`/`008F6CD8`/`008F6CE0`, `001EDF00`/`0019C5D0` quintuple plus `001AD510`. Interior anchor `001AAA0C` (an `001EDF00` call).

## SWE2-EC7-36 update (2026-09-19) - `001A9050`

`001A9050` (612 B) is an application config body - `008C2F70`/`008F6560`/`01F44830`, `00674A00`/`00210EC0`/`00210EB0`/`001D6FA0`/`00808C40`. Interior anchor `001A9079` (an `00808C40` call).

## SWE2-EC7-37 update (2026-09-19) - `00189570`

`00189570` (577 B) is an application record body - `008C5F74`, `00185C30` quintuple plus `0018A620` quadruple and `001AD440`/`001ACC30`/`0018A680`. Interior anchor `001895B0` (an `001AD440` call).

## SWE2-EC7-37 update (2026-09-19) - `001EB190`

`001EB190` (572 B) is an application init body - `008C5D68`/`01DFE090`/`01DFE094`/`01DFE098`, `00184E60`/`00189C20`/`005CC8A0`/`00861EC0`/`005CD0A0`. Interior anchor `001EB1B9` (an `00184E60` call).

## SWE2-EC7-38 update (2026-09-19) - `001B8400`

`001B8400` (499 B) is an application record body - `01FD4A68`, `0067ABF0`/`0067A2F0` pairs plus `0017D980`/`0067AB40`/`0067A990`/`0067A9B0`. Interior anchor `001B8411` (a `0017D980` call).

## SWE2-EC7-38 update (2026-09-19) - `001EEC80`

`001EEC80` (499 B) is the ten-helper fan-out the page names - `01F82E60`/`01F82E58`/`01F44830`, `"D3D11"`/`"./GameData/%s/ArtData/shaders/"` strings, `008F6574`, `0017D2E0`/`0019CE20`/`0019CB20`/`0063DA50`/`0063B010`/`00584740`. Interior anchor `001EECC1` (a `0017D2E0` call).

## SWE2-EC7-38 update (2026-09-19) - `0063DA50`

`0063DA50` (479 B) is an application record body - `02D3E780` triple, a single `00677CE0` call. Interior anchor `0063DB36` (the `00677CE0` call).

## SWE2-EC7-38 update (2026-09-19) - `001A1500`

`001A1500` (467 B) is an EASTL container builder - `008F3CB0`/`008C5F58`, `"EASTL vector"`/`"EASTL set"` strings, `001EDF00` quintuple plus `005CC8A0`/`001E7D30`/`00199DB0`/`005CD0A0`. Interior anchor `001A1548` (an `001EDF00` call).

## SWE2-EC7-39 update (2026-09-19) - `001B3940`

`001B3940` (424 B) is the `0x2380` singleton constructor the page names - `001EDF00` octuple plus the `001B3540`/`001B36D0` twins, `"EASTL map"`/`"EASTL vector"` strings. Interior anchor `001B397C` (an `001EDF00` call).

## SWE2-EC7-40 update (2026-09-19) - `0017D4C0`

`0017D4C0` (387 B) is the init burst proper the page names - five `01F7F4C0`-block globals stored, `00210EC0` quintuple plus `001DB500`/`00199790`/`001A14E0`/`001A16E0`/`001A17D0`. Interior anchor `0017D4D4` (a `001DB500` call).

## SWE2-EC7-40 update (2026-09-19) - `0019F490`

`0019F490` (390 B) is a sead container/string apply sibling - `"EASTL set"`/`"EASTL vector"`, `001EDF00` quintuple plus `005CC8A0`/`001A1130`/`00199DB0`/`005CD0A0`. Interior anchor `0019F4D7` (an `001EDF00` call).

## SWE2-EC7-40 update (2026-09-19) - `00184CE0`

`00184CE0` (377 B) is an application body - `00184E60`/`00189C20`/`0062DD10` pairs. Interior anchor `00184D09` (an `00184E60` call).

## SWE2-EC7-41 update (2026-09-19) - `00793250`

`00793250` (353 B) is the Phyre framework teardown/reinstall the page names - `01CB2508` vtable store, `00584730` triple/`005CD6D0`/`00633800`/`00793790`/`0016D6A0`/`00809054`. Interior anchor `00793282` (a `005CD6D0` call).

## SWE2-EC7-41 update (2026-09-19) - `001A3930`

`001A3930` (342 B) is an application body - `0016D720`/`0016D840` pair. Interior anchor `001A39A3` (an `0016D720` call).

## SWE2-EC7-41 update (2026-09-19) - `001A3A90`

`001A3A90` (330 B) is an application body - `0016D6D0`/`0016D840` pair/`001A44F0`/`001A3930`. Interior anchor `001A3AC5` (an `0016D6D0` call).

## SWE2-EC7-41 update (2026-09-19) - `001AD960`

`001AD960` (330 B) is an application body - `001AF2B0`/`001AE6B0` pair. Interior anchor `001AD9D7` (an `001AF2B0` call).

## SWE2-EC7-42 update (2026-09-19) - `0066F970`

`0066F970` (318 B) is one of the Phyre render-block-binding init group the page names - `00D690E0`/`01F44830`, `005CDAA0`/`005FD050`/`00808C40`. Interior anchor `0066F99A` (a `005CDAA0` call).

## SWE2-EC7-43 update (2026-09-19) - `001B1630`

`001B1630` (281 B) is a manager/object ctor family body - `01F44830`/`01F7F5A0`/`02CBB900`/`02CF7480`, `0016D680`/`0016D6A0`/`0017EBD0`/`001B1750`/`0060DD70`/`00610990`/`0062C360`/`0063A990`/`00808C40`/`00861EC0`. Interior anchor `001B165F` (an `0016D680` call).

## SWE2-EC7-43 update (2026-09-19) - `001B5DE0`

`001B5DE0` (292 B) is a game-application body - `"EASTL basic_string"` literal, `008F6600`/`02EBA2E0`/`02EBA2E1`, `001B4140`/`001B4860`/`001EDF00`. Interior anchor `001B5E4F` (an `001B4140` call).

## SWE2-EC7-44 update (2026-09-19) - `001AE6B0`

`001AE6B0` (271 B) is a vtable row body - two `call [rax+0x10]` vcalls, no direct calls. Interior anchor `001AE6DE` (the first vcall).

## SWE2-EC7-44 update (2026-09-19) - `001B1800`

`001B1800` (268 B) is a manager-family body - `001A0A90`/`001A0BB0`/`001A1220`/`001A1E40` plus `call [rax+0x18]` vcalls. Interior anchor `001B1857` (an `001A0A90` call).

## SWE2-EC7-44 update (2026-09-19) - `001A1310`

`001A1310` (257 B) is a body - `005CD4F0`/`005CD820`/`00808C40`/`00808F10`/`00861EBA` plus a `call rax` vcall. Interior anchor `001A1340` (a `005CD4F0` call).

## SWE2-EC7-46 update (2026-09-19) - `001A95C0`

`001A95C0` (234 B) is a body - `call [rax+0x10]`/`call [r9+0x18]` vcalls, no direct calls. Interior anchor `001A9610` (the first vcall).

## SWE2-EC7-46 update (2026-09-19) - `00793DA0`

`00793DA0` (234 B) is a call-free sparse struct copy - dword-pair copies over the whole record skipping every fourth dword (`+0x10`/`+0x20`/`+0x30`/`+0x40` pattern). Interior anchor `00793DA4` (a copy pair).

## SWE2-EC7-46 update (2026-09-19) - `00188640`

`00188640` (225 B) is a body - `call [rax+0x10]`/`call [r9+0x18]` vcalls, no direct calls. Interior anchor `00188690` (the first vcall).

## SWE2-EC7-46 update (2026-09-19) - `0019F300`

`0019F300` (222 B) is a call-free SIMD record copier - `movups` eight 16-byte lanes per `0x80` record, two-iteration inner loop over the `[rdx, r8)` span. Interior anchor `0019F340` (the copy loop head).

## SWE2-EC7-46 update (2026-09-19) - `001A1050`

`001A1050` (222 B) is a body - `0019F060` plus a `call [r9+0x18]` vcall. Interior anchor `001A109F` (the `0019F060` call).

## SWE2-EC7-47 update (2026-09-19) - `001B33A0`

`001B33A0` (220 B) is a body - `001EDF00` single call. Interior anchor `001B3405` (the `001EDF00` call).

## SWE2-EC7-48 update (2026-09-19) - `0019F620`

`0019F620` (207 B) is a body - `0019F490`/`001A0AF0`/`001EDF00`/`005CC8A0`/`005CC900`. Interior anchor `0019F63F` (an `0019F490` call).

## SWE2-EC7-48 update (2026-09-19) - `001D9080`

`001D9080` (206 B) is a body - `001D8BB0`/`001D8C80`/`001EB110`/`001EB150`. Interior anchor `001D9099` (an `001D8BB0` call).

## SWE2-EC7-48 update (2026-09-19) - `0021A920`

`0021A920` (201 B) is a body - `001AE6B0`/`001EDF00`. Interior anchor `0021A955` (an `001AE6B0` call).

## SWE2-EC7-48 update (2026-09-19) - `0018B320`

`0018B320` (198 B) is a body - `call [rax+0x10]`/`call [r9+0x18]` vcalls + `008C2A40` import. Interior anchor `0018B36D` (the first vcall).

## SWE2-EC7-48 update (2026-09-19) - `001A94F0`

`001A94F0` (198 B) is a body - `call [rax+0x10]`/`call [r9+0x18]` vcalls + `008C2A40` import. Interior anchor `001A953D` (the first vcall).

## SWE2-EC7-49 update (2026-09-19) - `001B4860`

`001B4860` (196 B) is a body - `001B3320` plus a `call [rax+0x18]` vcall. Interior anchor `001B4896` (the `001B3320` call).

## SWE2-EC7-49 update (2026-09-19) - `0019F0D0`

`0019F0D0` (186 B) is a call-free backward `0x140`-stride record copier - `movups` x8 unroll per `0x80`, two blocks per record. Interior anchor `0019F100` (the copy loop head).

## SWE2-EC7-50 update (2026-09-19) - `0019F190`

`0019F190` (184 B) is a call-free forward `0x140`-stride record copier - `movups` x8 unroll per `0x80`, sibling of the `0019F0D0` backward walk. Interior anchor `0019F1B0` (the copy loop head).

## SWE2-EC7-50 update (2026-09-19) - `00184E60`

`00184E60` (182 B) is a call-free `0xC0`-byte defaults record init - `1.0f` at `+4`/`+0xC`/`+0x18`/`+0x2C`, `movups` rows `008C5F80`/`008C5F90`/`008C5FB0`/`008C5FD0`, `+0xB8` = `0.1f`, `+0xBC` = `10000.0f`. Interior anchor `00184E67` (the first `1.0f` store).

## SWE2-EC7-50 update (2026-09-19) - `001A0AF0`

`001A0AF0` (182 B) is a body - `0016D6A0`/`0019FFD0`/`001A1050`/`002218D0`/`005CC8C0`/`005CD0A0`/`005CD1E0`. Interior anchor `001A0AFD` (an `0016D6A0` call).

## SWE2-EC7-50 update (2026-09-19) - `0018BAB0`

`0018BAB0` (180 B) is a body - `00186980`/`00189120`/`0018B4E0`/`001AB570`/`001F18A0`/`0085E730`. Interior anchor `0018BAD8` (an `00186980` call).

## SWE2-EC7-50 update (2026-09-19) - `001B3480`

`001B3480` (180 B) is a body - `001A4BF0`/`001EDF00`. Interior anchor `001B34E5` (an `001A4BF0` call).

## SWE2-EC7-51 update (2026-09-19) - `0019F250`

`0019F250` (174 B) is a call-free `0x140`-stride record copier - third sibling of `0019F0D0`/`0019F190`, `movups` x8 per `0x80` copying `r8` to `rcx` forward. Interior anchor `0019F270` (the copy loop head).

## SWE2-EC7-52 update (2026-09-19) - `001E7D30`

`001E7D30` (607 B) is an EASTL container-builder helper - `call qword [rax+0x10]`/`call qword [r9+0x18]` vcalls, no direct calls. Interior anchor `001E7EB8` (the `[rax+0x10]` vcall).


## SWE2-EC7-52 update (2026-09-19) - `001ACC30`

`001ACC30` (700 B) is a call-free record-parameter producer - `[rcx+0xB8]==2` and even `[rcx+0xA8]` gates write 2pi/1.0f/zero defaults, then a `[rcx+0xBC]` mode dispatch with `cvtdq2ps`/`divss` dequant paths on `[rcx+0x1E0]`/`[+0x1E4]`. Interior anchor `001ACCE2` (the case-3 dequant load).

## SWE2-EC7-54 update (2026-09-19) - `00793790`

`00793790` (339 B) is a Phyre framework teardown sibling - `005DD620`/`005DDB00`/`005DE250`/`00625ED0`/`0062B890`. Interior anchor `007937B3` (a `00625ED0` call).

## SWE2-EC7-55 update (2026-09-19) - `0062B890`

`0062B890` (353 B) is a Phyre framework teardown sibling - `00584730`/`0062BCB0` plus six vcalls. Interior anchor `0062B902` (a `00584730` call).


## SWE2-EC7-55 update (2026-09-19) - `0018A680`

`0018A680` (268 B) is an indirect-only application record body - five `call [rax+8]` vtable invocations plus `008C5F78`. Interior anchor `0018A6FE` (the first `call [rax+8]` vcall).


## SWE2-EC7-55 update (2026-09-19) - `0067ABF0`

`0067ABF0` (250 B) is an application record body - `001EDE70`/`0067AB50`/`006CC4F0`/`006CC550`/`006CC580`. Interior anchor `0067AC10` (a `001EDE70` call).


## SWE2-EC7-55 update (2026-09-19) - `001B9B80`

`001B9B80` (247 B) is the list deep-clone the application page names - `001B9B80` self-recursive call plus `001B9C80` and one vcall. Interior anchor `001B9B97` (a `001B9C80` call).

## SWE2-EC7-56 update (2026-09-19) - `001D8BB0`

`001D8BB0` (192 B) is an application body - `001D8B20`/`001FBD80`/`0020E630`/`0020E670`/`0020E680`/`0020E9F0`. Interior anchor `001D8BC2` (a `0020E680` call).

## SWE2-EC7-58 update (2026-09-19) - `001B1750`

`001B1750` (165 B) is a game-application body - `001A4BF0`/`001B14E0`/`001B1800`/`001EDF00`. Interior anchor `001B1760` (a `001B14E0` call).



## The `01F82C80` singleton typed, and what this page already knew (2026-09-19, OPUS)

The ensure-singleton table above has carried `001D62D0` → `[01F82C80]` since it was written,
noting the `0xF778` allocation and the five float initialisers. The object behind it is now typed
at **99.2 %** in `_types/` as **`FrameMarkerSingleton01F82C80`**, and the five floats turn out to be
its first twenty bytes rather than its character.

| offset | | |
|---|---|---|
| `+0x0000`–`+0x0010` | five f32 presets | `0.2 / -0.8 / 0.04 / 0.8 / 0.7` |
| `+0x0014` / `+0x0015` | per-marker report mode / one-shot init flag | the allocator writes both as one word |
| `+0x0018` | `resetTimeMs18`, f32 | `movss`, narrowed from the `005CC930` timer |
| `+0x001C` / `+0x0020` | CPU marker count / GPU query count, **both capped at 128** | one qword clear covers both |
| `+0x0030` | **128 × 24** — `{f64 timestampMs; char label[16]}` | label initialised `""`, later `"END"` |
| `+0x0C30` | **128 × 24** — elapsed per marker | |
| `+0x1830` | **128 × 24** — raw query results; entry 0 is the frame origin | |
| `+0x2430` | **128 × 16** — `{s32 = -1; u64 = 0}` | ends exactly on the `+0x2C30` sentinel |
| `+0x2C38` | 512 bytes, **not touched by any of the eight tied bodies** | the only substantial gap left |
| `+0x2E38`, `+0x6078`, `+0x92B8`, `+0xC4F8` | **four** colour arrays, `0x3240` each — 134 records × 96 bytes, each record six float4s with alpha `1.0` | |
| `+0xF738` | `float[4][4]` identity | the last 64 bytes |

`001D6000` is the per-frame entry: it loads the singleton at `001D6017` and calls the recorder
`001D6040`, the reporter `001D5650` and the reset `001D6170` in turn. `001D5650` publishes the
marker count into a **five-slot rotating frame table** — the `imul 0x66666667` / `sar edx, 1`
idiom at `001D5671` and `001D58A2` is a divide by five.

### This page held the refutation of an error made against it

The type was first declared with the route `STATIC 0x01F82C80`, which says the 63 KB object *is* the
memory at that address. **The sentence closing the table above already ruled that out** —
*"the globals form a contiguous manager-pointer block `01F7F4C0`–`01F82D00`"* — and the table
itself lists `001D6990` → `[01F82CB8]`, `001D8150` → `[01F82CD0]`, `001D89D0` →
`[01F82CD8]`, `001D8CD0` → `[01F82CE0]`, `001DB1E0` → `[01F82CF8]` and `001DB500` →
`[01F82D00]`: six further singleton pointers inside the `0xF778` extent the route claimed.

> **The database already contained the answer, in the very table the new row was derived from.**
> The route is now `PTR 0x01F82C80`. Recorded as `EVIDENCE-STANDARD` addendum bx, whose subject is
> an instrument that passed both its controls and was wrong anyway because the *window* it measured
> was built from the base under test.

A disassembly settles it in twenty-two instructions without any census: `001D62F7` calls the malloc
thunk with `ecx = 0xF778`, **all eleven field writes at `001D6306`–`001D6341` go through `rax`**,
and `rax` reaches `01F82C80` only at `001D6347`.

## SWE2-EC7-59 update (2026-09-19) - `001D6040`

`001D6040` (295 B) is the reporter/reset driver the application page names - `001D6170`/`005CC930`/`005CCB80`/`00808C40` plus two vcalls, `009002C8`/`01CEBD80`. Interior anchor `001D606B` (a `001D6170` call).


## SWE2-EC7-59 update (2026-09-19) - `001D6170`

`001D6170` (220 B) is the reset body the application page names - `001D58F0`/`001D5970`/`005CC930` plus one vcall, `009002C8`/`01F81830`/`01F81838`. Interior anchor `001D6183` (a `005CC930` call).


## SWE2-EC7-59 update (2026-09-19) - `0019F3E0`

`0019F3E0` (164 B) is a call-free `0x80`-stride record copier - 2-iteration `movups` pairs. Interior anchor `0019F412` (the first `movups` store).


## SWE2-EC7-59 update (2026-09-19) - `001B14E0`

`001B14E0` (159 B) is the save/resource body the application page names - `001B07A0`/`001D6E80`/`001D6EE0`/`001D6F20`/`001D6FA0`/`00210EC0` plus `008F80D0`/`01DF1B80`. Interior anchor `001B14F9` (a `001D6F20` call).

## SWE2-EC7-60 update (2026-09-19) - `001D5970`

`001D5970` (1629 B) is the `001D6170`-chain middle body the application page names - `001D6370`/`001D64D0`/`001D6630`/`001D6790`/`00615BC0`/`00616700`/`00624670` plus two vcalls, `008F30E4`/`008FCC84`/`0090035C`/`01CEBB70`. Interior anchor `001D5A05` (a `00615BC0` call).


## SWE2-EC7-60 update (2026-09-19) - `0067AB50`

`0067AB50` (157 B) is an application record body - `005CCB80`/`0062CC10` plus `01F7F5A0`. Interior anchor `0067ABBB` (a `005CCB80` call).


## SWE2-EC7-60 update (2026-09-19) - `00798000`

`00798000` (156 B) is the pair-zeroer the application page names - `0071F970` single call plus one vcall, `01CB28BC` and the `"%d,%d"` literal. Interior anchor `00798020` (a `0071F970` call).


## SWE2-EC7-60 update (2026-09-19) - `001A44F0`

`001A44F0` (155 B) is a game-application body - `0016D840` single call plus one vcall. Interior anchor `001A4564` (a `0016D840` call).

## SWE2-EC7-61 update (2026-09-19) - `001D64D0`

`001D64D0` (348 B) is a call-free float-pair writer - `{float,float}` array at `+0x2E38`, writes slots `i` and `i+1` (`rcx + r10*16`). Interior anchor `001D6506` (the `+0x2E38` float-pair store).


## SWE2-EC7-61 update (2026-09-19) - `001D6790`

`001D6790` (348 B) is a call-free float-pair writer sibling - same shape at `+0x6078`. Interior anchor `001D67C6` (the `+0x6078` float-pair store).


## SWE2-EC7-61 update (2026-09-19) - `001D6370`

`001D6370` (338 B) is a call-free normalized-triplet writer - `0x60`-stride records at `+0x92B8`, `cvtdq2ps`+`divss` channels r/g/b by a common divisor. Interior anchor `001D63AD` (the `+0x92B8` normalized store).


## SWE2-EC7-61 update (2026-09-19) - `001AD510`

`001AD510` (153 B) is a call-free `0x2AAAAAAAAAAAAAAB` divide-by-3 vector walker - `[r10+0xE8]` index table, writes `[r10+0xC0]` into each element `+0x44`. Interior anchor `001AD537` (the `0x2AAAAAAAAAAAAAAB` `movabs`).


## SWE2-EC7-61 update (2026-09-19) - `00628100`

`00628100` (153 B) is one of the `001B72B0` Y/U/V-channel triad callees - `0061FDA0`/`00627DA0`/`0062B100`/`0062BCB0`. Interior anchor `00628118` (a `0062BCB0` call). *(OPUS, 2026-10-01; ASTRA [`texture-resize-drain-caller`](../../_experiments/evidence/texture-resize-drain-caller/README.md), ACCEPTed by SWE2-AUDIT-SPEC ([review](../../_index/candidates/auditspec-review-texture-resize-drain-caller-0930/REVIEW.md)), static: when `+0xBC` is set and `0062BCB0` fails, it returns before both calls; otherwise the `0062B100` wait on the same object runs before the `00627DA0` resize of `+0x30`. That wait reads each old element's counter until it is not positive, one element at a time; it does not prove that nothing is pending afterwards. After a successful resize a masked count of 0 selects NULL and reads it (`0062815B`), so the callers must pass a positive count. Callers, per ASTRA [`texture-resize-input-domain`](../../_experiments/evidence/texture-resize-input-domain/README.md), ACCEPTed by SWE2-AUDIT-SPEC ([review](../../_index/candidates/auditspec-review-texture-resize-input-domain-0930/REVIEW.md)) and ASTRA [`texture-resize-upstream-safe-counts`](../../_experiments/evidence/texture-resize-upstream-safe-counts/README.md), ACCEPTed by SWE2-AUDIT-SPEC ([review](../../_index/candidates/auditspec-review-texture-resize-upstream-counts-0930/REVIEW.md)): six direct call sites pass 1, 4 or `max(1, r9d)` (`0017E8E0`, `0017F3B0`), so a raw 0 is excluded; the selected upstream callers of those two pass 1, 4 or 32. For an arbitrary dynamic `r9d` the count `0x80000000` still masks to 0. Callers outside these selected paths are not covered.)*

## SWE2-EC7-62 update (2026-09-19) - `00627DA0`

`00627DA0` (175 B) is a game-application body - `00584730`/`0061D100`. Interior anchor `00627DE8` (a `0061D100` call). *(OPUS, 2026-10-01; ASTRA [`texture-copy-capacity-caller`](../../_experiments/evidence/texture-copy-capacity-caller/README.md), ACCEPTed by SWE2-AUDIT-SPEC ([review](../../_index/candidates/auditspec-review-texture-copy-capacity-caller-0930/REVIEW.md)), static: the old count is the record's dword with bit 31 cleared, and `cmp`/`cmovb` set K = min(new count, old count) right before the `0061D100` call, so K <= N holds on this path. A new count equal to the whole old dword returns 0 with no work; a NULL buffer with a non-zero count returns 0xD before any change. On success the old buffer goes to `00584730` only when it is not the new one, not the inline `+8` slot, not NULL and bit 31 was clear; then the new pointer (unless inline) and the new count are stored.)*


## SWE2-EC7-62 update (2026-09-19) - `00185C30`

`00185C30` (148 B) is an application record body - `00184AF0` single call plus four vcalls. Interior anchor `00185C89` (a `00184AF0` call).


## SWE2-EC7-62 update (2026-09-19) - `001AE4B0`

`001AE4B0` (148 B) is a game-application body - `001AE6B0`/`00220760`. Interior anchor `001AE4C5` (a `00220760` call).


## SWE2-EC7-62 update (2026-09-19) - `001B9970`

`001B9970` (148 B) is an element-copy body - `001B9B80`/`001BA910`. Interior anchor `001B9985` (a `001BA910` call).



## SWE2-EC7-63 update (2026-09-19) - `00184AF0`

`00184AF0` (448 B) is a call-free pointer-swap body - early `0x16` return when `r8 == (rdx+8 or r9)`, else `[rdx+0xB8]` -> `[rcx+0x78]`. Interior anchor `00184B28` (the `+0x78` pointer store).



## SWE2-EC7-63 update (2026-09-19) - `001C1810`

`001C1810` (142 B) is the `SaveloadManager_RequestDisableAutosaveList` row body - `0016D6A0`/`001A0A90`/`001A1220` plus `008C3038`/`01DF6E30` and one vcall. Interior anchor `001C1822` (a `001A1220` call).



## SWE2-EC7-64 update (2026-09-19) - `001D89D0`

`001D89D0` (142 B) is an ensure-singleton body - `0016D6A0`/`00210EC0` plus `00900390`/`01F82CD8`. Interior anchor `001D89E4` (a `0016D6A0` call).



## SWE2-EC7-64 update (2026-09-19) - `001D8B20`

`001D8B20` (140 B) is an application body - `0017FFD0` single call plus `01CEBC9C`. Interior anchor `001D8B29` (a `0017FFD0` call).



## SWE2-EC7-65 update (2026-09-19) - `001B9CF0`

`001B9CF0` (137 B) is a `001EDF00`-apply body - `001A4BF0`/`001EDF00`. Interior anchor `001B9D48` (a `001EDF00` call).



## SWE2-EC7-65 update (2026-09-19) - `001B1B10`

`001B1B10` (135 B) is a manager/object-ctor body - `001AF000`/`001B0640`/`001FB360`/`001FB460`. Interior anchor `001B1B46` (a `001FB360` call).



## SWE2-EC7-66 update (2026-09-19) - `001B3290`

`001B3290` (130 B) is a small helper leaf - `001A5760` single call. Interior anchor `001B32DB` (a `001A5760` call).



## SWE2-EC7-66 update (2026-09-19) - `001C0E20`

`001C0E20` (130 B) is an ensure-singleton body - `001EDF00`/`00861EC0` plus `008C5F58`/`008F9B80` ('EASTL vector'). Interior anchor `001C0E79` (a `001EDF00` call).


## SWE2-EC7-67 update - `001B0640`

`001B0640` (129 B) is a game-application body - `001AD8E0`/`001FB460`. Interior anchor `001B066D` (a `001AD8E0` call).

## SWE2-EC7-69 update (2026-09-19) - `00615CD0` embedded sub-object ctor measured

`00615CD0` (31 B) measured - the `+0xD8` sub-object ctor `001B6D90` runs on
`PCameraPerspective`: calls `005DC400(this)` for the base init, writes
`[+0x20] = 0`, and returns `this`. The `005DC400` callee is the shared
param-block ctor the render-command-list page names.
Interior anchor `00615CE1` (the `[rbx+0x20] = 0` store).

## SWE2-EC7-69 update (2026-09-19) - `005CC900` triple-qword zero ctor measured

`005CC900` (17 B) measured - the `+0x1F8`/`+0x218`/`+0x238` child ctor
`006791B0` runs three times on the camera `+0x678` sub-object: zeroes
`[+0]`/`[+8]`/`[+0x10]` and returns `rcx`. Call-free; a plain `0x18`-byte
record initializer.
Interior anchor `005CC909` (the `[rcx+0x10]` store).

## SWE2-EC7-72 update (2026-09-19) - `0063B010` + `0062DD10` list walk and ctor measured

`0063B010` (48 B) is the `+0x98`-list find-first the `00796350` sweep
pairs with `0063DA50`: walks `rbx = [rbx + 0x98]` calling
`0063B040(node)` until nonzero or NULL, returning that code.
Interior anchor `0063B023` (the `0063B040` predicate call).

`0062DD10` (87 B) is the `00D562A8`-vtable ctor (RTTI `01D13630`, slot 0
= `0016D6A0`): `006CB5F0` base-init, then `1.0f` at `+0x38`/`+0x4C`/
`+0x60`/`+0x74` and zero at `+0x40`/`+0x48`/`+0x54`/`+0x5C`/`+0x68`/
`+0x70` - the default transform/colour record.
Interior anchor `0062DD2E` (the first `1.0f` store).

## SWE2-EC7-77 update (2026-09-20) - `00220760` + `001A5810` + `001F16C0` lifecycle helpers measured

`00220760` (119 B) is the `[rcx+0x18]`-head chain drain: each link
runs `001AF2B0(rcx, [link])` then the `+0x18` vtable slot of the
`[rcx+0x30]` object with `r8d = 0x30`; the head is then reset -
`[rcx+0x10] = rcx+8`, `[rcx+8] = rcx+8` - and `+0x18`, `+0x28`,
`byte[+0x20]` zeroed.
Interior anchor `002207A0` (the `call [rax+0x18]`).

`001A5810` (119 B) is the sibling drain - identical shape with
`00220390` as the per-link call and `r8d = 0x28` element size.
Interior anchor `001A5850` (the `call [rax+0x18]`).

`001F16C0` (115 B) is the `01F82EB0` register-object construct:
`0016D6A0(1)` gates, `001A1470(01F7F4C0, 0x18)` allocates; a live
record gets vtable `00902F28` (RTTI `01CED9D8`), `+8 = arg rcx`,
`+0x10 = arg rdx`; `01F82EB8` stores it, `001FB840(01F82EB0)` runs,
and it tails `001FB830(01F82EB0)`.
Interior anchor `001F1702` (the `01F82EB8` store).

## SWE2-EC7-78 update (2026-09-20) - `0079D920` timer/delta update measured

`0079D920` (118 B) is the elapsed-time commit: when `float[+0x6C]`
is positive it is promoted to double into `+0x48`, added into the
`+0x40` accumulator, and `+0xE0` gets the float truncation. When it
is non-positive `005CC930()` supplies the clock and `xmm0 = now -
02CB60E8 - [+0x50]`; `+0x40` takes that absolute, `+0x48` takes the
delta `xmm0 - old +0x40`, and `+0xE0` the float.
Interior anchor `0079D960` (the `005CC930` clock call).

## SWE2-EC7-79 update (2026-09-20) - `0060B720` + `005CD570` measured

`0060B720` (36 B) is the `rdx`-gated forwarder: a NULL `rdx`
returns immediately; otherwise the arg is stashed and
`0060AB10(rcx + 0x1010, &stack)` runs - the `+0x1010` sub-object
call.
Interior anchor `0060B73A` (the `0060AB10` call).

`005CD570` (104 B) is the error-string helper behind the wait
family: `[rcx]` goes to `008C2198`; a zero return arms
`008C20A8` (the error fetch) then `008C2208(0x1300, 0, err, 0x400,
&buf)` formats it and `008C21F8` frees the buffer on success;
returns 9 on the taken arm, 0 on the short one.
Interior anchor `005CD5B9` (the `008C2208` format call).

## SWE2-EC7-96 update (2026-09-20) - `002FC010` measured

`002FC010` (496 B) is the list-walk publish `0024B580` and
`0024B9B0` run: `byte[+0x37B]` nonzero decrements and returns 0;
otherwise every `02BC3D40`-chain entry with `[rdi+0x10] == rbx`
gets `word[+0x36A] |= 0x20`, the `+0x374` cursor chases `+0x372`
through `002EB740` publishes, the `+0x375` arm adds `| 0x40` plus
a zero-argument `002EB740`, then the entry is unlinked from the
`+0x28`/`+0x30` chain, relinked, `[rdi] &= 0xF000003F`, `+0x10`
cleared - the retire-and-requeue the frame loop drives.
Interior anchor `002FC103` (the `002EB740` call).

## SWE2-EC7-97 update (2026-09-20) - `002EB740` measured

`002EB740` (64 B) is the two-handle resolve trampoline this
page's `002FC010` (and `003B8670`) call: `003588B0` runs on
`rcx` then `ebx`, and the two resolved records tail into
`00319F50(rdi, rax, r8 = rsi)` - the handle-to-record pair the
publish path resolves before the real call.
Interior anchor `002EB754` (the first `003588B0` call).

## SWE2-EC7-106 update (2026-09-20) - `00252990` measured

`00252990` (81 B) is the gated
teardown chain `0022B8C0` and
`0022BC20` run: `001FBD80(1)` then
`00246790()`; only when the latter
answers nonzero does the sequence
`0039BDA0`, `00365990`,
`0024A710(1)`, `00245110(0208EA28)`,
`00245110(0208EA40)` and `00252500`
fire before the `001FBE50` tail - the
quiesce pass the frame paths share
when the subsystem reports live.
Interior anchor `002529A7` (the
`0039BDA0` call).

## SWE2-EC7-108 update (2026-09-20) - `0022CB90` measured

`0022CB90` (138 B) is the
cold-start state reset `0017D6E0`
and `0022A0B0` run:
`float[01E0283C] = 1.0`, six
`word` clears across `02064E1C` /
`02064E28` / `02064E2C` and
`02088E30` / `02088E34` /
`02088E38`, `qword[01E02830]` and
`dword[01E02838]` zeroed, a
`0x4000`-byte `00861EC0` clear of
`02064E30`, then two `0017D280`
report calls on the `00908D68` /
`00908D80` strings - the
application-root initialisation
sweep.
Interior anchor `0022CBF4` (the
`00861EC0` clear).

## SWE2-EC7-109 update (2026-09-20) - `001FB360` and `001EAA90` measured

`001FB360` (122 B) is the EASTL
map constructor `001ADD30` and
`001B1B10` run: `"EASTL map"`
goes to `001EDF00` for the
allocator record at `+0x30`, the
sentinel at `+8` self-links, and
head `+0x10`, size `+0x28` and
the flag byte `+0x20` zero - the
empty ordered map every table
starts as.
Interior anchor `001FB374` (the
`"EASTL map"` `lea`).

`001EAA90` (21 B) is the
two-dword setter `001C1D40` and
`001C2980` call:
`dword[rcx + 0x120] = edx`,
`dword[rcx + 0x124] = r8d`, and
`byte[rcx + 0xE9] = 1` - the
same dirty latch `001EAD20`
arms on the float twin.
Interior anchor `001EAA96` (the
`+0x124` store).

## SWE2-EC7-110 update (2026-09-20) - `001DE540` measured

`001DE540` (35 B) is the
mod-5 float table read
`0018A840`, `0018AC50`,
`001BC9D0` and `001BD940`
share: `dword[rcx + 0x18]`
folds through the
`0xCCCCCCCD` magic-multiply
(`mul` / `shr edx, 2` /
`lea eax, [rdx + rdx*4]` /
`sub`) into `index = value mod
5`, then `movss` returns
`float[00900ED0 + index * 4]`
- a five-entry lookup the
application state word selects
through.
Interior anchor `001DE55C`
(the indexed `movss` load).

## SWE2-EC7-111 update (2026-09-20) - `001AA7D0` measured

`001AA7D0` (100 B) is the
move-swap `001AB6B0` and
`001B07A0` run: the
destination three-pointer head
`{ptr, size, cap}` zeroes,
`001EDF00(dst + 0x18,
src + 0x18)` binds the
allocator, then all three head
words exchange with the
source's - the standard
move-construct that leaves
`src` holding the old empty
head.
Interior anchor `001AA803`
(the first swap store back
into `src`).

`001A07B0` (312 B) is the
kind-dispatching record submit
`001A0BB0`, `001A0C50` and
`001A1240` run: `0017D940(0)`
opens the frame, `dword[rdi]`
switches kinds 1..4 - kind 1
runs `0019CE20()` +
`0019CB20(result, rdi + 0x20)`
and latches `qword[+0x120]`
plus `byte[[+0x128]] = 1`,
kind 2 `001A0CF0`, kind 3
`001A0E50`, kind 4
`001A0F80`. `byte[rdi +
0x18]` then selects a direct
`call qword[rdi + 8]` or the
locked path:
`005CD4F0(rsi + 0x70)` /
`005CD820` around a
0x18-byte record append at
`[+0x98]` (`0019FA50` when the
vector is full), then
`002124C0(rsi + 0xB8, rdi)`
under the `rsi + 0x178` lock,
and `0017D960(0)` closes.
Interior anchor `001A07D8`
(the `sub edx, 1` dispatch
ladder).

## SWE2-EC7-113 update (2026-09-21) - `00863800` measured

`00863800` (65 B) is the
guarded interface call
`0035E9B0` and seven peers
(`0035E6F0`, `0035E700`,
`00368AD0`, `00369050`,
`003690F0`, `00369100`,
`003691B0`) run:
`0016D6A0(rbx != 0)` runs
first; a null `rbx` then
returns 0, else
`rcx = [[rbx]]` resolves the
object head and the IAT
import `008C20D8`
(`01CCC128`) runs with
`edx = 1`, `r8 = 0` -
returning 1. The
`0016D6A0` argument mirrors
the guard: the call gates on
the object being live.
Interior anchor `00863830`
(the IAT call).

## SWE2-EC7-115 update (2026-09-21) - `007936A0` measured

`007936A0` (103 B) is the
two-field teardown
`00793250` and `008A55B0`
run: when `dword[+0x10]`'s
bit 31 is clear,
`005F0330(qword[+0x18])`
frees the first field and
`+0x18`/`+0x10` zero; the
same ownership-bit test on
`dword[+0x00]` gates
`00584730(qword[+0x08])`
before `+0x08`/`+0x00`
zero - the two-allocator
record release the app
object's destroy path
shares with `007A0540`'s
convention.
Interior anchor `007936F0`
(the `00584730` free call).

## SWE2-EC7-116 update (2026-09-21) - `006CCA70` / `006CC580` / `006CC4F0` / `006CB5F0` measured

`006CCA70` (81 B) is the
guarded destroy `0067A9B0`
runs: when `qword[+0x10]`
is live and `0059BD80` on
it answers nonzero, the
record gets `0016D6A0`
(vtable-0 destruct) then
`00809950(ptr, 0x30)`
frees it and `+0x10`
clears.
Interior anchor `006CCA9C`
(the `0016D6A0` call).

`006CC580` (20 B) is the
length getter `0067A010`,
`0067A410` and `0067ABF0`
call: `dword[+0x54] -
dword[+0x50]` when
`byte[+0x20]` is set, else
0.
Interior anchor `006CC588`
(the `+0x54` read).

`006CC4F0` (94 B) is the
cursor query `00679600`
and `0067ABF0` run: after
the `006CC7C0` capacity
check on `r9d = [[+8] +
[+0x10]]`, it returns
`[+8] + dword[+0x1C]` - the
live cursor - or 0.
Interior anchor `006CC523`
(the `006CC7C0` call).

`006CB5F0` (132 B) is the
0x88-block constructor
`0062DD10` runs: stamps
vtable `00D86B80` ([0] =
`0016D6A0`, RTTI
`01D381A8`) and writes
`1.0f` into the twelve
diagonal fields `+0xC`,
`+0x14`, `+0x20`, `+0x34`,
`+0x38`, `+0x4C`, `+0x60`,
`+0x74` with the rest
zeroed - an identity
transform default.
Interior anchor `006CB5F8`
(the vtable load).

## SWE2-EC7-119 update (2026-09-21) - the `+0x4D0` lock pair and teardown measured

`0067A970` (20 B) is the
two-way forwarder
`001B82A0` and `001B82F0`
call: `dl` nonzero tails
`005CD500` on `rcx + 0x4D0`,
zero tails `005CD5E0` -
the enter/leave pair for
that lock.
Interior anchor `0067A977`
(the `dl` test).

`0067A440` (64 B) is the
mode-keyed version
`001B82A0`/`001B8400` call:
`dword[+0x268]` of 1 calls
`005CD500(+0x4D0)`, 2 calls
`005CD5E0`, either way
returns 1.
Interior anchor `0067A456`
(the mode-1 call).

`0067A410` (41 B) is the
readiness gate `001B8400`
runs: passes when
`byte[+0x2E8]` is set or
`006CC580(rcx + 0xA8)`
returns nonzero.
Interior anchor `0067A424`
(the `006CC580` call).

`0067A990` (30 B) queries
the `+0x490` object's
`vtable[+0x18]` with a
zeroed `xmm2` and returns
`setns` on the result -
a nonnegative-status probe
`001B8400` uses.
Interior anchor `0067A9A1`
(the `+0x18` call).

`0067A2F0` (72 B) is the
wrapped counter `001B8400`
reads: `(dword[+0x278] + 1)
* f64[+0x280]` reduced mod
`0x43E0000000000000`
(2^61) via subtract-range
correction, returned as
int64.
Interior anchor `0067A308`
(the `mulsd`).

`00679F40` (206 B) is the
teardown `0067A9B0` runs:
`00882020`, `008818E0`,
`00880B50`, `00880840`
drain `+0x3E8`, `+0x368`,
`+0x348`, `+0x320`, then
`00584730` frees `+0x4E8`;
when `byte[+0x4E5]` is
clear the `+0x490` object
gets `vtable[+0x10]` then
`vtable[+0x30]` and
`+0x498`/`+0x4A0`/`+0x4A8`
free, otherwise only
`vtable[+0x10]` runs and
`+0x4E4` latches 1.
Interior anchor `00679F84`
(the first `00584730`).

## SWE2-EC7-120 update (2026-09-21) - `005CD500` measured

`005CD500` (98 B) is the
kernel-object create half of
the `+0x4D0` pair
`0067A970`/`0067A440` drive:
IAT `008C21A0` tests
`[rcx]`'s handle first (a
nonzero return short-outs
with 0), then `008C20A8`
supplies the current-thread
id and `008C2208` creates
the object (`0x1300`/
`0x400` bounds, no name);
on failure `008C21F8`
closes `[rsp+0x50]` and the
return is 9.
Interior anchor `005CD539`
(the `008C2208` create
call).

## SWE2-EC7-121 update (2026-09-21) - `00633800`, `0062B250`, `0062AAB0` measured

`00633800` (122 B) is the
`+0x88`-chain release
`00793250` calls: from
`[rcx]` each node - the
object living `0x88` before
the link - gets its `+0x78`
cleared, then `[+0x18]` is
freed via `00584730` when
`[+0x10]`'s bit 31 is
clear, and the head's
`+0x10`/`+0x18` zero.
Interior anchor `00633862`
(the `00584730` call).

`0062B250` (57 B) is the
ready predicate `0079C140`
calls: when `[+0x1890] ==
1` it calls `[+0x118]`'s
`vtable[+0x58]` with two
stack outs and returns 0
only when the first out
comes back zero; any other
state returns 1.
Interior anchor `0062B271`
(the `vtable[+0x58]`
call).

`0062AAB0` (71 B) is the
mode setter `0079C140`
uses: `edx` 0/1/2 writes
`u16[+0x1848] = 0`/`1`/
`0x101` and modes 0 and 1
also store `r8d` at
`+0x184C` and return 0;
other `edx` returns
without a store.
Interior anchor `0062AAC0`
(the `0x101` store).

## SWE2-EC7-122 update (2026-09-21) - the `0079C140` display-mode family measured

`00629690` (723 B) is the
mode pick-and-apply
`0079C140` drives:
`[+0x1880]`'s
`vtable[+0x38]` enumerates
display modes and
`vtable[+0x40]` (`edx =
0x1C`) fetches the record
list; the `00808F10`
chkstk'd alloca holds
`count * 0x1C` records;
`005CDAA0` logs through
`00D55538`/`00D55570`/
`00D55598`/`00D555C0` (the
`"[Screen ..."` lines). The
scan matches width, height
and refresh (`r13d`, the
stack arg, `r14d` divided
from the record's `+8`/`+0xC`
pair); `008C29A8` runs with
`edx = -1`; `[+0x118]`'s
`vtable[+0x58]` query
writes `+0x1890`, and the
`vtable[+0x70]` /
`vtable[+0x50]` pair
applies the chosen record.
`+0x1890 = r12d` on
success - the field
`0062B250`'s predicate
reads.
Interior anchor `006298A5`
(the `vtable[+0x70]`
apply).

`00625F30` (215 B) is the
paired mode-changed
predicate: gated on
`+0x1898`/`+0x18A0` it
re-runs the `[+0x1880]`
enum and returns
`!(handle == +0x1898 &&
count == +0x18A0)`.
Interior anchor `00625FD6`
(the count compare).

`00625ED0` (20 B) is the
`+0x28 || +0x18` non-empty
predicate `00793790` (and
the `0062B890` drain sites)
test - the same list-pair
emptiness shape `006278B0`
uses on `+0x480`/`+0x4D0`.
Interior anchor `00625ED7`
(the `+0x18` compare).

`00626010` (76 B) is the
indexed device fetch the
save-image marshal
`00621C00` calls:
`[rdx+0x110]`'s
`vtable[+0x70]` receives
`r10[[r10+8] * 8]` (an
index-selected entry) and
writes a pointer out;
returns it, or 0 on failure
or null.
Interior anchor `00626044`
(the `vtable[+0x70]`
call).

## SWE2-EC7-123 update (2026-09-21) - `0061D3D0` and `0061D100` measured

`0061D3D0` (178 B) is the
viewport call `006278B0`,
`0061D490`, `0062AA80` and
`00625830` run on the
`+0x110` device: a 0x20-byte
viewport record on the stack
- `edx` as float, `+0x1870 -
r8d - arg` as float, `r9d`
and the stack arg as floats,
then `0`/`1.0f` - feeds
`vtable[+0x160]` with `edx
= 1`. This is the
screen-rect/viewport set the
recreate and the initial
device path both run.
Interior anchor `0061D46A`
(the `vtable[+0x160]`
call).

`0061D100` (121 B) is the
0x58-record buffer init
`00627DA0` calls: `edx == 0`
returns 0; `edx > 1`
allocates `edx * 0x58` with
`0017D260`, else the caller's
`+8` inline slot is the
buffer. `00613770` copies
`r9d` records from `r8`,
then `0061C250` zero-fills
the `(edx - r9d)` tail.
Returns the buffer.
Interior anchor `0061D14C`
(the `00613770` copy). *(OPUS, 2026-10-01; ASTRA [`texture-copy-construction`](../../_experiments/evidence/texture-copy-construction/README.md), ACCEPTed by SWE2-AUDIT-SPEC ([review](../../_index/candidates/auditspec-review-texture-copy-construction-0930/REVIEW.md)), static: `edx` is the new count N, `r9d` the copy count K, `r8` the source; N = 1 uses the helper record at `rcx+8`. The helper does not clamp: K <= N is its caller's precondition, and K > N would copy past an N-record buffer. The copied head keeps each record's `+0x38` counter and its `+0x48` / `+0x50` async data; the tail records get `+0..+0x30` and `+0x38` zeroed and the `00D54348` vtable at `+0x40`, while their `+0x48` / `+0x50` keep whatever the allocation held.)*

## SWE2-EC7-124 update (2026-09-21) - the `0061D100` record helpers and `0060DA50` measured

`0061C250` (93 B) is the
default-record fill
`0061D100` runs on the
tail: each 0x58 record gets
~~seven zeroed qwords, `+0x28`
zeroed, and the `00D54348`
vtable (RTTI `01D12448`)
installed at `+0x30`.~~
*(Corrected 2026-10-01, OPUS: seven zeroed qwords at `+0..+0x30`, a zeroed dword at `+0x38`, and the `00D54348` vtable (RTTI `01D12448`) at `+0x40`. The loop stores through `rax = rcx + 0x10` (`0061C25F`), so the old offsets were read 0x10 short. Found by ASTRA [`texture-copy-construction`](../../_experiments/evidence/texture-copy-construction/README.md), ACCEPTed by SWE2-AUDIT-SPEC ([review](../../_index/candidates/auditspec-review-texture-copy-construction-0930/REVIEW.md)); regression `tex_check.py` T1 in [`opus-texture-incorp-1001`](../../_index/candidates/opus-texture-incorp-1001/consumer-check.md).)*
Interior anchor `0061C297`
(the vtable store).

`00613770` (133 B) is the
record copy `0061D100` runs
on the head: `r8` records of
0x58 bytes - eight qword
copies plus `+0x38` dword,
the `00D54348` vtable at
`+0x40`, `+0x48` and `+0x50`
- from `rdx` to `rcx`.
Interior anchor `006137D9`
(the vtable store).

`0060DA50` (184 B) is the
kind-0x21 command writer
`00187950` calls: `00600B30`
claims the lock (else
`vtable[+0x10]` releases
`rcx`), a 0x80 record is
bump-taken from the
`+0x50`/`+0x58`/`+0x60`
region (first slot seeded
into `+0x88`, end at `+0x90`),
then `{kind=0x21, +8=dl,
+0xC=r8d}`; a full region
returns 0xD.
Interior anchor `0060DAD6`
(the kind store).

## SWE2-EC7-125 update (2026-09-21) - the range-checked pointer push measured

`0060AB10` (144 B) is the
insert helper `0060B720`
calls: it bounds-checks the
incoming pointer against the
container's `+8`/`+0x10`
range, derives the element
index as
`(ptr - base) >> 3`, and
when the vector is full
grows it through `005FE9C0`
before storing the pointer
and advancing the `+0x28`
cursor by 8. Two grow sites
(`0060AB46`, `0060AB7C`)
cover the empty and
at-capacity cases. Interior anchor `0060AB46` (the
`005FE9C0` grow call).

## SWE2-EC7-126 update (2026-09-21) - the vector grow and the pair release measured

`005FE9C0` (130 B) is the
`vector<T*>` grow `0060AB10`
falls into: when the free
run `([+0x10]-[+0x8])>>3`
can't take `rdx` more it
length-checks against
`0x1fffffffffffffff`
(`"vector<T> too long"`,
`008F6820`, thrown via
`008C2618`), picks
`max(need, cap + cap/2)`,
and tails into `005FE930`
for the realloc-and-move.
Interior anchor `005FEA04`
(the throw call).

`005DDB00` (111 B) is the
paired-buffer release
`005D2F80` and five
siblings run: for each of
the `{count|flag, ptr}`
pairs at `+0x40`/`+0x48` and
`+0x30`/`+0x38`, a bit-31
owner flag frees the pointer
through `00584730`; both
pairs are zeroed, then it
tails into `006108C0` for
the rest of the teardown.
Interior anchor `005DDB2C`
(the first `00584730` free).

## SWE2-EC7-127 update (2026-09-21) - node unlink and vector realloc measured

`006108C0` (200 B) is the
tagged intrusive-node unlink
`005DDB00` tail-jumps to (and
five other teardown paths
call): the `+8` byte selects
the node kind (0/1/2), the
candidate `[rcx]` is taken
only when its `+0x20`
back-link points back at the
list head (fail-closed
otherwise), the `0x100` busy
bit is cleared on the node,
and the successor - the
matching-kind node found via
`[r8]` or the sentinel - is
spliced through
`[rdx+0x20]`/`[rcx]`.
Interior anchor `006108FE` (the `0x100`-bit clear).

`005FE930` (142 B) is the
vector-reallocate core
`005FE9C0` delegates to after
its growth check: `005FEC70`
computes the new size, the
`008C2A40` import allocates
the new run, `end - begin`
bytes are moved across, the
old range is destroyed and
freed via `001A5A80` when
present, and the
`{begin, end, cap}` triple is
rewritten (`sar 3` element
counts, stride 8).
Interior anchor `005FE970` (the allocator call).

`0059FBA0` (60 B) is the union-source position dispatch the `001A0CF0`/`001A0E50` kind-2/kind-3 readers drive: if `+0x10` (a loaded-object pointer) is set it tail-jumps to `00215220` on it; else if `+8` (a file handle) is not `-1` it tail-jumps through the IAT `008C2150` import (`SetFilePointerEx`-family) with `(handle, rdx, 0, r8d)`; else if `+0x20` (a size/position field) is positive it tail-jumps to `001D6CE0` with `rcx` set to that field. A source with none of the three returns `-1`.

Interior anchor `0059FBC7` (function `0059FBA0`).

`00563520` (42 B) is the handler-register `0022A4B0` runs (already row-listed on this page): `002486B0(00563550)` creates the object bound to handler `00563550`, `00292260(obj)` initializes it, and the tail `00249410(obj)` registers it.

Interior anchor `00563538` (function `00563520`).

`00556500` (90 B) is the `lic_4_c` handler-register `0022A4B0` runs beside `00563520`: `002486B0(00556560)` creates the object bound to handler `00556560`, `002922C0` initializes it, `002493D0(obj, "lic_4_c", 0x79, 3, 2)` names and binds it (`00D23178`), the result is published into `02CA8FD8`, and the tail `00249410(obj)` registers — the licence-board child's slot on the application object table.

Interior anchor `00556522` (function `00556500`).

`002486B0` (67 B) is the twelve-slot allocator `00563520` and `00556500` run on `02090790`: up to twelve `0x20`-stride records are scanned for a clear `+0` flag; a free slot is 0x20-zeroed, its `+0` occupied bit set, `+8` = 1, `rcx` parked at `+0x10`, and the slot returned — a full table returns 0. The create arm behind the application object's handler registry.

Interior anchor `002486D3` (function `002486B0`).

`001F0AD0` (2738 B) is the `+0xAFE`-gated body `00187950` runs inside the render pass list: `byte[rcx+0xAFE]` must be set and at least one of `[rcx+8]`/`[rcx+0x10]` live, then `001EEE80`/`001EE040` x2, `00610330`, `001EF6D0` and the `001F1xxx` local arms - the pass's conditional stage.

Interior anchor `001F0B98` (function `001F0AD0`).

`001EEE80` (110 B) is the record refresh `001F0AD0`/`00188B10`/`00193AD0` run inside the render pass list: null `rcx` and `byte[rcx+8]` bail out, `[rcx]`'s record compares `+0x28`/`+0x2C` against `edx`/`r8d`, a mismatch probes `00625F00` and refreshes through `0062BCB0`, then `0060DD70(rbx, edx, r8d, [rbx], 0)` re-emits.

Interior anchor `001EEEC1` (function `001EEE80`).

`001EF6D0` (3731 B) is the transform stage `001F0AD0` runs inside the render pass list: `[r8]`'s `0x30`-byte vector block copies to the frame, `[rcx+0xA4]` zeroed and `+0xA0` holds the broadcast `w`, then SSE work runs through `00185AF0` x3, `001EB4B0`, `00861F4A`, `001EF560`, `00861F14`, `00185100`, `00187460` and `0018A120` - the pass's heavy vector stage, xmm6-xmm15 framed.

Interior anchor `001EF8A6` (function `001EF6D0`).

`0022FFE0` (1967 B) is the draw body the slot-4 pump `0017D6E0` runs: a `0x1B08` `chkstk` frame, `0026E500()` fetches the object, `00861EC0` clears two `0x400` buffers, `r13d = [rdi+0xC] * [rdi+8]` counts the grid cells, `00202C70`/`00202D70` stage the `02AEDEF0`/`02AEDDB0` templates, and the `00181560`/`00181910`/`001816B0`/`00181870`/`00181890` emit battery runs with `0017D2E0` x3, `00181FD0`, `00181350`, `00181310`, `001820E0`, `00181E70` and `002324F0` - the pump's per-frame draw.

Interior anchor `00230037` (function `0022FFE0`).

`001BAA30` (1463 B) is the texture-table body `001BC190` (the pump's largest) and `001BB120` run: `02CBB900` bases the workbench, the `008F9208` `/tex_` name stem feeds `001EDF00` x2 lookups, and `001B9A10` x16 with `0018A330` x2, `00183780`, `00220390` build the records - the texture-name record emit behind the slot-4 pump.

Interior anchor `001BAAD1` (function `001BAA30`).

`001EB4B0` (755 B) is the startup/apply body `001EBDD0`, `001EF6D0` and `0067F280` call: `00861F14` x4 only across 755 bytes - a long inline copy/seed pass with a single CRT helper.

Interior anchor `001EB531` (function `001EB4B0`).

`001AC950` (722 B) is the worker the renderer update `00189CE0` calls: `movss` triplets copy `[r8+0xC]`/`[r8+0x1C]`/`[r8+0x2C]` into `[rdx]` column order - the transform publish's call-free vector packer.

Interior anchor `001AC95A` (function `001AC950`).

`0019FA50` (467 B) is the call-free vector insert `001A07B0` uses: `qword[rsi+8]` vs `[rsi+0x10]` bounds-checks, `rbx` snaps `rdx` into the 0x18-element range, a descending `movups`/`movsd` loop shifts elements down 0x18 each from the tail to `rdi`, the gap at `rbx` copies into `rdx`, and `[rsi+8] += 0x18` - the app's 24-byte-element container insert.

Interior anchor `0019FAA0` (function `0019FA50`).

`001EF560` (360 B) is the orbit helper `001EF6D0` calls: `xmm1 * 0.5` subtracted from 2π (`0x40C90FDA`), `00861F1A` evaluates the trig pair, `xmm6 * -1.0` and `+ xmm8` give the rotated components, `[rbx + 0xC]` = 1.0f - the application's camera-angle step.

Interior anchor `001EF593` (function `001EF560`).

`001A0CF0` (352 B) is the string emit `001A07B0` calls: `00597970` resolves `[rdx + 0x20]`, `[rsi + 0x110]` is the handle (0xFFFFFFFF falls back through `001FDF70`), `[rsi + 0x108]` feeds `0059FBA0`, `0059D920` gates the `00598100`/`0059BD40`/`0059F4A0`/`001A09E0` commit - the application's localized-text publish.

Interior anchor `001A0D25` (function `001A0CF0`).

`001B9D80` (337 B) is the ordered find `001BAA30` calls: same `rcx + 8`/`[rcx + 0x18]` tree shape as `00223790`, `r9d = [r8]` vs `[rax + 0x20]` with `setb` walking, `0016D720`/`0016D840` finish - the application's map lookup twin.

Interior anchor `001B9DF3` (function `001B9D80`).

`00184F20` (335 B) is the record ctor `00189000` calls: `word[rcx]`/`byte[+2]` cleared, `[+8]`/`[+0x10]` take `rdx`/`r8`, `+0x18`/`+0x1C` zeroed, `rcx + 0x20` binds `001850B0` then `00184CE0`/`00186CD0`/`0062DD10` with `00808FE4` registering the teardown - the application's callback record.

Interior anchor `00184F7D` (function `00184F20`).

`001A0E50` (298 B) is the dword-patching sibling `001A07B0` calls beside `001A0CF0`: `rdx+0x20` carries the record, `[+0x110]` is the handle (`-1` resolves through `001FDF70`), `0059FBA0`/`0059D900` gate the write and `0059F4A0` appends at `edi + [rsi+0x100]`; the committed cursor back-patches `dword[image + rbp - 4] = edi` and `0059BD40`/`00598100` close the two stack blocks - the emit that fixes a length/count field into the section it just wrote.

Interior anchor `001A0F00` (function `001A0E50`).

`001A09E0` (171 B) is the `.cm`-name slot resolver `001A0CF0`/`001A0E50`/`001D6EC0` call: the name must exceed 8 bytes and end `.cm` (`len-3..len-1` = `2E 63 6D`); `name[len-8]` must index a nonzero byte in `[rcx + char + 0x1A1]` (the per-class validity table), `name[len-7..len-4]` parse as exactly four decimal digits through the `x5/x2` lea ladder less `53328` (`'0' x 1111`) and must stay `< 0x500`; the pointer then returns from `[rcx + (class x 0x500 + index) x 8 + 0x228]` - the class-keyed resource table behind the kind-2/kind-3 records, null on any failed check.

Interior anchor `001A0A25` (function `001A09E0`).

`001A09E0` (171 B) is the `.cm`-name slot resolver `001A0CF0`/`001A0E50`/`001D6EC0` call: the name must exceed 8 bytes and end `.cm` (`len-3..len-1` = `2E 63 6D`); `name[len-8]` must index a nonzero byte in `[rcx + char + 0x1A1]` (the per-class validity table), `name[len-7..len-4]` parse as exactly four decimal digits through the `x5/x2` lea ladder less `53328` (`'0' x 1111`) and must stay `< 0x500`; the pointer then returns from `[rcx + (class x 0x500 + index) x 8 + 0x228]` - the class-keyed resource table behind the kind-2/kind-3 records, null on any failed check.

Interior anchor `001A0A25` (function `001A09E0`).

`001820E0` (268 B) is the local-to-world transform `0022FFE0` runs on a vec3 in place: the object's basis comes from `0018A620` (`+8` variant when `byte[result]` nonzero) or `00189120 + 0x690`, and `v = basisX x v.x + basisY x v.y + basisZ x v.z + T` lands back on `rbx` with `[rbx+0xC] = 1.0f` - rows `+0x78`/`+0x88`/`+0x98` supply the basis and `+0xA8` the translation.

Interior anchor `001820F9` (function `001820E0`).

`00181FD0` (260 B) is the alternate-layout sibling of `001820E0` that `0022FFE0` also runs: the same `0018A620` (`+8` variant when `byte[result]` nonzero) or `00189120 + 0x690` basis fetch, but the in-place multiply reads basis columns at `+0x08`/`+0x14`/`+0x24` and translation `+0x28`/`+0x2C`/`+0x30` - `v = B x v + T` lands back on `rbx` with `[rbx+0xC] = 1.0f` - the second local-to-world layout on the same selector.

Interior anchor `00181FF0` (function `00181FD0`).

`0018B710` (253 B) is the allocate-wrap-enqueue `00185CD0` runs: `0085E730(0x30)` supplies the object, `001F1A10` builds it from `xmm1`/`xmm2`/`xmm3` plus the two stacked bytes and float, then the intrusive append writes `rbx` into `[rdi+0x8]`'s slot when it precedes `[rdi+0x10]` (else `001AB570` grows), `0018B4E0` finalises and a tail `jmp 0018AFF0(rcx = result, rdx = rbx)` forwards - the fire-and-forget half of the pair.

Interior anchor `0018B74A` (function `0018B710`).

`001EDF00` (14 B) is the vtable-stamp constructor every `001EDF00`-apply body and ensure-singleton stub runs: `lea rax,[00902720]` installs the `eastl::allocator_memory_log` vtable, `mov [rcx],rax`, `mov rax,rcx`, `ret` - the logging-allocator object's entire constructor, invoked wherever a sead/EASTL container records its allocator.

Interior anchor `001EDF07` (function `001EDF00`).

`0063B040` (916 B) is the application teardown drain `0063B010` wraps: while `[rsi+0x80]` bit 1 is clear it walks the intrusive list rooted at `rsi+0x10` (each node found by container-of `next - 0x50`), and for every node sweeps the `rsi+0x38` sibling chain chasing the `[+0x50]` vtable link list `[+0x78]` against the static sentinel nodes `02D3E780`/`02CF8470`/`02D3E680`/`02CF8580`; matching entries with nonzero `+0x74` get their element walked by `+0x38`-indexed table `[+0xF8]` entries and the vtable `+0x38`/`+0x70` virtuals, and the pass finishes by setting bit 1 of `+0x80` so the drain never runs twice.

Interior anchor `0063B143` (function `0063B040`).

`00676BD0` (882 B) is the string-keyed id-map lookup the teardown drain `0063B040` consults: two `gs:[0x58]`-keyed once-init blocks (`008092FC`/`0080929C` on `02D3ECE0` and `02D3EC9C`) lazily build the `02D3ECB0` tree - self-linked head, allocator vtable `008F6500` at `02D3ECD8`, `00808B90`-registered `008B1B10`/`008B1C00` atexit teardowns - and the second guards the one-time `00677030` registration of `"/GameData/D3D11/ArtData/shared/idmaps.txt"` into `02D3ECA8`; the lookup builds its key with `001A5630`, walks the tree under the `02D3E880` lock pair `005CD4F0`/`005CD820` by `00861ED2` byte-compare and `001A1990` ordering, and inserts misses through `00677350`/`00674F60`.

Interior anchor `00676DB6` (function `00676BD0`).

`00674F60` (348 B) is the ordered-map find the `02D3ECB0` string-tree performs: from the `[rcx+0x18]` root it descends the `+8`-adjusted nodes comparing first the `[rbx]` length against the query's `[r14]` count, then the `[rbx+8]` bytes through a `0x23`-bounded `008C29F8` scan and an inline terminator compare, with a length-difference short-circuit and a `008C2FE0`/`008C3000` fallback when either string is absent; the walk takes the `+8`/`+0x10` child by the sign of the result until it wraps to the head, returning the found node or 0 - called once per `idmaps.txt` entry during the one-time init `00676BD0` performs.

Interior anchor `00675019` (function `00674F60`).

`00677CE0` (255 B) is the name-keyed list splice `0063DA50` runs: `00676BD0` resolves `[rcx]`/`[rcx+8]` (length minus the `+8` flag bit) to a record whose `+0x40` chain is walked to `rdi`; both miss arms raise through `005CDAA0` with the `[rcx+0x30]` tag - `00D6C448` "Failed t..." when the lookup is null, `00D6C480` "Found as..." when the chain end misses - then the record's `+0x38` offset by `-dword[rdi+0xF4]` becomes the value spliced over every `[rsi+0x10]`-rooted link

Interior anchor `00677D50` (function `00677CE0`).

`00677350` (244 B) is the UTF-8 decode `00676BD0` runs: a lead-byte class ladder (`<0xC0` ascii; `0xC0..0xDF` one continuation; `0xE0..0xEF` two; `0xF0..0xF7` three; `0xF8..0xFB` four; `0xFC+` five - the old six-byte form) masks the lead by `(1<<(6-n))-1` and folds each `&0x3F` continuation in 6-bit steps into `r8d`, returning the codepoint

Interior anchor `006773D9` (function `00677350`).

`001D5520` (211 B) is the paired label refresh `00187950` runs under the `+0xA70`/`+0xC56` bytes: for each of `+0x10B0`/`+0x10B4` that isn't -1 it zeroes a 0x100 stack buffer (`00861EC0`), formats the name with `001CD0E0` (modes 9 and 0xA), then `001EA380(&+8, idx, buf)` applies it - the two-slot text update behind the frame body

Interior anchor `001D5580` (function `001D5520`).

`001B9A10` (211 B) is the keyed-tree accessor `001BAA30` uses: it descends the BST at `[rcx+0x18]`/`+8` on `+0x20` dword keys, returns `node+0x28` on a hit, and on a miss builds a `{key, zeroed links}` node and `001BA080`-inserts it before returning `node+0x28` - the application's `try_emplace` for keyed records

Interior anchor `001B9ACA` (function `001B9A10`).

`001BA080` (391 B) is the emplace `001B9A10` falls through to when the key isn't found: it bounds-checks `[arg4]+0x20` against both neighbour keys, `0016D6D0`-visits the hole, `vtable+0x10`-allocates a `0x58` node on `[+0x30]` and copies the 0x38-byte payload (`movups` x3 + `movsd`), `0016D840` links it at the visited position, `inc +0x28` - and when the range guards fail it delegates to `001B9EE0` - the map's insert-with-value

Interior anchor `001BA0E0` (function `001BA080`).

`001A0F80` (206 B) is the range-extract `001A07B0` runs on a parse result: `00597970` opens on `[rdx+0x20]` and `0059D920` yields the `[start,end)` pair at `[rsp+0x48]/+0x4C` - on failure `*[rsi+0x100] = 0`, else `0085E730` allocs `end-start+1`, `0059F4A0` copies, NUL-terminates, and the buffer lands at `*[rsi+0x100]` with the end cursor at `*[rsi+0x108]` when present - the 'slice this token into fresh memory' step

Interior anchor `001A0FD6` (function `001A0F80`).

`001B9EE0` (412 B) is the lower_bound+emplace `001BA080` delegates to when its range guards fail: it descends `[rcx+0x18]` by comparing the key word `*r8` against `node+0x20` (right `+8`, left `+0` - the EASTL ordering), `0016D720`-decrements on the not-less path, bound-checks the position against `r15`, vtable-allocates a `0x58` node on `[+0x30]`, copies the 0x38-byte payload, `0016D840`-links it, `inc +0x28`, and returns `*[rsi] = node, [rsi+8] = 1`

Interior anchor `001B9F20` (function `001B9EE0`).

`00187860` (202 B) is a state arm of the render pass list `00187950`: gated on `[+0xDB8]`, it jump-tables on `[+0xDAC]` in 0..7, writing next-state pairs (`+0xDAC` -> 3/4/7/0 with `+0xDA8` = 6) and calling `00185FB0`/`001876E0`; the tail block is a once-guard on `01F7F5AC` that runs `001876E0` then `00185FB0` on first entry

Interior anchor `00187885` (function `00187860`).

`00186010` (202 B) is the `+0xCD8 == 1` initialisation arm of the same pass-list object: it stores state 2, calls `00188730` and `0018B4E0` (whose record gets `+0x20 = -1`), then allocates `[+0xCF0] * (0x870 or [+0xADC] when `+0xDB8` is set or `+0xC30 == 3`) * 3` bytes via `00210EC0` into `+0xCF8`, a second `00861EC0` buffer of the same size, `00600070`-fills it from `[rbx+8]`, and closes with the owner's vtable `+0x10` plus `00610330` - the double-buffer setup step

Interior anchor `00186071` (function `00186010`).

`001876E0` (372 B) is the Capture-4K screenshot arm `00187860` invokes in pass state 7: it formats `"/Capture 4K/capture_series%03d_%04d.tga"` (state 7, counter pair `01F7F5A8`/`01F7F5AC`) or `"/Capture 4K/capture%03d.tga"` otherwise, opens `wb`, writes an 18-byte TGA header (`0xF00` x-origin word, type 2, `0x870` height), then loops `0x870` rows writing `0x2D00` bytes each from the `[rsi+0xDB0]` backbuffer bottom-up (`(0x86F - i) * 0x2D00`) - a 3840x2160 RGB dump

Interior anchor `001877F0` (function `001876E0`).

`0019EF90` (196 B) is the child-record drain `001BC190` runs on teardown: for each pointer in `[rdx+0x100, +0x108)` it `0019CE20`s the record and `0019CC50`s its `+0x108` list into `rax`, clears `[rdi+2]` and `[rdi+0x110]`, and `002124C0`s the node into `rbp+0xC8`; then resets `+0x108 = +0x100` (list emptied) and tail-jumps `002124C0` on `rbp+8`

Interior anchor `0019EFD0` (function `0019EF90`).

`001BA3B0` (184 B) is the emplace core `001BA080` delegates to once the insert position is chosen: the stack flag and the `[r8+0x20]`-versus-`[r9]` key compare decide the insert side `ebp`, `[[rcx+0x30]+0x10]` allocates the `0x58` node, a `0x38`-byte payload is copied wholesale from `rsi` into `node+0x20`, `0016D840` links the node under `rbx+8` with side flag `r9d`, `[rbx+0x28]` is bumped, and the fresh node returns through `[r15]`

Interior anchor `001BA414` (function `001BA3B0`).

`00181E70` (164 B) is the named float-pair registration `0022FFE0` runs: `001E9F40` builds a `0x110`-byte scratch string object, the `rbx` float pair copies to `+0x20` and the `rdx` name is appended by the byte-copy loop, `001C2F40` resolves the registrar and `001C2980(reg, &pair, 1)` files it, `001EA180` tears the scratch down

Interior anchor `00181EE1` (function `00181E70`).

`00600070` (163 B) is the ring-buffer record push `00186010` runs: `00600B30(rcx, 0, 1)` gates out to the vtable `[rax+0x10]` fallback, otherwise the `+0x60`/`+0x50` cursors advance past `+0x58` by `0x80` with wraparound; a nonnull cursor slot writes `{dword 0x10, rdi}` at `+0x88`-claimed space and returns 0, a null slot returns `0xD`

Interior anchor `00600086` (function `00600070`).

## Interior citations for the entry-cited functions (OPUS, 2026-10-01)

*The functions this page named only at their entry. Each was read from the certified image; the sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Verified by [`gameapp_interior.py`](../../_index/candidates/opus-gameapp-interior-1001/gameapp_interior.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic. `0061D490` is not stated here (1,211 B, several paths).*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `001850B0` | 65 B | calls `0062DD70` on `+0x298` and on `+0x108`, and stores the address `008C5D50` at `+0x190` and at `+0` | `001850C4`, `001850D7`, `001850DE`, `001850E3` |
| `00185FB0` | 86 B | calls `00188730` and `0018B4E0` and sets the returned object's dword `+0x20` to -1; calls `00861EC0([this+0xDB0], 0, 0x17BB000)` and `00600070([this+8], [this+0xDB0])`; calls vtable slot `+0x10` of `[this+8]` and tail-calls `00610330([this+8])` | `00185FBE`, `00185FCB`, `00185FD9`, `00185FF5`, `00186001` |
| `0018A820` | 13 B | stores `dl` in byte `+0`; when it is 0 also clears the word at `+1` | `0018A822`, `0018A826` |
| `00194AA0` | 14 B | stores the dwords `0x49` at `+0` and `0x4A` at `+4` | `00194AA6`, `00194AAD` |
| `00194AB0` | 58 B | calls `0016D6A0(qword 01F7FFD8 is null)`; when `01F7FFD8` is null, allocates 8 bytes through `00210EC0` and stores the block there | `00194AC0`, `00194AD4`, `00194ADE` |
| `00198750` | 64 B | when the qword `01F7FFE0` is null, allocates `0x40` bytes through `00210EC0`, constructs them with `00195060` and stores the result there | `0019876C`, `0019877E`, `00198784` |
| `00199790` | 61 B | when the qword `01F810F0` is null, allocates 1 byte through `00210EC0`, zeroes it and stores it there | `001997A3`, `001997B2`, `001997B5` |
| `0019F060` | 111 B | when `edx` is non-zero, allocates `edx` * 0x18 bytes through vtable slot `+0x10` of the allocator at `+0x18`, then copies the 0x18-byte elements of [`r8`, `r9`) into the new block | `0019F081`, `0019F089`, `0019F0A9`, `0019F0B2` |
| `001A1130` | 116 B | brings the count of 0x140-byte elements between `[rcx]` and `[rcx+8]` to `edx`: grows through `0019FC30` by the difference, or passes the excess range to `001A08F0` | `001A1151`, `001A117D`, `001A118A`, `001A119F` |
| `001A11B0` | 64 B | when the qword `01F81160` is null, allocates `0x140228` bytes through `00584740`, constructs them with `0019F620` and stores the result there | `001A11CC`, `001A11DE`, `001A11E4` |
| `001A1240` | 205 B | while byte `+0x1A0` is set: when byte `+0x68` is set, sets `+0x69` and calls `005CCB80(1)`; otherwise clears `+0x69` and, between `005CD4F0(+0x28)` and `005CD820(+0x28)`, unlinks the first node of the list at `+0x50`, releases it through vtable slot `+0x18` of the allocator at `+0x60`, sets `+0x68` when the list is then empty, and passes the value it took (`+0x10` of the node at `+0x58`) to `001A07B0`; returns 0 | `001A1274`, `001A1285`, `001A12C4`, `001A12CD`, `001A12E4` |
| `001A1420` | 55 B | allocates `edx` bytes through `0017D260(edx, 0x10)`, stores the block at `+0` and `+8` and its end at `+0x10`, and returns `rcx` | `001A1436`, `001A143B`, `001A144A` |
| `001A14E0` | 28 B | calls `001A1420(rcx, 0x2000000)` and returns `rcx` | `001A14E6`, `001A14EE` |
| `001ACF10` | 110 B | stores `edx` at `+0x248`, then makes two objects through `001EE040(0x200, 0x200, ...)` with `02CF76E8` and `02CF79C0`, storing them at `+0xD0` and `+0xC8` | `001ACF1A`, `001ACF40`, `001ACF51`, `001ACF71` |
| `001AD3E0` | 87 B | calls `0016D6A0(qword 01F811C8 is null)`; when it is null, allocates `0x258` bytes through `00210EC0`, constructs them with `001AA9E0` and stores the result at `01F811C8` | `001AD3FD`, `001AD410`, `001AD422`, `001AD42A` |
| `001AD8E0` | 125 B | copies the 0x40-byte elements of [`rcx`, `rdx`) to `r8` - qword `+0` directly, the rest through `001AE4B0` - and returns the destination end | `001AD923`, `001AD92E`, `001AD94F` |
| `001ADAB0` | 127 B | sets `[rcx]` = `r9`, then builds a copy of each 0x40-byte element of [`rdx`, `r8`) at `[rcx]` (qword `+0`, the rest through `0021A920`), advancing `[rcx]` by 0x40; returns `rcx` | `001ADACB`, `001ADAF5`, `001ADB05`, `001ADB1D` |
| `001ADB30` | 108 B | builds `edx` copies of the 0x40-byte element at `r8` at `rcx` (qword `+0`, the rest through `0021A920`) | `001ADB72`, `001ADB7D`, `001ADB83` |
| `001B1580` | 32 B | calls `001B1630`, then `001AF470`, then tail-calls `001C6C00`, all on the same object | `001B1589`, `001B1591`, `001B159B` |
| `001B1BA0` | 87 B | calls `0016D6A0(qword 01F811E8 is null)`; when it is null, allocates `0x4300` bytes through `00210EC0`, constructs them with `001ADD30` and stores the result at `01F811E8` | `001B1BBD`, `001B1BD0`, `001B1BE2`, `001B1BEA` |
| `001B24D0` | 94 B | fills the 16 qwords at `rcx` with `0x0000271000002710`, then stores `rcx + 0x40` at `+0x88` and `rcx` at `+0x80`; returns `rcx` | `001B24DE`, `001B2518`, `001B251C`, `001B2526` |
| `001B3320` | 113 B | copies the 0x38-byte elements of [`rcx`, `rdx`) to `r8`: the first 0x20 bytes through `001A5760` (skipped when source and destination are the same), then qwords `+0x20`, `+0x28` and dword `+0x30`; returns the destination end | `001B3353`, `001B335B`, `001B336E`, `001B3383` |
| `001B6BC0` | 102 B | when the qword `01F81210` is null, allocates `0x20` bytes, zeroes `+0`..`+0x17`, calls `001EDF00(block + 0x18, 008C5F58)`, copies `+0` to `+8` and stores the block at `01F81210` | `001B6BF2`, `001B6C08`, `001B6C10`, `001B6C19` |
| `001B7CE0` | 49 B | returns 1 when `[rcx+0x28]` is null; otherwise looks for `[rcx+0x30]` on the chain from that record's `+0x50` through `+0x78`, and returns 1 only when it is found and the record's dword `+0x74` is non-zero | `001B7CF6`, `001B7CFB`, `001B7D05`, `001B7D0E` |
| `001B80C0` | 56 B | with the count = dword `+0` without bit 31: returns 3 when `edx` is at or above the count; otherwise stores `r8` in slot `edx` - of the array at `[rcx+8]` when the count is above 1, else of the inline slots at `rcx+8` - and returns 0 | `001B80C2`, `001B80CA`, `001B80DB`, `001B80F1` |
| `001B82A0` | 79 B | when byte `+8` is set: calls `00229AE0(0)`, sets dword `+4` = 3, calls `0067A440(+0x678)` and `0067A970(+0x678, 0)`, and tail-calls `002E1C20(1, 0x15)` | `001B82B1`, `001B82BD`, `001B82D2`, `001B82E4` |
| `001B9C80` | 110 B | allocates a 0x58-byte node through vtable slot `+0x10` of the allocator at `+0x30`, copies 0x38 bytes from `rdx + 0x20` into node `+0x20`, sets node `+0x10` = `r8`, `+0` and `+8` = 0 and byte `+0x18` from `rdx`'s byte `+0x18`; returns the node | `001B9C9F`, `001B9CAF`, `001B9CCE`, `001B9CE2` |
| `001BB120` | 107 B | returns 0 unless `rdx` and its `+8` are set; otherwise asks `0019EB00(0019EF80(), [rdx+8])`, calls `001BAA30(rcx, rdx)` when the answer is true, and returns the answer | `001BB143`, `001BB14E`, `001BB160`, `001BB165` |
| `001BDA50` | 87 B | calls `0016D6A0(qword 01F81248 is null)`; when it is null, allocates `0x108` bytes through `00210EC0`, constructs them with `001BC9D0` and stores the result at `01F81248` | `001BDA6D`, `001BDA80`, `001BDA92`, `001BDA9A` |
| `001C0D40` | 84 B | calls `0016D6A0(qword 01F81258 is null)`, then always allocates `0x1B8` bytes through `00210EC0`, constructs them with `001BE730` and stores the result at `01F81258` (0 when the allocation fails) | `001C0D59`, `001C0D63`, `001C0D75`, `001C0D7B` |
| `001C0DD0` | 70 B | when `[rcx]` is set, byte `+8` is clear and `0019EB00(0019EF80(), [rcx])` is true, calls `001BF2E0(rcx)` and sets byte `+8` to 1 | `001C0DE5`, `001C0DF6`, `001C0E02`, `001C0E07` |
| `001C1710` | 10 B | atomically swaps byte `+0x10` with 0 and tail-jumps to `001C1810` | `001C1712`, `001C1715` |
| `001C18A0` | 64 B | when the qword `01F81260` is null, allocates `0xA78` bytes through `00210EC0`, constructs them with `001C0E20` and stores the result there | `001C18BC`, `001C18CE`, `001C18D4` |
| `001D5600` | 17 B | zeroes qword `+0` and word `+8` and returns `rcx` | `001D5607`, `001D560A` |
| `001D58F0` | 122 B | for 128 entries of 0x18 bytes from `+0x30`: zeroes the entry's first qword, copies the empty string `01CEB638` into the next 15 bytes through the CRT `strncpy` (IAT slot `008C2F70`) and zeroes the entry's byte `+0x17`; then zeroes dword `+0x1C` | `001D5926`, `001D5934`, `001D593E`, `001D595A` |
| `001D6990` | 82 B | calls `0016D6A0(qword 01F82CB8 is null)`; when it is null, allocates 8 bytes through `00210EC0`, zeroes them and stores the block there | `001D69A0`, `001D69B4`, `001D69C3`, `001D69CA` |
| `001D8AB0` | 110 B | calls `001D8700`; when byte `+0x1C` is set, calls `001D8690`, adds the double argument (rounded to float) to float `+0x20` and to double `+0x10`, stores the new `+0x10` (as float) times the float at `01CEBC50` at `+0x18`, and passes that to `001D7A20(001D8210(), value)` | `001D8AC6`, `001D8ADE`, `001D8AE3`, `001D8AF6`, `001D8B0E` |
| `001D8CD0` | 86 B | when the qword `01F82CE0` is null, allocates `0x38` bytes through `00210EC0`, zeroes byte `+0`, bytes `+4`..`+0xF`, qword `+0x28` and dword `+0x30`, sets dword `+0x10` = 3 and stores the block there (0 when the allocation fails) | `001D8CE3`, `001D8CF6`, `001D8CFD`, `001D8D0B` |
| `001DB500` | 69 B | when the qword `01F82D00` is null, allocates `0x20` bytes, runs `001A1420(block, 0x800000)` and stores the block there | `001DB51C`, `001DB52B`, `001DB533`, `001DB539` |
| `001F0570` | 57 B | stores the high 16 bits of `001DE5A0(*01F82D20)` at `+0x844` and the signed low 16 bits of a second such call at `+0x848` | `001F0580`, `001F0585`, `001F0588`, `001F059A` |
| `0020B840` | 347 B | releases entries of the list at `+0x30` (sentinel `+0x28`) until `rdx` bytes are freed: an entry is skipped when its record (`+0x28`) has byte `+0x10` set or dword `+0x14` = 5, and, unless `r9b` is set, when its non-negative word `+0xE` equals word `+0xE8` of `[+0x18]` or its positive word `+0xC` equals dword `+0x80` (or `+0x84`, unless `r8b` is set); each release subtracts the record's dword `+8` from qword `+0x90`, calls `0020B0F0` and `002124C0(+0x98, ...)`, decrements `+0x48`, unlinks the entry and frees it through vtable slot `+0x18` of the allocator at `+0x50`; a pass that falls short is repeated once with `r8b` set | `0020B894`, `0020B8BA`, `0020B8EB`, `0020B914`, `0020B93F`, `0020B970` |
| `0020BFA0` | 429 B | tries `0020B130(this, size)`; when that fails, between `005CD4F0(+0x58)` and `005CD820(+0x58)` it releases entries of the `+0x30` list (the skip tests of `0020B840`) until max(3 * size, `0xBEBC200`) bytes are freed, falls back to `0020B840(this, remainder, 1, 0)` when short, retries `0020B130`, and repeats while that fails and its stop flag stays clear; returns the `0020B130` result | `0020BFD0`, `0020BFEA`, `0020BFFA`, `0020C070`, `0020C0F5`, `0020C10F` |
| `0020E9F0` | 82 B | calls `0016D6A0(1)`, allocates `0xC0` bytes through `001A1470(*01F7F4C0, 0xC0)`, stores `009068B8` at the block's `+0`, stores the block at `+8` and returns block `+0x10` (0 when the allocation fails) | `0020E9FE`, `0020EA0F`, `0020EA23`, `0020EA29`, `0020EA32` |
| `00292260` | 95 B | for the ids 10, 20 and 14 in turn: when `002F8040(id)` is 0, calls `002491B0(rcx, id)` | `0029226E`, `0029227D`, `00292296`, `002922B4` |
| `002922C0` | 45 B | when `002F8040(0x11)` is 0, tail-calls `002491B0(rcx, 0x11)` | `002922CE`, `002922E2` |
| `0035E700` | 96 B | clears dword `022CA634`, calls `00863800` on the handles `*022CA610` and `*022CA618`, calls `008635F0(1)` while dword `022CA630` is non-zero, then calls `00863590` on both handles | `0035E70B`, `0035E715`, `0035E735`, `0035E74B` |
| `00368AD0` | 8 B | sign-extends `ecx` and tail-jumps to `00863800` | `00368AD3` |
| `00369050` | 19 B | stores `rdx` at `022D7F70` and tail-jumps to `00863800` with the handle `*022D7F68` | `00369057`, `0036905E` |
| `003690F0` | 12 B | tail-jumps to `00863800` with the handle `*022D7F90` | `003690F7` |
| `00369100` | 84 B | with the index = byte `[rcx]`: calls `0016D6A0(0x7C)`, then loops forever - `00863650` on the handle at the dword table `022CFEEC`, the callback at the qword table `022CFF10` when it is set, and, when `0017D3E0()` returns 0, `00863800` on the handle at the dword table `022CFEF0` | `00369112`, `00369128`, `0036913A`, `0036914D` |
| `003691B0` | 19 B | tail-jumps to `00863800` with the handle in the dword table `022CFEEC` at index `ecx` | `003691B3`, `003691BA`, `003691BE` |
| `0050CE40` | 43 B | passes the format string at `00D22938` (`++ debug_sound_info_regist ++ syncv = %ld`) and `0035E810()`'s result to `0017D280`, then calls `0016D6A0(1)` and tail-calls `0016D6A0` | `0050CE44`, `0050CE53`, `0050CE5D`, `0050CE66` |
| `0050D780` | 133 B | resolves an id (`00267E10(r9)`, or word `[rdx]` when that is negative) to a record through `00358940(002640C0(), id)`; when the record's byte `+3` has top bits `0x60`, `002EA6A0(record)` is non-zero and `+0xC0` is set, passes the format string at `00D22A0C` (`%d `) and the signed byte `+0x14D` of `+0xC0` to `0017D280` | `0050D7A0`, `0050D7B1`, `0050D7C5`, `0050D7F0` |
| `0067A010` | 529 B | unless dword `+0x260` is 1, repeats until it is: takes an item with `006CC4F0`, feeds its bytes (`+0x10`, count `+4`) to `0016DFE0(+0x2A8)` and calls `006CC550`; for each output `0016E040(+0x2A8)` yields it takes a slot with `006CC6A0(+0xA8, [+0x52C])` (stopping when there is none), waits with `006CC920` while dword `+0x2F0` minus `006CC580()` is below 3, writes the output's three sources (`+0x30`, `+0x38`, `+0x40` with the dwords `+0x50`, `+0x54`, `+0x58`) through `00679570` and submits with `006CC710`; finally calls `006CC670(+0xA8)` and clears byte `+0x2E8` | `0067A06C`, `0067A091`, `0067A0D0`, `0067A107`, `0067A14D`, `0067A1B4`, `0067A214` |
| `0067F280` | 344 B | copies the twelve floats at `rcx` (`+0`..`+0x2C`), the floats `+0x20`..`+0x28` of `rdx` and the float at `01CEBBA8` into stack operands, calls `001EB4B0` on them, and writes 48 bytes of the result back over `rcx` `+0`..`+0x2F` | `0067F293`, `0067F2CB`, `0067F2D8`, `0067F383`, `0067F3A3`, `0067F3CA` |
| `008B1B10` | 38 B | calls `001A49C0(02D3ECA8, *02D3ECC0)` | `008B1B1D`, `008B1B24`, `008B1B2B` |
| `008B1C00` | 31 B | calls `0067F580(01F2EA70)` | `008B1C0D`, `008B1C14` |
