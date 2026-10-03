---
system: The Lua loader — what the engine will accept as a chunk
category: 23-Third-Party-Libraries
status: AUDITED
owner_layer: CodeDomain:ThirdParty.Lua; no PrimaryOwner
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: offline disassembly of the shipping EXE with capstone; function boundaries and
    code-domain tags from the GN160 export at work/graph/functions.tsv; imports resolved by
    walking the PE import directory; reachability by four instruments, each with its own
    passing positive control
last_reviewed: 2026-09-13
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-lua-loader-pass-1 - the 18-byte fingerprint reconstructs byte for byte from the instruction stream and the two globals, both of which resolve from their own displacements, so lua_Number = 4 and not-integral are measured rather than read; and every structural claim holds - 414 and 103 byte bodies, the 0x11 comparison length at 0082E4CC, one caller for the header checker, the three callers and three callees of the loader, and mode = NULL as a single instruction at 00683C5A. Two instructions the section-2 listing omits are recorded as unread, not interpreted. Nothing was executed # <- corrected 2026-10-02, OPUS - 0x11 at 0082E490+0x3C is the read length, not a comparison length; the comparison covers all 18 bytes (0082E490+0x69..+0x89)
  last_pass_kind: falsification
  crossref_clean: true
  reopened_count: 0
---

# The Lua loader — what the engine will accept as a chunk

> **`DA-3` answered.** The loader is `00683C30`, it is Phyre's own, and it passes **`mode = NULL`** —
> which means the engine will accept **plain Lua source text** as readily as precompiled bytecode.
>
> **And `DA-3`'s own stated hope is disproved**: identifying the loader does *not* convert `DA-1`
> into a static question, because the loader's callers are the same virtually-dispatched executors
> that made `DA-1` a runtime question in the first place.

## 1. What a player sees

Nothing directly — but this is the single most useful fact in the database for anyone who wants to
add behaviour to FFXII rather than change numbers in it.

**If you can get a script to the engine, you can write it in ordinary Lua text.** You do not need to
compile it first, you do not need a byte-compiler matched to the game's build, and you do not need to
reverse a bytecode format. The engine's loader looks at the first byte of whatever it is handed: if
it is the compiled-chunk marker it runs the bytecode reader, and **otherwise it runs the full Lua
parser** — which is present, complete, and wired in.

The catch is the other half, and this document is explicit about it: **whether the shipped game ever
hands the loader anything is still not established.**

## 2. The Lua build fingerprint, from the code that writes the header

`0082E490` (414 B) constructs the 18-byte precompiled-chunk header a byte at a time, so the build's
configuration can be read directly out of the instruction stream rather than guessed:

```asm
0082E4C7  mov esi, 0x61754C1B                 ; "\x1bLua"
0082E4D2  mov [rsp+0x20], esi
0082E4D6  mov [rsp+0x24], 0x04010052
0082E4DE  mov [rsp+0x28], 0x00040408
0082E4E6  mov [rsp+0x2c], eax                 ; dword from 01CCD300
          movzx edi, word [01CCD304]          ; final 2 bytes
```

Laid out as the bytes it produces:

| offset | bytes | meaning |
|---:|---|---|
| 0 | `1B 4C 75 61` | `LUA_SIGNATURE` — `"\x1bLua"` |
| 4 | `52` | `LUAC_VERSION` — **0x52, i.e. Lua 5.2** |
| 5 | `00` | `LUAC_FORMAT` — 0, the official format |
| 6 | `01` | little-endian |
| 7 | `04` | `sizeof(int)` = 4 |
| 8 | `08` | `sizeof(size_t)` = 8 |
| 9 | `04` | `sizeof(Instruction)` = 4 |
| 10 | **`04`** | **`sizeof(lua_Number)` = 4** |
| 11 | `00` | numbers are **not** integral |
| 12–17 | `19 93 0D 0A 1A 0A` | `LUAC_TAIL`, read from `01CCD300` |

> **`lua_Number` is 4 bytes, not 8.** Stock Lua 5.2 on x64 uses `double`; **this build uses `float`**.
> Every number in every FFXII Lua script is single precision — about 7 significant decimal digits,
> and integers are exact only up to 2²⁴ (16,777,216), not 2⁵³.

**That is a load-bearing fact for two different people.** Anyone producing bytecode must build their
`luac` from a Lua 5.2 configured with a 4-byte `lua_Number`, or the header check rejects it. And
anyone writing script logic should know that a counter passing 16.7 million stops incrementing.

**The header size is confirmed by the checker, not just by the writer.** ~~The comparison at `0082E490`~~
~~runs over **`0x11` = 17 bytes**~~ `0082E490` reads **`0x11` = 17 bytes** and compares all 18 *(corrected 2026-10-02, OPUS: `0082E490+0x3C` `mov r8d, 0x11` is the read length; `0082E490+0x69`..`+0x89` compare qword, qword and word, bytes 0-17, byte 0 being the `0x1B` the checker plants at `0082E490+0x5A`)* — `LUAC_HEADERSIZE - 1` — because the first byte has already been
consumed by the loader that dispatched here. 17 + 1 = 18, and the table above is 18 bytes.

## 3. The chain, end to end

```
00684D10 / 00684F60 / 00686280        Phyre script execution
    |
    v
00683C30   PhyreScript_LoadBuffer      103 B   <-- mode = NULL is set here
    |
    v
00812F70   luaL_loadbufferx             46 B
    |
    v
00810180   lua_load                    180 B
    |
    v
0081DF50   luaD_protectedparser              ; takes f_parser's ADDRESS at 0081DF7C
    |
    v
0081D790   f_parser                    356 B
    |
    +-- first byte == 0x1B --> 0082E910  luaU_undump    (bytecode)
    +-- otherwise           --> 0082BE30  luaY_parser    (SOURCE TEXT)
```

