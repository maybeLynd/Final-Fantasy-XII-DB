---
system: The @FEF effect carrier and the @FMC/@FMN/@FMW/@FRM motion entries of .cm/.ca
  files - the model-attached effect and the authored motion-command/motion-library records
category: 17-Presentation-Rendering
status: DOCUMENTED — the embedded EFX0010 reaches only the ret 0 stub (DD batch 14, A1-A9); which @FEF models a session loads and the target-bearing arm's look are runtime-only (owner re-status 2026-10-01, OPUS, on SWE2-CONTRACT's proposed line; documented_rule READY)
owner_layer: PrimaryOwner:Presentation
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the @FEF sub-record binder 00504940 (from 00504F00 at 00505026), the stub
    0016D6A0, the spawn thunk 0041E580 and its resolver 00409FE0, the EFX dispatch
    003B38B0 -> 003EDAD0, the motion-descriptor init 0041BEE0, the
    presentation-entry init binding at 0041D2C5-0041D374 and the motion starter
    00423B10 disassembled from the authority image; the authored layouts then
    re-parsed out of all 1,066 .cm and all 3,164 .ca files in the archive
    (members/fef_motion_entry_census.py, 8 checks, FAILS 0), 2026-09-28
last_reviewed: 2026-09-29
archive_formats:
  - "cm"
  - "ca"
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-fef-falsification-pass-1
  note: written by SWE2-DATA as the UQ-218 @FEF/@FMW/@FRM slice, incorporating
    FABLE's evidence record (_index/candidates/uq218-cm-entry-residues/). The
    @FEF wrapper layout, its sub-record binding, the stub consumer and the
    name-keyed external-EFX spawn path are code-proven; the motion-entry headers,
    names and binding slots are code-proven and census-verified; the @FMC
    command-stream grammar is executor-proven and the .ca variant-1 slot
    tables are census-verified positional entry-offset bands whose selector is
    code-proven (`004090D0` slot[80·group + cmdSlot]); the @FMN fields and tail
    grammar and the @FMW channel mapping are executor- and corpus-proven, and
    the embedded EFX0010 payload is proven dead-authored by an image-wide
    sweep (FABLE, _index/candidates/uq218-embedded-efx-sweep/, FAILS 0), and
    all 33 authored @FMC opcodes have handler-level operand semantics read
    from the dispatch bodies, and FABLE's uq218-residue-fable record closes
    +0x31A/+0x31C provenance, the +0x100 scale consumer, the +0x44 ticket
    readers, 0041E580's callers, and the @FMW arm-0 layout including the
    extended 0x1C record disposition.
    and the 02B64380 row type (the boot-seeded `0040A230` init, CON-195, stores `.rdata`
    `obj_finish` path strings at folded-name slots, all 144 verified), and
    the `0x0B` locomotion classifier `004256E0` behind selector kinds
    `0`/`0xA`/`0xB` (FABLE uq218-fmc-selector-kinds, re-verified
    `classifier.py` FAILS 0) — geometry, availability gating and fallback
    proven; ~~exact band names and the yaw-left sign remain inference/open~~ the band -> @FMN
    binding and the yaw sign are measured through the op 0x0B -> record -> op 0x09 path (2026-09-30,
    pass 18: a positive yaw delta is the character's left).
    Op `0x28` is resolved to mechanism: the authored dword is a lane index
    0..10 into the bound effect definition's request map
    (`byte[def+0xA+lane]` -> `dword[def+0x2C+4*map]` -> `0020E600` ->
    `00333280` child spawn); lanes are per-effect authored ports.
---

# `@FEF` and the motion entries — the model-attached effect and the authored motion commands (SWE2-DATA)

**Package:** `SWE2-DATA-UQ218-FEF-MOTION` (UQ-218 residue). **Player-facing:** this is
the data that puts an effect on a model — summon entrance and aura effects are the
visible case — and the authored motion sets behind weapon draw/fire/reload
states and treasure-chest open states. **Population:** every `.cm` (`1,066`) and
every `.ca` (`3,164`) in the archive. Census: `members/fef_motion_entry_census.py`.

## Entry inventory (SWE2-DATA)

`.cm` files (entry-index table at `+0x30` / `+0x40` by container variant):

| tag | entries | files | role (this sheet) |
|---|---:|---:|---|
| `@FCP` | 1,066 | 1,066 | character parameter block — `fcp-character-parameter-block.md` |
| `@FTR` | 1,066 | 1,066 | node/skeleton table — `ftr-node-table.md` |
| `@FOR` | 1,066 | 1,066 | LOD/variant config — `fdm-and-for-entries.md` |
| `@FDM` | 1,045 | 1,045 | keyed draw-part table — `fdm-and-for-entries.md` |
| `@FTE` | 1,044 | 1,044 | texture table — `fte-fct-texture-colour-tables.md` |
| `@FCT` | 1,044 | 1,044 | colour table — `fte-fct-texture-colour-tables.md` |
| `@FMC` | 209 | 45 | motion command records (this sheet) |
| `@FEF` | 144 | 144 | model-attached effect (this sheet) |
| `@FMN` | 111 | 45 | motion name record (this sheet) |
| `@FMW` | 111 | 45 | motion weight/blend record (this sheet) |
| `@FRM` | 0 | 0 | **`.ca`-only** — the motion resource itself |

The three motion tags co-occur — all `45` `.cm` carriers have all three, and
`@FMN`/`@FMW` are exactly `1:1` (`111`/`111`). The carriers are the
`weapon` (`29` files) and `treasure` (`16` files) directories under
`ps2data/obj_finish/in`.

`.ca` files: `1,969` variant-0 files are 4-entry packs (`@FMC`, `@FMN`, `@FMW`,
`@FRM` — the same four-tag set the container page records); `1,195` variant-1
files are **positional slot tables** of `81`–`311` u32s, every nonzero slot a
blob-relative entry offset (census-verified, zero exceptions): a sparse `@FMC`
band first (holes = motions with no command track — e.g. `c1004_00` has `27`
`@FMC` tracks in ~`80` slots), then a contiguous `@FMN` band, a contiguous
`@FMW` band of the same length (`24`/`24` in `c1004_00`, 1:1 as in `.cm`), and
`@FRM` always the last slot. `378` of the `1,195` carry only the `@FRM`.
`@FRM` occurs exactly once per `.ca` (`3,164`/`3,164`).

The slot selector is resolved too (`004090D0`, reached via `00408F80` for
index lookups and via `00409780`/`00409A30` for tag+name-keyed ones): the
blob is the `@FRP`-magicked container, `dword[+0x30]` = per-group FMC-band
stride (**`80`** in all `1,195`) and `dword[+0x34]` = group count (`{80,1}` in
`1,150`, `{80,3}` in `45` — three identical 80-slot command-track groups, e.g.
`n1018_e3`, = the model-variant dimension). Slot `i` =
`80 * group + cmdSlot`, `0` = absent, entry = `+0x40 + slotval` (offsets are
relative to the table base). `0041CA70` passes `group = s16 word[entry+0x31A]`
and `cmdSlot = word[entry+0x31C] & 0xFFF`; `00408F80` is the group-0-only
wrapper. The `@FMN`/`@FMW`/`@FRM` bands sit after the `80 × groups` FMC zone
(FMN band start = `80 × groupCount`).

**Where `+0x31A`/`+0x31C` come from** (FABLE `uq218-residue-fable` D/A/V,
verified here): the entry initialiser `0041D220` copies descriptor `word+0x20`
→ entry `+0x31C` and `word+0x24` → entry `+0x31A` (`0041D249`/`0041D2A6`).
`0041D220`'s sole caller is the admission `0051BA80`, reached from the first
bind `00424550` and the re-bind `00424D80`; both build the descriptor on the
stack with `+0x20` = the **render event** being bound (the motion slot) and
`+0x24` = `movsx byte[render+0x413]`. Render `+0x413` is the actor's
**standard-motion variation**: verb `01AA stdmotionvariation` (`002E8220`)
stores `v<<3` into actor `+0x14F` bits 3–7 and mirrors `+0x14F>>3` to
`+0x413` (the unit-definition refresh is the other writer); corpus uses
`0`/`1`/`2`. So `+0x31C` = bound render event (motion slot) and `+0x31A` =
which bank of 80 slots — neither is stored in the `.ca`.

## `@FEF` — the model-attached effect (SWE2-DATA)

Authored layout (`144`/`144`, census checks `fef-kind`, `fef-name==basename`,
`fef-magic-off`):

```
+0x00  '@FEF', u32 kind = 0, u32 entryLen, u32 +0x0C = 1
+0x10  char[0x20] name        (== file basename: "s0031", …)
+0x30  embedded EFX file, verbatim — bytes 'EFX0010\0' …
       EFX u32 +0x08 = 1.0f;  u32 +0x0C = entryLen - 0x30 (the EFX's own size)
```

One `@FEF` per carrier, always the last entry (`index 6 of 7`). Dirs: monster
`82`, npc `27`, summon `26`, gadget `9` (FABLE census). The embedded payload is a
complete `EFX0010` document in the sense of
[`../Effect-File-Formats/efx-and-efb-effect-containers.md`](../Effect-File-Formats/efx-and-efb-effect-containers.md)
— 16-byte magic header + chunk list.

### Binding — and the stub

`00504940` (called from the render-record binder `00504F00` at `00505026`):

- resolves `word[rec+0x1F0]` (the `@FRP` selector) → object, then the section
  ordinal `dword[rec+0x200]` via `004096C0` → blob base → `rec+0x1F8`;
- resolves `word[rec+0x228]` (the `@FEF` selector written by `00504E70`) and
  section index `dword[rec+0x238]` → entry pointer → `rec+0x230`;
- then calls `0016D6A0(ecx = dword[obj+0x44], rdx = @FEF + 0x30)` at `005049BD`
  — the embedded-EFX pointer.

**`0016D6A0` is `C2 00 00` — `ret 0`.** The only observed binder-path consumer
of the embedded `EFX0010` is a stub — and FABLE's image-wide sweep
([`_index/candidates/uq218-embedded-efx-sweep/`](../../_index/candidates/uq218-embedded-efx-sweep/README.md),
`efx_consumers.py` E0–E3 + controls, FAILS 0, reproduced here) closes the
rest: every E8/E9 rel32, jcc rel32/rel8 and rip-`lea` at a real instruction
start plus raw u64s in data gives `003B38B0`/`003B3B10` exactly one caller
each (both in `00409FE0`); `'@FEF'` is an immediate at exactly `0040A0A4`,
`00504F78`, `00504FCE`; and over every `.pdata` body no qword read of
`[R+0x230]` carries the render record's shape — while the same fingerprint
over *writes* does find the binder, so a same-shape reader would have been
seen. ~~Remaining caveat: a reader through a *copied* pointer, or via the magic
dispatcher `003EDAD0`, is not excluded.~~ *Corrected 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 14)*: both routes are excluded (A1–A9, in the batch-14
section below). No followed route reads `+0x230`, and none of `003EDAD0`'s six callers passes an `@FEF` entry.

### The live spawn path is name-keyed and external

