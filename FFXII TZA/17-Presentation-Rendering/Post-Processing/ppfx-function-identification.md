---
system: PPFX / Yebis post-processing — function identification
category: 17-Presentation-Rendering
status: AUDITED
owner_layer: CodeDomain — no PrimaryOwner (middleware)
evidence_tier: 2
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 8 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
audit:
  passes: 2
  last_pass: 2026-09-02
  last_pass_state: falsification-pass
  crossref_clean: true
  reopened_count: 0
---

# PPFX / Yebis post-processing — function identification

> **135 more functions named** (plus 12 exception funclets) from authored diagnostics — the same technique that named 90
> audio functions, applied to the middleware that produces FFXII's bloom, depth of field and
> glare.

## 1. What the player sees

FFXII's characteristic look — the soft bloom around bright light, the way distance blurs, the
star-shaped glare off water and metal, the auto-adjusting exposure when you walk out of a
cave — is not the base renderer. It is a post-processing layer applied after the scene is
drawn, and this document identifies the functions that implement it.

Nothing here changes behaviour. It makes the behaviour *findable*: anyone wanting to alter
FFXII's depth of field now knows which functions to read.

## 2. Native mechanism

The post-processing middleware is **PPFX**, the Yebis library. Like SEAD it narrates its own
failures with strings naming the method that raised them:

```
CPostEffect::SetFramebuffer(): Cannot be called while BeginPostEffectScene() ...
CPostEffect::Initialize(): IGPUDevice::CreateDevice() failed.
IGPUDevice::ApplyRenderState_DepthTestEnable() is not supported.
CRenderGlare::CreateSystemObjects(): m_pStarGeneration->Initialize() failed (0x%x)
TEXSHADERSET::CreateEffect(): IGPUEffect::CreateEffectFromFile() failed (0x%x:
```

Scanning `.text` for RIP-relative `LEA` instructions targeting those strings and attributing
each to its containing function gives:

| Result | Value |
|---|---:|
| Distinct strings matched (20 class prefixes) | 545 |
| LEA references found | **317** |
| Entries attributed | **147** — but **135 functions + 12 exception funclets**, see section 10 |
| References not inside any known `functions.tsv` entry | **0** (12 landed in funclets) |
| Still named `FUN_*` beforehand | **135 of 135 real functions — 100 %**, not 92 %; see section 10. **Carries almost no weight — vtable methods are 96.0 % `FUN_*` to begin with; section 11.** |

Tooling: `Tools/analysis-kit/gfz-scripts/string_xref.py`; output
`Tools/work/rtti/ppfx_xrefs.tsv`.

### Validation

**Cross-validation against RTTI.** 23 of the 147 also appear in the independently recovered
vtable mapping. Every case agrees:

| Address | RTTI class | Emitted string |
|---|---|---|
| `006E04F0` | `PPFX::IPfxBaseRenderToTexture` | `IPfxBaseRenderToTexture::Initialize()` |
| `006E07A0` | `PPFX::IPfxBaseRenderToTexture` | `IPfxBaseRenderToTexture::Uninitialize()` |
| `00724EC0` | `PPFX::IGPUDevice` | `IGPUDevice::ApplyRenderState_DepthTestEnable()` |
| `00724F50` | `PPFX::IGPUDevice` | `IGPUDevice::ApplyRenderState_DepthFunc()` |

**Ownership coherence.** All 147 carry **no V120 PrimaryOwner** — consistent with PPFX being
third-party middleware rather than an FFXII subsystem. That is the *opposite* of the audio
result, where all 90 were `Audio`-owned, and both are correct: each mapping lands entirely
within one coherent ownership class. A faulty scan would scatter.

**Regression.** Re-running the audio scan after the multi-pattern tool change reproduced
exactly 208 references / 90 functions, confirming the change did not perturb the earlier
result.

### Class inventory

Named in strings, corroborating the RTTI class list from the same subsystem:

| Class | String mentions | Role from context |
|---|---:|---|
| `CPostEffect` | 201 | the post-effect scene root — `BeginPostEffectScene` / `SetFramebuffer` |
| `IGPUDevice` | 69 | GPU abstraction — device, surface, texture, render-state |
| `CDepthOfField` | 56 | depth of field, incl. aperture filter shapes |
| `CTextureUtil` | 41 | shared texture pool |
| `CRenderGlare` | 38 | glare / star generation |
| `CTinyEffect` | 26 | effect build |
| `IGPUSurface` | 22 | surfaces |
| `IPfxBaseContext` | 17 | context lifecycle |
| `CRenderTexture` | 16 | render targets, depth resolve |
| `IPfxBaseRenderToTexture` | 12 | RTT lifecycle |
| `IGPUTexture` | 10 | textures |
| `TEXSHADERSET`, `IGPUEffect`, `CRenderTextureArray` | 9, 8, 9 | shader/effect loading |

`CDepthOfField::ApplyDepthOfField_ApertureFilterLevel_EAPERTUREFM_DISC_...` names an
**aperture filter mode** enum — the depth-of-field bokeh shape is selectable, with `DISC` one
of the values.

`IGPUDevice::ApplyRenderState_*() is not supported` indicates the GPU abstraction has render
states the Direct3D backend deliberately declines rather than implements.

## 3. Key addresses

Full mapping: `Tools/work/rtti/ppfx_xrefs.tsv` (317 rows).

| Address | Identity |
|---|---|
| `006E04F0` | `IPfxBaseRenderToTexture::Initialize` |
| `006E07A0` | `IPfxBaseRenderToTexture::Uninitialize` |
| `00724EC0` | `IGPUDevice::ApplyRenderState_DepthTestEnable` |
| `00724F50` | `IGPUDevice::ApplyRenderState_DepthFunc` |

## 4. Data structures and formulas

None. This document produces identity, not mechanism ~~— no PPFX function body has been read~~ *(corrected 2026-10-02, OPUS: H-4 and H-6 below read three bodies)*.

**Reference resolution** (as for audio):

```
target_va = insn_va + 7 + disp32
function(addr) = the f with  f.entry <= addr < f.entry + f.body_bytes
```

