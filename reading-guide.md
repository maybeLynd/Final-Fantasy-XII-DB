# Reading the database

Back to [Home](README.md).

## Pages

Pages come in four kinds. The table at the top of a page gives its `kind`, shown here in brackets:

- **Explanation** (`system`) describes a game mechanic: what the player sees, how it works, its layouts,
  operations and state, and modding notes.
- **Walkthrough** (`operation`) follows one thing the game does, step by step in the order it happens.
- **Format** (`format`) describes a file or data format: where it comes from, its layout, the shipped data
  and how the loader treats each field.
- **Reference table** (`reference`) lists a set of game values, with the same data beside them as a `.tsv` file.

Each page title names the topic and then what the page covers. Each topic's README lists its pages
with a one-sentence summary of what you will find on each.

## Addresses and names

Addresses are virtual addresses in the shipping `FFXII_TZA.exe` (SHA-256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`), image base included. The image loads at
its preferred base `0x00120000` unless mandatory ASLR moves it; then each address is at the module base plus
(address - `0x00120000`).

A function is identified by its address. Where a page also gives a function a name such as
`ImageAddress_ResolveRuntimePointer`, the name is this database's label for it: the executable
does not contain it, unless the page says the name is a string in the executable.

## Access tables

Many tables list the instructions that read or write one object, one row per instruction. Their columns:

- `function`: the address of the function that holds the instruction.
- `name`: the function's name, or `FUN_` and its address in lower case where this database has no name for it.
- `site`: the address of the instruction.
- `disp`: the offset from the object's start that the instruction reaches; for an element of an array, the offset
  from the element's start.
- `kind`: `r` a read, `w` a write, `rw` both (for example `add [rcx+8], eax`), `addr` (or `a`) the address is
  computed and nothing is read or written (`lea`). Values such as `set` and `copy` are explained on the pages that
  use them.
- `instruction`: the instruction as disassembled.
- `route`: how the object reached the register the instruction addresses through (below).
- `note`: a remark on the row, where it has one; in a route-seeded row, the host the access descends from
  (below).
- `width`, in some tables: the size of the access, in bytes or as `byte`, `word`, `dword` or `qword`.

### Reading a route cell

A route cell such as `route-seeded STATIC 0x02CC0410 base+0x2F8 exposed` has up to three parts:

- an opening word that says where the search for the object's accesses started;
- the object's route: where the object lives, in the forms listed under "Route forms";
- marks about this one access: `base+0xN`, `exposed` and `zeroclear`.

Some cells hold a route alone, with no opening word. Where a table's page describes its own `route` column, as the
actor record, battle unit and spawn record field tables do, the page's description applies.

### Starting points

The opening word names how the search found the object:

- `route-seeded`, followed by a route: the search started wherever the code obtains the object through that route.
  The rest of the cell is the object's route as this database recorded it when the table was made.
- `vtable-seeded 0x00D31898`: at each function listed in the virtual function table at that address, with the object
  in `rcx`.
- `ctor-seeded 0x006C0EB0`: at that function, with the object in `rcx`: its constructor, or another function that
  takes the object as its first argument.
- `ctorrdx-seeded 0x005A26F0`: at that function, with the object in `rdx`. Such a function builds the object in place
  for a PhyreEngine class descriptor, which is in `rcx`.
- `call-seeded 0x001D50D0`: at each call to that function, with the object its return value in `rax`.
- `static-seeded 0x02B3F570`: the object is at that address; at each instruction that puts the address in a register.
- `ctor 0x005049E0` after `route-seeded`, alone or as one of the alternatives: the search also started at that
  function, the one this database lists as the type's constructor, with the object in `rcx`. It names no host.
- `seeded on proven entry points:` and a list of functions: at each listed function, with the object in `rcx`.
  Without the colon, `seeded on proven entry point` or `entry points` names only the listed functions whose
  search reached the row's access.

From these starting points the search follows the object into the functions it is passed to as an argument, so a
row's function can be several calls away from the start.

A route-seeded row whose `note` names a host lists in its route cell only the alternatives whose search reached
the row's access. The host is where such an alternative yields the object: `host: this function` is the row's
own function, and `host` with addresses names the functions the access descends from, such as the function that
loads the route's pointer, a method of its virtual function table, the function its `ARG` names or a caller of
its `FN`.

Other tables name their starting point in one of these forms:

- `gptr 0x01F81300`: the code loaded the object's address from the pointer stored at that address, and the
  instructions using the loaded value in the same function are listed.
- `ptr-depth1 0x0209A670+0x0`: the same, also followed one call deep into the functions the value is passed to;
  `+0x0` is the offset of the object from the loaded address.
- `array 0x02098E10 rip`: an access to the array at that address whose operand is relative to `rip`, not a register
  holding the array.
- `embed ActorManagerSlot+0x110`: the rows of the containing object's table that fall inside this object, which
  starts at that offset in it; `disp` counts from this object's start.
- `call 0x00193D50`, `ctor 0x0018CD90` or `gptr 0x01F81300`, then steps such as `->arg0@0x0017CF72`: the object was that
  function's return value, the object that constructor builds (in `rcx`), or the value loaded from that address,
  and was then passed as argument 0 (`rcx`), 1 (`rdx`) and so on at each call site listed.
- A step `+lea3F0` in such a chain: a pointer to offset 0x3F0 of the object was formed with `lea` and followed.
- `argN+0xK<F@S`, as in `arg0+0x0<0x00264010@0x00264025`: the function received the object's address plus K as argument
  N from the caller F, at the call site S. `arg0 from 0x00358F90 at 0x0035900B` and
  `arg0+0x30 from 0x0026B2E0 at 0x0026B3D8` say the same in words.
- `STACK (0x003200A0 out)`: the object is a record on the stack whose address each caller passes to the function
  `0x003200A0`, which fills it.

### Route forms

The route after `route-seeded` describes where the object lives. Offsets and strides are hexadecimal, `count=` is a
decimal number or the name of the member that holds the count:

- `PTR 0xADDR`: the object's address is stored at ADDR. With `+0xOFF`, the object starts OFF bytes after the stored
  address. `PTR [0xADDR]` means the same.
- `STATIC 0xADDR`: the object is at ADDR.
- `ARRAY 0xADDR stride=0xS count=N`: element i is at `ADDR + i*S`. `index=` names what selects the element, as in
  `index=slot`.
- `PARRAY 0xADDR stride=0xS count=N`: the same array, with its start stored at ADDR.
- `SLOTPTR 0xADDR stride=0xS`: a table of pointers at ADDR, S bytes apart, each pointing at one object;
  `SLOTPTR Type +0xOFF stride=0xS` is the same table at offset OFF inside an object of type `Type`.
- `FN 0xADDR+0xOFF`: the object starts OFF bytes after the address the function at ADDR returns. With `bank=0xD`
  the function serves several kinds of object, and the search uses the calls whose `rcx` was loaded from offset D
  of a member.
- `EMBED Type +0xOFF`: the object lies inside an object of type `Type`, at offset OFF; with `stride=0xS count=N` it
  is one of N elements S bytes apart from there.
- `CHAIN Type +0xOFF`: the object is the member at offset OFF of `Type`, or the object that member points at, as
  `Type`'s field list declares. Each further `+0xN` follows one more pointer. With `stride`, the member points at
  the start of an array of such objects.
- `VTABLE 0xADDR`: the object is reached through virtual calls: each function in the virtual function table at ADDR
  receives it in `rcx`.
- `RELOFF Type +0xOFF`: the object starts at an object of type `Type` plus the 32-bit value stored at its offset
  OFF.
- `PKREF 0xFN Parent +0xOFF`: the 32-bit value at offset OFF of `Parent` (a type, or an address that holds the
  object) is a pack offset, and the function at FN turns it into the object's address.
- `ARG rcx 0xADDR`: the object is in that register when the function at ADDR starts.
- `DYNAMIC` and a description: the object's place is computed while the game runs, and the text says how. A search
  does not start from it; it starts from the cell's other routes.

Within a route:

- Two or more routes separated by a vertical bar are alternatives: the object can be reached each way, and the
  search started from each one it could use. When the row's `note` names a host, the cell lists only those that
  reached the row's access; otherwise it does not say which one did.
- A route, ` <- ` and a second route, as in `CHAIN Manager0209AC60 +0x2F8 <- PTR 0x0209AC30`: the first places
  the object in or behind a member of another object, and the second is the route of the outermost such object,
  where the search started. The rows are the accesses that fall in this object.
- Text after ` - ` or ` -> ` describes that route, as in `-> the object itself (vtable written there by 0x0015BC40)`.
- Names such as `SlowReaderRecordBank`, `RenderContext02CC0410` or `PApplication*` are this database's labels for
  object types: the executable does not contain them. The symbol index lists each as a structure; a trailing `*`
  means a pointer to that type.

### Marks on an access

- `base+0xN`: the register the instruction addressed through held the address of the object's byte N, so `disp` is
  N plus the instruction's own displacement. `base+0x-7D8` means the register pointed 0x7D8 bytes before the
  object's start, into the object that contains it.
- `exposed`: the function has more than 20 callers, or the search reached it through such a function. Its
  accesses may come from a helper that works on many kinds of object, so they say less about this object's layout.
- `zeroclear`: the instruction writes a register that holds zero, and the same function writes zero at the same
  width at the next or the previous offset: part of clearing a run of bytes, which does not mark where fields begin.

## Symbol index

[symbol-index.tsv](FFXII%20TZA/symbol-index.tsv) gives each symbol the page that explains it: the structures, fields,
script verbs and file families of the database, every function and written global the pages and tables cite, and
every other address in the executable that a page cites. Its columns:

- `kind`: structure, field, script verb, file family, function, global or data (a table, a vtable or other data).
- `symbol`: the type name, `Type+0xOFFSET` for a field, the call id of a script verb, the path pattern of a file
  family, or the address. An address inside a function is listed under the function's entry.
- `names`: the names the tables give the address, or the name of the type, field or verb.
- `home`: the page that explains it. For an address, the page whose top table lists it first; else the page that defines it (the address in a heading, in the first
  cell of a table row, or in a sentence that says what it is or does), else the page that cites it most; an address
  only tables cite has the table that cites it most.
- `see_also`: the other pages that describe a structure.
- `cited_in_files`: how many pages and tables other than `home` cite the address; `README.md` files, this index and
  `phenomenon-index.tsv` are not counted, and neither is a table cell that holds an authored number, a game id or a text code.

## Phenomenon index

[phenomenon-index.tsv](FFXII%20TZA/phenomenon-index.tsv) starts from what the player sees or hears and gives its cause and
the page that explains it. Every row is copied from a page or table of the database. Its columns:

- `kind`: setting or input (a Config row, a control, a settings file value, a launcher setting, a render setting, a
  script verb or another input that shows something), or feature (what a page says the player sees).
- `phenomenon`: what is seen or heard: the input's visible effect, or the opening of the page's "What the player
  sees" section (one row per item when it opens with a list).
- `cause`: the input that causes it, or the title of the page.
- `source`: the table or page the row is copied from.
- `page`: the page that explains it.
