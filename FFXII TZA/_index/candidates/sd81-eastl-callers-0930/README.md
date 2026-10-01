# SD-81: what the 99 callers of the EASTL red-black tree build with it (SWE2-ORACLE, 2026-09-30)

Register row **SD-81** (owner SWE2-DATA), on
[the-ordered-container-runtime.md](../../../24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/the-ordered-container-runtime.md)
section 7: *"What the 99 callers build with the tree, and which wrappers sit between them and the six bodies."*
Assigned by OPUS. Board task `SWE2-ORACLE-SD81-EASTL-CALLERS-0930`.

This record is **static**. There is no isolated execution and no live evidence. The checker is `sd81_callers.py`. It
reads the certified image (SHA-256 `73461d08…21f8`, check A0) through `Tools/analysis-kit/gfz-scripts/retool.py`. Its
output is `sd81_callers.out` (**`FAILS 0`**; a second run is byte-identical). The per-caller table is
`sd81-callers.tsv`, written by `python -B sd81_callers.py --tsv sd81-callers.tsv`.

## The answer (SWE2-ORACLE)

**Every container instantiation that inserts through this tree is a `map` or a `set` with unique keys.** No
multimap or multiset insert path exists among the callers (checks B5–B7).

The 99 split into three kinds.

- **1 is a member:** `0016DA60` itself (the erase, calling the two rotations).
- **56 are EASTL's own insert path, instantiated 24 times.** Each of the 24 instantiations (`I01`–`I24`) has one
  **insert-unique** body (it calls `dec` + `ins`: descend, `--position`, compare with the predecessor, reject a duplicate
  through `byte [ret+8] = 0`). Sixteen of them also have an **insert-hint** body (`inc` + `ins`: validate the hint with
  `++`, fall back to the insert-unique) and an **insert-at** body (`ins` only: the parent is the caller's position
  argument). These 56 bodies *are* the container wrappers between the game and the six bodies. In EASTL source terms
  they are `DoInsertValue`/`DoInsertKey`, `DoInsertValueHint` and `DoInsertValueImpl`. Those names are **INFERENCE**
  from the library; the three roles are read from the bytes (B2–B6, G1).
- **42 are game or manager code with the container operation inlined:** 30 **erase** bodies (`inc` + `era`) and 12
  **walk** bodies (`inc` only: iteration, clear, destroy).

**Typed: 90 of the 98 non-member callers** are tied to one of the 24 instantiations. Each tie gives node size, key
compare and value layout.

- **56** are tied by code: call edges and a shared node helper.
- **31** are tied because they erase or walk **the same tree**. The tree expression resolves to the same key as one the
  instantiation's insert bodies resolve to (same global, same singleton + offset, or same RTTI class + offset). A
  value returned by an indirect call or a null-object path never ties two bodies.
- **3** are tied by **INFERENCE**:
  - `001A9ED0` shares a tree key with `001A7770`.
  - `001B67F0` inserts into an `I01` tree of the same node size on the same object.
  - `001B6990` is the only instantiation matching its node size + key.
- **8 are not tied** (see the last section).

**Located: for 81 of the 98, the tree's owner was resolved beyond the body's own `this`.** The owner is a global, a
singleton's global pointer, an RTTI class, a stack local or an array element.

### The 24 instantiations (SWE2-ORACLE)

Fifteen instantiations are reached by an allocator-name tag. The other nine are I02, I03, I05, I12, I19, I20, I22, I23
and I24.

The node size and key compare come from the insert-unique body. The value is every store and constructor call the
insert path makes on the fresh node. "Tag" means the tree was constructed with EASTL's default allocator name for that
template: `"EASTL map"` (`008F4120`) or `"EASTL set"` (`008F3CB0`). That is **proven** for the tagged trees (section F,
check F1). The set/map word for an untagged instantiation is **INFERENCE**, from value bytes versus key bytes. Type
names such as `uint32` restate the width and signedness of the compare. They are not declarations.

