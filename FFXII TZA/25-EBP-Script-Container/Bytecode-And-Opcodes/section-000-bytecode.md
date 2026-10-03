---
system: EBP section_000 — the script image (header, tables, name pool and bytecode)
category: 25-EBP-Script-Container
status: AUDITED
owner_layer: CodeDomain — loader owned by PrimaryOwner:ActorEntity; execution by Script_VM_Native_Bridge
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
corpus_validated: "1114 / 1114 EBP2 containers (of 1115 us .ebp files), 2026-09-03"
last_reviewed: 2026-09-11
ebp_units:
  - "section_000"
archive_formats:
  - "scriptimage | explained | the four ATEL control scripts ctrl/btlctrl/evctrl/mapctrl.bin in ch/in (.bin member; leading 0x8000000B, +0x04 = file size): a bare section_000 script image - header section 2, parsed by ActorManager_BindLoadedDefinitionPayload 0026C8C0, section 3; no PC path names the four files (unnamed-bin-families.md)"
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: GN160-repos-1e-falsification-1
  crossref_clean: true
  crossref_checked: null
  crossref_report: null
  reopened_count: 0
---

# EBP `section_000` — the script image

> **This is the script.** Slot 0 of every container holds the compiled behaviour of a map or
> cutscene: a fixed 0x90-byte header, a set of authored tables, a pool of names, and the bytecode
> the [interpreter](../../01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md)
> executes one opcode at a time.

**Corpus validation, before anything else.**

| | |
|---|---|
| files examined | **1,115 of 1,115** `us` `.ebp` files |
| this unit present in | **1,114 of 1,114 containers** — every container has one |
| the missing file | `us/event/evt_t/evt_t0020/evt_t0020.ebp` is **not a container at all** (§5) |
| co-occurrence | occurs with every other section type; never absent from a container |
| size range | `+0x04` reports 0x1E0 – 0xFB4C0 bytes; header is **always exactly 0x90** |

---

## 1. What the player sees

**Almost everything in the game that is not a number in a battle formula.**

A soldier in Rabanastre who turns to watch you pass. A treasure chest that gives a Potion the first
time and nothing after. The gate that will not open until you have talked to the right person. The
sandstorm that rolls into the Westersand. A cutscene: the camera swings, a character walks to a
mark, a line plays, everyone waits, the camera cuts. **Every one of those is compiled into
`section_000` of one `.ebp` file**, and the engine runs it instruction by instruction.

Two things in this section are unusually human. Each script carries **the name of the Square Enix
developer who wrote it** and **the filename of the `.src` source it was compiled from** — the file
`alc_a0100.ebp` records that it was built from `alc_a0100.src` by `mtaniguc`. And the script's
handlers are named the way the authors named them: `init`, `main`, and — in Japanese — `カット１`,
`カット２`, "Cut 1", "Cut 2", the cutscene takes.

The other thing a modder will want is the **`option` block**: the authored knobs sitting in the
header, including the one the glossary already knows as `weatherProbability` — *the per-slot chance
the current weather survives the transition roll*. §4 shows exactly where it is and how it is
encoded, and 775 of the 1,114 scripts spell it `{100, 0, 0}`.

## 2. The layout

Offsets from the **start of the section** (= file base + directory slot 0, which is `0x80` in every
shipped container).

```struct EbpSection000Header base=section size=0x90
+0x00  u32  marker       0x8000000B in 1114/1114 — NOT the file magic, see §8
+0x04  u32  length       bytes of real content, excluding 0x40 padding
+0x08  u32  authorOff    -> NUL-terminated ASCII developer username
+0x0C  u32  sourceOff    -> NUL-terminated ASCII .src filename, e.g. "alc_a0100.src"
+0x10  u32  timestampOff -> NUL-terminated ASCII build stamp, "MM/DD HH:MM"
+0x14  u32  sumTableOff  -> u16 count then u16 entries — the loader SUMS these
+0x18  u32  tableOff18   -> THE SCRIPT DIRECTORY: u32 count, then 0x30-byte per-script entries (BW-5, section 4)
+0x1C  u32  _zero1C      0 in 1114/1114, and never read
+0x20  u32  tableOff20   -> u32 count then 4-byte records
+0x24  u32  tableOff24   -> u32 count then float32 data
+0x28  u32  tableOff28   -> u32 count then 8-byte records
+0x2C  u32  tableOff2C   -> table
+0x30  u32  tableOff30   -> table
+0x34  u32  scalar34     scalar, 0 in exactly 1 file
+0x38  u32  tableOff38   -> table
+0x3C  u32  mspSize      size of the msp region; 0 in 352 files                 (corrected 2026-09-12, see the note below section 3)
+0x40  u32  mspOffset    -> THE MSP REGION: what a tag-3 packed reference (0x03xxxxxx) resolves into
+0x44  u32  stackSize    size of the local-variable storage; 0 in 161 files
+0x48  u32  stackOff     -> THE LOCAL-VARIABLE STORAGE (zero in the file), the `local` class's base
+0x4C  u32  namePoolOff  -> THE NAME POOL, concatenated NUL-terminated strings (= +0x48 only when +0x44 is 0)
+0x50  i16  flag50       SIGNED 16-bit, sentinel 0xFFFF = none — 493/1114 are -1
+0x52  u8[2]  unk52       contents unknown — flag50 is provably 16-bit; the gap is a question, not padding
+0x54  u32  tableOff54   -> table
+0x58  u32  tableOff58   -> table
+0x5C  u32  tableOff5C   -> table
+0x60  u32  optionOff60  -> length-prefixed byte array, variable arity
+0x64  u32  optionOff64  -> length-prefixed byte array, ARITY 3 in 1114/1114 — weatherProbability
+0x68  u32  optionOff68  -> length-prefixed byte array, arity 2 where present (789 files)
+0x6C  u32  trapRefs     -> {u32 count = 1; u32 packedRef} - the trap table's tag-3 reference, read by 002641B0 (corrected 2026-09-12)
+0x70  u32  optionOff70  -> length-prefixed OFFSET array, ARITY 5 in 1114/1114
+0x74  u32  optionOff74  -> length-prefixed byte array, variable arity
+0x78  u32  unk78        not individually characterised   (ff12-script: u16 saveIndex, u16 anchorIndex)
+0x7C  u32  unk7C        not individually characterised   (ff12-script: u16 unkLocation, u16 unkNavIcon)
+0x80  u32  unk80        not individually characterised   (ff12-script: unknown16Arr3Off)
+0x84  u32  unk84        not individually characterised   (ff12-script: jumpGroup2Off; +0x88 u16 unkScriptId2, +0x8A u16 mooglingIndex)
+0x88  u32  unk88        not individually characterised
+0x8C  u32  unk8C        not individually characterised
```

The header ends at `+0x90` and all authored data begins there. **`+0x52 .. +0x54` is reported
`UNACCOUNTED` and that is correct** — `flag50` is provably 16-bit (§3), and what occupies the two
bytes after it is not known. A gap is a question, not padding.

