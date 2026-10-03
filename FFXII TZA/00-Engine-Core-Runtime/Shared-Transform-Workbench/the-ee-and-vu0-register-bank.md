---
system: The "shared transform workbench" is the register bank of the PS2 assembly emulation — EE general-purpose registers, HI / LO, and the VU0 vector unit's registers
category: 00-Engine-Core-Runtime
status: DOCUMENTED — the translated-vs-C split (UQ-38) is OUT OF EVIDENCE BOUNDARY (2026-09-28, answerable only from the source tree or FF12X64.pdb; static bracket 47 / 31 / 95), the vf row mapping (UQ-36) and VU0-vs-Square ownership (UQ-39) are OUT OF EVIDENCE BOUNDARY (2026-09-27, answerable only from the PS2 executable); multi-thread reach (UQ-40) answered 2026-09-18: one user thread, the thread pools carry no jobs; UQ-37 answered 2026-09-15. The three OUT OF EVIDENCE BOUNDARY rows are limits stated in §7, not answers. Re-statused 2026-09-29 (FABLE) under _index/candidates/status-currency-ruling-fable
owner_layer: none — the register state of translated PS2 assembly, which every subsystem that kept hand-written PS2 assembly shares
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: every rip-relative operand into 022D8F10-022D949F and 01EF93F0-01EF93FF over all listed functions, split into
    read / write / address and mapped to registers (members/ee_register_census.py -> members/ee-register-census.tsv); the
    semantics of each named register were read at the instruction sites cited in section 2
last_reviewed: 2026-09-14
audit:
  passes: 1
  last_pass: 2026-09-14
  last_pass_state: swe2-audit-sem-falsification-pass-1 vs exe 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  falsification_passes: 1
  last_falsification: 2026-09-14
  crossref_clean: false
  reopened_count: 0
---

# The register bank of the PS2 assembly emulation

