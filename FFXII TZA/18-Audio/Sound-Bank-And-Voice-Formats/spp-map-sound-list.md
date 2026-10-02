---
system: .spp / SPP1 — the map sound list that mapsoundplay, the map's sound emitters and its weather ambience index
category: 18-Audio
status: AUDITED
owner_layer: PrimaryOwner:Audio
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 33 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
corpus_validated: "546 / 546 SPP1 lists (1 loose .spp + 545 .mpk slot 10), SeSep walk replayed exactly, 2026-09-13"
last_reviewed: 2026-09-13
archive_formats:
  - "spp"
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-spp-map-sound-list-pass-1 - all 546 lists re-derived from the archive with independent code; every corpus figure exact; the three id bands are exhaustive with extents 1001-1185, 10002-10313, 50001-50268 and 632 distinct ids
  crossref_clean: false        # 2026-09-30 (SWE2-DATA): false until the pass-22 UNACCOUNTED NEIGHBOUR findings are accounted (FRONTIER-REQ-SWE2-DATA-PASS22-DEBT; OPUS-REQ-DATA-PASS30-CROSSREF-CLEAN-0930)
  reopened_count: 0
---

# `.spp` / `SPP1` — the map sound list

> A header, a list of sound-effect ids, and a small per-weather table. The field's map pack carries one in
> slot 10 next to its `SeSep` bank in slot 0. Binding it registers every bank chunk; afterwards three
> things index the list by position: the script verbs `mapsoundplay(i)` / `mapsoundplay_2bb(i, …)`, the
> map's positional sound emitters, and the weather ambience, which picks one entry per weather slot. The
> one loose `.spp` file, `env99.spp`, is the same format with the bank embedded after the list.

**Corpus validation.**

| | |
|---|---|
| lists examined | **546** — the 1 loose `.spp` and slot 10 of all 545 `.mpk` that have one (every one also has slot 0) |
| magic `SPP1` | **546 / 546** |
| the `SeSep` walk with `+0x08` as its length ends with fewer than 16 bytes left | **546 / 546** |
| the chunk ids the walk registers are the listed ids, in order | **546 / 546** |
| ids per list | 1 … 48 |
| id ranges | 10000–19999: 3,398 · 50000–59999: 2,110 · 1000–1999: 1,015; bit 31 never set — **and those three are the whole population, with tighter real extents: `10002`–`10313`, `50001`–`50268`, `1001`–`1185`; 632 distinct ids in 6,523 references (§9)** |
| `+0x18` = the id list's end rounded up to 16, and the bytes from there to the next table are zero | **546 / 546** |
| weather table present (`+0x1A` ≠ 0) | 545 (all packs); entries 3 in 226, 1 in 189, 2 in 130; 1,115 indices in range, 12 are `-1` |

Census: [`census.py`](../../_experiments/evidence/spp-map-sound-lists/census.py) →
[`census.out.txt`](../../_experiments/evidence/spp-map-sound-lists/census.out.txt) (ties sorted; two runs
byte-identical).

---

## 1. What the player sees

**The sound effects a field can make, numbered for that field.** A zone script does not name a sound id; it
calls `mapsoundplay(n)` (3,838 calls in the shipped `us` scripts, 2,106 of them
`mapsoundplay(mp_map_set_hitse)`) and the engine plays entry `n` of the current map's list. The map's placed
sound emitters refer to the same numbering, and **the looping ambience changes with the weather**: the list
names one entry per weather slot, and a weather change switches to that entry's sound (§3). The sound data
travels in the same pack as the list, so entering a field loads exactly these effects and leaving unloads them.

## 2. The layout

```struct Spp1Header base=file size=0x20
+0x00  u32       magic        'SPP1' (53 50 50 31); no reader compares it
+0x04  u32       count        ids at +0x20; 1..48
+0x08  u32       bankLength   byte length handed to the SeSep walk 002DF070
+0x0C  u32       bankOffset   the bank's offset from the list when no separate bank is supplied; = +0x1A + 16 in every pack list
+0x10  u16       hasMapNo     1 when +0x12 carries a MapNo (386), 0 with +0x12 = 0xFFFF (160); no reader found
+0x12  u16       mapNo        the zone's MapNo — the planmapname.bin / navimapdata.bin index space; constant across every .mpk of a zone family (verified by name join, §7); no reader found
+0x14  u32       zero14       0 in 546
+0x18  u16       reservedAt   = (0x20 + 4*count + 15) & ~15 in 546; the bytes it points at are zero in 546; no reader found
+0x1A  u16       weatherAt    offset of the weather table; 0 in the loose file (the SP1 block's table is used instead)
+0x1C  u32       zero1C       0 in 546
```

