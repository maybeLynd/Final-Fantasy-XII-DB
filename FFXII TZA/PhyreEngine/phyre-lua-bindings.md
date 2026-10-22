---
title: "PhyreEngine Lua bindings: how engine objects are pushed to and taken from Lua, the generated adapters, and what installs them"
kind: "system"
category: "PhyreEngine"
addresses: "0x00682D20, 0x00684080, 0x00684090, 0x00682980, 0x00682A10, 0x006828F0, 0x00599770, 0x00599B70, 0x00812960, 0x02E41000, 0x005A0E80, 0x005A10F0, 0x005A2BA0, 0x00584E10, 0x00584C50, 0x0063F850, 0x00683FF0, 0x006841F0, 0x00682AA0, 0x00684F60, 0x00810ED0, 0x00810470, 0x005A08E0, 0x00685AC0, 0x006822E0, 0x00681F30, 0x006827C0, 0x00681C50, 0x00681D80, 0x0067E6C0"
---

## What the player sees

Nothing. The executable carries the glue that lets PhyreEngine hand its objects (cameras, nodes,
animation clips, world matrices) to Lua scripts and take them back, but the shipped game never runs a
Lua script, so none of this code does anything during play.

## How it works

### The object userdata

`0x00682D20(L, object, descriptor)` pushes an engine object: it calls `lua_checkstack(L, 1)`
(`0x0080F420`), allocates a 16-byte userdata (`0x00810240`), stores the class descriptor and the object
pointer in it, fetches `registry["PhyreObject"]` (`0x0080FA50` with index `-1001000`) and sets that as the
userdata's metatable (`0x00810F60`). The metatable is only an identity tag: no code outside the
interpreter stores anything in it.

Two more value kinds use the same scheme with their own registry keys: `"Vector"` (16-byte
userdata, pushed by `0x00684280`, `0x00684300`, `0x00684360`, `0x006843D0`, `0x00684450`) and `"Matrix"`
(`0x40` bytes, `0x00684130`).

### Recognising a script value

`0x00682980(L, index)` is `luaL_testudata` against `"PhyreObject"`: `lua_touserdata`, `lua_getmetatable`,
fetch the registry entry, `lua_rawequal`, pop both, and return the userdata only when the metatables
are the same table. `0x00682A10` and `0x006828F0` do the same for `"Vector"` and `"Matrix"`.

### Object accessors

Each `PObjectAccessor<T>::Get` reads the value on top of the stack with `0x00682980`, pops it, and walks
the userdata's descriptor through the base links at descriptor `+0x78` until it reaches `T`'s
descriptor, so a derived object is accepted where a base is wanted. They come in two forms:

- Reference (`T &`), e.g. `0x00599770` for `PClusterHeader`: a non-Phyre value, or a Phyre object of
  another class, raises a Lua error.
- Pointer (`T *`), e.g. `0x00599B70`: `nil` yields a null pointer; another Lua type raises
  `"Unable to obtain object pointer from script - found another type of data instead (Lua type %d)"`.

Before raising, an accessor writes its source file, line and own name into the record at `0x02E41000`;
the error itself goes through `luaL_error` (`0x00812960`: `luaL_where`, `lua_pushvfstring`,
`lua_concat`, `lua_error`).

### The binding slots of a class descriptor

Every reflected class has a descriptor whose vtable carries its script bindings. In the
`PClusterHeader` descriptor vtable `0x00D249A8` and the `PAnimationChannelTarget` vtable `0x00D28030`:

```python
slot 3  +0x18  get a value from the script      0x00584E10 (copies the 84-byte header out)
slot 4  +0x20  push a value  # 0x00584D30, 0x005A0E80
slot 5  +0x28  get a pointer from the script  # 0x00584C50
slot 6  +0x30  push a pointer, nil when null  # 0x00584C70, 0x005A5980
```

An abstract class's slot 3 is `0x0063F850`, which only logs that the operation is not supported. The
push adapters are one-line tail calls into `0x00682D20` through the jump thunk `0x00684080` (or
`0x00684090`) with the class's descriptor; a class pushed as a base adds the base's offset first
(`0x005A10F0` adds 8). The nullable form tests the pointer and pushes `nil` (`0x00810620`) instead
(`0x005A2BA0`).

For `PInputMapper` (descriptor vtable `0x01CB1178`) slot 3 is `0x007919D0`: it takes the mapper from the
script with its reference accessor `0x00796860` and copies it into the out-value with `0x007939A0`, which
copies the `0x2C8`-byte object member by member and the `0x88`-byte block at `+0x230` through
`0x00793DA0`; that one skips the dwords at `+0x10`, `+0x20`, `+0x30` and `+0x40` of the block.

### Method-call adapters

