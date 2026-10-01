# repos-9e — question A-1, the 158 unclassified functions

Session state: parent fresh-imported into `work/proj_h9e` (`GFZ_H9E`), `Verify-GfzCheckpoint`
returned **CHECKPOINT VERIFIED**, ledger `38,161 / 38,003 / 158 / 99.58596 / overlap 0`, residual
sha `c5d4b7f7fb1ffbf0c3f54c671bb0af02b0513901af634c5ca755333ce3d338ff`. Evidence regenerated into
`work/repos-9e/residual`. **No `Apply-*` or `Pack-*` was run.**

138 bodies extracted, **27 read**, **4 proposed**, **153 of 158 left unresolved**.

---

## COVERAGE

**New document.** `99-Unresolved-Residual/Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md`
— `DOCUMENTED`, tier 1, 0 audit passes. All nine sections. `check_links.py`,
`check_layout_units.py` and `verify_doc_addresses.py` all pass (the one `.text` non-function
citation is `00366638`, a jump table, documented as such in the data-address block).

**Recommendation once the rows are applied:** this system belongs in
`16-UI/Text-And-Number-Rendering/` beside `numeric-formatting-and-character-mapping.md`, which is
its upstream half. It is under `99-Unresolved-Residual/` only because that was my assigned
category. Phase E move, your call — `check_links.py` is the gate and I have kept every link
relative.

### Pre-enrichment rows — 4, ready for the gate

`Database/Tools/work/repos-9e/repos9e_pre.tsv`, authored 4-column, hash left for
`EnrichCurrentBodyManifest` per the hash-convention trap.

```
Apply-GfzBatch.ps1 -PreEnrichTsv ...\work\repos-9e\repos9e_pre.tsv -BatchId <yours> -ExpectedCount 4
```

| Address | Body | Proposed CodeDomain |
|---|---:|---|
| `003649A0` | 3020 B | `Presentation.Text.GlyphRunTexturedQuadEmissionAndPenAdvance` |
| `00366110` | 1318 B | `Presentation.Text.BraceTagMarkupInterpreterAndTextStateMutation` |
| `00364530` | 684 B | `Presentation.Text.NonDrawingGlyphRunAdvanceAndExtentMeasurement` |
| `0053E0B0` | 718 B | `Presentation.Text.ScrolledWindowLineCullShadowAndGlyphRunDispatch` |

If applied: 158 → 154, 99.58596 % → 99.59644 %. I am not asking for the percentage; I am asking
for four functions whose bodies say what they do.

### A fifth, read but deliberately NOT proposed

`00226640` (861 B). Complete body is a **deferred set/clear flag commit** run over every actor of
every active manager (`00263FF0(i)`, `i < 3`, or only manager 0 when its third argument is
non-zero). Six independent `(current, pendingSet, pendingClear)` triples are reconciled with the
identical idiom `if (set) { cur |= set; set = 0; } if (clr) { clr = 0; cur &= ~clr; }` — at
battle-unit `+0x40/+0x54/+0x60`, `+0x44/+0x4C/+0x58`, `+0x48/+0x50/+0x5C`, actor
`+0x10C/+0x110/+0x114`, and sub-object `[actor+0xC0] +0x170/+0x174/+0x178` and
`+0x164/+0x168/+0x16C`. Three transitions fire callbacks: `Actor_StopRequestedMovement` when the
first word goes empty-to-non-empty, `002E92F0`, and the two predicates `00238B40` /
`00312130`. Collected handles at `+0x1F0`/`+0x1F8` are then resolved and dispatched.

**Why I am not proposing it:** the mechanism is fully established but I did not read the six
flag words' consumers, so I cannot say what the commit *means* — and "deferred flag commit over
actors" without that is closer to a shape class than a mechanism identity. Yours to take or
leave; I would rather hand you an honest maybe than a fourth-plus-one.

---

## OPEN-QUESTIONS

New. Ids proposed, not claimed — `next_question_id.py` says pick nothing by eye and you assign at
merge.

| Proposed id | Question | Owner document |
|---|---|---|
| `PROPOSED-repos9e-1` | Which strings are `ex`-prefixed, and how does renderer `002B0280` differ? `00364980` proves the split and its selector; nothing says what distinguishes the populations. | glyph-run rendering |
| `PROPOSED-repos9e-2` | The shadow offsets in `0053E0B0` — a per-kind signed byte pair in runtime data. Mechanism established, values unobserved, so "drop shadow" is inferred from shape. | glyph-run rendering |
| `PROPOSED-repos9e-3` | The `{i}` icon payload: three argument bytes, and how they index the icon path in `0053E0B0`. | glyph-run rendering |
| `PROPOSED-repos9e-4` | Glyph table record byte `+0x04` — advance width or bearing? One reader, and the arithmetic fits both. | glyph-run rendering |
| `PROPOSED-repos9e-5` | The projection callback at `TextState+0x20`. Contract known from the call site; no implementation read. | glyph-run rendering |
| `PROPOSED-repos9e-6` | What `002AC5F0`, `002AAE40`, `002AF960` each draw. All three are font drawing (below); which text each owns is not established. | glyph-run rendering |
| `PROPOSED-repos9e-25` | **ANSWERED — the block is a C++ static object and its constructor chain sets 57 of the 65.** `005DC580(block+0x000)`, `005DC430(block+0x0D0)`, `005DC720` itself; 107 distinct block offsets, all written through `this` and therefore invisible to every absolute-address scan. | what-the-console-tunes |
| `PROPOSED-repos9e-29` | **Eight arm addresses with no writer found at all** — `+038`, `+040`, `+048`, `+068`, `+0E0`, `+0E8`, `+10C`, `+16C`. `005DC720` contains a bulk fill Ghidra renders as an empty `do {} while` at `this+0xA1D`; look there before concluding anything. | what-the-console-tunes |
| `PROPOSED-repos9e-26` | **ANSWERED — eight shadow-map matrices.** 64 contiguous bytes each, written inside the `"update shadowmap"` scope, built by `001EF6D0` from vtable-bearing frustum objects at `object+0x148` stride `0xD8`, live count at `block+0x3E4`. See the AUDIT-LOG entry. | what-the-console-tunes |
| `PROPOSED-repos9e-28` | **Whether the eight slots are lights, casters or cascades.** The count is a runtime value, not a constant, which argues against fixed cascades — but nothing read here says what fills the array. | what-the-console-tunes |
| `PROPOSED-repos9e-27` | **When `001F0AD0` runs.** *What* it copies is resolved; its cadence is not, and "per frame" is an assumption the document declines to make. | what-the-console-tunes |
| `PROPOSED-repos9e-7` | **The residual-wide string instrument.** `DumpUnresolvedStringReferences.java` reports 0 and the correct answer is at least 2 direct and at least 13 at depth 1. Should the scan be fixed, and should every other `Dump*`/`Scan*` script be audited for the same dependency on un-run analysis? | the-unresolved-158 |

**Bearing on existing questions, not closures — yours to judge:**

- **AC-6** (what the 13-function cluster is): three of its members — `002AC5F0`, `002AAE40`,
  `002AF960` — close a scope named `"display : draw Font"`. The text hypothesis that §11 killed
  and then reinstated is **right**, on evidence stronger than the reinstatement had.
- **AC-5** (why the mechanical classifiers failed): the string scan is one demonstrated reason.
  It answers "does this function reference an authored string" by asking whether Ghidra holds a
  *typed string* at the target — and this program has none — so the answer is no for every
  function in the binary regardless of the code. See the correction in AUDIT-LOG below.
- **AC-1** stays open. 153 of 158.

---

## AUDIT-LOG

### Instrument defect — `DumpUnresolvedStringReferences.java` returns a structural zero

**This is the block's most consequential finding and it invalidates a premise, not a number.**

Both `99-Unresolved-Residual/README.md` and `the-unresolved-158.md` state as founding fact that
the 158 have **zero** authored strings. `the-unresolved-158.md` §13 elevates this to "a
structural fact about the residual, not a null result" and concludes "the tail really is
complete-body reading, one function at a time." My own freshly regenerated `STRING_REFS.tsv`
reproduces the zero.

**The zero is an artefact of the scanner.** It walks instructions, calls
`instruction.getReferencesFrom()`, then `listing.getDataContaining(target)`, then tests
`data.getValue() instanceof String`. **It reports the contents of the Ghidra database, not the
contents of the binary.** Same species as the others logged today: a plausible number rather
than an obvious failure.

**Which link breaks — corrected 2026-09-02, after you flagged the scoping.** My first message
said `-noanalysis` at import meant Ghidra "never created references or typed string data."
**The references half is false and I withdraw it**: the packed parent carries prior analysis,
and this session's own `DATAREF_CONTEXTS.tsv` has 378 reference-derived rows. `-noanalysis`
prevents *re*-analysis on import, not all analysis ever. The break is narrower and does not
involve the import flag: **there is no defined string data.** Decompiling the two functions
with direct string references shows every string target as undefined `&DAT_00905988`,
`&DAT_008FB2B4`, `&DAT_00D10F50` — never a typed `s_…`. Independently, the only `data_type`
values in the entire certified dataref dump are `PEx64_UnwindInfo`,
`_IMAGE_RUNTIME_FUNCTION_ENTRY` and `IPToStateMapEntry[…]` — three EH structures defined by
hand, and nothing else. The zero measures **which bytes an earlier session happened to type**.
Why the typing is absent is not established and I am not guessing.

**A near-miss worth having on record.** While checking this I grepped for `s_[A-Za-z0-9_.]+`
and appeared to find a defined string `s_ResolveRuntimePointer` — which would have shown string
typing was merely patchy and sent the correction the wrong way. It was a substring match inside
the function name `ImageAddress_ResolveRuntimePointer`. **An unanchored regex is not a symbol
search.** It was caught only because the "string" had no reason to exist where it appeared, not
because the method was sound.

**Your three-script scoping is confirmed independently, and extends to a fourth.** I read the
primitives rather than take it on report: `ScanUnresolvedExactByteCloneDomains` uses
`getMemory().getBytes()` — reads the image, unaffected, **its empty result is a true negative
and you were right to protect it**. `ScanUnresolvedQualifiedSymbols` uses `getSymbolTable` /
`getPrimarySymbol` **and** `getReferencesFrom` — partly affected, exactly as you scoped it.
`DumpUnresolvedIncomingOwnerRefs` uses `getReferenceManager().getReferencesTo()`, and since
references demonstrably exist here, **it is unaffected too** — I was wrong to lump it in. So of
the four I named, one is broken, one is half-broken, and two return real negatives. Your rule —
*a negative from a tool is a claim about the tool until you know which layer it queried* — is
the right generalisation, and my original message over-applied it.

Corrected measurement — every RIP-relative `LEA` in `.text` resolved against every NUL-terminated
printable run in `.rdata`/`.data`/`.rodata`, attributed by certified body extents:

```
population : the 158 certified-current residual functions, sha c5d4b7f7…
instrument : 50,717 LEAs scanned, 8,611 string refs across 3,312 functions
control 1  : 0017F850 -> "display : draw Font"   PASS
control 2  : 00378540 -> "MWeather"              PASS  (agrees with the Weather documents)
shape check: result is 13 specific functions with specific strings, not "everything reaches sprintf"

direct string reference        :  2 / 158   (reported: 0)
string one call away           : 13 / 158   (never measured)
```

Both direct hits verified at instruction level, not merely counted: `0036A570` LEAs a contiguous
8-byte-aligned label table at `00D10F40` (`M2/l M2/U M2/L M /l M /U M /L FREE /I /C`);
`0020AC30` LEAs `.json`, `spc_`, `sum_`, `0001`.

**Eleven residual functions acquire a name at depth 1.** Five families, in a set the database
said had none:

