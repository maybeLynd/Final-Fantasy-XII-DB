---
system: The blinking icon and its atlas
category: 99-Unresolved-Residual
status: AUDITED — both reservations closed 2026-09-18: 0208F570 is the 60 Hz tick counter the UI frames advance by the present interval, and 002DD7E0's dwords are fontcolor.bin's face colours (grey everywhere the file does not ship); see §5's table
owner_layer: CodeDomain:Presentation.Icon
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN161 -> GN162 - REPLACED 2026-09-21 (OPUS), because the snapshot-identity basis this block carried is FALSE at GN162: this document cites record(s) 002B6350, which batch R30 touched. The weaker basis HOLDS and is measured: the advance changed 30 records in comment and tags ONLY - 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten (check_delta_additivity.py GN161 -> PARENT, control passed) - and check_stranded_absence.py, sweeping the GN160 resolved set which strictly CONTAINS all 30, reports no live absence claim on any line of this document
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    voided_by: any delta that REMOVES or REWRITES a comment, tag, name, prototype or body range - re-run the additivity test at each checkpoint
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-03
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: residual-walk-repos-55
  crossref_clean: true
  reopened_count: 0
---

# The blinking icon and its atlas

**`002B8EE0`, 2,865 bytes, residual when surveyed — classified at GN161 `Presentation.Icon.PulsingIconDrawFromAtlasOrResource` — and the thing it does that nothing else in the database
records is make an icon pulse.**

## 1. What the player sees

**An icon that breathes.** Its brightness rides a sine wave with a period of **exactly 60 frames** —
one second at 60 fps — and the depth of the pulse is **authored per icon**, not fixed. An icon whose
record carries a pulse amount of zero does not move at all.

**The same routine draws the icon three different ways** depending on what the record asks for: a
plain stamp from a packed atlas, a two-pass draw with an outline or shadow underneath, and a variant
that walks a list of **sub-items and draws each one** on top.

## 2. The pulse

```c
fVar16 = sinf((DAT_0208F570 * 3.1415927f) / 30.0f);
```

**`DAT_0208F570` is a frame counter and the argument advances by `π/30` per frame**, so the sine
completes a cycle every **60 frames**. It is evaluated twice, in the two branches, and applied to the
same field — `context + 0x5A` — in two different ways:

| branch | what the pulse does |
|---|---|
| atlas path | `+0x5A = base + sin × (((base >> 1) × amount) >> 8)` — **modulates around the record's own brightness**, by a fraction of it |
| resource path | `+0x5A = 128.0 + sin × ((amount << 4) >> 8)` — **modulates around a fixed 128**, ignoring the base |

> **Two pulses with the same period and different centres.** The first keeps an icon's authored
> brightness and breathes around it; the second discards it and breathes around the midpoint.
> **`amount` is `record + 0x50` in both**, so one authored number drives both shapes.

**And the pulse is skipped entirely** when `record + 0x50` is zero (atlas path) or when bit 15 of the
flags at `record + 0x28` is set (resource path).

## 3. The atlas

When `record + 0x02 == 1` the icon comes from a packed atlas reached through `param_5 + 8 → +0x20`:

```c
atlas = *(longlong *)(*(longlong *)(param_5 + 8) + 0x20);
index = atlas[0x44 + atlas[0x44] * 2] + record[0x20];       // a two-level index
base  = atlas + 0x30 + atlas[0x40];                          // the entry array
entry = base + index * 8;                                    // 8 bytes per entry
u = *(uint *)(entry + 4)        & 0xFFF;                     // two 12-bit fields
v = *(uint *)(entry + 4) >> 12  & 0xFFF;
pal = *(byte *)(entry + 7);
context[0x5C] = atlas[0x30 + atlas[0x42] + (pal >> 4)] + (pal & 0xF);
```

**Read at instruction level** — the 12-bit mask is a literal and the stride is in the addressing
mode:

```asm
002B904B  mov   r11d, 0xfff                          ; the 12-bit mask
002B9058  movd  xmm1, dword ptr [0x0209E5AC]         ; a global Y offset added to the position
002B908E  movzx eax, word ptr [rdx + r8*0x8 + 0x4]   ; entry stride 8, field at +4
002B9094  and   ax, r11w                             ;   u = entry[+4] & 0xFFF
002B909D  mov   eax, dword ptr [rdx + r8*0x8 + 0x4]
002B90A2  shr   eax, 0xc
002B90A5  and   ax, r11w                             ;   v = entry[+4] >> 12 & 0xFFF
```

**Three separate `ushort` offsets in the atlas header do three different jobs** — `+0x40` locates the
entry array, `+0x42` a palette-remap table, `+0x44` an index table that is itself indexed by its own
first element. **`record + 0x20 == 0xFF` is the "no icon" sentinel** and returns immediately.

> **A 12-bit-packed pair and a nibble-split palette byte** is a PlayStation-2-era atlas format, and
> it is reached only when the record says `kind == 1`. The other kinds carry an explicit width and
> height at `record + 0x24` / `+0x26` instead.

## 4. Colour comes from a shared table with a grey fallback

Every colour in this function is fetched by id:

```c
undefined4 FUN_002dd7e0(uint id) {          // 002DD7E0
    if (0 <= (int)id && id < DAT_0215E6B8 && DAT_0215E6C8 != 0)
        return *(undefined4 *)(DAT_0215E6C8 + id * 8);
    return 0x80808080;
}
```

**Six ids are used — `0x6B`, `0x6C`, `0x6D`, `0x6E`, `0x6F`, `0x70` — in three pairs**, one pair per
drawing path, and each pair is passed to `002752E0` together with the pulse amount to produce a
blend. **The table has 88 callers image-wide**, so it is the engine's shared UI palette rather than
anything this function owns.

> **The fallback is `0x80808080`**, and `0x80` is `1.0` in the 1/128 fixed point the text renderer
> also uses. **An out-of-range colour id does not fail — it draws at flat mid-grey.**

**And the blended result is immediately overwritten** by four bytes from `01E0CE60`–`01E0CE6C`, with
the last scaled by the icon's brightness. **The blend is computed and then discarded on both paths
that compute it** — reported as measured; whether the store is dead or the overwrite is conditional
in a way the decompilation flattens is **not established.**

## 5. ~~Reached only through a table~~ Reached through nothing admissible