| inst | node | key at `+0x20` | value written into the node | container | tag | trees (owner) | same-tree erase / walk |
|---|---|---|---|---|---|---|---|
| I01 | 0x28 | qword, unsigned | the key only | `set<uint64>` | EASTL set | 57 trees: two-set pools in AsyncJobManager, AssetListManager, AsyncLoadManager, AudioFileLoadManager, AudioSeadObjectManager, the five `*AudioController` classes (+0x40/+0x78), singletons `01F81150`/`01F811E8`/`01F811F8`/`01F81200`/`01F81240`/`01F83438`, globals `01F82D80`/`01F82DB8`/`01F82F30`/`01F82F68`, an array of sets at `*[01F7F5B8]` (stride 0x38) | 19, plus 001B67F0 and 001B6990 (INF) |
| I02 | 0x28 | dword, signed | the key only | `set<int32>` (INF) | – | `this+0xB0`/`+0xE8` of job function `001A3160` | – |
| I03 | 0x38 | dword, signed | xmm + dword (to +0x34) | map (INF) | – | `this+0x490` of `001A3160` | 001A7770, 001A9ED0 (INF) |
| I04 | 0x38 | dword, signed | xmm + qword | map | EASTL map | `*[01F81168]+0x268` | 001A5980 |
| I05 | 0x28 | dword, unsigned | qword | map (INF) | – | `*[01F81168]+0x3E0` | – |
| I06 | 0x88 | qword, unsigned | key + `001A2750` copy at +0x28 (0x60 B) | map | EASTL map | `*[01F81168]+0x448` | – |
| I07 | 0x40 | string compare `001A3100` | an eastl::string-shaped object (3 qwords + allocator at +0x38) | `set<string>` | EASTL set | `*[01F81168]+0x3A0` | – |
| I08 | 0x48 | string compare `001A3100` | string + qword | map | EASTL map | `*[01F811C8]+0x8` | – |
| I09 | 0x30 | dword, unsigned | xmm (key + 8 B) | map | EASTL map | 7: font system `*[01F81200]+0x28/+0x60/+0x98`, `*[01F81150]+0x28`, `*[01F811E8]+0x20/+0x2200`, `*[01F83438]+0x20` | 0019CC50, 001B1960, 0020B840, 0020BFA0 |
| I10 | 0x48 | dword, unsigned | key + string at +0x28 | map | EASTL map | global `02EB37B8` | – |
| I11 | 0x28 | dword, unsigned | the key only | `set<uint32>` | EASTL set | a stack local of `001BAA30` | – |
| I12 | 0x58 | dword, unsigned | 3 xmm + qword | map (INF) | – | `*(this+0x8)+0x10` of `001BC190`; `001BB120`'s rdx | – |
| I13 | 0x48 | string compare `001A3100` | string + qword | map | EASTL map | `*[01F81240]+0x1C0/+0x1F8` | – |
| I14 | 0x40 | qword, unsigned | `001BC950` at +0x20 (0x20 B) | map | EASTL map | `*[01F81248]+0x20` | 001BD4A0, 001BDAC0 |
| I15 | 0x48 | string compare `001A3100` | string + dword | map | EASTL map | `*[01F81258]+0x78` | – |
| I16 | 0x48 | string compare `001A3100` | string + qword | map | EASTL map | `*[01F81258]+0x20` | 001BF230 |
| I17 | 0x30 | qword, unsigned | xmm (key + 8 B) | map | EASTL map | `*[01F811F8]+0xF30` | 001E9A30 |
| I18 | 0x30 | dword, signed | xmm (key + 8 B) | map | EASTL map | `*[01F81168]+0x4E8`, `*[01F81240]+0xB0`; also an indirect call's result `+0x58` and `001FB770`'s `this+8` (not identified) | 001A6CC0, 001BC190 |
| I19 | 0x28 | dword, signed | qword (key + adjust at +0x24) | map (INF; see K2) | – | the value `001FC420` returns: `node+0x28` of an I20 node | – |
| I20 | 0x60 | dword, signed | key + `001FBEF0` (a tree copy constructor) at +0x28 | `map<int32, map>` | (K2) | font `+0x70` | – |
| I21 | 0x48 | dword, unsigned | 2 xmm + qword | map | EASTL map | the font object `001FC060` builds, `+0x38` | – |
| I22 | 0x48 | dword, unsigned | key + `001FBFC0` at +0x28 (0x20 B) | map (INF) | – | `this+0xA8` of `001FDB50`/`001FDB90` (the `.fex` store) | – |
| I23 | 0x50 | string compare `001A3100` | `001FE570`: a string plus `001FE6B0` at +0x20 | map (INF) | – | `*(this+0x8)` of `001FF6B0` / `00200E60` | – |
| I24 | 0x60 | compare `001A1990` (MSVC `std::string`-shaped) | `00675300` (0x40 B) | map (INF) | – | globals `01F81188`, `02D3ECA8` | – |