`0041E580` is a 12-byte thunk — `mov rcx,[rcx+0xD90]; jmp 00409FE0` — called
from `002E4DB4`, `002E4EFA`, `003DC371`, `003DD8AB`. All four sites are
**load-completion callbacks** taken by `lea` (FABLE `uq218-residue-fable` C):
`002E4D20` a script name-binding completion, `002E4E50` a per-lane sub-record
of the binding, `003DC340` a motion-cache slot (`02B57F70`), `003DD850` the
`motionread` verb's (`0x00A2`) external-source request — the `@FEF` effect is
built when a named resource finishes loading, and none of the four uses the
returned handle. The ticket `dword[obj+0x44]` itself has five readers (`E`):
the stamp `003B3B10` (`chara\hN.efx` number), the stop/release `003B37E0`
(`00409CFD` + `00409EB8`, entry disposal), `003B3550` via `0041F6FB` (builds
the character's render object from the ticket, once per character record),
and the binder's `ret 0` stub — the ticket is the **external** effect's
handle, a different pointer than the dead embedded payload. `00409FE0` (the
object in
`rdi` is built by `002ED570`/`00409710`/`00409A60` and holds the name word):

- `0040A0A4`–`0040A0B4`: looks the `@FEF` section up by tag (`00409A30` with
  `edx = 0x46454640`); `-1` → bail. **@FEF presence gates the whole path.**
- `0040A0C0`–`0040A123`: walks the container name to its NUL, then folds the
  last five characters into a letter+number index — the first char multiplies
  by `1,280` (`(c·5)<<8`), the trailing chars fold Horner-style ×10 with a
  `−0x1A0A` bias — indexing the pointer table `02B64380`. A null row faults
  (`0040A135`).
- **`02B64380` rows are `char*` resource paths.** The table sits in the
  `.data` virtual tail (`02B64380`, `.data + 0xD74380`, past the raw extent
  `01F7E400` → zero-filled at load). Its populator ~~survives as dead-stripped
  code~~ is the routine at `0040A230`, *run at start-up (`00409F80`, CON-195; corrected 2026-09-30, SWE2-DATA)* (`.pdata` gap `0040A22C`–`0040AA20`): an unrolled loop of
  144 `lea rax, [rdata path]` / `mov [rip → slot], rax` pairs ending in `ret`.
  ~~No pointer to `0040A230` exists anywhere in the image, and no live rip-ref
  writes the span — so in the shipped build the routine never runs and every
  row stays `NULL`.~~ **CORRECTED 2026-09-29 (OPUS, CON-195): `00409F80` calls it (`00409F84`), and
  `0041E3A0` - the render resource root's initialiser, on the start-up chain from `0017D000` through the boot
  fixups `0022A0B0` - calls `00409F80` (`0041E40B`). The rows are seeded at start-up; the absence scan had
  looked for rip references and pointers, not a `rel32` call.** All 144 surviving assignments verify exactly:
  `table[fold(stem)] = path` where the paths are
  `PS2Data\obj_finish\in\{gadget,monster,npc,summon}\…\<stem>.cm` — `g`×9,
  `m`×82, `n`×27, `s`×26 — the same set as the `@FEF`-carrying `.cm` corpus.
  ~~Shipped-state consequence: reaching this arm with `@FEF` present would fault
  at `0040A135`; the external-name indirection is a vestigial PS2-era
  `obj_finish` staging path, not a live loader.~~ **(CON-195) A seeded name does not fault, and all 144 seeded
  paths are entries of the installed archive; whether a shipped session reaches this arm is not observed.** *(2026-09-30,
  pass 18: the arm is the load-completion path of every one of the 144 `@FEF` models — below.)*
- `0040A13C`–`0040A16F`: `002E9770`/`002E98F0` split the fold into
  `(class, number)`, then `002DF960(class, number)` returns the file's
  archived size from the lookup `u32[02EC3EE0 + class·0x1388 + num]`; the size
  is rounded to `0x40`, and `edx = dword[r14 + roundup64(size) − 4]` — the
  last dword of the loaded resource's own extent (`r14` = `003AB7F0(arg2)`,
  the record whose `+0x10` supplied the name).
- `0040A174`: `003B38B0(rbp, offset)` (`rbp` = `[obj+0x18]` on the primary
  branch) builds the type-3 effect instance
  (pool `02EBDB88`, per the EFX page) → `003EDAD0` dispatches on `EFX0010` /
  `EFX0009` / `EFX0008`; the handle is stored at `obj+0x44`
  (`0040A17C`) — the same `+0x44` the binder path passes to the stub. The row
  (path string) is then handed to `001D6EC0` at `0040A17F` — ~~a name/logging
  call, not blob access~~ **the `AsyncLoadManager` companion lookup** *(corrected 2026-09-30, pass 18, below)*.
- `003B3B10` is also driven with `chara\h` + `%d.efx` (`.rdata` `00D122F0` /
  `00D122F8`) — the external effect files
  `ps2data/effect_finish/jp/chara/h*.efx` (`126` files).

FABLE's join makes the split concrete: **no `.cm` dword equals the EFX file
offset in `143/144` files**, so the `source` `00409FE0` hands to `003B38B0` is
the external blob, not the embedded payload. On every path the image-wide
sweep can see the embedded `EFX0010` reaches only the `ret 0` stub —
dead-authored data in the shipping image ~~(the residual caveat is a
copied-pointer or `003EDAD0`-dispatched reader, not a direct one)~~. *Corrected 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 14)*: that caveat is closed by
A1–A9 below.

## The motion entries (SWE2-DATA)

### `@FMC` — named motion commands (`.cm`, `209` in `45` files; `.ca`, `31,942`)

Header `{'@FMC', kind 1, entryLen, u32 +0x0C = event record count}`,
`char[0x20]` name at `+0x10`, record array from `+0x30`. The names are command names: every weapon
file carries the same five (`weapon_shot`, `weapon_deact`, `weapon_active`,
`weapon_ready`, `weapon_rlx_ready` — `×29`), every treasure file the same four
(`treasure_dead`, `treasure_ready`, `treasure_open`, `treasure_opened` —
`×16`). Lengths `0x50`–`0x120` (`0xB8` = `184` modal, `81`).

**Payload grammar (executor-proven, corpus-total).** `u32 +0x0C` is the event
record count and `+0x30` starts a tiled array of event records, each
`{u8 kind, u8 0, u8 0, u8 subCount, u16 byteLen}` (`0041CD30` bounds the walk by
`dword[+0x0C]` and advances `word[+4]` per record; both record kinds carry a
`subCount`-long stream of sub-records `{u16 key, u16 {cmdCount:6, byteLen:10}}`,
each followed by `cmdCount` commands `{u16 {opcode:7, byteLen:9}}` + operands).
The executor `0041E000` (`PresentationEmbeddedRecord_ExecuteCommandStreamUntilThreshold`)
walks the selected record's keyed sub-records — `key ≤ threshold` fires, the
first `key > threshold` exits with the cursor `state+0x8C` left parked there
(persistent across ticks: each call fires only newly-reached keys; on record
end the cursor resets to `state+0x88` and `state+0x96 |= 0x80`) — and
dispatches every command through the 76-entry × 0x10 table `01EFFAF0`
(`{fn +0, gate byte +8}` — entries with gate byte set are skipped when
`ctx+0xC` bits `0x10`/`0x14` qualify; opcode `0x08`/`0x2C` set the completion
flag). Verified on the full archive: `32,151` `@FMC` entries, `112,439`
records (`32,151` kind-1 — exactly one per entry — and `80,288` kind-0),
`439,220` sub-records, `1,714,500` commands, **zero** structural violations;
`33` of `76` opcodes occur. The table slots are named
`PresentationAuthoredCommand_ClassNN_*` (unused slots point at the
`_guard_check_icall` pad). What earlier read as a `+0x44`/`+0x48`/`+0x4E` word
pattern is the first record's commands — e.g. `10 04`/`0F 06` encode op
`0x10`/`0x0F` with `len 8`/`12` (`{u16 arg, f32}` operands), and `+0x48` =
`0xFFFF` is the lead sentinel key, not a field value.

**Sub-record key domain (resolved 2026-09-28, executor + corpus).** The key is
a **frame index** into the motion's timeline. The per-tick call site passes
`threshold = cvttss2si(f32[state+0xC])` (`0041DBD2`) — the same float
frame-position domain that drives the `@FMW` channel sampler `0041A470`
(`xmm11`, returned by `001ED020` on `obj+0x3C`). Corpus: `272` distinct keyed
values spanning `0`–`700` (the keyed run in `FFFF`-leading records uses only
`0`–`260`), sorted strictly ascending with no duplicates, and key `0` opens
`112,437` of `112,439` records' keyed runs (fire-on-start). `0xFFFF` is
**not** the end marker — it is always **sub-record #0** (`40,441` of
`112,439` records — `38,502` kind-0 + `1,939` kind-1) and carries 1–2
commands: op `0x01` "play track" alone (`38,854`), or the `0x0A`+`0x0B`
selector pair (`1,939`, all kind-1). `0041CD30` scans for it into `state+0x90`
and sets
`state+0x88`/`+0x8C` (cursor init) to the sub-record **after** it — so the
keyed run is what the threshold walk sees, while the `0xFFFF` block's
commands are re-executed **every tick** from the `0041DAD3` direct dispatch
(`state+0x90`-addressed; skipped when `+0x90 == −1`). The remaining callers
of `0041E000`: `0041DBB8`/`0041DC47`/`0041DCC6` pass `r8d = −1` (fire-all
flush — armed when `f32[qword[ctx+0x18]+0xC] ≥ f32[ctx+0x34C]`, the motion's
end position, sets `word[state+4] = 2`); `0041C8FF` is the catch-up loop
replaying `threshold = 1..(int)elapsed` after `0041ADA0` reports elapsed
frames.

**Per-opcode operand semantics (mapped 2026-09-28, image-verified).** Two
dispatch shapes: sixteen ops carry real bodies in `00417110`–`00417DE0`, and
the other ops are null-gated **hook thunks** — a 24-byte body that loads
`tabA[op]` from the `.bss` hook table at `02CA4410` (indexed by opcode;
`0041CCA0` zero-fills it at init, `0041D6C0`/`0041D6D0` install entries) and
tail-jumps it as `fn(obj = qword[ctx+0x2E0], cmd)` if non-null. All hooked ops
are registered at startup (`00426A0D`–`00426B84` for ops `0x11`–`0x48`;
`002EA4xx` registers `tabA[4]=002E70C0`, `tabA[5]=0016D6A0` stub,
`tabA[6]=002E7090`, `tabA[0x0C]=002E70A0`, `tabA[0x26]=002E7080`); the thunk
machinery also reads `tabB` at `02CA4670` (op `0x05` additionally posts to
`tabB[5]=00520C50`). Command lengths below are corpus-verified; operand
semantics are read from the handler bodies. Semantic names crosswalk to
[the authored presentation command handlers](../Authored-Commands/the-authored-presentation-command-handlers.md),
[the ramp-channel contract](../CONTRACT-authored-command-ramp-channels.md) and
[the fade channels](../Character-Render-Records/how-a-character-fades-the-ten-channels.md)
(FABLE `uq218-fmc-opcode-crosswalk` + `uq218-fmc-selector-kinds`, both
re-verified here FAILS 0).

