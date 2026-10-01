---
system: The .nmb per-area index and the resource-kind path table
category: 02-Resource-And-Asset-Pipeline
status: DOCUMENTED — the five requests are resolved and kind 26 does resolve (SWE2-CONTRACT DD batch 9); the kind-37 size array ends at index 2,963; stated limit: 36 of the request function's 51 calls pass a computed kind, so 'nothing else asks for kind 26' is not claimed (owner re-status 2026-09-30, OPUS; was: five requests remain unresolved (incl. whether kind 26 resolves) and where the size array ends is not established)
owner_layer: CodeDomain:Resource.PathTable
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
corpus_validated: "166 / 166 areas, both locale copies, extracted from FFXII_TZA.vbf 2026-09-04"
last_reviewed: 2026-09-04
archive_formats:
  - "nmb"
audit:
  passes: 1
  last_pass: 2026-09-05
  last_pass_state: GN160-corpus-and-code-reparse-repos-1e — all 332 archive entries decompressed and re-parsed, both path functions re-decoded; 11/11 corpus claims and every instruction anchor confirmed, no defects found
  crossref_clean: false
  reopened_count: 0
---

# `.nmb` — the per-area index, and the path table that addresses it

> A tiny per-area file — a count, an offset table, and a list of entries — that ships beside every
> [`.ard`](README.md). The engine reaches it as **resource kind 26** of a global path table, and
> that table holds **321 areas** where only **166** ship a file.

**Corpus validation, before anything else.**

| | |
|---|---|
| files examined | **332 `.nmb`, extracted from the archive** — every one in `ps2data/plan_master/{ch,in}/plan_map/<area>/area/` |
| logical corpus | **166 areas.** Each ships twice, under `ch` and `in`, and the two copies are **byte-identical in 166 of 166** — re-hashed here, not inherited |
| this unit present in | **166 of 166** areas that have an `.ard`; the stem sets are identical and neither half ever ships alone |
| size range | **8 B – 162 B**, median 50 B, mean 56.3 B, **19 distinct sizes** |
| entries held | **0 – 22 per area, 1,146 in the corpus** |

Every claim below was checked over all 166 areas unless a smaller count is given.

---

## 1. What the player sees

**Nothing directly.** No `.nmb` byte reaches the screen.

What it does is sit beside the `.ard` for every region of the world that has one — Dalmasca
Estersand, the Garamsythe Waterway, the Henne Mines — and carry a short list, between zero and
twenty-two entries long, whose length tracks how big that area's `.ard` is. **Four areas have a
`.nmb` with no entries at all**, which is the shipped way of saying "this area has none of whatever
this counts."

*(SWE2-CONTRACT, 2026-09-30, DD batch 9.)* **In the shipped game no `.nmb` is ever loaded.** The one piece of
code that asks for them, a per-frame assembler, is linked but never switched on (§3, FZ-8). Even if it ran, it would
stop at area 300 and miss the twenty `tri_*` areas at the end of the table. Players on the Korean and Chinese
language settings would get the `ch` copies and everyone else the `in` copies, which are byte-identical anyway (§7).

**The honest summary is that this file is small, structurally simple, and semantically undecided.**
What it *indexes* is settled below; what its entries *mean* is not, and §7 says so rather than
inventing a story.

## 2. The layout

```struct NmbHeader base=file size=0x04
+0x00  u16  count    number of entries -- 0..22
+0x02  u16  version  always 0x0064 (100) in 166 of 166
```

Immediately after the header, at `+0x04`, comes an offset table of **`count + 1`** `u32` values —
one per entry plus a terminator — and then the entries themselves.

    +0x04  u32 offset[count + 1]   file-relative, strictly ascending

*Deliberately not a `struct` fence: `check_layouts.py` requires a literal array length and this one
is `count + 1`. A fence with an invented length would be worse than prose, so the variable-length
table is stated here and only the fixed-size structures above and below are fenced.*

**The table has `count + 1` entries, not `count`.** The last one is the file size, so every entry's
length is the distance to the next offset and the final entry is bounded like all the others. This
is the same "length is the distance to the next offset" idiom the EBP container uses, but here the
terminator is stored explicitly rather than implied by EOF.

```struct NmbEntry base=entry size=0x03
+0x00  u8  tag    0x12 in 1,146 of 1,146
+0x01  u8  code   0xBA in 1,120, 0xBB in 26
+0x02  u8  _zero  0x00 in 1,146 of 1,146
```

**Every entry in the corpus is exactly 3 bytes**, but that is an observation about the data, not a
constraint in the format: the offset table can express any length, and nothing read here requires 3.
A sheet that called the entry a fixed 3-byte record would be over-reading the corpus.

**File size is therefore `4 + 4*(count+1) + 3*count` = `8 + 7*count`**, which is exactly the 19
observed sizes — 8, 15, 22, 29, … 162 — with no size unaccounted for.

## 3. The loader contract

**A `.nmb` path is resolved by `(kind = 26, index)` against a global table of path tables.** The
array at kind 26 holds one entry per area, so `index` selects an area — ~~but **what a caller would
actually pass is not established**, because no request for kind 26 resolves. See *"The index the
caller passes is not the raw id"* below before treating an array position as an argument.~~
*Corrected 2026-09-30 (SWE2-CONTRACT, DD batch 9): the index is the array position, and kind 26 does resolve.* The
file-size table sizes kind 26 by array position (FABLE, 2026-09-11, below). A kind-26 request resolves to a path
through the third consumer, `002DF780`, reached from the request machine. It never goes through `ResourcePath_Get`,
whose eleven sites all resolve to other kinds. See *"All eleven sites resolve, and the kind-26 route"* below.

**`ResourcePath_Get` — `0x002DF980`, 22 bytes, the entire function:**

```
ResourcePath_Get(int kind, int index):
    movsxd rax, ecx                       0x002DF980   kind, SIGN-extended
    lea    r8, [rip + 0x1e7f676]          0x002DF983   -> g_pathTables = 0x0215F000
    movsxd rcx, edx                       0x002DF98A   index, SIGN-extended
    mov    rax, [r8 + rax*8]              0x002DF98D   pick the table for `kind`
    mov    rax, [rax + rcx*8]             0x002DF991   pick the path for `index`
    ret                                                -> char*
```

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| `kind` | `ResourcePath_Get` `0x002DF980` | — | — | **no bound of any kind — see below** |
| `index` | `ResourcePath_Get` `0x002DF98D` | — | — | **no bound of any kind — see below** |
| `+0x00` count | not read by any function read here | — | — | — |
| `+0x02` version `0x0064` | — | — | — | **yes — no reader found; the constant `0x0064` is far too common to census, so this rests on no reader existing in the functions read, not on a scan** |

> **Neither index is checked.** There is no comparison, no mask and no default in those 22 bytes —
> both arguments are sign-extended and used directly as scaled offsets. A caller passing a bad
> `kind` or `index` reads whatever qword lies there and returns it as a `char*`. **The safety is
> entirely in the callers**, which were not audited here; that is a statement about this function,
> not a claim that the game can be made to fault.

**`ResourcePath_Copy` — `0x002DF880`** is the same two-step lookup plus a bounded copy: it returns
`-1` when the resolved pointer is NULL (`0x002DF89E`), otherwise copies bytes until a NUL or until
`maxLen` is reached (`0x002DF8C4`), then writes a terminator at `dst[copied]` (`0x002DF8D1`).
**The terminator is written after the length check, so the destination needs `maxLen + 1` bytes**,
not `maxLen`. `0x002DF780` is a third caller of the same table, reached from `0x0046E030`.

**No caller requests kind 26 with a literal, and the search that failed has a positive control.**
*Added 2026-09-04 by `repos-4b`.*

1. A byte-pattern scan of the whole `.text` for `mov ecx, 26` (`B9 1A 00 00 00`) and `mov edx, 26`
   (`BA 1A 00 00 00`) followed within 48 bytes by a `call` to `0x002DF980`, `0x002DF880` or
   `0x002DF780`: **zero hits.**
2. **The control:** the identical scan over every kind 0–63 *does* find sites — kind 11 at
   `0x002FC599`, kind 28 at `0x001B7F93` and `0x0035B8AE`. The instrument finds literal kind
   requests; it does not find one for 26.
3. **Site-by-site resolution of all eleven `ResourcePath_Get` call sites.** Six now resolve, and
   **every one of them resolves away from 26**:

| site | kind | how it was resolved |
|---|---|---|
| `0x001B7F93` | 28 | literal in the calling instruction |
| `0x0035B8AE` | 28 | literal |
| `0x002FC599` | 11 | literal |
| `0x0032FD5A` | **5 or 8** | both literals in the same function — `0x0032FD30` and `0x0032FD3F`; kind 5 is the `{ebp, mot}` map-script slot |
| `0x003322C8` | **5, 8 or 37** | `FUN_00332250` whitelists its kind argument before use — `cmp ebx,8` / `cmp ebx,0x25` / `cmp ebx,5` at `0x00332285`–`0x00332292`, and anything else branches past the call. **37 is not a content kind** — see below |
| `0x00379A5A` | **4** | passed through from `FUN_00379A10`'s single caller, `mov ecx, 4` at `0x00378B51` |

~~**Five remain unresolved**, and the reason is recorded rather than glossed: `0x001BB397` takes the
kind from a returned value; `0x002EEF70` from an object field (`[rdi+0xC40]`); and `0x001DA31B`,
`0x001F5E64` and `0x00863144` sit behind wrappers whose graph "caller" is a 9–179-byte tail-call
stub, so the real caller is a further level up and was not chased.~~
*Corrected 2026-09-30 (SWE2-CONTRACT, DD batch 9): all five resolve, and none can be 26.* Each takes its
`(kind, index)` pair from a decoder that the page had not read. The decoders' whole output sets are below.

> ~~**This is an absence of a *literal or statically-resolvable* request, and no more.** Five of
> eleven sites still take the kind from data this pass did not resolve, so a data-driven request for
> kind 26 remains possible. **It is not evidence that `.nmb` is never loaded** — it is the reason
> §7's open question about the consumer is still open.~~
> *Corrected 2026-09-30 (SWE2-CONTRACT, DD batch 9): no site is left unresolved, so `ResourcePath_Get` is never
> asked for kind 26.* That still does not mean `.nmb` is never loaded through another route. The kind-26 route is
> the request machine and `002DF780` (below), and FZ-8 shows that its one issuer never starts.
>
> **And a scan alone could not settle it in either direction.** `repos-4b` and `repos-1e` established
> on the `.sab` format that a constant comparison can be built against a **`.rdata` tag reached
> through a memory operand** (`cmp eax, [rip+0x541614]`), which a `.text` immediate scan returns zero
> hits for even though the check is real and runs on every load. A kind id loaded from a `.rdata`
> word would be invisible to step 1 the same way. **Step 1's control tells you the instrument finds
> literals; it does not tell you no request exists.**

### All eleven sites resolve, and the kind-26 route (SWE2-CONTRACT, 2026-09-30)

*DD batch 9, checker [`b9_vbf_nmb.py`](../../../_index/candidates/swe2contract-ddres-b9-0930/b9_vbf_nmb.py)
N1–N6.*

| site | decoder | kinds it can pass |
|---|---|---|
| `0x001BB397` | `002E98F0(id, &kind, &index)` (`001BB38A`) | the id-letter set below |
| `0x001F5E64` | `002E98F0` (`001F5E59`), on the id in `[rsi+0x480]` | the id-letter set |
| `0x00863144` | `002E98F0` (`00863137`) | the id-letter set |
| `0x002EEF70` | `002ED6F0` (`002EEF63`), on `(edi << 16) \| esi` (`002EEF50`–`002EEF5F`) | the id-letter set |
| `0x001DA31B` | `0032F170(0, id, &kind, &index)` (`001DA2FB` `xor ecx,ecx`) | **5** only: manager 0 takes the `id * 3` arm (`0032F172` → `0032F19E`–`0032F1A1`) |

**The id-letter decoder `002ED6F0`.** A packed id holds its number in the low 16 bits (`002ED6F0`) and a letter in
bits 16–23 (`002ED6F7`–`002ED6FA`). A jump table over `'C'`…`'w'` (`002ED6FD`–`002ED724`) maps the letter to a kind
and an index multiplier, and every other letter goes to kind 1 (`002ED840`). The whole output set is:

- `b` → 22, `c` → 14, `g` → 13, `m` → 34, `n` → 19, `s` → 23, `t` → 25, `w` → 16
- `C` → 15, `M` → 18, `N` → 20, `S` → 24
- every other letter → 1

The table's own kinds agree with these letters: kind 22 begins `b0001.cm`, kind 14 `c1004.cm`, kind 34 `m1002.cm`.
`002E98F0` is the same decoder plus 0x33 on a kind-1 index (`002E9905`–`002E990A`). **26 is not in the set.**

So `ResourcePath_Get`'s eleven sites resolve to kinds 1, 4, 5, 8, 11, 13–16, 18–20, 22–25, 28, 34 and 37, and
**never to 26**. `ResourcePath_Copy` (`0x002DF880`) has one site, `00377E09`. It receives kind 4 from its only
caller (`mov r9d, 4` at `00378B1A` → `00377DED` → `00377DFD`).

**Kind 26 resolves through the request machine instead.** The route is:

1. `0032E620(kind, index, …)` queues a request slot through `0032E870`, which stores the kind byte at slot `+0x21`
   (`0032E943`) and the index at `+0x24` (`0032E902`).
2. The machine `0032E070`, in state 1 (`0032E0BD`), reads both (`0032E0D3` / `0032E0DB`) and calls `0046E030`
   (`0032E0F1`), which calls `002DF780` (`0046E03E`).
3. `002DF780` refuses the request when `size[kind][index]` in the `.fst` is `-1` (`002DF7B0`). Otherwise it fetches
   `g_pathTables[kind][index]` (`002DF7BF` / `002DF7CC`).

So a kind-26 request names the `.nmb` at its array position. Of `0032E620`'s 51 call sites, 15 pass an immediate
kind. **The only one passing 0x1A is `00324637` in the assembler `00324510`**, which FZ-8 (below) shows never
starts. The other 36 sites compute their kind. They are not resolved here, so this is not a proof that nothing else
could ask for kind 26.

**The assembler would not cover all the shipped areas even if it ran.** It loops over ids 0–300
(`mov edi, 0x12d`, `00324597`; `cmp eax, edi`, `00324678`) through its `{u32 size, u32 requestId}` pairs at
`022C27B8`, stride 8 (`00324607`). So that table ends at `022C311F`. The `.fst` sizes kind-26 ids up to 320, and the
20 areas at ids 301–320 are `tri_a` … `tri_t`. This is a measurement, not a claim about how the code came to be:
the assembler's bound (301) is smaller than the path table (321).

**Namespace 37 in that whitelist is a size override, not a content kind** — which matters here
because it is the difference between "three formats can reach this path" and "two can". For
managers 1..3 the same load path probes the size twice at **one index**, `Resource_GetSize(primary)`
then `Resource_GetSize(37, sameIndex)` at `0x0032FDC4`–`0x0032FDDC`, and **the namespace-37 answer
is the one stored** (`0x0032FDE8`); the primary result is computed into `r12d` and discarded on that
path, kept only when the override is skipped (`0x0032FDF1`). Reading by `repos-1e`, reproduced here
from the bytes.

> **RETRACTED, 2026-09-04.** An earlier version of this paragraph said *"namespace 37's path array
> is empty — a namespace with no paths cannot resolve a filename"*, offered as proof that 37 is not
> a content kind. **That was false and the error was mine**: my slot enumerator stopped after three
> consecutive NULLs, and **kind 37's arrays begin with 120 NULL entries**, so a head-only read
> returned zero. Re-walked correctly, both bases are **fully populated**. Kept visible rather than
> silently replaced; see §6.

**What namespace 37 actually is: a fully populated parallel table with namespace 8's exact stride-4
layout**, consulted in place of 8 for managers 1–3. Re-walked from both bases with NULLs treated as
holes rather than terminators, the `in`-tree array partitions by index parity **with no exceptions**:

| `index mod 4` | extension | count |
|---:|---|---:|
| 0 | `ebp` | 329 |
| 1 | `mot` | 329 |
| 2 | `snd` | 329 |
| 3 | `vpcjp` | 329 |

**329 logical ids × 4 assets — exactly the `index = id * 4` rule namespace 8 uses.** That structural
identity is *why* 37 can substitute for 8 at the same index: same stride, same slot meanings,
different content. **An override has to have the overridden table's shape, and it does.** Reading and
correction by `repos-1e`; the parity partition reproduced here from the bytes.

