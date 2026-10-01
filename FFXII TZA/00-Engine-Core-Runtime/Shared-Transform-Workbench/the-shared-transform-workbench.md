---
system: The shared transform workbench — a matrix area four subsystems pass arguments through
category: 00-Engine-Core-Runtime
status: AUDITED
owner_layer: none — established here, not assumed
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN160 -> GN161 - the records this document rests on are unchanged except for `00248A90`, which gained a plate comment and CodeDomain tags in batch R109 and lost nothing; voided by any delta that removes or rewrites a comment, tag, name, prototype or body range; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
audit:
  passes: 1
  last_pass: 2026-09-02
  last_pass_state: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  crossref_clean: true
  reopened_count: 0
origin: BQ-13 — found while auditing B-4; a relationship class the call graph cannot see
---

# The shared transform workbench

> **249 functions write one 1.5 KB area of memory, and almost none of them call each other.**
> They meet only at the buffer. This documents what is in it, and answers the question that
> mattered: is this shared scratch, or does one subsystem own it and the rest borrow?

> **IDENTIFIED 2026-09-14 (FABLE): the area is the register bank of the PS2 assembly emulation.** It holds the EE
> general-purpose registers (`022D8F10 + 16·k`, `$zero` never written), HI / LO (`022D9110` / `022D9120`), and the VU0
> CLIP flag (`022D9130`), Q (`022D9198`), ACC (`022D91A0`) and 31 vector rows (`022D91B0`–`022D939F`). vf00 is the
> constant at `01EF93F0` that BQ-20 read. Translated PS2 assembly writes its operands into these registers, which is why
> the measurements below look like a memory calling convention. Each register is tested at instruction level, and a
> census of 267 functions is given, on [the EE and VU0 register bank](the-ee-and-vu0-register-bank.md). BQ-16 (no
> matrix division: the rows are registers) and BQ-19 (registers are volatile) are answered there. The ledger mirror is
> pending.

**Neither, exactly.** It is an **argument-passing area** — a memory calling convention for a family
of shared matrix routines. Nobody owns it because almost nothing survives in it long enough to be
owned.

## 1. What the player sees

Every frame, FFXII has to answer the same question thousands of times: *given this thing, where does
it end up on screen?* A character's hand, a shadow, a spell effect, the camera itself — each is a
position and an orientation that has to be combined with several others before anything can be drawn.

The combining is done with matrices, and the engine keeps a **workbench** for it: a fixed slab of
memory holding a row of them. Code that needs a transform done writes its numbers into the workbench,
calls a shared routine, and reads the answer back out.

What makes it worth a document is *who* uses it. Graphics code, obviously. But also the sound code —
because positional audio needs to know where the listener is facing — and character code, and
movement. Four different parts of the game, sharing one workbench, none of them owning it.

For a modder that has one blunt consequence. **The workbench is not yours and it is not empty.** If
you hook something that uses it and leave your numbers behind, the next caller — which may be the
sound system — picks up your matrix instead of its own. Nothing crashes. Things just end up in the
wrong place.

## 2. Native mechanism

### 2.1 Where it is, and that it starts empty

The area is `022D8F00`–`022D9500` in `.data`, and it is **past the end of the section's file image**:
`.data` has raw bytes only up to VA `01F7E400`. So the workbench has **no initial contents** — it is
zero-filled at load and everything in it is built at run time. There is no static layout to read; the
structure has to come from the code that touches it.

### 2.2 It is an array of 16-byte rows, and that is provable

Of every address in the region accessed 16 bytes wide — the width of an SSE register, one matrix row
— there are **46, and all 46 are 16-byte aligned.** The alignment histogram is `{0: 46}`, with no
exceptions. A region that merely happened to hold floats would not do that.

### 2.3 One matrix, proven by the code that copies it

`003970A0` is 44 bytes and does nothing else:

```asm
003970A0  movups xmm0, xmmword ptr [rip + 0x1F42109]   ; -> 022D91B0
003970A7  movups xmmword ptr [rcx], xmm0               ;    dst + 0x00
003970AA  movups xmm1, xmmword ptr [rip + 0x1F4210F]   ; -> 022D91C0
003970B1  movups xmmword ptr [rcx + 0x10], xmm1        ;    dst + 0x10
003970B5  movups xmm0, xmmword ptr [rip + 0x1F42114]   ; -> 022D91D0
003970BC  movups xmmword ptr [rcx + 0x20], xmm0        ;    dst + 0x20
003970C0  movups xmm1, xmmword ptr [rip + 0x1F42119]   ; -> 022D91E0
003970C7  movups xmmword ptr [rcx + 0x30], xmm1        ;    dst + 0x30
003970CB  ret
```

**Four consecutive rows at `022D91B0`, copied out as one contiguous 64-byte block.** That is a 4×4
matrix, and it is the engine's own statement of the fact — not an inference from address adjacency.
`022D91B0` is also the most-used four-row base in the region: **41 four-row access sequences by 19
functions**, more than any other.

**What is *not* proven:** that the rest of the area divides into further 64-byte matrices on a clean
stride. Rows are accessed in runs of 4, 6, 8 and more, and a sliding window over a long run produces
apparent "bases" 16 bytes apart. ~~**One matrix is established; the rest of the area is an array of
16-byte rows whose grouping is open** (BQ-16).~~ *Superseded 2026-09-26 (FABLE, Claude Opus 5.5): **BQ-16** was answered on 2026-09-14. The rows do not divide into matrices: `022D91B0`–`022D939F` are VU0 vector registers, and a "matrix" is whatever four registers a routine loads (the banner at the top of this page).*

### 2.4 The initializer

`0036D9E0` (918 B) writes **80 slots and reads none** — the only function in the region with that
shape. It is a bulk clear, written as pairs of qword stores walking the rows in order:

```asm
0036DA05  mov qword ptr [rip + 0x1F6B7A8], 0   ; -> 022D91B8
0036DA10  mov qword ptr [rip + 0x1F6B795], 0   ; -> 022D91B0
0036DA1B  mov qword ptr [rip + 0x1F6B7A2], 0   ; -> 022D91C8
0036DA26  mov qword ptr [rip + 0x1F6B78F], 0   ; -> 022D91C0
            ...  continuing through 022D9428
```

