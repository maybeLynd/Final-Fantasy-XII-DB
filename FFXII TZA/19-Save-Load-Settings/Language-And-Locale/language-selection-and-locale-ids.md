---
system: Language selection and locale ids
category: 19-Save-Load-Settings
status: AUDITED
owner_layer: none - the accessors are unowned; consumers span Input, Presentation, Resource
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: capstone read of 0017E270 in full; string-pointer table at 0x01DF0030 dumped
    from the image; reference census for the global at 0x01F82D20
last_reviewed: 2026-09-02
audit:
  passes: 6
  last_pass: 2026-09-02
  last_pass_state: survived-and-confirmed-the-confirm-cancel-swap
  crossref_clean: false        # 2026-09-30 (SWE2-DATA): false until the pass-22 UNACCOUNTED NEIGHBOUR findings are accounted (FRONTIER-REQ-SWE2-DATA-PASS22-DEBT; OPUS-REQ-DATA-PASS30-CROSSREF-CLEAN-0930)
  reopened_count: 0
---

# Language selection and locale ids

> **FFXII: The Zodiac Age carries nine languages in one executable.** A two-letter code table at
> `0x01DF0030` names them, a global setting picks one, and a 407-byte function maps the code to an
> internal id. **The ids are not the table positions** — the mapping has deliberate gaps.

**For a player.** Choosing a language changes far more than menu text: it selects which text the
game loads and, on the evidence of a neighbouring field, may decide the confirm/cancel button
convention (section 4). The nine options are Japanese, English, French, German, Italian, Spanish,
Korean and two Chinese variants — plus a tenth `none` entry that no code path matches.

---

## 1. The code table

```
0x01DF0030   array of char* , 10 entries
   [0] "jp"   [1] "en"   [2] "fr"   [3] "de"   [4] "it"
   [5] "es"   [6] "kr"   [7] "ch"   [8] "cn"   [9] "none"
```

The strings themselves are packed at `0x008C5904` on a 4-byte pitch, `none` last.

## 2. The setting

```c
int languageIndex = *(int *)(*(void **)0x01F82D20);      /* field +0x00 of the singleton */
const char *code   = ((const char **)0x01DF0030)[languageIndex];
```

`0x01F82D20` is a global pointer to a shared runtime object — around 150 instructions across
`Input`, `Presentation`, `PlatformOnlineAchievements`, `CoreRuntimeScheduling`, `Resource` and
unowned code reference it, and its pointer is stored exactly once, at `00798261`. **Its field `+0x00`
is the language index.** What else the object holds is section 4.

## 3. Code to id — `0017E270`, read in full

The function compares the selected code against each entry, three bytes at a time (two letters and
the terminator), and returns an internal id:

| code | table index | **returned id** |
|---|---:|---:|
| `jp` | 0 | **10** |
| `en` | 1 | **1** |
| `fr` | 2 | **2** |
| `de` | 3 | **3** |
| `it` | 4 | **4** |
| `es` | 5 | **5** |
| `kr` | 6 | **7** |
| `ch` | 7 | **8** |
| `cn` | 8 | **11** |
| anything else (including `none`) | — | **10** |

**The id space is not the table order.** Positions `0`, `6` and `9` are never produced, `jp` maps to
`10` rather than `0`, and the two Chinese variants land at `8` and `11` either side of the unused
`9`. A mapping that skips values is the signature of an id space that **outlived an earlier
arrangement** — but nothing here says what occupied `0`, `6` or `9`, and this document does not
guess. **AV-1.**

The last two arms are written as branchless arithmetic rather than a `mov`:

```asm
0017E3F0  xor eax, eax / neg eax / sbb eax, eax / add eax, 0xB    ; cn  -> 11
0017E3FA  sbb eax, eax / or eax, 1 / neg eax / sbb eax, eax / add eax, 0xB   ; default -> 10
```

Both were evaluated by hand from the flag state rather than read off a constant: the `cn` arm enters
with `CF = 0` and yields `11`; the default arm's `neg` on a non-zero value forces `CF = 1`, so the
following `sbb` yields `-1` and the result is `10`. **`none` therefore behaves exactly like `jp`.**

## 4. The neighbouring field, and why it matters

The same singleton carries at least two more fields with one-line accessors:

| accessor | reads | note |
|---|---|---|
| `0017E210` | `+0x64` | **decides the binding pair swap** — see [the input stack](../../15-Input/Input-Stack/input-stack-device-channel-and-bindings.md) section 12 |
| `0017E260` | `+0x58` | 9 callers, unidentified |
| `0017E270` | `+0x00` | the language index, above |

`InputBinding_ShouldKeepAuthoredPairOrderForPlatformState` swaps two adjacent binding dwords when
`+0x64` is non-zero. **That this object is the locale carrier raises the prior on `+0x64` being a
regional convention, and therefore on the swapped pair being confirm/cancel** — the difference
between circle-confirms and cross-confirms.

**It is still a lead, and the standard is explicit about why:** the shape of one sibling field is not
evidence about another. What is established is that the language index and the binding-swap flag live
on the *same* object. ~~**AU-5** (what writes `+0x64`) remains open, and until it is answered nothing
here says whether a player can change the swap.~~ *Superseded 2026-09-26 (FABLE, Claude Opus 5.5): **AU-5** is answered. `+0x64` is `DecideButton` in `GameSetting.ini`, so the player can change the swap.*

## 5. What is not known

- What occupied ids `0`, `6` and `9`. **AV-1.**
- What the object at `0x01F82D20` is as a whole — three fields are identified out of an unknown
  total. **AU-6.**
- What `+0x58` holds. **AV-2.**
- Where the language index is written from — the settings file, a launcher, or a platform query.
  The same argument-passing blind spot that hides the `+0x64` writer applies. **AV-3.**
- Whether the id feeds text asset selection, font selection, or both. No consumer of `0017E270`'s
  return value is read here. **AV-4.**

## Open questions

