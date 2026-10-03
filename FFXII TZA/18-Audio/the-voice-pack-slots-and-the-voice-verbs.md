---
system: The voice-pack slots and the voice verbs — 64 slots that load an event's or map's .vpc / .vpcjp pack for a manager, hold its sabf cues, and start them through the stream controller once loaded
category: 18-Audio
status: AUDITED — the slot, the verbs and the .vpc pack's layout read; the mode byte, the slot word and the states (GA-4) answered 2026-09-17, the cue table and the cue-index rule (GA-3) 2026-09-18
owner_layer: PrimaryOwner:Audio
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation delta - every function this document cites whose record differs between the stamped snapshot and GN161's gained a plate comment and tags ONLY (empty comment before, tag set a subset, checked field by field), and this document makes no uncorrected absence claim about any of them; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 1 cited address(es) among the 128 records changed across GN158..GN161; each differs only in comment and tags; 0 live absence claims (check_stranded_absence.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-DELTA-RELIANCE-BASIS; re-measured and applied for this document 2026-09-14 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-13
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-voice-pack-pass-1 - the language bit reproduces to the instruction (020BE6E0 resolved from its own displacement, bit 10 of +4, inverted by 002DEBB0) and the null path defaults to the language pack; CORRECTED: the array has TWENTY reading functions but only nineteen lie in the stated range - the twentieth is 003E9780, BELOW it, which is the request pump's post-pass helper the page's own first sentence names - and five in-range functions never touch the array, so the range holds 24 entries and is not the reader set
  crossref_clean: false        # 2026-09-30 (SWE2-DATA): false until the pass-22 UNACCOUNTED NEIGHBOUR findings are accounted (FRONTIER-REQ-SWE2-DATA-PASS22-DEBT; OPUS-REQ-DATA-PASS30-CROSSREF-CLEAN-0930)
  reopened_count: 0
---

# The voice-pack slots and the voice verbs — 64 slots that load an event's or map's `.vpc` / `.vpcjp` pack for a manager, hold its `sabf` cues, and start them through the stream controller once loaded

> **The 64 blocks at `02B5D0B0` that the request pump's post-pass helper walks are the voice
> slots.** A zone or event script calls `voiceread` to load the voice pack that belongs to the pack
> its manager is running — the fourth file of the event quadruplet (`.ebp`, `.mot`, `.snd`,
> **`.vpc`**), from the player's language for table 1 and from `in` (`.vpcjp`) for table 0 —
> `voiceplay` marks a cue pending with its volume and pan, and every request-pump pass starts the
> cues whose `sabf` bank the stream controller has finished taking. Which table plays is one bit
> of the config word: the voice-language setting.

## 1. What the player sees

Spoken lines in cutscenes and in the field, in the voice language chosen in the config. A line
that is asked for before its pack has arrived plays as soon as it has; a manager that is torn
down takes its voice packs with it.

## 2. Native mechanism

### 2.1 The slot

Sixty-four blocks of `0x40` bytes at `02B5D0B0`, one per **slot**; the verbs address a slot by
number and **twenty functions read it** — nineteen in `003E98B0` … `003EA5C0` and **the pump helper `003E9780`, which is below that range** (corrected §7; five functions inside the range never touch the array):

```
VoiceSlot (0x40) at 02B5D0B0 + slot * 0x40
  +0x00  u8    manager        the actor-manager slot (0..4) the pack belongs to (dispose-all key)
  +0x04  u8    state          0 free · 1 parked · 2 loading · 3 delivered · 4 dispose pending · 5 delivered, more owed (GA-4; corrected 2026-10-01)
  +0x05  u8    manager        as passed at load (003EA088)
  +0x07  u8    heap           2, or 0xC when the expanded voice memory 02B5E0B0 is set (003EA01D-003EA02A)
  +0x0C  u16   kind[0]        0x25 (37): the `in` pack, .vpcjp        (003EA06B, table index 0)
  +0x0E  u16   kind[1]        8: the language pack, .vpc
  +0x10  u16   id             the pack's base id + 3 = its fourth file (003EA071-003EA07A)
  +0x14  u32   size[0]        slot k's size from the pack's PKFL directory (0032F360, section 2.5)
  +0x18  u32   size[1]
  +0x20  u8*   table[0]       the loaded .vpcjp
  +0x28  u8*   table[1]       the loaded .vpc
  +0x30  u8*   current        table[voiceLanguage], refreshed by every entry point
  +0x38  rec*  speakers       24-byte records per cue: +0x10 manager, +0x14 speaker id (003EA1DC-003EA1DF)
```

**The table a call uses is chosen by the voice language.** Every entry point calls `002DEBB0`,
which is `bit 10 of [020BE6E0] + 4 == 0` (`002DDE20`), and copies `table[that]` to `+0x30`: bit
set → table 0, the `in` `.vpcjp`; clear → table 1, the language `.vpc`.

### 2.2 Load — `voiceread`

`voiceread` (`0085`, `0034EE40`) and `voiceread_20a` (`020A`, `0034E8B0`) pop their arguments and
call `003EA0D0(manager, slot, flag)` with the manager taken from the running script's context
(`002640C0()` `+0x28`); the verb is a no-op when the calling actor's manager (actor `+0x15`) has
its `+0x201` byte set (`00267310`). `003EA0D0` resets the slot (`003E98B0`: frees both tables
through `003697F0`, clears `+4` and `+0x30`) and loads table 1 then table 0 through
`003E9F80(manager, slot, flag, table)`:

1. **the pack's id**: `0032F240(manager)` — the manager's current pack index — then
   `0032F170(manager, index)` maps it to a kind and a base id: managers 1–3 → **kind 8**, `index × 4`
   (the event quadruplets of `plan_master/<lang>/event/…`); manager 4 → kind 1, `index + 0x6B`;
   manager 0 → kind 5, `index × 3` (the field triplets of `plan_work/…`). The slot stores
   `base + 3` — the quadruplet's fourth file, the `.vpc` — and the table's kind: **8 for table 1,
   0x25 (37, the `in` array, whose fourth file is `.vpcjp`) for table 0**;