| op | len | uses | handler | semantics (operand reads shown) |
|---|---|---|---|---|
| `0x00` | 4 | 32,151 | `00417810` | **begin — motion number + end frame** — `word+2` sign bit ⇒ held (`0x7FFF7FFF` to `state+0x16`, flag `+0x96` bit 4 cleared); else `frames−1` → `+0x16`/`+0x18`, normalized phase `+0x1C`. Rotates selector `+0x31C`→`+0x324`→`+0x326`; tail-calls `[[02CA4668]+0x2F8]`. |
| `0x01` | 4 | 64,880 | `00417920` | **play track *n*** — `word+2` = `{id:12, mode:4}` (authored modes `{0: 26,026, 1: 36,362, 2: 2,492}`); mode 0 or 2 (with `rec+4==2`) resolve via `0041C9A0` → desc row `+0x80=id`, `+0x96|=2`, `+0x88`→`+0x8C`; mode 1 either initialises the descriptor row (clears + `+0x18=0x1E0000`, `+0x20=30.0f`, `+0x50/+0x52/+0x68=−1`) or sets `ctx+0xC` bit 7. |
| `0x03` | 4 | 6,464 | `00417A80` | **hold here** — if `rec == ctx+0x18` set `ctx+0xC|=8`; else `word[rec+0x18]=word[+0x14]`, `+0x96|=0x40`, and if `rec+0x5E==−1` fill `rec+0x5E = s16[cmd+2] · global_word` (with a `−1→1` coercion). |
| `0x04` | 4 | 27,631 | `00417AD0` | **action-timeline event** (bank A id 4) — 12-mode dispatch on `byte[cmd+2]−1` (jump table). Arm 0 posts four `{dword[cmd], tag 0x80..0x83}` messages to the `ctx+0x2C0` receiver via `tabA[4]`; other arms set `ctx+0xC` bits `0x8000`/`0x200000`, `byte[obj+0x419]|=1|2`, or run `0041F2F0`+`00423F20` on `s16[obj+0xCC]`; always `ctx+0x2C8|=0x10`. |
| `0x05` | 4 | 23,784 | `00417C60` | **character sound** (bank B id 5) — posts `cmd` to `tabA[5]` (the `ret 0` stub — dead) and `tabB[5]`=`00520C50` (`0046CBA0(obj+0x5F0, w+2&0xFFF, w+2>>12)`); `ctx+0x2C8|=0x20`. |
| `0x06` | 4 | 7,008 | `00417CC0` | **second battle guard** (bank A id 6) — posts `cmd` to `tabA[6]`=`002E7090` (conditional `byte[rcx+0xD]&1` gate → `00325090`); `ctx+0x2C8|=0x40`. |
| `0x08` | — | 0 | `00417D00` | **completion** (body exists, never authored) — gated on `ctx+0xC` bits `0x11`/`0x0E`; `+0x2E8` bit0 `^=` `s8[cmd+3]&1`; `byte+2==0xFF` ⇒ bit1 + `+0x354=0`, else `+0x354 = 1/(n+1)`; `ctx+0xC|=0x800` (and `0xE` when `0xD`); clears bit `0x400` on the `002ED570`-resolved `+0x338` object. |
| `0x09` | 4 | 78,455 | `00417F40` | **play this bone motion** (`@FMN` select) — resolves `word[ctx+0x364]` into the `022C6F28` `0x740`-stride record array, `word[ctx+0x318]` via `00409F50`, then tag-looks-up `'@FMN'` (`00409930`/`00409FA0`); index `s16[ctx+0x2A] + word[cmd+2]>>1` (`word[cmd+4]==1` selects the alternate arm). |
| `0x0A` | 6 | 6,726 | `00418600` | **set the selector for `0x0B`** — `byte[cmd+2..5]` → `ctx+0x2DC..0x2DF` (`+0x2DC` = selector kind; `+0x2DD`/`+0x2DE` are the `lo`/`hi` some kinds read); stamps `word[rec+4]=1`, `+8|=2`, `rec+0x20=ctx+0x340`. |
| `0x0B` | `6+2·count` | 6,726 | `00417110` | **choose the next track from a list** — always follows a `0x0A` (all 6,726); gated on `ctx+0xC&0x40000`; `byte[ctx+0x2DC]` is the selector kind — ten authored (`0`/`1`/`2`/`0xA`/`0xB`/`0x10`/`0x20`/`0x21`/`0x24`/`0x25`), each dispatching a selector fn in `.data` table `01F000A0` (installed at `02CA4668` via `0041D6E0`; unlisted kinds → `005C5230` = return 0); kinds `0`/`2`/`0xA`/`0x10` first read back their prior result byte at `obj+0x4B8+i`. `word[cmd+2]>>4` → `ctx+0x2DA`; result `−1` = no change, else lo16 = list index, hi16 = track offset → `obj+0x6DC`/`+0x6D8` and `byte[obj+0x4B8+i]`; then for `i` in `[result&0xFFFF, word[cmd+4])` resets matching `0xA0`-stride desc rows and issues a synthetic op-`0x01` `{0x201, ((word[cmd+6+2i]+resultHi16)<<4) \| (word[cmd+2]&0xF)}`. |
| `0x0D` | 12 | 268,691 | `004173D0` | **per-slot ramp channel, tag 0** — `003B6A90(row, byte+2, {f32+4, f32+8}, 0, 1.0)`; tag byte `+0`, fields `+0x50/+0x54`, targets `+0x60/+0x64`. |
| `0x0E` | 8 | 214,068 | `00417440` | **ramp channel, tag 1** — `003B69B0(row, byte+2, f32+4)`; field `+0x70`, target `+0x74`. |
| `0x0F` | 12 | 295,480 | `00417460` | **ramp channel, tag 2** — `003B6A10(row, byte+2, {f32+4, f32+8}, 0, 1.0)`; fields `+0x58/+0x5C`, targets `+0x68/+0x6C`. |
| `0x10` | 8 | 136,235 | `004174D0` | **ramp channel, tag 3** — `003B6950(row, byte+2, f32+4)`; field `+0x78`, target `+0x7C`. |
| `0x11` | 4 | 10,617 | →`00520160` | **bone trails on/off** — `obj+0x294 |= 0x1000000`; `byte[cmd+2]` → `obj+0x3D0`. |
| `0x12` | 4 | 32,515 | →`005207C0` | **look-at tracking enable** (`RelationLook_SetTrackingEnabled`) — `003E6DA0(obj)` → `003E29F0(obj2, 4, byte[cmd+2]!=0)`. |
| `0x13` | 6 | 5,805 | →`00520430` | **store + broadcast the controller switch** — gated on `word[obj+0x2F2]==0`; `byte+2&0xB9`→`+0x3F4` (`0x80` rejected), `byte+3`→`+0x3F5`, `word+4` operand; `+0x290` bit 9 + `00429500`. |
| `0x15` | 4 | 1,218 | →`00520740` | **draw/sheathe: re-attach children** — `obj+0x290|=0x800000`; `byte[obj+0x3D1]` bits 0–2 `^=` `byte+2`, bits 3–5 `^=` `byte+3`. |
| `0x16` | 6 | 329 | →`00520BD0` | **bind sub-resource variants** — `byte+2&1`→`+0x3D2`; `word+2>>1`→`+0x3D3`; `word+4`→`+0x3F8`; then `0042B550(obj)` (refresh). |
| `0x18` | 4 | 28,222 | →`00520C80` | **footstep effect** — gated on `00421E20(obj,0,0x100,…)` hit → `003B0C50(s16[obj], byte+2)`. |
| `0x1A` | 4 | 12,876 | →`00520C10` | **move/turn toward the target along a profile** — `00422D50` resolves a sub-object with nonzero `+0x370` → `003E6340(obj2, word+2)`. |
| `0x1D` | 4 | 5,639 | →`00520D30` | **pose-sequencer event** — multi-mode on `byte+2`: `0xFD`→`obj+0x4B7|=0x40`; `0xFF`→ `003E55B0` section `+0xB8=byte+3` + `00477610(dword+0x450)`; `0xFE`→`00428B30(word[obj],1)`; else hi nibble gates `byte+0x413` counter, lo nibble → `003E7450(obj, byte+3, 0, lo)`. |
| `0x1E` | 4 | 0 | →`00520DF0` | nibble-selector sibling of `0x1D` (registered, unauthored). |
| `0x1F` | 4 | 0 | →`00520140` | `003E6710(…, word+2&1)` — flag set (registered, unauthored). |
| `0x20` | 4 | 148 | →`005207A0` | **alias bone `0x107`** — `word[obj+0x2F4] = (word+2 != 0) + 0x303`. |
| `0x21` | 4 | 613 | →`00520780` | **alias bone `0x108`** — `word[obj+0x2F6] = (word+2 != 0) + 0x305`. |
| `0x23` | 10 | 261 | →`00520180` | **fade channel 1** (attached-piece visibility) — `004293C0(1, word+2, f32+4, word+8)`. |
| `0x24` | 12 | 1,493 | →`005201B0` | **ramp a rotator's speed** — child-targeted: `dword[obj+0x18]` resolves via `002ED570` (`−1` = self); `word+6` sign+0x40 arm → `0051A780`; `word+6!=0` → `00519100` name→id lookup; tail `003DFE70(part, word+2, word+4, f32+8)`. |
| `0x25` | 12 | 740 | →`00520320` | **restore the rotator's speed** — same resolution, tail `003DFF20`. |
| `0x26` | 4 | 0 | →`002E7080` | `0026BE90(0,1)` (registered at `002EA4E2`, unauthored). |
| `0x28` | 8 | 115 | →`00520720` | **effect request lane** — `003E6AA0(obj, dword+4)` stores `dword+4` into `obj+0x304` bits 27–31 with dirty bit 27 of `+0x294`; the dirty pass `00427DE0` invokes `003B3C00(handle=[obj+0x288], value)`, which range-checks `value ∈ 0..10` and dispatches `0024FE70(effectCtx, value)` — the authored dword is a **lane index into an 11-entry request map** on the bound effect's definition (`def = [[ctx+0x130]+0x80]`): `byte[def+0xA+lane]` selects `dword[def+0x2C+4·map]` (a resource id), resolved by `0020E600` and spawned into the object's 16-slot child table by `00333280(childObj, id, lane)` (lane stamped at `child+0x11`). Lane 0 = no request. Authored: `{1: 112}` across exactly four monster files (`m1043_10`/`m1044_10`/`m1132_10`/`m1133_10`, blocks `ready`/`knockback_s`/`knockback_l`/`c_turbo`/`ev_walk`/`avoid`), `{10: 3}` in `m1143_10.ca` (`knockback_l` ×2, `dead` ×1) — per-effect authored lanes, not global semantics (`members/fmc_op28_census.py`, FAILS 0). |
| `0x29` | 4 | 47,472 | →`00520D00` | **footstep sound** — `0046CC70(obj+0x5F0, 0, 1, s16+2)`. |
| `0x2A` | 20 | 7,183 | →`005206B0` | **pooled, generation-tagged handle** — `003E7140(obj, s16+2, s16+4, f32+8, f32+0xC, f32+0x10)`. |
| `0x2C` | 10 | 387,789 | `00417DE0` | **blend-in rule by previous motion** (selector/match) — `word+2` vs `state+0x326&0xFFF` (`0xFFFF` default); `s8` pair list at `+7`/`+8` scanned for match/`0xFF`; match advances cursor `+0x32A`. |
| `0x2F` | 4 | 30 | →`00520E30` | **presentation event to the child sub-tree** — deferred post `0042EF90(word[obj+8], cb `00521000`, s16+2|0x2000, obj)`. |
| `0x34` | 8 | 28 | →`00520800` | **character shadow-parameter write** — `byte+2==0xFF` is the global arm: `003AFD30(byte+3!=0)` writes `dword[02B3F554]` and `003B6930(4|6)` rewrites the low 2 bits of `dword[02B3F524]`. Otherwise `003AFC10(dword[obj+0x118])` resolves the object's handle in the shadow-param pool (32 × `0x70` records at `02B3F570`, tag `dword[+4]`) and a compressed jump table dispatches on `byte+2−1`: byte map `u8[00520B50+sel]`→case, dword target `u32[00520B2C+case*4]+0x120000`. The "128-way" table has **8 real cases** — only the power-of-two selectors `1/2/4/8/16/32/64/128` (`byte+2` is a field bitmask, one bit per field) reach code; everything else falls to the `00520B20` return stub. |
| `0x3F` | 18 | 3,108 | →`00520510` | **a directed sway** (op `0x48` is the same command) — deferred event, gated `word[obj+6]==−1`; `00426870(obj, cb `00520E90`, {word+2, word+0x10&0xFFF, bit15, dword+4/+8/+0xC})`. |