```struct Spp1Id base=file+0x20 size=0x04
+0x00  u32       soundId      one per entry; bit 31 selects the voice class in 002DF010 / 002DEF40 and is never set
```

```struct Spp1WeatherTable base=file+weatherAt size=0x10
+0x00  u16       n            1..3 in the packs
+0x02  i16[7]    entryIndex   index into the id list per weather slot; 00363B40 reads at most 3; -1 = no ambience
```

A pack's slot may run 0, 16, 32 or 48 bytes past `+0x0C`. The loose file has no weather table and puts its
`SeSep` bank at `+0x0C` (`0x70`). The bank is the `SeSep` chunk container of
[the sound request page](../Audio-Boundary/how-a-sound-request-becomes-a-voice.md): 16-byte-aligned chunks
`{'SeSe', 'p', …, +0x08 id, +0x0C size | bit 31}`, the chunk data at `+0x10`.

## 3. The loader contract

**Binding.** When the map pack binds its sound (bind bit 0 in `003775D0`,
[the map pack](../../03-World-Area-Field/Map-Pack/the-map-ctrl-pack.md) §3.4), `003635E0(list, bank, handle)`:

1. unbinds any previous list (`00363750`, below);
2. takes `bank` if it is non-null, else `list + [list + 0x0C]` (`00363602`–`0036360D`);
3. walks the bank with length `[list + 0x08]` (`00363627` → `002DF070`), which rounds the length up to 16 and,
   while more than 16 bytes remain, checks `SeSe` + `p` (`002DF090`–`002DF0A4`), stops when a chunk is larger
   than what remains (`002DF0AF`), and registers the chunk through `001DBE60(id, data)`;
4. frees the pack's bank block if one was given (`0036363F` → `003697F0`);
5. stores `handle` at `022CBA88` and the list at `022CBAF8` (`00363657`, `00363662`).

**Script playback.** `mapsoundplay` (verb `0x02BA`, `00346260`) pops `i` and, if a list is bound and
`i <u count` (`00346291`), plays `id[i]` through `002DF010` unless `00267310(byte [ctx + 0x15])` returns
non-zero. `mapsoundplay_2bb` (`0x02BB`, `00346990`) pops three values — the third is `i` — and plays `id[i]`
through `002DEF40(id, second, first)` under the same bound (`003469D5`).

**Emitters.** `003638B0`, called for each emitter record by `003631B0` (which walks the pack's slot-16 `SP1`
block at `022CBAF0`), reads the record's first dword as a list index; for `0 <= index < count` and a
non-negative id (`0036397F`–`00363996`) it plays the id at the record's `+0x20/+0x24/+0x28` position through
`002DEFA0` when `00229EA0(id)` returns 2. The emitter record belongs to `SP1`, not to this file.

**Weather ambience.** `00363B40` (called from `002620E0`, after `00379860(weather slot)`, `00379290` and `003DE920`) clears the
three selections at `022CBB58` and the three-entry keep list at `022CBB64` to `-1` (`00363B63`–`00363B77`), then, if the list's `weatherAt` is
non-zero, reads `n` and for slots `i < min(n, 3)` takes `entryIndex[i]`; an index in `0..count-1` whose id is
positive becomes selection `i` and is appended once to the keep list (`00363BA2`–`00363C2C`). With `weatherAt`
zero it reads the same shape — a dword count and dword indices — from the `SP1` block's `+0x04` table
(`00363C38`–`00363CD4`). It then takes the committed weather slot (`00265920`, the `getweatherslot` value,
[choosing the field environment variant](../../03-World-Area-Field/choosing-the-field-environment-variant.md))
minus one, `w`. Only `w < n` is tested (`00363C2E`–`00363CDB`), so `n = 4` with weather slot 4 would read `022CBB64`, the keep
list's first entry, as a selection — shipped tables have `n <= 3`. A selection that exists and is non-negative becomes the current ambience `022CBA7C`: handed to
`00363840` when `022CBB2D` is set, otherwise, when a sound is active (`022CBA70`), the current one gets
`002DF190(current, 0xF)` and the new id is recorded, else `003636A0` runs (`00363CF4`–`00363D85`). Without such a
selection the current id gets `002DF190(current, 0xB4)` (`00363D9B`–`00363DD5`); with neither a weather table
nor an `SP1` block, `00363E40(0xB4)` (`00363DA3`). The units of `0xF` and `0xB4` are not established here.

