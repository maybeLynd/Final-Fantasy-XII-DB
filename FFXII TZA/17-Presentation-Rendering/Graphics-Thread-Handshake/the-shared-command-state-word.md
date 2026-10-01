---
system: The shared graphics command-state word and the settle-spin handshake
category: 17-Presentation-Rendering
status: AUDITED
owner_layer: PrimaryOwner:Presentation
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 48 cited function entries, 0 of them among the 109 records that changed GN160 -> GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0), established for this document 2026-09-14 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-07
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-shared-command-state-word-pass-1
  crossref_clean: true
  reopened_count: 2
---

# The shared graphics command-state word

> One 32-bit global is the entire handshake between the thread that runs the game and the thread
> that draws it. **Every instruction that implements it is invisible to Ghidra's decompiler.**

## 1. What the player sees

Nothing — while it works.

FFXII packs what happens each frame — who swung, where the camera is, which effect fired — into a
**batch of drawing commands**, publishes it, and then reaches a point where it will not go on until
the batch has been accounted for.

> ⚠ **Corrected 2026-09-07, hours after this document was written.** The first version of this
> section said the batch is handed to *a second thread that turns it into pixels*. **That is not
> established and the evidence now points away from it** — see section 10. What is proven is the
> publish-and-account protocol below; **who consumes the batch is an open question.**

**The waiting is real and it is a spin, not a sleep.** At eleven points in every frame — two of them
inside the main loop itself — the game reads one shared word twice in a row and loops until the two
reads agree, burning CPU rather than yielding it. Whatever is on the other end of that word, the game
will not proceed until it settles.

It is also why the in-game **screen capture** briefly costs a frame: capture sets its own bit in the
same word, and the same handshake has to run before drawing continues.

## 2. Native mechanism

### The word

**`0x02EBA3F8`** — a single `dword`. **24 write-form and 38 read-form references** across the image,
and every one of them is in graphics submission, the main loop, or effect capture.

### The idiom: spin until two reads agree

```asm
0036F2D0  mov  ecx, dword ptr [02EBA3F8]        ; read it
0036F2D6  mov  eax, dword ptr [02EBA3F8]        ; read it AGAIN
0036F2DC  cmp  ecx, eax
0036F2DE  jne  0036F2D0                         ; disagree -> read both again
0036F2E0  and  dword ptr [02EBA3F8], 0xFFFFFEF3 ; agreed -> clear bits 2, 3, 8
0036F2EA  ret
```

Two loads of **the same address**, compared, looping while they differ. The loop exits only when the
value is **stable across two consecutive reads** — that is, when the other thread is not part-way
through updating it. It is a lock-free settle wait, with no atomic instruction, no `lock` prefix and
no memory barrier.

The whole of `GraphicsSync_ClearSharedCommandStateBits` (`0036F2C0`) is 43 bytes and does exactly
this.

### The bits, and who moves them

`AND 0xFFFFFEF3` clears the complement of `0x0000010C`, so bits **2, 3 and 8**.

| bit | mask | set by | cleared by |
|---:|---|---|---|
| **8** | `0x100` | `GraphicsCommand_PublishCompletedBatchState100` (`0036F3EB`), `GraphicsCommand_CopyAlignedBatchAndPublishState100` (`003A2E16`), `GraphicsCommand_CopyAlignedBatchWithControlRecordsAndPublishState100` (`003A2F59`) — each `mov dword [02EBA3F8], 0x100` | `GraphicsSync_ClearSharedCommandStateBits` (`0036F2E0`); both capture paths |
| **2, 3** | `0x4`, `0x8` | ~~not located~~ only the reset burst (`0036F32F`–`0036F33B` clears 2 / sets 3; `0036F348` writes `0x14D`, both set) — **and no instruction in the image tests either bit** (2026-09-12, `CG-1`) | `GraphicsSync_ClearSharedCommandStateBits` (`0036F2E0`); the burst's own final store of 0 (`0036F352`) |
| **4, 5** | `0x30` | ~~not located~~ only the reset burst's `0x7FFF0` (`0036F313`) — never tested (2026-09-12, `CG-2`) | `GraphicsSync_WaitBackendState100Cl…` (`0036F341`, `AND 0xFFFFFFCF`), then the burst's final 0 |
| **16** | `0x10000` | `EffectCapture_ProcessCaptureDraw` (`00374CEC`), `EffectCapture_ProcessSecondaryCaptureDraw` (`003761EC`) — `OR 0x10000` | the same two, `AND 0xFFFEFEFF` (`00374CF6`, `003761F6`) — which clears **8 and 16 together** |
| 4–18 | `0x7FFF0` | `GraphicsSync_WaitBackendState100Cl…` (`0036F313`) writes the literal `0x7FFF0` | |

> *Read with UQ-211 (2026-09-18):* the publishers store an address and a count into this same cell immediately before the `0x100`, so the rows above are successive values of one dword, not independent fields.

**Bit 8 is the batch-published flag, and the ledger's own function names say so**: three separate
publishers write the literal `0x100` into this word, and all three are named `…PublishState100`.
**"State100" is the value `0x100`.** The protocol is:

```
graphics side : publish a batch     ->  [02EBA3F8] = 0x100          (bit 8 up)
game side     : settle-spin until the word is stable
              : AND 0xFFFFFEF3       ->  bits 2, 3, 8 down          (batch consumed)
```

Effect capture layers on top: `OR 0x10000` to mark a capture in flight, then one
`AND 0xFFFEFEFF` that retires **the capture bit and the published-batch bit together**.

### Where the spin is inlined — a complete census

~~Twelve settle-spin loops exist in `.text`.~~ **Eleven settle-spin loops exist in `.text`, and all eleven spin on `0x02EBA3F8`** (corrected 2026-09-13):

| loop | owning function |
|---|---|
| `0022A850`, `0022AE50` | `0022A770` |
| `0022AFA0` | `0022AF50` |
| `0022B040` | `0022B000` |
| `0022B2C0` | **`MainLoop_Draw`** (`0022B0B0`) |
| `0022B720` | `0022B6E0` |
| `0022B820` | `0022B7E0` |
| `0022BAD0` | **`MainLoop_UpdateAndRenderFrame`** (`0022B8C0`) |
| `0022BD20` | `0022BC20` |
| `00262AE0` | `002628B0` |
| `0036F2D0` | `GraphicsSync_ClearSharedCommandStateBits` (`0036F2C0`) |

`0022B6E0`'s 9-member exclusive subtree is bound on
[the resource-queue page](../../02-Resource-And-Asset-Pipeline/the-resource-request-queue.md) —
its `0022B720` spin drains this word before `GraphicsSync_ClearSharedCommandStateBits` runs
at `0022B7A4`.

~~The twelfth, `0037CE10` in `AddMotion_LoadHighModelReplace` (`0037CCC0`), uses the same
settle-until-stable shape on a **different** global, `0x02ADD940`, over 11 instructions rather than
4 — so the idiom is a house style, not one function's quirk.~~

> **Corrected 2026-09-13 (OPUS): `0037CE10` is not a settle-spin.** Its two loads of `02ADD940` go
> into **the same register** (`mov rax, qword ptr [rip…]` at `0037CE10` and again at `0037CE29`), so
> the second overwrites the first rather than being compared with it — and the loop's `cmp` is
> `ecx, -1` against **source data**, not against a second read. It is a copy loop advancing `rdx` and
> `rbx`, storing through `[rdx + rax - 0x14]` and `[rdx + rax - 4]`, terminated by a `−1` sentinel;
> `02ADD940` is a **qword base pointer** reloaded because the compiler did not keep it live across
> the stores, not a dword state word. **There are eleven settle-spins, not twelve, and all eleven are
> on `02EBA3F8`** — see the falsification pass.

