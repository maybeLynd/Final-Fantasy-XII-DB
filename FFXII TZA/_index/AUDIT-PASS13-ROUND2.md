# Pass 13, round two — independent re-derivation, 2026-09-14 (OPUS)

The re-run that clears [round one](AUDIT-PASS13-ROUND1.md), which failed. **A fresh sample was
required**: re-deriving round one's twelve would test my memory of round one rather than the corpus.
Same rule, same bound (48–640 bytes, every 71st of the sorted *Key addresses* pool), same
enforcement — the answers file was not opened until every derivation below was written to disk.

| | |
|---|---:|
| derivations compared | **11** |
| agree with the document | **11** |
| **findings against the corpus** | **0** |
| the auditor's semantic label was wrong | 1 (`0038EBE0`) |
| drawn, then excluded as contaminated | 1 (`002567E0`) |

**Several agreements are exact, which is worth stating because "agrees" can mean anything:**

| address | the document says | the body does |
|---|---|---|
| `001600D0` | *"4-char payload, allocates 5"* | copies 4 of the 5 bytes it allocated |
| `0032ABF0` | `PersistentFlag_SetBank2048` | refuses `id > 0x7FF` — the bound is in the name |
| `00409C30` | `…MatchesTagAndName32` | eight dwords at `+0x10`…`+0x2C`, compared inline |
| `0022B000` | *"mode 6 body; sets mode 5"* | writes `5` to `02064AD3` |
| `001BE430` | *"finds a model's record and its `%s_town` twin"* | two optional out-pointers, one per match |

**The contamination is recorded rather than hoped away.** `002567E0` was drawn, and its claim row —
*"`CAM7_HitCheck` | 384 B | dry run on the scratch player"* — had been on screen while I read the
scripted-camera page to adjudicate round one's `CAM7_ResetSlot` finding. A body whose one-line claim
I have already read cannot be re-derived blind. **Dropping a drawn item is a bias risk and naming it
is the mitigation**; the 31 other rows visible in those three pages are excluded from every later
round as well.

**And the pass found the auditor out again, in round one's exact shape.** `0038EBE0` calls
`00320D50()`, and the body divides the result by 1000 with the `0x10624DD3 / sar 6` idiom, subtracts
a stored value, adds 1000 and reduces again. With no context that reads as a clock, and it was
derived as *"a phase in 0..999 within a one-second cycle"*. `00320D50` is four instructions:

```
00320D50  mov      rcx, qword ptr [rip + 0x2b9e439]   ; 02EBF190
00320D57  cvttss2si eax, dword ptr [rcx + 0x5ac8]
00320D5F  add      eax, dword ptr [rcx + 0x5acc]
00320D65  ret
```

— **the walked-distance accumulator**, exactly as
[`the-count-clock-and-bank-recipes.md`](../08-Combat-Formula/Recipe-System/the-count-clock-and-bank-recipes.md)
says, where the same modulo-1000 arithmetic is *"the distance walked since the last use, in
thousandths"*. The arithmetic was derived correctly and the meaning attached to it was invented.

> **Twice in two rounds the auditor's error has been the same: structure from the bytes, meaning
> from a binding the bytes do not carry.** That is the finding this pass produces about itself, and
> it is the reason the protocol says pass 13 must never be mechanised — a checker cannot make this
> mistake, and cannot catch it either.

---

## The eleven derivations, as written before any document was opened

---

## `001600D0` — 240 B

**A C++ dynamic initialiser for a file-scope EASTL string global**, the same shape as round one's
`0015FE00` at a different address: the three-pointer triple at `01FD40D8` / `01FD40E0` / `01FD40E8`
with its allocator at `01FD40F0`, named by `"EASTL basic_string"`.

The assigned value is the literal `"true"` at `008FCDA0`: length computed as
`008FCDA4 - 008FCDA0 + 1 = 5`, so the `jbe 1` static-empty-buffer branch is not taken; it allocates
5 through the allocator's vtable slot `+0x10`, copies **4 bytes** and writes the NUL. Ends
`lea rcx, 008A80A0 ; jmp 00808B90` — the destructor registered with atexit.

## `001BE430` — 235 B

**Find two entries in a string list: one equal to a name, one equal to that name plus `_town`.**

`"%s_town"` is formatted into a `0x20`-byte stack buffer by `0017D2E0`. The first argument is a
vector of `char *` (`begin` at `+0x00`, `end` at `+0x08`, 8-byte elements, count by
`(end-begin) >> 3`). For each element it runs an **inlined `strcmp`** — the `sub r8, r9` trick that
walks both strings through one index — first against the plain name, storing a hit through the third
argument, then against the `_town` buffer, storing a hit through the fourth. Both out-pointers are
optional and checked for null. Carries a stack cookie, as anything with a buffer does.

## `0022B000` — 163 B

**A sibling of round one's `0022AF50`**, instruction for instruction in its first half: the same
subsystem sequence (`0036F2F0`, `0035AF10`, `0035AE30`, `0035FF90`, `0036FDF0`), the same
**spin until two consecutive reads of `[02EBA3F8]` agree**, the same tail group, the same
`003583F0(0) != 0 → 00376470 / 00375500(7)` conditional, and `return 1`.

Three differences: no string is passed to the `0016D6A0` stub (round one established that
`0016D6A0` is `ret 0`); it calls `0036D400(1, 1)` and `00375F20` where the other calls
`0022B0B0(0, 1)`; and it leaves **`byte [02064AD3] = 5`** where the other leaves `3`. So this is the
same step for a different mode.

## `002DD1E0` — 268 B

