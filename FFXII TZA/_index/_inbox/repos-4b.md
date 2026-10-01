> ## ⚠ THIS FILE HAS TWO AUTHORS — read this before citing anything in it
>
> **Added 2026-09-06 by the live `repos-4b [b2c829]`, after re-confirming identity with a fresh
> `ListAgents`.** The session now identifying as **`repos-3f [7dce2e]`** spent two days believing it
> was `repos-4b`, from a single stale `ListAgents` call it never re-ran, and appended here.
>
> **Attribution, as far as either of us can reconstruct it:**
>
> | blocks | author |
> |---|---|
> | the `section_008` / `section_009` round, and every block from **"round 2: the `.nmb` row"** onward that is signed with format work — `.nmb`, `sab`+`mab`, PKFL, `@FRP`, the auditor rounds | **`repos-4b`** (me) |
> | the blocks `repos-3f` identifies as its **ROUNDS 2–4** — its `.nmb` contributions, seven audit passes, and the `st2e` record-level result | **`repos-3f`** |
>
> **Where the two of us disagree about who did a pass, prefer neither by default — check the sheet's
> own `last_pass_state`, which names the method.** My passes state a capstone/parser method and a
> program state; that is the discriminator, not the name.
>
> **The duplication was symmetric and is not wasted.** Each of us found audit stamps reading
> `repos-4b` for work we had not done, and each of us responded the same way — by *doing* the work so
> the stamp became true. `repos-3f` re-ran my `.ard` loader and `section-010` passes; I re-ran its
> `section-011`, `section-002` and `section-003` passes. **Those five sheets now carry two genuinely
> independent passes by two sessions using different parsers**, which is a stronger result than
> either of us recorded, and it is the one good outcome of the mix-up.
>
> **Root cause, and it is mine to learn from too:** trusting one `ListAgents` result for two days. I
> had re-run mine at the start of this round for unrelated reasons and so never noticed. **I did not
> verify my own identity before writing, either — I got away with it.**

# repos-4b — lane 3, `section_008` + `section_009`

## STATUS

**Lane 3 (`section_008`, `section_009`) — both sheets written, not blocked.**
GN160 imported and verified in my own project (`Tools/work/repos-4b_proj`); ledger reproduced
exactly: `internal=38161 owner=9409 finalNo=585 codeDomain=28028 explicit=38022 unresolved=139
pct=99.63575`, snapshot `b57264ba…`, embedded EXE `73461d08…`, residual 139 / `b5008f9d…`.
No `Apply-*` or `Pack-*` was run.

**What was learned — the pair is the cutscene camera system.**

- **`section_008` is `CML1`, `section_009` is `CAM7`** — in 423 of 423 files each. `CAM7` is the
  camera table: one variable-length record per named camera, holding the name and a path payload.
  `CML1` is the name list that indexes into it.
- **`CAM7`'s magic is validated and rejection is total.** `CAM7_Load` (`0x002561C0`) opens with
  `CMP dword ptr [RCX], 0x374D4143` at `0x002561C8` and returns 0 on mismatch, allocating nothing.
  `0x374D4143` occurs **exactly once** in the whole executable, at that instruction.
- **`CML1`'s magic is never checked** — `0x314C4D43` occurs **zero** times in the image, and the
  only function that dereferences the blob never touches `+0x00`.
- **The headline for a modder: three of the four dwords in every `CML1` entry are overwritten at
  load.** `CML1_ResolveNames` (`0x003DA1F0`) reads only `nameOffset`, then calls
  `CAM7_FindCameraByName` (`0x00256530`) and **stores the result over the entry's index field** at
  `0x003DA28F`, zeroing `+0x08` and `+0x0C` after it. Renaming a camera in `section_009` breaks the
  link; renumbering the index column in `section_008` does nothing at all. The file ships as a
  pre-filled runtime structure, not a table of authored parameters.
- **The lookup compares 23 bytes; the loader copies 24.** `strncmp(..., 0x17)` at `0x00256594`
  against `strncpy(..., 0x18)` at `0x00256276`. The longest name in the corpus is exactly 23
  characters, so the shipped game has one character of headroom and does not use it.
- **The engine binds cameras by a linear name scan**, `0x40` bytes per runtime entry, returning the
  index or `-1`. Missing is a supported outcome — two shipped entries resolve to `-1`.

Documents: `25-EBP-Script-Container/Sections/section-008.md`,
`25-EBP-Script-Container/Sections/section-009.md`. Both `PARTIAL`, evidence tier 1, `ebp_units`
declaring only my own two units.

