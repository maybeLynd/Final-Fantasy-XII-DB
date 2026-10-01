---
system: TIM2 images (.tm2 and .nfs) — validation and the seven-slot registry
category: 02-Resource-And-Asset-Pipeline
status: AUDITED
owner_layer: PrimaryOwner:Resource
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
corpus_validated: "456 files (447 .tm2 + 9 .nfs), frozen magic census, 12 of 12 sampled 'TIM2'; no file opened — see section 5"
last_reviewed: 2026-09-06
archive_formats:
  - "tm2 | standard | Sony PS2 TIM2 image container. The spec names the format; section 3 is what THIS build rejects — a 4-byte memcmp, a low-nibble gate on +0x40, and a hard seven-slot registry."
  - "nfs | standard | The same TIM2 container under a different extension — 9 files, all quest menu art. Established by the frozen magic census, not by the extension."
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-tim2-registry-pass-1
  crossref_clean: false
  reopened_count: 0
---

# TIM2 images (`.tm2` and `.nfs`) — validation and the seven-slot registry

> The PS2-era image container the remaster still carries for menu and quest art. **The format is a
> published Sony standard; what is not published is that this build accepts at most seven of them at
> a time, and silently refuses an eighth.**

**Corpus validation.**

| | |
|---|---|
| files | **456** — `tm2` **447** (303.8 MB) + `nfs` **9** |
| trees | `ps2data/image` for both |
| signature | **`TIM2` in 12 of 12 sampled**, per the frozen magic census — one signature across both extensions |
| **files opened** | ~~none~~ **all 456, 2026-09-13 (§8)** — magic `TIM2` in **456 / 456** |
| **the validator would accept** | **10 of 456** — all nine `.nfs`, and one `.tm2` by coincidence (§8) |

> **`.nfs` is TIM2 too, and that is a census result rather than a guess.** `ASSET-FORMATS.md` §4
> previously carried *"`nfs` unknown"*; the frozen signature census groups it with `tm2` at 456
> files. **This sheet declares both because they are one format** — the signature-group rule.

---

## 1. What the player sees

Menu backgrounds, the game-over image, quest artwork — the flat 2-D pictures the interface is built
from, as opposed to the 3-D world. `.nfs` is specifically the quest menu art.

**For a modder the useful fact is the ceiling.** However many TIM2 images a screen wants, **the
engine holds seven registered at once**; the eighth is refused and the caller gets a failure code
rather than a picture. Replacing art is safe; *adding* it is not.

## 2. The layout

**The payload is the Sony TIM2 container and this sheet does not restate it** — that is what the
`standard` disposition means. Only the two header bytes this build actually tests are given here,
with their offsets from the start of the file:

```struct Tim2ValidatedFields base=file
+0x00  char[4]  magic     'TIM2' — compared with a 4-byte memcmp, not an immediate
+0x04  u8[60]   tim2HeaderBody  the TIM2 header proper — read by the decoder, not this validator; deliberately NOT field-split (see note)
+0x40  u32      formatId  only the LOW NIBBLE is tested, and it must equal 1
```

> **The `+0x04..+0x40` span is declared as one unsplit block and that is deliberate.**
> The 60 bytes between the two tested fields are the TIM2 header proper; **naming its members here
> would be transcribing an external spec into a fence and presenting it as read**, which is exactly
> the label-a-gap failure the template warns against. The span is a question, and the answer is in
> Sony's documentation rather than in this binary.

**`+0x40` is the field the spec cannot tell you about**, because the check is a property of this
build, not of TIM2. Everything between `+0x04` and `+0x3F`, and the whole image body, is read by the
decoder rather than by the validator and is out of scope here (§7).

## 3. The loader contract

`FUN_0039BEC0(data)` is the gate, and it is small enough to give whole. It returns a **slot index
1–7 on success and 0 on every failure** — so zero is both "no slot" and "rejected", and a caller
cannot tell which.