> **CORRECTED 2026-09-16 (OPUS), on `FABLE-CONTRA-OPUS-THE-BLINKING-ICON-IS-REACHED-ONLY-THROUGH-AN-EXCEPTION-SCOPE-TABLE`.**
> The sentence below called `01D70800`/`01D70810` a *dispatch table of 4-byte RVAs*. They are not
> a dispatch table. FABLE decoded them as **record 0 and record 1, FIELD 2 — the Handler slot** —
> of a `SCOPE_TABLE` spanning `01D707F4`–`01D72AF8` with count 560, reached from a `RUNTIME_FUNCTION`
> whose `UNWIND_INFO` carries an EHANDLER/UHANDLER flag. What looked like *“a record pairing
> `002B7B80` with `002B8605` and a data pointer”* is `{Begin, End, Handler, JumpTarget}` with
> `Handler = 002B7B80` and `JumpTarget = 002B8605`.
>
> **THE ALIGNMENT, PROVED 2026-09-16 (OPUS) on `AUDITSPEC-REQ-OPUS-BLINKING-ICON-SCOPE-TABLE`.**
> SWE2-AUDIT-SPEC verified these records from the image and read `002B7B80` as **field 0, Begin**;
> FABLE read it as **field 2, the Handler**. Both quoted real bytes. They disagree because they read
> on different 16-byte grids, and **only one grid divides the table**:
>
> ```
> count dword at 01D707F4 = 0x230 = 560
> 01D72AF8 - 01D707F8 = 0x2300 = 560 x 16   exactly
> 01D72AF8 - 01D70800 = 0x22F8 = 559.5 records   impossible
> ```
>
> Records begin at `01D707F8`. **A window opened at `01D70800` straddles two of them**, which is why
> it still looks coherent — it shows `{002B7B80, 002B8605, …}` because those are fields 2 and 3 of
> one record followed by fields 0 and 1 of the next. On the proven grid:
>
> ```
> record 0  01D707F8  {00140921, 00389809, 002B7B80, 002B8605}
> record 1  01D70808  {01D707C0, 0x21,     002B7B80, 002B8605}
> record 2  01D70818  {01D707C0, 00140821, 0022E408, 002B7590}
> ```
>
> **FABLE's field index is right and this paragraph needs no correction.** The proof is recorded
> because the misaligned reading is the one you reach for naturally — you land on it by opening a
> window at the address this page names.
>
> **Not asserted:** the column NAMES beyond position. Record 1's field 0 points into `.rdata`, so the
> shape is not a plain `C_SCOPE_TABLE`, and an alignment argument cannot settle what all four columns
> are called. The conclusion both peers share is untouched: these are 16-byte exception-table
> records, banned as evidence.
>
> **The conclusion survives and gets stronger, which is why this is a repair and not a withdrawal.**
> Both “references” are fields of exception metadata, which this database bans as evidence — the
> same ban this section's own note below applies to a *third* xref.
>
> **~~So `002B7B80` has no admissible static reference at all.~~ CORRECTED THE SAME DAY (OPUS), and
> the withdrawn sentence was mine, not FABLE's.** Everything above this line stands. What followed it
> went one step past the evidence: there IS an admissible reference, and it is ordinary code.
>
> ```
> 002B6427  lea r8, [rip + 0x1752]      ->  002B7B80        (inside 002B6350)
> 002B6474  call 0x245000               rcx=obj  rdx=0xBC08  r8=the address  r9=&local
> ```
>
> `r8` is written nowhere between the two, so the address is passed as the **Win64 third argument**
> to `00245000`. A function address materialised into an argument register is a **use**, not metadata.
>
> **How it was missed is the part worth keeping.** The absence rested on `get_xrefs_to`, which
> reported three. An absence claim needs an image-wide, boundary-free sweep, and that rule was
> available before the sentence was published. Swept with a positive control — `0020E600`, 4,365
> call sites found — `002B7B80` has: **1 `LEA` in `.text`**, 2 RVA words in `.rdata` at the scope-table
> Handler slots, 1 in `.pdata`, and **38 four-byte coincidences inside `.text` instruction streams**
> that are not references at all. A raw byte count would have said 42.
>
> **The holder of the missing reference was one of the residual thirty, and that thirty is now zero.** `002B6350` carried no
> `CodeDomain` when this was written; GN162 classified it `UI.MapScreen.TrackMapContainerBuild`. Whether the unanalysed residue is *where missing xrefs hide* — which would make
> the residual-30 work a correctness debt and not only a completeness one — is a question this
> page raises and does not answer.
>
> The heading still stands corrected: there is no table. But something admissible does reach it.
>
> Section 7's open question — *what the dispatch table at `01D70800` dispatches on* — is answered
> and withdrawn by the same decoding: it dispatches on nothing, because it is not a dispatch table.
>
> ---
>
> ### SUPERSEDED THE SAME DAY — it is not a `SCOPE_TABLE` either. They are CHAINED `RUNTIME_FUNCTION` entries.
>
> **Everything above about the `SCOPE_TABLE` is withdrawn**, on
> `FABLE-CONTRA-OPUS-REINSTATED-THE-TABLE-IS-CHAINED-RUNTIME-FUNCTION-ENTRIES`, which FABLE filed
> after withdrawing their own scope-table contradiction in full. **OPUS verified the scope-table
> reading and published it, so the superseded reading was mine too.** Re-derived here from the
> authority image at this HEAD:
>
> ```
> 01D707F8  UNWIND_INFO header 0x21 -> version 1, flags 0x4 = UNW_FLAG_CHAININFO
>           SizeOfProlog 0x09, CountOfCodes 2  ->  body = 4 + 2*2 = 8 bytes, ending EXACTLY at 01D70800
> 01D70800  RUNTIME_FUNCTION { Begin=002B7B80, End=002B8605, UnwindInfo=01D707C0 }
> 01D7080C  UNWIND_INFO header 0x21, CountOfCodes 0  ->  body = 4 bytes, ending EXACTLY at 01D70810
> 01D70810  RUNTIME_FUNCTION { Begin=002B7B80, End=002B8605, UnwindInfo=01D707C0 }
> ```
>
> When `UNW_FLAG_CHAININFO` is set, what follows the unwind codes **is a `RUNTIME_FUNCTION`** — not a
> handler, not language data. Every element of the original sentence is now accounted for exactly:
> *"16 bytes apart"* is a 4-byte chain header plus a 12-byte `RUNTIME_FUNCTION`; *"pairing `002B7B80`
> with `002B8605`"* is `Begin` and `End`; and **the *"data pointer"* is `UnwindInfoAddress`**.
>
> **`01D707C0` is `002B7B80`'s OWN primary `UNWIND_INFO`**, which is why every record points there.
> Checked against `.pdata` independently: the `RUNTIME_FUNCTION` for `002B7B80` reads
> `{Begin=002B7B80, End=002B8605, UnwindInfo=01D707C0}` — match. That `UNWIND_INFO` has header `0x19`
> (flags `0x3`, no chain bit, so the control refuses it), handler `00808BA8` = `__GSHandlerCheck`.
>
> **AND THAT IS WHERE THE `560` CAME FROM.** The alignment proof above rests on *"the count dword at
> `01D707F4` is `0x230` = 560"* and on `01D72AF8 − 01D707F8 = 0x2300 = 560 × 16` **exactly**. `0x230`
> is not a record count. **It is the GS cookie offset in `__GSHandlerCheck`'s language data**, sitting
> in `002B7B80`'s own `UNWIND_INFO`. The exact division was numerology over a cookie offset, and it
> read as a proof because it was *arithmetically* perfect while being *structurally* meaningless. A
> figure that divides exactly is not thereby a count of anything.
>
> **The two sibling pages carry the same structure**, verified the same way: `01D6CC48` and
> `01D6CC98` are both `{Begin=0027CE70, End=0027CF22, Unwind=01D6CC2C}`, and `01D6F79C` and
> `01D6F7AC` are both `{Begin=002A6190, End=002A674F, Unwind=01D6F778}` — each pointing at its own
> procedure's primary `UNWIND_INFO`. Their column header, already corrected to *"excl. **all** unwind
> data"*, is right as it stands.
>
> **What does not change:** these are exception-table records and remain banned as evidence — now as
> item **six** on `EVIDENCE-STANDARD`'s list by its own name, `_IMAGE_RUNTIME_FUNCTION_ENTRY`
> records, rather than as EH maps. `002B7B80`'s admissible reference is still the `lea` at `002B6427`.
> **What the guard missed is unchanged and is the lesson:** the rule *"every `DATA` xref above the
> start of `.pdata` is unwind data"* is a **section** test where the ban names a **class**, and
> chained `RUNTIME_FUNCTION` records live in `.rdata`, **below** `.pdata`.

