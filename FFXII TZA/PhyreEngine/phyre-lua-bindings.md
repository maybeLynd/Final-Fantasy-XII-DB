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

The two stores (`0x00682D59`, `0x00682D5C`) sit behind a null test of the userdata (`0x00682D57`) that never skips them:
`0x00810240` returns the new object's address plus `0x30` (`0x00810286`). The metatable call is a tail jump with index
-2 (`0x00682D74`-`0x00682D8B`), so the pushed userdata stays on top of the stack.

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
- `0x00599770` pops the value before any test (`0x00599790`) and returns the object pointer at userdata `+0x08` when
  the walk reaches the `PClusterHeader` descriptor `0x02CAA0A0` (`0x005997B0`, `0x0059985B`).
- For a non-Phyre value it first calls `0x0063BC00` with `0x02CAA0A0` (`0x00599817`) and keeps the result as its return
  value, which the error never lets it reach.
- A Phyre userdata whose descriptor word is null skips that call (`0x005997A4`). Both raise at line `0x8D`, with
  the class name at descriptor `+0x30` (`0x0059981F`-`0x00599856`), and the message
  `"Object obtained from script was not a Phyre Object when an object of type "%s" was required."`
- A Phyre object of another class raises at line `0x8F` with the two class names (`0x005997C2`-`0x005997FD`):
  `"Object obtained from script was of type "%s" when an object of type "%s" was required."`
- Pointer (`T *`), e.g. `0x00599B70`: `nil` yields a null pointer; another Lua type raises
  `"Unable to obtain object pointer from script - found another type of data instead (Lua type %d)"`.
- `0x00599B70` pops a `nil` before returning null (`0x00599C3E`) and raises for another non-Phyre value, at line
  `0x76`, with that value still on the stack (`0x00599C50`-`0x00599C8B`). It pops a Phyre value (`0x00599B99`); a null
  descriptor word returns the object pointer unchecked (`0x00599BAD`, `0x00599C1B`), and the walk returns it on a
  match (`0x00599BC3`).
- A Phyre userdata holding a null object pointer (`0x00599BA8`) goes to the same type test, applied to the value
  now on top: a `nil` there is popped too and null returned, and any other type raises the line-`0x76` error.
- A Phyre object of another class raises at line `0x6A` with the two class names (`0x00599BCE`-`0x00599C09`):
  `"Object pointer obtained from script was of type "%s" when an object of type "%s" was required."`

Before raising, an accessor writes its source file, line and own name into the record at `0x02E41000`;
the error itself goes through `luaL_error` (`0x00812960`: `luaL_where`, `lua_pushvfstring`,
`lua_concat`, `lua_error`).

`luaL_error` does not return. `lua_error` (`0x0080F7F0`) calls `0x0081D2B0`, which ends in `0x0081E2C0` (`0x0081D341`):
that one jumps back to the protected call (`0x00861EE4`) or, outside one, runs the panic function and calls `abort`
(`0x0081E340`, `0x0081E342`). An accessor's code after the call therefore never runs.

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

`0x005A2BA0` reads the pointer from the address in `r8` (`0x005A2BA9`). For null it calls `lua_checkstack(L, 1)`
(`0x005A2BCE`) and tail-jumps to the `nil` push (`0x005A2BDB`); otherwise it adds 8 (`0x005A2BB4`) and tail-jumps to
`0x00684080` with the descriptor `0x02CAF0E0` (`0x005A2BB8`-`0x005A2BC4`).

`0x00584E10`, slot 3 of `PClusterHeader`, takes the header from the script with the reference accessor `0x00599770`,
passing it `L` from its second argument (`0x00584E16`, `0x00584E1C`). It copies the 84 bytes the accessor returns to
the out-value in `r8`: five 16-byte moves and the dword at `+0x50` (`0x00584E21`-`0x00584E4A`).

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
through slot 6.

Both take `(L, count, data, descriptor)` and create the table with `count` array slots (`0x0068400B`, `0x00684213`).
For each element they push the key *i*, from 1, as a number (`0x00810580`), call the slot with the descriptor, `L`
and the element's address, and store with `lua_settable(L, -3)` (`0x00684030`-`0x00684052`, `0x00684230`-`0x00684252`).
`0x00683FF0` steps by the dword at descriptor `+0x38` (`0x00684023`, `0x0068405A`), `0x006841F0` by 8 (`0x0068425A`). A count
of 0 leaves the table empty (`0x00684012`, `0x0068421A`), and the table stays on top of the stack.

