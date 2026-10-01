---
system: Embedded Lua 5.2.1 and the Phyre object bindings
category: 22-Middleware-PhyreEngine
status: DOCUMENTED
owner_layer: CodeDomain:Phyre.ScriptVM + ThirdParty.Scripting.Lua
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
  passes: 2
  last_pass: 2026-09-08
  last_pass_state: GN160-xiionline-61-R7-metatable
  crossref_clean: false
  reopened_count: 0
corrects_gfz: true
---

# Embedded Lua 5.2.1 and the Phyre object bindings

> **FFXII: The Zodiac Age has a complete Lua interpreter inside it.** Not a mod loader's Lua —
> the shipping executable embeds Lua 5.2.1, and PhyreEngine wires the engine's own C++ objects
> into it through roughly 1,219 generated binding functions.

## 1. What the player sees

Nothing, in normal play — and that is the honest answer. There is no console, no script prompt,
no visible scripting feature in the retail game.

What matters is what this *makes possible*. The engine already contains a full, general-purpose
scripting language, already knows how to hand its own objects — cameras, animations, world
matrices, components — to that language, and already knows how to report when a script fails.
The plumbing a modder would otherwise have to build from scratch is compiled into the game.

The one place it becomes almost visible is failure: when a script errors, the engine formats

```
execute: lua_pcall failed - error code: %d
```

That message exists in six places in the game's own code. Something in the retail build is set
up to run Lua and report when it goes wrong.

## 2. Native mechanism

### The interpreter is Lua 5.2.1 — four independent confirmations

**1. The authored version string**, verbatim in the binary:

```
$LuaVersion: Lua 5.2.1  Copyright (C) 1994-2012 Lua.org, PUC-Rio $
$LuaAuthors: R. Ierusalimschy, L. H. de Figueiredo, W. Celes $
```

**2. `bit32` is present.** That library was *added* in Lua 5.2 and removed after it. Its presence
alone brackets the version.

**3. The 5.2-specific environment machinery**: `_ENV` (introduced in 5.2), `LUA_PATH_5_2`,
`LUA_CPATH_5_2`, `LUA_NOENV`.

**4. The stack-index constants match 5.2's 64-bit build exactly** — see the next section. This
one is structural rather than textual, and it is the strongest of the four because it cannot be
left over from a header comment.

### `lua_type`, reconstructed from the binary

`FUN_008119F0` is Lua 5.2's `lua_type` with `index2addr` inlined. Every constant checks out:

```c
uint FUN_008119f0(longlong L, int idx)
{
    if (idx < 1) {
        if (idx < -0xF4627) {                       // idx <= LUA_REGISTRYINDEX
            if (idx == -0xF4628) {                  // == LUA_REGISTRYINDEX
                o = *(L + 0x18) + 0x40;             // G(L)->l_registry
            } else {                                // an upvalue index
                cl = **(L + 0x20);                  // ci->func
                if ((int)cl[1] == 0x16) return 0xFFFFFFFF;   // light C fn: no upvalues
                if (*(byte *)(cl + 10) < -idx + -0xF4628) return 0xFFFFFFFF;  // nupvalues
                o = ((-idx + -0xF4629) + 2) * 0x10 + cl;
            }
        } else {
            o = idx * 0x10 + *(L + 0x10);           // L->top + idx
        }
    } else {
        o = idx * 0x10 + **(L + 0x20);              // ci->func + idx
        if (*(L + 0x10) <= o) return 0xFFFFFFFF;    // beyond top -> LUA_TNONE
    }
    if (o == &DAT_01CCB510) return 0xFFFFFFFF;      // luaO_nilobject -> LUA_TNONE
    return *(uint *)(o + 1) & 0xF;                  // ttypenv(o)
}
```

| Constant in body | Lua 5.2 definition | Match |
|---|---|---|
| `-0xF4628` = `-1001000` | `LUA_REGISTRYINDEX = -LUAI_MAXSTACK - 1000`, `LUAI_MAXSTACK = 1000000` (64-bit) | ✅ |
| stride `0x10` | `TValue { Value value_; int tt_; }` = 16 bytes on 64-bit | ✅ |
| `& 0xF` on the tag | `ttypenv(o)` = `novariant(rttype(o))` = `& 0x0F` | ✅ |
| `0x16` = `22` | `LUA_TLCF = LUA_TFUNCTION \| (1 << 4)` = 22 — light C function, which has no upvalues | ✅ |
| `+ 10` for the count | `CClosure.nupvalues`, right after `CommonHeader` (8 + 1 + 1) | ✅ |
| `0xFFFFFFFF` | `LUA_TNONE = -1` | ✅ |
| `DAT_01CCB510` | `luaO_nilobject`, the `isvalid()` sentinel | ✅ |

Seven independent constants, all consistent with one version. This is what pins 5.2 structurally.

### How a Phyre object is recognised — the `PhyreObject` metatable

`FUN_00682980` is the type-checked userdata fetch that nearly every binding calls first:

```c
longlong FUN_00682980(lua_State *L, int idx)
{
    p = lua_touserdata(L, idx);                     // FUN_00811950
    if (p != NULL) {
        if (lua_getmetatable(L, idx) != 0) {        // FUN_0080FBA0
            lua_getfield(L, LUA_REGISTRYINDEX, "PhyreObject");   // FUN_0080FA50
            eq = lua_rawequal(L, -1, -2);           // FUN_00810810
            lua_settop(L, -3);                      // FUN_00811130 — pop both
            if (eq != 0) return p;                  // metatables match
        }
    }
    return 0;
}
```

Note `0xFFF0B9D8` in the raw decompilation — as a signed 32-bit value that is `-1001000`, i.e.
`LUA_REGISTRYINDEX` again, this time as the argument to a field fetch.

**`"PhyreObject"` is the registry key for the shared metatable.** Every engine object handed to
Lua carries it, which is how the bindings tell "this userdata is a Phyre object" from "this is
someone else's userdata". This is the textbook `luaL_testudata` pattern.

### The generated bindings

1,219 functions carry a `Phyre.ScriptVM.*` tag. They are small and mechanical, and the *only*
thing that varies between siblings is a per-type descriptor pointer:

```c
void FUN_005a0e80(L, obj, ctx) { thunk_FUN_00682d20(obj, ctx, &DAT_02cad640); return; }
void FUN_005a1420(L, obj, ctx) { thunk_FUN_00682d20(obj, ctx, &DAT_02cad040); return; }

void FUN_005a10f0(L, obj, ctx)                  // base-class adjustment variant
{
    p = ctx + 8;                                // this-pointer fixup
    if (ctx == 0) { ... }
    thunk_FUN_00682d20(obj, p, &DAT_02cadd50);
    return;
}
```

`FUN_00682D20` is the shared push routine; the `&DAT_...` operand is the type's descriptor.

**How shared, measured 2026-09-02.** `00682D20` has only **7 direct callers** — but **834 more
reach it through jump thunks**, for **841 in total**. That is the highest thunked reach of any
function this database cites. The binding families do not call the push routine directly; they call
`thunk_FUN_00682d20`, which is why the generated code in the listing above is a single tail call.
**Nearly every one of the 1,219 bindings funnels through this one routine.**
The `+ 8` in the middle variant is a **base-class this-pointer adjustment**, which is what a
multiply-inherited type needs when pushed as one of its bases.

| Binding family | Count |
|---|---|
| `ScriptVM.ObjectPointerAccessor` | 323 |
| `ScriptVM.ObjectPushAdapter` | 305 |
| `ScriptVM.NullableObjectPushAdapter` | 299 |
| `ScriptVM.ObjectReferenceAccessor` | 265 |
| *(remaining ScriptVM families)* | 27 |
| **Total** | **1,219** |

The pointer/reference and nullable/non-nullable split mirrors C++ parameter kinds: a `T*` that
may be null needs a `nil` path, a `T&` does not.

The mangled names `PCallerImplementation`, `PCallerImplementation0` and `PInterface` appear in
the binary's RTTI and confirm these are template-generated call adapters rather than hand-written
glue.

### The game runs Lua, not just links it

Six sites in the game's own `.text` reference the `lua_pcall` failure string:

| Site | Enclosing function | GFZ tag |
|---|---|---|
| `00684E12` | `00684D10` (586 B) | `ThirdParty.Scripting.Lua` |
| `00685030` | `00684F60` (471 B) | `NativeRoutine.AcyclicDirectCall.ExtendedBounded` |
| `006850DE` | `00684F60` | same |
| `0068535A` | `006852B0` (262 B) | same |
| `006863C1` | `00686280` (1448 B) | `ThirdParty.Scripting.Lua` |
| `00686628` | `00686280` | same |

The message is authored by Square Enix / Phyre, not by Lua itself — Lua's own errors never use
that wording. Something in the retail build calls `lua_pcall` and reports the result.

`package` support is compiled in too: `luaopen_%s`, `LUA_PATH`, `LUA_CPATH`, `LUA_NOENV`, and the
default search path