Two qwords per 16-byte row, high half then low half, straight through the area. It also sets a small
header outside the region (`01EF93FC` from a constant, `01EF93F0`/`01EF93F4` zeroed).

**The initializer carries no owner tag.** Whatever lifecycle authority the workbench has sits in an
unowned function.

### 2.5 The decisive question: is it state, or is it arguments?

State is written by one party and read back by another later. Arguments are written and read by the
same party in the same breath. The region answers plainly:

| measurement | result |
|---|---|
| functions touching the matrix rows | **216** |
| of those, functions that **write** | **215** |
| of those, functions that only **read** | **1** |
| owner categories that write rows | Presentation, Audio, Movement, ActorEntity, UI |
| owner categories that only read rows | **none** |

**Every subsystem that touches the workbench writes to it before reading.** The single exception is
`003970A0`, the getter in §2.3 — one function in the whole image consumes a matrix it did not write.

Across the wider region, 18 functions read without ever writing, and **16 of those read only two
slots**, `022D94B0` and `022D94B4`, always 8 bytes wide and never as floats. Those two are pointers,
not matrix data, and no RIP-relative store to them exists anywhere — they are written through a
register. They are a separate object that happens to live in the same page.

So the pattern is: **write your operands into the shared rows, call the shared routine, read the
result back.** That is a calling convention implemented in memory. It is the same shape as the
verb-to-verb hand-off in the ScriptVM — where one script verb's handler pushes its arguments onto the
operand stack for another verb's handler to pop — and it is what you would expect from an engine
whose ancestor passed matrices through fixed vector-unit register banks.

### 2.6 Does Presentation own it after all?

It is the obvious suspicion, and it does not survive.

| owner | functions writing the region | slots written |
|---|---:|---:|
| Presentation | **144** | 235 |
| Audio | 4 | 41 |
| ActorEntity | 1 | 29 |
| Movement | 2 | 1 |
| UI | 1 | 6 |

Presentation dominates *use* — but use is not ownership, and this database may not infer one from the
other. The three tests that would establish ownership all fail:

1. **Does another subsystem keep its own sub-area, which would make this several objects with several
   owners?** No. ActorEntity, UI and Movement write **zero** slots that Presentation does not also
   write. Audio writes just **four** (`022D8F20`, `022D9130`, `022D9133`, `022D9478`). They are using
   the same rows, not neighbouring ones.
2. **Does Presentation hold the lifecycle?** No. The only whole-area initializer, `0036D9E0`, is
   unowned.
3. **Does anything persist for an owner to hold?** Essentially not. One function in the image reads a
   matrix row it did not write.

**Verdict: no owner, and "shared scratch" undersells it.** It is a shared *parameter area*, which is
why it has no owner: there is no transaction to own.

## 3. Key addresses

Addresses are Ghidra image base `0x00120000`.

| Address | Working name | Body | Role |
|---|---|---:|---|
| `0036D9E0` | workbench clear | 918 B | writes 80 slots, reads none — the only initializer; **unowned** |
| `003970A0` | matrix 0 getter | 44 B | the one function that reads a matrix it never writes |
| `00361DE0`, `00362230`, `003623C0`, `00363FD0` | the four Audio users — **the spatial-source closest-point helpers of the listener update (BQ-18, 2026-09-12)** | — | write 11–28 slots each and read fewer: the slots `022D92A0`–`022D9318` are their vector temporaries, the accumulator `022D91A0`/`022D9198` their dot-product scratch |
| `0025C830` | the ActorEntity user | — | writes 29 slots, reads 24 |
| `0035DCC0` | the UI user | — | writes 6, reads 3 |
| `00230790`, `0032A6E0` | the Movement users | — | one slot each, `022D91B0` — matrix 0's first row |

Addresses are Ghidra image base `0x00120000`. **Every row above is a function.**

### Data addresses cited by this document

These are `.data` BSS regions, not functions; the byte counts are **region extents, not body
sizes**, and this block carries no body-size column for that reason.

| Address | Name | Kind | Contents |
|---|---|---|---|
| `022D8F00`–`022D9500` | the transform workbench | BSS region, 1,536-byte | BSS; 315 addresses touched, 249 writers, 251 readers |
| `022D91B0` | **matrix 0** | BSS region, 64-byte | proven 4×4 by `003970A0`; the most-used four-row base (41 sequences, 19 functions) |
| `022D91A0`–`022D939F` | the row array | BSS region, 512-byte | 32 aligned 16-byte rows, accessed in runs |
| `022D8F90`–`022D900F` | second row block | BSS region, 128-byte | 8 aligned rows, 2 Presentation functions |
| `022D8F30`–`022D8F6F` | third row block | BSS region, 64-byte | 9 functions, 14 four-row sequences |
| `022D94B0`, `022D94B4` | two pointers | BSS region, 8-byte each | read by 16 functions in the `0036Dxxx`–`0036Exxx` family, never RIP-written |

## 4. Data structures and formulas

```
transform workbench        022D8F00 .. 022D94FF        1,536 B, BSS (no file image)

  proven:
    022D91B0  float[4][4]  matrix 0      -- 003970A0 copies rows +0x00 +0x10 +0x20 +0x30
                                            into a 64-byte destination
  row array (grouping beyond matrix 0 unproven, BQ-16):
    022D91A0 .. 022D939F   32 rows x 16 B, every SSE access 16-byte aligned (46/46)
    022D8F90 .. 022D900F    8 rows
    022D8F30 .. 022D8F6F    4 rows
  separate objects in the same page:
    022D94B0   void*        read 8 bytes wide by 16 functions, never RIP-written
    022D94B4   void*        same
    022D9138   u32          RNG enable/mode - see rng-streams.md, NOT part of the workbench
```

The clear, written out exactly as `0036D9E0` performs it:

```c
for (row = 022D91B0; row < 022D9428; row += 16) {
    *(u64 *)(row + 8) = 0;      /* high half first */
    *(u64 *)(row + 0) = 0;
}
```

