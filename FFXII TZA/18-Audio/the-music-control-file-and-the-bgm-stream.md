---
system: musicctrl.bin and the script BGM stream — the field → track table is a kind-9 resource loaded whole at boot and rebased in place; the 0x38-byte descriptor beside it is a script-driven streaming reader that the shipped build cannot feed
category: 18-Audio
status: AUDITED
owner_layer: PrimaryOwner:Audio
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 75 cited function entries, 0 of them among the 109 records that changed GN160 -> GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0), established for this document 2026-09-14 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
corpus_validated: "ps2data/image/ff12/in/common/musicctrl.bin (1,615 B, byte-identical to the ch/common copy) extracted from FFXII_TZA.vbf and walked page by page under the reader's own decoding: 11 pages, 291 runs, every page's chain ending exactly at the next page's offset, the last run at field 1311 = the header's maximum; all 1,115 us .ebp scripts walked for the eight BGM-stream verb ids with the SetSaveData walk (six hits on 302B) as the positive control, 2026-09-11"
last_reviewed: 2026-09-13
archive_formats:
  - "MUS0 | explained | musicctrl.bin (.bin member): {MUS0, u32 maxFieldId, u32 pageOffset[11], runs} - (kind 9, 0x20) into 02B5E0D0, walked by 003EAA70, section 2"
  - "fhmusicdata | explained | fhmusicdata.bin (.bin member; kind-9 path index 0x1C): {u32 count 27, u32 offset[27] (stride 22), 11-u16 records} (706 B) - structural layout only: no requester found by a whole-image constant/loop/record sweep with positive controls, so no field is read or named in this build, section 2"
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-musicctrl-pass-1 - every published figure reproduces, including the two byte-identical copies, the header, all eleven page offsets, the per-page run counts and the total 291 with every chain closing exactly, the last run at 1311/0 meeting maxFieldId, and 0 of 1,115 scripts calling the nine BGM-stream ids against a 302B control of six; ADDED: the decoding note never states the widths - the run header is a u16 (start:11, span:5) followed by a COUNT BYTE at +2, and the reader's advance is 3*count + 4 - without which the walk cannot be reproduced at all
  crossref_clean: false        # 2026-09-30 (SWE2-DATA): false until the pass-22 UNACCOUNTED NEIGHBOUR findings are accounted (FRONTIER-REQ-SWE2-DATA-PASS22-DEBT; OPUS-REQ-DATA-PASS30-CROSSREF-CLEAN-0930)
  reopened_count: 0
---

# musicctrl.bin and the script BGM stream — the field → track table is a kind-9 resource loaded whole at boot, and the descriptor beside it is a streaming reader the shipped build cannot feed

> **Two things share one small block of BSS at `02B5E0C0`, and they were being read as one.** The
> qword at `02B5E0D0` is the **field → track table** the music page decodes: it is the shipped file
> `ps2data/image/ff12/in/common/musicctrl.bin`, resource kind 9 index 32, loaded whole through the
> request queue at boot and rebased in place by its completion callback. The `0x38` bytes from
> `02B5E0E0` are **not a read layer under the queue**: they are the one descriptor of the **script
> BGM stream** — eight verbs (`usebgmstream` … `getbgmstreamstatus`) that allocate a ring buffer,
> stream a kind-`0x24` file into it in 64 KB pieces and hand it to the sound layer. In the shipped
> build that stream can never load: kind `0x24` has no path array, no size-table entry, and no
> script calls the verbs. Its one side effect is the only thing that would ever make the queue chunk
> a request.

**Corpus validation, before anything else.**

| | |
|---|---|
| file | `ps2data/image/ff12/in/common/musicctrl.bin`, 1,615 B; the `ch/common/` copy is byte-identical; no other copy in the archive |
| header | `"MUS0"`, `u32 maxFieldId = 1311`, `u32 pageOffset[11]` = 52, 106, 260, 491, 628, 790, 1024, 1227, 1329, 1463, 1571 |
| walk | 291 runs (12, 28, 39, 29, 30, 33, 35, 18, 29, 27, 11 per page); every page's chain ends **exactly** at the next page's offset, the last at end of file; the first run of each page starts at 12, 129, 253, 380, 517, 640, 767, 898, 1009, 1153, 1283 |
| positive control | the walk uses the decoding the music page took from `003EAA70` — **`w` is a `u16`, and `count` is the byte at run `+2`** (`start = w & 0x7FF`, `span = w >> 11`, stride `4 + 3 × count`; the widths added §8, without which the walk cannot be reproduced); the reader's own header check (`maxFieldId`) and the file's last run (start 1311, span 0) meet at the same number |
| the shipped scripts | 0 of 1,115 `us` `.ebp` files call any of the verb ids `0448`–`044F` or `201E`; the same byte walk finds the six `302B` sites the presets page records |

## 1. What the player sees

**The music an area plays as the story moves on is authored in one small data file, not in the
executable and not in the area's script.** Change `musicctrl.bin` and every area's ladder changes;
the executable never rebuilds or rewrites the table after boot.

Nothing a player can reach uses the BGM stream. The verbs exist, the descriptor exists, and the
state machine ticks every frame from the request pump — but no shipped script issues the verbs and
the file kind they would read has no files. A modder who wants a long streamed track through this
path has to supply all three: a script that calls the verbs, a path array for kind `0x24`, and
size-table entries for it.

## 2. The music-control file — `02B5E0D0`

### 2.1 What loads it, and when

`00379D20` (23 B) is the boot loader for three whole-file kind-9 resources, in this order:

```
00379D24  call 003EAC40      ; npcdic.bin     kind 9 index 0x1F -> 02B5E0D8, callback 003EAC70
00379D29  call 00473D20      ; questbase.bin  kind 9 index 0x21 -> 02CA6C60, callback 0016D6A0 (none)
00379D32  jmp  003EAB60      ; musicctrl.bin  kind 9 index 0x20 -> 02B5E0D0, callback 003EAB90
```

Its only caller is the boot fixer `0022A0B0` (`0022A433`, between `00379E90` and `0036E310`) — the
function [what-the-engine-fixes-at-boot](../00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md)
describes. `003EAB60` is reached by a **tail jump**, which is why a scan for `call` sites found none
(`DG-5`). `02B5E0D0` has exactly one writer in the image (`003EAB78`), ~~so the table is bound once per~~
~~process and never rebound or freed: its lifetime is the process.~~ *(Qualified 2026-09-27 (FABLE, Claude Opus 5.5), on
`ASTRA-RETURN-FABLE-MUSICCTRL-BINDING-PROVENANCE`: one writer is not one invocation.)*
- *`003EAB60` calls the loader and stores the result with no guard: no old-pointer test, no one-shot flag.*
- *Its route in is a boot job the application queues, which reaches the boot fixer above. OPUS's MC-1 qualification
  in [the contract](CONTRACT-music-control-file-and-bgm-stream.md) reads that chain and finds no one-shot guard on it.*