```
!\lua\?.lua;!\lua\?\init.lua;!\?.lua;!\?\init.lua;.\?.lua
```

where `!` is the executable's directory on Windows. Whether the standard libraries are actually
opened at runtime is **not** established from strings alone — see **R-4**, which is the single
highest-value open question in this document.

## 3. Key addresses

| Address | Identification | Verified |
|---|---|---|
| `008119F0` | `lua_type` (with `index2addr` inlined) | ✅ read, 7 constants matched |
| `00811130` | `lua_settop` | ✅ read (call sites), tier 5 name |
| `0080FA50` | `lua_getfield` | tier 5 — signature + registry index |
| `0080FBA0` | `lua_getmetatable` | tier 5 |
| `00810810` | `lua_rawequal` | tier 5 |
| `00811950` | `lua_touserdata` | tier 5 |
| `00682980` | `Phyre::checkPhyreObject` — type-checked userdata fetch | ✅ read |
| `00682D20` | shared object push routine — `{descriptor, object}` userdata with the `PhyreObject` metatable | ✅ read 2026-09-14 (R-2) |
| `0080F420` / `00810620` | `lua_checkstack` / `lua_pushnil` | ✅ read 2026-09-14 (R-3) |
| `005A0E80` / `005A10F0` / `005A1420` | `ObjectPushAdapter` samples | ✅ read |
| `005A2BA0` / `005A2F20` / `005A3360` | `NullableObjectPushAdapter` samples | ✅ read from the disassembly 2026-09-14 (R-3) |
| `00599B70` / `00599CA0` / `00599DD0` | `ObjectPointerAccessor` samples | ✅ read |
| `00684D10` / `00686280` | Lua execution sites (`lua_pcall`) | not read |
| `01CCB510` | `luaO_nilobject` | — |
| `00D6FDE0` | the string `"PhyreObject"` | — |

## 4. Data structures and formulas

```
lua_State (5.2, 64-bit)          offsets as used by index2addr
  +0x10   StkId    L->top
  +0x18   ptr      G(L)          global_State; l_registry at G+0x40
  +0x20   ptr      L->ci         CallInfo; *ci = ci->func

TValue                           16 bytes
  +0x00   Value    value_
  +0x08   int      tt_           type tag

CClosure / LClosure
  +0x00   GCObject *next
  +0x08   lu_byte  tt
  +0x09   lu_byte  marked
  +0x0A   lu_byte  nupvalues
```

**Stack index resolution** (`index2addr`, exactly as compiled):

```
idx >= 1                       ->  ci->func + idx*16, invalid if >= L->top
LUA_REGISTRYINDEX < idx < 1    ->  L->top + idx*16
idx == LUA_REGISTRYINDEX       ->  &G(L)->l_registry
idx <  LUA_REGISTRYINDEX       ->  upvalue (LUA_REGISTRYINDEX - idx), invalid on a light C fn

LUA_REGISTRYINDEX = -LUAI_MAXSTACK - 1000 = -1000000 - 1000 = -1001000 = -0xF4628
```

**Type of a stack slot:**

```
lua_type(L, idx):
    o = index2addr(L, idx)
    return (o != luaO_nilobject) ? (o.tt_ & 0x0F) : LUA_TNONE(-1)
```

**Phyre object recognition:**

```
checkPhyreObject(L, idx):
    p = lua_touserdata(L, idx)
    if p == NULL: return NULL
    if !lua_getmetatable(L, idx): return NULL
    lua_getfield(L, LUA_REGISTRYINDEX, "PhyreObject")
    eq = lua_rawequal(L, -1, -2)
    lua_settop(L, -3)
    return eq ? p : NULL
```

## 5. Call chain

```
engine wants to run a script
  -> 00684D10 / 00686280
     -> lua_pcall
        -> on failure: "execute: lua_pcall failed - error code: %d"

script touches an engine object
  -> ScriptVM.ObjectPointerAccessor  (323)
     -> checkPhyreObject (00682980)
        -> lua_touserdata / lua_getmetatable
        -> lua_getfield(L, LUA_REGISTRYINDEX, "PhyreObject")
        -> lua_rawequal / lua_settop
     -> the C++ object pointer, or NULL

engine hands an object to a script
  -> ScriptVM.ObjectPushAdapter  (305)  /  NullableObjectPushAdapter  (299)
     -> [optional base-class this-pointer adjustment]
     -> 00682D20(obj, ctx, &typeDescriptor)
        -> descriptor comes from Phyre reflection
```

**Upstream:** whatever schedules script execution — not yet identified (**R-5**).
**Downstream:** the reflection descriptors, which supply the type identity each push needs.