**Unbinding.** `00363750` walks the list's ids (`00363774`–`003637E4`): an id in 1000–1999 that is in the keep
list stays registered; every other id is unregistered through `002DF050` → `001DBE40` (skipped for a negative
id). It then copies the selections `022CBB58`–`022CBB77` back over `022CBB38`–`022CBB57`, releases the handle
when non-negative (`002DEB40`), and clears `022CBAF8`.

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| `magic` | — | **not checked** by any reader | — | yes, in this build |
| `count` | `00363774`, `00346291`, `003469D5`, `0036398B`, `00363BE0` | an index `>= count` plays or selects nothing (unsigned in the verbs, signed after a sign test in the emitter and weather readers) | — | — |
| `bankLength` | `00363627` | — | rounded up to 16; a chunk larger than the rest stops the walk silently | — |
| `bankOffset` | `00363607` | — | — | when the pack supplies its slot-0 bank (every shipped pack) |
| `id[i]` | `00363791`, `0034629A`, `003469DA`, `00363990`, `00363BE6` | the emitter reader skips a negative id; the weather reader skips an id `<= 0` | — | — |
| `weatherAt` | `00363BA2` | 0 → the `SP1` block's table is used | — | — |
| weather `n`, `entryIndex` | `00363BD0`, `00363BD8` | an index `< 0` or `>= count` | only the first 3 entries are read | entries 4–7 |
| `+0x10`–`+0x18`, `+0x1C`, the zero table | — | — | — | **no reader found** — `+0x10`/`+0x12` are the MapNo pair (§2) and `+0x18` the zero-pad offset; all three are dead-authored on PC |

**The write path.** None — the list is used in place.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `003635E0` | bind: bank walk, list and handle store | ✅ full body |
| `00363750` | unbind: id release with the keep list | ✅ full body |
| `00363B40` | weather ambience selection | ✅ full body |
| `003638B0` | positional emitter playback | ✅ full body |
| `002DF070` | `SepBank_WalkChunks` | ✅ full body |
| `002DF050` | unregister wrapper (non-negative ids) | ✅ full body |
| `00362F60` | list getter | ✅ full body |
| `00346260` | `mapsoundplay` (`0x02BA`) | ✅ full body |
| `00346990` | `mapsoundplay_2bb` (`0x02BB`) | ✅ full body |
| `00265920` | committed weather slot (`0017D490()` if positive, else payload `+0x1060` + 1) | ✅ full body |
| `002DF010` / `002DEF40` | play by id | ✅ full bodies ([sound request page](../Audio-Boundary/how-a-sound-request-becomes-a-voice.md)) |
| `003631B0` | the `SP1` emitter walk that calls `003638B0` | ◐ the call site only |

### Data addresses

| Address | Name | Kind | Contents |
|---|---|---|---|
| `022CBAF8` | current map sound list | `.data` ptr | written by `003635E0`, cleared by `00363750` and `00362F70` |
| `022CBA88` | bound handle | `.data` i32 | `-1` when none |
| `022CBB58` / `022CBB64` / `022CBB70` | weather selections (3) / keep list (3) / keep count | `.data` | filled by `00363B40` |
| `022CBA7C` | current ambience id | `.data` i32 | `00363B40` |
| `00917290` | `SeSep` magic | `.rdata` | 5 bytes |

**The readers were enumerated, not sampled.** `tools/ripscan.py` lists ten RIP references to `022CBAF8`:
writes in `00362F70`, `003635E0`, `00363750`; reads in `00362850` and `00362DC0` (null tests only), `00362F60`
(the getter, whose two callers are the verbs), `00363750`, `003638B0` and `00363B40` (two). The pack's own
pointer `02ADD068` has five references, all in the pack loader, binder and teardown.

## 5. Corpus survey

546 lists, 6,523 ids, all distinct within their list. Counts: 5 (61 lists), 7 (60), 9 (40), 15 (38), 1 (34),
19 (30). `+0x10`/`+0x12` split the lists in two: 386 with `(1, n)` and 160 with `(0, 0xFFFF)`, the loose
`env99.spp` among the latter. The weather table's 12 `-1` entries leave a weather slot without ambience.

## 6. Falsification pass

Not yet run. Positive controls in the census: the archive index's 1 `.spp` and 550 `.mpk` entries, and the
exact replay of `002DF070` registering the listed ids in order in 546 of 546 lists. The first draft of this
sheet said no reader used the tables after the ids; the reference enumeration found `00363B40`, which reads
`+0x1A`, and the sheet was rewritten before publication.

## 7. What this document does not claim

