> Second pass, drafted by a Claude Opus 5.5 subagent under FABLE, 2026-09-27; its scratch scripts are not published. FABLE re-checked 004ADD10's selector (the local at [rbp+0x1A0] and the read-only callee 004AD9E0) by hand. This supersedes findings.md section 5's reasons for the five partial rows.

# UQ-213 - the five partial rows, resolved

Static read of `FFXII_TZA.exe` (image base `0x120000`), 2026-09-27. Nothing was executed. This follows up `uq213-programs.tsv` / `findings.md` section 5.

## Method

The method has three steps. A result counts only after the control below reproduces with it.

1. **Program side.** Find every GS hand-off in the program: `call r*` / `jmp rax` to the callback, or a call to an XGKICK leaf. For each one, compute the **reaching definitions over the function's CFG** of the value that picks the tag cell. That value is the kick `rcx`, the leaf's `02064DD0`, or the index of the 16-byte cell copied into the output. The instrument is `cfg_reach.py FUNC USE REG|mem:ADDR`. It builds basic blocks from every direct `jcc`/`jmp` and does a backward search. For `mem:` targets it reports the calls it passes through, and each of those callees was then read.
2. **Template side.** Decode the tag cell from the builder's own immediate stores (the page's field layout):
   - NLOOP is bits 0-14 and EOP is bit 15.
   - In the upper dword: PRE is bit 14, PRIM is bits 15-25, FLG is bits 26-27 and NREG is bits 28-31.
   - REGS is one nibble per register.
3. **Between build and upload.** List every writer of the tag cell and of any A+D PRIM pair. This covers rip-relative stores (`riprefs.py`), and register-based stores in each user of the template, read from their bodies.

Tools, all in the scratchpad: `dumpfn2.py` (a dump with rip targets resolved), `cfg_reach.py`, `vi_stores.py` (`uq213_vi.py` plus a record of every store to a tracked VU cell).

## Control: type 0x68, program 004E0F70 - PASS

**Program side.**
- **Leaf call.** `004E289C call 004DF360`. The only reaching definition of `02064DD0` there is `004E148E mov word [02064DD0], r8w`. The callees it passes through do not write it:
  - `0022CC20` writes only `01E02830`;
  - `0022CC30` / `0022CC40` write only `02064DEC`;
  - `004DF360` writes only `02064DB0`/`DB4`/`DB8`/`C60`.
- **The r8 at `004E148E`.** Its reaching definitions are `004E0FED` / `004E11A9` / `004E11F1`. All three load `word [02064B0C]`, which is never written and so is 0. So `DD0` = 0.
- **Inside the leaf.** `004DF366`/`004DF386` load `cell[word 02064DD0]`. Its bytes +4..+F are written to the kick cell at `004DF3EC`/`004DF3F2`, then `call r11` at `004DF410`.
- **A+D kick.** `004E0FB6`-`004E0FEA`: `rcx` = cell `word[02064B0C]` + 0x2B = 43.

**Template side.**
- `004E2930`, cell 0: `004E2999` `+0x20` = `0x8000` (NLOOP 0, EOP); `004E2992` `+0x24` = `0x602E4000`; `004E298B`/`004E2984` REGS = `0x00008000_00412412`.
- Decode: NREG 6, FLG PACKED, PRE 1, PRIM `0x05C`. That is TRIANGLE_STRIP with IIP (0x08), TME (0x10) and ABE (0x40). REGS is ST, RGBAQ, XYZF2, ST, RGBAQ, XYZF2.

**This equals the page's decode, TRIANGLE_STRIP 0x05C, IIP+TME+ABE, NREG 6.** The control passes.

---

## 004758E0 - TRIANGLE_FAN, PRIM set by an A+D write: 0x5D (IIP+TME+ABE) or 0x4D (IIP+ABE) per block, as the caller writes it; vertex tag PRE=0, NREG 3 ST,RGBAQ,XYZF2 - **read**

The program emits no leaf kick. It builds a **GIF tag chain** in VU cells 100+ and hands its head to the callback once.

### The vertex tag

