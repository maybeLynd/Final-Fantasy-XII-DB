---
system: The .sab sound bank container (and its .mab sibling)
category: 18-Audio
status: AUDITED — the container, its families and how every bank is addressed are read; the 4,097 six-digit se banks' route (the record factory's id-based path) closed 2026-09-18
owner_layer: PrimaryOwner:Audio
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 5 cited function entries, 0 of them among the 109 records that changed GN160 -> GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0), established for this document 2026-09-14 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
corpus_validated: "4,609 / 4,609 .sab and 116 / 116 .mab, every header read from FFXII_TZA.vbf 2026-09-04"
last_reviewed: 2026-09-12
archive_formats:
  - "sab"
  - "mab"
audit:
  passes: 1
  last_pass: 2026-09-05
  last_pass_state: GN160-corpus-and-code-reparse-repos-1e — 4,725 files re-parsed from the VBF and all three cited functions re-decoded; 14/14 corpus figures and every instruction anchor confirmed, 1 branch-vs-read anchor corrected
  crossref_clean: false        # 2026-09-30 (SWE2-DATA): false until the pass-22 UNACCOUNTED NEIGHBOUR findings are accounted (FRONTIER-REQ-SWE2-DATA-PASS22-DEBT; OPUS-REQ-DATA-PASS30-CROSSREF-CLEAN-0930)
  reopened_count: 0
---

# `.sab` — the sound bank container, and `.mab`, its sibling

> Every sound effect in the game arrives in one of these. A four-byte tag, a short header, and a
> directory of exactly four chunks — **the same four in all 4,609 files**. `.mab` is the same
> container with three chunks and holds the music.

**Corpus validation, before anything else.**

| | |
|---|---|
| files examined | **4,609 `.sab` and 116 `.mab`** — every one in the archive, header read directly from the VBF |
| `.sab` lives in | `ps2data/sound/se` (4,345) and `ps2data/sound/shout` (264) — nowhere else |
| `.sab` size | 838 MB total, **mean 182 KB** |
| `.mab` size | 1,312 MB total, **mean 11 MB** — two orders of magnitude apart, in the same directory |
| chunk arity | **`.sab` always 4, `.mab` always 3** — one distinct chunk sequence each, across the whole corpus |

Every claim below was checked over **all 4,609 `.sab` and all 116 `.mab`**, not over a sample.

---

## 1. What the player sees

**This is where sound effects live.** A sword hitting a Wolf, the Save Crystal's chime, a Mist
Charge igniting, the menu blip when you move the cursor — each of those is one entry inside one of
these banks. The engine does not ship loose sound files; it ships **banks**, and a bank is a named
group of related sounds that load and unload together.

The split visible in the filenames is the split the game actually uses: **`se`** banks (4,345 of
them) are the general effect banks, and **`shout`** banks (264) are the battle voice clips — Vaan's
"Take that!", the quickening calls. `.mab` files are the music, and they are roughly sixty times
larger apiece, which is what you would expect of streamed music against short effect samples.

**One player-visible fact falls straight out of the file list:** the archive ships **132 sound banks
this build can never play**. They are the PlayStation 4 versions of the battle-voice banks, left in
the PC archive beside the Windows ones. See §5.


## `AS-2` answered — the banks name their own battle events (FABLE, 2026-09-22)

§1 calls the `shout` banks *“the battle voice clips”*, and the register carried `AS-2` as still open
on the narrow point: **battle voice specifically, or all character speech?** The banks answer it
themselves — **every sample inside them is named for a battle event.**

`shout00.win.sab` opens `sabf` / `shout00` / `snd ` / `seq ` / `trk ` / `mtrl`, and the `mtrl` chunk
is followed by the sample names in order:

```
us:  veVN_01at  veVN_02at  veVN_03at  veVN_04dm  veVN_05dm  veVN_06dm
     veVN_07crt veVN_08crt veVN_09dead veVN_10dead
jp:  vjVN_01at  vjVN_02at  vjVN_03at  vjVN_04dm  vjVN_05dm  vjVN_06dm
     vjVN_07crt vjVN_08crt vjVN_09dead vjVN_10dead
```

`ve` is the English voice, `vj` the Japanese; `VN` is the actor. **The suffixes are the events:**
`at` attack, `dm` damage, `crt` critical, `dead` death.

### The layout is identical across all 132 banks (FABLE, 2026-09-22)

**Censused over every bank in both languages, with the `sabf` magic as the control — 66 of 66 parsed
per language, 0 rejected:**

