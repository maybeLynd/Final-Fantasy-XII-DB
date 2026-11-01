---
title: "Lazy statics and one-time initialisation: thread-safe local statics, their guards, the shared lock and the release on exceptions"
kind: "system"
category: "Compiler and C runtime"
addresses: "0x008092FC, 0x0080929C, 0x0080926C, 0x008093C0, 0x00809364, 0x00809124, 0x02EAED40, 0x02EAED68, 0x02EAED70, 0x02EAED78, 0x02EAED80, 0x01F44850, 0x02EAED3C, 0x00189CE0, 0x01F7F5C8, 0x008964A0, 0x005C3B10, 0x02CB5D48, 0x02CB5D58, 0x02CAD140, 0x00630180, 0x0062FF50, 0x006301F0, 0x00630490, 0x006B19A0, 0x005AD8F0, 0x005E5400, 0x00221770, 0x00210EC0"
---

## What the player sees

Much of the engine's type information and many of its singletons do not exist when the game starts;
each is built the first time code asks for it, often during a load. If something stops a thread in the
middle of such a first build without letting it finish or unwind, every later thread that needs the
same object waits forever: the game sits on a loading screen using little CPU and does not crash. That
outcome follows from the code below.

## How it works

### The gate at each use

Each function-local static with a dynamic initialiser has a 32-bit guard in `.data` and an inline gate.
From `0x00189CE0`, guard `0x01F7F5C8`:

1. Read this thread's epoch: the TLS block for index `_tls_index` (`0x02EAED3C`) through `gs:[0x58]`, dword
   `+0x04` (`0x00189D22`–`0x00189D3A`).
2. `cmp [guard], epoch; jle` (`0x00189D3D`): when the guard is not greater, the static is ready and the
   block is skipped without any call.
3. Otherwise call `_Init_thread_header(&guard)` (`0x00189D4C`).
4. If the guard is now -1 (`0x00189D51`), this thread builds the object and calls
   `_Init_thread_footer(&guard)`; any other value means another thread finished it.

The accessor `0x005C3B10` is the smallest complete case (115 bytes): it returns the static `0x02CB5D48`
whose guard sits at `+0x10` (`0x02CB5D58`), and on first use stores the class descriptor `0x02CAD140` with
bit `0x1` set and a zero beside it.

### Guard and epoch values

- A guard starts at 0 (all lie in the zero-filled part of `.data`, `0x01F7F5C8`–`0x02EBA258`).
- The header sets it to -1 while one thread builds the object.
- The footer increments the global epoch `0x01F44850` and stores the new value in the guard and in the
  thread's epoch. The global epoch starts at `0x80000000`, so a finished guard holds `0x80000001` or more
  and is negative as a signed number.
- The TLS template (`0x03004000`) starts every thread's epoch at `0x80000000`, below every finished
  guard, so a thread's first pass over a finished guard calls the header, which copies the global epoch
  into the thread and returns.

### The runtime routines

All of them hold the critical section `0x02EAED40` only briefly:

- `_Init_thread_header` (`0x008092FC`) enters the lock and loops: a guard of 0 becomes -1 and the routine
  returns; a guard that is neither 0 nor -1 copies the global epoch into the thread and returns; a guard
  of -1 calls `_Init_thread_wait(100)` (`0x00809321`) and checks again. It leaves the lock by a tail jump
  to `LeaveCriticalSection` (`0x0080935C`), so the object is built outside the lock.
- `_Init_thread_footer` (`0x0080929C`) enters the lock, increments the epoch, stores it in the guard and
  the thread, leaves the lock and calls `_Init_thread_notify` (`0x00809364`).
- `_Init_thread_abort` (`0x0080926C`) enters the lock, sets the guard back to 0, leaves the lock and
  notifies.

`_Init_thread_wait` (`0x008093C0`) is called from that one site with 100 ms. With no event handle in
`0x02EAED70` it calls `SleepConditionVariableCS(0x02EAED68, 0x02EAED40, 100)`, which releases the lock while
asleep; otherwise it leaves the lock, waits on the event and re-enters. `_Init_thread_notify` wakes all
sleepers (`WakeAllConditionVariable`), or sets and resets the event. Both decode their function pointer
from `0x02EAED78` or `0x02EAED80` as `ror64(cookie xor value, cookie & 0x3F)`.

### Setting up the lock