- [x] ~~What occupied language ids `0`, `6` and `9`.~~ **AV-1 closed 2026-09-12 (FABLE): what
      occupied them is not in the image, but how the code still treats them is.** The cached id
      (`01E02814`, getter `00229E40`, 37 call sites) is compared image-wide against 1, 2, 6, 7, 8,
      9, 10, 11 and 12 and against the set `0xD81` — so two of the three holes are consulted by
      shipped code even though `0017E270` never produces them. **Id 0** is handled as a CJK
      language: it is in `00229E50`'s set `{0, 7, 10, 11}` (with `kr`, `jp`, `cn`; `00229E56`–
      `00229E63`) and in `002DDE60`'s "`jp` / `cn` / `ch` / `kr` / `0` → layout flag `0x400`" chain
      (`002DDF24`–`002DDF55`) — consistent with `0` having been Japanese before `jp` moved to 10.
      **Id 6** is handled as a Latin-alphabet language: `1 ≤ id ≤ 6` selects the Latin glyph block
      in `00434CD0` / `00435050` (`00434E3C`–`00434E4E`), and `002DDE60` sets bit 12 for `en` **or
      6** (`002DDEF4`–`002DDF1E`) — the slot after `es` that no shipped language fills. **Id 9** has
      no dedicated arm anywhere: in the one ten-way per-language table that lists it, `00473E80`
      (`00473EC0`–`00473F65`), ids 6–9 share the default arm with `kr` and `ch` — the languages
      without a two-letter folder suffix (`us`, `fr`, `de`, `it`, `es` and `jp` have their own).
      Which real languages were once 0, 6 and 9 is authoring history the binary does not carry;
      a reconstruction needs only the three treatments above. **AV-1.**
- [x] ~~What `+0x58` on the singleton holds.~~ **ANSWERED** - index 22, **`CameraRevise`**
      (Off/On, default On). Section 10. **AV-2.**
- [x] Where the language index at `+0x00` is written from. **AV-3.**
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (AV-3): all three — the OS, then the
      settings file, then Steam, which wins.* The singleton is built and filled in one sequence in `007980A0`:
      1. **`GameSettingConfig_InitDefaultsAndPath`** (`00798257`) copies the defaults, then replaces `Language` from the
         OS LANGID (`001DE0C0`; the mapping is [the settings page](../Game-Settings-Config/game-settings-ini-and-runtime-config.md) §9).
      2. The global is stored (`00798261`, the single store this page cites). **`GameSettingConfig_LoadOrCreateFile`**
         (`0079826B`) then parses `GameSetting.ini`, whose `Language=` value overwrites `+0x00` through the generic parse
         path (`001DF6AE`).
      3. **`007A0C60`** (`00798272`) then asks Steam.
         - It gets the context from `SteamInternal_ContextInit` (`007A0C94`) and takes `+0x30`. The context filler
           `001F3AE0` stores there the interface created with version string `STEAMAPPS_INTERFACE_VERSION…` (`001F3BED`–
           `001F3BFF`).
         - It calls vtable slot 4 (`007A0CAA`), the `GetCurrentGameLanguage` position in `ISteamApps`.
         - It matches the returned name by length and bytes: `japanese`→0, `english`→1, `french`→2, `german`→3,
           `italian`→4, `spanish`→5, `koreana`→6, `tchinese`→7, `schinese`→8 (`007A0D10`–`007A0F09`). That is exactly
           this page's code-table order.
         - It stores the index through `001DF340(cfg, 0, index)` (`007A0F17`). An unmatched name writes nothing.
      - **So when Steam reports one of the nine languages, the running game uses Steam's language**, whatever the OS or
        the ini said. The ini keeps its old value until the next settings write serialises all 31 settings. `007A0FC0`,
        which reads `+0x00`, runs immediately after (`00798277`).
      - **No menu writes it.** Of the 38 call sites of the generic setter, only `007A0C60` stores index 0 as a constant
        ([the Config screen](../../16-UI/Config-Screen/the-config-screen-and-what-a-setting-change-runs.md) §11, `DI-1`).
        The console's computed-index sites (`001D47E0`, `001D48A3`, `001D491E`, `001D4B60`, `001D4B76`) were not
        resolved to their index ranges.
- [x] ~~What consumes `0017E270`'s returned id.~~ **ANSWERED** — `0022A0B0` caches it at
      `0x01E02814` during startup. Section 6. **AV-4.**
- [x] ~~Why `0017E410` returns a hardcoded `10` — the same id as `jp` and as the unmatched default —
      and what the value cached at `0x01E0281C` is for.~~ **AV-5 closed 2026-09-12 (FABLE): the
      cache is dead.** A rip scan of `01E0281C` finds exactly one reference in the image — the boot
      store at `0022A0D6` — and **no reader**; the constant 10 is the fallback language id (`jp`, and
      the unmatched default) parked in a global nothing consults. Why the constant exists is
      authoring history; its effect in the shipped build is nil. **AV-5.**
- [x] ~~Which of `0x01E0C2A0` / `0x01E0C2A4` is the confirm mask.~~ **ANSWERED** — `0x01E0C2A0` is
      **confirm**, `0x01E0C2A4` is **cancel**. The confirm branch tests its handler's result and can
      fail (rejection sound `2`); the cancel branch discards the result and always plays sound `3`.
      Section 8. **AV-6.**
