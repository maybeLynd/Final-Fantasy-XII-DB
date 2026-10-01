> Drafted by a Claude Opus 5.5 subagent pass under FABLE, 2026-09-27. The instruments it names were scratch scripts and are not published here. The bytes-decided claims are in `uq204_emits.py` (E5). FABLE re-read the `0xA9` tag stores (`00479613`, `0047961A`), the drain branch and the scratch-base setter `0022A152` by hand.

# UQ-204 residue: what the six raw-packet walks would draw, and whether the mode-0 staging is read

Static read of `FFXII_TZA.exe` (image base `0x120000`), 2026-09-27. Instruments are in the scratchpad:
- `dumpr.py`: `dumpfn.py` plus resolved rip targets.
- `rd.py`: section-aware byte dump. It reports the `.data` virtual tail, which starts at `01F7E400`.
- `trk.py`: a linear register follower with four modes. `addr` follows lea-rip or image-base addresses. `load` follows a qword loaded from a global. `reg` follows a register-passed pointer. `deref` follows a pointer loaded out of a table.
- `callers.py`: a raw E8/E9 index.
- `ibrel2.py`: `ibrel.py` with the `rip` base excluded. `ibrel.py`'s regex also matches `[rip + disp]`, so it can report false positives, for example `0016D124`.

## Common frame: the arena prefix that `003A3010` / `003A31A0` lay down (no PRIM)

Both appenders write the same 0x40-byte prefix at `[02F8F2D0]` before the walk's packet:

| arena off | store | value | meaning |
|---|---|---|---|
| +0x00 | `003A3063` word / `003A307D` byte+3 | 3 / 0x10 | DMA tag: QWC 3, ID 1 (cnt) |
| +0x08 | `003A3096` dword | 0 | VIF NOP |
| +0x0C | `003A306E` word / `003A3082` byte+0xF | 3 / 0x50 | VIF `DIRECT 3` |
| +0x10 | `003A3078` word | 0x8001 | GIF tag low: NLOOP 1, EOP 1 |
| +0x14 | `003A3047` and 0x3FFF, `003A3056` or 0x20000000 | | PRE 0, PRIM 0, FLG 0 (PACKED), NREG 2 |
| +0x18 | `003A3087` qword | 0xEE | REGS: A+D, A+D |
| +0x20/+0x28 | `003A30AA` / `003A30AE` | `qword[01EFAC20 + 8*dword[02AEE900]]` (`003A309A`/`003A30A6`), then 0x42 | `ALPHA_1` |
| +0x30/+0x38 | `003A30B6` / `003A30BE` | 0x51001, then 0x47 | `TEST_1`: ATE 1, ATST NEVER, AFAIL FB_ONLY, ZTE 1, ZTST GEQUAL |

`003A31A0` makes the same stores at `003A31F3`–`003A3254`.

- The `ALPHA_1` table at `01EFAC20` is in the file-backed `.data`. It reads `0x44, 0x48, 0x42, 0x44, 0x49, 0x46, 0x80000000A8, 0x04`.
- One literal oddity: bits 16–31 of the GIF tag (word +0x12) are never stored, and bits 32–45 survive the `and`. The tag's reserved field therefore carries whatever the arena held before.
- **This is a GS register-write tag with PRE = 0. It sets no primitive.**
- Then the walk's packet is copied to arena +0x40. `003A3160`/`003A3172` (and `003A3318`/`003A3321` in `003A31A0`) re-tag packet +0x10 as `0x30` (ref) and point it at packet +0x20.
- In the four walks below, packet +0x10 is never written. So that descriptor's QWC word is 0.

"Mode 0" in each walk is selected when the blend index is 0. That index is `byte[def+0x49] >> 5`; for `0x97` it is `word[def+0x24A] & 7`. The branches are `0044D7BF`, `00453780`, `00460ECC` and `0045BE4F`. `0xA4` and `0xA9` have no mode-0 call.

## (A) Per walk