**Object boundaries were derived from writer sets, not from address adjacency.** Two slots belong to
one object when the same functions touch them; adjacency proves nothing and is banned as evidence in
this database. Under that rule the page holds **62 objects**, not the 13 an adjacency-only coalescing
reports (§10).

## 5. Call chain

There is no call chain. That is the point of the document.

```
144 Presentation functions ─┐
  4 Audio functions         ├─ WRITE ─> 022D8F00..022D9500 ─ READ ─> the same functions
  1 ActorEntity function    │            (the workbench)
  1 UI function             │
  2 Movement functions      ┘
 97 unowned / CodeDomain functions

              0036D9E0 ── clears the whole area, reads nothing (unowned)
              003970A0 ── reads matrix 0 without writing it (the only such function)
```

**Upstream / downstream do not apply.** These 249 functions overwhelmingly do not call one another;
they are related only by touching the same memory. **No call-graph reading can find this
relationship**, which is why it went undocumented while the database already had the equivalent for
shared *code*.

**Do not confuse with:**

- [`../Shared-State-Accessors/cross-subsystem-accessor-hubs.md`](../Shared-State-Accessors/cross-subsystem-accessor-hubs.md)
  — shared **code**: three tiny functions with 168 callers across 14 subsystems. This is shared
  **memory**. The two are the same phenomenon seen through different instruments.
- [`../Ownership-Boundary/intentionally-ownerless-functions-and-shared-scratch.md`](../Ownership-Boundary/intentionally-ownerless-functions-and-shared-scratch.md)
  — the audit that found this area. That document's coarse description of it is corrected here.
- [`../../21-RNG-And-Determinism/rng-streams.md`](../../21-RNG-And-Determinism/rng-streams.md) —
  `022D9138` sits inside the same page and is **not** part of the workbench. Two writers, never
  accessed as a float, unrelated to the row array.

## 6. Modding notes

- **Treat the workbench as caller-saved.** Anything you write there is visible to the next user
  and **almost nothing restores it**. Write your operands, take your result, and assume the area
  is clobbered.

  > **CORRECTED 2026-09-08 — this said “nothing restores it”.** An explicit save/restore pair
  > exists — `0036D930` and `0036D8E0` — and **nine functions use it**, each of them both
  > saving and restoring, protecting one of exactly two rows: `022D8F30` (5 callers) or
  > `022D8F90` (3), with one saving both. The depth counter is at **`022D8F08`, inside this
  > very region**. The conclusion above still holds — 240 of the 249 writers restore nothing —
  > but *“nothing restores it”* was a property of most users stated as a property of the area.
  > [the save/restore pair](the-workbench-has-a-save-and-restore-and-nine-functions-use-it.md).
- **The sound code is a user.** Four Audio functions write 11–28 slots each. A graphics hook that
  leaves stale values in the rows can move where sounds appear to come from — a class of bug with no
  visual symptom at all.
- **`022D91B0` is the one row-block you can name with confidence.** If you need to read a transform
  out of the engine, `003970A0` already does exactly that and is 44 bytes long.
- **Do not patch `0036D9E0` out.** It is the only thing that clears the area, and it is unowned, so
  nothing else will do it for you.
- **`022D9138` is not scratch.** It is inside the same page and it controls a random-number stream.
  Writing it changes determinism.
- **Best intervention point:** the function that writes its operands, not the workbench. The
  workbench has no semantics of its own — the meaning is in who filled it and what they called next.
- **XIIOnline:** there is nothing here to replicate. A parameter area holds no authoritative state
  between transactions; two clients agreeing on it would be agreeing on the residue of whichever
  routine ran last.

## 7. What is not known

- [x] ~~How the row array divides into matrices beyond `022D91B0`. Rows are accessed in runs of 4, 6
      and 8, and a sliding window makes every 16-byte offset look like a base.~~ **BQ-16 ANSWERED —
      the premise is wrong and the answer is already on the sibling page.**
      [`the-ee-and-vu0-register-bank.md`](the-ee-and-vu0-register-bank.md) §: *"It does not divide
      into matrices. It is 31 vector registers and ACC."* **Every 16-byte offset looks like a base
      because every 16-byte offset IS one** — each is a distinct VU0 vector register, and a "matrix"
      is four consecutive registers a particular routine happens to use together, not a declared
      structure. The sliding window was not defeating the analysis; it was the answer.
      **Ticked 2026-09-13 (OPUS) as a stale checkbox, not as new work** — the callout in §1 of this
      page already said *"BQ-16 (no matrix division: the rows are registers) … answered there."*
