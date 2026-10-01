> Drafted by a Claude Opus 5.5 subagent pass under FABLE, 2026-09-27. FABLE re-read the draw route (control M4) and six of the thirteen contradictions below (1, 2, 3, 4, 6, 9) against the bytes; the other seven are the reader's, routed as such.

# BB-1: what CharacterRenderObject renders, per method (static, 2026-09-27)

Exe sha256 73461d08...21f8. Per-slot rows are in `bb1-methods.tsv`. The drafting scripts were scratch and are not published; `bb1_methods.py` is the control.

## Verdict counts (31 slots)

| verdict | n | slots |
|---|---:|---|
| draws | 0 | none |
| uploads (CPU-side shader parameters) | 8 | 8, 10, 12, 14, 19, 20, 24, 30 |
| state only | 14 | 1, 6, 7, 9, 11, 13, 15, 16, 18, 21, 22, 23, 25, 26 |
| bookkeeping | 9 | 0, 2, 3, 4, 5, 17, 27, 28, 29 |

Confidence: 27 read, 4 partial (2, 7, 11, 26).

## The walker and its control

`walk()` follows direct `call`, and `jmp`/`jcc` that leave the body, to depth 4. It uses linear disassembly of each `functions.tsv` body.

**Control:** from `002F4020` the walker reaches every function in the render-reaching set:
- `0039D5A0` through `002F4020 -[002F4146]-> 004427D0 -[004428C3]-> 0039C4C0 -[0039C52B]-> 0039D5A0`;
- `0020E680` through `0044CC50 -[0044CFEE]-> 003A34D0 -[003A3564]-> 0020E680`;
- and `003A3010`, `003A31A0`, `003A33B0`, `003A35E0`, `00540C20`, `00540DB0`, `0039D6C0`, `0039D970`, `0020E630`.

*Correction to the brief:* `00442550` does **not** reach `0039D5A0`. Its only caller is `0039C4C0` (`0039C52B`), which only `004427D0` calls. `00442550` reaches `0039D970`, `0020E680` and `0020E630` (`00442550 -[004425E8]-> 0039C550 -[0039C5A5]-> 0039D970 -[0039D9A8]-> 0020E680`).

**Result:** none of the 31 slots reaches any function in that set within depth 4. The draw method `001F5D70` does not reach it either (99 functions reached).

The union of one-hop direct callees across the 31 slots is **46**, which matches the page. The only rip-slot call is `008C2CC8` = `_fdtest`.

## What puts a character on screen

The draw is a **non-virtual** method, `001F5D70`. It goes to the **Phyre renderer's own command ring**, not to the Gi draw list. It is reached from a per-frame list that slot 1 fills:

1. **Enqueue, per frame.** The render record's update `0053AB50` calls slot 1 through wrapper `0017F0B0` (`0053AE1A` / `0053AE2C`). Slot 1 `001F89B0` push_backs `this+0x28`, a pooled `CharacterOrderedObject` (vtable `00903940`, `+8` = this), into the list `[01F7F5E0]` via `0018AFF0`.
2. **Frame render.** `GameApplication` slot 8 `0017D090` tail-jumps to `00187950` (`0017D0B0`). `00187950` walks the list three ways:
   - `0018B100` at `00187D05` (partition 0..`+0x24`);
   - `0018B100` at `00188128` (the rest);
   - with byte `+0xC34` = 1 (`00187D20`): `001F0AD0` -> `001F06D0` -> `0018B1B0` (`001F07C7`, mask 6).
   Each walk calls the element's vtable `+8` (`0018B187`, `0018B26D`, `0018B2F9`), which is `00215320`: `mov rcx,[rcx+8]; jmp 001F5D70`. The list is emptied at `00188204` (`0018B040`).
3. **Draw.** `001F5D70` does the following:
   - It reads the latch late (`001F5E05`).
   - It skips the object when `+0x4A8` < 0.75 (`001F5E2D`).
   - **Shadow pass** (`+0xC34` set; `+0x4B6` required, `001F5E18`): it sets the renderer's default pass to `ShadowRender` or `ShadowRenderWithRef` (`001F617C` / `001F6185`), then calls `0060B980` per mesh instance with mode 2.
   - **Otherwise:** it calls `001FAD50` per record (`001F6315`) and slot 30 through the vtable (`001F6347`). It then calls `0060B980` per mesh instance with mode 3 (`AlphaModeRender` default, `001F64A8` / `001F64EB`), or modes 4 and 5 (`ChrOpaque` default `01F2D980`, `001F666A`; `001F66BA`, `001F675A`), and restores mode 1.
   - The renderer is `[[01F7F598]+8]` (`001F5DEB`).