~~`002B8EE0` ← `002B9A20` ← `002B7B80`, and **`002B7B80` has no code callers at all** — two data~~
~~references, at `01D70800` and `01D70810`, sitting **16 bytes apart in a dispatch table of 4-byte~~
~~RVAs**, each record pairing `002B7B80` with `002B8605` and a data pointer.~~

> **`get_xrefs_to` reported a third and it is not a reference.** It lands inside `.pdata`, whose
> bounds were read from the section table rather than assumed, so the row is a
> `RUNTIME_FUNCTION` record — **exactly the unwind metadata this project bans as semantic evidence.**
> The document's own address checker flagged it before this sentence was written. **Every `DATA`
> xref above the start of .pdata is unwind data**, and an xref count including them is inflated by
> one per function.
>
> **This note names no address at all, and that is deliberate.** Writing them out — backticked or
> bare — puts them into the evidence census, and the checker cannot tell an address cited *as*
> evidence from one cited as **an example of what does not count**. It reported three violations
> when the paragraph named them properly, and two after they were merely un-backticked.
> **Discussing a banned address must not look like using one**, and the only way to satisfy that
> here was to describe them instead.

> **The whole chain is virtual-dispatched**, which is the ordinary reason a large function ends up on
> the residual list: nothing names it and nothing calls it by address.

## 6. Where it joins the database

**`002D8C80` — which this function calls twice — is already documented** as the inline-icon drawer,
in [how a line of text becomes glyph quads](Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md)
§(icon record kind): *"the icon is drawn by `002D8C80` from a different record kind in `0053E0B0`."*

> **That is the confirmation that this is icon drawing, and it is somebody else's finding rather
> than this document's inference.** Everything above would otherwise rest on the shape of the code.

**`002B8EE0` is one of the three functions in the 158 survey's residual cluster 3** — with `002BCB00` and `002DBDD0`,
6,775 bytes total — per [the unresolved 158](the-unresolved-158.md) §(clusters). **`002DBDD0` is
called from here twice**, so the cluster is a real call cluster and not just a size grouping.

## 7. Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Is the period really 60 frames? | The argument is `frame × π / 30`; a sine repeats every `2π`, so `Δframe = 2π ÷ (π/30) = 60`. **Arithmetic, not inference.** |
| Is `DAT_0208F570` a frame counter? | **Established by cross-reference 2026-09-18 (FABLE): it counts 60 Hz ticks.** Its writers are all on record ([the millisecond page](../16-UI/Widget-Object-Model/starting-a-widget-animation-and-the-millisecond-that-becomes-frames.md), the writer table): the UI frame handlers `00250540`, `002506D0`, `00250730` and `002507C0` add `00184950()` to it once per presented frame, and that getter returns `[01F3DA18]`, the DXGI present sync interval clamped to 1–3 ([game settings](../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md), DH-7) — the number of 60 Hz vblanks each presented frame spans — and only while the frame argument `02064AA0` is zero ([the frame page](../22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md)); `00228130` re-bases it from `[01FD46F4]` on message 18. So `sin(counter × π / 30)` completes a cycle every 60 ticks: **one second at 60 Hz whatever the present interval**, which is what a blink cadence needs. *(Previously: not established here — the reading, not a measurement.)* |
| Is `002DD7E0` really a palette? | **Established by cross-reference 2026-09-18 (FABLE): the dwords are the face colours of `fontcolor.bin`.** The array behind `0215E6C8` (count at `0215E6B8`) is the `fontcolor` blob `{u32 count, u64 pairs[count]}` that the kind-7 id-5 loader `0029CED0` → `002DD810` installs ([the loader-bound families](../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/loader-bound-bin-families.md), `fontcolor`); each `u64` is a colour pair, face and shadow, so `002DD7E0(id)` returns the face quad and `002DD7B0(id)` the first byte of the shadow quad. The file ships only in the `ch` and `in` locales, so in every other locale the pointer stays null and **every id yields the grey `0x80808080`** — the default is the shipped behaviour there, not a fallback. *(Previously: not established — colour was the reading.)* |
| Are the two pulse formulas really different, or one the decompiler split? | Different centres (`base` vs the literal `128.0`), different shifts (`>> 8` on `(base>>1)×amount` vs on `amount<<4`), in different branches. **Two expressions.** |
| Is the atlas two-level indexing real? | `atlas[0x44 + atlas[0x44] * 2]` — **the table at `+0x44` is indexed by its own first element**, then the record's byte is added. Unusual enough to be worth stating exactly rather than paraphrasing. |
| Why is so little of this document anchored to instructions? | **`002B8EE0` has no defined function body**, so `search_instructions` cannot see inside it — it scanned 554,739 instructions and matched none of them here. Anchors had to be recovered by direct `disassemble_bytes` on guessed ranges, and §3 is the section that got them. **The rest rests on decompilation**, and that is stated rather than papered over. |
| Could `002B7B80`'s missing callers be the empty-body artifact? | **No** — this was checked. `edges.tsv` is the complete source (see [drawing a line character by character](Glyph-Run-Rendering/drawing-a-line-character-by-character.md) §5), and the three references it has are all `DATA`. |

## 8. What this document does not claim

