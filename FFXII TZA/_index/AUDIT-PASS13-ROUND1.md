# Pass 13, round one — independent re-derivation, 2026-09-14 (OPUS)

**Audit protocol pass 13**, which the protocol says should never be mechanised: *"re-derive each
mechanism from the body without reading the document, then compare"*. `final_audit_verdicts.py` had
it as **"no instrument, never recorded as run"**. This is the record of the first run, published
here rather than left in a work directory, because **an audit nobody else can check is not an
audit** — the artefacts were originally cited at a `Tools/work/` path that `.gitignore` excludes.

## Method

**Blindness was enforced by the sampler, not by intention.** Every address in a *Key addresses*
table was collected, sorted, and every 72nd taken. The sampler wrote two files: an assignment
carrying **address and size only**, and an answers file naming the document and quoting its claim
row. The answers file was not opened until all twelve derivations were written to disk. **Even the
document's filename was withheld** — `battle-runtime-mode-ladder.md` tells a reader most of what a
body is before a byte is disassembled. Eight addresses read earlier in the same session were
excluded by name.

Each body was read from `disasm_fn.py`, which reads the shipping executable
(`73461D08…`, image base `0x00120000`) and resolves RIP-relative targets with the tool rather than
by hand. Every derivation below is reproducible with `disasm_fn.py <address> <size>`.

**The bound, stated rather than hidden.** Only bodies of **48–640 bytes** were eligible: below 48
there is rarely a mechanism to re-derive, and above 640 a blind reading is a day's work per
function, so the pass would have covered four things instead of twelve. **This run therefore says
nothing about large bodies**, and any verdict drawn from it carries that bound.

## The sample, and what the comparison found

| address | size | the document's claim | verdict |
|---|---:|---|---|
| `0015FE00` | 240 B | *"one process-global string: 2-char payload, allocates 3"* | agrees |
| `001BE1A0` | 572 B | `AddMotion_ParseFile`, ✅ full body | **agrees field for field** |
| `0022AF50` | 174 B | *"mode 4 body — screen capture … sets mode 3"* | agrees |
| `002566E0` | 193 B | `CAM7_ResetSlot` — *"clear four players"* | **DIFFERS — the body clears one** |
| `002D87D0` | 306 B | no name; *"near-identical sibling of `002D8690`"* | not contradicted |
| `002FD970` | 237 B | `InventoryBitsetClass_QueryState` | agrees |
| `003154B0` | 367 B | *(Platform-owned)* — **not read** | no claim to compare |
| `0032AAD0` | 104 B | `PersistentFlag_QueryBank512High` | agrees, and the name is exact |
| `0035EA40` | 291 B | `InputControl_WorkerDeadlineLoop` | agrees |
| `0038D280` | 180 B | slot 113/125 — `FinalizeTargetHpMagnitude` | **the auditor's reading was weaker** |
| `00409660` | 89 B | `ResourceEntry_FindSectionPointerByTagAndName` | agrees |
| `006B6700` | 71 B | *"embedded-string destructor — not read"* | **DIFFERS — a list-unlink loop** |

**Two findings against the corpus**, both corrected in the same commit as this record:

1. `class-descriptor-and-metadata-system.md` already carried a dated correction calling `006B6700`
   *"a list-unlink loop, not a string destructor"* — and its **Key addresses row and a later section
   still stated the refuted claim**. A correction that does not reach a page's own index and prose
   leaves the refuted claim in the two places a reader looks first.
2. `the-scripted-camera-player.md` summarised `CAM7_ResetSlot` as *"clear four players"*. It
   `memset`s **one** `0x2E0` record; the three pointer arrays it frees are in the slot header, which
   is why a slot is `0x30 + 4·0x2E0 = 0xBB0`. The page's own §2 line and layout table were already
   right — only the summary was wrong, in the direction that makes a reconstruction clear four
   records instead of one.

**Two findings against the auditor**, recorded because a pass whose findings are always against the
documents is measuring the auditor's confidence rather than the corpus:

3. `0038D280`. The independent reading called it a countdown, because
   `(float[02AEE058] − float[02AEE05C]) × float[02AEE054] → int` reads as a timer with no context.
   The step-table page binds it to slots 113 and 125 as `FinalizeTargetHpMagnitude` and names
   `02AEE054`–`5C` as the shared scratch record — the same globals. **The arithmetic does not
   determine the meaning; the table binding does**, and the document held the stronger evidence.
4. `0016D6A0` is `c2 00 00` — **`ret 0`**. Two derivations called `call 0016D6A0` a *named marker*
   because a string literal is loaded into `rcx` first. The `"SCREEN CAPTURE"` literal at `00908D38`
   is still referenced by `0022AF50` and still reaches a stub: **the instrumentation was compiled
   out and the call sites were left behind.**

**Pass 13 therefore FAILED on this run** and is recorded as failing; the protocol restarts all
thirty on any failure, and this was a failure that existed before anyone looked for it. A clean
re-run on a fresh sample is owed.