- `0047597E` sets `r9` = base × 16, and `004759D1` adds 0x10: the cell is base + 1.
- `00475A17` loads that cell (template cell 1) and `00475A2D` stores it to `02064B40`.
- The only reaching definition of `02064B40` at its single read, `00476A35`, is `00475A2D`. The callees it passes through do not write it:
  - `005375F0` and `005376D0` / `005379D0`, whose only pointer store is `mov word [rdi]`, into the VI words `02064B10`/`B12`/`B14`;
  - `0022CC20`.
- Image-wide, `02064B40` has 2 rip references, both in this function.

### Chain build, per block

- **Block index.** It is `02064DB8`. Its reaching definitions are `004759A6` (base + 2, from `0047593A`) and `00476B7B` (+0xF per block, `00476B76`). So the A+D blocks are template cells 11/26/41/56.
- **Block enable.** `00475AA9` reads `word cell[blk]`; `00475AD4`/`00475AD8` skip the block when it is 0.
- **A+D copy.**
  - Loads: `00476912`/`00476995` (cell blk+9 = the A+D tag, NLOOP 5, EOP 0), `00476917`, `0047692C`, `0047693F`, `00476957`, `00476969` (cells blk+10..+14 = CLAMP_1, TEX0_1, ALPHA_1, TEST_1, **PRIM**).
  - Stores to the cursor (`02064DB4`, set to 100 at `004759B5`): `004769A1`, `004769BB`, `004769D5`, `004769E8`, `004769FB`, `00476A0F`.
- **Vertex tag and its cell pointer.** `00476A18` records the next cursor cell at cell base+0x50. `00476A5C` stores the `02064B40` tag there.
- **Vertices.** The loop `00476A61`-`00476B25` writes 3 cells per vertex: ST (`00476B0D`), RGBAQ (`00476B08`), XYZF2 (`00476B1C`).
- **NLOOP.** `00476B46` stores `dword = si`, the vertex count. EOP is 0 and bits 16-31 are 0; PRE, PRIM and NREG are left alone.

### End of the chain

- `00476C14`-`00476C47`: the last vertex tag, whose cell is read from cell base+0x50, gets `+0x8000` (EOP).
- `00476C35` gives cell 100. `00476C5E`/`00476C61` then do `call r12` with `rcx` = cell 100.
- `r11` = base at both uses: its reaching definitions at `00476A03` are `00475F8A`/`0047672F` = `word [02064B0C]`.

### Template (02AE9600, builder 00476C80)

| cell | stores | content |
|---|---|---|
| 1 | `00476CEA` (dword0 = 0), `00476CF2` (`0x30000000`), `00476CF9` (REGS `0x412`) | NREG 3, PRE 0, ST,RGBAQ,XYZF2 |
| 11+15k | fill loop: `00476D7B` = 5, `00476D85` = `0x10000000`, `00476D8F` = 0xE | A+D, NLOOP 5 |
| 16+15k | `00476DE2` data `0x5D` (address `rdx` = 0) | the PRIM pair |

So the vertices take PRIM from the A+D PRIM write, because the vertex tag has PRE 0.

### Runtime writers of the block-0 PRIM data (`02AE9720` = template +0x120 = cell 16)

| writer | 0x5D (textured branch) | 0x4D (untextured branch) |
|---|---|---|
| `0036F550` (VFX layer emit) | `0036F6D7` | - |
| `0036F9F0` (layer reset) | `0036FB6B` | - |
| `00374280` (screen-effect kind 6) | `00374358` | `003743FB` |
| `003745C0` (kind 2) | `003746C4` | `00374761` |
| `00462540` (type 0xA2) | `004628FD`, `00462A68` | `0046272F` |
| `00463460` (type 0xA5) | `00463788`, `0046394A` | `00463614` |

- For both effect types the store is `mov dword [reg+0x30], ...`, and the base is the per-block PRIM cell:
  - `00462540`: `rdi` = `02AE96F0` (lea at `00462673`), then +0xF0 per block (`00462F91`);
  - `00463460`: `rbx` = `02AE96F0` (lea at `0046355F`), then +0xF0 per block (`004637D4`).
