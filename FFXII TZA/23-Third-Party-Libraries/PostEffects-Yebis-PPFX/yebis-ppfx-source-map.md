---
system: Yebis / PPFX post-effects — the source map recovered from surviving assertion strings
category: 23-Third-Party-Libraries
owner_layer: CodeDomain — ThirdParty / CompilerGeneratedEH; no PrimaryOwner
status: AUDITED
evidence_tier: 2
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 45 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-02
audit:
  passes: 1
  last_pass: 2026-09-02
  last_pass_state: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  crossref_clean: true
  reopened_count: 0
origin: open question BK-3 — do the recovered PostEffects source paths map to further middleware structure
function_families:
  - "PPFX post-effect library | C | members/ppfx-span.tsv | 1598 | Yebis / PPFX post-effect library (Silicon Studio), statically linked, not FFXII code: every census entry from 006DA880 up to 007911E0 (exclusive) less 128 already dispositioned or foreign (14 A-measured, 113 in other declared families - including the 17 MSVC std::_Tree bodies the linker emitted inside the span, resolved for the ordered-container row 2026-09-16 - plus the import stubs and tail-call forwarders), one ICF-folded body whose RTTI is also Bullet's, and 0071F970, which Phyre framework code at 0079xxxx also calls (members/select_ppfx.py). Evidence: 465 entries lea a ..\src\ source path of the 25 files of sec.2.2 or a PPFX diagnostic, or sit at a PPFX:: vtable slot; the lower edge is PPFX's nesting-counter pair 006DA880 / 006DA8A0, the upper edge Phyre::PFramework descriptors at 007911E0. Controls: 44 outbound call targets, all CRT, math imports, MSVC string / container helpers or one PPFX-only initialiser; inbound callers only the integration client at 006Cxxxx, static initialisers and teardown thunks; shared .data globals only static-lifetime zones and the TLS index. Boundary: the library bodies; the integration client (006C9B20 onward) and the static-lifetime thunks are NOT covered 12 members left the family 2026-09-17, since measured as A (A beats a declaration): 006E9C20 and eleven more, dropped by re-running members/select_ppfx.py; a further member, 00769640, went A on the same-day re-sweep; and another, 0078A530, went A on 2026-09-17. 9 member(s) left the family 2026-09-29, since measured as A (A beats a declaration); every removed address and its reason is in _index/candidates/ec7-refused-family-repair-0929/removed-members.tsv. Re-derived by re-running members/select_ppfx.py, which now leaves the UC-1 frontier bodies out of its population (UC-1 series break 2026-09-28; unpatched, it admitted 733 of them); its output equals this file. 2026-09-30 (SWE2-EC7, GI re-status): 1 member left the family, since measured as A (A beats a declaration) after SWE2-FRONTIER c97af7156 re-statused the 13 GI pages PARTIAL -> DOCUMENTED; select_ppfx.py re-run on a clean HEAD export drops exactly that one and admits nothing; the members file is the selector's output. 2026-09-30 (SWE2-EC7, DD re-status A-drift, record _index/candidates/ec7-dd-adrift-pairing-0930): 8 member(s) left the family, since measured as A (A beats a declaration) after OPUS re-statused the MSVC ordered-container page (3dac81ee9) DOCUMENTED; the selector re-run on a clean HEAD export drops exactly these and admits nothing; the members file is the selector's output; addresses and causing pages in the record. 2026-10-01 (OPUS for SWE2-EC7, A-drift round 5, record _index/candidates/opus-adrift-round5-1001): 1 member(s) left the family, since measured as A (A beats a declaration) after OPUS re-statused the script VM interpreter page (56a49cc8c) DOCUMENTED; members/select_ppfx.py re-run on a clean HEAD export drops exactly it and admits nothing; the members file is the selector's output; addresses and causing pages in the record. 2026-10-01 (OPUS for SWE2-EC7, A-drift paired with owner re-status batch 15, record _index/candidates/opus-dd-restatus-15-1001): 2 member(s) left the family, since measured as A (A beats a declaration) after OPUS re-statused the text-element dispatch table page DOCUMENTED (owner batch 15); exact A removal in the same publish (selector not re-run); addresses and causing pages in the record."
  - "PPFX post-effect library, UC-1 bodies in its span | C | members/ppfx-span-uc1.tsv | 732 | not this game's code: the PPFX library's own bodies in its link span, declared apart from the parent row under FABLE family ruling R1 (4e32dd8df) by SWE2-EC7, record _index/candidates/ec7-uc1-span-rows-0929. 732 UC-1 bodies admitted to frontier 2026-09-28, dispositioned by span 2026-09-29. TEST 1: every member lies strictly inside 006DA880 up to 007911E0 with a listed PPFX member on each side. TEST 2: select_ppfx.py re-run with the span's 733 UC-1 bodies in its population admits all 733, its source-file and edge assertions hold, and its outbound, inbound and globals controls name the same targets and zones (one existing CRT target gains one caller). TEST 3: a raw reference index (every decoded body, a .text rel32/rel8 byte scan, DIR64 relocations, RVA cells) finds every reference to a member inside the span - 114 referenced, 617 referenced by nothing, none from game code - and every outside target a member reaches is one the listed PPFX members already reach. NOT covered: 2 UC-1 bodies of the span that RVA-valued data cells outside it match (possibly by coincidence, not excluded), which stay frontier. Generator: _index/candidates/ec7-uc1-span-rows-0929/uc1_span_tests.py --write. 2026-09-30 (SWE2-EC7, AUDITSEM-REQ-EC7-UC1-SPAN-00712180-0930): +1 member - the one 353-byte UC-1 body OPUS applied as frontier in the 257-up band (b6061b9f3), which uc1_band.py reads only since 9e90a97ea, so the 2026-09-29 run could not see it. It passes TEST 1 and TEST 3 (one reference, from inside the span); SWE2-AUDIT-SEM's TEST 2 re-run at HEAD admits it with the controls holding (_index/candidates/auditsem-review-uc1-span-ppfx-0930 section 4); the generator re-run on a clean HEAD export writes exactly this one more: 732 members, 115 referenced, 617 referenced by nothing."
---

# Yebis / PPFX post-effects — the recovered source map

> The release build reduced the assertion reporting function to a bare `return`. It could not
> delete the **arguments** already pushed at each call site — so the `__FILE__` pointer and the
> `__LINE__` number are still sitting in the code, at the exact place every assertion stood.
> **26 source paths and 1,857 call sites survive**, and they attribute **193 compiled functions to
> the source file they were written in.**

BK-3 asked whether 18 recovered paths map to further middleware structure. They do: there are
**26**, they reconstruct a four-directory source tree, and the attribution reaches **188 functions
the RTTI recovery could not name**.

