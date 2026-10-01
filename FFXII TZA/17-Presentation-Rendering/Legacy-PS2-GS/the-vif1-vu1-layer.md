---
system: The PS2 VIF1 / VU1 layer the PC port still runs — command packets, recompiled microprograms and the GS hand-off
category: 17-Presentation-Rendering
status: DOCUMENTED — UQ-213 answered 2026-09-27 (57 microprograms; each draws the primitive of the template tag it stamps); UQ-215 answered 2026-09-27 (13 parametric arms, only V4_32 ever reaches them) (box pending)
owner_layer: CodeDomain:Presentation.LegacyPS2GS (proposed) — the same console fossil family as the GS texture budget
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 204 addresses cited - 31 data, 66 entry, 104 interior, 3 text-data, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-13
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_kind: reproduction
  last_pass_by: OPUS
  last_pass_state: opus-vif1-vu1-pass-1 - independent reproduction against the function list, by a party whose own instrument disagreed with the page. EVERY CHECKED FIGURE HOLDS. The named bodies reproduce to the byte: 004B1190 32,136 and 004EF860 219 exactly as written, and the six "largest in the region" are in true descending order (32,136 / 28,422 / 24,541 / 22,073 / 18,098 / 15,212). The 219-byte family of section 2.5 is 7 of 7 at 219 B with 004CF280 at 197 B. The 47 is internally consistent - 35 template-path programs plus 29 render-command programs less 17 shared = 47 - and "all ARCH frontier" holds: every named body has an empty owner, and the function list's own tags (Presentation.RegisteredFunction, FunctionAddressReferencedFromCode) independently corroborate the registration story the page tells from disassembly. ADJUDICATED IN THE PAGE'S FAVOUR AGAINST MY OWN PUBLISHED CLASSIFIER: classify_vu_region.py files 004B1190, the largest body in the region, as "drives VU state, not float-dominated" at 29.9 % float - ten points below its threshold - while this page names it a microprogram on registration evidence with 17 VU-helper calls. The page is right and the instrument is wrong; the float ratio is not a necessary condition. Recorded in 99-Unresolved-Residual/README.md, where my count is now stated as a floor of 24 against a ceiling of 59, an interval that brackets this page's independently derived 47. ONE COMPLETENESS NOTE, NOT A DEFECT: section 2.5 names 7 bodies of 219 bytes in 00470000-00500000; there are 9. The page says "several", so it claims no exhaustive list. NOT CHECKED: the 329,225 B total for the 35 template-path programs, which needs the enumeration re-run rather than the six named members; and every open item the page lists as unread.
  crossref_clean: false
  reopened_count: 0
---

# The PS2 VIF1 / VU1 layer

> **Some of FFXII's PC rendering still runs the PlayStation 2 vector-unit pipeline.** It builds VIF1 command
> packets the PS2 version sent to its VU1 coprocessor. An interpreter in the executable decodes those packets.
> The VU1 microprograms they call exist as recompiled x64 functions, working over an emulated 1,024-word VU
> memory. Their GS output goes to a callback. This is where most of the `0x480000`–`0x500000` region comes from.

**PARTIAL.** The interpreter, the machine state, the installation paths and the program population are read.
**Not read:**
- what any single microprogram draws;
- how the GS data is finally turned into PC draw calls;
- the UNPACK formats.

*(2026-09-13, FABLE. The region had been catalogued as "generated float-table builders" and "unexplained
float code". Found while choosing frontier families; see §8.)*

## 1. What the player sees

Nothing different. Whatever this layer draws looks as it did on the PS2 because it runs the same
microprograms, translated. That is also why this code has no strings, no RTTI and no names: it was never
C++ written for the PC.

## 2. Native mechanism

### 2.1 The interpreter — `0022C970`, a VIF1 command decoder

`0022C940(packet, size, callback, context)` passes the VU memory base `02064E30` (`0022C95A`) to `0022C970`,
which walks the packet four bytes at a time and switches on the top byte (`0022C9DB`). **Every case it handles
is a VIF1 command, with VIF1's field layout:**

| code | VIF1 name | what `0022C970` does | sites |
|---|---|---|---|
| `0x01` | STCYCL | low byte → `02088E40` (CYCLE), next byte → `02088E3C` (WL) | `0022C9DE`–`0022C9F2` |
| `0x02` | OFFSET | `data & 0x3FF` → `02088E34`; clears bit 6 of `02088E38`; copies `02088E30` to `02064E28` | `0022C9FD`–`0022CA1C` |
| `0x03` | BASE | `data & 0x3FF` → `02088E30` | `0022CA28`–`0022CA31` |
| `0x4A` | MPG | **the payload is an 8-byte x64 function pointer**, stored at `02068E30[addr]`; `addr` is appended to the list `02088E50` (count `02088E44`) | `0022CA3D`–`0022CA60` |
| `0x50` / `0x51` | DIRECT / DIRECTHL | calls the callback with the data pointer, then skips `count × 16` bytes | `0022CA68`, `0022CB24`–`0022CB39` |
| `0x60`–`0x7F` | UNPACK | `0022BFF0(vuMem, …)` with ADDR (`& 0x3FF`), NUM (bits 16–23) and flag bits 14 / 15 | `0022CA73`–`0022CAC7` |
| `0x14` / `0x15` | MSCAL / MSCALF | flush (`0022C8D0`), pick the largest installed address not above the requested one, call the program stored at `02068E30` + addr × 8, passing the callback and context | `0022CAD0`–`0022CB1E` |

**Qualified 2026-09-27 (FABLE, Claude Opus 5.5), on ASTRA's static packages. These five points state preconditions the
table above leaves implicit. None of them is a claim that a shipped packet breaks one.**
- **MSCAL's choice when nothing is eligible** (`ASTRA-RETURN-FABLE-VIF-PROGRAM-SELECTION`,
  `_experiments/evidence/vif-program-selection-boundary/`).
  - The best candidate starts at 0 (`0022CADD xor eax, eax`). An empty list jumps straight to the call (`0022CAE5`).
  - The scan compares each list dword unsigned against the request (`0022CAF6 jb`) and keeps the largest (`cmovae`).
  - So MSCAL calls **the largest installed address not above the request if there is one, and slot 0 otherwise**.
    Slot 0 must therefore be callable whenever that fallback can happen.
  - The `0x10000` compare after the scan (`0022CB07`) cannot fire for the u16 addresses MPG appends, so it is not a
    no-match guard. Nothing checks the pointer before the indirect call at `0022CB1E`.
  - The 11-byte count reset in ASTRA's package stores 0 to the list count `02088E44` and nothing else, so it leaves
    the pointer table and list bytes as they were. The flush MSCAL calls first (`0022C8D0`) writes only the
    TOP/TOPS/status words.
  - Not established: when the count is reset in normal play, and whether a stale slot 0 is ever called.
- **The callback flag is a dword truth test of a byte-written slot** (`ASTRA-RETURN-FABLE-VIF-CALLBACK-FLAG-WIDTH`,
  `_experiments/evidence/vif-callback-flag-width/`, isolated original-code runs).
  - `001DB550` zeroes `esi` and stores only `sil` into its fifth-argument slot (`001DB5B9`).
  - The wrapper reads that slot as a **dword** (`0022C944`) and forwards it.
  - The decoder imports it (`0022C9BB`) and passes it on for DIRECT/DIRECTHL (`0022CB27`).
  - The callback tests all 32 bits (`001DB643 test r8d, r8d`, then `setne`), and the collector stores the resulting
    byte (`001DB67D`, `001DB729`).
  - So a zero low byte does not make the flag false; the upper three bytes of the stack slot decide it too. In
    ASTRA's runs, `0x100` and `0x80000000` in the slot gave 1, and a low byte of 1 overwritten to 0 gave 0.
  - Not established: what the upper bytes hold in normal play, and whether the flag ever changes a picture.
  - *Added 2026-09-27 (FABLE, Claude Opus 5.5), routed by OPUS's adjudication (`_index/candidates/opus-astra-returns-2026-09-27/`,
    control `vif_flag_init.py`): the frame never writes the upper three bytes - its only store to the slot is that byte store -
    so the flag is false exactly when the bytes inherited at `[rsp+0x21]`–`[rsp+0x23]` are zero.*
- **Admission and progress** (`ASTRA-RETURN-FABLE-VIF-ADMISSION-PROGRESS`, `_experiments/evidence/vif-admission-progress/`).
  - The decoder takes the next four-byte header (`0022C9D6`) before it compares its cursor with the byte length
    (`0022CB55`). A length of 1–3, or a remainder of 1–3, still reads a whole header.
  - UNPACK is not given the remaining length; its return is added to the cursor after it runs.
  - For `V4-32` with NUM > 0 and WL = CL = 0, the UNPACK loop at `0022C630`–`0022C686` adds zero to every counter and
    repeats without end. NUM = 0 bypasses it, and WL = CL = 1 progresses. *(qualified 2026-09-27, FABLE, Claude Opus 5.5, adopting OPUS's owner read 532305504: WL = 0 alone is enough - the loop's test counter advances only by `add ebx, r11d` (`0022C67E`), the WL term, so any CL stalls it once WL = 0.)*
  - These are conditions a packet producer must meet. Not established: whether any shipped packet has these values.
- **The GIF size is a 32-bit total over a 64-bit walk** (`ASTRA-RETURN-FABLE-GIF-SIZE-COPY`,
  `_experiments/evidence/gif-size-copy-boundary/`). See §2.1a.
- **UNPACK cycles** (`ASTRA-RETURN-FABLE-VIF-CYCLE-AND-CURSOR`). See UQ-215 in §7.

On the PS2, MPG uploads microcode words into VU1 micro memory. **Here it uploads a pointer to a function
that already is that microcode, compiled.** MSCAL then calls it. The `0x3FF` masks and the 1,024-entry
address space are VU1's.

**The entry.** `001DB550` walks an object's chunked packet list and calls `0022C940` once per chunk
(`001DB5E0`), with callback `001DB640` (`001DB5C0`) and the object as context. `001DB550` is reached only through
a data qword: it is **slot 0 of the `GiVmax` render command's vtable `009007E8`** (RTTI `.?AVGiVmax@@`; slot 1 `001DB3D0`), one of
the [Gi render commands](../Gi-Render-Commands/gi-render-command-family.md). `001DB840` allocates the `0x640`-byte command
(`001DB875`–`001DB88A`) before appending its packets. The callback forwards to `001DB660`, which copies the GS data
into the object's chunked buffers (`memcpy` at `001DB6A8`).

### 2.1a Two phases: run on the CPU, then replay as GIF packets

