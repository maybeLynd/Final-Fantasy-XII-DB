> Drafted by a Claude Opus 5.5 subagent pass under FABLE, 2026-09-27. Its scratch instruments are not published; `uq213_programs.py` re-derives the population and the control tags from the bytes.

# UQ-213 - what each VU1 microprogram draws: notes

Static read of `FFXII_TZA.exe` (image base `0x120000`), 2026-09-27. Nothing was executed.
Table: `uq213_programs.tsv` (57 rows). Instruments (scratch, not published; `uq213_programs.py` re-derives the population):
- `uq213_raw.py`: raw E8/E9/0F8x index of the registrars, `001DB840`, `008631E0` and `001DB7E0`.
- `uq213_sites.py` -> `uq213_sites.txt`: the program argument at every registrar site, by backward register slice.
- `uq213_addrtaken.py`: every place any VU-touching function's address is formed.
- `uq213_emu.py` / `uq213_tags.py` -> `uq213_tags.tsv`: a constant-propagating replay of every template builder, including fill loops, `memset`, `008631D0` and `008631E0`, then a GIF-tag decoder over the replayed bytes.
- `uq213_objrefs.py` -> `uq213_objrefs.txt`: who references each template object, in both rip-relative and image-base-relative form.
- `uq213_prog.py`: own-tag constants in each program, EOP stamps and kicks.
- `uq213_vi.py`: a linear VI-register dataflow. For each kick or leaf call it reports which VU cell supplies the tag.
- `uq213_join.py`: the per-program join. `uq213_write.py` writes the table.

## 1. Population: 57, not 47

**The four registrars take the program as the page says. Checked from their bodies:**
- `003A34D0`: `mov rsi, r9` (`003A3500`), then `mov r9, rsi` (`003A357A`), then `call 001DB840` (`003A35B9`).
- `003A33B0`: `003A33E1`, then `003A3457`, then `003A34A4`.
- `003A35E0`: `mov rdi, r8` (`003A35FD`), then `mov r9, rdi` (`003A3616`), then `003A363D`.
- `003A2F70`: `003A2F8D`, then `003A2FA6`, then `003A2FDE`.

So in every case the program reaches `001DB840` as its fourth argument. `001DB840` has exactly these four callers.

**Raw call index.** It agrees with the instruction cache at every site: 104 sites in 49 functions.

| registrar | sites |
|---|---:|
| `003A34D0` | 45 |
| `003A35E0` | 27 |
| `003A33B0` | 22 |
| `003A2F70` | 10 |

None of the four has its address taken anywhere: no `lea`, no qword pointer.

**The three sources.**
- **(a) Registrars.** 44 distinct programs; every site's `r9` or `r8` is a `lea [rip]` of the program. Split by path:
  - through `003A34D0` / `003A35E0`: 29;
  - through `003A33B0` / `003A2F70`: 15, disjoint from the 29.
- **(b) Templates.** The `mpg_program` column of `vif1-packet-templates.tsv` has 35 distinct programs.
- **(c) Region table.** 45 rows whose role is `microprogram(...)`: 34 template and 28 registrar, overlapping.
- **Union: 57.** (a) and (b) share 22 programs, so (a) ∪ (b) = 57. All 45 rows of (c) are inside it.

**Where the page's 47 comes from.** It is (b) ∪ (the 29 registered through `003A34D0` / `003A35E0`), which share 17, so 29 + 35 − 17 = 47. The difference is the ten programs registered only through `003A33B0` / `003A2F70`:
- `00499A20`, `0049B9E0`, `0049D540`, `004A0090`, `004A1E30`, `004A33B0`, `004A4410`, `004A8B00`, `004AAFC0`, `004B0230`;
- effect types `0x8C`, `0x8E`, `0x8F`, `0x90`, `0x92`, `0x95`.

**Where the region table's 45 differs.**
- `002F0280` and `0053F490` lie outside `0x470000`–`0x500000`.
- The same ten are rowed `VU-helper(VU-state-toucher) ... not installed`.