> **The 1.5 KB area this database calls the [shared transform workbench](the-shared-transform-workbench.md) is the
> register set of a PS2 CPU, kept in memory.** FFXII's PS2 code included hand-written MIPS assembly for its matrix and
> vector math (the VU0 vector coprocessor) and for its 16-bit SIMD work (the EE's MMI instructions). The PC port did not
> rewrite those routines. It translated them instruction by instruction, and the registers the instructions name became
> globals:
>
> - `022D8F10 + 16·k` is **GPR[k]**, the 32 general-purpose registers as 128-bit images. GPR[0] is `$zero`.
> - `022D9110` / `022D9120` are **HI / LO**.
> - `022D9130` is the VU **CLIP** flag word, `022D9198` is **Q** and `022D91A0` is **ACC**.
> - `022D91A0 + 16·n`, n = 1…31, are the **vector registers**.
> - `01EF93F0` is **vf00**, the constant (0, 0, 0, 1).
>
> The engine names the layer itself. The routine that sets vf00 at start-up prints
> ~~**`"PS2 Assembly emulation initilization completed! "`**~~ **`"PS2 Assembly emulation initilization completed! *** \n"`** *(corrected 2026-10-02, OPUS: the string at `00908D80` runs on to `*** ` and a newline before its NUL)* (`0036D990` → `00908D80`; the spelling is the game's).
>
> **267 functions (389,071 bytes) address the bank. 257 of them are ARCH frontier, and 188 are cited by no page.** The
> census is [`members/ee-register-census.tsv`](members/ee-register-census.tsv).

## 1. What the player sees

Everything that moves in 3-D passes through this code at some point. A spell's particles are placed, a character's
bones are multiplied through, a sound source's nearest point to the listener is found, and a 16-bit table is packed.
FFXII did that work on the PS2 in assembly for the vector unit, and the remaster still runs the same instructions. They
are now written as x64 moves into a fake register set, which is why the database found "249 functions writing one
buffer and never calling each other". Those functions all ran on the same CPU.

## 2. How the identification was made

The earlier pages measured this area correctly and named it by its shape. [The workbench page](the-shared-transform-workbench.md)
proposed "a calling convention implemented in memory", and §2.5 even compared it to "an engine whose ancestor passed
matrices through fixed vector-unit register banks". OPUS then found the start-up string beside the vf00 constant (BQ-20)
but filed the constant apart from the matrix area. This page shows that the constant and the area are one register set.
It gives one semantic test per register, each read at instruction level, and a census of which registers each function
uses.

The tests are chosen so that a parameter area, a matrix pool, or ordinary globals would fail them.

| register | prediction if it is that register | observed |
|---|---|---|
| GPR[0] `022D8F10` | read-only; used as the constant zero | **0 writers, 44 readers.** Loops end on `cmp [loop register], [022D8F10]` (`0039502A`, `003952AF`), which is `bne rX, $zero`. |
| GPR roles | temporaries used most, then return and argument registers; callee-saved registers barely | readers / writers: **t0 47 / 64, t1 39 / 46, t2 37 / 41, t3 21 / 27, t4 17 / 20, t5 11 / 13, t6 7 / 6, t7 4 / 6**; v0 19 / 29, v1 10 / 10, a0 9 / 9, a1 9 / 9; **a2, a3, s0–s2, s4–s7, sp, ra: none**; at, s3, t8, t9: one function each. That is the order of a MIPS leaf routine's register use. |
| HI / LO `022D9110` / `022D9120` | written by multiplies, the high and low products apart | `0026EE00` multiplies signed 16-bit pairs (`imul`) and stores the first product to **LO** and to t2's first dword, the second to **HI** and to t2's second dword, and another to LO's second dword (`0026F0E0`–`0026F0FA`). That is `PMULTH`'s exact result rule. The same body shifts by 7 (`psrlw`, `0026F2A2`) and clamps word by word (`0026F2C0`–`0026F2D6`), both MMI shapes. 10 writers, 1 reader. |
| CLIP `022D9130` | shift left by 6, then set six comparison bits against \|w\| | `0025A8E0`: `shl eax, 6` (`0025A8EE`), then `or 1` when x > \|w\|, `or 2` when −x > \|w\|, `or 4` for y… (`0025A906`–`0025A939`). That is `VCLIP`. |
| Q `022D9198` | written by division or square root, read to scale a vector | Its **55 writers** store a `divss` result at 51 store sites (`VDIV`; `0024AEB0` divides **vf00.w** by a w, then `0024AEDB` multiplies a vector row by it, which is `VDIV Q, vf00w, …` followed by `VMULq`). At 24 sites they store `sqrtf(|x|)` (`VSQRT`; `002F1D3D`–`002F1D59`, then `002F1D61` adds it to vf00.x, which is `VADDq`). |
| ACC `022D91A0` | written by an `…A` operation, then consumed by `MADD` / `MSUB` | `00363FD0` writes ACC.xyz = row − row (`VSUBA`, `0036413D`–`0036415D`), then computes s·row + ACC (`VMADD`, `0036417D`–`003641A8`). 83 writers, 46 readers. |
| vf00 `01EF93F0` | the constant (0, 0, 0, 1); writers only (re)establish it | Exactly **3 writers**, all storing (0, 0, 0, 1). The clear `0036D9E0` and the emulation start-up `0036D990` store it field by field. `0036DD80` copies the 16-byte constant `008C5FD0` = (0, 0, 0, 1.0). **129 readers.** |
| vector rows `022D91B0`–`022D939F` | 31 float rows, component-masked writes (`xyz` more than `w`) | 31 rows, float-dominated. Component writes: row + C (w) is touched least in most rows, as a destination mask `xyz` produces. The one proven 4×4 block, `022D91B0`–`022D91EF` ([the two primitives](the-two-transform-primitives.md)), is rows 1–4, which is how VU0 code holds a matrix: four vector registers. |

**Start-up.** `0036D990` is called from the boot routine `0022A0B0` ([what the engine fixes at boot](../what-the-engine-fixes-at-boot.md)) at `0022A125`. The next call, `0022CB90`, clears the VU1 memory `02064E30` (0x4000 bytes) of the separate VU1 layer ([the VIF1 / VU1 layer](../../17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md)).
`0036D990` stores vf00 and prints `"Sizeof 64 bit int = %d\n"` with 8 and then the completion line, through `0017D280`.

**The save and restore are register pushes.** [The save / restore contract](../CONTRACT-transform-workbench-save-restore.md)
(`0036D930` / `0036D8E0`) saves a count of 16-byte cells and restores them later. The first pointer at each of the nine direct call sites is
**v0** (`022D8F30`: `0026EE17`, `003AFDE0`, `003D8E6C`, `004300EC`, `00431D40`, `00462270`) or **t0** (`022D8F90`:
`002F1CE9`, `002F1DA0`, `0044C42E`). A routine that clobbers a register its caller still needs saves it first. The
depth count `022D8F08` sits just before GPR[0].

## 3. The map

```
PS2 assembly emulation register bank          (all BSS: no file image, zero at load)

  01EF93F0  f32[4]   vf00 = (0, 0, 0, 1)     written by 0036D990, 0036D9E0, 0036DD80 only
  022D8F08  u32      save depth              0036D930 / 0036D8E0
  022D8F10  128-bit  GPR[0]  $zero           never written
  022D8F10 + 16k     GPR[k]  k = 1..31       used: at v0 v1 a0 a1 t0..t7 s3 t8 t9 (§2 table)
  022D9110  128-bit  HI
  022D9120  128-bit  LO
  022D9130  u32      VU CLIP flag word       shl 6 | six comparison bits
  022D9198  f32      VU Q                    VDIV / VSQRT result
  022D91A0  f32[4]   VU ACC
  022D91A0 + 16n     f32[4]  vector register n = 1..31   (row 1 = 022D91B0 ... row 31 = 022D9390)
  022D9470  u32      flag word               bit 0x80 set by 0036DD90, bit 0x40 by 0036DDA0 (§6)
```

**Not assigned by this page:**
- `022D9140`–`022D916C`, a block of float slots with raw integer stores followed by `divss` (`003B5DBF`–`003B5DD7`).
  Their use resembles MIPS FPU registers, but the placement is not proven, and Q's semantics (§2) exclude the idea
  that `022D9198` belongs to that block.
- `022D9138`, documented as RNG state ([rng streams](../../21-RNG-And-Determinism/rng-streams.md)).
- `022D94A0`, a 64-bit loop register compared against `$zero` (42 functions, `00394E50`–`00545650`).
- The 32 × 24-byte record table at `022D94B0` (BQ-17 / BI-8), which BI-12 already separated.

## 4. What this re-explains

| earlier reading | now |
|---|---|
| "a memory calling convention for a family of shared matrix routines"; "no owner" (workbench §2.5–2.6; BQ-13) | **Right in effect, and now explained.** Nobody owns the registers of a CPU. Every subsystem that kept PS2 assembly uses them. |
| "how the row array divides into matrices past `022D91B0`" (BQ-16) | **It does not divide into matrices.** It is 31 vector registers and ACC. A "matrix" is whatever four registers a routine loads, so the grouping belongs to each routine, not to the area. The live measurement recorded under BQ-16 (a 16-byte unit at `022D91F0`, a 32-byte unit at `022D9210`) is two routines' register use. |
| "whether the matrix at `022D91B0` is world, view or projection" (BI-9) | **Rows 1–4 hold whatever the last routine to use them loaded.** The matrix has no fixed identity, and the title-screen observation that the rows were degenerate and not maintained fits that. The convention BI-9 proved (row-major, translation in row 3, w forced to 1) belongs to the routine `00398F90`, which uses ACC and vf00 (census). |
| "whether any of the 62 objects is persistent" (BQ-19) | **Registers are volatile by definition.** A value that survives between routines is a register nobody overwrote, not an object. |
| "why chain A and chain B share state" (BI-6) | **They share a CPU, not an object.** `003CD840` and `003D2B60` use GPR t0–t5 with 980 and 339 MMI-shaped SIMD mnemonics, which is translated MMI assembly. `00438860` uses ACC and four vector rows, which is translated VU0 assembly inside a C routine. The "198 fixups into `022D9000`" were accesses to the page that holds the register bank. |
| the audio closest-point helpers use `022D92A0`–`022D9318` "as vector scratch" (BQ-18) | **They are VU0 routines.** `00363FD0` is `VSUBA` / `VMADD` over vector rows; `0036DD90` / `0036DDA0` set flag bits on the compare paths of `00361DE0`. |
| effect element type 5's walker helpers (`00394B70`–`00396F20`, `0039E6B0`–`0039F9F0`, `00432300`, `00432CC0`; [effect type dispatch](../../17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md) §2.5) | `00432300` / `00432CC0` are translated MMI routines over t0–t5. `00394E50` / `00395050` are VU0 loops over ACC and the vector rows that end on `$zero`. |

**BI-1 is not changed in substance.** The `003CD840` machine is still the render-model subresource-variant binding
system. This page says what its body is made of (translated MMI assembly), not what it binds.

## 5. The census

`members/ee_register_census.py` classifies every rip-relative operand into the ranges of §3 as a read, a write (the
first operand of a storing or arithmetic instruction) or an address (`lea`). For each function it also counts
MMI-shaped mnemonics (`psrldq`, `pextrw`, `pinsrw`, `pmullw`, the saturating adds, the 16-bit shifts and so on).
**Limit:** an access through a base register loaded by `lea` (the word loop at `0026F2C0` indexes `[rax + rbp]` after
`lea rbp, [022D8F30]`) is counted as an address, not attributed to a register. A function that only receives a pointer
into the bank, like the save / restore pair `0036D930` / `0036D8E0`, is not a member. Every member also has at least
one direct read or write, so no member rests on an address alone.

| population | functions |
|---|---:|
| address the bank | **267** (389,071 B) |
| … use GPRs | 99 (32 with MMI-shaped mnemonics) |
| … use vector rows, ACC, Q or CLIP | 217 |
| … both | 72 |
| … only the vf00 constant | 22 |
| … only HI / LO | 1 (`00506A40`) |
| ARCH frontier | **257** |
| cited by a page | 79 (69 of them frontier) |
| **frontier and uncited** | **188** (233,191 B) |

The largest members are `003CD840` (21,276 B, GPR + MMI), `003D2B60` (20,710 B, GPR + MMI), `00438860` (20,603 B, ACC
+ vector rows), `00533B20` (9,526 B, t2 + Q + ACC + 27 rows), `0040B780` (8,458 B, Q + ACC + 28 rows), `005131C0`,
`00411650`, `00548A00`, `00413C80`, `0050AC20` (GPR t0–t6) and `002A0440` (a0 a1 v0 v1).

**What membership means.** A member contains translated PS2 assembly, either as its whole body or as fragments inside a
C routine (`004355D0` / `00437130` are C with fragments in their helpers). Membership says **how** the member computes. It
does not say **what** it computes. It is a reading key, not an EC-7 class explanation, so this page declares no
`function_families` row.

### 5.1 The 188 uncited members, read back into operations (SWE2-FRONTIER, EE-REGISTER-MEMBERS)

`members/ee-register-members.tsv` gives every `frontier=A / cited=no` row a per-function line: the
ordered bank-access sequence compressed to register granularity (`R`/`W`/`A` per register, run
counts), a split column, and a caller-derived purpose. The instrument is
`Database/Tools/work/SWE2-FRONTIER/ee_members_final.py`; its register map is §3 verbatim.

**Split of the 188** (whole-translated = bank traffic dense enough that the body *is* the PS2
routine; C-fragment = a C routine with at most four bank accesses):

| split | members |
|---|---:|
| translated VU0 whole routines | **111** |
| C routines with translated fragments | 41 |
| C routines, ≤4 bank ops (fragments) | 20 |
| MMI/SIMD-heavy mixed | 16 |

The 20-row `C-fragment` class is defined by **at most four bank accesses**, not by vf00 alone —
eight of them touch non-vf00 registers (`002F67C0` `Wvf01`; `00376470` `Rvf00×2 Wvf01`;
`003A2B90` `$v0`+`vf21`+`vf20`; `003B4310`/`003B5D40`/`0053DB50` `W$t0`; `004010A0`
`vf20`+`$t0`; `0044B960` `vf21`). Rows touching only `Rvf00` are C routines borrowing the
constant.

**Families the caller map already resolves.** BFS through `edges.tsv` / `edges_live.tsv`:
`CharacterRender_UpdateCombatLookAndAuxControllers` reaches **16** of the 188;
`CharacterRender_RebindCombatLookAndSkeletonResources` reaches **14**; their union covers 30.
The `00442170` subtype dispatcher's eight step bodies (`005315B0`/`0052F780`/`00531DB0`/
`00530770`/`0052FCA0`/`00530230`/`005318A0`/`00530E40`) are all members — each is a translated
VU0 routine, which is consistent with those arms being element-type update programs. Seven
members are the [per-model oscillator](../../17-Presentation-Rendering/Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md)
family (`0040B780`, `0040DBB0`, `0040D890`, `0040F390`, `0040FF30`'s siblings `00413340`,
`00413C80`, `00411650`) — the subsystem's heavy stages are exactly the translated-assembly
population. Three members have no direct caller in `edges.tsv` (`0029BC80`, `00398390`,
`0042D050`) — installer or indirect reach only; **not** dead-code claims.

**Controls re-derived.** The three known members reproduce under the sequence reader:
`00398F90` reads vf01–vf04 with ACC accumulation and a vf00 read — the point-through-rows-1-4
with w=1 documented in §6's worked examples; `0025A8E0` is the CLIP strobe `RCLIP / WCLIP×8 /
RCLIP` (VCLIP); `00363FD0` loads vf16–vf19, writes Q once (`Rvf00 → WQ`, the division step of a
normalize) and accumulates through ACC — the segment-distance shape. The reader's labels for all
three match the page's prior claims.

**Limits.** The `ops_summary` column is register traffic in instruction order, not a VU0
disassembly — masks and the actual arithmetic are still in the bodies. A purpose of the form
"via caller X (frontier)" is a provenance note, not an identity. Rows whose only bank access is
`Rvf00` are C routines borrowing the constant, not translated code.

## 6. How to read a member

Once the map is known, each x64 instruction group maps back to the PS2 operation it was translated from:

| x64 over the bank | PS2 operation |
|---|---|
| `movss [vfN.c], xmm` per component, components limited to a mask | a VU0 op with destination mask |
| `divss` / `sqrtf(|x|)` stored to `022D9198` | `VDIV` / `VSQRT` into Q |
| `shufps x, x, 0; mulps [row]` after a Q store | `VMULq` |
| store to `022D91A0` then `mulss …; addss [022D91A0]` | `V…A` then `VMADD` |
| `shl [022D9130], 6; or …` | `VCLIP` |
| `imul` of 16-bit pairs to `022D9110` / `022D9120` | `PMULTH` / `PMULTW` |
| `cmp [loop register], [022D8F10]; jne` | `bne …, $zero` |
| `call 0036D930` with v0 / t0 … `call 0036D8E0` | save and restore of a clobbered register |

The operation sequence can then be matched against the PS2 VU0 library's routines (matrix multiply, apply, rotate-
translate-perspective, clip-screen, normalize, outer product) or read as Square's own. **The 0x40 / 0x80 bits of
`022D9470` have the shape of VU status sticky flags. Which flags they are is not mapped.**

## 7. What is not known

- [x] **UQ-36.** Whether vector row n is PS2 register vf*n*. The linear map is the simplest translation and fits the one fixed
      point (vf00 at `01EF93F0`, outside the rows), but no instruction states a register number. The row index is a
      coordinate, not a proven name.
      **Narrowed 2026-09-18 (FABLE): a per-member row census gives the map a consistency test it passes, and a fingerprint test it cannot pass because the fingerprints are absent.* Every rip-relative operand of all 267 members was binned into the rows (`022D91A0 + 16n`), Q, CLIP and the `vf00` constant, read and write separately. Under the linear map the PS2 SDK's `libvu0` allocations would show as `sceVu0MulMatrix` = reads rows 4–7 and 8–11, writes 12–15 and ACC; `sceVu0ApplyMatrix` = reads 4–7 and 8, writes 9; `sceVu0Normalize` = rows 1 and 2 with `vf00.w` into Q. **No member has any of them** (the two members whose read sets merely contain 4–11, `0040B780` and `00411650`, read and write most of the bank). The test is also run as a shape, permutation-invariant: no member reads two disjoint blocks of four rows and writes exactly four others plus ACC, so the SDK's matrix multiply is not among the members under *any* row naming. What the members do show is their own convention: rows 20 and 21 are touched by 124 and 128 members (row 20 read-write, row 21 read-only in ~60 of them), rows 1–3 by 68–76, ACC by 142 and `vf00` by 136, rows 4–19 by 12–55 each; and repeated templates (`{0 w, 1 r, 2 rw, 4 r, 5 w, 20 rw, 21 r}` with Q written, nine members; `{0, 2–4 r, 6–8 rw}`, eight). So the row index is consistent with `vf`*n* (nothing contradicts it and `vf00` sits outside the rows) but is not proven by it, and the SDK's fixed allocations cannot prove it because the SDK routines are not here.*
      *OUT OF EVIDENCE BOUNDARY 2026-09-27 (FABLE, Claude Opus 5.5; signed by OPUS, non-author, d893251b4): answerable only
      from the PS2 executable `SLPM_667.50`, which the shipped `system.cnf` names and nothing ships. The residue stays
      unanswered in fact. [Package](../../_index/candidates/oeb-package-ps2-2026-09-27/README.md), [review](../../_index/candidates/oeb-ps2-review-opus/README.md).*
- [x] **UQ-37 ANSWERED 2026-09-15 (OPUS) — they are two different things, and neither is
      the state this row assumed.**
      - **`022D9140`–`022D916C` is not a structure. It is scalar staging for moving values
        between general-purpose and XMM registers through memory.** The tell is that the *same*
        slot is written by an integer `mov` and then read by a float instruction: **35 such pairs
        across the 11 functions that touch the block**. `0053DC03` writes `mov dword [022D9168],
        0x3f800000` — `1.0f` by its **integer** encoding — and `0053DC2A` then does
        `subss xmm4, [022D9168]`. `003B5DBF`/`003B5DC9` do the same on `022D914C`, and
        `003B5DD1`/`003B5DD7` write `edx` to `022D9148` and immediately `divss` by it.
      - **That explains the mixed access widths the row noticed.** Over the block: 35 `movss`,
        32 `mov`, 7 `subss`, 6 `mulss`, 4 `movsxd`, 3 `comiss`, and one each of `movd`, `minss`,
        `divss`, `addss`. A structure would not be written as an integer and read as a float at the
        same address; a spill slot is.
      - **`022D9140` itself is never referenced at all** (control `022D8EB4`, 26 references, so
        absence is meaningful). **Corrected 2026-09-15, same day:** the range
        `022D9140`–`022D916C` is **TWELVE dwords**, eleven are referenced, and the **only**
        unreferenced one is **`022D9140`** itself. My first wording said *“11 of the 13 … the
        two unused ones”*; the thirteenth address was `022D9170`, which is outside the range
        this row asks about, and counting it in made one unused slot look like two.
      - **`022D9470` is a write-only sticky flag word. Nothing in the image reads it.** It has
        **exactly two references, and both are writes**: `0036DD90` is `or dword [022D9470], 0x80;
        ret` (11 B) and `0036DDA0` is `or dword [022D9470], 0x40; ret` (8 B). No load, no test, no
        `lea` — so no pointer to it can be formed and reached another way.
      - **Which VU flags they are cannot be recovered here, and that is a property of the code, not
        a gap in the reading.** Bits accumulate and are never consulted, so no behaviour depends on
        them and no behaviour can distinguish one flag assignment from another. Naming them would
        need a source outside the binary.
      - *Re-checkable: one range census with a stated control, plus the same-slot int-store /
        float-read test. If any instruction reads `022D9470`, the second half is wrong and should be
        reopened against OPUS.* **UQ-37.**
- [x] **UQ-38.** How many members are whole translated routines and how many are C routines with translated fragments. *(OUT OF EVIDENCE BOUNDARY 2026-09-28, applied by FABLE (Claude Opus 5.5) on OPUS's non-author signature ([record](../../_index/candidates/uq38-oeb-signature-opus/README.md)): the authoring class is carried only by the unshipped source tree and `FF12X64.pdb`. The static bracket stands, corrected: 47 whole-shaped (5 of which FRONTIER's density instrument calls C+fragments), 31 C by both instruments, 95 undecided. Closed for the gate, unanswered in fact.)* That split
      decides whether a member's PS2 counterpart is one library routine or inline code.
      ***NARROWED 2026-09-17 (FABLE): the split is not mechanically derivable from either signal tried, and here is why.** Two instruments, two different signals, all 267 members. (1) SWE2-FRONTIER's `members/ee-register-members.tsv` classifies the 188 uncited members by bank-access DENSITY (`translated` when at least one instruction in fifty touches the bank and at least 15 do): translated 111 / C+fragments 41 / C-fragment 20 / MMI-mixed 16. (2) A second instrument (`members/ee_member_calls.py` → `ee-member-calls.tsv`) uses what ELSE the body does — calls to functions outside the member set (the bank save/restore pair excepted) and stack-slot traffic: whole 47 / mostly 38 / C+fragments 182. **They disagree on 95 of the 188**, all FRONTIER-`translated` members that call outside the set. But what those 95 call is a short common list — `__security_check_cookie` (46), `00430B90` (36), `0039ADE0` (35), `00397ED0` (34), `00398480` (34), `005002E0` (31), `003A8950` (30), `sqrtf` (28), `ImageAddress_ResolveRuntimePointer` (28), the composer `00397910` (27) — library-shaped routines that a PS2 routine would reach by `jal`, so a call is not evidence of C either. And the density distribution over the 267 is unimodal (median 0.19, no gap between 0.10 and 0.40), so any density threshold is a choice, not a measurement. **What the question needs is a per-member criterion neither instrument has:** whether x64 registers carry values ACROSS bank stores (C keeps locals in registers; a translation reloads every operand from the bank). That is a liveness read per body, not a census. Until it is done the honest figure is a bracket: **at least 47 members call nothing outside the set and spill almost nothing** (the largest is `003CD840`, 21,276 B), which is the shape of a whole translation; the 95 are undecided; ~~the 41 both instruments call C+fragments are settled that way~~ *(corrected 2026-09-28, FABLE, Claude Opus 5.5, on OPUS's recount in the UQ-38 signature: both instruments agree on C+fragments for **31** members; FRONTIER's 41 include 5 that ee_member_calls calls whole and 5 it calls mostly)*. Static; both TSVs are re-runnable.*
      ***Narrowed 2026-09-27 (FABLE, Claude Opus 5.5): the criterion proposed above is measured and retired - this translator carries values across bank stores.** Per member, the fraction of xmm reads whose value predates the latest bank store in the block is higher for the 47 agreed whole translations (median 0.535) than for the 31 agreed C members (0.333), the reverse of the criterion's premise, and the sets overlap. `003CD840` shows why: `psrldq xmm0, 1` / bank store at `003CD877` / `movd eax, xmm0` - a 128-bit value lives in a host register across the store. The split therefore needs provenance: the PS2 executable (`system.cnf` names `SLPM_667.50`; the ELF is not shipped) or the translator's rules. The bracket stands (47 whole-shaped, 41 C, 95 undecided). [Record](../../_index/candidates/uq38-carry-criterion/README.md) (example control FAILS 0).*
- [x] **UQ-39.** Which members are PS2 VU0 library routines and which are Square's own assembly.
      **Narrowed 2026-09-18 (FABLE): the SDK's `libvu0` routines are not among the members.* The same row census (UQ-36) shows none of `sceVu0MulMatrix`, `sceVu0ApplyMatrix` or `sceVu0Normalize` — neither under the linear map nor as a permutation-invariant shape — and no member's allocation matches the library's habit of `vf4`–`vf15` temporaries; the members cluster on rows 20 / 21 and 1–3 and repeat their own templates. Whatever library the routines came from, it is not Sony's `libvu0` under any register renaming; the Square-versus-library split therefore has one side removed, and the remaining question is whether the templates are Square's or a middleware's, which a register census cannot say.*
      *OUT OF EVIDENCE BOUNDARY 2026-09-27 (FABLE, Claude Opus 5.5; signed by OPUS, non-author, d893251b4): answerable only
      from the PS2 executable `SLPM_667.50`, which the shipped `system.cnf` names and nothing ships. The residue stays
      unanswered in fact. [Package](../../_index/candidates/oeb-package-ps2-2026-09-27/README.md), [review](../../_index/candidates/oeb-ps2-review-opus/README.md).*
- [x] **UQ-40.** Whether any translated routine is reached from more than one thread. The bank has no lock, so two concurrent users
      would corrupt each other. Nothing here shows concurrency.
      ***NARROWED 2026-09-17 (FABLE): no worker thread reaches any member by a direct call; what remains is the thread pools' job pointers.** Roots walked over `edges.tsv` (direct calls only): the two loop entries `MainLoop_UpdateAndRenderFrame` `0022B8C0` and `MainLoop_Draw` `0022B0B0`; the eight IAT-created start routines of `UQ-152` (`00171370`, `005CCAB0`, `005CCBA0`, `007A5550`, `007A5E50`, `007DD950`, `007DEC40`, `00863500`); and, because `00863500` is a 28-byte trampoline that calls **vtable slot 1** of the object it is given (`call [rax+8]` at `0086350C`), the slot-1 bodies of every thread class the RTTI names — `crossThreadImpl` `00863410`, `Phyre::PThreadPool` `006AA230`, `PThreadPoolWorkStealing` `006BAA40`, `PThreadPoolImmediate` `006CE570` (`Sys::Thread`'s slot 1 is `_purecall`). **Result: the update loop reaches 183 of the 267 members and the draw loop 40; the 35 they share are one thread, because both loops hang from the same caller-less root `0017CCD0`. None of the eleven non-main bodies reaches a member at all — their cones are 1 to 57 functions of video decode, audio and pool bookkeeping.** So by direct calls the bank has exactly one user thread, which is what its lack of a lock would require. **The bound:** `PThreadPoolWorkStealing` executes jobs it is handed as function pointers, and those pointers are not walked; a job that reached a member would not appear here. Closing the row means censusing the pool's job submissions (the class's methods are reached through its vtable, so `edges.tsv` cannot count them). 84 members are reached by neither loop directly — through function pointers or vtables — and are unattributed, not attributed to another thread.*
      ***ANSWERED 2026-09-18 (FABLE) — the pools carry no jobs, so the bank has exactly one user thread.** The bound the 2026-09-17 narrowing left was the thread pools' job pointers; they are censused now. Every pool object in the image is built inside `Phyre::PThreadPool::getDefault` `006AA280`: a `PThreadPoolImmediate` (`006CE5B0`) when the thread-count dword `01F2EB30` is 1 or less, else the `PThreadPoolWorkStealing` in static storage `02E4E610` (`006BA880`, vtable `00D81200`), with the count `01F2EB30` (shipped 1) raised to the processor count by `007979B0` — the popcount of the affinity mask, or `GetSystemInfo` (`008C2220`) when that is zero — through the setter thunk `005A0AE0` → `006AA370`, its only caller (`00797A09`, from `007980A0` ← `007A3770` ← the entry). So on a multi-core machine the work-stealing pool exists and its threads run `006BAA40`. But nothing hands it work: the constructors are called only from the getter (whole-image call sweep), the pool object is referenced only by the getter and the static destructor `008B41F0` (→ `006BA940`), and the getter's two callers are the boot initialiser `005A08E0`, which calls slot 2 *start* (`006BAB40`, `005A0A99`), and the shutdown `005A0840`, which calls slot 3 *terminate* (`006BAED0`, `005A0882`). The submit slot 5 — `006BAAD0`, which appends a job object to the queue at pool `+0x28` / `+0x80` and kicks slot 6 when a batch fills; or the immediate pool's `006CE650`, which tail-jumps the job's slot 1 on the caller's thread — is referenced by nothing but the two vtables, and the execute loop `006BB110` (`call [rax+8]` on each queued job, `006BB2E1`) has no caller outside them. No pool pointer is stored anywhere, no job vtable is constructed anywhere, so no job body exists for a worker to run. With the direct-call result of 2026-09-17 (none of the eleven non-main thread bodies reaches a member) that leaves the main loop's thread as the bank's only user, which is what the missing lock requires. Static: the bodies, `edges.tsv`, and image-wide sweeps for calls, rip-relative references and pointers to the pool, its constructors, its vtable slots and its thread-count accessors.*

## 8. Evidence

| claim | evidence | tier |
|---|---|---|
| the layer names itself | `0036D990` → `0017D280` with `00908D80` = ~~`"PS2 Assembly emulation initilization completed! "`~~ `"PS2 Assembly emulation initilization completed! *** \n"` *(corrected 2026-10-02, OPUS: read from the image)*; called from `0022A125` | 1 |
| vf00 is the constant (0, 0, 0, 1) with 3 writers | `0036D990`, `0036D9E0` (`0036D9E0`–`0036D9FB`), `0036DD80` (`008C5FD0` = 0, 0, 0, 1.0); census `vf00` row | 1 |
| GPR[0] never written | census: 44 readers, 0 writers; `0039502A` / `003952AF` loop exits | 1 |
| GPR role order | census register table (§2) | 1 |
| HI / LO by `PMULTH` | `0026F0D4`–`0026F0FA`; `psrlw` `0026F2A2`; word clamp loop `0026F2C0`–`0026F2D6` | 1 |
| CLIP | `0025A8E5`–`0025A939` | 1 |
| Q | 55 writers; at the store sites the value comes from `divss` 51 times and from `sqrtf` 24 times; `0024AEB0`–`0024AEDE`; `002F1D48`–`002F1D69` | 1 |
| ACC | `0036413D`–`003641A8` | 1 |
| save / restore passes v0 / t0 | the first pointer at the nine call sites of §2 | 1 |
| census figures | [`members/ee_register_census.py`](members/ee_register_census.py) → [`members/ee-register-census.tsv`](members/ee-register-census.tsv) | 1 |

## 9. Related

- [The shared transform workbench](the-shared-transform-workbench.md), the measurements this page reinterprets.
- [The two transform primitives](the-two-transform-primitives.md): `00397910` / `00398F90`, executed; members of this
  census.
- [The workbench save and restore](the-workbench-has-a-save-and-restore-and-nine-functions-use-it.md) and
  [its contract](../CONTRACT-transform-workbench-save-restore.md).
- [The VIF1 / VU1 layer](../../17-Presentation-Rendering/Legacy-PS2-GS/the-vif1-vu1-layer.md): the other PS2 unit the port
  still runs, with its own emulated memory and recompiled microprograms.
- [The largest unclassified functions](../../99-Unresolved-Residual/Largest-Unclassified-Code/the-largest-unclassified-functions.md),
  chains A and B.

## 10. Falsification pass 2026-09-14 — SWE2-AUDIT-SEM

**Program state:** shipping EXE `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`,
canonical GZF addresses. **Attack chosen:** independent byte-exact re-read of every load-bearing
instruction site cited in §2/§8 — the self-naming banner, the vf00 writers and constant, the
GPR[0] `$zero` loop exits, the PMULTH/HI/LO and CLIP ranges, the VDIV/VSQRT Q-stores, the ACC
accumulation, and all sampled save/restore first-pointer sites.

### SURVIVED — every attacked claim

- The banner string `00908D80` is literal; `0036D990` reaches `0017D280` twice and is called from
  `0022A125` inside `0022A0B0`.
- vf00: `1.0f` (`01CEBBA8`) → `01EF93FC` with `01EF93F0`/`01EF93F8` zeroed; `0036DD80` copies
  `008C5FD0` into `01EF93F0`. Constant `(0,0,0,1.0)` exact.
- GPR[0]: at `0039502A`/`003952AF` the compared operand is `rdx` reloaded from `022D8F10` one
  instruction earlier (`00395023`, `003952A8`) — `cmp [022D94A0], rdx` is `bne loopreg, $zero`
  as claimed. The ref census shows `022D8F10` read-only.
- HI/LO, CLIP, Q (VDIV `0024AEB0` + VMULq `0024AEDB`; VSQRT `002F1D59` + VADDq), ACC
  (`0036413D`–`003641A8`), and all six sampled save/restore first-pointer sites: byte-exact.

### Result

Zero defects found. The vf-n linear map stays a self-flagged §7 hypothesis — the page does not
overclaim it. Full attack record: `Database/Tools/work/SWE2-AUDIT-SEM/REVIEW-two-unattacked-tier1.md`.

*(Pass 22 adjacency, 2026-09-14: beyond the ScriptVM logger population — `0022A0B0`, the startup
hub cited on this page, calls **actor** `002368D0` and **input** `0035B270`; `0025A8E0` and
`0036DD80` are called by **actor** `0025C830`; and `002F67C0` calls **movement** `002330D0` (5
edges). The register-bank helpers are reached from actor-init and locomotion code as well as the
script verbs; shared state, shared callers.)*

*(Pass 22 live-graph completion, 2026-09-15: `0025C830` also calls `Party` `00358BB0` (1
edge) — the actor-side caller reaches party state through the same shared accessor family.)*

## Crossings into other layers — FINAL-AUDIT pass 22 (OPUS, 2026-09-18)

**Eleven edges, two layers, and ten of them arrive through one citation used as a chain link.**

**The carrier is `007980A0`, and it is the program's main body** — 2,153 bytes and 56 direct calls,
not a static initialiser. §264 cites it in exactly one role: *"`007980A0` ← `007A3770` ← the
entry"*, establishing that the thread-pool constructors are reached from the program entry at all.
**That is the whole of the claim.** Ten of its callees land in the platform layers — the online and
achievement entry points, a platform service getter, an input-side helper — and **none of them is
inside the region this page is talking about**, which is the getter chain and nothing else.

> A body of that size reaches most of the engine. Citing it to establish reachability imports its
> entire neighbourhood, which is the class this protocol records on
> [`static-initialisers-and-teardowns.md`](../../24-Compiler-And-CRT-Runtime/Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md)
> and `five-small-bin-tables.md`. **The citation is correct and is kept**; what was missing was
> saying which layers it drags in and why none of them is a claim by this page.

**The eleventh is the timer.** `005A08E0`, cited here for calling slot 2, also calls a 78-byte
platform routine that reads the high-resolution counter. **A pool object asking what time it is says
nothing about the register bank**, and this page owns nothing in the platform layer.

**Neither layer is owned here.** The bank's subject is the EE/VU0 register file and its one user
thread; the platform edges are what a boot chain and a timer look like from the outside.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Presentation — CLIENT, fan-in of 396 edges.** Render bodies use the register-bank routines. By Presentation neighbours: `00397910` 76, `00398F90` 64, `0044B960` 36, `0036DD80` 29, and `CharacterRenderRecord_UpdateRootLODAndPresentationState` 24. Presentation is the bank's largest client by edge count.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAction — SERVICE.** `002368D0` on this page calls `BattleAction_ResetPresentationSlotPool`, owned by that layer. What it reaches is a 99-byte reset of **32 slots of `0x30` bytes** based at `022C17D8`: it clears the two heads at `[022BEB88]` and `[022BE978]`, and stamps each slot with `0x80000000`, a `-1` counter and an `0xFFFF` sentinel; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Resource — CLIENT (11 edges through 4 of this page's functions).** The Resource layer reaches this page at `0022A0B0`, `0017D280`, `002368D0`, `0042D050`. `ResourceTable_ResolveEntryByIndex` is the worked example, read in full - it is the paged resource-table lookup, and it gives the whole shape: the index selects a `0x10`-byte slot in one table and, shifted right by `byte[+0x4C]`, a `0x20`-byte group in another; a `-1` slot resolves to nothing, and everything else lands at the group's base plus `(index & dword[+0x50]) * dword[+0x48]`; **2 of the 11 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**ActorEntity — CLIENT and SERVICE (9 edges).** The actor body `0025C830` calls the VCLIP routine `0025A8E0` and the vf00 re-establisher `0036DD80` (which copies the constant (0, 0, 0, 1) from `008C5FD0` into vf00), and also calls the actor helpers `00233D70`, `ActorHandle_EncodeRegistryEntry` `003589B0` and `ActorResource_SubmitRequestDescriptor` `003DBB60` and the party commit thunk `PartyFocus_CommitPendingPackedActorHandle_Thunk` `00358BB0`; `0025C170` calls `0025C830`; `ActorSystem_InitializeManagerRuntime` `0026CE60` calls `00358BB0`; and the boot routine `0022A0B0` calls `BattleStorage_InitializeWorkArrays` `002368D0`. `0025C830` is one of the actor bodies that executes on the register bank (§5.1); its other callees are the actor layer's own work, and the boot routine that starts the emulation layer also sets up the battle work arrays.

**Audio — CLIENT and OUT-OF-SCOPE (16 edges).** The audio bodies `00361DE0`, `003623C0` and `00363FD0` call `0036DD80`, and `00361DE0` and `003623C0` call the flag-bit setters `0036DD90` and `0036DDA0`; `003631B0` calls `00361DE0` and `00362230` calls `00363FD0`; the thread start routines `007A5E50` and `007DD950` call the audio bodies `007AD630`, `007AD670`, `007BAEC0`, `007BB670`, `007BB780`, `007BC4F0` and `007DD600`. The audio closest-point helpers are VU0 routines on this bank (§4: `00363FD0` is `VSUBA` / `VMADD`, and the two setters set flag bits `0x80` and `0x40` on `00361DE0`'s compare paths), so audio is a client of the bank; the two start routines are roots of the worker-thread reachability walk in §7 and their audio callees are that thread's own work.

**Movement — SERVICE and CLIENT (7 edges).** `MainLoop_Draw` `0022B0B0` calls `00357780`, and `MainLoop_UpdateAndRenderFrame` `0022B8C0` calls `00263560` and `0037CF00`; `002368D0` calls `Navigation_ClearDataset` `00383A20`; `002F67C0` calls `002330D0`, which calls `00233050`; and `0026C3E0` calls `00358BB0`. The two loop entries are cited only as roots of the §7 walk and their movement calls are ordinary frame work; `002F67C0` writes vf01 and calls into movement, which is one of the bank's cross-layer consumers the census found.

**Party — SERVICE and CLIENT (3 edges).** `0022B8C0` and `0025C830` call `00358BB0`, and `PartyRoster_AssignActorAndCommitFocusWhenEligible` `0050C610` calls it too. `00358BB0` is a 5-byte thunk into the party layer's commit of a pending focus handle; the main loop and a bank-using actor body both commit focus through it, and nothing in the commit touches the register bank.

**RNG_Random_Selection — OUT-OF-SCOPE (1 edge).** `0022A0B0` calls `RNG_MT19937_Seed` `00379CF0`. The boot routine that starts the emulation layer also seeds the gameplay generator; the bank has nothing to do with it.

**Save_Load_Settings — CLIENT and OUT-OF-SCOPE (4 edges).** `GameSettingConfig_ParseText` `001DE5D0` and `GameSettingConfig_ParseOneSettingValue` `001DF350` call `0017D280`, and the program's main body `007980A0` calls `GameSettingConfig_InitDefaultsAndPath` `001DE050` and `GameSettingConfig_LoadOrCreateFile` `001DED50`. `0017D280` is a variadic print routine that formats to stdout (the start-up line of §2 goes through it), and the settings parser prints through it as well; `007980A0` is cited as the pool constructor's carrier, and loading the settings file is its other start-up work.

**Script_VM_Native_Bridge — CLIENT (24 edges).** 24 script-bridge bodies call `0017D280`, among them `0050C670`, `0050C8D0`, `0050D240`, `0050D5E0`, `0050EBA0` and `00510870`. They print through the same stdout routine the emulation start-up uses; that shares a print helper, not the register bank.

**UI — CLIENT (3 edges).** `0035DCC0` calls `0036DD80`; `00368010` calls the composer `00397910`; `00247AE0` calls `0039ADE0`. A UI body re-establishes vf00 before bank work, and two UI bodies call the library-shaped bank routines §5.1 lists; the UI is a client of the bank's routines.

**World — OUT-OF-SCOPE (1 edge).** `0022A0B0` calls `00266D10`. Another step of the boot routine, outside the one call (`0022A125`) this page cites it for.

**WorldAreaField — CLIENT and SERVICE (3 edges).** `World_UpdateSimulationTick` `00314020` calls `0017D280`, `0022B8C0` calls `00314020`, and `0025C830` calls `FieldData_GetActiveFieldRecordBit15` `00377C20`. The world tick prints through the shared stdout routine, the frame calls the world tick, and the bank-using actor body reads the field's action-permission bit; none of these is a register-bank relationship.

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-the-ee-and-vu0-register-bank-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `002330D0` | 59 B | calls a 114-byte helper with its arguments unchanged and, when the returned word is non-negative, adds to it the low 16 bits of (word `rcx+0x40` plus 1) times the sign-extended low word of `r8d`; returns the word, unchanged when negative | `002330E0`, `002330E8`, `002330EE`, `002330F8`, `002330FC` |
| `0029BC80` | 451 B | switches on dword `[rdx]`: for 4 it fills a stack vector (dword `01EF93F0`, -1.0 `01CEBC9C`, dword `01EF93F8`, 0), calls a 72-byte helper (`02AED560`, buffer), zeroes the buffer's dword `+0xC`, calls a 33-byte helper (buffer, buffer) and stores at word `+0x58` of qword `rcx+0x38` that signed word times (1.0 minus 1.428571 times (min(1.0, max(0.3, the xyz dot product of the vector and the buffer from a 37-byte helper)) minus 0.3)), truncated; for 2 it returns 0 at once when a 19-byte helper Q returns a negative value, else calls Q twice more and, when `rcx` is non-null, stores the third result at word `+0x9A`, 0 at `+0x98`, dword `01E0C1D8` at `+0x9C` and dword `01E0C1DC` minus the second result at `+0x9E`; for 1 it calls a 24-byte helper with `rcx` and the result of a 19-byte table-address helper for 0, then (when `rcx` is non-null) stores dword `01E0C1DC` minus the second Q result at word `+0x9A`, 0 at `+0x98`, dword `01E0C1D8` at `+0x9C` and the first Q result at `+0x9E`, and on both paths calls a 26-byte helper (`rcx`, `0xA1`); those three cases return 0, and any other value returns the result of a 3-byte stub that returns 0 (called with `rcx`, `rdx`) | `0029BCA1`, `0029BCBD`, `0029BD75`, `0029BDAA`, `0029BE1F` |
| `00398390` | 224 B | multiplies float `022D930C` in place by dword `01EF93F0`, copies the 16-byte vectors at `rcx` and `rdx` to `022D92E0` and `022D92F0`, stores the products y1*z2, z1*x2 and x1*y2 at `022D91A0`, `022D91A4` and `022D91A8`, stores the cross product of the two xyz parts (y1*z2-z1*y2, z1*x2-x1*z2, x1*y2-y1*x2) at `022D9300`, `022D9304` and `022D9308`, and copies the 16 bytes at `022D9300` to `r8` | `0039839C`, `003983B7`, `003983ED`, `00398450`, `00398467` |
| `003A2B90` | 53 B | stores the bit pattern of `xmm1`, sign-extended to a qword, at `022D8F30`, copies the 16 bytes at `022D8F30` to `022D92F0`, subtracts `xmm1` from each of the four floats of the 16-byte vector at `rcx`, and writes the result to both `022D92E0` and `rcx` | `003A2B9E`, `003A2BAC`, `003A2BB7`, `003A2BBA`, `003A2BC1` |
| `0050C670` | 54 B | takes `v` from the 7-byte getter of dword `02B40E18` (called with the incoming registers), calls an 85-byte helper (`00D22888`, v) and tail-jumps `VMResult_WriteInt32(rcx, v)` | `0050C67D`, `0050C68D`, `0050C6A1` |
| `0050C8D0` | 54 B | takes `v` from the 7-byte getter of dword `02B40E18` (called with the incoming registers), calls an 85-byte helper (`00D228A8`, v) and tail-jumps `VMResult_WriteInt32(rcx, v)` | `0050C8DD`, `0050C8ED`, `0050C901` |
| `00510870` | 220 B | reads three values a, b, c with three `VMValueStack_PopInt32CoerceFloat32(r9)` calls and takes `p` = a 421-byte helper's result for (c, b, a); when `p` is non-null and a 50-byte helper (`rdx`, `p`) returns non-zero it calls `VMResult_WriteInt32(rcx, 1)`, an 85-byte helper (`00D22B30`, c), a 27-byte helper (`p`, 1) and the 85-byte helper (`00D22B58`, a 109-byte helper's result for (byte `p+0x15`, word `p`)); otherwise it calls `VMResult_WriteInt32(rcx, 0)` and the 85-byte helper (`00D22B80`, c) | `005108B8`, `005108CB`, `005108DC`, `00510903`, `0051091E` |
| `006BA940` | 99 B | stores `00D81200` at qword `[rcx]`, calls a 300-byte helper (`rcx`), then eh_vector_destructor_iterator (`rcx+0x58`, `0x10`, 2, the address of `_guard_check_icall`) and eh_vector_destructor_iterator (`rcx+0x38`, `0x10`, 2, the address of `_guard_check_icall`), and tail-jumps a 34-byte helper (`rcx`) | `006BA959`, `006BA95C`, `006BA976`, `006BA990`, `006BA99E` |
| `00863410` | 26 B | when qword `rcx+0x18` is non-null calls it with qword `rcx+0x20` as `rcx`; returns 0 on both paths | `00863414`, `0086341D`, `00863421`, `00863423` |

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-03, cloud-drafted)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../../_index/candidates/fable-home-the-ee-and-vu0-register-bank-1003/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
| `003AC870` | 24 B | `00376470` + 0x82 | stores 1.0 (`01CEBBA8`) to dword `02B3F51C` and byte 0 to `02B3F503` | Interior anchor `003AC878`; Interior anchor `003AC880` |