Each method registered with `0x00632FB0` gets a `PMethodCallerConcrete` caller object holding the member
function at `+8`. Slot 1 of its vtable is the Lua adapter: it pops the arguments (accessors, or the
number readers `0x00811640` and `0x00811470`), takes `this` through an accessor, calls the member
function, pushes the result (an object, `nil`, a number through `0x00810580`, or a `"Vector"`) and
returns 1. `0x006B2400` takes a float; `0x005C1E70` returns a nullable object.

Slot 2 is the native call (`0x005CC300`, `0x005CC3E0`): it calls the member function and, when the
caller asks for the result with the matching type tag, writes `{0, result}` to the out-record and
returns 1. In the `PAnimationClip` caller vtable `0x00D34C38` the two slots are `0x005C1E70` and
`0x005CC3E0`.

A script caller's slot 2, `0x00686280`, runs the script and converts its result the same way. For a
`float` result type (`0x01F2E690`) `0x006810B0` reads the top of the Lua stack as a number (`0x00811640`),
pops it (`0x00811130` with -2) and writes `{0, value}`; `0x00681130` does the same for `double`
(`0x01F2E6E0`), widening the value. Each returns false for any other result type.

### Arrays and copies

`0x00683FF0` pushes an array as a new table (`0x0080F740`), storing element *i* at key *i* with the element
descriptor's slot 4 and `lua_settable` (`0x00811090`); `0x006841F0` does the same for pointer elements
through slot 6. `0x00682AA0` copies values between two Lua states: nil, booleans, light userdata,
numbers and strings directly, and `PhyreObject`, `"Vector"` and `"Matrix"` userdata by re-pushing
them; other types are logged as unsupported.

### Registration at start-up

The engine start-up `0x005A08E0` calls `0x0067E6C0` (the `PWorldMatrix` methods `getMatrix`,
`setMatrix`, `setMatrix4x3`, `lookAtWorldMatrix` and member `m_matrix`) and slot 1 of every module in
its list. For the scripting module this is `0x00685AC0` (slot 1 of `PUtilityScripting`, vtable
`0x00D6FD98`), which calls:

- `0x006822E0`: the `PScript` members (see Layouts);
- `0x00681F30`: `PScheduler` methods `GetCurrentScheduler`, `GetCurrentScript`, `addScript`,
  `removeScript`;
- `0x006827C0`: `PScriptCallbackHandler` members `m_entryPoint` and `m_handler`;
- `0x00681C50`: the `PAsyncProcessHeader` method `getAsyncResult`;
- `0x00681D80`: `PClassCallableMethodScript` members `m_script`, `m_nameAsString`, `m_entryPoint`.

All of these write the engine's reflection tables through `0x00632960`, `0x00632A10` and `0x00632FB0`;
none calls the Lua interpreter. `0x00685AC0` then appends four library openers to a list nothing reads.

### What installs the bindings in Lua

Nothing does. Of the interpreter's functions, code outside it calls 32, and none puts an engine
function or table where a script can reach it:

- `lua_pushcclosure` (`0x00810470`) is called only inside the interpreter, by its own library openers,
  so no binding is ever pushed as a Lua function.
- The only global written from outside is `phyre_pscript`, a light userdata naming the running
  `PScript`, set by `lua_setglobal` (`0x00810ED0`) in the executor `0x00684F60`.
- `lua_settable` is used only on tables the array pushers have just created, and `lua_setmetatable`
  only on userdata just pushed.

The bindings therefore run only when engine code that already holds a `lua_State` calls them, as
`0x00684F60` does when it pushes an object as the argument of a script's entry point. The game never
creates a state (see the Lua runtime page), so they never run.

`0x006852B0(record, n)` is the other caller of that shape, the "execute" of a script record (called from
`0x00685140`, `0x006853C0` and `0x00685560`):

1. It returns 7 when the record has no script (`+0x08`) and 1 when it has no `lua_State` (`+0x30`).
2. It fetches the global named by entry `n` of the script's name list at `+0x28` (`lua_getglobal`, `0x0080FB20`)
   and pushes the record's object (`0x00682D20`, object `+0x10`, descriptor `+0x18`).
3. It calls the global with that one argument and no results: `lua_pcallk(L, 1, 0, 0, 0, NULL)` (`0x00810340`).
4. A failure is logged through `0x005CDAA0` as `"execute: lua_pcall failed - error code: %d\n%s (%s)"` with
   the message and the script's name, and the message is popped.
5. It runs a full collection (`lua_gc(L, LUA_GCCOLLECT, 0)`, `0x0080F800`) and returns 0.

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | descriptor | class descriptor of the object |
| `+0x08` | `void*` | object | the engine object |

The `PObjectAccessor` failure record at `0x02E41000`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | file | source path of the accessor template |
| `+0x08` | `u32` | line | `0x6A` / `0x76` pointer form, `0x8D` / `0x8F` reference form |
| `+0x10` | `void*` | function | the accessor's own name |