---

## The twelve derivations, as written before any document was opened

---

## `0015FE00` — 240 B

A **C++ dynamic initialiser for a file-scope EASTL string global.**

The global is the classic three-pointer `basic_string` triple at `01FD4018` (begin), `01FD4020`
(end), `01FD4028` (end-of-storage), with its allocator object at `01FD4030`; the allocator is
constructed twice by `001EDF00` and named by the literal `"EASTL basic_string"` at `008F6600`.

The assigned value is the 2-character literal at `009047A4`: the length is computed as
`009047A6 - 009047A4 + 1 = 3` (the NUL counted), so the `jbe 1` short-string branch is *not* taken.
It allocates 3 bytes through the allocator's vtable slot `+0x10`, `memcpy`s **2 bytes**, stores
`end = begin + 2` and writes the NUL. The `cmp eax,1` branch it does not take would have pointed the
string at the static empty buffer `02EBA2E0`.

It ends `lea rcx, 008A7FB0 ; jmp 00808B90` — **registering the destructor with atexit** and tail-
jumping, which is the MSVC shape for a global with a non-trivial destructor.

## `001BE1A0` — 572 B

A **three-level loader that deserialises a packed table into heap structures**, allocating with
`00210EC0` and zeroing with `00861EC0`.

    header   0x20 B   +0x14 int16 N0 (read from the stream)   +0x18 -> array of N0 x 0x10 records
    record   0x10 B   from an 8-byte source record:
                        src+0 byte  -> rec+6      src+1 byte  -> rec+7
                        src+2 word  -> rec+0      src+4 word  -> rec+4  = N2
                        src+6 word  -> rec+2      = N3
                      +0x08 -> array of N2 x 0x28 entries
    entry    0x28 B   from a 0x1C-byte source stride: qword@0, dword@8, qword@0xC, dword@0x14,
                      dword@0x18 copied straight across; +0x20 -> array of N3 x 0x1C leaves
    leaf     0x1C B   copied 1:1 from a 0x1C-byte source stride

Every count is `int16` and every multiply is guarded with `cmovo rax, -1` (the MSVC overflow-check
idiom), so a count of zero yields a zero-byte allocation rather than a skip. The 8-byte `movsd`
copies suggest the entry payload is float pairs.

## `0022AF50` — 174 B

A **capture/step routine bracketed by a named marker**: `0016D6A0("SCREEN CAPTURE")` opens it and a
second `0016D6A0` closes it, with a sequence of subsystem calls between them
(`0024F980(1)`, `0036F2F0`, `0035AF10`, `0035AE30`, `0035FF90`, then `0036FDF0`, `0022B0B0(0,1)`,
`0035AF10`, `0035AF20(0)`, `0035AE30`).

In the middle it **spins until two consecutive reads of the dword at `02EBA3F8` agree** —
`mov ecx,[x] / mov eax,[x] / cmp / jne` — the shape of waiting for a counter written by another
thread to settle. It then runs a second group, and conditionally (`003583F0(0) != 0`) calls
`00376470` and `00375500(7)`. It leaves `byte [02064AD3] = 3` and returns 1.

## `002566E0` — 193 B

**Reset one slot of a 5 x 4 array of 0x2E0-byte records**, with a per-row header.

`cmp ecx,5 / jge ret` bounds the first index; strides are `0xBB0` (outer) and `0x2E0` (inner) over
the base `02092830`, and `0xBB0 / 0x2E0 = 4` exactly — but the row header sits at `02092800`, which
is `0x30` **before** the first record, so a row is `0x30 + 4 * 0x2E0 = 0xBB0`. The arithmetic closes.

It `memset`s the record, writes `-1` into `+0x184` (an id/handle field set to invalid), and calls
`003CBFF0` on the sub-object at `+0x210`. Then, on the **row header only**, it zeroes `+0x08` and
releases three owned pointers at `+0x10`, `+0x18`, `+0x20` through `003697F0`, nulling each.

## `002D87D0` — 306 B

**Modulate a colour and hand a draw command to another object.**

Three bytes at `A+0x90..0x92` are each multiplied by the int16 at `A+0x5A` and shifted right 7
(fixed-point /128) into a packed RGB triple; the byte at `A+0x93` is scaled by a *different* int16,
`A+0x58`, for the fourth channel. The packed dword is stored to `A+0x94` and to `B+0x30`.

`00364980([B+0x28])` then chooses between two paths. On the fast path it writes `B+0x60` (the byte
at `A+0x64` minus one, or 0 when that byte is <= 0) and calls `003649A0(B)`. On the slow path it
constructs a temporary via `00203170`, stores the two float arguments into it at `+0x60`/`+0x64`,
calls `00397910(A, tmp, tmp)`, sets `B+0xB8 = 0x3001` and `B+0x20 = tmp`, and calls `002B0280(B)`.

Either way it clears the `A+0x64` latch. The body carries a stack cookie (`01F44830`), so it has a
buffer.

