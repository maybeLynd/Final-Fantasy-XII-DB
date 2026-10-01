# BB-1 — what `CharacterRenderObject` renders, per method

FABLE, Claude Opus 5.5, 2026-09-27. **NATIVE/STATIC. Nothing was executed.**
Table: `bb1-methods.tsv` (31 rows, one per slot of vtable `00903B68`). Detail: [`findings.md`](findings.md). Control:
`bb1_methods.py` (4 checks, FAILS 0).

**The question.** BB-1 asked what the class renders, per method. Only the ready flag and the allocation had been read,
and no rendering call had been traced out of any of the 31 methods. The page's 2026-09-02 negative stands: none of
the 31 draws by itself. What was missing is where the drawing happens, and what each method feeds into it.

**The answer: the class draws through a method outside its vtable, reached through the per-frame ordered list.**

| step | code | control |
|---|---|---|
| enqueue, per frame | the render record's update `0053AB50` calls slot 1 on `[r12+0x6B8]` through `0017F0B0` (`0053AE1A`, `0053AE2C`). Slot 1 `001F89B0` push_backs `this+0x28`, a pooled `CharacterOrderedObject` whose `+8` points back at `this`, into the ordered list `[01F7F5E0]` (`0018AFF0`) | M4 |
| frame render | `GameApplication`'s render slot 8 (`0017D090`) runs the pass list `00187950`. It walks the list through `0018B100` and calls each element's slot 1, which for this element class (vtable `00903940`) is `00215320`: `mov rcx, [rcx+8]; jmp 001F5D70` | M4 |
| draw | `001F5D70`, a non-virtual method of the class, calls Phyre's draw submit `0060B980` for each mesh instance, in a shadow, alpha or opaque mode (`001F5F38`, `001F61CC`) | M4 |
| submit | `0060B980` copies each material's parameter block into the renderer ring and appends a `0x80`-byte draw record (findings §"render path") | reader, not re-checked |

**What each method feeds into that route** (the table has every slot):
- **Parameter uploads (8, 10, 12, 14, 19, 20, 24, 30).** These write the CPU-side shader parameters of each character
  material: lights, the alpha threshold, `clutBank`, punch-through alpha, textures / cube maps / texture animation,
  the reflection sampler, refraction, and shadow and height values. `0060B980` copies those blocks into the ring.
- **State only (14 slots).** These stage values the draw reads through another method:
  - slot 16 picks each mesh segment's named render pass;
  - slots 13 and 9 feed `001FAD50`;
  - slots 22, 23 and 25 feed slot 30;
  - slots 6 and 7 place the cube-map probe lookup.
- **Bookkeeping (9 slots).** Lifecycle, getters and setters.

M3 confirms the 2026-09-02 negative for all 31: no slot's direct closure (depth 4) reaches a Gi emitter or the draw
list. It carries a control that does reach one.

**Not followed.** Three things were not traced:
- the renderer ring's consumer and its D3D11 calls, the Phyre backend every Phyre draw shares;
- the readers of the mesh-instance matrices that slots 7 and 26 write;
- a dozen small helpers named in the rows.

These are below the question's grain: what each method renders is established at the level of the draw it feeds.

**Contradictions.** Thirteen page and contract statements are contradicted by the bytes (findings, last section; item
13 there agrees).
- **Routed to FRONTIER** (`FABLE-REQ-FRONTIER-BB1-SLOT-TABLE-CORRECTIONS`): items 1–4, the §3 slot-table rows from
  FRONTIER's NOCALLER-INSTALLERS pass; item 7, SWE2-STRUCT's `+0x3B0` row; and item 12, the EC7 note on `001EF060`.
- **FABLE's own, corrected in this publish** ([consumer check](consumer-check.md)): items 5, 6, 8 and 9 (the
  2026-09-08 layout and call-chain prose), items 10 and 11 (the contract's R-4), and item 14 (BB-2's "light count").
  Each was re-read by hand at its instruction.

FABLE checked six of them in the bytes:
- slot 1 appends; it does not release;
- slot 6's `008C2CC8` is the CRT import `_fdtest`;
- slot 11's constant is at `008C5B34` (1/128);
- slot 9's `008C5B40` is one `255.0` divisor;
- `+0x4AC` is `1.0f` from the constructor, a float;
- slot 26 never reads `+0x4B4`.