- None of these writes the cell-1 vertex tag. The rip-relative writers touch +0x28/+0x2C at most below +0x40. `00462540`'s `rdi`-relative stores go no lower than `rdi-0xB0` (+0x40).
- The template object is itself the uploaded packet: `00462FE0`-`00463004` pass `+0x18`, `+0x8` and `+0xC` to `003A34D0`.

**Confidence: read.** The mode and the TME bit are the caller's choice, and every writer is listed above.

---

## 0047A9C0 - TRIANGLE_FAN PRIM 0x05D (IIP+TME+ABE), PRE=1 vertex tag, NREG 3 ST,RGBAQ,XYZF2; preceded in the chain by A+D NLOOP 4 (CLAMP_1, TEX0_1, ALPHA_1, TEST_1) - **read**

This is the same chain shape as 004758E0, but the primitive comes from the vertex tag's PRE, not from an A+D PRIM write.

### Program side

**The vertex tag.**
- `0047AA65`/`0047AA9D` load cell base+0 (`r9` = `r11` × 16, `0047AA1A`/`0047AA23`) and `0047AABE` stores it to `02064B40`.
- At `0047B89E` the only reaching definition is `0047AABE`, through the callees `005375F0`, `005376D0` and `0022CC20`.

**Chain.**
- `r11` = base, from its reaching definitions `0047AD2B`/`0047B627` at `0047B7EA`.
- Loads: cells 11..15 at `0047B810`/`0047B88A` (the A+D tag), `0047B815`, `0047B82B`, `0047B83F` and `0047B854`.
- Stores to the cursor: `0047B896`, `0047B8B0`, `0047B8CA`, `0047B8E1`, `0047B8F0`.
- `0047B8FC` records the tag cell at cell base+0x50.
- `0047B923` stores the `02064B40` tag.
- The vertex loop is `0047B930`-`0047B9F4`, 3 cells per vertex.
- `0047BA15` stores NLOOP = `si`.

**End.** `0047BA4D`-`0047BA80` set EOP on the last tag. `0047BA6E`, `0047BA97` and `0047BA9A` do `call r15` with `rcx` = cell 100.

### Template (02AE9A50, builder 0047BAF0)

- UNPACK `0x6C140000` (V4-32, num 20, addr 0) at `0047BB2D`.
- Cell 0 (`+0x20`): dword0 = 0 (`0047BB2D` qword); `0047BB35` = `0x302EC000` → NREG 3, PRE 1, PRIM `0x05D`; REGS `0x412` (`0047BB3C`).
- Cell 11: `0047BC53` NLOOP 4, `0047BC5D` A+D, `0047BC67` REGS 0xE.

### Between build and upload

- The only user, `00375280`, copies the whole 0x170-byte template to the stack (`003752CA`-`00375357`) and then patches it:
  - TEX0_1 data at copy +0xF0 (`003753A1`);
  - ALPHA_1 data at +0x100 (`003753B5`, from the alpha table `01EFAC20`);
  - data cells at +0x50..+0xCC.
- **Nothing lands on +0x20..+0x2F (the tag) or +0xD0.** The patched copy is what `00375438 call 003A35E0` registers.
- Image-wide rip references to the object: only the `lea`s `003752CA` and `0037E2A4`.

**Confidence: read.** `00375280` writes ALPHA_1 at run time, so the template's `ALPHA_1 = 0x44` is not the drawn value.

---

## 004ADD10 - TRIANGLE_FAN PRIM 0x05D (IIP+TME+ABE), NREG 3 ST,RGBAQ,XYZF2 (template cell 17); first kicks A+D NLOOP 2 CLAMP_1, TEX0_1 (cell 13). The strip tag at cell 16 is uploaded but never used - **read**

**The previous pass's premise was wrong.** The `r13` that `004AF20C` loads does not reach the tag load.
- `004AF20C` reads word0 of VU cell 27. That cell is a program-owned double-buffer pointer:
  - `004ADE4E` writes 0x35, from `004ADE20`;
  - `004ADE6B` writes cell 28 = 0x53, from `004ADE2C`;
  - `004AF232`-`004AF24E` swap the two.
