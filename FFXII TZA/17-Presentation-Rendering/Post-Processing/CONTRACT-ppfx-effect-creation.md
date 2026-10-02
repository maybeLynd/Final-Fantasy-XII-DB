---
contract: load the PPFX shader-set effect from its compiled file and bind every technique and uniform it exposes to a handle slot, so that a failure here takes the whole post-processing layer down at once rather than per effect
category: 17-Presentation-Rendering
scope: operation
level: L2
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 17-Presentation-Rendering/Post-Processing/the-post-processing-effect-catalogue.md
entries: ["0072A320", "0072D820", "0078A120", "006DF480"]
registry_slots: []
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the body was decoded from the authority image on 2026-09-21 (OPUS) with capstone over its
    full 13,547-byte extent - 2,965 instructions - and every population figure below was RE-DERIVED
    from that decode rather than carried from the page: the direct-call census, the per-helper call
    counts, and the string census behind the catalogue. The caller was disassembled separately. The
    per-technique semantics remain the page's and are cited to it.
last_reviewed: 2026-09-21
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-29
  last_pass_state: opus-falsification-pass-1-2026-09-29-exe-73461d08
  crossref_clean: false
  reopened_count: 0
---

# Contract — PPFX shader-set effect creation

> **Scope, stated plainly because it is short of the system.** S-40 is *"post-processing — the Yebis
> effect catalogue"*, and the registry credits it with exactly one primary page. That page covers
> **one operation**: `TEXSHADERSET_CreateEffect`, which loads the compiled effect and binds its
> techniques and uniforms to handle slots. **It does not cover the pass chain** — what runs, in what
> order, against which targets — which lives on
> [the post-process passes page](../../22-Middleware-PhyreEngine/Post-Process-Chain/the-post-process-passes-and-their-shader-constants.md)
> in another category. So this contract is `scope: operation` and **S-40's contract cell should read
> SCOPE-SHORT, not MET.** Recording that is the point: the alternative was to call an
> initialisation contract a subsystem contract and quietly overclaim a verdict cell.
>
> **Provenance.** Everything in sections 2–5, 7, 9 and 10 is **NATIVE/STATIC**, decoded here on
> 2026-09-21. The catalogue's per-technique meanings are the page's. Section 13 is **empty**.

## 1. Purpose

Every post-processing effect the game can draw — depth of field, motion blur, bokeh, bloom, the
scatter and composite passes — is a *technique* inside one compiled shader effect. Before any of
them can run, that effect has to be loaded and each technique and each uniform looked up once and
kept as a handle. This is that step. It runs once, and if it fails **nothing in the layer draws**,
because there is no per-effect fallback: the failure is reported at the file, not at the technique.

## 2. Interface