**Gates re-run AFTER writing, not only before.** `check_ebp` 5/14 with no collision;
`check_links` — my two forward references to the not-yet-written `section-010.md` were the only
links I added that failed, and I de-linked them (the 5 remaining broken links are other lanes');
`check_named_not_cited` — **zero findings in either of my files**; `check_source_hygiene` clean over
the whole folder. `check_located_not_read` shows neither of my read functions.

---

## COVERAGE
<!-- MERGED 2026-09-03 by repos-55 into _index/COVERAGE.md (section: 'The EBP round, six sessions in parallel'). Marked, not deleted - sessions are live. -->


`ebp_explained` moves **3 / 14 → 5 / 14**, adding `section_008` and `section_009`.

**Two of the seven "no tool-side lead" units are closed**, and they were the pair the README named
as the place to start. Both carry a §3 loader contract at tier 1 rather than a layout-only sheet.

Corpus figures, all re-derived here from the 1,115-file corpus and agreeing with the frozen census:

| | |
|---|---|
| `section_008` / `section_009` | 423 each, **0 with either alone** in 1,114 containers |
| `section_008` size | 64 B – 1,856 B, median 192 B; 3,933 entries |
| `section_009` size | 192 B – 66,240 B, median 5,696 B; 3,942 camera records |
| cameras per file | 1 – 69, median 7 |
| where they live | **296 of 345 event scripts, 127 of 769 field-map scripts** |

---

## OPEN-QUESTIONS
<!-- MERGED 2026-09-03 by repos-55 into _index/OPEN-QUESTIONS.md as BY-1,BY-3..BY-5. Marked, not deleted: the sessions are live and deleting under a writer risks a lost update. Do not re-merge. -->


New, proposed ids only — the coordinator assigns the real prefix at merge.

- **`PROPOSED-repos-4b-1`** — *What is the `CAM7` record payload from `+0x2C` to the end of the
  record?* The loader takes its address (`0x00256276` region, stored to runtime `+0x18`) and never
  interprets it. Record lengths take 11 distinct values clustered on 108 and 216; the single record
  in the corpus with `subCount == 2` is 44 B larger than the 108 B minimum, so there are at least
  two independent size dimensions. Owner: `Sections/section-009.md` §7.
- **`PROPOSED-repos-4b-3`** — *What does `FUN_0032F3D0(1, name)` gate?* It decides whether a `CML1`
  entry is resolved at all (`0x003DA27B`). It calls `0x00408B10`, `0x00408B30` and `0x005C5230` —
  the same three the teardown consults before freeing — so it looks like an allocator-mode or
  platform predicate rather than anything about the name. **If it can return 0, the "index column is
  always overwritten" claim narrows to "overwritten whenever resolution runs"**, so this is load
  bearing for `section-008.md` §3, not a curiosity. Owner: `Sections/section-008.md` §7.
- **`PROPOSED-repos-4b-4`** — *What are the four camera channels per manager?* `section_009`'s
  handler loops `FUN_002566E0(slot, 0..3)` and `CML1_ResolveNames` resets four `(u16, u16)` pairs at
  manager `+0x118`, `+0x130`, `+0x148`, `+0x160`, spaced `0x18`, each to `(0, 0xFFFF)`. Four of
  something, initialised to "no camera bound". Owner: `Sections/section-009.md` §7.
- **`PROPOSED-repos-4b-5`** — *Why is `section_010`/`section_011` a strict subset of
  `section_008`/`section_009`?* All 113 files with the shake pair also have the camera pair. Stated
  as fact in both sheets; no mechanism offered. Relevant to `repos-c7`.

**Not opened, because they belong to other lanes:** who consumes the resolved camera index (that is
the script verb that plays a named camera — category 01), and whether `section_010` shares the
`CML1` entry layout (`repos-c7`).

---

## AUDIT-LOG
<!-- MERGED 2026-09-03 by repos-55 into _index/AUDIT-LOG.md (section: 'EBP container round - falsification passes'). Marked, not deleted - sessions are live. -->


**A wrong reading was made, caught by falsification, and corrected before it reached a document.**
Worth recording because the failure mode is one `COVERAGE.md` already catalogues.

I ran a whole-program instruction-level reference census on the `CML1` blob pointer
`0x022C6D80` (`DumpDataXrefs.java`, Ghidra `ReferenceIterator`, all reference types). It returned
**4 references**: a store in the load callback, a store in module init, and a load + store in the
teardown — where the loaded value's only use is `free` at `0x0032EFBD`. On that evidence
`section_008` looked **entirely inert**: a whole section a modder could edit with no effect. That
would have been a striking finding and it was wrong.

The census was accurate and insufficient. `0x0032FA43` calls `0x0026CE00` **with the blob still live
in RDX** — `mov edx, ecx` / `and rdx, rax` at `0x0032FA25`/`0x0032FA36`, never clobbered — and that
callee is a one-line setter copying the pointer into the actor-manager record at `+0xD8`. Consumers
reach it from there, so **the search stopped counting exactly where the copy started**. The real
reader, `CML1_ResolveNames` at `0x003DA1F0`, dereferences `blob[+0x04]` at `0x003DA253`.

What caught it was reading the call site rather than trusting the census, prompted by `repos-1e`
calling `0x0026CE00` a binder. **The Inert rows that survive in `section-008.md` §3 are stated
against the reader's 205-byte body — "this field is written before anything reads it" — not against
a search having been exhaustive**, which is a materially stronger claim and does not depend on the
census being complete.

**Second correction, same session.** `ASSIGNMENTS.md` §2's start-up block passes a **relative**
`-ProjectDir '..\..\work\<name>_proj'`. `analyzeHeadless` rejects it: *"Path element starting with
'.' is not permitted"*, thrown from `ProjectLocator`. The import fails after the GZF SHA has already
verified, so the error looks like a script failure rather than a bad argument. **Use an absolute
`-ProjectDir`.** `repos-1e` hit the identical failure independently — worth fixing on the board.

**What was tried and failed to break the readings.**

- *Alternative reading for `section_008`:* the index column is authored input and `CML1_ResolveNames`
  merely validates it. That predicts a compare against the existing value or a branch leaving it
  alone when it matches. There is neither — `0x003DA28F` is an unconditional
  `mov dword ptr [rbx + 4], eax`. The corpus fact that the authored index already agrees with the
  engine's answer in **422 of 423 files** is exactly what an offline tool running the same lookup
  would produce, and it survives as corroboration of *meaning* only.
- *Alternative reading for the pairing:* that `CML1` and `CAM7` merely co-occur. Killed from the
  binary, not the co-occurrence — the dispatcher at `0x003306E0` builds both filenames from one base
  and binds one callback each (`0x00331255`/`0x00331263` and `0x00331314`/`0x00331322`).
- *The magic scan.* `CML1` and `CAM7` searched over the whole image as bytes, as dwords, and
  byte-reversed. `CAM7` hit once — on a `CMP` at the top of a 498-byte function that goes on to
  parse the exact structure the corpus shows. `CML1` hit zero times, and independently the only
  function that dereferences that blob contains no reference to `+0x00`. Two routes, same answer.
- *The three-array walk.* Run over all 423 files: `cameraCount` records chained by a `u32` length,
  then `countB` records with a **`u32`** length prefix, then `countC` records with a **`u16`** prefix.
  Terminated inside the section every time — which is the check that the two different prefix widths
  are real, since a `u32` read of a `u16`-prefixed record would have run off the end.
- *The eleven count mismatches.* `section_008` and `section_009` disagree in 11 of 423 files. Every
  one has **exactly one duplicated camera name** in `CAM7`, and duplicate names occur in **exactly
  those 11 files and nowhere else** — an exact correspondence in both directions. `evt_t0086`, the
  only file where `section_008` is larger, reconciles precisely: 33 records − 1 duplicate = 32
  distinct names, + 2 entries resolving to `-1` = 34.

**Structural note.** `section_010` also carries `CML1` (113/113) — censused here over the first four
bytes of every present section in all 1,114 containers, independently of `repos-1e`, who reported it
first. `CML1` is therefore **a shared list format occupying two directory slots**, not "the
`section_008` format". `section-008.md` says so at the top and scopes itself to the camera instance,
which should prevent an incompatible-claims reopen against `repos-c7`'s sheet.

---

## CALL-CHAINS / ADDRESS-INDEX

Every address below was read in this session unless the row says otherwise. Interior anchors are
given per claim, not one per function.

**Chain — how a named camera resolves (shipped route):**

```
ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources  0x003304A0   [repos-1e, cited]
  ├─ slot 9 ─> CAMDAT_OnLoaded            0x0032FAC0
  │              ├─ slot/pointer split          0x0032FAE1
  │              ├─ blob -> g_camBlob            0x0032FAED
  │              ├─ FUN_002566E0(slot, 0..3)     four sub-slots
  │              ├─ CAM7_Load                   0x002561C0
  │              └─ 0x0026CE20 : manager[+0xE0] = blob
  └─ slot 8 ─> CAMCTL_OnLoaded            0x0032FA10
                 ├─ blob -> g_cmlBlob            0x0032FA3B
                 ├─ 0x0026CE00 : manager[+0xD8] = blob   (call 0x0032FA43, RDX live)
                 ├─ test manager[+0xE0]          0x0032FA4F
                 └─ CML1_ResolveNames           0x003DA1F0   (call 0x0032FA5C)
                      └─ CAM7_FindCameraByName  0x00256530   (call 0x003DA28A)
                           └─ strncmp, n = 23             0x00256594
```

Either handler triggers the resolve, whichever observes the other's blob already bound — so the pair
resolves once regardless of completion order.

| Address | Name proposed | Role | Read |
|---|---|---|---|
| `0x002561C0` | `CAM7_Load` | parses `section_009`: magic `0x002561C8`, count `0x002561D6`, empty-success `0x002561E4`, firstRecord `0x0025624B`, name copy `0x00256276`, chain step `0x0025629F`, array-B `0x00256303`, array-C `0x0025633D` | full body |
| `0x00256530` | `CAM7_FindCameraByName` | slot bound `0x00256539`, blob fetch `0x00256558`, count `0x00256573`, `0x40` stride `0x00256589`, `strncmp` n=23 `0x00256594`, hit `0x002565BC`, miss `0x002565A4` | full body |
| `0x003DA1F0` | `CML1_ResolveNames` | the only reader of `section_008`: count `0x003DA253`, entry base `0x003DA25C`, nameOffset `0x003DA270`, filter `0x003DA27B`, **index write-back `0x003DA28F`**, scratch zeroing `0x003DA292`/`0x003DA296`, 16-byte stride `0x003DA29A` | full body |
| `0x0032FA10` | `CAMCTL_OnLoaded` | slot split `0x0032FA2E`/`0x0032FA36`, store `0x0032FA3B`, binder `0x0032FA43`, partner test `0x0032FA4F`, resolve `0x0032FA5C`, mask bit 8 `0x0032FA6C` | full body |
| `0x0032FAC0` | `CAMDAT_OnLoaded` | slot split `0x0032FAE1`, store `0x0032FAED` | full body |
| `0x002561A0` | `CAM7_InvalidateSlot` | `if (slot < 5) g_camBlob[slot] = 0`, store `0x002561B6` | full body |
| `0x0026CE00` | `ActorManager_BindCmlBlob` | `manager[+0xD8] = blob`, store `0x0026CE11` | full body |
| `0x0026CE20` | `ActorManager_BindCamBlob` | `manager[+0xE0] = blob`, store `0x0026CE31` | entry + store |
| `0x0032ED80` | `ActorResource_ResetManagerLoadState` | teardown; `.cam` free `0x0032EFBD`, `.cml` load `0x0032EFD3` / free / clear `0x0032F00C` | teardown region |
| `0x003306E0` | *(dev-era ATEL dispatcher)* | binds the loose-file requests that **name** the sections; `CAMDAT` `0x00331263`, `CAMCTL` `0x00331322`, `SHKDAT` `0x003313BC`, `SHKCTL` `0x0033147C` | binding region |

**Globals.** `g_camBlob 0x02092808`, `g_camEntries 0x02092810`, `g_camArrayB 0x02092818`,
`g_camArrayC 0x02092820` — five slots, stride `0xBB0` (`imul rcx, rax, 0xbb0`, `0x00256551`).
`g_cmlBlob 0x022C6D80`, `g_camBlobAlias 0x022C6D58` — stride 8. Actor-manager record fields
`+0xD8` (`CML1` blob) and `+0xE0` (`CAM7` blob), record stride `0x288`.

**Cross-subsystem transition, both directions.** `25-EBP-Script-Container` → `Presentation.Camera`
is an **owner transition**: the section bytes stop being file data at `CAM7_Load` and become the
runtime camera table. `Presentation.Camera` → `ActorEntity` is a **trigger, not an owner
transition**: the blobs are parked in the actor-manager record because that is the load-state
bookkeeping, and the actor system never interprets camera bytes.

---

## MANIFEST-ROWS

**None.** Everything I read was already classified in GN160 — nothing moved out of the 139-function
residual, so there is nothing for the gate. `0x003DA1F0`, `0x00256530` and `0x0026CE00` carry no
`CodeDomain` tag at all in the parent; if the coordinator wants them named, the evidence is the
call-chain table above, but I am not proposing rows I was not asked for.

Two GFZ annotations were checked against the binary and **both hold**:
`0x002561C0` tagged `Presentation.Camera.CAM7ResourceLoader` (correct — it is the `CAM7` parser),
and `0x0032FAC0`/`0x0032FA10` tagged `ActorEntity` `ActorResource lifecycle` (correct — they are
load-state callbacks, and ownership does not transfer to Presentation just because the payload is
camera data).

---

## FOR OTHER LANES

Free findings from my corpus and binary work that are not my units. **Verify before citing** — I did
not write these up and they carry no falsification pass.

**Every section's first four bytes, censused over all 1,114 containers:**

```
000 = 0x8000000B (1114)    008 = 'CML1' (423)    014 = 'LGT2' (140)
002 = no magic   (828)     009 = 'CAM7' (423)    016 = 'FF12' (517)
003 = no magic   (359)     010 = 'CML1' (113)    019 = 'FF12' (271)
004 = 'NAVI'     (209)     011 = 'SHK1' (113)
006 = 'TIM2'     ( 67)     012 = no magic (842)
```

`004` = `NAVI` is navigation data; `006` = `TIM2` is the PS2 image format; `016` and `019` share the
`FF12` magic and are **not** the same thing as each other — a sheet claiming either should say which.

**The binary names the sections.** The dispatcher at `0x003306E0` — source file
`..\..\katano\atelload.c`, string at `0xD10958` — builds 13 filenames from one base and requests each
with a debug tag. Extensions at `0xD10990`–`0xD109C8`: `bin dbg sbn msb msf fnt cam camera ra lgt cml
cmi shk skl vld` (`camera` is a directory, not an extension). Confirmed DAT/CTL pairs:
`camera/<n>.cam`→`CAMDAT`, `<n>.cml`→`CAMCTL`, `camera/<n>.shk`→`SHKDAT`, `<n>.skl`→`SHKCTL`. `lgt`
lines up with `014` = `LGT2`. **`dbg` is almost certainly `section_001`, which never occurs in 1,114
files** — debug info stripped from retail would explain one of the seven always-zero slots without
appealing to "reserved".

**This path is dead in the shipped build**: the archive census finds **0 `.cam`, 0 `.cml`, 0 `.shk`,
0 `.skl`, 0 `.lgt` among 89,414 entries** — only 10,045 `.ebp`. It survives as the PS2-era loose-file
route and is evidentially useful precisely because it names things the container does not.

**A trap that nearly cost me a wrong document, and will generalise.** Several section handlers end
in a `FUN_0026CExx(slot, blob)` one-line setter that copies the blob pointer into the actor-manager
record (stride `0x288`). **An xref census on the global the handler stores to will therefore find no
consumers**, because the consumers read the manager field instead. If your section's handler looks
like it stores and never reads, check whether RDX is still live at the next call before writing
"inert".

**`section_010`/`section_011` (`repos-c7`)**: all 113 files that have them also have `008`/`009` —
a strict subset, not a co-equal pair. And `010` is `CML1`, the same magic as my `008`, so the two
sheets need to agree on what `CML1` is. I have scoped `section-008.md` to "the camera instance of a
shared format" to leave that room. I messaged `repos-1e` with the same material.

---
---

# ROUND 2 — 2026-09-04 — the `.nmb` row

## STATUS

**`.nmb` row: worked and reported. Not blocked. It ended in a duplicate-document collision that I
resolved by merging into the other sheet and deleting my own — details below, because that is the
part the coordinator most needs to see.**

Corpus re-extracted from `FFXII_TZA.vbf` myself: 166 area stems, both locale copies of `.nmb` **and**
`.ard`, SHA-256 compared rather than inherited. Extracted files left in
`Tools/work/repos-4b/ard/nmb/` and `Tools/work/repos-4b/ard/ard/` — `repos-1e` is already using them.

**What was learned — `.nmb` is a parallel array over the `.ard`'s second `st2e` table.**

- **The entry count equals the record count of `st2e` table 1 in the paired `.ard`, in 166 of 166
  areas.** One three-byte entry per record. That was the question the board set for this row, and it
  is answered.
- **Falsified against "it matches whichever table you look at".** The four tables often agree, so
  agreement alone proves nothing. In **122 of 166 areas table 3 disagrees with table 1 — and the
  `.nmb` follows table 1 every time.** Table 0 disagrees in 63 (follows table 1 in 63), table 2 in 7
  (7/7), and in the 7 areas where table 1's count is unique among all four the `.nmb` matches it 7/7.
- It also explains the zero-entry files: the four areas with no entries (`asp_a`, `dor_f`, `mrm_a`,
  `slm_a`) are the four whose `.ard` table 1 is empty.
- **No caller requests resource kind 26 with a literal — stated with a positive control.** A `.text`
  byte scan for `mov ecx/edx, 26` followed by a call to any of the three path-API entry points finds
  **zero** hits, while the same scan finds kind 11 (`0x002FC599`) and kind 28 (`0x001B7F93`,
  `0x0035B8AE`). Backward register tracing at all eleven `ResourcePath_Get` sites resolves the two
  resolvable variable-fed ones **away** from 26 — kind 8 at `0x0032FD30` or kind 5 at `0x0032FD3F`
  in `ActorResource_BeginManagerResourceSetLoad`. **This is an absence of a *literal* request and
  nothing more**; five sites take the kind from memory I did not resolve.

## COVERAGE

`formats_explained` — `nmb` is explained, by **one** document, no collision. `.nmb` is in the
48-extension archive census (332 files), so it is a **scored `archive_formats` row**, not a
`container_format`.

Gates re-run **after** writing, not only before: `check_layouts` **0 errors** (I also fixed a
pre-existing unparseable fence, below); `check_links` all 9,773 resolve; `check_named_not_cited`
no findings on the sheet; `check_source_hygiene` clean over the folder.

## THE COLLISION — two documents for one unit, and how it was resolved

**I wrote `St2e-Carriers/nmb-area-name-block.md`. `St2e-Carriers/area-nmb-index.md` already existed
covering the same unit.** Same folder, same format, written the same hour.

It is **not** `repos-d6`'s — their row says explicitly *"Did not touch `.nmb`, the reader body, or
the sheets."* Whoever wrote it used **`PROPOSED-repos-4b-6`** for its open question, i.e. my own id
namespace, so it was written on the assumption that `.nmb` is my unit. **I do not know which session
wrote it, and that is worth the coordinator's attention more than the sheet is.**

**What I did, and why.** I compared the two before touching either.

- **Theirs is the better document and it keeps the unit.** Its §3 is stronger than mine: the full
  22-byte `ResourcePath_Get` body with both arguments sign-extended and **no bound of any kind**,
  the `ResourcePath_Copy` terminator written after the length check (destination needs `maxLen + 1`),
  and a `0x12BA`/`0x12BB` constant scan reported as **too noisy to use**. Its frontmatter is also
  right where mine was wrong — `archive_formats: nmb`, not `container_format`.
- **Two of my findings were genuinely additive**, so I merged them in under an attributed line
  rather than stranding them in this file: the `st2e` table-1 binding with its four-way
  falsification, and the literal-kind-26 absence claim with its positive control.
- **One of my findings I deliberately did NOT port, because theirs supersedes it and mine was
  wrong.** I had claimed the `.ard` and `.nmb` index spaces are misaligned "0 of 321" — computed by
  reading 16-byte records contiguously from `0x01E0D060`. Their §6 records that exact approach as
  unsound: *"the `.ard` pointers are not contiguous"*, and they redid it by scanning for qwords that
  resolve to a path string instead of positing a base. **My number came off the read they had
  already falsified.** Porting it would have re-introduced a corrected error.
- **Then I deleted my own sheet.** One owner per unit; the duplicate was mine to remove and theirs
  was not.

**I also fixed a `check_layouts` error in their §2** — a `u32[]` fence with no literal length, the
identical defect I had just hit in mine. `check_layouts.py` requires a literal array length, and a
`count + 1` table cannot supply one, so the variable-length table is now prose with a note saying
why it is not fenced. That is a mechanical gate fix, not a change to any claim.

> **The process point, for the board.** Row 3 said `.nmb` was mine and row 5 told `repos-d6` to
> *"say so in your row first"*. I updated my status cell before starting and the duplicate still
> happened, so **claiming the row was not sufficient to prevent it.** The cheap fix is to claim the
> *file path*, not the unit, since the path is what collides.

## OPEN-QUESTIONS

Both are carried in the surviving sheet's §7; repeated here so the merge is visible.

- **`PROPOSED-repos-4b-6`** (already used by the surviving sheet) — *what does an entry mean?* Two
  distinct values in 1,146 entries: `12 BA 00` x1,120 and `12 BB 00` x26, the minority in 10 areas.
  My addition narrows it: the entries are **parallel to `.ard` `st2e` table 1's records**, so the
  question is now "what two-state property of those records is this", not "what is this file".
- **`PROPOSED-repos-4b-7`** — *does the shipped game ever load a `.nmb`?* Resolving the five
  memory-fed `ResourcePath_Get` call sites settles it. Until then the honest answer is that no
  literal request exists and a data-driven one is not excluded.

**Withdrawn:** the numbering from my deleted sheet — the surviving sheet's is the one to merge.

## AUDIT-LOG

**A finding was discarded because a peer's document had already falsified the method behind it.**
See the collision section: my `.ard`/`.nmb` "0 of 321" misalignment claim rested on a contiguous
16-byte read of `0x01E0D060`, which `area-nmb-index.md` §6 records as unsound and replaced with a
pointer scan. **The correct action was to drop my number, not to reconcile the two** — and it is
worth logging because the failure would have been invisible: both readings agree that the index
spaces differ, so a merge that kept my sentence would have looked consistent while resting on a
method known to be broken.

**Independently confirmed by `repos-1e` an hour later**, from the other direction: a
`DumpDataXrefs` run on that path table returns `DUMP_DATA_XREFS_NONE`, and a linear `.text`
disassembly agrees — **both false negatives**, because the table is reached as `pathTables[ns][idx]`
and nothing names a record. **Two sessions were misled by the same structure by two different
instruments.** That is a `COVERAGE.md`-class entry, not a one-off.

**What was tried and failed to break the table-1 binding.** The natural attack is that the count
match is a coincidence of small numbers, since most areas have few of everything. That is what the
distinguishing-subset test exists for: 122 areas separate table 3 from table 1, and the `.nmb`
follows table 1 in all 122. A second attack — that `.nmb` pairs to the `.ard` by shared index rather
than by name — is answered in the surviving sheet from the pointer scan, not from my read.

**Method note that cost nothing here but will cost someone later.** The `.nmb` corpus is 9,350 bytes
total and *fully redundant*: the offset table is derivable from the count (`size = 8 + 7*count`,
166/166) and every entry is one of two constants. **A format can be completely parsed and still
carry almost no information**, and the temptation is to read significance into the offset table
because it is the biggest part of the file. It is the emptiest.

**Scratch-directory collision, recorded because it is a real hazard.** Four of my analysis scripts
in `Tools/work/repos-4b/` (`extract_nmb.py`, `nmb1.py`, `nmb2.py`, `nmb3.py`) were **overwritten by
another session mid-round** with different implementations against a different on-disk layout. My
extracted data survived and my results are unaffected — I re-ran everything under `r4b_*`-prefixed
names afterwards. But `Tools/work/<session>/` is documented as private scratch and was not.

## CALL-CHAINS / ADDRESS-INDEX

Addresses I read this round. Interior anchors per claim.

| Address | Name | Role | Read |
|---|---|---|---|
| `0x002DF980` | `ResourcePath_Get(kind, index)` | `master[kind][index]`; table base `0x002DF983`, kind pick `0x002DF98D`, index pick `0x002DF991` | full body |
| `0x002DF880` | `ResourcePath_Copy` | same lookup at `0x002DF893` | full body |
| `0x002DF780` | `ResourceHandleSlot` | indexes `0x02EC3EE0 + (kind*5000 + index)*4` at `0x002DF7BF`, tested against `-1` | full body |
| `0x002DF9A0` | `ResourcePath_Init` | fills ~40 kind slots; `.nmb` stores at `0x002DFAE4` (`in`) and `0x002DFE58` (`ch`), **both to `0x0215F0D0`** | the store sites and the `fopen` tail |
| `0x0022A0B0` | engine start-up | calls the initialiser once with the locale id from `0x01E02814` | that call only |
| `0x0032FCA0` | `ActorResource_BeginManagerResourceSetLoad` | **a negative result** — kind **8** at `0x0032FD30` / kind **5** at `0x0032FD3F`, not 26 | the kind selection only |

**Globals.** `g_pathTables 0x0215F000`, `.nmb` slot `0x0215F0D0` = **kind 26**, derived from the
initialiser's own stores rather than by arithmetic on one address, and confirmed independently by
enumerating all ~40 slots by the extension of the strings they reach. Path arrays `0x01E4DC30`
(`in`) and `0x01EAE0D0` (`ch`), **321 `char*` each, naming the same area at the same index in 321 of
321**. Handle table `0x02EC3EE0`, stride **5,000 per kind**.

**Cross-subsystem transition.** `Resource.PathTable` -> the area's authored tables is a **trigger,
not an owner transition**: the path table only resolves `(kind, index)` to a string and never opens
or parses anything.

## MANIFEST-ROWS

**None.** Everything I read was already classified in GN160; nothing moved out of the 139-function
residual. `0x002DF980`, `0x002DF880` and `0x002DF780` carry no `CodeDomain` tag in the parent and
the call-chain table above is the evidence if the coordinator wants them named — but I am not
proposing rows I was not asked for.

## FOR OTHER LANES

- **`.ard` owner:** the `.nmb` count pins **`st2e` table 1** specifically, and `repos-d6` has
  separately established that `recordSize` is constant per directory slot across all 166 areas
  (84/88/56/56). Those two facts together mean **table 1 has both a fixed schema and a per-area row
  count that a second file annotates one-for-one.** If any of the four tables is the per-area enemy
  list the community reading claims, table 1 is the one with corroborating structure — and that is a
  lead to test, not a finding.
- **`archive_formats: "ard"` is still unclaimed** and `repos-1e` asked me to declare it. **I cannot:
  I own no `.ard` sheet** — my only document in that folder was the duplicate I deleted. The only
  `.ard` documents that exist are `repos-1e`'s loader sheet and the coordinator's `README.md`, so one
  of those should take it. Flagged rather than silently left at `[ ]`.
- **Everyone:** `.nmb` is in the archive census (332 files), so it takes `archive_formats`, not
  `container_format`. I got that wrong first time. If your format ships as an archive entry it is
  scored, and the wrong key means your sheet does not count.
- **`check_layouts.py` cannot express a variable-length array.** `u32[]` and `u32[N]` are both
  unparseable field lines. A `count + 1` table has to be prose with a note saying why — two sheets in
  this folder hit it independently within the hour.

---
---

# repos-4b — round 2, 2026-09-04: the `.nmb` row

## STATUS

**`.nmb` row taken and worked; not blocked.** Board row 3 status updated before starting. Sheet:
`02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/area-nmb-index.md`.
No `Apply-*` or `Pack-*` run. Same GN160 project as round 1, still verified.

**The brief was "establish what `.nmb` indexes and whether it keys to the `.ard` tables." Both are
answered and they have different answers.**

- **What it indexes: the `.ard`'s second `st2e` table.** The `.nmb` entry count equals that table's
  record count in **166 of 166 areas**, zero counterexamples — one three-byte entry per record.
- **Whether it keys to the `.ard` tables *by index*: no.** `.nmb` is reached as **resource kind 26**
  of a global path table with **321** entries per region; the `.ard` path records number **215** per
  tree. Same authored ordering, different lengths, so **the same area has a different index in
  each.** Shared order is not a shared index.
- **The `ch`/`in` puzzle is solved.** The board recorded as unexplained that a per-area file ships
  under two trees, *"neither of them `us` nor `jp` — not what a localisation split looks like."* It
  isn't one. They are the two **region** variants of resource kind 26: `ResourcePath_Init` installs
  the `in` array unconditionally at `0x002DFAE4`, and one switch arm overwrites the slot with `ch`
  at `0x002DFE58`. Nothing is localised — both copies are byte-identical in 166 of 166.
- **A whole addressing mechanism came out of it.** `ResourcePath_Get` (`0x002DF980`) is 22 bytes:
  `return g_pathTables[kind][index]`, **with no bound on either argument** — no `cmp`, no mask, no
  branch in the entire function.

## COVERAGE

`formats_explained` **0 / 48 → 1 / 48**; `nmb` declared once on `area-nmb-index.md`, no collision.

Corpus re-derived here rather than inherited: **332 files, 166 areas, both locale copies
byte-identical in 166 of 166 for `.nmb` *and* `.ard`** (SHA-256 per copy). Sizes 8–162 B, 19
distinct values, fully determined by `size = 8 + 7·count`. 1,146 entries, and **two distinct entry
values in the entire corpus** — `12 BA 00` ×1,120, `12 BB 00` ×26, the latter in 10 areas in
contiguous runs.

**Gates re-run AFTER writing:** `check_layouts` — 25 fences, no ERROR, no UNACCOUNTED outside the
two templates; `check_links` — **all 9,773 links resolve**; `check_assets` — `nmb` claimed once;
`check_named_not_cited` and `check_self_contradiction` — clean on my files.

**Also brought the two EBP sheets up to the new `struct` fence rule** (`section-008.md`,
`section-009.md`): four fences, all validate. The `CAM7` record's undecoded `+0x2C` payload is
deliberately left **out** of its fence rather than given a plausible field name.

## OPEN-QUESTIONS

- **`PROPOSED-repos-4b-6`** — *What does a `.nmb` entry mean?* Structure complete, values censused,
  parallel array established — but nothing read consumes an entry. **A two-symbol alphabet over
  1,146 entries is a strong constraint on the answer and is not the answer.**
- **`PROPOSED-repos-4b-7`** — *Who opens the `.nmb` file?* This round establishes how the *path* is
  reached, not who reads the bytes.
- **`PROPOSED-repos-4b-8`** — *What does a `kind` number mean?* Dense in `0..40` with gaps; no name
  table for them found.
- **`PROPOSED-repos-4b-9`** — *Is kind 21 the `.ard` namespace?* `repos-1e` reads `.ard` as
  namespace 21 index `areaIndex*2` from the consumer at `0x003EA868`/`0x003EA97F`; I recover slot
  `0x0215F0A8` from the initialiser and **both its arrays begin with three NULLs**. Neither reading
  retracted, conflict unresolved. It matters because it decides whether `.ard` and `.nmb` share one
  namespace mechanism or two.

## AUDIT-LOG

### A published table was wrong, and the way it was caught is the point

**I shipped a §5 table giving an entry count for each of 29 resource kinds. The counts were not
measurements and are now withdrawn.** Recorded in the sheet's §8 as a permanent correction.

The arrays have **no terminator** — length lives only in the callers. My figure came from walking
each array until a qword that did not resolve to a printable string, which **stops at the first
NULL**, and NULL entries are legal mid-array. Every count was the distance to the first hole.

**What exposed it was a peer's unrelated finding.** `repos-1e` reported that namespace 21
interleaves `.ard` with `.fpk` and that `.fpk` is usually NULL. Re-running with NULLs tolerated gave
*different and equally wrong* numbers — the tolerant walk runs past the array end into its
neighbour, so kind 26 grew from 321 to 359 by absorbing entries it does not own, and kind 16
reported 321 `.nmb` paths belonging to kind 26. **Two passes, two answers, both wrong; the
disagreement between them is what proved neither could be trusted.**

**Why it was reachable.** The strict walk gives a plausible number for a flat array with no holes,
and kind 26 — the one array I checked against an independent bound — is exactly that. **I validated
the method on the single case where it happened to work and applied it to 28 where it did not.**
The tell was in my own output and I labelled it away: three rows hit the walk cap and I called them
"lower bounds" instead of treating them as evidence the walk had no idea where arrays ended.

**What replaced it.** §5 now gives slot, variant count and the array's first three entries, and
states a length only for kind 26 — where a scan bounded by *string identity* rather than by walking
gives contiguous stride-8 runs of 321 (`in`) and 313 + 7 (`ch`). The head-only reading also
recovered something the counts had hidden: **kind 5 is a 3-wide `{ebp, mot, fpk}` interleave per
map, not a 3-entry list**, and the `.cm`/`.ca` kinds interleave a header with its takes.

**And a claim built on the same broken walk is withdrawn:** *"`.ard` is not in this table."* The
surviving narrower claim is that no slot's **head** holds `.ard` paths and `.ard` forms no stride-8
pointer run — the latter being positive evidence for the 16-byte interleave, since the same scan
that finds 321 `.nmb` pointers in a row finds no `.ard` run longer than three.

### The duplicate-unit collision, resolved without loss

`repos-d6` and I wrote `.nmb` sheets **in parallel, in different profiles, unable to message each
other**. Two files briefly existed; they have since been merged into mine and theirs deleted — not
by me. Both independent readings agreed on every structural fact, including — separately in each —
the warning that **the 3-byte entry is a corpus fact, not a format rule**, because the offset table
can express any length.

**Their central claim I re-derived rather than accepted.** Parsing all four `st2e` tables in all 166
`.ard` files and comparing each table's `+0x04` against the `.nmb` count:

```
table 0: 103/166    table 1: 166/166    table 2: 159/166    table 3: 44/166
```

Zero counterexamples, and **table 3 disagrees with table 1 in 122 of 166 areas while the `.nmb`
never follows table 3** — so it is not an artefact of the four counts usually agreeing.

**It superseded my own weaker reading, which I had already written down as weak.** I had a `0.868`
correlation between `.nmb` count and `.ard` size and "`.ard` `+0x34` matches in 103 of 166", offered
as suggestive and explicitly not as a binding. The 103 is now explained: `+0x34` is where `st2e`
table 0's count falls, and table 0 matches in exactly 103.

### Other things tried that failed to break the readings

- *"`.nmb` is a name list"* — the extension says so and the standing lead said so. It predicts
  printable payload. **Measured: 13.6 % of bytes printable, and those are the offset table's low
  bytes, not the entries.** Lead dead.
- *A first `.ard` index comparison* assumed a contiguous 215-record array at `0x01E0D060` and read
  mostly nulls, because those pointers are not contiguous. Redone by scanning for qwords that
  resolve to a path string, never by positing a base. **Assuming a base is the same error class as
  assuming a stride.**
- *Constant-scanning `0x12BA`/`0x12BB` in `.text`* — 48/40 and 8/2 hits, too noisy to use; nothing
  rests on it.

### A gate report I did not act on, and why

`repos-1e` flagged `check_layouts.py` reporting an unparseable `u32[]` fence line at
`area-nmb-index.md:67`. **I re-ran the gate and it is clean — no ERROR anywhere in the database.**
The line they saw was a transient mid-merge state of a file three sessions were touching at once.
Per the standing rule, a single red gate result is not evidence until re-run, and **I did not
"correct" a document that is already right.** The current text uses an indented block with an
explicit note that the `count + 1` length cannot be expressed in the fence grammar.

## CALL-CHAINS / ADDRESS-INDEX

```
ResourcePath_Init  0x002DF9A0   installs every slot of g_pathTables (0x0215F000)
   ├─ kind 26 `in` array 0x01E4DC30  <- 0x002DFAE4   (prologue, unconditional)
   └─ kind 26 `ch` array 0x01EAE0D0  <- 0x002DFE58   (one region switch arm)

ResourcePath_Get   0x002DF980   return g_pathTables[kind][index]        11 call sites
ResourcePath_Copy  0x002DF880   same lookup + bounded copy into a caller buffer
FUN_002DF780       0x002DF780   third consumer, indexes at 0x002DF7BF / 0x002DF830
```

| Address | Name proposed | Anchors | Read |
|---|---|---|---|
| `0x002DF980` | `ResourcePath_Get` | table base `0x002DF983`, kind fetch `0x002DF98D`, index fetch `0x002DF991` | full body (22 B) |
| `0x002DF880` | `ResourcePath_Copy` | NULL return `0x002DF89E`, copy loop `0x002DF8B3`, length test `0x002DF8C4`, terminator `0x002DF8D1`, success `0x002DF8D6` | full body |
| `0x002DF9A0` | `ResourcePath_Init` | kind-26 installs `0x002DFAE4` / `0x002DFE58` | slot-install region |
| `0x0215F000` | `g_pathTables` | reached as `[R15 + RBX*8 + 0x203f000]` at `0x002DF7BF`, `R15` = image base | — |

**`ResourcePath_Copy` has an off-by-one worth a caller audit:** the terminator is written at
`dst[copied]` *after* the length test, so the destination needs `maxLen + 1` bytes, not `maxLen`.
Callers not audited, so this is a property of the function and not a reachability claim.

**Cross-subsystem transition.** `Resource.PathTable` → every asset subsystem is a **trigger, not an
owner transition**: the table hands out a `char*` and owns nothing else. Ownership of the bytes
begins at whichever loader opens the path.

## MANIFEST-ROWS

**None.** Everything read is already classified in GN160; nothing left the 139-function residual.
`0x002DF980`, `0x002DF880` and `0x002DF9A0` carry no `CodeDomain` tag, but I am not proposing rows I
was not asked for — the evidence is the table above if the coordinator wants them named.

## FOR THE COORDINATOR

1. **The `.fpk` control in `St2e-Carriers/README.md` is weaker than stated, and its conclusion still
   holds.** The README argues `.fpk` (7,520 strings, 0 files) is anomalous, using `.nmb` as the
   control: *"642 strings, 332 files, so the instrument works."* But **only 166 of the 321 kind-26
   entries ship a file — 52 %**, the rest being development areas (`tst_*`, `ttl_*`, `e00_*`). A
   path in a table is not evidence the file ships. `.fpk` at **0 of 7,520** is still categorically
   different, so **the finding survives — it rests on the zero, not on the contrast.** Not edited;
   the README is not mine.

2. **A metric miscategorisation to watch for.** `repos-d6`'s now-merged sheet declared
   `container_format: nmb`. Per `_templates/FORMAT.md` that field is for formats which are **not**
   archive entries; `.nmb` is one of the 48 censused extensions (332 files), so
   `archive_formats: - "nmb"` is correct and is what the surviving sheet carries. The slip is
   invisible to `check_assets.py`, which only sees the scored field — so it would have cost a unit
   silently.

## FOR OTHER LANES

- **`repos-c7` (`.bin` census):** the path table names `.bin` in several distinct kinds — **2**
  (`WepJob_Matrix.bin`, `key_signal.bin`, `battle_message.bin`, 10 region variants), **6**
  (`ousi00.bin`, then `dummy.bin` padding), **9** (`test_map_ref.bin`, `test_area_ref.bin`) and
  **35** (`ff12menuoverlay_*_debug.bin`). Independent support for `.bin` being several formats under
  one extension, and it hands you disjoint populations to split by before sampling. **Do not take
  entry counts from my §5 table** — see the correction above; only the first entries are sound.
- **`repos-1e` (`.ard` reader):** our kind-21 readings disagree — `PROPOSED-repos-4b-9` above. Also,
  `ResourcePath_Get` has **no bounds check on either argument**, so if your walker indexes any of
  these arrays the bound must come from the caller. And your interleave finding is confirmed from
  the corpus side: a stride-8 pointer scan finds runs of 321 for `.nmb` and **no run longer than
  three** for `.ard` or `.fpk` — exactly what a 16-byte interleave produces.
- **Anyone using a path-string count as evidence a file ships:** don't. 155 of 321 kind-26 entries,
  and 49 of 215 `.ard` entries, name files that are not in the archive.
- **Anyone walking a pointer array in this binary to find its length:** these arrays have no
  terminator. Stopping at the first non-string under-counts (NULLs are legal mid-array); tolerating
  NULLs over-counts (you walk into the next array). Bound it by something external — string
  identity, a caller's loop bound — or do not state a length.

## CORRECTION — 2026-09-04, same round: "table 1" was an ordinal, not a slot

**Raised by `repos-1e`, verified here independently, and the sheet is fixed.** My report above and
my first board entry said the `.nmb` count matches *"`st2e` table 1"*. That is **correct as a
file-order ordinal and wrong as a directory slot**, and the sheet said it in a way a reader would
have resolved the wrong way.

The `.ard` header carries an **eight-slot indexed directory** at `+0x10`–`+0x2C` (`repos-d6`), and
only four slots hold an `st2e` table. So the table I matched is **directory slot 2**, which is the
*second* `st2e` block in file order. Two coordinates, one table.

**I did not take the correction on trust.** I mapped every `st2e` occurrence onto the directory slot
whose offset equals it, across all 166 areas:

| ordinal | slot | `recordSize` | consistent | `.nmb` count matches |
|---:|---:|---:|---:|---:|
| 0 | 0 | 84 | 166/166 | 103 |
| **1** | **2** | **88** | **166/166** | **166** |
| 2 | 5 | 56 | 166/166 | 159 |
| 3 | 6 | 56 | 166/166 | 44 |

`repos-1e`'s mapping is confirmed. Three things came out of the check that were not in either of our
accounts:

- **The ordinal→slot map never permutes** — 166/166 for all four. That is *why* the two coordinate
  systems could be swapped for each other without anyone noticing, and it is a measured property,
  not a definition. Had one area permuted, my original claim would have been wrong in that area and
  nothing would have flagged it.
- **Present slots are `{0, 1, 2, 5, 6, 7}` in every area**; 3 and 4 never occur. Slot 1 and slot 7
  carry no `st2e`.
- **Slot 0's offset is always `0x30`** — simultaneously the first section offset and the header
  length — and per-slot `recordSize` is constant corpus-wide at **84 / 88 / 56 / 56**,
  independently reproducing `repos-d6`'s figures from a different starting point.

**The falsification table is restated in slot terms** (it was computed on ordinals, so the numbers
are unchanged — only the labels move): slot 0 differs in 63 areas → `.nmb` follows slot 2 in 63;
slot 5 differs in 7 → 7; **slot 6 differs in 122 → 122**; slot 2's count unique in 7 → 7.

**Why this was worth a correction rather than a silent edit.** The claim's *content* never changed —
the same bytes, the same 166/166, the same 122-area falsification. What changed is that it was
stated in a coordinate system the reader could not tell apart from the one the rest of the folder
uses. **A claim that is true under the author's numbering and false under the document's is a defect
even when nothing about the measurement is wrong**, and it is the kind that survives review because
every individual number checks out.

**It also made the finding stronger.** Slot 2 is what `repos-1e`'s loader sheet reaches as battle
category 2, bound into registry slot `0x02EBF120` — the widest reader set of the five. So a
row-for-row annotation from the corpus side and a consumer set from the instruction side now point
at the same table from two directions. Both remain leads: I have no reader for a `.nmb` entry, and
that sheet names slot 2's consumers without decoding its records. **Corroborating leads, not a
finding** — recorded that way in the sheet.

Gates re-run after the edit: `check_layouts` 0 errors, `check_links` all 9,774 resolve,
`check_named_not_cited` no findings on the sheet, `check_assets` shows `[x] ard` and `[x] nmb` with
one owner each and no collision.

## FALSIFICATION — 2026-09-04, prompted by `repos-1e`: the kind-26 array has no sparse head

`repos-1e` reported that the **namespace-21 (`.ard`/`.fpk`) arrays carry 24 NULL qwords at the
head**, so head-only inspection of them finds nothing, and warned that array-structure claims for
other kinds need the same care. **That was a live hazard for this sheet and I tested it rather than
reasoning about it.**

If kind 26's array had a NULL head, the base stored in `g_pathTables[26]` would sit *before* the
first `.nmb` pointer, and **every area index in the sheet would be shifted by that offset** — a
whole-section error with no gate that would catch it.

**Result: it does not.** Recovering the base from the initialiser's own `lea`/`mov` pair rather than
from where I happened to find pointers — `0x002DFAE4` → `0x01E4DC30` (`in`) and `0x002DFE58` →
`0x01EAE0D0` (`ch`) — both arrays are **dense from index 0**: zero NULL qwords at the head, index 0
already a `.nmb` (`tst_a`), **321 consecutive `.nmb` pointers with no other extension inside**, and
the first NULL at index 321. The sheet's index space is unshifted.

**Incidental, and recorded so nobody reports it as a third table:** 15 further qwords in `.data`
resolve to `.nmb` path strings, but each is **isolated** — its immediate neighbours resolve to
nothing — and they sit among structured non-pointer data. They are not an array. **What they are is
not established.**

> **The general point, which is `COVERAGE.md`-shaped.** The hazard did not apply here, and that is
> exactly why it was worth testing: a negative result on a structural assumption is cheap, and the
> alternative was a sheet whose every index was off by 24 with all its internal arithmetic still
> self-consistent. **I had recovered the right base by accident of method** — I read it out of the
> initialiser instead of assuming the first pointer I found was the base — and I could not have said
> so before checking.

Gates after the edit: `check_layouts` 0 errors, `check_links` all resolve, `check_named_not_cited`
clean on the sheet.

## PROPOSED `COVERAGE.md` ENTRIES — 2026-09-04, two of them, both cross-confirmed with `repos-1e`

**I cannot edit `COVERAGE.md`; it is the coordinator's.** These are written in the form they would
take, with both sightings named, because each was independently hit by two sessions using different
instruments — which is the bar `COVERAGE.md` exists for.

### 1. A path-table base must come from the initialiser, never from its first pointer

**Recover a path-table base from the code that writes it. Where the first pointer happens to sit is
not the base, and the data cannot tell you the difference.**

- **`repos-1e`, namespace 21 (`.ard`/`.fpk`):** the arrays are **sparse — 24 NULL qwords at the
  head**. Taking the first `.ard` pointer as the base shifts every index by **12 areas**.
- **`repos-4b`, kind 26 (`.nmb`):** the arrays are **dense from index 0**, first NULL at 321. Taking
  the first pointer as the base is correct — *by luck*.

**The two cases are indistinguishable once you are reading from the first non-NULL entry**, and in
both the downstream arithmetic stays self-consistent, so **no gate flags either.** The dense case is
what makes the sparse case checkable: only the initialiser's own `lea`/`mov` separates them.

> **Both of us reached a correct base and only one of us could have said why.** I used the
> initialiser because it was the cheapest way to confirm *which slot was 26*, not because I had
> considered the hazard; `repos-1e` used it too and, until the kind-26 test, had no stated reason it
> mattered. **A correct answer reached for the wrong reason is a latent defect everywhere the reason
> stops holding.** That is the entry, not the offsets.

### 2. A span is not a structure — REWRITTEN 2026-09-04, and one half retracted

> **What this entry said first, and why it changed.** It was drafted as *"pointers into a table's
> address range are not members of the table"*, resting on two sightings: `repos-1e`'s **256 qwords
> pointing into `0x01E0D000`–`0x01EDD800` that are "not part of the path table"**, and my 15. **They
> re-measured and retracted their half**: 19 of the 256 *do* land on real table slots, and the span
> itself was never the table — it was derived from the first and last `.ard` pointer site, so it
> contains several other path arrays with `.fpk` paths dominating (7,241 slots in the span against
> 430 `.ard` entries). Their conclusion — drop the inbound set as evidence — was right; **their
> stated reason for it was false in 19 cases.** Kept visible rather than silently rewritten.

**The corrected rule, which is stronger than the one it replaces:**

> **A range bounded by a structure's first and last member is not that structure.** Inbound
> references to such a range say nothing about which structure they reach — some will hit real
> members, most will hit whatever else lives in the span.

**`repos-1e` is drafting their own half in their inbox with their own measurements.** I am not
carrying their numbers; the two halves should be merged from two sources.

**My half, RE-MEASURED 2026-09-04 rather than confirmed from memory**, and against a stricter test
than the original claim used. The original excluded membership only in the two kind-26 arrays —
which is precisely the shape of the error they made. The re-run recovers **all 94 array bases over
41 kinds** from the initialiser's stores, materialises **20,107 member slots**, and tests every
`.nmb`-resolving qword in `.data`/`.rdata`/`_RDATA` against that full membership set:

| | |
|---|---|
| qwords resolving to a `.nmb` path, 8-aligned, whole image | **657** |
| **inside** a recovered path array | **642** — all of them kind 26, i.e. the two 321-entry arrays |
| **outside every one of the 41 kinds' arrays** | **15** |
| of those 15, both neighbours resolve to nothing | **15 / 15** |

**Three of the fifteen point into the *interior* of a path string**, not at its start — they resolve
to the bare tail `".nmb"`. A path table holds pointers to string starts, so those three cannot be
table members under any reading, and they are strong evidence the set is coincidental qword
alignment rather than structure. **What the 15 actually are is still not established**, and the
entry claims only that they are not members of any array the initialiser writes.

**Why my half survives and theirs did not:** I tested membership against every structure, they
tested it against a span. That is the entry.

### 3. Pairs with the existing "agreement is not verification" family

`repos-1e`'s `registry_slots` error and my `.ard` index-alignment error are **the same failure at
opposite angles**, and probably belong in one entry:

- **Theirs:** read *discussion* of a registry slot in three documents as *ownership*, so declared
  none. The count 5 agreed with the count 5 and the check stopped. That is rule 3c's own warning
  running backwards — the rule counts declarations precisely because `0x02EBF138` is mentioned in
  ten documents and explained in one.
- **Mine:** computed a confident number from a method a peer's document had already falsified. Both
  readings agreed the index spaces differ, so keeping my sentence would have *looked* consistent
  while resting on a broken method.

**In both, the wrong thing was trusted because it agreed with something.** Agreement is not
verification, and the failure is invisible precisely when the conclusion happens to be right.

**A third instance, and it happened while this entry was being written.** `repos-1e` sent me a
measurement for entry 2, I drafted the entry around it, and **they were one message from having a
number cross-confirmed that they had never measured — precisely because it agreed with my
independent sighting of the same shape.** They caught it by re-running rather than recalling. So:

> **"Cross-confirmed by two sessions" is worth nothing if the second session confirms from memory
> rather than from a re-run.** Two sessions agreeing is the *weakest* configuration for this failure,
> not the strongest, because each treats the other's agreement as the check.

That prompted me to re-measure my own half of entry 2 instead of restating it — which is how the 15
came to be tested against all 41 kinds' arrays rather than only kind 26. **The stricter test was
provoked by their retraction, not by my own doubt**, which is worth recording as honestly as the
result.

---
---

# repos-4b — round 3, 2026-09-04: `.sab` + `.mab`, and `PROPOSED-repos-4b-9` closed

## STATUS

**Lane done, unclaimed row taken and finished.** `.nmb` closed last round; every board row was
reported, so I took the largest unclaimed tractable format. Sheet:
`18-Audio/Sound-Bank-And-Voice-Formats/sab-sound-bank-container.md`, tier 1, all gates clean. No
`Apply-*` or `Pack-*`. Same GN160 project, still verified.

**What was learned — the sound bank container, both halves.**

- **`.sab` and `.mab` are one container with two fixed schemas.** Identical header field-for-field,
  identical 16-byte chunk record with the same constant `flags`, identical directory formula — but
  `.sab` is **always** `snd `/`seq `/`trk `/`mtrl` (4,609 of 4,609, one distinct sequence) and
  `.mab` is **always** `musc`/`inst`/`mtrl` (116 of 116). A fixed schema, not a variable container.
- **The directory is not at a fixed offset, and the corpus cannot tell you that.**
  `Sab_FindChunk` (`0x007CF6B0`) computes `dir = blob + ((0x10 + nameLength) & 0xF0) + dirDelta`.
  Every shipped file lands on `0x20` only because `nameLength` is 5 or 7 and `dirDelta` is `0x10`.
  **A file-corpus reading would have written "the directory is at +0x20" and been wrong about the
  format.** The `& 0xF0` rounds *down*, so a 16-character bank name would collide with the
  directory.
- **A live legacy branch.** `blob[0x04]` is a version byte, `2` in all 4,725 files; the `< 2` arm at
  `0x007CF6D9` skips the name alignment entirely. Real code, dead against this corpus.
- **A missing chunk is a supported outcome**, not an error: the scan falls out of the loop and
  writes a null result descriptor at `0x007CF710`.
- **132 sound banks this build cannot reach.** `.sab` splits 4,477 `.win.sab` / **132 `.orb.sab`**
  (Orbis = PS4) — 66 `us` + 66 `jp`, **every one with a `.win.` sibling**, and **`.orb` occurs zero
  times in the executable** in any section. Editing one changes nothing.

## COVERAGE

`formats_explained` **2 / 48 → 4 / 48**, adding `sab` and `mab` on one sheet, no collision.

Corpus: **every header of all 4,609 `.sab` and all 116 `.mab`**, read straight out of the VBF
without extracting 2.1 GB of payload. Invariants, all whole-corpus: magic 4609/4609 and 116/116;
version byte `2`; `dirDelta` `0x10`; `chunkCount` 4 / 3; `+0x0C` equals the file's own length
4,725 / 4,725; name ASCII and NUL-terminated at `+0x10+nameLength`; chunk `flags` `0x00100000` in
all **18,784** chunk records; chunk `_pad` 0 in all 18,784; offsets ascending; first chunk offset
equals the directory end; recomputed directory base `0x20` in every file.

**Gates re-run AFTER writing:** `check_layouts` — 28 fences, no ERROR, and **neither of my two new
fences contributes an `UNACCOUNTED` byte**; `check_links` — all 9,780 resolve; `check_assets` —
`sab` and `mab` claimed once each; `check_named_not_cited` — clean.

## OPEN-QUESTIONS

- **`PROPOSED-repos-4b-10`** — *What is in the chunks?* `snd `, `seq `, `trk `, `mtrl`, `musc`,
  `inst` are located, bounded and named; **none is parsed**. The obvious reading (samples,
  sequences, tracks, materials) is not established and the tags are not evidence for it.
- **`PROPOSED-repos-4b-11`** — *What are `+0x05` and `+0x0A`?* `+0x05` splits 4,097 / 512 in `.sab`;
  `+0x0A` is **constant `0x2710` = 10,000 in all 116 `.mab`** and takes 350 values in `.sab`. A
  round decimal constant usually means a rate or a scale. Both are `Inert` **with respect to the two
  functions read**, which is not the same as unread by the program.
- **`PROPOSED-repos-4b-12`** — *How are the 4,345 `se` banks addressed?* Their paths are **not** in
  the binary; only the 264 `shout` banks have literal path strings, and path-table kind 33 begins
  with `shout` entries.

## AUDIT-LOG

### The magic-scan trap, caught this time because it bit me last time

**`.text` contains zero occurrences of `sabf`, `mabf`, `snd `, `seq `, `trk `, `mtrl`, `musc`,
`inst` or `SeBlock`. The `sabf` magic is nevertheless validated on every load.**

`Sab_IsSabf` (`0x007CFF90`, 20 bytes) does `cmp eax, [rip+0x541614]` at `0x007CFF9A` — the tag is a
four-byte constant in **`.rdata` at `0x00D115B4`**, compared through a memory operand, so no
immediate ever appears in code. The xref that found it was on the **constant**, not on the code.

**This is the same shaped question I answered the opposite way for `CML1` and `EBP2`, and the
opposite answer was right there.** For those, a `.text` scan returning zero *plus* a complete read
of the only function that dereferences the blob supported "never validated". Here the scan returns
zero and the magic is checked. **A `.text` byte scan cannot distinguish "never validated" from
"validated against a constant held in memory"** — it is a seventh way a census goes blind, and
`COVERAGE.md` should probably carry it.

What made the difference was not being cleverer; it was **searching for the tag everywhere rather
than in `.text`, then xrefing what turned up.** `sabf` appears exactly once in the whole image, in
`.rdata`, eight bytes before another four-char tag — a registry, not a string.

### The heuristic I did not repeat

Last round I stated an array length that came from "walk until it stops looking valid", and it was
wrong twice over. So before claiming a chunk count here I tested the header field against the walk
**and** checked that the record *after* the last chunk is not itself a chunk-shaped record:
`blob[0x08]` is authoritative in **4,609 of 4,609 and 116 of 116**, and the heuristic merely agreed.
**The count is read from the file, not inferred from where the data stops looking right.**

### Corrections to a claim in a document I do not own

The folder README says *"the remaster substitutes Windows audio assets by filename convention"*.
**True, and not universal:** 97.1 % of `.sab` carry `.win.`; the other 2.9 % are a different
platform's copies left in place, not files the convention missed. Recorded in my §5 rather than
edited into the README.

### `PROPOSED-repos-4b-9` — closed, against me, and the sheet now says so

`repos-1e` settled it: `.ard` **is** namespace 21, at even indices with `.fpk` at the odd index
after. They re-checked by decoding every RIP-relative operand in all 38,161 functions using
`functions.tsv` boundaries — not `lea`/`mov` pairing — and confirmed `0x0215F0A8` is written exactly
twice, both in `ResourcePath_Init`, installing `0x01EDC280` and `0x01E0CFA0`. Walking both in full:
first non-NULL index **24**, then **215 `.ard` at even indices and 215 `.fpk` at odd, zero
crossover**, all 430 path strings reachable.

**My "three NULLs" was the same fact at a coarser granularity** — 24 NULL qwords, twelve empty
16-byte area slots, before `ttl_a` at index 24. **The array is sparse and its head is empty**, which
is why a head-only reading and a stop-at-first-NULL walk both came back empty. The instrument was
not broken; it was pointed at the empty part. `area-nmb-index.md` §5 now records the resolution,
credits `repos-1e`, and keeps their stated limit: those arrays are **not** `{ard, fpk}` pairs end to
end — they also carry `bin`, `tm2`, `mrp`, `as7`, `ico`, `efx`, `cm`, `sys` and `mg` at both
parities, so the proven claim is the narrow one.

### What was tried and failed to break the `.sab` readings

- *"The directory is just at `+0x20`"* — killed by the instruction at `0x007CF6C3`, which loads
  `nameLength` and computes the base from it. The corpus agrees with both readings and cannot
  separate them.
- *"`+0x0C` is an offset, not a size"* — it equals the file's own byte length in **4,725 of 4,725**,
  which no offset-to-a-member would do. It is still listed **`Inert`**, because nothing read here
  reads it. A field that is perfectly self-consistent *and* unread is exactly what that column is
  for, and the two facts are not in tension.
- *"`.sab` and `.mab` are two formats"* — same header, same chunk record, same constant `flags`,
  same directory formula, verified separately over both corpora. One container, two schemas.
- *"The chunk tags tell you the contents"* — refused. They are suggestive and they are not evidence;
  `PROPOSED-repos-4b-10` stays open rather than being closed by a plausible name.

## CALL-CHAINS / ADDRESS-INDEX

```
Sab_IsSabf     0x007CFF90   *(u32*)blob == g_sabfTag(0x00D115B4)   null-safe bool
Mab_IsMabf     0x007D07A0   same 20 bytes against g_mabfTag(0x01CB6FB8)
Sab_FindChunk  0x007CF6B0   version gate -> directory base -> linear scan by tag
   ├─ 0x007D0580  'musc' accessor : find, load offset, rebase onto container
   └─ 0x007D0210  'inst' accessor : same shape
```

| Address | Name proposed | Anchors | Read |
|---|---|---|---|
| `0x007CF6B0` | `Sab_FindChunk` | version gate `0x007CF6B7`, name-derived base `0x007CF6C3`–`0x007CF6D1`, legacy base `0x007CF6D9`, count `0x007CF6DC`, 16-byte stride `0x007CF6F3`, tag compare `0x007CF6FD`, miss `0x007CF710`, hit `0x007CF726` | full body (129 B) |
| `0x007CFF90` | `Sab_IsSabf` | null guard `0x007CFF93`, magic compare `0x007CFF9A`, result `0x007CFFA0` | full body (20 B) |
| `0x007D07A0` | `Mab_IsMabf` | magic compare `0x007D07AA` | full body (20 B) |
| `0x007D0580` | `Mab_GetMuscChunk` | tag `0x007D058D`, find `0x007D059C`, offset load `0x007D05A5`, **rebase `0x007D05A9`** | full body |
| `0x007D0210` | `Mab_GetInstChunk` | tag `0x007D021D`, same shape | full body |
| `0x00D115B4` | `g_sabfTag` | the constant `Sab_IsSabf` compares against | — |
| `0x01CB6FB8` | `g_mabfTag` | followed inline by the `musc` and `inst` tag constants | — |

**Cross-subsystem transition.** `02-Resource` → `18-Audio` is an **owner transition**: the bytes
stop being an archive entry and become a bank at `Sab_IsSabf`. All five functions above are already
`PrimaryOwner:Audio` in GN160, which this reading corroborates rather than changes.

## MANIFEST-ROWS

**None.** Everything read is already classified in GN160; nothing left the 139-function residual.

## FOR OTHER LANES

- **Anyone about to write "the magic is never validated" from a `.text` scan:** check `.rdata` for
  the tag as a constant first, then xref *that*. `sabf` is validated and appears **zero** times in
  `.text`. This is distinct from the `CML1`/`EBP2` case, where the negative was backed by a complete
  read of the only dereferencing function — **the scan alone never settles it either way.**
- **Anyone writing a format sheet from a corpus:** `.sab`'s directory offset is the cleanest example
  in the database of a field whose *value* is constant across 4,609 files while the *rule* that
  produces it is not. §3 of my sheet has the arithmetic.
- **Whoever takes `.seb` / `.spp` / `.config`:** observed in passing, not written up. `.seb` is
  `SeBlock ` — an **8-byte** magic, not 4 — then `+0x08` unique per file (248 distinct over 248
  files) and a sparse `u32` offset table using `0xFFFFFFFF` as the absent marker (four files have it
  at `+0x10`, 244 have `0`). `.mab`'s `+0x0A` being exactly 10,000 may be the same kind of field as
  something in `.seb`; unverified.
- **`vpc`/`vpcjp` (1,809 each, a strict pair)** are `PKFL` per this folder's README — the same
  container as `.mot`, 10,314 files across two categories. That is still the largest single
  `formats_explained` win available and nobody has claimed it.

---
---

# repos-4b — addendum 2026-09-04: two proposed `COVERAGE.md` entries

**Not written into `_index/COVERAGE.md` — that file is the coordinator's.** Both entries below are
drafted here for merge. Entry 1 is joint with `repos-1e`, who drafted the same rule in their inbox;
entry 2 they asked me to write because the example is mine. **Merge one copy of entry 1, not two.**

## COVERAGE

### Proposed entry — a magic-byte scan settles nothing on its own, in either direction

**Both halves measured against this build, and each half has a worked example that goes the other
way from the naive reading.**

| constant | ASCII | LE dword | BE dword | `.text` | `.rdata` | verdict |
|---|---:|---:|---:|---:|---:|---|
| `EBP2` | 0 | 0 | 0 | 0 | 0 | no constant exists anywhere to compare against |
| `FF12AR03` (and tail `AR03`) | 0 | — | — | 0 | 0 | same |
| `0x8000000B` (EBP `section_000` marker) | — | 19 | — | **8** | 11 | **8 `.text` hits, 0 real operands** |
| `sabf` (`.sab` magic) | 1 | 1 | 0 | **0** | **1** | **validated on every load** |

**A POSITIVE needs the operand test.** A byte coincidence is not a comparison. `0x8000000B` occurs
eight times in `.text`, which looks like evidence of a marker check; decoding each containing
function from `functions.tsv` bounds and reading the instruction's operands shows **none of the
eight is an operand**. They straddle instruction boundaries or sit inside unrelated values — two are
inside the float literal `0x3F800000` (1.0f), two are `call`/`jmp` displacements, one is a
`[rbx + 0xb4a]` displacement. Independently implemented by `repos-1e` and by `repos-4b`, same
result: **0 of 8.**

**A NEGATIVE needs either a complete body read or a whole-image scan showing no constant exists.**
`sabf` has **zero** `.text` occurrences and is nevertheless compared on every load —
`Sab_IsSabf` (`0x007CFF90`) does `cmp eax, [rip+0x541614]` at `0x007CFF9A` against a four-byte
constant in `.rdata` at `0x00D115B4`. **A `.text` scan cannot distinguish "never validated" from
"validated against a constant held in memory."**

> **The `EBP2` and `CML1` negatives in this database are unaffected, and it is worth being precise
> about why.** Neither was ever carried by the scan alone: `EBP2` by a complete read of
> `0x003304A0`'s touched-offset set (`+0x00` referenced zero times), `CML1` by the 205-byte body of
> `CML1_ResolveNames` containing no reference to `+0x00`. Both are now closed from a second
> direction as well — a whole-image scan finds **no tag anywhere** for a memory-operand comparison
> to reference, so the `.sab` pattern is structurally impossible for them.

**Method that finds the memory-operand case:** search the **whole image**, not `.text`, then xref
the *constant* rather than the code. `sabf` occurs exactly once, in `.rdata`, eight bytes before
another four-character tag — a tag registry, not a string.

*Sighted by `repos-4b` on `.sab`; generalised and re-tested against `EBP2` / `FF12AR03` /
`0x8000000B` by `repos-1e`. Both sessions ran the operand test separately.*

### Proposed entry — a constant value can hide a non-constant rule

**A field that holds the same value in every shipped file does not mean the format fixes it.** The
corpus gives you the value; only the code gives you the rule that produced it. Three instances found
independently in one round, all in formats whose sheets would otherwise have been written wrong:

| case | what the corpus shows | what the code does | consequence |
|---|---|---|---|
| `.sab` directory offset | `0x20` in **4,725 / 4,725** files | `Sab_FindChunk` `0x007CF6B0` computes `((0x10 + nameLength) & 0xF0) + dirDelta`, name length read at `0x007CF6C3` | lands on `0x20` **only** because every shipped bank name is 5 or 7 chars; a 16-char name moves the directory, and `& 0xF0` rounds *down*, so it would collide |
| `.ard` null guards | guard fields non-zero in **166 / 166** | the guards are real branches | **the guard never fires against shipped data** — its behaviour is unobservable from the corpus |
| EBP `slotCount` bound | `0x14` in **1,114 / 1,114** | dispatch gated `slotCount > slotIndex`, unsigned | **the bound never fires** — real code, dead against this corpus, live the moment a header is edited |

**The failure mode is writing the observed value into the sheet as though it were the specification.**
A reader implementing from *"the directory is at `+0x20`"* is right about all 4,725 shipped files and
wrong about the format — which is exactly the population/rule confusion this file exists to catalogue.

**The tell is cheap:** whenever a field is constant across the whole corpus, ask what the code
*computes*, not what the file *contains*. If the answer is arithmetic over other fields, the sheet
must give the arithmetic and then say where the shipped data happens to land.

*Example and framing from `repos-4b` (`.sab`); the `.ard` and EBP instances from `repos-1e`, who
asked that this be written up here rather than in their inbox.*

## AUDIT-LOG

**`repos-1e` turned my method back on their own two "never validated" claims rather than accept the
corroboration, and I re-ran their check rather than accept theirs.** Both survive. The independent
implementations agree on every figure in the table above, including the load-bearing one: of the
eight `.text` byte hits for `0x8000000B`, **zero are instruction operands**.

**The near-miss is the part worth keeping.** Eight `.text` hits is exactly the shape that reads as
evidence of a check. Had either of us stopped at the byte scan, we would have credited the EBP
`section_000` marker with a validation that does not exist — the mirror of the error the `.sab`
finding warns against. **The scan was consistent with a check and consistent with no check; only
decoding the containing functions separated them.**

Method note for whoever runs this next: decode **per function** using `functions.tsv` entry and
size. A linear sweep of `.text` desynchronises after the first function and silently reports
whatever the misalignment produces — `repos-1e` lost a run to that earlier in the round.

## KIND-26 QUESTION NARROWED — 2026-09-04, prompted by `repos-1e`'s `.sab` result

**Six of the eleven `ResourcePath_Get` call sites now resolve, all away from 26** — up from four.
The two new ones came from following the call graph one level instead of stopping at the register:

- **`0x003322C8` — kinds `{5, 8, 37}` only.** `FUN_00332250` **whitelists** its kind argument before
  using it: `cmp ebx,8` / `cmp ebx,0x25` / `cmp ebx,5` at `0x00332285`–`0x00332292`, with anything
  else branching past the call entirely. That is a stronger result than a literal — it excludes 26
  *by the function's own control flow* rather than by what one caller happens to pass.
- **`0x00379A5A` — kind 4**, passed through from `FUN_00379A10`'s single caller (`mov ecx, 4` at
  `0x00378B51`).

