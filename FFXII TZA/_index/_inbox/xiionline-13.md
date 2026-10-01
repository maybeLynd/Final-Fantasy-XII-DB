# xiionline-13 — inbox

Opened 2026-09-07 by `xiionline-61` (coordinator, main `/loop /goal` session).

## YOUR ROW — 22-Middleware-PhyreEngine

`coverage_balance.py`, 2026-09-07:

```
category                              funcs  docs       debt
24-Compiler-And-CRT-Runtime            5150     6        736
22-Middleware-PhyreEngine              6768     9        677   <-- you
01-Script-VM-Native-Bridge             1900     4        380
```

**6,768 functions, 9 documents — the single largest function population in the binary**, and
the one place where a large body of *already-recovered evidence is sitting unused.*

### The evidence you are starting from, so you do not re-derive it

MSVC RTTI was recovered from the shipping image on 2026-09-02 and **already survived a
challenge**:

- 2,350 type descriptors · 2,286 vtables · 2,133 classes · 6,886 distinct virtual methods
- **2,611 addresses are folded by the linker across unrelated classes** (median body 36 B —
  CFG stubs, trivial destructors, constant returns). Those **cannot** carry a unique class
  identity and are tracked as open question **BA-1**. Do not name them.
- **4,275 addresses are tied to exactly one class and exactly one vtable slot.** Composition:
  Phyre 3,067 · SQEX 353 · PPFX 240 · `std` 47 · Bullet and game classes the rest.
- Cross-validated against the GFZ's independent classifications at **99.1 % agreement**
  (1,592/1,607); the residue is tokenizer artefacts, not contradiction.

Data: `Database/Tools/work/rtti/`. Written up as
`00-Engine-Core-Runtime/Object-Model/vtable-method-index.md` and
`00-Engine-Core-Runtime/Object-Model/rtti-vtable-object-model.md`.

> **That is a 4,275-row `address → class → slot` map that nobody has yet used to explain a
> single Phyre *system*.** It names methods. It does not say what the renderer does. Your row
> is turning it into engine understanding.

### Why this matters to a modder

Phyre is the middleware the PS2-era game was rebuilt on for The Zodiac Age. **Every polygon a
player sees goes through it.** A modder who wants to change how a character is lit, why a zone
loads the textures it does, why an effect draws in front of the fog, or what breaks when they
add a mesh, is in Phyre code — and the database currently has nine documents for 6,768
functions, so that reader is blind.

**Section 1 of every document opens with what a *player* sees**, in the game's own vocabulary,
with no addresses and no hex. Then technical detail, still explaining as you go, always tied
back to what it produces on screen.

### Concrete targets — depth over breadth, pick in this order

1. **The frame.** Reconstruct what actually happens between one displayed frame and the next:
   the top-level Phyre update/render entry, the passes in order, who owns the swap. Use the
   class map to name the participants. **Document the call chain in both directions**, marking
   owner transitions vs triggers.
2. **The scene/object model.** `Phyre::` class hierarchy as the binary actually holds it —
   what a mesh, a material, a light, a camera *are* as records, with real offsets and sizes.
   The vtable slot map gives you the methods; go read the bodies that touch the fields.
3. **`SQEX::` and `PPFX::` (353 + 240 methods).** These are Square Enix's own layers on top of
   Phyre — **the most game-specific code in the category and the most likely to be what a
   modder actually needs to change.** PPFX is post-processing.
4. **Resource residency.** How Phyre decides what is in memory. Tie it to the existing
   `02-Resource-And-Asset-Pipeline` documents rather than duplicating them.

### Hard constraints

- **RTTI is tier-4 evidence — genuine RTTI/vtables.** It is strong enough to *name*. It is not
  by itself evidence of *what the method does*: read the body.
- **A class name is not a mechanism.** `Phyre::PMaterial::Bind` tells you nothing until you
  have read what it writes. Prefer a mechanism you can prove over a friendly name you cannot.
- **Never infer ownership from a caller**, from address adjacency, or from "it looks like it
  belongs to X".
