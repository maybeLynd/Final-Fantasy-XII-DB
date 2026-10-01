# UQ-384 and UQ-385: the GS replay draws through the one D3D11 primitive renderer, and the 19 "caller-less" VU rows are microprograms (SWE2-STRUCT for OPUS, 2026-09-30)

Board claim: OPUS-UQ384-385-0930. Evidence class: **static only**, on the certified image (sha256 `73461D08...`, R0).
Checker: [`uq384_385.py`](uq384_385.py), output [`uq384_385.out`](uq384_385.out): 41 PASS, **FAILS 0**, with nine
positive controls (K1-K9). Nothing was executed. The register and the page boxes are not ticked here.

## Answers in player terms (SWE2-STRUCT for OPUS)

**UQ-384.** Some effects and 2D pieces still use the PS2's drawing language. The game runs those little PS2 programs on
the CPU, collects the PS2 graphics-chip commands they produce, and later replays them. The replay draws through **the
same Direct3D 11 primitive renderer that every other legacy draw command in the game uses**. It is one object, built
once when rendering starts. Nothing is created per effect.

Of the PS2 graphics-chip settings in those packets, the PC port honours:
- the primitive type and its flags;
- texture, texture clamp, texture alpha;
- alpha blending and the alpha/depth tests.

It writes down fog amount, fog colour, the fog-enable bit, the depth-buffer settings and one PRIM flag (FIX), but
**no code anywhere reads them back**. So a PS2 packet that asks for fog or a different depth-buffer mode cannot change
the picture through those settings. Two kinds of vertex are dropped outright:
- vertices sent the PS2 "don't draw yet" way (XYZ3 / XYZF3);
- colours and vertices sent through the generic address-plus-data route.

**UQ-385.** The 19 VU routines that "nobody calls" are not hidden helper routines and not entries reached through some
table. **Each is itself one of the game's VU1 drawing programs.** A drawing command installs it, and the PS2
"start program" command (MSCAL) runs it. No direct call to them exists because programs are never called directly. The
earlier census gave them the "toucher" role without first setting aside the microprograms. Nothing is missing, and
the residue the box named does not exist.

## UQ-384 (a): the object at `[01FC35F8]` (SWE2-STRUCT for OPUS)

The lead from this lane's own [`sd7-sd107-closure-0930`](../sd7-sd107-closure-0930/README.md) S1/S2 was **verified,
not cited**. That record checked the class name of `00D86960` and the single writer, but it did not show that the
value written is an instance of that class. That link is made here.

| step | finding |
|---|---|
| R1 | `01FC35F8` has **one writer**, `0021037B mov [01FC35F8], rdx` in `00210320`. Three censuses agree: the rip census, a byte-level rel32 sweep of all of `.text` (1 writer, 20 readers), and no data pointer, image-base-relative operand or lea into `01FC3480`-`01FC361F`. Seven byte runs that spell such addresses sit inside rip-relative encodings at `002FB250`; they are dismissed by decoding. |
| R2 | `00210320` stores its incoming `rdx` unmodified. Its only caller is `001DB4AC`, and no qword or dword names it. |
| R3 | `001DB3D0` hands its own `rdx` (kept in `rsi`) to every `00210320` call. It is **`GiVmax` slot 1** (vtable `009007E8`, RTTI), named only by the qword `009007F0`, with no direct caller. |
| R4 | `GiVmax` is constructed only by `001DB220`, which is called from `001DB840` (the registrar build) and `001DB7E0` (the effect-element build). |
| R5 | Submission goes `0020E630` -> `001FB810` -> `001A17F0` -> `[[01F7F4D0]+8]` slot 0. `[01F7F4D0]` is the 0x10-byte `GeometryRenderTargetImmediate` built once by `001A17D0`, with `+8` set to the object itself. Neither reader of `01F7F4D0` stores through it. |
| R6-R7 | `001F48B0` wraps the command at `+0x18` of a `GeometryInstanceOrderedObject` (slot 1 `001F49F0`). The render pass drain `0018B100` calls that slot (`0018B187`), and it queues a `0x80`-byte block `{0x2F, 001F4A10, command}` through `005FEA50`. |
| R8 | The block executor `0060A410`: the opcode `0x2F` decodes through its own jump table to the arm `0060A899`. That arm calls `block+8` with a frame whose field 0 is `r14`. `r14` is written once, at `0060A46F`, from `00624670()`. |
| R9 | `00624670` jumps to the magic-static getter `005FD050`, which returns `02CC0410` on both exits. It is the only caller of the constructor `00615840`. |
| R10 | `001F4A10` calls the command's slot 1 with `rdx = frame[0] + 0x18C0` (`00624660`) = **`02CC1CD0`**. |
| R11 | `00615840` constructs `this + 0x18C0` with `006C8750`, which writes `00D86960` (**RTTI `PrimitiveRendererD3D11`, 45 slots**) at `+0` and `00D86AD0` (same class, secondary) at `+8`. The only other lea of `00D86960` is `006C8870`. |
| R12 | `02CC0410` and `01FC35F8` lie in the zero-initialised tail of `.data`. The object is **static storage, constructed in place; there is no allocation**. |
| R13 | So the receiver is `02CC1CD0` = `02CC0410 + 0x18C0`, a `PrimitiveRendererD3D11`, set at the start of each `GiVmax` replay. |