`0x00682AA0` copies values between two Lua states: nil, booleans, light userdata,
numbers and strings directly, and `PhyreObject`, `"Vector"` and `"Matrix"` userdata by re-pushing
them; other types are logged as unsupported.

`0x00682AA0(from, to, first, count)` returns 1 when either state is null (`0x00682CE1`) and 5 when they are the same
state or `first` is 0 (`0x00682ACF`). It returns 9 when `lua_checkstack(to, count)` fails (`0x00682AEB`-`0x00682AF4`),
and otherwise 0 after copying `count` values from index `first` upward (`0x00682CB7`-`0x00682CD2`). Each value goes by
its `lua_type` (`0x00682B35`) through the nine-entry table at `0x00682CF4`:

- nil, booleans, light userdata and numbers are pushed with `0x00810620`, `0x00810450`, `0x008105A0` and `0x00810640`;
- a string is read with `0x00811530`, pushed with `0x00810660`, and then one value is popped from the source state
  (`0x00682BAD`);
- tables, functions and threads push nothing and log
  `"Unsupported type being copied between script contexts: '%s'"` with the type name (`0x00811A70`, `0x00682BD8`);
- userdata is tested as `"Vector"` (`0x00682A10`), then `"Matrix"` (`0x006828F0`), then `"PhyreObject"` inline, and
  re-pushed by `0x00684450`, `0x00684130` or `0x00682D20` (`0x00682C88`);
- a userdata that is not one of the three pushes nothing and logs
  `"Unsupported user data being copied between script contexts"` (`0x00682C9B`);
- an index past the top, whose type is -1 (`0x00811A0B`), is skipped with nothing logged (`0x00682B3D`).

### Registration at start-up

The engine start-up `0x005A08E0` calls `0x0067E6C0` (the `PWorldMatrix` methods `getMatrix`,
`setMatrix`, `setMatrix4x3`, `lookAtWorldMatrix` and member `m_matrix`) and slot 1 of every module in
its list, stopping at the first that returns non-zero (`0x005A0964`, `0x005A0A39`-`0x005A0A3E`). For the scripting
module this is `0x00685AC0` (slot 1 of `PUtilityScripting`, vtable `0x00D6FD98`), which calls, in this order and
ignoring their results (`0x00685AC4`-`0x00685AD8`):

- `0x006822E0`: the `PScript` members (see Layouts);
- `0x00681F30`: `PScheduler` methods `GetCurrentScheduler`, `GetCurrentScript`, `addScript`,
  `removeScript`;
- `0x006827C0`: `PScriptCallbackHandler` members `m_entryPoint` and `m_handler`;
- `0x00681C50`: the `PAsyncProcessHeader` method `getAsyncResult`;
- `0x00681D80`: `PClassCallableMethodScript` members `m_script`, `m_nameAsString`, `m_entryPoint`.

`0x006827C0`, `0x00681C50` and `0x00681D80` each pass their class descriptor (`0x02E41170`, `0x02E41270`, `0x02E41070`) to
`0x006388C0` first (`0x006827DB`, `0x00681C6B`, `0x00681D9B`). Each ends with a tail jump to `0x00639450` with it (`0x006828E6`,
`0x00681D6C`, `0x00681F1C`), which sets bit `0x40000000` of descriptor `+0xFC` (`0x00639465`). Each registration in
between runs once, inside its own thread-safe static guard (`0x008092FC`, `0x0080929C`), and passes its record's
teardown to `atexit` (`0x00808B90`).

The members go through `0x00632960`. For `PScriptCallbackHandler` they are `m_entryPoint` at `+0x00` (`0x00682849`)
and `m_handler` at `+0x08` (`0x006828B7`). For `PClassCallableMethodScript` they are `m_script` at `+0x50`, whose
sixth argument is 2 (`0x00681DE5`, `0x00681E11`) where the other members give 0, `m_nameAsString` at `+0x58`
(`0x00681E7F`) and `m_entryPoint` at `+0x60` (`0x00681EED`).