## 5. Call chain

~~Not derived.~~ *(answered: see the-post-processing-effect-catalogue.md §5 and CONTRACT-post-processing-subsystem.md for the call chain; 2026-10-02, OPUS)* One ordering constraint is stated by the strings themselves:

```
CPostEffect::BeginPostEffectScene()
    ... SetFramebuffer() is refused inside this window ...
CPostEffect::EndPostEffectScene()
```

`CPostEffect::SetFramebuffer(): Cannot be called while BeginPostEffectScene()` establishes a
**scene bracket** with an ordering rule the library enforces at runtime.

## 6. Modding notes

- **Start from `ppfx_xrefs.tsv`.** 147 named ~~functions~~ entries *(corrected 2026-10-02, OPUS: 135 functions and 12 funclets, the correction below)* is the entry point for any
  post-processing work — bloom, DoF, glare, exposure.
- **Respect the scene bracket.** `SetFramebuffer` outside `Begin/EndPostEffectScene` is
  explicitly refused.
- **Depth-of-field aperture shape is an enum**, not a constant — `EAPERTUREFM_DISC` is one
  member.
- **This is licensed middleware** (Yebis). Its behaviour is not FFXII-specific and upstream
  documentation may apply.
- **XIIOnline:** post-processing is entirely client-local presentation. Nothing here should
  ever be networked.

## 7. What is not known

