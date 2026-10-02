# The object behind the `+0xC0` pointer in item 3's twelve bodies (FABLE, 2026-10-02)

**Result: ANSWERED (static).** None of the twelve bodies loads `+0xC0` from an ActorStorageRecord. Ten load it from
a UI widget, one from an audio submix voice, and in one the "load" reads a stack argument. So none of their 17 stores
can reach a SecondaryContext element. That means none of them can change the source byte of CharacterRenderRecord
`+0x0C1`, and item 3's index is 0 or 1 on every path.

Script: [c0_receivers.py](c0_receivers.py). Output: [c0_receivers.out](c0_receivers.out) (`FAILS 0`). It is static and
read-only, and it reuses the hash-checked image helpers from
[../mempage-residue-fable-1002/mp_lib.py](../mempage-residue-fable-1002/mp_lib.py).

## Question

The question comes from item 3 of [mempage-residue-fable-1002](../mempage-residue-fable-1002/README.md)
([script](../mempage-residue-fable-1002/item3_c1_writers_and_domain.py),
[output](../mempage-residue-fable-1002/item3_c1_writers_and_domain.out)). Item 3's tracker followed every
`mov reg, qword ptr [base + 0xc0]`, whatever its type, and found 17 wider stores in 12 bodies that land on
SecondaryContext element `+0x10` offsets. Element byte `+0x10` is the source of the nibble that `002E28E0` and
`002E3110` copy into CharacterRenderRecord `+0x0C1`. The memory page
([where-the-games-memory-comes-from.md](../../../24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md))
leaves this open: "the object type behind the `+0xC0` pointer in twelve bodies".

The decisive fact comes from the type store ([types.tsv](../../../_types/types.tsv)). SecondaryContext exists only
inside an ActorStorageRecord, at `+0x350`, and the only way to it is that record's `+0xC0`, which the region planter
`00266AD0` sets. So a store can touch the nibble only if the `+0xC0` it dereferences belongs to an ActorStorageRecord.

## Method

- **R1.** The script re-reads the 17 stores from item 3's `.out`: the B2 rows marked POSSIBLE, minus the setter
  `002EBC90` itself. It asserts there are 17 stores in 12 bodies.
- **R2: reaching definitions on each body's own CFG.**
  - The CFG uses direct branches and MSVC jump tables. A table is decoded from `lea rB, [rip -> image base]` followed
    by `mov r32, dword [rB + rI*4 + T]`, and any jump that cannot be decoded this way would be printed. None was.
  - From each store's base register, the script follows definitions back through field loads, register copies,
    `lea`, induction (`add r, imm`), pool arithmetic (`imul`, `add r, [rip]`), call returns, global cells and stack
    arguments, until it reaches a root.
  - Two or more reaching definitions are reported AMBIGUOUS and counted as a failure.
  - One loop step was read by hand and is declared in the script: `007B0311`, a list walk through `+0x10`.
- **R3: typing each root, with every fact re-checked against the bytes.** The facts are:
  - raw E8/E9/jcc callers, and the register each caller passes, traced with R2;
  - rip operands that name a handler. A widget class is identified by `lea [rip -> handler]` followed by the widget
    allocator `00244F50` (size in `ecx`) or the in-place constructor `00245000` (size in `edx`);
  - RTTI complete-object locators for vtables;
  - the class's own writers of `+0xC0`, and each written value traced with R2;
  - the type store's rows ([types.tsv](../../../_types/types.tsv), [fields.tsv](../../../_types/fields.tsv),
    [field-access-index.tsv](../../../_types/field-access-index.tsv)).
- **R4: an image-wide scan for writers of Manager0209AC60's members `+0x2E0` and `+0x300`.** It takes stores through
  any register loaded from the pointer cell `0209AC30`, plus direct rip operands at the static. It finds 4 and 2
  writers. They equal the type store's field-access-index write rows for those two members.

## Controls

All four controls pass.

