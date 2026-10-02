---
system: EBP section_009 — the CAM7 camera table
category: 25-EBP-Script-Container
status: AUDITED
owner_layer: CodeDomain:Presentation.Camera
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN161 -> GN162 - REPLACED 2026-09-21 (OPUS), because the snapshot-identity basis this block carried is FALSE at GN162: this document cites record(s) 00258350, which batch R30 touched. The weaker basis HOLDS and is measured: the advance changed 30 records in comment and tags ONLY - 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten (check_delta_additivity.py GN161 -> PARENT, control passed) - and check_stranded_absence.py, sweeping the GN160 resolved set which strictly CONTAINS all 30, reports no live absence claim on any line of this document
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
corpus_validated: "1115 / 1115 us .ebp files, 2026-09-03 (1114 containers; 423 carry this section)"
last_reviewed: 2026-09-12
ebp_units:
  - "section_009"
audit:
  passes: 2
  last_pass: 2026-09-13
  last_pass_state: opus-section-009-pass-2
  crossref_clean: true
  reopened_count: 0
---

# EBP `section_009` — the `CAM7` camera table

> Every named camera a script can cut to: its name, its start position, and the animated
> path it flies along. The engine parses it at load into a fixed 0x40-byte lookup entry per
> camera; [`section_008`](section-008.md) is the name→index map that sits beside it.

**Corpus validation, before anything else.**

| | |
|---|---|
| files examined | **1,115 of 1,115** `us` `.ebp` files (1,114 are containers) |
| this unit present in | **423 (37.9 % of 1,114)** |
| co-occurrence | **always with [`section_008`](section-008.md)** — 423 together, **0 with either alone**, in 1,114 containers. Also always with `section_000`. |
| size range | **192 B – 66,240 B, median 5,696 B** |
| cameras held | 1 – 69 per file, median 7, **3,942 in the corpus** |

Every claim in §2 and §5 below was checked over **all 423 files**, not over one that was opened.
Where a claim holds for fewer, the count is given.

---

## 1. What the player sees

**This is the cutscene camera.** When a chest opens and the view swings round to the treasure,
when the party steps into Rabanastre's Southern Plaza and the camera pulls back over the crowd,
when a summon lands and the shot cranes up — the position the camera moves to, and the path it
takes to get there, are read out of this section of the map's or event's script file.

Scripts do not compute camera moves. They **name** one: an author writes a shot called `cut1`,
`open04` or `mapgcam_mfr_gate1`, stores it here, and the script says "play that shot." The names in
the shipped files read exactly like a shot list — `cut1`, `cut2`, `cut3`, `cut_05_02`,
`alc_b0400_cam_01`, `stay_cam_mg_cut06`, and a number of Japanese ones the localisation never
touched (`カット00` in `sum_d0001`).

**296 of the 345 event scripts have one, and 127 of the 769 field-map scripts do.** That split is
the fact behind a thing every FFXII player has noticed: **cutscenes have directed camera work and
ordinary field maps mostly do not.** A field map without this section has no authored shots at all
— the camera stays under player and follow-cam control the whole time you are in it.

## 2. The layout

Offsets are **from the start of the section**, which is where the container's directory slot 9
points. Section start is always `0x40`-aligned (an invariant of the container, checked over all
5,419 offsets in the corpus).

```struct Cam7Header base=section size=0x20
+0x00  u32   magic        'CAM7' (0x374D4143 LE) -- 423/423
+0x04  u32   cameraCount  number of camera records -- 1..69
+0x08  u32   countB       number of array-B records -- 0..382
+0x0C  u32   countC       number of array-C records -- 0..48
+0x10  u32   _reserved0   always 0 in 423 of 423
+0x14  u32   _reserved1   always 0 in 423 of 423
+0x18  u32   _reserved2   always 0 in 423 of 423
+0x1C  u32   firstRecord  offset of camera record 0, from SECTION start -- 0x20 in 423/423
```

