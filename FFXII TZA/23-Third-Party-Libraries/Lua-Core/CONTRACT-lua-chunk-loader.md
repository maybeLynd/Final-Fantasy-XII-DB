---
contract: The Lua chunk loader — accept a buffer, fork on its first byte, produce a callable chunk
category: 23-Third-Party-Libraries
scope: subsystem
readiness: CONTRACT READY   # §13 carries no live observation; isolated original-code only
confidence: PROVEN
implements: the-lua-loader-and-what-it-accepts.md
entries: [00683C30, 00812F70, 00810180, 0081DF50, 0081D790, 0082BE30, 0082E910, 0082E490, 008216A0]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 58 addresses cited - 4 data, 17 entry, 34 interior, 3 literal, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-08
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-12
  last_pass_state: opus-lua-chunk-loader-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — the Lua chunk loader

> Formalises [the Lua loader and what it accepts](the-lua-loader-and-what-it-accepts.md) into
> something an engineer can reimplement and a differential test can be written from. **`F-4`'s last
> named candidate.**
>
> **Every constant below was re-derived from the binary for this contract**, not transcribed. That
> pass confirmed the source page in full and added two details it does not mention — see §12.
>
> **Readiness is `CONTRACT READY`, not `RECONSTRUCTION READY`**: §13 carries no LIVE observation. **Nothing here has
> been observed in a live process**, and `DA-1` — whether the shipped game ever hands this loader
> anything at all — remains open.

## 1. Purpose

Turn a buffer of bytes into a callable Lua chunk. **The first byte decides everything**: `0x1B` runs
the bytecode reader, anything else runs the full Lua source parser. Both are present and wired in,
and the engine refuses neither.

**For a modder that is the headline fact in this database**: if you can get a script to the engine,
you can write it in ordinary Lua text — no byte-compiler, no bytecode format to reverse.

## 2. Interface

| operation | entry | conv | signature | returns |
|---|---|---|---|---|
| Phyre entry point | `00683C30` (103 B) | MS x64 | `(lua_State* rcx, Buffer* rdx)` | `al` — `true` on success |
| load a buffer | `00812F70` (46 B) | MS x64 | ~~`(L, const char* data, size_t len, u32 name, const char* mode)`~~ `luaL_loadbufferx(L, const char* buff, size_t size, const char* name, const char* mode)` *(corrected 2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 322, to match the boxed correction; `00683C36`–`00683C57` re-read)* | Lua status |
| generic load | `00810180` (180 B) | MS x64 | `(L, reader, data, name, mode)` | Lua status |
| protected parse | `0081DF50` (226 B) | MS x64 | `(L, ZIO*, …)` — takes `f_parser`'s address at `0081DF7C` | Lua status |
| **the fork** | `0081D790` (356 B) | internal | `f_parser(lua_State* L, void* ud)` | — |
| source path | `0082BE30` (630 B) | internal | `luaY_parser(L, z, buff, dyd, name, firstchar)` | `Proto*` |
| bytecode path | `0082E910` | internal | `luaU_undump(L, z, buff, name)` | `Proto*` |
| header check | `0082E490` (414 B) | MS x64 | builds 18 bytes, **reads 17**, compares **18** — see the box below | — |
| interpreter | `008216A0` (4,778 B) | internal | `luaV_execute` | — |

**`0081D790` has zero callers in the call graph.** It is reached only through a function pointer
taken at `0081DF7C`, which is why a caller-based search cannot find it; the source page establishes
its reachability with four instruments, each with its own passing control.

## 3. Types

### 3.1 The precompiled-chunk header — 18 bytes, built a field at a time

`0082E490` assembles it on the stack from immediates, so the build's configuration is readable
straight out of the instruction stream:

```asm
0082E4C7  mov  esi, 0x61754C1B          ; -> 1B 4C 75 61   "\x1bLua"
0082E4D2  mov  [rsp+0x20], esi
0082E4D6  mov  [rsp+0x24], 0x04010052   ; -> 52 00 01 04
0082E4DE  mov  [rsp+0x28], 0x00040408   ; -> 08 04 04 00
0082E4E6  mov  [rsp+0x2c], eax          ; <- dword [01CCD300] = 19 93 0D 0A
0082E4B9  movzx edi, word [01CCD304]    ; <- 1A 0A
```