| control | applied to | required | got |
|---|---|---|---|
| P1, positive (CRR writer) | the two known `+0x0C1` stores, `002E29E9` and `002E33B3` | R2 reaches the pool cell `022C6F28` with stride 0x740, which types.tsv gives as CharacterRenderRecord's instance | both reach it. Chain: `+0xC0` load → word `+0` → `*0x740` → `+ [022C6F28]` |
| P1 specificity | the 17 stores | the same CRR rule fires on none | fires on 0 |
| P2, positive (actor) | the ActorStorageRecord census load `00225D86` (`mov rcx, [rbx + 0xc0]`) | R2 roots `rbx` in the return of `00358940`, which types.tsv names as the record lookup (block + 8 + i*8). Its `rcx` is the manager slot from `00263FF0` | it does. No chain of the 17 reaches `00358940` or the manager slot table |
| N1, negative (known non-actor) | `00406A60`'s `+0xC0` load `00406C45` | R2+R3 give the 0xF0-byte widget registered by `004051B0` (slot `02B62D88`), matching the type store's WidgetSingleton02B62D88 row and its `+0xC0` field row, which cites `00406C45` | they do |

## Per body

In the base provenance chains, "arg0" means the body's first argument (`rcx`). Each arrow points back toward the
root.

| body | store site(s) | base provenance (R2) | receiver of the `+0xC0` load (R3) | what `+0xC0` holds: the stored-to object | verdict |
|---|---|---|---|---|---|
| `00292390` | `00292793` (w8 `+0x10`) | `+0xC0` @`002926F2` ← `+0x300` @`002926BB` ← cell `0209AC30` | the 0x170-byte widget whose handler is `00291D90`. Created by `002920C0`, it publishes itself at Manager0209AC60 `+0x300` in its message-1 arm (`00291F96`), and R4 finds no other non-null writer | `00291D90`'s only `+0xC0` stores: null (`00291E71`), or the return of `0024A440` (`00291F32`). That return is an entry of the 64-slot, 0x48-byte static table at `0208F580` that `0024A4E0` scans (the named-image registration) | widget / registration entry. **Not an actor** |
| `002986E0` | `00298C4C`, `00298C63`, `00298DAC`, `00298EFE` (w2 `+0x10`) | `+0xC0` ← `rdi` = arg0 (`0029871D`) | arg0 comes from its only raw site, `00299406`, which passes `00299090`'s own receiver | same as `00299090` | **not an actor** |
| `00299090` | `002991AD`, `0029926B`, `00299305` (w8 `+0x10`) | `+0xC0` ← arg0 (`002990A9`) | the 0xD8-byte widget with handler `00299090`, built in place by `00245000` (`0029C34D`, `0029C374`) inside PaneListWidget0B68 `+0x7C0` | the only `+0xC0` store is `002990FC`, the return of `0028F830`: slot *(`0209BE80`) + index*0x20, a 32-byte slot in the heap block ManagerSingleton0209BE80 | widget / manager slot. **Not an actor** |
| `0029A0A0` | `0029A29C` (w1 `+0xA0`) | `+0xC0` ← arg0 (`0029A0C9`) | PaneSlotWidget0160, the 0x160-byte widget with handler `0029A0A0`, built in place at `0029BBDA` | written only by `00297710`, whose only site, `0029A4EB`, passes this widget. The value is element-block child `[[+0x60]+0xA0/0xA8/0xB0]+0x18`, the pointer `00247870` treats as a Widget (flags `+0x40`, bit 5). The stored byte `+0xA0` is that child widget's own opacity byte (Widget `+0x0A0`) | child widget. **Not an actor** |
| `002CBA50` | `002CBBD3` (w4 `+0xD0`) | `+0xC0` @`002CBB7E` ← `+0x2E0` @`002CBA5D` ← cell `0209AC30` | the 0x170-byte widget with handler `002CBF80`. Its three creators store it at Manager0209AC60 `+0x2E0`, the handler nulls it, and R4 finds exactly these four writers | the only `+0xC0` store is `002CC20E`: a 0xF8-byte child widget (handler `002CABF0`, `00244F50` at `002CC206`), linked through `00244960`. The stores at `+0xC0`..`+0xEC` lie inside the child's 0xF8 bytes | child widget. **Not an actor** |
| `00408780` | `004087C2` (w4 `+0x100`) | `+0xC0` @`0040879A` ← cell `02B62D80` | WidgetSingleton02B62D80, a 0xE8-byte widget with handler `00406E80`. The type store's field-access-index already types `0040879A` | `00406E80`'s only `+0xC0` stores: null (`00406FB8`), or a child widget from `00244F50` (`00407107`), which is released through `00245020` (`00408226`) | child widget. **Not an actor** |
| `0053E640` | `0053E814` (w4, at `+0x10` of 0x20-byte records) | `[rdx]` with `rdx` = `+0x10`, then `+0x20` per step, ← `+0xC0` @`0053E7C3` ← arg0 (`0053E64F`) | arg0 comes from its only raw site, `0053E48F`, which passes the receiver of `0053E380`: the 0x1498-byte widget registered at `0053ED3F` and published at `02CA8A80` | `0053E380`'s only `+0xC0` stores: a 64 KiB buffer from `00249810`, cleared with memset (`0053E50D`, `0053E51D`), or null after its free through `003697F0` (`0053E3D5`, `0053E3DA`) | widget buffer. **Not an actor** |
| `00558FB0` | `00559306` (w8 `+0x100`) | `+0xC0` @`00559208` ← arg0 (`00558FCC`) | the 0xE8-byte widget with handler `00558FB0`, built by `00558F20` | the only `+0xC0` store is `00559107`. Its value is the creation parameter (jump-table entry 0, message 1, is the only route to `005590EF`), which `00558F20` sets to its own `rcx`. Both sites of `00558F20` pass a 0x190-byte widget (handler `00560910`, registered at `005601EC`): either `00560910`'s receiver, or the `+0xC0` of `00561390`, which is that same owner | owner widget. **Not an actor** |
| `00561390` | `005616A8` (w8 `+0x100`) | `+0xC0` @`00561601` ← arg0 (`005613A9`) | WidgetSingleton02CA9670, the 0x110-byte widget with handler `00561390`, built by `00561300` | the only `+0xC0` store is `00561580`, from the creation parameter in the message-1 arm. Both sites of `00561300` pass the same 0x190-byte owner: `00560910`'s receiver, or `00558FB0`'s `+0xC0` | owner widget. **Not an actor** |
| `00564E10` | `005650DD` (w8 `+0xD0`) | `+0xC0` @`005650B3` ← `+0xC0` @`005650A4` ← arg0 (`00564E39`) | arg0 is a 0x188-byte widget. Its four handlers end in the shared tail `005636F0` / `00563930` / `00563B10` / `00563D20` → `005651E0`, and it is created by `00564B90` → `00564AC0` → `00244F50` and stored at Manager0209AC60 `+0x170` + i*8 (`00564C40`). The sites are `00564CAC` (that widget's receiver) and `005651D7` (the `+0x170` slot). The `+0xC0` load at `005650B3` reads from that widget's own `+0xC0`, a Widget: `005650ED` passes it to `00247950` (Widget `+0x10` and `+0x40`) | that Widget's `+0xC0` is a peer Widget. The body links it with arg0 through `+0xD8` (`005650BC`, `005650C6`), and `002D45C0` walks it as a widget (`+0x10` parent, `+0x40` flags, `+0x7C`) | peer widget. **Not an actor** |
| `007DACF0` | `007DAD95` (w4, float) | `rdi` = `+0x44`, then `+0x20` per step, ← `mov rbx, [rsp + 0xc0]` @`007DAD10` = **the fifth (stack) argument**, not a field | the only raw site, `007DACDE` in `007DACC0`, passes `rcx + 0x40`. `007DACC0` is reachable only as slot 3 of the vtable at `01CB7970`, whose RTTI is `SQEX::Sd::Driver::HilbertFilter` | the filter object's own float state | audio filter. **Not an actor**, and not a `+0xC0` load at all |
| `007E01F0` | `007E0504` (w16 `+0x10`) | `+0xC0` @`007E04DE` ← arg0 (`007E021B`) | the only raw site, `007B0306`, passes the `+0x20` payload of the nodes in the list at `02EAD2D0`, walked from head `02EAD2F0` through `+0x10`. Only `007AEC10` inserts a payload, and that payload is the object constructed by `007DFF20`, whose vtable at `01CB82D0` has RTTI `SQEX::Sd::Driver::Core::CoreSubmixVoice`. The list's initialiser `007AEE20` zeroes every payload | the constructor zeroes `+0xC0` (`007DFF63`). `007E0130` then fills `+0xB8` and `+0xC0` from `007AD460` (`007E01A4`..`007E01CD`) with a buffer of four bytes per channel | audio buffer. **Not an actor** |

**Counts:**
- ten widget receivers: `00292390`, `002986E0`, `00299090`, `0029A0A0`, `002CBA50`, `00408780`, `0053E640`, `00558FB0`,
  `00561390` and `00564E10`;
- one audio voice: `007E01F0`;
- one stack argument: `007DACF0`;
- zero ActorStorageRecord receivers;
- zero bodies left undecided.

## Limits

- **Coverage of `+0xC0` writers.** Each class's writers were swept in that class's own handler and creator, and in
  the callees named above. The two Manager0209AC60 members were swept image-wide (R4). A writer outside the class,
  in code that knows the layout, would be missed. In every body, though, the stored-to object is also dereferenced
  as its own type: widget helpers, the 0x20- and 0x48-byte records, and the per-channel buffer.
- **The 0x188-byte widget's `+0xC0` writer was not located.** Its content is typed by use only: two widget helpers
  read it with the Widget layout.
- **The voice list's payload writers.** Only two were found: the insert `007AF380` (`007AF455`) and the pool
  initialiser (`007AEEF1`, zero). The list object is named by two rip operands, `007AEC90` and `007AF2F3`. The four
  register-based inserts into other lists pass a null payload.
- **What R2 does not follow.** R2 is intraprocedural. It reaches arguments through raw callers and through
  registrations. It does not cover handler dispatch: that a widget's handler receives the widget in `rcx` is the
  type store's Widget contract (proc at `+0x00`, `void(*)(Widget*, const WidgetMessage*)`).
- **Side observation, not acted on.** `0028F830` indexes ManagerSingleton0209BE80 from its base in 0x20-byte steps,
  while the type store models that block's first bytes as header qwords.

## Proposed page sentence

This replaces the memory page's "Still open, static: the object type behind the `+0xC0` pointer in twelve bodies
whose wider stores land on these offsets (no receiver is proven)."

> None of the twelve bodies whose wider stores an untyped `+0xC0` tracker placed on these offsets reaches an actor
> record: in ten the `+0xC0` belongs to a UI widget and holds a child or owner widget, a manager slot, an
> image-registration entry or a private buffer, in one it belongs to an audio submix voice and holds a per-channel
> buffer, and in one the "pointer" is a stack argument of an audio filter method, so none of them can change the
> source byte and the index stays 0 or 1 *(answered 2026-10-02, FABLE, static; record
> `_index/candidates/c0-receiver-fable-1002/`)*.

The page's status line would then drop "the +0xC0 receiver type in twelve bodies (static)" from its open list. FABLE
edits the page; this folder does not touch it.

run: c0_receivers.py at fd96f1634

## Consumer check (FABLE)

affected: `Database/FFXII TZA/24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md`

- consumer: the memory page's `+0x0C1` closure note: revised-here (the open receiver sentence struck and answered by role).
- consumer: the memory page's status line: revised-here (the item is dropped; the arena blocks' run-time placement stays open).
- consumer: [`mempage-residue-fable-1002`](../mempage-residue-fable-1002/README.md) item 3: agrees (this closes its one narrowed fact; not edited).