4. **Phyre per-segment submit, `0060B980`.** It reads the pass-override array that slot 16 wrote into the mesh instance (`0060BB65`, `0060BB8F`, `0060BBA4`, `0060BBB6`, `0060BBBF`, `0060BBD2`) to choose each segment's pass. It resolves the segment's material through `0060CD10` (`0060BC34`) and reads the material's `+8`, the parameter data block the slots write (`0060BE5E`). It passes that block to `005FECF0` (`0060BF2C`), which calls `00602A40` (`005FED6F`). `00602A40` bump-allocates in the renderer ring (`+0x28`..`+0x38`) and **memcpys the whole data block** (`00602A9A`). Finally `0060C020` (`0060BF9E`) appends a `0x80`-byte draw record (tag 1/2) to the ring at renderer `+0x50`/`+0x58`/`+0x60` (`0060C220`-`0060C24C`).

**Not followed:** how that ring reaches D3D11. It is not the Gi double buffer: `RenderCommandBuffer_ConfigureBackingRange` `004FE420` configures a `{base, cursor, size}` at `+0`/`+8`/`+0x10`, a different layout, called from `RenderCommand_*` initialisers.

## What each group of slots contributes

- **Pass selection: slot 16.** Per mesh segment it writes `{index, mode, pass A, pass B}`:
  - pass A: `ChrOpaque`, `ChrOpaquePT`, `ChrOpaqueClip*` and the Reflection/Refract variants, or `NearFade*` below +0x4A8 0.75;
  - pass B: `AlphaMode*`.
  `0060E960` copies these into `[mi+0x90]`, and `0060B980` consumes them. Slot 16 also drives slots 14/19/20/10/13 per element.
- **Shader parameters into each record's material data block `[[record+0]+8]`:**

  | slot | parameters |
  |---|---|
  | 8 | lights (`lichtAmbient`, `lichtDir1-6`, `lichtColor1-6`, `sunIndex`) |
  | 10 | `AlphaThreshold` |
  | 12 | `clutBank` |
  | 14 | `PTAlphaThreshold` |
  | 19 | textures, palette, normal/specular, cube and irradiance maps, texture animation, fresnel, camera light, `eTp` |
  | 20 | `RefSampler` |
  | 24 | refraction |
  | 30 | `iDebugMode`, `mSpecialShadowFlag`, `m_chrObjHeight`, `m_chrObjFlyingHeight`, `g_txShadow`, `g_txChrAlpha` |

  The draw copies the block into the ring at `00602A9A`. The link from the block to the draw is established only for the material resolved through `[mi+0x20]` (`0060CD10`), which is the same array slot 2 binds (`001F7092`, binder owner store `001F8452`).
- **Staged, then written by another method:**
  - slot 13's transform banks and slot 9's fog vector: `001FAD50` writes them, called from `001F5D70`;
  - slots 22/23: through `001FB310` and `001F0850`, then slot 30;
  - slot 25: into slot 30;
  - slots 6/7 position: into `001ABF50`, then probe ids/weights, then slot 19;
  - slots 15/11/21/20 flags: read by slot 16 or `001F5D70`;
  - slots 17/18: the texture-animation vector read by slot 19.
- **Transforms into the mesh instances (reader not traced):**
  - slot 7: world matrix, `[mi+8]`;
  - slot 26: numerically named node palette, `[mi+0x18]`.

## Page and contract statements the bytes contradict