- *So how often the framework runs that job, and whether heap 5 is ever released or reset, are **not established**.
  "Bound once, never freed, process lifetime" is not shown. Nothing read here shows a second binding in normal play
  either.*

Each of the three goes through `0051ED10(kind, index, callback)` (153 B), the whole-file loader:

```c
size  = 0032E400(kind, index);                 /* the file-size table's entry AS IS; see below */
0036C1D0(5); block = 0036A190(size); 0036C140();   /* heap 5 */
desc = { 0, (u32)callback, 0051EDB0, 0016D6A0, 0 };  /* arg, onDone, onCancel, onPart */
0032E620(kind, index, block, size, &desc);     /* queue the read */
return block;                                  /* handed back before the bytes arrive */
```

**The size is rounded up to 64 on one path only** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 325, which executed it; `0032E400` re-read.)*. With a table for the kind and an index below
`0x400`, `0032E400` returns the table entry unchanged (`0032E428`–`0032E430`). Only the fallback rounds a positive
size up to a multiple of 64 (`0032E43B`–`0032E448`). The fallback serves a kind with no table or an index of
`0x400` or more. Kind `0xFF` returns `-1`. OPUS measured the table path through the stream machine: a
`0x12345`-byte file clamps the ring to `0x12345`, not `0x12380`. *The comment in the listing above used to say
"rounded up to 64" for every path.*

The file arrives through [the request queue](../02-Resource-And-Asset-Pipeline/the-resource-request-queue.md):
the pump issues the read, and on delivery `0032E330` calls the slot's done callback with the
descriptor's `+8` word as its first argument (`0032E34C` `mov ecx, [rcx+0x60]`). That callback is
`0051EDB0` — two instructions, `movsxd rax, ecx; jmp rax` — so **the `+8` "arg" word is the real
callback, carried as a sign-extended 32-bit pointer**, which is sound only because the image is
loaded at `0x120000` and never relocated.

The path is the kind-9 array `01EBF740` entry 32 (`ResourcePath_Init` installs it; entries 28–35
read `fhmusicdata.bin`, `npc_name.bin`, —, `npcdic.bin`, **`musicctrl.bin`**, `questbase.bin`,
`questhint.bin`, `questhittext.bin`). The size comes from
[the file-size table](../02-Resource-And-Asset-Pipeline/Loose-Files-And-Size-Tables/file-size-tables-fst.md)
at `(9, 32)`.

**Entry 28, `fhmusicdata.bin`, has a layout and no requester (2026-09-29, SWE2-DATA,
`OPUS-REQ-DATA-BUCKET-MEMBER-FORMATS`).** One copy ships (`ps2data/image/ff12/common/fhmusicdata.bin`,
706 bytes); its path sits at kind-9 index `0x1C` in all ten language arrays.

```struct FhMusicDataHeader base=file size=0x70
+0x00  u32      count          27
+0x04  u32[27]  offset         from file start; offset[0] = 4 + 4*count = 0x70, constant stride 22
```

Each record is 11 `u16`: word `+0` a strictly ascending key (0–47, 27 distinct), words `+0x0C`,
`+0x0E`, `+0x12`, `+0x14` zero in every record, and the rest small values (`+0x02` = 1, `+0x04`
18 or 20, `+0x06` 0 or 1, `+0x08` = 1, `+0x0A` 1 / 18 / 20, `+0x10` 1–3 or 20); `4 + 4·27 + 22·27 =
706` exactly. **No request for `(9, 0x1C)` was found**: no constant kind/id pair at any of the
122,250 call sites, no id-register load of `0x1C` before a request call (control: the loop form
`lea edx, [rbx+0x98]` at `00291CF3` is found), no stored `(9, 0x1C)` pair in code or data, and the
9,351 prefetch lists never name it. So its fields have **no reader in this build**, and none is
named here. The sweep cannot see a kind/id computed at run time at the 89 register-held request
sites. Check: [`b2_fhmusicdata.py`](../_index/candidates/bucket-members-0929/checks/b2_fhmusicdata.py)
(14 checks, FAILS 0).

### 2.2 The completion callback rebases the pages in place

`003EAB90` (71 B) ~~runs once, when the bytes are in:~~ runs as the load's completion callback, once per load,
when the bytes are in:

```c
t = *(u8 **)0x02B5E0D0;
pages = (t->maxFieldId + 0x7F) >> 7;            /* 11 for 1311 */
for (i = 0; i < pages; i++)
    if (t->pageOffset[i]) t->pageOffset[i] += (u32)t;   /* a 32-bit add */
```

After it, the header's page words are **absolute 32-bit addresses**, which is exactly how the reader
consumes them (`003EAA9C` `movsxd rax, dword [r8 + rcx*4 + 8]` then an immediate dereference). Two
things follow for a modder: the block must live below 2 GB for the sign-extension to land — heap 5 is
where `0051ED10` puts every whole-file table — and a page offset of 0 stays 0, which the reader
treats as "no page" (`−1`).

*Qualified 2026-09-27 (FABLE, Claude Opus 5.5), on `ASTRA-RETURN-FABLE-MUSICCTRL-PAGE-BOUNDARY`
(`_experiments/evidence/musicctrl-page-boundary/`). The rebase and the reader count pages differently:*
- *The rebase visits `(maxFieldId + 127) / 128` page words (`003EAB9A`–`003EABA7`).*
- *The reader accepts every field id up to and including `maxFieldId` (`003EAA88 cmp [r8+4], ebx` / `jl`) and selects
  page `fieldId / 128`.*
- *The two agree unless `maxFieldId` is a multiple of 128, 0 included. Then field `maxFieldId` selects page
  `maxFieldId / 128`, one past the rebased set (with 0, no page is rebased at all). A non-zero word there is used unrebased, as an absolute sign-extended
  address. A zero word returns −1. For example, with `maxFieldId` 128 only page 0 is rebased, but field 128 reads page 1.*
- *The shipped file is unaffected: 1311 gives 11 pages, and the reader's highest page is index 10.*
- *So "every page word is absolute after the rebase" holds only for the visited pages. A modded table whose
  `maxFieldId` is a multiple of 128 must leave that extra word zero.*

### 2.3 The file, walked

The music page decodes the reader; the file confirms the decoding and adds what only the data can
say:

```
musicctrl.bin (1,615 B)
  +0x00  char[4]  "MUS0"
  +0x04  u32      maxFieldId          1311
  +0x08  u32[11]  pageOffset          file offsets until 003EAB90 rebases them
  +0x34  run[]    page 0 … page 10    each page a chain of runs, contiguous, no terminator
run
  +0x00  u16      start | span<<11    fields start … start+span inclusive (span 0 = one field)
  +0x02  u8       count               ladder rungs
  +0x03  u8       track               the default track (0 = silence)
  +0x04  rung[count]  { u16 threshold, u8 track }   3 B each
```