```
0039bec9  TEST RCX,RCX                  ; null buffer
0039becc  JNZ  0039bed6                 ;   -> reject, return 0
0039bed6  MOV  R8D,0x4                  ; compare length 4
0039bedc  LEA  RDX,[0x00D11470]         ; the string "TIM2"
0039bee3  CALL qword ptr [0x008C2FF8]   ; imported 4-byte compare
0039bee9  TEST EAX,EAX
0039beeb  JNZ  0039bece                 ; magic mismatch -> reject, return 0
0039beed  MOV  EAX,dword ptr [RDI+0x40]
0039bef0  AND  AL,0x0F
0039bef2  CMP  AL,0x1
0039bef4  JNZ  0039bece                 ; low nibble of +0x40 != 1 -> reject, return 0
0039befb  LEA  RDX,[0x02AEE810]         ; the registry
0039bf02  MOV  EBX,0x1                  ; scan starts at index 1, NOT 0
0039bf13  CMP  qword ptr [RDX+RAX*8],0x0
0039bf1c  CMP  EBX,0x8                  ; ... through index 7
0039bf21  XOR  EAX,EAX                  ; no free slot -> reject, return 0
0039bf31  CMP  qword ptr [RDX+RCX*8],RDI ; already registered?
0039bf35  JZ   0039bf40                 ;   -> return its existing index
0039bf37  MOV  qword ptr [RDX+RCX*8],RDI ; claim the slot
0039bf3b  CALL 0x0039BF50               ; initialise it
0039bf40  MOVZX EAX,BX                  ; return the slot index
```

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| the buffer pointer | `0x0039BEC9` | null → returns 0 | — | — |
| `+0x00` magic | `0x0039BEE3`, a 4-byte compare against `0x00D11470` | not `TIM2` → returns 0 | — | — |
| `+0x40` low nibble | `0x0039BEF0` / `0x0039BEF2` | `!= 1` → returns 0 | — | — |
| `+0x40` high 28 bits | — | — | — | **yes — masked off by `AND AL,0x0F` and never read** |
| every other header field | — | — | — | not read *by this function*; the decoder is out of scope (§7) |

> ### Three facts a spec cannot give you
>
> **1. The magic is checked by `memcmp`, not by an immediate.** `TIM2` occurs **exactly once in the
> whole executable** and **zero times in `.text`** — a scan for the constant finds nothing, and the
> check is nonetheless there. *This is the third distinct magic-checking idiom in this database:
> an immediate compare (`CAM7`), a byte-at-a-time loop (`EFX0010`), and now a `memcmp` against a
> `.rdata` string.* **A search that assumes one of them will report a false absence for the other two.**
>
> **2. The registry holds seven images and ~~index 0 is never used~~ index 0 belongs to someone
> else.** `0x0039BF02` starts the scan at 1 and `0x0039BF1C` stops it at 8, over the table at
> `0x02AEE810`. An eighth concurrent image **fails with the same 0 the malformed-file path
> returns.**
> **⚠ Corrected 2026-09-13 (§8) — §6's own killer observation fires.** `FUN_0039C150` **reads
> and writes entry `[0]`** (`0039C173`, `0039C182`), filling it lazily from another object. The
> scan starts at 1 because slot 0 is **reserved**, not because it is unused.
>
> **3. Re-registering the same buffer is idempotent** (`0x0039BF31`): it returns the existing index
> without re-initialising, so the identity that matters is the **buffer address**, not the contents.
> Two different images at the same reused address would collide.

**What loading normalises:** nothing. The validator does not modify the buffer; `FUN_0039BF50` sets
up the slot, and its body was not read.

**Four callers** — `0x0029CAC0`, `0x0037F1F0`, `0x003BC4E0`, `0x00575710` — none read in this block.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `0x0039BEC0` | `FUN_0039bec0` — the TIM2 validator and slot allocator | ✅ |
| `0x00D11470` | `.rdata` — the string `TIM2`, the **only** occurrence in the image | ✅ |
| `0x008C2FF8` | the imported 4-byte compare the magic test calls | ❌ import thunk only |
| `0x02AEE810` | the seven-slot TIM2 registry; entries `[1]`–`[7]` | ✅ |
| `0x0039BF50` | slot initialiser, called once per newly claimed slot | ❌ not read |
| `0x0029CAC0` · `0x0037F1F0` · `0x003BC4E0` · `0x00575710` | the four callers | ❌ not read |

## 5. Corpus survey

**No `.tm2` or `.nfs` file was opened** — `ps2data/image` is not in the local extraction and no
`.vbf` exists on this machine. The corpus column is the archive index plus the **frozen magic
census**, which is an independent instrument and the reason `nfs` can be grouped with `tm2` at all.