~~**Which subsystem's icons these are.**~~ **Answered 2026-09-26 (FABLE, Claude Opus 5.5): the track map's markers.**
[The map screens](../16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md) read the chain from the other end.
The track-map page procedure `002B7B80`'s draw arm hands its marker list to `002B9A20`. That routine calls this
function once per node (`002B9AE0`) and follows the node's `+0x60` link. So the "record" this page reads is one marker
node, and the "global Y offset" of §3 (`0209E5AC`) is the layout key `ExtraTrackMapJumpIconOffsetY`. The cluster
sibling `002BCB00` (§6) is the location map's twin. It is reached the same way, one call per marker node, and makes
the same atlas test and the same 60-tick pulse. *The paragraph
below is the earlier reasoning, kept as history.*

The `002Bxxxx` neighbourhood contains functions calling
`WorldTransition_GetActiveOrPendingFieldId` and `PersistentFlag_QueryBank2048`, which would suggest a
map or field overlay — **but those are different functions in the same address range, and a
neighbourhood is not a call relationship.** Nothing in `002B8EE0` names its own subject.

What `002D8530`, `002DBDD0`, `00403970`, `00403BC0`, `00404120` and `00404730` do. What the four
bytes at `01E0CE60` are. What `003BC160` / `003BDCD0` / `003BDB30` enumerate — only that the loop is
bounded by `003BDCD0`'s return and gated on bit 6 of `record + 0x28`. ~~What the dispatch table at
`01D70800` dispatches on.~~

> **WITHDRAWN 2026-09-16 (OPUS), closing
> `FABLE-CONTRA-OPUS-THE-BLINKING-ICON-IS-REACHED-ONLY-THROUGH-AN-EXCEPTION-SCOPE-TABLE`.** Section 5
> has answered this since the same day — *it dispatches on nothing, because it is not a dispatch
> table* — but **the question was left standing here**, which is the failure the contradiction
> explicitly predicted would *"consume somebody's afternoon"*: a section-5 correction that does not
> reach into section 7 leaves the database still asking what a `SCOPE_TABLE`'s `Handler` field
> dispatches on. **A correction that does not retract the question it answers is half a correction.**
> `01D70800` is ~~field 2 of record 0 of the scope table at `01D707F4`~~ **a chained
> `RUNTIME_FUNCTION` for `002B7B80` itself, introduced by the `UNW_FLAG_CHAININFO` header at
> `01D707F8`** — corrected within the hour; see section 5. The scope-table reading, and the grid
> proof OPUS published for it, were both superseded: the `560` that proof divides by is
> `__GSHandlerCheck`'s GS cookie offset, not a record count. **The withdrawal of the question
> stands** — it is not a dispatch table under either reading.

*(Pass 22 adjacency, 2026-09-14: `002B7B80` — the icon proc — calls **actor** `00265020`/
`003588B0`, **input** `00250200` and **scheduler** `001EDEC0`; and `002DD7E0` is called by
**save** `00581930` (5 edges). A HUD element that reads actor state, polls input and yields to
the scheduler inherits the whole UI frame's reach; `002DD7E0`'s save caller is the icon state
persisting into the payload.)*

