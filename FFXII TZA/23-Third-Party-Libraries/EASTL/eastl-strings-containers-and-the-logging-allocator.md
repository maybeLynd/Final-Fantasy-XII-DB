---
system: EASTL — strings, containers and the logging allocator
category: 23-Third-Party-Libraries
status: AUDITED — every register row is closed (owner re-status 2026-09-30, OPUS): the EASTL version is OUT OF EVIDENCE BOUNDARY (BS-5, 2026-09-27; UQ-306 SUPERSEDED as its duplicate) - the image holds no version banner, and the eight EASTL strings bound the line to an EA-internal branch, whose version only that branch or the build configuration states (§7)
owner_layer: CodeDomain:EASTL.*
evidence_tier: 3
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
last_reviewed: 2026-09-30
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  crossref_clean: true
  reopened_count: 0
  promoted: 2026-10-01 DOCUMENTED -> AUDITED by SWE2-AUDIT-SPEC (FRONTIER eligibility census sweep): falsification record 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2; audit_crossrefs at HEAD reports 0 unresolved findings; cross-subsystem neighbours dispositioned in their section; killer observations recorded in the pass; promoter is not the last substantive author (last substantive commit: OPUS)
function_families:
  - "EASTL basic_string<char> static initialisers | C | members/eastl-string-static-initialisers.tsv | 51 | not this game's code: compiler-generated dynamic-initialiser stubs, one per static eastl::basic_string. PROVED BY FORM PLUS THE LITERAL ITSELF - 51 members, all 240 bytes, 178 byte positions identical (the other 62 are the operands that must vary: object, literal, dtor). Every member leas 008F6600 - the ASCII literal EASTL basic_string, the allocator_memory_log tag; the code names its own library type. CONTROL: every member calls 001EDF00 (allocator_memory_log ctor, this page's identifying symbol) EXACTLY twice - the stack copy and the allocator embedded at +0x18 of the static object - and tail-jumps 00808B90, the atexit wrapper. Body semantics read: construct allocator, zero the three-pointer string, measure the literal (end minus start plus one), allocate through the allocator vtable or point all three pointers at the shared empty byte 02EBA2E0, copy the literal, NUL-terminate, register the dtor. THE BOUNDARY: the form is the toolchain's; a reconstruction declaring the same static strings gets these from its own compiler. NOT dispositioned: 001EDF00 (documented here), the per-object destructors, the literals, and which game string each object holds. Selector: members/select_eastl_string_static_inits.py"
  - "EASTL basic_string<char> static initialisers - variant forms | C | members/eastl-basicstring-variant-initialisers.tsv | 7 | not this game's code: the same allocator_memory_log / EASTL basic_string initialiser mechanism as the 51-member 240-byte family, in the toolchain's other generated shapes (6 at 228 bytes, 2 at 74 bytes - different source-string argument forms). PROVED BY THE TAG LITERAL - every member leas 008F6600 (\"EASTL basic_string\"), calls 001EDF00, and tail-jumps the atexit wrapper 00808B90; every member is a .CRT$XI array entry and census-wide skeleton scans find no unclaimed twins. NOT dispositioned: 001EDF00, the per-object destructors, and the strings. Selector: members/select_xc_array_clusters.py (under 24-Compiler-And-CRT-Runtime/Static-Initialization-And-Teardown) 1 member(s) left the family 2026-09-20, since measured as A (A beats a declaration): 0015C560"
  - "EASTL container static initialisers - vector, map, list | C | members/eastl-container-static-initialisers.tsv | 4 | not this game's code: the same allocator_memory_log mechanism with the other EASTL container tag literals - \"EASTL vector\" (008C5F58), \"EASTL map\" (008F4120 x2), \"EASTL list\" (008F3CC0) - one static container each. PROVED BY THE TAG LITERAL - every member leas one of the three tags, calls 001EDF00, tail-jumps 00808B90, and sits in the .CRT$XI array. NOT dispositioned: 001EDF00, the destructors, and the four containers. Selector: members/select_xc_array_clusters.py (under 24-Compiler-And-CRT-Runtime/Static-Initialization-And-Teardown)"
---

# EASTL — strings, containers and the logging allocator

> The twelfth third-party library, missing from this database until 2026-09-02. It is the string and
> container layer underneath almost everything else, and its string representation has already turned
> up inside three other documents without being named.

## 1. What the player sees

Nothing, directly — and that is the point. EASTL is Electronic Arts' replacement for the C++ standard
library, and FFXII uses it for the two most ordinary jobs in any program: **holding a piece of text,
and holding a list of things**.

It matters to a modder for one blunt reason. When you look at any structure in this game and see
three consecutive pointers, you are very often not looking at three separate fields — you are looking
at **one string or one list**, and misreading it as three pointers will make the whole structure
around it come out wrong. Recognising the shape is the difference between reading a struct correctly
and inventing one.