Several inlined sites spin and then **call `0036F2C0`**, which spins again before clearing. The wait
is therefore performed twice on those paths: once inline, once inside the clear.

> *Answered by reference 2026-09-14 (FABLE, `CG-5`): the double wait costs a few instructions and guards nothing.* A
> settle-spin repeats only when a store to `02EBA3F8` lands between its two loads, which needs a writer on another core.
> The eight writer functions (the three publishers, the clearer, the reset burst, both effect-capture draws, `0036D7E0`)
> all run on the main thread, and no thread start reaches any of them (`CG-3`, §7). So on every path both spins are two
> loads and a compare that agree on the first pass, and the second spin is redundant rather than protective. It costs
> nothing measurable in frame pacing. The limit is `CG-3`'s: the Tk workers' per-thread callback tables were not followed.

## 3. Why this is invisible to the decompiler

**Ghidra emits only the `and`.** The two loads read the same address with no `volatile` qualifier, so
common-subexpression elimination folds them into one value; `cmp x, x` is then constant-true, the
`jne` is proven unreachable, and the loop is deleted as dead code.

That transformation is **correct under the C memory model and wrong about the machine.** Under C, a
non-`volatile` object cannot change between two adjacent reads; on the hardware, another core writes
it.

> **Read from decompiled output alone, this engine's frame contains no synchronisation whatsoever.**
> Eleven waits — including both inside the main loop — vanish, and what remains looks like a plain
> flag clear.

Originally observed by `xiionline-13` on `0036F2C0`; the census above was produced independently by
disassembling `.text` and is reported at 12 sites against their 11, the difference being the
`0x02ADD940` site on a different global.

**Consequence for this database: every threading claim sourced from decompiled output is suspect**
and owes re-derivation from disassembly. Tracked as `CF-6`. *(2026-09-18: answered - both loop shapes are censused image-wide and the debt is a list of thirty loops; see "The second failure mode, censused" below.)*

## 4. Data structures and formulas

```
sync word            [0x02EBA3F8]  dword

settle wait          do { a = word; b = word; } while (a != b);

publish a batch      word  = 0x100                       /* bit 8 */
consume a batch      word &= 0xFFFFFEF3                  /* ~0x0000010C -> clears 2, 3, 8 */
backend state gate   word &= 0xFFFFFFCF                  /* ~0x00000030 -> clears 4, 5   */
capture begin        word |= 0x00010000                  /* bit 16 */
capture end          word &= 0xFFFEFEFF                  /* ~0x00010100 -> clears 8, 16  */
```

## 5. Call chain

```
MainLoop_UpdateAndRenderFrame 0022B8C0
   settle-spin 0022BAD0 on 02EBA3F8
MainLoop_Draw 0022B0B0
   settle-spin 0022B2C0 on 02EBA3F8  -> call GraphicsSync_ClearSharedCommandStateBits 0036F2C0
                                            settle-spin 0036F2D0 -> AND 0xFFFFFEF3

GraphicsCommand_CopyAlignedBatchAndPublishState100                003A2D80  -> word = 0x100
GraphicsCommand_CopyAlignedBatchWithControlRecordsAndPublishState100 003A2E30 -> word = 0x100
GraphicsCommand_PublishCompletedBatchState100                     0036F360  -> word = 0x100

EffectCapture_ProcessCaptureDraw           003749F0  -> OR 0x10000 ... AND 0xFFFEFEFF
EffectCapture_ProcessSecondaryCaptureDraw  00376050  -> OR 0x10000 ... AND 0xFFFEFEFF
```

## 6. Modding notes

- **Do not read this engine's threading from decompiled output.** Disassemble. The single most
  important synchronisation primitive in the frame is deleted by the decompiler at all eleven sites.
- **The wait is a spin, not a sleep.** A hook that lengthens the graphics side does not yield the
  core; it burns it. Anything injected between publish and consume is inside a busy-wait.
- **Bit 8 is the one to watch.** Three publishers write the whole word to `0x100` — not `OR`, a
  plain `mov` — so a publish **discards every other bit**. Any bit a mod sets in this word before a
  publish is lost.
- **Capture retires two bits at once.** `AND 0xFFFEFEFF` clears the capture bit *and* the
  published-batch bit; treating the capture path as independent of batch submission is wrong.

## 7. What is not known

- [x] ~~**What bits 2 and 3 mean.** They are cleared with bit 8 by the same instruction and **no
  writer that sets them has been located.**~~ **`CG-1` ANSWERED 2026-09-12 (FABLE): in this build
  they mean nothing observable — they exist only inside the reset's nine-store burst, no wait
  separates the stores, the burst ends by storing 0, and no instruction in the image tests
  either bit.** The complete reader census of `02EBA3F8` (40 loads, function list plus the gap-code
  index, which has none) is: the settle-spin pairs in the nine frame callers (`0022A850`…`0022BD26`,
  `00262AE0`) and in the clearer (`0036F2D0`); the burst's own read-modify-write (`0036F32F`); the
  publishers' guard reads, which compare the word against cursor words as unsigned ranges
  (`0036F3B2`–`0036F3E9`, `003A2DE1`–`003A2E14`, `003A2F10`–`003A2F5B`) with no mask; and effect
  capture's `bt eax, 8` spins (`00374C76`, `00374CB6`, `00374CE6`, `00376176`, `003761B6`, `003761E6`).
  Nothing masks `0x4`, `0x8`, `0xC` or `0x14D`. Between the burst's first store and its last there is
  no branch, call or wait, so on the one thread that exists here (`CG-3`) the intermediate values
  can only ever be seen by another core, and the fence that would name that core (`02EAF6D8`) is
  never written. So the burst is a fossil of a console-side command protocol — write the state
  block's address, a 15-bit mask, a command word `0x14D`, then 0 — carried over into a build with
  no consumer; what each command *meant* to that backend is not decidable from this executable.
  The same census answers **`CG-2`** below.
  *Premise corrected 2026-09-12 (FABLE):* setters exist, in
  `GraphicsSync_WaitBackendState100ClearAndResetSharedState` itself — `and eax, 0xFFFFFFFB` / `or
  eax, 8` / store (`0036F32F`–`0036F33B`: clears bit 2, **sets bit 3**), then the literal **`0x14D`**
  (`0036F348`: bits 0, 2, 3, 6, 8 — **sets both**). The earlier census read immediates at the
  `or` sites only; these go through a register and a full-word literal. Every write-form reference
  to the word is dword-wide (24 sites) and the one qword store in the neighbourhood (`00862CC6`,
  `02EBA3F0`) ends at `+7`, so no wider store reaches it, and the gap-code operand index (code
  outside the function list) has no reference to `02EBA3F8` at all. What the two bits *mean*
  stays open; the reset sequence writes the word nine times in a row (`0036F30D`–`0036F352`:
  ~~`eax` (0)~~ the low dword of the address `022D9B50` (`lea rax` at `0036F304` — the frame page's
  reading; the word after the command-stream family's state block at `022D9AB0`–`022D9B4C`),
  `0x7FFF0`, 0, that address twice, `(w & ~4) | 8`, `w & ~0x30`, `0x14D`, 0), which reads as a
  command sequence for the other thread rather than a state.
- [x] ~~**What bits 4 and 5 mean**, and why `GraphicsSync_WaitBackendState100Cl…` writes the literal
  `0x7FFF0` (bits 4–18) into the word at `0036F313`.~~ **`CG-2` ANSWERED 2026-09-12 (FABLE) with
  `CG-1`:** `0x7FFF0` is the second store of the same uninterrupted nine-store burst, overwritten
  by 0 two instructions later and by the burst's final 0 at its end; bits 4 and 5 are set by
  nothing else and tested by nothing in the image (census above). The mask-then-partial-clear
  pattern is what a command protocol looks like when its consumer is gone, not a flag field.
- [x] ~~**Which thread executes the publishers.** The handshake is proven; the thread topology is
  inferred from the settle-spin idiom, not read.~~ **`CG-3` ANSWERED 2026-09-12 (FABLE): the main
  thread — and on PC there is no other party.** Three instruments, none of which passes through
  `MainLoop_*` by assumption. **(1) Upward.** A function-list-independent `E8`/`E9` caller index walked
  from each publisher to its roots: `GraphicsCommand_PublishCompletedBatchState100` (834 functions
  explored, every root a frame or input entry such as `0017CCD0`, `0017D090`, `00227EE0`, `0023B330`,
  with `MainLoop_UpdateAndRenderFrame` `0022B8C0` and `MainLoop_Draw` `0022B0B0` on the graph — e.g.
  `0036F360` ← `RenderCommand_SubmitCurrentBufferAndSwap` `003A1DB0` ← `0036D400` ← `0022B000` ←
  `0022A580` ← `0022A490` ← `0017D6E0` ← `0017CCD0`); `GraphicsCommand_CopyAlignedBatchAndPublish
  State100` (29 explored, root `0022BEB0` via `VFXSystem_RenderLayerPass`, same two `MainLoop_*`
  functions on the graph); and `GraphicsSync_ClearSharedCommandStateBits` itself (17 explored, roots
  `0017CCD0` / `0022BEB0`, both `MainLoop_*` on the graph) — so the bits are set and cleared by the
  same thread — `0022A580`'s own members are now bound on the game-application page (the worker
  deadline enqueue/drain family). The third publisher, `GraphicsCommand_CopyAlignedBatchWithControlRecordsAndPublish
  State100`, has a single caller `0045BAE0` (interior read 2026-09-17, SWE2-FRONTIER: 1,068 B — `00434A70` first at [`0045BB57`](../../_index/ADDRESS-INDEX.md), `00202D50` ×5 + `0020E600` ×4 + `0039B960` ×3 — a workbench-armed commit body) that ~~has no caller, no `E9`, and no pointer anywhere in
  the file: unreached in this build~~ **IS REACHED — corrected 2026-09-16 (OPUS).** The three instruments