- [x] ~~What `022D94B0` and `022D94B4` point to. Read 8 bytes wide by 16 functions in one tight family
      (`0036DDC0`–`0036E9B0`), never written through a RIP-relative store, so they are set through a
      register.~~ **BQ-17 ANSWERED 2026-09-12 (FABLE): not two pointers — the base of a 32-entry
      table of 24-byte records, written by the same family through its index.** Every one of the
      eighteen references is a `lea` that takes the address (no code loads the word itself), and the
      readers index it: `0036DDC0` clamps its argument to `0..31` (`0036DDC8`–`0036DDD5`), forms
      `base + idx·24` (`lea rcx, [rax + rax*2]` · `lea rbx, [rax + rcx*8]`, `0036DDDB`–`0036DDE6`) and
      reads a dword id at `+0`, a word state at `+4` (`test word [rbx+4], 0xFFFB`, then `= 4`) — so
      "8 bytes wide" was the `[rax + rcx*8]` scale, not a pointer width. The writers the rip census
      could not see are the indexed stores through the taken base: `0036DE5A` and `0036DF6A`
      (`mov word [r9 + rdx*8], r10w` on `022D94B4`, the state word) and `0036E2F8` (`or byte [rax +
      rdx + 0x10], dil` on `022D94B0`, a flag byte at `+0x10`). The ten rip-relative qword stores at
      `022D94A0` (`00394E50`–`00396F20`) are the neighbouring global before the table, not these
      cells. So `022D94B0` is the workbench's 32-slot record table — `{u32 id; u16 state; …; u8
      flags @+0x10}` at 24 bytes — and slot 0's first two fields are what the sheet saw. **BQ-17.**
- [x] ~~What the four Audio users compute. They write 11–28 slots each and read fewer, so they are
      using the workbench as arguments — but which transform they are asking for is unread.~~
      **BQ-18 ANSWERED 2026-09-12 (FABLE): no matrix transform — they compute a spatial sound
      source's *effective position* for the listener, using the workbench as vector scratch.** All
      four hang off `003631B0(listenerPos, idList, table, …)`, the per-source loop of the audio
      listener update `00362850` ([the world tick](../Battle-Frame/the-world-tick-and-the-field-frame.md)):
      for each source id the loop resolves the source record (`022CBAF0` + the table's word) and
      switches on its shape byte `+9 & 0x7F` (`0036326A`–`0036327B`) — **0 → `00361DE0`**,
      **1 → `003623C0`**, **2 → `00362230`**, else the raw position — then hands the resulting
      `vec4` and the record's radii `+0x38` / `+0x54` / `+0x58` to `00361810` and `003638B0`
      (`003632D1`–`00363344`). Each helper takes `(listenerPos, out, source)` and writes one point
      to `out`: `00361DE0` (kind 0) rotates by the source yaw `+0x50` (`cosf` / `sinf`, `00361E8C`–
      `00361EA5`), uses the half-extents `+0x30` / `+0x34`, takes two `sqrtf` (`00362090`, `003620B4`)
      and returns the projected closest point `origin + dir × t` (`00362175`–`003621E2`) or, when
      the source's flags say so, the source's own position `+0x20..+0x28` (`003621F9`–`0036220D`);
      `003623C0` (kind 1) rotates by the same yaw, clamps into the `+0x30` / `+0x34` box (the
      inside test `test al, 0x33` at `003626B2`) and returns the clamped point (`003626B9`,
      `003627FA`); `00362230` (kind 2) walks `+0x14` segments of 32 bytes from `+0x40`, calls
      **`00363FD0`** on each — `d = p0 − p1`, `t = clamp(dot(a, d) / |a|², 0, 1)`, squared distance
      to the segment (`00363FFB`–`003641D4`) — keeps the nearest and returns its closest point
      `p0 + t × (p1 − p0)` (`003622C8`–`0036238A`). So the "transform they ask for" is the closest
      point of a yaw-rotated round source, a yaw-rotated box source and a polyline source
      respectively — the game-side geometry behind the driver's `Sd::Lay` shape classes; the slots
      they write (`022D92A0`–`022D9318`) are the temporaries of that geometry and `0036DD80` /
      `0036DD90` / `0036DDA0` the workbench's vector helpers between them.
- [x] ~~Whether any of the 62 behavioural objects is genuinely persistent state rather than parameter
      space. The test applied here is population-wide; individual slots were not traced.~~
      **BQ-19 ANSWERED on the same sibling page:** *"Registers are volatile by definition. A value
      that survives between routines is a…"* — the question dissolves once the area is read as a
      register bank rather than an object store. **Ticked 2026-09-13 (OPUS) as a stale checkbox.**
- [x] ~~What `0036D9E0`'s header writes (`01EF93F0`, `01EF93F4`, `01EF93FC`) configure.~~
      **BQ-20 ANSWERED 2026-09-13 (OPUS): they are not three globals — they are ONE 16-byte vec4
      holding `(0, 0, 0, 1.0f)`, and it is a constant, not workbench state.** The header writes the
      four dwords in three instructions, which is why the sheet saw three addresses:
      `0036D9E0` loads `1.0f` from `01CEBBA8` and stores it to `01EF93FC` (`movss`), then zeroes
      `01EF93F4` as a **qword** — covering `F4` *and* `F8` — and `01EF93F0` as a dword. So the block
      is `{0.0, 0.0, 0.0, 1.0}`: the identity homogeneous vector, W = 1.
      **It has exactly two writers and they write the same thing.** The second is `0036D990`
      (74 B), which sets the identical values and then announces itself through the variadic logger
      `0017D280` — `"Sizeof 64 bit int = %d\n"` with 8, then
      **`"PS2 Assembly emulation initilization completed! *** \n"`**. So this cell belongs to the
      **PS2 assembly-emulation layer's start-up**, not to the matrix area the rest of this page
      describes, and the workbench initialiser touches it because it runs that start-up.
      **It is consumed as a vector, not as scalars**: 98 functions read `01EF93F0`, many with
      `movups xmm, xmmword ptr [rip+…]` taking all sixteen bytes at once (`00250010`, `00270260`,
      `00271960`, `002762A0`); the components are separately read by `movss`/`addss` in 35–36
      functions each.
      **CONTROL, because "written only at initialisation" is the kind of claim this index has been
      wrong about before.** The `0` in a writers column is only trustworthy if nothing takes the
      address — `UNEXPLAINED-GLOBALS.md`'s own header records a contract that quoted such a `0` as
      *"never written"* and was wrong. Scanning `01EF93E0`–`01EF9410` for address-taking finds
      **exactly two `lea`s, at `0036E70C` and `0036E75D`, and both target `01EF9400`** — the
      adjacent int table, which they only index and read (`mov r9d, [r8 + rax*4]`). **Nothing takes
      the address of `01EF93F0`–`01EF93FF`**, so the RIP-relative census is complete over this block
      and the two-writer count is exact rather than merely unseen.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The area is BSS with no file image | PE section table: `.data` VA `01DF0000`, raw size `0x18E400`, so raw ends at VA `01F7E400`; every workbench address resolves to no file offset | 1 |
| Every 16-byte access is 16-byte aligned | whole-image disassembly: 46 addresses accessed at width 16, alignment histogram `{0: 46}` | 1 |
| `022D91B0` is a 4×4 matrix | complete body of `003970A0` — four `movups` loads at +0/+16/+32/+48 stored to one 64-byte destination | 1 |
| `0036D9E0` clears the area and reads nothing | complete body: 80 slot writes `022D91B0`–`022D9428`, zero reads | 1 |
| 215 of 216 row-touchers write; one reads only | per-slot writer and reader sets over all 38,161 function bodies | 1 |
| Non-Presentation owners write no private sub-area | slot-set difference against Presentation's slots: ActorEntity 0, UI 0, Movement 0, Audio 4 | 1 |
| `022D94B0`/`B4` are pointers, not matrix data | 8-byte access width on every one of 150 accesses, never a float instruction, no RIP-relative store | 1 |
| Object boundaries | writer-set similarity, not adjacency — see §10 | 1 |
| `01EF93F0` is one vec4 `(0,0,0,1)`, not three globals | `0036D9E0` header: `movss` of `1.0f` from `01CEBBA8` to `+0xC`, qword `0` at `+4` covering `F4`/`F8`, dword `0` at `+0`; 98 readers, many `movups` 16 bytes wide; second writer `0036D990` writes the same values and logs "PS2 Assembly emulation initilization completed!" | 1 |
| Nothing takes the address of `01EF93F0`–`01EF93FF` | scan of `01EF93E0`–`01EF9410` for address-taking: exactly two `lea`s, `0036E70C` and `0036E75D`, both targeting the adjacent int table `01EF9400` and only reading it — so the rip census is complete over this block | 1 |
| `022D9138` is RNG state, not workbench | two writers, no float access; corroborated by `rng-streams.md` | 1 + 9 |

**On the ownership verdict.** It rests on three failed tests, not on a head count. The head count
(144 Presentation writers against 8 from four other categories) is deliberately *not* the argument,
because this database may not infer ownership from a population of users — that is the same
inheritance error the evidence standard bans for callers.

**Superseded readings:** the document that found this area described `022D8F00`–`022D9500` as *"13
objects"*, one of them a 660-byte buffer with 215 writers. Both figures came from coalescing write
targets by address adjacency. Corrected in §10.

## 8b. A save/restore exists, and a call-only scan finds five ninths of it — 2026-09-08

[the save/restore pair](the-workbench-has-a-save-and-restore-and-nine-functions-use-it.md) documents `0036D930` / `0036D8E0` in full and corrects §6 above.

> **Four of the nine restores are tail-jumps** — `0026F413`, `003AFFAB`, `00431F0A`,
> `0046242E` — the natural shape for a helper called last. **An `E8`-only scan finds five of
> nine and reports a leak that is not there**, which is this database's four-instrument rule
> earning its keep on a question that looked like plain bookkeeping.

**And the restore was verified by execution, not only by reading**: a 16-byte marker written to
`022D8F30`, `0026EE00` run as shipped under emulation, and the marker found intact with the
depth counter back at zero.

## 9. Related

- [`../Ownership-Boundary/intentionally-ownerless-functions-and-shared-scratch.md`](../Ownership-Boundary/intentionally-ownerless-functions-and-shared-scratch.md) — B-4, where this was found, and whose description of the area this document corrects
- [the save/restore pair](the-workbench-has-a-save-and-restore-and-nine-functions-use-it.md) — the pair that corrects §6, and `0026EE00` as a worked user
- [`../Shared-State-Accessors/cross-subsystem-accessor-hubs.md`](../Shared-State-Accessors/cross-subsystem-accessor-hubs.md) — the shared-code counterpart
- [`../../21-RNG-And-Determinism/rng-streams.md`](../../21-RNG-And-Determinism/rng-streams.md) — owns `022D9138`, inside the same page
- [`../../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md`](../../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md) — the same idea one layer up: handlers passing arguments to each other through a shared stack

## 10. Falsification pass 2026-09-02 — the object boundaries were derived the banned way

**Attack chosen.** This area entered the database in the B-4 audit as *"13 objects, the largest a
660-byte buffer with 215 writers"*. Both numbers came from **coalescing write targets whose addresses
were within 8 bytes of each other** — that is, from address adjacency, which the evidence standard
bans as proof precisely because it merges unrelated things. Having already been burned once in the
other direction (84 consecutive bytes read as 84 globals), the first thing to attack was my own
clustering rule.

### CORRECTED: 62 objects, not 13

Objects were re-derived **behaviourally**: two slots belong to the same object when the same functions
touch them. Grouping consecutive touched slots only where the toucher sets overlap by a Jaccard
index of 0.25 or better gives **62 groups**, against 13 from adjacency alone. The adjacency rule
over-merged by nearly five to one, and the "660-byte buffer" it produced does not exist as a single
object — the same span contains three 64-byte row blocks, a 20-byte hot spot with 138 writers, a
148-byte area with **one** writer, and several single slots.

**Both of my clustering errors were the same error.** Adjacency splits one object into many when the
access is byte-wise, and merges many objects into one when they are packed. It was wrong in both
directions within two blocks of each other, and neither failure announced itself in the number.

### SURVIVED: every structural claim that came from the code rather than from a rule

- **All 46 SSE-width accesses are 16-byte aligned**, no exceptions.
- **`003970A0` copies four consecutive rows into one 64-byte block**, which fixes a matrix at
  `022D91B0` from the engine's own code. This is the claim the earlier reading should have led with
  and did not have.
- **`0036D9E0` clears 80 slots and reads none.**
- **215 of 216 row-touchers write before reading.**

### SURVIVED, and it is the answer to the question: no owner

The suspicion worth testing was that Presentation owns the area and everyone else borrows — 144 of
the 152 owned writers are Presentation. Three tests, all negative: no other owner keeps a private
sub-area (ActorEntity, UI and Movement write **zero** slots Presentation does not; Audio four); the
whole-area initializer is **unowned**; and only one function in the image reads a row it did not
write. **A parameter area cannot be owned because nothing is held in it.**

### What was tried and did not break anything

- **Looked for read-only consumers**, which would prove persistence. Eighteen exist across the page;
  **sixteen of them read only two slots**, always 8 bytes wide and never as floats — pointers, a
  different object. One reads matrix 0. That is the entire persistent surface.
- **Checked the page against every document that already cites an address in it.** `rng-streams.md`
  claims `022D9138`; the writer set agrees at two writers and the slot is never touched by a float
  instruction, so it is not workbench data. **No contradiction, and the check is what stopped the
  page being described as one object.**
- **Tried to enumerate the matrices structurally** by finding every four-row-at-16-byte-stride
  sequence. It produces bases 16 bytes apart, because a sliding window over a longer run matches at
  every offset. The method cannot separate matrices, so the grouping past `022D91B0` is left open
  (BQ-16) rather than guessed.

### Status

`DOCUMENTED`, one falsification pass. What would kill it: a function that reads a workbench row it
never wrote and is not `003970A0`; a private sub-area belonging to a non-Presentation owner; a second
whole-area initializer that carries an owner tag; or a static initializer for the region, which the
section table says cannot exist.

## 11. An outer bound from reference holes, and a near-miss worth recording — 2026-09-08

### ⚠ What I nearly published

Arriving here from the globals frontier (`022D92E0` ranked top of `UNEXPLAINED-GLOBALS.md` with ~250
writers), I segmented `022D8F00`–`022D9500` by **holes** — spans that no instruction references at
all — and got **nine runs**. That was about to be written up as an object map.

**It would have been a regression to the method §10 already banned.** Hole segmentation *is*
adjacency clustering: it merges everything between two holes into one object. §10's correction
—13 objects by adjacency → **62 by behavioural overlap** — already establishes that adjacency
over-merges here by nearly five to one, and nine is worse than the thirteen it rejected.

> **The document caught the error, not the analyst.** `check_already_answered.py` pointed at `BQ-13`,
> `BQ-13` pointed here, and §10 named the exact mistake before it reached a file. That is the
> intended function of both, and it is worth recording that it worked.

### What does survive: holes are a *necessary* boundary, never a sufficient one

A hole is not an adjacency argument. It is the **absence of any reference**, and an object cannot
span bytes that nothing touches. So the nine runs are a valid **outer bound**: the 62 behavioural
objects must nest inside them, and no object crosses a hole.

| # | extent | bytes | max writers | max readers | sub-offsets touched |
|---:|---|---:|---:|---:|---|
| 1 | `022D8F00`–`022D8F70` | 112 | 29 | 44 | all 16, byte-granular |
| 2 | `022D8F90`–`022D9010` | 128 | 64 | 47 | all 16, byte-granular |
| 3 | `022D9040`–`022D9050` | 16 | 0 | 1 | `+0xC` only |
| 4 | `022D9090`–`022D90B0` | 32 | 1 | 1 | `+0x0` only |
| 5 | `022D9110`–`022D9170` | 96 | 10 | 13 | `0,4,8,C` + one byte access |
| 6 | `022D9190`–`022D9430` | **672** | 128 | 103 | `0,4,8,C` — **the workbench** |
| 7 | `022D9450`–`022D9460` | 16 | 2 | 0 | `0,4,8,C` |
| 8 | `022D9470`–`022D9480` | 16 | 5 | 0 | `0,8` |
| 9 | `022D94A0`–`022D94C0` | 32 | 42 | 28 | `+0x0` 8-wide, `+0x4` — **`BQ-17`'s two pointers** |

**Run 6 is this document's subject** and contains most of the 62. **Runs 1, 2 and 5 are byte-granular
and float-free**, which is a different object kind from the workbench's clean `0,4,8,C` float4
pattern — that width signal is independent of both adjacency and toucher-overlap, and §10 records
that the matrix-separation attempt lacked exactly such a discriminator. **Offered as a lead for
`BQ-16`, not as an answer.**

### A worked example of the memory calling convention

`FUN_002F1EC0` (121 B) is the clearest instance of what §2 describes, small enough to read whole:

```asm
002F1EC0  movups xmm1, [rcx]              ; a
002F1EC3  movups [022D92E0], xmm1         ; slot A <- a
002F1ECA  movups xmm2, [rdx]              ; b
002F1ECD  movss  xmm0, [022D92E4]
002F1ED5  addss  xmm1, xmm2               ; x
002F1ED9  movups [022D92F0], xmm2         ; slot B <- b
002F1EE0  movss  [022D92E0], xmm1
          shufps xmm1, xmm2, 0x55 / addss / movss [022D92E4]   ; y
          shufps xmm1, xmm2, 0xAA / addss / movss [022D92E8]   ; z
          shufps xmm2, xmm2, 0xFF / addss / movss [022D92EC]   ; w