| Residual fn | Body | Named by | Reads as |
|---|---:|---|---|
| `002AC5F0` | 7489 B | `display : draw Font` | font drawing — the largest unclassified function in the game |
| `003649A0` | 3020 B | `display : draw Font` | font drawing — proposed above |
| `002AAE40` | 2440 B | `display : draw Font` | font drawing |
| `002AF960` | 1117 B | `display : draw Font` | font drawing |
| `0018EEE0` | 1581 B | `ColorBuffer` `ColorBufferSampler` `apply_MainTex` `gamma` `resolution` `colorR/G/B` `percent` | a post-processing colour pass |
| `001E8070` | 1293 B | `fontclut_%d` | font colour look-up tables |
| `001D72F0` | 937 B | `display AutoSave Window` | the autosave indicator |
| `001C2980` | 897 B | `softEdges`, `Debug Info:` | — |
| `0036A570` | 729 B | own table + `TkFreeMain:Allready Free:%p from %p` | a memory allocator |
| `0036A2A0` | 495 B | `TkFreeMain:Allready Free:%p from %p` | the same allocator |
| `0020AC30` | 572 B | `JsonData/CutScenes/`, `mDofFocusDistance`, `mDofApertureFnumber`, a `plan_master\…\event\` regex | cutscene JSON and depth-of-field |

`002AAE40` is the function `the-unresolved-158.md` §11 called *"the purest example in the
database of why a call-context classifier cannot touch these"* — no caller, all three data refs
banned EH metadata. It is font drawing, and the evidence was one call below where every scan was
looking.

**Limits of my instrument, stated so nobody over-trusts it.** Only `48 8D`/`4C 8D` RIP-relative
`LEA`; misses `mov reg, imm64`, pointer-table indirection and 32-bit absolute forms; needs a
NUL-terminated printable run of ≥2. **2 and 13 are lower bounds, not counts.** Script at
`work/repos-9e/`, output at `work/repos-9e/depth1_strings.txt`. Caller ownership is still not
callee ownership and none of these strings assigns a `PrimaryOwner`.

### Switch verified against the whole construct, per the §12 lesson

`00366110`'s eleven cases were derived twice and independently: from the decompiled body, and by
decoding the raw 22-entry dword jump table at `00366638` out of the authorized EXE. Exact
agreement — `a c f h i k n p r s v`, with the other eleven slots sharing a default at `003665F3`.
The 22-entry span rules out a twelfth case hidden below a truncation. This is the check §12 said
was missing when this document's own switch claim was wrong within the hour.

**Recording a wrong intermediate rather than hiding it.** I first parsed that table as MSVC's
dword-plus-byte-index form and got index values of 243 and 216 — impossible, which stopped the
reading. The table is 22 dwords, no byte table. The tell was that the numbers were absurd, not
that the parse looked wrong: had the bytes happened to fall under 16, the mis-parse would have
produced a plausible and entirely false case list.

### Other verifications

- **Residual list not reused.** Prior `verify/residual_addrs.txt` diffed against this session's
  freshly regenerated `verify_GFZ_H9E/residual_addrs.txt`: identical, sha `c5d4b7f7…`.
- **Cluster instrument positive-controlled** before it was used to pick targets: over the 158 it
  reproduces the independently recorded structure exactly — 14 clusters of ≥2 plus 109 singletons,
  largest 13.
- **Body extents checked for over-run.** All four proposed functions end `C3` followed by `0xCC`
  padding to the next function. `00366110`'s 90-byte gap is fully accounted as its own jump table
  (88 B) plus a 2-byte NOP.
- **Layout units.** Three decompilations of `TextState` with different pointer types (`float*`,
  `longlong`, `float*`) agree field for field, which is the check that the §4 offsets are bytes
  and not subscripts. `check_layout_units.py` clean for my document.
- **Batch measurement re-taken** as the mission requires: **80 functions in 10.7 s, 80/80 ok, 0
  fail, 0 miss, 432 KB.** Second batch 46/46, third 12/12. Extraction is not the constraint.
  **138 extracted, 27 read** — only the 27 are claimed.
- **EH census on the fresh dump:** 378 incoming data refs — 197 `PEx64_UnwindInfo`, 158
  `_IMAGE_RUNTIME_FUNCTION_ENTRY`, 7 `IPToStateMapEntry`, 16 real code references. The README
  quotes 382/199/160/6 for the 160-set; note its own table summed to 381, not 382. Nothing in
  this block rests on any of them.

### Reopen recommended (I did not edit the document — not my category)

`16-UI/Text-And-Number-Rendering/numeric-formatting-and-character-mapping.md`. Trigger 2 and
trigger 7. Its §1 records the measuring function as unread and states that whether numbers form
even columns "is not known". `003647E0` is that function. **Control code `0x0001` advances the
pen by the advance width of the glyph for `'0'`** — a figure space. So numbers *do* align, and
the document's withdrawn claim stays withdrawn: the padding is a figure space, not a per-digit
width override. The correction is worth adding to its §8 rather than to mine.

---

### Falsification pass 1 on `the-largest-unclassified-functions.md` — 5 overturned, 8 survived

Taken from the *Now owed instead* table, a document I did not write. Recorded in its new **§20**;
frontmatter carries `falsification_passes: 1` and the program state it ran against. Four inline
corrections applied at the points of error, each keeping the superseded reading visible.

**The document had eleven recorded amendments and no recorded attack**, and that distinction is the
finding behind the finding: nine of those amendments were the author extending their own reading,
and **both things that broke here had survived all eleven**. Self-extension is not self-attack.

**Overturned**

1. **The headline census is stale by two** — 10,154 / 2,667,070 B → **10,152 / 2,666,058 B**. Cause
   proven, not inferred: re-running the census over `graph/functions.tsv` reproduces all three of
   the document's figures exactly, and that dump is the 01:09 state, missing the two GN closures.
   Its frontmatter claims the GN hashes, so its stated state and its actual source disagree. **This
   is precisely the defect `the-unresolved-158.md` §13 documents, in the same folder.** The warning
   was written and then walked into.
2. **Its stated self-check is vacuous.** "the owner column reproduces the ledger's `owner=9409`
   exactly, which is the check that the column is being read correctly" — because `overlap=0`, the
   owner count is 9,409 *whatever the CodeDomain filter does*. Demonstrated: the check **passes**
   with a filter that classifies all 38,161 functions as untagged, an answer wrong by 28,007.
3. **§6 "called from one dispatcher" is false** — `003CD840` has three callers, `003D2B60` three.
4. **§10 "`003CD840` twice" is wrong — three sites**, byte-proven, and the third is on the
   **pre-dispatch common path**, so chain A's main operation runs unconditionally rather than under
   two opcodes. `0036B130` is x4, not x3. There is also a tail region past all eight arms where
   `003D2B60` is actually invoked — §11 proved it "the same machine" without establishing when it runs.
5. **A second dispatcher, and it is the missing half of §19's identification.** `003CD2C0` (688 B,
   untagged, so in this document's own population) sits **8 bytes past the first dispatcher's jump
   table** and is a structural twin — `jmp rcx` at `003CD3F7`, its own 8-entry table at `003CD570`
   all landing inside its body, the same twelve callees **plus `003CD650`**. Reached from
   `0053AB50`, a different entry path.

   **The extra callee identifies it.** `003CD650` is the release primitive §18 decoded, and its only
   two callers are this dispatcher and the GFZ-named
   `RenderModelInstance_RemoveSubresourceVariantBinding`. So §19's Ensure/Remove pair is mirrored in
   the dispatch layer: **`003CCF20` never frees a record; `003CD2C0` does.** This *extends* §19
   rather than contradicting it — the binding system has a bind dispatcher and a release dispatcher,
   and the document described only the first.

**Survived** — recorded because an unrecorded audit did not happen. The `003CD298` jump table (8
entries, all inside the body, entry 8 is padding); all eight opcode→operation mappings; opcodes 4
and 8 composing; `003CD840` calling nothing; twelve distinct callees; the `00258D70`/`00258E40`
entry; and §18's reading of `003CD650`, which my caller census independently corroborated.

**The "no strings" claim survived, and this is the part worth carrying to the other documents.** It
had been resting on `DumpUnresolvedStringReferences.java` — which reports "no strings" for *every*
function in the binary, so it was supporting nothing. Re-tested with the corrected byte-level
scanner (control `0017F850` → `"display : draw Font"`, PASS) across all fourteen functions of the
machine, depth 0 and depth 1: **genuinely no authored string.** The claim is unchanged and is now
supported rather than merely unrefuted.

**Consequence for the other documents.** Every "no strings" claim anywhere in the database is
currently unsupported by default, not because it is wrong but because the instrument behind it
cannot return anything else. They are cheap to re-establish — the scanner is at
`work/repos-9e/`, and it needs a control each time.

**New questions raised by the pass (proposed ids):** `PROPOSED-repos9e-8` the second dispatcher's
opcode map, undecoded; `PROPOSED-repos9e-9` what reaches the tail region at `003CD24D`;
`PROPOSED-repos9e-10` `00431B10` and `003A9C10`, the other two callers of chain A, unread.

**Not tested, and now the largest untested surface there:** §12–§15 — the transform block, the
descriptor table, the tag handlers and the packed-id convention. I read them and did not attack them.

`check_links.py` passes (955 links). `verify_doc_addresses.py` flags only `003CD298` and `003CD570`,
both jump tables, both documented as such in the §20 table.

---

### Falsification pass 1 on `why-the-unowned-code-has-no-owner.md` — 5 overturned, 6 survived

Recorded in its new **§15**; frontmatter carries `falsification_passes: 1` and the state it ran
against. Five inline corrections applied at the points of error, superseded readings left visible.

**The central finding survives, and that is the headline.** *Two thirds of the uncalled unowned code
is reached through a pointer in a data table, so an `E8`-based edge list is blind to it by
construction.* Re-derived independently from the image: **7,186 of 10,923 = 65.8 %**, against its
7,185 of 10,924 = 65.8 %. Within one function on both sides. It is a real discovery and it stands.

**This document defends itself better than the last one** — §3 has an explicit *"Limits of this
measurement"* block, §11 measured a scan against a control, §1 is itself a retraction. **None of the
five failures is of a kind those defences were pointed at.** Four are undeclared populations; one is
a correction applied to half its own evidence.

**Overturned**

1. **§3's slot table is stale with respect to §3's own correction.** Reported
   `27,392 .rdata / 204 .data / 8 _RDATA`; correct is **29,000 / 3,015 / 8**. Proven, not inferred:
   re-running the scan with the candidate set restricted to `CodeDomain`-tagged functions —
   the restriction its own correction note calls a bug — reproduces **204 and 8 exactly**, `.rdata`
   within 4, and gives distinct-functions **7,332**, which is the **7,331** that note says was
   wrong. So the fix was applied to the distinct count and not to the slot counts printed beside
   it. **`.data` is understated ~15-fold**, and that is the substantive part: `.rdata` slots are
   static vtables, `.data` slots are the runtime-built dispatch tables the largest-unclassified
   document identifies as a major engine pattern. At 204 it reads as an almost pure vtable story.
2. **§1 and §2 contradict each other by 398** on the same eleven groups — §1 says 15,498, §2's rows
   sum to 15,896. §2 reproduces exactly; §1 does not.
3. **The 3,891 exception funclets are excluded from every population in §2 and §3, never declared.**
   Not an error — invisible. Four separate figures (5,283 / 172,156 B / 10,924 / 3,739) reproduce
   *only* after subtracting 3,891, and no caption says so. Same defect you just fixed in
   `progress.py`, arrived at from the document side.
4. **"70.4 % of the executable" is 70.4 % of a denominator never given** — 34,270 non-funclet
   functions. Against all 38,161 it is **63.2 %**. "Of the executable" is the one reading that is
   not true.
5. **The headline calls named upstream library code "unexplained".** The 24,116 population
   reproduces exactly, but **8,458 of it (35.1 %) carries a specific mechanism identity**, including
   `ThirdParty.Video.LibVPX_VP8_1_6_0.Vp8FilterBlock1d16V6Ssse3`, `EASTL.BasicString.StaticInitializer`,
   `ThirdParty.Rendering.Yebis`. A function matched to a named upstream routine is **tier 6
   identified** by our own hierarchy. The mission prompt's own figure for "accounted for and not
   understood" is ~11,800 — about half. (Sensitivity stated in §15: even excluding Phyre's 6,768 as
   a grey area, ~1,690 unambiguously identified functions sit inside a count of "unexplained".)

**Survived** — the 65.8 % ratio; the entire dark-set breakdown (`Phyre` 1,743, `NativeRoutine` 514,
`Runtime` 361, `NativeAdapter` 243, `Boundary` 173, `CompilerGeneratedCFG` 145, `NativeLeaf` 91 —
**all seven exact**); `_RDATA` 8; distinct functions 10,472 (I get 10,473); §2's `substantial` row
exact on all three figures; and §1's retraction of pass 51, whose edges-vs-functions reasoning is
sound.

**Instrument controlled before its results were believed**, using the trick that needs no external
claim: a run of ≥8 consecutive 8-byte-aligned qwords all equal to function entries **is** a vtable.
The scan finds **1,534** such runs, largest 1,172 slots at `008C31D8`, verified against raw bytes.

**Pattern across both passes, worth a rule.** Three of my ten findings across the two documents are
the same shape: **a correction or an exclusion applied to one number and not to the one printed next
to it.** The stale census in the other document, the half-applied scan correction here, the
undeclared funclet exclusion here. In each case both numbers were published side by side and nothing
compared them. Cheap check: **re-derive every number in a table from one stated population and fail
the table if any row needs a different one.**

**Not tested, now the largest untested surface there:** §5 (the eight specimens), §6 (the 112-record
table) and §10–§14 (AR-4 and its closure). §12–§14 carry positive claims this pass did not go after.
Also untested: whether any of the 7,186 address-taken functions is a *dead* vtable slot — §3 flags
it as a limit itself. And the `.data` slot population is now known to be 15× larger than reported and
**nothing has been read from it** — `PROPOSED-repos9e-11`.

`check_links.py` 975 links all resolve. `verify_doc_addresses.py` **ok**, zero findings.

---

### The `.data` slot population, read — and a third instrument of the same family

Written as **§16** of `why-the-unowned-code-has-no-owner.md`, with one of my own §15
characterisations withdrawn in place.

**The count is now certified rather than an upper bound.** §3's limits block conceded that a
coincidental integer can match a function entry, so the figure is an upper bound. It need not be:
**every genuine absolute pointer in a PE carries a base relocation**, or ASLR breaks it.
Intersecting with the 114,962 `DIR64` entries in `.reloc` separates real pointers from coincidence
exactly.

| section | slots matching an entry | reloc-backed | coincidental |
|---|---:|---:|---:|
| `.rdata` | 29,000 | **27,202** | **1,798** (6.2 %) |
| `.data` | 3,015 | **3,015** | **0** |
| `_RDATA` | 8 | **0** | **8** (100 %) |

Control: the 1,172-slot table at `008C31D8` is 1,172-of-1,172 backed.

**The `_RDATA` 8 were never real** — all eight qwords are `0x00800000`, sitting among
`0x7F000000`-type neighbours in a block of float bit patterns. It is simultaneously a valid function
entry and the IEEE-754 smallest normal float, and nothing relocates it. **The document reported 8
and my audit reproduced 8, and both were wrong, because both used the same method.** The rule was
already in the database; it turns out to apply to this pair.

**I withdraw one of my own §15 claims.** I wrote that the `.data` slots are "the runtime-built
dispatch tables". Wrong. `.data` spans `01DF0000`–`02F97530` virtually but its **raw image covers
only `01DF0000`–`01F7E400`**; all 3,015 slots are inside it and relocated, so they are **statically
initialised in the file**. The runtime-built regions (`022D9000`, `02AEE000`) are far past raw where
a static scan cannot see them at all. I conflated two parts of `.data`. The corrected reading is
sharper anyway: a pointer statically initialised into a **writable** section is one the engine
intends to be **replaceable**.

**"Nothing has been read from it" was also wrong — 75.7 % is already documented.** Measured against
the spans other documents state (base, stride, extent), not proximity:

| slots | table | already documented in |
|---:|---|---|
| 1,740 | ScriptVM native dispatch family 0, `01EED700`, 1,496 × `0x20` | `scriptvm-native-dispatch-table.md` |
| 339 | Battle action handler table, `01EEC460`, 359 slots | `battle-action-handler-table.md` |
| 202 | Combat formula step table, `01EFA5C0`, 202 × 8 | `combat-formula-step-table.md` |
| **2,281** | **inside a documented table** | |
| 734 | outside every documented span, **501 of them ScriptVM-owned** around `01F26xxx` — consistent with the four further ScriptVM tables | |

**Genuinely undocumented remainder: about 233 slots.** My own first coverage instrument was wrong
and is recorded as such: keyed on "is any address within 64 bytes of this run cited", it reported
1,959 of 1,977 runs uncited — nonsense, because a 1,496-record table cites its *base*, not its rows.
The battle action document had **already done this section's exact run analysis** (its §142: *"226
and 62 slots. They are one table; the runs break at null entries"*) and the proximity test could not
see it. **A coverage test keyed on citation distance measures how documents are written, not what
they cover.**

**The remainder, characterised:** Audio at `01F41E98` (26) and `01F41E60` (6); `01F003A8` (13, of
which **7 targets are unresolved functions**); `01EECFE0` (12, ItemsEquipment + a Party callback);
`01E0C498` (10); 58 CFG stubs as null placeholders; and the one with modder value —
**`malloc`/`free`/`calloc`/`realloc` stored as function pointers in a writable section** at
`01F41CF8` and `01F44CE0`. That is the cleanest allocator interception point in the image: swapping
it needs no code patching.

### The consequential finding: a third scan of the same broken family

Intersecting the certified slots with the 158 returns exactly one hit:

```
slot 00916518  [.rdata]  ->  002AAE40      base-relocation certified
```

`002AAE40` is the function `the-unresolved-158.md` §11 singles out as having *"**no admissible
reference of any kind** — no caller, no vtable, no dispatch table. It is the purest example in the
database of why a call-context classifier cannot touch these."*

**It has one.** The certified evidence dump lists three incoming references for it, all the banned
EH records that passage describes, and **`00916518` is absent from the dump entirely.**

Same cause as the strings: `DumpUnresolvedIncomingDataRefContexts` reports references Ghidra holds,
and Ghidra holds none from a data slot never typed as a pointer. **This one matters most, because
that scan is the source of the category's founding claim** — *"96 % of the incoming references to
these 158 are exception metadata"*. That census counts only references the database happens to
contain, and a relocated function pointer is exactly the admissible tier-8 evidence the category
says the residual lacks.

**Recommend `the-unresolved-158.md` §11 and the category README be corrected** — not my call to make
unilaterally on the category's flagship, so flagging rather than editing. The fix is cheap and
mechanical: re-census incoming references as `.reloc`-certified data slots plus the existing scan.
**`PROPOSED-repos9e-13`.**

**The locality is not used as evidence.** The slot sits 8 bytes before the power-of-ten table at
`00916520`. Adjacency is banned here, and the document I audited before this one flagged an
adjacency, declined to claim it, and was later proved right — it was coincidence. Recorded as a
reason to look, nothing more. The independent evidence that `002AAE40` is font drawing is tier 2 and
unrelated: it closes the `"display : draw Font"` scope.

**New questions:** `PROPOSED-repos9e-12` who overwrites these slots at runtime — all are statically
initialised and whether anything ever replaces them is untested, which is the whole point of a
writable section. `PROPOSED-repos9e-13` the re-census above. Also noted: the `.rdata` side is now
certified (27,202 of 29,000) and **unread**, and it is nine times larger than `.data`.

`check_links.py` 987 links resolve. `verify_doc_addresses.py` **ok, zero findings**.

---

### `PROPOSED-repos9e-13` DONE — the reference re-census, all 158

**Ready to merge into `the-unresolved-158.md` as a new section — I have not edited that file.** You
hold the merge on the category flagship and you have just corrected §11; this is written so it can
be pasted.

**Population:** the 158 certified-current residual functions, sha `c5d4b7f7…`, enumerated before the
scan and not chosen by it. **Predicate published below.** Three controls, all PASS.

#### The result

| admissible incoming evidence | functions | certified dump reported |
|---|---:|---:|
| direct caller (graph **+ byte-level, incl. thunks**) | **144** | 143 |
| code reference — verified RIP-relative `LEA` | **12** | "13" |
| relocated data slot → entry | **1** | 0 |
| relocated data slot → into the body | **0** | 0 |
| **at least one admissible reference** | **~~156~~ 157 of 158** | — |
| **no admissible reference of any kind** | **~~2~~ 1 of 158** | — |

> **CORRECTED 2026-09-03 by my own follow-up — please apply to the merged flagship text.** Route (a)
> of this census used `edges.tsv`, and **a thunk is a sink in the call graph.** `0020AC30` is reached
> through the 5-byte `thunk_FUN_0020ac30` at `001EC660`, called from the named
> `ActorResource_BeginManagerResourceSetLoad`. A byte-level `E8`/`E9` decode finds it at once.
> **`the-thunk-layer-and-why-call-counts-disagree.md` documents this exact failure** and calls it
> *"the single most common way a measurement of this binary comes out wrong"*; I did not consult it.
> Measured across all 158: 143 have callers in both graph and bytes, **1 in bytes only**, 0 in graph
> only, 14 in neither. **So: 144 with a direct caller, 157 with admissible evidence, 1 evidence-free
> — `00392A10`.** The dead-code finding is unaffected and now stronger (see below).

**The 143 corroborates the existing count exactly** — §10 says 15 of the 158 have no caller, and
158 − 143 = 15. That is an independent derivation agreeing with a recorded one.

#### The two functions with nothing

```
0020AC30   572 B    no caller, no code reference, no data slot
00392A10   707 B    no caller, no code reference, no data slot
```

**Neither is `002AAE40`.** And they are not equally dark: **`0020AC30` references authored strings
directly** — `.json`, `spc_`, `sum_`, `0001`, and one call deeper `JsonData/CutScenes/`,
`mDofFocusDistance`, `mDofApertureFnumber`, a `plan_master\…\event\` path regex. It has no *incoming*
evidence and strong *outgoing* evidence.

**`00392A10` (707 B) is the only function in the residual with neither.** No caller, no code
reference, no relocated data slot, and absent from the depth-1 authored-string result. It is the
real "purest example", and it is a 707-byte function rather than the 2,440-byte one §11 named.

#### The certified dump's "16 real code references" is 14, across 12 functions

Every one of the 16 rows was decoded from the image. **Fourteen are genuine RIP-relative `LEA`s.
Two are not:**

```
0023F8B0 from 0023F06E   48 89 83 20 01 00 00   mov [rbx+0x120], rax
                         -> the STORE of the address the previous instruction loaded.
                            Ghidra recorded two references for one address-taking.