2. **the size**: `0032F360(manager, slot, table)` reads `[directory + slot × 8 + 0xC]` — the
   **size** word of slot `slot` in the pack's own PKFL directory, held per manager at `022C6EC0`
   (the `.vpcjp`) / `022C6EE8` (the `.vpc`) since the manager's pack loaded (§2.5); a size ≤ 0
   loads nothing;
3. **the block**: heap 2, or heap `0xC` when the expanded voice memory pointer `02B5E0B0` is set
   (`setexpandvoicememory` `0395` / `removeexpandvoicememory` `0396` → `003EA200`), zeroed
   (`00861EC0`), stored in `table[t]` with its size;
4. **the request**: if `00267310(manager)` says the manager is in its sub-step mode the slot is
   marked resident (state 1) without a read; otherwise `003E9EF0` asks `0032F320(manager, slot,
   table)` for the slot's **offset** (`[directory + slot × 8 + 8]`) and queues
   `0032E620(kind, packId, block, size, &{fileOffset = offset, onDone = 003E9D30 for table 0,
   003E9E10 for table 1})` — a read of **sub-file `slot` of the `.vpc` / `.vpcjp`** into the block;
   state 2.

On delivery `003E9D30(slot)` sets state 3 (5 when the slot was already in state 2 with a positive
size), `+8 = −1`, clears the speaker table pointer, and walks the pack's cue table clearing every
pending bit and handle (`003E9DC0`–`003E9DCF`).

### 2.5 Where the directories come from — the manager's pack load

A manager's pack is loaded by `ActorResource_BeginManagerResourceSetLoad` (`0032FCA0`, manager,
index): after resetting the manager (`002628B0`, `ActorResource_ResetManagerLoadState` `0032ED80`)
and recording the index (`022C6D28` / `022C6D40` per manager), it maps the index to a namespace and
base id exactly as §2.2 does (`0032FD19`–`0032FD44`), loads the `.ebp` itself (`002DF980`,
`001EC660`), and requests **only the directory** of each companion into four tables `0032F430`
allocates at boot: `.snd` (`base + 2`, `0x88` bytes → `022C6E98`), `.mot` (`base + 1`, `0x88` →
`022C6E70`), and for managers 1–3 the `.vpc` (`base + 3`, `0x208` → `022C6EE8`) and the `.vpcjp`
(namespace 37, `0x208` → `022C6EC0`), setting bits 12, 13, 15 and 14 of the manager's load word
`022C6E48` (`0032FEAA`, `0032FF17`, `0032FF82`, `0032FFEE`); each directory's completion
(`00331760`, `003302B0`, `00331820`, `003317C0`) clears its bit and, when none remain, bit 3 of the
manager record's `+0x11` (`00263FF0`). A PKFL directory is `{u32 offset, u32 size}` per slot — this
loader is what settled that ([the container sheet](../26-PKFL-Package-Container/Container/pkfl-package-container.md) §8)
— so the voice slots read a sub-file's offset and size straight from the pack's header, and a
`.vpc` uses at most slots 0–13 of its 64.

**A boot-time aside from the same allocator.** `0032F430`, besides the twenty tables, sizes and
loads namespace 8 id `0x350` — `plan_master/<lang>/event/pre_z/pre_z0000/pre_z0000.ebp` — into a
block it keeps at `022C6F10` (size at `022C6D3C`), then pumps the queue to completion
(`0032E520`). **It is event pack index `0xD4` kept resident:** `ActorResource_BeginPrimaryPayloadLoad`
(`00330310`) tests the requested index against `0xD4` (`00330335`) and, when the block exists,
takes its size from `022C6D3C` instead of the size table (`0033033D`–`0033034D`) and **copies the
resident bytes into the manager's payload** (`003303F1`–`00330407`, `00861EBA`) instead of queuing a
read — so whichever manager loads `pre_z0000` gets it without touching the archive. `GA-6` answered;
why that one event is treated so is not read.

### 2.3 Play — `voiceplay`, and the pass that actually starts it

`voiceplay` (`0087`, `003515B0`) pushes the defaults 0x40 and 0x7F and falls into the three-argument
form (`00B5`, `00351020` → `003581B0`), which pops the cue word — **slot in the high byte, cue index
in the low 24 bits** (`0035820D`–`00358218`) — a speaker id (or the actor's own `[r15]` word when
negative), and calls `003EA180(slot, cue, manager, speaker)` to record manager and speaker in the
slot's 24-byte record for that cue, then `003E9C10(slot, cue, pan, volume, flag)`:

```
cue = table[voiceLanguage] + 0x10 * index          (cue table: +4 count; 16-byte entries)
  +0x08  u32   bits 0-23 offset of the cue's bank in the pack; bits 24-30 volume (clamped 0..0x7F); bit 31 pending
  +0x0B  u8    the volume byte, as the starter reads it (& 0x7F)
  +0x0C  u32   bits 0-23 the bank's byte size
  +0x0F  u8    pan (003E9D09)
  +0x10  u32   stream id, from 002DF660
  +0x14  u32   load handle
```

If the cue has no handle yet, `003E9C10` checks the bank at `table + offset` begins **`sabf`**
(`memcmp`-style import at `003E9CD0`, four bytes against `00D115B4`) and hands it to the stream
controller — `002DF660(&streamId, bank, size)`, the same call the BGM stream makes
([the music-control page](the-music-control-file-and-the-bgm-stream.md) §3.3) — storing the load
handle at `+0x14`; then it sets the pending bit, the volume bits and the pan byte.

**The start happens later, in the request pump.** Every pass ends in `003E9780`
([the queue page](../02-Resource-And-Asset-Pipeline/the-resource-request-queue.md) §8), which walks
the 64 slots in state 3, and for each pending cue whose handle has completed (`002DEE90`) — while the
mode byte `02064AD3` is 2 (`00229EA0`) — calls `002DF680(streamId, pan, volume & 0x7F)`, the stream
start, clears the pending bit and the handle and writes −1 to the slot's `+0x08` word; a pending cue
without a handle is re-asked through `003E9A10` and dropped when the stream says no.