`GiVmax` works in two phases.

**Phase 1 — slot 0, `001DB550`, runs the packets and collects the output.** Each GS output is copied by `001DB660`:
- the copy's size comes from `0020F310`;
- the copy's pointer is appended to the chunked list at `+0x228` (count `+0x224`);
- the callback's flag byte is appended to the list at `+0x430` (count `+0x42C`) (`001DB6BC`–`001DB729`). *That byte
  is the result of a dword test on a stack slot whose caller wrote only its low byte (§2.1, qualified 2026-09-27).*

**Phase 2 — slot 1, `001DB3D0`, replays them against the render device.** It:
1. sets render state (`002105B0`, `002104D0`, and `00210560(0x51001)` when `+8` is set);
2. calls `00210320(packet, device, flag)` for every collected copy (`001DB44A`–`001DB4B5`);
3. resets state (`002104E0`, `002105B0(0)`).

**The copies are GIF packets.** `0020F310` walks **PS2 GIF tags** and sums their sizes (`0020F350`–`0020F3C5`):

| field | bits | how it is read |
|---|---|---|
| NLOOP | 0–14 | `& 0x7FFF` |
| EOP | 15 | stops the walk |
| FLG | 58–59 | `>> 0x3A & 3` |
| NREG | 60–63 | 0 means 16 |

| FLG | packet size |
|---|---|
| 0, PACKED | (NREG × NLOOP + 1) × 16 bytes |
| 1, REGLIST | NREG × NLOOP rounded up to even, × 8 + 16 bytes |
| 2 / 3, IMAGE | (NLOOP + 1) × 16 bytes |

These are the GIF sizing rules. If the byte `01E027C0` is 0, the size is a flat 16 (`0020F316`–`0020F322`).

*Qualified 2026-09-27 (FABLE, Claude Opus 5.5), on `ASTRA-RETURN-FABLE-GIF-SIZE-COPY`. The formulas stand. What the
returned number means needs these conditions:*
- **The total is 32-bit; the walk is 64-bit.** Each tag's size fits 32 bits, at most 8,388,368. The total accumulates
  in `r10d` (`0020F3B8 add r10d, edx`), so it wraps at 2^32. The header cursor advances by each tag's own size,
  zero-extended into a 64-bit pointer (`0020F3C0`–`0020F3C2`), so the walk itself does not wrap.
- **The last tag is counted, not read.** EOP stops the walk after adding the final tag's size; that tag's payload is
  never touched.
- **Nothing bounds the walk.** The helper takes no buffer length and has no overflow check. `001DB660` hands the
  returned size, zero-extended, to its allocation call and then to the `memcpy` at `001DB6A8`, with no check between.
- **So the return is the copied extent only if** the headers up to an EOP are readable, the source really extends
  that far, and the total stays below 2^32. ASTRA's symbolic layouts show the limits: 257 maximal PACKED tags already
  set the sign bit (which the zero-extension carries), and a declared total of exactly 2^32 returns 0.
- Not established: what bounds real producers, how the gate byte is initialised, what the callees do with such sizes,
  and whether any such packet is reachable.
`00210320` splits the same tag and additionally extracts **PRE (bit 46)** and **PRIM (bits 47–57)**
(`00210390`–`002103E7`) before its register handlers (`0020EC80`, `0020FE70`, `0020F3E0`).

*Replay by mode - added 2026-09-27 (FABLE, Claude Opus 5.5), on `ASTRA-RETURN-FABLE-GIF-REGLIST-DISPATCH`; static, and
read again here from the bytes.* Sizing (above) and replay are different walks. The replay does not treat every mode
alike:
- **NLOOP 0** skips the mode fields (`002103BE`) and the handling (`00210426`). It goes straight to the EOP test
  (`00210489`): EOP 1 ends the walk, EOP 0 moves on to the next 16-byte header.
- **PACKED with NLOOP > 0** goes to `0020F3E0`, which returns the cursor the EOP test then uses. With PRE set it first
  flushes and sets PRIM (`0021043B`–`00210447`).
- **REGLIST with NLOOP > 0** leaves the walk through the completion flush at `002104A0` (`00210473`–`00210476`), whatever
  its EOP bit. So a non-empty REGLIST tag ends this replay, and an empty one follows the EOP rule. "Every REGLIST tag
  stops" would overstate it.
- **IMAGE (2, 3)** advances NLOOP × 16 bytes with no payload handler (`0021047F`–`00210486`), then takes the EOP test.

PRE is applied only on the PACKED path. What the flush submits, and how often shipped packets use each mode, is not
established.

**So the path ends in a GS emulation that turns GIF packets into PC draw state.**

### 2.1c What runs a `GiVmax` command — the program runs at emit time, only the GS replay is deferred (FABLE, Claude Opus 5, 2026-09-20)

**The question this answers.** [The bone trails](../Character-Render-Records/the-bone-trails.md) named it and declined to
guess: their draw "queues one render command of `0x488` bytes with the VU1 microprogram `0053F490` through the registrar
`003A35E0`", which acquires a node through `0020E680`, builds through `001DB840` and commits with a tail jump to
`0020E630` — *whether that command is ever consumed* was left open as an append-versus-drain question. **It is consumed,
and its two halves happen at different times.**

**`001DB840` ends by running the packet itself.** Its last two calls are `002105C0` (result into the command's byte
`+0x638`) and **`001FB840(node)`** at `001DBA18`; `001FB840` promotes `node+8` to `node+0` and **tail-jumps the command's
vtable slot 0** — for `GiVmax` that is `001DB550`, the interpreter loop of §2.1. So the VIF1 packet is decoded, MSCAL
calls the microprogram, and the GS output is collected into the command's chunked buffers **before the registrar
returns**. ([The Gi family page](../Gi-Render-Commands/gi-render-command-family.md) §12b establishes `001FB840` and
"slot 0 = prepare, at emit time" from the general side; what is added here is that for a VU1 command *prepare is the
whole program run*.)

**Two shared globals make that mandatory rather than incidental.** `001DB840` builds the packet as chunk descriptors of
`{pointer, length}`, and the first two point at **image-wide scratch**:

| chunk | pointer | length | contents | site |
|---|---|---:|---|---|
| 1 | `01F82D08` | 8 | the registrar's **first two arguments**, rewritten there on every call | `001DB8DD`–`001DB8F0` |
| 2 | `01DFD038` | `0x10` | the constant VIF word **`0x4A000000` = MPG**, and at `+8` **the microprogram pointer** | `001DB964`–`001DB970` |
| 3 | the caller's | the caller's | the payload, appended by `001DB340` | `001DB9CF`–`001DB9E8` |
| 4 | the caller's | the caller's | a second payload, only when arguments 7 and 8 are non-null | `001DB9ED`–`001DBA05` |

A whole-image RIP sweep of `01DFD038`–`01DFD048` and `01F82D08`–`01F82D10` finds **`001DB840` and nothing else** touching
either. The chunk holds the *pointer*, not a copy, so a second registrar call overwrites the first call's packet header;
the packet must be consumed inside the call, which is exactly what `001FB840` does. **The MPG word is never written** —
only its `+8` program pointer is — so every VU1 command in the game uploads its program at **VU address 0**.

**So `003A35E0(vifWord1, vifWord2, program, payload, payloadSize)` takes two literal VIF1 command words**, and the
interpreter's MPG case (§2.1) installs `program` where a later MSCAL in the payload will find it.

**What is deferred is the GS replay — slot 1 — and it goes through a per-frame list.** After `001DB840` returns,
`003A35E0` tail-jumps `0020E630(node, 2)`, and `0020E630` is not a mode switch but a **category encoder**:

| mode | mask passed on | site |
|---:|---:|---|
| 0 | `8` | `0020E639` |
| 1 | `0x20` | `0020E646` |
| 2 | `0x40` | `0020E653` |
| 3 | `0x20` | `0020E65B`–`0020E663` |
| other | `0` | `0020E630`, `0020E667` |

`001FB810` then passes `(the command, mask)` to `001A17F0`, whose default handler is
`GeometryRenderTargetImmediate` (`001F48B0`); that wraps the command in a `0x28`-byte record carrying the mask at
`+0x20` and **appends it to an EASTL vector held in the global `01F7F5E0`**. The vector is drained by the **render pass
list `00187950`** — application slot 8's render path
([the game application](../../00-Engine-Core-Runtime/Application-Root/game-application.md) §3) — which calls
`0018B100(list, whole, device)` twice a frame. `0018B100` asks each record for its mask (slot 2, `001F49E0`), tests it
against the list's own `+0x20`, and only then calls slot 1 with the device. **A mode of 4 or more therefore produces a
record that can never run**, because `test mask, 0` is always zero.

**Census of the 31 submit sites** (every `call`/`jmp` to `0020E630` in the listed bodies, mode read back from the last
write to `edx` within 24 instructions): **18 use mode 2**, 2 use mode 0 (`001D8BB0`, `001EB800`), 10 forward a
caller-supplied mode — the eight `Gi*` arena factories at `0086xxxx` plus `GiBeginScene`/`GiEndScene`
(`001FBD80`/`001FBE50`) — and one computes it (`0039D890`, `lea edx, [rbp + 2]`). So **`0x40` is the ordinary category
for this family** and the two other constants are the exception.

**The two VU1 registrars differ only in when the submit happens, not in when the program runs.**

| | `003A34D0` | `003A35E0` |
|---|---|---|
| builds the command | `001DB840` (`003A35B9`) | `001DB840` (`003A363D`) |
| runs the program | **yes, inside `001DB840`** | **yes, inside `001DB840`** |
| submits slot 1 | **deferred** — stores the node at `record+0x18` of the sorted draw list `[02F8F2F8]`, count `02F8F2C6` (`003A34F3`–`003A3515`, `003A35CB`), for `003A3740` to submit | **immediately** — tail jump to `0020E630(node, 2)` (`003A3664`) |

`003A34D0` is therefore the *sorted* registrar and `003A35E0` the *unsorted* one; a `003A35E0` command **never enters the
draw list at `02F8F2F8`** and so is never sorted against the effect elements
([the effect-element dispatch](../Effect-File-Formats/effect-element-type-dispatch.md) reads that list's append, drain
and rewind).

**One neighbour of that drain crosses a layer line.** The render pass list `00187950` also calls the singleton getter
pair `00182E80` / `00182EB0`, which the function list still tags **Audio**
([the ownership boundary](../../00-Engine-Core-Runtime/Ownership-Boundary/intentionally-ownerless-functions-and-shared-scratch.md)
already rows them as a reclassify pair). Each tests the framework singleton, forwards it to a four-byte field reader
when it exists, and otherwise returns a constant — `0x438` and `0x780`, 1080 and 1920 — so the pair reads like
**display height and width**, and the Audio tag like an ownership artefact rather than a sound path. *That last step is
an inference from the two constants; the ownership page reads the same fallbacks as IDs.*