**Emit a draw packet into a command buffer, guarded by a global enable at `0215E6D0`.**

The slot is `02EBEFC0 + [02EBEFF0] * 0x18` (`lea rax,[rax+rax*2]` then `*8`); the context gets
`[ctx] = slot`, `[ctx+8] = slot[8]`, and a write cursor `[ctx+0x10] = slot[8] + 0x20`.

It then copies **four 16-byte rows — a 4×4 matrix — twice**: into the globals at `022D8F30`…`8F60`
and into the cursor, advancing it by `0x40`. Next it writes `word [src+0x5A]` into three consecutive
dwords and `word [src+0x58]` into the fourth — **the same `+0x58` / `+0x5A` pair round one found
`002D87D0` using as colour and alpha scales**. Finally it advances a second cursor by `0x10` and
writes the constants `0x8026400000000001` and `0x41414141`, which have the shape of a PS2-era
list tag rather than of data.

## `002FFCF0` — 479 B

**An eligibility test for a 16-bit id against an actor, returning a status code rather than a bool.**

    [actor] & 0x10                      required, else refuse
    [actor+0x698]                       required non-null
    ([sub+0x64] | [sub+0x3C]) & 0x80000003   if set, 00377C20() must return non-zero
    byte[sub+5] == 1 and [[actor+0x6A0]] & 0x30   refuse
    byte[sub+5] == 1 and [[actor+0x6A0]] & 0x48   refuse
    00322C50(0x14, id, 1) == 0          return 4

The `4` is a distinct refusal code, not a generic failure; the earlier refusals leave by a different
path.

## `00317930` — 493 B

**A validity test for a 16-bit id in one of five categories.** `category > 4` refuses. A per-category
sentinel table of five words at `00D107E8` (`0x1000`, then `0xFFFF`s) short-circuits to **1** when
the id equals its category's sentinel, and `id == 0xFFFF` returns **0**.

Otherwise `00322C50(6, id, 0)` decides — **the same query `002FFCF0` calls with kind `0x14`** — and
when it fails and the fifth argument is non-zero, `00309EC0(id, 0) >= 1` is a second chance. It then
walks a list at `[02EBF0F8]` whose count is at `+0x0C`.

## `0032ABF0` — 119 B

**The setter for a 2,048-bit flag bank.** `id > 0x7FF` returns without touching anything. The byte is
`id/8` (with the signed-division correction), the mask `1 << (id & 7)`, and the second argument
chooses the operation: non-zero → `or`, zero → `and` with the complement. The bank is at **`+0x13B4`**
of the singleton from `002EF2B0`.

Round one's `0032AAD0` queries a bank at `+0x14B4` of **the same singleton** with a `+0x100` bias on
the id, which lands at `+0x14D4 + id/8` — `0x120` bytes above this bank's base. **They are adjacent
banks, not the same one**, and I am not asserting a relationship between them beyond the shared
singleton.

## `0035F420` — 360 B

**Poll one input device and fold its buttons into the caller's slot array.**

`byte[rec+2]` selects a device handle from the int table at `022CB3B8`. Three calls carry the state
into fixed buffers — `00862660(handle, 022CB640)`, `00862670(handle, 022CB680)`, `00862680(022CB6C0)`
— after which the **16-bit button mask** is assembled by hand as
`byte[022CB643] << 8 | byte[022CB642]`.

`byte[rec]` is reduced modulo 16 by the `shr 4 / neg / shl 4 / add` idiom. Entries are **36 bytes**
at `rec + 0x44 + index*36` (`rax*9 + 0x11`, scaled by 4), each stamped with its slot index at `+2`,
and the loop walks the mask bit by bit. An 8-byte permutation `0507040603020100` at `01EF9238` remaps
the order.

## `0038EBE0` — 349 B

**A timed per-entity step on a 0x40-byte record, phased within one second.**

The record index is `byte[arg+4]` into the table at `0208D480` when the argument is non-null and
`byte[arg+5] == 0`; otherwise `0031B860()` supplies a context (cached to `[02EBF188]`) and the index
is `byte[ctx+0xEA9]` into a *different* table at `0208DE80`. The record is `table + index * 0x40`,
and **bit 0 of `byte[rec+0x12]` gates everything that follows**.

The timing is `00320D50()` — milliseconds — reduced by the `0x10624DD3 / sar 6` divide-by-1000 idiom,
minus a stored start at `[[02EBF190] + 0x5B00]`, plus 1000, reduced again: **a phase in `0..999`
within a one-second cycle.**

## `00409C30` — 101 B

**Does this resource entry match a tag and a name?** Returns 1 or 0.

The tag is skipped when it is `0` **or `0x4C4C4140`** — `40 41 4C 4C`, the bytes `@ALL` — otherwise
`[entry] == tag` is required. The name, when supplied, is compared as **eight dwords at
`entry+0x10` … `entry+0x2C`**, i.e. 32 bytes, each compared separately rather than through a call.

This is the same family as round one's `00409660`, which resolves an entry index.

## `006DF480` — 137 B

**A printf-style writer into a fixed 2 KB global buffer, with an installable sink.**

The four register arguments are spilled to the shadow space and `rsp+0x58` is taken as the varargs
tail, so it is variadic. `0016D670()` supplies a handle whose low bit is then set (`or rcx, 1`), and
the import at `008C2F08` is called with the buffer `02EA0BA0`, the size `0x800`, the format and the
va_list. A negative return becomes `-1` (`cmovs`).

The output is then dispatched **through the function pointer at `02EA0B88` when one is installed**,
and otherwise through the import at `008C2120`. The count is returned.