named in the struck clause are the three that missed three other bodies on the same
day: none enumerates **`0F 8x rel32`**, the conditional near jump. The route, every site verified to be
a real instruction boundary by decoding its container from that container's own entry:

> ```
> FUN_00441970 [Presentation]   call 002F4020    at 00441A47 and 00441A77
> FUN_002f4020                  call 0045BAD0    at 002F42C2
> 0045BAD0  cmp byte ptr [rcx], 0      a 10-byte guard stub
> 0045BAD3  jne 0045BAE0               conditional TAIL JUMP, out of its own 10 bytes
> 0045BAD9  ret
> ```
>
> The top of the chain is **`Presentation`-owned**, which is the right neighbourhood for a
> graphics-command publisher. The identical idiom — a tiny guard stub that conditionally tail-jumps
> into a body whose census then misses the route — also hides the nine-patch box renderer
> described on its own page in `99-Unresolved-Residual`.
>
> **The premise is refuted; the runtime question is not answered.** Whether `[rcx]` is ever non-zero
> is not decidable from the bytes, so this publisher is **not known to be unreached** rather than
> known to run. The two-thread topology argument below rested on it being unreached and is weakened
> to that extent; it is left standing rather than rewritten, because the thread evidence is separate
> and belongs to whoever owns it. **(2) Downward.** Every thread the process creates was
  enumerated two ways — the imports (`CreateThread` ×5, `_beginthreadex` ×4: the VP8 decoder threads
  `00171370`, ~~the D3D workers~~ `005CCAB0` / `005CCBA0` *(relabelled 2026-09-14, FABLE: `005CCAB0` is the minidump-writer thread and `005CCBA0` a guarded thread trampoline that calls the function at `ctx+8` with the argument at `ctx+0x10` after an `IsDebuggerPresent` test; neither is a D3D worker — [the runtime service surface](../../24-Compiler-And-CRT-Runtime/Runtime-Service-Surface/what-the-game-asks-windows-for.md), CV-3)*, the audio thread `007A5550` from three sites,
  `007DEC40`, `007DD950`, and the CRT trampoline `00863500`) and the engine's own thread API
  `008636E0` that the import census cannot see (descriptor = entry, 0x4000 stack, name, argument,
  priority): **`TkSyncVEmulationThread`** (`0035EA40`, priority 30, from `InputControl_Initialize
  AndRegisterFrameUpdate`), **`TkBGThread%d`** (`00368C10`, 36), **`TkSyncvThread%d`** (`00369100`, 30)
  and **`TkPowerOff`** (`00368AE0`, 1), all four created by `00368ED0`. A breadth-first walk over
  calls and tail jumps to depth 8 from every entry reaches none of the three publishers, the
  bit-clearer, or any function that touches `02EBA3F8` or `02EAF6D8`; the Tk workers dispatch through
  per-thread callback tables (`021B7F70`, `021AFF10`), which is the one route this instrument cannot
  follow. **(3) The fence.** The "backend" word `02EAF6D8` the reset spins on (`0036F2F0`–`0036F302`,
  `and eax, 0x100`), `02EAF6D8` has **no writer**: no rip-relative store (24 listed references, all reads), no
  reference in the code outside the function list (gap index), and no store through the two bases
  that are address-taken beside it (`02EAF6C0` `+0x18`, `02EAF6E0` `−8`, in the Tk library
  `00859D20` / `00862130` / `008621E0` / `008624D0` / `00862A20` / `00862A40`); it lies past `.data`'s
  raw size, so it is zero for the life of the process and the spin never iterates — as [what happens between two frames](../../22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md)
  already records ("never"). Conclusion: the settle-spin and bit-8 protocol is the PS2 GS handshake
  carried into the PC port with **no backend thread behind it**; both "sides" execute on the main
  thread inside the frame, and the wait is a no-op. A reimplementation may keep the protocol for
  fidelity but must not block on it.
- [x] ~~**Whether `0x02EAF6D8` runs the same protocol.** `xiionline-13` is chasing "the thread that
  clears `02EAF6D8` bit `0x100`" — **a different global with the same bit-8 role**, which suggests a
  family rather than a singleton.~~ **`CG-4` ANSWERED 2026-09-12 (FABLE): no protocol at all.** The
  word `02EAF6D8` has no writer of any form (rip-relative, gap code, or through the two address-taken bases
  beside it — CG-3 §7), is zero for the life of the process, and every one of its seventeen waits
  is a hoisted load that cannot observe a change; there is no thread to chase. It is a fence with
  nobody on the other side, not a second command-state word.
