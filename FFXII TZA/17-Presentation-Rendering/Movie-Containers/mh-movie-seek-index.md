---
system: .mh — the PS2 movie seek index, shipped and not read
category: 17-Presentation-Rendering
status: AUDITED
owner_layer: PrimaryOwner:Presentation
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
corpus_validated: "43 / 43 .mh in the archive index, all opened, 2026-09-12"
last_reviewed: 2026-09-12
archive_formats:
  - "mh"
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-mh-seek-index-pass-1
  crossref_clean: true
  reopened_count: 0
---

# `.mh` — the PS2 movie seek index

> One small file per PS2 cutscene movie (`ps2data/movie_finish/<lang>/<name>.mh`): a `.mhe` header
> and a table of `{byte offset, frame, flags}` entries into the PS2 movie stream. The remaster plays
> `.webm` instead, and this build fetches the `.mh` path only to throw it away — **the files are inert**.

**Corpus validation.**

| | |
|---|---|
| files examined | **43 of 43** `.mh`, all opened |
| where | `ps2data/movie_finish/us` (35), `/in` (7), `/jp` (1) |
| size | 228 B – 94,356 B |
| magic `.mhe` | **43 / 43** |
| size = `0x18 + 12 × entryCount` | **43 / 43** |
| entry offsets and frames non-decreasing, first frame 0, last offset below `+0x0C` | **43 / 43** |
| `+0x08` / `+0x0A` | 512 × 352 in 37, 512 × 448 in 6 |
| a `.webm` with the same stem | **39 / 43** |
| `.md` files (the movie streams the index points into) | **0** shipped |

Census: [`census.py`](../../_experiments/evidence/mh-movie-index/census.py) →
[`census.out.txt`](../../_experiments/evidence/mh-movie-index/census.out.txt).

---

## 1. What the player sees

**Nothing.** The FMV cutscenes play from the remaster's WebM videos. On the PS2 each movie was an `.md` stream with this `.mh` index beside it so the player
could seek or resume inside the stream; the streams were not shipped with the remaster, the indexes
were, and nothing opens them.

## 2. The layout

```struct MheHeader base=file size=0x18
+0x00  char[4]  magic       '.mhe' in 43 of 43
+0x04  u8       field04     1 in 3, 5 in 34, 9 in 6
+0x05  u8       field05     1 in 43 of 43
+0x06  u16      field06     varies
+0x08  u16      width       512 in 43 of 43
+0x0A  u16      height      352 in 37, 448 in 6
+0x0C  u32      streamBytes above every entry offset
+0x10  u32      frameCount  1.00-1.05 x the last entry's frame
+0x14  u32      entryCount  size = 0x18 + 12 x entryCount in 43 of 43
```

```struct MheEntry base=record size=0x0C
+0x00  u32      offset      byte offset into the stream; non-decreasing
+0x04  u32      frame       frame number; non-decreasing, 0 in the first entry
+0x08  u32      flags       0 in 8,445, 2 in 6,105, 1 in 39 entries
```

The width / height and frame reading of `+0x08`–`+0x10` rests on the values (512 × 352 / 448 are PS2
video sizes, and `frameCount` tracks the last indexed frame), not on a reader: there is none (§3).

## 3. The loader contract

**There is no reader of the `01ECB4D0` paths.** The paths live in the resource path array for kind **28** (pointer at
`01ECB4D0`), in pairs: index `2m` is `…\<NAME>.md`, index `2m + 1` is `…\<NAME>.mh`. The image has
exactly two constant kind-28 lookups, and neither opens the `.mh`:

- **`001B7F30`** fetches index `2m` (`001B7F8A`–`001B7F93`), cuts the name between the last `\` and the
  `.` (`001B7FB4`–`001B7FF7`), and formats `"%s%s.webm"` (`008F8D70`) under `/GameData/D3D11/ArtData/video/`
  (`008F8D10`) — the `.md` path is used only for its name, and no `.md` file ships.
- **`0035B840`** (reached through `00356460`) fetches index `2m + 1` at `0035B8AE` and **discards the
  result**: the next instructions load `ecx` from its own argument and call `001848A0`, which does not
  read `rax`.

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| the whole file | — | — | — | **yes — no reader by three routes:** the magic `.mhe` occurs 0 times in the image (bytes and dword); the 45 `.mh` path strings sit in the kind-28 path array; both constant kind-28 lookups are read and neither opens the file |

The kind-28 array has 45 `.mh` names against 43 shipped files; the two extra names, `in\anx.mh` and
`us\dlb.mh`, have no file (and `anx.webm` ships with no `.mh`).

> **The array is NULL-*sparse*, not NULL-terminated** (measured 2026-09-13, §6). Indices
> **76–81 and 92–93** are empty and the array continues past them; the 45 pairs occupy ~~92 of~~ 90 *(corrected 2026-10-02, OPUS: the 98 qwords from `01ECB4D0` hold 90 non-null pointers)* of
> the first 94 slots. A walk that stops at the first NULL reports 38 `.mh` and loses
> `in\ANX.mh` — which is what happened on the first attempt at this check.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `001B7F30` | movie open: `.md` name → `.webm` path | ✅ full body |
| `0035B840` | fetches and discards the `.mh` path | ✅ full body |
| `00356460` | the stub that jumps to `0035B840` | ✅ full body |

### Data addresses

| Address | Name | Kind | Contents |
|---|---|---|---|
| `01ECB4D0` | kind-28 path array | `.data` | `OPN.md`, `OPN.mh`, `NAL.md`, `NAL.mh`, … |
| `008F8D70` | `"%s%s.webm"` | `.rdata` | the video path format |
| `008F8D10` | `"/GameData/D3D11/ArtData/video/"` | `.rdata` | the video root |

## 5. Corpus survey

`+0x04 = 9` in six (`bd2`, `opd`, `end`, `epl`, `opn`, `stf`); a height of 448 in six (`bd2`, `se1`, `se2`,
`opd`, `ivt`, `stf`). `stf.mh` is the largest at 94,356 B. The four stems without a `.webm`
are `in\bd2`, `in\se1`, `in\se2` and `jp\opd`.

## 6. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run first, one address at a time and read in full.)*

**Nothing on this page is wrong.** The corpus was re-extracted from `FFXII_TZA.vbf` and re-censused
with independent code — not by re-reading `census.out.txt` — and **every figure comes back
identical**:

| claim | re-derived |
|---|---|
| 43 `.mh`, us 35 / in 7 / jp 1 | **43**, us **35** / in **7** / jp **1** |
| magic `.mhe` 43 / 43 | **43 / 43** |
| `size = 0x18 + 12 × entryCount` 43 / 43 | **43 / 43** |
| offsets and frames non-decreasing, first frame 0, last offset below `+0x0C` | **43 / 43** |
| sizes 228 B – 94,356 B, `stf.mh` largest | **228 – 94,356**, largest is `us/stf.mh` |
| `+0x04` — 1 in 3, 5 in 34, 9 in 6 | **{1: 3, 5: 34, 9: 6}** |
| `+0x05` — 1 in 43 | **{1: 43}** |
| `512 × 352` in 37, `512 × 448` in 6 | **37 / 6** |
| flags — 0 in 8,445, 2 in 6,105, 1 in 39 | **{0: 8445, 2: 6105, 1: 39}**, 14,589 entries |
| `frameCount` is 1.00–1.05 × the last frame | **1.000 – 1.049** |
| 39 of 43 have a `.webm` of the same stem | **39 / 43**, and the four without are exactly `in/bd2`, `in/se1`, `in/se2`, `jp/opd` |
| `anx.webm` ships with no `.mh` | **true** — the webm is there, the file is not |
| 0 `.md` files shipped | **0** |
| §5: `+0x04 = 9` in bd2, opd, end, epl, opn, stf | **exactly those six** |
| §5: height 448 in bd2, se1, se2, opd, ivt, stf | **exactly those six** |
| §3: the kind-28 array holds 45 `.mh` names against 43 files, the extras being `in\anx.mh` and `us\dlb.mh` | **45 `.mh` and 45 `.md`**, and both extras are present |

### Route 1 is stronger than stated, and now has a control

§3 says the magic *"occurs 0 times in the image (bytes and dword)"*. Measured over the **whole 32 MB
file**, not just `.text`: `.mhe` occurs **zero times anywhere**. The control is a magic that *is*
read — **`SRYK`**, the BigFile header, occurs **once, and in `.text`**, which is what a magic a
reader compares against looks like.

> *(`PS2D` was tried as a second control and thrown away: 62,577 occurrences, none in `.text`. A
> four-byte literal that is also ordinary data cannot control anything.)*

### A fourth route §3 does not have: nothing reads the array `01ECB4D0`

`01ECB4D0` has **exactly one** code reference in the image — `002DFAF9`, in `FUN_002DF9A0`, and it is
a `lea` whose next instruction **stores the array's address into a global**. No function indexes the
array directly; the kind-28 lookups reach it through that published pointer. So the inertness claim
rests on four independent legs now: no magic in the file, no `.md` shipped, both constant kind-28
lookups read and neither opening the file, and **no direct reader of the array at all**.

### ⚠ The array has NULL slots inside it, and they cost me two false findings

Walking `01ECB4D0` and stopping at the first NULL gives **38** `.mh` names, no `in\ANX.mh`, and a
folder split of us 34 / in 4. **All three are artefacts.** The array has NULL entries at indices
**76–81 and 92–93** and continues past them; read to the end it holds **45 `.md` + 45 `.mh`**
(us 36 / in 8 / jp 1) in ~~92~~ 90 populated slots *(corrected 2026-10-02, OPUS: slots 0-97, less the NULLs at 76-81 and 92-93)*, exactly as §3 says.

> I drafted *"the array holds 38, not 45"* as a correction before checking where the strings are
> pointed from. Every one of the 45 is pointed at from **one contiguous run, `01ECB4D8`–`01ECB7D8`**
> — 776 bytes, past the index my walk had stopped at. **A terminator you assumed is not a
> terminator you measured**, and the cheap check was to ask the strings who points at them rather
> than asking the array where it ends.
>
> **This is worth recording on the page** because the next reader will walk the same array: it is
> **not** NULL-terminated, it is **NULL-sparse**.

**Not claimed.** `MH-1` stands — what `+0x04`, `+0x06` and the entry flags meant is still
unrecoverable from a build with no reader, and this pass adds no evidence about their meaning. The
width/height reading is still an inference from the values, not from a consumer. The two constant
kind-28 lookups were **not** re-derived here *(answered: see the screen-fade page, which re-derives `001B7F30` (2026-09-25); 2026-10-02, OPUS)*; §3's own account of `001B7F30` and `0035B840` is taken
as read, and only the array-reference route was measured independently. The archive was **read, never
written**, and nothing was executed.

## 7. What this document does not claim

- [x] **UQ-222.** What header fields `+0x04` and `+0x06` and entry flags 0 / 1 / 2 meant to the PS2 player — not
      recoverable from this build, which has no reader. `MH-1`.
      *OUT OF EVIDENCE BOUNDARY 2026-09-27 (FABLE, Claude Opus 5.5; signed by OPUS, non-author, d893251b4): answerable only
      from the PS2 executable `SLPM_667.50`, which the shipped `system.cnf` names and nothing ships. The residue stays
      unanswered in fact. [Package](../../_index/candidates/oeb-package-ps2-2026-09-27/README.md), [review](../../_index/candidates/oeb-ps2-review-opus/README.md).*

## 8. Related

- [Movie containers](README.md) — the `.webm` side.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings become reportable once citations written 0x... or FUN_... count (R5); tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — CLIENT.** `ResourcePath_Init` (2,831 bytes), which this page cites, is called from the 978-byte core start-up root.
- **Audio — CALLEE fan-out.** The `0067A9B0` teardown this page documents calls five Audio-layer helpers — `005CD330`/`005C5230` (paired release on `+0x218`/`+0x238` row buffers), `005CD5E0` (the `+0x4B8`/`+0x4D0` pair release), `005CD700` (`+0x508` clear), `005CD840` (`+0x508` acquire) — plus `005CD330`'s own Audio-side callers (`00211AC0` et al., 8 edges per `edges.tsv`). Crossing accounted: the movie container borrows the Audio row-buffer release contract; no ownership moves.
- **CombatAction - CLIENT (1 edge).** `00313A00` is called by bodies filed to CombatAction: `00313DB0` - shared machinery across the layer boundary, no shared ownership.
- **Gameplay - SERVICE (1 edge).** `00313DB0` reaches bodies filed to Gameplay: BattleRuntime_GetMode0To5FromFlagsAndFieldBit15 (`0030D9A0`) - shared machinery across the layer boundary, no shared ownership.
- **Input - CLIENT and SERVICE (2 edges).** `003C8990` is called by bodies filed to Input: InputGameplay_ArbitrateDigitalInputAndModalState (`00253C70`); `00313DB0` reaches bodies filed to Input: `00226BE0` - shared machinery across the layer boundary, no shared ownership.
- **InputGameplay - CLIENT and SERVICE (2 edges).** `002E1CA0` is called by bodies filed to InputGameplay: `00313A00`; `00313DB0` reaches bodies filed to InputGameplay: `00313A00` - shared machinery across the layer boundary, no shared ownership.
- **Movement - CLIENT (1 edge).** `00313DB0` is called by bodies filed to Movement: `00234520` - shared machinery across the layer boundary, no shared ownership.
- **Party - MECHANICAL (1 edge).** Shared-helper fan-in on BattleUnit_ResolveByFocusHandle (`0031B7E0`). All 1 edges run through it - one accessor’s spread, not a per-caller relationship.
- **Resource - SERVICE (10 edges).** `0017D960`, `001B7690`, `001B7F30`, `001B82F0` (+4 more) reach bodies filed to Resource: `0017D940`, `0017D960`, `001D9F90`, `001DADA0` (+3 more) - shared machinery across the layer boundary, no shared ownership.
- **Save_Load_Settings - CLIENT (2 edges).** `002E1CA0` is called by bodies filed to Save_Load_Settings: SaveStorageQueue_ControllerStateHandler (`005823B0`), SaveLoad_ControllerLifecycleHandler (`00582860`) - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT and SERVICE (33 edges).** `002E1CA0`, `0035CF50`, `003C8990` are called by bodies filed to UI: `00251F40`, `00254AC0`, `00254B50`, `00279E20` (+5 more); `00279E20`, `0035D6B0`, `003C8990` reach bodies filed to UI: `00272EE0`, `00273460`, `00273A20`, `00276960` (+19 more) - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT and SERVICE (3 edges).** `00313A00` is called by bodies filed to WorldAreaField: BattleSystem_RunFieldFrameOrchestrator (`00234590`); `00313A00`, `00313DB0` reach bodies filed to WorldAreaField: FieldData_GetActiveFieldRecordBit15 (`00377C20`) - shared machinery across the layer boundary, no shared ownership.

## The `001848A0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`001848A0` (24 B) — singleton forwarder preserving `ecx`: `call
001B7F20`, then `001B82F0(singleton, ebx)` (`001848A8`/`001848B7`).