| offset | bytes | meaning |
|---:|---|---|
| 0 | `1B 4C 75 61` | `LUA_SIGNATURE` |
| 4 | `52` | `LUAC_VERSION` — **Lua 5.2** |
| 5 | `00` | official format |
| 6 | `01` | little-endian |
| 7 | `04` | `sizeof(int)` |
| 8 | `08` | `sizeof(size_t)` |
| 9 | `04` | `sizeof(Instruction)` |
| 10 | **`04`** | **`sizeof(lua_Number)` — FLOAT, not double** |
| 11 | `00` | numbers are not integral |
| 12–17 | `19 93 0D 0A 1A 0A` | `LUAC_TAIL`, from `01CCD300` |

**4 + 4 + 4 + 4 + 2 = 18 bytes.** Read back from the image, `01CCD300` holds
`19 93 0D 0A 1A 0A` exactly.

> **`lua_Number` is 4 bytes.** Stock Lua 5.2 on x64 uses `double`; this build uses `float`. **Every
> number in every FFXII Lua script is single precision** — integers exact only to 2²⁴ = 16,777,216.
> A counter, a gil total or an experience total past that stops incrementing by one.

### 3.2 The Phyre buffer, as `00683C30` reads it

```
+0x10  u32    length     bit 31 CLEARED before use (`btr eax, 0x1f`) -> r8, the size    [was: "name"]
+0x18  ptr    data       NULL -> refuse
+0x48  u64    name       tagged pointer; the low bit is subtracted off -> r9, the name  [was: "length"]
                         (corrected 2026-09-25 on OPUS block 322, to match the boxed correction)
```

## 4. Preconditions · postconditions · invariants

**Preconditions.** `00683C30` requires a live `lua_State` in `rcx` and a buffer in `rdx`. It
dereferences `rdx` **before** any null check on the buffer itself — only `data` is checked.

**Postconditions.** `true` only when `luaL_loadbufferx` returned 0. On failure the Lua stack is
restored: the error message is converted and popped (§10).

**Invariants.**
- **The fork is on the first byte and nothing else.** `cmp esi, 0x1B` at `0081D7DD`.
- **Both mode guards are `if (mode && …)`.** With `mode == NULL` neither can fire.
- ~~The header comparison is over **`0x11` = 17 bytes** (`mov r8d, 0x11` at `0082E4CC`) — the 18-byte
  header less the first byte, already consumed by the dispatcher.~~ **17 bytes are read and all 18 are compared.**
  `0082E4CC mov r8d, 0x11` sets the read length, and `0082E4EA` plants byte 0 (`0x1B`) itself. *Corrected 2026-09-25
  (FABLE, Claude Opus 5.5), on OPUS block 301, to agree with the correction box below.*

## 5. State

| | detail |
|---|---|
| **read** | `01CCD300` / `01CCD304` (`LUAC_TAIL`), the error-string literals in §12 |
| **written** | the `lua_State`'s stack; nothing global on this path |
| **allocated** | the `Proto` and its `Closure`, by the Lua allocator, not by these functions |

## 6. Relationships

```
00684D10 / 00684F60 / 00686280      Phyre script execution (three callers, UNREAD)   <- corrected 2026-10-02, OPUS - answered, read since: EXP-110 ran the callers (2026-09-25, §13) and EB-1 was answered 2026-09-26
        |
00683C30  PhyreScript_LoadBuffer    <-- mode = NULL is set HERE
        |
00812F70  luaL_loadbufferx
        |
00810180  lua_load
        |
0081DF50  luaD_protectedparser      <-- takes f_parser's ADDRESS at 0081DF7C
        |
0081D790  f_parser
        |
        +-- first byte == 0x1B --> 0082E910  luaU_undump   (bytecode)
        +-- otherwise           --> 0082BE30  luaY_parser   (SOURCE TEXT)
```

## 7. State transitions — the fork, with its compiler trick

```c
static void f_parser(lua_State *L, void *ud)          /* 0081D790 */
{
    int c = zgetc(p->z);
    const char *mode = p->mode;                       /* [rbx + 0x50] */
    if (c == 0x1B) {
        if (mode && strchr(mode, 'b') == NULL) error("attempt to load a binary chunk");
        f = luaU_undump(L, p->z, &p->buff, p->name);
    } else {
        if (mode && strchr(mode, 't') == NULL) error("attempt to load a text chunk");
        f = luaY_parser(L, p->z, &p->buff, &p->dyd, p->name, c);
    }
}
```

