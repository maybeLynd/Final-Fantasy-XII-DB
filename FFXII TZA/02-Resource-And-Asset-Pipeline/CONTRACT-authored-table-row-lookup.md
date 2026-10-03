---
contract: address a row in an authored data table through its registry header
category: 02-Resource-And-Asset-Pipeline
scope: family
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 02-Resource-And-Asset-Pipeline/authored-data-table-registry.md
entries: ["0020E600", "003876D0", "0030E360"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 173 addresses cited - 58 data, 35 entry, 78 interior, 2 literal, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-11
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-authored-table-row-lookup-pass-1  # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — the authored table row lookup

Not one function. A four-instruction shape that **226 distinct functions** write out inline to reach
authored data: read a reference, resolve it, read a stride, multiply. Every status definition, every
equipment row, every gambit definition is addressed this way, and a reimplementation that gets this
one shape right gets the addressing of the game's authored content right with it.

## 1. Purpose

Authored tables ship as data with base-relative references rather than pointers, so nothing in them
can be used until it is relocated against the loaded image. The registry holds, per table, a header
that says where the rows are and how far apart they sit. Every consumer does the same four steps
rather than calling a shared accessor — the shape is inlined, not centralised, which is why it must
be specified once here instead of documented at one call site.

## 2. Interface

There is no single entry point; this is a shape. Its one shared callee:

| | |
|---|---|
| entry point | `0020E600` — `ImageAddress_ResolveRuntimePointer`, the only function the shape calls |
| calling convention | Microsoft x64; `ecx` = the base-relative reference |
| parameters | the `uint32` at `header + 0x0C` |
| return type | pointer |
| return semantics | the resolved address of the row array, or **0** when it cannot be resolved — and every caller in this family tests it (§10.1) |
| the resolver, whole | `0020E600` is three instructions: `mov eax, ecx` / `add rax, qword ptr [rip → 01F83530]` / `ret`. It zero-extends a 32-bit reference and adds one global 64-bit base, which is why every consumer's 32-bit address arithmetic is sound |
| callbacks | none |

A worked instance, `BattleStatus_ComputeDefaultShortTimer` (`003876D0`, 88 B), whole:

```asm
003876D6  mov   rax, [rip+...]        ; rax = *(02EBF118), the registry slot -> header
003876DF  test  rax, rax / je         ; the slot itself may be null
003876E4  mov   ecx, dword [rax+0xC]  ; the base-relative reference
003876E7  call  0020E600              ; resolve it
003876EC  test  rax, rax / je         ; the resolve may fail
00387700  mov   rcx, [rip+...]        ; the header again
00387707  movzx ecx, word ptr [rcx+8] ; the record stride, a u16
0038770B  imul  ecx, ebx              ; * the row index
0038770E  add   ecx, eax              ; + the resolved base = the row
```

## 2a. The base the whole shape adds -- and why this contract stops short of calling it zero

**Added 2026-09-11 (`OPUS-PROBE-RESOLVEBASE`), from a contract-first probe: implementing §2 from this
text alone required the value of `01F83530`, and the text did not have it.**

What was found, and it is more than expected:

- **`0020E620` is the inverse of `0020E600`.** `RuntimePointer_EncodeImageAddress` is
  `sub ecx, dword ptr [01F83530]` / `mov eax, ecx` / `ret` -- the encode side of the same base. §7
  already sends `+0x14` through it without saying what it does; it turns a runtime address back into
  a stored reference.
- **The two functions read the same global at different widths** -- `qword` in the resolver, `dword`
  in the encoder. Confirmed at byte level: the resolver is `8B C1 / 48 03 05 …` (**REX.W**, a 64-bit
  add of a qword) and the encoder is `2B 0D … / 8B C1` (**no REX.W**, a 32-bit subtract of a dword).

  > **⚠ SHARPENED 2026-09-12 (OPUS), then CORRECTED the same day after
  > `ASTRA-CONTRA-OPUS-REFERENCE-MODULO-WINDOW`. Both halves of the first version were wrong in
  > different ways, and the second is the one to read.**
  >
  > Writing `decode(x) = base + zext32(x)` and `encode(p) = (uint32)(p - base)` — **both modular**:
  >
  > ```
  > decode(encode(p)) = base + ((p - base) mod 2^32)
  > decode(encode(p)) == p   <=>   ((p - base) mod 2^64) < 2^32
  > ```
  >
  > **The bound is an UNSIGNED 64-BIT DISTANCE from the base, not a signed difference and not a
  > property of the base.** Checked rather than accepted:
  >
  > | base | `p` | round-trips? | `mod 2^64 < 2^32`? | base fits 32 bits? |
  > |---|---|:--:|:--:|:--:|
  > | `0000000100000000` | `0000000100001000` | **yes** | yes | **no** |
  > | `FFFFFFFFFFFFF000` | `0000000000001000` | **yes** | yes | **no** |
  > | `0000000000000000` | `0000000100001000` | **no** | no | yes |
  >
  > So **"the base fits in 32 bits" is neither necessary nor sufficient** — my first correction
  > called it necessary, which rows 1 and 2 refute — and the signed form cannot describe row 2 at
  > all, where the distance wraps. The EXP-076 wrap control already had that shape on file.
  >
  > **The ordinary reading still holds where its assumption is stated**: for a base and pointers in
  > one non-wrapping window below 4 GiB — which is what this contract's consumers have always been
  > — the modular bound and the plain difference agree.
- **`01F83530` lives in `.bss`** -- past the end of `.data`'s raw data -- so it **begins as zero**.
- **Exactly two instructions in the image reference it, and both are these reads.** Nothing writes it
  rip-relative, and **nothing takes its address**: a sweep of `01F83500`-`01F83560` finds six
  referencing instructions, all rip-relative accesses to individually-addressed neighbours, and not
  one `lea`.

**If the base is zero, both functions are identities**, and a "base-relative reference" is simply a
32-bit-truncated absolute address -- which would settle the open point §3 raises about `+0x0C`, and
would explain this contract's own observation that every consumer's 32-bit address arithmetic is
sound.

**This contract does not claim that, and the reason is a control that failed.** The same sweep was
pointed at registry slot `02EBF138`, which is certainly written -- §7 names `003845F0` doing it. The
sweep reports **no rip-relative write to it either**, because that write goes through a pointer in
`rcx`. So the instrument provably cannot see the class of write that matters, and "no writer found"
here is bounded by exactly that blindness. What raises the confidence above the registry case is the
absence of any `lea`: the slots' writer gets its address from one, and nothing supplies this global's.

**The discriminator is one read and needs no game state beyond a loaded process: read the qword at
`01F83530`.**

### ⚠ CORRECTED 2026-09-12 — that read was already performed, and the confidence-raiser above is too strong

**Raised by ASTRA (`ASTRA-CONTRA-OPUS-REFERENCE-LIFETIME`) and verified here before being accepted.**

**The read is not owed; it is on file.** [`EXP-002`](../_experiments/EXP-002-st2e-group-tables.md)
records, on 2026-09-08: *"the arena base at `[0x01F83530]` reads `0` at the title screen, which
matters because `ImageAddress_ResolveRuntimePointer` adds it"*. This section queued that exact read
as class A of a runtime request **four days later**, and a block reading it would have asked for an
observation the database already had — the same shape as `EC-4`, and the reason
`check_already_answered.py` exists.

**So the identity reading has one live observation behind it**, and this contract now says so. What
it must not say is more than that:

| what the observation supports | what it does not |
|---|---|
| at the title screen the base is `0`, so **at that moment** both functions are identities and a stored reference is a 32-bit-truncated absolute address | that the base is `0` **for the process lifetime**. One snapshot is a moment, and repeating it is another moment |
| §3's open point about `+0x0C` is answered *for that state* | that it is answered for every state the 226 consumers run in |

**And the argument that raised confidence above the failed control is withdrawn.** This section
admitted the sweep *"provably cannot see the class of write that matters"* — a store through a
pointer in a register — and then leaned on **the absence of any `lea`** to raise confidence anyway.
That does not follow, and this contract's own §7 is the counter-example: `003845F4` writes a
registry slot through `rcx`, and **the address in `rcx` need not come from a `lea` in the same
function**. A layer that hands out addresses is exactly the shape that would defeat it, and one
exists: **`0036BC60` splits linked free blocks across fifteen `0xA8` records at `022D7FD0`**, and
`functions.tsv` already tags it `ImageAddressArena`.

> **`BW-2` in the question register reads ANSWERED with *"no arena"*, and that answer rests on
> `FUN_0036C660` being a container release through the import at `008C2F70`. It is not a release:
> parsing the PE import directory gives `008C2F70` = `api-ms-win-crt-string-l1-1-0.dll!strncpy`, and
> `free` is at `008C2B48` — one slot away.** That row and
> [`ebp2-container.md`](../25-EBP-Script-Container/Container/ebp2-container.md) are FABLE's, and
> ASTRA has routed the correction to them; it is named here because `BW-2`'s answer explicitly
> extends *"the same convention settled for the authored-table resolver (J-C)"* to this contract,
> and **this contract must not lean back on a conclusion that leans on it.**

**What is genuinely open, restated honestly:** whether anything ever writes `01F83530` after the
title screen. A second snapshot cannot settle it; a **write watchpoint** on that address is the
right instrument.

> **⚠ TIGHTENED 2026-09-12, raised by ASTRA and accepted after reading the code.** The sentence this
> replaces said a watchpoint "across a load **can**" settle it. **It cannot.** A watchpoint settles
> **the interval it was armed for** and says nothing about any moment outside it, so one armed
> across one load answers *"nothing wrote it during that load"* — not *"nothing ever writes it"*.
> The honest form of the observation is a watchpoint plus a stated interval, and the claim it can
> support is bounded by that interval. **A negative from a monitored window is a fact about the
> window.**

## 3. Types

`AuthoredTableHeader`, **at least 0x20** — reached through a qword registry slot. The size is a lower
bound from the registrar (§7), not a proven total: nothing observed shows where the header ends.

| offset | size | field | type | meaning | evidence |
|---|---|---|---|---|---|
| `+0x00` | 2 | `slotCount` | `uint16` | **the index bound of the encoded-pointer array that begins at `+0x04`** — consumers range an index `≤ +0x00 − 1` before loading `dword[+0x04 + idx*4]` and decoding it through `0020E600`. On `02EBF160` the array is read pairwise (`elem[idx]`/`elem[idx+1]` delimit a row range), so it carries `count+1` slots; on `02EBF168`/`02EBF170` it is a plain element count, and `02EBF170`'s decoded sub-tables repeat the same word as their own bound (`003214DF` reads `word[rax]` of the resolved table against `sel & 0x7FF`). **This field is per-band-family**: on ref-array bands `+0x04` is element 0 of the pointer array, not `rowCount`; the `+0x04` rowCount claim is scoped to the row-lookup family | `0023A717` (`02EBF168`, `[rsi+0x50]` bound loop), `002FE06C` (`02EBF168`, `edx` bound → `[rcx+rdx*4+4]` → `rbx+0x6E0`), `00308EE9`/`00308F11` (`02EBF160`, `0x8000+idx` bound → `elem[idx]`/`elem[idx+1]` weighted ranges), `003214CD` (`02EBF170`, `(sel>>0xB)&0x1F` bound) — function-list census over all 38,161 bodies, 2026-09-20 |
| `+0x02` | 2 | — | `uint16` | **reserved — no verified band-header reader.** The two sites previously attributed (`003155E6`, `003063C1`) read `+0x02` on resolved *row* pointers (`rsi`/`rcx` reloaded to element addresses before the read), not the header; the widened census finds zero accesses at band `+0x02` | function-list census over all 38,161 bodies, 2026-09-20; `003155CA`, `003063C1` re-read in context |
| `+0x04` | 4 | `rowCount` | `uint32` | **the row count, on row-lookup bands** — nine consumers bound an index on it with unsigned `jae` before resolving `+0x0C`; ~43 more use it as a loop bound or last index. On ref-array bands (`02EBF160`/`02EBF168`/`02EBF170`) the same dword is element 0 of the `+0x00`-counted pointer array — headers are not uniform across bands | 140 reads in the band-register census (FABLE's run: 120); `00237FF5`, `002388B5`, `0023AE25` |
| `+0x08` | 2 | `recordStride` | `uint16` | the distance between rows, **read at runtime, never compiled in** | 566 u16 reads across 264 functions; `00387707` |
| `+0x0C` | 4 | `recordArrayRef` | `uint32` | a reference to the row array, resolved by adding the global base; whether it is base-relative or a truncated absolute is the open point in §7 | 1100 reads across 227 functions, **every one of them 4-byte**; `003876E4` |
| `+0x10` | 4 | — | `uint32` | a second reference, rebased the same way | `00384614`–`0038461E` |
| `+0x14` | 4 | — | `uint32` | a reference to a **counted** sub-structure: rebased, passed through `0020E620`, then resolved and read as a word | `00384647`, `0038465D`, `00384688` |
| `+0x18` | 4 | — | `uint32` | a third reference | `00384625`–`0038462F` |
| `+0x1C` | 4 | — | `uint32` | a fourth reference, the highest field the registrar touches | `00384636`–`00384640` |

~~The registry is a band of qword slots at `02EBEF70..02EBF3FC`, 8 bytes apart.~~ The census band is `02EBEF70..02EBF3FC`, 8 bytes apart; the registry array inside it is `02EBF008`–`02EBF200`, and the band also holds other globals *(corrected 2026-10-02, OPUS: `00236C30+0x3E0` binds `02EBF008` and `00236C30+0x401` stores `02EBF200`; `02EBF000` is a float that `0039AF20+0x7` stores with `movss`, and `02EBEF78` is the EFX rebase table `003A9BA0+0x20` loads)*. **Forty of them are
headers of this shape.** Not all are: `02EBF190` holds `BattleSystemState`. Membership is established
by a slot exhibiting the idiom, never by its address falling in the band — a distinction that cost a
first measurement its extra fields.

## 4. Preconditions · postconditions · invariants

**Preconditions.** The registry slot must have been filled at load, and the reference at `+0x0C` must
resolve. Both are checked by the callers in this family, and §10.1 says what the checks actually do.

**Postconditions.** The computed address is `resolve(header->recordArrayRef) + header->recordStride *
index`. Nothing is written; the lookup is pure.

**Invariants.** The stride is *data*. Two builds of the same table with different row widths both work
without a code change, and **a reimplementation that hard-codes any row width is wrong even when it
matches today's data.** This is the single most important consequence of the whole shape.

## 5. State

| | fields / globals | evidence |
|---|---|---|
| read | the registry slot, `header+0x08`, `header+0x0C` | `003876D6`, `00387707`, `003876E4` |
| written | nothing | the shape is pure |
| allocated | nothing | |
| deallocated | nothing | |

## 6. Relationships

**Callees:** `0020E600` only.
**Callers:** 226 distinct functions across combat, equipment, status, gambits and formula code. The
busiest tables by distinct consumers: `02EBF138` (127), `02EBF0F8` equipment (40), `02EBF130` (21),
`02EBF118` status definitions (16), `02EBF040` (13), `02EBF038` (12), `02EBF0D8` gambit definitions (6).

## 7. State transitions

The lookup itself is stateless. The registry slots transition once, from null to filled, and the
transition is not a simple store — **it rewrites the header in place**, which this contract did not
say when it was first published.

`003845F0(slotAddress, headerAddress)` writes the header into the slot (`003845F4 mov qword ptr
[rcx], rdx`) and then, for each of `+0x0C`, `+0x10`, `+0x18` and `+0x1C` that is non-zero, **adds the
header's own 32-bit address to it** — converting a header-relative offset into the base-relative form
every consumer then reads. `+0x14` gets more: it is rebased, passed through `0020E620`, stored back,
and the result resolved and dereferenced as a word, so it points at a counted sub-structure.

Two consequences. First, `+0x18` and `+0x1C` are header fields, so the header is **at least 0x20**
and the 0x10 recorded before was too small. Second, and for a reimplementation the important one:
**a header read straight out of the file is not in the form consumers expect.** The references must
be rebased once, at registration, and rebasing them twice corrupts them exactly as silently as not
rebasing them at all.

### 7a. The registry map — which slot comes from which directory offset

**35 pairs**, decoded from `FUN_00236C30`. Each registration is `lea rcx, <slot>` /
`movsxd rdx, dword ptr [blob + N]` / `call <registrar>`, so a pair is the nearest preceding **lea** and
the nearest preceding **movsxd** before each call.

| blob | slot |
|---|---|
|`+0xC`|`02EBF018`|
|`+0x10`|`02EBF0B8`|
|`+0x14`|`02EBF0A8`|
|`+0x18`|`02EBF0B0`|
|`+0x1C`|`02EBF0C0`|
|`+0x24`|`02EBF0E0`|
|`+0x28`|`02EBF108`|
|`+0x2C`|`02EBF160`|
|`+0x30`|`02EBF110`|
|`+0x34`|`02EBF038`|
|`+0x44`|`02EBF130`|
|`+0x48`|`02EBF128`|
|`+0x4C`|`02EBF100`|
|`+0x6C`|`02EBF0C8`|
|`+0x70`|`02EBF020`|
|`+0x74`|`02EBF060`|
|`+0x78`|`02EBF0F0`|
|`+0x7C`|`02EBF0E8`|
|`+0x80`|`02EBF0A0`|
|`+0x84`|`02EBF098`|
|`+0x88`|`02EBF090`|
|`+0x8C`|`02EBF088`|
|`+0x90`|`02EBF080`|
|`+0x94`|`02EBF078`|
|`+0x98`|`02EBF070`|
|`+0x9C`|`02EBF068`|
|`+0xA8`|`02EBF050`|
|`+0xAC`|`02EBF048`|
|`+0xE8`|`02EBF058`|
|`+0xEC`|`02EBF040`|
|`+0xF4`|`02EBF030`|
|`+0xF0`|`02EBF028`|
|`+0xF8`|`02EBF170`|
|`+0x114`|`02EBF010`|
|`+0x118`|`02EBF008`|

**The order of those two instructions is not stable, and getting it wrong shifts the whole map.** The
first registration emits `movsxd` *before* `lea`; every later one emits `lea` first. A first version
of this section paired each `movsxd` with the **following** `lea` and was therefore **shifted by one
slot from the second row onward** — it produced 34 pairs and put the party definition table at
`+0x34`. It was published that way and is corrected here.

**Two independent checks say this version is right.** It reproduces §7's own example — the party
definition table at `+0x44` into `02EBF130`, which the wrong version contradicted — and it yields
**35** pairs, matching the count §7 already stated, where the wrong version gave 34.

**The map cannot be inferred, which is why an error in it is dangerous.** The directory has gaps, slot
order does not follow offset order, and nothing about a slot can be guessed from its neighbour, so a
reader has no way to spot a bad row. That is the argument for checking a decode against something the
database already knows **before** publishing it rather than after.

**TWO OF THE 35 GO THROUGH A DIFFERENT REGISTRAR.** `FUN_00236C30` makes **33** calls to `003845F0`
and **2** to `003846F0`. This section first said `003845F0` for all 35; the map's rows are right and
the mechanism named for two of them was not.

**AND IT IS ONE ORCHESTRATOR, NOT TWO PATHS.** An earlier revision of this section called the bespoke
binders "a separate path". They are not: `FUN_00236C30` **calls them itself** — `00237FC0`, `00238160`,
`00238660` and `00238880` are all invoked from it. The registry is filled by one initialisation
function using three mechanisms: register directly, register through the variant, or **delegate** to a
function that registers and then does more.

> **§15a, 2026-09-12 (OPUS): this map is not the roster behind §15's "40 registry slots", and
> should not be read as one.** The 35 mapped rows plus the four bespoke-binder slots below are **39**.
> Re-deriving §15's own criterion over the band gives **40**, and the two sets are not nested: three
> slots this map lists — `02EBF078`, `02EBF160`, `02EBF170` — **never feed both halves**, and four
> slots that do — `02EBF120`, `02EBF140`, `02EBF148`, `02EBF150` — **appear nowhere in §7**. The
> overlap is 36. **The count is right and the enumeration is a different set**, which is consistent
> with what this paragraph already says — the map is the *directory-bound* part, not the qualifying
> part — but a reader counting the rows to check the 40 will not get it.

**THE MAP IS THE DIRECT PART, AND THE FOUR TABLES THIS DATABASE CITES MOST ARE NOT IN IT.** The 35 rows
are internally consistent — 35 distinct slots, no duplicates — but §6's busiest consumers are absent:

| slot | what the database calls it | its own binder |
|---|---|---|
| `02EBF138` | 127 distinct consumers, the busiest | `FUN_00237FC0` (`00237FD5`) |
| `02EBF0F8` | equipment, 40 consumers | `FUN_00238160` (`00238169`) |
| `02EBF118` | status definitions, 16 | `FUN_003847B0` (`003847B3`) |
| `02EBF0D8` | gambit definitions, 6 | `GambitTargetDefinition_BindAndBuildMenuLookup` (`00238895`) |

**Each has a bespoke binder, all reached from the orchestrator, all ending at the same registrar.**
`FUN_00237FC0` does `movsxd rdx, ecx` — the header arrives as an **argument**, not from a blob
directory — then `lea rcx, <slot>` and `call 003845F0`, and then keeps working: it reads the slot back
at `00237FE3` and loops. The gambit one announces its extra work in its name.

**`02EBF118`'s binder is a tail-jump thunk and a `call`-matching sweep cannot see it.** `FUN_003847B0`
is fifteen bytes — `movsxd rdx, ecx` / `lea rcx, <02EBF118>` / **`jmp 0x3845F0`**. A sweep of every
`call 003845F0` in the image reports 36 registrations and **omits this one**; widening it to `jmp`
finds ~~exactly one tail-jump binder image-wide, this~~ six tail-jump sites: this one, `00238640` (into `02F973C0`, outside the registry) and four in `0023A160` (the `.ard` slots `02EBF120`/`140`/`148`/`150`), plus a seventh in `0023A160` that jumps to `003846F0` for `02EBF168` *(corrected 2026-10-02, OPUS: `003847B0+0xA`, `00238640+0xE` and `0023A160+0x22` / `0023A160+0x31` / `0023A160+0x40` / `0023A160+0x61` jump to `003845F0`, and `0023A160+0x52` to `003846F0`)*. Recorded because the same sweep briefly made the
status-definition table look unregistered.

So the registry is filled two ways: **35 tables in bulk from one blob's directory, and a handful
individually by functions that take the header as a parameter and then do more.** §7's count of 47
slots image-wide less these 35 leaves twelve, and four of the twelve are named here. A reader who took
§7a for the whole registry would conclude the busiest table in the game is unregistered.

**Limit:** this is the *correspondence*, not the contents. The directory offsets are immediates in the
code; what each entry points at is authored data loaded at runtime and is not in the image.

**Who fills the registry:** 47 slots image-wide, **35 of them by `FUN_00236C30` alone**, each from its
own offset in one blob's directory — the party definition table from directory `+0x44` into slot
`02EBF130`, for example.

> **An interpretation this contract does NOT settle.** The instructions above are certain; what the
> stored values *mean* is not. `0020E620` is the exact inverse of the resolver — `sub ecx, dword ptr
> [rip → 01F83530]` against the same global the resolver adds — so the pair converts between two
> address forms. But the registrar receives its second argument as `movsxd rdx, dword ptr [rax+0x44]`,
> a sign-extended **32-bit** directory value, and immediately stores it into the slot as a qword,
> while every consumer dereferences the slot as a pointer. Both are only consistent if the blob is
> mapped where a 32-bit value is a usable address, which decides whether `+0x0C` after registration
> holds a base-relative offset or a truncated absolute address. **That depends on the runtime value of
> the global at `01F83530` and cannot be read statically.** The arithmetic reproduces correctly either
> way — `resolve(x)` is `*(uint64*)0x01F83530 + (uint32)x` whatever `x` denotes — so §12 is safe to
> implement; the naming in §3 is the part that is provisional. Registered as J-C.
>
> *Static half settled 2026-09-12 (FABLE, J-C; a note only — the contract's own text is the
> owner's).* **⚠ Withdrawn as a proof 2026-09-24 (FABLE, Claude Opus 5.5) — kept as history; the
> reconciliation below replaces it.** ~~**The naming does not wait for the live read: the global is zero at every instant of
> the shipped process, so a stored reference is the low 32 bits of an absolute address.**~~ §2a
> already has the two halves — `01F83530` sits at `.data` `+0x193530`, past the section's raw
> data (`0x18E400`, so zero-initialised), and a capstone pass over every function finds exactly the
> two reads and no store, no `lea`, no address-taking of any kind ~~— and together they are a proof,
> not a lean: nothing in the image can give the qword a value, so `resolve(x) = (uint32)x` and
> `encode(p) = (uint32)p` for the whole life of the process (only injected code could change that).~~
> What the live read still confirms is **soundness**, not naming: the registrar's `movsxd` and the
> encoder's `dword` read are consistent only while every blob sits **below 2 GB**. The image gives
> that no guarantee of its own — it imports **no `VirtualAlloc`** (538 imports; the allocators are
> the CRT's `malloc` / `calloc` / `realloc` / `_aligned_malloc` from `api-ms-win-crt-heap-l1-1-0`,
> plus `GlobalAlloc` / `LocalAlloc`), so every blob comes from the process heap — but its header
> clears **`DYNAMIC_BASE`** (`DllCharacteristics 0x8120`; `HIGH_ENTROPY_VA` set is inert without it),
> and Windows applies no address-space randomisation to a process whose executable opts out, so the
> heap grows bottom-up from the lowest free addresses above the image at `00120000`. That the early
> blobs land below 2 GB is therefore an OS-policy fact the shipped game relies on, not an
> image-proven one; ~~the queued read of `01F83530` cannot come back non-zero, and~~ the discriminating
> live observation is the blob addresses themselves (any registered slot `< 0x80000000`). A
> reimplementation must reproduce the low-address placement or store 64-bit references.

### The image-address base: what the image initialises, and what later code could write — reconciled 2026-09-24 (FABLE, Claude Opus 5.5)

The struck note above, register rows `CD-2` and `UQ-83`, and a pending register verification all
turned one census into *"nothing can ever write the base"*. The census does not reach that far. The
base has two separate facts, and they are stated separately here.

**Initialised: zero, proven from the section table.** `01F83530` is `.data` `+0x193530`, and the
section's raw data ends at `0x18E400`, so the loader supplies zero. That is the value **at load**,
and nothing more.

**Writable: bounded by five routes, each swept with a control.** The artefact is
[`members/image_address_base_writer_bounds.py`](members/image_address_base_writer_bounds.py) (output
`members/image_address_base_writer_bounds.json`, repeat byte-identical). It sweeps every listed body.

| route | result | control that must fire |
|---|---|---|
| R1 rip-relative operands into `01F83430`–`01F83630` | the base has exactly **two**, both reads: `0020E602` (`add`, qword) and `0020E620` (`sub`, dword). The window has 65 rip writes, all to other cells. | the two reads are found, and at least one write in the window is classified as a write |
| R2 the window's address formed in a register (rip `lea`, `mov` immediate) | none for the base. **Two neighbours are taken: `01F83460` and `01F83580`.** | the neighbour `lea`s are found |
| R3 the address stored as data (64-bit VA, 32-bit VA, 32-bit RVA, every section) | none | a vtable slot known to be stored as data is found |
| R4 the two neighbours whose addresses are taken | **one route reaches the base**: `00210570`'s indexed store into the table above it (see below) | the constructor's last store at `+0xC8` is found, and so are `00210570`'s two indexed stores |
| R6 original-code replay of `00210570`, then the resolver `0020E600`, over the unmodified image bytes | id `0xFFFB` stores the texture pointer **into the base**, and `resolve(0x1234)` then returns `0x1234 + pointer`. Ids `0x0005`, `0x3FFF`, `0x4000`, `0x8000` and `0xFFFC` leave the base zero. | an in-range id leaves the base zero |
| R5 bulk writes (`memset`/`memcpy`/`memcpy_s`/`memmove`, `rep stos`/`rep movs`) with a static destination | 1,586 sites decoded. 58 resolve to a static destination with a length, and **none covers the base**. No static destination below it within 1 MiB has an unresolved length. The nearest ends at `01F810E0`. | a target placed inside `InputManager_Initialize`'s `memset` of `01F80F90` is reported |

**The neighbours are what the old census missed, and they are where a computed writer would have
to come from.**
- **`01F83460`, below: the static AMD Display Library wrapper.** It ends **exactly at the base**.
  The CRT initializer `0015DC80` constructs it through `0020D2F0`: `LoadLibrary` of `atiadlxx.dll`
  or `atiadlxy.dll`, then `GetProcAddress` for the `ADL2_*` entry points. The constructor's last
  field store is the qword at `+0xC8`, so the object is `0xD0` bytes and `+0xD0` **is** `01F83530`.
  Its address **escapes**: `0020D2B0` publishes it into `01E02588`, and `0020D2F0` passes `this+0x10`
  to `0020E420`. R4 swept 50 functions: those that take the address, the constructor, the
  destructor `008A7360`, the three vtable slots of `009064B8`, and the whole compiland
  `0020C600`–`0020E600`. It found only the constructor's own stores at `+0xC0`/`+0xC8`. Nothing
  stores at `+0xD0` through `this`, or at `+0xC0` through `this+0x10`.
- **`01F83580`, above: the PS2 texture-id table, 16-byte entries.** Its two readers (`0020EB60`,
  `0020F250`) index it with `((TEX0 >> 37) & 0x3FFF) × 16`, which is never negative. **Its writer is
  not bounded below.** `00210570` is the bind that `GiSetTexture`'s execute slot `00863040`
  tail-jumps to (vtable `01CCFA30` slot 1). It does:

  ```
  00210570  mov eax, 0x4000
  00210575  cmp cx, ax ; jge skip          ; a SIGNED 16-bit test: upper bound only
  0021057A  movsx rax, cx                  ; ids 0x8000-0xFFFF become -32768..-1
  00210588  mov [01F83580 + rax*16], rdx   ; the texture pointer
  0021058C  mov [01F83580 + rax*16 + 8], r8d
  ```

  So **id `0xFFFB` (-5) stores the texture pointer into `01F83530`, the base itself.** The replay
  (R6) shows it end to end on the original bytes. More generally, ids `0x8000`–`0xFFFF` write 16-byte
  entries anywhere in the 512 KB of `.data` below the table.

**Is that route driven in the shipped game? Not by any id producer read here.** `GiSetTexture`
records are built only by the factory `00863060`, whose two callers take the id from the texture
pool:
- The allocator `002D81D0` hands out ids between `[02F8F20C]` and `[02F8F208]`. `002D7FC0` sets
  those to `0x3B00 + d` and `0x3C00 + d`, where `d = (W − 0x200) × 21` when the PS2 frame width
  `W = [022D8EAC]` exceeds 512, and 0 otherwise.
- `W`'s only rip-relative writer stores the constant `0x200` (`0036D286`), so **d = 0 and the
  pooled ids are `0x3B00`–`0x3BFF`**.
- `002D7D50` re-derives its id as `(key >> 37) & 0x3FFF`.
- `002D7D90`, `002D7E00` and `002D83B0` pass through a caller's id.

At the shipped width no producer read emits an id with bit 15 set. The route's safety is therefore
**a property of the id discipline and a constant width, not of the code**. A frame width above
about 1,353 would push the pool past `0x8000`. Some widths put `0xFFFB` inside the pool's 256 ids:
2,902–2,913 is the first such band, and the 16-bit wrap repeats it at larger widths.

A well-formed member write of the ADL wrapper cannot reach the base. The texture table's writer
**can**, with an out-of-range id.

**So the honest statement is:** the base is **zero at load**. **One in-image store route reaches
it**, and the producers read here do not drive that route at the shipped width. **Not excluded:**
- the three pass-through id sources' own callers;
- stores through a register computed from an unrelated base (pointer arithmetic, aliases), and the
  1,528 bulk-write sites the census could not pin to a static destination with a length;
- code outside the executable: CRT and Phyre modules, the OS, injected DLLs.

**One live read agrees:** EXP-002 read `0` at the title screen. That is a moment, not the process
life (§2a). **"The base is zero for the whole process" is well supported and not proven.** The
naming in §3 (a stored reference reads as the low 32 bits of an absolute address) rests on that
support, and it is stated as *supported*.

> **For a reimplementation and for modding:** keep `GiSetTexture`'s id check **unsigned**
> (`id < 0x4000`). A texture-pack mod that raises the frame width or feeds its own ids through
> `00863060` can silently rebase **every authored-table read in the game** through this one store.

**A zero at load is also not evidence about producers.** The codec fixes the **range** a stored
reference can address (§10.1). It does not say which code produced the referenced bytes. That
question belongs to the registrar and the allocator (§7, `1a`).

**Read two later quotes with this scope.** The 2026-09-20 ruling below quotes the lifetime page:
*"the two functions are therefore truncation and zero-extension in every shipped path"*. It also
leans on the OPUS type rows' *"IDENTITY on the unsigned 32-bit domain"*. Both are exact **at base
zero**. Base zero is the load-time value, and this section shows that the one store route able to
change it is not driven by the id producers read. So both quotes are supported claims, not
process-life facts. The ruling's own conclusion does not depend on them: range, not storage kind.

## 8. Script · resource · event interactions

This *is* the resource interaction. Everything authored that combat code reads — status definitions
with their duration units and clear masks, equipment rows, gambit definitions — arrives through it.
A mod that changes a table's row width changes `+0x08` and nothing else has to move.

## 9. Determinism

Fully deterministic and frame-independent. No RNG, no timing, no shared state. Called from whichever
thread the consumer runs on, with no synchronisation, which is safe only because nothing writes.

## 10. Failure paths and edge conditions

1. **Both guards exist and neither returns.** The callers test the slot for null and the resolve for
   zero — and on either failure they fall into the *same* row read with the base register zeroed.
   `BattleStatus_ComputeDefaultShortTimer` takes `je 00387712`, `xor ecx, ecx`, and then reads
   `byte ptr [rcx + 9]` — **address 9**. The status-write cascade takes `xor edx, edx` / `mov ecx,
   edx` at `0030E686` and then reads `dword ptr [rcx + 0xc]` — **address 0xC**. The branch is
   compiled as a value guard, not a control guard: it selects a null base and proceeds to
   dereference it.
2. **So a missing table faults rather than degrades**, and that is the original's behaviour on both
   paths examined. A reimplementation that returns a default instead is **more defensive than the
   original and must declare it** — this is a parity difference of exactly the kind
   `CONTRACT-persistent-flag-banks.md` records as DX-1, arrived at independently here.
3. **The index is not bounds-checked in the canonical shape** — `003876D0` and its siblings
   index without testing. But §14 item 1's closure changes the second half of this sentence:
   the header *does* state a row count (`+0x04`), and **nine** consumers do check it before
   resolving `+0x0C`, all with the unsigned `jae` of a count guard (`00237FC0`, `002388B5`,
   `0023AE25` re-verified 2026-09-20). So bounds-checking is *per-consumer*: the canonical
   shape carries no check, the checking consumers carry their own, and a reimplementation
   that bounds-checks the canonical shape would be more defensive than the original at those
   sites while matching the nine guarded ones.

## 11. Observable behaviour

In memory: for a table whose slot is known, `*(uint16*)(slot_target + 8)` is the row width and rows
begin at the resolved reference. Changing the stride and re-laying the rows changes every consumer at
once with no code change — which is both the observable prediction and the modding consequence.

## 12. Reproduction formula

```
row(slot, index):
    header = *(void**)slot
    if header == 0:              base = 0          # NOT a return - see 10.1
    else:
        base = ImageAddress_ResolveRuntimePointer(*(uint32*)(header + 0x0C))
        if base == 0:            base = 0
    stride = *(uint16*)(header + 0x08)             # on the failure path this reads from 0
    return base + stride * index
```

The formula is written to show the failure path faithfully. Reproducing it *as written* will fault
where the original faults; reproducing it with an early return will not, and that is the declared
difference.

## 13. Runtime validation

**Evidence class: isolated original-code, over the resolver, its inverse and one worked instance.
Arena placement **observed live**: [`EXP-079`](../_experiments/EXP-079-arena-live-placement.md)
(ASTRA, `method: C`, `live_game: true`) saw it in two named states; §15 carries it at tier 3,
PARTIAL — two states are not all-time safety and the 4 GiB question stays unsettled.
~~No live run stood behind this header~~ (2026-09-12); superseded 2026-09-16 (SWE2-ORACLE,
`OPUS-CONTRA-AUTHORED-TABLE-LIVE-CLAIM`).**

**What ran:** `0020E600`, `0020E620` and `BattleStatus_ComputeDefaultShortTimer` `003876D0`, as
shipped bytes under Unicorn at their real virtual addresses. **The instance's own call to the
resolver is not stubbed** — the real three instructions run inside it, which is the point of
executing a shape rather than a subsystem. The base at `01F83530`, the registry slot at `02EBF118`
and the scale at `01DFE0B4` are planted. The slot is the one §7a's registry map names **status
definitions, 16 bytes a row, registered by `FUN_003847B0`** — so the byte the instance reads at
`+0x09` is a field of a status definition, and the stride the fixture drives is that table's own.
**What did not run:** the other 225 functions that perform this lookup, and whatever fills the base
at runtime.

**Instrument:**
[`diff_table_lookup.py`](../../../Reconstruction/Tests/Differential/diff_table_lookup.py) against
[`table_lookup.c`](../../../Reconstruction/Game/Resource/table_lookup.c).

**Result: 387 commands, 145 compared lines, 0 mismatches** — 27 distinct resolve results out of 29,
and **33 resolver calls across 21 timer calls**, which is the double resolve below counted.

> **The command count was `386` until 2026-09-12 and the run reports `387`.** Corrected by re-running the
> suite rather than by quoting it. One stale digit is harmless; the habit that produced it is not, which
> is why §15's matching figure is corrected in the same pass.

### The mutation campaign

**11 mutants: 8 KILLED, 0 SURVIVED, 3 EQUIVALENT, 0 INVALID, 0 NO_BUILD**, with
`production_inputs_stable: true` and the four input hashes re-checked against the files as published.

**Getting to no survivors took three fixture changes, and each one was the same lesson: a value the
fixture supplies is a value the suite cannot test.** The first run left four survivors, all of them
defaults overwritten before they could matter — the three globals' initialisers, dead because every
case began by resetting them, and the row address's initial value, invisible because page zero was
uniformly zero on both sides. A case that runs **before any reset** made the initialisers live, and a
**planted page zero** made the null path's read at `+9` distinguishable from `+8` or `+10`. That
still left the timer scale, because the pre-reset case reads a **zero** byte and any scale times zero
is zero; planting a non-zero byte at address 9 closed it. The first of those changes is what caught
the scale error recorded above.

### EXP-077 — what it establishes for this contract, and what it does not

**Consumed 2026-09-12 (OPUS), from [`EXP-077`](../_experiments/EXP-077-arena-initializer-address-width.md)
(ASTRA).** The arena initializer `00369D30` (707 B), its block-header writer `0036A490` (215 B) and
this contract's own encoder `0020E620` (9 B) were executed as shipped bytes under Unicorn with one
`sprintf` stub.

**Verified here before being consumed**, against the image rather than the record: all three body
SHA-256 match, `00369D44` is `4C 8B F2` (`mov r14, rdx`), and the id bound at `00369D47` is
`cmp esi, 0xE` / `ja` — **unsigned**, which is what rejects the negative id after `00369D3B`
sign-extends it. **The record is accurate on every point checked.**

| what it establishes | what it does NOT |
|---|---|
| **The initializer imposes no low-address ceiling.** Backing at `40010000`, `80010000` and `100010000` all returned with the full pointer layout retained in the record's **direct** pointer fields (`+08`, `+20`, `+28`, `+30`, `+38`, `+40`, `+90`, `+98`) | that a high backing address is **safe**. Initialization is not allocation, and none of the later link, split or release paths ran |
| **A pointer truncation is detectable**: the private `mov r14d, edx` mutant stores `10000` and faults at `00369E4C` | anything about the native allocator, the boot sequence, or placement in a running process |
| the unsigned `id > 14` rejection, and that invalid ids write nothing outside the stack | that ids are bounded anywhere else |

> **The limit this contract has to add, because it owns the encoder.** **All 36 encoder calls across
> EXP-077's six cases took the argument `0`** — checked in the sealed
> [`initializer-result.json`](../_experiments/evidence/resource-arena-backing/initializer-result.json),
> not inferred from the prose. So the experiment drives the encoder's **call sites** and never its
> **arithmetic**, and it contains no evidence about encoded links at any address, high or low.
>
> **And by §2a's sharpened condition, the high case could not have round-tripped.** EXP-077 ran with
> the decoder base at zero and backing at `100010000`; `p - base = 0x100010000 >= 2^32`, so
> `encode` truncates it to `00010000` and `decode` returns `00010000`, not the backing pointer.
> **The direct pointer fields retain a high address and an encoded link cannot.** Those are two
> different fields of the same record, and reading the first result as permission for the second is
> the specific mistake available here.

### EXP-078 — the same bound, failing as a WRITE SOMEWHERE ELSE

> **The block header is now in the type store** as `ImageAddressArenaBlockHeader` (`CLASSIFIED / HIGH`, size UNRESOLVED), beside `ImageAddressArenaRecord` (`0xA8`) which is a different object. The two neighbour links are `PROVEN`; **the free-list pair at `+0x04` / `+0x08` is `DISCOVERED / PROBABLE` and deliberately not assumed to match**, because EXP-078's two inserters were loaded and never reached.

**Consumed 2026-09-12 (OPUS), from [`EXP-078`](../_experiments/EXP-078-arena-allocation-link-width.md)
(ASTRA).** Seven original cases on EXP-077's sealed output, **with no callee stubs in the allocation
stage**, asking what happens when the allocator actually *creates and later consumes* encoded
neighbour links.

**Re-read here before being consumed** — and **the direction was inverted until 2026-09-13**
(`ASTRA-CONTRA-OPUS-ARENA-UNLINK-CONSUMER`). The mechanism is four instructions of `0036C9D0`:

```
0036CA52  mov  ecx, [rbx + 0x10] / call 0x20e600   ; rsi = decode(+0x10) = the SUCCESSOR
0036CA5A  mov  ecx, [rbx + 0x0C] / call 0x20e600   ; rdi = decode(+0x0C) = the PREDECESSOR
0036CA70  call 0x20e620                            ; encode(rdi) = encode(predecessor)
0036CA75  mov  dword ptr [rsi + 0xc], eax          ; successor->+0x0C = encode(predecessor)
0036CA85  call 0x20e620                            ; encode(rsi) = encode(successor)
0036CA8A  mov  dword ptr [rdi + 0x10], eax         ; predecessor->+0x10 = encode(successor)
```

> **Both register labels were swapped**, and the structure stayed a correct doubly-linked unlink
> either way - which is why it read plausibly for weeks. `+0x0C` is the *previous* neighbour and
> `+0x10` the *next*, so removing a block writes its predecessor into the successor's prev slot and
> its successor into the predecessor's next slot. **The old comments said the opposite of both.**

**The pointers it stores through are the DECODER's output.** `0020E600` is
`base + zext32(reference)`, so with the base at zero a block at `P = 0x100010000` has its header
reference decode to **`0x10280` — the low 32 bits — and the store goes there.** The recorded faults
land at `0x10280 + 0x10 = 0x10290` and `0x10FF80 + 0x0C = 0x10FF8C`, which is exactly where those
two instructions write.

| what EXP-078 establishes | what it does NOT |
|---|---|
| **Initialization surviving a high backing pointer does not mean later operations do.** EXP-077's high case returned correctly; the *second* allocation faults at a predicted store | that the shipped game ever places its arena there. **Actual placement and lifetime remain open** |
| **The failing fields are the NEIGHBOUR links at `+0x0C` / `+0x10`, not the free-list links at `+0x04` / `+0x08`** — different fields, and only the former go through the decoder here | that the free-list links are safe; they were simply not the path this experiment exercised |
| a low mirror makes the second allocation **return the correct high pointer while writing into the separate low region** — five recorded events at `0036CA8A`, `0036CA8D`, `0036B83E`, `0036B853`, `0036B856` | **persistent corruption or a crash.** The mirrored bytes end **unchanged**: `0x10290` is cleared and restored and the word was already zero. **Wrong-region access is the finding; corruption is not** |
| **a return-value-only comparison would pass a broken link.** The targeted control made the decoder ignore its reference; both allocations still returned the expected low pointers, and only the predecessor assertion caught that `+0x0C` had become zero | that any historical campaign covered this — none was rerun |

> **This is §2a's bound failing in practice rather than in algebra.** The round trip is exact only
> while `((p - base) mod 2^64) < 2^32`; a block 4 GiB above a zero base violates it, and the
> consequence is not a wrong number handed back — **it is a dword written into whatever occupies the
> truncated address.**

> **And it changes what a parity test for this shape has to compare.** §16's `CONTRACT` dimension
> asks for computed row addresses; **that is not enough for the arena.** A suite that compares
> returns alone passes the broken-predecessor control. **Links have to be asserted.**

**Two further details read here and not in the record's summary.** After unlinking, `0036CA92`
writes the word **`0xFF99`** over the block's header word — where an initialised free block carries
`FF12` (§EXP-077) — so **an unlinked block is tagged, not merely relinked**; and both stores are
accompanied by a word write at the neighbour's `+0x3E`, which is the second field this path touches
and is unexplained.

**The three equivalences are the addresses themselves** — `01F83530`, `02EBF118`, `01DFE0B4` — which
the reconstruction carries as documentation and never dereferences, because the fixture supplies
those globals' *values* directly.

### The failure path, now executed, and a one-sided probe

§10.1 is confirmed rather than corrected: the null test selects a zero base and reads through it.
The fixture maps a page at address 0 so both sides can be compared over that path — and a **separate
one-sided probe unmaps it and calls the shipped bytes again**, which faults:
`Invalid memory read (UC_ERR_READ_UNMAPPED)`. So §10.2's warning is now carried by a run: a
reimplementation that returns a default here is more defensive than the game, and that has to be a
declared decision.

### The double resolve

The instance loads `02EBF118` three times (`003876D6`, `003876F1`, `00387700`) and calls the resolver
**twice** on the same reference (`003876E7`, `003876FB`), testing only the first result. It is sound
only because the base cannot change between the two calls. The reconstruction reproduces both calls,
and the control that resolved once — which is how anyone would naturally write it — **failed on 43 of
135 lines**, because the call count is visible to anything watching the resolver.

### The row address is built in 32-bit arithmetic, and the harness nearly hid it

`0038770B imul ecx, ebx` and `0038770E add ecx, eax` are both 32-bit, so the 64-bit base the resolver
just produced is **truncated** before `movzx eax, byte ptr [rcx + 9]` reads through it. The suite
drives a stride and index whose product is exactly `2^32`, where a 64-bit reimplementation reads a
different row; the control doing the arithmetic in 64 bits **failed on 2 of 135 lines** as the suite
then stood.

**That control passed twice before it failed**, and the reason is worth recording: the harness's row
read originally took a **32-bit** address, so the interface performed the truncation itself and no
reconstruction could get it wrong. Widening that parameter to 64 bits is what made the property
testable. *A harness interface narrower than the thing under test silently proves the thing under
test.*

### What is still owed, and it is live-only

§11's observation is unchanged and still worth one reading: a known slot's `+0x08` against the row
width the authored data actually uses. Nothing here bears on what writes `01F83530` — it is `.bss`,
begins as zero, and ~~no instruction in the image writes it~~ one in-image store can write it *(corrected 2026-10-02, OPUS: the texture-id table writer's `+0x18` reaches it for id `0xFFFB`, its `+0x5` compare being signed; undriven, not absent - §7's reconciliation)* — nor on the `.data` dword at `01DFE0B4`.

**A correction made by the run, 2026-09-12.** A draft of this section said that dword was **zero in
the shipped image**, taken from a disassembler annotation printing the QWORD at that address —
`3F80000001000000`, whose high half is the `1.0f` at `01DFE0B8` that the HP write uses as its time
scale. Read out of `.data` directly the dword is `01 00 00 00`, **one**. The suite caught it: the
case that runs before any fixture reset, added so the reconstruction's initialisers are tested
against the image's own initial state, failed until the initialiser said 1.

**Experiment records that name this contract** — found by `OPUS-CONTRACT-RUNTIME-AUDIT`, 2026-09-13. Each names this
contract in its own `contract:` frontmatter while this section did not cite it back.

- [`EXP-079`](../_experiments/EXP-079-arena-live-placement.md) — **method -**, no declared method; cited in section 15, not here.

**None of these is a live run**, so none of them changes the evidence-class statement at the
top of this section. They are listed because a reader auditing what has been executed against
this contract should not have to find them from the experiment side only.

## 14. Unresolved

1. ~~**The row count for any table.**~~ **RESOLVED 2026-09-20 (SWE2-CONTRACT), accepting FABLE's
   J-A census and re-verifying it.** `+0x04` is a `uint32` row count, and the consumers that
   check it read it exactly as one. Independent reproduction of the band-register census (every
   `mov r, [rip → 02EBF000..02EBF178]` in the image — 1,799 loads — with the header offsets the
   destination register is then read at inside a 96-byte window) finds the same population
   shape FABLE reported: `+0x04` read 140 times (their run: 120 — the difference is window
   policy, not disagreement), `+0x08` 583 (their 592), `+0x0C` 1,001 (their 1,034), plus `+0x00`
   23 and `+0x02` 11 — both word reads, now in §3 as unassigned u16 fields. Three of the nine
   claimed bound-checkers re-verified in the image: `00237FF5` (`cmp esi, [rdx+4]; jae`, slot
   `02EBF138`), `002388B5` (same shape, `02EBF0D8`), `0023AE25` (`cmp ebx, [rax+4]; jae`,
   `02EBF038`) — each guards the index before resolving `+0x0C`. §3's field table now carries
   `+0x04` as `rowCount`, and §10.3 is corrected: bounds-checking is per-consumer, not absent.
   **Follow-up 2026-09-20 (SWE2-CONTRACT): the `+0x00`/`+0x02` residuals are also closed.** A
   function-list census (all 38,161 bodies, register tracked until rewrite or clobbering call)
   attributes `+0x00` to **four true readers**, all the same shape — an index is ranged
   `≤ word[+0x00] − 1` before a `dword[+0x04 + idx*4]` load is decoded through `0020E600`:
   `0023A717` (`02EBF168`), `002FE06C` (`02EBF168`), `00308EE9`/`00308F11` (`02EBF160`, pairwise
   `elem[idx]`/`elem[idx+1]` row ranges for `0x8000+idx` weighted ids), `003214CD` (`02EBF170`,
   `(sel>>0xB)&0x1F`; the decoded sub-table's own `+0x00` then bounds `sel&0x7FF` at `003214DF`).
   So `+0x00` is `slotCount` — the bound of the encoded-pointer array at `+0x04` — and `+0x04`
   is element 0 of that array on these bands: **the header is not uniform across band families**.
   `+0x02` has **zero** verified band-header readers — `003155E6` and `003063C1` read `+0x02` on
   resolved row pointers — and is dispositioned reserved.
   > *Answered 2026-09-12 (FABLE, J-A; a note only — the contract's own text is the owner's).* **The
   > header does carry it: `+0x04` is a `uint32` row count, and the consumers that check it read it
   > exactly as one.** A census keyed on the registry band rather than on the stride — every
   > `mov r, qword ptr [rip → 02EBF000..02EBF178]` in the image (239 functions) and the header
   > offsets that register is then read at — finds **120** reads of `+0x04` beside the 592 of
   > `+0x08` and 1,034 of `+0x0C` the contract already counts (and 24 of `+0x00`, 13 of `+0x02`,
   > which §3 also omits). **Nine** consumers bound an index on it before resolving `+0x0C`, all
   > with the unsigned `jae` of a count check: `00237FC0` (`00237FF5`, slot `02EBF138`),
   > `GambitTargetDefinition_BindAndBuildMenuLookup` (`002388B5`, `02EBF0D8`),
   > `BattleStats_InitializeDefinitionRecord` (`0023AE25`, `02EBF038`),
   > `Inventory_InitializePrimaryStateFromAuthoredTable` (`0023AF80`, `02EBF048`), `002FA920`
   > (`002FA9F0`, `02EBF058`), `BattleStats_ComputeLpIncludingOwnedLicenseCosts` (`003237F5`,
   > `02EBF038`), `BattleMenu_BuildCommandEntryList`, `00239960` and `0033A720`. **Forty-three**
   > more read it as a loop bound or a last index (`mov ebp, [hdr+4]` then a counted walk in
   > `00295FE0` / `002960B0`; `[hdr+4]` then `dec eax` in `00239960` / `BattleUnit_ApplyUnitDefinition`
   > `0023A656`). The remaining consumers — roughly 190 of the 239 — index without reading it, so
   > **each of those carries its own bound** (an id drawn from another table, or a literal cap such
   > as `0023AE10`'s `cmp esi, 6`); the safety question is therefore per-consumer and now checkable
   > against a field, not unanswerable. The registrar's rebasing loop over the `+0x14`
   > sub-structure (`00384688`, a word count at its head) is a separate count for a separate array.
1b. ~~**What the word at a block header's `+0x3E` is.**~~ **RESOLVED 2026-09-20 (SWE2-CONTRACT),
   adopting the type store's `guardWord` row and re-verifying it.** `+0x3E` is the last two
   bytes of the `0x40` block header — a **guard word every writer stores zero to and every
   reader compares against zero**. The type store
   (`ImageAddressArenaBlockHeader.0x3E = guardWord`, CLASSIFIED / HIGH, OPUS 2026-09-20)
   measured it over all 38,161 function bodies: 92 word accesses at displacement `0x3E`,
   36 in the arena manager; **all 33 header stores settle zero** (immediate, `xor`-self, or
   registers proven zero by hand — `bp` after `xor ebp,ebp` at `0036AF3D`/`0036C4CC`, `r14w`
   after `xor r14d,r14d` at `0036A351`); the only non-word overlaps are descriptor `+0x38`
   qword stores on a different base and two `lea +0x3F` align-ups that dereference nothing.
   **Re-read independently:** all five `cmp word [rdx+0x3E],0` gates — `0036B8C3`, `0036B743`,
   `0036B683`, `0036B803`, `0036CB76` — take the identical `!= 0 → 0036A570` arm (the arena's
   dump reporter, flags `edx = 0xB`), and the free path's own gate is `00369A80`, the
   "MCB Broken" abort (`exit(1)`). Every writer sampled in the image stores zero: the unlinker
   `0036C9D0` clears it on all four relinked neighbours and the block (`r14w = 0` at
   `0036CA20`/`0036CA35`/`0036CA78`/`0036CA8D`/`0036CAB8`), the inserters and linker clear it
   the same way, and the allocator `0036BC60` stores `r13w = 0` at `0036BE91`/`0036BEA5`.
   **So the field is a corruption sentinel, not program state**: nonzero is not a value the
   code can produce — it detects foreign damage (an overrun of the unbounded `+0x34` string
   copy is the store's named candidate; payload underrun is the other arm). The report arms
   are armed-but-dead in the shipped image — reachable only through memory corruption, which
   is exactly what they exist to catch.
1c. ~~**Whether the free-list links at `+0x04` / `+0x08` go through the decoder too.**~~
   **RESOLVED 2026-09-20 (SWE2-CONTRACT) — yes, both directions, and the direction
   assignment is now settled.** The encoding half was already answered in the type store
   without reaching an inserter (`ImageAddressArenaBlockHeader.0x04/0x08`: the unlinker's
   unconditional prefix decodes `+0x08` at `0036C9EB` and `+0x04` at `0036C9FF` through
   `0020E600` and re-encodes through `0020E620`). What the store left open — **which field
   is forward and which is back** — the two never-reached inserters answer statically.
   Read in full, they are mirror-image insert operations on a doubly-linked list:
   `0036B670` decodes `rcx->+0x08` to find the forward neighbour `rbp`, then stores
   `rsi->+0x08 = enc(rbx)`, `rbp->+0x04 = enc(rbx)`, `rbx->+0x04 = enc(rsi)`,
   `rbx->+0x08 = enc(rbp)` — insert `rbx` between `rsi` and `rbp`. `0036B730` is the
   same surgery mirrored: decodes `rcx->+0x04` for the back-side neighbour, stores
   `rsi->+0x04 = enc(rbx)`, `rbp->+0x08 = enc(rbx)`, `rbx->+0x04 = enc(rbp)`,
   `rbx->+0x08 = enc(rsi)`. When `rsi == 0` both encode `0` into the new block's two
   links — the empty-list case. **So `+0x04` is `prev` (back link) and `+0x08` is
   `next` (forward link)** in the free list — an encoded doubly-linked chain exactly
   like the `+0x0C`/`+0x10` neighbour pair. Each inserter also runs the `+0x3E`
   guard-word gate on entry (`cmp word [rdx+0x3e],0` → `0036A570` report on nonzero,
   then the `008C2D80` `int3` thunk) and clears `+0x3E` on every block it touches —
   consistent with the `guardWord` disposition above. EXP-078's note stands: the
   inserters were loaded but never reached, so this direction reading is static
   evidence, not executed.
1a. **Whether any arena backing ever sits more than 4 GiB from the decoder base**, measured as
   the unsigned 64-bit distance §2a fixes the round trip to. EXP-077 shows the *initializer* accepts
   a backing
   pointer outside that window and stores it whole in the record's direct fields. So the question is
   whether the allocator can ever produce one in a running process — an **allocator and placement**
   question, and live.

   > **It is NOT a question about the encoder, and a first draft of this item said it was.** The
   > encoder is `sub ecx, dword [01F83530]`: it reads **`ECX`** and therefore **cannot see bits
   > 32–63 of its argument at all**. There is no input at which it "notices" a high pointer and no
   > case that could show one — `encode(p)` is `trunc32(p) - lo32(base)` by construction, which the
   > pilot's existing 32-bit cases already establish. **Building a case to drive a >4 GiB pointer
   > through it would measure nothing the existing cases do not**, and queuing one would have been
   > manufacturing coverage. The algebra is the proof; what is missing is an observation of the
   > allocator, not of this function.
2. **What the other slots in the band point at**, beyond `02EBF190` being `BattleSystemState`.
   **NARROWED 2026-09-20 (SWE2-CONTRACT) — the STATIC delivery's population map is now fully
   enumerated in the image.** The plumbing is one registration, one callback:
   `BattleStorage_InitializeWorkArrays` registers the delivery stub `00238850` for loader
   `0x13` `"STATIC"` via `003843F0` at `002369CE` — the only `003843F0` call site in the
   image. On delivery `00238850` binds the blob pointer cell `0208E680` through the
   `003846F0` variant binder and tail-jumps to `00236C30(1)`, whose populate arm tears down
   the prior blob (`00384500`, clears `0208E680`), stores scalar `blob+0x04`→`02EBF180`,
   then binds **35 band slots** — 33 through the standard rebase binder `003845F0` and 2
   through the `003846F0` variant, `blob+0x2C`→`02EBF160` and `blob+0xF8`→`02EBF170` (the
   two `slotCount`/ref-array bands of §3), plus scalar `blob+0x11C`→`02EBF200`.
   (`00236C30(0)` re-registers `00238850` — the no-blob arm, reached only through the
   registered-callback path.) Six more calls consume the blob whole; ~~three of them are~~ five of them are
   inner binders that fill ~~four~~ five additional slots — `00237FC0`→`02EBF138`,
   `00238160`→`02EBF0F8`, `00238880` (`GambitTargetDefinition_BindAndBuildMenuLookup`, fed
   `blob+0x20`)→`02EBF0D8`, ~~and~~ `00238660`→`02EBF158` and `003847B0`→`02EBF118` *(corrected 2026-10-02, OPUS: `00236C30+0x164` calls `003847B0` with `blob+0x40`, and `003847B0+0x3` names `02EBF118` before its `jmp 0x3845f0`)*. **~~39~~ 40 of the 47 slots' provenance is
   thus named.**
   The remaining ~~eight — `02EBF000`, `02EBF0D0`, `02EBF118`, `02EBF120`, `02EBF140`,~~ seven split: the five `.ard` slots `02EBF150`, `02EBF168`, `02EBF120`, `02EBF148` and `02EBF140` are bound by the dispatcher `0023A160` through tail-jumps, and only `02EBF000` and `02EBF0D0`
   ~~`02EBF148`, `02EBF150`, `02EBF168` —~~ have **no binder-family provenance** *(corrected 2026-10-02, OPUS: `003847B0+0xA`, `00238640+0xE` and `0023A160+0x22` / `0023A160+0x31` / `0023A160+0x40` / `0023A160+0x61` jump to `003845F0`, and `0023A160+0x52` to `003846F0`)*: the
   `003845F0`/`003846F0` caller census is complete ~~(36 and 5 sites, all enumerated above or~~ for `call` (36 and 5 sites), and the tail-jumps add six and one,
   ~~internal)~~, so those slots are either written by non-binder paths (`0039AF20`'s float
   block is the known example) or delivered by other loader ids; their contents are authored
   data either way, which the image cannot name.
3. **Whether the two null guards are reachable at all.** If the registry is always filled before any
   consumer runs, the near-null reads are dead code and the parity difference in §10.2 is moot. That
   is a runtime question and §11 does not answer it.
   > *Static half settled 2026-09-12 (FABLE, J-B; a note only — the contract's own text is the
   > owner's).* The slot band `02EBF000`–`02EBF178` has **no rip-relative writer in the image** (a
   > capstone pass over every function; ~~the only stores in the band are~~ the stores in the band are `00238660`'s `02EBF158`
   > and `0039AF20`'s float block, and `00324510`'s two at `02EBF178` *(corrected 2026-10-02, OPUS: `00324510+0x48` and `00324510+0x18A` store `rax` there)*) — every slot is written **through the pointer** the binder
   > `00236C30` hands to `AreaData_BindAndRebaseSectionDescriptor` (`003845F0`), which stores its
   > `rdx` **unconditionally** (`003845F4`), so a blob whose directory entry resolves to null leaves
   > the slot null rather than untouched. `00236C30` is ~~not called by anyone: it is~~ tail-jumped to by the registered stub `00238850` *(corrected 2026-10-02, OPUS: `00238850+0x1F` `jmp 0x236c30` with `ecx = 1`; the call at `002368D0+0xFE` registers `00238850`, whose address `002368D0+0xF7` loads)*, the body of the **delivery
   > callback** `BattleStorage_InitializeWorkArrays` registers at boot for loader id `0x13`, name
   > `"STATIC"` (`002369BB`–`002369CE`: `003843F0` → ~~`00384420(0x13, 00236C30, "STATIC", 4, 6, 4)`~~ `00384420(0x13, 00238850, "STATIC", 4, 6, 4)` *(corrected 2026-10-02, OPUS: `002368D0+0xF7` loads `00238850` into `rdx`)*, the
   > same request path [the registry page](authored-data-table-registry.md) §M-7 documents for ids `0x47`–`0x52`), under the bootstrap
   > frame `0022A0B0` ← `0017D4C0`. So the band is **null from process start until the STATIC blob
   > is delivered**, and the guards are reachable in exactly two cases: a consumer ticking inside
   > that boot window, or a STATIC blob missing the entry. Which of the two the shipped game can
   > produce is the live half — discriminating observation: a breakpoint on `00387712` or `0030E686`
   > with the slot null before any battle frame; expected never to fire with the shipped `STATIC`.

## 15. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| the stride is a u16 at `+0x08` | `00387707 movzx ecx, word ptr [rcx + 8]`. 566 u16 reads in 264 functions — **but §15a could not reproduce 264 under any stated population: only 227 functions read the stride of a registry header at all, and image-wide the pattern is 1377 reads in 694 functions. The 264 is wider than the shape and its definition is not recorded here; the *claim* is independently established by the instruction and by the suite** | 1 (static, isolated original code) | PROVEN |
| the reference is a dword at `+0x0C` | 1100 reads in 227 functions, all 4-byte; `003876E4` | 1 (static, isolated original code) | PROVEN |
| 40 registry slots are headers of this shape | a slot counts only when one function feeds both halves from the same tainted register. **Re-derived independently 2026-09-12 (§15a) over the whole band `02EBEF70`–`02EBF3FC`, 146 qword slots: 40, exactly.** ~~exactly one slot in the band shows a single half~~ — **corrected: NO slot shows a single half.** Every slot shows both halves or none; the four in dispute (`02EBF078`, `02EBF0D0`, `02EBF160`, `02EBF170`) show **no read at all** through a register tainted by them | 1 (static, isolated original code) | PROVEN |
| 226 functions perform the lookup | the same measurement | 1 (static, isolated original code) | PROVEN |
| the band is mixed | `02EBF190` holds `BattleSystemState` per `_types/types.tsv` | 1 (static, isolated original code) | PROVEN |
| the failure path dereferences a null base | `00387712 xor ecx, ecx` then `00387714 movzx eax, byte ptr [rcx + 9]`; `0030E686`/`0030E68A` for the second. **Executed**, and a one-sided probe with no page at zero shows the shipped bytes fault | 1 (isolated original-code) | PROVEN |
| the resolver zero-extends its reference and adds a 64-bit base | `0020E600` whole: `mov eax, ecx` / `add rax, qword [01F83530]`. Executed at references up to `0xFFFFFFFF` and at bases above 4 GB | 1 (isolated original-code) | PROVEN |
| the encoder subtracts the same global read as a DWORD, so the two are inverses ~~only below 4 GB~~ exactly while `(p - base) mod 2^64 < 2^32`, whatever the base's high half *(corrected 2026-10-02, OPUS: `0020E620` subtracts the base's low dword and `0020E600+0x2` adds the full qword back, so the pair returns `base + ((p - base) mod 2^32)`; the next row's ruling)* | `0020E620` whole. Executed in both directions at a base of `0x100000000`, ~~where the round trip does not return the reference~~ where a reference below `2^32` comes back unchanged by that algebra | 1 (isolated original-code) | PROVEN |
| **the exact round-trip condition is `((p - base) mod 2^64) < 2^32`** | the two encodings read at byte level: resolver `8B C1 48 03 05` (REX.W, qword) against encoder `2B 0D` (no REX.W, dword), both at `01F83530`, and BOTH OPERATIONS ARE MODULAR. **This row first read `0 <= p - base < 2^32` and called a 32-bit base necessary; `ASTRA-CONTRA-OPUS-REFERENCE-MODULO-WINDOW` refuted both halves and the counterexamples were re-checked here** — base `0x100000000` round-trips, and so does the `FFFFFFFFFFFFF000` wrap window EXP-076 already captured | 1 (static) | PROVEN |
| the header carries a `uint32` row count at `+0x04`, and nine consumers bound-check on it | FABLE's J-A band-register census (120 `+0x04` reads vs 592 `+0x08` / 1,034 `+0x0C`), independently reproduced 2026-09-20 (140/583/1,001 over 1,799 band loads; difference is window policy); three bound-checkers re-read in the image: `00237FF5`, `002388B5`, `0023AE25` — all `cmp index, [hdr+4]; jae` before resolving `+0x0C` | 1 (static) | PROVEN |
| `+0x00` is `slotCount` — the index bound of the encoded-pointer array at `+0x04` — and `+0x02` is a reserved header word; headers are not uniform across band families | function-list census over all 38,161 bodies (register tracked until rewrite or clobbering call), 2026-09-20: four true `+0x00` readers all range an index `≤ word[+0x00]−1` before `dword[+0x04+idx*4]` → `0020E600` (`0023A717`, `002FE06C` on `02EBF168`; `00308EE9`/`00308F11` pairwise ranges on `02EBF160`; `003214CD` on `02EBF170`, nested via `003214DF`); zero verified band-header `+0x02` readers — `003155E6`/`003063C1` are row `+0x02` reads | 1 (static) | PROVEN |
| the initializer retains a backing pointer above 4 GiB in the record's DIRECT fields | [EXP-077](../_experiments/EXP-077-arena-initializer-address-width.md), ASTRA — three bodies executed as shipped bytes; **body hashes, the mutant bytes and the unsigned `cmp esi,0xE / ja` re-verified here against the image** | 1 (isolated original-code) | PROVEN |
| what EXP-077 shows about ENCODED links at a high address | **nothing**: all 36 encoder calls across its six cases took the argument `0`, checked in the sealed `initializer-result.json`. **EXP-078 is the experiment that drives them** | none | SUPERSEDED |
| **the neighbour unlink stores through the DECODER's output, so a high block writes to its truncated low address** | **re-read by me**: `0036CA60 call 0020E600` then `0036CA75 mov [rsi+0xc], eax` and `0036CA8A mov [rdi+0x10], eax`; [EXP-078](../_experiments/EXP-078-arena-allocation-link-width.md) records the two faults at `0x10290` and `0x10FF8C`, which are `+0x10` and `+0x0C` of the truncated addresses | 1 | PROVEN |
| the failing fields are the neighbour links `+0x0C` / `+0x10`, distinct from the free-list links `+0x04` / `+0x08` | EXP-078, and the unlinker's own operands above. The free-list inserters `0036B670` / `0036B730` were **loaded but never reached**, so nothing is established about them | 1 | PROVEN |
| a low mirror leaves the mirrored bytes **unchanged** | EXP-078's five recorded events: `0x10290` is cleared and restored and the word was already zero. **Wrong-region access, NOT persistent corruption** | 1 (executed) | PROVEN |
| **a return-value-only comparison passes a broken predecessor link** | EXP-078's targeted control: both allocations returned the expected low pointers and only the predecessor assertion caught `+0x0C` becoming zero | 1 (executed) | PROVEN |
| an unlinked block is tagged `0xFF99` over its header word **only when the caller's `edx` is non-zero** | `0036CA4E test ebp, ebp` / `0036CA50 je 0036CAAE` **jumps past** `0036CA92 mov eax, 0xff99` / `0036CA99 mov word ptr [rbx], ax`. Corrected 2026-09-13: this row previously said every unlink tags the block | 1 | PROVEN |
| the `+0x3E` word is a corruption guard every writer stores zero to and every reader compares against zero — nonzero is not a state the code produces | store row `ImageAddressArenaBlockHeader.0x3E = guardWord` (OPUS 2026-09-20: 33 stores all-zero over 38,161 bodies, no non-word overlap that writes it); re-read 2026-09-20: five identical `cmp word[+0x3E],0 → 0036A570` report gates (`0036B8C3`/`0036B743`/`0036B683`/`0036B803`/`0036CB76`) plus the free path's `00369A80` MCB-Broken abort, and all sampled stores are zero (`0036CA20`-`0036CAB8`, `0036BE91`/`0036BEA5`) | 1 (static) | PROVEN |
| the free-list links are an encoded doubly-linked chain — `+0x04` is `prev`, `+0x08` is `next` | read 2026-09-20: `0036B670` decodes `rcx->+0x08` for the forward neighbour then stores `rsi->+0x08`/`rbp->+0x04`/`rbx->+0x04`/`rbx->+0x08` as a between-insert; `0036B730` is the mirror through `+0x04`. Both decode via `0020E600` and encode via `0020E620`, gate on `+0x3E` and clear it on every touched block; `rsi==0` encodes `0` into both links | 1 (static) | PROVEN |
| the STATIC delivery populates ~~39~~ 40 *(corrected 2026-10-02, OPUS: `003847B0`→`02EBF118` is the fifth inner binder, `00236C30+0x164`)* of the 47 band slots, through a fully enumerated binding map | read 2026-09-20: loader `0x13` `"STATIC"` → delivery stub `00238850` (binds `0208E680` via `003846F0`, tail-jumps `00236C30(1)`) → 35 slot bindings in `00236C30` (33×`003845F0` + 2×`003846F0` for `02EBF160`/`02EBF170`) + scalars `02EBF180`/`02EBF200` + ~~four~~ five inner-binder slots (`00237FC0`→`02EBF138`, `00238160`→`02EBF0F8`, `00238880`→`02EBF0D8`, `00238660`→`02EBF158`, `003847B0`→`02EBF118`). Binder caller census ~~complete: 36 `003845F0` + 5 `003846F0` sites~~: 36 `call` and 6 `jmp` sites of `003845F0`, 5 `call` and 1 `jmp` of `003846F0` *(corrected 2026-10-02, OPUS: `003847B0+0xA`, `00238640+0xE` and `0023A160+0x22` / `0023A160+0x31` / `0023A160+0x40` / `0023A160+0x61` jump to `003845F0`, and `0023A160+0x52` to `003846F0`)* | 1 (static) | PROVEN |
| where the arena actually sits in a running game | **BOUNDED OBSERVATION, 2026-09-13** ([EXP-079](../_experiments/EXP-079-arena-live-placement.md), ASTRA). In **two named states** of one session: arena 11 backing moved `7C5D3040` → `7C5D2040`, arena 14 sat at `6610EF40` and was **newly enabled**, and **arena 7 stayed enabled** with an `EFX0010` backing, pointer `763A2940`, and **all-zero 64 bytes at `+0x38` / `+0x90` / `+0x98`. **Two states are not all-time safety**, there is **no causal free/allocation trace**, and **“enabled” is not “an initialized, usable allocator”** — ASTRA states that limit explicitly and it is carried here rather than softened. So the 4 GiB question this contract turns on is **still not settled by placement evidence**: these backings are all below 4 GiB, which is consistent with the round-trip condition holding in these two states and proves nothing about others | 3 | PARTIAL |
| the worked instance resolves the same reference TWICE and tests only the first result | `003876E7` and `003876FB` against one null test at `003876EC`. Executed: **33 resolver calls across 21 timer calls** (re-run 2026-09-12; this row read 31 and 18, which no longer matched the suite), and the control that resolved once failed | 1 (isolated original-code) | PROVEN |
| the row address is built in 32-bit arithmetic and truncates the resolved base | `0038770B imul ecx, ebx` / `0038770E add ecx, eax`, both 32-bit. Executed at a stride and index whose product is exactly 2^32; the control doing it in 64 bits failed | 1 (isolated original-code) | PROVEN |
| the timer multiplies the row byte by the .data dword at 01DFE0B4, which the image holds as 1 | `00387718 imul eax, dword ptr [01DFE0B4]` then `imul eax, eax, 0x1e`; the dword read out of `.data` is `01 00 00 00`. Executed at several scales including zero and including the image's own value, which is what a case running before any fixture reset tests | 1 (isolated original-code) | PROVEN |
| nothing observed live | **superseded 2026-09-13**: EXP-079 observed arena placement live in two named states (row above). The **meaning, writer and lifetime of arena 7 remain unobserved**, and ASTRA has taken the offline trace; §13's other open items are untouched | 3 | PARTIAL |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

Everything below is re-derived from the shipped bytes: 38,161 functions disassembled **per function**
(1,787,590 instructions, **0 skipped**), never as a linear sweep — a linear sweep stops at the first
undecodable byte and silently under-counts, which produced a false refutation earlier in this sweep.

### What I tried to break, and could not

**The suspicion was the population.** `movzx r, word [reg+8]` and `mov r32, [reg+0xC]` are among the
commonest addressing patterns in any C++ image, so a census of them says nothing about *this* record
unless it is confined to the shape. **It is:** image-wide the patterns give **1377 reads in 694
functions** and **4898 reads in 2028 functions**, far above the document's 566/264 and 1100/227. The
census is not image-wide, and that suspicion is **refuted**.

**Then the document's own criterion was implemented and run over the whole band** — a register
tainted by `mov R64, [rip → slot]`, taint carried through 64-bit register moves and killed by any
other write; the reference half is `mov ecx, [taintedR + 0x0C]` *reaching* a `call 0020E600`; the
stride half is a u16 read at `[taintedR + 8]`; a slot qualifies when **one** function shows both.
Over `02EBEF70`–`02EBF3FC` (**146 qword slots**):

| the document says | this pass measures | |
|---|---|---|
| 40 registry slots are headers of this shape | **40** | ✅ exact |
| 226 functions perform the lookup | **226** | ✅ exact |
| the reference is read in 227 functions | **227** — the 226 that resolve, plus one that reads the stride and does not | ✅ exact, and it explains the 226/227 gap |

**Control:** `02EBF118`, the worked instance's own slot, shows `+0x0C` 4-byte ×43 and `+0x08` 2-byte
×42 and reaches the resolver **42** times. The instrument sees halves where they exist.

> **Two numbers reproduced exactly by a differently-derived measurement is the strongest thing in this
> pass**, and it is what makes the two disagreements below worth acting on rather than explaining away.

### Corrected: no slot shows a single half

§15 said *"exactly one slot in the band shows a single half"*. **Zero do.** Every slot in the band
shows **both** halves or **none**. The four that do not qualify — `02EBF078`, `02EBF0D0`, `02EBF160`,
`02EBF170` — show **no read at all** through a register tainted by them, not a lone half: `02EBF170`
is referenced 58 times, and every one is a null test or a pass to a binder (`movsxd rdx, [rax+0xF8]`
then `call 003846F0`), never a field read.

**Limit of the model, stated rather than buried:** this is register taint. A header spilled to the
stack and reloaded, or passed through a call, is not followed. A single half hiding behind a spill
would be invisible here — but the same model reproduces the document's own 40 and 226 exactly, which
is the control that makes its disagreement on this point meaningful.

### Corrected: §7's map is not the roster behind the 40

35 mapped rows + 4 bespoke-binder slots = **39**, and they are not a subset of the qualifying 40.
Three mapped slots never qualify (`02EBF078`, `02EBF160`, `02EBF170`); four qualifying slots are
absent from §7 (`02EBF120`, `02EBF140`, `02EBF148`, `02EBF150`). **Overlap 36.** The count is right;
the enumeration is a different set. §7 now says so.

### Open: the stride census's 264 functions

Only **227** functions read the stride of a registry header at all, and **226** of those resolve. The
stride row claims **264**, which is wider than the shape and narrower than image-wide (694). Five
stated populations were tried — image-wide 694, reads-both-offsets 301, reads-stride-and-calls 252,
reads-both-and-calls 233, shape-verified 227 — and **none is 264**. It is plausibly the shape plus
functions that receive the header as a *parameter* rather than loading it from a slot, which would be
a legitimate wider population, but **the document does not record which population it is** and it
cannot be reproduced from what is written. The *claim* does not depend on it: the stride is
established by `00387707` and by the executing suite.

**What this pass did not touch:** no claim wording or order changed, so `CONTRACT_MAP` is unaffected.
Nothing here is a live observation; §13 is unchanged and the live-game pause still holds.

## 16. Parity plan

`STRUCTURAL` — read a known slot's `+0x08` and compare with the authored row width.
`CONTRACT` — for several tables, compute a row address by this formula and compare against the
address the game uses.
`EDGE-CASE` — the two null paths, which cannot be driven without forcing a slot to null, and which
§14.3 says may be unreachable. **Both are now driven under emulation** (§13): a fixture page at
address 0 makes them comparable, and a one-sided probe without that page shows the shipped bytes
fault. What is still undriven is a null path in a LIVE process.
`CALCULATION` — **added 2026-09-12:** a stride and index whose product is exactly 2^32, where the
row arithmetic's 32-bit truncation is the only thing that keeps the address in range. The original
plan had no case that could tell 32-bit arithmetic from 64-bit.
`SERIALIZATION` — re-lay a table at a different stride and confirm every consumer follows.

> **⚠ A parity suite for the arena shape must assert LINKS, not returns.** EXP-078's targeted control returned both expected pointers with a broken predecessor, so a return-value comparison passes it. Any future arena pilot compares `+0x0C` and `+0x10` after each operation, or it is measuring the wrong thing.

## 17. Related

- `02-Resource-And-Asset-Pipeline/authored-data-table-registry.md` — the registry this formalises.
- `10-Status-Periodic-Terminal/Status-Write/the-status-write-and-its-side-effects.md` — the status
  definition table, one of the forty, and where this shape was noticed.
- `14-Story-Event-Quest-Hunt/CONTRACT-persistent-flag-banks.md` — DX-1, the same "a reimplementation
  that adds the missing guard is more defensive than the original" problem in another subsystem.

## 18. Materialisation re-encodes stored offsets — and the base differs per table — 2026-09-13 (OPUS)

`ASTRA-REQ-OPUS-LOAD-MATERIALIZATION`. When a loaded resource is materialised, `002A00F0` walks it
and **re-encodes every stored offset through the same `0020E600` / `0020E620` pair this contract
already owns**. The load-bearing fact is that **two tables in the same object use two different
bases**, so one relocation rule does not fit both.

```asm
002A00F0
002A00F6  cmp byte ptr [rcx+3], 1 / je     ; ALREADY RELOCATED -> return; set at 002A016A
002A00FF  ecx = [obj+8]  + esi(=obj)       ; object-relative
002A010E  call 0x20E620 / mov [rsi+8], eax ;   -> re-encoded arena offset
002A0119  call 0x2A1A80                    ; table A
002A011E  ecx = [obj+0x28] + esi           ; object-relative
002A012D  call 0x20E600 -> rbp             ; table B's BASE POINTER
002A0141  lea rbx, [rax+8]                 ; first row's field
002A0145  ecx = [rbx]
002A0147  add ecx, ebp                     ; <-- TABLE-BASE-relative
002A0150  lea rbx, [rbx+0xC]               ; stride 0xC
```

```asm
002A1A80                                   ; table A
002A1AC3  lea rdx, [rcx+rcx*4]             ; index * 5
002A1AC7  ecx = [r14 + rdx*4 + 0x10]       ; base + index*0x14 + 0x10
002A1ACC  lea rbx, [r14 + rdx*4]           ; <-- the ROW
002A1AD0  add ecx, ebx                     ; <-- ROW-relative
```

| table | count at | row stride | field | the stored offset is relative to |
|---|---|---:|---:|---|
| **A** (`002A1A80`, base `[obj+0x20]`) | `[obj+0x1C]` | **`0x14`** | `+0x10` | **its own row** |
| **B** (`002A00F0`, base `[obj+0x28]`) | `[obj+0x24]` | **`0xC`** | `+0x8` | **the table base** |

> **Two tables, two bases, one function.** A reimplementation that relocates both the same way
> corrupts one of them, and the corruption is silent because both produce plausible in-arena
> addresses. The distinction is visible only in one register: `add ecx, ebx` (the row) versus
> `add ecx, ebp` (the table base).
>
> **The `byte[obj+3] == 1` guard makes materialisation idempotent** — the object carries its own
> "already relocated" flag, set at `002A016A` after the walk. Relocating twice would double every
> offset, so this flag is load-bearing, not a cache.

### The index boundary the loop keeps

`002A1AC0 movsxd rcx, edi` **sign-extends** the index into the address computation, while the loop
bound `002A1ADC cmp edi, [rsi+0x1C]` / `jb` is **unsigned**. So a count at or above `0x80000000`
would keep the unsigned test true while the sign-extended index addresses *before* the table. **This
is the same 32-bit-quantity-from-a-64-bit-world pattern catalogued in
[`CONTRACT-efx-source-rebase.md` §7](CONTRACT-efx-source-rebase.md)**, here in an index rather than a
delta. No shipped count is claimed to reach that value; the boundary is recorded, not exercised.

**Carried forward as ASTRA's, not re-derived:** `00249670` → `0024A1D0`'s format 13/14 preparation
and the observation that **other formats also set flag 6**; `0024A4E0` being a **64 × 48 partial-reset
pool rather than a fresh zeroed object**; format 14's reordering of 64-byte groups into 128-byte pairs
with no `N % 16` tail; and the graphics helper's dimensions wrapping at 16 bits. Also ASTRA's, and
worth repeating because it is the player-facing point: **native callbacks return before `002495C0`
increments the ready count, so "ready" does not mean a valid image.**

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Gameplay — SERVICE.** `0030E360` on this page calls `BattleUnit_UpdateEngagementStateFlag`, owned by that layer. What it reaches is the engagement test, which reads the unit record's `+0x698` block and tests `+0x3C` OR `+0x64` against its own mask; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Rewards_Progression_Economy — SERVICE.** `0030E360` on this page calls `BattleUnit_ProcessDefeatRewardsAndLoot`, owned by that layer. What it reaches is defeat-and-loot processing, which reads the defeated unit's `+0x698` block, needs `byte[+5] == 1`, and is suppressed entirely by bit 3 of `byte[+0xE9A]`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**CoreRuntimeScheduling — MECHANICAL (SWE2-CONTRACT 2026-09-15, 36 edges).** 29 edges are the
image-pointer fixup pair `0020E600` `ImageAddress_ResolveRuntimePointer` (19) and `0020E620`
`RuntimePointer_EncodeImageAddress` (10) inside the lookup's method bodies; the remainder is the
`0017D4C0`/`0022A0B0`/`0022BDF0`/`001DB500`/`001A14E0` core-helper neighbourhood the loader lives
inside. Mechanical infrastructure, below any scheduling relationship.

**Movement — MECHANICAL (SWE2-CONTRACT 2026-09-15, 13 edges).** All 13 edges route through the single
shared accessor `0033A720` (interior read 2026-09-17, SWE2-FRONTIER: `0020E600` first at [`0033A904`](../_index/ADDRESS-INDEX.md), row-lookup ×2): two callers (`BattleLocomotion_ResolveTargetSpacingAndAvoidance`,
`BattleLocomotion_ResolveDefaultHeadingConstraint`) and eleven callees (`0033CC80`/`0033D200`/
`004687F0`/`00335F90`/`00337470`/`00339DF0`/`00335180` (interior read 2026-09-17, SWE2-FRONTIER: `00383840` first at [`0033527C`](../_index/ADDRESS-INDEX.md), `0020E600` at `003352A9`)/`BattleLocomotion_TestForwardStepClearance`/
`0033B6F0`/`003208C0`/`0033CEF0`) all neighbour `0033A720`, which this contract cites. Shared
accessor fan-in — no locomotion relationship to the row-lookup semantics.

**CombatFormula — CLIENT and SERVICE (SWE2-CONTRACT 2026-09-15, 9 edges).** `00239960` calls
`BattleStats_InitializeDefinitionRecord` and `BattleStats_GetByBattleSlotIndex`; `0030E360` calls
`BattleFormula_BuildConditionalStatusHpTransitionResult`, `BattleFormula_BuildInactiveStatusTransitionResult`
and `BattleStats_FindOwningBattleUnit`, and trades calls with `BattleFormula_ApplyTargetResult` and
`BattleStats_ModifyHPAndProcessLethalState`; `003876D0` is reached by
`BattleFormula_AppendStatusAddOperation`. The table rows feed the stats/result machinery — a real
consumption crossing, small and named.

**Presentation — SERVICE (SWE2-CONTRACT 2026-09-15, 7 edges).** `0022A0B0` calls `AddMotion_LoadHighModelReplace`
`0037CCC0` and `AddMotion_LoadSkeletonMapping` `0036FFF0`; `0024A1D0` calls the five
`Presentation.Graphics.AssetMaterializationSupport` helpers `00181190`/`00181250`/`00181520`/
`00180E70`/`00181000`. Row lookup serves the load/materialize path — mechanical adjacency, named.

**ActorEntity — CLIENT on five edges, SERVICE on one (6 edges, three neighbour bodies read).** The
functions cited here reach the battle-unit pool through its two bounded accessors.
`BattleUnit_GetBySlotIndex` `00236820` is called by `0033CEF0` and `0033D200`, and it is the shape
worth recording: a negative slot returns null, a slot at or above `dword[0208E6A0]` returns null, and
otherwise the record is `[0208E688] + slot × 0xF50`. **`BattleUnit_GetSlotCount` `00236850` is two
instructions returning that same `dword[0208E6A0]`** — the bound and the count are one value, not two
that could drift. `0033A720` calls `ActorRuntime_GetClass3FloatPair` `00265090`, which refuses any
body whose kind nibble is not 3 (`byte[+3] & 0xE0 == 0x60`) and otherwise tail-jumps to `003DA710`
with `[body+0xB8] + 0x50`. `0022A0B0` and `0030E360` reach `BattleStorage_InitializeWorkArrays`
`002368D0` and `00300FC0`; the one edge the other way is `002368D0` reaching `003843F0` on this page.
The crossing is that this page's consumers index a bounded pool; it owns none of it. Read from the
shipping bytes 2026-09-14 (OPUS).

**Platform — MECHANICAL (FABLE, Claude Opus 5.5, 2026-09-24, 3 edges).** §7's base reconciliation cites
the static AMD Display Library wrapper `01F83460` because the image-address base is the first qword
after it. The cited bodies are its constructor `0020D2F0` and the helpers `0020DE30`/`0020E420`
the constructor calls. They are Platform code: GPU-vendor adapter enumeration through `atiadlxx.dll`.
They are cited only to show that the wrapper **ends** at `+0xD0` and never stores there. Adjacency
in `.data`, no data or control relationship to the row lookup.

**Audio — MECHANICAL (SWE2-EC7-34, 1 edge).** `00203080` — the shared UI-object helper this page cites inside the `0033B6F0` row-lookup body — is called by `00362850` on the Audio layer. Shared-helper fan-in; no audio relationship to the row-lookup semantics.

## The `00236C30` exclusive subtree — all 5 members bound (SWE2-FRONTIER, followup queue)

`00236C30` — the 1,037-B orchestrator this contract calls the delivery mechanism — owns **5
frontier functions**. Every member was disassembled from the shipping image; interior cites
are one instruction inside each extent. The root's two modes, confirmed from the bytes:
arg `0` frees `[0208E680]` through `00384500`, nulls the cell, and tail-calls
`003843F0(0x13, 00238850, <rodata 007146AF>)`; nonzero rebinds — `[0208E680]` is the source
object, its directory fields feed 33 × `003845F0` + 2 × `003846F0` slot registrations plus
the five member calls below (`+0x20` → `00238880`, `+0x38` → `00238160`, `+0x3C` →
`00237FC0`, `+0x40` → `003847B0`, `+0xA0` → `00238660`). `003845F0` itself is
`AreaData_BindAndRebaseSectionDescriptor`: it stores the descriptor into the slot and adds
the source base into its `+0xC`/`+0x10`/`+0x18`/`+0x1C` offsets, translating `+0x14`
through `0020E620`.

What each bespoke binder does *after* registering (the "and then do more" this contract
names but did not enumerate):

| member | slot / role | interior |
|---|---|---|
| `00237FC0` (404 B) | registers the header arg into `02EBF138`, then iterates the slot's own row table — `[[slot]+0xC]`-indexed rows under `dword[+4]`, each fetched with `0020E600` and re-registered | [`00237FF5`](../_index/ADDRESS-INDEX.md) |
| `00238160` (248 B) | registers into `02EBF0F8`, then walks the index band `0x1000 .. [slot]+4 + 0x1000`, row-fetching (`0020E600`) and rewriting each entry's back-reference | [`002381AC`](../_index/ADDRESS-INDEX.md) |
| `00238880` (411 B) | registers into `02EBF0D8`, then **builds the menu lookup**: two passes over the rows take `byte[+0x16]`/`byte[+0x17]` (0xFF = absent), max+1 gives the dimensions (`0208D310`/`0208D312`), a `rows×cols` u16 table is allocated into `0208D318` and filled `0xFF`; pass 2 stores `0x6000 + i` at `[row, col]` | [`002389F9`](../_index/ADDRESS-INDEX.md) |
| `00238660` (488 B) | the deep rebaser: `[02EBF158] += arg`, then a `word[+6]` × `word[+4]` nested walk rebasing every element's `+4`/`+8` fields by the same delta through `0020E600`/`0020E620` | [`0023868D`](../_index/ADDRESS-INDEX.md) |
| `003847B0` (15 B) | the tail-jump one-cell binder into `02EBF118` — already enumerated above as the sweep-invisible case | [`003847B3`](../_index/ADDRESS-INDEX.md) |

`003843F0`, `00384500`, `003845F0`, `003846F0`, `00384510`, `00861EC0`, `0020E600` and
`0020E620` are shared callees with other callers — deliberately not census members.

## The `0036BC60` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`0036BC60` ~~(~179 B)~~ (887 B) *(corrected 2026-10-02, OPUS: the body runs 887 bytes from `0036BC60`)* — arg spill `r9d`/`ecx`, four-register body
(`0036BC60`/`0036BC6C`).

| member | role | interior |
| --- | --- | --- |
| `0036B8B0` | `rdx` non-null gate, `word[+0x3E]` count compare (`0036B8B0`/`0036B8C3`) | [`0036B8B0`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.


### Interior citation — frontier hubs `0036B730`, `0036B670` (2026-09-18, SWE2-EC7)

`0036B730` / `0036B670` — 179 B each, 4 callers each: the two free-list
inserters, now read — `word[rdx+0x3E] != 0` is the error arm (`0036A570`
report + `int3`); the live arm resolves `[rsi+4]`/`[rsi+8]` through
`0020E600`, cross-writes `dword[rbx+4]`/`[rbx+8]` via `0020E620` at
[`0036B77E`](../_index/ADDRESS-INDEX.md) /
[`0036B6BE`](../_index/ADDRESS-INDEX.md), and clears `+0x3E`. The twins
differ only in which field pair is the source (`+4`/`+8` vs `+8`/`+4`).

## SWE2-EC7-24 update (2026-09-18) — `00384510`, `0036B210`, `0036C900` row-access helpers

`00384510` (103 B) is the bind helper: `0036C1D0(4)`, `0036C1A0(6)`, then
`0036A190(ecx)` for the row pointer — non-null rows get `0036C660(row, rsi,
edi)` — and `0036C110`/`0036C140` close the pair. Interior anchor `00384533`.

`0036B210` (161 B) is a resolver-chain linker: `0020E600`-resolves `[rdx+4]`,
then walks `[node+0xC]`/`[node+4]` links until the resolved bases diverge, calls
`0036B2C0`, stamps `word[+0x3E]`/`byte[+0x15]` zero, and lazily publishes the
result into `[rsi+0x90]`/`[rsi+0x98]` when those slots are empty. Interior
anchor `0036B228` (the first resolve).

`0036C900` (198 B) is the pointer-table bit-clear: `(rdx - [rcx+0x10])` +
`dx`/`0x10000` `sar 0x10` gives a 16-bit index into `[rcx+0x28]`'s pointer bank;
on match it re-resolves `[r8+8]` via `0020E600`, splits the index `>>5`/`&0x1F`,
nulls the bank slot and clears the bit in `[rsi+0x20]`'s word table. Interior
anchor `0036C931` (the `sar`).

## SWE2-EC7-34 update (2026-09-19) - `0033B6F0`

`0033B6F0` (936 B) is a row-lookup body - 13-xmm spill prologue, `004687F0`/`0033CB70`/`0033BA0A`/`0033B9B3`/`0033B86C`/`00203080`. Interior anchor `0033B799` (an `004687F0` call).

## SWE2-EC7-42 update (2026-09-19) - `0036B2C0`

`0036B2C0` (324 B) is an authored-table body - `0020E600` quadruple plus `0036C9D0`. Interior anchor `0036B2D2` (a `0020E600` call).

## SWE2-EC7-44 update (2026-09-19) - `00339DF0`

`00339DF0` (262 B) is an authored-table chain body - `0033CB70` single call. Interior anchor `00339E6E` (the `0033CB70` call).

## SWE2-EC7-49 update (2026-09-19) - `00181190`

`00181190` (189 B) is a `Presentation.Graphics.AssetMaterializationSupport` helper - `00183EE0`/`001B1C00`. Interior anchor `00181223` (an `00183EE0` call).

## SWE2-EC7-49 update (2026-09-19) - `00181250`

`00181250` (189 B) is a `Presentation.Graphics.AssetMaterializationSupport` helper - `00184140`/`001B1C00`. Interior anchor `001812E3` (an `00184140` call).

## SWE2-EC7-59 update (2026-09-19) - `00335F90`

`00335F90` (161 B) is an authored-table-row body - `00318CA0`/`00335E50`/`0033D3E0` plus `008FCC8C`. Interior anchor `00335FC7` (a `00335E50` call).


## ASTRA's zero-base contradiction, ruled — 2026-09-20 (OPUS)

`ASTRA-CONTRA-OPUS-ARENA-ZERO-STORAGE-INFERENCE` asks that a third hypothesis be retained: *zero
base with valid low-address runtime references*, and that encoding, placement, the actual
`003E3C30` entry, and allocation-versus-authored storage be kept apart.

**ACCEPTED, and the reasoning is sound.** Re-read from the shipping image rather than from this
page: the decoder is `mov eax, ecx` — a 32-bit move, so it **zero-extends** — then
`add rax, qword [01F83530]`, then `ret`. The encoder is `sub ecx, dword [01F83530]`,
`mov eax, ecx`, `ret`. The base cell lies in the **BSS tail of `.data`** (section VA `01DF0000`,
virtual size `0x11A7530`, raw size `0x18E400`), so it is not raw-backed and reads zero at load.
At base zero `decode(x) = x`, and a nonzero 32-bit `x` is therefore a **valid low address**, not
a degenerate one. Nothing about a zero base makes a consumer dead or a storage authored.

**There is nothing to retract, which is the substantive part of the answer.** §2a already says
*"If the base is zero, both functions are identities"*, and
`authored-reference-lifetime-evidence.md` already records the whole-image census and concludes
*"the two functions are therefore truncation and zero-extension in every shipped path"*. The
OPUS type rows agree: `RenderStrideC0Bank` and `RenderStrideC0Element` record that `0020E600`
is *"the IDENTITY on the unsigned 32-bit domain, so the decoded value IS the stored reference"*
and explicitly downgrade the word *pointer* to **32-bit reference into the arena**. The
hypothesis ASTRA asks to retain is already this store's position; no live row asserts the
inference being contradicted.

**What the codec constrains is RANGE, not storage kind.** The asymmetry is the whole content:
the decoder adds the full 64-bit base while the encoder subtracts only its **low 32 bits**, so
the pair round-trips ~~only while the base's high half is zero and the delta fits 32 bits~~ exactly while `(p - base) mod 2^64 < 2^32`, whatever the base's high half *(corrected 2026-10-02, OPUS: `0020E620` subtracts the base's low dword and `0020E600+0x2` adds the full qword back, so the pair returns `base + ((p - base) mod 2^32)`)* — the
bound §10.1 already states as `((p - base) mod 2^64) < 2^32`. That constrains where the arena
may sit. It says nothing about who produced its contents.

### The producer evidence ASTRA asked for (OPUS)

**The arena's backing is allocated by the engine's own allocator, and that is readable
statically.** The banner EXP-079 read at the backing — `TKMALLOC EXECSPACE=02` — is not a
third-party artefact: `TKMALLOC EXECSPACE=%02d/START ADRS=%p` is a **format string in the
shipping image** at raw `0xBEFD20`, sitting immediately after `MallocHandleAllocationError`. The
engine prints it about its own exec-space allocation. *This was checked because the opposite was
suspected — a separately-installed allocator mod of the same name exists in this environment —
and the check refuted the suspicion before it was routed as a correction.*

Corroborating the CRT-heap reading independently: `VirtualAlloc` and `HeapAlloc` do not appear
anywhere in the image, case-insensitively, while the control strings `KERNEL32.dll` and
`Malloc…` both do. A first pass of that search was case-sensitive and returned "absent" for all
three probes, which made it worthless rather than informative; the controls are what turned it
into evidence.

**So the backing is runtime-allocated by the engine. That still does not settle skeleton storage
kind**, and the distinction is worth keeping sharp: memory allocated at runtime can be filled
from a file. The discriminating test is about the *field*, not the arena — whether an encoded
reference is written by a call to the encoder `0020E620` (produced at runtime) or arrives by a
load/copy into the structure (authored, carried in the data). That test is independent of the
base and is not answered here.

**Left open exactly as ASTRA asked:** the actual `003E3C30` entry remains unobserved, and the
storage-kind question stays separate from encoding and placement.

**The `003E3C30` body, read 2026-10-02 (OPUS, on ASTRA's rig-index-list package, re-read at the bytes).** It
decodes the rig's `+0x88` list (`003E3C42`/`003E3C48`) before it tests the **unsigned** DWORD count `+0x8C`
(`003E3C52`, `jbe`). Each list entry is an unsigned DWORD index (`003E3C68` `mov ecx, [rbx]`), scaled to
`decode(+0x78) + 0x230 + index * 0x290` (`003E3C6A`-`003E3C77`) and passed to `00203170`. The loop compares
unsigned (`003E3C8B`, `jb`) and checks no index against a bone count. Its entry remains unobserved, as above.

## SWE2-EC7-92 update (2026-09-20) - `00384420` row-fetch orchestrator measured

`00384420` (204 B) is the lookup orchestrator `003843F0` wraps:
`0032E400(2, index)` resolves the row (negative -> return 0),
`0036C1D0`/`0036C1A0`/`0036A190` chain to the record, `0036C660`
applies `r8`/`index` against it when non-null, `0036C110` +
`0036C140` run the paired step, and `0032E620(2, index, rec, ret,
0, aux)` publishes through a stack record.
Interior anchor `0038444E` (the `0032E400` call).

## SWE2-EC7-110 update (2026-09-20) - `001B21D0` measured

`001B21D0` (247 B) is the
find-or-create row lookup
`00181190` and `00181250`
run. `001B1440(rdi)` produces
the `ebx` key; the EASTL tree
at `rdi + 0x2200` (root
`[+0x18]`, sentinel `+8`)
descends on `dword[+0x20]`
and a hit returns `qword[node
+ 0x28]`. A miss calls
`001BA860(rdi + 0x2140)` for
the new row, then re-descends
and `001AE9B0` emplaces the
`{ebx, rsp + 0x30 pair}` node
so `[node + 0x28]` receives
the fresh pointer - the
memoizing insert half of the
table cache. The tail
`001FB800(row, rbp)` invokes
the caller's continuation.
Interior anchor `001B2200`
(the `dword[r9 + 0x20]` key
compare).

Mechanical neighbours this
section's citations add:
`001B1440` also has a
Platform caller `001B1960` -
a caller/callee fan-in edge,
not row-lookup semantics.

`0036A570` (729 B) is the arena class inspector the `+0x3E` guard-word checks report to: `bt dword[022D89B8], ecx` gates on the class bit; `ecx <= 0xE` selects `022D7FD0 + ecx*0xA8`; the `bpl` flag mask arms five walks - bit0 walks the `+0x10` node list formatting `byte[+0x14]&1`/`byte[+0x15]` status strings (`FREE`, `M2/U`..`M /L`, `/I`/`/C` suffixes) and resolving `dword[+0x30]`/`+8`/`+0x10` via `0020E600`, bit1 walks `+0x90`, bit3/bit4 follow the `+0x48`/`+0x40` index chains (`(rcx - dword[+0x30])>>4` slots), bit5 calls `0036A850` on `+0x50` - the arena's diagnostic dump behind every corruption gate.

Interior anchor `0036A5B2` (function `0036A570`).

`0036A490` (215 B) is the 0x40-byte record initializer the row-lookup callers fill through: when `rdx` is live it writes magic `0xFF12` at `+0`, `0xFF` at `+2`, the class byte at `+3`, zeroes `+0x14`/`+0x16`/`+0x1E`, stamps nine `0020E620(0)` results into `+4`/`+8`/`+0xC`/`+0x10`/`+0x20`/`+0x24`/`+0x28`/`+0x2C`/`+0x30`, ORs `8` into `byte[+0x15]` while `dword[022D8E28]` is nonzero, and takes `r8d`/`r9w` into `+0x18`/`+0x1C` - the shared header fill beside `0036A570`'s inspector.

Interior anchor `0036A4D3` (function `0036A490`).

`0036B5F0` (124 B) is the slot-map insert: `(rdx - [rcx+0x10] + dx) >> 0x10` picks the `qword[[rcx+0x28] + i*8]` bucket - an empty bucket takes the pointer, an occupied bucket takes it only when the existing key is larger (prepend wins on smaller) - and `1 << (i & 0x1F)` sets the `dword[[rcx+0x20] + (i>>5)*4]` bitmap bit either way - the occupancy index the row-lookup and ebp2 callers share.

Interior anchor `0036B622` (function `0036B5F0`).

`0020BB10` (801 B) is EASTL `vector` insert-with-fill for 0x18-stride records: it magic-divides the element count, and when capacity suffices memmoves the tail right by `r8d` elements and fills the gap with the 24-byte value at `r9`; on growth it reallocates through the `[rsi+0x18]` allocator (`+0x10` allocate / `+0x18` deallocate vcalls), copies head and tail, fills the middle, and rewrites the begin/finish/capacity triplet. The authored-table row lookup leans on it for mid-table row insertion.

Interior anchor `0020BBF0` (function `0020BB10`).

`0036A850` (367 B) is the recursive flag-tag walk `0036A570` runs over an authored-table node: bit 0 of `[rbx+0x14]` selects the `M2/` prefix else `M /`, bits 0-2 of `[rbx+0x15]` pick the `U`/`L`/`l` suffix (`FREE` when the `+0x14` bit is clear) and bit 3 switches the trailer between `/I` and `/C`; the assembled tag lands in a stack buffer the body never hands out, so the pass is the traversal itself - it recurses into the `[rbx+0x24]` child and then iterates the `[rbx+0x28]` sibling chain, both resolved through `0020E600`.

Interior anchor `0036A90C` (function `0036A850`).

`0036C380` (289 B) is the segment splice `0036CB00` runs to move `[r9]` bytes of a source segment into a target list: the source's `+0x4`/`+0x8` neighbours are resolved through `0020E600`, the extent delta `[r15+0x18] - arg4 + [out+0x18]` is computed while `[out+0x18]` is rewritten to `arg4` and `+0x3E` cleared, `0036C900` and `0036C9D0(r15, 1)` bracket the move, and `0036A490` copies the `[rbp+1]`-sized payload into the `[out+0x40] + arg4` region counted by `[rbp+0x60]`; the new extent is then linked - `0036B670`/`0036B730` onto the resolved neighbours or straight into `[rbp+0x90]`/`[rbp+0x98]` when a neighbour is absent - `0036B7F0` and `0036B5F0` rebind the record, head/tail pointers are repaired when they pointed at the source, and `[rbp+0x60]` is incremented for the new element.

Interior anchor `0036C40C` (function `0036C380`).

`0036AE00` (287 B) is the predecessor seek `00369860` runs over the offset-chained record list: the chain head resolved from `[rdx+0xC]` through `0020E600` is converted to a packed index (`(ptr - [rsi+0x10]) >> 16`, plus the carry's low word), the `[rsi+0x20]` bitmap is walked backwards by 32-bit words to the last set bit at or below it, the `[rsi+0x28]` entry table is then scanned backwards for a pointer strictly below the query `rdi`, and the `[rbx+8]` successor chain - each link resolved through `0020E600` - is chased while the resolved next stays at or below `rdi`; it returns the last such record, or 0 when the head index resolves negative.

Interior anchor `0036AE93` (function `0036AE00`).

`0036ACE0` (286 B) is the successor seek pairing `0036AE00` over the same structure: the head resolved from `[rdx+0x10]` is packed-indexed identically, the `[rsi+0x20]` bitmap is scanned forwards from that index for the first set bit bounded by the `[rsi+0x58]` count, the `[rsi+0x28]` table walks forwards to the first pointer strictly above `rdi`, and the `[rbx+4]` predecessor chain is chased while each `0020E600`-resolved next stays at or above the query - returning the boundary record or 0.

Interior anchor `0036AD6C` (function `0036ACE0`).

`0036D2F0` (265 B) is the row-republish `0036D280` runs: `0016D6A0` fills a `0x280`-byte stack record seeded from the `022D8EAC`/`022D8EB0`/`022D8EB4` globals (kind words `0x31`/2/1 in the header), then the record's fields republish to `022D8E50..022D8EA0` - the dword pair folded `imul` then `(x + (x>>31 & 0x7FF)) >> 11` into `022D8EB8`, the `+0x78` member xor-folded by `(eax^ecx) & 0x1FF`, and the trailing `movups`/`movsd` block landed at `022D8E88`/`022D8E98`

Interior anchor `0036D353` (function `0036D2F0`).

`0036C290` (228 B) is the element insert `0036CB00` runs, the gap-open counterpart to `0036C380`'s splice: it copies the `rdx+0x18 - ebp - 0x40` tail bytes down through `0036A490` at `rsi = rdx+0x40+arg4`, clears `u16 +0x3E` on both `rsi` and `rdi`, rewrites `rdi+0x18` to `arg4`, then `0036B7F0`/`0036AE00`/`0036ACE0`/`0036B730`/`0036B670` re-link the neighbouring elements (high/low side chosen by `rdi < [rbx+0x18]`), `0036B210` + `0036B5F0` rebind the record, and `[rbx+0x60]` increments

Interior anchor `0036C313` (function `0036C290`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

**WorldAreaField and World — CLIENT, 70 edges: the area loaders use the same arena and request machinery as the row
binds.**
- **The arena helpers.** This contract's bind helper `00384510` runs the arena push/pop pair `0036C1D0` / `0036C1A0` /
  `0036C110`, the row fetch `0036A190` and ~~the rebase~~ the header tagger `0036C660` *(corrected 2026-10-02, OPUS: `0036C660+0x1A` checks the `0xFF12` block magic at payload `-0x40`, `0036C660+0x30` `strncpy`s seven name bytes into payload `-0xC` and `0036C660+0x40` stores the tag word at `-0x22`; nothing is rebased)*. The field loaders run the same helpers:
  `MapRef_BeginLoadResources`, `AreaArd_LoadOrUnloadFieldResource`, `AreaArd_BindLoadedRootAndBattleSections`,
  `00377DC0`, `00378030`, `003788F0`, `003789A0`, `00378BC0`, `00267930` and `003319D0`. The map-table requester
  `00378540` (filed World) runs them too.
- **The request path.** `0032E400` / `0032E620` is shared the same way.
- **Area data.** The registrar `003846F0` and `AreaData_BindAndRebaseSectionDescriptor` (`003845F0`) are also called
  by `BattleData_SetAreaArdSectionCategory`, and the registry map's `00236C30` binds area sections through them.
- **Other readers.** `BattleSystem_InitializeAreaState` calls `00239960`, and `0033A720` reads the field id.

The area loaders' order is `the-world-tick-and-the-field-frame`'s. This contract owns the row lookup, the registry
map and the binds.

**Status_Periodic_Terminal — SERVICE, 13 edges.** The two functions this contract names as table readers,
`BattleStats_ChangeStatusAndProcessSideEffects` (`0030E360`) and `BattleStatus_ComputeDefaultShortTimer`
(`003876D0`), are status-write machinery. They are called by the add/remove-status bodies and
`BattleFormula_AdvanceStatusTimersAndBuildResult`, and they call the action reset and terminal recovery. The page
cites them only for the table row each reads; what a status does is `CONTRACT-status-write`'s.

**CombatAI — CLIENT, twelve edges.**
- `AiOrder_EvaluateTargetSelector`, `AiOrder_ComputeBoundedSelectorScalar`, `BattleEnmity_PropagateToPerceivingFoes`
  and the perception rebuild walk the battle-unit slots (`BattleUnit_GetBySlotIndex` / `BattleUnit_GetSlotCount`).
- The registry map binds the gambit target table through `GambitTargetDefinition_BindAndBuildMenuLookup`, which
  also calls `00384510` and `003845F0`.
- `00239960` loads the authored gambit preset (`GambitConfig_LoadAuthoredPresetAndRebuildRuntimeOrders`).

**Items_Equipment_Shops_License and Items — CLIENT, seven edges.**
- `00239960` applies the authored start state: `Inventory_MutateEncodedItemPrimaryChannelMode1`,
  `BattleStats_SetEquipmentSlotDirect` and `BattleStats_SetLicenseNodeStateAndApplySideEffects`.
- `002FA920` classifies an item (`ItemDefinition_ClassifyEncodedItemCategory`, `BattleIdClassD_GetRuntimeFlagBit1`).
- `BattleStats_ClearAllEquipmentSlotsByMappedId` walks the slots.
- The registry map calls the items-filed `00238660`.

**Party — CLIENT, four edges.** `PartyConfiguration_ReconcileRosterFromCurrentSelectors` and
`PartyConfiguration_SetSelectorsAndReconcileRoster` walk the slots, and `00239960` sets
`PartyConfiguration_SetDefinitionSelectorForIndex`.

**Script_VM_Native_Bridge — CLIENT, seven edges.** The script adapters `0050D8F0`, `0050DAD0`, `0050DF70` and `0050DFE0`
use the arena pair, the rebase and the request path.

**Input and RNG_Random_Selection — MECHANICAL, four edges through the boot.**
- The bootstrap `0017D4C0` → `0022A0B0` (cited as the frame the STATIC blob arrives under) creates the input manager
  (`InputManager_CreateSingleton`).
- The boot calls the input fix-up `0035B270` and seeds `RNG_MT19937_Seed`.
- The UI-side `00291C80` issues the same request `0032E620`.

*Tier 2: ledger names, sizes and `edges.tsv`, roles as this page reads them; no new body read (OPUS, 2026-09-29,
pass-22 debt `42a617a9a`).*

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../_index/candidates/opus-contract-authored-table-row-lookup-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00249670` | 13 B | tail-jumps to `0024A1D0` with `rcx` = qword `rcx+0x18` and `rdx` = qword `rcx+8` | `00249674`, `00249678` |
| `002A1A80` | 119 B | replaces dword `rcx+0x20` with `0020E620(that dword + the low 32 bits of rcx)` and passes the new value to `0020E600`; then, over the `0x14`-byte rows at the returned base for indices 0 up to dword `rcx+0x1C` (unsigned), replaces each row's dword `+0x10` with `0020E620(that dword + the low 32 bits of the row address)` | `002A1A96`, `002A1A9F`, `002A1AA2`, `002A1AD0`, `002A1AD9` |
| `002D7FC0` | 138 B | calls `00861EC0(02F8DA00, 0, 0x1800)` and `00861EC0(02F8C200, 0, 0x1800)`, copies dword `022D8EAC` to `02F8F214`, and with `d` = ((that value - 0x200) * 0x540) >> 6 when it is above 0x200 (unsigned) and 0 otherwise, stores 0x3B00 to `02F8F200`, `d + 0x3B00` to `02F8F20C`, `d + 0x3C00` to `02F8F210` and `02F8F208`, and `d + 0x2A00` to `02F8F204` | `002D7FD3`, `002D7FF2`, `002D7FF8`, `002D8004`, `002D8027` |
| `0050DAD0` | 174 B | reads `p` = qword at `002640C0()` and `q` = qword `rdx+0x40`, takes `a`, `b`, `c` from three `00267E10(r9)` calls, then calls in order `0036C1D0(b, a)`, `0036C1A0(5)`, `x` = `00263E40(p, dword at q)`, `y` = `0036B160(c)`, `0036C6C0(y, x, c)`, `0036C110()` and `0036C140()`, and tail-jumps to `0026B4E0(incoming rcx, y)` | `0050DAF1`, `0050DB1F`, `0050DB34`, `0050DB4D`, `0050DB79` |