> ~~**The counts are extent-dependent and are not asserted.** `repos-1e` measured 2,168 and 1,972
> entries scanning to indices 3961/3999; bounding each array at the next base in address order gives
> **1,316 each**. The two runs disagree because *where an array ends* is not established, only where
> it starts. The parity partition and the "not empty" result are robust to that; **the totals are
> not, and neither of us should quote one until the extent rule is settled.**~~
> *Corrected 2026-09-30 (SWE2-CONTRACT, DD batch 9): each kind-37 array ends at index 2,963, so it has 2,964 slots
> and 1,316 paths.* Two independent bounds give the same end (checker N7):
>
> - **The layout.** Both bases, `01ECBCF0` and `01EA4D00`, are followed by the next of the 94 bases
>   `ResourcePath_Init` installs at exactly 2,964 slots.
> - **The engine's own size table.** All twelve `.fst` files size kind 37 only at ids 120–2,963 (1,080 ids), and
>   `002DF780` refuses any id whose size is `-1` (`002DF7B0`).
>
> Inside those 2,964 slots are 120 head NULLs and **1,316 paths, 329 at each `index mod 4`**. So 1,316 is the path
> count and 2,964 the extent. `repos-1e`'s 2,168 and 1,972 came from scans to indices 3,961 and 3,999, past that
> end and into the next arrays. Kind 26's
> 321 is fixed the same way: the `.fst` sizes kind-26 ids up to 320.

**So the whitelist's three values are two content namespaces and one override of the same shape**,
and the boundary it draws — manager 4's namespace 1 excluded — is drawn identically in the override
probe, which admits only managers 1..3 (`lea eax,[rdi-1]` / `cmp eax,2` / `ja` at `0x0032FDB9`).
**The same fact from two functions**, and that symmetry is unaffected by the retraction above.

*(A literal-site scan finds `37` only at `Resource_GetSize`, never at `ResourcePath_Get`/`_Copy`.
**That is not evidence it never resolves a filename** — it is the same literal-only limit this sheet
applies to its own kind-26 claim, and with a populated array behind it the narrowing applies here
too.)*

**A requester for kind 26 exists, and the file-size table fixes its index (2026-09-11, FABLE).**
`00324510`, from `MainLoop_UpdateAndRenderFrame` (`0022BAEF`), issues `0032E620(0x1a, i, cursor, id)`
for up to 301 ids read from a runtime table at `022C27B8` (`003245F6`–`0032463C`) and publishes the
buffer it assembles at registry slot `02EBF178` — so the literal scan above could not see it, and
it is the reader of `.nmb` bytes §7 says was not found, loading them into one buffer rather than
walking them. And the index is the array position: [the file-size table](../../Loose-Files-And-Size-Tables/file-size-tables-fst.md)
sizes kind 26 by `id`, its 166 sized ids are exactly the array positions of the 166 shipped
`.nmb` files, and every entry equals the archive's size of that file (an affine search over strides
1–4 and offsets −8 … 8 peaks only at `id × 1 + 0`; the same holds for kinds 2, 16 and 21). What
fills the 301 ids, and who reads the assembled buffer, is **FZ-8**.

**`00324510` read whole (2026-09-11) — the assembler, its buffer and its table.** The state word
`022C27A0` runs 1 → 2 → 3: **state 1** installs `003244F0` as both the done and the cancel callback
of a part descriptor at `022C2678` (`+0 count`, `+8 arg`, `+0x10` / `+0x18` the callbacks), writes
the count **301** as the first `u16` of the buffer at `[022C27B0]`, sets the write cursor
`022C3150 = buffer + 0x4BC` (4 + 302 × 4: a `u32 offset[301]` table follows the count), zeroes the
index `022C3148` and the in-flight count `022C27A8`, and moves to **state 2**, which each pass issues
up to ten reads at a time (`022C27A8 < 10`): for area `i` with a non-zero entry in the 301-entry
table at `022C27B8` — **`{u32 size, u32 requestId}`** per area, the size being the request's byte
count — it writes `offset[i] = cursor − buffer`, queues `0032E620(0x1A, i, cursor, size, &desc)`,
stores the request id in the pair, and advances the cursor by `(size + 3) & ~3`. `003244F0(pair)`
runs on delivery or cancel: `pair = {0, −1}` and `022C27A8--`. When `i` reaches 301 and nothing is
in flight, `02EBF178 = buffer` and **state 3**; a state-3 pass with `022C27A4` set frees the buffer
and zeroes the word and the slot. The assembler is driven from three frame loops (`0022AE6F` and
`0022BD3F` in the two loading loops `0022A770` / `0022BC20`, and `MainLoop_UpdateAndRenderFrame`
`0022BAEF`). ~~**Still open:** what writes the 301 sizes and sets state 1 — no rip-relative,
lea-based or image-base-relative write reaches `022C27A0` or the table (whole-image scans of both
forms), so the filler addresses the block through a pointer it is handed — and who reads the
assembled index through the slot.~~ **`FZ-8` answered 2026-09-13 (FABLE):** **nothing does, so the shipped image never builds the index.** `00324510` runs every frame from three loops, but its state word `022C27A0` is BSS zero and state 0 exits at once (`0032451C`–`00324529`); the only stores to it are the machine's own 2, 3 and 0 (`003245CF`, `003246A1`, `00324551`), which need state 1 first. Nothing starts it, allocates its buffer `022C27B0` (whose only store is the release's 0, `0032454A`) or fills the size table `022C27B8`. Instruments, each with a control: RIP-relative references to `022C2790`–`022C3148` — all 17 inside `00324510` / `003244F0`; the addresses `022C27A0`–`022C27B8` and `02EBF178` as 32-bit absolute or image-relative constants anywhere in the file — 0 (control: the jump table `0027FAD0`'s RVA is found); no data qword holds them; no `memset`/`memcpy` from a lea base in `022A0000`–`022C27A0` spans the block; and a register-tracked search for `lea R, [rip + base]` followed by `[R + disp]` landing in the block or the table — 0 (control: it finds `002479B0`'s `[rbp + r9*8 + 8]` into `0208ED68`). The publication slot `02EBF178` has the same result: its two RIP references are the machine's writes, and the register-tracked search finds no reader. **So the `.nmb` loader is linked, frame-driven and dormant**; the 166 shipped `.nmb` files are sized for it but not assembled by it. **Limit:** a pointer into the block produced by arithmetic from an unrelated value, or a registry walk with a runtime index, would escape these instruments.

### The index the caller passes is not the raw id — and for kind 26 it was unknown until the size table fixed it

**A requester picks the namespace *and* an index expression together.** The clearest instance is the
three-way branch in `ActorResource_BeginManagerResourceSetLoad` at `0x0032FD19`–`0x0032FD44`, read
here from the bytes:

| manager | namespace | index expression | anchors |
|---|---:|---|---|
| `<= 0` | **5** | `id * 3` | `mov esi,5` `0x0032FD3F`, `lea ebp,[r15+r15*2]` `0x0032FD44` |
| `1..3` | **8** | `id * 4` | `mov esi,8` `0x0032FD30`, `lea ebp,[r15*4]` `0x0032FD35` |
| `== 4` | **1** | **`id + 0x6B`** | `lea esi,[rdi-3]` `0x0032FD27`, `lea ebp,[r15+0x6b]` `0x0032FD2A` |

**Two of the three scale; the third offsets.** So the index is an **affine** function of the id —
a multiplier, an addend, or both — chosen per namespace by the requesting code. A namespace whose
requester scales by *k* makes its array read as a `k * 8`-byte record: `.ard` at stride 2 is why
that table reads as a 16-byte `{ardPath, fpkPath}` record (`repos-1e`), and namespace 5 at stride 3
would read as a 24-byte one.

> **This is exactly why a stride must not be read out of an array.** The scale and the addend live
> in the *caller*, and the array cannot distinguish `id * 1` from `id + 0x6B` — both produce a flat,
> un-interleaved table.

**And that is the limit of what this sheet can say about kind 26.** What is measured is the
**array**: 321 entries, dense from index 0, one distinct area stem per entry, no other extension
interleaved. ~~What is **not** established is the index expression a requester would use, because
**no request for kind 26 resolves** (above). A flat array is *consistent with* `id + 0` and equally
consistent with `id + c` for some constant — the namespace-1 branch shows an addend is a real
option in this engine, not a hypothetical one. **So every area index this sheet quotes is a position
in the array, not a proven argument to `ResourcePath_Get`.**~~
*Corrected 2026-09-30 (SWE2-CONTRACT, DD batch 9): the index expression is `id + 0`.* The one kind-26 requester,
`00324510`, passes its loop index `i` straight through (`mov edx, eax`, `00324627`). The `.fst` sizes kind 26 at
exactly the array positions of the shipped files (FABLE, above). And `ResourcePath_Get` is never the route for
kind 26 (the eleven sites above), so the area indices this sheet quotes are the arguments a kind-26 request passes.

### The table of tables — `g_pathTables` at `0x0215F000`

`ResourcePath_Init` (**`0x002DF9A0`**, 2,831 bytes) fills the slots. `.nmb` is **slot `+0xD0`,
kind 26**:

```
0x002DFADD  lea rax, [rip + 0x1b6e14c]     -> 0x01E4DC30   the `in` array
0x002DFAE4  mov qword ptr [rip+0x1e7f5e5], rax             -> g_pathTables[26]
   ... switch on the region argument ...
0x002DFE51  lea rcx, [rip + 0x1bce278]     -> 0x01EAE0D0   the `ch` array
0x002DFE58  mov qword ptr [rip+0x1e7f271], rcx             -> g_pathTables[26], again
```

**The `in` array is installed unconditionally in the prologue; one arm of the region switch
overwrites the slot with the `ch` array.** So the default build reaches `in\...` paths and exactly
one region reaches `ch\...` — which is what the archive shows from the other side, and it means
**the two trees are not a localisation split at all.** They are the two region variants of one
resource kind, and no `.nmb` text is localised: the two copies are byte-identical.

> This answers one of the two questions the README raised — *"why does a per-area data file ship
> under exactly two locale trees, neither of them `us` nor `jp`?"* **Because the path table for
> kind 26 has exactly two region variants, and `in` is the default.** The trees are named for
> territories, not languages, and the file's own bytes never vary.

**Both arrays are 321 entries of pure `.nmb` paths** — measured by walking each until a qword that
is not a pointer to a printable C string.

### Every resource kind in the table

Recovered from `ResourcePath_Init`'s own instruction stream, because the slots are written at run
time and the `.data` image holds zeros.

> **Array length is not derivable from the data, and an earlier version of this table said it was.**
> These arrays have **no terminator**: the length is known only to the callers. Two automated passes
> disagreed and **both were wrong** — stopping at the first non-string under-counts, because NULL
> entries are legal mid-array; tolerating NULLs over-counts, because the walk runs straight into the
> next array. The `entries` column is therefore **withdrawn** for every kind except 26, where an
> independent bound exists. See §6 and §8.

**What the first entries show instead, and it is more useful than a length:** several of these are
**interleaved record arrays, not flat lists.** Kind 5 is `{ebp, mot, fpk}` per map; the `.cm`/`.ca`
kinds interleave a header with its takes. A count would have hidden that.

| kind | slot | variants | first three entries |
|---:|---|---:|---|
| 0 | `+0x000` | 1 | `system.cnf`, `SLPM_667.50`, `ioprp300.img` |
| 1 | `+0x008` | 10 | `NULL`, `NULL`, `NULL` |
| 2 | `+0x010` | 10 | `WepJob_Matrix.bin`, `key_signal.bin`, `battle_message.bin` |
| 4 | `+0x020` | 1 | `ous0100.mpk`, `ous0101.mpk`, `NULL` |
| 5 | `+0x028` | 10 | `tst_a01.ebp`, `tst_a01.mot`, `tst_a01.fpk` — **a 3-wide interleave per map** |
| 6 | `+0x030` | 1 | `ousi00.bin`, `dummy.bin`, `dummy.bin` |
| 7 | `+0x038` | 1 | `NULL`, `NULL`, `NULL` |
| 8 | `+0x040` | 10 | `NULL`, `NULL`, `NULL` |
| 9 | `+0x048` | 9 | `NULL`, `test_map_ref.bin`, `test_area_ref.bin` |
| 10 | `+0x050` | 1 | `c_all.efx`, `m_all.efx`, `FileSizeTable_%s.fst` |
| 11 | `+0x058` | 1 | `m0000.efx`, `m0001.efx`, `m0002.efx` |
| 12 | `+0x060` | 7 | `e0000.efx`, `e0001.efx`, `e0002.efx` |
| 13 | `+0x068` | 1 | `g0001.cm`, `g0001_00.ca`, `g0002.cm` |
| 14 | `+0x070` | 1 | `c1004.cm`, `c1004_00.ca`, `c1004_10.ca` |
| 15 | `+0x078` | 1 | `hc1004_01.cm`, `hc1010_01.cm`, `hc1004_02.cm` |
| 16 | `+0x080` | 1 | `w2002.cm`, `w2202.cm`, `w2203.cm` |
| 19 | `+0x098` | 1 | `n1059.cm`, `n1059_00.ca`, `n1059_10.ca` |
| 20 | `+0x0A0` | 1 | `hn1018_11.cm`, `hn1018_12.cm`, `hn1032_01.cm` |
| 21 | `+0x0A8` | 2 | `NULL`, `NULL`, `NULL` — **see the note below** |
| 22 | `+0x0B0` | 1 | `b0001.cm`, `b0001_00.ca`, `b0003.cm` |
| 23 | `+0x0B8` | 1 | `s0002.cm`, `s0002_00.ca`, `s0002_10.ca` |
| 24 | `+0x0C0` | 1 | `hs0003_01.cm`, `hs0011_01.cm`, `hs0015_01.cm` |
| 25 | `+0x0C8` | 1 | `t0004.cm`, `t0005.cm`, `t0006.cm` |
| **26** | **`+0x0D0`** | **2** | **`tst_a.nmb`, `tst_b.nmb`, `tst_c.nmb` — 321 entries, see below** |
| 27 | `+0x0D8` | 1 | `wave0000.wd`, `wave0001.wd`, `wave0002.wd` |
| 28 | `+0x0E0` | 1 | `OPN.md`, `OPN.mh`, `NAL.md` — **`{md, mh}` pairs** |
| 30 | `+0x0F0` | 1 | `m1002_10_0272.ca`, `m1015_10_0278.ca`, `m1015_10_0268.ca` |
| 31 | `+0x0F8` | 1 | `music000.bgm`, `music001.bgm`, `music002.bgm` |
| 32 | `+0x100` | 1 | `se000.seb`, `se007.seb`, `se001.seb` |
| 33 | `+0x108` | 1 | `shout00.win.sab`, `shout01.win.sab`, `shout02.win.sab` |
| 34 | `+0x110` | 1 | `m1002.cm`, `m1002_00.ca`, `m1002_10.ca` |
| 35 | `+0x118` | 1 | `ff12menuoverlay_00_debug.bin`, `..._01_debug.bin`, `..._00_debug.bin` |
| 37 | `+0x128` | 2 | `NULL`, `NULL`, `NULL` |
| 38 | `+0x130` | 1 | `m0000.efx`, `m0001.efx`, `m0002.efx` |
| 39 | `+0x138` | 1 | `shout00.win.sab`, `shout01.win.sab`, `shout02.win.sab` |

Kinds **3, 17, 18, 29, 36 and 40** are assigned a pointer to a location holding no resolvable
string; **they are unprofiled, not proven empty.** Kinds **1, 7 and 8** begin with NULLs and may be
populated later in the array — the head is not evidence about the tail.

**`variants` is how many different arrays `ResourcePath_Init` can install in that slot.** Kinds 1,
2, 5 and 8 have ten, kind 9 has nine, kind 12 seven, and kinds 21, 26 and 37 two. The ten-variant
kinds all begin with identical entries, so **the variants differ later in the array, not at the
head** — which is why a head-only reading cannot tell them apart.