**A third entry point, and the layer's biggest customer.** `001DB7E0` takes the same `0x640` bytes from the same
arena and constructs the same `GiVmax` **with no packets of its own**, for a caller that appends them itself. Its two
callers are `00540DB0` and `00540C70`, the finalisers every effect element type reaches
([effect element type dispatch](../Effect-File-Formats/effect-element-type-dispatch.md)): the element measures a
packet, builds it into the frame arena at `02F8F2D0`, and `00540DB0` walks the resulting chunk table appending each
chunk with `001DB340` before tail-jumping `0020E670` — a thunk to `001FB840`, so the same slot-0 run happens there.
**So the effect system draws through this layer too**, and the `0x4A000000` MPG chunk is not built for it: the
element's own packet carries its program.

**Not read here:** the render-thread command stream that `001F49F0` hands the replay to — see the Gi family page §12e,
where the remaining gap is now stated; `001DB640`/`001DB660` beyond §2.1a; what `002105C0` measures.

### 2.1b The GS translator — which GS registers the PC port honours

`0020F3E0` handles one PACKED GIF packet. For each register slot:
1. It takes the slot's 4-bit descriptor from the tag's REGS field (`0020F451`–`0020F47D`).
2. Unless the descriptor is 1–5 or `0xE`, it first flushes the pending batch (`0020F480`–`0020F49A`).
3. It dispatches through a byte map at `0020FB28` (descriptor `0`–`0x4F` → case) and an offset table at `0020FAD4` (both jump-table data inside `.text`, after the function)
   (`0020F4A1`–`0020F4BD`).

**Twenty cases have handlers; every other register id falls through to one shared "ignore" target, `0020FA6F`:**

| case | GS register(s) | handler |
|---|---|---|
| 0 | PRIM | `0020F4C2` |
| 1–5 | RGBAQ, ST, UV, XYZF2, XYZ2 | `0020F55F`, `0020F5AA`, `0020F61E`, `0020F66B`, `0020F6B5` |
| 6–10 | TEX0_1, TEX0_2, CLAMP_1, CLAMP_2, FOG | `0020F97F`–`0020F9C7` |
| 11 | A+D (address + data) | `0020F9F0` → `0020FCA0` |
| 12, 13 | TEXA, TEXFLUSH | `0020F9FA`, `0020FA09` |
| 14–19 | ALPHA_1/2, TEST_1/2, ZBUF_1/2 | `0020FA17`–`0020FA62` |
| — (60 ids) | everything else, including FRAME, SCISSOR, XYOFFSET, TEX1, PRMODE/PRMODECONT, COLCLAMP, DTHE, FBA, PABE, DIMX, TEXCLUT, MIPTBP | ignored (`0020FA6F`) |

**The vertex kick (XYZ2, `0020F6B5`).**
1. At `0x2AA` = 682 pending vertices, the batch is flushed through `0020EC80` (`0020F6D6`–`0020F6DE`).
2. `00210230` converts the packed coordinate into a **48-byte vertex** at `01FC3620 + n × 48` (`0020F6F6`–`0020F708`):
   - X = bits 0–15 × `0.0625`, Y = bits 32–47 × `0.0625` (`00210274`–`002102AF`; the constant at `008F30EC`) — GS's
     12.4 fixed point;
   - Z = the second qword's bits 4–27;
   - when the byte `01FD3611` is set, the conversion is skipped and three floats are taken directly (`0021024D`–`00210267`).
   - *Added 2026-09-27 (FABLE, Claude Opus 5.5), on `ASTRA-RETURN-FABLE-GS-COORDINATE-CONVERSION`, read again from the
     bytes:*
     - **Only the packed path bounds Z.** It clamps Z first to the upper float at `01FD3664`, then to the lower at
       `01FD3660` (`002102B8`–`002102D2`), so with inverted bounds the lower one wins. The direct-float path skips both.
     - **Both paths then run the same transform.** `0020EA50` builds (X, Y, Z, 1), with X/Y/Z reordered from the
       converter's temporary. It writes four colour bytes as unnormalised floats at `+0x10`–`+0x1C`; there is no
       ÷ 255, and which byte is which channel is not established.
     - **Matrix.** The call at `0020EAD3` multiplies by the matrix at `01FD3620` through the leaf `00217060`:
       `out[j] = X·m[j] + Y·m[4+j] + Z·m[8+j] + W·m[12+j]`. That is a row vector times a row-major matrix, or
       equivalently a column-major matrix times a column vector. The conventional row-major matrix times a column
       vector would transpose it.
     - **Rounding order.** Each output is summed as (Y·m + X·m), then + Z·m, then + W·m, each product rounded to f32.
       A reimplementation that reorders the sum is not bit-exact. The same leaf and convention serve `EXP-219`
       (`ASTRA-RETURN-FABLE-MATRIX-APPLICATION-CONVENTION`).
     - **Divide.** XYZ is divided by the transformed W, and W is replaced by W / W (`0020EAD8`–`0020EB0C`). A zero or
       NaN W is not examined.
     - **UV.** The byte `01F8357F` selects one of two stored UV pairs into `+0x20` / `+0x24`.
     - **Tail.** `+0x28`–`+0x2F` of the 48-byte vertex is not written on this path. That does not make it padding.
3. PRIM's low three bits (the GS primitive type) select one of seven index generators through the jump table at `0020FB78` (data inside `.text`)
   (`0020F721`–`0020F741`). They append u16 indices to `01FCB610` (count `01F83564`); `n` is the vertex count
   `01F83568` after the new vertex:

   | PRIM type | arm | indices written |
   |---|---|---|
   | 0 point | `0020F743` | `n−1` |
   | 1 line, 2 line strip | `0020F769` | `n−2, n−1` |
   | 3 triangle, 4 triangle strip | `0020F79F` | `n−3, n−2, n−1` |
   | 5 triangle fan | `0020F7BD` | index `0` (the fan's first vertex; the index count is checked against `0x8000` at `0020F7D4`), then `n−2, n−1` |
   | 6 sprite | `0020F819` | the two GS corner vertices become four (`0020F887`–`0020F933`), then six indices: two triangles |

   Only one arm serves line and line strip, and one serves triangle and triangle strip, so list-versus-strip must be
   decided before the index arm. ~~The likely place is `00210230`'s return value, which gates the arms at `0020F70D`;
   that is not read.~~ **Read 2026-09-27 (FABLE, Claude Opus 5.5), on `ASTRA-RETURN-FABLE-GS-PRIMITIVE-READINESS`.**
   The separation is a saturating phase counter. The steps:
   - **PRIM.** Writing PRIM (`0020FE70`) stores the type at `01F83562` (`0020FE7B`) and calls `0020FBA0`. That sets
     the vertices a primitive needs (`01F83570`) and the carry (`01F8356C`). The caller then zeroes the phase
     (`01F83574`) and the vertex count (`0020FEF5` / `0020FEFB`).
   - **Each XYZ2** increments the phase, saturating it at the requirement (`0020F6C1`–`0020F6D0`, a signed `cmovg`).
   - **The readiness test.** After the vertex is written, `002102E8` answers true only when bit 47 of the XYZ2
     qword's upper half is clear and the phase equals the requirement.
   - **On true**, `0020F70D` resets the phase to the carry before dispatching the index arm. On false it skips the
     arm (`0020FA6F`).

   | PRIM | requirement | carry | ready on vertices 1–6 |
   |---|---:|---:|---|
   | 0 point | 1 | 0 | 1 1 1 1 1 1 |
   | 1 line | 2 | 0 | 0 1 0 1 0 1 |
   | 2 line strip | 2 | 1 | 0 1 1 1 1 1 |
   | 3 triangle | 3 | 0 | 0 0 1 0 0 1 |
   | 4 triangle strip | 3 | 2 | 0 0 1 1 1 1 |
   | 5 triangle fan | 3 | 2 | 0 0 1 1 1 1 (the leaf also sets the fan flag `01F83561`) |
   | 6 sprite | 2 | 0 | 0 1 0 1 0 1 |

   So lists reset after each shape, and strips and fans keep one or two vertices of progress. The bit-47 flag
   (GS ADC) suppresses a ready answer without resetting the phase: with ADC on a triangle list's third vertex, the
   fourth vertex is the one that completes.

   The leaf also stores `01F83578` (0 point, 1 line, 2 triangle or sprite); its reader is not traced here. PRIM 7
   changes none of these words. ASTRA executed the counter components in isolation, with vertex conversion,
   geometry and drawing omitted. The table is those transitions, which the code above also gives statically.
4. **The flush `0020EC80`** handles the batch:
   - it draws through `0020ED30` and then `0020EB60(lastIndex + 1, device)` (`0020EC9E`–`0020ECAD`);
   - it resets the index count (`0020ECB2`);
   - when the vertex buffer is full, it carries the unfinished primitive's trailing vertices to the front (`memcpy`,
     `0020ECCA`–`0020ED1A`).
5. **`0020EB60` submits the batch** through the object at `[01FC35F8]`:
   - it copies the 48-byte vertices (`0020EBE1`–`0020EC0C`, `memcpy` from `01FC3620`);
   - it copies the indices (`0020EC0F`–`0020EC45`, `memcpy` from `01FCB610`);
   - it draws through that object's slot `+0x28` (`0020EC67`).
   The object's class is not identified here.
6. **`0020ED30` selects draw state.** Among other checks, it calls `0020F250`, which looks up a 16-byte texture
   entry in the table `01F83580`. The key is `(TEX0 >> 37) & 0x3FFF` (`0020F260`–`0020F274`), and the lookup applies
   only when `TEX0 & 0x3F00000` is at least `0x300000` (`0020F253`–`0020F25E`).

**Not read:** ~~how list and strip variants are separated~~ (read 2026-09-27, item 3), the rest of `0020ED30`'s state selection, the class behind
`[01FC35F8]`, and what the individual state handlers store.

### 2.2 The machine state