**`0081D790` has zero callers in the call graph** — it is reached only through a function pointer,
which is why no earlier pass found it. Section 6 establishes that with four instruments.

## 4. `f_parser` — the fork, and the trick in it

```c
static void f_parser (lua_State *L, void *ud)        /* 0081D790 */
{
    int c = zgetc(p->z);                             /* the first byte of the chunk */
    const char *mode = p->mode;                      /* [rbx + 0x50] */

    if (c == 0x1B) {                                 /* LUA_SIGNATURE[0] */
        if (mode && strchr(mode, 'b') == NULL) error("attempt to load a binary chunk");
        f = luaU_undump(L, p->z, &p->buff, p->name);          /* 0082E910 */
    } else {
        if (mode && strchr(mode, 't') == NULL) error("attempt to load a text chunk");
        f = luaY_parser(L, p->z, &p->buff, &p->dyd, p->name, c);   /* 0082BE30 */
    }
    ...
}
```

**One detail worth naming**, because it is the kind of thing that makes a disassembly look stranger
than it is:

```asm
0081D7DD  cmp  esi, 0x1b            ; esi = the first byte
0081D7E0  jne  0x81d811
0081D7E7  lea  edx, [rsi + 0x47]    ; 0x1B + 0x47 = 0x62 = 'b'
0081D7ED  call [008C2A10]           ; VCRUNTIME140.dll!strchr
...
0081D816  mov  edx, 0x74            ; 't'
0081D81B  call [008C2A10]
```

**The compiler derived the character `'b'` from the signature byte it had just compared against**,
rather than loading the constant — `0x1B + 0x47 = 0x62`. The `'t'` on the other branch is a plain
immediate, because there is no register holding a useful base there. The two `strchr` calls are Lua
5.2's `checkmode()`, and `008C2A10` resolves through the PE import directory to
`VCRUNTIME140.dll!strchr`.

## 5. `mode = NULL` — and why that is the whole answer

```asm
00683C5A  mov  qword ptr [rsp + 0x20], 0     ; the 5th argument to luaL_loadbufferx
00683C63  call 0x812f70                       ; luaL_loadbufferx(L, data, len, name, mode)
```

The fifth argument is the `mode` string, and Phyre passes **zero**.

> **Both `checkmode` guards are `if (mode && ...)`.** With `mode == NULL` neither guard can fire, so
> **neither form is refused.** The loader accepts precompiled bytecode and Lua source text with equal
> willingness, and the only thing that decides which path runs is the first byte of the buffer.

Had Phyre passed `"b"`, source text would be rejected and this database would be recording the
opposite conclusion. **It passes nothing, and that is a deliberate-looking choice by the engine's
authors, not an accident of the Lua build.**

The rest of `00683C30`, in full — it is only 103 bytes:

```c
bool PhyreScript_LoadBuffer(lua_State *L, Buffer *b)      /* 00683C30 */
{
    size_t      len  = *(u32 *)(b + 0x10) & 0x7FFFFFFF;   /* btr eax,31 -> r8, the size argument */
    const char *name = *(char **)(b + 0x48) - (*(u8 *)(b + 0x48) & 1);   /* -> r9, the chunk name */
    const char *data = *(char **)(b + 0x18);

    if (data == NULL) return false;                       /* silent refusal */

    if (luaL_loadbufferx(L, data, len, name, NULL) != 0) {
        FUN_00811530(L, -1, NULL);      /* the lua_tolstring shape: index -1, no length out */
        FUN_00811130(L, -2);            /* the lua_settop shape: mov edx, 0xFFFFFFFE */
        return false;
    }
    return true;
}
```

> *Corrected 2026-09-14 (FABLE):* the first version of this sketch had `len` and `name` swapped. In `luaL_loadbufferx(L,
> buff, sz, name, mode)` the size travels in `r8` and the name in `r9`. `00683C44`/`00683C57` put `+0x10 & 0x7FFFFFFF` in
> `r8` and `+0x48` minus its low bit in `r9`, as `EB-4` below already stated.
>
> **The two inner names are inferred from their argument shapes~~, not proven~~.** *(answered: `00811130` is `lua_settop`, read in full - the contract's §10 note; `00811530` stays shape-named; 2026-10-02, OPUS)* `FUN_00811530(L, -1, NULL)`
> and `FUN_00811130(L, -2)` are the `lua_tolstring` / `lua_settop` idiom for "read the error message,
> then pop it", but neither function was disassembled here. **They are written as `FUN_` above for
> that reason.**

**A null buffer returns `false` without touching Lua at all**, and **a compile error is swallowed**:
the error message is converted to a string and then popped, and the function returns `false`. Nothing
here writes it anywhere. **A syntactically invalid script fails silently as far as this function is
concerned** — ~~whatever reporting exists is in the three callers, which are not read here.~~ and no caller reports it either *(answered: `EB-4` below, 2026-09-12; 2026-10-02, OPUS)*.

The `- (*(u8 *)(b + 0x48) & 1)` ~~on the length is the small-string-optimisation tag bit being masked~~
~~off a packed length field, the same idiom this database records for EASTL strings.~~ is a tag bit subtracted off the **name pointer**, not off a length, and it is not an EASTL idiom: this build's EASTL strings carry no tag *(corrected 2026-10-02, OPUS: `00683C30+0x6`..`+0x14` put `[b+0x48]` minus its low bit in `r9`, the name; the length is `[b+0x10]` with bit 31 cleared, `00683C30+0x17`..`+0x27`, in `r8`; the EASTL page's three-pointer string, `001600D0`)*.

## 6. Reachability — four instruments, four controls