- [x] ~~No PPFX function body has been read.~~ These are identities only. **H-4.**
      **The word “No” is false, and the counter-example is one line below this box.**
      *(Narrowed 2026-09-16 (FABLE), and narrowed rather than retracted, because the substance holds.)*
      **`H-3`'s answer, directly beneath, reads a PPFX body**: Yebis's own printf wrapper `006DF480`
      *“reaches the API at `006DF4FA`”* — an interior address, which is the project's own test
      for a body having been read. And
      [the Gi render command family](../Gi-Render-Commands/gi-render-command-family.md) quotes
      `PPFX::IGPUDevice`'s `AddRef` instruction for instruction — `inc [rcx+8] ; mov eax,[rcx+8] ;
      ret` — and reads it as a COM-style refcount returning `int`.
      **Two bodies, one of them three instructions long, against 147 identities: the question's
      substance is intact and only its universal is wrong.** This page carries **1** interior citation
      and 8 entry citations; the effect catalogue beside it carries **0** interior. Unlike `UQ-64`,
      which was stale by seventy-three, this one is stale by about two — worth correcting because a
      universal negative is either true or it is not, and worth saying it is nearly true so nobody
      reads the correction as a bigger claim than it is.
      *SUPERSEDED 2026-09-26 (FABLE, Claude Opus 5.5) under FRONTIER's class-1 ruling: a population-coverage statement; the population is carried by 17-Presentation-Rendering/Post-Processing/ppfx-function-identification.md. See the register row.*
- [x] ~~Whether PPFX diagnostics also reach `OutputDebugStringA` as SEAD's do — if so the
      renderer narrates its failures live too.~~ **H-3 — ANSWERED 2026-09-07: yes.** Not directly —
      through **Yebis's own printf wrapper `006DF480`**, which reaches the API at `006DF4FA`.
      **90 of the 102 functions re-identified here by diagnostic-string prefix call it**, among 160
      callers and 800 call sites. **The renderer narrates live**, and it looked silent only because
      a census taken at the API misses everyone who logs through a wrapper. See
      [`../../24-Compiler-And-CRT-Runtime/Runtime-Service-Surface/what-the-game-asks-windows-for.md`](../../24-Compiler-And-CRT-Runtime/Runtime-Service-Surface/what-the-game-asks-windows-for.md).
- [x] ~~The full `EAPERTUREFM_*` aperture-mode enum.~~ **H-5 CLOSED 2026-09-14 (OPUS) —
      dispositioned NOT ANSWERABLE FROM THE SHIPPING ARTEFACT, which is a finding rather than a gap.**
      Re-measured over the whole 32,864,752-byte image: `EAPERTUREFM` occurs **6** times (the earlier
      narrowing said three), every one inside a
      `CDepthOfField::ApplyDepthOfField_ApertureFilterLevel_EAPERTUREFM_DISC…` log format at
      `00DA8660`, `00DA8710`, `00DA8970`, `00DA8D30`, `00DA8D90` and `00DAADB0`. **`_DISC` is the only
      member name present.** All six are unreferenced: **0** rip-relative references from `.text` and
      **0** absolute 8-byte pointers anywhere in the file, against a positive control of **2,517**
      referenced `.rdata` targets inside `00D80000`-`00DB0000`, so the test is not simply blind in
      that range. The per-mode logging was compiled out and the remaining members exist only in the
      YEBIS/PPFX headers, which are not a shipped artefact. It reopens as a one-line read if a header
      ever enters the corpus.
      *Narrowed 2026-09-14 (FABLE), not answered: the executable names one member, and the rest is not in the image.*
      - **Every `Aperture` identifier in the file** (a byte search of the whole EXE) is: `ApplyApertureFilter`,
        `ApplyDepthOfField_ApertureFilterAllLevels`, `…_ApertureFilterLevel`, `…_ApertureFilterLevel_EAPERTUREFM_DISC`,
        `…_EAPERTUREFM_DISC_ApplyApertureFilter`, `IsSupported_BokehAperture`, `SetApertureAiryDiscEnable`,
        `SetApertureFilterLevelVisualize`, `UpdateApertureFilterLevelParams`, `currentApertureLevel`,
        `fApertureFilterLevel`, `mDofApertureFnumber`, `mDofSpecialApertureFnumber`, `m_aApertureLevelCombination`,
        `m_iApertureDiameterParam`, `m_nApertureFilterLevels`, `m_pApertureFilterSharedLevelSourcePool`,
        `m_pApertureFrameBuffer` and `previousApertureLevel`.
      - **`EAPERTUREFM_DISC` is the only enum member among them.** The three log strings that carry it (`00DA8660`
        "…failed", `00DA8710` "…succeeded", `00DAADB0` "…(%d, %s)") have **no reference anywhere in the file**: a byte-wise
        rel32 scan of all of `.text` at every offset, and absolute (image-base and VA) and RVA pointer searches, all come
        back empty. So the per-mode code that printed them did not survive into this build.
      - The Airy-disc and bokeh features are separate switches (`SetApertureAiryDiscEnable`,
        `IsSupported_BokehAperture`), not named members of this enum.
      - Recovering the other members needs the YEBIS headers or another build.
- [x] ~~Which `IGPUDevice::ApplyRenderState_*` calls are unsupported and why.~~ **H-6 ANSWERED 2026-09-22 (FABLE):** three — `DepthTestEnable` (`00724EC0`), `DepthFunc` (`00724F50`) and `AlphaFunc` (`00724FF0`) — each returning **`E_NOTIMPL`** and logging a rate-limited warning; a fourth string, `AlphaTestEnable`, is **dead** and is the one that gives the reason, `(DX10/11)`. See the section above. **H-6.**
- [x] The remaining ~44 string-named classes outside audio and post-processing. **H-2.**
      *SUPERSEDED 2026-09-26 (FABLE, Claude Opus 5.5) under FRONTIER's class-1 ruling: a population-coverage statement; the population is carried by 17-Presentation-Rendering/Post-Processing/ppfx-function-identification.md. See the register row.*
- [x] ~~The 7 further PPFX functions a broader pattern set finds, incl. `006F8740`
      (section 10). The documented 135 is a floor.~~ **H-7 ANSWERED 2026-09-13 (FABLE):** the floor is replaced by the object — every census entry from `006DA880` up to `007911E0` is Yebis / PPFX (1,766 entries, 1,660 declared; `006F8740` among them), bounded by source-path evidence, edges and controls on [the Yebis / PPFX source map §11](../../23-Third-Party-Libraries/PostEffects-Yebis-PPFX/yebis-ppfx-source-map.md). **H-7.**

## `H-6` answered — three render states are declined with `E_NOTIMPL`, and a fourth is dead (FABLE, 2026-09-22)

§4 named two `ApplyRenderState_*` bodies from their strings. **There are four such strings and
three live decliners**, found by enumerating every `IGPUDevice::ApplyRenderState_*` string in the
image and sweeping the code for rip-relative references into their `.rdata` band. *The sweep is
controlled by this page's own pair:* `00724F12` → `00D9C320` reproduces §4's
`00724EC0` = `ApplyRenderState_DepthTestEnable` exactly.

| body | render state | `__LINE__` passed to the warning |
|---|---|--:|
| `00724EC0` | `ApplyRenderState_DepthTestEnable` | **5588** (`0x15D4`) |
| `00724F50` | `ApplyRenderState_DepthFunc` | **5671** (`0x1627`) |
| `00724FF0` | **`ApplyRenderState_AlphaFunc`** — *not previously identified* | **5846** (`0x16D6`) |

### They do not silently ignore the call — they return `E_NOTIMPL` (FABLE, 2026-09-22)

**Every one of the three ends `mov eax, 0x80004001` on *both* exit paths** — `E_NOTIMPL`, the
standard COM “not implemented” code. *So a caller is told, on every call, that the state was not
applied;* the logging is decoration on top of a real return value, not the whole behaviour.

**And the warning is rate-limited, which is why it is easy to miss in a log.** Each body owns a
counter (`02EA1988` for `DepthTestEnable`, `02EA1990` for `AlphaFunc`) and prints only when the
counter is **0**, or when `counter % 100 == 25` — the `0x51EB851F` / `sar 5` divide-by-100 idiom at
`00724ED0`–`00724EED`. Two verbosity globals (`01F3BA80`, `01F3BA8C`) must **both** be `>= 1` as
well. *A build with either at zero declines silently while still returning `E_NOTIMPL`.*

The message is assembled from two calls to the same logger: the prefix
`..\src\GPU\GPUInterfaceDevice.cpp(%d) : Feb 18 2016 PPFX WARNING: ` with the line number, then
the state's own sentence. **That names the source file and the build date of the GPU abstraction
layer**, which is where all three live.

### The fourth string is dead, and it is the one that gives the reason (FABLE, 2026-09-22)

`00D9C8A0` reads **`IGPUDevice::ApplyRenderState_AlphaTestEnable() is not supported (DX10/11).`**
and **nothing reaches it**: 0 rip-relative references, and 0 occurrences of its address as a
64-bit pointer, a 32-bit pointer or an RVA anywhere in the file. *That is the same shape §7 already
established for the `EAPERTUREFM_DISC` log strings — the code that printed it did not survive into
this build.*

> **The dead string is nonetheless the best evidence for the “why”, because it is the engine's own
> parenthetical.** `(DX10/11)` says the class of reason: Direct3D 10/11 removed these from the
> dynamic fixed-function state — alpha test outright, and depth test/func into immutable
> depth-stencil state objects that cannot be set one field at a time. **So the PPFX interface keeps
> per-state setters that a D3D11 backend structurally cannot honour, and answers `E_NOTIMPL`.**
> *Stated as the reading the parenthetical supports; the backend does not explain itself further,
> and no code path was found that would.*

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| 317 references across 147 functions | `string_xref.py` over the authorized EXE joined to the 38,161-function table | 2 |
| No spurious matches | **all 147** carry no PrimaryOwner — a single coherent ownership class, as expected for middleware | 2 |
| Attribution complete | 0 references fell outside a known function body | 2 |
| RTTI and strings agree | 23 functions in both mappings, zero contradictions | 2 + 4 |
| The technique is sound, not lucky | validated independently on two subsystems with opposite ownership profiles (Audio: all Audio-owned; PPFX: all unowned), both 0 unattributed | 2 |
| Tool change did not perturb earlier results | audio scan re-run after the multi-pattern change reproduced exactly 208 / 90 | 2 |
| A scene bracket exists | `CPostEffect::SetFramebuffer(): Cannot be called while BeginPostEffectScene()` | 2 |

**Scope honesty:** identity only. `00724EC0` is `IGPUDevice::ApplyRenderState_DepthTestEnable`
because it says so when it refuses — that does not mean its body has been read.

## 9. Related

- [`../../18-Audio/sead-function-identification.md`](../../18-Audio/sead-function-identification.md) — the same technique, first application
- [`../README.md`](../README.md) — category overview
- [`../../22-Middleware-PhyreEngine/README.md`](../../22-Middleware-PhyreEngine/README.md) — the other middleware layer

## 10. Falsification pass 2026-09-02

**Attack chosen.** Like the SEAD document, this is a count plus an attribution table produced by a
tool the database still has, so every figure can be **regenerated rather than re-read**. Two things
were done: the stored mapping was recounted, and the scan was **re-run from the binary** with an
independently chosen pattern set.

### SURVIVED: every stored figure, and the strongest claim in the document

| Claim | Re-derived | Result |
|---|---|---|
| 317 LEA references | rows in `ppfx_xrefs.tsv` | **317** |
| 0 references outside a known entry | attribution column | **0** |
| 135 still named `FUN_*` | distinct entries named `FUN_*` | **135** |
| **all carry no V120 PrimaryOwner** | owner column, all 147 | **147 / 147, zero exceptions** — **but this is true of every middleware namespace in the image and is not evidence of a coherent class; section 11.** |
| 23 of them also in the RTTI vtable mapping | join against `methods.tsv` | **23** |

The four cross-validated rows were checked individually and **all four agree exactly** — class and
emitted string both, e.g. `00724EC0` is `PPFX::IGPUDevice` slot 21 and emits
`IGPUDevice::ApplyRenderState_DepthTestEnable() is not supported.`

The EXE was hash-checked before the re-scan: `73461d08...721f8`, the authorized binary.

### CORRECTED: 147 is not 147 functions - it is 135 functions and 12 funclets

Twelve of the 147 attributed entries are named `Unwind@<addr>` in `functions.tsv`. They are **not
distinct functions**. What they are was established rather than assumed, and one hypothesis was
disproved on the way:

- They are in **`.text`** (RVA `0x782289`, inside `.text` `0x001000..0x7A1635`) - so they are not
  a `.rdata` blob. *(An earlier reading of mine said `.rdata`; that compared a VA against RVA section
  ranges and was wrong.)*
- ~~**None of the twelve is a `.pdata` `UnwindInfoAddress` target** — 0 of 12 against all 20,202
  distinct unwind-info RVAs. So they are not `UNWIND_INFO` records either.~~ *(pass 6, 2026-09-15, OPUS)* Withdrawn as
  evidence, because `.pdata` is banned. Nothing needs it: the placement in `.text` (above) and the funclet
  prologue (below) already establish what the bytes are.
- Their bytes are a textbook MSVC x64 **funclet prologue**:

```
40 55              push rbp
48 83 EC 30        sub  rsp, 0x30
48 8B EA           mov  rbp, rdx        <- RDX carries the establisher frame: the funclet ABI
48 8D 05 37F34E00  lea  rax, [rip+0x4EF337]
```

`mov rbp, rdx` is the signature. These are **exception-handling funclets** — real code, entered while
unwinding. The dump names ordinary catch funclets `Catch_All@`, so `Unwind@` is a distinct naming for
code reached through unwind info.

**This makes the document's own headline stronger, not weaker.** 147 − 12 = **135**, which is exactly
the number the document reports as *"still named `FUN_*` beforehand"*. Those are the same 135. So
**every single real function this scan identified was previously unnamed — 100 %, not 92 %.** The
92 % was an artifact of counting funclets in the denominator.

The ownership-coherence argument is unaffected in substance: the 12 funclets trivially have no owner,
and the 135 real functions are **135 / 135** unowned — ~~which is the coherent class the document claims~~. **The unowned figure does not establish a coherent class: `sce`, `std`, `PrimitiveRendererD3D11` and every `bt*` namespace are 100 % unowned too. Section 11.**

### The string set mixes two kinds of string

**28 of the 317 references** (16 distinct strings) point not at method diagnostics but at
**member-variable names** — `CPostEffect::m_pRenderBuffer`, `CPostEffect::m_pRenderGlare`,
`CPostEffect::m_pGlareModulatorWork`. These are what the funclets load. A member name identifies a
*field*, not the function referencing it, so it is weaker identity evidence than
`IGPUDevice::ApplyRenderState_DepthFunc() is not supported.` Both kinds sit in one table; the
distinction is worth keeping when reading `ppfx_xrefs.tsv`.

### 135 is a floor, not a total

The scan was re-run with 13 bare class-name patterns instead of the original 20:

```
patterns 13   distinct strings 565   references 333   entries 155   unattributed 0
```

The documented set is a **strict subset** — every one of the original 317 references reappears, zero
contradictions. Removing the 13 funclets in that run leaves **142 real functions**, so the broader
scan finds **7 more** than the document.

At least one is a genuine miss, not a pattern artifact:

```
CPostEffectEndPostEffectScene_PreProcess: CRenderTexture::ResolveCurrentDepthStencilTexture() failed (0x%x: %s).
```

a real PPFX diagnostic referenced **twice from `006F8740`**, absent from the documented 317. Its class
prefix is `CPostEffectEndPostEffectScene_PreProcess`, which a `CPostEffect::`-style pattern does not
match — the string names the *calling site* before the failing call, breaking the `Class::Method()`
shape the patterns assume.

**Interior read 2026-09-17 (SWE2-FRONTIER):** `006F8740` is `CPostEffect::EndPostEffectScene_PreProcess`
itself — the diagnostic names its own site. The 2,275-B body works the `02EA18xx`/`02EA19xx` PPFX state
block (byte flag `02EA18B1` tested against `r12b` at `006F8D85`), calls `0077F3A0`, `006FE080`,
`007142F0`/`00714560` and `00722900`, and both `PPFX ERROR: ` format strings at `00D90A58`/`00D90E70`
are referenced at [`006F8E86`](../../_index/ADDRESS-INDEX.md) and `006F8FF3` — the two sites the scan
counted.

### NOT re-derived

**545 distinct strings across 20 class prefixes.** The exact 20 patterns are not recorded anywhere, and
prefix choice changes the count directly (13 bare names gave 565). The figure stands as written,
explicitly unconfirmed. **Anyone re-running this scan should record the pattern list with the output** —
without it the headline count is not reproducible, which is the one thing a count of this kind must be.

## 11. Audit — what the 100 % figures are worth once the base rate is known

Two of this document's headline figures were checked against the population they were drawn from.
**Both are arithmetically correct and both are much weaker than their presentation implies.**

### `135 / 135 still named FUN_*` — unremarkable

| population | share still named `FUN_*` |
|---|---:|
| whole binary (38,161) | 84.2 % |
| excluding `Unwind@` / `Catch_All@` (34,270) | **93.8 %** |
| **all RTTI vtable methods (6,883)** | **96.0 %** |
| **PPFX's own methods (284)** | **93.0 %** |

**PPFX is slightly *less* unnamed than the vtable population it sits in.** The scan did not find
virgin territory; **the binary is virgin territory**, and a set of 135 functions drawn from it will be
all-`FUN_*` most of the time. The honest effect size is 96 % → 100 %, not 0 % → 100 %.

### `147 / 147 carry no V120 PrimaryOwner` — the wrong denominator

Against the whole binary's 73.8 % unowned this looks decisive. **Against the population PPFX actually
belongs to it is unremarkable, because middleware is unowned by definition of how V120 was tagged:**

```
PPFX                     284 methods   100.0 % unowned
sce                       75            100.0 %
std                       62            100.0 %
PrimitiveRendererD3D11    42            100.0 %
btDiscreteDynamicsWorld   41            100.0 %
btCollisionWorld          31            100.0 %
Phyre                   5268             97.4 %
--------------------------------------------------------
SQEX                     498             13.7 %   <- the one real exception
```

**Every middleware namespace is ~100 % unowned.** "PPFX carries no owner" is a restatement of "PPFX is
middleware", which the frontmatter already says (`owner_layer: CodeDomain — no PrimaryOwner`). It is
**not** independent evidence that the 147 form a coherent class.

**The genuinely informative row is `SQEX` at 13.7 %** — the only middleware namespace that *is* owned,
because its audio driver was analysed as gameplay-adjacent. That asymmetry is a real fact; the 100 %
rows are not.

### What survives

**The identification itself is untouched.** It rests on **317 LEA references with 0 outside a known
entry** and on the **four cross-validated RTTI rows**, not on either percentage. This audit removes two
pieces of decoration from the argument and leaves the load-bearing evidence exactly as it was.

## 137 functions the diagnostic strings name (2026-09-19, OPUS)

*This page carries 23 `Class::Method` names and already cites the `PPFX ERROR: ` format strings at
`00D90A58` / `00D90E70`. The image carries **569** `C*::`/`I*::` method-name strings for this
middleware, and they name far more than 23 functions.*

**The method, and the discrimination that makes it safe.** A diagnostic string naming a method is
referenced from the function that reports it, so a function referencing **exactly one** such name is
that method; a function referencing **several** is a caller or a dispatcher. Of 153 functions
touching these strings, **150 reference exactly one** and only **3** reference several — two with a
pair and one with seventeen, which is a dispatcher and is excluded. **137 of the 150 are still
`FUN_xxxxxxxx`.**

By class: `CPostEffect` 59, `IGPUDevice` 17, `CTextureUtil` 12, `CTinyEffect` 9, `CDepthOfField` 5,
`CRenderGlare` 5, and ~~sixteen~~ at least seventeen more classes with 1–3 each *(corrected 2026-10-02, OPUS: the list below alone names seventeen more)*.

```
0077ECE0  CDepthOfField::ApplyDepthOfField
0076F400  CDepthOfField::CreateDeviceResources
0077BF30  CDepthOfField::CreateScatterBokehOpticsTexture
0077A8C0  CDepthOfField::CreateScatterBokehTexture
00779150  CDepthOfField::Initialize
00727460  CGPUResourceManage::RegisterStaticGPUDevice
0070BB00  CPostEffect::ApplyAmbientOcclusion
0070BD80  CPostEffect::ApplyApertureFilter   <-- name used by more than one function
0070C050  CPostEffect::ApplyApertureFilter   <-- name used by more than one function
0070C460  CPostEffect::ApplyDepthOfFieldFilter
0070BA00  CPostEffect::ApplyEffects
006F6010  CPostEffect::ApplyEffects_DepthOfField
006F3BE0  CPostEffect::ApplyEffects_GenerateNormalAndLinearDepth
0070C810  CPostEffect::ApplyGaussianBlurFilter
0070B780  CPostEffect::BeginPostEffectScene
006F2560  CPostEffect::BeginTemporaryFilter
0070B990  CPostEffect::EndPostEffectScene
006F9030  CPostEffect::EndPostEffectScene_InternalProcess
006FB810  CPostEffect::EndPostEffectScene_Process
006F2690  CPostEffect::EndTemporaryFilter
006FE4C0  CPostEffect::GetMaxMotionBlurCameraRecurrences
007069E0  CPostEffect::InitializeAfterimage
00706940  CPostEffect::InitializeContinuousEffects
00706A50  CPostEffect::InitializeFeedback
00706760  CPostEffect::SetActiveView
0070DBA0  CPostEffect::SetAlphaOutputParameters
0070AA80  CPostEffect::SetAmbientOcclusionEnable
0070D920  CPostEffect::SetAmbientOcclusionMaskSource
0070A1F0  CPostEffect::SetAntialiasEnable
0070A260  CPostEffect::SetAntialiasFalloffDistance
0070A060  CPostEffect::SetApertureAiryDiscEnable
00709F40  CPostEffect::SetChromaticAberrationEnable
0070DC10  CPostEffect::SetColorGradingLutEnable
007114F0  CPostEffect::SetDepthFactorSource
00711350  CPostEffect::SetDepthOfFieldEdgeQuality
00706690  CPostEffect::SetDeviceContext
0070D780  CPostEffect::SetEffectMaskAlphaSource
0070D5C0  CPostEffect::SetEffectMaskColorSource
0070AF90  CPostEffect::SetFeedbackEnable
0070CD40  CPostEffect::SetFramebuffer
0070A0F0  CPostEffect::SetGaussianBlurEnable
0070A410  CPostEffect::SetGeometryBlurEnable
0070D400  CPostEffect::SetGlareModulatorSource
00707560  CPostEffect::SetGlareParameters
0070A350  CPostEffect::SetHeatShimmerParticleEnable
00709C90  CPostEffect::SetLensDistortionEnable   <-- name used by more than one function
00709D10  CPostEffect::SetLensDistortionEnable   <-- name used by more than one function
00707880  CPostEffect::SetLightShaftEnable
0070A480  CPostEffect::SetMotionBlurEnable
00708110  CPostEffect::SetMultisampleMode
007112F0  CPostEffect::SetRenderSceneHeightReverse_Gcm
00706B70  CPostEffect::SetRenderSceneLuminanceScale   <-- name used by more than one function
00707500  CPostEffect::SetRenderSceneLuminanceScale   <-- name used by more than one function
0070D090  CPostEffect::SetRenderSceneViewportScale
0070DFD0  CPostEffect::SetStaticSceneSource
0070AB80  CPostEffect::SetTemporalAntialiasEnable
0070B070  CPostEffect::SetTonemapResampleFilter
0070B500  CPostEffect::SetVignetteByOptics
0070B610  CPostEffect::SetVignetteByOpticsImageCircle
00705520  CPostEffect::Uninitialize
0070E520  CPostEffect::UnregisterDeviceSurface
0070E600  CPostEffect::UnregisterDeviceTexture
007067E0  CPostEffect::UpdateAlternateFrame
006F7660  CPostEffect::UpdateParameters_Base
007621F0  CRenderGlare::CreateDeviceResources
00760700  CRenderGlare::CreateSystemObjects
00766680  CRenderGlare::GenerateGlare_Afterimage
007677B0  CRenderGlare::GenerateGlare_Composite
00768980  CRenderGlare::Initialize
00722A40  CRenderTexture::BeginTiling
00722C80  CRenderTexture::EndTiling
006F1F60  CRenderTexture::m_mapDeviceTextureRenderTexture
0075DA10  CRenderTextureArray::CopyToSurface
0075B760  CRenderTextureArray::Initialize
0075E330  CRenderTexturePool::AllocateTextures
00731EA0  CTextureUtil::CreateLensRayConvergenceTexture
0073DD70  CTextureUtil::DrawRectGPU_DepthOfFieldLayerMask
007364D0  CTextureUtil::DrawRectGPU_MadCocT2_Sn
00735720  CTextureUtil::DrawRectGPU_MadT1_Sn   <-- name used by more than one function
00735B70  CTextureUtil::DrawRectGPU_MadT1_Sn   <-- name used by more than one function
00737D70  CTextureUtil::DrawRectGPU_MadT1_Sn   <-- name used by more than one function
00735530  CTextureUtil::DrawRectGPU_TexCoordMadT1_Sn
00735240  CTextureUtil::DrawRectGPU_TexCoordOffsetMadTn
0073BD30  CTextureUtil::DrawRectGPU_TonemapHDR
00780590  CTextureUtil::GetResult_UpdateInternalLuminance
007307A0  CTextureUtil::InitializeDevice
0072F7D0  CTextureUtil::InitializeDeviceSharedTexturePoolWithCheck
00790160  CTinyEffect::ApplyVertexInputs
0078C730  CTinyEffect::BuildEffect
0078F710  CTinyEffect::CreateDeviceProgram
0078D920  CTinyEffect::CreateFromFile
0078D7E0  CTinyEffect::CreateFromMemory
0078DFB0  CTinyEffect::CreateGlobalParameter
0078C080  CTinyEffect::CreateParameter
0078E3C0  CTinyEffect::CreateProgram
0078F800  CTinyEffect::CreateTechniquePrograms
00789160  IGPUBaseQuery::CreateDeviceQuery
00787E40  IGPUBuffer::BuildBuffer
00788250  IGPUBuffer::Map
00788430  IGPUBuffer::Unmap
00724FF0  IGPUDevice::ApplyRenderState_AlphaFunc
00724F50  IGPUDevice::ApplyRenderState_DepthFunc
00724EC0  IGPUDevice::ApplyRenderState_DepthTestEnable
00726360  IGPUDevice::CreateDepthStencilSurface
00726A70  IGPUDevice::CreateIndexBuffer
00726C30  IGPUDevice::CreateInputAttribute
00726D00  IGPUDevice::CreateQueryOcclusion
00726550  IGPUDevice::CreateSurface   <-- name used by more than one function
00726700  IGPUDevice::CreateSurface   <-- name used by more than one function
00725AA0  IGPUDevice::CreateTexture   <-- name used by more than one function
00725E40  IGPUDevice::CreateTexture   <-- name used by more than one function
007268C0  IGPUDevice::CreateVertexBuffer
00725C80  IGPUDevice::CreateVolumeTexture   <-- name used by more than one function
00725FF0  IGPUDevice::CreateVolumeTexture   <-- name used by more than one function
007259D0  IGPUDevice::DrawIndices
00723760  IGPUDevice::InitializeDevice
00723440  IGPUDevice::InitializeDeviceBuffers
0078A120  IGPUEffect::CreateEffect
0078A240  IGPUEffect::CreateEffectFromFile
00788800  IGPUIndexBuffer::CreateIndexBufferpGPUIndexBuffer
00788A40  IGPUInputAttribute::BuildInputAttribute
00788DB0  IGPUInputAttribute::CreateInputAttributepGPUInputAttribute
007861A0  IGPUSurface::AttachToOtherSurfaceFramebuffer
00786500  IGPUSurface::CreateSurface
00785C90  IGPUSurface::RegisterD3DSurface
007872F0  IGPUTexture::CreateTexture
00786DD0  IGPUTexture::ReleaseLevelSurfacesAttachToTexture
007885A0  IGPUVertexBuffer::CreateVertexBufferpGPUVertexBuffer
006DAA70  IPfxBaseContext::Initialize
006DAFB0  IPfxBaseContext::Uninitialize
006DB1B0  IPfxBaseContext::UninitializeDeviceResources
006E04F0  IPfxBaseRenderToTexture::Initialize
006E07A0  IPfxBaseRenderToTexture::Uninitialize
006DA990  IPfxContext::Instantiate
006E0470  IPfxRenderToTexture::Instantiate
0072A320  TEXSHADERSET::CreateEffect
0072D820  TEXSHADERSET::InitializeDevice
```

**SEVEN names are claimed by more than one function, covering 15 of the 137 rows** — marked above:
`CPostEffect::ApplyApertureFilter`, `::SetLensDistortionEnable`, `::SetRenderSceneLuminanceScale`,
`IGPUDevice::CreateSurface`, `::CreateTexture`, `::CreateVolumeTexture` (two functions each) and
`CTextureUtil::DrawRectGPU_MadT1_Sn` (three). An overload, a wrapper and its implementation, or a
routine emitted more than once; the string cannot distinguish them, and applying them mechanically
would produce duplicate names. **129 of the 137 names are unique; those 15 rows need a look first.**

*(Corrected in place: this paragraph first said "three names claimed by two functions each", which
confused two different counts — the **3** is the number of FUNCTIONS referencing several names, and
the collisions among NAMES are 7. Different quantities on opposite sides of the same mapping.)*

**NOT APPLIED AS NAMES.** This is evidence for the page that owns PPFX function identity, not a
rename. What the string proves is *which method reports this error*, which is strong; whether that
becomes the recorded name — and how the ~~three~~ seven collisions *(corrected 2026-10-02, OPUS: the count above)* resolve — is this page's call.

*Static: every `C*::`/`I*::`/`TEXSHADERSET::` method-name string in the image resolved to its VA and
matched against every RIP-relative operand in all listed function bodies. The same pass over
`[sead][!!error!!]` strings named 25 more functions in `18-Audio`.*

### An external check on the naming method (2026-09-19, OPUS)

The 137 names above come from the binary's own diagnostic strings. That method is only worth
something if a name it produces can be compared against a name somebody derived independently, and
four of the addresses in this set also appear in
[`the-post-processing-effect-catalogue.md`](the-post-processing-effect-catalogue.md), which named
them from **behaviour** — what the function does — before these strings were read.

| address | the catalogue's independent finding | the string's name | |
|---|---|---|---|
| `0072A320` | `TEXSHADERSET_CreateEffect`, derived from "load the effect, register 325 techniques and 36 uniforms" | `TEXSHADERSET::CreateEffect` | **agree, to the word** |
| `0078A120` | "`IGPUEffect::CreateEffectFromFile` wrapper" | `IGPUEffect::CreateEffect` | agree — the function is `CreateEffect` and it calls `CreateEffectFromFile` |
| `006DF480` | "the logger" | Yebis's printf wrapper | agree |
| `0072D820` | *unnamed* — recorded only as "its only caller" | `TEXSHADERSET::InitializeDevice` | **the string supplies a name the catalogue did not have** |

`0072A320` is the useful one. The catalogue reached `TEXSHADERSET_CreateEffect` by reading 13,547
bytes of behaviour, with no access to the name; the string says `TEXSHADERSET::CreateEffect`. Two
methods that share no evidence produced the same name, which is the check this table exists for.

**The sample is four.** Four agreements do not establish an error rate for the other 133, and no
rate is claimed here. What they do establish is that the method is not systematically wrong, which
a single disagreement would have refuted.

---

## `TEXSHADERSET`'s own layout — twelve arrays, from `CreateEffect`'s unrolled initialisation (2026-09-19, OPUS)

This page names `0072A320` as **`TEXSHADERSET::CreateEffect`** from its string, and describes it as
*"load the effect, register 325 techniques and 36 uniforms"*. **The 13,547-byte body also gives the
object's layout**, because it initialises its arrays by unrolled address arithmetic rather than a
loop, and each unrolled run states a base and a stride outright.

`CreateEffect` takes the object in `rcx` and works through `r14 = rcx + 8` (`0072A496`). Every
`lea r<n>, [r14 + disp]` with a displacement above `0x1000` falls into a clean arithmetic run:

| base (from `r14`) | terms seen | stride | span |
|---|---:|---:|---:|
| `+0x1714` | 3 | `0xB00` | 8,448 B |
| `+0x3294` | 3 | `0x580` | 4,224 B |
| `+0x4324` | 9 | `0x580` | 12,672 B |
| `+0x718C` | 9 | `0x58` | 792 B |
| `+0x74B0` | 3 | `0x58` | 264 B |
| `+0x7790` | 4 | `0x20` | 128 B |
| `+0x7858` | 5 | `0x2C0` | 3,520 B |
| `+0x9958` | 4 | `0x1600` | 22,528 B |
| `+0xE3F0` | 4 | `0x898` | 8,800 B |
| `+0xFE3C` | 15 | `0x84` | 1,980 B |
| `+0x1B0A0` | 5 | `0x2C0` | 3,520 B |
| `+0x1BED0` | **25** | `0x2C0` | 17,600 B |

**"Terms seen" is the number of unrolled `lea`s, which is a LOWER BOUND on the element count, not
the count.** An unrolled prologue followed by a loop would show only its prologue here. The
*strides* are exact — each run is an arithmetic progression with no gaps — and the strides are what
a reconstruction needs.

> **The object is at least ~~`0x220E0`~~ `0x221DC` bytes.** The highest displacement `CreateEffect` touches is
> ~~`+0x220DC`~~ `+0x221D0`, and that is through `r14 = rcx + 8`, so the allocation is at least ~~`0x220E4`~~ `0x221DC` from
> `rcx` *(corrected 2026-10-02, OPUS: `0072A320`+0x176 `lea r14, [rbx + 8]`, +0x34B8 `mov dword ptr [r14 + 0x221d0], eax`; the catalogue's `+0x221D8`)*. Three strides repeat — `0x580` twice, `0x2C0` three times, `0x58` twice — which is what a
> class holding several arrays of a few record types looks like.

### Why this is recorded here and not on the type it was first attributed to

**I initially attributed the `0x84` run to `ManagerSingleton0209BE80`**, because `+0xFE3C` and its
sixteen successors fall inside that type's declared extent and the pattern is strikingly coherent —
seventeen collinear displacements, sixteen of them the same instruction form. Every word of that
was true and none of it was evidence about that type. `CreateEffect` never loads
`*(void**)0x0209BE80` and touches none of its known fields; `lea r14, [rbx + 8]` makes its object
the caller's argument; and `+0x220DC` is twice that type's `0x10FD0`.

The splits were withdrawn — see
[`EVIDENCE-STANDARD` addendum bw](../../_index/EVIDENCE-STANDARD.md) — and the rule that came out
of it is the reason this section exists: **tie the FUNCTION to the type, not the number to the
extent.** Here the tie is positive and already on this page: the string in `CreateEffect`'s own
body names the class.

### The sibling: `FUN_001D6630`'s colour array belongs to a different object again

The same retraction covered a normalised-RGBA array whose arithmetic is correctly read —
`movsxd r10, edx` / `lea rdx, [r10+r10*2]` / `shl rdx, 5` is a **96-byte stride**, and the three
stored floats are byte components divided by the `255.0f` at `008C5B40` with a literal `1.0f`
fourth. Its object arrives as an argument through
`FUN_001D6170` → `FUN_001D5970` → `FUN_001D6630`, and **it is not `TEXSHADERSET` and not the
manager singleton** — it is identified, one level further up.

**`FUN_001D6000` loads it from the global `01F82C80`:**

```
001D6017  mov rbx, qword ptr [01F82C80]   ; the object
001D601E  mov rcx, rbx
001D6021  call 001D6040                    ; -> 001D6170 -> 001D5970 -> 001D6630
```

[`game-application.md`](../../00-Engine-Core-Runtime/Application-Root/game-application.md) already
carries that global in its ensure-singleton table: **`001D62D0` → `[01F82C80]`, allocation
`0xF778`** (≈ 63 KB), *"float-preset fields `0.2`/`-0.8`/`0.04`/`0.8`/`0.7`"*. So the colour array
belongs to that 63 KB singleton, and **the allocation size bounds the array the strides could
not**: from base `+0xC4F8` (50,424) there are `0xF778 - 0xC4F8 = 0x3280` = 12,928 bytes left, so
**at most 134 elements of 96 bytes fit**. The `+0xF738` cluster — ten qword stores of float
constants by `FUN_001D5970` — also lands inside that allocation, 0x40 bytes from its end, which is
consistent with the page's note about float presets.

> **The store has no type for `*(void**)0x01F82C80`.** A 63 KB singleton with a known allocator,
> a known ctor chain and at least two identified interior structures is a type candidate, and it
> is recorded as one rather than created here — naming it needs its own pass, not a footnote on a
> PPFX page.

*(OPUS 2026-09-19. Strides measured from the image; element counts deliberately given as lower
bounds. The class name is this page's, not mine — which is the whole point of putting the finding
on it.)*

## SWE2-EC7-61 update (2026-09-19) - `001D6630`

`001D6630` (338 B) is the `FUN_001D6630` colour-array writer the ppfx page names - call-free normalized-triplet store at `+0xC4F8` (verifies the page: a different object's array than `001D6370`'s `+0x92B8`). Interior anchor `001D666D` (the `+0xC4F8` normalized store).

## Cross-subsystem neighbours — SWE2-STRUCT (pass-22 dispositions)

- **CoreRuntimeScheduling - CLIENT (1 edge).** `001D62D0` is called by bodies filed to CoreRuntimeScheduling: `0017D4C0` - shared machinery across the layer boundary, no shared ownership.
- **Platform - SERVICE (2 edges).** `001D6040`, `001D6170` reach bodies filed to Platform: `005CC930` - shared machinery across the layer boundary, no shared ownership.

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-ppfx-function-identification-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `007911E0` | 72 B | when bit 31 of dword `+8` of `rdx` is clear, the dword is above 1 (unsigned) and qword `+0x10` is non-null, calls `00584730(qword +0x10)`; on every path then zeroes qword `+0x10` and dword `+8` of `rdx` and returns 1 in `al` | `007911F7`, `00791204`, `00791212`, `00791219`, `0079121D` |

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-ppfx-function-identification-ee-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `006FE080` | 215 B | stores `edx` to dword `[rcx+0x500]`; when byte `[rcx+0xd09]` is zero it stores `edx` to `+0x508` and returns it; otherwise it stores `edx` to `+0x504` and `+0x50c` and applies a step rule to it (a value equal to dword `+0x4d0` becomes dword `+0x4d4`, any other value is incremented and replaced by `+0x4d0` when it is unsigned above `+0x4d4` + dword `+0x36c` - 1), then when dword `+0xd10` is at least 2 (signed) it stores the result to `+0x504` and steps it again, then when dword `+0xd0c` equals 2 and qwords `+0xa88` and `+0x148` are both zero it stores the result to `+0x50c` and steps it again, and finally stores the result to `+0x508` and returns it in `eax` | `006FE093`, `006FE0CC`, `006FE0D8`, `006FE11E`, `006FE14C` |
| `00724F50` | 130 B | reads the dword counter `02EA198C` and, only when it is zero or its signed remainder modulo 100 equals 25 and the dwords `01F3BA80` and `01F3BA8C` are both non-zero, calls `006DF480(00D9C530, 0x1627)` and then `006DF480(00D9C368)` with `edx` as the first call left it; on every path it increments `02EA198C` and returns `0x80004001` | `00724F68`, `00724F7A`, `00724F9D`, `00724FA9`, `00724FC6` |
| `00724FF0` | 130 B | reads the dword counter `02EA1990` and, only when it is zero or its signed remainder modulo 100 equals 25 and the dwords `01F3BA80` and `01F3BA8C` are both non-zero, calls `006DF480(00D9CA20, 0x16d6)` and then `006DF480(00D9C578)` with `edx` as the first call left it; on every path it increments `02EA1990` and returns `0x80004001` | `00725008`, `0072501A`, `0072503D`, `00725049`, `00725066` |
