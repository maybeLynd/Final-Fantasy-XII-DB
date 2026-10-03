---
system: Persistent flag banks
category: 14-Story-Event-Quest-Hunt
status: AUDITED
owner_layer: PrimaryOwner:Story_Event_Quest_Hunt
evidence_tier: 1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN158 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN158 this document cites none of batch R109's 109; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-08
archive_formats:
  - "flagdef | explained | mapjumpgroupinit.bin (.bin member; FLAGDEF1): 8-byte tag, u16 count at +8, u16 flag ids from +0x0A (10 + 2*53 = 116) - (kind 9, 0x28) published to 02ADD0D0 by 00378B90, read by PersistentFlag_ApplyAuthoredInitialPrimarySet 00379160, section 8f"
  - "flagrom | explained | mapjumpgroupflagrom.bin (.bin member; FLAGROM1, a different layout from FLAGDEF1): {char[8], u16 count 152, u16 offset[152], bit-15-terminated u16 threshold lists} (856 B) - (kind 9, 0xA) by 00378540, published to 02ADD0C8 by 00378BA0, read only by PersistentFlag_QueryAuthoredThresholdSchedule 00377970, section 2"
audit:
  passes: 2
  last_pass: 2026-09-02
  last_pass_state: falsification-pass-1-repos-46
  crossref_clean: true
  reopened_count: 6
---

# Persistent flag banks

> **Everything the game remembers about your story is bits.** ~~Six banks~~ Five banks of them (six accessor families) *(corrected 2026-10-02, FABLE, on OPUS's byte verdict C-V1, [record](../_index/candidates/opus-story-readiness-fixes-1002/byte-verdicts.md))*, living at known
> offsets inside your save, and two reserved ids that mean *always* and *never*.

## 1. What the player sees

Every door that stays unlocked, every cutscene that does not replay, every hunt marked complete,
every chest you already opened, every NPC whose dialogue has moved on — all of it is a **single
bit**, set once and remembered.

That is why story progress is granular and irreversible in the way it is. There is no "chapter
number". There is a wall of switches, and the game asks about individual switches constantly:
*has this happened yet?*

Two of those switches are special and are not really switches at all. **Flag 0 is hardwired to
"yes" and flag 1 to "no"** — so an authored condition can say *always* or *never* just by naming
them.

## 2. Native mechanism

### ~~Six banks~~ Five banks, all inside the save payload (corrected 2026-10-02, FABLE)

*Five storage regions under six accessor families: `Bank512`'s Low and High pairs address one region at `+0x14B4` (AA-4, section 8b).* *(corrected 2026-10-02, FABLE, on OPUS's byte verdict C-V1, [record](../_index/candidates/opus-story-readiness-fixes-1002/byte-verdicts.md))*

Every accessor resolves through `SaveImage_GetPersistentPayloadBase()` — the same payload base the
current-area accessor reads. **Story progress is save state, addressed by offset.**

| Bank | Payload offset | Valid ids | Bytes |
|---|---|---|---:|
| `Bank64A` | `+0x1384` | `0 .. 0x3F` | 8 |
| `Bank64B` | `+0x138C` | `0 .. 0x3F` | 8 |
| `Bank2048` | `+0x13B4` | `0 .. 0x7FF` | 256 |
| `Bank512` (Low + High accessors) | `+0x14B4` | `0 .. 0x1FF` | 64 |
| `Primary` | `+0x14F4` | `2 .. 0x1FF` | 64 |

**The layout is contiguous apart from one gap**, which is strong internal corroboration that these
offsets were read correctly:

```
0x1384 +   8 = 0x138C      Bank64A ends exactly where Bank64B begins
0x138C +   8 = 0x1394      ... then a 32-byte gap to 0x13B3        [AA-5]
0x13B4 + 256 = 0x14B4      Bank2048 ends exactly where Bank512 begins
0x14B4 +  64 = 0x14F4      Bank512 ends exactly where Primary begins
Primary spans 0x14F4 .. 0x1533
```

### The bit arithmetic

Every query and setter uses the same shape:

```c
bool PersistentFlag_QueryBank2048(int flag_id)
{
    if (flag_id < 0x800 && flag_id >= 0) {
        adj  = flag_id >> 0x1F & 7;            // sign-correction for negative ids
        idx  = flag_id + adj;
        base = SaveImage_GetPersistentPayloadBase();
        return (*(byte *)(base + (idx >> 3) + 0x13B4)
                & (1 << ((idx & 7) - adj & 0x1F))) != 0;
    }
    return false;
}
```

```c
void PersistentFlag_SetPrimary(int flag_id, int enabled)
{
    if (flag_id - 2U < 0x1FE) {                // ids 2..511 only
        adj  = flag_id >> 0x1F & 7;
        idx  = flag_id + adj;
        byte mask = 1 << ((idx & 7) - adj & 0x1F);
        base = SaveImage_GetPersistentPayloadBase();
        if (enabled) *(base + (idx >> 3) + 0x14F4) |=  mask;
        else         *(base + (idx >> 3) + 0x14F4) &= ~mask;
    }
}
```

> ### 2026-09-08 — the sign correction is real, and four accessors have no guard in front of it
>
> This document noted the sign-correction idiom and stopped there. Censusing the bound test of
> all eleven bank accessors shows **seven reject a negative id and four do not**:
> `QueryBank2048` and both `Bank512` queries add `test ecx,ecx / js`; `SetPrimary`,
> `SetBank2048` and both `Bank512` setters use an **unsigned** `ja`. **The four `Bank64`
> accessors use a signed `jl`/`jge` and add nothing**, so a negative id reaches the
> arithmetic — and in the two setters, `movsxd rcx, edi` then
> `or byte [rax + rcx + 0x1384], bl` **writes before the bank**: `id = -16` lands on payload
> `+0x1382`, `id = -1024` on `+0x1304`.
>
> **Latent, not demonstrated.** No caller was found that passes a negative; the shipped ids
> are `u16`. Full table and the arithmetic worked through by hand in
> [the contract](CONTRACT-persistent-flag-banks.md) §10. `DX-1`.

`flag_id >> 0x1F & 7` is 0 for any non-negative id, so it is a compiler-emitted sign correction for
the division-by-8, not a semantic field. **Out-of-range ids fail closed** — a query returns
`false`, a setter does nothing.

### One encoded id, two different lookups

`PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` takes an *encoded* id and switches on a bit:

```c
bool PersistentFlag_QueryPrimaryOrAuthoredThresholdGate(uint encoded_flag_id)
{
    index = encoded_flag_id & 0x3FFF;                    // low 14 bits

    if ((encoded_flag_id >> 0xE & 1) != 0)               // bit 14 set
        return PersistentFlag_QueryAuthoredThresholdSchedule(index);

    if (index < 0x200) {
        if (index == 0) return true;                     // reserved: ALWAYS
        if (index == 1) return false;                    // reserved: NEVER
        base = SaveImage_GetPersistentPayloadBase();
        return (*(byte *)(base + (index >> 3) + 0x14F4)
                & (1 << (encoded_flag_id & 7))) != 0;
    }
    return false;
}
```

Three things this establishes exactly:

**Bit 14 is a mode bit — and it switches between two completely different storage systems.** Clear
means "read the Primary flag bank in the save". Set means "consult the authored threshold schedule",
which **does not read the save at all** — see §2's threshold-schedule section below.

**Flag 0 is a hardwired `true` and flag 1 a hardwired `false`.** They never touch storage. An
authored condition can express *always* or *never* by naming ids 0 and 1.

**The low 14 bits are the index**, so a single 16-bit authored value carries both mode and index.

### The authored threshold schedule — not a flag lookup

`PersistentFlag_QueryAuthoredThresholdSchedule` is named as though it belonged to the flag system.
**It does not touch the save payload.** It reads a table of authored thresholds and compares them
against a single field variable:

```c
bool PersistentFlag_QueryAuthoredThresholdSchedule(int index)
{
    if (!g_table) return false;
    if (index >= *(u16 *)(g_table + 8)) return false;          // entry count
    off = *(u16 *)(g_table + 10 + index * 2);                  // per-index offset
    if (off == 0) return false;                                 // 0 = no schedule
    p = g_table + off;
    v = FieldData_GetVariable0();                               // the progress variable
    result = false;
    for (;;) {
        entry = *p;
        if ((short)v < (entry & 0x7FFF)) return result;          // below this threshold: stop
        p++;
        result = !result;                                        // TOGGLE at every crossing
        if ((short)entry < 0) return result;                     // bit 15 marks the last entry
    }
}
```

**The answer is the parity of how many thresholds the progress variable has passed.** Each entry is
a `u16`: bits 0-14 a threshold, bit 15 the end-of-list marker. So an authored condition can be true
**only between two story points** — on at the first threshold, off at the second, on again at the
third.

That is the mechanism behind a condition that is live for one stretch of the game and dead after it:
*this NPC has this line only until you finish that quest.* A plain flag cannot express it, because a
flag never goes back.

**The table is `mapjumpgroupflagrom.bin` (2026-09-29, SWE2-DATA, `OPUS-REQ-DATA-BUCKET-MEMBER-FORMATS`).**
`00378540` requests it as kind 9 index `0xA` (`0037870A` / `0037876F`); the completion `00378BA0`
stores the pointer in `g_table` = **`02ADD0C8`** through `mov eax, ecx`, so only its low 32 bits
(the §8f truncation convention). The body above is its only reader (`00377976` loads `02ADD0C8`;
`003779B5` / `003779D1` mask `0x7FFF`); the other reference is the teardown store at `00377D15`.
All nine locale copies are byte-identical, 856 bytes:

```struct FlagRomHeader base=file size=0xA
+0x00  char[8]  magic          'FLAGROM1' - never compared in .text
+0x08  u16      count          152 - the entry count the body bounds the index by
```

then `u16 offset[152]` from `+0x0A` (from file start, ascending, none zero, `offset[0]` = the table
end `0x13A`), then the records: `u16` lists, bits 0–14 a threshold, bit 15 on the last entry only
(271 words; `10 + 2·152 + 2·271 = 856`). Record lengths: 48 of one entry, 98 of two, 1 of three, 3
of four, 2 of six. Worked example: record `0x67` (the highest index any gate call site uses) is
`[300, 306|END]`, true exactly while `300 ≤ variable < 306`. It is a **different layout** from its
`FLAG`-tagged sibling `mapjumpgroupinit.bin` (`FLAGDEF1`, §8f) — the shared leading `FLAG` is a
prefix, not a format. Check: [`b1_flagrom.py`](../_index/candidates/bucket-members-0929/checks/b1_flagrom.py)
(31 checks, FAILS 0).

**The variable it compares against is not a flag.** `FieldData_GetVariable0` (`00265270`, 22
callers) returns the first `u16` of the current field's authored variable block, or `0` when the
block is absent:

```c
u16 FieldData_GetVariable0(void)
{
    if ((g_fieldFlags & 1) == 0) return 0;
    if (g_fieldVariables == NULL) return 0;
    return *(u16 *)g_fieldVariables;
}
```

**`0xFFFF` is a sentinel and nine call sites use it.** `0xFFFF` has bit 14 set, so it is a threshold
query with index `0x3FFF` = 16,383 — which fails the entry-count bound unless the authored table has
more than sixteen thousand schedules. Every index actually observed in the binary is `<= 0x67`. So
`gate(0xFFFF)` is **false**, and it is how a caller says "no condition here". *Whether a given caller
reads that as "never" or as "absent" depends on its own polarity and is not asserted.*

**The encoded ids that actually appear**, harvested from the 32 call sites of the gate:

```
threshold queries (bit 14 set)  0x4004 0x4006 0x4007 0x4008 0x4009 0x400A 0x400B
                               0x400C 0x400D 0x4010 0x4011 0x4067   and 0xFFFF
Primary bank reads (bit 14 clear)  0x0001 0x0002 0x0054 0x005E 0x006F 0x0107
```

### Worked example — the save header call

The save finalizer calls this gate with `0x400B`, documented earlier without knowing what it meant:

```
0x400B  =  0100 0000 0000 1011
             ^bit 14 set          -> authored threshold schedule
              low 14 bits = 0x000B = 11
```

So `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate(0x400B)` is **threshold-schedule query
number 11**, not a flag read at all. That closes **V-5**.

## 3. Key addresses

