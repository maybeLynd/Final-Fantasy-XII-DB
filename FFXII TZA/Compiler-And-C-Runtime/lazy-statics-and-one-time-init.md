---
title: "Lazy statics and one-time initialisation: thread-safe local statics, their guards, the shared lock and the release on exceptions"
kind: "system"
category: "Compiler and C runtime"
addresses: "008092FC, 0080929C, 0080926C, 008093C0, 00809364, 00809124, 02EAED40, 02EAED68, 02EAED70, 02EAED78, 02EAED80, 01F44850, 02EAED3C, 00189CE0, 01F7F5C8, 008964A0, 005C3B10, 02CB5D48, 02CB5D58, 02CAD140, 00630180, 0062FF50, 006301F0, 00630490, 006B19A0, 005AD8F0, 005E5400, 00221770, 00210EC0"
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
From `00189CE0`, guard `01F7F5C8`:

1. Read this thread's epoch: the TLS block for index `_tls_index` (`02EAED3C`) through `gs:[0x58]`, dword
   `+0x04` (`00189D22`–`00189D3A`).
2. `cmp [guard], epoch; jle` (`00189D3D`): when the guard is not greater, the static is ready and the
   block is skipped without any call.
3. Otherwise call `_Init_thread_header(&guard)` (`00189D4C`).
4. If the guard is now -1 (`00189D51`), this thread builds the object and calls
   `_Init_thread_footer(&guard)`; any other value means another thread finished it.

The accessor `005C3B10` is the smallest complete case (115 bytes): it returns the static `02CB5D48`
whose guard sits at `+0x10` (`02CB5D58`), and on first use stores the class descriptor `02CAD140` with
bit 0 set and a zero beside it.

### Guard and epoch values

- A guard starts at 0 (all lie in the zero-filled part of `.data`, `01F7F5C8`–`02EBA258`).
- The header sets it to -1 while one thread builds the object.
- The footer increments the global epoch `01F44850` and stores the new value in the guard and in the
  thread's epoch. The global epoch starts at `0x80000000`, so a finished guard holds `0x80000001` or more
  and is negative as a signed number.
- The TLS template (`03004000`) starts every thread's epoch at `0x80000000`, below every finished
  guard, so a thread's first pass over a finished guard calls the header, which copies the global epoch
  into the thread and returns.

### The runtime routines

All of them hold the critical section `02EAED40` only briefly:

- `_Init_thread_header` (`008092FC`) enters the lock and loops: a guard of 0 becomes -1 and the routine
  returns; a guard that is neither 0 nor -1 copies the global epoch into the thread and returns; a guard
  of -1 calls `_Init_thread_wait(100)` (`00809321`) and checks again. It leaves the lock by a tail jump
  to `LeaveCriticalSection` (`0080935C`), so the object is built outside the lock.
- `_Init_thread_footer` (`0080929C`) enters the lock, increments the epoch, stores it in the guard and
  the thread, leaves the lock and calls `_Init_thread_notify` (`00809364`).
- `_Init_thread_abort` (`0080926C`) enters the lock, sets the guard back to 0, leaves the lock and
  notifies.

`_Init_thread_wait` (`008093C0`) is called from that one site with 100 ms. With no event handle in
`02EAED70` it calls `SleepConditionVariableCS(02EAED68, 02EAED40, 100)`, which releases the lock while
asleep; otherwise it leaves the lock, waits on the event and re-enters. `_Init_thread_notify` wakes all
sleepers (`WakeAllConditionVariable`), or sets and resets the event. Both decode their function pointer
from `02EAED78` or `02EAED80` as `ror64(cookie xor value, cookie & 0x3F)`.

### Setting up the lock