002F1F2E  movups xmm0, [022D92E0]
002F1F35  movups [rcx], xmm0              ; a <- result
002F1F38  ret
```

```c
void Vec4AddInPlace(float4 *a /*rcx*/, const float4 *b /*rdx*/);   /* 002F1EC0 */
```

> **Both operands are copied into globals, the arithmetic is done component-by-component through
> them, and the result is copied back.** The register values are already in `xmm1`/`xmm2` — the
> globals buy nothing. This is the memory calling convention §2 describes, in its purest form, and it
> is why `022D92E0`/`022D92F0` carry ~250 and ~230 writers while holding nothing between calls.

**Consequence for reconstruction, and it is the reason this matters:** a reimplementation must **not**
model these slots as engine state. They are the argument registers of a math library that spills to
memory. **And the pair is not reentrant** — two threads calling this simultaneously would corrupt
each other's operands. Whether anything ever does is `BQ-19`'s question, not answered here.

### Method

`page2.py`-style scan: every non-EH function body disassembled, every RIP-relative memory operand in
`022D8F00`–`022D9500` recorded with **its operand width** and its read/write role. Widths come from
the instruction encoding, not from the address. EH funclet bodies excluded throughout.

## Residual placements — 2026-09-14 (SWE2-FRONTIER, residual-placement package)

| function | size | role (call-signature read) |
|---|---:|---|
| `00248A90` | 888 | single-callee workbench driver: entire body reduces to `0036DD80` plus its own argument setup; caller `002CEFD0` |

## The `0025C830` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`0025C830` — the ActorEntity user (29 slot writes / 24 reads): record
`rsi = [rdx+0xB8]` (`0025C85A`), `byte[rdx+8]`/`byte[rsi+0x5C]` kind
bytes (`0025C86C`/`0025C87C`), `xmm11 = float[rsi+4]` (`0025C880`),
`[02099D78]` context (`0025C898`), `dword[rsi+0x60]` saved then
overwritten with `r14d` (`0025C8B3`/`0025C8B9`), `byte[rdx+0xD]`
(`0025C8BD`), `0037C860` (`0025C8CE`), `byte[r12+0x16]` test
(`0025C8F0`), `00226BD0(0xA)` (`0025C8FE`), `00233D20` (`0025C909`).

| member | role | interior |
| --- | --- | --- |
| `0025A8E0` (164 B) | staging-cell writer — `movss [rdx+0xC]`, `andps 0x7FFF…` abs (`0025A8F7`), `movss [rcx]`, `xorps 0x8000…` negate (`0025A917`), `movss [rcx+4]` (`0025A92C`), bumps the `022D9130` staging bank (`0025A8E5`/`0025A8F1`/`0025A926`) | [`0025A8F7`](../../_index/ADDRESS-INDEX.md) |
| `00227420` (62 B) | gated option setter — `test dword[01FD46D4], 0x40000` arm (`00227424`), `-1` sentinel pair (`00227432`/`0022743D`), `00226BE0`, tail `00226280` (`00227454`). The `0x400` arm cited here earlier lives in `00227460` — a separate 62-B twin on the same `01FD46D4` global, reached through Script-VM thunk `00350400`, not a member of this subtree (AUDITSEM-CONTRA-FRONTIER-27464-ARM, 2026-09-17) | [`00227432`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0037C860`, `00226BD0`, `00233D20`,
`00226BE0`, `00226280`. `0025A8E0`'s `022D9130` cells are the same
staging bank the `00433830` blend kernel consumes.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAction — CLIENT (2 edges).** `00313DB0`, owned by that layer, calls
the shared helpers `00226280` and `00226BE0` this page's `0025C830` section
names. The crossing is that caller consulting shared callees, not ownership
of either helper. Read from `edges.tsv` 2026-09-17 (SWE2-FRONTIER).