### 2.4 Stop, pan, dispose

- **`voicestop`** (`0088`, `00351EB0` → `003EA2C0(slot, cue)`): waits for the cue's handle
  (`003EA3E0` polls `002DEE90`, yielding through `0035EA30`), closes the stream (`002DF690`) and
  clears the pending bit and both words.
- **`voicepan`** (`00B1`, `00352E80` → `003EA430(slot, cue, pan)`): `002DF610(streamId, pan)` on a
  cue with a stream (`001DC240`).
  *Added 2026-09-18 (FABLE):* `001DC240` walks the stream's voices and calls the pan wrapper `002256F0` through `00225280`, and `voicechangepan(cue, frames, pan)` (`00B4`, `00354A20` → `003EA4B0`) reaches the same setter with a fade. What the byte means - an angle, `64` dead ahead, `0x80` and above behind - and the 18 shipped calls are on [the sound-request page](Audio-Boundary/how-a-sound-request-becomes-a-voice.md) under UQ-242.
- **`voicedispose`** (`008C`, `00352DB0` → `003E98B0(slot)`): frees the slot; the manager teardown
  (`002628B0`, and `00360710`) calls `003E9970(manager)`, which frees every slot whose `+0` byte is
  that manager.
- `voicereadsync`, `voicesync`, `voicestandby`, `voicevolume`, `voicechangevolume`,
  `voicechangepan`, `voiceplay_28b` / `_28c` and the `actoriopvoice*` verbs are the same family's
  other entry points; only the six above are read here.

## 3. Modding notes

- **A voice line is a `sabf` bank inside the event's `.vpc`** (or `.vpcjp`), addressed by offset and
  size from the pack's cue table; the pack is a PKFL container
  ([the container category](../26-PKFL-Package-Container/README.md), 1,809 `.vpc` / `.vpcjp` pairs).
  Replacing a line means replacing the bank in the pack and keeping the cue table's offset and
  size in step.
- **The voice language is one config bit** — bit 10 of the word at `[020BE6E0] + 4` — read at
  every voice call, not only at load: both packs are loaded, and the bit picks which one plays.
- **A cue's volume lives in the cue word's bits 24–30**, capped at `0x7F`; `voiceplay`'s defaults
  are ~~volume `0x40`, pan `0x7F`~~ **pan `0x40`, volume `0x7F`**. *Corrected 2026-09-21 (FABLE, on
  `ASTRA-CONTRA-FABLE-VOICEPLAY-DEFAULT-ORDER`, re-read from the shipping bytes rather than taken on
  trust.)* **The pair was printed the wrong way round, and a modder following it changed two
  different controls.** `003515B0` pushes `0x40` then `0x7F`; `00351020` pops three and re-pushes
  `−1 / cue / 0x40 / 0x7F / 1`; `003581B0`'s five pops leave `0x40` in `r14d` and `0x7F` in `ebp`
  (`003581F4`, `003581EA`), so `003E9BF0` → `003E9C10` receives `r8d = 0x40`, `r9d = 0x7F`. **The
  callee separates them outright**: `003E9D09` stores `r8b` at the cue entry's `+0x0F`, while
  `003E9D00`–`003E9D06` masks the other with `0x7F` and shifts it into `+0x08` bits 24–30 — and the
  pump reads them back the same way, `003E9825` taking byte `+0x0F` as the pan argument of
  `002DF680` and `003E981F` taking byte `+0x0B` as the volume. Which is also the only reading that
  makes sense of the values: `0x40` is the **centre** of `0..0x7F` and `0x7F` is **full** volume,
  where the reversed pair would have every line play at half volume, hard panned.
- **The expanded voice memory** (`setexpandvoicememory`) moves the packs to heap `0xC`.

## 4. What is not known