Three record arrays follow, back to back, in this order. **No array stores its own base offset**
except the first; each array begins where the previous one ended, and each record carries its own
length, so the walk is strictly sequential.

**Array A — the cameras.** `cameraCount` records starting at `+firstRecord`. Variable length.

```struct Cam7Record base=record
+0x00  u32       _zero         always 0 in 3942 of 3942
+0x04  u32       recordLength  distance to the next record, bytes
+0x08  char[24]  name          NUL-padded; strncpy'd with n = 24 by the loader
+0x20  u32       attachWord    eye/target attachment bitfield, decoded by 002572E0 at manager init; 0x80008000 in 3730/3942
+0x24  u16       eyeJoint      copied to runtime +0x30; the joint for eye attachment modes 1 and 2
+0x26  u16       targetJoint   copied to runtime +0x32; the joint for target attachment modes 1 and 2
+0x28  u8        firstCommand  type byte of the command stream: 1 (key) in 3941/3942, 2 (segment) in one
```

> **DECODED 2026-09-12 (FABLE, `BY-1` answered) — see [the scripted camera player](../../17-Presentation-Rendering/Scripted-Camera/the-scripted-camera-player.md) §4.**
> From `+0x28` to the end of the record is **a command stream**: type byte `1` = a 0x40-byte key
> pose (eye, target, roll, field of view in degrees, three path-follow scalars), `2` = a 0x2C-byte
> segment (13 timing words, two path words, duration in frames, interpolation kind, absolute flag),
> `0xFF` = end, followed by three pad bytes. The interpreter is `00258350`, which the runtime entry's
> `+0x18` pointer feeds. All 3,942 records parse and end exactly at their length
> ([`census.out.txt`](../../_experiments/evidence/cam7-path-commands/census.out.txt)). The old reading follows: *"The **path payload** runs from `+0x2C` to the end of the record. Its length is
`recordLength - 0x2C` and its contents are not decoded — the runtime keeps a pointer to `+0x28`
and never interprets it. It is deliberately left out of the fence rather than given a plausible
field name; see §7 and `BY-1`."* — the runtime does interpret it, through the pointer.

`recordLength` is a multiple of 4 in all 3,942 records. It is **not** a fixed stride: 216 B in
3,421 records, 108 B in 421, then 324 (59), 432 (20), 388 (11), 280 (3), 560 (2), and one each
of **152**, 496, 540, 648 and 1,296. *(The 152 was missing from this list until 2026-09-13;
see the falsification pass — it is the file's one anomalous record, and its length follows
from that.)*

**Array B.** `countB` records, immediately after array A. Each begins with a **`u32` length**;
the walk advances by that length. 15,350 records in the corpus; 49 files have none. *(Decoded
2026-09-12: **ease curves** — `u32 length = 0x18 + 0x24·n`, `u32 n`, start time and value, end time
and value, then `n` 0x24-byte cubic keys whose spans sum to 1.0; evaluated by `003CC5F0`. Each is
referenced by exactly one segment timing word. [Player page §4.3](../../17-Presentation-Rendering/Scripted-Camera/the-scripted-camera-player.md).)*

**Array C.** `countC` records, immediately after array B. Each begins with a **`u16` length** —
a different width from array B, and getting that wrong desynchronises the walk. 1,682 records in
the corpus; 196 files have none. *(Decoded 2026-09-12: **paths** — `u16 length = 0x20 + 0x38·n +
8·m`, `u16 n` cubic segments, `u16 m` arc-length pairs, start and end points; evaluated by `003CC740`
through the arc table `003CC890`. Each is referenced by exactly one segment path word.
[Player page §4.4](../../17-Presentation-Rendering/Scripted-Camera/the-scripted-camera-player.md).)*

> **The three-array walk was run over all 423 files and completed on every one**, landing inside
> the section every time. That is the check that the two different length widths are real: a u32
> read of a u16-prefixed record would have run off the end.

## 3. The loader contract