## 1. What the player sees

The glow.

FFXII: The Zodiac Age looks markedly different from the 2006 original, and the most obvious part of
that is the light: sunbeams that bloom when you step out of a cave, the soft halo around a summon's
charge, the way the background goes gently out of focus during a close conversation. That layer is
not Square Enix's own code. It is **Yebis**, a post-effects package licensed from Silicon Studio, and
the remaster runs the whole image through it every frame.

This document recovers the shape of that package from the inside — which of its source files each
piece of compiled code came from — using text the developers never meant to ship. Every time a Yebis
programmer wrote a sanity check, the compiler recorded the file name and line number next to it. The
release build removed the code that would have printed them. It left the file names.

So: **the depth-of-field code is 22 functions from one file, the glare code 19 from another**, and a
modder who wants to change how FFXII blooms now knows exactly where to look.

## 2. Native mechanism

### 2.1 Why the strings survived

An assertion compiles to roughly:

```c
if (!condition)
    Report(__FILE__, __LINE__, ...);     /* Report reduced to `ret` in release */
```

The linker can fold `Report` down to a bare return — and this binary does exactly that, onto the
same three-byte `ret 0` that `/OPT:ICF` collapsed some 273 `ret`-bodied functions onto. What it
cannot do is delete the argument set-up at each call site, because that code is inside the caller.
So each surviving site still contains:

- a `lea` of the `__FILE__` string, and
- a `mov <reg>, imm` carrying `__LINE__`.

**~~1,857 such sites survive across 940 functions.~~** **363 such sites survive across 193 functions**; the other 1,494 sites, in 747 functions, are `PhyreScripting.inl`'s (§2.5) *(corrected 2026-10-02, OPUS: `lea` references to the 25 PPFX path strings counted at the image)*. They are authored evidence — the file names are
what a Silicon Studio engineer typed — and they are tier 2 in this database's hierarchy.

### 2.2 The recovered source tree

```
..\src\                            ppfx.cpp · ppfxRenderToTexture.cpp
..\src\GPU\                        19 files  (below)
..\src\GPU\TinyEffect\             TinyEffect.cpp · TFXString.cpp
..\src\UT\                         ppfxLicense.cpp
```

and two absolute paths that name the **build machines**:

```
d:\bamboo\build\yeblic-ppfxlic-bl2015\src\gpu\GPUClassUtil.h
e:\jenkins\workspace\c11019p16003\middleware\phyreengine\include\Scripting/PhyreScripting.inl
```

**Two different middleware vendors, two different CI systems.** Yebis/PPFX was built under
**Atlassian Bamboo** in a workspace named `yeblic-ppfxlic-bl2015` — *yebis licensed*, *ppfx
licensed*, *build 2015* — and PhyreEngine under **Jenkins** in `c11019p16003`. The relative
`..\src\` form of every other PPFX path says those files were compiled with a working directory one
level below `src`, which is why only the two headers pulled in from elsewhere kept their full paths.

### 2.3 The file-to-function map

| source file | functions | distinct `__LINE__` values | sites |
|---|---:|---:|---:|
| `..\src\GPU\GPUDepthOfField.cpp` | **22** | 59 | 75 |
| `..\src\GPU\TinyEffect\TFXString.cpp` | 20 | 6 | 30 |
| `..\src\GPU\GPUPostEffect.cpp` | 19 | 35 | 48 |
| `..\src\GPU\GPURenderGlare.cpp` | 19 | 25 | 39 |
| `..\src\GPU\TinyEffect\TinyEffect.cpp` | 18 | 19 | 21 |
| `…\src\gpu\GPUClassUtil.h` | 15 | 1 | 20 |
| `..\src\GPU\GPURenderTexture.cpp` | 10 | 17 | 20 |
| `..\src\ppfx.cpp` | 8 | 7 | 9 |
| `..\src\GPU\GPUInterfaceBuffer.cpp` | 8 | 10 | 10 |
| `..\src\GPU\GPUTextureUtil.cpp` | 7 | 20 | 20 |
| `..\src\GPU\GPUInterfaceTexture.cpp` | 7 | 5 | 7 |
| `..\src\GPU\GPURenderTextureArray.cpp` | 5 | 6 | 8 |
| `..\src\GPU\GPUTextureLuminance.cpp` | 5 | 6 | 7 |
| `..\src\GPU\GPUInterfaceSurface.cpp` | 5 | 4 | 5 |
| `..\src\ppfxRenderToTexture.cpp` | 4 | 2 | 4 |
| `..\src\UT\ppfxLicense.cpp` | 4 | 9 | 10 |
| `..\src\GPU\GPUInterfaceEffect.cpp` | 4 | 3 | 4 |
| `..\src\GPU\GPURenderTexturePool.cpp` | 3 | 4 | 5 |
| `..\src\GPU\GPUGlareDef.cpp` | 3 | 3 | 3 |
| `..\src\GPU\GPUInterfaceDevice.cpp` · `GPUInterfaceQuery.cpp` | 2 each | 2 | 2 |
| `GPUMath.cpp` · `GPUUtil.cpp` · `GPUResourceManage.cpp` · `GPUInterfaceResource.cpp` | 1 each | ≤11 | 1–11 |

**193 functions, 192 of them attributable to exactly one file.** The single exception references two,
which is what inlining across a header boundary looks like.

The shape of the package is legible from the file names alone: a thin public layer (`ppfx.cpp`), a
GPU abstraction with an `IGPUInterface*` family per resource kind, concrete render-target management
(`GPURenderTexture*`, three files including a **pool**), the effects themselves (depth of field,
glare, luminance, post-effect), a small embedded shader/effect system (`TinyEffect`), and a licence
check.

### 2.4 The licence file is in the shipped binary

`..\src\UT\ppfxLicense.cpp` contributes **4 functions and 9 distinct assertion lines**. Yebis is
licensed middleware and its licence validation is compiled into the retail game. The build workspace
name says the same thing twice — `yeb**lic**-ppfx**lic**`.

### 2.5 The Phyre path is a different animal

`PhyreScripting.inl` is referenced **1,494 times from 747 distinct functions**, and **not one of them
is also a PPFX referencer** — the two sets are disjoint. Its sites carry **no recoverable `__LINE__`
constant**, which is what distinguishes it from the assertion pattern: this is one header included
into 747 generated scripting bindings, not 747 assertions. It is evidence about PhyreEngine's
scripting layer and belongs to that document, not this one.

## 3. Key addresses

| Address | What |
|---|---|
| `00D23FF0` | `…\middleware\phyreengine\include\Scripting/PhyreScripting.inl` — 1,494 sites, 747 functions |
| `00D8E4C0` | `..\src\ppfx.cpp` — first of 9 copies |
| `00D8FC48` | `..\src\ppfxRenderToTexture.cpp` |
| `00D90348` | `..\src\GPU\GPUMath.cpp` — 11 copies, one per assertion line |
| `00D90E50` | `..\src\GPU\GPUPostEffect.cpp` |
| `00D94ED0`, `00D94F50` | `d:\bamboo\build\yeblic-ppfxlic-bl2015\src\gpu\GPUClassUtil.h` — ~~the referenced copies~~ two of the six referenced copies, with `00DA7278`, `00DA72B8`, `00DAA000` and `00DAA040` *(corrected 2026-10-02, OPUS: `lea` references counted per copy, 20 sites in all; the other six copies are unreferenced)* |
| `0016D6A0` | the folded `ret 0` the assertion reporter collapsed onto |

The string blob runs from about `00D8E4C0` to `00DAC3F8` in `.rdata`. Individual paths appear in
**multiple copies** — `GPUDepthOfField.cpp` 67 times, `GPUPostEffect.cpp` 38 — because the compiler
emits one copy per translation-unit instance and `/OPT:ICF` did not fold them.

## 4. Data structures and formulas

There is no formula; the artefact is a string table and a call-site convention.

```
at each surviving assertion site, within a ±5-instruction window:

    lea   <reg>, [rip + disp]        ; -> the __FILE__ string in .rdata
    mov   <reg32>, imm               ; the __LINE__ number, 1 <= imm <= 30000
    call  <reporter>                 ; folded to 0016D6A0 (ret 0) in this build