| address | size | role | evidence |
|---|---:|---|---|
| `02064E30`–`02068E30` | `0x4000` | **VU memory: 1,024 cells of 16 bytes**, indexed `cell << 4` | `0022C95A`; the microprograms' `shl eax,4` / `[idx + 02064E30]` (e.g. `004804F0`–`004804FB`) |
| `02064B00`–`02064E30` | — | microprogram working registers: 16-bit words used as cell indices (`02064B0C`, `02064DB0`, `02064DB4`, `02064DB8`, `02064DD0`) and float scratch | 1,591 references in `004B1190` alone |
| `02064DEC` | u16 | status flags, set **only** by `0022CC40` (`|= 0x40`) and `0022CC30` (`|= 0x80`) | the only two writers (rip census) |
| `02068E30` | ~~1,024 × 8~~ **room for 16,384 × 8** (`0x20000` bytes to `02088E30`); *the code does not bound the index* | installed-program table (the "micro memory"). *Corrected 2026-09-25 (FABLE, Claude Opus 5.5), on OPUS block 277:* the MPG arm indexes it with the command's **unmasked** imm16 (`0022CA45 movzx ecx, bx` → `0022CA4F mov [r9 + rcx*8], rax`); the only `0x3FF` masks in `0022C970` are the OFFSET and BASE arms' (`0022CA09`, `0022CA2D`), and nothing references `02068E31`–`02088E2F`. | `0022CA4F`, `0022CB1E` |
| `02088E30`–`02088E50` | — | VIF registers: BASE, OFFSET, a status word, WL, CYCLE, installed count | §2.1 |

The status helpers run on arithmetic outcomes. `004804A0` compares a result with 0 and calls `0022CC40` when it is
zero (`004805A2`) and `0022CC30` when it is negative (`004805B4`). **`0x40` / `0x80` are the positions of the VU
status register's sticky Z and sticky S flags.** Forty functions call them, including 24 of the 35 template-installed programs (§2.3).

### 2.3 How programs get installed — two packet builders

**Packet templates.** `008631E0(packet, program, addr)` appends a 16-byte `(0x4A000000 | addr, program)` record to
`02EAF930` (count `02EB37B0`). It writes a reference to that record into the packet (`00863206`–`0086322B`).
37 functions call it, one site each, installing **35 distinct programs**, all at address 0.

A typical caller, `00476C80`, builds a whole PS2-style packet in place:
1. MPG `004758E0` (`00476C89`–`00476C93`);
2. BASE 0 and OFFSET 0 (`0x3000000` / `0x2000000`);
3. STCYCL 4,4 (`0x1000404`);
4. UNPACK `0x6C`, 0x42 items (`0x6C420000`), followed by vertex floats that include **`2048.0`** (`0x45000000`), the
   centre of the PS2 GS drawing area;
5. GS register writes;
6. MSCALF 0 (`0x15000000`, `00476E4D`) and FLUSHA (`0x13000000`, `00476E57`).

**Render-command registration.** `003A34D0` / `003A35E0` take a program pointer (`r9` / `r8`) and pass it to
`001DB840`. That function appends the static MPG template at `01DFD038` (`0x4A000000`) and stores the program at
`01DFD040` (`001DB964`–`001DB970`). ~~76~~ 72 *(corrected 2026-09-27, FABLE, Claude Opus 5.5: 45 + 27)* call sites register **29 programs**; 17 are shared with the template path, so
this path adds 12. For example, `0044E530` registers `004804A0` at `0044E8D9`–`0044E8E0`.

**Together: ~~47~~ 57 distinct microprograms** *(corrected 2026-09-27, FABLE, Claude Opus 5.5: the ten registered only through `003A33B0` / `003A2F70` - `00499A20`, `0049B9E0`, `0049D540`, `004A0090`, `004A1E30`, `004A33B0`, `004A4410`, `004A8B00`, `004AAFC0`, `004B0230` - were missed; [record](../../_index/candidates/uq213-microprogram-draws/README.md))*, all ARCH frontier. 35 of them total 329,225 B, including the largest
functions in the region (`004B1190` 32,136 B, `004C8320`, `004F7070`, `004EF940`, `004E31E0`, `004E7D90`).

### 2.4 The startup "float-table builders" are pre-built VIF packets

The `0x480000` builder page's 66 startup objects (**BH-1**) are packet templates of the kind above. The census
(`vif_tags.py`) scanned immediate dword stores for VIF1 command values:

| group | functions | store STCYCL **and** MSCAL/MSCALF | other VIF codes |
|---|---:|---:|---|
| startup hub targets (`0037DF90` / `0037E0F0`) | 76 | **49** | BASE 58, OFFSET 58, UNPACK 63, FLUSHE 56, DIRECT 28 |
| MPG packet builders (§2.3) | 37 | 24 | BASE 37, OFFSET 37, UNPACK 28 |
| control: 300 random functions of 300–3,000 B | 300 | **0** | FLUSHE 10, FLUSHA 2 (common constants) |

The builders "store immediate constants" (83 % `mov`) because a VIF packet *is* constants: command words, vertex
data, GS register values.

### 2.4a The template census — every immediate store accounted

[`vif1-packet-templates.tsv`](vif1-packet-templates.tsv) decodes all **77 template rows** (generator
[`members/gen_vif_templates.py`](members/gen_vif_templates.py) over `members/vif_templates.py`; re-run reproduces
it byte-for-byte). The
population reconciles the two earlier counts: the hubs make **77 calls, not 66** — 68 in-region
(`0x480000`–`0x500000`, the §2.4 objects; one builder, `004E3110`, is called twice with two objects, giving 67
distinct in-region builders) plus **9 out-of-region calls** the earlier census filtered out: six MPG builders
(`00476C80`, `004791E0`, `004795D0`, `0047A800`, `0047BAF0`, `002EFF50`) and three plain builders (`0047E140`,
`00479450`, `002F0110`). All nine still receive a `.data` object pointer in `rcx`. Two of the in-region calls are
`E9` tail-jumps, which the first census's call-only scan missed *(corrected 2026-09-27, SWE2-DATA, on FABLE's
byte check): `0037E0E3 jmp 004A8860` with `rcx = 02AE1EF0` set at `0037E0D8`, and `0037E33F jmp 004C3610` with
`rcx = 02AEAFC0` set at `0037E334` — verified in the image. There are therefore no `mpg-solo` rows; both
builders are hub-called.* The union is 76 distinct builders /
77 distinct objects, and 31 of the in-region builders are dual-role (build an object *and* emit an MPG record via
`008631E0`).

Per row: destination object, memset size, the ordered command stream, MPG program/address, and the GS register
writes. Command totals across all rows: STCYCL 87, UNPACK 87, BASE 58, OFFSET 58, MSCALF 50, FLUSHA 50, DIRECT 29,
FLUSH 26. The dominant shapes are `BASE → OFFSET → STCYCL → UNPACK → MSCALF → FLUSHA` (19 rows) and variants with a
`DIRECT n` carrier before the final FLUSHA (29 rows carry one DIRECT each); 21 rows are pure data-upload templates
that end inside their UNPACK payload with no
baked trailer. Object headers: `0x30` on exactly the 37 MPG rows (stamped by `008631E0`), `0x10` on 19 rows
(`008631D0`), absent on 21. 31 rows carry an embedded `008631D0` sub-header at `+0x10` — the helper stamps
`word=count, kind=0x10` over a NOP dword, so the final object reads `0x10WWWWWW` at that slot (shown as `SUBHDR`
in the TSV). The interpreter has no `0x10` case — it is a transparent no-op slot to `0022C970`, while the word
carries the record's item count for CPU-side readers (it tracks the UNPACK item totals — `w=17` = `num=17` on
`00499850`; on the rest it runs the item total plus a small record overhead, e.g. `w=197` vs `55+120+20=195`
items on `004B8F20`).
The `0x10000000` immediate stores the §2.4 raw scan counted as FLUSHE are payload data — none sits at a stream
position the interpreter treats as a command.

**GS register writes are rare in the templates themselves.** DIRECT payloads are GIF packets, but 28 of 29 decode
to empty terminators — only `004C2040` carries a real write (`CLAMP_1=0`). Two further templates (`00476C80`,
`0047BAF0`) end their UNPACK payload with literal `{qword reg-id, qword value}` pairs — `ST=0, CLAMP_1=0,
RGBAQ=0, XYZF2=0` — matching the tail of the §2.3 worked example. Everything else inside the UNPACK payloads is
VU-image data consumed by the installed microprogram at MSCAL time; any GS writes it produces are emitted by that
compiled code, not statically present in the template.

**Store-accounting control:** every immediate store in all 77 builders lands either on a command-word position or
inside a payload span covered by a decoded command — **zero unattributed stores** (the header/sub-header stores by
`008631D0`/`008631E0` are tracked separately, not counted as packet bytes).

### 2.4b Who copies these templates at run time — six of them are effect-element prototypes (FABLE, Claude Opus 5, 2026-09-20)

§2.4a decodes all 77 template rows; **it does not say who uses one.** Six rows are prototypes for the draw of an
**effect element type** ([effect element type dispatch](../Effect-File-Formats/effect-element-type-dispatch.md)), and
the run-time builders there copy one and rewrite it.

**A template is a prototype, not the packet that ships.** `00542100`, type `'h'`'s builder, copies `02AEB610`'s
`0x200` bytes onto the stack (`00542152`) and then lays the arena block's descriptor table down from that copy:

- the row's `0x30` object header — **the MPG descriptor for `004DF440`** — goes down **verbatim** at the block's
  `+0x00`, so the program registration is carried through untouched;
- the row's `+0x10` sub-header (`w=0x1E`, stamped by `008631D0`) is copied to `+0x10` and then **re-tagged to `0x30`
  and re-pointed** at the payload the builder has just written at `+0x50` (`00542443`–`00542454`);
- the 16-byte row `02AEB810` — **the MPG descriptor for `004E0F70`** — is copied in whole at `+0x20` (`0054245A`);
- two more descriptors follow at `+0x30` and `+0x40`, the second inline with `STCYCL CYCLE=4 WL=4` in its prefix.

*So the startup object supplies the program registrations and the packet skeleton, and the run-time builder supplies
the data.* The row's own tiling is exact and is what the `00540DB0` walk consumes: `0x18 + 0x1E × 0x10 + 8 = 0x200`.

**Which element type runs which program.** Measured by taking each type builder's rip-relative references into
`02AE0000`–`02AF0000`, matching them to the startup hub's `(object, builder)` pairs, and reading the `008631E0`
program out of each builder:

| element type | template rows | their builders | the microprograms it installs |
|---|---|---|---|
| `'h'` `0x68` | `02AEB610`, `02AEB810` | `004E2930`, `004E2C90` | **`004DF440`** (6,957 B), **`004E0F70`** (6,587 B) |
| `'i'` `0x69` | `02AEB0F0`, `02AEB290` | `004DCA00`, `004DC8C0` | **`004DCC00`** (4,581 B), **`004DDDF0`** (5,479 B) |
| `0xA3` | `02AEA270` | `004DC6B0` | **`004DB350`** (4,953 B) |
| `0xA6`, `0xA8` | `02AE9BC0` | `004DADD0` | **`004DA8A0`** (1,327 B) — shared by both types |
| `'j'` `0x6A` | `02AE9130` | `004DA610` | **`004D7BF0`** (10,177 B) |