1. **Section 3, slot 1: "releases the +0x28 child".** `0018AFF0` is a push_back (`0018B006`-`0018B013`, grow `001AB570` at `0018B020`), so slot 1 **appends** the child to `[01F7F5E0]`. Removal is slot 3's `0018B0B0` (`0018B0DB` nulls matches).
2. **Section 3, slot 6: "opens a tagged record via 008C2CC8, checks a == 2 tag".** `008C2CC8` is the IAT entry `api-ms-win-crt-math!_fdtest`. The `== 2` test zeroes NaN inputs (`001FA024`/`001FA02A`) before the stores to `+0x3B0..+0x3B8`.
3. **Section 3, slot 11: "mulss against 008C5B2C".** The operand at `001F8BE0` resolves to `008C5B34` (1/128). `008C5B2C` holds 0.001.
4. **Section 3, slot 9: "clamps arg+0xC against the 008C5B40 bounds pair".** `008C5B40` is one divisor (255.0, used at `001F9ABF`/`001F9ACC`). The clamp is [0, 1.0], with 1.0 at `01CEBBA8` (`001F9AB2`).
5. **Section 4 layout, "+0x2C8 .. +0x2E0 slot 24" and "+0x2E8 .. +0x310 slot 30".** These are handle offsets **inside the 0x318 records** (`001FA262`/`001FA269` and `001FA8C2`/`001FA8C9` compute `record = base + i*0x318`). They are not fields of the object.
6. **Section 4 layout, "+0x4AC int".** Slot 16 compares it as a float against 0.9 (`001FA5A4`/`001FA5AD`). The constructor (`001F4EBE`) and ResetState (`001F8A1E`) write 1.0f there.
7. **Section 4 layout, "+0x3B0 is passed as an out-param vec4 to 001ABF50".** `001ABF50` only reads it (`001AC075`, `001AC07B`; `r15` = arg4 at `001ABF71`). It writes `+0x3D0` and `+0x3C0` (`001ABF6E`, `001ABF74`).
8. **Section 1 / section 6 / GFZ name of slot 24, "material overrides that tint a body when a status lands".** Slot 24 writes only `refractionEnabled`, `refractionPower`, `refractionAlpha` and `RefractionSampler` (`001FA329`, `001FA33E`, `001FA353`, `001FA35E`, `001FA369`). Section 6's "neither has been read; both are named only" is now read: slot 24 is refraction, and slot 26 is a node-matrix palette.
9. **Section 5 call chain, "per frame, guarded on +0x4B4: ... slot 26".** Slot 26 `001FAA10` never reads `+0x4B4`.
10. **Contract R-4: "Thirteen gate at entry ... slots ... 24".** Slot 24 can store `byte [001BC000()+0x230] = 1` (`001FA1C2`) before its latch test (`001FA1C9`). This is the same shape R-4 already records for `001F89E0`.
11. **Contract R-4: "the record's +0x10 bit 0 (001FA5DE)".** The byte tested is `+0x10` of the object held at `record+0x00` (`001FA5DA mov rcx, [rcx+rax]`), not the record's own `+0x10`.
12. **Page EC7 note on 001EF060: "XORs 0x80000000 into the nine floats at rdx".** It reads `rdx` and writes the sign-flipped 3x4 to `[[rcx+8]]` (`001EF126`-`001EF166`). `rdx` is unchanged.
13. **Section 8c "BB-1, upgraded": "whatever draws, it is not reached in one call from these methods".** This is true. The draw is `001F5D70` (non-virtual), reached through the list that slot 1 fills and `CharacterOrderedObject` slot 1 `00215320`. Section 1's "this is the object that draws a character" holds, but through that method, not through any of the 31 slots.
14. **Section 2, "param+0xD0 is the light count".** It is range-tested as an index ((x+1) <= 6 unsigned, `001F9F08`/`001F9F0C`) and stored through the `sunIndex` handle (`001F9F15`). This is a naming-level disagreement, not a byte-level one.

## Not followed / limits

- **After the ring:** the ring's consumer and the D3D11 upload/draw calls.
- **Readers not traced:** the consumers of the mesh-instance matrices written by slot 7 (`[mi+8]`) and slot 26 (`[mi+0x18]`).
- **Bodies not read:** `001AD440`, `001A9930`, `001D50D0`, `0017FE10`, `001AC670`, `001AC720`, `00183320`, `00186840`/`00186A00`/`00186A80`, `001EE410`/`001EE1D0`, `001BDAB0`/`001BD7D0`.
- **Order:** slot 30 reads `001F0850()+0x4C`/`+0x50`, which `001FB310` writes only on the shadow branch. The frame order between those two was not established.
