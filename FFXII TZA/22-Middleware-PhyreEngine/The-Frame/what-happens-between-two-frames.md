---
system: The frame — from the Phyre tick to the displayed image
category: 22-Middleware-PhyreEngine
status: AUDITED
owner_layer: CodeDomain:Phyre boundary + PrimaryOwner:CoreRuntimeScheduling — the join is the subject
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-07
audit:
  passes: 1
  last_pass: 2026-09-12
  last_pass_state: opus-what-happens-between-two-frames-pass-1
  crossref_clean: true
  reopened_count: 1
---

# The frame — from the Phyre tick to the displayed image

> What actually happens between one picture on your screen and the next: which of seven frame
> modes is running, which passes it draws, and where PhyreEngine's authority stops and a
> **PlayStation 2 Graphics Synthesizer command stream** takes over.

## 1. What the player sees

Sixty times a second the game reads your controller, moves the world on a little, and paints a
new picture. That much is obvious. What is not obvious is that **the game is not always doing
the same thing** — it runs one of seven distinct kinds of frame, and it switches between them at
moments you can feel.

Walking around Dalmasca Estersand, you are in the **field frame**. It reads the pad, draws the
world, updates the camera, and — if you are holding the speed-up — runs the world forward
*twice more* before drawing. That is why fast-forward makes Vaan sprint but does not make the
picture smoother: the extra work is simulation, not extra pictures.

Press Start. The game does not simply open a menu. It runs **one special frame whose entire job
is to photograph the screen**, and only then switches to the **menu frame**, which is a
completely separate loop with its own update and its own draw. That photograph is why the world
behind the Gambit and License Board screens sits there frozen and slightly soft — you are
looking at a still, not at a paused world. Close the menu and the game hands control back to the
field frame.

The picture itself is built in layers, and the engine names them in its own code: the world, an
ambient-occlusion pass that darkens creases and contact points, a water pass, post-processing,
a PlayStation-2-style depth-of-field blur, a Gaussian blur, and the visual effects that sit on
top. Each layer can be switched off independently, and the switches are a single row of bits.

And underneath all of it is the thing that explains the rest of this document: **the PC game
still draws by writing PlayStation 2 graphics hardware commands.** It builds a list of
instructions in exactly the format the PS2's graphics chip ate in 2006, in a buffer it then
publishes for something else to consume. The engine's own labels for its frame phases still say
`[PS2]main loop draw`. This is not a metaphor or a leftover comment — it is the live drawing path
of the shipping game.

The code around that buffer is shaped like a handshake with a second thread — a wait, a publish,
a "backend busy" flag. **In the shipping build that handshake does nothing**, for a reason
§2.4 sets out exactly. Where the commands are actually consumed is the largest thing this
document does not know.

## 2. Native mechanism

### 2.1 Where the frame starts: the Phyre slot the game fills

FFXII **is** a PhyreEngine application — `GameApplication` derives from
`Phyre::PFramework::PApplication` and overrides 18 of its 31 virtual slots (established in
[the-game-is-a-phyre-application.md](../Application-Framework-Boundary/the-game-is-a-phyre-application.md)).
Slot 4 is the frame tick. That document stops at the slot. This one continues from it.

```
Phyre::PFramework::PApplication   (framework drives)
  -> GameApplication slot 4       0017CCD0   237 B   the frame tick
     -> 0017D6E0                  404 B              tick -> frame adapter
        -> 0022A490               30 B               frame entry
           -> 0022A580            465 B              THE FRAME-MODE DISPATCH
              -> one of seven mode bodies
```

`0022A490` is trivially small and does two things: it stores its second argument into the
frame-argument global `02064AA0`, calls the dispatcher, and bumps a counter at `02064AD0` when
the dispatcher returns non-zero. It is the seam where a Phyre-driven callback becomes a
game-owned frame.

### 2.2 The seven frame modes

`0022A580` is where a frame *decides what kind of frame it is*. It is not a state machine with
transitions declared anywhere — it is a `switch` on one byte, `02064AD3`, and the mode bodies
change that byte themselves when they want the next frame to be different.

Before the switch, the dispatcher does the fixed per-frame work every mode needs, and computes
two booleans from the current mode that decide whether the input subsystem is pumped this frame:

```c
mode = *(u8*)0x02064AD3;

// bVar1 - "this mode suppresses the pre-switch input pump"
if ((mode - 4u & 0xFFFFFFFD) == 0) {        // true for mode 4 and mode 6
    DAT_01FD4A68 = 1;  DAT_01FD4A84 = 0;    // pumpInput = false
} else {
    DAT_01FD4A68 = 0;
    if (((mode - 2u & 0xFFFFFFFC) != 0) || (mode == 4))
         DAT_01FD4A84 = 0;                  // modes 0, 1, 6 -> false
    else DAT_01FD4A84 = 1;                  // modes 2, 3, 5 -> true
}
DAT_02064AD8 = (DAT_02064AD8 == 0);         // per-frame parity flip
```

`(mode - 4) & 0xFFFFFFFD == 0` is true for exactly `mode == 4` and `mode == 6` — the two
**transition** modes. `(mode - 2) & 0xFFFFFFFC == 0` is true for modes 2, 3, 4 and 5; mode 4 is
then excluded by name. So the modes that pump input are exactly the three *interactive* ones.

| mode | body | size | engine's own section labels | what it is |
|---:|---|---:|---|---|
| 0 | `0022B6E0` | 255 B | — | early boot; hands to mode 1 when `0032E520(1) == 0 && *(u8*)0x0209273C == 5` |
| 1 | `0022B7E0` | 219 B | — | second boot stage; hands to mode 2 |
| 2 | `0022A770` | 2001 B | `[PS2]main loop all`, `[PS2]process controller` / `PAD CONTROL`, `[PS2]draw` / `DRAW`, `[PS2]process camera` / `CAMERA`, `OTHER`, `[PS2]fast mode` / `FAST MODE`, `CAMERA`, `OTHER`, `VFX` | **the field/battle frame** |
| 3 | `0022B8C0` | 856 B | `PAD CONTROL`, `UI VFX`, `ATEL CONTROL`, `SOUND`, `OTHER`, `VFX`, `CLOSE FULLMENU` | **the full-menu frame** |
| 4 | `0022AF50` | 174 B | `SCREEN CAPTURE` | one-shot: capture the screen, then set mode 3 |
| 5 | `0022BC20` | 463 B | `PAD CONTROL`, `CAPTURE DRAW`, `ATEL CONTROL`, `SOUND`, `OTHER`, `VFX` | a second capture-backed interactive mode |
| 6 | `0022B000` | 163 B | — | one-shot: draw once, then set mode 5 |

The transitions are written in the mode bodies, as literal stores:

```c
0022AF50 (mode 4) : ... MainLoop_Draw(0, 1); ...            *(u8*)0x02064AD3 = 3;
0022B000 (mode 6) : ... FUN_0036D400(1); ...                *(u8*)0x02064AD3 = 5;
0022B6E0 (mode 0) : if (0032E520(1) == 0 && *(u8*)0x0209273C == 5)  *(u8*)0x02064AD3 = 1;
0022B7E0 (mode 1) : if (0032E520(1) == 0 && 0037C2E0() == 0)        *(u8*)0x02064AD3 = 2;
0022B8C0 (mode 3) : if (002E05C0() == 0) { /* "CLOSE FULLMENU" */   *(u8*)0x02064AD3 = 2; ... }
```

**The mode is also written from outside the bodies (read 2026-09-13).** Every RIP reference to `02064AD3` was
listed: besides the five body stores above and the boot initialiser's `= 0` (`0022A1A0` in `0022A0B0`), the byte has a
one-instruction setter `00229F00` and a sign-extending getter `00229EA0` (26 raw call sites). The setter's callers are
`002E09A0` — the router's input-mailbox drain in the world tick's tail — which sets **4** (`002E0D39`) after ORing
`0x100203` into `0215F1DC`, and `002E2240(flag)`, which sets **6** when `flag` is non-zero (`002E2257`, also ORing
`0x100203`) and **2** otherwise (`002E2274`, clearing those bits). So the menu is opened by a mailbox request
(mode 4), a capture-backed screen by `002E2240(1)` (mode 6), and `002E2240(0)` returns to the field frame.

**Mode 4 → 3 is the menu opening and mode 3 → 2 is the menu closing.** Mode 4's only section
label is `SCREEN CAPTURE` and its only draw is `MainLoop_Draw(0, 1)` with the alternate path
selected — that is the still image the menu is drawn over.

### 2.3 The frame's own section labels, and why they look like CFG noise

Each phase boundary in a mode body compiles to:

```asm
lea  rcx, [rip + disp]        ; -> an ASCII label in .rdata
call 0016D6A0                 ; a 3-byte function whose whole body is `ret`
```

These are **retail-stubbed profile markers**: in the shipping build the marker function was
reduced to a bare `ret`, and the linker then folded that stub together with the CFG guard
`__guard_check_icall`, which is also a bare `ret`. Ghidra names the surviving address
`_guard_check_icall`, so the decompiler renders every frame-phase label as
`_guard_check_icall("PAD CONTROL")` — which reads like disassembly noise and is in fact **the
engine telling you the name of the phase you are looking at**.

This is a concrete instance of open question **BA-1** (2,611 linker-folded addresses) doing
real damage: the folding does not merely cost a name, it disguises live authored data as
compiler plumbing.

Two marker families run in parallel in mode 2. The `[PS2]` family is the PlayStation 2 heritage
scope name; the bare uppercase family is the PC profiler section. They arrive in pairs —
`[PS2]process controller` then `PAD CONTROL`, `[PS2]draw` then `DRAW`, `[PS2]process camera`
then `CAMERA`, `[PS2]fast mode` then `FAST MODE`.

**`CAMERA` and `OTHER` appear twice in mode 2, before and after `FAST MODE`.** That is the
speed-up: the fast-forward phase re-runs the camera and the residual update work, so holding the
speed-up button costs extra *simulation*, not extra drawing.

### 2.4 The graphics handshake, and why it does nothing

The code here is shaped like a rendezvous with a graphics backend: two separate 32-bit words,
both using bit `0x100`, one polled and one published.

| word | address | written by game code? | apparent role |
|---|---|---|---|
| the backend fence | `02EAF6D8` | **never** | "backend busy"; the frame polls it |
| the shared sync word | `02EBA3F8` | yes | the frame's own command-stream state |

**All 17 references to `02EAF6D8` in `.text` are loads. Not one is a store.**

That looked like confirmation — the frame only polls, so the writer must be another thread. It is
not. Disassembling all 17 shows every one of them compiled to the *same* shape, and the shape is
the point:

```asm
0036F2F0  mov  eax, dword ptr [02EAF6D8]   ; the load is HERE
0036F2F6  and  eax, 0x100
0036F2FB  nop  dword ptr [rax + rax]
0036F300  test eax, eax                    ; <-- the loop starts HERE
0036F302  jne  0036F300                    ; and branches back to the TEST, not the load
```

**The load is outside the loop.** `eax` is read once, masked once, and the loop then spins on a
register that nothing inside it can change. So the wait has exactly two possible behaviours: if
bit `0x100` happened to be set at the moment of the load, the process hangs forever; if it was
clear, the loop is never entered at all. **It cannot wait**, no matter who writes the word.

This is a non-volatile read hoisted out of a spin loop — the compiler was entitled to do it
because the global carries no `volatile`, and the intended synchronisation did not survive
optimisation. It is not a one-off: **all 17 sites are hoisted**, at `0024D40A`, `0024D47E`,
`00259045`, `002590CA`, `00259113`, `0036F2F0`, `00374C3F`, `00374C7E`, `00374CBE`, `00375528`,
`0037559F`, `00375648`, `0037613F`, `0037617E`, `003761BE`, `003A2DAE` and `003A2ED6`.

Three further facts say the loop is in the never-entered case rather than the hang case, which is
also what shipping and playable requires: `02EAF6D8` lies past `.data`'s raw size and is therefore
**zero at load**; **no RIP-relative store to it exists anywhere in `.text`**; and none of the
image's **nine** thread procedures is a plausible consumer of a graphics command stream (the
largest is 555 B, and the enumeration is complete — five `CreateThread` and four `_beginthreadex`
sites, no others). The imports name no graphics module beyond stock `d3d11.dll`, `dxgi.dll` and
`D3DCOMPILER_47.dll`.

So the honest statement is: **the producer side is real and complete, and the consumer is not in
this executable's frame path.** Something drains these buffers — the game renders — but this
document has not found it, the fence that would have pointed at it is inert, and no thread here
is it. That is `PROPOSED-xiionline-13-1`, and §8 records the reading this replaced.

The rest of `0036F2F0`, after the loop that never runs:

```c
// 0036F2F0, complete body, once the (inert) wait falls through
*(u32*)0x02EBA3F8 = (u32)0x022D9B50;               // reset the command-stream state block
*(u32*)0x02EBA3F8 = 0x0007FFF0;
*(u32*)0x02EBA3F8 = 0;
*(u32*)0x02EBA3F8 = (u32)0x022D9B50;
*(u32*)0x02EBA3F8 = (u32)0x022D9B50;
*(u32*)0x02EBA3F8 = (*(u32*)0x02EBA3F8 & ~4u) | 8u;
*(u32*)0x02EBA3F8 &= 0xFFFFFFCF;                   // clear bits 4 and 5
*(u32*)0x02EBA3F8 = 0x0000014D;
*(u32*)0x02EBA3F8 = 0;
```

Every one of those nine stores targets the **same** address — verified in raw bytes, not from
the decompiler. See §8 for why that matters and what remains unproven about it.

The closing half is `0036F2C0`. **The word it guards, `02EBA3F8`, is owned by
[the-shared-command-state-word.md](../../17-Presentation-Rendering/Graphics-Thread-Handshake/the-shared-command-state-word.md)**
— that document is the reference for the word, its bit meanings and its 62 references; this one
covers only how the frame uses it. Its complete 43-byte body is **not** what the decompiler
shows:

```asm
0036F2C0  nop / nop / nop                     ; 16 bytes of loop-entry alignment
0036F2D0  mov  ecx, dword ptr [02EBA3F8]
0036F2D6  mov  eax, dword ptr [02EBA3F8]
0036F2DC  cmp  ecx, eax
0036F2DE  jne  0036F2D0                       ; spin until two successive reads agree
0036F2E0  and  dword ptr [02EBA3F8], 0xFFFFFEF3   ; clear bits 0x004 | 0x008 | 0x100
0036F2EA  ret
```

The spin is a **settle read**: loop until the word is stable across two consecutive loads, then
do the read-modify-write. **Unlike the fence wait above, this one is genuine** — the branch target
`0036F2D0` is the first load, so both loads are re-executed each iteration and the loop can
observe a change. Whether it ever *does* is a different question: absent a concurrent writer two
successive loads always agree and the loop exits on its first pass. It is correct code guarding
against a writer this document has not found. The same eleven-instruction idiom is inlined at the
top of every mode body — `0022A850`, `0022AE50`, `0022AFA0`, `0022B040`, `0022B2C0`, `0022B720`, `0022B820`,
`0022BAD0`, `0022BD20` — and once more at `00262AE0`.

**Ghidra's decompiler deletes every one of them.** It treats the global as non-volatile,
common-subexpression-eliminates the two loads into one, proves `cmp ecx, ecx` always equal, and
removes the loop as unreachable. Read from the decompiler alone, `0036F2C0` is a one-line bit
clear and the frame bodies contain no synchronisation at all. See `COVERAGE.md` notes in the
inbox report.

### 2.5 What the frame actually produces: a PS2 GIF command stream

