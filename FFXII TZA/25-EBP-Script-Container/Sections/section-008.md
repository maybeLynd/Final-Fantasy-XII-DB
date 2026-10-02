---
system: EBP section_008 — the CML1 camera name list
category: 25-EBP-Script-Container
status: AUDITED
owner_layer: CodeDomain:Presentation.Camera
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
corpus_validated: "1115 / 1115 us .ebp files, 2026-09-03 (1114 containers; 423 carry this section)"
last_reviewed: 2026-09-12
ebp_units:
  - "section_008"
audit:
  passes: 2
  last_pass: 2026-09-13
  last_pass_state: opus-section-008-pass-2
  crossref_clean: true
  reopened_count: 0
---

# EBP `section_008` — the `CML1` camera name list

> The list of camera names a script is allowed to ask for, each paired with ~~a slot the engine~~
> ~~fills in at load time with~~ the matching camera's index in
> [`section_009`](section-009.md). ~~**The index that ships in the file is never used** — the~~
> ~~engine recomputes it by name.~~ **The index that ships in the file is the binding**; the name lookup never runs in the shipped build *(corrected 2026-10-02, OPUS: `0x003DA27B` and `0x003DD1AB` pass kind 1 to `FUN_0032F3D0`, whose kind-1 arm ends in `0x005C5230` = `xor eax, eax; ret`, so the stores at `0x003DA28F` / `0x003DD1BF` never run; the correction in §3)*.

**Corpus validation, before anything else.**

| | |
|---|---|
| files examined | **1,115 of 1,115** `us` `.ebp` files (1,114 are containers) |
| this unit present in | **423 (37.9 % of 1,114)** |
| co-occurrence | **always with [`section_009`](section-009.md)** — 423 together, **0 with either alone**. Also always with `section_000`. |
| size range | **64 B – 1,856 B, median 192 B** |
| entries held | 1 – 69 per file, **3,933 in the corpus** |