- **Its value never picks the tag cell.**

**Tag load.** `004AFE4D lea eax, [r13+0x11]`, then `004AFE64 movups xmm0, [cell]`.
- `cfg_reach.py 004ADD10 004AFE4D r13`: the only reaching definition is **`004AFBD1 movsx r13d, word [rbp+0x1A0]`**, a stack VI local.
- **`[rbp+0x1A0]`: its only writer is `004ADDC0 mov qword [rbp+0x1A0], rax`, with `rax = 0` (`004ADDBE xor eax, eax`).** A scan of every `rbp`-relative store whose range overlaps +0x1A0..+0x1A1 finds only that one, and there are no indexed `rbp` stores.
- The five calls that take `lea r9, [rbp+0x1A0]` all go to `004AD9E0`. It only reads `[r9]`/`[r15]` (`004ADA22`, `004ADCAE`).
- So `r13` = 0 and the tag is **cell 17**.

**Emission.** `004AFE5C`-`004AFE93` copy the tag to cell `word[cell 27]` − 1. `004AFE7F`/`004AFE96` stamp dword0 = `di | 0x8000` (NLOOP = count, EOP). `004AFEA9 call [rbp-0x80]` (the saved callback, `004ADD84`) with `r8` = 1.

**The first kick** is `004ADEB5`/`004ADEBC`, with `rcx` = `02064F00` = VU base `02064E30` + 0xD0 = cell 13. These two are the program's only callback calls.

**Template (02AE31F0, builder 004B0000).**

| cell | stores | decode |
|---|---|---|
| 13 | `004B01A4` `0x8002`, `004B01AE` `0x10000000`, `004B01B8` 0xE; pairs at `004B01CA` (8 = CLAMP_1) and `004B01DC` (6 = TEX0_1) | A+D, NLOOP 2, EOP |
| 16 | `004B01E7` `0x8000`, `004B01F1` `0x302E4000`, `004B01FB` `0x412` | STRIP `0x05C`, NREG 3 |
| 17 | `004B0206` `0x8000`, `004B0210` `0x302EC000`, `004B021A` `0x412` | **FAN `0x05D`, PRE 1, NREG 3, ST,RGBAQ,XYZF2** |

The template's only user, `0045AEF0` (type 0x94), writes:
- +0x50/+0x54 and +0x40..+0x4C (cells 2 and 1);
- +0x100 and +0x110 (the CLAMP_1 and TEX0_1 data);
- `lea`s of +0x60 and +0xB0 passed as the output of `00397910`.

None of these reaches +0x120..+0x13F. The object is registered as is (`0045B173`/`0045B213` +0x18, through `003A2F70` at `0045B19E` / `003A33B0` at `0045B227`).

**Confidence: read.** The answer is "fan, not strip, in every template", because this program has one template and its cell index is constant. A residual check was not done: the vertex loop's register-based stores into VU memory were not proved to stay off cell 17. They write at `word[cell 28]`, which is ≥ 0x35.

---

## 004C0EA0 - TRIANGLE_STRIP PRIM 0x054 (TME+ABE, flat), NREG 9 ST,RGBAQ,XYZF2,ST,XYZF2,ST,XYZF2,ST,XYZF2 (one colour and 4 textured vertices per loop, i.e. a quad); preceded in the chain by A+D NLOOP 1 TEX0_1 - **read**

**Where its state lives.** The VI-like state is a private **.data block `02CA7F40`-`02CA7F7F`**. It is not in a different VU memory bank: the VU memory it addresses is the usual `02064E30` (`004C0F41 lea r13`).
- `riprefs 02CA7F40 02CA7F80`: 41 references, **all in 004C0EA0**.
- No image-base-relative disp32 (`0x2B87F40`-`0x2B87F7F`) and no absolute pointer to it occur in the file.
- `004C0F68`-`004C0FAF` zero the block on entry.

**The fields.**