**`CAM7_Load` — `0x002561C0`, 498 bytes.** One function parses the whole section. It is reached from
`CAMDAT_OnLoaded` (`0x0032FAC0`), which the container's directory walker
(`ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources`, `0x003304A0` — established by
`repos-1e`, cited not re-derived) invokes for slot 9. The handler receives a single packed argument:
**the low 4 bits are the manager slot index and the rest is the blob pointer** — split at
`0x0032FAE1` as `param & 0xF` and `param & ~0xF`. The section's `0x40` alignment is what makes that
packing safe.

**The same callback also serves a loose `.cam` file.** The extension-based ATEL loader in
`..\..\katano\atelload.c` (`0x003306E0`) binds this handler to a request for `camera/<name>.cam` at
`0x00331263`. **That path is dead in the shipped build**: the archive census finds **0 `.cam` and
0 `.cml` among 89,414 entries**, against 10,045 `.ebp`. It is the PS2-era loose-file route, left in
the binary — and it is what *names* the sections; see §6.

**Dead by construction, not only by census (2026-09-13).** The loader sizes every sibling file first with
`0x0032E400(0xFF, name)`, and that function returns `-1` for kind `0xFF` before any lookup
(`0x0032E404 cmp ecx, 0xff` → `0x0032E438 or eax, -1`). The `.cam` name buffer is `[rbp+0xA50]`: its size query
at `0x00330EBB` lands in `r12d` (`0x00330ECC`), and `0x003311EF test r12d, r12d / js` skips the whole `CAMDAT`
request, so even a shipped `camera/<name>.cam` would never be opened by this route. The same −1 is why the
control modules' companions are inert ([the ATEL companions sheet](../../01-Script-VM-Native-Bridge/ATEL-Control-Modules/the-ctrl-module-debug-companions.md)).

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| `+0x00` magic | `CAM7_Load` at **`0x002561C8`** (`CMP dword ptr [RCX], 0x374D4143`) | **mismatch → returns 0 immediately**, nothing is allocated | — | — |
| `+0x04` cameraCount | `0x002561D6` | — | see the slot rule below | — |
| `+0x08` countB | `0x002562EF` | — | — | — |
| `+0x0C` countC | `0x00256342` | — | — | — |
| `+0x10`,`+0x14`,`+0x18` | — | — | — | **yes — no reader found; see the method below** |
| `+0x1C` firstRecord | `0x0025624B` | — | — | — |
| rec `+0x04` length | `0x0025629F` | — | — | — |
| rec `+0x08` name | `strncpy(dst, src, 0x18)` from `0x00256276` | — | **24 bytes, no terminator added** | — |
| rec `+0x20`, `+0x22` | **`002572E0`** at manager runtime init (`00257341` onward) — not the loader | — | — | **no — the attachment word.** *Corrected 2026-09-12; this cell read "yes — no reader found". True of `CAM7_Load`, which this table describes; the reader is a separate pass over the resident section.* |
| rec `+0x24`, `+0x26` | `0x00256289`, `0x0025629A` | — | — | — |
| rec `+0x28`… | address taken by the loader; **interpreted by `00258350`** (2026-09-12) | — | — | — |

**The magic is genuinely checked, and this is worth stating plainly** because the container that
holds this section is not: `EBP2` appears nowhere in the executable, while `CAM7` appears exactly
once — at `0x002561CA`, as the immediate of that one `CMP`. **Corrupt the four bytes at the start
of section 9 and the section silently does not load**; corrupt the four at the start of the file
and nothing is known to happen.

**What loading builds.** Three parallel arrays, indexed by manager slot:

```
g_camEntries    0x02092810[slot]   cameraCount * 0x40 bytes   allocated at 0x00256240
g_camArrayB     0x02092818[slot]   countB      *    8 bytes   allocated at 0x00256303
g_camArrayC     0x02092820[slot]   countC      *    8 bytes   allocated at 0x0025633D
g_camBlob       0x02092808[slot]   the section pointer itself, stored at 0x00256205
```