**Independent control.** 107 functions touch VU state (a rip operand into `02064B00`–`02088E50`). Of these, exactly 57 have their address formed anywhere in the image, and they are exactly the 57 above.
- Every such formation is the registrar argument or `008631E0`'s `rdx`.
- There are no image-base-relative forms, no immediates, and no qword pointers to any of them.

## 2. The tag-finder control

The finder replays each builder's stores into a byte image, then accepts a quadword when all of these hold:
- reserved bits 16–45 are zero;
- FLG is PACKED;
- if PRE = 0, PRIM is 0;
- if PRE = 1, the PRIM type is 0–6;
- NREG is 1–15, and each of the first NREG nibbles names a real descriptor;
- the quadword sits at a cell of an UNPACK payload, or of a DIRECT payload.

| control | result |
|---|---|
| `0x68`, template `02AEB610` (`004E2930`) | cell 0: `TRIANGLE_STRIP` PRIM `0x05C` IIP+TME+ABE, NREG 6, `ST,RGBAQ,XYZF2` x2. **Pass.** |
| `0x69`, template `02AEB0F0` (`004DCA00`) | the same tag, field for field. **Pass.** |
| `0xA3`, template `02AEA270` (`004DC6B0`) | cell 0: `LINE` PRIM `0x049` IIP+ABE, NREG 4, `RGBAQ,XYZF2` x2. **Pass.** |
| `0xA9`, template `02AE8CF0` (`004795D0`) | cell 0 at +0x20: PRIM `0x05C` (0x5C), NREG 3, `ST,RGBAQ,XYZF2`, from stores `0047960B`/`00479613`/`0047961A`. **Pass.** |
| bone trail, `005409C0` | cell 0: `0x05C`, NREG 6, as on the-bone-trails 5e. **Pass.** |

**The first version failed the `0x68` and `0x69` controls.** It also required REGS nibbles above NREG to be zero. But the authored REGS upper dword there is `0x00008000` (`004E2984`, `+0x2C`), so nibble 11 is 8. The GS ignores nibbles above NREG, so the rule was dropped. That relaxation is the only change made after seeing the controls.

**Against the page's `vif1-gif-tags.tsv`.**
- All 75 of its tags are recovered.
- Four differ only in cell numbering. The page numbers within the payload; this table uses the VU address (UNPACK `addr` + index):

  | builder | page cell | VU address |
  |---|---:|---:|
  | `00479450` | 7 | 9 |
  | `004DA650` | 15 | 45 |
  | `004DC8F0` | 3 | 131 |
  | `004E2CD0` | 3 | 43 |

- The finder finds 123 tag cells in 61 builders, against the page's 75 in 45: 59 PRE = 1 vertex tags (page 36), 61 A+D, 2 PRE = 0 vertex tags and one NOP-only quadword. Why it finds more:
  - it runs fill loops;
  - it replays all 77 rows, including the two `mpg-solo` builders.
- One accepted quadword, `004A1C10` cell 23 (PRE = 0, NREG 1, NOP), is treated as data, not as a tag.

**The own-tag scan is sensitive, and the programs carry no tag of their own.**
- On the builders `004E2930`, `004795D0`, `004DC6B0`, `004C8080` and `004802F0`, it finds every tag high-dword immediate (for example `0x602E4000`, `0x302E4000`, `0x4024C000`).
- Its base rate is 3 of 300 random functions of 300–3000 B outside the region.
- **It finds 0 in the 57 programs.**

## 3. How a program gets its GIF tag (the basis of the "read" rows)

No program holds a tag constant. Each one copies a VU cell that its packet's UNPACK uploaded from a template. It then stamps NLOOP|EOP into the first dword and hands the cell to the callback. There are two shapes:

1. **Inline copy.**
   - Typical programs: the `LINE`, `TEX0_1`-quad and `0x8C`–`0x95` programs.
   - The program loads the template's tag cell, and the A+D cells before it, as 16-byte cells indexed from the VI word `02064B0C`. It copies them to an output buffer (for example cells 200/612 or 250–252/637–639), stamps the count and kicks.
   - Example: `004804A0` stamps cell 17 at `00480898` and copies it to cells 200 and 612 at `004808B5` / `004808BD`.
2. **Leaf.**
   - The XGKICK-shaped leaves (`004C4C40`, `004DF360`, `004E78A0`, `004ECB70`, `00479370`, `004DB270`, `004D7B10`, `004CF3B0`, `004C7F00`, and `002EFE70`, which is outside the region) copy `cell[word 02064DD0]` into the kick cell's bytes +4..+F.
   - The program sets `02064DD0` to `word[02064B0C] + K` before calling.
   - **Every leaf program kicks its template's A+D register packet first,** with `rcx` = that cell, and then emits vertices with K = the vertex tag's cell. `uq213_vi.py` reports this for all of them:
     - K = 0 everywhere except `004ECC50` (K = 8, matching its tag at cell 8);
     - `004C8320` uses K = 0, 1, 2 and 3: its four tags.

**Premises checked.**
- **`02064B0C` is never written.** It has 470 references, all `movsx`, `movzx` or `cmp`. No wider store reaches it; the highest is a dword at `02064B08`. There are no image-base-relative references. It lies in the `.data` virtual tail, so it is 0.
- **None of the 47 distinct UNPACK immediates in the builders sets the TOPS flag** (bit 15). So template cell numbers are VU addresses.
- **No code outside a tag's builder stores rip-relative into any tag quadword.** The only foreign references are `lea`s by the pair builders `00544D30`, `005473A0`, `0054B3E0`, `00547A00`, `005480E0`, `0054AA90`, `0054BE70` and `0054D740`, which take the payload's address to copy it. A register-based store into the arena copy is **not** excluded. Nor is a walk overwriting the A+D placeholder values (CLAMP_1, TEX0_1, ALPHA_1 and TEST_1 are 0 in most templates).

## 4. Counts by primitive (57 programs, by the vertex primitive each one's tag names)