| census | |
|---|---|
| runs | **291**; 122 span more than one field (largest span 22 = 23 fields); 726 field ids covered, 586 of 0…1311 uncovered (a lookup returns −1 = silence) |
| ladders | **48 runs carry one** — 133 rungs, at most 6 on one run (field 742); 41 of the 48 end with the rung `{11000, 0}` |
| tracks | 70 distinct track values across defaults and rungs |
| page ends | a page's chain has no terminator; a lookup that misses a page's last run reads the **next page's first run**, whose start exceeds every id of the page, and fails there. On the last page the last run *is* field 1311 and the header refuses anything above it, so no lookup walks past the end of the file |

So `DG-3` is answered: **the ladder is exercised** — one run in six carries one, and several change
track more than once as the story variable climbs (field 742: 75 by default, then 0 → 39 → 0 → 31 → 59 → 0 as the variable
passes 1976, 1982, 2200, 2250, 2350, 11000).

**The earlier count of 316 runs** ([EXP-008](../_experiments/EXP-008-the-real-music-table.md)) came
from a walker that did not stop at the next page's offset: its per-page counts run one or two above
these on pages 0–9 and reach 25 on page 10 with a "highest start" of 1810, above the header's
maximum — the overrun into the file's tail. The table it captured is this file; the count is not.

## 3. The script BGM stream — `02B5E0E0`

### 3.1 The descriptor

One `0x38`-byte descriptor, initialised by `003EB050` (from `0032EA90`, which also initialises the
queue). The checker `003EB0D0` is written as a loop over a `0x38`-stride array bounded to one
iteration, so there is one stream:

```
BgmStream at 02B5E0E0 (0x38 B)
  +0x00  i32   requestId        the queue's id of the read in flight, −1 idle
  +0x08  u8*   buffer           script-allocated ring buffer (usebgmstream)
  +0x10  i32   bufferBytes      the ring size; shrunk to the file size when the file is smaller
  +0x14  i32   soundHandle      from 002DF660 when the sound layer takes the buffer
  +0x18  i32   streamId         the sound layer's stream, 0 = none
  +0x1C  i32   kind             always 0x24
  +0x20  i32   index            the verb's argument
  +0x24  i32   fileBytes        from the file-size table
  +0x28  i32   bytesRead        cumulative
  +0x2C  i32   ringCursor       bytesRead mod bufferBytes
  +0x30  u8    state            1…8
  +0x31  u8    active
  +0x32  u8    0x40             handed to 002DF680 at play
  +0x33  u8    0x7F             handed to 002DF680 at play
```

### 3.2 The verbs

| id | verb | handler | what it does |
|---|---|---|---|
| `044D` | `usebgmstream(bytes)` | `003557C0` | frees any stream (`003EB010`), then `003EACA0(bytes)`: rounds up to a 64 KB multiple with a floor of `0x30000`, allocates from heap 2 (`0036C1D0(2)`, `0036A190`), tags it with the empty string at `00D51814` (`0036C660`), and `003EB180` records buffer and size |
| `0448` | `bgmstreamread(index)` | `00354690` → `003EB100` | with a buffer present: kind `0x24`, the index, counters and handles zeroed, `requestId = −1`, **state 1, active** (`003EB10C`–`003EB139`); then the VM wait byte `00314D40(1)` |
| `0449` | `bgmstreamreadsync` | `00354920` → `003EB0A0` | keeps waiting while active and the state is neither 0 nor 5 |
| `044A` | `bgmstreamplay` | `003EB150` | active and state 5 → state 6 |
| `044B` | `bgmstreamplaysync` | — | no handler in the table |
| `044C` | `bgmstreamstop` | `003EADC0` → `003EAD10` | per state: pump the queue to idle (`0032E520(0)`), or poll `002DEE90(soundHandle)` until the sound layer is done (yielding through `0035EA30`), then close the stream (`002DF690(streamId)`); clears `active` |
| `044E` | `freebgmstream` | `003EB010` | stop as above, free the buffer (`003697F0`), zero buffer and size |
| `044F` | `getbgmstreamstatus` | `00355FB0` | `VMResult_WriteInt32(003EB0D0())` — 1 while active |
| `201E` | `debug_bgmstream(x)` | `0050C7F0` | pops the argument and does nothing |

### 3.3 The machine — `003EADE0`, ticked by the request pump

The pump `0032E070` calls `003EADD0` → `003EADE0` in its state-1 arm (`0032E0BD`) and at the end of
every pass (`0032E29B`). ~~A return of 1 means the stream submitted or advanced~~ *(narrowed 2026-09-30, OPUS,
static: every return path is `mov eax, esi`, and `esi` is set to 1 only at `003EAE54` and `003EAFA2`, each right
after a submit through `0032E780`; so **a return of 1 means the stream submitted a piece**, and the advances 2 → 4
and 4 → 5 return 0. Reported by SWE2-ORACLE's
[S-08 drain record](../_index/candidates/s08-bgm-machine-drain-0930/README.md))*, and **the state-1 arm
then skips the queue for that pass** (`0032E0C4` `jne 0032E2A0`): the stream is served before any
queued request. *Both submits precede the machine's next state write (`003EAE4C` before `003EAE63`, `003EAF9A`
before `003EAFAD`); with the request pool full, that submit re-enters the requester before the state moves. ORACLE's
executed replay of that case (states 1 and 7; review pending) bounds the
[queue contract](../02-Resource-And-Asset-Pipeline/CONTRACT-resource-request-queue.md)'s I3 same-call drain. No shipped
script feeds the stream (§3.4), so the case is a modded-script domain.*

| state | on entry | leaves when |
|---|---|---|
| 1 | `fileBytes = 0032E400(0x24, index)`; `bufferBytes = min(bufferBytes, fileBytes)`; submit the first `bufferBytes` through `0032E780(kind, index, buffer, bufferBytes, 0)` → `requestId`; `bytesRead = bufferBytes`, `ringCursor = 0` | → 2 |
| 2 | wait until `0032E4D0(requestId)` says not in flight | → 3 → `soundHandle = 002DF660(&streamId, buffer, bufferBytes)` → 4 in the same pass |
| 4 | wait until `002DEE90(soundHandle)` returns 0 | → 5 ("ready"; `bgmstreamplay` moves it on) |
| 6 | `002DF680(streamId, 0x40, 0x7F)`; `soundHandle = 0` | → 7 |
| 7 | all read (`bytesRead ≥ fileBytes`): `002DF630(streamId)` non-zero → stay; zero → **clear `active`**. Otherwise the next piece: `min(0x10000, bufferBytes − ringCursor, fileBytes − bytesRead)` bytes at `buffer + ringCursor` through `0032E780`; `bytesRead += n`, `ringCursor = bytesRead mod bufferBytes` | → 8 |
| 8 | wait until not in flight | → 7 |