- [x] **SQ-1.** ~~What `+0x10` and `+0x12` hold, why `+0x18` points at a zero table,~~ what the id ranges
      (1000s, 10000s, 50000s) distinguish *(the 1000s band is answered — the ambience/weather class — see below; ~~the 10000s/50000s split is not~~ — **answered 2026-09-27 (SWE2-DATA): the id is the `.sab` filename, the bands are the folders `se001`/`se010`/`se050`, and no consumer dispatches on the band — the split is an authored namespace, see the SWE2-DATA update at the end of this page**)*, ~~what `00229EA0` returning 2 and `00267310` mean for playback,~~ *(narrowed 2026-09-13 (FABLE): the two playback tests are identified. `00229EA0` takes no argument — it returns the main loop's frame mode `02064AD3` — so an `SP1` emitter plays only in the field/battle frame, mode 2 (`00363998`–`003639A0`; [what happens between two frames](../../22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md) §2.2), never behind a full menu or during capture. `00267310(manager)` returns the manager record's sub-step byte (`02099011 + slot × 0x288`), which makes the world tick run that manager's slots up to fifteen extra times in a frame ([the world tick](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md)); `mapsoundplay` skips the sound while the calling actor's manager (`[ctx + 0x15]`, `00346296`) is in that mode (`0034629E`–`003462A5`), so a script re-simulated to catch up does not fire its one-shot sounds again. `mapsoundplay_2bb` has no such test)* and whether the loose
      `env99.spp` is ever requested — its name sits at kind-1 indices 24 and 58 of `01E19670`, and the only
      constant-kind-1 request found is `debug_loadjfdata`'s (`002EF336`), but requests with a kind held in a
      register were not enumerated. `SQ-1`.
      **Narrowed 2026-09-18 (FABLE), the `env99.spp` half.* Two DATA facts and one code census. The archive holds **exactly one `.spp`**, `ps2data/sound/se/map/position_map/spp/env/env99.spp`, and **none of the 9,341 prefetch lists** under `prefetchdata/` names any `.spp` at all — every map's list arrives as `.mpk` slot 10, which is the 546-list census above — so `env99` is never prefetched with a map. The kind-1 requester is `0032E620(kind = ecx, id = edx, callback = r8, r9d)`; its **38 call sites** pass an immediate kind at fifteen of them, and `1` only at the debug site `002EF336` (the others are 2, 3, 6, 7, 8, 9, `0x1A`, `0x20`, `0x23`, `0x27`), while **23 sites take the kind from a resource-record byte or a register**: `MapRef_BeginLoadResources` `[rdi+9]` with ids `[rdi+2]` / `[rdi+4]` (`00268809`, `0026883E`), `ActorResource_BeginManagerResources` `esi` and `[rsi+0x1D]`, the boot completion `003A13F0` `[rbp+0x20]`, `00378540`'s six record-byte sites, and the rest. So the code never names kind 1 outside debug, and whether any shipped resource record carries kind 1 with index 24 or 58 is a census of those record tables, which this page has not run; until it is, `env99` is a file with a name in the kind-1 table, no prefetch, and no constant requester. DATA: the archive index and the prefetch lists; static: the requester's call sites.*
      **Corrected 2026-09-18 (FABLE), same day: the kind classification above was wrong.* A forward constant pass over every `E8` site of the requester in `.text` (51 sites, not 38) resolves the kind at 35 of them: kind 1 at **two** — the debug slot loader and `00378540`'s first request, `(1, 32)` = `planmapname.bin` (its request name string is `MapName`; the same body then asks `(9, 8)` `navimapdata.bin`, `(9, 0x27)` `gramap_weatherinfo.bin`, `(9, 0xA)` `mapjumpgroupflagrom.bin`, `(9, 0x28)` `mapjumpgroupinit.bin`, `(9, 0x29)` `eventmemorylist.bin` and `(9, 9)` `soundfoottable.bin`) — and `MapRef_BeginLoadResources`' two sites are `(9, 4)` `map_ref.bin` and `(9, 2)` `test_area_ref.bin`, constants reached by `lea` arithmetic, not record bytes. Sixteen sites take the kind from an argument or a record word (`00249210`'s family is the menu set, kind 7 at every resolved caller; `003DDA70` words `+0x10` / `+0x12`; `003DF550` words `+0x2C` / `+0x2E`; `003E9EF0`'s word table; `003A13F0`'s record dwords `+0x18` / `+0x20`; the wrappers `0032EB40`, `0051ED10`, `00330310`, `00378030`), and a data-section scan for `(1, 24)` and `(1, 58)` in those record shapes finds no record. So no constant site names `env99`, and the residue is the record-driven sixteen.*
      **Answered 2026-09-27 (SWE2-DATA): the header pair, the zero table and the bands, and the record channel traced.** `+0x10`/`+0x12` are a **MapNo pair** — `+0x10` is 1 iff `+0x12` carries the zone's MapNo, the same index space `planmapname.bin` is keyed by (`00377B60`, `u16` offset table at `+0x10`). The value is constant across every `.mpk` of a zone family (87 `plan_master/map_ctrl/<zoneNN>` families → exactly one value each), `0xFFFF` when `+0x10` is 0, and joining it to `planmapname.bin` returns real zone names — 590 "Athroza Quicksands" for `dor01`/`dor02`, 549 "Ice Field of Clearsight" for `rbn10`, 555 "Port Section" for `var01`, 539 "Walk of Flitting Rifts" for `rsn01`/`rsn52`, 506 "The Northsward" for `mic01`, 517 "City of Other Days" for `sav02`, 564 "Central Brig Access" for `rbn20`, 526 "The Switchback" for `lus01`, 532 "The Greensnake" for `gol01`; `rwg*`/`srb01`/`ztc01` carry MapNo 0 with the flag set (PLMN slot 0 is unnamed). `+0x18` is `align16(0x20 + 4·count)`, the offset of the zero pad before the weather table. **All three are dead-authored on PC** — the ten `022CBAF8` readers were re-checked and none touches `+0x10`..`+0x18`; the pair is PS2-era zone binding the port never consults. *The bands:* **the 1000s are the ambience/weather class** — every index the weather table selects is a 1000s id (1,115/1,115 in range, 12 `-1`), the loose `env99.spp` is all-1000s, and 1k chunks carry a distinct payload shape (payload byte 0 ∈ `0x82`–`0x84`, byte 4 = `0x20`; 10k/50k payloads carry byte 4 ∈ {0, 1}); what separates the 10000s from the 50000s was not pinned down. *The `env99` record channel:* the "record-driven sixteen" read their kind/id from **runtime** request records and queues, not authored tables — `003DDA70`'s `word[rbx+0x10]`/`+0x12` are filled by `003DD4C0` from the `0215FD88` drain queue (`002E65A0`), `003DF550`'s `+0x2C`/`+0x2E` are runtime record words, `003E9EF0`'s word table is a runtime descriptor reached through `002640C0`/`00267E10`, `003A13F0` pops the pending-request queue via `002ED8C0`, and `MapRef`'s two sites are constants `(9,4)`/`(9,2)` reached by `lea` on a zeroed register. No authored record table feeds `0032E620`; a kind-1 request can only come from a constant site (the debug loader, and `(1, 32)` `planmapname.bin`) or a runtime-computed value — none was found producing 1. `env99` remains a file with a name in the kind-1 table, no prefetch and no located producer; the residue is a computed-kind producer, not a record. DATA: the zone-key join and the weather/band correlation over all 546 lists; static: `00377B60`, `0032E400`/`0032E620`/`0032E870` and the producer chains above.*

## 8. Related

- [The map pack](../../03-World-Area-Field/Map-Pack/the-map-ctrl-pack.md) — slot 10 and the bind order.
- [The sound request page](../Audio-Boundary/how-a-sound-request-becomes-a-voice.md) — `SeSep` and the play functions.
- [Choosing the field environment variant](../../03-World-Area-Field/choosing-the-field-environment-variant.md) — the weather slot.
- [Sound bank and voice formats](README.md) — the folder's format plan.

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run first, one query at a time and read in full. This page was
published earlier the same day; the pass is peer review of fresh work, and the board shows its task
`FABLE-S50-SPP` DONE and committed before the claim.)*

