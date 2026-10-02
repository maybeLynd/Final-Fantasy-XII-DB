---
system: EBP section_011 — the SHK1 camera-shake curve bank (engine name SHKDAT)
category: 25-EBP-Script-Container
status: AUDITED
owner_layer: CodeDomain:Presentation.Camera
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
corpus_validated: "1115 / 1115 us .ebp scripts (1114 containers), 2026-09-03"
last_reviewed: 2026-09-12
ebp_units:
  - "section_011"
audit:
  passes: 1
  last_pass: 2026-09-05
  last_pass_state: "GN160 (gzf fa0db293…d2f708, snapshot b57264ba…d18fea34, exe 73461d08…d89721f8) — independent pass by repos-4b, PERFORMED 2026-09-05: own SHK1 parser over all 113 sections / 299 records, plus capstone read of 0x0037DAC0-0x0037DB20. Every corpus and instruction claim reproduced; one width refinement (+0x08 is u16, see §2)"
  last_pass_by: repos-4b
  crossref_clean: true
  reopened_count: 1
---

# EBP section_011 — the `SHK1` camera-shake curve bank

> The animation curves that make the camera lurch, rumble and tremble during a cutscene — the
> engine calls this section **`SHKDAT`**, and the file's own authors called the curves
> シェイク ("shake"), 振動 ("vibration") and 手ブレ ("handheld camera wobble").

**Corpus validation, before anything else.**

| | |
|---|---|
| files examined | **1,115 of 1,115** `us` `.ebp` scripts (1,114 real containers) |
| this unit present in | **113 (10.1 %)** |
| co-occurrence | **always with `section_010`** — 113/113, never observed alone. Also **always with `section_008` and `section_009`** (113/113), so the shake pair is a strict *subset* of the camera pair. |
| size range | **256 B – 13,184 B, median 1,472 B** |
| where | 109 under `us/event/`, 4 under `us/plan_map/`; **no other tree has one** |
| magic | `SHK1` at `+0x00` in **113 of 113** |

Every number in this sheet is measured over all 113 files that contain the section, and every
claim below says which population it holds over. Nothing here is generalised from one file.

---

## 1. What the player sees

**A cutscene where the camera shakes.** Vaan braces as the ground shudders around him; a Judge's
blade rings off stone and the view jolts; a summon lands and the picture trembles for a few
seconds before settling.