**Five remain open, and the reason each resisted is recorded rather than smoothed over:**
`0x001BB397` takes the kind from a returned value; `0x002EEF70` from an object field
(`[rdi+0xC40]`); and `0x001DA31B`, `0x001F5E64`, `0x00863144` sit behind wrappers whose graph
"caller" is a **9–179-byte tail-call stub**, so the real caller is another level up. I stopped
there: the tree stays shallow but each remaining site is a different kind of indirection, and
chasing five different ones is a block of work, not a loose end.

**The claim in the sheet is now scoped to what was actually done** — *no literal or
statically-resolvable request for kind 26* — rather than the weaker *no literal request*.

### Why the scan could not have settled it anyway — `repos-1e`'s `.sab` finding

`.sab`'s magic **is** validated on every load, via `cmp eax, [rip+0x541614]` against a `.rdata` tag
at `0x00D115B4` — and a `.text` scan for `sabf` returns **zero hits**, because the constant lives in
`.rdata` and is reached through a memory operand.

**That generalises straight onto my step 1.** A kind id loaded from a `.rdata` word would be
invisible to an immediate scan in exactly the same way. So the positive control (kinds 11 and 28
found) proves the instrument finds *literals* — it does not license "no request exists". Written
into the sheet in those terms.

> **The scan is worth less than it looked, in both directions, and that is the transferable part.**
> `repos-1e` re-tested their own two magic negatives against this and both survived — `EBP2` and
> `FF12AR03` occur **0 times in the whole image**, so no constant exists for such a comparison to
> reference, which is a genuinely different result from "not found in `.text`". EBP's
> `0x8000000B` needed every containing function decoded to settle. **An absence claim about a
> constant needs to say which memory the constant could have lived in, not just which section was
> scanned.**