### Every corpus figure reproduces, re-derived from the archive

The 545 packs were re-split with the `.mpk` layout from
[the map-ctrl pack](../../03-World-Area-Field/Map-Pack/the-map-ctrl-pack.md) (`+0x00 count`,
`+0x04 u32[32] size`, `roundup((count+1)×4, 0x40)` then a `0x40` header before each present slot) and
slot 10 walked with independent code — not by re-reading `census.out.txt`:

| claim | measured |
|---|---|
| **545** packs carry slot 10, and every one also has slot 0 | **545 / 545** |
| **546** lists with the loose `env99.spp` | **546** |
| magic `SPP1` | **546 / 546** |
| ids per list 1…48 | **1 … 48** |
| `+0x14` zero | **546 / 546** |
| `+0x18` = `(0x20 + 4·count + 15) & ~15` | **546 / 546** |
| bit 31 never set | **0 of 6,523** |
| `10000–19999` 3,398 · `50000–59999` 2,110 · `1000–1999` 1,015 | **3,398 · 2,110 · 1,015** |
| `+0x10` — 1 in 386, 0 in 160 | **386 / 160** |
| `+0x12` = `0xFFFF` exactly when `+0x10` is 0, else one of 46 values | **160 / 160**, and **47** distinct values in all — `0xFFFF` plus **46** others |
| weather table present in 545; entries 3 in 226, 1 in 189, 2 in 130 | **545**; **226 / 189 / 130** |
| 1,115 indices in range, 12 are `-1` | **1,127 indices, 12 of them `-1`** — 1,115 + 12 |