The `PScript` members `0x006822E0` registers; `0x00680F40` clears them and sets `m_executionInterval`
to 1:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `PArray` | m_scriptChunk32 | PArray&lt;PUInt8&gt; |
| `+0x10` | `PArray` | m_scriptChunk64 | PArray&lt;PUInt8&gt;; the loader reads +`0x10` count, +`0x18` data |
| `+0x20` | `PArray` | m_functionNames | PArray&lt;PString&gt;; entry points by index |
| `+0x30` | `void*` | m_onLoadEntryPoint |  |
| `+0x38` | `void*` | m_onUnloadEntryPoint |  |
| `+0x40` | `void*` | m_defaultEntryPoint |  |
| `+0x48` | `void*` | m_sourceName |  |
| `+0x50` | `u8` | m_isPersistent |  |
| `+0x54` | `u32` | m_executionInterval |  |

## Shipped data

Measured from the executable (SHA-256 `73461d08…d89721f8`).

| Fact | Value |
|---|---|
| `PObjectAccessor<…>::Get` names | 747: 402 pointer, 345 reference, over 412 bound types |
| callers of `0x00682980` | 750 functions |
| calls into the push routine | 834 through `0x00684080`, 16 through `0x00684090`, 6 direct (`0x00681066`, `0x006811DD` jmp, `0x00682C88`, `0x00684B22`, `0x006850A7`, `0x0068530B`) |
| `luaL_error` call sites | 1,568 in 803 functions |
| interpreter functions used from outside | 32 called, plus 4 library openers whose addresses `0x00685AC0` takes |
| `lua_pushcclosure` callers outside the interpreter | 0 |
| globals set from outside | 1, `phyre_pscript` |

## State

- `0x02E41000`: the most recent accessor failure, overwritten by each.
- The registry keys `"PhyreObject"`, `"Vector"` and `"Matrix"`: read, never written, by the binding
  layer.

## Modding notes

- Running Lua against the engine needs a `lua_State` built outside the executable, with tables stored
  under the three registry keys; without them every push sets a `nil` metatable and every accessor
  rejects what it is given.
- No engine method is callable from Lua as shipped: a host must push its own C functions that call the
  method-call adapters.
- Hand a push adapter the object's own pointer: an adapter that pushes the object as one of its bases
  adds the base's offset itself, and adding it first pushes a wrong address.

## Related

- [Lua runtime](../Third-Party-Libraries/lua-runtime.md): the interpreter, its chunk loader and why
  no script runs.
- [Script interpreter](../Scripts-And-Script-Commands/script-interpreter.md): the game's own script
  machine.
- The adapter families, beside this page:
  - `phyre-lua-bindings-object-push-adapters.tsv` (slot 4, static descriptor, 304);
  - `phyre-lua-bindings-nullable-object-push-adapters.tsv` (slot 6, 295);
  - `phyre-lua-bindings-object-pointer-accessors.tsv` (323) and
    `phyre-lua-bindings-object-reference-accessors.tsv` (264);
  - `phyre-lua-bindings-context-acquire-three-arg-dispatch-adapters.tsv` and
    `phyre-lua-bindings-optional-pointer-context-dispatch-adapters.tsv` (70 each; descriptor from a
    getter);
  - push variants: `phyre-lua-bindings-optptr-static-descriptor-dispatch-adapters.tsv`,
    `-optptr-offsetadd-dispatch-adapters.tsv`, `-optptr-membercall-forward-adapters.tsv`,
    `-optptr-membercall-resultdispatch-adapters.tsv`, `-optptr-membercall-dispatch-adapters.tsv`,
    `-nativeadapter-descriptorforwardtailcall.tsv`, `-nativeadapter-optptrallocrecordinstall.tsv`;
  - slot 1 method adapters: `phyre-lua-bindings-member-vcall-optptr-dispatch-adapters.tsv`,
    `-optptr-membercall-vcall-dispatch.tsv`, `-nativeadapter-floatpipelinevcalladapter.tsv`,
    `-nativeadapter-optptrfloatpipelinelookup.tsv`, `-nativeadapter-optptrmembercallclonedforward.tsv`,
    `-nativeadapter-optptrmembercallvcallforward.tsv`, `-nativeadapter-optptrmembercallvcallresult.tsv`,
    `-nativeadapter-optptrmemberoffsetvcall.tsv`;
  - slot 2 native calls: `phyre-lua-bindings-tagged-outrecord-vcall-adapters.tsv`,
    `-tagged-outrecord-vcall-advance-adapters.tsv`, `-nativeleaf-taggedoutrecordvptrstore.tsv`;
  - `phyre-lua-bindings-pscript-accesses.tsv` (the `PScript` field stores of `0x00680F40`).