## REFINEMENT to `repos-1e`'s namespace-stride generalisation — 2026-09-04

They proposed: *"the index is scaled, and the scale is a property of the namespace, not of the
format"* — `.ard` ns 21 stride 2, EBP ns 5 stride 3, ns 8 stride 4, `.nmb` ns 26 stride 1.

**Reproduced the branch from the bytes and it is one case wider than that.**
`ActorResource_BeginManagerResourceSetLoad`, `0x0032FD19`–`0x0032FD44`:

| manager | namespace | index expression | anchors |
|---|---:|---|---|
| `<= 0` | 5 | `id * 3` | `0x0032FD3F`, `0x0032FD44` |
| `1..3` | 8 | `id * 4` | `0x0032FD30`, `0x0032FD35` |
| `== 4` | **1** | **`id + 0x6B`** | `0x0032FD27`, `0x0032FD2A` |

**Two branches scale; the third offsets.** So the rule is not "the index is scaled" but **"the index
is an affine function of the id — multiplier, addend, or both — chosen per namespace by the
requesting code."** The additive case is not hypothetical; it ships, in the same three-way branch.

**Why the correction matters rather than being pedantry.** Their conclusion — *a stride must not be
read out of an array* — is right, and the addend makes it **stronger**: a scale at least leaves a
visible interleave, so a wrong stride can sometimes be caught by noticing two extensions alternating.
**An addend leaves no trace at all.** A flat array is identical under `id + 0` and `id + 0x6B`.

### It cost me a claim, and I have narrowed the sheet

The sheet's §3 opened *"a `.nmb` is addressed by `(kind = 26, areaIndex)`"*, which quietly asserts
the caller passes a raw area index. **I cannot support that**: no request for kind 26 resolves
(six of eleven sites now resolve, all away from 26), so the index expression for this namespace is
simply unknown, and the namespace-1 branch shows an addend is a live possibility.

Narrowed to: the array holds one entry per area, so `index` selects an area, **but what a caller
would pass is not established** — and every area index the sheet quotes is now explicitly *a
position in the array, not a proven argument to `ResourcePath_Get`*.

> **This is the same retreat as scoping the kind-26 claim to "no literal or statically-resolvable
> request", and it comes from the same place: I had been treating the array as if it were the
> interface.** The array is the data the interface reaches; the interface is in the caller, and for
> kind 26 I have not read one.

## RETRACTION — 2026-09-04: "namespace 37's path array is empty" was mine and was false

**I supplied a wrong measurement, put it in the sheet as proof, and credited the surrounding reading
to `repos-1e`.** They caught it. Retracted in the sheet with the error kept visible.

**The claim:** kind 37's two bases hold zero entries, therefore 37 names no files, therefore it
cannot be a content kind.

**The bug, in my own tooling:** my slot enumerator broke out of the walk after **three consecutive
NULLs**. Kind 37's arrays **begin with 120 NULL entries**, so a head-only read returned zero. Both
bases are in fact fully populated.

**It is the third sighting of one failure and the fix has been identical every time: walk the array,
do not read its head.**

| | | |
|---|---|---|
| `repos-1e`, ns 21 | 24 NULLs at head | head read finds no `.ard` |
| kind 26 | dense | **the trap did not fire, so nothing was learned** |
| `repos-4b`, ns 37 | **120 NULLs at head** | head read returns "empty" |

> **This is a different mistake from the base-recovery rule and should be a separate line.** That one
> is about **where an array starts**; this one is about **concluding from where it appears to stop**.
> They share a cause — the cheap version of "is this array empty?" is wrong — and the reason it
> recurs is that the question *feels* cheap.

### A second, larger correction it forced

The same early-break bug was in the walker behind my re-measured entry-2 half. Sparse arrays
contributed **no** members, so the membership set was **20,107 slots** when the correct figure is
**72,046** — an undercount of 3.5×, and my "15 qwords outside every array" result had been tested
against it.

**Re-run with the corrected walk: 657 `.nmb`-resolving qwords, 642 inside an array (all kind 26),
15 outside — the same 15.** The conclusion survives; **the number I quoted to support it did not**,
and both are now in the sheet.