### `0x81` — walk `0044D4A0`, packet `02AE0850`, 0x150 bytes
- **PRIM: none.** No GIF tag and no PRIM (A+D register 0x00) store exists in the packet.
- The packet is `lea`'d only at `0044D7F2` and `0044D805`. It is handed to `003A3010` (`0044D7F9`) or `003A2D80` (`0044D80C`), with the size set at `0044D7ED` and `0044D800`.
- Every store into it is a rip store in the walk: first at `0044D519` (+0x20), then +0x20–+0x9F and +0xC0–+0xEF. The one callee store is the 4×4 matrix `00397910` writes through `r8 = 02AE0940` (+0xF0–+0x12F, `lea` at `0044D7AB`; loop stores `00397A75`/`00397AB6`/`00397ADC`/`00397AE0`).
- **+0x00–+0x1F and +0x130–+0x14F are never written.** The object is in the `.data` virtual tail, so it is 0 at load. Five checks found no other writer:
  - `riprefs 2AE0850 2AE09A0`: only this walk.
  - `trk addr`: no other register-based access or call argument.
  - `ibrel`: 0.
  - Raw dword search for the address or its RVA: 0.
  - The startup hub `0037DF90`/`0037E0F0` registers no builder for it. It sits directly after template `02AE06B0` (`004A1C10`), which ends at +0x198.
- The contents are floats and ints (def `+0x220..+0x290`, element `+0x230..+0x258`, the colour bytes from `0026EE00`) and a matrix. That is VU-input data, not a GS packet.
- **Confidence: read.** The tag is absent.

### `0x8A` — walk `00453150`, packet `02AE5B90`, 0xDC0 bytes
- **PRIM: none.** The packet is handed off at `004537A5`, `004537BC` and `004537CB`, with the size set at `004537A0`, `004537B7` and `004537C6`.
- The lowest store is `00453369` (+0x20). Other stores:
  - Up to 32 rows of 0x50 bytes at +0x1A8, copied from resource items at stride 0x90 (`0045353D`–`0045359D`).
  - Indexed dword pairs at +0xBA0 and +0xBA4 (`00453632`, `0045363F`).
  - Qwords at +0xBB8 with stride 0x10 (`004535C8`).
  - A matrix at +0xF0 via `00397910` (`r8 = 02AE5C80`, `00453706`).
- +0x00–+0x1F are never written. The same checks as `0x81` all came back empty.
- The resource rows are copied field by field. None of them is a constant, and nothing is tag-shaped.
- **Confidence: read.**

### `0x97` — walk `0045BAD0` → `0045BAE0`, packet `02AE3460`, 0x1C0 bytes
- **The drawn data comes from a resource.** At `0045BE30`/`0045BE37` the walk reads `dword[def + 0x2A0 + 4*dword[elem+0x298]]` and resolves it (`0045BE3E`).
- It then passes `Resolve(entry+0x10)` as a pointer and `dword[entry+0x14]` as a byte count to one of two calls:
  - `003A2E30` (`0045BE73`, mode 0), which appends a `0x30` ref descriptor at `003A2E95`–`003A2EA6` plus a `STCYCL 4/4` descriptor at `003A2EB6`–`003A2ED2`.
  - `003A31A0` (`0045BEE0`), which inserts the same pair at `003A333F`–`003A3383`.
- The packet itself has no tag. Its lowest store is `0045BE09` (+0x40), and +0x00–+0x3F are never written.
- **Stopped there, as instructed.** The primitive would be in the resource payload.

### `0xA0` — walk `00460BC0`, packet `02ADEDF0`, 0x150 bytes
- **PRIM: none.** The packet is handed off at `00460EF5` (`003A3010`, with `r8d = 0`) and `00460F08` (`003A2D80`).
- The lowest store is `00460C2A` (+0x20). The top of the packet, +0xF0–+0x12F, is a 64-byte copy from `02AEECB0` (`00460E9C`–`00460EC5`).
- The only other reference in the range is `0037D8AA` (`lea rcx, 02ADEE7C`) in `0037D890`. It is a loop end bound. The loop's last store is at `02ADEC8C`, below the packet.
- **Confidence: read.**

### `0xA4` — walk `00522300`, packet `02AE9300`, 0x210 bytes
- **PRIM: none.** The only hand-off is `003A3010` at `005227C5`, with the size set at `00522778`.
- The lowest store is `00522549` (+0x40), and +0x00–+0x3F are never written.
- **Probably the data half of a CLAMP_1 / TEX0_1 / ALPHA_1 / TEST_1 register block, with the tag and register addresses missing.** This is an inference from layout, not from a tag. The qword slots at +0xE0, +0xF0, +0x100 and +0x110 take four values:

  | slot | store | value |
  |---|---|---|
  | +0xE0 | `005225DD` | `00431830`'s second output qword (`dword[def+0xCC]`) |
  | +0xF0 | `005225E8` / `005226FB` | `00431830`'s first output qword, a TEX0-shaped word; CBP is OR'd in above bit 37 at `00431A9A` |
  | +0x100 | `0052273E` | `qword[01EFAC20 + 8*i]`, the `ALPHA_1` value table (image-base form `[rbx+rdx*8+0x1DDAC20]` at `00522728`/`00522736`) |
  | +0x110 | `0052278E` | 0 |

  - That is the same register order as `0xA9`'s template (below).
  - But the tag that would sit at +0xD0 and the address qwords at +0xE8, +0xF8, +0x108 and +0x118 are **never written**. There is no template for this object.