| | |
|---|---|
| entry point(s) | `0072A320` `TEXSHADERSET_CreateEffect`, **13,547 B, 2,965 instructions** *(the database's working name; the authored log string inside it spells the C++ form)*, — the largest body this database has contracted. Interior: the first gated log call is `0072A383`, the descriptor staging call `0072A3A6` |
| calling convention | Microsoft x64, `this` in `rcx`. **One caller**: `0072D820` (396 B), at `0072D872`. |
| return type | `int`, an HRESULT-shaped code |
| return semantics | **0 is success.** The caller tests it at `0072D879` and, on non-zero, logs through `006DF480` with the source line `0x1084` and calls `0071B3C0` before abandoning the sequence. Inside, the same shape guards the file load: ~~`IGPUEffect::CreateEffectFromFile`~~ `IGPUEffect::CreateEffect` *(corrected 2026-10-02, OPUS: `0078A120`+0xEA logs that name)* via `0078A120` is called once and its failure is returned unchanged, so **the HRESULT a caller sees is the loader's, not this function's**. |
| callbacks / indirect dispatch | the caller continues into `call qword ptr [rax + 0x38]` at `0072D8D9` — a vtable slot on the object the previous step returned. That step is outside this operation. |

## 3. Types

**This operation binds handles into its own receiver and declares no type of its own here.** The
receiver is the `TEXSHADERSET` object in `rcx`; its handle layout is censused separately in
[`members/ppfx-handle-layout.tsv`](members/ppfx-handle-layout.tsv) and is not re-derived.

**A neighbouring type worth naming, because it is easy to confuse with this one.**
`PostProcessParamContext` (0x4A8, `_types`, lazy singleton at `[01F7F5F0]` allocated by `00193D50`)
is the **render-parameter block** — the per-effect switch bytes
[the render command list contract](../CONTRACT-render-command-list-and-graphics-handshake.md) reads
at `+0x198`, `+0x199`, `+0x19A`, `+0x180`, `+0x3E8` and `+0x49C`. **It is not the receiver here and
is not touched by this operation.** One is the compiled effect's handle table; the other is the
authored switches that decide whether a pass runs at all.

## 4. Preconditions · postconditions · invariants

**I-1 — ONE FILE, ONE FAILURE, NO PER-EFFECT FALLBACK.** The effect is loaded once through
`0078A120` and every one of the 325 techniques is a lookup inside it. There is no path that loads a
second file or continues with a partial set, so a load failure is total: **the layer is unavailable,
not degraded.**

**I-2 — THE CENSUS REPRODUCES EXACTLY, AND THAT IS THE CHECK.** Decoded from the image here:
**358 direct call sites to 22 distinct targets**, and the per-helper counts are
`00715C70`×91, `0072DCF0`×65, `007157A0`×48, `00719380`×40, `007182F0`×40, `0072EB20`×26,
`006DF480`×10, `00715CC0`×8, `0017D2E0`×8, `0072DFD0`×4, `0072DAC0`×3, `0072EC00`×3,
`0071A380`×2, `0072E5B0`×2. **Every figure matches the page's corrected table row for row**,
including its own falsification-pass correction from 364/24 to 358/22 — so that correction is
confirmed independently rather than taken on trust.

**CORRECTED 2026-09-29 (falsification pass 1): the census is right and its reading was not.** FABLE corrected the
catalogue page on 2026-09-18 (UQ-225). This contract, written on 2026-09-21, cited that page's table and **missed its
correction**, carrying the old reading into §6. Pass 1 re-derives the correction independently and extends it. The
counts reproduce exactly again, but **five of the fourteen targets are string utilities, not registration helpers**
(FABLE's four plus `00715CC0`, the resize the wrappers call with `len - 1` right after construction). Together they
account for **227 of the 332 sites**:
- `00715C70` ×91 releases a string buffer through the allocator's release slot (`006DA8A0`), skipping the shared
  empty sentinel;
- `007157A0` ×48 constructs a string from a C string (a strlen loop, then an allocation through `006DA880`);
- `00719380` ×40, `007182F0` ×40 and `00715CC0` ×8 are string copy and resize, classified by their callee shape
  (they were not read line by line).

None of the five reaches the effect's lookup slots. **Registration is the effect object's own vtable:**
- `call [rax+0x60]` 224 times inline (176 with a `tech_` literal in `rdx`), `call [rax+0x48]` 33 times, and
  `call [r8+0xC8]` 8 times;
- plus the wrappers `0072DCF0`, `0072EB20`, `0072DFD0` and `0072DAC0`, each of which reaches `+0x60` itself;
- plus `0072E5B0`, `0072E940` (technique names) and `0072EC00` (the `asamp2D_*` sampler arrays).

§6's line that called them "fourteen registration helpers" is struck there and kept as history.

**I-3 — 325 TECHNIQUES AND 36 UNIFORMS, COUNTED FROM THE BODY'S OWN STRING REFERENCES.** A sweep of
every RIP-relative `lea` in the extent yields 379 targets, 374 of which decode as printable `.rdata`
strings and 364 of which are distinct: **325 begin `tech_`** and the remaining 39 are 36 uniform
names plus `%s%d` and the two `..\src\GPU\GPUTextureUtil.cpp` source strings. The page's headline —
*"register 325 techniques and 36 uniforms"* — is exact.

**I-4 — THE COUNT ARGUMENT IS A VARIANT MULTIPLIER, SO THE HANDLE COUNT EXCEEDS THE NAME COUNT.**
The two helpers that take a count (`0072DCF0`, 65 sites; `0072EB20`, 26) register ~~*n* handles~~ *n* handles, *n* × 22 for `0072DCF0` *(corrected 2026-10-02, OPUS: `0072DCF0` formats `%s%d` for each counted variant (`0072DCF0`+0x90..+0xA4) and registers each one under all 22 suffixes of the table at `02EA2250` (`0072DCF0`+0x1EC `lea rdi, [02EA2250]`, +0x1F3 `lea esi, [rbp + 0x16]`))*, under
one name, and the literal at the call site says how many — observed ~~4, 8, 17 (`0x11`) and 25
(`0x19`)~~ **(CORRECTED 2026-09-29, falsification pass 1: that list was incomplete)**. The count arrives in `r9d`, as an
immediate or as `r15d + k`, with `r15d = 1` set once at `0072A85F` and incremented only after the last counted site.
Every one of the 91 sites resolves, and the full set is **1 (15 sites), 4 (2), 8 (42), 16 (6), 17 (8), 25 (5),
32 (4), 33 (8) and 64 (1)**. The two counted helpers therefore register **1,172 handles over 91 named sites**.
**A name census therefore under-counts the handles**, and any figure quoting "332 registrations" is counting call
sites, not slots. Since pass 1 it is not even counting registrations: see I-2's correction.

**I-5 — IN A RETAIL RUN THIS FUNCTION IS SILENT.** Every one of its 10 `006DF480` calls sits behind
`[01F3BA80]` **and** one of `[02EA0B40]` / `[01F3BA90]`. The strings are in the image and are never
printed, which is why the function must be identified from its `.rdata` and not from a log.

**Postcondition.** On success, every technique and uniform the compiled effect exposes has a handle
in the receiver and the caller proceeds to the vtable step at `0072D8D9`. On failure, the receiver
is left in whatever state the partial registration reached — **nothing observed unwinds it** — and
the caller abandons the sequence.

## 5. State

| | fields / globals | evidence |
|---|---|---|
| read | `[01F3BA80]` log master gate, `[02EA0B40]` verbose gate, `[01F3BA90]` error gate | the ten gated `006DF480` sites |
| written | handle slots in the receiver (see the members census) | the 22-target call census |
| allocated | no receiver storage of its own; the effect's storage belongs to the loader. **Transient name strings** are constructed around the lookups (`007157A0`, 48 sites) *(pass 1)* | `0078A120` is called once |
| deallocated | ~~nothing~~ **the transient name strings only** (`00715C70`, 91 sites; `00715360` once) *(pass 1)*. **No teardown path was found** for a partially registered receiver. | complete decode of the extent |

## 6. Relationships

```
0072D820 (396 B, the only caller)
   006DF480  "..\src\GPU\GPUTextureUtil.cpp(%d) : PPFX: "  line 0x1074
   006DF480  "==== TEXSHADERSET::CreateEffect() ===="
   0072A320  <- THIS OPERATION
   test eax, eax                                   0072D879
     non-zero -> 006DF480 line 0x1084 "Feb 18 2016 PPFX ERROR:" -> 0071B3C0
   call [rax + 0x38]                               0072D8D9   (outside this contract)
     non-zero -> 006DF480 line 0x1094 -> 0071B3C0

0072A320
   0078A120   IGPUEffect::CreateEffectFromFile wrapper, once   <- corrected 2026-10-02, OPUS - IGPUEffect::CreateEffect (0078A120+0xEA)
   ~~fourteen registration helpers, 332 of the 358 sites~~   (corrected, pass 1:)
   effect vtable lookups inline: [rax+0x60] x224, [rax+0x48] x33, [r8+0xC8] x8
   registration wrappers: 0072DCF0 x65, 0072EB20 x26 (both counted), 0072DFD0 x4, 0072DAC0 x3,
                          0072E5B0 x2, 0072E940 x1, 0072EC00 x3 (sampler arrays), 0071A380 x2
   string utilities: 00715C70 x91, 007157A0 x48, 00719380 x40, 007182F0 x40, 00715CC0 x8 (227 sites)
   006DF480 x10, sprintf x8, memset, a string release (00715360), the stack-cookie check   <- corrected 2026-10-02, OPUS - and single calls to 0078A530, 0078A960 and 0071B3C0 (0072A320+0x86, +0xBB, +0xEB): 22 direct targets in all
```

## 7. State transitions

| previous | resulting | condition |
|---|---|---|
| no effect | effect loaded, handles bound | `0078A120` returns 0 and every registration runs |
| no effect | **layer unavailable** | `0078A120` returns non-zero — returned unchanged, I-1 |
| partially bound | *(no transition)* | nothing unwinds a partial bind; see §5 |

## 8. Script · resource · event interactions

**The compiled effect file is the authored input** and the only one: the name and its
`_LUMINANCE_REMAP_S1.pso` companion are literals in the body. **No script verb reaches this
operation**; it runs from the caller's initialisation sequence.

**The suffix grammar is the authored contract between the shader build and this code** — `_Sn` for
*n* sampler/shader variants with the count passed as the argument, `_Tn` for texture-count variants,
`_TSn_n` for both, `_USNORM` for unsigned-normalised targets, and `_A`/`_R`/`_G`/`_B` per channel.
The uniform names carry their type in the prefix (`f`, `af`, `v`, `m44`, `am44`, `asamp2D`,
`asamp3D`). **Adding a variant means changing the count literal here as well as the shader**, which
is the coupling a reimplementation most needs to know.

## 9. Determinism

**RNG — none.** **Timing** — once, during initialisation, before any pass runs. **Threading** — no
lock, no atomic and no thread check appears in the extent; the operation is called from one site and
nothing observed makes it re-entrant.

## 10. Failure paths and edge conditions

1. **File load fails** → the HRESULT is returned unchanged and the caller aborts (I-1).
2. **A technique is absent from the compiled effect** → not distinguished here; the registration
   helpers' own failure behaviour is not read, and that is a limit of this contract rather than a
   statement that they cannot fail.
3. **Logging disabled** → the normal case; no diagnostic is emitted on any path (~~I-4~~ I-5 *(corrected 2026-10-02, OPUS: I-5 is the retail silence; I-4 is the count multiplier)*).
4. **Partial registration** → no unwind observed (§5).

## 11. Observable behaviour

- With the log gates set, the four `TEXSHADERSET::CreateEffect` lines and the `GPUTextureUtil.cpp`
  line numbers `0x1074` / `0x1084` / `0x1094` appear in order; in a retail run nothing appears.
- **The externally visible consequence of failure is total**: no post-processing draws at all. That
  is the differential test this contract most wants — force the loader to fail and confirm the layer
  is absent rather than degraded.
- The build date `Feb 18 2016` is in the error strings and identifies the middleware build.

## 12. Reproduction formula

```
CreateEffect(this):                                  # 0072A320
    if logMaster and verbose:
        log("..\\src\\GPU\\GPUTextureUtil.cpp(%d) : PPFX: ", 0x90B)
        log("==== TEXSHADERSET::CreateEffect() ====")
    hr = CreateEffectFromFile(device, <name>, "_LUMINANCE_REMAP_S1.pso", 0)   # via 0078A120   # <- corrected 2026-10-02, OPUS - 0078A120 is IGPUEffect::CreateEffect (0078A120+0xEA)
    if hr: log(" ... failed (0x%x: %s)"); return hr                            # I-1
    log(" ... succeeded"); log("get parameter handles ...")
    for each of the 325 technique names and 36 uniform names:
        if the helper takes a count: register <count> handles under the name   # I-4
        else:                        register one handle
    return 0
```

## 13. Runtime validation

**Empty. Nothing here has been observed on a running game**, and the log lines that would show it
are gated off in a retail build (I-5), so observing it needs the gates set rather than a normal run.

| claim | how it was observed live | date | result |
|---|---|---|---|
| — | — | — | — |

## 14. Unresolved

1. **Whether a registration helper can fail, and what happens if one does.** §10.2. Resolved by
   reading the fourteen helpers' bodies~~; none was read here~~. *(answered: see §10's pass 1 - five are string utilities and registration is the vtable; 2026-10-02, OPUS)*
2. **What the vtable step at `0072D8D9` is**, and whether it is part of the same initialisation
   contract. It is the caller's, and this contract stops at its own return.
3. **The handle count**, as opposed to the name count (I-4). **Partly resolved by pass 1:** the two counted helpers
   register 1,172 handles over their 91 sites. The whole operation's total still needs the loop bounds of
   `0072DFD0`, `0072DAC0`, `0072E5B0` and `0072EC00`, which were not resolved.

## 15. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| 358 direct sites, 22 targets, and the per-helper counts | capstone decode of the full 13,547-byte extent, 2,965 instructions, immediate-operand call census; interior anchors `0072A383` (the first gated `006DF480`) and `0072A3A6` (the `0078A530` descriptor stage) | 1 | PROVEN |
| 325 `tech_` names and 36 uniform names | every RIP-relative `lea` in the extent resolved and decoded — 379 targets, 374 printable, 364 distinct | 1 | PROVEN |
| One caller, and the failure shape | complete body of `0072D820` (396 B): `0072D872`, `0072D879`, the `0x1074`/`0x1084`/`0x1094` log lines | 1 | PROVEN |
| Logging is gated off in retail | the ten `006DF480` sites and their three gate globals | 1 | PROVEN |
| The suffix grammar and per-technique meanings | [the catalogue page](the-post-processing-effect-catalogue.md) §2.5 and §4 | carried, tier 1 at source | VERY HIGH |
| `PostProcessParamContext` is a different object | `_types`: 0x4A8, lazy singleton at `[01F7F5F0]` via `00193D50`; not referenced in this extent | 1 | PROVEN |

## 16. Parity plan

| dimension | tested how |
|---|---|
| **STRUCTURAL** | the name census and the per-helper call counts of I-2/I-3 |
| **CONTRACT** | I-1: assert a load failure is returned unchanged and nothing continues |
| **EDGE-CASE** | §10's four paths |
| **INTEGRATION** | the caller's sequence of §6, including that the vtable step is gated on this return |

**Not tested, and why:** **RNG**, **CALCULATION**, **SERIALIZATION** — none present.
**PRESENTATION** — what each technique draws is the shader's, not this operation's.
**TIMING** — once at initialisation; nothing finer is established.
**FULL SUBSYSTEM** — explicitly out of reach: this is one operation of S-40 and the pass chain is
not covered (see the header).

## Falsification pass 1 — 2026-09-29 (OPUS): the census holds, its reading does not

Every claim was re-derived from the shipping image (`73461d08…`) by
[`falsify_ppfx_effect_creation.py`](../../../Tools/analysis-kit/gfz-scripts/falsify_ppfx_effect_creation.py). Each check
states its killer first and then searches for it. `audit_crossrefs.py` ran on this folder first. Result: **ten checks
survive, one structural reading is corrected, and one list is completed.**

| check | killer searched for | result |
|---|---|---|
| P0 physical | an entry or extent that differs; an anchor that decodes otherwise | survives: 13,547 B / 2,965 instructions; caller 396 B; `0072A383`, `0072A3A6`, `0072D872`, `0072D879` and `0072D8D9` decode as cited |
| P1 I-1 | a second loader call, or a registration on the non-zero path | survives: one `0078A120` site (`0072A3D1`); the non-zero edge reaches `ret` in 41 instructions, calling only log, `0071B3C0` and the cookie check |
| P2 I-2 census | any count differs | survives: 358 sites, 22 targets, every per-target count |
| P3 I-3 strings | any count differs | survives: 379 / 374 / 364; 325 `tech_`; 36 uniforms plus `%s%d` and the two source strings |
| P4 I-4 counts | a counted site whose count is not an immediate or a resolvable `r15`-relative value; handles not exceeding names | survives, **list completed**: the values are {1, 4, 8, 16, 17, 25, 32, 33, 64}, giving 1,172 handles over 91 sites |
| P5 I-5 gating | a log call without `[01F3BA80]` and one of `[02EA0B40]` / `[01F3BA90]` in its 40 preceding instructions | survives: all 10 are gated |
| P6 one caller | another `call`/`jmp`, a RIP-relative reference, or a stored 8-byte pointer to `0072A320` anywhere in the image | survives: only `0072D872` |
| P7 §9 threading | a lock prefix, an `xchg` on memory, or a call through an import slot | survives: none |
| P8 §3 distinction | a reference to `[01F7F5F0]` or a call to `00193D50` | survives: none |
| P10 §12 | a first log line other than `0x90B` | survives |
| P11 §6 reading | a "string utility" reaching the lookup slots, or a wrapper that does not | **corrected**: see I-2. 227 of the 332 sites are string utilities; registration is the effect's vtable `+0x60` / `+0x48` / `[r8+0xC8]` |

**What was tried and did not break it:**
- whole-image reference scans for the entry (direct, RIP-relative and stored pointer);
- following the loader's failure edge instruction by instruction;
- resolving every count argument rather than sampling it.

**Crossref (audit_crossrefs, this folder):** two findings name `00193D50`'s ten callers (Presentation 9, Resource 1)
as unmentioned neighbours. `00193D50` is cited only in §3's *do not confuse with*, as the allocator of a different
object, and it is not a relationship of this operation. Those callers belong to the render-parameter block's owner,
[the render command list contract](../CONTRACT-render-command-list-and-graphics-handshake.md). `crossref_clean` stays
`false`, as recorded.

**Not attacked by this pass:**
- §8's suffix grammar and the per-technique meanings, which are the catalogue page's;
- the loop bounds of `0072DFD0`, `0072DAC0`, `0072E5B0` and `0072EC00` (§14.3);
- whether a lookup can fail (§14.1).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

**Resource — CLIENT, one edge, and it is the §3 distinction's object, not this contract's.** This page cites
`00193D50` only to rule it out: it is the lazy allocator of the `PostProcessParamContext` singleton at `[01F7F5F0]`,
the render-parameter block the console's HBAO toggles write. It is not the effect-creation path. Its one
resource-layer caller is `001A7A50` (597 B, filed `Resource`), which the arm catalogue lists among the engine
re-init code that reaches that block. That edge is the parameter block's consumer relationship, owned by the
catalogue pages (`arm-catalogue-slice-D-ids-108-139`). This contract creates no resource.

*Tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.*