### ✔ Two sharpenings, not corrections

**The three id bands are the whole population, not a top three.** Bucketed by thousand there are
**exactly three** — 1000, 10000, 50000 — and they account for all **6,523** references. Read as a
top-three list the row is silently open-ended; it is closed.

**And the band labels are decade buckets, not measured extents:**

| band | distinct ids | references | actual extent |
|---|--:|--:|---|
| `1000–1999` | 144 | 1,015 | **`1001`–`1185`** |
| `10000–19999` | 257 | 3,398 | **`10002`–`10313`** |
| `50000–59999` | 231 | 2,110 | **`50001`–`50268`** |

**632 distinct sound ids are referenced by every map sound list in the game**, over 6,523 slots — and
one of them, `10293`, appears **115** times, in better than a fifth of all lists. A modder adding an
id now has the populated extents rather than the decade they sit in.

### A note on my own check, not on the page

The *"bytes from `+0x18` to the next table are zero, 546 / 546"* row reads **545 / 546** if the check
spans `reservedAt → weatherAt` and falls back to end-of-file when `weatherAt` is 0. The one file that
fails is **`env99.spp`** — the loose list, whose `weatherAt` **is** 0 and which §2 says carries **the
bank embedded after the list**. There is no next table there, so the fallback measures the bank.
**The page is right and the check needs the loose file carved out**; recorded so the next reader does
not repeat it.

**Not claimed.** What `+0x10` and `+0x12` are for — no reader was found for either and this pass
found none. Whether any `mapsoundplay(n)` in the shipped scripts indexes past its map's `count`: the
script corpus was not joined to the pack corpus here, and it is the obvious next bounds test. ~~Whether
the 632 ids resolve against a `.sab` bank's own id space — not tested~~ — **tested 2026-09-27
(SWE2-DATA): all 632 join, zero misses — the id is the `.sab` filename, `se<id/1000>/se<id>.win.sab`
(see the SWE2-DATA update below)**; the CHSE-to-`.seb` membership
test does not transfer, because these ids are not block numbers. The archive was **read, never
written**, and nothing was executed.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL.*

- **Presentation — CLIENT.**
  - The frame-mode getter `00229EA0` is read by `RenderModelInstanceContainer_ProcessActiveEn…`,
    `PresentationEntry_UpdateForCurrentGlobalPhas…` and two more bodies.
  - `002620E0` calls a 699-byte Presentation body.
  - The `SeSep` body `002DF070` is called by a 271-byte body.
  - `00267310` is read by a 511-byte body.
- **Movement — CLIENT and SERVICE.**
  - `00267310` is read by `Movement_UpdateSteeringTowardTarget` and a 935-byte body.
  - `00379290` calls a 134-byte movement helper.
  - `003DE920` is called by two movement bodies (73 B and 141 B).
- **Input — CLIENT.** `00267310` is read by the 1,002-byte Input body.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Party — SERVICE.** `00362850` on this page calls `PartyFocus_GetCurrentPackedActorHandle`, owned by that layer. What it reaches is a seven-byte getter returning the packed handle at `022C7FE0`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Save_Load_Settings — SERVICE.** `002620E0` on this page calls `SaveImage_GetPersistentPayloadBase`, owned by that layer. What it reaches is a 20-byte accessor returning `002EF640() + 0x200` - **the base the persistent flag banks are indexed off**, so those banks live inside the save payload; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

## SWE2-EC7-98 update (2026-09-20) - `002DF190` measured

`002DF190` (16 B) is the argument-shuffle `00363410`,
`00363B40` and `00363E40` call: `r9d = edx`, `r8d = ecx`,
`edx = 0`, `ecx = 1`, then tail `jmp 001DBF50` - the
(1,0)-repack into the shared sound-list helper.
Interior anchor `002DF19B` (the `001DBF50` tail jmp).

## SWE2-DATA update (2026-09-27) — the bands are `.sab` folders; the split is namespace, not dispatch

**The id is the filename.** `00222DC0` (the bank-record factory, reached through `0021A040`)
computes `id / 1000` (the `0x10624DD3` multiply and `sar 6` at `00222E26`–`00222E33`) and formats
`"%s/se%03d/se%06d%s"` (`009089A8`) against `[01E027E0]` = `PS2Data/sound/se/sead_data_win` and
`00908998` = `.win.sab` — so id `50001` opens `se050/se050001.win.sab`. Joined against the archive,
**all 632 distinct ids name a shipped file (0 misses)**; the three bands are exactly the three
per-sound folders `se001` (157 files), `se010` (263), `se050` (239). This also closes the §9
falsification page's open ".sab join — not tested" note.