- **Confidence: read** for the absence of a tag; **partial** for the A+D-block reading.

### `0xA9` — walk `00528150` → `005479B0` / `00547A00` → `00540C20`
The walk builds up to four 0x90-byte records on the stack (base `rbp-0x30`). `00547A00` then lays them into the arena at `[02F8F2D0]` from two startup templates:
- `02AE8CF0`: builder `004795D0`, hub call at `0037E227`.
- `02AE8D30`: builder `00479450`, hub call at `0037E233`.

Both templates are virtual-tail objects. Their bytes are the builders' immediate stores. Nothing else writes either range: `riprefs` and `trk` find only the hub and `00547A00`, and `ibrel` returns 0.

**The vertex-list tag (template `02AE8CF0`):**
- Arena +0x00–+0x1F is copied from `02AE8CF0` (`00547A9B`–`00547AB1`). That is the MPG descriptor from `008631E0` (+0 word 1, +3 `0x30`, program `00479650`), then `BASE 0` / `OFFSET 0`, then the `008631D0` sub-header (`w=2`), then `STCYCL 4/4`, then `UNPACK V4-32 num=2 addr=0` (`0047960B`).
- `00547ABC`/`00547AC7` re-point that descriptor at `02AE8D10` (template +0x20).
- **Template +0x20 is a GIF tag:**
  - Low dword 0: the qword store at `0047960B` ends there. So NLOOP = 0 (stamped at run time) and EOP = 0.
  - High dword **`0x302E4000`** (`00479613`): **PRE 1, PRIM 0x5C, FLG 0 (PACKED), NREG 3**.
  - REGS **`0x412`** (`0047961A`): `ST, RGBAQ, XYZF2`.
- **PRIM 0x5C = type 4 (TRIANGLE_STRIP), IIP 1 (Gouraud), TME 1 (textured), FGE 0, ABE 1 (alpha blend), AA1 0, FST 0 (STQ, not UV), CTXT 0, FIX 0.** Vertex count per loop = 1 × (ST, RGBAQ, XYZF2). NLOOP is not fixed.
- Template +0x30 holds floats 2048.0, 2048.0, 256.0, 224.0 (`00479622`–`00479637`).

**The register block (template `02AE8D30`):**
- `00547A2F`–`00547A99` copy the whole 0x100 bytes to the stack.
- Per record, the walk's fields overwrite it (`00547B3B`–`00547BE6`), and the result is copied to the arena at `00547C21`–`00547CAF` (first record, 0xF0 bytes) or `00547CB5`–`00547D13` (later records, 0x100 bytes).
- The template has `UNPACK V4-32 num=12 addr=2` at `0047946C`. Its payload cell 7 (+0x80) is **an A+D tag**: `0x8004` (`00479513`), `0x10000000` (`0047951D`), `0xE` (`00479527`). That decodes as NLOOP 4, EOP 1, PRE 0, NREG 1, A+D.
- That tag carries four register writes, but no PRIM:

  | reg (addr store) | template value | per-record value (walk store → `00547A00` copy) |
  |---|---|---|
  | `CLAMP_1` 0x08 (`00479539`) | 0 | rec+0x70 → t+0x90 (`00547BAF`/`00547BB6`). Written at `00528424` (0), `005284BA` (the `00431830` second qword in that arm, or `dword[r15+0x22]`). |
  | `TEX0_1` 0x06 (`0047954B`) | 0 | rec+0x78 → t+0xA0. Written at `0052842C`/`005284C9`: the `00431830` first qword. |
  | `ALPHA_1` 0x42 (`00479561`) | 0x44 | rec+0x80 → t+0xB0. Written at `005284E0`: the `01EFAC20` table. |
  | `TEST_1` 0x47 (`00479577`) | 0x33001 | rec+0x88 → t+0xC0. Written at `00528782` (0x1001: ATE 1, ATST NEVER, AFAIL FB_ONLY, ZTE 0) or `00528792` (0x51001: … ZTE 1, ZTST GEQUAL). The branch is at `00528727`/`00528780`. |