*(Pass 22 live-graph completion, 2026-09-15: `00265020` — the shared getter the icon proc
reads — is itself called from `Script_VM_Native_Bridge` bodies (`00346710`, `0050F6E0`,
`00344AF0`, and twenty more, 23 edges), `Movement` bodies (`00300310`, `0033CA00`, `00337C10`,
`002EC2C0`, and twelve more, 16), `CombatAction` (`002F8060`, `00307300`, `00320E10`, 3),
`Party` (`00303CC0`, `00304180`, `00359150`, 3), `Spawn_Encounter_Lifecycle` (`00234AF0`,
`002350C0`, `00234DA0`, 3), `Audio` (`00362850`, plus `00581930`'s callee `00225580`, 2),
`Gameplay` (`0031ADB0`, `00339630`, 2), `Rewards_Progression_Economy` (`002FB150`, `00312280`,
2) and `CombatFormula` (`00384F40`, 1). The icon reads image-wide tuned state; the getter's
caller population is the account, not a defect.)*

*(Pass 22 live-graph sweep 2, 2026-09-15: `00250200` calls `CoreRuntimeScheduling` `00229DF0`/
`00229E00` and `002B7B80` calls `001EDEC0` — the icon's yield points (8 edges); `00312280`
reaches `Platform_Online_Achievements` `00316A50` (1); `00234AF0`/`002F8060` reach
`RNG_Random_Selection` `00328370`/`00379CD0` (2); `002F8060` reaches `Story_Event_Quest_Hunt`
`0032AD70` (1). The shared getter's callers carry their own layers with them.)*

## Crossings into other layers — FINAL-AUDIT pass 22 (OPUS, 2026-09-18)

**Status, periodic and terminal — four edges, and this page is the SERVICE at every one.** The four
functions this page cites are each called from that layer:

- `BattleUnit_RunPeriodicCombatMaintenance` calls **two** of them — the nearby-authored-field-action
  trigger and the loot-overlap search.
- `BattleStats_ChangeStatusAndProcessSideEffects` calls the defeat-rewards body.
- `BattleFormula_AdvanceStatusTimersAndBuildResult` (`00386C70`, 935 B) calls the five-byte
  Mersenne-Twister thunk.

**The periodic maintenance pass is what drives all four.** That is the direction worth stating: this
page documents what those bodies do with an atlas and an icon, and the status layer is the thing that
runs them on a timer. **Nothing in that layer is owned here.**

*Two of the three callers are named by symbol rather than by address, and that was measured: both
`00310DB0` and `0030E360` would import an ActorEntity edge this page does not mention. `00386C70` is
safe and is written out.*

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAI — SERVICE.** `00307300` on this page calls `BattleEnmity_ApplyActionParameters`, owned by that layer. What it reaches is the parameter pass: `byte[+5] == 0` on the stats record, then `byte[+0x1D]` of the parameter block and `byte[+4]` of the record decide what is written; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Resource — SERVICE (SWE2-EC7-158, 4 edges).** Batch-123's `0037FBA0` matcher is called by `0037F4D0`, which — with `0029CED0`/`002B7B80` — calls the resource layer's `00249210`/`00249580`; the atlas's callers consult shared helpers, fan-in only.

- **Presentation — CLIENT (SWE2-EC7-164, 90 edges, one fan-in).** The `00184950`/`001EDEC0`/`00249580`-family helpers this page's `003800D0` cites are called across the presentation layer (`001D7DD0`, `002B7B80`, `002BAF80`…) — the atlas's machinery is shared with the rendering callers, not owned here.
- **SaveLoad — CLIENT (3 edges).** The triple `00249210`/`00249410`/`00249580` `003800D0` drives is also called by the save layer's `00582790` — the same fan-in the resource row describes.
- **UI — CLIENT (126 edges, one fan-in).** `001EDEC0` and the shared helpers are called across the UI layer (`00252030`, `00276D30`, `0027C870`…) — the screen code consults the same leaves.

## SWE2-EC7-29 update (2026-09-18) — `003BC160` gated kind-6 scan

`003BC160` (244 B) is the gated entry scan the map screen's field->record
driver shares — three gates before any table work: `[02B457E0]` non-null,
`byte[+0xC8] == 1`, `dword[+0xD0] & 0x100`, then `0037ED80() == 1`.
`00473B70(0)` counts the table, `003BC260(obj)` resolves the kind word
`+0xCC` through `0046B240`/`00315DC0`/`00380170` (fallback `0046B180`),
and the loop `00473BB0(0, i, kind, &rec)` walks entries: on
`rec[+0] == 1 && rec[+0x14] == 0` it writes `02B457D8 = (i != 0)` and
returns `003C0380(rec[+0xC])`; any failed gate or a full walk returns
-1. Interior anchor `003BC1FC` (the `call 00473BB0` in the scan loop).

## SWE2-EC7-30 update (2026-09-18) — `003BC260` kind-word gate + `003C0380` deep scan + `002752E0` packed lerp

`003BC260` (81 B) is the `+0xCC` kind-word resolve the `003BC160`
paragraph names: three tests on `word[rcx+0xCC]` — `0046B240(id)` must
hold, `00315DC0(id)` must return 0, `00380170(id)` must return -1 —
and only then does it tail-`jmp 0046B180(id)`; any failed test skips
the dispatch and returns. Interior anchor `003BC2A6` (the
`jmp 0046B180` fallback).

`003C0380` (201 B) is the deep scan `003BC160` returns into: 50
records of the `02B457E0` bank's `+0xE8` list (element base = the
list pointer + its own `+8` word), keeping entries whose first byte
equals `00264F90()`; each keeper gets `esi = 003BFF20(i, arg)` (arg
when that returns -1) and `ebp = 003C0340(i)` sub-records walked
through `003BF430(i, j, &tmp)` until one reports `tmp == 0` and
`word[+0xC] == esi` — the index is returned, else -1. Interior
anchor `003C040A` (the `003BF430` fetch inside the sub-scan).

`002752E0` (57 B) is the pair-lerp the pulse path feeds: both
operands are `cvtdq2ps`-converted `int32x4` vectors,
`out = trunc(a + (b - a) * ((r9 << 4) * 0.0898))` — the `mulps`/
`addps` blend with a `shufps`-broadcast scalar built from the
`r9` amount — written back as integers with `cvttps2dq`.
Interior anchor `0027530A` (the `mulps` blend).

`0026A950` (97 B) — reached through `002EC2C0` — is a third sibling
of the `0026A8E0`/`0026A870` wrap stores: same
`xmm1 + sgn(xmm1)*pi` bias, same `(byte[rcx+3] & 0xE0) == 0x60`
gate, same `x - trunc(x/2pi)*2pi - bias` recenter, but the
normalized angle lands in the secondary context's record at
`[[rcx+0xB8]]+0x224`. Interior anchor `0026A9A8` (the `+0x224`
store).

## SWE2-EC7-42 update (2026-09-19) - `0050F6E0`

`0050F6E0` (302 B) is a blinking-icon body - `002E9A30`/`0026A1A0`/`00267E10`/`00264010`/`00265020` pair/`003A19A0`/`00267F60`/`00267DB0`. Interior anchor `0050F6FC` (a `002E9A30` call).

## SWE2-EC7-44 update (2026-09-19) - `002B9A20`

`002B9A20` (260 B) is a body - `002B8EE0` single call. Interior anchor `002B9AE0` (the `002B8EE0` call).

## SWE2-EC7-48 update (2026-09-19) - `00303CC0`

`00303CC0` (205 B) is a `Party`-group body - `00265020`/`00265090`/`0030D9A0`/`0031ABF0`/`00327200`/`00336390`/`00808C40`. Interior anchor `00303CD3` (a `00265020` call).

## SWE2-EC7-49 update (2026-09-19) - `00315DC0`

`00315DC0` (197 B) is a body - `0046B180`/`0046B1A0` pair. Interior anchor `00315DD5` (a `0046B180` call).

## SWE2-EC7-59 update (2026-09-19) - `00344AF0`

`00344AF0` (160 B) is a blinking-icon body - `00265020`/`00267DB0`/`0026B4C0`/`003A1D30`. Interior anchor `00344B15` (a `00267DB0` call).


## SWE2-EC7-86 update (2026-09-20) - `003BECA0` two-slot word-table find measured

`003BECA0` (202 B) is the keyed word-table walk the icon callers
run: `003C0380` yields a category byte; slots 0-1 of the
`[02B457E0+0x120]` table (0xA8 stride, `byte[+0x10]` must match)
each hold a pointer whose `word[+8]`-based index list is scanned
for the argument word; a hit returns `rdx + word[rdx+2]` (the
`0xFFFF` sentinel returns the raw pointer); miss returns 0.
Interior anchor `003BED52` (the hit arm reading `word[rdx+2]`).

## SWE2-EC7-88 update (2026-09-20) - `003BF920` + `003BC9F0` measured

`003BF920` (114 B) is the two-stage word fetch the icon callers
run: `003BF430(ecx, edx, &mode)` must resolve, then
`mode == 0` runs `003C18A0` while nonzero runs `003C0F70`; a
zero result, a failed second `003BF430` probe, or a nonzero
second mode all return `0xFFFF` - otherwise `word[rax+0xC]`.
Interior anchor `003BF962` (the second `003BF430` probe).

`003BC9F0` (190 B) is the state-commit handshake the icon
callers run: with `byte[+0xC8] == 1` it stores `rdx`/`cx` into
`+0xC0`/`+0xCC`; the `0037F050()` == 0 path runs
`0037EDB0(word[+0xCC])` (must not return -1), records
`word[+0xCE]`, and requires `0037FD50` to succeed; the nonzero
path runs `0037F440` and may `003BC3E0(rdx, 0x102)` on
failure - returning 1 only on a completed arm.
Interior anchor `003BCA8E` (the `0037FD50` call).

## SWE2-EC7-89 update (2026-09-20) - `0037FD50` + `0037EDB0` + `003C0F70` measured

`0037FD50` (232 B) is the element-slot commit `003BC9F0` finishes
its handshake with: slot `ecx` of the `[02AED490+0xC8]` list
(`word[+0xA]` count, 8-stride elements) supplies the kind byte at
`+0x10` and the `dword>>8 & 0x3FF` sub-id; the kind is counted
across slots 0..ecx-1, `+0xE6`/`+0xE7`/`+0xE8`/`+0xEA` are written
on the shared record, and `0037FBA0` runs the assembled
descriptor - returning 0 on an out-of-range or empty slot, 1 on
commit.
Interior anchor `0037FE0E` (the `0037FBA0` call).

`0037EDB0` (86 B) is the partner lookup `003BC9F0` calls first: a
linear scan of the same `[02AED490+0xC8]` list for the element
whose `dword>>8 & 0x3FF` matches `ecx` - returning the index, or
-1 when the list is absent or the id is not present.
Interior anchor `0037EE02` (the matched arm).

`003C0F70` (246 B) is the nonzero-mode word fetch `003BF920`
dispatches to: `word[+0x16]` shorts through `0032A8A0`,
`byte[+0xCA] == 6` returns 1 outright, `byte[+0x14]` runs
`003BDDE0` whose `003BCBA0` bit-0xB result gates the table path,
and the fallback reads `byte[table + ecx*8 + 4]` out of the
`[02B457E0+0xE8]` index list through `002543F0`, with a final
`word[+0x12]`/`0032A8A0` probe deciding 1 or 0.
Interior anchor `003C0FE0` (the `003BDDE0` call).

## SWE2-EC7-102 update (2026-09-20) - `00473CC0` measured

`00473CC0` (92 B) is the dual `0x8000`-tagged resolve
`003BDB30`, `003BD1B0` and `003BE3A0` call: `r10d`
indexes a `movsxd` sub-table at
`[[02CA6C70] + 8 + r10*4]`, then two
`word[+4]`/`word[+6]` pairs are resolved against the
`0x8000` sentinel - a word `>= 0x8000` stores 0 to the
`r8`/`r9` out-pointers, otherwise the out-pointer gets
`rcx + (word & 0x7FFF)` - and the return byte is
`byte[rcx+1]`. The pair-resolve mode 6 of the counted
enumerator runs.
Interior anchor `00473CE4` (the first `0x8000`
compare).

## SWE2-EC7-106 update (2026-09-20) - `00250CA0` measured

`00250CA0` (418 B) is the `word[+0xE6]`
transition ladder `00250540`,
`002506D0` and `002508E0` run on
`020927F0`: a pending `dword[+0x13C]`
first interpolates `float[+0x130]`
through `00248F40(1, word[+0x13A],
dword[0208F570] - +0x13C)` and clears
on completion; then `dword[+0x11C]` /
`+0x12C` drive the ladder - mode 3
interpolates against `word[+0x120]`
and steps to 4, mode 5 against
`word[+0x122]` with `~([+0xE8] >> 3)
& 1` and steps to 6, mode 7 against
`word[+0x12A]` and steps to 8 - and
each finished leg writes `result *
float[+0x118] + float[+0x114]` into
`float[+0x110]` (mode 7 into
`float[+0x124]` instead) - the
timed fade the blink atlas exposes.
Interior anchor `00250CEE` (the first
`00248F40` call).

`0037FBA0` (430 B) is the record matcher `0037FD50`/`0037F4D0`/`0037FE40` call (sibling of `0037E8D0`): `byte[rcx+0xEE]` counts a `0x18`-stride scan of `+0xF0` records matching `byte[+1] == byte[rdx+1]` and, for kind 2, `byte[+2] == byte[rdx+2]`; `+0xEF` counts a second table, and `0037FA80`/`0037FFD0`/`0037FEA0`/`0037F190` act on hits - the atlas's keyed record find.

Interior anchor `0037FC49` (function `0037FBA0`).

`0037FEA0` (213 B) is the flag set/clear `0037FBA0`/`0037F1F0` call: both records must be non-null with `word[+6] != 0xFFFF`, `ecx + ebx + eax == 0` skips `00473D50`, and `02AED490`'s `+0xE0` gets `| 0x100` or `& ~0x100` - the icon's dirty-flag commit.

Interior anchor `0037FEE2` (function `0037FEA0`).

`0037F190` (96 B) is the event dispatch `0037FBA0`/`0037F1F0` call: null `rcx` returns; `byte[rdx+1]` is the kind (2 also loads `word[rdx+4]`), a `{0x10, kind, payload}` record is built on the stack, and `call [rcx]` fires the callback - the icon's notify primitive.

Interior anchor `0037F1C2` (function `0037F190`).

`0037FA80` (284 B) is the stack-collapse pass `0037FBA0` runs on the `byte[rcx+0xEE]`-counted ring: entries walk down 0x18-stride from the top (`rcx + 2 + (i + 0xA) x 24`), and each whose marker `byte[+1] == 2` with `byte[+2] != dl` dispatches on `byte[rbx]` - 1 frees `qword[+0x10]` through `003697F0` and clears the entry, 2 rewrites it to 3, anything else drops `r13` to 0; every handled entry decrements `byte[rcx+0xEE]` and the sweep continues while `count == index` holds - the pop that validates and releases the pushed pages, returning `r13`.

Interior anchor `0037FB63` (function `0037FA80`).

`0037FA80` (284 B) is the stack-collapse pass `0037FBA0` runs on the `byte[rcx+0xEE]`-counted ring: entries walk down 0x18-stride from the top (`rcx + 2 + (i + 0xA) x 24`), and each whose marker `byte[+1] == 2` with `byte[+2] != dl` dispatches on `byte[rbx]` - 1 frees `qword[+0x10]` through `003697F0` and clears the entry, 2 rewrites it to 3, anything else drops `r13` to 0; every handled entry decrements `byte[rcx+0xEE]` and the sweep continues while `count == index` holds - the pop that validates and releases the pushed pages, returning `r13`.

Interior anchor `0037FB63` (function `0037FA80`).

`0037FFD0` (203 B) is the slot push `0037FBA0` calls when `[+0xEF]` is non-zero: against peer `[02AED490]` it rejects when `[+0xE5]` is clear or the peer's `(+0xEE - 1 + 0xA) x 24` byte is `2`/`3`, else copies the `+0x3F0` 16-byte record into its own `(+0xEE + 0xA) x 24` slot (stamp `2`, `+0xEE` incremented), stores `003800D0`'s product at `+0x10`, decrements `+0xEF` and `rep movsq`-compacts the remaining `+0x3F0` queue - the bounded-stack push/shrink pair

Interior anchor `0038001F` (function `0037FFD0`).

`003BFF20` (194 B) is the nested-table lookup `003C0380` uses for atlas rows: through `[02B457E0]+0xE0` it bounds-checks `ecx` against `+9` then reads the `+0xA`-indexed word offset, chases `+4`-header `+8`-stride subtables twice more, and scans the resulting `r11`-keyed 4-byte-entry list for word `edx` - returning the matched `+2` word or `-1`

Interior anchor `003BFF5D` (function `003BFF20`).

`003800D0` (158 B) is the format-dispatch helper `0037FFD0` calls: record byte `[rdx+1] == 4` requires `[rcx+0xD8]` live and yields `(esi=2, ebx=0x129, ebp=1)`, `== 2` yields `ebx = [rdx+2] + 0x12A`, and anything else keeps `(0, 0, 3)`; the triple then drives `00249580` -> `00249210(rax, 7, ebx, esi, ebp)` -> `00249410`, returning `[rbx+8]`

Interior anchor `0038012B` (function `003800D0`).

`0037F440` (143 B) is the commit-submit `003BC9F0`'s handshake calls: `02AED490` non-null refuses with 0, else it packs `{cl, dl, r8b, r9b, stack-arg}` into a stack request with callback `0037F4D0` and hands it to `00244F50(0x5F0, ...)` with `r10 = 0` - the icon commit's enqueue into the shared request allocator this page names.

Interior anchor `0037F49F` (function `0037F440`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

This page describes unowned code in the residual folder, and it cites the bodies that supply or consume that code. Each layer below arrives with those bodies' other call edges. The page claims only the mechanism it reads, not the layers they touch.

**Audio — MECHANICAL, 23 edges.** `00225580` is called by `00222740`, `00222F20`, `00223190`, `00223DA0` and 6 more; `00362850` calls `002DF410`, `002DF560`, `00362C60`, `00362D20` and 3 more; `00184950` is called by `00361170`, `00361200`; `Actor_GetWorldPosition` (`00265020`) is called by `00362850`; `00362850` is called by `00363560`; `003A1D30` is called by `00361810`; `00581930` calls `00225580`.

**CombatFormula — MECHANICAL, 64 edges.** `RNG_MT19937_NextU32_Thunk` (`00379CD0`) is called by `BattleFormula_BuildCandidateStatusMask` (`003851F0`), `00387130`, `BattleFormula_RollSpecialGuardOutcome` (`00387FD0`), `BattleFormula_ComputeKnockbackChance` (`00388350`) and 49 more; `Battle_ProcessActionTarget` (`00307300`) calls `BattleFormula_MapTargetEntryCodeToOutcome` (`002FEE20`), `BattleStats_ModifyPrimaryResource` (`00300CE0`), `BattleFormula_MapOutcomeToTargetEntryCode` (`0030DAE0`), `BattleFormula_ApplyTargetResult` (`003112F0`) and 2 more; `Actor_GetWorldPosition` (`00265020`) is called by `00384F40`; `00304180` calls `BattleStats_GetByMappedBattleSlot` (`00320AB0`); `BattleUnit_ProcessDefeatRewardsAndLoot` (`00312280`) calls `BattleStats_GetByMappedBattleSlot` (`00320AB0`); `00384F40` calls `BattleStats_FindOwningBattleUnit` (`0031B860`); `00384F40` is called by `BattleFormula_ApplyPreResolutionTargetGates` (`00390AB0`).

**Gameplay — MECHANICAL, 11 edges.** `Actor_GetWorldPosition` (`00265020`) is called by `0031ADB0`, `BattleAction_FindApproachGeometryAroundTarget` (`00339630`); `Battle_ProcessActionTarget` (`00307300`) calls `BattleUnit_SubmitResultReactionMode` (`00328480`), `BattleUnit_DispatchActorPresentationEvent` (`003299B0`); `Spawn_ValidateCandidateDistanceToPlayers` (`00234DA0`) is called by `BattleUnit_HasNonPartyEngagementEvidence` (`00308040`); `002543F0` calls `BattleEncodedId_DispatchQueryMode0Value` (`00309EC0`); `00303CC0` calls `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` (`0030D9A0`); `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` (`0030D9A0`) is called by `BattleRuntime_GetModeDependentDistanceThreshold` (`00309A90`); `00320E10` is called by `0031ADB0`; `RNG_SharedGameplayLCG_NextU32` (`00328370`) is called by `00312B40`; `003C18A0` calls `BattleEncodedId_DispatchQueryMode0Value` (`00309EC0`).

**Movement — MECHANICAL, 108 edges.** `ActorRuntime_GetClass3FloatPair` (`00265090`) is called by `002FB340`, `002FB500`, `00309B10`, `BattleUnit_GetNavigationClearanceRadius` (`0030A130`) and 16 more; `Actor_GetWorldPosition` (`00265020`) is called by `0024B6F0`, `Movement_UpdateSteeringTowardTarget` (`002E45E0`), `002EBFA0`, `002EC2C0` and 12 more; `Battle_ProcessActionTarget` (`00307300`) calls `00265200`, `Actor_SetDesiredMovementHeading` (`0026A0D0`), `0026B0C0`, `Actor_SetFacingHeading_Variant1` (`0026B620`) and 2 more; `0050F6E0` calls `00265200`, `002690D0`, `0026A1A0`, `0026AC70` and 2 more; `0026A8E0` is called by `002690D0`, `002EBFA0`, `002EC140`, `002EC1C0` and 1 more; `00304180` calls `00265200`, `Actor_SetDesiredMovementHeading` (`0026A0D0`), `0026B0C0`, `Actor_SetFacingHeading_Variant1` (`0026B620`) and 1 more; `VMValueStack_PushFloat32Bits` (`00267F60`) is called by `00345430`, `003488B0`, `00349680`, `003548B0`; `0026A870` is called by `002EBFA0`, `002EC140`, `002EC1C0`, `002EC2C0`; `003A1D30` is called by `Movement_ComputeDeltaFromHeadingSpeed` (`002E4380`), `Movement_UpdateSteeringTowardTarget` (`002E45E0`), `Movement_PrepareCandidatePosition` (`002E5380`), `0046AD20`; `0026A950` is called by `002EBFA0`, `002EC140`, `002EC2C0`; `002EC2C0` calls `0026A870`, `0026A8E0`, `0026A950`; `002EC2C0` is called by `002EAAA0`, `002EBFA0`, `002EC510`; `00336390` is called by `00336210`, `00337700`, `PartyFollow_SolveFormation` (`00338490`); `BattleAction_FindApproachGeometryAroundTarget` (`00339630`) calls `thunk_FUN_0026e350` (`0032A790`), `003377C0`, `BattleLocomotion_CheckActorPairClearance` (`0033D660`); `BattleUnit_PublishLocomotionPosition` (`00300310`) calls `0026B0C0`, `00392170`; `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` (`0030D9A0`) is called by `BattleRuntime_GetModeDependentBaseDistance` (`00309AE0`), `00311F70`; `PartyRoster_GetActorBySlot` (`0031ABF0`) is called by `00311E20`, `0033CA00`; `RNG_SharedGameplayLCG_NextU32` (`00328370`) is called by `00239210`, `00312DF0`; `00384F40` calls `00334790`, `00334A70`; `003A19A0` is called by `002EBFA0`, `002EC2C0`; `Spawn_TrySelectCandidatePosition` (`00234AF0`) calls `00265200`; `00264010` is called by `002E5180`; `0026A1A0` is called by `002EBFA0`; `BattleUnit_PublishLocomotionPosition` (`00300310`) is called by `BattleUnit_PublishLocomotionPositionAndFacing` (`003003F0`); `00303CC0` calls `00336390`; `BattleUnit_ProcessDefeatRewardsAndLoot` (`00312280`) calls `00319490`; `00320E10` calls `BattleUnit_GetNavigationClearanceRadius` (`0030A130`); `00336390` calls `thunk_FUN_0026e100` (`0032A6A0`); `00337C10` is called by `0033D890`; `0033CA00` calls `00265200`; `0033CA00` is called by `00311E20`.

**Party — MECHANICAL, 30 edges.** `Actor_GetWorldPosition` (`00265020`) is called by `00303CC0`, `00304180`, `PartyFocus_TryGetCurrentActorWorldPosition` (`00359150`); `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` (`0030D9A0`) is called by `00303CC0`, `00303F00`, `PartyFocus_SelectAndRequestDefaultActor` (`00326500`); `PartyRoster_GetActorBySlot` (`0031ABF0`) is called by `00303CC0`, `00303F00`, `00304180`; `SpawnLifecycle_CheckAndRetireByNativeRange` (`002350C0`) calls `BattleUnit_GetPartyLeader` (`003272A0`), `PartyFocus_IsCurrentPackedActorHandle` (`003273B0`); `00304180` calls `PartyRoster_GetActorBySlot` (`0031ABF0`), `PartyFocus_SetPreferredDefinitionSelectorAndRefresh` (`00327850`); `0031ADB0` calls `BattleUnit_ResolveByFocusHandle` (`0031B7E0`), `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`); `00327200` is called by `00303CC0`, `00304180`; `0033CA00` calls `PartyRoster_GetActorBySlot` (`0031ABF0`), `003272F0`; `Spawn_TrySelectCandidatePosition` (`00234AF0`) calls `BattleUnit_GetPartyLeader` (`003272A0`); `Spawn_ValidateCandidateDistanceToPlayers` (`00234DA0`) calls `PartyFocus_IsCurrentPackedActorHandle` (`003273B0`); `00264010` calls `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`); `00264010` is called by `VMPartyCommand_SetSecondaryFocusActorFromActorIndex` (`00353530`); `ActorRuntime_GetClass3FloatPair` (`00265090`) is called by `00303CC0`; `00303CC0` calls `PartyRoster_GetActorBySlot` (`0031ABF0`); `RNG_SharedGameplayLCG_NextU32` (`00328370`) is called by `BattleUnit_SeedPartyCombatStanceRecheckTimer` (`003081E0`); `00336390` is called by `00303CC0`; `BattleAction_FindApproachGeometryAroundTarget` (`00339630`) calls `BattleUnit_ResolveByFocusHandle` (`0031B7E0`); `00362850` calls `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`); `003A1D30` is called by `PartyControl_ApplyAnalogLocomotionToActor` (`00358CB0`).