That trembling is not improvised at runtime and it is not a physics side-effect. It is
**hand-authored, per cutscene, as a named animation curve**, and this section is where those
curves live. The authors gave them plain working names in Japanese, and the shipped files still
carry them: `シェイク01` ("shake 01"), `振動02` ("vibration 02"), `手ブレ01` ("handheld wobble
01"), and descriptive ones like `振動１・地中に潜る` ("vibration 1 — burrowing into the ground")
and `剣を上げる` ("raising the sword").

**This is why only 113 scripts have one.** A shake belongs to a directed scene, so the section
appears almost entirely under `us/event/` and never in an ordinary map script that has no camera
work. And it is why the section never appears without `section_009`: **you cannot shake a camera
in a file that does not have one.** All 113 files with a shake also carry the camera pair.

The companion section [`section_010`](section-010.md) holds the *names*. This section holds the
*motion*. A cutscene asks for `シェイク01`; `section_010` turns that name into a number; this
section supplies the curve the number selects.

## 2. The layout

**All offsets are from the start of the section body** — that is, from the byte the container's
directory slot 11 points at — not from the start of the file. The engine's own arithmetic uses
this origin: at `0x0037DB00` it computes the data area as `chunkBase + dataOffset`.

### 2.1 Chunk header — 16 bytes

```struct Shk1Header base=section size=0x10
+0x00  char[4]  magic        'SHK1' - bytes 53 48 4B 31 = 0x314B4853 little-endian
+0x04  u16      recordCount  number of named shakes, 1 .. 13 observed
+0x06  u16      curveCount   number of curves in the data area, 2 .. 127 observed
+0x08  u16      dataOffset   first curve, from the chunk start, 0x70 .. 0x4F0 observed
+0x0A  u16      _unread      0 in 113 of 113; the loader's read at +0x08 is 16-bit
+0x0C  u32      _reserved0   0 in 113 of 113; no instruction in the loader reads it
```

**`+0x04` and `+0x06` are two 16-bit fields, not one 32-bit count.** The engine reads them at two
different widths at two different instructions — `cmp word ptr [rcx + 4], 0` at `0x0037DAC4` and
`movzx ebx, word ptr [rdi + 6]` at `0x0037DADD` — which is what proves the split. A corpus reading
alone could not tell this from a u32 whose high half happens to be small.

`dataOffset` is always exactly `0x10 + 0x60 * recordCount` — **113 of 113 files**. It is stored
anyway rather than computed, which matters, because the engine reads the stored value and the
reader is 16-bit (see §3).

> **Audit note, 2026-09-05 (`repos-4b`): `dataOffset` is read 16-bit, so the fence says `u16`.**
> This sheet already states in §3 that *"the reader is 16-bit"*; the §2 fence nevertheless declared
> `u32`, and the two did not agree. The loader reads it with **`movzx eax, word ptr [rdi + 8]` at
> `0x0037DAF5`** — a 16-bit load — so `+0x0A` is a separate half that nothing reads. **Measured:
> `+0x0A` is 0 in 113 of 113, so a `u32` read and a `u16` read return the same value on every
> shipped file and the corpus cannot tell them apart.** Only the instruction can. Consequence for a
> modder: a `dataOffset` above `0xFFFF` would be truncated, which caps a section at **682 records**
> (`(0xFFFF − 0x10) / 0x60`; 683 is the first count that overflows) against an observed maximum
> of 13 — **unreachable in practice, and still the wrong width to write down.**
>
> *This note first said `1092`, which is `0xFFFF / 60` — the record stride `0x60` read as decimal
> 60. Caught by another session and corrected here and in §3. **A hex stride used as a decimal in
> a one-line sanity figure**, in the same edit that corrected a width; the arithmetic in an aside
> is not exempt from being checked.*

### 2.2 Record array — `recordCount` entries, stride `0x60`, starting at `+0x10`

One entry per named shake.

```struct Shk1Record base=record size=0x60
+0x00  char[24]  name        NUL-terminated Shift-JIS, zero-padded to 24 bytes
+0x18  u32       duration    total length in frames, 10 .. 1000 observed
+0x1C  u32       _reserved0  0 in all 299 records
+0x20  u16[32]   curveId     channel table; 0 = channel unused, else a 1-based curve index
```

`0x18 + 4 + 4 + 64 = 0x60`, which is the stride exactly.

**The name field is 24 bytes and not 16**, which is easy to get wrong: 32 of the 299 names are 8
bytes and look like they sit comfortably in a 16-byte field. Eleven names are longer than 15 bytes
and one is 20, so a 16-byte field would truncate them. Two independent facts settle it — the
record stride only adds up at 24, and **the sibling `CAM7` loader for `section_009` copies its
record name with `strncpy(dst, src, 0x18)`**, a literal 24 in the instruction stream. Measured: all
299 records contain a NUL inside `name[0x18]`, and in all 299 every byte after that NUL is zero.

**`curveId` is `u16[32]` and not `u32[16]`.** Read as 32-bit the values are nonsense — one record
in `alc_z0104.ebp` yields `1507350` in a file with 54 curves. Read as 16-bit the same bytes give
`22, 23`, and the ids across the whole file run `1, 2, 3 … 54` in order with no gaps. Measured over
all 113 files: **the ids form exactly `1 … curveCount`, each used exactly once, in strict ascending
order — 113/113 on all three tests.** That is what a 16-bit read predicts and a 32-bit read cannot
produce.

All 32 channel slots are used somewhere in the corpus, at very uneven rates:

```
slot   0   1   2   3     4   5   6   7     8   9  10  11    12  13  14  15
      74  38  76  33   138  79 139  62    37  16  37  13   106  72 105  66

slot  16  17  18  19    20  21  22  23    24  25  26  27    28  29  30  31
     160  93 157  73    46  11  46   7    31  13  31  11    23  12  23  11
```

The counts pair up strikingly — `(4,6)` at 138/139, `(12,14)` at 106/105, `(16,18)` at 160/157,
`(20,22)` at 46/46, `(24,26)` and `(28,30)` at 31/31 and 23/23 — while the odd slot beside each is
used roughly half as often. **What the 32 channels individually mean is not established here**;
see §7.

### 2.3 Data area — `curveCount` curves, chained, starting at `dataOffset`

Curves are **not** an array of fixed stride and **not** an offset table. Each curve begins with its
own byte length and the next curve starts that many bytes later.

```struct Shk1CurveHeader base=record size=0x18
+0x00  i32  byteLength   distance to the next curve; always 24 + 36 * keyCount
+0x04  u32  keyCount     1 .. 85 observed
+0x08  f32  startTime    until this frame the curve returns valueBefore; non-zero in 295 of 1,839 (259 above 0.001, up to 11.6)
+0x0C  f32  valueBefore  equals the first key's segment start value in 1,839 of 1,839
+0x10  f32  duration     curve length in frames - 30.0, 40.0, 60.0, 100.0, 150.0, 200.0 ...
+0x14  f32  valueAfter   equals the curve's end value in 1,839 of 1,839; also the value when keyCount is 0
```

The header is followed immediately by `keyCount` keys of 36 bytes each, laid out below. **The key
array cannot be written inside the fence**: `check_layouts.py` admits only a literal `[N]`, and this
length is a header field. The keys are therefore fenced separately as one record, which is the
correct description anyway — the stride is fixed and only the repetition count varies.

**`byteLength == 24 + 36 * keyCount` in all 1,839 curves in the corpus.** That is the strongest
single invariant in this section, and it is what makes the chain self-describing.

Walking the chain from `dataOffset` for exactly `curveCount` steps lands, in **113 of 113 files**,
on a run of fewer than `0x40` zero bytes and nothing else — that is, exactly on the container's
alignment padding. The section has no trailing data the reader does not account for.

### 2.4 The key — 36 bytes, nine f32

Confirmed across all 5,103 keys: the stride is 36 bytes and the fields are floats.

```struct Shk1Key base=record size=0x24
+0x00  f32  _unnamed0    not identified - see section 7
+0x04  f32  _unnamed1    not identified - see section 7
+0x08  f32  _unnamed2    not identified - see section 7
+0x0C  f32  startFrame   cumulative start time in frames; 0.0 in every curve's first key
+0x10  f32  coefA        segment cubic, s^3 term (read by the evaluator)
+0x14  f32  coefB        segment cubic, s^2 term
+0x18  f32  coefC        segment cubic, s term
+0x1C  f32  coefD        segment cubic, constant: the value at the segment's start
+0x20  f32  weight       normalised segment weight; the weights of a curve's keys sum to 1.0
```

**~~Seven~~ Three of the nine are named `_unnamedN` on purpose.** *(corrected 2026-10-02, OPUS: the fence names six — `startFrame`, `coefA`–`coefD`, `weight` — and leaves three `_unnamed`, the 2026-09-26 note below)* Every byte is accounted for, so the fence
reports no gap — but an accounted byte is not an explained one, and a plausible name here would be
the label-a-gap failure the template warns against.

The last field is a **normalised segment weight**: within a curve, **the ninth float of every key
sums to 1.0**. The fourth float is the segment's **cumulative start time in frames**, and it equals
the running sum of the previous keys' weights times the curve's `+0x10` duration. Worked from
`mic_c0100.ebp`, curve 2, duration 30.0:

```
key0 weight 0.18732  ->  0.18732 * 30.0 = 5.6196  = key1 cumulative start
key1 weight 0.81268  ->  0.18732 + 0.81268 = 1.0
```

**Four of the other seven are identified by the evaluator; three are never read (2026-09-26, FABLE, Claude Opus
5.5).**
- **The evaluator.** `003CC5F0 (curve, time, out)` is what the runtime calls for every curve.
  - `keyCount` 0 returns `valueAfter`. A time at or before `startTime` returns `valueBefore`. A time at or past
    `duration` returns `valueAfter`.
  - Otherwise `u = time / duration`. It walks the keys, accumulating the ninth float until the sum passes `u`.
  - With `s` the position within that segment (`(u - start) / weight`), it returns
    `coefA·s³ + coefB·s² + coefC·s + coefD` (`003CC638`–`003CC6AE`).
- **The data agrees.** `coefD` is the value at the start of a segment, so each key's `coefD` must equal the previous
  key's `coefA + coefB + coefC + coefD`. That holds at **3,264 of 3,264** joints across the 113 unique sections.
  *Control:* random key pairs pass 318 of 3,264. The header's `valueBefore` and `valueAfter` equal the first
  segment's start value and the last segment's end value in 1,839 of 1,839 curves.
  `members/shk1_curve_check.py` prints all of these.
- **Never read.** The first three floats are not read by the evaluator, and neither is the fourth. The fourth matches
  the cumulative start frame in 4,654 of 5,103 keys, and the evaluator recomputes it from the weights instead. They
  are authoring data this runtime ignores, like the ADM offset triple.

~~**The remaining seven floats are not identified here.** They are plainly a value and its tangents —
the magnitudes are small signed quantities with matching ± pairs across successive keys, e.g.
`-6.54603 / +9.81905` in one key answered by `+6.54603 / -9.81905` in the next — but naming which
float is position, which is angle and which is a tangent needs the evaluator read, and §7 says so
rather than guessing.~~

## 3. The loader contract

**`FUN_0037da90` at `0x0037DA90` is the whole of it.** The complete body is 42 instructions and
every claim below cites the instruction that makes it true.

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| `+0x00` magic | `0x0037DA96` `cmp dword ptr [rcx], 0x314b4853` | **mismatch → the whole section is ignored** (`jne` at `0x0037DA9F` to the epilogue at `0x0037DB36`; not even the chunk pointer is stored) | — | — |
| `+0x04` recordCount | `0x0037DAC4` `cmp word ptr [rcx + 4], 0` | — | **read 16-bit only**; used solely as a non-zero gate — if zero, the `je` at `0x0037DAC9` skips all binding | — |
| `+0x06` curveCount | `0x0037DADD` `movzx ebx, word ptr [rdi + 6]` | — | **read 16-bit, zero-extended**; sizes the allocation (`lea ecx, [rbx*8]`, `0x0037DAE1`) and bounds the walk (`0x0037DB22`) | — |
| `+0x08` dataOffset | `0x0037DAF5` `movzx eax, word ptr [rdi + 8]` | — | **read 16-bit only~~ — the high half of the u32 is discarded~~.** *(corrected 2026-10-02, OPUS: `+0x08` is a `u16` and `+0x0A` its own unread `u16` — §2.1's fence, audit note of 2026-09-05)* Data must begin within 65,535 bytes of the chunk start | — |
| `+0x0C` | — | — | — | **yes — no instruction in the loader touches `[rcx+0xC]`**, and the 42-instruction body is complete |
| record array | **`Shk1_FindByName` `0x0037DB80` reads the record NAMES** during the same load sequence, called from `SHKCTL_ResolveNames` `0x003DD120` | — | — | **not inert — CORRECTED 2026-09-05.** This row previously read *"yes, at load"*. True of the loader `FUN_0037da90`, which never reads `+0x10` onward — but misleading, because a sibling function reads the names in the same sequence. **The names are load-bearing; renaming a record breaks `section_010`'s link to it.** *(Corrected 2026-09-12: `Shk1_FindByName` is reachable only behind `0x0032F3D0`, which returns 0 in the shipped build — [section-010 §3](section-010.md#3-the-loader-contract) — so renaming a record breaks nothing and `section_010`'s authored index selects it.)* Durations and the channel table remain with no reader found |
| curve `+0x00` byteLength | `0x0037DB1C` `movsxd rcx, dword ptr [rax]` | — | **read as *signed* 32-bit**, then `add rax, rcx` at `0x0037DB1F` | — |
| curve `+0x04` keyCount | — | — | — | **yes, at load.** The walk is driven by `byteLength` alone; `keyCount` is never consulted while chaining |

What the function does, in order:

1. `0x0037DA96` — compare `[chunk]` against `'SHK1'`. **The magic is genuinely validated.** This is
   worth stating plainly because the container's own `EBP2` magic is *not* found anywhere in the
   image; at section level, this one is.
2. `0x0037DAB9` — `imul rsi, rax, 0x3d0`. The bank is stored per manager slot with a **`0x3D0`-byte
   stride**, at `0x02ADD980`.
3. `0x0037DAC4` — gate on `recordCount != 0`.
4. `0x0037DAE1` / `0x0037DAE8` — allocate `curveCount * 8` bytes: a flat array of curve pointers,
   held at `0x02ADD988`.
5. `0x0037DAF5` / `0x0037DB00` — `curve = chunkBase + (u16)dataOffset`.
6. `0x0037DB10`–`0x0037DB25` — for `curveCount` iterations: store the pointer, then
   `curve += *(s32 *)curve`.

**What loading normalises: nothing.** The loader copies no field and rewrites nothing. It stores
one base pointer and builds one pointer array; the chunk is used in place thereafter.

### The three limits a modder will actually hit

- **`dataOffset` is truncated to 16 bits.** Declared ~~`u32`~~ `u16` *(corrected 2026-10-02, OPUS: §2.1's fence, audit note of 2026-09-05)* at `+0x08` in §2.1 and read
  `movzx eax, word ptr [rdi + 8]` at **`0x0037DAF5`**, then `add rax, rdi` at `0x0037DB00`. The
  largest value in the shipped corpus is `0x4F0`, so no shipped file is anywhere near the ceiling —
  but a hand-built section whose record array pushes the data past 65,535 bytes will have its data
  area read from the wrong place, silently and with no error. **That caps a section at 682 records.**
  *(Corrected 2026-09-05 from "roughly 1,092": `dataOffset = 0x10 + 0x60·recordCount` must stay
  ≤ `0xFFFF`, so the cap is `(0xFFFF − 0x10) / 0x60 = 682.49`. **1,092 is `0xFFFF / 60` — the stride
  `0x60` read as decimal 60.** The corrected figure is 62 % of the published one; neither is reachable
  by any shipped file, so nothing else in the sheet moves.)*
- **`byteLength` is signed.** A curve length with the top bit set walks the pointer *backwards*.
  Nothing bounds-checks the walk against the section end, so a wrong length reads whatever follows.
- **`recordCount == 0` disables the section completely**, even with a valid magic and a full data
  area. The `je` at `0x0037DAC9` skips the allocation entirely, and the file keeps no curves.

### Lifetime, and the resource identity

The section is not read from the file by this function — it arrives as a **streamed resource with
the engine's own tag `SHKDAT`** (the string at `0x00D109EC`). The registration lives in
`FUN_003306e0`, which pairs the tag with the completion callback `FUN_003316b0` and pending-mask
bit **`0x400`**. `FUN_003316b0` at `0x003316B0` calls this loader once the bytes have landed.

Teardown is ~~`FUN_0032ED70`~~ `FUN_0032ED80` (`ActorResource_ResetManagerLoadState`) *(corrected 2026-10-02, OPUS: `0x0032ED70` is `or qword ptr [022C6E48 + mgr*8], 1`, a pending-bit setter, `0x0032ED70+0xA`)*: at `0x0032F027` it calls the unbind `FUN_0037da70`, then frees the
chunk at `0x0032F059` and nulls the slot at `0x0032F060`.

**There are exactly five shake manager slots.** `FUN_0037da70` opens with `cmp ecx, 5` / `jge` at
`0x0037DA70`–`0x0037DA73`: a slot index of 5 or more is **silently ignored, not rejected**. The
sibling `CAM7` loader carries the same `< 5` bound.

The runtime consumer `FUN_0037d1f0` at `0x0037D1F0` indexes `slot * 0x3d0 + subSlot * 0xf0`, and
the reset loop in `FUN_003316b0` runs `subSlot` over `0..3` — so each of the five slots holds
**four concurrently playing shakes**, of `0xF0` bytes of state each. `FUN_0037d1f0` takes the shake
index as a parameter and tests it against `-1` first, which is the value `section_010` stores for a
name bound to nothing (see that sheet's §5).

**The write path: there is none.** Nothing in the executable writes a `SHK1` chunk. These are
authored offline — the toolchain extensions `shk` (`0x00D109C0`) and `cml` (`0x00D109B8`) sit in
the same string table as the tags — and the game only ever reads them.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `0x0037DA90` | `SHK1` section loader — binds the chunk and builds the curve pointer table | ✅ full body, 42 instructions |
| `0x0037DA96` | the magic compare against `0x314B4853` — **the only occurrence of those bytes in the image** | ✅ |
| `0x0037DA9F` | the `jne` that abandons the section on a magic mismatch | ✅ |
| `0x0037DAB9` | `imul rsi, rax, 0x3d0` — the per-slot stride | ✅ |
| `0x0037DAC4` | 16-bit read of `+0x04`, gate on non-zero | ✅ |
| `0x0037DADD` | 16-bit zero-extended read of `+0x06` (`curveCount`) | ✅ |
| `0x0037DAF5` | **16-bit read of the ~~32-bit~~ `u16` `+0x08`** *(corrected 2026-10-02, OPUS: §2.1's fence)* ~~— the truncation~~ | ✅ |
| `0x0037DB1C` | `movsxd` of the curve `byteLength` — the signed read | ✅ |
| `0x0037DB22` | the loop bound against `curveCount` | ✅ |
| `0x0037DA70` | unbind; carries the `cmp ecx, 5` slot bound | ✅ |
| `0x0037D1F0` | runtime shake start — `slot * 0x3d0 + subSlot * 0xf0`, `-1` = none | ✅ entry and indexing arithmetic |
| `0x003316B0` | `SHKDAT` stream-completion callback | ✅ |
| ~~`0x0033166F`~~ `0x00331715` | ~~`btr rdi, 0xb`~~ `btr rbx, 0xa` — clears pending-resource bit `0x400` *(corrected 2026-10-02, OPUS: `0x0033166F` is `test rdi, -2` in slot 10's handler, whose `btr rdi, 0xb` at `0x00331662` clears `0x800`; `FUN_003316b0` clears `0x400` at `0x00331715`)* | ✅ |
| `0x003306E0` | `atelload` registration — pairs tag, callback and mask bit | partial — the `SHKDAT` block, call sites `0x00331406` and `0x00331705`; **never runs in this build** - the whole body sits behind its first size query, a kind-`0xFF` lookup that returns -1 (`00330F7D jle 003315E7`; OPUS `a31c65871`, 2026-09-29) |
| ~~`0x0032ED70`~~ `0x0032ED80` | teardown — unbind, free, null *(corrected 2026-10-02, OPUS: `0x0032ED70` is `or qword ptr [022C6E48 + mgr*8], 1`, a pending-bit setter)* | partial — the `SHKDAT` block `0x0032F01B`–`0x0032F06A` |
| `0x02ADD980` | per-slot chunk base, stride `0x3D0` | data |
| `0x02ADD988` | per-slot curve pointer array | data |
| `0x00D109EC` | the tag string `SHKDAT` | data |

## 5. Corpus survey

**Invariants — every one measured over all 113 files, not over one.**

| | |
|---|---|
| `SHK1` magic at `+0x00` | **113 / 113** |
| `+0x0C` zero | **113 / 113** |
| `dataOffset == 0x10 + 0x60 * recordCount` | **113 / 113** |
| curve chain ends on `< 0x40` bytes of zero padding | **113 / 113** |
| `byteLength == 24 + 36 * keyCount` | **1,839 / 1,839 curves** |
| curve ids form exactly `1 … curveCount`, each once, ascending | **113 / 113** |
| record `+0x1C` zero | **299 / 299 records** |
| `name[0x18]` NUL-terminated, all bytes after the NUL zero | **299 / 299 records** |
| `recordCount` equals `section_010`'s entry count | **112 / 113** — see the outlier below |

**What varies.** 1–13 records per file (299 in total); 2–127 curves per file (1,839 in total);
1–85 keys per curve (5,103 in total). Record durations run 10–1,000 frames and cluster hard on
round values — 150 frames (32 records), 120 (27), 30 (24), 300 (17), 180 (15), 1000 (14), 60 (14)
— which is what hand-authoring at 30 fps looks like: one second, two, four, five, ten.

**Most curves are trivial.** 853 of 1,839 curves have a single key and 415 have two; only 12 have
more than eleven. The long ones are the exception, not the norm, and a reader who opens one of the
big files first will get a misleading impression of the format.

**Outliers, each worth its own line:**

- **`us/event/evt_t/evt_t0083.ebp` is the one file where the two sections disagree.** Its
  `section_010` declares four names but one carries the index `0xFFFFFFFF`. The runtime treats `-1`
  as "no shake" (`FUN_0037d1f0` tests the index against `-1` before using it), so this is **a name
  authored and deliberately left bound to nothing** — not corruption. It is the reason the
  `recordCount` match is 112/113 and not 113/113, and the reason this sheet does not claim the two
  counts always agree.
- **The largest section is 13,184 bytes**, over nine times the median.
- **Four files sit under `us/plan_map/` rather than `us/event/`** — including `mrm_b02` and
  `mrm_d02` — so a shake is not strictly a cutscene-only feature, though it is overwhelmingly one.

## 6. Falsification pass — 2026-09-03
## 6. Falsification pass — 2026-09-03

> **Independent audit, `repos-4b`, 2026-09-05 — every claim reproduced.** Own SHK1 parser over all
> **113** sections and **299** records: magic `SHK1` 113/113; `recordCount` **1–13**; `curveCount`
> **2–127**; `dataOffset == 0x10 + 0x60 × recordCount` **113/113**; `+0x0C` zero **113/113**; every
> record name has a NUL inside 24 bytes with **every byte after it zero, 299/299**; name lengths
> **4–20**; `duration` **10–1000**; record `+0x1C` zero **299/299**. The `curveId` triple test —
> the non-zero ids forming **exactly `1..curveCount`**, **each used once**, **in ascending order** —
> passes **113/113 on all three**. Loader anchors re-decoded: `cmp word ptr [rcx + 4], 0` is at
> `0x0037DAC4` and `movzx ebx, word ptr [rdi + 6]` at `0x0037DADD`, **both exactly as cited**.
>
> **What I attacked and failed to break.** (1) That `u16[32]` might be `u32[16]` — the ids-form-a-
> permutation test is the discriminator and it passes on all 113 files, which a 32-bit read cannot
> produce. (2) That the 24-byte name might be 16 — 11 names exceed 15 bytes and one is 20, so a
> 16-byte field would truncate them. (3) That `dataOffset`'s stored value might diverge from the
> computed one somewhere — it never does.
>
> **The one refinement:** the §2 fence declared `+0x08` as `u32` while §3 said the reader is 16-bit.
> Corrected to `u16` plus an unread `u16`; see the note above §2.2. **No figure moved.**

**These are attacks that were actually run, with what each returned.** Two of them changed the
reading and are recorded as changes rather than quietly fixed.

| attack | result |
|---|---|
| Is `dataOffset` relative to the file, the container payload, or the section? | **The section.** `0x0037DB00` is `add rax, rdi`, where `rdi` is the chunk pointer the loader was handed. Not inferred from the corpus — read from the instruction. |
| Is the record channel array `u32[16]` rather than `u16[32]`? | **No, and this is the one that nearly went wrong.** `u32[16]` was the first reading and it fits 42 of 113 files. It fails on `alc_z0104.ebp`, which yields id `1507350` in a 54-curve file. Under `u16[32]` all 113 files give ids `1 … curveCount`, once each, ascending. **The corpus falsified the first reading; the reading was replaced, not softened to fit.** |
| Is the record name field 16 bytes? | **No — 24.** 16 fits the common 8-byte names and truncates the 11 names longer than 15 bytes. `0x18 + 4 + 4 + 64` is the stride exactly, and the sibling `CAM7` loader copies its name with a literal `strncpy(…, 0x18)`. |
| Does the byte-length chain hold, or does it only hold on the file that was opened? | **All 1,839 curves in all 113 files**, and the walk lands on the padding every time. This began as a two-file observation and was taken to the whole corpus before being written down. |
| Is `+0x04` just the low half of a u32 count? | **It is a 16-bit field.** `cmp word ptr [rcx+4], 0` reads two bytes. The corpus cannot distinguish this; the instruction can. |
| Is `+0x0C` unused, or merely unread by the search that was run? | **Unread by a complete-body reading of the only loader.** The body is 42 instructions and none references `[rcx+0xC]`. That is stronger than a failed scan — but it is scoped to this one function, and §7 states that scope rather than claiming more. |
| Could the decompiler have invented a value the instruction stream does not have? | **Checked, and this mattered.** Ghidra's C output for this module is unreliable — `FUN_0037dc30`, `FUN_0037d7f0` and `FUN_00331610` all decompile with **empty `if` and `do` bodies**. Every address cited in §3 and §4 was therefore taken from the **disassembly**, not from the pseudocode. |
| If an external tool agrees, was it consulted before or after? | **`ff12-script` was not consulted for this section at all**, before or after. Everything here is the container census plus the loader body. The oracle is therefore still available to falsify this sheet, which is worth more than a confirmation obtained by looking first would have been. |
| Was the peer session's independent reading used as evidence? | `repos-c9` independently reported the `SHK1`/`CML1` magics and the single `.text` occurrence, matching this sheet. **Recorded as corroboration only** — every claim here rests on the loader body and the census, both re-derived in this session. |

**The killer observation for the central claim.** The claim is *"`byteLength` chains the curves and
`curveCount` bounds the walk."* It would be false if any file's chain overran its section, ended
short, or landed inside data rather than on padding. That is exactly what was tested, on all 113
files. One counterexample kills it; there are none.

> **2026-09-12:** the name resolution this note describes never runs in the shipped build — the gate `0x0032F3D0`
> returns 0 ([section-010 §3](section-010.md#3-the-loader-contract)) — so the only reader of this section's record
> names that has been found, `Shk1_FindByName`, is unreachable, and `section_010` binds by its authored index.

> **Propagated correction, 2026-09-05.** `repos-4b`'s audit of the twin
> [`section-010.md`](section-010.md) found `SHKCTL_ResolveNames` (`0x003DD120`), which ~~resolves~~ would resolve
> `section_010`'s entries by **name** *(corrected 2026-10-02, OPUS: its store never runs in the shipped build — `0x003DA27B` and `0x003DD1AB` pass kind 1 to `FUN_0032F3D0`, whose kind-1 arm ends in `0x005C5230` = `xor eax, eax; ret`, so the stores at `0x003DA28F` / `0x003DD1BF` never run; the 2026-09-12 note above)* through `Shk1_FindByName` (`0x0037DB80`) — a reader of *this*
> section's record names. §3's record-array row is corrected above. **The loader contract itself is
> unchanged**: every claim about `FUN_0037da90` was and remains a complete-body reading, and the
> `0x0037DB80` bound (`< 5`) and stride (`0x3D0`) that `repos-4b` cite match what §3 already stated
> from `FUN_0037da70`.

### Audit pass — 2026-09-05, `repos-4b` (independent; not the author)

**Every corpus claim was re-derived with an independent parser over all 113 sections and all 299
records. All of them reproduce exactly**, including the channel histogram entry for entry.

| claim under attack | re-derived |
|---|---|
| magic `SHK1` | **113 / 113** |
| `dataOffset == 0x10 + 0x60 * recordCount` | **113 / 113** |
| `+0x0C` reserved zero | **113 / 113** |
| 299 records; `recordCount` 1–13; `curveCount` 2–127; `duration` 10–1000 | **all exact** |
| name has a NUL inside 24 bytes, and every byte after it is zero | **113 / 113 on both** |
| record `+0x1C` zero in all 299 | **113 / 113** |
| `curveId` is `u16[32]`: ids are exactly `1 … curveCount`, each once, strictly ascending | **113 / 113 on all three** |
| the 32-slot usage histogram | **every one of the 32 counts matches to the entry** |

**Instruction-stream claims, re-read from the bytes:** `cmp word ptr [rcx + 4], 0` at `0x0037DAC4`
and `movzx ebx, word ptr [rdi + 6]` at `0x0037DADD` — **the two-`u16` split is proven, not inferred**,
exactly as §2.1 argues. The `je` at `0x0037DAC9` confirms `recordCount == 0` skips the allocation
outright. And `movzx eax, word ptr [rdi + 8]` at `0x0037DAF5` confirms the 16-bit `dataOffset` read.

**What broke: one number.** The 16-bit ceiling was published as "roughly 1,092 records"; it is
**682**. `1,092` is `0xFFFF / 60` — the record stride `0x60` used as decimal 60. Corrected in §3.

> **The corpus could not have caught this and neither could a gate.** The largest shipped
> `dataOffset` is `0x4F0`, so **no file exercises the limit** — it is a derived, modder-facing
> figure with nothing to check it against, and the arithmetic looked right because 60 is a
> plausible-looking stride. **A derived limit that no shipped datum can reach needs its arithmetic
> shown, which is why the correction shows it.**

**Not attacked:** what the 32 channels individually mean, and the curve-data semantics in §2.3–2.4 —
both are already declared open in §7.

## 7. What this document does not claim

- ~~**What the 32 channels individually mean.**~~ **ANSWERED (`CA-2`) by the runtime sampler, read on
  [the camera page](../../17-Presentation-Rendering/Scripted-Camera/how-a-camera-reaches-the-renderer.md) §4a
  (2026-09-19) and propagated here 2026-09-26 (FABLE, Claude Opus 5.5).** `FUN_0037D1F0` is eight sine oscillators,
  with the gameplay generator drawing a fresh random factor every frame.
  - **Slot `k` is parameter `k mod 4` of oscillator `k div 4`:** speed base, speed random range, amplitude base,
    amplitude random range.
  - **Oscillators 0–2** are the camera **eye offset** (x, y, z, in the camera's frame). **Oscillators 3–5** add to them
    to make the **look-at offset**. **Oscillator 6** is **roll** and **oscillator 7** is **field of view**.
  - So the pairs this sheet counted — `(4,6)`, `(12,14)`, `(16,18)`, `(20,22)` — are an oscillator's two base values.
    The odd slots next to them are the random ranges, which authors fill about half as often.
- ~~**Seven of the nine floats in a key.**~~ **ANSWERED (`CA-3`), §2.4:** floats five to eight are the segment cubic
  and float nine the weight, all read by `003CC5F0`. Floats one to three are never read, and neither is the fourth
  (the cumulative start frame).
- ~~**Why the odd-numbered channel slots are used about half as often as the even ones.**~~ They are the random
  ranges (see the first item); a shake with no randomness leaves them 0.
- **Whether `+0x0C` is read anywhere outside `FUN_0037da90`.** The claim is scoped to the loader.
  Nothing else was found that parses the chunk header, but "the loader does not read it" is the
  claim being made here.
- ~~**Whether the floats at curve `+0x08`, `+0x0C` and `+0x14` are always zero.**~~ **Counted 2026-09-26: they are
  not — and the sheet's "nearly every curve" was wrong.** `+0x0C` and `+0x14` are non-zero in about half the curves,
  because they are the curve's values before the start and after the end (§2.3). `+0x08` is a start time, non-zero in
  295 curves. **A field nobody counted is not an invariant**, and here it was not even nearly one.
- **What `FUN_003306e0` does with the section before the callback fires.** The registration block is
  read; the surrounding 984-instruction function is not.
- **Whether `recordCount`'s upper 16 bits are meaningful.** The loader reads only the low half. ~~No~~
  ~~shipped file has a non-zero upper half, so the corpus cannot say whether the field was ever~~
  ~~intended to be 32 bits wide.~~ *(corrected 2026-10-02, OPUS: there is no upper half — `+0x06` is `curveCount`, read on its own at `0x0037DADD` `movzx ebx, word ptr [rdi + 6]` and non-zero (2..127) in all 113 `us` sections, read through `vbf_read_entry` from `FFXII_TZA.vbf`)*

## 8. Related

- [`section-010.md`](section-010.md) — the `CML1` name directory, the other half of this strict
  pair. It turns an authored name into the index this section's records are addressed by, and it is
  the section that carries the `-1` "bound to nothing" case.
- `section-008.md` / `section-009.md` — the camera pair, `CAMCTL` / `CAMDAT`. **`section_008`
  carries the same `CML1` magic as `section_010`**: the CTL/DAT split is one design used twice. The
  `CAM7` loader at `0x002561C0` is the direct sibling of this one, and is where the 24-byte name
  field is confirmed by a literal.
- [`../README.md`](../README.md) — the `EBP2` container and the section directory this section is
  addressed through.
- `../../01-Script-VM-Native-Bridge/README.md` — the VM that runs the cutscene which asks for a
  shake by name.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings become reportable once citations written 0x... or FUN_... count (R5); tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **ActorEntity — SERVICE and CLIENT, 22 edges.**
  - Cited section handlers are called by `ActorResource_BeginManagerResourceSetLoad`, `ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources` (twice) and `ActorResource_ResetManagerLoadState`.
  - They call `ActorResource_FinalizeManagerRuntimeAfterLoads` and small actor helpers (21 to 193 bytes).
- **Presentation — SERVICE and CLIENT.** Cited functions call Presentation bodies of 170 and 498 bytes, and one (712 bytes) is called by a 285-byte Presentation body.
- **CombatAction — CLIENT.** `BattleAction_InitializeGlobalSpecialSequenceMode` calls a 16-byte function this page cites.
- **RNG_Random_Selection — SERVICE.** A 712-byte function this page cites draws from `RNG_MT19937_NextFloatClosed`.
- **CoreRuntimeScheduling — SERVICE.** The same 712-byte function calls a 27-byte core helper.
- **Resource — MECHANICAL (1 edge).** 1 call from page-cited bodies into shared Resource plumbing (`0032E400`) - the helpers' general call surface, not a Resource relationship of this page's subjects.
- **WorldAreaField — CLIENT (1 edge).** 1 inbound (WorldAreaField bodies `00378A60` call page-cited `0032F3D0`). Substantive edges include `0032F3D0` is called by `00378A60`.