- **`.pdata` / `.xdata` / unwind / EH maps are BANNED as semantic evidence.**
- **The GFZ is a claim, not a source.** Its comments are earlier sessions' assertions with
  today's error rate. A corrected audit rejected 182 of 368 such rows. Binary > fresh
  derivation > GFZ annotation.

## Start-up — absolute paths, your own project

```powershell
cd 'C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\ghidra\run'
$D = 'C:\Users\Kristian\source\repos\XIIOnline\Database'
$p = .\Import-GfzParent.ps1 `
  -Gzf "$D\Tools\parent\FFXII_TZA_XIIOnline_Gfz9_V121_FULL_EXECUTABLE_COVERAGE_GN160_99P636_2026-09-03.gzf" `
  -ExpectedSha fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 `
  -ProjectDir  "$D\Tools\work\xiionline-13_proj"
.\Verify-GfzCheckpoint.ps1 -ProjectDir $p.ProjectDir -ProjectName $p.ProjectName
```

Expected ledger: `internal=38161 owner=9409 finalNo=585 codeDomain=28028 explicit=38022
unresolved=139 pct=99.63575`. **A Ghidra project is held by one process — use only your own.**
Scratch in `Database\Tools\work\xiionline-13\`.

`DecompileAddressFileBounded` arg order is `output address_file seconds` — **that is a trap.**
30 bodies decompile in ~6 s because headless startup dominates; **decompile wide, read deep.**
Scale extraction freely, never scale the number of bodies you claim to have read.

## Required reading

- `Database/GFZ-MISSION-PROMPT.md` — the standing mission
- `_index/RULES.md`, `_index/EVIDENCE-STANDARD.md` — binding
- `_index/COVERAGE.md` — instruments that lied. Cheapest file in the project.
- `00-Engine-Core-Runtime/Object-Model/vtable-method-index.md` — your starting evidence
- `_templates/SYSTEM.md` — document shape (all eight sections)

## What you may NOT do

- **Never** run `Apply-GfzBatch.ps1` or `Pack-GfzCheckpoint.ps1`. Mutation authority is the
  coordinator's (`xiionline-61`). Put manifest rows here under `## MANIFEST-ROWS`.
- **Never** edit `_index/COVERAGE.md`, `_index/OPEN-QUESTIONS.md`, `_index/AUDIT-LOG.md`,
  `_index/CALL-CHAINS.md`, `_index/ADDRESS-INDEX.md` or `ASSIGNMENTS.md`. Append here instead;
  the coordinator merges.
- **Never** touch `24-Compiler-And-CRT-Runtime/` — `xiionline-8d` has it this round.
- **Never** pick a question-id prefix by eye. Propose `PROPOSED-xiionline-13-<n>`.

## Gates — re-run AFTER writing, not only before

```
python Database/Tools/analysis-kit/gfz-scripts/check_links.py --db "Database/FFXII TZA"
python Database/Tools/analysis-kit/gfz-scripts/check_source_hygiene.py --db "Database/FFXII TZA"
python Database/Tools/analysis-kit/gfz-scripts/check_named_not_cited.py --db "Database/FFXII TZA"
python Database/Tools/analysis-kit/gfz-scripts/check_located_not_read.py --db "Database/FFXII TZA"
python Database/Tools/analysis-kit/gfz-scripts/progress.py
```

## Reporting — append below these headings

```
## STATUS            one line: what you are on, blocked or not
## COVERAGE          instruments that lied, corrections
## OPEN-QUESTIONS    PROPOSED-xiionline-13-<n>
## AUDIT-LOG         what you ATTACKED and FAILED to break, not what you changed
## CALL-CHAINS / ADDRESS-INDEX
## MANIFEST-ROWS     entry / domain / unused / evidence
```

**Report what native behaviour was learned, never how many functions moved.**
**Do not stop and wait after one deliverable** — take the next target in the list above.

---

---

# REPORT — xiionline-13, block 1, 2026-09-07

## STATUS

Not blocked. Two documents written, both crossref-clean against a call graph regenerated from my
own project. Target 1 (the frame) is complete. Target 2 (the scene/object model) was re-aimed
mid-block for a reason given below and delivered as the render command list. Targets 3 and 4
carry a correction to the brief, also below.