- [x] **UQ-211.** No body of the three publishers has been read in full; only their writes to this word.
      **ANSWERED 2026-09-18 (FABLE): all three read whole, and what they do is program a PS2 DMA channel whose registers have all been given the same address.**
      - **`0036F360` (150 B), `(buffer, count of 16-byte records)`.** If the last record's first dword has `0x30000000` under the mask `0x70000000` it appends one more record `{0x10000000, 0}` - or, at `0x200` records or more, overwrites the last one with it (`0036F372`..`0036F39C`). Then it stores `buffer & 0x3FF0` to `02EBA3F8`, stores the count to **the same cell** (`0036F3A6`, `0036F3AC`), loads that cell three times into three registers and compares them with each other as if they were a read cursor, a write cursor and a size (`0036F3B2`..`0036F3E9`), and stores `0x100` (`0036F3EB`). It calls nothing and reads nothing from the buffer except that one dword.
      - **`003A2D80` (171 B), `(source, byte count)`.** Rounds the size up to 16, `memcpy`s the batch to the buffer at `[02F8F2E0]`, spins on bit 8 of `02EAF6D8` (the word CG-4 shows is never written), flips bit 10 of the buffer pointer's low dword with `xor 0x400` - two staging buffers `0x400` apart - and then performs the same address / count / three-loads / `0x100` sequence on `02EBA3F8` (`003A2DC5`..`003A2E16`).
      - **`003A2E30` (314 B), `(source, bytes, second pointer, second byte count)`.** The same copy, then it writes two 16-byte records after the batch by hand: `{u16 = second count / 16, byte +3 = 0x30, dword +4 = the second pointer as a 32-bit image address}` through `RuntimePointer_EncodeImageAddress`, and `{u16 0, byte +3 = 0x10, dword +4 = encoded null, dword +8 = 0, word +0xC = 0x0404, byte +0xF = 1}` (`003A2E95`..`003A2ED2`); then the same register sequence with count + 2.
      - **Reading, labelled as such.** Every value fits the PS2 DMA controller and nothing else offered so far: 16-byte records whose top nibble is a tag id (`3` = *ref*, carrying a 32-bit address and a word count; `1` = *cnt*) are DMA source-chain tags; `0x01000404` in a tag's spare words is the VIF code STCYCL 4,4 that [the VIF1 page](../Legacy-PS2-GS/the-vif1-vu1-layer.md) decodes; address then count then `0x100` is MADR, QWC and the CHCR start bit; and the reset burst's pointer, `0x7FFF0`, the bit 2 / 3 edit and `0x14D` read as ring base, ring size mask, the control register's drain field and a CHCR mode word. On the PS2 these are different registers. **In this image they are one cell**, which is the static fact and does not depend on the reading: the three 'cursor' loads can only return the value just stored, so each guard loop ends on its first pass, and the table in section 3 is a list of values that pass through one dword rather than a set of independent bit fields. It also explains CG-1, CG-2 and CG-4 together - bits never tested, a fence never written, one thread - as the remains of a hardware kick with no hardware behind it.
      - **What this does not say:** how a batch then reaches the renderer. None of the three hands the buffer to anything; the consumer of the staging buffers at `[02F8F2E0]` and of the ring they are copied from was not traced here. Static, three bodies and the reset read in full; the register names are inference from the values.

## 8. Evidence

| claim | evidence | tier |
|---|---|---|
| The idiom is a settle-spin on one global | complete 43-byte disassembly of `0036F2C0`; all three RIP-relative operands resolve to `02EBA3F8` | 1 |
| Eleven inlined sites on this global, twelve overall | `.text` disassembled function by function; loops matched as "≥2 RIP loads of one address + cmp + backward `jne`" | 1 |
| Bit 8 is the published-batch flag | three publishers write the literal `0x100`; the ledger names all three `…PublishState100` | 1 + 4 |
| Clearing bits 2, 3, 8 | `AND 0xFFFFFEF3`, complement `0x0000010C` | 1 |
| Capture uses bit 16 | `OR 0x10000` / `AND 0xFFFEFEFF` at four cited sites | 1 |
| The decompiler deletes the loop | Ghidra output for `0036F2C0` contains the `and` and no loop | 1 |
| ~~Two threads exist~~ | **WITHDRAWN 2026-09-07** — all nine thread procedures enumerated and disassembled by `xiionline-13`; **none can be a graphics-command consumer.** The far end of the protocol is unknown. Section 10. | — |

**The scan that found the census was wrong the first time and returned zero**, including on the site
already disassembled by hand. The loop-start was computed by adding the branch displacement to the
instruction end *and* to the branch offset — a double count. **A census that returns zero on its own
positive control is a broken census**, and it was rerun rather than reported.

## 9. Related

- [`Legacy-PS2-GS/`](../Legacy-PS2-GS/) — the GS budget work reaches the same graphics backend from
  the resource side.
- [`Render-Command-List/the-ordered-render-command-list.md`](../Render-Command-List/the-ordered-render-command-list.md)
  — what is *in* the batches this word gates.
- [`../../00-Engine-Core-Runtime/Application-Root/game-application.md`](../../00-Engine-Core-Runtime/Application-Root/game-application.md)
  — the main loop that contains two of the eleven spins.

## 10. Correction 2026-09-07 — the second thread is not established, and a neighbouring fence is inert

**Raised by `xiionline-13` against their own published claim, and it lands on this document's §1.**

### What was claimed

That the batch is handed to a graphics thread which turns it into pixels. **Withdrawn.**

### What refutes it

`xiionline-13` enumerated **every thread this image creates** — 5 `CreateThread` and 4
`_beginthreadex` sites, each disassembled for the `lea` supplying its start routine, largest
procedure 555 bytes — and **none of the nine could be a consumer of the graphics command stream.**

> *Count refined 2026-09-16 (FABLE), reproduced independently from the IAT slots `008C21C8` and `008C2D70`:* the site count is right - **5 + 4 = 9 call sites** - but they supply **eight distinct procedures, not nine**. `007A5550` is the start routine at both `007A5232` (in `FUN_007A4D50`) and `007B6FE4` (in `FUN_007B6F70`). The eight are `00171370 thread_decoding_proc`, `005CCAB0`, `005CCBA0`, `007A5550`, `007A5E50`, `007DD950`, `007DEC40` and `00863500`. **The refutation this section rests on is unaffected**; the count is. Their forward direct-call cones are 1 to 57 functions.
The imports name no graphics module beyond stock `d3d11`, `dxgi` and `D3DCOMPILER_47`.

> *Premise corrected 2026-09-12 (FABLE):* "every thread this image creates" counted the imports
> only. The engine's own thread API `008636E0` creates four more — `TkSyncVEmulationThread`,
> `TkBGThread%d`, `TkSyncvThread%d`, `TkPowerOff` (§7, CG-3) — and none of them reaches the handshake
> either, so the refutation holds on thirteen threads rather than nine.

**So the protocol in sections 2–5 stands and its far end does not.** Something accounts for published
batches; this document does not know what, and §1 asserted an answer it had not earned.

### The neighbouring function that looks identical and is inert

Thirty bytes away from the genuine spin sits its opposite:

```asm
0036F2F0  mov  eax, dword ptr [02EAF6D8]   ; the load is OUT HERE
0036F2F6  and  eax, 0x100
0036F300  test eax, eax                    ; <-- the loop starts here
0036F302  jne  0036F300                    ; branches to the TEST, not the load
```

**Nothing inside the loop can change `eax`.** The spin therefore either never runs or never exits,
*regardless of who writes the word* — a non-`volatile` read hoisted out of a spin by the optimiser.
`02EAF6D8` sits past `.data`'s `SizeOfRawData`, so it is zero at image load, and no RIP-relative store
to it exists in `.text`: the loop falls straight through, every time.

Verified here independently by disassembly before accepting it.

> **`0036F2C0` and `0036F2F0` are thirty bytes apart and are opposites.** One re-reads inside the
> loop and is a genuine wait; the other reads once outside and is dead. **Decompiled, both render as
> ordinary spins.**

### Why this document's census is not affected

The scan in section 2 required **two or more RIP-relative loads of one address *inside* the loop
body**. A hoisted spin has one load outside it and therefore **cannot match** — so the eleven sites
reported here are genuine by construction, and `0036F2F0` was correctly not among them.

**That was luck as much as design.** The filter was written to find the idiom, not to exclude its
inert twin, and it happens to do both.

### What this does to `CF-6`

`CF-6` said decompiled threading claims owe a re-derivation. It is stronger than that:

> **A spin loop cannot be verified from decompiled output at all.** Only the **branch target**
> separates a working spin from an inert one, and the branch target is exactly what decompilation
> discards. **There are two failure modes, not one: spins the decompiler deletes, and spins the
> decompiler invents.**

### The method note worth more than the finding

`xiionline-13` named the killer observation *"is `02EAF6D8` written by frame code?"*, censused all 17
sites, found every reference to be a load, and read that as confirming a cross-thread producer.
**For a hoisted read, "all references are loads" is equally consistent with dead code.** The
observation was sound; the inference was not. **Re-attacking the same bodies for their branch
targets rather than their operands is what broke it.**