| member | role | interior |
| --- | --- | --- |
| `001B82F0` (large) | movie-container op — forwards `edx` to `0067A9B0(rcx + 0x678)` (`001B8304`/`001B830B`) | [`001B830B`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `001B7F20`, `0067A9B0`.

## SWE2-EC7-19 update (2026-05-15) — `0067A9B0` two-channel ring-cursor advance

`0067A9B0` (390 B) is the state-`1`→`3` channel teardown this page's `001B82F0` reaches (`0067A9B0(rcx+0x678)`): `[rcx+0x268] != 1` returns `al=1` immediately (`0067A9BF`); on the armed state it writes `+0x268=3`/`+0x260=1` (`0067A9C8`/`0067A9DC`) and runs the shutdown sequence — `006CC670` on `+0x150` when `+0x480` is non-null, `005CD840`+`005CD700` on `+0x508` with `+0x510=0`, the `008001B0`+`00809950` release of the `+0x288` 0xB8-byte buffer (`0067AA35`..`0067AA4E`), `006CCA70` on `+0x290`, `006CC670` on `+0xA8`, `005CD330`+`005C5230` on `+0x218` with `+0x230=0`, `0016DDD0` on `+0x2A8`, and when `+0x480` is non-null `005CD5E0` on `+0x4B8`/`+0x4D0`, `005CD330`+`005C5230` on `+0x238` with `+0x250=0`, `006CC730(+0x150,0)`, `00679F40(rcx)` (`0067AA9D`..`0067AB07`). It closes with `006CC730(rcx,0)` and `006CC730(+0xA8,1)` (`0067AB0C`..`0067AB1F`) and returns `al=1` — the seek/reset arm the movie container runs when the seek index is repositioned.

## SWE2-EC7-110 update (2026-09-20) - `001B7690` measured

`001B7690` (75 B) is the
cold-start chain `001B7F30`
and `001B8400` run:
`dword[rcx]` latches -1,
`+4`/`+9`/`+0x18`/`+0x20`
zero, `0067A9B0(rcx + 0x678)`
~~initializes~~ tears down *(corrected 2026-10-02, OPUS: state 1 to 3, `0067A9B0`+0x12..+0x18)* the trailing
sub-record, then ~~three~~ two
~~one-argument~~ invokes *(corrected 2026-10-02, OPUS: `001B7690`+0x2B `0017D960(1)` and +0x38 `002E1CA0(1, 0x15)`, then the tail `jmp` at +0x46)* -
`0017D960(1)`, `002E1CA0(1)`
(the `edx = 0x15`, `ecx = 1`
decode) - and the tail
`00229AE0(1)` completes the
ordered bring-up.
Interior anchor `001B76AA`
(the `+0x678` sub-record
offset).

Mechanical neighbours this
section's citations add:
`002E1CA0` also has an
InputGameplay caller
`00313A00` and five UI
callers (`00279E20`,
`0035CF50`, `0035D6B0`,
`003C8990` among them),
and `00313A00` in turn has
a CombatAction caller
`00313DB0` whose own
Gameplay, Movement and
Party fan-in is likewise
mechanical - caller/callee
edges, not seek-index
semantics.

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-mh-movie-seek-index-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `001D9F90` | 64 B | returns at once when `edx` is above 1 (unsigned); otherwise atomically decrements dword `+0x24 + edx*4` of `rcx` and stores, as a float at `+0x8C`, the QPC time getter's value minus the double at `02CB60E8`, plus 2.0 (`01DFCFE0`) | `001D9F93`, `001D9FA3`, `001D9FA9`, `001D9FAE`, `001D9FC2` |
| `0035CF50` | 66 B | when qword `022CA468` is zero or dword `022CA45C` is non-zero, calls `002E1CA0(8, 0)`, `002E1CA0(8, 0xB)` and `00252D90()` and zeroes dword `022CA45C`; otherwise returns without work | `0035CF5E`, `0035CF6C`, `0035CF79`, `0035CF7E`, `0035CF83` |

## Cross-subsystem neighbours of the interior rows (OPUS, 2026-10-02)

- **Platform — SERVICE (1 edge).** The countdown step `001D9F90` in the rows above calls the timer read `005CC930`, which calls `QueryPerformanceCounter` through the import slot `008C2188` (`005CC930+0x9`) and scales the count by the frequency held at `02CB6120`. The step uses it to stamp the float at `+0x8C`: the timer value less the double at `02CB60E8`, plus 2.0. Edge from `edges.tsv`; both bodies read.