**Which methods the GS buffers replay through (D1-D3).** All 20 rip reads of `01FC35F8` were followed (D1). Two more
receivers are the same object (D2):
- `001DB3D0`'s own `rsi`;
- the PACKED TEXFLUSH arm's `r8`, which is `00210320`'s `rdx` spilled to `[rsp+0x90]`. Its only other writes sit in
  index arms that exit only to the reloading loop tail or to the no-return range-check failure `0020FACE`.

The replay makes 24 dispatches at 17 slots, all inside the 45-slot table (D3):

| slot | method | call sites |
|---:|---|---|
| 0 | `006CA760` | `0020EBED` |
| 1 | `006CB5E0` | `0020EC0C` |
| 2 | `006CA650` | `0020EC22` |
| 3 | `006CB530` | `0020EC45` |
| 5 | `006C8BF0` | `0020EC67` (the page's "slot `+0x28`" draw) |
| 8 | `006CAEB0` | `0020F13C`, `0020F22E` |
| 9 | `006CAE90` | `0020F1BB` |
| 11 | `006CAD90` | `001DB416`, `001DB4ED` |
| 15 | `006CAB80` | `00210178`, `002101EA` |
| 16, 17 | `0060D760` | `002101BB`, `00210016` |
| 19 | `006CAB40` | `0021018D`, `002101FC` |
| 20 | `006CABF0` | `002100DE` |
| 21 | `006CAC00` | `00210049`, `00210075` |
| 36 | `006CAE70` | `00210092` |
| 37 | `006C9B00` | `002104F7`, `0020FD88` (A+D TEXFLUSH), `0020FA0F` (PACKED TEXFLUSH) |
| 39 | `006C9AF0` | `0020F191` |

What each method does is **not read here**. OPUS's [render-context record](../render-context-02cc0410/README.md) types
the setters' fields for slots 6-12, 15, 26 and 32.

## UQ-384 (b): what the GS state handlers store (SWE2-STRUCT for OPUS)

Both jump tables were decoded from the bytes:
- PACKED: map `0020FB28`, offsets `0020FAD4`;
- A+D: map `0020FE14`, offsets `0020FDD8`.

Every arm was walked to its exit (H1-H4). The output lists every descriptor.

**PACKED reaches only descriptors 0-0xF (H1).** The descriptor is `(REGS >> 4k) & 0xF`. The eight arms for
`0x3B`-`0x4F` (TEXA, TEXFLUSH, ALPHA, TEST, ZBUF) exist in the table but cannot be reached from PACKED. Those registers
arrive through A+D. This qualifies the page's §2.1b "cases 12-19" rows; nothing there is struck.

| register | PACKED arm (stores) | A+D arm (stores) |
|---|---|---|
| PRIM | `0020F4C2`: type `01F83562`; IIP `01FC3600`, TME `01F8357C`, FGE `01F8357D`, ABE `01F8357E`, FST `01F8357F`, CTXT `01FC3601`, FIX `01FC3602` (bytes; bit 7 AA1 dropped); then `0020FBA0`, and phase `01F83574` and vertex count `01F83568` := 0 | `0020FD07`: `0020FE70` with the data's low dword (the same split) |
| RGBAQ | `0020F55F`: R, G, B, A bytes reversed into `01FC361F`..`01FC361C`; `(int)` of the last Q `01E027B0` into `01FC3618` | ignored |
| ST | `0020F5AA`: S/Q `01FCB604`, T/Q `01FCB600`, Q `01E027B0` (floats) | ignored |
| UV | `0020F61E`: 14-bit U `01FCB60C`, V `01FCB608` as floats | ignored |
| XYZF2 / XYZ2 | `0020F66B` / `0020F6B5`: phase, vertex count (XYZF2 also zeroes `01F83563`), then the vertex path `0020F6F6` (page §2.1b items 2-3) | ignored |
| TEX0_1 / _2 | `01FC3588` / `01FC3590` (qword) | the same |
| CLAMP_1 / _2 | `01FC35B8` / `01FC35C0` | the same |
| FOG | `0020F9C7`: `(int)(F x 0.0625)` byte into `01F83563` | ignored |
| A+D | `0020F9F0` -> `0020FCA0`: the data `01FC3608`, the register `01FC3610`; outside 1-5 it flushes and sets `01FC3603` | - |
| TEXA | unreachable | `01E027B8` |
| FOGCOL | ignored | bytes 0-2 into `01FC3604`/`05`/`06` |
| TEXFLUSH | unreachable | device slot 37 (`[01FC35F8]`) |
| ALPHA_1 / _2 | unreachable | `01FC35D8` / `01FC35E0` |
| TEST_1 / _2 | unreachable | `01FC35C8` / `01FC35D0` |
| ZBUF_1 / _2 | unreachable | `01FC35E8` / `01FC35F0` |
| XYZF3, XYZ3, NOP and all others | ignored (`0020FA6F`) | ignored (`0020FDD2`) |

**Who reads what was stored (H6, control K4).** The census covers rip operands of any width overlapping the value, a
byte-level sweep of `.text`, image-base-relative operands (control K9) and data pointers.
- Read: TEX0 by `0020EB60` and `0020ED30`; CLAMP by `0020ED30` and `0020FF10`; TEST and ALPHA by `0020FF10`; TEXA by
  `0020ED30` (one byte); the PRIM bytes by `0020EB60`, `0020ED30`, `0020FF10` and `0020EA50`; RGBAQ, ST and UV by
  `0020EA50`.
- **Never read: FGE `01F8357D`, FIX `01FC3602`, FOG `01F83563`, FOGCOL `01FC3604`-`06`, `(int)Q` `01FC3618`, ZBUF_1
  `01FC35E8`, ZBUF_2 `01FC35F0`.**

## UQ-385: the 19 (SWE2-STRUCT for OPUS)

| step | finding |
|---|---|
| V1 | The list was not on the page, so it was rebuilt by the census's own method (`vu1_census.json` touchers x the E8/E9 edge index, as `Tools/work/SWE2-FRONTIER/vu1_region_tsv.py`). 54 = 33 + 2 + **19**, which matches §2.6. The 19: `004804A0 00485790 00488340 0048AF70 0048D4B0 0048F8C0 004958A0 00499A20 0049B9E0 0049D540 004A0090 004A1E30 004A33B0 004A4410 004A8B00 004AAFC0 004B0230 004C0EA0 004C37C0`. |
| V2 | All 19 are among UQ-213's 57 microprograms. 9 were already in the registrar list the census used; 10 were added by UQ-213 through `003A33B0` / `003A2F70`. |
| V3 | No direct call / jmp / jcc of any width targets any of them (byte-level rel32 and rel8 sweeps; controls K5, K7). Each is preceded by `0xCC`, so none is entered by fall-through. 11 byte runs spell a rel32 to one of them, but none decodes as an instruction that uses it. |
| V4 | No qword holds any of the 19, and no base-relocated slot does (K8). Every 32-bit match is metadata: each one's own `.pdata` BeginAddress; chained-unwind parent links of their fragments (8 of the 19); the handler data of `005A5790` (an RVA `0x485790`); two `.pdata` RVAs of `005A5790` and `005C0090`; and bytes inside `00315EC5`. |
| V5 | Each address is formed only by rip `lea` (48 sites; byte sweep = rip census). Each lea feeds the program argument of a registrar call with no rewrite in between: `003A34D0` x17, `003A33B0` x16, `003A35E0` x8, `003A2F70` x7. Control K6 rejects a non-registrar lea. |
| V6 | Route: registrar -> `001DB840` arg 4 -> MPG chunk `+8` (`01DFD040`, sole writer) -> the MPG case copies the qword into `02068E30[addr]` (touched only by `0022C970`) -> MSCAL `call [rax + r9*8]` (`0022CB1E`). |
| V7 | The MPG arm has no loop and consumes exactly 4 + 8 bytes, so **no VU microcode is embedded** in which a JAL / JR could be decoded. A compiled JAL would be a direct call, and V3 found none. |
| V8 | **0 JAL/JR sub-program targets, 0 data-referenced entries; all 19 are "neither": registered VU1 microprogram entries started by MSCAL.** |
| V9 | The region table's real sub-programs (21 rows) are disjoint from the 19 and every one has a direct caller. |

## Limits (SWE2-STRUCT for OPUS)

- **R5-R10 follow the established Gi execute route.** A `call [reg+8]` on a `GiVmax` elsewhere cannot be excluded
  syntactically, because slot-1 dispatches are everywhere. The supports are:
  - slot 1 is named by one qword only;
  - the handler object's `+8` has no other writer through its two readers;
  - all 24 replay dispatches land in `PrimitiveRendererD3D11`'s table.
- **The never-read results (H6) are a static reference census.** A pointer computed by arithmetic from an unrelated
  base cannot be excluded statically. The nearest bases are:
  - the vertex array `01FC3620`, indexed upward;
  - the texture table `01F83580`. Its writer `00210570` takes a signed 16-bit index (`movsx` after `cmp cx, 0x4000`),
    and how its callers bound that index was not read.
- **Not read:** what the 17 device methods do; what `0020ED30` / `0020FF10` do with the values they read.
- **V1's inputs are not in git:** `vu1_census.json`, `vu1_registered_programs.json` and `edges.tsv` live in the
  gitignored `Tools/work`. The rebuild reproduces the page's 54/33/19/2 exactly; V2-V9 do not depend on them.
- Static only. Nothing here shows a path runs or how often.

## Page edits and routed items (SWE2-STRUCT for OPUS)

- The page has dated answer notes on its UQ-384 and UQ-385 boxes in §7. **No box was ticked and nothing was
  struck**, so no consumer check is needed. The page was clean in `git status` before the edit.
- **Routed to the page owner (not edited, outside the two boxes):**
  - §2.6's line "19 have no E8/E9 caller - consistent with VU `JAL`/`JR` sub-programs or install paths not yet found
    (§7)" is superseded by V8;
  - the box above UQ-385 still says "Still open";
  - §2.1b's "Not read: ... the class behind `[01FC35F8]`, and what the individual state handlers store" and item 5's
    "The object's class is not identified here" are answered here;
  - the §2.1b table's cases 12-19 are PACKED-unreachable (H1).
- **Routed to FRONTIER:** in `members/vu1-region-functions.tsv`, the 9 registrar rows among the 19 carry the evidence
  "registrar census; ... not installed", which contradicts itself. The toucher role on all 19 should not imply an
  uninstalled helper. UQ-213 already routed the other 10.

## For SWE2-DATA: proposed register row text (pipe-free, not applied) (SWE2-STRUCT for OPUS)

**UQ-384:** ANSWERED 2026-09-30 (SWE2-STRUCT for OPUS), static. `[01FC35F8]` holds `02CC1CD0` = `02CC0410` + `0x18C0`,
the embedded PrimitiveRendererD3D11 (vtable `00D86960`, RTTI, 45 slots). It is written only at `0021037B`, from GiVmax
slot 1's rdx. The Gi execute callback `001F4A10` supplies that rdx as the render context's `+0x18C0`. The object is
static storage built in place by `00615840` and `006C8750`; nothing is allocated. The replay calls 17 of its slots from
24 sites. Handlers: PACKED reaches 12 arms (PRIM split into bit bytes, RGBAQ bytes plus int Q, ST as S/Q, T/Q and Q, UV
floats, XYZF2 and XYZ2, TEX0, CLAMP, FOG, A+D); its arms for `0x3B`-`0x4F` are unreachable. A+D reaches 14 (PRIM, TEX0,
CLAMP, TEXA, FOGCOL, TEXFLUSH as device slot 37, ALPHA, TEST, ZBUF) and ignores RGBAQ, ST, UV, XYZ and FOG. FGE, FIX,
FOG, FOGCOL, int Q and ZBUF_1/ZBUF_2 are stored and never read. [record](README.md),
`uq384_385.py` FAILS 0.

**UQ-385:** ANSWERED 2026-09-30 (SWE2-STRUCT for OPUS), static. None of the 19 is a JAL or JR sub-program target, and
none is data-referenced. All 19 are VU1 microprogram entries from UQ-213's 57: 9 were already rowed registrar-path and
10 were added by UQ-213. Each address is formed only by rip lea as a registrar's program argument (48 sites), and MSCAL
starts it through the program table `02068E30`. No VU microcode is embedded, because MPG carries one x64 pointer. The
only data matches are `.pdata`, unwind and handler metadata. [record](README.md),
`uq384_385.py` FAILS 0.

run: uq384_385.py at d5888bccf (FAILS 0)