## Falsification pass 1 — 2026-09-13 (OPUS)

| claim | measured |
|---|---|
| `02EBA3F8` has **24 write-form** and **38 read-form** references | **24 and 38** — the writes are 18 `mov`, 4 `and`, 2 `or`; every read is a `mov` |
| `0036F2C0` is **43 bytes** | **43** |
| `AND 0xFFFFFEF3` clears bits **2, 3, 8** | `~0xFFFFFEF3` = `0x10C` = bits **2, 3, 8** |
| `AND 0xFFFEFEFF` retires the capture bit and the batch bit together | clears bits **8 and 16** |
| the eleven loop sites and their owning functions | **all eleven exact**, at the addresses and in the functions § lists |

### The settle-spin census is exhaustive — and it is eleven, not twelve

The shape § describes can be searched for directly: **two loads of the same rip-relative address into
two *different* registers, a `cmp` of those two registers, and a conditional jump backwards to the
first load.** Run over every body in `functions.tsv`, that search returns **eleven loops, all on
`02EBA3F8`**, and they are precisely the eleven § tabulates — the same addresses, the same owning
functions, nothing extra anywhere in the image.

That is the strong half of §'s claim, confirmed exhaustively rather than sampled: **no other global
in this executable is waited on this way.**

### But the twelfth is not a settle-spin, and the conclusion it carried does not follow

§ offered `0037CE10` in `AddMotion_LoadHighModelReplace` as the same shape on a different global,
*"so the idiom is a house style, not one function's quirk."* Read out:

```asm
0037CE10  mov  rax, qword ptr [rip + 0x2760b29]   ; -> 02ADD940
0037CE17  lea  rdx, [rdx + 4]
0037CE1B  inc  r8d
0037CE1E  mov  dword ptr [rdx + rax - 0x14], ecx
0037CE22  mov  ecx, dword ptr [rbx + 4]
0037CE25  add  rbx, 8
0037CE29  mov  rax, qword ptr [rip + 0x2760b10]   ; -> 02ADD940  (same register)
0037CE30  mov  dword ptr [rdx + rax - 4], ecx
0037CE34  mov  ecx, dword ptr [rbx]
0037CE36  cmp  ecx, -1
0037CE39  jne  0x37ce10
```

Three things rule it out, any one of them sufficient:

- **both loads target `rax`** — the second overwrites the first, so nothing compares them;
- **the `cmp` is `ecx, -1`** — against a sentinel in the *source data*, not against a second read of
  the global;
- **`02ADD940` is loaded as a `qword`** and used as a **base** (`[rdx + rax − 0x14]`), not as a dword
  state word. It is reloaded twice because the compiler did not keep it live across the stores.

This is a **copy loop with a `−1` sentinel**: `rdx` and `rbx` advance, `r8d` counts, two dwords are
written per iteration. The repeated load is a register-allocation artefact, and the resemblance to
the settle-spin is entirely in the two loads of one address — which is the one feature the idiom
shares with ordinary code.

**So the "house style" conclusion loses its only support.** What remains is narrower and more
useful: the settle-until-stable idiom occurs **eleven times, on one word, in graphics submission and
the main loop** — *one protocol's idiom*, not a convention of the codebase. A reconstruction told it
was a house style might reach for it elsewhere; nothing in this image would justify that.

> The near-miss is instructive in the same direction as §10's own method note. **Two loads of the
> same address is the eye-catching half of the pattern and the half that carries no information** —
> what makes a settle-spin is the *comparison of the two results*, and that is exactly what this loop
> does not do.

**Not claimed:** nothing here was executed or observed live, and this pass does not touch §10's
standing correction that the second thread is not established. §§2's per-bit attributions beyond the
two masks, and §§4–7, were not re-derived.

## The second failure mode, censused - 2026-09-18 (FABLE)

Both of `CF-6`'s failure modes now have an image-wide census, so the debt it records is a finite list and not a standing suspicion. *Spins the decompiler deletes* - two loads of one address compared with each other - were searched for over every listed body on 2026-09-13 (OPUS): **eleven, all on `02EBA3F8`**. *Spins the decompiler preserves although they cannot wait* - a backward conditional jump whose whole loop body is `test` / `cmp` / `nop` on registers, so nothing it tests can change - are searched for by [inert_spin_census.py](members/inert_spin_census.py) over 38,161 listed bodies ([inert-spin-census.tsv](members/inert-spin-census.tsv)): **nineteen**. Positive control: the known one in `GraphicsSync_WaitBackendState100ClearAndResetSharedState` is found. Negative control: none of the eleven two-load loops is reported. **Seventeen of the nineteen are the hoisted test of bit 8 of `02EAF6D8`** - which is, independently, exactly the number of references that word has in the image, every one a load: each reference is one dead fence, spread over nine functions (the two batch publishers, the reset, the effect-capture and queue bodies, the VFX fence passes; the TSV lists them). Since the word is zero-initialised and never written, all seventeen fall through on their first pass. **The other two were not known and are of the opposite polarity**: in two main-menu procedures a word is loaded once and the loop is `test eax, eax` / `je` back to the `test` - *wait until non-zero* with the load hoisted out. The words are `02CA8F94` and `02CA96D4`; each has one writer in the image, an eleven-byte function that stores `1`, and that function's only reference is the `lea` that hands it as the completion callback of a load queued once, from the boot init burst `0017D4C0` (the first is the texture `lic_4_c`). So each word is a *loaded* latch, set once and never cleared, and the loop was written as *wait for the load*. As compiled it cannot wait: if the latch is already up it falls through, and if it were still down the loop would never end, whatever thread the completion runs on. That the game does not hang there says only that the load has always finished before a player can open those screens - a latent hang, not an observed one. **What this does to the debt.** A threading claim in this database could be wrong through one of these two decompiler behaviours only if it concerns one of these thirty loops. The eleven are waits on a word whose writers all run on the main thread (`CG-3`, `CG-5`) and which `UQ-211` reads as the folded registers of a PS2 DMA channel - they synchronise nothing in this build; the seventeen are dead; the two are latches polled wrongly. None of the thirty is a working cross-thread wait, so **the sentence that opened this item - read from decompiled output the frame contains no synchronisation through this word - is, for this binary, also what the disassembly says.** The method rule stands as a rule: a spin is verified from its branch target, never from decompiled output. *Limits:* both censuses walk listed function bodies linearly, so code the function list does not contain is not covered; loops that wait through a call (a kernel wait, a sleep) are outside both shapes and are not something a decompiler removes. Static.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Developer — SERVICE.** `0017D6E0` on this page calls `FUN_001c2f50`, owned by that layer. What it reaches is a string-assembling routine over the EASTL allocator at `008F6600`, the globals at `01F8127C` / `01DF6E38` / `01DF6E40` and the static empty buffer `02EBA2E0`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**RNG_Random_Selection — SERVICE.** `0022B6E0` on this page calls `RNG_MT19937_NextU32_Thunk`, owned by that layer. What it reaches is a five-byte thunk - `jmp 00863BF0` - onto the CRT's Mersenne Twister next-u32; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Movement — MECHANICAL (SWE2-CONTRACT 2026-09-15, 10 edges).** `0022B8C0`/`0022BC20`/`002628B0` call `00263560` (3
edges); `0022B8C0` calls `0037CF00`; `0022B0B0` calls `00357780`; `002628B0` calls `0026A1D0`/
`003792D0`/`003791C0`/`003DAA20`/`00379070`. The handshake's frame bodies run on the same tick that
steps movement — cadence adjacency.