`0081D790` is reached by no `call`. That is exactly the situation in which a call-only census reports
dead code, so all four instruments were run, **and each was given a positive control that is positive
*for that instrument*.**

| instrument | control | control result | `f_parser` |
|---|---|---|---|
| `E8 call rel32` | `008216A0` (`luaV_execute`) | **3 hits** | 0 |
| `E9 jmp rel32` | `008216A0` | **1 hit** | 0 |
| code memory-operand (`lea`) | `0081D790` itself | **1 hit** | **1 — `0081DF7C`, in `0081DF50`** |
| raw data-section qword | `005A2B80` | **3 hits** (`00D2A290`, `00D2A520`, `00D2A620`) | 0 |

> **Every instrument returned a positive in this same run**, so every zero above is a statement about
> the binary and not about the tooling. `f_parser` is address-taken exactly once, by
> `luaD_protectedparser`, which hands it to the protected-call machinery — the standard Lua 5.2
> shape.

**The earlier control error is worth recording.** The first attempt used `0082E910` (`luaU_undump`)
as the control for the *qword* scan. It returned zero — correctly, because `luaU_undump` is reached
by a direct `call` and never appears as a stored pointer. **A control has to be positive for the
instrument being tested, not merely "known reachable".** Using a reachable-by-some-other-means
address as a control would have made a working scan look broken and a broken scan look working.

## 7. `DA-3` answered — and its own premise corrected

**`DA-3` asked: "What supplies a chunk, if anything does?"** and added that *"identifying the loader
would convert `DA-1` from a runtime question into a static one."*

**The loader is identified: `00683C30`.** Its three callers are `00684D10`, `00684F60` and
`00686280` — and **`00684D10` and `00686280` are two of the four executors `DA-1` already names**, the
ones the Lua bindings document reports as *"reached only by virtual dispatch"*.