The one place it becomes almost visible: **an empty string in this build does not own any memory at
all.** Every empty string in the game points at the same single shared byte. That is not a
micro-optimisation nobody notices — it is why the game can create and discard enormous numbers of
empty strings during loading without touching the allocator once.

## 2. Native mechanism

### The string is three pointers, and there is no inline buffer

An `eastl::basic_string` here is **24 bytes: three pointers**.

```
begin        the first character
end          the null terminator's position (so length == end - begin)
capacity_end one past the last allocatable byte
```

Note what is *not* here: this build carries **no short-string optimisation** — no inline character
buffer, no union, no length-in-the-low-bits trick. A string of any non-zero length owns a heap
allocation. That is worth stating explicitly because the opposite is so often assumed, and because
one nearby idiom looks like SSO and is not: the reflection binder in
[`../../22-Middleware-PhyreEngine/Animation-Channel-Binding/animation-channel-binding-and-transform-composition.md`](../../22-Middleware-PhyreEngine/Animation-Channel-Binding/animation-channel-binding-and-transform-composition.md)
tests the low bit of a pointer's first byte to choose inline storage — that is **MSVC's** short-string
representation in a different structure, not EASTL's.

### The empty string is a shared global, not an allocation

When a string is constructed from a C string of length 0, the code does not call the allocator:

```c
n = strlen(src) + 1;
if (n < 2) {                       /* the string is empty */
    end          = &DAT_02EBA2E0;  /* a shared, process-global single byte */
    capacity_end = &DAT_02EBA2E1;
} else {
    end = capacity_end = allocator->allocate(n);
}
```

Every empty string in the process therefore points at the same address. The destructor's guard is
what makes that safe, and it is the reason the guard looks odd out of context:

```c
if ((capacity_end - begin) > 1 && begin != NULL)
    allocator->deallocate(begin, capacity_end - begin);
```

A one-byte "capacity" can only be the shared sentinel, so the `> 1` test is precisely *"this is not
the shared empty string"*. **Anyone hooking string destruction must preserve that test** — freeing
the sentinel would corrupt every empty string in the game at once.

### The allocator is a vtable, and it is named

Allocation does not go through `operator new`. It goes through a small object whose vtable is
`eastl::allocator_memory_log::vftable` — a **genuine qualified symbol in the image**, which is what
identifies the library beyond doubt. Two slots are used everywhere:

```
allocator vtable
  +0x10   allocate(self, size, flags)
  +0x18   deallocate(self, ptr, size)
```

`deallocate` is **sized** — the caller passes the byte count back, recomputed from the pointers. The
allocator is constructed with a **name string**, and every string allocation in the game passes the
same literal:

```
"EASTL basic_string"
```

The class name (`allocator_memory_log`) plus a per-allocation name argument says this build ships the
**memory-logging** allocator, not the plain one — ~~the shipping game retains the ability to attribute~~
~~allocations by name.~~ *(Corrected 2026-09-30, OPUS: it retains the class, not the capability. The constructor
`001EDF00` stores only the vtable and never reads the name argument (BS-6, §7; [`eastl_dd_check.py`](../../_index/candidates/opus-dd-eastl-0930/eastl_dd_check.py) N1), so no allocation can be
attributed by that name in this build.)*

### Vector growth

The vector body carries four fields — `begin`, `end`, `capacity_end`, and an inline **allocator**
(not a pointer to one; the allocator object sits at `+0x18` in the container). Growth on an
insert of `n` elements:

```c
newCapacity = max(size + n, size == 0 ? 1 : size * 2);
```

So: **double, unless the request needs more than double, in which case take exactly what is needed** —
and a first insertion into an empty vector allocates exactly 1 element, not a default block. A vector
that grows one element at a time therefore reallocates at 1, 2, 4, 8, … and a bulk insert of 100 into
an empty vector allocates exactly 100.

### Fifty-eight string globals, built at startup

`EASTL.BasicString.StaticInitializer` is 58 functions, each building **one process-global string**.
They are structurally identical and **not** byte-identical — 52 are 240 bytes and 6 are 228, and two
sampled bodies have different SHA-256s. Each one:

1. constructs the named allocator,
2. zeroes its three pointers,
3. allocates exactly `len + 1`,
4. `memmove`s the literal in from `.rdata`,
5. writes the terminator,
6. registers its own `atexit` destructor in the `008Axxxx` range. *(Anchored 2026-09-30, OPUS: `0015C62B` loads the
   destructor `008A69F0` and `0015C63F` tail-jumps to the atexit wrapper `00808B90`; `0015D610` does the same with
   `008A70F0`; [`eastl_dd_check.py`](../../_index/candidates/opus-dd-eastl-0930/eastl_dd_check.py) A1.)*