recovered attribution:
    function F was compiled from source file S
      <=>  F's body contains a RIP-relative reference to S's string
```

**The `__LINE__` window is a heuristic and is stated as one.** A `mov reg, imm` within five
instructions of the `lea` is *usually* the line number, but nothing marks it as such. The file
attribution does not depend on it — the `lea` alone carries that — so a wrong line number cannot
corrupt the map.

## 5. Call chain

```
the frame's rendered image
  -> PPFX / Yebis post-effect chain
     ppfx.cpp                 public entry
       -> GPUInterface*.cpp   the GPU abstraction (device, buffer, texture, surface, query, effect)
       -> GPURenderTexture*   render targets, including a pool
       -> GPUDepthOfField.cpp · GPURenderGlare.cpp · GPUTextureLuminance.cpp · GPUPostEffect.cpp
       -> TinyEffect/         embedded shader-effect system
       -> ppfxLicense.cpp     licence validation, shipped
```

**Upstream:** the renderer. **Downstream:** the frame buffer.

**Do not confuse with:**

- [`../../22-Middleware-PhyreEngine/`](../../22-Middleware-PhyreEngine/) — the *other* middleware in
  this binary, built by a different vendor on a different CI system. `PhyreScripting.inl`'s 747
  functions are Phyre's, and the two reference sets are **disjoint**.
- [`../third-party-middleware-inventory.md`](../third-party-middleware-inventory.md) — the inventory
  that counts PPFX; this maps its internals.
- The RTTI vtable index. It recovers **class** identity; this recovers **file** identity. They agree
  where they overlap (§10) and mostly do not overlap at all.

## 6. Modding notes

- **This is the map to FFXII TZA's bloom and depth of field.** `GPURenderGlare.cpp` (19 functions)
  and `GPUDepthOfField.cpp` (22) are where the remaster's characteristic look is computed.
- **Attribution is by string reference, so it is exact and cheap to reproduce.** Find the `.rdata`
  string, take its references, and you have that file's functions.
- **99 of the 193 are exception funclets, and their file attribution is one step weaker than the
  rest of this map — stated here rather than left implicit.** ~~They inherit their file from the function they unwind, so a funclet's path tells you which source file its parent came from.~~
  **Reworded 2026-09-16 (FABLE) on `AUDITSPEC-REQ-FABLE-YEBIS-221-PAIRING`, per the pass-6
  adjudication.** *Inherit* was doing work it could not support. **A funclet's bytes cannot name a
  source file** — it is a fragment of its parent's body and the compiler emits the path reference at
  the assertion call site, which is in the parent. So the attribution is **two claims, and only one of
  them is evidence:**
    - **Which parent a funclet belongs to is METADATA-LOCATED.** That pairing comes from the unwind
      information, which **pass 6 bans as evidence for what the program does**. It is used here only
      to *locate* the parent, never to assert behaviour — the distinction the protocol's pass-6
      ruling draws between evidence and a method of finding something checked elsewhere.
    - **Which file that parent came from is a STRING REFERENCE in `.text`**, the same admissible
      basis as the other 94, and parents in this span demonstrably carry those strings: **46 of 400
      sampled non-funclet bodies inside `006DA880`–`007911E0` `lea` a `..\src\` path or a PPFX
      diagnostic.**
  **The consequence, which the old wording hid:** if a pairing is wrong the attribution is wrong,
  so **these 99 are attributed one metadata step further out than the 94** and should not be quoted
  as though they were string-attributed. It remains, as before, often the only identity a funclet
  has — which is the reason to record how it was obtained rather than to drop it.
- **`0016D6A0` is the assertion reporter and it is a `ret 0`.** Hooking it gives you every failed
  Yebis assertion in the game, with file and line already in registers at the call site. That is a
  free diagnostic channel the shipped build leaves open.
- **The licence code is in there.** `ppfxLicense.cpp` ships. Nothing in this document is a route
  around it, and modifying middleware licence checks is not a supported use of this map.
- **XIIOnline:** post-effects are per-client presentation. Nothing here is authoritative state and
  none of it needs to agree across clients.

## 7. What is not known

- [x] What each of the 193 functions *does*. This document establishes **where they came from**, not
      what they compute. File identity narrows the search enormously and closes nothing.
      **BQ-29.**
      *SUPERSEDED 2026-09-26 (FABLE, Claude Opus 5.5) under FRONTIER's class-1 ruling: a population-coverage statement; the population is carried by 23-Third-Party-Libraries/PostEffects-Yebis-PPFX/yebis-ppfx-source-map.md. See the register row.*
- [x] ~~The `TinyEffect` subsystem~~ — 38 functions across two files, one of them a string module
      (`TFXString.cpp`, 20 functions from only 6 distinct assertion lines). An embedded
      shader-effect language is implied by the name and is not established. **BQ-30.**
      *Identity established 2026-09-13 (FABLE), box left for the ledger mirror (BQ-30):* `CTinyEffect`'s methods (`0078F960`–`0078FB90`)
      and the `TFXString` bodies are members of the declared PPFX C row (`members/ppfx-span.tsv`). `TFXString` is a
      **source-text tokenizer**: `00717760` references the comment delimiters `*/` / `/*` / `//` (`00717DEF`,
      `00717E63`, `00717ED8`; strings `00D99908`–`00D99910`) and calls `0071A230`, which compares characters against
      `"space, tab, newline"` (`00D9993C`, `0071A280`–`0071A2B2`). So an effect-source text parser is present. Not established: that
      retail FFXII feeds it any text (`00717760` has no direct caller).
- [x] ~~Whether the `__LINE__` values reconstruct anything useful about file size or ordering.
      `GPUDepthOfField.cpp` shows 59 distinct lines and `GPUTextureUtil.cpp` 20 from 7 functions;
      neither has been checked against a known Yebis release.~~
      **BQ-31 ANSWERED 2026-09-22 (FABLE): no — and the obstacle is not the missing release, it is
      that the line values are not determinate.** §4 already says the window is a heuristic with
      *“nothing marking”* a `mov reg, imm` as the line number. **Re-implementing the method
      independently shows how much rides on that**, because the two halves behave completely
      differently.

      | §2.3 file | `lea` refs recovered | §2.3 sites | | distinct lines at window 16 / 24 / 32 / 48 B | §2.3 lines |
      |---|--:|--:|---|---|--:|
      | `GPUDepthOfField.cpp` | **75** | 75 | | 25 / 26 / 26 / 29 | 59 |
      | `GPUTextureUtil.cpp` | **20** | 20 | | 15 / 17 / 17 / 17 | 20 |
      | `GPUPostEffect.cpp` | **48** | 48 | | 6 / 6 / 6 / **18** | 35 |
      | `GPURenderGlare.cpp` | **39** | 39 | | 3 / 3 / 3 / 4 | 25 |

      **The attribution half reproduces exactly — four files, four exact matches** — which is the
      control: the sweep reads the image correctly, and §2.3's file map is confirmed by an
      independent pass. **The line half does not reproduce at all.** It disagrees by two- to
      eight-fold and it *moves with an arbitrary parameter*: `GPUPostEffect.cpp` goes from 6
      distinct values to 18 simply by widening the search window from 32 bytes to 48.

      > **So the answer is no, for a reason internal to the artefact.** A reconstruction of file
      > length would need the maximum line to be a real line; an ordering would need each value to
      > belong to its `lea`. **Neither holds when the value is whichever `mov reg, imm` happens to
      > sit nearest**, and this build's compiler interleaves unrelated constants there. *Checking
      > against a known Yebis release would not repair this — it would compare a real file against
      > numbers that are not reliably line numbers.*

      > **What survives, and it is the useful half.** The `lea` reference alone carries the file
      > attribution, needs no window, and reproduces exactly. §4 already said a wrong line number
      > *“cannot corrupt the map”*; this measures how wrong they can be while leaving the map
      > intact. **Static: image sweep, nothing executed.** **BQ-31.**
- [x] ~~Why `GPUClassUtil.h` alone kept an absolute path while every `.cpp` is relative, and why it has
      **12 copies but exactly one line number (73)**.~~ **BQ-32 ANSWERED 2026-09-22 (FABLE): one macro,
      on one line, in the one header.** It is the only `.h` in the set (`.cpp` 24 relative / 0 absolute,
      `.h` 1 absolute / 0 relative) and headers reproduce the include directory's spelling; the `73` is
      not in the string at all but is passed by the code, a nearby immediate at 19 of the 20 reference
      sites. See the section above. **BQ-32.**
- [x] ~~Whether `PhyreScripting.inl`'s 747 functions are one generated binding family.~~ *Answered 2026-09-13 (FABLE): three families (323 / 264 declared, 160 routed).* That question
      belongs to category 22 and is filed against it. **BQ-33.**

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| ~~26 source paths exist in the image~~ 29 source paths exist in the image - PPFX's 25, `PhyreScripting.inl` and three FFXII `..\..\katano\` `.c` files *(corrected 2026-10-02, OPUS: `.rdata` sweep; the 26 are the PPFX and Phyre paths)* | regex sweep of every section's raw bytes for a path separator plus a C/C++ extension | 2 |
| All 26 are referenced from code | RIP-relative operand scan over all 38,161 real function bodies | 1 |
| 1,857 sites, 940 functions | same scan | 1 |
| 193 PPFX functions, 192 single-file | reference sets per path, intersected | 1 |
| The two build systems | the two absolute paths, read verbatim | 2 |
| The reporter is folded to `ret 0` | `0016D6A0` is three bytes; the folding is established in [the funclet document](../../24-Compiler-And-CRT-Runtime/Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md) | 1 |
| File identity agrees with class identity where both exist | 5 of 5, §10 | 1 + 4 |
| 99 of the 193 are exception funclets | their `CodeDomain` in the snapshot | 3 |

**Superseded readings:** the first sweep of this document found **13** paths and would have reported
that number. See §10.

## 9. Related

- [`../third-party-middleware-inventory.md`](../third-party-middleware-inventory.md) — the inventory PPFX appears in
- [`../../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md`](../../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md) — 240 PPFX methods by class; the independent instrument this map was checked against
- [`../../24-Compiler-And-CRT-Runtime/Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md`](../../24-Compiler-And-CRT-Runtime/Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md) — the funclets that carry 99 of these paths, and the `/OPT:ICF` folding that spared the strings
- [`../../22-Middleware-PhyreEngine/`](../../22-Middleware-PhyreEngine/) — where `PhyreScripting.inl` belongs


## 11. The library's extent — 1,638 functions declared (2026-09-13, FABLE; recounted by OPUS; regenerated 2026-09-16, SWE2-EC7)

§2.3 attributed 193 functions to source files by their surviving assertion arguments. The **linked
object** is much larger: **every census entry from `006DA880` up to `007911E0`** — 1,766 entries — is
Yebis/PPFX, and **1,638** of them are declared here as EC-7 letter C (`members/select_ppfx.py`
regenerates the list and prints every figure below). The count fell 1,657 → 1,638 when later
declarations claimed what the span had absorbed: 17 MSVC `std::_Tree` bodies (the ordered-container
family's `_Isnil` carriers) and A-measured bodies leaving the family under *A beats a declaration*.

**Evidence inside the span.** 465 entries carry it directly: they `lea` one of the 25 ~~`..\src\`~~ paths *(corrected 2026-10-02, OPUS: 24 `..\src\` paths and the absolute `GPUClassUtil.h`)*
of §2.2 or a `PPFX` diagnostic (`..\src\ppfx.cpp(%d) : Feb 18 2016 PPFX ERROR:`), or sit at a
`PPFX::` vtable slot. Only two entries carry foreign RTTI, and both are identical-code-folded bodies:
`006DA8C0` (shared with `Yebis::YebisPfxMemoryAllocatorD3D11`) and `00786F42` (shared with Bullet's
`btBoxShape`).

**The edges.**

- **Lower, `006DA880`.** `006DA880` increments and `006DA8A0` decrements the counter `02EA0B3C` that
  `006DA8F0` tests, and the two are called from PPFX bodies only (`006DA990`, `006DAA70`, `006DE950`, …). `006DAA70` itself is read 2026-09-17 (SWE2-FRONTIER): 1,235 B — `..\src\ppfx.cpp` diagnostics ×12 through `006DF480` (first at [`006DAAC9`](../../_index/ADDRESS-INDEX.md)), `006E0F00`/`006E0CA0`/`006DA880` ×2 — the `CPostEffect` populate's calling site.
  The entries before them belong to Phyre: `006DA6C0` is a `Phyre::VTS::ScreenState*` slot, `006DA850`
  is called from `006C9B20`, `006DA860` from the static initialiser `00167990`.
- **Upper, `007911E0`.** `00790AD0`–`007911D0` — `std::vector` growth helpers, the dispatchers over
  them and the `D3DReflect` import stub — are called only from PPFX bodies (`0078AD20`, `0078DFB0`,
  `0078C730`, …); `007911E0` opens a run of `Phyre::PFramework` class descriptors.
  `0078AD20` itself is read 2026-09-17 (SWE2-FRONTIER): a 1,399-B **TinyEffect** sibling —
  `..\src\GPU\TinyEffect\TinyEffect.cpp` diagnostics, `00E21D78`-block `.rdata` descriptors loaded
  at [`0078AD61`](../../_index/ADDRESS-INDEX.md), `007911D0`/`00790DF0` descriptor helpers ×6.
  `0078C730` itself is read 2026-09-17 (SWE2-FRONTIER): a 4,261-B **TinyEffect** body —
  `..\src\GPU\TinyEffect\TinyEffect.cpp` diagnostics ×39 through `006DF480` (first at
  [`0078C772`](../../_index/ADDRESS-INDEX.md)), the `ETFXPT_FLOAT`/`FLOAT4`/`FLOAT4x4`/`SAMPLER`
  parameter-type tokens and the `cgstrip`/`glsl_bin` shader-blob tags — the TinyEffect
  effect-descriptor deserializer, with `00715C70` ×24 / `00716410` ×11 / `007187E0` ×8
  registration helpers.

**Left out (stay in the frontier or in their own families).** 11 A-measured entries; 96 entries already
in OPUS's generated families (static-pointer / member-pointer tail calls, virtual tail calls, deleting
destructors, vtable installers, forwarders, import stubs, no-op stubs); `00786F42` (folded with
`btBoxShape`); and **`0071F970`**, an 83-byte body called both from PPFX (`0071D9E0`, `0071E290`) and
from Phyre framework code (`00798000`, `00799980`, `0079BDF0`, `0079D430`) — a shared body whose
provenance its position cannot decide.

> **Crossings named — FINAL-AUDIT pass 22 (FABLE, 2026-09-14). `0071F970`'s provenance narrowed.**
>
> **`0071F970` matches `sscanf_s` as the UCRT header defines it inline.** It takes the options from an 8-byte static
> accessor (`0018A320` → `01F7F5B0`, the shape of `__local_stdio_scanf_options`) and ORs in bit 0
> (`_CRT_INTERNAL_SCANF_SECURECRT`). It then calls `__stdio_common_vsscanf` with length `-1` and a null locale
> (`0071F991`–`0071F9B5`). A header-inline function is emitted once per image, so the body belongs to the CRT headers
> rather than to PPFX or Phyre. That fits both caller sets. *Narrowed, not closed:* the match is by shape.
>
> **Its framework callers are option parsers, and the ledger's labels for them are nominal:**
>
> - `00798000` parses `"%d,%d"` and is labelled **Input**;
> - `0079FB10` reports `"Error opening : %s"` and parses `"%d:%d:%d"`, labelled **Input**;
> - `0079BDF0` compares an option name against `"Frames"` (`_stricmp`) and is reached from `007A08A0`, both labelled
>   **Input**;
> - `00799980` is labelled **Application**. It parses one `%f` into `+0x6C`. When the value is not positive, it
>   rebases the double at `+0x50` on the **Platform** timer `005CC930`, less the engine start time `02CB60E8`.
>
> **The STL helpers `001A5500` and `001A5630` are MSVC `std::string` insert and append** (`"invalid string position"`,
> `"string too long"`). Their callers outside the span are:
>
> - **Platform** `0020DE30`, which parses `PCI_VEN` / `SUBSYS` out of a device id string (interior
>   verified 2026-09-17, SWE2-FRONTIER — the `PCI_VEN`/`DEV`/`SUBSYS` tokens load at
>   `00906898`/`009068A0`/`009068A4` and are matched through `00195200` ×8, first at
>   [`0020DF24`](../../_index/ADDRESS-INDEX.md));
> - **Platform** `00781EC0`, which formats `%02x-%02x-%02x-%02x-%02x-%02x`;
> - **PlatformOnlineAchievements** `007A0C60`, the Steam language query;
> - **Save_Load_Settings** `GameSettingConfig_ParseText` (`001DE5D0`).
>
> Those are shared-library edges. None puts game logic inside the PPFX span or PPFX logic outside it.

**Controls — what could have exposed game code inside the span.**

1. **Outbound.** 44 distinct direct-call targets outside the span: the CRT and its math imports
   (`sqrtf`, `powf`, `logf`, `tanf`, …), `sprintf` `0017D2E0`, MSVC `std::string` / container
   helpers (`00195200` is `_Tidy` with its `capacity >= 0x10` test; `001A5500`, `001A5630`, `001DFA10`,
   `001DF990`, `00204760`, `001A4C90`), a static-address accessor `0018A320`, the thread-safe-static
   header / footer, and `006CBBC0`, an initialiser only PPFX calls. **None is game logic.**
2. **Inbound.** Every direct caller from outside is the integration client (`006CBD20`, `006CBEA0`,
   `006CC090`, … — 23 functions at `006Cxxxx`, the code that reads `FeatureId = YEBIS_D3D11 …`), a static
   initialiser at `0016xxxx`, or a teardown / unwind thunk at `008Axxxx` / `008Bxxxx`; the one exception
   is the excluded `0071F970`.
3. **Shared globals.** Security cookie aside, the `.data` locations PPFX shares with outside code are
   referenced only from static-lifetime zones (`0016xxxx`, `008Bxxxx`) and the TLS index `02EAED3C` that
   every thread-safe static reads. **None is shared with game code.**

**The vendor (answers `X-7`).** Three independent indications join the product name and the
`yeblic-ppfxlic` build workspace of §2.2: the licence module `..\src\UT\ppfxLicense.cpp` and
`006DFF40`'s `License text is not set.` / `License is not valid.` checks in `ppfx.cpp`; the strings
`YEBIS_D3D11`, `YEBIS Expiration Problem` and `The YEBIS library passed over the expiration date` stored
in `ppfx.cpp`'s own string pool (`00D8ECB8`, `00D8F170`, `00D8F690`); and **`TjmjdpoTuvejp` at
`00D8F1C8`, in the same pool, which is `SiliconStudio` with every character shifted up by one.** That
last string has **no** code or data reference — it is evidence of what was compiled into the unit, not
of a runtime check. Together: **PPFX is the post-effect core shipped as Silicon Studio's Yebis, not a
Sony component.**

**Scope.** A C disposition says whose code this is and where it ends. What the 1,657 bodies compute is
§7's open work (`BQ-29`~~, `BQ-30`~~). *(`BQ-30` was answered on 2026-09-13: TinyEffect / TFXString is PPFX's effect-source text tokenizer. Noted 2026-09-26, FABLE, Claude Opus 5.5.)*

## `BQ-32` answered — one macro, on one line, in the one header (FABLE, 2026-09-22)

`BQ-32` asks two things that look unrelated and have a single cause.

### The absolute path tracks the EXTENSION, not the file (FABLE, 2026-09-22)

Sweeping every source path in the image and splitting by form:

| extension | absolute | relative |
|---|--:|--:|
| `.cpp` | **0** | **24** |
| `.c` | **0** | **3** |
| `.h` | **1** | **0** |

**`GPUClassUtil.h` is not a special file — it is the only *header* in the set, and every
translation unit is relative while the one header is absolute.** That is what MSVC's `__FILE__`
does: it reproduces the path *as the compiler saw it*. A `.cpp` arrives as the relative path on the
command line (`..\src\GPU\GPUPostEffect.cpp`); a header arrives through the include search and
reproduces the include directory's own spelling, which on this build machine was absolute
(`d:\bamboo\build\yeblic-ppfxlic-bl2015\…`). *So the question's premise — that one file “kept” an
absolute path — inverts it: nothing kept anything, the header simply never had a relative one.*

### `73` is not in the string — it is passed by the code (FABLE, 2026-09-22)

**All 12 occurrences are byte-identical and none of them contains `73`:** the string is exactly
`d:\bamboo\build\yeblic-ppfxlic-bl2015\src\gpu\GPUClassUtil.h`, with no `(%d)` and no number.
The line number is a separate argument, and the code supplies it:

> **20 code sites reference ~~the twelve copies~~ six of the twelve copies, and `73` is a nearby immediate at 19 of them.** *(corrected 2026-10-02, OPUS: per-copy `lea` counts 6 + 6 + 1 + 1 + 3 + 3; `00D9BC88`, `00D9BCC8`, `00DA61D8`, `00DA6288`, `00DAC3B8` and `00DAC3F8` have none)*
> (The exception is `00714314` in `FUN_007142F0`, which loads its line number by another route.)

**So both halves are one fact: a macro on line 73 of that header, expanded in many translation
units.** Each expansion emits its own `__FILE__` literal — which is why there are **twelve copies**
rather than one pooled string — and every expansion carries the same `__LINE__`, because it is the
**same single line**. *A macro used at many call sites in many `.cpp` files produces exactly this
shape: N copies of one path, all reporting one line.*

> **This also retires the shape §10 flagged.** That pass saw *“six identical copies of
> `GPUClassUtil.h`, all at line 73”* and correctly distrusted it, but attributed it to **display
> truncation**. The truncation was real and was a tool defect; **the repetition was not** — the
> copies and the single line number are both properties of the image, and they have an ordinary
> cause. *A shape that “made no sense” turned out to make sense once the line number was traced to
> the caller instead of the string.*

## 10. Falsification pass 2026-09-02

**DEFECT 9: the sweep required a drive letter and found 13 paths.** The pattern was written from
BK-3's own example, `d:\bamboo\build\yeblic-ppfxlic-bl2015\src\gpu\GPUClassUtil.h`, which begins with
a drive letter. **Yebis emits its `__FILE__` as a relative path** — `..\src\ppfx.cpp` — so the sweep
missed **287 of 300 strings, 96 % of the evidence**, and returned a tidy, plausible 13.

Two things caught it, and neither was the tool. First, the printed output showed **six identical
copies of `GPUClassUtil.h`, all at line 73** — a display artefact of truncating to the last 72
characters, but a shape that made no sense and forced a second look. Second, BK-3 said **18**, and 13
is not 18; a census that disagrees with the question it is answering has to explain the difference
before it reports.

Widened to "any string containing a separator and a C/C++ extension", the population became **300
strings / 26 distinct paths**, and the recovered tree is coherent — four directories, a public
entry point, a GPU abstraction, the effects, an embedded effect system and a licence file. **A
too-narrow pattern does not produce a coherent source tree; it produces a fragment.**

### SURVIVED: the attribution, cross-checked against an instrument that never saw a string

The recovered vtable index assigns **class** identity from RTTI. It overlaps this map on only **5**
functions — but on all five the class name and the file name are the same object:

| function's source file | recovered class |
|---|---|
| `GPURenderTexture.cpp` | `PPFX::CRenderTexture` |
| `GPUTextureUtil.cpp` | `PPFX::CTextureUtil` |
| `GPUInterfaceTexture.cpp` | `PPFX::IGPUTexture` |
| `GPURenderTextureArray.cpp` | `PPFX::CRenderTextureArray` |
| `ppfxRenderToTexture.cpp` | `PPFX::IPfxBaseRenderToTexture`, `PPFX::IPfxRenderToTexture_Dx11` |

**Five of five.** Two independent recoveries — one from RTTI structures, one from assertion text —
naming the same code the same way.

The other **188 functions are outside the vtable index entirely**, which is the point: RTTI can only
name virtual methods, and most of a post-effects library is free functions and statics. **The two
instruments are complementary rather than redundant**, and this one reaches nearly 40 times as many
functions in this library as the overlap suggests.

### SURVIVED: the Phyre path is genuinely a different phenomenon

`PhyreScripting.inl` has 1,494 sites but **no recoverable `__LINE__`**, and its 747 functions are
**disjoint** from the 193. If it were the same assertion mechanism, the line numbers would be there
and the sets would mix. It is a header included into generated bindings, and it is filed to
category 22 rather than absorbed here.

### What was tried and did not break anything

- **Checked whether unreferenced strings exist** — a path present but never used would suggest dead
  code or a stripped module. There are **none**: all 26 are referenced.
- **Checked the `__LINE__` heuristic's blast radius.** It is a ±5-instruction window and nothing marks
  the immediate as a line number. The **file** attribution does not use it, so a wrong line cannot
  corrupt the map; the line counts in §2.3 are reported as what they are.
- **Counted string copies.** `GPUDepthOfField.cpp` appears 67 times, `GPUPostEffect.cpp` 38. That is
  one copy per translation-unit instance with no ICF folding of `.rdata` — consistent with a library
  delivered as many small objects, and it means copy count is **not** a measure of importance.

### Status

`DOCUMENTED`, one falsification pass. What would kill it: a function referencing a PPFX path whose
recovered RTTI class contradicts its file; a 27th path in a form neither sweep matched; or evidence
that `0016D6A0` is not the reporter these sites call.

## OPUS independent audit of the EC-7 row — 2026-09-13

**This is the largest single disposition in the database**: 1,657 functions, **15% of the 11,219**
A+B+C total. Its selector is an **address span** — everything from `006DA880` to `007911E0` less
104 — with direct evidence on **465 entries (28%)** and the remaining **1,195 riding on
contiguity**. Contiguity is a sound argument for a statically linked library and it is exactly the
kind that has to be tested rather than accepted, so OPUS tested it as EC-7 owner.

### The arithmetic is exact

| | |
|---|---:|
| non-funclet census entries in `006DA880`–`007911E0` | **1,766** |
| declared members | **1,657** |
| declared members outside the stated span | **0** |
| span entries not declared | **109** |

The row accounts for exactly 109: 107 already dispositioned (11 A-measured, 96 in the generated
families), one ICF-folded body, and `0071F970`. **1,766 − 109 = 1,657, to the unit.**

**RECOUNTED 2026-09-13 (OPUS, EC-7 owner), because the checker refused the row.** Two more span
entries were measured as **A** after this member list was generated - `00717760` among them - so the
list still claimed bodies that had since been individually explained, and a C family that overlaps an
A measurement double-counts the same function. `check_dispositions` caught it as
`2 member(s) are already measured as A`, `select_ppfx.py --write` regenerated the list, and the
figures above are the regenerated ones: **1,657** members, **11** A-measured exclusions, **109** span
entries not declared.

**The refusal is the mechanism working, not a defect.** An EC-7 member list is a snapshot of a moving
boundary: every time a body in the span is individually explained, the family that contains it must
shrink. Nothing but this check would have noticed, and the row would have quietly claimed two
functions twice.

**One figure here was also mine and wrong.** The audit table published 1,660 declared members against
a file whose member count was 1,659 - it counted the header row. That is corrected above rather than
left, because an audit section that cannot add up is worse than one that is absent.

### ✖ Nothing in the span is attributed FFXII code - and this test is WEAKER than it looks

- declared members carrying **any** `owner`: **0** of 1,657.
- declared members carrying an FFXII-subsystem tag (`GFZ.V120.PrimaryOwner.*`, `FFXII.*`):
  **0 distinct tags**.

> **Downgraded the same day, by running the same test over all 91 accepted families.** Eight other
> rows *do* contain owner-attributed members - **1,126 of the SEAD sound library are tagged
> `FFXII.Audio`**, and the CRI HCA decoder, both libogg objects, libvorbis and Tremor carry
> `owner=Audio` - **and none of that is a defect.** `owner` is a **call-graph subsystem
> attribution**, not an authorship claim: an audio codec statically linked into the audio subsystem
> is owned by Audio *and* is third-party code, and both are true at once.
>
> **So this test passes here for a reason that has nothing to do with PPFX being correctly
> bounded** - the post-effect span simply sits in a region the classifier never attributed to a
> subsystem. A test that a correctly-dispositioned library would fail, and that an incorrectly
> bounded one in unowned territory would pass, is **not the discriminator I presented it as.**
>
> **What still stands:** the arithmetic reconciliation to the unit, and the inbound-caller boundary
> check by kind. Those two carry the audit; these two bullets are context.

### The inbound-caller boundary holds

The row claims callers are *"only the integration client at `006Cxxxx`, static initialisers and
teardown thunks"*. Every direct call in `.text` was checked: **559 distinct callers from outside
the family**, of which 426 are at `0079xxxx`+ (the Phyre framework above the upper edge) and 6 in
the integration client. The remaining **129 were classified by kind**, not by address:

| kind | callers |
|---|---:|
| static initialiser | 70 |
| thunk / adapter | 36 |
| teardown / destructor | 15 |
| constructor vtable install and one already-excluded PPFX body | 8 |

**Every one falls inside the kinds the row permits, and none is owner-attributed engine code.**

### What this audit does and does not establish

> **It establishes that the span contains no FFXII engine code and that the boundary claim
> survives an independent check.** It does **not** establish that each of the 1,195
> contiguity-only members is individually PPFX — a passing negative control is not positive proof
> of membership, and no amount of "nothing wrong found" converts into one.

**Stated limits of the audit itself:** caller kinds were read from the classifier's tags, not from
each body, which is weaker than a decode; and the eight "constructor vtable install" callers were
sampled rather than enumerated. **The row is accepted on this evidence and remains open to a
positive-membership challenge**, which is the standing an address-span disposition should have.


### Interior citation — frontier hub `001A5500` (2026-09-18, SWE2-EC7)

`001A5500` — 293 B, 11 callers: the MSVC `basic_string` insert-at-position the
map above names. Confirmed against the image: `[rdx+0x10]` position check
throws `"invalid string position"` via `008C2620` at
[`001A5531`](../../_index/ADDRESS-INDEX.md); `rdi > -2` throws `"string too
long"`; capacity shortfall calls `00195670` grow, self-insertion
(`rbx == rsi`) takes the `00196AC0` copy arm, and `00861EBA` (memmove) shifts
the tail. Sibling of `001A5630`/`001A52A0`.

### Interior citation — frontier hub `00195670` (2026-09-18, SWE2-EC7)

`00195670` — 398 B, 10 callers: the MSVC `basic_string` capacity grow the
insert above calls. Read from the shipping image: `size | 0xF` rounding, the
`0xAAAAAAAAAAAAAAAB` multiply at
[`001956B3`](../../_index/ADDRESS-INDEX.md) computing the 1.5x growth policy
(capacity / 2 headroom check), the `0x1000` small/large split routing through
`008C2608` on overflow — `_Grow`'s whole shape, `_Tidy`'s partner.
## SWE2-EC7-32 update (2026-09-18) — `001DFA10` heap-block validator + `00196AC0` `string::erase`

`001DFA10` (85 B) is the deallocation-side validator the map
lists: when `r8 >= 0x1000` the candidate pointer is audited —
`dl & 0x1F` alignment, `[rdx-8] < rdx`, and the gap
`rdx - [rdx-8]` bounded to `[8, 0x27]` — each failure raising the
`008C2DA8` fatal handler; a clean block proceeds with
`rdx = [rdx-8]` into a tail `jmp 00210EB0`. Interior anchor
`001DFA29` (the `[rdx-8]` header read).

`00196AC0` (198 B) is `basic_string::erase(pos, len)`: `rdx`
against `+0x10` throws `"invalid string position"` through
`008C2620`; `len >= size - pos` truncates (new size, NUL at
`buf[pos]`, `+0x18 >= 0x10` picking the heap buffer); otherwise
`008C2A40` memmoves the tail down before the same terminate.
Interior anchor `00196B4B` (the `call [008C2A40]` memmove).

## SWE2-EC7-40 update (2026-09-19) - `0079BDF0`

`0079BDF0` (375 B) is a Yebis PPFX body - `01CB273C`/`01CB2748`, `"Frames"` string, `008C3000` thunk triple plus `0079BFD0`/`005CDAA0`/`0071F970`. Interior anchor `0079BE3C` (an `008C3000` thunk call).

## SWE2-EC7-42 update (2026-09-19) - `006CBBC0`

`006CBBC0` (316 B) is a call-free render-pass descriptor defaults init - literal stores: `+0`=1, zeros `+8..+0x58`/`+0x80`/`+0xc8`/`+0xe8`/`+0xec`, `byte[+0x30]`=1, `+0x34`=-1, `+0x38`=1, `+0x60`/`+0x70`=0.25f, `word[+0x68]`=0x101, `+0x6c`=8, `+0x78`=1, `+0x88`=-1, `+0xcc`=-1, `+0xd0`=0.85f. Interior anchor `006CBC19` (the `+0x60` 0.25f store).

## SWE2-EC7-50 update (2026-09-19) - `00204760`

`00204760` (185 B) is a body - `001A4C90`/`00210EB0` plus four `008C2DA8` import calls. Interior anchor `002047A0` (an `001A4C90` call).

## SWE2-EC7-55 update (2026-09-19) - `0079BFD0`

`0079BFD0` (243 B) is a Yebis PPFX body - `005CDAA0`/`0079C0F0`/`007A1230` plus `01CB2720`. Interior anchor `0079BFF3` (a `007A1230` call).

## SWE2-EC7-59 update (2026-09-19) - `00167990`

`00167990` (163 B) is the `PMapPair` static initialiser the yebis page names - `0067FFB0`/`006DA860` plus `00D86BD8`/`02E5BDE0`/`02E5BDE8`. Interior anchor `001679A4` (a `006DA860` call).


## SWE2-EC7-114 update (2026-09-21) - `007A1230` / `007A0540` measured

`007A1230` (123 B) is the
text-scan step `0079BFD0`
runs on the `+0x18` cursor:
IAT `008C2F88` classifies
each byte (space-class skip),
a `0x23` (`#`) at the
cursor calls `0079C0D0` to
jump the comment and
resumes, anything else
returns the cursor - the
whitespace/comment skipper
of a config text parser,
returning 0 at the end of
the buffer.
Interior anchor `007A1253`
(the IAT classify call).

`007A0540` (132 B) is the
sized-array setter
`0079FB10` runs: a changed
`edx` allocates `edx * 0x98`
bytes at alignment 8 through
`0017D260` (failure on a
nonzero count returns `0xD`),
the old `qword[+8]` block
goes to `00584730` when the
prior count's bit 31 was
clear and the pointer live,
then `[+8]` and `[+0]`
relatch - the `0x98`-record
resize with the same
ownership-bit convention
`001B70E0` tore down.
Interior anchor `007A05AC`
(the `+8` pointer store).

## SWE2-EC7-115 update (2026-09-21) - `0079D9A0` / `0079C0F0` / `0079C0D0` measured

`0079D9A0` (90 B) is the
field splitter `0079FB10`
runs on `[rcx, rdx)`: scan
to the first `r8b`
delimiter or terminator,
then NUL-write at the next
`r8b`/end and return
`token + 1` - a bounded
field cutter for the config
text `007A1230`/`0079C0F0`
walk.
Interior anchor `0079D9B9`
(the scan-advance load).

`0079C0F0` (72 B) is the
find-next-space `0079BFD0`
calls: over
`[+0x18, +0x20)` it returns
the first byte IAT
`008C2F88` classifies
nonzero, or 0 at the end -
the complement of
`007A1230`'s skip-spaces,
the two halves of the
parser's token walk.
Interior anchor `0079C10A`
(the classify call).

`0079C0D0` (32 B) is the
find-newline `007A1230`
calls on `#`: returns the
`0x0A` inside
`[+0x18, +0x20)` or 0 -
the line skip behind the
comment path.
Interior anchor `0079C0E0`
(the `0x0A` compare).

## SWE2-EC7-116 update (2026-09-21) - `006DA860` measured

`006DA860` (14 B) is the
trivial constructor
`00167990` calls: stamps
vtable `00D8E1E8` ([0] =
`006DA8C0`, RTTI locator
`01D3BC50`) on `rcx` and
returns it.
Interior anchor `006DA867`
(the vtable store).

## Cross-subsystem neighbours — SWE2-STRUCT (pass-22 dispositions)

- **Audio - CLIENT (2 edges).** `005CC930` is called by bodies filed to Audio: `00223190`, `00224570` - shared machinery across the layer boundary, no shared ownership.
- **CoreRuntimeScheduling - CLIENT (1 edge).** `005CC930` is called by bodies filed to CoreRuntimeScheduling: `001E03F0` - shared machinery across the layer boundary, no shared ownership.
- **Presentation - CLIENT (12 edges).** `001A52A0`, `001A5630`, `005CC930`, `006DA850` are called by bodies filed to Presentation: `001A6FF0`, `001C3D50`, `001C5570`, `001C5750` (+8 more) - shared machinery across the layer boundary, no shared ownership.
- **Resource - CLIENT and SERVICE (17 edges).** `001A52A0`, `001A5500`, `001A5630`, `005CC930` (+1 more) are called by bodies filed to Resource: `001D9F90`, `001DA290`, `001DADC0`, `001F4060` (+4 more); `0079D430`, `0079FB10` reach bodies filed to Resource: `00597970`, `00598100`, `0059BD80`, `0059D920` - shared machinery across the layer boundary, no shared ownership.

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-yebis-ppfx-source-map-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00786F42` | 32 B | with `rbx` as it holds on entry (this body never sets it), stores `edx` in dword `+0xEC`, `rcx` in qword `+0`, `rdx` in qword `+0xF0` and 3 in dword `+0x10` of `rbx`, then adds 0x20 to `rsp`, pops `rbx` and returns the entry `rbx` | `00786F45`, `00786F4B`, `00786F4E`, `00786F55`, `00786F5C` |