**Input — CLIENT (4 edges).** `0035B4B0` and `0035B510` call `00226280`, and
`00226BE0` calls `00227420` and its Script-VM-reached twin `00227460` — the
`01FD46D4` option-setter pair. Input-layer clients of shared helpers named
here; fan-in, not shared ownership. Read from `edges.tsv` 2026-09-17
(SWE2-FRONTIER).

**ActorEntity, Audio, Movement, Party, Presentation, World and WorldAreaField — CLIENT (shared-callee edges, SWE2-EC7 batch-161).** The `0036E1E0` slot-refresh entry names `00314020` (`World_UpdateSimulationTick`) and `0024DE70`; the tick's own call fan-out reaches presentation helpers (`00202C90` callers `00274CB0`/`0028D460`/`003B3F10`...), audio (`002DEBF0`, `002DF370`), movement (`0026A1D0`/`0026C3E0`/`0022D7E0`), party (`00263750`/`003590D0`), actor-entity (`00263660`/`0026C5D0`/`0025C830`), world (`002623A0`, `00266D10`) and world-area/field callers (`00377C20`, `00234590`). The workbench banks are consulted through the tick; the crossing is the tick's own breadth, not subsystem state living here. Edge list from `edges.tsv`.
- **Save_Load_Settings — MECHANICAL (2 edges).** 2 Save_Load_Settings-side calls into shared helper(s) the page cites (`0017D280`) - the helpers' general call surface, not a Save_Load_Settings relationship of this page's subjects.
- **Spawn_Encounter_Lifecycle — CLIENT (1 edge).** 1 inbound (Spawn_Encounter_Lifecycle bodies `SpawnGroup_DispatchPendingCompletionSignals` (00307030) call page-cited `00233D20`). Substantive edges include `00233D20` is called by `SpawnGroup_DispatchPendingCompletionSignals` (00307030).
- **UI — CLIENT (34 edges).** 34 inbound (UI bodies `0035DCC0`, `003F9390`, `003F8FE0` call page-cited `00202C90`, `00270260`, `00249110`). Substantive edges include `00270260` is called by `00550FB0`; `00270260` is called by `004027D0`; `00270260` is called by `003F8FE0`; `00270260` is called by `003F9390`; the remaining edges run through shared helpers the page cites.
## Interior citation — frontier hubs `0039A9B0` / `00397ED0` / `0036DD80` / `005002E0` (2026-09-17, SWE2-EC7)