The frame does not call Direct3D. It **fills a buffer of 16-byte records** and flips it.

```c
// 003A1D50 - RenderCommand_InitializeDoubleBuffers, complete body
FUN_004FE3C0(&buffer0);                       // 02EBEFC0
FUN_004FE3C0(&buffer1);                       // 02EBEFD8
*(u32*)0x02EBEFF0 = 0;                        // current index
ConfigureBackingRange(&buffer0, 0x200, 0x000);
ConfigureBackingRange(&buffer1, 0x200, 0x200);
```

**512 records each, 16 bytes per record**, carved out of one arena whose base is `01FD4A78`:

```c
// 004FE420 - RenderCommandBuffer_ConfigureBackingRange, complete body
if (buffer->bInitialized == 0) FUN_003EC8A0();
buffer->bInitialized          = 1;
buffer->pBegin = buffer->pWrite = NULL;
buffer->nCapacity16ByteUnits  = 0;
if (capacity != 0) {
    p = (record*)(*(char**)0x01FD4A78 + (i64)base_unit_offset * 0x10);
    buffer->pBegin = p;
    if ((u64)((i64)base_unit_offset << 5) > 0x80000)  *(u32*)0 = 0;   // deliberate crash
    buffer->pWrite = p;
    buffer->nCapacity16ByteUnits = capacity;
}
```

Emitting one record is three instructions, and it appears inline hundreds of times:

```c
p = buf->pWrite;
buf->pWrite = p + 2;      // +0x10 bytes
p[0] = <64-bit data>;
p[1] = <64-bit register id>;
```

**That is the PlayStation 2 GIF PACKED A+D record: a 64-bit data word followed by the 64-bit
number of the Graphics Synthesizer register it is destined for.** The claim is not made from
the shape alone — see §4.1, where the GIFtag constant independently says `REGS = 0xE` (A+D) and
`NREG = 1`, and §4.2, where the register numbers and their bit layouts are recovered from the
arithmetic that builds them.

Flipping the buffer is `003A1DB0`:

```c
// 003A1DB0 - complete body
old = *(u32*)0x02EBEFF0;
*(u32*)0x02EBEFF0 = 1 - old;                     // flip
new = *(u32*)0x02EBEFF0;
PublishCompletedBatchState100(buf[old].pBegin,
                              (int)((buf[old].pWrite - buf[old].pBegin) >> 4));
buf[new].pWrite = buf[new].pBegin;               // reset the far buffer's cursor
return &buf[new];
```

and publishing it is `0036F360`:

```c
// 0036F360 - the terminator and the publish
if (count == 0) return;                          // nothing to publish
end = (char*)begin + count * 0x10;
if ((*(u32*)(end - 0x10) & 0x70000000) == 0x30000000) {   // last record is an open subpacket
    term = (count < 0x200) ? end : end - 0x10;   // room to append? else overwrite the last
    if (count < 0x200) count++;
    *(u64*)term       = 0x10000000;              // terminator record
    *(u64*)(term + 8) = 0;
}
...
*(u32*)0x02EBA3F8 = 0x100;                       // <- publish: bit 8 of the shared sync word
```

**`0x200` in the terminator logic is the same 512 as the buffer capacity.** When the buffer is
full there is no room to append a terminator, so the last record is sacrificed instead. Two
independently-read functions agreeing on the same constant for the same reason is the strongest
corroboration in this document.

### 2.6 The pass list, and the switch that turns each pass off

`MainLoop_Draw` (`0022B0B0`, 1583 B) is the render pass list. Every pass is guarded by one bit
of a single table, and every pass is bracketed by a named GPU debug scope.

The scope pair is `001EB150` (push) and `001EB110` (pop):

```c
// 001EB150 - push a named scope
if (name != NULL && GetRenderCommandList() != NULL
    && *(void**)0x01F7F4E0 != NULL && *(char*)(*(char**)0x01F7F4E0 + 8) != 0)
        FUN_0018C160(GetRenderCommandList(), name);      // 0018C160, 150 B
```

`GetRenderCommandList` is `0018CA40`, an 8-byte function returning the singleton at `01F7F5E8`.
That singleton is **not a GPU device** — it is a command list; see
[the-ordered-render-command-list.md](../../17-Presentation-Rendering/Render-Command-List/the-ordered-render-command-list.md), and §8 for the reading this replaced.
`0018C160` allocates a `RazorMarkerPushObj` and appends it. The whole marker system is gated on a
debug object at `01F7F4E0` with an enable byte at `+8`, so in a retail run with that byte clear
the names cost two loads and a branch — and no command object is created at all.

The passes, in the order `MainLoop_Draw` runs them:

```
                             "mainLoopDraw"          <- outer scope
  bit 8   command-buffer flush block (submit / wait / resume)
  bit 4   VFXSystem_RenderLayerPass(1)
  bit 0   0036FBB0, 0036F430
  bit 4   EffectSystem_ProcessQueuedGraphicsEffectsForPass(2), VFXSystem_RenderLayerPass(2)
  bit 6   00332420(1)
  bit 1   0017F2F0, 0017F070, 00332420(2)
                             "mask border 0"
                             "AO render"             <- only if 0017FE10() != 0
  bit 4   VFXSystem_RenderLayerPass(3), EffectSystem_...ForPass(3)
                             "Water effect"          <- only if 0017FE20() != 0
  bit 0   0036F450
                             "post-processing render"
  bit 2   VFXSystem_RenderLayerPass(4)
                             "PS2 DOF"
  bit 4   VFXSystem_RenderLayerPass(5), EffectSystem_...ForPass(5)
                             "Gaussian Filter"
  bit 3   00252A70  (or 00251010 on the alternate path)
                             "mask border 2"
  bit 4   EffectSystem_...ForPass(6), VFXSystem_RenderLayerPass(6)
```

`"post-processing render"` is emitted from one of **two** places in the body, selected by
`00180040()`, and both are additionally gated on `02064ADC != 0 && 02064AE0 == 0` and on the
widescreen/aspect flags in `020926E4`. `02064AE0` is set to 1 immediately after, so **the
post-processing pass runs at most once per draw** whichever site fires.

### 2.7 The queued-effect kinds `00375500` dispatches (SWE2-FRONTIER, switch-families package)

`EffectSystem_ProcessQueuedGraphicsEffectsForPass` (374 B) walks the 0x70-stride queue at
`02EBF9E0`: an entry is live when `[+0x68]` is nonzero, its class byte `[+2]` indexes the
enable table at `02EC07E0`, the low nibble of `[+1]` must equal the pass argument, and
`[+0x10] bit 0` must be clear (`00375560`–`003755B4`). The kind byte `[+0]` minus one is
bounded ≤ `0xC` and dispatched through the RVA table `00375678` (site `003755C0`); the body
spin-waits on `02EAF6D8 bit 0x100` (`00375528`–`00375535`, the graphics-thread handshake)
before the walk **and again per entry at `0037559F`–`003755B2`**, and each dispatched kind's
return is tested at `0037562F` — `jne 0037563D` skips the shared `00375470` epilogue when the
handler returns nonzero (pass-gate mismatch), `dec edi`/`inc edi` then drives the loop tail;
`0039D570`/`0039D3F0` run once before the walk.

| kind | arm | handler | role |
|---|---|---|---|
| 1 | `003755CD` | `003740B0` (454 B) | gated on `00254A70()` (the post-result state predicate) and word `020926E4 bit 0x800`; compares `002EF9F0(3)` against `[+0x68]`; calls `003583F0(1)` |
| 2 | `003755D7` | `003745C0` (868 B) | pass gate `+0x1D` vs `00358320()`; builds the `02AE96xx` draw-state block (~40 fields: quad `02AE9680`–`02AE96CC`, ptrs `02AE96E0`/`96F0`/`9700`/`9710`/`9720`, callback `004758E0` — interior verified 2026-09-17 (SWE2-FRONTIER): `005375F0`/`005376D0` head at [`00475C12`](../../_index/ADDRESS-INDEX.md), `0022CC20` ×2 + `004753B0` — same processor-trio profile as `00478280`, name base `01EFAC20`; `004753B0` itself is a 1,322-B processor battery — `0022CC20`/`0022CC40`/`0022CC30` ×6/×2/×2 over the `008F3134` constant at [`004753B4`](../../_index/ADDRESS-INDEX.md)) |
| 3 | `003755E1` | `003749F0` | `EffectCapture_ProcessCaptureDraw` |
| 4 | `003755EB` | `00375B90` (500 B) | pass gate `+0x1D`; iterates the `02EBEFC0`/`02EBEFF0` list |
| 5 | `003755FF` | `00375D90` (299 B) | pass gate `+0x1F`; builds the `02AE95xx` block, callback `00478280` — interior verified 2026-09-17 (SWE2-FRONTIER): 3,925 B of `0022CC20` ×8 + `0022CC40`/`0022CC30` ×2 processor calls over `005375F0`/`005376D0`/`004ECB70` ×3, first call at [`004784A0`](../../_index/ADDRESS-INDEX.md) |
| 6 | `003755F5` | `00374280` (823 B) | pass gate `+0x1D`; same `02AE96xx` block family as kind 2, different fields |
| 7 | `00375609` | `00374E30` (411 B) | pass gate `+0x1E`; builds the `02AE8Bxx`/`02AE8Cxx` block, callback `00479650` — interior verified 2026-09-17 (SWE2-FRONTIER): `0022CC20` ×7 + `0022CC40`/`0022CC30` ×6 each over `005375F0`/`005376D0` ×2 + `00479370`, first call at [`00479873`](../../_index/ADDRESS-INDEX.md) |
| 8–10 | `0037563D` | inline | skip — kinds 8/9/10 fall through to the loop tail |
| 11 | `00375613` | `00376220` (243 B) | pass gate `+0x1F`, edi = `0x200` buffer class |
| 12 | `0037561D` | `00376050` | `EffectCapture_ProcessSecondaryCaptureDraw` |
| 13 | `00375627` | `00375280` (496 B) | pass gate `+0x1D`; `02AE9A50` block, callback `0047A9C0` — interior verified 2026-09-17 (SWE2-FRONTIER): `005375F0`/`005376D0` head at [`0047ABEF`](../../_index/ADDRESS-INDEX.md), `0022CC20` + `004753B0` — same profile as `004758E0` |

The shared idiom — `00358320()` returns the current pass id; each handler compares the
record's `+0x1D`/`+0x1E`/`+0x1F` byte against it and returns 1 on mismatch — makes the byte a
**per-record pass assignment**: a match builds the kind's `02AE8xxx`–`02AE9xxx` state block
(or runs the capture draw) for this pass.

### 2.8 The `0022B0B0` exclusive subtree — the draw call's 45 helpers

The exclusive-callee census assigns 45 frontier functions to `MainLoop_Draw`. All were
signature-swept 2026-09-15 (`bshape.py`); they cluster as follows:

| cluster | members | role |
|---|---|---|
| scope/emit wrappers | `0017F070`, `0017F270`, `0017F720`, `0017FE20` (`01F7F504`), `001809E0`, `00182390`, `00182410`, `00182730`, `00183030`, `00183120`, `00184900`, `001863E0`, `001863F0` | 7–150 B thunks over `0018CA40` (the command-list singleton), `00189120`, `001A9930`, `001EB150`/`001EB110` — the marker and emit vocabulary §2 already names |
| four-sibling pass arms | `0018BD30`, `0018C580`, `0018C860`, `0018CB30` | identical 143–150 B shape: `0085E730` + one `001F1xxx` variant + `001AB570` + `0018B4E0` — four passes that differ only in their `001F1xxx` step |
| `022C7F90` flag accessors | `003582A0`, `003582C0`, `003582E0`, `00358300`, `00358380`, `003583B0` | six 18–21 B **getters** — bit-extracts over the `022C7F90` 4-byte records, no setter among them (AUDIT-SEM rev 8710) — siblings of the `022C7F92` family in the `0022A770` subtree |
| char-render record helpers | `00332420` (`022C6F28`/`022C6F30`), `00332440` (200 B — `001EB150` ×5 scopes around `00426500`/`0041E4D0`/`00425DC0`/`00428E40`/`004264A0`, table `00D10A18`–`00D10AA8`), `00426340`, `00426420`, `00426500`, `00428E40` | per-record draw steps over the `022C6F28` character-render array, each wrapped in a named scope |
| `02B405xx`/`02AD9B60` bank readers | `003B4E50` (378 B — `02B40508`–`02B40514` byte bank + `022C6F28`), `003B6B80` (`02B40528`), `0036FBB0` (268 B — `003B4E50`/`003B5340`, `02AD9B60`), `003B5980` (629 B — `01EF93F0`/`022D91C0` pose banks + `022C6F28`), `0036F410`/`0036F430` | draw-state reads the passes consult; `003B5980` is the pose-bank consumer inside the draw list |
| draw setup | `00229F20` (110 B — `001EB150`/`001826E0`/`0017F670`/`0017F330`/`00180A30`/`001EB110`/`0017ECF0` over `00908BB8`/`C8`), `00251010` (665 B — `0208F570`/`020927F0`/`022D8EAC` + alloc pair `0036C1D0`/`0036C140`), `0026E1A0` (`0209A370`–`0209A3C0`) | the frame's submit/setup arms |
| leaves | `001A5A70`, `001AA2C0` (`008C5F6C`/`01CEBBA8`/`01DFE0B4`), `001F1980`/`001F1E50` (the pass arms' `001F1xxx` steps — `00212CC0` + `00903350`/`00903370` consts), `003769E0` (`020926C0`), `003ACA60`, `003ACA70` | seven 7–228 B call-free or single-global bodies |

The pattern matches §2's description: every pass arm is scope-bracketed (`001EB150` push /
`001EB110` pop) and gated by a flag word; the helpers supply the emit, record-fetch and
bank-read vocabulary between the scopes.

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `0017CCD0` | `GameApplication` slot 4 | 237 B | the Phyre frame tick the game overrides |
| `0017D6E0` | tick → frame adapter | 404 B | sole caller of the frame entry |
| `0022A490` | frame entry | 30 B | stores the frame argument, calls the dispatcher |
| `0022A580` | **frame-mode dispatch** | 465 B | the `switch` on `02064AD3` |
| `0022B6E0` | mode 0 body | 255 B | early boot; sets mode 1 |
| `0022B7E0` | mode 1 body | 219 B | second boot stage; sets mode 2 |
| `0022A770` | mode 2 body — **the field frame** | 2001 B | pad, draw, camera, fast mode, VFX |
| `0022B8C0` | mode 3 body — **the full menu** | 856 B | `MainLoop_UpdateAndRenderFrame`; sets mode 2 to close |
| `0022AF50` | mode 4 body — **screen capture** | 174 B | one draw, then sets mode 3 |
| `0022BC20` | mode 5 body | 463 B | capture-backed interactive mode |
| `0022B000` | mode 6 body | 163 B | one-shot; sets mode 5 |
| `0022B0B0` | `MainLoop_Draw` | 1583 B | **the render pass list** |
| `0036F2F0` | frame-open backend wait — **inert** | 105 B | loads `02EAF6D8` outside its own loop; resets the state block |
| `0036F2C0` | settle-read then clear | 43 B | spin until stable, clear `0x10C`; **decompiler drops the spin** |
| `0036F360` | publish completed batch | 150 B | terminator record, then `02EBA3F8 = 0x100` |
| `003A1DB0` | submit current buffer and flip | 84 B | the double-buffer flip |
| `003A1D50` | initialise the two buffers | 82 B | 512 records each |
| `003A1E10` | reconfigure both ranges | 62 B | capacity and base offset |
| `004FE420` | configure one backing range | 120 B | carves from the arena at `01FD4A78` |
| `003A2090` | begin subpacket | 39 B | writes the GIFtag, masks `NLOOP` to zero |
| `003A2020` | finalise subpacket | 102 B | back-patches `NLOOP` from the record count |
| `005044B0` | current write buffer | 22 B | `&buffer[index]` |
| `00504490` | submit-and-swap wrapper | 20 B | tail-calls `003A1DB0` |
| `0036D400` | **frame GS register setup** | 979 B | emits `FRAME`/`ZBUF`/`XYOFFSET`/`SCISSOR`/… |
| `00184460` | viewport rect mapper | 505 B | PS2 reference coords → device pixels |
| `001EB150` | push named GPU scope | 63 B | the pass names; enqueues `RazorMarkerPushObj` |
| `001EB110` | pop named GPU scope | 54 B | enqueues `RazorMarkerPopObj` |
| `0018CA40` | **render command list** singleton | 8 B | returns `01F7F5E8` — a command list, *not* a device |
| `0018C160` | enqueue `RazorMarkerPushObj` | 150 B | allocates a 0x20-byte command object |
| `0018C0D0` | enqueue `RazorMarkerPopObj` | 144 B | |
| `00182970` | post-processing pass wrapper | 44 B | enqueues `PostProcessObj` via `0018C610` |
| `0016D6A0` | folded bare `ret` | 3 B | **both** the marker stub and `__guard_check_icall` |
| `00358380` | pass gate — bit 0 | 18 B | `mask & 1` |
| `003582A0` | pass gate — bit 1 | 20 B | `mask >> 1 & 1` |
| `00358350` | pass gate — bit 2 | 21 B | `mask >> 2 & 1` |
| `003583B0` | pass gate — bit 3 | 21 B | `mask >> 3 & 1` |
| `003583F0` | pass gate — bit 4 | 21 B | `mask >> 4 & 1` |
| `00358300` | pass gate — bit 5 | 21 B | `mask >> 5 & 1` |
| `003582C0` | pass gate — bit 6 | 21 B | `mask >> 6 & 1` |
| `003582E0` | pass gate — bit 7 | 21 B | `mask >> 7 & 1` |
| `003583D0` | pass gate — bit 8 | 21 B | `mask >> 8 & 1` |
| `00358330` | whole mask | 15 B | returns all 16 bits |
| `00358340` | aux gate — bit 2 of the high half | 14 B | reads `022C7F92` |