**ActorEntity — MECHANICAL (SWE2-CONTRACT 2026-09-15, 9 edges).** All edges route through `002628B0`, which calls
`003DE920`/`00263660`/`0037B230`/`003DDC20`/`ActorSystem_ReleaseManagerRecords`/`002695A0`/`003B6C20`
and is called by `0025BFB0`/`ActorResource_BeginManagerResourceSetLoad`. One shared body, no
handshake semantics.


**Resource — SERVICE (SWE2-EC7 batch-149, 1 edge).** `00427320`, the dispatch the `00426560` chain-pass entry cites, resolves its table row through `002ED570` (`ResourceTable_ResolveEntryByIndex`) - the handshake borrows the resource layer's lookup; it owns no resource state.

**CoreRuntimeScheduling — SERVICE.** The op-append machinery this page's `0018CA50` entry names (`0085E730`/`001F1DF0`/`001AB570`/`0018B4E0`/`0018AFF0`) sits inside the core-runtime call neighbourhood: `0017CCD0` reaches `0017D6E0`, which fans out to `001A1460`/`001DB600` and siblings - shared callee plumbing across the scheduling layer, not a scheduling contract this page owns.

## Interior citation — frontier hub `0036D400` (2026-09-18, SWE2-EC7)

`0036D400` — 979 B, 6 A-measured callers; the packet emit that fills this handshake's command
buffer. Interior verified: 16-byte cursor-advanced records — `[rcx+8]` is the write cursor,
each emit bumps it `+0x10` and stamps `{payload-qword, kind}` pairs (kinds `0x4C`, `0x4E`,
`0x18`, `0x47`, `0x50000` seen in one pass, e.g. [`0036D53B`/`0036D733`](../../_index/ADDRESS-INDEX.md));
the frame's own size dwords are normalised to floats via `cvtdq2ps`/`divss` by the `008Bxxxx`
constants (`0036D45E`–`0036D4E8`); and the tail writes the packet header —
`(count-1) | 1<<0x1C` at [`0036D781`/`0036D786`](../../_index/ADDRESS-INDEX.md) — and trailer
`0x5000000011000000 | count<<32` (`0036D792`–`0036D7A4`) before `003A1DB0` hands off. The
`0x300`/`0xBF0F88` arm selects between two source lanes by the `(ecx!=0)|((edx!=0)<<1)` mode
bits at `0036D42F`–`0036D483`.

## Interior citation — frontier hub `003DE920` (2026-09-18, SWE2-EC7)

`003DE920` — 66 B, 8 callers; the set/clear arm on the shared state byte `02B59350`.
`edx` selects the arm: nonzero calls `0037ACD0` then `bts` ([`003DE938`](../../_index/ADDRESS-INDEX.md)),
zero calls `0037ACA0` then `btr`, both operating on bit `cl` of the same byte
(load `movsx` / store `mov` to `02B59350`). The map-ctrl pack's bit-8 arm
(`0037AA90(lights,0)` + this) is the handshake-side flag the graphics pass reads.

## SWE2-EC7-24 update (2026-09-18) — `0037B230` channel-record reset

`0037B230` (84 B) bounds-checks `ecx <= 4` and zeroes one `0x50`-byte channel
record at `02EBF420 + ecx*0x50` — eight qwords cleared then `+0x40/+0x44/+0x48`
set to `1.0f` and `byte[+0x4C]` zeroed, the scale-triple default. Interior
anchor `0037B24C` (the first store).

## SWE2-EC7-36 update (2026-09-19) - `008621E0`

`008621E0` (674 B) is a command-state word body - `008C2E00`-`008C2F00` rdata run, `00861EC0`/`008629C0` pairs plus `00809728`/`00808C40`/`0019C5D0`. Interior anchor `0086222C` (an `00861EC0` call).

## SWE2-EC7-43 update (2026-09-19) - `0035EA40`

`0035EA40` (291 B) is `TkSyncVEmulationThread` - the page's priority-30 thread body: `01CEBD90`/`022CA5F8`-`022CA640` thread-state words, `0016D6A0`/`0017D3E0`/`00369160`/`003691B0`/`005A0820`/`008635F0`/`00863650`/`00863690`. Interior anchor `0035EA5F` (an `0016D6A0` call).

## SWE2-EC7-43 update (2026-09-19) - `008636E0`

`008636E0` (276 B) is the engine thread-create API - `"UnknownThread"` literal, `01CCFA88`/`01CCFA98`/`02EB37B8`, `0016D6A0`/`001A5760`/`001AE550`/`00210EC0`/`00863430`. Interior anchor `00863703` (an `0016D6A0` call).

## SWE2-EC7-45 update (2026-09-19) - `0022BEB0`

`0022BEB0` (238 B) is the `VFXSystem_RenderLayerPass` root - `0017F2F0`/`0017F370`/`00181AB0`/`00181C10`/`00181C70`/`00181DD0`/`00181E30`. Interior anchor `0022BEB4` (an `0017F2F0` call).

## SWE2-EC7-54 update (2026-09-19) - `001AE550`

`001AE550` (347 B) is a shared-command-state body - `001A4BF0`/`001AEC30`/`001EDF00` plus two vcalls, `008F6600`/`02EBA2E0`/`02EBA2E1` and the `"EASTL basic_string"` literal. Interior anchor `001AE5C9` (a `001EDF00` call).

## SWE2-EC7-55 update (2026-09-19) - `001AEC30`

`001AEC30` (282 B) is a shared-command-state body - `0016D6D0`/`0016D840`/`001AE7C0`/`001AEB00`/`001AEF70`. Interior anchor `001AEC67` (a `0016D6D0` call).

## SWE2-EC7-56 update (2026-09-19) - `001AEB00`

`001AEB00` (304 B) is a shared-command-state body - `0016D720`/`0016D840`/`001AE7C0`. Interior anchor `001AEB73` (a `0016D720` call).

## SWE2-EC7-58 update (2026-09-19) - `00862130`

`00862130` (167 B) is a shared-command-state body - `00808C40`/`00861EC0`/`008629C0` plus three vcalls, `008C2B08`/`008C2E00`/`008C2F00`/`00901010`. Interior anchor `0086215B` (a `00861EC0` call).



## SWE2-EC7-65 update (2026-09-19) - `001AE7C0`

`001AE7C0` (137 B) is a shared-command-state body - `001A4BF0`/`001EDF00`. Interior anchor `001AE81D` (a `001EDF00` call).



## SWE2-EC7-65 update (2026-09-19) - `001AEF70`

`001AEF70` (134 B) is a shared-command-state body - `0016D840`/`001AE7C0`. Interior anchor `001AEFB8` (a `001AE7C0` call).


## SWE2-EC7-78 update (2026-09-20) - `00863690` + `00863650` virtual-call wrappers measured

`00863690` (76 B) and `00863650` (61 B) are the `0016D6A0`-gated
virtual-call wrappers the handshake callers run: `0016D6A0(rcx != 0)`
gates; a NULL object returns 0; otherwise `[[rbx]][0]` is called
through the `008C20E0` import slot - `00863690` passes the caller's
`edx`, `00863650` forces `edx = -1`. Both return 1 on the taken arm.
Interior anchors `008636C6` / `0086367C` (the indirect calls).

## SWE2-EC7-93 update (2026-09-20) - `00376D80` + `00376BE0` measured