- [x] **GA-3.** The `.vpc` pack's own layout — *narrowed 2026-09-11:* the cue table is **sub-file `slot` of
      the PKFL package** (offset and size from its directory); what the cue's bytes `+0`–`+7` hold
      and how the cue index relates to the event script's line ids remain. `GA-3`.
      *Container pinned 2026-09-15 (OPUS) — the cue question itself is untouched and stays open.*
      The PKFL header is `"PKFL"`, then `+0x04`, then `(offset, size)` pairs from `+0x08`.
      ***First half answered 2026-09-15 (FABLE), authored data + static: a cue's `+0x00`–`+0x07` are
      the previous cue's two runtime words, and they are empty in every shipped file.*** The second
      half — how the cue index maps to event-script line ids — is untouched, so the row stays open.
      - **The cue table is the `VSP1` sub-file itself, and there is no separate cue slot.** Every
        populated slot of every `us` `.vpc` is a `VSP1`: **510 sub-files across 201 packs**, no
        exception. The container is `VSP1`, a `u32` count at `+0x04`, then *count* 16-byte records at
        `+0x10 × i`, whose `+0x08` and `+0x0C` are §3's offset and size fields.
      - **The offset/size pairs tile each sub-file exactly.** Over all **2,554** records: every record
        begins where the previous one ends, the last ends on the sub-file's byte length, and there are
        **0 gaps and 0 overlaps**. That is what pins the record stride at `0x10` independently of the
        code.
      - **So §3's `+0x10` stream id and `+0x14` load handle belong to the NEXT record's slot.** That is
        not a slip in §3 — `003E9C10` computes the record with `shl rbx, 4` (×16) and then genuinely
        uses `[rbx + 0x10]` and `[rbx + 0x14]`, storing the handle at `+0x14` (`003E9CF1`). **A cue's
        two runtime words physically live in the following cue's `+0x00` / `+0x04`.**
      - **Which is exactly why the file has nothing there.** `+0x00` and `+0x04` are **zero in all
        2,044 records other than record 0**, in every one of the 510 sub-files. Record 0's are not an
        exception to the rule but a consequence of it: with no cue −1, the container header sits in the
        slot that cue's runtime words would occupy — `VSP1` at `+0x00` and the count at `+0x04`.
      - **A prediction this reading makes, tested and held.** If the last cue's runtime words sit past
        the final record, they must land in padding rather than in the first bank's bytes — so the
        data must start at least 8 bytes after `0x10 × count`. **It holds in 510 of 510 sub-files**,
        with the slack always a whole multiple of 16 (16 ×134, 32 ×133, 48 ×146, 64 ×97).
      - **Not claimed:** that the engine never writes past the table. The prediction shows the shipped
        packs leave room; it does not show the writer checks.
      - **A cheap probe at the second half, recorded because it FAILED and the next reader should not
        repeat it.** §2.3 says `voiceplay`'s cue word carries the index in its low 24 bits, and a verb
        call is three bytes — one of `0x58` / `0x59` / `0x5D` / `0x5E` then the `u16` verb id — so a raw
        byte scan of the sibling `.ebp` for `voiceplay` (`0x0087`) and its three-argument form
        (`0x00B5`) looks like it should count the calls. Over the **201** `us` events that ship both a
        script and a pack it finds 272 calls against **2,554** cues, and **most scripts score zero
        while their pack holds cues** — `alc_z0104` has 46 cues and no hit. Only **35 of 201** match
        exactly (`bds_e0100` 3 = 3, `bds_e0101` 2 = 2). **A scan that finds nothing in the majority of
        a population it should cover is measuring its own blind spot, not the data:** `.ebp` bytecode
        is sectioned, and scanning the container end to end is not the same as scanning the code. The
        second half needs the script properly decoded, not a byte search.
      ***Second half ANSWERED 2026-09-18 (FABLE): a script's cue index is the ordinal into its own pack's cue table, in play order, and the packs hold exactly the cues their scripts play.** The `.vpc` of an event script (`ps2data/plan_master/<lang>/event/<area>/<map>/<map>.vpc`, read from the archive) populates one PKFL slot, slot 0, whose sub-file is a `VSP1` block with the cue count at `+4` and 16-byte entries; `voiceread` takes the slot (0, 1 or 2 in the shipped scripts) and `voiceplay` and its `_28b` / `_28c` / `_b5` forms take the cue index as their last argument. Over the 1,115 `us` event containers decompiled with ff12-script, 196 scripts play voice cues, and joining each to its `us` pack gives: the highest index plus one equals the pack's count in 189, is below it in 7 (spare trailing cues, e.g. `alc_a0100` plays 0..4 of 6), and exceeds it in none; 176 scripts use every index from 0 upward without gaps. So there is no line-id table: the authoring numbers a scene's lines and its cues together, the pack is built in that order, and the script names each cue by its position. One value stands outside the table: 27 scripts also pass index 127, beyond every pack's count, so the play verb must treat 127 as a sentinel rather than a cue (its body was not re-read for that case). The per-script listing is [`members/voice-cue-census.tsv`](members/voice-cue-census.tsv). DATA from the corpus and the archive.*
      ***The ordinal reading stands; the operand positions and the "exceeds it in none" / "127 sentinel" details are corrected 2026-09-19 (SWE2-DATA), native + authored.*** The play verbs do **not** all take the cue word as their last argument. The wrappers push constants with `00267F90` (a *push*, `edx` = the value) and forward to the shared bodies `003581B0` / `00351020`; `00267E10` pops. Popping in order gives the operand map:
        - `voiceplay` (`0087`, arity 1): **arg0** = cue word `slot<<24 | index`; the pushed defaults are **speaker `−1`, pan `0x40`, volume `0x7F`** *(the labels were in a different order from the values until 2026-09-21; see §3)*.
        - `voiceplay_b5` (`00B5`, arity 3): **arg0** = cue word — the *first* argument, not the last; arg1/arg2 take the `0x40`/`0x7F` positions; speaker defaults to `−1` → actor field `word[r15]`.
        - `voiceplay_28b` (`028B`, arity 2): **arg1** = cue word; arg0 = speaker id written to the cue record's `+0x14` (`003EA1DF`), `−1` → actor field.
        - `voiceplay_28c` (`028C`, arity 4): **arg1** = cue word; arg0 = speaker id; arg2/arg3 take the `0x40`/`0x7F` positions. It is arg1 — the *second* of four — not the last.
        `003E9C10` resolves `slot → rbx = 02B5D0B0 + slot*64`, reads the slot's loaded `VSP1` block, and **bound-checks `index` against the block's `+4` count — `count <= index` returns silently** (`003E9C74–003E9C7E`). So the cue index is a direct ordinal into whichever `VSP1` the slot holds; there is no lookup table, and out-of-range references are engine no-ops, not traps.
        Re-decoded with the corrected positions over all `us` event scripts (2,531 statically-resolved play sites in 198 scripts, every cue word a literal, slot byte **always 0**): **1,295 sites are in range and 1,236 are out of range** against the same-named pack's slot-0 `VSP1` count — 99 of 198 scripts carry at least one, and the values run to **330** against a shipped `VSP1` count ceiling of 24 (`bhm_c0102` passes 273–278 and 317–330; `alc_z0104` passes 71–79 and 146–157). The out-of-range sets are dense contiguous runs — shaped like a per-scene numbering whose cues are not in the joined pack — so they are either dead references the bound check drops, or references to a `VSP1` bound into slot 0 by a mechanism the same-named `.vpc` join cannot see (e.g. a parent event's pack; `.vpcjp` counts are identical, so the locale variant is ruled out). Which block `voiceread(slot)` binds is the loader-side question the authored data leaves open. The earlier "exceeds it in none" and "index 127 is the sentinel" claims do not hold under the corrected operands: `127` appears in the cue position at only **2** sites — the `127`s the first census collected were the `0x7F` default sitting in `voiceplay_28c`'s arg2/arg3 (and `_b5`'s arg1/arg2) positions, which its last-argument reading mistook for cue words. Per-script/per-verb argument listing: [`members/voice-cue-arg-census.tsv`](members/voice-cue-arg-census.tsv) (generator `gen_voice_cue_arg_census.py`; supersedes `voice-cue-census.tsv` for argument semantics). NATIVE for the operand map and bound check; DATA for the census.*

      **`+0x04` is the directory capacity in slots, and it varies by family** — `16` for `.mot` and
      `.snd`, `64` for `.vpc` and `.vpcjp` — which is why a single reading of it as a byte length does
      not hold. *(I first read it as a byte length, which implies 7 slots and would have made this
      page's “slots 0–13” wrong. It is not wrong: the highest slot index actually used in the 1,809
      `.vpc` files is exactly **13**.)*
      **Verified as a prediction over all 8,505 files of the three large families:** every populated
      slot lies inside its file (**0** past EOF) and **no file ever populates a slot at or beyond its
      own `+0x04`** — `.mot` reaches index 15 of 16, `.snd` 15 of 16, `.vpc` 13 of 64.
      Slot totals: `.mot` **9,909** containers in 4,392 packs, `.snd` **21,114** in 2,304, `.vpc`
      **4,590** in 1,809. *The `.mot` figure is an independent control rather than a new count* — it
      matches the 9,909 already recorded on
      [resource-section-addressing](../02-Resource-And-Asset-Pipeline/resource-section-addressing.md)
      exactly, from a different route. §2.5's four PKFL families are that page's and this one's
      finding, not mine; the census only confirms them at 10,314 packages in total.
      **Not claimed:** what `+0x04` means beyond capacity — nothing in the corpus varies it within a
      family, so the data cannot distinguish “capacity” from “fixed per format”, and 36 `.vpc` files
      populate their slots with gaps rather than a contiguous run, which is unexplained.