~~**What that costs:** the distribution of the `+0x40` low nibble across the 456 shipped files is
unmeasured.~~ **MEASURED 2026-09-13 (§8): the validator would accept 10 of the 456 shipped files.**
The low nibble is **5 in 417**, **0 in 19**, **1 in 10** and **0xC in 10** — and the ten that carry
the accepted `1` are **all nine `.nfs` plus one `.tm2`**.

~~`.nfs` is 9 files against `.tm2`'s 447, all quest menu art, and the extension split does not
correspond to any difference this validator can see — it tests the same four bytes for both.~~
**⚠ Refuted 2026-09-13 (§8).** It tests the same four bytes for both **and then tests a fifth
field that separates them almost perfectly**: 9 of 9 `.nfs` pass the `+0x40` gate, 1 of 447 `.tm2`
does, and that one is a coincidence. The extension split corresponds to exactly what this
validator accepts.

## 6. Falsification pass — 2026-09-06

| attack | result |
|---|---|
| Is the magic checked at all? | **Yes, and the obvious scan says no.** `TIM2` appears 0 times in `.text`; the check is a `memcmp` against `.rdata`. **The positive controls prove the scan works for other idioms** — the same method finds `cmp dword ptr [rcx],'CAM7'` at `0x002561CA` and `SRYK` at `0x001F43DA`. **Absence of an immediate is not absence of a check**, and this is the cleanest example of it in the database. |
| Is `0x02AEE810` really a seven-entry table? | The scan is bounded by `MOV EBX,1` at `0x0039BF02` and `CMP EBX,0x8` at `0x0039BF1C`, both literals in the listing. |
| Could the decompiler have invented the idempotency? | Read from the listing, not the decompiler: `0x0039BF31` `CMP qword ptr [RDX+RCX*8],RDI` followed by `JZ` past the store. |
| Is `.nfs` really TIM2, or an extension coincidence? | The **frozen magic census** groups them, 456 files at signature `TIM2`. This sheet does not add evidence; it declares on the census's. |
| Does the claim rest on a file? | **No file was opened**, and §5 says what that leaves unmeasured. |

**The killer observation** for *"seven slots, index 0 unused"* would be a second registrar writing
`[0]`, or a caller that indexes the table directly rather than through `FUN_0039BEC0`. **Neither was
searched for** — only the four callers are known, and none was read.

## 7. What this document does not claim

- **The TIM2 image format itself.** That is the `standard` disposition: the spec is external and this
  sheet deliberately does not restate it.
- **What `+0x40` means in the spec.** The engine tests its low nibble against 1; **mapping that onto
  a named TIM2 header field would be inheriting an external reading**, and this sheet reports the
  test rather than the interpretation.
- **What the decoder does with the other fields**, or what `FUN_0039BF50` initialises.
- **Whether the seven-slot ceiling is ever reached in play.** The limit is in the code; the pressure
  on it is not established.
- **Anything measured from a shipped file**, for the reason in §5.

## 8. Related

- [`../../_index/ASSET-FORMATS.md`](../../_index/ASSET-FORMATS.md) §4 — where *"`nfs` unknown"* is
  resolved, and §8 item 5, the `standard` sweep this sheet belongs to
- [`../Prefetch-And-Json-Data/ah-asset-header-manifests.md`](../Prefetch-And-Json-Data/ah-asset-header-manifests.md)
  — the `.ah` lists that name texture assets, and the third magic idiom's counterpart
- [`../../17-Presentation-Rendering/Effect-File-Formats/efx-and-efb-effect-containers.md`](../../17-Presentation-Rendering/Effect-File-Formats/efx-and-efb-effect-containers.md)
  — the byte-at-a-time magic idiom, against this sheet's `memcmp` idiom
- EBP `section_006` also carries the `TIM2` signature in 67 of 1,115 containers — owned by
  `repos-c9`; **the same image container appears embedded in a script container**, which is the
  third place TIM2 turns up and is not explained by either sheet

## 8. Falsification pass 2 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run first, one address at a time and read in full.)*

§5 named the one measurement it wanted and could not make: *"the distribution of the `+0x40` low
nibble across the 456 shipped files is unmeasured … a file that does not carry it would be silently
refused."* **The archive is available now. All 456 files were opened.**

### The signature census is no longer a sample