**Script_VM_Native_Bridge — MECHANICAL, 199 edges.** `VMResult_WriteFloat32` (`0026B4C0`) is called by `00340B50`, `00340E90`, `00340F80`, `00341250` and 48 more; `00264010` is called by `00341410`, `00343D10`, `00344390`, `003448F0` and 30 more; `VMValueStack_PushFloat32Bits` (`00267F60`) is called by `WorldActorScriptVM_InterpretBytecode` (`0025E4C0`), `00340480`, `00340BE0`, `00342040` and 30 more; `0026A1A0` is called by `0033F270`, `0033F770`, `0033FBA0`, `00340480` and 25 more; `Actor_GetWorldPosition` (`00265020`) is called by `0033FD60`, `00344AF0`, `00345180`, `00345830` and 19 more; `003A19A0` is called by `00345830`, `003461B0`, `0034BE50`, `00357DE0` and 1 more; `003A1D30` is called by `00344AF0`, `00345180`, `00352F70`; `0050F6E0` calls `VMValueStack_PopNumericDiscard` (`00267DB0`), `VMValueStack_PopInt32CoerceFloat32` (`00267E10`), `VMValueStack_PushFloat32Bits` (`00267F60`); `MapRef_GetPersistenceGroupId` (`00264F90`) is called by `00357450`, `0050CDE0`; `002EC2C0` is called by `00357C40`, `00357D10`; `PersistentFlag_SetBank512Low` (`0032AD70`) is called by `00353750`, `00353BD0`; `00344AF0` calls `VMValueStack_PopNumericDiscard` (`00267DB0`), `VMResult_WriteFloat32` (`0026B4C0`); `RNG_MT19937_NextU32_Thunk` (`00379CD0`) is called by `00354BF0`, `00355140`; `002E9A30` is called by `0050F6E0`; `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` (`0032A8A0`) is called by `0034E0B0`; `00346710` calls `VMResult_WriteFloat32` (`0026B4C0`); `0046B180` is called by `00351F90`; `0046B1A0` is called by `0033FAA0`; `0046B240` is called by `0033F6E0`.