- [x] ~~The per-manager resource index at `021C6EC0` / `021C6EE8`~~ **ANSWERED 2026-09-11 (§2.5)** —
      the four tables are the PKFL directories of the manager's `.vpcjp`, `.vpc`, `.mot` and `.snd`,
      loaded by `ActorResource_BeginManagerResourceSetLoad`; unrelated to the `.nmb` index. `FZ-20`.
- [x] ~~What the resident `pre_z0000.ebp` that `0032F430` loads at boot into `022C6F10` is for.~~
      **ANSWERED 2026-09-11** — it is event pack `0xD4`, served from memory by
      `ActorResource_BeginPrimaryPayloadLoad` whenever a manager loads that index (§2.5). `GA-6`.
- [x] ~~**GA-4.** What the mode byte `02064AD3` (`00229EA0`, written by `00229F00`) gates, and what the slot's~~
      `+0x08` word and states 4 / 5 mean. `GA-4`. *Narrowed 2026-09-13 (FABLE):* the byte is the main loop's
      **frame mode** ([what happens between two frames](../22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md) §2.2),
      and 2 is the field/battle frame — so a loaded cue starts only in the field frame (`003E9815`–`003E981D`); in the
      full-menu frame (3), the capture modes (4–6) and boot (0–1) it stays pending and starts on the first pass after
      the mode returns to 2. The `+0x08` word and states 4 / 5 remain.
      *Narrowed further 2026-09-14 (FABLE): the slot word is write-only, and every state store is read.* The slot
      array is 64 × `0x40` at `02B5D0B0`: state byte `+0x04`, manager byte `+0x05`, language tables `+0x20` / `+0x28`,
      selected table `+0x30`. Twenty functions reference it (RIP census), plus `003E9EF0`, which is handed the slot.
      - **`+0x08` is written only as `−1`**, at `003E9844` in the pump after a start and at `003E9D8D` / `003E9E6A` in the
        two load callbacks. No instruction in the family reads it. The other `[reg + 8]` accesses there address cue
        records, after the register was reloaded with a cue.
      - **States**, from every store:
        - **0** free: the dispose `003E98B0` clears it after freeing the tables (`003E992E`).
        - **1** parked: the load request `003E9F80` sets it when `00267310(manager)`, the byte
          `02099011 + 0x288·manager`, is non-zero (`003EA098`–`003EA0A1`). Otherwise it submits the read.
        - **2** loading: the submit `003E9EF0` sets it after `0032E620`, unless the slot is already 5 (`003E9F5E`–`003E9F64`).
        - **3** delivered: the load callback (`003E9D30` for table 0, `003E9E10` for table 1) sets it (`003E9D89`).
        - **4** dispose pending: `003E98B0` on a slot in state 2 only marks it (`003E9954`). The callback then
          disposes on delivery (`003E9D94`–`003E9D9B`); it also disposes when the pack header is not `VSP1`
          (`003E9DDC`–`003E9DF5`).
        - **5** delivered, more to come: the callback sets it instead of 3 when the prior state was 2 and
          `0032F360(manager, slot, 1)` returns a positive count (`003E9D74`–`003E9D83`). A later submit keeps 5, and
          the next delivery sets 3.
      - **Residue:** which pass promotes a parked slot (state 1) to a submit, and what the count `0032F360` reads
        (`[table + slot·8 + 0xC]` of a four-entry manager array) stands for.
      ***ANSWERED 2026-09-17 (FABLE): the byte is the frame mode (2026-09-13), the slot word is write-only and the states are read (2026-09-14), and the residue closes: nothing promotes a parked slot, and the count is the sub-file's size.** The submit `003E9EF0`, the only writer of state 2, has exactly one caller, the load request `003E9F80` (`003EA0AD`). That request sizes the table through `0032F360` (`003EA009`), allocates the buffer (`0036A190` or `0036A100`, `003EA03C`..`003EA043`), records size, pointer, manager and kind in the slot (`003EA06B`..`003EA08C`), then either parks the slot in state 1 when `00267310(manager)` is set (`003EA098`..`003EA0A1`) or submits. A census of every compare of the state byte in `003E9800`..`003EA200` finds compares with 0, 2, 3 and 5 and none with 1, so a parked slot is promoted by no pass: it stays parked until a new load request for the same slot runs the same path with the manager's byte clear. The count `0032F360(manager, slot, table)` is `[directory + slot x 8 + 0xC]` of the manager's PKFL directory, the sub-file's size (§2.5), so state 5 means the pack's second table exists and a delivery is still owed. Static, bodies read.*
