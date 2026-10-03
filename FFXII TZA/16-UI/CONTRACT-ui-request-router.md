---
contract: The UI request router — the mailbox, the three refusals, and the request word that latches them
category: 16-UI
scope: subsystem
readiness: CONTRACT READY   # the interface and the refusals are STATIC; no live capture of a refused request
confidence: PROVEN
implements:
  - Request-Router/ui-request-router.md
entries: [00254B50, 002E1B10, 002E09A0, 00280A00, 00252B40, 00252D90, 002E1A60, 002E0DA0]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: read from the authority image in this session (2026-09-21, FABLE). The dispatch table in §3
    is decoded from the two `.rdata`/`.text` tables by
    `_index/candidates/fable_routertab.py`, with the control that ids 1 and 4 must resolve to one
    route; the cell population in §5 is an image-wide rip-relative sweep
    (`_index/candidates/fable_ripband.py`).
last_reviewed: 2026-09-29
falsification_passes: 0   # <- corrected 2026-10-02, OPUS - the body records Falsification pass 1 (2026-09-29, OPUS)
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-ui-router-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — the UI request router (FABLE)

> **This contract exists because S-36's contract covers two of its three pages.**
> OPUS's [L2 verdict](../_index/L2-VERDICTS.md) for S-36 says it in terms:
> `CONTRACT-widget-object.md` is `scope: subsystem`, its `implements:` names
> `the-widget-constructor-and-object-sizes.md` and `the-widget-message-protocol.md`, and
> *"**the router is the remainder**."* Its contract cell reads **SCOPE-SHORT** for that reason and
> for no other.
>
> This is the same **COVERAGE** gap as S-35's, one layer downstream, and it is answered the same
> way: by stating the invariants and ordering that hold **across** the router's operations, and
> restating none of the widget contract's object model, message protocol or construction ABI.
> It formalises [`Request-Router/ui-request-router.md`](Request-Router/ui-request-router.md), whose
> §2 identifies the requests and §7 tracks which ids are still unnamed — **neither is repeated
> here**, because a contract is about the mechanism, and which screen id 18 opens is not a
> mechanism.

## 1. The subsystem in one paragraph

A **request** is a small integer that asks the UI to do something — open the Battle Menu, cycle a
target, change leader, open a shop. Producers raise one from three places: the input arbiter, the
zone script, and widgets. They do not reach the screen directly. Every request passes a **router**
that can refuse it, and most requests are deferred one step through a **single-slot mailbox** that
the world tick drains. The contract below is about **what refuses a request, what silently
replaces one, and in what order** — the three things a caller has to know and that no page states
together.

## 2. Interface

| operation | entry | conv | signature | returns |
|---|---|---|---|---|
| route a request | `00254B50` (263 B) | MS x64 | `(u32 request ecx, u32 parameter edx, u32 flag r8d)` | `eax` — **0 = refused**, otherwise the route's own value |
| post a deferred request | `002E1B10` (85 B) | MS x64 | `(u32 id ecx, u32 parameter edx)` | `eax` — 1 stored, **0 refused** |
| drain the mailbox | `002E09A0` (1,002 B) | MS x64 | `()` — called once per tick at `0031427D` | — |
| schedule a generic request | `00280A00` (193 B) | MS x64 | `(u32 request ecx, u32 parameter edx, u32 flag r8d)` | `eax` — 1 scheduled, **0 busy** |
| set the request word | `00252B40` (29 B) | MS x64 | `(u32 id ecx, u32 flag edx)` — tail-jumps into the prelude `00254740` | — |
| release the request | `00252D90` (71 B) | MS x64 | `()` — unwinds the stop registry, then zeroes the word and the flag | — |
| post a fullscreen request | `002E1A60` (123 B) | MS x64 | `(u32 selector, u32 parameter)` — translates, then posts | — |
| translate a script selector | `002E0DA0` (104 B) | MS x64 | `(u32 selector)` | `eax` — a request id, bit 15 preserved |

## 3. Dispatch

`00254B50` normalises `id = request & 0x7FFF` (`00254B69`) and, for `id` in `1..24`
(`00254BD6`-`00254BDC`), dispatches through **two** tables: a 24-byte arm index at `00254C70`
indexed by `id - 1`, then a 4-byte RVA table at `00254C58` indexed by that byte, added to the image
base `00120000` (`00254BE7`-`00254BF9`). **Six arms, decoded from the tables:**

| arm | route | requests |
|---|---|---|
| `00254BFB` | `0035D660` | **1, 4** — one route for two ids, as the page states |
| `00254C04` | `0035D980` | 3 |
| `00254C0D` | `003C87B0` | 5 |
| `00254C16` | `0028E970` | 12 — the only arm that forces `eax = 1` (`00254C1D`) |
| `00254C24` | `0035D080` | 24 |
| `00254C2D` | `0028F970` then `00280A00` | **2, 6-11, 13-23** — and every id outside `1..24` |

**The raw dword, not the normalised id, reaches the generic scheduler.** The arm at `00254C2D`
passes `ebp` — the untouched `ecx` — to `00280A00` (`00254C37`), while `ebx` (masked) was what
selected the arm and what the policy test used. **Bit 15 therefore survives into the payload and the
descriptor** and is visible to the two widgets; a reimplementation that passes the masked id loses
it. **Both sides measured** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 327, which executed it ([package](../_index/candidates/s36-opus-replay-request-router/README.md)); the table at `01E0C2C0`, `00254B80`–`00254BC5` and `00280A00` re-read.)*: for request `0x8007` the scheduler receives `0x8007`, while `00252B40`
writes the masked `7` to `02092730` and `020927D8`. So the request word holds the masked id and the payload
holds the raw one.

## 3a. Pre-emption of the open UI, and the request-2 cancel (FABLE, 2026-10-03)

*Added on SWE2-AUDIT-SEM's S-36 point 3. Static; every body below was read from the certified image, and the callers
come from a raw `.text` index (E8/E9 rel32, 0F 8x rel32, EB/7x rel8).*