| | `us` | `jp` |
|---|--:|--:|
| banks parsed / rejected | **66 / 0** | **66 / 0** |
| distinct actor codes (one per bank) | **66** | **66** |
| samples suffixed `at` | 198 | 198 |
| samples suffixed `dm` | 198 | 198 |
| samples suffixed `crt` | 130 *(+2 `ctr`)* | 130 *(+2 `ctr`)* |
| samples suffixed `dead` | 132 | 132 |
| **classified samples** | **660** | **660** |

**660 = 10 × 66, and the histogram divides exactly: 198 = 3×66, 132 = 2×66.** So **every one of the
66 actors has precisely three attack lines, three damage lines, two critical lines and two death
lines** — ten, no more and no fewer, in both languages.

> **The two localisations are the same manifest.** The counts match column for column, and so does
> the defect: `crt` is misspelt **`ctr` in exactly two places in each language**. Two independently
> recorded voice sets do not reproduce one another's typo — they were generated from one list, and
> only the prefix (`ve`/`vj`) and the audio differ.

### What settles `AS-2`, stated exactly (FABLE, 2026-09-22)

**These banks contain battle voice and nothing else.** A bank of *all character speech* would carry
story lines, and the sample names would not be a four-event grid repeated 66 times. The size
corroborates it: the whole `us` set is **4.9 MB across 66 banks**, min 58 KB, mean 76 KB, max 98 KB
— a tight band with no outliers, which is what a fixed per-actor bark set looks like and what
scene-length dialogue never does. **For scale, `ps2data/sound` totals 1,312 MB of music and 822 MB
of effects against 17 MB of `shout`.**

### Two corrections to §1 (FABLE, 2026-09-22)

1. **No sample is named for a Quickening.** §1 illustrates the banks with *“Vaan's ‘Take that!’, the
   quickening calls”*. The first half is right — `shout00` is `VN` and its lines are attack and
   damage. But across all 132 banks the only suffixes are `at`, `dm`, `crt`, `dead`; **nothing is
   named for a Quickening.** Where those calls live is **not established here.**
2. **Nine `us` banks carry an eleventh sample** on a different pattern, `vefah_01<ACTOR>`
   (`shout18`, `22`, `24`–`30`), and **`shout62` carries `vjD032` — a `vj`-prefixed name inside a
   `us` bank**, a shipping slip of the same kind as the `ctr` typo. What `fah` denotes is **not
   established.**

> **Scope.** This is the shipped `.sab` corpus read statically — chunk tags and sample names, not
> decoded audio. It establishes what the `shout` banks *contain* and therefore what
> `ShoutAudioBank` loads. It does **not** claim the game has no speech elsewhere: cutscene dialogue
> is not in this tree, and this says nothing about where it is. **NATIVE/STATIC — shipped-asset
> evidence, not live.**

## 2. The layout

Offsets are from the start of the file.

```struct SabHeader base=file size=0x10
+0x00  char[4]  magic        'sabf' (.sab) or 'mabf' (.mab) -- 4609/4609 and 116/116
+0x04  u8       version      2 in every shipped file; the loader branches on this
+0x05  u8       _flag        1 in 4,097 .sab and 0 in 512; 1 in all .mab
+0x06  u16      dirDelta     0x10 in every shipped file -- added to the aligned name end
+0x08  u8       chunkCount   4 in every .sab, 3 in every .mab
+0x09  u8       nameLength   strlen of the name at +0x10 -- 5 or 7
+0x0A  u16      _param       350 distinct values in .sab; always 0x2710 in .mab
+0x0C  u32      totalSize    == the file's own byte length, 4609/4609 and 116/116
```

The bank name follows at `+0x10`: **`nameLength` ASCII bytes then a NUL**, verified in every file.
It is *not* a fixed-width field — see §3, where the loader computes the directory position from it.

Then the chunk directory, `chunkCount` records of 16 bytes:

```struct SabChunkRecord base=record size=0x10
+0x00  char[4]  tag       'snd ' 'seq ' 'trk ' 'mtrl' (.sab) / 'musc' 'inst' 'mtrl' (.mab)
+0x04  u32      flags     0x00100000 in all 18,436 .sab and 348 .mab chunk records
+0x08  u32      offset    payload offset, RELATIVE TO THE FILE START
+0x0C  u32      _pad      0 in all 18,784 chunk records
```

**`offset` is file-relative**, and that is read off the instruction that uses it, not inferred: the
consumer at `0x007D05A9` computes `chunk->offset + container->base`.

## 3. The loader contract

**`Sab_IsSabf` — `0x007CFF90`, 20 bytes; this is the entire function.**