**The header is exactly `0x90` (144) bytes in 1,114 of 1,114 files.** That is not an assumption from
one file: taking the smallest in-section value across every offset-valued header field, in every
container, gives **144 every time**. Nothing is ever pointed at below `0x90`, and the first thing at
`0x90` is the build timestamp string.

**All offsets in this header are relative to the start of the section**, not to the file and not to
the payload. `+0x08` = `0x9C` in `alc_a0100.ebp` resolves to section+0x9C, which is `"mtaniguc"`.

### The `option` block is a run of length-prefixed arrays

~~`+0x60` through `+0x74` each point at an array whose **first byte is the element count**, followed~~
~~by that many bytes.~~ `+0x60` through `+0x74` each point at a counted array, but not of one shape: `+0x64` is a count byte then that many bytes, while `+0x6C` and `+0x70` are a `u32` count then `u32` elements *(corrected 2026-10-02, OPUS: `002641FF` `cmp esi, dword ptr [rcx]` and `00264203` `mov ebx, dword ptr [rcx + rsi*4 + 4]` read `+0x6C`'s target as `{u32 count; u32 ref[]}`, and `+0x70`'s target is `05 00 00 00` then five ascending `u32` offsets in the shipped images; `+0x60`, `+0x68` and `+0x74` carry three zero bytes after the count in every file, so the data does not settle their width)*. Censused over all 1,114 files, three of them have a **fixed** arity:

| field | first byte of target | reading |
|---|---|---|
| `+0x64` | **`3` in 1114/1114** | a 3-element authored option — `weatherProbability` |
| `+0x6C` | **`1` in 1114/1114** | ~~a 1-element authored option~~ `{u32 count = 1; u32 packedRef}`, the trap reference *(corrected 2026-10-02, OPUS: `002641FF` / `00264203`; the header map above, corrected 2026-09-12)* |
| `+0x70` | **`5` in 1114/1114** | 5 entries, and these are 4-byte offsets rather than bytes |
| `+0x68` | `2` in all 789 where non-zero | a 2-element option |
| `+0x60`, `+0x74` | varies (0–15+) | variable-length authored lists |

**A count that is the same in every one of 1,114 files is a fixed-arity field, not a coincidence.**
That is what makes `+0x64` identifiable: the glossary independently records `weatherProbability` as
a three-value authored option, and `+0x64` is the only header field whose array is three elements in
every script.

## 3. The loader contract

Slot 0 is dispatched by the container walker (`0x003304A0`, read at `00330504`, called at
`00330514`) into:

```
ActorResource_OnDefinitionPayloadLoaded          0x0032F850
  → ActorManager_BindLoadedDefinitionPayload     0x0026C8C0   (1,330 B — the header parser)
```

`OnDefinitionPayloadLoaded` recovers the section pointer (`0032F871 and rdi, rax`), stores it to
`DAT_022c6c28[manager]`, and — this is the one guard on the whole section —

```asm
0032F87E  cmp byte ptr [rdi], 0        ; is the FIRST BYTE zero?
```

**checks only that the section's first byte is non-zero.** The marker `0x8000000B` begins with
`0x0B`, so it passes; a zero-filled buffer fails and the manager is flagged "definition not loaded".
**The marker itself is never compared against `0x8000000B`.** Like the container's `EBP2`, it is
authoring provenance.

Then a **language-selected decoder** is chosen — `FUN_00267930` (id 5), `FUN_00267bb0` (id 0xD) or
`FUN_00267c20` (id 0xE), gated by `FUN_0036b200` — and passed to the header parser as a callback.
This is the seam where a localisation variant changes how the script's text is decoded.

### What `ActorManager_BindLoadedDefinitionPayload` reads

The payload pointer lives in `r15` (`0026C8F7 mov r15, rdx`) and the destination is the actor-manager
record in `rdi` (`0x02098E10 + idx*0x288`, proved by `FUN_00263FF0` at `00263FF3`/`00263FFA`).
Enumerating **every** `r15` reference in the 1,330-byte body gives the complete read set — there are
no others:

| Field | Read by | Instruction | Becomes | Inert |
|---|---|---|---|---|
| `+0x00` marker | — | — | — | **YES — only `!= 0` on the first byte, at `0032F87E`** |
| `+0x04` length | — | — | — | **YES — no reader found in the loader (see §7)** |
| `+0x08` author | — | — | — | **YES — no reader found; pure provenance** |
| `+0x0C` source name | — | — | — | **YES — no reader found; pure provenance** |
| `+0x10` timestamp | — | — | — | **YES — no reader found; pure provenance** |
| `+0x14` | `0026C8C0` | `0026CB7D movsxd r11,[r15+0x14]` | a **sum**, see below | — |
| `+0x20` | `0026C8C0` | `0026CB3C movsxd rax,[r15+0x20]` | rebased → record `+0x68` | — |
| `+0x24` | `0026C8C0` | `0026CB47 movsxd rax,[r15+0x24]` | rebased → record `+0x70` | — |
| `+0x28` | `0026C8C0` | `0026CB60 movsxd rax,[r15+0x28]` | rebased → record `+0x78` | — |
| `+0x2C` | `0026C8C0` | `0026CB52 movsxd rax,[r15+0x2c]` | rebased → record `+0x80` | — |
| `+0x48` ~~name pool~~ **local-variable storage** (corrected 2026-09-12) | `0026C8C0` | `0026CB04 mov eax,[r15+0x48]` | rebased → record `+0x50` (`0026CB17`) | — |
| `+0x50` | `0026C8C0` | `0026CD1A cmp word ptr [r15+0x50], bx` | a **boolean** → record byte `+0x12` | — |
| `+0x1C`, `+0x18`, `+0x30`–`+0x44`, `+0x4C`, `+0x54`–`+0x8C` | — | — | — | **not read by this loader** (§7) |

**Signedness is a real distinction here and the sheet keeps it.** `+0x20`, `+0x24`, `+0x28` and
`+0x2C` are sign-extended (`movsxd`); **`+0x48` is zero-extended** (`mov eax`, `0026CB04`). A
negative value in the first four would rebase *backwards* out of the section; in `+0x48` it cannot.

**Rebasing is unchecked.** Each is `add rax, r15` (`0026CB0F`, `0026CB40`, `0026CB4B`, `0026CB56`,
`0026CB64`) with **no bound against `+0x04` and no bound against the section's extent.** An offset
past the end of the file produces a pointer past the end of the buffer, stored and used later. **The
loader clamps nothing and rejects nothing here** — the only rejection in the entire section-0 path is
the first-byte-non-zero test at `0032F87E`.

### The one field that is transformed rather than stored

`+0x14` is the exception: its table is **reduced to a single number**.