- The tail is `MSCALF 0` (`00479582`), `FLUSH`, `DIRECT 1`, the `0x8000` empty terminator (`004795A1`) and `FLUSHA`.
- `00540C20` appends the sort entry: +0 is the arena block (`00540C4A`), and the +0x10 callback is 0 (`00540C63`).
- **Confidence: read** for the tag fields, since the template bytes were replayed from the stores. **Partial** for the draw: NLOOP is stamped by microprogram `00479650`, which was not read, and so is which cells it emits.
- Side finding: `Legacy-PS2-GS/members/vif1-gif-tags.tsv` has a row for `00479450` (the A+D tag, which matches the above) but **no row for `004795D0`**, even though this PRIM 0x5C tag sits at its +0x20. The census gives no reason for the omission. A possible cause is the qword store at +0x1C that straddles into the tag. Not checked.

## (B) Is the mode-0 staging copy ever read?

**Setup.** `0022A0B0` sets `qword[01FD4A78] = 01FE0000`: `lea rax, 01FE4A9F` at `0022A13F`, `and rax, ~0xFFFF` at `0022A14C`, store at `0022A152`. `003A3670` copies it into `02F8F2E0` (`003A370C` load, `003A371A` store).

The staging region is wider than +0x800:
- `003A2D80` and `003A2E30` copy to `[02F8F2E0]`, then toggle bit 0x400 (`003A2DCB`, `003A2F06`). So the copy lands at base+0 or base+0x400.
- Sizes: 0x150 for `0x81` and `0xA0`, 0x1C0 plus two 0x10 control records for `0x97`, and **0xDC0 for `0x8A`**. The staged bytes therefore span **[+0, +0xDC0) or [+0x400, +0x11C0)**, not only [+0, +0x800).

**Census of the pointer and the region:**
- The rip census of `01FD4A78` finds 25 references in 15 functions.
- With the rip base excluded, `01FD4A78`, `02F8F2E0`, `01EF9438` and the static span `01FD8000`–`01FF0000` have **0 image-base-relative operands**.
- `riprefs 1FD8000 1FF0000`: the only reference is the `lea` at `0022A13F`. No code addresses the scratch region except through the pointer.
- `trk addr` over the three pointer globals: no register-based access.

**Control (positive).** The follower finds the sprite request at base+0x800 in all six functions that make it. Each loads `01FD4A78` and runs `add reg, 0x800`:

| function | load / add | first access at +0x800 |
|---|---|---|
| `004490D0` | `004490F1` / `004490FB` | `004492BA` `movdqa [rsi]` W16 +0x800–+0x810; `004492D4` W16 +0x820; `004492E0` W16 +0x810; `004492AD` W8 +0x838 |
| `00449AB0` | `00449ABB` / `00449AC5` | `00449B6C`, `00449B77`, `00449B83`, `00449B8F` `movaps` W16 +0x800–+0x840 |
| `0044BAC0` | `0044BAED` / `0044BAF7` | `0044BC83` `movdqa [rsi]` W16 +0x800; own reads at `0044BE0C` and `0044C08D` (R16 +0x810) |
| `004453D0` | `00445853` / `0044585D` | `0044586F`/`0044587B` RMW byte +0x9F1; indexed bytes from +0x930 |
| `00447020` | `00447545` / `00447553` | `00447569`/`00447575` RMW byte +0x9F1 |
| `00447ED0` | `0044851A` / `00448528` | `00448542`/`0044854E` RMW byte +0x9F1 |

The follower also sees +0 accesses where they exist, for example `003ABE4D` and `003B4376` below. So an absence at +0–+0x800 elsewhere is meaningful.

The pointers these six functions pass to callees are all at least +0x800 (+0x800, +0x810, +0x840, +0x870). The callees `00444340`, `004355D0`, `0026EE00`, `00431D30`, `003AFDD0`, `002F1F40`, `0044B8C0` and `00431830`, followed with `trk reg`, use only non-negative offsets. None of these six functions touches [+0, +0x800).

**Every access that meets [base+0, base+0x800):**