> ### The variant column is recovered by an instrument known to undercount — here is what is
> ### independently confirmed and what is not
>
> Every figure above comes from pairing `lea reg,[rip+d]` with the `mov [rip+e], reg` that consumes
> it, inside `ResourcePath_Init`. **That method demonstrably misses stores**: `repos-1e`'s
> implementation of it recovered 83 array bases where `repos-3f` got 94, and 8 variants for kind 8
> where the true value is 10. Mine is the same *kind* of instrument, so it carries the same risk.
>
> **A second method settles the rows it can reach.** Each region variant emits its own full path
> string for the same file stem, so **distinct strings ÷ distinct stems is the variant count**, and
> it reads no initialiser at all. Measured over the image:
>
> | ext | strings | stems | ratio | the kind it fixes |
> |---|---:|---:|---:|---|
> | `.nmb` | 642 | 321 | **2.000** | **kind 26 — confirms 2** |
> | `.ebp` · `.mot` | 10,380 | 1,038 | **10.000** | **kind 5 — confirms 10** |
> | `.mpk` | 550 | 550 | **1.000** | kind 4 — confirms 1 |
> | `.wd` | 260 | 260 | **1.000** | kind 27 — confirms 1 |
> | `.bgm` | 256 | 256 | **1.000** | kind 31 — confirms 1 |
> | `.seb` | 608 | 608 | **1.000** | kind 32 — confirms 1 |
> | `.md` · `.mh` | 45 | 45 | **1.000** | kind 28 — confirms 1 |
> | `.cnf` | 1 | 1 | **1.000** | kind 0 — confirms 1 |
>
> **Every row this method can reach agrees with the extraction.** It reaches a row only when the
> extension belongs to exactly one kind; where an extension is spread across several — `.bin`
> (7.120), `.efx` (2.707), `.tm2` (5.306), `.irx` (1.750) — the ratio mixes kinds and **cannot
> adjudicate**, so those variant counts still rest on the extraction alone and should be treated as
> lower bounds.
>
> **Kind 21 is confirmed at 2 by something stronger than the ratio.** `.ard` turns out to be
> single-kind, so `430 / 215 = 2.000` is unmixed — but reachability settles it outright. All **430**
> `.ard` pointers in the image fall into exactly **two** regions of **215** each, at `0x01E0D060`
> and `0x01EDC340`, and **all 430 strings are reachable from them, none unreached**. Each region
> begins exactly 24 qwords past its array base (`0x01E0CFA0`, `0x01EDC280`) — the sparse head
> described in the `PROPOSED-repos-4b-9` note above. A third array would have to re-point at strings
> already fully accounted for. *Measured here; `repos-1e` reached the same result from the
> initialiser's write count.*
>
> **Kind 8 is now confirmed at 10 as well, by a bounded re-walk.** All the arrays above were re-derived through `repos-1e`'s `walk_array`, which requires an explicit slot count and refuses an unbounded call: namespace 8 yields **ten** arrays of 329 `{ebp, mot, snd, vpc}` records each. The same re-walk reproduces kind 26's **321** from two arrays. **A caveat on how that is argued:** an earlier version of this passage claimed the differing extents between siblings were themselves a control — they are not, and the reasoning is withdrawn (see the PKFL sheet's §8, same defect). **Every one of these arrays is dense to its boundary — headroom zero — so widening the bound only starts counting the next array and there is no plateau to observe.** What anchors 321 is external: `.nmb` has **642 strings over 321 stems = 2.000**, `.nmb` is single-kind, and all 642 are reached from the two arrays with none unreached. That holds whatever the walk bound is.

> **That leaves kinds 1, 2, 9 and 12 unconfirmed**, and kind 8's true value is known to be 10
> — the direction of the error to expect if any of the others is wrong is *low*, since every
> instance found so far has undercounted.

**Kind 26's length is measured, and it is the only one that is.** The independent bound is a scan
of `.rdata`/`.data`/`_RDATA` for qwords pointing at `.nmb` path strings, which yields **contiguous
stride-8 runs of 321 (`in`) and 313 + 7 (`ch`)** — bounded by string identity rather than by
walking, so it cannot overrun into a neighbour.

**That method works for `.nmb` and provably cannot work for `.ard`.** The same scan for `.ard` and
`.fpk` finds **no contiguous run longer than three**, because those two extensions are *interleaved*
at 16-byte stride and so never form a stride-8 run of one extension. The instrument's failure is
itself the evidence for the interleave.

> ### `PROPOSED-repos-4b-9` — RESOLVED 2026-09-04, in `repos-1e`'s favour
>
> This sheet briefly recorded a disagreement: `repos-1e` reads `.ard` as **namespace 21, index
> `areaIndex*2`**, with `areaIndex*2 + 1` holding the `.fpk` path, at slot `0x0215F0A8` — the same
> slot this table lists — while both arrays recovered here for that slot begin with NULLs.
>
> **`repos-1e` is right, and the reason this pass could not see it is the interesting part.**
> Answering the challenge, they decoded every RIP-relative operand in all 38,161 functions using
> `functions.tsv` boundaries rather than `lea`/`mov` pairing, and confirmed `0x0215F0A8` is touched
> **exactly twice, both writes, both in `ResourcePath_Init`** — arrays `0x01EDC280` (`0x002DFA9E`)
> and `0x01E0CFA0` (`0x002DFE66`). Walking both in full: **first non-NULL index 24**, then
> **215 `.ard` at even indices and 215 `.fpk` at odd**, zero crossover either way, and all 430
> `.ard` path strings reachable — none unreachable.
>
> **The "three NULLs" seen here were the same fact at a coarser granularity** — 24 NULL qwords, i.e.
> twelve empty 16-byte area slots, before `ttl_a` at index 24. **The array is sparse and its head is
> empty**, which is exactly why a head-only reading and a stop-at-first-NULL walk both come back
> empty. The instrument was not broken; it was pointed at the empty part.
>
> **The narrow claim this sheet made survives intact and is now explained rather than merely true.**
> `repos-1e` also records a limit worth repeating: those arrays are **not** `{ard, fpk}` pairs end to
> end — they also carry `bin`, `tm2`, `mrp`, `as7`, `ico`, `efx`, `cm`, `sys` and `mg` paths at both
> parities. The proven statement is the narrow one: *within* these arrays every `.ard` sits at an
> even index and every `.fpk` at the odd index after it, 215 / 215.

**So the earlier claim that "`.ard` is not in this table" is withdrawn — `.ard` is namespace 21.**
What this sheet's own evidence supports is the narrower and now-explained statement: **no slot's
*head* resolves to `.ard` paths, and `.ard` forms no stride-8 pointer run** — the first because the
array is sparse, the second because `.ard` and `.fpk` interleave at 16-byte stride.

**The write path.** None. Nothing writes `.nmb`; it is authored offline.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `0x002DF980` | `ResourcePath_Get(kind, index)` — the whole 22-byte function: table fetch `0x002DF98D`, path fetch `0x002DF991`, no bounds check anywhere | ✅ full body |
| `0x002DF880` | `ResourcePath_Copy(kind, index, dst, maxLen)` — NULL return `0x002DF89E`, copy loop `0x002DF8B3`, length test `0x002DF8C4`, terminator `0x002DF8D1` | ✅ full body |
| `0x002DF9A0` | `ResourcePath_Init(region, flag)` — installs every slot; `.nmb` `in` at `0x002DFAE4`, `ch` at `0x002DFE58` | ◐ the slot-install region and the `fopen` tail |
| `0x002DF780` | third consumer of `g_pathTables`, indexed at `0x002DF7BF` and `0x002DF830` — ~~✗ entry only~~ *(corrected 2026-09-30, SWE2-CONTRACT, DD batch 9: read whole — the `.fst` `-1` refusal `0x002DF7B0`, then the path fetch; the route every kind-26 request takes)* | ✅ full body |
| `0x0215F000` | `g_pathTables` — the table of path tables, indexed by resource kind | — |
| `0x01E4DC30` | the `.nmb` path array, `in` tree, 321 × `char*` | — |
| `0x01EAE0D0` | the `.nmb` path array, `ch` tree, 321 × `char*` | — |
| `0x002ED6F0` / `0x002E98F0` | the id-letter decoders behind four `ResourcePath_Get` sites; kind set `{1, 13–16, 18–20, 22–25, 34}` *(SWE2-CONTRACT, 2026-09-30)* | ✅ full body |
| `0x0032F170` | the manager decoder: `≤0` → kind 5 `id*3`, `1..3` → kind 8 `id*4`, `4` → kind 1 `id+0x6B` *(SWE2-CONTRACT, 2026-09-30)* | ✅ full body |
| `0x0032E620` → `0x0032E870` → `0x0032E070` → `0x0046E030` | the request route to `0x002DF780`: kind at slot `+0x21`, index at `+0x24` *(SWE2-CONTRACT, 2026-09-30)* | ◐ the kind/index path |
| `0x00324510` | the dormant kind-26 assembler: `0x1A` at `0x00324637`, ids 0–300, pairs at `0x022C27B8` *(SWE2-CONTRACT, 2026-09-30)* | ✅ (FABLE, 2026-09-11) |
| `0x01ECBCF0` / `0x01EA4D00` | kind 37's two arrays, 2,964 slots each, 1,316 paths *(SWE2-CONTRACT, 2026-09-30)* | — |

## 5. Corpus survey

**Invariants — checked over all 166 areas and all 1,146 entries.**

| | |
|---|---|
| `+0x02` version | `0x0064`, **166 / 166** |
| offset table length | `count + 1`, **166 / 166** |
| `offset[0] == 4 + 4*(count+1)` | **166 / 166** — the first entry begins exactly where the table ends |
| `offset[count] == file size` | **166 / 166** — the terminator is the file length |
| offsets strictly ascending | **166 / 166** |
| entry length | 3 bytes, **1,146 / 1,146** |
| entry `+0x00` | `0x12`, **1,146 / 1,146** |
| entry `+0x02` | `0x00`, **1,146 / 1,146** |

**The whole corpus contains exactly two distinct entry values.** `12 BA 00` occurs 1,120 times and
`12 BB 00` 26 times. 1,146 entries across 166 areas, and **no third value anywhere.** A format with
9,350 bytes of payload carrying two distinct symbols is a strong finding in its own right: whatever
`.nmb` encodes, almost all of the information is in the **count and the ordering**, not the values.

**`0x12BB` appears in 10 areas of 166**, and where it appears it forms contiguous runs rather than
scattering:

| area | count | `BB` | pattern (`B` = `12 BA 00`, `b` = `12 BB 00`) |
|---|---:|---:|---|
| `bds_e` | 5 | 4 | `Bbbbb` |
| `bhm_c` | 11 | 5 | `BBBBBbbbbbB` |
| `bhm_d` | 1 | 1 | `b` |
| `dor_b` | 3 | 2 | `Bbb` |
| `mrm_e` | 2 | 1 | `Bb` |
| `rui_c` | 2 | 1 | `Bb` |
| `tri_d` | 6 | 1 | `BbBBBB` |
| `tri_f` | 15 | 2 | `BBBBBBBBBBbbBBB` |
| `tri_q` | 14 | 4 | `BBBBBBBbbbbBBB` |
| `tri_t` | 10 | 5 | `BBBBBbbbbb` |

**Four areas have `count == 0`** — a valid file of exactly 8 bytes holding a header and a single
terminator offset.

**Entry count correlates strongly with `.ard` size**, Pearson r = **0.868** over the 166 areas. It is
a correlation and nothing more; no field in the `.ard` header equals the `.nmb` count in all 166
areas. The best single candidate, `.ard` `+0x34`, matches in **103 of 166** — which is *not* a
binding, and is recorded here so the next person does not re-derive it and mistake it for one.

### The entry count is the record count of the `.ard`'s `st2e` table in **directory slot 2** — 166 of 166

*Added 2026-09-04 by `repos-4b`, whose board row was "establish what `.nmb` indexes and whether it
keys to the `.ard` tables". Measured on the extracted files, so it does not depend on the pointer
work above.*

> **Two numberings exist and conflating them is easy.** The `.ard` header carries an **eight-slot
> indexed directory** at `+0x10`–`+0x2C` (`repos-d6`), and only four of its slots hold an `st2e`
> table. So *"the second `st2e` block in the file"* and *"directory slot 2"* are different
> coordinates that happen to name the same table. **This section uses the slot number**, and the
> record size disambiguates it in one step.

`st2e`'s `+0x04` is the record count
([the `st2e` sheet](../vbf-archive-and-st2e-tables.md#2-the-st2e-table-header), confirmed there by
file-length arithmetic). **The `.nmb` entry count equals the record count of the table in directory
slot 2 in all 166 areas** — so `.nmb` is a **parallel array over that table: one three-byte entry
per record.**

Mapping each `st2e` occurrence onto the directory slot whose offset equals it, over all 166 areas:

| file-order ordinal | directory slot | `recordSize` | areas | `.nmb` count matches |
|---:|---:|---:|---:|---:|
| 0 | **0** | 84 | 166 / 166 | 103 |
| **1** | **2** | **88** | **166 / 166** | **166** |
| 2 | **5** | 56 | 166 / 166 | 159 |
| 3 | **6** | 56 | 166 / 166 | 44 |

**The ordinal→slot map never permutes** — slot 0 is always first in the file, slot 2 always second,
in 166 of 166. That is why the two coordinates can be used interchangeably here; it is a measured
property of the corpus, not a definition. Present slots are `{0, 1, 2, 5, 6, 7}` in every area
(3 and 4 never occur), slot 0's offset is always `0x30` — simultaneously the first section offset
and the header length — and the per-slot `recordSize` is constant across the whole corpus,
independently reproducing `repos-d6`'s 84 / 88 / 56 / 56.

That also explains the count distribution: the four areas with zero entries (`asp_a`, `dor_f`,
`mrm_a`, `slm_a`) are the four whose slot-2 table is empty.

**Falsified against "it matches whichever table you look at".** The four tables often carry equal
counts, so agreement with slot 2 alone would prove nothing. The distinguishing subsets:

| test | areas | `.nmb` follows slot 2 |
|---|---:|---:|
| slot 0 differs from slot 2 | 63 | **63** |
| slot 5 differs from slot 2 | 7 | **7** |
| **slot 6 differs from slot 2** | **122** | **122** |
| slot 2's count unique among all four | 7 | **7** |

**In 122 of 166 areas slot 6 disagrees, and the `.nmb` never follows it.** The binding is to slot 2
specifically, and it survives the test designed to break it.

> **This is a correspondence, not a meaning.** What the slot-2 table *holds* is the `.ard` sheet's
> question and is not answered here — so this says what the count is parallel to, and stops. Whether
> the two symbols annotate those records is the obvious next reading and is **not** established.
>
> **It does corroborate from the corpus side**, though, and the two lines are independent:
> [the `.ard` loader sheet](how-the-ard-loader-binds-area-battle-data.md) reaches slot 2 as battle
> category 2, bound into registry slot `0x02EBF120` — the widest reader set of the five. A
> row-for-row annotation from the file side and a consumer set from the instruction side are
> **two leads that corroborate rather than merely coexist**; neither decodes a record.

### The table is nearly twice the shipped corpus

| population | size | relationship |
|---|---:|---|
| `.nmb` path table, per region | **321** | the master area enumeration |
| `.ard` path records, per tree | **215** | **a strict subsequence of the `.nmb` order** |
| areas that ship both files | **166** | all 166 appear in both tables |

**155 of the 321 `.nmb` table entries name a file that is not in the archive**, and **49 of the 215
`.ard` entries** do the same. Zero shipped areas are missing from either table. The table-only stems
are development areas — `tst_a` … `tst_p`, `ttl_a` … `ttl_c`, `e00_a` … — which is what the head of
the `.nmb` array is made of.

> **This qualifies the `.fpk` argument in [the README](README.md).** That section uses `.nmb` as the
> control — *"642 strings, 332 files, so the instrument works"* — against `.fpk`'s 7,520 strings and
> zero files. The control is weaker than it looks: **only 52 % of `.nmb` table entries ship a
> file.** A path in the table is plainly not evidence that the file ships. `.fpk` at **0 of 7,520**
> is still categorically different from `.nmb` at **166 of 321**, so the conclusion stands — but it
> stands on the zero, not on the contrast. That is a correction owed to a document this sheet does
> not own; it is reported, not edited.

## 6. Falsification pass — 2026-09-04

| attack | result |
|---|---|
| Are the offsets relative to the file, the header, or the entry array? | **The file.** `offset[count]` equals the file size in 166 of 166, and `offset[0]` equals `4 + 4*(count+1)` — both only true on a file-relative origin. Two independent checks, same answer. |
| Is the 3-byte entry a format rule or a corpus accident? | **A corpus accident, and the sheet says so.** The offset table can express any length; nothing in `ResourcePath_Get` or `ResourcePath_Copy` touches entry contents at all. Recorded as an observation over 1,146 entries, not as a constraint. |
| Are the two locale copies really identical, or was that inherited? | **Re-hashed here.** SHA-256 of both copies of all 166 areas: identical in 166 of 166, for `.ard` as well as `.nmb`. Not taken from the README. |
| Does `.nmb` share an index with `.ard`? | **No.** They live in different structures — `.nmb` in `g_pathTables[26]` at 321 entries per region, `.ard` in a separate 16-byte record array at 215 per tree. Same *ordering*, different *length*, so the same area has different indices in each. The shared ordering says both were emitted from one authored area list; it does not make them co-indexed. |
| Was the first `.ard` comparison sound? | **No, and it was redone.** The first pass assumed a contiguous 215-record array based at `0x01E0D060` and read mostly nulls — the `.ard` pointers are not contiguous. Every pointer position in the final comparison is found by scanning `.rdata`/`.data`/`_RDATA` for qwords that resolve to a path string, never by positing a base. |
| **Does the kind-26 array have a sparse head, so that every area index here is shifted?** | **No — tested, not assumed.** `repos-1e` found the namespace-21 (`.ard`/`.fpk`) arrays carry **24 NULL qwords at the head**, which is why head-only inspection of those finds nothing. If kind 26 did the same, the base stored in `g_pathTables[26]` would sit before the first `.nmb` pointer and **every index in this sheet would be wrong by that offset.** Recovering the base from the initialiser's own `lea`/`mov` pair rather than from where pointers were found: `0x002DFAE4` → `0x01E4DC30` and `0x002DFE58` → `0x01EAE0D0`. Both have **0 NULL qwords at the head**, index 0 is already a `.nmb` (`tst_a`), the run is **321 consecutive `.nmb` pointers with no other extension inside**, and the **first NULL is at index 321**. The sparse-head hazard is real for namespace 21 and absent here. *(`repos-4b`, 2026-09-04, prompted by `repos-1e`.)* |
| **Was the base recovered by judgement, or by luck?** | **By luck, and the sheet says so because it is the reason the method is mandatory.** I read the base out of the initialiser because it was the cheapest way to confirm *which slot was 26* — not because I had considered that the first pointer in a dense run might not be the base. Doing the obvious thing instead, and taking `0x01E4DC30` as the base because that is where the run starts, would have been **right here and wrong on namespace 21**, and nothing in the data distinguishes the two cases: dense and sparse arrays look identical once you are reading from the first non-NULL entry. **A correct answer reached for the wrong reason is a latent defect everywhere the reason stops holding** — here, every sparse array. Hence the rule, which is not about this format: **recover a path-table base from the initialiser that writes it, never from where its first pointer is found.** |
| Is there a third `.nmb` array the two-array claim misses? | **No — and the first version of this row used too weak a test.** It originally excluded membership only in the two kind-26 arrays, which is not enough: a stray could belong to some *other* kind's array. Re-measured twice. The first re-measurement recovered all 94 array bases across all 41 kinds from `ResourcePath_Init`'s own stores but **walked each array only to its first NULL**, so every sparse array contributed no members and the membership set was **20,107 slots — an undercount of 3.5×**. Re-walked with NULLs treated as holes and each array bounded by the next base in address order: **72,046 member slots**. **The conclusion is unchanged under the corrected test, and the growth is itself evidence**: the extra **51,939** member slots were 51,939 fresh opportunities for one of the strays to turn out to be a member, and **none did**. A membership set that triples without moving the answer says more about the answer than the original run could. Of **657** 8-aligned qwords in `.rdata`/`.data`/`_RDATA` that resolve to a `.nmb` path, **642 are inside a recovered array and every one of those is kind 26** — the two 321-entry arrays and nothing else. The remaining **15 are outside all 41 kinds' arrays**, all sit in `.rdata` (*not* `.data`, as this row first said), and **15 of 15 have both neighbours resolving to nothing**. **Three of the fifteen point into the *interior* of a path string**, resolving to the bare tail `".nmb"` — a path table holds pointers to string starts, so those three cannot be members under any reading. **What the 15 are is not established**; the claim is only that they belong to no array the initialiser writes. *(Re-measured after `repos-1e` retracted the analogous `.ard`-side claim, which had tested membership against an address span instead of against the structures.)* |
| Could the `0x12BA`/`0x12BB` values be found in the binary as constants? | **The scan is too noisy to use and is not relied on.** `0x12BA` occurs 48 times as a 2-byte LE value in `.text` and 40 times as a 4-byte; `0x12BB`, 8 and 2. Against that floor a real reference is indistinguishable from an arithmetic coincidence — the same measurement that killed the EBP marker scan. **No claim here rests on it.** |
| Did the community reading influence any of this? | **There is no community reading of `.nmb` to inherit**, and the `.ard` enemy-attribute reading is not used anywhere above. |

**What was tried and failed to break it.** The obvious alternative structure is that `.nmb` is a
name or string list — the extension suggests it and the README's standing lead says so. That
predicts printable payload bytes. **Measured: 13.6 % of all bytes are printable, and the printable
ones are concentrated in the offset table's low bytes, not the entries.** The entries are `0x12`,
`0xBA`/`0xBB`, `0x00` — no encoding puts a NUL in the middle of a name list this uniformly. The
lead is dead, and the file is an index, not a name list.

## 6b. Independent audit pass — 2026-09-05, `repos-1e`

**Method.** All 332 `.nmb` archive entries decompressed in full from `FFXII_TZA.vbf` and re-parsed
with a fresh reader; both cited path functions re-decoded with capstone. Program state: GN160
(`gzf fa0db293…`).

**Every corpus claim reproduces exactly.**

| claim | sheet | re-parse |
|---|---|---|
| archive entries / logical areas | 332 / 166 | **332 entries, 166 stems, `ch` 166 + `in` 166** |
| the two locale copies are byte-identical | 166 / 166 | **166 / 166, re-hashed** |
| `+0x02` version | `0x0064` in 166 / 166 | **100 in 166 / 166, no other value** |
| offset table has `count + 1` entries, last = file size | — | **166 / 166** |
| offsets strictly ascending | — | **166 / 166** |
| `size = 8 + 7*count` | "exactly the 19 observed sizes" | **holds in 166 / 166; exactly 19 distinct sizes, 8 … 162** |
| total entries | 1,146 | **1,146** |
| every entry exactly 3 bytes | 1,146 | **1,146 / 1,146, no other length** |
| entry `+0x00` tag | `0x12` in 1,146 / 1,146 | **`0x12` × 1,146** |
| entry `+0x01` code | `0xBA` × 1,120, `0xBB` × 26 | **exact** |
| entry `+0x02` `_zero` | `0x00` in 1,146 / 1,146 | **exact** |

**Both path functions reproduce instruction for instruction.** `ResourcePath_Get` `0x002DF980` is
the six instructions printed, `movsxd` on **both** arguments, and `0x002DF98A + 0x1e7f676` resolves
to `0x0215F000` as claimed. In `ResourcePath_Copy` all three cited addresses are exact and do what
the sheet says: `0x002DF89E` is the NULL branch (`0x002DF8A0 or eax,0xffffffff` → −1),
`0x002DF8C4 cmp rcx,r9` is the `maxLen` test, `0x002DF8D1 mov byte ptr [rax+r11],0` is the
terminator.

**The `maxLen + 1` warning is confirmed and is a real safety property.** The loop exits when
`copied >= maxLen`, and the terminator is then written at `dst[copied]` — so with `copied == maxLen`
the write lands one byte past a `maxLen`-sized buffer. **A caller sizing `dst` to exactly `maxLen`
overflows by one**, and nothing in the function prevents it.

**Both "no bound of any kind" rows hold.** Neither argument is compared against anything in the
22 bytes — no `cmp`, no mask, no branch — and both are **sign**-extended, so a negative `kind` or
`index` indexes backwards from the table base. That is the sheet's sharpest safety claim and it
survives.

### The auditor's parse was wrong first, and that is the finding worth keeping

My first re-parse read the offset table as **`u16`** and produced *negative* entry lengths and
"last offset == file size" in **4 of 166** — a result that looked exactly like a broken format
claim. **The sheet says `u32` in plain text immediately under the fence**, and I had not read it.

> **This is the third time in this session's audits that a disagreement was the auditor's
> instrument**, after an empty list counting as vacuously sorted and an unscoped `0x40` count. The
> pattern is worth naming: **a re-parse that disagrees is evidence about the parser until the layout
> has been read, not skimmed.** A format sheet's prose carries constraints the fence grammar cannot
> — here `count + 1` and the `u32` width — and skipping it produces confident nonsense.

**What was attacked and held.** (a) That the 3-byte entry might be a fixed record the offset table
merely echoes — the table *can* express any length and every one of 1,146 is 3, so the sheet's
refusal to call it a fixed record is the right call and the data does not force it. (b) That
`size = 8 + 7*count` might be a fit to a few sizes — it holds for all 166 with 19 distinct sizes.
(c) That the byte-identical locale copies might have been inherited from the `.ard` census — they
were re-hashed here from decompressed bytes.

**Not audited:** ~~the five unresolved `ResourcePath_Get` call sites in §3, and~~ what a `.nmb` entry's
`tag`/`code` pair *means* — §7 already declines ~~both~~ it. *(Corrected 2026-09-30, SWE2-CONTRACT, DD batch 9:
the five sites are resolved in §3, "All eleven sites resolve, and the kind-26 route".)*

## 7. What this document does not claim

- **What an entry means is not established.** The structure is complete and the values are censused,
  but nothing read here consumes an entry. `ResourcePath_Get` returns a path; the code that opens the
  file and walks it was not found. **A two-symbol alphabet over 1,146 entries is a strong constraint
  on the answer and is not the answer.** → `PROPOSED-repos-4b-6`
- **`0x12BA` vs `0x12BB` is undecided.** 1,120 against 26, in contiguous runs, in 10 areas. Whether
  it is a type, a flag or a variant is not claimed.
- ~~**The `.nmb` file reader is not identified.** This sheet establishes how the *path* is reached, not
  who opens it. `ResourcePath_Init` itself calls `fopen`/`fread`/`fclose` at its tail, but on a
  `sprintf`'d name from a different table — that is not the `.nmb` path.
  → `PROPOSED-repos-4b-7`~~
  *Corrected 2026-09-30 (SWE2-CONTRACT, DD batch 9): identified, and dormant.* The reader is the assembler
  `00324510`. It requests every sized area through `0032E620(0x1A, i, …)`, and the path is resolved by `002DF780`
  (§3). It never starts, because nothing moves its state word out of 0 (FZ-8, §3). No code that walks an entry
  exists in what was read, which is why the entry's meaning (first bullet) stays open.
- ~~**Which region selects the `ch` tree is not named.** The install happens in one arm of a switch on
  `ResourcePath_Init`'s first argument; the argument's values were not mapped to territories.~~
  *Corrected 2026-09-30 (SWE2-CONTRACT, DD batch 9): regions 7, 8 and 11, which are KR, CH and CN.* The switch is
  on `region - 1` over eleven arms (`002DFBAF` / `002DFBB3`). Only the arms for 7, 8 and 11 reach the `ch` install
  at `002DFE58`. The default arm, which covers 0 and every value above 11, does not (checker N8). The same argument
  indexes the language-name table `01E88B00` that names the `.fst` (`002E03F5`), and
  `r8` is not rewritten in between. That table reads `JP US FR DE IT ES UK KR CH ASIA IN CN`, so the `ch` tree
  serves the Korean and Chinese builds, and every other language reads `in`.
- **The three 2000-entry arrays in the §3 table are lower bounds**, cut off by the profiler's walk
  limit rather than by their own terminators.
- **Callers of `ResourcePath_Get` were not audited**, so the unbounded `kind`/`index` is a property
  of that function and not a reachability claim. *(2026-09-30, SWE2-CONTRACT, DD batch 9: the eleven sites'
  **kinds** are now resolved (§3); their **index** ranges are still not audited against the arrays' extents.)*
- **Nothing here is claimed about what the `.ard`'s four `st2e` tables hold.** The `.ard` is another
  session's unit and the community enemy-attribute reading is left exactly where the README put it.

## 8. Corrections

**2026-09-04 — the per-kind `entries` column was wrong, and is withdrawn.** `repos-4b`.

*What was believed.* §5 carried a table giving an entry count for each of 29 resource kinds — "kind
2: 40 `.bin`", "kind 5: 3 `.ebp`/`.mot`", and so on — with three rows flagged as `≥2000` walk-limit
lower bounds.

*What is now believed.* **Those counts were not measurements.** The arrays have no terminator, and
their length lives only in the callers. The figure came from walking each array until a qword that
did not resolve to a printable string, which **stops at the first NULL** — and NULL entries are
legal mid-array. Every count was therefore the distance to the first hole, not the length.

*What proved it.* `repos-1e` reported that namespace 21 interleaves `.ard` with `.fpk`, and that
`.fpk` is usually NULL. Re-running the profile with NULLs tolerated produced *different and equally
wrong* numbers — the tolerant walk runs past the array end into its neighbour, so kind 26 grew from
321 to 359 by absorbing entries from the array next to it, and kind 16 reported 321 `.nmb` paths it
does not own. **Two passes, two answers, both wrong, and the disagreement is what exposed it.** The
head-only reading that replaced them also revealed what the counts had hidden: kind 5 is a 3-wide
`{ebp, mot, fpk}` interleave, not a 3-entry list.

*Why the earlier reading was reachable.* The strict walk gives a plausible number for a *flat*
array with no holes, and kind 26 — the one array checked against an independent bound — is exactly
that. **The method was validated on the one case where it happened to work, then applied to 28
cases where it did not.** The tell was available and ignored: three rows hit the walk cap and were
labelled "lower bounds" rather than treated as evidence the walk had no idea where the array ended.

*Consequence.* The `entries` column is gone; §5 now gives the slot, the variant count and the first
three entries, and states a length only for kind 26, where a scan bounded by string identity gives
321. The claim **"`.ard` is not in this table"** is also withdrawn — it rested on the same broken
walk. The narrower surviving claim is that no slot's *head* holds `.ard` paths and `.ard` forms no
stride-8 pointer run.

## Evidence (SWE2-CONTRACT, 2026-09-30)

| claim | evidence | tier |
|---|---|---|
| The header, offset table and 3-byte entries, over 166 areas | §5 invariants; §6b re-parse of all 332 archive entries | 9 (shipped archive) |
| `ResourcePath_Get` / `_Copy` bodies and their missing bounds | §3, §6b, read whole | 1 (static) |
| The `in` / `ch` arrays at slot `+0xD0`, 321 entries each | `ResourcePath_Init`'s own stores `0x002DFAE4` / `0x002DFE58`; §6 sparse-head row | 1 (static) |
| The `.nmb` count follows the `.ard`'s directory slot 2 | §5, 166 of 166 with the distinguishing subsets | 9 (shipped archive) |
| All eleven `ResourcePath_Get` sites resolve, none to 26 | `002ED6F0` / `002E98F0` / `0032F170` read whole; the jump table enumerated; checker N1–N5 | 1 (static) |
| A kind-26 request resolves through `0032E620` → … → `002DF780` | checker N6 | 1 (static) |
| The one kind-26 issuer is `00324510`, dormant, bounded at 301 ids | FZ-8 (FABLE, §3); checker N6 (the census of `0032E620`'s 51 sites is of immediates only) | 1 (static) |
| The kind-37 arrays end at index 2,963 (2,964 slots, 1,316 paths) | the next of the 94 installed bases; all twelve `.fst` files; checker N7 | 1 (static) + 9 (shipped `.fst`) |
| Kind 26 is indexed by array position | the `.fst` affine search (FABLE, §3); `00324627` passes `i` unchanged | 1 (static) + 9 (shipped `.fst`) |
| `ch` serves regions 7, 8, 11 = KR, CH, CN | the region switch and the language-name table; checker N8 | 1 (static) + 2 (the language strings) |

## 9. Related

- [`St2e-Carriers/README.md`](README.md) — the `.ard`, its path table, and the `.fpk` question this
  sheet qualifies in §5.
- [`_index/ASSET-FORMATS.md`](../../../_index/ASSET-FORMATS.md) — the 48-extension archive census
  this unit is scored against.
- [`25-EBP-Script-Container/Sections/section-008.md`](../../../25-EBP-Script-Container/Sections/section-008.md)
  — the same "offset table plus a terminator" idiom, and the same authored-index-recomputed-at-load
  hazard worth checking for here once a reader is found.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver / encoder fan-out is MECHANICAL.*

The two loading loops this page cites, `0022A770` and `0022BC20`, are the field frame and mode 5:

- **Input — SERVICE.** Both loops rebuild the input frame snapshot: `InputGameplay_RebuildFrameSnapshotFromChanne…`,
  `InputGameplay_RebuildRemappedTransitionMaskS…`, `InputControl_SetOneShotFrameCallback` and helpers. `0022A770` also
  reads `InputGameplay_GetRemappedHistoryMask0C` / `…04`. The request `0032E620` is also issued by the 177-byte
  item-graphics loader.
- **Presentation — SERVICE.** Both loops run the graphics-sync pair, `EffectSystem_ProcessQueuedGraphicsEffectsFor…` and
  presentation bodies. `0022A770` runs `MainLoop_Draw` and `RenderSystem_RunCharacterUpdatePipeline`. The request is
  shared with two Presentation bodies.
- **Movement — SERVICE.** `0022BC20` calls a 219-byte movement helper, and `PartyFocus_CommitPendingPackedActorHandle`
  (`00358BC0`) calls the 10-byte movement-body-pool consumer.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**ActorEntity — CLIENT.** `FUN_003306e0`, owned by that layer, calls `00332250` on this page. That caller is a 3,882-byte routine that takes a **`0x1ED8`-byte stack allocation** through the stack probe before it starts; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Audio — SERVICE.** `0022A770` on this page calls `FUN_0036f460`, owned by that layer. What it reaches is a float normalisation against 1.0 that keeps the previous value in the global at `02AD9B50` and steps by -1.0 until it is in range; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**CoreRuntimeScheduling — CLIENT (12 edges through 6 of this page's functions).** The CoreRuntimeScheduling layer reaches this page at `0022A770`, `00324510`, `0022BC20`, `002DF9A0` and 2 more. `FUN_001ec760` is the worked example, read in full - it is a 2,232-byte body behind the same `[01F82E38]` gate and the same `001EC560` predicate as the cutscene-override table, and it does nothing at all when either refuses; **3 of the 8 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Party — SERVICE.** `0022BC20` on this page calls `PartyFocus_CommitPendingPackedActorHandle_Thunk`, owned by that layer. What it reaches is a five-byte thunk - `jmp 00358BC0`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**PlatformOnlineAchievements — SERVICE.** `0022A770` on this page calls `FUN_00316930`, owned by that layer. What it reaches is a 287-byte walk of the same `[022C2550]` table against the data at `01EED130`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).
- **Save_Load_Settings — CLIENT (1 edge).** 1 inbound (Save_Load_Settings bodies `002EF300` call page-cited `0032E620`). Substantive edges include `0032E620` is called by `002EF300`.
- **Script_VM_Native_Bridge — CLIENT (1 edge).** 1 inbound (Script_VM_Native_Bridge bodies `0050DFE0` call page-cited `0032E620`). Substantive edges include `0032E620` is called by `0050DFE0`.
- **UI — SERVICE (1 edge).** 1 outbound (page-cited `0022A770` call UI bodies `00254E50`). Substantive edges include `0022A770` calls `00254E50`.