## `002FD970` — 237 B

**A bit-flag query keyed by a packed 16-bit handle.** Returns 0 or 1, never anything else.

`handle >> 12` selects one of at most 16 records of `0x58` bytes at `01EEBCC0`; `handle & 0xFFF` is
the element index. The second argument selects the set:

    kind 0, 1   bitset at rec+0x08, WORD-addressed: bit (idx & 0xF) of word[idx >> 4]
    kind 2      no set - returns 0
    kind 3      bitset at rec+0x20, BYTE-addressed: bit (idx & 7) of byte[idx >> 3]
    kind 4      bitset at rec+0x30, BYTE-addressed
    pointer null -> 0

The `cdq / and edx,7 / add / sub / sar 3` sequence is signed-division-by-8, so a negative index is
handled arithmetically rather than rejected.

## `003154B0` — 367 B

**A generic "is this condition satisfied" query** over a (category, index) pair, with three shapes.

    category < 5   per-category base and count in two int16 tables at image 0x00D10630 / 0x00D10640;
                   index >= count -> 0. Otherwise bit (base + index) of the bitset at +0x32CC of
                   the singleton returned by 002536A0.
    category == 7  index < 0x1E; bit `index` of a second bitset at +0x3844 of the same singleton.
    category == 6  index < 0x200; walks a table at [022C2550]: +8, a 16-bit relative offset, an
                   entry count at +6, then 4-byte records whose LOW 12 BITS are the index. On a
                   hit, the record's top nibble selects the test:
                     nibble 0 -> compare 00265270()'s int16 against word[rec+2], satisfied if >=
                     nibble 1 -> recurse: 00315420(word[rec+2]) > 0
                   Miss, or any other nibble -> 00315420(index) > 0.
    anything else  0

## `0032AAD0` — 104 B

**A flag query over the second block of a two-block bitset.** `id` must satisfy `0 <= id < 0x100`
(both bounds explicit; the negative case returns 0 rather than indexing backwards). The bit tested
is `id + 0x100` of the bitset at `+0x14B4` of the singleton from `002EF2B0` — so ids 0..255 occupy
bits 256..511, and bits 0..255 of the same array belong to something else.

## `0035EA40` — 291 B

**A timed pump loop, the body of a worker.**

It opens with `0016D6A0(0x7C)` — the same marker call `0022AF50` uses with a string — publishes
`[022CA630] = 1` on entry and `0` on exit (a "running" flag), and runs while `[022CA634] != 0` (the
enable/count flag, tested four separate times).

Each iteration: spin on `0017D3E0`, sleeping via `008635F0(1)` between polls; acquire `[022CA610]`
through `00863650`; read a double clock from `005A0820`; take the scheduled time
`double[022CA640 + slot*8]`. A **negative** scheduled time is a first-use marker — it records the
clock as the base (`xmm7`) and negates the value with the sign mask `8000000000000000` from
`01CEBD90`; otherwise it subtracts elapsed time to get the remainder. If any time remains, it
signals `[022CA618]` through `00863690` with the remainder truncated to an integer (milliseconds).
Then, if `[022CA5F8]` is set and `[00369160()] != 0`, it calls `003691B0(0)`.

The slot index wraps at 256 (`lea eax,[rbx+1] / movzx ebx, al`), so the schedule array is 256
doubles.

## `0038D280` — 180 B

**A countdown step that routes a scaled remainder into one of two slots.**

`xmm1 = float[02AEE058] - float[02AEE05C]`. If that is negative, it stores `0` to `[02AEE004]` and
returns. If `[02AEDFCC] != 0` it takes an abort path: `[02AEDFC0] = 1`, `[02AEE004] = -1`, and
`or dword [[r8+0x10] + 0x140], 1` — setting bit 0 of a flag word on an object reached through the
argument.

Otherwise it scales: `eax = (int)(remaining * float[02AEE054])`. Which of `[02AEE004]` and
`[02AEE008]` receives it, and which is set to `-1` (inactive), depends on both `[02AEDFD0]` and
bit `0x1000` of `[r8+8]` — the four combinations are written out separately. If the value that
ends in `eax` is not `-1`, it **tail-jumps to `00387B00`**; otherwise it returns.

## `00409660` — 89 B

**Resolve an index, or 0.** A null `this` returns 0. It calls `00409780` with two stack outputs; if
the int at the first is `-1` (not found) the function returns 0. Otherwise it calls `00409600(this)`
for a base and returns `base + found`, sign-extended to 64 bits.

## `006B6700` — 71 B

**`intrusive_list::clear()`** — detach every node from a circular doubly-linked list.

The head is the argument; `[head] == head` means empty. Each node's links live at `+8` (prev) and
`+0x10` (next), so the node pointer is `link - 8`. It unlinks in the standard order
(`prev->next = next; next->prev = prev`) and then **self-links the removed node's two pointers**,
which is what makes the node safe to re-insert. Nothing is freed — this detaches, it does not
destroy.