| Address | Name | Size | Verified |
|---|---|---:|---|
| `0032A8A0` | `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate` | 122 B | ✅ read |
| `0032A930` | `PersistentFlag_QueryBank2048` | 100 B | ✅ read |
| `0032A9A0` | `PersistentFlag_QueryBank64A` | 93 B | ✅ read |
| `0032AA60` | `PersistentFlag_QueryBank512Low` | 100 B | ✅ read |
| `0032AAD0` | `PersistentFlag_QueryBank512High` | 104 B | ✅ read |
| `0032AB60` | `PersistentFlag_SetPrimary` | 121 B | ✅ read |
| `0032ABF0` | `PersistentFlag_SetBank2048` | 119 B | ✅ read |
| `0032AA00` | `PersistentFlag_QueryBank64B` | 93 B | ✅ read |
| `0032AC70` / `0032ACF0` | `PersistentFlag_SetBank64A` / `64B` | 116 B | ✅ read |
| `0032AD70` / `0032ADF0` | `PersistentFlag_SetBank512Low` / `High` | 119/123 B | ✅ read |
| `00377970` | `PersistentFlag_QueryAuthoredThresholdSchedule` | 127 B | ✅ read — §10 |
| `00379160` | `PersistentFlag_ApplyAuthoredInitialPrimarySet` | 86 B | ✅ read — §8f |
| `00377440` | `EventMemory_QueryDefinitionIdAbsent` | 62 B | ✅ read — [event memory](event-memory-at-actor-bind.md) §2 |
| `02ADD0A8` / `02ADD0D0` | the two authored list globals | — | `eventmemorylist.bin` / `mapjumpgroupinit.bin`, §8f |
| `002EF2D0` | `SaveImage_ResetPersistentPayloadAndApplyAuthoredInitialFlags` | 38 B | ✅ read — §8f (owner `Save_Load_Settings`) |

> **All 15 functions the ledger assigns to `Story_Event_Quest_Hunt` are now read individually**
> — disposition **A** for the category's entire owned population. The three `partial` rows above
> were stale: two had been read by later passes of this document and its sibling without the
> table being updated, and the third is read in §8f. `002EF2D0` is listed because it is the
> caller, though it is owned elsewhere.

## 4. Data structures and formulas

```
Save persistent payload  (base = SaveImage_GetPersistentPayloadBase() = activeBuffer + 0x200)

  +0x1044   i32     active or pending field (area) id        [from the hub document]
  +0x1384   u8[8]   Bank64A          ids 0..0x3F
  +0x138C   u8[8]   Bank64B          ids 0..0x3F
  +0x1394   u8[32]  UNKNOWN - 256 flags' worth, unexplained    [AA-5]
  +0x13B4   u8[256] Bank2048         ids 0..0x7FF
  +0x14B4   u8[64]  Bank512          ids 0..0x1FF  (Low = 0..0xFF, High = 0x100..0x1FF)
  +0x14F4   u8[64]  Primary          ids 2..0x1FF
  +0x1534   u8      the saved music-track override (verb 0x471)                    [AA-8]
  +0x1535   u8      written-only: 1 by the options apply, any by debug_setscreenmode [AA-8]
  ---- end of payload at +0x1537; total length 0x1538 = 5,432 bytes             [§8f]
```

**Bit addressing**, identical in every bank:

```
byteOffset = bankBase + (id >> 3)
bitMask    = 1 << (id & 7)

query(id) = (payload[byteOffset] & bitMask) != 0
set(id,1) : payload[byteOffset] |=  bitMask
set(id,0) : payload[byteOffset] &= ~bitMask
```

**Encoded gate id** (16-bit authored value):

```
bit 14      : 0 = Primary flag bank, 1 = authored threshold schedule
bits 13..0  : index

gate(v) = (v & 0x4000) ? thresholdSchedule(v & 0x3FFF)
        : (v & 0x3FFF) == 0 ? true
        : (v & 0x3FFF) == 1 ? false
        : (v & 0x3FFF) < 0x200 ? primaryBit(v & 0x3FFF)
        : false
```

**Range guards — all fail closed:**

```
Bank2048    0 <= id < 0x800
Bank64A     0 <= id < 0x40
Bank512     0 <= id < 0x100 per accessor half (Low, High+0x100)
Primary     2 <= id < 0x200          (expressed as: id - 2u < 0x1FE)
```

## 4b. The payload map, and where the banks sit in it

The five bank offsets were re-derived by censusing **every** caller of
`SaveImage_GetPersistentPayloadBase` (70 of them) and recording each displacement applied to the
returned pointer. All five reproduce exactly, and nothing else in the binary reaches them:

```
+0x1044 .. +0x105C   WorldTransition state block - field id, destination, previous field,
                     previous destination, options, transition field   (7 dwords)
+0x1060 .. +0x1064   a byte-flag cluster; +0x1062 alone has 29 access sites
+0x1164, +0x1364     unexplained
+0x1384, +0x138C     Bank64A, Bank64B
+0x1394 .. +0x13B3   THE GAP - no accessor, by either route              [AA-5]
+0x13B4              Bank2048
+0x14B4              Bank512
+0x14F4              Primary
+0x1534, +0x1535     a live field immediately after Primary              [AA-8]
                     ...and the payload ends at +0x1537: 0x1538 bytes    [§8f]
```

**The gap is confirmed by two disjoint censuses.** The payload base is
`SaveImage_GetRawSaveBufferBase() + 0x200`, so code can reach the same bytes without the payload
accessor — that escape route was checked, and its 28 callers touch 36 displacements, **none of them
in the gap**. Neither census would see a pointer stored to memory and read back later, nor a bulk
`memcpy` over the whole payload; that limit is stated rather than assumed away.

## 4c. The banks in one table: what each is for, who touches it, what starts it *(synthesis, 2026-09-18, FABLE)*

*One new reading, marked below; otherwise sections 2, 4, 7, 8b and 8f and two sibling pages hold these facts separately; this is the one
table a reimplementer or a save editor needs. Offsets are in the persistent payload (active buffer `+0x200`).*

| bank | offset, size | ids | what it is for | native readers and writers | script access | state on a new game |
|---|---|---|---|---|---|---|
| `Primary` | `+0x14F4`, 64 B | `2`..`0x1FF`; id 0 reads *always*, id 1 *never*, neither touches storage | **the map-jump-group flags**, in the game's own words (verbs, this section's note below): the general story and world-state bank, and the only one native Input, UI, Save and Story code consults | many native readers; also reachable as AI operand kind 8; bit 14 of a query id switches to the authored threshold schedule, which is not a flag read at all (section 2) | `setmapjumpgroupflag` 4,625 uses, `releasemapjumpgroupflag` 4,610, `ismapjumpgroupflag` 3,667 | payload zeroed, then **52 flags set** from `mapjumpgroupinit.bin` - 53 listed, the leading 0 dropped by the setter's own range guard (`DS-1`) |
| `Bank512` | `+0x14B4`, 64 B | `0`..`0x1FF`, two 256-id accessor pairs over one region | authored field-action and trigger state - **treasure**, by its verbs | set by the nearby-field-action trigger in combat, queried by a combat-action function (section 8b) | `istreasureflag` (the high half, 26 uses), `istreasurebattleflag` (the low half, no shipped use) | zero |
| `Bank2048` | `+0x13B4`, 256 B | `0`..`0x7FF` = the NPC-name dictionary's id space | **names the player has been told**: bit `id` makes name pair `id` show its second, personal string | read by the display-name resolver and the shop's two name readers; **set by the message-window opener** for the actor being spoken to | `settalknpcname`, `releasetalknpcname`, `istalknpcname` (57 / 79 / 1 shipped uses) | zero: every name starts generic |
| `Bank64A` | `+0x1384`, 8 B | `0`..`0x3F` | named for the airship by its verbs - *appear* | none | `setshutoralappear`, `clearshutoralappear`, `isshutoralappear` - **no shipped use** | zero, and nothing shipped changes it |
| `Bank64B` | `+0x138C`, 8 B | `0`..`0x3F` | the same - *enable* | none | `setshutoralenable`, `clearshutoralenable`, `isshutoralenable` - **no shipped use** | zero, and nothing shipped changes it |
| the gap | `+0x1394`, 32 B | - | no accessor by any route (`AA-5`) | none found | none found | zero |
| the tail | `+0x1534`..`+0x1537` | - | live, outside every bank; meaning open (`AA-8`) *(2026-09-26 (FABLE, Claude Opus 5.5): `AA-8` ANSWERED - `+0x1534` is the saved music-track override, `+0x1535` is written and never read, `+0x1536`/`+0x1537` are untouched; see the field map above)* | six access sites | - | zero |

**The verb join behind the two bold names (new on 2026-09-18, the one addition this section makes).** Joining the accessors' script-handler callers to [the verb table](../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv): the handlers of `setmapjumpgroupflag` and `releasemapjumpgroupflag` pop one integer and tail-jump to `PersistentFlag_SetPrimary` with 1 and 0, and `ismapjumpgroupflag`'s calls the Primary query; `istreasureflag`'s calls the `Bank512` high query and `istreasurebattleflag`'s the low. In the 1,114 decompiled `us` scripts the three map-jump verbs are used 12,902 times over **330 distinct literal ids, from 2 to `0x402A`** - the minimum is the setter's own lower bound and the ids above `0x4000` are threshold queries - and **46 of the 52 flags `mapjumpgroupinit.bin` pre-sets are referenced by a script**, which ties that file's name to this bank from both sides. The verbs `setnaviicon`, `clearnaviicon` and `isnaviicon` share the same three handler addresses and have no shipped use. So `DS-1`'s *what the 52 gate* has its vocabulary - they are map-jump-group flags the scripts test and flip - though which map jumps each id controls is per-script reading that was not done.

**Per-id census (added 2026-09-18, FABLE).** [mapjump_flag_census.py](members/mapjump_flag_census.py) and [mapjump-flag-census.tsv](members/mapjump-flag-census.tsv) list every id the three verbs are given as a literal: **328 flag ids and 2 threshold-query ids**, 12,900 literal calls and 2 with a computed id, with each id's set / release / is counts, script count and areas. Two shapes stand out and are left as observations: ids `0x2`..`0x9` are each set and released exactly 13 times by the same 13 scripts, a block handled as a unit; and the busiest pre-set id, `0x80`, is set 162 times, released 243 and tested 243 across 81 scripts. Six of the 52 pre-set ids are named by no script literally (`0x56`, `0x65`, `0x66`, `0x10B`, `0x148`, `0x14B`), which leaves their readers to native code or computed ids. What each id *means* is still per-script reading; the table says where to read.

**Where the other half is (added 2026-09-18, FABLE).** The native consumers of these flags that fit the verbs' name are the map screens: on [the map-screens page](../16-UI/Map-Screens/the-map-screens-and-their-shared-map-data.md) every node, link and 24-byte point entry of the shared map data carries gate ids in its words `+0xE` / `+0x12` / `+0x14`, and the row builders query each through this bank's accessor to decide whether the entry is available or locked. One script read for shape, `alc_c01`: a per-frame loop switches on the current map and keeps the pairs `127` / `128` and `0x164` / `0x165` **mutually exclusive**, choosing a side from a boss-defeated global and a `scratch1` gate variable - two alternative sets of connections for one place, selected by which flag of the pair is up. ~~*Not checked:* that the gate ids stored in the map data are the same ids the scripts flip.~~ **Checked 2026-09-18 (FABLE): the join holds, and it says what one of the fields is for.** [lmap_gate_join.py](../16-UI/Map-Screens/members/lmap_gate_join.py) parses `menumap_location.bin` with the native layout (control: it reproduces the 384 A and 111 B point entries) and intersects the point entries' persistent gate words with the scripts' flag census ([lmap-gate-join.tsv](../16-UI/Map-Screens/members/lmap-gate-join.tsv)). **Word `+0x12`: 51 distinct ids, 2 of them threshold-form and 49 inside the bank's `2`..`0x1FF` range, and all 49 are flags a shipped script sets - and not one of the 49 is ever released.** So `+0x12` is a one-way *revealed* flag: a point appears on the map once some zone script has set its flag, and stays. Word `+0xE`: 11 distinct ids - 2 in range (both script-set, never released), 4 in the threshold form with bit 14 set (story-progress gates, not flags) and 5 with bit 15 set, a form this page does not read. Word `+0x14`, by contrast, is **not** a flag id in a point entry: 78 of its 79 distinct values lie outside the bank's range, which agrees with the map-screens page's other reading of it as a link-selector byte; the `PersistentFlag(word[+0x14])` rows of that page's section 4 belong to the other tables they name.

**Behaviour a reimplementation must keep.** (1) The whole `0x1538`-byte payload is cleared by one `memset` and the
initial Primary set applied immediately after, before the first frame (section 8f). (2) Every setter range-checks
and silently ignores an id outside its bank; nothing reports the failure, so an authored id out of range is a
no-op, not an error. (3) A name bit is set by *opening a conversation*, with no script involved, so an NPC's name
changes the first time the player speaks to them even in a field whose script never mentions names. (4) None of
this is the script VM's `scratch` storage: the completed-group word, for instance, lives in `scratch1`, which
every field transition clears ([the storage-class page](../01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md)),
while these banks ride in the save.

**Still not known:** which map jump each Primary id controls; the gap and
the tail; and whether the airship reading of `shutoral` is right - it is an inference from a romanised identifier
with no shipped use to test it against.

## 5. Call chain

```
authored script / event / world logic asks "has this happened?"
  -> PersistentFlag_QueryPrimaryOrAuthoredThresholdGate(encodedId)
     -> bit 14 set  : PersistentFlag_QueryAuthoredThresholdSchedule(index)
     -> bit 14 clear: index 0 -> true, index 1 -> false,
                      else read Primary bank at payload +0x14F4

something happens
  -> PersistentFlag_Set<Bank>(id, 1)
     -> payload byte |= bit                    <- now part of the save

new game / save-image reset
  -> 002EF2D0  SaveImage_ResetPersistentPayloadAndApplyAuthoredInitialFlags
     -> memset(payloadBase, 0, 0x1538)              every bank goes to zero
     -> tail-jump PersistentFlag_ApplyAuthoredInitialPrimarySet
        -> for each u16 id in mapjumpgroupinit.bin: PersistentFlag_SetPrimary(id, 1)
                                                                             [§8f]

save
  -> SaveImage_FinalizeHeaderAndChecksum
     -> PersistentFlag_QueryPrimaryOrAuthoredThresholdGate(0x400B)   <- threshold #11
  -> the whole payload, flags included, is captured and written
```