All 24 full owner lists, with how each was reached, are in `sd81_callers.out` section G.

**The string keys, read rather than named.**

- `001A3100` takes two `{begin, end}` pairs. It `memcmp`s the shorter length, then compares lengths. The node
  helpers build that key as three zeroed qwords, an allocator through `001EDF00` at key+0x18, and a range-assign
  `001A4BF0(begin, end)`. That is the `eastl::basic_string` layout of
  [the EASTL page](../../../23-Third-Party-Libraries/EASTL/eastl-strings-containers-and-the-logging-allocator.md).
  The name is **INFERENCE**; the layout is measured.
- `001A1990` tests a capacity at +0x18 against 0x10 before choosing inline or heap storage, and takes the size from
  +0x10. That is MSVC's small-string layout. The name `std::string` is **INFERENCE**.

**Two recurring shapes, structural facts from the bytes.**

- **The two-set pool.** Most of the `I01` erase bodies move a key between two `I01` sets on one object, one set at
  `+k` and one at `+k+0x38`.
  - The shared `001BA860` (20 call sites) erases `begin()` of the first set and inserts its key into the second.
  - `002124C0` (18 call sites) finds a key in the second set, erases it and inserts it into the first.
  - Each of the five `*AudioController` classes (Music/Sep/Seb/Shout/Stream) inlines the same pair on its own
    `+0x40`/`+0x78` sets, behind virtual slots 7 and 3.
  - The meaning "free-id / used-id pool" is **INFERENCE**. The data movement is read.
- **Arrays of sets.** `0062EBC0`/`0062EC70` index `*[01F7F5B8]` by `i * 0x38`. `0x38` is the size of one EASTL
  rbtree object: compare slot, anchor `+0x08..+0x27`, size dword `+0x28`, allocator `+0x30`.

## The wrappers (SWE2-ORACLE)

- **None in front of the six.** No rip-relative reference names any of them (A3), and no caller is a thunk. The
  smallest of the 99 is 134 bytes (A4). The page's "no dispatcher" stands.
- **The 56 insert-path bodies are the wrappers.** They are listed above.
- **Six node-construction helpers sit beside the insert path, not between it and the six bodies:** `001A3190`,
  `001AB2C0`, `001AE7C0`, `001B9CF0`, `001BEA90`, `001BEB20`. Ten insert sites take their node from one of them. The
  other 80 allocate inline (B1b).
- **21 thin wrappers (≤ 48 bytes) sit directly above the 99** (section W).
  - Five are `this`-adjusting virtual slots, each `add rcx, 0x20; jmp`: `00218980`, `00219B10`, `0021B150` and
    `0021C440` are slot 7 of Music, Sep, Seb and Shout AudioController. `0021D570` is slot 3 of Music, Shout and
    Stream AudioController.
  - Four are non-virtual `add rcx, k; jmp`: `00220CD0`, `00220D30`, `002211A0`, `00221210`.
  - Eight are singleton-getter-then-tail-call forwarders: `0017F0D0`, `0017FA50`, `0017FC70`, `00180280`, `001802B0`,
    `00181610`, `001D6BB0`, `00186610`.
  - Three are small float/threshold stubs into `001A7770`.
  - One, `0062EB90`, fronts `00199DB0` for five callers.

**One count to reconcile with OC-2.**

- OC-2's "80 of 80" counts **insert sites**, and B1 reproduces all nine sizes with the page's per-size counts.
- Counted as **allocate sites** there are **81**. One insert site, `001FFD0F` in `001FFB30`, is fed by two allocates
  on two branches, `001FFC30` and `001FFCE1` (B1a).

## A contradiction this record raises (SWE2-ORACLE)

It came out of the positive control. P1 holds: the census reads the font page's `.ker` store as 0x28-byte nodes with
a signed dword key and an 8-byte value, without being told.

The same bytes contradict the page's section 3 claims that the `.ker` writer builds a **flat**
`map<rightCp, adjust>`, that the record's second dword is "saved to the stack at `001FDC15` and **never read back**",
and that the kern path is "structurally inert".

- **K1.** `001FDC10` spills `r8d` (record `+4`) to its home slot, `[rsp+0x18]` at entry. It passes that slot's
  address as the key argument of `001FC420(font + 0x70, &rec[+4])`. `001FC420` is a find-or-insert on an I20 map
  (0x60-byte nodes), and it returns `lea rax, [rbx+0x28]` at `001FC55C`, the node's value. `001FDC10` then inserts
  `rec[+0]` → `rec[+8]` into **that** value through `001FC9F0` (I19).
