---
system: EBP `section_012` — the per-map actor manifest
category: 25-EBP-Script-Container
status: AUDITED
owner_layer: CodeDomain:Actor.Resource
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
corpus_validated: 842 of 1,114 EBP2 containers, 2026-09-03 — every container that has the section
last_reviewed: 2026-09-03
ebp_units:
  - "section_012"
audit:
  passes: 1
  last_pass: 2026-09-05
  last_pass_state: "GN160 — gzf fa0db293…d2f708, snapshot b57264ba…d18fea34, exe 73461d08…d89721f8; ledger internal=38161 owner=9409 finalNo=585 codeDomain=28028 explicit=38022 unresolved=139 pct=99.63575"
  last_pass_by: repos-4b
  crossref_clean: true
  reopened_count: 0
---

# EBP `section_012` — the per-map actor manifest

> A short list, in ~~every third map file~~ 842 of the 1,114 map containers (75.6 %) *(corrected 2026-10-02, OPUS: read through `vbf_read_entry` from `FFXII_TZA.vbf`; §1's own count)*, naming **which actors that map needs** — its NPCs, its
> monsters, its treasures — as a numeric id and a one-letter category.

| | |
|---|---|
| files examined | **1,114 of 1,114** EBP2 containers |
| this unit present in | **842 (75.6 %)** |
| co-occurrence | no pairing; the most common section after `000` |
| size range | **64 – 256 B**, median 64 — 726 files at 64, 63 at 128, 52 at 256, one at 192 |
| entries | **6,771 total**, 1 – 55 per file, median 3 |

## 1. What the player sees

**Which characters and creatures are actually in a place.** Walk into a map and the game must
already know that this stretch of the Estersand needs those wolves, that merchant, that chest —
this is the list it was told. Nothing here decides *behaviour*; it decides **the cast**.

## 2. The layout

```struct Ebp012Manifest base=section
+0x00  u32   count   number of entries; 1..55 observed
```

**`+0x04` onward is a variable-length array of `count` × `Ebp012Entry`**, then zero padding to the
next `0x40` boundary. It is deliberately **not** in the fence: the fence grammar has no
variable-length type, and inventing a fixed one — `u32[15]` for the 64-byte case — would state a
bound the format does not have. *`check_layouts.py` rejected the first attempt at exactly this,
then reported the array as a 60-byte `UNACCOUNTED` gap, which would have been a worse lie than
leaving it out.*

Each entry is two `u16`:

```struct Ebp012Entry base=record size=0x04
+0x00  u16   id              category-relative model number -- the mapping is PER-LETTER, see 5
+0x02  u16   categoryLetter  a single ASCII letter
```

**The section is zero-padded to a `0x40` boundary and the padding is genuinely zero in 842 of
842 files.** `4 + 4 × count` never exceeds the section length in any file.

## 3. The loader contract

**The handler stores; it does not parse.** Dispatched from
`ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources` (`0x003304A0`) under the gate
`slotCount > 12`, offset read at `0x003305EA`, call at `0x003305FA`.

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| section pointer | `FUN_0032fb70` (`0x0032FB70`, 186 B) — stored to **two** places, see below | — | — | — |
| `+0x00 count` | **not read by the handler** | — | — | see below |
| entries | **not read by the handler** | — | — | see below |

`FUN_0032fb70` does exactly five things, and none of them is parsing:

```
0032FB85  mov  edx, ecx                          ; the packed argument
0032FB8E  and  ecx, 0xf                          ; low 4 bits = manager index
0032FB96  and  rdx, rax   (rax = 0xFFFFFFF0)     ; the rest = section pointer
0032FB9B  mov  [0x022C6DA8 + rcx*8], rdx         ; STORE the pointer, per manager
0032FBA3  call FUN_0026ce40(rcx, rdx)            ; SECOND STORE -- rdx is still the pointer
0032FBB3  btr  rdi, 9                            ; clear pending-bit 9 in 0x022C6E48[mgr]
```

> ### AMENDED 2026-09-05 by the audit — the pointer is stored twice, not once
>
> **`RDX` still holds the section pointer at `0x0032FBA3`.** It is set at `0x0032FB96` and nothing
> between there and the call touches it — `0x0032FB99` writes `ebx`, not `rdx`. So the call is
> `FUN_0026CE40(managerIndex, sectionPointer)`, **two arguments**, and the second is the payload.
>
> **`FUN_0026CE40` is a 21-byte one-line setter** — `movsxd rax, ecx` / `imul rcx, rax, 0x288` /
> `lea rax, [rip+0x1e2c0bf]` (`0x0026CE4A`) / `mov [rcx+rax], rdx` (`0x0026CE51`) — resolving to
> **`0x02098F10`, which is the actor-manager record at `+0x100`** (base `0x02098E10`, stride
> `0x288`).
>
> **It is byte-identical in shape to the setters this section's own §3 gestured at:**
> `0x0026CE00` → `+0xD8` (`section_008`) and `0x0026CE20` → `+0xE0` (`section_009`). Three sections,
> three adjacent fields of one record, one setter each.
>
> **The blockquote below cited the `section_008` aliasing precedent and then missed the identical
> instruction three instructions after the store it did read.** The precedent is not that a copy
> *might* exist — it is that the copy is made by a two-argument setter at the next call, with the
> pointer live in `RDX`. That is exactly what is here. *(`repos-4b`, audit pass 1.)*
>
> **Consequence for §7:** the consumer to look for reads **`managerRecord[+0x100]`**, not
> `0x022C6DA8[manager]`. `0x02098F10` has a **second writer** — `ActorManager_BindLoadedDefinitionPayload`
> at `0x0026CC31` (`MOV [RDI + 0x100], RBX`) — so the field is written from two paths.

`r14` is `rip - 0x20FB8E` at `0x0032FB87`, which resolves to the image base `0x00120000`, so the
three displacements are the per-manager tables **`0x022C6DA8`** (pointer), **`0x022C6E48`** (flags)
and **`0x022C6D28`** (id, used only on the manager-0 error path at `0x0032FC00`).

> **The consumer is not in this function~~ and this document does not claim to have found it~~.** *(answered: there is none — nothing in this executable walks the section, §7, 2026-09-27; 2026-10-02, OPUS)* It
> reads the pointer back out of one of the two places the handler puts it — and **the amendment
> above narrows which: `managerRecord[+0x100]`, not `0x022C6DA8[manager]`**, because that is the one
> a consumer reaches through `FUN_00263FF0`. **That is precisely the aliasing case `COVERAGE.md`
> records for `section_008`**, where a reference census returned four hits and made a live section
> look inert because the search stopped where the copy started. **No `Inert` row is asserted here**,
> because asserting one would require the reader's body, which has not been read.
>
> *The census result is confirmed by the audit: `0x022C6DA8` has exactly **4** references — handler
> store, init store, teardown load and clear. The warning was right, and it was right for the right
> reason.*

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `003304A0` | dispatcher, gate `slotCount > 12` | ✅ |
| `003305EA` | reads the slot-12 offset | ✅ |
| `003305FA` | calls the handler | ✅ |
| `0032FB70` | the handler — stores and clears the pending bit | ✅ complete body |
| `0026CE40` | **`ActorManager_BindSection012Blob(mgr, ptr)`** — `managerRecord[+0x100] = ptr`; `lea` `0x0026CE4A`, store `0x0026CE51` | ✅ complete 21-byte body *(audit 2026-09-05)* |
| `0026CC31` | second writer of `+0x100`, inside `ActorManager_BindLoadedDefinitionPayload` | ◐ that instruction only |
| `0032F1B0` | ~~teardown path~~ the load finalizer, `ActorResource_FinalizeManagerRuntimeAfterLoads`, run when the flags word goes to zero *(corrected 2026-10-02, OPUS: `0032F1F9` calls the light binder `0037AA90` and `0032F227` `0026CE60`; section-014.md)* | ❌ |

### Data addresses cited

| Address | Name | Kind | Contents |
|---|---|---|---|
| `022C6DA8` | — | per-manager pointer table | the stored `section_012` pointer, stride 8 |
| `022C6E48` | — | per-manager flags | bit 9 = payload pending |
| `022C6D28` | — | per-manager id | stride 4, error path only |

## 5. Corpus survey — what the entries are

**Column 2 takes exactly 11 values across all 6,771 entries, and every one is a printable ASCII
letter.** Seven map onto the archive's own `obj_finish` category directories:

| letter | entries | `obj_finish` category | archive dirs |
|---|---:|---|---:|
| `n` 110 | 3,100 | **npc** | 1,699 |
| `g` 103 | 1,287 | **gadget** | 103 |
| `c` 99 | 819 | **chara** | 161 |
| `C` 67 | 440 | — | — |
| `t` 116 | 410 | **treasure** | 17 |
| `m` 109 | 348 | **monster** | 1,679 |
| `w` 119 | 157 | **weapon** | 326 |
| `N` 78 | 131 | — | — |
| `b` 98 | 39 | — | — |
| `s` 115 | 32 | **summon** | 96 |
| `S` 83 | 8 | — | — |

**~~Column 1 is the model number less 1000~~** Column 1 is the model number less 1000 for `c`, `m` and `n` only; for `b`, `g`, `s` and `t` it is the model number itself *(corrected 2026-10-02, OPUS: re-run against the `obj_finish` stems in `FFXII_TZA.vbf` — at `id + 1000` `g` 0 of 97, `b` 0 of 12, `s` 0 of 13, `t` 0 of 10; directly 77, 10, 10 and 8; the per-letter table below)*, tested against the 935 distinct `(letter, id)` model
stems in the archive:

| letter | resolves | rate |
|---|---|---:|
| `m` | 333 of 348 | **95.7 %** |
| `n` | 2,187 of 3,100 | 70.5 % |
| `c` | 237 of 819 | 28.9 % |
| `w` | 34 of 157 | 21.7 % |
| `g` `t` `s` `b` `C` `N` `S` | 0 | **0 %** |

> **The monster column is the strong result and the one worth using: `m` + `id + 1000` names a real
> model in 95.7 % of cases.** So `section_012` answers *"which creatures does this map load"* —
> directly, from a 64-byte table, without running the game.

### The zeroes are explained — the mapping is per-letter, not global

*Independent audit, `repos-4b`, 2026-09-05, own parser over 1,114 containers and own stem
extractor over the `obj_finish` tree (4,230 file basenames, reduced to per-letter model-number
pools).* **The `id + 1000` rule was only ever tested against `id + 1000`.** Testing the
*direct* rule as well resolves four of the five categories this section called unexplained:

| letter | distinct ids | `id + 1000` resolves | **`id` resolves directly** | rule |
|---|---:|---:|---:|---|
| `c` | 16 | 5 | 0 | `id + 1000` |
| `m` | 57 | **50** | 0 | `id + 1000` |
| `n` | 112 | **77** | 0 | `id + 1000` |
| `b` | 12 | 0 | **10** | **`id`** |
| `g` | 97 | 0 | **77** | **`id`** |
| `s` | 13 | 0 | **10** | **`id`** |
| `t` | 10 | 0 | **8** | **`id`** |
| `w` | 54 | 7 | 14 | ambiguous |
| `C` `N` `S` | 111 | 0 | 0 | neither |

**`g`, `t`, `s` and `b` are model-backed after all.** Their models are numbered from `0001`
(`g0001`, `t0004`, `b0001`, `s0031`) while `c`/`m`/`n` models are numbered from `1000` (`c1004`,
`m1002`, `n1059`) — so one offset cannot serve both and the section stores a **category-relative**
number. Applying the right rule per letter takes the overall resolution from **28.8 % to 52.1 %** of
distinct `(letter, id)` pairs.

**`C`, `N` and `S` still resolve under neither rule.** The `obj_finish` tree does carry `hc`, `hn`
and `hs` stem families, and mapping the uppercase letter to the `h`-prefixed family gives 13 of 40,
13 of 66 and 1 of 5 — ~~**better than zero and not a finding**: each id set is larger than its~~
~~candidate pool (40 ids against 17 `hc` stems), so the mapping cannot be complete whatever it means.~~
~~Recorded as a lead.~~ *(answered: the uppercase letters are the high-detail tables, indexed per file, not per stem — UQ-333 below; 2026-10-02, OPUS)* *(corrected 2026-10-02, OPUS: `obj_finish/in/high` ships 47 `hc*.cm` files over those 17 stems, read through `vbf_load_index`; UQ-333's table holds 48 entries)*

## 6. Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Is the entry `u32` rather than two `u16`? | **Killed by the corpus.** Read as `u32` the values are sparse and meaningless; read as `(u16,u16)` the second column collapses to **11 values, all ASCII letters**. A 4-byte read cannot produce that by chance. |
| Is the padding meaningful? | **No** — zero in 842 of 842, checked byte-wise past `4 + 4×count`. |
| Is `id = A + 1000` real, or a coincidence of small numbers? | **Real for `m`, and the control is the failure rate elsewhere.** 95.7 % for monsters against 0 % for `g`/`t`/`s` — a rule that fired everywhere would be the suspicious result. |
| Was the first stem extractor trusted? | **No, and it was wrong.** The first regex found only **26** model stems because `obj_finish` has an extra path level, and it produced a 0 % hit rate for every letter. **The instrument was broken, not the hypothesis** — corrected to 935 stems before any conclusion was drawn. |
| Does the handler parse the table? | **No.** Complete 186-byte body read; it stores a pointer and clears a bit. **No `Inert` row is claimed** for fields it does not touch. |

### Audit pass 1 — 2026-09-05, `repos-4b` (independent; not the author)

**Every corpus claim was re-derived from the 1,115-file corpus rather than re-read, and all of them
reproduce exactly.** This is the "attacked and failed to break" half.

| claim under attack | re-derived result |
|---|---|
| present in 842 of 1,114 containers | **842 / 1,114** ✔ |
| size 64–256 B, median 64; 726@64, 63@128, 52@256, one@192 | **identical, including the single 192-byte outlier** ✔ |
| `+0x00` count, 1–55, median 3 | **1–55, median 3** ✔ |
| 6,771 entries total | **6,771** ✔ |
| column 2 takes exactly 11 values, all printable ASCII | **11 values; all `.isalpha()`; every per-letter count matches to the entry** ✔ |
| padding past `4 + 4×count` is zero | **842 / 842** ✔ |
| `4 + 4×count` never exceeds the section length | **842 / 842** ✔ |
| the `0x022C6DA8` aliasing warning | **Correct.** An instruction-level reference census returns **4** hits — store in the handler, store in init (`0x0032F4E2`), load + store in teardown (`0x0032F0B7`, `0x0032F0F0`). Exactly the shape the sheet warned about, and the warning was right to refuse an `Inert` row. |

**What broke:** the §3 claim that the handler stores the pointer in one place. It stores it twice —
see the amendment in §3. **The sheet named the precedent that would have caught it and did not apply
it to its own call site**, which is the finding worth recording, more than the missing field is.

**A bounded consumer search, run and failed — recorded so it is not repeated blind.**
`FUN_00263FF0(idx)` returns the manager record in `RAX`, so the founded search is: inside the **93**
functions that call it, look for a read of `[rax + 0x100]` — or of a register copied from `rax` —
within 40 instructions of the call. **Zero hits.** That does **not** mean no consumer exists: the
record pointer can be cached in a field, passed as a parameter, or re-derived further from the call.
**It means the cheap founded search is exhausted and the next attempt needs a different handle.**
| *(audit 2026-09-05, `repos-4b`)* Does the whole structural reading reproduce from an independent parser? | **Yes, exactly.** 1,114 containers, **842** with the section, **6,771** entries, sizes 64/128/192/256 at 726/63/1/52, count range 1–55, `4 + 4×count ≤ length` in 842/842, padding all zero in 842/842, and column 2 exactly **11** distinct values with the per-letter counts matching this sheet term for term. **Nothing structural moved.** |
| *(audit)* Is the second `u16` really a `u16`, or a byte plus something? | **A `u16`.** Its **high byte is 0 in all 6,771 entries** — a `u8` letter followed by an unrelated byte would not be. |
| *(audit)* Is `id = model − 1000` a general rule? | **No — and that is the one claim that broke.** It is right for `c`, `m`, `n` and wrong for `b`, `g`, `s`, `t`, which resolve under the **direct** rule. See §5. The sheet's own 0 % rows were the symptom; they were read as *"these categories are not model-backed"* when the cause was that only one of the two rules had been tried. |

## `UQ-334` narrowed from the shipped trees (FABLE, 2026-09-22)

`UQ-334` asks whether the `n` ids that resolve to nothing are **a different numbering** or
**absent models**. Two measurements over the extracted game, and the first one is a hypothesis of
mine that the data killed.

### The shipped PC tree adds nothing — *my own first guess, refuted* (FABLE, 2026-09-22)

The 2026-09-05 audit built its stem pool from **`ps2data/obj_finish`**. The shipped PC game also
carries a character tree at **`gamedata/d3d11/artdata/chr`**, so the obvious hypothesis was that
the unresolved ids name models the PS2-derived pool never saw. **They do not.**

| tree | `n` stems |
|---|--:|
| `ps2data/obj_finish` | **175** |
| `gamedata/d3d11/artdata/chr` | **173** |
| **present in the D3D11 tree and NOT in `obj_finish`** | **0** |

*The D3D11 pool is a subset.* The same holds for `m`, `b`, `g`, `s`, `t` and `w` — only `c` gains
anything (4 stems). **So an unresolved `n` id is not a model hiding in the tree the audit did not
read**, and that branch of the question is closed.

### The numbering is sparse enough that absent models need no second rule (FABLE, 2026-09-22)

| | |
|---|--:|
| `n` stems, union of both trees | **175** |
| the numbering range they occupy | **`n1009` … `n1248`** — 240 slots |
| **gaps inside that range** | **65** |
| distinct `n` ids that do not resolve | **35** (112 distinct, 77 resolve) |

**There are nearly twice as many holes in the model numbering as there are unresolved ids**, so
*“the model was never shipped”* accounts for all 35 without positing a second numbering at all.
**The categories that resolve well show the same relationship**, which is the control: `m` has 254
stems over a 282-slot range — **28 gaps** against only **7** unresolved ids.

> **This narrows the question; it does not close it.** Sufficiency is not proof. What would settle
> it is checking whether those 35 ids land **inside** `1009…1248` — in which case they are simply
> absent models — or **outside** it, which would be the signature of a different numbering. **That
> ~~needs the id list, and the database does not store one~~**~~: the 112 came from `repos-4b`'s own~~
> ~~parser over 1,114 containers, and no `members/` file on this page carries them.~~ *(answered: `members/section012-model-ids.tsv` stores it, and UQ-334 is answered from it, 2026-09-25; 2026-10-02, OPUS)* *Writing that
> list out is the single cheapest thing that would finish `UQ-334`.*

## 7. What is not known

- [x] **UQ-332.** **Who reads the stored pointer** — the consumer that walks the entries. Until it is read,
      nothing here says what the engine *does* with the manifest. **Amended 2026-09-05: the search
      target is `managerRecord[+0x100]`, not `0x022C6DA8[manager]`** — the handler stores to both and
      the manager record is the one a consumer would reach through `FUN_00263FF0`. The bounded
      search over that accessor's 93 callers is already spent (§6); it returned nothing.
      **Narrowed 2026-09-14 (FABLE): a second, wider search also finds no reader.** `Tools/work/FABLE/regprose/mgr_field_census.py` tracks record pointers over every function in `.text`, without a control-flow graph. It follows:
      - the accessor's return value;
      - RIP-relative and image-base-relative `lea`s into the five-slot array, including bases already biased by a field offset, which is the setter's own idiom (`lea` of `02098F10`);
      - the current-manager cache `02099D70`;
      - register copies, `add`/`lea` offsets and stack slots;
      - arguments passed into callees, to a fixpoint (38 + 5 + 1 + 1 seeded callees).
      Across the whole image, exactly **two** accesses land on `+0x100`, and **both are writes**: the setter `FUN_0026CE40` (`0026CE51`) and the clear in `ActorManager_BindLoadedDefinitionPayload` (`0026CC31`, which stores 0 while it resets the record's fields). The known clear was recovered only once the image-base idiom was modelled, which is the recall check for the census.
      **What is not excluded:**
      - **Indirect escapes.** Three table-dispatched functions with no direct callers write `{record, index}` through an out-pointer (stores at `0034E4B3`, `0034F41D` and `0034FCB7`), and a fourth writes the slot-0 record to `+8` of one (`0034AF69`). A consumer reached through those handles, or through an indirect call, is outside the census.
      - **Other copies.** A copy of the record pointer held in another structure is also outside it.
      - **The other store.** The `022C6DA8[manager]` copy has one load, in `ActorResource_ResetManagerLoadState` (`0032F0B7`). That load only tests the pointer before a release call, and the release is gated on `005C5230(5)`, a folded stub that returns 0. It then clears both stores, the second through the setter with 0 (`0032F0FA`). So it is not a walker.
      - **The container route.** A reader could find section 12 through the container's section directory rather than through either stored pointer.
      **ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5), static: nothing in this executable walks it.** The only directory reads
      of section 12 are the loader's presence test and handler dispatch; the four sync-verb escapes' polls read only the
      manager byte `+0x10`; and no caller of the model-id decoder takes its id from a list. See
      [the UQ-332 record](../../_index/candidates/uq332-no-reader/README.md) (3 checks).
- [x] ~~Why `g`, `t`, `s` and `b` ids resolve to no model~~ — **closed by the 2026-09-05 audit**: they resolve under the *direct* rule, not `id + 1000`. Their models are numbered from `0001`. See §5.
- [x] **UQ-333.** What `C`, `N` and `S` are. Uppercase variants of `c`/`n`/`s` is the obvious guess and **is not
      evidence**; ~~no `obj_finish` category matches them~~ *(corrected (FABLE, Claude Opus 5.5, 2026-09-26): `obj_finish\in\high`
      does; answer below)*.
      **ANSWERED (FABLE, Claude Opus 5.5, 2026-09-26), static: they are the high-detail model tables, `hc`, `hn` and `hs`.**
      - **The format.** An entry `{u16 id, u16 letter}` read as a u32 is `(letter << 16) | id`. That is the
        engine's model-id format: its decoder reads the number from bits 0–15 and the letter from bits 16–23.
      - **What the decoder does with each letter** (executed under Unicorn):
        - `C` → resource-path kind 15, index = id; `c` → kind 14, index = id × 25;
        - `N` → kind 20, index = id; `n` → kind 19, index = id × 25;
        - `S` → kind 24, index = id; `s` → kind 23, index = id × 25.
      - **What those kinds hold.** Read from the arrays `ResourcePath_Init` installs:
        - kinds 15, 20 and 24 are flat lists of `obj_finish\in\high` models — 48 `hc*.cm`, 87 `hn*.cm` and
          5 `hs*.cm`;
        - kinds 14, 19 and 23 are the chara, npc and summon trees, in 25-slot blocks (a `.cm` and its `.ca` takes).
      - **The data fits the tables.** Every `C` id (0–46) is below 48, every `N` id (up to 86) below 87, and every
        `S` id (0–4) below 5 (`members/section012-model-ids.tsv`). The `N` and `S` maxima are exactly the
        tables' last indices.

      *Limits:*
      - The section's reader is still unlocated (the census above), so no instruction is shown passing an entry
        to the decoder.
      - The **lowercase** ids do not follow the decoder's block order: kind 14 holds `c1004`, `c1029`, `c1010` at
        blocks 0, 1, 2, while §5's rule reads `c` ids as model − 1000. So that reader translates lowercase ids
        somehow, and the direct-index reading of the uppercase ids rests on the range fit, not on a traced read.

      Control: [`uq333_letters.py`](../../_index/candidates/uq333-high-detail-letters/uq333_letters.py) (5 checks, FAILS 0).
      *Narrowed 2026-09-25 (FABLE, Claude Opus 5.5): they are not ordinals into the script's own entry list.*
      [`members/section012_ordinal_test.py`](members/section012_ordinal_test.py) compares every id with
      its container's `section_000` entry count. Only **77.0 %** of `C` ids (339 of 440, 128 containers) and
      **36.6 %** of `N` ids (48 of 131, 72 containers) fall below it. `N` ids run to 86 in scripts with 36
      entries. `S` (8 ids, values 0–4) passes, but values that small cannot discriminate.
- [x] ~~What `FUN_0026CE40` does with the manager index immediately after the store.~~ **Answered
      2026-09-05.** It takes **two** arguments, not one — the question as posed assumed a single
      manager index and that framing is what kept it open. It stores the section pointer into
      `managerRecord[+0x100]`. See §3.
- [x] ~~**UQ-334.** Whether the 30 % of `n` ids that resolve to nothing are a different numbering or absent models.~~
      **ANSWERED 2026-09-25 (FABLE, Claude Opus 5.5): both, and the split is measured.** Of the 35 unresolved
      `n` ids, **26 fall inside** the `n1009`…`n1248` model numbering, in its gaps: absent models. **9 fall
      outside** it, and they are exactly ids **0–8** (`n1000`…`n1008`), a contiguous block below the lowest
      model. That is not what missing models look like. What ids 0–8 denote is not established; no engine
      reader of this section is known (UQ-332). See
      [§ The id list, written out](#the-id-list-written-out--uq-334-answered-fable-claude-opus-55-2026-09-25).
      *Narrowed 2026-09-22 (FABLE):* the shipped D3D11 character tree adds **zero** `n` stems over the
      `obj_finish` pool the audit used, so they are not models in an unread tree; and the `n` numbering
      has **65 gaps** in its `n1009…n1248` range against **35** unresolved ids, so *absent models*
      suffices without a second numbering. ~~**Not closed** — that is sufficiency, not proof, and the id~~
      ~~list needed to finish it is not stored anywhere.~~ *(answered: closed by the 2026-09-25 answer above, from `members/section012-model-ids.tsv`; 2026-10-02, OPUS)* See the section above.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| layout, padding, counts | 842 of 842 containers, `census_ebp_container.py` directory walk | 1 |
| dispatch gate and call site | complete body of `0x003304A0` | 1 |
| handler stores and does not parse | complete 186-byte body of `0x0032FB70`, capstone against the authorized EXE | 1 |
| table addresses | `r14 = rip - 0x20FB8E` at `0x0032FB87` → image base `0x00120000` | 1 |
| column 2 is a category letter | 6,771 entries, 11 distinct values, all printable ASCII | 1 |
| `id = A + 1000` for `c`, `m`, `n` only | 50/57 `m`, 77/112 `n`, 5/16 `c`, against 4,230 `obj_finish` stems | 9 |
| `id` resolves *directly* for `b`, `g`, `s`, `t` | 10/12, 77/97, 10/13, 8/10, same stem set | 9 |
| structural reading reproduces independently | own parser, 1,114 containers, every figure identical | 1 |

**Superseded readings:** the first model-stem extractor matched 26 stems and reported 0 % for every
letter; corrected to 935 stems. The 0 % result was an artefact of the extractor, not a finding.

**Superseded 2026-09-05 by independent audit (`repos-4b`):** *"column 1 is the model number less
1000"*, stated without qualification in the §2 fence. It holds for three letters of eleven. The
audit built its model pools per letter prefix (`b` 17, `c` 17, `g` 103, `m` 254, `n` 175, `s` 26,
`t` 17, `w` 326, plus `hc`/`hn`/`hs`) from the same `obj_finish` tree, and under the *direct* rule
the four "unexplained zero" categories resolve. **The structural half of this sheet survived the audit unchanged; only the id-mapping
claim moved.**

## 9. Related

- [the container](../Container/ebp2-container.md) — the directory this section is dispatched from
- [`_index/COVERAGE.md`](../../_index/COVERAGE.md) — the `section_008` aliasing case this §3 defers to

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings become reportable once citations written 0x... or FUN_... count (R5); tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Presentation — CLIENT.** The 21-byte manager-record accessor this page cites is called by Presentation bodies of 511 to 4,782 bytes.
- **Input — CLIENT.** The same accessor is called by Input bodies of 1,002 and 1,936 bytes.
- **Movement — CLIENT.** The same accessor is called by Movement bodies of 702 and 2,026 bytes.
- **Actor — SERVICE (1 edge).** 1 outbound (page-cited `ActorResource_FinalizeManagerRuntimeAfterLoads` (0032F1B0) call Actor bodies `0037AA90`). Substantive edges include `ActorResource_FinalizeManagerRuntimeAfterLoads` (0032F1B0) calls `0037AA90`.
- **ActorEntity — CLIENT and SERVICE (79 edges).** 53 inbound (ActorEntity bodies `0032FA10`, `0032FAC0`, `ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources` (003304A0) call page-cited `00263FF0`, `ActorResource_FinalizeManagerRuntimeAfterLoads` (0032F1B0), `0026CE00`); 26 outbound (page-cited `ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources` (003304A0), `ActorResource_FinalizeManagerRuntimeAfterLoads` (0032F1B0), `0032FB70` call ActorEntity bodies `00263FF0`, `ActorResource_FinalizeManagerRuntimeAfterLoads` (0032F1B0), `0037B290`). Substantive edges include `0026CE00` is called by `ActorResource_ResetManagerLoadState` (0032ED80); `0026CE00` is called by `0032FA10`; `0026CE20` is called by `ActorResource_ResetManagerLoadState` (0032ED80); `0026CE20` is called by `0032FAC0`; the remaining edges run through shared helpers the page cites.
- **Party — MECHANICAL (1 edge).** 1 outbound (page-cited `ActorSystem_InitializeManagerRuntime`
  (`0026CE60`, cited in the `0032F1B0` row correction) calls the 5-byte Party thunk `00358BB0`) -
  shared plumbing, not a Party relationship. *(residue bullet 2026-10-02, SWE2-CONTRACT)*
- **UI — SERVICE (1 edge).** 1 outbound (`0026CE60` calls the 67-byte UI body `00253A30`).
  *(residue bullet 2026-10-02, SWE2-CONTRACT)*
- **WorldAreaField — CLIENT and SERVICE (2 edges).** 1 outbound (`0026CE60` calls
  `BattleSystem_InitializeAreaState` (`002342F0`)); 1 inbound (WorldAreaField body `003775D0`
  calls the page-cited light binder `0037AA90`). *(residue bullets 2026-10-02, SWE2-CONTRACT)*

## The id list, written out — UQ-334 answered (FABLE, Claude Opus 5.5, 2026-09-25)

The narrowing above named the missing piece: the id list, which no file stored.
[`members/section012_model_ids.py`](members/section012_model_ids.py) writes it to
[`members/section012-model-ids.tsv`](members/section012-model-ids.tsv). It reads every `us` `.ebp`
(directory slot 12 at `+0x40`) and resolves each `(letter, id)` against the stems of the full
extract's `ps2data/obj_finish` tree, using §5's two rules.

**Controls, all reproduced exactly:** 842 containers carrying the section, 6,771 entries, 112
distinct `n` ids of which 77 resolve, 175 `n` stems over `n1009`…`n1248`, and 65 gaps. The script
refuses to write if the first two differ.

| unresolved `n` ids | count | where they fall |
|---|--:|---|
| `n1010` `n1011` `n1012` `n1015` `n1023` `n1024` `n1025` `n1029` `n1041` `n1049` `n1050` `n1051` `n1052` `n1063` `n1065` `n1074` `n1086` `n1088` `n1116` `n1157` `n1158` `n1160` `n1161` `n1165` `n1170` `n1173` | **26** | inside the model numbering, in its gaps |
| `n1000` … `n1008` (ids **0–8**) | **9** | below the lowest model, contiguous |

**So UQ-334's either/or has both answers.**
- 26 are models that were never shipped, which is the reading the narrowing found sufficient.
- 9 are a separate low range. Ids 0–8 are all used, and no model is numbered anywhere near them,
  which points to a different meaning for small `n` ids rather than to missing files.
- In 146 containers those low ids all sit below the container's entry count. With values that
  small the test cannot discriminate, so it is not evidence that they are entry ordinals.

The same ordinal test **fails for `C` and `N`** (77.0 % and 36.6 %), which narrows UQ-333.