So the authored stream is a **motion-event bytecode**: `0x00` begin +
`0x01`/`0x09` track/motion select, `0x0A`+`0x0B` the track selector pair
(selector kinds live in `.data` `01F000A0`; seven of ten are read —
kind `0x10` is a `rand()`-driven countdown, kind `1` a random variant that
can flip to its "evaded" pair, kind `2` a sticky three-way, `0x20`–`0x25`
yaw quadrants; `uq218-fmc-selector-kinds`), the `0x0D`–`0x10` ramp-channel writes into the
`0xE0`-stride param row `02B40528` (`byte+2` = frame count, `0` = snap),
`0x2C` the blend-in rule, `0x05`/`0x06`/`0x0A` bookkeeping, and the
hooked ops gameplay side-effects (bone trails, look-at, draw/sheathe,
footsteps, fades, rotators, deferred posts). The hook-table indirection is
a **subsystem boundary**: `01EFFAF0` entries with `fn = 0016D6A0` or
unregistered `tabA` slots are inert, so the `0x02`/`0x07`/`0x0C`/… stub
slots and hook ops `0x14`/`0x19`/`0x1E`/`0x1F`/`0x26`/`0x48` (registered
but unauthored) are dead lanes.

**The op-`0x34` shadow-param subsystem** (`003AF340`–`003AFDF0`, pool
`02B3F570`): a 32-slot pool of `0x70`-byte records, each tag-validated by
`dword[+4]`. The character object owns a handle at `obj+0x118`
(`(counter<<8)|slot`), mirrored into the resolved visual sub-object at
`+0x360`; `003E73B0` is the mode setter — `obj+0xC0` bits 3–4 hold the
mode, `0` frees the record via `003AFBE0`, `1` allocates via
`003AF340(s16[obj])` which defaults `+0x08/+0x10/+0x14` = `1.0`,
`+0x24..+0x38` = `1.0`, `+0x1C` = `0x11000000`, `+0x18` =
`f32[src+8]/u8[src+0x10]`, `+0x20&0xF1|1`. Record fields: five ramped
channels `{u8 frames; f32 target; f32 rate}` at `{+0x1C,+0x24,+0x2C}`,
`{+0x1D,+0x28,+0x30}`, `{+0x1E,+0x34,+0x38}`, `{+0x54,+0x3C,+0x48}`,
`{+0x55,+0x44,+0x4C}`; mode byte `+0x1F` (low nibble `1|2`, bits 4–5
`0x10|0x20`); `+0x40` f32, `+0x50` f32, `+0x56` u16 size enum
(`0x40/0x80/0x100` quantized on `≤1.5/≤2.5/else`), `+0x58` dirty flags.
`byte+2` of the command is the field bitmask (bits `0/1/2/5/6` = the
ramps, `3`/`4` = the mode nibbles, `7` = a `{1:+0x40, 2:+0x56, 4:+0x50}`
sub-selector); `byte+3` is the ramp frame count (`≤1` snaps the target
and zeroes the countdown, else `rate = (target − current)/frames`);
`dword+4` is the f32 target. Advance: `003AF460` steps every live
record's ramps once per frame from `00426117`; `003AFB30` steps a single
handle's ramps and is called **inside the `@FMC` seek/catch-up paths**
(`0041C8F1`, `0041D9D1` — next to `visualObj+0x360` reads at `0041C8EB`,
`0041D9CB`, `0041DFA8`), so shadow-parameter ramps replay
deterministically under motion seeking exactly like the `0x0D`–`0x10`
`02B40528` channels. Reset helpers `003AFC30`/`003AFC80` restore the
defaults; `003AFCD0` pool-inits.

**The `0x0A`/`0x0B` locomotion classifier** (`004256E0`, selector kinds
`0`/`0xA`/`0xB` — FABLE's `uq218-fmc-selector-kinds` record, re-verified
here against the certified image, `classifier.py` `FAILS 0`): reached
through per-kind forwarding thunks `00422400`/`00422410` with a kind
argument `0`/`1`/`2` (kinds `0`/`0xA`/`0xB` respectively). It reads a
**band index** out of the render record's locomotion state and writes it
to `rec+0x2A0`; the result is `index + ((1 − esi) << 16)` — never `−1`,
and the high half is the track offset the `0x0B` handler adds to the
element ids. Priority: if `003E7D10(rec+0x6A4, 4)` reports a render-pool
override the initial band is `0xE` (remapped to `0xB`/`0xC`/`0xD` by the
kind argument). Below the model-speed threshold `+0x23C`, the last turn
(current facing `+0x124` minus previous facing `+0x254`, wrapped)
classifies: `0` when ~zero or within ±C1, else `6` — or `7` when the model
supports it and the turn reaches the model's turn angle; the selected
track offset carries the turn sign. Between `+0x23C` and `+0x420` it
compares the movement heading `+0x244` against facing: ±45° → `1`,
`(45°,135°]` → `3`, `[−135°,−45°)` → `4`, otherwise `5`. At or above
`+0x420` the default is `2`, replaced by target-bearing bands when view
query `0x1000` reports flag `0x20` and a target resolves (±45° → `2`,
`(45°,135°]` → `0xA`, `[−135°,−45°)` → `9`, else `0xB`); kind arguments
`0`/`2` lower bands `9`–`0xB` by one. Every candidate band is gated on
one of five FCP model-property ids read via `004FE2F0`
(`0x63070F30`/`0x62070E30`/`0x61070D30`/`0x60070C30`/`0x63070B2D` — FCP
section-9 bit-field flags, not motion names) and missing motions fall
back to simpler bands. The frame-limit scalar `01DFE0B4`, turn-angle
scale `01DFE0B8` and the low-speed tolerance `01DFE0BC` (`1.0`/`0.5` at
30/60 fps) modulate the windows. **Authored corroboration:** the `.ca`
`@FMN` band is the character's locomotion set —
`idle`, `walk_f_l`/`walk_f_r`, `run_l`/`run_r`,
`walk_l_l`/`walk_l_r`, `walk_r_l`/`walk_r_r`, `walk_b_l`/`walk_b_r`,
`stp_l`/`stp_r`, `run_l_l`/`run_l_r`, `run_r_l`/`run_r_r` (e.g.
`c1004_23.ca` slots `80`–`96`) — a positional match for the band
families, and each `_l`/`_r` pair is the hi16 track offset's target.
~~Still inference-only: the exact band→name binding and which yaw sign is
the character's left.~~ *(Answered 2026-09-30, pass 18 — the section below.)*

**Selector state record.** Kinds `1`/`2`/`0x10` keep their scratch in the
`0x740`-byte record at `qword[ctx+0x2E0]` — one of `0xA0` pooled records
at `[02B3EF28]` (pool init `004269A0` → `0041F730`: `memset 0x740`, then
`word[+0x40F] = 0xFFFF` so `+0x410` starts undecided; an `ebp = −1` fill
sets `+0x412`/`+0x2AF`/`+0x408`/`+0x24C`/`+0x288`/`+0xC4`/`+0xC8`/`+0x2C4`/
`+0x434` to `0xFF`/`−1`). Kind 1
(`00422420`): `+0x40E` arm timer, `+0x411` drawn variant 0–4
(`003A6E60(5)`; +5 on the `11 × frameLimit` pass if the evaded/absorbed
bit of query `0x20` is set). Kind 2 (`00422500`): `+0x410` sticky choice
(`0xFF` undecided → `0` combo-continue bit 2 / `1` evaded bit 4 / `2`),
`+0x40E` reused as combo-age counter clamped at `3 × frameLimit`. Kind
`0x10` (`004225A0`): `+0x412` rolled-once byte
`((rand % (ctx+0x2DE−ctx+0x2DD+1)) + ctx+0x2DD−1) × frameLimit`. **Resets
(verified):** record init `0041F730` (callers `004269C3`/`00427A13`/
`00429291`) and the `@FMC`-bind site `004252A7` (inside the `00409FA0`/
`00409FD0` `'@FMC'`/`'@FRP'` name-query body) zero `+0x40E` and set
`+0x412 = 0xFF` on every new motion block; `+0x410`/`+0x411` have no
external writer — a decided kind-2 stick survives a rebind until the
record is re-initialised.

**Binding:** `0041D2DF`–`0041D30E` in the presentation-entry init resolves
`@FMC` → `entry+0x320` through `00409A30(obj, '@FMC', entry+0x2EC)` — the
third argument is the name key the multi-entry `@FMC` set is matched on —
falling back to `@FRP` on `-1` (`0041D301`). The FCP page records how this is
selected: `fcp +0x2FA` is the first-`@FMC` index and the event map picks
`firstFMC + i` of the model's own `@FMC` set, started through `00423B10`
(`fcp-character-parameter-block.md`).

`00423B10(rbx = motion request, rdx = ctx, esi = motion index)` is the starter:
it gates on `ctx+0x284 & 0x8000000`, resolves `word[req+8]` as an index into
the render-record array `022C6F28` (stride `0x740` — the UQ-196 array), walks
the descriptor chain at `+0xA`, resolves each descriptor's resource id at
`+0x68` through `0020E600`, recurses, and on the follow-on at `+0xC4` reaches
`rax+0xDA8 → 0051B9E0` to set `+0xC |= 2`, `word[+0x24] = 1`.