**Do not confuse with:** the `.lua` files shipped in `x64\scripts\` of a modded install. Those
belong to the third-party `ff12-trampoline.dll` mod loader and have **no established connection**
to the engine's embedded interpreter. Two separate Lua environments can exist in one process.

**Also do not confuse with:** the FFXII **event/script system** (`.ebp` files, EBP2 magic
`0x8000000b`), which is a completely different, custom bytecode VM that drives story and battle
scripting. That is the one that actually runs the game. Lua is engine-level middleware.

## 6. Modding notes

- **A complete Lua 5.2.1 interpreter is already in the retail EXE.** Any tooling that wants to
  script the engine does not need to inject one.
- **Write for 5.2 specifically.** `bit32` exists; `goto` exists; the 5.1 `setfenv`/`getfenv`
  pair does not; `_ENV` replaces them. Code written for 5.1 or 5.3+ will not run unchanged.
- **`"PhyreObject"` in the Lua registry is the gate.** A userdata without that exact metatable
  is rejected by every accessor. Anything constructing engine objects for Lua must set it.
- **`package` search paths are compiled in**, including `!\lua\?.lua` — the `lua\` folder beside
  the executable. No such folder ships with the game, and whether the loader is actually
  registered is unproven (**R-4**).
- **Watch the base-class adjustment.** Push adapters for multiply-inherited types add a fixed
  byte offset to the object pointer. Hooking one and passing the unadjusted pointer will corrupt
  the object identity silently.
- **XIIOnline:** a Lua object identity is a raw in-process pointer wrapped in userdata. It is a
  local address and must never be treated as a network identity — the same rule that applies to
  BattleUnit slot indices.

## 7. What is not known

- [x] What `00684D10` and `00686280` actually execute — which scripts, from where, and when. *(closed — the register row is WITHDRAWN.)*
      **R-1.**
- [x] What `FUN_00682D20` does with the descriptor when pushing. **R-2.**
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (R-2):* **it stores the descriptor in the
      userdata, beside the object pointer.** `00682D20(L, obj, descriptor)`, read in full (112 B), runs five steps:
      1. `lua_checkstack(L, 1)` (`0080F420`, whose limit is `0xF4240` = `LUAI_MAXSTACK`).
      2. `lua_newuserdata(L, 16)` (`00810240`, which tags the value `0x47` = collectable userdata and returns the block after
         its 0x30-byte header).
      3. `ud[0] = descriptor`, `ud[8] = obj` (`00682D59` / `00682D5C`).
      4. `lua_getfield(L, LUA_REGISTRYINDEX, "PhyreObject")` (`00682D60`–`00682D6F`).
      5. A tail call of `00810F60(L, −2)`, which sets that table as the new userdata's metatable (`lua_setmetatable` by
         position).
      
      A Phyre object in Lua is therefore a 16-byte `{descriptor, object}` pair behind the shared `PhyreObject`
      metatable. `luaL_testudata`'s `00682980` hands back exactly that pair, so a binding can check the type from `ud[0]`
      before using `ud[8]`. The descriptor is not consulted during the push; nothing is converted or copied.
- [x] The `NullableObjectPushAdapter` null path — the decompilation's empty blocks hide it
      (see §8). **R-3.**
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (R-3):* **a null pointer pushes `nil`.** In
      each of the three samples (`005A2BA0`, `005A2F20`, `005A3360`), read in full, the adapter loads the object pointer from
      `[r8]`.
      - **Null:** `lua_checkstack(L, 1)` (`0080F420`), then a tail call of `00810620`. That body is Lua's `lua_pushnil`:
        `L->top->tt = 0 ; L->top += 16`.
      - **Non-null:** a tail call of `thunk_FUN_00682d20` (`00684080`) with the type's descriptor, `02CAF0E0` in the
        first sample. `005A2BA0` first adds 8 (the base-class adjustment); the other two push the pointer unadjusted.
      
      The empty blocks were the tail calls.
- [x] ~~**Whether `luaL_openlibs` runs and the `package` loader is registered at runtime.** If it
      is, the engine can load `.lua` files from disk.~~ **R-4 ANSWERED 2026-09-12 (FABLE): neither
      runs — no standard library is ever opened.** The `loadedlibs` table is at **`01CCB3E0`**:
      `{"_G", 00814F90}`, `{"table", 00815E30}`, `{"package", 00828D30}`, `{"coroutine", 00815500}`,
      `{"io", 00826500}`, `{"os", 00827430}`, `{"string", 00817550}`, `{"debug", 00828540}`, then a
      null pair — a custom build: **no `math`, no `utf8`** (`luaopen_math` is compiled in at
      `00819410`, the function that fills the lib table `01CCB160` and sets `pi` / `huge`, but it is
      in no table). Nothing references the table: no `lea` in any listed function, no rip-relative
      reference in the code outside the function list (gap index), no 8-byte pointer to it and no
      4-byte immediate of it anywhere in the file — so `luaL_openlibs`, whose only job is to walk
      that table, was dead-stripped or never linked. Each open function's **only** reference in
      the image is its table entry (one 8-byte hit each; `luaopen_string` two), and none has an
      `E8` / `E9` caller, so no library is opened individually either. Consequences: `require`,
      `package.path` / `cpath` and the searchers are never installed (the strings survive in
      `.rdata` because the code is linked, not because it runs), and the engine's only way to run
      Lua is `luaL_loadbufferx` on an in-memory chunk (§12 of the loader contract). **The engine
      cannot load `.lua` from disk.** Not established: whether a game-side binder registers the
      Phyre object functions into `_G` without the base library. **R-4.**
- [x] ~~What schedules script execution — is there a per-frame hook, or is it load-time only?~~
      **R-5 ANSWERED 2026-09-22 (FABLE): neither — the question has a third answer, because the
      scheduler is never constructed.** The 2026-09-18 note below closed the *data* route; the
      *code* route is now closed too, and together they leave none.
      - **`PScripting::PScheduler`'s vtable is `00D6FD68`** (its slot 0 is `00685140`, the executor
        § already names). **Exactly two bodies in the image reference that vtable**: `00681560`,
        which stamps it into `this` (`0068157D` / `00681584 mov [rcx], rax`) — the constructor —
        and `00681880`, which stamps it and frees — the destructor.
      - **The constructor has exactly ONE caller: `00680D80`**, and that body is 44 bytes of
        placement construction — `test rdx, rdx` / `mov rcx, rdx` / `call 00681560` / `mov al, 1`
        (`00680D97`–`00680DA5`): *construct in place at the address you are given, report success.*
      - **`00680D80` has ZERO code references and exactly one stored pointer** — `.rdata`
        `00D6F418`, which is **slot 10 of `PClassDescriptorWithoutDefaultConstructor<PScheduler>`**
        (vtable base `00D6F3C8`). *So the only route to a live `PScheduler` is the reflection
        descriptor's construct slot, reached when something asks the descriptor to make one.*

      > **And nothing ever asks.** The note below censused all **35,984** shipped `.phyre` clusters
      > and found **177 declared class names, none of them `PScheduler`, `PScript`,
      > `PScriptCallbackHandler` or `PScriptableComponent`**, and none containing `Script`,
      > `Sched`, `Lua` or `Caller`. A cluster instantiates only classes its own table declares.
      > **So the descriptor is never asked, the constructor is never called, and no `PScheduler`
      > exists at any point in the shipped game.** *“Per-frame or load-time” presupposes an object
      > that is scheduled; there is none.*

      > **Why this is a closed set and not an absence of evidence.** The sweep is over *stored
      > pointers and rip-relative references*, not the call graph: two references to the vtable,
      > one caller of the constructor, one stored pointer to that caller. Each step enumerates
      > every way the previous one can be reached.
      >
      > **The one route that does NOT need any of those, corrected 2026-09-22 (FABLE) the same
      > day — an earlier draft of this box stated the bound wrongly.** A caller does not need a
      > reference to `00680D80`; it needs the **descriptor**, and can then reach slot 10
      > virtually. So the real question is who holds the descriptor, and that is now enumerated.
      > **It is a static object at `02E41370`**, constructed at boot by the CRT initializer
      > `00166140` (zero callers; its one stored pointer is `.rdata` `008C41E0`, inside the
      > initializer table) and destroyed at exit by `008B2300` (26 bytes, the vptr swap to
      > `00D6F120` then `jmp 00633390`, zero callers — `atexit`-registered).
      >
      > **`02E41370` has nineteen referencing sites and not one belongs to the game.** Two are
      > that initializer, two are that teardown, and the remaining fifteen are all inside the
      > scripting module itself — `00680950` ×2, `00681F30` ×6, `006836B0`, `00683DC0`,
      > `00683F70`, `00685810`, `006858C0`, `006859E0`, `00685FB0`. *This is the enumeration
      > behind `DA-1`'s stated bound (“the descriptor's other references are all inside the
      > scripting module itself”), and the two that look like exceptions are the CRT's own
      > teardown rather than a consumer.*
      >
      > **So no code outside the scripting module and the CRT's init/teardown ever holds the
      > descriptor, and the scripting module's own entries are the ones nothing reaches.**
      > *Consistent with `DA-1` and `UQ-312`: the Lua path is linked, registered and reflected end
      > to end, and nothing in the shipped game enters it.* **NATIVE/STATIC — image and shipped
      > assets, nothing executed.** **R-5.**
      *Placed 2026-09-18 (FABLE), not closed:* the scheduling object is `PScripting::PScheduler` - three of its vtable slots reach the `lua_pcall` executors (the *executes a chunk* level below) - so *what schedules* is a class, and whether it is per-frame is a question about an object that, on the evidence added under `DA-1` the same day, the shipped data never creates. *Narrowed 2026-09-18 (FABLE), from the data side:* **no shipped asset declares a scripting class.** The image registers four - `PScheduler`, `PScript`, `PScriptCallbackHandler`, `PScriptableComponent` (the registrar join, [phyre-registrar-classes.tsv](../Reflection-And-Class-Metadata/members/phyre-registrar-classes.tsv)) - and the corpus census of all 35,984 shipped `.phyre` clusters ([the packed-namespace page](../Phyre-Asset-Container/the-packed-namespace-and-the-file-side-schema.md)) finds 177 declared class names, none of them one of the four and none containing `Script`, `Sched`, `Lua` or `Caller`. A cluster instantiates only classes its own table declares, so the reflection route - the one way a scheduler or a script object could come to exist without a direct constructor call, and the only kind of route the static trace could not follow - has nothing to instantiate in the shipped game. *Bound:* a native caller that asks the `PScheduler` descriptor for an instance through a virtual slot would not show here; the descriptor's other references are all inside the scripting module itself. The live check stays the decider; the static-plus-data weight is now against a scheduler ever existing.
- [x] ~~The exact boundaries of the Lua library in the address space.~~ **R-6 ANSWERED** (§10, 2026-09-03, by naming every `luaL_Reg` function; *exact link range 2026-09-13 (FABLE):* every census entry from `0080F2E0` up to `00830760` — a zlib object and four import thunks below, Bullet above — declared as the Lua 5.2.1 row on [the inventory](../../23-Third-Party-Libraries/third-party-middleware-inventory.md)). **R-6.**
- [x] ~~Whether the `PhyreObject` metatable carries `__index` / `__newindex` handlers, and what
      they expose.~~ **R-7 ANSWERED 2026-09-08 — no.** The `__index`/`__newindex`/`__eq` strings
      sitting beside `PhyreObject` in `.rdata` are **Lua's own**, entries 0, 1 and 5 of
      `luaT_eventname[]` at `01CCBA90`. **Phyre's binding layer names none of them**; `__newindex`
      and `__eq` are referenced by nothing in the image. **The metatable is an identity token, not a
      dispatch table.** See the section at the end of this document.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The interpreter is Lua 5.2.1 | authored `$LuaVersion: Lua 5.2.1 …` string in the authorized EXE | 2 |
| Version corroborated three more ways | `bit32`, `_ENV`, `LUA_PATH_5_2` strings | 2 |
| Version corroborated structurally | 7 constants in `FUN_008119F0` matching 5.2's 64-bit build | 1 |
| `FUN_008119F0` is `lua_type` | complete body; `index2addr` shape + `ttypenv` + `LUA_TNONE` | 1 |
| `"PhyreObject"` is the registry metatable key | `lua_getfield(L, LUA_REGISTRYINDEX, "PhyreObject")` in `FUN_00682980` | 1 |
| `FUN_00682980` is a type-checked userdata fetch | complete body — the `luaL_testudata` sequence | 1 |
| Push adapters differ only by type descriptor | three sibling bodies read; identical but for the `&DAT_` operand | 1 |
| Base-class this-pointer adjustment | the `+ 8` in `FUN_005A10F0` against siblings with none | 1 |
| The game calls `lua_pcall` | 6 RIP-relative LEA references to the failure string, resolved to enclosing functions | 1 |
| Binding family counts | GFZ `CodeDomain` tag census | 3 |
| EXE provenance | SHA-256 of the file read matches the authority SHA exactly | 1 |

### The GFZ under-attributes the Lua C API — a correction, with numbers

`FUN_008119F0` is `lua_type`. It is proven above from its complete body against seven Lua 5.2
constants. The GFZ classifies it as:

```
GFZ.V121.CodeDomain.NativeInline.BoundedLoop.NoComputedTransfer
```

That is a **generic structural filler tag** — it describes the function's control-flow shape and
says nothing about what it is. The same is true of its neighbours: `lua_settop`, `lua_getfield`,
`lua_getmetatable`, `lua_rawequal` and `lua_touserdata` all carry `NativeInline` / `NativeLeaf` /
`NativeRoutine` shape tags.

Measured over the cluster that provably contains the Lua C API:

```
0x80F000 - 0x812FFF :  108 functions,  6 tagged Lua,  102 generic  (94%)
```

Across the whole 90-function `ThirdParty.Scripting.Lua` domain, the tagged set sits at `0x680000`
(2), `0x800000` (1), `0x810000` (40) and `0x820000` (47) — so the domain exists and is correct
where applied; it simply stops short of the C API surface.

**This does not make the GFZ wrong, it makes it incomplete**, and the distinction matters. Every
GFZ tag examined here was *true*; 102 of them were merely uninformative. That is a different
failure from the ScriptVM dispatch-table case, where a GFZ claim was substantively wrong.

The `Phyre.ScriptVM.*` naming, incidentally, is **vindicated**: there really is a script VM, and
those 1,219 functions really do bind objects into it.

### A false negative I published to myself and had to retract

Partway through this block I ran `strings` against the EXE, grepped for `lua`, `luaL_`,
`__index`, `PhyreObject` and eleven other markers, and got **zero for every one**. I recorded
"there is no scripting VM in this binary" and began writing up the `ScriptVM` tag as a misnomer.

`strings` is not installed on this machine. The command emitted nothing and the pipeline dutifully
counted nothing. Re-running the same searches by reading the file bytes in Python found
`PhyreObject`, `_ENV`, `__index`, `__newindex`, `bit32`, `luaopen_` and the full version banner
immediately.

**A zero from a tool that did not run looks exactly like a zero from a tool that found nothing.**
The check that would have caught it costs one line: search for a string already *known* to be
present — `PhyreObject` had appeared in a decompilation minutes earlier — and treat a zero on the
positive control as a broken tool, not as evidence. That control is now the rule for any
absence-based claim in this database.

The order also matters. The structural derivation of `LUA_REGISTRYINDEX` was what forced the
retraction, and it came from reading a body rather than querying a tool. **Absence of evidence
from tooling lost to a structural proof from the binary, which is the correct precedence.**


## 12. The two callers executed — [`EXP-110`](../../_experiments/EXP-110-phyre-script-callers-exec.md), folded in 2026-09-19 (OPUS)

`EXP-110` ran `00684D10`, `00684F60` and `00686280` from shipped bytes with the Lua stack
primitives real. **It does not answer §7's open item** — *which* scripts these execute, from where
and when, is still unknown and stays open. What it settles is **how** they marshal arguments and
dispatch results, which is the part a reimplementation needs.

> The request routed this to `CONTRACT-lua-chunk-loader`. That contract is about turning bytes into
> a chunk; these three are the **callers**, and this is their page.

### There are TWO sentinel chains, and they are not the same length

`00686280` compares a returned pointer against a chain of sentinel getters. **The marshal side
compares twelve; the result dispatch compares nine.** A static reading that found the twelve and
applied them to both is where the "12" came from.

| | sites | getters |
|---|---|---|
| **marshal**, `00686437`–`006865A3` | 12 | `00630490`, `0062FF50`, `0062FFC0`, `00630030`, `006300A0`, `00630110`, `00630180`, `00630420`, `006303B0`, **`006301F0`, `00630260`, `006302D0`** |
| **result dispatch**, `0068664B`–`00686772` | **9** | the same list **minus the three in bold** |

**The three the dispatch does not compare are the last three of the marshal's set**, and they fall
through to the generic fallback instead of taking a typed arm — which is exactly `EXP-110`'s
*"s9/s10 and s11 fall into the GETA/GETB/MSHL/unknown fallback"*, arrived at from the other side.

### The result store is 1/2/4/8, not 1/4/8

Every dispatch arm writes the tag slot at `[r14+8]`, and the widths are **not** three:

| width | sites |
|---|---|
| `byte` | `0068667D`, `006866B1` |
| **`word`** | **`006866EF`** |
| `dword` | `0068672E` |
| `qword` | `0068676C`, `006867B8` |

**A grouping that reads the `word` arm as a `dword` writes two bytes it should not.** This is a
reconstruction-visible ABI detail, not a cosmetic one.

### `006372A0` returns a constant address

```
006372A0  lea rax, [rip + 0x26c0fc9]   ; 02CF8270  .data
006372A3  ret
```

Seven bytes, no load — **it is the address of a `.data` cell, not a read of one, and not a TLS
access.** The dispatch compares against `SING() | rbp`, and `rbp` is set to `1` at `006863FF`
before the chain begins, so **the comparand is statically `02CF8271`** — established here without
relying on the trace.

### What a model of the Lua stack must get right

- **Pops preserve bytes.** `SETTOP` and the pcall-side pops move `q[state+0x10]` only; a popped
  `TValue` image stays resident and is re-observable if the top revisits the slot. **Slot storage
  must be indexed independently of logical depth** — and depth can go *negative*, because a pcall
  can push the top below the frame base.
- **Only three typed pushes exist in the marshal loop** — `PUSHB` (boolean), `PUSHN` (number),
  `PUSHI` (everything else matched). There is no dedicated pusher for the `s11` tag; it takes the
  `PUSHI` arm. The dispatch helper `00681010` is reached only by *unmatched* tags.
- **`SETFLD` consumes `PUSHP`'s type tag.** The popped slot's `d8` is the only path by which the
  light-userdata tag (`ty = 2`) is observable at all.

### Two rough edges in the shipped code

- **A null-state checkout is still consumed.** `00686280` checks out exactly one element per pool
  even when that element's state fails its gate — the cursor advances regardless. A reimplementation
  that retries on a failed gate drifts the cursor.
- **`00684D10`'s early-exit `esi` is uninitialised** on the loader-fail path; the observed
  `0xFFFFFFFE` is the register's leftover value, not a chosen code. **Do not treat it as a status.**

Also measured: the cursor holder points **directly** at the payload array — `q[holder + i*8]`, with
no second indirection — and the unknown-result log passes leftover `r14` as its `r8`, which is
visible only in a trace and is not a recomputed argument.

*(OPUS 2026-09-19, on `REQ-OPUS-PHYRE-CALLERS-FINDINGS` from SWE2-ORACLE. Each finding re-read from
the bytes; the sentinel counts re-derived independently and found to be two chains rather than one
disputed bound.)*

## 9. Related

- [`../Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`](../Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md) — the descriptors these bindings push
- [`../../01-Script-VM-Native-Bridge/`](../../01-Script-VM-Native-Bridge/) — the *game's* `.ebp` script VM, a different system entirely
- [`../../23-Third-Party-Libraries/`](../../23-Third-Party-Libraries/) — Lua sits alongside Bullet, libvpx, zlib, libvorbis and Dear ImGui
- [`../../_index/EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md) — the positive-control rule this block added