| primitive (PRIM) | programs |
|---|---:|
| `TRIANGLE_STRIP` `0x05C` (IIP+TME+ABE), NREG 3/6/10/12 | 26 (one of them, `004E7D90`, partial) |
| `TRIANGLE_STRIP` `0x054` (TME+ABE, flat), textured quad per loop | 5 (`0047C360`, `00482860`, `0048AF70`, `0048D4B0`, `0048F8C0`) |
| `LINE` `0x049` (IIP+ABE) | 6 (five with NLOOP 240 authored, plus `004DB350`) |
| `LINE` `0x059` (IIP+TME+ABE) | 2 (`004EBE80`, `004ECC50`) |
| `LINE_STRIP` `0x04A` (IIP+ABE) | 2 (`004B9EA0`, `004BC320`) |
| `POINT` `0x040` (ABE) | 5 (`004C2160`, `004C37C0`, `004C4D20`, `004C5DF0`, `004C6DE0`) |
| `TRIANGLE_FAN` `0x05D` (IIP+TME+ABE) | 4 (`004DA8A0` through an A+D PRIM write; `004758E0`, `0047A9C0` and `004ADD10` partial) |
| `TRIANGLE_FAN` `0x045` (ABE) | 1 (`004CF490`) |
| `SPRITE` `0x056` (TME+ABE) | 1 (`002F0280`) |
| mixed | 2 (`004B1190`: LINE_STRIP `0x04A` + TRIANGLE_STRIP `0x054`; `004C8320`: TRIANGLE `0x043`/`0x053` + TRIANGLE_STRIP `0x044`/`0x054`) |
| no GS output of their own | 2 (`004DF440`, `004DCC00`: the first program of the `0x68` / `0x69` packets) |
| tag route not traced | 1 (`004C0EA0`: its caller's template holds TRIANGLE_STRIP `0x054`) |

**A few regularities.**
- **ABE is set in every PRE = 1 tag, and FGE, AA1, FST and CTXT are clear in all of them.**
- **Five tags write PRIM through A+D, not through PRE:**
  - `00476C80`, cells 11/26/41/56: PRIM = `0x5D`, loop-built;
  - `004DA650`, cell 45: PRIM = `0x5D`.

## 5. Partial rows (5), and why

| program | why partial |
|---|---|
| `004758E0` | Kicks a chain that starts with the template's A+D block, which writes PRIM `0x5D`. The route of the PRE = 0 vertex tag (cell 1) into that chain was not traced. |
| `0047A9C0` | Same chain shape. The TRIANGLE_FAN tag at cell 0 is loaded (`0047AA9D`), but its route to the kick (`0047BA9A`) was not traced. |
| `004ADD10` | VI state lives in stack locals. The tag cell is a VU-memory word (`004AF20C`) + 17, so the tag is FAN (cell 17) or STRIP (cell 16). |
| `004C0EA0` | Its VI-like state lives outside `02064Bxx`, and the kick cell is a clamped data word. The TRIANGLE_STRIP `0x054` is only its caller's template tag. |
| `004E7D90` | Read for the `0x6B` path (template `02AECAD0`). For `0x67`, the payload `00460170` passes through `003A33B0` was not traced to a template. |

## 6. What the page (and adjacent records) state that the bytes contradict

1. **The population count** (`the-vif1-vu1-layer.md` 2.3 "Together: 47 distinct microprograms", and the UQ-213 box). The image uses **57**. The ten `003A33B0` / `003A2F70` programs are missing (section 1).
2. **"76 call sites register 29 programs"** (2.3). `003A34D0` and `003A35E0` have **72** call sites (45 + 27; raw index = instruction cache), and they register 29 programs. All four registrars together have 104 sites and 44 programs.
3. **"The remaining two MPG builders (004A8860, 004C3610) are never hub-called"** (2.4a). **The hubs tail-jump to them:**
   - `0037E0E3 jmp 004A8860`, with `rcx = 02AE1EF0` set at `0037E0D8`;
   - `0037E33F jmp 004C3610`, with `rcx = 02AEAFC0` set at `0037E334`.
   - Run-time readers of those objects: `004595C0` (type `0x91`, 45 rip refs) and `00451530` (25).
4. **"00476C80 ... nothing tag-shaped"** (2.4d, the eight read by hand). **The fill loop `00476D01`–`00476DFF` (4 iterations, stride 0xF0) writes an A+D tag** at cells 11/26/41/56:
   - the tag is NLOOP 5, NREG 1, A+D (`00476D7B`, `00476D85`, `00476D8F`);
   - its fifth pair is **PRIM = 0x5D** (data `00476DE2`, address `rdx = 0` at `00476DED`).
   - Before the loop, `00476CF2` / `00476CF9` write a PRE = 0, NREG 3 `ST,RGBAQ,XYZF2` tag at cell 1.
   - The page's table counts 16 stores for this builder. The body has 56 `mov` stores to memory (immediate or register), 35 of them inside the loop.
5. **"45 of the 74 builders ... carry at least one tag"** (2.4c) undercounts. Sixteen more builders carry tags:
   - `00476C80`, `004791E0`, `004795D0`, `0047A800`, `0047BAF0`, `0049B850`, `0049FE90`, `004A1C10`, `004A3150`, `004A4220`, `004A6490`, `004A8860`, `004AD840`, `004C3610`, `004D0E80`, `004D3FE0`.
   - Among them is `004795D0`, whose `0x5C` tag the UQ-204 residue record decoded by hand.
   - Builders already on the page also have further vertex tags. Examples: `0047E140` cell 22, `00485390` cell 23, `0048AB40` / `0048CE70` / `00492D40` cell 23, `0048F410` cell 24, `004B8F20` cell 47, `004C2040` cell 187, `004C8080` cells 2–3.
6. **The 2.4c element-type table is wrong on two rows:**
   - **`'j'` `0x6A` "none found".** The tag is in the co-template `02AE9140` (builder `004DA460`, already in the page's own `vif1-gif-tags.tsv`: cell 0, `0x05C`, NREG 6). `004D7BF0` uses it through leaf `004D7B10` with `02064DD0 = 0` (`004DA285`).
   - **`0xA6` / `0xA8` "ten vertices under whatever PRIM the GS already holds".** `004DA8A0` itself kicks cell 45 first (`004DA8F5`), which is `02AE9D50`'s A+D block ending in PRIM = `0x5D`. The ten PRE = 0 vertices are therefore a TRIANGLE_FAN, IIP+TME+ABE.
7. **Region table and 2.6.** The ten programs of item 1 are rowed "VU-state-toucher, not installed". 2.6's "`004A6780` is called by six sibling touchers (`00499A20`, `0049B9E0`, `0049D540`, `004A0090`, `004A33B0`, `004A4410`)" names six installed microprograms. `004A6780` is a helper those programs call.
8. **UQ-204 table** (`uq204-element-type-emits.tsv`). Types `0x80`, `0x82`, `0x83`, `0x86` and `0x87` each register **two** programs, but their rows name one. The walk's early helper registers the second, a POINT program:

   | type | walk | call | early helper | POINT program |
   |---|---|---|---|---|
   | `0x80` | `0044CC50` | `0044CCB7` | `0044D080` | `004C6DE0` |
   | `0x82` | `0044DD00` | `0044DD67` | `0044E160` | `004C5DF0` |
   | `0x83` | `0044E530` | `0044E597` | `0044E980` | `004C4D20` |
   | `0x86` | `00450550` | `004505B7` | `00450940` | `004C37C0` |
   | `0x87` | `00451180` | `004511E7` | `00451530` | `004C2160` |

9. **"Not read: what any single microprogram draws"** (page header) and **2.4b's open "whether the two programs a type installs run in one MSCALF each or one of them is a fallback".**
   - For `0x68` and `0x69`, the first program (`004DF440`, `004DCC00`) contains **no callback call, no leaf call and no indirect jump**, so it emits nothing itself. The second (`004E0F70`, `004DDDF0`) emits.
   - Each template carries its own MSCALF 0: `02AEB610` +0x1D0, `02AEB820` +0x90, `02AEB0F0` +0x170 and `02AEB2A0` +0x90. So they read as two runs. This rests on the template command streams, not on the run-time arena copy, which was not replayed.

No contradiction was found with the-bone-trails 5d/5e. The replayed `005409C0` gives the same tag, and the A+D block `0053F490` kicks first is cell 64: CLAMP_1, TEX0_1, ALPHA_1 = `0x48`, TEST_1 = `0x53001`.

## 7. Feature coverage

**53 of the 57 programs have an effect element type** (all but `002F0280`, `00478280`, `0047A9C0` and `0053F490`).

**Non-effect users** (6 programs; `004758E0` and `00479650` have both):

| user | program |
|---|---|
| queued screen-effect descriptor kinds 2 (`003745C0`) and 6 (`00374280`) | `004758E0` |
| screen-effect kind 5 (`00375D90`) | `00478280` |
| screen-effect kind 7 (`00374E30`) | `00479650` |
| screen-effect kind 0x0D (`00375280`) | `0047A9C0` |
| six VFX display layers (`0036F550`, `0036F9F0`) | `004758E0` |
| character render record authored packet (`003E6680` -> `0051CDE0` -> `00540C70`) | `002F0280` |
| bone trails (`0051BC70`) | `0053F490` |

The screen-effect kinds are dispatched by `00375500`.

**One draw path is never submitted on PC.** `00479650`'s `0xA9` use is the raw arena packet that the UQ-204 record says the PC build never submits.