**Spawn_Encounter_Lifecycle — MECHANICAL, 13 edges.** `RNG_SharedGameplayLCG_NextU32` (`00328370`) is called by `Spawn_TrySelectCandidatePosition` (`00234AF0`), `Spawn_PrepareRandomCandidateForCurrentEntry` (`002355A0`), `SpawnPoint_GeneratePositionFromAuthoredRegion` (`00236450`), `SpawnKeep_InitializeEntriesFromDefinitionTable` (`002395A0`) and 1 more; `Actor_GetWorldPosition` (`00265020`) is called by `Spawn_TrySelectCandidatePosition` (`00234AF0`), `Spawn_ValidateCandidateDistanceToPlayers` (`00234DA0`), `SpawnLifecycle_CheckAndRetireByNativeRange` (`002350C0`); `Spawn_TrySelectCandidatePosition` (`00234AF0`) calls `Spawn_ValidateCandidateDistanceToPlayers` (`00234DA0`); `Spawn_TrySelectCandidatePosition` (`00234AF0`) is called by `Spawn_SelectAndPrepareAutomaticEntry` (`00235720`); `Spawn_ValidateCandidateDistanceToPlayers` (`00234DA0`) is called by `Spawn_TrySelectCandidatePosition` (`00234AF0`); `SpawnLifecycle_CheckAndRetireByNativeRange` (`002350C0`) calls `SpawnGroup_UpdateExpectedMemberLaneMask` (`00306E60`); `BattleUnit_PublishLocomotionPosition` (`00300310`) is called by `SpawnUnit_FinalizeSpawnEntryActivation` (`0023A410`).

*Tier 2: ledger names and `edges.tsv`; no body read for this note (OPUS, 2026-09-29, pass-22 slice OPUS-P22-SLICE-24-99).*