- [x] What id space `0x8001` / `0x8002` belong to. **AV-8.**
- [x] ~~What UI sound ids `2` and `3` are.~~ **AV-9 closed 2026-09-12 (FABLE): the names are not
      in the image or the data; the roles are.** `00249C60` is `Audio_RequestSound_WorldLiveResolve`
      ([how a sound request becomes a voice](../../18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md)): its argument is a **bank-local index**, resolved by `003A1180` to
      `bankSlot × 512 + index` against the current bank-slot handle at `02AEF3FC`, and `.sab` banks
      carry **no per-entry names** — only the bank's own name at `+0x10` ([the `.sab` container](../../18-Audio/Sound-Bank-And-Voice-Formats/sab-sound-bank-container.md); the one
      non-area bank, `se000`, 9.4 MB, names itself `se000` and nothing else). So "what sound 2 is"
      has no authored answer anywhere in the shipped files. What the image does fix is **who plays
      them**: index `3` is requested at **33** call sites and `2` at **15** (index 5 at 20, `0x25` at
      11, 4 and 1 at 8 each), and the sites that pass 2 and 3 are the menu widgets
      (`0023BD40`, `0023CE10`, `0023FBE0`, `00240AD0`, `00241D40` — the second and third read
      2026-09-17, SWE2-FRONTIER: `0023CE10` drives `00249C60` ×3 / `002445C0` ×3 / `00243260` ×2,
      first call [`0023CE6B`](../../_index/ADDRESS-INDEX.md); `0023FBE0` drives `00249C60` ×7 /
      `0023EF80` ×4 / `0023ED10` ×4 / `002405F0` ×3, first call `0023FC6D`) and
      `BattleMenu_UpdateCommandSelectionAndDispatch` (`00277E4C` = 3, `00277EC7` = 2) — the cancel /
      back path and the refused-confirm path this page already read. The bank the handle names at
      runtime is written by `003A1390`, which has no direct caller in the function list; its
      argument is not read here. **AV-9.**
- [x] Whether an options menu calls `0022A4F0`, which would make the convention a live, player-facing
      toggle rather than a start-up-only decision. **AV-7.**

## 6. Falsification pass 2026-09-02 — survived, and the confirm/cancel lead is now a finding

### Attack: is `+0x00` really *the* language index?

If any other code indexed the table at `0x01DF0030` from a different source, the reading would be
wrong. **The table is referenced by exactly one instruction in the executable** — the `lea` inside
`0017E270`. There is no competing indexer and no second index source. The claim stands.

### AV-4 answered: where the id goes

`0022A0B0` (owner `CoreRuntimeScheduling`, 978 B) is a startup routine that caches several derived
settings into globals in one run:

```asm
call 0x17E270 ; the language id           -> mov [0x01E02814], eax
call 0x17E410 ; returns the constant 10   -> mov [0x01E0281C], eax
call 0x17E210 ; the singleton's +0x64 field
```

**The language id is cached at `0x01E02814`.** `0017E410` is six bytes — `mov eax, 0xA ; ret` — a
hardcoded **10**, which is exactly the id `0017E270` returns for `jp` and for anything unmatched.
A fixed fallback sitting beside the computed value. **AV-5.**

### The confirm/cancel swap, confirmed

The `+0x64` field does not only reorder two binding fields. In the same routine it **exchanges two
button masks between two globals**:

```asm
0022A0E1  call  0x17E210          ; eax = singleton->+0x64
0022A0E8  mov   ecx, 0x2000
0022A0EF  mov   r8d, 0x4000
0022A0F5  mov   eax, r8d          ; eax = 0x4000
0022A0F8  setne dl                ; dl  = (field != 0)
0022A0FD  mov   [0x01FD4A64], edx ; cache the boolean
0022A103  cmove ax, cx            ; field == 0 -> ax = 0x2000
0022A107  cmove cx, r8w           ; field == 0 -> cx = 0x4000
0022A10C  mov   [0x01E0C2A4], cx
0022A119  mov   [0x01E0C2A0], ax
```

| `+0x64` | `0x01E0C2A0` | `0x01E0C2A4` |
|---|---|---|
| `0` | **`0x2000`** | **`0x4000`** |
| non-zero | **`0x4000`** | **`0x2000`** |

**Two button bit masks, held in two globals, exchanged by the locale field.** That is the
confirm/cancel convention as a mechanism, independent of what the bits are named — and it is the same
field that reorders the binding pair in
[the input stack](../../15-Input/Input-Stack/input-stack-device-channel-and-bindings.md) section 12.
**Two separate consequences of one setting, found from opposite directions.**

**On the bit values:** in the PlayStation button-mask convention `0x2000` is Circle and `0x4000` is
Cross. That identification is **external knowledge, not read from this binary**, and it is recorded
as such. Nothing here depends on it: the mechanism is a swap of two masks either way, and **which
global is "confirm" was not established at the time of this pass** — no consumer of `0x01E0C2A0` or `0x01E0C2A4` was read in
this pass. **AV-6.** *(Superseded by section 8, which answers it: `0x01E0C2A0` is CONFIRM. This
sentence is left in place because it was true of the pass that wrote it — the reading below is not
retracted, it is completed.)*

### A neighbourhood worth noting

`0x01E0C2A0` and `0x01E0C2A4` sit 24 and 20 bytes below
[force fight mode](../../00-Engine-Core-Runtime/Force-Fight-Mode/force-fight-mode.md) at
`0x01E0C2B8`. A block of small runtime-mode words. **Adjacency is banned as proof** and nothing is
inferred from it; it is recorded so a later pass reading that block knows both are in it.

### What this pass did not do

It did not establish which mask means confirm, what consumes them, or what writes `+0x64`
(**AU-5**, still open). It converts one lead into a finding and leaves the rest labelled.

## 7. The button convention as a complete mechanism (2026-09-02)

Section 6 established that `+0x64` exchanges two masks. The rest of the mechanism is small enough to
state in full.

| address | size | role |
|---|---:|---|
| `0x01F82D20 + 0x64` | 4 B | **the setting** |
| `0022A4F0` | 66 B | **apply** — owner `Input`, standalone and callable at any time |
| `0022A0B0` | — | startup apply, the same logic inline |
| `0022A540` | 12 B | **query** — `return g_flag == 0` |
| `0x01E0C2A0`, `0x01E0C2A4` | 2 B each | the two button masks |
| `0x01FD4A64` | 4 B | cached boolean `(setting != 0)` |

`0022A4F0` in full:

```c
void ApplyButtonConvention(void)          /* 0022A4F0, owner Input */
{
    int f = *(int *)(*(void **)0x01F82D20 + 0x64);
    *(int *)0x01FD4A64 = (f != 0);
    if (f == 0) { *(u16 *)0x01E0C2A0 = 0x2000; *(u16 *)0x01E0C2A4 = 0x4000; }
    else        { *(u16 *)0x01E0C2A0 = 0x4000; *(u16 *)0x01E0C2A4 = 0x2000; }
}
```