### Data addresses cited by this document

| Address | Name | Kind | Contents |
|---|---|---|---|
| `02064AD3` | frame-mode selector | `.data` u8 | 0–6; written by the mode bodies themselves |
| `02064AA0` | frame argument | `.data` u32 | stored by `0022A490`, cleared by mode 3 |
| `02064AD0` | completed-frame counter | `.data` u8 | incremented when the dispatcher returns non-zero |
| `02064AD8` | per-frame parity | `.data` u32 | toggled once per frame |
| `022C7F90` | **render-pass enable mask table** | `.data`, **uninitialised at load** | stride 4, indexed by draw mode; low `u16` is the pass mask |
| `022C7F92` | aux mask, entry 0 | `.data` | the high `u16` of entry 0 |
| `02EBEFC0` | command buffer 0 | `.data`, uninitialised | `0x18`-byte descriptor |
| `02EBEFD8` | command buffer 1 | `.data`, uninitialised | `0x18`-byte descriptor |
| `02EBEFF0` | current buffer index | `.data`, uninitialised | 0 or 1 |
| `01FD4A78` | command arena base | `.data` | pointer the backing ranges are carved from |
| `02EBA3F8` | shared sync word | `.data`, uninitialised | the frame's command-stream state |
| `02EAF6D8` | **graphics backend fence — inert** | `.data`, uninitialised | **17 references, all loads, all hoisted out of their loops** |
| `01E0C1D8` / `01E0C1DC` | reference viewport | `.data`, initialised | `0x200` × `0x1C0` = **512 × 448** |
| `01F7F5E8` | **render command list** | `.data` | an EASTL vector of command-object pointers; returned by `0018CA40` |
| `01F7F5E0` | second render command list | `.data` | every command object is appended here too |
| `01F7F4E0` | debug-scope object | `.data` | enable byte at `+8` gates every pass name |
| `020926E4` | display/aspect flag word | `.data` | bits 1, 8, 16 gate post-processing |
| `02064ADC` / `02064AE0` | post-processing latches | `.data` | "eligible" / "already run this draw" |
| `008C5B38` | `1.77778` | `.rdata` | 16:9; the aspect correction constant |
| `01CEBB70` | `0.5` | `.rdata` | the centring term |
| `00908C88` | `"PAD CONTROL"` | `.rdata` | first of the frame section labels |
| `022D9B50` | command-state block | `.data`, uninitialised | address stored into `02EBA3F8` by the frame-open wait |

## 4. Data structures and formulas

### 4.1 The GIFtag, recovered from the code that writes it

`0036D400` opens its batch with

```c
RenderCommand_BeginSubpacket(&scope, 0x1000000000008000, 0xE);
```

and `003A2090` writes those two quadwords as a 16-byte header, then clears everything but bit 15
of the first dword:

```c
// 003A2090 - complete body
hdr             = scope->pCommandBuffer->pWrite;
scope->pCommandBuffer->pWrite = hdr + 1;          // +0x10
scope->pSubpacketHeader = hdr;
*(u64*)&hdr->dword0 = header_qword;               // low 64 bits
hdr->qwTypeOrAux08  = type_or_aux_qword;          // high 64 bits
hdr->dword0        &= 0x8000;                     // keep bit 15, clear bits 0-14
```

Decoding `0x1000000000008000` against that behaviour:

```
bits  0-14  NLOOP  = 0        <- cleared by the &0x8000, back-patched at finalise
bit     15  EOP    = 1        <- the only bit the mask preserves
bits 58-59  FLG    = 0        <- PACKED
bits 60-63  NREG   = 1
high 64     REGS   = 0xE      <- register descriptor 0xE
```

`003A2020` back-patches `NLOOP` from how many records were actually written:

```c
// 003A2020 - complete body
count = (u32)(((char*)scope->pCommandBuffer->pWrite - (char*)hdr - 0x10) >> 4);
if ((*(u64*)hdr & 0x0C00000000000000) == 0x0400000000000000) {   // FLG == 1
    nreg = hdr->dword1 >> 28;  if (nreg == 0) nreg = 16;
    hdr->dword0 |= (count * 2) / nreg;
} else {
    hdr->dword0 |= count;
}
scope->pSubpacketHeader = NULL;
```

The `(count * 2) / nreg` branch is taken only when `FLG == 1`, and doubling the record count
before dividing by the register count is correct exactly when **two registers are packed per
16-byte record** — while the other branch adds the count unmodified, which is correct exactly
when **one register occupies a whole record**. The code therefore states, from its own
arithmetic, that `FLG == 1` means two-per-record and `FLG != 1` means one-per-record, and that
the default batch runs with `NREG == 1`.

*Corroboration, not source:* this is the PlayStation 2 GIFtag, whose `FLG` field is
`0 = PACKED, 1 = REGLIST, 2 = IMAGE`, whose `REGS` descriptor `0xE` is `A+D`
(address-and-data), and in which REGLIST does pack two 64-bit registers per quadword. The
external names are attached to arithmetic already recovered in full; nothing above depends on
them.

```struct GraphicsCommandRecord base=record size=0x10
+0x00  u64  data        the value destined for the register
+0x08  u64  regId       Graphics Synthesizer register number
```

```struct GifTagHeaderRecord base=record size=0x10
+0x00  u32  dword0      NLOOP in bits 0-14, EOP in bit 15
+0x04  u32  dword1      PRE/PRIM/FLG/NREG; NREG in bits 28-31 of this dword
+0x08  u64  regs        register descriptor list, 4 bits per register
```

```struct RenderCommandBuffer base=record size=0x18
+0x00  u64  pBegin                 first record of this buffer's range
+0x08  u64  pWrite                 write cursor
+0x10  u32  nCapacity16ByteUnits   0x200 by default
+0x14  u32  bInitialized           set by ConfigureBackingRange
```

```struct SubpacketScope base=record size=0x10
+0x00  u64  pSubpacketHeader   the GIFtag being filled, NULL when closed
+0x08  u64  pCommandBuffer     the RenderCommandBuffer being written
```

### 4.2 The registers the frame sets, and their exact values

`0036D400` emits seven `(data, regId)` pairs. `w` is `022D8EAC`, `h` is `022D8EB4`:

```c
// register 0x4C
data = (u64)(*(u32*)0x022D8EA8 * *(u32*)0x022D8EB8) | ((u64)((i32)w >> 6) << 16);
// register 0x4E
data = (u64)(*(u32*)0x022D8EB8 * 2) | 0x1000000;
// register 0x18
data = ((u64)((0x1000 - h) * 8) << 32) | (u64)(u32)((0x1000 - w) * 8);
// register 0x40
data = (((u64)(h - 1) << 32) | (u64)(u32)(w - 1)) << 16;
// register 0x1A
data = 1;
// register 0x46
data = 1;
// register 0x45
data = 0;
```

Read as field layouts, without needing any external table:

- **`0x4C`** carries a base value in the low bits and **`width / 64`** at bit 16. Dividing a
  width by 64 to store it is a buffer-width-in-64-pixel-pages field.
- **`0x18`** stores `(0x1000 - dimension) * 8` for each axis. `0x1000` is 4096 and the `* 8`
  is a 1/16-pixel fixed-point conversion at half scale — this **centres a `w` × `h` viewport
  inside a 4096 × 4096 coordinate space**.
- **`0x40`** stores `w - 1` at bit 16 and `h - 1` at bit 48, with zeros at bits 0 and 32 — an
  inclusive `(x0, x1, y0, y1)` clip rectangle.

*Corroboration:* these are the Graphics Synthesizer registers `FRAME_1` (`0x4C`), `ZBUF_1`
(`0x4E`), `XYOFFSET_1` (`0x18`), `SCISSOR_1` (`0x40`), `PRMODECONT` (`0x1A`), `COLCLAMP`
(`0x46`) and `DTHE` (`0x45`), and the field positions above are theirs. The independent PS2-GS
finding in
[texture-mip-local-memory-budget.md](../../17-Presentation-Rendering/Legacy-PS2-GS/texture-mip-local-memory-budget.md)
— which recovered GS *pixel storage formats* from an unrelated function — reaches the same
conclusion from the opposite end of the engine.

### 4.3 The render-pass enable mask

One `u32` per draw mode at `022C7F90`, stride 4; the low `u16` is the pass mask:

```c
passEnabled(bit, drawMode) = (*(u16*)(0x022C7F90 + drawMode * 4) >> bit) & 1
```

| bit | accessor | what it gates in `MainLoop_Draw` |
|---:|---|---|
| 0 | `00358380` | `0036FBB0`, `0036F410`, `0036F430`, `0036F450`, `00475390` |
| 1 | `003582A0` | `0017F2F0`, `0017F070`, `00332420(2)` |
| 2 | `00358350` | `00377230`, `VFXSystem_RenderLayerPass(4)` |
| 3 | `003583B0` | `00252A70` / `0017FD70` / `002450B0` |
| 4 | `003583F0` | **every** VFX and queued-effect pass |
| 5 | `00358300` | second argument to `0036D400` |
| 6 | `003582C0` | `00332420(3)`, `00332420(0)`, `00332420(1)` |
| 7 | `003582E0` | first argument to `0036D400` |
| 8 | `003583D0` | the mid-draw command-buffer flush block |

**The table is in an uninitialised part of `.data`** — it is zero in the file on disk and built
at runtime, so its values cannot be read out of the image. What is fixed in the image is the
*shape*: nine bit positions, one `u16` per draw mode, stride 4.

**No shipped script writes it.** A census of all 10,045 `.ebp` files in `FFXII_TZA.vbf` —
9 locales × ~1,115 `plan_master` scripts plus the 8 `image/` controllers, 237,734 script
bodies decoded with zero faults — finds **not one call** to the three named setter verbs
`20A0`/`20A1`/`20A2` (`debug_setdraw*status`), in any call form, in any locale. The result
is backed by two instruments: a linear symbolic-stack decode that consumed every script's
exact instruction count, and an alignment-independent scan for the 12 possible three-byte
call encodings that returned 0 hits. The neighbouring debug verbs (`0x2098`–`0x20AE`) are
called, so the hole is real: **bits 2, 3 and 4 are set only by the native bulk-configure
routines, never by authored data** (NATIVE/STATIC; `Tools/work/DATA/drawmask/`).

**Correction and completion 2026-09-18 (FABLE): "draw mode" is *which draw of the frame*, and there are two.** The formula above is right; its domain is `drawMode` in {0, 1}. **ANSWERED 2026-09-18 (FABLE): there are two draw modes, not seven; the index is *which draw of the frame* - the ordinary one and an optional second one - and every value either entry can hold is written by one of nine native routines, all read.** The static step this row named as next is done ([drawmask_callers.py](members/drawmask_callers.py), [drawmask-callers.tsv](members/drawmask-callers.tsv): 105 call or jump sites to the setters in 17 functions), and it overturns three things the row said. (1) *`MainLoop_Draw` is not passed the constants 0, 1, 2, 3, 4 and 6.* Every getter call in it is `mov ecx, ebx`, and `ebx` is its own first parameter; the constants my earlier pass read belong to neighbouring calls. Its three call sites pass **0** (`0022A82D`, and `0022AF8A` with a second argument of 1) and **1** (`0022A8B8`). The frame body `0022A770` always runs the draw for index 0, and runs it **again for index 1 only if entry 1's whole word is non-zero** (`00358330(1)`), after the command-word settle, the queued-effects pass 7 when pass 0's bit 4 is up, storing 1 to the byte at `+8`, and a capture sequence gated on the byte at `+9`. (2) *The layout is two entries and three bytes*, which removes the conflict this row recorded between a 4-byte stride and the byte accessors at `+8` and `+9`: `{u16 pass bits, u16 upper bits}` for draw 0, the same for draw 1, then bytes `+8`, `+9` and `+0xA`. The word I called non-indexed at `+2` is draw 0's upper word. (3) *Bit 1 has a setter*, `00358580` (33 B, the same shape as its siblings); the row said none was found. **What the nine routines leave** (bits of the low word; *on* / *off* lists are exactly what is stored): the reset `00358510` - draw 0 bits 0-7 on and bit 8 off, draw 1 bits 0-7 off, `+8` = 0, `+9` = 0, `+0xA` = 1, through the whole-entry setter `00358450`; `0024C7C0` - draw 0 bits 0-6 on, draw 1 bits 0-7 off (the ordinary state); `0024CBE0` - draw 0 bits 0-6 on, **draw 1 bits 0-7 on**, `+9` = 1; `002F1A90` - `+9` = 1, draw 0 bit 3 off and bit 4 on, **draw 1 bits 0-6 on**, `+8` = 1 (its value register is loaded with 1 earlier in the body, outside the artefact's window); and its registered completion `002F1950` - draw 0 bits 3 and 4 on, draw 1 bits 0-6 off, `+9` = 0; `003AB500` - draw 0 everything but bit 3 on (bits 0, 1, 2, 4, 5, 6, 7), draw 1 only bits 3 and 4 on; `003AAA50` - the same two-bit move alone (draw 0 bit 4 on and bit 3 off, draw 1 bits 3 and 4 on); `0035B7D0` - draw 0 bit 8 on, bits 0, 1, 2, 6 off, upper bits 0 and 1 off; and `0035B8D0` its inverse - bit 8 off, bits 0, 1, 2, 6 on, upper bits 0-3 on. Bit 3 is the menu pass and bit 4 the system-effect pass by the game's own verb names, so `003AB500` reads directly: **draw the scene without the menu, then draw the menu and the system effects in a second draw of the same frame.** The three `debug_*` verbs take their index from the script and are never called. No pointer to a setter exists in the image (no `lea`, no data cell), so these sites are all of them. *Not read:* what each of the nine routines is for beyond what its stores show, and therefore which state holds in a given scene - that, and only that, is what a live read would add. Static.