### Pre-emption: the router closes what is open before it knows whether it will serve the new request (FABLE)

R-a (`00254B71`) and R-b (`00254BC1` / `00254BC5`) pass first. Then, before the id is range-checked at `00254BD9`, the
router makes three calls **unconditionally**:

1. **`0017E7D0` (`00254BC7`)** is `jmp 0016D6A0`, and `0016D6A0` is `ret 0`. It does nothing on this build.
2. **`0035DA80` (`00254BCC`)** closes the object at `+0x10F78` of the manager at `0209BE80`, when there is one.
   - `002904B0` tests that qword (`002904B9`). When it is null, `0035DA80` returns at `0035DAB8`.
   - Otherwise it calls `00290450(1)` and stores 0 to `022C8380` (`0035DA99`).
   - It calls `00290500(0)`, which tail-jumps to `00296BE0` on that object.
   - It releases the request word through `00252D90` (`0035DAA8`).
   - It tail-jumps to `00254980(0)` (`0035DAB3`). With a zero argument, `00254980` keeps `002E1CA0`: the `cmovne` at
     `0025499B` picks `002E1C20` only for a non-zero argument. So it **clears** capability row 8 bits 1, 8, 0, 11, 9,
     6 and 20 (`002549A2`–`002549E2`).
3. **`003C8990` (`00254BD1`)** closes request 5's widget when it is open and flagged.
   - It returns at `003C8A0F` unless qword `02B47730` is non-null (`003C899B`) and that widget's byte `+0x40` has bit 4
     (`003C89A0`, `test byte ptr [rax + 0x40], 0x10`).
   - Otherwise it calls `00249C60(3)`, `0035D060(1)` and `002470C0(widget)`, stores 3 at the widget's `+0xD0`
     (`003C89CD`), calls `0035C080()`, and stores 0 at `+0xC8` (`003C89E8`).
   - It calls `0028FFE0(1, 0)` and releases through `00252D90` (`003C89FC`).
   - It tail-jumps to `002E1CA0(8, 0)` (`003C8A0A`), which clears row 8 bit 0.

**What a caller and a reimplementation must take from this:**
- **The open UI is torn down before the route runs.** That includes a request that R-c then refuses inside
  `00280A00`, and an id outside `1..24`, which reaches the generic arm. A 0 from R-c does not mean "nothing happened"
  (§4).
- **Both closers end in `00252D90`**, which zeroes `02092730` and `02092734`. When either closer runs, the word reads 0
  from that point until the route's own `00252B40`, and a refused route leaves it at 0.
- **Pre-emption never runs while the latch is 1**, because R-a refuses first. It runs only while nothing is open, or
  while the open request was posted with flag 0. Request 5's route is one such request: it posts
  `00252B40(id, 0)` at `003C88D4`.
- **The same three calls run at two other sites.**
  - The arbiter `00253C70` inlines R-a and R-b **for request 5 only**. It tests the latch at `00253FE3`, builds the
    same mask from `01E0C2C4` (`00253FFC`–`00254029`) and tests id 5's bit (`0025402B`, `test cl, 0x20`). Then it makes
    the three calls (`00254030`, `00254035`, `0025403A`) and calls request 5's route `003C87B0(5)` directly
    (`00254044`). The router is not involved.
  - `00254FC0` is the bare triple (`00254FC4`, `00254FC9`, tail-jump `00254FD2`). Its one caller is `0026C4EC`.
  - `0035DA80` alone is also called at `0029C020`, and `003C8990` alone at `00251FE8`, `00254ADC` and `00255348`.
    These callers are not followed here.

*Falsified by:* a path from R-b's pass to a route that skips `0035DA80` or `003C8990`; or a range test or dispatch of
the id before `00254BCC`.

### The request-2 cancel: the drain drops request 2 when the policy forbids it (FABLE)

The drain checks manager slot 0 first (R-5, `002E0B8B`). When the slot is ready, the drain reads the pending byte
(`002E0BAF`). It runs the cancel only when the pending byte is set and the id is 2 (`002E0BC0`,
`cmp dword ptr [0215F1A4], 2`). There are two arms, and `ebp` is 0 throughout the body (`002E09B6`):

1. **The mode term.** The drain calls `0037B330` (`002E0BCD`). `0037B330` returns byte `02ADD930`, or 4 while byte
   `02ADD931` is non-zero. A non-zero return clears the pending byte: `cmovne ecx, ebp` (`002E0BE5`), stored at
   `002E0BEC`.
2. **The policy term.** The drain recomputes the capability aggregate inline (`002E0BDE`–`002E0C52`). This is the OR of
   the sixteen dwords from `0215F1C0` to `0215F1FF`, the same code as `002E0FA0`, including `btr ebx, 0x13` when
   `00360360(0x10)` is set. The drain then re-reads the pending byte (`002E0C56`). It clears the byte when the aggregate
   has bit 0 or bit 3: `test bl, 9` (`002E0C5E`), then `cmovne r8d, ebp` (`002E0C61`). The store is `002E0C65`.

**What is stored.** Only the pending byte changes. The id and the parameter stay in their cells. The blocked byte is
cleared at `002E0D3E`, as on every drain. The router is never called: `test r8b, r8b` / `je` (`002E0CC4`) jumps over the
router call at `002E0D0B`. So the request is **dropped, not deferred**. The effect is that of the not-ready discard,
except that the id and parameter are not zeroed.

**Why bits 0 and 3.** In the inhibit table (§5a), the entries for aggregate bits 0 and 3 are both `0x4`, request 2, and
no other entry has bit 2 set. So `test bl, 9` is exactly the condition under which R-b would refuse request 2. The drain
drops the request rather than passing it to the router to be refused. The `btr` of bit 19 cannot change `test bl, 9`,
which reads bits 0–7 only. The `0037B330` term has no counterpart in the router.