00402000 from 002A756C   81 8b e8 03 00 00 00 20 40 00
                         -> or dword ptr [rbx+0x3E8], 0x402000
                            an IMMEDIATE BITMASK that happens to equal a function entry.
```

**`00402000`'s only credited "real code reference" is an OR-mask constant.** It is not
address-taken in code at all; it keeps its admissible status only because it has a direct caller.

So the category's evidence table needs three edits, not one:

| | README says | actual |
|---|---|---|
| real code references | 16 across 13 functions | **14 across 12** |
| relocated data slots | not measured | **1** (`00916518` → `002AAE40`) |
| "96 % of incoming references are banned" | stated of the image | true **of the reference dump**; the dump both **over**-reports (a mask, a double-count) and **under**-reports (relocated slots) |

**The scan is wrong in both directions, which is worth saying plainly.** The two earlier findings
were about absence — references Ghidra was never told about. This one is presence: a reference it
was told about that is not a reference. An instrument that both invents and omits cannot be
corrected by adjusting the number in one direction.

#### Predicate (published, per the rule)

```
a function F among the 158 HAS ADMISSIBLE INCOMING EVIDENCE iff any of:

  (a) an entry in edges.tsv with callee == F and callee_external == false
  (b) a RIP-relative LEA in .text whose computed target == F exactly:
        bytes 48|4C  8D  modrm&0xC7==0x05  rel32,  target = insn + 7 + rel32
  (c) an 8-byte-aligned VA inside a non-.text/.pdata/.reloc section's RAW extent that
        carries a DIR64 base relocation and whose qword == F exactly
  (d) as (c), but the qword lands strictly inside [F, F + body_bytes)      -> 0 hits
```

Known blind spots, stated so the count is used correctly: (b) sees only the `LEA` form, so a
`mov reg, imm64` address-taking would be missed — none of the 16 verified rows uses that form, but
the scan does not prove none exists elsewhere. (c) reads only the file image, so any pointer written
into `.data` at runtime is invisible; **91 % of `.data` is not in the file image.** Both make
**156 a floor**, not a ceiling — the true number of functions with admissible evidence can only be
higher, so **"2 of 158 are evidence-free" is itself an upper bound on darkness.**

#### Controls

1. **Recover the certified dump's verified code references** — all 12 genuine targets recovered.
   PASS. *(This control initially FAILED on `0023F8B0` and `00402000`, which is how the double-count
   and the OR-mask were found. The control was right and the scanner was right; the dump was wrong.
   I fixed the control's expectation only after decoding both sites from the image.)*
2. **Relocation parse** — the 1,172-slot vtable at `008C31D8` is 1,172-of-1,172 backed. PASS.
3. **Known hit** — `00916518` → `002AAE40` recovered. PASS.

#### What this changes

- **§11's "purest example" passage now has a correct subject.** `002AAE40` has a relocated data
  slot; `00392A10` has nothing. The rhetorical point survives intact and applies to a different
  function.
- **AC-5** ("why did the mechanical classifiers fail?") gains a sharper answer: for 13 of the 15
  caller-less functions the classifiers had evidence available and the instrument did not surface
  it. Only **one** function was ever genuinely without a handle.
- **The residual is far less dark than the category believes.** 156 of 158 have an admissible
  incoming reference. The barrier was never evidence; it was the census.

---

### `00392A10` read — a nine-patch box renderer that nothing calls

**New document.** `99-Unresolved-Residual/Dead-Nine-Patch-Renderer/the-box-renderer-that-is-never-called.md`
— `DOCUMENTED`, tier 1, all nine sections. `check_links.py` (1,010 links), `check_layout_units.py`
and `verify_doc_addresses.py` all clean; the address check reports **ok, 12 entries, zero findings**.

**What it is.** A resizable bordered box drawn as a 3×3 nine-patch — four fixed corners, a stretched
middle row and column — with a bilinear colour gradient built from four corner colours. The exact
derivation, straight from the body:

```c
colWidth[1]  = totalWidth  - rightColumnWidth - leftColumnWidth;   // stretched centre column
rowHeight[1] = totalHeight - bottomRowHeight  - topRowHeight;      // stretched centre row
```

Rows and columns of zero extent are skipped rather than drawn empty. Four 24-bit corner colours
expand into a sixteen-entry grid that each cell indexes with a stride, so the nine cells form one
continuous gradient. A mode flag from `002DD4B0` selects between the nine-slice path and a
single-quad fallback.

**What it is not: reachable.** Four independent routes, each with a control that could fail:

1. call graph — zero callee entries
2. every `E8`/`E9` in `.text` decoded — **zero reach it**; *control:* the same scan recovers the
   three known edges out of `00392A10`, PASS
3. every RIP-relative `LEA` — none targets it; and the `MOV r64,imm64` blind spot **I published in
   the re-census predicate is empty for this binary** — the form occurs 1,413 times in `.text` and
   not one carries a base relocation, so none encodes an image address
4. the 8-byte and 4-byte encodings of its address occur **zero times anywhere in the file**

Claim stated as *"unreachable by every static route"*, not *"never executes"* — static analysis
cannot establish the latter and the document says so.

**It is the root of a dead island of five functions, 4,090 bytes.** `00392CE0`, `002DC7F0`,
`002DD1E0` and `002DD090` are each called **only** by `00392A10`, so they die with it; 3,490 bytes
of that is inside the residual. Two of its callees are *not* dead — `002DC290` (11 callers, the
live cell drawer the game actually uses) and `002DD4B0` (10 callers). **The dead code calls live
code; nothing live calls the dead code.** Its own fallback path routes into `002DC290`, which is why
that half looks ordinary.

**A vacuous control caught in the act, recorded in §8.** My first version of route 3 required the
relocation up front, matched nothing at all, and would have reported a meaningless zero that looked
identical to a real one. Re-run without the relocation requirement, the matcher fires 1,413 times —
so the zero became a measurement. Same species as the `_RDATA` eight, one step earlier in the
process.

**Do-not-confuse recorded:** `002D6990` `ThreeByThreeAtlasPatchGeometryBuild` is a **different,
live** 3×3 mechanism with two callers and a disjoint callee set. The engine has a working 3×3 patch
system *and* this dead one. Whether one superseded the other is **not** claimed —
`PROPOSED-repos9e-14`.

**Modding note that matters:** the middle extent is computed by subtraction with **no clamp**, so a
box narrower than `left + right` produces a negative centre column and the loop draws with a
negative size rather than skipping.

**New questions:** `PROPOSED-repos9e-14` why it is dead (cut feature, unshipped configuration, or
superseded — nothing distinguishes them); `-15` what `002DD4B0`'s global is and what its ten other
callers use it for; `-16` the exact vertex format `002DC7F0` emits — 2,194 bytes read for colour and
flag handling, not for its output records.

**What this closes.** The residual now has **zero** functions that are unexplained in a way that is
a statement about the binary rather than about our instruments. The last one is explained, and the
explanation is that nothing calls it.

---

### `0020AC30` read — it is LIVE, and finding its caller broke my own census

**New document.** `99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md`
— `DOCUMENTED`, tier 1, all nine sections. `check_links.py` 1,019 links resolve;
`verify_doc_addresses.py` **ok** on both new documents.

**It is not evidence-free. It is reached through a thunk.**

```
ActorResource_BeginManagerResourceSetLoad  0032FCA0
  -> thunk_FUN_0020ac30                    001EC660   5 bytes, one JMP
     -> 0020AC30