| field | value | set at |
|---|---|---|
| `02CA7F44` | tag cell = **0xBB (187)** | `004C1011` |
| `02CA7F48` | vertex cursor = 0xBC (188) | `004C101D`; then `004C1640`/`004C1E5B` |
| `02CA7F54` | chain start = **0xB9 (185)** | `004C1029` |
| `02CA7F50` | loop count, word +4 of VU cell 2 | `004C1006`/`004C1030` |
| `02CA7F4C` | NLOOP counter | zeroed at `004C0FC1`, then `inc` at `004C1623`/`004C1E23` |

The only reaching definition of `02CA7F44` at `004C1F82` is `004C1011`, and of `02CA7F54` at `004C1FBF` is `004C1029`. The paths pass `sinf`/`cosf` only.

**Emission.**
- `004C1F8E` ORs 0x8000 into `02CA7F4C`.
- `004C1FB5`/`004C1FBB` store dword `02CA7F4C` into cell 187's dword0 (NLOOP = loop count, EOP). The high word `02CA7F4E` is only ever zeroed (`004C0F68`).
- `004C1FBF`-`004C1FDA`: `rcx` = VU cell 185. `004C1FDD`/`004C2032` do `jmp rax` (the callback, `rax` = `r12` = the entry `rcx`, from `004C0ECB`), with `r8` = 1 (`004C1F95`).
- This is the only hand-off.

**Template (02AEA3A0, builder 004C2040; registered with 004C0EA0 by `004620CF`-`004620FC`, which pass +0x18 and size 0xC08).**

| cell | stores | decode |
|---|---|---|
| 185 | `004C20C1` = 1 (NLOOP 1, EOP 0), `004C20B7` `0x10000000` (A+D) | A+D block |
| 186 | `004C20CB` = 6 | TEX0_1 |
| 187 | `004C20F3` `0x8000`, `004C20E9` `0x902A4000`, `004C20DF` `0x24242412`, `004C20D5` = 4 | NREG 9, PACKED, PRE 1, PRIM `0x054`; REGS 2,1,4,2,4,2,4,2,4 |

The walk `00461270` writes cell 186's data (+0xBC0/+0xBC4 at `00461ABF`/`00461AC5`) and the cells +0x20..+0x58. It does not write +0xBB0 or +0xBD0 rip-relatively.

**Confidence: read.** One residual: the walk's per-item stores (`rsi` from `02AEA3F4`, stride 0x30) are bounded by a byte count (`[rdi+0x1B3]`), not by a visible constant. That they stop below cell 185 rests on the item layout (3 cells per item from cell 3) and was not proved.

---

## 004E7D90 - TRIANGLE_STRIP PRIM 0x05C (IIP+TME+ABE), NREG 6 ST,RGBAQ,XYZF2 ×2, for BOTH 0x6B and 0x67; first kicks A+D NLOOP 4 CLAMP_1, TEX0_1, ALPHA_1, TEST_1 (cell 25) - **read**

**Program side.** It is the same for both types.
- **A+D kick.** `004E7DF2`/`004E7DF9`: `rcx` = cell `word[02064B0C]` + 0x19 = 25; `004E7E0E call r14`.
- **Leaf calls.** At `004EB7F8` and `004EB8AC` (`004E78A0`), the only reaching definition of `02064DD0` is `004E8069 mov word [02064DD0], r8w`, whose `r8` comes from `004E7E11 movsx r8d, word [02064B0C]` = 0. So **the cell is 0**.
- **Callees.** `0022CC20`/`30`/`40` and `sqrtf` do not write `DD0`. `004E78A0` reads it (`004E78A6`) and writes only `02064DB0`/`DB4`/`DB8`/`C60`.
- **Stores to cells 0 or 25.** The linear store tracker (`vi_stores.py`) finds none; the tracked stores go to cells 70 and up.

**The 0x67 payload.**
- The walk `00460170` sets `[02CA5EF0]` = `02AEC660` (`0046019F`/`004601B1`) and registers `rcx` = `02AEC660`+0x18, size **0x1E8** (`00460790`/`00460784`, `004607A2 call 003A33B0`). So the packet is `02AEC678`-`02AEC85F`.
- **The builder of `02AEC660`, `004E7980` (startup/39), tail-jumps at `004E79AF` to `004E7A90` with `rcx` = `02AEC670` (`004E7998`).** `004E7A90` is the same payload builder the hub also calls for 0x6B's `02AECAD0` (`0037E1A8`/`0037E1AF`; the hub builds `02AEC660` at `0037E184`/`0037E18B`).
- So the 0x67 packet is STCYCL + UNPACK V4-32 num 30 addr 0 (`004E7AAC` `0x6C1E0000`), and then cells 0..29 with the same tag cells as 0x6B:

| cell | stores | decode |
|---|---|---|
| 0 | `004E7AB3` `0x8000`, `004E7ABA` `0x602E4000`, `004E7AC1`/`004E7AC8` REGS `0x00008000_00412412` | STRIP `0x05C`, PRE 1, NREG 6 |
| 25 | `004E7CE6` `0x8004`, `004E7CF0` `0x10000000`, `004E7CFA` | A+D, NLOOP 4, EOP |

- **Walk writes into that payload.** They are made only through `[02CA5EF0]`, whose 12 references are all in `00460170`:
  - +0x40..+0x58 and +0x60..+0xEC (cells 2-12);
  - +0xF0..+0x16F (cells 13-20, the matrices at `004605BF`-`00460621`) and +0x168;
  - +0x1C0 and +0x1D0 (CLAMP_1 and TEX0_1 data, `00460492`/`004604A0`);
  - +0x1E0 (ALPHA_1, `004604BB`) and +0x1F0 (TEST_1 = `0x51001` or `0x70000`, `004604D2`).
- **None of these touches +0x20 (cell 0) or +0x1B0 (cell 25).**
- **The second payload.** It is `[rdi+0x3D0]`, 0x260 bytes per item, initialised from `02AEC860` (startup/40) by `0045FD50` (`0046003A`-`004600BE`). Its UNPACK is num 34, addr 30 (cells 30-63), followed by MSCALF 0. So it re-runs 004E7D90 per item without overwriting cells 0 or 25. The walk fills its data at `00460680`-`00460703`.

**Confidence: read.** The template's CLAMP_1/TEX0_1/ALPHA_1/TEST_1 placeholders are filled at run time by the walk (0x67) or the pair builder (0x6B). The PRIM comes from the cell-0 tag's PRE, so it does not depend on them.

---

## Summary

| program | draws | confidence |
|---|---|---|
| `004758E0` | TRIANGLE_FAN via A+D PRIM: `0x5D` IIP+TME+ABE or `0x4D` IIP+ABE per block (caller-written); PRE=0 vertex tag, NREG 3 ST,RGBAQ,XYZF2 (template cell 1); up to 4 fans per packet | read |
| `0047A9C0` | TRIANGLE_FAN `0x05D` IIP+TME+ABE, PRE=1 tag (template cell 0), NREG 3; after A+D NLOOP 4 | read |
| `004ADD10` | TRIANGLE_FAN `0x05D` IIP+TME+ABE (template cell 17, fixed by stack VI local `[rbp+0x1A0]` = 0); strip cell 16 unused | read |
| `004C0EA0` | TRIANGLE_STRIP `0x054` TME+ABE flat, NREG 9 (ST,RGBAQ,XYZF2 + ST,XYZF2 ×3), cell 187; state in the private block `02CA7F40`-`02CA7F7F` | read |
| `004E7D90` | TRIANGLE_STRIP `0x05C` IIP+TME+ABE, NREG 6, cell 0, for both 0x6B and 0x67 (0x67's payload is `004E7A90`-built at `02AEC670`) | read |

**Corrections to `uq213-programs.tsv` / `findings.md`.**
- **004ADD10.** "the tag cell index depends on a VU-memory word (`004AF20C`)" is wrong. That word is a program-written buffer pointer, and it does not reach the tag load. The cell is constant 17.
- **004758E0 (and the section 4 count).** The fan is not always `0x5D`. Screen-effect kinds 2 and 6 and effect types 0xA2 and 0xA5 write `0x4D` (untextured) in their no-texture branches.
- **004E7D90 / 0x67.** 0x67 does not "read only the MPG record `02AEC660`". Its first payload spans `02AEC678`-`02AEC85F`, which is the `004E7A90`-built template.