**The ordering this creates.**
- The cancel runs **before** the record guard (`002E0C6C`–`002E0CA9`). If the policy forbids request 2 at this drain,
  the request is dropped even though the guard would only have deferred it. The guard never sees it.
- The post already refuses request 2 while aggregate bit 0 is set (R-2, `002E1B27`–`002E1B33`). The cancel adds bit 3
  and the mode term, and catches either condition when it arises after the post.

*Falsified by:* a store to `0215F1A4` or `0215F1A8` on the cancel path; a router call reached with the pending byte
cleared; or a cancel test for an id other than 2.

## 4. The three refusals, and why a caller cannot tell them apart

All three return **0**. They are three different states of the subsystem.

| # | refusal | where | what it means |
|---|---|---|---|
| **R-a** | the **latch**: `02092734 == 1` | `00254B71`, before any policy read | ~~a generic request is already open~~ a request posted with flag 1 is open *(corrected 2026-10-02, OPUS: `00252B40` stores its second argument in `02092734`, and `00254B50+0x2A` refuses every id while it is 1; callers passing 1 include request 3 `0035D980+0xCA`, request 24's widget `0035D6B0+0x175`, `0027EFA0+0x35`, `0035C960+0xA9` and `003F4E70+0x19C`)* |
| **R-b** | the **policy**: the requested bit is set in the inhibit mask | `00254BC1 bt` | the game currently forbids this operation |
| **R-c** | the **root is busy**: `*(0209AC30) + 0xB8` or `+ 0xC0` is non-null | `00280A1A`, `00280A28` — *inside* `00280A00`, after the router passed it | a generic request widget is still mounted |

`R-a` is tested **before** `002E0FA0` is called at all, so a latched router never reads the
capability policy. `R-c` is tested **after** the router has accepted and dispatched, so a caller that
sees 0 cannot tell whether the request was forbidden or merely late.

**The inhibit mask is rebuilt on every call.** `00254B80` reads the aggregate, then eleven iterations
walk the 22-entry table at `01E0C2C0` two entries at a time — `rcx` starts at `01E0C2C4` and each
pass reads `[rcx - 4]` and `[rcx]` and advances by 8 (`00254B88`-`00254BBF`), ORing an entry into
`r10d` for every aggregate bit that is set. The mask is never cached.
**R-b can refuse only six ids** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 327, which executed it ([package](../_index/candidates/s36-opus-replay-request-router/README.md)); the table at `01E0C2C0`, `00254B80`–`00254BC5` and `00280A00` re-read.)*. The union of the table's 22 entries is `0x20402E`: ids **1, 2, 3, 5, 14
and 21**. Nine entries are non-zero. Every other id passes the policy test whatever the aggregate holds. OPUS
tested every aggregate bit alone: the router refused exactly when that bit's entry holds the masked id's bit, 13
refusals in 154 cases. *Read here, not executed:* `bt r10d, ebx` has a register operand, so the bit offset is
taken modulo 32. A masked id of 32 or more is therefore tested as `id mod 32`: id 33 is refused whenever id 1
would be.

## 5. The mailbox is a single slot

`002E1B10` writes three of these four cells; the fourth it only reads:

```
0215F1A0   u8    pending          set 1 by the post, cleared by the drain
0215F1A1   u8    blocked          the post refuses outright while this is non-zero
0215F1A4   u32   id
0215F1A8   u32   parameter
```

Image-wide, `0215F1A4` and `0215F1A8` have **five writers and exactly one reader each**, and that
reader is the drain `002E09A0`. The five writers are the post `002E1B10`, the script path
`002E1A60`, the request-12 path `002E1AE0`, and the two resets `002E09A0` and `002E15D0` — the same
five for both cells, which is what makes them one record rather than two. The pending byte
`0215F1A0` carries those same five writers and **two** readers, the drain and `002E12D0`; the
blocked byte `0215F1A1` is written by `002E09A0`, `002E15D0` and `002E1690` and read by all three
posts plus `002E25B0`.

> **The id and the parameter have no reader but the drain.** That is the measurement R-1 rests on:
> nothing else in the image can observe a posted request, so nothing can notice one being replaced.

**A second post before the drain silently replaces the first, and both return 1.** There is no
queue, no count and no failure code for the overwrite. Seven producer call sites share the one slot:
`00253D78`, `00253EE6`, `00253F44` and `00253F53` in the input arbiter, plus `0035C81E` (request 11),
`0035D750` and the developer hook's tail-jump at `0050DAC4`.

## 5a. State (FABLE, 2026-10-03; declared on SWE2-AUDIT-SEM's S-36 D2)

§5 names the mailbox. This section declares every cell the router's own code keeps, with each cell's writers and readers.
The census is [`census_router_state.py`](../_index/candidates/fable-s36-router-repairs-1003/census_router_state.py)
(its output is beside it; FAILS 0). It covers five forms:

- RIP-relative operands in every `.pdata` body, plus the 13,800 catalogue functions that have no `.pdata` entry. Four of
  the mailbox's own accessors are such leaves.
- A raw rel32 sweep of `.text`: 167 windows, 43 confirmed instructions, none outside a decoded body.
- Image-base-relative `[reg+RVA]` forms, VA displacements, and RVA/VA constants: none.
- Addresses formed by `lea` near a cell, followed through their register.

Counts below are functions; sites are instructions. Nothing here is executed.