**Who the nine routines are, as far as their callers say (added 2026-09-19, FABLE).** A raw call and jump sweep, joined to the verb table. **`002F1A90` is the script verb `crossfade`** (`016F`; handler `00353260`): the whole scene drawn in the second draw while the first keeps only the system-effect pass, with the capture byte `+9` up - and `002F1950`, which it registers as its completion, is the crossfade's end. **`0035B7D0` is `movieplay`** (`036A`; handler `00356D20` tail-jumps to it) - bit 8 on and the four scene passes 0, 1, 2 and 6 off for draw 0 - and **`0035B8D0` is `movieend` / `moviecancel`** (`036D`, `036E`; handler `0033FA20`), its inverse. `00358510`, the reset, has one caller, `0022A0B0`. The other four belong to one native module: `003AB500`, `0024CBE0` and (through `0024EA10`) `003AAA50` are all called from `0024D540`, a 551-byte body that `MainLoop_Draw`, `MainLoop_UpdateAndRenderFrame` and `0022BC20` each call and that does this work only while the frame-mode byte `02064AD3` is 2 or 6 - `003AB500` further only when bit 0 of `020926E4` is up and its own argument is 0; and `0024C7C0`, the return to the ordinary state, is reached by tail jump from three bodies of the same address band (`0024CEB0`, `0024EB20`, `0024FA40`). ~~*What that module is was not established.*~~ **Identified an hour later, by the verbs that reach its other entry points: it is the script-driven screen-effect module - cut-in, motion blur and soft focus** - sharing the flag word `020926E4`. `cutinplay` (`0310`) reaches `0024CF50`, which raises bit 3 and fills the cut-in state from `02092638`; `cutinclear` (`0311`) reaches `0024CEB0`. `moveblurplay` (`031B`) reaches `0024EC00`, which clears bit 4, fills the state from `02092678`, sets bit 5 and - its last store, `0024ED38` - sets bit 4 again (*this sentence first said the setter of bit 4 was not traced; it is the play body itself*); `moveblurclear` (`031C`) reaches `0024EB20`, and `moveblurclearfade` (`03BC`) reaches it at once only for a zero-frame fade, otherwise through a scheduled fade whose end callback jumps to it (*first written as a direct reach*). `setsoftfocusmode` (`02AE`) reaches `0036E810`, which calls `0024FAE0` to turn soft focus on - bit 0, and the state block at `020925F0` - and `0024FA40` to turn it off. Each of the three *clear* bodies ends in the tail jump to `0024C7C0`, the ordinary mask. So, of the per-frame calls in `0024D540`: **`003AB500` is soft focus** (it is the one gated on bit 0 and handed `020925F0`) - the scene drawn without the menu, then the menu and the system effects in the second draw, which is how a blur can soften the world and leave the menu sharp; **`0024CBE0` is the cut-in** (it returns at once unless the cut-in byte `02092640` is set); and **`0024EA10` with `003AAA50` is motion blur** (gated on bit 4, consuming bit 5). The family is twenty-four verbs (`cutin*` `0310`-`031A`, `moveblur*` `031B`-`0322`, `03AC`, `03BB`-`03BD`, and `setsoftfocusmode`) and now has [a page of its own](../../17-Presentation-Rendering/Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md).

### 4.4 The viewport: PS2 coordinates mapped onto your monitor

`00184460` takes a rectangle in **reference-resolution** coordinates and maps it to the device:

```c
if (FUN_001B1620() == 0) { refW = 0x200; refH = 0x1C0; }   // 512 x 448  (PS2 NTSC)
else                     { refW = 0x780; refH = 0x438; }   // 1920 x 1080

devW = deviceWidth();    devH = deviceHeight();

y = (devH * y_in) / refH;
h = (devH * h_in) / refH;

if (!widescreenCorrected) {
    x = (devW * x_in) / refW;
    w = (devW * w_in) / refW;
} else {
    x = (int)(((float)(devH * x_in) * aspect) / (float)refW);   // aspect defaults to 1.77778
    w = (int)(((float)(devH * w_in) * aspect) / (float)refW);
    x = (int)(((float)devW - (float)devH * aspect) * 0.5f + (float)x);   // centre the pillarbox
}
```

The field frame calls it as `00184460(0, 0, *(u32*)0x01E0C1D8, *(u32*)0x01E0C1DC, 1)`, and those
two globals hold `0x200` and `0x1C0` in the shipping image. **The full-screen viewport is
requested in 512 × 448 PlayStation 2 coordinates and scaled up**, which is why the reference
resolution is the divisor in every term.

## 5. Call chain

```
Phyre::PFramework::PApplication  (framework owns the loop)
  -> GameApplication slot 4                 0017CCD0     [AUTHORITY 22 -> 00]
     |                                                   the framework decides WHEN; everything
     |                                                   about WHAT the frame does is decided below
     |                                                   this hop, so a reimplementation must own
     |                                                   the game side entirely. Labelled under
     |                                                   CALL-CHAINS.md rule 6, 2026-09-18.
     -> 0017D6E0
        -> 0022A490
           -> 0022A580                      frame-mode dispatch
              |
              +-> 0036F2F0                  wait for the graphics backend  (every mode)
              |
              +-> mode body 0..6
              |     |
              |     +-> 0022B0B0  MainLoop_Draw           (modes 2 and 4)
              |     |     +-> 0036D400   emit GS register batch
              |     |     +-> 001EB150 / 001EB110  named pass scopes
              |     |     +-> per-pass calls, each gated on one bit of 022C7F90
              |     |
              |     +-> 0036D400                          (modes 0, 1, 3, 6)
              |     +-> 00184460   viewport in PS2 coordinates
              |
              +-> 0036F2C0                  settle, clear the command-state bits
              |
              +-> (via 003A1DB0, from 38 call sites across the engine)
                     -> 0036F360            publish: 02EBA3F8 = 0x100
                        ~~~~~~ the frame's involvement ends ~~~~~~
                        the consumer of these buffers is NOT in this executable's
                        frame path and was not found: PROPOSED-xiionline-13-1.
                        The 02EAF6D8 fence that would point at it is inert (2.4).
```

**Upstream (who causes this):** PhyreEngine's application framework. The game never calls the
frame; the framework calls slot 4 and the game's override is what a frame *is*. `0017D6E0` is
the sole caller of `0022A490`, and `0022A490` is the sole caller of the dispatcher — the chain
from the middleware slot to the mode switch is a single unbranched path.

**Downstream (what this causes):** a filled 16-byte-record command buffer and one store of
`0x100`. Everything a player sees is downstream of *that store*, not of any Direct3D call made
on this thread.

**Do not confuse with:**

- **There are three layers here, not two, and only the middle one is a flat buffer.** The pass
  wrappers in `MainLoop_Draw` **enqueue C++ command objects** — `PostProcessObj`, `Ps2DofObj`,
  `AmbientOcclusionObj` and the rest — onto a command list; see
  [the-ordered-render-command-list.md](../../17-Presentation-Rendering/Render-Command-List/the-ordered-render-command-list.md). Those objects are the same
  mechanism as the `Gi*` family
  ([gi-render-command-family.md](../../17-Presentation-Rendering/Gi-Render-Commands/gi-render-command-family.md)),
  and they share one contiguous vtable block. The GIF `(data, register)` stream documented here
  is the *third*, lowest layer, written by `0036D400` and friends into a flat buffer with no
  vtable anywhere. A pass wrapper does not write GS registers; it appends an object that will.
- **`003A1DB0` is not the display swap.** Its name says "swap" and it has 38 callers, but its
  only callee is the publish function and its whole body flips an index between two heap ranges.
  The presentation swap chain is created at `00625830` via `D3D11CreateDeviceAndSwapChain`
  (`0080F2C8`), which is not on this call chain at all.
- **`0036F2C0` and `0036F2F0` look like the same idiom and are not.** `0036F2C0` re-reads
  `02EBA3F8` each iteration and is a working settle-read. `0036F2F0` loads `02EAF6D8` **once,
  outside its loop**, and cannot wait for anything. Telling them apart needs the branch target,
  which decompiled output does not give you — and the decompiler renders the inert one as a
  plausible `do { } while (g & 0x100);`.

## 6. Modding notes

- **Best intervention point for turning a pass off:** one bit of `022C7F90 + drawMode * 4`.
  Bit 4 disables every VFX and queued-effect pass at once; bit 2 removes one VFX layer;
  bit 0 removes the `0036FBB0` group. This is a single 16-bit write per draw mode and it is the
  highest, cheapest seam in the whole render path — every gate reads the table fresh on every
  draw, so a change takes effect on the next frame with no invalidation needed.
- **Best intervention point for changing what a frame *is*:** the mode byte `02064AD3`. Writing
  it changes which body runs next frame. Note that modes 4 and 6 are **one-shot** — they
  overwrite the byte themselves before returning, so a write to `02064AD3` that lands on those
  is discarded within one frame.
- **Regenerates itself — do not write directly:** `02EBEFF0` (the buffer index),
  `buffer->pWrite` (reset on every flip), `02064AE0` (the post-processing "already ran" latch,
  cleared at the top of each draw). `02EAF6D8` is a special case: nothing writes it and nothing
  can usefully read it, so setting bit `0x100` by hand does **not** pause the frame — it either
  does nothing or hangs the process at whichever of the 17 sites loads it next.
- **Breaks if:** you enlarge the command buffers past the arena. `004FE420` contains a
  deliberate null-pointer store when `base_unit_offset * 32 > 0x80000`, so an oversized
  `RenderCommand_ConfigureDoubleBufferRanges` crashes immediately rather than corrupting memory.
  Raising the `0x200` capacity without also raising the `0x200` in the terminator logic at
  `0036F360` silently loses the last record of every full batch instead.
- **Breaks if:** you add work between the settle-read and the bit clear in a mode body. The
  inlined spin at `0022BAD0` and its eight siblings exists to make the following
  read-modify-write safe; the decompiler does not show it, so a patch written against
  decompiled source will not know it is there. Note the asymmetry: **that** spin is real, while
  the `02EAF6D8` fence wait in the same function is not.
- **Multiplayer / XIIOnline:** the frame mode is **local presentation state**, not world state.
  Two clients in the same zone can legitimately sit in different modes — one in the field frame,
  one in the menu — and mode 3 does not advance the world. The world tick is
  `World_UpdateSimulationTick` (`00314020`), reached from mode 3 as well as mode 2, so "the menu
  is open" is not by itself a reason to expect the simulation to be stopped: check that call,
  not the mode.
- **Mod compatibility:** nothing in this path reads authored files. It is all code and runtime
  globals, so it does not conflict with asset mods; but two code mods that both write
  `022C7F90` or `02064AD3` will conflict silently, because neither value is versioned or
  checked.

## 7. What is not known

- [x] **CG-6.** **Where the GIF command buffers are consumed.** Reframed by this pass: the question is not
      "which thread clears `02EAF6D8`" — nothing writes that word and the waits on it cannot
      observe it anyway. Ruled out so far: all 17 fence waits (hoisted), all nine thread
      procedures in the image (none is a plausible consumer), and any separate graphics module
      (the imports name only stock D3D11/DXGI). The `0x70000000` record-class mask was searched
      across `.text` and its 12 hits are an unrelated 32-slot handle table at `02EBE5E0`, not a
      record walker. Also ruled out: `Phyre::PThreadPool` and its work-stealing variant, which are
      live classes but touch none of the buffer references; the `00445`-`0044B` handler family
      that reads the arena, which is a *producer* dispatched by `002F4020` on a record type byte;
      and the mid-draw flush block, whose two submit-shaped calls both go to `005C5230`
      (`xor eax, eax; ret`). (`PROPOSED-xiionline-13-1`)
      **LEAD ADDED 2026-09-13 (OPUS): the arena pointer is COPIED to a second global, and the three
      functions that read the copy were never in the consumer search.** `00370DF0` is fifteen bytes
      and does nothing else:

      ```asm
      00370DF0  mov rax, [01FD4A78]      ; the arena
      00370DF7  mov [01EF9438], rax      ; an alias
      00370DFE  ret
      ```

      `01EF9438` then has **9 references in 5 functions** — `00370DE0` (15 B, the same copy in
      reverse), `00370DF0` itself, and **three readers that never touch `01FD4A78` at all**:
      `00370BD0` (254 B), `00370CD0` (269 B, reads the alias three times) and `00373540` (256 B,
      reads it three times). **A census of `01FD4A78` cannot see any of them**, which is exactly
      the second of the four indirections in EVIDENCE-STANDARD 13aw — *the producer hands the value
      somewhere else* — and it is why an otherwise exhaustive elimination missed this branch.
      **`00373540` is in the handle world.** It opens by taking `[rcx+0xA0]` as a **handle** and
      resolving it through **`0020E600`** — the same 32-bit-offset-against-`01F83530` resolver that
      the `02EAF930` registry uses (`EVIDENCE-STANDARD` 13aw, second row) — and bails with `-1` when
      the resolution yields null. So these three sit on the handle-addressed side of the engine,
      where a rip-relative census of *any* buffer address is structurally blind.
      **NOT A CLAIM THAT THE CONSUMER IS FOUND.** None of the three bodies has been read through, and
      none is asserted to walk a command buffer. What changes is that the search space is no longer
      exhausted: three functions that could not previously appear are now named, and the reason they
      could not appear is a mechanism rather than an oversight.
      **AND ONE PIECE OF THE EXISTING EVIDENCE IS WEAKER THAN IT READS.** The bullet notes that the
      mid-draw flush's two submit-shaped calls both go to `005C5230` (`xor eax, eax; ret`). That is
      true, but `005C5230` is **not a stubbed-out GIF submit** — it is the image's shared
      return-zero, called by **351 functions over 438 sites**. The image contains 46 pure no-op
      stubs in total (34 `ret 0`, 12 `xor eax,eax; ret`), and this is the busiest of them. A submit
      resolving there says the call does nothing; it says **nothing specific about the GIF path**,
      and should not be read as evidence that this particular submit was neutered.
      **ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5), static: nothing in this executable reads a finished batch.** The
      submit `003A1DB0` is the only place the finished half is formed; it hands `(begin, count)` to `0036F360`, which
      reads one dword (to append the end tag) and writes the one-cell DMA registers (UQ-211). Every other access forms the
      current half and appends, bounds or counts-then-flushes; OPUS's alias `01EF9438` is scratch space for index lists.
      [The CG-6 record](../../_index/candidates/cg6-no-consumer/README.md) (7 checks).
- [x] **UQ-297.** *(answered 2026-09-18 in section 4.3)* The runtime contents of the pass-enable mask `022C7F90` for each draw mode. The table is
      uninitialised in the image; only its shape is proven. (`PROPOSED-xiionline-13-2`)