- [x] ~~Manager 4's kind-1 mapping (`index + 0x6B` into the `.ca` array) — whether any shipped script
      loads a voice pack under manager 4.~~ **`GA-5` ANSWERED 2026-09-13 (FABLE):** **no — and no shipped script can.** A voice slot's id comes from `0032F240(manager)`, which is `−1` unless the manager's loaded flag `022C6D18[m]` is set, and the pack index it returns (`022C6D28[m]`) has one writer in `.text`, `ActorResource_BeginManagerResourceSetLoad` (`0032FD09`), called only from `WorldSimulation_ProcessDeferredModeRequest` `0032FC30`. Its eight call sites pass manager **0** (the world tick, `003140B8`), **1** (the field pass, pack `0xD4`, `0025DAE1`), **3** (`BattleAction_InitializeGlobalSpecialSequenceMode` `00306C0A`, `00353590`, `003CA077`), **`clamp(n + 1, 1, 3)`** (`003522C0`, `00353080` — the event-load verbs), or the script's own operand — **only in `debug_eventload`'s poll** (verb `0x202D`, `0050D110`–`0050D115`), which is also the only caller of manager 4's unload request `00314410`. The 1,114 decompiled `us` scripts never call `debug_eventload` (control: other family-2 debug verbs do appear — `debug_mapjump` 297 times, `debug_tty_string` 192). So in shipped play manager 4 never holds a pack, the kind-1 `index + 0x6B` mapping is reached only through that debug verb, and a voice verb run by a manager-4 actor would find no pack. Boot's resident pack is slot 5 (`022C6D1D`/`022C6D3C`, `0032F430`), not manager 4.

## 5. Evidence

| claim | evidence | tier |
|---|---|---|
| the 64 slots, their fields and states | `003E9F80`–`003EA0BC`, `003E9D30`–`003E9DCF`, `003E98B0`–`003E9963`, `003E9970`–`003E99C9` | 1 |
| the verb bindings | [the verb table](../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv) rows `0085`, `0087`, `0088`, `008C`, `00B1`, `00B5`, `020A`, `0395`, `0396`; handler bodies `0034EE40`, `003515B0`, `00351020`, `003581B0`, `00351EB0`, `00352DB0`, `00352E80` | 1 |
| kind 8 / 37 and the fourth file | `003E9FED`–`003EA005` (`0x25` / `8`), `003EA071`–`003EA07A` (`+3`); the kind-8 array `01ED1990` ids 120–123 = `nal_a0100.ebp / .mot / .snd / .vpc`, the kind-37 array's id 123 = `.vpcjp` | 1 |
| the manager → kind map | `0032F170`–`0032F1AB` | 1 |
| the voice-language bit | `002DEBB0` → `002DDE20`: `[020BE6E0] + 4`, `shr 10, and 1` | 1 |
| the `sabf` check and the stream hand-off | `003E9CC0`–`003E9CF1`; magic bytes at `00D115B4` | 1 |
| the start in the pump | `003E97F0`–`003E9869` | 1 |

## 6. Related

- [`the-music-control-file-and-the-bgm-stream.md`](the-music-control-file-and-the-bgm-stream.md) — the stream controller these cues go through.
- [`../02-Resource-And-Asset-Pipeline/the-resource-request-queue.md`](../02-Resource-And-Asset-Pipeline/the-resource-request-queue.md) — the pump whose post-pass helper starts the cues.
- [`../04-Actor-Entity/Actor-Manager-Record/the-actor-manager-record-field-map.md`](../04-Actor-Entity/Actor-Manager-Record/the-actor-manager-record-field-map.md) — the five managers and their `+0x201` byte.
- [`../_index/ASSET-FORMATS.md`](../_index/ASSET-FORMATS.md) — `.vpc` / `.vpcjp` as PKFL containers.

## 7. Falsification pass 1 — 2026-09-13 (OPUS)

*(Static only — the shipped image and the function list. Nothing executed, and no audio was played.)*

### ✔ The language bit reproduces exactly

`002DDE20` is `mov rax, [rip + 0x1E808B9]` — which resolves to **`020BE6E0`**, the address §2.1 names
— then `mov eax, [rax+4]` / `shr eax, 0xA` / `and eax, 1`: **bit 10 of `[020BE6E0] + 4`**, to the
instruction. `002DEBB0` (23 B) inverts it with `sete`, so `table[002DEBB0()]` gives **bit set →
table 0** (the `in` `.vpcjp`) and **clear → table 1** (the language `.vpc`), exactly as published.

> **One behaviour the bytes add:** `002DDE20` returns through a **null check**
> (`test rax, rax / je`), and on the null path `eax` still holds the low half of the null pointer —
> zero. So **with the config object absent the language pack, table 1, is chosen**, not the `in`
> pack. A default worth knowing for a reimplementation that builds the config later than the audio.

### ✖ Corrected: the readers are twenty, and one of them is outside the stated range

§2.1 says the array's readers are *"the family `003E98B0` … `003EA5C0`, twenty functions"* and that
this family **is the only reader**. A census of every rip-relative operand landing anywhere in the
`64 × 0x40` block finds **twenty reading functions** — the count is right — but:

* **nineteen** of them lie in the stated range;
* **the twentieth is `003E9780`, below it**;
* and **five functions inside the range never touch the array** (`003E9AA0`, `003E9BF0`, `003E9EF0`,
  `003EA2A0`, `003EA3E0`), so the range holds **24** entries, not twenty.

**`003E9780` is the page's own abstract.** Its `lea r14, [rip + 0x2773938]` resolves to
**`02B5D0E0` = slot 0's `+0x30`**, and it then walks the slots reading `[r14-0x2C]` (the state byte
`+0x04`), selecting `[r14 + rcx*8 - 0x10]` (`table[0]` / `table[1]`) by `002DEBB0()` and storing it
into `[r14]` (`+0x30`) — **the "refreshed by every entry point" behaviour §2.1 attributes to the
entry points is also done here, in a pass over all 64 slots.** Its only caller is `0032E070`, the
request pump, which makes it *"the request pump's post-pass helper"* the page's **first sentence**
names. The abstract and §2.1 disagree, and the abstract is right.