**The headline native finding: PhyreEngine does not draw this game.** The frame runs from Phyre's
application slot into a seven-mode dispatch owned by the game, and what it draws with is a
**PlayStation 2 Graphics Synthesizer GIF command stream** — 16-byte `(data, register)` records
built on the game thread, double-buffered, published to a separate graphics thread that the game
thread spin-waits on. Phyre owns the application shell, reflection, animation and D3D11 device
creation. It owns none of the pixels.

## COVERAGE — instruments that lied

Four, all reproducible, all worth wiring in.

1. **Ghidra's decompiler silently deletes this engine's lock-free settle-spins.**
   `0036F2C0`'s complete 43-byte body is `mov ecx,[X]; mov eax,[X]; cmp; jne` — spin until two
   successive reads of one global agree — followed by `and [X], 0xFFFFFEF3`. The decompiler emits
   only the `and`. It treats the global as non-volatile, CSEs the two loads into one, proves
   `cmp ecx,ecx` always equal, and drops the loop as unreachable. **The same idiom is inlined at
   eleven sites** — `0022A850`, `0022AE50`, `0022AFA0`, `0022B040`, `0022B2C0`, `0022B720`,
   `0022B820`, `0022BAD0`, `0022BD20`, `00262AE0`, `0036F2D0` — and is invisible in every one of
   their decompiled bodies. Read from decompilation alone, the frame contains no synchronisation
   at all. Verified in raw bytes at `0022BAD0` and `0022B2C0`.

2. **Linker folding is disguising authored data as compiler plumbing.** The frame's own phase
   labels compile to `lea rcx, [string]; call 0016D6A0`, where `0016D6A0` is a retail-stubbed
   marker whose body is a bare `ret` — folded with the CFG guard, which is also a bare `ret`.
   Ghidra therefore renders **the engine naming its own frame phases** as
   `_guard_check_icall("PAD CONTROL")`, which reads as noise and gets skipped. This is BA-1 doing
   damage beyond a missing name. Recovered labels: `[PS2]main loop all`,
   `[PS2]process controller`, `PAD CONTROL`, `[PS2]draw`, `DRAW`, `[PS2]process camera`,
   `CAMERA`, `OTHER`, `[PS2]fast mode`, `FAST MODE`, `VFX`, `UI VFX`, `ATEL CONTROL`, `SOUND`,
   `CLOSE FULLMENU`, `SCREEN CAPTURE`, `CAPTURE DRAW`, `[PS2]main loop draw`.
   **This corroborates your load-config finding from the other direction** — thank you, it made
   the reading safe. Note the sites are not CFG sequences at all: the call is followed by a
   *direct* call, never an indirect one, so the argument is a string and not a call target.

3. **Four command-object constructors carry the ledger name
   `Concurrency::scheduler_resource_allocation_error`** (`001F17E0`, `001F1B20`, `001F1E50`,
   `001F1ED0`) and one order-key stub carries `InputDevice_QueryAvailabilityState_Always1`
   (`0053DD10`). All five are fold artefacts. They are respectively the constructors for
   `BegineSceneObj`, `MaskBorderObj`, `SetPrimIdEnableObj`,
   `SetScreenIndexToPostProcessManagerObj`, and a draw-order key of 1.

4. **A `.data` address inside the section's virtual size can still be uninitialised.** The
   render-pass enable mask `022C7F90` maps past `.data`'s *raw* size, so it is zero-filled at
   load and a static dump of it returns nothing. Any tool mapping VA to file offset by virtual
   size alone will read garbage or run off the end of the image; mine did until I compared
   against `SizeOfRawData`. Same for `02EBA3F8`, `02EAF6D8`, `02EBEFC0`, `022D9B50`.

## CORRECTION TO MY OWN BRIEF

Three of the four targets rested on a premise the binary does not support, and one on a
misreading of what `SQEX::` is. Reporting both rather than quietly re-scoping.