Four more workbench leaves, all read against the shipping image:

- `0039A9B0` (574 B, 36 frontier callers) — a compose-and-clamp pass. It splats the four lanes of
  the caller's `[rcx]` row across the workbench globals (`mulps`/`mulss` chains at
  [`0039AA05`](../../_index/ADDRESS-INDEX.md)–`0039AAC8`), then runs two four-iteration loops that
  min-clamp dword pairs in the `022D8F30`/`022D8FA0` window (loop heads `0039AB80`/`0039ABB0`,
  `r8` folded as `-image_base` so the bases are `0x120000`-relative). Not a pure transform — the
  tail is bound enforcement on a shared table.
- `00397ED0` (342 B, 34 frontier callers) — the vec4-by-4x4-matrix transform loop. Copies the
  caller's four source vectors to the stack, then for each of 4 rows writes
  `sum_k in[k]*mtx[row][k]` (`mulss`/`addss` quads at
  [`00397F20`](../../_index/ADDRESS-INDEX.md)–`00397FF2`); stack-canary exit via `00808C40`.
  In-place-safe (source staged on stack before first store).
- `0036DD80` (15 B, 33 frontier callers) — constant-vec4 publish sibling of `0022CC20`:
  `movaps xmm0,[008C5FD0]` — the same constant `0022CC20` publishes — then
  `movups [01EF93F0],xmm0` at
  [`0036DD87`](../../_index/ADDRESS-INDEX.md).
- `005002E0` (389 B, 29 frontier callers) — a transform-eval + bounds-check predicate: composes
  `0039AF70` -> `00398F90` -> `002F1D90` on the caller's vector (first call at
  [`00500348`](../../_index/ADDRESS-INDEX.md)), then compares the scalar result against the
  `[rbx+4]`/`[rbx+8]` float window or the `0x6000..0xA000` word window on the result record —
  returns a bool, no writes escape.

NOT claimed: which semantic pass drives `005002E0`'s two range windows, or which table owns the
`022D8F30` min/max pairs `0039A9B0` maintains.

