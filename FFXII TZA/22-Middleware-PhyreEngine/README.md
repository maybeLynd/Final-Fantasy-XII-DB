# Middleware - Sony PhyreEngine

**Engine category.** The middleware FFXII TZA is built on: D3D11 rendering, reflection, physics adapters, texture and stream machinery.

| | |
|---|---|
| Classification source | CodeDomain: Phyre.* |
| Functions | 6,768 |
| Status | see [`../_index/COVERAGE.md`](../_index/COVERAGE.md) |

## Systems in this category

- [`The-Frame/what-happens-between-two-frames.md`](The-Frame/what-happens-between-two-frames.md) —
  **DOCUMENTED, tier 1, crossref-clean.** The category's second framing correction, and a larger one:
  the frame runs from Phyre's slot 4 into a **seven-mode dispatch** on one byte, and what it draws with
  is **a PlayStation 2 Graphics Synthesizer GIF command stream** — verified GIFtag, GS register numbers
  and field layouts — handed to a separate graphics thread. **Phyre owns the shell, not the pixels.**
  Recovers the engine's own names for the frame phases (`PAD CONTROL`, `FAST MODE`, `SCREEN CAPTURE`)
  from markers the linker disguised as CFG checks, and the nine-bit render-pass enable mask.

- [`Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md`](Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md) —
  **DOCUMENTED, tier 1.** 4,557 functions (1 in 8 in the whole binary) that describe the game's
  own C++ classes to itself. Includes a proof that **a body-bytes SHA-256 cannot detect clones**.
- [`Application-Framework-Boundary/the-game-is-a-phyre-application.md`](Application-Framework-Boundary/the-game-is-a-phyre-application.md) —
  **DOCUMENTED, tier 1, one falsification pass.** The category's framing correction: FFXII does not
  *use* PhyreEngine, it **is** a PhyreEngine application. `GameApplication` derives from
  `Phyre::PFramework::PApplication` — 31 slots, **18 overridden, 13 inherited** — so the frame
  tick, the `FFXII_TZA.vbf` mount and the input pump are game code filling middleware slots.
  Explains the subsystem map's finding that no game subsystem calls Phyre: **the control flow runs
  the other way.**

- [`Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md`](Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md) —
  **DOCUMENTED, tier 1, one falsification pass.** The engine's own field list, read back out:
  **680 fully-resolved field records over 246 named classes**, each with a **real byte offset** —
  `VPLight`, `VPMeshInstance`, `VPNode` and `VPPhysicsRigidBodyBase` recovered in full. Answers
  **BJ-4**, whose premise was wrong: there is no type-id constant. **680 of the 682 registrations
  are lazy**, so a descriptor exists at startup with an empty member list. Closes **BL-4** and
  **BL-2**, and corrects the descriptor-layout units in the sibling document.

- [`Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md`](Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md) —
  **DOCUMENTED, tier 1.** The retail EXE embeds **Lua 5.2.1**, with 1,219 generated binding
  functions. Carries a measured GFZ correction (94% of the Lua C API cluster is generic-tagged)
  and a retracted false negative.

- [`Script-Object-Accessors/phyre-script-object-accessors.md`](Script-Object-Accessors/phyre-script-object-accessors.md) —
  **DOCUMENTED, tier 2.** **747 functions named in one pass** — generated
  `PObjectAccessor<T>::Get` instantiations, all from one header, that type-check objects handed
  over by Lua before the engine touches them. Carries a **GFZ audit: precision 100 %, recall 79 %**.

- [`Shader-Variant-Selection/the-context-switch-axes-and-the-variant-key.md`](Shader-Variant-Selection/the-context-switch-axes-and-the-variant-key.md) —
  **DOCUMENTED, tier 1.** The nine `PContextSwitch` classes and the eight named axes —
  `NUM_LIGHTS`, `SKINNING_ENABLED`, `LOD_BLEND`, `SHADER_LOD_LEVEL`, `ORTHO_CAMERA`,
  `INDICES_16BIT`, `INSTANCING_ENABLED`, `LOW_RES_PARTICLES` — that decide which compiled shader
  permutation a draw gets. Each evaluates one property of the draw into a context-variant key,
  which is binary-searched in the material's variant table; the same objects write the `-D`
  defines back out. Reads 18 of the 48 functions of `UQ-289` and measures the rest.

- [`Post-Process-Chain/the-phyre-post-effect-class-family.md`](Post-Process-Chain/the-phyre-post-effect-class-family.md) —
  **DOCUMENTED, tier 2 for the names and tier 1 for everything else.** PhyreEngine's whole post-effect
  catalogue, decoded from MSVC RTTI: **37 classes and nine implementations**. The `Base` and `D3D11`
  layers override nothing but their destructors, and Phyre's MLAA and screen-space ambient occlusion
  are compiled in and inert — the game renders its own. Names the eleven `0065xxxx` bodies that are
  the largest block of `UQ-289`, and joins the post-effect classes to the shader-variant key.

**Composition of this category** (by CodeDomain tag): Reflection 4,557 · ScriptVM 1,219 ·
Middleware 347 · Rendering 287 · PostProcessing 72 · Physics 70 · Animation 69 · SceneCamera 22 ·
Framework 19 · Serialization 18 · Geometry 14 · Threading 13 · remaining 61.

**Highest-leverage task in the whole database:** the EXE ships roughly 2,350 RTTI `type_info` class markers (`.?AV` x2297, `.?AU` x53) mangled with `...@Phyre@@`. Recovering `address -> class -> method` would name most of this category mechanically. Use `DumpMsvcVtableRtti.java`, or a scripted COL walk on LIEF. Tracked as open question **B-3**.
*Status 2026-09-26 (FABLE, Claude Opus 5.5): done. **B-3** is ANSWERED: the recovered class set was applied on 2026-09-02 as the vtable method index. What remains is per-function placement, **AQ-2** (PARTIAL: 4,515 of the 6,769 `CodeDomain:Phyre` functions placed on a class by vtable evidence), and the linker-folded bodies that carry no single class, **BA-1**.*

## How to add a system here

1. Copy [`../_templates/SYSTEM.md`](../_templates/SYSTEM.md) into a descriptively-named
   subfolder (or as a `.md` file if it is a single mechanism).
2. Fill all eight sections. A missing section means `STUB` or `PARTIAL`, never `DOCUMENTED`.
3. Mirror every "What is not known" entry into
   [`../_index/OPEN-QUESTIONS.md`](../_index/OPEN-QUESTIONS.md).
4. Register any cross-subsystem chain in
   [`../_index/CALL-CHAINS.md`](../_index/CALL-CHAINS.md).
5. Obey [`../_index/EVIDENCE-STANDARD.md`](../_index/EVIDENCE-STANDARD.md).
   No banned evidence class, ever.