**No band dispatch exists.** Every consumer selects a list *index*, never an id range: `003638B0`
reads the index from the emitter record and bounds it against `count`; `mapsoundplay`'s literal
script args are small ints (≤ ~17) — indices into the list, not banded ids; the `SP1` emitter
record's `+0` field is a list index; the weather table stores indices. Emitters select both bands —
over 456 `.mpk` slot-16 `SP1` blocks the emitter records pick 50k ids 1,324 times, 10k 537, 1k 8 —
and both bands travel the same loader path (`0021A040` → `00222DC0`). Their `.sab` files carry the
same four-chunk schema (`snd ` `seq ` `trk ` `mtrl`, chunk flag `0x00100000`), and the `snd `
program header is byte-identical in shape across folders.

**`sabf +0x0A` is a flat bank index, not a class code.** Re-read as a `u16` over all ~~268~~ 267 `se` folders *(corrected 2026-10-01, OPUS, by a census of all 4,609 `.sab` headers: the archive holds 267 `se` folders - no `se003`-`se006` - so the ordinals run 0-267 with slot 3 unused; the 350 distinct values the container page counts are these 267 plus 83 in the 132 `shout` banks, `5172`-`5256`; every folder carries exactly one value; `../../_index/candidates/opus-sab-param-census-1001/`)* it
is a strict ordinal — se000→0, se001→1, se002→2, se007→4, se010→5, se050→6, se100/se101→7/8,
se150/se151→9/10, se200–se433→11–244, se600–se610→245–255, se650→256, se700–se709→257–266,
se434→267 — one slot per folder in the global bank table. Its single identified reader
`007EE01D` (`movzx ebx, word [rcx+0xA]` / `cmp bx, 1` / `movaps xmm9, xmm8`) special-cases index 1
— `se001` only — zeroing `frpan` so the ambience band plays non-positional. Indices 5 (se010) and
6 (se050) take the identical `jne` fall-through; nothing else branches on them. And `sabf +0x05`
splits the two loaders: `0` in all 248 single-file block folders (opened by `SebAudioBank` via
`"%s/se%03d/se%03d%s"`, `00908A38`), `1` in every per-sound folder.

**So the 10000s/50000s split is an authored namespace partition, not a runtime class** — but the
partition *is* marked in authored data. `00222DC0` reads only the first **five bytes** of the
`SeSep` payload: payload dword `pl[0..3]` → record `+0x40` *and* `+0x45`, payload byte `pl[4]` →
`+0x44` *and* `+0x49` — two stacked `{u32, u8}` records, exactly the `.seb` node's
`{u32@0,u8@4}` + `{u32@5,u8@9}` double-record shape (UQ-255). `+0x40`/`+0x44` are the authored
pair; `+0x45`/`+0x49` the working copy. `+0x49` is the record's **live state byte**: the `.sab`
record start `00223190` reseeds it per
start with *the same rule and the same helpers as the `.seb` node's `+0x09`*
([the `.seb` block page](seb-se-block-index.md), UQ-255) — bit 7 → `0`; bit 5 (`0x20`) → the
`00210B30`/`00210710` second-exclusion lookup plus `+0x49 = (authored & 1) | 0x40`; otherwise
copied verbatim — and the family's walkers test `+0x49` under the same mask family `0x69`,
`0x68|0x01`, `0x01`, `0x40` (`002230D0`/`00223100`/`00223130`/`002234D7`). Authored across the
corpus: **1k = `0x20` in 1,015 of 1,015** (bit 5 — the exclusion arm *and* a second read at
`002232AB` that selects a different `007A78B0` float, consistent with the non-positional
`sabf+0x0A==1` → `frpan = 0` treatment), **50k = `0x01` in 1,992 of 2,110** (bit 0 — the flag that
skips the `007A7010`-equals-3 bookkeeping at `002234D7` and satisfies the `test 1` gates), **10k =
`0x00` in 2,713 of 3,398** (unflagged default). The exceptions — 685 ten-k chunks flagged bit 0 and
118 fifty-k chunks unflagged — say the flag, not the folder, carries the semantics: the bands are
where authors filed each kind, and the flag byte is what the runtime reads.

**What the flags mean, and what remains open.** Bit 0 marks the lifecycle the `007A7010`-gated
start path exempts — dominant on the emitter-selected band (emitters pick 50k 1,324:537), which
makes the convention legible as "persistent positional source" vs the unflagged one-shot —
but that *name* is inference from selection patterns, not a field the code names; the bit's
authoritative meaning is exactly the `+0x49` mask behavior above. Bit 5 is the exclusion-and-
spatialization arm — dormant in `.seb` (never authored there), live here and authored by every
ambience id.

