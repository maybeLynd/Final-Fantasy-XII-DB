---
system: The NPC name dictionary — npcdic.bin, the actor's +0x102 name id, and the persistent flag that swaps a name
category: 04-Actor-Entity
status: AUDITED
owner_layer: PrimaryOwner:ActorEntity — the file belongs to the resource pipeline, the lookup to the actor
evidence_tier: 1
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the binder, the relocation callback, the three accessors, the display-name resolver, the setter and
    the two script verbs read whole; the shipped us/bin/npcdic.bin extracted from the archive and decoded with
    the text encoding of section-002-text.md; the persistent-flag query is the flag-banks page's
last_reviewed: 2026-09-11
archive_formats:
  - "NPC0 | explained | npcdic.bin (.bin member): {NPC0, u32 relocated, u32 count, i32 offsets[count], strings} - binder 003EAC40 (kind 9, 0x1F) to 02B5E0D8, relocating callback 003EAC70, section 2"
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-npcdic-pass-1 - the us file re-decoded from the archive and exact (37,545 B, NPC0, 2282, 1141 pairs, 247 differing, section-002 encoding, both section-1 examples verbatim); new: all nine locales share NPC0/2282/1141 while the differing-pair count is per-language, 247 us to 275 fr
  last_pass_kind: authored
  crossref_clean: true
  reopened_count: 0
---

# The NPC name dictionary

> Every field NPC carries a 16-bit name id. The id indexes a **pair** of strings in one file,
> `npcdic.bin`, and a persistent flag with the same number decides which of the two the game
> shows — which is how "Rabanastran" becomes "Arryl" once you have met her. 1,141 pairs, 247 of
> which differ.

## 1. What the player sees

A townsperson's name tag reads "Imperial", "Rabanastran", "Wistful Bangaa" — until that person's name flag is
set (by the first message window opened for them, or by a script; section 2.3), after which the same person is "Sherral" or "Arryl". Nothing about the actor changes; the
second string of its name pair is chosen.

## 2. Native mechanism

### 2.1 The file and its binder

`003EAC40` (36 B) is the dictionary's binder: it calls the resource loader `0051ED10(kind 9,
index 0x1F, callback 003EAC70)` and stores the returned block at the global **`02B5E0D8`**
(`003EAC44`–`003EAC58`). Its only caller is `00379D20`, the boot loader of three kind-9 tables — `questbase.bin` (index `0x21`, `02CA6C60`) and `musicctrl.bin` (index `0x20`, `02B5E0D0`) follow the same path ([the music-control page](../../18-Audio/the-music-control-file-and-the-bgm-stream.md) §2.1). The shipped file that block holds is
`ps2data/image/ff12/<lang>/bin/npcdic.bin` — resource-pool entry `84 + 31` for a language block
(`…/es/bin/npcdic.bin` at pool index 115), 37,545 bytes for `us`:

```
NpcDictionary               (npcdic.bin, base = file start; loaded whole, relocated in place)
  +0x00  char[4]  magic "NPC0"
  +0x04  u32      relocated flag        0 in the file; 003EAC70 sets 1
  +0x08  u32      count                 2282 = 1141 pairs
  +0x0C  i32[count] entries             file offsets in the file, string pointers once relocated
  +0x23B4 …       the strings           0-terminated, text encoding of section-002-text.md
                                        (0x20–0x39 = A–Z, 0x3A–0x53 = a–z, 0x04 = space)
```

The callback `003EAC70` (39 B) walks the `count` entries adding the block's address to each
(`003EAC7E`–`003EAC8D`) and writes the flag `+0x04 = 1` (`003EAC8F`), so after loading each entry
is a pointer. Entry `2 × id` is the pair's **first** name, `2 × id + 1` its **second**; the first
entry's offset is exactly `0x0C + 4 × count = 0x23B4`, which is the layout's own check.

### 2.2 The three accessors

| function | returns | bounds |
|---|---|---|
| `003EAC10(id, flag)` | entry `2 × id + (flag != 0)` | null block or `2 × id + flag ≥ count` → 0 (`003EAC12`–`003EAC33`) |
| `003EABE0(id)` | entry `2 × id + 1` — the second name unconditionally | the same bounds (`003EABE0`–`003EAC02`) |
| `003EAC70(block)` | — | the relocation callback above |

### 2.3 Which name: the actor's `+0x102` and a persistent flag

`00263990(actor)` (74 B) is the display-name resolver ([the spawn keep entry](../../05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md)
§7, `FD-3`): if the actor's word `+0x102` is negative it returns the literal text pointer at
`+0xF8` (`00263994`–`002639AB`); otherwise it strips bit 14 of the id, asks
`PersistentFlag_QueryBank2048(id)` ([the flag banks](../../14-Story-Event-Quest-Hunt/persistent-flag-banks.md)),
and calls `003EAC10(id, flagSet)` (`002639B1`–`002639D5`). So **the persistent 2,048-bit bank's
bit `id` selects the second string of pair `id`** — the flag and the pair share one number.
`002639E0` (42 B) does the same from a bare id, and `0026DEA0` (18 B) from an explicit `(id, flag)`.

**Who sets the bit (added 2026-09-18, FABLE).** Not only scripts. The message-window opener `002E16B0(actor, ...)` begins, for a non-null actor, with `PersistentFlag_SetBank2048(actor word +0x102, 1)` (`002E16DF`..`002E16EB`); the setter rejects ids above `0x7FF` unsigned, so a negative literal-pointer id sets nothing. So **the name changes because the player opened a conversation with that actor** - the engine records it, and the script verbs over the same bank are the second way in. The bank side is on [the flag banks](../../14-Story-Event-Quest-Hunt/persistent-flag-banks.md) (UQ-138). Static.

The id is written by `00269F40(actor, id)` (16 B): a non-negative id has bit 14 cleared and is
stored at `+0x102` (`00269F40`–`00269F4F`); a negative one is stored as is — the literal-pointer
case above. The two script verbs behind it are `setnpcname` (`0x38A`, `0034B9A0`) and
`setshopname` (`0x4A9`, `0034C170`): each pops one int (`00267E10`) and, for a **negative** value,
only stores it if `003EABE0(id)` returns a non-null entry (`0034B9B7`–`0034B9CC`) — a guard
whose index arithmetic on a negative id is the page's open item.

### 2.4 The shipped pairs

Decoded from `us/bin/npcdic.bin` with the encoding above:

| pair | first | second |
|---:|---|---|
| 0 | Rabanastran | Rabanastran |
| 1 | Imperial | Imperial |
| 3 | Awein | Awein |
| 5 | Chocobo Aficionado | Chocobo Aficionado |
| 16 | Imperial | **Sherral** |
| 104 | Rabanastran | **Arryl** |
| 105 | Rabanastran | **Nathyl** |
| 106 | Rabanastran | **Hedg** |
| 107 | Rabanastran | **Wakk** |
| 108 | Rabanastran | **Cotze** |

247 of the 1,141 pairs differ; 894 repeat the first name, for which the flag changes nothing.

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `003EAC40` | `NpcDictionary_Load` | 36 B | binds `02B5E0D8` through `0051ED10(9, 0x1F, 003EAC70)` |
| `003EAC70` | `NpcDictionary_RelocateEntries` | 39 B | offsets → pointers, `+0x04 = 1` |
| `003EAC10` | `NpcDictionary_GetName` | 39 B | entry `2 × id + flag` |
| `003EABE0` | `NpcDictionary_GetSecondName` | 35 B | entry `2 × id + 1` |
| `00263990` | `Actor_GetDisplayName` | 74 B | `+0xF8` literal, or the pair by `+0x102` and the flag |
| `002639E0` / `0026DEA0` | name by id / by (id, flag) | 42 / 18 B | the same lookup without an actor |
| `00269F40` | `Actor_SetNameId` | 16 B | `+0x102`, bit 14 cleared for non-negative ids |
| `0034B9A0` / `0034C170` | `setnpcname` / `setshopname` | 60 / 88 B | the verbs |
| `0032A930` | `PersistentFlag_QueryBank2048` | 100 B | the selecting flag |
| `02B5E0D8` | — | — | the dictionary block pointer |

## 4. Data structures and formulas

```
name(actor) = actor.w_102 < 0 ? actor.p_F8
            : dict[2 * (actor.w_102 & ~0x4000) + (Bank2048[actor.w_102 & ~0x4000] ? 1 : 0)]