### `@FMN` — the motion name record (`.cm`, `111`; `.ca`, `18,303`)

Header `{'@FMN', kind 0x02001111, entryLen, u32 +0x0C = tail record count}` —
`0x02001111` is constant in all `.cm` entries. Two `char[0x20]` names: `+0x10`
the motion slot name (`idle00`, `shot_f_m0`, `ded0`,
`CreateStartPoseDammyActFile*`…), `+0x30` a second name (`idle0` —
truncated/derived form). `+0x50` u32 pair (`0x1E`/`0x134` in w2601), `+0x60`
four f32s — `0.349`, `0.349`, `1.047`, `1.047` rad (20°/60° pairs) in the
sampled weapon — zeros to `+0xF0`, then the per-node channel-record stream.
Lengths `0x124`–`0x194` (`.cm`; `.ca` entries reach `0x654`+).

**Binding:** the motion-descriptor init `0041BEE0` resolves `@FMN` →
`desc+0x54`, falling back to `@FRP` on `-1` (`0041C003`).

**Resolution (`0041B4E0`, verified):** `desc+0x50` (u16) = the `@FMN` resource
index resolved by `00409F50`; `desc+0x54` = the section index within it
(`004096C0`); `desc+0x5C` (s16) = the entry index (`00408F80`) → `desc+0x70` =
the `@FMN` entry pointer. `@FMW` uses the parallel `desc+0x52`/`+0x58` pair but
always index `0` (`0041B52F`) → `desc+0x78`. The descriptor's container pointer
is `desc+0x48`; `+0x50 == -1` skips resolution entirely (`0041B53D`).

**Tail grammar (executor-proven).** The stream walker is `0041C040`–`0041C1D9`;
its stream base comes from the kind-bits switch `00409190` — for kind
`0x02001111` the base is `+0xF0` (other kinds select `+0x40`/`+0x60`/`+0x70`/
`+0x90`/`+0xC0`; none occur in the corpus). `u32 +0x0C` = record count
(`.cm`: {2: 25, 3: 15, 5: 71}; `.ca`: up to 40+). Each record is 22 bytes:

```text
u16 nodeKey                                   — resolved by 00370E00 to the
                                                bone/node index
u16 packed { chMask:9, byteLen:6, flag:1 }    — advance = byteLen (always 22;
                                                flag always 0 corpus-wide)
u16 chIdx[9]                                  — one slot per channel 0..8
```

Per record the walker calls `0041B550` with the nine `chIdx` words; mask bit
`i` set ⟺ `chIdx[i] < 0x8000` (a real `@FMW` channel-row index); cleared bits
carry `0x8000|n` (absent marker). Active channels are initialised through the
`0x1C`-byte runtime channel rows (`0041B650` arm dispatch into `@FMW`).
`word[+0x50]` feeds duration state `+0x16`/`+0x18` plus normalised phase
`+0x1C` in the same loop.

Corpus: **746,142 records** across `.ca` + `.cm` (668,500 inside the v1 slot
scan) — every record `byteLen = 22`, flag `0`, **zero** mask↔`0x8000`
mismatches, **zero** stream overruns (checks `fmn-tail-grammar`,
`fmn-tail-adv22`, `fmn-tail-mask-vs-8000`, `fmn-tail-ca-count`).

**Verified fields:**

- `f32 +0x60`..`+0x6F` — a **corpus-uniform constant block**: all 111 `.cm`
  records carry `{20°, 20°, 60°, 60°}` in radians (two bit-variants of
  `π/9`/`π/3` only — census check `fmn-f60-clamp-const`). Consumer proven:
  `004182E3`–`004183B2` (the `dword[entry+4] & 3 == 1` arm of the @FMN/@FRP
  applier) feeds `{+0x60,+0x64}` → `003E3460` → node `+0x28` and
  `{+0x6C,+0x68}` → `003E3590` → node `+0x20`, both on the
  `dword[obj+0x338]`/`+0x330`-resolved node (`r15+0x94` → `0020E600`) —
  clamp-limit pairs. Same arm consumes `+0x70` (vec2 → `003E2EA0`, count 2),
  `{+0xA4,+0xA0}`/`dword+0xA8` → `003B5CE0` into the `0xE0`-stride global
  `02B40528` keyed by `dword[obj+0x35C]`, and `byte+0xEE` (bit7 →
  `obj+0x66D` flag; `&7` → `003E2D20` → node `+6` byte).
- **The `kind & 3` layout split (proven 2026-09-28):** `00418173` tests
  `dword[entry+4] & 0x3000000 == 0x02000000`, then `004182F8` splits on
  `dword[entry+4] & 3`. All 20,207 shipped `@FMN` entries are `&3 == 1` and
  **zero `@FRP` entries exist** in `.cm`/`.ca` — the `&3 == 0` arm
  (`+0x30`/`+0x34`/`+0x38`/`+0x3C` as two f32 pairs → `003E3460`/`003E3590`,
  `+0x40` vec2 → `003E2EA0`, `byte+0xBE` flag) reads the *same logical fields
  at different offsets* — an alternate entry layout (the `@FRP` fallback
  family), never exercised by shipped `@FMN` data. The `+0x30` f32 reads are
  therefore **not** a second-name consumer; they are arm-0 layout reads.
- `u32 +0x50` pair — **both fields ruled 2026-09-28.** First word is the
  duration consumed by the walker (`movzx word[r14+0x50]` at `0041C18A` →
  state `+0x16`, mirrored to `+0x18` unless flag `0x40`) and equals `u8[0]`
  of every `@FMW` channel descriptor (15,037/15,037 channel-bearing pairs).
  `u32 +0x54` is the **post-record block offset** — equals `0xF0 +
  nrec*22` (10,628 entries) or `+2` with a pad u16 (9,579); the block at
  `entry+f54` is a per-channel f32 stream (`{0.0, 1.0, ∓π/2, 0.0667…}` —
  rest/default values). Its sole reader `0041B5B9` (`cmp dword[rdx+0x54],0`
  inside `0041B550`, rdx = `@FMN` per `0041C10B`) selects between **two
  identical arms** — a vestigial gate: the field is authored but
  behaviorally dead, and no code indexes into the f32 block it names.
- `nodeKey` resolution is proven: `00370E00` (gated on `dword[ctx+0x9C]==2`)
  tail-jumps `00373540`, which resolves `ctx+0xA0` via `0020E600` and walks a
  global 12-byte-entry linked registry at `01EF9438`, comparing each entry's
  key u16 (`00409250`) to `nodeKey`, requiring flag `0x100`, **unlinking** the
  matched node (claiming it off the list) and returning its index. The
  `≥0x800` `nodeKey` domain (~239k records) is the larger key space of that
  registry. In the apply path the field is consumed directly: `0041947A`
  computes `node = nodeBase + nodeKey*0x290` — a plain index into the
  0x290-stride node-object array.
- The second name at `+0x30` (`idle0`, `ev_rlx_door`, `sp2` — a truncated
  form of the `+0x10` name) has **no shipped-code reader found**: the only
  `+0x30` accesses in the applier are the arm-0 f32 reads above, which never
  fire on `&3==1` entries. Treat it as authored metadata (a short alias)
  until a consumer appears.

### `@FMW` — the track-data record (`.cm`, `111`; `.ca`, `18,303`)

Header `{'@FMW', kind 0, entryLen, u32 +0x0C = 0}`, `char[0x10]` name at `+0x10`
(only half the name field — the u16 stream starts at `+0x20`). Exactly `1:1`
with `@FMN`. Bound to `desc+0x58` in `0041BEE0` (`0041C01F`); `0041B4E0`
resolves `desc+0x78` = the `@FMW` entry pointer (index `0` of section
`desc+0x58`).

**Verified fields** (`0041B650` reads them directly):

- `u32 +0x30` — base offset of the track data inside the entry (corpus:
  `{0x40, 0x8C, 0xA0, 0x64, 0xC8, 0x138}`; `0x40` for 66/111). For arm `1` it is
  the flag-tagged byte stream; for arm `0` the table head.
- `u32 +0x34` — **format arm** selected by `0041B650`'s first branch.
  Corpus-verified over the full extract: `.cm` `{1: 110, 0: 1}` (the sole
  `.cm` arm-`0` is `treasure/t0006.cm` at `0xC0C0`, `0x644` bytes) and `.ca`
  `{1: 17,576, 0: 727}` — arm `0` is a common `.ca` authoring, not a one-off
  (arm0_census.py). The arms are storage variants, not motion parameters.
- `u32 +0x40` — channel-track offset table: `0041B650` resolves it via
  `00409150` (u32 table, arm `0`) or `00409170` (u16 table, arm `1`), then
  indexes per channel.

**Arm `1` (packed stream, `110/111`) — fully decoded.** `00409170` resolves the
u16 table at `+0x40` (`dword +0x0C` = channel count, `0x44` = 68 in c1004_00):
entry `chIdx` gives the entry-relative offset of a channel descriptor —
`{u8 frameCount, u8 streamCount cnt, u16, u32[cnt] delta-stream base offsets,
then {u32 litOff&0x1FFFF | hi flag bits, f32 bias, f32 scale} per key}` —
0x14 stride when cnt=1 & 1 key. `frameCount` equals the paired `@FMN`'s
`word+0x50` duration in all 15,037 channel-bearing `.ca` pairs (the 779
exceptions are empty `@FMW` tables — static poses). `0041B650`
then walks flag bytes at `fmw + dword[+0x30] + litOff + cursor`: `0x80` = s16
**little-endian** literal (`byte[p+2]<<8 | byte[p+1]`, `0041B7C6`/`0041B7D3`),
`0x40` = repeat last value, else s8 literal. The literal is
denormalized `lit*scale + bias` → runtime slot `+0x8`; a second read at the
advanced cursor yields the next-key value as `lit2*scale + +0x8` → slot `+0xC`
(the lerp pair); a delta stream (offsets = the leading `cnt` u32s selected by
slot byte `+0x13`) accumulates s16 deltas into `word[+0x4]/+0x6`.

**Arm `0` (run tables, `727` `.ca` + `1` `.cm`):** the descriptor head is
`{u32 frameCount (bit 31 = extended), u32 nA, u32 nB [, u32 nC + nC×0x1C
records]}`, then two run-record arrays (FABLE `uq218-residue-fable` §2 — the
codec is pinned at `0041B412`/`0041B41F`; the record shapes are a read
attribution): A records (8 B) `{u32 streamOff, u16, u16 keyCount}` are the
**frame runs** (`frame += lit` from `0`); B records (16 B) `{u32 streamOff,
u16, u16 keyCount, f32 bias, f32 scale}` are the **value runs** (`v0 =
bias + lit·scale`, then `v += lit·scale`). Both decode with the same flag-byte
codec (low 6 bits = run length, `0x80` = s16 little-endian literals, `0x40` =
repeat). `00409150` resolves u32 offsets to the element tables consumed by the
interpolators `0041B3A0` / `0041B920` / `0041BB00` / `0041B460`; a descriptor
dword `>= 0x80000000` selects the extended/indirection form (`+0x4`/`+0xC`
recompute the element base). Corpus control (subagent, not re-run): every
frame run starts at `0`, ends at `frameCount − 1`, strictly increasing;
`nA == nB` on 50,768 inline / 19,673 extended channels.