**The `'b'` is computed, not loaded:** `lea edx, [rsi + 0x47]` with `esi = 0x1B` gives `0x62 = 'b'`.
The `'t'` on the other branch is a plain `mov edx, 0x74`. Both `strchr` calls go through
`008C2A10`, which resolves through the PE import directory to `VCRUNTIME140.dll!strchr`.

## 8. Script · resource · event interactions

**Only four of the eleven standard libraries are registered** — `math`, `bit32`, `string`,
`coroutine` — per
[the bindings document](../../22-Middleware-PhyreEngine/Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md).
**Being able to compile source does not give you `print`, `pairs`, `io` or `os`.**

## 9. Determinism

Fully deterministic in its input buffer. No randomness, no clock, no global mutable state on this
path. The same bytes produce the same `Proto` every time.

## 10. Failure paths and edge conditions

| condition | behaviour |
|---|---|
| `data == NULL` | returns `false` at `00683C87` **without touching Lua at all** |
| compile error | **swallowed** — `FUN_00811530(L, -1, NULL)` then `FUN_00811130(L, -2)`, the `lua_tolstring` / `lua_settop` idiom, then `false` |
| bytecode with a wrong header | rejected by the ~~17-byte~~ 18-byte compare, 17 bytes read *(corrected 2026-10-02, OPUS: `0082E490+0x3C` `mov r8d, 0x11` is the read length; `0082E490+0x69`..`+0x89` compare qword, qword and word, bytes 0-17, byte 0 being the `0x1B` the checker plants at `0082E490+0x5A`)* |
| `mode == "b"` and text supplied | would be refused — **but Phyre passes NULL**, so it cannot happen on this path |

> **A syntactically invalid script fails silently here.** The message is produced, converted, popped
> and discarded. ~~**Whether any of the three callers reports it is unread**~~ **No caller reports it** *(answered: `EB-4`, answered 2026-09-12 on the loader page; 2026-10-02, OPUS)* (`EB-4`), so a modder
> should not expect a syntax error to announce itself.
>
> **A null data pointer is indistinguishable from a failed compile** at this level: both return
> `false`.

**The two inner functions are named from their argument shapes~~, not proven~~** *(answered: `00811130` is `lua_settop` - a negative index moves `top` by `idx + 1` slots, a non-negative one sets `top = base + idx + 1` and nils the gap, its whole 72-byte body; run as SETTOP in EXP-110; `00811530` stays shape-named; 2026-10-02, OPUS)* — `(L, -1, NULL)` and
`(L, -2)` — and are written `FUN_` for that reason.

## 11. Observable behaviour

```asm
00683C5A  mov qword ptr [rsp + 0x20], 0    ; the 5th argument: mode
00683C63  call 0x812f70                     ; luaL_loadbufferx(L, data, len, name, mode)
```

**Phyre passes zero for `mode`.** Both guards are conditional on `mode` being non-NULL, so **neither
form is refused** and the first byte alone decides the path. Had Phyre passed `"b"`, source text
would be rejected and this contract would say the opposite.

## 12. Reproduction formula

```c
bool PhyreScript_LoadBuffer(lua_State *L, Buffer *b)      /* 00683C30 */
{
    /* corrected 2026-09-25 (OPUS block 322): +0x48 is the NAME, +0x10 the LENGTH */
    const char *name = (const char *)(*(uint64_t *)(b + 0x48) - (*(uint8_t *)(b + 0x48) & 1)); /* tag off -> r9 */
    uint32_t    len  = *(uint32_t *)(b + 0x10) & 0x7FFFFFFF;                                  /* btr eax,31 -> r8 */
    char    *data = *(char **)(b + 0x18);

    if (data == NULL) return false;

    if (luaL_loadbufferx(L, data, len, name, NULL) != 0) {
        FUN_00811530(L, -1, NULL);
        FUN_00811130(L, -2);
        return false;
    }
    return true;
}
```

**Two details this contract's re-derivation adds, which the prose page does not mention:**

1. **The 17 is in a register, not the compare instruction.** `mov r8d, 0x11` at `0082E4CC`, set
   before the call at `0082E4EF` — so a reader looking for a literal `17` beside a `cmp` will not
   find one.
2. **A separate `0x1B` is staged at `[rsp+0x38]`** (`0082E4EA`) with the comparison buffer taken as
   `lea rdx, [rsp+0x39]` (`0082E4B4`). The first byte is held *next to* the 17 compared bytes rather
   than inside them, which is the physical form of "the first byte has already been consumed".