**The rest of the `SeSep` payload (`SWE2-DATA-SESEP-FIELDS`).** A `SeSep` payload is *not* a
five-byte record — sizes run 72–1,064 B and byte 5 onward is a **program stream** (a compact
opcode/param record stream; e.g. `c1 00` repeats, `37 00 00 24 50 00 …` runs). On PC that stream
is **dead-authored**: `002DF070` is the only `SeSe`-magic walker and hands each `(id, payload)`
to `001DBE60` → `00210C40` → `0021A040` → `00222DC0`, which reads only `pl[0..4]`; no code
re-walks the region or re-finds a chunk by id, and the record never stores the payload pointer.
The playable program on PC comes from the `.sab` file's `snd `/`seq `/`trk `/`mtrl` chunks —
the stream is PS2-era bytecode carried structurally, the same disposition as the `.seb` node's
dead u32.

~~`dword0` itself is **not** dead, though: the record block `+0x40`..`+0x4c` is copied into the
request-entry shape (string pointers at `+0x30`/`+0x38`, params at `+0x40`..`+0x4c` — the clone
loops at `002191xx`/`002197xx` move it wholesale) and `00213140` pushes it into a child engine
object through the shared SEAD param-push slot `vft[+0x100]` — `edx = [+0x40]` (dword0),
`r8d = [+0x44]` (flags byte + dword0-copy low bytes), `r9d = [+0x48]`, stack `= [+0x4c]`, `1`
(`00213179`–`00213199`). The leaf consumer's field-level use is engine-side and open.~~

***Corrected 2026-09-28 (FABLE, Claude Opus 5.5): `00213140` is not audio code, and no reader of
`dword0` is found.*** The earlier sentence was a join on offsets. Record:
[`sq1-dword0-consumer`](../../_index/candidates/sq1-dword0-consumer/README.md).
- **`00213140` is slot 1 of a UI font-text instance.** It has one reference in the image, slot 1 of
  `DynGeoFontTextInstance`'s vtable. The `+0x40`..`+0x4c` it passes are four dwords of that 0x98-byte UI object,
  copied in by the object's own setter from a field of its builder. Its `vft[+0x100]` call goes to the object passed
  in `rdx`. Slot 1 of `DynGeoTextureInstance` makes the same `arg->+0x100` call, so this is the DynGeo family's
  interface, not a SEAD one.
- **The record here has a different shape.** The binder writes a bank object that it takes from its controller's
  pool (`vft[+0x30]` at `0021A0A9`). It holds a packed `{u32 +0x40, u8 +0x44, u32 +0x45, u8 +0x49}` block. The
  `SepAudioBank` (`00907B48`, stride 0x68) fill copies `+0x30`..`+0x3c` as four dwords, so they are not pointers, and
  the clone loops above move the whole block.
- **`dword0` is only ever copied.** The dword at `+0x45` has 8 accesses in the whole image: the binder's store, and
  7 in the bank copy/fill/insert family. In the audio region, every 32-bit read of `[reg + 0x40]` is an element copy
  stored straight back, apart from `00213140`'s. No `SepAudioBank` slot reads or takes the address of `+0x40`.
- **Limit.** 359 reads of that shape outside the region are not classified. The claim is that no reader was found in
  the bank code, not that no reader exists.

The `+0x49` state byte stays live as described above.
Authored shape of `dword0` across the corpus: `b0 ∈ 1–16` with bit 7 as a flag
(`0x82`/`0x83`/`0x84` dominate 1k and 50k; `0x04` dominates 10k — 1,486 of 3,398), `b1 = 0xE0`
dominant (varies widely when `w0hi = 2`), `w0hi ∈ {1, 2}` — byte-identical in shape to the
`.seb` node's dead carryover u32 (`{1–16|0x80, 0xE0, 0x01, 0x00}`), confirming the two chunk
families were authored by the same record template.

*DATA: the id→file join over all 632 ids, the `sabf` `+0x05`/`+0x0A` census over ~~268~~ 267 `se` folders *(corrected 2026-10-01, OPUS)*, the
`SeSep` payload census over all 6,523 chunks (flag byte + dword0 subfields + payload sizes), and
the payload-consumption trace; static: `00222DC0`, `0021A040`, `002DF070`, `001DBE60`,
`007EE01D`, `003638B0`, `003631B0`, `00223190`, `002230D0`–`002234D7`, ~~`00213140`/`007EFC40`~~ (see the
correction above).*