**Upstream:** the event/script VM and world logic.
**Downstream:** the save image — these bits *are* save state, not a mirror of it.

**Also upstream, and unexpected:** the gate has **32 callers**, one of which is
`InputGameplay_ArbitrateDigitalInputAndModalState` — **story flags participate in input
arbitration**, not only in event and dialogue logic.

**Do not confuse with:** the Save category, which serialises the payload but does not own what the
bits mean. The GFZ makes this boundary explicitly and it is correct.

## 6. Modding notes

- **Story progress is bits at fixed save offsets.** A save editor can read and write them directly
  once the container is decoded: Primary at payload `+0x14F4`, Bank2048 at `+0x13B4`.
- **Payload offset, not file offset.** Payload base is `activeBuffer + 0x200`, and the on-disk
  `SAFH` file is encoded — see the save document. You cannot seek to `0x14F4` in the file.
- **Flag 0 = always, flag 1 = never.** Do not reuse them, and do not expect a bit to exist for them.
- **Primary skips ids 0 and 1** — its usable range starts at 2 even though storage begins at bit 0.
- **Bit 14 of an authored id changes the meaning entirely.** A value like `0x400B` is not flag 11.
- **Everything fails closed.** An out-of-range query is `false`, an out-of-range set is a no-op —
  so a corrupt id silently does nothing rather than crashing.
- **XIIOnline:** these bits are per-client save state with no reconciliation. Two players will hold
  different story flags; any shared-world model must decide whose progression is authoritative
  before a flag gates anything visible. Because they are plain bits at known offsets, they are also
  the easiest progression state to synchronise deliberately.

## 7. What is not known

- [x] **AA-8** (filed 2026-09-02 as a second `AA-6`; **renumbered 2026-09-08**, see below). The
      field at payload `+0x1534`/`+0x1535`, immediately after the Primary bank. Six access sites
      through the payload accessor and one through the raw buffer; outside every documented bank.
      **Bounded in §8f** — the payload is `0x1538` bytes, so this is its last four bytes and
      nothing follows. §4b, §8f, §10.
      *Narrowed 2026-09-14 (FABLE), from a displacement census of `+0x1534`–`+0x1537` (payload base) and
      `+0x1735` (raw buffer = payload `− 0x200`):*
      - **`+0x1534` is the saved music-track override.** It is set by `0026A720` (verb `0x471`); a negative
        argument clears `+0x1063` bit 6 and zeroes it. `002628B0` also clears it (`00262A65`–`00262A76`).
        `0025DBB6`, `00262029` and `0026DE41` read it in place of the field's track while bit 6 is set.
        [Save payload map, FG-3](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md);
        [area music](../18-Audio/how-the-music-changes-when-you-change-area.md).
      - **`+0x1535` is written and never read by displacement.** Its one store is `002EF370(b)` (buffer
        `+0x1735`, `002EF37D`). That store is reached from the options apply `002DDA30` ~~with its own argument~~
        (`002DDB4A`) and from verb `0x20D1` (catalog `debug_setscreenmode`, `0050D192`). A reader through a
        block copy is not excluded.
        *Corrected 2026-09-26 (FABLE, Claude Opus 5.5): the options apply passes the constant 1, not its argument.*
        `ebx` is set by `mov ebx, 1` at `002DDAC4` on every path, nothing between there and the call rewrites it, and
        no branch enters that stretch from outside. So every options apply writes 1, and only the debug verb can
        write any other value.
      - **`+0x1536` / `+0x1537`: no displacement access.**
      **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): the payload's last four bytes are one live byte, one written-only
      byte and two untouched bytes.**
      - `+0x1534` is the saved music-track override (above).
      - `+0x1535` is written with 1 by every options apply and with the script's integer by
        `debug_setscreenmode`, and **nothing reads it**. An image-wide census of every listed body, from its own entry,
        finds one access at raw `+0x1735` (the store) and none at payload `+0x1535`–`+0x1537`. Every payload `+0x1534`
        access is byte-wide, so none covers the bytes after it.
      - The three qword operands at `+0x1530` in the image sit on objects larger than the payload: a `lea` on a
        `0x1620`-stride battle-menu element that also has fields at `+0x153A` / `+0x153E`, and `0027CE70`'s `this`,
        which has fields at `+0x1550`, `+0x1578` and `+0x15EF`. The payload ends at `+0x1538`.
      - `+0x1536` / `+0x1537` have no access at any width, and are consistent with tail padding.

      The byte is saved with the payload but never consulted as data, so its name rests only on the verb's catalog
      name. The census limit: code handed the payload pointer by another function and reading it at a
      computed offset would not be seen. Control: `_index/candidates/aa8-payload-tail/payload_tail.py` (8 checks). Consumer check:
      `_index/candidates/aa8-payload-tail/consumer-check.md`.

- [x] ~~`Bank64B`'s payload offset.~~ **AA-1 CLOSED in section 8b — `+0x138C`.**
- [x] **UQ-138.** *(answered 2026-09-18, at the end of this item)* What each bank is *for*. Six banks with different capacities implies six different
      categories of memory (story, hunts, chests, dialogue...). **AA-2 — the highest-value
      unknown here.**
      *Register check 2026-09-14 (FABLE): the ledger's `AA-2` says ANSWERED, but its own text establishes one bank of six.*
      `Bank512` carries authored field-action and trigger state. `Primary` is read by Input, UI, Save and Story.
      `Bank2048`, `Bank64A` and `Bank64B` have no engine consumer, and their labels are unproven. So this box stays
      open, and the register verdict is queued for revision to PARTLY ANSWERED.
      *Narrowed 2026-09-18 (FABLE): a third bank is placed.* `Bank2048` is the told-names set, indexed by NPC-name id, read by the display-name resolver and written when a message window opens for an actor (the corrected paragraph in the caller census above). Three of six are now established - `Primary`, `Bank512`, `Bank2048`; `Bank64A` and `Bank64B` remain script-only with no label, and the 32-byte gap stays AA-5.
      **ANSWERED 2026-09-18 (FABLE): the script verbs that reach each bank carry authored names, and the names say what the three unlabelled banks are for.** Joining each accessor's script-handler callers to [the verb table](../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv): `Bank2048` is reached by **`settalknpcname`** (`0x399`), **`releasetalknpcname`** (`0x39A`) and **`istalknpcname`** (`0x39B`) - the told-names set, in the game's own words, agreeing with the native readers and writer found earlier today; `Bank64A` by **`setshutoralappear`** / **`clearshutoralappear`** / **`isshutoralappear`** (`0x2FA`, `0x2F9`, `0x2F8`); `Bank64B` by **`setshutoralenable`** / **`clearshutoralenable`** / **`isshutoralenable`** (`0x2FD`, `0x2FC`, `0x2FB`). Each handler is the only script-side caller of its accessor in that role, so the join is one-to-one. *Shipped use, from the 1,114 decompiled `us` scripts:* `settalknpcname` 57 times in 23 scripts (22 distinct literal ids), `istalknpcname` once, `releasetalknpcname` 79 times in a single script that also declares a debug-director actor; **the six `shutoral` verbs are never used**, so nothing in the shipped `us` scripts ever touches `Bank64A` or `Bank64B` and those 128 bits stay as the new-game `memset` left them. *Reading of the name, labelled as such:* `shutoral` transliterates the airship's name (Strahl), which would make the two banks *where it appears* and *where it may be used* - an inference from a romanised identifier, with no shipped use to test it against. **So:** `Primary` - general story and system state, the only bank native Input, UI, Save and Story code reads, with 52 bits pre-set on a new game (DS-1); `Bank512` - authored field-action and trigger state; `Bank2048` - NPC names told; `Bank64A` / `Bank64B` - two authored 64-bit sets named for the airship and unused in the shipped scripts; and the 32-byte gap is AA-5. Authored names plus a corpus census; static for the joins.
- [x] ~~What the authored *threshold schedule* is, and how it differs from a flag.~~ **AA-3
      CLOSED in §10** — it is not a flag lookup at all: a list of authored `u16` thresholds
      compared against `FieldData_GetVariable0()`, and the answer is the **parity** of how many
      have been passed, so an authored condition can be true only *between* two story points.
- [x] ~~Why `Bank512` is split Low/High.~~ **AA-4 CLOSED in section 8b** — one 512-flag bank, two
      256-flag accessor pairs over the same region.