`0x00681C50` registers `getAsyncResult` once, inside its guard (`0x02E42490`). `0x00632FB0` fills the method record
`0x02E42440` (`0x00681CCB`), the record's `+0x28` is cleared (`0x00681CD0`), and the record is linked into the method
list at `+0x90` of the descriptor at record `+0x10` unless `0x005A7A40` finds a method of that name there
(`0x00681CF5`-`0x00681D14`). On every call it then builds the caller object at `0x02E42470`: vtable `0x00D70200`, the
member function `0x00685980` at `+0x08`, and its address in record `+0x28` (`0x00681D31`-`0x00681D54`).

All of these write the engine's reflection tables through `0x00632960`, `0x00632A10` and `0x00632FB0`;
no registrar calls the Lua interpreter. `0x00685AC0` then appends four library openers, `math` `0x00819410`, `bit32`
`0x00818A40`, `string` `0x00817550` and `coroutine` `0x00815500`, with their names to the list at `0x02E41578` through
`0x006844C0` (`0x00685ADD`-`0x00685B24`). It returns 0 (`0x00685B29`), also when `0x006844C0` returns 13 because its
allocation failed (`0x006844F2`).

Only `0x006844C0` reads the list's entries, copying the earlier pairs into each new buffer (`0x0068452C`-`0x00684533`);
the other two users, `0x00685F60` and `0x008B25C0`, free it. No code calls an opener from the list.

### What installs the bindings in Lua

Nothing does. Of the interpreter's functions, code outside it calls 32, and no call puts an engine
function or table where a script can reach it:

- `lua_pushcclosure` (`0x00810470`) is called only inside the interpreter, at 9 sites, so no binding is ever
  pushed as a Lua function. No data word holds its address.
- Its callers are `luaL_setfuncs` (`0x0081363A`), the base library's `pairs` and `ipairs` (`0x0081498C`,
  `0x00814A1C`), `coroutine.wrap` (`0x008151A4`), `string.gmatch` (`0x00815F8B`) and the `io` library's line iterator
  (`0x00825FB4`).
- The package library calls it for its searchers table (`0x008288D9`), in its opener (`0x00828D6E`) and in its
  C-library loader, which pushes a function found with `GetProcAddress` (`0x00828C4C`).
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

The executor `0x00684F60(record, L, n)` takes the state as an argument and runs the chunk before the entry point:

1. It returns 7 when the record has no script (`+0x08`, `0x00684F82`) and 1 when `L` is null (`0x00684F9B`).
2. It loads the chunk with `0x00683C30(L, script)` (`0x00684FBC`) and returns 9 when that fails (`0x00684FC3`).
3. It pushes the script as a light userdata and stores it in the global `phyre_pscript` (`0x00684FD5`, `0x00684FE4`).
   It then runs the chunk with no arguments and no results, `lua_pcallk(L, 0, 0, 0, 0, NULL)` (`0x00684FFF`).
4. A failure is logged through `0x005CDAA0` with first argument 3, as
   `"execute: lua_pcall failed - error code: %d\n%s (%s)"` with the message and the script's `m_sourceName`, bit
   `0x1` cleared (`0x00685022`-`0x0068503F`). The message is popped and 0 returned.
5. When the dword at record `+0x20` is negative it logs `"execute: no valid script entryPoint set (%s)"` with the
   source name and returns 0 (`0x00685054`-`0x00685078`).
6. Otherwise it fetches the global named by entry `n` of the script's name list at `+0x28`, bit `0x1` cleared
   (`0x0068507D`-`0x00685097`). It pushes the record's object (`0x00682D20`, object `+0x10`, descriptor `+0x18`,
   `0x006850A7`) and calls the global with that one argument and no results (`0x006850C2`).
7. It reads the top of the stack as a string (`0x006850D2`). A failure logs
   `"execute: lua_pcall failed - error code: %d\n%s"` with first argument 3 and pops the message
   (`0x006850DB`-`0x006850FA`).
8. After a success, a string or number on top is logged with `"%s\n"` and first argument 2 (`0x00685101`-`0x00685115`).
   It returns 0.

## Layouts

### Reflected members

The members below are the ones the code of this page's classes uses or the reflection registers; each registered member is named by its registration (the registering function, through 0x00632960), and each class fence covers only those members.