## 9. Falsification pass 2026-09-02 — the control case

**Attack chosen, and why this one.** One pass earlier, this document's sibling —
[`../Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`](../Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md)
— was found to have a **correct total with a wrong breakdown**: eight of its ten family rows were
undercounted and 256 functions were misfiled into a `(remaining)` row. Same author, same counting
method, same shape of table. **A defect found in one document must be looked for in its siblings**,
so this document's family table was attacked with exactly that failure in mind.

**Result: SURVIVED, completely.** An exact-component census of every
`GFZ.V121.CodeDomain.Phyre.ScriptVM.*` tag across all 38,161 functions reproduces **every row**:

| Binding family | Document | Census | |
|---|---:|---:|---|
| `ScriptVM.ObjectPointerAccessor` | 323 | **323** | match |
| `ScriptVM.ObjectPushAdapter` | 305 | **305** | match |
| `ScriptVM.NullableObjectPushAdapter` | 299 | **299** | match |
| `ScriptVM.ObjectReferenceAccessor` | 265 | **265** | match |
| *(remaining families)* | 27 | **27** | match — `ReflectionBridge` 20, `VarargsBridge` 2, `InputBinding` 2, `CrossContextObjectCopy` 1, `ScriptEntryPoint` 1, `ApplicationBridge` 1 |
| **Total** | **1,219** | **1,219** | match |

The census also shows **1,219 tag instances across 1,219 distinct functions**, so no function is
counted twice through multiple ScriptVM tags.

**This is the control that diagnoses the sibling's failure.** The same method, applied by the same
author to the same kind of table, produced a breakdown that is exact in every row here. That rules
out a systematic flaw in how these tables are counted, and supports the sibling's diagnosis
precisely: there, the family rows and the total came from **two different queries** and only the
total was checked. Here they plainly came from one.