**The count of twenty is a reader count, not a range.** Stating it as an address range excludes the
one reader the document opens with and includes five functions that are not readers at all.

**Not claimed.** Everything downstream of §2.2 — the id mapping, the PKFL size read, the `sabf`
hand-off and the cue records — was **not re-read**; this pass measured the array's readers and the
language bit. What the five non-reading range members do. Nothing was executed.

## Residual placements — 2026-09-14 (SWE2-FRONTIER, residual-placement package)

| function | size | role (call-signature read) |
|---|---:|---|
| `001E59B0` | 645 | voice-slot body on `[rcx+0x218]`/`+0x250`: `00861EBA`, `001E6040` x2, `0018AA00`; caller `001A9BF0` |

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL.*

- **Presentation — CLIENT.**
  - The frame-mode getter `00229EA0` is read by `RenderModelInstanceContainer_ProcessActiveEn…`,
    `PresentationEntry_UpdateForCurrentGlobalPhas…` and two more bodies.
  - The sound calls `002DEE90` and `002DEBB0` are also made by Presentation bodies of 271–1,073 bytes.
  - `003E9A10` and `003EA3E0` are called by Presentation bodies of 297 B and 151 B.
  - `001E6040` is called by a 1,302-byte body, and `002DF980` by a 1,636-byte body.
  - The slot accessors `0032F170` / `0032F240` and the manager-slot byte reader `00267310` are read by a 511-byte
    body.
  - The actor-manager accessor `00263FF0` is read by five Presentation bodies.
- **Input, Movement and Party — CLIENT and SERVICE.**
  - The frame-mode setter `00229F00` is called by the 1,002-byte Input body.
  - `00263FF0` is read by the unread 1,936-byte Input body and by two movement bodies.
  - `00267310` is read by `Movement_UpdateSteeringTowardTarget` and a 935-byte movement body.
  - **The area unload `002628B0` touches party and movement state as well.** It calls
    `PartyControl_SetMovementSuppressionBit`, `PartyFocus_ClearCurrentActorIfEligible`, six movement helpers,
    `CharacterRenderSystem_RefreshDistanceCullEna…` and three Presentation bodies.
- **CombatAction — CLIENT.** `0032E520` is also called by a 183-byte CombatAction body. The file-request family (`0032E400` size probe, `0032E620` request, `0032E520`, `0032E4D0`, `0032E070`) is shared: its **Presentation** callers (119 B and 337 B bodies), the **Input**-filed item-graphics loader (177 B) and script-verb bodies are CLIENTS, not audio dependencies.
- **CoreRuntimeScheduling - CLIENT and SERVICE (9 edges).** `0035EA30`, `0032E520` are also called by bodies filed to core runtime scheduling: `0022B6E0`, `0022B7E0`, `0022A0B0` (+2 more); `002628B0`, `003E9780` reach bodies filed to core runtime scheduling: `00229EE0`, `00229EA0` - shared machinery across the layer boundary, no shared ownership.
- **Resource - CLIENT and SERVICE (54 edges).** `0032E620`, `0036A190`, `0036A100` are also called by bodies filed to resource: `003EADE0`, `00249210`, `001DA290` (+16 more); `0032E070`, `0032F430`, `0032FCA0` reach bodies filed to resource: `0032E620`, `0032E520`, `0032E400` (+12 more) - shared machinery across the layer boundary, no shared ownership.
- **SaveLoad - CLIENT (1 edge).** `0032E4D0` is also called by bodies filed to save/load: `00280140` - shared machinery across the layer boundary, no shared ownership.
- **Save_Load_Settings - CLIENT and SERVICE (2 edges).** `0032E620` is also called by bodies filed to save/load/settings: `002EF300`; `002628B0` reaches bodies filed to save/load/settings: `002EF2B0` - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT (2 edges).** `00229EA0` is also called by bodies filed to UI: `002468A0`, `00246C20` - shared machinery across the layer boundary, no shared ownership.
- **World - CLIENT (3 edges).** `0032E620`, `0032F430`, `0036A190` are also called by bodies filed to world: `00378540`, `00266D10` - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT and SERVICE (19 edges).** `0036A190`, `0032E620`, `0036A100` are also called by bodies filed to world area: `00268750`, `00378030`, `003EA820` (+9 more); `002628B0`, `0032F430` reach bodies filed to world area: `00378230`, `003DFA50`, `003EAA00` (+1 more) - shared machinery across the layer boundary, no shared ownership.
### Interior citation — frontier hub 0032F240 (2026-09-18, SWE2-EC7)

**0032F240** (31 B, 4 A-measured callers) — the pack-index getter §79's GA-5 answer already names: `if (byte[022C6D18[manager]]) return dword[022C6D28[manager*4]]; return -1`. `lea rcx,[rip-0x20f24a]` materialises the image base so the table reads land at `022C6D18` (loaded flag) and `022C6D28` (pack index) exactly as the inventory states — the `−1` the voice verbs branch on is the empty-slot code, and `0032FD09`'s write is the only producer. In-scope: flag byte test [`0032F24C`](../_index/ADDRESS-INDEX.md); pack-index load [`0032F254`](../_index/ADDRESS-INDEX.md) — 4 callers, all A.

## SWE2-EC7-18 update (2026-05-15) — `0018AA00` slot helper fragment

`0018AA00` (16 B) is the indexed slot fetch one of this cluster's helpers shares (the voice-pack slot functions this page enumerates): `r8d = movzx r8b`, `rax = movsxd edx + r8*4` (`0018AA04`..`0018AA0B`), `rax = [rcx + rax*8]`, `ret` — a two-operand index (`edx + r8*4`) into `rcx`'s qword slot table, the `001E59B0` slot body this page lists calls it to resolve channel rows; its measured callers reach it from the slot-verbs' scan arms this page describes.