- **K2.** The value is itself an EASTL map. `001FC420` names a stack tree `"EASTL map"` (`001FC487`), and
  `001FBEF0` copies that tree into the pair (`001FC4E8`). `001FBEF0` is the same body the I20 node runs at
  `node+0x28`.

So the writer builds `map<int32 rec+4, map<int32 rec+0, int32 rec+8>>`.

- The nested layout the reader `001FDDD0` walks is exactly this: inner sentinel at outer `node+0x30`, inner root at
  `node+0x40`. So "the inner walk reads past the node into adjacent heap" does not follow.
- **Not settled here:** whether the writer's outer key (record `+4`, which the page calls the left / preceding glyph)
  is the same code point the reader looks up first (the current glyph). That is the page owner's to adjudicate.
- The font page and the register are not edited. This is reported to OPUS for routing.

## Proven, inference, and limits (SWE2-ORACLE)

**Proven by the bytes (static):**

- The census.
- The roles.
- The node sizes, including the nine OC-2 sizes tied to named bodies.
- The key width, signedness or compare callee.
- The value stores and constructor calls.
- Unique-key behaviour (the reject path).
- The same-tree ties.
- The allocator-name tags and their agreement with the value layout (F1).
- The owners reached through getters, stores to globals, vtable slots and constructors.
- K1 and K2.

**INFERENCE, and marked as such:**

- The EASTL method names.
- `map` or `set` for the 8 untagged instantiations other than I20. I20 is a map of maps by K1/K2.
- The type names of the string keys.
- The three inferred ties.
- The "pool" and "job" readings. `001A3160` is a function pointer that `001A9ED0` stores with its own `this` into a
  job record from AsyncJobManager `01F81100` (`001A9F4B`–`001A9F55`). Its `this` is therefore very probably
  `*[01F81168]`, the object `001A7770` also reaches at `+0x490`. That is not proven.

**The 8 untied callers, narrowed rather than typed:**

- `001ACF80`, `001C0960`: 0x48 nodes whose value destructor frees through an allocator at `node+0x38`. That narrows
  them to I08/I13/I15/I16. Neither has a direct caller, a vtable slot or a lea.
- `001FB660` (0x30 nodes, `this+8` of an object reached through I09's value), `00220B80` (AudioSeadObjectManager
  `+0x3A0`, tagged `EASTL map` by `0021E570`, 0x30 nodes) and `00223A20` (SebAudioBank `+0x58`, 0x30 nodes; its only
  shared key with I18 was an indirect call's result, which is not an identity): ambiguous among I09/I17/I18 by size.
- `001B6A70`: 0x28 nodes, ambiguous among five.
- `001A7F10`, `001FEE80`: the tree is loop-carried or passed in `rdx`, and was not resolved in the body.

**Limits:**

- The tracker keeps one load level and eight values per register. It follows at most four caller levels.
  "argument not tracked" rows are the tracker's limit, not an absence.
- Owner sets are "reached from"; one insert body serves several trees (I01: 57).
- `ctor_extent` is a lower bound (three levels of callees).
- The allocator-name follower requires the size dword and the anchor self-link in the same body, and 89 of 90 sites
  pass. The one not followed is in `001FF6B0`.
- The census covers direct calls and jumps over retool's function list. That no reference names the six (A3) is read
  over rip-relative operands only, consistent with FABLE's section 9 qword and RVA sweep.
- Static only. No isolated execution, no live observation.

## Files (SWE2-ORACLE)

- `sd81_callers.py`: the checker. It runs in about 7 s once retool's cache exists. Checks A0–A4, B1–B7, G1, F1, P1,
  K1 and K2.
- `sd81_callers.out`: its output, `FAILS 0`.
- `sd81-callers.tsv`: one row per caller. Columns: role, instantiation and how it was tied, node size and its source,
  key compare, insert kind, container reading (with its proof or the INFERENCE mark), the tree in the body, header
  owner(s), construction tag.

**Review:** SWE2-AUDIT-SPEC (`ORACLE-REQ-AUDITSPEC-SD81-0930`). SWE2-DATA restates SD-81 as the row owner
(`ORACLE-REQ-DATA-SD81-ROW-0930`).