The C initialiser `00809124` creates the lock (`__vcrt_InitializeCriticalSectionEx`, spin count 4000),
looks up `InitializeConditionVariable`, `SleepConditionVariableCS` and `WakeAllConditionVariable` in
`kernel32.dll`, and with all three present initialises the condition variable and stores the encoded
sleep and wake pointers, clearing `02EAED70`. If any is missing it stores a `CreateEventW` handle in
`02EAED70` instead; failure to find `kernel32.dll` or create the event fast-fails with code 7.

### A first build that never finishes

The header returns before the object is built and the wait sleeps with the lock released, so a
stuck build blocks only the threads that reach the same guard. Those threads see -1 and wait 100 ms
at a time indefinitely, since only the footer or `_Init_thread_abort` change a -1 guard.

### Release when a constructor throws

For 1,545 guards the compiler emitted a 12-byte unwind funclet, `lea rcx, [guard]; jmp 0080926C`, all in
`008964A0`–`008A6950` (`008964A0` serves guard `01F7F5C8`). Each funclet's RVA appears in the `.rdata`
unwind maps, and each funclet guard is one of the gate guards. A constructor that throws therefore
resets its guard to 0 and wakes the waiters. The other 136 guards have no funclet.

### Teardown registration

526 of the 707 functions holding these statics call `atexit` inside the guarded block, at 1,541 sites,
so an object's teardown is registered at the moment it is first built and the teardown order follows
the build order. See [static initialisation and teardown](static-initialisation-and-teardown.md) for
what happens to those registrations at exit.

### What the statics are

Many hold Phyre type information:

- The 61 descriptor-pair accessors (115 bytes each, like `005C3B10`) build `{descriptor | 1, 0}` pairs.
  Their 27 descriptors are all Phyre class descriptors: the code that fills each one stores a
  `PClassDescriptorConcrete`, `PClassDescriptorForType` or `PClassDescriptorWithoutDefaultConstructor`
  vtable for classes such as `PAnimatableComponent` (`02CAD140`), `PNode`, `PEntity`, `PCamera`,
  `PLight`, `PString` and `PApplication`.
- The 57 pair initialisers build the same kind of pair; 41 of them call one of nine functions for it: the type-default
  descriptors `00630180` (`PTypeDefault<unsigned int>`), `0062FF50` (`<char>`), `006301F0`
  (`<float>`) and `00630490` (`<bool>`), and lazily built wrapper descriptors for `Vector4`
  (`006B19A0`), `Vector3`, `Quat`, `PMatrix4` and `PMatrix4x3`.
- The scalar-conversion tree registrars on [image hardening](image-hardening.md) are 144 more.

The largest holders, `005AD8F0` and `005E5400`, guard 28 statics each.

Plain null-checked singletons are a different pattern with no guard or lock: `0018A620` allocates its
object through `00210EC0` when the pointer at `01F7F5D0` is null. `00221770` is a one-argument
allocation thunk to the same entry.

## Layouts

```
guard (u32, .data)
   0           never built
  -1           being built by one thread
  0x80000001+  built; the epoch at which it finished

per-thread TLS block (template at 03004000)
  +0x04  u32   epoch        starts 0x80000000

runtime globals
  01F44850  u32           global epoch, starts 0x80000000
  02EAED40  CRITICAL_SECTION
  02EAED68  CONDITION_VARIABLE
  02EAED70  HANDLE        event, 0 when the condition variable is used
  02EAED78  u64           encoded SleepConditionVariableCS
  02EAED80  u64           encoded WakeAllConditionVariable

descriptor pair static (005C3B10's 02CB5D48)
  +0x00  u64   descriptor   address | 1
  +0x08  u64   zero
  +0x10  u32   guard
```

## Shipped data

| Fact | Value |
|---|---|
| header and footer call sites | 1,732 each |
| distinct guards | 1,681, in `01F7F5C8`–`02EBA258` |
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
- `exception-handling.md`: the unwind maps that hold the guard-release funclets.
- [Class hierarchy](../Engine-Core/class-hierarchy.md): the Phyre descriptor classes by RTTI.