```

**And `the-thunk-layer-and-why-call-counts-disagree.md` documents this exact failure mode** — its §1
calls it *"the single most common way a measurement of this binary comes out wrong"* and its §2 says
a graph census **loses the path at the thunk**. The warning was written down and I did not consult
it. That is the same shape as `the-largest-unclassified-functions.md` walking into the stale-dump
warning its own sibling recorded — which I found and criticised two passes ago. **I have corrected
the re-census above; the merged flagship text needs the same edit.**

**The cost was measured, not assumed:** across all 158, 143 have callers in both graph and bytes,
**1 in bytes only**, 0 graph only, 14 neither. The thunk hole cost exactly one function — and it was
half the headline result.

**What the function does.** Records which cutscene asset occupies each of five slots and decides
**from the name** whether that scene gets a depth-of-field sidecar. Slot index bounds-checked to
`< 5`; the index is published to `01DFE40C` for the call and cleared on every exit (24 readers). A
change guard compares length then `memcmp` and **skips everything if the name is unchanged**. On a
real change it releases the old entry, assigns the new into a 32-byte slot record at
`01F832F0 + slot*0x20`, then runs three substring tests:

```c
found("sum_")  ->  load "<name>.json";  if found("0001") then flagA = 1   // 01F832E8
else if found("spc_")                                    flagB = 1        // 01F832E9
```

`001C5750`, a direct callee, composes `JsonData/CutScenes/<name>.json` and reads
**`mDofFocusDistance`** and **`mDofApertureFnumber`** — focus distance and aperture, the two
parameters a depth-of-field effect needs. **So a cutscene is cinematically focused because someone
named its asset so that it would be**, and the look is two numbers in a text file.

Note the asymmetry, which is in the code: `0001` is tested **only** when the name contains `sum_`,
and `spc_` **only** when it does not.

**Authored names, from the id table at `00902540`:** `sum_j0001`, `sum_a0001`, `sum_f0001`,
`sum_i0001`, `sum_m0001`, `sum_l0001`, `sum_h0001`, `spc_z0000`, among `mrm_g0100`, `bds_f0100`,
`n1150`, `m1266`… **What `sum_`/`spc_` denote is NOT claimed** — the bridge is authored data in the
VBF archives, and `ff12-vbf` can open them, so it is tractable rather than merely open
(`PROPOSED-repos9e-17`).

**The dead-code finding next door is unaffected and now stronger.** Route 2 there is byte-level so a
thunk would have been caught, but I checked the indirect form explicitly: `FF 25` occurs **291 times**
in `.text` (control: form present, PASS), such a thunk needs a pointer slot holding the address, and
the 8-byte encoding of `00392A10` occurs **zero** times anywhere in the file. **No indirect thunk can
reach it.** Added to that document as route 5.

**Net for the category:** 157 of 158 have admissible incoming evidence; **exactly one function,
`00392A10`, is evidence-free, and it is evidence-free because nothing calls it.**

New questions: `-17` what `sum_`/`spc_` denote (VBF-tractable); `-18` what the two flags cause —
`0020AA40`/`0020AA30` read them, callers not followed; `-19` the JSON schema beyond the two keys.

---

### `PROPOSED-repos9e-18` ANSWERED — the flags gate a script-VM stand-down

Added as **§10** of the cutscene document; the question is struck in its §7. Gates clean.

**The cutscene's name changes how often actor scripts stand down during that scene.**

Each flag has exactly one reader, each reader exactly one caller, and graph and byte-level callers
agree at every hop (checked both ways — the thunk lesson applied):

```
01F832E8 flag A -> 0020AA40 (8 B) -> 001EC5E0 (17 B) -> 3 consumers
01F832E9 flag B -> 0020AA30 (8 B) -> 001EC5C0 (17 B) -> 4 consumers
```

The named consumer, `WorldActor_UpdateRuntimeAndScriptExecutionState`, runs a per-frame loop over
`0x28`-byte script entries. In entry states 1 and 2 it runs bytecode and then decides whether to
stop:

```c
if ( ( result != 0
    || ( FUN_001ed130() && (worldState - 1u) < 2 && flagB() == 0 )    // states 1,2
    || ( worldState == 3 && flagA() != 0 )                            // state 3
    || DAT_022C7F84 != 0 )
   && FUN_00357770() == 0 )
        entry[0x16] = 1;