```

## 5. Call chain

```
resource load (00379D20) -> 003EAC40 -> 0051ED10(9, 0x1F, 003EAC70) -> 02B5E0D8 -> 003EAC70 relocates
script: setnpcname / setshopname -> 00267E10 pop -> 00269F40 -> actor +0x102
display: 00263990(actor) -> 0032A930(id) -> 003EAC10(id, flag) -> the string
```

## 6. Modding notes

- **To rename an NPC** edit the pair in `npcdic.bin`; to make a reveal happen, set the persistent
  flag with the pair's number — the second name needs no script change.
- **Pairs whose two strings match** are inert: setting their flag changes nothing visible.
- Ids with bit 14 set reach the same pair as without it; the bit is stripped before both the flag
  test and the lookup.

## 7. What is not known

- [x] **FN-2.** ~~**What bit 14 of a script-assigned name id marks**, and why `setnpcname` accepts a negative
  id only when `003EABE0` finds a non-null entry for it.~~ **ANSWERED 2026-09-14 (FABLE) for the name id and
  `+0x102`; its `+0x100` residue is split out as `FN-3` below (the register rule for a row asking two questions).**
  *narrowed 2026-09-13 (FABLE):* **bit 14 is never produced for a name, and the negative-id guard is a "dictionary loaded" test.** The setter `00269F40` clears bit 14 of every non-negative id before storing it (`00269F44`) and the resolver strips it again (`002639B4`, `002639C6`); the 1,114 decompiled `us` scripts call `setnpcname` 6,220 times and `setshopname` 127 times, and none of the 6,206 literal arguments has bit 14 set — the only negative literal is `setnpcname(−1)`, 91 times; the other 141 calls pass a variable. For `−1`, `003EABE0` computes index `2 × (−1) + 1 = −1` and reads `[npcdic + 0xC − 4] = [npcdic + 8]`, the dictionary's own count dword (`003EABE0`–`003EABFA`), so `setnpcname(−1)` is accepted exactly when `npcdic.bin` is loaded with a non-zero count, and then makes the resolver return the actor's literal text pointer `+0xF8` — the spawn entry's own name. **The other 16-bit writers of `+0x102` are not actor records:** `003AAA50` writes a stack local (`rbp = rsp − 0x198`, `003AAA57`), `0041B550` a mask object handed in `rcx` (called from `0041BEE0`, which also ORs bits into the same word at `0041B5FA`), and `00552250` / `005528C0` counters of UI objects built by the widget factory. Residue: the same classification for the 16-bit writers of `+0x100` beside `00269F20`. *Residue narrowed 2026-09-14 (FABLE, FN-2):* an image-wide scan of 16-bit stores to `+0x100` gives 24 sites *(22 until 2026-09-14; the first scan matched single-base operands only and missed two indexed stores — `AUDITSEM-CONTRA-FABLE-FN2-PLUS100`)*. Two are the actor's: the setter `00269F20` (`00269F27`) and the initialiser (`002666C1`). Fourteen are the non-actor objects already classified above or plainly not records: `003AAA50`'s stack frame (`003AAB9D`), `0041B550`'s 0x108-stride element (`0041B585`), the world-map widget objects (`00552250` ×3, `005528C0` ×5), `rsp + 0x100` in `0055BAC0` (interior read 2026-09-17, SWE2-FRONTIER: the store is at [`0055BB9A`](../../_index/ADDRESS-INDEX.md), read back at `0055BF1D`; `00282DF0` first call at `0055BAE0`, then `00365B30`/`002F9860`/`002DD7E0`/`002DB080`), and three PhyreEngine objects in `0063xxxx`. Eight are untyped: `0053AB50` twice (`0053B701`, `0053B730`, `mov word [r13 + r15*2 + 0x100]` — an indexed array element whose base `r13` is the function's second argument, which the auditor traces to the FCP character parameter block fed from `00521290` records), `001294D0` (base loaded from `[rbp+0x18]`), `002D14E0` (an allocation result, beside a store to `+0xEA`), `003A8020` and `003A8290` (Presentation, beside `+0xE8` / `+0xF0` and a call to `004FF080`), `004FF080` (clears `+0x103` bit 0 beside `+0x100`) and `00504520` (an indexed element).  None of the eight reaches its base through the actor route, and their neighbouring fields do not match the actor record's `+0xF8` / `+0x100` / `+0x102` name trio. **Not typed by allocator, so this stays a narrowing, not a proof.**
- [x] ~~**FN-3.** **Whether any of the eight untyped 16-bit stores to `+0x100` writes an actor record.**~~
  **ANSWERED 2026-09-16 (FABLE) — no, not one of the eight, and the answer is a typing rather than an
  absence.** *Split from `FN-2`, 2026-09-14 (FABLE).*

  **The discriminator is size.** An actor record is carved from **one** `memset`-zeroed pool allocation by
  `ActorStorage_AllocateAndInitializeRecords` (`002679F0`) at **720 to 1,760 bytes** per kind, from the eight-entry
  table at `01E0C328` (`EH-2`, `EH-6`); the `+0x100` writer that *is* the actor's sits inside
  `ActorStorage_InitializeRecord` (`002666C1`, in `00266530`) beside the setter `00269F20` (`00269F27`). **Every one
  of the eight that reaches an allocator allocates 336 to 448 bytes** — smaller than the smallest actor record of
  any kind. The eight stores are four objects, not eight.

  | store | object | how the base is typed | actor record? |
  | --- | --- | --- | --- |
  | `0053B701`, `0053B730` (in `0053AB50`) and `00504557` (in `00504520`, sole caller `0053AB50`, same base in `rcx`) | element `idx` of a **u16 handle array** at `base + 0x100` | `base` is `0053AB50`'s second argument, spilled at `0053ABFD` and reloaded at `0053B57E`; both call sites in `0053D780` (`0053DA5B`, `0053DA94`) pass a **resource-table entry** returned by `ResourceTable_ResolveEntryBySignedIndex16` (`004780B0`) over the table at `+0xDA0` | **no** |
  | `001295B8` (in `001294D0`) | **no object at all** — both callers pass `lea rdx, [rbx + 0x180]` (`0017027C` in `0016FE80`, `00174B05` in `00174790`), an interior pointer into the caller's own block | the body writes **sixteen u16s at a stride of `0x20`**, `+0x00` through `+0x1E0`, unpacked from SSE lanes with `movd` / `psrldq`; `+0x100` is lane 8 of 16 | **no** |
  | `002D168F` (in `002D14E0`) | a **336-byte** heap object | `00244F50(0x150, 002D2DB0, 0)` at `002D14FC`; `00244F50` serves sizes up to `0x120` from a 112-slot pool of 288-byte slots at `[0208EA58]` flagged by `+0xA2`, and routes anything larger to `002497B0` then `0036A100` | **no** |
  | `003A80A8` (in `003A8020`), `003A8304` (in `003A8290`), `004FF08F` (in `004FF080`) | one object of **352, 432 or 448 bytes** | `byte [descriptor + 0xC2]` picks `0x160` / `0x1B0` / `0x1C0` at `003A807C`–`003A808A` and `0036A190` allocates it | **no** |

  **The handle array is the strongest of the four, because it is not a field at all.** `[r13 + r15*2 + 0x100]` is
  read at `0053B6BA` and written at `0053B701` / `0053B730`, and the same object carries a **u32 array** at
  `[r13 + r14*4 + 0x140]` — two indexed arrays where the actor record has two scalars. The index is variable by
  construction: `r15d` comes from `movzx r15d, byte [rbp + rax + 0x83b0]` (`0053B6B1`), a byte remap table the
  function builds at `0053B480` / `0053B523` and reads once per iteration of the loop that carries `[rbp + 0x90]`.
  **At index 1 the store would land on `+0x102`**, the actor record's other name word, so the two layouts cannot be
  the same object. What the slots hold is settled too: they are handles into the **256-entry, 48-byte** table at
  `[02CA8450]` with its live count at `[02CA8458]` — `005210F0` allocates and returns `0xFFFF` when 256 are live,
  `005212E0` resolves `table + (h & 0xFF) * 48` only if `word[entry] == h`, `00521250` releases against the
  refcount at `word[+0x24]`, and `0xFFFF` is the free sentinel `00504520` tests at `00504545`. **Resource handles,
  not name ids.**

  **The list object is the second.** `003A8020` is its constructor: it allocates, calls `004FF080` to clear
  `+0xE0` / `+0xE8` / `+0xF0` / `+0xF8` and `word +0x100` and bit 0 of `+0x103`, then writes `word +0x100` from its
  third argument, **`byte +0x102`** from its fourth, and `+0xE0` with the descriptor back-pointer, and links the
  object into the list anchored at `[02EBEF98]` — `+0xE8` previous, `+0xF0` next, head at `[anchor]`, tail at
  `[anchor + 8]`. `003A8290` walks that list through `+0xF0`, matching `word +0x100` against its argument. So here
  `+0x102` is a **byte** where the actor record's is a u16, and `+0xF0` is an **8-byte link** where the actor
  record has a 4-byte undeclared span (`EH-3`).

  **Where this is a typing by use rather than by allocator, it says so.** The handle-array base is typed by its
  **owning collection** — a resource-table entry — which is the second of the two routes this question asked for;
  its own allocator lives inside that table and was not chased. The 32-slot reading of the u16 array rests on the
  u32 array at `+0x140` abutting it, which is adjacency and is **inference, not measurement**.

  *Correcting `FN-2`'s residue line above:* it says `0053AB50`'s base is *"the FCP character parameter block fed
  from `00521290` records"*. The base being the second argument is right. The relationship to `00521290` is
  backwards: `00521290` is the linear search over the same 256-entry handle table, and its records are what the
  block's `+0x100` array **points at**, not what feeds the block.
- [x] ~~**UQ-92.** **How resource kind 9 resolves to the language `bin` block** — inferred here from the index
  (`0x1F` → pool entry `84 + 31` = `npcdic.bin`) and the file's layout matching the accessors,
  not from the loader's kind table (`0032E400`'s per-kind size arrays at `022C51F0`).~~
  **Answered 2026-09-14 (FABLE), from the loader:** the inference holds, and it is now read rather than matched.
  - **The resolution is a two-level table.** The read issuer `002DF780` takes the path as `directory[kind][id]`: it loads `[0215F000 + kind × 8]` (`002DF7BF`), then `[that + id × 8]` (`002DF7CC`). The size probe `0032E400` only sizes the file.
  - **The language picks the table.** `ResourcePath_Init` (`002DF9A0`) switches on the language and, in each of nine arms, stores that language's kind-9 path array into directory slot 9, `0215F048` (`002DFC11`, `002DFC63`, `002DFCC3`, `002DFD23`, `002DFD83`, `002DFE2E`, `002DFEB8`, `002DFF11`, `002DFF6A`).
  - **Entry 31 is the dictionary in every language.** Read from the image, entry 31 of each of the nine arrays is `PS2Data\image\ff12\<lang>\bin\npcdic.bin` for `us`, `fr`, `de`, `it`, `es`, `kr`, `cn`, `ch` and `in`. Entry 32 of the three arrays checked (`us`, `fr`, `in`) is `in\common\musicctrl.bin`, the music table's request (kind 9 index `0x20`).
  So `0x1F` is the id inside kind 9, and the `84 + 31` pool arithmetic describes the same string from the pool's side.

## 8. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| The binder, callback and three accessors | `003EAC40`, `003EAC70`, `003EAC10`, `003EABE0` read whole | 1 | PROVEN |
| The flag selects the second name | `00263990` read whole: `0032A930` then `003EAC10(id, result != 0)` | 1 | PROVEN |
| The file's layout | `us/bin/npcdic.bin` extracted: magic, count 2282, first offset `0x23B4 = 0x0C + 4 × 2282`, strings decoded with the section-002 encoding | 1 (shipped data) | PROVEN |
| The setter and the verbs | `00269F40`, `0034B9A0`, `0034C170` read whole; verb table rows `038A` / `04A9` | 1 | PROVEN |
| Kind 9 = the language `bin` block | index match and layout match only | 2 | PLAUSIBLE |

## 9. Related

- [`../../05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md`](../../05-Spawn-Encounter-Lifecycle/Spawn-Record/the-spawn-keep-entry-field-map.md) — where `+0xF8` / `+0x100` / `+0x102` come from.
- [`../../14-Story-Event-Quest-Hunt/persistent-flag-banks.md`](../../14-Story-Event-Quest-Hunt/persistent-flag-banks.md) — the 2,048-bit bank.
- [`../../25-EBP-Script-Container/Sections/section-002-text.md`](../../25-EBP-Script-Container/Sections/section-002-text.md) — the text encoding.

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run first, one query at a time and read in full.)*

### The file reproduces exactly, decoded from the archive

`ps2data/image/ff12/us/bin/npcdic.bin` re-extracted and walked with independent code:

| claim | measured |
|---|---|
| 37,545 bytes for `us` | **37,545** |
| magic `NPC0`, `+0x04` = 0 in the file | **`NPC0`**, **0** |
| `count` 2282 = 1,141 pairs | **2282**, **1,141** |
| the strings begin at `+0x23B4` | the entry array ends at **`0x23B4`** exactly, and the lowest entry offset **is** `0x23B4` |
| entries are file offsets | ascending, `0x23B4`…`0x9297`, all inside the file |
| the `section-002-text` encoding | decodes cleanly — `0x20`–`0x39` → `A`–`Z`, `0x3A`–`0x53` → `a`–`z`, `0x04` → space |
| **247** pairs differ | **247** |

And §1's two examples come out of the bytes verbatim: pair **16** is `Imperial` → `Sherral`, pair
**104** is `Rabanastran` → `Arryl`.

### ✔ New: the structure is a nine-locale invariant, the content is not

Nine copies ship — `ch cn de es fr in it kr us` — and **every one** carries magic `NPC0`, `count`
**2282** and **1,141** pairs. **So "the id indexes a pair" is not a `us` artefact**; the pair count is
fixed across every language while the string blob is translated (sizes run **30,426** for `in` to
**43,006** for `de`).

**What is *not* invariant is how many pairs actually differ:**

| | `us` | `ch` | `in` | `kr` | `cn` | `de` | `es` | `it` | `fr` |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| pairs whose two strings differ | **247** | 250 | 250 | 250 | 252 | 255 | 257 | 261 | **275** |

> **This matters for the mechanism, not just for the census.** §2 establishes that the flag selects
> entry `2·id + 1` — it does that whatever the strings are. Where a pair's two strings are
> byte-identical the swap happens and **is invisible**. So the same story flag produces a visible
> rename for **28 more ids in French than in English**, and a modder who tests the mechanism in one
> language can watch a name not change and conclude the flag did nothing. **The id space is shared;
> the set of ids on which the swap shows is per-language.**

**Not claimed.** `FN-2` is untouched — what bit 14 of a script-assigned name id marks, and why
`setnpcname` accepts a negative id only when `003EABE0` finds a non-null entry, are still open. So is
§7's second item: **how kind 9 resolves to the language `bin` block** is still inferred from the index
and the layout, not read from `0032E400`'s per-kind size arrays at `022C51F0` — this pass did not
touch the loader. Which of the 247 (or 275) pairs a shipped flag actually sets: **not traced**; the
pairs are counted, not matched to flags. Nothing was executed and no name was observed in game.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Audio — SERVICE, not read.** Two cited functions call a 51-byte Audio-filed helper. What it does is not read here.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Movement — SERVICE, and the crossing is incidental to why this page cites the caller at all.**
`ActorStorage_InitializeRecord` (`00266530`), which this page cites **only** to locate the actor's
`+0x100` writer for `FN-3`, calls two Movement-owned bodies. **They are its business, not the
dictionary's, and naming the caller is what pulled them in** — recorded here because the pass-22
rule is that naming a far end obliges the sentence, not that the sentence has to pretend the crossing
is a shared responsibility.

- The **1,339-byte** one sets the record's `+0x09` to `(prior & 0xE9) | 1` — **bit 0, field movement
  enabled**, which is `BV-3`'s answer and is why this call sits in the initialiser at all — and then
  installs defaults into the **movement context** at `[record+0xB8]`: `1.0f` into a run of float
  slots, **π** into three angle slots, and zeros into the rest. It calls one helper, **not named
  here**, because naming a callee of a far end is what the 2026-09-16 refinement of this page's own
  crossing rule forbids.
- The **420-byte** one is gated on kind 3, reads a float pair through the movement context's `+0x50`,
  and then configures the **movement body** behind the secondary context's `+0x138`. Its own callee
  is likewise not named.

**Neither is read further than that**, and neither is a responsibility this page shares: the
dictionary's subject is names, and `00266530` appears in it as a size discriminator. Read from the
shipping bytes 2026-09-16 (FABLE), after `OPUS` measured pass 22 RED at `HEAD` and **two of the five
findings were this page's, from a citation I added on 2026-09-16 without the sentence.**

**CoreRuntimeScheduling — CLIENT.** `FUN_0022a0b0`, owned by that layer, calls `00379D20` on this page. That caller is a startup sequence that WRITES the globals the small scheduling getters read - `[02064AA4]`, `[01E02814]` and `[01E0281C]`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Input — SERVICE.** `002D14E0` on this page calls `FUN_001e0f20`, owned by that layer. What it reaches is a 21-byte forwarder: it calls `00198790` and tail-jumps to `001986D0` with the result; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).


**Gameplay — SERVICE (SWE2-EC7-161, 2 edges).** `003BD480` — the entry store this page's
`003BD040` enumerate calls — is called by `00309EC0` on the Gameplay layer, and `00203170` is
called by `00339630`. Consultation of the store, not shared ownership.

**Presentation — CLIENT (SWE2-EC7-161, 667 edges).** The dictionary's subjects are heavily
consulted by the Presentation layer (`00181330` calls `001B03D0`; `00274CB0`/`002AFDC0`/
`002DBxxx` call it back) — the name table exists to feed presentation rows. Fan-in both
directions, no shared ownership.

**Story_Event_Quest_Hunt — SERVICE (SWE2-EC7-161, 5 edges).** `00263990`/`002639E0`/`002E16B0`
call `0032A930`/`0032ABF0` on that layer, and `003BD480` is called there too — the dictionary's
lookups service story-row text. Mechanical consultation.

**UI — CLIENT (SWE2-EC7-161, 307 edges).** `002A0440` and the UI layer call this page's subjects
(`00181330`, `00181560`, `001816B0`, `00181870`, +303 more) — the dictionary is consulted by UI,
not shared with it.


**CombatAction — SERVICE (SWE2-EC7-162, 2 edges).** `003148F0` - the vtable resolver this
page's `003BD480` calls - is called by `002F8060`/`002FA740` on the CombatAction layer.
Shared-resolver fan-in; no combat relationship to the dictionary.

**PlatformOnlineAchievements — SERVICE (SWE2-EC7-162, 1 edge).** `003148F0` is also called by
`003160C0` on that layer - the same shared resolver, reached from the achievement path.

**Save_Load_Settings — SERVICE (SWE2-EC7-162, 8 edges).** `00254380`/`00254A10`/`00264F90`/
`00282DF0` are called by `00583D60`/`005832B0` there - the dictionary's table helpers are reused
by the settings layer; mechanical fan-in.

**Script_VM_Native_Bridge — SERVICE (SWE2-EC7-162, 24 edges).** `00202E90`/`00203170`/`00264F90`
are called by `00356160`/`00357450` on that layer - script-VM bodies reach the same resolvers
the dictionary uses. Shared-helper fan-in.

**Spawn_Encounter_Lifecycle — SERVICE (SWE2-EC7-162, 1 edge).** `003148F0` is called by
`00233780` there - one more shared-resolver reach; no spawn relationship.

**CombatAI — SERVICE (SWE2-EC7-163, 2 edges).** `0046B180`/`0046B240` — the two
calibration helpers this page's `003C0A00` armed-walk runs — are also called by
`AiTargetSelector_ResolveOperandValue` (`00321190`) on the CombatAI layer.
Shared-helper fan-in; no AI relationship to the dictionary.

**Resource — SERVICE (SWE2-EC7-163, 49 edges).** The dictionary's table helpers
are consulted by the Resource loaders: `00265270` is called by `001DA220`/
`001DA970` there, and `002DF780` calls `001D6B40`/`001D6D90` (+45 more of the
same shape). Mechanical fan-in; no shared ownership.

## The `00379D20` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00379D20` (~36 B) — `003EAC40()`, `00473D20()`, tail `003EAB60`
(`00379D24`/`00379D32`).