```
Sab_IsSabf(void* blob) -> bool
  0x007CFF90  test rcx, rcx
  0x007CFF93  jne  0x7CFF98
  0x007CFF95  xor  al, al           ; NULL -> false
  0x007CFF97  ret
  0x007CFF98  mov  eax, [rcx]
  0x007CFF9A  cmp  eax, [rip+0x541614]   ; -> g_sabfTag @ 0x00D115B4
  0x007CFFA0  sete al
  0x007CFFA3  ret
```

**The magic is validated, and a byte scan of `.text` cannot see it.** The tag is not an immediate —
it is a four-byte constant in `.rdata` at `0x00D115B4`, compared through a memory operand. Searching
`.text` for the bytes `sabf` returns **zero hits**, and concluding "the magic is never checked" from
that would have been wrong. `Mab_IsMabf` (`0x007D07A0`) is byte-for-byte the same shape against
`0x01CB6FB8`. See §6.

**`Sab_FindChunk` — `0x007CF6B0`, 129 bytes; the whole directory contract.**

```
Sab_FindChunk(container, out, const u32* wantTag)
  r9 = container->blob                              0x007CF6B0
  if (blob[0x04] < 2)                               0x007CF6B7   <- VERSION GATE
        dir = blob + u16@[blob+0x06]                0x007CF6D9   <- legacy layout
  else  dir = blob + ((0x10 + blob[0x09]) & 0xF0)              0x007CF6C3..0x007CF6D1
                    + u16@[blob+0x06]               0x007CF6D4
  n = blob[0x08]                                    0x007CF6DC   <- chunkCount
  for (i = 0; i < n; i++)                           0x007CF6E3, 0x007CF704
      rec = dir + (i << 4)                          0x007CF6F3   <- 16-byte stride
      if (*(u32*)rec == *wantTag) -> found          0x007CF6FD, 0x007CF700
  not found: out->ptr = 0                           0x007CF710
  found:     out->ptr = rec                         0x007CF726
```

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| `+0x00` magic | `Sab_IsSabf` **`0x007CFF9A`** | **mismatch → `false`**; NULL → `false` | — | — |
| `+0x04` version | `Sab_FindChunk` **`0x007CF6B7`** | — | — | — |
| `+0x05` `_flag` | — | — | — | **yes — no reader in either function read here** |
| `+0x06` `dirDelta` | `Sab_FindChunk` **`0x007CF6BC`** (read) and **`0x007CF6D4`** (added to the base) | — | — | — |
| `+0x08` `chunkCount` | `Sab_FindChunk` **`0x007CF6DC`** | — | — | — |
| `+0x09` `nameLength` | `Sab_FindChunk` **`0x007CF6C3`** | — | **rounded DOWN to a multiple of 16** | — |
| `+0x0A` `_param` | **`007EE01D`** (read as a `word`; see below) | — | — | ~~**yes — no reader found in the functions read; not a scan result**~~ — **a reader is now identified**, and the old cell was *correctly scoped*: it reported the functions that had been read, not a failed sweep |
| `+0x0C` `totalSize` | — | — | — | **yes — no reader found in the functions read**, and it equals the file length in 4,725 of 4,725 |