- [x] ~~**UQ-298.** What the nine successive stores to the single word `02EBA3F8` in `0036F2F0` mean. The
      values (`022D9B50`, `0x7FFF0`, `0`, `0x14D`) and the bit operations are exact, but a
      sequence of whole-word writes to one address is not a structure and is not yet explained.
      (`PROPOSED-xiionline-13-3`)~~ **Answered 2026-09-14 (FABLE), by reference:** they are **a command sequence whose consumer no longer exists**. This was read as `CG-1` / `CG-2` on [the shared command state word](../../17-Presentation-Rendering/Graphics-Thread-Handshake/the-shared-command-state-word.md) §7 (the inert fence is §10), and re-checked here.
      - **Nothing in between.** Between the first store (`0036F30D`) and the last (`0036F352`) there is no branch, call or wait. The two read-modify steps (`0036F32F`, `0036F341`) read back what the burst itself just wrote.
      - **No reader of the values.** No instruction in the image tests bits 2, 3, 4 or 5, or the values `0xC` or `0x14D`. The only masked reads of the word are the bit-8 settle-spins and the unmasked range compares of the publishers.
      - **No other thread watching.** The `02EAF6D8` fence at the top of the function is inert: its load is hoisted out of the spin, and the word is never written. So nothing establishes a core that could observe the intermediate values.
      - **The only lasting effect** is the final store of 0.
      The shape — the state block's address, a 15-bit mask, a clear, a set of bit 3, the command word `0x14D`, then 0 — reads as a console-side backend protocol carried over intact. **What each command meant to that backend is not decidable from this executable**, because the receiver is not in it.
- [x] **UQ-299.** What modes 5 and 6 are in player terms. Their section labels (`CAPTURE DRAW`) and their
      transition (6 → 5) are proven; the feature they serve is not. (`PROPOSED-xiionline-13-4`)
      **NARROWED 2026-09-25 (FABLE, Claude Opus 5.5): the entry, the exit and what the mode saves are read, and
      the owner is one modal object. Its on-screen name is still open.**
      - **Only two callers of `002E2240`.** Mode 6 is set in exactly one place and mode 2 is restored in exactly
        one place: `002E2240` has two raw callers.
      - **Entry: `00228930`.** It runs at the tail of `002507C0`, the per-frame driver that the mode-2 and mode-1
        bodies call. It acts only when the `[0209AC30] + 0xC8` object exists and bit 12 (`0x1000`) of that
        object's flags word (`[+0xC0] + 8`) is set. It then does four things:
        - saves the sixteen words `002E1020(0..15)` into `01FD4700`…;
        - calls `002E2240(1)` (`00228989`), which ORs `0x100203` into `0215F1DC` and sets mode 6;
        - clears bit 12;
        - copies `00244620()` into bit 14.
      - **The request bit has one writer.** Bit 12 is raised only at `00228295`, in the message-1 arm of
        `00228130`, which points the object's `+0xC0` at `[0209AC30] + 0x3F8`. So the word is
        `[0209AC30] + 0x400`, the same one the load-restart path ORs `0x600` into.
        - Domain: every `or`/`bts` on a `[reg + 8]` operand with `0x1000`, plus every write or RMW to a
          `[reg + 0x400]` dword, across the function list.
        - Control: `00285E6B` is found. The other `+0x400` writers set other bits (`00285EB6` bit 13) or are
          plain `mov` stores in three functions in the Phyre address range. Their receivers were not traced,
          so "one writer" holds for the setting forms and is bounded by those three.
      - **`00228130` is the message handler of the `0xD8` object.** `00228700` installs it at `+0xC8`
        as a `0xD8`-byte object. The modal gate (the battle-mode ladder page's "modal state machine") calls `00228700` when its input conditions fire.
        Those conditions include pad word `02F9736A` tested against `00915538` = `0x8`, i.e. bit 3. That bit is
        **Start** *if* this word uses the DualShock order of the binding-name table, where R2 is bit 9 (the
        force-fight page); that equivalence is inferred, not read.
      - **Exit.** Message `0x12` (`00228168`–`00228178`) calls `00229510`. That function sets mode 2 through
        `002E2240(0)`, which clears the `0x100203` bits. It then replays the saved words for groups 2 and 8
        only, bits 0–21, through `002E1CA0` / `002E1C20`.
      - **What it is not.** It is **not the pause menu**: that is the separate `[01FD4940]` widget, opened
        by `002282F0` on button bit `0x15`.
      - **The companion object.** Its `+0xD0` object (created by `002289D0`) formats four
        text rows (row format `0x467C`, row ids `0xF`–`0x12` and `0xC`) and reaches two save-image
        helpers and the two context-bit setters beside the load-restart path.
      - ~~**Still open:** which screen this is. Resolving it needs those text ids turned into strings, or a live
        observation.~~ No debug string sits in any of the five bodies (a scan of every `lea` target).
      - **ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5): it is the interruption dialog - "controller not connected" or
        "disc cannot be found".** The text ids were resolved from the shipped files as follows.
        - `002F9860(id)` splits the id into id ÷ 1000, a text group, and id mod 1000, a row.
        - A group reaches its file through `002FA560` → `002385D0`. That maps the group through the byte table
          `01E09F68` to a kind-2 loader id, and loads the `MMSG` resource. By the same size-match method as `GE-1`
          (`FileSizeTable_US.fst`, 5,000 dwords per kind), group 2 is loader id 21, which is
          `test_battle/us/binaryfile/menu_message.bin` (10,036 bytes). Group 18 is loader id 55, which is
          `menu_command_template.bin` (5,856 bytes). The control, group 12 → id 49 → `listhelp_status.bin`,
          reproduces `GE-1`.
        - Decoded, with `0x20`–`0x39` as `A`–`Z`, `0x3A`–`0x53` as `a`–`z` and string offsets from table + 12:
          - `0x82E` (group 2, row 94) is **"The FINAL FANTASY XII disc cannot be found."**;
          - `0x830` (row 96) is **"DUALSHOCK analog controller not connected to controller port 1. Please
            connect a DUALSHOCK analog controller to controller port 1."**;
          - `0x467C` (group 18, row 44) is a pure control-code row template.
        - The dialog's state word `+0xE2` chooses between the two messages. State 1 loads `0x830`
          (`00228F59`–`00228F97`), and state 2 loads `0x82E` (`00228F0F`–`00228F4E`). State 1 is reached when
          pad 0's status (`0035F150(0, 0, 0)`, the `0x294`-stride pad records at `022CAE90`) stays empty
          until the countdown `01E027F8` (initial 6) runs out (`00228E96`–`00228EDF`). The disc state involves the
          word `[022CBBA4]` read through `003641F0`.

        *So modes 6 → 5 host the PS2-era controller / disc interruption screen. Which of its states the PC build
        reaches in play, and whether the entry gate's pad bit is Start, are not established; both are live
        questions.*
- [x] **UQ-300.** What `ATEL` stands for in the `ATEL CONTROL` section label of modes 3 and 5. ~~*(NO ADMISSIBLE SOURCE, reviewed and signed 2026-09-26 by OPUS; see the register row UQ-300.)*~~ *OUT OF EVIDENCE BOUNDARY, 2026-09-27 (FABLE, Claude Opus 5.5): FRONTIER's batch-K Extension 2026-09-27f classes an identifier name by its carrier, the unshipped source / `FF12X64.pdb`; OPUS's signature carries. See the register row UQ-300.*
      (`PROPOSED-xiionline-13-5`)
- [x] ~~**UQ-301.** Whether the `0x200` record capacity is ever raised at runtime by
      `RenderCommand_ConfigureDoubleBufferRanges` (`003A1E10`), which exists precisely to change
      it but whose callers were not traced in this pass. (`PROPOSED-xiionline-13-6`)~~ **Answered 2026-09-14 (FABLE): never raised. The only runtime change halves it for one window and then restores it.**
      - **Argument order.** `003A1E10(capacity, offset)` configures buffer 0 as `(capacity, offset)` and buffer 1 as `(capacity, offset + capacity)`. This follows from `RenderCommandBuffer_ConfigureBackingRange(buffer, capacity, offset)`, which stores `capacity` at `+0x10` and the base `01FD4A78 + offset × 16` (`004FE45D`–`004FE485`).
      - **Two raw call sites, both in `RenderResourceRoot_UpdatePresentationAndSkeletonContainers` (87 B).**
        - On entry it calls `(0x100, 0x200)` (`0041E349`–`0041E353`): 256 records each, at record offsets 512 and 768. That is the default buffer 1's range split in two.
        - It then runs `SkeletonModelGroup_UpdateFinalPoses` and a second update.
        - It leaves by tail-calling `(0x200, 0)` (`0041E386`–`0041E392`), which restores the initialiser's 512-record ranges at 0 and 512.
      - **Reach.** The function's one caller is `RenderSystem_RunCharacterUpdatePipeline`.
      **So nothing enlarges the buffers.** For the character update's duration they are 256 records each, over the arena's upper half.
      *Not read:* §2.5's terminator test compares the record count with the literal `0x200`, not with the configured capacity. Whether anything is emitted inside the halved window, and so whether that literal can exceed the smaller ranges, is not established here.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The frame chain `0017CCD0 → 0017D6E0 → 0022A490 → 0022A580` | complete exact-current bodies of all four; `0017D6E0` is the sole caller of `0022A490` and `0022A490` the sole caller of `0022A580` in a call graph regenerated from this program state | 1 |
| Seven frame modes selected by `02064AD3` | complete body of `0022A580`: a `switch` with seven arms | 1 |
| The mode transitions 4→3, 6→5, 0→1, 1→2, 3→2 | complete bodies of `0022AF50`, `0022B000`, `0022B6E0`, `0022B7E0`, `0022B8C0`; each contains a literal store to `02064AD3` | 1 |
| The frame section labels | `lea rcx, [label]; call 0016D6A0` decoded from raw bytes in eight function bodies; each target read as a NUL-terminated ASCII string from `.rdata` | 1 + 2 |
| `0016D6A0` is a folded bare `ret` shared by the marker stub and the CFG guard | 3-byte body; instance of open question BA-1 | 1 |
| `02EAF6D8` is never written by game code | displacement census over the whole `.text` section for that exact address: 17 sites, every one a `mov r32, [rip+d]` load, confirmed by disassembling each. Blind to base-pointer writes, per `COVERAGE.md` | 1 |
| **All 17 fence waits are hoisted and cannot observe a change** | raw disassembly of all 17: in every one the conditional branch targets the `test`, at a *higher* address than the `mov` that loads the word, so the load is outside the loop | 1 |
| `02EAF6D8` is zero at load | its RVA lies beyond `.data`'s `SizeOfRawData`, so it is zero-filled | 1 |
| No thread in this image consumes the command stream | complete enumeration of thread creation: 5 `CreateThread` and 4 `_beginthreadex` call sites, each disassembled for the `lea` supplying its start routine; nine procedures, largest 555 B. **Premise corrected 2026-09-12 (FABLE):** the enumeration was not complete — the engine's own thread API `008636E0` creates four more threads the imports never show (`TkSyncVEmulationThread` `0035EA40`, `TkBGThread%d` `00368C10`, `TkSyncvThread%d` `00369100`, `TkPowerOff` `00368AE0`, all from `00368ED0`); a depth-8 walk from each reaches neither the publishers nor the shared word, so the claim stands on thirteen procedures, not nine (CG-3) | 1 |
| No separate graphics module | every DLL-shaped string in the image: 32, of which the graphics ones are stock `d3d11.dll`, `dxgi.dll`, `D3DCOMPILER_47.dll` | 2 |
| `0036F2C0` contains a settle-spin the decompiler omits | raw bytes `8b0d…/8b05…/3bc8/75f0` at `0036F2D0`–`0036F2DE`, compared against the decompiler's one-line output for the same function | 1 |
| The same spin is inlined in the mode bodies | raw disassembly at `0022BAD0` (inside `0022B8C0`) and `0022B2C0` (inside `0022B0B0`); displacement census locates nine more | 1 |
| A command record is 16 bytes, `(data, regId)` | the emit idiom in the complete body of `0036D400`, repeated seven times with distinct register numbers | 1 |
| `NLOOP` is back-patched from the record count | complete bodies of `003A2090` and `003A2020`, read together | 1 |
| The GIFtag constant `0x1000000000008000` with `REGS = 0xE` | the literal operands at the `003A2090` call site in `0036D400`, decoded against the mask `&0x8000` that `003A2090` applies | 1 |
| The register field layouts (`>> 6` page width, `0x1000` centring, inclusive clip rect) | the arithmetic that builds each `data` value in `0036D400` | 1 |
| The GS *names* for those registers | external PlayStation 2 hardware documentation, attached to an already-exact native matrix; **corroboration only**, and no claim above rests on it | 9 |
| 512 records per buffer, and why `0x200` appears in the terminator logic | `003A1D50` passes `0x200` as capacity; `0036F360` compares the record count against `0x200`; the two were read independently | 1 |
| Nine pass-gate bit positions over `022C7F90` | complete bodies of the eleven accessor functions, each a single shift-and-mask | 1 |
| `022C7F90` is uninitialised in the image | PE section walk: its RVA lies beyond `.data`'s raw size, so it is zero-filled at load | 1 |
| The 512 × 448 reference viewport | complete body of `00184460` with the literals `0x200`/`0x1C0`; the call site in `0022B8C0` passes the globals `01E0C1D8`/`01E0C1DC`, whose initialised contents in the image are `0x200` and `0x1C0` | 1 |
| The EXE analysed is the authority binary | SHA-256 of the file used for every raw-byte reading in this document is `73461d08…21f8`, matching the recorded authority hash | 1 |
| No body-size drift | the call graph was regenerated from this program state and every body size in §3 taken from it; a diff of `entry, body_bytes` against the previous dump is empty | 1 |

**Killer observations named and sought:**

- *"`02EAF6D8` is written by ordinary frame code, so the two-thread reading is fiction."* — Sought
  by censusing the whole `.text` for that displacement and disassembling all 17 hits. Every one
  is a load, which I first read as confirming a cross-thread producer. **That inference was
  wrong**, and re-attacking the same 17 bodies for their *branch targets* rather than their
  operands is what broke it: see the superseded reading below. The literal claim — no game-code
  writer — survived; the conclusion drawn from it did not.
- *"`003A1DB0` presents the frame, so calling it a command-buffer flip is wrong."* — Sought in
  its callees: it has exactly one, and that one only writes a terminator and a status word. The
  swap chain is created in a function not on this chain. **The friendly name was wrong; the
  document uses the mechanism instead.**
- *"The `(data, regId)` pairing is pattern-matching on a coincidence."* — Sought an independent
  witness in the GIFtag: `REGS = 0xE`, `NREG = 1`, `FLG = PACKED`, and a finalise routine whose
  two branches only make arithmetic sense under one-register-per-record and
  two-registers-per-record respectively. **Two independent readings agree.**
- *"The decompiler is right and my disassembly is misaligned."* — Sought by dumping the raw
  instruction bytes alongside every RIP target, and by confirming the function extents against
  the regenerated graph. `0036F2C0`'s 43-byte extent contains both the spin and the `and`.
  **The decompiler was wrong.**

**Crossref audit disposition (2026-09-07, against a graph regenerated from this program state):**

`audit_crossrefs.py` reported **zero** `GHOST ADDRESS` and **zero** `BODY DRIFT` for this
document, and eight `UNACCOUNTED NEIGHBOUR` findings. Every one is dispositioned here.