~~**`name` is passed in `r8d` — 32 bits.** It cannot be a full 64-bit pointer; the image loads at
`0x00120000` with ASLR clear, so a 32-bit address is sufficient here. **Whether it is a pointer or an
index is not established.**~~

> **✖ WRONG — THIS CONTRACT HAD TWO ABI FIELDS SWAPPED. `r8` is the SIZE; the name is `r9`.**
> Corrected from FABLE's EB-6 note by OPUS 2026-09-13 and re-derived at the image first:
> `00812F70` is `luaL_loadbufferx(L, buff, size, name, mode)` and it stores **`rdx` and `r8` as the
> reader's `{buff, size}` pair** — `00812F79 mov [rsp+0x30], rdx`, `00812F85 mov [rsp+0x38], r8`,
> `00812F8A lea r8, [rsp+0x30]` — with the reader `getS` in `rdx` (`00812F7E`). **`r9` is never
> touched.** It arrives at `lua_load` (`00810180`), which copies it to `rbx` and passes it as the
> chunk name, defaulting to the string at `01CCA108` when null: `008101AF test rbx, rbx` /
> `008101BA cmovne r8, rbx` / `008101BE call 0081DF50`.
>
> **So the reasoning above was applied to the wrong field.** "32 bits, therefore maybe an index"
> was asked about a LENGTH, and the real name pointer — a full 64-bit `const char *` — went
> undescribed. Nothing here is an index. The corrected shape at the call site `00683C30`: the u32
> at record `+0x10` with bit 31 cleared is the **chunk length** and bit 31 a flag, and the qword at
> `+0x48` less its low tag bit is the **chunk name**.
>
> **A plausible argument about the wrong operand is the most expensive kind of error a contract can
> carry**, because it reads as care taken.

> *Answered 2026-09-12 (FABLE, EB-6). **ADJUDICATED AND FOLDED BY OPUS 2026-09-13**, re-derived at the image; the correction is above.* **The 32-bit
> register is the `size`, and the `name` is the 64-bit `r9`: §3.2 has the two fields swapped.**
> `00812F70` is `luaL_loadbufferx(L, buff, size, name, mode)`: it stores `rdx` and `r8` as the
> reader's `{buff, size}` pair at `[rsp+0x30]` / `[rsp+0x38]` (`00812F79`, `00812F85`), leaves `r9`
> untouched and calls `00810180` with the reader `getS` (`00812F7E`), `&ls` and the stack `mode`
> (`00812F74`–`00812F8F`); `00810180` is `lua_load` — it copies `r9` to `rbx`, opens the `ZIO`
> (`0081C620`), and passes `rbx` as the chunk name, defaulting to the string `"?"` at `01CCA108` when
> null (`008101AF`–`008101BE`, `cmovne`), into `luaD_protectedparser` (`0081DF50`). So in `00683C30`
> the u32 at record `+0x10` with bit 31 cleared (`r8d`) is the **chunk length**, bit 31 a flag, and
> the qword at `+0x48` minus its low tag bit (`r9`) is the **chunk name, a 64-bit `const char *`**.
> Nothing here is an index; the corrected shape is `+0x10 u32 length (bit 31 flag)`, `+0x18 ptr
> data`, `+0x48 tagged ptr name`. What the tag bit at `+0x48` marks (the SSO reading in §3.2 is a
> guess from its subtraction) is the residue.

## 13. Runtime validation

**Evidence class: isolated original-code. Live capture: still absent.** (2026-09-12)

The header check `0082E490` runs at its real virtual address under Unicorn against an independent
reconstruction. Nothing else in the family has been executed, and **nothing at all has been observed
in a live process** — `DA-1` below is untouched by this and remains the subsystem's most important
unknown.

> **ADDED 2026-09-25 (OPUS, for FRONTIER-REQ-OPUS-EXP110-BACKREF): the callers have since run, the
> loader has not.** [EXP-110](../../_experiments/EXP-110-phyre-script-callers-exec.md) (method B, no
> live game; 48/48 cases, 38/38 mutants, stable across three processes) executed the three Phyre
> script-execution callers this contract named — `00684D10`, `00684F60`, `00686280` — and nine real
> TValue-stack leaves (`0080FD00` GETTOP, `00811130` SETTOP, the push family, `008113D0`, `008119F0`)
> against an independent model. **`00683C30` itself was a scripted boundary there** (entry-intercepted,
> planted return), so this contract's subject is exercised only *through* its callers: the sentence
> above — "nothing else in the family has been executed" — is superseded for the callers and still
> true for the loader body. `DA-1` is untouched.