The other objects these builders touch carry no program: `02AEB2A0` (`004DC8F0`), `02AE9D50` (`004DA650`),
`02AE9EE0` (`004DB060`) and `02AEB820` (`004E2CD0`) are data-only rows, and type `'j'` additionally reads eight
`02AE92xx` objects the startup hub never registers.

**So seven of the ~~47~~ 57 microprograms have a named runner.** Not what they draw — ~~**UQ-213 stays open**~~ *UQ-213 is
answered, 2026-09-27 (FABLE, Claude Opus 5.5), at its box* — but *which
element type invokes them*, which is the coordinate a reader needs before opening a 6,957-byte body.

**One figure re-derived, because pass 1 asked for it.** This page's `audit.last_pass_state` records "the 329,225 B
total for the 35 template-path programs" as **NOT CHECKED**. An independent enumeration — every call site of
`008631E0` in the listed bodies, taking the program from the `lea rdx` that precedes it — gives **37 sites, 35
distinct programs, 329,225 bytes**, and its six largest are `004B1190` 32,136, `004C8320` 28,422, `004F7070` 24,541,
`004EF940` 22,073, `004E31E0` 18,098 and `004E7D90` 15,212, in that order. **Both figures reproduce**, through the
registrar rather than through the function list. *Thirty of the 35 lie in `00480000`–`00500000`; the five outside are
`002F0280`, `004758E0`, `00478280`, `00479650` and `0047A9C0`.*

**Not read here:** what any of the seven draws; the eight `02AE92xx` objects type `'j'` reads; whether the two
programs a type installs run in one MSCALF each or one of them is a fallback.

### 2.4c Every template's GIF tag, read out of its own bytes — the population (FABLE, Claude Opus 5, 2026-09-20)

§2.4b ends on "what any of the seven draws" being unread. **Most of it is readable statically**, because of what
[the bone trails](../Character-Render-Records/the-bone-trails.md) §5d found in one program: the microprogram
*stamps* `NLOOP` at emit time but **copies `PRIM`, `FLG`, `NREG` and `REGS` from a VU cell its template uploaded**.
The register list is authored data. §5e decoded one such cell by hand; this applies the same decode to **all 74
hub-called builders**.

**Method.** Replay each builder's immediate stores into a byte image, find its `UNPACK` command words, and decode
every 16-byte payload quadword as a candidate GIF tag, accepting only quadwords whose reserved bits 16–45 are zero,
whose `FLG` is `PACKED`, whose `PRIM` type is ≤ 6 and whose `NREG` descriptors all name real registers. Generator
[`members/gen_gif_tags.py`](members/gen_gif_tags.py) → [`members/vif1-gif-tags.tsv`](members/vif1-gif-tags.tsv).
*The image is each builder's own store extent, not a fixed window* — the first version of this used a `0x600`
window and silently truncated the largest templates, losing one register-write tag, so the figures below are the
ones a size-independent run gives.

**Both controls, reported as measured.**

| control | result |
|---|---|
| **positive** — `005409C0`, the trail template §5e decoded by hand | reproduces that decode exactly; asserted, the tool refuses to write its table otherwise |
| **negative** — the same predicate over 150 ordinary functions of > 400 B in `00300000`–`00500000` | **4 accept — a 2.7 % base rate** |

*The predicate is not perfectly specific, and the threshold was not moved to make it look so.* Against that base
rate, ~~**45 of the 74 builders (61 %) carry at least one tag**~~ *(corrected 2026-09-27, FABLE, Claude Opus 5.5: sixteen more carry one, e.g. `00476C80`, `004795D0`, `004A8860`, `004C3610` - so at least 61; [record](../../_index/candidates/uq213-microprogram-draws/README.md))*.

**And the 29 that carry none mostly cannot.** **21 of them author no `UNPACK` command at all** — a template with
no payload has nowhere to keep a tag — leaving **8** that upload a payload and still yield nothing. *That is the
honest size of the unexplained remainder: eight builders, not thirty.* A tag reaching VU memory by a route the
replay does not model, a `memcpy` or a computed store, would still read as empty, so those eight were left
unresolved when §2.4c was written. **They have since been read, and the residual is zero** — §2.4d. *(These 21 are **not** §2.4a's 21 pure data-upload rows — those end **inside**
an `UNPACK` payload, so they have one. The two counts coinciding is a coincidence.)*

**The 75 tags split almost exactly in half, and the halves do different jobs.**

| | count | `PRE` | what it is |
|---|---:|---|---|
| `NREG 1`, descriptor **`A+D`** | **38** | **0 in all 38** | a **GS register write** packet — `NLOOP` register writes, no drawing |
| `NREG ≥ 2`, vertex registers | **37** | 1 in 36 of 37 | a **vertex list** — the primitive and the per-vertex register layout |

*`PRE = 0` means the tag does not write `PRIM`, so on the register-write half the `PRIM` field is not a primitive
and is not reported as one.*

**This bounds §2.4a's "GS register writes are rare in the templates themselves."** That sentence is about **DIRECT**
payloads, and there it holds — 28 of 29 are empty terminators. It does **not** generalise: the **UNPACK** payloads
carry **96 register-write slots**, and they name only four registers.

| register | slots | of those, carrying a value |
|---|---:|---:|
| `CLAMP_1` (`0x08`) — texture wrap | 26 | 1 |
| `TEST_1` (`0x47`) — alpha / depth test | 23 | 10 |
| `TEX0_1` (`0x06`) — texture buffer + function | 23 | 0 |
| `ALPHA_1` (`0x42`) — blend equation | 22 | 8 |
| `PRIM` (`0x00`) | 1 | 1 (`0x5D`) |
| id `0x0E` — **not a GS register**, see the last paragraph | 1 | 0 |

**20 slots carry a value; 76 name a register and hold zero** — a named placeholder the run-time builder fills, which
is the same division of labour §2.4b found for the descriptor table. *The register ids are corroborated
independently:* [one coloured rectangle](../../99-Unresolved-Residual/drawing-one-coloured-rectangle.md) decodes
`0x47` as `TEST_1` and `0x42` as `ALPHA_1` out of an unrelated packet, and the
`ZTE` / `ZTST` bit positions used here are the ones an earlier pass confirmed on `TEST_1 = 0x50000`.

**Every authored `TEST_1` is the same configuration:** `ATE = 1` with `ATST = NEVER` and `AFAIL` ∈ {`RGB_ONLY`,
`FB_ONLY`}, `ZTE = 1`, `ZTST` `GEQUAL` (8) or `ALWAYS` (2). An alpha test that never passes, with `AFAIL` choosing
what still gets written, is **the PS2 idiom for drawing colour while leaving the Z buffer alone**. **And every
authored `ALPHA_1` is one of three equations** — `0x48` = `Cs·As + Cd` (additive, 5 templates), `0x44` =
`(Cs−Cd)·As + Cd` (the ordinary lerp, 2), `0x42` = `Cd − Cs·As` (subtractive, 1).

**The vertex-list half uses eleven shapes.** `FGE` is clear on all 37 and `ABE` is set on all 36 that write `PRIM`:

| × | primitive | `NREG` | `REGS` |
|---:|---|---:|---|
| 9 | `TRIANGLE_STRIP` | 6 | `ST, RGBAQ, XYZF2` × 2 |
| 7 | `LINE` | 4 | `RGBAQ, XYZF2` × 2 |
| 6 | `TRIANGLE_STRIP` | 3 | `ST, RGBAQ, XYZF2` |
| 4 | `POINT` | 2 | `RGBAQ, XYZF2` |
| 3 | `LINE_STRIP` | 2 | `RGBAQ, XYZF2` |
| 2 | `LINE` | 6 | `ST, RGBAQ, XYZF2` × 2 |
| 1 each | `SPRITE` 5, `TRIANGLE_FAN` 3, `TRIANGLE` 4, `TRIANGLE_STRIP` 5, `TRIANGLE_FAN` 5 | | |

**28 of the 37 carry `NLOOP = 0`** — the count is stamped at emit time, exactly as §5d read off the trail's
epilogue. **Nine carry an authored count**, and five of those are the *same* packet in five different builders:
`004802F0`, `00482410`, `00487BA0`, `004956A0`, `004978F0`, each **`NLOOP = 240`, `PRIM 0x049` = Gouraud-shaded
alpha-blended untextured `LINE`, `RGBAQ, XYZF2` × 2** — a fixed 240-segment line packet, complete in the template.

**Joined to §2.4b's element-type map, four of the five types get a primitive:**

| element type | its row | the tag in that row |
|---|---|---|
| `'h'` `0x68` | `02AEB610` | `TRIANGLE_STRIP`, IIP + TME + ABE, `NREG 6`, `ST, RGBAQ, XYZF2` × 2 |
| `'i'` `0x69` | `02AEB0F0` | **the same tag, field for field** |
| `0xA3` | `02AEA270` | `LINE`, IIP + ABE, untextured, `NREG 4`, `RGBAQ, XYZF2` × 2 |
| `0xA6`, `0xA8` | `02AE9BC0` | `NLOOP = 10`, `NREG 3`, `ST, RGBAQ, XYZF2`, **`PRE = 0`** — ~~ten vertices under whatever `PRIM` the GS already holds~~ *(corrected 2026-09-27, FABLE, Claude Opus 5.5: `004DA8A0` first kicks (`004DA8F5`) the A+D block of `02AE9D50` that ends in PRIM = `0x5D` (`vif1-gif-tags.tsv`), so the ten vertices form a triangle fan)* |
| `'j'` `0x6A` | `02AE9130` | ~~none found~~ *(corrected 2026-09-27, FABLE, Claude Opus 5.5: the tag is in the co-template `02AE9140`, builder `004DA460`: cell 0, `0x05C`, NREG 6)* |

**And the trail's tag is one of these.** `005409C0` builds a *pool* template (`02CA8A90`), nothing to do with the
startup rows — yet its tag is identical in every decoded field to `02AEB610`'s, type `'h'`'s prototype. *That is a
shared authored drawing convention appearing in two independently built templates.* **It is not evidence that the
trail is a type `'h'` element**, and nothing here tests that.