| | §5 | measured |
|---|---|---|
| files opened | **none** | **456** |
| magic `TIM2` | 12 of 12 **sampled** | **456 / 456** |
| trees | `ps2data/image` | **456 / 456** under `ps2data/image` |
| `.tm2` / `.nfs` | 447 / 9 | **447 / 9** |
| bytes | `.tm2` 303.8 MB | **318.6 MB** decompressed over both |

So the signature-group rule that lets `.nfs` be declared TIM2 now rests on **every file**, not twelve.

### ⚠ The validator would refuse 446 of the 456 shipped files

The `+0x40` low nibble, over all 456:

| low nibble | files | |
|---:|---:|---|
| 5 | **417** | |
| 0 | 19 | |
| **1** | **10** | **the only value `FUN_0039BEC0` accepts** |
| 0xC | 10 | |

And the ten are not a random ten:

| file | `+0x40` |
|---|---|
| `…/{ch,cn,de,es,fr,in,it,kr,us}/quest/menuquest.nfs` — **all nine `.nfs`** | `0x..2F41` |
| `…/in_sdver/tm2_menu/w_line01.tm2` — **one `.tm2`** | `0x01010101` |

> **`FUN_0039BEC0` is the `.nfs` gate, not the TIM2 gate.** Nine of nine `.nfs` pass; **one of 447
> `.tm2` passes, and its `+0x40` is `0x01010101`** — a run of `01` bytes that satisfies the nibble by
> accident. §5's *"the extension split does not correspond to any difference this validator can see"*
> is refuted by the validator's **second** test.
>
> The 417 files with nibble 5 carry the bytes `65 58 74 00` at `+0x40` — ASCII **`eXt\0`**. *(That
> tag belongs to the external TIM2 specification and is named here only as the bytes that are
> there.)* So `+0x40` is **not a uniform `formatId` across the corpus**: in most files the field the
> validator gates on is part of a different structure, which is why the gate fails them.

**What this does not say.** It does not say the art is unreachable — 446 `.tm2` files plainly render.
It says **this function is not the route they take**, and §3's four callers, none of which was ever
read, are where that route would be found. The page's own framing — *"the gate"*, *"however many TIM2
images a screen wants, the engine holds seven"* — is a claim about the format that the corpus makes a
claim about **one loader** instead.

### ⚠ §6's killer observation fires: index 0 is used

§6 says the killer for *"seven slots, index 0 unused"* would be **a second registrar writing `[0]`**,
and that **neither it nor a direct indexer was searched for**. Searched:

`0x02AEE810` is touched by **10 instructions in 8 functions**, not one. Six `lea` the base
(`0039BA30`, `0039BAD0`, `0039BB30`, `0039BB60`, `0039BDA0`, `0039BF50`), `FUN_0039BEC0` is the
seventh — and the eighth is **`FUN_0039C150`**, which addresses **entry `[0]` directly**:

```asm
0039C163  mov rcx, [rip + 0x27526FE]     ; -> 02AEE868, another object
0039C16A  test rcx, rcx / je
0039C173  cmp qword ptr [rip + ...], 0   ; -> 02AEE810, ENTRY [0]
0039C17B  jne 0x39C189
0039C17D  mov eax, [rcx]                 ; a relative offset stored in that object
0039C17F  add rax, rcx                   ;   made absolute
0039C182  mov qword ptr [rip + ...], rax ; -> 02AEE810, ENTRY [0] WRITTEN
```

**So slot 0 is lazily filled by a different owner**, and `0x0039BF02`'s `MOV EBX,1` is a *reservation*,
not an off-by-one curiosity. *"Index 0 is never used"* becomes **"index 0 belongs to `FUN_0039C150`"**,
which is a better fact and the one a modder counting slots needs.

### The magic idiom holds, with its controls

`TIM2` occurs **once in the whole file** and **zero times in `.text`**, and `0x00D11470` is referenced
by **exactly one** instruction, `0039BEDC` in `FUN_0039BEC0`. §6's point stands unchanged.

**Not claimed.** Which loader the 446 `.tm2` files actually go through — the four callers are still
unread, and this pass adds a reason to read them rather than reading them. What `eXt` means: the
bytes are measured, the meaning is external. What `FUN_0039C150` is, beyond that it owns slot 0 and
resolves a relative pointer from `02AEE868`. `FUN_0039BF50` is still unread. The archive was **read,
never written**, and nothing was executed.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings become reportable once citations written 0x... or FUN_... count (R5); tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **ActorEntity — CLIENT.** A 72-byte registry function this page cites is called by a 170-byte actor body.
- **Save_Load_Settings — CLIENT.** The 0xA0-byte SaveLoad body `005832B0` calls `00254A10`,
  the record helper `0039BA30` falls through to when `edx != 0` — the slot-object getter path
  the readers share. Crossing-accounted.