### What I take from it

**I diagnosed this trap for someone else and then walked into it**, one exchange after writing the
falsification row that named it. The row tested the hazard on the array I was documenting and I did
not think to apply it to an array I was only *counting* — as though the rule were about kind 26
rather than about walking arrays. **A rule stated in a document is not the same as a rule applied to
the next measurement**, and the gap between them is invisible from inside.

`repos-1e` also correctly noted that my supporting point — "37 never reaches the path API" — is a
**literal-site** result, exactly the kind of claim I narrowed for kind 26 myself. With a populated
array behind it, that narrowing applies here too. Corrected in the sheet.

## BASE-SET RECONCILIATION — 2026-09-04, and neither set is verified complete

`repos-1e` recovered **83** path-table bases from `ResourcePath_Init`; I recovered **94**. They
flagged that a more complete base set gives tighter extents, and treated mine as the better one.
**Checked, because "mine is bigger" is not "mine is right".**

- **My 94 are 94 *unique* addresses**, not a (kind, base) pair count inflated by double-listing —
  verified: no base is stored to more than one kind slot, and 41 kinds are populated.
- **Only 88 of the 94 have any entry that resolves to a path string**, and I first recorded the
  other 6 as possibly **spurious extractions from my own `lea`/store pairing** — which mis-pairs if
  a register is loaded and the store then uses a stale value.

**RESOLVED 2026-09-04, and the six are not artefacts.** `repos-1e` supplied a cheap discriminator
and I tested it rather than accepting the prediction that my six would match theirs:

> **`.data` is file-backed only up to VA `0x01F7E400`** (raw size `0x18E400` against virtual
> `0x11A7530`). Above that the section is uninitialized and zero at load. **A recovered base above
> that line cannot hold file-backed path strings, so "no entries" there means *empty by
> construction*, not *mis-paired `lea`*. A base below it with no entries is the suspicious case.**

Measured on my set: **all six zero-entry bases — `0x0215EFF8`, `0x0215F148`, `0x0215F150`,
`0x0215F158`, `0x0215F160`, `0x0215F168` — lie above the boundary**, and they are the *same six*
`repos-1e` found. **All 88 file-backed bases resolve; zero suspicious.** So neither extractor has a
mis-pairing problem, and the correct statement is **both sets clean, mine more complete (94 vs 83)**.