```

**The two flags act in opposite directions, in disjoint states:** flag B must be **clear** for the
state-1/2 arm, so a `spc_` scene **suppresses** it; flag A must be **set** for the state-3 arm, so a
`sum_…0001` scene **enables** it.

`entry[0x16]` is a one-shot stop marker the same loop consumes on the next pass — cleared, then the
loop breaks for the frame. So a script runs a step and stands down until the following frame.

**So the naming convention reaches past the depth-of-field sidecar and into script pacing.** That is
the second thing the name decides, and it was invisible from `0020AC30` alone.

**Bounds, stated in the document:** I read **one consumer of three (flag A) and of four (flag B)**.
`0034CF90` and `0034D790` (137 B each) have **zero callers by graph *or* bytes** — the same position
`00392A10` was in before it was read — and `00180120` (39 B, from `00229590`) was not followed. The
five gate predicates are treated as opaque. New questions `-20` (the other consumers) and `-21` (the
predicates) record both.

---

### `PROPOSED-repos9e-21` ANSWERED — all five gate predicates named

Added as **§11** of the cutscene document; `-21` struck in its §7. Gates clean.

**`00357770` is the veto you predicted, and it is the script telling the engine it is still working.**
Seven bytes: `return DAT_022C7F88`. Its partner `00357760` clears that global **immediately before**
each bytecode step, and the gate tests it after — so it reports what happened *inside* the step.

**Thirteen of its fourteen writers are ScriptVM native command handlers**, located in the dispatch
table at `01EED720`:

```
cmd   45 00356C40 (+0x10)   cmd 1018 00340C70 (+0x10)   cmd 1304 0034AF20 (+0x00)
cmd   46 00357530 (+0x10)   cmd 1019 003414E0 (+0x10)   cmd 1305 0034B290 (+0x00)
cmd   47 0033F8E0 (+0x10)   cmd 1020 00341D70 (+0x10)
cmd   48 003401F0 (+0x10)   cmd 1021 00342450 (+0x10)
cmd  641 0034BBD0 (+0x10)   cmd 1056 0034A1D0 (+0x10)   cmd 1415 0034E630 (+0x10)
```

*Control:* that table's own census reproduces the documented figure exactly — **1,234 records with a
non-null field `+0`**, as `scriptvm-native-dispatch-table.md` §4 states. **PASS**; a wrong base or
stride would not land on it.

**Eleven of thirteen write from field `+0x10`** — the handler slot that runs while a command is still
in progress. So the flag means **"a native script command signalled during this step that it has not
finished"**, and when raised it vetoes the stand-down outright, whatever the other arms say. Exactly
the shape you anticipated.

**The third arm is an authored bracket.** `DAT_022C7F84` has exactly two writers, both ScriptVM
commands: **cmd 1485 sets it, cmd 1486 clears it.** A paired set/clear on consecutive ids is scripted
data turning the behaviour on for a region and off again.

**`001ED130` wires back to `0020AC30`.** It reads `DAT_01DFE40C` — the current-slot marker the slot
setter publishes — and the same `01F832B0` per-slot flag array:

```c
return !( fieldVar == 0x19 || (fieldVar == 0x10C7 && perSlotFlag[currentSlot] == 5) );
```

Two hard-coded carve-outs. **`001ED180`** requires three unrelated predicates clear **and** the
transition field id to be one of `0x2F4`, `0x2E9`, `0x27B` — so the state-1/2 arm is inactive except
during three specific world transitions. **`001EDDA0`** and **`001EDE80`** test the same two globals
on opposite polarity — two faces of one runtime mode; `001EDDA0` has 50 callers, so it is a general
engine-mode question rather than anything local.

**The gate restated with every term named is in §11.** Shape: the VM's own result, three narrowly
gated situational arms, and a hard veto from any command that says it has not finished.

**New, both authored-data bound:** `-22` what field ids `0x19`/`0x10C7` and transition ids
`0x2F4`/`0x2E9`/`0x27B` name — same VBF bridge as `-17`; `-23` what the fifteen ScriptVM commands
listed above do — located in the table, no body read.

---

### `PROPOSED-repos9e-23` ANSWERED — they are the script's waiting commands

Added as **§12**; `-23` struck in §7. All 23 handler bodies behind the 15 command ids read — 1,184
bytes, largest 147. Gates clean under the **fixed** `check_links` (141 files, 1,032 links).

**`DAT_022C7F88` does not mean "something happened". It means a script command is still waiting.**

Player-facing: **"Press X to continue."** A cutscene script pausing for a button, a condition or a
frame count raises the flag every frame it is still waiting; the §10 gate then refuses to stand the
script down, so the wait is re-polled on the very next frame. **That is why a cutscene prompt
responds the instant you press it.**

| family | cmds | shape |
|---|---|---|
| **wait for a button** | 45–48, 1018–1021 | poll an input mask, raise the flag while not pressed |
| **wait for a condition** | 641, 1056 | build a state mask from the actor, raise while zero |
| **wait N frames** | 1415 | countdown, raise while counting |
| **produce a value, yield anyway** | 1304, 1305 | write an int result, raise **unconditionally** |
| **authored bracket** | 1485 / 1486 | set / clear `022C7F84` plus two matched helper pairs |

The eight button waits are one routine against **two banks of four accessors** — a *history* bank and
an *actor-state-aware* bank at the same four offsets — and nine commands share the secondary handler
`003567F0`, which pops the button mask off the VM value stack. So an authored wait-for-button is one
command id plus one integer.

**Two findings inside that I did not expect:**

**1. It closes a loop from my first block tonight.** The four
`InputGameplay_GetActorStateAwareRemappedMask04/08/0C/10` accessors are exactly the four that
`the-unresolved-158.md` §11 named as readers of the eight-slot actor registry at `0209C4D0`. **The
cutscene stand-down gate, the ScriptVM wait commands and that registry are one mechanism**, reached
from three unrelated directions across the session.

**2. Scripted waits are not uniform across the game.** Command 1415's countdown decrements a
**second time** when `FUN_001ED180()` is true — the same three-world-transition predicate from §11.
So every scripted frame-wait runs at **double rate during those three transitions**, and the
predicate that gates the stand-down arm also halves scripted timing.

**The protocol, stated:** field `+0x10` is the poll handler; a command returns true to stay active
and raises the flag on the same path. The return value keeps the command alive; the flag tells the
frame loop not to stand the whole script down. Two consumers, one fact.

**New:** `-24` — `FUN_00267310`, the shared escape tested against `actor[0x15]`, used by families B
and C. It ends every scripted wait regardless of the condition, and naming it is probably the
highest-value single lookup left in this thread.

**On the `check_links` fix:** every "N links resolve" figure I quoted before this tick was over 209
files including scratch; it is 141 now. My four documents were re-checked independently against the
corrected population and carry no broken links. **Noted as a correction to my own reporting, not
just yours** — I quoted those numbers as gate evidence six times.

---

### `PROPOSED-repos9e-24` ANSWERED — the escape is a per-manager flag byte, and it is not a cutscene mechanism

Added as **§13**; `-24` struck in §7. Gates clean (141 files, 1,034 links; `verify_doc_addresses` ok;
`check_layout_units` clean for my documents).

`FUN_00267310` is 22 bytes: `return table[managerIndex * 0x288 + 0x201]` — **byte `+0x201` of a
648-byte actor-manager record**, indexed by `actor[0x15]`.

**The array base was derived, not assumed.** Sweeping `.text` for `imul r64, r64, 0x288` finds **55
sites in 46 functions** *(control: form present — PASS)*, and the lowest base they pair with is
`02098E10`. The one named user of that stride, `ActorManager_SetResourceTeardownCallback`, works at
`+0x108` of the same records — so it is the actor-manager array, on independent evidence.

**It is a bitmask, not a boolean.** `0026A5B0(managerIndex, on, bit)` sets or clears one bit:

```c
if (on) *f |=  (byte)(1 << (bit & 0x1F));
else    *f &= ~(byte)(1 << (bit & 0x1F));
```

**Set from two ScriptVM commands and four engine paths** — cmd 1337 (begin) and cmd 1306 (poll) reach
the setter two hops up, plus `00228130`, `002628B0`, and `ActorManager_BindLoadedDefinitionPayload`
writing the byte directly.

> **A wrong expectation, caught by the control and recorded in §13.** I expected the setter's two
> immediate callers to be dispatch entries, as the `022C7F88` writers were. **They are not** — the
> membership test returned **0 of 4**, and only one hop further up did two commands appear. By
> analogy I would have written "script commands set these bits" about a byte the engine also writes
> on four other paths.

**And it is not a cutscene mechanism.** **65 functions read it** (graph and bytes agreeing exactly),
including **`World_UpdateSimulationTick`** and **`Movement_UpdateSteeringTowardTarget`**, plus
`WorldActorScriptVM_InterpretBytecode` reading the field directly. The waiting commands are one
consumer among many — so §12's thread ends by walking out of its own subsystem.

**The modding-relevant fact:** waits test `FUN_00267310(...) != 0` — **the whole byte, not a specific
bit**. So *any* bit set in a manager's flag byte terminates *every* scripted wait belonging to that
manager. A wait cannot opt out, and a bit set for one purpose ends waits that had nothing to do with
it.

**Player-facing, stated at the limit of the evidence:** a manager-wide switch that makes scripted
waits stop waiting — which is what skipping or fast-forwarding scripted content looks like from
outside. **Which bit means what is not established**, and naming one "the skip button" needs the bit
assignments, which sit behind the same authored-data boundary as `-17`/`-22`.

**New:** `-25` — the eight bit assignments. The setter takes the bit index as a runtime argument, so
the constants are in the four setter callers (`00360710`, `00360A50`, `00360880`, `003603F0`), none
of which was read. That is a small, self-contained job.

**The cutscene thread is now complete from the code side.** `0020AC30` → slot classification → DoF
sidecar → the two flags → the stand-down gate → the five predicates → the fifteen waiting commands →
the escape byte. Everything remaining in it is authored data: `-17`, `-22`, `-25`.

---

### Falsification pass 1 on `18-Audio/.../how-a-sound-request-becomes-a-voice.md` — 10 overturned, 11 survived, 2 gate false positives dispositioned

Recorded as its new **§10**; frontmatter carries the pass. Four inline corrections applied at the
points of error. Gates clean (1,036 links; `verify_doc_addresses` ok, 153 addresses).

**This document is unusually resistant.** Machine-code listings byte-exact, RTTI table correct in
every row, three separate global reference censuses reproducing to the function. **All three failures
are the same failure:** every population figure was measured over `edges.tsv`, and the call graph
omits the thunk layer.

**Overturned**

1. **`00249C60` has 100 non-Audio callers, not 99.** Verified at instruction level —
   `0058066A: e8 f1 95 cc ff` inside `0057FE80`, preceded by `lea ecx,[rax+1]`. Split corrected to
   **68 unowned / 29 UI / 3 Save_Load_Settings**. *(The call site independently corroborates the
   document's central claim that the function takes its argument in `ECX` — from a site it never
   saw.)*
2. **The inbound-surface census is a floor.** Graph: 174 → 168 surface, 305 callers, 401 edges — all
   reproduce **exactly**. Byte decode: **188 → 182, 325, 421**. And the graph has **zero** edges the
   decode lacks, so the figures move in one direction only, by about 8 %.
3. **§8's "168, not 174" correction went one way only.** 174 is an upper bound for the retraction
   reason it gives *and* a lower bound for the thunk reason it does not. Corrected both ways: **182**.

**Cause named:** of the 20 omitted non-Audio→Audio edges, **19 are `JMP` tail calls and 17 come from
functions Ghidra itself names `thunk_FUN_…`**. A thunk is a sink in the call graph, so the edge out
of it is never recorded and its target's caller list omits it. These thunks are non-Audio while their
targets are Audio, which is exactly the quantity the census counts.

**Survived** — body of `00249C60` byte-exact including the `lea r8d,[rdx+0x3f]` peephole; its gate
displacement resolving to `02091098` exactly; `00249CA0` being the same 51 bytes with `003A11F0`;
`002256B0`'s `0x7F`/`0x40` writes; `0016D6A0` as `C2 00 00`; the `SeSep` magic; **all five bank
kinds, vftables and constructors** (each checked for a `LEA` to its stated vftable *and* a
`mov edx, kind`); `02091098` one writer three readers; `022CB726` three writers one reader;
`0215EF4D` "three writers set it to `0x7F`" (seven writers exist, exactly three write that immediate
— the sentence says what it means); `002DEC00` 12 non-Audio callers on both routes.

**The standing `check_layout_units` finding on this file is a FALSE POSITIVE and is now
dispositioned.** It has been red on every run all session. The machine code settles it: `002256B0`
opens `48 c7 41 14 ff ff ff ff` — a **qword** store at `+0x14` covering `+0x14`–`+0x1B` — and the
next write is a dword at `+0x1C`, with **no write to `+0x18` at all**. So `+0x18` is genuinely inside
the qword, the document says so in the row itself, and this is the checker's own documented
legitimate case. **The document was right and the gate was noise.** Someone should stop it recurring.

**A defect in my own instrument, recorded because it nearly inverted a result.** My first
RIP-relative scanner hardcoded the modrm `REG` field to `0`, so it saw only `EAX`-sourced stores and
reported `02091098` as having **zero** writers — it would have "refuted" a true claim. The control
that caught it was requiring the scan to find the six writers of `0215EF44` the document names. **A
control drawn from the document under attack is the cheapest guard against a scanner too narrow to
see the thing it is testing.**

**The seven BODY DRIFT findings you sent: all seven confirmed and corrected, and the pattern you
spotted was the real finding.** Actual sizes 231 / 78 / 62 / 97 / 97 / 62 / 62. Two candidate
measurement mistakes tested and both fail — measuring to the first `ret` gives 225/78/56/97/97/35/56,
and none of the seven has a tail `JMP` — so these did not come from mis-measuring the current program,
and §3's provenance sentence is **not true of those seven rows**. Where they came from is a question
only the author can answer.

**Your instinct that a claim sits underneath the sizes was right.** Three claimed sizes for seven
functions is a grouping:

| implied group | actual | verdict |
|---|---|---|
| `00217FD0`, `0021CC10`, `0021BDB0` all "46 B" | all **62** | holds |
| `00212710`, `0021A9F0`, `00219400` all "66 B" | **78**, 97, 97 | **breaks** |

**`00212710` is the base `AudioController` constructor and is not the same size as the two derived
constructors it was grouped with.** And the two surviving groups are now *better* supported than the
document had them — byte-diffing shows `00217FD0` vs `0021BDB0` and vs `0021CC10` differ in **6 of 62
bytes**, and `00219400` vs `0021A9F0` in **12 of 97**. So there are two genuine constructor families
(one emitted routine specialised three ways, another specialised twice) plus a base that belongs to
neither — a structural fact §3 never stated.

**The `GHOST ADDRESS` on `02AEEDC8` is a checker artefact, and I have dispositioned it rather than
edited the document.** The address appears **only** in the data-address block the template requires,
with `Kind = 24 B/entry` in the column that holds `u32`/`s8`/`pointer` for the other rows. It is a
stride in the stride column; the checker matches the `NN B` shape anywhere in the row. **The document
is compliant.** Writing `24-byte entries` would silence it without changing the claim, but that is a
decision about the tool — I have not made it, and the row must not be deleted to quiet a gate.

> **Two gates have been red on this document continuously, both falsely, and neither was ever
> dispositioned.** An undispositioned false positive is not free — **it is the noise a real finding
> hides in**, and this file was carrying seven genuine BODY DRIFT findings behind them the whole time.

**Not tested:** §4's formulas (read for structure, constants not re-derived), §2's music block and
the 16-slot initialiser, the five controller constructors and their pool constants, and the
`0016D6A0` reference census cited from a peer.

---

### Glyph document: maintenance done, pass still owed

**Not a falsification pass** — I wrote this document, and it is recorded in the file as §10 marked
explicitly as maintenance, with the pass shown as owed. All eight `audit_crossrefs` findings handled.

**Two BODY DRIFT, corrected:** `002D8690` and `002D87D0` are **306 B**, not 1,106.
**Cause:** `002D28E0` is 1,106 B and sat one row away in the working listing this document was
written from — a size transcribed from the wrong row of a neighbouring table. Both wrong values being
identical is the tell.

**One data-row correction accepted and re-verified from the image**, not taken on report:
`008C5F80` is a pool of six signed axis vectors — `+X`, `+Y`, `−Y`, `+Z`, `−Z`, `+W` — of which
`00203170` copies four that assemble to the identity. **The pool has no `−X`**, which nobody has
explained. My original row named the address after the use four of its six rows are put to; that is
the same species as inheriting an owner from a caller.

**Five UNACCOUNTED NEIGHBOUR, all dispositioned:**

- **Three are shared-utility noise, with the fan-in to prove it.** `00203170` has **84 callers across
  five owner classes**; `00202B90` 14; `00202F70` 12. Movement's 27 edges are Movement using the same
  vector maths as text rendering **because it is the same maths**, not because the paths meet.
- **One is an artefact of citing a control.** `00378540` appears in this document exactly once — as
  the *positive control* for the string scanner in §8. The checker cannot tell a **system claim**
  from an **instrument control** and inherits the control's whole neighbourhood.

  > **Publishing your controls costs audit noise.** We have spent the session pushing sessions to
  > name controls in the document, which is right, and the consequence is that every control address
  > drags its neighbours into `audit_crossrefs`. Worth a tool decision — mark control citations, or
  > ignore addresses appearing only in an evidence section.

- **One is a real gap and I did NOT disposition it away.** `002AAE40` and `002B0280` both call
  `ImageAddress_ResolveRuntimePointer`. `002AAE40` is one of the four functions this document
  identifies as font drawing by the `"display : draw Font"` scope, and `002B0280` is the **other**
  text renderer §2 says exists. **Both resolve authored-data pointers and the document never says
  so.** Whether that belongs in §2's mechanism is exactly the judgement an author should not make
  about their own omission — **flagged for the incoming auditor.**

**Handed to whoever takes the pass**, rather than self-assessed: the `0053E0B0` shadow-offset reading
is inferred from shape with the offsets in runtime data I never observed; the `{i}` icon path is
unread; and the `+0x04` glyph-record field has one reader and two readings I could not separate. I
also still hold the working listings, so *"what produced this error"* is cheap from me — as the 1,106
shows — and that costs the auditor nothing in independence.

---

### Falsification pass 1 on `22-Middleware-PhyreEngine/.../animation-channel-binding...md` — 3 overturned, 6 survived, BM-1 closed

Recorded as its new **§10**; frontmatter carries the pass; table, §2 and §7 corrected in place. Gates
clean (1,041 links; `verify_doc_addresses` ok; `check_layout_units` clean for this file).

**Every number in §3 is exact.** All five body sizes, the descriptor layout, the log string and the
`1.0f` constant survive. **What failed is a boundary: the document read six entries of a
nineteen-entry table and described the six as the table.**

**The semantic table is 19 entries, not 6.** Walking the stated stride from the stated base until the
name-pointer pattern breaks (`01F2D008`, pointer `0`) gives, beyond the six:
`ShaderParameterF1`, `LightColor`, `LightIntensity`, `LightFalloffAndPenumbra`, `CameraFov`,
`CameraZNear`, `CameraZFar`, `CameraOrthographicSize`, `MorphTargetWeight`, `UserAttributeBool`,
`UserAttributeInt`, `UserAttributeFloat`, `UserAttributeVector`. **All nineteen are referenced from
`.text`** (2–5 sites each), so none is vestigial.

**`BM-1` closes.** The 2-component entry at `01F2CEB8` is **`ShaderParameterF2`** — and the component
count the document already had was right, which is a point in the reading's favour: it measured the
field it could reach and did not guess the one it could not.

**And the boundary error costs a player-facing claim.** §1 and §2 give *"a shader parameter"* as the
example of a non-transform channel. The table says the set also includes **light colour, intensity
and falloff; camera FOV, near, far and orthographic size; morph target weight — the channel that
drives facial expression; and four user-attribute types.** So one animation file can pull the
camera's FOV, dim a light and change a face in the same bundle of curves that moves the skeleton.
**The mechanism section was right and its example was the narrowest one available.**

**Survived**, each on evidence that could have refuted it: the five body sizes; the `+0x00`/`+0x08`/
`+0x10` layout, re-checked across **all nineteen** rather than the six cited; the refusal string at
`00D31E50`; `01CEBBA8` = `1.0f`, **which the glyph document cites as the same constant from an
unrelated direction**; and §2's *"pointer compare against three known globals"* — every `LEA` in the
composer's 1,674 bytes decoded, exactly six sites, two each, `Rotation`/`Translation`/`Scale` and
nothing else.

**An unfit instrument of mine, recorded.** To test *"exactly one descriptor object per semantic"* I
first counted name byte-strings: `Rotation` 2, `Translation` 2, **`Scale` 5,167** — because "Scale" is
a common English substring. **That instrument cannot answer the question at all.** The right test uses
the pointer: read each descriptor's own name pointer and find every 8-byte-aligned qword equal to it.
**One slot each, image-wide** — the claim holds. *A test that looks equivalent to the right one and
is not is worth more in the log than the answer it gave.*

**Not tested:** §4's formulas (quaternion normalize, quat→matrix, the `flags & 3` / `flags & 4`
dispatch) — read for structure, no constant re-derived; the binder's path walk and its four kinds;
the two `MarkContributedSlots` variants; `005A7E90`'s virtual dispatch; and `ChannelValue`
`+0x18`..`+0x27`, still open.

---

### Falsification pass 2 on `18-Audio/.../what-the-engine-calls-to-make-a-sound.md` — 2 overturned, 4 survived, 1 self-correction

**Note: this document already carried a pass** (§10, `repos-2d`, 2026-09-03) — it was listed to me as
never attacked. Mine is **§11**, and it deliberately attacks what §10 said it could not.

**The numeric layer is clean.** Flagged in advance because the companion had seven sizes estimated
from decompiled line count — **that defect did not reach this document**: all eight sizes exact, 177
and 2,064 exact, the partition sums to 177.

**Overturned 1 — the population split counts the rejection bucket as Audio, which the document's own
argument forbids.** Re-deriving with *"Audio caller"* = `owner == Audio` gives **14 / 69 / 43**, not
25 / 54 / 47. Rather than call it wrong I tested five definitions to find which reproduces it. Two
do, and they are the same rule: **a caller counts as Audio if it is Audio-owned OR is itself tagged
`Boundary.Audio.NativeSupport`.**

That rule is defensible — but §5 and §8 argue at length that **`Boundary.Audio.NativeSupport` is a
rejection bucket, not the audio API**. **The same tag is a rejection bucket where §8 needs it and
Audio membership where §4 needs it.** The numbers are not wrong; the definition is unstated and
contradicts the document's thesis. Under the stricter rule **69 of the 177 are called only from
outside Audio, not 54** — which *strengthens* §8. §4 now states its rule inline with both readings.

**Overturned 2 — "no callers at all: 51" is 50 against the bytes.** `0035D030` is reached through
`thunk_FUN_0035d030` (5 B). Same class that hid `0020AC30`'s caller.

**And a correction to my own earlier pass, which is the part worth carrying.** In the companion's
§10 I wrote that the graph *"never invents an edge, only omits — so every figure is a lower bound."*
**The first clause was true of that population and is not a property of the instrument.** Across the
whole image the graph holds **384 edges a direct `E8`/`E9` decode does not** — indirect calls Ghidra
resolved. Over the 177 here: **1 graph-only, 8 bytes-only.**

> **Neither route bounds the other. They see different things** — the graph sees resolved indirect
> calls, the byte decode sees thunk tail-jumps. A figure from either is a floor with respect to the
> other's blind spot, not a floor absolutely.

> **A property measured on one population is not a property of the instrument.** Same error as
> reading six entries of a nineteen-entry table: a boundary observed, then assumed to be the edge.
> I have corrected the companion document as well as recording it here.

**Not attacked:** §2's disassembly and the two constants (§10 covered them); §8's rejection-bucket
analysis itself as opposed to its use in §4; the `0215EFxx` layout; §7's three unknowns; and the
206-vs-211 site count §10 recorded rather than reconciled — still open, and I add nothing to it.

---

### Falsification pass 1 on `05-Spawn-Encounter-Lifecycle/spawn-placement-height-and-authored-tunables.md` — 0 overturned, 11 survived, 2 refinements

Recorded as its new **§11**; frontmatter stamped; two §3 rows refined. Gates clean (1,047 links;
`verify_doc_addresses` ok on 135 addresses).

**Nothing was overturned, and the pass was not cheap.** The author recused because it had been
corrected twice by adjacent work rather than review, and both errors had survived their own
adversarial pass. I attacked the two already-wrong claims first.

**36 of 36 body sizes exact. 5 float constants exact.** The sine table at `01F004E0` sampled at 338
points across the full 32,768 — **0 mismatches**, worst |Δ| 1.2e-08 — and reading one past the end
gives `1.0`, not `sin(2π)≈0`, so **the claimed extent ends exactly where the pattern breaks.**

**Family 3 holds 147 in its first dword** (control: family 0 reads 1496 as documented, PASS), and
**all ten primitive → handler mappings confirmed** by walking the 147 × `0x20` records, including
`0x3053` at **record 83** exactly as stated.

**The keep bank corroborated three ways**, because Correction 2 had already changed it once: stride
`imul …, 0x250` 50 sites concentrated in `Spawn*`; `mov reg, 0x9400` in the initialiser and the
area-transition rotator; and `0x9400 / 0x250 = 64` with no remainder.

**The flag bits settled by the encoding.** Bits 45 and 49 cannot be reached by `test r/m64, imm32`,
so they compile as a 64-bit immediate — and it is the same immediate in both places:
`mov r64, 0x0002200000000000`, twice in `00235720`. Correction 1 is right and **the two bits travel
together as one mask.**

**Refinement 1 — the reset mask clears five bits.** `00236A60` masks with `0xFFFF7FFDFFE7FFFD`:
**clears 1, 19, 20, 33, 47**, preserves 59. *"Preserves bits 45 and 49"* is true but describes the
reset by naming two of the 59 it does not touch; the informative half is the five it does. §3 refined.

**Refinement 2 — the `0x250` stride is not a keep-bank signature.** **18 of the 50 stride sites are
inside one function**, `0043F450` — `PrimaryOwner:Presentation`, 9,092 B, **referencing neither bank
pointer**. The document's identification survives *because it is anchored on the pointers, not the
stride*, which is the right anchor. Recorded so nobody later treats the stride as an identifier.

**Two instrument notes, because both were nearly wrong.** My flag-bit matcher looked only for the
`BT` family and found **bit 26 and nothing else** — it could have been reported as "45 and 49 are not
tested here". **The partial positive inside the same function is what said the matcher was the
problem, not the code.** And the `0x9400` scan initially had only the non-REX `mov reg, imm32` form.

**Not attacked, and the next pass should start here:** §2a/§2b's central mechanism (the ground probe
and *"nothing generates a Y coordinate"*) — read for structure, no body re-derived; **§2e's census**
*"does every zone install the tunables"*, which is the largest remaining surface and the same shape
as the population claims that failed in two other documents tonight; §4's formulas beyond the
constants; Correction 3; and the `002D81D0` false-positive analysis.

---

### `0072A320` read — it is `TEXSHADERSET::CreateEffect`, and it names every post-processing effect in the game

**New document.** `17-Presentation-Rendering/Post-Processing/the-post-processing-effect-catalogue.md`
— `DOCUMENTED`, tier 2, all nine sections, 845 lines because **the catalogue is the deliverable**.
Gates clean (1,059 links; `verify_doc_addresses` ok; `check_layout_units` clean for this file).

**Identity from four authored log strings in its own body**: `==== TEXSHADERSET::CreateEffect() ====`,
the `IGPUEffect::CreateEffectFromFile()` failed/succeeded pair, and `get parameter handles ...` —
with `..\src\GPU\GPUTextureUtil.cpp` and a **Feb 18 2016** build date.

**What it does:** runs once at start-up, loads a compiled `.pso` effect, then makes **364 direct
calls** — ~323 of them registrations across **seven helper shapes** — to fetch a handle for
**325 shader techniques and 36 uniforms**. The full list is in §4, nothing elided.

**The catalogue is the finding.** 35 families: **Depth 63, Motion 50, Bokeh 40, Scatter 32,
Composite 20, Generate 16, Mad 15, Temporal 14, Bright 9**, then Cross, Lens, Colour, Alpha,
Feedback, **Fxaa2**, Heat, Render, Glare, and singles including **AlchemySsao**, Corona, Dilate,
Median, Tonemap. Uniforms name three HDR encodings (`LOGRGB`, `REINHARDRGB`, `RGBALUM`), vignette,
chromatic/lens distortion, gamma and colour-transform matrices.

**A direct link to authored data:** the uniform **`fParam_FocusDistance`** is the shader end of
**`mDofFocusDistance`**, the key the cutscene sidecar reads out of `JsonData/CutScenes/<name>.json`.
A number a scene author typed into a text file arrives here as a shader parameter. **Stated as a
name correspondence, not a traced dataflow** — §8 says so explicitly.

**The suffix grammar is decoded** — `_Sn`/`_Tn`/`_TSn_n` are variant families and the helper's
**count argument is the multiplier**: `…LayerMaskT1_Sn` with `0x19` registers 25 handles under one
name.

**Fourth narrow matcher, and the sharpest one.** My first string scan used `[ -~]` and
returned 364 — **and the five it dropped were the five that name the function**, because each ends
in `
`. **A printable-only filter is not neutral: it selects against log messages, which are the
most identifying strings there are.** Caught by the rule from §14 — the GFZ's own comment quoted
`TEXSHADERSET::CreateEffect()` as a string this function references, my scan did not report it, and
the known positive disagreeing is what sent me to look.

**Second instrument limit, stated because it affected a number:** a linear `E8` decode found 37
apparent call targets of which **13 are not functions** — `E8` bytes inside other instructions'
operands. Excluded; the 24 real ones carry all the high counts. **The per-helper counts are sound;
a raw target count would not have been.**

**Generalisation audit, per the phase-transition caution:** the suffix grammar rests on 325 names;
the count-as-multiplier reading rests on **four observed literals at two of the seven helpers** and
is explicitly not established for the other five; the `fParam_FocusDistance` link rests on **one**
name pair. All three are labelled with their support in §8.

**Not known and said so:** no shader body was read — they are in the `.pso`, not the executable —
so 325 names are recovered and **zero techniques are explained**. The object layout is deliberately
unpublished: handles go to `this + N` on a `longlong *`, so the slots are **qword indices, not byte
offsets**, and no byte map was verified.

---

### The console tuning block identified — it is the render settings

**New document.** `00-Engine-Core-Runtime/Developer-Tuning-Console/what-the-console-tunes.md` —
`PARTIAL`, tier 2, all nine sections. Gates clean (1,069 links; `verify_doc_addresses` ok).

**The 1,132-byte block at `02CB7FD0`–`02CB8438` holds FFXII TZA's render settings.** Five of its 25
referencing functions carry strings that name it outright: **`EnableYebis`, `EnableAO`, `EnableDof`,
`EnableShadow`, `EnableIBL`, `EnableMapNormalMap`, `AODepthFullRes`, `ShadowBias`,
`ShadowValueB/G`** in `001C7940` and `001C3D50`; the debug-menu renderer `001CD0E0`
(`"%s NOT EDITABLE"`, `"(EMPTY)"`, `" steps (O to capture)"`); a render pass list in `00187950`
(`"Post Process : color correction"`, `"update shadowmap"`); and `PhyreScene::enable/disableMsaaInternal()`.

**`EnableYebis` names the middleware** — so one console dial switches the entire post-processing
layer whose 325 techniques I catalogued an hour ago.

**And the loop closes across three authoring routes.** `001C3D50` and `001C7940` are **the same two
functions** that reference `mDofFocusDistance`/`mDofApertureFnumber` from the cutscene JSON sidecar.
So depth of field is authored three ways — a console dial, a per-scene JSON override, and the
`fParam_FocusDistance` shader uniform — **and two of them meet in the same pair of functions.**
Recorded as a **shared-consumer argument, not a traced dataflow**; no path was followed between
them.

**The control is the part worth carrying.** These are floats: **an integer-only form list finds
almost nothing in this block**, and — this is the trap — **it would still have found the console**,
because the arms use `addss`. It would have missed every consumer and **supported the opposite
conclusion, that the block is console scratch.** Control: the 91 arms the TSV lists as touching the
span must appear, and they do (all inside `001D1660`). PASS.

**Where I disagree with the handoff, unreconciled:** the work order says **28** referencing
functions, my scan finds **25**. My form list is certainly not exhaustive — three of my scans today
were too narrow — and a register loaded by an earlier `lea` is invisible to it. **Take 25 as a
floor**; the qualitative claim that most readers are outside the console is unaffected.

**`01F82D20`, the hottest console address, is characterised and NOT identified.** 61 referencing
functions spanning the console, the debug menu, `InputManager_*`, and a large `0079xxxx`–`007Axxxx`
audio-driver cluster; every access a `MOV r32` read. **A global read by audio, input and UI alike is
not a render setting**, and I stopped rather than guess.

**Generalisation audit:** the block's identification rests on **five functions of the twenty-five**
— the other twenty carry no strings — and on their string tables rather than a resolved
name-to-offset binding. **Naming the block is not naming its fields**, and §4 publishes no offset
map because none was verified. The obvious next job is tractable: a name and its offset meet inside
`001C7940`.


### Correction to my own published numbers — the site counts in `what-the-console-tunes.md` were inflated

**Fixed in the document; recorded here because the earlier entry below carries the pre-correction
framing.** `F3 0F 10 05` (`movss`) matched my `MOVSS load` form at the `F3` byte **and** my `MOVUPS`
form at the `0F` byte, computing the same target from two site addresses; REX-prefixed integer forms
doubled the same way at the `48` and at the opcode. The scan advanced one byte after a match instead
of past the matched instruction.

| function | published | correct |
|---|---:|---:|
| `001D1660` | 337 | **254** |
| `001CD0E0` | 158 | **79** |
| `006084B0` | 14 | **7** |
| `00186CD0` | 9 | **7** |
| `001F0AD0` / `001C7940` / `001C3D50` | 154 / 30 / 19 | unchanged |

**Function counts (25, and 61 for `01F82D20`) were never affected** — a doubled site still names the
same function — and no identification moves, because those rest on strings.

**This defeats the known-positive control.** The three matcher defects I logged earlier were
*absences*, which a known-positive catches because the scan fails to find something you know is
there. **An over-count finds the positive perfectly.** The tell was internal: `MOVSS load` and
`MOVUPS` reporting **82 and 82**, then **78 and 78**, then 5/5 and 1/1. Two independent forms do not
land on identical counts four times.

> **For an absence defect the tell is a disagreement with the world. For an inflation defect the tell
> is a suspicious agreement inside your own output.**

**And the failed first repair nearly closed it.** Deduping by site address produced *identical*
numbers — the two matches have different site addresses, so site-dedupe cannot help — which reads as
"no bug after all". **A fix that changes nothing is evidence about the fix, not about the defect.**
The only reason it stayed open is that the 82/82 pairing survived the failed repair and was still
sitting in the output.

---

### Name-to-offset binding done — 29 settings named, and the block is two things, not one

**`what-the-console-tunes.md` section 4 replaced.** It previously read "Not established,
deliberately".

**The mechanism.** Both loaders run one idiom per setting: look the name up in the scene's map; if
the tag is `6` (absent) fall back to the global default map at `01F813C8`; look it up again; read it
through a typed reader; store it.

```
001FF740   wraps the C-string key and returns the container node   (EASTL doc's name kept)
00200BE0   tag == 6            -> "absent"
00200B50   tag 2 -> cvtpd2ps | tag 1 -> cvtdq2ps | else xorps      -> float in xmm0
00200B80   tag 1 -> mov eax   | tag 2 -> cvttsd2si | else 0        -> int
```

`00200B50` and `00200B80` were read **from their bytes**. Ghidra types `00200B50` as `void` — it
does not model the `xmm0` return — and taking that signature at face value would have made every
float setting look like a discarded read.

**Result: 29 offsets named, 21 of them console-arm addresses**, all floats. The table is in the
document. Highlights: `mDebugWater*` occupies eight consecutive slots `+074..+090`;
`chrFresnelSpecular{Intensity,Power,ClampValue,SkinIntensity}` occupies `+0D0..+0DC`;
`mMapAmbientColor` **R/G/B** is `+0A0/+0A4/+0A8`.

**The structural finding is bigger than the table.** `001F0AD0` writes **144** block addresses and
**not one of them is touched by a console arm**. The two populations are disjoint, so the range is
not one settings array:

```
+000..+18C  console-tunable settings          84 arm addresses, 21 now named
+190..+38C  8 x (vec4 + 3x4 matrix)           001F0AD0, from one live render object,
                                              block stride 0x40, object stride 0xD8, both exact
+3B0..+434  scalars and two vec3s             001F0AD0
+438..+444  four mMapShadow* settings         loaders only; no arm, no 001F0AD0 write
+464..+468  two arm addresses                 unnamed
```

**A second settings run** at `01DFE198`/`01DFE19C` and `01F82ED8`-`01F82F08` carries eleven more
named settings — `mMapChrAmbientIntensity` **RGB**, `mMapChrAmbientOffset` **RGB**,
`mMapChrDirLightColorIntensity` **RGB**, `mChrShadowSlopeOffset`, `mChrShadowDepthBias`. Two slots
inside it, `01F82EE4` and `01F82F04`, are named by neither loader. **This does not bear on
`01F82D20`** — proximity in uninitialised `.data` is not evidence, and that question stays open.

#### The method, and the rule it had to replace

**The obvious binding rule — take the string nearest the store — is wrong 26 times out of 30 in
`001C7940`, and it fails silently.** The compiler schedules the next setting's `lea rdx,"name"`
before the current setting's store, so the nearest string is usually the *following* setting's name.
The result is a table shifted by one, and a shifted table reads perfectly plausibly: it puts
`chrFresnelSpecularPower` at `+0D0` and `chrFresnelSpecularClampValue` at `+0D4`, one slot off, in a
run where every name is a `chrFresnelSpecular*`.

| function | adjacency agrees | adjacency wrong |
|---|---:|---:|
| `001C7940` | 4 | **26** |
| `001C3D50` | **19** | 0 |

> **`001C3D50` would have validated the adjacency rule 19 out of 19.** A session that checked its
> method on that function and applied it to `001C7940` would have published twenty-six wrong rows
> with a passing control behind it. **A heuristic verified on one function is verified on one
> function** — the two differ only in how the compiler scheduled them, which nothing in the method
> can see.

**The control that catches it is semantic.** Four RGB triples appear across the two loaders. A colour
triple must land on three consecutive slots in R, G, B order; the dataflow binding puts all four in
that order, and adjacency puts `mMapAmbientColorB` at **both** `+0A0` and `+0A4` and loses R
entirely. The parse never saw the letters.

> **A third species of instrument defect, after the absences and the over-count: an absence
> disagrees with the world, an over-count agrees suspiciously with itself, and a mis-binding does
> neither — it produces a complete, plausible, well-formed answer. What catches it is a fact about
> the subject matter the instrument had no access to.**

#### Independence audit, as asked

`001C7940` and `001C3D50` agree on all 19 offsets they both bind, zero disagreements. **They are not
clones** — 153 settings against 97, 61 names unique to the first and 5 to the second, different
order, different lookup wrappers. So the agreement corroborates that the extraction is not a parser
artifact. **It is weaker corroboration of the binding itself**, since both were written by the same
authors against the same names. The independent check on the binding is `001F0AD0`: its 144
addresses and these 29 are perfectly disjoint, and a mis-assigned set has no reason to be disjoint
from an unrelated function's write set.

#### Denominators

29 offsets named, of which **21** are console-arm addresses (8 of the 29 have no arm). `001C7940`
loads **153** distinct settings and only **29** reach the block — most go to a settings object at
`01F81300`, so **naming the block did not name most of the settings, because most of the settings
are not in it.**

#### `001FF740` — a three-way name collision, resolved by someone else mid-edit

`check_consistency` flagged `001FF740`: the EASTL document had
`eastl_string_construct_from_cstring`, I had written `Map_FindByName`. I dropped mine and adopted
theirs. **While I was still editing, another session settled it a third way** —
`EASTL_LookupByCString`, with a correction section appended to *this* document saying neither
original name was right. That name now stands and I have left it alone.

**One refinement their section does not have, and it is a step in the same chain.** It places the
find in `001FF6B0`. `001FF6B0` does not return — it **tail-jumps**: its body ends
`E9 BE FD FF FF` (`jmp 001FF4F0`), not `E8` + `RET`, and `001FF740` ends `mov rax, rbx` / `ret`. So
**`001FF4F0` is the find**, `001FF6B0` is the "ensure this variant is a map, then find" wrapper, and
`001FF740` is the C-string adapter over both. Ghidra types `001FF6B0` as `void` because it does not
model a value returned through a tail call — **the same modelling gap that types `00200B50` as
`void`**, which is the second time in one pass that a Ghidra signature would have hidden the value
everything downstream reads.

**A process note, not a complaint.** Two sessions edited this document within the same few minutes,
and my second splice failed its exact-match guard rather than clobbering the other session's text.
That guard is why nothing was lost — a blind write would have silently reverted their correction
section. **Read-modify-write with an exact-match assertion, not a blind splice**, whenever a document
is one another session may also be holding.

**Gates:** `check_links` 8,159 relative links resolve; `verify_doc_addresses` 0 non-function `.text`
citations; `check_consistency` 0 name / size / caller-count disagreements.


### `PROPOSED-repos9e-26` ANSWERED — the eight entries are shadow-map matrices, and my own layout claim was wrong

**The call site settles it without an inference.** `001F0AD0`'s only caller is `00187950`, the render
pass list, and the call sits inside a **named scope**:

```c
FUN_001D5630(marker, ctx, "update shadowmap");     // scope OPEN - the name is an argument
  if (flag == 0)  FUN_001F0AD0(src, ctx, param_1 + 0x690);
  else          { FUN_001F0AD0(src, ctx, param_1 + 0x358); flag = 0; }
FUN_001D5620(marker, ctx);                         // scope CLOSE
```

`001F0AD0` is the **only** call between open and close, in either arm. Same construct as
`"display : draw Font"` in the glyph document — a name passed as an argument to a scope-open, not a
string that happens to be nearby.

**Where they come from.** `001F0AD0` calls `001EF6D0` immediately before the copies, and `001EF6D0`
walks the same array:

```c
plVar25 = (longlong *)(object + 0x148);
do {
    *(float *)(plVar25 + 0x18) = ...;  (**(code **)(*plVar25 + 8))(plVar25);   // set, recompute
    *(float *)(plVar25 + 0x19) = ...;  (**(code **)(*plVar25 + 8))(plVar25);
    FUN_0018A120((longlong)i * 0xD8 + 0x150 + object);
    i++;  plVar25 = plVar25 + 0x1B;                // 0x1B qwords = 0xD8
} while (i < *(int *)(object + 0x13C));
```

Each entry is an **object with a vtable** — vtable `+0x00`, the 64-byte matrix `+0x78`, parameters
`+0xC0/+0xC4/+0xC8/+0xD0`, size `0xD8`. A float written, a virtual slot called to recompute: a camera
or frustum retargeted per shadow slot.

**Eight slots, and a live count.** The copy is unrolled eight times with no guard, so all eight are
always copied; how many are *in use* is `object+0x13C` — the same field that bounds the loop — and
`001F0AD0` copies it to **`block+0x3E4`**.

**And the whole block is one shader constant buffer.** `006084B0` copies every part of it into one
destination object: `+000..+18F` sixteen bytes at a time to `dest+0x110`, `+190..+44F` in one
704-byte `005DEC50` call to `dest+0x2A0`, `+450..+470` field by field. Nothing left out, nothing
interleaved.

#### The correction, and it is the same mistake I had just finished writing up

**I published "8 x (vec4 + 3x4 matrix)". It is 8 x one contiguous 64-byte entry.**

The compiler emits each entry's last twelve dwords before its first four. I grouped the 144 stores
**in emission order**, saw `4 then 12`, and wrote that down as the layout. Re-merging by *constant
delta and destination contiguity*, with emission order discarded, collapses the sixteen dwords into
one 64-byte run in both spaces — and sixteen contiguous floats on a 64-byte stride is a 4x4 matrix.

> **This is the adjacency defect again, one section later, in a different costume.** For names I had
> just proved that instruction order is not semantic order — 26 of 30 wrong — and then read
> instruction order as *structure* in the very next paragraph. **Knowing a rule and applying it are
> different acts**, and the first does not perform the second.

**What should have caught it earlier:** two runs with the *same delta* whose destinations are
adjacent are one run. My grouper required emission adjacency as well, so it split every entry in
two. **A merge that respects the order the compiler chose is measuring the compiler, not the data.**

#### A third Ghidra signature gap in the same pass

`001F0850` returns the source object — the global at `01F82EA8` — and Ghidra types it `void` and
decompiles it to an empty body. That is the third in this pass, after `00200B50` (`xmm0` return not
modelled) and `001FF6B0` (returns through a tail call). **A decompiler's return type is a claim about
a function, and in this executable it has been wrong three different ways.**

**Not used as evidence:** `01F82EA8` sits in the same uninitialised `.data` neighbourhood as the
second settings run at `01F82ED8`-`01F82F08`. That is allocation, not meaning, and nothing here
rests on it.

**Gates:** `check_links` 8,184 relative links resolve; `verify_doc_addresses` 0 non-function `.text`
citations; `check_consistency` no address described two different ways.


### `PROPOSED-repos9e-25` ANSWERED — and the answer was hidden by an instrument limit, not by a missing form

**`-25` asked what initialises the 65 console-arm addresses no loader binds. The premise of my own
question was wrong: the block is not uninitialised data.** It is a **C++ static object** with a
constructor and an `atexit` destructor. `00162410` is the static initializer, and its whole body is
four instructions:

```asm
00162414  48 8D 0D B5 5B B5 02   lea  rcx, [rip+0x2B55BB5]   ; -> 02CB7FD0, the block
0016241B  E8 00 A3 47 00         call 005DC720               ; the constructor
00162420  48 8D 0D 99 93 74 00   lea  rcx, [rip+0x749399]    ; -> 008AB7C0, the destructor
0016242A  E9 60 67 6A 00         jmp  atexit
```

`005DC720` calls two field-setters, arguments fixed by the bytes rather than inferred:

```asm
005DC742  48 8B F9              mov  rdi, rcx        ; rcx is still the block base
005DC745  E8 36 FE FF FF        call 005DC580        ; 005DC580(block + 0x000)
005DC74A  48 8D 8F D0 00 00 00  lea  rcx, [rdi+0xD0]
005DC751  E8 DA FC FF FF        call 005DC430        ; 005DC430(block + 0x0D0)
```

Between them the chain writes **107 distinct block offsets** — `+000..+0C4`, `+0D0..+180`,
`+42C..+468` — covering **57 of the 65**. The object runs out to `+0x1020`; the 1,132-byte "block"
is only the part console arms touch.

#### The instrument limit is the finding

I ran a **widened** store scan first — read-modify-write forms, `INC`/`DEC`, the shift group, the
SSE stores, `CMPXCHG`/`XADD`, with the `/reg` field checked so `CMP` and the non-writing `FF` forms
are excluded — and a **known-positive control that passed** (over the 29 named addresses it found
both config loaders, and two writers I had not known about). It reported **131 stores over the 65,
all from `001D1660`, and nothing else in the image.**

> **That absence was true for the instrument and false about the program.** The constructor writes
> through `this`: every store is `[rcx+disp]` and carries no absolute address for a RIP-relative
> matcher to match. **The hole was not a missing instruction form — it was the addressing mode
> itself**, and no amount of widening the form list would have closed it.

**This is a fourth species for the taxonomy, and it is worse than the other three.** An absence
defect is a form the matcher cannot see; widen the forms and it goes away. **This is a whole class
of writes the matcher's *addressing model* cannot see, and a known-positive control drawn from the
same addressing mode passes cheerfully.** My control used absolute-addressed writers to validate a
scan whose blind spot was non-absolute writers.

> **A control can only certify the axis it varies.** Mine varied instruction form and certified
> instruction form. It said nothing about addressing mode, and I read it as if it had.

**What found it anyway:** following the seven `LEA`s of an address *inside* the block, rather than
the stores. Six take `block+000`. One of them is `00162410`, 32 bytes, and it is the static
initializer. **The pointer escape I had listed as a caveat was the answer.**

#### The defaults, and a third independent check on the binding

**27 of the 29 named offsets have a constructor default, and they read as their names** —
`mDebugWaterParallaxFactor` 0.04, `chrFresnelSpecularClampValue` −0.8, `mCubemapIntensity` 0.6,
`mMapShadowFadeSpeed` 0. The full table is in the document. `005DC580` carries no strings and knows
nothing about any name.

**`mMapAmbientColor` R/G/B defaults to 1 · 1 · 1 — white.** Under the adjacency binding the same
three names read **2 · 1 · 1**, which is not a colour anybody defaults to. **The defaults
discriminate the two candidate bindings and pick the one dataflow picked.**

**And the second control I tried does not discriminate, which I am reporting rather than dropping.**
`mEyeA…` and `mEyeB…` both default to 0.66 — an A/B pair sharing a value, which looks like
confirmation. Under the adjacency binding both read 0.02: equal as well. **A control that agrees
with you is not a control unless the alternative would have disagreed.**

#### A hypothesis I nearly published, killed by measuring it

`005DC430`'s first three values are `005DC580`'s second, third and fourth. That invites reading
`+0D0..+180` as the same struct shifted — which would have mapped every named offset onto an unnamed
twin and looked like a major structural result. Tested across all fields at every 4-byte shift:
**best 4 of 38 overlapping fields; at shift 0, 0 of 37. Rejected.**

**And the first version of that test was broken** — `005DC430` takes `undefined4 *`, so
`*(undefined1 *)(param_1 + 0x2a)` is byte `0xA8`, not byte `0x2A`, and I had scaled only the
subscript form. It rejected the hypothesis anyway. **A test that gives the right answer for the
wrong reason is not a test**, and if the hypothesis had been true that run would have rejected it
just as confidently. I only trusted the verdict after fixing the units and re-running.

> **Three consecutive values agreeing at the head of a sequence is not a shifted copy.**

#### Two corrections to this document

1. **"Uninitialised `.data`, built at run time, no file image; there is nothing to patch in the
   file"** — wrong on every clause. The defaults are immediates in `.text` and are patchable, and
   they, not `001F0AD0`, are where a default comes from.
2. **"Nothing else writes them afterwards"** — true for 28 of the 29 named settings. `mCubemapIntensity`
   at `+168` is also stored once each by `001846B0` and `001846F0`, both found by the widened scan.

**Gates:** `check_links` 8,209 relative links resolve; `verify_doc_addresses` 0 non-function `.text`
citations; `check_consistency` no address described two different ways.

---

## CALL-CHAINS / ADDRESS-INDEX

New chain, both directions, owner transition marked:

```
message / menu / HUD text
  -> 0053E0B0   scrolled window line loop, cull + colour modulate   [TRIGGER]
     -> 002D8690 / 002D87D0   renderer selection
        -> 00364980   record starts "ex"?  yes -> 002B0280
        -> 003649A0   no -> glyph-run quad emitter
           -> 003647E0   control codes 1/2/3, U+0020, U+3000, '{'
              -> 00366110   {tag} interpreter, 11 tags
                 -> 003656A0                    measure, for {a}
                 -> 00203170, 00366690, 00202F70  build the {r} matrix at 022CBE00+0x1E0
           -> 00365FD0 / 00364210   glyph LRU cache hit / miss-and-fill
           -> 003666E0               log2 for the texture descriptor
           -> 00474650               glyph pixels -> graphics local memory 0x3440
           -> 00202B90               rotate the four corners
           -> 003A2090 / 003A2020    subpacket open / close        [OWNER TRANSITION]
           -> 003A1DB0               submit and swap at 0x180 records
           -> 0017F850               close scope "display : draw Font"

  -> 00364530   measure-only walk, same glyph table, no drawing
```

New `ADDRESS-INDEX` entries — functions:

| Address | Body | Name |
|---|---:|---|
| `003649A0` | 3020 B | `Text_EmitGlyphRunQuads` |
| `00366110` | 1318 B | `Text_InterpretBraceTag` |
| `00364530` | 684 B | `Text_MeasureGlyphRun` |
| `0053E0B0` | 718 B | `Text_DrawScrolledWindowLines` |
| `003647E0` | 366 B | `Text_HandleControlCodes` |
| `00364210` | 367 B | `GlyphCache_FillOnMiss` |
| `00365FD0` | 171 B | `GlyphCache_PromoteOnHit` |
| `003666E0` | 88 B | `Log2OfPowerOfTwo` |
| `00364980` | 24 B | `Text_IsExPrefixed` |
| `00202B90` | 181 B | `Vec3TransformByMatrix` |
| `00203170` | 60 B | `LoadIdentityMatrix4x4` |
| `0017F850` | 38 B | `FontScope_CloseAndFlush` |

Data addresses — **not** for the function index:

| Address | Kind | Contents |
|---|---|---|
| `008C5B18` | `.rdata` string | `"display : draw Font"`, one code reference (`0017F854`) |
| `00366638` | `.text` jump table | 22 dword RVAs, dispatch for `00366110` |
| `01CEBC84` | `.rdata` f32 | `16.0` — texture-coordinate fixed-point scale |
| `01CEBB70` | `.rdata` f32 | `0.5` — half-texel inset |
| `01CEBBA8` | `.rdata` f32 | `1.0` — the "unscaled" comparand |
| `008F3134` | `.rdata` f32 | `100.0` — the `{s}` percent divisor |
| `008C5F80` | `.rdata` f32[16] | the 4×4 identity, rows at `+0x00/+0x10/+0x30/+0x50` |
| `00D10F40` | `.rdata` strings | allocator labels, referenced directly by residual `0036A570` |

New `ADDRESS-INDEX` entries from the console name-binding pass — functions:

| Address | Body | Name |
|---|---:|---|
| `00200B50` | 41 B | `Variant_ReadFloat` — tag 2 `cvtpd2ps`, tag 1 `cvtdq2ps`, else `0.0f`; Ghidra types it `void` |
| `00200B80` | 31 B | `Variant_ReadInt` — tag 1 `mov`, tag 2 `cvttsd2si`, else `0` |
| `00200BE0` | 8 B | `Variant_IsAbsent` — `tag == 6`, selects the global default map |
| `00193F70` | - | setter, writes `+0x1E9` of the settings object |
| `00194300` | - | setter, writes `+0xF0` of the settings object |

`001FF740` and `001FF6B0` are **not** proposed for renaming — the EASTL document owns them.

Data addresses — **not** for the function index:

| Address | Kind | Contents |
|---|---|---|
| `02CB7FD0` + `0x000..0x18C` | `.data`, uninitialised | console-tunable settings; 84 arm addresses, 21 named |
| `02CB7FD0` + `0x190..0x38C` | `.data`, uninitialised | 8 x (vec4 + 3x4 matrix), written by `001F0AD0`, no arm |
| `01F813C8` | `.data` | the global default settings map used when a key is absent |
| `01F81300` | `.data` | the settings object most of the 153 settings land in |
| `01DFE198` / `01DFE19C` | `.data` | `mMapChrUpwardDirLightAngleThres` / `mMapChrUpwardDirLightColorIntensity` |
| `01F82ED8`-`01F82F08` | `.data` | the second settings run, 11 named, 2 slots unnamed |

New `ADDRESS-INDEX` entries from the `-26` read — functions:

| Address | Body | Role |
|---|---:|---|
| `00187950` | 3,311 B | the render pass list; opens `"update shadowmap"` and calls `001F0AD0` inside it |
| `001F0AD0` | 2,738 B | the shadow-map block update: builds via `001EF6D0`, then copies 144 fields into the block |
| `001EF6D0` | 3,731 B | builds the per-slot frustum objects, `object+0x148` stride `0xD8`, loop bound `object+0x13C` |
| `006084B0` | 1,419 B | fills the shader constant buffer from the whole block |
| `005DEC50` | 1,924 B | unrolled 704-byte copy, `block+190..+44F` into the constant buffer |
| `001F0850` | 66 B | returns the source object `01F82EA8`; Ghidra types it `void` with an empty body |
| `001D5630` / `001D5620` | - | named GPU scope open / close; the name is an argument |

Data addresses — **not** for the function index:

| Address | Kind | Contents |
|---|---|---|
| `01F82EA8` | `.data` | the shadow render object `001F0AD0` copies from |
| `02CB7FD0` + `0x190..0x38F` | `.data` | eight 64-byte shadow matrices, block stride `0x40` |
| `02CB7FD0` + `0x3E4` | `.data` | the live shadow-slot count, from `object+0x13C` |

New `ADDRESS-INDEX` entries from the `-25` read — functions:

| Address | Body | Role |
|---|---:|---|
| `00162410` | 32 B | static initializer for the tuning block: constructor + `atexit(destructor)` |
| `005DC720` | 362 B | the block's constructor; writes `+42C..+468` and out to `+0x1020`, calls the two setters |
| `005DC580` | - | defaults for `block+000..+0C4`, 45 fields |
| `005DC430` | - | defaults for `block+0D0..+180`, 41 fields; **not** a shifted copy of `005DC580` |
| `008AB7C0` | 12 B | the `atexit` destructor; calls `005DDDB0(block)` |
| `005DDDB0` | 186 B | teardown |
| `00607F00` | 154 B | stores the block base into `*(obj+0x98)` — a second pointer escape |
| `001846B0` / `001846F0` | - | each stores `mCubemapIntensity` (`block+168`) once |