> ### `CML1` is not this section's private format — it occupies two directory slots
>
> **`section_010` carries the same `CML1` magic, in all 113 files that have it.** Censused here
> over the first four bytes of every present section in all 1,114 containers, and independently by
> `repos-1e`. `section_008`'s partner is `CAM7` (cameras); `section_010`'s partner is `SHK1`
> (`section_011`). **This sheet documents the camera instance.** The format itself — a name list
> whose indices are resolved against a partner table — is the same in both, and
> `section_010`/`section_011` are `repos-c7`'s units.
>
> All 113 files with `section_010` are a **strict subset** of the 423 with this section. The two
> "strict pairs" the census found are not two co-equal mechanisms; the shake pair only ever appears
> where the camera pair already is. *That co-occurrence is not engine-enforced (BY-5, answered 2026-09-26, FABLE, Claude Opus 5.5). The ATEL registration `003306E0` gates each stream on its own lookup, and neither shake guard reads a camera guard: `SHKD` on record `rbp+0xB60` and `SHKC` on `rbp+0x500`, against `CAMC` on `rbp+0x3F0`. *(Qualified 2026-09-29, SWE2-DATA from OPUS `a31c65871`: true of the code after the body's first size query, which gates the whole body and, being a kind-`0xFF` lookup, never passes in this build.)* The shake resolver `003DD120` reads only the slot's shake list (`+0xF0`) and its own per-slot bank `02ADD980`, never the camera list `+0xD8`. In the shipped build even that lookup is gated off (`0032F3D0` returns 0, `BY-3`), so the authored index is the binding. So the subset is a property of how the files were authored (the `cml`, `cam` and `shk` formats sit side by side in the engine's format-name table), not a rule the loader applies. Control: `_index/candidates/by5-shake-camera-independence/independence.py`.*

---

## 1. What the player sees

**Nothing directly — and that is the honest answer.** No pixel on screen comes from this section.

What it causes is that **cutscene cameras can be referred to by name at all.** An author writing a
scene says "cut to `cut1`"; this section is the lookup that turns that name into the actual camera
record. It is the index at the front of the book, not the book.

The names are the shot list of the scene: `cut1`, `cut2`, `open04`, `alc_b0400_cam_01`,
`stay_cam_mg_cut06`. The section exists in **296 of the 345 event scripts and 127 of the 769
field-map scripts** — the same split as [`section_009`](section-009.md), because they always ship
together.

## 2. The layout

Offsets are **from the start of the section**, which is where the container's directory slot 8
points. Section start is always `0x40`-aligned.

```struct Cml1Header base=section size=0x10
+0x00  char[4]  magic    'CML1' (0x314C4D43 read as a little-endian u32) -- 423/423
+0x04  u32   count       number of entries -- 1..69
+0x08  u32   _reserved0  always 0 in 423 of 423
+0x0C  u32   _reserved1  always 0 in 423 of 423
```

`count` 16-byte entries follow at `+0x10`, then the name blob — NUL-terminated strings back to
back — then zero fill to the next `0x40` boundary (0–63 bytes observed).

**Entry, 16 bytes.** The 16-byte stride is not inferred from the corpus — it is the literal
`add rbx, 0x10` at `0x003DA29A` in the reader.

```struct Cml1Entry base=record size=0x10
+0x00  u32   nameOffset   byte offset of the name, RELATIVE TO THE SECTION START
+0x04  i32   index        into section_009's camera array; -1 (0xFFFFFFFF) = unbound, CAM7_FindCameraByName's not-found return (0025653E) -- THE BINDING: read by the camera-start and hit-check verbs, never overwritten in the shipped build, see 3
+0x08  u32   _reserved0   zeroed at load regardless of contents -- 3933/3933 already 0
+0x0C  u32   _reserved1   low byte zeroed at load -- 3933/3933 already 0
```

*(Fence harmonised 2026-09-11 with `section_010`'s — the same chunk design, declared once: the entry
is `base=record`, `+0x04` is a signed index whose unbound value is the lookup's `-1`, and the two
trailing dwords are `_reserved`. This sheet's `cameraIndex` is that `index`.
OPUS-REQ-FABLE-FENCEDUP.)*

**`nameOffset` is relative to the section, not to the file and not to the entry.** The reader
computes `blob + (i32)entry[0]` at `0x003DA270`–`0x003DA278`, where `blob` is the section base.
Getting that origin wrong is the most common way a format sheet goes wrong, so it is anchored to
the instruction rather than to the fact that the numbers happen to look right.

## 3. The loader contract

**This section has no parser of its own.** It arrives, its base pointer is stored, and it is read
later — once — by the function that binds it to `section_009`.

**Arrival: `CAMCTL_OnLoaded` — `0x0032FA10`.** The container's directory walker
(`ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources`, `0x003304A0`, established by
`repos-1e`) calls this with one packed argument: **low 4 bits = manager slot, rest = blob pointer**,
split at `0x0032FA2E` / `0x0032FA36`. It then:

1. stores the blob at `g_cmlBlob = 0x022C6D80[slot]` — `0x0032FA3B`;
2. calls `0x0026CE00(slot, blob)` — a one-line setter that copies the same pointer into the
   **actor-manager record** at `+0xD8` (`0x02098EE8 + slot * 0x288`), store at `0x0026CE11`;
3. tests the manager's `+0xE0` — the `CAM7` blob — at `0x0032FA4F`, and **only if `section_009`
   has already arrived** calls `CML1_ResolveNames` at `0x0032FA5C`;
4. clears pending-resource bit 8 (`btr rbx, 8`, `0x0032FA6C`).

**Nothing is parsed on arrival, and the magic is never checked.** `CML1` (`0x314C4D43`) occurs
**zero times** in the executable — as bytes, as a dword, and byte-reversed — against `CAM7`'s single
hit. Corrupting the first four bytes of this section changes nothing.

> **CORRECTED 2026-09-12 (FABLE) — the resolver below never resolves anything in the shipped build, so the authored
> index column is the binding.** `FUN_0032F3D0` (`0x0032F3D0`, 87 bytes) returns 0 early when byte `02B62DAB` is 1 or byte `02B62DA8` is 3; otherwise kind 0, 1 and 2 load `4`, `5` and `14` into `ecx` and call **`0x005C5230`, whose whole body is `xor eax, eax; ret`** (`33 C0 C3`, a routine shared by about 880 call sites), and `test eax, eax` / `je` at `0x0032F410`–`0x0032F412` then returns 0. Only kinds 3 and above can return 1, and **all six call sites in the image pass 0, 1 or 2** (`0x002E4D46`: 2; `0x00378AAB`, `0x00378AEA`, `0x00378B01`: 0; `0x003DA27B`, `0x003DD1AB`: 1). So the store `e[+0x04] = CAM7_FindCameraByName(…)` at
> `0x003DA28A`–`0x003DA28F` **never executes**, and since that is `CAM7_FindCameraByName`'s only caller the name lookup
> is unreachable. The two zeroing stores at `0x003DA292` / `0x003DA296` sit outside the gate and still run.
>
> **The column is read afterwards, as authored.** `0x003DA400` — the camera start reached from `camerastart_7d`
> (`0x0034F2F0`) and `camerastart_7e` (`0x0034F930`) — bounds the script's entry number against `+0x04` and loads
> `[blob + entry·0x10 + 0x14]`, entry `+0x04`, at `0x003DA456` as the `section_009` record to play; `0x003DA330`, behind
> `camerahitcheck` (`0x0034EDB0`) and `camerahitcheck_33c` (`0x0034E9B0`), loads the same field at `0x003DA35E`.
>
> The earlier reading below took the gate for a platform predicate that might return either value and did not read
> the routine it ends in. Evidence, with the byte reads, the six call-site kinds and the corpus consequence:
> [`census.out.txt`](../../_experiments/evidence/cml1-authored-index-binding/census.out.txt).

**The read: `CML1_ResolveNames` — `0x003DA1F0`.** The whole body, 205 bytes:

```
  blob = manager[+0xD8]
  manager[+0x18] = 0xFFFF ; manager[+0x1A] = 0xFFFF          -- 0x003DA204, 0x003DA20B
  for p in {0x118, 0x130, 0x148, 0x160}:                      -- 0x003DA212 .. 0x003DA247
      manager[p] = 0 ; manager[p+2] = 0xFFFF
  if (blob == NULL) return                                    -- 0x003DA24E
  count = blob[+0x04]                                         -- 0x003DA253
  e     = blob + 0x10                                         -- 0x003DA25C
  while (count-- > 0) {                                       -- 0x003DA260, 0x003DA29E
      name = blob + (i32)e[+0x00]                             -- 0x003DA270, 0x003DA278
      if (FUN_0032F3D0(1, name) != 0)                         -- 0x003DA27B
          e[+0x04] = CAM7_FindCameraByName(manager[+0x28], name)   -- 0x003DA28A, 0x003DA28F
      e[+0x08] = 0                                            -- 0x003DA292
      e[+0x0C] &= 0xFFFFFF00                                  -- 0x003DA296
      e += 0x10                                               -- 0x003DA29A
  }
```

**Upstream of all of this, the container can refuse to dispatch the slot at all.** The walker gates
every section on `slotCount > slotIndex`, **unsigned**: for this section, `cmp dword ptr [rdi+4], 8`
/ `jbe` at `0x00330593`–`0x00330597`, then the directory read `mov eax, [rdi+0x30]` (`0x10 + 8*4`)
at `0x00330599`, a zero-offset skip at `0x0033059E`, the file-relative rebase `add rax, rdi` at
`0x003305A0`, the manager-index packing `or eax, ebx` at `0x003305A5`, and the call at `0x003305A9`.
`slotCount` is `0x14` in all 1,114 containers, so **the gate is real code that never fires against
this corpus — and fires the moment someone edits the header.** Setting `+0x04` to 8 or less silently
removes the camera list.

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| container `+0x04` | the walker, `0x00330593` | **`slotCount <= 8` → the section is never dispatched** | — | — |
| directory slot 8 | the walker, `0x00330599` | **offset `0` → treated as absent** | — | — |
| `+0x00` magic | — | — | — | **yes — `0x314C4D43` occurs 0× in the executable (byte, dword and byte-reversed scan of the whole image)** |
| `+0x04` count | `CML1_ResolveNames` **`0x003DA253`** | — | — | — |
| `+0x08`, `+0x0C` | — | — | — | **yes — no reader found; the walker's own header census (`repos-1e`) shows the container never reads them either** |
| entry `+0x00` nameOffset | `CML1_ResolveNames` **`0x003DA270`** | — | — | — |
| entry `+0x04` cameraIndex | `0x003DA400` at `0x003DA456` (camera start); `0x003DA330` at `0x003DA35E` (hit check) | — | — | **no — this is the binding.** The write at `0x003DA28F` is behind `0x0032F3D0`, which returns 0 in the shipped build. *Corrected 2026-09-12; this cell read "yes, and strongly — the engine writes this field at `0x003DA28F` before anything reads it".* |
| entry `+0x08` | — | — | — | **yes — zeroed at `0x003DA292`** |
| entry `+0x0C` | — | — | — | **yes — low byte zeroed at `0x003DA296`** |
| the name blob | via `nameOffset`, compared by `strncmp` | — | **23 bytes compared, see below** | — |

> ### The authored index column does nothing
>
> **~~Three~~ Two of the four dwords in every entry are overwritten at load.** *(corrected 2026-10-02, OPUS: `+0x08` is zeroed at `0x003DA292` and `+0x0C`'s low byte at `0x003DA296`; the `+0x04` store never runs — `0x003DA27B` and `0x003DD1AB` pass kind 1 to `FUN_0032F3D0`, whose kind-1 arm ends in `0x005C5230` = `xor eax, eax; ret`, so the stores at `0x003DA28F` / `0x003DD1BF` never run)* Only `nameOffset` is read.
> `cameraIndex` ships with the correct answer already in it — and it agrees with what the engine
> computes in **422 of 423 files** (§5) ~~— but the engine never looks: it calls~~
> ~~`CAM7_FindCameraByName` and **stores the result over the top**, at `0x003DA28F`.~~ — and the engine uses it as authored: the call and its store sit behind a gate that returns 0 *(corrected 2026-10-02, OPUS: `0x003DA27B` and `0x003DD1AB` pass kind 1 to `FUN_0032F3D0`, whose kind-1 arm ends in `0x005C5230` = `xor eax, eax; ret`, so the stores at `0x003DA28F` / `0x003DD1BF` never run; the reversal below)*.
>
> For a modder this is the useful half of the sheet. **~~Renaming a camera in `section_009` breaks~~
> ~~the link; renumbering the index column in `section_008` does nothing at all.~~** **Renumbering the index column in `section_008` changes which camera plays; renaming a camera in `section_009` changes nothing** *(corrected 2026-10-02, OPUS: `0x003DA27B` and `0x003DD1AB` pass kind 1 to `FUN_0032F3D0`, whose kind-1 arm ends in `0x005C5230` = `xor eax, eax; ret`, so the stores at `0x003DA28F` / `0x003DD1BF` never run; the reversal below)*. ~~The file is a~~
> ~~runtime structure that ships pre-filled, not a table of authored parameters.~~

> **REVERSED 2026-09-12 — the box above has the direction wrong.** The write it relies on is behind a gate that returns
> 0 on every shipped call (correction at the head of this section). **Renumbering the index column in `section_008`
> changes which camera a script plays; renaming a camera in `section_009` changes nothing**, because no reachable code
> compares the names. The eleven duplicate-name files (§5) are where this shows: in **all eleven** the authored index
> points at the **later** of the two same-named records, where the name lookup would have returned the earlier, and in
> **seven** of the eleven the two records differ (2–11 bytes). The shipped game plays the later record; a
> reimplementation that resolves by name plays the earlier one.

**The lookup: `CAM7_FindCameraByName` — `0x00256530(slot, name)`.**

```
  if ((u32)slot >= 5) return -1                                -- 0x00256539
  blob = g_camBlob[slot]        (0x02092808, stride 0xBB0)     -- 0x00256558
  if (blob == NULL) return -1                                  -- 0x0025655D
  n = blob[+0x04]                       (CAM7 cameraCount)     -- 0x00256573
  for (i = 0; i < n; i++)                                      -- 0x00256576, 0x002565A0
      if (strncmp(name, g_camEntries[slot] + (i << 6), 23) == 0)   -- 0x00256589, 0x00256594
          return i                                             -- 0x002565BC
  return -1                                                    -- 0x002565A4
```

**A linear scan, `0x40` per entry, and `n = 23`.** Three things follow, and all three are checkable:

- **The compare length is 23, while [`section_009`](section-009.md)'s loader copies the name with
  `strncpy(…, 24)`.** Two camera names differing only in their 24th character are the same camera
  to this lookup. The longest name in the corpus is exactly 23 characters, so the shipped game never
  reaches it — but it is one character of headroom, not none.
- **A name with no matching camera resolves to `-1`**, the same value two entries carry in the
  shipped corpus (§5). Missing is a supported outcome, not a crash.
- **When two cameras share a name, the scan returns the first.** *(2026-09-12: the scan is unreachable in the shipped build; the authored index picks the later duplicate in all eleven files — see the reversal above.)* Eleven files contain exactly one
  duplicated camera name (§5), so this is reachable in the retail data.

**What loading normalises.** Beyond the three entry fields: five `(u16, u16)` pairs in the manager
record are reset ~~to `(0, 0xFFFF)`~~ on every resolve — `+0x18` to `(0xFFFF, 0xFFFF)`, and `+0x118`, `+0x130`, `+0x148`,
`+0x160` to `(0, 0xFFFF)` *(corrected 2026-10-02, OPUS: `0x003DA204` / `0x003DA20B` store `0xFFFF` to both `+0x18` and `+0x1A`; `0x003DA212`–`0x003DA247` store `0` / `0xFFFF` to the other four; BY-4 below)*. The last four are spaced `0x18` apart, and `section_009`'s handler separately loops
`FUN_002566E0(slot, 0..3)`, so there appear to be **four camera channels per manager** each holding
a resolved index initialised to "none". Their use is not established here. *(Established 2026-09-12, `BY-4`: `+0x110 + 0x18·ch` are the four **camera channels** (`ActorManagerSlotEntry`); each pair is the channel's **state** (`0` idle) and the **`CML1` entry number** it was started with (`0xFFFF` none), and `+0x18` / `+0x1A` are the main and sub frames' owning channel, both set to `0xFFFF`. See [the scripted camera player](../../17-Presentation-Rendering/Scripted-Camera/the-scripted-camera-player.md) §2.2.)*

**Ordering.** `CML1_ResolveNames` runs from whichever of the two handlers observes the other's blob
already present, so the pair resolves once regardless of which section's load completes first.
`section_009`'s handler reaches it through `0x0026CE20` and the same `+0xE0`/`+0xD8` test.

**Teardown.** `ActorResource_ResetManagerLoadState` (`0x0032ED80`) loads the blob at `0x0032EFD3`,
~~frees it at `0x0032EFBD`~~ passes it to the free at `0x0032F005` only when `0x005C5230(5)` returns non-zero, which it never does, and clears the slot at `0x0032F00C` *(corrected 2026-10-02, OPUS: `0x0032EFBD` frees the slot-9 blob; slot 8's `[r14 + rdi*8 + 0x21a6d80]` is loaded at `0x0032EFD3` and its free is gated at `0x0032EFF4`–`0x0032F000`)*. The freed pointer's only use is the
free itself.

**The write path.** None found. Nothing in the executable emits `CML1`; it is authored offline.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `0x003DA1F0` | `CML1_ResolveNames` — ~~the only reader of this section~~ the load-time pass over this section, whose index write-back never runs; entry `+0x04` is read at run time by the §3 readers and by `0x003DA300` at `0x003DA31F` *(corrected 2026-10-02, OPUS: `0x003DA27B` and `0x003DD1AB` pass kind 1 to `FUN_0032F3D0`, whose kind-1 arm ends in `0x005C5230` = `xor eax, eax; ret`, so the stores at `0x003DA28F` / `0x003DD1BF` never run)* (count `0x003DA253`, nameOffset `0x003DA270`, index write-back `0x003DA28F`, scratch zeroing `0x003DA292`/`0x003DA296`, stride `0x003DA29A`) | ✅ full body |
| `0x00256530` | `CAM7_FindCameraByName` — slot bound `0x00256539`, blob fetch `0x00256558`, count `0x00256573`, `0x40` stride `0x00256589`, `strncmp` n=23 `0x00256594`, hit `0x002565BC`, miss `0x002565A4` | ✅ full body |
| `0x0032FA10` | `CAMCTL_OnLoaded` — slot/pointer split `0x0032FA2E`/`0x0032FA36`, blob store `0x0032FA3B`, binder call `0x0032FA43`, partner test `0x0032FA4F`, resolve call `0x0032FA5C` | ✅ full body |
| `0x0026CE00` | binder: `manager[+0xD8] = blob`, store at `0x0026CE11` | ✅ full body |
| `0x0026CE20` | the `CAM7` twin: `manager[+0xE0] = blob`, store at `0x0026CE31` | ◐ entry + that store |
| `0x0032ED80` | teardown — free `0x0032EFBD`, clear `0x0032F00C` | ◐ read for the teardown only |
| `0x003304A0` | container directory walker; dispatches slot 8 here. Established by `repos-1e`, cited not re-derived | ✗ |

## 5. Corpus survey

**Invariants — checked over all 423 files and all 3,933 entries.**

| | |
|---|---|
| `+0x00` magic | `CML1`, **423 / 423** |
| `+0x08`, `+0x0C` | `0`, **423 / 423** |
| entry `+0x08`, `+0x0C` | `0`, **3,933 / 3,933** — already what the loader would write |
| entry `nameOffset` in range | **3,933 / 3,933** land past the entry array and inside the section |
| entry `cameraIndex` in range | **3,933 / 3,933** — either a valid `section_009` index or `-1`, never out of range |
| tail padding after the last name | 0–63 bytes, i.e. **padded to `0x40`** |

> **2026-09-12 — measured against the lookup the resolver would compute** (first match, `strncmp` n = 23), the column
> differs in **exactly 11 entries, one per duplicate-name file**, and each points at the later duplicate
> ([`census.out.txt`](../../_experiments/evidence/cml1-authored-index-binding/census.out.txt)). The paragraph below compares names at the authored index, which agree for
> duplicates too; it stands, and "the engine's own answer" in it is the answer the engine would give if the resolver
> ran. It does not.

**The authored index column agrees with the engine's own answer in 422 of 423 files.** For every
entry, the camera at the authored index has the same name as the entry — which is precisely what an
offline tool running the same lookup would produce. It is corroboration that the column *means* what
§3 says, and it is **not** evidence that the column is read.

**`-1` appears exactly twice in 3,933 entries**, both in `evt_t0086.ebp`, on the names `ELE_OUT_1`
and `ELE_IN_3` — two names with no camera record at all. The offline tool wrote the same "not
found" value the runtime lookup returns.

### The eleven files where the two counts disagree — fully explained

`section_008`'s count and `section_009`'s count are equal in **412 of 423** files. All eleven
exceptions have the same cause: **`section_009` contains one duplicated camera name, and
`section_008` lists each distinct name once.**

| file | `008` | `009` | the duplicated `CAM7` name |
|---|---:|---:|---|
| `ald_a0180` | 11 | 12 | `cut_05_02` |
| `bul_a0101` | 20 | 21 | `cut1_2` |
| `byu_x0100` | 15 | 16 | `cut2_2` |
| `evt_t0081` | 4 | 5 | `mapgcam_mfr_gate1` |
| `evt_t0083` | 35 | 36 | `open04` |
| `ozm_c0180` | 5 | 6 | `cut4` |
| `rbn_a0380` | 10 | 11 | `stay_cam_mg_cut06` |
| `sum_d0001` | 21 | 22 | `カット00` |
| `glf_a01` | 11 | 12 | `cut001` |
| `grm_e13` | 12 | 13 | `mapgcam_SUIMON_E_床の丸` |
| `evt_t0086` | **34** | **33** | `magcam_rblj01_r_nw2` |

**Duplicate camera names occur in exactly these eleven files and nowhere else in the 423.** The
correspondence is exact in both directions, which is what makes this an explanation rather than a
coincidence.

`evt_t0086` is the only file where `section_008` is the *larger* of the two, and it reconciles
exactly: 33 camera records − 1 duplicate name = 32 distinct names, + the 2 entries resolving to
`-1` = 34.

**Entry ordering is not the camera order.** The entries are in the authored order of the names, and
the index column is a permutation: **284 of 423 files** have it as the identity `0,1,2,…`, and the
other 139 do not. A reader that assumed entry *i* describes camera *i* would be wrong in a third of
the corpus.

## 6. Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Is `nameOffset` relative to the file, the section, or the entry? | **The section.** `0x003DA270`–`0x003DA278` computes `blob + (i32)e[0]` with `blob` the section base held in `r14` from `manager[+0xD8]`. Decided by the instruction, not by the numbers. |
| Is the entry really 16 bytes, or did the corpus just fit? | **`add rbx, 0x10` at `0x003DA29A`.** The corpus is consistent with it in all 3,933 entries, but the stride is read off the loop. |
| **Is this section inert?** | **No — and this reading was wrong once and corrected.** A whole-program instruction-level reference census on `g_cmlBlob` (`0x022C6D80`, Ghidra `ReferenceIterator`, all reference types) returns **4 references**: two stores, one load, one clear — and the loaded value's only use is `free`. That census is accurate and **insufficient**: `0x0032FA43` calls `0x0026CE00` with the blob **still live in RDX**, which copies it to `manager[+0xD8]`, and consumers reach it from there. This is exactly the blind spot `COVERAGE.md` catalogues — *a displacement search stops counting where a base pointer starts*. **The Inert rows in §3 are stated against the reader's body, not against that census.** |
| Then are `+0x08`/`+0x0C` and the index column really unread? | **They are written before any read could occur** — `0x003DA28F`, `0x003DA292`, `0x003DA296` — and `CML1_ResolveNames` is the only function that dereferences the blob. This is a stronger statement than "no reader found", and it does not depend on a search having been exhaustive. *Corrected 2026-09-12: only `+0x08`/`+0x0C` are written unconditionally; the index store at `0x003DA28F` is behind the gate that returns 0, and the index is read at `0x003DA456` and `0x003DA35E`.* |
| Could the magic be checked by arithmetic the constant scan cannot see? | **Not for this section.** The scan found `CML1` zero times, and separately the only code that ever dereferences the blob is `CML1_ResolveNames`, whose 205 bytes contain no reference to `+0x00`. Both routes agree. |
| Does the `strncmp` length really differ from the `strncpy` length? | **Yes: `mov r8d, 0x17` at `0x00256583` (23) against `strncpy` n = `0x18` (24) at `0x00256276`.** Two different immediates in two different functions. |
| Did an external tool supply any of this? | **No tool reads `CML1` or `CAM7`.** `ff12-script` reads `section_000` only. There is no oracle here to inherit errors from, and none was consulted. |

**What was tried and failed to break it.** The obvious alternative reading is that the index column
is authored input and `CML1_ResolveNames` merely *validates* it. That would predict a compare
against the existing value, or a branch that leaves it alone when it already matches. There is
neither: `0x003DA28F` is an unconditional `mov dword ptr [rbx + 4], eax` on the success path, and on
the failure path of the `0x0032F3D0` filter the field is simply left as-is and still never read. *(Corrected 2026-09-12: the failure path is the only path the shipped build takes, and the field is read — at `0x003DA456` and `0x003DA35E`. The reading this paragraph rejected, that the column is authored input, is the right one.)*
The 422/423 agreement in §5 is the observation that would have supported the alternative, and it
survives as corroboration of *meaning* only.

## 7. What this document does not claim

- ~~**`FUN_0032F3D0(1, name)` is not read.**~~ **Read 2026-09-12 (`BY-3` answered): it returns 0 for kinds 0–2, which is every call in the image, so no entry is ever resolved and the "narrows" case below is the only case** — see the correction at the head of §3. The original text follows. It gates whether a name is resolved at all, and it calls
  the same three functions (`0x00408B10`, `0x00408B30`, `0x005C5230`) that the teardown consults
  before freeing — so it looks like an allocator-mode or platform predicate rather than anything
  about the name. **Not established.** If it can return 0 for a name, that entry keeps its authored
  index and §3's "overwritten" claim narrows to "overwritten whenever resolution runs".
  → `PROPOSED-repos-4b-3`
- ~~**The four `(u16, u16)` pairs at `+0x118`/`+0x130`/`+0x148`/`+0x160` are described, not
  explained.**~~ **Explained 2026-09-12 (`BY-4`):** the state and entry words of the four camera channels — see §3's note. The original text follows. That there are four, that they are `0x18` apart, and that `section_009`'s handler
  loops `0..3`, are facts; "four camera channels" is the reading they suggest and is not proven.
- **Who consumes the resolved index is not documented here.** *Answered 2026-09-12:* `0x003DA400` (the camera start behind `camerastart_7d` / `camerastart_7e`) and `0x003DA330` (behind `camerahitcheck` / `camerahitcheck_33c`) read entry `+0x04` — the authored value, since nothing overwrites it. The original text follows. This sheet establishes that the index
  is written into the entry at `0x003DA28F`; what reads it back — presumably the script verb that
  plays a named camera — belongs with
  [category 01](../../01-Script-VM-Native-Bridge/README.md) and was not traced.
- **The `CML1` format as used by `section_010` is not covered.** Only the magic
  and the 113-file count were checked here. Whether `section_010` shares the entry layout, and
  whether `SHK1` has an equivalent of `CAM7_FindCameraByName`, is `repos-c7`'s unit.
- ~~**`section_010`'s subset relationship is stated, not explained.**~~ All 113 files with the shake
  pair also have the camera pair; ~~no mechanism is offered for why.~~ *(answered: the co-occurrence is not engine-enforced — BY-5, answered 2026-09-26, §2; 2026-10-02, OPUS)*

## 8. Related

- [`section_009` — the `CAM7` camera table](section-009.md) — the partner this section indexes into.
- `section_010` — the other `CML1`, paired with [`SHK1` (`section_011`)](section-011.md); same
  magic, different partner. `repos-c7`'s unit; ~~the sheet does not exist yet, so this is~~
  ~~deliberately not a link.~~ its sheet is [`section-010.md`](section-010.md) *(answered: written since; 2026-10-02, OPUS)*.
- [`25-EBP-Script-Container/README.md`](../README.md) — the container and the frozen census.
- [`01 — Script VM & Native Bridge`](../../01-Script-VM-Native-Bridge/README.md) — where a script
  names a camera.

## Falsification pass 2 — 2026-09-13 (OPUS)

§5 is an unusually specific survey — nine denominators, two named entries, eleven named files with
the duplicated name in each, and a claim that holds *in both directions*. Specific claims are
falsifiable claims, so all of it was re-derived from a corpus extracted from `FFXII_TZA.vbf` in this
session, with the container walk written independently. **Names were compared as raw bytes**: two of
the eleven are Japanese, and a decode step is one more place to be wrong.

**Nothing needed correcting.**

| claim | measured |
|---|---|
| **423** files carry a CML1 section 8 | **423**, of 1,115 containers |
| magic, and header `+0x08`/`+0x0C` zero | **423 / 423** each |
| **3,933** entries | **3,933** |
| entry `+0x08`/`+0x0C` zero | **3,933 / 3,933** |
| `nameOffset` past the array and inside the section | **3,933 / 3,933** |
| `cameraIndex` a valid index or `−1` | **3,933 / 3,933** |
| tail padding 0–63 bytes | **0..63** |
| `−1` appears **exactly twice**, both in `evt_t0086`, on `ELE_OUT_1` and `ELE_IN_3` | **exactly those two** |
| the counts agree in **412 of 423** | **412** |
| the index column is the identity in **284 of 423** | **284** |
| every entry's name equals the camera at its authored index, in **422 of 423** | **422** |

### The eleven exceptions, and the claim that runs both ways

All eleven files came back with the same counts and **the same duplicated name**, including the two
that are Shift-JIS — `sum_d0001`'s `カット00` and `grm_e13`'s `mapgcam_SUIMON_E_床の丸`, matched as
bytes rather than as text.

And the harder half held: **files containing a duplicated `CAM7` name are exactly the eleven
mismatch files, with nothing outside the set.** §5 calls that "what makes this an explanation rather
than a coincidence", and it is the part a survey most easily gets wrong, because it requires scanning
the 412 files where nothing is wrong.

`evt_t0086`'s reconciliation is exact as stated: **33 camera records − 1 duplicated name = 32
distinct, + the 2 entries resolving to `−1` = 34**, and those two `−1` entries are the only two in
the corpus.

> **A page whose claims are this specific is cheap to check and expensive to fudge.** Nine
> denominators and eleven named files either come back or they do not; there is nowhere for an
> approximation to hide. That is worth more than a page with the same content stated loosely.

**Not claimed:** nothing here was executed or observed live. §3's loader contract, the `0x003DA29A`
stride instruction and `0x003DA270`'s name-origin computation were not re-read — this pass took §2's
layout and every corpus figure in §5. §5's own 2026-09-12 note stands: the index column agrees with
the lookup the resolver *would* compute, and that the resolver does not run is unchanged here.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-CONTRACT)

- **ActorEntity — CLIENT and SERVICE (44 edges).** 16 inbound (ActorEntity bodies `ActorResource_ResetManagerLoadState` (0032ED80), `ActorResource_BeginManagerResourceSetLoad` (0032FCA0), `0032FAC0` call page-cited `002566E0`, `0026CE00`, `0026CE20`); 28 outbound (page-cited `ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources` (003304A0), `ActorResource_ResetManagerLoadState` (0032ED80), `0032FA10` call ActorEntity bodies `0026CE00`, `ActorResource_FinalizeManagerRuntimeAfterLoads` (0032F1B0), `00263FF0`). Substantive edges include `002566E0` is called by `ActorResource_ResetManagerLoadState` (0032ED80); `002566E0` is called by `0032FAC0`; `002566E0` is called by `003306E0`; `0026CE00` is called by `ActorResource_ResetManagerLoadState` (0032ED80); the remaining edges run through shared helpers the page cites.
- **WorldAreaField — CLIENT (3 edges).** 3 inbound (WorldAreaField bodies `WorldSimulation_ProcessDeferredModeRequest` (0032FC30), `00378A60` call page-cited `0032F3D0`, `00408B10`, `00408B30`). Substantive edges include `0032F3D0` is called by `00378A60`; `00408B10` is called by `WorldSimulation_ProcessDeferredModeRequest` (0032FC30); `00408B30` is called by `WorldSimulation_ProcessDeferredModeRequest` (0032FC30).
- **Presentation — SERVICE (1 edge).** The ATEL registration body `003306E0` calls `002561C0`, the Presentation-side record installer that validates the `CAM7` magic and stores the record into the slot table at `02092800` (stride `0xBB0`).
- **Resource — SERVICE (1 edge).** The same `003306E0` calls `0032E400`, the indexed resource-descriptor resolver (bounds check `0xFF`, pointer table `022C51F0`).

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-section-008-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0034E9B0` | 90 B | calls `00267E10(r9)` twice (results a, then b), calls `003DA330(002640C0(), b AND 0xFFFFFF, a)` and tail-jumps `0026B4E0(rcx, that result)` | `0034E9C8`, `0034E9D2`, `0034E9DE`, `0034E9EC`, `0034EA05` |
| `0034EDB0` | 101 B | calls `00267F90(r9, -1)`, then `00267E10(r9)` twice (results a, then b), calls `003DA330(002640C0(), b AND 0xFFFFFF, a)` and tail-jumps `0026B4E0(rcx, that result)` | `0034EDCB`, `0034EDD3`, `0034EDE9`, `0034EDF7`, `0034EE10` |