## Interior citation — frontier hub `00250010` (2026-09-18, SWE2-EC7)

`00250010` — 217 B, 12 callers; the workbench-adjacent float-state initialiser. It loads
the 16-byte seed constant at `01EF93F0`, splats its four lanes through `shufps 0x55`/`0xAA`/
`0xFF` into the `022D92F0`–`022D931C` mirror block ([`00250029`](../../_index/ADDRESS-INDEX.md) —
the same `022D92xx` block `00398C50` publishes the sin/cos tables into), then copies four
16-byte rows out of `022D9310`/`022D9300`/`022D92F0`/`01EF93F0` into `[rcx]` through
`[rcx+0x30]` (`002500C4`–`002500E5`). Sixty-four bytes of preset state plus the splatted
scalar mirrors, exactly what a fresh transform context is seeded with before the per-frame
compose runs.

## SWE2-EC7-33 update (2026-09-19) - `00361810`

`00361810` (982 B) is the recursive transform helper the workbench feeds `+0x38`/`+0x54`/`+0x58` radii - two self-calls plus `003A1C50`/`002DEBF0`/`00861F14`/`00861F02`/`0036DDA0`/`0036DD90`. Interior anchor `00361910` (a `003A1C50` call).

## SWE2-EC7-34 update (2026-09-19) - `00248A90`

`00248A90` (888 B) is a workbench slot walker - `ecx<=0` early out, `+2` index offsets on `r8`/`rdx`/`r9`, one `0036DD80` call per element. Interior anchor `00248C9E` (the `0036DD80` call).

## SWE2-EC7-38 update (2026-09-19) - `0035DCC0`

`0035DCC0` (492 B) is a transform-workbench body - `022D92E0`/`022D92E4`/`022D92E8` triples, `003588B0`/`00265470` pairs plus `00249110`/`0036DD80`/`00861F14`/`00808C40`. Interior anchor `0035DD0F` (a `003588B0` call).

## SWE2-EC7-41 update (2026-09-19) - `00271960`

`00271960` (328 B) is a transform-workbench body - `008F311C`/`008F3134`/`00908E14`/`009159FC`/`00915A04`/`00915A08`/`01EF93F0`/`01F44830`, `00270260`/`00808C40`. Interior anchor `00271A6C` (a `00270260` call).

## SWE2-EC7-61 update (2026-09-19) - `0032A6E0`

`0032A6E0` (153 B) is a Movement-user transform slot - `00861F02` single call plus `00908E30`/`0209A670`/`022D91B0`. Interior anchor `0032A769` (a `00861F02` call).


## SWE2-EC7-67 update - `002762A0`

`002762A0` (128 B) is a shared-transform body - `00202C90` x3 plus `01EF93F0`/`00915830`. Interior anchor `002762C6` (a `00202C90` call).

## SWE2-EC7-89 update (2026-09-20) - `003B24C0` keyed flag-bit read measured

`003B24C0` (75 B) is the tag-checked probe the workbench callers
run: `ecx` must carry the `0x70000000` tag, then the 32-slot
0x30-stride table at `02EBE5E0` is scanned for a matching key
dword; a hit returns `byte[slot + 0x20] & 1`, anything else
returns 0.
Interior anchor `003B24FA` (the matched arm).

## SWE2-EC7-90 update (2026-09-20) - `003B1710` slot-table state pump measured

`003B1710` (424 B) is the per-frame pass over the 32-slot
0x30-stride `02EBE5E0` table the workbench callers run:
`0036C1D0(8)` brackets it; each live slot (keyed `dword`,
`byte[+0x20]` bit-0 gated by the arg) dispatches on `+0x1C`
through an 8-arm jump table - `0032E4D0`/`0032E520`/`003B21E0`/
`0032E590`/`003B2710`/`0024F410`/`0024EE60`/`0024EE10`/
`0024B1F0` lifecycle calls - and removed slots are compacted by
a backward `movups` shift with `02EBEBB0` as the tail watermark;
the body tails `0036C140`.
Interior anchor `003B1784` (the jump-table read).

## SWE2-EC7-91 update (2026-09-20) - `0024B1F0` + `003B2710` measured

`0024B1F0` (70 B) is the insertion the workbench callers run on
the same `+0x348`/`+0x350` list `0024EE10` unlinks: `rcx` is
appended after the `rip`-kept tail (`[+0x350]` = old tail,
`[+0x348]` = new), both globals updated - or the record becomes
both head and tail when the list was empty.
Interior anchor `0024B203` (the tail-link store).

`003B2710` (61 B) is the keyed lookup `003B1710`'s dispatch arms
run: a 0x30-stride table between two `rip` bounds is scanned for
a live `dword` whose pointer field equals `rdx` and `dword[+4]`
equals `ecx` with `dword[+0x1C]` in {5,6} - returning
`qword[+8]`, or 0 on a miss.
Interior anchor `003B2748` (the matched arm).

## SWE2-EC7-104 update (2026-09-20) - `00265470` measured

`00265470` (86 B) is the three-dword position
read `002718E0`, `002EBFA0` and `0035DCC0`
call: `byte[rcx + 3] >> 5` selects the transform
class - class 2 copies `[[rcx + 0xB8] + 0x00 /
+0x04 / +0x08]` into the `rdx` / `r8` / `r9`
out-slots, class 1 copies `+0x20 / +0x24 / +0x28`
of the same record, and any other class (or a
null `rcx`) zeroes all three. The two field
triples are the same base record read at
different origins, so callers get a uniform
vec3 regardless of which representation the
object carries.
Interior anchor `00265475` (the `byte[+3]` class
read).

`0036E1E0` (173 B) is the 32-slot refresh `00314020` (`World_UpdateSimulationTick`) runs over the `022D94B0` record table: index `ebx` clamps into `0..0x1F`, each `0x18`-stride slot with a live `+4` word gets `0024DE70(dword[+0])` stored at `+6` - a `5` result back-stamps `+4`, a `0` clears `+0` and `+4` outright - while slots already at `+4 == 0` fold `ebp &= 1`; the function returns whether any slot stayed live

Interior anchor `0036E23B` (function `0036E1E0`).