- **Presentation — CLIENT and SERVICE (45 edges).** 39 inbound (Presentation bodies `003EFDF0`, `002B0280`, `00474710` call page-cited `RenderCommand_SubmitCurrentBufferAndSwap` (003A1DB0), `RenderCommand_BeginSubpacket` (003A2090), `RenderCommand_FinalizeSubpacket` (003A2020)); 6 outbound (page-cited `003EFDF0`, `0039BDA0`, `RenderCommand_SubmitCurrentBufferAndSwap` (003A1DB0) call Presentation bodies `003EFDF0`, `GraphicsCommand_PublishCompletedBatchState100` (0036F360), `RenderCommand_SubmitCurrentBufferAndSwap` (003A1DB0)). Substantive edges include `0039BA30` is called by `002B0280`; `0039BDA0` is called by `00252A20`; `0039BDA0` is called by `002528A0`; `0039BDA0` calls `003EFDF0`; the remaining edges run through shared helpers the page cites.
- **UI — CLIENT (15 edges).** 15 inbound (UI bodies `002AC5F0`, `00295D90`, `00554EA0` call page-cited `00254A10`, `RenderCommand_SubmitCurrentBufferAndSwap` (003A1DB0), `0039BA30`). Substantive edges include `0039BA30` is called by `002AC5F0`; the remaining edges run through shared helpers the page cites.
## SWE2-EC7-23 update (2026-09-18) — `0039BA30` registry object accessor

`0039BA30` (153 B) is the indexed registry accessor: `cl` byte slot ->
`[02AEE810 + rax*8]` object pointer (null -> 0), `rbx = rsi + 0x10`; `edx == 0`
returns `&[rbx+0x30]` gated on `[rbx+0x30] & 0x18000` (the flag lane), else the
`00254A10` path — the slot-object getter the image-registry readers share.
Interior anchor `0039BA40` (the table fetch).

## SWE2-EC7-43 update (2026-09-19) - `0039BDA0`

`0039BDA0` (278 B) is a `0039Bxxx` tim2-family body - `02AEE810`-`02AEE890` slot group, `003EFDF0` single call. Interior anchor `0039BE07` (the `003EFDF0` call).

## SWE2-EC7-53 update (2026-09-19) - `003EFDF0`

`003EFDF0` (584 B) is a `0039Bxxx` tim2-family dispatch body - `003A1DB0`/`003A1F20`/`003A2020`/`003A2090`/`003A21A0` plus `02EBEFC0`/`02EBEFF0`. Interior anchor `003EFE22` (a `003A1F20` call).

## SWE2-EC7-55 update (2026-09-19) - `003A21A0`

`003A21A0` (243 B) is a call-free DMA-tag packet emitter - `0x10000001`/`0x51000001`/`0x30000000`/`0x51000000` tag words plus the `0x800000000008000` flag bit, chunked at `0x4000` into `[r11+0x10]`'s queue. Interior anchor `003A2211` (the `movups` tag emit).


## SWE2-EC7-82 update (2026-09-20) - `00473B70` index-table fetch measured

`00473B70` (19 B) is the indexed byte fetch the registry callers
share: `ecx` selects `dword[02CA6C68 + rcx*4 + 8]` - a pointer -
and the fetch returns `byte[ptr]`; no bounds check, no calls.
Interior anchor `00473B7A` (the `movsxd` pointer load).

## SWE2-EC7-91 update (2026-09-20) - `0039BF50` node-list field materializer measured

`0039BF50` (413 B) is the materializer the TIM2 callers run: a
`rip`-held list of qword nodes is walked, and each node's
`word[+6]`-counted sub-records at `+0x10` that exceed 0x30 bytes
take three `0020E600`-resolved offset fixups (`+0xC`, `+0x14`,
`+0x18` under the `0x4000` flag bit) plus a bit-packed word pair
at `+0x1C`/`+0x1E` built from a `rip`-indexed base and the
`si`-derived row/column; records advance by `word[+0x16]`,
capped by a `x 0x3C` limit.
Interior anchor `0039BFC6` (the first `0020E620` call).