## SWE2-EC7-25 update (2026-09-18) — `0032F360` indexed dword getter

`0032F360` (55 B) bounds-checks `ecx <= 3`, picks `021A6EC0[ecx]` when
`r8d == 0` else `021A6EE8[ecx]`, requires `byte[0]` non-zero, and returns
`dword[rcx + rdx*8 + 0xC]` — the per-kind row-column fetch the voice/slot
verbs share (-1 on any miss). Interior anchor `0032F38E` (the `+0xC` read).

## SWE2-EC7-36 update (2026-09-19) - `001E59B0`

`001E59B0` (645 B) is a voice-pack slot body - `01F7E340`, `00861EBA`/`001E6040` pairs plus `0018AA00`. Interior anchor `001E5AD7` (an `00861EBA` call).

## SWE2-EC7-46 update (2026-09-19) - `001A9BF0`

`001A9BF0` (223 B) is a body - `001A2EE0`/`001E59B0`. Interior anchor `001A9C9E` (an `001A2EE0` call).

## SWE2-EC7-57 update (2026-09-19) - `003EA0D0`

`003EA0D0` (171 B) is the `003EA0D0(manager, slot, flag)` call the voice-pack page names - `002DEBB0`/`003E98B0`/`003E9F80` plus `02B5D0B0`. Interior anchor `003EA0F0` (a `003E98B0` call).

## SWE2-EC7-61 update (2026-09-19) - `003EA200`

`003EA200` (151 B) is a voice-pack body - `002DEBB0`/`0032E520`/`003697F0`/`0036D160`/`003E98B0` plus `02B5D0B7`/`02B5E0B0`. Interior anchor `003EA225` (a `002DEBB0` call).



## SWE2-EC7-63 update (2026-09-19) - `001A2EE0`

`001A2EE0` (144 B) is a voice-pack body - `001A37C0` single call. Interior anchor `001A2F5D` (a `001A37C0` call).



## SWE2-EC7-64 update (2026-09-19) - `003E9A10`

`003E9A10` (140 B) is a voice-pack re-ask body - `002DEBB0` single call plus `02B5D0B0`. Interior anchor `003E9A2D` (a `002DEBB0` call).



## SWE2-EC7-66 update (2026-09-19) - `003EA4B0`

`003EA4B0` (134 B) is a pan-wrapper voice-pack body - `002DEBB0`/`002DF620` plus `02B5D0B0`. Interior anchor `003EA4DE` (a `002DEBB0` call).



## SWE2-EC7-66 update (2026-09-19) - `003EA5C0`

`003EA5C0` (134 B) is a block-owning voice-pack body - `002DEBB0`/`002DF6B0` plus `02B5D0B0`. Interior anchor `003EA5EE` (a `002DEBB0` call).


`003EA330` (176 B) is the per-slot pending-entry reset `003E98B0` runs on the `02B5D0B0` 64-stride slot table: `002DEBB0` first, then when `byte[rsi+4] == 3` and a child list sits at `[rsi + rax*8 + 0x20]` the loop walks its `dword[+4]`-counted `0x10`-byte entries, `003EA3E0` gets `(+0x10, +0x14)` per entry, and each entry clears the `+8` sign bit and zeroes `+0x10`

Interior anchor `003EA3B0` (function `003EA330`).

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../_index/candidates/opus-the-voice-pack-slots-and-the-voice-verbs-cloudint-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0034E8B0` | 114 B | with `s` = dword `+0x28` of `002640C0()`, reads `a` = `00267E10(r9)` and then `b` = `00267E10(r9)`; when `00267310(byte rdx+0x15)` returns 0 and `003EA0D0(s, b, a)` returns non-zero it calls `00314D40(1)`, otherwise it calls nothing further | `0034E8CA`, `0034E8D2`, `0034E8EA`, `0034E8FA`, `0034E908` |
| `0034EE40` | 124 B | calls `00267F90(r9, 0)`; then, with `s` = dword `+0x28` of `002640C0()`, reads `a` = `00267E10(r9)` and then `b` = `00267E10(r9)`; when `00267310(byte rdx+0x15)` returns 0 and `003EA0D0(s, b, a)` returns non-zero it calls `00314D40(1)`, otherwise it calls nothing further | `0034EE5F`, `0034EE64`, `0034EE84`, `0034EE94`, `0034EEA2` |
| `003522C0` | 91 B | with `a` = dword `[r8]` and `b` = dword `[r8+4]`, does nothing when `00264170()` returns 0, when `001C3370()` returns 1 or when `a` is negative; otherwise, with `n` = `a`+1 held between 1 and 3 (signed), calls `0032FC30(n, b)` and `0032ED70(n)` | `003522D1`, `003522DF`, `003522E6`, `003522FD`, `00352304` |
| `00352DB0` | 35 B | with `n` = `00267E10(r9)`, calls `003EA330(n)` and tail-jumps to `003E98B0(n)` | `00352DB9`, `00352DC2`, `00352DCE` |
| `00353080` | 107 B | calls `00314D40(1)` first; then, with `a` = dword `[r8]` and `b` = dword `[r8+4]`, does nothing more when `00264170()` returns 0, when `001C3370()` returns 1 or when `a` is negative; otherwise, with `n` = `a`+1 held between 1 and 3 (signed), calls `0032FC30(n, b)` and `0032ED70(n)` | `00353099`, `003530A3`, `003530B7`, `003530C8`, `003530CF` |

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted, opus-the-voice-pack-slots-and-the-voice-verbs-ee-1003)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../_index/candidates/opus-the-voice-pack-slots-and-the-voice-verbs-ee-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00351020` | 173 B | Reads three dwords from the object in `r9` with three calls to `00267E10`, then calls `00267F90` on that object five times with -1, the third value read, the second, the first and finally 1, and tail-jumps to `003581B0` with the original `rcx`, `rdx`, `r8` and `r9`. | `00351057`, `0035106E`, `0035108C`, `00351099`, `003510C8` |