`PClassCallableMethodScript` (`0x68` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[80]` | methodRecord | the method record the class shares with the methods `0x00632FB0` registers: list links at `+0x00` and `+0x08` (`0x00682E75`, `0x00682EED`), the class descriptor at `+0x10` (`0x00682E88`), the name at `+0x18` (`0x00682E8F`), and at `+0x28` a pointer to the invoker at `+0x30`, whose vtable `0x00D6FDB8` and back-pointer `0x00682E30` stores (`0x00682F04`-`0x00682F10`); no registered member covers it (`0x006812B0` registers the `0x68`-byte class at `0x006812FA`) |
| `+0x58` | `void*` | m_nameAsString | the method's name: `0x00682E30` (entered through `0x00680510`) walks a loaded instance list of the class (count `+0x70`, objects `+0x58` of the list), copies this name with bit `0x1` cleared into the record's name at `+0x18` (`0x00682E7C`-`0x00682E8F`) and links the record into the method list at `+0x90` of the class descriptor at its `+0x10` unless a method of that name is already there (`0x00682E93`-`0x00682EF7`); m_nameAsString (ptr), registered by `0x00681D80` (`0x00632960` at `0x00681E7F`); no shipped .phyre file declares PClassCallableMethodScript |
| `+0x60` | `void*` | m_entryPoint | m_entryPoint (ptr), registered by `0x00681D80` (`0x00632960` at `0x00681EED`); no shipped .phyre file declares PClassCallableMethodScript |

`PScript` (`0x58` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x30` | `void*` | m_onLoadEntryPoint | m_onLoadEntryPoint (ptr), registered by `0x006822E0` (`0x00632960` at `0x00682540`); no shipped .phyre file declares PScript; cleared by the placement constructor `0x00680F40` (`0x00680F5B`) |
| `+0x38` | `void*` | m_onUnloadEntryPoint | m_onUnloadEntryPoint (ptr), registered by `0x006822E0` (`0x00632960` at `0x006825B2`); no shipped .phyre file declares PScript; cleared by the placement constructor `0x00680F40` (`0x00680F5F`) |
| `+0x40` | `void*` | m_defaultEntryPoint | m_defaultEntryPoint (ptr), registered by `0x006822E0` (`0x00632960` at `0x00682624`); no shipped .phyre file declares PScript; cleared by the placement constructor `0x00680F40` (`0x00680F63`) |
| `+0x48` | `void*` | m_sourceName | the script's source name; low bit is a flag and is cleared when `0x00683C30` reads it (`0x00683C36`-`0x00683C3D`); m_sourceName (ptr), registered by `0x006822E0` (`0x00632960` at `0x00682696`); no shipped .phyre file declares PScript; cleared by the placement constructor `0x00680F40` (`0x00680F67`) |
| `+0x50` | `u8` | m_isPersistent | m_isPersistent (u8), registered by `0x006822E0` (`0x00632960` at `0x00682709`); no shipped .phyre file declares PScript; cleared by the placement constructor `0x00680F40` (`0x00680F6B`) |
| `+0x51` | `u8[3]` | pad51 | alignment bytes after m_isPersistent (u8 at `+0x50`) up to m_executionInterval (`+0x54`; 1 from the placement constructor `0x00680F40`, `0x00680F6E`); no registered member covers it (`0x00681400` registers the `0x58`-byte class at `0x00681450`) |

`PScriptCallbackHandler` (`0x18` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | m_entryPoint | m_entryPoint (ptr), registered by `0x006827C0` (`0x00632960` at `0x00682849`); no shipped .phyre file declares PScriptCallbackHandler |

`PScheduler` (`0x2F8` bytes, offsets from the start of the record):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x99` | `u8[7]` | bytes99 | the bytes between the byte at `+0x98` and the handle at `+0xA0` of the handle wrapper at `+0x98`: the scheduler's slot 3 `0x00685DB0` passes `+0x98` to `0x005CD6D0` (`0x00685E82`-`0x00685E8C`), which clears the byte (`0x005CD6DE`) and closes the handle with CloseHandle (`0x005CD6E1`-`0x005CD6E5`); no registered member covers it (`0x00681350` registers the `0x2F8`-byte class at `0x006813A0`) |
| `+0xA8` | `u8[1]` | byteA8 | the flag of the handle wrapper at `+0x98`: `0x005CD6D0` clears it after closing the handle (`0x005CD6EB`), reached from the scheduler's slot 3 `0x00685DB0` (`0x00685E8C`); no registered member covers it (`0x00681350` registers the `0x2F8`-byte class at `0x006813A0`) |
| `+0xA9` | `u8[591]` | tailA9 | the rest of the scheduler up to its `0x2F8`-byte end: slot 3 `0x00685DB0` waits with Sleep(1) until the pointers at `+0xD8` and `+0xE0` agree (`0x00685EA0`-`0x00685EE7`), then clears `+0xD8`, `+0xE0`, `+0xC0`, `+0xC8` and the dword at `+0xD0` (`0x00685EE9`-`0x00685EF9`); no registered member covers it (`0x00681350` registers the `0x2F8`-byte class at `0x006813A0`) |

### Binding records

The structures below are the ones the mechanisms above use.

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `void*` | descriptor | class descriptor of the object |
| `+0x08` | `void*` | object | the engine object |

The `PObjectAccessor` failure record at `0x02E41000`, with the line at `0x02E41008` and the function at
`0x02E41010` (747 accessors store all three, for example `0x005997D0`, `0x005997E5` and `0x005997EF`):

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
| `+0x10` | `PArray` | m_scriptChunk64 | PArray&lt;PUInt8&gt;; the loader reads `+0x10` count, `+0x18` data |
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
- `0x02E41058`: the script record being run. The `PScheduler` slots `0x00685140`, `0x006853C0` and `0x00685560` store the
  record before each call of `0x006852B0` or `0x00684F60` and 0 after it; `0x00683AF0` returns its script `+0x08`, or 0
  when no record is set, and `0x00681F30` takes that function's address (`0x006820EF`).
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
  - [`phyre-lua-bindings-object-push-adapters.tsv`](phyre-lua-bindings-object-push-adapters.tsv) (slot 4, static descriptor, 304);
  - [`phyre-lua-bindings-nullable-object-push-adapters.tsv`](phyre-lua-bindings-nullable-object-push-adapters.tsv) (slot 6, 295);
  - [`phyre-lua-bindings-object-pointer-accessors.tsv`](phyre-lua-bindings-object-pointer-accessors.tsv) (323) and
    [`phyre-lua-bindings-object-reference-accessors.tsv`](phyre-lua-bindings-object-reference-accessors.tsv) (264);
  - [`phyre-lua-bindings-context-acquire-three-arg-dispatch-adapters.tsv`](phyre-lua-bindings-context-acquire-three-arg-dispatch-adapters.tsv) and
    [`phyre-lua-bindings-optional-pointer-context-dispatch-adapters.tsv`](phyre-lua-bindings-optional-pointer-context-dispatch-adapters.tsv) (70 each; descriptor from a
    getter);
  - push variants:
    - [`phyre-lua-bindings-optptr-static-descriptor-dispatch-adapters.tsv`](phyre-lua-bindings-optptr-static-descriptor-dispatch-adapters.tsv);
    - [`phyre-lua-bindings-optptr-offsetadd-dispatch-adapters.tsv`](phyre-lua-bindings-optptr-offsetadd-dispatch-adapters.tsv);
    - [`phyre-lua-bindings-optptr-membercall-forward-adapters.tsv`](phyre-lua-bindings-optptr-membercall-forward-adapters.tsv);
    - [`phyre-lua-bindings-optptr-membercall-resultdispatch-adapters.tsv`](phyre-lua-bindings-optptr-membercall-resultdispatch-adapters.tsv);
    - [`phyre-lua-bindings-optptr-membercall-dispatch-adapters.tsv`](phyre-lua-bindings-optptr-membercall-dispatch-adapters.tsv);
    - [`phyre-lua-bindings-nativeadapter-descriptorforwardtailcall.tsv`](phyre-lua-bindings-nativeadapter-descriptorforwardtailcall.tsv);
    - [`phyre-lua-bindings-nativeadapter-optptrallocrecordinstall.tsv`](phyre-lua-bindings-nativeadapter-optptrallocrecordinstall.tsv);
  - slot 1 method adapters:
    - [`phyre-lua-bindings-member-vcall-optptr-dispatch-adapters.tsv`](phyre-lua-bindings-member-vcall-optptr-dispatch-adapters.tsv);
    - [`phyre-lua-bindings-optptr-membercall-vcall-dispatch.tsv`](phyre-lua-bindings-optptr-membercall-vcall-dispatch.tsv);
    - [`phyre-lua-bindings-nativeadapter-floatpipelinevcalladapter.tsv`](phyre-lua-bindings-nativeadapter-floatpipelinevcalladapter.tsv);
    - [`phyre-lua-bindings-nativeadapter-optptrfloatpipelinelookup.tsv`](phyre-lua-bindings-nativeadapter-optptrfloatpipelinelookup.tsv);
    - [`phyre-lua-bindings-nativeadapter-optptrmembercallclonedforward.tsv`](phyre-lua-bindings-nativeadapter-optptrmembercallclonedforward.tsv);
    - [`phyre-lua-bindings-nativeadapter-optptrmembercallvcallforward.tsv`](phyre-lua-bindings-nativeadapter-optptrmembercallvcallforward.tsv);
    - [`phyre-lua-bindings-nativeadapter-optptrmembercallvcallresult.tsv`](phyre-lua-bindings-nativeadapter-optptrmembercallvcallresult.tsv);
    - [`phyre-lua-bindings-nativeadapter-optptrmemberoffsetvcall.tsv`](phyre-lua-bindings-nativeadapter-optptrmemberoffsetvcall.tsv);
  - slot 2 native calls: [`phyre-lua-bindings-tagged-outrecord-vcall-adapters.tsv`](phyre-lua-bindings-tagged-outrecord-vcall-adapters.tsv),
    [`phyre-lua-bindings-tagged-outrecord-vcall-advance-adapters.tsv`](phyre-lua-bindings-tagged-outrecord-vcall-advance-adapters.tsv), [`phyre-lua-bindings-nativeleaf-taggedoutrecordvptrstore.tsv`](phyre-lua-bindings-nativeleaf-taggedoutrecordvptrstore.tsv);
  - [`phyre-lua-bindings-pscript-accesses.tsv`](phyre-lua-bindings-pscript-accesses.tsv) (the `PScript` field stores of `0x00680F40`).

### Columns of the six adapter and accessor lists

`phyre-lua-bindings-object-push-adapters.tsv`, `phyre-lua-bindings-nullable-object-push-adapters.tsv`,
`phyre-lua-bindings-object-pointer-accessors.tsv`, `phyre-lua-bindings-object-reference-accessors.tsv`,
`phyre-lua-bindings-context-acquire-three-arg-dispatch-adapters.tsv` and
`phyre-lua-bindings-optional-pointer-context-dispatch-adapters.tsv` have one column, `entry`: the entry address of
one body, one row per body in address order. Every body of a list has the form below.

| List | Rows | Each body |
|---|---:|---|
| object push adapters | 304 | ends with a jump to `0x00684080`: 188 bodies of 21 bytes pass the object as it is; 116 of 31 bytes add a base offset (8 in 111, 1 in 3, `0x30` and `0x10` in one each) and pass null for a null object |
| nullable object push adapters | 295 | 60 bytes (184), 64 (108) or 63 (3): for a null object it calls `lua_checkstack` (`0x0080F420`) and jumps to the `nil` push `0x00810620`, otherwise it jumps to `0x00684080` |
| object pointer accessors | 323 | 301 bytes (203) or 302 (120): calls `0x00682980` once and `0x00811130`, `0x008119F0` and `luaL_error` (`0x00812960`) twice each |
| object reference accessors | 264 | 249 bytes (160) or 282 (104): calls `0x00682980`, `0x00811130` and `0x0063BC00` once each and `luaL_error` (`0x00812960`) twice |
| context-acquire three-argument dispatch adapters | 70 | 47 bytes: calls a getter of its own with `rcx` 0 (70 different getters) and jumps to `0x00684080` with the getter's result in `r8` |
| optional-pointer context dispatch adapters | 70 | 80 bytes: the same getter call (70 different getters); for a null object it calls `0x0080F420` and jumps to `0x00810620` instead |

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Audio: `0x005CD6D0` is called by `0x002118E0`, `0x00211AC0`, `0x00219610`, `0x0021AC00`, `0x0021EEA0`, `0x00220B80`; those
  functions are documented on [audio manager](../Sound-And-Music/audio-manager.md).