Arrays B and C hold **pointers straight back into the section blob** — the records are never
copied. The section must therefore stay resident for as long as the slot is live, which it does:
the blob pointer is what the teardown frees.

Each camera's 0x40-byte runtime entry is:

```
+0x00  char[24]  name          strncpy from record +0x08, n = 24
+0x18  ptr       -> record +0x28   (the path payload, in the blob)
+0x20  u64       0             written zero by the loader, every load
+0x28  u64       0             written zero by the loader, every load
+0x30  u16       from record +0x24
+0x32  u16       from record +0x26
```

**The name field is the one real hazard for a modder.** `strncpy` with `n = 24` into a field
that is exactly 24 bytes **adds no NUL terminator when the source fills all 24**, and the very next
bytes are the payload pointer at `+0x18`. In the shipped corpus the longest camera name is
**23 characters** (histogram in §5) and **not one of 3,942 names is unterminated**, so the game
never exercises this. A 24-character name would.

**And the lookup that finds a camera by name compares only 23 bytes** — `strncmp(name, entry, 23)`
at `0x00256594`, one fewer than the copy. Two cameras whose names differ only in their 24th
character are indistinguishable to `CAM7_FindCameraByName`. *(2026-09-12: that lookup is unreachable in the shipped build — its only caller sits behind a gate that returns 0 — so the camera a script plays is chosen by `section_008`'s authored index, not by name.)* See
[`section_008` §3](section-008.md#3-the-loader-contract).

**The slot rule, and what happens past it.** There are **5 manager slots** (`slot < 5`, tested at
`0x002561DC`). For `slot >= 5` the loader sets `cameraCount = -1` before allocating — `alloc(-1 << 6)`
— and every subsequent loop is guarded `0 < count`, so nothing is written. **A blob is still stored
at `g_camBlob[slot]` before that test**, at `0x00256205`, with no bound on `slot`. Whether any
caller can reach `CAM7_Load` with `slot >= 5` was not established here; ~~the one caller reads~~ the live caller, `0032FAC0` (call at `0032FB0A`), reads *(corrected 2026-10-02, OPUS: `CAM7_Load` has two call sites — `0032FB0A`, and `003312A7` in `003306E0`, the loose-file route §6 finds dead in the shipped build)*
`param & 0xF`, which admits 0–15.

**Empty is a success.** `cameraCount == 0` with `slot < 5` returns **1** at `0x002561E4` without
allocating anything — a distinct outcome from the magic rejection, which returns 0.

**No field is clamped and no field is normalised.** `firstRecord`, `recordLength`, `countB` and
`countC` are all used as read, with no range test against the section's own length — which the
loader is never told. A short or truncated section walks off the end.

**The write path.** None found. Nothing in the executable writes `CAM7`; it is authored offline.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `0x002561C0` | `CAM7_Load` — the whole parser (magic `0x002561C8`, name copy `0x00256276`, chain step `0x0025629F`, array-B build `0x00256303`, array-C build `0x0025633D`) | ✅ full body |
| `0x002561A0` | invalidate slot: `if (slot < 5) g_camBlob[slot] = 0` — the store is at `0x002561B6` | ✅ full body |
| `0x0032FAC0` | CAMDAT completion callback — unpacks slot from `param & 0xF` at `0x0032FAE1`, stores the blob at `0x0032FAED`, calls `CAM7_Load` | ✅ full body |
| `0x00256530` | `CAM7_FindCameraByName(slot, name)` — the reverse lookup [`section_008`](section-008.md) drives: `0x40` stride `0x00256589`, `strncmp` n=23 `0x00256594`, hit `0x002565BC`, miss `0x002565A4` | ✅ full body |
| `0x0026CE20` | binder: `manager[+0xE0] = blob`, store at `0x0026CE31` — how `section_008` learns this section has arrived | ◐ entry + that store |
| `0x003304A0` | container directory walker; dispatches slot 9 to `0x0032FAC0`. Established by `repos-1e`, cited not re-derived | ✗ |
| `0x003306E0` | the dev-era ATEL dispatcher; binds this callback to the loose-file `CAMDAT` request at `0x00331263` (tag string `0x0033122D`, filename buffer `0x00331255`) | ◐ read for the binding only |
| `0x0032ED80` | `ActorResource_ResetManagerLoadState` — teardown; frees the blob at `0x0032EFBD`, clears the slot at `0x0032EFC4` | ◐ read for the teardown only |
| `0x002572E0` | a consumer; re-reads `+0x1C` off the stored blob at `0x0025735E` | ◐ entry + that read |

## 5. Corpus survey

**Invariants — every one checked over all 423 files and all 3,942 records.**

| | |
|---|---|
| `+0x00` magic | `CAM7`, **423 / 423** |
| `+0x10`, `+0x14`, `+0x18` | `0`, **423 / 423** |
| `+0x1C` firstRecord | `0x20`, **423 / 423** — the loader reads it, but it has never been anything else |
| record `+0x00` | `0`, **3,942 / 3,942** |
| record length % 4 | `0`, **3,942 / 3,942** |
| three-array walk | terminates inside the section, **423 / 423** |
| name NUL-terminated within 24 B | **3,942 / 3,942** |

**What varies.** `cameraCount` 1–69. `countB` 0–382 (49 files zero). `countC` 0–48 (196 files
zero). Record length takes ~~11~~ 12 distinct values *(corrected 2026-10-02, OPUS: 3,942 records walked in the 423 `us` sections, read through `vbf_read_entry` from `FFXII_TZA.vbf` — 108, 152, 216, 280, 324, 388, 432, 496, 540, 560, 648, 1,296; the 2026-09-13 pass)*.

**Name lengths — the strncpy limit is 24 and the corpus stops at 23:**

```
 4:111   5:432   6:472   7:112   8:943   9:382  10:200  11:130
12:108  13: 79  14:137  15: 45  16:373  17: 32  18: 86  19: 92
20: 87  21: 49  22: 41  23: 31        24: 0   <- never reached
```

**Duplicate camera names exist, in exactly 11 files.** Each of those 11 has **exactly one** name
used twice — `cut4`, `cut001`, `open04`, `cut_05_02`, `cut1_2`, `cut2_2`, `mapgcam_mfr_gate1`,
`magcam_rblj01_r_nw2`, `stay_cam_mg_cut06`, `カット00`, `mapgcam_SUIMON_E_床の丸`. This is the
entire explanation for the 11 files where this section's count and `section_008`'s disagree; see
[`section_008` §5](section-008.md#5-corpus-survey).

**~~`subCount`~~ `firstCommand` (the first command's type) at record `+0x28` is 1 in 3,941 of 3,942 records.** *(answered: "The lead held (2026-09-12)" below and the §2 fence; 2026-10-02, OPUS)* The single exception is a record
of 152 bytes where it is 2, against a 108-byte minimum — 44 bytes more. An invariant that holds
3,941 times and breaks once is a much better lead than one that always holds.

> **The lead held (2026-09-12).** `+0x28` is the first command's type: `1` = key. The exception,
> `dst_a07` record 2, starts with a segment (`2`), so it is `0x28 + 0x2C + 0x40 + 4 = 152` bytes where
> a lone key is `0x28 + 0x40 + 4 = 108`; key-move-key is 216. Its script starts it on the same channel
> straight after record 1, so the segment blends out of record 1's last key
> ([player page §2.4](../../17-Presentation-Rendering/Scripted-Camera/the-scripted-camera-player.md)).

**Outlier worth its own line.** The largest section in the corpus is 66,240 B, 345× the smallest.

## 6. Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Is `+0x1C` an offset from the section or from the file? | **From the section.** `CAM7_Load` computes `blob + *(u32*)(blob + 0x1C)` at `0x0025624B`, where `blob` is the section pointer. It is `0x20` in all 423 files, so the corpus alone could not have decided this — the instruction did. |
| Does the record chain hold on the corpus or on the file that was opened? | **All 423, all 3,942 records.** Walking `cur += *(u32*)(cur+4)` for exactly `cameraCount` steps, then `countB` u32-prefixed records, then `countC` u16-prefixed records, terminated inside the section every time. |
| Is `CML1` really the partner, or did the two just happen to co-occur? | **The binary says so, not the co-occurrence.** `0x003306E0` builds two filenames from one base and requests both: `camera/<name>.cam` tagged `CAMDAT` → callback `0x0032FAC0` → this loader, and `<name>.cml` tagged `CAMCTL` → callback `0x0032FA10`. Both leas are in the disassembly at `0x00331255`/`0x00331263` and `0x00331314`/`0x00331322`. |
| Could the `0x8000` at record `+0x20` be read somewhere the census missed? | ~~**Not resolved by search alone, and it is not claimed.**~~ **Yes — `002572E0` reads it** *(corrected 2026-10-02, OPUS: `00257341` `mov edx, dword ptr [rdi + 0x20]` with `rdi` = blob + `[blob + 0x1C]`, the first record, and bit 15 — the `0x8000` — at `002573BB`–`002573C6` `shr ecx, 0xf` / `and cl, 1`; §3's attachment word, corrected 2026-09-12)*. The loader provably does not touch it — it reads `puVar3[0x12]`/`[0x13]`, byte offsets `0x24`/`0x26`, and nothing at `0x20`. A consumer reading it through the `+0x18` payload pointer would be a *backward* read past the pointed-to address, which nothing observed does. ~~Listed inert **with that method named**, not asserted unused.~~ *(answered: read — the correction at the head of this cell; 2026-10-02, OPUS)* |
| Did an external tool supply any of this? | **No tool reads `CAM7`.** `ff12-script` decompiles `section_000` only. Nothing here has an oracle, which is why every claim is anchored to an instruction or a 423-file count. |
| Does the shipped game actually take the `.cam` file path? | **No — and that is why the extension evidence is still usable.** The archive census finds **0 of 89,414 entries** with either extension. The shipped route is the container walker at `0x003304A0` (`repos-1e`), which calls the *same* `0x0032FAC0`. The dead loose-file path is what **names** the section: one callback per request, `camera/<n>.cam` tagged `CAMDAT` and `<n>.cml` tagged `CAMCTL`. |
| Is `CAM7` the only thing `CML1` pairs with? | **No — `section_010` is also `CML1`**, paired with `SHK1` (`section_011`), 113/113. Censused here over the first four bytes of every present section in all 1,114 containers. `CML1` is a shared list format and this section is one of its two partners — which the dispatcher's `.cam`/`.cml` and `.shk`/`.skl` DAT/CTL pairs say independently. |

**What was tried and failed to break it.** A magic-constant scan of the whole executable for
`CML1` (`0x314C4D43`) and for `CAM7` (`0x374D4143`), as bytes and as dwords, forwards and
byte-reversed: `CAM7` hit **exactly once**, `CML1` **zero times**. If `CAM7_Load` had been one of
several parsers, or if the constant were built by arithmetic, the single hit would not have landed
on a `CMP` at the top of a 498-byte function that goes on to parse the exact structure the corpus
shows.

## 7. What this document does not claim

- ~~**The path payload from record `+0x2C` to the end of the record is not decoded.**~~ **Decoded 2026-09-12 (`BY-1` answered)** — a key/segment/end command stream from `+0x28`, §2 and [the player page](../../17-Presentation-Rendering/Scripted-Camera/the-scripted-camera-player.md). The original text follows. The loader
  takes its address and stops. Record lengths cluster on 108 and 216 with 11 distinct values, and
  the one `subCount == 2` record is 44 B larger than the 108 B minimum — so there are at least two
  independent size dimensions. Calling it "the animated path" in §1 rests on the field being a
  per-camera variable-length payload in a camera table, **not on a decode**. → `PROPOSED-repos-4b-1`
- ~~**Arrays B and C are counted and walked, not interpreted.**~~ **Interpreted 2026-09-12** — ease curves and paths, §2. The original text follows. Their record contents are unread; all
  that is established is the count fields, the two different length-prefix widths, and that the
  runtime keeps pointers to them.
- ~~**The four-channel loop is not explained.**~~ **Explained 2026-09-12 (`BY-4` answered): four camera channels per actor-manager slot**, each a 0x2E0-byte player record that `002566E0` clears; scripts bind a `CML1` entry to a channel with `camerastart*` and the `(u16, u16)` pairs `section_008` resets are each channel's state and entry number ([player page §2.2](../../17-Presentation-Rendering/Scripted-Camera/the-scripted-camera-player.md)). The original text follows. Before calling `CAM7_Load`, the CAMDAT handler loops
  `FUN_002566E0(slot, 0..3)` — four sub-slots per manager, matching the four `(u16, u16)` pairs
  [`section_008`](section-008.md) resets. What the four channels are was not established.
  → `PROPOSED-repos-4b-4`
- **The `slot >= 5` path was not shown to be reachable.** The out-of-range blob store at
  `0x00256205` is described as read, not as exploitable.
- *Superseded 2026-09-12:* `0x002572E0`, `0x00257230`, `0x00258350` and `0x002567E0` are read, and what the camera data does once loaded is documented in [the scripted camera player](../../17-Presentation-Rendering/Scripted-Camera/the-scripted-camera-player.md). The original text follows: `0x002572E0` and the other consumers of `g_camEntries` were not read in full — only the `+0x1C`
  re-read was confirmed. **What the camera data does once loaded is not documented here**; this
  sheet is the file format and its loader.

## 8. Related

- [`section_008` — the `CML1` camera name list](section-008.md) — the strict partner; its `id`
  column indexes **this** section's record array.
- [`25-EBP-Script-Container/README.md`](../README.md) — the container, its directory, and the
  frozen 13-section census.
- [`01 — Script VM & Native Bridge`](../../01-Script-VM-Native-Bridge/README.md) — the verbs a
  script uses to name a camera live there, not here.

## Falsification pass 2 — 2026-09-13 (OPUS)

§6 records a falsification pass from 2026-09-03 against the section walk. This one re-derives
**every corpus number in §2** from a corpus extracted from `FFXII_TZA.vbf` in this session, with the
container walk written from §2's own description rather than imported from the census script beside
the page — so a mistake in that script could not reproduce itself here.

| claim | measured |
|---|---|
| **423** files carry a CAM7 section 9 | **423**, out of 1,115 `us` containers |
| section starts are `0x40`-aligned over **5,419** offsets | **5,419 offsets, zero misaligned** |
| magic, and `_reserved0/1/2` zero, and `firstRecord == 0x20` — 423/423 each | **423 / 423 / 423** |
| `cameraCount` 1..69 · `countB` 0..382 · `countC` 0..48 | **1..69 · 0..382 · 0..48** |
| **3,942** camera records, `+0x00` zero in all | **3,942 / 3,942** |
| `attachWord == 0x80008000` in **3,730** | **3,730** |
| `firstCommand`: 1 in 3,941, 2 in one | **{1: 3941, 2: 1}** |
| `recordLength` a multiple of 4 in all | **0 exceptions** |
| **15,350** array-B records, **49** files with none | **15,350 · 49** |
| **1,682** array-C records, **196** files with none | **1,682 · 196** |
| the three-array walk completes inside the section on every file | **423 / 423** |

### The one stride the list was missing is the one record worth listing

The distribution came back with **twelve** distinct lengths, not eleven: a single record of
**152 bytes**, absent from §2's list.

It is not an extra anomaly. **It is the same record** — `dst_a07.ebp` record 2, `dst_a07_e02`, the
one whose `firstCommand` is `2` instead of `1`, which §2 already notes and which the player page's
census reports as *"streams starting with a segment: `[('dst_a07.ebp', 2)]`"*.

And its length follows from that, exactly:

| stream | bytes |
|---|---|
| the ordinary `KSKE`: `0x28` header + key `0x40` + segment `0x2C` + key `0x40` + end and pad `4` | **216** |
| `dst_a07_e02`'s `SKE`: `0x28` + segment `0x2C` + key `0x40` + end and pad `4` | **152** |

So the page's own three facts about this record — it starts with a segment, it is the only one, and
its stream is `SKE` — **predict 152 without measuring it.** The omission mattered because §2 presents
the list as the observed set: a parser written from it would treat 152 as impossible, and the record
it would reject is the single most interesting one in the corpus.

### `BY-4` is closed

I raised `BY-4` on 2026-09-12: `census.py`'s output was not byte-reproducible, because
`Counter.most_common()` and plain dicts print ties in insertion order, so a re-run showed three
differences that were ordering rather than value. FABLE added `mc()` and `sd()` — a deterministic
tie-break and a key-ordered dict.

**Re-run here against an independently extracted corpus: byte-identical to the committed
`census.out.txt`.** The artefact is now diffable, which is what makes it evidence rather than a
record of one run. Closed, and confirmed by the consumer who raised it.

**Not claimed:** nothing here was executed or observed live. §3's loader contract and §4's addresses
were not re-derived; this pass took §2's layout and every corpus denominator in it.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

**Movement — SERVICE.** The camera-data interpreter `00258350` calls a 154-byte movement helper
([the scripted camera player](../../17-Presentation-Rendering/Scripted-Camera/the-scripted-camera-player.md)).

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Presentation — SERVICE and CLIENT.** A cited body calls three Presentation-filed bodies (694, 128 and 253 bytes), and another cited body is called by the 694-byte one.

*Citation spellings (R5), 2026-09-14 (FABLE):* these crossings become reportable once citations written 0x... or FUN_... count (R5); tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Resource — CLIENT and SERVICE, 9 edges.** The 80-byte size probe this page cites is called by Resource bodies of 126 to 522 bytes, and a 3,882-byte function it cites calls that probe.
- **ActorEntity — CLIENT and SERVICE (53 edges).** 18 inbound (ActorEntity bodies `ActorResource_ResetManagerLoadState` (0032ED80), `0032FAC0`, `003306E0` call page-cited `002566E0`, `0032E400`, `002561C0`); 35 outbound (page-cited `ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources` (003304A0), `ActorResource_ResetManagerLoadState` (0032ED80), `0032FAC0` call ActorEntity bodies `00263FF0`, `002566E0`, `ActorResource_FinalizeManagerRuntimeAfterLoads` (0032F1B0)). Substantive edges include `002561A0` is called by `ActorResource_ResetManagerLoadState` (0032ED80); `002561C0` is called by `0032FAC0`; `002561C0` is called by `003306E0`; `002566E0` is called by `ActorResource_ResetManagerLoadState` (0032ED80); the remaining edges run through shared helpers the page cites.
- **World — CLIENT (1 edge).** 1 inbound (World bodies `00378540` call page-cited `0032E400`). Substantive edges include `0032E400` is called by `00378540`.
- **WorldAreaField — CLIENT (5 edges).** 5 inbound (WorldAreaField bodies `MapRef_BeginLoadResources` (00268750), `00378030`, `AreaArd_LoadOrUnloadFieldResource` (003EA820) call page-cited `0032E400`). Substantive edges include `0032E400` is called by `MapRef_BeginLoadResources` (00268750); `0032E400` is called by `00378030`; `0032E400` is called by `AreaArd_LoadOrUnloadFieldResource` (003EA820); `0032E400` is called by `00379A10`.