`00376D80` (649 B) is the eight-slot periodic publish the handshake
callers run: each slot's gate dword at `02CDBExx` admits a four-float
copy - two source floats plus two destinations - with `or word
[flags], 8` marking the slot dirty; eight identical 0x51-byte
repetitions, unrolled.
Interior anchor `00376D99` (the first slot's flag set).

`00376BE0` (408 B) is the eight-iteration 0x90-stride record pass
beside it: `[rbx-0x54]` gates, `and word [rbx], 0xFFF7` clears, the
bit-0 arm computes `1 - [rbx-0x14]*[rbx-0x24]*x` into three published
floats, `003AC900`/`003ABD00` fetch the target record, and the tail
writes `+0x20..+0x28`, `+0x40`/`+0x44`, a `minss`-clamped scaled vec3
at `+0x10..+0x18` with `+0x1C = 1.0f` when `comiss` passes (else
`+7 |= 2`).
Interior anchor `00376CB6` (the `003AC900` call).

## SWE2-EC7-94 update (2026-09-20) - `003323D0` measured

`003323D0` (78 B) is the handshake re-init `0022A770` and
`0022B8C0` call: it installs the `02CD6F4D`/`02CD6F4E` globals,
runs the `004262E0`/`00426560`/`00426090` triple, hands the two
`02CD6Fxx` objects to `0041E340` and `00425E10`, calls `004288E0`,
and tail-calls `00428F80` - the full six-call re-arm the render
side runs when the shared word is rebuilt.
Interior anchor `003323F3` (the `00426090` call).

## SWE2-EC7-95 update (2026-09-20) - `004262E0` + `00314370` measured

`004262E0` (91 B) is the first call the `003323D0` re-init runs
(and `00332660` beside it): after `00370DF0`, it walks the
`0x740`-stride record chain under `02CD6F28` - `[rdx+0x48800]`
seeds the index (`-1` done), bit 2 of `+0x284` gates a `00422A30`
call per record, and `word[+4]` carries the next index until `-1`.
Tail `00370DE0`.
Interior anchor `0042630E` (the `+0x284` flag test).

`00314370` (85 B) is the five-slot publish `0022A770` and
`0022B8C0` run alongside it: `ebx` 0-4 feeds `00263FF0`, and any
slot whose `+0x10` has bit 0 set gets `003DA050` then `003DCFB0`;
`002555D0` runs once after the loop and it tail-calls
`00259820(esi)`.
Interior anchor `0031438D` (the `+0x10` bit-0 test).

## SWE2-EC7-96 update (2026-09-20) - `00370DF0` + `00370DE0` measured

`00370DF0` (15 B) and `00370DE0` (15 B) are the two global installs
`00426090` and `004262E0` bracket the `0x740`-stride walk with: the
first copies the `02CD4A78` qword into `02C0A434`, the second
installs the `005E9EC0` constant address into `02C0A444` - the
open/close pointer pair the walk's callers rely on.
Interior anchors `00370DF7` and `00370DE7` (the two stores).

## SWE2-EC7-106 update (2026-09-20) - `00251E00` + `002512B0` measured

`00251E00` (117 B) is the backing-buffer
resize `0022AF50` and `0022B000` run
on the `020927F0` record: gated on
`word[+0xE4] <= 1`, it computes
`w = (dword[022D8EAC] + 0xFF) >> 8`
and `h = (dword[022D8EB4] + 0xFF) >>
8` (the 256-quantized dimension
reads), then `bytes = w * h * 3 <<
0xE`; when positive,
`0036CAD0([+0xC0], bytes)` reallocates
and the result is stored back to
`[+0xC0]` - the size-following
realloc the record's pixel buffer
tracks the frame dimensions with.
Interior anchor `00251E1C` (the first
`022D8EAC` load).

`002512B0` (2,670 B) is the overlay
composer `0022B8C0` and `0022BC20`
run on the same record - the largest
body in this batch. `byte[+0xE8]` bit
2 vetoes outright; `word[+0xE4] > 3`
or negative exits, `2..3` emits a
single `0x502`-tagged `0x58`-byte
record through `00375900`, and the
`<= 1` arm builds the full set: a
`0x60`-byte header record whose qword
field at `+0x30` is bit-packed with
tag `0x102a00` (or `0x202a00` on the
`float[+0x110] != 1.0` /
`[+0xD8] == 0` arms), x/y indices
resolved through `002D8150` into bits
`0x3C000000` and `0x3C0000000` of the
packed qword, `00182B20` fetches on
the record's `+0xC0`/`+0xC8`/`+0xD0`/
`+0xF8` pointers, `00182B40` lazily
allocates `[+0xD8]` when `float[+0x110]
== 1.0`, and `word[+0xE6]` case 7
scales `byte[+0xCC]`/`[+0xCD]` by
`float[+0x124] * byte[+0x129]` with a
`0x66666667` divide - six
`00375900` submits in all before the
`0x101`-tagged trailer record.
Interior anchor `00251316` (the first
`00861EC0` record clear).

## SWE2-EC7-107 update (2026-09-20) - `00247810` measured

`00247810` (89 B) is the flag-field
byte-pair write `00227EE0`,
`002A6A80` and `0057C480` run: bits
18-20 of `dword[rcx + 0x44]`
(`<< 0xD >> 0x1D`) steer the record's
`+0xAC`/`+0xAD` bytes - when bit 2
is armed the armed low bits write
`0xF9` individually, when clear each
byte becomes `0xF9` or `6` per its
own bit - the two-byte publish the
handshake record carries.
Interior anchor `0024781B` (the
`+0x44` shift-out).

## SWE2-EC7-109 update (2026-09-20) - `00214C30` measured

`00214C30` (898 B) is the
display-state synchronizer
`0022A580` and `0022B0B0` call:
stack-cookie guarded, `ecx` is the
mode (`movsxd rbp`), and the
`01FD3AE0`..`01FD3B14` block is
the shared command state. Mode 0
re-syncs: `001C53B0()` /
`001C53D0()` gate the
`01FD3AE6` latch, `00193D50()` +
`0018D5F0(out, &rec)` produce a
0x14-byte record copied to
`01FD3B00` / `01FD3B04` /
`01FD3B14`; flag bytes
`01FD3AE4` / `AE5` / `AE0` /
`AE1` / `AE2` / `AE3` each arm a
one-shot notify through
`001CC920` / `001CC800` /
`001C61F0` / `001C7290` /
`001C5040`, with float pairs
`01FD3ACC`/`AD0` and
`01FD3AD8`/`ADC` staged into
`01FD3AF4`/`AF8` and
`01FD3B08`/`B0C` when
`dword[01FD3AE8]` is nonzero.
`001EC560()` vetoes the active
paths. A per-slot byte/dword
table at `01EB3AE0` (bounds
`rbp < 2`, `00809728` fail-fast)
drives `0018CA40()` +
`0018CA50` / `0018BC90`
applies.
Interior anchor `00214D72` (the
`01FD3AE5` flag read after the
`001CC920` notify).

Mechanical neighbours introduced by
this section's citations: `001EC560`
(the veto the sync reads) carries a
StoryEvent caller (`001ED240`, 1
edge). That is an edge of the veto,
not of the command state - noted so
the audit accounts for it.

## SWE2-EC7-111 update (2026-09-20) - `00186910` measured

`00186910` (91 B) is the
three-table index select
`00181AB0`, `00181B20` and
`00182A60` run: `dl == 0`
indexes `qword[[+0xC30] * 8
+ 0xB08]`; `dl` nonzero
chooses between two
`[+0xDD0]`-indexed tables -
`[+0xB50]` when
`byte[+0xDBB]` is armed AND
`0017F280()` answers nonzero,
`[+0xB48]` otherwise. The
alternate path needs both
gates, not either.
Interior anchor `00186935`
(the `+0xB50` table read).

## SWE2-EC7-112 update (2026-09-20) - the `0018CA40`/`01F7F538` family measured

`00182250` (34 B) and
`00182220` (44 B) are the
two arms `0022B0B0` /
`0022B8C0` (and `001B2530`,
`001EC060`, `001FBD80` for
the first) run: both fetch the
`0018CA40` object - `00182250`
unconditionally calls
`0018B5D0(obj, 0)`, `00182220`
calls `0018B670(obj, 0)` only
when the object is live - and
both latch
`dword[01F7F538] = 1`. The
flag is written whether or
not the object existed.
Interior anchors `00182263`
and `0018223D` (the
`01F7F538` latches).

`0017F6B0` (103 B) is the
gated notify `0022B0B0` and
`0022B8C0` run: when
`dword[01DF08EC]` is set,
`dword[01F7F4F0]` must also
be set; when `01DF08EC` is
clear, `01F7F4F0`, `01F7F4F4`,
`01F7F4F8` and `01F7F500`
must ALL be zero AND
`001B7D20(001B7F20())` must
answer true. Either path then
needs `0018CA40()` live and
tails `0018C450(obj, 3)` - a
mode-3 poke behind a five-
word state gate.
Interior anchor `0017F6E1`
(the `001B7F20` probe).

`0017F670` (62 B) is the
simpler sibling `00229F20`,
`0022B0B0` and `002F4520`
run: `dword[01DF08E8]` AND
`dword[01F7F4F0]` both set,
plus a live `0018CA40()`,
then `0018C450(obj, ecx)` -
the caller-chosen mode.
Interior anchor `0017F676`
(the `01DF08E8` test).

`0017F2F0` (58 B) is the
two-singleton poke
`0022B0B0` and `0022BEB0`
run: `001BC000()` live clears
`byte[obj + 0x230]`, and
`0018CA40()` live tails
`0018BA20(obj)` - each arm
independent, both optional.
Interior anchor `0017F303`
(the `+0x230` clear).

## SWE2-EC7-113 update (2026-09-21) - `001B7D20` measured

`001B7D20` (8 B) is the
`dword[+4] == 3` kind
predicate `0017F6B0` runs
mid-dispatch (`00180170`,
`001E03F0`, `001EC5A0` run
it too): `cmp`/`sete`/`ret`
and nothing else - one field
of the record answering
whether it carries the kind-3
shape.
Interior anchor `001B7D24`
(the `sete`).

`00863520` (31 B) is the
window-half helper
`00368C10`, `00368C80`,
`00368ED0` and `00369080`
call: `eax = (0x20 - 2*edx)
>> 1` (i.e. `0x10 - edx`),
passed to the IAT import at
`008C21E0` (`01CCC382`) and
zero returned - a 32-slot
budget split against the
incoming count.
Interior anchor `0086352E`
(the `sar`).

## Carried into the S-39 subsystem contract, and what was re-read (OPUS, 2026-09-21)

S-39 now has a contract —
[`CONTRACT-render-command-list-and-graphics-handshake.md`](../CONTRACT-render-command-list-and-graphics-handshake.md),
`scope: subsystem` — and this page is one of its two sources. **Nothing here is corrected.** What
follows is the boundary between what that contract re-derived and what it carries from here, so a
reader of either knows which is which.

**Re-read against the image on 2026-09-21.** The settle-spin itself: `0036F2C0`'s complete 43 bytes,
including that the two loads at `0036F2D0` and `0036F2D6` land in **different registers** (`ecx` and
`eax`) and are compared — the property the whole reading depends on and the one the decompiler
destroys — and the `and dword ptr [02EBA3F8], 0xFFFFFEF3` at `0036F2E0`. The inline copy in
`MainLoop_Draw` was read in context: `0022B2C0`–`0022B2CE` is the same four-instruction shape, and
`0022B2D0` then **calls** `0036F2C0`, which spins again — §2's double wait, confirmed at its most
important site.

**Carried, not re-derived.** The eleven-site census, the thread topology (`CG-3`), the never-written
fence `02EAF6D8` (`CG-4`), the meaning-free bits (`CG-1`, `CG-2`) and the DMA reading of the
publishers (`UQ-211`). Those rest on this page's own instruments and its `audit.passes: 1`, and the
contract cites them as this page's rather than restating them.

**What the contract adds that is not a question about this word.** The other half of S-39 — the
ordered render command list — turned out to hold the subsystem's load-bearing ordering: which of two
lists owns the command objects, the fixed clear-then-destroy pair at both teardown sites, and a
forward-walk early exit that ambient occlusion arms. Those are on
[the list page](../Render-Command-List/the-ordered-render-command-list.md) and in the contract's §4;
none of them touches `02EBA3F8`.

**The one thing this page and the list page do not jointly establish**, and the contract records it
as such: how a walked-and-executed command list becomes the buffer the three publishers kick. §7's
`UQ-211` closes with the same gap from the other end — "how a batch then reaches the renderer" —
and the contract does not paper over it.

`003A31A0` (517 B) is the command-packet emit `0045BAE0` calls: `02F8F2D0`/`02F8F2D8` bound the arena, `align16(rsi+0x40)+0x20` is the cursor check, then the packet is stamped - word 3 at `+0`, `byte[+3]` = 0x10, word 3 at `+0xC`, `byte[+0xF]` = 0x50, word 0x8001 at `+0x10`, qword 0xEE at `+0x18`, `r8d & 0xFFFFFF` arg, `02AEE900`-indexed pointer at `+0x20` - with `0020E620`/`0024E460`/`00861EBA` behind, the state word's packet arm.

Interior anchor `003A32A2` (function `003A31A0`).

`001CC800` (277 B) is the depth-of-field publish `00214C30` runs on its `r9d == 0` arm: `dword[01DFE40C]` must stay <= 4 with `dword[01F832B0 + mode x 4]` positive; three `01F813F8`-indexed `x 0x10` container lookups (`001FF6B0` + `001FF740` name resolve) write `EnableDof` (`cl != 0`) through `00202820` and `mDofFocusDistance`/`mDofApertureFnumber` (the `cvtss2sd`'d `xmm1`/`xmm2` pair) through `002027B0` - the named-property push the handshake's parameter pass issues.

Interior anchor `001CC87A` (function `001CC800`).

`00426560` (238 B) is the 0x740-record chain pass `003323D0` runs: from the head index `022C6F28+0x48800` it follows `+4` links, and a record qualifies when `+0x2AE&1` is clear, `+0x284&0x1000004==4`, `+0x304&1` set, `+0x294&8` clear, and (`+0xC4==-1` or the `004232D0`/`00422D50` pair yields a `+0xC&8`-clear object); a qualified record's `[rbx]` u16 leads to `00427320(next, 0x1001)` and the flag rewrite `+0x294 = (+0x294 & 0xFFFDFA7F) | 0x20`, `+0x304 &= ~1`

Interior anchor `004265EC` (function `00426560`).

`003A20C0` (212 B) is the paired command-record emitter `0036D400` runs over `edx` quad-steps: each iteration pushes TWO `0x10`-byte commands onto `[rcx+0x10]`'s `+8` cursor - `(0x1000-r8d)*8 + (0x1000-edx)*8`-derived packed offsets ORed with `arg<<0x18`-style high halves, `qword[+8] = 4` - the split offset/size command pair issued per `0x40`-block

Interior anchor `003A2159` (function `003A20C0`).

`001C7290` (207 B) is the epoch reset `00214C30` runs: it `01CCEB62`-memmoves the `[01F81338..01F81340]` cursor span back to base (adding the shift to `01F81340`), clears `01F81284`/`01F81410`/`01F81414`/`01F81415`, wraps `01F813F8` mod `0x80000001` into `01DF6E4C`, `00202880`-resets the four sub-records `01F813A8`..`+0x40`, then tail-jumps `001C7940` - the per-epoch rollback of the shared command buffer

Interior anchor `001C7313` (function `001C7290`).

`0018CA50` (177 B) is the op-record append `00214C30` runs on the shared command list: `0085E730(0x28)` allocates the node, `001F1DF0` initialises it from the `(dl, xmm2, xmm3)` payload, the node pushes onto the `[rcx+8]`/`[rcx+0x10]` vector (`001AB570` when it must grow), and `0018B4E0`'s owner receives it through the `0018AFF0` tail

Interior anchor `0018CAA3` (function `0018CA50`).