**What this does and does not settle for `UQ-213`.** It names, for 37 packets, **the primitive and the register
each vertex quadword carries**. It says **nothing about what the values mean** — what an `ST` pair spans, how
`RGBAQ` combines with authored colour — which is the part §5e also left open. **One tag is reported as a probable
false positive rather than dropped:** `00485390` cell 21 decodes as `A+D` but its single payload slot names register
id `0x0E`, which is not a GS register.

### 2.4d The eight read by hand — the sweep has no unexplained residual (FABLE, Claude Opus 5, 2026-09-20)

§2.4c leaves **eight** builders that upload a payload and yield no tag. *A statistical sweep with eight cases it
cannot account for is a sweep with an eight-case escape hatch*, so all eight were read directly. **None contains a
tag.** This is interior hand-reading, not the sweep — different evidence, stated separately.

**Three were read store by store.** `004E3110` (2 payload quadwords), `004D3D60` (4) and `004DA3C0` (3) author
nothing but IEEE floats and small integers — `0x41F00000` = 30.0, `0x40A00000` = 5.0, `0x3F800000` = 1.0,
`0xC1300000` = −11.0, `0x3D3A29C7` ≈ 0.0455, counts `0x05`, `0x16`, `0x20` — and each ends with the same trailer:
`MSCALF`, `FLUSH`, `DIRECT 1`, the `0x8000` empty-terminator quadword, `FLUSHA`. **That is §2.4a's dominant shape
exactly.** There is no tag in them to miss.

**The other five were classified store by store**, each value typed as a VIF command word, a float or an integer:

| builder | stores | VIF cmd | UNPACK | int | float |
|---|---:|---:|---:|---:|---:|
| `002F0110` | 31 | 5 | 1 | 16 | 9 |
| `00476C80` | 16 | 5 | 1 | 7 | 3 |
| `004C7FE0` | 11 | 3 | 1 | 2 | 5 |
| `004D0B50` | 27 | 5 | 1 | 7 | 14 |
| `004E79C0` | 11 | 5 | 1 | 4 | 1 |

Command words plus a float/integer payload; ~~**nothing tag-shaped in any of them.**~~ *(corrected 2026-09-27, FABLE, Claude Opus 5.5: `00476C80` is the exception - its fill loop `00476D01`–`00476DFF` writes an A+D GIF tag at cells 11/26/41/56, `NLOOP 5` / `NREG 1` / `REGS 0xE` at `00476D7B`–`00476D8F`, whose fifth pair is PRIM = `0x5D`)* And `00476C80` is one of the
two rows §2.4a already reports as ending its `UNPACK` payload with literal `{qword reg-id, qword value}` pairs
(`ST=0`, `CLAMP_1=0`, `RGBAQ=0`, `XYZF2=0`) — **raw pairs, not an `A+D` GIF tag**, which is exactly why a tag
decoder passes over it. *An independent page's description and this decoder's silence agree on the same row.*

**So §2.4c's 29 tagless builders are fully accounted:** 21 author no `UNPACK` at all, and the 8 that do contain no
tag. **Bound:** "read" here means every *immediate store* was classified. A payload arriving by a route the replay
does not model would still be invisible — though for these eight the VIF command stream *is* authored, so a second
payload source would have to overwrite bytes the builder itself wrote.

**One hypothesis was tested and failed, and it is recorded because it failed.** Before reading them, the obvious
explanation was that these eight author too little of their declared payload for a tag to land in the authored
part. Measured as authored bytes over declared payload bytes, the eight run at a **36 % median against 51 % for
the 45 builders that do yield a tag** — overlapping distributions, and `004E3110` is **88 %** authored with no tag.
*Sparsity is not the explanation;* it plausibly covers only `00476C80` (6 %) and `004E79C0` (4 %).

### 2.5 The XGKICK-shaped leaf

`004EF860` is the 219-byte leaf of the AC-7 twins. Functions of about the same size sit beside several microprograms
(219 B: `004C4C40`, `004C7F00`, `004CF3B0`, `004D7B10`, `004DB270`, `004DF360`, `004E78A0`; 197 B `004CF280`; 216 B
`004ECB70`). **Form comparison (SWE2-FRONTIER, this pass):** eight of them share `004EF860`'s exact shape —
219 B (216 B for `004ECB70`), exactly one call and it is `call r11` (the indirect GS callback), 14 rip-relative
state accesses. `004CF280` (197 B) does **not** match the form — zero calls, three rip refs; it is a different
kind of leaf. `004EF860` itself:
1. writes a 16-bit word `+ 0x8000` into the VU cell at register `02064DB0` (`004EF8A7`–`004EF8B6`);
2. copies the cell at register `02064DD0` beside it;
3. calls its callback with a pointer into VU memory (`004EF910`).

**Handing a pointer into VU memory to the GS callback is what VU1's XGKICK does.** The shape is read; the claim
that it *is* XGKICK is ~~not yet established (§7)~~ **settled 2026-09-15 (OPUS) and the answer is NO** — the
addressing is VI-style (both operands 16-bit, `shl 4`, against base `02064E30`), but the body also builds the
packet and advances two pointers, which XGKICK does not. It contains the kick; it is not the kick. See `UQ-214`
in §7.

### 2.7 The 2D layer end to end: described twice, drawn once *(synthesis, 2026-09-18, FABLE)*

*This section adds no new reading. It joins five results published on 2026-09-18 into the one account a
reimplementer needs, and says which page carries the evidence for each step. Everything below is static
unless marked.*

**What it is for.** Every flat 2D primitive the menus and HUD draw - a tinted rectangle, a quad with four
vertex colours, a nine-region frame - is issued by a small primitive function that still does what it did
on the PlayStation 2 and then does the PC's work as well.