**Instrument:** [`diff_lua_header.py`](../../../../Reconstruction/Tests/Differential/diff_lua_header.py)
against [`lua_header.c`](../../../../Reconstruction/Game/Script/lua_header.c).

**Result: 70 commands, 23 compared lines, 0 mismatches.** All six outcomes are reached — `OK` once,
`not a` five times, `truncated` once, `version mismatch in` three times, `incompatible` seven times
and `corrupted` six — and **the read length observed is 17 on every single case**, which is the
measurement that separates this contract's old reading from the true one.

**The expected header is taken from the image, not retyped.** The harness assembles it from the
three immediates in the instruction stream and the six tail bytes at `01CCD300`, and prints it:
`1B 4C 75 61 52 00 01 04 08 04 04 00 19 93 0D 0A 1A 0A`. A suite that hard-coded the header would
agree with a reconstruction that hard-coded the same mistake.

**Which rejection, not just whether.** The original never returns on a bad header — it formats a
message and raises — so the comparison reads the verdict off the message pointer the formatter is
handed, and the reconstruction returns the same five-way answer instead of raising. A
reimplementation with every accept/reject answer right and every message wrong would pass a weaker
suite and ship a loader nobody can diagnose.

**The case the suite exists for.** Byte 0 never comes off the stream, so the stream's first byte is
header byte **1** — and corrupting *that* must be rejected as `not a`. Driven alongside the accepted
case, the two pin the boundary from both sides: one shows the planted byte is not read, the other
shows the byte after it is.

**`corrupted` is reachable only one way**, and the suite shows it rather than asserting it: every
single-byte deviation in the six-byte tail selects it, and no deviation anywhere else does.

### How far the instrument itself has been tested

**42 mutants: 34 KILLED · 1 EQUIVALENT · 7 SURVIVED · 0 NO_BUILD · 0 TIMEOUT · 0 INVALID.**
Production inputs verified stable, all four hashes checked against the working tree afterwards.

**Every survivor is adjudicated, and they fall into three kinds — none of them a gap:**

| kind | mutants | why no case can distinguish it |
|---|---|---|
| the comparison starts at byte 1 instead of byte 0 | 2 | **Byte 0 is planted identically on both sides.** Comparing it or not cannot change an answer — which is this contract's central fact, arriving as a mutation. |
| the comparison reads one byte *further* | 4 | Covering more than the original does still covers everything the original does. One reads a byte past the 18, where the padding matches on both sides. |
| the verdict enum is renumbered | 1 | `LH_OK = 0 → 1` shifts every enumerator; the driver reports by name, and the numbering is internal encoding rather than interface. |

**What makes this a result rather than an excuse is the pair that did NOT survive.** The two mutations
that would *drop* a byte from coverage were both **KILLED**: the offset that would stop the second
comparison covering byte 8, and `16 → 17`, which would stop the tail being compared at its true
start. So the suite detects coverage *loss* and is blind only to coverage *gain* — which is the
correct asymmetry for a test of an exact-match check, and the opposite one would be the defect.

**The first campaign of this pilot is not cited, and the reason is worth recording.** It returned
**22 survivors, fifteen of them one mistake**: the driver seeded its stream from
`LuaHeader_Expected`, the table under test, so mutating an expected byte moved the fixture with it
and the two stayed consistent. That is the same defect found in `character_publish` **one pilot
earlier** and written up there as *a fixture that derives its layout from the header under test
cannot detect a layout error in it* — and then repeated immediately. The driver now carries its own
copy of the eighteen bytes, the harness reads a third copy out of the image, and the correction is
spelled out in the driver rather than cross-referenced, because a cross-reference is evidently not
enough to stop it happening again.

**What would fill it**, in order of value: whether a `lua_State` exists at all in a running game;
whether `00683C30` is ever entered; and if so, what the first byte of the buffer is. The first two
need a breakpoint or a trace, which `F-3` lists as not built. **That is why `DA-1` is still open, and
it is the single most important unknown about this subsystem** — everything above describes a loader
that may never be handed anything.

## 14. Unresolved