> **So load and execute are the same functions, and identifying the loader moves `DA-1` not at all.**
> The chunk-supplier and the chunk-runner were never two separate unknowns that could be attacked
> from opposite ends; they are one unknown, still gated behind virtual dispatch. **`DA-1` remains a
> runtime question and a breakpoint on `00684D10` ~~remains the way to settle it~~ can only confirm the static bound.** *(answered: the contract's `DA-1`, bounded 2026-09-26 - the image holds no code that can create a `lua_State`; 2026-10-02, OPUS)*

**What `DA-3` does settle is the capability, which is the more useful half:** *if* a chunk is
supplied, it may be source text. That is now static and certain.

`00684F60` is a **third** call site not named by `DA-1`'s four-executor set~~, and is not read here~~ *(answered: read below, narrowed 2026-09-14 - PScheduler slots 0, 1 and 4 reach it and it takes `[task + 8]` as the buffer; 2026-10-02, OPUS)*.

## 8. Key addresses

| address | size | what |
|---|---:|---|
| `00683C30` | 103 B | `PhyreScript_LoadBuffer` — **passes `mode = NULL`** |
| `00812F70` | 46 B | `luaL_loadbufferx` |
| `00810180` | 180 B | `lua_load` |
| `0081DF50` | 226 B | `luaD_protectedparser`; takes `f_parser`'s address at `0081DF7C` |
| `0081D790` | 356 B | **`f_parser`** — the source/bytecode fork |
| `0082BE30` | 630 B | `luaY_parser` — the source path, called only from `f_parser` |
| `0082E910` | — | `luaU_undump` — the bytecode path, called only from `f_parser` |
| `0082E490` | 414 B | the header writer / checker; ~~17-byte compare~~ 17-byte read, 18-byte compare *(corrected 2026-10-02, OPUS: `0082E490+0x3C` read length, `0082E490+0x69`..`+0x89` compare)* |
| `008216A0` | 4,778 B | `luaV_execute` — the bytecode interpreter loop, 3 calls + 1 tail jump; interior verified 2026-09-17 (SWE2-FRONTIER): `008233F0` at [`00821733`](../../_index/ADDRESS-INDEX.md), `00821090` ×7/`0081E9C0` ×5/`00823030` ×3 opcode helpers, and the `'for' initial value must be a number` FORLOOP-prep strings |
| `00812FA0` | 776 B | `luaL_loadfilex` — the **file** loader (see §10) |
| `00814B30` | 287 B | a third `lua_load` caller, **zero callers**, not identified |
| `008C2A10` | — | `VCRUNTIME140.dll!strchr` |

### Data addresses

| address | contents |
|---|---|
| `01CCD300` | `19 93 0D 0A 1A 0A` — `LUAC_TAIL` |
| `01CCD287` | `"precompiled chunk"` |
| `01CCD2F0` | `"binary string"` |
| `01CCB888` | `"attempt to load a %s chunk (mode is '%s')"` |
| `01CCA878` | `"=(load)"` |

## 9. Modding notes

- **Write plain Lua. Do not compile it.** The parser is present and the mode is unrestricted, so
  source text is accepted wherever a chunk is accepted.
- **If you do produce bytecode, your `luac` must match this build**: Lua **5.2**, little-endian,
  `int` 4, `size_t` 8, `Instruction` 4, and **`lua_Number` 4 bytes (`float`)**. A stock x64 `luac`
  emits `lua_Number` 8 and the header check rejects it.
- **Numbers are single precision.** Integer arithmetic is exact only to 2²⁴. A frame counter, a gil
  total or an experience total above 16,777,216 will not increment by one.
- **A compile error is swallowed by `00683C30`** — it pops the message and returns `false`. Do not
  expect a syntax error to announce itself; ~~whether any caller reports it is unread~~ no caller reports it *(answered: `EB-4`, 2026-09-12; 2026-10-02, OPUS)*.
- **A null data pointer returns `false` before Lua is touched**, so an empty or unresolved script
  asset is indistinguishable from a failed compile at this level.
- **Only four of the eleven standard libraries are registered** — `math`, `bit32`, `string`,
  `coroutine` — per
  [the bindings document](../../22-Middleware-PhyreEngine/Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md).
  **Being able to compile source does not give you `print`, `pairs`, `io` or `os`.**

## 10. What is not known

- [x] **UQ-312.** **Whether the shipped game ever supplies a chunk.** ~~Unchanged by this document — see §7.~~ *(closed — the register row is WITHDRAWN.)*
  `DA-1`.
  ***NARROWED 2026-09-22 (FABLE): no PRECOMPILED chunk ships. The source case is untouched and is why this box
  stays open.***
  *Why a content scan was the missing instrument.* [The bindings page](../../22-Middleware-PhyreEngine/Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md)
  established that **no `.lua` file ships** — `lua` is not among the 48 extensions censused over the
  89,414-entry archive index. **That cannot settle `DA-1`**, because all three suppliers take the chunk from a
  field *inside* an object, never from a path: read from the bytes, `00684D10` and `00686280` both take
  `[rcx + 8]` as the source object, ~~the buffer from `[obj + 0x50]` and the length from `[obj + 0x60]` **with
  bit 0 masked off** (`00684D3F`–`00684D4E`, `006862D1`–`006862DF`), returning at once on a zero length~~ *(corrected
  2026-09-26 (FABLE, Claude Opus 5.5): `[obj + 0x50]` is the registered member `m_script`, a `PScript` pointer, and `[obj + 0x60]` is
  the tagged string `m_entryPoint`. The early return means "no entry point", not a zero length. The length is the
  `PScript`'s own `+0x10`, read inside `00683C30`; see the `UQ-313` box)*; and
  `00684F60` takes `[task + 8]` directly (`00684F76`). **An embedded chunk would never carry a `.lua`
  extension**, so only a scan of file *contents* can answer it.
  *The scan.* Every byte of all **89,414 files, 55 GB**, of the full game extract was searched for the Lua
  signature `1B 4C 75 61`. **Two matches, both coincidental**, and both inside large compressed video:
  `anx.webm` at `0x14D56B36` continues `08 1a 04 d9 …` and `vnp.webm` at `0x1BABF637` continues
  `17 70 d8 34 …`. **Neither is followed by the version byte `52`, and neither carries the Lua 5.2 header
  shape** (`52 00` then the size fields and the `19 93 0D 0A 1A 0A` tail). A four-byte signature matching
  twice in 55 GB of compressed data is what chance predicts.
  *The control, because a zero needs one.* The same pattern run against the executable returns **two hits**,
  and the second (at **file offset** `0x70DEE2` — a position in the file, not an image address) continues `c7 41 04 52` — **the version byte `52`, which is where this page's
  "Lua 5.2" reading is confirmed from the bytes rather than inferred.** So the pattern and the tool both
  return positives in the same run, and the corpus zero is a statement about the data.
  *What the signature scan does NOT establish.* `lua_load` accepts **source** as well as precompiled chunks,
  and source carries **no signature at all**. That scan bounds the precompiled case only.

  ***The source case, addressed by a second instrument — same date, same corpus.*** A source chunk has no
  signature, so it cannot be searched for directly. But it has to arrive the same way a precompiled one does:
  **two of the three suppliers read it out of a `PClassCallableMethodScript` instance** (`[rcx + 8]`, then
  `[obj + 0x50]` / `[obj + 0x60]`), so an asset would have to **name that class**. Searching all **89,414
  files** for the class name returns **zero**. **Control, same method and same corpus:** `PMesh` returns
  **2,019 files and counting** — the pass was still running when this was written, which does not matter,
  because a zero against a control already at two thousand positives is a statement about the data.
  **And the zero is not vacuous: the class is fully registered with Phyre's reflection.** It carries a
  descriptor vtable, a parent chain, a default buffer and an **instance size of `0x68`**
  ([the reflection members](../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/members/phyre-class-instance-sizes.tsv)).
  *So the machinery to deserialise one exists and nothing uses it.* ~~`0x68` also independently corroborates the
  field reading above — the buffer at `+0x50` and the length at `+0x60` both sit inside a 104-byte object.~~
  *(Corrected 2026-09-26 (FABLE, Claude Opus 5.5): the schema registers `m_script` at `+0x50` and `m_entryPoint` at `+0x60`, both inside
  the 104-byte object; the source bytes live in the `PScript` that `m_script` points to.)*

  ***Why the box stayed open until now.*** The class scan covered **two of the three suppliers**. The third,
  `00684F60`, takes its buffer from `[task + 8]` on a **`PScheduler`** task and never touches
  `PClassCallableMethodScript`, so nothing there bounded that route. Both scans also bound only what the extract
  contains; anything assembled at run time is outside them.*

  ***THE THIRD SUPPLIER IS NOW BOUNDED TOO — 2026-09-22 (FABLE), same corpus, one pass, with controls.***
  §11 records that `00684F60` is reached from **`PScheduler` slots 0, 1 and 4**, so an asset driving that
  route has to name `PScheduler` exactly as the other two have to name `PClassCallableMethodScript`.
  **Searching all 89,414 files of the full extract, 0 unreadable:**

| needle | files |
|---|--:|
| `PScheduler` — the third supplier's owner | **0** |
| `PScript` — widened | **0** |
| `PClassCallableMethodScript` — the other two, **re-run as its own control** | **0** |
| `PMesh` — control | **2,091** |

  **The control settles what the zeros mean.** `PMesh` reaches 2,091 files in the same pass, and the
  earlier pass's *“2,019 and counting”* is now complete at that figure — so the reader walks the corpus
  correctly and the three zeros are statements about the data. **So every one of the three chunk
  suppliers needs an object of a class no shipped file names.**

  ***What that does and does not settle.*** It closes the **authored** route completely, where before it
  closed two thirds of it: no shipped asset can deserialise any of the three supplier objects, so no chunk
  reaches `lua_load` by being loaded. **It does not close the box**, because the page's own residue is
  unchanged — *who fills a method descriptor's `+0x50` and a task's `+0x08`* — and an object built
  **natively at run time** carries no class name into any file and is outside every scan here. `DA-1`
  remains a runtime question and a breakpoint on `00684D10` ~~remains the way to settle it~~ can only confirm the static bound *(answered: the contract's `DA-1`, 2026-09-26; 2026-10-02, OPUS)*. *A further
  limit worth stating: the name scan works because a `.phyre` cluster stores its class names as strings;
  a non-`.phyre` file feeding a natively-constructed object would never carry the name at all.*

  ***THE CONSTRUCTION ROUTE IS NOW CLOSED FOR ALL THREE SUPPLIERS — 2026-09-22 (FABLE), and it is
  the same shape in each case.*** The scans above bound what the shipped *data* declares. This
  bounds what the *code* can build, and the two together leave no route.

  | | suppliers 1 and 2 (`00684D10`, `00686280`) | supplier 3 (`00684F60`) |
  |---|---|---|
  | owning class | `PClassCallableMethodScript::PCallerScript` | `PScripting::PScheduler` |
  | its vtable | `00D6FDB8` | `00D6FD68` |
  | code references to that vtable | **1** — `00682F04 mov [rax], r14` in `00682E30`, the stamp | **2** — `00681560` (constructor), `00681880` (destructor) |
  | callers of the constructor | **1** — `00680510`, a tail jump | **1** — `00680D80` |
  | that caller's own references | **0 code**, 2 stored: `00D6EBE0` and `00D6EC68` | **0 code**, 1 stored: `00D6F418` |
  | what those slots belong to | slot 14 of `PClassDescriptorAbstract<PClassCallableMethodScript>` (`00D6EB70`) and of `PClassDescriptorWithoutDefaultConstructor<…>` (`00D6EBF8`) | slot 10 of `PClassDescriptorWithoutDefaultConstructor<PScheduler>` (`00D6F3C8`) |

  **So in both cases the only way to build the object is to ask its class descriptor**, and the
  constructor is reachable through nothing else — each step enumerates every reference to the
  previous one, and at the top the factory has *no code reference at all*, only descriptor slots.

  > **And no shipped asset ever asks.** The census recorded above finds **177 declared class names
  > across all 35,984 clusters**, none of them `PScheduler`, `PScript`, `PScriptCallbackHandler`
  > or `PClassCallableMethodScript`, and a cluster instantiates only what its own table declares.
  > **So the descriptors are never asked, the constructors never run, and none of the three
  > supplier objects exists at any point in the shipped game.** *This is the same conclusion `R-5`
  > reaches for the scheduler, by the same method, extended to the other two.*

  > **Why the row still stays open.** A native caller holding a descriptor could invoke the create
  > slot without any of this showing — that is `DA-1`'s standing bound, and it is unchanged. For
  > `PScheduler` that bound is now enumerated (its descriptor is the static `02E41370`, whose 19
  > referencing sites are the CRT's init and teardown plus fifteen inside the scripting module).
  > **The equivalent enumeration for `PClassCallableMethodScript`'s two descriptors has not been
  > run, and is the next step for this row.** **NATIVE/STATIC.**
- [x] **UQ-313.** **What the three callers of `00683C30` pass as the buffer**, and where it comes from. `EB-1`.
  **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5) (as `EB-1`; this id was already folded onto it): all three hand `00683C30` a
  `PScript` object, and no shipped asset can supply one.** Control: [`script_class_census.py`](../../_index/candidates/eb1-script-source/script_class_census.py) (5 checks, FAILS 0).
  - **The callable-method callers.** `00684D10` and `00686280` pass `PClassCallableMethodScript::m_script`, the
    schema-registered `PScript` pointer at `+0x50`. They are gated on the tagged `m_entryPoint` string at `+0x60`.
    The narrowing below calls these the buffer and its length; the schema names them.
  - **The scheduler caller.** `00684F60` passes its task's `+8`, with `rdx` unchanged from `00684F76` to the call at
    `00684FBC`.
  - **What `00683C30` reads.** From the `PScript` it takes the source bytes at `+0x18`, their size as dword `+0x10`
    with bit 31 cleared, and the chunk name as the tagged `m_sourceName` at `+0x48`
    (`00683C36`–`00683C4E`).
  - **Where it comes from.** `PScript` has no vtable. Its instances are made by its reflection descriptor, and no
    shipped `.phyre` namespace declares `PScript` or `PClassCallableMethodScript`: 35,984 files, 19 distinct pools,
    128 classes (control: `PMesh` and `PAssetReference` are found). Whether code builds one through the descriptor
    at run time is `UQ-312`'s question, which stays open.
  ~~`00684F60` in particular is a call site no prior pass names.~~ **Corrected 2026-09-14:** `DA-3`
  names all three — `00684D10` / `00684F60` / `00686280` — on **2026-09-08**, four days before this
  bullet's own last review. **The question itself stands**: `DA-3` gives the chain and that
  `00683C30` passes `mode = NULL`; it does not say what any caller passes as the *buffer*, which is
  what is asked here.
  *Narrowed 2026-09-14 (FABLE), from the three bodies:* the classes are already identified on [the bindings page](../../22-Middleware-PhyreEngine/Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md).
  - **`00684D10` and `00686280`** are slots 1 and 2 of `PClassCallableMethodScript::PCallerScript`. Both take the
    **method's own source object**: `rcx = [this + 8]`, then the buffer `[rcx + 0x50]` (`00684D37`–`00684D3B`,
    `006862C9`–`006862CD`). Each returns without loading when the qword at `[rcx + 0x60]`, less its low bit, is zero
    (`00684D3F`–`00684D4E`, `006862D1`–`006862DF`).
  - **`00684F60`** is reached from `PScheduler` slots 0, 1 and 4 (`00685140`, `00685560`, `006853C0`). It takes
    `[task + 8]` as the buffer (`00684F76`) and returns 7 when that is null, and 1 when `L` is null.
    `00685140` starts from the first task of the list it is given (`rbx = [rdx]`, `00685183`), publishes itself as the running scheduler at
    `02E41050` (refusing with `0x17` if one is already running, `00685168`–`0068517C`), and passes each task's
    `+0x20` dword as the third argument (`00685207`).
  - **The `lua_State` is not the caller's own.** All three paths take a free 40-byte entry from a scheduler's pool:
    the running scheduler `[02E41050]` (for `00685140`, itself), or `[02E41020]`, which `00686280` also tries. The
    pool has count `+0x58`, capacity `+0x48 & 0x7FFFFFFF` and array `+0x50`. They
    `memcpy` the entry's template (`+0x18`, size `+0x10 & 0x7FFFFFFF`) into its destination `+0x08`, and use its
    `+0x20` as `L` (`00684D5A`–`00684DBB`, `006862E7`–`0068635D`, `006851C5`–`006851FC`).

  **So the buffer is a source object owned by a script method descriptor or by a scheduler task.** It is never
  read from a file here, which agrees with the bindings page's finding that no `.lua` ships. **Still open:** who
  fills a method descriptor's `+0x50` and a task's `+0x08`, which is `UQ-312`'s question seen from the data side.
- [x] ~~**Whether `luaL_loadfilex` (`00812FA0`) is reachable from engine code.** It is the file-system
  loader; its callers are `00814A70`, `00814C50` and `00829320`, none traced here.~~ **`EB-2` ANSWERED
  2026-09-12 (FABLE): no** — the three callers are `loadfile`, `dofile` and a `package` searcher, all
  library-table entries that are never opened (see `EB-3` below and `R-4`). The engine cannot load a
  `.lua` file from disk.
- [x] ~~**`00814B30`** (287 B), the third `lua_load` caller, with **zero callers** — presumably a
  registered C function reached through a Lua table, but not identified.~~ **`EB-3` ANSWERED
  2026-09-12 (FABLE): it is `load`**, the entry at `01CCA460` of the base library's `{name, function}`
  table (`collectgarbage` `008147B0`, `dofile` `00814C50`, `error`, `getmetatable`, `ipairs`,
  `loadfile` `00814A70`, **`load` `00814B30`**, `next`, `pairs`, `pcall`, `print`, …), and that table is
  opened only by `luaopen_base` `00814F90`, which sits in the `loadedlibs` table nothing references
  (R-4) — so `load` is never registered and the function is dead in the shipped build. The same
  settles **`EB-2`**: `luaL_loadfilex`'s three callers are `loadfile` and `dofile` (base library) and
  `00829320`, an entry of the function-pointer array at `01CCC998` beside `008293F0` — the `package`
  library's searchers, opened only by `luaopen_package` `00828D30` in the same unreferenced table.
  **The file-system loader is not reachable from engine code.**
- [x] ~~**Whether `00683C30` reports a compile failure anywhere.** It swallows the message; the three
  callers were not read.~~ **`EB-4` ANSWERED 2026-09-12 (FABLE): no.** `00683C30(L, source)` hands
  the source's buffer `+0x18` and length `+0x10 & 0x7FFFFFFF` to `luaL_loadbufferx` (`00812F70`);
  on any non-zero status it discards the message (`00811530(L, −1, 0)`, `00811130(L, −2)`) and
  returns 0, else 1. Its three callers test that byte and take a silent exit: `00684D10` and
  `00686280` unlink the entry they had just added (count `+0x58` decremented when the last entry is
  the one being built, `00684F12`–`00684F37`, `006867D4`–`006867FF`) and return 0; `00684F60`
  returns the status 9 it loaded before the call (`00684FB7`, `0068511F`–`00685136`). No call to any
  logging, message or debug-output function lies on the three paths — a failed compile is
  invisible.
- [x] **The parser's own seven functions** (`00829810`, `0082A280`, `0082AAD0`, `0082AD40`,
  `0082BC50`, `0082BE30`, `0082D5C0`, plus `0082F000`) are identified as a family by their error
  strings but **only `0082BE30` is placed in the chain**; none is read. `EB-5`.
  *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (EB-5):* **seven are Lua 5.2.1 `lparser.c`
  functions and the eighth is a code generator.** Each is named against the 5.2.1 source by two things: its own strings
  and its place in the call graph, whose neighbours are themselves identified by string. No body was read line by line.
  **Neighbours used as anchors:**
  - `0081D790` `f_parser`: `attempt to load a %s chunk (mode is '%s')`;
  - `0082A660` `exprstat`: `syntax error`;
  - `0082CCC0` `simpleexp`: `cannot use '...' outside a vararg function`;
  - `0082B2A0` `funcargs`: `function arguments expected`;
  - `0082B180` `forstat`: `'=' or 'in' expected`;
  - `0082AFA0` `fornum`: `(for index)`, `(for limit)`, `(for step)`;
  - `0082C220` `new_localvar`: `local variables` limit.

  | function | name | evidence |
  |---|---|---|
  | `0082BE30` | `luaY_parser` (with `mainfunc` / `statlist` inlined) | only caller `f_parser`; calls `0082D130` twice, `statlist`'s `return` case and its loop |
  | `0082D130` | `statement` | called only from `luaY_parser` |
  | `00829810` | `assignment` | `C levels`, `syntax error`, `%s expected`, and it calls itself (the `,` left-hand-side list) |
  | `0082A280` | `constructor` (with `errorlimit` inlined) | `items in a constructor`, `too many %s (limit is %d) in %s`; callers `funcargs` and `simpleexp` |
  | `0082D5C0` | `suffixedexp` | callers `assignment`, `exprstat` and `simpleexp`; calls `funcargs` |
  | `0082AD40` | `forlist` | `(for generator)`, `(for state)`, `(for control)`; caller `forstat` |
  | `0082AAD0` | `forbody` | callers exactly `forlist` and `fornum` |
  | `0082BC50` | `localstat` (by call shape) | caller `statement`; calls `new_localvar` and the list routine `0082D470` twice. `localfunc` would call `body` rather than an expression list. |
  | `0082F000` | not a parser function: an `lcode.c` helper | no strings; its seven callers are all in the code generator (`0082F660`…`00830410`) |

  `0082F000`'s exact `lcode.c` name was not recovered.

## 11. Evidence

| claim | evidence | tier |
|---|---|---|
| The build is Lua 5.2 with `lua_Number` = 4 bytes | the 18 header bytes read out of the writer's immediates at `0082E4C7`–`0082E4E6`, with `LUAC_TAIL` verified at `01CCD300` | 1 |
| Header size 18, checker ~~compares 17~~ reads 17 and compares 18 *(corrected 2026-10-02, OPUS: `0082E490+0x3C` `mov r8d, 0x11` is the read length; `0082E490+0x69`..`+0x89` compare qword, qword and word, bytes 0-17, byte 0 being the `0x1B` the checker plants at `0082E490+0x5A`)* | `mov r8d, 0x11` at `0082E4CC`; 17 + the pre-consumed signature byte | 1 |
| `f_parser` forks on the first byte | `cmp esi,0x1b` / `jne` at `0081D7DD`, with `luaU_undump` on one arm and `luaY_parser` on the other | 1 |
| `'b'` is computed as `0x1B + 0x47` | `lea edx,[rsi+0x47]` at `0081D7E7` with `rsi` proven `0x1B` by the branch | 1 |
| `008C2A10` is `strchr` | PE import directory walked to the named thunk | 1 |
| **`mode` is `NULL`** | `mov qword ptr [rsp+0x20], 0` at `00683C5A`, immediately before the call | 1 |
| `f_parser` is address-taken exactly once | four-instrument scan, **each instrument with its own passing positive control** | 1 |
| `luaV_execute` is called | 3 `E8` + 1 `E9` from `0081D900`, `0081E5A0`, `0081E920` | 1 |
| The loader's callers are two of `DA-1`'s executors | `edges.tsv`, cross-read against the bindings document's own list | 1 |
| Whether a chunk is ever supplied | ~~**not established — and this document does not narrow it**~~ bounded statically, not closed *(answered: `UQ-312` narrowed and the contract's `DA-1` bound, 2026-09-26; 2026-10-02, OPUS)* | — |
| What the three callers pass | ~~**not read**~~ a `PScript` object *(answered: `EB-1`, 2026-09-26; 2026-10-02, OPUS)* | — |
| Whether `luaL_loadfilex` is reachable | ~~**not traced**~~ no *(answered: `EB-2`, 2026-09-12; 2026-10-02, OPUS)* | — |

## 12. Related

- [`../../22-Middleware-PhyreEngine/Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md`](../../22-Middleware-PhyreEngine/Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md)
  — the interpreter's identification as 5.2, the `PhyreObject` metatable, the four registered
  libraries, and the executors `DA-1` is about.
- [`../third-party-middleware-inventory.md`](../third-party-middleware-inventory.md)
  — the category's inventory of linked middleware.
- [`../EASTL/eastl-strings-containers-and-the-logging-allocator.md`](../EASTL/eastl-strings-containers-and-the-logging-allocator.md)
  — ~~the packed-length idiom `00683C30` uses on its buffer~~ the untagged string layout, which `00683C30`'s tagged name pointer is not *(corrected 2026-10-02, OPUS: the low bit comes off the name, `00683C30+0x6`..`+0x14`)*.

## 13. Falsification pass 1 — 2026-09-13 (OPUS)

*(Static only. Nothing executed, and no chunk was loaded or run.)*

### ✔ The build fingerprint reconstructs byte for byte

The eighteen bytes were rebuilt **from the instruction stream and the two globals**, not read from the
page: `mov esi, 0x61754C1B`, `mov [rsp+0x24], 0x04010052`, `mov [rsp+0x28], 0x00040408`, then the
dword at `01CCD300` and the word at `01CCD304`. Both globals resolve from their own displacements —
`0082E4AE` → `01CCD300` and `0082E4B9` → `01CCD304`, exactly the two addresses §2 names — and
`01CCD300` holds `19 93 0D 0A 1A 0A`.

```
1b 4c 75 61 52 00 01 04 08 04 04 00 19 93 0d 0a 1a 0a
```

Field by field: signature `"\x1bLua"`, version **`0x52`**, format `0`, little-endian, `sizeof(int)`
**4**, `size_t` **8**, `Instruction` **4**, **`lua_Number` 4**, integral **0**. **Every cell of §2's
table, including the two that carry the argument** — a 4-byte `lua_Number` and numbers that are not
integral.

### ✔ The rest of the structural claims

| claim | measured |
|---|---|
| `0082E490` is 414 B | **414** |
| ~~the comparison runs over `0x11` = 17 bytes~~ the read runs over `0x11` = 17 bytes and the comparison over 18 *(corrected 2026-10-02, OPUS: `0082E490+0x69`..`+0x89`)* | **`mov r8d, 0x11` at `0082E4CC`** — the page gives the length without its address |
| `0082E490`'s callers | **one**, `0082E910` |
| `00683C30` is 103 B | **103** |
| **`mode = NULL`** | **`mov qword ptr [rsp + 0x20], 0` at `00683C5A`**, the fifth argument to `call 00812F70` |
| `00683C30`'s three callers are `00684D10`, `00684F60`, `00686280` | **exactly those three** |
| the loader swallows the message | its **only three callees** are `00812F70`, `00811530`, `00811130` — load, then the two stack operations on the error path |

**`mode = NULL` is the page's load-bearing fact and it is one instruction**, at a named address, with
the packed-length idiom (`movzx eax, byte [rdx+0x48]` / `and eax, 1` / `sub r9, rax`) visible three
instructions earlier. Nothing in the 103 bytes contradicts it and there is no second write to that
slot.

### ○ Two instructions §2's listing leaves out

Between the constants and the call, `0082E4CC` sets `r8d = 0x11` (the length §2 discusses) and
`0082E4EA` writes the single byte `0x1B` to a **different** stack slot, `[rsp+0x38]`. After
`call 0x81C6A0` returns zero, `0082E4F9`–`0082E503` loads `[rsp+0x20]` and `[rsp+0x38]` and compares
them as **qwords**. **That second step is not described anywhere on the page**~~, and it is **not read~~
~~here either**~~ *(answered: read and executed in the contract, 2026-09-12 - all eighteen bytes compared in three groups, `0082E490+0x69`..`+0x89`; 2026-10-02, OPUS)* — recorded so that a reimplementer copying §2's listing knows the block continues.

**Not claimed.** Whether the shipped game ever hands the loader a chunk — `DA-1` is untouched, and
this pass **ran nothing**. What `0081C6A0`, `00811530` or `00811130` are. The four executors, cited
from the Lua-bindings page rather than re-derived. Nothing was executed.

## The `00686280` exclusive subtree — all 4 members bound (SWE2-FRONTIER, followup queue)

`00686280` (1,448 B) is `PCallerScript` slot 2 — the second of the three
executors `DA-1` names. The body reads as: scheduler context from
`[02E41050]`/`[02E41020]` (`006862E7`/`006862F3`), `00861EBA` copy of the
script name, then a long arg-push and call sequence — `005CDAA0` tag reads,
`00811130`/`008113D0`/`00811470`/`00811530` stack pushes, the `0062FF50`–
`00630420` `lua_*` block (pcall/gettop/setfield family), and the
`0080F420`/`00810340`/`00810640` core calls — with `006811B0` and `00681010`
doing the load-and-dispatch at `00686412`/`006865C6`, and `006810B0`/
`00681130` extracting the return value.

| member | role | interior |
| --- | --- | --- |
| `00681010` (145 B) | the tagged-object dispatch — `006372A0`, `or rax, 1`, compare against `rcx`; match → `rbx = [rax-8]` (header) then `00682D20(rdi, rbx, rax)`, no-match → `0080F420(rdi, 1)` + `00810620`; always returns 1 | [`0068102D`](../../_index/ADDRESS-INDEX.md) |
| `006810B0` (122 B) | the float return extractor — gate fail → 0; else `00811640(rsi, -1, 0)` (stack top), `00811130(rsi, -2)` (pop), and `movss` into `dword[rdi+8]` with `[rdi] = 0` when `rdi` is set (`006810F2`–`00681111`) | [`00681102`](../../_index/ADDRESS-INDEX.md) |
| `00681130` (126 B) | the double twin — same shape but `cvtss2sd` then `movsd` into `qword[rdi+8]` (`00681182`–`00681195`) | [`00681182`](../../_index/ADDRESS-INDEX.md) |
| `006811B0` (78 B) | the load-and-dispatch — `rdi = [rdx]` buffer nonnull → `00682D20(rbx, rdi, 006372A0(rbx))`; else `0080F420(rbx, 1)` + `00810620` (`006811C0`–`006811F9`) | [`006811CB`](../../_index/ADDRESS-INDEX.md) |

Shared callees deliberately outside the census: `006372A0` (tag getter),
`00682D20` (the real call), `0080F420`/`00810620` (error raise + path), the
`0062FF50`–`00630420` `lua_*` block, `00811130`/`008113D0`/`00811470`/
`00811530`/`00811640`, `005CDAA0`, `00630490`, `00861EBA`.

## Cross-subsystem neighbours — SWE2-STRUCT (pass-22 dispositions)

- **Resource - CLIENT (69 edges).** `0062FF50`, `00630420`, `00630490` are called by bodies filed to Resource: `005850F0`, `00585270`, `005853F0`, `00585570` (+59 more) - shared machinery across the layer boundary, no shared ownership.

## Homed bodies: functions reached only indirectly whose callees this page cites (OPUS, 2026-10-02, F homing)

*No page cited these functions and none of their callers is documented: they are reached by table or pointer dispatch or through undocumented callers. Each one calls something this page documents, which the sentence names. Each sentence states what the body does (access and representation, not purpose); the anchors are instructions inside it that do it. Drafted locally and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-the-lua-loader-and-what-it-accepts-homing-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0063C450` | 68 B | calls `008113D0(rdx, -1)` and keeps whether it returned non-zero, calls `00811130(rdx, -2)`, then stores that flag as a byte at `[r8]` | `0063C468`, `0063C46B`, `0063C47A`, `0063C47D`, `0063C482` |