> **`+0x0A` has a native consumer, and it can cancel a spatial axis — 2026-09-21 (FABLE, consuming
> `ASTRA-NOTICE-FABLE-PAN-BANK-HEADER-IDENTITY` and `-PAN-CALLER-ADDENDUM`).** The voice caller
> `007EDE90` reads this word and, **when it equals 1**, replaces the incoming front/back value with
> zero before the mixer: `007EE01D movzx ebx, word ptr [rcx+0xA]` / `007EE02B cmp bx, 1` /
> `007EE031 movaps xmm9, xmm8`, and both mixer call sites (`007EE0C6`, `007EE17A`) then pass that
> register. *With `frpan` zero the mixer's tested mono case returns exactly `(0.5, 0.5)`*
> ([the voice page](../Audio-Boundary/how-a-sound-request-becomes-a-voice.md), `UQ-242`).
>
> **That the word is this header's `+0x0A` is established by a checked chain, not by its
> displacement.** `007BD8D0` resolves `owner+0x20` through `007B2470`; for an object whose primary
> vtable is `01CB83F8` — original RTTI `.?AVOnMemoryBank@Driver@Sd@SQEX@@`, locator at zero subobject
> offset with a matching self RVA — slot 7 is `007E2A70`, which wraps **bank `+0x50`** in a wrapper
> whose vtable `01CB6E30` is RTTI `AudioBinaryFile` and whose `+8` is that payload. So `007EE019`
> reads the bank's payload, not a wrapper field mistaken for file data.
>
> **What this does not say.** ~~Which shipped banks carry value 1~~, why the field takes its other
> values, and whether any particular cue or scene takes the branch are **not** established — and the
> other values must not be called inert, because only the equality test against 1 is settled. The
> corpus figures this page already reports (350 distinct SAB values, `0x2710` for MAB) are unchanged
> and were not re-run.
>
> ***Two shipped banks do carry it — 2026-09-21 (FABLE, consuming `ASTRA-NOTICE-FABLE-SAB-AUTHORED-OVERRIDE`).***
> From the designated reference VBF, under `ps2data/sound/se/sead_data_win/`:
>
> | entry | embedded bank name | `+0x0A` | declared logical bytes |
> |---|---|---:|---:|
> | `se001/se001001.win.sab` | `se001` | **1** | 469,552 |
> | `se001/se001002.win.sab` | `se001` | **1** | 349,232 |
> | `se000/se000.win.sab` | `se000` | 0 | 9,434,608 |
>
> The first positive's complete 16-byte header is
> `73 61 62 66 02 01 10 00 04 05 01 00 30 2A 07 00`, and **it checks against the table above field by
> field** — `sabf`, version 2, flag `01`, `dirDelta` `0x0010`, `chunkCount` 4, `nameLength` 5,
> `+0x0A` = `0x0001`, and `totalSize` `0x00072A30` = **469,552**, which is the declared size. *The
> field is identified by the whole layout agreeing, not by its displacement.*
>
> **So the consumer is not dead in this build** — but **two named entries are not a census**, and none
> was run: how many banks carry 1, and whether these two are ever the bank a voice is playing from,
> are still open. The evidence is first-block format controls over retained index records and decoded
> blocks, not a whole-payload validity claim.
| chunk `+0x04` flags | — | — | — | **yes — constant `0x00100000` in all 18,784 records, and neither function reads it** |
| chunk `+0x08` offset | consumer **`0x007D05A5`** | — | — | — |

> ### The directory is not at a fixed offset — it is computed from the name length
>
> `dir = blob + ((0x10 + nameLength) & 0xF0) + dirDelta`
>
> **Every shipped file lands on `0x20`**, because `nameLength` is 5 or 7 and `dirDelta` is `0x10`:
> `(0x10 + 5) & 0xF0 = 0x10`, plus `0x10`, is `0x20`. A corpus reading alone would conclude the
> directory is simply at `+0x20` and be wrong about the format. **A bank name of 16 characters or
> more moves the directory**, and the `& 0xF0` rounds *down*, so a 16-byte name gives `0x20 + 0x10`
> — the name would collide with the directory unless `dirDelta` grew too.
>
> Verified: recomputing the base with this formula and walking `chunkCount` records from it produces
> a clean directory — printable tags, in-range offsets — in **4,609 of 4,609 `.sab` and 116 of 116
> `.mab`**.

**The version gate has a live legacy branch that nothing in this build takes.** `blob[0x04]` is
**2 in every one of the 4,725 files**, so the `< 2` path at `0x007CF6D9` — which skips the name
alignment entirely and puts the directory at `blob + dirDelta` — is **real code, dead against this
corpus**. It is the PS2-era layout, kept.

**A missing chunk is a supported outcome, not a failure.** The scan falls out of the loop and writes
a null result descriptor at `0x007CF710`; callers get a valid object with a null payload pointer
rather than an error. Nothing checks the tag against a whitelist, so a bank with different tags
parses fine and simply never matches.

**No bounds check relates `chunkCount` to `totalSize`.** The loop trusts `blob[0x08]` and the
directory base; a file claiming more chunks than it holds walks off the end. Neither function
compares an offset against `+0x0C`.

**The write path.** None found. Nothing in the executable emits `sabf`; the banks are authored
offline.

### How a bank is named, and the platform infix

**The PC build addresses these files by a platform-infixed name.** `.win.sab` occurs **129 times**
in the executable and **every one of the 129 full `.sab` path strings carries the infix** — e.g.
`PS2Data\sound\shout\us\shout00\shout00.win.sab`. `.win.` in general occurs 131 times, covering
`.win.mab` and `.win.config` as well.

**`.orb` occurs zero times in the executable** — not as `.orb`, not as `.orb.`, in any section. The
132 `.orb.sab` files in the archive (§5) are addressed by nothing.