Each has **its own three globals and its own destructor** — they are not entries in a table.

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `001EDF00` | `eastl_allocator_memory_log_ctor` | 14 B | writes `eastl::allocator_memory_log::vftable` — **the qualified symbol that identifies the library** |
| `001FF740` | `EASTL_LookupByCString` | 300 B | `strlen` → empty-sentinel or allocate `len+1` → `memmove` → terminate; 17 callers |
| `001E7D30` | `eastl_vector_insert_fill_reallocate` | 607 B | the growth policy and the element-shuffling insert |
| `001600D0` | `eastl_string_static_init` (sample) | 240 B | one process-global string: 4-char payload, allocates 5 |
| `0015FE00` | `eastl_string_static_init` (sample) | 240 B | one process-global string: 2-char payload, allocates 3 |
| `00200E60` | `JsonBox_Value_LoadFromStream` | 1,527 B | **read 2026-09-12 (BS-1)** — JsonBox's parser: 13 `basic_istream::get`, 3 `putback`, 14 of the JsonBox token globals, building EASTL `map` / `vector` / `basic_string` values |
| `001FF210` | `JsonBox_Value_Output` | 707 B | **read 2026-09-12 (BS-1)** — JsonBox's writer: recursive (calls itself twice), `operator<<` on `basic_ostream`, 5 token globals, string escaping through `memmove` |
| `001FF6B0` | callee of `001FF740` | 130 B | ~~consumes the constructed temporary — **not read**~~ read 2026-09-30 (OPUS; also on [what the console tunes](../../00-Engine-Core-Runtime/Developer-Tuning-Console/what-the-console-tunes.md)): makes the JsonBox value an object (type 3, a `0x38`-byte map whose allocator is named `EASTL map`) when it is not one, then tail-jumps to the find `001FF4F0` ([`eastl_dd_check.py`](../../_index/candidates/opus-dd-eastl-0930/eastl_dd_check.py) F1) |

Addresses are Ghidra image base `0x00120000`. Every row above is a function.

### Data addresses cited by this document

| Address | Name | Kind | Contents |
|---|---|---|---|
| `02EBA2E0` | shared empty-string byte | 1 byte | what every empty `basic_string`'s `end` points at |
| `02EBA2E1` | shared empty-string capacity end | — | one past the sentinel; the `> 1` guard's whole purpose |
| `01FD40D8` | a string global's `begin` | pointer | sample triple written by `001600D0` |
| `01FD40E0` | same string's `end` | pointer | |
| `01FD40E8` | same string's `capacity_end` | pointer | |

## 4. Data structures and formulas

```
eastl::basic_string  -- 24 bytes, three pointers, NO inline buffer
  +0x00  ptr  begin
  +0x08  ptr  end            length == end - begin
  +0x10  ptr  capacity_end   capacity == capacity_end - begin
```

```
eastl::vector  -- begin/end/capacity_end plus an INLINE allocator object
  +0x00  ptr  begin
  +0x08  ptr  end            size  == (end - begin) / elementSize
  +0x10  ptr  capacity_end
  +0x18  ---  allocator      the object itself, not a pointer to one
```

```
eastl::allocator_memory_log vtable
  +0x10  void *allocate  (self, size_t n, int flags)
  +0x18  void  deallocate(self, void *p, size_t n)      <- SIZED
```

### Construction from a C string — the exact sequence

```c
n = strlen(src) + 1;
if (n < 2) { end = 02EBA2E0; capacity_end = 02EBA2E1; }   /* shared sentinel */
else       { end = capacity_end = allocate(n); capacity_end = end + n; }
begin = end;
memmove(begin, src, n - 1);
end = begin + (n - 1);
*end = 0;
```

### Destruction guard

```c
if ((capacity_end - begin) > 1 && begin != NULL)
    deallocate(begin, (int)capacity_end - (int)begin);
```

### Vector growth, exactly

```c
size = (end - begin) / elementSize;
doubled  = (size == 0) ? 1 : size * 2;
required = size + n;
newCapacity = (required < doubled) ? doubled : required;
newBlock = allocate(newCapacity * elementSize);
...
deallocate(oldBegin, ((capacity_end - oldBegin) / elementSize) * elementSize);
```

At the site read, `elementSize` is **16** (the code shifts by 4 throughout), so this instantiation is
a vector of 16-byte elements.

### Static string initializer, exactly

```c
allocator = eastl_allocator_memory_log_ctor("EASTL basic_string");
begin = end = capacity_end = NULL;
p = allocator->allocate(payloadLen + 1, 0);
capacity_end = p + payloadLen + 1;
begin = end = p;
memmove(p, literal, payloadLen);
end = p + payloadLen;
*end = 0;
atexit(<this string's own destructor>);
```

## 5. Call chain

```
any subsystem needing text or a list
  -> EASTL_LookupByCString  001FF740
     -> eastl_allocator_memory_log_ctor   001EDF00   ("EASTL basic_string")
     -> allocator vtable +0x10  allocate
     -> memmove
  -> ... use ...
  -> allocator vtable +0x18  deallocate   (guarded by capacity > 1)

process start
  -> 58 x eastl_string_static_init        (each registers its own atexit destructor)
```