**It is a separate, self-contained function, not only startup code.** The convention can therefore be
re-applied while the game is running — which is what an options-menu toggle needs. Whether a menu
actually calls it is not shown here; the function's existence and shape are. **AV-7.**

### The masks are read almost everywhere

| global | reads | writes |
|---|---:|---:|
| `0x01E0C2A0` | 47 | **2** (`0022A0B0`, `0022A4F0`) |
| `0x01E0C2A4` | 39 | **2** (the same two) |

Consumers span `UI` (`BattleMenu_UpdateCommandSelectionAndDispatch`, menu and list handlers),
`Input` (`InputGameplay_ArbitrateDigitalInputAndMotion`) and a large amount of `Boundary` code —
roughly **90 read sites** for a pair of two-byte globals written in exactly two places. That is the
shape of a value the whole front end depends on and nothing but the settings path may touch.

**Which of the two is "confirm" is still not established at the time of this pass.** Naming it needs
a consumer read that distinguishes accept from cancel, not a count. **AV-6 — and section 8 does
exactly that read and answers it: `0x01E0C2A0` is CONFIRM.**

### Method correction made during this pass

The first reference census reported many of these sites as writes. **It was wrong.** It classified
any instruction with memory as operand 0 as a write, which mislabels `test word ptr [mem], imm`,
`cmp dword ptr [mem], reg` and `or ax, word ptr [mem]` — all reads.

Corrected by restricting writes to `mov [mem], reg`, the counts collapse from dozens to **two per
global**, and the two writers are the two functions above. **`struct_map.py` already encodes this
distinction in its `WRITERS` set; the error came from re-deriving the test inline instead of reusing
the tool's.** The wrong version made a settings value look like something ninety functions could
modify.

## 8. AV-6 answered — which mask is confirm (2026-09-02)

Counting references could never settle this; a consumer that treats the two differently can.
`BattleMenu_UpdateCommandSelectionAndDispatch` (`002778C0`, owner `UI`) tests both, a few instructions
apart, and the two branches are **not** symmetric.

```asm
;--- MASK-A4 branch, builds record id 0x8002 -------------------
00277E36  mov  rax, [rsi]          ; handler from the object's slot
00277E45  call rax                 ; result DISCARDED
00277E47  mov  ecx, 3
00277E4C  call 0x249C60            ; UI sound 3
00277E51  xor  eax, eax            ; always returns 0
00277E53  jmp  exit

;--- MASK-A0 branch, builds record id 0x8001 -------------------
00277EB8  call rax
00277EBA  test eax, eax
00277EBC  jne  0x277D3C            ; SUCCESS -> continue elsewhere
00277EC2  mov  ecx, 2
00277EC7  call 0x249C60            ; UI sound 2, only on failure
00277ECE  jmp  exit
```

| | `0x01E0C2A0` | `0x01E0C2A4` |
|---|---|---|
| record id built | `0x8001` | `0x8002` |
| handler result | **tested**, branches on success | **discarded** |
| outcome | may succeed **or fail** | always the same |
| UI sound | `2`, **only when it fails** | `3`, **always** |

**An action that can be refused is confirm; an action that always succeeds is cancel.** Selecting a
battle command can be rejected — no MP, invalid target, an unavailable command (see
[battle command availability and reason codes](../../07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md)) —
and the game answers with a rejection sound. Backing out of a menu cannot fail.

```
0x01E0C2A0  =  CONFIRM mask
0x01E0C2A4  =  CANCEL  mask
```

That also explains the distinct sound ids: `2` is the refusal buzzer on a rejected confirm, `3` the
ordinary cancel sound.

### The whole setting, end to end

| `+0x64` | confirm (`0x01E0C2A0`) | cancel (`0x01E0C2A4`) |
|---|---|---|
| **`0`** | `0x2000` | `0x4000` |
| **non-zero** | `0x4000` | `0x2000` |

In the PlayStation button-mask convention `0x2000` is Circle and `0x4000` is Cross — **external
knowledge, not read from this binary**. Under it, `+0x64 == 0` gives **Circle confirms, Cross
cancels** (the Japanese convention) and non-zero gives the inverse. That `0` is also the
"keep the authored pair order" case in
[the input stack](../../15-Input/Input-Stack/input-stack-device-channel-and-bindings.md) is
consistent: the authored order is the Japanese one, and everything else is the swap.

**The identification of confirm and cancel above does not depend on the button names.** It rests on
which branch can fail.

### What is still not established

- ~~What `0x8001` / `0x8002` are ids in. A third id space, distinct from the `0x4000` battle action
  space and from the button masks. **AV-8.**~~ *Answered (AV-8; superseded 2026-09-26 (FABLE, Claude Opus 5.5)): not an id space; they are the payload codes of message `0x0C`, confirm and cancel.*
- What sound ids `2` and `3` are named. **AV-9.**
- What writes `+0x64` — still **AU-5**, and still the question that decides whether a player can
  change this.

## 9. AV-8 not answered, and a name this database invented (2026-09-02)

### The constant census failed, and it was the right kind of failure

`0x8001` and `0x8002` looked like members of an id space worth enumerating. Scanning every
`mov [mem], imm` in the image for immediates in `0x8000`-`0x80FF` produced **15 distinct values
across ~180 sites** — and `0x8000` alone appears in **74 functions**, spread across `NativeRoutine`,
`NativeInline` and `Presentation`.

**That is contamination, not an id space.** `0x8000` is an ordinary constant — a sign bit, a buffer
size, a flag — and a bare-immediate search cannot tell those from a message code. This is the same
trap pass 58 recorded when `002D8050` used `0x4000` as a pointer-alignment constant. **The census is
withdrawn as evidence.**

What survives is only what the record itself shows:

```
[rbp-9]  dword  0x0C            kind
[rbp-1]  qword  0x8001 / 0x8002 code
[rbp+7]  qword  computed value
         -> lea rdx,[rbp-9] ; mov rcx,rsi ; call [rsi]   (slot-0 virtual call)
```

A 24-byte record dispatched through the object's first vtable slot. ~~**Identifying the space needs the
receiver `rsi`, not more constant scanning.** **AV-8** stays open with that as the next step.~~ *Superseded 2026-09-26 (FABLE, Claude Opus 5.5): **AV-8** is answered, and its premise was wrong. `0x8001` / `0x8002` are not an id space: they are payload codes of message `0x0C` to a window-procedure-style handler, `0x8001` confirm and `0x8002` cancel.*

### CORRECTION: `...AndDisplay` was never a real name

Sections 7 and 8 named `002778C0` **`BattleMenu_UpdateCommandSelectionAndDisplay`**. Its actual name
is **`BattleMenu_UpdateCommandSelectionAndDispatch`**.

The name first reached this database through a table whose column was cut at
`BattleMenu_UpdateCommandSelectionAndDisp`, and the missing ending was **completed rather than
looked up**. It then propagated to three files and five places before a full-width listing exposed
it.

**Nothing in the confirm/cancel finding depended on it** — that rests on which branch tests its
handler's result — but the failure mode is worth naming precisely: **a truncated identifier invites
completion, and completion feels like reading.** Standard rule 3 already forbids characterising a
*construct* from a truncated excerpt; it now covers identifiers explicitly.

## 10. The singleton identified, and the external premise withdrawn (2026-09-02)

`0x01F82D20` is the **GameSetting.ini configuration object** — 31 settings, one dword each, at
**offset = index x 4**. That explains every field this document had to guess at:

| field | index | key |
|---|---:|---|
| `+0x00` | 0 | **`Language`** |
| `+0x58` | 22 | **`CameraRevise`** (Off/On) — **AV-2 answered** |
| `+0x64` | 25 | **`DecideButton`** (Circle/Cross) |

Full layout in
[the GameSetting.ini configuration object](../Game-Settings-Config/game-settings-ini-and-runtime-config.md).

**The `0x2000` = Circle identification is no longer external.** Row 25 of the value-name table at
`0x01DFD150` is exactly `{"Circle", "Cross"}`, and `0022A4F0` writes `0x2000` to the confirm mask when
the field is `0`. **The game's own strings say which button it is.** Section 6's EXTERNAL caveat is
withdrawn — nothing in the confirm/cancel finding ever depended on it, and now nothing needs to.

### Two language tables, and they do not conflict

| table | entries | |
|---|---:|---|
| `0x01DFD150` row 0 | **9** — `jp en fr de it es kr ch cn` | the **ini value names**: what a player may select |
| `0x01DF0030` | **10** — the same nine plus **`none`** | the **runtime code table** documented in section 1 |

`none` exists at runtime and is not selectable. The two derivations agree on the nine and explain the
tenth.

**`Language`'s compiled-in default is `1` = `en`**, overwritten immediately after the defaults copy by
a region query at `001DE0C0`. So the shipped default is English and the effective default is the OS
locale — consistent with `0017E270` mapping an unmatched code to the same id as `jp`.

## 11. `ch` and `cn` identified (2026-09-02)

Section 1 listed `ch` and `cn` without saying which Chinese each is. The LANGID mapping at `001DE0C0`
settles it:

| code | index | is |
|---|---:|---|
| **`ch`** | 7 | **Chinese, Traditional** — selected for LANGID `0x0404`, `0x0C04`, `0x1404` |
| **`cn`** | 8 | **Chinese, Simplified** — selected for primary id `0x04` otherwise |

All Chinese LANGIDs share primary id `0x04`, so the code runs a **full-LANGID test first** to split
Traditional off, then falls back to the primary-id chain. `0x1C04` is explicitly excluded from the
Traditional set and therefore lands on Simplified.

**The unmatched default is `1` = `en`**, carried in a register (`edi`) initialised for the defaults
loop and never reset — which is why an unknown locale gets English while an unmatched *code string*
in `0017E270` gets the same id as `jp`. **Two different fallbacks in two different places**, and this
document previously described only the second.

Full mapping and the settings object in
[the GameSetting.ini configuration object](../Game-Settings-Config/game-settings-ini-and-runtime-config.md)
section 9.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL.*

**Rewards_Progression_Economy — CLIENT.**

- The locale getter `00229E40` is read by `EnemyChain_UpdateOnDefeat`. That is the chain clamp that
  [the chain page](../../13-Rewards-Progression-Economy/the-chain-and-its-sticky-coin.md) crossings trace to the locale:
  999 or 998 by locale.
- The sound resolver `003A1180` is called by the level-up path, the fanfare. It is MECHANICAL, the audio request chain,
  and is named here only because this page cites the resolver.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CombatAction — SERVICE.** `BattleMenu_UpdateCommandSelectionAndDispatch` calls `BattleUnit_IssueCommandByFocusHandles` and `BattleUnit_IssueCommandByFocusHandlesWithOptionalPartyFanout`. The localised battle menu hands the chosen command to the combat action layer.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**ActorEntity — SERVICE.** `0022A0B0` on this page calls `BattleStorage_InitializeWorkArrays`, owned by that layer. What it reaches is an initialiser: it writes +inf to `[02F973B8]`, zeroes `[02089300]`, sets `[0208E6A0]` to `0x20` and calls `003844F0`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatFormula — CLIENT.** `BattleFormula_ApplyTargetResult`, owned by that layer, calls `003A1180` on this page. That caller is the target-result application: it resolves the owning unit for both the source and the target stats records, keeps bit 9 of its flags argument as a switch, and **unless bit 0 is set** runs an eligibility test between the two units that abandons the whole call when it fails; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Script_VM_Native_Bridge — CLIENT (5 edges through 4 of this page's functions).** The Script_VM_Native_Bridge layer reaches this page at `00229E40`, `00229E50`, `003A1180`, `00473E80`. `FUN_0033fed0` is the worked example, read in full - it is a 37-byte forwarder that reads the frame-mode getter and **maps the single value `0xA` to zero** before passing it on; **5 of the 5 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).


**Presentation — CLIENT (SWE2-EC7-161, 94 edges).** `0027B430` — the locale-change emit this
page measured — drives `0027C730`/`0027D740`/`00275440`/`00244F00`/`00249C60` toward the widget
layer; the page's subjects are broadly consulted by Presentation (`0016D680` called by
`00183A00`/`00183C60`/`00183EE0`/`001946xx`). Consultation, not shared ownership.