| address | width | name | meaning | writers (sites) | readers (sites) |
|---|---|---|---|---|---|
| `0215F1A0` | u8 | pending | 1 = a request waits in the slot | **5.** Set to 1 by the post `002E1B10` (`002E1B35`), the script post `002E1A60` (`002E1ABD`) and the request-12 path `002E1AE0` (`002E1AE9`). The drain `002E09A0` clears it at dispatch (`002E0D10`) and on the request-2 cancel (`002E0BEC`), and re-stores it, unchanged or 0, at `002E0C65`, which is the not-ready discard's store. The reset `002E15D0` clears it (`002E15D2`). | **2.** The drain (`002E0BAF`, `002E0BD2`, `002E0C56`) and the getter `002E12D0`. The getter's callers are the arbiter at `00253CBA`, which returns 0 while a request is pending, and `0035C72A` and `0035C7E6`. |
| `0215F1A1` | u8 | blocked | non-zero = every post refuses | **3.** Set to 1 by `002E1690` (`002E1690`). Cleared by the drain at the end of every drain (`002E0D3E`), and on the not-ready discard (`002E0BA3`). Cleared by the reset `002E15D0` (`002E15E5`). | **4.** The three posts: `002E1B10` (`002E1B1A`), `002E1A60` (`002E1AA6`) and `002E1AE0` (`002E1AE0`). The can-post test `002E25B0` (`002E25B4`). |
| `0215F1A4` | u32 | id | the posted request id, stored unmasked (`002E1A60` stores the translated selector, bit 15 kept) | **5.** `002E1B10` (`002E1B41`), `002E1A60` (`002E1AC4`) and `002E1AE0` (`002E1AF0`, constant `0xC`). Zeroed by the drain on the not-ready discard (`002E0B97`) and by the reset (`002E15D9`). | **1, the drain:** `002E0BC0` (the request-2 test), `002E0CD0` (the transition-exempt set), `002E0D05` (the router's `ecx`), `002E0D1B` (`00253BC0`'s `ecx`). |
| `0215F1A8` | u32 | parameter | the request's parameter, the router's `edx` | **5.** `002E1B10` (`002E1B47`), `002E1A60` (`002E1ACA`) and `002E1AE0` (`002E1AFA`, 0). Zeroed by the drain (`002E0B9D`) and by the reset (`002E15DF`). | **1, the drain:** `002E0CFC`. |
| `020927D8` | u32 | request-id copy | the masked id of the last `00252B40` call | **1.** `00252B40` (`00252B4C`), with the same value it stores to `02092730`. Neither the release `00252D90` nor the reset `00252DE0` clears it; both zero only `02092730` and `02092734`. So the copy outlives the request. | **1.** `00254710` (`00254714`), which returns `0028F740()` (word `+0x10FAC` of the manager at `0209BE80`) when the copy is 17 or 18, and 0 otherwise. It has one caller, `00346DA0` (`00346DA9`). |
| `01E0C2C0` | u32[22], 88 B, initialised data | inhibit table | entry *i* is the mask of request ids that capability-aggregate bit *i* forbids. It is indexed by the bit number of `002E0FA0`'s result and walked two entries per pass for 11 passes. | **0.** No store, no pointer constant and no image-base-relative form anywhere in the image. | **3**, each through `lea` of `01E0C2C4` and then `[reg-4]` / `[reg]`: the router `00254B50` (`00254B88`, `00254BA5`, `00254BB1`); the arbiter `00253C70` (`00253FFC`, `00254014`, `0025401D`, for request 5's inlined test, §3a); and `00254500` (`0025450C`, `00254526`, `00254530`), which returns the mask itself and has six raw call sites. |

**The table's contents** are as follows. Read from the image; the union is `0x20402E`, and there are nine non-zero entries, as U2 measured.

| entry (aggregate bit) | 0 | 1 | 2 | 3 | 5 | 6 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|
| mask | `0x4` | `0x2A` | `0x8` | `0x4` | `0x20` | `0x4000` | `0x200002` | `0x4020` | `0x8` |
| request ids | 2 | 1, 3, 5 | 3 | 2 | 5 | 14 | 1, 21 | 5, 14 | 3 |

**Notes the table does not carry:**
- **The record's bytes +2 and +3 are not mailbox state.** Each has one writer and one getter in other code (census
  rows), and nothing in §5 or §6 reads them. The fields proposal declares them so that the record's extent is honest.
- **The blocked byte lasts one drain.** The drain clears it on every path (`002E0D3E`). The script begin handlers
  `003462D0` and `003470D0` call `002E1690` right after their fullscreen post, so the block holds from that post to the
  next drain. No producer can replace the script's request in between. This narrows R-1 for the script path only.
- **The capability rows directly above the mailbox are indexed with an upper bound only.** The row writers `002E1C20`,
  `002E1CA0` and `002E1CD0` test `cmp ..., 0x10; jge`, and the reader `002E1020` has no bound at all. A row index of -6
  or less would land on the parameter or below it. Every caller the census traced passes 0 to 15: constants, a loop
  counter 0..15, or `0` or `3`. Not every constant-relative `lea` base was traced to its constant (dispositions in the
  census output). So "no caller reaches the mailbox" rests on reading, not on a bound in the code.

## 6. The invariants

Each is stated with the observation that would falsify it.

**R-1 — The mailbox holds one request, and losing one is silent.**
Three cells, five writers, one reader; the post returns 1 whether or not it overwrote an unread
request (`002E1B35`-`002E1B47`, then `mov eax, 1` at `002E1B3C`). A producer cannot detect the loss,
so **ordering between producers within one tick is a correctness property of the callers**, not of
the mailbox.
*Falsified by:* a count, a ring or a second slot in the three cells.

**R-2 — The mailbox's policy test is narrower than the router's, so passing it proves nothing.**
`002E1B10` consults `002E0FA0` for **id 2 only**, and tests **aggregate bit 0** (`002E1B27`-`002E1B33`).
The router tests **the requested id's bit** against the full 22-bit projection. A request can
therefore be accepted by the mailbox and refused by the router one step later, and for a different
reason.
*Falsified by:* a policy test in `002E1B10` that covers ids other than 2.

**R-3 — The request word is written by the route, never by the router, so it records dispatches and
not attempts.**
`00252B40` is called by every route and by nothing else in the router; it masks the id, writes
`02092734 = flag`, `020927D8` and `02092730 = id`, then tail-jumps into the per-id prelude
`00254740`. A refused request leaves all three unchanged.
*Falsified by:* a write to `02092730` on a refusal path.

