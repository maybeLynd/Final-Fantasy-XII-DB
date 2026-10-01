# Evidence standard

Every claim in this database must be traceable to one of the tiers below. A document that
cannot cite a tier for a claim must state the claim as unknown instead.

This is inherited from the GFZ build standard and is not negotiable — the project already
lost 182 classifications once by relaxing it.

---

## Evidence hierarchy — strongest first

| Tier | Evidence | Notes |
|---:|---|---|
| 1 | **Complete exact-current function body** | Disassembly/decompilation, control flow, field accesses, constants, loops, native ABI. The primary authority. |
| 2 | Authored/runtime **strings** directly tied to the body or its data | e.g. `MWeather`, `DecideButton`, the Weather Slot debug format string |
| 3 | **Qualified symbols**, when genuine | `…@Phyre@@`, std/EASTL mangled names |
| 4 | Real MSVC **RTTI / vtables / class descriptors** with independently verified object identity | ~2,350 `type_info` class markers ship in the EXE |
| 5 | **Exact-body clones** with unanimous interpretation | identical bytes, already-classified twin |
| 6 | Coherent **upstream source / library** match | Bullet, Lua, zlib, Vorbis, EASTL |
| 7 | Genuine typed pointer / vtable / **static registration** evidence — *after excluding exception metadata* | see banned list |
| 8 | Actual code **address-taking / data references** | real `.text` references only |
| 9 | **ff12-script / EBP / VBF** and other authored game-data schema | proves authored intent, never ownership |
| 10 | **Runtime evidence** — LiveLab, DynamoRIO traces, Cheat Engine | when it materially improves certainty |
| 11 | **Call graph / neighbourhood** | supporting context only, never a primary claim |

A stronger later source may supersede an earlier tentative label. When that happens, record
the correction *and the reason* in the document's §8 — do not silently rewrite history.

### Tier 10 has no "different build" caveat — the runtime target is the same bytes

Verified 2026-09-02. The playable client used for live work,

```
D:\FFXII MP Mod\FFXII_TestClient1\x64\FFXII_TZA.exe     32,864,752 bytes
SHA-256 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
```

is **byte-identical** to the EXE embedded in the certified GZF (`$GfzAuthorizedExeSha` in
`Tools/ghidra/run/GfzEnv.ps1`, reproduced by `ExtractEmbeddedOriginal.java` during every
`Verify-GfzCheckpoint.ps1` run). It is the unmodified shipping binary, not a patched test build.

Why this matters: a runtime observation and a static reading here describe **the same instruction
bytes at the same image base** (`0x00120000`). So a Cheat Engine read or a live trace may be used
to *falsify* a static claim directly, with no "the client may differ" escape. That escape was never
available anyway — but it also cannot be *invoked* to dismiss an inconvenient runtime result.

Tier 10 is still tier 10. Runtime evidence breaks ties, catches a misread, and answers "does this
path ever actually execute?" — it does not outrank a complete exact-current body, and a single
observed value never establishes a general rule. Re-verify the hash if the client is ever replaced.

### A name oracle is tier 9 until it is joined to the binary — then it is tier 2

Added 2026-09-03. The game ships **two large plain-text corpora that name the engine's own
internals**, and they take the same standing as `ff12-script` does for EBP: **an oracle, never an
authority.**

| corpus | size | what it names |
|---|---|---|
| `jsondata/maps/*.json` | 459 files, **175 distinct keys** | per-area rendering parameters — `mDofFocusDistance`, `mSAOBiasSce`, `mShadowValueLerpMinForMap` |
| `jsondata/cutscenes/*.json` | 337 files, keyed `Cut 1`…`Cut N` | the same vocabulary, per camera cut |
| `prefetchdata/<lang>/*.txt` | ~1,040 per language × 9 | which assets each scene loads, and its declared total size |

**A key in an authored file proves what the authoring tool called a value. That is tier 9 —
*proves authored intent, never ownership*.** On its own it may not be used to name a field.

**But the join promotes it.** `census_jsondata_names.py` asks whether the shipping binary contains
each key as a literal string. **137 of 175 are present.** A key that is present is no longer merely
authored: it is a **string tied to a body — tier 2 — one xref from the function that reads it**, and
therefore a legitimate route from an authored name to a struct field.

So the rule:

- **Key present in `.text`/`.rdata` → cite at tier 2**, with the string's VA, and name the reader.
- **Key absent → tier 9, and it may not name anything.** It is a lead for a corpus survey, nothing
  more.
- **Never cite the corpus for a field the binary does not mention.** That is the whole failure the
  tier-9 cap exists to prevent, and a plain-text name is unusually persuasive precisely because it
  looks like source.

> **The absent half is evidence of something else entirely.** Of the 38 keys with no literal, **27
> carry authoring-tool markers** — `mCascadeNumberCheckBoxCheckState`, `mCascadePartition0Lock-
> CheckBoxCheckState`. **Square Enix's internal lighting-editor UI state ships inside the retail
> game data.** And the two signals agree perfectly: **no tool-marked key is in the binary, and none
> of the 137 present keys is tool-marked.** Two independent classifications with zero
> contradictions is evidence; one signal renamed twice would not be.

**Absence of a literal is still not proof of inertness** — the standing rule, established by
`PClusterHeaderBase` (eighteen recovered fields, zero name strings). A reader dispatching on a hash
needs no literal. Write *"no reader found by string search"*, never *"unused"*.

**With one properly controlled exception**, which is what a positive control is for:

```
mMapAmbientColorR   in 70 files   008FA750
mMapAmbientColorG   in 52 files   008FA768     <- three siblings, consecutive, all found
mMapAmbientColorB   in 46 files   008FA780
mMapAmbientColorA   in 18 files   -- no literal --
```

**The instrument demonstrably finds this family, and does not find the alpha.** That is an absence
claim with a control, which the standard permits — and it is a real modder fact: the alpha is
authored in eighteen files and read by nothing.

### A companion binary is tier 1 about itself and tier 9 about the game

Added 2026-09-03. The install ships **more than one executable**, and one of them is not native:
`FFXII_TZA_GameSetting.exe` is a **managed .NET assembly** (verified — CLR data directory at RVA
`0x2008`, size 72), as are `SharpDX.dll` and `Steamworks.NET.dll`.

Managed code decompiles to near-source, so the temptation is to read it as tier 1. **It is not, and
the reason is the same one that caps authored game data at tier 9:**

> **Fidelity is not ownership.** A perfect reading of the settings tool tells you exactly what the
> *tool* does. It tells you what `FFXII_TZA.exe` does only to the extent that the two agree — and
> the interesting cases are precisely the ones where they do not.

So the rule, stated once:

- **Tier 1 about the companion binary itself** — its own methods, constants and validation.
- **Tier 9 about the game** — *"proves authored intent, never ownership"*, exactly as for EBP and
  VBF schema. A value the tool refuses to write is **not** a value the game refuses to read.
- **The companion binary's own SHA-256 must be recorded** in `verified_against:` beside
  `exe_sha256`. A document resting on a second binary and stamping only the first is claiming
  provenance it does not have.

This matters immediately: the database documents the `GameSetting.ini` **reader** (the `0x65C`
singleton at `0x01F82D20`). The **writer** is the managed tool. Where they disagree about a valid
range, **the binary wins and the disagreement is the finding.**

---

## Banned as proof — absolutely

Never use any of these to establish semantics, ownership, or registration:

- caller ownership → callee ownership
- address adjacency or address-range ownership
- "it looks like it belongs to X" without complete mechanics
- incoming owner references **alone**
- generic classification applied to reach a coverage percentage
- a stale residual/evidence list after a mutation
- PE `.pdata`
- PE `.xdata`
- unwind records (`PEx64_UnwindInfo`)
- EH maps
- IP-to-state maps (`IPToStateMapEntry`)
- `_IMAGE_RUNTIME_FUNCTION_ENTRY` records
- exception tables misread as callback/vtable/registration tables

### Why this matters here specifically

Of the 382 incoming data references to the 160 currently-unresolved functions:

| Count | Type | Usable? |
|---:|---|---|
| 199 | `PEx64_UnwindInfo` | ✗ banned |
| 160 | `_IMAGE_RUNTIME_FUNCTION_ENTRY` | ✗ banned |
| 6 | `IPToStateMapEntry[...]` | ✗ banned |
| 16 | real code references (13 functions) | ✓ |

An earlier branch (`CS`, 99.00422 %) treated the banned classes as registration evidence.
The corrected audit re-proved 186 rows and **rejected 182**. Those 182 must never be
restored without new independent proof.

---

## The two independent layers — one label per function

Do not collapse these. Cross-layer overlap must remain **0**.

> **"INDEPENDENT" MEANS THEY ANSWER DIFFERENT QUESTIONS, NOT THAT ONE FUNCTION MAY CARRY BOTH.**
> This heading read *"orthogonal"* until 2026-09-13, and that word invited the opposite reading —
> orthogonal usually means *independently assignable*, which would make the `overlap = 0` rule two
> lines below a contradiction. **It is not a contradiction and the rule is real: one label per
> function, stated here in the imperative and enforced by the checkpoint verifier.** The worked
> example below is about **two functions**, a caller and a callee, not one function wearing two
> labels. *(Raised as `FABLE-NOTICE-OPUS-LAYER-OVERLAP-RULE`; the notice's premise is corrected and
> its consequence is accepted — see **The 9,409** below.)*

**`PrimaryOwner` (V120)** — *which FFXII subsystem owns the state/resource/lifecycle
transaction?* An authority classification. Never inherited from callers, address
neighbourhoods, references, or convenience.

**`CodeDomain` (V121)** — *what mechanism/library/runtime behaviour does this function
implement?* May describe generic maths, containers, middleware or rendering without
granting any ownership.

Worked example: `002F7380` is called only from a **Movement**-owned dirty dispatcher, but
its complete body manages a **Presentation** Legacy PS2 GS texture budget. Movement owns the
upstream resource/dirty transaction; the callee's CodeDomain is Presentation. Caller
ownership is not inherited.

**And the ledger agrees with the example, which is the check that matters.** `002F7380` carries
`owner` **empty** and the single tag
`GFZ.V121.CodeDomain.Presentation.LegacyPS2GS.TextureMipLocalMemoryBudgetAndReferenceSlotTableRebuild`.
**One label, the one this section prescribes.** The cross-tab over all **38,161** functions is
CodeDomain-only **28,137**, owner-only **9,409**, `FinalNoPrimaryOwner`-only **585**, neither
**30**, **both 0** *(GN161, 2026-09-14; written against 28,028 / 139 at GN158 — R109 moved the
neither-cell into CodeDomain-only)* — the rule holding, not an accident.

### The 9,409 — what `overlap = 0` costs, and how it must be read

**A consequence of the rule, accepted 2026-09-13 (OPUS).** Because the layers are mutually exclusive
per function, **the 9,409 owner-only functions were never eligible for a mechanism label.**

> **"OWNED, NO `CodeDomain`" IS NOT-OFFERED, NEVER DECLINED.** Any frontier narrative that reads a
> missing `CodeDomain` as *the classification looked at this function and could not name its
> mechanism* is wrong for every one of the 9,409, and they are **the largest non-Phyre block of the
> frontier**. EC-7 must frame them as **unclassified-by-pipeline**, not unclassified-by-difficulty.
> **This dispositions nothing and moves no metric** — it removes a reading, which is a smaller claim
> than it looks and the only one the evidence supports.

**And the verifier's `overlap != 0` gate is kept, correctly, but labelled for what it is.** It holds
at 0 because the rule is enforced upstream, so it is a **regression canary** — it would catch the
tagger changing — and **not a discriminating audit check**. `FINAL-AUDIT-PROTOCOL` pass 12 must say
so of its half one; **half two, the document-frontmatter conflation hunt, is the half that
discriminates.** No GFZ edits are requested and none are licensed by this ruling.

---

## Naming discipline

- Prefer a mechanism-level name you can prove over a friendly name you cannot.
- Do not attach a player-facing label (a menu name, an effect name, a status name) unless an
  internal binary/resource/script bridge closes it.
- Keep numeric identities numeric when unproven — e.g. UI requests **14** and **21** are
  structurally valid slots with no recovered friendly name, and stay numeric.
- When external documentation (a wiki, a mechanics FAQ) agrees with an already-exact native
  matrix, it may be cited to attach the familiar name — as corroboration, tier 10 at best,
  never as the source of the claim.

### Address-notation discipline — a pointer cell is not its object

*Ruled 2026-09-21 (FRONTIER) on `OPUS-REQ-FRONTIER-PAGES-SPELL-A-POINTER-CELL-AS-AN-OBJECT-BASE`,
using `0209AC30`/`Manager0209AC60` as the worked example: `0209AC30` is a **pointer cell** (sole
writer `002800F0` installs `lea rcx,[0209AC60]`); the object is `0xE00` bytes at `0x0209AC60`.*

- **Canonical field spellings** — pick either, both mean `0209AC60 + 0xNN`:
  - `[0209AC30]+0xNN` — dereference-then-offset, plus **outside** the brackets;
  - `*(0209AC30) + 0xNN` — the explicit C form.
- **Banned spellings** — `[0209AC30 + 0xNN]`, `size[0209AC30 + 0xNN]`, bare `0209AC30 + 0xNN`:
  read literally they name an address `0x30` **below** the intended field, and they collide with
  the route language where `PTR a +o` evaluates `*(a+o)` — the exact transcription that produced
  CON-137's real-but-wrong live pointer this session. Prose a reader must silently repair is prose
  that gets transcribed literally into a route.
- Naming the manager `the 0209AC30 manager` is acceptable only where no field arithmetic follows;
  for the object itself prefer `Manager0209AC60` / `0209AC60`.
- The rule is not specific to this cell: wherever a document's base token is a pointer cell
  (verified single-writer install, e.g. via `ImageAddress_ResolveRuntimePointer` records), field
  arithmetic must be spelled through the dereference, never through cell arithmetic.

---

## The GFZ itself is a claim, not a source

**The GFZ can be wrong, and has been.** Its function comments, prior handoff prose, GN
addenda and sealed "evidence" records are all *claims about the binary produced by earlier
sessions* — with the same error rate as anything written today. The corrected CS audit
re-proved 186 rows and **rejected 182**: a third of that branch was wrong, and it had looked
authoritative right up until someone checked.

The authority order is therefore:

| Rank | Source |
|---:|---|
| 1 | **The binary.** Exact-current function bodies, bytes, tables, strings. |
| 2 | A **fresh derivation** from the binary, with its method stated and reproducible. |
| 3 | A GFZ **annotation or handoff document** describing the binary. |

**Source beats prose — including our own prose.** A GFZ comment saying a function does X is a
claim about that function, not the function. When a fresh derivation and a GFZ annotation
disagree, the derivation does **not** automatically lose. Weigh the actual evidence:

- How was each obtained? A direct table read outranks a prose recollection.
- How was each validated? 1,224 clean samples outranks one asserted pair.
- Is either reproducible right now? Re-derive both before choosing.

**Do not defer to the GFZ merely because it is older or sealed.** A sealed checkpoint
certifies that annotation state was *persisted correctly* — not that the annotations are
*true*. Persistence certification is about bytes, never about semantics.

When a conflict appears:

1. **Do not pick a winner by provenance.** Find the observation that settles it and go get it.
2. If the GFZ is wrong, say so explicitly and record it in `AUDIT-LOG.md` — a wrong annotation
   that stays unchallenged will be inherited by every future session.
3. If the fresh derivation is wrong, record that too, with what misled it.
4. If it cannot be settled yet, hold **both** as unresolved. Never let the older claim win by
   default.

## Falsification duty — how a claim earns the right to be called fact

**Support is not proof.** Anyone can assemble evidence that agrees with a reading they
already believe. A claim earns its place in this database only after someone has
deliberately tried to destroy it and failed.

Every claim must be attacked at least once, on the record. Writing a document is the first
half of the job; the second half is a separate pass whose explicit goal is to prove that
document wrong.

### The falsification pass

For each claim in §8, in order:

1. **State the killer.** What specific observation would make this claim false? If you cannot
   name one, the claim is not falsifiable and does not belong here — rewrite it until it is.
2. **Go looking for that observation specifically.** Not for more supporting evidence — for
   the counter-evidence. Search the binary for it.
3. **Re-derive, do not re-read.** Rebuild the call chain from the *current* call graph, not
   from the document and not from memory. A chain that was true 3,000 classified functions
   ago may have gained an edge.
4. **Attack every "Do not confuse with."** Is the distinction still real, or did it rest on
   something that has since been reclassified?
5. **Attack the ownership boundary.** Does the owner/mechanism split still hold, or did it
   quietly become caller-inheritance?
6. **Re-check for banned evidence.** Did any `.pdata`/`.xdata`/unwind/EH reasoning creep in
   through a citation chain?
7. **Verify physically.** Every cited address still resolves, with the same body extent, and
   still carries (or still lacks) the classification the document claims.
8. **Record the attack** in §10, including what you tried that did *not* break it. An
   unrecorded audit did not happen.

Run `Tools/analysis-kit/gfz-scripts/audit_crossrefs.py` before every pass. It performs
checks 3 and 7 mechanically across the whole database and will surface relationships no
human would think to re-check.

---

## Status lifecycle

`DOCUMENTED` is **no longer the completion bar.** `AUDITED` is.

| Status | Meaning |
|---|---|
| `STUB` | Placeholder. Structure only. |
| `PARTIAL` | Some sections filled; known to be incomplete. |
| `DOCUMENTED` | All eight sections filled, every claim cites a tier. **Not yet fact.** |
| `AUDITED` | Survived at least one deliberate falsification pass, recorded in §10, against a named program state. |
| `REOPENED` | Was `DOCUMENTED`/`AUDITED`; new evidence extended or contradicted it. Must return through `DOCUMENTED` → `AUDITED`. |

A document drops to `REOPENED` the moment any trigger below fires. There is no such thing as
"closed forever" — only "closed against a stated program state."

### Reopening triggers

Any one of these forces a reopen. They are not judgement calls.

1. **A cited address gains a caller or callee in a subsystem the document does not mention.**
   *This is the common one.* You document Movement, close it, and later work proves a
   Movement function feeds battle logic — the Movement document is now wrong by omission and
   reopens. `audit_crossrefs.py` detects this as `UNACCOUNTED NEIGHBOUR` /
   `NEW SINCE BASELINE`.
2. A newly classified function references a mechanism this document describes.
3. A cited address's body extent or classification changes.
4. Two documents make incompatible claims. **Both** reopen.
5. A higher evidence tier becomes available for a claim previously carried by a lower one —
   the claim must be re-derived from the stronger source, even if the conclusion is unchanged.
6. Runtime/dynamic evidence disagrees with a static reading.
7. An open question closes in a way that touches the document.
8. External source (upstream library, Workshop source, script catalog) contradicts it.
9. A superseded reading elsewhere used this document as support.

### Propagation

Reopening is transitive. If document A cited document B's conclusion as evidence and B is
overturned, **A reopens too.** Follow §9 Related links in both directions and reopen
everything downstream of the change. Record the propagation in `AUDIT-LOG.md`.

### Corrections are permanent record

When an audit overturns something, the document keeps the correction trail in §8:
what was believed, what is now believed, what proved it, and why the earlier reading was
reachable. Never silently rewrite. The reasoning that led somewhere wrong is itself evidence
about where else the same mistake may be hiding — that is exactly how the `.pdata`
contamination was caught, and it cost 182 classifications to learn.

---

## Completion bar

## Positive controls on any absence claim

**A zero from a tool that did not run looks exactly like a zero from a tool that found nothing.**

On 2026-09-02 a `strings | grep` sweep of the authorized EXE returned zero for `lua`, `luaL_`,
`__index`, `PhyreObject` and eleven other markers. The conclusion drawn — "there is no scripting
VM in this binary" — was written down and acted on. `strings` is not installed on this machine.
The command produced no output and every count was faithfully zero.

Reading the same file's bytes directly found `PhyreObject`, `_ENV`, `__index`, `__newindex`,
`bit32`, `luaopen_` and `$LuaVersion: Lua 5.2.1` immediately. The binary embeds a complete Lua
interpreter.

**Rule.** Any claim of the form "X is not present" must be accompanied by a *positive control*:
the same query, run the same way, against something already known to be present. If the control
does not come back, the tool is broken and the absence is not evidence. In that instance the
control was free — `PhyreObject` had appeared in a decompilation minutes earlier.

**Corollary on precedence.** What forced the retraction was a structural derivation from a
function body (`LUA_REGISTRYINDEX = -1001000`), not a better query. A structural proof from the
binary outranks an absence reported by tooling. Prefer reading a body over asking a tool whether
something exists.

### AMENDMENT 2026-09-08 — a positive control is necessary and NOT sufficient

**The rule above was satisfied and the negative was still false.** A hardware-breakpoint run
reported **0 hits on `003EAA70` in-world**, beside a positive control on the same instrument that
fired **127,578 times**. Every requirement was met. Armed **alone**, in the same state, the same
breakpoint on the same address recorded **1,130,002 hits in 75 seconds**.

**The control proved the instrument could SEE. It did not prove the instrument left the program
ALONE.** Two other breakpoints in that run were firing tens of thousands of times a second, and
the program under them did not merely run slower — **it stopped executing the path being
measured**.

```text
armed together   003EAA70 + 00265270 + 0020E600      003EAA70:            0 hits / 8 s
armed alone      003EAA70                            003EAA70:    1,130,002 hits / 75 s
```

**Rule.** Any instrument that can *change* the program's behaviour — a breakpoint, a hook, a
patch, a write, an injected DLL — must, in addition to a positive control:

1. **be run with the measured target ALONE.** Take the control in its own run. A control sharing
   a run with the target is a second experiment competing with the first.
2. **report its own load** — hit rate, CPU cost, wall time — so a reader can see whether the
   observation was taken under perturbation.
3. **have any negative re-taken at a lower load** before it is written down.

> **A perturbing instrument satisfies every other guard in this document and still lies.** That is
> what makes this failure mode worth its own rule: nothing already written here would have caught
> it.

### AMENDMENT 2026-09-08 (second) — a HIT COUNT is not an EVENT COUNT

The amendment above was written from a run whose numbers were themselves wrong. The same
hardware-breakpoint tool reported **133,679**, **127,578**, **255,944** and **1,130,002** hits;
every one of those is retracted as a count of anything.

**A hardware breakpoint re-fires on the instruction it just reported** unless the debugger sets
`EFLAGS.RF` and clears `DR6` before continuing. This one did neither, so it looped on a single
address at the speed of the debug-event round trip. The proof is one line:

```text
60 consecutive recorded hits on 0020E600  ->  1 distinct (thread, rcx, rdx) triple
after the fix, 300 recorded hits          ->  161 distinct triples
```

**Rule.** Before a count from any event-based instrument is written down, **show that repeated
events are distinct**. Record enough state per event -- thread, arguments, a timestamp -- to
tell *one thing happening many times* from *one thing reported many times*, and print the
distinct count beside the raw one.

> **Note what this rule would have caught and the earlier rules would not.** The instrument had a
> positive control that fired. It was run with the target alone. It reported its own load. Every
> guard passed, and the number was still an artifact of the instrument reporting itself.
>
> **A zero was never affected** -- an instrument that cannot re-report something that never
> happened. That asymmetry is why the retracted counts do not invalidate the zeroes taken with
> the same tool.

### AMENDMENT 2026-09-12 (OPUS) — a COUNT without its UNIT cannot be checked

The amendment above governs counts from an instrument that can re-report one event. This one governs
the far commoner case: a **static** count, correct as written, that no reader can reproduce because
the document never says *what was counted*.

**Six examples from one sweep, every one of them a correct number:**

| written | the unit that gives it | units that do not |
|---|---|---|
| "the **fifteen** functions that reference `01EEBCC0`" | 15 functions | 19 instructions |
| "the **21** `02EBF170` sites" | 21 name-lookup sites | 42 references here, 58 image-wide, 9 functions |
| "eleven read-modify-write masks" | 11 distinct constants | 16 instructions, 12 offsets, 9 in place |
| "**251** handlers" | a **union** of two sets | 239 + 13 = 252 |
| "**121** sites in **70** functions" | both, named separately | either alone says nothing |
| "the **23** steps" | 23 numbered steps | 39 calls to 35 targets |

**In every case the document was right and the checker was wrong**, and in every case the checker had
no way to know: "sites", "handlers", "steps" and "masks" each admit two or three readings that differ
by a factor of two or more.

**Rule.** When a count is written down, **name the unit in the same sentence** — functions, call
sites, instructions, distinct constants, union members, numbered steps. Where two units are both
interesting, give both, as the flag-bank census does with *"121 sites in 70 functions"*.

**Rule for a reader.** When a count does not reproduce, **change the unit before doubting the value**.
Six times out of six in this sweep, the value was right.

> **Why this belongs beside the event-count rule and not inside it.** That rule asks whether repeated
> events are *distinct*. This one asks what a thing *is* before it is counted at all — and unlike the
> event rule, **it bites on zeroes too**: "no writer" means nothing until "writer" is defined as an
> instruction, a function, or a path.

## A body-bytes hash cannot identify clones

Two functions may compile from the same source, decompile to character-identical C, and still
hash differently. Proven at `005847E0` vs `00584950`: 92-byte bodies, 8 differing bytes, all four
pairs the low halves of rel32 displacements, **each differing by exactly `0x170` — the distance
between the two function addresses.** No opcode or immediate differs.

Any body containing a relative call or a RIP-relative reference is position-dependent, so its
hash is too. **Never deduplicate by body hash**; it silently undercounts duplication. This is why
the evidence hierarchy carries a distinct *exact-body clone* tier rather than treating hash
equality as clone detection. It applies to both hash conventions in use here — address-salted and
plain body bytes.

## The two hash conventions, written down

The sentence above named two conventions for two years without recording what either one *is*, so
no citation in the corpus could be checked against the image. Both are now stated exactly, and both
have been reproduced byte-for-byte:

| Convention | Definition | Who produces it |
|---|---|---|
| **plain body** | `sha256(body bytes)` | ASTRA's probes — `arena_alloc_probe.py`, `arena_init_probe.py`, `cap_policy_probe.py`, `efx_rebase_probe.py` all publish `body_sha256={hex(a): sha256(b)}` |
| **address-salted** | per body range, in iteration order: `BE64(range.min) ‖ BE64(range.max) ‖ the range's bytes` | `Database/Tools/ghidra/scripts/EnrichCurrentBodyManifest.java:5`, the manifest the GZF apply gate compares |

`range.max` is **inclusive** — Ghidra's `getMaxAddress()` is the last byte of the range, so it is
`min + length − 1`. Getting that off by one produces a plausible-looking hash that matches nothing.

The distinction is not academic, and the log records the day it bit: the enricher produced
`0966b7b4…a16071` / `ed6a32eb…0140ab5` where the handoff prose quoted `c076cfea…` / `15594f61…`
throughout, and *"a hand-built manifest would have aborted"*. **All four values are correct.** They
are the same two bodies — `00313A00` at 289 B and `002F7380` at 723 B — under the two conventions,
and every one of the four reproduces from the authorised image. Neither value is a mistake for the
other; a citation is only wrong if it uses one where the reader needs the other, which is why a page
citing both writes `plain-body` beside one and `gate hash` beside the other.

## A truncated hash is a check-value, and both halves must reproduce

Almost nothing in the corpus cites a hash at full length. The normal form is head-ellipsis-tail
inside an evidence cell — `complete body of `00385F60` (2,302 B, `f887bb1f…8142`)` — and a
`[0-9a-f]{64}` sweep matches **none** of them. Anyone auditing hashes with a 64-hex regex is reading
a population of provenance stamps and will conclude, wrongly, that the corpus barely cites hashes.

**The convention: eight leading characters, then the LAST 4–8 characters of the same hash.** The
widths vary by page and that is fine — the defect is never the width, it is the value. The
convention is measured rather than asserted: the 58 truncated provenance stamps reproduce it 58
times out of 58.

**The two halves fail independently and mean different things.** Eight hex characters is 32 bits, so
a head that reproduces at the stated length means the citation names the right body, at the right
size, in the right convention. A wrong tail on such a row is four to six mis-transcribed characters
— *not* a wrong body and *not* the wrong convention. Collapsing both into "hash mismatch" would hide
exactly the distinction that matters, so `check_body_hashes.py` reports them separately.

That separation earned its keep immediately. A first sweep found 25 citations whose tails did not
reproduce, and the instinct — that the bodies or the convention were wrong — was wrong in all 25:
every head reproduced. Two error shapes were behind them, a window slipped one or two characters
early (`…f182` for `…182f`), and single-character corruption, including one `…eeee` that was a
placeholder never filled in. All 25 are corrected against recomputed values, and where the same hash
was cited in two documents the same wrong tail appeared in both — **these propagate by copying, so
they are worth correcting at the source rather than one page at a time.**

**A citation must name what was hashed.** Two rows cannot be checked at all, not because the values
are suspect but because they are hung off another function's row — a jump table and a 43-byte PSM
table with no address of their own. A hash with nothing to recompute it against is decoration.

## There are two legitimate provenances, and only one of them can go stale

A `verified_against:` block records which program state a document's claims were checked against.
Two kinds are in use, both legitimate, and conflating them has been producing a false alarm on a
red gate for as long as both have existed:

| Kind | Names | Can it go stale? |
|---|---|---|
| **GZF-derived** | `gzf_sha256` (the parent) + `snapshot_sha256` + `exe_sha256` | **Yes.** The parent advances, and the stamp falls behind. |
| **Image-derived** | `exe_sha256` + `method:` — what was disassembled and how | **No.** It never referenced a parent, and the authority EXE hash is fixed. |

**An image-derived document is not a GZF-derived one missing its stamp.** Its evidence is the
binary: *"disassembled from the shipping EXE with every RIP target computed by a tool"*, *"a
read-before-write liveness worklist validated against 46 contract-stated signatures"*. `CLAUDE.md`
ranks the shipping EXE and a directly verified native body as **native semantic authority**, above
prose and handoffs; a GZF parent is a prior session's annotation *claim* about that same binary, at
the same error rate as today's — which is precisely the reasoning the corpus already used when it
refused to treat GFZ tag names as evidence.

**So stamping an image-derived document with a `gzf_sha256` would make it worse**, not better: it
would attach a dependency the document does not have, and assert a verification against a parent
that was never consulted.

**Measured, 2026-09-14:** of 365 system documents, **242 GZF-derived, 117 image-derived, 6 with no
block at all**. Every one of the 117 carries the authority EXE hash — **zero wrong hashes**. And of
`check_provenance`'s 130 documents reported as having no `snapshot_sha256`, **117 are image-derived
and never used a snapshot**; the real snapshot debt is **13** — 7 GZF-derived documents genuinely
missing the line, plus the 6 with no block.

> **This is not a metric made to agree by weakening evidence.** Nothing is reclassified to make a
> number fall: the 117 documents' evidence is unchanged and their EXE hashes were checked, not
> assumed. What changed is that a checker was asking a GZF-shaped question of documents whose
> evidence is the image.

**The minimum a block must carry**, stated because its absence is why four different shapes coexist:

- **GZF-derived:** `gzf_sha256`, `snapshot_sha256`, `exe_sha256`.
- **Image-derived:** `exe_sha256` — which must equal the authority hash — **and `method:`**, naming
  what was read and how. An `exe_sha256` alone says a document was checked without saying against
  what part of the binary or by what procedure, and **72 of the 117 are currently in that state**.
  They are not false provenance; they are thin, and filling them in is real work rather than a
  relabelling.

## A transferred stamp: how a verification carries to a later parent

`check_provenance` is right that a stamp must never be rewritten — advancing a `gzf_sha256` asserts
a verification that never happened. But a verification can still *hold* against a later parent, and
when it provably does, saying nothing is its own kind of inaccuracy: it leaves a document looking
unverified against a state it is in fact verified against.

**The witness is the annotation snapshot, not the function census.** This was adjudicated
2026-09-14 (`OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144`, FABLE, commit `9bedb5e0`) after I proposed the
census and was wrong twice over: the export I used is timestamped **twelve minutes before the GN158
pack**, so it was not the generation I labelled it, and a census records comment *length* with no
prototype, calling convention or namespace — it could not witness what I asked of it. The
`GFZFunctionAnnotationSnapshotV2` files named by `snapshot_sha256` carry full per-function records,
and against those the real movement is **19 functions GN158→GN160 and 15 GN159→GN160, plate comment
and tags only, embedded EXE identical.**

**So a transfer is written as a new field beside the original, never over it:**

```yaml
verified_against:
  gzf_sha256: 2ed8affb…          # untouched: the parent the verification ran against
  snapshot_sha256: 46f02e26…     # untouched: the witness it is transferred on
  exe_sha256: 73461d08…
  transfers_to:
    parent: fa0db293…            # the certified parent it also holds against
    basis: snapshot-identity     # every function this document cites has byte-identical
                                 # per-function records in both snapshots
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0)
```

**What a transfer does NOT cover, and it must be stated rather than implied.** Neither witness
covers non-function symbols, the DTM, instruction-address comments, equates or reference overrides —
**and decompiler output depends on all of them.** A document that quotes decompiler state
(`DAT_`, `param_`, `local_`, `undefined`, `PTR_`, a cast) is therefore *not* transferable on snapshot
identity alone: it needs a symbol + DTM + comment export diff, or a targeted re-read. Of 176
documents re-sorted, **103 are function-identical, 53 of those also quote decompiler state, and 20
sit in a genuine snapshot delta** (`_index/candidates/provenance-snapshot-resort.tsv`).

> **Token absence supports a transfer; it does not prove one.** A page that happens not to write
> `DAT_` may still rest on a decompilation. The class is a filter for who must be re-read, not a
> certificate — which is exactly why the transfer records its basis instead of just its conclusion.

### The second basis: an additive-annotation delta

A document that *does* cite a changed function can still carry, and the reason is measurable.
Adjudicated 2026-09-14 (`OPUS-REQ-FABLE-DELTA-RELIANCE-BASIS`): **all 19 GN158→GN160 and all 15
GN159→GN160 differing records are purely additive** — the plate comment and the repeatable comment
are *empty in the stamped snapshot*, and the stamped tag set is a *subset* of the certified one,
19/19 and 15/15.

**So a document verified against the stamped generation cannot have relied on the added text,
quoted or paraphrased: in that generation it did not exist.** That is a stronger result than asking
whether the document quotes a tag — the test I first proposed, which could not see a paraphrase and
said so.

**The only claim an additive delta can falsify is an absence claim** about those functions —
*unclassified*, *untagged*, *no annotation*. Fourteen such sentences were found, five were genuinely
stale and are corrected; the rest were scoped to the old state, self-aware, link text, or
append-only history.

> **What voids this basis, recorded in every stamp that uses it:** any delta that **removes or
> rewrites** a comment, tag, name, prototype or body range. Additivity is a property of a particular
> advance, not of advances in general, so **the test is re-run at each checkpoint** and documents
> citing a rewritten function owe a targeted re-read. A stamp that does not say what would
> invalidate it is a stamp nobody can re-check.

## An experiment's `contract:` key says what it was DESIGNED to test

Not what may later cite it. The two readings look interchangeable and are not, and the difference
decides whether a correct record gets edited to suit a checker.

`EXP-005` and `EXP-006` carry `contract: none — a harness-capability question`, which is accurate:
they were not run against a contract. `CONTRACT-binding-profiles` §13 cites the live pointer chain
they resolved, which is also accurate. **Both sides are right.** A checker that asks "does the cited
record name this contract back?" will flag the pair forever, and the remedy it suggests — point the
record's key at the contract — would make the record say something false about its own design.

> **Evidence produced without the contract in view is more independent, not less.** An experiment
> designed to confirm a contract and one that happened to resolve the same chain are not equal
> evidence, and the weaker-looking `contract: none` is attached to the stronger case.

So: a record whose `contract:` key is **empty** is a bookkeeping gap worth closing. A record whose
key says **`none` with a reason** is a declaration, and a contract citing it is an ordinary
cross-reference that the corpus does not happen to index in that direction. Neither side owes an
edit.

## A generated family membership goes stale every time A grows

An EC-7 class family whose members come from a **span rule** — *"every census entry in
`[007A4380, 007F41A0)` except … entries already A-measured"* — has a **generated** member list. The
generator excludes A-measured bodies by design, so the moment anyone measures one individually the
file on disk is wrong and `check_dispositions` refuses the whole family.

**Refusing the whole family over two collisions is correct**: a declaration that is wrong about its
own membership is not partially valid. But the cost is blunt — the entire family leaves the declared
surface, and the EC-7 figure moves by its full size.

**This is not hypothetical and it is not one family.** On 2026-09-14 it fired three times in one
session: `SQEX SEAD sound library span` twice (1,216 → 1,211 → 1,210, as `007A5B50` and then
`007B1E10` were measured), and `PPFX post-effect library` once (1,657 → **1,655**, `0071D9E0`). The
PPFX break alone moved the frontier by **1,655 bodies** — 19,844 to 21,499.

> **The mechanics punish the better evidence.** An A measurement makes the surface *stronger* —
> class-explained becoming individually measured is the direction EC-7 wants — and each one
> presents as a thousand-body regression until somebody notices.

**So the rule, for any family whose members are generated:**

1. **Publishing an A measurement inside a family's span is not finished until that family's selector
   has been re-run and its declaration's member count updated.** The members file and the count are
   two halves of one statement; a file that disagrees with its declaration is the next refusal.
2. **The declaration must name its generator**, so the repair is mechanical rather than archaeology.
   Both families already do; that is why each break took a minute to fix rather than an hour.
3. **Nothing may "fix" a refusal by editing the members file by hand.** Regenerate, or the next run
   silently reintroduces whatever the rule excludes.

**And nothing catches this without a runner.** The first break sat unnoticed through several
`progress.py` reads, because the headline figure is above the disposition line. The third was found
only because `check_untouched_runs` and `check_frontier_shape` **refuse to report a percentage when
their frontier disagrees with `check_dispositions`** — a guard that exists precisely so a silently
diverging denominator stops the run instead of colouring every number below it.

## Incomplete is not the same as wrong

Two distinct GFZ failure modes have now been recorded, and conflating them would be a mistake:

- **Substantively wrong** — the ScriptVM dispatch-table index mapping, where a GFZ claim
  contradicted the binary. That one required rejecting the annotation.
- **Merely uninformative** — the Lua C API at `0x80F000`–`0x812FFF`, where 102 of 108 functions
  carry a generic shape tag (`NativeInline.*`, `NativeLeaf.*`). Every one of those tags is
  *true*. None of them says what the function is. `FUN_008119F0` is `lua_type`, tagged
  `NativeInline.BoundedLoop.NoComputedTransfer`.

The second kind is not a defect to reject, it is a gap to fill — and it is the larger share of
the remaining work. Roughly 11,800 functions carry a generic shape class.

## Citing a hub imports its whole neighbourhood

Crossref audit pass 4 flagged six new cross-subsystem relationships across two documents. None was
a discovery. All six appeared because those documents had been reopened to cite a **hub** - a small
accessor with dozens of callers - and the audit correctly propagated every one of that hub's
neighbours onto the citing document's surface.

`Actor_GetWorldPosition` has 79 callers across 12 subsystems. `WorldTransition_GetActiveOrPendingFieldId`
has 49 across 10. `BattleUnit_GetBySlotIndex` has 40 across 9. **Any document that names one of
these inherits all of them.**

The wrong fix is to enumerate the census in every citing document; that duplicates it and rots.
The right fix is an explicit **disposition by reference**:

> These edges belong to hub X, whose complete caller census is enumerated in <hub document>. They
> are not <this category> relationships.

That satisfies audit criterion 9 - every cross-subsystem neighbour is explained *or* explicitly
dispositioned with a reason - without copying data. A disposition by reference is only valid when
the hub document actually contains the census; pointing at a document that does not enumerate them
is not a disposition, it is a deferral.

**Corollary:** a rising UNACCOUNTED NEIGHBOUR count is not necessarily decay. It rose from 128 to
140 between passes 3 and 4 purely because more documents cited more real addresses. The number to
watch is GHOST ADDRESS, BODY DRIFT and CLASSIFICATION - which have been **zero in every pass so
far**.

## Compute a scan's noise floor before believing its hits

A byte-pattern scan over a 32 MB binary tries millions of positions. At that scale, **matches happen
by chance**, and the count that matters is the *excess* over the expected rate - not the raw hit
count.

Worked example, 2026-09-02: scanning `.text` for RIP-relative displacements landing inside the
persistent-flag banks returned 9 candidates across 3 functions, which looked like a finding.

```
scan positions      ~8e6 code bytes x 3 trial opcode lengths  =~ 24e6
P(random disp32 lands in a 256-byte window)  = 256 / 2^32
expected false hits, 256-byte span           =~ 1.4
expected false hits,  64-byte span           =~ 0.36
observed                                      = 2 and 1
```

**The observation was indistinguishable from noise before any verification.** Disassembly then
confirmed all nine were false: seven were not instruction boundaries, and the two that were decoded
to `test rax, rax` and `shr eax, 5` - three-byte instructions with **no memory operand**, so the
"displacement" was just the following bytes.

**Rule.** Before interpreting the hits of a wide byte scan:

1. Estimate the expected false-positive count from the window size and the number of scan positions.
2. If the observed count is within that range, treat every hit as unproven until individually
   verified.
3. Verify by checking the hit is a real instruction boundary **and** that the instruction actually
   has the operand the scan assumed.

This is the same failure family as the narrow-test false negatives already on file, inverted: there
a too-narrow test missed real things; here a too-wide test invented them. Both are cured by
characterising the instrument before trusting the reading.

## Hand-maintained indexes drift; check them mechanically

`_index/COVERAGE.md` is written by hand alongside each new document. On 2026-09-02 a first-ever
check against the filesystem found it **undercounting by 7 documents across 3 categories** -
claimed 36, actual 43.

Two distinct causes, both instructive:

- **A hardcoded count where an increment was needed.** Index updates written as
  `s/\| 16-UI \| \d+ \|/| 16-UI | 1 |/` set the count to `1` rather than incrementing it. Those
  categories already contained documents from an earlier session, so adding one *lowered* the
  recorded total. The same block of work updated another category with a lambda that incremented
  correctly - so the error was inconsistency, not ignorance.
- **Plain staleness.** `03-World-Area-Field` had drifted 2 vs 6 with no recent edit at all.

**Neither was detectable by reading the index**, which is the point: an index that disagrees with
reality looks exactly like one that agrees.

`Tools/analysis-kit/gfz-scripts/check_coverage.py` now compares COVERAGE against the filesystem and
exits non-zero on any disagreement (`--fix` rewrites the counts, leaving descriptions alone). It
belongs in the same routine as `check_links.py`: **run both before treating the index as evidence
of anything.**

The general rule: **a hand-maintained summary of machine-checkable facts must be machine-checked.**
Link resolution had such a check from the start; document counts did not, and drifted for as long
as they went unchecked.

## Never edit a provenance stamp to make a check pass

`check_provenance.py` reports that 13 of 43 documents name a parent GZF that is no longer current.
**The one-line fix is to rewrite those hashes.** It would take seconds, the checker would go green,
and the database would be worse.

A `verified_against:` stamp is a claim about **which program state a document's assertions were
checked against**. Rewriting it to the current hash asserts a verification that never happened -
it converts an honest record of debt into a false record of diligence. The check would then be
measuring nothing at all.

**The rule: a provenance stamp may only be advanced by actually re-verifying.** Re-read the cited
bodies against the current parent, confirm the claims still hold, *then* update the stamp. If the
claims do not hold, correct the document - and the stamp follows the work, never leads it.

This is the concrete form of the standing instruction that a failed audit is fixed by re-deriving
the truth, not by adjusting the text until the audit passes. The stale stamps are registered as
**AH-1 .. AH-14** in `OPEN-QUESTIONS.md` and are carried as debt.

**A useful distinction the tools now make:**

- `check_links.py` and `check_coverage.py` verify *mechanical* facts about the database. A failure
  there is a bookkeeping error and may be auto-fixed.
- `check_provenance.py` verifies a *claim about work performed*. A failure there is debt, and
  auto-fixing it would be falsification. The script deliberately has no `--fix`.

A system is `DOCUMENTED` when:

1. all eight sections of the template are filled;
2. every address cited resolves in the current parent and its body extent matches;
3. the call chain is stated in both directions;
4. §7 "What is not known" is either empty or every entry is mirrored in `OPEN-QUESTIONS.md`;
5. every claim in §8 cites a tier;
6. no banned evidence class appears anywhere in the reasoning.

A system is `AUDITED` — the actual bar — when, in addition:

7. a falsification pass has been run and recorded in §10, naming the program state it ran
   against;
8. `audit_crossrefs.py` reports no unresolved finding for it;
9. every cross-subsystem neighbour of every cited address is either explained in the document
   or explicitly dispositioned as irrelevant, with the reason;
10. every claim has a stated killer observation that was searched for and not found.

100 % explicit classification is **not** completion. Generic shape classes
(`NativeRoutine.*`, `NativeAdapter.*`, `NativeLeaf.*`, `NativeInline.*`, `NativeDispatch.*`)
account for a function without explaining it, and roughly 11,800 functions currently carry
one. Those all still owe a real document — and then an audit.

**The target is not 100 % documented. It is 100 % documented, 100 % explained, and
100 % factual — where "factual" means every claim survived a genuine attempt to kill it.**


## Suggestive evidence is not deciding evidence

Added 2026-09-02 after **four** instances in a single day. They looked unrelated while they were
happening; written down together they are obviously one error.

| What was seen | What it was read as | What it actually was |
|---|---|---|
| Multiplier constants `2`, `0.5`, `0.125` between two `ApplyElementAffinity` steps | elemental affinity — weak / half / strongly resistant | **paired** values selected by unit category; `2` and `0.5` are the *same stage* for two different categories |
| A byte tested by `PartyFollow_SolveFormation` and `Reward_Compute…ForRecipient` | "1 = party side" | also tested by `SpawnGroup_*` and `EnemyChain_UpdateOnDefeat` — one value cannot be both |
| Two slot bindings both solving to base `0x01EFA5C0` | independent confirmation | the two points are adjacent and their ids differ by 1, so **any** pair like that agrees by construction |
| A `0x3F` bound over four parallel arrays | "a 63-entry in-flight command table" | the VM's **return-value list** |

**The common shape: evidence that narrows the possibilities was treated as evidence that picks one.**
Constants, names, adjacency and array shape all *constrain* what a thing can be. None of them
*decides*. In every case the deciding evidence was one disassembly away — the branch that selects the
constant, the writer that sets the byte, a third independent binding, the store that fills the array.

**The check, before naming anything from suggestive evidence:**

1. Name at least one **other** thing that fits the same evidence. If nothing comes to mind, the
   evidence is probably weaker than it feels, not stronger.
2. Name the observation that would **separate** them.
3. Either go and make that observation, or record the reading explicitly as a lead — never as a
   finding.

Step 3's second branch is legitimate and cheap. Three of the four cases above were caught *because*
they had been written down as leads with their evidence attached, which made them attackable on a
later pass. The one that was not — the base derivation — survived two passes and a status promotion
before anyone noticed the agreement was guaranteed.

**A corollary for structures specifically.** A struct's *shape* — its stride, its bounds, its
parallel arrays — constrains what it could be. **Only its writes say what it is.** Read the code that
fills a structure before naming the structure.

## Naming: which column header means what

A reader must be able to tell, at a glance, whether a name in this database was **recovered** or
**authored here**. Three column headers carry that distinction. They are not interchangeable, and a
table that names functions must use one of them.

| header | means | obligation |
|---|---|---|
| **`Name`** | the ledger's name, **verbatim** from `functions.tsv` | must match exactly — `check_names.py` enforces this |
| **`Working name`** | **this database authored it**; the ledger leaves the function `FUN_*` | the name is a description, never evidence; nothing may rest on it |
| **`Identification`** | matched to an **external, checkable** definition — an upstream library API, an RTTI class | pair it with a **`Verified`** column saying how (the Lua document is the model) |

**`Working name` is already the corpus convention** — 16 documents use it — but it was never defined,
which is why this section exists. A minted name under a `Working name` header is correct practice,
not a defect: naming a function you have understood is the point. **Publishing one under a bare
`Name` header is the defect**, because it claims recovery.

**Overriding a real ledger name is a stronger act than minting** and must be stated inline, with the
ledger's name given. The Weather documents do this correctly:

> *"**Naming note.** The GFZ calls `0026D910` `WorldField_InitializeCurrentFieldRuntimeParameters`."*

That is the required form. **The GFZ can be wrong and this database may disagree with it — but it may
never disagree silently.**

## A function's address need not be stored anywhere

The longest-running structural question in this database — why thousands of functions had no caller
and no stored pointer — had a one-line answer that no amount of scanning **data** could reach:

```asm
lea rcx, [rip + disp]        ; the address exists only in a register
```

**Not a call, not a jump, not a stored pointer.** The value is materialised in code and handed to a
callee that may stash it at runtime. **Every scan of data is blind to it by construction**, however
well controlled. It accounts for **90.7 %** of the functions that six other mechanisms could not
explain.

**The rule:** before concluding a function is unreferenced, scan `.text` for a `lea` that computes its
address. In this image, **every** rip-relative reference to a function entry is a `lea` — nothing
reads code as data.

**Withdrawn: 4-byte image-relative (RVA) scanning.** Measured against controls it runs at **1.16x
chance in `.rdata`** and **0.9x in `.text`** — noise in both. Everything it appeared to find is
better recovered **structurally**, and each structural parse carries its own validity check, which is
stronger than a control because it **fails loudly instead of quietly**:

| instead of scanning for | parse | its built-in check |
|---|---|---|
| EH funclet addresses | `.pdata` → `UNWIND_INFO` → language-specific data | `FuncInfo` magic `0x19930520/21/22` |
| exception copy constructors | `ThrowInfo` → `CatchableTypeArray` → `CatchableType` | `pType` must name a `.?A`-prefixed TypeDescriptor |
| jump-table targets | `jmp reg` ← `add reg,base` ← `mov reg32,[base+idx*4+T]` | entry count from the preceding `cmp`/`ja` bound |

**Recovering funclet entry points from unwind data is not the banned inference.** The ban is on
treating *the presence of a `.pdata` entry* as evidence a function is reached — it says only that a
function has a prologue worth unwinding. Reading the handler data to learn **which funclets exist** is
a structural parse and is sound.

## Data loss at a boundary reports success

**2026-09-02.** `rtti_recover.py` carried four defects, found together. Every one **destroyed
information at a boundary**, and not one raised an error:

| boundary | defect | what it produced |
|---|---|---|
| harvest | regex stopped at the first `@@` | every template name truncated before decode |
| decode | demangler dropped the argument list | 16 distinct types wearing one name |
| width | 250-character bound | two real 264/265-char descriptors silently dropped |
| write | `mangled` column hardcoded `''` | the evidence of the collapse discarded |

**None corrupted a value. Each discarded one** - and each produced a smaller, tidier, entirely
plausible number: 2,133 classes instead of 2,248, 2,284 vtables instead of 2,286. A wrong value looks
wrong; **a missing one looks like a clean result.**

**The check:** at every boundary where data is selected - a regex, a length bound, a decode, a column
written - ask *what does this silently drop, and would I notice?* Prefer a terminator to a delimiter
that can occur inside the data (`\x00` over `@@`), prefer a bound proven against the data over a
round number, and **never write a placeholder where a real value exists** - the discarded field is
usually the one that would have exposed the fault.

Corollary: **two tools agreeing is worth more than either being careful.** This defect survived
because nothing else computed the same numbers; it died the moment a second implementation did.

### The inverse: data CREATED at a boundary

**2026-09-02, same pipeline.** Three vtable slots resolved to targets that were never pointers:

```
00444F4C = "LOD"   00D85180, beside "PLODLevel"
006C6543 = "Cel"   00D5A248, beside "PrecomputeSingleScattering"
00755F6D = "m_u"   00D337A0
```

Phyre stores short field names **inline in the reflection record** (SSO-style, <=7 chars plus NUL).
An inline 3-letter name read as a little-endian qword **is** a small integer, and these three land
inside `.text`'s VA range - so a "points into `.text`" filter admits them as code pointers. There are
exactly three because it needs the right letters.

**The guard is an entry check, not a range check.** "Is a known function entry" rejects all three;
"is inside `.text`" cannot. Anything scanning pointer runs over reflection data needs the stronger
test, because such tables are full of inline short strings by construction.

**Both directions share the tell** - a plausible number, no error raised. The asymmetry is worth
knowing: **a discarded value leaves no trace, an invented one leaves a decodable byte pattern.** The
fabrication was explained in a single check; the truncation took three passes to find.

## Enumerate every route, or the negative is only about your scan

**2026-09-02.** A reachability partition published **3,395 functions / 748 KB** as reached by no
static route. The true figure is **351 / 88 KB** - **wrong by 8.5x**, from two independent gaps in
the instrument:

| gap | cost |
|---|---|
| the LEA route matched **`48 8D` only**, not `4C 8D` (destinations `r8`-`r15`) | misclassified the example the section led with |
| **no `E9` route at all** - `jmp rel32` to an entry is a **tail call** | **2,895** functions reached no other way |

**Both routes were already known to this project.** `string_xref.py` documents both LEA encodings in
its own docstring, and tail calls appear throughout the database's own call-chain sections. **The scan
was written from scratch rather than assembled from what the toolkit already encoded.**

**A "nothing reaches this" result is a statement about the routes you enumerated, never about the
binary.** Before publishing one, list the routes deliberately - direct call, tail call, both LEA
encodings, absolute pointers, vtables, jump tables - and say which were checked. **A negative's
strength is exactly the completeness of that list**, and an unlisted route is indistinguishable from
an absent one.

**The disagreement is what caught it.** A peer instrument built independently gave a figure 8x lower;
reconciling them took one pass and prevented a research programme resting on a wrong denominator.
**Two instruments that share a source agree for free - two that do not are worth the cost of
comparing.**

## Advice carries the evidence burden of a finding

**2026-09-02.** A document's modding section named **six opcodes as free** and recommended them as
"the natural slots for a new instruction", listing `0x01` and `0x02` first. A second table found later
gives every opcode an **instruction length**, and **`0x01` and `0x02` are length 0**: a handler
installed there never advances the program counter and spins until the frame budget expires. **The two
worst slots in the table were recommended first.**

The finding they rested on was sound - those six opcodes really do reach the default handler. **The
advice was a different claim**: that reaching the default handler is *the whole* qualification for
being usable. Nothing had tested that, because a recommendation reads like a summary of the finding
rather than a new assertion.

**A "you could" or "the natural way to" sentence is a claim about what would happen if someone did
it.** Before publishing one, state what the action depends on and check each dependency, or mark it
explicitly as untested. **Prose that tells a reader to act is held to the standard of a finding, not
of a summary** - it is the one kind of sentence in this database that can cost a reader work.

## A function's identity is not uniform across its branches

**2026-09-02.** A document identified the single writer of a combat scalar as *"the host-timing
initialiser - it calls timeGetDevCaps and timeBeginPeriod"*. The function does call those. **It calls
them on the branch that does not contain the write.** Its argument selects between two unrelated
jobs, and the store sits on the other one, next to `timeEndPeriod`.

The error survived because the summary was true of the function and false of the instruction. Naming a
function from its most recognisable API call, then attributing a specific store to that name, silently
assumes the function does one thing.

**A write belongs to the branch that contains it.** When a claim attaches a specific access to a
function's purpose, check that the access and the purpose are on the same path - and where a function
is two jobs behind one entry point, say which branch, not which function.

**The same pass showed the cost in the other direction.** The prose said "shutdown-path default
restore"; the ledger row for the same fact said "the shutdown branch"; and the value written was
neither a default nor a restore. **Two summaries of one function disagreed with each other for
several passes and neither was checked against the bytes**, because each read plausibly on its own.

## An attack instrument is an instrument

**2026-09-02.** A falsification pass on the 4,275-address vtable index reported **2,134 addresses
missing** - a defect that would have invalidated half the document. **It was the attack script.** The
appendix packs two `(address, class, slot)` triples per row, and a single regex over the line
**consumes the `|` separator the second triple needs**, finding only the first of each pair.

**The tell was arithmetic:** 2,141 is 4,275 / 2. Without noticing that, the "finding" would have been
published as a defect in a document that is in fact exact.

**A falsification pass that reports a defect is exactly as capable of being wrong as the document it
attacks - and is LESS likely to be re-examined**, because a found defect feels like the pass
succeeding. **Verify the attack before believing its result**, with the same standard applied to any
other instrument: what would it report if the document were perfect, and is that what a perfect
document would produce?

The corrected run found **0 missing, 0 extra, 0 slot mismatches, 0 name mismatches.**

## A discriminator must be able to return "I don't know"

**2026-09-02.** Re-verifying 16 candidate exclusions, the instrument was built with **three** verdicts -
two decisive disqualifications and an explicit **UNKNOWN** meaning *the exclusion rests on nothing*.
First run: **3 decisive, 12 UNKNOWN.**

**That bucket then fixed the instrument twice.** Reading an UNKNOWN case exposed a deleting destructor
whose deallocation went through a wrapper rather than a direct `free` (converted 11); reading the last
one exposed another that **delegated its vtable restore to its base class**. Final state: 16 of 16
resolved, **zero unknown** - and the published claim came out *stronger* than before the audit.

**A two-valued discriminator could not have done this.** It would have reported 3 exclusions and 13
silent under-detections as 16 exclusions, and nothing would have prompted a second look.

**Nearly every bad number this database has recorded came from an instrument with no way to abstain:**

| instrument | what it could not say | what it said instead |
|---|---|---|
| live functions strictly inside a residual span | "this span cannot distinguish" | `N = 0` |
| `u8 < 251` as a dense-index test | "a byte satisfies this anyway" | 8 confident hits |
| "reads `edx`" by operand name | "this operand is written, not read" | an inverted verdict |
| slot-0 exclusion, two-valued | "this one rests on nothing" | 16 exclusions |

**The rule: every discriminator gets an explicit not-determined verdict, and its count is reported.**
A run with a large UNKNOWN bucket is an honest partial result; a run with none is either finished or
lying, and only the bucket tells you which.

## Adjacency is banned as evidence between instructions too

**2026-09-02.** A verification script paired each `lea <vtable>` with the **immediately following**
`mov [rcx+N], rax` and reported the second vtable store as absent. It was not absent - the compiler
had scheduled an unrelated `mov dword [rcx+0xA0], esi` between the pair:

```
006C876E  lea  rax,[rip+0x6be35b]        ; the vtable
006C8775  mov  dword ptr [rcx+0xa0], esi ; unrelated, interleaved
006C877B  mov  qword ptr [rcx+8], rax    ; the store the check missed
```

**The database bans address adjacency as evidence; this is the same fallacy one level down.**
Instruction *order* is not instruction *dependency* - an optimising compiler interleaves independent
work freely, and "the next instruction" is not "the consumer".

**The correct test is register liveness:** does anything write `rax` between the producer and the
candidate consumer? If not, they are paired regardless of what sits between them. **Any scan that
matches an instruction to "the next one" is asserting adjacency**, and will silently fail on scheduled
code - which is all optimised code.

## An opcode profile says nothing about where the data goes

**2026-09-02.** The largest unclassified function in the image, `003CD840`, was profiled and called
**"the shape of a codec or unpacker"** on its opcode mix: `psrldq` 686, `pextrw` 294, `movdqa` 588,
no calls, no strings. Published as a shape. **Overturned one pass later by reading it:**

```
loads  :   299 sites over  6 distinct global addresses
stores : 1,235 sites over 21 distinct global addresses
```

**A codec streams** - advancing registers over buffers, computed addresses. **This hammers 21 literal
addresses.** It is a fully-unrolled state machine over a fixed register file, which is close to the
opposite of a codec, and **the instruction census could not have distinguished them**: both use the
same opcodes.

**The rule: an opcode profile constrains what code does to VALUES; it says nothing about what it does
to MEMORY.** Shuffles, extracts and packs look identical whether the destination is a streaming buffer
or a fixed global. **Before naming a function's purpose from its instruction mix, classify its
operands** - how many distinct addresses, literal or computed, and how often each is touched. That is
a cheap second pass and it is where the answer actually lives.

Related to *a real mechanism is not an explanation until it is the right size*: both are cases where a
true observation about a function fails to constrain the conclusion drawn from it.

## A census that prints identifiers must not truncate them

**2026-09-02, twice in one session, by the author of the rule against it.** Two documents were
published naming a function by a clipped string:

```
WorldActorScriptVM_Interpret        ->  WorldActorScriptVM_InterpretBytecode
RenderCommand_InitializeDouble      ->  RenderCommand_InitializeDoubleBuffers
```

**Both had the same cause and neither was carelessness at the writing desk.** An analysis script
printed a name through `%-28s` / `%-30s` for column alignment; the clipped string looked like a
complete identifier; it was copied into prose. The standing rule - *never complete or characterise a
name from a truncated view* - **cannot fire when the truncation is invisible.**

`check_names.py` caught both, which is the argument for a check that runs unconditionally every pass
rather than a habit that runs when remembered.

**The durable fix is in the instrument:** when a scan prints an identifier that may end up in a
document, print it in full and let the column be ragged. Alignment is worth less than a name.

## Agreement between measurements that share a source is not corroboration

**2026-09-02, a correction caught one step before publication.** A census of the unresolved residual
returned **160** where the ledger says **158**. Four checks agreed:

```
three-way census over functions.tsv           -> 160
owner column reproduces the ledger exactly    -> 9,409
finalNo column reproduces the ledger exactly  ->   585
tag census, case-insensitive, no alternate spelling -> CodeDomain on 28,007 vs ledger's 28,009
```

Four routes, one conclusion: *the ledger is over by two.* **It was not.** The two extra functions had
been **resolved and certified two hours earlier**, and the category's own README named both, with an
evidence file called `GM160_CURRENT160_ADDRS.txt` - the residual **was** 160; two were closed.
`functions.tsv` simply had not been regenerated.

**All four checks read the same dump.** Reproducing two of its columns against the ledger felt like
independent confirmation and was not - it confirmed the dump was internally faithful, which was never
in doubt. **A second measurement corroborates only if it can fail independently of the first.**

**The check:** before publishing a correction to an authority, ask *what artifact is my evidence drawn
from, could every one of my checks be wrong together, and does the thing I am correcting already
explain the difference?* Here the answer to the last question was in the README of the exact category
under audit.

**Related but distinct** from the base-rate and magnitude rules: those catch a number that cannot
inform; this catches a number that informs, is measured correctly, and is drawn from a stale source.

## A class with a virtual destructor states its own object size

**2026-09-02, from peer session repos-39.** MSVC's scalar deleting destructor passes the object size
to sized `operator delete`, so the size is **written in the code**, once per class:

```asm
call <real destructor>
test bl, 1
je   skip
mov  edx, <OBJECT SIZE>     ; <- stated, not inferred
call free
```

**This needs no constructor call site**, which is the usual route (`mov ecx,<size> ; call <alloc>`)
and which can simply come up empty. In the audio family both routes were tried: the five concrete
controllers confirmed twice, and **the six banks only once**, because their allocation does not put a
literal size in the calling function.

**Keep it beside the allocation route, not instead of it.** Where both exist they cross-check; where
only one does, say which. Reporting twelve sizes as if all twelve had two independent confirmations
would have been the easy and wrong write-up.

It generalises to any MSVC class with a virtual destructor - a one-pass, code-stated size for the
whole game-specific class set.

## A real mechanism is not an explanation until it is the right size

**2026-09-02.** A 195-row gap between two RTTI tools was explained as `/OPT:ICF` COMDAT folding. The
folding is real, the surplus rows genuinely are folded code, and the explanation was still wrong:

```
rows the proposed mechanism acts on : 18,720
the gap being explained             :    195
tools agreeing on folded pairs      : 2,672 / 2,704  (98.8 %)
```

**A mechanism operating on 18,720 rows does not explain a discrepancy of 195.** Its presence was
mistaken for a fit. The real cause was a demangler that drops template arguments and collapses
distinct instantiations into one class string - folding only supplied the shape it acted on.

**The check:** having named a mechanism, ask *how many cases does it touch, and how many does the
thing I am explaining have?* If the mechanism is far larger than its effect, something else is
selecting the cases - **find that instead, because it is the actual cause.** Ninety-nine per cent
agreement under a mechanism means the mechanism is shared, not causal.

This is the sibling of the base-rate check: there, a number needs its denominator; here, a mechanism
needs its magnitude. **Both fail by being locally true.**

## A metric that returns its value by construction is not a measurement

Distinct from a *biased* instrument: this is one whose output **could not have come out otherwise**,
so it carries no information at all while still producing a confident number. **Three instances,
two of them found on the same day by different analyses.**

| the metric | the number | why it was empty |
|---|---|---|
| live functions counted **strictly inside** `[first residual, last residual]` | `N = 0`, read as "an isolated dead region" | **zero by construction** for any contiguous run — it was selecting for contiguity and being read as isolation |
| `u8` fields whose values are `< 251`, as evidence of an index into a 251-entry table | 8 fields at 98–100 % | **a byte satisfies `< 251` for 98 % of its range**; the test cannot separate the hypothesis from the null |
| 4-byte image-relative scan for function references | 54,655 hits | **1.16x** a control of provable non-functions |

**The check:** before believing a count, ask *what value could this have produced if the hypothesis
were false?* If the answer is "the same one", the number is not evidence — no matter how precise it
looks, and no matter that the instrument is correctly implemented. **All three of the above were
correctly implemented.**

The two 2026-09-02 cases are instructive together: one produced a **zero** that read as a finding, the
other produced **eight hits** that read as a finding. **Both directions fail the same way.**

### The wrong-denominator form: 100 % is not a result until you know the base rate

The commonest way this failure reaches a finished document is **not** a broken test — it is a correct
count compared against a population the subject was never drawn from. **Found in two documents on
2026-09-02, with opposite verdicts inside the same file.**

| claim | compared against | actually drawn from | verdict |
|---|---|---|---|
| ppfx: `135/135` still `FUN_*` | whole binary, 84.2 % | **vtable methods, 96.0 %** (PPFX itself 93.0 %) | **unremarkable** |
| ppfx: `147/147` no PrimaryOwner | whole binary, 73.8 % | **middleware, ~100 %** (`sce`, `std`, `bt*` all 100 %) | **restates "PPFX is middleware"** |
| sead: `90 (100 %)` still `FUN_*` | — | **`Audio`-owned functions, 100.0 % of 2,064** | **guaranteed before the scan ran** |
| **sead: `208/208` land in `Audio`** | `Audio` = **5.41 %** of the binary; null ≈ **11** | — | **survives — 19x its null** |

**The check is one question: what population was the subject drawn from, and what does that population
do anyway?** A 100 % against a 96 % base rate is decoration; a 100 % against a 5 % base rate is the
result the document rests on. **Nothing on the face of the number distinguishes them.**

Corollary for writing: **quote the base rate next to any saturated figure**, or omit the figure. A
percentage with no denominator stated is not a claim a later reader can audit.

### Three failed instruments in one sub-question — stop modelling and ask directly

Testing whether GFZ naming clusters per class produced **three broken metrics in a row** before the
question was answered without any of them:

1. **Grouped by the wrong column** — `methods.tsv` col 0 is *address*, not class, so every "class" was
   one function repeated and homogeneity was **100 % by construction**. Produced a confident `76/76`
   **while auditing for exactly this failure.**
2. **Simulated null collapsed a dict** — an address appearing in several vtables made `dict(zip(...))`
   overwrite entries; the tell was an implausible spread (29–763) across 200 runs of a statistic that
   should concentrate.
3. **Analytic null contaminated by shared methods** — `/OPT:ICF` folding and shared base-class slots
   put the same functions in hundreds of vtables, so one widely-shared named function breaks
   homogeneity for hundreds of classes at once. Gave a nonsensical 0.02x deficit.

**The answer needed no clustering model at all** — one table of per-namespace base rates settled it.
**When the third instrument breaks, the question is usually being asked the hard way.**


## Instrument-shaped blind spots

A negative result is only as good as the instrument that produced it, and this database has now
produced **seven** wrong answers from instruments that could not see the thing being claimed absent.
Before publishing any claim of absence, name the instrument and ask what it structurally cannot see.

**The seventh is different from the other six and worth reading first:** the instrument was correct
and complete, and the error was in the **unit**. A measurement of edges was read as a measurement of
functions. An instrument you trust can still answer a question you did not ask.

| Instrument | Cannot see | What it got wrong |
|---|---|---|
| call-edge census | **inlined** consumers | `rng-streams.md` §8b — seven Loot/EnemyChain functions inlining the LCG were reported as non-consumers |
| scan for `MOV`/`LEA` **loads** | **write-only** globals | `authored-data-table-registry.md` §8c — two write-only slots reported as having no reference |
| an **edge count** read as a call-site count | a caller that calls the same callee more than once | `item-id-encoding-and-equipment-compatibility.md` §9 - `002F9F20` shows **1 edge** but contains **2 call sites**; `cross-subsystem-accessor-hubs.md` §9 drew a vacuous conclusion from the same confusion |
| a string scan filtered on a **literal** the code parameterises | paths built with `printf` placeholders (`/GameData/%s/...`) | `reflected-render-parameters-and-shader-assets.md` §9 - 3 of 18 asset paths missed; the missing ones were the direct evidence for the very convention being argued |
| reading a decompiled `switch` in printed order | cases printed **after** a mid-list `default:` | `gambit-evaluation-and-enmity.md` §8i - modes 8, 9, 10 missed; the switch was called "eight-case" when it has eleven |
| `strings`-style text search with no positive control | anything, when the tool is absent or the pattern is wrong | a "no scripting VM in this binary" claim, retracted; Lua 5.2.1 is present |
| a **caller census**, in the direction it was run | that the same census run the *other way* answers a different question | `phyre-subsystem-map.md` §11 - 2,904 unowned->Phyre **edges** became a claim about ~11,836 **functions**; measured in reverse, only **317 of 15,498** (2 %) are predominantly Phyre-called, and the conclusion was withdrawn in pass 52 |
| a **direct-call edge list** of any kind | functions reached **only through a pointer stored in data** | `why-the-unowned-code-has-no-owner.md` §3 - **7,185 of 10,924** apparently-uncalled unowned functions (65.8 %) are address-taken in `.rdata`'s 27,392 pointer slots. No `call` ever names them |
| a breakpoint / hook / patch **taken beside a hot one**, even with a positive control | that the instrument's own load **stopped the measured path running** | `RUNTIME-RESEARCH.md` §8d - `003EAA70` read **0 hits in-world** beside a control firing 127,578 times; armed alone it reads **1,130,002 in 75 s**. See the amendment above |
| a differential test that reports **“vs reconstruction: OK”** | that the value it compared came from a **copy of the reconstruction living inside the test** | `angle_wrap_driver.c` printed its own capped `wrap_loop_capped()` instead of `Angle_WrapLoop`, which had **never been executed by anything**. Found by `recon_coverage.py`, not by the test |

**Rules that follow, and they are not optional:**

1. **For a shared global, ask who *writes* it, not who reads or calls it.** Use
   `DumpDataXrefs.java`, which classifies read / write / data separately.
2. **Control every count, in both directions.**
   **Every zero** — before believing "no references / no strings / no matches", run the same
   instrument against something known to be present. A zero from an instrument never shown to return
   non-zero is not evidence.
   **A constant is not a fact about a system; it is a fact about sixteen bits.** Audited 2026-09-02,
   `0x4000` carries **eight** unrelated meanings in this image: the extended order-id base, the cancel
   button mask, the `GUARD_CF` flag, a `qwUnitFlags` bit, a gambit resume bit, a persistent-flag gate
   bit, the pooled-record free bit, and a texture-arena seed. Searching for a constant finds all
   eight.
   **And every non-zero.** Before believing a count, run the instrument against a set known to be
   **absent**. Measured 2026-09-02: a 4-byte RVA scan of `.rdata` matched **54,655** positions on
   real function addresses and **46,966** on a control set of equally many non-function addresses,
   same range, same alignment — **1.16x chance, i.e. nothing**. The same control gave the 8-byte
   pointer scan **106x**. **Two instruments in one pass differed by a factor of ninety in
   trustworthiness, and nothing in their output said so.** A scan matching tens of thousands of
   values against millions of words will hit by chance; the hit count cannot tell you whether it did.
    Before believing "no references / no strings / no matches", run
   the same instrument against something known to be present. A zero from an instrument never shown
   to return non-zero is not evidence.
3. **Never characterise a construct from a truncated excerpt** - in either direction. A capped
   census (`most_common(40)`, `head`, a page limit) or a body printed to N lines can produce a false
   **positive** claim as easily as a false disagreement. This rule was first written as
   "never report a *disagreement* from truncated output" and was **too narrow**: within the hour, a
   case set read off a 35-line excerpt of `002ABF70` was published as complete and was wrong
   (`0,1,2,4` for an actual `0,1,2,3,4,5,7`). If the claim is about a whole construct - a switch, a
   table, a loop's bounds - the whole construct must be in view.
   **This covers identifiers.** A name cut off by a column width invites completion, and completion
   feels like reading: `BattleMenu_UpdateCommandSelectionAndDisp` was written up as `...AndDisplay`
   and propagated to five places in three files before a full-width listing showed the real ending,
   `BattleMenu_UpdateCommandSelectionAndDispatch`. **Resolve a truncated name against the source table before quoting it**, never
   against what it looks like it should say.
4. **Count switch labels, never reading-order.** A decompiler emits `default:` wherever it falls in source order, which can be the middle of the list. Cases after it are easy to miss.
5. **When scanning for authored paths or names, do not filter on a literal the code may build at
   runtime.** Search the stable part of the pattern and inspect what comes back; a `%s`, `%d` or
   concatenated segment is invisible to a filter written against one expanded example.
6. **A direct-caller census misses IMPORTED callees entirely.** An imported function is reached by
   `FF 15` through a pointer slot, not `E8` to an address, so it produces **no function-to-function
   edge**. Measured: **417 of 538 import slots are called, across 3,543 indirect call sites**, none
   of them in `edges.tsv`. This is how `rand` appeared to have one caller when thirty functions call
   it — and why it was recorded as a sound-driver detail when it is a gameplay RNG used by Movement,
   Combat Action and Lua's `math.random`. **For any imported symbol, use
   `analysis-kit/gfz-scripts/iat_xrefs.py`, never the call graph.**
7. **A decompiler's symbol is a claim about the bytes, not the bytes.** Ghidra printed `rand()` in
   two functions that contain no call to `rand`; both reach it through an import slot. Where a name
   carries the weight of a finding, resolve it — to a call target, an import entry, or a string.
8. **A direct-caller census misses thunked callers.** 835 functions in this image are a bare
   `JMP rel32`, forwarding to 750 distinct targets, and a caller census of the *target* does not
   see them. This produced a wrong "dead code" finding within one hour of the same defect being
   corrected elsewhere: four accessors declared uncalled were each reached through a thunk, from
   the script VM. **Before claiming a function is uncalled, resolve the thunks that point at it.**
   `analysis-kit/gfz-scripts/` has the sweep.
9. **A census of edges is not a census of functions.** One helper called 864 times contributes
   **864 edges and one function**. Any claim of the form "most of X is Y" must count the thing named
   in the claim. Pass 51 concluded that the generic shape classes *were* the game/middleware seam
   from 2,904 edges; counting functions gave 2 %, and the conclusion was retracted. **Before
   publishing a proportion, say out loud what the denominator is.**
10. **Before calling a function uncalled, scan the data sections for its address.** Two thirds of
   the apparently-uncalled unowned code in this image is reached through a table pointer. Vtable and
   dispatch-table entries produce no call edge and never will. `.rdata` holds **27,392** such slots
   addressing **10,472** distinct functions, of which **6,883** sit in an RTTI-named vtable. This is the same defect as rules 6 and 8 - an indirect
   reach the edge list cannot represent - at a much larger scale, and it is now the **third** time
   it has produced a wrong answer.
11. **Reading a `defaultdict` mutates it.** A caller index built as `defaultdict(set)` and *read*
   during an earlier loop inserted empty entries, silently shrinking a later "no caller" population
   from 10,984 to 10,674 - a 2.8 % error invisible in the output. Build membership sets with a plain
   `set`, or test with `.get`. A measurement tool that changes what it measures is the same class of
   defect as an instrument-shaped blind spot, and it is harder to see.
12. **An edge count is a count of distinct callers, never of call sites.** `edges.tsv` stores one
   row per caller-callee pair (verified: 90,525 rows, 90,525 distinct pairs, no duplicates). A
   function called three times from one place contributes one edge. Never phrase an edge count as
   "called N times", and never infer from `edges == distinct callers` - that identity holds by
   construction and proves nothing.
13. **Before claiming anything is new, read the database and its artifacts.** Three times now a pass
   has announced a finding the database already held: the recipe interpreter (AK-1/AK-2), thirteen
   third-party libraries already inventoried with versions, and an entire RTTI vtable recovery whose
   `classes.tsv` / `methods.tsv` were sitting in `Tools/work/rtti/`. **The cost of checking is one
   directory listing and one grep.** The cost of not checking is a false novelty claim inside an
   otherwise sound document - which is worse than no document, because it is believable.
   **Fourth occurrence 2026-09-02**, and the pattern is now clear enough to name: *reading* this rule
   is not *running* it. The practical form is a pre-flight, not a principle — **before investigating
   an address, a structure or a term, grep the corpus for it.** That pass re-derived the entire PE
   Load Config CFG parse, hex value for hex value, from a document that already contained it.
   Corollary: **duplicated work is not wasted if the two results are compared.** The second RTTI
   recovery agreed with the first on 2,286 vtables exactly, entering the graph from the opposite
   end, and that agreement is stronger evidence than either run alone. Compare, then say plainly
   that it was a duplicate.
14. **Operand position is not access role.** An ad-hoc scan that calls "memory as operand 0" a write
   mislabels `test [mem], imm`, `cmp [mem], reg` and `or reg, [mem]` — all reads. It turned a pair of
   settings globals with **two** writers each into globals that ninety functions appeared to modify.
   Restrict writes to the mnemonics that actually store (`mov [mem], reg` and friends).
   `analysis-kit/gfz-scripts/struct_map.py` already encodes this in its `WRITERS` set — **the error
   came from re-deriving the test inline instead of reusing the tool's.** Reuse the tool.
15. **A negative about one function is not a negative about its callees.** Established the hard way:
   `002AC5F0`'s output-only parameter was used to rule out text handling for a whole cluster, and
   the character loop turned out to be in the function it calls.

### AMENDMENT 2026-09-13 (OPUS) — a NOVELTY claim is a claim about the database, and needs the same search

Every amendment above governs a claim about the **binary**. This one governs the claim a pass makes
about **itself**: *this is new*. It is stated constantly — in headings, in "New:" sections, in an
open question — and until 2026-09-13 nothing required it to be checked.

**Two instances in one session, both by the same agent, both of its own earlier work:**

| the claim | what already held it |
|---|---|
| *"the class **is** the id's top nibble — and the page never says so"* (class-registry pass) | `the-encoded-id-space-and-the-query-record.md` §2.1 states `class = nibble + 5` outright — **and that page had been audited by the same agent five commits earlier** |
| *"The value stack is **four parallel arrays**, and both of its ends fail silently"* (calling-convention pass) | `CONTRACT-script-to-native-bridge.md` gives the `0x284` size, the four arrays, `+0x184`, the 63-slot guard and the `+0x84` zeroing; the mirror-image failure modes are the **headline** of `OPUS-PASS-SCRIPT-BRIDGE`, the same agent, 2026-09-12 |

Both cost more than the wasted effort. The first carried **two wrong field offsets** into a page
(`+0x38` read as "the record's first dword", `+0x48` as "the fifth dword"), because a claim written
without looking is also written without the other page's correct layout in view. **Duplicating a
finding and getting it wrong are the same failure**, arriving together.

**The rule.** Before a pass writes that something is new, unstated, uncovered or unread, it runs
`check_already_answered.py` on the addresses and terms the claim names — the tool exists for exactly
this and says so in its own docstring. One call. If the search returns a document, the finding is a
**re-derivation** and is published as one; independent re-derivation is worth something, and saying
which it is costs a sentence.

**Why this is not a gate.** `check_novelty_claims.py` (added the same day) sweeps *absence
phrasings* — "never says", "no document", "not stated" — and catches the first instance's shape.
It cannot catch the second: that section made **no absence claim at all**, it simply put known facts
under a heading reading **"New"**, and matching the word *new* across this corpus is not viable.
**A gate can only see the claims that announce themselves**, so the search belongs in the pass
procedure and this amendment is where it is recorded.

> **The tell, in both cases:** the agent had read the other document *within the same week* and in
> one case had audited it personally. Familiarity is what removes the impulse to search — which is
> why it has to be a step rather than a judgement call.

### AMENDMENT 2026-09-13b (OPUS) — the gate prints its register rows LAST, so do not truncate it

The 2026-09-13 amendment requires `check_already_answered.py` before a pass writes that something is
new. **It fired, and it was defeated by a pipe.**

Running the falsification pass on
[which roll is on which generator](../21-RNG-And-Determinism/which-roll-is-on-which-generator.md), I
ran the gate with two addresses and a term at once. It printed a **37-document** list and I read the
output through `head -14`. `check_already_answered.py` prints its matching documents first and its
**`OPEN-QUESTIONS.md` rows last** — so the truncation removed exactly the part that mattered: four
register rows, `AD-2`, `AD-6`, `AE-3` and `CQ-1`, all reading **ANSWERED**, covering the address I
had asked about.

I then decoded `FUN_00319530` from the image and drafted it as a finding, including a "correction"
to the page's correlation bullet that the register's own answer (`AE-3`: the trigger is a **pickup
collection**, not a combat event) shows to be wrong. **The draft was retracted before publication
only because the gate was re-run un-truncated on the second attempt.**

> **Rule.** Run the gate, and read **all** of it — the register section is the half that answers the
> question, and it is the half a `head` removes. If the output is long, narrow the query (one address
> at a time) rather than cutting the output; the tool ends with the line
> *"At least one register row already answers this. Read it before assigning."*, and if you cannot
> see that line you have not run the gate.

This is the same shape as the three failures already tabulated here: an instrument that works,
defeated by how its result was read. It is recorded rather than fixed in code because the tool is
correct — the defect was in the reading.


### AMENDMENT 2026-09-13c (OPUS) — run the gate again on the addresses your *finding* introduces

Amendment 2026-09-13b fixed how the gate's output is read. This one is about **when** it is run.

On the falsification pass for
[the katano development saves](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/katano-debug-savedata.md)
I ran `check_already_answered.py` first, correctly and untruncated, on the page's own subject: the
term `savedata` and the three addresses the page names (`002EF300`, `0050D9A0`, `01E19670`). Nothing
answered it, and that was true.

The pass then went somewhere the page did not: the four header constants, and from there to
`00253A80`, `002370C0`, `00233C10` and `02EBF190`. I drafted *"New: the four header constants are the
image's geometry"* — and **two of the four were already answered.** `V-2` has carried since
2026-09-10 that `0x05071901` is the battle-state block's magic, compared at `00233C4D`, and that
`0x20050223` occurs once in the whole executable; there is a page,
[version stamps and what loading normalises](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/version-stamps-and-what-loading-normalises.md),
about exactly that. Re-running the gate on the *new* addresses printed `V-2` immediately.

> **Rule.** The gate answers the question *"is this new?"* for the addresses you give it. A pass that
> travels — and a good one does — ends up holding addresses it did not start with. **Run it again
> before writing "new", with the addresses and terms the finding itself introduces**, not the ones
> the page came with.

Two things made the near-miss visible rather than published, and both are worth keeping: the second
run was made *before* the section was committed, and the claim was written as a table with a column
saying which rows were already on record — a shape that makes an unattributed row obvious.

The correction also found its own reward: the *other* two constants, `+0x5C` and `+0x64`, were **not**
placed anywhere, and `+0x64` turned out to be the battle-state block's size — the fact the page had
been asking about since it opened `SV-1`. **The claim shrank and got sharper.**


### AMENDMENT 2026-09-13d (OPUS) — a field census over a pointer needs register liveness, and an impossible offset is the tell

Auditing [the shared drawing context](../99-Unresolved-Residual/Glyph-Run-Rendering/the-shared-drawing-context.md), I rebuilt its offset map independently: find the instruction that loads the global pointer into a register, then attribute every later `[reg + disp]` in that function to the struct.

It returned **67 distinct offsets, including `+0x-080`, `+0x-010` and `+0x-001`**. **A struct published at its own base has no negative offsets**, so the result announced its own defect: the trace never killed the register when the function reused it, and every unrelated `[rax + disp]` after the load was counted.

> **Rule.** A field census that follows a pointer through registers must **kill the register on redefinition** and account for branches, or it is measuring the function's whole register traffic rather than the struct. Until it does, publish nothing from it — and treat **any offset the type cannot have** (negative, past the known size, misaligned against a known width) as proof that the instrument is wrong rather than as a discovery.

The page had already recorded this exact failure mode on 2026-09-03, from a different tool. **Reproducing it from scratch is the reason it is worth a standard**: the naive shape is the one a fresh implementation reaches for, and it fails silently except for the impossible values it prints.

## AMENDMENT 2026-09-13e (OPUS) - three instruments, four controls each, and only the fourth could see

**Rule.** Before a reference census is allowed to support a negative, run it over **targets the
database already documents as positive**. If the controls come back zero, the instrument is blind
and the census says nothing about the targets.

I set out to test whether eight archive formats (`cl2`, `as7`, `btm`, `lst`, `mg`, `mrp`, and the
generic `dat`/`bin`) are read by this executable at all. Three instruments in a row returned a
confident zero, and **all three were blind**:

| instrument | controls (`st2e`, `EBP2`, `PKFL`, `TIM2` / `.ebp`) | targets | verdict |
|---|---|---|---|
| the magic as a **string** in the image | **0** | 0 | blind |
| the magic as a **32-bit immediate** in `.text` | **0** | 0 | blind |
| **`lea` references** to the path strings | **0** for `.ebp` across **10,380** strings | 0 | blind |
| **membership of a pointer table** | `.ebp` **10,380 / 10,380** | `.cl2` 27/27, `.lst` 10/10, `.btm` 24/24 | **works** |

`.ebp` is the script container - fourteen documented units, an entire category. **Zero of its
10,380 path strings is `lea`-referenced**, because the engine does not reach a resource path from
code; it reaches it through a per-language pointer array. Under the instrument that can see that,
the eight "suspect" formats behave **exactly like the controls**.

> **The conclusion I was one step from writing - "the remaster ships PS2-era data it never
> reads" - is not supported, and the evidence points the other way.** It would have been a tidy,
> plausible, wrong claim built on three zeros in a row.

**This is the fourth instrument failure recorded in two days** (2026-09-13c, 13d, the `005C0820`
format string, the `sqrt*` mnemonic scan). The pattern is stable enough to state as a rule rather
than an anecdote: **a zero is a property of the filter until a positive control says otherwise**,
and the control has to be something the database already calls true.

## AMENDMENT 2026-09-13f (OPUS) - a value inside a code range is not a pointer, and a perfect agreement is a question

Two failures in one measurement, opposite in shape.

### The false positive: 139 of 256 "pointers" were numbers

Asking how the unlisted code at the head of `.text` is reached, an 8-byte-aligned scan of every
section found absolute pointers into five of the sixty-six blocks - a tidy answer, and a wrong one.

| the value | times it appears | what it is |
|---|---:|---|
| `0000000000140000` | 63 | a 4 KiB boundary |
| `0000000000150000` | 42 | a 4 KiB boundary |
| `0000000000130000` | 33 | a 4 KiB boundary |

**Of 256 hits in the window, 139 land exactly on a 4 KiB boundary**, and reading the `.rdata`
around them shows record tables and runs of 16-bit values. They are numbers that happen to lie in a
code range.

> **The pointer instrument had no false-positive control until it produced an answer worth
> believing.** The previous amendment made a rule of running positive controls before accepting a
> zero. This is the same rule from the other side: **before accepting a hit, ask what else in the
> image would produce it.** Round values, small integers and lengths all fall inside a code range
> that starts at a round address, and a scan that cannot tell them from pointers has no precision
> to quote.

### The false comfort: 24,360 of 24,360 is not a verification

The image's exception directory was used as an independent census of the function list. **Every one
of its 24,360 primary ranges matched a listed body exactly. Nothing was missing.**

That looked like the list was complete. It was not: `.pdata` describes only what the unwinder must
walk, so a leaf function that never moves `rsp` - which is what hand-written SIMD assembly is -
appears in neither. **The instrument and the list are blind in the same place, so their agreement
carries no information about that place.** The control that showed it: **10,326 of the 34,270
listed bodies have no primary `.pdata` range either**, which is the same boundary seen from the
other side.

> **A cross-check that agrees perfectly has either confirmed the thing or cannot see the
> question.** Before reporting agreement as verification, state what the second instrument would
> have to have found in order to disagree - and if the answer is "nothing it can see", it is not a
> second instrument.

## AMENDMENT 2026-09-13g (OPUS) - the instrument said it was blind, in writing, and I quoted its zero anyway

`CONTRACT-widget-object.md` §5 asserted that `0208EA28` is **never written, NULL for the life of the
process, and a reimplementation must pass NULL there too**. It is written, at startup, three times
over, and the contract's conclusion would have built every menu in the game without a parent.

### Where the zero came from

`UNEXPLAINED-GLOBALS.md` row 15: **0 writers, 122 readers.** And directly above that table, in the
generated document itself:

> *"**Blind spot, stated up front.** RIP-relative only. Globals reached as `[reg + index*8 + disp]`
> do not appear here … **Absence from this index is not absence from the binary.**"*

**The callout was there. I read the row and not the header.**

### What the write actually looks like

```
00247CF2  mov  ebp, 3
00247D20  lea  rdi, [rip+...] -> 0208EA20     ; an ARRAY BASE
00247D9F  mov  qword ptr [rdi], rbx           ; the store the scan cannot see
00247DAC  add  rdi, 8
00247DB0  sub  rbp, 1 / jne
```

Three roots at `0208EA20`, `+8`, `+0x10`. A rip-relative scan sees the `lea` of the base and no store
to any member, because **there is no store to any member** - there is one store through a walking
pointer, executed three times.

### The part that makes this worse than a blind instrument

The withdrawn paragraph **anticipated exactly this objection and answered it wrongly**:

> *"…the two functions that do `lea` the neighbouring block base `0208EA20` (`00247D20`, `0025061C`)
> write only `[base+0]`, never `[base+8]`."*

**`00247D20` is the instruction above.** I had it in my hand, named it in the prose, and did not
follow the loop it begins. Checking the objection made the claim *sound* tested while leaving it
exactly as untested as before.

### The rules

> **A `lea` of an array base is the beginning of a walk.** Treat it as a write to every member of
> that array until the loop is read, not as a write to member zero.
>
> **"Never written" is not establishable by a rip-relative scan for any array member**, and no count
> of loads raises the confidence of that negative by any amount.
>
> **An instrument that declares its own blind spot has done its part.** Quoting a zero from a table
> whose header says the zero is unreliable is not an instrument failure - it is a reading failure,
> and it is the reader's to own. The three previous amendments on blind instruments all concerned
> tools that gave no warning. **This one warned me.**

## AMENDMENT 2026-09-13h (OPUS) — the rebase crosses a call boundary, so no same-body probe can reach it

**The type store's width claims are clean wherever they are checkable, and the checkable fraction is
under half.** Both existing instruments were run rather than replaced:

| instrument | result |
|---|---|
| `check_census_widths.py` | **862 comparisons, 0 disagreements.** Reach: 894 of 1,857 declared rows are in the 16 types that have a census mapping; **963 rows in 231 types are outside it entirely** |
| `check_cited_site_widths.py` | **0 disagreements.** ~~Of the 510 rows citing an address but quoting no instruction, **72** decode to an access at the row's own offset (72 agreed, 0 disagreed) and **438** show no such access at any cited address~~ **CORRECTED 2026-09-13, same day: 474 / 67 / 407.** The three figures were inflated because this checker kept its OWN hardcoded list of censused types, ten names against the census map's seventeen, so 378 declared rows across seven types were counted as uncensused. It now imports the map instead of restating it |

### The 407 are not adjudicable by any instrument that reads only the cited function, and this is measured

The obvious hypothesis is that many of the 407 are the **rebased-base** shape rather than bad
citations: a field reached as `[reg + small]` where `reg` is the record's base plus a constant is
invisible to a probe keyed on the row's own offset. Today's slot-stage work proved that shape exists —
`BattleUnit +0x694`'s only installing writer is `mov byte ptr [rdi + 4], al` at `0030D056`.

**So I built the probe, gave it that case as its positive control, and the control FAILED.** The reason
is worth more than the probe would have been:

> `0030CFB0` takes the rebased pointer **as its first argument** — `0030CFC9 mov rdi, rcx` — and the
> `unit + 0x690` rebase is produced by its **caller** (`00304850`, in `r12`). **The rebase crosses a
> call boundary.** A probe that decodes the cited body and looks for a `lea` inside it cannot see a
> constant applied in a different function, and neither can `check_cited_site_widths`.

**The 407 are therefore an instrument-reach figure, not an evidence verdict.** Nothing here says those
rows are unsupported; it says the two instruments the project owns cannot speak to them, and that a
probe confined to one body never will.

### What follows, and what deliberately does not

1. **Do not quote 407 as "rows without evidence."** Quote it as *rows outside the reach of a same-body
   width probe*, the same way `EC-7`'s frontier is quoted.
2. **The instrument that would settle them follows the base across one call edge** — caller supplies
   `base + k`, callee accesses `[reg + (offset − k)]`. **It is not built here.** It is worth building
   when something actually needs those rows adjudicated, and not before; an instrument built for the
   tidiness of a number is the failure `AMENDMENT 2026-09-13f` names.
3. **The failed control is the deliverable.** Had I widened the probe until it passed, I would have
   reported a fraction of them as "explained by rebasing" on an instrument that had already told me it
   was blind — which is exactly `AMENDMENT 2026-09-13g`, one day later, by the same author.

### Addendum to 13h — one census was unread because nothing pointed at it, and the reach is now ranked

**A census file existed that no map entry named.** `evaluation-context-accesses.tsv` sat in the tree
while `check_census_widths.py` compared 16 types; wiring it moved the reach from **894 to 899 rows in
17 types**, the comparisons from 862 to 867, and the usable width observations from **12,337 to
12,546** — with **0 disagreements still**, so the newly-read census agrees with all five of its rows.
Found by comparing the declared maps against the `*-accesses.tsv` files on disk, which is the same
check the static-catalogue comment above describes discovering the hard way: *"912 rows of evidence
were sitting unread behind a column name."* **It happened again, for a different reason — a file
nothing referenced — and one comparison of map against disk catches both.**

**The remaining 958 rows in 230 types are not a tooling gap.** Each census needs its own seed: a
pointer chain declared per type, which is what `record_field_scan.py` follows. Ranked by declared rows,
so the next census is chosen by reach rather than by whoever asks:

| rows | type | | rows | type |
|---:|---|---|---:|---|
| 35 | `SteeringRecord` | | 18 | `PClusterHeaderBase` |
| 26 | `PersistentFlagPayload` | | 17 | `ImageAddressArenaBlockHeader` |
| 21 | `PhyreClusterHeader` | | 16 | `Widget` |
| 20 | `PPhysicsRigidBodyBase` | | 12 | `ImageAddressArenaRecord` |
| 20 | `PPhysicsCharacterControllerBase` | | 12 | `AchievementState` |
| 20 | `ImageBackedStateBlock` | | 11 | `PSamplerStateBase` |
| 18 | `PMeshInstance` | | 11 | `POctree` |

The top fifteen hold **268 of the 958** uncovered rows (27.8 %), and **56 types hold one row each** —
so census generation has a steep head and a long tail, and the tail should never be the reason the
head waits.

### Addendum to 13h — the three silent subtractions, audited; two are complete, one costs seven rows

The width checker discards census lines in three classes before comparing anything. **Nothing had
re-audited them since they were introduced**, and they are the largest subtraction in the instrument,
so a zero disagreement count depends on them being right.

| exclusion | audited 2026-09-13 |
|---|---|
| **indexed at zero displacement** (10) | correct — `[rax + rcx*4]` at displacement 0 is not a field at offset 0 |
| **no operand width** (490) | **complete, not heuristic.** Broken down it is exactly **440 `lea` + 50 `nop`** and nothing else. A `lea` computes an address without accessing memory and a `nop dword ptr [rax+rax]` touches nothing, so **no width observation is lost here at all** |
| **unrolled SIMD block copy** (357) | **sound in intent, and it costs seven declared rows** — now printed by the checker instead of absorbed |

**Every one of the seven is an array**, and the split matters:

- `BattleUnit +0x0100` and `+0x0110`, both `f32[4]`: their per-element 4-wide evidence survives, so the
  rule **costs nothing** — a float quad read one lane at a time is exactly what the census kept.
- `BattleUnit +0x06C0` (`u8[16]`), `CharacterRenderObject +0x04C4` / `+0x0584` (`f32[4][12]`) and
  `SavePayload +0xE040` / `+0x2E250` (`uint8[512]`): **a block move IS the natural access to these**, so
  the rule removes precisely the evidence that would have confirmed them. Those rows are **UNCHECKED,
  not passing.**

> **The rule is not weakened.** An unrolled `movups` run really is a region copy rather than a field
> read, and loosening it would trade seven quiet rows for a class of false widths. What changes is that
> **the checker now prints what it subtracted**, because a zero that was partly bought by discarding the
> only evidence for a row is not the same as a zero that was earned — and until today the output could
> not tell those apart.

### Addendum to 13h — the `WIDTH DELIBERATE` exemption, audited: not abused, and granted by substring

A field row may declare a width its census disagrees with **provided it says why**. Nothing had ever
checked that the *why* is there, which is the same shape of unaudited escape hatch as the three
exclusions above.

**Audited: it is not abused.** All **ten** rows carrying the marker give a real reason — between **216
and 2,087 characters**, each naming instructions and making an argument (a read-modify-write settles a
2-2 split; a constructor's store width is not a field width; a union declared as a span; a dword whose
readers mostly want its low byte). **No row takes the exemption on an assertion.**

**Two of the ten no longer need it**, and the checker now says so:

| row | why the marker is stale |
|---|---|
| `ActorStorageRecord +0x010` declared 1 | census `{1: 14}` — plain agreement |
| `EvaluationContext +0x008` declared 4 | census `{8: 1, 4: 46, 1: 2}` — **it agrees only because the orphan census wired earlier today is now being read.** The marker was written when the row could not be checked at all |

> **Wiring one unreferenced census retired a hand-written exemption.** That is the concrete argument
> for choosing the next census by reach: an exemption is a promise that something cannot be checked,
> and some of those promises have quietly expired.

**The latent hole is the grant, not the data.** The exemption was taken on a bare substring test —
`"WIDTH DELIBERATE" in evidence` — with no requirement that anything follow it, so a row could earn it
by merely *mentioning* the rule. The form is already inconsistent (`BattleUnit +0x1A4` writes
`WIDTH DELIBERATE,` with a comma), so the test cannot demand punctuation; it now demands **prose** —
at least 40 characters of reason. **Nothing today is excluded by that**, the shortest real reason being
216 characters, and a future empty one will be reported as a defect rather than pass silently.

### Addendum to 13h — the union, which no instrument reported and nobody had

Three instruments check declared field widths and **each reports only its own reach**, so the question
a readiness gate actually asks — *how much of the type store's width evidence is verified at all* — had
no answer. Measured by emitting the `(type, offset)` pairs each one actually compares:

| instrument | rows it compares |
|---|---:|
| `check_census_widths` | 867 |
| `check_evidence_widths` | 633 |
| **overlap between those two** | **545** |
| `check_cited_site_widths` | 67 — **disjoint by construction**, it selects rows with no census *and* no quoted instruction |

> **Union: 1,022 of 1,857 declared rows — 55.0 %. Eight hundred and thirty-five rows are width-checked
> by nothing.** And the two large instruments duplicate **545 rows**, more than eighty per cent of the
> smaller one's output.

**Both halves of that matter and they pull in opposite directions.** The 55 % is the honest ceiling on
*"the width claims are clean"* — every disagreement count in this kit is zero, and that zero covers
just over half the store. The 545-row overlap says the remaining effort should go to **reach**, not to
another instrument over the same rows: a third opinion on `BattleUnit +0x100` is worth less than a
first opinion on any of the 835.

**Nothing here is a defect.** No instrument claimed union coverage; the number simply did not exist
because each file honestly reported its own scope and no one added them up. It is recorded so that
*"0 disagreements"* is never quoted without *"over 55 % of the store"* beside it.

### Addendum to 13h — 55.0 % was two evidence classes added together, and should not be quoted as one

The union figure published above mixes rows whose widths come from **decoded instructions** with rows
whose widths come from **the engine's own reflection metadata**. Split by provenance:

| | declared rows | checked by census or quoted instruction | + cited-site | coverage |
|---|---:|---:|---:|---:|
| **game-side** | 1,244 | 955 | +67 | **1,022 — 82.2 %** |
| **SDK / middleware** (`P<Upper>…`, `CD3D11_…`, `D3D…`) | 613 | **0** | +0 | **0.0 %** |
| total | 1,857 | 955 | +67 | 1,022 — 55.0 % |

**All 613 SDK rows declare their width from reflection registration** — *"reflection registration at
`00613902` (caller `00613800`); size from the C primitive"* is the shape, and it is the shape of every
one of them. **They are not unsupported; they are supported by a different kind of evidence**, and all
three width instruments compare against instruction accesses only. Their `0.0 %` is a fact about the
instruments' language, not about the rows.

> **The contrast is measured, not asserted.** `check_cited_site_widths` ran its probe over **130
> game-side candidates and hit 67 — 52 %** — and over **344 SDK candidates and hit 0**. Same probe,
> same image, same day. An SDK row cites the address where the engine *registers* the field, not an
> address where anything *accesses* it, so decoding that site can never find an access at the row's
> offset.

**What this changes.** *"0 disagreements over 55 % of the store"* understates the instruction-checked
work by a third and overstates what is owed on the SDK rows, because the two populations are not
comparable. Quote them apart: **82.2 % of game-side rows are instruction-checked with zero
disagreements**, and **613 reflection-declared rows have had no independent check of any kind** — which
is a real gap, but a gap in *cross-checking a declaration*, not in evidence.

**No instrument is at fault and none is changed here.** Checking a reflection-declared width against
the accesses that use it is a different instrument from all three of these, and it is not built on the
strength of this measurement alone.

### Addendum to 13h — the coverage index and the width censuses, cross-read for the first time

`types_index.py --validate` reports **247 types, 1,857 fields, 0 errors, 307 gaps**: no field overruns
its type and **no two fields overlap**, so the coverage index's declared-byte percentages rest on clean
arithmetic. The gaps are the interesting half, and nobody had ever asked which of them the project
**already has the evidence to close**.

Intersecting each gap in a censused type with that type's own cleaned census:

| | bytes |
|---|---:|
| gap bytes inside censused types | 46,308 |
| **gap bytes the census already has accesses inside** | **1,683, in 76 gaps across 12 types** |

**Those 76 are rows nobody wrote, not layout nobody recovered.** `CharacterRenderRecord` alone holds
gaps with 12, 8, 8 and 7 distinct accessed displacements inside them — a 48-byte hole at `0x180` with
twelve separate accesses in it is a run of fields, not an unknown.

**They are candidates and the file says so.** An access inside a gap can be an indexed read into an
array declared elsewhere, so each row has to be read before a field is declared; the
`displacement_count` column is the signal strength, not a verdict. The list is
[`_types/recoverable-layout-gaps.tsv`](../_types/recoverable-layout-gaps.tsv).

> **The cheapest layout recovery available is not a new census — it is the census we already have,
> read for what it says about the holes.** The remaining 44,625 gap bytes in those same types have no
> access anywhere in their census and are genuinely unrecovered; the 1,683 are waiting on someone to
> write them down.

### Addendum to 13h — "307 gaps" describes 64 types, not 247, and I nearly published the confound as a finding

Splitting the gap census by population produced a clean-looking result — **225 gaps in censused types,
82 in game-side types without a census, and ZERO in SDK types** — and the zero was an artefact.

> **All 179 SDK-shaped types declare no parsable `size` in `types.tsv`**, so the gap loop skipped every
> one of them. They do not have *no gaps*; **the question was never asked of them.** That is the same
> shape as the `0.0 %` instruction-coverage in the addendum above: an instrument silent on a
> population, and the silence read as a result. **I caught it only by asking whether the zero could be
> an artefact of a missing size — the check this file exists to demand, applied to my own output.**

The honest population:

| | types | declared rows |
|---|---:|---:|
| declare a parsable size — **the only ones `--validate` can gap-check** | **64** | 1,206 |
| no declared size | 183 (179 SDK + **4 game-side**) | **651 — 35.1 % of the store** |

**`types_index --validate`'s "247 type(s), 1,857 field(s), 0 error(s), 307 gap(s)" is four counts over
two different populations.** The types and fields are the whole store; the errors and gaps are the 64
types that declare an extent. Nothing is wrong in the tool — a type with no size *cannot* be
gap-checked, and the tool's own docstring says callers must treat 0 as "no declared size" — but the
line reads as one population and is not.

**The four game-side types with no declared extent are the actionable residue**:
`EquipmentDefinitionRecord`, `FieldRecordTable`, `ImageAddressArenaBlockHeader`, `Widget`. Unlike the
179 SDK types, these plainly should have a size, and until they do their rows sit outside the gap
census entirely.

### Addendum to 13h — the same type spelled two ways, and a control that declined to test it

`check_type_refs.py` reports **0 dangling references**, which is correct, and splits the `ctype`
column into *"resolved to a declared type: 16 names"* and *"references OUT to middleware: 13 names,
76 rows — a boundary, not a gap."* **Seven of those thirteen differ from a type the store DOES declare
by a single leading character.**

| ctype as written | a declared type |
|---|---|
| `UCD3D11_BLEND_DESC` · `UCD3D11_DEPTH_STENCIL_DESC` · `UCD3D11_RASTERIZER_DESC` | `CD3D11_BLEND_DESC` · `CD3D11_DEPTH_STENCIL_DESC` · `CD3D11_RASTERIZER_DESC` |
| `VPComponent` · `VPEntity` · `VPTypedObject` · `VPWorldMatrix` | `PComponent` · `PEntity` · `PTypedObject` · `PWorldMatrix` |

The other six — `PClassDescriptorBase`, `PClassDescriptorForClassDescriptor`,
`D3D11_DEPTH_STENCILOP_DESC`, `PMatrix4`, `PMatrix4x3`, `PString` — resolve to nothing either way.

**The fact is that one type is spelled two ways.** `CD3D11_RASTERIZER_DESC` is a declared type and
`UCD3D11_RASTERIZER_DESC` is a reference; **23 of the 76 "boundary" rows are of this shape.** That is
the address rule — *never describe one thing two ways* — applied to type names, where nothing enforces
it.

**The hypothesis is that `V` and `U` are MSVC decoration residue** (`V` = class, `U` = struct in a
decorated name). **I could not test it and I am not acting on it.** The width test that would have —
a pointer-to-class reference should be 8 bytes — **did not fire: every one of these rows declares
size `0`**, the Phyre reflection shape that carries no width, and the control comparand had no rows at
all. *A control that declines to run supports neither side.*

**Routed as a question to the type store's owner, not rewritten here.** *ANSWERED 2026-09-27 (OPUS, the owner), and only with the mechanism this paragraph said was missing: in an MSVC decorated name a class-type template argument is `V<Name>@` and a struct `U<Name>@`, and each prefixed spelling still in the store occurs in the image ONLY inside decorated names, never as a bare token (`VPString` 15, `VPMatrix4` 7, `VPMatrix4x3` 3, `UD3D11_DEPTH_STENCILOP_DESC` 2), with the unprefixed name declared. That is a per-reference proof, not a name-shape argument, so the 41 rows were corrected with the proof in each evidence cell (9d8c7f32f); the regression that rejects the prefixed spelling is `_index/candidates/typeref-dedecorate/dedecorate.py`.* Stripping a leading character
from seven type references on a name-shape argument is exactly the unsupported bulk disposition this
file forbids, and the fact that seven of thirteen land on declared types is suggestive, not deciding —
the same standard that downgraded the `st2e` count match to a lead.

### Addendum to 13h — a usability score that a missing extent flatters

`type_usability.py` is careful by design: it counts byte arrays as **opaque** rather than typed, and it
presents three byte-weighted views and a per-type view while explicitly refusing to pick one, because
`SavePayload` and `SpawnKeepImage` together are **86 % of every described byte in the store**.

**One number in it was returned by construction.** The extent it divides by is
`d["size"] or (typed + opaque)` — and for a type with **no declared size** that fallback makes
`undeclared` **zero automatically**, because the only bytes it can count are the ones already declared.

> `FieldRecordTable` scored **"size 4, 100 % typed, 0 % undeclared"** on one declared field and no known
> extent. So did `EquipmentDefinitionRecord`; `ImageAddressArenaBlockHeader` scored 100 % on 47
> synthesised bytes and `Widget` 89 % on 73. **All four are the game-side types with no declared size**
> — the same four already routed as `OPUS-REQ-SWE2-STRUCT-UNSIZED-TYPES`.

The tally *"types with no undeclared bytes: 18"* therefore contained **four that were never measured**.
It now reads **"14 measured (+4 with a SYNTHESISED extent, whose 0 % is by construction, not
measured)"**, and names them. The fallback itself stays — a row still has to be printed — but it no
longer flatters a count.

**This is the section of this file it violated**, *"a metric that returns its value by construction is
not a measurement"*, found by asking of a well-made instrument the same question the four before it
were asked: **what does this number do when the input is missing?**

### Addendum to 13h — two rows cited runtime evidence as tier 3, and §15 is not one table

**All 47 contracts carry a §15 Evidence table.** Surveying the `tier` / `confidence` columns across
them: **252 rows at tier 1 PROVEN, 183 "isolated original-code" PROVEN, 106 "static" PROVEN, 30 `—`
UNKNOWN, 24 `none` UNKNOWN**, and a short tail.

**The tier column is free text, not an enum** — `1`, `2`, `3`, `isolated…`, `static…`, `live…`, `—`,
`none` all appear — so a mis-set tier cannot be caught by a value check. Two were caught by reading:

| contract | row | was | is |
|---|---|---|---|
| `CONTRACT-input-name-registry` | *"The real registration order"* — evidence *"walked live in both registries"* | **3** | **10** |
| same | *"any runtime observation"* — evidence *"§13, five observations…"* | **3** | **10** |

**Tier 3 is *qualified symbols*; tier 10 is *runtime evidence*.** Both rows cite live walks of the
game's own lists and were filed as mangled-name evidence. The `PROVEN` confidence was right — the
evidence supports it — and the mis-tier **understates**, which is the safer direction but still a
mis-citation, in the one contract in the store at `RUNTIME VALIDATED and DIFFERENTIAL TESTED`, about
the very evidence that earns it that. Corrected in place with the reason in the cell.

> **And a bound on any instrument that counts §15 rows.** Several contracts put **further tables** under
> the §15 heading — a step table in `CONTRACT-preparation-step-family`, an entry table in
> `CONTRACT-field-music-selection`, an offset table in `CONTRACT-status-write`, a formula table in
> `CONTRACT-efx-source-rebase`. A positional reader takes those for evidence rows: **my own survey
> counted 659 and about twenty of them are not evidence rows at all.** §15 is a section, not a table,
> and a count over it must say which.

### Addendum to 13h — the `tier` column is carrying two axes, and the hierarchy is not extended to fix it

**306 evidence rows across 27 of the 47 contracts put a non-numeric value in `tier`**, and they are not
drift — they are a consistent second vocabulary:

| spelling | rows |
|---|---:|
| `isolated original-code` | 183 |
| `static` | 57 |
| `static + **executed**` | 28 |
| `static, isolated original code` | 22 |
| `live` | 2 |
| qualified one-offs (`static — a census is not an execution`, …) | ~5 |

**The hierarchy ranks evidence STRENGTH; these cells record evidence METHOD.** Tier 1 is *the complete
exact-current function body*; `static` and `isolated original-code` both describe **how** that body was
examined — read, or run. Two axes in one column, which is the same structural fault as the readiness
ladder recorded in `KNOWLEDGE-SCHEMA` §5a, in a different table.

### The ruling: nothing is added to the hierarchy

1. **The eleven tiers are unchanged.** This file says they are not negotiable and that the project lost
   182 classifications once by relaxing them; **no twelfth tier is created here**, and none is needed.
2. **These rows are not un-tiered.** Evidence read from or executed on the exact current function body
   **is tier 1**, however it was obtained; `live` is **tier 10**. The cell was recording the method
   instead of the rank, not claiming a rank outside the scale.
3. **The method is worth keeping** — it is exactly what §13's *evidence class* line records — so the
   correct form is **tier and method together**: `1 (isolated original-code)`, `1 (static)`,
   `10 (live)`. Method alone is not a tier.
4. **This is a wording rule, not a licence to upgrade 306 rows.** A cell reading `static` may rest on a
   census or a displacement scan rather than a full body read — one of the spellings is literally
   *"static — a census is **not** an execution"*. **Each owner checks their own rows**; rewriting 306
   cells to tier 1 on a naming argument would be the bulk disposition this file forbids.

Routed as `OPUS-REQ-CONTRACT-OWNERS-TIER-SPELLING`; nothing is rewritten here.

### Addendum to 13h — the `confidence` column did NOT drift, and the one value I could fix was mine

Having found the `tier` column carrying a second vocabulary, the obvious next question is whether
`confidence` did the same. **It did not.** Against the charter's eight — `PROVEN | VERY HIGH | HIGH |
PROBABLE | HYPOTHESIS | UNKNOWN | CONTRADICTED | SUPERSEDED` — the §15 tables read:

| | rows |
|---|---:|
| on the list | **629** (PROVEN 565, UNKNOWN 54, HIGH 3, VERY HIGH 2, SUPERSEDED 1, PROBABLE 1, blank 3) |
| off the list | **5** |

**99.2 % on-list is a healthy vocabulary**, and the contrast with the tier column's 306 off-scale cells
is the useful part: one column grew a second axis and the other did not, in the same tables, written by
the same people. **Drift is not inevitable; it happened where the scale did not fit the work.**

> **One of the five was mine, written this morning.** The coast-down contract's *"what `0020E600` and
> `0051B9E0` are"* row — which I upgraded when I propagated the `0051B9E0` reading — read
> **`ESTABLISHED`**, a word not on the list, with `static, isolated original code` in the tier cell.
> Corrected to **`1 (static, isolated original code)` / `PROVEN`**, which is also the first application
> of the tier ruling I published an hour earlier. **The 306 rows I routed to their owners include one
> of my own, and it is the one I fixed first.**

The remaining four belong to their contracts' owners and are not rewritten here: `PARTIAL` ×2
(`CONTRACT-authored-table-row-lookup`), `QUALIFIED` (`CONTRACT-sound-request`), and
`**not re-measured here**` (`CONTRACT-field-music-selection`). Each is a *narrower* word than the
charter offers rather than a stronger one, so none overstates; they are wording, routed with the tier
re-spelling as one job.

### Addendum to 13h — 63 `PROVEN` rows describe an instruction without giving its address

The inbox rules say an instruction anchor *"is what distinguishes a read from a mention for every
instrument this project has"*, and that rule is enforced on prose. **Nothing enforces it inside an
evidence table.** Across the 47 contracts' §15 sections, the **566 `PROVEN` rows** divide:

| the evidence cell | rows |
|---|---:|
| cites an address | 398 |
| address in the claim cell instead | 24 |
| points at a section or another document | 26 |
| **no address, but names a run, census or instrument** | **55** |
| **no address and no run — a described instruction with nothing to follow** | **63** |

**The 55 are correctly cited.** For an executed claim the evidence *is* the run — *"150 random pairs
predicted exactly"*, *"40 samples over four seconds, 0 of 16 bytes moved"* — and an address would name
the wrong thing. The README's anchor rule is about reading, not running.

**The 63 are the gap, and none of them is wrong.** They quote real code — *"there is no `test rax,rax`
between the load and the use"*, *"both pushes write literal `0` to it"*, *"`cmp eax, 0x3F / jge` in both
pushes"*, *"`lea rdx,[rax+rax*4]` then `*8`"*. A reader can find every one of those. **But no instrument
can**, and *"at least one anchor per function"* was never the standard — *"a prologue constant, a stride,
a loop bound and a state write are four different claims and each needs its own."*

> **This is a followability gap, not an evidence gap** — the same distinction drawn for the 407
> width rows above. Quote it as *"11.1 % of `PROVEN` evidence rows describe code without an anchor"*,
> never as *"unsupported"*.

Routed with the tier and confidence wording as **one pass over §15**, so producers touch each table
once rather than three times. Nothing is rewritten here: adding an address to 63 rows means finding
the right address for each, which is reading, not formatting.

### Addendum to 13h — the contradiction ledger had been refusing to update for eight days, silently

`CONTRADICTIONS.tsv` held **59 records, newest dated 2026-09-10**, while the tree held **112 dated
correction markers**. The gap was not neglect: **`contradiction_index.py extract` aborts**, by design,
with *"unmatched history overlaps new markers; review source_header anchors first"* — and it had been
aborting since **2026-09-05**, unnoticed, because nothing reports a tool that refuses.

**The tool was right to refuse.** Its own comment says *"a changed header in the same document/date/kind
could be a renamed record, not new history. Never guess or create a second identity for that case."*
Three rows had had their source **line** edited after the ledger was built:

| row | what changed |
|---|---|
| `CON-026` | identical for 480 chars, then the line **continues** with an appended *"(Corrected 2026-09-12: `Shk1_FindByName` is reachable only …)"* |
| `CON-047` | identical for 381 chars, then **continues** with *"**Decoded 2026-09-11:** the section is `battle_pack.bin`'s …"* |
| `CON-048` | **reworded in place**: *"`+0x698` is one type with two homes"* → *"points at one record *type* whose storage depends on the definition kind"* — corroborated independently by the battle-unit field map's own *"(reworded 2026-09-13 from 'one type, two homes')"* |

Each was reviewed and its `source_header` migrated to the current line. **The ledger now holds 113
records — 97 CORRECTED, 8 WITHDRAWN, 4 RETRACTED, 3 SUPERSEDED, 1 OVERTURNED — with 0 identities lost,
0 hand-written claims altered and 140 summary cells preserved.** Fifty-four corrections that had been
greppable-only are records again.

> **The first migration corrupted the file and was reverted byte-identically.** I wrote it with
> `csv.DictWriter`; `read_ledger` is a raw `line.split("	")` with no CSV quoting, so `QUOTE_MINIMAL`
> wrapped every field containing a double quote and the file's quote count went **24 → 82**. Restored
> from a backup taken before the write, then redone as a plain tab-split line edit **with the quote
> count asserted unchanged before writing.** *A writer whose reader is not the same format is the same
> failure this file spends its length on, committed in the tooling instead of the prose.*

**`CON-033` remains unmatched and does not block:** its source no longer exists, because `DG-1` —
*"Where the table at `0x02B5E0D0` comes from"* — was **answered** on 2026-09-11, superseding the partial
retraction it recorded. The row keeps its identity and history, which is the ledger's whole purpose.

## Addendum 2026-09-13i — `method:` carries the strongest method, not the first or the last

An experiment record's `method:` field holds **one** value, and records routinely use more than one:
`EXP-081` read a static installer account (Method A) and then observed a running process (Method C).
Nothing said which one the field should carry, so this does.

**`method:` names the strongest method the record's conclusions rest on**, ordered
`A < B < C`: offline preparation and retained-evidence assessment, then isolated original-code
execution, then ordinary UI input and read-only process observation of the running game. `live_game:`
is `true` if the running game was touched at all.

**The reason is the filter, not the taxonomy.** The field exists so that a reader can ask *which claims
in this database rest on the original process running* and get a complete answer. A record that
observed a live process and was filed under the static step it began with is **invisible to exactly the
query the field was added for**, and an invisible live dependency is the one kind this database cannot
afford — it is what `live_game:` was introduced to make countable. Under-reporting the method hides a
dependency; over-reporting it only over-counts what needs re-validation, and that error is recoverable
by reading the record.

**Where a record used several methods, its body says so and the frontmatter does not.** The field is an
index, not a summary; the prose is the account.

> **Applied to `EXP-075`..`EXP-081` on 2026-09-13 (OPUS)**, whose `method:`/`live_game:` keys were
> missing. Every value was read from the record's own body — a Unicorn version for the four isolated
> runs, a PID for the three live ones — and each is receipted with its source line in
> [`_experiments/evidence/experiment-metadata-recovery/EXP-075-081-method-receipt.json`](../_experiments/evidence/experiment-metadata-recovery/EXP-075-081-method-receipt.json).
> **The routed request assumed only the author could answer this**; the records answered it themselves,
> which is why it came off ASTRA's queue during the usage window instead of waiting six days. `ASTRA`
> owns those records and may overrule any row on return.

## Addendum 2026-09-13j — `static original-code reading` is not `isolated original-code`

Every one of the 32 contract `## 13. Runtime validation` sections written before today opens
**"Evidence class: isolated original-code"**, and every one of them means the same thing: the shipped
bytes were **executed**, at their real virtual addresses, under emulation, against an independent
reconstruction. It is a strong class and it has earned its standing.

Five contracts had no §13 at all, and when they were given one on 2026-09-13 four of them had nothing
to put in that field. Their claims are decoded from the instructions and reasoned about. **Nothing
ran.** Filing that as *isolated original-code* would have overstated it by precisely the distinction
this file exists to protect, so the class below now exists:

> **`static original-code reading`** — the shipping instructions were decoded and reasoned about. **No
> code was executed**, in any evidence class: not live, not under emulation, not against a
> reconstruction. Supporting material of the same kind — the import table, the string pool, a
> call-graph census, a `.rdata` literal — belongs here too and should be named, because none of it is
> an execution either.

**Why a separate word rather than a qualifier.** *"isolated original-code, but not executed"* would
have worked as prose and failed as data: §13 is read by instruments and by anyone asking which
contracts rest on running code. A qualifier hides inside a string; a class sorts. The cost of the
distinction collapsing is that **reading an instruction and running it become the same evidence**, and
that is the single confusion this database is least able to afford.

**The ladder consequence is that this class sits below `isolated original-code`, not beside it.** A
contract at `static original-code reading` has not been falsified by anything that could disagree with
it — which is why a page can be entirely correct, carefully argued, `PROVEN` in confidence, and still
have never once been contradicted by a machine. **`RUNTIME VALIDATED` is two rungs up from here, not
one.**

> **Where it was applied 2026-09-13 (OPUS):** `CONTRACT-storage-read-completion`,
> `CONTRACT-save-container-transform`, `CONTRACT-efx-source-rebase`,
> `CONTRACT-authored-command-ramp-channels` and `CONTRACT-resource-entry-tree` — the five contracts
> that had no §13. Each section also names **what would move it**, and for three of the five that
> turns out to need no running game at all, so they are `SWE2-ORACLE`-shaped work rather than items
> for `ASTRA`'s queue.

## Addendum 2026-09-13k — a bit census is a FLOOR for two flag fields in five, and empty for one in six

Describing flag fields from their access censuses on 2026-09-13 produced the same caveat over and
over — *"the bit list is a floor, not a census"* — and eventually the obvious question: how often is
that true? Measured across every censused type, over the 217 fields that carry a mask operation
(`and` / `or` / `xor` / `test` on memory):

| what the masks are | fields | what a bit list means |
|---|---:|---|
| literal masks only | 132 | **complete** — every bit the image touches appears as a constant |
| mixed literal and register | 47 | a **floor** — some bits never appear as a literal |
| **register masks only** | **38** | **empty and meaningless** — no bit of the field is ever named |

**So 85 of 217 — two in five — cannot have a complete bit list derived from the image, and 38 of
those cannot have any.** `ActorStorageRecord +0x110` has nine mask operations and not one constant
among them; `SecondaryContext +0x15C`, `+0x168` and `+0x174` have nine each.

> **THE RULE. A claim of the form "bit N of this field is unused" is unsupportable unless every mask
> applied to the field is a literal.** Where a register supplies the mask, the bits the field can
> carry are decided at runtime by whatever computed that register, and a census of the instruction
> stream cannot see them. A field's row should say which of the three cases it is, and the rows
> written on 2026-09-13 do.

**This is not a defect in the census and cannot be fixed by a better scan.** It is a property of the
code: `or dword ptr [rbx + 0x110], r13d` names no bit because the program does not name one there.
The only instruments that could close it are a runtime observation of the values actually written, or
a data-flow trace back to whatever builds the mask — and the second is bounded work that would have
to be done per field, per writer.

### RETRACTED AND REMEASURED THE SAME DAY: both figures above were wrong, in opposite directions

Everything above this line was published within two hours, and building the instrument that the
refinement asked for — an actual per-site trace rather than a grep — falsified both of its numbers.
They are struck here rather than edited in place, because the way they failed is the finding.

**The 132 / 47 / 38 table does not reproduce.** It was produced by an ad-hoc command that was not
kept, and no population I can construct yields those three numbers together. `check_register_masks.py`
now states its population explicitly — every censused type, every offset whether or not a row is
declared for it, a mask being `and`/`or`/`xor`/`test` with the field as the memory DESTINATION — and
over **1,545 mask operations** it gives:

| what the masks are | fields | ~~was published as~~ |
|---|---:|---:|
| literal masks only | 79 | ~~132~~ |
| mixed literal and register | 44 | ~~47~~ |
| register masks only | **70** | ~~38~~ |

The register-only count nearly doubles. Only one of the three published numbers can be reproduced at
all, and only by silently restricting to declared fields — which is not the population the other two
came from. **A table whose three cells come from three populations is worse than no table**, because
it invites exactly the arithmetic it cannot support.

**"29 of the 38 — three in four" is WITHDRAWN.** That was `shl reg, cl` appearing *somewhere in the
masking function*, which says the idiom occurs in the body, not that it computed *this* mask. A body
can shift a bit for one field and mask another with something else entirely. Chasing each mask
register backward from its own site, per site, over the 70:

| what actually builds the mask | fields |
|---|---:|
| `shl r, cl` — a bitmap indexed at runtime | **22** |
| loaded from MEMORY — a table, a field, a global | 23 |
| a literal one instruction away (`mov eax, 0xfffe`) | 1 |
| a call's return value | 1 |
| the chase declined | 23 |

So the traced figure is **22 of 70, under a third** — not three in four. The ceiling, if all 14 of the
declined fields whose bodies do contain the idiom turned out to be bitmaps, is 36 of 70. Nothing
between 22 and 36 has been established either way, and the floor is what has been traced.

> **THE CHASE DECLINES WHERE IT CANNOT SEE, AND THAT IS NOT THE SAME AS THE FIELD BEING UNKNOWABLE.**
> `ActorStorageRecord +0x110` — the field whose hand trace started all of this, whose mask IS
> `1 << arg0` established instruction by instruction — comes back UNRESOLVED, because its definition
> sits above the branch target `00225D7A` and a linear backward walk must not read past a label
> anything jumps to. The instrument is right to refuse and the row is right to claim. **An
> instrument's silence is a fact about the instrument.**

**Two things the remeasurement found that the census could not:**

`CharacterRenderRecord +0x61C` (`liveFlags`) was counted as register-only and therefore as
unenumerable. It is neither: `00424196 mov eax, 0xfffe` then `0042419B and word ptr [rdi + 0xc], ax`
clears **bit 0**, and the field's own row has said so since it was written. **A register operand is
not by itself an unknown value**, and a census that reads the operand without chasing it will keep
reporting literals as unknowns.

**MEMORY is a new class and it is a lead, not a dead end.** 23 of the 70 take their mask from memory —
`BattleStatsRecord.statusWord3` from `[rbx + 0x4c]`, `statusWord2` from `[rbx + 0x48]`. Those are
addresses. A bit vocabulary shared between a status word and whatever supplies its mask is a
structural relationship, and it is reachable by the same static work that resolved `+0x110`.

**What survives from the two sections above:** the three classes are the right classes; a shared mask
is still evidence of its own; the `+0x110` row stands as written; and the rule that a register mask
blocks a literal bit list without necessarily blocking the structure stands, now with a measured
frequency instead of an assumed one. **What does not survive is every number attached to them.**

### REFINED THE SAME DAY: a register mask is usually `1 << index`, and that IS the structure

The rule above says the bits a register-masked field can carry "are decided at runtime by whatever
computed that register, and a census of the instruction stream cannot see them". The first half is
right and the second is too pessimistic, which the very next trace showed.

`ActorStorageRecord +0x110` has nine mask operations and no literal. Four instructions resolve it:

```asm
00225CE8  movsxd r13, ecx        ; the function's FIRST ARGUMENT
00225CEB  mov    edi, 1
00225CFA  shl    edi, cl         ; edi = 1 << arg0     a single bit, chosen by index
00225CFC  mov    esi, edi
00225D06  not    esi             ; esi = ~edi
```

So `or [..], edi` sets bit `arg0` and `and [..], esi` clears it: the field is a **bitmap indexed by
an entity index**, one bit per index, and its structure is entirely knowable. It is not a set of
named flags with hidden members.

**Measured over all 38 register-only masked fields: 29 of them have `shl reg, cl` in the function
that masks them.** Three in four are this idiom. So:

> **A register mask blocks a LITERAL bit list and does not necessarily block the STRUCTURE.** Before
> recording a field as unenumerable, trace the mask: if it is `1 << reg`, the field is a bitmap and
> the row should say what the index is, not that the bits are unknown. The nine remaining fields are
> where the original caveat still stands — and even there it is a statement about what has been
> traced, not about what is knowable.

**The cost of getting this wrong is asymmetric**, which is why the correction is worth its space. A
field recorded as "bits unenumerable" invites nobody to look again; a field recorded as "bitmap
indexed by the caller's slot argument" is implementable.

> **A shared mask is evidence of its own.** At `00225D74`-`00225D80` one computed pair — `edi` to set,
> `esi` to clear — is applied to four different flag words in four consecutive instructions. That
> establishes those four words share a bit vocabulary even though none of the bits can be named, and
> a reimplementation giving any one of them a private numbering would be wrong in a way no per-field
> reading could catch. **Unenumerable is not the same as unconstrained.**

## Addendum 2026-09-13m — an entry-only citation is worth what the function's SIZE says it is

The two coverage dimensions disagree by 7,384 functions: `engine_explained` counts a function once
any document names any address in its body, and `A` counts it only when a DOCUMENTED page names an
address **strictly inside** it. The gap is every function a documented page cites at its entry and
nowhere else, and the scorer carries a caution on each side — the gap "is a mention, not an
explanation", and also "a page can explain a six-instruction function perfectly while citing only
its entry".

**Both cautions are right, which is the signal that the population needs splitting rather than
arguing about.** `check_entry_only_sizes.py` splits it by the one discriminator available without
reading 7,384 documents:

| bytes | entry-only | of gap | A | of A | what that size means |
|---|---:|---:|---:|---:|---|
| 0–16 | **791** | 10.7 % | 27 | 1.9 % | a thunk or stub — **the entry IS the body** |
| 17–64 | 1,573 | 21.3 % | 230 | 16.3 % | a few instructions |
| 65–256 | 3,728 | 50.5 % | 574 | 40.7 % | a small function |
| 257–1024 | 1,136 | 15.4 % | 451 | 32.0 % | a substantial function |
| 1025+ | **156** | 2.1 % | 128 | 9.1 % | a large body — an entry citation is a mention |

> **THE RULE. An entry-only citation is not one kind of evidence, and the headline figure cannot be
> read as a single claim in either direction.** Of the gap: **791 are functions of 16 bytes or less,
> where an entry citation names the whole body** and calling them mentions UNDERSTATES the database;
> **156 are bodies over a kilobyte**, where "a mention" is exact and needs no qualification; and
> **6,437 — 87 % — are 17–1024 bytes and genuinely arguable**, which a size bucket cannot settle and
> must not pretend to.

**Neither dimension is corrected by this and neither should be.** `engine_explained` goes on
counting entry citations, `A` goes on refusing them, and the honest change is that the difference
between them is no longer one undifferentiated number that each side can read its own way.

**The control behaves the way a working instrument should.** Interior citations skew LARGE — 32.0 %
of `A` is in the 257–1024 band against 15.4 % of the gap, and 9.1 % is over a kilobyte against
2.1 % — which is what must happen if interior citation is what explaining a big function requires.
A distribution that came out flat would have meant the buckets were measuring nothing.

**And size is a proxy too.** A 300-byte table of moves can be explained in a sentence; a 40-byte body
can hide a subtlety. The buckets bound the argument. They settle no individual row, and the 6,437 in
the middle are the honest shape of the question rather than a number anyone gets to claim.

---

## Addendum 2026-09-13n — the EC-7 family gate checks a note's SHAPE, never its CLAIM

`check_dispositions.py` accepts a declared family on structure: five fields, a readable members
file, unique members, no cross-family collision, and a non-empty note. That gate is real and it
refuses. But its own refusal text names what the note is for — *"C without a note — the bar is a
falsifiable claim, not a label"* — and **nothing had ever tested the claim.** 94 families carry
12,202 bodies of `C` disposition on notes no instrument had read.

`check_family_spans.py` tests the one rule shape that can be checked mechanically, and the
highest-risk one: a **link span**. A span disposition is the dangerous kind, because a wrong
boundary sweeps real engine code out of the frontier as somebody else's library and nothing looks
at it again.

| | families | bodies | |
|---|---:|---:|---|
| INSIDE | **12** | 3,392 | every member obeys the span the note names |
| OUTSIDE | 1 | 1,216 | flagged — and resolved by reading, see below |
| NO-SPAN | 81 | 8,343 | the note states no range; **the checker declining, not a pass** |

**4,608 of 12,951 declared bodies — 36% — now sit in a family whose span claim is tested rather
than asserted.** The other 64% remain asserted, and that number is published so the untested
majority stays visible instead of being folded into a clean-looking total.

> **THE TOOL'S FIRST RUN REPORTED THREE FAILING FAMILIES AND ALL THREE WERE ITS OWN FAULT.** This
> is the part worth keeping.
>
> - **`libwebm mkvparser`, 95 of 100 members "outside".** Its inclusion rule is the run
>   `007FFBC0 up to 00808888`; the regex had taken `007FFCD0-00800150` out of the note's **NOT
>   covered** clause. A range in an exclusion clause is not the family's extent.
> - **`libvpx VP8 DSP kernels`, 3 "outside"** — all three written out in its own note
>   (*"one at 00133B40 … two at 00158B40 / 00158C09"*).
> - **`libogg framing.c object`, 1 "outside"** — the span's own upper endpoint, reported because
>   the checker assumed an exclusive bound where the note gives no convention.
>
> **Three other agents' families were one publication away from being reported as defective.**
> The fixes were: read the span from the inclusion clause only; treat any address written in the
> note as accounted for; and test the endpoint under the most generous reading. Each removed a
> whole class of false positive, and `INSIDE` rose 1 → 2 → 12 as the parser stopped being wrong.

**The one surviving flag is `SQEX SEAD sound library span`, and it is not a defect either.** Nine of
its 1,216 members sit past the declared span — and the note ends *"plus nine SEAD entries just past
the span that RTTI or their only callers prove SEAD's"*. The count matches exactly. What no parser
can check is a prose exception with a stated count, so this one was settled by hand: the low edge is
sharp (non-audio tags below `007A4380`, `Audio;FFXII.Audio` from it), and the nine carry the same
audio ownership tags as the span's own members.

> **SO THE HONEST FINDING IS THE OPPOSITE OF THE ONE I WENT LOOKING FOR.** I opened this because a
> gate reporting *"families accepted: 94, refused: 0"* deserves suspicion, and because 36% of the
> population rests on it. The gate turns out to be narrow but sound, and **every family it accepted
> is consistent with its own note** — including all four a naive check called broken. The real
> limitation is not the families and not the gate: it is that these rules live in prose written for
> a human, carrying an inclusion range, named individuals, a stated count of exceptions, a
> `Controls:` clause and a `NOT covered:` clause. A parser picks the wrong clause. **If anyone wants
> this fully mechanical, the fix is structured fields in the declaration, not a cleverer regex** —
> and that is a change to the EC-7 format, which is not made casually and is not made here.

---

## Addendum 2026-09-13o — the second testable claim shape, and 78% of the EC-7 declared population

Addendum 13n tested the family notes' **span** claims and reached 13 families. The span shape is
rare. The common one is a **FORM** claim, and it is stronger.

The generated-code families — the reflection templates, the deleting destructors, the
static-initialiser registrations — do not describe a region. They describe a shape: *"all 1,149
bodies are exactly 92 bytes"*, *"254 members all 53 bytes"*, or a full partition,
*"188 at 46 B; 110 at 75-76 B"* and *"two body sizes (301 B (203) and 302 B (120))"*.

**A uniform-size claim is the strongest falsifiable statement in the EC-7 vocabulary: one member of
the wrong size refutes it outright.** A partition is stronger still, because it fixes the counts as
well, and `check_family_forms.py` also requires that **every** member land in some declared bucket —
a partition with a leftover is not a partition.

| | families | bodies | |
|---|---:|---:|---|
| MATCH | **20** | 5,493 | every member is the size its note claims |
| MISMATCH | **0** | 0 | |
| NO-CLAIM | 74 | 7,458 | no single unambiguous size; the checker declining |

### Both checks together

| | families | bodies | of declared |
|---|---:|---:|---:|
| span claim tested | 13 | 4,608 | |
| form claim tested | 20 | 5,493 | |
| **either** | **33** | **10,101** | **78 %** |
| neither | 61 | 2,850 | 22 % |

**No family declares both**, which is what one would expect: a note describes a region or a shape,
not both. **Zero mismatches across 10,101 bodies.** With both self-tests demonstrating a known
positive — the form checker's builds a family with one 91-byte member among 92-byte siblings and
requires that it fail — that is a real negative, not an absent one.

> **WHAT THIS DOES AND DOES NOT SAY.** It says that where a family's note makes a claim a machine can
> read, the members obey it — across 78% of the declared population, up from nothing this morning.
> **It does not say the families are correctly drawn.** That a body is 92 bytes does not prove it is
> PhyreEngine's reflection template rather than the game's own code; the notes carry that argument in
> prose — shared call targets, RTTI, instruction-form collapse — and those are still read by people.
> The size check tests the note's *stated* discriminator, which is exactly as much as it can do.

**I stopped extending the parser deliberately.** Each new phrasing was worth about two more families
by the end, and the 61 remaining notes state their rules in genuinely varied prose. Chasing them
would be a regex zoo, and the conclusion would not change: **the limit is that EC-7 rules are written
for humans, so full mechanisation needs structured fields in the declaration, not a cleverer parser.**
That remains a change to the EC-7 format, and it is still not made here.

---

## Addendum 2026-09-13p — half the "7,384 mentions" are already explained, and that corrects 13m

Addendum 13m split the 7,384 entry-only citations by body size and argued that a size bucket cannot
settle an individual row. That still holds. **What 13m never did was cross the population against
the DECLARED families, and doing so changes the shape of the largest qualifier on this database's
headline.**

`check_dispositions` prints, in every progress report:

> *7,384 of the 10,633 functions this scorer counts as cited are cited ONLY at their entry address
> by a DOCUMENTED page — a mention, not an explanation.*

Every word of that is true. The inference it invites is not.

| size band | entry-only | already declared B/C | genuinely undeclared |
|---|---:|---:|---:|
| 0-16  the entry IS the body | 791 | **409** (52%) | 382 |
| 17-64 | 1,573 | 622 (40%) | 951 |
| 65-256 | 3,728 | 1,951 (52%) | 1,777 |
| 257-1024 | 1,136 | 604 (53%) | 532 |
| 1025+ | 156 | 49 (31%) | 107 |
| **TOTAL** | **7,384** | **3,635 — 49%** | **3,749** |

**3,635 of those bodies are inside the 14,361 already.** They are explained *as a class* — by a
declared B or C family — and the fact that some page also names their entry address is incidental.
Presenting them among the 7,384 tells the same body's story twice: explained in the disposition
arithmetic, outstanding in the citation narrative.

The single largest contributor is `PClassDescriptorForType deleting destructors` — **all 1,149 of
them**, a PhyreEngine reflection template whose members are uniformly 92 bytes and whose form claim
was mechanically verified this same day (addendum 13o). Those are not 1,149 unexplained mentions.

> **THE GENUINELY UNDECLARED ENTRY-ONLY POPULATION IS 3,749, NOT 7,384.** That is still a real gap
> and it is still the largest one. It is half the size it has been reported at.

### This corrects a worklist I had already routed

`_index/entry-only-large-bodies.tsv` was published earlier today as **156 bodies / 387,465 bytes**
and handed to SWE2-FRONTIER as work. It was never crossed either. **49 of its 156 rows — 140,957
bytes, 36% of its mass — are already dispositioned** and are not work at all. The file now carries a
`declared_by` column and a header saying so; **the real queue is the 107 rows with an empty
`declared_by`, 246,508 bytes.**

> **WHY BOTH MEASURES MISSED IT, because it is a reusable lesson and not a one-off.** `measure_a`
> asks *"did a DOCUMENTED page cite inside this body?"* and the family gate asks *"is this body
> claimed by a declared class?"* Each is correct. Neither has ever been told about the other, so a
> body that answers *no* to the first and *yes* to the second is counted as explained by the
> arithmetic and as outstanding by the prose, **in the same report**. No figure was wrong. The two
> populations were simply never intersected, and an unintersected pair of measures will always
> produce a number that each side can read its own way.

**No metric moves here.** A + B + C is 14,361 and the frontier is 19,909, before and after. What
changes is that the qualifier under them now says which of its bodies are already counted above it.

---

## Addendum 2026-09-13q — the frontier decomposed, and a 57% that must never be quoted

Addendum 13p crossed one corner of the citation measure against the declared families and found half
of it already counted. `check_coverage_cross.py` now runs that cross over the **whole** population.
Its control is fatal: if the marginals do not reproduce 34,270 / 12,951 / 1,410 it refuses to print
the table, because a cross-tabulation measuring some other population would be far more convincing
than it deserves.

| | declared | not | total |
|---|---:|---:|---:|
| **A** — cited INSIDE by a DOCUMENTED page | 0 | 1,410 | 1,410 |
| entry-only, DOCUMENTED | 3,635 | 3,749 | 7,384 |
| cited, but neither of those | 250 | 1,600 | 1,850 |
| **not cited by any document at all** | 9,066 | **14,560** | 23,626 |
| TOTAL | 12,951 | 21,319 | 34,270 |

**`A` and the declared families are disjoint — 0 overlap, verified.** That is not luck: the family
gate refuses any member already measured as A, and this is the first time anything has checked that
the refusal actually holds across the whole store.

### What each measure uniquely reaches

| | bodies |
|---|---:|
| cited, no family — the citation axis alone | 6,759 |
| declared, never cited by any document — EC-7 alone | **9,066** |
| both | 3,885 |
| **touched by neither** | **14,560 — 42.49%** |

**EC-7's unique reach is the larger of the two.** 9,066 bodies are explained as a class by a family
and are cited by no document anywhere. A citation-only view of this project cannot see them at all.

> **THE UNION IS 57.51% AND IT IS NOT A COMPLETION FIGURE.** It must never be quoted as progress and
> the tool's own docstring says so. The two axes have completely different bars: `A` demands a
> DOCUMENTED page cite *inside* the body; a declared family demands a falsifiable class claim; and
> the citation axis at its weakest demands only that *some* document mention an address — which is
> the entire reason the entry-only qualifier exists. **A union of a strong measure and a weak one
> inherits the weak bar.** What the union is good for is its complement.

### The frontier is not one thing — and three quarters of it has never been mentioned

The frontier is 19,909 bodies that neither `A` nor a family claims. It decomposes:

| | bodies | |
|---|---:|---|
| **no document mentions them at all** | **14,560** | **73%** |
| entry-only mention | 3,749 | 19% |
| cited some other way | 1,600 | 8% |

That changes what "work on the frontier" means. **The 5,349 bodies some document already mentions
are a different task from the 14,560 nobody has ever written an address for** — the first needs a
page finished, the second needs one started. No published figure distinguished them before now, and
a worklist drawn from the frontier without this split would mix the two.

**No metric moves.** `engine_explained` is 31.06%, `A + B + C` is 41.91%, the frontier is 19,909 —
identical before and after. This addendum adds no explanation to anything; it says where the
unexplained part actually is.

---

## Addendum 2026-09-13r — the untouched work is half as clumped as the frontier looks

Addendum 13q found that 14,560 of the frontier's 19,909 bodies are cited by no document at all.
`check_frontier_shape.py` had already measured the frontier's contiguity and closed with the
reason it bothers:

> *What the runs decide is whether span dispositions are worth **attempting** at all — if the
> frontier were evenly scattered through documented code, they would not be.*

**It measures the runs over the wrong population for that question.** 5,349 frontier bodies are
already mentioned by some document, and they act as **bridges** between the ones that are not.

| | frontier (19,909) | untouched (14,560) |
|---|---:|---:|
| unbroken runs | 2,236 | **3,298** |
| longest run | 331 | 302 |
| in a run of ≥ 8 | 80.7 % | 54.1 % |
| in a run of ≥ 32 | 44.2 % | **15.8 %** |
| in a run of ≥ 128 | 8.4 % | 4.6 % |

**The untouched subset sits in MORE runs than the whole frontier, over 5,349 FEWER bodies.** Remove
the mentioned bodies and the frontier shatters. The share in a run of 32 or more falls by nearly two
thirds, and the fifteen longest untouched runs hold only **11 %** of the 3,225,312 untouched bytes.

> **SO THE ANSWER TO THE QUESTION THAT TOOL ASKS IS THE OPPOSITE OF WHAT ITS OWN FIGURES IMPLY.**
> Span and adjacency dispositions are substantially **less** worth attempting against the genuinely
> untouched work than against the frontier as reported. The remaining work is scattered, not
> blocked, and a span family carved out of it would be carving across code that is already
> documented or already declared. `check_frontier_shape.py` now prints this caveat above its own
> closing note, because the figures are otherwise read alone.

**Where the runs do point**, as candidates and nothing more: the longest is `0016AF20`–`0016D540`,
302 bodies in **9,792 bytes** — an average of 32 bytes each, which is a generated-stub shape worth
one person reading three of them. The largest by mass is `005850F0`–`00597200`, 220 bodies and
73,423 bytes, which is real code.

> **A RUN IS A PLACE TO LOOK, NOT A FAMILY.** Every disposition this project has accepted was argued
> from provenance — an RTTI class, a link span with justified edges, a uniform instruction form, a
> shared call target. **Adjacency is none of those**, and a family declared from adjacency alone is
> exactly the unsupported bulk disposition EC-7 exists to refuse. Nothing is dispositioned here and
> no metric moves: the frontier is 19,909 before and after.

---

## Addendum 2026-09-13s — one form image, two subsystems: why form collapse needs a target control

Addendum 13r said the longest untouched run, `0016AF20`–`0016D540`, was "worth one person reading
three of them". I read them. **The three-sample result was right and the conclusion I would have
drawn from it would have been wrong twice over.**

The three bodies share the MSVC dynamic-initialiser shape exactly:

```asm
sub rsp,0x28 / lea rcx,[a .data object] / call <ctor>
lea rcx,[a .text dtor] / add rsp,0x28 / jmp 00808B90   ; the atexit wrapper
```

Masking the four operand fields, **all 298 of the run's 32-byte bodies collapse to ONE form image**
and **all 298 tail-jump to the same target**. By the standard the accepted EC-7 families use —
*"N members, M byte images but ONE form image"* — that is a family.

### The first correction: the run is not the family

I found this shape by opening the longest contiguous run of never-mentioned bodies. **That is how I
looked, not what the family is.** Declaring "the bodies in `0016AF20`–`0016D540`" would have been an
adjacency family — the exact unsupported bulk disposition EC-7 exists to refuse, committed by the
person who refuses them.

Scanning the whole census for the form image instead finds **530 bodies, 232 of them outside the
run**, spanning `0015BCD0` to `00875630`. **The run covered 56% of the shape.**

### The second correction, and this is the methodological one

Those 530 bodies carry **one** form image. They do **not** carry one tail-jump target:

| | bodies | tail-jumps to | what that is |
|---|---:|---|---|
| **A** | **420** | `00808B90` | the CRT **atexit wrapper** — `call 00808B40`, normalise, return |
| **B** | **110** | `00639450` | **PhyreEngine class-descriptor code** — reads `[obj+0x70]`, sets bit 30 of `[obj+0xFC]` |

**The 298 I sampled were all group A. The sample could not see group B at all.** And the two groups
are not variants of one thing: A spreads over six constructors in a compact `0015Bxxx`–`0016Dxxx`
region; **B has exactly ONE constructor, `006388C0`, for all 110 members**, scattered from
`00584D10` to `00875630`, with its objects in `02CAxxxx`–`02CBxxxx`. They are two subsystems — the
CRT's static-initialisation path and PhyreEngine's reflection registration — that happen to be
emitted through the same 32-byte skeleton.

> **A MASKED FORM IMAGE IS NOT A SEMANTIC IDENTITY.** Form collapse proves the compiler emitted the
> same skeleton. It does not prove the bodies do the same thing, and **the field masking erases the
> very operand that distinguishes them.** A 530-member C family declared on form alone would have
> merged a CRT population with a middleware one under a single provenance sentence, and the sentence
> would have been false for one of them whichever way it was written.
>
> **This does not undermine the accepted families — it explains why their controls are there.** Every
> one of them pairs the form claim with resolved targets: *"CONTROL: three shared targets, each
> x138"*, *"all 298 call ONE target, 0063E2E0"*. That control is not decoration. **It is the half of
> the argument that form cannot supply**, and this is a concrete 530-body case showing what happens
> without it.

### State of the two groups, for whoever takes them

| | bodies | bytes | already declared | untouched |
|---|---:|---:|---:|---:|
| A → `00808B90` | 420 | 13,440 | **56**, in `C Runtime.NameRegistryEntry.StaticInitializer` | 360 |
| B → `00639450` | 110 | 3,520 | 0 | 103 |

**An existing family already holds 56 bodies of exactly group A's shape**, so group A is a question
about extending or siblinging that family, not a new claim. Group B is wholly undeclared.

**I have declared neither, and will not.** I am the adjudicator of EC-7 families; assembling the
evidence is mine, and ruling on a family I assembled is not. Routed to SWE2-EC7 with the members,
the form image, the resolved targets and the boundary question stated.

---

## Addendum 2026-09-13t — "unresolved = 0" is a tagging condition, and 61 of the 139 are already written up

`COMPLETION-PLAN` makes **`unresolved = 0`** a terminal condition and `ledger_resolved` sits at
99.59%. Read together they invite one reading: *139 functions nobody understands.* **That is not
what the number counts.**

`unresolved` means a body carries no `GFZ.V121.CodeDomain` classification in the coverage dump. It
is a **tagging state** produced by the checkpoint verifier. `progress.py`'s own guard settles the
semantics — it warns only when a residual address *is* classified in the dump, which would mean the
checkpoint had been mutated and not re-certified. **No warning fires today**, so the ledger is
internally consistent and all 139 are genuinely unclassified.

Whether the *database* explains a body is a different question asked by a different measure, and the
two had never been crossed. Crossed, the 139 (148,431 bytes, mean 1,067, largest 7,489) are:

| | bodies | bytes |
|---|---:|---:|
| **A** — a DOCUMENTED page explains its interior | **12** | 17,455 |
| entry-only mention by a DOCUMENTED page | 35 | 58,812 |
| cited by some document, not the above | 14 | 11,902 |
| declared by an EC-7 family | 0 | 0 |
| **nothing — no citation, no family** | **78** | 60,262 |

**61 of the 139 — 44% — are already touched by the database**, and twelve of them are fully
explained, by a page this addendum can name. `002AC5F0`, the **largest** residual at 7,489 bytes, is
one of them: `99-Unresolved-Residual/Glyph-Run-Rendering/drawing-a-line-character-by-character.md`
explains its interior.

> **SO THE TERMINAL CONDITION DOES NOT MEAN WHAT IT LOOKS LIKE IT MEANS.** Driving `unresolved` to
> zero is **checkpoint work — classifying bodies in the GZF and re-certifying** — not documentation
> work. Someone reading "139 unresolved" as a writing queue would spend effort re-explaining twelve
> functions that are already explained, and would still not move the number, because writing a page
> does not tag a body.

**And it gives the work an order.** The twelve A-explained bodies are the cheapest to classify:
whoever tags them has the evidence in hand and a page to cite. The 35 entry-only and 14
otherwise-cited come next. **The 78 that nothing touches — 60,262 bytes — are the only part that is
genuinely unexamined**, and they are 56% of the count but only 41% of the bytes.

| where the cheap end is | bytes | page that already explains it |
|---|---:|---|
| `002AC5F0` | 7,489 | `Glyph-Run-Rendering/drawing-a-line-character-by-character.md` |
| `00258350` | 1,942 | `Scripted-Camera/the-scripted-camera-player.md` |
| `0026F470` | 1,361 | `Weather/weather-probability-and-transition-roll.md` |
| `002AF960` | 1,117 | `Glyph-Run-Rendering/drawing-a-line-character-by-character.md` |
| `001D72F0`, `001D7A20` | 1,869 | `Application-Root/game-application.md` |

**No metric moves.** `ledger_resolved` is 99.59% and `unresolved` is 139, before and after. What
changes is that the 139 now has a shape and the cheapest end of it is named.

---

## Addendum 2026-09-13u — `questions_closed` cannot see an entire day's answers

`progress.py` classifies a register cell of exactly `**ANSWERED**` as UNTRUSTED — *"state inferred
from prose by the merge script"* — and counts it **neither as closed nor as open**. 296 rows sit
there, invisible to `questions_closed` in both directions.

`check_untrusted_answers.py` already split them by where the id appears elsewhere: 99 answered in a
structure the scorer reads, 3 with no verdict, 9 nowhere, and **185 that appear only in prose**. The
185 was left as "a mention is not an answer". **It was worth reading.**

| of the 185 prose-only ids | count |
|---|---:|
| whose own prose line says answered / resolved / settled / censused | **165 — 89 %** |
| of those, carrying an explicit date | 141 |
| attributed to FABLE | 102 |
| carrying no such marker — these need reading, not assuming | 20 |

They are not vague mentions. They read like this:

> **`AJ-7` ANSWERED 2026-09-12 (FABLE): the one MT19937, and yes — they share it**
> **`DE-3` answered 2026-09-12 (FABLE): the higher band is five opcodes** (`0031297D`–`003129A3`)
> **`CQ-1` answered 2026-09-12 (FABLE): the chain-rank bonus roll** … draws three LCG steps

— with the superseded text struck through above each one, across **93 pages**.

> **THE REGISTER SAYS ANSWERED. THE PAGE SAYS ANSWERED, WITH SUBSTANCE. THE SCORER DISTRUSTS BOTH,
> BECAUSE THE REGISTER CELL IS EMPTY.** `questions_closed` reads checkbox items and register table
> rows; an answer written into a page's narrative is invisible to it. **A day's work by FABLE on
> 2026-09-12 is not counted anywhere** — and it cannot be, until the text is carried into the cell.
> This is the same failure as the entry-only citations one addendum earlier: *the structure the
> scorer reads is not where the content lives.*

**The fix is propagation, not research.** `_index/candidates/untrusted-rows-answered-in-prose.tsv`
maps each of the 165 to the page and the exact line that answers it, with author and date.

> **AND I HAVE NOT RECLASSIFIED ONE OF THEM.** Moving 165 rows into `closed` would move a scored
> dimension by roughly seven points on the strength of a keyword match. **A marker is evidence that
> an answer was written, not a reading of whether the answer is good**, and that judgement belongs
> to whoever owns the question. Routed to FABLE, who wrote 102 of them.

**The worklist carries its own known defect, stated in its header.** The marker is matched at line
level, so a line that answers one id while doing something weaker to another tags both: `AF-1`'s
line reads *"AF-1 **narrowed**, AF-2 and AF-3 **answered**"* and AF-1 was narrowed. **165 is a count
of rows worth reading, not a count of answers.**

**No metric moves.** `questions_closed` is 996 / 2,275, before and after.

---

## Addendum 2026-09-13v — `questions_closed` counts at least 301 questions twice, and 17 rows disagree with their own pages

`progress.py` builds the dimension from two populations and **adds them**:

```
611 closed /  714 open   in per-document sections   = 1,325
384 closed /  566 open   in the register            =   950
                                                      -----
                                                      2,275   <- the denominator
```

Those had never been intersected by id. Intersected:

| | ids |
|---|---:|
| per-document checkbox questions carrying an id | 301 |
| register rows carrying an id | 1,106 |
| **in BOTH** | **301** |
| per-document only | **0** |
| register only | 805 |

> **EVERY SINGLE IDENTIFIED PER-DOCUMENT QUESTION ALSO HAS A REGISTER ROW.** `doc only` is zero. So
> at least **301 of the 2,275 — 13% — are the same question counted twice**, once in each half.

**The bound is a floor, not an estimate.** 1,013 per-document checkbox items carry no id at all and
cannot be matched this way. Their text matches a register row exactly in only 2 cases, and a fuzzy
sample of six found one clear reworded mirror at 0.82 similarity against five non-matches around
0.47–0.53 — so most of those 1,013 look genuinely distinct, and a few are not. **301 is what can be
proved; the true duplication is somewhat higher and is not quantified here.**

> **AND I HAVE NOT DEDUPLICATED, WHICH MATTERS MORE THAN THE FINDING.** Removing 301 duplicate
> countings takes the denominator from 2,275 to 1,974 and `questions_closed` from **43.78% to about
> 50.5%** — nearly seven points, from a definitional change, with no question answered. That is
> precisely the inflation this project's rules exist to refuse, and a scoring change is not mine to
> make alone in any case. **The measurement is published; the decision is routed.**

### Seventeen rows disagree with their own page

| the disagreement | rows |
|---|---:|
| document says **open**, register says **closed** | 5 |
| document says **closed**, register says **open** | 2 |
| document has a verdict, register cell is unstated | 10 |

The first seven are direct contradictions and belong to pass 28. The register claims an answer the
page denies for `AA-6`, `AG-1`, `AG-5`, `AO-5`, `S-1`; the page claims one the register denies for
`EF-1` and `Z-9`. **Which side is stale requires reading both** — `check_untrusted_answers.py`
already carries that warning from the day its author assumed the register was the thin one and all
three cases ran the other way.

Three of them — `Z-3`, `Z-9`, `Z-16` — are on one page, `09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md`,
which is where anyone settling these should start.

**No metric moves.** `questions_closed` is 996 / 2,275 before and after.

---

## Addendum 2026-09-13w — I went looking for thin audit blocks and found three of my own

`audit_coverage` carries weight **0.15**, three times `questions_closed`, and sits at 348/349. It
counts a page as audited when `passes > 0` **and** `last_pass_state` is present and not `null` — or
when `falsification_passes > 0` **and** the body carries a written falsification-pass section. The
scorer's own comment states the principle it was corrected into:

> *the whole point is that a number in the frontmatter is a claim, and only the section is evidence*

But the test reads `last_pass_state:\s*(\S+)` — **one token**, checked only against the string
`null`. A state of `x` satisfies it. So: how many audited pages record a state a reader cannot
re-derive anything from?

**174 of 348 record a state of 40 characters or fewer**, most of them the bare label
`falsification-pass`. Stated alone that is a 50% finding on a 0.15-weight dimension.

> **THE CONTROL REVERSED IT. 159 of those 174 — 91% — carry a written falsification-pass section in
> the body, median 863 characters, up to 4,361.** The frontmatter label is a label; the evidence is
> in the section, exactly where the scorer's own comment says evidence belongs. **This dimension is
> in better shape than a frontmatter-only reading makes it look**, and the 174 figure published
> alone would have been the same error this addendum series keeps finding: measuring the structure
> the instrument parses instead of the one the content lives in.

### Fifteen have neither — and three of them are mine

| | pages |
|---|---:|
| thin state, but a real falsification-pass section | 159 |
| **thin state and no section at all** | **15** |

**Three of the fifteen are pages I audited today**: `the-vif1-vu1-layer.md`,
`effect-element-type-dispatch.md` and `the-menu-effect-registry.md`. I wrote their audit blocks as
YAML **block scalars** (`last_pass_state: >-`), so the token the scorer captures is `>-` — non-null,
therefore passing — and **not one character of what I actually wrote is visible to it.** 345 of the
348 audited pages write the state inline as `<slug> - <prose>`, which puts a meaningful identifier in
the first token. I was the outlier, **while auditing other people's pages for this exact class of
defect.**

Converted to the corpus convention, content preserved verbatim; the first tokens are now
`opus-vif1-vu1-pass-1`, `opus-effect-dispatch-pass-1` and `opus-menu-effect-registry-pass-1`.
`audit_coverage` does not move — they were already counting, on the strength of `>-`.

**The remaining twelve are reported, not judged.** Eleven record
`reverification-against-current-parent` and one a build identifier; each names a pass without saying
what it found, and none has a section. That may be a legitimately different kind of stamp — a
re-verification against a new parent is not a falsification pass — so it is a question for whoever
owns those pages, not a defect I have established.

> **AND THE SCORER CANNOT READ A BLOCK SCALAR AT ALL.** `(\S+)` stops at the first token. Any page
> using `>-` passes on punctuation while its actual state goes unread. Three pages do; they were all
> mine and they are now fixed. The gap in the regex remains, and is recorded here rather than
> patched, because changing what `audit_coverage` accepts is a scoring change.

---

## Addendum 2026-09-13x — the 0.55 dimension, audited: 62% of it rests on a single citation

`engine_explained` carries **weight 0.55 — more than every other dimension combined** — and counts a
body as explained when **some document cites an address inside it**. That measure had never been
examined for what it admits.

| of the 10,739 bodies it counts | | |
|---|---:|---:|
| cited **exactly once**, anywhere in the database | **6,702** | **62.4 %** |
| cited twice | 1,129 | 10.5 % |
| cited 3–5 times | 1,311 | 12.2 % |
| cited 6–20 | 1,228 | 11.4 % |
| cited 21+ | 369 | 3.4 % |

| who is doing the citing | | |
|---|---:|---:|
| at least one **AUDITED or DOCUMENTED** page | 8,925 | 83.1 % |
| **only** pages not claiming to be finished | **1,814** | **16.9 %** |

Those 1,814 are carried by PARTIAL (1,497), REOPENED (335), NONE (253) and CONTRACT (3) pages, and
total **760,474 bytes**. 843 bodies are in both thin classes — cited once, by an unfinished page.

> **NEITHER NUMBER IS A DEFECT ON ITS OWN, AND THIS ADDENDUM DOES NOT CLAIM ONE.** A short function
> can be explained in a single line; a PARTIAL page can explain a particular body perfectly while
> being incomplete elsewhere; a page can explain a mechanism in prose and cite its address once. **A
> single citation is not evidence of non-explanation.** What the shape shows is that 62% of the
> largest-weighted dimension rests on evidence that nothing distinguishes from a passing mention.

### But it does admit the opposite of explanation, and here is the proof

`the-vif1-vu1-layer.md` is **PARTIAL** and says so in its own header: *"Not read: **what any single
microprogram draws**."* It cites 20 bodies exactly once each, **34,809 bytes**. Three of the largest —
`00499A20` (7,726 B), `0049D540` (10,573 B), `004A8B00` (8,992 B) — appear in exactly one sentence,
and that sentence reads:

> *"larger bodies (`00499A20`, `0049D540`, `004A8B00`, …) that **may be sub-programs reached by VU
> `JAL` / `JR` or installed by a path not found yet**."*

**That is the page stating it does not know what they are.** `engine_explained` counts all three as
explained — 27,291 bytes of them. This is not an inference about the 6,702; it is an existence proof
that the measure admits a sentence saying *we have not found how these are reached*.

> **THIS IS WHY `A` EXISTS, AND IT QUANTIFIES THE REASON.** `check_dispositions` already warns that
> *"interior citation is a stricter PROXY, not a true count"*. The proxy is stricter — it demands a
> DOCUMENTED page and an interior address — and it lands at **1,410** against `engine_explained`'s
> 10,739. Neither figure is the truth, and this addendum does not propose changing either: **the
> weighting is a scoring decision and is not mine to make.** What is now on the record is the
> distance between them, attributed rather than asserted.

**No metric moves.** `engine_explained` is 31.27% before and after.

---

## Addendum 2026-09-13y — both 100% dimensions challenged from outside their own documents; both held

A dimension at 100% is the one nobody re-examines. `registry_explained` (63/63) and `ebp_explained`
(14/14) are the last two scored surfaces never audited, and both are scored against a population
their own authors defined. That is the authored-denominator risk `progress.py` already warns about
for a different dimension — *"see check_formats.py for why a formats metric with an authored
denominator is worthless"* — and neither had been tested from outside the document that declares it.

**Both survive. Recorded because a real negative is worth as much as a defect, and only if it says
what would have falsified it.**

### `ebp_explained` — the census covered one locale of nine

The 14 units are the container plus 13 section types, censused by unpacking **1,115 us-language
scripts**. The archive holds **10,045 `.ebp` entries across nine locales**, and they are not equal:

| locale | scripts |
|---|---:|
| `ch`, `in` | **1,119** |
| `kr`, `cn` | 1,116 |
| `us`, `it`, `fr`, `es`, `de` | 1,115 |

**Five script units exist that the census never saw** — the four ATEL control modules
(`ctrl`, `btlctrl`, `evctrl`, `mapctrl`) and the title script `ttl_a01_e3`. If any carried a section
index outside the frozen thirteen, the population would be short and 14/14 would be 100% of the
wrong set.

Parsed from their containers — 20 slot offsets at `+0x10`, a zero meaning absent — they use sections
**0, 2 and 6 only**. All three are already in the census. **Nothing outside it.** The frozen
population holds.

### `registry_explained` — the bounds and the count both come from one document

The population is 63 slots, `02EBF008`–`02EBF1F8` on an 8-byte stride, *"derived from the registry
document's own bounds, and cross-checked against the slot count it states"*. **Both halves of that
cross-check come from the same document**, so neither can catch a truncated table. And the table
cannot be read from the file at all: its VA lies past the raw image, zero-filled on disk and
populated at runtime.

So the bound was tested against **the code that writes it**. A rip-relative sweep of `.text` finds
stride-aligned references at `02EBF200` and `02EBF208`, immediately past the declared end — exactly
the shape of a table that continues further than its document says.

**It does not continue.** The registry has one setter per slot, in a series 0x30 apart:

```asm
00238570  mov rcx,[02EBF1F0] / test / call 003844F0 / mov [02EBF1F0], rbx
002385A0  mov rcx,[02EBF1F8] / test / call 003844F0 / mov [02EBF1F8], rbx
002385D0  cmp ecx,0x1B / lea rcx,[01E09F68] / movzx ...   <- a different shape entirely
```

**The setter series ends at `002385A0`, whose slot is `02EBF1F8` — the declared last slot.** The next
function in series position is a jump-table dispatcher, not an accessor. `02EBF200` and `02EBF208`
are touched by `00236C30` and `00233E00`, unrelated functions far from the accessor family. The
63-slot denominator is confirmed independently of the document that declares it.

> **WHAT WOULD HAVE FALSIFIED EACH, SO THE NEGATIVES MEAN SOMETHING.** For EBP: any section index in
> those five uncensused units outside `{0,2,3,4,6,8,9,10,11,12,14,16,19}`. For the registry: a setter
> of the same form at `002385D0` referencing `02EBF200`. Both were looked for and neither is there.
>
> **AND THE SWEEP THAT FOUND THE CANDIDATE IS WEAK, WHICH IS WHY IT DID NOT DECIDE.** It scans
> undecoded 4-byte displacements and tries three instruction tails, giving 176 distinct targets in a
> window holding ~63 slots. It is a *pointer to where to disassemble*, and the disassembly is what
> settled it.

**No metric moves.** `registry_explained` 63/63 and `ebp_explained` 14/14, before and after.

---

## Addendum 2026-09-13z — the 296 untrusted rows, fully accounted: 92% have a findable answer

Three addenda have now chipped at the 296 register rows `progress.py` counts **neither** as closed
nor as open. This closes the accounting, and **corrects my own framing in 13u.**

| where the answer actually is | rows | does an answer demonstrably exist? |
|---|---:|---|
| in a checkbox or table row elsewhere | 99 | **yes** — all 99 `closed`, none contradicted |
| in a page's prose, with an explicit marker | 165 | **yes** — 141 dated, 102 by FABLE, 93 pages |
| **inside the register row itself** | **9** | **yes** — see below |
| in prose with no marker | 20 | needs reading |
| mentioned with no verdict anywhere | 3 | needs reading |
| **total** | **296** | **273 — 92% — have a locatable answer** |

### The nine I called "supported by nothing" are fully answered

`check_untrusted_answers.py` labels them **NOWHERE**, and its own docstring said *"nothing supports
the ANSWERED, and nothing contradicts it either."* **That is wrong, and I repeated it in 13u.** The
test looks *outside* the register, so it cannot see an answer written *inside* the row. The register
is `ID | Question | Owner document | Status`; the thin `**ANSWERED**` is only ever the **Status**
cell.

All nine carry a full, attributed answer in their Question or Owner-document cell:

> **`J-A`** — *"**ANSWERED 2026-09-12 (FABLE): the header carries it** — `+0x04` is a `uint32` row
> count, read at 120 sites after registry-slot loads; nine consumers bound an index on it with `jae`
> before resolving `+0x0C` (`00237FF5`, `002388B5`, …) and 43 more use it as a loop bound."*
>
> **`EZ-6`** — *"**ANSWERED 2026-09-12 (FABLE), ledger reconciled:** one reader image-wide,
> `BattleUnit_ProcessDefeatRewardsAndLoot` (`003122F4`) … **Correction: bit 2 is not set on every
> apply.**"*

**I read these as unanswered from a 110-character truncation, and my own keyword pass disagreed with
me. The keyword pass was right.** The instrument's NOWHERE definition is corrected in place — the
key is kept because it is published output, and the docstring now reads *"no support outside the
register, never nothing supports it."*

> **THE UNTRUSTED BUCKET IS OVERWHELMINGLY A FORMATTING ARTEFACT, NOT UNKNOWN WORK.** 273 of 296
> rows have an answer someone can go and read today. What every one of them lacks is **text in the
> Status column**, which is the only thing `progress.py` inspects. **The same content, moved one
> cell left or one page over, is invisible to the score.**
>
> That is now the third distinct place this surface hides an answer from its own scorer — a page's
> prose, a checkbox on another page, and the row's own adjacent cell. **The defect was never that
> the answers are missing.**

**And still nothing is reclassified.** 273 rows is roughly twelve points of `questions_closed` on a
keyword match. The measurement is published and the decision stays with the question owners and with
whoever owns the scoring.

**No metric moves.** `questions_closed` is 996 / 2,275, before and after.

---

## Addendum 2026-09-13aa — the seven verdict contradictions adjudicated, and S-1 answered

Addendum 13v found 17 register rows disagreeing with their own pages, seven of them direct
open/closed contradictions, and routed them. **Nobody claimed them, and adjudicating contradictions
is mine.** All seven are now settled by reading both sides.

| id | page says | register says | verdict |
|---|---|---|---|
| `AA-6` | open *and* closed | closed | **NOT A CONTRADICTION — my detector's fault** |
| `EF-1` | closed | open | register **stale** |
| `Z-9` | closed | open | register **stale** |
| `AO-5` | open | closed | register **wrongly claims closed** |
| `AG-1` | open | closed | register **wrongly claims closed** |
| `AG-5` | open | closed | register **wrongly claims closed** |
| `S-1` | open | closed | **answered today — see below** |

### `AA-6` was mine, not the corpus's

`persistent-flag-banks.md` carries two lines mentioning `AA-6`. One is ticked and reads
**`AA-6 CLOSED`**. The other is **unticked and is about `AA-8`** — *"filed 2026-09-02 as a second
`AA-6`; **renumbered 2026-09-08**"* — and my line-level id extraction took that renumbering note as
`AA-6`'s own verdict. **The same line-level matching error that produced `AF-1` in the prose
worklist**, in a second costume. The real count of contradictions is **six**, not seven.

### `S-1` is answered, and both of its options were wrong

*"Whether `.gfids` contains real RVAs or is zero-filled padding."* **Neither.**

The section's **virtual size is 48 bytes** — the 512 on disk is padding, all zero from byte 48. Those
48 bytes hold **twelve `u32` values**: `0x31 0x30 0x13 0x0A 0x0D 0x10 0x45 0x71 0x0A 0x62 0x37 0x0B`.
Not zero, and **not one is a plausible RVA**: `.text` spans RVA `0x1000`–`0x7A1635` and the largest
value here is 113. What the twelve integers mean is **not established**, and the answer says so.

**The load config settles the CFG half outright.** At RVA `01BCBE40`: `GuardCFFunctionTable` = **0**,
`GuardCFFunctionCount` = **0**, while `GuardCFCheckFunctionPointer` (`008C31C0`) and
`GuardCFDispatchFunctionPointer` (`008C31C8`) are both **set**, with `GuardFlags` = `0x100` —
`CF_INSTRUMENTED` **without** `CF_FUNCTION_TABLE_PRESENT`. **The target list is absent by
declaration, not by omission**: a link that had merely failed to finish would not clear the
table-present flag while keeping the instrumentation flag. That is the distinction S-1 was filed to
draw, answered from the load config rather than from the section size the page had been reasoning
from.

> **AND IT IS WRITTEN AS A TICKED CHECKBOX, DELIBERATELY.** The last three addenda established that
> an answer the scorer cannot see is an answer that does not count — 165 of them in page prose, 99 in
> a checkbox elsewhere, 9 in a register cell one column over. **`questions_closed` moved 996 → 997.**
> That is the first metric movement I have caused, and it came from answering a question with
> evidence, not from redefining a denominator.

**The five remaining contradictions are not mine to resolve** — each needs its page owner to say
which side is stale, and two of them (`EF-1`, `Z-9`) are stale in the register against answers the
pages already carry, which is the cheap direction. They stay open in
`OPUS-CONTRA-QUESTIONS-DOUBLE-COUNT`.

---

## Addendum 2026-09-13ab — one registry slot nothing references, and a scan I should never have written

`AG-5` asks whether the authored-table header is uniform across all 63 registry slots or only the
three read. `J-A`'s answer censused the band `02EBF000`–`02EBF178` — **which stops at slot 46 of 63**
— so the question is live for the upper sixteen.

**I did not answer it, and the way I failed is the point.**

### The instrument I wrote was wrong three times

I hand-rolled a byte scan for rip-relative loads of each slot. In order:

1. **It counted SETTERS as consumers.** Every slot has a setter of one form — `mov rcx,[slot]` to
   fetch the old pointer, `call 003844F0` to release it, `mov [slot],rbx` to store the new one. That
   load is not a consumer and will never read a header. Counting it made the upper slots look
   unread: a "7% read `+0x04`" figure that was an artefact of which slots have setter-only
   references.
2. **Corrected, it still missed `lea` entirely.** `02EBF1A0` is address-taken 13 times across four
   functions; my scan saw none of it, because it only matched dereferences.
3. **And it was simply wrong about a slot.** It reported `02EBF198` as having a setter. It has no
   references of any kind.

> **THE KIT ALREADY HAD THE RIGHT TOOL AND I DID NOT LOOK.** `data_xref_scan.py` takes
> `--range LO HI --stride N` and **refuses to run without a `--control`: a VA known to be
> referenced, so that an absence in its output means something.** That is the discipline my ad-hoc
> version lacked, and it is the discipline this whole addendum series is about. **Reaching for a
> fresh scan instead of the instrument built for the question cost three wrong intermediate
> readings, none of which reached publication only because each was checked.**

### What the right tool says

Control `02EBF138`: **723 references** — the control passes, so absence is meaningful.

| | slots | total refs | median per slot |
|---|---:|---:|---:|
| censused band `02EBF008`–`02EBF178` | 47 | 1,876 | **10** |
| beyond it `02EBF180`–`02EBF1F8` | 14 | 137 | **2** |

The upper slots **are** referenced — my "setter-only" reading is retracted — but far more lightly.
`02EBF190` alone carries **318 references in 176 functions**, and `02EBF188` 93 in 40.

### `02EBF198` is referenced by nothing

**Of the 63 slots, exactly one has no reference of any kind**: no reader, no setter, no
address-taken. Verified two independent ways — `data_xref_scan.py` over all 34,270 function bodies,
and a raw displacement sweep of `.text` that finds **0 candidate sites**, inside a listed body or
outside one. The same sweep finds all 318 of `02EBF190`'s, so it is not blind.

> **AND THE STRONG WORD IS BOUNDED.** *Nothing references it* means **no rip-relative displacement
> in `.text` resolves to it**. A slot reached only through an indexed access from a registry base
> pointer would not appear — though that is not this registry's pattern, since `00236C30` takes the
> address of some thirty-five slots **individually**. An allocated-but-unused slot is the simple
> reading; it is not the only one, and settling it belongs to the page that owns the registry.

**AG-5 remains open.** What is added is the reference distribution it needs, one unreferenced slot,
and the retraction of three readings of my own that a less careful pass would have published.

---

## Addendum 2026-09-13ac — correcting my own 165 upward: the answer vocabulary was wider than I searched

Addenda 13u and 13z reported that **165 of the 185** prose-only untrusted rows carry an explicit
answer marker, and that **273 of 296** rows overall have a locatable answer. **Both figures are too
low, and the cause is mine: I searched for a vocabulary narrower than the corpus uses.**

I matched `answered|resolved|settled|censused|fixed`. This corpus also closes a question with
**`closes`**, **`closed`**, **`corrected`**, **`narrowed`**, **`placed`**, and with the
`~~strikethrough~~` convention alone:

> *"all four bits are now placed. **`EX-7` closes.**"*
> *"**`M-4` closed 2026-09-12 (FABLE):** …"*
> *"~~so it is a small enum or count, not a magnitude~~ **corrected 2026-09-12 (FABLE, `CB-8`)**"*

Widening the vocabulary moves the prose-only count **166 → 179**, adding `AJ-6 AK-5 BM-1 CB-8 EX-7
EZ-1 FB-5 FB-6 FD-3 FJ-3 FK-1 FZ-28 M-4`.

### And one more is answered in a structure with no marker at all

`PS-1`'s answer is a **section heading**:

> *`## 10. Extension 2026-09-12 — the scalar is the object's distance from the viewer, and the node
> is the distance-fade colour (PS-1)`*

No marker word, because a heading that states the answer does not need one. **That is the fourth
distinct place this surface hides an answer from its scorer** — after a page's prose, a checkbox on
another page, and the register row's own adjacent cell.

### The corrected accounting

| | 13z published | corrected |
|---|---:|---:|
| prose-only with a locatable answer | 165 | **180** of 185 |
| **all 296 rows with a locatable answer** | **273 — 92%** | **288 — 97%** |

**Five are genuinely open or ambiguous**, and they are named so nobody re-derives the list:
`AG-9`, `CD-3`, `DG-7`, `EC-1`, `FC-2`.

> **`AG-9` IS THE QUESTION I RAN INTO MYSELF TODAY.** It asks for *"a base-plus-index scan keyed on
> the registry's own base"* — precisely the caveat addendum 13ab had to attach to
> `02EBF198` having no references: a slot reached only through an indexed access from a base pointer
> would not show in a displacement sweep. **The open question and my open caveat are the same
> question**, and neither knew about the other until now.

> **THE LESSON IS THE ONE THIS SERIES KEEPS FINDING, NOW TURNED ON MY OWN SEARCH.** I have spent the
> day showing that the scorer measures the structure it parses rather than the one the content lives
> in. **My keyword pass did exactly the same thing** — it measured the vocabulary I thought of. It
> was right about every row it flagged and wrong about thirteen it did not, and the direction of the
> error was to understate how much work had already been done.

**No metric moves.** `questions_closed` is 997 / 2,275, before and after. Nothing is reclassified:
288 rows is still a keyword match, and the judgement still belongs to the question owners.

---

## Addendum 2026-09-13ad — the registry loader mapped: AG-9 answered, AG-5 advanced, and 13y qualified

`00236C30` (1,037 bytes) is the **STATIC authored-data loader**. It takes one loaded blob at
`0208E680` and distributes dwords from its header into registry slots, **two different ways**:

```asm
lea rcx,[slot] / movsxd rdx,[blob+N] / call 003845F0    ; RELOCATING store
movsxd rax,[blob+N] / mov [slot],rax                    ; DIRECT store, no fixup
```

`003845F0` stores the value into the slot **and then fixes up the table it points at** — adding the
table's own base to the base-relative fields at `+0x0C` and `+0x10` to make them absolute. So a
relocating store means the slot holds a **table**; a direct store means it holds a **plain value**.

| | count | where |
|---|---:|---|
| relocating stores — slot holds a table | **33** | all inside the censused band |
| **direct stores — slot holds a plain dword** | **2** | `02EBF180` ← blob`+0x04`, `02EBF200` ← blob`+0x11C` |

### AG-9 is answered: no, and there is no base-plus-index scan to find

`AG-9` asks for *"a base-plus-index scan keyed on the registry's own base"*. **There is none.** The
mapping is an **explicit, non-monotonic, compiler-unrolled slot←offset table baked into this one
function** — `02EBF018` from blob`+0x0C`, then `02EBF0B8` from `+0x10`, `02EBF0A8` from `+0x14`,
`02EBF0B0` from `+0x18`. Slot order does not follow blob order and never returns to it. Nothing
indexes the registry from its base because **nothing needs to**: the correspondence is code, not
arithmetic.

That also settles the caveat addendum 13ab attached to `02EBF198` having no references. **The
indexed access it hedged against does not exist**, so `02EBF198` is unwritten by this loader and
unreferenced anywhere — an allocated slot with nothing in it.

### AG-5 advanced: the registry is NOT uniform

Two of the 35 slots this loader writes receive a **plain dword and no fixup**. They do not point at a
table and have no header to be uniform about. **`AG-5`'s answer is therefore "no" for at least
`02EBF180` and `02EBF200`**, and the remaining question is narrower than it was: whether the *33
table slots* share a header, not whether all 63 do.

### And it qualifies my own addendum 13y

13y confirmed the registry bound `02EBF008`–`02EBF1F8` against the per-slot setter series, and
dismissed the stride-aligned references at `02EBF200` as *"touched by unrelated functions far from
the accessor family"*. **`02EBF200` is written by `00236C30` — the loader that populates the
registry — from the same blob header, four bytes past the last table slot.**

> **THE BOUND IS STILL RIGHT, AND THE REASON IS NARROWER THAN I GAVE.** `02EBF008`–`02EBF1F8` is the
> extent of the **setter-managed table-pointer family**, and the setter series does end at
> `002385A0`. But the *structure the loader fills* does not stop there: it writes two plain-value
> fields, one inside the range and one past its end. **A denominator of 63 counts the pointer table,
> not everything `00236C30` initialises**, and 13y should have said so.

**The blob header is larger than the registry consumes.** The 34 dwords used span `+0x0C` to
`+0x11C` — a range holding **69 dwords, of which 35 go nowhere near the registry.** What those hold
is not established here.

**No metric moves.** `registry_explained` is 63/63, before and after.

---

## Addendum 2026-09-13ae — the STATIC resource contract, and 28 header dwords nothing reads

Addendum 13ad mapped `00236C30`'s distribution of the STATIC blob into registry slots and left the
question of the **35 header dwords it does not consume**. Following the blob pointer closes the whole
contract, because **only three functions in the image reference `0208E680`.**

### The contract

```
003843F0(0x13, 00238850, "STATIC")     registered by 00236C30 on its release path
                                        -- resource KIND 0x13 = 19, name "STATIC"

00238850(id)   36 bytes, the handler
   movsxd rdx, ecx            the id
   lea    rcx, [0208E680]     &the blob pointer
   call   003846F0            load the resource into it
   mov    ecx, 1
   jmp    00236C30            ... then distribute

00236C30(1)    1,037 bytes, the distributor
   33 x  lea rcx,[slot] / movsxd rdx,[blob+N] / call 003845F0    relocating: slot holds a TABLE
    2 x  movsxd rax,[blob+N] / mov [slot],rax                    direct: slot holds a PLAIN DWORD

00236C30(0)    the release path
   call 003844F0 on the blob, null 0208E680, re-register the handler
```

`003845F0` is the fixup: it stores the value into the slot, then adds the table's own base to the
base-relative fields at `+0x0C` and `+0x10` to make them absolute. **That is why the tables' headers
are self-relative on disk and absolute in memory**, and it is the mechanism behind `J-A`'s row count
at `+0x04` being directly readable while neighbouring fields need relocation.

### At least 28 header dwords are never read

Of the **69 dwords** spanning `+0x0C`–`+0x11C`, the distributor consumes **34**. Of the remaining 35:

| | dwords |
|---|---:|
| consumed into a registry slot | 34 |
| appearing as some `[reg + N]` read in one of the three functions | ≤ 7 |
| **matching no read at all in any of the three** | **≥ 28** |

> **THE BOUND IS A FLOOR AND THE METHOD SAYS WHY.** The offset extraction counts **any** `[reg + N]`
> in those functions, not only reads off a blob-derived register — so it **over-counts** reads, and
> the seven in the middle row are an upper bound on "possibly read". Over-counting reads can only
> shrink the unread set, so **28 is the minimum**, not an estimate.
>
> **And "nothing reads them" is bounded to the pointer.** It means no read through `0208E680` in the
> only three functions that reference it, none of which aliases the pointer anywhere else. A consumer
> handed a pointer *into* the blob by some path not through that global would not appear — though
> `00236C30` passes only individual dwords to `003845F0`, never the blob itself.

**So the STATIC blob's header is roughly half unused by the registry it feeds**, and what the
remaining dwords are for is not established here. That is a bounded, named question rather than a
gap: three functions, one global, and 28 offsets with no observed reader.

**No metric moves.**

---

## Addendum 2026-09-13af — `OPEN-QUESTIONS.md` cannot see 84% of the open questions

Addendum 13aa adjudicated `EF-1` and `Z-9` as *"register stale against answers the pages already
carry"* and called that the cheap direction. **Acting on it found something else.**

Both register rows read **"PARTLY / PARTIALLY ANSWERED"**, which `progress.py` correctly scores
`open` — a partial answer is not a closed question. So the register looked like the *precise* side
and the pages like the coarse one, and I nearly published that as a self-correction. **Reading each
case separately is what stopped it**, because the two are not alike:

- **`EF-1`** — the page's 2026-09-13 answer censuses **all six** functions that reach a result slot
  through the record idiom and fixes the tag set at `{0,1,2,3}`. That genuinely supersedes the
  register's 2026-09-08 *"tag 3 is float32"*. **Register stale; the page is right.**
- **`Z-9`** — the page ticks **the mechanism only** and says so outright, then carries the remainder
  *below as its own unticked question*: *"the box is ticked for the mechanism only … carried below
  as its own question rather than left inside a ticked one."* **The page is right, and it is better
  practice than either the register or my adjudication.**

### And `Z-9`'s successor has no register row

If I had closed `Z-9` in the register, its open remainder would have vanished from the register
altogether — **the successor question exists only as an unticked checkbox on a page.** The register
was not stale about that half; it was *carrying* it.

That is not one question's accident. Measured across the corpus:

| per-document checkbox items | |
|---|---:|
| open | 715 |
| closed | 613 |
| **open, carrying NO question id** | **600 — 84% of open** |
| open, with an id the register lacks | **0** |

**Every identified question is registered. 600 open questions were never identified**, and a
register keyed on ids cannot hold them. They are not small: *"stack arguments are not detected"*,
*"types are not derived, only slots"*, *"the remaining 222 `ABI_UNRESOLVED_DEFAULT` functions"*.

> **THIS IS THE EXACT MIRROR OF 13u AND 13z, AND THE PAIR IS THE POINT.** There, **answers** lived in
> page prose, in a checkbox on another page, in a register cell one column over — everywhere except
> where the scorer looks. Here an **open question** lives in a page checkbox with no id — everywhere
> except where the register looks. **The same structural gap, running both ways: the index and the
> content are kept in different places and neither is complete.**

> **WHAT THIS DOES *NOT* MEAN.** `questions_closed` does **not** undercount because of this: the 600
> are counted in the per-document half of the denominator. The defect is in
> **`OPEN-QUESTIONS.md` as an index** — anyone using it as the worklist is seeing 16% of the open
> questions. That is a different and smaller claim than "the metric is wrong", and it is the one the
> evidence supports.

**Nothing edited.** `EF-1` and `Z-9` stay as they are: closing `Z-9` in the register requires its
successor to be registered first, and issuing a question id is the page owner's act, not mine.
`questions_closed` is 997 / 2,275, before and after.

---

## Addendum 2026-09-13ag — AG-1's two slots have different producers, and neither is in the STATIC loader

`AG-1` asks what `02EBF190` and `02EBF138` hold — *"the highest-value"* question on the registry
page, and the two most-referenced slots in it: **723 references in 129 functions** and **318 in 176**.

Addendum 13ad mapped the STATIC loader `00236C30`, which fills 35 slots. **Neither of AG-1's slots is
one of them.** The busiest two entries in the registry have producers of their own, and they are not
alike.

### `02EBF138` — a table, loaded by the same helper from a different caller

Zero direct stores, exactly one `lea`:

```asm
00237FC0:  movsxd rdx, ecx          ; an id argument
           lea    rcx, [02EBF138]
           call   003845F0          ; the SAME relocating store the STATIC loader uses
           mov    rdx, [02EBF138]   ; read it straight back
           test   rdx, rdx / je ... ; and walk it
```

So `02EBF138` **does** hold an authored table with the relocated header — `003845F0` applies the same
`+0x0C` / `+0x10` fixup — but it is loaded **on demand with an id**, by a caller that immediately
iterates it, rather than distributed at startup with the other 33.

### `02EBF190` — not a table at all

Two direct stores. The initialising one:

```asm
00238A80:  call 002EF640            ; -> lea rax,[02164280] ; ret   (a 2-instruction accessor)
           add  rax, 0x4E68C
           mov  [02EBF190], rax
```

**`02EBF190` = `02164280 + 0x4E68C` = `021B290C`** — a **fixed interior address of a large
runtime-populated `.data` buffer**. Both the base and the target are in `.data` but **not
file-backed**: zero on disk, filled at run time. There is no file load, no `003845F0`, and no header
to relocate.

> **SO AG-5'S ANSWER HARDENS.** 13ad showed two slots holding plain dwords. This shows the
> second-most-referenced slot in the registry holds **a computed pointer into a static buffer**. The
> registry is a **heterogeneous pointer table** — startup-distributed tables, on-demand tables, plain
> dwords, and at least one fixed interior address — not 63 instances of one thing. **A question of
> the form "is the header uniform" has the answer "there is not one kind of entry to have a header".**

> **AND THIS IS PROVENANCE, NOT CONTENT.** AG-1 asks what they *hold*. What is established here is
> **where each pointer comes from**: one from an id-driven load through the shared fixup, one from a
> constant offset into a runtime buffer. **What the structure at `021B290C` actually is, and what
> `00237FC0` walks, are not established** — and 723 and 318 references are far too many to infer
> from a producer. The half that is answered is the half that was cheap.

**No metric moves.** `registry_explained` 63/63, before and after.

---

## Addendum 2026-09-13ah — AG-5 answered: the table header IS uniform, and 128 consumers prove it

Addenda 13ad, 13ag and this one close `AG-5` — *"whether the header is uniform across all 63 slots or
only the three read"*.

### The header, read whole from a second site

`00237FC0` loads `02EBF138` on demand and then walks it, and the walk is the complete contract:

```asm
mov   rdx, [02EBF138]
cmp   esi, [rdx + 4]         ; index < ROW COUNT at +0x04, bound-checked with jae
mov   ecx, [rdx + 0xC]       ; +0x0C = a handle
call  0020E600               ;   resolved to the row base
movzx ecx, word ptr [rdx+8]  ; +0x08 = ROW STRIDE, and it is a u16
imul  ecx, esi               ; base + stride x index = the row
```

That **independently confirms `J-A`** — `+0x04` is the row count, bound-checked with `jae` before
`+0x0C` is resolved — and adds two things J-A's answer did not state: **the stride at `+0x08` is a
`u16`**, and the reference at `+0x0C` is a **handle resolved through `0020E600`**, not a raw pointer.

### The idiom is not local to one slot

Every function referencing any registry slot — **355**, of which 351 were disassembled (bodies over
4,000 bytes skipped) — tested for the three header reads and the resolver call:

| what the function does | functions |
|---|---:|
| stride `+0x08` **and** handle `+0x0C` **and** `call 0020E600` | **128** |
| of those, **also** bound-checks against the count at `+0x04` | **38** |
| none of the idiom | 203 |
| partial shapes | 20 |

> **SO THE HEADER IS UNIFORM, AND THE ANSWER TO `AG-5` IS YES — FOR THE SLOTS THAT HOLD TABLES.**
> 128 consumers spread across the registry read the same three fields the same way and resolve
> through the same function. That is not three slots; it is the shape of the family.
>
> **The non-uniformity 13ad and 13ag found is of a different kind**: `02EBF180` and `02EBF200` hold
> plain dwords and `02EBF190` holds a computed interior pointer, so they have no header to be uniform
> about. **The registry is heterogeneous in what an entry IS; the entries that are tables share one
> header.** Those two statements were easy to confuse and are now separated.

### And 90 of the 128 never read the count

Only 38 of the 128 bound-check the index against `+0x04`. **This is exactly what `J-A` reported** —
*"nine consumers bound an index on it with `jae` … 43 more use it as a loop bound; the ~190 that
index without it carry their own bound, so safety is per consumer and checkable"* — reproduced here
by a different method over a different population, which is the strongest form of agreement available.

> **AND "90 DO NOT BOUND-CHECK" IS NOT "90 ARE UNSAFE".** The measurement is that they do not read
> the header's count. A consumer bounded by its own constant, by a caller-validated index, or by a
> loop over a separately known length is correct and would score the same way here. **Safety is per
> consumer, and this instrument cannot judge it** — it can only say which consumers the header's own
> bound is available to and unused by.

**No metric moves.** `registry_explained` 63/63, before and after.

---

## Addendum 2026-09-13ai — the fixup relocates four fields, not two, and the resolver was already known

Two corrections and one non-claim, from opening `0020E600` — the resolver 128 registry consumers
call on the table header's `+0x0C`.

### `0020E600` is already documented, and I checked before claiming

It is **ten bytes**: `mov eax, ecx / add rax, [01F83530] / ret` — a 32-bit offset promoted to a
pointer by one global base. **Five pages already describe it**, including the exact phrase *"the
offset resolves through `0020E600`"*. **There is nothing new to publish about it**, and I record that
rather than re-describing a known function as a finding. Reaching for the corpus first is the cheap
step this series keeps proving I should take.

### CORRECTION: the fixup relocates FOUR header fields, not two

Addenda **13ad** and **13ah** both say `003845F0` fixes up *"the base-relative fields at `+0x0C` and
`+0x10`"*. **It relocates four**, each with the same guarded form — read the field, skip it if zero,
add the table's own 32-bit base, store it back:

| relocated | `+0x0C` | `+0x10` | `+0x18` | `+0x1C` |
|---|---|---|---|---|

I had read the first two and generalised from them. The third and fourth are in the same routine, 30
bytes further on. **Two published addenda are corrected by this line**, and the authored-table header
is correspondingly larger than either of them implied.

**And the fixup resolves as well as relocates.** `003845F0` itself calls `0020E600` twice and
`0020E620` once while walking — so relocation and resolution are not two mechanisms meeting at the
header, they are one routine doing both.

### The open question this leaves, named rather than guessed

`003845F0` makes `+0x0C` absolute by **adding the table's own base**. `0020E600` then makes it a
pointer by **adding the global at `01F83530`**. Both operate on the same field, and **how they
compose is not established here.**

> The coherent reading is a single authored-data arena: fields are stored as 32-bit offsets, the
> fixup rebases them within the arena, and `01F83530` holds the arena's 64-bit base so the resolver
> can promote a 32-bit value to a real pointer. **That is a reading, not a measurement**, and it
> makes a testable prediction — `01F83530` should equal `table_ptr - low32(table_ptr)` for every
> table, identically. **Both the base and the tables are runtime-populated and zero on disk**, so
> that prediction cannot be checked statically, and I am not asserting the mechanism on the strength
> of its being the tidy explanation.

**No metric moves.**

---

## Addendum 2026-09-13aj — `0020E600` has an inverse, and their shared base has no writer

Chasing the composition question from 13ai down the cheap rungs before queuing it found two things
worth keeping.

**`0020E600` is half of a pair.** Its inverse sits 32 bytes away:

```asm
0020E600   mov eax, ecx / add rax, [01F83530] / ret     ; 32-bit value -> pointer
0020E620   sub ecx, [01F83530] / mov eax, ecx / ret     ; pointer -> 32-bit value
```

A bidirectional offset↔pointer converter around one global. `003845F0` calls **both** while walking
a table's header.

**And `01F83530` has no writer.** `data_xref_scan` over all 34,270 bodies finds **exactly two
references image-wide, and both are reads**. A raw displacement sweep of the entire `.text` finds the
same two and **zero sites outside any listed body**.

> **THAT ABSENCE CHANGES THE QUESTION RATHER THAN ANSWERING IT.** A base nothing writes may simply be
> **zero**, in which case both helpers are identity and survive as a symmetry from the PS2 original
> where offsets genuinely were arena-relative — and `003845F0`'s fixup, which adds the table's *own*
> base, already produces the final value. **That reading is simpler than the arena one I floated in
> 13ai, and the absence of a writer is evidence for it.** I am not adopting either.
>
> **The strong word is bounded:** *no writer* means no rip-relative store in `.text`, listed body or
> not. A value set by a relocation, an indexed write, or a `memcpy` over a containing struct would
> not appear.

> **RESOLVED — dated 2026-09-12 example, do not read as a current fact.** The answer arrived
> 2026-09-26 (FABLE, routed via `FABLE-REQ-FRONTIER-LEDGER-AND-STANDARD-01F83530-NOTES`):
> `01F83530` is **zero at image load** (past `.data`'s file-backed end `01F7E400`), and **one
> in-image store route does reach it** — the texture-id table writer `00210570`
> (`GiSetTexture` execute `00863040` → `00210570`) bounds its id only from above
> (`cmp cx,0x4000` / `jge`; `movsx`), so id `0xFFFB` stores a pointer **into** `01F83530` —
> replayed on the unmodified bytes
> (`02-Resource-And-Asset-Pipeline/members/image_address_base_writer_bounds.py`, R6: afterwards
> `0020E600` returns `x + pointer`). The id producers keep ids < `0x4000` at the shipped width
> `0x200`, so the route is **undriven, not absent**: *"no writer in the image"* was false as an
> image fact, and *"zero for the process life"* is supported, not proven, as a runtime claim.
> Canonical: `CONTRACT-authored-table-row-lookup.md` §7 reconciliation (`de52023ee`).

**Queued as `AQ-ARENA`**, with every cheaper rung shown as tried: existing evidence (five pages
describe the resolver, none states the base), static analysis (all three routines decoded),
call/data relationships (two references, both reads, no writer to follow), and isolated
original-code execution — which **cannot** help, because emulating the helpers reproduces arithmetic
already legible in the instructions and cannot supply the process's own value.

**The observation is one read of a qword, and it discriminates outright**: zero means identity,
non-zero means arena base and should equal `table_ptr - low32(table_ptr)` for every table.
**Fan-out 128** — every consumer reaching a row through the shared resolver. It needs no setup
beyond a loaded save, so it merges into any existing batch.

**No metric moves.**

---

## Addendum 2026-09-13ak — 144 magic-static initialisers, and this time the run WAS the family

The second-largest never-mentioned run, `005850F0`–`00597200`, holds 220 bodies — **144 of them
exactly 383 bytes**, and 212 tagged `Owner;Resource`. Opening one shows the MSVC **thread-safe local
static** idiom:

```asm
mov   ecx, [02EAED3C]        ; _tls_index
mov   rax, gs:[0x58]         ; the TEB's TLS array
mov   rdx, [rax + rcx*8]
lea   rdi, [02CAAFE8]        ; the static object
cmp   [02CAB018], eax        ; this static's guard epoch
call  008092FC               ; _Init_thread_header
```

### The form was derived, not guessed

The static-init family in 13ad was matched by **hand-masking** the byte ranges I judged to be
operands — which is a guess about instruction layout that can hide a field I failed to anticipate.
Here the skeleton is **derived from the members**: across the 144, **296 of the 383 byte positions
are identical** and the other **87 vary**. Those 87 *are* the operands, by measurement.

### And the run-versus-family check came out the other way

13ad's lesson was that the run is where I looked, not what the family is — there, the form found
**530** bodies against the run's 298. **Applied here, the census-wide search for the derived skeleton
finds exactly 144, all inside the run, none outside.** The check is only worth running because it can
come out either way, and this time it did.

| | |
|---|---|
| members | **144**, all 383 bytes, extent `005850F0`–`00592770` |
| shared call targets, **144/144 each** | `008092FC` (`_Init_thread_header`), `0080929C`, `00808B90` (the atexit wrapper), **`0067F700`** |
| disposition | **0 A-measured, 0 declared, 0 cited — 144 untouched frontier**, 55,152 bytes |

**`0067F700` is the provenance argument**, and it is already documented: `lazy-statics-and-the-one-time-init-lock.md`
covers it. 144 bodies calling one documented function is the same control the accepted families use
(*"all 298 call ONE target, `0063E2E0`"*) — adjacency is not doing any work here.

> **AND I HAVE DECLARED NOTHING, AGAIN.** The owning page declares no EC-7 family at all, so these
> are genuinely undeclared rather than a gap in someone's members file. Assembling the evidence is
> mine; ruling on evidence I assembled is not. Member list at
> `_index/candidates/magic-static-init-383.tsv`, with the shared targets, each member's guard and
> object addresses, and a header whose first line says it is not a declared family.

**No metric moves *by me*.** I declared nothing. The frontier read **19,909** when this work
started and **19,908** when it was written up — a peer's commit landed in between. Recorded
rather than quietly writing "before and after" over a figure I had not re-checked.

---

## Addendum 2026-09-13al — `00808B90` is the largest anchor in the frontier, and most of its mass was already routed

`00808B90` — the MSVC atexit wrapper — turned up as a shared call target in **two independent
families** found hours apart: the 32-byte dynamic-initialiser registrations (13ad) and the 383-byte
magic statics (13ak). Two families sharing one target is worth measuring rather than noting.

**1,614 bodies reference it**, over **2,630 sites** — 1,574 calls and 1,056 tail-jumps.

| disposition of those 1,614 | bodies |
|---|---:|
| already `A` | 6 |
| already declared B/C | 413 |
| cited only | 48 |
| **untouched frontier** | **1,147 — 313,638 bytes** |

**That is the largest single handle found on the frontier so far.** One function anchors 1,147
undeclared bodies, and its size histogram is not flat — 421 at 32 bytes, 260 at 53, 144 at 383 —
which is what a population of generated families looks like from outside.

### But most of that mass is work I routed today, and saying so is the point

| of the 1,147 untouched | bodies |
|---|---:|
| already in `static-init-form-530.tsv` | 360 |
| already in `magic-static-init-383.tsv` | 144 |
| **already routed by me today** | **504** |
| **not yet routed** | **643 — 246,966 bytes** |

> **PRESENTING 1,147 AS THE FINDING WOULD HAVE COUNTED MY OWN MORNING TWICE.** The anchor is real
> and the number is real, but 44% of it is already sitting in two candidate files with SWE2-EC7.
> This is the same double-counting shape addendum 13p found in the entry-only figure — a population
> measured one way and reported as though nothing else had touched it — and the fix is the same:
> intersect before publishing.

### What actually remains is a long tail, not a family

The 643 unrouted bodies cluster far more weakly than the two families did. Largest groups: **48** at
240 bytes, 38 at 815, 34 at 64, 30 at 12, 28 at 43, 22 at 91, 19 at 54, 17 at 184, 16 at 57.

**Nothing here is another 420-member block.** Whoever takes this should expect **several small
families rather than one**, and should derive each form from its own members — the method that
worked twice today — rather than assuming the shared anchor makes them one thing.

> **AND THE ANCHOR IS A PLACE TO LOOK, NOT PROVENANCE.** Sharing a registration helper says these
> bodies all register a destructor at exit. It does not say what they construct, and the accepted
> families each earned a shared-target control **of their own** on top of the form. A family
> declared from "calls `00808B90`" would be the same unsupported bulk disposition as one declared
> from adjacency, wearing a more technical hat.

Worklist at `_index/candidates/atexit-anchor-tail-643.tsv`, sorted by size with each body's
reference kind, and a header saying in its first line that it is not a declared family and not one
family.

**No metric moves.** Nothing is declared.

---

## Addendum 2026-09-13am — the tail's largest cluster is EASTL, and the code says so itself

The 643-body atexit tail (13al) clusters weakly, and I said whoever took it should expect several
small families and derive each form from its own members. Taking my own advice on the largest
cluster — 48 bodies at 240 bytes — produced the best-evidenced candidate of the four filed today.

| | |
|---|---|
| derived form | **178 of 240 byte positions identical**, 62 operands — derived, not hand-masked |
| census-wide | **52 bodies**, four more than the 48-body seed |
| shared target | **`001EDF00`, called exactly twice by every member** — 104 calls over 52 bodies |
| disposition | 0 A, 0 declared, 4 cited, **48 untouched**, 12,480 bytes |

**`001EDF00` is 14 bytes and already documented** on
`23-Third-Party-Libraries/EASTL/eastl-strings-containers-and-the-logging-allocator.md` — so the
owning page exists, in the directory where a "not this game's code" disposition belongs.

### The provenance is the strongest of the four

Every member opens the same way:

```asm
lea  rdx, [008F6600]      ; "EASTL basic_string"
lea  rcx, [rsp+0x30]
call 001EDF00
...
call 001EDF00
```

**All 52 reference a literal name string, and every one of them reads `"EASTL basic_string"`.**

> **THE CODE NAMES ITS OWN LIBRARY TYPE.** Compare what the other three candidates rest on: the
> static-init family on a form image plus a shared registrar; the magic statics on a form image plus
> `_Init_thread_header`; the atexit tail on nothing but a shared helper, which is why I refused to
> call it a family at all. **This one carries a string literal saying what it is.** That is the
> difference between inferring a library and reading its name out of the binary.

### One instrument caveat, because the numbers include it

The call-target scan treats any `0xE8` byte as a call opcode. Across a 240-byte body that
occasionally lands inside operand data: alongside the 104 real calls to `001EDF00` it reported three
"targets" of `4817BD77`, `5724F6A5` and `-72A20936`. **Those are not calls**; they are the scanner
reading data as an opcode, and they are recorded here rather than quietly dropped, because a reader
checking my working will see them.

**Filed as a candidate, not declared.** `_index/candidates/eastl-basic-string-init-52.tsv` carries
each member's name string and disposition state, and says in its first line that it is not a declared
family. Routed to SWE2-EC7 with the other three.

**No metric moves.** Nothing is declared.

---

## Addendum 2026-09-13an — the tail's second cluster calls an accepted family's own control

The 815-byte cluster of the atexit tail — 38 bodies in the worklist, **39 census-wide** — derives to
a form with **545 of 815 byte positions identical (67%)**, and carries two independent provenance
arguments.

**First, string literals again.** Every one of the 39 references **both `"m_count"` and `"m_els"`**.
They register a **two-member reflected type**, and the member names are in the code rather than
inferred.

**Second, and stronger: the shared targets are already an accepted family's control.** Ten targets
are called by all 39, and three of them —

> `006372A0`, `006373D0`, `00632D80`

— are exactly the addresses the accepted C family **`AbstractClassDescriptor base-aware
constructors`** names in its own note: *"CONTROL: six shared targets including `006372A0`, `006373D0`
and `00632D80`, each ×133."* **These 39 bodies call the same PhyreEngine class-descriptor
constructors that an already-declared family uses to prove itself.**

The rest of the shared set: `008092FC` (`_Init_thread_header`, ×4 per member), `0080929C`,
`00808B90` (atexit), `00630180` (×2 per member), `0063DC80`, `0063DF90`, `0063DFA0`.

| disposition | 1 A-measured, 0 declared, 0 cited, **38 untouched**, 31,785 bytes |
|---|---|

> **THIS IS THE SHAPE A FAMILY ARGUMENT SHOULD HAVE, AND IT IS WORTH NAMING.** Five candidates now
> sit with SWE2-EC7, and they are not equally evidenced — the difference matters more than the
> counts:
>
> | candidate | what it rests on |
> |---|---|
> | 530 static-init registrations | form image + a shared registrar |
> | 144 magic statics | form image + `_Init_thread_header` + one documented target |
> | 643 atexit tail | **a shared helper only — which is why I refused to call it a family** |
> | 52 EASTL | form + a string literal naming the type |
> | **39 two-member descriptors** | **form + string literals + targets that are another family's control** |
>
> **A candidate that reaches the same functions an accepted family reaches is being measured against
> a bar someone else already cleared.** That is the strongest kind of agreement available short of
> reading every body.

**Filed as a candidate, not declared**, at `_index/candidates/phyre-two-member-descriptor-39.tsv`.
I have now assembled five families and ruled on none of them.

**One caution I am keeping attached.** The call-target scan only counts a target when it lands on a
**real function entry** in the census — added after the EASTL pass reported three impossible targets
from `0xE8` bytes inside operand data. Every figure above survives that filter.

**No metric moves.** Nothing is declared.

---

## Addendum 2026-09-13ao — a declared family is 36 bodies short of its own form

Chasing the atexit tail's smallest cluster — 30 bodies of 12 bytes — found something better than a
sixth candidate. The form is as small as a form gets:

```asm
lea rcx, [a static]     ; 7 bytes
jmp <one target>        ; 5 bytes
```

**1,328 bodies in the census have exactly that shape**, and they partition cleanly by tail-jump
target. **They are also, overwhelmingly, already declared:**

| target | bodies | declared by ANY family | untouched | by |
|---|---:|---:|---:|---|
| `00633240` | 701 | **701** | 0 | `C PDataMemberMetadata static teardowns` |
| `006332A0` | 194 | **194** | 0 | the same family |
| `0016D6A0` | 185 | 149 | **36** | `C Control Flow Guard static-guard adapters` |
| `006B6750` | 70 | **70** | 0 | `C Phyre.Reflection.AnnotationStaticTeardown` |
| `005DDD60` | 60 | 0 | **60** | — nothing |
| `00808B90` | 31 | 1 | **30** | atexit; register-only, no construction |

**1,162 of 1,328 are already dispositioned.** Presenting "1,328 twelve-byte forwarders" as a finding
would have been 87% someone else's finished work — the check that stopped it is the same one that
stopped the 1,147 atexit figure two addenda ago.

### The finding is the 36 — and the cause is the selector, not the family

`Control Flow Guard static-guard adapters` declares **145 members** and its note gives the control:
*"PROVED BY FORM — 145 members, all 12 bytes, ONE byte image … CONTROL: exactly ONE external target,
`0016D6A0` ×145."*

**Re-running that stated control finds 185 bodies, not 145.** Measured against the declaration:

- **0 declared members fall outside the form**, so the form is not over-narrow and the comparison holds.
- 40 are not declared by it. **4 belong to `NativeAdapter.StaticAddressTailCall`** — a legitimate
  exclusion, since the gate refuses cross-family collisions.
- **36 are untouched frontier.**

Four discriminators were tried against the 36 and **all four failed to separate them**: the byte form
is identical; the tail-jump target is identical; the `lea` destination is in `.data` for all 145
declared and all 40 extras; and 37 of the 40 sit *inside* the declared address extent, so it is not a
selector run over a range either.

**The fifth one worked.** Every one of the 185 has its address taken by a `lea` in `.text` that
registers it with the MSVC `atexit` wrapper `00808B90` — but in **two different shapes**:

| | registered by `call` | registered by epilogue + tail-`jmp` |
|---|---:|---:|
| **declared** | **144** | 1 |
| **not declared** | 3 | **37** |

> **THE SELECTOR MISSED A REGISTRATION FORM; IT DID NOT MISJUDGE A BOUNDARY.** Both shapes reach the
> same wrapper and register the same kind of object — `add rsp,N ; jmp 00808B90` is the tail-call
> spelling of `call 00808B90`. There is no semantic difference between the two columns, so the gap is
> **mechanical**. This is precisely the staleness shape `check_dispositions` documents — *"almost
> always STALENESS, not a bad family … re-run its selector"* — with the selector's actual blind spot
> now named, which is what makes it fixable. The 4 off-diagonal cases are reported because they mean
> the correlation is 181/185, not 185/185: strong, and not total.

**THE FAMILY IS NOT WRONG ABOUT ANY BODY IT DECLARES.** All 145 are genuine atexit-registered
teardowns. What fails is **reproducibility**: a reader re-running the control as written gets 185.

### I nearly retracted this finding on a bad instrument, which is the part worth keeping

My first adjacency test accepted only `E8` (call) after the `lea`. It reported **0 of 36 registered**
against **144 of 145** — a clean discriminator that would have vindicated the family and made me
withdraw a true finding as a false alarm. The 36 were not unregistered; they used `E9`, and **my
instrument could not see a tail call.**

> **THE FAMILY'S SELECTOR AND MY CHECKER FAILED THE SAME WAY, INDEPENDENTLY, HOURS APART.** Every
> previous instrument error in this register *over*-counted, and the habit that catches those is
> distrusting a number that is too big. This one *under*-counted, and it was disguised as a
> discriminator — the most persuasive possible result, because it was the one I was hunting for. The
> check that caught it was reading the bytes the instrument had rejected (`48 83 C4 ..` is an
> epilogue, not a non-registration) rather than accepting the tidy 0-of-36.

### And the name is not supported by this image

- `DllCharacteristics` is **`0x8120`** — `IMAGE_DLLCHARACTERISTICS_GUARD_CF` (`0x4000`) is **clear**.
- The load-config `GuardCFFunctionTable` is **null, count 0**, and `GUARD_CF_FUNCTION_TABLE_PRESENT`
  (`0x400`) is clear in the guard flags.
- `0016D6A0` is **three bytes — `C2 00 00`, a bare `ret`.**

So every member does `lea rcx,[a static]` and returns. **Control Flow Guard is not enabled in this
binary and has no function table in it**, which leaves the name resting on nothing measurable. The
form, the `atexit` registration and the page's own subject all say what these actually are: **the
per-object teardown wrapper for a static whose destructor is empty**, its destructor folded to one
shared 3-byte `ret`.

**One dangling reference, recorded because a reader will chase it.** The family note ends *"NOT
dispositioned: `0016D6A0` — and see the note below, because what it IS matters here."* `0016D6A0`
occurs **exactly once** in that 121-line page — in that sentence. There is no note below, and the
Evidence table carries four rows, all four about the *other* family's target `00584730`.

**Nothing is declared and no metric moves.** The members file is SWE2-EC7's, the page is its owner's,
and a selector re-run is theirs to make.

---

## Addendum 2026-09-13ap — the tail-call spelling has one family, and it holds 35 of 141

Addendum 13ao found that the `Control Flow Guard static-guard adapters` selector matched
`call 00808B90` and missed `add rsp,N ; jmp 00808B90`. The obvious next question is whether that is
one family's slip or something wider, so I ran the same two-way split across the **whole** 12-byte
`lea rcx,[a static] ; jmp` population.

| | `call` | `jmp` | no `lea` site found |
|---|---:|---:|---:|
| **declared** | **1,133** | 20 | 8 |
| **not declared** | 3 | **121** | 43 |

**99.7% of `call`-registered bodies are declared. 14.2% of `jmp`-registered ones are.** A sevenfold
difference, and my first reading of it was that six selectors shared a bug.

### That reading was wrong, and the per-family split says so

| family | `call` | `jmp` |
|---|---:|---:|
| PDataMemberMetadata static teardowns | 853 | 0 |
| Control Flow Guard static-guard adapters | 144 | 1 |
| Phyre.Reflection.AnnotationStaticTeardown | 55 | 0 |
| Phyre.Reflection.PClassDataMemberStaticTeardownAdapter | 30 | 0 |
| Phyre.Reflection.ReflectionStaticTeardown | 28 | 0 |
| Phyre.Reflection.NamedDescriptorStaticTeardown | 15 | 0 |
| **NativeAdapter.StaticAddressTailCall** | 8 | **19** |

> **THERE IS NO SHARED BUG. THERE IS A DIVISION OF LABOUR WITH A HOLE IN IT.** Six families are
> `call`-spelled almost perfectly, and the seventh is *named for the other spelling* —
> `StaticAddressTail**Call**`. The tail-call bodies were never six selectors' business; they were one
> family's, and **that family declares 35 where 141 bodies use its spelling.** The population is not
> under-covered because a tool is broken; it is under-covered because **the one family scoped to it
> stopped early.**

**121 undeclared, in six clusters**, and 44 of them have a target that family *already covers*:

| target | undeclared | already in NativeAdapter |
|---|---:|---:|
| `005DDD60` | **60** | 0 |
| `0016D6A0` | **36** | 4 |
| `007DF700` | 11 | 0 |
| `001FEA00` | 6 | 0 |
| `00680030` | 6 | 1 |
| `006167C0` | 2 | 1 |

**44 of the 121 sit at a target the family has already accepted members from.** For those, no new
judgement is needed at all — its own declared control reaches them.

### This corrects the route I filed an hour ago

`OPUS-REQ-SWE2-EC7-CFG-GUARD-SELECTOR` asked for the **CFG** family's selector to be re-run over both
spellings, to pick up 36 bodies at `0016D6A0`. **That presumed the answer to a question I had not yet
asked.** `NativeAdapter.StaticAddressTailCall` already declares **4 bodies at that same target**, by
the tail-call spelling those 36 use. So the 36 have two plausible owners, and the two families'
definitions genuinely overlap:

- **CFG static-guard adapters** = form + the single target `0016D6A0` (145 members, one target)
- **NativeAdapter.StaticAddressTailCall** = form + the tail-call registration (35 members, 26 targets)

A body that is 12 bytes, jumps to `0016D6A0`, and registers by tail call **satisfies both**. Which
family takes it is a **boundary adjudication between two accepted families**, not a members-file
refresh — and it is not mine to make. The correction is filed to SWE2-EC7 alongside the original
route rather than replacing it, so the history stays readable.

**The largest cluster is nobody's under either definition.** `005DDD60` holds **60 bodies, 0
A-measured, 0 declared, 0 cited** — all 60 registered with `atexit`, all 60 by tail call, all 60 with
`.data` lea destinations. Unlike `0016D6A0`, its target is a **79-byte real function**, not a bare
`ret`, so these construct or destroy something rather than doing nothing.

**Nothing is declared and no metric moves.**

---

## Addendum 2026-09-13aq — a hex CONSTANT can be counted as a function citation, and the inflation is bounded at 53

Found sideways, while running pass 23's address check. One `Do not confuse with:` statement named
`` `0x04000000` `` and my checker flagged it as an address outside the image. It is not an address —
it is **bit 26**. The document says so in the same sentence.

That is my instrument's error and it cost nothing. **But the same shape reaches the scorer**, and
that does cost something, because `engine_explained` carries **weight 0.55** — the dominant term in
the whole completion figure.

`progress.py` counts a function as *explained* when a document contains a backticked token matching
`` `(?:0x)?(0[0-9A-Fa-f]{7})` `` that resolves inside its body. **A bit mask, a size, or a flag
constant has exactly that shape.**

### Measured, not asserted

| | |
|---|---:|
| distinct tokens that credit a function | 22,620 |
| distinct functions credited | 11,045 |
| tokens with ≤2 bits set | 7 |
| tokens with ≤4 bits set | 82 |
| **functions credited ONLY by a ≤4-bit token** | **53** |

**53 of 11,045 is the pessimistic ceiling — 0.48% — and it assumes every round-looking token is a
constant, which is false.** Reading the seven ≤2-bit tokens gives the real rate:

- `` `0x00400000` `` — *"4.00 MiB"*. **A size.** Credits 1 function, sole source for **0**, so it
  inflates nothing.
- `` `0x00800000` `` — *"`CryptDeriveKey` receives algorithm `0x6801` and flags `0x00800000`"*. **A
  crypto flag.** Sole source for **1 function**.
- `` `0x00480000` – `0x00500000` `` — a **region range** for the float-table builders. These are real
  `.text` addresses, so not constants; but crediting the two functions containing the *endpoints* of
  a range is a range claim being read as two citations.

> **CONFIRMED INFLATION: ONE FUNCTION IN 11,045.** Not an alarm, and deliberately not reported as
> one. It is recorded because *"do not inflate completion from citations"* is a standing rule, and a
> rule is only enforceable if someone has measured how far it is actually being broken. **The answer
> is: barely.** The scorer's own comments already record three corrections to this metric in both
> directions; this is a fourth, in the inflating direction, and the smallest of them.

**No change is being made to `progress.py`.** A filter that dropped low-bit tokens would throw away
genuine citations of functions at round addresses — `00480000` is a real one — to recover a single
function. **The cure would cost more than the disease**, and the honest fix is this note: a token
that resolves inside a body is *evidence of a citation*, not proof of one, and the 0.55-weight
metric carries a known contamination of about one function.

---

## Addendum 2026-09-13ar — `02CBF998` is the named render-pass registry, and all 60 of its teardowns now have names

The largest wholly-undeclared cluster in the 12-byte forwarder population — **60 bodies, 0
A-measured, 0 declared, 0 cited** — is no longer anonymous. Its shared tail-jump target was read
instead of counted, and it led to a global that `UNEXPLAINED-GLOBALS.md` ranks **8th of the forty
hottest** — *1 writer, 63 readers, 58 address-taken, explained by nothing.*

### Both sides of the contract, read from the bytes

`02CBF998` is the head of a **singly linked, name-keyed intrusive registry**.

```
node   +0x00   const char *name
       +0x08   node *next
```

**`005FDCB0` — register, 132 bytes.** Loads `name = [rcx]`; if null returns **`0x11`**. Walks from
the head running an **inline byte-by-byte `strcmp`** against each node's name; on a match returns
**`0x12`** — a duplicate-name refusal. Otherwise pushes on the **front** (`[rcx+8] = head`,
`head = rcx`) and returns **0**.

**`005DDD60` — unregister, 79 bytes.** Walks from the head comparing the *address* of each node's
`next` field against `rcx+8`, writes the successor through the previous slot, and **nulls the
removed node's `next`**.

**The 60 wrappers.** Each is 12 bytes — `lea rcx,[its own node] ; jmp 005DDD60` — and every one is
registered with the MSVC `atexit` wrapper `00808B90` **by the tail-call spelling**, which is why
13ap found them undeclared: they are in the blind spot the one tail-call-scoped family left.

> **A SHARED ANCHOR IS A PLACE TO LOOK; A DECODED TARGET IS PROVENANCE.** 13ap could say only that
> these 60 tail-jump the same address. Reading that address gives a struct layout, an ABI with three
> documented return codes, and the reason the objects exist.

### What they are, and how the names were recovered

**PhyreEngine render passes and post-process effects.** `ShadowRender`, `ShadowRenderWithRef`,
`OpaqueDepth`, `OpaqueGray`, `AlphaModeRender`, `NearFadeRender`, `VideoScreen`, `RenderFXAA`,
`RenderScreenSpaceReflection`, `RenderDoFComposite` / `Horizontal` / `Vertical`,
`RenderGaussianBlurX` / `Y` / `YComposite` / `YCompositeCombine`, `RenderCameraMotionBlur`,
`RenderPointLight` / `SpotLight` / `DirectionalLight`, `PrecomputeTransmittance` /
`SingleScattering` / `MultipleScattering` / `SingleIrradiance` / `MultipleIrradiance` /
`Radiance`, `RenderAtmosphere`, `Cel` / `CelInverted`, `AddToInscatter`, `CopyIrradiance`,
`RenderText_AlphaBlend` / `AlphaTest` / `HardEdges` / `SoftEdges` / `SoftEdgesAndGlow` /
`AndOutline` / `AndShadow`, and more — **60 of 60 named, with no gaps.**

> **THE NAMES ARE NOT IN THE FILE, AND THE FIRST ATTEMPT TO READ THEM CRASHED.** The nodes sit past
> the **raw end of `.data`** — the uninitialised tail — so `name` is written at run time by each
> static's constructor and `node+0x00` reads nothing out of the image. The crash was the honest
> failure; a checker that had silently returned zero names would have been worse. They are recovered
> instead from the **registration sites**: the function that takes a node's address also `lea`s the
> literal it registers under. **Control: a site is used only if it names exactly one node** — a
> function touching several cannot say which name is whose. 60 sites, 60 nodes, 60 names.

### What this is worth, stated without inflation

**No metric moves and nothing is declared.** The 60 remain undeclared frontier; what changed is that
they are no longer unidentified. Evidence in
`_index/candidates/render-pass-registry-teardowns-60.tsv`, reproducible via
`gfz-scripts/probe_render_pass_registry.py`.

**And one ranked unexplained global has an explanation** — which is not the same as being
dispositioned, and is not being counted as if it were. `UNEXPLAINED-GLOBALS.md` is generated; the row
will change when someone regenerates it against a document that cites `02CBF998`. **Writing that
document is not mine** — this is Presentation/PhyreEngine territory, and the post-process page
already exists.

---

## Addendum 2026-09-13as — four of "the 40 hottest globals nothing explains" are named Windows imports

`UNEXPLAINED-GLOBALS.md` ranks the frontier of unexplained global state, and its ranking is a
prioritisation: *"Ranked by total referencing functions. A global with many writers across many
owners is shared mutable state — the most expensive kind to discover late in a reconstruction."*

Having closed rank 8 (13ar), I checked what the rest of the top of that list actually is. **Seven of
the forty rows are not unexplained state.**

### Four are import-table entries, and they have names

Resolved from the PE **import directory** and the IAT data directory (`008C2000..008C31C0`):

| rank | global | it is | readers |
|---:|---|---|---:|
| 3 | `008C2A40` | **`VCRUNTIME140.dll!memmove`** | 169 |
| 5 | `008C20C0` | **`KERNEL32.dll!LeaveCriticalSection`** | 136 |
| 6 | `008C20B8` | **`KERNEL32.dll!EnterCriticalSection`** | 134 |
| 38 | `008C2DA8` | **`api-ms-win-crt-runtime-l1-1-0.dll!_invalid_parameter_noinfo_noreturn`** | 79 |

> **THEIR `0` WRITERS IS NOT A MYSTERY — THE LOADER WRITES THEM.** These are not game state that
> nothing explains; they are **named external functions**, fully resolvable from the PE headers, and
> a reconstruction does not have to discover them at all. `memmove` sitting at **rank 3** of the
> frontier's priority list is the ranking measuring reference popularity and calling it
> unexplainedness.

`globals_index.py` already discards 1,968 rows as *"EH funclet referrer, banned evidence"*, so the
mechanism for excluding a known class exists; **IAT entries are the same kind of exclusion and are
not being made.** The index is generated — the fix belongs in the generator, not in the file.

### Two more are one object, counted twice

**Rank 1 `01F2CDB8` and rank 4 `01F2CDA0` are the same static container.** `01F2CDB8` is exactly
`01F2CDA0 + 0x18`, and the qword stored there **is `01F2CDA0`** — a sentinel node whose root field
points back at itself, which is how an empty tree is initialised. The 144 magic-static initialisers
at `005850F0` stride `0x180` open with

```asm
lea rbx, [01F2CDA0]          ; the sentinel
mov [02CAAFE8], rbx
mov [02CAAFF0], rbx
mov rcx, [01F2CDB8]          ; the root
lea r10, [01F2CDB8]
cmp rcx, rbx                 ; empty?
```

so rank 1's 145 readers and rank 4's 147 address-takings are **one container being touched by one
already-identified family** — the 144-member magic-static candidate already routed to SWE2-EC7.

### What this is and is not

**It is not a claim that the index is wrong.** Every row is a real global with a real reference
count, and the header's own blind-spot callout is exemplary. What is wrong is the *reading* the
ranking invites: **seven of the top forty rows are a named import, a duplicate of another row, or
already explained**, and three of the top six are `memmove` and two critical-section calls.

**It is not a licence to inflate.** Nothing is dispositioned here and no metric moves. Four imports
being named does not explain four globals of FFXII state — **it removes four rows that were never
FFXII state**, which is a smaller and more honest claim.

**And the `0` in the writers column stays dangerous.** The index's own header records a CONTRACT that
quoted a `0` as *"never written, NULL for the life of the process"* and was wrong, because the scan
is RIP-relative and blind to stores through a walking pointer. That applies to ranks 1 and 4 exactly:
**the sentinel's fields are written constantly — through `rcx`, after a `lea`.**

---

## Addendum 2026-09-13at — the frontier's forty hottest globals are five, and this corrects 13as

13as reported that **seven** of the forty rows in `UNEXPLAINED-GLOBALS.md` are not unexplained state.
**That was measured against the published file, which is stale, and the real figure is worse.**
Regenerating with the file's own generator — which its header instructs (*"Regenerate it; do not quote
these numbers from memory"*) — moves the corpus-wide totals:

| | published | regenerated |
|---|---:|---:|
| cited by at least one system document | 2,145 | **2,363** |
| explained by nothing | 33,687 | **33,469** |

**218 globals have been cited since that file was written.** So every figure in 13as was taken from a
snapshot, and the classification below is against a fresh one.

### The fresh top forty, classified

| what it actually is | rows |
|---|---:|
| **VU1 microprogram working-register file, documented as a range** | **28** |
| named IAT import | 4 |
| one container sentinel, counted twice | 2 |
| the render-pass registry (13ar, explained today) | 1 |
| **genuinely open** | **5** |

> **THIRTY-FIVE OF FORTY ROWS ARE NOT UNEXPLAINED FFXII STATE.** A prioritisation list whose stated
> purpose is *"shared mutable state — the most expensive kind to discover late in a reconstruction"*
> is **87% artifact**, and a reader working it top-down spends their first twenty-eight rows inside a
> register file somebody already documented.

### The 28 are the same error this register has hit all day

`the-vif1-vu1-layer.md` §2.2 documents `02064B00`–`02064E30` as *"microprogram working registers:
16-bit words used as cell indices … and float scratch"*, and names `02064B0C`, `02064DB0`,
`02064DB4`, `02064DB8`, `02064DD0` explicitly.

**204 dword slots in that range. 9 cited verbatim. 28 of the fresh top forty are slots inside it.**

> **THE PAGE DOCUMENTS A RANGE; THE GENERATOR CREDITS AN ADDRESS.** Neither is wrong on its own terms
> — citing 204 individual dwords of a register file would be absurd, and a generator cannot guess
> that a range in prose covers an address. **The instrument measures the structure it parses, not the
> structure the content lives in** — for the fourth time in one run, now in the index that decides
> what gets worked next.

### What actually remains, which is the useful part

| rank | global | writers | readers | owners of writers |
|---:|---|---:|---:|---|
| 2 | `01F3BA68` | 1 | 169 | (none)×1 |
| 11 | `022D91A8` | 61 | 44 | (none)×30, **Presentation**×26, **Audio**×4 |
| 15 | `00900360` | 0 | 95 | — |
| 22 | `02AEE900` | 52 | 33 | **Presentation**×51 |
| 33 | `022D8FB0` | 38 | 39 | (none)×20, **Presentation**×18 |

**That is the real head of the frontier**, and three of the five already name an owner. `022D91A8`
with 61 writers across Presentation and Audio is the one the index's own sentence is describing.

### Stated without inflation

**Nothing is dispositioned and no metric moves.** Not one of the 35 becomes "explained" because I
classified it — 28 were already documented, 4 were never FFXII state, 2 were always one object, and
1 was explained an hour ago. **The frontier did not shrink; the list was never measuring it.**

**The fix is the generator's**, not the file's: exclude IAT entries, and either credit a documented
range or report range-covered addresses in a separate bucket. **Regenerating alone is not enough** —
it fixes the 218, and leaves all 28.

---

## Addendum 2026-09-13au — none of the forty is an isolated global, and this corrects 13at as 13at corrected 13as

Three figures for the same question in one evening, each from a wider measurement:

| | claim | measured against |
|---|---|---|
| 13as | **7** of 40 rows are not unexplained state | the **published** index — stale |
| 13at | **35** of 40 — five genuinely open | a **regenerated** index |
| **13au** | **none of the 40 is an isolated global** | regenerated, plus **proximity to any cited address** |

### The measurement 13at should have made

13at classified rows by recognising them — imports, a sentinel, a register file I happened to know
was documented. **Recognition does not scale and it missed things.** The general form of the question
is: *is any address near this one cited by some document?*

| | rows |
|---:|---|
| a cited address **within ±0x40** | **22** |
| a cited address within ±0x400 | 17 |
| **nothing within ±0x400** | **1** |

**The one is `02CBF998` — the render-pass registry explained in 13ar today**, which no document cites
yet because I routed it rather than writing someone else's page.

And the five 13at called *"genuinely open"* are not isolated either:

| global | nearest cited | Δ | the document |
|---|---|---:|---|
| `022D91A8` | `022D91A4` | **−4** | `CONTRACT-transform-primitives.md` |
| `022D8FB0` | `022D8FA0` | −16 | the workbench save/restore page |
| `00900360` | `00900370` | +16 | `object-construction-destruction-and-static-lifetime.md` |
| `02AEE900` | `02AEE910` | +16 | `effect-element-type-dispatch.md` |
| `01F3BA68` | `01F3BA80` | +24 | `the-post-processing-effect-catalogue.md` |

**A Δ of −4 is the adjacent dword.** And `022D91A8` / `022D8FB0` both sit inside
`022D8F00`–`022D9500`, which `the-shared-transform-workbench.md` §2 names outright: *"The area is
`022D8F00`–`022D9500` in `.data`."*

### What this does and does not license

> **PROXIMITY IS NOT EXPLANATION, AND THIS IS NOT A CLAIM THAT FORTY GLOBALS ARE EXPLAINED.** A cited
> neighbour means the **structure** is described, not that this dword's role is known. Nobody has
> said what `022D91A8` holds.

What it does establish is what the index **cannot** do:

> **`explained by nothing` IS AN ADDRESS-LEVEL PREDICATE APPLIED TO STRUCTURE-LEVEL DOCUMENTATION.**
> It cannot distinguish *"nobody has looked at this region"* from *"this region is documented and not
> enumerated dword by dword"* — and a register file, a transform workbench and an effect catalogue
> are all documented the second way, because the first way would be absurd. **So the ranking cannot
> currently find an undocumented region, which is the one thing it exists to do.**

**Nothing is dispositioned and no metric moves.** 33,469 globals remain uncited at address level and
that number is unchanged by any of this. What changed is that **the top forty are not the frontier's
head**, and work should not be prioritised from them until the generator can express range coverage.

**Folded into `OPUS-REQ-GLOBALS-INDEX-IAT`:** exclude IAT entries, and report a
**range-covered** bucket — an address whose neighbours are cited is a different thing from one
standing alone, and only the second kind is a frontier.

**Correction history preserved deliberately.** 13as was measured on a stale file, 13at on a fresh one
by recognition, 13au by a general test. **Each was published, each was wrong, and each was narrowed
by widening the measurement rather than by arguing.**

---

## Addendum 2026-09-13av — `audit_coverage` falls when a producer is working, and that is not a regression

`audit_coverage` moved **99.15% → 97.21%** in one evening. The numerator did not move at all:

```
351 documents, 348 audited   ->   358 documents, 348 audited
```

**Seven documents were added and none of them was audited yet.** All ten currently unaudited pages
are `PARTIAL`, nine of them under `16-UI` and one under `19-Save-Load-Settings` — the gambit, shop,
handbook, quest-list, map, licence-board, atlas, shared-dialog, unlabelled-pane and save/load screen
sheets. They are the live output of `FABLE-REQ-SWE2-FRONTIER-MENU-SCREENS`, which is **ACTIVE**.

> **A RATIO WITH A GROWING DENOMINATOR FALLS WHILE THE WORK IS GOING WELL.** A producer writing seven
> new sheets in an evening drives `audit_coverage` **down** by exactly the amount that the work was
> productive, and it recovers only when an auditor stamps them. Reading the drop as a quality
> regression would be precisely backwards — and reading it as *progress* would be the same error in
> the other direction, since nothing has been verified yet.

**The metric is honest; only a careless reading of it is not.** Six of the ten have no `audit:` block
at all and four have one that is present but **not stamped** — no `last_pass_state` — which the
scorer correctly refuses to count, for the reason its own comment records: a bumped counter is an
amendment, not an attack.

**Nothing to do here, deliberately.** The pages are occupied by an ACTIVE claim; the correct response
to a falling `audit_coverage` during production is to leave the producer alone and let the auditor
follow. This is recorded so the next reader of the number does not act on it.

---

## Addendum 2026-09-13aw — "no consumer found" is usually an indirection, and there are only four of them

Three open questions in one evening rested on the same shape: a rip-relative census of a global
reported a producer and nothing else, and the page concluded that no consumer had been located.
**All three times the consumers existed in quantity.** The census was right every time; the
inference from it was wrong every time.

| global | what the census saw | what was actually there |
|---|---|---|
| `02EAF930` | 1 reference — the appender's own `lea` | consumers hold a **handle to the entry**, encoded by `0020E620` and stored in the object's `+4`; they resolve it with `0020E600` and never touch the base |
| `01F7F5E0` / `01F7F5E8` | a setter and a getter | **56 and 46 functions** call the getters (`0018B4E0`, 33 B; `0018CA40`, **8 B**) |
| `02EBF198` | nothing at all | the array base is passed to `003845F0` with a **data-driven index**, so any slot is reachable unnamed |

> **A GLOBAL CENSUS MEASURES WHO NAMES AN ADDRESS, NOT WHO USES THE STATE.** Every indirection in
> this engine defeats it, and the engine is full of them. **"No consumer was located" should never be
> written as a finding without first asking which of these four it is.**

### The four, in the order they cost least to check

1. **An accessor.** Does a tiny function — 8 to 40 bytes — load the global and return it? Then count
   *its* callers. This is the cheapest check and it was the answer twice.
2. **A handle or id.** Does the producer hand something back that a consumer keeps? `02EAF930`'s
   appender `lea`s the **entry's own address**, compresses it against `01F83530` and stores the
   result in the object — so the consumer holds a pointer to the row and needs no base.
3. **A base plus a computed index.** Is the *array* base address taken and passed somewhere with an
   index? Then no individual element is ever named, and per-element absence proves nothing about
   per-element use.
4. **A member offset.** Is the global inside a struct that something else holds a pointer to? Then
   accesses are `[reg + disp]` and no rip operand exists at all.

### And the same discipline in reverse

**Absence still has to be measured before it is explained.** `02EBF198` survived a
**listing-independent** sweep — every byte of `.text` checked for a `disp32` resolving to it, with
two controls (a sibling slot at **318** candidates proving the sweep sees, and slot 46 at **exactly
2** proving it agrees with the body scan it is checking). Only after that is a zero worth writing
down, and even then it licenses *"no instruction names it"* and **not** *"nothing writes it"* —
because indirection 3 is live on that very array.

> **THE ONE-LINE RULE.** A census that reports *"producer, and nothing else"* has almost certainly
> found **an interface**, not an orphan. Look for the accessor first; it is eight bytes and it is
> usually right there.

---

## Addendum 2026-09-13ax — stale checkboxes are real, and address co-occurrence does not find them

Two open questions were closed today because **the corpus had already answered them and never
ticked the box**: AG-4, where the page called three slots unreferenced while its own AG-11 answer
said the main loop publishes one of them, and AG-1 — *"the highest-value unread data in the
database"* — which the same page answers in two dedicated sections.

That looked mechanisable. It is not, and the negative is worth recording so the checker does not get
built twice.

### The obvious heuristic, and why it fails

*For every open checkbox naming an address, does the same document resolve that address in a heading
or a line marked ✅ / ANSWERED?* Eight candidates. **Every one read so far is a false positive:**

- **Y-6**, *"the body of `001CA600`"* — the page does mark `001CA600` ✅, but for *"key-binding
  pattern read"*. The ✅ covers a pattern inside an **8,186-byte** function; the question asks for the
  body. **A narrower answer resolving the same address is not the answer.**
- **`0046A690`**, *"what sound id bank 7 resolves to, and whether it is a second presentation
  hook"* — §11 corrects **when** it runs and establishes it has one caller image-wide, and that
  correction is already quoted inside the checkbox. **Neither clause of the question is answered.**

> **THE HEURISTIC MEASURES ADDRESS CO-OCCURRENCE AND THE QUESTION IS ABOUT SEMANTICS.** Two
> statements about one address are not the same statement, and a compound question is not closed by
> answering one clause — the same distinction that kept KE-1 and `-13-7` open today.

### What actually found them

**Re-measuring the claim from the binary, then discovering the page already knew.** AG-4 fell out of
counting all 63 slots; AG-1 fell out of tracing the two slots' writers. In both cases the *page*
supplied the answer and the *binary* supplied the reason to go looking. **No text-level check would
have started either search.**

> **SO PASS 28 STILL HAS NO INSTRUMENT, AND THIS IS WHY.** `check_doc_self` compares a document to
> its own **structure** and passes cleanly on both pages. Detecting *"section A answers what
> section B still asks"* requires reading what both say — and a checker that guesses from shared
> addresses will spend an auditor's attention on eight false positives to find nothing.
> **Better to know the phenomenon exists and re-measure, than to trust a cheap proxy for it.**

---

## Addendum 2026-09-13ay — I published a re-derivation as a correction, and 13ax under-rated the cost

**Correcting `51dc91b4`, published minutes ago.** It carried *"class 13 reads FOUR slots, not three"*
as though it corrected the registry page. **It did not.** That page already holds a dedicated section,
`### 0x02EBF078 — the fourth table summed into encoded-id class 13's bound`, which names the function
(`BattleEncodedId_IsValidForClass`), lists all four slots with the **same instruction table** I
printed, states the null-guard, and **routes the disagreement with the class registry as
`OPUS-CONTRA-CLASS13-FOURTH-TABLE`.** The page found it first and had already escalated it.

**What I actually did was answer a stale checkbox by re-deriving its answer from the binary.** The
bullet still said *"three slots"*; the section above it said four. I read the bullet, went to the
bytes, and never checked whether a later section had superseded it.

### This is the fourth stale checkbox today, and the second one I paid for twice

| | the checkbox said | the page already said | how I found it |
|---|---|---|---|
| AG-4 | three slots unreferenced | AG-11: *"`02EBF178` is published by the main loop"* | re-measured, then noticed |
| AG-1 | *"the highest-value unread data"* | two dedicated sections, both ✅ | re-measured, then noticed |
| class 13 | three slots | §`0x02EBF078`: four, with a routed contradiction | **re-derived in full before noticing** |

**13ax concluded that stale checkboxes cannot be found by address co-occurrence and must be found by
re-measuring. That is still true, and it understated the cost.** Re-measuring finds them *after* the
work is done. Twice today that was cheap — the measurement was the point anyway — and once it was
pure duplication.

> **THE CHEAP GUARD I SHOULD HAVE RUN, AND NOW WILL.** Before answering any open checkbox: **grep
> the page for every address the checkbox names.** AG-1, AG-4 and class 13 would each have surfaced
> a later section in one command. That is not a checker and does not belong in the protocol — it is
> a habit, and it costs one grep against a re-derivation that cost an hour's equivalent of reading.

**The substantive content of `51dc91b4` stands** — the five killer tests, `00309440`'s bias table,
and the class-13 arithmetic are all correctly measured. **Only the novelty claim was wrong**, and it
is withdrawn on the page as well as here. `questions_closed` keeps the point: the checkbox genuinely
was open and is now genuinely closed, by whoever's reading.

---

## Addendum 2026-09-13az — the stale-checkbox check works when it matches on the QUESTION ID, not on an address

**This extends 13ax and partly overturns its conclusion.** 13ax reported that stale checkboxes
"cannot be found by address co-occurrence" and must be found by re-measuring. **The first half
stands; the second was too pessimistic.** Matching on the **question's own identifier** works, and
it is cheap.

### The signal that failed, and the one that works

| | rule | result |
|---|---|---|
| 13ax | an open checkbox names an address that a heading or ✅ line also names | **8 candidates, every one read a false positive** |
| **13az** | an open checkbox names a **question ID** that a non-checkbox line elsewhere calls *answered* | **1 real hit in 8 candidates** |

**MEASURED BEFORE BEING BELIEVED, and the first wording of this addendum said "hits are real",
which was too strong.** Eight candidates were read:

- **`AG-5` — real.** Its own page carries a section headed *"AG-5 answered: NO"*.
- **`AN-1` — false.** The register marks it **PARTLY ANSWERED**: what `FUN_003BA2E0` tests is
  settled, while the checkbox tracks what the two bytes *represent*. The page even says
  *"not re-opened here"*. **A partial answer matched the word and not the question.**
- **`AC-6` — false.** The register marks it plainly `OPEN`; the match came from a mention beside
  other answered items on a third page.
- **`AT-8` — ambiguous, left for its owner.** The register says *"THE FILE IS IDENTIFIED"* and names
  `action_data.bin`, which answers much of *"what the action space contains"* but not obviously all
  of it. **Not ticked by me.**

So the ID rule is **better than the address rule and not good**: 1 in 8 against 0 in 8. It is a way
to *generate candidates worth reading*, never a verdict.

**Why the second discriminates and the first does not.** An address appears in a page for a dozen
reasons, and *"`001CA600` ✅ key-binding pattern read"* resolves the address without answering
*"the body of `001CA600`"*. A **question ID** is written down in exactly two circumstances: to pose
the question, or to settle it. *"`AG-5` answered: NO"* cannot mean anything else.

### What it found immediately

**`AG-5`, on a page whose §8b is literally headed *"AG-1 answered, and AG-5 answered NO"***, with a
dedicated section two below the bullet giving the whole answer — that `0x02EBF190`'s `+0x04` is a
bitfield, so the header convention is not uniform and the registry is a global pointer array rather
than an authored-table array. **It had been sitting there since 2026-09-02.**

> **THAT IS THE THIRD STALE CHECKBOX ON ONE PAGE** — AG-1, AG-4 and now AG-5 — and the page's own
> section heading announces two of them. The drift is not between a page and the binary; it is
> between a page's **question list** and its **body**, and nothing in the corpus compares those two.

### Today's tally, and what it costs

**Seven stale checkboxes found:** AG-4, AG-1, class 13, BQ-16, BQ-19, AG-5 — and the class-13 one
**cost a full re-derivation** because I checked the bullet and not the page. Of the seven, **three
were caught before any work** (grep-first, 13ay) and **one after the work was wasted**.

**This still does not belong in the protocol as a checker.** The ID rule needs a human to confirm
that *"answered"* refers to the same question rather than a sibling clause — AG-4's bullet names a
premise that was corrected while its real survivor stays open, and a checker would have ticked it.
**It belongs in the habit**: before answering a checkbox, grep the page for its address **and its
question ID**. Two commands, and today they were worth more than any instrument I built.

---

## Addendum 2026-09-13ba — the open-question frontier mapped, and ASTRA is not what is blocking it

**706 open per-document questions**, classified by what it would take to answer them:

| class | count | share |
|---|---:|---:|
| names an address, **structural** — statically attackable | **180** | 25% |
| long prose, no anchor | 133 | 19% |
| a **"whether"** question — a yes/no claim to test | 75 | 11% |
| names a **field offset** (`+0x..`) — anchored to a struct | 72 | 10% |
| mentions runtime | 71 | 10% |
| asks meaning, no address | 56 | 8% |
| short, no anchor | 45 | 6% |
| names a hex token (id / mask) | 40 | 6% |
| address **plus** meaning — needs a consumer | 26 | 4% |
| names a file or format | 8 | 1% |

**Roughly 327 of 706 — 46% — are attackable statically today** (address-structural, field-offset, and
"whether" claims together).

### The finding that matters: ASTRA's absence is not the constraint

My first pass called the 71 runtime-flavoured questions the ASTRA backlog. **That was wrong and I
caught it before publishing.** Testing which of them actually claim a static route is exhausted:

> **7 of 71** — and the first count of this was **4**, because my pattern matched *"never observed"*
> and not *"not observed"*. **Corrected before publication, not after.**

Most read like *"Any runtime observation. None exists"* — **evidence-tier disclaimers rather than
questions that require runtime.** One is genuinely runtime-gated: `EX-9` asks whether ordinary
initialize/unload callbacks change the manager request mask mid-pass, and the native effects of
`0026CE60` and `002628B0` on a live area change **are not observed**. Its *other* half — enumerating
the writers — **FABLE answered today**, which grep-first surfaced before I re-ran the census.

The other **64 merely use a runtime word**. Two from the sample are directly attackable by methods
used earlier today:

- *"Which writers set the manager request mask `02099ABC`…"* — **a writer census with an
  address-taken control**, exactly the shape run on `02B62DB9` and `02EBF198`.
- *"The seven ids with no start site (1, 3, 8, 9, 14, 20, 21) — reached by a route the raw `E8`/`E9`
  index does not see, or unused"* — **EE-12's four-route reachability test verbatim**: direct call,
  64-bit pointer, 32-bit RVA table, `lea`, each with a control.

> **SO THE SIX-DAY ASTRA OUTAGE HAS NOT BLOCKED THIS FRONTIER, AND THE NUMBER SAYS SO.** The standing
> instruction is to mark only the affected claim boundary and advance another lane; **the affected
> boundary among open per-document questions is seven entries, most of them disclaimers.** A reader
> who assumed the runtime lane was holding up 10% of the frontier would have been wrong by a factor
> of ten.

### What the map does not say

**"Statically attackable" is not "cheap".** The 180 include bodies of 2,000+ bytes. And the **133
long-prose and 45 short unanchored** entries — 25% together — are not classified at all: they need
their own page's context to even judge, which is a limit of a corpus-wide sweep rather than a
property of the questions. **This is a map of tractability, not of value**; nothing here says the
statically attackable ones are the ones worth doing first.

---

## Addendum 2026-09-13bb — a function documented twice, on two pages, and no checker can see it

The eight stale checkboxes found today were all one shape: **a question answered elsewhere in its own
page's body**. `002ABB20` is the ninth and a different shape, and the difference is the point.

`ui-request-router.md` asked *"What `002ABB20` (918 B) does"*.
`99-Unresolved-Residual/measuring-text-by-drawing-it-with-the-output-off.md` §3–§4 had read it in
full — it scrolls a text window by the step at `+0xA0` and snaps to a line boundary, measuring with a
**borrowed stop-set** it saves and restores at both call sites. But the duplication is larger than
the one function:

| | `ui-request-router.md` | `measuring-text-…-off.md` §5 |
|---|---|---|
| what it calls `002ABF70` | *"an eight-mode jump table"* | *"the animation stepper"* |
| the dispatch | `+0xB0` **whole dword**, then `cl` | `state[+0xB0] & 0xFF` |
| the modes | 8 modes, **6 distinct bodies**, mode 6 a no-op | states **0–5 and 7** |
| the field table | `+0x5A .. +0xB0`, twelve rows | `+0x88 .. +0xA0`, seven rows |
| `+0x8C` | *"the target value, clamped to `0x7D00` = 32,000"* | *"the target line, **clamped at 32000**"* |
| `+0x5A` | *"a countdown"* | *"the brightness"* |

**Two pages, one 577-byte function, one state block, row for row — and neither cites the other.**

### Each held the half the other needed

Not a redundancy to delete. The router page has the **flag bit 22**, the constant `0x7D00`, and the
no-op mode. The measuring page has **what the object is** — a scrolling text window — and therefore
what the fields *mean*: `+0x8C` is a target **line**, `+0x90`/`+0x92` a pair **trailing** it. The
router page's own open question *"what mode 2 **is**"* was answered on the other page the whole time:
state 2 decrements `+0x5A`, `+0x5A` is the brightness that
[the rectangle primitive](../99-Unresolved-Residual/drawing-one-coloured-rectangle.md),
[the blinking icon](../99-Unresolved-Residual/the-blinking-icon-and-its-atlas.md) and
[the widget-tree draw pass](../99-Unresolved-Residual/the-widget-tree-draw-pass.md) multiply colours
by, so **mode 2 is a fade-out**. One page's "countdown" is three other pages' brightness.

### The checker gap, stated exactly

> **`check_consistency` PASSES ON BOTH, AND ALWAYS WOULD.** It compares **stated names and sizes** —
> *"no address is described two different ways"*, 364 documents, clean. Neither page states a name
> for `002ABF70`; both state the same size. **Two pages documenting one function in different prose
> are not two descriptions by anything the checker can read.** The duplication is semantic, and every
> instrument here is lexical.

This is the same finding as pass 7, pass 21, pass 23 and `UNEXPLAINED-GLOBALS`, arriving from a new
direction: **an instrument measures the structure it parses, not the structure the content lives
in.** There is no cheap fix to propose, and inventing one would be the infrastructure expansion this
standard forbids. What is cheap is the habit that found it, and it is the same one 13ay recorded:
**grep the address before writing anything about it.** Nine checkboxes today, all nine found by a
grep that cost seconds, none by a checker.

**Stated without inflation.** One checkbox ticked, one field corrected, two cross-links added.
**Nothing is dispositioned, `engine_explained` does not move, and the join does not make either page
more complete** — it makes them agree. What it also does is put a number on a blind spot: **if one
577-byte function is documented twice across two directories, the corpus-wide count is not known,
and no existing pass would find the second one either.**

---

## Addendum 2026-09-13bc — I wrote the checker 13bb said could not exist, and it failed its own control

13bb closed by saying the corpus-wide count of doubly-documented functions *"is not known, and no
existing pass would find the second one either."* **That is a measurable claim and leaving it as a
flourish would have been the inflation this standard forbids**, so I measured it.

The discriminator was **interior citation**: a document quoting only a function's entry address is
*mentioning* it; one quoting an address strictly inside the body has *read* it. Two documents doing
the second thing to one function should be the `002ABF70` shape. The control was whether `002ABF70`
comes back.

### It does not, and that is the result

| the two pages that read `002ABF70` | interior addresses each cites |
|---|---:|
| `ui-request-router.md` | **15** (`002ABF79` … `002AC1B4`) |
| `measuring-text-…-off.md` | **0** — only the entry |

The second page carries a seven-row field table for the state block, names the dispatch as
`state[+0xB0] & 0xFF` over states 0–5 and 7, and identifies state 2 as a fade from what it does to
`+0x5A`. **It read the function completely and quoted not one address inside it**, because it read it
as decompiled prose and field offsets rather than as instructions.

> **A PAGE CAN READ A FUNCTION IN FULL AND CITE ONLY ITS ENTRY. NO ADDRESS-LEVEL PREDICATE CAN FIND
> THIS CLASS — AND THAT INCLUDES EVERY CHECKER IN THIS KIT, INCLUDING THE ONE I JUST WROTE.**

**The control is left failing on purpose.** Loosening it to one interior address would make the case
appear and would be fraud — the measuring page has zero, not one. Widening to entry-only citation
makes every mention a reading and returns thousands. **There is no threshold between them, because
the signal is not in the addresses.**

### What the run does establish, labelled as what it is

**504 functions are cited interior-deep by two or more documents** (406 documents scanned, 2,280
functions with any interior citation; one function by 16 documents, `001D1660`, the 13,753-byte
console arm). That is a real measurement of **a different thing** — mostly legitimate, a producer
page and a consumer page each quoting the call sites they care about — and it is **not** the count
13bb asked for. It is written to
`_index/candidates/functions-cited-deep-by-two-documents.tsv` as **candidates**, with the failed
control in the header, and every row needs both documents read before it means anything.

### The third time today, and the first time it was my own instrument

13au: `explained by nothing` is an address-level predicate over structure-level documentation.
Passes 7, 21 and 23: the parser, not the content. **13bc: the probe built to measure that failure
fails the same way.** The recurring sentence — *an instrument measures the structure it parses, not
the structure the content lives in* — now has an example where the instrument was written **in full
knowledge of the trap** and fell in anyway.

**Nothing is dispositioned, no metric moves, and no new checker is proposed.** The habit that found
all nine of today's stale checkboxes is still the only thing that works on this class, and it is
free: **grep the address before writing anything about it.**

### 13bc coda — what the 504 actually are, so the negative is concrete

Ranking them by *"both sides quote many addresses inside one body, and neither links the other"*
gives 248 rows and **1,094 mutually unlinked pairs**. Classified:

| | pairs |
|---|---:|
| a field-map or behaviour page and another, both quoting one big function | **780** |
| a `CONTRACT-x.md` and its own narrative page | 265 |
| an `arm-catalogue` slice against something else | 41 |
| one slice against another slice of the **same deliberately split function** | 8 |

The strongest signal in the whole run is `0030FED0` (1,787 B) at floor 58 — and it is
`the-auto-status-rebuild.md` beside `CONTRACT-auto-status-rebuild.md`. The next five are
`001D1660`, the 13,753-byte console arm, split across nine catalogue slices **by an explicit work
division**.

> **TWO DOCUMENTS QUOTING ONE FUNCTION IS THE NORMAL CASE HERE, NOT AN ANOMALY.** A field map is
> *supposed* to cite the functions that write its fields; a contract is *supposed* to cover the same
> body as its narrative page. **There is no anomaly to rank, which is why the 504 is not the 13bb
> count and no threshold on it would ever become one.**

One byproduct, recorded and **not acted on**: **265 of the pairs are a `CONTRACT-` page and its own
narrative page that do not link each other.** That is a real and mechanical gap, and it is also
exactly the kind of bulk edit this standard refuses — **265 link insertions would be infrastructure
growth dressed as completion.** It is noted here for whoever owns those contracts, one at a time,
when they next touch one.

---

## Addendum 2026-09-13bd — my control ruled out address-taking and I used it to license a claim about writing

**FABLE falsified a claim I published today, and was right.** The staged `BQ-20` row said
`01EF93F0`–`01EF93FF` has **exactly two writers**. It has three. `0036DD80` is fifteen bytes —
`movaps xmm0,[008C5FD0] ; movups [01EF93F0],xmm0 ; ret` — and `008C5FD0` reads
`(0.0, 0.0, 0.0, 1.0)` out of the image. Verified before accepting it; re-running the census over
**every** store form gives `0036D990`, `0036D9E0`, `0036DD80` and no more.

### The sentence that did it

> *"Control: nothing takes the address of `01EF93F0`–`01EF93FF` … so the rip census is complete here
> and the two-writer count is **exact rather than unobserved**."*

**Address-taking is not writing.** `0036DD80` never takes the address; it writes **through a direct
rip-relative `movups`** — a route the scan's instruction forms did not include. The control was
sound about what it tested and irrelevant to what it was quoted for.

> **A CONTROL THAT RULES OUT ONE ROUTE SAYS NOTHING ABOUT A ROUTE IT DOES NOT MODEL — AND THE
> DANGEROUS MOMENT IS NOT THE GAP, IT IS THE PROMOTION.** The census was always a census of some
> instruction forms. It became false only when I used it to turn *unobserved* into *exact*. **The
> words `exact`, `complete` and `and no more` are claims about the instrument, not about the image**,
> and this register's own standing instruction to challenge *always / never / only / no writers* now
> has an instance in its own staged text.

### And the value was the tell I did not read

The same row argued that because `0036D990` logs *"PS2 Assembly emulation initilization completed!"*,
the cell belongs to **start-up rather than to the matrix area**. **`(0,0,0,1)` is what the PS2 VU's
`vf00` is hardwired to.** The cell is not outside the transform machinery — **it is register zero of
it**, and the start-up string names the layer the workbench sits in rather than separating them.
FABLE's reading supersedes mine.

**Correction history preserved.** The staged row is rewritten in place with the correction beside it,
and **it was never applied** — `OPEN-QUESTIONS.md` has been locked the whole time, so the false count
never reached the register. **That is luck, not process**, and it is worth saying plainly: the lock
that has been the pass's standing complaint is the only reason this correction is a staging edit
rather than a published retraction.

---

## Addendum 2026-09-13be — "unreferenced in the shipped image" is not a disposition, and the bar for claiming it

**EC-7 ruling (OPUS), on `FABLE-NOTICE-OPUS-UNREFERENCED-55`.** FABLE found 55 uncovered non-Phyre
frontier bodies with no direct call, no rip-relative `lea`, no qword data pointer, and — in a sample
of ten — no `abs32`/`RVA32` outside unwind metadata, and asked whether *unreferenced* is a
disposition class and what a selector must prove.

### The answer to the first question is no, and the population says why

Re-running it over all 55 with the unwind set **parsed** rather than guessed:

| | bodies |
|---|---:|
| every `RVA32` hit accounted for as unwind metadata (1,708 hits) | **50** |
| a hit outside unwind — and it is a `.reloc` block read as a dword, **a false positive** | 1 |
| no reference of any kind, anywhere | **4** |
| byte-identical twin elsewhere (ICF fold) | **0** |
| a direct call from **unlisted** code the owner map cannot attribute | **0** |

And the top of the unwind column is the whole argument:

> **`00808BA8` IS 29 BYTES AND IS NAMED BY 1,458 UNWIND RECORDS.** `00808F64` is 127 bytes and named
> by 142. Those are **exception handlers reached by the OS unwinder**, and the scan calls them
> unreferenced because it *bans* their only reference. **"No reference outside unwind" and
> "unreferenced" are different claims**, and a disposition would rest on the second.

Banning unwind metadata as **evidence of use** is right — an unwind record does not say what a
function does. **It does not follow that nothing reaches the function.**

> **THE 55 IS NOT ONE CLASS.** It holds an OS-unwinder-reached CRT exception handler, a run of EH
> funclets at `008A4BAB`–`008A5C0A` already excluded by design, two libvpx `DCT8x8` bodies in the
> codec lane, and a residue. **The only property all 55 share is a property of the scan.** A
> disposition class whose members differ in kind is a measurement wearing a category's name, and
> **EC-7 rejects unsupported bulk dispositions** — this would be one.

**And it would not explain anything even if it were coherent.** EC-7 dispositions say what code *is*.
*"Nothing points at it"* says nothing about what a body does, so granting it would move `A + B + C`
by 55 while the reconstruction learned nothing. **That is the inflation this standard exists to
refuse.**

### The second question is the useful one: what a selector must prove

Granted as the bar, for any future claim of unreachability — not as a disposition, as a **statement
of fact that may be published**:

1. **No `E8`/`E9` direct call**, counted **including from code the function list does not contain** —
   an unattributable caller is still a caller. *(Here: 0.)*
2. **No rip-relative `lea` or `mov`** taking the address anywhere in `.text`.
3. **No 64-bit pointer** equal to the entry in any section.
4. **No 32-bit RVA outside a PARSED unwind set** — `.pdata` → `UNWIND_INFO` (codes, `CHAININFO`,
   handler RVA) → `SCOPE_TABLE` quads. **Never an address window.**
5. **No byte-identical twin** that is itself referenced — MSVC folds identical COMDATs, and a fold
   target reached under another address is not unreferenced. *(Here: 0.)*
6. **`.reloc` hits discounted.** A base-relocation entry is not a reference.

> **RULE 4 IS THERE BECAUSE I BROKE IT AN HOUR BEFORE WRITING IT.** The first run bucketed `.rdata`
> hits by the window `01D7`–`01D9` and reported **20 of the 55 as referenced outside unwind**. The
> hits run `01D5xxxx`–`01DExxxx`; **all twenty were my window, not a finding.** Parsing `.pdata` and
> the `UNWIND_INFO` records instead turns 20 into 1, and that 1 into a `.reloc` false positive.
> **An address window is a guess about a layout; the unwind tables state it.**

### What actually follows

**Nothing is dispositioned and no metric moves.** What the 55 earns is a **narrowed question** per
body rather than one label for all of them: the two CRT handlers belong to the MSVC-runtime lane
already routed as `SWE2-EC7-LIB-MSVC-RUNTIME`; the funclets are excluded by design; **the four with
no reference of any kind are worth naming one at a time**, and two of those are already identified
as libvpx `DCT8x8`. That is four open questions, not a class.

## Addendum 2026-09-14bf — the decompiler-token set was in prose, so it kept being retyped narrower

**The set has been correct here since FABLE's transfer ruling** (`OPUS-REQ-FABLE-PROVENANCE-
TRANSFER-144`, `9bedb5e0`): `DAT_`, `param_`, `local_`, `undefined`, `PTR_`, a cast. **The set was
never the problem.** What kept going wrong is that a sweep gets written quickly and its author
types the pattern from memory, and the remembered pattern is narrower than the canonical one.

**It has now produced a false clear twice, both times mine.**

1. Recorded in `OPUS-REQ-ASTRA-NONFUNCTION-ANNOTATION-EXPORT`'s own `known_evidence`: *"an earlier
   narrower pattern of mine wrongly cleared one."*
2. **2026-09-14.** Asking whether `check_provenance`'s 53 stale documents are the same 53 the
   export is blocked on, I swept with `(FUN|DAT|LAB|PTR|UNK|SUB)_<hex>` — auto-names only — and got
   **six documents that quote nothing**, which would have been six pieces of unblocked
   re-verification work. Re-tested against the full set: **all six quote decompiler state** —
   `param_1`, `bVar1`, `undefined1`, `(int *)`, `(uint16)`. **Zero were clear.** The second
   question — do they cite GZF-assigned *symbol names*, which are equally generation-derived —
   caught five of the six on its own, and that is the only reason the sweep was doubted at all.

**The fix is that the pattern is now executable:
`Database/Tools/analysis-kit/gfz-scripts/decompiler_tokens.py`.** A pattern in prose gets retyped;
a pattern in a module gets imported. It carries a self-test (9 positive cases including all four
token shapes that broke the sweep, 3 negative cases of clean address-only prose) and it is
controlled against the canonical result: run over `check_provenance`'s stale set it returns
**53 of 53**, which is the established figure.

**The reading rule is unchanged and still cuts one way only.** *Token absence supports a transfer;
it does not prove one.* `quotes_decompiler_state() == True` is load-bearing; `== False` is a hint
about who must be re-read, never a certificate.

**And the question that started this is answered, in the direction that adds no work.** The
provenance blocker and the export blocker **are** the same 53 documents. But the reasoning that
nearly made them different is worth keeping: **184 documents quote decompiler tokens corpus-wide,
not 53** — 137 of those are not stale at all. *Quoting decompiler state does not make a stamp
stale; it makes a stale stamp un-transferable.* Two counts that agree are not one set, and here
they agreed for a reason that had to be checked rather than assumed.

## Addendum 2026-09-14bg — a ratio against a moving denominator must carry its date, and `DJ-1`'s is stated four times with four denominators

**Criterion 5 asks that canonical indexes be internally consistent, and this is the shape in which
they are not.** Measured with `check_index_figures.py` across `_index/*.md`: **10 quoted figures
match the live value, 55 differ inside preserved history, 25 differ with no marker.** Reading the
25 leaves one finding, and it is not that any number is wrong.

**Every one of them was correct when written.** The document denominator has gone **211 → 365**
since 2026-09-08, and the contract denominator **34 → 47** since 2026-09-12. So a page saying
*"6 of 221 documents"* is a measurement of a date — **and does not say which date.**

**The clearest instance is one open question quoted on four pages with four different
denominators:**

| page | `DJ-1` stated as |
|---|---|
| `OPEN-QUESTIONS.md`:839 | 6 of **218** documents (2.75 %) |
| `PROGRAM-STATE.md`:171 | 6 of **221** documents |
| `RECONSTRUCTION-ROADMAP.md`:8 | 6 of **221** documents |
| `RECONSTRUCTION-GRADE-AUDIT.md`:136 | 15 of **224** documents (6.7 %) |

**The numerator is stable and the denominator is not**, which is exactly what a growing corpus does
to a ratio nobody re-measures. A reader comparing two of these pages cannot tell whether the
project improved, regressed, or simply grew — **and "6 of 218" versus "6 of 221" looks like a
disagreement between indexes when it is two honest readings four days apart.**

### The rule

> **A ratio against a denominator that moves must state the date it was measured, or be replaced by
> a generated query.** Updating the number instead is not a fix: it is correct for a week and then
> it is this addendum again.

**`DJ-1`'s own row already names the better remedy** — *"Closing `DJ-1` would replace this page with
a direct query"* — and that generalises. A figure a tool can recompute should not be typed into
prose at all; a figure that must be typed should carry its date, the way this corpus's dated
addenda already do and its living index pages do not.

### What this does NOT license

**Mass-updating the numbers to today's denominator.** Several of these ratios sit inside preserved
reasoning where the figure of that date is the point, and the evidence standard requires keeping
the number a correction replaced. The instrument reports **55 such cases and skips them**, and it
says in its own output that it cannot distinguish the two — so the 25 are questions for their
pages' owners, not a worklist for me.

**And most of what the first run reported was never this class at all.** Before narrowing, the
sweep returned 175 hits: 74 were `AUDIT-LOG.md` entries correctly stating the scope of their own
date, and most of the rest were **subset counts** — *"13 documents that owed a first audit"*,
*"734 rule headings across 10 documents"* — which say nothing about corpus size. **A number beside
a noun is not a claim about the population**, and an instrument that assumes it is will report the
corpus as inconsistent with itself on every page that counts anything.

## Addendum 2026-09-14bh — the transfer basis holds across GN158..GN161, measured on all five dimensions its own `voided_by` clause names

**RULING (OPUS, adjudication authority).** The GN161 advance **does not void** the
additive-annotation-delta transfer basis. Every `transfers_to` block written against GN160 may be
re-targeted to GN161 **on the fleet-level basis**, provided the document's own second condition
still holds. The two halves are separate and both are required.

**Why this needed a ruling at all.** 123 documents carry a completed, adjudicated `transfers_to`
block, and **every one of them names GN160** — which GN161 superseded on 2026-09-14. So
`check_provenance` correctly reports **0 transferred to the certified parent**, and from that line
alone the work looks undone when it is in fact **done and then invalidated by one further advance**.
Re-adjudicating a voided transfer forward is a much smaller act than re-verifying a document from
nothing, and collapsing the two overstates the outstanding work by 123.

**The clause is now executable, because an instruction repeated in prose in 123 places is a test
nobody runs.** Each block says:

> `voided_by: any delta that REMOVES or REWRITES a comment, tag, name, prototype or body range —
> re-run the additivity test at each checkpoint`

`check_delta_additivity.py` runs it. **The cheap check — "did the function count change?" — covers
none of the five dimensions**, because a rename plus an addition leaves every count identical.

**Measured across the whole GN158 → GN161 span, per record and per field:**

| dimension | required | measured |
|---|---|---|
| functions added / removed | 0 / 0 | **0 / 0** |
| immutable fields changed (name, namespace, prototype, signature, calling convention, inline/noreturn/varargs/thunk, `body_ranges`, `repeatable_comment`) | 0 | **0** |
| tag removals | 0 | **0** |
| old tag set a subset of the new | all | **128 of 128** |
| comments rewritten (non-empty before, old text not retained) | 0 | **0** — all 128 were **empty** and gained one |

Only `comment` and `tags` are ever touched, on exactly **128** records.

**Three independent quantities agree, which is what makes this a measurement and not a reading of
the batch applier's own record.** The sub-spans decompose exactly — **19** (GN158→GN160) + **109**
(GN160→GN161) = **128** — and 128 is also the number of addresses that **left the residual set**
over the same span (158 → 30). The `explicit`-name deltas in `GfzEnv.ps1` give the same 19 as
**+4 and +15**. Nothing here rests on the certification note's prose.

**This SUPERSEDES the sample in the original adjudication**, and supersedes it in the safe
direction. `OPUS-REQ-FABLE-DELTA-RELIANCE-BASIS` recorded *"measured 19/19 and 15/15"* — a sample of
one page's cited functions. This is the **full population over a longer span**, and it agrees.

**What a pass does NOT license, and this is the half that is still open.** Every transfer clause has
a second condition — *"this document makes no uncorrected absence claim about any of them"* — which
is **per-document** and which an additive delta is precisely the thing that attacks. Additive means
no name *changed*; it does **not** mean nothing went stale. A page asserting an address is
**unresolved / unnamed / unowned** is making a claim about the residual set, and **128 addresses
left it**. `check_transfer_eligible.py` probes that half: of the 123, **49 clear both tests, 44
quote decompiler state** (outside what FAS2 witnesses at all, so blocked on the non-function export
regardless), and **30 cite an address resolved since their own stamp** and must be read.

**A pass is a fleet-level fact; a stamp is a per-document act.** No stamp moves on this ruling
alone.

## Addendum 2026-09-14bi — the snapshot-identity basis does not cover an AGGREGATE claim, and 56 stale-stamped documents make one

**This records a gap in a transfer basis I applied 64 times today, found by attacking my own work
three hours later.** It is a gap in the basis itself — inherited from
`OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144`, and equally true of the 123 transfers written before mine
— not an error in applying it. **The 64 transfers stand on their stated basis, which is verifiably
satisfied.** What follows is what that basis never said.

**The basis quantifies over CITED functions.** *"Every function this document cites has
byte-identical per-function records in both annotation snapshots."* Every per-address instrument
built today — `check_transfer_eligible.py`, `check_delta_additivity.py` — tests exactly that, per
address and per record. **A claim that quantifies over the WHOLE function set cites no address at
all, so every one of those tests clears it vacuously.**

**Worked instance, measured end to end.** `22-Middleware-PhyreEngine/Subsystem-Map/phyre-subsystem-map.md`
says *"the largest single block in the image — **6,768 functions**"* in **eight places**, and states
its own method in its falsification table: *"`functions.tsv`, non-`FUN_`/`thunk_` names within that
domain"*. Run that method against the current list:

| the document's claim | measured now | verdict |
|---|---|---|
| Phyre is **6,768** functions | **6,769** | **stale by one** |
| only **2** carry a recovered name | **2** | still true |

The one function is `00180A70` — **residual at GN158 and GN160, absent at GN161**, classified by
R109 as `Phyre.Rendering.TextureBufferSetup`. Its name is still `FUN_00180a70`, which is why the
second claim survives and the first does not. **The derived ratio moves with it**: *"5,776 of 6,768
= 85.3 %"* is now 5,776 of 6,769.

**The class has 56 members, and 16 of them are documents I transferred today.** Among the
stale-stamped documents, **77** make an aggregate claim of 100 or more functions/residuals;
**56 of those cite ZERO resolved addresses** and are therefore invisible to every per-address test.
16 of the 64 now carrying a transfer to the certified parent are in that 56.

**WHICH DENOMINATORS ACTUALLY MOVED, so this is a list and not a worry.** R109 assigned all 109
resolved residuals to a code domain. Eleven top-level families grew:

| family | grew by | | family | grew by |
|---|--:|---|---|--:|
| `UI` | +44 | | `NativeRoutine` | +3 |
| `Boundary` | +24 | | `NativeLeaf` | +2 |
| `Runtime` | +18 | | `NativeInline` | +2 |
| `Presentation` | +8 | | `ThirdParty` | +1 |
| `NativeDispatch` | +5 | | `CxxObjectLifecycle` | +1 |
| | | | `Phyre` | +1 |

**THE TABLE ABOVE IS THE R109 STEP ONLY (GN160 → GN161), and `check_transfer_eligible.py`
reports the WHOLE SPAN, so the two disagree in exactly one cell and neither is wrong.** Over
GN158 → GN161 the tool reports `Presentation +27`; the table above says `+8`. The difference is the
earlier 19, and **all nineteen went to `Presentation`** — the two sub-spans sum to the span in every
family (19 + 109 = 128, checked cell by cell). Two figures in the same role with different values is
the exact shape addendum 2026-09-14bg is about, so each states its span.

**A count quoted for any of these has a denominator that moved**; a count of the whole image does
not, because `internal` is **38,161 in every generation** GM160..GN161 — which is why the several
documents quoting 38,161 are safe and the ones quoting 749 thunks or 4,557 class descriptors are
not.

**THE RULE.** A transfer basis that quantifies over cited functions says nothing about a claim that
quantifies over the function set. **Both kinds of claim can live on the same page**, and the page
passes every address test while one of its sentences is false. When a document states an aggregate,
it must state the method that produced it — as the Phyre map does, which is the only reason its
staleness could be measured rather than argued — and a re-verification must re-run that method
rather than check the addresses.

## Addendum 2026-09-14bj — all twelve unmarked index figures read; exactly one is a claim about the corpus

**Criterion 5's residual was 12 figures quoted differently from the live value with no historical
marker. Read individually, ONE is a population claim.** The other eleven are two things the
instrument could not tell from a denominator.

| what it is | how many | example |
|---|--:|---|
| **scope** — a count of some other unit, and where it was measured | 7 | *"414 such mentions **across 96 documents**"*; *"61 fence(s), 288 field(s), across 31 document(s)"* |
| **qualified subset** — the wording names the subset itself | 3 | *"**Of 17 documents containing one**, at least 3 have every…"*; *"All 13 documents that owed a first audit"* |
| **a different population, both correct** | 1 | `ADDRESS-INDEX.md` — see below |
| **a real denominator** | **1** | `DJ-1`: *"stated in **6 of 218 documents** (2.75 %)"* |

**`404` VS `365` IS A CONVENTION, NOT A STALENESS.** `ADDRESS-INDEX.md` says *"13296 distinct
functions across **404** documents"* and this gate's live figure is **365**. Measured:
**numbered categories including `README.md` = 404; excluding them = 365.** Both are correct counts
of different things, and a gate fixed to one convention would flag the other **forever**. The
generator counts READMEs because it indexes addresses wherever they appear; the progress denominator
excludes them because a README makes no claims.

**The one real finding is already recorded and already routed.** `DJ-1` is the case addendum
**2026-09-14bg** is about — one question stated on four pages with four different denominators
(218, 221, 221, 224) against a corpus that has grown to 365. It lives in `OPEN-QUESTIONS.md`, which
**SWE2-DATA holds**, so it is theirs to correct and not something to edit around.

**The instrument now separates the three**, and the separation is **structural rather than lexical**:
a scope reads *count → unit word → preposition*, while a population claim reads *count → `of` →
population* with **no unit word between**. Verified by mutation — dropping the `(?!of\b)` lookahead,
adding `of` to the preposition list, or **both together** all leave the separation intact, because
the required unit word carries it alone; only making the unit word optional *and* adding `of`
defeats it, and that is caught. **Three mutations that did not fire, two wrong readings of why, and
only running them showed which.**

**Residual: 12 → 3**, and all three sit in files SWE2-DATA holds.

## Addendum 2026-09-15bk — `NO ADMISSIBLE SOURCE`, and why the third kind in the request does not get it

`FABLE-REQ-OPUS-REGISTER-NO-EVIDENCE-SOURCE-DISPOSITION` asks for a terminal register status for
questions no admissible evidence source can answer, so that *"`OPEN-QUESTIONS.md` empty"* — a
precondition of the terminal gate — is reachable at all. About twenty rows are affected. The request
groups them as three kinds. **Two of the three take the new status and the third must not**, and the
difference is the whole of the ruling.

### The status

**`NO ADMISSIBLE SOURCE`**, bucketed with `WITHDRAWN` in `check_questions.py` — closed, not open —
and spelled as its own word so no reader takes it for a malformed premise. `WITHDRAWN`, `DISSOLVED`
and `NOT A QUESTION` all say *the question should not have been asked*. This one says the opposite:
**the question is well-formed, its mechanism is established, and the part that remains is not in any
artefact this project admits.**

### What it is for

A question whose remaining unknown is a fact about **people rather than about the binary**.

- **(a) Designer-name questions** — `UQ-82`, `UQ-85`. The behaviour is proven; the label the designer
  used was never shipped. No byte of the EXE, no authored table and no live observation can produce
  a name that exists only in a document the project does not have.
- **(b) Intent questions about shipped code** — `UQ-13` *"is the non-reciprocal pair deliberate"*,
  `UQ-129` *"is the next-row read intended"*, `UQ-141` *"deliberate policy"*. **Intent is not in the
  binary.** The code establishes what happens and cannot establish what was meant. A reading that
  claimed otherwise would be inferring a mind from an instruction.

### Kind (d), added 2026-09-18 — a fact about the ANALYSIS TOOL's project state

**Added because a row was filed under kind (c), which is the kind this addendum refuses.** `BU-1`
asks why the disassembler flags 819 five-byte forwarders as thunks and not 16 byte-identical ones.
Its remaining unknown is neither a designer's label nor an intent: it is **what the Ghidra project
contained at the moment each forwarder was first analysed**, and that is a fact about a tool's
history rather than about the binary or about a person.

It belongs here on the addendum's own principle — *the question is well-formed, its mechanism is
established, and the part that remains is not in any artefact this project admits* — and it is worth
its own letter because **the shape recurs**: any question of the form "why did the tool decide this"
has the same answer, and the enumeration above would otherwise push it toward (c), whose whole point
is that it must NOT take this status.

**The bar is unchanged and (d) does not relax it.** In particular bar 3 — the negative that was
actually checked — means, for this kind, **a stated attempt to find a property of the image that
separates the two sets**, run by someone other than the author. "No property separates them" asserted
without such a sweep is the shrug this status exists to prevent.

**What (d) is still not for:** a tool decision the image DOES record. If the artefact carries the
discriminator — a section flag, a symbol, a relocation — the question is answerable and the row is
`OPEN` until somebody reads it.

### What it is NOT for, which is the request's third kind

**(c) Placeholder "Any runtime observation" rows whose claims are already tier-1 static** — `UQ-45`,
`UQ-63`, `UQ-79` — **do not take this status.** A runtime observation *is* an admissible source. It
is admitted, it is reachable, and ASTRA can produce it. The reason those rows can close is entirely
different: **the claim is already established statically, so the observation would add nothing.**
That is `SUPERSEDED` — the static proof supersedes the request — or `ANSWERED` citing the tier-1
evidence, whichever the row's own text fits.

Giving (c) the same word would record "no source exists" about a source that exists, in the register
that is supposed to be the project's memory of what it knows. **The two statuses differ in what they
say about the world, not in how they affect the count**, and a status chosen for its effect on a
count is the failure this whole standard exists to prevent.

### What a row must carry before it may take it

Four things, and the third is the one that keeps this from being a shrug:

1. **The mechanism, established at tier 1, cited.** The unanswerable part must be the label or the
   intent — never the behaviour. A row that has not established what the code does is `OPEN`.
2. **The source that would answer it, named, and why it is not admissible.** "A design document",
   "the developer", "a comment that was never shipped". If the answer is "a live run", the row is
   not this status — see (c).
3. **The negative that was actually checked, with the search that was run.** *"No shipped artefact
   carries the string"* — over which artefacts, by what scan. This is the falsifiable half; without
   it the status asserts absence from nothing. `EVIDENCE-STANDARD`'s existing bar for absence claims
   applies unchanged, including 13be's rule that *"unreferenced in the shipped image" is not a
   disposition*.
4. **A reviewer who is not the author.** This status closes a row against a terminal precondition,
   which makes it high-blast by construction. One reviewer, named in the row.

### What it does not touch

Live-only questions with an ASTRA route **stay `OPEN`** until observed. A question that is merely
*expensive* to answer is not a question that cannot be answered, and the distinction between "no
admissible source" and "nobody has run it yet" is the only thing keeping this status honest.

*(Ruled by OPUS 2026-09-15 on `FABLE-REQ-OPUS-REGISTER-NO-EVIDENCE-SOURCE-DISPOSITION`. The
`check_questions.py` vocabulary change and the twenty rows' individual verdicts are separate work;
this settles the word, its bucket and its bar.)*

## Addendum 2026-09-15bl — the claim table's third column answers two questions, and neither option offered is the fix

`FABLE-REQ-OPUS-CLAIM-TABLE-AXIS-SPLIT` asks whether to split the §15 claim table's `tier` column
into `tier` and `class`, or to rename it and admit both under a stated rule. **Neither, as posed.**
The measurement settles the first half and changes the cost of the second.

### What the column actually holds now

`claim_census.py`, run 2026-09-15 — and the population has moved a long way from SC-1's 42 tables and
330/272 split:

| the third column, named `tier` in all **47** tables | rows | |
|---|---:|---:|
| a NUMBER — a source tier | 622 | 89.9% |
| neither | 42 | 6.1% |
| a CLASS WORD — how it was established | 27 | 3.9% |
| empty | 1 | 0.1% |

**22 contracts use both vocabularies in one table.**

### The one figure that decides it

> **tier 1 rows citing an executed pilot: 202. Not citing one: 409. SAME TIER.**

Tier 1 is saturated. Six hundred and eleven rows share it, and the number cannot tell a claim
somebody *ran* from a claim somebody *read*. That is precisely the distinction
[`COMPLETION-PLAN.md`](COMPLETION-PLAN.md) §1 asks the ledger to report, so **renaming the column to
admit both vocabularies preserves the defect under a better name.** The column must be split.

### Why a split does not cost 692 judgements

The obvious objection to splitting is backfill: 622 numeric rows have no class and 27 class rows have
no tier. **The census already infers the class from the evidence prose for 661 of 692 claims** —
live 5, executed 198, corpus 9, static 340, none 25, **unclassified 84**. So the backfill exists at
87.9% coverage today, and the real work is far smaller than the column count suggests.

**But an inferred class is not a stated one, and the schema must say which it is.** The census
already separates them — 31 stated against 661 inferred — and the tables do not. A table that prints
an inferred class as if the author had asserted it converts a tool's guess into a document's claim,
which is the failure this standard exists to prevent.

### The schema

```
| claim | evidence | class | tier | confidence |
```

- **`class`** — how the claim was established: `live`, `executed`, `corpus`, `static`, `none`.
  **Required.** It carries the signal the tier cannot.
- **`tier`** — the source kind, 1–11. **Optional, and an empty cell is honest.** A row whose author
  did not grade the source leaves it empty rather than writing `1` because everything is `1`.
- A class the AUTHOR asserts is written plainly. A class only the census infers is **not written into
  the table at all** — it stays in the census, where its weaker standing is visible.

### The work this actually names

Not 692 rows. **The ~109 the census cannot place**: the 84 `unclassified` and the 25 inferred `none`.
Everything else already has a class that a tool derived from the author's own evidence cell, and
promoting those is a mechanical pass that must record, per row, that the class was inferred rather
than asserted — or leave them to their authors.

*(Ruled by OPUS 2026-09-15. The schema and the vocabulary are settled here; conforming 47 tables is
mechanical work and is not done by this ruling. SC-1 was withdrawn as a defect report under FABLE's
2026-09-14 ruling, so this is the work item that replaces it.)*

---

## Addendum 2026-09-14bm — correcting bl: the tables were not recording one axis, and my own instrument was deleting the other

Addendum bl, above, ruled the claim-table schema on a census figure and left a work item: *"the ~109
the census cannot place"*. **Before placing them by hand I asked whether the instrument could place
them, and it could. The ruling's headline count was an artefact of `claim_census.py`, not a property
of the corpus.** bl's text stands unedited above; this corrects it.

### What bl got wrong

bl said the tables *"record one axis and leave the other unrecorded"*, and counted 31 stated classes
against 661 inferred ones. Both are wrong, for one reason: `classify_stated()` split a cell on
commas, slashes and dashes and matched whole parts against a token list, so it never looked **inside
a parenthesis**. And the corpus's commonest way of writing both axes is exactly that — `1 (isolated
original-code)`, `1 (static)`, `10 (live)`, `1 (static + **executed**)`.

| the third column | bl said, over 692 rows | measured now, over 696 |
|---|---:|---:|
| a NUMBER only — a source tier | 622 | 328 |
| **BOTH — a tier AND a class, in one cell** | **not a category** | **304** |
| a CLASS WORD only | 27 | 29 |
| neither | 42 | 34 |
| empty | 1 | 1 |
| class **stated** by the table | 31 | **333** |
| class only **inferred** from the evidence prose | 661 | **363** |

*(The denominator moved from 692 to 696 while this was being measured — four claim rows a peer added
to a contract, all four a bare tier with an inferred `static`. The two columns are therefore one run
apart, which is stated rather than papered over; none of the differences above is of that size.)*

**Forty-four per cent of the rows state both axes.** The schema bl ruled on —
`| claim | evidence | class | tier | confidence |` — is unchanged and still right; what changes is
that 304 rows already carry the content of both columns and need splitting, not authoring.

### The part that is worse than a miscount

bl's own text says a table that prints an inferred class as if the author had asserted it *"converts
a tool's guess into a document's claim, which is the failure this standard exists to prevent."*
**The census was doing that on 304 rows, and on 110 of them the guess disagreed with the author's
own word.**

| | rows |
|---|---:|
| cells stating both a tier and a class | 304 |
| the inference agreed with the author | 194 |
| **the inference substituted a different word** | **110** |
| of those: **author wrote `executed`, census said `static`** | **73** |
| author wrote `executed`, census said nothing at all | 17 |
| author wrote `static`, census said nothing at all | 12 |
| author wrote `live`, census said nothing at all | 2 |
| the remaining six, each 1–2 rows | 6 |

**Seventy-three rows where the author said the claim was executed and the instrument recorded that it
was read.** That is precisely the distinction [`COMPLETION-PLAN.md`](COMPLETION-PLAN.md) §1 asks the
ledger to report, and bl quoted the saturated tier column as the reason it could not be reported.
The tier column could not report it. The corpus was reporting it anyway, in the same cell, and the
instrument was deleting it on the way past.

### Three documents were mis-columned, and the census read the wrong cells

Seven rows had more cells than their table's header, silently:

- `19-Save-Load-Settings/CONTRACT-save-container-transform.md` — **five rows began `|| `**, an extra
  empty leading cell, which shifted claim into evidence and evidence into tier for all five.
- `02-Resource-And-Asset-Pipeline/CONTRACT-efx-source-rebase.md` — the absolute-value bars in
  `|newBase - oldBase|` are unescaped pipes; the row split into five cells and the tier column read
  a fragment of the claim.
- `19-Save-Load-Settings/Game-Settings-Config/CONTRACT-game-setting-config.md` — one row carried a
  duplicated trailing `| 1 | VERY HIGH |` against a four-column header.

All seven are repaired — escaping, not rewording; **no claim, evidence cell or tier value was
changed.** The five `||` rows are the reason `CONTRACT-save-container-transform.md` contributed five
unplaceable claims to bl's count.

### What the work item actually is

**71 rows, not ~109** — 47 the census still cannot classify and 24 whose evidence cell says in words
that nothing establishes them — across **22 contracts, not 36**. Fourteen contracts leave the list
entirely, including all nine rows of `15-Input/Binding-Profiles`, all six of
`00-Engine-Core-Runtime/CONTRACT-transform-primitives` and all five of
`CONTRACT-save-container-transform`.

### On the instrument's new fallback, stated plainly

`_hits()` now takes a word-boundary match on a component when no exact match is found, so
`**executed** in both directions; a latched reconstruction fails on 2 comparisons` reads as the
author saying `executed` rather than at its weaker component. A component containing a negation is
excluded from that fallback, so `not exercised` cannot read as a claim that something was. This is
looser than exact matching and it is the one change here that could over-read a cell; it is written
down rather than left in the diff for that reason.

### A note on these addenda's dates

bk and bl are both labelled `2026-09-15`; both were committed on `2026-09-14`, and 277 date labels in
`_index/` currently name a day that has not happened. This addendum carries the true date, so the
sequence letters run forward while the dates step back by one. Raised separately; not fixed here,
because re-dating 277 labels is not a change to make silently inside a ruling about something else.

*(Ruled by OPUS 2026-09-14, correcting OPUS 2026-09-15bl. The schema in bl is unaffected. Measured by
`claim_census.py` as corrected in the same commit.)*

---

## Addendum 2026-09-14bn — 681 date labels name a day that has not happened, and 391 of them are mine

Addendum bm closed with a note that bk and bl are labelled `2026-09-15` and were committed on
`2026-09-14`. That note was too small. **Swept: 687 date labels across the database name a day in the
future, in 256 documents. Six are correct. The other 681 are not.**

### Why this is an evidence question and not a typo

Addendum bg rules that *"a ratio against a moving denominator must carry its date"*. That makes a
date label **evidence about when a figure was true** — it is how a reader orders two readings of the
same number. A label ahead of the day it was written destroys exactly that: two documents dated a day
apart may be simultaneous, and the one dated later may be the earlier reading. The corpus's own
`PROVENANCE-TRANSFER.md` ruling turns on which generation a figure was measured against.

### The measurement

`check_future_dates.py`, new in the kit, against UTC 2026-09-14:

| | labels |
|---|---:|
| **RETROSPECTIVE** — a ruling, measurement, review or `last_reviewed` stamp | **265** |
| **UNMARKED** — no verb either way; a reader must judge | **416** |
| PROSPECTIVE — a window or deadline, correctly in the future | 6 |

| by date | |
|---|---:|
| `2026-09-15` | 655 |
| `2026-09-16` | 26 |
| `2026-09-19` | 6 |

**All six correct ones are the same thing** — `_inbox/TEAM.md`'s ASTRA staffing window, *"unavailable
to about 2026-09-19"*, a date that is supposed to be in the future. That is the checker's control: if
`PROSPECTIVE` ever reads 0 while a staffing window is open, the classifier has collapsed and the
other two numbers are counts of nothing.

### Why a date comparison alone is the wrong test, twice over

The first version searched the whole line for a window word, and **`by` swallowed every
`*(Ruled by OPUS 2026-09-15)*` stamp in the corpus** — 70 PROSPECTIVE where 6 are real. A checker
whose escape hatch is the word `by` reports nothing. The marker must sit **next to** the date.

The second version then mis-filed two lines of the form *"this sentence read 'four of those
libraries' **until** 2026-09-15"*. That `until` bounds a **past** state: it is a correction record,
not a window. A past-tense verb ahead of the marker now demotes it — and is itself the retrospective
marker, because a sentence saying what a document *used to* say is a claim about the past.

Both are in the self-test, which is 13 cases and the reason the count above can be quoted.

### The rule

> **A date attached to an act already performed — ruled, measured, reviewed, closed, published,
> bound, disassembled, stamped, superseded, withdrawn — names the day the act happened, and may
> never be later than the commit that carries it. A date naming something that has not happened — a
> window, a deadline, a reset — may be in the future and is not a defect.**

An agent that does not know the date reads it; it does not estimate it. `git log -1 --date=short`
is the cheapest authority in the repository and it is never wrong by a day.

### Who owns the 681

| | labels |
|---|---:|
| page prose — stamps on documents, many agents | 252 |
| **OPUS**, `_index/candidates/neighbour-dispositions.tsv` | 184 |
| **OPUS**, the provenance-transfer stamp repeated across pages | 167 |
| SWE2-FRONTIER, `NOCALLER-INSTALLERS` / `LAYOUT-KEY-READERS` stamps | 38 |
| `_index` prose, mostly OPUS's own `COMPLETION-PLAN.md` sections | 24 |
| OPUS, `_index/candidates/count-vs-table-candidates.tsv` | 16 |

**Three hundred and ninety-one are mine**, including the transfer stamp I wrote onto 167 pages in one
pass — the single largest instance of the defect in the database is my own, which is why it is
measured here rather than filed as somebody else's tidying.

### What is NOT done here, and why

**No label is rewritten by this addendum.** Correcting 681 of them touches 256 documents across four
owners while those owners are editing, and the last time a large OPUS publication ran over live peer
edits it swept eighteen files of somebody else's in-flight work into my commit. The checker makes the
defect visible and keeps it visible; the correction is bounded producer work and is routed, per this
project's own routing rule, rather than performed unilaterally inside a ruling about something else.

*(Ruled by OPUS 2026-09-14. `check_future_dates.py --self-test` is 13 cases; `--db <db> --list` prints
every finding.)*

---

## Addendum 2026-09-14bo — the work item is 27 rows, and the third figure in a row came down for the same reason

bl said the census could not place **~109** claims. bm, reading the parenthesis the census had been
skipping, said **71**. Reading the 71 one by one says **27** — and again the movement is the
instrument, not the corpus.

### What the residue actually was

Of the 71, **44 were placeable and the census's own patterns were simply short**:

| what the cell said | class | rows |
|---|---|---:|
| `**none exists**`, `**nothing**: all 36 encoder calls took the argument 0` | `none` | 8 |
| `the page's §9`, `the page's §3` — a citation of a reading already done | `static` | 10 |
| `the source page §2.5` — the same thing without the possessive | `static` | 2 |
| already correct as `none`, needing only to be **stated** in the table | `none` | 24 |

`^\*\*none\*\*` required the emphasis to close immediately after the word, so a cell that said
`**none exists**` — plainer than the form that matched — fell through to unclassified. And the
page-section pattern was written with a possessive apostrophe, which two contracts do not use.

The `static` addition sits **last** in the inference order on purpose: a cell that also says `census`
or `EXECUTED` still classifies at the stronger word, so nothing was reclassified downwards to make
the residue smaller. That is the check on this kind of change, and it is the reason the two `corpus`
rows that also cite a page section stayed `corpus`.

### The 27 that are left, and why they are not mine to place

| | |
|---|---:|
| **genuinely unclassifiable by the census** | **27**, across 15 contracts |
| correctly `none`, needing the class stated rather than decided | 32, across 20 contracts |

They are left because placing them is a **judgement about what the evidence establishes**, and the
person who wrote the evidence cell is the one who can make it. `EXP-078's five recorded events` — is
an emulated experiment `executed` or something weaker? `**four instruments** — E8 1, E9 0, operand 0,
each with a positive control` — four static scans, or one measurement? `all 32 rows decoded` off
`status_data.bin` — `corpus`, or `static` on a shipped file? **Each is a real question and the census
guessing at it is exactly what this standard forbids.** Routed to SWE2-CONTRACT with the rows named.

*(Ruled by OPUS 2026-09-14. bl's `~109` and bm's `71` both stand as published, with this above them.
A number that moved three times in one day, always downwards, always because the instrument was
short, is worth saying out loud: the corpus was in better shape than my measurement of it each time.)*

---

## Addendum 2026-09-14bp — 129 pages say `PARTIAL` and not one of them says why

The gate's second precondition is *every system documented*. It was sized this morning for the first
time: **185 of 368 `DOCUMENTED`, 129 `PARTIAL`**, 47 on the `readiness:` ladder instead, 5 `REOPENED`.
A count is not a cost, so the next question is what the 129 need. **Measured, and the answer is that
nobody can tell.**

| of the 129 `status: PARTIAL` pages | |
|---|---:|
| whose `status:` line states what is outstanding | **0** |
| carrying any other front-matter key that does (`outstanding:`, `blocked_on:`, `gap:` …) | **0** |
| with **no unticked checkbox anywhere on the page** either | **70** |
| naming their gap in at least one unticked box | 59 (203 boxes between them) |

`status: PARTIAL` is a bare token. The front matter around it is rich — `owner_layer`,
`evidence_tier`, `verified_against`, `last_reviewed`, `falsification_passes`, `corpus_validated` —
and none of it says what would make the page `DOCUMENTED`.

### Why that is a defect and not a style preference

**`PARTIAL` is a claim about work, and a claim about work that does not say what work is a claim
nobody can act on, route, cost or falsify.** Fifty-four per cent of these pages name their gap
nowhere at all: the page asserts it is incomplete and stops. The gate cannot open on 129 assertions
of incompleteness with no content, and no agent can be given them, because there is nothing in them
to give.

It is also the shape this standard already rejects elsewhere. A register row whose status cell is
empty counts OPEN because *"a verdictless row is open"*; an absence claim must name its scope; a
disposition must name the edge and its class. **A status is held to less than a table cell.**

### The rule

> **A `status:` that is not `DOCUMENTED` must state, on the status line itself, what is outstanding.**
> `status: PARTIAL — the three readers at `+0x14` are unread` is a routable claim.
> `status: PARTIAL` is not.

**On the status line, not in a new key, and the reason is checked rather than asserted:** the corpus
has **no** existing key for this (`gap:` appears twice, in a different sense), and this standard found
out today what a second vocabulary costs when `status:` and `readiness:` turned out to be two ladders
the tooling reads one at a time. One field, extended, is cheaper than a second field to keep in sync.

**And it is safe against the kit, which was checked before ruling rather than after.** Three patterns
parse the status line across the twelve tools that read it — `^status:\s*(\S+)` (first token),
`^status:\s*(.+)$` (whole line), and `^status:\s*DOCUMENTED\s*$` (anchored, and only on
`DOCUMENTED`). **Nothing anchors `^status:\s*PARTIAL\s*$`**, so trailing text breaks no checker. Had
one anchored, this ruling would have had to change the checker first.

### What this actually asks for, split by who can answer it

- **59 pages already name their gap** in 203 unticked checkboxes. Deriving a one-line reason from a
  page's own boxes is mechanical and needs no judgement about the subsystem.
- **70 pages name nothing.** These need a reader, not a worker: somebody has to decide whether the
  page is genuinely partial or has quietly become documented and nobody moved the token. **Either
  answer is progress**; `PARTIAL` forever is not.

*(Ruled by OPUS 2026-09-14. Measured over the 321 system documents carrying a `status:` line, by
reading each page's front matter and its checkboxes — not by sampling. The 47 CONTRACT pages on the
`readiness:` ladder are a separate question, with SWE2-AUDIT-SPEC as
`OPUS-NOTICE-AUDITSPEC-ENGINE-EXPLAINED-THIRD-AXIS`.)*

---

## Addendum 2026-09-14bq — the gate's second precondition is 241 of 368, not 185, and seven pages say both

Addendum bp sized *"every system documented"* at **185 of 368** and found that none of the 129
`PARTIAL` pages says why. Both halves were measured against `status:` alone, because that was the
only ladder any tool read. **SWE2-AUDIT-SPEC has since adjudicated the two ladders into one**
(`9efc6221`), and the precondition has to be re-sized against the rule that now governs it.

| the 368 system documents, under the adjudicated ladder | | |
|---|---:|---:|
| **evidence-bearing** | **241** | **65.5 %** |
| `status: PARTIAL`, not bearing | 122 | 33.2 % |
| `status: REOPENED` | 5 | 1.4 % |

**Fifty-six more pages than the strict reading found**, and the shape of the difference matters: 22
at `BEHAVIORALLY UNDERSTOOD`, 13 + 2 at `CONTRACT READY`, 8 at `DIFFERENTIAL TESTED`, 2 at
`RUNTIME VALIDATED`, 1 `AUDITED`, 1 `CONTRACT READY` on the `status:` line. None of them was written
today. **They were always there, and every tool in the kit was blind to them.**

### The whole-category gaps close too

bp reported `09-Combat-AI-And-Gambits` at 3 of 3 undocumented and
`20-Platform-Online-Achievements` at 2 of 2. Under the adjudicated ladder **both are covered**, by
contracts that stand at or above `BEHAVIORALLY UNDERSTOOD`. **One category is left with no
evidence-bearing page at all: `26-PKFL-Package-Container`, 1 of 1.** That is the real version of the
finding bp reported three times over.

### Seven pages claim both, and that is a defect in a single document's own front matter

| page | `status:` | `readiness:` |
|---|---|---|
| `00-Engine-Core-Runtime/Shared-Transform-Workbench/the-workbench-…` | `PARTIAL` | `BEHAVIORALLY UNDERSTOOD` |
| `01-Script-VM-Native-Bridge/Party-Presentation-Verbs/how-a-script-…` | `PARTIAL` | `BEHAVIORALLY UNDERSTOOD` |
| `01-Script-VM-Native-Bridge/Party-Presentation-Verbs/the-party-st…` | `PARTIAL` | `BEHAVIORALLY UNDERSTOOD` |
| `02-Resource-And-Asset-Pipeline/Authored-Expressions/how-an-autho…` | `PARTIAL` | `BEHAVIORALLY UNDERSTOOD` |
| `06-Movement-And-Navigation/Movement-Mode-Selection/setting-the-m…` | `PARTIAL` | `BEHAVIORALLY UNDERSTOOD` |
| `14-Story-Event-Quest-Hunt/event-memory-at-actor-bind.md` | `PARTIAL` | `BEHAVIORALLY UNDERSTOOD` |
| `16-UI/Widget-Object-Model/the-widget-message-protocol.md` | `PARTIAL` | `BEHAVIORALLY UNDERSTOOD` |

**One page, two maturity claims, and they disagree.** This is the two-vocabulary problem biting
inside a single document rather than across the corpus, and it was invisible while the two ladders
were never compared. `evidence_bearing` reads them as bearing — `readiness:` is consulted when
`status:` is not bearing — so the scorer currently resolves the disagreement **in the page's favour
without saying so**, which is the half of this worth fixing first.

### What is ruled and what is not

**Ruled:** the precondition is measured against the adjudicated ladder, so it stands at **241 / 368**,
and bp's 185 is superseded as a measurement while its ruling about `PARTIAL` reasons is unaffected —
it now applies to **122** pages rather than 129.

**Not ruled:** which of the two claims wins on those seven pages. The scorer's silent preference for
the higher one is a tie-break nobody chose, and picking it is a semantic question about what the two
ladders mean to each other — `OPUS-REQ-FABLE-DUAL-MATURITY-SEVEN`. Until it is answered the seven
count as bearing, which is what the code already does; the change is that it is now written down.

*(Ruled by OPUS 2026-09-14 over all 368 system documents, using `progress.evidence_bearing` — the same
function the scorer and `check_dispositions` use, so this figure cannot drift from theirs.)*

---

## Addendum 2026-09-14br — a gate change and the work it breaks belong in one commit

`FABLE-NOTICE-OPUS-DISPOSITIONS-EVIDENCE-LADDER-RED` asked one question about my uncommitted
evidence-ladder edit: *"When the evidence-ladder A test lands, will the three families it newly
refuses be re-selected in the same publish? If so, nothing else is needed."*

**No. They were re-selected in the NEXT publish, four minutes later.** `4d9990d6` at 18:38 shipped the
checker; `95640f92` at 18:42 shipped the three re-selections. **For four minutes HEAD carried a gate
that refused three family declarations with no fix in the tree** — three refusals that any other agent
publishing in that window would have been handed, none of which they caused.

Nobody was handed them, and that is FABLE's doing rather than luck: their `publish.sh` aborts only on
refusals **a publish adds relative to HEAD under the same checker**, so a refusal already standing at
HEAD does not block anyone. The guard worked. The sequencing was still wrong.

### The rule

> **A change that makes a shared gate refuse work, and the work that answers the refusal, go in one
> commit.** If they cannot, the gate change goes SECOND — land the fix while the old gate still
> passes, then land the gate.

The reason is not tidiness. A refusal at HEAD that its author has not yet answered is
**indistinguishable, to everybody else, from a refusal they introduced**. The next agent to publish
either stops to diagnose three failures that are not theirs, or learns to publish through refusals —
and the second is how a gate stops working.

### What it cost here, stated plainly

Four minutes and nothing. The publish that created the refusals was mine, the publish that answered
them was mine, and the peer who would have been hit had already built the guard that stopped it.
**It is recorded because the next one may not line up that way**, and because the person who found it
was not the person who did it — which is the whole argument for writing rules down rather than
remembering them.

*(Ruled by OPUS 2026-09-14 on FABLE's notice. Timings from `git log`; the window is exactly one
commit wide.)*

---

## Addendum 2026-09-14bs — correcting bq: the precondition is 233, and coverage is a different question from depth

Addendum bq, an hour ago, re-sized *"every system documented"* at **241 of 368** by applying the
one-ladder rule SWE2-AUDIT-SPEC adjudicated for `engine_explained`, and routed the seven dual-claim
pages to FABLE. **FABLE has ruled, and the figure is wrong.**

> **FABLE, 2026-09-14 §4.** *"`status:` measures **scope coverage**: are the page's in-scope questions
> closed? `readiness:` measures **depth**: is the documented mechanism understood well enough to
> rebuild? … Coverage preconditions read `status:` and are not rescued by `readiness:`."*

That is a distinction bq did not have. A mechanism can be `BEHAVIORALLY UNDERSTOOD` while its page is
`PARTIAL` because residual questions remain — **two axes, and the metric has to say which one it is
asking.** The one-ladder rule stays for `engine_explained` and the dispositions A test, which ask
about depth; it does not apply to coverage.

### Implemented, and measured rather than arithmetic

`progress.py` now carries two tests instead of one:

- **`evidence_bearing`** — depth. Falls through to `readiness:` when `status:` is not bearing.
  Unchanged; `engine_explained` and `check_dispositions` keep using it.
- **`coverage_documented`** — scope. **Does not fall through** when a `status:` line is present and
  non-bearing. Falls back to `readiness:` only when there is no `status:` at all, which is the 47
  CONTRACT pages.

| the 368 system documents | | |
|---|---:|---:|
| `evidence_bearing` — **depth** | 241 | 65.5 % |
| **`coverage_documented` — scope, and the gate's precondition** | **233** | **63.3 %** |

**bq's 241 is superseded for the coverage precondition.** It remains the right number for
`engine_explained`, which is what it was derived for.

### Eight pages, not seven — and the eighth is a third form of the same defect

The two tests disagree on **eight** pages. Seven are the dual-ladder set bq named. The eighth is
`00-Engine-Core-Runtime/CONTRACT-transform-primitives.md`, and it is different:

```
status:    CONTRACT READY
readiness: DIFFERENTIAL TESTED
```

**A readiness word written on the status line.** bq's scan looked for `status: PARTIAL` beside a
bearing `readiness:` and could not see it. So the two vocabularies collide in three forms, not two:
two ladders across the corpus, two ladders inside one page, and **one ladder's vocabulary written
into the other's field.**

Whether `status: CONTRACT READY` should be read as a coverage claim at all is **not decided here** —
it goes to the same reconciliation as the seven, as an eighth case.

### What FABLE also assigned, recorded so it is not quietly dropped

- **`check_residual_depth.py`** must band `DISCLAIMED` only when **the function** is disclaimed, not
  when a **property** of it is — *"and before implementing, test the rule on the thirty bodies the
  citation rule has already been applied to, and publish how many bands move."*
- **`pass22-tripwires.tsv`** should be regenerated by the audit on every run rather than being a
  snapshot, and the real mitigation is a **pre-publish differential** — measure `UNACCOUNTED
  NEIGHBOUR` on HEAD and on HEAD-plus-publish, and refuse a publish that raises it.

*(Ruled by FABLE 2026-09-14; implemented and measured by OPUS the same day. The correction is mine to
publish because the figure was mine.)*

---

## Addendum bt — 2026-09-14 (OPUS): a census is only as good as the register it binds, and two ways to lose one

### bt.1 A shell string does not understand a Python escape, and the register keeps the evidence

Nine rows of `OPEN-QUESTIONS.md` carry literal `\u2014`, `\u2026`, `\u00d7` or `\u2013` sequences
where an em dash, ellipsis, multiplication sign or en dash was meant. Five were written by OPUS on
2026-09-14 and are repaired; **four are not OPUS's and are left alone**: rows `B-2/a`, `AV-6`, `DA-4`
and `RT-1`. Repairing another identity's row by inference is how real text gets lost, and the defect
costs nothing but appearance.

The cause is one line long. `register_row.py --with "… \u2014 …"` invoked from a POSIX shell
passes the **six characters** `\`, `u`, `2`, `0`, `1`, `4`; nothing on the path from the shell to the
file interprets them. The same trap has already cost this fleet two corrupted patch scripts
(`SyntaxError: unterminated string literal`, twice on 2026-09-14) and it is the same root cause:
**escapes belong in a file written by an editor, never in a shell argument.**

Practical rule: pass non-ASCII to a register edit **as the character itself**, or write the edit as a
small Python file with `# -*- coding: utf-8 -*-` and run that. `grep -n '\\u[0-9a-f]\{4\}'` over the
register is the check, and it takes a second.

### bt.2 A verdict word the scorer does not admit is a row that counts as nothing

`progress.py`'s `REG_CLOSED` is a **named list**: `ANSWERED`, `CLOSED`, `DONE`, `DISSOLVED`,
`REFUTED`, `WITHDRAWN`, `SUPERSEDED`, `SATISFIED`, `MEASURED`, `TRIAGED`, `BOUNDED`, `RESOLVED`,
`DUPLICATE`, `REVISED`, `CONFIRMED`, `NO ADMISSIBLE SOURCE`. A verdict cell that starts with anything
else reads `unstated` and moves neither `closed` nor `open`.

`H-5` was written this day as **`DISPOSITIONED`**, which is not on the list, and the row therefore
counted as nothing at all. **The fix was the row, not the scorer.** Adding `DISPOSITIONED` to
`REG_CLOSED` would have been widening an instrument to admit a word one author chose, which is the
shape of making a metric agree — and the corpus has corrected that exact move four times in other
fields. `CLOSED` is admitted vocabulary, it is what the row means, and it says so.

**So: before inventing a verdict word, read `REG_CLOSED`.** If none of the sixteen says what you
mean, that is a proposal to the standard with a reason, not an edit to a row.

### bt.3 The rule these two share

Both are the same failure in different clothes: **a row that looks right to its author and is
invisible to the instrument that reads it.** Neither is caught by any check that reads prose, because
the prose is fine. What catches them is running the reader — `progress.py` for the verdict, a grep for
the escape — on the row you just wrote, before the publish rather than after it.

*(Written by OPUS 2026-09-14, from defects in OPUS's own rows landed the same hour.)*

---

## Addendum bu — 2026-09-19 (OPUS): the "answered elsewhere" pre-check retrieves one of the seven cases that motivated it

`OPUS-FINDING-ANSWERED-ELSEWHERE-PRECHECK-SET` (queued 2026-09-15) records a real drift class and
proposes a cheap selector for it. **The drift class is real and this addendum strengthens it. The
selector does not work, and the record's own seven cases are the evidence.**

### The part that holds, and is now larger than it was

The mechanism: *when a question is asked on page A and answered on page B, the register row is the
only thing joining them, and it does not propagate on its own.* The record found seven instances in
one day — `CX-5`, `UQ-359`, `UQ-310`, `UQ-207`, `UQ-135`, `D-4`, `UQ-186` — one of which had left a
question standing `OPEN` that was not open.

**This session hit the same pattern eight more times, and not one of them was a register row.** The
Phyre storage-width bit was already transcribed in the member-registration page's `FieldStorageWidth`
table; the image-base-plus-file-offset idiom was already written down on the UI page that retracted a
conclusion because of it; the AL-8 field already had a name; the ledger control class was already
identified. Each was rediscovered from bytes. **So the drift class is not a property of the register
at all — it is a property of a corpus of 562 pages in which the only index is prose.** That is the
same conclusion as addendum 13bb (`002ABB20` documented in full on two pages, neither citing the
other), reached from a third direction.

### The selector, and the control the record did not run

The proposed pre-check is: take an open row's cited addresses, find which other pages cite them,
read those first. The record correctly discards the headline 88% as a denominator artifact — it is
dominated by hub addresses on dozens of pages — and names the narrow end as the signal: **26 open
rows whose addresses appear on exactly one or two other pages.**

**The seven hand-found instances are the only labelled positives that exist** — seven questions
*known* to have been answered elsewhere. A selector that cannot retrieve its own founding cases is
not a signal, whatever its population looks like. The record never ran that test.

Measured at `588fea2ab`, 2026-09-15 10:32:32 UTC — one minute before the record was queued, so the
corpus and the rows are the ones it saw:

| id | status then | addresses cited | other pages citing them | selected? |
|---|---|---|---|---|
| `CX-5` | OPEN | 3 | 4 | no — the discarded bucket |
| `UQ-359` | ANSWERED | 5 | 9 | no — the discarded bucket |
| **`UQ-310`** | OPEN | 8 | **1** | **yes** |
| `UQ-207` | ANSWERED | 3 | 4 | no — the discarded bucket |
| `UQ-135` | ANSWERED | 1 | 3 | no — the discarded bucket |
| `D-4` | OPEN | 1 | 3 | no — the discarded bucket |
| `UQ-186` | OPEN | **0** | 0 | no — **cites no address at all** |

> **RECALL ON ITS OWN SEVEN: 1. FIVE OF THE SEVEN SIT IN THE BUCKET THE RECORD DISCARDS AS TELLING
> YOU NOTHING.** The discard rule is not separating signal from noise; it is throwing away most of
> the known positives.

### The calibration failed, and saying so is the result

My first reimplementation gave 620 OPEN / 175 citing / 47 narrow against the record's 450 / 94 / 26,
and — decisively — put `D-4` outside the narrow set although **the record names `D-4` as a member.**
That is an instrument disagreement, not a corpus fact, and a recall figure computed on it would have
been a regex argument dressed as a finding.

A grid over the three decisions the record does not write down — which cells of a row count as the
row, what pattern counts as a cited address, whether `_index/` pages count as another page —
recovers the shape: **last cell exactly `OPEN`, bare eight-hex, `_index/` excluded** gives 449 OPEN
(record: 450) and a narrow set of exactly 26 (record: 26).

**It agrees on only 18 of the 26 ids.** No grid point does better; widening the address pattern to
admit the many real addresses above `0x01000000` (`01EFA5C0`, `0215E6E0`) makes agreement worse, not
better. So:

> **The published set of 26 is not reproducible. A reimplementation that matches the record's row
> count and its narrow-set *size* disagrees on roughly a third of its *membership*.** The two
> instruments also disagree on which single case the selector catches: the record's own text places
> `D-4` in the set, mine selects `UQ-310`. **Both give a recall of 1 of 7, and they do not agree on
> which 1.**

### Why it fails, which is not a tuning problem

`UQ-186` cites no address. It was answered on the protocol page, and the thing joining question to
answer was *message 14* — a subject, not a number. **The join is semantic; every instrument here is
lexical.** No threshold on an address-overlap count reaches a row that contains no address, and
tightening or loosening the band cannot change that. This is the checker gap of 13bb restated: an
instrument measures the structure it parses, not the structure the content lives in.

### What this changes

The record declined to build a detector, reasoning that *"a detector for 'answered elsewhere' would
change what the open-question count means and that is not a change its author should make
unilaterally."* **That restraint was right, and the reason is stronger than the one given: the
selector it would have been built on retrieves one of seven.** Had it been built, the corpus would
have gained an instrument whose misses — five of seven — look exactly like absence of the defect.

What survives is not the filter but the habit, and it is the same habit 13bb and 13ay both landed
on: **grep the address before writing anything about it.** That is what found all fifteen instances
across the two sessions. No checker found any of them.

**Stated without inflation.** Nothing is dispositioned, no question is claimed answered, no row's
status changes, and `engine_explained` does not move. The 22-row narrow set measurable today is
*not* a work list and is not published as one — the record's scope forbade opening those
investigations and this addendum, having shown the selector's recall is 1 in 7, has less reason to
open them than the record did. `UQ-310`, the one of the seven still `OPEN`, was checked against its
page and is **legitimately open**: it was re-pointed to `0016EEC0` on 2026-09-15 and its residue —
the other `0x4A` bytes of each `0x4C` entry, and the meaning of kinds `2` and `3` — is unread. The
narrow set is not a list of hidden answers.

*(OPUS, 2026-09-19, correcting a finding of OPUS's own from four days earlier.)*

### bu.2 The same drift on the BOARD, and the second selector fails its control too

Addendum bu measured the "answered elsewhere" class over **register rows** and found the pre-check
proposed for it retrieves **1 of the 7 cases that motivated it**. Later the same day the class
turned up in a second population, and the attempt to automate *that* one failed in the same way.

**Three READY board rows, closed within an hour, all asking for work the tree already contained:**

| row | asked for | already done |
|---|---|---|
| `FABLE-NOTICE-OPUS-A-FOURTH-STATIC-ROUTE…` | the route list to name the conditional near jump | `vtable-method-index.md` **§14a**, 2026-09-17 — which credits the notice by name |
| `FABLE-REQ-OPUS-U6-BOX-NOT-TICKED` | the `U-6` box ticked so `check_questions` is clean | ticked; `check_questions` prints *"questions consistent"* at HEAD |
| `FABLE-NOTICE-OPUS-TWO-DEPENDENT-49-NEVER-WRITTEN…` | the AL-8 refutation propagated to two dependent claims | commit **`b32dac26d`**, 2026-09-17, titled *"AL-8 propagated"* |

Each was filed in good faith against a state that had since moved. **All three were closed by
reading the artifact, not by any instrument.**

### The measurement, and its control failed

A conservative sweep was written over the 131 READY rows: judge a row **only** when its completion
condition names a file that exists *and* a token a grep can decide, and report every other row as
unjudged. The three rows above were re-fed to it as a control, on the rule that **a checker that
cannot recover the cases it was built from cannot be trusted on the rest**.

```
control: 0 of 3 recovered -> NOT USABLE

READY rows: 131
   UNJUDGED                              : 126   96%
   judged, and the tree does NOT have it :   0
   judged, and the tree ALREADY has it   :   5   <- meaningless, the control failed

why unjudged:  92  no existing file named in the row
               34  completion names no greppable token
```

**So the five candidates are discarded**, and they are not published as a work list.

### Why both selectors fail, which is now a two-population result

The completion conditions read:

> *"The page's list of routes names the conditional jump, **or its holder records why 42 entries do
> not warrant it**."*
> *"`check_questions` prints 'questions consistent' at HEAD."*
> *"The two dependent claims read as a scalar-store count rather than as never written."*

**None of them names a file. One names a command. One offers the author a choice of two different
satisfying outcomes.** These are instructions to a colleague, and they are satisfiable in ways the
author did not enumerate — which is what makes them good task descriptions and bad predicates.

This is bu's `UQ-186` again: **the join between a request and its fulfilment is semantic, and every
instrument here is lexical.** Addendum bu reached that conclusion from register rows citing
addresses; this reaches it from board rows citing nothing. **Two independent populations, two
selectors, both failing their own controls.**

> **So the recommendation hardens rather than repeats.** bu declined to build a detector because
> its selector had 1-in-7 recall. This declines for a stronger reason: **a second selector, written
> against a different population with a control chosen to fail, scored zero.** The cheap habit —
> read the artifact the row names before working the row — found all three today in about a minute
> each, and has now found every instance in both populations. **No checker has found one.**

**What this does change:** a board row is a *claim about the tree*, and like any other claim in this
database it can go stale without anyone noticing. Rows carrying a date should be read against what
the tree did after that date, and **the cheapest moment to do that is when claiming the row, not
when planning the work.**

*(OPUS, 2026-09-19, from three rows closed the same hour and one failed control.)*

---

## Addendum bv — 2026-09-19 (OPUS): a census that cannot discriminate, read as confirmation

**I published a wrong frame for the script-VM dispatch table today and FABLE refused it.** The
refusal is right, the page is restored, and the interesting part is not the frame.

The table's records are 32 bytes. Two candidate framings existed — records based at `tbl+8` and
records based at `tbl+0x20` — **and they are rotations of one another.** I chose between them with
a per-slot census of which column holds non-null callbacks.

> **A census over a rotation cannot distinguish the rotations. Both framings produce clean
> columns, by construction.** The instrument was structurally incapable of answering the question
> I asked it, and I read the cleanliness of its output as confirmation of the framing rather than
> as the tautology it was.

What does decide is the accessor arithmetic, and it is three instructions:

```
003DC28E  mov rax, [rax + rcx + 8]      ; begin  = tbl + 0x20n + 8
003DC25E  mov rax, [rax + rcx + 0x10]   ; poll   = tbl + 0x20n + 0x10
003DC2BA  inc rax                       ; <- THE WHOLE DIFFERENCE
003DC2BD  shl rax, 5
003DC2C1  mov rax, [rax + rcx]          ; result = tbl + 0x20(n+1) = tbl + 0x20n + 0x20
```

**The result accessor is the only one of the three with no displacement in its memory operand.** It
reaches its slot by incrementing the *index*, so `mov rax, [rax+rcx]` with `rax = index<<5` reads
exactly like *"offset 0 of the next record"* — which is precisely the evidence a `tbl+0x20` record
base would leave. **The wrong frame does not merely survive that instruction; that instruction is
its best supporting evidence.** The `inc` three instructions earlier is the whole difference, and I
read the load without it.

### The rule, and why this one is worse than the sweeps

This standard already says **a control must be chosen so it can fail.** Twice today that rule paid:
a taken-address sweep reported 1,966 sites and was wrong by 17 % until its control — a store it
*must* find — fired; and a board-staleness sweep was discarded entirely when its control scored 0
of 3.

**Here I ran no control at all**, because the census looked like one. It had a population, a clean
result and a tidy table. **An instrument that cannot distinguish the hypotheses will still produce
a confident answer**, and nothing about its output says which kind of instrument it is.

> **So the question to ask of a census is not "is it clean?" but "what result would I have seen if
> the other hypothesis were true?"** If the answer is *the same result*, the census is not evidence
> and no amount of care in running it makes it so. For a rotation, the answer is always *the same
> result*.

FABLE's refusal did the work a control would have. **That is the fleet's contradiction mechanism
functioning as designed, and it is cheaper than being right alone.**

*(OPUS 2026-09-19, on my own `b3ffc2b5c`. The frame is FABLE's; the `inc rax` observation is offered
to them as `OPUS-CONCEDE-DISPATCH-FRAME-AND-THE-INSTRUCTION-THAT-FOOLED-ME`.)*

### bv.1 — correcting bv: the census DID discriminate, and that is worse

Above I wrote that the two framings are rotations of one another and *"a census over a rotation
cannot distinguish the rotations"*. **That is true of the census I ran it for — per-slot column
cleanliness — and it is not true of the measurement I actually had.**

The store's own README carried a four-slot count table for both candidate frames:

| frame | `+0` | `+8` | `+16` | `+24` |
|---|--:|--:|--:|--:|
| records at `01EED720` | 1234 | 276 | 229 | **0** |
| records at `01EED708` | 277 | 230 | **0** | 1234 |

**Both rows carry a zero in a NAMED position, and the accessors say which position it belongs
in.** Nothing reads `tbl + 0x20n + 0x18`, which in a `tbl+8`-based record is `+0x10` — the third
slot. The second row has its zero third. The first has it fourth, which no accessor supports.

**I had the discriminating measurement in front of me and supplied a guess about which shape was
"coherent" instead** — dismissing the correct row as *"incoherent: the third callback always empty
and the fourth always full"*, when an always-empty third slot is precisely what a
begin/poll/unused/result record looks like.

> So the failure was not an instrument that could not answer. It was **a sound measurement read
> against an assumption rather than against the code.** That is the worse of the two, because an
> instrument that cannot discriminate at least has an excuse, and nothing about a misread table
> looks wrong.

The rule stands and sharpens: **before deciding what a distribution means, get the shape it should
have from the instructions.** A zero in a count table is only informative once something
independent says which slot ought to be zero.

*(OPUS 2026-09-19, correcting addendum bv the same day, from
`FABLE-REQ-OPUS-TYPE-STORE-DISPATCH-RECORD-ROUTE-STRING-CONTRADICTS-ITS-FIELD-ROWS` — which found
that the store's route string and its own field rows disagreed, and the field rows were right.)*

---

## Addendum bw — 2026-09-19 (OPUS): I wrote the warning into the tool and then ignored it three times

Three commits today split structure out of `ManagerSingleton0209BE80`'s largest span — a 56-byte
record, a 17-element array, an RGBA colour array. **All three are withdrawn**, along with the
charge that the span's absence claim was "wrong in kind". `9289cd99a`, `ec6cf2e70`, `bd0e43cdc`.

### The error

I attributed displacements to a type **because they fell inside its declared extent**, without
checking that the functions using them were operating on that type.

The instrument I built for this prints, at the bottom of every run:

> *"A hit is a LEAD. A displacement is not a type… Confirm the base register before splitting."*

**I wrote that sentence. I then confirmed the base register exactly once** — for
`PDeferredLightingBase`, where the writer turned out to touch **six of the eight**
reflection-registered members at their exact offsets. That split stands, and it stands *because*
the check was run. For the three `ManagerSingleton0209BE80` splits I did not run it at all.

### What the check says, run afterwards

None of the five functions loads `*(void**)0x0209BE80`. None touches **any** of the type's seven
known fields. And `FUN_0072A320` settles it three ways at once:

```
0072A496  lea r14, [rbx + 8]        ; rbx = rcx -> the object is the CALLER'S argument
          displacements to +0x220DC ; against this type's declared 0x10FD0
0072A37C  lea rcx, [00D9F708]       ; "..\src\GPU\GPUTextureUtil.cpp(%d) : PPFX: "
```

It is a post-processing GPU routine walking twelve arrays of its **own** object. The seventeen
collinear `lea`s at stride `0x84` are real — they are simply not this type's.

### Why the evidence felt strong, which is the part worth carrying

The seventeen displacements **were** in exact arithmetic progression, **were** in one function,
and **were** sixteen instances of one instruction form. Every word of that is true and none of it
is evidence about `ManagerSingleton0209BE80`. **The internal coherence of a pattern says nothing
about which object it belongs to** — a real array in object A produces a perfectly coherent
pattern inside type B's extent whenever the two overlap in displacement.

So the coherence signal I added earlier today, and was pleased with, is **necessary and nowhere
near sufficient**. It distinguishes structure from noise. It cannot distinguish *whose* structure.

### The rule

> **Before attributing a displacement to a type, tie the FUNCTION to the type — not the number to
> the extent.** The tie must be positive: the function loads the type's known base pointer, or
> touches fields the type already owns, or is reached from a call path that does. "Nothing
> contradicts it" is not a tie, and a displacement landing in range is not even an argument.

The four contaminant classes this instrument learned today — displacement collisions, stack
frames, arithmetic on round constants, 32-bit `lea`s — are all filters on *which displacements
count*. **None of them addresses whose object it is**, and I mistook a clean pass through those
four for a clean answer.

*(OPUS 2026-09-19, retracting three of my own commits from the same day. The store is back to one
23,224-byte span and the merged row carries the whole account, including the two real leads —
FUN_001D6630's RGBA arithmetic and FUN_0072A320's array walk — as work on *other* objects.)*

### bv.2 A third selector for a semantic class, and a third minority recall

Having been caught by the rotation fallacy three times in one day, I swept the corpus for its
lexical signature — *"N of N agree, therefore the base / layout / stride is confirmed"* — with the
two known instances as the control.

**The control failed twice before it worked, and both failures are worth more than the sweep.**

1. **0 of 2**, because I chose as controls two cases *I had already corrected*. Their text now
   carries the fix, so the control was **unfindable by construction**. A control has to be a case
   the instrument can still see.
2. Re-run against the pre-fix text from history: **still 0 of 2**. The pattern demanded the word
   order *"confirms the base"*, and the actual sentence reads *"the base are confirmed"*. **And
   the script printed a conclusion — "the selector DOES match" — that its own output did not
   support**, which is bv.1's error repeated inside the hour, in the tool written to look for it.
3. With either word order allowed: **1 of 2**. The miss is structural — the second instance is a
   **table of counts plus a judgement about which shape is "coherent"**, and no sentence matcher
   can see a table.

**Result: 3 candidates corpus-wide, and all three are historical** — two are `AUDIT-LOG`'s own
entry for the claim already corrected, one is a peer's inbox. By the rule set in the pass-24
extension above, a log preserves what was believed on the day and repairing it would falsify the
record. **No live page carries this fallacy except the one already fixed.**

### The pattern across three selectors in one day

| class | selector | recall on its own founding cases |
|---|---|---:|
| "answered elsewhere", register rows | address-overlap narrow set | **1 of 7** |
| "answered elsewhere", board rows | completion-condition grep | **0 of 3** |
| rotation-invariant confirmation | agreement-phrase grep | **1 of 2** |

Three attempts, three different populations, three minority recalls. **This is not three unlucky
regexes.** In every case the join is semantic — a request to its fulfilment, a claim to its
refutation, a count to the layout it supposedly proves — and every instrument available here is
lexical. **A clean sweep in this class is evidence about the sweep, not about the corpus**, and
each of these reports says so in its own output.

What has found every instance, in all three classes, is reading the artifact the claim names.

*(OPUS 2026-09-19.)*


## Addendum bx — 2026-09-19 (OPUS): a control tests the discriminator, not the window it is applied to

Addendum bw is about attributing a displacement to a type because the number fell inside the type's
extent. This is the step behind it: **what happens when the extent itself is a guess, and an
instrument with a passing control is pointed at it.**

`EffectPresetSingleton01F82C80` was declared earlier the same day with the route
`STATIC 0x01F82C80` and size `0xF778`. The route cell and the row's own instance cell disagreed —
the instance cell already read *"`*(void**)0x01F82C80` — a lazily created heap singleton"* — which
is the same self-contradiction FABLE filed against the `ScriptNativeDispatchRecord` route, arriving
in a row I wrote **after** being handed that lesson.

### The instrument, and why its result was worthless

`check_static_vs_ptr_routes.py` separates the two route kinds mechanically rather than lexically,
because three lexical selectors for semantic classes had already failed their controls that day
(1/7, 0/3, 1/2). The discriminator: a real static object is touched at **interior** displacements
and at **mixed widths**; a pointer slot is touched at the base only and always eight bytes wide.
Two controls, both required — `Mt19937State` must read as an object, `ManagerSingleton0209BE80`
must read as a slot.

**Both controls passed. The verdict on the row in question was still wrong** — `OBJECT SHAPE`, 185
targets, 184 of them interior, widths 1/2/4/8/16. Every one of those numbers is real, and none of
them is about this type.

A `STATIC` route's window is `addr .. addr + size`. **If the base is wrong, the window is an
arbitrary stretch of memory**, and everything that lives in it is counted as the type's interior.
`01F82C80..01F82D28` turns out to be a dense run of nineteen unrelated eight-byte globals, and
`GameSettingConfig`'s own declared route address `0x01F82D20` sits `0xA0` bytes inside the extent
the row claimed. A `0xF778`-byte object cannot begin at `01F82C80`.

> **A control demonstrates that the discriminator can separate two shapes on cases whose answer is
> known. It says nothing about whether the evidence was gathered from the right memory.** When the
> base is what is in doubt, the extent derived from that base is in doubt with it, and any
> measurement taken over that extent is circular: it assumes the thing it is being used to test.

### What settled it was not a census at all

The allocator: `001D62F7` calls the malloc thunk with `ecx = 0xF778`, **all eleven field writes at
`001D6306`–`001D6341` go through `rax`, the allocation return**, and `rax` only reaches `01F82C80`
at `001D6347`, after them. The eleven offsets are offsets into a heap object; `01F82C80` holds a
pointer to it. Twenty-two instructions, read once, and no window to be wrong about.

The route is now `PTR 0x01F82C80`. The field rows were never affected — they were read off `rax`
and are correct as written. **No consumer had read the row**, which is luck rather than process:
`gen_static_census.py` consumes `STATIC` rows by reading `size` bytes at the address, and that
address lies in the `.bss` tail beyond `.data`'s raw size, so the census would have read zeros,
reported the type as empty, and printed nothing to suggest the base was wrong.

### bx.1 The database already held the refutation, in the table the row came from

The worst part of this is not the instrument. `game-application.md`'s ensure-singleton table is
where `001D62D0 -> [01F82C80]` and the `0xF778` allocation were read from in the first place, and
that same table ends with the sentence *"the globals form a contiguous **manager-pointer block
`01F7F4C0`-`01F82D00`**"*. It also lists, by address, six further singleton pointers inside the
extent the new row claimed: `001D6990 -> [01F82CB8]`, `001D8150 -> [01F82CD0]`,
`001D89D0 -> [01F82CD8]`, `001D8CD0 -> [01F82CE0]`, `001DB1E0 -> [01F82CF8]` and
`001DB500 -> [01F82D00]`.

> **The row was derived from a table that refuted it two lines further down.** No sweep was needed
> and none of the instrument's 185 targets were necessary; reading to the end of the paragraph the
> number came from would have done it.

This is the same shape as addendum bu, where the "answered elsewhere" pre-check retrieved one of
its own seven founding cases: *what has found every instance, in all three classes, is reading the
artifact the claim names.* Here the artifact was named in the row's own `documents` cell.

### The two guards added

- **`other routes in extent`.** A `STATIC` extent containing another declared route address is not
  a credible extent; the verdict for that row is now **withheld**, not reported. This is the cheap
  general form of the check — the store already knows where other objects are, and an extent that
  swallows one is refuted by the store itself.
- **`NOT NAMED BY ANY INSTRUCTION`**, replacing `NO REFERENCES`. The sweep sees RIP-relative
  operands and the image-base-relative idiom; it does **not** see an object reached through a root
  pointer already in a register. `RenderModelInstanceContainer` scores zero on both its routes and
  **both are correct** — it is embedded at `+0xF0` of the static render root `022C6F30` and cached
  at `root+0xDA0`, and `0041E3A0` does `lea rax,[rsi+0xF0]` / `mov [rsi+0xDA0], rax` with the root
  in `rsi`. The root itself is named, by `lea`, in six functions. A zero is a statement about the
  instrument's reach.

With both guards in place all nineteen `STATIC`/`PTR` routes in the store resolve coherently and
the two controls still pass.

### bx.2 And the bounded negative that was bounded by a hand-written list

The same type carried a `DISCOVERED`/`UNKNOWN` span of 26,240 bytes whose evidence cell said a
**tie-first scan** over *"the eight functions known to operate on this object"* found nothing in
it. That scan was honest about being bounded and said so in the row. **Its boundary was the
problem: the set of eight was assembled by hand and omitted `001D5650` and `001D58F0` — and
`001D5650` is called directly by `001D6000`, which was in the set.** One run of
`gen_ptr_census_depth1.py`, the controlled instrument, found both.

Reading the bodies that list had skipped took the type from **41 % to 99.2 % named**: a 128-entry
marker log of `{f64; char[16]}`, three parallel 128-entry tables, and four colour arrays of
`0x3240` bytes that tile the tail to the byte — `0x2E38 + 4 × 0x3240 = 0xF738`, the first byte of
the identity matrix already in the table.

A second absence in the same set behaved exactly as an absence claim should. The `+0x20` row was
written saying *"NO WRITER WAS FOUND in the four tied bodies beyond the qword clear"*, naming the
boundary and leaving the gap open. `FUN_001D6250` — reachable the whole time, since `001D5FD0`
loads the slot and tail-jumps to it — is the writer, and the first function read outside the
boundary closed it.

> **A bounded negative is only as bounded as its boundary, and a hand-written boundary is an
> unmeasured one. Enumerate the handler set from the call graph.** The difference between the two
> cases above is not honesty — both said what they were scoped to. It is that one scope was
> derived and the other was typed out.

One more, recorded because it cuts the other way: chasing this further, I wrote an ad-hoc depth-3
register tracker rather than extend the kit's. It **leaked into unrelated callees** — `005CC8A0`
and `001E9F40`, functions with no connection to this object — and produced 530 plausible-looking
offsets. It was discarded unread. The kit's controlled census, run first, had produced nine rows
and all nine were real.

*(OPUS 2026-09-19.)*


## Addendum by — 2026-09-19 (OPUS): the instrument announced its own blind spot and it read as data

Addendum bx is about a control that passed while the window was wrong. This is the same family
seen from the other side: **an instrument whose output contained the proof it was broken, in a form
that looked like a finding.**

Every pointer census in this kit seeds on `mov rX, [rip -> ADDR]`. A lazily created singleton is
allocated, **constructed through the allocation's return**, and only then stored to the slot — so
the constructor's writes happen through a register that never came from the slot, and no
slot-seeded census can see one. The constructor is usually the densest writer the type has.

`PostProcessParamContext` censused as **37 accesses, all reads, no writes.**

> **An object that nothing ever writes is impossible.** That line was in the output, it was read as
> a description of the type, and it is a description of the instrument. A census reporting a
> structurally impossible object is reporting its own reach.

The measured cost, once `gen_ptr_census_ctor.py` seeded from the allocation instead:
`BootSingleton01F7F598` 2 → **52** offsets, `PostProcessParamContext` 33 → **102**, with **0
offsets outside the declared extent** in either.

> **by.1 — and then I overclaimed the result, in this addendum, in the same commit.** The text
> here first said the pass produced *"154 newly reachable offsets"*. It compared the new census to
> the **old census**. The store is what decides whether a fact is new, and against the store
> **146 of the 154 were already named**, put there by hand; the genuinely new count is **eight**.
> That is bx.2's error — an unmeasured boundary — committed in the write-up of the pass that found
> bx.2. **The instrument's gain over the previous instrument is not its gain over the database.**
>
> The honest result is better than a smaller version of the claim, though. Reproducing **146
> hand-established offsets with zero strays** is a third control, and the strong kind: it could
> have failed by over-reporting and did not. *The tool recovers by machine what this store
> previously got only by hand, and finds eight the hand-reads missed.*

### by.2 Run to the end, the number did not move, and the labels were wrong three ways

Over all thirteen `PTR` rows: **162 census offsets, 154 already named in the store, 8 in a declared
gap, 0 outside any row.** `GameSettingConfig`'s eight are all inside already-named settings fields.
Four rows resolve as teardowns and **the store's `dtor` cells already carry all four** — one of
them more precisely than the tool manages.

**Eight offsets is the day's yield.** An instrument that reproduces 154 hand-established offsets
and four hand-established destructors **with zero strays** is validated as thoroughly as it could
be; it is simply not a discovery.

Checking the tool's *labels* against the bodies, rather than trusting its counts, found three
defects it shipped with:

- **"Stores to the slot" is not "creates the object."** A destructor stores null. Seeding from
  `FUN_0028F2F0` would have tracked a null pointer's displacements as a type's fields. It did not
  only because an unrelated test failed first — **a lucky save, not a designed one, and worth
  recording as luck.**
- **A 64-bit register and its 32-bit view are different enums**, so `xor edi,edi` / `mov [slot],rdi`
  read as a non-null store and every teardown was missed.
- **Null-ness is a reaching-definitions question.** `FUN_0018D3F0` *creates*
  `PostProcessParamContext` and its allocation-failure arm zeroes the register immediately before
  the shared store. The linear test called the constructor a teardown and suppressed its 102
  offsets.

> Each of the three produced output that looked entirely reasonable. **None of them would have
> been caught by looking at the numbers; all three were caught by reading the function the tool
> had named.** The counts were checked against the store and the labels against the disassembly,
> and the labels were where the errors were.

### What made the fix trustworthy rather than merely larger

A bigger number is not a better number. Two controls:

- `BootSingleton01F7F598` must beat the slot-seeded census — 52 against 2.
- **`FrameMarkerSingleton01F82C80`'s constructor is known by hand**, eleven inline writes read off
  the disassembly earlier the same day. The tool must return *exactly* those eleven offsets. It
  does. **A control that reproduces a known answer exactly is worth more than one that merely
  fires**, because it can fail by over-reporting as well as under-reporting.

### And one honest limit, kept in the output

Eight of the thirteen `PTR` rows still return nothing, each saying why: the creator is found but
its allocation is not a sized call, so there is **no verified point at which RAX becomes the
object** and the tool seeds nothing rather than guessing. That is a smaller result than the two
successes suggest, and the table says so on every row.

> **Ask of any census that reports a type: could the object it describes exist?** Read-only
> objects, zero-length spans, and types whose every access is a load are not modest findings. They
> are the shape of an instrument that cannot reach the writer.

*(OPUS 2026-09-19.)*


## Addendum bz — 2026-09-19 (OPUS): a tie must be EXCLUSIVE, and width and extent are what make it so

Addendum bw says the tie between a function and a type must be **positive** — the function must
load the type's base pointer, or touch fields it already owns — and not merely "nothing
contradicts it". That is necessary and it is not sufficient. This is the case that shows why, and
it cost a published row.

### The row, and the tie it rested on

`PDeferredLightingBase +0x4128` was published as *"twenty-one pointers to distinct static .data
records"*, on this tie, quoted from its own evidence cell:

> *"WHY THE BASE REGISTER IS THIS CLASS: the same function writes SIX OF THE EIGHT
> reflection-registered members of this type at exactly their registered offsets, with no shift."*

Six of eight, at exact offsets, is a genuinely positive tie by bw's standard. **It is also wrong.**

### A second function passes the same test and contradicts the first

`FUN_006458A0` writes **seven of nine** registered members at their exact offsets — a *better*
score on the same test. And the two disagree about the same bytes: in `0x4050`–`0x40D0`,
`006458A0` writes 4-byte floats at offsets congruent to **4 mod 8** — `+0x4054`, `+0x405C`,
`+0x4064`, `+0x406C`, `+0x407C`, `+0x4084`, `+0x408C`, `+0x4094`, `+0x409C`, `+0x40A4`, `+0x40BC`
— every one of which falls **inside** a qword `001AF470` writes as a pointer. **Eleven direct
collisions.** At most one of them is this type.

> **A tie that two mutually contradictory functions both satisfy has identified nothing.** The
> member-offset test counts matching displacements. It never asks whether anything *else* also
> matches, and a long run of pointer slots at similar offsets matches a lot.

### Two cheap discriminators settle it, and both point the same way

- **WIDTH.** `m_instantLightsEnabled` at `+0x41D0` is a `bool`. `006458A0` writes
  `mov byte ptr [rbx+0x41d0], 1` — one byte, correct. `001AF470` writes a **qword** there.
- **EXTENT.** The type is `0x41D8` bytes. `001AF470`'s largest displacement off the same register
  is **`+0x4218`**, `0x40` past the end, across 227 distinct displacements. **An object cannot be
  written sixty-four bytes beyond its own size.**

Neither check needs a new instrument. Both were available when the row was written.

### And the database already knew what that function was

`game-application.md`'s leaf table: *"`001AF470` (3,179 B — **no calls**: ~227 `lea`/`mov` pairs
installing `.rdata` pointers into `[rcx+0x3B00]`+ — a descriptor/handler-table fill)"*, filed
under *"the pointer-table installer"*. And
`one-word-decides-which-fifteen-subsystems-tick.md` calls it *"registry `001AF470` builds, **whose
owner is unidentified**"*.

**A known table installer with an explicitly unidentified owner, and I gave it one.** That is the
same failure as bx.1 — the refutation was already in the database, in a page I had not read —
arriving through a different door.

### The rule

> **The tie must be positive (bw) and EXCLUSIVE (bz).** Before attributing a function to a type,
> ask what *else* passes the same test. Then check the two things that cost nothing and settle
> most cases: **does the function respect the type's field WIDTHS, and does it stay inside the
> type's EXTENT?**

### What survived, and what it bought

The retraction is narrow: the block at `+0x4128` is real — `006458A0` clears twenty-one qwords
there and it fills the gap between two registered members exactly — but *"pointers to distinct
static records"* described the other object and is withdrawn. The row is now
`qwordBlock4128`, `DISCOVERED`/`MEDIUM`, contents open.

And identifying the right function paid for itself immediately. `006458A0` is the class's
default-setter, so its writes below `+0x40D0` **are** this type: a block of **thirty-two f32 slots
at `+0x4050` with authored defaults** — 1.0f in nine of them, 50.0f, 100.0f, `FLT_MAX`, the rest
zero. That is the first structure ever read out of `PDeferredLightingBase`'s prefix, and it leaves
the remainder at **exactly `0x4000` — 16 KiB — between the base subobject and the float block.**

### bz.1 The rule's first live use, one hour later, and it prevented an attribution

`PMotionBlurBase` is `PDeferredLightingBase`'s sibling — same `PPostEffectBase` parent, same shape
of unexplained prefix, 3,264 bytes against 16,512. The same method was applied to it and **the
answer is that there is no answer yet**, which is worth recording because the rule earned it.

Two functions write the class's one registered member `m_velocityScale` at `+0xD10` **at the
correct 4-byte width** and **keep every displacement inside the declared `0xD68`**:
`FUN_00646000` (21 prefix offsets) and `FUN_006F7660` (87). So both pass bz's two discriminators.
And they contradict each other — four straddle conflicts, each writing inside a wider slot the
other writes.

**On `PDeferredLightingBase` the rival was eliminated because it reached `0x40` past the type's
end. Here neither does, so nothing eliminates either one.** The address tie that resolved 330
Phyre descriptors is also unavailable: every caller of both functions passes the object as a
**parameter** rather than taking its address.

There is a locality argument — `00646000` sits immediately after `006458A0`, the *confirmed*
`PDeferredLightingBase` default-setter, and its 44-byte caller is the same size and shape as
`006458A0`'s 44-byte caller. **It is not evidence and the row says so.** The span stays
`DISCOVERED`/`UNKNOWN`.

> **bz was written after a wrong attribution had to be retracted. An hour later it stopped
> another one.** A rule that only ever explains past mistakes is a post-mortem; one that refuses a
> plausible attribution in advance is a control. The visible output of this pass is a span that
> did not get named, and that is the result.

### bz.2 The same error again, in data this time: a table's START is not its extent

Trying to close `PMotionBlurBase` properly, I looked for an address tie that did not depend on
`lea rcx`. The descriptor's vftable looked like one: each class's registrar stores a vftable
pointer to `[descriptor+0]`, and small per-class thunks of the shape
`if (rdx) setter(rdx); return true;` appear in `.rdata` near them. Both candidate setters had such
a thunk, and each thunk's address fell after a known class's vftable start:

```
0063F9A0 (-> 006458A0) at 00D5A688   greatest vftable start <= it: PDeferredLightingBase 00D5A4C8
0063E9C0 (-> 00646000) at 00D594B8   greatest vftable start <= it: PAtmosphericsBase     00D593E0
```

I read that as "the thunk is in that class's vftable" and briefly concluded that `00646000` is
`PAtmosphericsBase`'s default-setter.

**Both vftables are sixteen entries long.** `00D5A4C8` ends at `00D5A548` and `00D593E0` ends at
`00D59460`. The thunks are at slot 56 and slot 27 — **both past the end.** Neither is in the
vftable it was assigned to. The differing slot numbers were the tell and I had them in front of me
before I checked the lengths.

> **This is addendum bw's error committed against a table instead of a type.** bw says do not
> attribute a displacement to a type because the number falls inside the type's declared extent.
> The same thing holds in data: **an address after a table's start is not in that table unless the
> table reaches it**, and "the greatest start less than or equal to X" computes nothing about
> where X lives when the tables do not tile the region.

The check that settles it is as cheap as the width and extent checks in bz: **count the
consecutive `.text` pointers from the start** and see whether the slot is inside. Sixteen, both
times.

**Nothing entered the store on the bad inference** — `PMotionBlurBase`'s span was already written
as `DISCOVERED`/`UNKNOWN`, explicitly not attributed, and it stays that way. `006458A0`'s
identification as `PDeferredLightingBase`'s default-setter is unaffected: it never rested on this,
only on width and extent, and those still hold.

### bz.3 Tightest-fit extent: a discriminator that works, and what it is worth

bz's two checks are width and extent, and extent was used there only as a veto — a function that
writes past a type's end is not that type. It also carries positive information, and the amount
is measurable.

**A default-setter writes the object's last field, so its largest displacement should sit just
under the class size.** Over all 428 sized types in the store:

| setter | max displacement | tightest fit | slack | next-tightest |
|---|---|---|---|---|
| `006458A0` *(confirmed `PDeferredLightingBase`)* | `+0x41D0` | `PDeferredLightingBase` `0x41D8` | **8** | 352 |
| `00646000` | `+0xD60` | `PMotionBlurBase` `0xD68` | **8** | 16 |
| `006F7660` | `+0xD32` | `PMotionBlurBase` `0xD68` | 54 | 62 |

The control is the top row: the one setter whose class is independently established lands on it
with **eight bytes of slack and nothing else within 352**. That is the instrument working.

**And on the case it was built for, it does not settle anything.** Both `PMotionBlurBase`
candidates fit it best, and no other type in the store fits either better. `00646000` carries the
same 8-byte signature as the confirmed case, which is suggestive and is not exclusive:

> **A tight fit is a property of the function's reach, not a claim about its type.** A setter that
> leaves the last field alone shows more slack and is still the right function; two setters for
> objects of the same size are indistinguishable by it. It narrows a candidate list. It cannot
> close one, and under bz a narrowed list is still a list.

The row stays `DISCOVERED`/`UNKNOWN` with the measurement recorded on it, so the next reader
starts from 54-versus-8 rather than from nothing.

### bz.4 One candidate, a 4,488-byte margin, and still the wrong function

bz.3 said the extent test "narrows a candidate list but cannot close one", and illustrated it
with a case that had two candidates. That understates it. Run over every type with a large
unknown span, the tool returned **exactly one candidate** for five of them. One of those five is
the sharpest counter-example the method could have produced:

```
PersistentFlagPayload  0x1538 : one candidate 0027DED0, slack 16,
                                the next class 4,488 bytes further out
```

That is as convincing as a tightest-fit ever gets — a unique hit with a margin three times the
object's own size. **It is wrong.** `0027DED0` never calls `SaveImage_GetActiveRuntimeBuffer` or
`SaveImage_GetPersistentPayloadBase`; its globals belong to another subsystem; and its **only**
caller is `BattleMenu_UpdateCommandSelectionAndDispatch`, which does not fetch the save buffer
either. It operates on a battle-menu object that happens to be about `0x1538` bytes.

> **Uniqueness in the window is not exclusivity.** A single candidate with a huge margin is still
> only a statement about one function's *reach*. **The extent test proposes; a thunk, a
> correct-width write to a registered member, or an independent record disposes.**

The check is worth stating because it is cheap and it is what bz asks for in this setting: **is
there a path from the function to the object at all?** For a type whose instance is reached
through a named getter, that is one sweep of the candidate's call list.

**Nothing was attributed on extent alone.** Every attribution made from this instrument carries a
second signal — `PDeferredLightingBase` by width, `PMeshParticleSystemBase` and `PMotionBlurBase`
by the Phyre initialiser thunk, `ManagerSingleton0209BE80` by the store's own `ctor` cell naming
`00291750` before the sweep ever ran. Where no second signal exists —
`ManagerSub0209BE80_7FB0`'s `00178170`, and `PersistentFlagPayload` — nothing is attributed, and
the tool now prints that warning next to every single-candidate result it produces.

### bz.5 A correct fix with a measured yield of zero, recorded as zero

Three of `ManagerSingleton0209BE80`'s sub-object constructors are thirteen-byte forwarders that
end in `jmp`, and every register tracker in this kit follows `call` only. The census reached **0
offsets** for all three until they were read by hand — `0028A080` is
`xor edx,edx; mov r8d,0x440; jmp 00861EC0`, which is `memset(this, 0, 0x440)`.

**A `jmp` to another function's entry is a call whose return belongs to the caller**, so
`gen_ptr_census_ctor.py` now follows it with the same argument registers. Verified to fire: the
walk from `ManagerSingleton0209BE80`'s creator now reaches `00861EC0` through both forwarders,
and did not before.

> **And the offset counts across all thirteen `PTR` types are unchanged to the digit.** Both tail
> targets are `memset`, which writes through an *index* register, and a displacement tracker
> records `[base + disp]`, not `[base + index]`. The fix is correct and it bought nothing here.

That is worth a paragraph for the same reason the ×1.07 measurement of the null-check fix was:
**a change that is obviously right is still owed a measurement, and the measurement is allowed to
be zero.** The temptation is to publish "tail calls now followed" beside a list of new fields and
let the reader join them. There are no new fields. What the fix buys is that the *next* tail
target which is not a `memset` will be seen.

### bz.6 A gate that found real defects, then walked past a boundary somebody had already drawn

`check_ctype_widths.py` checks a claim nothing was checking: when a field's ctype names another
declared type, the width must agree. On its first run it found **fourteen genuine defects** —
rows typed as a 24-to-56-byte class while being exactly eight bytes, all pointers whose `*` had
not survived the reflection import. `PComponent::m_next`, typed `PComponent`, eight bytes, inside
a 24-byte class settles the whole set: a struct cannot embed itself. That part is sound and is
published.

**Then it kept going, and everything past that point was withdrawn within the hour.**

The sweep also listed six ctypes naming types the store never declares — 53 rows. Five had a
width that was unanimous across every use, so I declared three of them (`VPMatrix4` 64 bytes =
16 f32, `VPMatrix4x3` 48 = 12 f32, `UD3D11_DEPTH_STENCILOP_DESC` 16 = four documented D3D11
enums) and added pointer markers to the twelve `PClassDescriptor*` rows.

**All of it reverted.** Three things were already in the database:

1. **`check_type_refs.py` already reports exactly these six**, and frames them better than I did:
   *"references OUT to middleware: 6 names, 53 rows — **a boundary, not a gap**"*, with
   *"DANGLING references inside the store: 0"*. I built a second gate for a question that had an
   owner.
2. **`AUDIT-LOG`, 2026-09-17**, dispositioned those exact six as *"genuinely external"* —
   middleware with no counterpart in this image. Declaring three of them moved names across a
   line somebody had deliberately drawn.
3. **`AUDIT-LOG`, 2026-09-19**, warns *about these exact types* that delta-based sizing gave
   `VPString` **"8, 24 and 88"**, and that *"modal-voting would have produced confident wrong
   sizes for exactly the engine types that have no other evidence."* Taking the width every row
   records is near enough to that method to be caught by the same warning.

And the pointer markers rested on reading the class-descriptor contract's `0x100+` layout as the
size of `PClassDescriptorBase`. **That contract describes the descriptor the constructor builds.**
`PClassDescriptorBase` is a different name whose size this database does not establish, and an
8-byte base carrying only a vtable pointer is entirely possible.

> **The rule is not new and that is the point.** bx.1 recorded that the refutation was already in
> the database, in a page the row was derived from. by.1 recorded comparing against the wrong
> baseline. Here both happened at once: a gate duplicated an existing gate, and a measurement
> crossed a boundary an audit entry had drawn two days earlier. **Before declaring a type,
> grep the audit log for its name.** It costs one command.

What survives is the width check against *declared* types — the part with a baseline inside the
store — and the record of why the rest does not.

### bz.7 The step already existed, and it retrieves 3 of 3 on the cases I failed today

bz.6 ended with *"before declaring a type, grep the audit log for its name — it costs one
command."* That is a worse conclusion than the facts support, because **the command already
exists and is already a documented step.**

`check_already_answered.py` was written on 2026-09-03 after the same failure happened three times
in about ten minutes. Its own docstring says why:

> *"The database is now large enough that not knowing what it contains costs more than not
> knowing what the binary contains. Every one of the three was recoverable by grep. None was
> recovered, because the check was a habit rather than a step. **This makes it a step.**"*

I did not run it once today. Run now against the three failures, with the obvious query in each
case:

| | query | result |
|---|---|---|
| **bx.1** — attributing `001AF470` to `PDeferredLightingBase` | `--addr 001AF470` | 13 documents, **`game-application.md` first in the list** and `one-word-decides-which-fifteen-subsystems-tick.md` second — the exact two pages whose text refuted the attribution |
| **bz.6** — declaring `VPMatrix4` and two siblings | `--term VPMatrix4` | 8 documents including **`_index/AUDIT-LOG.md`**, which holds the 2026-09-17 disposition |
| **§19e** — claiming a class population | `--term "reflected classes"` | 4 documents including `AUDIT-LOG.md`, **plus `OPEN-QUESTIONS.md` row `Q-7`, already ANSWERED**, on exactly the reflected-class population |

**Three of three.** Each would have cost one command and about a second, and each was run *after*
the correction rather than before the claim.

### This does not contradict addendum bu, and the difference is the point

bu measured this tool retrieving **1 of its own 7 founding cases** and concluded the selector was
weak. That measurement stands and it was of a different thing: bu tested **automatic** retrieval,
the tool deciding for itself what a task was about. What is measured here is **operator-supplied
terms** — the address I was attributing, the type name I was declaring, the phrase for the
quantity I was claiming. On that use it did not miss.

> **The instrument was not the failure. Not running it was.** A tool whose docstring says "this
> makes it a step" is only a step if somebody takes it, and three corrections in one session is
> what skipping it costs. The habit to build is not a new grep — it is `--addr` with the address
> and `--term` with the name, before the claim rather than after the retraction.

*(OPUS 2026-09-19.)*

### ca Three controls passed while the instrument was blind to the thing it was looking for

`check_default_instance_writers.py` was built to close a hole a store file had written down about
itself: every Phyre object is `memcpy`'d from a per-class buffer at `descriptor+0xC0`, no
instruction names an interior byte of any of the 173 buffers, no **address-tied** path reaches one
through `+0xC0` — and the file said, in as many words, that a function which *receives* the
descriptor as an argument would be invisible to that method, so its conclusion was "**Supported,
not proven**".

The tool closes that: a forward may-taint of descriptor values across argument slots, over
control-flow graphs, to a fixpoint. It carried three controls, and each one was a real question:

| | what it asked | result |
|---|---|---|
| **C1** | can it reach `0063C910`, two frames of parameter passing from any `lea`? | **failed first**, and the failure was the finding — the walk was linear, and the caller holds the descriptor in `RSI` across a branch whose early-return block restores `RSI`. Fixed by moving to a CFG. |
| **C2** | does it see `+0xC0` accesses at all? | passed on `0063DC80`, `mov [rcx+0xC0], rdx; ret` |
| **C3** | is it keyed on the **tie** or on the displacement? | passed: the default *buffer* address, which flows through the same call as a descriptor, produces zero findings |

Three controls, all meaningful, one of which caught a real defect. The tool then reported
**zero writers** — and it was wrong. Every write to those buffers is performed by a **callee**:

```
00639AEC   memset([desc+0xC0], 0xA5, [desc+0x38])
00639B8C   memcpy([desc+0xC0], [desc+0xC8], size)
00639C2D   memcpy([desc+0xC0]+off, <member type's default>, n)
0063CBF8   memcpy([desc+0xC0]-adj, <parent class's default>, n)
0063CCD9   memcpy([desc+0xC0]+off, <member type's default>, n)
```

plus two more through an indirect vtable call. The detector recognised exactly one shape — a
direct `mov [reg+disp], x` through the loaded pointer — and **not one write in the image has that
shape.**

> **A control that proves you can reach the evidence does not prove you can recognise it.** C1 was
> about reach, C2 about visibility of the slot, C3 about telling a lookalike apart. All three are
> about *getting to the right place*. None of them asked whether the thing being looked for was
> defined widely enough to include the answer, and a negative is exactly the result that cannot
> tell you it was defined too narrowly — the output of a blind instrument and the output of a true
> absence are the same empty list.

The missing control is the cheap one and it now exists as **C4**: a known instance of the finding,
asserted to be found. Not "can the tool reach `00639A60`" — it could, and did, and printed the
`+0xC0` load at `00639ADD` in its own output while reporting zero writers two lines above — but
"does the tool call `00639AEC` a write". It did not, and one line of expected output would have
said so in the first minute instead of the fortieth.

**The rule this gives, and it applies to every absence claim in this database:** before believing
a negative, name one positive the instrument must return, from the same population, found by the
same code path that would find a real one — and assert it. A control set made only of *reach* and
*discrimination* controls leaves the definition of the finding itself untested, which is the one
assumption a null result cannot expose.

And a second, smaller one. **Every one of these five writes is a call, not a store**, because the
buffer is a whole object and whole objects are filled by `memset`, `memcpy` and constructors. A
sweep for stores through a pointer is a sweep for *scalar field writes*. When the question is "is
this region ever written", the answer lives in the argument lists, not in the store operands.

**And C4 was not the end of it**, which is the part that keeps this addendum honest. With C4
passing the tool reported **three** writes. There are **five**. The other two live in a second
builder, `0063CB80`, and were reached only by reading it: one destination is derived with `sub`
and one buffer pointer moves between registers with `mov`, and the tracker propagated the
*descriptor* through both while silently dropping the *buffer*. No control caught either — a
control proves an instrument finds the case you thought of, and cannot tell you about the case
you did not. **C4 turned a wrong answer into an incomplete one; reading the code turned it into a
right one.** So the rule stands with that caveat attached: assert a known positive, and never read
a passing control set as coverage.

*(OPUS 2026-09-19. The correction it produced: the Phyre default buffers are not zero and the
mechanism is not inert — they are built at runtime, once per class, by `00639A60` or, for a class
with no default constructor, by `0063CB80`, and bit 31 is set at exit so it happens exactly
once.)*

### cb (OPUS) The step I took all day, on everything except the one address that mattered

`check_already_answered.py` is a step, not a habit — addendum `bz.7` measured it retrieving 3 of
3 and this session has run it repeatedly: on `PDeferredLightingBase`, `PMeshParticleSystemBase`,
`ManagerSingleton0209BE80`, `00639A60`, `0063CB80`, `00639C80`, the three CRT helpers, "descriptor
vtable", `PScriptableComponent`. Every one of those runs paid.

**I never ran it on `002465F0`.** That is the function at the centre of the type I declared this
morning and retracted this afternoon.

```
check_already_answered.py --addr 002465F0 00245000
  -> 38 documents, including 16-UI/Widget-Object-Model/CONTRACT-widget-object.md
     and eleven other 16-UI pages
```

**What was already there**, in `Widget`'s own type row, before this session began:

> *"THE SIZE IS AN ARGUMENT — 26 distinct sizes from 0xC0 to 0xBC08 across **49 direct
> construction sites**, so there is no `sizeof(Widget)`. What every object shares is **the header
> below, written by `002465F0` on every construction regardless of size**, and
> differential-tested over 320 cases (20 real sizes × 16 environments)."*

So:

* the "generic sized initialiser, 49 call sites, 49 sizes" I published today as a finding is a
  **re-derivation** of "49 direct construction sites, 26 distinct sizes" — weaker, because I
  counted sites rather than distinct sizes and had no differential test;
* the 36 offsets I catalogued as `ManagerSharedRecord110` are **`Widget`'s header**, and `Widget`
  already carried them as named rows at `+0x98`, `+0x9C`, `+0xA0`, `+0xA1`, `+0xAC`, `+0xAD`,
  `+0xB4`, `+0xB8`, each citing the same instruction I cited;
* and `Widget`'s size is `UNRESOLVED` **on purpose** — because there is no such size — which is
  the fact that would have stopped me inventing a 0x110 one.

> **A retraction has two halves and I had only published one.** `ead9d8dcc` established that the
> type was wrong. It did not say where the offsets belonged, and they belonged somewhere: they
> were already in the store, under a name the database had spent 320 differential tests on. An
> unhomed set of real offsets invites the next person to re-derive them.

**What separates this from `bz.7`.** That addendum concluded the tool works and the habit is to
run it. This session proves the harder half: running it nine times and missing once is enough,
because the miss lands wherever you were least suspicious. `002465F0` did not look like a
question — it looked like a small forwarder I had already read. **The address you are most sure
about is the one worth thirty seconds.**

*(OPUS 2026-09-19. The alignment question that led here is settled the same way: `+0xA1` is a
genuine two-byte store at an odd offset, made by the shared header initialiser into every object
it builds — which is why the same instruction is cited by two different types' rows, and why
neither is wrong to cite it as long as it says whose instruction it is.)*