**CombatAI — SERVICE (SWE2-EC7-163, 1 edge).** `0031EB20` — the shared emit
helper this page's `0027B5A0` marshal hands the copied record to — calls
`00327A10` (`GambitConfig_ClassifyActionTargetPairCompatibility`) on that
layer. The emit's downstream menu work, not a locale relationship.

**Gameplay — SERVICE (SWE2-EC7-163, 3 edges).** `0031EB20` also calls
`00309EC0`/`0030B0E0`/`00322C50` — the `BattleEncodedId` query helpers — on
the Gameplay layer. Same downstream fan-out; mechanical.

**Party — SERVICE (SWE2-EC7-163, 1 edge).** `0031EB20` calls `0031B7E0`
(`BattleUnit_ResolveByFocusHandle`) on the Party layer — the emit resolves
its unit there. Mechanical, not shared ownership.

**WorldAreaField — SERVICE (SWE2-EC7-163, 1 edge).** `0031EB20` calls
`00313F60` (`FieldData_GetActiveFieldRecordBit15`) on that layer — one more
of the emit's downstream reads. Mechanical.

**Movement — CLIENT (SWE2-EC7-166, 2 edges).** `00263C20`, the score
lookup this page's `0027D330` stat writer consults, is also called by
`00335760`/`00338490` on the Movement layer. A shared leaf, not a shared
responsibility.
## The `00473E80` exclusive subtree — all 4 members bound (SWE2-FRONTIER, followup queue)

`00473E80` (372 B) is the **locale-change dispatcher**: `ebx ≤ 4` gates a jump
through `00229E40` (`00473EE3`), and each of the six arms loads a 2-character
code pair from `.rdata` — `00D22658` (`in`), `009005E0` (`us`), `008C5918`,
`008C590C` (`fr`/`de` pair), `008C5914` (`it`/`es`), `008C5910` (`de`/`it`) —
before `0017D2E0`, `002DF8E0`, and the member chain `00183180` → `001D8D60`
apply it (`00473F93`–`00473FD2`).