**Upstream:** everything. EASTL is a leaf dependency of the whole engine, which is why its functions
appear in the caller sets of Audio, Resource, Phyre and Script/VM documents alike.

**Do not confuse with:**

- **MSVC's short-string representation**, which *does* use the low bit of the first byte to select
  inline storage. That idiom appears in the Phyre reflection binder and is a different library.
- **`001EDF00` is tagged `Runtime.ContainerStringSupport`, not `EASTL.*`** — so the very function
  that writes the `eastl::` vtable is outside the tag family this document is scoped to. Another
  instance of the category boundary not matching the code.

## 6. Modding notes

- **Best intervention point:** the allocator vtable. Both `allocate` and `deallocate` are virtual, so
  a single vtable swap redirects every EASTL allocation in the game~~, and the name argument gives you~~
  ~~free attribution of what asked for it.~~ *(Corrected 2026-09-30, OPUS: the constructor discards the name (BS-6), so a
  hook sees no tag; attribute by the caller's return address instead.)*
- **Regenerates itself:** nothing. These are plain data structures with no cached derived state.
- **Breaks if:**
  - You free a string whose capacity is 1. That is the **shared** empty-string sentinel and every
    empty string in the process points at it.
  - You assume a short string is stored inline. It is not, in this build — every non-empty string is
    a heap allocation.
  - You pass the wrong size to `deallocate`. It is sized, and the caller recomputes it from the
    pointers rather than storing it.
  - You read `begin`/`end`/`capacity_end` as three unrelated fields of an enclosing struct.
- **Multiplayer / XIIOnline:** EASTL objects are **local heap state** and must never cross the wire —
  the pointers are meaningless in another process. Send the text, never the string.
- **Mod compatibility:** the 58 process-global strings are built from `.rdata` literals at startup;
  changing a literal changes the global, and each has its own independent destructor, so there is no
  table to keep in step.

## 7. What is not known

- [x] ~~The 12 unread `EASTL.ContainerRuntime` bodies, including the two largest (`00200E60` at 1,527 B
      and `001FF210` at 707 B). This document reads 2 of 14.~~ **BS-1 ANSWERED 2026-09-12 (FABLE): the
      tag group is JsonBox's reader and writer plus EASTL's own container helpers, and one MSVC
      body.** All fourteen were profiled by imports, callees, allocator tags and referenced globals:
      - **JsonBox (three):** `00200E60` (1,527 B) is `Value::loadFromStream` — 13 `basic_istream::get`,
        3 `putback`, 14 of the token globals BS-3 catalogued (`true` / `false` / `null` / the escapes),
        EASTL `map` / `vector` / `basic_string` construction; `00201C40` (612 B) is its string reader —
        `get` / `peek` / `putback` and the library's own diagnostic literal `Expected '"', got '` …
        `', ignoring it.`; `001FF210` (707 B) is `Value::output` — recursive, `basic_ostream::operator<<`
        (through the stream inserters `00194B00` / `001DDE10` of BK-6), five token globals, `memmove`
        escaping. `00201C40` calls `00200E60` and `00200E60` calls the value builders `002001F0` /
        `00202740` / `00201890`.
      - **EASTL container helpers (ten):** three byte-identical 467-B bodies (`001997F0`, `001A1500`,
        `001E6FD0`) construct an object holding an `EASTL vector` and two `EASTL set`s (five
        allocator-log constructions each); `001BC9D0` (693 B) and `001E71B0` (717 B) build `map` /
        `vector` members through `eh_vector_constructor_iterator`; `001FC420` (339 B) and `001FC640`
        (303 B) are `map` / `vector` operations; `001E7D30` (607 B) is the reallocating insert §3
        already names; `001FF740` (300 B) and `0020AA50` (476 B) are `basic_string` helpers over
        `memmove`.
      - **Not EASTL (one):** `00783AA0` (540 B) is MSVC's `std::vector<T>` growth — `_Xlength_error`
        with the literal `vector<T> too long` — mis-tagged into the family.
      The library inventory's `X-6` gains its JsonBox half from this: JsonBox parses an `istream`
      into EASTL-backed values, which is the sidecar `JsonData/*.json` path the console pages read.
- [x] Which EASTL container types beyond `vector` and `basic_string` are present. The tag family names
      only `BasicString` and `ContainerRuntime`, which is a classification, not an inventory.
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (BS-2), from this page's own §8 table plus
      one check:* **`list`, `set` and `map`, beyond `vector` and `basic_string`.**
      - **Why these five.** They are EASTL's default container names (`EASTL_*_DEFAULT_NAME`), and they are the only
        `EASTL `-prefixed literals in the image: `008F3CC0` `list`, `008F3CB0` `set`, `008F4120` `map`, beside `vector`
        `008C5F58` and `basic_string` `008F6600`.
      - **Each is loaded by code as the allocator constructor's name argument.** For example `001D9456` loads
        `lea rdx, "EASTL list"` and calls `001EDF00`, and the next two stores self-link the new list head (`001D9462`).
        Rip-relative load sites and functions: `vector` 67 in 56, `basic_string` 134 in 111, `set` 56 in 29, `map` 34 in
        20, `list` 15 in 10.
      - **The limit of that evidence.** A container type the game only ever builds with an explicit allocator name would
        leave no default literal. The absence of `hash_map`, `deque`, `fixed_*` and the others is therefore not proven.
        What is proven is the presence of these five.
      - **Where the names go.** They cost nothing at run time: BS-6 below shows the allocator discards the name.
- [x] ~~What the 58 process-global strings actually **are**. Each payload is a `.rdata` literal that has
      not been read out; they are 2–4 characters in the two sampled cases, which is unusually short.~~
      **BS-3 ANSWERED 2026-09-12 (FABLE): they are JsonBox's constants, instantiated four times.**
      All 58 `EASTL.BasicString.StaticInitializer` bodies were read for the literal they `memmove`
      (the first `lea` in every one is the allocator's log tag `"EASTL basic_string"` at `008F6600`,
      not the payload). **52** of them are **four identical sets of thirteen** — the JSON escape
      tokens `\b`, `\u`, `\r`, `\f`, `\n`, `\"`, `\\`, `\/`, `\t`, the keywords `true`,
      `false`, `null`, and the hex alphabet `0123456789ABCDEFabcdef` — filling the globals
      `01F830A0`–`01F83240`, `01FD3C68`–`01FD3DE8`, `01FD3E08`–`01FD3F88` and `01FD3FA8`–`01FD4128`
      (one set per translation unit that included the JsonBox header; e.g. `0015D610` → `01F830E0`
      = `null`, `001600D0` → `01FD40E8` = `true`, `0015FE00` → `01FD4028` = `\\`). The remaining **6**
      (`0015C560`, `0015C650`, `0015C7C0`, `0015C8D0`, `0015C9E0`, `0015CB10` → `01F81298`–`01F81398`)
      build **empty strings**: their literal at `01CEB638` is `""`, so `len + 1 = 1` takes the
      `jbe` path and the triple is set to the shared sentinel `02EBA2E0` / `02EBA2E1`. That is also
      why they are 228 bytes and the other 52 are 240. The "unusually short" reading was right — they
      are two-byte escape sequences and one-word keywords, the whole vocabulary a JSON writer needs.
- [x] ~~**BS-4.** Why 6 of the 58 static initializers are 228 bytes and 52 are 240.~~ **ANSWERED
      2026-09-15 (OPUS) — the conclusion above stands; the mechanism it stated did not.** All 58
      bodies were read. Every one that leas `rsi` at the `""` literal `01CEB638` is **228** bytes
      (6 of them) and every one that leas it at a real payload is **240** (52), with no crossover;
      sizes taken from the function inventory rather than re-derived. **But the empty variant does
      not omit the `memmove`** — it calls the same import (`008C2A40` → `VCRUNTIME140.dll!memmove`)
      with a length of zero. The 12 bytes are three separate savings, and they account for the
      difference exactly:
      **(1) +5** — a non-empty body leas the payload's end and start into `rax` and `rsi`
      (`48 8d 05` + `48 8d 35`, 14 B); the empty body leas only `rsi` and folds the end onto it
      with `mov eax, esi` (7 + 2 = 9 B), because begin and end are the same address.
      **(2) +3** — the length argument: `xor r8d, r8d` (3 B) against `mov r8d, 4` (6 B).
      **(3) +4** — the terminator: the empty body stores the buffer pointer and writes
      `byte [rdi] = 0` (7 + 3 = 10 B); the non-empty one computes `lea rax, [rdi + 4]`, stores
      that, and writes `byte [rax] = 0` (4 + 7 + 3 = 14 B).
      5 + 3 + 4 = 12, and 228 + 12 = 240. Both shapes keep all three calls and the same branch
      structure — the `jbe` is simply always taken in the empty case.
      *(Worked at `0015C560` (228 B) against `0015D610` (240 B, `null`); the six are `0015C560`,
      `0015C650`, `0015C7C0`, `0015C8D0`, `0015C9E0`, `0015CB10`.)*
- [x] **UQ-306.** The EASTL **version**. No version banner has been found, unlike zlib 1.2.11, libvpx 1.6.0 and
      Lua 5.2.1, all of which state their own version in the image. *(Closed 2026-09-27 as `BS-5`, OUT OF EVIDENCE
      BOUNDARY; `UQ-306` is SUPERSEDED as its duplicate. The version is stated only in EA's internal EASTL branch or the
      game's build configuration, neither of which ships. So this page names the line (the branch that carries
      `allocator_memory_log`) and not the number; the version is unanswered in fact. Pointer added 2026-09-30, OPUS.)*
      ***NARROWED 2026-09-17 (FABLE): the image holds no version, and what it does hold bounds the line, not the number.** A scan of every printable run in the executable for `eastl` or `EASTL` finds exactly eight: the six allocator names `EASTL vector` (`007A4D58`), `EASTL set` (`007D2AB0`), `EASTL list` (`007D2AC0`), `EASTL map` (`007D2F20`), `EASTL basic_string` (`007D5400`) and `EASTL` (`01BB9C78`), and the two RTTI descriptors `.?AVallocator_memory_log@eastl@@` (`01E266F8`) and `.?AVallocator@eastl@@` (`01E5C900`). The six names are the headers' default allocator names, the `EASTL_*_DEFAULT_NAME` strings built from `EASTL_DEFAULT_NAME_PREFIX`, which the library has carried across its releases, so they do not pin a version. The class `eastl::allocator_memory_log` does not appear in the public EASTL releases (the 3.x line published from 2016), so the build's EASTL is an EA-internal branch rather than a public release, which is a reading of the public tree, not a claim the image makes. No assert message, macro string or `EASTL_VERSION` value is present, so the exact number is not in the image. *(The register's live id for this box is `BS-5`; `UQ-306` is its registered duplicate.)** ~~*(NO ADMISSIBLE SOURCE (lost build), reviewed and signed 2026-09-26 by OPUS; see the register row BS-5 (UQ-306 is its duplicate).)*~~ *OUT OF EVIDENCE BOUNDARY, 2026-09-27 (FABLE, Claude Opus 5.5): FRONTIER ruled that NO ADMISSIBLE SOURCE does not extend to a lost build artefact (batch-K Extension 2026-09-27b); OPUS's signature carries, on the same four conditions. See the register row BS-5.*
- [x] Whether `allocator_memory_log` actually logs anywhere, or whether the name is retained and the
      logging compiled out.
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (BS-6):* **it does not log; the logging is
      compiled out, and the name is discarded at construction.**
      - **The constructor keeps no name.** `001EDF00` is all 14 bytes: it writes the vtable `00902720` and returns
        `this`. The name argument in `rdx` is never stored.
      - **No slot does anything but allocate.**

        | slot | body | what it does |
        |---:|---|---|
        | 1 | `001EDF10` | `_aligned_malloc(size, alignment)` (`api-ms-win-crt-heap`), tail call |
        | 2 | `001EDF80` | `_aligned_malloc(size, 16)` |
        | 3 | `001EDFE0` | `_aligned_free(p)` when `p` is non-null |
        | 4 | `0016D690` | returns the constant name `"EASTL"` (`01CDAE78`) |

      - **The only extra work is an inert record.** Each of slots 1–3 first creates, once, a 32-byte `malloc` record at
        `01F82E48` holding `0x2000000`, `0x200000`, 0 and 0. The pointer is referenced by exactly those three functions, one
        test and one store each, and nothing ever reads the record. The logging facility's state is created and never
        consulted.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The library is EASTL and the allocator class is `eastl::allocator_memory_log` | `001EDF00`'s complete 14-byte body writes the **qualified symbol** `eastl::allocator_memory_log::vftable` | 3 |
| Every string allocation is tagged `"EASTL basic_string"` | authored string literal passed at each construction site | 2 |
| `basic_string` is three pointers with no inline buffer | complete bodies of `001FF740`, `001600D0`, `0015FE00` — three globals written, no inline buffer anywhere | 1 |
| The empty string is a shared global and the `> 1` guard protects it | complete body of `001FF740`: `if (n < 2)` takes `02EBA2E0`/`02EBA2E1`, and the matching deallocate guard | 1 |
| Allocator slots `+0x10` allocate / `+0x18` deallocate, deallocate sized | complete bodies of `001FF740`, `001E7D30`, `001600D0` — three independent sites agreeing | 1 |
| Vector growth `max(size + n, size ? size*2 : 1)` | complete exact-current body of `001E7D30` | 1 |
| 58 static initializers, 52 at 240 B and 6 at 228 B, structurally identical but not byte-identical | body-extent census over the GN graph; two sampled bodies have different SHA-256s (`71e1dd63…` vs `795aded7…`) | 1 |

**Method note and a correction made in flight.** An earlier reading of this set recorded the 58
initializers as *"all exactly 240 bytes"*, which was taken from the head of a size-sorted list rather
than from the distribution. The census gives **52 at 240 and 6 at 228**. Same defect shape as pass
133's three overturns — a number correct for the rows actually looked at, generalised to the set.

**Scope note.** This document covers the **72 functions in the bare-name `EASTL.*` tag family** — the
ones that a `ThirdParty.*` census could not see, which is why the library was missing from
[`../third-party-middleware-inventory.md`](../third-party-middleware-inventory.md) entirely until
falsification pass 3. `001EDF00` is *not* in that family (it is tagged
`Runtime.ContainerStringSupport`) and is documented here anyway, because it is the function that
proves the library's identity.

**Superseded readings:** none — this is the document's first version.

## 9. Related

- [`../third-party-middleware-inventory.md`](../third-party-middleware-inventory.md) — the census that missed this library; corrected to twelve libraries, 801 functions
- [`../Bullet-Physics-Integration/phyre-to-bullet-rigid-body-materialization.md`](../Bullet-Physics-Integration/phyre-to-bullet-rigid-body-materialization.md) — the other third-party mechanism document
- [`../../22-Middleware-PhyreEngine/Animation-Channel-Binding/animation-channel-binding-and-transform-composition.md`](../../22-Middleware-PhyreEngine/Animation-Channel-Binding/animation-channel-binding-and-transform-composition.md) — uses **MSVC's** short-string idiom, deliberately contrasted in §6
- [`../../24-Compiler-And-CRT-Runtime/Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md`](../../24-Compiler-And-CRT-Runtime/Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md) — the 58 initializers are contributors to that table

## 10. Falsification pass 1 — 2026-09-03, by a session that did not write this document

Program state: GZF `2ed8affb…`, snapshot `46f02e26…`, EXE `73461d08…`. Attacked in provenance order —
the qualified symbol, the universal claim and the absence claim first, because those are the three
that carry the most and cost the least to state.

**Nothing was overturned.** One completeness gap was found and filled.

### The absence claim, which was the one worth attacking

§2 states there is **no short-string optimisation** — a negative, load-bearing on §6's advice about
hooking string destruction, and the sort of claim that is usually inferred from a struct size. A
24-byte string is **not** evidence of it: modern EASTL's SSO layout is also 24 bytes, a union whose
inline buffer occupies the same space as the three pointers.

The evidence that does settle it is the constructor's control flow. `001FF740` contains exactly one
length test:

```asm
001FF7A6  cmp   eax, 1                     ; eax = strlen(src) + 1
001FF7A9  jbe   0x1FF7D7                   ; the ONLY branch on length
001FF7B7  mov   rax, [rsp + 0x40]
001FF7BC  call  qword ptr [rax + 0x10]     ; allocate  -- taken for every n >= 2
...
001FF7D7  lea   r14, [rip + 0x2CBAB02]     ; -> 02EBA2E0   the shared sentinel
001FF7E8  lea   rax, [rip + 0x2CBAAF2]     ; -> 02EBA2E1
```

**One branch, at length 1.** No second threshold, no inline buffer, and both arms write the same
three qwords at `+0x00`, `+0x08`, `+0x10` of the string. The claim holds, and now rests on the branch
structure rather than on the size.

### The rest, attacked and confirmed

| claim | how it was attacked | result |
|---|---|---|
| `eastl::allocator_memory_log` is a genuine qualified symbol | searched the image for the RTTI type descriptor | **`.?AVallocator_memory_log@eastl@@`** — present once, namespace included |
| the empty-string sentinel is `02EBA2E0` / `02EBA2E1` | resolved both RIP displacements from the constructor's bytes | exact |
| allocate is vtable slot `+0x10` | read the call site | `call qword ptr [rax + 0x10]` |
| `001FF740` has 17 callers | edge census | **17** — exact |
| 58 static initializers, 52 × 240 B and 6 × 228 B | tag census over the ledger | **58; {240: 52, 228: 6}** — exact |
| the name literal passed to the allocator | resolved `lea rdx,[rip+0x6F6E98]` from `001FF761` | `008F6600` = `"EASTL basic_string"` |

### The gap: the allocator names five container kinds, not one

§2 quotes a single literal. The image holds **five**, and they are the whole set of `EASTL `-prefixed
literals in it:

| literal | address |
|---|---|
| `EASTL basic_string` | `008F6600` |
| `EASTL vector` | `008C5F58` |
| `EASTL set` | `008F3CB0` |
| `EASTL list` | `008F3CC0` |
| `EASTL map` | `008F4120` |

That **strengthens** §2's reading rather than weakening it: a build that ships a name-tagging
allocator and supplies five distinct tags ~~is one that can attribute allocations per container kind,~~
~~which is exactly what `allocator_memory_log` implies.~~ *(Corrected 2026-09-30, OPUS: the tags are supplied, but
the constructor drops them (BS-6), so the build cannot attribute by them; the five tags show which containers route
through the allocator and nothing more.)* It also tells a modder which containers route
through the named allocator — string, vector, set, list and map, and nothing else.

Related, and not previously stated: the allocator constructor `001EDF00` has **230 distinct callers**,
against 17 for the string constructor. **The named allocator is used far beyond strings**, which the
five literals independently predict.

### What I tried that failed to break it

- Attacked the SSO negative expecting it to rest on the 24-byte size, which would not have supported
  it. It rests on the constructor's branch structure instead.
- Attacked *"every string allocation passes the same literal"* by enumerating every `EASTL `-prefixed
  string in the image, expecting a second string-related tag. The other four are for other
  containers, so the claim is true as scoped — and the scope was narrower than the evidence.
- Checked the two sampled 240-byte initializers' size class against all 58 rather than the two.
- Ran the neighbour check first: 13 cited addresses, one shared with the unowned-code census and four
  with `OPEN-QUESTIONS.md`. No contradiction.



### Name corrected 2026-09-03 — `001FF740` is a lookup wrapper, not a constructor and not the find

Two documents named this address differently and **neither name was right**: `Map_FindByName` in one,
`eastl_string_construct_from_cstring` in the other. Decompiled and settled:

```c
uVar3 = FUN_001edf00(local_res10, "EASTL basic_string", ...);   // named allocator
do { lVar4++; } while (*(char *)(param_2 + lVar4) != '');      // inline strlen of ARG 2
if (uVar2 < 2) { puStack_38 = &DAT_02eba2e0; ... }              // shared empty sentinel
else            puStack_38 = (**(code **)(local_28[0] + 0x10))(...);  // allocate
memmove(...); *puStack_38 = 0;                                  // copy + terminate
uVar3 = FUN_001ff6b0(param_1, &local_40);                       // DELEGATE
(**(code **)(local_28[0] + 0x18))(local_28, local_40, ...);     // FREE
return uVar3;                                                   // return the DELEGATE'S result
```

> **Not a constructor: it destroys the string on the way out and returns another function's result.
> Not the find either: the lookup is `001FF6B0`.** It converts a C string to the container's string
> type, delegates, and cleans up. ~~**20 callers.**~~ *(Corrected 2026-09-30, OPUS: 17 calling functions, at 669 call
> sites, as §3 and §10 say; [`eastl_dd_check.py`](../../_index/candidates/opus-dd-eastl-0930/eastl_dd_check.py) F2.)*

**Each author saw one half of it** — the string construction at the top, or the by-name lookup it
serves — and each named the whole function after the half they were reading.

**The EASTL evidence is unaffected and this is worth stating separately from the name.** The
no-short-string-optimisation claim rests on this body's control flow — **one branch at length 1, the
shared sentinel at `02EBA2E0`, both arms writing the same three pointers** — and every one of those is
visible in the decompilation above. **The reasoning was right; the label on the function was not.**

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Presentation — CLIENT (2 edges, one fan-in).** All 2 edges are Presentation bodies reaching `001FF6B0` on this page. `FUN_001c5570` is the worked example - it is a 472-byte routine in an `0x80`-byte frame with a stack cookie and one preserved SSE register. The crossing is **one shared subject with 2 callers on that layer**, not 2 separate relationships. Edge count from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Resource — CLIENT (SWE2-EC7, batch 167, 1 edge).** The batch-167 `001A6A20` runtime `basic_string` build is called by that layer's `001A9A30` - a Resource body constructing the `"start"` literal string through the shared `001EDF00` allocator attach; the crossing is that call, not a Resource responsibility of this page.

## The `001E71B0` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`001E71B0` (717 B) — EASTL map plumbing: `00808FE4` helper registration
on `001E7710`/`001E7480` (`001E7201`), member `001E6FD0`
(`001E7214`), the `"EASTL map"` string `008F4120` (`001E7226`), two
`001EDF00` calls (`001E7256`), then three more `00808FE4`
registrations pairing `00212D90` with `00212D30`/`00212CF0`
(`001E7355`/`001E737E`), member `00212D60` (`001E738B`).

| member | role | interior |
| --- | --- | --- |
| `001E6FD0` (467 B) | map/node constructor — `(rcx, edx)`; `qword[rcx]`/`[+8]`/`[+0x10]` zeroed (`001E7002`–`001E7009`), `-2` scope mask (`001E6FE4`) | [`001E7002`](../../_index/ADDRESS-INDEX.md) |
| `00212D60` (40 B) | small ctor — `00212CC0` (`00212D69`), installs vtable `00906DA0` (`00212D6E`), `dword[rbx+0x18] = 0` (`00212D75`) | [`00212D6E`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00808FE4`, `001EDF00`, `00212CC0`,
and the `00212D90`/`00212D30`/`00212CF0` registration targets.

`001A6A20` (669 B) is a runtime `eastl::basic_string` build around the `008F67B0` literal `"start"`: `001EDF00` attaches the `allocator_memory_log` named `008F6600` (`"EASTL basic_string"`) to both stack copies, the 6-length span is allocated through the allocator vtable `+0x10`, and the result is filled from the literal before iterating `02EBA2E0`/`02EBA2E1` - the shared empty-byte this page names as the EASTL empty-string sentinel; cookie `01F44830` guards the 0x90 frame.

Interior anchor `001A6A67` (function `001A6A20`).

`001BCE30` (372 B) is an ordered `eastl::list` lower-bound the render object's `001BD840` calls: it walks the `[rcx+0x18]` node chain comparing `qword[node+0x20]` against `*rdx` (`cmp`/`cmov` lower-bound step), attaches the `008F3CC0` `\"EASTL list\"` allocator via `001EDF00` when no node owns the key, then splices a new node through `001BC8C0`/`001BD1B0` - the ordered-key insert-or-find the EASTL families share.

Interior anchor `001BCEA2` (function `001BCE30`).