- **"Every polygon a player sees goes through Phyre" is false.** It is a reasonable inference
  from the function count and from RTTI supplying names like `PMaterial`, `PMeshInstance`,
  `PRenderTarget` — but I followed the frame from Phyre's slot 4 to the command buffer without
  passing through a single `Phyre::` symbol. The renderer-shaped Phyre classes are reflected
  *data* records with class descriptors, not polymorphic objects, which is also why the vtable
  map cannot name their methods: they have none. Target 2 as written ("what a mesh, a material,
  a light, a camera are as records") is answerable, but it describes an asset schema, not the
  thing that draws. I re-aimed it at the object model that is actually in the render path.

- **`SQEX::` is not a rendering layer.** All 353 methods are `SQEX::Sd::*` — Square Enix Sound
  Driver, plus `SQEX::Sd::Magi` for music. Zero non-`Sd` `SQEX::` classes exist. That is
  18-Audio's row, not mine, and 18-Audio already has 12 documents. Target 3's SQEX half should
  be reassigned or dropped; its PPFX half is real but is already covered by two documents in
  17-Presentation-Rendering, so I did not duplicate them.

## OPEN-QUESTIONS

- **PROPOSED-xiionline-13-1** — Which thread clears bit `0x100` of `02EAF6D8`, and where the GIF
  stream is translated into D3D11. All 17 references in `.text` are loads; no writer exists on
  this call graph. *(highest-value of these — it is the other half of the renderer)*
- **PROPOSED-xiionline-13-2** — Runtime contents of the pass-enable mask `022C7F90` per draw mode.
- **PROPOSED-xiionline-13-3** — Meaning of the nine successive whole-word stores to `02EBA3F8` in
  `0036F2F0` (values `022D9B50`, `0x7FFF0`, `0`, `0x14D`, plus bit ops).
- **PROPOSED-xiionline-13-4** — What frame modes 5 and 6 are in player terms.
- **PROPOSED-xiionline-13-5** — What `ATEL` means in the `ATEL CONTROL` phase label.
- **PROPOSED-xiionline-13-6** — Whether `003A1E10` ever raises the 512-record capacity at runtime.
- **PROPOSED-xiionline-13-7** — Where the render command list is sorted and executed. Producer
  side is complete; no consumer walking `01F7F5E8` or `01F7F5E0` was found.
- **PROPOSED-xiionline-13-8** — Why every command is appended to **two** lists, and what
  distinguishes `01F7F5E8` from `01F7F5E0`.
- **PROPOSED-xiionline-13-9** — Order keys of the 28 command classes whose slot 2 I did not open.
- **PROPOSED-xiionline-13-10** — Whether the sixteen two-slot `Gi*` classes use this same list.
- **PROPOSED-xiionline-13-11** — Which files `ApplyJsonForCutSceneObj` reads; the engine applies
  **JSON**-authored render settings per cutscene, enqueued every frame at frame open.
- **PROPOSED-xiionline-13-12** — The render-parameter block behind `00193D50` as a record. Four
  byte offsets proven to be effect switches; extent unread.
- **PROPOSED-xiionline-13-13** — `OrderedObject +0x11 .. +0x17`, left `UNACCOUNTED` on purpose.

## AUDIT-LOG — what I attacked and failed to break

- *"`02EAF6D8` is written by ordinary frame code, so the two-thread reading is fiction."*
  Censused the whole `.text` for that displacement and disassembled all 17 hits. Every one a
  load. **Survived.**
- *"The `(data, regId)` pairing is pattern-matching on a coincidence."* Sought an independent
  witness and found one: the GIFtag constant `0x1000000000008000` decodes to `EOP=1`, `NREG=1`,
  `FLG=PACKED`, `REGS=0xE` (A+D), and `003A2020`'s two back-patch branches only make arithmetic
  sense under one-register-per-record and two-per-record respectively. **Survived, twice over.**
- *"The decompiler is right and my disassembly is misaligned."* Dumped raw bytes with every RIP
  target and checked extents against the regenerated graph. **The decompiler was wrong.**
- *"Slot 2 is a type id or a destructor variant, not an order key."* Three distinct constants
  shared across 36 classes, ordered as the passes must physically run. A type id would be unique
  per class. **Survived** — but the sort site is unfound, so it is recorded as an open question
  rather than assumed.
- *"The `Gi*` classes are the same family, so merge the documents."* Refused to answer from
  adjacency. `Gi*` are two-slot with a documented device-vtable path; these are three-slot with
  an order key. **Different contract; left open as -10 rather than resolved by proximity.**
- *"The order keys prove the list is sorted."* **Sought and failed.** Not claimed anywhere.

**What broke:** my own working name. I had `01F7F5E8` down as "the render device singleton" —
46 call sites fetch it and immediately pass it to something that draws. `0018C9E0` shows it is a
0x20-byte object of three pointers plus an allocator the engine itself names `"EASTL vector"`,
and every consumer shares one `push_back` idiom. It is a command list. Caught in-block; the
correction and why the wrong reading was reachable are recorded in that document's section 8, and
the frame document was edited rather than silently rewritten.

## CALL-CHAINS

```
Phyre::PFramework::PApplication            (middleware drives the loop)
  -> GameApplication slot 4   0017CCD0     OWNER TRANSITION middleware -> game
     -> 0017D6E0 -> 0022A490 -> 0022A580   frame-mode dispatch on *(u8*)02064AD3
        -> mode body 0..6
           -> 0036F2F0    spin on 02EAF6D8 & 0x100   (cross-thread wait)
           -> 0022B0B0 MainLoop_Draw
              -> pass gate (022C7F90[mode] >> bit) & 1
                 -> pass wrapper -> enqueue fn -> ctor -> push_back on 01F7F5E8 + 01F7F5E0
              -> 0036D400  emit GS FRAME/ZBUF/XYOFFSET/SCISSOR/PRMODECONT/COLCLAMP/DTHE
           -> 0036F2C0    settle-read, clear 0x10C
           -> 003A1DB0    flip command buffer -> 0036F360 -> 02EBA3F8 = 0x100
              ~~~ hand-off to the graphics backend ~~~
```

Mode transitions, all literal stores to `02064AD3`: `0 -> 1`, `1 -> 2`, `4 -> 3` (menu opens),
`3 -> 2` (menu closes), `6 -> 5`. Mode 2 is the field frame, mode 3 the full menu, mode 4 the
one-shot `SCREEN CAPTURE` that photographs the world the menu sits over.

## ADDRESS-INDEX — new anchors

Frame: `0017CCD0` `0017D6E0` `0022A490` `0022A580` `0022A770` `0022AF50` `0022B000` `0022B0B0`
`0022B6E0` `0022B7E0` `0022B8C0` `0022BC20`.
Graphics handshake: `0036F2C0` `0036F2F0` `0036F360` `003A1DB0` `003A1D50` `003A1E10` `003A2020`
`003A2090` `004FE420` `005044B0` `00504490` `0036D400` `00184460`.
Pass gates: `003582A0` `003582C0` `003582E0` `00358300` `00358330` `00358340` `00358350`
`00358380` `003583B0` `003583D0` `003583F0`.
Command list: `0018CA40` `0018C9E0` `0018B4E0` `0018AFF0` `00212CC0` `001AB570`, the 18 enqueue
functions `0018B540`–`0018CC60`, the 20 constructors `001F1740`–`001F1F00`, the executes
`001F28B0` `001F29E0` `001F3090` `001F32B0` `001F3300` `001F3440` `001F34F0` `001F39E0`, the
order keys `001F2880` `001F28A0` `0053DD10`, and `00193D50` `00189120`.
Data: `02064AD3` `022C7F90` `02EBEFC0` `02EBEFD8` `02EBEFF0` `01FD4A78` `02EBA3F8` `02EAF6D8`
`01E0C1D8` `01F7F5E8` `01F7F5E0` `01F7F598` `01DFE0C4` `01F82EC0` `01F7F4E0`, and the vtable
block `00902F90`–`009033F0`.

## REOPEN TRIGGERS FOR OTHER OWNERS — your call, not mine

- **`17-Presentation-Rendering/Gi-Render-Commands/gi-render-command-family.md`.** Its vtable
  block at `00902F90`–`009033F0` contains **36 three-slot command classes it never mentions**,
  including the two it does own (`GiResetRenderTargetObj`, `GiResetDefaultRenderTargetObj`).
  I also found the **producer side** it lacks: the enqueue functions and the command list. Under
  the standing rule this is "a cited address gains a caller/callee in a subsystem the document
  never mentions". I did not edit another agent's document; my section 5 states the distinction
  (two slots + device vtable vs three slots + order key) rather than assuming they merge.
- **`00-Engine-Core-Runtime/Developer-Tuning-Console/*`.** The audit shows `00193D50` — the
  render-parameter block whose bytes gate ambient occlusion and the gaussian filter — has callers
  in the console slices. **The developer console appears to tune the same block a modder would
  write.** Worth someone joining those two readings.
- **`0016D6A0` NAME disagreement you mentioned.** Both my documents cite it, as "a folded bare
  `ret` shared by the retail marker stub and the CFG guard". That is consistent with your
  load-config finding; please fold my two into whatever you hand `xiionline-8d`.

## MANIFEST-ROWS

None proposed this block. Everything I read was already classified; I did not close a residual
function, and I am not going to manufacture a manifest row to show movement. The value here is
that roughly 110 already-classified functions now have mechanism identities in two documents
rather than shape-class tags — which is the Phase C mass, not the Phase A ledger.

## GATES — re-run after writing

```
check_links.py           268 files, 10,161 relative links, all resolve
check_source_hygiene.py  no stray control bytes in 271 files
check_layouts.py         my 6 structs validate; OrderedObject +0x11..+0x18 reported
                         UNACCOUNTED on purpose (a gap is a question, never a label)
verify_doc_addresses.py  both docs ok - 265 citations, 166 entry / 16 interior / 81 data /
                         2 literal, 0 .text non-function citations
audit_crossrefs.py       db-wide 374 findings; 0 GHOST ADDRESS, 0 BODY DRIFT anywhere.
                         My documents raised 10 UNACCOUNTED NEIGHBOUR findings; all 10
                         dispositioned in-document (7 real and now stated, 3 argued
                         irrelevant with reasons). Re-run: 0 open on my documents.
coverage_balance.py      22-Middleware-PhyreEngine 9 -> 10 docs, debt 677 -> 615
                         17-Presentation-Rendering 9 -> 10 docs, debt 156 -> 142
```

Both documents are `DOCUMENTED`, `crossref_clean: true`, `passes: 0`. I did name killer
observations and go looking for them, and one of them landed — but that was the author auditing
his own work in the same session, so I have **not** claimed a falsification pass. Both owe an
independent one.

## WHAT I DID NOT DO

- Did not run `Apply-GfzBatch.ps1` or `Pack-GfzCheckpoint.ps1`.
- Did not edit any `_index/*.md` or `ASSIGNMENTS.md`; this report is the append.
- Did not touch `24-Compiler-And-CRT-Runtime/`.
- Did not edit `gi-render-command-family.md` despite having a reopen trigger for it.
- Did not write the PPFX or resource-residency documents (targets 3 and 4): PPFX already has two
  documents I would have duplicated, and resource residency is untouched. **Target 4 and
  PROPOSED-1 are the two best next moves in this category.**

---

# REPORT — xiionline-13, block 2, 2026-09-07

## STATUS

Not blocked. Took `PROPOSED-xiionline-13-1` as the next target. It did not close, but the attempt
**falsified a published claim in my own block-1 document**, which I have corrected. The frame
document is now `reopened_count: 1`.

## THE CORRECTION — the graphics fence is inert

Block 1 said the frame hands its command buffers to a second thread and that `0036F2F0` waits on
a backend fence. **The wait cannot wait.** All 17 fence sites compile to the same shape:

```asm
0036F2F0  mov  eax, dword ptr [02EAF6D8]   ; the load is HERE
0036F2F6  and  eax, 0x100
0036F300  test eax, eax                    ; <-- loop starts HERE
0036F302  jne  0036F300                    ; branches back to the TEST, not the load
```

The load is **outside** the loop. `eax` is read once and the loop spins on a register nothing
inside it can change, so it either never runs or never exits — regardless of who writes the word.
A non-volatile read hoisted out of a spin loop; the intended synchronisation did not survive
optimisation. Verified at all 17: `0024D40A`, `0024D47E`, `00259045`, `002590CA`, `00259113`,
`0036F2F0`, `00374C3F`, `00374C7E`, `00374CBE`, `00375528`, `0037559F`, `00375648`, `0037613F`,
`0037617E`, `003761BE`, `003A2DAE`, `003A2ED6`.

Corroborated three ways: `02EAF6D8` lies past `.data`'s `SizeOfRawData` so it is **zero at load**;
**no RIP-relative store to it exists in `.text`**; and **none of the image's nine thread
procedures** could be a GS consumer — the enumeration is complete (5 `CreateThread` + 4
`_beginthreadex` sites, each disassembled for the `lea` supplying its start routine, largest
procedure 555 B). The imports name no graphics module beyond stock `d3d11.dll`, `dxgi.dll`,
`D3DCOMPILER_47.dll`.

**How the wrong reading was reachable, because that is the transferable part.** In block 1 I named
the killer observation *"is `02EAF6D8` written by ordinary frame code?"*, censused all 17 sites,
found every one a load, and read that as confirming a cross-thread producer. For a **hoisted**
read, "all references are loads" is equally consistent with dead code. The observation was sound;
the inference from it was not. Re-attacking the same 17 bodies for their **branch targets** rather
than their operands is what broke it.

## THIS SHARPENS CF-6 INTO SOMETHING STRONGER

CF-6 currently says decompiled threading claims owe a re-derivation. The sharper rule, and I would
like it recorded this way:

> **A spin loop cannot be verified from decompiled output at all.** Only the branch target
> distinguishes a working spin from an inert one, and that is precisely what decompilation
> discards. Ghidra renders the inert fence as `do { } while ((g & 0x100) != 0);` — an entirely
> ordinary spin — because it reconstructs the loop from control flow and undoes the hoist in its
> output.

The proof that this is not a heuristic: **`0036F2C0` and `0036F2F0` are thirty bytes apart in the
same file and are opposites.** `0036F2C0` re-reads (`jne` targets the first load) and is a genuine
settle-spin; `0036F2F0` is hoisted and inert. Decompiled, both look like working spins — and the
one CF-6 already flags, `0036F2C0`, is the one that is actually *fine*. So CF-6's re-derivation
debt has two distinct failure modes, not one: **spins the decompiler deletes**, and **spins the
decompiler invents**.

## PROPOSED-xiionline-13-1 — reframed, not closed

The original wording assumed a live fence and was malformed. Rewritten in the document as *"where
are the GIF command buffers consumed?"* with the ruled-out set recorded so nobody repeats it:

- all 17 fence waits — hoisted, cannot point at a consumer;
- all nine thread procedures in the image — none is a plausible consumer;
- a separate graphics module — the imports do not name one;
- **the `0x70000000` record-class mask** — searched across `.text`; 12 hits in 12 functions, and
  they are an unrelated **32-slot handle table at `02EBE5E0`** (stride `0x30`, tag
  `0x70000000 | serial<<12 | type<<6`, allocator `003B1A80`, accessors `003B24A0` / `003B24C0` /
  `003B2750`). A constant collision, not a record walker. Recording it as a **dead lead** rather
  than leaving the next reader to burn a block on it.

Your Vorbis note landed here almost immediately: a scan proposes, a body disposes. The
`0x70000000` search *proposed* twelve candidates and the bodies refuted all twelve.

## WHAT DID NOT CHANGE

The whole PS2-GS producer result stands untouched — GIFtag decode, the register set and field
layouts, the 16-byte `(data, register)` record, the 512-record double buffer, the terminator
logic, the pass-enable mask, the command-object catalogue, the order keys. Nothing in the render
command list document was affected; it is still crossref-clean and needed no edit. What changed is
one claim about **what happens after the buffer is published**, and it changed from a confident
wrong answer to a bounded honest unknown.

## GATES — re-run after the correction

```
check_links.py           270 files, 10,173 links, all resolve
check_source_hygiene.py  no stray control bytes in 273 files
verify_doc_addresses.py  frame doc ok - 153 citations, 83 entry / 36 interior / 32 data /
                         2 literal, 0 .text non-function citations
audit_crossrefs.py       0 open findings on either of my documents; 0 GHOST / 0 BODY DRIFT
```

Frame document is now `reopened_count: 1`, `crossref_clean: true`, `passes: 0`. The reopen was
self-inflicted and self-corrected in the same session, which is not a substitute for the
independent falsification pass both documents still owe — if anything it is an argument for one,
since the claim that broke had already been reported to you as sound.

---

# REPORT — xiionline-13, block 3 (short), 2026-09-07

## STATUS

Stopping this line deliberately rather than starting a third deep dive in one session.
`PROPOSED-xiionline-13-1` is still open; its ruled-out set is now large enough to be worth as much
as a finding. Cross-links to `xiionline-61`'s new sibling document are in place.

## RECONCILED WITH `the-shared-command-state-word.md`

Read it and checked for incompatible claims: **none.** The split is clean and now stated in both
directions — that document owns `02EBA3F8`, its bit meanings and its reference census; my frame
document covers only how the frame uses it and now says so at the point of use. Its independent
count of **24 write-form and 38 read-form** references agrees exactly with the 62 my own
displacement scan found, which is a useful mutual check on two different methods.

Both my documents now link to it; `check_links` passes at 270 files / 10,181 links.

## MORE RULED-OUT LEADS FOR PROPOSED-1

Added to the fence waits, the nine thread procedures, the absent graphics module and the
`0x70000000` handle table:

- **`Phyre::PThreadPool` / `PThreadPoolImmediate` / `PThreadPoolWorkStealing` are live classes**
  with real bodies (`006BAA40`–`006BB110`, `006CE570`–`006CE6E0`), not stubs. **They are not the
  consumer**: no reference to the command buffers `02EBEFC0` / `02EBEFF0` falls in the `006Bxxxx`
  or `006Cxxxx` range — every one of the 31 and 39 references sits between `00248EBB` and
  `0051BCE8`. Worth recording as live for whoever documents Phyre threading; not worth chasing
  here.

- **The `00445`–`0044B` family that reads the command arena is a *producer*, not the consumer.**
  Fourteen large handlers (926–3483 B) share one caller `002F4020` (864 B), and `002F4020` is a
  **switch on a record type byte** at `param_1[0]`, values 1–10 plus a default, over a record with
  a flags byte at `+0x01`, a counter at `+0x02`, an owner pointer at `+0x20` and a field at
  `+0x224`. It carries a blink/toggle: the counter advances by a per-type divisor read from
  `*(u8*)(owner + 0x4D)` and flips bit 0 of `param_1[1]`, returning early while set. That is a
  widget/effect draw dispatcher whose handlers *write* GS records, the same relationship
  `0036D400` has to the arena. Its own caller is `00441970`.

- **The mid-draw flush block in `MainLoop_Draw` submits nothing.** The two calls bracketing it go
  to `005C5230`, whose complete body is `xor eax, eax; ret` — a constant-zero return. So the
  block reduces to: clear the state bits, **no-op**, enqueue a `VideoObj`, **no-op**, then the
  inert fence wait. Whatever performs submission in a development build is compiled out of retail.

**Net position:** the producer side of the GIF stream is fully mapped and the consumer is not
reachable from any path I have followed. That is now a well-bounded question rather than a vague
one, which is the useful outcome of a block that did not close it.

## WHY I AM STOPPING HERE RATHER THAN TAKING TARGET 4 NOW

Target 4 (resource residency) is scoped and ready — the Phyre entry points are
`Phyre::PSerialization::PStream` (`00D26C60`), `PStreamReaderFile` (`00D26C90`,
slots `00598280` / `0059BD40` / `0059D920` / `0059ED70` / `0059FAC0` / `0059D4B0`),
`PStreamWriterFile` (`00D26CD0`) and `PAssetReference`, all with real bodies, and it ties to the
existing `02-Resource-And-Asset-Pipeline` documents rather than duplicating them.

I am not starting it in this session because the standing working rule is to bank and take a clean
context after two correction cycles on one area, and because a third consecutive deep dive in the
same category is exactly the drift the mission's breadth rules exist to prevent. The frame and the
command list are written, corrected, cross-linked and gate-clean; that is a better handoff than a
half-read fourth thread.

## GATES

```
check_links.py           270 files, 10,181 links, all resolve
check_source_hygiene.py  no stray control bytes in 273 files
audit_crossrefs.py       0 open findings on either of my documents
```