| Subsystem | Edges | Disposition |
|---|---:|---|
| `Movement` | 13 | **Real and now stated.** `MainLoop_Draw` calls `00357780`, and modes 3 and 5 call `00263560` and `0037CF00`. The frame drives movement; that is what a frame does, and §5 previously showed it only as unnamed callees. See the note below. |
| `ActorEntity` | 7 | **Real and now stated.** Six edges are callees of `World_UpdateSimulationTick` (`00314020`), which this document already cites as the world tick; the actor update hangs off it. The seventh, `002E05C0 caller 0026DFB0`, means the menu-close predicate is also read by actor code. |
| `Party` | 5 | **Real, and partly already visible.** `00358BB0` (`PartyFocus_CommitPendingPackedActorHandle_Thunk`) appears in the §5 chain but was never named as Party. Modes 2, 3 and 5 all commit a pending party-focus handle once per frame. |
| `Platform` | 5 | **Genuinely irrelevant.** All five are internal callers/callees of `00625830`, which this document cites *only* to say the swap chain is created somewhere off the frame chain. Its internals are the D3D11 device-creation system's business and are not a claim here. |
| `Audio` | 3 | **Real and now stated.** The `"SOUND"` section label in modes 3 and 5 is an actual audio entry: `0022A770` calls `0036F460`, and the world tick calls `00362850` and `002DEBA0`. |
| `RNG_Random_Selection` | 2 | **Real and worth stating for determinism.** Boot modes 0 and 1 both call the MT19937 next-u32 thunk `00379CD0` **once per frame**, so the generator advances during boot at a rate set by frame count. Anyone reproducing an RNG sequence from a cold start must account for that. |
| `Rewards_Progression_Economy` | 2 | **Surfaced by the row above, and it makes that row matter more.** `00379CD0` is a 5-byte thunk onto one shared generator, and `002F9A60` / `002F9B20` in the rewards and loot path are two of its many callers across combat, spawning and rewards. So the per-frame advance in boot modes 0 and 1 is not a private stream — **it displaces the shared sequence every other consumer later draws from.** Two runs that spend a different number of frames in boot do not agree on loot. The neighbour edges themselves are not this document's subject; the consequence is, and is stated here. |
| `Developer` | 1 | **Real, minor.** `0017D6E0` calls `001C2F50`; the developer-tuning console is ticked from the tick→frame adapter, above the mode switch, so it runs in every mode. |
| `PlatformOnlineAchievements` | 1 | **Real, minor.** The field frame `0022A770` calls `00316930` once per frame — achievement polling on the gameplay path only. |

**What the Movement, ActorEntity, Party and Audio findings have in common** is that this document
described the frame as *scheduling and drawing* and left what it schedules unnamed. It is a frame:
its callee set is the whole game. The finding is fair, and the honest statement is that the mode
bodies are the top of the call graph for movement, actors, party focus, audio and achievements,
each entered exactly once per frame from the mode bodies named in §2.2 — not that those
subsystems are outside this document's scope.

**Superseded readings:**

- **Believed in the first version of this document, and published:** that `0036F2F0` is a working
  cross-thread wait, that the frame "hands the list to a second thread", and that a graphics
  backend clears `02EAF6D8` bit `0x100` when it has drained the buffers. **Now believed:** the
  wait cannot wait. In all 17 sites the load of `02EAF6D8` sits *outside* the loop — the branch
  targets the `test`, not the `mov` — so the loop spins on a register nothing inside it changes:
  it either never runs or never exits. Proved by disassembling the branch target of each of the
  17, then corroborated three ways (the word is zero-filled at load; no `.text` store to it
  exists; none of the image's nine thread procedures could consume a command stream, and the
  imports name no graphics module beyond stock D3D11/DXGI).
  **Why the earlier reading was reachable, and where the same mistake will be hiding:** the
  decompiler renders this as `do { } while ((g & 0x100) != 0);` — a perfectly ordinary spin —
  because it reconstructs the loop from control flow and the hoisted load reads as loop-invariant
  code motion it can undo in its output. *"All references are loads"* then looks like the
  confirming observation, when for a hoisted read it is equally consistent with dead code.
  **A spin loop cannot be verified from decompiled output at all**: only the branch target
  distinguishes a working spin from an inert one, and that is exactly what decompilation
  discards. The sibling settle-spin at `0036F2C0`, thirty bytes away in the same file, *is*
  genuine — so the two cannot be told apart without the disassembly.

- **Believed while this document was being written:** that `01F7F5E8` is "the render device
  singleton", because 46 call sites fetch it and immediately pass it to a function that draws
  something. **Now believed:** it is an **EASTL vector of render command objects**, proved by
  `0018C9E0`, which allocates a 0x20-byte object of three pointers plus an allocator named
  `"EASTL vector"`, and by every consumer sharing one `push_back` idiom against `+0x08` / `+0x10`.
  The earlier reading was reachable because *"fetch the singleton, call a function on it, a pass
  happens"* is exactly what using a device looks like from the call site — which is the reason
  ownership may never be inferred from a caller. Corrected within the same pass; the mechanism
  described in §2.6 was unaffected, only the name.

- **Believed on entry to this pass:** "Every polygon a player sees goes through PhyreEngine"
  — the framing this document's own category was assigned under. **Now believed:** PhyreEngine
  owns the application shell, the reflection and asset system, animation, and the D3D11 device
  creation, but **the per-frame scene drawing is a PlayStation 2 GIF command stream that does
  not enter Phyre code at all.** Proved by following the frame from the Phyre slot to the
  command buffer without passing through a single `Phyre::` symbol. The earlier reading was
  reachable because the category's function count is dominated by generated reflection glue, and
  because RTTI supplies plausible renderer class names — `PMaterial`, `PMeshInstance`,
  `PRenderTarget` — for classes the frame never touches. **A class name is not a mechanism.**

## 9. Related

- [`../Application-Framework-Boundary/the-game-is-a-phyre-application.md`](../Application-Framework-Boundary/the-game-is-a-phyre-application.md) — establishes the slot-4 tick this document starts from
- [`../Subsystem-Map/phyre-subsystem-map.md`](../Subsystem-Map/phyre-subsystem-map.md) — its finding that "no game subsystem calls Phyre" is explained here: the render path leaves Phyre entirely
- [`../../17-Presentation-Rendering/Render-Command-List/the-ordered-render-command-list.md`](../../17-Presentation-Rendering/Render-Command-List/the-ordered-render-command-list.md) — what each pass wrapper enqueues, and the order key that decides layering
- [`../../17-Presentation-Rendering/Graphics-Thread-Handshake/the-shared-command-state-word.md`](../../17-Presentation-Rendering/Graphics-Thread-Handshake/the-shared-command-state-word.md) — **owns `02EBA3F8`**, the word the frame's settle-spins guard. Independently reached the same retraction of the two-thread reading; its census of 24 write-form and 38 read-form references agrees with the 62 this document's own scan found
- [`../../17-Presentation-Rendering/Legacy-PS2-GS/texture-mip-local-memory-budget.md`](../../17-Presentation-Rendering/Legacy-PS2-GS/texture-mip-local-memory-budget.md) — the same PS2 GS fossil, reached from texture budgeting
- [`../../17-Presentation-Rendering/Gi-Render-Commands/gi-render-command-family.md`](../../17-Presentation-Rendering/Gi-Render-Commands/gi-render-command-family.md) — the *other* drawing path; see §5 "Do not confuse with"
- [`../../17-Presentation-Rendering/Post-Processing/the-post-processing-effect-catalogue.md`](../../17-Presentation-Rendering/Post-Processing/the-post-processing-effect-catalogue.md) — what the `"post-processing render"` scope contains
- [`../../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md`](../../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md) — the class map this pass started from, and open question BA-1 on folded addresses

## Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

Three claims about `02EAF6D8` stand or fall together, and **all three hold exactly**.

| claim | measured |
|---|---|
| never written by game code — **17 sites**, every one `mov r32, [rip+d]` | **17** references in `.text`, **17** reads, **0** writes |
| **all 17 fence waits are hoisted** — each conditional branch targets the `test`, at a *higher* address | **17 of 17**, and **0** sites had no conditional branch within five instructions — the check covered every one |
| zero at load — its RVA lies beyond `.data`'s `SizeOfRawData` | `.data` raw ends at RVA `01E5E3FF`; the word is at RVA `02D8F6D8`. **Beyond it, therefore zero-filled** |

> **Taken together these are stronger than any one of them.** A fence word that **nothing writes**,
> that **begins at zero**, and whose **every waiter loads it once and then spins on a register**,
> cannot be satisfied by anything in this image. Each claim alone leaves an escape — an unseen writer,
> a re-read, a non-zero initial value — and the three close all three escapes at once.
>
> The **`0` writes** is the claim that needed the population stated, and it has it: the census is over
> the whole `.text`, and the seventeen are enumerated rather than sampled.

### `0016D6A0`, a fourth time — and here is the mechanism

This page calls `0016D6A0` *"a folded bare `ret` shared by the marker stub and the CFG guard"*. This
sweep met the same three bytes as the verb dispatch's absent-callback filler, the save-image clear's
tail jump, and a field-music rebase callback. **This page supplies the reason the others only
observed: the linker folded identical three-byte bodies.** One address, four documented uses, one
cause.

**Not claimed:** nothing here was executed or observed live; `BA-1` stays open, and the thread and
DLL censuses in the same table were not re-run.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Resource — SERVICE (FABLE, Claude Opus 5.5, 2026-09-25).** UQ-299's answer follows the text-group loader into that
layer's resource-request path. This page claims only which shipped text files the dialog's ids name. The frame drivers'
other resource callees are that layer's business.

**CombatAction — CLIENT.** `BattleUnit_TryTriggerNearbyAuthoredFieldAction`, owned by that layer, calls `00379CD0` on this page. That caller is the nearby-trigger attempt, a `0x98`-byte frame with a stack cookie carrying three arguments through to the test; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatFormula — CLIENT (53 edges, one fan-in).** All 53 edges are CombatFormula bodies calling `00379CD0` on this page: the five-byte thunk onto the CRT's Mersenne Twister that this page documents. `BattleFormula_RollGuardParryMode` is the worked example - it reduces its draw modulo 100 against the threshold at `[02AEDFDC]`. The crossing is **one shared primitive with 53 callers**, not 53 separate relationships, and naming a single body would say less than the count does. Edge count from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Audio — CLIENT (SWE2-EC7-166, 33 edges).** `00181DD0`, the allocator
this page's `003B4160` slot issuer runs, and `001EDDA0`, its flag gate,
are also consulted by the Audio layer - `00181DD0` by `00332C40`/
`003B99D0`/`003D7CE0`/`003D7DC0` and `001EDDA0` by `0024B9B0` (+25 more
of the same shape). Shared leaves.

**CoreRuntimeScheduling — CLIENT (SWE2-EC7-166, 136 edges).** The frame
subjects `0017CCD0`/`0017D6E0` are consulted by the scheduling layer
(`0017D6E0` calls `001A1460`/`001DB600` and is called there; +133 more
of the same shape). Consultation of the frame's helpers, not shared
ownership.

**Presentation — CLIENT (SWE2-EC7-166, 1,204 edges).** The frame's
subjects are consulted across the Presentation layer - `0017D6E0` calls
`00189CE0`/`001BC190`/`001BDAC0` and is called there, the broadest
crossing this page carries (+1,200 more of the same shape). The frame
feeds presentation; no shared ownership.

**UI — CLIENT (SWE2-EC7-166, 29 edges).** `0017FFD0`, `00181DD0`,
`001EDDA0` and `001A1470` are called by `002C7B10`/`0024B9B0`/`0018EEE0`
on the UI layer (+25 more) - the widget side reads the frame's records.
Consultation, not shared ownership.
## The `00358BB0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00358BB0` (`PartyFocus_CommitPendingPackedActorHandle_Thunk`, 5 B) —
`jmp 00358BC0`.

