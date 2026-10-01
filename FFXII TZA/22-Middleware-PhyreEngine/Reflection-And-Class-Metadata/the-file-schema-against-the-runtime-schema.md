---
system: The file schema against the runtime schema — joining .phyre's own class table to the recovered field list
category: 22-Middleware-PhyreEngine
status: DOCUMENTED - was REOPENED; the trigger (the 2026-09-07 Route 1 error) is resolved (section 3b rewritten, CL-1 / CL-2 and SD-64..SD-67 answered), and a non-author falsification pass on 2026-10-01 SURVIVED (Route 4, all 21 descriptors live RTTI) (owner re-status 2026-10-01, OPUS, on SWE2-STRUCT's swe2struct-reopened3-0930)
owner_layer: CodeDomain:Middleware.PhyreEngine
evidence_tier: 3
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 1 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
corpus_validated: 169 of 35,984 .phyre files, 2026-09-03 — a partial corpus, and that limits every count here
last_reviewed: 2026-09-05
archive_formats:
  - "phyre | external | PhyreEngine is generic middleware and its container is documented outside this project; COMPLETION-PLAN.md §7 puts re-documenting it from the file side out of scope. What this build does with it is NOT deferred and is this document's subject — the class table each file carries, joined against the 682 field records recovered from the binary, with the 22 file-declared candidates accounted for (§3b and §7: 21 registered classes, CL-1; PContextSwitch a type-table entry, CL-2). ASSET-FORMATS.md §5 records the disposition and the obligation it carries."
audit:
  passes: 2
  last_pass: 2026-10-01
  last_pass_kind: falsification
  last_pass_state: swe2struct-falsification-2026-10-01 - Route 4 SURVIVED (22 bare, 21 descriptor, 21 accessor, 0 absent; all 21 descriptors live RTTI)
  crossref_clean: false
  reopened_count: 1
---

# The file schema against the runtime schema

> **This database has recovered 682 field records from the binary. Every `.phyre` file carries the
> same kind of table in plain text. Nobody had checked one against the other.** This does, and the
> disagreement is concentrated in one place.

**Evidence tier 9, deliberately.** Half of this rests on authored game data, which the
[evidence standard](../../_index/EVIDENCE-STANDARD.md) rates as *"proves authored intent, never
ownership"*. **That is not a caveat bolted on the end — it changes what the result means**, and §3
is built around it. *(Note 2026-09-30, SWE2-DATA: the front matter's `evidence_tier: 3` is the binary side, the qualified `PClassDescriptor*<T>` symbols of §3b; tier 9 is the authored file side. The page's claims carry whichever of the two they rest on.)*

## 1. What the player sees

Nothing directly. Indirectly: it is why a character, a texture or a shader can be a file on disk and
a working object in memory. The engine writes down its own field list, and the asset writes down
the field list it was built against. ~~**When those two disagree, an asset does not load.**~~
*Corrected 2026-10-01 (SWE2-STRUCT for OPUS):* a disagreement does not by itself stop a load.
- **The loader has a path for it.** For a file-declared entry with no native record, the cluster loader `0059AC00`
  builds a dynamic descriptor and dynamic members, through `006393A0` and `00632B30` (§7).
- **No shipped file takes that path.** All 527 file-declared members are registered statically (`SD-65`), so the
  two lists never disagree in the shipped data.
- **What the loader does refuse** is a different list: a wrong platform, a physics engine other than Bullet or none,
  and a truncated file. See [the cluster-header page](../Phyre-Asset-Container/the-cluster-header-and-what-the-loader-rejects.md).

## 2. Two schemas of the same thing

| | Source | Size |
|---|---|---|
| **runtime schema** | the member-registration call sites in `.text` — [the recovered field schema](member-registration-and-the-recovered-field-schema.md) | **682 records, 246 class names, 179 distinct leaves** |
| **file schema** | every `.phyre` file's own `PClassDescriptor` table, in plain ASCII | 4,502 distinct identifiers across 169 files |

The recovered names carry MSVC RTTI decoration — `V` for class (173), `U` for struct (4), `V?$` for
templates (2). Files declare the undecorated form. **Stripping that prefix is the entire
normalisation**, done explicitly rather than by fuzzy matching, because a loose matcher would
manufacture the agreement this join exists to test.

> **246 full names collapse to 179 leaves, and the collapse was checked rather than assumed.**
> **Only two leaves cover more than one full name** — `PArray` (66 instantiations) and `PSharray`
> (9). Both are templates, so collapsing them is correct: a file declares `PArray` once. **Had the
> normaliser been merging distinct classes, this is where it would have shown.**

## 3. The join, and the 22

**Class level: 64 of 179 recovered classes are declared by a file in this corpus.** The other 115
are **not a finding** — the corpus is 169 files, overwhelmingly one character's assets.

**The interesting direction is the other one.** Names a file declares that the recovery never
produced. A first pass reported **72**, and that number was wrong: the filter was `^P[A-Z]`, which
catches a great deal that is not a class. Classified:

| | count | what they are |
|---|---:|---|
| not class names | **27** | shader semantics (`POSITION`, `POSITION_MORPH`), pixel-shader entry points (`PS_Blur`, `PS_Combine`), shader parameters (`PS2ZBias`, `PS2WHMatrix`), and fragments the identifier regex mis-cut (`PDXd`, `PINn`, `PY_`) |
| primitive types | **8** | `PChar`, `PInt32`, `PUInt8/16/32`, `PString`, `PMatrix4`, `PMatrix4x3` |
| enum types | **7** | `PLightType`, `PLODBlendType`, `PLODMetricType`, `PRenderDataType`, `PSceneRenderPassType`, `PShadowCasterType`, `PTextureFormatBase` |
| Base-suffix variants | **8** | §4 — not misses at all |
| **candidate gaps** | **22** | below |

```
PShaderVertexProgram    PShaderFragmentProgram    PShaderFragmentProgramD3D11
PShaderGeometryProgram  PShaderGeometryProgramD3D11  PShaderComputeProgram
PShaderProgramBase      PShaderPassParameterLocationTypesBase
PShaderPassParameterLocationTypesConstantBuffer
PTexture2DD3D11         PTextureCubeMapD3D11      PSamplerStateD3D11
PStreamInputLayoutD3D11 PDataBlockBufferD3D11     PIndexDataBlockBufferD3D11
PBase   PClassDescriptor   PContextSwitch   PNodeContext
PMaterialSet   PMeshSegmentContext   PMeshInstanceSegmentContext
```

> **The coherence is what makes these credible.** Fifteen of the twenty-two are **shader programs
> and D3D11 resource classes.** A random scatter of names would suggest a broken filter; a clean
> concentration in one subsystem suggests a real boundary.

**And two readings of that boundary are available. This document does not choose between them:**
*(Pointer 2026-10-01 (SWE2-STRUCT for OPUS): §3b chooses. Reading 2 is dead for 21 of the 22, and `CL-1` and `CL-2`
account for all 22; the falsification pass of 2026-10-01 below re-measures it.)*

1. **A gap in the recovery.** Those classes register their fields through a path the 682-call-site
   census never covered — a different registrar, or a module the census did not walk.
2. **They are not registered by this build at all.** The assets are cross-platform and carry a class
   table built elsewhere. **A file declaring `PShaderVertexProgram` proves the class exists in
   authored data — tier 9 proves authored intent, never ownership.** The PC binary may simply never
   register it.

**Reading 2 is the same shape as an inert field**: the bytes exist, the name is there, and the
shipped build does nothing with it.

## 3b. Four routes. Three fail, and the fourth settles it

> **REOPENED 2026-09-07.** The first version of this section said all three routes failed and
> concluded *"the question is not statically answerable."* **That conclusion was false**, and it
> rested on a Route 1 measurement that was simply wrong. Independently refuted by `xiionline-8d`
> and re-derived from the shipping image before this rewrite. The original claims are preserved
> in §8b so the path to the wrong answer stays visible.

**Route 1 — search the image for the class-name strings. *This was the error.***

The original table reported `ClusterHeader` → **0 strings, 18 recovered fields**, and built the
whole section on it. The image contains **18** occurrences of `ClusterHeader` and **6** of
`PClusterHeaderBase`, including three mangled class-descriptor symbols in `.data`:

```
?AV?$PClassDescriptorConcrete@VPClusterHeaderBase@PBinary@PSerialization@Phyre@@@Phyre@@
?AV?$PClassDescriptorAbstract@VPClusterHeaderBase@PBinary@PSerialization@Phyre@@@Phyre@@
?AV?$PClassDescriptorForType@VPClusterHeaderBase@PBinary@PSerialization@Phyre@@@Phyre@@
```

`ShaderVertexProgram`, also reported as 0, has **10**. Run correctly over all 22 candidates:

| route | result |
|---|---:|
| **bare name present in `.rdata` / `.data`** | **22 / 22** |
| **named as a template argument of `PClassDescriptor*<T>`** | **21 / 22** |
| **owns a `PObjectAccessor<class …>::Get` of its own** | **21 / 22** |
| **absent by all three** | **0 / 22** |

`PContextSwitch` is the single exception on the latter two, and only just: its accessor strings are
`PArray<class Phyre::PRendering::PContextSwitch const *,8>::Get` — accessors for an *array of* the
class, not for the class. It does carry a bare `PContextSwitch` string at `00D809C8`.

**So reading 2 of §3 — "the PC binary may never register it" — is dead for 21 of the 22.** A class
named by its own `PClassDescriptorConcrete` and reached by its own object accessor is registered.
The remaining question is not *whether* they are registered but *why the 682-call-site census
missed them*, ~~which is a recovery gap and is now `CL-1`~~. *(Corrected 2026-09-30, SWE2-DATA, from `CL-1` (answered 2026-09-14, corrected 2026-09-26): the census misses nothing it counts, so these are not recovery gaps. Fifteen of the 21 register no data member through any of the five member routes. Five register one array member, which the census did not count per class. `PShaderPassParameterLocationTypesBase` registers two through `00632A70`. See §7.)*

**Why the search failed, and it caught the auditor too.** Phyre does not emit RTTI for the class;
it emits RTTI for **`PClassDescriptor*<TheClass>`**, so the class name appears as a *template
argument*, never as a bare `.?AVPClusterHeaderBase@…` type descriptor. `xiionline-8d`'s first
attempt searched the direct form, found 2 of 22, and was about to file a narrow partial correction.
**The control refused it:** of the 18 classes this document says *are* recovered, only **one** has a
direct RTTI descriptor, and the image holds 40 `@Phyre@@` descriptors against 246 class names.

> **A search that finds 1 of 18 known positives cannot support a negative.** Both wrong answers —
> the original section and the audit that nearly replaced it — came from searching for a name in
> the form we expected it to be written, without first proving the search can find names that are
> known to be there.

**Route 2 — census the class descriptor objects. Still impossible statically, and unaffected.**
The 246 descriptors span `02CA9DA0`–`02EBA030` and every one reads as zeroes in the shipped image *(anchored 2026-09-30, SWE2-DATA: the whole span lies past the end of `.data`'s raw bytes, in the zero-filled virtual tail. All 249 class-descriptor globals the current field schema names are there, `_index/candidates/dd-data-2-0930/schema_checks.py` S1, S2, control C1)*:
uninitialised globals constructed at run time, which is why registration sits inside one-time-init
guards. There is no object to inspect until the process runs. **This route was sound and remains so.**

**Route 3 — the registrar level. Still fails, and for the reason originally given.**
Of the **315 class registrars**, **142 register no named field**. Testing all 22 against the 741
strings those registrars reference gives **0 of 22** — because those strings are member and
script-binding names (`FindEntityForObject`, `addChild`, `GetGlobalTime`). **The registrars do not
reference their own class name.** Sound, and it is now the pointer to `CL-1` rather than to a dead
end: §11 of the sibling document is the right place to look, and it was tested with the wrong names.

**Route 4 — the qualified symbols themselves. This is the one that works.** The mangled
`PClassDescriptor*<T>` and `PObjectAccessor<T>` symbols are tier-3 evidence, present in the shipped
image, and they answer the question directly for 21 of 22 without needing the process to run.

## 4. The `Base` trap — eight false misses

**Eight names look like gaps and are not:**

| file declares | recovery has |
|---|---|
| `PClusterHeader` | `PClusterHeaderBase` |
| `PDataBlock` | `PDataBlockBase` |
| `PIndexDataBlock` | `PIndexDataBlockBase` |
| `PMeshSegment` | `PMeshSegmentBase` |
| `PSamplerState` | `PSamplerStateBase` |
| `PShaderPass` | `PShaderPassBase` |
| `PTexture2D` | `PTexture2DBase` |
| `PTextureCubeMap` | `PTextureCubeMapBase` |

**The recovery names the abstract base; the file declares the concrete type.** Anyone joining these
two sources without this table will read eight matches as eight misses — an 11 % error on the gap
count, in the direction that invents work.

## 5. Method, and what it cannot do

**Corpus scan.** NUL-terminated ASCII identifiers of 3–63 characters, from every `.phyre` on disk.
Reproducible: `Tools/work/h94/scripts/phyre_join.py`.

**Member matching is UNATTRIBUTED, and this is the method's real limit.** A string scan says the
name `m_width` occurs in a file. **It does not say which class declares it.** Attributing members to
classes requires parsing the `PClassDescriptor` structure, which this does not do — so no per-class
field comparison has been made, and the headline result is **class-level only**. The unattributed
member figure is deliberately not printed as a percentage beside the class one, because two numbers
side by side get read as one check.
*(Pointer 2026-10-01 (SWE2-STRUCT for OPUS): this limit was the scanner's, and it is lifted elsewhere.*
- *Members are stored in class order: class i owns the next `w3` member records (§7; [the packed-namespace page](../Phyre-Asset-Container/the-packed-namespace-and-the-file-side-schema.md) §8).*
- *The per-class comparison has been made: 527 of 527 file-declared members are registered statically (`SD-65`).)*

**The corpus is 169 of 35,984 files** — and skewed: 70 textures, 13 shaders, and only **6 meshes
against 2,097 in the archive.** Mesh, animation and physics classes are under-represented by
construction. Extracting a stratified sample would move every count here.

## 6. Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Does the leaf normaliser merge distinct classes? | **Checked.** 246 full names → 179 leaves, and **only 2 leaves cover more than one name**: `PArray` and `PSharray`, both templates. Correct behaviour, not collision. |
| Is "72 gaps" real? | **No, and it was this document's own first answer.** 27 are not class names, 8 primitives, 7 enums, 8 naming variants. **22 survive.** The `^P[A-Z]` filter was too loose and shader semantics beginning with P walked straight through it. |
| Are the 22 gaps in the recovery, or classes this build never registers? | **ANSWERED 2026-09-07, against this row.** They are ~~**recovery gaps**~~ *(not recovery gaps: `CL-1`, SWE2-DATA 2026-09-30)* for 21 of 22 — each is named by its own `PClassDescriptor*<T>` symbol and reached by its own object accessor. `PContextSwitch` alone is unsettled (`CL-2`). This row's "not established" was correct only while Route 1 was believed. |
| Is the member-level agreement being passed off as a per-class check? | **No** — it is unattributed and labelled so in the script, its docstring and §5. |
| Is "the string search will settle it" true? | **Yes, and this row was the document's worst error.** `PClusterHeaderBase` has **6** strings, not 0, and `ClusterHeader` **18**. The `PMeshInstance` control proved only that the search finds *one* name — not that it finds names in the form Phyre actually writes them, which is as a template argument of `PClassDescriptor*<T>`. **A control that passes on one known positive licenses nothing.** See §3b and §8b. |
| Would a bigger corpus change the numbers? | **Yes, and in a known direction.** 115 recovered classes unseen is an artefact of 169 files; 6 meshes against 2,097 guarantees mesh classes are under-counted. |
| Is the `Base` mapping real or coincidence? | Eight pairs, each differing by exactly the suffix `Base`, each the abstract/concrete pair the naming convention predicts. **Not one is a near-miss on some other name.** |

## 7. What is not known

> *Corpus 2026-09-12 (FABLE), for the row "would a bigger corpus change the numbers": yes, as
> predicted.* All 35,984 namespaces give **177 class names** (138 in `phyre-field-schema.tsv`) and
> **349 field names** (262 in it) against the 169-file 107 / 236, and **every one of the 545 names
> is a NUL-terminated string in `FFXII_TZA.exe`**. The 39 classes outside the recovered dataset are
> mostly field-less leaves and the D3D11 / array-holder classes, the 87 fields mostly array members
> and D3D11 structure fields — the same boundary as the 22 / 47, at scale (`CW-3`, `CW-4`).
> *(2026-09-26 (FABLE, Claude Opus 5.5), `CW-3`: the boundary is a limit of the census, not of the engine. The schema counts one
> member registrar; all 85 corpus field names it lacks are registered through the array-member registrar and two
> other variants. See [the packed-namespace page](../Phyre-Asset-Container/the-packed-namespace-and-the-file-side-schema.md) §2.)*

~~Whether the 22 are recovery gaps or unregistered classes.~~ **Closed 2026-09-07: ~~recovery gaps,~~
~~21 of 22~~ registered, 21 of 22**, on tier-3 qualified symbols — see §3b. *(`CL-1` since: not gaps in the recovery. SWE2-DATA 2026-09-30.)* Two questions replace it:
**`CL-1`** — why the 682-call-site census misses 21 classes that carry both descriptor RTTI and
object accessors; §11 of the sibling document (*142 registrars with no named field*) is the right
place, and it was tested with the wrong name form.
> *Narrowed 2026-09-12 (FABLE):* the census is not short of call sites — a raw `E8`/`E9` index of the
> whole `.text`, independent of the function list, finds exactly **682** sites for
> `PClassDataMember_Register` (`00632960`), all inside listed functions, none in the code the list
> does not cover. So the 21 classes do not register members through `00632960` from anywhere in the
> image; their members must arrive through a different registrar (the `PClassDataMemberArrayDynamic`
> constructors the vtable index lists are the candidates), which is where the next test belongs.
>
> **`CL-1` ANSWERED 2026-09-14 (FABLE): the census misses nothing it counts. ~~Sixteen~~ *(corrected (FABLE, Claude Opus 5.5, 2026-09-26): fifteen;
> see the correction below)* of the 21 register no data member,
> and five register one array member, which the census does not count per class.**
>
> **Method.** For each class, its class-descriptor global was taken from its own `PClassDescriptor*<T>` RTTI: the
> static initialiser stores that vtable into the global. Every call to the field registrar `00632960` and to the
> array-member registrar `00632A10` was then resolved to the descriptor it passes in `rdx`. Each call site was
> disassembled from its owner's entry, tracking non-volatile registers and the lazy descriptor accessors.
> **All 165 `00632A10` sites and 680 of the 682 `00632960` sites resolve**, the same 680 the census resolves.
> **Controls:** `PClusterHeaderBase` resolves to 18 fields and `PLight` to 10, matching the census rows for their
> descriptors.
>
> | of the 21 | field registrations | array members | a name-map registration (`006388C0`) |
> |---|---:|---:|---|
> | **16:** the thirteen shader-program and D3D11 classes other than the two in the next row, plus `PBase`, `PClassDescriptor` and `PMeshSegmentContext` *(corrected (FABLE, Claude Opus 5.5, 2026-09-26): 15 — `PShaderPassParameterLocationTypesBase` registers two members, below)* | **0** | **0** | all but `PBase` (none found) |
> | **5:** `PShaderPassParameterLocationTypesConstantBuffer`, `PStreamInputLayoutD3D11`, `PNodeContext`, `PMaterialSet`, `PMeshInstanceSegmentContext` | **0** | **1 each** | all five |
>
> `PContextSwitch`, the 22nd, has no descriptor global, as §3b already found.
>
> **Why the census could not see them.** It has one row per direct call to `00632960`. A class with no data member
> has no such call. An array member is registered by `00632A10`, which calls `00632960` once from inside its own
> body, so the census never has a caller that names the class.
>
> **The shape, in one example.** `PShaderVertexProgram`'s descriptor constructor `005DB720` hands `00632D80` an
> instance size of `0x98` and, as its base chain, the descriptor of `PShaderVertexProgramD3D11` (`02CF1940`). The
> D3D11 base does register a field. The class's registrar `005D3250` makes only the name-map insert and the shared
> finaliser call.
>
> **So the earlier guess is withdrawn:** ~~these classes do not have members arriving through a different
> registrar. The platform-neutral classes carry no reflected members of their own,~~ *(corrected below)* and the
> five array holders carry one each. Whether a file's declaration of these classes lists members this build does
> not register is a separate question, and it is not asked here (**`SD-65`**, SWE2-DATA 2026-09-30).
>
> **Corrected (FABLE, Claude Opus 5.5, 2026-09-26): one of the sixteen does register members, through a registrar CL-1 did not resolve.**
> CL-1 resolved the sites of two registrars. ASTRA's [phyre-array-registration-sentinel](../../_experiments/evidence/phyre-array-registration-sentinel/README.md) showed that a direct count's
> zero is not proof of no registration by another route. So the count was repeated over **every** route that reaches
> the member record base `00632FB0` (E8 or E9) with the descriptor passed through unchanged. There are five:
> - `00632960` (`PClassDataMember`), 680 sites;
> - `00632A10` (array), 165 sites;
> - `00632A70`, 29 sites;
> - `00632BE0`, 21 sites;
> - `00632B30` (`PClassDataMemberDynamic`), 1 site.
>
> All 895 sites outside those five resolve to a descriptor except the one `00632B30` site, whose descriptor is its
> caller's `this`. Direct callers of `00632FB0` that load their own `rdx` build other named objects and are not member
> registrars.
> - **`PShaderPassParameterLocationTypesBase` registers two members** through `00632A70`: `m_parameterStart` at
>   `005EA16A` and `m_parameterCount` at `005EA1E3`, both inside its guarded registrar `005EA0E0`. The field
>   schema and the type store already carry both rows (`phyre-field-schema.tsv`, `_types/fields.tsv`). Only this
>   answer's prose was behind them.
> - **The other fifteen register nothing through any of the five**, `PBase` and `PClassDescriptor` included. Their
>   descriptors are `02CF8270` and `02CF8470`, from the static initialisers `00164180` and `00163E30`.
> - **The five array holders still carry one each**, and the controls reproduce the counts: `PLight` 10 and
>   `PClusterHeaderBase` 18.
> - **A member can also be added at load time.** `00632B30` is called only from `006393A0`, a descriptor method,
>   and `006393A0` only from the cluster loader `0059AC00` (at `0059AEA7`). That pass builds dynamic descriptors
>   and dynamic members for file-declared entries with no native record. ~~**Which shipped classes take
>   it is not established here**~~ *(`SD-65` answered 2026-09-30, OPUS `49f9a523b`: **none** — across all
>   35,984 files the loader's dynamic-class flag `w7` bit 0 is set on 0 records, and 527/527 file-declared
>   members are registered statically)* (**`SD-65`**, SWE2-DATA 2026-09-30). "Registers no data member" therefore means *no static registration*, not "the
>   loaded class never has one" — though for every shipped file the two coincide.
>
> **Limits that stand:**
> - ~~A registration that calls a descriptor's attach slot (`+0x40`) without any of the five kinds is not swept~~
>   *(**`SD-66`** answered 2026-09-30, OPUS `ba2580021`, narrowed on `auditsem-review-dd-owner-read-2-0930` §3:
>   yes — five bodies (19 calls) attach inline-built members through a static descriptor's `+0x40`, and every one
>   registers the reflection system's own metaclasses, not a game class. The candidate's table `02CF8580` is a
>   class descriptor — RTTI `PClassDescriptorWithoutDefaultConstructor<PClassDescriptorDynamic>`, answered
>   2026-09-14).*
> - Every static registration here sits under a one-time guard, and a site is not evidence that its guard ran in any
>   title or scene.
> - A file member's offset is not its native offset. For example, `PMeshInstanceSegmentContext`'s file record puts
>   `m_streamBindings` at file offset 0, while the native registration passes `+0x38` ([phyre-array-registration-sentinel](../../_experiments/evidence/phyre-array-registration-sentinel/README.md)).
>   ~~The native type and width stay OPUS's question~~ *(**`SD-67`** answered 2026-09-30, OPUS `aac0f6798`:
>   `m_streamBindings` is `Phyre::PSharray<const PRendering::PMeshInstanceSegmentStreamBinding *>`, 16 bytes at
>   native `+0x38` — the member-registration page §20 already carries `005E6860` passing offset `0x38`, kind 4,
>   element size 8).*
>
> Control: [`cl1_registrar_complete.py`](../../_index/candidates/cl1-registrar-complete/cl1_registrar_complete.py) (7 checks, FAILS 0). Its sensitivity check restricts the count to CL-1's two registrars and
> gets 0 for `PShaderPassParameterLocationTypesBase`, which is the defect.
**`CL-2`** — whether `PContextSwitch` is genuinely unregistered or carries a third name form.
Absence in two forms is weak evidence in a document whose central finding turned on an unexpected
form; it has a bare `.rdata` string at `00D809C8` and array-typed accessors only.
> **CL-2 answered 2026-09-12 (FABLE): it is not a class, so no class registration is missing.** In
> the shipped files `PContextSwitch` is a **type-table entry** — region A, beside `PUInt32`,
> `PChar`, `float`, `PLightType`, `PShadowCasterType` — in all 2,184 shader/mesh clusters that name
> it, and a **class record in none** (0 of 35,984); the only class that refers to it is
> `PArray<PContextSwitch *>`, whose element type it is (2,184 files). The same holds for the other
> enum-like names the type table carries (`PLightType`, `PShadowCasterType`, `PSceneRenderPassType`,
> `PRenderDataType`, `PLODMetricType`, `PLODBlendType`). PhyreEngine registers such types through the
> type path, not `PClassDescriptor*<T>`, which is exactly the observed pattern: a bare name string,
> array accessors, no descriptor RTTI. The 22nd "gap" was a category error; ~~21 recovery gaps stand~~ the other 21 are registered classes that `CL-1` accounts for *(SWE2-DATA 2026-09-30)*.

> **Supplement 2026-09-21 (FABLE) — the answer above holds for the file schema, and the runtime
> half now has a cause rather than a category.** `PContextSwitch` *is* a live C++ class in this
> image — base vtable `00D80EA8`, a constructor at `006B8590`, eight subclasses each with their own
> vtable and one static instance — so "not a class" is exactly right about the cluster corpus and
> should not be read as a statement about `.text`. Two things this row left loose are settled by
> [the context-switch axes and the shader-variant key](../Shader-Variant-Selection/the-context-switch-axes-and-the-variant-key.md):
> **the bare string at `00D809C8` is the name of an object freelist**, declared by the initializer
> `00167010` for `0x100` objects of `0x28` bytes (and a second pool for their names), not a
> registration artefact; and **no switch object is ever serialised**, because an asset names a
> switch and the loader resolves the name against a runtime registry, manufacturing a plain
> base-class instance through `006B89C0` for any name the engine does not implement. A class whose
> instances are resolved by name and never written to a cluster has nothing for a class descriptor
> to do — which is why the type path is the *right* registration for it, and not merely the
> observed one.
~~Which class declares which member in a~~
~~file.~~ ~~What the 27 non-class names are for beyond "shader-side identifiers"~~ *(`SD-64` answered 2026-09-30, OPUS `02d334dbe`: they are string payload, not schema entries — `PS2*`/`PTAlphaThreshold` in `PShaderParameterDefinition::m_name`, `POSITION` in `PShaderStreamDefinition::m_name` / `PStreamInputDescD3D11::m_semantic`, `PS_*` entry points in `PShaderPassInfo::m_fragmentEntryPoint`, `POSITION_MORPH`/`PROCEDURAL_TEXTURE_ENABLED` in `PMaterialSwitch::m_name`; none sits in any file table)*. ~~Whether the full 35,984~~
~~corpus contains classes absent from all 169 files read here. Why the recovery's coverage falls off~~
~~precisely at the shader and D3D11-resource boundary.~~ *(Corrected 2026-09-30, SWE2-DATA: three of the four are answered. Members are stored in class order, and class *i* owns the next `w3` member records ([the packed-namespace page](../Phyre-Asset-Container/the-packed-namespace-and-the-file-side-schema.md) §8). The full corpus declares 177 class names against the sample's 107 (`CW-4`). The fall-off is a limit of the census, which counts one member registrar (`CW-3`). The non-class names are `SD-64`, since answered on the item above.)*

## Key addresses (SWE2-DATA, 2026-09-30)

| address | what | where on this page |
|---|---|---|
| `00632FB0` | the member-record base every member route reaches | §7, `CL-1` |
| `00632960` / `00632A10` / `00632A70` / `00632BE0` / `00632B30` | the five member routes (plain, array, and three variants) | §7 |
| `00632B30` | the load-time dynamic-member route, reached only from a descriptor method the cluster loader runs | §7 |
| `02CA9DA0`–`02EBA030` | the class-descriptor globals, zero until run time | §3b Route 2 |
| `00D809C8` | the bare `PContextSwitch` string (a freelist name) | §7, `CL-2` |

## What is still open (SWE2-DATA, 2026-09-30)

- [x] ~~What the 27 non-class names of the 72-candidate list are for, beyond "shader-side identifiers".~~ **`SD-64` — answered 2026-09-30 (OPUS `02d334dbe`):** string payload of shader-parameter, stream, pass and material-switch objects — not file-schema entries.
- [x] ~~Which shipped classes take the load-time dynamic-member route, and whether a file declares members for a class
      that this build does not register statically.~~ **`SD-65` — answered 2026-09-30 (OPUS `49f9a523b`):** none — `w7` bit 0 set on 0 of all shipped records; 527/527 file-declared members are statically registered.
- [x] ~~Whether any registration reaches a descriptor's attach slot (`+0x40`) outside the five member routes.~~ **`SD-66` — answered 2026-09-30 (OPUS `ba2580021`):** yes — five bodies, 19 calls, all registering the reflection metaclasses (`02CF8580` is a class descriptor).
- [x] ~~The native type and width of `PMeshInstanceSegmentContext::m_streamBindings`: file offset 0, native `+0x38`.~~ **`SD-67` — answered 2026-09-30 (OPUS `aac0f6798`):** `PSharray<const PMeshInstanceSegmentStreamBinding *>`, 16 B at `+0x38`.

## Evidence (SWE2-DATA, 2026-09-30)

| claim | evidence | tier |
|---|---|---|
| file-side class and field names (107 / 236 in 169 files; 177 / 349 corpus-wide) | the shipped `.phyre` namespaces, §3 and §7 | 9 (authored) |
| 21 of 22 candidates are registered classes | qualified `PClassDescriptor*<T>` symbols and object accessors, §3b | 3 |
| the census misses nothing it counts | `CL-1`; `cl1_registrar_complete.py` (7 checks) | 1 |
| `PContextSwitch` is a type-table entry in files and a live class in `.text` | `CL-2`, the 2026-09-21 supplement | 9 / 1 |
| the descriptor globals are zero in the image | `_index/candidates/dd-data-2-0930/schema_checks.py` S1, S2, C1 | 1 |
| the `Base` mapping (eight pairs) | §4 | 9 |

## 8b. Superseded readings — the permanent record

**Believed 2026-09-05 and published, surviving one falsification pass:** that a search of the image
for the 22 class names returns nothing (`ClusterHeader` → 0 against 18 recovered fields), that all
three routes fail, and therefore that *"the question is not statically answerable"* and only tier-10
runtime enumeration could settle it.

**Now believed:** all 22 are present as bare strings, 21 of 22 carry their own
`PClassDescriptor*<T>` qualified symbol and their own `PObjectAccessor<T>::Get`, and the question is
answerable statically at tier 3.

**Why the wrong answer was reachable, and where the same mistake will be hiding.** The search was
run for the name in the form a reader expects it to be written — a bare or directly-mangled class
symbol. Phyre emits RTTI for the *descriptor template*, so the class name only ever appears as a
template argument. The document then validated the instrument on a single positive control
(`PMeshInstance`), which passed, and treated that as licence for a negative across 22 names.

> **The methodological finding, which outlives the correction:** §5 of this document specifies its
> corpus scanner reproducibly — sections, bounds, tool. §3b stated **no method at all** for its
> image-side search. **Every claim in this document that records its procedure is right, and the
> single claim that does not is the single one that was wrong.** That is not a coincidence worth
> explaining away; an unstated method is an unreviewable one.

A negative result needs its control to be *representative*, not merely present: of the 18 classes
this document says are recovered, only one has a direct RTTI descriptor, so a direct-form search
finds 1 of 18 known positives. **A search with 6 % recall on known positives cannot support a
negative**, and neither the original nor the first audit attempt measured that recall before
concluding.

## 8. Related

- [the recovered field schema](member-registration-and-the-recovered-field-schema.md) — the runtime
  half, 682 records, and now with `phyre-field-schema.tsv` published beside it
- [the class descriptor system](class-descriptor-and-metadata-system.md) — the 4,557 functions that
  describe the game's classes to itself
- `phyre-field-schema.tsv` — the companion data, `class_leaf` column added for this join

## Falsification pass 2026-10-01 (SWE2-STRUCT for OPUS)

*Run by a Claude session in the SWE2-STRUCT lane for OPUS, a non-author of this page. Record and checker:
[`swe2struct-reopened3-0930`](../../_index/candidates/swe2struct-reopened3-0930/README.md), [`p2_route4.py`](../../_index/candidates/swe2struct-reopened3-0930/p2_route4.py) (14 checks, FAILS 0).*

**Attack chosen: §3b's Route 4 table.** It is the claim the page's reopening turned on, and everything after it
rests on it: `CL-1`, `CL-2`, the 21 / 1 split, and the evidence row "21 of 22 candidates are registered classes".
The table says:
- all 22 candidate names are bare strings in `.rdata` / `.data`;
- 21 are the template argument of a `PClassDescriptor*<T>` RTTI symbol;
- 21 own a `PObjectAccessor<class … T …>::Get`;
- none is absent by all three;
- `PContextSwitch` is the one exception.

The killer looked for was a candidate whose descriptor symbol is a stray string rather than live RTTI, or a match
that came from a longer name. Both readings in §8b were wrong because their search had never been shown able to find
known positives.

**Method.** The certified image (`73461d08…`) was parsed directly, and every printable `.rdata` / `.data` string was
indexed. Three things were added that the table did not test:
1. **Live RTTI.** Each descriptor symbol must be a live type descriptor: its RVA must be held by a complete object
   locator in `.rdata`.
2. **Exact argument.** The template argument is matched exactly, between `@V` and `@`. So
   `PShaderFragmentProgram` cannot be credited with `PShaderFragmentProgramD3D11`'s symbol.
3. **Controls.**
   - `PClusterHeaderBase` and `PLight` are recovered classes, and they pass all four tests.
   - `PLightType`, a type-table entry, has no descriptor.
   - A fabricated name is absent by all three.
   - The live-RTTI test, run on 37 non-RTTI accessor strings, fires on none.

**Result: SURVIVED.**

| test | result | checks |
|---|---|---|
| bare name in `.rdata` / `.data` | **22 / 22** | F1 |
| template argument of `PClassDescriptor*<T>` | **21 / 22**, the exception `PContextSwitch` | F2, F8 |
| own `PObjectAccessor<class … T …>::Get` | **21 / 22**, the exception `PContextSwitch`, whose two accessors are for `PArray<… PContextSwitch const *,8>` | F3, F5 |
| absent by all three | **0 / 22** | F4 |
| the descriptor is live RTTI (held by a COL) | **21 / 21** (new) | F6, C5 |
| bare `PContextSwitch` at `00D809C8` | holds | F7 |

### The reopening trigger is resolved (SWE2-STRUCT for OPUS)

The page reopened on 2026-09-07, because §3b's first version rested on a wrong Route 1 measurement (*"0 strings"*)
and concluded that the question was not statically answerable. The trigger is resolved on the page:
- §3b was rewritten from the shipping image, and §8b keeps the superseded reading.
- `CL-1` (no class misses its members: 15 register none, 5 register one array member, and
  `PShaderPassParameterLocationTypesBase` registers two) and `CL-2` (`PContextSwitch` is a type-table entry) are
  answered.
- The four follow-ups `SD-64` to `SD-67` are answered.

This pass re-measures the corrected Route 1 and Route 4 figures, and they hold.

**Also corrected:** §1's *"When those two disagree, an asset does not load"*, which the page's own §7 contradicted.
The loader builds dynamic members for an unmatched file entry, and no shipped file has one (`SD-65`).

**What this pass did not attack:** the corpus counts of §3 and §7 (169 files; 177 / 349 corpus-wide), the eight
`Base` pairs of §4, and `cl1_registrar_complete.py`'s registrar census, which has its own control.