**R-4 — The latch closes the router and the arbiter together.**
`02092734` has exactly **three readers image-wide**: the router at `00254B71`, the input arbiter
`00253C70` at `00253FE3`, and `003F4E70` — a mirror, not a gate: it copies the latch's bit 0 into
the window's `+0xF8` bit 0 on the mount message and never writes or branches on the latch (§8,
GH-1). The generic route sets it to 1 (`00280A60` passes
`edx = 1`), and only the release `00252D90` (`00252DCB`) and the hard reset `00252DE0` (`00252E05`)
clear it. **So while a generic request is open, the input subsystem's own arbitration sees it too** —
this single dword is where S-35 and S-36 meet.
*Falsified by:* a fourth reader, or a clear on any other path.

**R-5 — A posted request is drained in the same tick, under a guard.**
`002E09A0` is called at `0031427D`, in the **fixed tail** of `World_UpdateSimulationTick`, and the
arbiter's two call sites (`00314137`, `003141F2`) are earlier in the same body. What defers a
request is the drain's guard — `02092730` must be `0` or `5`, no slot of the eight `0x68` records at
`0215F200` may carry `+0x38` or ~~`+0x3E` bit 7~~ **`+0x3E` bit 0**, the pending byte must be set, ~~the device must be
available, and for an id outside `{12, 15, 17, 18, 19}` no transition may be running~~ — **not a frame
boundary.**
*Corrected 2026-09-26 (FABLE, Claude Opus 5.5), on `OPUS-NOTE-FABLE-S36-R5-DRAIN-GUARD`. OPUS executed the drain
(`candidates/s36-opus-replay-request-router/r45.py`), and each point was re-read here from the bytes:*
- **`+0x3E` bit 0, not bit 7.** `002E0C8D`–`002E0C9E` load the byte, `shl al, 7` / `sar al, 7` it, OR in `+0x38`
  and branch on non-zero. The shift pair keeps bit 0. OPUS measured `0x01` blocking and `0x80` dispatching.
- **The device and transition clauses never hold a request on this build.** The device term, the shared
  predicate called at `002E0CC9`, is `mov eax, 1; ret`, so the `cmove esi, ebp` at `002E0CD6` never fires. `esi` keeps the 1 it was given at `002E09C7`,
  and the transition test at `002E0CF1` (`test esi, esi; je`) never blocks, even while a transition runs.
- **A not-ready manager slot 0 DISCARDS the request; it does not defer it.** When the manager-slot readiness query for slot 0 returns non-zero
  (`002E0B8B`), the drain zeroes the request word `0215F1A4` and its argument `0215F1A8` (`002E0B97`, `002E0B9D`),
  the byte `0215F1A1` (`002E0BA3`) and, through `r8b = 0` at `002E0C65`, the pending byte `0215F1A0`. It does so
  without calling the router. A reimplementation that re-queues here keeps a request the original drops. *(This corrects the world-tick page's own earlier wording; see
[the world tick](../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md)
EX-3, corrected 2026-09-21.)*
*Falsified by:* a second drain call site, or a path from a producer to `002E09A0` that leaves the
tick.

**R-6 — The generic scheduler mounts two widgets for one request, and refuses rather than queues.**
`00280A00` builds a 16-byte payload and a 24-byte descriptor on its own stack and hands **the same
descriptor** to two `0xD8`-byte widgets with procs `0027FB70` and `00280140` (`00280A6F`,
`00280A85`). If either root slot `+0xB8` / `+0xC0` is occupied it returns 0 **before** touching the
request word, so a busy scheduler leaves no trace of the attempt.
**The per-id prelude runs BEFORE the first mount, and for some ids it reaches the sound layer** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 327, which executed it ([package](../_index/candidates/s36-opus-replay-request-router/README.md)); the table at `01E0C2C0`, `00254B80`–`00254BC5` and `00280A00` re-read.)*. The
scheduler calls `00252B40` at `00280A60`, ahead of both widget mounts. `00252B40` writes the request word and the
latch, then tail-jumps into the prelude `00254740`. OPUS traced the prelude through the stop registry to a stop
callback. For ids **2, 6, 15 and 17** a stop callback of that walk reaches the audio layer before any widget
is mounted (executed). For ids 7 and 8 it does not, and the first widget mounts first. *So for those four ids a
generic request already has a sound-side effect by the time its widgets exist. A reimplementation that mounts
first and stops afterwards reorders the two.*
*Falsified by:* a third widget, or a pending list on the root.

## 7. What a reimplementation must not do

1. **Do not treat a `0` return as one condition.** R-a, R-b and R-c are three states with three
   different remedies (wait, obey the policy, wait for the widget to unmount).
2. **Do not mask the request before the generic route.** §3 — bit 15 is carried on purpose.
3. **Do not give the mailbox a queue** without also giving the producers a way to learn they were
   replaced; seven call sites currently rely on it silently.
4. **Do not set the request word in the router.** R-3 — the word means *dispatched*, and the stop
   registry unwind in `00252D90` is paired with the prelude `00254740` that `00252B40` jumps into.
5. **Do not forget that the latch also gates input.** R-4.

## 8. What this contract does NOT establish

- ~~**Which screens the unnamed request ids open.** `7, 8, 9, 12, 13, 15, 16, 18, 19, 20` are still
  unnamed and tracked as `UQ-162` on the owning page.~~ **`UQ-162` answered 2026-09-25 (FABLE, Claude Opus 5.5)** on
  the owning page:
  - 12 is the `spattack` window;
  - 15, 17 and 18 open the world map in three kinds, 15 being the airship-route map;
  - 19 is the hunt list;
  - 7, 8, 9, 13, 16 and 20 have no producer (unused, like 14 and 21).

  It is an identity question, not a mechanism question, and this contract still does not depend on it.