### `"PhyreObject"` — upgraded from asserted to unique

§2 says *"`"PhyreObject"` is the registry key for the shared metatable"* and §3 cites the string at
`00D6FDE0`. Both check out, and the scan adds something the document did not claim:

```
00D6FDE0  (.rdata)  50 68 79 72 65 4f 62 6a 65 63 74 00   "PhyreObject"
```

The byte sequence `PhyreObject\0` occurs **exactly once in the entire 32 MB image**. So the string is
not merely *a* registry key used at the site read in `checkPhyreObject` — there is no second copy
anywhere for a different metatable to use. "The registry key" is now a **uniqueness result** rather
than an inference from one call site.

### Not attacked

The `lua_type` reconstruction (§2) and its seven matched constants were not re-derived this pass;
they remain tier 1 on the original read. The Lua 5.2.1 version pin was independently re-confirmed
during pass 6 from the `$LuaVersion` banner in the image.

## 10. The Lua standard library, named exactly — 2026-09-03

**R-6 is answered.** The Lua library's boundary in the address space is not a guess: the interpreter
registers its C functions through `luaL_Reg` arrays, and those arrays are in the image, so **every
standard-library function can be named by the name Lua itself calls it.**

### The predicate

A 16-byte record is a `luaL_Reg` entry iff **both** its qwords carry an `IMAGE_REL_BASED_DIR64`
relocation, the first points at a printable NUL-terminated C string of 1–32 bytes, and the second
points at a **known function entry**. Runs of three or more consecutive such records are an array.

```c
typedef struct luaL_Reg { const char *name; lua_CFunction func; } luaL_Reg;   /* 16 bytes */
```

That is Lua 5.2's own declaration, and it matches the layout measured here byte for byte — name at
`+0`, function at `+8`. This document already established the interpreter is **Lua 5.2.1** from its
version banner and the presence of `bit32`; the register arrays are an independent confirmation of
the same version, because `bit32` exists as a library **only** in 5.2.

**148 records matched; 145 of them fall in 12 arrays; 143 distinct functions are named.**

### The twelve arrays

| base | entries | library |
|---|---:|---|
| `01CCB160` | 27 | **math** |
| `01CCA3F0` | 22 | **base (_G)** |
| `01CCC6C0` | 16 | **debug** |
| `01CCAD50` | 14 | **string** |
| `01CCAFF0` | 12 | **bit32** |
| `01CCC0B0` | 11 | **io** |
| `01CCC2E0` | 11 | **os** |
| `01CCC170` | 9 | **io file methods** |
| `01CCB3E0` | 8 | **loadedlibs — opened at startup** |
| `01CCA950` | 6 | **coroutine** |
| `01CCAA90` | 6 | **table** |
| `01CCB470` | 3 | **preloadedlibs — available via require** |

Two of the twelve are not libraries but Lua 5.2's own bootstrap lists from `linit.c`:
**`01CCB3E0` is `loadedlibs`** — the eight libraries opened at startup (`_G`, `table`, `package`,
`coroutine`, `io`, `os`, `string`, `debug`) — and **`01CCB470` is `preloadedlibs`**, the three left
for `require` (`bit32`, `math`, `string`). Stock 5.2 opens all of them at startup, so **this build
moved `bit32` and `math` out of the startup set**; `string` appears in both lists.

### The complete map

Every row is `lua_CFunction` address to the exact name Lua exposes it under.


**`01CCB160` — math** (27)

| name | address | name | address |
|---|---|---|---|
| `abs` | `00818A80` | `log` | `00818F40` |
| `acos` | `00818C80` | `max` | `008191F0` |
| `asin` | `00818C40` | `min` | `00819170` |
| `atan2` | `00818D00` | `modf` | `00818E40` |
| `atan` | `00818CC0` | `pow` | `00818EE0` |
| `ceil` | `00818D60` | `rad` | `00819080` |
| `cosh` | `00818B80` | `random` | `00819270` |
| `cos` | `00818B40` | `randomseed` | `008193E0` |
| `deg` | `00819040` | `sinh` | `00818B00` |
| `exp` | `00819000` | `sin` | `00818AC0` |
| `floor` | `00818DA0` | `sqrt` | `00818EA0` |
| `fmod` | `00818DE0` | `tanh` | `00818C00` |
| `frexp` | `008190C0` | `tan` | `00818BC0` |
| `ldexp` | `00819110` |  |  |

**`01CCA3F0` — base (_G)** (22)

| name | address | name | address |
|---|---|---|---|
| `assert` | `00814CD0` | `print` | `008141F0` |
| `collectgarbage` | `008147B0` | `rawequal` | `00814650` |
| `dofile` | `00814C50` | `rawlen` | `008146A0` |
| `error` | `008144D0` | `rawget` | `00814700` |
| `getmetatable` | `00814550` | `rawset` | `00814750` |
| `ipairs` | `008149E0` | `select` | `00814D20` |
| `loadfile` | `00814A70` | `setmetatable` | `008145B0` |
| `load` | `00814B30` | `tonumber` | `00814340` |
| `next` | `008148F0` | `tostring` | `008141C0` |
| `pairs` | `00814950` | `type` | `008148B0` |
| `pcall` | `008140A0` | `xpcall` | `00814120` |

**`01CCC6C0` — debug** (16)

| name | address | name | address |
|---|---|---|---|
| `debug` | `00828140` | `upvaluejoin` | `00827DA0` |
| `getuservalue` | `00827530` | `upvalueid` | `00827D60` |
| `gethook` | `00828000` | `setuservalue` | `00827570` |
| `getinfo` | `00827600` (interior read 2026-09-17, SWE2-FRONTIER: `008119F0` first at [`0082762F`](../../_index/ADDRESS-INDEX.md), `00810DF0` ×14 + `00810660`/`00810580` ×5 — the debug-library info builder) | `sethook` | `00827E50` |
| `getlocal` | `00827A10` | `setlocal` | `00827B60` |
| `getregistry` | `00827470` | `setmetatable` | `008274D0` |
| `getmetatable` | `00827490` | `setupvalue` | `00827CE0` |
| `getupvalue` | `00827C60` | `traceback` | `00828330` |

**`01CCAD50` — string** (14)

| name | address | name | address |
|---|---|---|---|
| `byte` | `00816C50` | `len` | `00816790` |
| `char` | `00816D70` | `lower` | `00816940` |
| `dump` | `00816E50` | `match` | `00815F30` |
| `find` | `00815F20` | `rep` | `00816AC0` |
| `format` | `008162F0` (interior read 2026-09-17, SWE2-FRONTIER: `0080FD00` first at [`0081632E`](../../_index/ADDRESS-INDEX.md), `00813450`/`00812590` ×3 + `0017D2E0` ×4 — the format-string builder) | `reverse` | `008168A0` |
| `gmatch` | `00815F40` | `sub` | `008167C0` |
| `gsub` | `00815FA0` | `upper` | `00816A00` |

**`01CCAFF0` — bit32** (12)

| name | address | name | address |
|---|---|---|---|
| `arshift` | `00818760` | `extract` | `00818880` |
| `band` | `008184B0` | `lrotate` | `008187E0` |
| `bnot` | `00818670` | `lshift` | `008186A0` |
| `bor` | `00818590` | `replace` | `00818950` |
| `bxor` | `00818600` | `rrotate` | `00818830` |
| `btest` | `00818520` | `rshift` | `00818700` |

**`01CCC0B0` — io** (11)

| name | address | name | address |
|---|---|---|---|
| `close` | `00825570` | `popen` | `00825770` |
| `flush` | `00825E50` | `read` | `00825AF0` |
| `input` | `008258A0` | `tmpfile` | `00825820` |
| `lines` | `00825A10` | `type` | `00825490` |
| `open` | `00825660` | `write` | `00825BC0` |
| `output` | `00825930` |  |  |

**`01CCC2E0` — os** (11)

| name | address | name | address |
|---|---|---|---|
| `clock` | `00826C10` | `remove` | `00826AB0` |
| `date` | `00826C50` | `rename` | `00826B00` |
| `difftime` | `00827200` | `setlocale` | `00827260` |
| `execute` | `00826A50` | `time` | `00826F50` |
| `exit` | `008272D0` | `tmpname` | `00826B60` |
| `getenv` | `00826BD0` |  |  |

**`01CCC170` — io file methods** (9)

| name | address | name | address |
|---|---|---|---|
| `close` | `00825570` | `setvbuf` | `00825DA0` |
| `flush` | `00825EC0` | `write` | `00825C30` |
| `lines` | `008259C0` | `__gc` | `00825600` |
| `read` | `00825B60` | `__tostring` | `00825510` |
| `seek` | `00825CA0` |  |  |

**`01CCB3E0` — loadedlibs — opened at startup** (8)