| member | role | interior |
| --- | --- | --- |
| `00183180` (30 B) | the adapter — `001D8D30()` gets the context, tail `001D8D60(context, rbx)` (`00183194`) | [`00183189`](../../_index/ADDRESS-INDEX.md) |
| `001D8D60` (482 B) | the rebuild — `00183720`, `001D8FF0`, the `0059xxxx` text-service battery (`00597970`/`0059D920`/`0059FAC0`/`0059F4A0`/`0059BD40`), then `00184380` with the u16 code pair at `[rsp+0xAC]`/`[rsp+0xAE]` (`001D8E13`), `00210EC0`, `0016D680`, `0017EBD0`, `001EE820` (`001D8EBD`), `0062C360`, `00210EB0`, `0016D6A0`, `00598100` | [`001D8E13`](../../_index/ADDRESS-INDEX.md) |
| `00184380` (210 B) | the codec apply — `0085E730`, memset via `00861EC0`, then the `0061xxxx` text-conversion family `006160B0`/`0060DD70`/`00610990`/`00625F00`/`0061E200`/`0061FDA0` (interior read 2026-09-17, SWE2-FRONTIER: 1,190 B — `005FD050` first at [`0061FE1A`](../../_index/ADDRESS-INDEX.md), `0061C550` ×2 + `00620B70`/`0061F890`) | [`001843A9`](../../_index/ADDRESS-INDEX.md) |
| `001EE820` (185 B) | the 3→4-byte glyph expansion — `ebx` rows over `r11` (base + `(ebx-1)·edx` when the flag byte is set), inner `esi` pixels: `{[r9+2], [r9+1], [r9], 0xFF}` per 4-byte out (`001EE880`–`001EE8A8`) | [`001EE896`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00229E40` (jump table), `0017D2E0`,
`002DF8E0`, `001D8D30`, `00183720`, `001D8FF0`, the `0059xxxx` battery,
`006160B0`/`0060DD70`/`00610990`/`00625F00`/`0061E200`/`0061FDA0`,
`00210EC0`/`00210EB0`, `0016D680`/`0016D6A0`, `0017EBD0`, `0062C360`,
`00598100`, `0085E730`, `00861EC0`, `00808C40`.


## Interior citation — frontier hubs `00597970`, `00598100` (2026-09-18, SWE2-EC7)

`00597970` — 162 B, 16 callers (5 A-measured); the dual-vtable callable's ctor. Interior
verified: installs vtables `00D26C60` then `00D26C90` at `[rdi]`
([`005979BB`–`005979EE`](../../_index/ADDRESS-INDEX.md)), stamps `[+8] = 0xB`, copies `rdx`
through `001C26B0` into `[+0x10]` (`005979CF`), seeds `+0x28`/`+0x30`/`+0x40` to `-1`/0/`-1`,
keeps the `r8b` flag at `+0x38`, and sets `[+0x1C]` to `[+0x20]` or `-1` when it is zero
(`005979F1`–`00597A06`). Optional `rdx` arm runs `0059EE90` on the `+0x20` pair (`005979AF`).

`00598100` — 54 B, 16 callers (5 A-measured); the sibling ctor for the same callable family.
Interior verified: same `-2` sentinel local (`00598104`), vtable `00D26C60` installed at
`[rcx]` ([`0059810D`/`00598114`](../../_index/ADDRESS-INDEX.md)) — the pair are the
bind/locale-delegate objects the language path constructs per option.


### Interior citation — frontier hub `00610990` (2026-09-18, SWE2-EC7)

`00610990` — 61 B, 20 callers: the `0061xxxx` text-conversion family's level
recompute, called by the codec apply above. When `byte[rcx+0x18] >> 1` is odd it
takes `min(dword[+0x28], dword[+0x2C])` and counts its bit-length (`inc ecx` /
`shr eax` at [`006109B4`](../../_index/ADDRESS-INDEX.md)) — the mip count from
the smaller dimension — else `ecx = dword[rcx+0x10]`; the result is written to
`[rcx+0x14]` only when it changed.
### Interior citation — frontier hubs 001C26B0, 0061C550 (2026-09-18, SWE2-EC7)

Two hubs the locale/text-conversion family reaches:

- **001C26B0** (107 B, 4 A-measured callers) — `strlen`+alloc+copy: `0017D260(len+1, 2)` (the family's allocator) then `00861EBA` memcpy — the strdup the codec apply uses for per-locale name copies. Anchor [`001C26FB`](../../_index/ADDRESS-INDEX.md).
- **0061C550** (312 B, 4 A-measured callers) — the hex-key builder the `0061xxxx` text-conversion family names: copies the base name to a stack buffer, appends `_`, then eight hex chars of r9 (two chars per 8-bit shift group, high nibble first), then `call [r14] +0x28` — the resource-name format the locale record's table lookups key on. Anchor [`0061C60E`](../../_index/ADDRESS-INDEX.md).

## SWE2-EC7-18 update (2026-05-15) — `002405F0` locale-table XMM store block

`002405F0` (108 B) is the locale-id validator inside this page's selection path: `cl-4` bounds a six-arm `0012065C` jump table (`002405F7`..`00240612`) mapping slots `4..9` to word ids `0x1E`, `0x1F`, `0x23`, `0x22`, `0x20`, `0x21` (`00240614`..`00240637`); `00254DD0` probes the id (`0024063F`) and the body returns `(al==0)` — `1` when the probe fails or the index is out of range (`00240646`..`00240657`). The six ids are the selectable locale rows the language menu offers.

## SWE2-EC7-19 update (2026-05-15) — `00625F00` text-conversion prologue head

`00625F00` (11 B) is the `+0xBC` readiness predicate one of the `0061xxxx`/`0062xxxx` text-conversion family members this page groups with `006160B0`/`0060DD70`/`00610990` uses: its whole body is `cmp dword[rcx+0xBC],0; setne al; ret` (`00625F00`..`00625F0A`) — a three-instruction null test returning 1 while the record's `+0xBC` field is populated.

## SWE2-EC7-34 update (2026-09-19) - `0059EE90`

`0059EE90` (876 B) is the data-source resolver behind Phyre's file stream reader - cookie, `00865390`, the `00D27910` rdata string (`[FFXII_data_notcache] %s 
`, a data-source log tag), three `00808F10` allocs, `0059F1D6`/`005CDAA0`/`001D6B20`; called as `0059EE90(this+0x20, path, 1)` by the stream-construction family and it writes the data-source selector byte at `this+0x38`. (FABLE-CONTRA-0059EE90: not the locale init - reachable from locale code because locale code opens files; six callers, four the `005979xx` stream family.) Interior anchor `0059EEE8` (the `00865390` call).

## SWE2-EC7-36 update (2026-09-19) - `00240AD0`

`00240AD0` (656 B) is a language/locale body - `00914C64`/`0208E6C8`/`0209AC30`, `00305A00`/`003058B0`/`002F9860`/`002D48C0`/`002D46F0`. Interior anchor `00240B16` (a `00305A00` call).

## SWE2-EC7-36 update (2026-09-19) - `0061F890`

`0061F890` (598 B) is a locale record op - `00D551D8` rdata, `0061C550` pair plus `005FD050`. Interior anchor `0061F8B5` (a `0061C550` call).

## SWE2-EC7-42 update (2026-09-19) - `00620B70`

`00620B70` (317 B) is a locale body - `"PTexture_UAV"`, `00D551E8`, `005FD050`/`0061C550`. Interior anchor `00620B95` (a `005FD050` call).


## SWE2-EC7-64 update (2026-09-19) - `007A0FC0`

`007A0FC0` (142 B) is a call-free LCID dispatch leaf - `ecx` = `0x407`-`0x412` arms, `jmp [008C22E0]` IAT tails (`SetThreadUILanguage` family). Interior anchor `007A0FE0` (the `jmp rcx` dispatch entry).



## SWE2-EC7-64 update (2026-09-19) - `001D8FF0`

`001D8FF0` (139 B) is a text-service rebuild body - `00183720`/`005CDAA0` plus `008C5B40`/`009003C0`. Interior anchor `001D9005` (a `005CDAA0` call).


## SWE2-EC7-67 update - `002DF8E0`

`002DF8E0` (128 B) is a recursive locale-path probe - `001D6F20`/`001D6EE0`/`001D6E80`/`001D6EC0` family plus self-call `002DF8E0`. Interior anchor `002DF8F2` (a `001D6F20` call).

## SWE2-EC7-103 update (2026-09-20) - `0027EC40` measured

`0027EC40` (205 B) is the indexed pair publish
`0023E020` and `00240AD0` call: gated on
`[02EBF190]` and `[0209AC30]+0xF8` both nonnull,
`0030A790` fills a stack record and returns a
count, then each `rbx` entry pairs
`[rdi + rbx*8 + 0xC0]` (its `[+0x60]` node's
`+0xB0`, or `rbp` when null) with
`stack[rbx]`'s `abs(dword[+0x190])` into a
`0029FF60` call with `rdx + 0xD0`, `r8d = 0x20`
and the `ebp`/`rbp` zeros - the per-entry
rect/id publish the locale-change arms run.
Interior anchor `0027ECEB` (the `0029FF60`
call).

## SWE2-EC7-107 update (2026-09-20) - `0023CC90` measured

`0023CC90` (129 B) is the deferred
`0x4C0` install `0023FBE0` and
`00281ED0` call: while `0208E6D0`
is null it builds the `{0, cl, 0}`
stack descriptor, runs
`00244F50(0x4C0, 0023CE10, &desc)`,
stores the result to `0208E6D0`,
binds it through
`00246AD0(*0208EA28, result)`, and finishes with
`002CA150(002F9860(0x504), 0)` -
the one-shot register the locale
arms share.
Interior anchor `0023CCD0` (the
`00244F50` call).

`0027B430` (362 B) is the emit `002778C0` calls: `dword[r8 + 0x2FF0] >> 11 & 1` is the flag bit, `word[rdx + 0x153E]` the arg, `0027C730(rdx + 0x4C0, ...)` stages, `0027D740` broadcasts (the widget emitter), then `00275440` x4, `00244F00`, `00249C60` - the locale-change notification path.

Interior anchor `0027B474` (function `0027B430`).

`0027C730` (306 B) is the staging lookup `002778C0`/`0027B430` call: `edx` signs to `esi` (`>0`->1, `==0`->0, `<0`->-1), `[rcx]` mode `0xD`/`0xF`/`0x1C` selects the `(eax, r15d)` pair `(1,0x11)`/`(2,0x12)`/`(3,0x13)` with `(0,0x10)` default, then `0027B5A0`/`0027B6C0` - the emit's mode-to-constant map.

Interior anchor `0027C7E1` (function `0027C730`).

`0027CD00` (353 B) is the locale compute `002778C0` calls: `[rcx + 4]` nonzero gates `00273710`, `002713E0` fills `[rbp + 0x27]`, `002722A0(rbp - 0x19, 02AEDDB0, rbp + 0x27)` formats, `cvtdq2ps` + `comiss` on `[rbp - 0x11]` writes `word[rbx + 8] = 1` when negative - the locale refresh's sign flag.

Interior anchor `0027CD2F` (function `0027CD00`).

`0027B5A0` (288 B) is the marshal `0027C730`/`002778C0` call: `__chkstk` probes 0x1088 bytes, then copies the record (`+8`/`+0x18`/`+0x28` movups, `+0x38` movsd, `+4`/`+0x44` dwords) into the frame and hands it to `002647E0`/`00273710`/`0031EB20` - the locale emit's record copy.

Interior anchor `0027B5AC` (function `0027B5A0`).

`0027D330` (332 B) is the per-slot stat pair `002778C0` (`BattleMenu_UpdateCommandSelectionAndDispatch`) writes: computes `(word[rbx+0xF4]+word[rbx+0xF2])*byte[rbx+0xEC] + sbyte[rbx+0xEE] + sbyte[rbx+0xED]` into `[r8+0x2FE8][rcx*4+0x14]` and a second variant into `+0x16`, then a `+0x2FF0 & 0x400` gate with `dword[rsi+0x4C0]==0xF` selects a `002737B0`/`003588B0`/`00263C20` consult on `[rsi+r9*8+0x510]` - the command-selection stat staging.

Interior anchor `0027D42E` (function `0027D330`).

`0027C280` (323 B) is the filtered collector `002778C0` (`BattleMenu_`) calls: `0035D4E0` returns the id table (0 -> returns `r15d`), then for each of `dword[r12]` entries `00273320` resolves `[r14]` and `0035BB20` fetches the record - entries whose `byte[rax]&9` is clear are appended to the stack buffer as `(esi, eax)` pairs (`ebp` counts) before `00273600`/`00808C40` finish - the menu's accept-mask enumeration.

Interior anchor `0027C2F4` (function `0027C280`).

`0027D480` (238 B) is the id-pair emit `002778C0` runs: `edx - 2 <= 0x12` dispatches a 19-arm jump table at `0027D570` whose arms load `(ecx, edx)` pairs - `0x15`/`0x12`, `0x15`/`0x13`, `3`, `7`, `6`, `0xD`, `edx - 0xA` with `0x18`, `r8w` with `0x14` - into `0035D330`, then `[rax+0x18]` feeds `002B58B0` and the result (default `01CEB638` zero) goes with `rbx` to `003EE8C0`; the `word[rbx+0x4B0] x 0x1E0` row takes `+0x290 = 1.0f` and `+0x294 = dil` - the battle-menu command-label publish.

Interior anchor `0027D4BD` (function `0027D480`).

`003EE8C0` (305 B) is the ping-pong text-slot reset `0027D480` runs on the locale record: the `[rcx+0x4B0]` counter selects a `0x1E0`-stride slot in the `+0x294`-offset bank (flag word masked `& 0xFFFFFCFF` before the counter wraps at 2), the slot's `+0xC0`-based twin is then initialised - `+0x1D4` gains `0x300`, `+0x88` = 1.0f, `+0x1D0`/`+0x188`/`+0x1B8` zeroed, the arg2 name copied through `00254F30` into the 0x80 field (a null name writes a single NUL), `+0x1D4` bit 0x200 cleared when both arg3 and arg4 are zero, and arg3/arg4 stored at `+0x18C`/`+0x1BC` - before tail-jumping `002B3400` on the `rdi+0x160` bank's matching slot.

Interior anchor `003EE95D` (function `003EE8C0`).

`00273600` (173 B) is the insertion sort `0027C280` runs over the locale list: `ecx` qword entries at `rdx`, `r8d` selecting order - the inner loop shifts `[r9+i*8]` right while the moving element's low dword compares `jle` (ascending arm) or `jge` (descending arm) against it, `r9+8` stepping one entry per outer pass

Interior anchor `00273636` (function `00273600`).

`0027DE30` (154 B) is the query-and-submit wrapper `002778C0` runs: `00272E10(ecx, edx, out = rsp+0x30)` fills the query record; when it returns 0 and both out dwords are empty `00290B90(ecx)` answers instead; else `00321060(ecx, out2)` resolves and on a non-negative result `00290320(ecx, out[+8])` submits - a nonzero `ebx` is passed to `0028F9E0` once more and returned on success.

Interior anchor `0027DE58` (function `0027DE30`).