- [x] **AA-5.** The 32-byte gap at `+0x1394`-`+0x13B3` (256 flags' worth) between `Bank64B` and `Bank2048`.
      **AA-5 — now exactly located and sized.**
      **ANSWERED 2026-09-21 by SWE2-CONTRACT on [the flag-bank contract](CONTRACT-persistent-flag-banks.md) (item 2); noted here 2026-09-26 (FABLE, Claude Opus 5.5): dead space by all three access routes.** The payload sits at the fixed address `02164480`, so the gap is absolute `02165814`–`02165833`. An operand-level census of all 163 helper calls in ~~104~~ 98 functions *(corrected 2026-10-02, FABLE, on OPUS's byte verdict C-V13, [record](../_index/candidates/opus-story-readiness-fixes-1002/byte-verdicts.md))* finds no displacement in the gap by either base and no rip-relative operand into the payload, and no `lea` forms a pointer into it. The bytes exist only to be zeroed by the `0x1538` memset: reserved space between `Bank64B` and `Bank2048`, not a bank.
- [x] ~~`EventMemory_QueryDefinitionIdAbsent` and its global `DAT_02ADD0A8`.~~ **AA-6 CLOSED** —
      the function is decoded in full in
      [event memory at actor bind](event-memory-at-actor-bind.md) §2, and §8f names what fills
      the list: the shipped `eventmemorylist.bin`, resource `(kind 9, index 41)`, 26 bytes,
      published by `00378A50`.
- [x] **DS-1.** *(answered 2026-09-18, at the end of this item)* Which ids `mapjumpgroupinit.bin` (`(9, 40)`, 116 bytes, room for 53) and
      `eventmemorylist.bin` (`(9, 41)`, 26 bytes, room for 8) actually carry. Both are inside the
      31 GB `SRYK` archive; extracting them answers it outright. §8f.
      **ANSWERED 2026-09-18 (FABLE), from the extracted archive, parsed with the readers' own layout (`u16` count at `+8`, `u16` entries from `+0x0A`).** **`mapjumpgroupinit.bin`** - magic `FLAGDEF1`, count 53, and `10 + 2 * 53 = 116` bytes exactly. Its entries are `0x0`, `0x56`, `0x65`-`0x66`, `0x70`, `0x79`-`0x7A`, `0x80`, `0xFC`, `0x108`, `0x10B`-`0x10C`, `0x11C`, `0x12C`-`0x134`, `0x136`-`0x137`, `0x13A`-`0x155` and `0x158`. The first entry is **0, which the setter's `2 <= id <= 0x1FF` guard drops** - the case section 8f predicted - so a new game starts with **52** Primary flags set, not 53, and 37 of them are the two dense runs `0x12C`-`0x134` and `0x13A`-`0x155`. All nine language copies (`ch`, `cn`, `de`, `es`, `fr`, `in`, `it`, `kr`, `us`) are byte-identical. **`eventmemorylist.bin`** - magic `EVMEMLST`, count 8, `10 + 2 * 8 = 26` bytes: `0x0`, `0x31`, `0x29C`, `0x29E`, `0x30E`, `0x367`, `0x368`, `0x390`, one copy under `common`; [the event-memory page](event-memory-at-actor-bind.md) had already recorded these eight. Both lists open with a zero entry, so the zero is the format's habit rather than an authored id. *Not established:* what the 52 flags gate - the file's name says map-jump groups, which is a name, not a reading of their consumers. Authored data.
- [x] **UQ-139.** The ten-byte publishers store `mov eax, ecx` — 32-bit — into globals their consumers
      dereference as 64-bit pointers. **Already open as `PROPOSED-repos2d-4`**, filed by
      [the field-record document](../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md);
      §8f only widens it from three publishers to five.
      **ANSWERED 2026-09-18 (FABLE, at `PROPOSED-repos2d-4` in that document); verified 2026-09-23
      (SWE2-CONTRACT).** The truncation *is* the resolve: `ImageAddress_ResolveRuntimePointer`
      `0020E600` is `mov eax, ecx; add rax, [01F83530]` and the base is zero ~~,~~ **at image load** *(scope corrected
      2026-09-25, FABLE, Claude Opus 5.5: one in-image store route, the texture-id writer's signed id `0xFFFB`, can
      write it and is undriven at the shipped width; "zero for the process's life" is supported, not proven —
      [the row-lookup contract](../02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md) §7)*, so the publisher's
      `mov eax, ecx` zero-extension and a reader's full-width dereference agree. All five §8f
      publishers are the same ten-byte shape on the same `0032E620` delivery chain, so the answer
      covers the widened family unchanged. *Re-verified here:* `01F83530` has exactly two
      rip-relative references image-wide — the `add` in `0020E600` and the `sub` in its inverse
      `0020E620` — is never `lea`-materialised, and carries no shipped value, so the base stays
      zero on shipped code; the same census resolves the `J-C`-class residual this file's
      siblings recorded for the same global.
- [x] ~~Whether hunts and the bestiary use these banks or separate storage.~~ **AA-7 ANSWERED 2026-09-12 (FABLE):** hunts are script conventions over these banks; the bestiary is a native 512-byte sighting / defeat block at save payload `+0xB404`, keyed by the class row's word `+0x52` — separate storage ([event memory at actor bind](event-memory-at-actor-bind.md) §3).

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| All banks live in the save persistent payload | every accessor calls `SaveImage_GetPersistentPayloadBase()` | 1 |
| Bank offsets `0x1384` / `0x13B4` / `0x14B4` / `0x14F4` | complete bodies of the five query functions and two setters | 1 |
| Layout is contiguous | `0x13B4+256 = 0x14B4` and `0x14B4+64 = 0x14F4`, arithmetic on read offsets | 1 |
| Bit addressing `(id>>3, 1<<(id&7))` | identical in every body read | 1 |
| Range guards, fail-closed | explicit bounds tests returning `false` / returning early | 1 |
| Bit 14 selects threshold-vs-flag | `(encoded_flag_id >> 0xE & 1)` branch in `0032A8A0` | 1 |
| Flag 0 = true, flag 1 = false | literal `return true` / `return false` before any storage read | 1 |
| `0x400B` is threshold #11 | `0x400B & 0x4000` set, `0x400B & 0x3FFF` = 11 | 1 |

### The contiguity check is doing real work

The three bank bases were read from three separately decompiled functions. Nothing forced them to
line up. That `0x13B4 + 256` lands exactly on `0x14B4`, and `0x14B4 + 64` exactly on `0x14F4`, is an
independent consistency check on both the offsets **and** the capacities implied by the names —
`Bank2048` really does occupy 2048 bits, `Bank512` really does occupy 512.

Had any offset been misread, the arithmetic would not close. This is the kind of corroboration that
a single function body cannot provide on its own.

### V-5 closed, V-1 advanced

This block was opened to fill an empty category and incidentally answered two save questions:

- **V-5 closed** — `PersistentFlag_QueryPrimaryOrAuthoredThresholdGate(0x400B)` in the save header
  path is authored threshold schedule #11.
- **V-1 advanced** — the payload interior now has 336 mapped bytes (`0x1384`–`0x1533`) plus the area
  id at `0x1044`, against 353,424 total. Still overwhelmingly unmapped, but no longer opaque.

### What is named but not proven

The bank *names* (`Bank64A`, `Bank2048`, `Primary`) are GFZ labels. The **capacities** they imply are
confirmed by the range guards read here, and the **offsets** are read from bodies — but the names do
not say what each bank stores, and nothing in this pass does either. **AA-2** records that gap rather
than guessing that Bank2048 is "story" and Bank512 is "hunts".

## 8b. Reopened 2026-09-02 - the complete bank map, and who uses each

The remaining accessors were read and every bank's callers were censused. **AA-1 and AA-4 are
closed; AA-2 is partly answered; AA-5 is now precisely bounded.**

### The full layout - contiguous but for one gap

| Bank | Payload offset | Flags | Bytes | Ends |
|---|---|---:|---:|---|
| `Bank64A` | `+0x1384` | 64 | 8 | `0x138B` |
| `Bank64B` | `+0x138C` | 64 | 8 | `0x1393` |
| *(gap)* | `+0x1394` | - | **32** | `0x13B3` |
| `Bank2048` | `+0x13B4` | 2048 | 256 | `0x14B3` |
| `Bank512` | `+0x14B4` | 512 | 64 | `0x14F3` |
| `Primary` | `+0x14F4` | 512 | 64 | `0x1533` |

**AA-1 closed:** `Bank64B` is at `+0x138C` - exactly `0x1384 + 8`, immediately after `Bank64A`,
as the contiguity of the rest predicted.

**AA-4 closed: `Bank512Low` and `Bank512High` are not two banks.** They are two accessor pairs over
**one** 512-flag region at `+0x14B4`. The `High` setter carries a literal `0x100` alongside the same
`0x14B4` base, and both guard `id < 0x100` - so `Low` covers ids 0-255 and `High` covers 256-511 of
a single 64-byte block. That is why both reported the same base offset in the first pass.

**AA-5 sharpened:** the only discontinuity is a **32-byte gap at `+0x1394`-`+0x13B3`** - exactly
256 flags' worth - sitting between the two 64-flag banks and the 2048 bank. Still unexplained, but
now exactly located and sized.

### Who touches each bank

Every bank has an identical Script-VM surface: **one query handler and two setter handlers**. That
uniformity is itself a finding - the VM exposes the same three opcodes per bank.

| Bank | VM query | VM setters | Non-VM consumers |
|---|---|---|---|
| `Primary` | `0034E0B0` | `0034DD90`, `0034EE20` | **Input, UI x2, Save, Story** |
| `Bank2048` | `0034E980` | `0034DFA0`, `0034E320` | none |
| `Bank64A` | `0034D940` | `0034CA20`, `0034D190` | none |
| `Bank64B` | `0034DDB0` | `0034CD40`, `0034D600` | none |
| `Bank512` | `00354540` / `00354000` | `00353750`, `00353BD0`, `00352EA0`, `00353390` | **CombatAction** |
| | | | |

The VM handlers also split into two address clusters - `0x0034Cxxx`-`0x0034Exxx` for
Primary/2048/64A/64B, and `0x00352xxx`-`0x00354xxx` for the 512 pair. The 512 region is handled
somewhere structurally separate.

### What that constrains - AA-2, partly

**`Primary` is the bank the engine itself consults.** Its named non-VM callers:

```
InputGameplay_ArbitrateDigitalInputAndModalState   (Input)   - gates player input
FUN_00281AE0, FUN_0029C530                         (UI)      - menu state
SaveImage_FinalizeHeaderAndChecksum                (Save)    - stamped into the save header
PersistentFlag_ApplyAuthoredInitialPrimarySet      (Story)   - authored new-game state
```

~~30 query callers~~ 32 callers of the gate, Primary's only reader (59 direct call sites in 31 functions, plus one caller through the gate's thunk) *(corrected 2026-10-02, FABLE, on OPUS's byte verdict C-V14, [record](../_index/candidates/opus-story-readiness-fixes-1002/byte-verdicts.md))*, against 4 setters: **written rarely, read constantly, and by subsystems outside
the script VM.** It is the general-purpose game-state bank.

**`Bank512` is written by combat.** `BattleUnit_TryTriggerNearbyAuthoredFieldAction` (`002F8060`)
*sets* a `Bank512Low` flag, and `FUN_002FA740` (CombatAction) queries it. That makes `Bank512` the
bank carrying **authored field-action / trigger state** rather than narrative progress.

~~**`Bank2048`, `Bank64A` and `Bank64B` have no engine consumer at all** - only the script VM reads or
writes them. They are pure authored state, invisible to every other subsystem.~~

> **CORRECTED 2026-09-18 (FABLE): true of `Bank64A` and `Bank64B`, false of `Bank2048`.** **`Bank2048` is the set of NPC names the player has been told, and the engine both reads and writes it.** A raw call index of its two accessors finds native callers this page's census missed. *Readers* of `PersistentFlag_QueryBank2048`: the display-name resolver `00263990(actor)` and its by-id twin `002639E0`, which strip bit 14 from the actor's name id at `+0x102`, query bit `id`, and pass `(id, flag)` to the dictionary lookup - the bit selects the second string of name pair `id` ([the NPC-name dictionary](../04-Actor-Entity/Actor-Names/the-npc-name-dictionary.md) section 2.3); and the two name-source readers on the shop page, `002B9C70` and `002BA530`. *Writer* of `PersistentFlag_SetBank2048`: the message-window opener `002E16B0(actor, ...)`, whose first act for a non-null actor is `SetBank2048(actor word +0x102, 1)` (`002E16DF`..`002E16EB`); the setter rejects any id above `0x7FF` unsigned (`0032ABF7`), which also discards the negative ids that mean a literal name pointer. So opening a conversation with an actor sets that actor's name bit for good, and every later display of the name takes the pair's other string. The bank's index space is the name dictionary's id space, which is why it needs 2,048 bits. The script-side accessors (`0034E980` query; `0034DFA0`, `0034E320` set) let authored scripts do the same by hand. Static, from the bodies. What the two strings are is already on the dictionary page from the shipped `npcdic.bin`: 247 of 1,141 pairs differ, a generic tag first and a personal name second (`Rabanastran` / `Arryl`), so the bit is *this person's name is known*.
> The census that produced the struck sentence counted callers by owner label; the four native readers and the writer sit in functions with no owner label, which is how a *genuine negative* two paragraphs below came to be neither. `Bank64A` and `Bank64B` were re-checked the same way and do have only script-handler callers (one query and two setters each).

### The limit of this inference, stated plainly

This is a **caller census**, not a semantic proof. The evidence standard bans inferring a callee's
ownership from its callers, and that ban is respected here: nothing above reassigns an owner.

What a caller census *can* support is a bounded claim about **usage**: which subsystems read and
write a bank is an observed fact, and "no engine subsystem touches `Bank2048`" is a genuine
negative. What it cannot support is the label - **nothing here shows that `Bank2048` holds "story"
flags or that `Bank64A` holds "hunts".** Those labels remain unproven, and **AA-2 stays OPEN** with
this usage evidence recorded as a constraint on the answer, not the answer.

## 8c. Reopened 2026-09-02 - audit pass 5: a 75/25 roll writes a permanent flag

Crossref audit pass 5 flagged one **NEW SINCE BASELINE** relationship for this document:
`RNG_Random_Selection`, from the edge `002F8060 -> 00379CD0`.

`BattleUnit_TryTriggerNearbyAuthoredFieldAction` had been cited three times in this database - as
the CombatAction consumer that *writes* a `Bank512Low` flag - **without ever being read**. The audit
caught that, so it was read.

```c
short BattleUnit_TryTriggerNearbyAuthoredFieldAction(unit, out_target_units, inout_target_count)
{
    fieldId = WorldTransition_GetActiveOrPendingFieldId();      // the area-id hub
    ...
    /* locate an authored field record near the unit (proximity gate) */
    ...
        roll = RNG_MT19937_NextU32_Thunk();
        if (roll % 100 < 0x4B)  chosen = record[3];             // 0x4B = 75  -> 75% branch
        else                    chosen = record[4];             //             -> 25% branch

        if (*(byte *)(record + 2) != 0xFF)                      // 0xFF = no flag to set
            PersistentFlag_SetBank512Low(record[2], 1);         // record it in the SAVE
        ...
}
```

### What this establishes

**A 75/25 split.** `roll % 100 < 0x4B` is exactly 75 - the record carries **two** alternative
outcomes and the common one is chosen three times in four.

**The outcome is written to the save.** `PersistentFlag_SetBank512Low` puts a bit in the persistent
payload at `+0x14B4`. So a randomised field action **permanently records that it happened**, and
`0xFF` is the sentinel for "this record sets no flag".

**AA-2 is confirmed for `Bank512`.** Section 8b inferred from a caller census that `Bank512` carries
authored field-action / trigger state. This is the setter call in context, and it does exactly that.
The constraint is now backed by a read body, not only by who calls what.

**The authored record layout**, as far as it is used here:

```
field-action record   (short *)
  [2]  u8     persistent flag id to set; 0xFF = none
  [3]  short  outcome chosen on the 75% branch
  [4]  short  outcome chosen on the 25% branch
```

> *Read further 2026-09-12 (FABLE; AF-1 narrowed, AF-2 and AF-3 answered).* **These records are the
> area's traps.** The function walks the table `[022BE948]` — `count` at `+0`, clamped to 32, and
> `u32` offsets from `+4` (`002F80BC`–`002F80C5`, `002F81A8`–`002F81B2`), built for the field by
> `002FA740` — skipping records whose bit is clear in the field's mask (`bt r15d, i`, from the
> 12-byte per-field entries at `02EC3EA0`, `002F8160`–`002F820E`). Each record's **shorts `[0]` and
> `[1]` are its position ÷ 10** (`002F81BE`–`002F81E9`, the divisor `10.0` at `008F8180`) and the
> **proximity gate is `1.3`** — `comiss xmm7 = [00901B34] = 1.29999995` against the distance
> `003A1920` returns from the actor's position (`002F81EF`–`002F81F7`), so "about 1.3" was exact.
> The MT19937 roll picks **short `[3]` (75 %) or `[4]` (25 %)** — bytes `+6` / `+8` — and that value
> is a **trap-message kind** handed with the actor to `0046A9D0`, which posts battle message
> row 3 for `0x103` (*"… triggered a trap. Your pockets feel lighter…"*), row 1 for `0x104`
> (*"… healing nearby allies"*), row 2 for `0x105` (*"… energizing nearby allies"*) and row 0 for
> anything else (*"… triggered a trap"*) ([the battle message table](../07-Combat-Action/Post-Result-Events/the-post-result-events-and-the-battle-message-table.md)). Then `002FB8C0(record, unit, &out)`
> ~~applies the trap's effect~~ **gathers the units the trap reaches** (read whole below), `003EC700(i, 3)`
> retires the trap's world marker, the record's bit is cleared in the field mask and
> the mask stored back (`002F8293`–`002F82A4`). The flag byte `+4` is set before the gather
> (`002F8243`–`002F8253`). ~~Bytes `+0x0A` onward are read by `002FB8C0` (`002FB8E0`) and remain the
> layout's residue.~~

> **AF-1 answered 2026-09-12 (FABLE): the trap record whole, where the table comes from, who arms it,
> and what each trap does.**
>
> ```
> trap record  (12 bytes; the table is {u32 count <= 32; u32 offset[count]} of these)
>   +0x00  s16  x / 10                        (002F81BE-002F81E9; 002FA82C)
>   +0x02  s16  y / 10
>   +0x04  u8   persistent flag id, 0xFF = none   (set on trigger, 002F8243-002F8253; a set flag stops re-arming, 002FA7E8-002FA7FA)
>   +0x05  u8   arm chance, percent                (roll % 100 < chance at field load, 002FA7FC-002FA81C)
>   +0x06  u16  action id, 75 %                     (002F8237)
>   +0x08  u16  action id, 25 %                     (002F823E)
>   +0x0A  u8   radius, world units; 0 = the triggering unit alone   (002FB8E0, 002FB9E2-002FB9F1)
>   +0x0B  u8   0 in every shipped record
> ```
>
> **Where the table lives.** `002FA740` takes it from `002641B0(0, 0)`: manager slot 0's script
> image, header **`+0x6C`** — ff12-script's `trapDataOff`, the option this page's sibling censused
> as "arity 1" — is `{u32 1; u32 packedRef}`, and the reference is a storage-class-tagged offset
> (`tag = bits 24–26`, `offset = bits 0–23`; `002641E4`–`00264233`, the same six-way base chooser
> `00265770` the variable classes use, [the storage-class page](../01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md)). Every shipped reference is **tag 3, the
> `msp` region** (`image + tableOff40`, [the section-000 page](../25-EBP-Script-Container/Bytecode-And-Opcodes/section-000-bytecode.md)). **Census over 1,114 scripts:** 389 carry a
> table; 143 of them hold **489 real traps**, the other 246 a single all-zero record (flag 0, chance
> 0, no actions — the compiler's empty entry, which never arms because `roll % 100 < 0` fails). No
> real trap names action 0; chances are 100 (487) or 60 (2); radii 0 (18), 2–8 (276) or 10 (195).
>
> **Arming.** The script verb **`settrapresource`** (`0x053B`, `00355400` → `003EC630`, [the verb table](../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv))
> releases the previous marker resource, stores and loads the new one (`002EBD60(id, 1)`) and
> tail-calls `002FA740` (`003EC679`) — its only caller. That walks the records, skips one whose flag
> is already set (`PersistentFlag_QueryBank512Low`), rolls the arm chance, sets bit *i* of the
> field's mask and places a world marker at the record's position (`002FB560(i, x, y)`,
> `002FA81E`–`002FA841`). The mask is kept in a **ring of three 12-byte `{fieldId, mask}` entries
> at `02EC3EA0`** (count `02EC3EC8`, write index `02EC3EC4`, rotated `% 3`, `002FA878`–`002FA8F7`),
> which is what the trigger walk looks up by field id. **`settrapshowstatus`** (`0x0547`,
> `00355E00` → `003EC6C0`) shows or hides the sixteen marker slots `003EB720` indexes.
>
> **Who can spring one, and who is hit.** The trigger walk refuses a unit whose stats flags carry
> bit 26 or whose **effect id 37 — *"Move safely past traps"*** (`listhelp_ability.bin` string
> 37, [the battle text banks](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md) §5.1) — is set in either layer (`+0x6C` / `+0x7C` bit 5, `002F80CA`–`002F80E8`),
> and a unit whose stats `+5` is 1, or 0 with the kind byte `+4` in 27–39 — the Esper genera
> (`002F80F3`–`002F8115`).
> `002FB8C0` then walks the four slot-map members (`0031B810`), skipping the same classes plus the
> out-of-play mask, and keeps each whose distance to the record's position (`003A1920`) is at most
> the radius `+0x0A`; a radius of 0 returns the triggering unit alone (`002FB8E0`–`002FB8EC`). The
> message is posted once for the trigger (`0046A9D0`) whatever the outcome.
>
> **What a trap does.** The chosen action id returns to `BattleUnit_RunPeriodicCombatMaintenance`
> (`00310FC9`–`003110BA`), which — if `BattleEncodedId_IsValidForClass(20, id)` — for each gathered
> unit attaches the row's `+0x24` effect (bit 15 stripped: 115–118, `002EACD0`) and runs
> `BattleFormula_ResolveTargetResult` / `BattleFormula_ApplyTargetResult` (`0031108C`, `003110AB`)
> on a zeroed result record. The sixteen rows a shipped trap can name are **246–261** ([the action definition row](../07-Combat-Action/Action-Definition-Row/the-action-definition-row.md)),
> unnamed in bank 0; their recipes are single-slot (`01EF96C0`, [the count-clock page](../08-Combat-Formula/Recipe-System/the-count-clock-and-bank-recipes.md)):
>
> | rows (uses in the 489 traps) | recipe → slot | what the slot does |
> |---|---|---|
> | 246 / 247 / 248 (113 / 157 / 213) | 94 → 106 (`0038CD60`) | **HP damage `(1 + roll % power) × (1 + roll % level)`** — two MT draws, `power` the row's `+0x10` (30 / 90 / 180), `level` the target's stats `+0x1C2`; into the HP-loss slot `02AEE004` |
> | 249 / 257 (67 / 37) | 95 → 107 (`0038CE40`) | the same product (power 20 / 100) into the **MP-loss** slot `02AEE00C` |
> | 260 (57) | 96 → 108 (`0038CF20`) | the same product (power 80) into the **HP-gain** slot `02AEE008` — *"… healing nearby allies"* |
> | 261 (27) | 97 → 109 (`0038D000`) | the same product (power 50) into the **MP-gain** slot `02AEE010` — *"… energizing nearby allies"* |
> | 259 (22) | 99 → 163 (`0038F6F0`) | **gil loss** `(1 + roll % 99) × (1 + roll % level)` into the result context's `[+0x10] + 8`, zeroed when `00309BF0` returns 0 (`0038F7D0`–`0038F7E9`) — *"Your pockets feel lighter"* |
> | 250 / 251 / 252 / 253 / 254 / 255 / 256 / 258 (25 / 35 / 58 / 44 / 39 / 28 / 35 / 21) | 98 → 181 (`BattleFormula_CalcApplyCandidateStatusesRequired`) | **inflict the row's `+0x18` status mask**: Sap; Confuse + Berserk; Petrify; Blind; Silence; Reverse + Disable; Disease; Oil ([the thirty-two statuses](../10-Status-Periodic-Terminal/the-thirty-two-statuses.md)) |
>
> The four damage / restore slots are one body with four output slots (`0038CD60` read whole; the
> other three differ only in the final store). So a Traveler-style trap deals up to `power × level`,
> and the "safe from traps" Float status is realised as effect id 37 in the merged layer.

### The cross-system chain

```
BattleUnit_TryTriggerNearbyAuthoredFieldAction
  -> WorldTransition_GetActiveOrPendingFieldId   (World: which area)
  -> proximity gate against a nearby authored record
  -> RNG_MT19937_NextU32_Thunk                   (RNG: 75/25)
  -> PersistentFlag_SetBank512Low                (Story: permanent save bit)
```

**Four owners in one function** - Combat Action, World/Area, RNG and Story - and the result is
save state. That is the tightest cross-subsystem coupling found so far, and it is a genuine
determinism concern: **a permanent, save-recorded flag is set from an MT19937 draw.**

For XIIOnline that is worse than the LCG cases. MT19937 needs 624 words to reproduce, and the
consequence here is not a transient outcome but a **bit written into the save**. Two clients that
disagree on this roll disagree permanently.

### Credit where due

This was **not** found by reading a category. The audit reported an unexplained subsystem edge on a
document, and following it exposed a function cited three times and never verified. That is the
second time the crossref audit has produced a finding rather than merely a chore - the first being
the accessor hubs in pass 3.

## 8d. Reopened 2026-09-02 - AF-4 answered: exactly two, and they are a pair

The determinism question from section 8c was whether **any other site writes a permanent save flag
from an RNG draw**. It is answerable exactly, by intersecting two caller sets:

```
functions that call any PersistentFlag_Set*  :  17
functions that draw from any RNG             :  91   (incl. the 7 inline-LCG consumers)
                                          both :   2
```

~~**Two, and only two**~~ **Two functions both draw and set a persistent flag**, but only `002F8060` sets it downstream of its draw; `002FAFD0` sets its flag (`002FAFFD`) before its first draw (`002FB01D`), so the chest's flag does not depend on the roll - its contents do *(corrected 2026-10-02, FABLE, on OPUS's byte verdict C-V10, [record](../_index/candidates/opus-story-readiness-fixes-1002/byte-verdicts.md))*. Otherwise they are strikingly alike: **both write `Bank512Low`, both draw
MT19937.**

| Function | Owner | Flag id from | Split |
|---|---|---|---|
| `002F8060` `BattleUnit_TryTriggerNearbyAuthoredFieldAction` | CombatAction | ~~`record[2]`~~ byte `+0x04` (`record[2]` counts shorts) *(corrected 2026-10-02, FABLE, on OPUS's byte verdict C-V9, [record](../_index/candidates/opus-story-readiness-fixes-1002/byte-verdicts.md))* | hardcoded **75 / 25** |
| `002FAFD0` *(unowned)* | - | ~~`record[9]`~~ byte `+0x09` | ~~authored threshold + **50 / 45 / 5**~~ authored gil chance (byte `+0x0B`), then **50 / 50** between two item ids, or **95 / 5** between two others with the armlet *(corrected 2026-10-02, FABLE, on OPUS's byte verdicts C-V8 and C-V9, [record](../_index/candidates/opus-story-readiness-fixes-1002/byte-verdicts.md))* |

### The second site, read

```c
areaId = WorldTransition_GetActiveOrPendingFieldId();

if (record[9] != 0xFF)
    PersistentFlag_SetBank512Low(record[9], 1);        // the flag is set FIRST

roll = RNG_MT19937_NextU32_Thunk();
if (record[0xB] <= roll % 100) {                        // authored per-record threshold
    roll = RNG_MT19937_NextU32_Thunk();                 // second draw
    if      (roll % 100 < 0x32) ...                     // 50   -> outcome A
    else if (roll % 100 < 0x5F) ...                     // 95   -> outcome B
    else                        ...                     //      -> outcome C
}
...
roll = RNG_MT19937_NextU32_Thunk();                     // third draw
```

*In the sketch above `record` is a byte pointer: `record[9]` and `record[0xB]` are the bytes `+0x09` (flag id) and `+0x0B` (gil chance). The second draw is not a three-way split: the armlet test picks one of two pairs - with it, `< 0x5F` takes the id at `+0x10` and the rest `+0x12` (95 / 5, `002FB0ED`); without it, `< 0x32` takes `+0x0C` and the rest `+0x0E` (50 / 50, `002FB0FE`). AF-6 below reads it whole.* *(corrected 2026-10-02, FABLE, on OPUS's byte verdicts C-V8 and C-V9, [record](../_index/candidates/opus-story-readiness-fixes-1002/byte-verdicts.md))*

Three things distinguish it from its sibling:

**A different record layout.** The flag id sits at ~~`record[9]`, not `record[2]`~~ byte `+0x09` (the chest indexes bytes), not byte `+0x04` (the trap's `record[2]`, which counts shorts), and the gate
threshold at ~~`record[0xB]`~~ byte `+0x0B` *(corrected 2026-10-02, FABLE, on OPUS's byte verdict C-V9, [record](../_index/candidates/opus-story-readiness-fixes-1002/byte-verdicts.md))*. So there are **two distinct authored field-action record formats**, not
one - which matters for anyone trying to parse them.

**The probability is authored, not hardcoded.** Where `002F8060` compares against a literal 75, this
one compares against `record[0xB]`. Per-record tuning.

~~**A three-way outcome, 50 / 45 / 5.** `< 0x32` (50) then `< 0x5F` (95) splits the remainder into a
45% band and a 5% tail.~~ **Two two-way pairs, not a three-way outcome:** the item pick is **50 / 50** (`< 0x32`) without the armlet and **95 / 5** (`< 0x5F`) with it, each between its own two ids *(corrected 2026-10-02, FABLE, on OPUS's byte verdict C-V8, [record](../_index/candidates/opus-story-readiness-fixes-1002/byte-verdicts.md))*. And it makes **at least three MT19937 draws** in one pass.

**In both functions the flag is set unconditionally of the roll** - `0xFF` meaning "no flag" is the
only escape. The bit records *that the record fired*, not *which outcome came up*.

> *AF-6 answered 2026-09-12 (FABLE): the second format is the treasure chest, and the "50 / 45 / 5"
> is two different pairs.* `002FAFD0` has one caller — the end thunk `0050FAF0` of the durative
> script verb **`btlAtelOpenTreasureMessage`** (`0x3037`, [the verb table](../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-table.tsv)) — which resolves the
> chest record from the script's packed reference (`0050FB25`) and calls it with an output triple.
> Read whole (`002FAFD0`–`002FB14A`):
>
> ```
> treasure record
>   +0x00  u8    the chest's index in the field's per-chest mask  (002FB00F -> 002FB430(table, fieldId, index, 0))
>   +0x08  u8    flags: bit 6 = the gil amount is random, 1 .. N  (002FB07C-002FB090)
>   +0x09  u8    persistent flag id, 0xFF = none                  (set FIRST, 002FAFEA-002FAFFD)
>   +0x0B  u8    gil chance, percent                              (roll % 100 < +0x0B -> gil)
>   +0x0C  u16   item id, normal pick, roll < 50                  (002FB103)
>   +0x0E  u16   item id, normal pick, roll >= 50                 (002FB109)
>   +0x10  u16   item id, armlet pick, roll < 95                  (002FB0F2)
>   +0x12  u16   item id, armlet pick, roll >= 95                 (002FB0F8)
>   +0x14  u16   gil amount (or N), normal                        (002FB06F)
>   +0x16  u16   gil amount (or N), armlet                        (002FB069)
> out: {kind: 1 = gil (+4 amount), 0 = item (+4 id, +6 = 1), 2 = nothing}
> ```
>
> **The "armlet" case** is the party leader (`BattleUnit_GetPartyLeader`, `003272A0`) being in play
> (`0x80000003` clear) and carrying **layer id 25 in either effect layer** (`+0x6B` / `+0x7B` bit 1,
> `002FB05D`–`002FB067`, [the two-layer model](../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md)) — the augment whose shipped help text is *"Search the
> deepest recesses of chests, coffers, and the like"* (`listhelp_ability.bin` row 25, [the battle text banks](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md)
> §5.1), granted by the accessory **Diamond Armlet** (`0x115E`; the three weapon rows that also carry
> byte 25 are outside the derived rebuild's category gate). So a chest is gil with probability
> `+0x0B` %, otherwise an item: **50 / 50 between two ids without the armlet, 95 / 5 between two
> other ids with it** — the "45 / 5" was the second pair's split read as a tail of the first — and
> a `0xFFFF` id yields nothing (`002FB135`). Three MT19937 draws at most: the gil test, the amount
> (when bit 6) or the item pick.

### What this settles

**The ~~RNG-to-permanent-save surface~~ set of functions that both draw and set a persistent flag is exactly two functions, one bank, one generator** (only one sets its flag after drawing, and in neither does the flag depend on the drawn value) *(corrected 2026-10-02, FABLE, on OPUS's byte verdict C-V10, [record](../_index/candidates/opus-story-readiness-fixes-1002/byte-verdicts.md))*. That is a
much better answer than "unknown", and a much smaller problem than it could have been: for XIIOnline,
reconciling those two call sites covers the entire path by which a random draw becomes irreversible
save state.

The bound is tight because it comes from a **set intersection over the whole call graph**, not from
sampling. Its one weakness is inherited: an inlined `PersistentFlag_Set*` would not appear as a call
edge, exactly as the inlined LCG did not (see the RNG document). The seven known inline-LCG consumers
were included on the RNG side, but no equivalent write-scan was run for the flag banks. **AF-5.**

## 8e. Reopened 2026-09-02 - AF-5 answered: no inlined flag writes, so the AF-4 bound is tight

Section 8d flagged its own weakness: the "exactly two" result came from **call edges**, and an
*inlined* `PersistentFlag_Set*` would not appear - the same gap that hid seven inlined LCG consumers
in the RNG document. Two independent checks close it.

### Check 1 - the payload-base callers

Any inlined flag write must first resolve the payload base. All **70 callers** of
`SaveImage_GetPersistentPayloadBase` were already decompiled (see the save document), so they can be
searched for the bank offsets directly:

| Bank | Functions referencing its offset |
|---|---|
| `Bank64A` `+0x1384` | ~~`QueryPrimaryOrAuthoredThresholdGate`,~~ `QueryBank64A`, `SetBank64A` - the gate has no `+0x1384` operand; it reads Primary `+0x14F4` (`0032A900`) *(corrected 2026-10-02, FABLE, on OPUS's byte verdict C-V5, [record](../_index/candidates/opus-story-readiness-fixes-1002/byte-verdicts.md))* |
| `Bank64B` `+0x138C` | `QueryBank64B`, `SetBank64B` |
| `Bank2048` `+0x13B4` | `QueryBank2048`, `SetBank2048` |
| `Bank512` `+0x14B4` | `QueryBank512Low`, `QueryBank512High`, `SetBank512Low`, `SetBank512High` |
| `Primary` `+0x14F4` | `QueryPrimaryOrAuthoredThresholdGate`, `SetPrimary` |

**Non-`PersistentFlag_*` functions touching a bank offset: zero.** All twelve accessors appear and
nothing else does.

### Check 2 - absolute addressing

`SaveImage_GetPersistentPayloadBase` is itself only 20 bytes, so it could be inlined too - in which
case a caller would address a bank as an **absolute global**:

```
active buffer  0x02164280
payload base   0x02164480          (= active + 0x200)
Bank64A  0x02165804    Bank64B 0x0216580C    Bank2048 0x02165834
Bank512  0x02165934    Primary 0x02165974
```

Scanning `.text` for any RIP-relative displacement landing inside those spans produced **9 raw
candidates** across three functions.

**All nine are false positives.** Each was checked against a linear disassembly sweep:

| Candidate | Instruction boundary? | Actually decodes as |
|---|---|---|
| `001DD581/582/583` | no | mid-instruction inside a `call rel32` |
| `0031D443/445` | no | mid-instruction |
| `0031D444` | yes | `test rax, rax` - **3 bytes, no displacement operand** |
| `0035D604/605` | no | mid-instruction inside `mov eax,[rip+0x1F6ADE2]` (target `0x022C83EC`, not a bank) |
| `0035D606` | yes | `shr eax, 5` - **3 bytes, no displacement operand** |

Seven are not instruction boundaries at all. The two that are decode to instructions with **no
memory operand**, so the "displacement" the scanner read was simply the following bytes.

### The noise estimate came first, and that mattered

Before disassembling, the expected false-positive count was computed: ~8 M code bytes x 3 trial
opcode lengths is ~24 M scan positions, and a uniformly random 32-bit displacement lands in a
256-byte window with probability `256 / 2^32`.

```
expected false hits, Bank2048 (256 B span)  =  24e6 * 256 / 2^32  =~ 1.4
expected false hits, a 64-byte span          =  24e6 *  64 / 2^32  =~ 0.36
observed: 2 in Bank2048, 1 in Primary
```

**The observation was already consistent with pure noise**, which is why each hit was verified rather
than reported. Three apparent findings, all dissolved.

### The conclusion

**No code writes a persistent flag bank except the twelve named accessors.** Therefore section 8d's
intersection is not merely a call-edge bound - it is **tight**:

> ~~**Exactly two functions in FFXII turn a random draw into permanent save state**, and both are
> known: `002F8060` and `002FAFD0`.~~ **Exactly two functions in FFXII both draw a random number and set a persistent flag** - `002F8060` and `002FAFD0` - **and in neither does the flag depend on the draw**: only
> `002F8060` sets its flag after drawing, and `002FAFD0` sets it before its first draw. The draw decides the trap's message and the chest's contents, not the flag *(corrected 2026-10-02, FABLE, on OPUS's byte verdict C-V10, [record](../_index/candidates/opus-story-readiness-fixes-1002/byte-verdicts.md))*.

### Why this one is recorded even though nothing was found

This database already carries three cases where a narrow instrument produced a confident false
answer that had to be retracted. This is the first where the noise floor was estimated **before**
believing the output - and it caught all three apparent hits before any of them reached a document.

The rule generalises: **a byte-pattern scan over millions of positions needs its false-positive rate
computed before its hits are interpreted.** Nine candidates looked like evidence; the arithmetic said
to expect about two by chance; verification found zero real ones.

## 10. Falsification pass 1 - 2026-09-02

**Program state:** parent `2ed8affb...`, snapshot `46f02e26...`, embedded EXE `73461d08...`, ledger
38,161 / 38,003 / 158, verified before any reading.
**Instruments:** a base-tracking displacement census over **every** caller of
`SaveImage_GetPersistentPayloadBase` (70) **and** of the raw buffer accessor beneath it (28), with
the tracked register dropped the instant anything but a copy writes it; the exact call-site census
over all 38,161 bodies; six bodies decompiled.

### Killer observations named, and hunted

| Claim | What would kill it | Result |
|---|---|---|
| the five bank offsets and sizes | any accessor using a different offset | **SURVIVED exactly**, all five, from a 70-caller census |
| §3's fifteen addresses and their sizes | one row disagreeing | **SURVIVED**, 15/15 |
| "every accessor resolves through the payload base" | a bank reached another way | **SURVIVED and strengthened** — verified across **both** routes |
| `0x400B` is threshold query 11 | the call site not existing | **SURVIVED**, and there are **three** such call sites, not one |
| flag 0 = always, flag 1 = never | either touching storage | **SURVIVED** |
| **AA-5: a 32-byte gap at `+0x1394`** | any access in that range | **SURVIVED** — nothing, by either route |
| §1: a story bit is "set once and remembered" | something clearing a bank | **SURVIVED a targeted attack** — see below |
| **bit 14 selects "the authored threshold schedule"** | the other mode not being a flag read at all | **the description was incomplete — §2 rewritten** |
| the payload map ends at Primary (`+0x1533`) | a live field past it | **OVERTURNED — `+0x1534` exists** |

### The attack that looked most likely to succeed, and failed

Two functions are named **`WorldPersistence_ResetBanksAndMarkInitializationState`** (`00268320`) and
**`WorldPersistence_ResetBanksForFieldTransition`** (`0026DB30`). If either cleared a flag bank, §1's
*"set once and remembered"* and the whole irreversibility claim would fall.

**Neither touches a bank.** Tracked through the payload base, `00268320` writes exactly one byte —
`+0x1061` — and `0026DB30` tests exactly one — `+0x1062`. Both are in the world-transition byte
cluster, nowhere near `+0x1384`-`+0x1533`. **"Banks" in those names is not these banks.** The
irreversibility claim survives, and it survives a test that was pointed straight at it by the
engine's own naming.

### What the threshold schedule actually is

The document said bit 14 chooses "the authored threshold schedule" and left it there. Reading
`00377970` shows **the other half of the gate leaves the save system entirely**: it walks a list of
authored `u16` thresholds, compares each against `FieldData_GetVariable0()`, and **toggles** the
answer at every threshold the variable has passed, with bit 15 marking the last entry.

So the answer is a **parity**, and an authored condition can be true *only between two story
points* — something a flag cannot express, because a flag never goes back. §2 now carries the body,
the variable accessor and the observed id vocabulary.

**`0xFFFF` turns out to be a sentinel used by nine call sites**, decoding to threshold index
`0x3FFF` — beyond any plausible entry count, since every index actually observed is `<= 0x67`.

### `+0x1534` — the map was one field short

Primary ends at `+0x1533`, and the document's map stopped there. **`+0x1534` has six access sites**
(`ActorManager_RunFieldRuntimePass` among them) and `+0x1535` is reached through the raw buffer
accessor. Registered as **AA-6**.

### What was tried and failed to break it

- **Censused both routes to the payload.** The base is `rawBuffer + 0x200`, so the accessor can be
  bypassed; the bypass has 28 callers and 36 displacements and **none is in the AA-5 gap**. An
  absence claim about a memory range is only as good as the enumeration of ways to reach it, and
  there were two.
- **Ran the census against the known offsets first.** All five documented banks came back before the
  instrument was pointed at anything unknown.
- **Checked the address table mechanically** rather than by eye: 15 rows, 15 body sizes, no
  disagreement.
- **Looked for the gate's callers rather than assuming its documented one.** There are **32**,
  including two five-byte thunks the §3 table does not list, and one of them is
  `InputGameplay_ArbitrateDigitalInputAndModalState` — story flags reach input arbitration.
- **Re-checked for banned evidence.** No `.pdata`/`.xdata`/unwind/EH reasoning; the offsets come
  from tracked register arithmetic, not from address adjacency.

### Limits of the two censuses, stated

Neither would see a payload pointer stored to memory and read back later, nor a bulk `memcpy` over
the whole payload. The AA-5 and AA-6 findings are bounded by that, exactly as the two-hop limit
recorded in audit pass 129.

### Status

**Nothing overturned in the bank mechanics** — offsets, sizes, bit arithmetic, range guards, the
reserved ids and the address table all survived exactly. **One description was substantially
incomplete** (the threshold schedule), **one map was a field short** (`+0x1534`), and the
irreversibility claim survived the attack the function names invited. **This document has now had
its first falsification pass.**

## 8f. Reopened 2026-09-08 - `00379160` read: what a new game switches on before you press a button

**The category's last unread owned function.** With this section every one of the **15 functions the
ledger assigns to `Story_Event_Quest_Hunt`** has been read individually - see §3, where three rows
that still said `partial` are corrected.

### What the player sees

A new game does not begin with a blank slate. ~~**Room for fifty-three authored ids is switched on in
the Primary bank before the first frame of play**~~ **Fifty-two authored ids are switched on in the Primary bank before the first frame of play** - the shipped list holds fifty-three, but the first is id 0, which `SetPrimary` rejects (it accepts 2 to 0x1FF) *(corrected 2026-10-02, FABLE, on OPUS's byte verdict C-V2, [record](../_index/candidates/opus-story-readiness-fixes-1002/byte-verdicts.md))*, and they come out of a shipped file whose name
says what they are: `mapjumpgroupinit.bin`. Everything else in the persistent payload - every bank
in §4 - is zero at that moment, wiped in a single `memset`.

### The reset chain

```
FUN_00266D10  (1,185 B, no owner)          a run of ~20 subsystem resets
  -> 002EF2D0

SaveRuntime_ResetActiveImageAndRebindState  (002EF650, 50 B, Save_Load_Settings)
  -> memset(0x02164280, 0, 0x56690)         the whole save image, 353,936 bytes
  -> 0016D6A0(0) ; 00253A80()
  -> 002EF2D0
  -> tail-jump 00238A80
```

and `002EF2D0` (38 B, `Save_Load_Settings`, unnamed in the ledger as `FUN_002ef2d0`) is:

```asm
002EF2D0  sub  rsp, 0x28
002EF2D4  call 0x2EF640              ; SaveImage_GetActiveBuffer -> lea rax, 0x02164280
002EF2D9  xor  edx, edx              ; fill byte = 0
002EF2DB  mov  r8d, 0x1538           ; length
002EF2E1  lea  rcx, [rax + 0x200]    ; = SaveImage_GetPersistentPayloadBase()
002EF2E8  call 0x861EC0              ; VCRUNTIME140.dll!memset, via IAT slot 008C2A60
002EF2ED  add  rsp, 0x28
002EF2F1  jmp  0x379160              ; TAIL-JUMP into the flag applier
```

`002EF640` is the same buffer accessor `002EF2B0` goes through - `002EF2B0` is literally
`GetActiveBuffer() + 0x200`, which is where §4's *"base = activeBuffer + 0x200"* comes from.

> **The persistent payload is exactly `0x1538` = 5,432 bytes**, and one `memset` clears all of it.

> ### This bounds AA-8 (renumbered - see §7)
>
> §4b's map ended at `+0x1535` with a field it could not place. The payload's authored length is
> `0x1538`, so **`+0x1534` .. `+0x1537` are the last four bytes of the payload and nothing follows
> them.** The unexplained field is a tail, not an opening into further structure. Its *meaning* is
> still unknown; its *extent* is now closed.

### The function, in full

```asm
00379160  push  rbx
00379162  sub   rsp, 0x20
00379166  mov   rbx, [rip + 0x2763F63]     ; = 02ADD0D0
0037916D  test  rbx, rbx
00379170  je    0x3791B0                   ; no list -> do nothing
00379172  mov   [rsp + 0x38], rdi
00379177  movzx edi, word [rbx + 8]        ; entry count, u16
0037917B  add   rbx, 0xA                   ; entries start at +0x0A
0037917F  test  di, di
00379182  je    0x3791AB                   ; count 0 -> do nothing
00379184  mov   [rsp + 0x30], rsi
00379189  mov   esi, 0xFFFF                ; the loop decrement, as a 16-bit -1
0037918E  nop
00379190  movzx ecx, word [rbx]            ; id
00379193  mov   edx, 1                     ; value = 1
00379198  call  0x32AB60                   ; PersistentFlag_SetPrimary(id, 1)
0037919D  lea   rbx, [rbx + 2]
003791A1  add   di, si                     ; di -= 1, 16-bit
003791A4  jne   0x379190
```

```c
void PersistentFlag_ApplyAuthoredInitialPrimarySet(void)      /* 00379160 */
{
    const u8 *t = g_initialFlagList;                          /* 02ADD0D0 */
    if (t == NULL) return;
    u16 n = *(u16 *)(t + 8);                                  /* entry count */
    const u16 *p = (const u16 *)(t + 0x0A);
    if (n == 0) return;
    do {
        PersistentFlag_SetPrimary(*p++, 1);                   /* 0032AB60 */
    } while (--n);
}
```

**It only ever sets.** `edx` is the literal `1` on every iteration, so the `and`-with-`~bit` arm of
`PersistentFlag_SetPrimary` (at `0032ABC8`) is never reached from here. **It does not check whether
a flag is already set** - it does not need to, because the payload was zeroed four instructions
earlier.

**Ids 0 and 1 in the list would be silently dropped.** `PersistentFlag_SetPrimary` guards with
`lea eax, [rcx - 2] ; cmp eax, 0x1FD ; ja return`, so it accepts `2 <= id <= 0x1FF` and rejects
everything else - including the two hardwired ids §2 documents as *always* and *never*. The applier
does no bound check of its own; **the setter's guard is the only one in the path.**

**The counter is 16-bit and the loop is a `do`/`while`.** `add di, si` with `si = 0xFFFF` is a
16-bit decrement, and `n == 0` is rejected before entry, so the loop runs exactly `n` times and
cannot wrap.

### Reachability: `E8` says `00379160` uncalled, and `E8` is wrong

| instrument | result for `00379160` | control | control result |
|---|---|---|---|
| `E8 call` | **0** | `001DE4F0` | 1 - positive |
| `E9 jmp` | **1** - at `002EF2F1` | `001D1660` | 1 - positive |
| code memory-operand | 0 | `02ADD0A8` | 3 - positive |

> **A `call`-only reachability query reports this function uncalled, and it is on the new-game
> path.** `E8-only-reachability` is tied for the most frequent recorded cause of a wrong answer in
> [the contradiction ledger](../_index/CONTRADICTION-LEDGER.md); this is another instance, caught by
> the four-instrument rule rather than by luck. **The tail-jump is the whole of its reachability.**

### Where the list comes from, and the shipped file that fills it

Every reference to `02ADD0D0` in the image - three of them, with `02ADD0A8` as a positive control at
three:

| site | in | what |
|---|---|---|
| `00377D1C` | `WorldAreaField_BootMapTables` (`00377CC0`) | **clears** it, in a run of `mov [g], rbx` |
| `00378B92` | `00378B90` | **publishes** into it |
| `00379166` | `00379160` | **reads** it |

`00378B90` has **zero `E8` callers and zero `E9` jumps**. It is *address-taken*, by
`lea rax, [rip + 0x3CC]` at `003787BD` inside `WorldAreaField_RequestAuthoredMapTables`
(`00378540`) - the routine
[the field-record document](../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md)
already describes as asking the resource system for an authored table and installing a ten-byte
publisher for each. **That document lists three such registrations. There are at least five**, and
the two it does not list are these:

```asm
003787B5  mov   edx, 0x28                  ; resource index
003787BD  lea   rax, [00378B90]            ; the publisher
003787C8  mov   [rbp - 0x20], rax          ; into an 0x18-byte descriptor at [rbp-0x30]
003787D6  lea   ecx, [rdx - 0x1F]          ; = 9, the resource kind
   ...    call  0x32E620                   ; Resource_SubmitRequest

0037881A  mov   edx, 0x29
0037881D  lea   rax, [00378A50]
0037882C  mov   [rbp - 0x20], rax
00378836  lea   ecx, [rdx - 0x20]          ; = 9 again
00378841  call  0x32E620
```

Both compute the kind as `9` from the index by different displacements - `0x28 - 0x1F` and
`0x29 - 0x20` - which is a compiler reusing one register, not two different kinds.

| request | publisher | global | consumer |
|---|---|---|---|
| `(kind 9, index 0x28 = 40)` | `00378B90` | `02ADD0D0` | `PersistentFlag_ApplyAuthoredInitialPrimarySet` |
| `(kind 9, index 0x29 = 41)` | `00378A50` | `02ADD0A8` | `EventMemory_QueryDefinitionIdAbsent` |

**The file names come out of the executable's own path array** - the same array, and the same
method, the field-record document used. Its `navimapdata.bin` at kind 9 index 8 is the control:

```
array base (IN build) = 0x01E12660     dense, 8-byte stride, one path pointer per index

  idx  8   0x01E126A0 -> PS2Data\image\ff12\in\bin\navimapdata.bin           <- CONTROL, matches
  idx 39   0x01E12798 -> PS2Data\image\ff12\in\common\gramap_weatherinfo.bin <- CONTROL, matches
  idx 40   0x01E127A0 -> PS2Data\image\ff12\in\bin\mapjumpgroupinit.bin
  idx 41   0x01E127A8 -> PS2Data\image\ff12\common\eventmemorylist.bin
```

Both controls land where the field-record document says they should, including its *"31 slots
apart"* - `0x01E12798 - 0x01E126A0 = 0xF8 = 31 * 8`.

The image ships **one such array per language**; the `CH` array at base `0x01E0E3B0` gives the same
two files at the same two indices, with `ch` substituted in the localised path and
`eventmemorylist.bin` - which lives under `common` - **not merely equal but the same pointer value**,
`0x00967E40`.

> **`02ADD0A8` is `eventmemorylist.bin`.** That answers the question
> [`event-memory-at-actor-bind.md`](event-memory-at-actor-bind.md) filed against itself - *"what
> populates the `02ADD0A8` list with ids"*. **AA-6 closed.**

### How many entries, from the shipped size tables

`Resource_GetFileSizeByKindAndIndex` (`0032E400`) reads `g_sizeTables[kind][index]` from an array of
per-kind table pointers at `0x022C51F0`, guards `index < 0x400`, and rounds its answer **up to 64
bytes** before returning it. The tables are the shipped `FileSizeTables\FileSizeTable_*.fst`.

Those files are **820,000 bytes = 41 kinds x 5,000 `u32`, with no header** - kind `k`'s table starts
at byte `k * 20000`. That layout was **derived from a control, not assumed**: the field-record
document states `navimapdata.bin` is exactly 3,470 bytes, and searching an `.fst` for the value
3,470 returns **exactly one offset, 180,032**, where `180032 = 9 * 20000 + 8 * 4` - kind 9, index 8,
to the byte.

| kind 9 index | file | stored size |
|---:|---|---:|
| 8 | `navimapdata.bin` | 3,470 (control) |
| 39 | `gramap_weatherinfo.bin` | 2,628 |
| **40** | **`mapjumpgroupinit.bin`** | **116** |
| **41** | **`eventmemorylist.bin`** | **26** |

**All twelve shipped language tables agree exactly** on all four values.

Both files fit the header shape the two consumers read - eight bytes, a `u16` count at `+8`, then
`u16` entries from `+0x0A`:

```
mapjumpgroupinit.bin   116 bytes  ->  (116 - 10) / 2 = 53 entries
eventmemorylist.bin     26 bytes  ->  ( 26 - 10) / 2 =  8 entries
```

> **Both divide exactly**, which tests the record shape as much as the arithmetic: a wrong header
> size or a wrong element width would leave a remainder in at least one of them, and neither leaves
> one. **These are capacities, not counts** - the `u16` at `+8` is what the loop trusts, and a file
> may carry fewer entries than it has room for. The files live inside the 31 GB `SRYK` archive and
> were not extracted, so **the ids themselves are unknown. `DS-1`.**
>
> **The route exists.** The field-record document's frontmatter carries
> `navimapdata_bin_md5` and a `vbf_path`, so a file has already been pulled out of that archive
> in this database and hashed. `DS-1` is a *retrieval*, not a research problem.

### The publishers store a 32-bit value into a 64-bit pointer

All three ten-byte publishers in this family are byte-identical but for the global:

```asm
00378A50  8B C1              mov  eax, ecx        ; <- 32-bit; zero-extends into rax
00378A52  48 89 05 ...       mov  [02ADD0A8], rax
00378A59  C3                 ret
```

`mov eax, ecx` is `8B C1`, and the two bytes before both `00378A50` and `00378B90` are `CC CC`
padding, so this is the real entry and not a misaligned decode. **The high 32 bits of these globals
are therefore always zero**, while `00379160` and `00377440` dereference them as full 64-bit
pointers.

> **This is not a new finding and is deliberately not filed as one.**
> [The field-record document](../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md)
> §2a already records the same truncation for its three publishers, names the engine's
> `ImageAddress_ResolveRuntimePointer` convention as the likely reason, and holds it open as
> **`PROPOSED-repos2d-4`**. What §8f adds is only that **the family is five publishers, not
> three**, and that two of the five feed this category.

### What this section does not claim

- **What the 53 ids are.** The file is named `mapjumpgroupinit.bin`, and a sibling
  `mapjumpgroupflagrom.bin` sits at kind 9 index 10 in the same array. *"Initial state of the map
  jump groups"* is what the **name** says; **no id has been read**, and nothing here proves the
  flags govern zone transitions rather than merely being named after them. `DS-1`.
- **That `FUN_00266D10` is "new game".** It is 1,185 bytes of consecutive subsystem resets and it
  calls this chain; it was **not read in full**, and no menu path was traced to it.
- **What `0016D6A0`, `00253A80` and `00238A80` do.** Named as the chain around
  `SaveRuntime_ResetActiveImageAndRebindState`, unread.
- **That `00378540` registers exactly five tables.** Five are now accounted for; the routine is 943
  bytes and was read only at the two sites the operand scan pointed to.
- **What the eight bytes before the count are.** Both list files carry a `+0x00` .. `+0x07` header
  that neither consumer touches.


## 9. Related

- [`../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md`](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md) — the payload these offsets index, and the `SAFH` container
- [`../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md`](../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md) — the area id at payload `+0x1044`
- [`../01-Script-VM-Native-Bridge/scriptvm-native-dispatch-table.md`](../01-Script-VM-Native-Bridge/scriptvm-native-dispatch-table.md) — the VM that asks these questions

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. MECHANICAL-only crossings are recorded in the registry, not here.*

- **Movement — CLIENT.** The small unit accessors this page cites are read throughout locomotion:
  - **`BattleUnit_GetPartyLeader` (`003272A0`)** is read by `PartyFollow_SolveFormation`,
    `PartyFollow_LookupDestination`, `BattleLocomotion_DecodeOrderGoal`, `BattleLocomotion_BuildSolverContext`, the
    battle message poster client in the `00469xxx` range and four unnamed locomotion bodies.
  - **`BattleUnit_FindMappedDefinitionSelectorByIndex` (`0031B810`)** is read by `PartyFollow_SolveFormation` and two
    locomotion bodies.
  - **The 3-D distance `003A1920`** is read by `Movement_UpdateSteeringTowardTarget`,
    `Navigation_TestSegmentAgainstAuxObstaclesXZ` and four more bodies.
  - The 477-byte trigger sibling `002FA740` calls a 342-byte body. That body reaches six movement helpers of 5–393
    bytes.
  - `002EACD0` is called by the 68-byte stance-bit setter `00313500`.
- **Spawn_Encounter_Lifecycle — CLIENT.**
  - `Spawn_TrySelectCandidatePosition` and `SpawnLifecycle_CheckAndRetireByNativeRange` read `BattleUnit_GetPartyLeader`.
  - The retire check and `Spawn_ValidateCandidateDistanceToPlayers` read `0031B810`.
- **Items_Equipment_Shops_License — SERVICE and CLIENT.**
  - The save rebind `SaveRuntime_RebindImageBackedGameplayState` (`00238A80`) rebases inventory class descriptors.
  - `0050FAF0` grants loot through `Inventory_GrantEncodedLootItem`.
  - `Inventory_QueryOwnedCountIncludingReservedActionItems` reads `0031B810`.
- **Presentation — CLIENT.**
  - `FieldData_GetVariable0` (`00265270`) is read by the debug menu renderer.
  - `002EACD0` forwards to a 958-byte Presentation body.
  - `0031B810` is read by `PartyCombat_UpdateStanceState` and `BattleUnit_BroadcastPartyCombatTargetRel…`.
  - `0032E400` is read by two Presentation bodies of 119 and 337 bytes.
  - `003EC6C0` and `003EC700` index the sixteen marker slots through a 38-byte helper.
  - The console body `001D1660` calls three Presentation console bodies.
- **PlatformOnlineAchievements — CLIENT.** Two achievement-side bodies (308 B and 367 B) read `FieldData_GetVariable0`.
- **Audio — CLIENT.** The console's two audio legs, and the 335-byte Audio-filed body that reads the persistent payload
  base (`002EF2B0`).
- **ActorEntity - SERVICE (34 edges).** `002628B0` reaches bodies filed to ActorEntity: `0025B070`, `00263660`, `002695A0` - shared machinery across the layer boundary, no shared ownership.
- **CoreRuntimeScheduling - CLIENT and SERVICE (6 edges).** `00265270`, `00266D10`, `002EF650` are also called by bodies filed to core runtime: `001EC760`, `0022A0B0`, `0022B6E0`; `002628B0` reaches bodies filed to core runtime: `00229EE0` - shared machinery across the layer boundary, no shared ownership.
- **Input - CLIENT and SERVICE (8 edges).** `00265270` is also called by bodies filed to input: `00253C70`; `002628B0`, `00266D10`, `002DDA30` reach bodies filed to input: `0035B5D0`, `00226BE0` (ActorControlMaskPropagationRuntime), `001E0FF0` - shared machinery across the layer boundary, no shared ownership.
- **Party - CLIENT and SERVICE (8 edges).** `002EACD0` is also called by bodies filed to party: `00312EE0`; `002628B0`, `0026DB30` reach bodies filed to party: `00358B40`, `00359200`, `003590E0` - shared machinery across the layer boundary, no shared ownership.
- **RNG_Random_Selection - SERVICE (8 edges).** `002F8060`, `002FA740`, `002FAFD0` reach bodies filed to random selection: `00379CD0` - shared machinery across the layer boundary, no shared ownership.
- **Resource - CLIENT and SERVICE (26 edges).** `00265270` is also called by bodies filed to resource: `001DA220`, `001DA970`; `001D1660`, `002628B0` reach bodies filed to resource: `002EEEE0`, `0032E520` - shared machinery across the layer boundary, no shared ownership.
- **Rewards_Progression_Economy - CLIENT (5 edges).** `002EACD0`, `0031B810`, `00379CD0` are also called by bodies filed to rewards/progression: `0030C650`, `002F8BB0`, `002F9A60` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT and SERVICE (83 edges).** `002641B0`, `0026A720`, `002E16B0` are also called by bodies filed to script VM / native bridge: `0050CB80`, `00345E70`, `0033F950`; `00266D10` reaches bodies filed to script VM / native bridge: `003DC2D0` - shared machinery across the layer boundary, no shared ownership.
- **Status_Periodic_Terminal - CLIENT (4 edges).** `002EACD0`, `002F8060`, `00379CD0` are also called by bodies filed to status/periodic terminal: `00301140`, `00310DB0`, `00386C70` - shared machinery across the layer boundary, no shared ownership.
- **World - CLIENT (6 edges).** `0026DB30`, `002EF2D0`, `0032E400` are also called by bodies filed to World: `00266D10` (NativeSupport), `00378540` (Area) - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT and SERVICE (65 edges).** `00265270` is also called by bodies filed to WorldAreaField (world area): `001EDCD0` (AuthoredPresentationCondition); `002628B0` reaches bodies filed to WorldAreaField (world area): `00378230`, `003DFA50`, `003EAA00` - shared machinery across the layer boundary, no shared ownership.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CombatFormula — CLIENT, fan-in of 55 edges.** Three cited flag-bank functions are called by formula bodies, including `BattleFormula_PrepareMagickPowerAttackVsDefense` and bodies of 120 to 298 bytes.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAI — CLIENT.** `AiOrder_EvaluateTargetSelector`, owned by that layer, calls `0031B810` on this page. That caller is the selector evaluation, 6,963 bytes of it: it indexes its table at a **six-byte stride** and takes a word at `+6`, two bytes at `+8` and `+9` and a signed word at `+0xA` before deciding anything; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Gameplay — CLIENT.** `FUN_00312b40`, owned by that layer, calls `003272A0` on this page. That caller is a 582-byte routine that writes the constant **2** into its fourth argument before reading `word[+0]` and the signed `word[+2]` of its second; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

## SWE2-EC7-92 update (2026-09-20) - `00377B60` word-table string lookup measured

`00377B60` (45 B) is the flag-bank name lookup the `0029C530`/
`002B9C70`/`002BA530` callers share: index `ecx` bounds against the
table's `+4` dword count, the `+0x10` word array gives the name's
offset into the table itself, and a zero word or out-of-range index
returns the `02EB1F0` fallback string.
Interior anchor `00377B74` (the `+0x10` word load).

## SWE2-EC7-110 update (2026-09-20) - `001DD8E0` measured

`001DD8E0` (395 B) is the
sorted 0x1C-record find-or-append
`001DD420` and `001DDBA0` run.
`qword[+0x28]` gates the whole
body; when `dword[+0x34] !=
dword[+0x20]` the `[+0x40]`
array is freed through
`00210EB0` and rebuilt as
`(dword[+0x20] + 1) * 0x1C`
bytes through `00210EC0`.
`00861EBA` shifts the tail
before the new slot's four
dwords zero. The key is the
word pair `word[01F82D20 +
0x2E]` / `+0x2C` (sign-extended):
the scan at `001DD9A0` matches
`{dword, dword}` per record and
on hit stores the index to
`[+0x38]` and exits; on miss
the key appends at slot
`dword[+0x34]`, `+0x38` latches
that index, and the bubble pass
at `001DD9E0` swaps 0x1C
records (movups 16 B + dword +
`+0x18` dword) into ascending
key order, and `+0x38` records
the index the new record
settles at.
Interior anchor `001DD9A0`
(the key-compare loop head).

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../_index/candidates/fable-persistent-flag-banks-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `003EC6C0` | 59 B | calls `003EC6C0 + 0x8` and returns without further work when it returns non-zero; otherwise, for index 0 to 15, calls `003EB720(index)` and then `003EC6C0 + 0x24` with that result and the incoming `ecx` | `003EC6C8`, `003EC6CF`, `003EC6DA`, `003EC6E4`, `003EC6EB` |

## Homed bodies re-homed here for host fit (FABLE, 2026-10-03; AUDIT-SPEC batch 4)

*Each body below was homed on another page by FABLE's homing stream (cloud-drafted, FABLE-verified). SWE2-AUDIT-SPEC reviewed its sentence, site and anchors exact, and rejected only the host: that page cites the caller as a foreign or boundary mention (commit `95d495604`). The row is moved here because this page cites the caller in its own text. The sentence is unchanged. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Verified by [`move_rows.py`](../_index/candidates/fable-home-host-moves-b4-1003/move_rows.py): every site transfers to its function, this page cites the caller outside this section, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors | moved from |
|---|---|---|---|---|---|
| `00231F20` | 43 B | `002FB560` + 0xA5 | sign-extends the word `r8w`, shifts it left by 5 (a 32-byte stride) and indexes the array at qword `rcx+0x10`; copies the four dwords at offsets `+0x0`, `+0x4`, `+0x8` and `+0xC` of that 32-byte element to `rdx+0x0` through `rdx+0xC` | Interior anchor `00231F24`; Interior anchor `00231F28`; Interior anchor `00231F2C`; Interior anchor `00231F47` | [world-loot-pickups-the-ten-slot-pool-and-the-despawn](../13-Rewards-Progression-Economy/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md) |
| `0033CBF0` | 129 B | `002FB560` + 0xFB | under a stack cookie (`01F44830`), calls `0033CBF0` + 0x2F with `rcx` = a local at `rsp+0x20`; passes the incoming float `xmm2` as `xmm0` to the call at + 0x37; calls + 0x49 with that local as both `rcx` and `rdx` and the float result of + 0x37 in `xmm2`; then calls + 0x59 with the incoming `rcx`, the local and the incoming `rdx` | Interior anchor `0033CC1F`; Interior anchor `0033CC27`; Interior anchor `0033CC39`; Interior anchor `0033CC49` | [world-loot-pickups-the-ten-slot-pool-and-the-despawn](../13-Rewards-Progression-Economy/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md) |
| `003EC5B0` | 56 B | `002FB560` + 0x33 | calls `003EC5B0` + 0x8 with the incoming `ecx` and returns its value when non-zero; otherwise returns 0 when dword `02B5EC94` is zero or `ecx` is above 15 (unsigned), and else calls + 0x2D with (`ecx`, dword `02B5EC94`, 0, 1) and a fifth (stack) argument of 0, returning that call's `eax` | Interior anchor `003EC5B8`; Interior anchor `003EC5C1`; Interior anchor `003EC5CB`; Interior anchor `003EC5D4`; Interior anchor `003EC5DD` | [world-loot-pickups-the-ten-slot-pool-and-the-despawn](../13-Rewards-Progression-Economy/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md) |
| `003EC720` | 73 B | `002FB560` + 0x79 | keeps the incoming floats `xmm1`, `xmm2` and `xmm3` across a call to `003EC720` + 0x1E made with the incoming arguments, then tail-jumps (+ 0x44) with `rcx` = the sign-extended dword that call returned and the saved `xmm1`, `xmm2` and `xmm3` restored | Interior anchor `003EC73E`; Interior anchor `003EC743`; Interior anchor `003EC74C`; Interior anchor `003EC764` | [world-loot-pickups-the-ten-slot-pool-and-the-despawn](../13-Rewards-Progression-Economy/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md) |
| `003EC770` | 73 B | `002FB560` + 0x12A | keeps the incoming floats `xmm1`, `xmm2` and `xmm3` across a call to `003EC770` + 0x1E made with the incoming arguments, then tail-jumps (+ 0x44) with `rcx` = the sign-extended dword that call returned and the saved `xmm1`, `xmm2` and `xmm3` restored | Interior anchor `003EC78E`; Interior anchor `003EC793`; Interior anchor `003EC79C`; Interior anchor `003EC7B4` | [world-loot-pickups-the-ten-slot-pool-and-the-despawn](../13-Rewards-Progression-Economy/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md) |