The extended head is `{u32 frameCount|0x80000000, u32 nA, u32 nB, u32 nC}`,
then `nA`×8B A records at `+0x10`, then `nC`×0x1C records, then the B array
at `+0x10 + nC·0x1C + nA·8` — the identical address expression in
`0041B3C3`/`0041B474`/`0041B920`'s twin/`0041BB00` and the `0041B6C4` init
site in `0041B650`. Every shipped extended descriptor has `nA == nB == nC == 1`
(6,200/6,200 sampled over `.ca`), so the `0x1C` block is a fixed per-channel
extension record in practice, not a variable array. All five `00409150`
consumers are enumerated and none reads the record's fields: the four
interpolators and init only scale `nC·0x1C` to skip it, and the fifth
(`0041D945`, inside `0041D820`) reads only bit 31 — it scans each desc row's
channel descriptors (rows whose `@FMW` has `+0x34 != 1`) and sets a flag
that selects the `0041C850` replay path, where `0041ADA0` derives the frame
position modulo `dword[entry+0x50]` duration instead of the straight
`state+0xC` read. Bit 31 therefore means "this motion's event timeline
replays through the wrap-aware path" — a presence flag, not a pointer to
data the runtime reads. The 0x1C record itself is stable across the corpus
(`{u32 ~6 (98%), f32, u16{0,N} twice, u32 ~2, u16{1,M}, u16{6,7}}`) and has
no shipped-code consumer — authored metadata, dead in this runtime.

**Node stream consumption (`0041B550`):** the `@FMN` tail records (above) are
the source; `0041B550` receives each record's nine `chIdx` words and iterates
the nine channel slots — each active index selects one `0x1C`-byte runtime
channel slot at `nodeRow + i*0x1C` (i = 0..8), initialised via `0041B650`
against the `@FMW` track data. Runtime node-row layout proven by the callee:
`word[+0x100]` = the record's `nodeKey`, `word[+0x102]` = active-channel
bitmap (`0x80<<i`), `dword[+0xFC]` = the record's container-relative offset;
inactive slots get `word[slot+4]=0xFFFF`, `qword[slot+8]=0`. Per slot:
`word[slot+0]` = authored `chIdx`, `word[+0x4]` = current key frame,
`word[+0x6]` = next key frame (the delta stream accumulates s16 frame deltas
into `+0x6`), `f32 +0x8` = current key value, `f32 +0xC` = next-key value (lerp
pair), `word[+0x10]`/`dword[+0x12]`/`word[+0x16]`/`u8 +0x18`/`u8 +0x19` =
stream cursors and key index. The walker `0041C040`–`0041C1D9` is gated on
`container+0x54` (`@FMN`); `0041C260`'s snapshot arm copies the eight dwords
`row+0xF0..0x10C` to `+0x130..+0x14C`.

**Apply path — the channel→component map (executor-proven).** The per-frame
sampler `0041A470(slot, @FMW, frame)` advances the key cursors
(`while word[+6] <= frame`: cur = next, then decodes the next frame delta and
the next value delta `lit*scale + cur`) and returns the linear sample
`+0x8 + (frame - word+4)/(word+6 - word+4) * (+0xC - +0x8)` (zero span → cur).
`0041BDC0` is the re-seek twin — re-walks each row's record
(`dword[row+0xFC]`) and re-decodes active channels, gated on
`(@FMN kind >> 4) & 3 == 1`. The driver (body spans `004193xx`–`0041A46B`)
iterates the owner's node-row table — `dword[owner+0x2B8]` resolved through
`003AB7F0` on `[owner+0x2B0]`, `word[owner+0x2BC]` rows of stride `0x108` —
and for each row computes `node = nodeBase + nodeKey*0x290` (`imul` at
`0041947A`: **`nodeKey` is a direct index into the 0x290-stride node-object
array**, matching `00373540`'s returned index domain). Channels apply in
three vec3 groups, gated by the row bitmap (`0x80<<i`):

| channels | staging vec4 | consumer | semantic |
|----------|--------------|----------|----------|
| `0-2` | `node+0x190` | `0046D380(x,y,z)` → LUT `01F004E0` (0x8000 entries/rev, `idx-0x2000` = cos) builds a 3×3 | **Euler XYZ rotation, radians** → node matrix `+0xC0..` |
| `3-5` | `node+0x1B0` | copied vec4 → `node+0xF0` | **translation XYZ** — row 3 of the local 4×4 at `+0xC0..0xFF` |
| `6-8` | `node+0x1D0` | copied vec4 → `node+0x100` | **scale XYZ** — vec4 past the matrix; writes suppressed when `byte[node+0x280] & 2` |

Writes replicate down the object's `+0x278` chain (`0020E600` walk) — each
linked sibling receives the same value. Group-written bits (`1`=rot, `2`=trans,
`4`=scale) then gate the copy-back into the matrix, and `word[node+0x280] |=
0x10` marks the node dirty when the state flag `+0x96 & 0x20` is set.
`00418650`/`004186A0`/`00418700` are the same three group stores factored as
leaf setters (`f32[obj + nodeKey*0x10 + chIdx*4 + {0x190,0x1B0,0x1D0}]`).

**`+0x100` downstream read.** The bone's scale vec4 is consumed by the
final-pose composer `00373860` (sole caller `003705BA`; the `0x290` records are
skeleton bones): unless `byte[bone+0x280]` has bit `0x10`, `&bone+0x100` (`lea
r9` at `00373B58`) feeds `00372610` (call `00373B85`), which scales the pose's
rows by the vec4 through four `00202FE0` calls. With bit `0x10` set the vec4 is
first multiplied component-wise by `bone+0x1E0`. The bone's `+0x80` matrix
carries the **unscaled** pose — children take `+0x80` as parent, so scale does
not inherit down the hierarchy; only the bone's own final matrix (copied via
the handle at `+0x284`) carries it. A second pass `003703A0` additionally
scales rows 0–2 of `+0x80` into the **skinning palette** — `renderRecord
+0x6C0`, a `boneCount`×0x40 heap array lazily allocated by
`0019C580(0x12, 0, count*0x40)` (`word[part+0x8A]` = the bone count): each
record is `{4 vec4 rows — the part's `+0x150` bind matrix composed with the
bone's `+0x80` pose via `00202D60`/`00202D70`, rows scaled by the `+0x100`
vec4 via three `00202FE0` calls, translation row at `+0x30`, then
`i32 +0x3C` = the bone's parent index (`word[bone+0x270]`, −1 for the
root)}`. The consumer chain is now read: `+0x6B8` holds a device-created
skinning object (`0017F0D0` → `001BD4A0` on the global render-device
singleton `01F81248`, gated by `0017EFC0(dword[+0x6B0])`), `+0x6D0` a
`count*4` buffer linked to it by `0017EF60`; at `0053B209` inside the
`0053B2xx` draw builder the thunk `0017F260` calls
`skinObj->vtbl[0xD0] (palette = rec+0x6C0, boneCount = word[part+0x8A])` —
the palette upload for GPU skinning (FABLE `uq218-residue-fable` S —
composer/reader pinned; the non-inheritance and `+0x1E0`/`+0x6C0` details
are read attribution).

### `@FRM` — the motion resource (`.ca` only, `3,164` = one per file)

Header `{'@FRM', kind 0, entryLen, u32 +0x0C = 1}`, `char[0x20]` name at
`+0x10` == file basename (`s0031_00`…) in all `3,164`. Payload head at `+0x30`
is a u32 offset list — `s0031_00`: `{0x100, 0x20, 0x40, 0xA0}`;
`s0031_10_4005`: `{0x1701, 0, 0, 0}` — pointing into the entry. Lengths
`0x110`–`0x8B0` (`0x170` modal, `1,453`).

**Binding:** `0041D31F`–`0041D36E` (same init, right after `@FMC`): finds the
`@FRM` section via `00409660`, requires `dword[sectionRec+8] > 0x30` (the entry
must exceed its own header), then `entry+0x378` = `@FRM` index `+0x30` (payload
head) and `entry+0x37C` = that `+ dword[sectRec+0x38]` (a second region inside
the entry). The surrounding `{u16 tag, u32 idx}` sub-record at `entry+0x2EC`
follows the `00504E70` convention. `@FRM` is what `.cm` models reference
indirectly through their `.ca` companions — it never appears in `.cm`
(`0/1,066`, census check `frm-not-in-cm`).

**Consumer hand-off (verified):** in the motion-start path under `00423B10`,
`00423E51`/`00423E7C` read `dword[entry+0x37C]` (the second `@FRM` region
offset) into the request object at `+0xE8` on the found branch and `+0x100` on
the `-1` branch, then `0020E600` resolves `dword[req+0xD8]` — the two bound
regions are handed to the request, not parsed here.

## UQ-218 pass 18 — band names, the yaw sign and the `@FEF` companion (SWE2-DATA, 2026-09-30)

*[Record](../../_index/candidates/uq218-pass18-0930/README.md); `band_names.py`, `fef_tables.py`, `for_tail_census.py`, all FAILS 0, static.*

**The band → `@FMN` binding is a code path.** Op `0x0B` (`00417110`) turns the classifier's result into list index
`i = result & 0xFFFF` and track offset `h = result >> 16`, and plays track `list[i] + h` (`00417281`, `0041727D`,
`0041735C`, `00417367`). A track is a **record index inside the bound `@FMC` entry** (`0041CD30` walks the records and
stamps the index at `0041CDC8`), and that record's op `0x09` names the `@FMN` (index `word[cmd+2] >> 1`; all 33,753
indexes on these paths land on an `@FMN` slot). Over 1,489 authored kind-`0`/`0xA`/`0xB` selectors: band 1 → `walk_f`,
2 → `run`, 3 → `walk_l_*`, 4 → `walk_r_*`, 5 → `walk_b_*`, 6 → `trn_l`/`trn_r`, 7 → `hi_trn_*`, 8 → `stp_*` (kind `0xA`),
9 → `run_l_*`, 10 → `run_r_*`, 11 → `run`, 12 → `sleep` (kinds `0`/`0xB` renumbered as the classifier paragraph says;
models without a motion repeat a simpler one, e.g. `walk_f` in the side slots). The offset `h` is the start foot
(`_l` / `_r` variant).

**The yaw sign: positive is left.** heading − facing in (45°, 135°] (`004258C6`, band 3) binds `walk_l_*` 287 / 281 times
and `walk_r_*` never; [−135°, −45°) (band 4) the reverse. A non-negative turn (`0042576B`, `0042588F`) plays `trn_l`
(226, `trn_r` 0) and a negative one `trn_r`. This agrees with the `(sin yaw, cos yaw)` step on X / Z in a right-handed
Y-up frame. The target-bearing arm maps (45°, 135°] to `run_r_*`; what that looks like against the target is not
claimed.