| step | what happens | state touched | evidence |
|---|---|---|---|
| 0 | **The bracket gate - on some primitives, not all.** The four-colour quad emitter and the nine-region opener return at once unless the draw-bracket flag `0215E6D0` is set; the tinted-rectangle primitive has no such test (the flag's reader census lists five functions and it is not one). The flag is raised by the bracket opener around the widget-tree draw pass and cleared by its close. | reads `0215E6D0` | [cutscene-slot page](../../99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md) UQ-348 |
| 1 | **Inputs.** A draw context: a 4x4 transform in its first 64 bytes, tint bytes, a brightness word `+0x5A` and an alpha word `+0x58` (both on a scale where `0x80` is one), a blend setting `+0x78` and an alpha-test setting `+0x80`; plus the caller's rectangle and up to sixteen colour bytes. | none | [rectangle page](../../99-Unresolved-Residual/drawing-one-coloured-rectangle.md) sections 2 to 4; same cutscene-slot page, UQ-350 |
| 2 | **The PS2 description.** A DMA tag, then VIF1 codes - a padding word, `UNPACK` of four-component 32-bit vectors (transform, colour and position per vertex), a second `UNPACK` of GIF tags (alpha test and blend by address+data, then a four-vertex alpha-blended strip of RGBAQ + XYZF2), `MSCAL` - written at the cursor of one of two ring buffers described at `02EBEFC0`. The points-through-a-matrix call that once filled the positions is an empty function on the PC. | ring cursor advances, 16-byte aligned | cutscene-slot page UQ-347; [glyph page](../../99-Unresolved-Residual/Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md) UQ-365 |
| 3 | **The kick.** Submitting flips the ring index `02EBEFF0` between 0 and 1 and calls a publisher that stores the buffer address, the record count and `0x100` into the single cell `02EBA3F8`, comparing three loads of that same cell in between. It hands the buffer to nothing. | `02EBEFF0`, `02EBA3F8` | [handshake page](../Graphics-Thread-Handshake/the-shared-command-state-word.md) UQ-211 |
| 4 | **The PC description.** The same primitive then drives the immediate-mode batcher on the singleton at `[01F811E8]`: begin (state cleared, colour reset to `0x80` x 4), the two state handles, a topology, a texture *name* (null on the rectangle and nine-region paths; the quad emitter's was not checked), the colour as `(r, g, b, a)`, and the vertices - a strip of `n` becomes `n - 2` triangles of 0x30-byte vertices appended to the current one of 64 batches. Live corners come from the per-point perspective transform, not from step 2. | batcher state `+0x3930`..`+0x3AA0`, batch table `+0x2328`, index `+0x3928` | rectangle page section 4; cutscene-slot page UQ-344 |
| 5 | **The flush.** Ending the primitive walks the batches up to the current index; each becomes one `DynGeoTextureInstance` allocated from the frame's ring arena and driven through its virtual interface (vertex count first). From there it is the dynamic-geometry family's business. | ring arena `[01F7F4C0]` | rectangle page section 4; [DynGeo page](../../16-UI/Dynamic-Geometry-Instances/dyngeo-instance-family.md) |

**What a reimplementation has to reproduce, and what it can drop.** Steps 0, 1, 4 and 5 decide what reaches
the screen. Steps 2 and 3 have no consumer among the functions that reference the ring descriptors, the
staging pointer or the kick cell (rip-relative censuses; the bound is stated on the rectangle page), so a
reimplementation that omits them changes no pixel - but it must keep **step 0 where it exists**, because for the quad emitter and the
nine-region opener the PS2-era bracket flag gates the live path as well: requested outside the bracket they draw
nothing on either back-end, while a tinted rectangle draws regardless. The `0x80`-is-one scale of tint, brightness and alpha is a PS2 convention that survives into step 4
and must be kept.

**Known, unknown, and why.** Known: the packet grammar, the kick, the batcher's state block and flush.
*Not known:* what the batcher's topology table at `008F80F8` and the four integers of its mode setter select;
how `DynGeoTextureInstance` turns a batch into a draw (its page's open box on the 21-slot interface); and
whether any *file-borne* VIF packet exists at all, which is the residue of UQ-215 above. *(2026-09-27, FABLE, Claude Opus 5.5: one does exist, effect type `0x97`'s resource payload, and it never reaches the decoder; see UQ-215's answer.)* *Inference, labelled:*
the PS2 register names in steps 2 and 3 are readings of the values; the one-cell fact and the GIF-tag field
decodes do not depend on them.

## 3. Key addresses

| address | role |
|---|---|
| `0022C940` / `0022C970` | VIF1 interpreter entry / decoder |
| `0022BFF0` | UNPACK |
| `0022C8D0` | the flush MSCAL calls first |
| `0022CC40` / `0022CC30` | VU sticky Z / sticky S |
| `001DB550` | packet-list submit (reached through a data qword) |
| `001DB640` → `001DB660` | GS hand-off callback |
| `008631E0` | MPG record emitter (37 callers) |
| `001DB840` | registration-path packet append with static MPG template `01DFD038` |
| `003A34D0` / `003A35E0` | render-command registrars that install a program |
| `004EF860` | XGKICK-shaped leaf |

## 4. Data structures and formulas

```
VIF command word   [31:24] code  [23:0] parameters
MPG on this port   0x4A000000 | addr   then   u64 function pointer        (PS2: NUM words of microcode)
program call       02068E30[ max{ a in 02088E50 : a <= requested } ]( callback, context )
VU memory          02064E30 + cell * 16,  cell in [0, 1023]
```

## 5. Call chain

```
GiVmax vtable 009007E8 slot 0  ->  001DB550
  -> 0022C940(packet, size, 001DB640, object)
       -> 0022C970  decode
            MPG    -> 02068E30[addr] = program
            UNPACK -> 0022BFF0 -> VU memory
            MSCAL  -> program(callback, context)      47 microprograms, mostly 0x470000-0x500000; also 002F0280, 0053F490
                        -> 0022CC40 / 0022CC30        sticky flags
                        -> 004EF860-shaped leaves      -> callback(pointer into VU memory)
            DIRECT -> callback(data)
  001DB640 -> 001DB660 -> GiVmax +0x228 / +0x430 GIF packet copies
GiVmax vtable 009007E8 slot 1  ->  001DB3D0  ->  00210320(packet, device, flag)   GS emulation (not read)
```

## 6. Modding notes

- **Only 20 GS registers are honoured** (§2.1b). A packet that relies on FRAME, SCISSOR, XYOFFSET, TEX1 filtering or
  PRMODE has that part silently ignored on PC. This is a concrete place to look for PS2-vs-PC visual differences.
- **These visuals are not shaders.** Changing what this path draws means changing a recompiled microprogram or the
  packet data it is fed, not D3D11 shader code.
- **Packet templates are in `.text`, not data.** The startup templates are built into uninitialised `.data` from
  immediates (BH-1), so editing their vertex floats or GS register values means patching instruction operands.
- **XIIOnline:** purely presentation; nothing here is simulation state. It needs no synchronisation.

### 2.6 The member census — every `0x470000`–`0x500000` function classified

[`members/vu1-region-functions.tsv`](members/vu1-region-functions.tsv) lists all **351** listed functions in the
region with a role and an evidence string each (SWE2-FRONTIER `FABLE-REQ-SWE2-FRONTIER-VU1-REGION`; census inputs
are FABLE's `vu1_census.json` + `vu1_registered_programs.json` + the raw E8/E9 edge index):

| role | rows |
|---|---:|
| microprogram (template-path, via `008631E0`) | 34 |
| microprogram (registrar-path, via `003A34D0`/`003A35E0`/`001DB840`) | 28 |
| MPG packet builder | 36 |
| startup template (called only from hubs `0037DF90`/`0037E0F0`) | 73 |
| VU helper — VU-state toucher, not installed | 54 |
| VU helper — sticky-flag user | 40 |
| sub-program (called only from microprograms) | 21 |
| XGKICK-shaped leaf (form-matches `004EF860`) | 9 + the `004EF860` reference |
| other / no caller in E8/E9 index | 149 + 16 |

Rows sum past 351 because roles overlap (a body can be both installed paths, or a builder and a flag user). The
census's frontier-only counts (30/31/36/54/46) are the subset marked `frontier` in FABLE's lists; this TSV covers
every listed function including the `0x470000`–`0x480000` head, which is mostly small non-VU helpers called from
`003Exxxx`/`0046FD00` — honestly labelled `other` with their callers, not attributed to the layer.

**The 54 VU-state touchers are layer-internal.** Asked whether any has a caller that is not a microprogram: only
two have non-microprogram callers at all, and in both cases the callers are themselves touchers — `004A6780` is
called by six sibling touchers (`00499A20`, `0049B9E0`, `0049D540`, `004A0090`, `004A33B0`, `004A4410`) and
`004EF860` by `004EDB50`/`004F5360` (both touchers). The other 33 have only microprogram callers and 19 have no
E8/E9 caller — consistent with VU `JAL`/`JR` sub-programs or install paths not yet found (§7).

## 7. What is not known

- [x] **UQ-213.** What each of the ~~47~~ 57 microprograms draws, and which game feature uses each packet.
      *ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5). The image uses 57 VU1 microprograms: the four registrars register 44, and the
      templates install 35. No program carries a tag of its own; each draws the primitive of the template tag cell it
      selects and stamps. That gives 26 TRIANGLE_STRIP `0x05C`, 6 TRIANGLE_STRIP `0x054`, 6 LINE `0x049`, 5 POINT `0x040`,
      4 TRIANGLE_FAN `0x05D`, 2 LINE `0x059`, 2 LINE_STRIP `0x04A`, 1 TRIANGLE_FAN `0x045` and 1 SPRITE `0x056`. Two more
      are mixed, and two (the first programs of the `0x68` / `0x69` packets) draw nothing themselves. The table names
      each program's users. [Record](../../_index/candidates/uq213-microprogram-draws/README.md), `uq213_programs.py`
      FAILS 0.*
- [x] ~~**UQ-214.** Whether `004EF860` and its copies are exactly XGKICK.~~ **ANSWERED 2026-09-15 (OPUS) — NO: it
      CONTAINS an XGKICK-equivalent kick and is a whole GS packet emitter.** **UQ-214.**
      *Answered by a different discriminator than the one this box proposed, and the proposed one is still undone —
      see below.*
      - **The addressing IS VI-style, which is what §2 wanted and did not have.** Both address operands are 16-bit
        words, sign-extended then `shl 4`, indexing VU memory at base `02064E30`: `02064DD0` at `004EF866`–`004EF877`
        and `02064DB0` at `004EF88B`–`004EF899`. A 16-bit register scaled by 16 to reach VU memory is VI addressing,
        and the callback really does receive that pointer — `rcx = rdx + rbx` at `004EF8A3` survives to `004EF910`.
      - **But XGKICK writes nothing and advances nothing, and most of this body does both.** Before the kick it builds
        into VU memory — a dword at `+0x00` as `word[02064DB8] + 0x8000` (`004EF8A7`–`004EF8B6`), then eight bytes at
        `+0x04` and four at `+0x0C` from a quadword fetched through the other register and staged at `02064C60`
        (`004EF8C8`–`004EF8F2`). After the kick it advances `02064DB0` and `02064DB4` from `word[02064B0C]`
        (`004EF913`–`004EF92E`), around compare-and-conditional-add arithmetic on `0x2A8` and `0x168`.
      - **So the eight form-matched siblings share an emit-and-advance routine, not an instruction.** Calling it
        XGKICK would flatten ~200 bytes of packet construction and pointer management into one operand.
      - **This box's own discriminator — decode the passed cell as a GIF tag and check it against the GS register
        writes that follow — was NOT run.** It bears on *what the packet is*, which stays open; the question of
        whether the function *is* XGKICK did not need it. **Not claimed:** that the `0x2A8`/`0x168` arithmetic is a
        double buffer (the shape of a wrap is reported, the mechanism is not read), or what the `+0x8000` names.
- [x] **UQ-215.** The UNPACK formats `0022BFF0` implements, e.g. `0x6C`.
      *The grid (S / V2 / V3 / V4 x 32 / 16 / 8, plus V4_5) was read by OPUS on 2026-09-15; the register row carries it.*
      *Narrowed 2026-09-18 (FABLE): the three halves OPUS left open on this row, two closed and one bounded.* **The mask flag is ignored.** The decoder tests `(cmd & 0x60) == 0x60`, takes `vn = (cmd >> 2) & 3` and `vl = cmd & 3`, bit 14 as the unsigned flag, bit 15 as the add-TOPS flag, bits 16-23 as NUM and the low ten bits as ADDR (`0022CA73`..`0022CAC7`); bit 4 of the command, VIF's `m`, is never extracted, so `0x7x` decodes exactly as `0x6x` and there is no mask, row or column register anywhere in the decoder's state. **The `V4_5` arm is RGBA 5:5:5:1 as on the PS2:** one 16-bit word gives `(w & 0x1F) << 3`, `(w >> 2) & 0xF8`, `(w >> 7) & 0xF8` and `(w >> 8) & 0x80`, so the top bit becomes alpha `0x80` (`0022C840`..`0022C87F`). The unsigned flag is tested in each of the eight 16- and 8-bit arms (`test r9d, r9d`), and a write cycle longer than the cycle length leaves through the early exit at `0022C00D`, so filling writes are not implemented. *(qualified 2026-09-27, FABLE, Claude Opus 5.5, adopting OPUS's owner read 532305504: that exit returns 0 (`0022C8C2` `xor eax, eax`), and the interpreter adds the return to its cursor, so the payload's first dword is then parsed as the next VIF command - not a harmless skip.)* **Which formats are authored, bounded to code-built packets: only `V4_32`.** All 87 UNPACK commands in [vif1-packet-templates.tsv](vif1-packet-templates.tsv) are `V4-32`, and an image-wide sweep of stored dword immediates with a top byte in `0x60`..`0x7F` and an UNPACK-shaped low word finds 98 with `0x6C` (24 with the TOPS flag) and nothing else that survives reading: of the 19 `0x60` / `0x70` hits, twelve (`0x602E4000`, `0x602CC000`) are the upper half of a GIF tag lying inside a `V4_32` payload (read at `004DA4A1`: the UNPACK header is the `0x6C140000` four bytes before the payload starts) and seven are `0x..808080` colour constants; the three others are `0x7D000000` (an unaligned stack store), `0x7F000000` (a stack store in library code) and `0x6464007F` (a store to a global), none at a command slot of a packet.The UI quad emitter is one of the 98 and its packet is decoded whole on [the cutscene-slot page](../../99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md) (UQ-347). **What keeps the row PARTIAL:** packets that reach the decoder from loaded data rather than from code were not censused, so the other twelve arms are unexercised by code-built packets, not shown dead.
      *Narrowed 2026-09-26 (FABLE, Claude Opus 5.5): two of the thirteen arms misaddress their source.* Each arm's inner loop was measured for its source stride and compared with the PS2 packed element size, and eleven match. **`V2-32` advances 4 bytes per element against a packed 8.** `0022C2D0` / `0022C2DA` read `[rax+r8*4]` and `[rax+r8*4+4]` with one `inc r8` per element (`0022C2DF`), ~~so consecutive elements overlap by a dword.~~ **`V4_5` advances 8 against a packed 2.** It reads word `[rax+r8*8]` (`0022C840`) with `inc r8` (`0022C879`), ~~so it takes one halfword in four.~~ *(Qualified 2026-09-27 (FABLE, Claude Opus 5.5), on `ASTRA-RETURN-FABLE-VIF-CYCLE-AND-CURSOR`; ASTRA's executed original cycles, `_experiments/evidence/vif-unpack-cycle-boundary/`. The inner strides stand. What they do to a whole stream depends on the write cycle:*
      - *They act only inside one write cycle that holds more than one element. Each new cycle moves the source base on by `8 × WL` (`V2-32`) or `2 × WL` (`V4_5`) bytes and restarts the inner index. With WL = CL = 1 the packed elements are read in order. With NUM 3, `V2-32` starts its elements at bytes 0, 4, 16 for WL = CL = 2 and 0, 4, 8 for WL = CL = 3; `V4_5` starts at 0, 8, 4 and 0, 8, 16.*
      - *The returned count is not the span read. `V4_5` with NUM 3 returns 8 but reads through byte 9 (WL = CL = 2) or byte 17 (WL = CL = 3). In a whole packet it read the low halfword of the next STCYCL header as colour, and the decoder then parsed that header as a command anyway.*
      - *`V2-32` writes two of each cell's four dwords.*
      - *So a reimplementation must keep the cursor advance, the addresses read, the per-cycle restart and the partly written lanes as four separate facts.)*
      Neither arm is used by any code-built packet (all are `V4_32`, above), so on those paths the defect is latent. A reimplementation matching the decoder needs it only if data-borne packets use those formats, which is the census that keeps this row PARTIAL. Control: `_index/candidates/uq215-unpack-strides/unpack_strides.py` (5 checks; planted control `S-16`).
      ***ANSWER ESTABLISHED 2026-09-27, FABLE, Claude Opus 5.5, static (box left open: eight retained preimage copies of this page carry it, FABLE-REQ-FRONTIER-CHECKLISTS-SKIP-RETAINED-PREIMAGES): no loaded-data VIF command stream reaches the decoder, so no shipped content exercises the other twelve arms.** The interpreter `001DB550` is reached only as `GiVmax` slot 0, and chunks enter only through `001DB340`. Every payload the four VU1 registrars are given is an exe `.data` template (101), a code-built stack buffer (2) or type `0x67`'s record block, whose records copy the template `02AEC860` (`UNPACK 0x6C22001E`, V4_32) and whose per-frame data is a code-filled work buffer. Where resource bytes enter an effect packet, the builder writes the V4_32 header itself (`or ecx, 0x6C000064` at `0054C10E` / `0054D9EE`). The one VIF stream that does come from data, effect type `0x97`'s resource payload, is appended through the raw-packet appenders `003A2E30` / `003A31A0`, which the PC drain never submits (UQ-204). The `V2-32` / `V4_5` defects are therefore latent on every route. [Record and control](../../_index/candidates/uq215-no-data-borne-packets/README.md) (7 checks, FAILS 0).*
      *ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5): no loaded-data VIF command stream reaches the UNPACK decoder, so no shipped content
      exercises the twelve non-V4_32 arms, and the V2-32 / V4_5 source defects above are latent on every route. The
      one data-borne VIF stream (effect type `0x97`'s payload) goes through raw-packet appenders the PC drain never
      submits (UQ-204). [Record](../../_index/candidates/uq215-no-data-borne-packets/README.md), `uq215_routes.py`
      FAILS 0.*
- [x] **UQ-384.** ~~Who consumes `001DB660`'s GS buffers~~ `GiVmax` slot 1 `001DB3D0` replays them through `00210320` (§2.1a); the
      register coverage and the vertex path are in §2.1b. **Still open:** ~~list-versus-strip separation~~ (read 2026-09-27, §2.1b item 3), the device
      class behind `[01FC35F8]`, and the state handlers' stores. *(Marker normalised 2026-09-30 (FABLE, [record](../../_index/candidates/qid-marker-truth-fable-0930/README.md)): the box named no row; its residue is registered as UQ-384 and the box is open.)*
      *Answer established 2026-09-30 (SWE2-STRUCT for OPUS), static; ~~box left open until the register row moves~~ (the row moved and the box is ticked, 2026-10-01): **`[01FC35F8]` holds `02CC1CD0` = `02CC0410 + 0x18C0`, the embedded `PrimitiveRendererD3D11` (vtable `00D86960`, RTTI, 45 slots).** It is written only at `0021037B`, from `GiVmax` slot 1's `rdx`, which the Gi execute callback `001F4A10` supplies as the render context's `+0x18C0`. The object is static storage built in place by `00615840` and `006C8750`; nothing is allocated. The replay calls 17 of its slots from 24 sites. **The state handlers store** the raw GS register qwords (TEX0, CLAMP, TEXA, ALPHA, TEST, ZBUF, contexts 1 and 2) into per-register globals, split PRIM into flag bytes, and keep RGBAQ as bytes, ST and UV as floats and FOG as a byte. TEXFLUSH calls device slot 37. PACKED can reach only descriptors 0-0xF, so its arms for `0x3B`-`0x4F` are unreachable; A+D drops RGBAQ, ST, UV, XYZ and FOG. FGE, FIX, FOG, FOGCOL, `(int)Q` and ZBUF_1/2 are stored but never read. [Record](../../_index/candidates/swe2struct-uq384-385-0930/README.md), `uq384_385.py` FAILS 0.* *(UQ-384 answered 2026-09-30 by SWE2-STRUCT for OPUS `875433f7c`, [record](../../_index/candidates/swe2struct-uq384-385-0930/README.md); register restated 2026-10-01 by OPUS for SWE2-DATA.)*
- [x] ~~Which object type owns `001DB550` (its vtable).~~ `GiVmax`, vtable `009007E8` slot 0 (§2.1).
- [x] ~~The 45 region functions that touch VU state but neither template path installs~~ — **layer-internal
      (§2.6):** the 54 touchers have no caller outside the VU1 family; 33 are called only by microprograms, 19 by
      nobody in the E8/E9 index (VU `JAL`/`JR` sub-programs remain the candidate path), and the two with
      non-microprogram callers are called only by sibling touchers. Still open: which of the 19 caller-less rows
      are JAL/JR sub-programs vs. data-referenced entries.
- [x] **UQ-385.** Which of the 19 caller-less rows are `JAL` / `JR` sub-programs and which are data-referenced entries (split out of the box above, whose live text said "Still open"; registered 2026-09-30, FABLE, [record](../../_index/candidates/qid-marker-truth-fable-0930/README.md)).
      *Answer established 2026-09-30 (SWE2-STRUCT for OPUS), static; ~~box left open until the register row moves~~ (the row moved and the box is ticked, 2026-10-01): **none of the 19 is a `JAL` / `JR` sub-program target and none is data-referenced.** All 19 are VU1 microprogram entries from UQ-213's 57: 9 were already rowed registrar-path and 10 were added by UQ-213. Each address is formed only by a rip `lea` as a registrar's program argument (48 sites), and MSCAL starts it through the program table `02068E30`. No VU microcode is embedded, because MPG carries one x64 pointer, so there is no `JAL` / `JR` to decode. The only data matches are `.pdata`, unwind and handler metadata. [Record](../../_index/candidates/swe2struct-uq384-385-0930/README.md), `uq384_385.py` FAILS 0.* *(UQ-385 answered 2026-09-30 by SWE2-STRUCT for OPUS `875433f7c`, [record](../../_index/candidates/swe2struct-uq384-385-0930/README.md); register restated 2026-10-01 by OPUS for SWE2-DATA.)*

## 8. Evidence

**How it was found.** Ranking function-pointer tables and address regions by EC-7 frontier mass led to the
`0x480000` region's largest bodies. Those bodies are passed as function pointers to `003A34D0`, not called.
Reading one (`004804A0`) showed 16-byte cells indexed by 16-bit words and two flag helpers with the VU sticky-flag
bit positions. Following where `02064E30` is handed out led to `0022C940` / `0022C970`, whose cases are the VIF1 command set
(§2.1).

**Controls.**
- The VIF-code census (§2.4) uses a 300-function random control: 0 functions store STCYCL together with MSCAL.
- The program census runs two independent paths (the template emitter and the registrars); they agree on 17
  programs, and neither was needed to find the other.

**Instruments** (in `Database/Tools/work/FABLE/pub140-scratch/tools/`):
- `vu1_census.py`: MPG emit sites, programs, region classes, flag users;
- `vif_tags.py`: VIF codes per group, with the control;
- `fptables.py`, `rtti_vtables.py`, `forms_of.py`: the survey that led here.

**Not claimed:**
- that every function in the region belongs to this layer (46 "other" functions are unclassified);
- that the PS2 microcode is recoverable (only its recompilation is in the image).

## 9. Related

- [The `0x480000` builder region](../../00-Engine-Core-Runtime/Startup-Data-Construction/generated-float-table-builders.md): its
  66 objects are §2.4's packets (BH-1).
- [The unresolved 158](../../99-Unresolved-Residual/the-unresolved-158.md): AC-7's bank is §2.2's VU memory and its leaf is
  §2.5.
- [GS texture-mip local-memory budget](texture-mip-local-memory-budget.md): the other PS2 GS fossil.

## Residual placements — 2026-09-14 (SWE2-FRONTIER, residual-placement package)

| function | size | role (call-signature read) |
|---|---:|---|
| `0020FF10` | 793 | two-call body: `0020F2A0` then `001EE650`; caller `0020ED30` (the `0020Exxx` VU-adjacent family) |

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — CLIENT and SERVICE.** Cited functions are called by the 978-byte core start-up root (2) and call a 93-byte core helper (2).

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**Audio — MECHANICAL (3 edges).** The render pass list `00187950` calls `00182E80`, and the getter pair `00182E80` / `00182EB0` tail-jump to the four-byte field readers `002256A0` (the dword at `+0x14`) and `00225680` (the dword at `+0x10`) when the framework singleton exists, falling back to `0x438` and `0x780` otherwise. All four are filed to Audio, but what they do is read two dwords of the framework singleton with 1080/1920 fallbacks, the pair the paragraph on the drain above describes; the edges are that display-size read, and no sound path is involved.

## Interior read — frontier hub `008631E0` (2026-09-17, SWE2-EC7) — evidence only

`008631E0` — 84 B, 36 frontier callers at census. Read against the shipping image (page is
PARTIAL — no disposition claimed): the MPG record emitter sibling of `008631D0`. It stamps
`word [rcx] = 1`, `byte [rcx+3] = 0x30`, bumps the queue counter at `02EB37B0`, stores
`arg3 | 0x4A000000` into the tag slot `[02EAF930 + idx*8]` and `arg2` into `[+8]`, then writes the
`0020E620`-encoded form of `arg2` into `[rcx+4]` — a {tagged-payload, encoded-pointer} enqueue
record, same base-image fixup discipline as the `0020E600`/`0020E620` family.