| member | role | interior |
| --- | --- | --- |
| `00358BC0` | `byte[022C7FF8]` gate, then `dword[022C7FE4]` commit (`00358BC4`/`00358BD1`) | [`00358BC4`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## Interior citation — frontier hub `0022CC20` (2026-09-17, SWE2-EC7)

`0022CC20` — 15 B, 56 frontier callers at census; the processor-battery rows above already list
it as the repeated call inside the draw-state block builders. Interior verified:
[`0022CC27`](../../_index/ADDRESS-INDEX.md) is `movups [rip+...], xmm0` — the whole body is
`movaps xmm0, [rip+0x6993A9]` (a 16-byte `.rdata` constant at `008C5FD0`) then `movups` storing it
to the `.data` cell `01E02830`; `ret`. A **constant-vec4 publish**: the builders call it to reset
one global quad to its canonical value before the rest of the block is filled.

NOT claimed: which draw-state field `01E02830` is (the processors' records are the enclosing
context, not this leaf's owner).

## Interior citation — frontier hubs `0022CC40` / `0022CC30` (2026-09-17, SWE2-EC7)

The two flag leaves the processor batteries above already pair with `0022CC20`. Both read against
the shipping image:

- `0022CC40` (9 B, 36 frontier callers) — `or word ptr [02064DEC],0x40; ret` at
  [`0022CC47`](../../_index/ADDRESS-INDEX.md). Sets bit 6 of the shared flags word.
- `0022CC30` (13 B, 36 frontier callers) — `mov eax,0x80; or word ptr [02064DEC],ax; ret` at
  [`0022CC3B`](../../_index/ADDRESS-INDEX.md). Sets bit 7 of the **same** flags word —
  `0022CC40`'s sibling, not a copy.

Both are pure flag-set leaves: no return value, no reads of the word they modify.

## Interior citation — frontier hubs `003A1DB0` / `0022CC40`-class anchor (2026-09-17, SWE2-EC7)

`003A1DB0` — 84 B, 17 A-measured callers at census; the submit-and-flip whose complete body this
page already quotes. Interior anchor only: the flip is `eax = 1 - dword [02F8EFF0]` stored back
at `003A1DCA`, the two 24-byte slots are `lea rcx,[rdx+rdx*2]`-indexed at
[`003A1DD0`](../../_index/ADDRESS-INDEX.md), the record count is `(end-begin)>>4`, and
`call 0036F360` at `003A1DEF` is the submit before `entry[+8] = begin` mirrors the range.


## Interior citation — frontier hubs `001EB150`, `001EB110` (2026-09-18, SWE2-EC7)

`001EB150` — 63 B, 6 A-measured callers; `001EB110` — 54 B, same callers' sibling. Twin
guarded frame-boundary hooks. Interior verified: both call `0018CA40()` for the shared frame
object, require it and the global flag byte `[01F7F4E0]+8` nonzero (`001EB167`–`001EB177`,
`001EB11E`–`001EB12E`), then tail into the real hook — `0018C160(obj, arg)` at
[`001EB184`](../../_index/ADDRESS-INDEX.md) for `001EB150`, `0018C0D0(obj)` at `001EB13C` for
`001EB110`. When the flag is down both are no-ops; the gate is the frame's armed state.


## Interior citation — frontier hubs `003583F0`, `005376D0` (2026-09-18, SWE2-EC7)

`003583F0` — 21 B, 9 callers; the `022C7F90` flag-table bit read. Interior verified:
`word [022C7F90 + ecx*4]` loaded, `>> 4`, `& 1` at
[`003583FA`–`00358401`](../../_index/ADDRESS-INDEX.md) — bit 4 of a 32-bit-per-index flag
word.

`005376D0` — 760 B, 13 callers; a float-table builder sibling of the generated-table family.
Interior verified: fills `02064B10`/`02064CB0` via `005379D0` calls with `02064B04` presets —
`-pi/2` (`0xBFC90FD8`) then `+pi/2` (`0x3FC90FDB`) at [`00537710`/`0053774C`](../../_index/ADDRESS-INDEX.md)
— and accumulates `word [02064B0C]`/`[02064B10]` counts into a `0x80`-based index
(`00537771`–`00537785`). The pair of quarter-turn constants brackets a symmetric table.


### Interior citation — frontier hubs `00376470`, `0036FDF0` (2026-09-18, SWE2-EC7)

Two of the per-frame driver's (`0022A770`/`0022B8C0` cluster) five-callee fan-out.

`00376470` — 1,300 B, 5 callers. A per-record transform batch: each iteration
walks a 0x90-stride record (`rbx += 0x90` at `00376919`), builds a 4x4-float
block on the stack, runs `00202D70` + `00202FE0` (normalise) on all four rows
([`003767EA`](../../_index/ADDRESS-INDEX.md)), transforms through `0017ED50`,
then re-normalises the result and hands it to `001849E0`. `00182530` finalises
after the loop; `__security_check_cookie` (`00808C40`) guards the 0x200-byte
stack frame. This is the batch that publishes each channel's transform rows.

`0036FDF0` — 381 B, 5 callers, `InputGameplay_RebuildRemappedTrans…`. Clears the
seven `0276A0xx` counters, then per pad (`edi` 0..1, `rsi` the row): for each
lookback `ebx = 1 - InputControl_GetHistoryLookbackCount(pad)` .. 0 it ORs the
four history masks `0035EF10/70/D0/30` into the `0x29B9E20..2C` word quads
([`0036FE74`](../../_index/ADDRESS-INDEX.md)), then remaps each quad through
`InputControl_RemapMaskThroughChannelLogicalMap` (`0035EDE0`) into
`0x29B9E04..1C`. The button-history to logical-button table the frame rebuilds
before reading input.

### Interior citation — frontier hub `005375F0` (2026-09-18, SWE2-EC7)

`005375F0` — 224 B, 12 callers: the per-frame oscillator advance on the
`02064B04`/`02064C70` float cells. Read from the shipping image: it compares
`02064CB0` against `01E02830`, latches `02064B0C`, adds the `3E22F983` step
onto the accumulator, stores π (`40490FDB`) into `02064B04`, and composes the
`shl 4 / shl 3 / &0x80` masked word written to `02064B10` at
[`00537658`](../../_index/ADDRESS-INDEX.md) — with mirrored cells at
`02064DDC`/`02064DE0` and a `dx == cx` arm that swaps in the negated-π pair.
The angle-table state `005376D0` presets. No calls.
## SWE2-EC7-23 update (2026-09-18) — `003A2090`/`003A2020` freelist pair + `0039D570`/`0039D3F0` alloc wrappers

`003A2090` (39 B) is the intrusive 16-byte-element freelist push: `[rcx+8]`
bump cursor, `r10 = [r9+8]` grabbed, `[r9+8] = r10 + 0x10`, `[rcx] = r10` head,
`[r10] = rdx` link, `[head+8] = r8`, `or [head], 0x8000` flag — the queue push
the frame's record pool drives. Interior anchor `003A209C`.

`003A2020` (102 B) is the load-metric companion: `rdx = ([rax+8] - [r8] - 0x10)
>> 4` element count, `rax = [r8] & 0xC00000000000000` top-bits mode compare,
`ecx = [r8+4] >> 0x1C` nibble divisor (0x10 default), `(rdx*2) / ecx` folded
back via `or [r8]` — the occupancy field the pool publishes. Interior anchor
`003A203B`.

`0039D570` (46 B) is the two-path alloc pair dispatch: `ecx != 0` ->
`00862E50` + `00862E90(2)`; else `008652B0` + `008652F0(2)` — the CRT alloc
wrappers the frame bodies share. Interior anchor `0039D578`.

`0039D3F0` (23 B) is the single-path sibling: `00865130` + `00865170(2)` —
the matching wrapper pair. Interior anchor `0039D3F4`.

## SWE2-EC7-24 update (2026-09-18) — `0035EF10` wrapped word fetch

`0035EF10` (86 B) bounds-checks `ecx < 2`, strides `ecx * 0x294` into
`022CAE90`, then adds `r8d` to `byte[+1]` with a signed `mod 0x10` wrap in
both directions (`&0xFFFFFFF0` fix-up below zero, `neg/shl 4` fold above
`0xF`), and returns `word[rdx + (index+2)*36]` — a 9-word ring element.
Interior anchor `0035EF1E` (the `imul 0x294`).

## SWE2-EC7-34 update (2026-09-19) - `003745C0`

`003745C0` (868 B) is the frame-boundary init - a `00358320` version read compared against `byte[rbx+0x1D]`, the `02AE9628` float store, `02AEECF0`/`01EFAC20` records, `003A35E0`/`003748DD`/`0037476B`/`003746B9`/`003746AB`/`0017FFD0`. Interior anchor `003745C9` (the `00358320` call).

## SWE2-EC7-35 update (2026-09-19) - `00374280`

`00374280` (823 B) is a frame-boundary sibling - `movzx byte[rbx+0x1D]` version read like `003745C0`, float stores into `02AE9628`/`02AE9730`/`02AE9820`/`02AE9910`, `003A35E0`/`00358320`. Interior anchor `00374289` (a call site).

## SWE2-EC7-35 update (2026-09-19) - `0024CBE0`

`0024CBE0` (715 B) is a between-frames helper - `02092640`/`02092638` state, `0xfffffffe64122d00`/`0x664122d00` mask constants, then two each of `00375900`/`00358780`/`00358720`/`003586E0`/`00358670`/`00358610` plus `00861EC0`. Interior anchor `0024CC25` (an `00861EC0` call).

## SWE2-EC7-35 update (2026-09-19) - `003AB500`

`003AB500` (698 B) is the sibling helper - `009155F0` rdata, the `0xffffffe03fffffff` mask, three `00375900` plus the same `003586xx`/`003587xx` helper run. Interior anchor `003AB555` (a `00375900` call).

## SWE2-EC7-36 update (2026-09-19) - `00251010`

`00251010` (665 B) is a between-frames helper - `01CEBB70`/`01CEBBA8`/`0208F570`, `00375900`/`00182B40` pairs plus `0036C1D0`/`0036C140`/`00808C40`. Interior anchor `00251070` (a `00375900` call).

## SWE2-EC7-36 update (2026-09-19) - `003B5980`

`003B5980` (629 B) is a between-frames sibling - `01CEBBA8`/`01CEBD80`/`01EF93F0`/`01EF93FC`, `00861F14`/`00421FF0`/`003E6F70`/`0036DD80`. Interior anchor `003B59E2` (an `00861F14` call).

## SWE2-EC7-37 update (2026-09-19) - `0017ED50`

`0017ED50` (518 B) is a between-frames body - `01F7F550`/`01F7F560`/`01F7F570`/`01F7F558` fields, `0017E7E0` quadruple plus `00189120`. Interior anchor `0017EDCB` (an `00189120` call).

## SWE2-EC7-37 update (2026-09-19) - `00184460`

`00184460` (505 B) is the viewport rect mapper the page names - PS2 reference coords to device pixels, `008C5B38`/`01CEBB70`, `001DDAB0` octuple plus `001DD110` triple and `00189120`/`001DD8C0` pairs and `001B1620`/`00186AA0`/`00186A90`. Interior anchor `0018448A` (an `001B1620` call).

## SWE2-EC7-37 update (2026-09-19) - `00375B90`

`00375B90` (500 B) is a between-frames sibling - `02EBEFF0`/`02EBEFC0`, `003A22A0` triple plus `002D7F20`/`003A1DB0` pairs and `00358320`/`002D7E00`/`002D7D50`. Interior anchor `00375BAA` (a `00358320` call).

## SWE2-EC7-38 update (2026-09-19) - `00375280`

`00375280` (496 B) is a between-frames body - `01F44830`/`02AE9A50`/`0047A9C0`, `00358320`/`003A35E0`/`00808C40`. Interior anchor `003752A9` (a `00358320` call).

## SWE2-EC7-38 update (2026-09-19) - `003740B0`

`003740B0` (454 B) is a between-frames sibling - `020926E4`/`01CEBBA8`/`01EFAC20`, `00254A70`/`002EF9F0`/`003583F0`/`00358320`/`00863B40`/`00863B90`. Interior anchor `003740B9` (a `00254A70` call).

## SWE2-EC7-39 update (2026-09-19) - `002F1A90`

`002F1A90` (433 B) is a between-frames body - `01DFE0B4`/`022BE7C8`, `001EDDA0` triple plus `002E1C20`/`00358720`/`00358780`/`00374D40` pairs and `002F16B0`/`003587B0`. Interior anchor `002F1AD4` (a `002E1C20` call).

## SWE2-EC7-39 update (2026-09-19) - `00374E30`

`00374E30` (411 B) is a between-frames sibling - the `02AE8BE8`..`02AE8C3C` dword block, `00358320`/`003A35E0`. Interior anchor `00374E39` (a `00358320` call).

## SWE2-EC7-40 update (2026-09-19) - `003B4E50`

`003B4E50` (378 B) is a between-frames sibling - `022C6F28`/`02B40508`..`02B40514` byte fields, `003E6AA0` pair. Interior anchor `003B4EF2` (a `003E6AA0` call).

## SWE2-EC7-42 update (2026-09-19) - `00377230`

`00377230` (301 B) is a frame body - `02ADBFC8`/`02F97348`, `001EDDA0`/`002F3860`/`0024C060`/`0024D4E0`/`0024D770`/`0046EDD0`/`00465690`/`0047BD30`/`00464BD0`. Interior anchor `0037726E` (an `001EDDA0` call).

## SWE2-EC7-42 update (2026-09-19) - `00375D90`

`00375D90` (299 B) is a frame body - `02AE9518`/`02AE951C`/`02AE9528`/`02AE954C`, `00358320`/`003A35E0`. Interior anchor `00375D99` (a `00358320` call).

## SWE2-EC7-44 update (2026-09-19) - `0036FBB0`

`0036FBB0` (268 B) is the draw-mode bit-0 bank body - `003B4E50`/`003B5340` (the `02B405xx` bank readers the page names). Interior anchor `0036FBB4` (a `003B4E50` call).

## SWE2-EC7-44 update (2026-09-19) - `00370CD0`

`00370CD0` (269 B) is a battle-stats-adjacent body - `0020E600`/`00409270`. Interior anchor `00370CE7` (a `0020E600` call).

## SWE2-EC7-44 update (2026-09-19) - `00373540`

`00373540` (256 B) is a body - `0020E600`/`00409250`/`00409270`. Interior anchor `00373555` (a `0020E600` call).

## SWE2-EC7-44 update (2026-09-19) - `00370BD0`

`00370BD0` (254 B) is a body - `0020E600` single call. Interior anchor `00370BE5` (the `0020E600` call).

## SWE2-EC7-45 update (2026-09-19) - `00376220`

`00376220` (243 B) is a body - `00358320`/`0036F2C0`/`0036F2F0`/`0039D0C0`. Interior anchor `00376243` (a `00358320` call).

## SWE2-EC7-46 update (2026-09-19) - `001AA2C0`

`001AA2C0` (228 B) is a call-free float ramp integrator - `(target - 1.0f) * pi/2` per-frame step divided by `cvtsi2ss(01DFE0B4)` and scaled by `+0x330`, accumulating into `+0x30C`/`+0x310` with `comiss` wrap clamps at 0.0f/1.0f. Interior anchor `001AA2D1` (the `+0x2E8` load).

## SWE2-EC7-47 update (2026-09-19) - `004ECB70`

`004ECB70` (216 B) is a body - `call r11` register calls only. Interior anchor `004ECC1D` (the first register call).

## SWE2-EC7-49 update (2026-09-19) - `005379D0`

`005379D0` (194 B) is a call-free float-threshold flag builder - `ucomiss` on each of `[rdx]`..`[rdx+0xC]` vs `xmm2`, accumulating per-component equal/below flags with `jp` NaN handling. Interior anchor `005379DA` (the first `ucomiss` pair).

## SWE2-EC7-49 update (2026-09-19) - `0035B8D0`

`0035B8D0` (192 B) is a body - `001848E0`/`002E1C40`/`002E1CD0`/`00358560`/`00358580`/`003585B0`/`00358650`/`00358670`. Interior anchor `0035B8D6` (an `001848E0` call).

## SWE2-EC7-49 update (2026-09-19) - `00358450`

`00358450` (190 B) is a call-free bit-field packer into `022C7F90[ecx*4]` - `dx & 1` parity plus `0xFFF9`/`0xFFE1`/`0xFFFB`/`0xFFC1`/`0xFF83`/`0xFF05` mask folding builds the packed word; `or word[..+2], 0xF`. Interior anchor `00358462` (the `+2` OR).

## SWE2-EC7-51 update (2026-09-19) - `002F1950`

`002F1950` (172 B) is a body - `002E1CA0`/`00358580`/`003585B0`/`00358610`/`00358670`/`003586E0`/`00358720`/`00358780`. Interior anchor `002F1959` (a `002E1CA0` call).

## SWE2-EC7-52 update (2026-09-19) - `00464BD0`

`00464BD0` (828 B) is a frame body - `003B42B0`/`003B4770`/`0042FDB0`/`00431D30`/`003A2B20`/`002F1F40` plus `02F97348`. Interior anchor `00464C18` (a `003B42B0` call).

## SWE2-EC7-55 update (2026-09-19) - `0017E7E0`

`0017E7E0` (255 B) is a call-free 4x4 matrix-vector transform - `[rcx]`-`[rcx+0x3C]` rows against `[r8]`/`[r8+4]`/`[r8+8]`, dot products into xmm5-xmm8. Interior anchor `0017E82B` (the `[rcx+0x10]` row multiply).

## SWE2-EC7-56 update (2026-09-19) - `00374D40`

`00374D40` (234 B) is a between-frames body - `00182B40`/`00375900` plus `01CEBBA8`/`02ADB6D0`/`02ADB6D8`/`02EC07F0`. Interior anchor `00374DE1` (a `00182B40` call).

## SWE2-EC7-62 update (2026-09-19) - `0018BD30`

`0018BD30` (150 B) is one of the four identical pass arms - `0018B4E0`/`001AB570`/`001F1980`/`0085E730`. Interior anchor `0018BD53` (a `0085E730` call).



## SWE2-EC7-65 update (2026-09-19) - `003A35E0`

`003A35E0` (137 B) is an emit variant - `001DB840`/`0020E680`. Interior anchor `003A3604` (a `0020E680` call).


## SWE2-EC7-73 update (2026-09-19) - `003A4220` three-resolver chain measured

`003A4220` (99 B) is the resolver chain the frame bodies call: on the
`02F97348` singleton, `word[+0x36A] & 0x7000 == 0x3000` tries
`0036E620(ecx)` first; `byte[rcx] == 2` falls to `0036E4B0`; finally
`0036E4E0` - any nonzero result tails `002E9B80`, all-zero returns -1.
Interior anchor `003A424A` (the `0036E620` first try).

## SWE2-EC7-74 update (2026-09-19) - `00368AA0` + `00365990` flag and gated init measured

`00368AA0` (27 B) is the `02EC0B39` bit setter: `al = 1 << cl`, `edx`
nonzero ANDs `~al` (clear), zero ORs `al` (set) - the indexed flag bit
the frame bodies toggle.
Interior anchor `00368AAD` (the `and` clear arm).

`00365990` (81 B) is the gated init pair: when `022CBE00`'s `+0x240`
bit `0x40000000` is set it runs `0039BD50(0x34E0)` then
`00474600([rcx+0x190], 0x3500, 0, [+0x244] via stack, 0x10)` - the
two-call table provision behind one flag.
Interior anchor `003659D7` (the `00474600` provision call).

## SWE2-EC7-98 update (2026-09-20) - `002E05C0` measured

`002E05C0` (23 B) is the inverted predicate `0022B8C0`,
`00267720`, `0026DFB0` and `0050D1E0` call: `00253C20` runs
and the return is `eax == 0` - the negated availability gate
the frame's consumers consult.
Interior anchor `002E05C4` (the `00253C20` call).

## SWE2-EC7-113 update (2026-09-21) - `00863B40` measured

`00863B40` (78 B) is the
`02EB37F8` singleton
constructor `003740B0`
runs: `0016D6A0(1)` first,
then 0x70 bytes through
`001A1470` on the
`01F7F4C0` allocator, the
`01CCFAB0` vtable installed
on success (slot 0 is
`0016D6A0` itself), the
object parked in the global,
and `object + 0x10`
returned - zero on
allocation failure.
Interior anchor `00863B6E`
(the vtable install).

`008635F0` (17 B) is the
`0035EA40`-called IAT
forwarder: the import at
`008C21B0` (`01CCC316`)
runs unconditionally and
zero returns - the
smallest shape in this
family.
Interior anchor `008635F4`
(the IAT call).

`005A0820` (22 B) is the timestamp helper `0035EA40` (`TkSyncVEmulationThread`) calls: `005CC930` reads the performance counter and the result has `02CB60E8` (the captured base tick) subtracted as a `double` — an elapsed-time query, not a deadline test; the caller compares the delta against its sync budget.

Interior anchor `005A0829` (function `005A0820`).

`004640A0` (804 B) is the frame body `00377230` calls: `00861EC0`, `003ABD00`, `004309C0`, `002F31C0`, `00431D30`, `003A2B20` x3, `0039AF70`, `00398F90`, `002F1F40`, `003A4220`, `003590D0`, `002E9B80`, `003A3FD0`, `003AB960`, `003AC920`, `004643D0` and `00464650` under the cookie check - the frame step's widest helper fan-out.

Interior anchor `004640FE` (function `004640A0`).

`00464650` (839 B) is the frame body `004640A0` calls: `00861EC0`, `003ABD00`, `002F31C0`, `00431D30`, `003A2B20` x3, `00398480`, `0039AF70`, `00398F90`, `002F1F40`, `003A4220`, `003590D0`, `002E9B80`, `003A3FD0`, `003AB960` and `003AC920` under the cookie check - the fan-out's second stage.

Interior anchor `0046468E` (function `00464650`).

`003AC920` (311 B) is the parameter stage the frame bodies `004640A0`, `004643D0` and `00464650` all call (a boot-time pass seeds it too): `byte[rcx]` selects 2/3/4/5 - `1/x^2` reciprocals into `+0x30`/`+0x40`/`+0x48`, or the full vector-length path writing `+0x30`/`+0x34`/`+0x38`/`+0x3C`/`+0x48`/`+0x4C` - the frame's interpolation parameter computer, call-free.

Interior anchor `003AC954` (function `003AC920`).

`004643D0` (637 B) is the build-or-dispatch step the frame body `004640A0` calls (the `003AC920` parameter stage is its callee): `dword[+0x244] == 0` builds the `word 0x8006`/`|0x80` stack record after `00861EC0` with the `02F97348` byte class selecting flag bits, otherwise `002E9B80`/`002F1F40`/`002F31C0`/`003590D0`/`003A2B20`/`003A3FD0`/`003A4220`/`003AB960`/`003ABD00`/`003AC920`/`00431D30` run the dispatch - the frame's state-gated emit.

Interior anchor `00464415` (function `004643D0`).

`003B4160` (329 B) is the handle-slot issuer `00464BD0` calls: scans the `02B404E0` table (64 entries x 0x60) for a zeroed slot, `00181DD0` allocates, serial `02B404C4` increments (wraps at 0xFFFFFF) and packs `(serial<<8)|slot` into `[rbx]` as the handle; a `001EDDA0` gate doubles `word[rsi+0xA]`, then float fields fill the record - the frame's packet-slot allocator.

Interior anchor `003B41C1` (function `003B4160`).

`00376AC0` (276 B) is the fade-weighted vector write `00376470`'s per-record batch calls: `xmm3 = 1 - [rcx+0x40] x [rcx+0x30] x [rcx+8]` attenuates the `020926C0`/`020926C4`/`020926C8` global triple, `003AC900` runs, and when `dword[rbx+0x50]` is nonzero `003ABD00`'s slot takes `{+0x60,+0x64,+0x68}` into `+0x20..+0x28`, `01F004E0`'s float into `+0x40` and `1.0f` into `+0x44`; `xmm6 = min(1.0f, [rbx+8] x 1.5) x [rbx+0x30]` above the `01CEBB60` epsilon scales `{+0x44,+0x48,+0x4C}` into `+0x10..+0x18` with `byte[+7] &= ~2` and `+0x1C = 1.0f`, else `byte[+7] |= 2` - the weight crossfade between the frame's global basis and the record's own vector.

Interior anchor `00376B3B` (function `00376AC0`).

`00332590` (42 B) is the character-render-array binder the frame helpers call: `lea rcx,[022C6F30]` then `[022C6F20] = rcx` installs the record object, `0041E500` and `00426950` run the two setup halves, and `jmp 003697C0(ecx=6)` tail-enters the six-slot stage - the `022C6F20`/`022C6F30` pair's initializer.

Interior anchor `003325A2` (function `00332590`).

`00375F80` (206 B) is the lane flush `002F1950` runs mid-frame: `0024B240` releases and nulls `[02ADB6D0]`, then for each of the three lane counters at `02EC07F0..+8` it scans the 32x`0x70` record table at `02EBFA48` for a `+0`-keyed match and `rep movsq`-compacts the slot's tail up one record, zeroing `02EC07D8` and the lane count; `02ADB6D8` clears at the end - the frame's dead-lane compaction

Interior anchor `00375FE0` (function `00375F80`).

## Interior citations for the entry-cited functions (OPUS, 2026-10-01)

*Functions this page named only at their entry. Each was read from the certified image; the sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. `003ACA60` is not here: its whole work is the entry instruction. Verified by [`twoframes_interior.py`](../../_index/candidates/opus-twoframes-interior-1001/twoframes_interior.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0017F070` | 52 B | once: while byte `01F7F50C` is 0 and `0018CA40()` is non-null, sets the byte to 1 and tail-calls `0018C580` on that object | `0017F074`, `0017F087`, `0017F09A` |
| `0017F330` | 63 B | when `0018CA40()` and `001A9930()` are non-null and `001A94B0(001A9930())` is true, tail-calls `0018BB70(0018CA40())` | `0017F350`, `0017F355`, `0017F365` |
| `001809E0` | 66 B | when `001A9930()` is non-null and `001A94B0` on it is true, calls `001A5A70` on it, then tail-calls `001AA2C0` on it | `001809F6`, `00180A07`, `00180A18` |
| `00180A30` | 61 B | when `001A9930()` is non-null and `001A94B0` on it is true, calls `001A8F80` on it; in every case then tail-calls `0018C2A0(0018CA40())` | `00180A46`, `00180A57`, `00180A68` |
| `00182410` | 36 B | returns byte `+0xDB9` of the object `00189120()` returns, or 0 when there is none | `0018241E`, `00182423` |
| `001826E0` | 67 B | when `00189120()` is non-null, tail-calls `0018B970(0018CA40(), [00193D50() + 0x2B8], 0, 0)` | `001826F8`, `00182707`, `00182719` |
| `00182730` | 74 B | when `00193D50()` is non-null, calls `001944D0` on it with every other argument 0 or 0.0 | `00182743`, `00182757`, `00182770` |
| `00183120` | 43 B | when `005C5230()` is non-zero, tail-calls `0018CB30(0018CA40(), ecx)` | `00183128`, `00183139`, `00183140` |
| `00184900` | 70 B | with `0018CA40()` present: when `005C5230()` is non-zero and `0017D8B0()` is not 2, sets dword `+0xC30` of `00189120()` to 3; then tail-calls `0018C860(0018CA40())` | `0018491C`, `00184926`, `0018493C` |
| `001863F0` | 30 B | tail-calls `0018BD30(0018CA40(), dl)` | `001863F9`, `00186409` |
| `001A1460` | 9 B | copies qword `+8` to `+0x18` | `001A1464` |
| `001A5A70` | 15 B | copies qword `+0x90` to `+0x98` | `001A5A77` |
| `00229F20` | 110 B | when dword `01FD49E8` is non-zero: marks `"AO render"` (`001EB150`), runs `0017F670(1)` and `001826E0`; when it is still non-zero and the argument is non-zero, marks `"Water effect"` and runs `0017F330`, `00180A30`, `001EB110` and `001826E0`; then `0017ECF0` and a tail call to `001EB110` | `00229F38`, `00229F47`, `00229F60`, `00229F79`, `00229F83` |
| `0022A490` | 30 B | stores `edx` in dword `02064AA0`, then increments byte `02064AD0` when `0022A580()` is non-zero | `0022A49A`, `0022A4A3` |
| `002385D0` | 102 B | for a group index up to `0x1B`, reads the signed loader id from the byte table `01E09F68`; when it is not negative, calls `008478A0(id)` and returns `00384420(id, rdx, 00914698, that result, 8, 4)`; otherwise 0 | `002385E8`, `002385FA`, `0023861E`, `0023862E` |
| `0024B240` | 43 B | appends `rcx` to the 256-qword array at `02091950` and increments the word count `0209216A`; at 256 entries it tail-jumps to `00182CA0` instead | `0024B24F`, `0024B25F`, `0024B263` |
| `00253C20` | 45 B | returns 1 when `0035D050()` is non-zero and dword `02092730` is 0 or 3, else 0 | `00253C24`, `00253C2D`, `00253C37`, `00253C3C` |
| `0026E1A0` | 36 B | multiplies the four 16-byte float vectors `0209A380`, `0209A370`, `0209A390` and `0209A3C0` lane by lane and stores the product at `0209A3B0` | `0026E1A7`, `0026E1B5`, `0026E1BC` |
| `002D7F20` | 119 B | returns entry `ecx` of an eleven-dword table built on the stack (the eight dwords at `00917230`, then `0x100`, `0x200`, `0x400`); 0 when `ecx` is above 10 | `002D7F43`, `002D7F66`, `002D7F82` |
| `002F3860` | 41 B | stores into qword `02F97348` either `[[rcx+8]+0x10]` or, when byte `[rcx]` is `0xF0`, `[rcx+0x18]`; then tail-jumps to `0024ED80` | `002F3863`, `002F386D`, `002F387D`, `002F3884` |
| `0033FA20` | 21 B | calls `0035B8D0`, then tail-calls `0016D6A0` with `xmm0` = 0.0 | `0033FA24`, `0033FA29`, `0033FA30` |
| `00353260` | 102 B | reads three values from `00267E10` on argument 4; when the byte at `02099011 + 0x288 * (byte +0x15 of argument 2)` is 0 (a 22-byte table read), calls `002F1A90(third, second, first)` | `0035327D`, `0035329C`, `003532AC` |
| `0035B7D0` | 105 B | a fixed call sequence: `00358750(0, 1)`, `003586E0`, `00358580`, `00358670`, `003585B0` (each with 0, 0), `003586C0(0)`, `00358560(0)`, `002E1CD0(0, 0)`, `002E1C40(0, 4)`, `00368AA0(0, 0)`, then a tail call to `001848C0` | `0035B7DB`, `0035B816`, `0035B822`, `0035B834` |
| `0035EDE0` | 112 B | returns a mask: for each of bits 0-15 that is set in `edx`, reads the signed byte at `022CB114 + 0x294*ecx + bit`, and when it is not negative sets that bit number in the result | `0035EDF5`, `0035EE1F`, `0035EE2E`, `0035EE42` |
| `00368AE0` | 18 B | calls a 61-byte helper with the sign-extended argument, then `00368B00`; it does not return (an `int3` follows) | `00368AE4`, `00368AE7`, `00368AEC` |
| `00368C10` | 88 B | an endless loop over slot `[rcx]` (byte): calls a 61-byte helper with qword `022D7F68 + 8*slot`, calls the function pointer at `022D7F70 + 8*slot` when it is set and clears it, then calls a 31-byte import wrapper on (dword `022CFEF4` + 4*slot, 0x24) | `00368C38`, `00368C4A`, `00368C59`, `00368C61`, `00368C66` |
| `0036E810` | 104 B | when `ecx` is non-zero, passes a stack record {mode 2 when `edx` is 1 else 1, byte `r8b`, float `xmm3`} to `0024FAE0`; otherwise calls `0024FA40` | `0036E83B`, `0036E841`, `0036E84A`, `0036E861` |
| `0036F410` | 28 B | calls `0026E1A0` and `003ECE60`, then tail-calls `003ED7F0(1)` | `0036F414`, `0036F419`, `0036F427` |
| `003769E0` | 15 B | copies the 16 bytes at `020926C0` to `0209A380` | `003769E7` |
| `003A1E10` | 62 B | calls `004FE420(02EBEFC0, rcx, edx)`, then tail-calls `004FE420(02EBEFD8, rcx, rcx + edx)` | `003A1E2C`, `003A1E31`, `003A1E49` |
| `003ACA70` | 9 B | clears the bits of `cl` in byte `02B3F520` | `003ACA72` |
| `003B4770` | 30 B | indexes the 96-byte records at `[02B404E0]` by `cl`; returns the record plus `0x20` when its dword `+0` equals `ecx`, else 0 | `003B4777`, `003B477B`, `003B4782`, `003B478B` |
| `003B6B80` | 28 B | indexes the `0xE0`-byte records at `[02B40528]` by `cl`; when the record's dword `+0x10` equals `ecx`, stores `xmm1` at `+0x14` | `003B6B83`, `003B6B91`, `003B6B96` |
| `003E6F70` | 17 B | tail-jumps to `003E56A0` when qword `+0x400` is non-zero, else returns 0 | `003E6F78`, `003E6F7E` |
| `00425DC0` | 78 B | calls `0051D1D0`, then walks the `0x740`-byte records of `[022C6F28]` from the index in dword `+0x48800`, calling `003E6680` on each and following its word `+4` until -1 | `00425DC4`, `00425DE3`, `00425DEE`, `00425DFA` |
| `004264A0` | 88 B | stores in word `+0x4882C` of `[022C6F28]` the value `002E9B80(003590D0())`, or -1 when `003590D0()` is 0; then calls `00425FB0(0042D050, 0042CBF0, [022C6F28])` and tail-jumps to `00428980` | `004264AF`, `004264BB`, `004264CE`, `004264EA`, `004264F3` |
| `00428E40` | 48 B | when byte `+0x48842` of `[022C6F28]` is 1 and byte `+0x48843` is 0, calls `00426420` and tail-calls `00521440` | `00428E4B`, `00428E54`, `00428E5D`, `00428E66` |
| `0046EDD0` | 89 B | for id `+0xC`: when `0035B240(id)` has any bit other than bit 2, reads an integer through a 409-byte reader, divides it as a float by the constant at `00906A44`, passes it to `0035B550` and returns 1; otherwise calls a 158-byte Input-layer body on id and returns 0 | `0046EDE1`, `0046EDF0`, `0046EE01`, `0046EE09`, `0046EE1C` |
| `00474600` | 75 B | builds a stack record {16 zero bytes, the 24-byte entry `02EBEFC0 + 24*[02EBEFF0]`} and passes it with `rcx` and its fifth argument to `003A22A0`, then calls `003A1DB0` | `0047461D`, `0047462C`, `0047463C`, `00474641` |
| `00475390` | 31 B | when dword `02EBA4C0` is non-zero and dword `02EBA4D0` is 0, tail-calls `00474710(02EBA4C0)` | `00475399`, `004753A2`, `004753A9` |
| `00504490` | 20 B | calls `0016D6A0(0)`, then tail-calls `003A1DB0` | `00504494`, `00504496`, `0050449F` |