**The `@FEF` arm appends and instances a companion effect.** `0019FFD0` seeds the `AsyncLoadManager` (`01F81160`)
table at `+0x228` with 144 paths keyed by class letter and four digits (`001A09E0`), every one
`PS2Data\effect_finish\jp\chara\hNNNN.efx` (125 distinct; the 126th shipped file `h0000.efx` is not named). The file
layer appends the companion after the model and stores the model's length in the buffer's last dword (`001A0CF0`,
`001A0E50`, `001A0F4E`). `00409FE0` then instances the effect from that offset (`0040A16F`, `003B38B0`), looks the
row's path up again (`001D6EC0`), and records `NNNN` from `chara\h%d.efx` (`strstr`, `sscanf`) at the effect record
`+0x30` (`003B3B10`, `003B3B2C`). All 144 `02B64380` rows key a companion and every model and companion ships, so the
arm runs on the load completion (`0041E580`) of each of the 144 `@FEF` models; which a session loads is content.
`003B33D0(handle)` returns that number (callers `0024D140`, `0024D330`; the latter tests the current type-3 effect for
number `0x34`).

## DD batch 10: op 0x12's write and the residue list brought current (SWE2-CONTRACT for OPUS)

*For the player:* the motion command that switches a character's look-at tracking on or off flips a single bit on
the look record. The checks are in
[`b10_checks.py`](../../_index/candidates/swe2contract-ddres-b10-0930/b10_checks.py) (M1), static.

The residue list below, item by item:
- **`0x12`: answered (M1).** `005207C0` calls `003E29F0(obj, 4, byte[cmd+2] != 0)`, and the kind-4 arm writes bit 7
  of the look record's `+0x1C`. Its reader is not traced here. *(2026-09-30, OPUS, [`opus-look-bit7-0930`](../../_index/candidates/opus-look-bit7-0930/README.md) L1-L4: there is none - the only bit-7 test covering `+0x1C` in the image, `002698AC`, is on an actor record, and no byte load of `+0x1C` feeds a bit-7 operation; the bit's other writer is `0041DD40`.)*
- **The `02B64380` note in the `+0x44` bullet was stale.** It is struck, because the first bullet and pass 18 resolve
  it.
- **The falsification pass's two open bullets.** The `001D6EC0` question is answered by pass 18. Reachability is
  runtime-only: every `@FEF` model's load completion runs the arm, and which models a session loads is content.
- **Still open, and not guessed here.**
  - ~~The embedded `EFX0010`'s remainder (a reader through a copied pointer, or a `003EDAD0`-dispatched use).~~
    *Corrected 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 14)*: answered by the batch-14 section below (A1–A9). Neither route exists.
  - What the target-bearing arm's `run_r_*` looks like against the target, which is a visual question.

  Both are listed in the batch record, the first as a proposed register row and the second as runtime-only.
  *(The first is answered by DD batch 14, below.)*

| claim | evidence | tier |
|---|---|---|
| op `0x12` sets bit 7 of the look record's `+0x1C` | M1 | 1 |

## DD batch 14: the embedded payload's last two routes are closed (SWE2-CONTRACT for OPUS)

*For the player:* the effect stored inside a model file is never shown. What appears on a summon or a monster is the
separate `chara\hNNNN.efx` file the loader adds after the model. *For a modder:* editing the embedded copy changes
nothing in game.

The checks are in [`b14_checks.py`](../../_index/candidates/swe2contract-ddres-b14-0930/b14_checks.py) (A1–A9). They are static, plus the extract's 144 `@FEF` models
and the archive.

**No copied pointer (A1, A9).**
- `00504940` stores the entry pointer at its record's `+0x230` (`005049A7`). It forms the `+0x30` pointer only in a
  register and passes it only to `0016D6A0`, which is `ret 0`.
- So a copy needs a read of `+0x230`. The record is a 0x260-byte entry of the model pool (`00477EE0`).
- A census followed every source of such a record, three calls deep: the getters `004780B0`, `003E55B0` and
  `0041E590` at every call site, the creation in `004780C0`, and the binder's callback `00478270`.
- It finds `+0x230` written once (`005049A7`) and read nowhere. Its two other hits are loop aliases: `005049E0`'s
  twenty-dword reset from `+0x194`, and `00504BC0`'s sixteen-dword read from `+0x140`. No record pointer escapes to
  memory on those routes.
- Control: the same census finds batch 10's three readers of `+0x218` / `+0x21C`: `005044D0`, `00504D30` and
  `0053AB50`. It finds them only because the census lets `__chkstk` (`00808F10`) keep the argument registers.

**No `003EDAD0` use (A2–A8).** `003EDAD0` has six direct call sites, no rip reference and no pointer in data. Each
caller's pointer was traced to where it comes from:

| caller | the pointer it passes | source |
|---|---|---|
| `0026FB90` | `r14 + 0x10`, the blobs of a parsed `.efb` | the mode-1 `.efb` block |
| `002FC4A0` | `[01FD4A30]` | a fixed boot block (`0022A240`, 0x3000100 bytes) that file loads fill (`002FC860`) |
| `003B0660` | `[01FD4A30]` (loaded at `003B06F8`, not its argument) | the same block, filled with namespace 10's `c_all.efx` |
| `003B2220` | `[entry + 0x28]` of the table `02EBE5E0` | `003B2310` stores `[01FD4A30]` there and fills it from namespace 12; the field's other writers store 0 or move whole entries |
| `003B29B0` (from `00558FB0`, `00561390`, `00572E10`) | the `0057A2D0` result | a fresh block loaded from namespace 7: `m_all.efx`, `m_all2.efx`, `m_all3.efx` |
| `003B38B0` (from `00409FE0`) | model base + the dword at the model buffer's end | the companion `.efx` the file layer appends after the model (`001A0E1B`, `001A0F4E`) |

- None of the six sources is an `@FEF` entry, and none reads `+0x230`.
- In all 144 `@FEF` models the embedded payload lies below the model's length, so it is never the appended companion.
- Namespace 12 also names 18 `.cm` files, and 17 of them ship. Each starts `@FRP`, and `003EDAD0` tests the EFX magic
  first, so such a file loaded into `[01FD4A30]` is refused at its first byte.

So the embedded `EFX0010` reaches only the `ret 0` stub. No register row is needed.

| claim | evidence | tier |
|---|---|---|
| the `+0x30` pointer goes only to the stub; `+0x230` is never read on any followed route | A1, A9 (census with control) | 1 |
| `003EDAD0`'s six callers pass no `@FEF` entry | A2–A8 | 1 |

## Evidence list

- Disassembled from the authority image: `00504940` (`00504A0`), `0016D6A0`,
  `0041E580`, `00409FE0` (`0040A1C0`), `003B38B0` → `003EDAD0` (EFX version
  dispatch, per the EFX page), `0041BEE0` (`0041C100`), `0041B4E0`, `0041B550`,
  `0041B650`, `0041C260`, `0041D2C5`–`0041D374`, `00423B10` (`00423C80`),
  `00423E51`/`00423E7C`, plus resolvers `00409F50` / `004096C0` / `00408F80` /
  `00409150` / `00409170` / `0020E600`; apply path `0041A470` (sampler),
  `0041BDC0` (re-seek), the `004193xx`–`0041A46B` driver, setters
  `00418650`/`004186A0`/`00418700`, `0046D380` (Euler→3×3 via the `01F004E0`
  sin/cos LUT), `0046D350`/`0046D730`/`00476F40`/`00477130` (matrix compose).
- Archive census `members/fef_motion_entry_census.py`: `FF12_VBF=<vbf> python
  fef_motion_entry_census.py` — 12 checks, `FAILS 0` on the shipping archive.
- FABLE's evidence record:
  [`../../_index/candidates/uq218-cm-entry-residues/`](../../_index/candidates/uq218-cm-entry-residues/)
  — the `00504940`/`0016D6A0` stub finding, the `02B64380` letter+number index,
  the `chara\h%d.efx` strings and the 143/144 non-join were re-verified against
  the image above.

## Residue — what was not claimed

- **`02B64380` rows** — **resolved**: rows are `char*` resource-path strings
  (`PS2Data\obj_finish\in\{gadget,monster,npc,summon}\…\<stem>.cm`), stored at
  `fold(stem)` by the init routine `0040A230` (144 `lea`/`mov`
  pairs in a `.pdata` gap, ~~unreferenced — shipped rows stay `NULL`~~ **called at start-up through `00409F80`,
  CON-195**). The
  `00409FE0` arm is ~~therefore vestigial~~ **not shown vestigial by this (CON-195)**: it treats the row as a non-null gate
  and a name passed to `001D6EC0`, while the real payload offset comes from
  `dword[r14 + roundup64(002DF960(class,num)) − 4]` — the loaded resource's
  own tail dword. `002DF960` is a size lookup `u32[02EC3EE0 + class·0x1388 +
  num]`, not a blob sizer. Residual: whether any shipped load path still
  reaches the `@FEF` arm ~~(it would fault on the zero table — evidence says
  none does)~~ **(the table is seeded at start-up, CON-195, so reaching it with a seeded name does not fault;
  reachability in a shipped session is not observed)**. **Resolved 2026-09-30 (pass 18, below):** `001D6EC0` looks the row's
  path up in the `AsyncLoadManager` companion table, whose 144 seeded entries name `effect_finish\jp\chara\hNNNN.efx`;
  the file layer appends that companion to the model, and the arm instances it and records `NNNN`.
- **The embedded `EFX0010` payload's fate** — closed by FABLE's image-wide
  sweep (`uq218-embedded-efx-sweep`, FAILS 0): no consumer beyond the `ret 0`
  stub exists among direct/jcc/thunk/rip/data edges, the `@FEF` tag sites are
  exactly the three named, and no `.pdata` body reads `rec+0x230` with the
  render record's shape. ~~Not excluded: a copied-pointer reader or a
  `003EDAD0`-dispatched use — a bounded remainder, not a live lead.~~ *Corrected 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 14)*: both are excluded
  (A1–A9, the batch-14 section).