```asm
0026CB7D  movsxd r11, dword ptr [r15 + 0x14]   ; table offset
0026CB81  movzx  r10d, word ptr [r11 + r15]    ; u16 count at the table head
0026CB8C  lea    rcx, [r15 + 4]
0026CBC1  movzx  r12d, word ptr [rax + r15 + 2]; u16 entries, walked two at a time
```

The loop accumulates two running sums over the `count` u16 entries, adds the odd leftover entry if
the count is odd, and stores `total` into record `+0x20`. So:

```
record[+0x20]  =  Σ  u16 entries of the table at section+[+0x14]
```

**A total of something the script declares per-entry, computed once at load.** The count is `≤ 8` in
every file censused (max observed 8), which makes this a small fixed-purpose table rather than a
per-object list.

`+0x50` is the other transformed field: `cmp word ptr [r15+0x50], bx` with `bx = 0`, and the result
`value >= 0` is stored as a byte. **It is 16-bit and signed**, and the corpus confirms the reading —
`0xFFFF` (i.e. `-1`) appears in **493 of 1,114** files as a "none" sentinel, `0` in 537, and small
positive values in the rest. A 32-bit reading of the same bytes gives nonsense (452 files "out of
range"), so the instruction width is doing real work.

### The write path

**There is none.** No code in the executable constructs this header. The `+0x08`/`+0x0C`/`+0x10`
provenance strings — an author's username, a `.src` filename, a build timestamp — are the signature
of an **offline compiler**, and `+0x0C` matching the `.ebp` filename in **1,114 of 1,114** files is
about as direct as that evidence gets.

## 4. Data structures and formulas

> **The msp region, the local storage and the name pool — corrected 2026-09-12 (FABLE).** The
> sampled file has an empty local storage, which made `+0x48` and `+0x4C` coincide and the name pool
> look like the `+0x48` region. **Census over 1,114 containers:** `+0x4C = +0x48 + +0x44` rounded up
> to 16 in all 953 files whose `+0x44` is non-zero (the bytes between are zero in the file — e.g.
> `alc_a0280.ebp`: size 8, storage `0x1FC0`, names `0x1FD0`), and the two are equal in exactly the
> 161 files with `+0x44 = 0`. So **`+0x48` is the local-variable storage** the binder rebases into
> the manager slot's `+0x50` — the `local` class's base, to which each actor adds its directory
> entry's `+0x1C` (`stackBegin`, [the storage-class page](../../01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md)) — and **`+0x4C` is the name pool.** `+0x3C` / `+0x40`
> are the **msp region** (size, offset): the interior a **packed reference** addresses — `tag` in
> bits 24–26, `offset` in bits 0–23, resolved by the six-way base chooser `00265770` (the same
> table as the variable classes), so `0x03xxxxxx` is `image + mspOffset + xxxxxx`. The first proven
> consumer is the trap table: `+0x6C` is `{u32 1; u32 packedRef}` and `002641B0(slot, index)`
> returns the resolved pointer ([the trap record](../../14-Story-Event-Quest-Hunt/persistent-flag-banks.md)); ff12-script names the fields `mspSize`, `mspOffset`,
> `stackStorageSize`, `stackStorage`, `funcNamesOff` and `trapDataOff`, and its comment on `+0x40`
> ("access to msp by functions 0x3000000 + offset … strings can be used that way") is the same
> mechanism seen from the compiler's side. The option-field names in the header map's right margin
> (`+0x78`–`+0x8A`) are the oracle's, unproven here.

### The name pool at `+0x4C` — the script's authored identifiers

`+0x4C` points at a run of NUL-terminated strings (in `alc_a0100.ebp` the local storage is empty, so
`+0x48` lands on the same bytes). It begins:

```
"init\0" "main\0" "<83 4a 83 62 83 67 82 50>\0" "<...82 51>\0" "<...82 52>\0" "<...82 53>\0"
   init     main    Shift-JIS カット１          カット２       カット３       カット４
```

**`init` and `main` are the actor handler names** the authoring model uses, and `カット1..4` are the
cutscene takes. The pool is **not length-prefixed and carries no count** — it is a flat string blob,
and the tables elsewhere in the header index into it.

**This is Shift-JIS, in the `us` build.** The identifiers were never localised; only the *displayed*
text (sections 002/003) was. That is why a language-selected decoder is installed at load
(`FUN_00267930` / `FUN_00267bb0` / `FUN_00267c20`, §3) while the names stay Japanese.

### `weatherProbability` — where the glossary's `+0x64` actually points

> **BW-4 answered 2026-09-12 (FABLE): the reading instruction is `002658EB`, and the three bytes are
> availability flags to ~~their one consumer, not chances against a roll~~ the transition chooser, and the current weather's own byte is a chance against a roll.** *(corrected 2026-10-02, OPUS: the survival roll is `0025ACA0`, below)* `002658B0(idx)` reads
> the manager record at `02098E10` (version word `≥ 7` at `002658E5`), resolves its `+0x64`
> reference through `ImageAddress_ResolveRuntimePointer` (`002658EE`) and returns `byte[table +
> clamp(idx − 1, 0, 2) + 1]` (`002658F8`–`00265900`) — the arity-3 array behind its length byte,
> indexed by weather 1..3. ~~Its only caller is~~ Its callers are `0025ACA0` (`0025ACCC`) and the transition chooser `0025ABA0` (`0025ABD4`,
> `0025ABE4`, `0025AC05`, `0025AC11`, `0025AC30`, and `0025AC40`, `0025AC61`, `0025AC81` *(corrected 2026-10-02, OPUS: `retool.py callers 002658B0`, nine sites)*): from the current weather it tests candidates'
> bytes **`> 0`** and picks the first available; when both alternatives are open the order is a
> `RNG_MT19937_NextU32 % 100 < 50` coin (`0025ABB8`–`0025ABCB`), ~~and the byte's *value* is never~~
> ~~compared to the roll.~~ and the current weather's byte *is* compared to a roll before the chooser runs *(corrected 2026-10-02, OPUS: `0025ACA0` reads it at `0025ACCC`; `0` re-chooses (`0025ACD6`), `>= 100` keeps (`0025ACD8` `cmp edi, 0x64` / `jge`), otherwise `0025ACDD`–`0025ACEF` draw `00379CD0`, scale it to `0..99` (`imul rcx, rax, 0x64` / `shr rcx, 0x20`) and keep the weather when the draw is below the byte (`jb`); only a failed roll calls `0025ABA0` at `0025ACF3`)*. `0025ABA0` is called from `0025ACA0`, itself reached from the native-command
> family (`002620E0`). So the field gates which weathers may follow the current one; ~~the glossary's~~
> ~~"chance" is a misnomer for this consumer, and whether another reader weighs the values is not~~
> ~~established~~ the glossary's "chance" is right for the current weather's byte, which `0025ACA0` weighs *(corrected 2026-10-02, OPUS: `0025ACD8`–`0025ACEF`, as above)* (the `+0x64` load census over `00260000`–`00280000` finds no other on this record).

The [glossary](../../_index/GLOSSARY.md) records `weatherProbability` as *"authored per-slot chance
the current slot survives the transition roll, script header `+0x64`"*. **This sheet locates it
precisely, and refines the description in one respect:**

> `+0x64` is **an offset field, not the value.** The dword at section+0x64 is a section-relative
> pointer; the option lives at its target, encoded as a **length-prefixed byte array with a fixed
> arity of 3**.

In `alc_a0100.ebp`, `+0x64 = 0x114`, and section+0x114 is:

```
03 64 00 00
^^ count = 3
   ^^ ^^ ^^  = 100, 0, 0      -> option weatherProbability = {100, 0, 0}
```

`100 = 0x64`, which is exactly the decompiled form the category README quotes. Censused over the
whole corpus the count byte is **`3` in 1,114 of 1,114 files**, and the ~~value triples distribute as~~ eight most common of the 17 distinct triples are (1,087 of the 1,114 files) *(corrected 2026-10-02, OPUS: read through `vbf_read_entry` from `FFXII_TZA.vbf`; missing are `{30, 50, 20}` 9, `{80, 10, 5}` 5, `{0, 70, 30}` 4, `{1, 1, 1}` 4 and five single-file triples)*:

| triple | files |
|---|---:|
| `{100, 0, 0}` | 775 |
| `{0, 100, 0}` | 118 |
| `{0, 30, 70}` | 73 |
| `{100, 100, 100}` | 43 |
| `{0, 0, 100}` | 35 |
| `{0, 60, 30}` | 24 |
| `{0, 50, 50}` | 10 |
| `{30, 50, 0}` | 9 |

**Most maps are `{100, 0, 0}` — slot 0 always survives the roll, i.e. the weather never changes.**
The interesting maps are the minority, and `{0, 30, 70}` / `{0, 50, 50}` are the ones where a player
actually sees weather turn over. Values are per-slot percentages and **do not have to sum to 100**
(`{100,100,100}` and `{30,50,0}` both occur), so this is three independent per-slot chances, not a
distribution.

### The authored tables

The four tables the loader rebases into the manager record, as observed in `alc_a0100.ebp`:

| header field | target shape | first bytes |
|---|---|---|
| `+0x20` → record `+0x68` | u32 count `0x23` = 35, then **4-byte records** | `23 00 00 00 \| 00 00 00 03 \| 01 00 00 03 …` |
| `+0x24` → record `+0x70` | u32 count `0x44` = 68, then **float32 data** | `44 00 00 00 \| 00 00 80 bf (-1.0f) \| …` |
| `+0x28` → record `+0x78` | u32 count 4, then **8-byte records** | `04 00 00 00 \| 15 00 00 11 00 00 00 00 \| …` |
| `+0x2C` → record `+0x80` | index/relation data with `0xFFFF` fills | `00 00 00 00 08 00 ff ff ff ff …` |

All four share the shape **`u32 count` followed by fixed-width records**. The float table at `+0x24`
is the one a modder is most likely to want — floats in a script image are positions, angles and
timings.

> **Decoded by their runtime readers, 2026-09-11 (FABLE-S000-DECODED).** The interpreter reaches the
> four rebased pointers through the manager slot it receives as its first argument
> ([the interpreter page](../../01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md) §14), and each table has exactly one kind of reader:
>
> | header field → slot | reader | what the records are |
> |---|---|---|
> | `+0x20` → `+0x68` | `PUSHI` (`0x4E`, `00261855`): `[pool + operand*4 + 4]` | **the int constant pool** — the 4-byte records are the script's integer immediates |
> | `+0x24` → `+0x70` | `PUSHF` (`0x50`, `0026187D`) | **the float constant pool** |
> | `+0x28` → `+0x78` | `ScriptVariable_Resolve` (`00262440`, `00262459`) | **the variable descriptor table** — each 8-byte record's first dword is `offset:24 \| class:3 \| float:1 \| width:4` ([the storage-class page](../../01-Script-VM-Native-Bridge/Interpreter-Core/script-variables-and-their-storage-classes.md) §2.2); the `15 00 00 11` above is a `file`-class `s8` at offset `0x15` |
> | `+0x2C` → `+0x80` | `PUSHTAG` (`0x4C`, `002617C9` / `00261806`) | **the tag table** — count at `+0`, then 8-byte entries whose dword `+0` is an offset added to the image base and whose word `+0xE` becomes the pushed value |
>
> Three more header offsets the loader leaves alone are read at runtime as **variable homes**:
> `+0x38` (`image + tableOff38`, the `file` class, installed into the slot's `+0x40` by
> `ActorSystem_InitializeManagerRuntime` at `0026D2F6`), `+0x40` (`image + tableOff40`, class 3, ~~no~~
> ~~shipped script uses it~~ which no shipped variable descriptor uses, though 389 of the 1,114 scripts reach it through the tag-3 trap reference at `+0x6C` *(corrected 2026-10-02, OPUS: `002641B0` → `00265770` case 3 at `002657B2` = image + `[image + 0x40]`; 0 class-3 descriptors among 43,466 in the `+0x28` tables, read through `vbf_read_entry` from `FFXII_TZA.vbf`)*) and the `+0x48` region (~~the name pool is only its start~~ the
> local-variable storage, `+0x44` bytes — the name pool is the next field, `+0x4C`; corrected
> 2026-09-12: the `local` class
> resolves `[slot + 0x50] + [[record + 0x40] + 0x1C]` through `00264E30`). So "not read at load"
> for `+0x38`, `+0x40` and `+0x48` now has its readers named.

### Entering the bytecode

The script becomes running code through `ActorResource_StartEntryScriptExecution` (`0x003DBDC0`),
whose two callers are the interpreter itself (`0x0025E4C0`) and
`ActorResource_SelectPendingEntryForExecution` (`0x003DB6E0`):

```c
offset = ActorScriptResource_GetBytecodeOffsetById(ctx, *(u16*)(entry + 4));  // 0x00358A00
ScriptExecutionState_ResetCore(exec);
*exec = offset + *(int64*)(ctx + 0x58);        // PC = image base + bytecode offset
*(u8*)(exec + 0x14) = 1;                       // execution-state kind
*(u8*)(entry + 0x11) = 3;                      // entry lifecycle advances
```

The lookup is bounds-checked, and its shape is exact:

```asm
00358A00  mov    r8, qword ptr [rcx + 0x48]    ; the table
00358A04  cmp    edx, dword ptr [r8]           ; id vs u32 count at the table head
00358A07  jb     0x358a0c                      ; out of range ->
00358A09  xor    eax, eax                      ;   returns 0, silently
00358A0C  movsxd rax, edx
00358A0F  mov    eax, dword ptr [r8 + rax*8 + 8]  ; 8-byte stride, dword at entry+0   <- corrected 2026-10-02, OPUS - entries start at +4 after the u32 count, so +8 + 8*id is the entry's SECOND dword (offsetWithinScript); the shipped tables put the name-pool offset first ('init', 'main'), BW-5 below
```

**An out-of-range script id returns offset `0`, not an error** — so it starts executing at the image
base rather than refusing. Its sibling `FUN_003589E0`, called by the interpreter, is the same
construct on a different table: `[rcx+0x50]`, **4-byte stride from `+4`** (`003589EF`).

> **The structure is the ActorStorageRecord, 2026-09-11 (FABLE-S000-DECODED).** The generation-3
> record census reaches both lookups from the actor record: `ActorResource_StartEntryScriptExecution`
> (`003DBDC0`) receives the record in `rcx`, takes the request entry from the record's `+0xA8` array
> by its `+0x11` slot (`003DBDD4`–`003DBDEE`), calls `ActorScriptResource_GetBytecodeOffsetById` with
> the record unchanged (`003DBDF2`, reading the record's **`+0x48`** table), and forms the pc as
> `offset + [record + 0x58]` (`003DBE02`–`003DBE09`) — the store's `payloadSectionB` **is** the
> bytecode base, so the GFZ comment was right and the earlier "ruled out" was the manager slot, a
> different object. `FUN_003589E0`'s table is the record's `+0x50` (`payloadSectionA` of the *record*,
> not of the slot, which shares the name). Both are per-actor pointers into the image; who plants
> them is the remaining half of BF-4 (`ActorStorage_InitializeRecord` stores the record's `+0x40` at
> `00266734`).

> **BW-5 answered 2026-09-12 (FABLE): the two tables are the script's function table and its jump
> table, and the initialiser plants both from the script directory.** `ActorStorage_InitializeRecord`
> (`00266530`) takes the image in `rsi`, forms the directory as `image + [image + 0x18]`
> (`00266710`–`00266717`) and the actor's entry as `directory + 4 + index × 0x30` — the stride is
> `0x20` when the image's first word is below 8 (`0026671A`–`0026672D`), which no shipped file is:
> the marker `0x8000000B` puts every container on the 0x30-byte layout. Then, with `0020E600`
> (`ImageAddress_ResolveRuntimePointer`, an add of the process image base) on each offset:
>
> ```
> script directory entry  (0x30 bytes; ff12-script's tScriptNames, CScriptContainer.h)
>   +0x00  u32  scriptNameOff   into the name pool (+0x4C)
>   +0x04  u16  scriptType      0..7 (0 event, 1, 3, 5, 6 field actor, 7 in the corpus)
>   +0x06  u16  pcId            0xFF, or 0x80..0x83 = a party slot: 00266738-00266792 plants the record
>                               in the live roster 0209A1F0 at pcId & 0x7F and sets record +0x12 / +0x0F
>   +0x08  u32  scriptStartOff  -> record +0x58, the bytecode base            (002667C0-002667CA)
>   +0x0C  u32  numOfInstructions
>   +0x10  u32  nameOff         -> record +0x48: {u32 count; {u32 nameOffInPool, u32 offsetWithinScript}[count]}
>                                                                              (00266795-002667A2)
>   +0x14  u32  listOff         -> record +0x50: {u32 count; u32 offsetWithinScript[count]}
>                                                                              (002667A6-002667B9)
>   +0x18  u32  sepaOff         -> tFuncFooter {u16 0x12; u16 special[18]} then the spawn data
>   +0x1C  u32  stackBegin      (the local class's per-actor offset, [record+0x40]+0x1C)
>   +0x20  u16  duplicateId;  +0x22  u16  pos;  +0x24..+0x2C  u32 x 3, zero
> ```
>
> So `ActorScriptResource_GetBytecodeOffsetById(record, id)` returns **function `id`'s offset within
> the script** (the 8-byte entry's second dword) and the pc is that plus the script's start; and
> `FUN_003589E0(record, imm)` returns **jump target `imm`'s offset within the script** — its three
> callers are the `JMP` family's shared implementation in the interpreter (`002618AE`, `00261967`,
> `00261A63`, each followed by `mov r14, [r15 + 0x58]`, [the interpreter page](../../01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md)), so a jump immediate is an
> index into the script's jump table, not a byte offset — which is what ff12-script's decompiler
> assumes (`localjmpVector[instruction->getImm()]`, `CScriptDecompileAsmDecode.cpp:335`). In
> `alc_a0100.ebp` the directory holds 18 scripts; the first (`ドラクロア研究所`, start `0xBC0`) has two
> functions, `init` at `+0` and `main` at `+1`, and 81 jump targets; `EventLightActor` has `init`,
> `setEventLight` and 11 jump targets. **Census over all 1,114 containers, 26,390 entries:** the
> marker's low word is `0x000B` in every file (0x30-byte stride throughout); every entry's `listOff`
> equals `nameOff + 4 + 8 × functionCount`, every `sepaOff` begins `0x0012`, and every entry's
> function 0 starts at offset 0. ff12-script's `_writeFunctionMetadata` emits exactly this layout,
> and its `tScriptHead` names `+0x18` `funcBodyDecOff`. The earlier "name pool" reading of the
> ledger row was the manager slot's `+0x50` (set from header `+0x48` at `0026CB17`), a different
> object; the record's `+0x50` is this jump table ([the storage-record field map](../../04-Actor-Entity/Actor-Storage-Record/the-actor-storage-record-field-map.md)).

## 5. Corpus survey

**Invariants over all 1,114 containers:**

| | |
|---|---|
| `+0x00` = `0x8000000B` | **1,114 / 1,114** |
| `+0x04` ≤ distance to the next present section | **1,114 / 1,114** (exactly equal in 304; the rest padded to `0x40`) |
| `+0x1C` = 0 | **1,114 / 1,114** — and never read, so **inert, not merely constant** |
| header size = `0x90` | **1,114 / 1,114** |
| `+0x0C` string matches the `.ebp` filename stem | **1,114 / 1,114** |
| `+0x64` target arity | **3 in 1,114 / 1,114** |
| `+0x6C` target arity | **1 in 1,114 / 1,114** |
| `+0x70` target arity | **5 in 1,114 / 1,114** |

**`+0x04` is the true content length and the padding is the container's doing.** In 304 files the
section runs exactly to the next slot; in the other 810 the gap is larger because the next offset is
rounded up to `0x40`. So a reader must take the *length* from `+0x04` and must **not** infer content
from the slot-to-slot distance.

**Provenance fields, censused:**

| field | result |
|---|---|
| `+0x08` author | printable in **1,097 / 1,114**; **28 distinct names** — `t-hirose` 220, `mtanaka` 184, `naomif` 112, `ymurasaw` 91, `kryoko` 86, `s-ohzono` 71, … |
| `+0x0C` source | printable in **1,114 / 1,114**, all matching the filename |
| `+0x10` timestamp | printable in **1,114 / 1,114**; **1,113 are `"00/00 00:00"`** and exactly **one** is `"11/22 12:00"` |

**The timestamps were deliberately zeroed for the shipping build, and one file escaped it.** That is
a build-process artefact preserved in the retail data, and the single outlier is the kind of detail
that is worth recording precisely because a summary would erase it. The 17 files whose author field
is not printable are worth a look by anyone extending this sheet.

**The outlier that is not this section:** `us/event/evt_t/evt_t0020/evt_t0020.ebp` has **no
`section_000`** because it is not a container — it is a bare section body (marker `0x80000007`,
2,416 bytes) wearing a `.ebp` name. It is the reason this unit is 1,114 of 1,115 rather than
1,115 of 1,115.

### REQ-family channel census — 2026-09-18 (SWE2-DATA, `FABLE-REQ-SWE2-DATA-REQ-CHANNEL-RANGE`)

Full-corpus scan of **all 10,036 valid `.ebp` containers** (every locale, 237,662 script bodies;
[`members/req-channel-census.tsv`](members/req-channel-census.tsv),
[`members/gen_req_channel_census.py`](members/gen_req_channel_census.py)). The REQ-family descriptor
builders pop three stack values; the third pop — the **first-pushed** argument — is the channel,
stored into the descriptor at `002689B1` (the EF-2 narrowing). Only three channel-carrier opcodes
ship: `REQ` (197,102 sites), `REQEW` (101,398) and `REQSW` (27,704); `FREQ`, `TREQ`, `FREQSW`,
`TREQSW`, `FREQEW` and `TREQEW` never appear. `PREQ*`/`REQWAIT`/`REQCHG`/`REQCANCEL`~~/`REQALL`/`REQIALL`~~ *(corrected 2026-10-02, OPUS: `REQALL` and `REQIALL` pop a channel — `00261B6C` / `00261C69` `call 00267E10` into `[rsi + 0x26]` at `00261B80` / `00261C7D` — the correction that follows)*
consume built entries and carry no new channel. ***Corrected 2026-09-24 (FABLE, Claude Opus 5.5) for
`REQALL`/`REQIALL`:*** each pops **one channel** and submits fresh requests to a whole authored actor
list. The channel is an immediate between 0 and 7 at all 51,511 shipped sites, so no `≥ 0x80` channel is
authored there either. See the next section.

**All 326,204 channel operands are authored immediates; distribution
{0:18, 1:242611, 2:43738, 3:16446, 4:13347, 5:7929, 6:198, 7:1917} — maximum `0x07`, zero ≥ `0x80`.**
Closes UQ-54/EF-2 on the authored side: no shipped script can write a negative channel byte
([closure note](../../01-Script-VM-Native-Bridge/Spawn-Verbs/the-script-to-native-calling-convention.md)).

Decode notes from the census: `0x03`/`0x04` are real unnamed 1-byte opcodes mid-code (not data);
script regions bound at the script directory offset; `CALL`-family stack effects come from the
measured verb table (arity = `pops_int+pops_float`, result = `pushes+result_writes`); duplicate
script entries share code regions and are deduplicated by (file, pc).

### `REQALL`, `REQIALL`, `REQWAITALL` — one opcode, a whole actor list — 2026-09-24 (FABLE, Claude Opus 5.5)

**What the player sees.** An event starts several characters at once: a whole group turns, walks or
emotes on the same beat, and the scene waits until every one of them has finished before it goes on.
Scripts do this with three opcodes. The first two hand a request to every actor on an **authored list**;
the third waits for the whole list.

**The list is data in the script's own payload.** Payload header `+0x30` holds the payload-relative
offset of a table:

```
table = payload + [payload + 0x30]    { u32 count; u32 listOffset[count] }            (payload-relative)
list  = payload + listOffset[i]       { u32 count; { u16 actorOrdinal; u16 functionId }[count] }
```

The opcode's 16-bit operand is `i`. The handlers read it exactly this way: `00261B27`–`00261B53`
(`REQALL`), `00261C24`–`00261C50` (`REQIALL`), `00261CCD`–`00261CF9` (`REQWAITALL`). Each offset goes
through the resolver `0020E600` and then has the payload base **added again** (`movsxd rcx, eax; add
rcx, r13`). That is correct only while the image-address base is zero. So this path is one more
consumer that relies on the zero base the
[authored-table contract](../../02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md) §7
reconciles.

On a shipped script (`us/event/alc_a/alc_a0100.ebp`), list 0 is actors 9–17, each running function 1,
and list 1 is the same actors running function 2.

**What each opcode does** (static, read from the handlers and the submitter `00268B10`):

| opcode | stack | effect |
|---|---|---|
| `0x5F REQALL` | pops the **channel** | If any listed actor still has that channel active, it parks as **wait kind 7** and rewinds the PC to re-execute (`00261B97`–`00261BB6`). Otherwise, or once the channel is free, it submits one request per listed actor: run `functionId` on `channel` (`00268A80` → `00268B10` → `003DBB60`/`003DBBE0`). |
| `0x63 REQIALL` | pops the **channel** | The same, with a flag of 1 passed to `00268B10`. After a successful submit, if the target's manager slot has `slotFlags` bit 7 or `passFlags` bit 1, it also bumps the target's `+0x10`, sets `1 << channel` in its `+0x24` and marks the slot (`00268BEA`–`00268C0B`). |
| `0x61 REQWAITALL` | none | Arms **wait kind 5** on the list. The actor stays parked while any listed `(actor, functionId)` still has an active request entry (`00261D0B`–`00261D24`, poll `002674B0`). |

**Details that change behaviour:**
- **The busy check is conditional.** `REQALL`/`REQIALL` test the dispatch byte `edx = [slot + 0x201]`,
  the manager slot's `subStepOptIn`, at `00261B15`/`00261C12`. When it is zero they skip the kind-7 check
  and submit at once, leaving any contention to entry admission (the request queue's kinds 0/2/4).
- **The channel survives the park.** The popped channel is kept in wait `+0x26`. When the check passes it
  is pushed back for the submitter; on re-execution after a park, `+0x15` selects the path that re-pushes
  it (`00261BD0`).
- **Some targets are skipped silently.** `00268B10` skips any listed actor whose record byte `+0x18` is 1
  (`00268BBE`, `00268C60`). ~~The type store labels that value "active", which does not fit a skip. The
  label and this branch disagree, and the question is routed to the type owner rather than resolved
  here.~~ *Resolved 2026-09-27 (FABLE, Claude Opus 5.5), on OPUS-NOTICE-FABLE-SECTION000-PAIRLINK-RESOLVED: the owner renamed the byte on 2026-09-25 - `ActorStorageRecord +0x18` is `pairLinkState` (0 unlinked, 1 the linked side, 2 the initiator; `00262F90` writes `1` into the partner at `00262FDB` and `2` into the initiator at `00262FF0`, and the teardown `002693D0` switches on 1/2). So the skip drops the linked partner of a pair; label and branch agree (the store row records the skip).*
- **The submit path depends on the issuer.** The issuer's `+0x02 == 1` and `+0x10 == 0` select the
  immediate insertion `003DBB60`; otherwise the deferred `003DBBE0` is used. This is the same issuer gate
  as the single-actor path (`00268850`, Section-12 `A12-1`).
- **The wait holds a pointer into the payload.** The armed wait keeps `encode(list address)`, a 32-bit
  image-address reference, in slot `+0x1C` with its cursor at `+0x22`. It therefore stays valid only as
  long as the script's payload stays bound and does not move. That is the list-wait **ownership**
  answer: the list belongs to the script resource, and the wait borrows it.

**Measured over every shipped script**
([`members/gen_list_wait_census.py`](members/gen_list_wait_census.py) →
[`members/list-wait-census.tsv`](members/list-wait-census.tsv)). The census's control is that its site
counts reproduce the REQ-family census exactly.

| | `REQALL` | `REQIALL` | `REQWAITALL` |
|---|---:|---:|---:|
| sites | 47,812 | 3,699 | 8,851 |
| list index out of range | **0** | **0** | **0** |
| empty list (a no-op) | 2,286 | **1,485** | **1,674** |
| longest list | 41 | 34 | 41 |
| channel immediates | 0–7 (1: 31,018) | 1–5 (1: 3,339) | — |

6,077 of 10,036 scripts carry a list table: 44,894 lists and 298,410 pairs, with actor ordinals up to
116 and function ids 1–63. **No shipped operand reaches the null-list path**, which an out-of-range
index would take. Empty lists are authored, and they turn `REQIALL` and `REQWAITALL` into immediate
no-ops at 40% and 19% of their sites (and `REQALL` at 5%).

**Not established here:**
- what `0025B580` does after a submit;
- the meaning of target `+0x10`, `+0x24` and `+0x26` beyond "per-channel masks set in lockstep";
- why so many lists are empty. Presence filtering at build time is one reading, not tested.

## 6. Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Is `+0x0C` really the source filename, or a name that merely looks like one? | **It matches the containing `.ebp`'s own filename stem in 1,114 of 1,114 files.** A coincidence would not survive 1,114 trials. |
| Is `+0x64` the option value, or an offset to it? | **An offset.** The dword there is `0x114` in the sampled file — not a probability. Its *target* is `03 64 00 00`. The glossary's `+0x64` is right about the location and this sheet refines the encoding. |
| Is the `3` at `+0x64`'s target a count, or the first data byte? | Fixed at `3` across **all 1,114** files while the following bytes vary freely, and `+0x6C`/`+0x70` are likewise fixed at `1`/`5`. A data byte that never varies while its neighbours do is a length. |
| Could `weatherProbability` be a different option that also has three elements? | **Not fully excluded, and the sheet says so.** `+0x64` is the *only* header field with arity 3 in every file, and the glossary independently names `+0x64`. Two independent pointers to the same offset is strong~~, but the *reader* was not found — see §7.~~ *(answered: `002658B0` reads it at `002658EB` — BW-4 in §4; 2026-10-02, OPUS)* |
| Is `+0x50` 16-bit or 32-bit? | **16-bit.** The instruction is `cmp word ptr` (`0026CD1A`), and the corpus agrees: as u16 it is a clean `-1`/`0`/small-positive sentinel field; as u32, 452 files are out of range. |
| Is the header really 0x90, or is that one file? | Taking the minimum in-section offset over every offset field in every container returns **144 in all 1,114**. |
| Did the decompiler invent the `+0x14` summation? | Read from raw instruction bytes at `0026CB7D`–`0026CBC1` out of the PE image, independently of the decompiler. |
| Is the object in `ActorScriptResource_GetBytecodeOffsetById` the actor-manager record? | **No — disproved.** If it were, `[rcx+0x50]` would be the name pool (record `+0x50` is set from `+0x48` at `0026CB17`), and `FUN_003589E0` would read `"init"` as a u32 count. It is a different structure; see §7. |
| **The oracle.** Does `ff12-script` agree? | **Not consulted for any claim in this sheet.** Every statement is from the loader body or the file corpus. The tool's decompiled output was used only as the *category README already quotes it* — `option weatherProbability = {100, 0, 0}` — and that quotation is what §4 goes on to **confirm independently from the bytes**, in the right direction: bytes first, tool second. |

## 7. What this document does not claim

- **The bytecode encoding itself is not documented here.** This sheet covers the script *image* —
  header, tables, name pool, and how a script id becomes a PC. The instruction stream that the PC
  then walks is the
  [interpreter document](../../01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md)'s
  subject (100 opcodes, one-byte opcode, operand pre-decode at `0x0025E59D`).
- ~~**Who reads `weatherProbability` was not found.**~~ `ActorManager_BindLoadedDefinitionPayload` does
  **not** read `+0x64`; ~~the consumer is in the weather subsystem and was not identified.~~ *(answered: `002658B0` reads it for the chooser `0025ABA0` and the survival roll `0025ACA0` — BW-4 in §4, corrected 2026-10-02; 2026-10-02, OPUS)* So the
  binding rests on (a) fixed arity 3 in all 1,114 files and (b) the glossary's independent
  attribution of `+0x64` — **not on a read instruction.** That is weaker than the rest of §3 and is
  marked as such. `PROPOSED-repos-1e-4`.
- **`Inert` in §3 means "no reader found in the section-0 loader path", with the search named.**
  It is `ActorResource_OnDefinitionPayloadLoaded` plus every `r15` reference in
  `ActorManager_BindLoadedDefinitionPayload`. **Other subsystems demonstrably read fields this
  loader does not** — `+0x64` is the proof of that, so `+0x04`, `+0x08`, `+0x0C`, `+0x10`, `+0x18`,
  `+0x30`–`+0x44`, `+0x4C` and `+0x54`–`+0x8C` must be read as *"not read at load"*, **not** as
  "nothing anywhere reads them". A neighbouring session showed the same trap in section 8, where the
  handler copies a base into a second global and an xref census on the first one under-counts.
- ~~**The tables at `+0x20`/`+0x24`/`+0x28`/`+0x2C` are shaped, not decoded.**~~ Decoded 2026-09-11
  by their runtime readers — int pool, float pool, variable descriptors, tag table (§4). What an
  individual *tag* entry means beyond the pushed word is still open.
- ~~**The structure behind `ActorScriptResource_GetBytecodeOffsetById` is unidentified.**~~ Identified
  2026-09-11: the **ActorStorageRecord** (§4, "Entering the bytecode") — `+0x48` the function-offset
  table, `+0x58` the bytecode base, `+0x50` the table `FUN_003589E0` indexes. The manager slot was
  rightly ruled out; the GFZ comment's `ctx+0x58` was right about a different object.
  `PROPOSED-repos-1e-5` closed. *2026-09-12:* both tables named and their planter read — the
  script directory at header `+0x18` (BW-5, §4).
- ~~**`+0x4C` equals `+0x48` in the one file inspected and was not censused.**~~ Censused 2026-09-12: equal in the 161 files with an empty local storage, `+0x48 + +0x44` rounded to 16 in the other 953 — `+0x48` is the local storage, `+0x4C` the name pool (§3 note).
- **The 17 files with a non-printable author field were not examined.**
- **The language decoders** `FUN_00267930` / `FUN_00267bb0` / `FUN_00267c20` are named as callbacks
  selected by `FUN_0036b200`; their bodies were not read, so "language-selected text decoder" is
  inferred from the selection structure, not from decoding logic.

## 8. Corrections and record

- **`0x8000000B` is not the `.ebp` file magic.** An earlier note in this project recorded it that
  way. It is **this section's marker**, one level down: the file magic is ASCII `EBP2` at file `+0x00`
  and `0x8000000B` sits at file `+0x80`, where slot 0 points. Both are in the first 132 bytes of
  every script, which is how they came to be one sentence. **Neither is validated by the engine** —
  the container walker never reads `+0x00`, and the section handler tests only that this section's
  first byte is non-zero (`0032F87E`), which the marker's low byte `0x0B` satisfies incidentally.
- **The path to the container's `Inert` rows did not repeat the constant scan.** That census is
  recorded dead in the [container sheet](../Container/ebp2-container.md) §8 with the measurement
  that kills it.

## 9. Related

- [`ebp2-container.md`](../Container/ebp2-container.md) — the wrapper that dispatches slot 0
- [`../README.md`](../README.md) — the category census and the 14-unit denominator
- [`01 — Interpreter core`](../../01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md)
  — executes the bytecode this section holds
- [`01 — Verb dispatch`](../../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md)
  — where a script verb becomes engine behaviour
- [`_index/GLOSSARY.md`](../../_index/GLOSSARY.md) — `weatherProbability`, refined in §4
- [`19 — Save image`](../../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/version-stamps-and-what-loading-normalises.md)
  — the persistent flag bank that script globals address

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

- **Presentation — SERVICE.**
  - The header parser `ActorManager_BindLoadedDefinitionPayload` (`0026C8C0`) sets the character fade parameters
    (`CharacterRenderConfig_*Fade*`, `CharacterRenderSystem_SetFade*`).
  - `002620E0` calls a 699-byte Presentation body.
- **Movement — SERVICE.**
  - `0026C8C0` sets `Movement_SetRequestedSpeed`.
  - `ActorStorage_InitializeRecord` (`00266530`) calls two movement bodies, of 420 and 1,339 bytes.

  **Binding a script's header configures fade and movement speed.**
- **Audio — SERVICE.** `002620E0` calls a 768-byte Audio-filed body.
- **CombatAction — CLIENT.** The trap-table reader `002641B0` is also called by the 477-byte trigger sibling of
  `BattleUnit_TryTriggerNearbyAuthoredFieldAction`
  ([walking into an authored trigger point](../../03-World-Area-Field/walking-into-an-authored-trigger-point.md)).

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings become reportable once citations written 0x... or FUN_... count (R5); tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Input — CLIENT.** The 21-byte manager-record accessor this page cites is called by Input bodies of 1,002 and 1,936 bytes.

`00330060` (170 B) is the 16-lane flag commit the container walker `003304A0` calls per slot: `ecx` splits into base `ecx & ~0xF` (stored at ~~`0233A6F0 + lane*8`~~ `022C6CF0 + lane*8`) and lane `ecx & 0xF`; `0026C860` resolves the base, the ~~`0233AE48 + lane*8`~~ `022C6E48 + lane*8` word *(corrected 2026-10-02, OPUS: `00330097` `mov qword ptr [r15 + rax*8 + 0x21a6cf0], rbx` and `003300A4` / `003300B3` `[r15 + rdi*8 + 0x21a6e48]`, with `r15` = `00120000` at `0033007D`)* clears bit `0x40`, a result `& ~1` of zero runs `00263FF0(lane)` and clears bit 3 of `[rax+0x11]`, a nonnull-to-null transition runs `0032F1B0(lane)`, then `0017F790(ecx, base)` and a tail `0029CAC0(base)`

Interior anchor `0033009F` (function `00330060`).
- **Party — SERVICE (2 edges).** 2 outbound (page-cited `ActorManager_BindLoadedDefinitionPayload` (0026C8C0) call Party bodies `PartyControl_SetMovementSuppressionBit` (00359200), `PartyFocus_GetCurrentPackedActorHandle` (003590D0)). Substantive edges include `ActorManager_BindLoadedDefinitionPayload` (0026C8C0) calls `PartyControl_SetMovementSuppressionBit` (00359200); the remaining edges run through shared helpers the page cites.
- **RNG_Random_Selection — MECHANICAL (2 edges).** 2 calls from page-cited bodies into shared RNG_Random_Selection plumbing (`RNG_MT19937_NextU32_Thunk` (00379CD0)) - the helpers' general call surface, not a RNG_Random_Selection relationship of this page's subjects.
- **Save_Load_Settings — MECHANICAL (3 edges).** 3 calls from page-cited bodies into shared Save_Load_Settings plumbing (`SaveImage_GetPersistentPayloadBase` (002EF2B0)) - the helpers' general call surface, not a Save_Load_Settings relationship of this page's subjects.
- **Story_Event_Quest_Hunt — SERVICE (1 edge).** 1 outbound (page-cited `ActorManager_BindLoadedDefinitionPayload` (0026C8C0) call Story_Event_Quest_Hunt bodies `EventMemory_QueryDefinitionIdAbsent` (00377440)). Substantive edges include `ActorManager_BindLoadedDefinitionPayload` (0026C8C0) calls `EventMemory_QueryDefinitionIdAbsent` (00377440).
- **WorldAreaField - CLIENT and SERVICE (11 edges).** 4 inbound (WorldAreaField bodies `0025ACA0`, `0025ABA0`, `MapRef_BeginLoadResources` (00268750) call page-cited `002658B0`, `0025ABA0`, `00267930`); 7 outbound (page-cited `0025ACA0`, `002620E0`, `0025ABA0` call WorldAreaField bodies `002658B0`, `0025ABA0`, `WorldField_InitializeCurrentFieldRuntimeParameters` (0026D910)).

*(pass-22 residue, 2026-10-02, SWE2-CONTRACT — the cited thunk's fan-in, now in the graph)*
- **CombatFormula — MECHANICAL (53 edges).** 53 inbound calls from CombatFormula bodies to the cited
  `RNG_MT19937_NextU32_Thunk` (`00379CD0`) - the thunk's general call surface, not a CombatFormula
  relationship of this page's subjects.
- **CoreRuntimeScheduling — MECHANICAL (2 edges).** `0022B6E0` and `0022B7E0` call `00379CD0`.
- **Rewards_Progression_Economy — MECHANICAL (2 edges).** `002F9A60` and `002F9B20` call `00379CD0`.
- **Status_Periodic_Terminal — MECHANICAL (1 edge).** `00386C70` calls `00379CD0`.
