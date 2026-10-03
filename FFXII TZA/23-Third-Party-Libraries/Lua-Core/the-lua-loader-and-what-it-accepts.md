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

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-the-lua-loader-and-what-it-accepts-cloudint-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `005928F0` | 109 B | with `c` = byte `r8+0xc`, `a` = dword `+8` of qword `[r9+8]` and `b` = dword `+0x48` of qword `[r9+0x10]`, it starts the source at `rcx` + (`a` when `c` is non-zero, else `b`) and the destination at `rdx` + (`b` when `c` is non-zero, else `a`), then for dword `[r8]` elements stores each source byte, sign-extended, as a word, stepping the source by dword `r8+4` and the destination by dword `r8+8` | `00592920`, `0059292A`, `00592940`, `00592946`, `00592950` |
| `00595C00` | 108 B | with `c` = byte `r8+0xc`, `a` = dword `+8` of qword `[r9+8]` and `b` = dword `+0x48` of qword `[r9+0x10]`, it starts the source at `rcx` + (`a` when `c` is non-zero, else `b`) and the destination at `rdx` + (`b` when `c` is non-zero, else `a`), then for dword `[r8]` elements copies each source byte to a destination byte, stepping the source by dword `r8+4` and the destination by dword `r8+8` | `00595C30`, `00595C3A`, `00595C50`, `00595C56`, `00595C5F` |

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted, opus-the-lua-loader-and-what-it-accepts-ee-1003)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-the-lua-loader-and-what-it-accepts-ee-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `001600D0` | 240 B | constructs the string object at `01FD40D8`: its allocator name via `001EDF00(rsp+0x30, 'EASTL basic_string')` and `001EDF00(01FD40F0, that)`, begin/end/capacity qwords `01FD40D8`/`01FD40E0`/`01FD40E8` zeroed, then for the length 5 taken from `008FCDA4` - `008FCDA0` + 1 a buffer from the allocator's vtable slot `+0x10`(01FD40F0, 5, 0) (begin = end = buffer, capacity = buffer+5; a length of 1 or less would use the one-byte buffer `02EBA2E0` instead), `memmove(buffer, 008FCDA0 'true', 4)`, end = buffer+4 and a 0 byte there; it tail-jumps to `00808B90(008A80A0)` | `001600E6`, `00160141`, `00160196`, `001601AE`, `001601BB` |
| `005850F0` | 383 B | when dword `02CAB018` is above the epoch dword at `+4` of this thread's TLS block (index dword `02EAED3C`) it runs `008092FC(02CAB018)` and, when `02CAB018` is then -1, fills the node at `02CAAFE8`: qwords `+0`/`+8`/`+0x10` = the node, qword `+0x18` = the second and `+0x20` = the first of two `0062FF50()` results, qword `+0x28` = `00595C00`, registers `00808B90(008A83E0)` and closes with `0080929C(02CAB018)`; on every path it then sets bit `0x1` of qword `+0x10`, sets `+0`/`+8` to `01F2CDA0`, and walks the tree from the root qword `01F2CDB8` comparing (qword `+0x18`, qword `+0x20`) with each node's pair: an equal pair returns without linking; otherwise the node becomes child `+0` (smaller) or `+8` (larger) of the last node visited (or the root when the tree is empty), its qword `+0x10` = that parent + 1, and it calls `0067F700(01F2CDA0, node)` | `00585128`, `00585145`, `00585184`, `005851BC`, `0058525F` |
| `00585270` | 383 B | when dword `02CAB050` is above the epoch dword at `+4` of this thread's TLS block (index dword `02EAED3C`) it runs `008092FC(02CAB050)` and, when `02CAB050` is then -1, fills the node at `02CAB020`: qwords `+0`/`+8`/`+0x10` = the node, qword `+0x18` = the `0062FF50()` result and `+0x20` = the `0062FFC0()` result (called first), qword `+0x28` = `00595C00`, registers `00808B90(008A83F0)` and closes with `0080929C(02CAB050)`; on every path it then sets bit `0x1` of qword `+0x10`, sets `+0`/`+8` to `01F2CDA0`, and walks the tree from the root qword `01F2CDB8` comparing (qword `+0x18`, qword `+0x20`) with each node's pair: an equal pair returns without linking; otherwise the node becomes child `+0` (smaller) or `+8` (larger) of the last node visited (or the root when the tree is empty), its qword `+0x10` = that parent + 1, and it calls `0067F700(01F2CDA0, node)` | `005852A8`, `005852C5`, `00585304`, `0058533C`, `005853DF` |
| `005853F0` | 383 B | when dword `02CAB088` is above the epoch dword at `+4` of this thread's TLS block (index dword `02EAED3C`) it runs `008092FC(02CAB088)` and, when `02CAB088` is then -1, fills the node at `02CAB058`: qwords `+0`/`+8`/`+0x10` = the node, qword `+0x18` = the `0062FF50()` result and `+0x20` = the `00630030()` result (called first), qword `+0x28` = `005928F0`, registers `00808B90(008A8400)` and closes with `0080929C(02CAB088)`; on every path it then sets bit `0x1` of qword `+0x10`, sets `+0`/`+8` to `01F2CDA0`, and walks the tree from the root qword `01F2CDB8` comparing (qword `+0x18`, qword `+0x20`) with each node's pair: an equal pair returns without linking; otherwise the node becomes child `+0` (smaller) or `+8` (larger) of the last node visited (or the root when the tree is empty), its qword `+0x10` = that parent + 1, and it calls `0067F700(01F2CDA0, node)` | `00585428`, `00585445`, `00585484`, `005854BC`, `0058555F` |
| `00585570` | 383 B | when dword `02CAB0C0` is above the epoch dword at `+4` of this thread's TLS block (index dword `02EAED3C`) it runs `008092FC(02CAB0C0)` and, when `02CAB0C0` is then -1, fills the node at `02CAB090`: qwords `+0`/`+8`/`+0x10` = the node, qword `+0x18` = the `0062FF50()` result and `+0x20` = the `006300A0()` result (called first), qword `+0x28` = `005928F0`, registers `00808B90(008A8410)` and closes with `0080929C(02CAB0C0)`; on every path it then sets bit `0x1` of qword `+0x10`, sets `+0`/`+8` to `01F2CDA0`, and walks the tree from the root qword `01F2CDB8` comparing (qword `+0x18`, qword `+0x20`) with each node's pair: an equal pair returns without linking; otherwise the node becomes child `+0` (smaller) or `+8` (larger) of the last node visited (or the root when the tree is empty), its qword `+0x10` = that parent + 1, and it calls `0067F700(01F2CDA0, node)` | `005855A8`, `005855C5`, `00585604`, `0058563C`, `005856DF` |
| `00682E30` | 272 B | for each of dword `[rcx+0x70]` records starting at qword `[rcx+0x58]` (stride dword `+0x38` of qword `[rcx+0x50]`): self-links the record's qwords `+0`/`+8` (when non-null), stores qword `+0x58` with bit `0x1` cleared to qword `+0x18`, and, when that value is non-null, appends the record to the circular list whose sentinel is at qword `+0x10` + 0x90 unless an entry already in that list has a non-null qword `+0x18` string equal (byte compare to the terminator) to the record's; then stores `00D6FDB8` and the record to qwords `+0x30`/`+0x38` and `record+0x30` to qword `+0x28`; returns 0 | `00682E58`, `00682E8F`, `00682EC3`, `00682EF7`, `00682F10` |
| `006853C0` | 416 B | returns 0x13 unless it finds, in the list from qword `[rcx+0x40]` (next at qword `+0`), an entry `e` whose qwords `+8` and `+0x10` equal `rdx` and `r8`, and an index `i` below dword `[rdx+0x20]` AND 0x7FFFFFFF whose name (qword `i` of qword `[rdx+0x28]` with bit `0x1` cleared) is `r9` or a byte-equal string (`r9` pointing at an empty string counts as null); then, with qword `02E41058` = `e` around the call and 0 after it, the result is `006852B0(e, i)` when qword `e+0x30` is non-null, else, when dword `[rcx+0x58]` is below dword `[rcx+0x48]` AND 0x7FFFFFFF, it takes the next 0x28-byte slot `s` of qword `[rcx+0x50]` (incrementing `+0x58`), calls `00861EBA(qword s+8, qword s+0x18, dword s+0x10 AND 0x7FFFFFFF)` and `00684F60(e, qword s+0x20, i)`, and gives the slot back when it is still the last; returns the result | `0068540A`, `00685451`, `006854AE`, `00685502`, `00685518` |
| `00685560` | 373 B | returns 0x17 when qword `02E41050` is non-null; otherwise stores `rcx` there and, for each entry `e` of the list from qword `[rcx+0x40]` (next at qword `+0`) whose dword `+0x28` is not 1, word `+0x24` is non-zero and (word `+0x26` + `edx`) is a multiple of word `+0x24`: with qword `02E41058` = `e` around the call, `r` = `006852B0(e, dword e+0x20)` when qword `e+0x30` is non-null, else (only when a 0x28-byte slot of qword `[rcx+0x50]` is free below dword `+0x48` AND 0x7FFFFFFF) `00861EBA(qword s+8, qword s+0x18, dword s+0x10 AND 0x7FFFFFFF)` then `r` = `00684F60(e, qword s+0x20, dword e+0x20)` with the slot given back when still last; a non-zero `r` zeroes word `e+0x24`; finally it calls `00685B70(rcx)`, zeroes qword `02E41050` and returns 0 | `00685588`, `006855D5`, `006855F8`, `00685667`, `00685698` |
| `00810340` | 263 B | takes the error-handler offset as 0 for `r9d` = 0, else `0080F300(rcx, r9d)` - qword `[rcx+0x38]`, and the call slot `f` = qword `[rcx+0x10]` - (`edx`+1)*16; when the sixth argument is non-null and word `[rcx+0x44]` is 0, it fills the record `c` = qword `[rcx+0x20]` (qword `+0x38` = sixth argument, dword `+0x30` = fifth, qword `+0x28` = `f` - qword `[rcx+0x38]`, byte `+0x48` = byte `[rcx+0x49]`, qword `+0x40` = qword `[rcx+0x78]`), stores the offset to `[rcx+0x78]`, sets bit `0x10` of byte `c+0x22` around `0081D900(rcx, f, r8d, 1)`, then clears it and restores `[rcx+0x78]`, with result 0; otherwise the result is `0081DB20(rcx, 0080F2E0, &{f, r8d}, f - qword [rcx+0x38], offset)`; when `r8d` is -1 it raises qword `+8` of qword `[rcx+0x20]` to qword `[rcx+0x10]`; returns the result | `00810367`, `00810394`, `008103DA`, `008103E3`, `00810417` |
| `008113D0` | 148 B | resolves stack index `edx` to a 16-byte value slot (positive: qword `[qword [rcx+0x20]]` + idx*16, or the nil slot `01CCB510` when not below qword `[rcx+0x10]`; negative above 0xFFF0B9D8: qword `[rcx+0x10]` + idx*16; 0xFFF0B9D8: qword `[rcx+0x18]` + 0x40; below: with `v` = qword `[qword [rcx+0x20]]`, qword `[v]` + (0xFFF0B9D8 - idx + 1)*16, or `01CCB510` when dword `v+8` is 0x16 or the index exceeds byte `+0xA` of qword `[v]`); returns 0 when the slot's dword `+8` is 0, or is 1 with dword `+0` zero, and 1 otherwise | `008113E9`, `0081140E`, `0081141D`, `0081144A`, `00811456` |
| `00811470` | 190 B | resolves stack index `edx` to a 16-byte value slot (positive: qword `[qword [rcx+0x20]]` + idx*16, or the nil slot `01CCB510` when not below qword `[rcx+0x10]`; negative above 0xFFF0B9D8: qword `[rcx+0x10]` + idx*16; 0xFFF0B9D8: qword `[rcx+0x18]` + 0x40; below: with `v` = qword `[qword [rcx+0x20]]`, qword `[v]` + (0xFFF0B9D8 - idx + 1)*16, or `01CCB510` when dword `v+8` is 0x16 or the index exceeds byte `+0xA` of qword `[v]`); when the slot's dword `+8` is not 3 it calls `00823220(slot, rsp+0x20)` and, if that returns null, stores 0 to dword `[r8]` (when `r8` is non-null) and returns 0; otherwise it stores 1 to dword `[r8]` (when non-null) and returns the float `+0` of the slot (or of the converted value) truncated to an integer | `00811492`, `008114F1`, `008114FC`, `00811518`, `00811522` |
| `00811530` | 263 B | resolves stack index `edx` to a 16-byte value slot (positive: qword `[qword [rcx+0x20]]` + idx*16, or the nil slot `01CCB510` when not below qword `[rcx+0x10]`; negative above 0xFFF0B9D8: qword `[rcx+0x10]` + idx*16; 0xFFF0B9D8: qword `[rcx+0x18]` + 0x40; below: with `v` = qword `[qword [rcx+0x20]]`, qword `[v]` + (0xFFF0B9D8 - idx + 1)*16, or `01CCB510` when dword `v+8` is 0x16 or the index exceeds byte `+0xA` of qword `[v]`); when the low 4 bits of its dword `+8` are not 4 it calls `00823280(rcx, slot)`, which on 0 makes it store 0 to qword `[r8]` (when non-null) and return 0, and otherwise is followed by `0081A8A0(rcx)` when qword `+0x18` of qword `[rcx+0x18]` is above 0 and a fresh `0080F300(rcx, edx)`; it then stores qword `+0x10` of the slot's object to `[r8]` (when non-null) and returns the slot's object + 0x20 | `00811557`, `008115C3`, `008115CA`, `008115FF`, `0081161D` |
| `00811640` | 190 B | resolves stack index `edx` to a 16-byte value slot (positive: qword `[qword [rcx+0x20]]` + idx*16, or the nil slot `01CCB510` when not below qword `[rcx+0x10]`; negative above 0xFFF0B9D8: qword `[rcx+0x10]` + idx*16; 0xFFF0B9D8: qword `[rcx+0x18]` + 0x40; below: with `v` = qword `[qword [rcx+0x20]]`, qword `[v]` + (0xFFF0B9D8 - idx + 1)*16, or `01CCB510` when dword `v+8` is 0x16 or the index exceeds byte `+0xA` of qword `[v]`); when the slot's dword `+8` is not 3 it calls `00823220(slot, rsp+0x20)` and, if that returns null, stores 0 to dword `[r8]` (when `r8` is non-null) and returns 0.0; otherwise it stores 1 to dword `[r8]` (when non-null) and returns the float at `+0` of the slot (or of the converted value) in `xmm0` | `00811662`, `008116C1`, `008116CC`, `008116EE`, `008116F4` |
| `00812FA0` | 776 B | with `t` = `0080FD00(rcx)` + 1, pushes `=stdin` (`008105C0`) and reads `__acrt_iob_func(0)` when `rdx` is null, else pushes `@` + `rdx` (`00810540`) and opens `fopen(rdx, 'r')`, a null file returning `00811F50(rcx, 'open', t)`; it drops a leading EF BB BF (the three bytes at `01CCA2A4`, read by `getc`; a partial match keeps the bytes in a stack buffer), skips a first line starting `#` (appending one 0xA), and on a first byte 0x1B with a name reopens with `freopen(rdx, 'rb', f)` (null: `00811F50(rcx, 'reopen', t)`) and repeats both skips; the byte then in hand (unless -1) joins the buffer, `r` = `00810180(rcx, 008120F0, &state, 00811530(rcx, -1, 0), r8)`; it `fclose`s a named file, and when `ferror` was set calls `00811130(rcx, t)`, pushes `cannot %s %s: %s` with `read`, the name past its first byte and `strerror(*_errno())`, calls `00810D20(rcx, t)` and returns 7, else calls `00810D20(rcx, t)` and returns `r` | `00812FEE`, `0081307A`, `0081310F`, `008131E7`, `00813263` |
| `00814B30` | 287 B | with `n` = `0080FD00(rcx)`, `s` = `00811530(rcx, 1, &len)` and mode `m` = `00813380(rcx, 3, 'bt', 0)`: when `s` is non-null the status is `00812F70(rcx, s, len, 00813380(rcx, 2, s, 0), m)`; otherwise it takes the name `00813380(rcx, 2, '=(load)', 0)`, calls `00812740(rcx, 1, 6)` and `00811130(rcx, 5)`, and the status is `00810180(rcx, 00814E60, 0, name, m)`; a zero status returns 1, after `00810730(rcx, 4)` and `00811180(rcx, -2, 1)` when `n` is at least 4; a non-zero status calls `00810620(rcx)` and `0080FEE0(rcx, -2)` and returns 2 | `00814B5B`, `00814B74`, `00814BA6`, `00814BEF`, `00814C14` |
| `0081C6A0` | 181 B | copies `r8` bytes to `rdx` from the buffer whose remaining count is qword `[rcx]` and cursor qword `[rcx+8]`: while bytes remain to copy, an empty buffer is refilled by calling qword `[rcx+0x10]`(qword `[rcx+0x20]`, qword `[rcx+0x18]`, &size) (count = size, cursor = the returned pointer); a null pointer or zero size returns the number of bytes still uncopied; each pass copies min(remaining, count) bytes with `00861EBA` and advances both sides; returns 0 when all were copied | `0081C6C2`, `0081C6D5`, `0081C71E`, `0081C725`, `0081C72A` |
| `0081D900` | 149 B | increments word `[rcx+0x46]`; at exactly 200 it calls `0081D3A0(rcx, 'C stack overflow')` (which does not return), and at 225 or more it loads `edx` = 6 and `rcx` for a call that straddles the end of the recorded extent; otherwise it increments word `+0x44` when `r9d` is 0, calls `008216A0(rcx)` when `0081DCD0(rcx, rdx, r8d)` returns 0, decrements word `+0x44` (when `r9d` is 0) and word `+0x46`, and calls `0081A8A0(rcx)` when qword `+0x18` of qword `[rcx+0x18]` is above 0 | `0081D90A`, `0081D939`, `0081D945`, `0081D957`, `0081D983` |
| `0081E5A0` | 445 B | raises an error (sets qword `[rcx+0x10]` = `rdx`, stores `s` = `0081EF90(rcx, message)` to qword `[rdx]` with dword `+8` = byte `s+8` OR 0x40, advances `+0x10` by 0x10, calls `0081D9A0(rcx, 0)` when fewer than 0x10 bytes remain below qword `+0x30`, then `0081E2C0(rcx, -1)`) with `C stack overflow` when word `+0x46` is 200 or more, with `cannot resume non-suspended coroutine` when byte `+0xA` is 0 and qword `+0x20` is not `rcx+0x80`, and with `cannot resume dead coroutine` when byte `+0xA` is neither 0 nor 1; for byte 0 it tail-jumps to `008216A0(rcx)` unless `0081DCD0(rcx, rdx-0x10, -1)` is non-zero; for byte 1 it clears that byte, sets qword `c+0` of record `c` = qword `[rcx+0x20]` to qword `[rcx+0x38]` + qword `c+0x28`, and then either calls `008216A0(rcx)` (bit `0x1` of byte `c+0x22` set) or, when qword `c+0x38` is non-null, sets bit `0x8` of that byte and byte `c+0x49` = 1, calls it, and passes qword `[rcx+0x10]` - result*16 to `0081DC10` (when it is null, `0081DC10` gets the incoming `rdx`); both then call `0081E920(rcx, 0)` | `0081E5B9`, `0081E603`, `0081E657`, `0081E6B8`, `0081E70E` |
| `0081E920` | 147 B | until qword `[rcx+0x20]` is `rcx+0x80`, takes the record `c` it points at: when bit `0x1` of byte `c+0x22` is set it calls `008229F0(rcx)` and `008216A0(rcx)`; otherwise it raises qword `c+8` to qword `[rcx+0x10]` when word `c+0x20` is -1, sets byte `c+0x49` = 1 when bit `0x20` of byte `+0x22` is clear, rewrites that byte as (byte AND 0xCF) OR 8, calls qword `c+0x38`(rcx) and passes qword `[rcx+0x10]` - result*16 to `0081DC10(rcx, ...)` | `0081E940`, `0081E964`, `0081E974`, `0081E988`, `0081E992` |
| `0081E9C0` | 224 B | while the list at qword `[rcx+0x60]` has a head `u` whose qword `+0x10` is not below `rdx`: makes qword `u+0` the new head; when (byte `u+9` XOR 3) AND (byte `+0x54` of qword `[rcx+0x18]` XOR 3) is 0 it unlinks `u` through qwords `+0x18`/`+0x20` (only when qword `u+0x10` is not `u+0x18`) and calls `00823670(rcx, u, 0x28, 0)`; otherwise it unlinks it, copies the qword and dword at qword `u+0x10` into `u+0x18`/`u+0x20`, points qword `u+0x10` at `u+0x18`, pushes `u` on the list at qword `+0x60` of qword `[rcx+0x18]` and calls `0081A350(that, u)` | `0081E9F4`, `0081EA16`, `0081EA40`, `0081EA71`, `0081EA80` |
| `00821090` | 285 B | takes each of `r8` and `r9` as a number when its dword `+8` is 3, or when its low 4 bits are 4 and `0081C300(object+0x20, qword object+0x10, &n)` converts it (a stack copy {float `n`, 3} is used); when both are numbers it stores `0081BCF0(fifth argument - 6, first float, second float)` to float `[rdx]` and 3 to dword `[rdx+8]`; otherwise it returns when `00820E00(rcx, r8, r9, rdx, fifth argument)` is non-zero and else calls `0081D240(rcx, r8, r9)` | `008210B2`, `008210D9`, `0082115A`, `00821164`, `00821195` |
| `00823030` | 493 B | for up to 100 rounds with `t` = `rdx`: when `t`'s dword `+8` is 0x45 it takes `s` = `0081F4A0(h, r8)` for `h` = qword `[t]` and, unless `s` is empty (dword `+8` 0) and `h`'s qword `+0x10` table (bit `0x2` of its byte `+0xA` clear) yields a handler from `00823520(that, 1, qword +0x128 of qword [rcx+0x18])`, uses `s` (or `0081F700(rcx, h, r8)` when `s` is the nil slot `01CCB510`): copies the 16-byte value at `r9` into it, zeroes byte `h+0xA` and calls `0081A170(rcx, h)` when that value has bit `0x40` of its dword `+8`, its object byte `+9` AND 3 is non-zero and byte `h+9` has bit `0x4`, and returns; otherwise the handler is `00823560(rcx, t, 1)` (dword `+8` 0 loads `rcx`, `t` and `index` for a call that straddles the end of the recorded extent); a handler whose low 4 type bits are 6 is pushed with `t`, `r8` and `r9` (calling `0081D9A0(rcx, 0)` when stack room is short) and called by `0081D900(rcx, top-0x40, 0, bit 0x1 of byte +0x22 of qword [rcx+0x20])`; any other handler becomes `t`; after 100 rounds it calls `0081D3A0(rcx, 'loop in settable')` | `00823060`, `00823073`, `008230A0`, `008230C3`, `008231F2` |
| `008233F0` | 290 B | with mask byte `[rcx+0x48]` and record `c` = qword `[rcx+0x20]`: when bit `0x8` is set and dword `+0x50` is 0 it reloads `+0x50` from dword `+0x4C` and notes a count event; when bit `0x80` of byte `c+0x22` is set it clears it and returns; a count event calls `0081DA20(rcx, 3, -1)`; with bit `0x4` of the mask it takes `pc` = (qword `c+0x38` - code qword `+0x18`) / 4 - 1 of the prototype at qword `+0x18` of qword `[qword [c]]`, the line dword `pc` of qword `+0x28` (0 when null), and calls `0081DA20(rcx, 2, line)` when `pc` is 0, qword `c+0x38` is not above qword `[rcx+0x28]`, or the line differs from the one at that older position; it then stores qword `c+0x38` to `[rcx+0x28]` and, when byte `[rcx+0xA]` is 1, sets dword `+0x50` = 1 (count event), steps qword `c+0x38` back by 4, sets bit `0x80` of byte `c+0x22`, stores qword `[rcx+0x10]` - 0x10 to qword `c+0` and calls `0081E2C0(rcx, 1)` | `0082340A`, `00823438`, `00823464`, `008234CF`, `008234FB` |
| `00828D30` | 764 B | gets the registry subtable `_CLIBS` (`00812B70(rcx, 0xFFF0B9D8, ...)`), gives it a new table holding the closure `00828A80` as `__gc` and sets that as its metatable; creates the package table (`0080F740(rcx, 0, 2)`), fills it from `01CCC940` (`008135B0`) and `00828870(rcx)`, and stores `searchers`; for `path` (environment `LUA_PATH_5_2`, else `LUA_PATH`, by `getenv`) and `cpath` (`LUA_CPATH_5_2`, else `LUA_CPATH`): when a variable is set and registry `LUA_NOENV` is false it rewrites `;;` to `;` 0x1 `;` and 0x1 to the default with `00812C10`, else pushes the default (`!\lua\?.lua;...` or `!\?.dll;!\loadall.dll;.\?.dll`), then calls `008295D0(rcx)` and stores the field; it stores `config` (10 bytes at `01CCCB98`), `loaded` (`_LOADED`) and `preload` (`_PRELOAD`), registers the functions at `01CCC970` into the registry's index-2 table with the package table as their one upvalue (`008109F0`, `00810730(rcx, -2)`, `008135B0(.., 1)`), pops one value and returns 1 | `00828D4E`, `00828DD7`, `00828E40`, `00828F6C`, `00829005` |
| `00829320` | 204 B | takes the name `n` = `00812500(rcx, 1, 0)`, reads field `path` of index 0xFFF0B9D7 (`0080FA50`) and `p` = `00811530(rcx, -1, 0)`, raising `00812960(rcx, "'package.%s' must be a string", 'path')` when `p` is null; `f` = `00829460(rcx, n, p, '.', '\\')`; a null `f` returns 1, otherwise it tail-jumps to `008287F0(rcx, 00812FA0(rcx, f, 0) == 0, f)` | `00829339`, `00829350`, `0082937C`, `0082939D`, `008293C6` |
| `00829810` | 594 B | requires dword `[rdx+8]` to be 7, 8 or 9 (else `syntax error`); on token dword `[rcx+0x10]` = 0x2C it calls `00824260(rcx)` and `0082D5C0(rcx, &v)` for a new list node linked to `rdx`; when `v`'s dword `+0` is not 9 it retargets earlier nodes of kind 9 whose byte `+0xF`/`+0xE` match `v` (byte `+0xF` = 7, byte `+0xE` = byte `+0x44` of qword `[rcx+0x30]`) or, for kind-7 `v`, whose word `+0xC` matches, and on any change emits `0082F450(fs, 0 or 5, that byte, v's dword +4, 0)` and `008300E0(fs, 1)`; then `00829E10(fs, word +0x46 of qword [rcx+0x38] + r8d, 200, 'C levels')` and recursion with `r8d`+1; on 0x3D it reads `0082D470` expressions separated by 0x2C (`0082F860` between them) and, when their count `n` equals `r8d`, calls `00830300(fs, &e)` and stores `e`, otherwise calls `00829770(rcx, r8d, n, &e)` and lowers byte `fs+0x44` by `n` - `r8d` when `n` is larger; the stored value (by `00830410(fs, rdx+8, &e)`) is otherwise {6, byte `fs+0x44` - 1, -1}; other tokens raise `%s expected` for 0x3D | `0082983E`, `0082986D`, `00829908`, `00829945`, `008299EE` |
| `0082A280` | 840 B | emits `pc` = `0082F450(fs, 0xB, 0, 0, 0)` (fs = qword `[rcx+0x30]`), sets `rdx` to {dword 0xB, dword `pc`, qword -1}, calls `0082F860(fs, rdx)` and requires token dword `[rcx+0x10]` 0x7B (else `%s expected`); it then reads fields until 0x7D, separated by 0x2C or 0x3B: a pending list item is flushed with `0082F860` and, at 50 pending, `00830250(fs, dword rdx+4, count, 50)`; token 0x5B, or 0x120 followed by 0x3D (`008241A0`), goes to `0082C6E0`, any other to `0082D470` with the array count capped at 0x7FFFFFFD (`too many %s (limit is %d) in %s`); it calls `00829D70(rcx, 0x7D, 0x7B, line)`, flushes the rest (kinds 0xC/0xD through `00830350(fs, &v, -1)` and a -1 count), and writes `0081BFC0`(array count) << 23 and (`0081BFC0`(hash count) AND 0x1FF) << 14 into instruction `pc` | `0082A2CB`, `0082A309`, `0082A3D5`, `0082A3FE`, `0082A4C9` |
| `0082A660` | 158 B | calls `0082D5C0(rcx, &v)`; when token dword `[rcx+0x10]` is 0x3D or 0x2C it calls `00829810(rcx, &{0, v}, 1)`; otherwise, when `v`'s dword `+0` is not 0xC it calls `00824330(rcx, 'syntax error')`, and when it is it rewrites dword `v.+4` of the code array qword `+0x18` of qword `[qword [rcx+0x30]]` as (dword AND 0xFF807FFF) OR 0x4000 | `0082A685`, `0082A697`, `0082A6AD`, `0082A6B2`, `0082A6D2` |
| `0082AAD0` | 619 B | with fs = qword `[rcx+0x30]`: activates 3 locals (byte `fs+0x42` += 3, and each one's entry in qword `+0x30` of qword `[fs]`, indexed through the word list at qword `[qword +0x50 of qword fs+0x18]`, gets dword `+8` = dword `fs+0x28`); requires token 0x103 (else `%s expected`) and calls `00824260`; `p` = `0082F470(fs, 0x21, edx, 0x1FFFE)` when the dword fifth argument is non-zero, else `0082FB30(fs)`; links a stack block record into qword `fs+0x20`, activates `r9d` more locals the same way, calls `008300E0(fs, r9d)`, opens a second block, calls `0082D3B0(rcx)` and `0082B9A0` twice, and `0082FE20(fs, p)`; the loop instruction is `0082F470(fs, 0x20, edx, 0x1FFFE)` for a non-zero fifth argument, else `0082F450(fs, 0x22, edx, 0, r9d)`, `0082F960(fs, r8d)` and `0082F470(fs, 0x23, edx+2, 0x1FFFE)`; it calls `0082FDE0(fs, that, p+1)` and `0082F960(fs, r8d)` | `0082AAFA`, `0082AB6F`, `0082AC70`, `0082ACB7`, `0082ACE7` |
| `0082AD40` | 591 B | with fs = qword `[rcx+0x30]` and `b` = byte `fs+0x44`: declares locals through `0082C220` for `(for generator)`, `(for state)` and `(for control)` (strings from `008241C0` with lengths 15, 11 and 13) and for `rdx`, then one more for each token 0x2C followed by a token 0x120 (qword `[rcx+0x18]`; a missing 0x120 raises `%s expected`); requires token 0x10C (else `%s expected`), records the line dword `[rcx+4]`, reads `0082D470` expressions separated by 0x2C (`0082F860` between them) and adjusts them to 3 values (kinds 0xC/0xD through `00830350` and `008300E0`, otherwise `0082F860` and, for a shortfall, `008300E0` and `0082FBF0(fs, register, shortfall)`); then calls `0082F320(fs, 3)` and `0082AAD0(rcx, b, line, names - 3, 0)` | `0082AD7B`, `0082ADE2`, `0082AE0A`, `0082AED8`, `0082AF0F` |
| `0082AFA0` | 466 B | with fs = qword `[rcx+0x30]` and `b` = byte `fs+0x44`: declares locals through `0082C220` for `(for index)`, `(for limit)` and `(for step)` (strings from `008241C0` with lengths 11, 11 and 10) and for `rdx`; requires token 0x3D and then 0x2C (each else `%s expected`, after `00824260`), reading an expression with `0082D470` and `0082F860` after each; a third expression follows a further 0x2C, otherwise it emits `0082F490(fs, byte fs+0x44, 0082FCB0(fs, 1.0))` and `008300E0(fs, 1)`; then calls `0082AAD0(rcx, b, r8d, 1, 1)` | `0082AFD9`, `0082B034`, `0082B064`, `0082B0CD`, `0082B105` |
| `0082B180` | 280 B | links a stack block record into qword `+0x20` of fs = qword `[rcx+0x30]` (byte `+0x42` of fs, words `+0x28`/`+0x18` of qword `+0x50` of qword `fs+0x18`, byte `+0xE` = 1), calls `00824260` and requires token 0x120 (else `%s expected`), takes the name qword `[rcx+0x18]` and calls `00824260`; on token 0x3D it calls `0082AFA0(rcx, name, edx)`, on 0x2C or 0x10C `0082AD40(rcx, name)`, and on any other token `00824330(rcx, "'=' or 'in' expected")`; then it calls `00829D70(rcx, 0x106, 0x108, edx)` and `0082B9A0(fs)` | `0082B195`, `0082B1E5`, `0082B21E`, `0082B22B`, `0082B23F` |
| `0082B2A0` | 372 B | reads call arguments into a stack descriptor `a` (fs = qword `[rcx+0x30]`): token 0x28 calls `00824260` and, unless the next token is 0x29 (`a` kind 0), reads `0082D470` expressions separated by 0x2C (`0082F860` between) and calls `00830350(fs, &a, -1)`, then `00829D70(rcx, 0x29, 0x28, r8d)`; token 0x7B calls `0082A280(rcx, &a)`; token 0x121 sets `a` = {4, `00830510(fs, qword [rcx+0x18])`, -1} and calls `00824260`; any other raises `function arguments expected`; with `b` = dword `[rdx+4]` the count is -1 for kinds 0xC/0xD, else (after `0082F860` for a non-zero kind) byte `fs+0x44` - `b` - 1; it emits `0082F450(fs, 0x1D, b, count+1, 2)`, sets `rdx` to {0xC, that pc, -1}, calls `0082F960(fs, r8d)` and sets byte `fs+0x44` = `b`+1 | `0082B2CB`, `0082B2E7`, `0082B310`, `0082B3C6`, `0082B3E8` |
| `0082BC50` | 472 B | declares one local per name: repeatedly requires token 0x120 (else `%s expected`), takes qword `[rcx+0x18]`, calls `00824260` and `0082C220(rcx, name)`, continuing after each token 0x2C; on token 0x3D it reads `0082D470` expressions separated by 0x2C (`0082F860` between), otherwise none; it adjusts them to the name count (kinds 0xC/0xD through `00830350` and `008300E0`, otherwise `0082F860` and, for a shortfall, `008300E0` and `0082FBF0(fs, register, shortfall)`), then adds the count to byte `+0x42` of qword `[rcx+0x30]` and gives each new local's entry dword `+8` = dword `+0x28` of that record | `0082BC80`, `0082BC9F`, `0082BCC2`, `0082BD62`, `0082BDDC` |
| `0082BE30` | 630 B | creates `c` = `0081ECD0(rcx, 1)` and pushes it (dword type 0x46; `0081D9A0(rcx, 0)` when stack room is short), creates `p` = `0081ED30(rcx)` into qword `c+0x18` with qword `p+0x48` = `0081EF90(rcx, fifth argument)`, zeroes dwords `+8`, `+0x18` and `+0x28` of `r9`, and sets up a stack lexer state with `008242A0(rcx, &ls, rdx, qword p+0x48, dword sixth argument)` and a stack function state; it sets byte `p+0x7A` = 2, pushes `0081F6B0(rcx)` (type 0x45), opens a block, sets byte `p+0x79` = 1, calls `0082C3D0(&fs, env name, &{7, 0})` and `00824260(&ls)`, runs statements with `0082D130` until token 0x104..0x106, 0x115 or 0x11E (a token-0x112 statement ends the list), requires 0x11E (else `%s expected`), calls `00829F50(&ls)` and returns `c` | `0082BE61`, `0082BE70`, `0082BEEF`, `0082BFF9`, `0082C054` |
| `0082C220` | 233 B | with fs = qword `[rcx+0x30]` and the list `d` = qword `[rcx+0x50]`: takes `r` = `0082C8C0(rcx, rdx)`; when dword `d+8` + 1 - dword `fs+0x3C` exceeds 200 it raises `too many %s (limit is %d) in %s` with `local variables`, 200 and `main function` or `function at line %d`; when dword `d+8` + 2 exceeds dword `d+0xC` it grows qword `[d]` with `008235B0(qword [rcx+0x38], qword [d], d+0xC, 2, 0x7FFFFFFD, 'local variables')`; then stores word `r` at index dword `d+8` of qword `[d]` and increments `d+8` | `0082C23F`, `0082C250`, `0082C27C`, `0082C2A2`, `0082C2B6` |
| `0082CCC0` | 391 B | fills the descriptor at `rdx` from token dword `[rcx+0x10]` (a jump table) and then calls `00824260(rcx)`: 0x11F gives {5, dword `[rcx+0x18]`, -1}; 0x121 {4, `00830510(fs, qword [rcx+0x18])`, -1}; 0x10E, 0x114 and 0x107 give kinds 1, 2 and 3 with -1; 0x118 gives {0xD, `0082F450(fs, 0x26, 0, 1, 0)`, -1} but raises `cannot use '...' outside a vararg function` when byte `+0x79` of qword `[fs]` is 0; 0x7B tail-jumps to `0082A280(rcx, rdx)`, 0x109 calls `00824260` and tail-jumps to `00829B10(rcx, rdx, 0, dword [rcx+4])`, and any other token tail-jumps to `0082D5C0(rcx, rdx)` (fs = qword `[rcx+0x30]`) | `0082CCD6`, `0082CD2F`, `0082CDA9`, `0082CDC8`, `0082CE21` |
| `0082D130` | 349 B | with `l` = dword `[rcx+4]`, calls `0082A5D0(rcx)` and dispatches on token dword `[rcx+0x10]` (a jump table): 0x3B calls `00824260`; 0x10B `0082B7F0(rcx, l)`; 0x116 `0082DA80(rcx, l)`; 0x103 `00824260`, `00829A70` and `00829D70(rcx, 0x106, 0x103, l)`; 0x108 `0082B180(rcx, l)`; 0x111 `0082C9A0(rcx, l)`; 0x109 `0082B420(rcx, l)`; 0x10D `00824260` then `00824260` and `0082BB40` when the next token is 0x109, else `0082BC50`; 0x11D `00824260` and `0082B890(rcx, 0082D410(rcx), l)`; 0x112 `00824260` and `0082CB10`; 0x102 and 0x10A `0082B730(rcx, 0082FB30(fs))`; any other `0082A660(rcx)`; then it sets byte `+0x44` of fs = qword `[rcx+0x30]` to its byte `+0x42` and decrements word `+0x46` of qword `[rcx+0x38]` | `0082D140`, `0082D14B`, `0082D20D`, `0082D25B`, `0082D272` |
| `0082D470` | 331 B | calls `0082A5D0(rcx)`; for token 0x23, 0x2D or 0x10F (operators 2, 0 and 1) it takes the line dword `[rcx+4]`, calls `00824260`, recurses `0082D470(rcx, rdx, 8)` and calls `00830010(fs, operator, rdx, line)`, otherwise `0082CCC0(rcx, rdx)`; then, with `op` = `0082B570(token)`, while `op` is not 0xF and the byte `01CCCFA8[op*2]` is above `r8d`, it calls `00824260`, `0082FAE0(fs, op, rdx)`, `next` = `0082D470(rcx, &v2, byte 01CCCFA8[op*2+1])` and `0082FE40(fs, op, rdx, &v2, line)`, continuing with `next`; it decrements word `+0x46` of qword `[rcx+0x38]` and returns the last `op` (fs = qword `[rcx+0x30]`) | `0082D49B`, `0082D4E8`, `0082D4F9`, `0082D52B`, `0082D57C` |
| `0082D5C0` | 448 B | calls `0082C650(rcx, rdx)` and then, while token dword `[rcx+0x10]` selects a case (a jump table; fs = qword `[rcx+0x30]`, line = dword `[rcx+4]` at entry): 0x2E calls `0082A700(rcx, rdx)`; 0x5B calls `0082F7F0(fs, rdx)`, `00824260`, `0082D470(rcx, &k, 0)` and `0082F8E0(fs, &k)`, requires 0x5D (else `%s expected`), calls `00824260` and `0082FAA0(fs, rdx, &k)`; 0x3A calls `00824260`, requires 0x120 (else `%s expected`), calls `00824260` and `00830140(fs, rdx, &{4, 00830510(fs, name), -1})` and then `0082B2A0(rcx, rdx, line)`; 0x28, 0x7B and 0x121 call `0082F860(fs, rdx)` and `0082B2A0(rcx, rdx, line)`; any other token returns | `0082D5E7`, `0082D62F`, `0082D687`, `0082D6DB`, `0082D6F6` |
| `0082E910` | 243 B | takes the chunk name `r9` past its first byte when that byte is `@` or `=`, `binary string` when it is 0x1B, else `r9` as is; calls `0082E490(&{rcx, rdx, r8, name})`, creates `c` = `0081ECD0(rcx, 1)` and pushes it (dword type 0x46; `0081D9A0(rcx, 0)` when stack room is short), stores `p` = `0081ED30(rcx)` to qword `c+0x18` and calls `0082E350(&state, p)`; when dword `p+0x50` is 1 it returns `c`, otherwise it creates `c2` = `0081ECD0(rcx, that count)` with qword `c2+0x18` = `p`, stores it over the pushed slot (type 0x46) and returns `c2` | `0082E926`, `0082E95D`, `0082E96A`, `0082E9B4`, `0082E9CD` |
| `0082F000` | 460 B | calls `0082EEF0(rcx, rdx, r8d)` and, for kind dword `[rdx]` 0xA, `0082F500(rcx, rdx+8, dword rdx+4)`; when dwords `+8` and `+0xC` differ it walks both jump lists (code qword `+0x18` of qword `[rcx]`; each jump's controlling instruction is the previous one when the byte `01CCCCD0`[its low 6 bits] is negative; next = pc + 1 + (instruction >> 14) - 0x1FFFF, ending at -1) and, if any controlling instruction's low 6 bits are not 0x1C, emits (after `0082FB30(rcx)` unless the kind is 0xA) `0082F360(rcx, r8d << 6 OR 0x4003)` and `0082F360(rcx, r8d << 6 OR 0x800003)` (dword `+0x2C` = dword `+0x28` before each) and calls `0082F500(rcx, rcx+0x30, that jump)`; then it calls `00830540` for list `+0xC` and list `+8` with the current pc, `r8d` and the position of the emitted false and true load respectively (-1 when none was emitted); finally `rdx` becomes {6, `r8d`, -1, -1} | `0082F012`, `0082F07A`, `0082F135`, `0082F187`, `0082F1BD` |
| `0082F660` | 288 B | calls `0082F8E0(rcx, rdx)`; for kinds 1, 2 and 3 with dword `[rcx+0x34]` at most 0xFF it adds a constant with `0082EA10(rcx, key, value)` (kind 1: key {qword `[rcx+8]`, type 0x45} and a nil value; kinds 2/3: the boolean {kind == 2, type 1} as both), sets `rdx` to {4, index} and returns index OR 0x100; kind 5 first becomes {4, `0082FCB0(rcx, float rdx+4)`}; kind 4 returns dword `rdx+4` OR 0x100 when it is at most 0xFF; every other case calls `0082F5A0(rcx, rdx)` and, for a kind-6 value with differing dwords `+8`/`+0xC`, `0082F000(rcx, rdx, dword rdx+4)` when that register is at least byte `[rcx+0x42]`, else `0082F860(rcx, rdx)` (also used for non-6 kinds), and returns dword `rdx+4` | `0082F670`, `0082F69A`, `0082F6B2`, `0082F70C`, `0082F754` |
| `00830410` | 254 B | stores the value `r8` into the variable `rdx` (kind dword `[rdx]`): kind 7 frees `r8` then calls `0082F000(rcx, r8, dword rdx+4)`; kind 8 calls `0082F360(rcx, ((dword rdx+4) << 17 OR 0082F780(rcx, r8)) << 6 OR 9)`; kind 9 calls `0082F360(rcx, ((((signed word rdx+4) << 9 OR 0082F660(rcx, r8)) << 8 OR byte rdx+6) << 6) OR op)` with `op` = 0xA when byte `rdx+7` is 7 and 8 otherwise; for kinds 8, 9 and any other it then frees `r8`; freeing a kind-6 value whose dword `+4` has bit `0x100` clear and is at least byte `[rcx+0x42]` decrements byte `[rcx+0x44]` | `0083042E`, `0083045A`, `0083047B`, `008304A4`, `008304F8` |

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted, opus-the-lua-loader-and-what-it-accepts-ee-1003-2)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-the-lua-loader-and-what-it-accepts-ee-1003-2/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `008109F0` | 164 B | Resolves the stack index `edx` against the state at `rcx` to a 16-byte value slot: a positive index is taken from the current frame's base (the first qword of the record at `rcx+0x20`) and replaced by `01CCB510` when not below the top at `rcx+0x10` (unsigned); an index above -1001000 is taken from the top; exactly -1001000 gives the slot at `+0x40` of the object at `rcx+0x18`; lower indexes select upvalue number -1001000 minus the index of the frame's function closure (slot (n+1)*0x10), or `01CCB510` when the function value's type dword is 0x16 or the number exceeds the closure's byte `+0xA` (signed); it then calls `0081F580` with the slot's qword and `r8d`, copies the returned 16-byte value (qword plus type dword `+8`) to the top and advances the top by 0x10. | `00810A16`, `00810A21`, `00810A43`, `00810A74`, `00810A89` |
| `00812C10` | 765 B | Measures the pattern string at `r8`, sets up a stack buffer record (inline 0x200-byte area, length 0, owner `rcx`) and repeatedly finds the pattern in the subject `rdx` with the import at `008C2A08`; for each hit it appends the subject bytes before the hit and then the whole replacement string `r9`, each append first growing the buffer when the free space is too small (new size doubled, or length plus need, calling `00812960` with `01CCA278` on overflow, allocating through `00810240`, copying with `00861EBA` and calling `00810D20` with -2 when the old storage was not the inline area) before copying with `00861EBA`, and resumes after the pattern; when no hit remains it appends the rest of the subject through `00813450` and `00861EBA`, pushes the buffered bytes with `008105C0`, calls `00810D20` with -2 when the storage is not inline, and returns the result of `00811530` with -1 and 0, checking the stack cookie through `00808C40`. | `00812C91`, `00812D0C`, `00812D69`, `00812E42`, `00812EBF` |
| `008135B0` | 202 B | Calls `00812890` with `xmm1` = 502.0 (`01CCA3C4`) and `0080F420` with `r8d` + 0x14, raising through `00812960` with `01CCA240` and `01CCA308` when that returns zero; then, for each 16-byte entry of the array at `rdx` until one whose first qword is null, it calls `00810730` with minus `r8d` repeated `r8d` times (skipped when `r8d` is not positive), `00810470` with the entry's second qword and `r8d`, and `00810DF0` with -2 minus `r8d` and the entry's first qword; finally it tail-jumps to `00811130` with the bitwise NOT of `r8d`. | `008135D5`, `008135EF`, `00813625`, `0081363A`, `00813675` |
| `0081DC10` | 183 B | With the frame record at `rcx+0x20`: when byte `rcx+0x48` has bit `0x2` or `0x4` set it first, for bit `0x2` only, calls `0081DA20` with 1 and -1 (keeping the `rdx` source position relative to the stack base `rcx+0x38`), then copies the previous frame's (`+0x10`) qword `+0x38` to `rcx+0x28`; it makes the previous frame current at `rcx+0x20`, copies the value qword and type dword (the first 12 bytes) of each 16-byte slot from `rdx` to the frame's function slot (`[frame]`) onward while the signed word count at frame `+0x20` is not exhausted and the source is below the top `rcx+0x10` (unsigned), sets the type dword of the remaining wanted slots to 0 while the count stays positive, stores the end position to `rcx+0x10`, and returns the word count plus 1. | `0081DC2D`, `0081DC41`, `0081DC65`, `0081DC87`, `0081DCA0` |
| `008241C0` | 145 B | Using the state at `rcx+0x38`, calls `0081EFB0` with it and the incoming `rdx` and `r8`, pushes the returned object on that state's stack (qword plus a type dword equal to the object's byte `+8` OR 0x40) and calls `0081FB80` with the qword at `+8` of the record at `rcx+0x30` and the pushed slot; when the returned slot's type dword is 0 it writes 1 to its value and type dwords and, if the qword at `+0x18` of the state's `+0x18` record is greater than zero (signed), calls `0081A8A0`; it then pops the slot (top minus 0x10) and returns the `0081EFB0` result. | `008241D9`, `008241F7`, `0082420E`, `00824219`, `00824234` |
| `0082B9A0` | 408 B | With block record B at `rcx+0x20` and lexer L at `rcx+0x18`: if B has a predecessor (qword `+0`) and byte `+0xD` set it calls `0082FB30`, then `0082FD80` with that result and B's byte `+0xC`, then `0082FE20` with it; if B's byte `+0xE` is set it interns `01CCBCEC` with `0081EF90`, adds a label with `0082C310` (list at `+0x20` of L's `+0x50` record, dword `+0x28` of L's `+0x30` record) and passes that 0x18-byte entry to `0082A7C0`; it then makes the predecessor current, adds B's byte `+0xC` minus byte `rcx+0x42` to dword `+8` of the `+0x50` record, and while `rcx+0x42` exceeds B's `+0xC` decrements it and stores dword `rcx+0x28` into field `+0xC` of the 16-byte entry in the array at `[[rcx]+0x30]` numbered by the signed word at index `+0x42` + dword `rcx+0x3C` of the word array at `[[L+0x50]]`, copies `+0x42` to `+0x44` and B's signed word `+8` to dword `+0x28` of the `+0x50` record; with a predecessor it calls `0082C0B0` and returns, it returns when B's signed word `+0xA` is not below the record's dword `+0x18`, else it formats `01CCD0C0` (name byte `+8` = 4 and byte `+0xA` above 0) or `01CCD0E8` via `0081BFF0`, clears L's dword `+0x10` and calls `00824330`, where the range ends. | `0082B9CB`, `0082BA22`, `0082BA9A`, `0082BAC6`, `0082BB33` |
| `0082BB40` | 262 B | When the token dword `rcx+0x10` is not 0x120 it gets the token text from `00824340` with 0x120, formats `01CCCFC8` with it through `0081BFF0` and calls `00824330`, where the range ends; otherwise it saves the qword `rcx+0x18`, calls `00824260`, calls `0082C220` with the saved qword, increments byte `+0x42` of the function record at `rcx+0x30` and writes that record's dword `+0x28` into field `+8` of the 16-byte entry (array at qword `+0x30` of the record's first qword) numbered by the signed word at position dword `+0x3C` plus the new count minus 1 of the word array at the first qword of the `+0x50` record of the record's `+0x18` object, calls `00829B10` with a stack record, 0 and dword `rcx+4`, then writes dword `+0x28` again into field `+8` of the entry numbered the same way from dword `+0x3C` plus the stack record's dword `+4`, and returns after the stack-cookie check through `00808C40`. | `0082BB59`, `0082BB81`, `0082BB8A`, `0082BBD0`, `0082BC01` |
| `0082C6E0` | 470 B | Saves byte `+0x44` of the function record at `rcx+0x30`; when the token dword `rcx+0x10` is 0x120 it raises a limit error if the dword at `rdx+0x18` is above 2147483645 (signed), formatting `01CCD000` with `01CCD128`, that limit and either `01CCCFD8` or `0081BFF0` of `01CCCFE8` with dword `+0x68` of the record's first-qword object and calling `00824330`; otherwise it saves `rcx+0x18`, calls `00824260` and makes a stack key record of kind 4 holding the `00830510` result for the saved qword; for any other token it calls `00824260`, parses the key with `0082D470` and `0082F8E0`, and requires token 0x5D (else `00824340`, `0081BFF0` with `01CCCFC8` and `00824330`) before calling `00824260`; it then increments the dword at `rdx+0x18`, requires token 0x3D the same way, calls `00824260`, converts the key with `0082F660`, parses the value with `0082D470` and converts it with `0082F660`, emits through `0082F450` with 0xA, the dword at `+4` of the record at `rdx+0x10` and both results, restores byte `+0x44` and returns after the stack-cookie check through `00808C40`; the listing stops inside the 0x3D error path. | `0082C719`, `0082C756`, `0082C790`, `0082C7FF`, `0082C804` |
| `0082CB10` | 301 B | With the function record at `rcx+0x30`: when the token dword `rcx+0x10` minus 0x104 is at most 0x1A (unsigned) and its bit is set in mask 0x4020007, or the token is 0x3B, it passes first 0 and count 0; otherwise it parses an expression into a stack record with `0082D470` and, while the token is 0x2C, calls `00824260`, `0082F860` and `0082D470` again, counting expressions; when the record's kind dword is 12 or 13 it calls `00830350` with -1, for kind 12 with a single expression rewrites the code dword the record indexes (array at `+0x18` of the function record's first qword) by clearing bits `0x21` and setting `0x1E`, and for both kinds passes byte `+0x42` as first and -1 as count; for other kinds one expression passes the `0082F780` result as first and several pass byte `+0x42` after `0082F860`, with the expression count; it then calls `00830120` with first and count, calls `00824260` when the token is 0x3B, and returns after the stack-cookie check through `00808C40`. | `0082CB48`, `0082CB6A`, `0082CBCF`, `0082CBF5`, `0082CC0D` |
| `00830350` | 184 B | Works on the instruction indexed by dword `rdx+4` in the code array at `+0x18` of the record `[rcx]`: when the kind dword `[rdx]` is 12 it replaces the instruction's `0x7FC000` field with `r8d` + 1 and returns; when it is 13 it replaces the field above `0x7FFFFF` with `r8d` + 1 and the `0x3FC0` field with byte `rcx+0x44`, and when that byte plus 1 exceeds byte `+0x7A` of the record `[rcx]` (signed) it either calls `00824330` with `01CCD330` (when the sum is at least 0xFA) or stores the sum to `+0x7A`, then increments byte `+0x44`; other kinds return unchanged. | `0083037E`, `008303AB`, `008303CF`, `008303EC`, `008303EF` |
| `00830540` | 373 B | Returns at once when `edx` is -1; otherwise walks the jump chain through the code array at `+0x18` of the record `[rcx]`: for each index it derives the next one from the instruction's field above `0x3FFF` (field minus 0x1FFFF, with -1 ending the chain), takes the preceding instruction as the control when the index is at least 1 and the byte table at `01CCCCD0` has a negative entry for that instruction's opcode (`0x3F` field), and when the control's opcode is 0x1C either sets its `0x3FC0` field to `r9d` (when `r9d` is neither 0xFF nor equal to the control's field above `0x7FFFFF`) or rewrites it to opcode 0x1B with that top field shifted down by 17 (its low eight bits forming the `0x3FC0` field, its top bit ORed into bit 14) and the `0x7FC000` field kept, then points the jump at `r8d`; for other control opcodes it points the jump at the fifth argument; the jump field is set to target minus index minus 1 plus 0x1FFFF, and a distance whose absolute value exceeds 0x1FFFF (signed `jg`) calls `00824330` with `01CCD308`, where the range ends. | `00830598`, `008305C2`, `008305F2`, `0083060D`, `00830642` |