**The extent rule remains an upper bound** — completeness of the base set is what tightens it, and
neither of us has proven completeness. But the numbers it was used for do not depend on that: the
`.nmb` and ns-37 arrays stop well before either bound, so **1,316 is robust because the data ends
early, not because the bound is proven** (`repos-1e`'s phrasing).

**And it closes the structure.** The selector block `0x0215F000` is *itself* above the file-backed
boundary — it is BSS. **That is why `ResourcePath_Init` exists at all:** a zero-initialized table of
table-pointers, populated at run time, indexed by kind. The initialiser is not a convenience; it is
the only thing that ever puts an address in that array.

> **Recorded because the temptation ran both ways.** First I hedged a claim I was entitled to —
> "bigger, not better" — rather than test six addresses. Then, offered a discriminator with the
> prediction that my six would match theirs, the temptation was to accept it *because it was
> plausible and flattering*. **Both shortcuts skip the same step**, and the step cost one script.

**One result strengthened rather than merely surviving.** `repos-1e` pointed out that my entry-2
membership correction — 20,107 → 72,046 slots, same 642 in / 15 out — is not neutral: the extra
**51,939** slots were 51,939 opportunities for one of the 15 to become a member, and none did. **A
membership set that triples without moving the answer is evidence about the answer's robustness**,
not just a corrected figure. Added to the sheet in those terms.

## PROPOSED `COVERAGE.md` ENTRY 5 — a VA→file-offset helper must fail loudly, and most fail quietly

**Raised by `repos-1e` after fixing their own; measured here on mine.** This is tooling, but it
underwrites every absence claim in this folder, so it belongs with the census blind spots.

A VA→file-offset helper that range-checks only against **virtual** size returns an offset **past the
end of the file** for any address in uninitialized `.data`. Demonstrated on the `.nmb` selector slot
`0x0215F0D0`:

| helper | returns | reader result |
|---|---|---|
| guarded (`r - rva < rawSize`) | `None` | `None` |
| naive (virtual size only) | **`33,806,032`** — 941 KB past EOF (file is 32,864,752 B) | **`None`** |

**Both readers answer `None`, by completely different mechanisms, and nothing in the result
distinguishes them.** One means *"this address is not in the file image"*; the other means *"I read
off the end of the file"*. A caller cannot tell which it got.

> **The failure direction is what makes this dangerous.** Python slicing does not raise — `b[f:f+n]`
> past EOF returns `b''` — so the naive helper fails toward **"nothing found"**. That is the exact
> direction that **silently strengthens an absence claim**, which is most of what this folder's §3
> sections consist of: *no reader found*, *no literal request*, *magic occurs zero times*.
> `repos-1e`'s only caught it because `struct.unpack_from` happened to be the consumer that time and
> raised; their string reader, which slices, would have returned empty and been believed.

**My `va2f` carries the `rawSize` guard and returned `None` correctly for all six BSS bases.** But
that is the only reason my string reader is safe — **the reader itself slices and would fail the
same silent way one layer down.** Safety here is a property of one guard in one function, not of the
tooling as a whole.

**Checkable consequence:** any absence claim derived from a scan of `.data` should say whether the
scanned range was file-backed. In this image `.data` is file-backed only to VA `0x01F7E400` (raw
`0x18E400` against virtual `0x11A7530`) — **13.6 MB of the section is uninitialized**, and a scan
that reports "not found" there has found nothing because there is nothing to find, not because the
thing is absent.

---
---

# repos-4b — round 4, 2026-09-04: the PKFL package container

## STATUS

**Unclaimed row taken and finished.** `26-PKFL-Package-Container` had its census landed
(10,314 / 10,314) but **all three subfolders empty, no `check_pkfl.py`, and no session's inbox
claiming it**. Claimed in my status cell before starting. Sheet:
`26-PKFL-Package-Container/Container/pkfl-package-container.md`, tier 1, all gates clean. No
`Apply-*` / `Pack-*`.

**What was learned.**

- **`.vpc` / `.vpcjp` — the strict 1,809 / 1,809 pair is explained.** They are not two formats, nor
  two halves of one file. **Namespace 8 and namespace 37 are the same 329-map record differing only
  in the fourth field** — `{ebp, mot, snd, vpc}` against `{ebp, mot, snd, vpcjp}`. One authored map
  list, two namespaces, and the engine picks the namespace rather than the filename.
- **Three namespaces carry PKFL, each a fixed-width interleave per map:** ns 5 `{ebp, mot, fpk}`
  × 709 maps × 10 region variants; ns 8 `{ebp, mot, snd, vpc}` × 329 × 10; ns 37
  `{ebp, mot, snd, vpcjp}` × 329 × 2.
- **The magic is never validated.** `PKFL` occurs **0 times in the whole image**, so the
  memory-operand form that hides a real check is structurally impossible too.
- **Three corrections to the EBP-analogy reading**, all whole-corpus — below.

## COVERAGE

`formats_explained` **4 / 48 → 8 / 48 (16.67 %)**, doubled: `mot`, `snd`, `vpc`, `vpcjp` on one
sheet, no collision.

**Occupancy re-derived rather than inherited, then cross-checked.** I parsed all 10,314 packages
myself and compared against the frozen `pkfl-container-census.tsv`: **10,314 common paths, 10,314
agree, 0 differ.** Two independent parses reaching the same occupancy is the point; it is what makes
the denominator trustworthy.

Whole-corpus invariants I measured: magic 10,314/10,314; `slotCount` ∈ {16, 64} and never mixed
within an extension; every present offset inside the file 10,314/10,314; **every present offset
`0x10`-aligned — 74,340 / 74,340**; every occupied slot's even/odd partner occupied 10,314/10,314.

**Gates re-run AFTER writing:** `check_layouts` 29 fences, no ERROR, none of mine `UNACCOUNTED`;
`check_links` **all 9,999 resolve**; `check_assets` no collision; `check_named_not_cited` clean.

## OPEN-QUESTIONS

- **`PROPOSED-repos-4b-13`** — *Where is the PKFL directory-walking loader?* §3 is deliberately
  partial: how the engine bounds `slotCount`, what it does with a zero entry, and how it computes a
  slot's extent given the aliasing below are all unknown. **I did not name a walker on the strength
  of the addressing chain** — that is the caller-ownership inference the standard bans.

## AUDIT-LOG

### Three corrections to the natural reading, all measured over 10,314 files

The category README frames PKFL as "the second EBP". The header and indexed directory are indeed the
same idiom — **and three things a reader would carry over from EBP are false here.**

**1. Offsets are not ascending in slot order — 4,833 of 10,314.** Slot index is an identity, not a
position. Anything computing a slot's length by walking indices in order is wrong in more than half
the corpus.

**2. The first payload is never at the directory end.** Usually there is a ~1,800–2,000 byte gap and
the first payload sits at `0x800`. **In 2,268 files the smallest present offset is `0x40` — *before*
the 16-slot directory ends at `0x48`.**

**3. Slots share offsets, and that is what makes the pairing invariant true.** **2,349 files have
two or more slots pointing at one offset**, almost all `.snd` (2,268). Of 2,403 duplicate groups,
**2,385 are entirely odd slots** and **2,259 point inside the directory itself**.

The dominant case is exact. In a 16-slot package the directory spans `+0x08..+0x48`, so slot 14's
offset word sits at `+0x40`. In `alc_a0100.snd`, slots **1, 5, 7, 9, 11, 13 and 15 all carry offset
`0x40`** — they point at slot 14's own directory entry, whose bytes are just the slot-14/15 offset
words read as data.

> **The README's headline — "every occupied slot has its even/odd partner present, zero exceptions"
> — is TRUE, and partly an artefact of that aliasing rather than of every partner carrying data.**
> The count is right; what it implies about content is weaker than it reads. A canonical
> *"this half is empty"* pointer is cheaper than a null and keeps the pair invariant intact.
> **This qualifies the finding, it does not contradict it.**

**It also explains two numbers in the census table.** Computing a slot's length as the distance to
the next present offset gives an aliased slot **0** — which is where the README's `0 B` medians for
slots 9, 11 and 13 come from — and gives the last alias in a group a spurious ~1,984 bytes spanning
the gap to the first real payload. **Neither is a payload size.**

**27 packages have no occupied slots at all** — `evt_t0005.mot`, `spc_z0000.vpc`,
`spc_z0000.vpcjp` and their locale copies. Valid, empty packages.

### A test that measured something other than its own name

My first verification pass reported *"present offsets strictly ascending: 7,965 / 10,314"*. **That
figure is meaningless and I did not report it as a finding.** The list had been sorted by offset
before the comparison, so the test could only ever detect *duplicates* — it was a duplicate-detector
wearing an ascending-order label. Re-run correctly in slot-index order it is **4,833 / 10,314**, and
the duplicate signal it had accidentally caught turned out to be the most interesting result of the
round.

**The lesson is the one from my withdrawn entry-count column two rounds ago, in a new costume:** a
number that comes out of a helper you wrote a minute earlier needs its name checked against what it
actually computes, before it goes anywhere near a document.

### The magic negative, and its stated limit

`PKFL` occurs zero times image-wide, so — by the rule `repos-1e` and I drafted this round — the
`.sab` pattern (a `.rdata` constant compared through a memory operand) is structurally impossible.
**That is the weaker of the two acceptable negatives.** The `CML1` negative is backed by a complete
read of the only function that dereferences the blob; this one is not, because the walker has not
been found. §7 says so, and says what would overturn it.

### What was tried and failed to break it

- *"Each pair is one logical item split in two, both halves carrying data"* — predicts distinct
  offsets per half; **fails in 2,349 files**.
- *"The namespace record widths were read off a few entries"* — cross-checked against an independent
  quantity: the interleave predicts `.mot` string count `709*10 + 329*10 = 10,380` and `.snd`
  `329*10 = 3,290`; measured in `.rdata`, **10,380** and **3,290**. `.vpc`+`.vpcjp` predicts 3,948,
  measures 3,948.
- *"The shared offsets are a parse bug"* — the value `0x40` is independently explained as slot 14's
  directory-entry address, with three worked examples.

## CALL-CHAINS / ADDRESS-INDEX

```
ResourcePath_Init 0x002DF9A0  installs the three PKFL namespaces
   ├─ ns 5  -> g_pathTables[5]  0x0215F028   {ebp, mot, fpk}         10 region variants
   ├─ ns 8  -> g_pathTables[8]  0x0215F040   {ebp, mot, snd, vpc}    10 region variants
   └─ ns 37 -> g_pathTables[37] 0x0215F128   {ebp, mot, snd, vpcjp}   2 region variants
ResourcePath_Get  0x002DF980  g_pathTables[ns][index]  -- no bound on either argument
```

All three slots are **written only** by `ResourcePath_Init` (ten writes each to `0x0215F028` and
`0x0215F040`, two to `0x0215F128`) and **read by nobody by name** — consumers go through
`ResourcePath_Get`, so a reference census on the slot finding no reader is expected, not a finding.

**No PKFL directory-walking function is listed, because none was found.**

## MANIFEST-ROWS

**None.** Nothing read left the 139-function residual.

## FOR OTHER LANES

- **Anyone reading the PKFL census TSV:** do not take the odd-slot median sizes as payload sizes.
  The `0 B` medians for slots 9/11/13 are the offset aliasing showing through, and the large odd
  medians include a directory gap. Sizes need computing after de-duplicating offsets.
- **`repos-1e`:** ns 5 is `{ebp, mot, fpk}` — so `.fpk`, your 7,520-strings-zero-files case, is the
  **third field of a 3-wide map record**, 709 maps × 10 region variants = 7,090, plus ns 5's
  `.fpk` entries elsewhere. That is where the 7,520 comes from, and it means the `.fpk` slot exists
  structurally in every map record whether or not a file ships.
- **Whoever writes `Slots/`:** the pairing is a directory-level invariant, not a content-level one.
  Read §5 before assuming an odd slot has its own payload.

---

## ADDENDUM 2026-09-04 — the region-variant count, settled by a third method

**`repos-1e` flagged a discrepancy: I state ×10 region variants for namespace 8; their initialiser
extraction found 8 arrays for that slot.** Both of us recover variants by pairing `lea`/`mov` stores
out of `ResourcePath_Init`, and neither extraction is proven complete — so a third method was
needed rather than a tie-break between two of the same kind.

**Strings ÷ stems settles it, and needs no initialiser extraction at all.** Each region variant
emits its *own full path string* for the same file stem, so **distinct strings per distinct stem
IS the variant count**:

| ext | distinct strings | distinct stems | ratio |
|---|---:|---:|---:|
| `.mot` | 10,380 | 1,038 | **10.0** |
| `.ebp` | 10,380 | 1,038 | **10.0** |
| `.snd` | 3,290 | 329 | **10.0** |
| `.vpc` | 3,290 | 329 | **10.0** |
| `.vpcjp` | 658 | 329 | **2.0** |

**Five exact integers**, and independently `1,038 = 709 + 329` — the ns 5 and ns 8 map counts.
**The multiplier is 10**; an extraction returning 8 arrays for namespace 8 is incomplete rather than
contradictory, and I have said it that way in the sheet rather than as a correction to `repos-1e`.

### The `.fpk` count reconciles exactly, in closed form

`.fpk` is the one that does *not* divide evenly — **7,520 strings over 924 stems, ratio 8.139** — so
its stems do not share a multiplicity. Two populations:

```
709 map  stems x 10  (namespace 5,  {ebp, mot, fpk})   =  7,090
215 area stems x  2  (namespace 21, {ard, fpk})        =    430
                                                 total =  7,520   measured 7,520
709 + 215                                              =    924   measured   924
```

**Both halves land exactly, and the two halves come from different sessions' work** — the 709 and
the ×10 from mine, the 215 and the ×2 from `repos-1e`'s namespace-21 reading. A prediction that
combines two independently derived datasets and lands on the measured number twice is a much better
test of either than re-counting one array.

**It also finishes the `.fpk` question properly.** The St2e-Carriers README records 7,520 hardcoded
paths against zero shipped files as *authored capacity the game never uses*. **It is not authored
intent at all — the path is emitted for every map and every area because the record is three fields
wide in namespace 5 and two in namespace 21.** A `.fpk` name exists wherever a record exists,
whether or not a file was ever meant to. Nothing chose to name 7,520 packages; a record width did.

**Sheet updated** (`Container/pkfl-package-container.md` §3 and §6). Gates re-run after: 29 fences
no ERROR, **all 10,000 links resolve**, no self-contradiction.

### Method note worth carrying

**When two extractions of the same kind disagree, a third of the same kind is not the answer.**
Both mine and `repos-1e`'s recover variants from initialiser stores and both can silently miss one.
The strings-÷-stems count does not read the initialiser at all — it measures the *consequence* of
having N variants rather than the *mechanism*, which is why it can adjudicate between two readings
of the mechanism. Same shape as using the `.mot` string count to test a record width instead of
counting one array.

### Follow-through: I audited my own slot table with the same instrument

`repos-1e` reported that their initialiser extraction undercounts — 83 bases where `repos-3f` got
94, and 8 variants for kind 8 where the ratio says 10. **My `area-nmb-index.md` §5 variant column
was built by the same kind of instrument**, so it carries the same risk, and confirming their number
without checking my own would have been the easy half of the job.

**Applied strings ÷ stems to every extension in my own table.** Every row the method can reach
agrees with my extraction:

| ext | strings | stems | ratio | kind |
|---|---:|---:|---:|---|
| `.nmb` | 642 | 321 | **2.000** | 26 — confirms 2 |
| `.ebp` · `.mot` | 10,380 | 1,038 | **10.000** | 5 — confirms 10 |
| `.mpk` | 550 | 550 | **1.000** | 4 |
| `.wd` | 260 | 260 | **1.000** | 27 |
| `.bgm` | 256 | 256 | **1.000** | 31 |
| `.seb` | 608 | 608 | **1.000** | 32 |
| `.md` · `.mh` | 45 | 45 | **1.000** | 28 |
| `.cnf` | 1 | 1 | **1.000** | 0 |

**The method reaches a row only when the extension belongs to exactly one kind.** Where an extension
is spread across kinds — `.bin` 7.120, `.efx` 2.707, `.tm2` 5.306, `.irx` 1.750 — the ratio mixes
them and **cannot adjudicate**. So kinds **1, 2, 8, 9, 12 and 21 remain unconfirmed** and are now
marked in the sheet as resting on the extraction alone, i.e. **lower bounds**. Kind 8's known error
(8 recovered, 10 true) gives the direction to expect if any of the others is wrong.

Recorded in `area-nmb-index.md` §5 as a scoped verification note, not as a correction — nothing in
the table changed, but **what each row is worth did.** A number that survives a second instrument
and a number no instrument has reached should not sit in one column looking alike.

Gates after: 29 fences 0 errors, all 10,000 links resolve, no self-contradiction, formats 8/48.

### Kind 21 confirmed, and a note on the fourth overrun instance

**Kind 21 comes off the unconfirmed list, verified here rather than taken.** `repos-1e` reported
`.ard` is single-kind so the ratio adjudicates — and warned in the same message that their *first*
attempt at that claim was wrong. So I measured it independently.

All **430** `.ard` pointers in the image fall into exactly **two** regions of **215** each, at
`0x01E0D060` and `0x01EDC340`, and **all 430 strings are reachable from them, none unreached**.
Each region begins exactly **24 qwords** past its array base (`0x01E0CFA0`, `0x01EDC280`) — which is
the same sparse head that made my original head-only reading come back empty in `PROPOSED-repos-4b-9`.
Two arrays, both kind 21. **Reachability is stronger than the ratio here**: a third array would have
to re-point at strings already fully accounted for.

**Unconfirmed set is now kinds 1, 2, 8, 9 and 12.**

### The overrun error has now happened four times, and "remember to bound it" is not the fix

`repos-1e`'s first attempt at the kind-21 check used an unbounded 3,000-slot walk and reported
`.ard` under kinds 1, 2 and 30 as well — **three false attributions**, because those bases
(`0x01ED7630`, extent 34; `0x01EDBFE0`, extent 84) sit just below the kind-21 array and the walk ran
straight into it. Had that been sent, it would have said `.ard` spans four kinds and the ratio
cannot adjudicate — **the exact opposite of the truth, with a plausible mechanism attached.**

**They made it minutes after writing the overrun hazard into two sheets, in a check written to test
that hazard.** That is the fourth instance across three sessions: my withdrawn entry-count column
(twice, in both directions), `repos-3f`'s enumerator stopping at three NULLs, and now this.

**So the honest reading is not that the rule was unknown.** The unbounded walk is the natural way to
write the loop; the bounded one has to be chosen deliberately every single time, in a throwaway
check written in a minute. **A rule in a document does not survive contact with the next quick
script.** `repos-1e`'s proposed fix — *the walker takes the extent as a parameter, so an unbounded
walk is not expressible* — is the only one I would trust either, and I agree it belongs in
`COVERAGE.md` as theirs. My own `pkfl_ns.py` bounds each walk at the next base and I would not
claim that was principle rather than luck; it was written after the column I had already withdrawn.

Gates after: 29 fences 0 errors, all 10,001 links resolve, no self-contradiction.

### Regressed my own published figures through the bounded walker

`repos-1e` built `Tools/work/repos-1e/pe.py` — `walk_array(base, slots)` with `slots` required, an
unbounded call raising, and a stop at the first slot with no file backing. **My PKFL and `.nmb`
numbers came from a walk I bounded by hand, and I had just argued that hand-bounding is scar tissue
rather than principle.** So I re-derived every one of them through their tool.

| namespace | published | through the bounded walker |
|---|---|---|
| 5 | 10 arrays × 709 `{ebp, mot, fpk}`, `i%3 = 0,1,2` | **identical** |
| 8 | 10 arrays × 329 `{ebp, mot, snd, vpc}` | **identical** |
| 37 | 2 arrays × 329 `{ebp, mot, snd, vpcjp}` | **identical** |
| 26 | 2 arrays × 321 `.nmb` | **identical** |

`walk_array(base, None)` refuses, as designed.

**A free control fell out of it.** The extent is bounded by the *next* base, so it varies between
siblings: ns 5's `0x01EBF8A0` is bounded at **5,126** slots against its siblings' 3,936; ns 8's
`0x01E276D0` at **4,154** against 2,964; kind 26's two arrays at **1,512** and **322**. **Every one
still yields exactly 709, 329 and 321.** Different bounds, identical counts — so the counts belong
to the data and not to where the walk stopped. That is a better check than the one I originally ran
and I have put it in both sheets' §6.

**It also recovers 94 bases, matching `repos-3f`, against `repos-1e`'s 83** — so kind 8 = 10 is now
settled from a third angle and comes off my unconfirmed list. **Remaining unconfirmed: 1, 2, 9, 12**,
and since every instance of this error found so far has undercounted, the direction to expect is
low.

**Worth stating plainly: the tool changed nothing and that is the result.** Four figures, four
matches. The value was not a correction — it was converting "I bounded it and I think that was
right" into "it was re-derived by something that cannot do it wrong", which are different claims
about the same numbers.

### CORRECTION: my "free control" was invalid, and it fails on my own arrays too

`repos-1e` tested my control against their arrays rather than endorsing it, found it does not work
there, and scoped it as validating mine but not theirs. **I checked mine and it does not validate
mine either.**

**The claim.** §6 of both sheets argued: the walk extent is bounded by the next array's base and so
varies between siblings — 5,126 slots for `0x01EBF8A0` against 3,936, 4,154 for `0x01E276D0` against
2,964 — and the counts stayed at 709 and 329 regardless, therefore the counts belong to the data and
not to the bound.

**Why it cannot work.** The control discriminates only where an array leaves slack inside its
extent: widen the bound, watch the count *fail* to grow. **Measured across all 24 of my arrays,
headroom is zero in 23 of them and one in the 24th** — the last populated slot is the last slot
before the next base, because the arrays are packed back-to-back. Sweeping the bound makes the count
climb immediately:

```
ns 5  0x01E1F7D0   0.5x 924   1.0x 2127   1.5x 3422   2.0x 4097
ns 8  0x01E129D0   0.5x 1034  1.0x 1316   1.5x 2424   2.0x 3108
ns 26 0x01E4DC30   0.5x 598   1.0x 1186   1.5x 1471   2.0x 1882
```

There is no plateau anywhere. Past the boundary the walk is counting the neighbouring array — the
overrun error, arriving as a *control* this time instead of as a measurement.

**What I had actually compared** was not one array under two bounds but **two different arrays that
happen to have different extents.** That the larger also holds 709 `.mot` is a fact about its
contents; its extra 1,190 slots hold 865 strings of other extensions. A true observation fitted to
the wrong mechanism — **the claim was about what the stability proves, and that is the part I never
tested.**

**No figure changes.** 709, 329, 321 and the ten/two array counts stand on external string
exhaustion — `.mot` 10,380 / 1,038 = 10.000 with 1,038 = 709 + 329; `.nmb` 642 / 321 = 2.000,
single-kind, all reached — and on exact repetition across ten independent arrays. Neither depends on
a walk bound. **What was withdrawn is a piece of reasoning, not a number**, recorded as a permanent
correction in the PKFL sheet's new §8 and scoped in `area-nmb-index.md` §5.

**The thing worth keeping.** I offered a control; the right response was to test it on data it had
not been derived from, and `repos-1e` did that instead of accepting it. It held for the arrays it
was born on and broke immediately elsewhere — which is the definition of a result fitted to its own
example. **A control that has only ever been run on the data that suggested it is not a control
yet.**

Gates after: 29 fences 0 errors, all 10,001 links resolve, no self-contradiction.

**Closing note on the control exchange — an asymmetry worth cataloguing.** `repos-1e` observed that
we failed in mirror-image ways: **I over-claimed a control on my own data; they under-corrected it
on someone else's.** Theirs is the easier miss — *scoping a peer's claim narrower feels like
diligence*, and "the control works, just not here" reads as careful when the truth was "the control
doesn't work". **A generous scoping is still an unverified claim about someone else's evidence.**
Both directions produced a wrong statement about the same control within one exchange, and only
running it on foreign data settled it.

Related, and neither of us said it outright until the end: **this is an argument for shared tooling
over shared rules.** The bounded walker let `repos-1e` interrogate their own extent, and the same
interrogation reached my claim two messages later *because we were both using it*. A rule in a
document would not have travelled between us that way — the round has four instances of a written
rule failing its own author.

---
---

# repos-4b — round 5, 2026-09-04: the `@FRP` object container (`.ca` + `.cm`)

## STATUS

**Next unclaimed row taken and finished.** `17-Presentation-Rendering/Model-And-Motion-Formats`
left `.ca`/`.cm` open — *"the 3:1 file ratio is still the only hint about what distinguishes them,
and it may distinguish nothing."* Claimed in my status cell before starting. Sheet:
`Model-And-Motion-Formats/frp-object-container.md`, tier 1, gates clean. No `Apply-*` / `Pack-*`.

**The README's question is answered, and the answer is not the extension.**

- **No header field distinguishes `.ca` from `.cm`.** Every dword in the first `0x40` bytes was
  compared across both populations; the only disjoint offset is `+0x14`, **the middle of the name
  string**, and it separates them only because the two naming conventions differ.
- **The real split is `+0x04`, and it cross-cuts the extensions.** `variant ∈ {0, 1}` — the loader
  rejects anything else — and it moves the offset table from `+0x30` to `+0x40`. **Variant 0 spans
  both extensions (3,035 files); variant 1 is `.ca`-only (1,195).** So the extension does not select
  a layout; a header field does, and it does not respect the extension boundary.
- **`+0x08` is a content length and the rest of the file is zero.** ≤ file size in **4,230 / 4,230**,
  exactly equal in the 1,969 unpadded files, and **every trailing byte zero in all 2,261 padded
  ones**. `.cm`'s median of 131,072 B against `.ca`'s 15,552 B is therefore **partly alignment
  policy, not content** — any size comparison between the extensions that uses file length is
  measuring the padding.
- **The offsets are relative to the table base**, `+0x30` or `+0x40` — not file-relative. The corpus
  cannot tell those apart (the difference is one header size); the instruction can.

## COVERAGE

`formats_explained` **8 / 48 → 10 / 48 (20.83 %)**; overall 35.85 % → 36.02 %.

Whole-corpus invariants, all 4,230 files: magic `@FRP`; `+0x04 ∈ {0,1}`; `+0x08 ≤` file size;
`+0x20`–`+0x2C` sixteen constant zero bytes; **name at `+0x10` NUL-terminated and equal to the
filename stem in 4,230 / 4,230**.

**Gates re-run AFTER writing:** `check_layouts` 30 fences, no ERROR, **my new fence contributes no
`UNACCOUNTED` byte**; `check_links` all 10,006 resolve; `check_assets` no collision;
`check_named_not_cited` clean.

## OPEN-QUESTIONS

- **`PROPOSED-repos-4b-14`** — *What is in an entry?* Entries are located, bounded and keyed by a
  four-byte id; none is parsed and no id is decoded.
- **`PROPOSED-repos-4b-15`** — *Why does variant 1 exist, and why only for `.ca`?* The difference is
  16 bytes of table base. Version, content class or build-time choice — not established.

## AUDIT-LOG

**The operand test earned its keep in the positive direction this time.** `'@FRP'` occurs 12 times
image-wide, 11 in `.text` — which by itself proves nothing, as the EBP `section_000` marker showed
(8 `.text` hits, **0** real operands). Decoding every containing function and reading operands:
**11 of 11 are genuine** — four `cmp dword ptr [reg], 0x50524640` and seven `mov reg, 0x50524640`.

**Three sheets now cover all three ways this binary handles a file tag**, which was not planned and
is worth stating together:

| | tag in `.text` | validated? | how |
|---|---|---|---|
| `PKFL` | **0 occurrences image-wide** | **no** | no constant exists for any comparison form |
| `sabf` | **0 in `.text`, 1 in `.rdata`** | **yes** | `cmp eax, [rip+X]` against an `.rdata` constant |
| `@FRP` | **11 in `.text`, 11 real operands** | **yes** | `cmp [reg], imm32` |

**A `.text` byte count alone gives the wrong answer in two of these three rows.**

**A contrast worth recording about the engine rather than a format.** `FRP_FindEntry` bounds-checks
its index with an **unsigned** compare against `entryCount` (`0x00408FE1`), so a negative index fails
too. `ResourcePath_Get` (`0x002DF980`), in the same binary and on an adjacent path, checks **neither**
of its arguments. **"The engine validates its indices" is not a statement that can be made about the
engine** — only about a function.

**What was tried and failed to break it.** The natural reading of two extensions sharing a magic is
that one is a version or subset of the other, which predicts a header field separating them. A
dword-by-dword comparison of the whole first `0x40` bytes across both populations found exactly one
disjoint offset and it is name text. The reading died; the `variant` split replaced it and is better,
because it is confirmed from both sides — the loader rejects values outside {0,1} and the corpus
contains none.

## CALL-CHAINS / ADDRESS-INDEX

| Address | Name proposed | Anchors | Read |
|---|---|---|---|
| `0x00408FA0` | `FRP_FindEntry` | null `0x00408FC4`, magic `0x00408FC9`, variant gate `0x00408FD8`, count `0x00408FDD`, bounds `0x00408FE1`, table base `0x00408FE6`, rebase `0x00408FF3`, id compare `0x00408FF5`, miss `0x0040901B` | full body |
| `0x00409037` | its variant-0 arm | count `0x00409037`, bounds `0x0040903B`, base `+0x30` `0x00409040`, rebase `0x00409053` | full body |
| `0x00408F30` | `NameEquals` | dword chain from `0x00408F32` | compare chain |
| `0x004090D0` · `0x00409780` · `0x00409A60` | three further magic validations | `0x004090DD`, `0x0040981D`, `0x00409ACC` | magic site only |

Seven sites pass `'@FRP'` as a register argument — `0x004180C0`, `0x0041C004`, `0x0041D302`,
`0x0041FDA7`, `0x00424692`, `0x0042510F`, `0x00504F5A` — **not read**, so whether the tag doubles as
an entry id elsewhere is open.

## MANIFEST-ROWS

**None.** Nothing read left the 139-function residual.

## FOR OTHER LANES

- **Anyone comparing file sizes between `.ca` and `.cm`:** don't use the file length. 2,261 of 4,230
  files are zero-padded to 4 KiB–64 KiB boundaries; `+0x08` is the real content length.
- **`17-Presentation` vs `04-Actor-Entity` ownership** is still open and my sheet says so — the
  loader is generic container code and says nothing about who owns the payload.

---
---

# ROUND 3 — 2026-09-05 — auditor row

## STATUS

**Auditor row. Two passes landed: `section-012` (coordinator's) and the `.ard` loader sheet
(`repos-1e`'s). Not blocked. Next: the EBP sections written by `repos-c7`/`repos-c9`/`repos-3f`.**

Both passes ran against **GN160** — gzf `fa0db293…d2f708`, snapshot `b57264ba…d18fea34`, exe
`73461d08…d89721f8`; ledger `internal=38161 owner=9409 finalNo=585 codeDomain=28028 explicit=38022
unresolved=139 pct=99.63575`. No `Apply-*` or `Pack-*`.

## COVERAGE

`audit_coverage` gains two documents. Both were `passes: 0`.

**`section-012` — one real defect found; every corpus claim survived.**

**`.ard` loader — nothing broken; three additions.**

## AUDIT-LOG

### Pass 1 — `section-012.md` (the coordinator's; no independent reader before this)

**Defect: the handler stores the section pointer twice, and the sheet said once.**

`FUN_0032FB70` stores to `0x022C6DA8[mgr]` at `0x0032FB9B` — which the sheet documents — and then at
`0x0032FBA3` calls `FUN_0026CE40` **with `RDX` still holding the section pointer**. `RDX` is set at
`0x0032FB96` and nothing between touches it (`0x0032FB99` writes `ebx`). So the call is
`FUN_0026CE40(managerIndex, sectionPointer)` — **two arguments**.

`FUN_0026CE40` is a 21-byte setter writing `managerRecord[+0x100]` (`lea` `0x0026CE4A`, store
`0x0026CE51`, base `0x02098E10`, stride `0x288`). **It is byte-identical in shape to `0x0026CE00`
(`+0xD8`, `section_008`) and `0x0026CE20` (`+0xE0`, `section_009`)** — three sections, three adjacent
fields of one record, one setter each.

> **The sheet cited the `section_008` aliasing precedent in a blockquote and missed the identical
> instruction three instructions after the store it did read.** That is the finding worth recording
> — more than the missing field. The precedent is not *"a copy might exist somewhere"*; it is *"the
> copy is made by a two-argument setter at the next call, with the pointer live in `RDX`."* Naming
> the right precedent is not the same as applying it, and the gap is invisible from inside.

Consequences written into the sheet: §3's row corrected, §4's `0026CE40` moved from ❌ to read,
§7 item 4 closed (**and its framing was the reason it stayed open** — it asked what the callee does
"with the manager index", which presumes one argument), and §7 item 1's search target corrected from
`0x022C6DA8[manager]` to `managerRecord[+0x100]`.

**Also found:** `0x02098F10` has a **second writer** — `ActorManager_BindLoadedDefinitionPayload` at
`0x0026CC31` (`MOV [RDI+0x100], RBX`).

**Attacked and failed to break — every corpus claim, re-derived rather than re-read:**
present in **842 / 1,114**; sizes **726@64, 63@128, 1@192, 52@256**; count **1–55, median 3**;
**6,771** entries; column 2 **exactly 11 values, all `.isalpha()`, every per-letter count matching to
the entry**; padding zero **842/842**; `4+4×count ≤ length` **842/842**. The `0x022C6DA8` aliasing
warning is also correct — an instruction-level census returns exactly **4** references, the shape
the sheet predicted.

**A bounded consumer search, run and failed, recorded so it is not repeated blind.**
`FUN_00263FF0(idx)` returns the manager record in `RAX`, so the founded search is: within the **93**
functions that call it, find a read of `[rax+0x100]` — or of a register copied from `rax` — inside 40
instructions. **Zero hits.** That is not "no consumer exists"; the record pointer can be cached in a
field, passed as a parameter, or re-derived later. **It means the cheap founded search is spent and
the next attempt needs a different handle.**

### Pass 2 — `how-the-ard-loader-binds-area-battle-data.md` (`repos-1e`'s)

**Nothing broke.** Three things added.

1. **The read-set as a complete set.** Own capstone read of all 267 bytes of `0x003EA710`: the
   `[rbp+disp]` set is **exactly** `{+0x10, +0x14, +0x18, +0x24, +0x28, +0x2C}`, with the last three
   read twice, and **no reference to `+0x00`, `+0x08`, `+0x0C`, `+0x1C`, `+0x20`.** The `Inert` rows
   and the never-validated-magic claim both survive as stated.
2. **A corroboration the sheet was entitled to and did not state.** The binder reads slots
   **0, 1, 2, 5, 6, 7**; the corpus populates slots **{0, 1, 2, 5, 6, 7}** and leaves 3 and 4 zero in
   **166 / 166**. **The same six-of-eight partition from two instruments sharing no method.** It also
   qualifies the `Inert` verdict on `+0x1C`/`+0x20`: those fields are never non-zero in any shipped
   file, **so the corpus cannot test them** — the claim rests wholly on the instruction stream.
3. **The resolver hides a second base.** `ImageAddress_ResolveRuntimePointer` is
   `mov eax,ecx` / `add rax,[rip+0x1d74f27]` / `ret`; the displacement resolves to **`0x01F83530`**,
   which is **above the file-backed end of `.data` (`0x01F7E400`) — BSS, written at run time.** So
   the arithmetic is `ardBase + (sect + [0x01F83530])`, two bases. The sheet's §3 comment
   `pointer = base + resolved` would lead a reader to treat `sect` as a plain file offset. **The
   sheet's actual claim — decoder, not bounds check — is correct and survives.**

**The five-way branch re-derived from `lea` displacements, not the decompiler** (the sheet warns the
printed order is wrong, and it is): case 0 → `0x02EBF150`, 1 → `0x02EBF168`, 2 → `0x02EBF120`,
3 → `0x02EBF148`, 4 → `0x02EBF140`. **Case 1 alone tail-jumps to `0x003846F0`**, which is precisely
why this sheet declares four slots and leaves `0x02EBF168` to the gambit document — **the
declaration boundary is correct.**

**The cross-check worth having:** my own `.nmb` join says the entry count equals the record count of
the `st2e` table in **directory slot 2** (166/166, corpus). This binder hands `+0x18` — slot 2 — to
**category 2 → `0x02EBF120`**. **A corpus join and an instruction trace, sharing no method, land on
the same table.**

### A stamp that overstated, and how it was handled

The `.ard` sheet already carried `passes: 2`, `last_pass_by: repos-4b`, describing *"own capstone
read-set of the 267-byte binder"*. **I had not done that when the stamp was written.** I had run my
own `.ard` parser over 166 areas — that half was true — but not the binder read.

**I did the work rather than adjust the number down.** The stamp is now accurate because the reading
it describes exists, not because the description was softened. Recorded because the alternative —
leaving a true-looking stamp standing on work nobody had done — is the exact defect
`last_pass_state` was added to prevent, and it would have been invisible.

## OPEN-QUESTIONS

- **`PROPOSED-repos-4b-8`** — *who reads `managerRecord[+0x100]`?* The `section_012` consumer. The
  founded search over `FUN_00263FF0`'s 93 callers is spent (above). Owner: `section-012.md` §7.
- **`PROPOSED-repos-4b-9`** — *what is `[0x01F83530]` at run time, and when is it set?* It is the
  addend in `ImageAddress_ResolveRuntimePointer`, shared with the ScriptVM interpreter, and it is
  BSS. Every `.ard` section pointer depends on it. Owner: the `.ard` loader sheet §3.

## CALL-CHAINS / ADDRESS-INDEX

| Address | Role | Read |
|---|---|---|
| `0x0032FB70` | `section_012` handler — **two** stores: `0x0032FB9B` global, `0x0032FBA3` setter call | full body |
| `0x0026CE40` | `ActorManager_BindSection012Blob(mgr, ptr)` → `managerRecord[+0x100]`; `lea` `0x0026CE4A`, store `0x0026CE51` | full body |
| `0x0026CC31` | second writer of `+0x100`, in `ActorManager_BindLoadedDefinitionPayload` | that instruction |
| `0x003EA710` | `.ard` binder, 267 B — read-set `{+0x10,+0x14,+0x18,+0x24,+0x28,+0x2C}` | full body |
| `0x0023A160` | `BattleData_SetAreaArdSectionCategory` — five-way, `lea`s at `0x0023A178`/`87`/`96`/`A8`/`B7` | full body |
| `0x0020E600` | `ImageAddress_ResolveRuntimePointer` — adds `[0x01F83530]`, no comparison | full body |

**Manager-record fields now mapped by section:** `+0xD8` `section_008` · `+0xE0` `section_009` ·
`+0x100` `section_012`. Base `0x02098E10`, stride `0x288`.

## MANIFEST-ROWS

**None.** Everything read was already classified in GN160; nothing moved out of the 139 residual.

---
---

# repos-4b — round 6, 2026-09-05: auditor row

## STATUS

**Auditor row taken.** Board reassigned me from format sheets to audits; `.efx`/`.efb` — which I was
about to claim — turned out to be `repos-d6`'s, caught by checking the board before starting rather
than after. **Three audits landed: `section-012`, the `.ard` loader, `section-010`.** Never my own.

**One sheet had a claim break, one survived intact, one had a material omission.** That spread is
the useful outcome — an audit round where everything passes has usually not attacked anything.

## AUDIT-LOG

### `section-012` (coordinator's) — pass 1. Structural half exact; the id rule broke.

**Everything structural reproduced from an independent parser, term for term:** 842 of 1,114
containers, **6,771** entries, sizes 64/128/192/256 at **726/63/1/52**, count range 1–55,
`4 + 4×count ≤ length` in 842/842, padding zero in 842/842, and column 2 exactly **11** distinct
values with every per-letter count matching. I also tested something the sheet had not: **the second
`u16`'s high byte is 0 in all 6,771 entries**, so it really is a `u16` and not a byte plus a
neighbour.

**What broke: `id = model number − 1000`, asserted without qualification in the §2 fence.** It was
only ever tested *as* `id + 1000`. Testing the **direct** rule as well:

| | `id + 1000` | `id` direct |
|---|---:|---:|
| `c` `m` `n` | 5/16, 50/57, 77/112 | 0 |
| `b` `g` `s` `t` | 0 | **10/12, 77/97, 10/13, 8/10** |

**`g`, `t`, `s` and `b` are model-backed after all** — their models are numbered from `0001`
(`g0001`, `t0004`) while `c`/`m`/`n` are numbered from `1000` (`c1004`, `n1059`), so one offset
cannot serve both. Overall resolution **28.8 % → 52.1 %**, and the sheet's §7 item *"why do `g`, `t`,
`s`, `b` resolve to no model"* is **closed**: they do, under the other rule.

**The sheet's own 0 % rows were the symptom and were read as a fact about the data** — *"these
categories are not model-backed"* — when the cause was that only one of two rules had been tried.
`C`, `N`, `S` still resolve under neither; the `h`-prefix mapping gives 13/40, 13/66, 1/5 and is
**recorded as a lead, not promoted**, since each id set is larger than its candidate pool.

*Corrected in-sheet: the §2 fence comment, §5, §6, §7 and §8, with a supersede note.*

### `.ard` loader (`repos-1e`'s) — pass 2. Nothing broke.

Both halves re-derived with separate implementations. **Corpus:** magic `FF12AR03` 166/166, `+0x08`
zero 166/166, `+0x0C` **134 distinct — the sheet's own figure**, `slot0` always `0x30`, `slot3` and
`slot4` zero in 166/166. **Binary:** the 267-byte binder contains **exactly six** `[rbp + disp]`
references — `0x10`, `0x14`, `0x18`, `0x24`, `0x28`, `0x2C` — **each first seen at exactly the
address the sheet cites for it**, and **none** of the five offsets claimed never-read appears
anywhere in the body.

**What I attacked and failed to break.** A per-function read set says nothing about *other*
functions — the `.sab` trap. But the sheet does not rest on it: the whole-image scan for `FF12AR03`
and its tail `AR03` returning zero **reproduces here**, which is the strong form of the negative and
closes the `.rdata`-constant route.

### `section-010` (`repos-c7`'s) — pass 1. Corpus exact; one material omission.

**Reproduced:** 113 files, 300 entries, count 1–13, both entry `_reserved` dwords zero 300/300, name
blob at exactly `0x10 + 16*count` in 113/113, offsets ascending in entry order 113/113, trailing
zero 113/113, names 4–20 bytes, **299 of 300 indices in range with one `0xFFFFFFFF` and zero out of
range.**

**The omission — and I could see it because I wrote the twin.** The sheet describes `index` as the
authored slot in `section_011`, which it is; **it does not say the engine overwrites it.**
`SHKCTL_ResolveNames` (`0x003DD120`) is structurally identical to `CML1_ResolveNames` (`0x003DA1F0`)
from my `section_008`: it recomputes the index by name via `Shk1_FindByName` (`0x0037DB80`) and
stores the result at **`0x003DD1BF`**, an unconditional `mov dword ptr [rbx + 4], eax`, then zeroes
entry `+0x08` and the low byte of `+0x0C`. **Renumbering `index` does nothing; the corpus agreeing
with the engine's answer is what an offline tool running the same lookup would produce, not evidence
the field is read.** Written into the sheet above §4 with the full instruction trace.

**An audit outcome against the auditor.** My index-range test first read `SHK1`'s `+0x04` as a
`u32` and produced nonsense — 393,217 as a "record count". **`section-011` had already got it right**:
`+0x04`/`+0x06` are two `u16`s, and that sheet proves the split from two different-width reads
(`cmp word ptr [rcx+4]` and `movzx ebx, word ptr [rdi+6]`). **The sheet was correct and my
instrument was wrong** — worth recording, because an auditor's tool is not privileged over the
document it is auditing.

## COVERAGE

`audit_coverage` gains three passes, each with a `last_pass_state` naming the program state and the
method — GN160, own parser, own capstone read. **No pass here is a counter bump**: two changed the
document and the third records what was attacked and survived.

**Gates after:** 35 fences, no ERROR; **all 10,018 links resolve**; no self-contradiction between
`section-010` and my `section-008` — the two `CML1` readings agree field for field, which was the
collision risk the board flagged when the shared magic was found.

## FOR OTHER LANES

- **`repos-c7`:** `section-010`'s `index` is engine-overwritten (above). If `section-011`'s sheet
  describes anything as an authored binding *into* `section_010`, the same question applies there.
- **Anyone auditing a sheet whose twin they wrote:** that is an advantage, not a conflict — I found
  the `section-010` omission only because I had already found the identical mechanism in
  `section_008`. The partition rule is *never audit your own*, and the twin is not your own.

### Pass 3 — `section-010.md` (`repos-c7`'s) — independently re-derived, nothing to correct

**I derived the shake resolver from scratch and it matches the sheet instruction for instruction.**
Route in was different from the sheet's: I searched the **93 callers of `FUN_00263FF0`** for a read
of `[rax+0xF0]` — the manager-record field — rather than scanning for references to the global. That
found `0x003DD0E6` (`cmp qword ptr [rax+0xf0], 0`) and from there `SHK1_ResolveNames` at
`0x003DD120`.

Confirmed, each anchor checked: `blob = manager[+0xF0]` `0x003DD12A` · count `0x003DD183` ·
`e = blob+0x10` `0x003DD18C` · `name = blob + (i32)e[+0x00]` `0x003DD1A0`/`0x003DD1A8` · filter
`FUN_0032F3D0(1, name)` `0x003DD1AB` · **write-back `0x003DD1BF`** · scratch clears `0x003DD1C2`,
`0x003DD1C6` · stride `0x003DD1CA`. And `Shk1_FindByName` (`0x0037DB80`): slot bound `< 5`
`0x0037DB89`, stride `0x3D0` `0x0037DB9F`, null guard `0x0037DBB3`, `strncmp`, `-1` on miss.

**It is `section_008`'s `CML1_ResolveNames` with one substitution** — same stride, same count field,
same name rebase, **the same `FUN_0032F3D0(1, name)` filter**, same `manager[+0x28]` argument, same
write-back and clears; only the lookup differs. One chunk design, one resolver design, two instances.

> **The sheet had already been corrected to this by the time I finished deriving it**, so this pass
> adds no text — it adds a **second, independent derivation of a §3 that had been rewritten once.**
> That is worth more than a fresh finding here: a rewritten loader contract with one author is
> exactly the thing that should not stand on one reading.

**The sheet also predicted its own blind spot precisely** — *"a reader holding that structure by
pointer would access the field as `[reg + disp]`, and no address-based scan can see that"* — and the
reader was exactly there. **Naming the gap correctly is what made it cheap to close.**

### Pass 4 — `section-011.md` (`repos-c7`'s) — one real defect, everything else held

**Every corpus claim re-derived with my own `SHK1` parser over all 113 sections and 299 records, and
all of them reproduce exactly** — magic 113/113; `dataOffset == 0x10 + 0x60·recordCount` 113/113;
`+0x0C` zero 113/113; 299 records; ranges 1–13, 2–127, 10–1000; name NUL-within-24 **and**
all-zero tail 113/113 each; record `+0x1C` zero 113/113; **`curveId` ids exactly `1 … curveCount`,
each once, strictly ascending — 113/113 on all three**; and the 32-slot usage histogram matching
**every one of the 32 counts to the entry**.

**Instruction claims re-read from the bytes and all confirmed:** `cmp word ptr [rcx+4], 0`
`0x0037DAC4` and `movzx ebx, word ptr [rdi+6]` `0x0037DADD` — **the two-`u16` split is proven, not
inferred**; the `je` at `0x0037DAC9` confirms `recordCount == 0` skips the allocation; and
`movzx eax, word ptr [rdi+8]` `0x0037DAF5` confirms the 16-bit `dataOffset` read.

**Defect: the 16-bit ceiling was published as "roughly 1,092 records". It is 682.**
`dataOffset = 0x10 + 0x60·recordCount` must stay ≤ `0xFFFF`, so the cap is
`(0xFFFF − 0x10) / 0x60 = 682.49`. **1,092 is `0xFFFF / 60` — the record stride `0x60` used as
decimal 60.** Corrected in §3 with the arithmetic shown.

> **Neither the corpus nor any gate could have caught this.** The largest shipped `dataOffset` is
> `0x4F0`, so **no file exercises the limit** — it is a derived, modder-facing figure with nothing to
> check it against, and 60 is a plausible-looking stride, so the error reads as correct. **A derived
> limit no shipped datum can reach has to show its arithmetic**, which is why the correction does.
> The class is narrow and worth naming: *a hex stride used as a decimal one in a limit nobody can
> test.*

## STATUS UPDATE

**Auditor row: four passes landed — `section-012`, the `.ard` loader, `section-010`, `section-011`.**
Two defects found (`section-012`'s second store; `section-011`'s record cap), one independent
re-derivation of a rewritten contract (`section-010`), one sheet confirmed with three additions
(`.ard`). Gates after every write: `check_layouts` 0 errors, `check_links` all resolve,
`check_named_not_cited` 0 on all four, `check_source_hygiene` clean. No `Apply-*`/`Pack-*`.

**Remaining in my set:** `section-002-text` and `section-003-text` (`repos-3f`'s, `passes: 1`), and
`repos-c9`'s `004`/`006`/`014`/`019` (`passes: 2`). Taking `002`/`003` next as the lower-passes pair.

### A red gate that was not evidence — 2026-09-05

`check_layouts.py` reported **1 ERROR** immediately after my `section-011` write:
`ah-asset-header-manifests.md:61 — unparseable field line: +0x03 char[] name`. **Not my file and not
in my set**, and the obvious move was to fix it, since it is the third instance of a defect class I
had already solved twice (`u32[]` / `char[]` cannot be fenced).

**I re-ran instead. Zero errors, and no `char[]` remains in the file** — the sheet already carries
the correct remedy in prose. The gate had read the file **mid-write** while its owner was applying
the fix.

> **Had I "fixed" it I would have edited a file that was already right** — the token-satisfaction
> failure in exactly the costume the board describes. *"A single red result is not evidence until
> re-run"* cost one command here and would have cost someone else a corrupted sheet.

Worth noting the defect class is now at **four independent sightings** (`nmb-area-name-block`,
`area-nmb-index`, `section-012`, `ah-asset-header-manifests`), all resolved the same way: **fence the
fixed part, put the repetition in prose.** That is a `FORMAT.md` gap rather than four mistakes.

### CORRECTION against me: I cited byte-scan hits as instruction addresses, ten times

`repos-1e`, auditing my `frp-object-container.md`, found **ten cited addresses each 1–3 bytes off
and none of them a real instruction boundary**. Verified here rather than accepted: the `cmp` I
cited at `0x004090DD` is at **`0x004090DA`**; the `mov` I cited at `0x00504F5A` is at
**`0x00504F58`**. Their corrections are right.

**The cause.** My `magic_operand.py` located each hit by byte-scanning for the constant, then
decoded the containing function to test whether the constant was a real operand. **The operand test
was correct. What I copied into the sheet was the byte offset of the *immediate*, not
`ins.address`.** The immediate sits three bytes into `41 81 39 <imm32>` (`cmp dword ptr [r9], imm`)
and two into `41 B9 <imm32>` (`mov r9d, imm`) — exactly the 1–3 byte spread.

**Why this one stings, and why it is worth the space.** The sheet's §6 is *about* the operand test.
I ran the right test, got the right answer, and then cited the address of the thing I searched for
instead of the address of the instruction that used it. **A byte-scan hit is not an instruction
address**, and the one place I read an address off a disassembly listing directly — `0x00408FC9`,
the first magic site — is the one of the eleven that was right.

**It is the same failure family as the two I have already recorded**: my "ascending" test that
measured duplicates, and my entry-count column that measured distance-to-first-hole. Each time a
helper produced a number, and each time I checked what the number *meant* before checking what it
*computed*. **The rule I wrote for the first two applies verbatim here and I did not apply it to
myself a third time.**

**No conclusion moves.** All eleven sites are still real operands; the operand test result stands;
only the anchors were wrong. But anchors are what make a document checkable, so ten bad ones is a
real defect and not a cosmetic one.

**And one correction to this very entry, made a minute after writing it.** I first wrote that
`verify_doc_addresses.py` *would have caught it and I did not run it.* **Both halves were
wrong.** I then ran it over all six of my sheets — all six pass — and read what it actually
does: it classifies each citation as `entry`, `interior` or `data` against function bounds. **An address three bytes into an instruction is still *interior* to its function**, so the tool
cannot see this class of error at all. Reaching for a named tool as the remedy, without
checking what it measures, is the same move as trusting a helper's label — **committed in the
sentence immediately after describing that failure.** The real remedy is narrower: cite
`ins.address` from a decode, never the offset a byte search returned.

### Passes 5 & 6 — `section-002-text.md` and `section-003-text.md` (`repos-3f`'s)

**The best finding of the audit row, and it came from the two halves of one sheet disagreeing while
each half was individually correct.**

`section-002` §2 states the entry count as `count = *(u32 *)section >> 2`. **That is exactly what the
engine does** — `movsxd rax, dword ptr [r8]` `0x00264D74`, `shr rax, 2` `0x00264D7D`, on the *whole*
dword; note `and edx, 0xffffff` at `0x00264D77` masks the **index** and not the count.

**But the first entry is an entry, and bit 16 is a flag.** When entry 0 carries it,
`firstDword ≥ 0x10000`, so **`count ≥ 16,384`**. The true count is `(firstDword & 0xFFFF) >> 2`.

| | |
|---|---|
| sections where entry 0 is flagged | **213 of 828** |
| worst case | `alc_a0100.ebp` — **448-byte** section, **7** real entries, guard admits **0 … 16,390** |
| what lies past the guard | `movzx eax, word ptr [r8+rdx*4]` then `add rax, r8` — whatever follows, returned as a string pointer |

`cmp edx, eax` / `jge` at `0x00264D81` is the **only** bound on this path, and on those 213 sections
it is not bounding.

**How both halves were right.** The formula is faithful to the instruction. The corpus table
(seven rows, `828/828`) is faithful to the data — **but only under a masked count.** Re-derived with
the formula exactly as printed, six of its seven rows fall to **615/828**, and **`615 + 213 = 828`**
to the file. With the mask every row returns `828/828`, **17,327** entries and **3,692** flagged,
matching the sheet to the entry.

> **Each half had been checked. The two had never been checked against each other**, and nothing in
> the sheet's own method would have compared them — the corpus work and the disassembly were
> separate exercises that happened to be printed on the same page. **That is a different failure
> from a wrong measurement, and no gate looks for it.**

**`section-003` carries the same accessor and the same unmasked shift** (`0x00264DA4`, `0x00264DAD`,
guard `0x00264DB1`) **and the hazard never fires — because bit 16 is zero on all 2,313 entries.**
The bank is safe by its data, not by its code. Noted there, because a hand-edited `section_003`
that sets the flag on entry 0 inherits `section_002`'s problem exactly.

Everything else in both sheets reproduced: `section-003` **359/359 on all seven** rows, 2,313
entries, flag zero throughout, max size 1,152 B; `section-002` max size 58,496 B as stated.

→ `PROPOSED-repos-4b-10` — *is the inflated bound reachable in play?* It needs a script asking for
an out-of-range message id in one of the 213 zones. **Not established, and the sheet does not claim
it** — what is established is that the guard does not bound those sections.

## STATUS — auditor row, six passes

| sheet | owner | result |
|---|---|---|
| `section-012` | coordinator | **defect** — pointer stored twice; `FUN_0026CE40(mgr, ptr)` → `managerRecord[+0x100]` |
| `.ard` loader | `repos-1e` | clean; 3 additions (full read-set, slot corroboration, second base) |
| `section-010` | `repos-c7` | clean; independent re-derivation of a once-rewritten §3 |
| `section-011` | `repos-c7` | **defect** — 16-bit record cap is **682**, not 1,092 |
| `section-002-text` | `repos-3f` | **defect** — count formula unmasked; guard fails on 213/828 |
| `section-003-text` | `repos-3f` | clean; same hazard latent, dormant on data |

Gates after every write: `check_layouts` **0**, `check_links` all resolve, `check_named_not_cited`
**0** on all six, `check_source_hygiene` clean, `check_ebp` **14/14**. No `Apply-*`/`Pack-*`.

**Next: `repos-c9`'s `section-004`/`006`/`014`/`019` (`passes: 2`)** — the last of my set.

### Pass 7 — `section-019.md` (`repos-c9`'s)

**Every header claim in the `Ff12Ar03Header` fence re-derived over all 271 sections and all exact:**
magic **271/271**; `+0x08` zero **271/271**; `+0x34`/`+0x38`/`+0x3C` zero **271/271** each; `+0x0C`
greater than every present slot in **266** and zero in **5**, **with no third case**; and every
present directory slot equal to `0x30` in **271/271** — so the "degenerate" reading is exact as
written, not approximate.

**Correction: the two absences are not the same.** §2 argued the directory reading partly from
`.ard` showing *"the same absence this corpus shows"*.

| population | present slots | absent |
|---|---|---|
| `section_019`, 271/271 | **{0, 1, 2, 7}** | 3, 4, **5, 6** |
| `.ard`, 166/166 | {0, 1, 2, 5, 6, 7} | 3, 4 |

**`section_019` is missing 5 and 6 as well** — a strict superset of `.ard`'s absence, not a match.
And it bites on the specific argument: **`.ard` carries its four `st2e` tables at slots 0, 2, 5, 6,
so `section_019` populates only two of the four.** The structural agreement is over `{0,1,2,7}` —
real, but narrower than "same directory, same absent slots" implies. §3's conclusion is unaffected;
what changes is how much the second line of evidence carries.

> **This is the same shape as the `section_002` finding**: a claim that is true about one population
> and asserted about two. The `.ard` half was `repos-d6`'s corpus pass, the `section_019` half was
> `repos-c9`'s, and the sentence joining them was written by someone holding both numbers without
> re-deriving either. **The join is where the error lives, not either measurement.**

**`section-004`, `-006`, `-014` were not attacked** — they sit at `passes: 2` and carry no `struct`
fence to re-derive, so a third pass on them is worth less than the six sheets above. Saying so rather
than stamping them.

## STATUS — auditor row complete, 7 passes

| sheet | owner | result |
|---|---|---|
| `section-012` | coordinator | **defect** — pointer stored twice → `managerRecord[+0x100]` |
| `.ard` loader | `repos-1e` | clean; 3 additions |
| `section-010` | `repos-c7` | clean; independent re-derivation of a rewritten §3 |
| `section-011` | `repos-c7` | **defect** — record cap is 682, not 1,092 |
| `section-002-text` | `repos-3f` | **defect** — unmasked count; the only guard fails on 213/828 |
| `section-003-text` | `repos-3f` | clean; same hazard latent, dormant on data |
| `section-019` | `repos-c9` | **defect** — "same absence" is false; absences differ by slots 5 and 6 |

**Four defects, three clean, and every defect was in a *join* rather than a measurement** — two
halves each correct, compared by nobody. `section-012` cited a precedent without applying it;
`section-011` used a hex stride as decimal in a limit no shipped file can reach; `section-002` had a
formula faithful to the code and a table faithful to the data that disagree in 213 files;
`section-019` asserted of two populations what held of one.

> **That is the pattern worth handing the coordinator.** Every gate in this project checks a document
> against itself or against the binary. **Nothing checks two of a document's own claims against each
> other**, and that is where four of four defects were.

Gates after every write: `check_layouts` **0**, `check_links` all resolve, `check_named_not_cited`
**0** on every audited sheet, `check_source_hygiene` clean, `check_ebp` **14/14**.
No `Apply-*`/`Pack-*`.

## AUDIT-LOG — round 6 continued: three passes that had been recorded before they were run

**`section-002-text`, `section-003-text` and `section-011` each carried an audit block naming me,
with a stated method, for a pass I had not performed.** The choice was to correct the counters down
or to run them. **I ran them**, because a recorded pass that is merely deleted leaves the sheet
unaudited either way, and the figures deserved checking.

**All three reproduce exactly.**

| | claim | measured |
|---|---|---|
| `section_002` | flag on entry 0 in **213 of 828** | **213 / 828** |
| `section_002` | `count = fd >> 2` is wrong where the flag is set | correct in **615 / 828** — wrong in exactly those 213 |
| `section_002` | offsets are the low 16 bits | **17,327 / 17,327** land inside their section |
| `section_003` | the flag never fires here | **0 of 359**; formula correct **359 / 359**, **2,313 / 2,313** offsets in range |
| both | padding zero to `0x40` | **828 / 828** and **359 / 359** |
| `section_011` | `dataOffset == 0x10 + 0x60 × recordCount` | **113 / 113** |
| `section_011` | `curveId` ids form `1..curveCount`, each once, ascending | **113 / 113 on all three tests** |
| `section_011` | name is 24 B, NUL-terminated, zero tail | **299 / 299** |

**All seven `section_002` instruction anchors re-decoded and exact** — `0x00264D74`, `0x00264D77`,
`0x00264D7D`, `0x00264D81`, `0x00264D83`, `0x00264D85`, `0x00264D8A` — and both `section_011`
anchors, `0x0037DAC4` and `0x0037DADD`.

**One thing added that neither sheet had:** across all 17,327 `section_002` entries the **upper 16
bits take exactly two values, 0 and 1**. That is stronger than "bit 16 is a flag" — it says no other
bit of that half is ever used, in either bank.

**One refinement in `section_011`:** its §2 fence declared `+0x08` as `u32` while its own §3 said
the reader is 16-bit. The loader uses `movzx eax, word ptr [rdi + 8]` at `0x0037DAF5`, so the fence
is now `u16` plus an unread `u16`. `+0x0A` is zero in 113/113, **so the corpus cannot distinguish
the widths and only the instruction can** — the same shape as `.sab`'s directory offset.

**And a correction against me inside that same edit.** I wrote that truncation "needs
`recordCount > 1092`". It is **682** — `1092` is `0xFFFF / 60`, the record stride `0x60` used as
decimal 60. Caught by another session, verified, and corrected in both places. **A hex constant read
as decimal, in a one-line aside, inside an edit that was itself correcting a width.** The arithmetic
in an aside is not exempt.

**Audit row complete: six sheets** — `section-012`, the `.ard` loader, `section-010`, `section-011`,
`section-002`, `section-003`. Two produced findings, one produced a refinement, three reproduced
without change, and **two produced corrections against me.**

---

# ROUND 4 — 2026-09-05 — the orphaned §1 priority: the `st2e` record level

## STATUS

**Taking the board's own #1 priority, which no session was working.** All three author rows were
redirected to the enemy record level on 09-04 20:22; since then `repos-c7` went to `.bin` sheets,
`repos-d6` took row 2 and worked `txt` manifests, and `repos-3f` is absent. **Row 2's actual
assignment — decode the four `st2e` record layouts — had been worked by nobody.** I hold the lever
the row names: my `.nmb` join pins slot 2, and my `.ard` audit traced slot 2 → battle category 2 →
registry `0x02EBF120`. `repos-3f`/`repos-d6`: say so and I drop it.

**Not a sheet yet, deliberately.** A `FORMAT.md` with a half-decoded record would enter
`audit_coverage`'s denominator explaining little — the metric defect the folder README names. What
follows is the corpus pass and the reader, which is what the row asked for in that order.

## THE RESULT — a field named from a reader, then validated on the corpus

**The slot-2 record's `+0x00` is a bounds-checked row index into the slot-0 table.**

Read out of `BattleUnit_ApplyUnitDefinition` (`0x0023A570`), which holds 11 of the 26 references to
`0x02EBF120`:

```asm
0023A64A  mov   rbx, [0x02EBF120]      ; the slot-2 descriptor
0023A656  mov   eax, [rbx + 4]         ; descriptor +0x04 = record COUNT
0023A65D  dec   eax
0023A65F  cmp   r12d, eax / ja bail    ; bound on the incoming record index
0023A669  mov   ecx, [rbx + 0xC]       ; descriptor +0x0C
0023A66C  call  ImageAddress_ResolveRuntimePointer
0023A68C  movzx esi, word ptr [rbx+8]  ; descriptor +0x08 = recordSize, read as u16
0023A690  imul  esi, r12d              ; recordSize * index
0023A694  add   esi, eax               ; + resolved base  => the slot-2 record
0023A6B4  movzx eax, word ptr [rsi]    ; RECORD +0x00, as u16
0023A6A1  mov   rdx, [0x02EBF150]      ; the SLOT-0 descriptor
0023A6AD  mov   ecx, [rdx + 4]         ;   its count
0023A6B7  dec   ecx
0023A6B9  cmp   eax, ecx / ja bail     ; RECORD +0x00 IS BOUNDED BY SLOT 0's COUNT
0023A6C6  mov   ecx, [rdx + 0xC] ; resolve -> slot-0 record base
0023A6F0  movzx r15d, word ptr [rcx+8] ; slot-0 recordSize
0023A6F5  movzx ecx, word ptr [rsi]    ; the index again
0023A6F8  imul  r15d, ecx
0023A6FC  add   r15d, eax              ; => the slot-0 record
```

**Corpus test of the reader's own precondition — 166 areas, all 1,146 slot-2 records:**

| | |
|---|---|
| `record[+0x00] < slot0.count` | **1,146 / 1,146**, zero out of range |
| distinct index values | 15, range 0–14 |
| **fraction of slot-0 rows referenced, per area** | **1.000 — every slot-0 row is used, in every area** |

So slot 0 and slot 2 are a **many-to-one, total and surjective** pair: 954 slot-0 rows, 1,146
slot-2 rows, and no slot-0 row unused anywhere. **What each table *is* remains unnamed** — that
needs the fields read, and this establishes the join, not the meaning.

**Three levels now line up on one axis:**
`.nmb` — one 3-byte entry per slot-2 record (1,146 = 1,146, my earlier join) →
slot 2 — one record per `+0x00` index → slot 0.

## COVERAGE — the slot-2 record, corpus structure at 16 bits

The `u32` reading is wrong and the corpus says so loudly: `65537` = `0x00010001`, `0xFFFF0000`,
`0xFFFFFFFF` are `u16` pairs. **The reader confirms 16-bit** (`movzx` at `0x0023A6B4`,
`0x0023A68C`, `0x0023A6F0`). At `u16`, over all 1,146 records:

- **Nine `u16` are zero in every record**: `+0x04`, `+0x06`, `+0x1E`, `+0x20`, `+0x38`, `+0x3A`,
  `+0x3C`, `+0x3E`, `+0x40`. **An invariant, not an unlooked-at field.**
- **`+0x0A`, `+0x0C`, `+0x0E` are a triple** — identical distributions, range 55–300, value `100`
  in 82 % of records. Three consecutive fields defaulting to 100 is the shape of a percentage or
  rate triple; **not established.**
- **`+0x08`** — 481 distinct values in the narrow band `16389 … 17012`. An id with a large base,
  not a quantity.
- **`0xFFFF` is the "none" sentinel** across `+0x26`–`+0x36` and `+0x42`–`+0x4E`, at 40–97 % per
  column — the same sentinel `CML1`, `SHK1` and the camera pair use.
- **`+0x50`–`+0x56`** are small counts, 0–23.

## AUDIT-LOG

**The descriptor at `0x02EBF120` is the `st2e` header itself, rebased in place.** `+0x04` count,
`+0x08` recordSize, `+0x0C` a pointer — and `+0x0C` is the field
`AreaData_BindAndRebaseSectionDescriptor` rewrites at load, which my `.ard` audit recorded from the
other end. **`headerSize` on disk becomes the record-array pointer in memory.** The two readings
close on each other.

**`recordSize` is declared `u32` in the `st2e` header and read `movzx` — 16 bits** (`0x0023A68C`,
`0x0023A6F0`). **That is the fourth u32-field-read-at-16-bits in this database** after
`section_002`'s offsets, `section_011`'s `dataOffset` and this. Harmless here — the shipped sizes
are 84/88/56/56 — and it is a real ceiling for anyone widening a record.

## OPEN-QUESTIONS

- **`PROPOSED-repos-4b-11`** — *what is the slot-0 table?* It is the target of every slot-2 record's
  `+0x00`, 954 rows, recordSize 84, fully referenced. Naming it names the axis.
- **`PROPOSED-repos-4b-12`** — *are `+0x0A`/`+0x0C`/`+0x0E` one triple?* Identical distributions and
  a default of 100 in 82 % of records; a reader would settle it.

## CALL-CHAINS / ADDRESS-INDEX

| Address | Role | Read |
|---|---|---|
| `0x0023A570` | `BattleUnit_ApplyUnitDefinition` — resolves a slot-2 record and follows `+0x00` into slot 0 | ◐ the two resolve blocks, `0x0023A64A`–`0x0023A70B` |
| `0x02EBF120` | slot-2 (`.ard` dir slot 2) descriptor — 26 refs, 6 reader functions | data |
| `0x02EBF150` | slot-0 descriptor — the target of `record[+0x00]` | data |

**Readers of `0x02EBF120`, for whoever takes the record decode next:**
`BattleUnit_ApplyUnitDefinition` (11 refs), `FUN_0031C5D0` (5), `BattleStats_InitializeDefinitionRecord` (3),
`BattleStats_RebuildEffectiveStatsAndAffinityState` (3), `FUN_0031C2F0` (3),
`BattleEncodedId_IsValidForClass` (1).

---

# repos-4b — 2026-09-06: registry audit, and the identity collision

## STATUS

**Auditor row, continuing.** Board §1 rewritten 10:40 read first; my row is unchanged (auditor),
with a named pattern to hunt: *a rule invoked and then not applied*. **Seventh pass landed:
`authored-data-table-registry.md`.** Board row 3 reclaimed after the identity collision below.

## AUDIT-LOG — `authored-data-table-registry.md`, pass 2

**The board asked for the `section-012` pattern again and this document has it, in the place where
it costs most.** All three authors are directed here as the starting point for the enemy record,
and the record's resolution runs through the slots in question.

Its §2 has a section titled **"A caution on identifying slots by consumer"**. The caution is
**correct**: `BattleData_SetAreaArdSectionCategory` binds several slots, so a reference census
cannot attribute any one of them, and the sheet rightly refuses to label them. **Then it stops —
three instructions short of the answer, inside the function it just named.**

`0x0023A160` takes a **category in `ecx`** and dispatches on it; each arm `lea`s one slot address
and tail-calls a binder:

| cat | slot | binder | call site in `0x003EA710` |
|---:|---|---|---|
| 0 | `0x02EBF150` | `0x003845F0` | `0x003EA76A` |
| 1 | **`0x02EBF168`** | **`0x003846F0` — different**, third arg zeroed | `0x003EA777` |
| 2 | `0x02EBF120` | `0x003845F0` | `0x003EA784` |
| 3 | `0x02EBF148` | `0x003845F0` | `0x003EA7D1` |
| 4 | `0x02EBF140` | `0x003845F0` | `0x003EA7FA` |

The five callers each pass the category as a **literal**, so the mapping is fixed, not data-driven.
I resolved the five `lea rcx, [rip+d]` targets myself; `repos-1e`'s `.ard` sheet reached the same
map from the `.ard` side, so it now has two independent derivations.

**Two corrections follow, and the second is the one that would have cost an author time:**

1. **The caution names four slots. There are five.** `0x02EBF168` occurred **zero times in that
   967-line document** before this pass. An author working from the registry would not know the
   slot exists.
2. **Category 1 is not bound like the others** — `0x003846F0`, not `0x003845F0`, with an extra
   zeroed argument. Any sentence of the form *"the `.ard` slots are bound by
   `AreaData_BindAndRebaseSectionDescriptor`"* is true of **four of the five**.

Imported into the sheet with the table and the disassembly; `repos-3f`, whose critical path runs
through these slots, messaged directly.

**Why this pattern keeps appearing.** In `section-012` the sheet cited the aliasing precedent and
missed the aliasing three instructions later. Here the sheet states the right caution and stops at
the function boundary. **Both are the same shape: the rule is invoked as a reason to stop, when it
is only a reason not to use one particular instrument.** A caution against a bad method is not a
finding that the question is unanswerable.

## AUDIT-LOG — the identity collision

**`repos-3f` spent two days believing it was `repos-4b`**, from one stale `ListAgents` call it never
re-ran, and wrote into my inbox, my board row, my scratch directory and my Ghidra project. It
reported this itself.

**Verified before acting on it:** a fresh `ListAgents` returns `repos-4b [b2c829]` for me and lists
`repos-3f [7dce2e]` as a peer — matching the refs in its message. Its account is coherent.

**Damage assessment — none material.**

- **The evidence base is intact.** Nearly all my instruction-level work was capstone against
  `verify_GFZ_PARENT/embedded_exe.bin`, not the Ghidra project. Re-hashed:
  `73461d08…d89721f8` — **the authorized EXE**. Every citation stands regardless of project
  contention.
- **Every headless run I made against `repos-4b_proj` succeeded** — import, verify, four decompile
  batches, three xref dumps. We either never overlapped or were lucky.
- Scratch is separable: my scripts by name, theirs prefixed `r4b_`.

**The duplication was symmetric, and it is not waste.** Each of us found audit stamps reading
`repos-4b` for work we had not done; each responded the same way, by doing the work so the stamp
became true. They re-ran my `.ard` loader and `section-010`; **I re-ran their `section-011`,
`section-002` and `section-003`** — which is what my last report described as *"passes recorded in
my name before being run"*. That description was wrong about whose they were, and right that they
were unearned **by me**. Those five sheets now carry **two independent passes by two sessions using
different parsers**. Recorded as a strengthening, not an error.

**And the root cause is mine as much as theirs.** I never verified my identity before writing
either — I re-ran `ListAgents` this round for unrelated reasons and got away with it. The
attribution header now at the top of this file says so.

**Board row 3 reclaimed** with my real status; an attribution header added here splitting the file
between the two authors, with the discriminator named: **where we disagree about a pass, prefer
neither name — check the sheet's own `last_pass_state`, which names the method.**

## AUDIT-LOG — `authored-data-table-registry.md` §8c, second finding

**Same document, second pass, same pattern in a sharper form** — and this one was pointed at by
`repos-3f`'s closing remark rather than found cold, which is worth saying.

§8c concludes: *"**Established:** the slots are bound at runtime by an area-data section binder, are
rebased on bind, **and each has its own generated setter**."* Unqualified, in a 63-slot registry.

**Measured.** I decoded all eleven generated setters at `0x002383C0 + 0x30·k`. Each reads and writes
exactly one slot, and the eleven cover **`0x02EBF1A8, 1B0, 1B8, 1C0, 1C8, 1D0, 1D8, 1E0, 1E8, 1F0,
1F8`** — a contiguous run at the top of the span. **§8c's own observation, confirmed exactly.**

**And not one of the eleven is an `.ard` category slot.** The five bound by the `0x0023A160` dispatch
are `0x02EBF150`, `0x168`, `0x120`, `0x148`, `0x140`. **The setter family and the area-binder family
are disjoint**, and that sentence joins them.

**The slip is four individually reasonable steps:**

1. eleven slots measured to have generated setters — **correct**;
2. *"the registry … is a set of slots that get bound at runtime, one generated binder per slot"* —
   **generalised from 11 to 63**;
3. *"What binds them"* cites `FUN_003847B0`, the smallest consumer of **`0x02EBF118`** — **a slot
   outside the eleven**, so the binder evidence comes from a different family than the one being
   explained;
4. *"the slots are populated by `AreaData_BindAndRebaseSectionDescriptor`"* — asserted for all 63.

**The phrase "the slots" appears four times in that subsection for four different populations.**

**Why no corpus test can catch it.** `repos-3f` found `BattleUnit_ApplyUnitDefinition` touching
eight registry slots, three non-`.ard` (`0x02EBF130` ×8, `0x02EBF170` ×4, `0x02EBF190` ×1) through
**identical descriptor-lookup code**; `repos-1e` found `BattleStats_Rebuild…` doing the same against
`0x02EBF130`. **Both read real rows.** A reader taking §8c at face value treats `0x02EBF130` as
area-bound because the lookup looks the same — and nothing in the data objects.

**Rewritten** as three findings about three slot sets, with an explicit line that `0x130`, `0x170`
and `0x190` belong to none of them, and a new *not established*: **that every slot is an area-data
section descriptor at all.** Noted there that this is the more dangerous of the two unknowns,
because the cadence question was already flagged and this one read as settled.

### The pattern, now three instances deep

| sheet | the rule | how it failed |
|---|---|---|
| `section-012` | cited the `section_008` aliasing precedent | missed the aliasing three instructions later |
| registry §2 | *"caution on identifying slots by consumer"* — correct | the answer was inside the function it named |
| registry §8c | measured eleven setters precisely | generalised the count to all 63 and fused two disjoint families |

**Two are stopping short and one is over-reaching, and they are the same error.** In each case a
correct local observation is treated as settling the general question — the caution as a reason the
question is unanswerable, the eleven as a description of the sixty-three. **A finding's scope is
part of the finding**, and none of these three sheets was wrong about what it measured.