The C initialiser `0x00809124` creates the lock (`__vcrt_InitializeCriticalSectionEx`, spin count 4000),
looks up `InitializeConditionVariable`, `SleepConditionVariableCS` and `WakeAllConditionVariable` in
`kernel32.dll`, and with all three present initialises the condition variable and stores the encoded
sleep and wake pointers, clearing `0x02EAED70`. If any is missing it stores a `CreateEventW` handle in
`0x02EAED70` instead; failure to find `kernel32.dll` or create the event fast-fails with code 7.

### A first build that never finishes

The header returns before the object is built and the wait sleeps with the lock released, so a
stuck build blocks only the threads that reach the same guard. Those threads see -1 and wait 100 ms
at a time indefinitely, since only the footer or `_Init_thread_abort` change a -1 guard.

### Release when a constructor throws

For 1,545 guards the compiler emitted a 12-byte unwind funclet, `lea rcx, [guard]; jmp 0x0080926C`, all in
`0x008964A0`–`0x008A6950` (`0x008964A0` serves guard `0x01F7F5C8`). Each funclet's RVA appears in the `.rdata`
unwind maps, and each funclet guard is one of the gate guards. A constructor that throws therefore
resets its guard to 0 and wakes the waiters. The other 136 guards have no funclet.

### Teardown registration

526 of the 707 functions holding these statics call `atexit` inside the guarded block, at 1,541 sites,
so an object's teardown is registered at the moment it is first built and the teardown order follows
the build order. See [static initialisation and teardown](static-initialisation-and-teardown.md) for
what happens to those registrations at exit.

### What the statics are

Many hold Phyre type information:

- The 61 descriptor-pair accessors (115 bytes each, like `0x005C3B10`) are slot 4 of their caller classes' vtables,
  and each fills a two-entry argument-type list `{descriptor | 1, 0}` ([caller type lists](#caller-type-lists)):
  60 for methods without arguments (the receiver, then the 0 end) and one, `0x006AC6F0`, for the caller of a
  one-argument function (`PFunctionCallerConcrete<PEntity *, PWorldMatrix *>`: `PWorldMatrix *`, then the 0 end).
  - Their 27 descriptors are all Phyre class descriptors: the code that fills each one stores a
    `PClassDescriptorConcrete`, `PClassDescriptorForType` or `PClassDescriptorWithoutDefaultConstructor`
    vtable for classes such as `PAnimatableComponent` (`0x02CAD140`), `PNode`, `PEntity`, `PCamera`,
    `PLight`, `PString` and `PApplication`.
- The 57 pair initialisers each fill a three-entry list: a receiver, one argument and the 0 end. 41 of them take the
  argument's entry from a call to one of nine functions: the type-default
  descriptors `0x00630180` (`PTypeDefault<unsigned int>`), `0x0062FF50` (`<char>`), `0x006301F0`
  (`<float>`) and `0x00630490` (`<bool>`), and lazily built wrapper descriptors for `Vector4`
  (`0x006B19A0`), `Vector3`, `Quat`, `PMatrix4` and `PMatrix4x3`.
- The scalar-conversion tree registrars on [image hardening](image-hardening.md) are 144 more.

The largest holders, `0x005AD8F0` and `0x005E5400`, guard 28 statics each.

Plain null-checked singletons are a different pattern with no guard or lock: `0x0018A620` allocates its
object through `0x00210EC0` when the pointer at `0x01F7F5D0` is null. `0x00221770` is a one-argument
allocation thunk to the same entry.

## Layouts

```
guard (u32, .data)
   0           never built
  -1           being built by one thread
  0x80000001+  built; the epoch at which it finished
```

Per-thread TLS block (template at `0x03004000`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x04` | `u32` | epoch | starts `0x80000000` |

Runtime globals:

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x01F44850` | `u32` | global epoch | starts `0x80000000` |
| `0x02EAED40` | `CRITICAL_SECTION` |  | critical section |
| `0x02EAED68` | `CONDITION_VARIABLE` |  | condition variable |
| `0x02EAED70` | `HANDLE` | event | 0 when the condition variable is used |
| `0x02EAED78` | `u64` | sleep | encoded SleepConditionVariableCS |
| `0x02EAED80` | `u64` | wake | encoded WakeAllConditionVariable |

Descriptor pair static (`0x005C3B10`'s `0x02CB5D48`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u64` | descriptor | address \| 1 |
| `+0x08` | `u64` | zero |  |
| `+0x10` | `u32` | guard |  |

## Shipped data

| Fact | Value |
|---|---|
| header and footer call sites | 1,732 each |
| distinct guards | 1,681, in `0x01F7F5C8`–`0x02EBA258` |
| guards gated in more than one function | 19, accounting for 51 extra sites |
| functions holding statics | 707: 454 hold one, the largest 28 |
| unwind funclets calling `_Init_thread_abort` | 1,545, one per guard |
| holders registering teardowns | 526, at 1,541 `atexit` sites |
| `_Init_thread_wait` call sites | 1, timeout 100 ms |

Holders are counted by `.pdata` function, chained entries folded into their primary.

The member lists beside this page, each named `lazy-statics-and-one-time-init-<list>.tsv`:

| List | Members |
|---|---|
| `descriptor-pair-accessors` | 61 accessors with their static, guard and descriptor |
| `magic-static-pair-initialisers` | 57 pair builders that call a descriptor function |
| `magic-static-singleton-guards` | 17 holders whose only calls are header, footer and `atexit` |
| `bj5-residue` | 30 further holders that register no teardown |

## State

### Caller type lists

Most statics behind a gate are the argument-type lists of Phyre's callers. Each `PMethodCallerConcrete` or
`PFunctionCallerConcrete` class has its own holder in slot 4 (`+0x20`) of its vtable. The holder returns the
address of a static array of 8-byte entries, which it fills inside its guarded block on first use and never
changes afterwards. `0x005C4AD0`, slot 4 of `PMethodCallerConcrete<PAnimationSet, PResult, PCluster &>`
(vtable `0x00D34BD8`), fills `0x02CB59F0`:

```
0x02CB59F0  0x02CAE660 | 1   receiver: PAnimationSet       stored at 0x005C4B35
0x02CB59F8  0x02CF8780 | 1   argument 1: PCluster &        stored at 0x005C4B47
0x02CB5A00  0              end of the list               stored at 0x005C4B1F
0x02CB5A08  guard
```

Every list follows the same rules, checked entry by entry against the template arguments of its caller
class:

- a method's list starts with its class's descriptor (the receiver); a function's list starts with its first
  argument;
- the arguments follow in order; the return type has no entry;
- an entry is a static class descriptor, or the result of a descriptor function the holder calls inside the
  guarded block (`0x00630180` `unsigned int`, `0x0062FF50` `char`, `0x006301F0` `float`, `0x006B19A0` `Vector4`);
- bit `0x1` is set for the receiver and for an argument passed by reference or pointer, and clear for an
  argument passed by value;
- a 0 entry ends the list, and the guard is the next word.

The 61 descriptor-pair accessors hold two-entry lists: 60 of methods without arguments and one of the
caller of a one-argument function (`0x006AC6F0`). The 57 pair initialisers hold three-entry lists: a receiver and one
argument.

| Entries, end included | Method lists | Function lists |
|---|---:|---:|
| 2 | 60 | 5 |
| 3 | 71 | 0 |
| 4 | 13 | 0 |
| 5 | 4 | 0 |
| 6 | 5 | 0 |
| 7 | 2 | 0 |
| 8 | 1 | 0 |

### Who reads the lists

No instruction reads an entry in place. Apart from the holder's own store and its `lea` of the array, no
RIP-relative, image-base-relative or disp32 reference names any entry. The lists are read through slot 4, by
the animation target binders on the function or method they look up by name (see
[animation binding](../PhyreEngine/phyre-animation-binding.md)):

- `0x005C0B60` compares a function's entry 0 with `0x006B19A0() | 1` (`0x005C0C23`) and entry 1 with 0
  (`0x005C0C28`);
- `0x005C0C90` compares a method's entry 1 with `0x006B19A0() | 1` (`0x005C0D5A`) and entry 2 with 0
  (`0x005C0D60`).

On a mismatch each logs that the function or method "does not take a single const Vectormath::Aos::Vector4 *
parameter" (`0x00D31EA0`, `0x00D31F30`) and binds it anyway. Of the 226 calls and jumps through
`[reg + 0x20]` in `.text`, these two are the only ones that read the result as a type list. No code reads
the receiver entry, or any entry from `+0x18` on.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| each row of [lazy-statics-and-one-time-init-state.tsv](lazy-statics-and-one-time-init-state.tsv): the 406 entries of the 161 lists other than the first entries of the 61 descriptor-pair accessors, which are the `descriptor` column of [lazy-statics-and-one-time-init-descriptor-pair-accessors.tsv](lazy-statics-and-one-time-init-descriptor-pair-accessors.tsv) | `void*` | 0 (zero-filled tail of `.data`) | one entry of a caller's type list: its static, offset, guard, holder, caller vtable and class, the entry's type, its value and bit `0x1`, and the holder's abort funclet when it has one (75 of the 161 holders) | the holder, once, inside its guarded block (`set_by`) | `0x005C0B60` or `0x005C0C90` through slot 4, at the sites above (`read_by`); `-` for every other entry |

### The desktop probe

`0x0079E700` keeps `user32.dll` and three of its functions in lazy statics. Behind guard `0x02EACD50` it stores
`LoadLibraryA("user32.dll")` (`0x0079E7E6`). Behind guard `0x02EACD60` it stores `GetProcAddress` results for
`OpenDesktopA`, `CloseDesktop` and `SwitchDesktop` in `0x02EACD58`, `0x02EACD68` and `0x02EACD70`. It then opens
the desktop `"Default"` with access `0x100` (`DESKTOP_SWITCHDESKTOP`), calls `SwitchDesktop` on it and
closes it.

It returns 0 only when the desktop opens and `SwitchDesktop` succeeds, and 1 when the library or any
function is missing, the desktop does not open or the switch fails. The window procedure `0x00798FF0` calls it
for message `0x8001` (`0x00799720`) and calls `0x007A0A80` only on 0, with the byte `0x01F3DA05` set. No other code
uses the two globals below: no RIP-relative, image-base-relative or disp32 reference outside `0x0079E700` names
them.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EACD48` | `void*` | 0 (zero-filled tail of `.data`) | module handle of `user32.dll`; 0 means the probe returns 1 | `0x0079E700` (`0x0079E7F3`), once behind guard `0x02EACD50` | `0x0079E700`: the null test (`0x0079E72F`) and the three `GetProcAddress` calls (`0x0079E81D`, `0x0079E831`, `0x0079E84C`) |
| `0x02EACD58` | `void*` | 0 (zero-filled tail of `.data`) | address of `OpenDesktopA`; 0 means the probe returns 1 | `0x0079E700` (`0x0079E83F`), once behind guard `0x02EACD60` | `0x0079E700` (`0x0079E74B`), which calls it at `0x0079E782` |

### Physics enum name records

The physics module's init `0x006A4100` calls `0x0069E790` (`0x006A438F`) and then `0x0069E880` (`0x006A4394`). Each
builds a `0x20`-byte record on first use with `0x006CCD80`: `+0x00` the enum's name, `+0x08` the next record,
`+0x10` its table of `{name, value}` pairs and `+0x18` the pair count, which `0x006CCDA0` stores on every call.

| Record | Guard | Name | Table | Pairs |
|---|---|---|---|---|
| `0x02E4BDC8` | `0x02E4BDE8` | `PCollisionGroup` | `0x00D7A020` | 15: `PE_COLLISIONGROUP_DYNAMIC` 0, `_STATIC` 1, `_CHARACTER` 2, `_LAYER0`-`_LAYER11` 3-14 |
| `0x02E4BDF0` | `0x02E4BE10` | `PRigidBodyType` | `0x00D7A300` | 3: `PE_RIGIDBODYTYPE_STATIC` 0, `_DYNAMIC` 1, `_KINEMATIC` 2 |

Each call then walks the list from `0x02E5BF88` comparing names. Only when its name is absent does it store the
old head in its record's `+0x08` and make the record the head. After the init the head is `PRigidBodyType`,
whose `+0x08` is `PCollisionGroup`, whose `+0x08` is 0. Nothing else reads the list: no RIP-relative,
image-base-relative or disp32 reference outside the two holders names `0x02E5BF88`.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02E5BF88` | `void*` | 0 (zero-filled tail of `.data`) | head of the enum name records | `0x0069E790` (`0x0069E867`), `0x0069E880` (`0x0069E957`): the new record | `0x0069E790` (`0x0069E81D`), `0x0069E880` (`0x0069E90D`) |
| `0x02E4BDD0` | `void*` | 0 (zero-filled tail of `.data`) | `PCollisionGroup` record `+0x08`: the head when it was linked, 0 | `0x0069E790` (`0x0069E860`) | the list walks of `0x0069E790` (`0x0069E857`) and `0x0069E880` (`0x0069E947`) |
| `0x02E4BDF8` | `void*` | 0 (zero-filled tail of `.data`) | `PRigidBodyType` record `+0x08`: the head when it was linked, `0x02E4BDC8` | `0x0069E880` (`0x0069E950`) | the list walks of `0x0069E790` (`0x0069E857`) and `0x0069E880` (`0x0069E947`) |

### The largest-channel start value

`0x00712910` (called from `0x007125B0` at `0x00712830`) copies a colour of three floats, raising negative channels
to 0. When the target at `[r8]` is positive it scales the colour so its weighted sum equals the target
(`0.2126`, `0.7152`, `0.0722` when `r9b` is set, else `0.29891`, `0.58661`, `0.11448`). When the target is
negative it finds the largest channel, starting from `0x02EA1718`, and scales so that channel equals minus the
target.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02EA1718` | `f32` | 0 (zero-filled tail of `.data`) | `-3.40282e+38` (`0xFF7FFFFF`): the lesser of `-FLT_MAX` (`0x01F3C514` with the sign mask `0x01CEBDA0`) and `FLT_MIN` (`0x01F3C510`), the start of the largest-channel search | `0x00712910` (`0x00712A90`), once behind guard `0x02EA171C` | `0x00712910` (`0x00712A9D`) |

`0x007125B0` turns a colour temperature into an RGB scale, which its callers `0x00710FC0` and `0x007110C0` multiply into a matrix (`0x006F1070`). On its first call,
while the byte `0x01F3CA50` is 1, it clears the byte (`0x007126CF`), takes the chromaticity `0x00712380` computes for
6500 K (`0x45CB2000`), makes it an RGB colour with the caller's luminance (`0x006E1530`), and keeps the reciprocals of
the three channels (`0x00712748`-`0x00712760`). Every call multiplies the requested temperature's colour by them
(`0x007127D0`-`0x007127E0`), so 6500 K comes out with equal channels.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x01F3CA50` | `u8` | 1 | the reference white is still to be made | `0x007125B0`, 0 (`0x007126CF`) | `0x007125B0` (`0x007126B3`) |
| `0x02EA1708` | `f32` | 0 (zero-filled tail of `.data`) | 1 / red of the 6500 K colour | `0x007125B0` (`0x00712748`) | `0x007125B0` (`0x007127D0`) |
| `0x02EA170C` | `f32` | 0 (zero-filled tail of `.data`) | 1 / green of the 6500 K colour | `0x007125B0` (`0x00712758`) | `0x007125B0` (`0x007127D8`) |
| `0x02EA1710` | `f32` | 0 (zero-filled tail of `.data`) | 1 / blue of the 6500 K colour | `0x007125B0` (`0x00712760`) | `0x007125B0` (`0x007127E0`) |

## Modding notes

- Hook a holder before its gate or after it, never between the header and the footer. Returning early,
  suspending or killing the thread, or leaving by `longjmp` in that span leaves the guard at -1.
- A guard read from another process tells you the state: 0 never built, -1 being built (a stuck build if
  it stays there), anything else built. The finished values rise in build order, which gives the order
  in which the engine first needed each object.
- Do not write guards: a built value hands out an unbuilt object, and 0 over a built one constructs it a
  second time.
- Do not cache a pointer to one of these objects at load time; it exists only after first use.

## Related

- [Static initialisation and teardown](static-initialisation-and-teardown.md): the eager initialisers
  and the C initialiser that creates the lock.
- [Image hardening](image-hardening.md): the cookie used to encode the wait pointers, and the
  scalar-conversion registrars.
- [Object construction and destruction](object-construction-and-destruction.md): the objects these
  statics hold.
- [`exception-handling.md`](exception-handling.md): the unwind maps that hold the guard-release funclets.
- [Class hierarchy](../Engine-Core/class-hierarchy.md): the Phyre descriptor classes by RTTI.
- [`lazy-statics-and-one-time-init-magic-static-pair-initialisers.tsv`](lazy-statics-and-one-time-init-magic-static-pair-initialisers.tsv):
  thread-safe local-static accessors that install a tagged pair of descriptor pointers and return the static: the
  133-byte ones only store, the 134- and 138-byte ones also call one initialiser of their own; with each one's size
  and the functions it calls (57 rows).

The table has one row per accessor: `address` is where it starts, `size` its length in bytes and `targets` the
functions it calls directly.