**Only the 264 `shout` banks are named by literal path.** The 4,345 `se` banks are not: no full path
string for them exists in the image. They are reached through the resource-kind path table
([kind 33](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/area-nmb-index.md#3-the-loader-contract)),
whose array begins `shout00.win.sab`, `shout01.win.sab`, `shout02.win.sab` — **so the table covers
the shout banks, and how the `se` banks are addressed is not established here.** → `PROPOSED-repos-4b-12`
*(Partly answered 2026-09-12, FABLE: the **248** single-name banks `sead_data_win/se<n>/se<n>.win.sab` are
opened by `SebAudioBank` from the format `"%s/se%03d/se%03d%s"` (`00908A38`, `00223CB1`–`00223CD5`) with the id
of a loaded [`.seb` block](seb-se-block-index.md); the other 4,097 `se` banks are not reached by that route.)*
***Completed 2026-09-18 (FABLE): the other 4,097 open through the bank record factory `00222DC0` (its one caller `0021A040`), and the archive agrees name for name.*** The factory takes the bank id in `edx` and the five-character bank tag in `r9`, and builds the path with `%s/se%03d/se%06d%s` (`009089A8`): the first `%s` is the directory global `[01E027E0]`, initialised in `.data` to the string `PS2Data/sound/se/sead_data_win` (`00908950`); the first number is the id divided by 1,000 (the `0x10624DD3` multiply and `sar 6` at `00222E26`..`00222E33`); the second is the id itself, six digits (`00222E6D`..`00222E97`, with `.win.sab` from `00908998` as the last argument). The archive holds 4,345 files under `sead_data_win`: 248 with three-digit names, one per block directory, which the block reader opens with the three-digit format above, and 4,097 with six-digit names, every one in the directory of its own first three digits (`se001/se001001.win.sab` and so on, zero exceptions), which is exactly what the factory's format produces. So a se bank is addressed by its id alone: block `id / 1000`, file `id`.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `0x007CF6B0` | `Sab_FindChunk` — version gate `0x007CF6B7`, name-derived base `0x007CF6C3`–`0x007CF6D1`, legacy base `0x007CF6D9`, count `0x007CF6DC`, 16-byte stride `0x007CF6F3`, tag compare `0x007CF6FD`, miss `0x007CF710`, hit `0x007CF726` | ✅ full body |
| `0x007CFF90` | `Sab_IsSabf` — null guard `0x007CFF93`, magic compare `0x007CFF9A`, boolean result `0x007CFFA0` | ✅ full body |
| `0x007D07A0` | `Mab_IsMabf` — the same 20 bytes against `0x01CB6FB8` | ✅ full body |
| `0x007D0580` | a `musc` chunk accessor — tag `0x007D058D`, find `0x007D059C`, offset load `0x007D05A5`, **rebase onto the container `0x007D05A9`** | ✅ full body |
| `0x007D0210` | the `inst` accessor, same shape, tag at `0x007D021D` | ✅ full body |
| `0x00D115B4` | `g_sabfTag` — the `sabf` constant the magic test compares against | — |
| `0x01CB6FB8` | `g_mabfTag`, immediately followed by the `musc` and `inst` tag constants | — |

## 5. Corpus survey

**Invariants — every one checked over all 4,609 `.sab` and all 116 `.mab`.**

| | `.sab` | `.mab` |
|---|---|---|
| magic | `sabf` **4609 / 4609** | `mabf` **116 / 116** |
| `+0x04` version | `2` **4609 / 4609** | `2` **116 / 116** |
| `+0x06` dirDelta | `0x10` **4609 / 4609** | `0x10` **116 / 116** |
| `+0x08` chunkCount | `4` **4609 / 4609** | `3` **116 / 116** |
| `+0x0C` == file length | **4609 / 4609** | **116 / 116** |
| name ASCII + NUL at `+0x10+nameLength` | **4609 / 4609** | **116 / 116** |
| chunk `flags` == `0x00100000` | **18,436 / 18,436** | **348 / 348** |
| chunk `_pad` == 0 | **18,436 / 18,436** | **348 / 348** |
| chunk offsets ascending | **4609 / 4609** | **116 / 116** |
| first chunk offset == directory end | **4609 / 4609** | **116 / 116** |
| computed directory base | `0x20` **4609 / 4609** | `0x20` **116 / 116** |

**One chunk sequence each, with no exceptions.** Every `.sab` is `snd ` `seq ` `trk ` `mtrl`, in
that order — **one distinct sequence across 4,609 files**. Every `.mab` is `musc` `inst` `mtrl` —
one sequence across 116. This is a fixed schema, not a variable container, and it is the same shape
as the `.ard`'s "exactly four `st2e` tables in 166 of 166".

**What varies.** `nameLength` is 5 (4,345 — the `se` banks, names like `se000`) or 7 (264 — the
`shout` banks, `shout00`). `+0x05` is 1 in 4,097 and 0 in 512. `+0x0A` takes 350 distinct values *(267 `se` folder ordinals plus 83 `shout` values, one per folder - census 2026-10-01, OPUS, `../../_index/candidates/opus-sab-param-census-1001/`)* in
`.sab` and is **constant `0x2710` = 10,000 in all 116 `.mab`** — a round decimal constant, which
usually means a rate or a scale, and is not decided here.

**The bank name is not the file name.** `se001001.win.sab` and `se001002.win.sab` both carry the
name `se001`. The filename stem starts with the name field in **4,609 of 4,609**, but many files
share one bank name.

### 132 files this build cannot reach

**`.sab` splits into 4,477 `.win.sab` and 132 `.orb.sab`** — `orb` for Orbis, Sony's platform name
for the PlayStation 4. The 132 are **66 under `sound/shout/us` and 66 under `sound/shout/jp`**, and
**every one of the 132 has a `.win.` sibling with the same stem** — 132 of 132.

Against that, the executable names `.win.` 131 times and **`.orb` not once**. So these are the PS4
battle-voice banks shipped in the PC archive and addressed by nothing in the PC binary. **A modder
editing `shout12.orb.sab` would hear no change**, and finding that out by experiment costs an
evening.

> **This sharpens the folder README's claim rather than repeating it.** The README says *"the
> remaster substitutes Windows audio assets by filename convention"*. True — but the convention is
> not universal across the corpus: **97.1 % of `.sab` carry `.win.`, and the remaining 2.9 % are a
> different platform's copies left in place**, not files the convention missed.

## 6. Falsification pass — 2026-09-04

| attack | result |
|---|---|
| **Is the magic checked at all?** | **Yes — and the scan that says "no" is the trap.** Searching `.text` for the bytes `sabf` returns **zero hits**, the same result that is genuinely true for `EBP2` and `CML1`. But the tag is a `.rdata` constant at `0x00D115B4` compared through a memory operand at `0x007CFF9A`, so no immediate ever appears in code. **A `.text` byte scan cannot distinguish "never validated" from "validated against a constant in memory."** The xref that found it was on the *constant*, not on the code. |
| Is the directory really at `+0x20`, or does it just land there? | **It lands there.** The loader computes `((0x10 + nameLength) & 0xF0) + dirDelta`, and with the only two shipped name lengths that is always `0x20`. **The corpus cannot tell these apart; the instruction at `0x007CF6C3` can.** |
| Is `chunkCount` real, or did a walk heuristic get lucky? | **Real, and this was checked deliberately.** My first pass walked the directory until a non-printable tag — a heuristic that had already produced a wrong answer for me on the resource path tables the day before. Re-tested: `blob[0x08]` equals the walked count **and the record after the last one is not a chunk**, in 4,609 of 4,609 and 116 of 116. The count is authoritative and the heuristic merely agreed. |
| Is `offset` relative to the file, the directory, or the chunk? | **The file.** `0x007D05A9` adds it to the container base, and independently the first chunk's offset equals the directory end in every file. Two routes, same answer. |
| Are `.sab` and `.mab` really one format? | **Same container, different schema.** Identical header field-for-field, identical 16-byte chunk record with the same constant `flags`, identical directory formula — verified separately over both corpora — but a fixed and *different* chunk set and arity. Documented as one container with two schemas rather than two formats or one. |
| Did an external tool supply any of this? | **No tool was consulted.** No oracle reads `.sab`; every claim is anchored to an instruction or to a 4,609- or 116-file count. |

**What was tried and failed to break it.** The obvious alternative for `+0x0C` is that it is not a
size but an offset to something. It equals the file's own length in **4,725 of 4,725 files**, which
no offset-to-a-member would do. It is nonetheless listed as **`Inert`** in §3 — because *nothing
read here reads it*. **A field that is perfectly self-consistent and unread is exactly the case the
`Inert` column exists for**, and the two facts are not in tension.

## 6b. Independent audit pass — 2026-09-05, `repos-1e`

**Method.** All 4,725 files re-parsed from `FFXII_TZA.vbf` with a fresh block-0 reader, and all three
cited functions re-decoded with capstone against `functions.tsv` bounds. Program state: GN160
(`gzf fa0db293…`).

**Every corpus figure reproduces exactly — all fourteen.**

| claim | sheet | re-parse |
|---|---|---|
| files | 4,609 `.sab` + 116 `.mab` | **identical** |
| magic | `sabf` 4,609 / 4,609, `mabf` 116 / 116 | **identical** |
| `+0x04` version | 2 | **2 in all 4,725** |
| `+0x05` `_flag` | 1 in 4,097 `.sab`, 0 in 512; 1 in all `.mab` | **4,097 / 512 / 116 — exact** |
| `+0x06` `dirDelta` | `0x10` | **`0x10` in all 4,725** |
| `+0x08` `chunkCount` | 4 in every `.sab`, 3 in every `.mab` | **4 × 4,609, 3 × 116 — exact** |
| `+0x09` `nameLength` | 5 or 7 | **5 × 4,461, 7 × 264 — no other value** |
| `+0x0A` `_param` | 350 distinct in `.sab`; always `0x2710` in `.mab` | **350 distinct; `0x2710` in all 116** |
| `+0x0C` `totalSize` = file length | 4,725 / 4,725 | **4,725 / 4,725** |
| computed directory base | `0x20` in all | **`0x20` in all 4,725** |
| chunk records | 18,436 `.sab` + 348 `.mab` | **18,436 + 348** |
| chunk `+0x04` flags | `0x00100000` in all | **`0x00100000` in all 18,784** |
| `.sab` location split | `se` 4,345 / `shout` 264 | **identical** |
| sizes | `.sab` 838 MB, `.mab` 1,312 MB | **838 MB / 1,312 MB** |

**`Sab_IsSabf` is byte-for-byte as printed** — every one of the eight instructions and all eight
addresses. The `rip`-relative target resolves as claimed: `0x007CFFA0 + 0x541614 = 0x00D115B4`, and
the four bytes there are literally `sabf`. `Mab_IsMabf` is the same shape against `0x01CB6FB8`,
which holds `mabf`. **The sheet's headline instrument claim survives its own strongest test.**

**`Sab_FindChunk`'s every cited address is exact**, including the arithmetic the sheet builds its best
point on: `0x007CF6C3` `movzx eax, byte ptr [r9+9]` → `0x007CF6C8 add rax,0x10` →
`0x007CF6CC and eax,0xf0` → `0x007CF6D1 add rax,r9` → `0x007CF6D4 add r10,rax`. **The directory base
really is computed, not fixed**, and the corpus really does land on `0x20` for every file — so §3's
"a corpus reading alone would conclude the directory is at `+0x20` and be wrong about the format" is
demonstrated rather than asserted.

**One defect found and corrected: a field-table anchor pointed at a branch, not a read.** `+0x06
`dirDelta`` cited `0x007CF6C1`, which is `jb 0x7cf6d9` — the version-gate branch. The read of
`[r9+6]` is at **`0x007CF6BC`** (`movzx r10d, word ptr [r9+6]`), which happens *before* the branch,
so both arms use it. Corrected in §3 with the add site kept alongside.

**One apparent inconsistency that is not one.** §2 cites `0x007D05A9` for the offset consumer and
§3's table cites `0x007D05A5`. Both are right and they name different halves of one expression:
`0x007D05A5 mov eax, [r8+8]` reads `chunk->offset`, `0x007D05A9 add rax, [rbx+8]` adds
`container->base`. **Recorded so the next reader does not "fix" one of them.**

**What was attacked and held.** (a) That `.mab` might not really differ in arity — it does, 3 against
4, with no exceptions in 4,725 files. (b) That `chunkCount` might be a byte read wider than a byte —
it is `movzx r8d, byte ptr [r9+8]`, so values above 255 are unrepresentable. (c) That the
`0x00100000` flag might vary somewhere in 18,784 records — it does not. (d) That the directory-base
arithmetic might be a decompiler artefact — it is five consecutive instructions read from the bytes.

**Not audited:** what the four chunk tags *mean*, which §7 already declines to claim.

## 7. What this document does not claim

- **Nothing about chunk contents.** `snd `, `seq `, `trk `, `mtrl`, `musc` and `inst` are located,
  bounded and named; none is parsed. The obvious reading — samples, sequences, tracks, materials —
  is **not** established, and the tags are not evidence for it. → `PROPOSED-repos-4b-10`
- ~~**`+0x05` and `+0x0A` are undecided.** `+0x05` is a 0/1 split of 512 against 4,097; `+0x0A` is
  constant `10000` in `.mab` and takes 350 values in `.sab`. Neither is read by the two functions
  read here, so both are `Inert` **with respect to those functions only**, not proven unread by the
  program. → `PROPOSED-repos-4b-11`~~ *(Superseded, struck 2026-10-01, OPUS: §3 (2026-09-21) finds the reader `007EE01D movzx ebx, word [rcx+0xA]` / `007EE02B cmp bx, 1`, which zeroes `frpan` when `+0x0A` is 1, and the map sound list page (2026-09-27) gives `+0x0A` as a per-folder ordinal 0-267 and `+0x05` as the block / per-sound split. Whether the 350 distinct values in all `.sab` files agree with ~~268~~ 267 `se` folders plus the `shout` banks ~~is not re-counted here~~ is re-counted 2026-10-01 (OPUS): they do - 267 `se` ordinals (0-267, slot 3 unused) plus 83 `shout` values (`5172`-`5256`) make the 350, one value per folder; census `../../_index/candidates/opus-sab-param-census-1001/`.)*
- ~~**How the 4,345 `se` banks are addressed is not established.** Their paths are not in the binary,
  and path-table kind 33 begins with `shout` entries. → `PROPOSED-repos-4b-12`~~ *(Superseded: answered in §3 (2026-09-18) - the 248 block banks open through `%s/se%03d/se%03d%s`, the other 4,097 through the factory `00222DC0` with `%s/se%03d/se%06d%s`. Struck 2026-10-01, OPUS.)*
- **The callers of `Sab_FindChunk` were not audited**, so "no bounds check relates `chunkCount` to
  `totalSize`" is a property of that function and **not** a claim that a malformed bank can be made
  to fault.
- **`.seb`, `.spp` and `.config` are not covered** *(`.seb` is now: [the SE block index](seb-se-block-index.md), 2026-09-12)*, though `.seb`'s `SeBl` magic and its
  `0xFFFFFFFF`-sparse offset table were observed in passing and are recorded in the inbox for
  whoever takes them.
- **The `< 2` legacy branch is described, not exercised.** No file in the corpus takes it, so what
  a version-1 bank looks like is inferred from the arithmetic alone.

## 8. Related

- [`Sound-Bank-And-Voice-Formats/README.md`](README.md) — the folder's format plan, which named
  `.sab` as the first sheet to write.
- [`sqex-sd-sound-driver-architecture.md`](../sqex-sd-sound-driver-architecture.md) — the driver
  that consumes these banks.
- [`how-a-sound-request-becomes-a-voice.md`](../Audio-Boundary/how-a-sound-request-becomes-a-voice.md)
  — the engine side of playback.
- [`area-nmb-index.md`](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/area-nmb-index.md)
  — the resource-kind path table, whose kind 33 array holds the `shout` bank paths.

## SWE2-EC7-109 update (2026-09-20) - `001FB470` measured

`001FB470` (332 B) is the EASTL
rbtree insert-with-hint
`001A2E50`, `001FB770` and
`00223AD0` call: the hint node
`qword[r8]` is validated against
head/sentinel, `0016D6D0` finds
the successor, both orderings
around `dword[node + 0x20]` are
compared against `dword[r9]`,
a 0x30 node comes out of the
`qword[rcx + 0x30]` allocator's
`vtable[+0x10]` slot, the
0x10-byte payload is `movups`
copied, `0016D840` links and
rebalances, `dword[rcx + 0x28]`
counts the insert, and the
`001FB5C0` / `00223790` paths
cover the leftmost and generic
cases.
Interior anchor `001FB4A5` (the
`0016D6D0` successor call).

Mechanical neighbours introduced by
this section's citations: `0016D6D0`
(the rbtree successor the insert
calls) carries Presentation caller
fan-in (7 edges). Those are edges
of the container primitive, not of
the SAB format - noted so the audit
accounts for them.

`00223790` (344 B) is the ordered find `001FB470` calls: `rcx + 8` tree root with `[rcx + 0x18]` head, `r9d = [r8]` key compared against `[rax + 0x20]` walking left/right by `setl`, then `0016D720`/`0016D840` finish - the bank's key lookup.

Interior anchor `00223803` (function `00223790`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-EC7-163, 2026-09-22)

**Presentation — SERVICE (8 edges).** The container helpers this page's
lookup chain runs (`0016D6D0`/`0016D720`/`0016D840`) are shared accessors
called from Presentation — `0016D6D0` by `001ACF80`/`001B5B60`/`001BC190`/
`001BD4A0` (+4 more). Mechanical fan-in on the runtime container family.

**Resource — SERVICE (7 edges).** The same helpers are called from the
Resource layer — `0016D6D0` by `0020B840`/`0020BFA0`/`006761F0` and
`0016D720` by `00676000` (+3 more). Same shared-accessor fan-in.

`001FB5C0` (156 B) is the virtual-dispatch adapter `001FB470` runs: it computes `esi` from `[r8+0x20]` vs `[r9]` (and `r8 == rcx+8`/`[rsp+0x60]` lanes), invokes `[rcx+0x30]`'s `+0x10` method with `edx = 0x30`, copies the `r9` qword pair into `[rax+0x20]`, then calls `0016D840(r14, rdi, rbx+8, esi)`, bumps `[rbx+0x28]`, and stores `r14` to `[r15]` - the method-call plus shared-helper wrapper.

Interior anchor `001FB635` (function `001FB5C0`).
- **Platform - CLIENT (2 edges).** `0016D6D0` is also called by bodies filed to platform: `0019CC50`, `001B1960` - shared machinery across the layer boundary, no shared ownership.