The piece size is `002DF600` — a constant `0x10000`. The sound-layer calls are thin: `002DF660`
increments a serial at `0215EFDC` and reaches `001DC2E0`; `002DF680`, `002DF630`, `002DF690` reach
`001DC280`, `001DC2C0`, `001DC330`; each fetches the audio registry (`AudioRegistry_Get`,
`00210B30`) and calls one of `00211270`, `00211230`, `00211260`, `00211280` on it. Their roles were first
read off the machine's order; **the bodies agree (2026-09-11)**: all four go to the
`StreamAudioController` (manager `+0x18`, `[registry + 0x18]`), which keeps a list of stream bank
objects keyed by `+0x38` = stream id. `00211270` → `0021D770` allocates a stream id (`00212950`),
sizes the kind-6 bank (`002129F0`), builds a bank through the controller's vtable `+0x30` and binds
the buffer to it (`002251B0`); `00211230` → `0021D6B0` finds the bank by id and starts it
(`002252C0`, with the descriptor's `0x40` and `0x7F` as its two byte parameters — `0x7F` is full
scale on the mixer); `00211260` → `0021D700` returns 1 while the bank's state (`00225680`) is not 2;
`00211280` → `0021D840` stops the bank through its vtable `+0x10`, releases it through the
controller's `+0x18` and unlinks it (or all of them for id −1), falling back to a second pool at
controller `+0x20` (`0021C870`) (`FZ-15`).

### 3.4 Why the shipped build cannot feed it — three independent zeros with controls

| claim | measurement | control |
|---|---|---|
| kind `0x24` has no paths | `ResourcePath_Init` installs the pointer slot `0215F120` → array `0215F158`, which is BSS; a whole-image RIP-relative scan finds **no other reference** to either address (`002DFB69`, `002DFB70` only) | kind 9's array `01EBF740` is `.data`, populated, and the size table carries 26 ids for it |
| kind `0x24` has no sizes | kind 36 holds **no entry in any language's `.fst`** (the size-table page's census: kinds 3, 6, 17, 18, 27, 29, 31, 35, 36, 40 empty) — state 1 would size to −1 | kind 9 holds 26 |
| no script issues the verbs | byte walk of all 1,115 `us` `.ebp` for the four call opcodes followed by `0448`–`044F` or `201E`: **0 sites** | the same walk finds the six `302B` sites the presets page records |

A modded script could still reach the verbs; the first two zeros would then have to be filled too.

### 3.5 Its one effect on the queue

`0032E620`, the request builder, asks `003EB0D0` whether the stream is active (`0032E656`). **Only
when it is** does the builder chunk the request into `0x80000`-byte parts (`0032E66B`–`0032E735`);
otherwise it falls to `0032E742` and issues the request whole. So in the shipped game **no request is
ever chunked** — the part callback and the part accounting on the queue page are code that a live
BGM stream would exercise and nothing else does.

## 4. Modding notes

- **To change an area's music ladder** edit `musicctrl.bin`: a run's default track, its rungs, or add
  a run. Keep runs sorted by start within a page and keep every page's chain contiguous — the reader
  has no terminator and no page-end bound; it relies on the next page's first start being above the
  page's last id.
- **The header's `maxFieldId` is the only bound on the last page.** Raise it past the last run and a
  lookup above that run reads whatever follows the file in the block (allocator slack, then heap).
- **Both copies must change**: the game loads `in/common/musicctrl.bin` for every language, but
  `ch/common/` exists and is identical today; leave it in step.
- ~~**The table loads once, at boot.**~~ **The table loads on the boot path.** A changed file needs a restart ~~; nothing rebinds `02B5E0D0`.~~
  *(qualified 2026-09-27: no reload was found, but the binder has no guard, and whether that path can run again is
  not established, §2.1)*.
- **Keep `maxFieldId` off a multiple of 128**, or leave the header word after the last rebased page zero (§2.2).
- **To use the BGM stream** you need a script calling `usebgmstream` / `bgmstreamread` /
  `bgmstreamplay`, a kind-`0x24` path array (nothing fills `0215F158`), and `.fst` sizes for it.

## 5. What is not known

- [x] ~~What a track id indexes — the sound bank or stream list the number selects.~~ **ANSWERED
      2026-09-11** — `PS2Data/sound/music/magi_data/win/music<id>.win.mab`, through the Music
      controller ([the music page](how-the-music-changes-when-you-change-area.md), *DG-2 answered*). `DG-2`.