- **What `003F4E70` does with the latch.** It is the third reader in R-4 and was not read.
  ***Read 2026-09-23 (SWE2-CONTRACT): it mirrors the latch, it does not gate on it — R-4 stands
  unchanged.*** `003F4E70` is a message handler dispatching on `[rdx]` (ids 1, 2, `0x10`, `0x11`).
  On id 1 — the mount message — it copies the payload into the window object `rbx` (`+0xC0` state
  byte, `+0xD0`..`+0xF0` the `0x24`-byte block, `+0xC4`), then writes `+0xF4 = dword [02092730]`
  (the request id, R-3) and folds the latch into `+0xF8` bit 0: `003F4FD7`–`003F4FE2` is
  `eax = (flags ^ latch) & 1; eax ^= flags`, the copy-idiom — **`+0xF8` bit 0 becomes the latch's
  bit 0, the rest of the flags word unchanged.** The window records *which request opened it and
  whether the latch was set*, and the id-`0x11` arm later re-issues the pair —
  `00252B40(+0xF4, +0xF8 & 1)` at `003F4EBD`–`003F4ECC`. It never writes `02092734` and never
  branches on it, so the latch still closes exactly the router and the arbiter; the third reader
  is a snapshot for the window's own bookkeeping, not a qualifier.
- ~~**The two resets `002E15D0` and `002E1AE0` as writers of the mailbox cells.** Both appear in the
  §5 sweep; only their presence is claimed here.~~ *Corrected 2026-09-25 (FABLE, Claude Opus 5.5):* `002E1AE0` is
  not a reset. It stores **request 12** into the mailbox when it is free, and it is the only producer of 12 (script
  verb `0x2A8`). The two zeroing writers of the request word are `002E15D0` and `002E09A0` (`002E0B97`). All
  five writers are read in `UQ-162` on the owning page.
  ***`002E15D0` read 2026-09-23 (SWE2-CONTRACT): a second reset, not a third producer — the §2
  producer census is complete.*** It is a 28-byte leaf that zeroes all four cells unconditionally —
  `0215F1A0` (pending byte), `0215F1A1`, `0215F1A4` (id), `0215F1A8` (param) — and returns. Its two
  callers are both teardown paths: `0026A5F0`, the manager-slot unload recursion (the
  `002E15D0`/`002E1690` pair the field-runtime-pass contract documents firing once per slot —
  dropping a pending mailbox request when its manager goes away), and `0026DB30`
  `WorldPersistence_ResetBanksForFieldTransition`, the field-transition bank reset. `002E1AE0`
  stays as previously accounted (the request-12 path, reached through `0034DA80`'s tail-jump).
- **Anything live.** No refusal here has been observed in a running process.

## 9. Evidence

**Class: NATIVE/STATIC throughout.** Every entry, call site, table and store above was disassembled
from the authority image in this session. Two figures are measured rather than read:
the six dispatch arms (`_index/candidates/fable_routertab.py`, control: ids 1 and 4 must reach one
route — they do, `0035D660`) and the cell populations in §4-§5 (`_index/candidates/fable_ripband.py`, whose counts are
**per displacement**; the caveat and its control are stated at
[the input subsystem contract](../15-Input/CONTRACT-input-subsystem.md) §6-§6a).

The request identities, the fullscreen translator's table and the producer census are **carried from**
[`Request-Router/ui-request-router.md`](Request-Router/ui-request-router.md) §2 and are not
re-derived; nothing in §6 rests on them.

## 10. Cross-subsystem neighbours — disposition (FABLE, 2026-09-21)

This contract cites the world tick `00314020` and the arbiter `00253C70`, both hubs, and both for
**one call site each** — `0031427D` and the four mailbox posts. Their other neighbours are the
per-frame work of **CombatAI**, **CombatAction**, **CombatFormula**, **Movement**,
**Spawn_Encounter_Lifecycle**, **Status_Periodic_Terminal**, **Rewards_Progression_Economy**,
**ActorEntity**, **World** and **WorldAreaField**, and the plumbing reached through the folded stub
`005C5230` and the application getter `00796E20` (**Presentation**, **Resource**, **Developer**,
**PlatformOnlineAchievements**, **SaveLoad**, **Save_Load_Settings**). None of that is a claim of
this contract.

**Party is the one worth naming by position rather than by group.** The tick's fixed tail calls
`PartyFocus_UpdatePrimarySecondaryActorProcessing` (`00358EE0`) at `00314278`, **the instruction
immediately before the drain** at `0031427D`, and `PartyControl_UpdateControlledActorLocomotion`
(`00358C60`) earlier at `003140D4`. So the party focus is republished for this tick before any
pending request is routed. This contract does not follow what either does; the adjacency is recorded
because R-5 is an ordering claim and its immediate predecessor should not be left unnamed.

**CoreRuntimeScheduling** is the frame plumbing under all of it, and it is not a neighbour of this
contract's subject either. Its five edges here are the world tick's own caller, and scheduling
and timing calls made *by* the tick, the arbiter and the drain on paths this contract never follows.
**The far ends are deliberately not cited**, because naming one would import its neighbours for a
crossing this contract does not assert; the relationship class is the same as the rest of the group,
**a hub's other work**.

Two further edges are real and named as such: **Audio**'s `00229AF0` reads the same capability
aggregate `002E0FA0` that R-b's mask is built from, and **Story_Event_Quest_Hunt**'s `0032A8A0` is
consulted by the arbiter on the path that posts request 2. Neither is followed here.


## Cross-subsystem neighbours — SWE2-EC7 batch-168 dispositions

**Resource — SERVICE (SWE2-EC7, batch 168, 7 edges).** The batch-168 `003F4DD0` submit names callback `003F4840` and caller `003F4E70`, whose neighbours `00249320`/`00249580`/`0024A5A0`/`0032E4D0` live on that layer - the router hands work items into Resource-side queue helpers, a service crossing it consumes, not owns.

**Presentation — CLIENT (SWE2-EC7, batch 168, 20 edges).** `00249580`/`0024A5A0` are also reached from Presentation bodies (`002B7B80`, `002BAF80`, `00291320`, `002CE7xx`): that layer calls the same context-open/record helpers the router's submit path uses - shared-helper consultation, not a Presentation subject here.

**SaveLoad — CLIENT (SWE2-EC7, batch 168, 2 edges).** `00249580` is called by `00582790` and `00252D90` reaches `00280140` - two save-side bodies consulting the shared context helpers; the crossing is their call, not a SaveLoad responsibility of this page.

**Input — CLIENT (SWE2-EC7, batch 168, 41 edges).** `00253C70`, the request-completion helper this page's subjects consult, tails into the input layer's `0017DE10`/`001E0D80`/`001E0F20`/`00250130` family - UI request completion polls input state; the crossing is the helper's consult, not an Input subject here.

**WorldAreaField — SHARED HELPER (SWE2-EC7, batch 168, 21 edges).** `00253C70` also reaches `00265270`/`00313F60`/`00377C20` and `0026A5F0` is called from that layer - the field layer's records feed the same completion path the router drives; shared machinery, no shared ownership.

**ActorEntity — SERVICE (SWE2-EC7, batch 168, 13 edges).** `00252DE0`/`0026A5F0`/`0026DB30` answer callers like `002628B0`/`0025D9E0`/`0026C8Cx`, and `00253C70` forwards to `0025B4C0` - actor-side bodies consume the router's request helpers; service crossing, not ownership.

**CoreRuntimeScheduling — SERVICE (SWE2-EC7, batch 168, 7 edges).** `00253C70`/`002B7B80`/`002BAF80`/`002E09A0` delegate into `001EDE70`/`001EDEC0`-band runtime helpers - the router's records ride the scheduler's shared allocators; consulted machinery, not owned.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page. Section 10's heading is numbered, so the crossings gate does not read it; these paragraphs restate its dispositions edge by edge.*

**Audio — SERVICE, CLIENT and OUT-OF-SCOPE (6 edges).** `00229AF0` calls `002DF370` and is the caller of the capability aggregate `002E0FA0`; the widget proc `0027FB70` calls `002DE350` (an 8-byte read of one audio-side state byte) and `002DEE50` (27 bytes: stores that byte and tail-jumps into the audio layer); the world tick `World_UpdateSimulationTick` `00314020` calls `002DEBA0` and `00362850`. `00229AF0` is a sibling consumer of the same aggregate R-b's mask is built from and, when bit 21 is clear, updates bits of an audio mask through `002DF370`; one of the two widgets the router installs reads and sets an audio state byte; and the tick's audio calls are its other per-frame work, outside the one call site (`0031427D`) this contract cites the tick for.

**CombatAction — SERVICE (1 edge).** `0027FB70` calls `00300060`, which walks the flagged battle units and checks each one's current action id at `+0x714` against the action rows. The widget installed by the router consults the action layer's per-unit state; the router's routing does not depend on it.

**Developer — CLIENT, OUT-OF-SCOPE (1 edge).** `001C2F50` calls the application singleton getter `00796E20`. This contract cites `00796E20` only as the source of a framework object; a developer-tool body is another caller of that getter and has nothing to do with request routing.

**Movement — OUT-OF-SCOPE (5 edges).** `00314020` calls `00234520`, `003DAA20`, `003DAA40`, `003DAC70` and `0046AFA0`. These are the world tick's movement-side per-frame work (`00234520` drives the two pending-action rings); the contract cites the tick for its drain call alone, and none of these five touches the mailbox.

**Party — SERVICE and OUT-OF-SCOPE (5 edges).** `00314020` calls `PartyControl_UpdateControlledActorLocomotion` `00358C60` (which calls `PartyControl_ApplyAnalogLocomotionToActor` `00358CB0`) and `PartyFocus_UpdatePrimarySecondaryActorProcessing` `00358EE0` (which calls `PartyFocus_ProcessActorControlPresentationState` `00358F90`); the field-transition reset `WorldPersistence_ResetBanksForFieldTransition` `0026DB30` calls `PartyFocus_ResetState` `003590E0`. As section 10 records, `00358EE0` runs at `00314278`, immediately before the drain at `0031427D`, so the party focus is republished for the tick before any pending request is routed (R-5's predecessor); the field-transition reset, one of this contract's teardown paths, also resets the party focus.

**PlatformOnlineAchievements — CLIENT, OUT-OF-SCOPE (1 edge).** `008655A0` calls `00796E20`. A platform body reaches the same application singleton getter; the contract's use of the getter is unrelated.

**Script_VM_Native_Bridge — CLIENT (8 edges).** The begin handlers `003462D0` (`openfullscreenmenu_48d`) and `003470D0` pop two script values, post a fullscreen request through `002E1A60` and then call `002E1690`; `0050DAB0` (the developer hook, verb `0x2037`) pops one value and tail-jumps into the post `002E1B10`; `0050D0C0` and `0050D240` call the manager-slot unload `0026A5F0`; and `0034E0B0`, the script query of the primary persistent-flag bank, calls `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` `0032A8A0`. The script path is how fullscreen requests are posted, the developer-hook verb is the only producer of requests 7, 8, 9, 13, 16 and 20 (the request-router page's census), and scripts can trigger the unload teardown; the router accepts their posts like any other.

**Story_Event_Quest_Hunt — SERVICE and DEPENDENCY (2 edges).** The arbiter `InputGameplay_ArbitrateDigitalInputAndModalState` `00253C70` calls `0032A8A0`, which calls `PersistentFlag_QueryAuthoredThresholdSchedule` `00377970`. The arbiter consults a persistent story flag on the path that posts request 2, so whether that request is posted depends on the story layer's flag bank.

## 11. Related

- [The native UI request router](Request-Router/ui-request-router.md) — the L1 page this formalises
- [The widget object model contract](Widget-Object-Model/CONTRACT-widget-object.md) — the other two thirds of S-36
- [The input subsystem contract](../15-Input/CONTRACT-input-subsystem.md) — the producer side; R-4 is where the two meet
- [The world tick and the field frame](../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md) — the drain's call site and its guard
- [The capability / inhibition policy](../15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md) — the aggregate R-b projects

`003F4DD0` (145 B) is the request-record submit `003F4E70` calls: stack-builds a five-pointer node (callback `003F4840`, result `r11-0x30`, the caller's `+0xC8` pointer and `+0xD0` span, zeroed links), hands it to `00244F50` with `ecx = 0x130`, and sets `rbx+0xF8` bit 1 - a routed work item enqueue under the `01F44830` cookie.

Interior anchor `003F4E3F` (function `003F4DD0`).

## Falsification pass 1 — 2026-09-29 (OPUS): every invariant survives

**Attack.** §2's sizes, §3's dispatch, §4's three refusals, §5's mailbox census and R-1 to R-6 became checks. Each
census decodes every function to the larger of its catalogue size and its `.pdata` chain union. Script:
`Tools/analysis-kit/gfz-scripts/falsify_ui_router.py`, output `falsify_ui_router.out`, image `73461d08…`, 0 BROKEN,
exit 0. The 2026-09-25 additions from OPUS block 327's execution (the raw bit-15 pass, R-b's six ids, the prelude's audio
reach) are not re-executed.

| # | Clause attacked | Result |
|---|---|---|
| U0 | §2 | **survives**: 263 / 85 / 1,002 / 193 / 29 / 71 / 123 / 104 B |
| U1 | §3 | **survives**: `and 0x7FFF`; the two tables decode to exactly the six arms and id groups tabulated; the generic arm passes `ebp`, the raw request |
| U2 | §4 | **survives**: R-a's latch compare precedes the policy call; R-b's `bt`; R-c's two root tests; the inhibit table has 22 dwords, 9 non-zero, union `0x20402E` |
| U3 | §5 | **survives**: the id and parameter cells have the same five writers and one reader, the drain; the pending byte the same five writers and two readers; the blocked byte's three writers and four readers; seven producer sites, the last a tail-jump |
| U4 | R-1, R-2 | **survives**: the post returns `mov eax, 1`; its one policy call sits behind an id-2 compare and tests bit 0 |
| U5 | R-3 | **survives**: `00252B40` masks and writes `02092730`, `02092734` and `020927D8`, then tail-jumps `00254740`; the router writes none of them |
| U6 | R-4 | **survives**: the latch has exactly three reading functions; its writers are the set (`00252B46`) and the two clears (`00252DCB`, `00252E05`) |
| U7 | R-5 | **survives**: one drain call site, `0031427D`, after the arbiter's two sites in the same tick body |
| U8 | R-6 | **survives**: both root slots are tested before `00252B40` at `00280A60`; the two widget procs are `0027FB70` and `00280140` |

No correction.

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../_index/candidates/fable-contract-ui-request-router-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `002E0DA0` | 104 B | keeps `ecx AND 0x8000` and clears bit 15 of `ecx`; a remaining value above 6 (unsigned) returns 2 OR the kept bit, and 0 to 6 go through the seven-entry offset table at `002E0E08` to arms returning, in order, 0x11, 0x12, 0xA, 0xF, 0x13, 6 and 0x16, each ORed with the kept bit | `002E0DA2`, `002E0DA6`, `002E0DAF`, `002E0DC6`, `002E0E05` |
| `002E1AE0` | 37 B | when byte `0215F1A1` is 0, stores 1 to byte `0215F1A0`, 0xC to dword `0215F1A4` and 0 to dword `0215F1A8`; otherwise returns without a write | `002E1AE7`, `002E1AE9`, `002E1AF0`, `002E1AFA` |
| `003462D0` | 81 B | stores the zero-extended byte `00229EB0()` to dword `r8+4` and 0 to dword `r8+8`, takes `a` then `b` from two `00267E10(r9)` calls, calls `002E1A60(b, a)` and `002E1690()`, and tail-jumps to `002E0650()` | `003462EB`, `003462EE`, `00346308`, `0034630D`, `0034631C` |
| `003470D0` | 91 B | calls `00267F90(r9, 0)`, stores the zero-extended byte `00229EB0()` to dword `r8+4` and 0 to dword `r8+8`, takes `a` then `b` from two `00267E10(r9)` calls, calls `002E1A60(b, a)` and `002E1690()`, and tail-jumps to `002E0650()` | `003470E5`, `003470F5`, `00347112`, `00347117`, `00347126` |

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-02, cloud-drafted)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../_index/candidates/fable-home-contract-ui-request-router-1002/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
| `0037E8A0` | 47 B | `003F4E70` + 0xB1 | returns the address `01CEB638` when qword `+0xC8` of qword `02AED490` is null or when `ecx` is not below (signed) its zero-extended word `+0xA`; otherwise loads `ecx` from its dword `+0xC + ecx*8` and tail-jumps through the jump at `0037E8A0` + 0x2A | Interior anchor `0037E8A7`; Interior anchor `0037E8B3`; Interior anchor `0037E8BF`; Interior anchor `0037E8C6`; Interior anchor `0037E8CA` |
| `0037F3B0` | 134 B | `003F4E70` + 0x1A4 | returns 0 when qword `02AED490` is non-null; otherwise builds on the stack a pair (dword `0x10000`, `rcx`) and a block (dword 0, a pointer to that pair, qword 0), makes the call at `0037F3B0` + 0x56 with 0x5F0, the code address loaded at `0037F3EE` and the block, and returns 1; both paths check the stack cookie seeded from `01F44830` | Interior anchor `0037F3C3`; Interior anchor `0037F3D2`; Interior anchor `0037F3EE`; Interior anchor `0037F406`; Interior anchor `0037F40B` |