| function | access | mnemonic | width | offset range | R/W | what it is |
|---|---|---|---|---|---|---|
| `003A2D80` | `003A2DA9` call memcpy (`rcx = [02F8F2E0]` at `003A2D95`) | memcpy | n×16 | +0 or +0x400, n×16 bytes | W | the mode-0 stage itself |
| `003A2E30` | `003A2E71` memcpy; control records `003A2E95` w2, `003A2E98` w1, `003A2EA1` w4, `003A2EA6` w8, `003A2EB6` w2, `003A2EBA` w1, `003A2EC3` w4, `003A2ECF` w4, `003A2ECB` w2, `003A2ED2` w1 | mov | 1–8 | dest+n×16 … +0x20 | W | the mode-0 stage (`0x97`) |
| `003ABD50` (r12 = base, `003ABD74`) | `003ABE4D`, `003ABEEB`, `003ABF6E`, `003ABF7A`, `003AC0C8` `mov rax/rcx, [r12]` (r12 += 8 at `003ABF72`) | mov | 8 | +8k, k up to the list terminator | R | its own light-pointer list. Filled by the callee `003ACC10` (`rdx = base`, `003ABE01`) at `003ACF40` and `003AD1CC` (W8), terminated at `003AD402` (W8 0). Sorted by `003AEBC0` (`rcx = base`, `003ABE3B`): R/W at `003AEC06`–`003AEC65`. |
| `003AC110` (r14/r12 = base, `003AC12F`/`003AC1CB`) | `003AC2B3` W8 `[r12]` (+8k), `003AC3C4` W8 terminator (rbp = 0 from `003AC177`); `003AC43E` cmp, `003AC4A7`, `003AC53B`, `003AC54B`, `003AC815` cmp `[r14]` | mov/cmp | 8 | +8k | W then R | its own list, written in the same call before any read; sorted by `003AEBC0` via `003AC42C` |
| `003B4310` (rbx = base, `003B431D`) | `003B4376`, `003B4400` `mov [rbx]` (rbx += 8 at `003B46CB`, count-bounded) | mov | 8 | +8k, k < count | R | pointers written by the callee `003B4A50` (`rdx = base`, `003B4339`) at `003B4B29` W8; count returned in eax |
| `003B4750` | `003B475B` call `003B4A50` (`rdx = base`) → `003B4B29` | mov | 8 | +8k | W only | uses only the returned count |
| `003A3A50` (merge temp, `003A3AA8` `cmovb r8, [01FD4A78]` when hi−lo < 0x199; spilled at `003A3AB2`) | `003A3AF0` W16, `003A3AFB` W16, `003A3B07` W8 (left half, 0x28 per record, up to 205 records ≈ +0x2008) | movups/movsd | 16/8 | +0x28k | W | sort temp for the drain `003A3740` (call at `003A3760`) |
| `003A3A50` | `003A3B58` cmp `[rcx+8]`, `003A3B65` R16, `003A3B7A` R16, `003A3B84` R8, `003A3C08` R16, `003A3C15` R16, `003A3C1F` R8 | cmp/movups/movsd | 4/16/8 | +0x28k | R | reads back only the records it copied in this invocation |
| `00370DF0` → `01EF9438` = base (copy at `00370DF7`; bracketed in `00426090` `00426094`..`0042610D` and `004262E0` `004262E4`..`00426336`) | — | — | — | — | — | hands the base to the list functions below |
| `00370BD0` (r9 = `[01EF9438]`, `00370BFE`) | `00370C0E` W4 +0x1804; `00370C46` W4 +0 (conditional); `00370C58` W4, `00370C5A` W8, `00370C98` W4, `00370C9B` W4, `00370CA2` W4, `00370CA5` W4; `00370C9D` R4 `[rbx]`; `00370C62`/`00370CAC` RW4 +0x1804 | mov/inc | 4/8 | +0, +4+12i … +0x1808 | W, one R | linked list of 12-byte entries; the one read takes the previous entry's index, written earlier in the same call |
| `00370CD0` (`00370D05`/`00370D3C`/`00370D93`) | `00370D12` W4 +0x1804; `00370D46` W4 +0 (conditional); `00370D57`, `00370D5A`, `00370D9A`, `00370DA2`, `00370DAC`, `00370DAF` W; `00370DA5` R4 `[r14]`; `00370D62`/`00370DB6` RW4 | mov/inc | 4/8 | +0 … +0x1808 | W, one R (own entry) | same list |
| `00373540` (`00373582`/`003735C2`/`003735EE`) | `0037358C` R4 +0; `003735C9` R4 +12(i+1); `003735FC` R4 +12i+8; `00373611`, `00373619`, `00373634` R4 `[r9+0xC]`; `00373622` R4 `[r9+8]`; `0037362F` R4 cmp +0; writes `00373615`, `0037362A`, `00373638` | mov/cmp | 4 | +0 … | R/W | walks and unlinks the list that `00370CD0` built. Reached from `0041BEE0`: build at `0041C02A`, reads at `0041C0A6` via `00370E00` (type 2 only). |
| `004FE420` | `004FE467` `add r8, [01FD4A78]` → stored as buffer begin/cursor at `004FE472`/`004FE481` | — | — | begin = base + start×16 | — | backs render command buffers with the scratch |
| (via `004FE420`) buffer `02EBEFC0`/`02EBEFD8` | `003A1D50` (boot): slot 0 at +0 (cap 0x200), slot 1 at +0x2000; `0041E340` via `003A1E10`: +0x2000/+0x3000, then back to +0/+0x2000 | — | — | +0 … +0x2000 | — | `trk deref 2EBEFC0 2EBEFF0`: 255 accesses in 10 functions (`00249FD0`, `00272590`, `00276320`, `002DB080`, `002DC290`, `002DD420`, `002DD4C0`, `002DD550`, `00505570`, `00505E00`), **all W**. The only read found is the submit's tail check below. |
| `0036F360` (from `003A1DB0`, `rcx = begin`) | `0036F372` `mov eax, [r9-0x10]` | mov | 4 | begin + (n−1)×16 | R | the last qword the emitters appended (n > 0; `je` at `0036F362`); then W at `0036F395`/`0036F39C` |
| (via `004FE420`) buffer `02EBB700`/`02EBB718` | `002F5550` → `00466070` (`002F571F`: count 0x100, start 0): +0 and +0x1000 | — | — | +0 … +0x2000 | — | `trk deref 2EBB700 2EBB730`: 4 accesses in `00465FF0` (`0046601A`, `00466021`, `00466025`, `00466029`), all W |
| `0022A0B0`, `003A3670`, `00370DF0` | — | — | — | — | — | pointer plumbing only; no access through the base |