| member | role | interior |
| --- | --- | --- |
| `00473D20` | `0051ED10(9, 0x21, 0016D6A0)` registration, result -> `02CA6C60` (`00473D24`/`00473D38`) | [`00473D24`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `003EAC40`, `003EAB60`, `0051ED10`,
`0016D6A0`.

## Interior citation — frontier hub `00282DF0` (2026-09-17, SWE2-EC7)

`00282DF0` — 19 B, 40 frontier callers at census; this page's name-table accessor. Interior
verified: [`00282DFA`](../../_index/ADDRESS-INDEX.md) is `mov rax, [rax + rdx*8 + 0xAC8]` — the
whole body loads the dictionary base `qword[0209AC30]`, sign-extends the caller's index `ecx`,
and returns `base[idx*8 + 0xAC8]`. An unbounded pointer-table getter over the dictionary's
`+0xAC8` entry array — bounds are the caller's contract, not the getter's.

NOT claimed: the `+0xAC8` row's element type (pointer or handle slot — the load returns a qword,
whose interpretation is the caller's).

## SWE2-EC7-21 update (2026-09-18) — `00550470` word-field timer decrement

`00550470` (153 B) is the `027A2F38`-singleton display-update pass the name
display bodies drive: the object's `[+0x160]` child gets `002470C0` first, then
the singleton itself twice; a `{0xF, 0, 0, 0}` stack record is vcall'd through
`[rcx]`'s `+0x00` slot; finally `word[+0x170] |= 0x80` marks the pass — the
cookie-checked update the dictionary's name objects run. Interior anchor
`00550494` (the `+0x160` child fetch). Callers `00552250`/`005528C0`/`005542D0` —
the name-dictionary display bodies.

## SWE2-EC7-45 update (2026-09-19) - `005210F0`

`005210F0` (250 B) is a body - `00540FC0` single call. Interior anchor `005211C3` (the `00540FC0` call).

## SWE2-EC7-72 update (2026-09-19) - `005044B0` + `00504450` record/packet helpers measured

`005044B0` (22 B) is the `02EBEFC0` record getter: `02EBEFC0 +
[02EBEFF0] * 24` - the current row of the name table.
Interior anchor `005044BA` (the `02EBEFC0` lea).

`00504450` (53 B) is the packet push the draw-list family shares: writes
`0x10000000` at the `[rcx]->+8` cursor plus two zero dwords, advances
the cursor `0x10`, runs `0016D6A0(0)`, and tail-jumps `003A1DB0` - the
same tag-word scheme `00271080` stamps.
Interior anchor `00504477` (the `0016D6A0` call).

## SWE2-EC7-82 update (2026-09-20) - `005212E0` + `00521320` name-table access measured

`005212E0` (31 B) is the id lookup every dictionary caller runs:
`cx` indexes `02CA8450` at a 48-byte stride (`x*3 << 4`), and the
record is returned only when `word[rec]` matches `cx` - else 0.
Interior anchor `005212F7` (the `cmp word[rdx], cx` verify).

`00521320` (133 B) is the full-table reset on the same `02CA8450`
array: 64 iterations of 0xC0 stride, and inside each chunk the four
0x30 records' flag words at `+0x1C`/`+0x4C`/`+0x7C`/`+0xAC` lose bit0
(`& 0xFFFE`) while `+0x14`/`+0x44`/`+0x74`/`+0xA4` zero - all 256
records' live flags and payloads dropped.
Interior anchor `00521337` (the `+0x1C` flag clear).

## SWE2-EC7-103 update (2026-09-20) - `002747B0` measured

`002747B0` (137 B) is the `0xD8`-keyed lookup pair
`002B7590`, `002BA700`, `003CB650` and `00552250`
call: a nonnull `rcx` runs `00245000` with the
`00275F10` formatter and a stack out-record; a
null `rcx` instead runs `00244F50` with the same
`0xD8` size and `00275F10` target - the
present-versus-fetch split the name-dictionary
arms share.
Interior anchor `002747FA` (the `00245000`
call).

`00563110` (402 B) is the name-dictionary binder the world-map widget (`00552250`) runs: `00274780([+0x10], 0)` and `00274780([+0x10], 1)` fill `[rsi]`/`[rsi+8]` — the two entry lists; per entry `00555A50(list, i)` yields the name string, the `00D23270`..`00D232D0` `{name, key}` table (stride 0x10) is byte-compared, and a hit `0024A5A0(row+8)`-resolves the object pointer back into `[rbx]` — the string cell's object back-fill. Then `0024A5A0("w_line01")` lands in `+0x78`, `+0x94` = 0, and `+0x8C`/`+0x90` = 1.0f.

Interior anchor `005631C5` (function `00563110`).

`00563080` (143 B) is the teardown `00552250` runs on the same widget: `[+0x10]` `003697F0`-releases and nulls; the `+0x20`-based slot array frees indices 0-9 through `0024A680(obj, 1)` and nulls all eleven (`+0x20`..`+0x68`); then `+0x18`..`+0x68` (eleven qwords) `003697F0`-release and null — the object-table teardown.

Interior anchor `005630C3` (function `00563080`).

`00562F40` (66 B) is the `00555400` forwarder `005528C0` runs: `00555400([+0x20], [+0x8], edx, r8d, r9d, {three stack-arg words})` — a pure shim passing its own arguments plus the three stack words into the list helper.

Interior anchor `00562F78` (function `00562F40`).

`00562920` (262 B) is the nine-slot bit-0 clear `005528C0`/`00553DD0` run: each of `[+0x80]+0x60`'s `+0`..`+0x40` entries gets `+8` &= ~1 — a null `[+0x80]` writes to the null base, the same guard-through-null pattern the paired record writes use.

Interior anchor `00562A14` (function `00562920`).

`00562120` (108 B) is the vector-copy setup `005528C0` runs: `00202C90(this+0x20, r8)` and `00202C90(this+0x30, r8)` copy the arg vector twice, `00202C90(this, rdx)` copies the other, then tail `00275490(this+0x10, this, this+0x20, 0.5f)` — the half-lerp toward the arg vectors.

Interior anchor `00562160` (function `00562120`).

`005620A0` (127 B) is the triple-lerp `005528C0` runs: `00275490(this+0x20, this+0x20, this+0x30, 0.5f)`, then `&stack` = `00275490(this, this+0x20, 0.5f)`, then `00275490(this+0x10, this+0x10, &stack, 0x3EC3EF15)` — three blend passes at 0.5f / 0.5f / `0x3EC3EF15`.

Interior anchor `00562102` (function `005620A0`).

`00555400` (667 B) is the sprite-quad packet emitter `00562F40`/`0055A8A0` forward into (the `005528C0` map-page draw): `[rsi+0x90..0x93]` RGBA is faded by `word[+0x5A]` >> 7 and `word[+0x58]` >> 7 into a local colour (`+0x94` stamped back), `00271450`/`002714A0`/`00271480`/`002714C0` open and parameterize the packet, `00181560` flushes, and per `[r14+0x20]`-header entry `001819A0` resolves `{w@+0x14, h@+0x16}` while `002710C0`/`00271050`/`002714E0`/`00271100`/`00271080`/`00271010` pack vertex + texcoord pairs — closing on the `00555F80`/`00555D10` pair for the batched quads and the name list.

Interior anchor `005554CD` (function `00555400`).

`00554EA0` (846 B) is the same-position marker-layer draw `005528C0` runs beside `00555400`: walks `rdx`'s `+0x150`-chained record list (`+0x158`/`+0x160` bounds), computes `(word[rbx+0x138] >> 7) · ecx >> 7` as the per-marker fade written back to `word[+0x58]`, and per live marker calls `0029CD00`, `002718C0`, `002D8650` twice and `00254A10` — the second draw pass the map's destination/landmark pins ride on, at fixed-point 7-bit alpha.

Interior anchor `00554F6E` (function `00554EA0`).

`00555F80` (700 B) is the packetized quad draw `00555400` runs last: `xmm2 = K − 01E0C1D8·0.5 − x` and `xmm1 = K' − 01E0C1DC·0.5 − y` centre the arg position on the screen, `01F2CAC0`/`01F2CAC4` supply the quad extent floats, two `00203170` calls transform the vector at `[rcx]`/`[rcx+0x10]` (`00203170` is shared transform machinery — it is also driven by gameplay-side callers outside this page's scope), then per-entry `00202E90`/`00202D70`/`002030E0`/`00202C70` packet writes run under saved `xmm6`-`xmm11` — the viewer-rect draw `005528C0`'s render arm calls through `00555400`.

Interior anchor `0055602F` (function `00555F80`).

`00555D10` (619 B) is the name-list draw `00555400` runs: over `[r15+0x14]` entries at `r14 = rcx + [rcx] + [rdx+0x10]·2` (16-bit name records), each entry whose `word[0]` bit 0xF is clear is `00556240(&stack, 0, rbp, r12b)`-resolved then `00555B90`-drawn with `00271290`/`00202B70`/`00181350`/`00181330` — the destination-name label pass with `r9`'s `+0x14`/`+0x16` header supplying the base offset pair.

Interior anchor `00555D92` (function `00555D10`).

`005551F0` (165 B) is the line-emit wrapper `005528C0` runs after `005520F0`: the eased float `(word[+0x5A] · 0x8C >> 7)` fills a four-float local and `word[+0x58]` a fifth, then the `+0x1A0`-linked list from `rdi` is walked `00562A30(node+0x20, &floats, [node+0x1A0])` per node — one scaled-thickness line emit per chain member.

Interior anchor `00555260` (function `005551F0`).

`00555A50` (18 B) is the `0x20`-stride row indexer `00563110` calls per name entry: returns `rcx + [rcx+0x10] + rdx·0x20` — the name-record table's element address.

Interior anchor `00555A5B` (function `00555A50`).

`00550A00` (462 B) is the destination-label record build `005523BF`'s build arm runs: `003BD1B0(&buf, word[+0x172] | -1)` fills the string buffer, then per count the `[rsi+0x160]+0x170`-chained record takes a 0x38-byte copy (`movups` twice + `movsd`) of the fetched row, `0057E2F0` resolves it, and `word[+0x3C]`/`word[+0x3E]` are offset by `01F2CAAC`/`01F2CAB0` (WorldMapCursorOffsetX/Y) — the name-label layout pass.

Interior anchor `00550A9D` (function `00550A00`).

`00550820` (468 B) is the sibling propagation pass `005523BF` runs beside `00550A00`: over `rdi`'s `+0x140` chain, `003BFFF0(&stack, word[+0x172], byte[+0x39])` counts each node's links, then per index `[rbp+0x160]+0x118`'s `+0x140` chain is walked for the `+0x39`-matching record and `00550690` runs — parent-to-child record copy across the destination graph.

Interior anchor `00550873` (function `00550820`).

`00551130` (190 B) is the destination-entry locator the populate arm runs twice: `[rcx]`/`[rdx]` are zeroed, then `r8`'s `+0x140` chain is walked — `r9d` == 0 finds the first node with `+0x54` bit 0 clear, else the first whose `byte[+0x39]` matches the arg word — returning its `{+0x3C, +0x3E}` centre pair into the out slots.

Interior anchor `00551170` (function `00551130`).

`00551230` (117 B) is the mode query every `005528C0` arm runs first (`00551930`/`00551B30`/`005542D0` share): `{&out, 0x23, &out2, 0}` is built on the stack and `02CA8F38`'s vtable head is called — message 0x23 to the world-map widget returns the mode dword, 0 when the widget or its vtable is null.

Interior anchor `00551279` (function `00551230`).

`005512B0` (858 B) is the three-colour populate helper `005528C0`'s render arm runs twice: `word[+0x5A]` is eased `(·0x5A >> 7) · K` (`008C5B34`) into three `{qword, dword, float}` entries; in the `r8d` arm each entry's colour comes from `002DD7E0` on `0xB2`/`0xB3`/`0xB4`, the float pairs scaled per channel — the RGBA mix table the name and marker draws read.

Interior anchor `0055137A` (function `005512B0`).

`00551CD0` (162 B) is the relabel-rect compute `00553A1A` runs on the `+0x160` child: mode 1 centres a `0x40 x 0x40` box at `(01E0C1D8/4 - 0x20, 01E0C1DC/2 - 0x20)`; mode 0 picks a randomized rect — `x = 002C9430(0xA0-0x20) + 0x20`, `w = 01E0C1D8 - 0x140` — the box the relabel draws into.

Interior anchor `00551CF5` (function `00551CD0`).

`005520F0` (320 B) is the packetized record emit `005528C0`, `005512B0` and `005551F0` share: `00271450`/`002714A0`/`00271480`/`002714C0` open and parameterize the packet, four records push — `[rbx+0x78]+0x30`'s qword under tag 6, `0x60` under 0x14, `5` under 8, `0x3001` under 0x47 — `002710C0`/`00271050`/`00271080`/`00270FF0` run the stages, and the emit closes on `[rbx+0x78]+0x20`'s `{w@+0x14, h@+0x16}` header for `001819A0`.

Interior anchor `005521CB` (function `005520F0`).

`00553BB0` (251 B) is the scatter-rect compute `005528C0`'s render arm runs: a `{x, y, w, h}` word block centred on `01E0C1D8`/`01E0C1DC` — `w`/`h` fixed at 0x6A, `x`/`y` seeded at half the screen dims plus `002C9430(0x80)`-randomized offsets (+0x14) — the label/twinkle jitter rect the map surface draw consumes.

Interior anchor `00553C13` (function `00553BB0`).

`00553CB0` (287 B) is the edge-flag refresh the open-transition arm runs beside `00554A60`: two `002C9430(0x80)` rows seed the pair, then `word[+0x100]`/`+0x102` are tested against `01E0C1D8`-derived extents under `01F2CAA4` (the world-map width) — `edx` bit 2 or'd when `+0x100 > 0`, folded back when `+0x102` passes the bound — the scroll-limit state the pad arm reads.

Interior anchor `00553D1B` (function `00553CB0`).

`00553DD0` (353 B) is the destination-list rebuild `005528C0`'s populate arm calls: `00562080` runs per `0x30`-stride record under `+0x9F58`, copying `[this+0x108]+0x48`'s `+0x20`-chained rows — each `{w@+0x14, idx-list +0x16, off +0x10}` header expands into `{w0, w2, w4 & 0xFFF, (w4 >> 0xC) & 0xFFF}` quads written `+0xD0..+0xD6` per slot.

Interior anchor `00553E29` (function `00553DD0`).

`00554A60` (360 B) is the marker-angle stepper the open-transition arm runs on `+0x118`: per record flagged `+0x130` bit 0, bit 1 plus a `00254A10` test pick the `{0x3CCC, 0x2CCC}` or `{0x2666, 0x3666}` target pair, and `word[+0x138]` is eased toward it in +/-0x400 wrap steps (`r14d` = -0x400) — the pin-rotation tick the transition drives.

Interior anchor `00554ADD` (function `00554A60`).

`00554BD0` (718 B) is the entry-marker arm `005528C0`'s render pass runs on `+0x58`/`+0x5A`: a null `rdx` returns early, else the `[r8+0x80]+0x60`-chained subobjects at `+0x10`, `+0x28` and onward each take `+8 |= 1` — arming the marker's child widgets before the position pair is staged for the draw.

Interior anchor `00554C3B` (function `00554BD0`).

`00555B90` (370 B) is the per-entry sprite record `00555D10`'s name-list loop calls: `rdx`'s index or'd into `0x3000000000008000` under tag 0x412 heads the record; when `r9d` is live the `[r8]+0x18..+0x1E` words scaled by `[r9]+0x94..+0x97` bytes `>> 7` become the `+0x10..+0x1C` float quad — the coloured name-sprite packet.

Interior anchor `00555BB7` (function `00555B90`).

`00556240` (312 B) is the positioned sprite packet `00555D10` runs per name record: `00271450`/`002714A0` open, `00271480`/`002714C0` parameterize when `ebx` is live, then records `[rsi+0x80]` under tag 0x47, `[rsi+0x78]` under 0x42 and `1` under 0x1A push, `01F2CAC8` bit 0 selecting `0xA` versus `ebp ? 0x5C : 0x4C` for the last; `002710C0`/`00271050` close and `00181330`, `00181910([rsi+0x80])`, `001816B0([rsi+0x78])`, `4` emit — one name sprite per call.

Interior anchor `005562DB` (function `00556240`).

`00562A30` (1019 B) is the `w_line01` line draw `005551F0` runs per `+0x1A0` node: `00563360` then the `00271450`/`002714A0`/`002714E0` packet prologue, `00181560` flush, `00181910(0x3001)`, `001816B0(0x44)`, `00181870(4)`, `00181890(1, 1, 0, 0)`, and `001819A0` on `w_line01` (`009159E8`) whose `01F2CAF8`/`01F2CAFC` dims are scaled by the `02CA96C0`/`02CA96C4`/`02CA96CC` floats — one scaled-thickness line emit per chain node.

Interior anchor `00562AD8` (function `00562A30`).

`0057E2F0` (30 B) is the 0x38-byte record init `00550A00` runs per label entry — seven qwords zeroed, the blank the fetched row is then copied over.

Interior anchor `0057E305` (function `0057E2F0`).

`0057E070` (22 B) is the 0x28-byte sibling init `00550820` runs — five qwords zeroed, the smaller record form.

Interior anchor `0057E07D` (function `0057E070`).

`0057E030` (53 B) is the tail-append `00550820` runs: `rcx+8` heads a `+0x10`-next list; `rdx` links after the walked tail with `rdx+8` = the old tail — the child-link list build.

Interior anchor `0057E05C` (function `0057E030`).

`00550690` (388 B) is the link propagate `00550820` calls per `+0x39` match: `[rcx+0x160]+0x128`'s `+0x1A8` chain is walked for a `{+0, +8}` pair equal to `{rdi, rbx}` in either order — the dedup — and on a miss `003C00C0(&stack, word[+0x172], byte[rdi+0x39])` counts the links the loop then files. The parent-to-child edge copy.

Interior anchor `00550705` (function `00550690`).

`00550FB0` (373 B) is the vertex table `00550820` builds on the marker record: three `{word[+0x14+i*4], word[+0x16+i*4]}` pairs become `{x, 0, y, 1.0f}` floats in a `0x10`-stride local block and `+0x1A0` is set to 0x10; when `word[+0x18]`/`+0x1A` are both zero the `00900358` constants fill instead — the marker's corner quad.

Interior anchor `00550FF0` (function `00550FB0`).

`00550BD0` (985 B) is the marker blink compute `00554BD0` calls per entry: `+0x130` bit 2, `+0x54` bit 0x10000 and `+0x130` bit 3 select between `word[+0x5A] = 0x40` fixed and a `0208F570`-tick phase run through `00861F0E` scaled by `0x42800000` — the fade value the marker draw reads.

Interior anchor `00550C03` (function `00550BD0`).

`005552A0` (134 B) is the scroll clamp `00551130` calls on its out pair: `[rcx]` folds to `[0, 01F2CAA4 - 01E0C1D8]` (map width minus screen) and `[rdx]` to `[-002C9430(0), 01F2CAA8 - 01E0C1DC + 002C9430(1)]` — the clamped scroll position with randomized edge slack.

Interior anchor `005552D3` (function `005552A0`).

`00563360` (193 B) is the packet prologue `00562A30` and `005621A0` open with: `00271450`/`002714A0`/`00271480`/`002714C0` initialize the packet, then records `{0x5C under tag 0, 0x44 under 0x42, 1 under 0x1A}` push before `002710C0`/`00271050` — the standard line/list preamble.

Interior anchor `005633BD` (function `00563360`).

`00562E30` (254 B) is the emit wrapper `005520F0` calls: the `00271450`/`002714A0`/`002714E0` prologue, `00563430(r14, ebp, esi, rdi)` runs the draw, `{rsp+0xA0, +0xA8}` publish into `01F2CAF8`/`01F2CAFC` — the dims `00562A30` reads when scaling `w_line01` — then `00271100` and the `0xA0000007`-derived record at `+0x80`.

Interior anchor `00562E9A` (function `00562E30`).

`005621A0` (1711 B) is the batched record fill `005512B0` calls: `00563360`'s prologue, `00270420` measures `r12`, and a four-wide unrolled loop writes the per-entry records — the populate loop's heavy emitter.

Interior anchor `00562212` (function `005621A0`).

`00562080` (31 B) is the per-slot record reset `00553DD0` calls while rebuilding: `+0x28` = 0, `word[+0x26]` = 0x10, `+0x1C` = 0x808080, `+0x20` = 0x80808080 — the destination slot's defaults.

Interior anchor `0056208C` (function `00562080`).

`00561F90` (227 B) is the colour lerp `00553BB0` calls: per channel `(dst - src) * word[+0x24] >> 8 + src` over the `{+0x1C -> +0x90, +0x1D -> +0x91, +0x1E -> +0x92}` pairs against `{+0x20, +0x21, +0x22}` sources, with `byte[+0x5C]` = `rdx+0xC` — the fade step writing the RGB mix.

Interior anchor `00561FC9` (function `00561F90`).

`00561F60` (43 B) is the fade tick `00553CB0` calls: `+0x28` bit 0 selects `word[+0x24] += word[+0x26]` clamped at 0x100 or `-=` clamped at 0 — the lerp position advancing or retreating per slot.

Interior anchor `00561F6A` (function `00561F60`).

`00563430` (227 B) is the draw-parameter publish `00562E30` calls as `00563430(r14, ebp, esi, rdi)`: two `00203170` transforms (`rcx`, then `02CA9680`), `02CA9680`/`02CA9694` set to `1.0f`, the origin `00900384` minus half the `01E0C1D8`/`01E0C1DC` screen dims minus the `r8`/`r9` offsets into `02CA96B0`/`02CA96B4`, and the stack-arg record's four floats copied to `02CA96C0`/`C4`/`C8`/`CC` — the scale-and-position block `00562A30` reads when drawing `w_line01`.

Interior anchor `0056344C` (function `00563430`).

`00562190` (14 B) is the arg-swap thunk `00550BD0` tail-calls: `rcx`/`rdx` exchange and `jmp 00562850` — the marker blink's hand-off into the tagged-entry dispatch loop.

Interior anchor `00562199` (function `00562190`).

`00562850` (205 B) is the tagged-entry dispatch `00562190`'s arg-swap lands in: `00202C70` and `00203170` init the `+0x60`/`+0x20` locals, `[rsi+0x80]+0x58`'s half-width and half-height subtract from `r9d`/`r8d` into centered float origins, `00202D70` runs, then `002435C0([rsi+0x80]+0x50, rdx)` walks the tagged list before a second `00202C70` closes - the name/draw entry loop behind the map screen's text.

Interior anchor `005628E8` (function `00562850`).

`00540FC0` (7 B) is the field clear `005210F0` calls: `word[rcx+0x24] = 0` and return - the single-field reset in the `02CA8450` handle-table allocator.

Interior anchor `00540FC2` (function `00540FC0`).

`0053D4B0` (705 B) is the tagged-record emitter `0053AB50` runs: `[rax+8]+0x40` against `[rdx]`'s capacity triggers `00504450`/`005044B0` grow-and-repoint (`[rbx]` to the new block, `[rdi]` to `[rax]+count*0x10`), then `0x10000002`/`0x01000404`-family tags stamp into `[rax+8]` records with `003E56A0` - the growable tagged stream behind `0053AB50`'s record writes.

Interior anchor `0053D5DE` (function `0053D4B0`).

`0053D140` (876 B) is the sibling emitter `0053AB50` runs: `[rax+8]+0xA0` capacity check, the same `00504450`/`005044B0` grow-and-repoint into `[rbx]`/`[r14]`, then `0x10000008`-family tags stamp the records - the second tagged-record arm.

Interior anchor `0053D177` (function `0053D140`).

`003BD1B0` (718 B) is the string-buffer fill `00550A00` names directly: `003C08B0`, `003C0C50`, `003BD040`, `003BC260`, `00473BB0`, `003BFB60`, `003BFC70` and `00473CC0` build the label text under the cookie check - the destination label's name writer.

Interior anchor `003BD288` (function `003BD1B0`).

`003CD2C0` (688 B) is the element-kind dispatcher `0053AB50` calls: `cl<<6` record on `02B47790` (`+4` key check, `00181DD0` gate, `+0x38` presence), `byte[+1]&0x3F` picks direct `+8` or `0036B130`-resolved, `word[+2]` count into `003CD840` on `02B4A7A0`, then per `+0x28` element the `word[+0xA]`/`+0x34`/`+0x36` wrap math and `byte-1<=7` jump table to the eight `0050xxxx` handlers, tail `003D2B60` - the dictionary's kind-dispatch stage.

Interior anchor `003CD2DD` (function `003CD2C0`).

`0041B650` (706 B) is the value emitter the per-bone binder `0041B550` calls (an uncited sibling drives it too): `dword[rdx+0x34]==1` selects the `00409170` path else `00409150`, then `0041B3A0` x2, `0041B920`, `0041BB00`, `0041B460`, `0041BA10`, `0041BC40` fill the `rdi` output record's `+0x10`/`+0x16`/`+0x8`/`+0x6`/`+0x19` fields - the binding's two-shape converter.

Interior anchor `0041B67F` (function `0041B650`).

`003BFC70` (370 B) is the name setter `003BD1B0` calls: `movsx word[rcx + 4]`/`[+6]` are the record coords, `dl << 4` scales `r14d`, `00202C90` copies the name into the stack frame and `003BD6F0` commits - the dictionary's entry write.

Interior anchor `003BFD01` (function `003BFC70`).

`003BD040` (364 B) is the table iterator `003BD1B0`/`003BFB60`/`00551F00` call: `[02B457E0 + 0xD8]`'s `word[+0xA]` count plus its base bounds the walk over `cx` entries, `002543D0`/`002543A0` resolve each, `002F9860` fetches the string and `003BD480` stores - the dictionary's enumerate-and-fill.

Interior anchor `003BD0B9` (function `003BD040`).

`003BD480` (618 B) is the entry store `003BD040` calls: `cx` is the index, `003148F0` -> `00264F90` -> `00254380` resolves the table and count, `r13w == ax` `cmove`s the found flag; the `[02B457E0 + 0xE8]` + `word[+8]` walk matches `00254380(i)` against the index then stores through `003C08B0`/`003C0A00`/`003C1680` - the dictionary's index-keyed write.

Interior anchor `003BD4AA` (function `003BD480`).

`003C08B0` (333 B) is the record fetch `003BD480`/`003BCCA0`/`003BFFF0`/`003C00C0`/`003C0180`/`003BD1B0` call: `cx` index into `[02B457E0 + 0xD8]` + `word[+0xA]` table at `0x1C` stride; `bx == 0`, empty table, `edi >= dword[rdx]`, or `byte[rsi + 0xA] == 0` all bail; `word[rsi + 8] == 0xFFFF` then runs the `00254380`/`00264F90`/`00265270`/`003148F0` resolve - the dictionary's bounds-checked entry read.

Interior anchor `003C0922` (function `003C08B0`).

`003C0A00` (362 B) is the gated enumerate `003BD480`/`003C08B0` call: `dword[02B457E0 + 0xD0]` needs both bit 8 and bit 9 set before `003BC260`; then the `00254380`/`00264F90`/`00315DC0`/`00380170`/`0046B180`/`0046B240`/`00473BB0` chain iterates `cx` - the dictionary's armed-table walk.

Interior anchor `003C0A4A` (function `003C0A00`).

`00382BF0` (285 B) is the `02AEDFA0`-gated position publisher `0053AB50` calls: `dword[02AEDFA0] != ecx` exits; `word[02AEDFA0]` resolves `sx x 0x740 + 022C6F28` (a `-1`, a null base, or `dword[+0x284] == 0` fails into `00182870(0, -1.0f, 0)` and stores `02AEDFA0 = -1`); live records run `00421E20(word[02AEDFA4], 0, &vec)` for the position, `00202B70` transforms it through `02CA7F80`, and `00182870(2, dword[02AEDFA8] - out.y, 0)` publishes the height delta - the tagged emitter's channel-2 leg with its invalidation path.

Interior anchor `00382CA2` (function `00382BF0`).

`00382BF0` (285 B) is the `02AEDFA0`-gated position publisher `0053AB50` calls: `dword[02AEDFA0] != ecx` exits; `word[02AEDFA0]` resolves `sx x 0x740 + 022C6F28` (a `-1`, a null base, or `dword[+0x284] == 0` fails into `00182870(0, -1.0f, 0)` and stores `02AEDFA0 = -1`); live records run `00421E20(word[02AEDFA4], 0, &vec)` for the position, `00202B70` transforms it through `02CA7F80`, and `00182870(2, dword[02AEDFA8] - out.y, 0)` publishes the height delta - the tagged emitter's channel-2 leg with its invalidation path.

Interior anchor `00382CA2` (function `00382BF0`).

`003BF7C0` (274 B) is the mode-gated index scan the world-map arms `00551800`/`00551930`/`00551B30`/`005528C0` run: `r13b` parks at `byte[02B457E0 + 0xCA]`; for `esi < 0x3B` while `00254380(esi)` keeps matching `bx`, `[02B457E0 + 0xE8] + word[+8]` supplies the counted table and a nonzero `byte[+0xCA]` re-verifies `esi` through `003148F0`/`00264F90`; 8-stride entries whose `byte == esi` run `003C12B0(index)` and the first nonzero hit stops the scan, else `003BF6C0(r12 + r15 x 24, si)` fills the caller's slot; `r13 == 6` with `003C0E30(esi)` true `OR`s `0x20` into the slot head - the dictionary's per-index match-and-mark.

Interior anchor `003BF859` (function `003BF7C0`).

`003BFB60` (262 B) is the code-chain walker `003BD1B0` runs per byte lane `r14`: reading `byte[r14 + rbp + 8]`, a `0xFF` terminator returns `0xFF` (with `*out = 1` when the optional pointer is live), a byte equal to `[rbp+1]` stops the chain, and each other byte first scans `edi` entries of `r15` (`x 0x28` stride, tag at `+1`) returning the hit index; misses go through `003BD040(rbp, dl, &map)` for the table byte at `[rsp + r14 + 0x28]`, which is appended to the dedup list at `rsp+0x48` only if not already present - the chain decode the name-table reader composes.

Interior anchor `003BFBFB` (function `003BFB60`).

`00271050` (44 B) is the packet-closing stage `00555400`/`005520F0`/`00556240`/`00563360` share: writes the 16-byte command quad into `rdx = [rcx+0x30]` - `+0 = 0`, `+4 = 0x13000000`, `+8 = 0x10000000`, `+0xC = (([rcx+0x10] - rdx - 0x10) >> 4) | 0x50000000` - the fence record the sprite emitters append after their vertex/texcoord pairs.

Interior anchor `0027106D` (function `00271050`).

`00270420` (209 B) is the vec3 magnitude writer `005621A0` runs: for `r8d - 1` entries at `rdx+0x10` (stride `0x10`) it `00203080`s each vector, squares and sums the components, `cvtps2pd` + `00861F5C` (sqrt) yields the length, stored as float at `rdi + i*4` - the per-entry distance array

Interior anchor `0027046C` (function `00270420`).

`003C0180` (207 B) is the keyed sub-table scan `005528C0` runs: `r10 = [02B457E0 +0xD8] + word[+0xC]` reaches a packed `{u32 count, 8-byte entries}` block, the caller's mode byte is stored to `+0xCA`, and each entry whose `+2` key byte equals `dx` is `003C08B0`-filtered (zero aborts the whole scan) then `003BCCA0`-emitted into the caller's 16-byte-stride array - returns the accepted count

Interior anchor `003C01E1` (function `003C0180`).

`003C0E30` (207 B) is the membership scan `003BF7C0` runs: `02B457E0`'s `+0xD0` bits 8 set / 9 clear gate the body, `003BC260` resolves the working record, then a `+0xCB`-counted loop `00473BB0`s each slot and any `+0x20 == 1` result is `00264F90`-checked against `edi` - the same 'find entry matching this id' shape as `003C15B0`, with `00264F90` as its comparator

Interior anchor `003C0EA0` (function `003C0E30`).

`003BCCA0` (308 B) is the keyed row resolver `003C0180` and `003BFFF0` run per entry: the `[02B457E0]+0xD8` table plus its `+0xA` word gives a `{u32 count, 0x1C-stride rows}` block, the caller's key `cx` is bounds-checked against `[table]` and selects `key*0x1C + 4`; the `[rdi]`/`[rdi+1]` prefix chooses the mode byte fed to `003C08B0`, and on acceptance with `r15` live the row's data is emitted into the caller's result

Interior anchor `003BCD2F` (function `003BCCA0`).

`003BFFF0` (202 B) is the collect-all wrapper over `003BCCA0`: it stores the caller's mode byte to `[02B457E0]+0xCA`, walks the `+0xC`-offset sub-table's `[count]` 8-byte entries skipping `+2 != 0` rows, runs `003BCCA0` with key `dx` on each, and writes every accepted u16 into the `r15` out array - returns the accepted count

Interior anchor `003C0072` (function `003BFFF0`).

`003C0D70` (187 B) is the admission test `003C08B0` runs per dictionary candidate: `ecx >= 0x3B` refuses outright, a clear `[rax+0xCA]` byte accepts unconditionally, and otherwise `003148F0` -> `00264F90` must return `ebp`; when `edx != 0` the candidate must additionally match an entry in the `[rsi]`-counted 8-byte list hanging off `[02B457E0 + 0xE8] + [+8]` - one whose first byte equals `ebp` and which `003C12B0` accepts

Interior anchor `003C0DB0` (function `003C0D70`).

`003C00C0` (183 B) is the keyed sub-table emit `00550690` runs per accepted candidate: `r8b` is stored into the `[02B457E0 + 0xCA]` flag byte, `[02B457E0 + 0xD8]`'s `+0xC` word offset locates the counted entry list `r14`, `003C08B0(r15w)` gates admission, then every `[r14]`-counted 8-byte entry with `byte[+2] == 0` invokes `003BCCA0` - handed the key, the entry, and `rbp + edi*0x10` (or null) as the out-row - returning the emit count `edi`

Interior anchor `003C0120` (function `003C00C0`).

`003BCAF0` (174 B) is the keyed bitmask emit `00552250` runs on the `02B457E0` dictionary record: gated by `ecx != 0`, `byte[rax+0xC8] == 1` and a live `[rax+0xD8]` sub-table (`+0xC` word giving its end), it stamps `bl` into `[rax+0xC9]` and walks the 8-byte entries - each whose `+2` byte equals `bl` sets `1 << (id & 0x1F)` in the `[rax+0x270 + (id>>5)*4]` bitmask for both its `+0` and `+1` id bytes

Interior anchor `003BCB63` (function `003BCAF0`).

`00181F20` (161 B) is the `r8d = 0` sibling of the named float-pair registration `0053AB50` runs: `001E9F40` builds the `0x110` scratch string object, the `rbx` float pair copies to `+0x20` with the `rdx` name appended by the byte loop, `001C2F40` resolves the registrar and `001C2980(reg, &pair, 0)` files it, `001EA180` tears down

Interior anchor `00181F8E` (function `00181F20`).

`00290230` (19 B) is the one-byte state setter this family's shared callers stamp: when manager `0209BE80` is live, `cl` lands at its `+0x10FA3` byte and the body returns - the shared flag write `002B7590`, `002BA700` and `003CB650` reach from three different subsystems.

Interior anchor `0029023C` (function `00290230`).

`004041D0` (83 B) is the four-slot teardown the same shared callers (`002BA700`, `003CB650`) run on their record pairs: `0024A680(?, 1)` releases the pointers at `+0x00`, `+0x08` and `+0x10` in turn, while a live `+0x18` pointer goes through `003697F0` and the slot is then zeroed - the symmetric cleanup for the records this family builds.

Interior anchor `004041F4` (function `004041D0`).

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-the-npc-name-dictionary-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `001DA220` | 102 B | does nothing unless `001D6B20(rcx)` returns non-zero, `001D6B90()` returns zero and `00265270()` returns zero in `ax`; then stores word 0 at `rcx+0xE8` and calls `005CD4F0(rcx+0xF0)`, `001D9930(rcx)`, `005CD820(rcx+0xF0)` and `001D9EC0(rcx)` | `001DA229`, `001DA232`, `001DA23B`, `001DA253`, `001DA276` |
| `001DA970` | 100 B | does nothing unless `001D6B20(rcx)` returns non-zero and `00265270()` returns an `ax` that is above zero (signed) and differs from word `rcx+0xE8`; then stores that `ax` at `rcx+0xE8` and calls `005CD4F0(rcx+0xF0)`, `001D9930(rcx)`, `005CD820(rcx+0xF0)` and `001D9EC0(rcx)` | `001DA982`, `001DA98A`, `001DA98C`, `001DA9A1`, `001DA9C4` |
| `00275F10` | 231 B | switches on dword `[rdx]`: id 1 copies qword `[[rdx+8]]` to `rcx+0xC0` and dwords `[[rdx+8]+8]` and `[[rdx+8]+0xC]` to `+0xC8` and `+0xCC`; id `0x10` calls `00244F00(rcx)` when qword `[rdx+8]` equals the sign-extended dword `+0xCC`; id `0x12` calls the function pointer at qword `[[rcx+0xC0]]`, when both qwords are non-null, with `rcx` = qword `+0xC0` and a stack record holding dword `+0xC8` at its `+0` and 16 zero bytes at its `+8` (`+4` is not written); these three return 0, and any other id returns `005C5230(rcx, rdx)` | `00275F31`, `00275F3E`, `00275F82`, `00275FA8`, `00275FC8` |
| `00521290` | 70 B | scans the `0x100` entries of `0x30` bytes starting at the pointer in qword `02CA8450`, skipping entries whose first word is `0xFFFF`, and returns the address of the first entry whose dword `+4` equals `ecx`, or 0 when none does | `005212A6`, `005212AC`, `005212B7`, `005212C4`, `005212CE` |