| name | address | name | address |
|---|---|---|---|
| `_G` | `00814F90` | `io` | `00826500` |
| `table` | `00815E30` | `os` | `00827430` |
| `package` | `00828D30` | `string` | `00817550` |
| `coroutine` | `00815500` | `debug` | `00828540` |

**`01CCA950` — coroutine** (6)

| name | address | name | address |
|---|---|---|---|
| `create` | `008150F0` | `status` | `008151F0` |
| `resume` | `00815050` | `wrap` | `00815150` |
| `running` | `00815300` | `yield` | `008151C0` |

**`01CCAA90` — table** (6)

| name | address | name | address |
|---|---|---|---|
| `concat` | `008156F0` | `unpack` | `00815950` |
| `insert` | `00815540` | `remove` | `00815610` |
| `pack` | `008158A0` | `sort` | `00815A40` |

**`01CCB470` — preloadedlibs — available via require** (3)

| name | address | name | address |
|---|---|---|---|
| `bit32` | `00818A40` | `string` | `00817550` |
| `math` | `00819410` |  |  |

### What this does and does not settle

- **It names 143 functions exactly**, replacing generic shape tags with the identity the language
  itself uses. `FUN_00818a80` is `math.abs`.
- **It bounds the standard library**: the named functions span `00814xxx`–`0081Cxxx`, which is where
  the Lua C API lives, and gives R-6 a concrete answer rather than an estimate.
- **It does not name the interpreter core.** `lua_*` API functions and the VM itself carry no
  `luaL_Reg` entry, so they are untouched by this method.
- **It says nothing about which of these the game's own scripts may call.** Registration is not
  reachability; the sandbox question is separate and is not addressed here.

## 11. Registration is not reachability — four libraries of eleven — 2026-09-03

§10 named 143 standard-library functions. **Being registered in a `luaL_Reg` array does not mean a
script can call them**, and this section separates the two.

### `luaL_openlibs` does not run

Lua 5.2 opens its libraries by walking two arrays from `linit.c`. Both are present in this image —
§10 identified them as `loadedlibs` at `01CCB3E0` and `preloadedlibs` at `01CCB470` — and **neither
is referenced by any instruction, nor by any 8-byte pointer anywhere in the file.**

That is an absence claim, so it carries a control: of the **twelve** `luaL_Reg` bases §10 recovered,
**ten are referenced** from `.text`, each by exactly one function — the `luaopen_*` that installs it.
The two that are not are precisely the two bootstrap lists.

| base | library | referenced by |
|---|---|---|
| `01CCA3F0` | base | `00814F90` = **`luaopen_base`** |
| `01CCA950` | coroutine | `00815500` = **`luaopen_coroutine`** |
| `01CCAA90` | table | `00815E30` = **`luaopen_table`** |
| `01CCAD50` | string | `00817550` = **`luaopen_string`** |
| `01CCAFF0` | bit32 | `00818A40` = **`luaopen_bit32`** |
| `01CCB160` | math | `00819410` = **`luaopen_math`** |
| `01CCC0B0` + `01CCC170` | io + file methods | `00826500` = **`luaopen_io`** |
| `01CCC2E0` | os | `00827430` = **`luaopen_os`** |
| `01CCC6C0` | debug | `00828540` = **`luaopen_debug`** |
| `01CCB3E0` | `loadedlibs` | **nothing** |
| `01CCB470` | `preloadedlibs` | **nothing** |

**Nine more functions named**, and the standard bootstrap path is inert data.

### The game ~~opens~~ **registers** four libraries, by name, from one function — and nothing opens them *(heading corrected by FABLE, Claude Opus 5.5, 2026-09-25)*

> **Corrected 2026-09-25 (FABLE, Claude Opus 5.5), UQ-284.** The registrations below fill a list
> that **no code ever reads**. The four `luaopen_*` are never called, so no standard library is
> opened, which agrees with R-4 above. The table "What that means for a script" is amended to match,
> and the evidence is in [§ UQ-284 answered](#uq-284-answered--the-four-registrations-feed-a-list-nothing-reads-fable-claude-opus-55-2026-09-25).

`FUN_00685AC0` (120 B) makes five setup calls and then four registrations, each passing a name string
and a `luaopen_*`:

```asm
00685ADD  lea rdx, [00819410]  ; luaopen_math       lea rcx, [00D701CC] "math"
00685AF0  lea rdx, [00818A40]  ; luaopen_bit32      lea rcx, [00D701D4] "bit32"
00685B03  lea rdx, [00817550]  ; luaopen_string     lea rcx, [00D701DC] "string"
00685B16  lea rdx, [00815500]  ; luaopen_coroutine  lea rcx, [00D701E8] "coroutine"
          -> each: call FUN_006844C0(name, openFunction)
```

`FUN_006844C0` appends the pair to a growable 16-byte-per-entry list. **It has exactly four call
sites in the entire image, all four of them above.**

### What that means for a script

| library | registered? | opened? | evidence |
|---|---|---|---|
| `math`, `bit32`, `string`, `coroutine` | **yes** | **no** *(2026-09-25)* | the four registrations above, into a list nothing reads (UQ-284) |
| `base` (`_G`), `table`, `io`, `os`, `debug` | **no** | **no** | `luaopen_*` has **zero direct callers and zero address-takings** outside the two inert bootstrap arrays |

**`io`, `os` and `debug` are compiled into the executable and never registered.** Their code is
present and reachable by nothing: a script cannot call `os.execute`, `io.open` or `debug.sethook`
through this path, because the tables that would have installed them are never walked and their
openers are never called.

**For a modder that is the practical shape of the sandbox**: the Lua that ships here is not a general
Lua environment with dangerous parts removed — it is one where **only four of the eleven standard
libraries were ever wired up**, and the omission includes the two libraries that touch the operating
system. *(2026-09-25: "wired up" means registered only. Even those four are never opened; see
UQ-284.)*

### What is not established

- [x] ~~**UQ-282.** **`base` and `table` being absent is surprising and is not fully explained here.** A Lua
      environment with no `print`, `pairs`, `type` or `setmetatable` is unusual. The likeliest
      explanation is that the script environment is built by the **Phyre binding layer** documented in
      this file rather than by stock Lua, and supplies its own globals — but that is **not traced**,
      and this section does not claim it.~~ **ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5): the premise was
      selective absence, and it is false.** `base` and `table` are not singled out. The four
      "registered" libraries are never opened either (UQ-284), so **no standard library is opened by
      this build at all**, as R-4 found for the bootstrap path. Whether any `lua_State` is ever
      created is a separate question, `DA-1`, and it is unchanged.