- [x] ~~The four sound-layer entry points `00211270` / `00211230` / `00211260` / `00211280` (take
      the buffer, start, still playing, close — inferred from the machine's order).~~ **ANSWERED
      2026-09-11** — read in §3.3: bind a stream bank, start it, poll its state, stop and unlink it.
      ~~What `0x40` and `0x7F` set on the bank (`002256F0` / `002257E0`) is not named. `FZ-15`.~~ *(Answered from the setters, 2026-10-01, OPUS: `002256F0` takes `0x40` as the pan, `(v - 0x40) / 128` = 0, centre (`00225750`); `002257E0` takes `0x7F` as the volume, `127 / 127` = 1.0 (`0022581F`); both fade over `r8 / 60` s, 0 here. `FZ-15`.)*
- [x] ~~The rest of the queue's read plumbing named on the queue page: the four-state tick `0046DD50`
      over `02CA6068`, the status word, and `003E9780` / `003BB790` after each pass.~~ **ANSWERED
      2026-09-11** on [the queue page](../02-Resource-And-Asset-Pipeline/the-resource-request-queue.md) §8
      (the word is `0215EFF4`; the tick is dormant; the two passes are named, one of them opening `FZ-18`). `FZ-14`.

## 6. Evidence

| claim | evidence | tier |
|---|---|---|
| `02B5E0D0` is loaded by `0051ED10(9, 0x20, 003EAB90)` from `003EAB60`, whose caller is `00379D20`'s tail jump from `0022A433` | `003EAB60`–`003EAB83`; `00379D20`–`00379D32`; `0022A433`; whole-image callers of `003EAB60` (one, the `jmp`) | 1 |
| `0051ED10` sizes, allocates on heap 5 and queues the read with `0051EDB0` as the done callback and the caller's callback as the `+8` word | `0051ED2B`–`0051ED89`; `0051EDB0`–`0051EDB3`; `0032E34C`–`0032E34F` | 1 |
| kind 9 index 32 is `in/common/musicctrl.bin` | array `01EBF740` entry 32 → `00961CF0` | 1 |
| `003EAB90` adds the block's low 32 bits to every non-zero page word | `003EAB9A`–`003EABD4` | 1 |
| the file's layout and census | the extracted file walked under the reader's decoding (corpus block) | 1 |
| the descriptor's fields and constants | `003EB050`–`003EB09D` (init), `003EB100`–`003EB142` (read), `003EB180`–`003EB18D` (buffer), `003EADE0`–`003EAFE9` (machine) | 1 |
| the verb bindings | [the verb table](../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv) rows `0448`–`044F`, `201E`; handler bodies `003557C0`, `00354690`, `00354920`, `003EB150`, `003EADC0`, `003EB010`, `00355FB0`, `0050C7F0` | 1 |
| the pump serves the stream first | `0032E0BD`–`0032E0C4`, `0032E29B` | 1 |
| chunking happens only while the stream is active | `0032E656`–`0032E665` (`je 0032E742`), `0032E742`–`0032E759` | 1 |
| the three zeros | RIP scan over `0215F118`–`0215F128`; the `.fst` census; the script byte walk — each with the positive control in §3.4 | 1 |

## 7. Related

- [`how-the-music-changes-when-you-change-area.md`](how-the-music-changes-when-you-change-area.md) —
  the reader `003EAA70` and the ladder semantics; this page supplies the file it reads.
- [`CONTRACT-field-music-selection.md`](CONTRACT-field-music-selection.md) — the reconstruction
  contract for the reader; its "what fills the table" row is answered here.
- [`../02-Resource-And-Asset-Pipeline/the-resource-request-queue.md`](../02-Resource-And-Asset-Pipeline/the-resource-request-queue.md)
  — the queue that delivers the file and ticks the stream.
- [`../04-Actor-Entity/Actor-Names/the-npc-name-dictionary.md`](../04-Actor-Entity/Actor-Names/the-npc-name-dictionary.md)
  — the sibling kind-9 table loaded by the same boot function.
- [`Audio-Boundary/how-a-sound-request-becomes-a-voice.md`](Audio-Boundary/how-a-sound-request-becomes-a-voice.md)
  — the audio registry the stream's four calls go through.

## 8. Falsification pass 1 — 2026-09-13 (OPUS)

*(Static only — the shipped archive read never written, and the shipped image. Nothing executed and
no audio played.)*

### ✔ Every published figure reproduces, and the walk closes on all eleven pages

| claim | measured |
|---|---|
| two copies, **1,615 B**, byte-identical | **two**, both 1,615 B, **one SHA-256** |
| `"MUS0"`, `maxFieldId` **1311** | **exactly** |
| the eleven page offsets | **52, 106, 260, 491, 628, 790, 1024, 1227, 1329, 1463, 1571** — all eleven |
| runs per page **12, 28, 39, 29, 30, 33, 35, 18, 29, 27, 11** | **all eleven, and 291 in total** |
| every page's chain ends **exactly** at the next page's offset | **eleven of eleven**, the last at end of file |
| the first run start of each page | **12, 129, 253, 380, 517, 640, 767, 898, 1009, 1153, 1283** |
| the last run is start **1311**, span **0**, meeting the header's maximum | **exactly**, and **no run's start exceeds 1311** |
| **0 of 1,115** `us` scripts call `0448`–`044F` or `201E`, with the `302B` walk as the control | **0 for all nine ids; the control finds exactly six** |

### ➕ The decoding note is missing the widths — supplied here from the reader

§*Corpus validation* gives the decoding as *"`start = w & 0x7FF`, `span = w >> 11`, stride
`4 + 3 × count`"* and **never says what `w` is or where `count` comes from**. Beside a `>> 11` the
natural reading is that `w` is the dword at the run and `count` is one of its fields; **it is not**,
and a walk built that way collapses on the first page. `003EAA70` says it plainly:

```asm
003EAAA5  movzx ecx,  byte ptr [rax]        ; b0
003EAAA8  movzx edx,  byte ptr [rax + 1]    ; b1
003EAAAC  movzx r10d, byte ptr [rax + 2]    ; the COUNT, a byte of its own
003EAAB1  shl   edx, 8 ; add edx, ecx       ; w = b0 | (b1 << 8)   -- a u16
003EAAB8  shr   edx, 0xB                    ; span
003EAABB  and   ecx, 0x7FF                  ; start
...
003EAACB  lea   edx, [r10 + 2]              ; count + 2
003EAACF  lea   edx, [r10 + rdx*2]          ; count + 2*(count+2) = 3*count + 4
003EAAD3  add   rax, rdx                    ; the advance
```

```struct MusicCtrlRun base=run
+0x00  u16  packed     start = bits 0-10, span = bits 11-15
+0x02  u8   count      the run's entry count; the reader's advance is 3*count + 4
+0x03  ...             count entries of 3 bytes
```

**With the widths, the walk reproduces to the run**; without them it cannot be reproduced at all.
The measured distributions are `count` **0 in 243 of 291** (max 6) and `span` **0 in 169** (~~max 5~~ max 22, *corrected 2026-10-01, OPUS, re-walking the shipped file; §2.3 had it right*) —
a 5-bit span field, consistent with the `u16` split and with nothing larger ever appearing.

> **Recorded because it cost two attempts.** The figures on this page are right; the note that lets
> a reader re-derive them was one sentence short, and the missing sentence is the one that says how
> wide each field is.

**Not claimed.** §2.1 onward — the boot loader chain, the rebase callback, the descriptor and the
whole BGM-stream half — was **not re-read**; this pass re-measured the file, the walk and the script
negative. What a run's three-byte entries hold. Nothing executed.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL.*

- **Presentation — CLIENT.**
  - The music call `002DEE90` is also made by three Presentation bodies (271, 297 and 1,073 bytes).
  - `0032E070` calls a 297-byte Presentation body.
  - `0032E4D0` is read by two Presentation bodies (54 B and 247 B).
- **Input — SERVICE and CLIENT.**
  - `002DEE90` and `0032E070` call an 8-byte Input-filed getter, and `0032E070` also calls a 251-byte one.
  - `0032E4D0` is read by a 625-byte Input body.
  - The retracted 4-byte getter `00225680` is read by a 25-byte Input helper.
  - The boot initialiser calls the 119-byte Input initialiser and the AddMotion loaders.
- **Presentation — MECHANICAL.** The arena entry `0036A190` has 17 Presentation callers. The file-request family (`0032E400` size probe, `0032E620` request, `0032E520`, `0032E4D0`, `0032E070`) is shared: its **Presentation** callers (119 B and 337 B bodies), the **Input**-filed item-graphics loader (177 B) and script-verb bodies are CLIENTS, not audio dependencies.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — CLIENT and SERVICE.** A cited per-frame body is called by `MainLoop_UpdateAndRenderFrame`, a core frame body, both boot-mode bodies and the start-up subtree's root. The start-up root also calls three other cited bodies, and a cited body reads an 8-byte core getter.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAction — CLIENT.** `FUN_002fc3c0`, owned by that layer, calls `0032E4D0` on this page. That caller is a 183-byte dispatcher: `byte[rec+0x23] & 0xF`, bounded to 7, into an eight-entry jump table; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — SERVICE.** `003BB790` on this page calls `FUN_003ba7b0`, owned by that layer. What it reaches is a 402-byte state machine on `[02B40E14]`, bounded at **`0xF`** into a sixteen-arm jump table, whose first arm resets the state to 1 and clears `[02B40EC0]`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Platform — SERVICE.** `005CD4F0`/`005CD820` — the critical-section enter/leave pair the measured `00220CE0` scoped-lock getter brackets — are also called by `0019CC50`, a Platform-domain body. The lock pair is shared CRT/runtime plumbing: the crossing is that Platform uses it, not that this page owns anything in Platform.

**Save_Load_Settings — MECHANICAL (SWE2-EC7-160, 5 edges).** `00225580` is called by `005812B0`/`005817D0`/`00581930` and `0032E620` by `0058xxxx` — Save_Load_Settings bodies reaching this page's BGM helpers. Shared-helper fan-in, not a save relationship the music control file owns.
- **ActorEntity - CLIENT and SERVICE (12 edges).** `0032E400`, `0032E620`, `0036C660` are also called by bodies filed to actor entity: `00330310`, `002628B0`, `0032FCA0` (+2 more); `0022A0B0` reaches bodies filed to actor entity: `002368D0` - shared machinery across the layer boundary, no shared ownership.
- **RNG_Random_Selection - SERVICE (1 edge).** `0022A0B0` reaches bodies filed to random selection: `00379CF0` - shared machinery across the layer boundary, no shared ownership.
- **Resource - CLIENT and SERVICE (124 edges).** `005CD4F0`, `005CD820`, `0032E620` are also called by bodies filed to resource: `003EADE0`, `0032E070`, `00384420` (+39 more); `0032E070`, `0022A0B0`, `00379D20` reach bodies filed to resource: `0032E400`, `0051ED10`, `0046DFE0` (+23 more) - shared machinery across the layer boundary, no shared ownership.
- **World - CLIENT and SERVICE (6 edges).** `00314D40`, `0032E400`, `0032E620` are also called by bodies filed to world: `00378540`, `00266D10`; `0022A0B0` reaches bodies filed to world: `00266D10` - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT and SERVICE (24 edges).** `0036C660`, `0032E400`, `0036A190` are also called by bodies filed to world area: `00268750`, `00378030`, `003EA820` (+9 more); `003EAA70` reaches bodies filed to world area: `00265270` - shared machinery across the layer boundary, no shared ownership.
## The `002DF690` exclusive subtree — all 5 members bound (SWE2-FRONTIER, followup queue)

`002DF690` — the `bgmstreamstop` close ~~this page's state 6 names~~ (§3.2; state 6 calls `002DF680` - *corrected 2026-10-01, OPUS*) — is a 5-byte thunk to
`001DC330`. It owns **5 frontier functions**; every member was disassembled from the
shipping image and each interior cite sits inside its declared extent. The chain §3.3
sketches confirmed in full: `001DC330` fetches the audio registry (`00210B30`) and tails
`00211280(registry, streamId)`; `00211280` tries the controller's `+0x18` list first
(`0021D840`) and falls back to the `+0x20` pool (`0021C870`) only when the first returns
false.

| member | role | interior |
|---|---|---|
| `001DC330` (28 B) | the adapter: `00210B30()` (AudioRegistry_Get) then tail `00211280(registry, id)` | [`001DC33D`](../_index/ADDRESS-INDEX.md) |
| `00211280` (50 B) | two-list dispatch: `0021D840([rcx+0x18], id)`; when it returns false, `0021C870([rcx+0x20], id)` | [`0021129C`](../_index/ADDRESS-INDEX.md) |
| `0021D840` (215 B) | the intrusive-list remove-by-id over the `+8` sentinel list (elements at node `+0x10`, key `[elem+0x38]`): per match — `[elem].vtable+0x10` (stop), controller `[r14].vtable+0x18` unlink callback, node splice, then `[r14+0x18].vtable+0x18` free; `id == -1` unlinks **all** with size arg `+0x19→0x18` | [`0021D8AF`](../_index/ADDRESS-INDEX.md) |
| `0021C870` (85 B) | the fallback pool's broadcast-stop walk: same list shape; per element `00225000(elem, id)` and exits early on its true; `id == -1` calls `00225030(elem, -1)` instead | [`0021C894`](../_index/ADDRESS-INDEX.md) |
| `00225000` (47 B) | the per-element stop: `00221ED0()` non-null → `007A84A0(obj+8, float@008C5F6C, -1)` — a fade-out stop with a fixed constant — returns 1; null → 0 | [`0022500E`](../_index/ADDRESS-INDEX.md) |

`00210B30`, `00225030`, `00221ED0` and `007A84A0` are shared callees with other callers —
deliberately not census members.

## The `002DF630`/`002DF680` exclusive subtrees — 8 members bound (SWE2-FRONTIER, followup queue)

The state machine's other two stream verbs are the siblings of the `002DF690` stop
family — the same `00210B30` registry fetch, the same `[+0x18]` primary bank list, the
same `+0x38` element id. `002DF680` is the **start** the state 6 row names and
`002DF630` the **still-playing poll** state 7 spins on. All bodies re-disassembled from
the shipping image; every cite is interior to the named extent.

**`002DF680` — start (`streamId, 0x40, 0x7F`).** The 5-B thunk tails `001DC280`
(58 B — registry fetch + arg shuffle, `001DC296`–`001DC2B5`), which tails `00211230`
(33 B): the primary list is `[registry+0x18]` (`00211236`), `r9` is masked to
`0x7F` (the volume byte) and `r8` to a byte (`0021123A`–`0021123E`) before
`0021D6B0` runs. `0021D6B0` (71 B) walks the bank list and exact-matches
`element+0x38 == streamId` — no `−1` wildcard here, a start targets one bank —
then calls `002252C0` (`0021D6EA`). `002252C0` (265 B) builds the voice:
`00221E00(elem, 0, 0)` resolves the sound object; if `00225680` reports status 1 the
stale voice is reset through `007A7010`/`007A7A20` (`002252FB`–`00225322`), otherwise
the configure ladder runs — `002257D0`, `00225580(arg2)`, `00225590(1)`,
`002256E0(6)`, `00221C70(elem, obj, 0)`, ~~`002256F0(arg4 = 0x7F, the volume)`,
`002257E0(arg3 = 0x40)`~~ `002256F0(arg3 = 0x40, the pan: (v - 0x40) / 128, centre)`, `002257E0(arg4 = 0x7F, the volume: v / 127 = 1.0)` *(corrected 2026-10-01, OPUS: `002252DA mov ebp, r8d` / `00225367 mov edx, ebp` feeds the pan setter, `002252E5 mov esi, r9d` / `00225374 mov edx, esi` the volume setter)* (`00225327`–`00225379`) — then `007A78B0` starts playback
and on success `00225590(2)` marks it and the element's vtable `+0x50` attaches the
voice (`0022538C`–`002253AB`).

**`002DF630` — still-playing poll (`streamId`).** The thunk tails `001DC2C0`
(28 B — registry fetch, `001DC2C8`–`001DC2D7`), which tails `00211260` (9 B —
`rcx = [registry+0x18]`, `00211262`). `0021D700` (103 B) walks the list calling
`002253D0` on each element whose `+0x38` matches — or every element when the id is
0 (`0021D724`–`0021D72B`) — returning 1 on the first hit. `002253D0` (44 B)
resolves the element's voice through `00221E60(elem, 0)` and reports
`00225680(voice) != 2` (`002253D6`–`002253F0`) — so a non-zero return means "a
matching bank holds a voice that has not reached state 2", which is exactly the
poll the state 7 row waits on before clearing `active`.

| member | role | interior |
| --- | --- | --- |
| `001DC2C0` (28 B) | registry adapter for the poll | [`001DC2D2`](../_index/ADDRESS-INDEX.md) |
| `00211260` (9 B) | selects the primary list `[+0x18]`, tails `0021D700` | [`00211262`](../_index/ADDRESS-INDEX.md) |
| `0021D700` (103 B) | any-match scan: `+0x38` element key, id 0 matches all | [`0021D72F`](../_index/ADDRESS-INDEX.md) |
| `002253D0` (44 B) | voice status ≠ 2 predicate via `00221E60`/`00225680` | [`002253EA`](../_index/ADDRESS-INDEX.md) |
| `001DC280` (58 B) | registry adapter for the start (3 args) | [`001DC2A1`](../_index/ADDRESS-INDEX.md) |
| `00211230` (33 B) | masks `r9` to `0x7F`, `r8` to a byte, dispatches `0021D6B0` | [`00211244`](../_index/ADDRESS-INDEX.md) |
| `0021D6B0` (71 B) | exact-id list walk → `002252C0` | [`0021D6D4`](../_index/ADDRESS-INDEX.md) |
| `002252C0` (265 B) | the start: resolve/configure/`007A78B0`-start/attach | [`00225351`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00210B30` (registry), the `00221xxx`/`00225xxx`
voice helpers, `007A7010`/`007A78B0`/`007A7A20` (~~the XAudio-side calls~~ SEAD handle-level driver calls that queue commands to the sound thread; the backend is WASAPI - *corrected 2026-10-01, OPUS*), and the
element vtable `+0x50` attach. The list shape — head at `+8`, node links at `+0`,
element at `+0x10`, id at element `+0x38` — is the same structure the `002DF690`
stop family walks.


## Interior citation — frontier hub `002DEE90` (2026-09-18, SWE2-EC7)

`002DEE90` — 83 B, 16 callers (5 A-measured); the wait-until-done poll this page's
`bgmstreamstop` arm already names. Interior verified: a negative `ecx` arms the pump —
`0035E810` guards the section (`002DEEA1`), `001DBD00(edi)` is the status query
([`002DEEA8`/`002DEEBC`](../_index/ADDRESS-INDEX.md)) retried in a loop with `0035EA30(0)`
yields between attempts (`002DEEB3`–`002DEEC5`), then `0035E810` releases. A non-negative arg
skips the wait and tail-calls `001DBD00` directly (`002DEEDE`). Returns the last status.

## SWE2-EC7-42 update (2026-09-19) - `00225030`

`00225030` (297 B) is a music-control body - `00222080`/`00221770` triple/`00861EBA` pair/`002255B0`/`007A88F0`/`00809950`. Interior anchor `0022503F` (a `00222080` call).

## SWE2-EC7-48 update (2026-09-19) - `002251B0`

`002251B0` (199 B) is the music-bank start body - `00220D40`/`00221710`/`00221D10`/`00225580`/`00225590`/`002255A0`/`00225CC0`. Interior anchor `002251CF` (a `00220D40` call).

## SWE2-EC7-48 update (2026-09-19) - `0021D770`

`0021D770` (200 B) is a body - `00212950`/`002129F0`/`00212A70`/`002251B0` plus a `call [rax+0x30]` vcall. Interior anchor `0021D7B6` (a `00212950` call).

## SWE2-EC7-61 update (2026-09-19) - `00221C70`

`00221C70` (152 B) is the `00221C70(elem, obj, 0)` bank-path body the music page names - `0016D6A0`/`00220CE0`/`00221710`/`002256A0`/`007A87C0`. Interior anchor `00221C9F` (a `00221710` call).



## SWE2-EC7-65 update (2026-09-19) - `003EAD10`

`003EAD10` (135 B) is a music-control body - `0016D6A0`/`002DEE90`/`002DF690`/`0032E520`/`0035EA30`. Interior anchor `003EAD41` (a `0032E520` call).


## SWE2-EC7-77 update (2026-09-20) - `00220CE0` scoped-lock getter measured

`00220CE0` (79 B) is the `+0x300`-locked fetch: `005CD4F0(rcx+0x300)`
enters, `002204A0(rcx+8)` fetches the value, `005CD820` releases -
the audio object's locked accessor shape.
Interior anchor `00220D06` (the `005CD4F0` lock call).

## SWE2-EC7-108 update (2026-09-20) - `00221E60` measured

`00221E60` (108 B) is the twin
find `00221E00` and `002253D0`
call (9 edge callers total): the
same `rcx + 8` sentinel /
`[+8]`-link / `[+0x10]` payload
walk, keyed by `002256A0(payload)
== edx` instead of `00879750` -
the sibling lookup to `00221ED0`
on the music-control lists.
Interior anchor `00221E9F` (the
`002256A0` call).

## SWE2-EC7-113 update (2026-09-21) - `00862600` measured

`00862600` (31 B) is the
two-out-parameter read
`003BB790` runs: a non-null
`rdx` gets zeroed, a
non-null `r8` gets
`dword[02EAF8E0]` copied
out, and 1 returns - the
same global `00862620`
writes, exported read-only.
Interior anchor `00862610`
(the `02EAF8E0` read).

`003BB790` (400 B) is the command dispatcher `0032E070` calls: `02B40E10` selects the mode; mode 1 runs `00862600` for a code in `[rsp + 0x30]`, then `ebx + 0x13 <= 8`, `ebx + 0x4F <= 0x27` and `bt 0xFFFFF003FF` pick the range arm run by `003BA7B0`/`003BA990`/`003BAEB0`/`003BAC90`/`003BA5F0`/`003BA720`/`003BA680` - the BGM code-range dispatch.

Interior anchor `003BB7B2` (function `003BB790`).

`003BB920` (144 B) is the command post `00582040` makes on this page's `02B40E10` block: the busy flag refuses with 0, `r9d` must be non-zero, then it byte-copies `rcx`'s string into `02B40EC8`, stores `r8`/`r10d`/`r9d` at `02B40EF0`/`+0xC`/`+0x8`, sets `02B40FE0` = 1 and `02B40E1C` = 2, raises `02B40E10` = 1, calls `003BAEB0` and returns 1 - the enqueue half of the control file's chain.

Interior anchor `003BB950` (function `003BB920`).

`003BA720` (143 B) is the consume/release `003BB790`'s dispatcher runs on the same block: gated on `02B40E14`, `003BA3E0` snapshots `02B40E28` into the out record, then `ecx` is clamped against `02B4054C` - the remainder writes `02B4054C`, `02B40E14` and `02B40E10` are released and `dword[02B40540 + 0x284 + idx*8]` takes the result code; the over-budget arm writes 0 there instead - the dequeue-and-account half.

Interior anchor `003BA778` (function `003BA720`).

## Homed bodies: functions reached only indirectly whose callees this page cites (OPUS, 2026-10-02, F homing)

*No page cited these functions and none of their callers is documented: they are reached by table or pointer dispatch or through undocumented callers. Each one calls something this page documents, which the sentence names. Each sentence states what the body does (access and representation, not purpose); the anchors are instructions inside it that do it. Drafted locally and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../_index/candidates/opus-the-music-control-file-and-the-bgm-strea-homing-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00224890` | 111 B | when `edx` is 0 stores 0 to the dword at absolute address 0 (a deliberate fault) and returns `al` = 1; otherwise calls `00221ED0` with the incoming registers and, when it returns an object for which `00225680(object)` is non-zero, calls `007A77F0(object+8, float [r8], float [r8+4], float [r8+8])` and returns 1, else 0 | `00224899`, `002248A2`, `002248B2`, `002248CD`, `002248EC` |
| `0050CEC0` | 43 B | calls `0017D280` with the address `00D22968` and what `0035E810()` returns, then `0016D6A0(1)`, and tail-jumps to `0016D6A0` again without reloading `ecx` | `0050CEC4`, `0050CED3`, `0050CEDD`, `0050CEE6` |

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../_index/candidates/opus-the-music-control-file-and-the-bgm-strea-cloudint-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00220D40` | 82 B | calls `005CD4F0(rcx+0x350)`, then `00220600(rcx+0x1d0)`, then `005CD820(rcx+0x350)`, and returns the result of `00220600` | `00220D57`, `00220D66`, `00220D73`, `00220D7E`, `00220D84` |
| `002255B0` | 9 B | stores `rdx` to qword `+0x20` and `r8` to qword `+0x28` of `rcx` | `002255B4` |
| `00225CC0` | 9 B | stores `rdx` to qword `+8` and `r8d` to dword `+0x10` of `rcx` | `00225CC4` |
| `0032E780` | 44 B | returns -1 when `edx` is negative (signed); otherwise returns `0032E870(rcx, edx, r8, r9, the fifth (stack) argument, 0)` | `0032E786`, `0032E788`, `0032E790`, `0032E795`, `0032E7A2` |
| `00354690` | 33 B | calls `003EB100(00267E10(r9))` and tail-jumps to `00314D40(1)` | `00354694`, `00354697`, `0035469E`, `003546AC` |
| `003557C0` | 43 B | with `n` = `00267E10(r9)` it calls `003EB010()`, then tail-jumps to `003EB180(003EACA0(n), n)` | `003557C9`, `003557D0`, `003557D7`, `003557E6` |
| `003EB010` | 58 B | returns at once when qword `02B5E0E8` is null; otherwise calls `003EAD10(02B5E0E0)` and `003697F0(qword 02B5E0E8)`, then zeroes qword `02B5E0E8` and dword `02B5E0F0` | `003EB01C`, `003EB025`, `003EB031`, `003EB038`, `003EB03F` |
| `003EB0A0` | 34 B | returns 1 when byte `02B5E111` is non-zero and byte `02B5E110` is neither 0 nor 5, else 0 | `003EB0A7`, `003EB0A9`, `003EB0B4`, `003EB0B9`, `003EB0BF` |
| `003EB150` | 35 B | does nothing when byte `02B5E111` is 0; otherwise stores 6 to byte `02B5E110` when it holds 5, and stores its own value back otherwise | `003EB157`, `003EB165`, `003EB169`, `003EB16C` |

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted, opus-the-music-control-file-and-the-bgm-strea-ee-1003)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../_index/candidates/opus-the-music-control-file-and-the-bgm-strea-ee-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `003BA5F0` | 135 B | switches on dword `02B40E14`: 0 stores 1 there and 0 to dword `02B40EC0`; 1 calls `00862130(byte [02B40E20], 02B40E3E)` and stores 0xc to `02B40E14`; 12 tests `ecx` and, when `ecx` is 0 or -4 (`ecx`+4 with bit `0x4` masked off is zero), zeroes the qword at `02B40E14` and the dword at `02B40E10`, otherwise stores 9 to dword `02B40E18` and zeroes the qword at `02B40E10`; any other value returns without writing | `003BA5FC`, `003BA60B`, `003BA62C`, `003BA64C`, `003BA662` |
| `007A7A20` | 231 B | returns `0x82000000` when qword `[rcx]` is zero; when its low byte is 2, 8 or 9 it calls `007AB460(rsp+0x20)` and, if that is not negative, writes 0xd to dword `[p]`, qword `[rcx]` to `[p+8]`, `xmm1` to float `[p+0x10]` and `r8d` to dword `[p+0x14]` of the returned record `p` and returns `007AB550(p)`; when the low byte is 7 it calls `007BAD60(rsp+0x20)` and, if that is not negative, writes 0x10, qword `[rcx]` and `xmm1` to `p`, `p+8` and `p+0x10` and returns `007BAE50(p)`; a negative result from either first call is returned as is, and any other low byte returns -1; the stack cookie is checked through `00808C40` | `007A7A59`, `007A7A6E`, `007A7A9D`, `007A7AAE`, `007A7AE5` |
| `007A88F0` | 243 B | calls `007B24F0` with the incoming registers to get `h`, calls through `008C20B8` with `h` and calls `007B2470` with a stack copy of qword `[rcx]`; when that returns null it calls through `008C20C0` with `h` and returns 0, otherwise it calls `007D0A10` with the returned pointer, calls through `008C20C0` with `h`, and when `dl` is non-zero returns the `eax` of `007D0A10`; when `dl` is zero it repeats the `008C20B8`, `007B2470`, `008C20C0` sequence, calling through `008C21B0` with 1 after each lookup that returns non-null, and returns 0 once a lookup returns null | `007A8923`, `007A8930`, `007A8950`, `007A8963`, `007A899A` |