- **`@FMC` per-opcode operand semantics — mapped**: all `33` authored ops
  have handler-level operand reads on file (table above) plus semantic
  names crosswalked to the handler/ramp/fade pages. The sub-record `key`
  domain is **resolved** — keys are frame indices (`key ≤ int(f32
  state+0xC)` fires, cursor `+0x8C` persistent; `0xFFFF` is a lead
  per-tick init sub — op `0x01`/`0x0A`+`0x0B` — dispatched every tick via
  `state+0x90`, never an end marker). The `0x0B` locomotion classifier
  `004256E0` (kinds `0`/`0xA`/`0xB`) is **resolved** — geometry,
  availability gating and fallback verified (`classifier.py` FAILS 0),
  paragraph above. ~~Open: which yaw sign is the character's left, the
  exact band→`@FMN`-name binding (positional inference from the `.ca`
  locomotion set)~~ **both answered 2026-09-30 (pass 18, below)**; kind-1/2/`0x10` state bytes resolved — the `0x740`
  state record, its two reset sites and the full `00422420`/`00422500`/
  `004225A0` bodies are folded in the selector paragraph above; ~~`0x12` beyond
  name/callees.~~ *Corrected 2026-09-30 (SWE2-CONTRACT, DD batch 10, M1): `0x12`'s write is read. `005207C0`
  resolves the look object through `003E6DA0` and calls `003E29F0(obj, 4, byte[cmd+2] != 0)`. That function's kind-4
  arm stores the flag into bit 7 of the look record's byte `+0x1C` and leaves the other seven bits alone
  (`003E2A45`–`003E2A56`). Who reads that bit is not traced here.* (`0x28` is **resolved to mechanism** — the authored
  dword is a lane index `0..10` into the bound effect's request map
  `byte[def+0xA+lane]`→`dword[def+0x2C+4·map]`, id resolved via
  `0020E600` and spawned by `00333280`; lanes `1`/`10` are per-effect
  authored ports, not global semantics.)
  (`0x34`'s jump table is decoded — the "128-way" dispatch is a bitmask
  decoder into 8 field cases of the shadow-param record, above.)
- ~~**`@FMN` u16 tail**~~ — **resolved**: the `+0xF0` stream is a per-node
  channel-assignment table — `{u16 nodeKey, u16 {chMask:9, byteLen:6, flag:1},
  u16 chIdx[9]}`, walked by `0041C040`–`0041C1D9` into `0041B550`;
  `u32 +0x0C` = record count, `byteLen` always 22, mask bit `i` ⟺
  `chIdx[i] < 0x8000` (668,500+ records, zero violations). The `+0x30`
  second name (no shipped reader) and `+0x54` post-block offset (dead
  gate) are both ruled unshipped-authored — `@FMN` is fully dispositioned.
- ~~**`@FMW` channel→component map**~~ — **resolved** (apply path, above):
  slots `0-2`/`3-5`/`6-8` are Euler-XYZ rotation (radians), translation XYZ
  and scale XYZ respectively, staged at node `+0x190`/`+0x1B0`/`+0x1D0` and
  composed into the node's 4×4 (`+0xC0`, trans row `+0xF0`, scale `+0x100`).
  `nodeKey` is a direct `0x290`-array index; `+0x100` is read by the
  final-pose composer `00373860`→`00372610` (above). The arm-`0` run-table
  layout is read (above), including the extended form — the `0x1C` record
  is a fixed per-channel extension block (`nC == 1` throughout the corpus)
  with no shipped-code field consumer; only its presence (bit 31) selects
  the `0041C850` wrap-aware replay. `renderRecord+0x6C0` is also resolved
  — the skinning palette `{4 vec4 scaled rows + i32 parent index}`
  consumed by `skinObj->vtbl[0xD0]` at `0053B209` (above).
- ~~**`.ca` variant-1 slot-table semantics**~~ — **resolved** including
  provenance: `+0x31C` = the bound render event (motion slot), `+0x31A` =
  the actor's standard-motion variation (`stdmotionvariation`/unit def →
  actor `+0x14F` bits 3–7 → `render+0x413`), copied by `0041D220` from the
  `0051BA80` admission descriptor; neither is authored in the `.ca`.
- ~~**`+0x44` handle consumers and `0041E580`'s four caller bodies**~~ —
  **resolved** (above): the four spawn sites are load-completion callbacks,
  and the ticket has five readers including `003B3550` building the
  character render object. ~~`02B64380` row meaning stays open (first bullet).~~ *Corrected 2026-09-30
  (SWE2-CONTRACT, DD batch 10): the first bullet resolves it. The rows are the seeded `obj_finish` paths, and pass 18
  reads what the arm does with them.*

`0041C260` (309 B) is the row-snapshot arm `0041BEE0` runs when the entry's `byte[+0x96]` bit 0x10 is set (it also clears bit 0xA of the flag dword `*r8` on the way through): `003AB7F0` resolves the `+0x2B0` table, then for each of `word[+0x2BC]` s16 indices at `+0x100` it strides the index by `0x290` into `r14`'s rows, calls `0046D730` on `row+0xC0`/`+0x120`, and copies the eight dwords `+0xF0`..`+0x10C` down to `+0x130`..`+0x14C` - the per-entry state snapshot the motion entries keep.

Interior anchor `0041C2A6` (function `0041C260`).

## Cross-subsystem neighbours

**Resource — CLIENT (SWE2-EC7, batch 167, 53 edges).** The batch-167 `0041C260` snapshot arm names `003AB7F0`, which that layer's `00409FE0`/`00409CA0`/`00409D60`/`00409F50` reach, and the page's own `002DF960`/`002ED570` entries are called out of the same Resource fan-in - the resource pipeline drives these subjects; the crossing is that consultation, not shared ownership of the entry table.
- **ActorEntity - CLIENT and SERVICE (3 edges).** `002E8220` is called by bodies filed to ActorEntity: BattleUnit_RefreshActorRuntimeFromDefinition (`00238BF0`); `0022A0B0`, `00325090` reach bodies filed to ActorEntity: BattleStorage_InitializeWorkArrays (`002368D0`), ActorWork_GetBattleUnitRaw (`00263E30`) - shared machinery across the layer boundary, no shared ownership.
- **Audio - CLIENT and SERVICE (9 edges).** `00421E20` is called by bodies filed to Audio: `00332C40`, `003B99D0`; `0046CC70` reaches bodies filed to Audio: `002DEE80`, `00361BF0`, `003A0E20`, `003A0E50` (+3 more) - shared machinery across the layer boundary, no shared ownership.
- **CombatFormula - CLIENT (1 edge).** `004FE2F0` is called by bodies filed to CombatFormula: `00384E50` - shared machinery across the layer boundary, no shared ownership.
- **CoreRuntimeScheduling - CLIENT and SERVICE (8 edges).** `0017D4C0`, `0022A0B0`, `003325C0` are called by bodies filed to CoreRuntimeScheduling: `0017D000`, `0017D4C0`, `0022A0B0`; `0017D000`, `0017D4C0`, `0022A0B0` reach bodies filed to CoreRuntimeScheduling: `0017D4C0`, `001A14E0`, `001DB500`, `0022A0B0` (+1 more) - shared machinery across the layer boundary, no shared ownership.
- **Input - SERVICE (2 edges).** `0017D4C0`, `0022A0B0` reach bodies filed to Input: InputManager_CreateSingleton (`00198750`), `0035B270` - shared machinery across the layer boundary, no shared ownership.
- **Movement - MECHANICAL (13 edges).** Fan-in on the shared accessor `00202FE0`, PresentationEntryReferenceContainer_ResolveEntryById (`0051B9E0`). All 13 edges run through it - one accessor’s spread, not a per-caller relationship.
- **Party - MECHANICAL (1 edge).** Shared-helper fan-in on PartyFocus_GetCurrentPackedActorHandle (`003590D0`). All 1 edges run through it - one accessor’s spread, not a per-caller relationship.
- **RNG_Random_Selection - SERVICE (1 edge).** `0022A0B0` reaches bodies filed to RNG_Random_Selection: RNG_MT19937_Seed (`00379CF0`) - shared machinery across the layer boundary, no shared ownership.
- **SaveLoad - CLIENT (1 edge).** `0019C580` is called by bodies filed to SaveLoad: `00866200` - shared machinery across the layer boundary, no shared ownership.
- **Save_Load_Settings - SERVICE (3 edges).** `0017D4C0` reaches bodies filed to Save_Load_Settings: SaveloadManager_RefreshDisableAutosaveList (`001C1710`), SaveloadManager_EnsureSingleton (`001C18A0`), SaveloadManager_GetSingleton (`001C18E0`) - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (2 edges).** `0026BE90`, `002E8220` are called by bodies filed to Script_VM_Native_Bridge: `0034B310`, `0034D8D0` - shared machinery across the layer boundary, no shared ownership.
- **World - SERVICE (1 edge).** `0022A0B0` reaches bodies filed to World: `00266D10` - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - SERVICE (2 edges).** `001ED020`, `00325090` reach bodies filed to WorldAreaField: FieldData_GetVariable0 (`00265270`), FieldData_GetActiveFieldRecordBit15 (`00313F60`) - shared machinery across the layer boundary, no shared ownership.

## Falsification pass 1 — 2026-09-29 (OPUS): the "dead-stripped, NULL, vestigial" table refuted (CON-195); the binder and stub survive

**Attack.** The code claims of the `@FEF` section were turned into checks at their instructions, and the absence claim
at the centre was tested with a `rel32` call census, which the original census did not run. Script:
`Tools/analysis-kit/gfz-scripts/falsify_fef_entries.py`, output `falsify_fef_entries.out`, image `73461d08…` plus the
installed archive's own index (ASTRA's A17 parser), 0 BROKEN after the correction, exit 0. The `.cm` / `.ca` census and
FABLE's embedded-EFX sweep are carried, not re-run.

| # | Clause attacked | Result |
|---|---|---|
| F0 | the binder and the stub | **survives**: `005049BD` calls `0016D6A0`, which is `C2 00 00` |
| F1 | the thunk and its callers | **survives**: four load-completion sites |
| F2 | `00409FE0`'s gate, fold, table and null trap | **survives** |
| F3 | "no pointer to `0040A230` exists… the routine never runs and every row stays NULL" | **REFUTED (CON-195).** `00409F80` calls `0040A230` at `00409F84`, then tail-jumps `0051FB70`. `0041E3A0`, the render resource root's initialiser, calls `00409F80` at `0041E40B`. Every link of the start-up chain is a direct call: `0017D000` → `0017D4C0` → `0022A0B0` (the boot fixups) → `003325C0` → `003325D0` → `0041E3A0`. The table is therefore filled at start-up. The original scan looked for rip-relative references and data pointers to `0040A230`, not for a `rel32` call |
| F4 | the rows | **survives, with an addition**: 144 `.rdata` `obj_finish` `.cm` paths, and **all 144 are entries of the installed archive** |
| F5 | a consumer: the character-render-record page's "144 `lea` (.text fn)" | **REFUTED there (CON-196)**: every stored value is an `.rdata` string |

**What CON-195 changes, and what it does not.**
- The `00409FE0` arm does not fault for a folded name the populator seeded, and the path it reads names a real
  archive file. So "a vestigial PS2-era staging path, not a live loader" no longer follows.
- What the arm then does with the path (the page reads `001D6EC0` as a name/logging call) was not re-read here.
  *(Answered 2026-09-30 by UQ-218 pass 18, above: `001D6EC0` is the `AsyncLoadManager` companion lookup. Noted by
  SWE2-CONTRACT, DD batch 10.)*
- Whether a shipped session reaches the arm is not observed; this is a static reading. *(Runtime-only, SWE2-CONTRACT
  DD batch 10: statically the arm runs when any of the 144 `@FEF` models finishes loading (pass 18). Which of them a
  session loads depends on its content.)*
- FABLE's result that the **embedded** `EFX0010` payload reaches only the `ret 0` stub is untouched, as is the tail-dword
  source of the payload offset.