- [x] **UQ-283.** The five calls `FUN_00685AC0` makes before the four registrations (`006822E0` — **now read 2026-09-17, SWE2-FRONTIER:** 1,237 B carrying `m_defaultEntryPoint`/`m_executionInterval`/`m_functionNames` field names + `006388C0` registration at [`00682300`](../../_index/ADDRESS-INDEX.md), `008092FC`/`0080929C`/`00808B90` driver thunks ×9 — a script-binding descriptor body, not a global installer —, `00681F30`,
      `006827C0`, `00681C50`, `00681D80`) were **not read**. If any of them installs globals, the
      picture above is a floor rather than the whole environment.
      **ANSWERED 2026-09-18 (FABLE) — the five bodies are the five scripting classes' reflection registrations, and none of them touches Lua.** `00685AC0` (`00685AC4`–`00685AD8`) calls the five bodies directly, and every one opens the same way: `lea rcx, <descriptor>` then `call 006388C0`, the by-name registration the [class-descriptor contract](../Reflection-And-Class-Metadata/CONTRACT-phyre-class-descriptor.md) reads (it hashes the `char *` at `+0x30`). The five descriptors are the `PScripting` module's `PClassDescriptor` statics at a `0x100` stride: `006822E0` → `02E41470` (`PScript`, `006822F9`), `00681F30` → `02E41370` (`PScheduler`, vtable `00D6F3C8` installed by `00166140`), `006827C0` → `02E41170` (`PClassDescriptorConcrete<PScriptCallbackHandler>`), `00681C50` → `02E41270` (`PAsyncProcessHeader`), `00681D80` → `02E41070` (`PClassDescriptorWithoutDefaultConstructor<PClassCallableMethodScript>`, vtable `00D6EBF8` installed by `00166100`). After the registration each body builds that class's reflected members under `_Init_thread_header` / `_Init_thread_footer` guards with `atexit` teardown: `00681F30` (939 B) constructs four `PFunctionCallerConcrete<PScheduler *>` statics at `02E424A0`, `02E42500`, `02E42560` … named `GetCurrentScheduler`, `GetCurrentScript`, `addScript`, `removeScript` (`00D70040`–`00D70080`), through the caller constructor `00632FB0` and `005A7A40` / `005A0470`; `00681C50` (289 B) constructs one `PMethodCallerConcrete<PAsyncProcessHeader>` at `02E42440` (vtable `00D70200`) for `getAsyncResult`, whose method body is `008B2480`; `006827C0` (299 B) registers `PScriptCallbackHandler`'s `m_entryPoint` (`+0x0`) and `m_handler` (`+0x8`) through the member constructor `00632960`; `00681D80` (417 B) registers `PClassCallableMethodScript`'s `m_script` (`+0x50`), `m_nameAsString` (`+0x58`) and `m_entryPoint` (`+0x60`); `006822E0` registers `PScript`'s `m_defaultEntryPoint` / `m_executionInterval` / `m_functionNames` (SWE2's reading). The rows already sit in [`phyre-field-schema.tsv`](../Reflection-And-Class-Metadata/phyre-field-schema.tsv) and [`members/phyre-pscripting.tsv`](../members/phyre-pscripting.tsv). **The callee sets settle the question the box asked:** across the five bodies the external callees are `006388C0`, `00639450`, `00632960`, `00632A10`, `00632FB0`, `005A7A40`, `005A0470`, `005EF7E0`, `00618970`, `0062FFC0`, `00630180`, `00630490` and the three CRT guards — no `lua_*` or `luaL_*` body and no Lua state — so no global is installed before the four `luaopen_*` registrations, and the environment picture above is the whole of what `00685AC0` builds. The 2026-09-16 register reading (one shape over five `0x100`-stride objects with per-object once-guards) and this page's text (five distinct bodies) were both right: the shape is the registration, the bodies are the per-class member batteries. The sixth `0x100` slot `02E41570` belongs to a class none of the five registers and is outside this question. Static: the six bodies and the RTTI of the vtables they install.
- [x] ~~**UQ-284.** Whether the registered four are opened immediately or deferred until `require`.
      `FUN_006844C0` stores the pair rather than calling it, so **deferral is the reading the body
      supports**, but the consumer of that list was not traced.~~ **ANSWERED 2026-09-25 (FABLE, Claude Opus
      5.5): neither. The list has no consumer.** The only code touching it adds pairs, or frees it.
      `require` does not exist either, because `luaopen_package` never runs (R-4). See the section
      below.

## UQ-284 answered — the four registrations feed a list nothing reads (FABLE, Claude Opus 5.5, 2026-09-25)

**The list.** `006844C0` keeps the `(name, luaopen_*)` pairs in a growable array: a `u32` count
with bit 31 as a flag at **`02E41570`**, and the 16-byte-entry buffer pointer at **`02E41578`**.
It reads both cells, allocates `count + 1` entries, copies the old entries across and appends the
new pair (`006844CB`–`0068454E`).

**Every reference to either cell in the whole image**, taken three ways:
- **RIP-relative**, over `02E41500`–`02E41600`. Three functions: the appender `006844C0`;
  `00685F60`, which frees the buffer and zeroes both cells; and `008B25C0`, which does the same as
  an `atexit` teardown.
- **Image-relative 32-bit** (`0x2D21570` / `0x2D21578`) and **absolute 64-bit** pointers, in every
  section: **none**.
- **A base plus displacement**: every function that takes an address in `02E41000`–`02E4156F` (800
  functions, since the `PScripting` class descriptors sit at a `0x100` stride just below). None
  uses a displacement that lands on the two cells. The matcher is not blind: the same sweep finds
  3,380 `+0x30` operands.

**Who calls whom.** `00685AC0` and `00685F60` are slots 1 and 2 of the
`Phyre::PScripting::PUtilityScripting` vtable `00D6FD98`: one fills the list, the other frees it. The static object at `01F2EAC8` gets that vtable before `main` (`00166210`, above). **So slot 1
appends four pairs, slot 2 frees them, and nothing in between
reads the list.** Each of the four `luaopen_*` has no `call`, `jmp` or `jcc` site. Its only
references are its `lea` in `00685AC0` (`00685ADD`, `00685AF0`, `00685B03`, `00685B16`) and its
8-byte entries in the two inert bootstrap arrays, so none is ever called.

**What that answers.**
- UQ-284: the four are **neither opened at startup nor deferred to `require`**.
- UQ-282: `base` and `table` are not selectively missing. **No standard library is opened.**

What would still change this is code that reaches the cells through a pointer this sweep cannot
see, such as one computed at run time from an unrelated base. A breakpoint on read of `02E41578` in
a live session is the direct test. It is not needed for the static answer, because nothing in the
image forms that address.


## R-7 answered — 2026-09-08: the metatable is a name tag, not a behaviour table

**`R-7` asked whether the `PhyreObject` metatable carries `__index` / `__newindex`, and what they
expose. It does not, and the strings that made it look as though it might belong to Lua.**

### The trap this document's reader was one step from

In `.rdata` the strings sit like this:

```
00D6FDE0  'PhyreObject'
00D6FDF0  '__index'
00D6FDF8  '__newindex'
00D6FE04  '__eq'
00D6FE10  'm_script'
00D6FE20  'm_entryPoint'
```

`PhyreObject`, then exactly the three metamethods a binding layer would install, then two Phyre
reflection field names — **and immediately before them, the vtable of
`Phyre::PScripting::PClassCallableMethodScript::PCallerScript`.** It reads like Phyre's metatable
construction with its own strings around it.

**It is not. `__index`, `__newindex` and `__eq` are Lua's.**

They are entries **0, 1 and 5** of Lua 5.2's `luaT_eventname[]` table, which sits at **`01CCBA90`**
and whose seventeen entries read in exact tag-method order:

```
[0] __index  [1] __newindex  [2] __gc    [3] __mode   [4] __len    [5] __eq     [6] __add
[7] __sub    [8] __mul       [9] __div  [10] __mod   [11] __pow   [12] __unm   [13] __lt
[14] __le   [15] __concat   [16] __call
```

**The linker scattered that table's strings across `.rdata`** — some at `00D6FDxx` beside Phyre's,
some at `01CCBBxx`, some at `00D701xx`. **Their proximity to `PhyreObject` carries no meaning
whatever**, which is exactly why this database forbids address adjacency as evidence.

### What actually references them

| string | code references | in |
|---|---:|---|
| `PhyreObject` | **13** | the binding layer, including `FUN_00682980` this document already reads |
| `__index` | **2** | both inside Lua — `00826500` is tagged `ThirdParty.Scripting.Lua` |
| `__newindex` | **0** | — |
| `__eq` | **0** | — |

> **Nothing in Phyre's binding code names any of the three.** The only code that names `__index` is
> Lua's own interpreter, using its standard event table.
>
> So the answer to `R-7` is **negative**: the metatable is **an identity token, not a dispatch
> table** — created, stored under the registry key `"PhyreObject"`, and compared with
> `lua_rawequal`, precisely as §4 of this document already describes. **There is no evidence of a
> field-access handler behind it.**

**The honest limit:** an absent reference to a *name string* does not prove no metamethod is
installed, because Lua itself sets metafields by indexing the event table rather than by naming the
string. What is established is narrower and still decisive for a modder: **the Phyre binding layer
never names these metamethods, and two of the three are named by nothing in the image at all.**

### Bonus — where the "uncalled" Lua executors live

Two of the four functions that report `execute: lua_pcall failed` have **zero callers** (`00684D10` and `00686280`) in the call
graph: `00684D10` and `00686280`.

**They are vtable slots.** The vtable at `00D6FDB8` — RTTI complete-object-locator `01D25F10`,
type descriptor `.?AVPCallerScript@PClassCallableMethodScript@PScripting@Phyre@@` — holds

```
00D6FDB8  0067E690
00D6FDC0  00684D10      <- lua exec, "zero callers"
00D6FDC8  00686280      <- lua exec, "zero callers"
00D6FDD0  005C5230      <- the folded `xor eax,eax; ret` stub
00D6FDD8  005C5230      <- the same stub again
```

The other two executors, `00684F60` and `006852B0`, are called from `00685140`, `006853C0` and
`00685560` — **which are themselves slots of the vtable at `00D6FD68`,
`.?AVPScheduler@PScripting@Phyre@@`.**

> **Lua execution in this build is reached entirely through virtual dispatch**, which is why a
> direct-call census reports two of its four entry points as dead. **And two slots of the
> `PCallerScript` vtable are the same retail stub `005C5230` this database documents under four other
> identities** — see [`../../01-Script-VM-Native-Bridge/verbs-that-only-wait-and-verbs-that-do-nothing.md`](../../01-Script-VM-Native-Bridge/verbs-that-only-wait-and-verbs-that-do-nothing.md).

> **DA-4 answered 2026-09-12 (FABLE): the two stubbed slots are the caller's *return-type
> descriptor* and *parameter-descriptor list* — a script-defined callable is untyped by
> construction, not a removed capability.** The `PCallerScript` vtable at `00D6FDB8` has five slots
> (its RTTI base chain is `PCallerScript` → **`Phyre::PCaller`**): 0 the destructor `0067E690`, 1
> `00684D10` (the chunk compile-and-register path that ends in `luaL_loadbufferx`), 2 `00686280`
> (the execute path that ends in `lua_pcall`), and **3 and 4 = `005C5230`** (`xor eax, eax ; ret`).
> The C++ implementations of the same base, `PMethodCallerConcrete<…>` (vtables `00D34DE8`,
> `00D34D88` — the same slot-0 destructor `0067E690` on the first), fill those slots with real
> bodies: **slot 3 returns a tagged class-descriptor pointer** (`005C5200`: `lea rax, [02CF8470] ;
> or rax, 1 ; ret`; `005C5240` likewise with `02CAD840`) and **slot 4 returns a thread-safe
> function-static descriptor list** (`005C43F0` / `005C3CA0`: `_Init_thread_header` … a tagged
> descriptor pointer, a count from `00630180`, a null, then the static's address). So the `PCaller`
> interface is *destroy / call / call-from-binding / return-type descriptor / parameter
> descriptors*; a caller whose body is a Lua chunk has no C++ types to report, and both queries
> answer null. Nothing was dropped: reflection over a script callable is simply unavailable, and
> any caller of slots 3–4 must already handle a null (the concrete ones never return it).

**No `.lua` file ships.** `lua` is not among the 48 extensions censused over the 89,414-entry
archive index, so whatever these paths execute does not come from the shipped data.

## Does the Lua actually run? — 2026-09-08, three levels, only two of them established

The previous section left this deliberately open: *"Lua is linked and dispatchable is established;
Lua runs is not."* **One of the two gaps is now closed, and the other is closed off as far as static
evidence can take it.**

### Level 1 — linked. Established already.

Lua 5.2.1, **111 functions**, per
[`../../23-Third-Party-Libraries/third-party-middleware-inventory.md`](../../23-Third-Party-Libraries/third-party-middleware-inventory.md).

### Level 2 — **instantiated before `main`, on every launch. New.**

The four Phyre scripting vtables each have a constructor that installs them:

| class | vtable | constructor |
|---|---|---|
| `PScripting::PAsyncProcessBuffer` | `00D6FD50` | `00681560`, `00681720` |
| `PScripting::PScheduler` | `00D6FD68` | `00681560`, `00681880` |
| **`PScripting::PUtilityScripting`** | `00D6FD98` | **`00166210`** |
| `PClassCallableMethodScript::PCallerScript` | `00D6FDB8` | `00682E30` |

**`00166210` is tagged `Runtime.StaticLifetimeInfrastructure`, has no callers, and is entry 516 of
the CRT initializer table** at `0x008C31D8` that
[`../../24-Compiler-And-CRT-Runtime/Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md`](../../24-Compiler-And-CRT-Runtime/Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md)
documents.

> **So a `PUtilityScripting` object is built before `main` runs, unconditionally, every time the game
> starts.** The scripting subsystem is not dormant middleware waiting for a feature that was cut — one
> of its objects exists in every session, before the title screen.
>
> *The table parsed to exactly **1,172** entries, the figure that document states, and the control
> address is absent from it — so the membership test discriminates rather than matching everything.*

### Level 3 — **executes a chunk: not established, and the static evidence is against it**

- **No `.lua` file ships.** `lua` is not among the 48 extensions censused over the 89,414-entry
  archive index.
- **Every route into `lua_pcall` is virtual.** Two of the four executors are `PCallerScript` vtable
  slots; the other two are called from three `PScheduler` vtable slots.
- **`PScheduler` and `PCallerScript` are not static initialisers** — neither constructor appears in
  the 1,172-entry table — and the one function that constructs them, `00680D80`, **is itself a vtable
  slot** (`.rdata:00D6F418`) with no direct callers.

> **The chain from game code to a running Lua chunk is virtual at every link**, so a static caller
> trace cannot reach the end of it. **What can be said is bounded and worth saying: nothing in the
> shipped data is a Lua chunk, and no non-virtual path constructs a scheduler.**
>
> **What would settle it is a breakpoint on `00684D10`, not more static work.** That is the honest
> stopping point — the same shape as the character-controller answer in `AS-1b`, where reflection-driven
> instantiation was noted as invisible to every static test.

**For a modder the practical answer is: the engine registers a scripting module at startup, and there
is no evidence that a Lua state is ever created or that the shipped game hands it a script.**

### ⚠ Correction, same day — what construction actually does (`DA-2`)

**The sentence above first read *"there is a live Lua interpreter in the process"*. That was
overstated, and reading the 86 bytes settles it.**

`00166210` creates **no `lua_State`**. It is a self-registration:

```asm
00166210  cmp  qword [02CACC90], 0        ; the module list head
00166221  mov  rcx, [rax]                 ; walk the list...
00166224  cmp  dword [rcx+0x18], 0xFF     ; ...while this node's priority < 0xFF
00166236  jne  0x166221
0016623B  mov  [01F2EAD0], rcx            ; our `next` = the node we displace
00166249  mov  [rax], rcx                 ; link ourselves in
0016624C  lea  rax, [00D6FD98]            ; the PUtilityScripting vtable
0016625A  mov  [01F2EAC8], rax            ; ...written into a STATIC object
00166261  jmp  atexit                     ; 00808B90, register the destructor
```

**A statically-allocated `PUtilityScripting` at `01F2EAC8` gets its vtable written and is spliced into
a priority-ordered intrusive list headed at `02CACC90`** — a list **33 static initialisers register
into**, 64 references in all. Then `atexit`.

> **That is registration, not interpretation.** What exists before `main` is a scripting *module
> object* taking its place in a subsystem registry alongside thirty-two others. **Whether any
> `lua_State` is ever created remains unestablished**, and `DA-1` is unchanged.
>
> **The overstatement came from stopping at the right conclusion for the wrong reason** — "it is in
> the CRT initializer table" proves an object is constructed, and I let *constructed* become *live
> interpreter* across one sentence. **Entry 516 is still entry 516; it just does less than I said.**

## SWE2-EC7-58 update (2026-09-19) - `00681720`

`00681720` (166 B) is a call-free intrusive-list unlink - `[rax]`-chain walk matching `[rcx+0x18]`, relink of `[rdx+0x18]`/`+0x20` (`PAsyncProcessBuffer` family). Interior anchor `00681760` (the chain-walk load).


## SWE2-EC7-117 update (2026-09-21) - `00685B70` / `006844C0` measured

`00685B70` (145 B) is the
queue extract `00685140`
and `00685560` run: walks
the singly-linked chain at
`[+0x40]`, unlinks each
node whose `dword[+0x28]`
is 1, stamps its `+0x20`
to -1, and hands it to
`00680200(+0x8, node)` -
the completed-work requeue.
Interior anchor `00685BC7`
(the unlink store).

`006844C0` (216 B) is the
`02E41570`/`02E41578`
global-vector push
`00685AC0` calls:
allocates `(count + 1) *
0x10` via `0017D260`
(align 8), copies the old
`0x10` records, appends
the caller's 16-byte
record, frees the old
array through `00584730`
when its bit-31 ownership
is clear, and relatches
the count and base.
Interior anchor `00684576`
(the `00584730` call).

## SWE2-EC7-118 update (2026-09-21) - the `00685AC0` registration block measured

`00681F30` (939 B) is the
script-API registration
`00685AC0` runs on the
`02E41370` interface
(`006388C0` open, TLS slot
`gs:[0x58] + 4` counter):
four identical lock
(`008092FC`), name-register
(`00632FB0`), sentinel-link,
`00808B90` atexit,
`0080929C` unlock rounds
install `"GetCurrent
Scheduler"`, `"GetCurrent
Script"`, `"addScript"` and
`"removeScript"` plus the
`"pAk"` host object
(`00684830` callback,
vtable `02E42530`/
`02E42590` records).
Interior anchor `00681FB5`
(the first `00632FB0`
call).

`00681D80` (417 B) is the
same round on `02E41070`,
registering the three
named fields `"m_script"`
(0x50, flags 2),
`"m_nameAsString"` (0x58)
and `"m_entryPoint"` (0x60)
through `00632960`.
Interior anchor `00681E11`
(the `"m_script"` call).

`00681C50` (289 B) installs
`"getAsyncResult"` on
`02E41270` via `00632FB0`
and links the `00685980`-
callback record
(`02E42470` vtable block)
into the `+0x90` sentinel
list.
Interior anchor `00681CCB`
(the `00632FB0` call).

`006827C0` (299 B)
registers `"m_handler"`
(size 8) on `02E41170`
through `00632960` against
`02E423E0`/`02E4E430`,
atexit `008B2530`, then
tails into `00639450`.
Interior anchor `006828B7`
(the `00632960` call).

## Cross-subsystem neighbours — SWE2-STRUCT (pass-22 dispositions)

- **Resource - CLIENT (231 edges).** `0062FF50`, `0062FFC0`, `00630030`, `006300A0` (+7 more) are called by bodies filed to Resource: `001F4720`, `005850F0`, `00585270`, `005853F0` (+137 more) - shared machinery across the layer boundary, no shared ownership.