| id | what |
|---|---|
| `DA-1` | **whether the shipped game ever supplies a chunk.** The whole subsystem hangs on it. **Bounded statically 2026-09-26 (OPUS), not closed:** the image contains **no code that can create a `lua_State`**. `f_luaopen`'s markers are all absent: no `MEMERRMSG` literal, no `luaL_newstate` panic message, no reader of the tag-method name table `01CCBA90`, and `luaX_tokens` `01CCBBE0` is read only by `luaX_token2str` `00824340`. The controls are present: `ldo.c`, `llex.c` (`luaX_setinput` `008242A0`) and `lauxlib.c` are linked. See [`candidates/s50-opus-lua-state-constructor-census`](../../_index/candidates/s50-opus-lua-state-constructor-census/README.md), 8/8. So `00683C30` can run with a live state only if one built **outside this image** is handed in. What remains open: whether any module does that, and `EB-1` |
| `EB-1` | what the three callers of `00683C30` pass, and where the buffer comes from *(answered 2026-09-26, (FABLE, Claude Opus 5.5): a `PScript` object, whose instances no shipped asset declares; see [the loader page](the-lua-loader-and-what-it-accepts.md) `UQ-313`)* |
| `EB-2` | whether `luaL_loadfilex` (`00812FA0`) is reachable — if it is, the engine can load a `.lua` from disk *(answered: no - the loader page's `EB-2`, 2026-09-12; 2026-10-02, OPUS)* |
| `EB-3` | `00814B30` (287 B), a third `lua_load` caller with **zero callers**, ~~unidentified~~ *(answered: it is `load` - the loader page's `EB-3`, 2026-09-12; 2026-10-02, OPUS)* |
| `EB-4` | whether any caller reports a compile failure *(answered: no - the loader page's `EB-4`, 2026-09-12; 2026-10-02, OPUS)* |
| `EB-5` | the parser's own seven functions; only `0082BE30` is placed in the chain *(answered: on the loader page 2026-09-14; 2026-10-02, OPUS)* |
| ~~new~~ answered | ~~whether `name` is a pointer or an index, given it is passed as 32 bits~~ **a 64-bit pointer**, and the 32-bit value is the length *(corrected 2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 322, to match the boxed correction; `00683C36`–`00683C57` re-read)* |

## 15. Evidence

Static disassembly at the certified hash, with every constant in §3, §7, §11 and §12 **re-derived
from the instruction stream for this contract** rather than copied from the prose page. Imports
resolved by walking the PE import directory. `01CCD300` read back from the image bounded by
`SizeOfRawData`. **No `edges.tsv` caller count is used anywhere in this contract**, so the funclet
contamination class does not apply — and `f_parser`'s reachability deliberately rests on the source
page's four instruments, not on the call graph, because the call graph shows it as unreachable.

**Claim table added 2026-09-12 (`OPUS-LUAHDR-ISOLATED`).** The paragraph above states the method;
this enumerates the claims so `diff_lua_header.py` can map to them and a reimplementer can read them
row by row. Rows cover the header check only — the rest of the family is still static-only.

| claim | evidence | tier | confidence |
|---|---|---|---|
| the expected header is 1B 4C 75 61 52 00 01 04 08 04 04 00 19 93 0D 0A 1A 0A | three immediates at `0082E4C7`/`0082E4D6`/`0082E4DE` plus the six tail bytes at `01CCD300`. Executed — the harness reads them out of the image rather than retyping them | 1 (isolated original-code) | PROVEN |
| byte 0 is planted, not read: eighteen are built, seventeen are read | `0082E4EA mov byte [rsp+0x38], 0x1B`; `0082E4B4 lea rdx, [rsp+0x39]` with `0082E4CC mov r8d, 0x11`. Executed — the read length is compared on every case and is 17 every time | 1 (isolated original-code) | PROVEN |
| all eighteen bytes are compared | `0082E4F9`–`0082E519`: `qword`+`qword`+`word` over 0–7, 8–15, 16–17. Executed — a deviation in each group is driven | 1 (isolated original-code) | PROVEN |
| sizeof(lua_Number) in this build is 4, so a stock x64 luac chunk is rejected | byte 10 of the built header is `04` and byte 11 is `00`. Executed — byte 10 driven at `08`, which rejects as `incompatible` | 1 (isolated original-code) | PROVEN |
| the five rejections are selected by exact byte ranges | `0082E521` → `not a`, `0082E52D` → `version mismatch in`, `0082E536`/`0082E546` → `incompatible`, `0082E544` → `corrupted`, `0082E4F7` → `truncated`. Executed — each reached by its own range, and `corrupted` shown reachable only by a tail-only difference | 1 (isolated original-code) | PROVEN |
| any runtime observation | — see `DA-1` | none | UNKNOWN |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

### The header, rebuilt from the immediates that build it

| instruction | little-endian bytes | header offsets |
|---|---|---|
| `0082E4C7 mov esi, 0x61754C1B` | `1B 4C 75 61` | 0–3 |
| `0082E4D6 mov dword [rsp+0x24], 0x04010052` | `52 00 01 04` | 4–7 |
| `0082E4DE mov dword [rsp+0x28], 0x00040408` | `08 04 04 00` | 8–11 |
| `0082E4E6 mov dword [rsp+0x2C], eax` | `19 93 0D 0A` | 12–15 |
| `0082E4B9 movzx edi, word [rip → …]` | `1A 0A` | 16–17 |

Three immediates and a six-byte tail, exactly as §15 says, and they reassemble to
`1B 4C 75 61 52 00 01 04 08 04 04 00 19 93 0D 0A 1A 0A` — the stated header, byte for byte.
**Byte 10 is `04` and byte 11 is `00`**, so `sizeof(lua_Number)` is **4** in this build.

### Eighteen built, seventeen read — and the length is an immediate

§15 cites `0082E4EA mov byte [rsp+0x38], 0x1B` (byte 0 planted into the *read* buffer) and
`lea rdx, [rsp+0x39]` (the read starts one byte in). **The other half of that proof is beside them**:

```asm
0082E4CC  mov r8d, 0x11        ; 17 — the read length
```

The buffer is eighteen bytes, the read fills **seventeen** of them, and byte 0 is supplied by the
loader rather than by the file. The count is not inferred from the `lea`'s displacement; it is stated
by the call's own argument.

### All eighteen compared, in three groups

```asm
0082E4F9  mov rcx, [rsp+0x20] / mov rdx, [rsp+0x38] / cmp rcx, rdx    ; bytes 0–7
0082E508  mov rax, [rsp+0x28] / cmp rax, [rsp+0x40]                   ; bytes 8–15
0082E514  cmp di, word [rsp+0x48]                                     ; bytes 16–17
```

`8 + 8 + 2 = 18`. Nothing is skipped, and the planted byte 0 is inside the first comparison — so a
file whose first byte is *not* `0x1B` still passes that byte, because it was never read. **The
signature check on byte 0 is vacuous**, which is exactly what "planted, not read" means and is worth
stating in those terms.

### The five rejections

`0082E521 jne` (dword 0–3), `0082E52D jne` (word 4–5), `0082E536 jne` (qword 0–7), `0082E544 je` /
`0082E546 jmp` (dword 8–11) — five exits chosen by re-comparing progressively narrower slices of the
same eighteen bytes, as §15 describes.

**Not claimed:** no runtime observation; `DA-1` stays open.

## 16. Parity plan

**First pilot operation: the header check.** It is pure, takes 18 bytes and returns accept/reject,
and its boundary is exact — ~~**17 compared bytes, not 18**~~ **18 compared bytes, 17 read** *(corrected 2026-10-02, OPUS: `0082E490+0x3C` `mov r8d, 0x11` is the read length; `0082E490+0x69`..`+0x89` compare qword, qword and word, bytes 0-17, byte 0 being the `0x1B` the checker plants at `0082E490+0x5A`; the box below)*. A differential harness can plant headers
directly.

> ### ⚠ "compares 17" is wrong, and so is the boundary case built on it
>
> **CORRECTED 2026-09-12 (`OPUS-LUAHDR-ISOLATED`), from the body.** The function builds an 18-byte
> expected header, **reads 17 bytes from the stream**, and **compares all 18**.
>
> Byte 0 is not read because the function **plants it itself**: `0082E4EA mov byte [rsp+0x38], 0x1B`
> writes the signature's first byte into the actual-header buffer, and `0082E4B4 lea rdx, [rsp+0x39]`
> with `0082E4CC mov r8d, 0x11` reads the remaining **17** into the bytes after it. That byte was
> already consumed upstream — it is `luaY_parser`'s `firstchar`, which is how the loader told the two
> chunk kinds apart in the first place.
>
> The comparison is then three tests covering **all eighteen bytes**: `qword [rsp+0x20]` against
> `qword [rsp+0x38]` (bytes 0–7), `qword [rsp+0x28]` against `qword [rsp+0x40]` (8–15), and `di`
> against `word [rsp+0x48]` (16–17).
>
> **The boundary case below still holds, for a different reason, and a reimplementer needs the right
> one.** A file whose byte 0 differs is accepted — not because byte 0 is outside the compared range,
> but because **byte 0 never comes from the file**. A reimplementation that skipped comparing byte 0
> would agree on every accept/reject answer and would be built on a false mechanism; one that read 18
> bytes from the stream would consume one byte too many and desynchronise everything after the
> header.
>
> **The expected header, read out of the instruction stream and `01CCD300`:**
> `1B 4C 75 61 52 00 01 04 08 04 04 00 19 93 0D 0A 1A 0A`
>
> `sizeof(lua_Number)` in this build is **4**, and the integral flag is `0` — so the boundary case
> below is not hypothetical: a stock x64 `luac` emits `8` there and is rejected.
>
> **The five rejection paths are distinct and each carries its own word**, which is the part a
> reimplementer must reproduce to be diagnosable rather than merely correct:
>
> | condition | message |
> |---|---|
> | the 17-byte read returns non-zero | `truncated` |
> | bytes 0–3 differ from `1B 4C 75 61` | `not a` precompiled chunk |
> | bytes 4–5 differ (version, format) | `version mismatch in` |
> | bytes 0–7 match and 8–11 match, but 12–17 differ | `corrupted` |
> | bytes 8–11 differ (the four `sizeof` fields) | `incompatible` |
>
> ~~**Not yet executed.** This box is static reading; §13 is unchanged and still says so.~~ *(answered: executed in isolation - §13, 70 commands, 0 mismatches, 2026-09-12; 2026-10-02, OPUS)*

**Boundary cases that must actually distinguish something:**

- a header differing **only in byte 0** — must still be *accepted* ~~by the 17-byte compare, because~~
  ~~byte 0 is not in the compared range~~, because byte 0 never comes from the file *(corrected 2026-10-02, OPUS: `0082E490+0x5A` plants `0x1B` and the 18-byte compare covers it; the box above)*. A test using a wholly wrong header would never notice if a
  reimplementation compared all 18.
- `sizeof(lua_Number)` = 8 instead of 4 — the case a stock x64 `luac` produces, and the one a modder
  will actually hit.
- `LUAC_VERSION` 0x51 (Lua 5.1) against 0x52.
- a truncated buffer shorter than 18 bytes.

~~**No code has been written.** This section is a plan, not a status.~~ **DONE 2026-09-12** — see
§13. `STRUCTURAL`, `SERIALIZATION`, `EDGE-CASE` and `CONTRACT` are covered; `CALCULATION` and
`STATE-TRANSITION` are `N/A` because nothing is computed and nothing is kept. `INTEGRATION` is not
covered — the `ZIO` read is answered and no real chunk is loaded — and `FULL-SUBSYSTEM` is not,
because this is one operation of the loader and the fork, the parser and the undumper are not
reconstructed.

**Four things a reimplementer must take from this contract:**

1. **Read seventeen, not eighteen.** Byte 0 is already consumed; reading it again desynchronises
   everything after the header.
2. **Plant `0x1B` and compare all eighteen.** Skipping the comparison of byte 0 gives the same
   answers and rests on a mechanism the original does not have.
3. **Return the right refusal.** Five messages, each selected by an exact byte range.
4. **This build's `lua_Number` is four bytes.** A chunk from a stock x64 `luac` is rejected, and as
   `incompatible`.

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-contract-lua-chunk-loader-ee-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `008242A0` | 131 B | initialises the lexer state `ls` = `rdx` for Lua state `L` = `rcx`: dword `[ls]` = the fifth argument, byte `+0x68` = 0x2E, qword `+0x38` = `L`, dword `+0x20` = 0x11E, qword `+0x40` = `r8`, qword `+0x30` = 0, dwords `+4` and `+8` = 1, qword `+0x58` = `r9`, qword `+0x60` = `0081EF90(L, '_ENV')` with byte `+9` of that string gaining `0x20`; then for the buffer at qword `+0x48` stores `00823670(L, qword [buf], qword [buf+0x10], 0x20)` to qword `[buf]` and 0x20 to qword `[buf+0x10]`; returns nothing | `008242AF`, `008242B7`, `008242E3`, `008242F2`, `00824305` |