**Conclusion.** No instruction reads the staged packet as packet data.
- Every read that meets [base+0, base+0x800) reads a structure that the same function, or a callee in the same call, wrote first:
  - the light-pointer lists in `003ABD50`, `003AC110` and `003B4310`;
  - the merge-sort temporary in `003A3A50`;
  - the entry list read by `00370BD0`, `00370CD0` and `00373540`;
  - the render-submit buffer's last-tag check at `0036F372`.
- Each of these, and `003B4750` and the command-buffer emitters, **writes over** the staging range.
- `003A3A50`'s temporary overlaps +0 on every merge step that uses the scratch.
  - A merge step runs when hi − lo ≥ 9, that is, 10 or more entries. Smaller ranges take the insertion sort at `003A3C39`.
  - The scratch is the temporary when hi − lo < 0x199. Larger ranges use `[02F8F300]`.
  - The left half is at least 5 records, so the temporary covers at least 0xC8 bytes from +0.
- `003A3A50` runs every drain (`003A3760`), after the walks have staged.
- `003A2D80` and `003A2E30` themselves only write.
- The state word they publish (`02EBA3F8 = 0x100`) is the fossil protocol. Its page's reader census (`CG-1`) finds only guard and spin reads.

**One conditional stale read, not a packet consumer.**
- `0037358C` and `0037362F` read dword [+0]. `00370CD0` writes that dword (`00370D46`) only if some entry has flag `0x100`. `00370BD0`'s `00370C46` is likewise conditional.
- When no entry qualifies, `00373540` reads whatever last occupied base+0..+3 and treats it as a list index.
- Two things are not established: whether `0041BEE0` runs inside the `00426094`–`0042610D` bracket (its caller `00417F40` is reached only through the table at `01EFFB80`), and so whether this stale read can see staged bytes.

**Outside the asked window but inside `0x8A`'s staged span (+0x800–+0x11C0).**
- The sprite-request code merges bitfields into +0x9F1 and +0x9F2 by read-modify-write. For example, `0044586F`/`0044587B` and `00445889`/`004458B8` define bits 0–3 of +0x9F1 and carry bits 4–7 over from whatever was there before.
- The light records at +0x1000 are written by `003ADC40` and its siblings before `003ABF54`/`003AC521` read +0x101C.
- These reads were listed but not classified further.

**Bounds of the method.**
- `trk.py` is a linear pass. It does not follow stack spills; the spills that matter here (`003A3AB2`, `003AC18B`) were followed by hand.
- Pointers passed as parameters are followed only for the callees named above.
- The command-buffer sweep covers loads of the buffer-slot fields: rip, image-base, and `lea`-based with index. It does not cover buffer pointers passed onward as parameters, apart from `003A1DB0` → `0036F360`.
