---
system: The actor storage record, recovered from its initialiser
category: 04-Actor-Entity
status: AUDITED
owner_layer: PrimaryOwner:ActorEntity
evidence_tier: 1
level: L1
readiness: SIGNATURE RESOLVED
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: ActorStorage_InitializeRecord disassembled whole; every store to the record's base
    register collected with its operand width; the base proved stable before any offset was
    believed; layout written to _types/ and validated
last_reviewed: 2026-09-08
audit:
  passes: 1
  last_pass: 2026-09-12
  last_pass_state: opus-the-record-behind-every-actor-pass-1
  last_pass_kind: authored
  crossref_clean: true
  reopened_count: 0
---

# The record behind every actor

> **Imported from the research backlog, then re-derived.** The layout is in
> [`../../_types/fields.tsv`](../../_types/fields.tsv) as `ActorStorageRecord` — ~~41 fields~~ 85 rows on 2026-10-02, 41 at import *(answered: measured on `_types/fields.tsv`; 2026-10-02, OPUS)*,
> validated, 0 errors. Query it with `types_index.py --type ActorStorageRecord`.

## 1. What the player sees

Every character, monster, chest and moving thing in an area has a record the engine keeps for it, and
**every record in an area comes out of one block of memory allocated in a single go.**

When an area loads, the engine works out how much room all of its actors will need — **adding up a
size per actor kind, 720 to 1,760 bytes each** — takes that much memory once, zeroes it, and then
cuts it into individual records. **Each record is stamped with what kind of thing it is** before
anything else touches it, and that stamp is what later decides whether the thing can be steered, can
be spoken to, or can fight.

**There is no per-actor allocation and no recycling of individual slots**: an area's actors live and
die together with the block they were carved from.

## 2. ⚠ CORRECTED 2026-09-08 — it is not a recycler

**This section originally concluded that the record is recycled from a pool and that the mask
instructions preserve a previous occupant's bits. That is wrong, and §11 shows why.**

The sole caller, `ActorStorage_AllocateAndInitializeRecords` (`002679F0`), **allocates the whole pool
in one block and `memset`s it to zero** (`00861EC0`) immediately before calling this routine on every
record. **The memory is fresh.** On zeroed memory `and byte [rbx+0x14], 0x7F` and a plain store are
equivalent, so the masks cannot be preserving anything from a prior occupant — **there is no prior
occupant.**

**What the masks are actually for** is `+0x03`, which the *carve loop* writes before this routine
runs and which this routine **reads three times and never writes**. The read-modify-write forms are
how the compiler updates bit-fields inside bytes that are already live — several of them
(`+0x0C` masked twice, `+0x14` masked then rewritten) are this function updating its **own** earlier
work, not someone else's.

**The original text is kept below as the record**, because the instruction forms it lists are correct
and only the conclusion drawn from them was not.

### The instruction forms, which are as described

A constructor writes; this **reads, masks, and writes back**:

```asm
00266573  and byte ptr [rbx + 0x14], 0x7F      ; clear bit 7, keep the other seven
002665C8  and byte ptr [rbx + 0x09], 0xDF      ; clear bit 5, keep the rest
0026661B  and byte ptr [rbx + 0x0C], 0xFE      ; clear bit 0
002666AC  and byte ptr [rbx + 0x0C], 0x8F      ; clear bits 4-6
002666B0  and byte ptr [rbx + 0x13], 0x3C      ; keep ONLY bits 2-5 - the rest cleared
0026665A  or  byte ptr [rbx + 0x0E], 0xF0      ; SET the top nibble
002666F1  and dword ptr [rbx + 0x1C], 0xFFFFDEFF  ; clear bits 8 and 13
```

> **Eleven of the record's bytes are read-modify-written rather than assigned.** ~~For a freshly
> allocated object every one of those masks would be equivalent to a plain store, and the compiler
> would have emitted one. **The masks are there because the previous contents matter.**~~
> **⚠ That inference is withdrawn — see the top of this section.** The object *is* freshly allocated
> and zeroed; the compiler emitted masks anyway, because these are bit-fields the function updates
> more than once and `+0x03` must survive.

Only these are given definite values: `+0x04 = 0xFF00`, `+0x12 = 0xFF`, `+0x18 = 0xFFFF0000`,
`+0xF5 = 0xFF`, `+0x118 = 0x003C0000`, and a set of zeroed pointers and counters.

## 3. Where the record comes from

```c
void ActorStorage_InitializeRecord(Ctx *ctx /*rcx*/, RecordTable *tbl /*rdx*/, int index /*r8d*/)
{
    rsi = *(void **)ctx;
    r11 = 0x00120000;                       /* the image base, held in a register */
    rbx = *(Record **)((char*)tbl + index * 8 + 8);   /* the record for this slot */
    ...
}
```

**`rbx` is loaded exactly once**, at `0026656A`, and reappears only in the epilogue as a restored
callee-saved register. That was checked before any offset below was believed — **a base register
reassigned mid-function would silently merge two different structures' offsets into one layout.**

The table is an **array of pointers with an 8-byte header** (`tbl + index*8 + 8`), so records are
individually allocated and the table indexes them.

**The record stores its own slot number.** ~~The very first field written is~~ The field is written by
`mov word ptr [rbx], r10w` *(Corrected 2026-09-29, OPUS, falsification pass 1 of [the contract](../CONTRACT-actor-storage-record-initialisation.md), `CON-168`: the index store `mov word ptr [rbx], r10w` is at `002665EB`, after six record stores - `+0x14` masked first, then `+0xEC` and `+0xF5` - and the calls `00266AD0` and `00266BD0` with the record. It is not the first field written. The record still carries its own index.)* — `r10` is the sign-extended `index` argument. `+0x00` is the record's
own position in the table.

### ⚠ A note for the globals index

`lea r11, [rip - 0x146556]` puts **`0x00120000`, the image base, in a register**, and the function
then addresses globals as `[r11 + …]`. **That form is invisible to `rip_data_refs.tsv`**, which is
RIP-relative only — the blind spot `globals_index.py` documents. Any "which globals does this
function touch" answer for `00266530` from that dataset is incomplete by construction.

## 4. The layout

~~**41 fields, `+0x00` to `+0x11C`.**~~ **85 rows, `+0x00` to `+0x5A0`, 81 of them inside the `0x120` header** *(answered: `_types/fields.tsv`, measured; 41 at import; 2026-10-02, OPUS)*. The full table with widths, values and evidence is in
[`../../_types/fields.tsv`](../../_types/fields.tsv); the shape:

| region | contents |
|---|---|
| `+0x00`–`+0x03` | slot index (`u16`), a byte, and the **packed kind byte** |
| `+0x04`–`+0x23` | a dense block of **flag bytes and small integers** — eleven of them read-modify-written |
| `+0x28`–`+0x38` | three zeroed qwords |
| `+0x40`–`+0x58` | four pointers, written from computed values |
| `+0xB8` | a **context pointer — read, never written here** |
| `+0xEC`–`+0x11C` | a second block: pointers, counters, and `+0x118 = 0x003C0000` |

**Six spans are undeclared** — `+0x06`, `+0x23`–`+0x28`, `+0x60`–`+0xB8` (88 bytes),
`+0xC0`–`+0xEC` (44 bytes), `+0xF4`, `+0x108`–`+0x10C`. The initialiser does not touch them *(corrected 2026-09-27,
FABLE, Claude Opus 5.5: it fills `+0xC8`–`+0xEB` with `0xFFFF` in one `rep stosw` at `002668B0`, a string store the
scalar census could not see - an 18-slot override array, [FI-1](../../_index/candidates/fi1-offset-names/README.md))*, so
their layout is **unrecovered, not absent**, and the type store records them as gaps rather than
hiding them.

> **`0x11C` is a lower bound, not the size.** It is where the highest field this routine touches
> ends. ~~No allocation site was read, so the record may be larger.~~ *(answered: see "Records are 720 to 1,760 bytes, by kind" below — the allocation site `002679F0` was read; 2026-10-02, OPUS)* The type store says so.

## 5. Two correspondences with the actor in the movement code

[`../../06-Movement-And-Navigation/Facing-And-Steering/how-a-character-turns.md`](../../06-Movement-And-Navigation/Facing-And-Steering/how-a-character-turns.md)
reads an actor with a **packed byte at `+0x03`** (`& 0xE0 == 0x60`, an actor-kind gate) and a
**context pointer at `+0xB8`**. This record has a packed byte at `+0x03` — read here with `& 0x1F`,
the *complementary* mask — and a context pointer at `+0xB8`, read and never written.

> **Two independent offsets agreeing, with complementary masks on the same byte, is real evidence —
> and it is not proof.** The two could be the same type; they could be two types with a shared
> prefix. **Recorded as `PROBABLE` in the type store, not `PROVEN`**, and it is a cheap thing to
> settle: one function that takes both would do it. `EH-1`.

If they are the same type, `+0x03` decomposes as **top 3 bits = actor kind** (what steering gates on)
and **low 5 bits = something this initialiser masks off**.

## 6. Key addresses

| address | size | what |
|---|---:|---|
| `00266530` | 1,439 B | `ActorStorage_InitializeRecord` |
| `0020E600` | 10 B | `ImageAddress_ResolveRuntimePointer` — called ~~6×~~ **7×** (*corrected 2026-09-12 by falsification pass 1; the sites are `00266798`, `002667A9`, `00266903`, `00266976`, `002669C5`, `00266A1F`, `00266A69`*) |
| `003DBB60` | 120 B | `ActorResource_SubmitRequestDescriptor` — called 4×; builds a 9-byte stack descriptor `{kind@+0 (r9 mapped 1→0, 3→2, else keeps r9 — `003DBB7B`–`003DBB9D`), 1@+1, arg-dl@+2, arg-r8w@+4, 0x8000@+6, flag byte@+8 = (arg-byte&1)|(arg2≪1), with bit0 **set** on the unmapped-kind path (`003DBB87`)}` at `003DBBA0`–`003DBBC9`, then submits via `003DBCF0` (`003DBBCE`) |
| `00266AD0`, `00266BD0`, `00268EA0`, `003DB580` | 211/96/439/183 B | `ActorEntity` callees — ~~**not read**~~ read later on this page *(answered: see the region map, §12–§13, and the `+0x1C` passes; 2026-10-02, OPUS)* |
| `00265FF0`, `00268380` | 1,339/420 B | `Movement` callees — ~~**not read**~~ *(answered: `00265FF0` is read on the-movement-and-secondary-context-censuses.md, UQ-91; `00268380` in CONTRACT-actor-storage-record-initialisation.md's pass-22 section; 2026-10-02, OPUS)* |
| `00265B60`, `002681E0` | 1,067/230 B | unowned callees — **not read** |

## 7. Modding notes

- ~~**A recycled actor is not a clean actor.** Only the bits named in §2 are reset; everything else
  in those bytes survives from the slot's previous occupant.~~
  **⚠ Struck 2026-09-13 (OPUS) — stranded by §2's own 2026-09-08 correction.** There is no
  previous occupant to survive from: the pool is allocated in one block and `memset` to zero
  (`00861EC0`) immediately before this routine runs on every slot. **A freshly initialised
  record is zero everywhere this routine does not write**, which is the opposite of the advice
  this bullet gave.
- **`+0x00` is the slot index**, so a record can be identified without the table.
- ~~**`+0xB8` is not initialised here.** Whatever sets the context pointer runs elsewhere; a record~~
  ~~fresh from this routine still points at the previous occupant's context until it does.~~ *(answered: see §16's table, "`00266B54` plants the pointer" — `00266530` calls the planter `00266AD0` at `002665A9`; 2026-10-02, OPUS)*
- **Four `ActorResource_SubmitRequestDescriptor` calls** mean this routine also kicks off resource
  loading — resetting a record is not purely a memory operation.

## 8. What is not known

- [x] ~~**The record's real size.** `0x11C` is where the highest touched field ends.~~ **`EH-2` ANSWERED** in §11 of this document - "the record's real size, and my lower bound was a long way out". The box was never ticked, so the scorer counted a question this page had already answered as open.
- [x] ~~**The six undeclared spans**, 140 bytes in total, the largest being `+0x60`–`+0xB8`.~~
      **Re-measured 2026-09-11 (OPUS, confirmed with `types_index.py --validate`):** fifteen spans,
      70 bytes — declaring rows inside a hole splits it, so the count rose while the bytes fell. The one
      span worth a package is ~~`+0x064`–`+0x078` (20 bytes), initialiser-silent and, per the
      contract's §15, written by nobody among three construction paths and 48 functions~~ —
      **CLOSED 2026-09-12 (`OPUS-CONTRA-RECORDPOOL-VMREGS`): it is the script VM's register file**,
      four `int32` at `+0x64`–`+0x70` and four `float` at `+0x74`–`+0x80`, written by opcode handlers
      `0x36`–`0x3D` and read by `0x3E`–`0x45`. The contract's §15 ruled the interpreter's accesses
      out as sitting on another object; `r15` **is** this record, by the caller chain recorded in
      that contract's §14. The initialiser-silence was real and is the reason it looked empty — the
      writers are opcodes, not construction. `EH-3` loses its largest span.
- [x] ~~**Whether this record and the movement code's actor are the same type.**~~ **`EH-1` ANSWERED** in §11 - PROVEN, not probable: the carve loop in `ActorStorage_AllocateAndInitializeRecords` writes `+0x03` itself, and that is the byte the movement code's gate tests. Same box, never ticked.
- [x] **UQ-95.** **What any flag bit means.** The masks are exact; the semantics are entirely unread. `EH-4`. *(SUPERSEDED in the register 2026-09-26, FABLE, Claude Opus 5.5: a duplicate; the open residue is carried by **EH-4**)*
      **NARROWED 2026-09-16 (FABLE) — two bits of `+0x09` now have a meaning, and the premise was
      already too strong when it was written.**

      **`+0x09` bit 5 is a per-actor time stop that bypasses the seven shared stop sets.**

      - **Writer.** `0035A720(record, mode)`: `mode == 0` → `or byte [rcx+9], 0x20` (`0035A72D`) and,
        when the record has a `battleUnit` (`+0x30` non-null), `00233F50(record, 1)`, `002ED020(record)`
        and `Actor_StopRequestedMovement(record)` (`0035A738`–`0035A74D`); `mode != 0` →
        `and byte [rcx+9], 0xDF` (`0035A754`) and the resume path `002E97B0` → `00269D60`, then
        `0026A770`. `0035A7A0(managerIndex, groupOrMinus1, mode)` inlines the same body for the
        all-actors case (`0035A843` set, `0035A86B` clear) over the manager's records
        ~~`+0x1D6`…`+0x1D6 + 0x1DE`~~ `[+0x1DE]`…`[+0x1DE] + [+0x1D6]` *(corrected 2026-10-02, OPUS: `0035A7C6 movzx edi, word ptr [rax + 0x1DE]` is the start and `0035A7CD movzx esi, word ptr [rax + 0x1D6]` the count)*, **skipping active party members** — its gate is
        `002647B0(record) == 0`, and `002647B0` is `(u8)(int8)[record + 0x12] <= 3`, so it answers
        *"is this record's `partySlot` one of 0..3"* and `0xFF` fails it.
      - **Reader, three sites, one idiom.** `00226A50` and `00226AB0` (the single-actor publishers) and
        `00226640` twice (`00226847`, `0022688C`, the per-actor pass) each compute
        `edx = (stopSet != 0)` with `setne`, then **`test byte [record+9], 0x20` / `cmovne edx, 1`** —
        the bit replaces the computed value.
      - **Consequence.** `00226A50` tail-jumps `00238B40(record, edx)`, which sets **battle unit
        `+0x004` bit 5** iff `edx != 0`; `00226AB0` XORs the value and tail-jumps `00312130`, which
        sets **battle unit `+0x000` bit 36** iff its argument is 0. With the actor bit set both are
        forced on. Those are stop sets 6 and 7 of
        [the time-stop registry](../../00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md) §5.
      - **And the initialiser's own mask now reads as a fact rather than a shape:** `002665C8`
        `and byte [rbx+9], 0xDF` **starts every actor un-stopped.**
      - **A second, independent consequence, found afterwards and worth more than the first two
        because it is not a flag-to-flag relay.** `ActorManager_RunFieldRuntimePass` (`0025DF00`)
        opens one of its branches on a five-term gate at `0025E1E2`-`0025E215`, and
        **`test r8b, 0x20` / `jne` at `0025E208` skips the whole branch when `+0x09` bit 5 is set** —
        `r8b` is `byte[+0x09]`, loaded at `0025E1E2`. The same gate reads `+0x13` bit 1 and `+0x09`
        bit 7 (combined and shifted at `0025E1EE`-`0025E1FA`, which discards `+0x09` bit 6),
        `+0x14` bit 4 (`0025E1FC`), `byte[+0x18]` against zero and `[+0x38]` for null, and on
        success sets `+0x0D` bit 6 (`0025E217`). **So a time-stopped actor is skipped by the field
        pass as well as forced in the battle unit**, which is what a time stop should look like from
        two unrelated directions.

      > **The premise "not one bit's semantics is known" was already false on 2026-09-12.** The
      > time-stop registry page published `00238B40(actor, stopped ‖ actor+0x09 bit 5)` and
      > `00312130(actor, !(stopped ‖ actor+0x09 bit 5))` that day, in its §5 table. The *consumer* half
      > of this bit has been in the database for four days and this page never learned. What is new
      > here is the **writer**, the party exclusion, the movement stop, and therefore the meaning —
      > and the reason to say the rest plainly is that the drift, not the bit, is the reusable lesson.
      > *(Derived from the image first — the reader census below was run and `0035A7A0` read before
      > the registry page was opened.)*

      **`+0x09` bit 1 is a membership marker, and reading it recovered the actor handle's layout.**
      `0046BE80` walks the records and, for each one that `002E97B0` resolves with `[rax] != -1`,
      **skips it when bit 1 is set** (`0046BEF5`); otherwise it packs
      `((word[+0x16] & 0x7FF) << 4 | (byte[+0x15] & 0xF)) << 16 | word[+0x00]` into an output buffer
      and counts it (`0046BEFB`–`0046BF20`). That is `handleTag11`, `handleTag4` and `selfIndex`
      assembled into one dword — **the packed actor handle, whose resolver
      `ActorHandle_ResolveRegistryEntryByPackedId` (`003588B0`) is what `0046B560` then feeds** while
      setting bit 1 on every record it takes (`0046B62E`, `0046B651`); `0046B4C0`, `0046B690` and
      `0046B870` clear it (`and …, 0xFD`). The family is script-reachable — `0050D3A0` is a
      Script-VM-native-bridge thunk to `0046B4C0`. **Not claimed:** what the list is *for*;
      `0046B690` and `0046B870` have no direct caller and are reached indirectly.

      **Reader census, for whoever takes the next bit.** `ActorManager_GetRecordByOrdinal`'s return
      was tainted in all 75 of its callers and followed through register copies, volatile registers
      killed across calls (`Database/Tools/work/FABLE/drift5/eh4_readers.py`; controls `+0x00`,
      `+0x03` and `+0x30` — declared fields — all present). It reproduced the route-proven census
      already on this page rather than extending it, which is the useful result: **the mechanical work
      is done and the gap is semantic.** Per masked offset, from
      [`actor-storage-record-accesses.tsv`](actor-storage-record-accesses.tsv): `+0x08` 25, `+0x09` 33,
      `+0x0C` 33, `+0x0D` 13, `+0x0E` 17, `+0x13` **6**, `+0x14` 30, `+0x1C` 42. **`+0x13` is the
      thinnest and `+0x1C` the richest.**

      **Second narrowing, same day — `+0x0E`, `+0x1C` and `+0x14` bit 7, which is four of the eight
      offsets with a mechanism.**

      **`+0x0E`'s low nibble is the battle unit's runtime category mode.** `00269FE0(record, mode)`
      writes `byte[+0x0E] = (byte[+0x0E] & 0xF0) | (mode & 0xF)` (`0026A033`–`0026A03B`), and its
      caller `BattleUnit_RefreshActorRuntimeFromDefinition` (`00238BF0`) passes
      `movsx edi, byte [unit + 0x58]` (`00238E0D`) — the **runtime category mode** the
      [battle unit field map](../Battle-Unit/the-battle-unit-field-map.md) already carries at
      `+0x058` — with the actor record from `[unit + 0x10]`, skipping the call when the mode is 0
      (`00238E34`–`00238E3E`). **That is what `|0xF0` at `0026665A` is for:** the initialiser sets the
      **top** nibble to all ones, and all three writers on the record preserve it — `00269FE0`
      (`&0xF0`), `00267CC0` (`&0xF4` then `or 4`, so the nibble becomes 4), and
      `ActorSystem_BindBattleUnitsForEligibleRecords` (`&0xF1` then `or r14b`, `00265ACA`/`00265ACE`).
      The field is the low nibble; **nothing on these routes writes the top one again.**

      **`+0x1C` bits 8 and 13 move together, and only for mode 4 on a kind-3 actor.** `00269FE0` gates
      on `(byte[+0x03] & 0xE0) == 0x60`, then on `mode == 4`, and raises `or [+0x1C], 0x100` and
      `or [+0x1C], 0x2000` (`0026A00C`, `0026A01E`), each followed by `00268EA0(record)` when
      `byte[+0x0B] & 8`; **any other mode takes `and [+0x1C], 0xFFFFDEFF`** (`0026A003`), which clears
      exactly that pair. `00267CC0` is the same thing specialised to mode 4, reached when
      `byte[[unit + 0x6A0]] & 0x20` (`00238D98`–`00238DA0`). **So `EH-4`'s `&0xFFFFDEFF` ~~is not an~~
      ~~initialiser mask at all~~ is an initialiser mask too** *(corrected 2026-10-02, OPUS: `002666F1 and dword ptr [rbx + 0x1C], 0xFFFFDEFF` is inside `00266530`, the initialiser — three sites in all)* — the route-proven census puts ~~it~~ a copy at `00265AC3`, in
      `ActorSystem_BindBattleUnitsForEligibleRecords`, and ~~the second copy is~~ another at `0026A003`.

      **Swept, because a two-bit flag nobody sets would be the more interesting answer.** Every write
      at displacement `+0x1C` in all **38,161** listed bodies, immediate or register-sourced
      (`Database/Tools/work/FABLE/drift5/flags1c_bits813.py`). **Six sites carry either bit, and all
      six are these two functions** (`00267CCD`, `00267CDF`, `00267CFE`, `00267D13`, `0026A00C`,
      `0026A01E`). The other 21 immediate hits at that displacement are plainly other objects —
      `0x3EE66666` and `0x40733333` floats, `0xFFFFFFFF` sentinels, `0x300` word writes. 518 writes
      at `+0x1C` come from a register and are not classified; that is the sweep's honest limit, and
      it is why this is a narrowing.

      **The pair has exactly one reader, and it is a predicate that also reads two more of the eight.**
      `003DF6F0(packedHandle)` resolves through `ActorHandle_ResolveRegistryEntryByPackedId`
      (`003588B0`), returns 0 unless `byte[+0x14] & 0x20` (`003DF709`), `byte[+0x08] & 1`
      (`003DF70F`), `002E9FE0(record)` and `0025B7E0(record)` all pass, and finally returns
      `(dword[+0x1C] & 0x2100) != 0` (`003DF73A`) — **the exact complement of the clearing mask.**

      **The whole-word presets, and what they settle about `+0x03`.** `00266BD0` — called by the
      initialiser and by nothing else — switches on `byte[+0x03] & 0x1F` through an eight-entry jump
      table at `00266C30`, reached by **the image-base idiom** (`lea r9, [rip - 0x146BE7]` = `00120000`
      at `00266BE0`, then `mov edx, [r9 + rax*4 + 0x146C30]`), and writes one of five whole-word
      presets: row 0 → `0`, rows 1–2 → `0x38`, rows 3–4 → `0x40`, rows 5–6 → `0x30004`, row 7 →
      `0x34C85`; rows 5 and 7 also `or byte [+0x14], 0x80`. **Those rows are the kind table at
      `01E0C328`** — `{0,0,808} {1,0,936} {1,1,816} {2,0,840} {2,1,720} {3,0,1760} {3,0,1760}
      {3,1,1640}` — and **the presets group exactly by the row's `kind` field.** So `+0x03`'s low five
      bits are **the row index into that table**, which is what §5 left as *"something this initialiser
      masks off"*, and the top three bits are the row's kind: the movement gate's
      `(byte & 0xE0) == 0x60` picks kind 3, rows 5, 6 and 7, **the three largest entries**, exactly as
      `EH-1` says. **No preset carries bit 8 or bit 13**, ~~so an actor holds them only after a mode-4
      refresh.~~ **— and the conclusion is refuted below (sixteenth pass, 2026-09-16): verb
      `0176` `fieldsign` sets both through the generic index setter, with no mode-4 refresh
      anywhere in its path.** The premise about the presets still holds.

      **`+0x14` bit 7's writer pair closes with it.** The initialiser clears it (`&0x7F` at
      `00266573`), `00266BD0` sets it for rows 5 and 7 (`00266C1F`, `00266C24`), and `0025B070` reads
      the byte as `cmp byte [rax + 0x14], 0x80` — true only when **bit 7 alone** is set.

      **Still open, and it is the naming rather than the mechanism:** what a "runtime category mode"
      of 4 *is*, what the bit-8/13 condition means to `003DF6F0`'s one caller `002C64C0`, and the four
      offsets untouched here — `+0x08`, `+0x0C`, `+0x0D` and `+0x13`.

      ---

      **THIRD PASS, SAME DAY, AND IT RETRACTS PART OF THE TWO ABOVE. `EH-4` IS NOT AN OPEN QUESTION.
      IT IS A STALE ONE, AND THE ANSWERS ARE IN THIS DATABASE.**

      I went looking for `+0x08`'s remaining bits, traced `0026AD60` to three script verbs, and found
      the answer already published — **by me, on 2026-09-12, as `BV-3`** — on
      [how the engine chooses 3-D or flat movement](../../06-Movement-And-Navigation/Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md).
      That prompted a corpus sweep instead of more disassembly, and the sweep is the result.

      **Nineteen bits and one nibble of these eight offsets already carry a published meaning, on nine
      pages, none of them this one.**

      | offset | bit | what it means, and where it was already written |
      | --- | --- | --- |
      | `+0x08` | 0 | written by `00269F00`; the consumer is the line pass `0025B250` — the 3-D/flat movement page |
      | `+0x08` | 1–2 | the two-bit **"uses the map"** field, sole writer `0026AD60(actor, on)`, from verbs `007B` `usemapid` (8,210 corpus calls), `040D` `partyusemapid` (459) and `301D` `btlAtelSetCtrlCharPosToOrigin` — **`BV-3` ANSWERED 2026-09-12** |
      | `+0x08` | 2 | also the selector `002E5180` uses at `002E5290` to pick a different distance routine from `Vector3_ComputeXZDistance` for the frame's displacement (**the alternative is named on the movement page, not here** — its caller set reaches a layer this page does not discuss, and the refinement published today says a citation like that belongs in a crossing section or nowhere) — the 3-D/flat movement page and [how a character turns](../../06-Movement-And-Navigation/Facing-And-Steering/how-a-character-turns.md) |
      | `+0x08` | 3 | written with `+0x09` bit 6 by `0026A430`, **the char-hit setter** — [how a script changes how the party looks](../../01-Script-VM-Native-Bridge/Party-Presentation-Verbs/how-a-script-changes-how-the-party-looks.md), 2026-09-08 |
      | `+0x09` | 0 | **field movement enabled** — set at record initialisation, cleared only when the party is captured for a summon (verb `0232` `capturepartyforsummon`) — **`BV-3` ANSWERED 2026-09-12** |
      | `+0x09` | 2 | folded with a controller bit by `003B7770` / `003B7880` — the 3-D/flat movement page |
      | `+0x09` | 5 | the per-actor time stop — **consumer published 2026-09-12** on [the time-stop registry](../../00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md) §5; **the writer is new here** |
      | `+0x09` | 6 | the char-hit setter's other bit, and a field-frame gate |
      | `+0x0C` | 0 | ~~set when the bound script **is the `mapjump` special function**~~ *Corrected 2026-09-30 (OPUS, on SWE2-AUDIT-SPEC's batch-14 narrowing 2): set when the running function is the actor's **`parameter` special function** (footer word `+0x18` = `special[11]`, [`rc12-footer-channels-runstate-0930`](../../_index/candidates/rc12-footer-channels-runstate-0930/README.md))* — [how a script binds to an actor](../../01-Script-VM-Native-Bridge/Interpreter-Core/how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md) |
      | `+0x0D` | 4 | **the near flag** — set when `[02164200] × rec->+0x24 > remaining` — [the facing-and-steering contract](../../06-Movement-And-Navigation/CONTRACT-facing-and-steering.md) and the turning page |
      | `+0x0D` | 5 | gates the position-delta integrator — [heading, speed and the position delta](../../06-Movement-And-Navigation/heading-speed-to-position-delta.md) |
      | `+0x0D` | 6 | set by the field pass at `0025E217` — [the world tick and the field frame](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md) |
      | `+0x0E` | low nibble | **the actor's free-target type**, `ActorRuntime_GetClassNibble` (`00263C20`), authored by the script verb **`setfreetargettype`** (`0x0265`) — **`AL-3` ANSWERED 2026-09-12** on [the battle-record kind byte](../Battle-Record-Kind/battle-record-kind-byte.md) |
      | `+0x13` | 0 | OR-ed into the script-execution stop test — the time-stop registry, set 2 |
      | `+0x13` | 1 | a field-frame gate, composite with `+0x09` bit 6 — the world-tick page |
      | `+0x13` | 7 | ~~written by `0026AD00` as the sign of `edx`~~ **as `edx != 0` — corrected 2026-09-16 (FABLE), fourteenth pass: `neg` sets the carry on a non-zero operand, not on a negative one** — [the battle-unit field map](../Battle-Unit/the-battle-unit-field-map.md) |
      | `+0x14` | 4 | **cleared when the unit pool is full** — [the battle-unit slot pool](../battleunit-slot-pool-and-actor-class.md), 2026-09-12 |
      | `+0x14` | 5 | ~~**explicitly NOT established**~~ **the script *enable* flag** — `FRP-1`, answered 2026-09-18 (FABLE): set by verb `001E enable` and cleared by `001F disable` through the unlisted setter `00269E00` (disable also tail-jumps the entry removal `0025B500`); every pass that would build, line-test or step an entry skips it while clear; [the field-runtime-pass contract](../CONTRACT-field-runtime-pass.md) |
      | `+0x14` | 6 | the field pass's running conjunction, ~~published into slot `+0x12`~~ returned in `eax` *(corrected 2026-10-02, OPUS: `0025DEAB and r12d, eax` folds it, `0025DEE0 mov eax, r12d` returns it; the settled exit stores 0 into slot `+0x12`, `0025DB79`)* — the world-tick page and the same contract |
      | `+0x1C` | 8, 13 | raised when the free-target type is **4** on a kind-3 actor and cleared for any other value — **`AL-3` ANSWERED 2026-09-12** |

      **This is a lower bound built by grep and reading, not a census.** It excludes hits that turned
      out to be a different object — the *spawn* record's `+0x14` bits, a party-roster `+0x0C`, a
      battle-unit `+0x1C` — because a displacement is not an identity.

      **What that costs, stated against my own work.** Two of today's narrowings above are
      **re-derivations published as new, and one of them is weaker than the original**:

      - **`+0x0E` and `+0x1C` bits 8/13 are `AL-3`, answered 2026-09-12.** `AL-3` already has
        `00269FE0` at `0026A033`–`0026A03B`, the kind-3 gate, the `v == 4` rule and the refresh at
        `00238E0D`–`00238E3E`. **It also names the field better than I did.** I called the nibble "the
        battle unit's runtime category mode", which is where the value *comes from* on one route;
        `AL-3` names what it *is* — **the free-target type** — from the verb that authors it, and adds
        `btlAtelSetUnitType` (`0x3005`), the table `{1, 5, 3, 4}` at `01E09EE8`, and the derived
        values 4 and 7. **Read `AL-3`, not my paragraph.**
      - **The `0025E1E2` gate is the world-tick page's, published 2026-09-10**, and that page's count
        is the careful one: **four** record-bit gates, with `test rax, rax` on `+0x38` adjudicated as
        the callback-pointer null check rather than a fifth. My "five-term gate" above is loose.
      - **The time-stop consumers of `+0x09` bit 5 are the registry's, 2026-09-12.** The writer, the
        party exclusion and the movement stop are new here; the relay is not.

      **What survives as genuinely new from today:** `+0x09` bit 5's **writer** (`0035A720` /
      `0035A7A0`) with its party exclusion; `+0x09` **bit 1** as a membership marker and the packed
      actor handle read off `0046BEFB`–`0046BF19`; `00266BD0`'s eight-entry preset table and the
      conclusion that **`+0x03`'s low five bits index the kind table at `01E0C328`**; and the two
      image-wide sweeps, which are the part a route-proven census cannot do.

      **So what `EH-4` should ask now.** Not *"does any bit have a meaning"* — nineteen do. The real
      remainder is small and specific: ~~**`+0x08` bits 4–7, `+0x09` bits 3, 4 and 7,
      `+0x0C` bits 1–7, `+0x0D` bits 0–3 and 7, `+0x13` bits 2–6, `+0x14` bits 0–3 and 7, and
      `+0x1C` outside bits 8 and 13** — plus `+0x14` bit 5, which `FRP-1` already owns as not
      established.~~

      > **REBUILT 2026-09-16 (FABLE) — and the sentence was wrong on the day it was written.**
      > The **fourth pass's own table**, eight lines above this paragraph, names **`+0x08` bit 7**
      > (`020F` `setnochecktouchheightflag`, `00352BE0` → `0026BED0`) and **`+0x0D` bit 1** (`0234` /
      > `0235` `rootmoveenable` / `rootmovedisable`). **The same pass then listed both as open, two
      > paragraphs later.** The sixth pass answered **`+0x08` bit 4** (the character-SE-play flag,
      > verb `04D9` through `0035A990`) and an earlier narrowing answered **`+0x14` bit 7** — and
      > neither touched this sentence either.
      >
      > **I found that by re-deriving `+0x08` bit 7 from the shipping bytes today** — the same
      > fourteen-byte `0026BED0`, the same verb — and only discovering it was already published when
      > I grepped this page before writing it down. **That is the `EH-4` failure repeating inside the
      > page that was written to repair it**, and the lesson generalises past this record: *a page's
      > own summary is a claim about the page, and must be checked against it* — the same rule the
      > source hierarchy states for a document describing a function. **No gate compares a page's
      > summary to its own body**, and a peer's `check_premise_refuted` cannot: it joins a register
      > row's heading to the type store, not a paragraph to the paragraphs above it.

      **The remainder, rebuilt bit by bit against this page's body:** **`+0x0D` bits 2 and 3,
      `+0x13` bits 2–6, `+0x14` bits 0–3, and `+0x1C` outside bits 8 and 13.** Separately, and
      in a different column because they are **stated non-findings rather than unknowns**: `+0x08`
      bit 5 (read twice, no writer found — seventh pass) and `+0x14` bit 5 (~~`FRP-1` owns it as not~~
      ~~established~~ the script enable flag *(answered: `FRP-1`, 2026-09-18, in the bit table above; 2026-10-02, OPUS)*).

      > *Kept current, 2026-09-16 (FABLE).* The ninth pass closed `+0x0C` bits 4 and 5 and the tenth
      > closed `+0x09` bits 3, 4 and 7, and **this sentence is the one the tenth pass names as having
      > gone stale about bit 7** — so leaving it unstruck would repeat, on this page, the propagation
      > failure that pass is about. The passes themselves are appended below; the struck items are
      > answered there, not here.

      > **The lesson is not about this record.** A question survived six days after the corpus had
      > answered it, on a page that links to none of the nine pages that did, and it cost a full round
      > of re-derivation before anyone checked. **No gate compares an open question's premise against
      > the corpus**, and `check_questions --drift` cannot: it compares boxes to rows, not claims to
      > evidence. Routed to OPUS with the size staleness on the same page.
      >
      > **And a first measurement of how large the class might be, so the routing is not a hunch.**
      > The register holds **forty-six** distinct OPEN rows whose own text carries a universal
      > negative — *"not one … is known"*, *"entirely unread"*, *"no body has been read"* and
      > their kin. **Most will be honest**: a row saying no PPFX function body has been read is very
      > likely right, and a candidate list is not a finding. But it is the population a checker would
      > triage, one regular expression over the register produced it, and **one of the forty-six is
      > now known to be false** — this one. That is the argument for instrumenting the class: the
      > test is cheap and the first sample came back positive.

      ---

      **FOURTH PASS — four more bits, and the script verbs name them.** The `0026ADxx` block turns out
      to be a row of tiny generated bit setters, each `(record, bool)`, and every one of them has a
      verb behind it. **A verb's own name is authored evidence**, which is the strongest kind
      available for a flag bit short of running the game.

      | bit | verb | what the verb does with it |
      | --- | --- | --- |
      | `+0x0D` bit 1 | **`0234` `rootmoveenable`** and **`0235` `rootmovedisable`** | `003487D0` is `mov edx, 1 / jmp 0026B500` and `00348B80` is `xor edx, edx / jmp 0026B500` — **an enable/disable pair on one bit**, neither taking an argument. `0026B500` writes the bit and then tail-jumps a publisher with the same value, so the flag is pushed onward rather than only stored. Read by the field pass at `0025E328` and by `002E7104`. |
      | `+0x08` bit 7 | **`020F` `setnochecktouchheightflag`** | `00352BE0` pops the int and tail-jumps `0026BED0`, which is fourteen bytes and does nothing but write bit 7 from it. **The verb names the flag outright**, which is as close to an authored name as this record gets. |
      | `+0x08` bit 3 | **`0083` `usecharhit`** | `0034D120` pops the int and tail-jumps `0026A430`, which writes **both** `+0x08` bit 3 and `+0x09` bit 6 from it. |
      | `+0x09` bit 6 | **`0083` `usecharhit` AND `02FE` `usecamerahit`** | `0034D420` (`usecamerahit`) tail-jumps `0026A3A0`, sixteen bytes, which writes **only** `+0x09` bit 6. |

      > **And that asymmetry corrects a reading the corpus already invites.**
      > [How a script changes how the party looks](../../01-Script-VM-Native-Bridge/Party-Presentation-Verbs/how-a-script-changes-how-the-party-looks.md)
      > lists `0026A430` as *"char-hit setter … `+0x08` bit 3 and `+0x09` bit 6"*, which is correct
      > about that function. But **`+0x09` bit 6 is written by the CAMERA verb as well**, so it cannot
      > be read as the char-hit bit: `usecharhit` sets both, `usecamerahit` sets only bit 6.
      > **Established:** those two writers and those two values. **Interpretation, and flagged as
      > interpretation:** that bit 6 is the camera-hit bit and character hit implies camera hit, which
      > would explain why the narrower verb sets both and the broader one sets one. Nothing here
      > proves that; two verbs sharing a bit would also be explained by them being mutually exclusive
      > per actor, and no reader distinguishes them.

      **Where that leaves the remainder.** `+0x08` now has bits 0, 1–2, 2, 3 and 7 named and **bits 4,
      5 and 6 left**; `+0x0D` has bits 1, 4, 5 and 6 named and **bits 0, 2, 3 and 7 left**. Counting
      the nineteen from the inventory plus these, **twenty-three of the eight offsets' bits now carry a
      meaning**, and `EH-4`'s text still says none does.

      ---

      **FIFTH PASS — the method generalised, and it corrects one of my own claims above.** Every body
      of 80 bytes or less that read-modify-writes one of the eight offsets was collected and its
      callers joined against `scriptvm-verb-table.tsv`
      (`Database/Tools/work/FABLE/drift5/verb_backed_bits.py`): **123 short setters, 16 with a verb
      behind them, 107 without.** *(Qualified 2026-09-27, FABLE: three of the 16 - the `+0x13` LOD setters - write the secondary context, not this record; 13 stand. See the correction under the table.)*

      | offset | bits | the verb that authors it |
      | --- | --- | --- |
      | ~~`+0x13`~~ | ~~**the whole byte**~~ | ~~`0160` **`setlod`**, `040F` **`partysetlod`**, `042A` **`puppetsetlod`** — three verbs, one byte, written with `mov byte [rcx+0x13], dl`~~ *struck 2026-09-27 (FABLE, Claude Opus 5.5): a receiver error - `rcx` is not this record; see the correction below* |
      | `+0x0E` | bit 4 | `0389` **`settalkiconstatus`** |
      | `+0x0E` | bit 5 | `038B` **`setnavimapdrawstatus`** |
      | `+0x0E` | bit 6 | `053A` **`settargetliststatus`** |
      | `+0x0E` | low nibble ← 5 | `048F` **`gimmick_to_npc`**, which is `and 0xF5 / or 5` — it forces the **free-target type to 5** |
      | `+0x0C` | bit 7 | `02BE` **`setuptreasure`** and `0403`/`0493` **`set_talk_without_hide_status`** |
      | `+0x0D` | bit 3 | `0176` **`fieldsign`** and `0239` **`recttocircle`**, the latter passing a constant 1 |
      | `+0x0D` | bit 0 | set by `002EB330`, cleared by `002EB030` — the motion-bind pair, both of which also stamp `+0xF5 = 0xFF` and zero `+0xEC`, so the base is certainly this record. Reachable from `2000` `debug_bindp`, `2010` `debug_setmotion` and `207C` `debug_skillmotion`, which is how the sweep found them; the debug verbs are **not** the main route and the names are correspondingly weaker evidence than `rootmoveenable`'s. |

      > ~~**`+0x13` IS THE LOD BYTE**, and that settles two loose ends at once: the initialiser's
      > `&0x3C` at `002666B0` is masking a level-of-detail value, and `0025E2AA`'s
      > `cmp byte [rdi+0x13], 0x80` is testing the top bit of one — which `0026AD00` writes as the
      > sign of its argument, exactly as the battle-unit field map already recorded without knowing
      > what the byte was.~~

      ***Corrected 2026-09-27 (FABLE, Claude Opus 5.5), on OPUS-REQ-FABLE-EH4-1C-PRESETS-STRIKE: the LOD verbs do not write this record.** `setlod`'s setter `002EC680` loads `[rcx + 0xC0]`, the actor's secondary context, and stores through it (`002EC685`, `002EC691`); `puppetsetlod`'s `002EC6A0` gets a puppet-table entry + `0x10`; the shared tail's three callers pass the context. The type store already names that byte `SecondaryContextElement +0x013 lodLevel`. So `&0x3C` at `002666B0` and `cmp byte [rdi+0x13], 0x80` are about this record's own `+0x13`, whose bits keep the meanings the tables above give them; the thirteen other verb-backed setters stand. Control [`eh4_lod_receiver.py`](../../_index/candidates/eh4-1c-presets/eh4_lod_receiver.py) (OPUS; re-run by FABLE, FAILS 0).*

      > **AND THIS RETRACTS A CLAIM OF MINE FROM THE SECOND PASS ABOVE.** I wrote that `+0x0E`'s field
      > is the low nibble and *"nothing on these routes writes the top one again"*. Scoped to the three
      > writers I had then, that is true. **Read plainly it is false**: `settalkiconstatus`,
      > `setnavimapdrawstatus` and `settargetliststatus` each write one bit of the top nibble, and the
      > initialiser's `|0xF0` sets all four on at construction. **So `+0x0E` is a free-target type in
      > the low nibble and three named status flags in the top**, with bit 7 still unaccounted. A
      > scope qualifier a reader has to reconstruct is not a qualifier.

      **One candidate refused on reading, and it is the failure mode this sweep invites.** `00C7`
      **`bluralpha`** reaches a setter that writes `[rcx + 0x1C]`, so the displacement matched. Its
      handler passes **`rcx = 0`**, not an actor, and the setter clamps that to 0–3, computes
      `02B58A90 + idx * 0x68` and writes `[+0x34]`. **It is a four-element post-process array, nothing
      to do with this record.** Displacement is not identity, and a sweep keyed on displacement has to
      be read before it is believed.

      **Where the remainder stands: thirty-one of these offsets' bits now carry a meaning**, and the
      **107 verbless short setters are the next seam** — each is a lead with a caller list rather than
      a name.

      ---

      **SIXTH PASS — one more bit, and the thing that ties four of these threads into one mechanism.**

      **`+0x08` bit 4 is the character-SE-play flag.** `0035A990` is structurally the twin of the
      time-stop sweep `0035A7A0`: manager from `00263FF0`, walk the records from `+0x1D6` for
      `+0x1DE`, skip active party members with `002647B0`, and set `+0x08` bit 4 from the argument
      (`0035A9F6`–`0035AA03`). **Sole caller `00348BA0`, which is verb `04D9`
      `setcharseplay_freetarget_group`.**

      **And the verb's name gives up the selector both sweeps share.** Each filters on
      `00263BE0(record) == selector`, and `00263BE0` reads **`byte[+0x0E] & 0xF` — the free-target
      type** — and maps it to one of three groups:

      | free-target type | group |
      | --- | --- |
      | `1`, `2`, `7` | **0** |
      | `3` | **2** |
      | `0` and everything else | **1** |

      > **That upgrades the time-stop answer above, which was mine and incomplete.** I recorded
      > `0035A7A0(managerIndex, groupOrMinus1, mode)` and said the sweep runs over the manager's
      > records skipping active party members. It does — **but the group argument is this group**, so
      > **the per-actor time stop is applied per free-target group**, not to an undifferentiated set,
      > and `−1` is the all-groups case rather than the only case. `+0x09` bit 5 and `+0x08` bit 4 are
      > two flags driven by **the same selector over the same population**, and `+0x0E`'s nibble is
      > what the selector reads.

      > **And it answers what I left open about `+0x09` bit 1.** The fourth pass established that bit
      > as a membership marker in an enumeration and said plainly that *what the list is for* was not
      > claimed. **`0046B690`, `0046B870`, `0046BAC0` and `0046BD60` all call `00263BE0` too**, so the
      > family that sets and clears bit 1 is selecting actors **by free-target group** — which is what
      > the list is. The packed-handle assembly at `0046BEFB` is how the selection is handed on.

      **So the shape underneath these bits is one mechanism, not four accidents:** `+0x0E`'s low
      nibble types an actor, `00263BE0` buckets that type into three groups, and script verbs act on a
      whole group at once — stopping it (`+0x09` bit 5), enabling its sound (`+0x08` bit 4), or
      enumerating it (`+0x09` bit 1). **Thirty-two bits with a meaning, and the four that were
      strongest now share one reading.**

      ---

      **SEVENTH PASS — `+0x08` bit 5 is read twice and, on everything I can find, never set. Stated
      as a challenge to itself rather than as a result.**

      **Every byte access at `+0x08` in `00250000`–`00280000`**, which is where all five confirmed
      writers live: readers of bit 0 at `0025B2A0`, `0025BEB1`, `0025C1C6`; readers of **bit 5** at
      `0025C3E1` and `0025CC86`; bit 6 tested and set four times inside
      `ActorManager_RunFieldRuntimePass`; and the writers — `0026A430` bit 3, `0026AD60` bits 1–2,
      `0026BED0` bit 7, plus whole-byte stores in the two initialisers. **No `or`, `bts` or
      register-sourced store anywhere sets bit 5.**

      **And the two whole-byte writers cannot introduce it either.**
      `00265FF0`'s three stores are read-modify-writes on the old value — `and al, 0xFB / or al, 0x0A`
      and `and al, 0xF5 / or al, 4` twice — and **not one of them touches bit 5**. The record
      initialiser writes `+0x08` three times from `dl`, and **`00266607 and dl, 0xDF` clears bit 5
      between the first store and the second**, so the value left at the end of construction has bit 5
      clear whatever `dl` arrived with. The pool is one `memset`-zeroed allocation (`EH-6`), so the
      byte starts at zero as well.

      **Which makes both tests branches that cannot be taken.** Each is
      `test byte [rdi+8], 0x20 / je`, so the guarded block runs *only* when the bit is set.

      **What would refute this, and none of it has been ruled out.** A write through a pointer already
      advanced past `+0x08` carries no displacement and is invisible to a displacement census. A
      writer outside `00250000`–`00280000` would not have been listed — the range was chosen because
      every *confirmed* writer sits in it, which is a reason to look there first and not a reason to
      look nowhere else. And `dl` arriving at the **first** store with bit 5 set would put it in the
      record briefly, before `00266607` clears it; nothing reads the record during construction, but
      that is an argument rather than a measurement.

      **So this is filed as a reachability question, not a dead-code finding.** *"Cannot be taken"* is
      exactly the class of claim this page challenges elsewhere, and it would be poor form to make one
      here without saying how to break it.

      ---

      **EIGHTH PASS — one bit closed from the verb to the integrator, and one that is a constant.**

      **`+0x0D` bit 5 means "this actor has a non-zero position offset", and the whole path is
      readable.** Verb `0505` **`setposoffset`** (`00348F80`) pops three floats and calls `0026B170`,
      which is gated on kind 3, takes the movement context from `[actor + 0xB8]`, **stores the offset
      at context `+0x40` / `+0x44` / `+0x48`**, then computes `x² + y² + z²` and
      **`and byte [actor+0x0D], 0xDF` when that is zero, `or byte [actor+0x0D], 0x20` when it is not**
      (`0026B1E2`–`0026B1EF`). `rcx` is never reloaded between the entry and those two stores — only
      `rax`, the context — so the base is this record.

      > **And its reader is already written up on another page.**
      > [Heading, speed and the position delta](../../06-Movement-And-Navigation/heading-speed-to-position-delta.md)
      > carries `if ((a->flags0D & 0x20) == 0)` in its reconstruction, guarding two of the three
      > facing publishes. So the chain runs **verb → context offset → bit → integrator branch**, and
      > the bit is not a mode but a **cached predicate**: *is the stored offset non-zero*. Nothing had
      > to be inferred at any step.

      **`+0x0E` bit 7 is set once and never touched again.** Every one of the ten
      read-modify-writers of `+0x0E` in `00250000`–`00280000` preserves it — the masks are `0xF5`,
      `0xF1`, `0xBF`, `0xF0`, `0xDF`, `0xEF` and `0xF4`, and not one clears bit 7 — while the
      initialiser sets it with `or 0xF0` (`0026665A`) and clears the low nibble with `and 0xF0`
      (`002666F8`), so **construction leaves `+0x0E` at exactly `0xF0`**: free-target type 0, all four
      top-nibble flags on. **No bit test reads it**; the seven whole-byte `movzx` readers could, and
      none of them was traced far enough to say. So: **a bit that is 1 from construction onward, with
      three siblings that verbs turn off and on and no evidence that this one is ever consulted
      alone.** Recorded as that, and not as "unused".

      **Thirty-four bits with a meaning.**

      ---

      **NINTH PASS — `+0x0C` bits 4 and 5, and one of them is not the boolean it looks like.**

      **`+0x0C` bit 4 means "a movement speed has been requested".** It is set by
      **`Movement_SetRequestedSpeed`** (`0026D74C`), cleared by the movement update at `002E5353`
      (`and …, 0xEF`), and read at `00268256`, `002E52C3` and `00358FF4`. Writer, clearer and three
      readers, all named already — the bit simply had not been joined to them.

      **`+0x0C` bit 5 is the event-wake-rect flag, and the caution is worth more than the name.** Its
      only writer is `0026A660`, whose sole caller is verb `03DF` **`seteventwakerect`** (`0034DCA0`,
      the standard wrapper: pop the argument, actor in `rcx`, tail-jump). **Argument 0 clears the bit
      unconditionally** (`0026A6FE`). **A non-zero argument does not simply set it** — the body first
      indexes a `0x288`-stride table at `02098E10` by the actor's `handleTag4` (`+0x15`), checks
      `+0x18` and `+0xD2`, and resolves a script-image entry through `+0x40` and
      `ImageAddress_ResolveRuntimePointer`, only reaching `or byte [rdi+0x0C], al` at `0026A70F`
      afterwards. **So the bit records that the verb's request was accepted, not that it was made.**
      Reading it as a mirror of the argument would be wrong in exactly the cases that matter.

      Its readers are `0025C830` twice and `0025D5E0` once, and `0025D5E0` is ~~a shared predicate that~~
      **the request-bit clearer, which** **`02BF` `talktreasure`, `002B` `reqdisable` and `0176` `fieldsign`** all call. *Corrected 2026-09-16 (FABLE), sixteenth pass: it answers nothing — it performs a refusal, which is a different thing and is why the word mattered.*

      **Thirty-six bits with a meaning.**

      ---

      **TENTH PASS — a three-verb family closes `+0x09` bits 2, 3 and 4, and a fourth bit was
      already answered on another page of mine.**

      **`+0x09` bit 4 means "this actor has registered itself as a battle target".** Its **sole
      writer is the whole of `00346D10`** — verb **`0192` `registbattletarget`**, a **five-byte
      handler**: `or byte [rdx+0x09], 0x10` and `ret`. There is no argument, no gate and no second
      instruction. Its consumer is `003B6F80`, tail-jumped from `00346FA0` = verb **`0193`
      `setupsummonforevent`**: it walks the three kind blocks (`00263FF0` for the block,
      `ActorManager_GetRecordByOrdinal` for each ordinal in `[+0x1DE, +0x1DE + +0x1D6)`), tests the
      bit at `003B6FFD`, and collects up to **31** registrants other than the caller as encoded
      handles (`ActorHandle_EncodeRegistryEntry`). **Then it clears bits 2 and 4 on every actor it
      walks** — `and byte [rbx+0x09], 0xEB` at `003B7020`, outside the `if`. So the registration is
      **consumed**, not merely read: two `setupsummonforevent` calls in a row gather different sets.

      > **And the same loop corroborates yesterday's bit.** It calls
      > `Actor_StopRequestedMovement` (`0026D6D0`) on every actor it visits — the mechanism whose
      > flag is `+0x0C` bit 4, named in the ninth pass. The clean-up is not incidental to the
      > gather; it is the gather.

      **`+0x09` bit 3 is a scratch bit, and saying so is the finding.** It lives entirely inside
      `003B6DE0`, the routine `003B6F80` hands its list to. The first loop resolves each handle and
      **clears bit 3 while setting bit 2** (`and 0xF7` at `003B6E52`, `or 4` at `003B6E56`); the
      second loop compacts the pointer array and **tests bit 3** (`003B6E8A`) to drop a repeated id,
      **setting it** (`003B6E95`) on the first occurrence. Nothing outside that one function reads or
      writes it. It is a **uniqueness mark for one pass over one list**, kept in the actor record
      because the list is a list of actors — not a state of the actor, and a consumer that read it
      between calls would be reading residue.

      **`+0x09` bit 2 was already listed here as "folded with a controller bit". It now has a
      destination, a consumer and a polarity — and the polarity is the opposite of the obvious one.**
      `003B7770` and `003B7880` walk the same three kind blocks and compute, per actor,

      > `secondaryContext[+0x10] bit 1 := (actor[+0x09] bit 2) OR (secondaryContext[+0x14F] bit 0)`

      (`003B77FC`–`003B7833`, `003B791E`–`003B7962`), forcing it **set** for the actor recorded at
      `02EBCC68` — the summoner `003B6DE0` stores there. And `+0x10` bit 1 is a **visibility
      requirement**: `Actor_RefreshPresentationVisibility` (`002E8FD0`) admits the actor only when
      `byte[secondary+0x10] & 0x0B == 0x0B`, or `& 3 == 3` when `+0x11` bit 5 is set
      (`002E9052`–`002E9069`), and it is the **failing** arm that takes the `003E6A60` call.
      The same `+0x10` already carries **bit 0 = shown by script target group** and **bit 3 = the
      presentation-visibility enable**, both on
      [the context censuses](../Actor-Contexts/the-movement-and-secondary-context-censuses.md).

      **So bit 2 is an allow-list, not a hide flag: "stay visible through the battle-target
      presentation".** Every writer agrees. `setupsummonforevent` clears it on everybody
      (`003B7020`) and sets it only on the gathered registrants (`003B6E56`); `003B6D60` sets it on
      the party **leader alone** and publishes a one-entry list; `003B6CC0` clears it on **all four**
      roster slots; and verb **`0197` `shownobattletarget`** (`003480C0` → `003B8090`) sweeps every
      actor in every kind, sets `+0x10` bit 1 **directly** and clears bit 2 — the teardown that puts
      the world back.

      > **This corrects a universal on another page.**
      > [How the engine chooses 3-D or flat movement](../../06-Movement-And-Navigation/Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md)
      > says of secondary-context `+0x14F` bit 0 that **"every reader of bit 0 is a movement veto"**
      > and lists `003B7770` / `003B7880` among them, describing the fold as one *"not free-standing"*
      > flag. **The fold is real and at the cited addresses** (`003B7812`, `003B7934`) — but its only
      > destination is the presentation-visibility byte and its only consumer is
      > `Actor_RefreshPresentationVisibility`. **These two readers are not movement vetoes**, so the
      > universal is too strong. Nothing here is said about that page's other six readers, which are
      > not in question; the claim that needs narrowing is *"every"*.

      **`+0x09` bit 7 is not a discovery today. It is a propagation failure of mine.** The writer is
      `00263560`: it forms `bl = (byte[02099DE3] | byte[02099DE4] | byte[02099DE5] | byte[02099DE6])
      != 0`, gates on `byte[02098E20]` bit 0, and for each registered record of the four-entry roster
      at `0209A1F0` calls `00238B40(rec, bl)` and `00312130(rec, !bl)`, then writes the bit —
      `and byte [rsi+0x09], 0x7F` / `shl bl, 7` / `or byte [rsi+0x09], bl` (`002635EF`–`002635FF`) —
      and zeroes the requested speed. **I published that sentence on
      [the field record table](../../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md)
      on 2026-09-12 under `FZ-28`** — *"writes the roster byte `+9` bit 7 to it"* — **and never
      carried it here**, where the remainder paragraph below still lists bit 7 among the unknowns and
      the field-frame note reads the bit without a meaning. So the bit is **a per-party-member cache
      of the party hold**: the same boolean the time-stop registry receives, on the same iteration,
      for the same four records.

      **What is genuinely new today about bit 7 is its reader.** The composite at
      `0025E1E2`–`0025E1FA` in `0025DF00` loads `byte[+0x09]` and `byte[+0x13]`, masks `+0x13` to
      bit 1, shifts `+0x09` right by six, ORs, then shifts right by one — **which discards `+0x09`
      bit 6 and leaves `(+0x13 bit 1) | (+0x09 bit 7)`** — ORs the third term from
      `00359B80(actor)[+0x40]`, and `jne` past the rest. The rest is the `[actor+0x38]` callback
      raised at `0025E217`–`0025E222`. **A party member under the hold does not get that call.**

      **Thirty-nine bits with a meaning**, and one of the three was four days old on a page that
      does not link to this one.

      ---

      **ELEVENTH PASS — `+0x0D` bits 0 and 7, and a reader that no bit-mask sweep can see.**

      **`+0x0D` bit 0 is not a state of the actor. It is the mode the last standard-motion start
      used, cached on the record.** Six functions start a standard motion, and they are
      instruction-for-instruction identical apart from **three** things — the bit, where the motion
      id comes from, and where the blend comes from:

      | entry | `+0x0D` bit 0 | id → `+0xF0` | blend → `[rsp+0x20]` | `002EB0D0` arg 4 |
      | --- | --- | --- | --- | ---: |
      | `002EB330` | **set** (`or 1`) | `edx` | `-1.0f` | `0` |
      | `002EB380` | **set** | **`0x1001`**, fixed | `-1.0f` | `0` |
      | `002EB3E0` | **set** | `edx` | `xmm2` | `0` |
      | `002EB030` | **clear** (`and 0xFE`) | `edx` | `-1.0f` | `1` |
      | `002EB430` | **clear** | **`0x1001`**, fixed | `-1.0f` | `1` |
      | `002EB4F0` | **clear** | `edx` | `xmm2` | `1` |

      All six also write `+0xF5 = 0xFF` and `+0xEC = 0`, and all six **skip the call entirely** when
      `byte [actor+0x18] == 1`. So the bit is **the complement of `002EB0D0`'s fourth argument** —
      and inside `002EB0D0` that argument is the only thing deciding whether the blend is consulted
      at all: `test esi, esi` at `002EB23F`, where non-zero commits through `00427860` on the
      `0x740`-stride record at `[022C6F28]` and zero instead loads the float from `[rsp+0x60]` and
      compares it against `0.0`.

      **Its three readers are vetoes, and they are the smallest functions on this page.**
      `002E7090` (16 B) and `002E70C0` (16 B) each `test byte [rcx+0x0D], 1` and **tail-jump to their
      real work only when the bit is clear** — `00325090` and **`BattleUnit_HandleActionTimelineEvent`**
      (`00325260`, `CombatAction`) respectively; `002E70A0` (23 B) does the same for `003250F0` and
      additionally requires `[actor+0x30]` non-null. Nothing reads the bit any other way.

      > **The asymmetry is the finding, not the polarity.** The three **clearing** entries are called
      > from **26** listed bodies — script verbs, `BattleUnit_DispatchActorPresentationEvent`, the
      > party read-in — while the three **setting** entries have **five direct callers** between them.
      > So the ordinary way to start a standard motion leaves the action timeline live, and setting
      > the bit is the exception, not the default. **This is a count of listed bodies, not of the
      > engine**: both a table dispatch and one of the unlisted blocks would be invisible to it, and
      > two of those five callers (`0050D810`, `0050E3A0`) are themselves called by no listed body.

      **`+0x0D` bit 7 means "relax by yourself when the standard-motion read finishes".** Its sole
      writer is verb **`0266` `setautorelax`** (`00352CE0`, 38 bytes): it pops the argument through
      `VMValueStack_PopInt32CoerceFloat32`, forms `cl = (result != 0)`, and writes
      `and byte [rbx+0x0D], 0x7F` / `shl cl, 7` / `or byte [rbx+0x0D], cl` (`00352CF6`–`00352CFD`).
      Its sole reader is the **poll** of verb **`0119` `stdmotionreadsync`** (`0034B8D0`): when the
      read has completed (`002E4C30` answers `> 0`) it calls `002EAC90`, and **only then, only if the
      bit is set**, `002EB380` — the fixed-`0x1001`, bit-0-**setting** row of the table above. So the
      two bits meet: *auto-relax* starts motion `0x1001` with no further verb, in the mode that
      vetoes the action timeline.

      > **Why eight passes of mask sweeps never saw this bit.** The reader is not a `test`. It is
      > **`cmp byte [rdi+0x0D], 0x80` with `jb`** at `0034B927` — an unsigned compare against `0x80`,
      > which for a byte *is* a bit-7 test, and which no sweep for `test`/`and`/`or` immediates will
      > return. **The method has a blind spot and it is worth writing down**, because the remaining
      > bits on this record are exactly the ones the cheap sweep could not find.
      >
      > *Triaged before publishing, so the warning does not become a scare:* the sweep finds two
      > other byte compares at displacement `+0x0D` in the image, `002A7A60` and
      > `RelationLook_RemovePooledRelationRecord` (`00512CD0`), and **neither is this record** —
      > the first walks a cursor with word indices at `+0x14` / `+0x16` and word fields at
      > `+0x18`–`+0x1E`, the second is a Presentation pool. **A displacement is not a structure**,
      > which is the same caution this page applies to every route-free census.

      **On `0x1001`.** It is the only literal motion id in the six, and it is the id the engine
      starts on its own behalf, from both the setting and the clearing side. Calling it *the relax
      motion* rests on **verb `0266`'s own name and that fixed id**, not on a read of a motion table —
      the table has not been opened here, and if it disagrees it wins.

      **Forty-one bits with a meaning.**

      ---

      **TWELFTH PASS — `+0x0C` bits 1, 2, 6 and 7, and the byte is down to one.**

      **`+0x0C` bit 1 means two positioned records overlap in XZ.** Both setters sit immediately
      after a call to `003DA5A0` and a `comiss` against a register that is **zero** — `xorps xmm7,
      xmm7` at `0025BB84`, never rewritten before `0025BC79`; the `0025C830` site has the same shape
      at `0025CF66`. And `003DA5A0` returns a **signed gap**, not a distance: it subtracts the two
      positions component-wise, sums the squares of **X and Z only** (dropping Y at `003DA646`),
      takes the root, and finishes `xmm0 = distance - (r1 + r2)` (`003DA66E`, `003DA686`) from the
      two radii at `[rdi+0x0C]` and `[rbx+0x0C]`. It also writes the delta vector and a `1.0f` to an
      optional out-parameter. So the bit is set **exactly when that gap is negative**.

      > **Not "the movement body", which is a term this database already owns.** The
      > [movement-context census](../Actor-Contexts/the-movement-and-secondary-context-censuses.md)
      > resolves `003DA5A0`'s arguments to the **movement context at `+0x30`, `+0x40`, `+0x60` and
      > `+0x70`**, reading the radius at each `+0x0C`. So the two operands are `0x10`-spaced
      > *position-plus-radius records inside the movement context*, **not** entries of the 128-entry
      > pool behind the context's `+0x138` that
      > [the body pool page](../../06-Movement-And-Navigation/the-movement-body-pool-and-the-separation-pass.md)
      > calls a body. I nearly wrote *body* and it would have pointed a reader at the wrong structure.

      It is a **per-frame** flag: `0025C170`, called by `ActorManager_RunFieldRuntimePass` once per
      kind, **clears it on every record** at `0025C1BC` before the pass does anything else. And its
      query is `0025B4C0` — resolve the packed id, return `(record[+0x0C] >> 1) & 1` **only for kinds
      1 and 3**, zero otherwise — whose callers include
      **`InputGameplay_ArbitrateDigitalInputAndModalState`**.

      > **The caution is on the name, not the mechanism.** *Overlap* is what the arithmetic says.
      > Whether the game means by it *"the player is close enough to interact with this"* is a
      > reading of who asks, and one of the five askers is input arbitration. **Recorded as the
      > overlap, with the readers named**, so a later page can make the interaction claim on its own
      > evidence rather than inheriting it from here.

      **`+0x0C` bit 2 is a cached predicate on a movement-context dword, and the two sites do not
      agree on which dword.** Both are `cmp` / `je` pairs that set the bit when a dword is non-zero
      and clear it otherwise. In `0025C230` the dword is **`movementContext[+0x100]`**
      (`0025C6F2`–`0025C701`; `rbp` is `[actor+0xB8]`, loaded at `0025C268`, and `rdi` is the record).
      In `0025C830` it is **`movementContext[+0x60]`** against a register still zero from
      `0025C869` (`0025D22B`–`0025D237`) — **and the same function zeroed that dword itself** at
      `0025C8B9`, so there the bit reads *"`+0x60` became non-zero during this pass"*.
      [The movement-context census](../Actor-Contexts/the-movement-and-secondary-context-censuses.md)
      records `+0x100` with one reader and one writer, both `0025C230`, which is consistent with a
      value private to that pass. **What the two dwords have in common is not established here**, and
      the honest reading is *a cached per-pass predicate* rather than one named condition.

      **`+0x0C` bit 6 is a once-only latch, and the block it guards is worth more than the bit.**
      Inside `0025C830`, when `003DBB60` answers 1 and a second discriminant is 2, **and the bit is
      clear** (`0025D3B2`), the pass runs a block that increments
      `[02098E10 + handleTag4*0x288 + 0x1E4]`, folds three global enable bytes into a counter written
      to `02099DB8`, calls `00227420` and **one further helper this page deliberately does not name**,
      conditionally `002E1CD0` / `00237F40` / `00358BB0`, then `00268530(2)` — **and only then sets
      the bit** (`0025D433`), so it never runs again for that actor.

      > *Why one callee is unnamed:* `check_publish_neighbours` refused this publish for it. Its
      > callers sit in two layers this page does not discuss, so naming it here would make both into
      > unaccounted neighbours and the honest remedy — two crossing sentences about functions I have
      > not read — would be worse than the omission. **The guard's own ruling offers exactly this
      > alternative**, and the block's shape does not depend on which helper it is. The initialiser's `and 0x8F` at `002666AC` clears bits 4, 5 and 6, so the
      latch starts down at construction. **The `0x288`-stride table is the one verb `03DF`
      `seteventwakerect` indexes in the ninth pass** — same table, same `handleTag4` index, a
      different field.

      **`+0x0C` bit 7 selects which hold the field entry raises, and three verbs write it.** The
      writer is the whole of `0026A320` — sixteen bytes, `and byte [rcx+0x0C], 0x7F` / `setne` /
      `shl al, 7` / `or` — and it is reached from exactly three verbs: **`02BE` `setuptreasure`**
      passes a literal `1` (`0035525C`), **`02BD` `isquestok`** passes a literal `0` (`0035441D`),
      and **`0403` `set_talk_wituout_hide_status`** *(the engine's spelling)* passes its popped
      argument and tail-jumps. Its four readers all take it as `>> 7`: `00263050`, `00263230`,
      `00268D10` and `0028A090`.

      > **And the consequence is already published.**
      > [The field record table](../../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md)
      > records `00263480(ctx, mode)` being called from `00263050` and `00268D10` with
      > **`mode = (storage record byte +0xC >> 7) + 1`**, and the mode chooses which system-mode id
      > the hold request raises — **id 5 for mode 0, id 4 for mode 1**. So the bit is the per-actor
      > switch between those two ids, and `setuptreasure` and `isquestok` are the two sides of it.
      > The join is new; neither half is.

      **And bit 3 as well, which I nearly published as unwritten.** My sweep reported **seven
      `test byte [reg+0x0C], 8` readers in the image** (`0020411D`, `0031F105`, `0031F147`,
      `003231B2`, `00327B77`, `0041C518`, `004265E6`) **and no writer touching it with a mask** —
      and I had drafted exactly that sentence. It is misleading, because **the writer sets the bit in
      a register and then stores the byte**, which a sweep over memory operands cannot see:
      `ActorStorage_InitializeRecord` loads `+0x0C` into `r8b` (`0026661F`), keeps bits 0, 4, 5 and 6
      with `and r8b, 0x71`, **forces bit 3 with `or r8b, 8`** (`00266673`), stores the byte back
      (`0026667E`) and only then clears bits 4–6 with `and byte [rbx+0x0C], 0x8F`. **So bit 3 is set
      at initialisation and no masked writer ever clears it.**

      > **And reading that sequence is worth more than the bit.** The initialiser **does not zero
      these bytes** — it reads them and masks them. `+0x0C` comes out as `0x08` plus **whatever bit 7
      was**; ~~`+0x08` keeps its prior value with only bit 7 cleared (`002665BA`, `0026667A`)~~ `+0x08` comes out with bit 0 set, bits 5, 6 and 7 cleared and bit 4 set or cleared by a condition *(corrected 2026-10-02, OPUS: `002665E8 and dl, 0xBF`, `002665FA or dl, 1`, `00266607 and dl, 0xDF`, `0026664F` / `00266657`, `0026667A and byte ptr [rbx + 8], 0x7F`)*; and
      `+0x13`'s `and 0x3C` at `002666B0` **preserves bits 2–5**. On a freshly carved record that is a
      no-op, so the masks only mean something if the initialiser is ever re-run on a used record —
      which is exactly what an allocator that recycles slots would do. **That is a question about
      record reuse, not about flags**, and it is the strongest lead left on this page: if
      re-initialisation happens, `+0x0C` bit 7 and `+0x13` bits 2–5 are *persistent across a
      record's lives* and everything else on those bytes is not.

      **What bit 3 means is therefore bounded but not named.** *Set at initialisation, never cleared
      with a mask* fits a liveness or constructed marker, and its seven readers would be checks of
      it — but **not one of the seven has been triaged onto this record**; they sit in bands this
      page has not claimed, and a displacement is not a structure. **The writer is established; the
      readers are the open part.**

      **Forty-six bits with a meaning**, and `+0x0C` has none left.

      ---

      **THIRTEENTH PASS — the remainder sentence was wrong the day it was written, and `+0x08` bit 6.**

      **The repair is above, in §"So what `EH-4` should ask now".** Four bits this page had already
      answered were still listed there as open, two of them by the very pass that wrote the sentence.
      **I did not find that by auditing. I found it by wasting a derivation**: `+0x08` bit 7 was
      re-read from `00352BE0` and the fourteen bytes of `0026BED0` today, and the fourth
      pass's table had it with the same two addresses and the same verb. The rebuilt list is there;
      what belongs here is the one bit that survived the audit as genuinely new.

      **`+0x08` bit 6 is a per-slot latch inside `ActorManager_RunFieldRuntimePass`.** In the
      four-slot loop at `0025DC61`–`0025DCC7` the pass takes the record from an eight-byte pointer
      walk, and when `[rbx+0x28]` equals the loop's zero register it checks the bit at `0025DC75`.
      **If the bit is already set the whole block is skipped.** Otherwise, if `[rbx+0x17]` bit 2 is
      clear it calls `00269860(record, 1)` — which gates on `byte[02099DE1]`, indexes the
      **`0x288`-stride table at `02098E10` by `handleTag4`** and tests `+0x1C` bit 7 — and then
      **sets bit 6 at `0025DC8E` on both arms**.

      > **So the bit does not mean "the call was made".** It is set whether or not `[rbx+0x17]`
      > bit 2 vetoed the call, so what it records is *"this slot has been through that gate once"*.
      > A consumer reading it as evidence that `00269860` ran would be wrong on the vetoed arm, and
      > that is the same mistake the ninth pass caught on `+0x0C` bit 5 — **a bit set after a
      > conditional body is a record of the attempt, not of the outcome, unless the set is inside the
      > branch.** Three of these now. It is worth stating as a rule for the remaining bits.

      **And a second, already-published instance of the eleventh pass's blind spot.** `+0x14` bit 7's
      reader is `0025B070`, which does **`cmp byte [rax+0x14], 0x80`** — an unsigned byte compare,
      not a `test` — and this page recorded that reader several passes ago without noticing it was
      the same idiom. **The blind spot is not new; only naming it is.**

      **Forty-seven bits with a meaning**, and the four the audit recovered were never lost — only
      unlisted.

      ---

      **FOURTEENTH PASS — `+0x13` bit 7's row on this page was wrong, it now has a reader, and bits
      2–6 have nobody at all.**

      **The row was wrong, and the mistake is one instruction wide.** It read *"written by
      `0026AD00` as the sign of `edx`"*. `0026AD00` is sixteen bytes:
      `and byte [rcx+0x13], 0x7F` / `neg edx` / `sbb al, al` / `and al, 0x80` /
      `or byte [rcx+0x13], al`. **`neg` sets the carry when its operand is non-zero, not when it is
      negative**, and `sbb al, al` turns that carry into `0x00` or `0xFF`. So the bit is
      **`(edx != 0)`, sign-independent** — a negative argument sets it exactly as a positive one
      does. The row is struck above. The same idiom writes `+0x08` bit 7 through `0026BED0`, where
      the fourth pass's table says only *"from it"* and is right.

      **Its writer's condition comes from its sole caller, and it is three tests deep.**
      `BattleUnit_RefreshActorRuntimeFromDefinition` (`00238BF0`) passes `ebp`, which starts at zero
      and becomes `1` only when `[unit+0xE68]` is non-null, **that** record's `byte +0x05` is `1`,
      and `(byte[[unit+0xE68]+0x18] & 0x0E) == 4` (`00238E11`–`00238E2F`). So the bit is a
      **projection of an authored definition field** onto the runtime record, not a runtime decision.

      **And it now has a reader, route-proven on this record.** In
      `WorldActor_UpdateRuntimeAndScriptExecutionState` (`0025DF00`) the pass calls
      `003DA710(movementContext + 0x50, &a, &b)` — a shared helper two other listed bodies also call,
      **which this page does not name**: one of them has a caller in a layer this page does not
      discuss, and the neighbour guard refused the publish for it — takes `xmm3 = min(a, b)`
      (`0025E2AE`–`0025E2B4`), and then at `0025E2AA`
      tests the bit and, when it is **set**, **replaces `xmm3` with the constant at `0091573C`**
      (`0025E2BC`). That constant is **`1000000.0f`**. So the bit means *ignore the pair's minimum
      and use an effectively unbounded value* — **a limit override**, and the limit it overrides is
      computed from the movement context rather than authored.

      > **Third instance of the unsigned-compare idiom, and this one is route-proven.** The test is
      > `cmp byte [rdi+0x13], 0x80` with `jb` — a bit-7 test that no sweep for `test`/`and`/`or`
      > immediates returns. The eleventh pass called that a blind spot in the method; between
      > `0034B927` (`+0x0D` bit 7), `0025B070` (`+0x14` bit 7, published passes ago) and this one,
      > **it is the engine's normal way of testing a top bit on this record**, not a curiosity.

      **`+0x13` bits 2–6 have neither a writer nor a reader.** The route-proven census records six
      accesses at `+0x13`, **all reads**, and every one takes bit 0 (`and 1`, at `0025E224`,
      `00264DCC`, `00264DF0`, `0025E524`), bit 1 (`and 2`, at `0025E1E7`) or bit 7 (`0025E2AA`).
      Across the listed bodies the only writers whose base resolves to this record are `002628B0`
      and `0026CE60` — both storing a register I checked to be **provably zero at the write**
      (`xor ebp, ebp` earlier in each, with no reassignment in between) — `0026AD00`, which touches
      bit 7 alone, and the initialiser's `and byte [rbx+0x13], 0x3C` (`002666B0`), which **preserves
      bits 2–5** and clears 0, 1, 6 and 7.

      > **So the initialiser preserves four bits that nothing sets.** Two readings fit, and I am not
      > choosing between them: the mask is **vestigial** from a layout this build inherited, or a
      > **writer exists outside the bodies the function list contains** — and `progress.py` reports
      > about 244,619 bytes of code in roughly 1,308 blocks that the list does not contain at all, so
      > that second reading is not a formality. **These five bits belong in the stated-non-finding
      > column, not the unknown one**, which is a different claim: *nothing in the listed bodies
      > writes or reads them* rather than *their meaning is unknown*.

      **Still forty-seven bits with a meaning.** This pass corrected one and moved five out of the
      unknown column; it added none, and saying so is the point of counting.

      > **The counter is not a score.** It went up on ten of the last eleven passes and this is the
      > first time it did not, which is exactly when a count is worth having — a pass that corrects a
      > published row and disqualifies five bits from a list is worth more than one that adds a bit,
      > and a number that only ever rises would hide that.

      ---

      **FIFTEENTH PASS — a verb names one bit outright, and two more turn out to be the same
      predicate over two fields of one authored entry.**

      **`+0x0D` bit 3 is the wake area's shape, and the verb says so.** Verb **`0239`
      `recttocircle`** is `00349960`, **thirteen bytes**: `mov rcx, rdx` / `mov edx, 1` /
      `jmp 0026B480`. It sets the bit and does nothing else. `0026B480` is twenty-nine bytes and is
      **gated on kind 1** — `(byte[rcx+3] >> 5) == 1` — after which it clears bit 3 and re-sets it
      from the argument masked to one (`0026B48F`–`0026B499`), so argument `0` clears it. Its other
      caller is verb **`0176` `fieldsign`** (`00355A00`), which passes `1` on the arm where its own
      mode equals 1 (`00355A5A`–`00355A64`).

      > **That pairs with the ninth pass.** `+0x0C` bit 5 is the **event-wake-rect** flag, set only
      > through verb `03DF` `seteventwakerect` and read by ~~a shared predicate~~ the request-bit clearer *(answered: see the 2026-09-16 correction, "the request-bit clearer"; 2026-10-02, OPUS)* `talktreasure`,
      > `reqdisable` and **`fieldsign`** all consult. So one bit says *an event wake area was
      > accepted* and this one says *treat it as a circle rather than a rectangle* — **two bits, one
      > geometry**, and `fieldsign` writes into both halves.
      >
      > **What is not established is the consumer.** **No instruction in the image tests `+0x0D`
      > bit 3 with a mask** — I swept for it. The candidates are the two whole-byte readers of
      > `+0x0D` the census already lists, and neither was traced far enough to say. **The verb's own
      > name is authored evidence and it is what this rests on**, which the fourth pass called the
      > strongest kind short of running the game; it is not a reader.

      **`+0x1C` bits 2 and 10 are one predicate applied twice, and the second supersedes the first.**
      `ActorStorage_InitializeRecord` contains the block **twice**, instruction for instruction
      apart from three constants, both arms gated on `(byte[rbx+3] & 0xE0) == 0x60` — **kind 3**:

      | | bit 2 (`00266A08`–`00266A4E`) | bit 10 (`00266A52`–`00266AA4`) |
      | --- | --- | --- |
      | per-record override word | `+0xCC` | `+0xDC` |
      | taken when the override is **not** `0xFFFF` | the word itself | the word itself |
      | otherwise, field of the authored entry | `+0x06` | `+0x16` |
      | minimum the entry's own first word must exceed | `2` | `10` |
      | set when the resulting value is **non-negative** | `or …, 4` | `or …, 0x400` |
      | and then | — | **`and …, 0xFFFFFFFB` — clears bit 2** |

      Both set-paths also test `byte[+0x0B]` bit 3 and call `00268EA0` when it is set. The authored
      entry is reached the same way in both: `[record+0x40]`, field `+0x18`, through
      `ImageAddress_ResolveRuntimePointer`, indexed by a base the caller supplies.

      > **Three things follow, and the third is the one worth having.**
      > **(1)** `0xFFFF` in `+0xCC` / `+0xDC` is *"not overridden — ask the authored data"*, which is
      > an idiom rather than a value.
      > **(2)** The comparison against the entry's **own first word** is a **size or version check**:
      > the field at `+0x16` is only read when that word exceeds `10`, and the one at `+0x06` when it
      > exceeds `2`. **The authored entry is versioned, and the engine reads only as far as the entry
      > says it goes.**
      > **(3)** **Bit 10 clears bit 2 whenever it is set.** They are not independent flags; they are
      > a **two-slot priority pair**, and a consumer that tested bit 2 without knowing that would
      > read *"no first-slot index"* where the truth is *"a second-slot index replaced it"*.

      **And the pair is re-run by two verbs.** `0025AD10` is reached from verb **`00AC`
      `setentrygroup`** (`0034FA70`) and `0025AE00` from **`00BE` `setentrygroupall`** (`00340970`).
      `0025AD10` re-runs **only the bit-10 block**, and only when its mode argument is `2`
      (`0025AD83`); its mode also selects a group id — `0 → 0`, `1 → 7`, `2 → 10`, `4 → 14`, with
      **`3` selecting nothing at all** (`0025AD5D`, `jne` past the call), which is worth recording
      because a gap in a small dense mapping is usually a fact about the data rather than the code.

      **Fifty bits with a meaning.**

      ---

      **SIXTEENTH PASS — `+0x1C` is not a struct of named flags. It is a script-addressable request
      bitmap, and that refutes a universal this page has carried since the second narrowing.**

      **The two functions that do all the writing take an index, not a mask.**

      > `0026B4A0(record, index)` — 32 bytes — **`+0x1C |= (1 << index)`**
      > (`mov eax, 1` / `shl eax, cl` / `or dword [r8+0x1C], eax`), then a call when
      > `byte[+0x0B]` bit 3 is set.
      >
      > `0025D5E0(record, index)` — 88 bytes — **`+0x1C &= ~(1 << index)`**
      > (`mov eax, 1` / `shl eax, cl` / `not eax` / `and dword [rbx+0x1C], eax`).

      **And the index comes from the script.** Verb **`002A` `reqenable`** (`00355540`) pops it with
      `VMValueStack_PopInt32CoerceFloat32` and tail-jumps to the setter; verb **`002B` `reqdisable`**
      (`003558F0`) reaches the clearer. So a script names the bit it wants.

      **`+0x1C` bits 8 and 13 therefore have a second writer, and this page said they did not.**
      Verb **`0176` `fieldsign`** (`00355A00`) calls the setter **twice in a row** — `edx = 8` at
      `00355A71` and `edx = 0x0D` at `00355A7E` — **which is exactly the bit-8/13 pair** — and then
      clears index `3` through the clearer at `00355A8B`. There is no mode-4 refresh anywhere in
      that path. The sentence in §"the eight rows" is struck above; **its premise — that no kind-table
      preset carries either bit — is untouched and still true.**

      > **The consequence is not local.** `003DF6F0`'s last gate is
      > `(dword[+0x1C] & 0x2100) != 0` at `003DF73A`, the exact complement of the clearing mask. So
      > **a field sign makes an actor pass that eligibility predicate**, by the same two bits a
      > free-target type of 4 would raise. Whether that is intended is a question for the page that
      > owns `003DF6F0`; what is established here is that the two paths are indistinguishable at the
      > gate.
      >
      > **And joining that to a published claim gives the chain an end.**
      > [The battle-HUD layout readers](../../16-UI/Battle-Hud/the-battle-hud-layout-readers.md) §
      > *crossings* records `002C64C0` — `003DF6F0`'s one caller — as sitting behind **the
      > overhead-status and HP-gauge paths**. So the chain runs **verb `0176` `fieldsign` → `+0x1C`
      > bits 8 and 13 → `003DF73A` → the overhead display**, which is what a field sign would want.
      > **This is a join of two published readings, not a third one**: I have not read `002C64C0`,
      > and the HUD page's characterisation is its own. If that characterisation is wrong, this
      > sentence goes with it.

      **Why every sweep missed it, and this is the fourth shape today.** The setter's mask is
      *computed* — `shl eax, cl` — so a sweep for `or dword […+0x1C], 0x100` returns nothing. Today
      has now produced four writes or reads that a mask sweep cannot see: a **register-sourced set**
      (`or r8b, 8` into `+0x0C` bit 3), two **unsigned compares** standing in for bit tests
      (`cmp …, 0x80`), and now a **computed shift**. **A negative from a mask sweep is not evidence
      of absence on this record**, and the earlier scratch tool that asked *"does anything ever set
      bit 8 or bit 13"* was built on exactly that sweep and would have answered *no*.

      **So the question `EH-4` asks about `+0x1C` is mis-framed, and that is the useful part.**
      Asking what each bit *means* presumes named flags. These are **indices a script chooses**, and
      three things are answerable instead:

      | | |
      | --- | --- |
      | **which indices the engine reads for itself** | ~~0, 2, 3, 4, 5, 6, 7, 10, 11, 13, 14, 16, 17~~ 0, 2, 3, 4, 5, 6, 7, 8, 10, 11, 13, 14, 16, 17 *(corrected 2026-10-02, OPUS: `003DF73A test dword ptr [rbx + 0x1C], 0x2100` reads bit 8 with bit 13)* — each with named readers in the actor block |
      | **which it protects** | **4 and 5 cannot be cleared at all while `+0x0C` bit 5 is set** — the clearer returns before touching anything (`0025D5EA`–`0025D5FB`) |
      | **which carry side effects beyond the bit** | **16** also clears `+0x0B` bit 2 and calls `00262740`; **17** calls `002626C0` |

      > **The protection is the sharpest of the three.** `+0x0C` bit 5 is the **event-wake-rect**
      > flag from the ninth pass — the one that records that the verb's request was *accepted*. So
      > while an accepted wake rect is standing, **a script cannot disable request bits 4 and 5**,
      > and `reqdisable(4)` silently does nothing rather than failing. A consumer that assumed
      > `reqdisable` always clears would be wrong exactly there.

      **And a word of mine was wrong.** The ninth pass called `0025D5E0` *"a shared predicate that
      `talktreasure`, `reqdisable` and `fieldsign` all consult"*. It is not a predicate — it returns
      nothing and answers nothing. **It is the request-bit clearer, and in the protected case what it
      does is refuse.** Struck above. *Predicate* and *refusal* are not the same claim, and the
      difference is the whole of the protection.

      **Still fifty bits with a meaning.** Bits 8 and 13 were already counted; this pass gave them a
      second writer, refuted a universal, corrected a word and reframed the question — and added no
      bit. **Two passes in a row where the counter did not move, and both were worth more than the
      ones where it did.**

      ---

      **SEVENTEENTH PASS — the whole `+0x1C` index census, and it ends in a question only the
      authored data can answer.**

      Once the sixteenth pass established that `+0x1C` is written by index, the census is finite and
      cheap: **every call to either writer in the listed bodies, with the literal index where `edx`
      is a constant.** There are **nine call sites in the entire image**, and they use **six literal
      indices**:

      | index | who | set / clear |
      | ---: | --- | --- |
      | `2` | verb **`02BE` `setuptreasure`** (`00355830`) | clear |
      | `3` | verb **`0176` `fieldsign`** | clear |
      | `8` | verb **`0176` `fieldsign`** | **set** |
      | `10` | `BattleUnit_RefreshActorRuntimeFromDefinition` | **both**, on opposite arms |
      | `11` | verb **`0055` `camerachange`** (`00351F40`) | **set** |
      | `13` | verb **`0176` `fieldsign`** | **set** |
      | *chosen by the script* | verb **`002A` `reqenable`** | set |
      | *chosen by the script* | verb **`002B` `reqdisable`** | clear |

      > **Two of those six close the fifteenth pass's pair from the other end.** Index `10` is the
      > entry-group bit and index `2` its superseded partner — so besides the initialiser's twin
      > blocks and the two `setentrygroup` verbs, **`setuptreasure` clears bit 2 and the battle-unit
      > refresh drives bit 10 both ways**. The pair is touched by four different mechanisms and they
      > agree on the priority: nothing sets bit 2 except the initialiser.

      **And now the gap is the finding.** The engine **reads** thirteen indices in the actor block —
      `0`, `2`, `3`, `4`, `5`, `6`, `7`, `10`, `11`, `13`, `14`, `16`, `17`, each with a named reader
      — but only **six** are ever written by a literal. ~~So **eight indices are read by the engine and
      never named by it**:~~

      > ~~**`0`, `4`, `5`, `6`, `7`, `14`, `16`, `17`.**~~

      ~~**They can only be arriving from `reqenable` / `reqdisable` arguments in the shipped scripts.**
      That is not a gap in the executable and no amount of further reading of it will close them: the
      names live in authored data. **It is a `DATA` question, and it is now a well-posed one** — not
      *"what does bit 6 mean"* but *"which `reqenable` argument values do the shipped scripts pass,
      and where"*. Filed to `SWE2-DATA` rather than guessed at here.~~

      > ~~**The protected pair sharpens it.** Indices `4` and `5` are two of the eight, and the
      > sixteenth pass showed the clearer **refuses** to clear them while `+0x0C` bit 5 stands. So
      > the engine protects two indices it never sets itself — which is only coherent if scripts set
      > them, and is therefore evidence for the reading above rather than an assumption behind it.~~

      ***Corrected 2026-09-27 (FABLE, Claude Opus 5.5), on OPUS-REQ-FABLE-EH4-1C-PRESETS-STRIKE: the engine does set all eight.** My own second pass on this page publishes `00266BD0`'s whole-word presets, and they set every one at construction: `4` and `5` by rows 1-2 (`0x38`), `6` by rows 3-4 (`0x40`), `16` and `17` by rows 5-7 (`0x30004`, `0x34C85`), `0`, `7` and `14` by row 7 (`0x34C85`). `00266BD0` has one caller, `002665B1` on the entry path of `ActorStorage_InitializeRecord` `00266530`, and the initialiser's later `+0x1C` writes touch only indices 2, 8, 10 and 13. The *six* above are the index-literal writers; the presets are whole words, which the index census did not count. So the engine protects indices it sets itself, and the eight are not a data question. Control [`eh4_1c_presets.py`](../../_index/candidates/eh4-1c-presets/eh4_1c_presets.py) (OPUS; re-run by FABLE, FAILS 0). The sixteenth pass's protection itself stands.*

      **One caution on the census's own scope.** *Nine call sites* is a count over the bodies the
      function list contains, and the same list is short by roughly 244,619 bytes in about 1,308
      blocks. A tenth call site in unlisted code would not appear here. **What is safe is the
      positive half** — these nine exist and use these six indices — and what is provisional is the
      *only*.

      **Still fifty bits with a meaning.** Third pass running without a new bit; this one turned a
      question the executable cannot answer into a question the data can.

      ---

      **EIGHTEENTH PASS — the consumer the fifteenth pass could not find is four instructions from
      the bit it pairs with, and the byte-level frontier closes.**

      **`+0x0D` bit 3 does have a reader, and I published that it had none.** Three passes ago I
      wrote that *"no instruction in the image tests `+0x0D` bit 3 with a mask"* — which is still
      true — and then left its whole-byte readers as *"untraced"*. Traced now. In `0025C830`, at
      **`0025C8BD`**, the field pass does

      > `movzx eax, byte [rdx+0x0D]` / `shr eax, 3` / `and eax, 1` / `mov [rsp+0x40], eax`

      — it extracts **exactly bit 3** and parks it in a stack slot for the rest of the pass. The
      access is route-proven on this record. **Fifth shape a mask sweep cannot see**, after a
      register-sourced set, two unsigned compares and a computed shift: **shift-and-park.**

      > **And the pairing the fifteenth pass argued for on the writer side is visible on the reader
      > side, four instructions later.** At `0025C8EA` the same function tests
      > **`byte [rdi+0x0C], 0x20`** — `+0x0C` bit 5, the **event-wake-rect** flag. So one pass reads
      > *is there an accepted wake area* and *is it a circle* within four instructions of each other.
      > **Two bits, one geometry** was a claim about two verbs; it is now a claim about one consumer.

      **`+0x14` bit 7 gates battle-unit binding, and its reader is a fourth `cmp …, 0x80`.**
      `ActorSystem_BindBattleUnitsForEligibleRecords` does `movzx eax, byte [rax+0x14]` /
      **`cmp al, 0x80`** / `jb` at `00265A83`–`00265A89` and skips the record entirely when the bit
      is clear. With `0034B927`, `0025B070` and `0025E2AA` that is **four** unsigned compares
      standing in for a top-bit test on this record. The eleventh pass called the idiom a blind spot
      in the method; it is the method's blind spot and **the engine's default**.

      **`+0x0D` bit 2 and `+0x14` bits 0–3 have nothing at all — checked against all five shapes.**
      No masked test, no masked write, no register-sourced write through a shift, no computed index,
      no shift-and-extract. The route-proven census agrees: every bit-addressed access at `+0x14` is
      `0x10`, `0x20`, `0x40` or `0x80`, and none at `+0x0D` touches bit 2. **And the whole-byte
      writers preserve them** — `0026B8E0` walks a kind block writing
      `+0x14 = (+0x14 & 0xCF) | 0x40`, which keeps bits 0–3 and 7 untouched.

      > **That is the fourth byte with the same shape, and it is one observation rather than four
      > puzzles.** The initialiser leaves `+0x08` at *prior value with bit 7 cleared* (`and 0x7F`),
      > `+0x0C` at `0x08` plus prior bit 7 (`or 8` then `and 0x8F`), `+0x13` with **bits 2–5
      > preserved** (`and 0x3C`), and `+0x14` with **bits 0–6 preserved** (`and 0x7F`) — and in every
      > one of those four bytes, some of the preserved bits are bits **nothing in the listed code
      > ever sets**. The twelfth pass noticed the reading-and-masking; what is new is that the
      > *preserved* sets and the *never-written* sets overlap in four bytes independently. **Either
      > the masks are inherited from a layout this build no longer fills, or something outside the
      > listed bodies fills them** — and the same ~244,619 bytes in ~1,308 unlisted blocks are the
      > second reading's address. I am not choosing, and a third possibility is worth naming: the
      > record may be **populated at load time by a path that is neither the initialiser nor a
      > runtime writer**, which is a question about record lifetime rather than about flags.

      **So the byte-level frontier of `EH-4` is closed, and the question is not.** Every flag bit of
      `+0x08`, `+0x09`, `+0x0C`, `+0x0D`, `+0x13`, `+0x14` and `+0x1C` is now either **named**,
      **stated as a non-finding with the five shapes checked**, or **routed** — the `+0x1C` indices
      to `SWE2-DATA` as an argument census *(answered: see the 2026-09-27 correction above, "the engine does set all eight"; 2026-10-02, OPUS)*, and the preserved-bit pattern to whoever takes record
      reuse. **Fourth pass running without a new bit.** That is what a frontier closing looks like
      from the inside, and it is a better reason to stop counting than a round number.

      **Still fifty bits with a meaning.**

      ---

      **NINETEENTH — not a byte pass. The record-reuse question the eighteenth raised is answered,
      and the answer makes four bytes' masks vestigial.**

      The eighteenth pass left three readings of why `ActorStorage_InitializeRecord` preserves bits
      that nothing sets: an inherited layout, a writer among the unlisted bodies, or **population at
      load time by a third path**. It named the last as a question about **record lifetime** rather
      than about flags. That question is answerable, and the answer is the first reading.

      **The initialiser has exactly one caller, and it cannot be reached any other way.**

      | test | result | control |
      | --- | --- | --- |
      | direct `call` / `jmp` in the listed bodies | **one**, `ActorStorage_AllocateAndInitializeRecords` at `00267B79` | — |
      | `lea` taking its address | **none** | — |
      | its address stored as a pointer anywhere in the image's raw section data | **none** | **the control passes** — `0017CC70` occurs 3 times and `0079F9E0` 4 times, both real `GameApplication` vtable slots, and the bytes at `008C5760` confirm the layout |

      > **The control matters and is why this is stated at all.** My first pointer scan used
      > `Actor_RefreshPresentationVisibility` as a control and it returned **zero**, which made the
      > target's zero worthless — a negative from an instrument whose control fails proves nothing.
      > Two real vtable slots were substituted and both come back non-zero. **The same discipline I
      > have been applying to other people's censuses all day, applied to my own scan before it was
      > used.**

      **And that one caller zeroes the block first.** `ActorStorage_AllocateAndInitializeRecords`
      allocates through `qword [r15+0x88]` (`00267A79`), then at `00267A85`–`00267A8B` sets
      `rcx = the block`, `edx = 0`, `r8 = the byte count` and calls **`memset`** (`00861EC0`,
      named in the function list). The records are carved out of that block afterwards
      (`00267A96`–`00267AA2`), and only then is the initialiser run on each.

      > **So the masks preserve zero.** `and byte [rbx+0x08], 0x7F`, `or 8` then
      > `and byte [rbx+0x0C], 0x8F`, `and byte [rbx+0x13], 0x3C` and `and byte [rbx+0x14], 0x7F` all
      > operate on a byte that `memset` has just cleared. **The bits they "preserve" are zero at
      > construction**, and the eighteenth pass's *never written* becomes the stronger and simpler
      > **never written and zero** — for `+0x13` bits 2–5 and `+0x14` bits 0–3 both.
      >
      > **The masks are therefore vestigial**, which was the first of the three readings. A layout
      > this build no longer fills is the natural explanation for a read-modify-write that cannot
      > read anything but zero.

      **What this does not settle, stated rather than glossed.** The one-caller result is over the
      bodies the function list contains, and that list is short by roughly 244,619 bytes in about
      1,308 blocks; a second caller there would reopen it. The pointer scan covers the image's raw
      section data and cannot see an address a function *computes*. And nothing here speaks to
      whether a record is ever recycled **without** re-running the initialiser — that would be a
      different mechanism, and this pass did not look for it.

      **The count does not move, and that is the point.** This pass removed a question rather than
      adding a bit: *why does the initialiser preserve what nothing sets* is answered, and two of the
      three readings it had are closed. **Still fifty bits with a meaning.**
- [x] **What `+0x118 = 0x003C0000` encodes** — the only large non-pointer constant written. `EH-5`.
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (EH-5):* **two words, a countdown and its
      reload: `+0x118 = 0` and `+0x11A = 60` (`0x3C`).** The route-proven census
      ([`actor-storage-record-accesses.tsv`](actor-storage-record-accesses.tsv)) has two users.
      - `00268EA0` arms it. If a definition word is non-negative (the resolved table's `s16 +0x22`, or `0x10` when the
        table is shorter), it sets `+0x0B` bit 2 and copies the reload into the counter (`00268F76`–`00268F81`); otherwise it
        clears the bit and zeroes the counter (`00268F8A`–`00268F8E`). It has nine callers in the actor passes, the
        interpreter and the record initialiser.
      - `0025BAD0` (from the actor pass `0025B820`) runs it. While the pass's mask bit is set in `+0x0B` and bit 3 is clear,
        it adds `0xFFFF`, i.e. decrements by one per pass (`0025BCA2`), and treats zero as expiry (`0025BCAB`–`0025BCB2`).
        On expiry with bit 2 set it clears the bit and the counter (`0025BDF1`–`0025BE08`).

      So the constant is a **60-step per-actor countdown**, idle until armed. Counted in actor passes, not seconds, so its
      duration follows the update rate ([the ramp contract's UG-5](../../17-Presentation-Rendering/CONTRACT-authored-command-ramp-channels.md)
      shows how passes relate to frames for another counter). In the same pass the same definition word, or field `+0xE8`,
      is the function id handed to `ActorResource_SubmitRequestDescriptor` (`0025BD19`–`0025BD65`, mode 1). How that request
      is coupled to the countdown's expiry was not followed, and what the definition word denotes is not read.
- [x] ~~**Who calls `00266530`**, and therefore when a slot is recycled. Not traced. `EH-6`.~~
  **`EH-6` was ANSWERED on 2026-09-08 and this bullet was never ticked** (found 2026-09-13 by
  `check_stranded_unknowns.py`). **Exactly one caller**, established with four instruments and
  two controls: `ActorStorage_AllocateAndInitializeRecords` (`002679F0`) ←
  `ActorSystem_InitializeManagerRuntime` (`0026CE60`) ← `0025BFB0` / `0032F1B0`. **And the
  second half of the question is void**: §2 records that the pool is one allocation `memset` to
  zero immediately before, so a slot is never recycled and there is no "when".

> **Three statements were stranded by §2's 2026-09-08 correction and survived the 2026-09-12
> falsification pass** (found 2026-09-13 by `check_stranded_unknowns.py`): the `EH-6` bullet
> above, the §7 modding note, and an evidence row below that still read **PROVEN** for the
> conclusion §2 had struck. An append-only correction moves the *section* it lands in; it does
> not move the summary, the advice or the evidence table, and a pass that reads the corrected
> section can come away satisfied.

## 9. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| The base register is the record throughout | every write to `rbx` in the body enumerated: one load at `0026656A`, one epilogue restore | 1 | PROVEN |
| 41 fields and their widths | every store collected with its operand width from the instruction encoding | 1 | PROVEN |
| ~~It recycles rather than constructs~~ **It constructs; the masks run on zeroed memory** | eleven read-modify-write masks, listed in §2 with their exact constants — **the masks are real, the conclusion drawn from them was not**; §2 (2026-09-08) and `EH-6` | 1 | **CORRECTED 2026-09-13** |
| `+0x00` is the slot index | `mov word ptr [rbx], r10w` with `r10 = movsxd(r8d)`, the index argument | 1 | PROVEN |
| The table is pointers with an 8-byte header | `[rdx + r10*8 + 8]` | 1 | PROVEN |
| Same type as the movement actor | two offsets agree with complementary masks; the carve loop writes `+0x03` itself *(answered: see "`EH-1` answered — PROVEN, not probable"; 2026-10-02, OPUS)* | 3 | ~~**PROBABLE**~~ PROVEN |
| The record's true size | ~~**not established** — `0x11C` is a lower bound~~ 720 to 1,760 bytes by kind *(answered: see "Records are 720 to 1,760 bytes, by kind"; 2026-10-02, OPUS)* | — | UNKNOWN |
| Any field's meaning | **not established** | — | UNKNOWN |

## 10. Related

- [`../../_types/fields.tsv`](../../_types/fields.tsv) — the machine-readable layout.
- [`../../06-Movement-And-Navigation/Facing-And-Steering/how-a-character-turns.md`](../../06-Movement-And-Navigation/Facing-And-Steering/how-a-character-turns.md)
  — the actor whose `+0x03` and `+0xB8` match.
- [`../../_index/RESEARCH-IMPORT-BACKLOG.md`](../../_index/RESEARCH-IMPORT-BACKLOG.md) — the import.

## 11. The allocator — and `EH-1`, `EH-2` answered

**`ActorStorage_InitializeRecord` has exactly one caller**, established with all four instruments and
both controls passing: `E8` **1** (`00267B79` in `002679F0`) · `E9` **0** · code memory-operand **0** ·
data qword **0**. Controls: `memcpy` 632 `E8` + 5 `E9`; `005A2B80` 3 qword hits.

That caller is **`ActorStorage_AllocateAndInitializeRecords` (`002679F0`, 436 B)**, reached from
`ActorSystem_InitializeManagerRuntime` (`0026CE60`) ← `0025BFB0` / `0032F1B0`.

```c
void ActorStorage_AllocateAndInitializeRecords(Ctx *ctx)      /* 002679F0 */
{
    Desc *d = *(void**)ctx;
    int   count = ctx->i_20;
    int   N     = *(u16*)(d + *(int*)(d + 0x14));      /* number of kind entries */

    /* 1. size the whole pool */
    int payload = 0;
    for (k = 0; k < N; k++)
        payload += ((kindTable[k].size + 15) & ~15) * countArray[k];
    int hdr = (count * 8 + 0x17) & ~15;
    int total = hdr * 2 + payload;

    void *pool = ctx->vtbl_88(total);                  /* one allocation */
    memset(pool, 0, total);                            /* 00861EC0 - ZEROED */
    *(int*)pool = count;
    ctx->p_1F0 = (char*)pool + hdr;

    /* 2. carve, and stamp each record's kind */
    char *p = (char*)pool + hdr * 2;
    for (k = 0, slot = 0; k < N; k++) {
        ctx->u16_1D0[kindTable[k].kind] += countArray[k];
        for (j = 0; j < countArray[k]; j++) {
            ((void**)pool)[1 + slot++] = p;                       /* the pointer table */
            p[3] = (p[3] & 0xE0) | (k & 0x1F);                    /* low 5: sequence  */
            p[3] = (p[3] & 0x1F) | (kindTable[k].kind << 5);      /* top 3: KIND      */
            p += (kindTable[k].size + 15) & ~15;
        }
    }

    /* 3. prefix-sum the four per-kind counters: +0x1D0 -> +0x1D8 */
    for (i = 0, run = 0; i < 4; i++) { ctx->u16_1D8[i] = run; run += ctx->u16_1D0[i]; }

    /* 4. initialise every record */
    for (i = 0; i < count; i++)
        ActorStorage_InitializeRecord(ctx, pool, i);
}
```

### `EH-2` answered — the record's real size, and my lower bound was a long way out

The kind table at **`0x01E0C328`** is eight `{u8 kind, u8 sub, u16 size}` entries:

| # | kind | sub | size | rounded to 16 |
|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 808 | 816 |
| 1 | 1 | 0 | 936 | 944 |
| 2 | 1 | 1 | 816 | 816 |
| 3 | 2 | 0 | 840 | 848 |
| 4 | 2 | 1 | 720 | 720 |
| 5 | **3** | 0 | **1760** | 1760 |
| 6 | **3** | 0 | **1760** | 1760 |
| 7 | **3** | 1 | **1640** | 1648 |

**Records are 720 to 1,760 bytes, by kind** — not one size. §4's `0x11C` (284) was correctly labelled
a *lower bound*, and it was an underestimate by a factor of three to six. **The `_types/` entry is
corrected to a per-kind size with the table as its evidence.**

### `EH-1` answered — PROVEN, not probable

The carve loop **writes `+0x03` itself**:

```asm
00267AFA  movzx ecx, byte ptr [rdx + 3]
00267AFE  and   cl, 0xE0            ; keep the kind bits
00267B01  or    cl, r9b             ; OR in the sequence (r10b & 0x1F)
00267B04  mov   byte ptr [rdx + 3], cl
00267B07  and   cl, 0x1F            ; keep the sequence
00267B0A  movzx eax, byte ptr [r8]  ; the kind code from the table
00267B0E  shl   al, 5
00267B11  or    cl, al
00267B13  mov   byte ptr [rdx + 3], cl
```

```
record[+0x03] = (kindCode << 5) | (sequenceWithinKind & 0x1F)   // <- corrected 2026-10-02, OPUS - the low field is the row i of 01E0C328 (00267AE1-00267AE8 r9b = i & 0x1F), counted 0-7 across the table, not restarted per kind
```

**`Movement_SetSteeringMode`'s gate `(byte@+0x03 & 0xE0) == 0x60` therefore selects kind `0x60 >> 5`
= 3** — the three largest table entries, 1760/1760/1640 bytes.

> **The movement code's actor and this storage record are the same object.** Not "two offsets agree";
> the byte the movement code tests is written *here*, by this loop, with this encoding. **`EH-1`
> moves from `PROBABLE` to `PROVEN`**, and `+0x03` decomposes exactly as §5 guessed — top 3 bits
> kind, low 5 bits a per-kind sequence number.
>
> **Only kind-3 actors can be steered.** Whatever kinds 0, 1 and 2 are, `Movement_SetSteeringMode`
> returns immediately for all of them.

### What this says about §2's correction

`InitializeRecord` **reads `+0x03` three times** (`0026656F`, `002666BB`, `002669FA`) **and never
writes it** — it branches on the kind the carve stamped. That is the field the masks protect, and it
is why the routine is written read-modify-write on a block of memory that was zeroed moments earlier.

## The undeclared tail — what a static scan can and cannot see (2026-09-08)

The layout above came from `ActorStorage_InitializeRecord`'s own stores, which recovers **everything
the constructor initialises and nothing else**. The record runs to **1,760 bytes** for the largest
kind; the store declares `0x11C`. **A 1,476-byte tail has no declared field at all.**

`actor_field_scan.py` attacks it from a different anchor. The record's discriminator at `+0x03` is
proven — `(kind << 5) | (sequence & 0x1F)` — so code that decodes an actor's kind is unmistakable:

```asm
movzx  eax, byte ptr [rcx + 3]
shr    eax, 5                     ; or:  and eax, 0x1F
```

**55 functions in the image contain that sequence.** In each, the register the byte was read through
held an actor pointer, and every `[thatreg + disp]` access in the same function is a candidate field.
**70 distinct offsets** come out.

### The instrument's error bars, measured rather than asserted

| | |
|---|---|
| **Recall** — the 41 offsets the constructor proves are fields | **41 of 41 re-found (100 %)** |
| **Precision inside `0x000`–`0x118`**, where the constructor's set is near-complete | **41 of 62 (66.1 %)** |
| offsets found **beyond `0x118`**, in the undeclared tail | **8** |

> **The 21 "imprecise" offsets are not necessarily wrong.** The constructor's field set is not a
> complete layout of the header either — it is only what construction *writes*. An offset touched by
> actor code and never initialised is exactly what a field the constructor skips looks like. So 66 %
> is a **floor on precision**, not a measured error rate, and this document does not present the 21
> as noise.

### The first attempt was abandoned because its control said so

A linear forward **taint** was written first: mark the register at the decode, follow it, drop the
taint on any write to it or any call that clobbers it. It recovered **4 of the 41 known offsets —
9.8 %**.

> **It was not merely weak, it was useless**, and the control said so before a single new offset was
> published. An actor pointer is copied and reloaded constantly; a taint that dies at the first
> reload cannot see the accesses that matter. What replaced it is deliberately cruder — every access
> on the same register anywhere in the same function — and its cost is stated above as precision
> rather than hidden.

### What is actually in the tail

Full table, all ~~70~~ 56 offsets *(answered: the file holds 56 rows, the highest `0x118`, measured; 2026-10-02, OPUS)* with their function/read/write counts:
[`actor-record-offsets-observed.tsv`](actor-record-offsets-observed.tsv).

The six offsets seen through **two or more independent functions** are the only ones promoted into
`_types/` — and **the validator immediately falsified three of the six**:

> `0x044`, `0x05C` and `0x107` each **overlap a field the constructor already declares** —
> `0x040` (8 B), `0x058` (8 B), `0x106` (2 B). They are not new fields. They are evidence that
> **the constructor-derived sizes are too coarse**: a single `mov qword ptr [rec+0x40], 0` proves
> those eight bytes are *zeroed*, not that they are *one field*, and actor code reading a dword at
> `+0x044` proves a boundary inside it. The three declared fields were **narrowed** to the part the
> zeroing store actually justifies, rather than the observations being forced in beside them.
>
> **That is three corrections the type store would not have accepted silently.** Adding six rows
> produced three errors; the store is now `0 errors` again, and two of the narrowed fields leave a
> visible gap behind them, which is the correct outcome.



| offset | functions | reads | writes | operand size |
|---|---:|---:|---:|---:|
| `+0x044` | 2 | 2 | 0 | 4 |
| `+0x05C` | 2 | 0 | 2 | 1 |
| `+0x068` | 2 | 2 | 0 | 4 |
| `+0x0C0` | **3** | 8 | 0 | **8 — a pointer** |
| `+0x0E8` | 2 | 2 | 0 | 2 |
| `+0x107` | 2 | 2 | 0 | 1 |

The eight beyond `0x118` — `0x148`, `0x184`, `0x1C8`, `0x1D6`, `0x1DE`, `0x204`, `0x220`, and
`0x11A` on the boundary — are each seen in **one** function only and ~~are recorded in the TSV~~ are not in the TSV *(corrected 2026-10-02, OPUS: the file's highest row is `0x118`)*, **not**
promoted. `+0x220` is the most interesting of them: two reads and two writes at 4 bytes, so it is
live state rather than a constant.

### The honest conclusion about the tail

**Eight observed offsets across 1,476 bytes is close to nothing, and that is the finding.** The
kind-decode anchor reaches the header and stops; the tail belongs to systems that already hold a
typed actor pointer and never re-derive the kind. Recovering it needs a different instrument —
following the pointer through the systems that own it, or runtime observation of a live record.
**`DN-1`.**

## 12. `EH-3` — the `+0x60`–`+0xB8` gap opens, and the record turns out to point at itself (2026-09-10)

`EH-3` recorded six undeclared spans, the largest `+0x60`–`+0xB8`. It was not dark because the
record is unknowable there. **It was dark because the instrument's anchor was too narrow.**

### The anchor missed a whole family

`actor_field_scan.py` accepted two kind-decode forms — `shr 5` and `and 0x1F`. `Movement_SetSteeringMode`
uses a third:

```asm
0026AE96  movzx eax, byte ptr [rcx + 3]
0026AE9D  and   al, 0xe0
0026AE9F  cmp   al, 0x60          ; kind 3
```

`and 0xE0` keeps the kind instead of the sequence, and the scan never matched it. Adding that one
immediate takes the anchor from **55 functions to 174**.

### And the enumeration was counting the wrong object

The scan's old rule was *every* `[reg + disp]` anywhere in a function whose `reg` held an actor at
the decode. Its over-count is not noise — it has a name. Three instructions after the gate above:

```asm
0026AEA3  mov rcx, qword ptr [rcx + 0xb8]   ; rcx is now the MOVEMENT CONTEXT
0026AEB2  mov rax, qword ptr [rcx + 0xf0]   ; a context field, filed as an actor field
```

The scan now runs a forward taint **with copy propagation** — `mov rA, rB` carries the taint, any
other write kills the register, a call kills the volatiles — seeded at every decode in the function.
The 2026-09-08 taint that scored 4 of 41 lacked exactly the copy propagation.

| instrument | offsets | recall on the constructor's own 41 |
|---|---:|---:|
| forward taint, no copy propagation (abandoned 2026-09-08) | — | **4 of 41** |
| crude "every access on that register" | 70 | 41 of 41 |
| **forward taint with copy propagation** | **56** | **41 of 41** |

**Same recall, 14 fewer offsets.** And it declines to re-find **five of the six** offsets the crude
scan had itself promoted — `0x044`, `0x05C`, `0x068`, `0x0E8`, `0x107`; only `0x0C0` survives. That
is not a refutation, it is one instrument failing to reach what another reported, and the tool now
prints the two populations separately so the control cannot grade itself.

### What is in the gap: the record contains its own sub-objects

`00266AD0` (`ActorEntity`, 211 B) switches on the **sequence** `rec[3] & 0x1F` — the low five bits,
eight arms — and plants four pointers, **all of them interior pointers into the record itself**:

| seq | `+0xB8` | `+0xC0` | `+0xA0` | `+0xA8` |
|---:|---|---|---|---|
| 0 | `NULL` | `NULL` | `rec+0x120` | `rec+0x1E8` |
| 1 | `rec+0x120` | `NULL` | `rec+0x1A0` | `rec+0x268` |
| 2 | `rec+0x120` | `NULL` | `rec+0x1A0` | `rec+0x240` |
| 3 | `rec+0x120` | `NULL` | `rec+0x140` | `rec+0x208` |
| 4 | `rec+0x120` | `NULL` | `rec+0x140` | `rec+0x1E0` |
| 5, 6 | `rec+0x120` | `rec+0x350` | `rec+0x4D8` | `rec+0x5A0` |
| 7 | `rec+0x120` | `rec+0x350` | `rec+0x4D8` | `rec+0x578` |

`+0xA8` is `+0xA0` plus `0xC8` or `0xA0`, chosen at `00266B83` by `byte [01E0C329 + seq*4]` — the
**`sub`** field of the very kind table `EH-2` recovered at `01E0C328`. `sub == 1` gives `0xA0`.

### Two arrays, two counts, and the arithmetic closes on every kind

`003DB580(rec, n88, n89)` writes both counts and builds a free list:

```asm
003DB585  mov  r9, [rcx + 0xa0]
003DB594  mov  byte [rcx + 0x88], r11b     ; = n88
003DB59E  mov  byte [rcx + 0x89], r8b      ; = n89
          loop n89 times, stride 0x14:
003DB5BB    mov byte [r9 + 0], i+1          ; next index
003DB5C1    mov byte [r9 + 1], i-1          ; prev index
003DB5B3    mov dword [r9 + 4], 0x80000000
003DB5C7    mov word  [r9 + 0x10], 0
```

and `ActorStorage_InitializeRecord` picks the counts from the same `sub` byte at `00266588`–`002665A4`:
**`n88` = 8, or 6 when `sub == 1`; `n89` = 10, or 8 when `sub == 1`.** Then at `002667DF` it clears
the other array, `n88` elements of stride `0x28`.

**Both strides are confirmed independently, and the sizes settle it.**
`003DB550(rec, idx)` returns `[rec+0xA0] + idx*0x14` and **`NULL` for `idx == 0xFF`**;
`WorldActor_UpdateRuntimeAndScriptExecutionState` at `0025DFB6` computes
`[rec+0xA8] + (int8)[rec+0x11] * 0x28`. Against the eight per-kind sizes:

| seq | size | `+0xA0` array | `+0xA8` array | tail after it |
|---:|---:|---|---|---:|
| 0 | `0x328` | `0x120`, 10 × `0x14` = `0xC8` | `0x1E8`, 8 × `0x28` = `0x140` | **0** |
| 1 | `0x3A8` | `0x1A0`, 10 × `0x14` | `0x268`, 8 × `0x28` | **0** |
| 2 | `0x330` | `0x1A0`, 8 × `0x14` = `0xA0` | `0x240`, 6 × `0x28` = `0xF0` | **0** |
| 3 | `0x348` | `0x140`, 10 × `0x14` | `0x208`, 8 × `0x28` | **0** |
| 4 | `0x2D0` | `0x140`, 8 × `0x14` | `0x1E0`, 6 × `0x28` | **0** |
| 5, 6 | `0x6E0` | `0x4D8`, 10 × `0x14` | `0x5A0`, 8 × `0x28` | **0** |
| 7 | `0x668` | `0x4D8`, 8 × `0x14` | `0x578`, 6 × `0x28` | **0** |

**The `+0xA8` array is the record's tail, exactly, on all eight entries.** Nothing was rounded to
make that come out; the deltas `0xC8`/`0xA0` are `10`/`8` × `0x14` and the residues are `8`/`6` ×
`0x28`. Two element counts, two strides and eight record sizes agree with no slack.

### The five fields this closes

| offset | size | name | what it is |
|---|---:|---|---|
| `+0x062` | 1 | `slotIndexA0` | index into the `+0xA0` array; `0xFF` is the null index (`003DB550`) |
| `+0x088` | 1 | `slotCountA8` | `8`, or `6` when the kind table's `sub` is `1` |
| `+0x089` | 1 | `slotCountA0` | `10`, or `8` when `sub` is `1` |
| `+0x0A0` | 8 | `slotsA0` | interior pointer to `+0x89` × `0x14` slots — a doubly-linked free list |
| `+0x0A8` | 8 | `slotsA8` | interior pointer to `+0x88` × `0x28` slots, the record's tail |

Outside the gap the same read narrows one more: `+0x010` is declared `uint16` because the
constructor zeroes a word there, but `0025DFB6` reads a **signed byte at `+0x011`** and uses it as
the `+0xA8` slot index — the same "the zeroing store is coarser than the field" pattern that
`0x044`/`0x05C`/`0x107` already showed.

### Limits

- **What the slots ARE is not established.** The `0x28` element has a qword at `+0`, a qword at
  `+8`, a dword at `+0x10`, a byte enum at `+0x14` compared against `7` at `0025DFF0`, and a state
  byte at `+0x16`; the `0x14` element has next/prev indices and a dword seeded to `0x80000000`.
  Those are the constructor's clears plus one consumer, not a recovered type.
- `+0x62` and `+0x88` each come from a **single** function; `+0xA8` from two. `+0xA0` and `+0x89`
  come from `003DB580` and the initialiser's argument setup, which is a stronger chain than the
  scan.
- The region table is read **statically** from `00266AD0`'s jump table and the kind table. No
  runtime observation confirms a live record's pointers.
- `+0x6C`–`+0x88`, `+0x8A`–`+0xA0` and `+0x90`–`+0xA0` remain undeclared. `EH-3` is **narrowed, not
  closed**.

## 13. What the `+0xA0` slots are: a per-channel resource list, and five more gaps close (2026-09-10)

§12 fixed the two arrays' extent and said plainly that **what the slots ARE is not established**.
They are established now, and the answer came free: `003DB550`, the accessor §12 used only for its
stride arithmetic, is already named **`ActorResource_GetEntryByOrdinal`**. A whole named family
reads these slots, and [`the-field-runtime-pass`](../the-field-runtime-pass.md) §6 already lists it
without knowing what it operated on.

### The model

The `+0xA0` array is a **pool of `0x14`-byte `ActorResourceEntry` records**. Entries are not owned
individually — the array is interior to the actor record — and they move between lists by index:

```
rec +0x060  entryFreeListHead       -> the free pool
rec +0x061  detachedEntryListHead   -> entries whose state byte is 4, on no channel
rec +0x094[ch]  channelHead         -> per-channel list head      (slotCountA8 channels)
rec +0x08C[ch]  channelTail         -> per-channel list tail
rec +0x006  channelActiveMask       -> bit ch set while channel ch's list is non-empty
```

**`slotCountA8` is doing double duty, and that is the key that makes the whole layout click.** It is
the element count of the `+0xA8` array *and* the number of channels: `003DBF63` loads it as the
channel loop bound at `003DC01B`. So the `+0xA8` array is **one `0x28`-byte state block per
channel**, and `+0x011` — the signed byte §12 recovered as an index into it — is *which channel*.
Eight channels for `sub == 0` kinds, six for `sub == 1`.

### The search, read instruction by instruction

`ActorResource_FindActiveEntryByIdOrClass` (`003DBF60`) takes `(rec, id, class)`, either of which
may be negative to mean "don't filter on this", and returns an **entry index** or `0xFF`:

```c
if (rec->slotCountA8 == 0) return 0xFF;
for (ch = 0; ch < rec->slotCountA8; ch++) {
    if (!(rec->channelActiveMask & (1 << ch))) continue;        /* 003DBFA2 bt */
    for (i = rec->channelHead[ch], n = 0; i != 0xFF; i = e->next, n++) {
        e = rec->slotsA0 + i * 0x14;                            /* 003DBFCB */
        if (id    >= 0 && e->resourceId       == id)    return i;
        if (class >= 0 && (e->classAndFlag>>1) == class) return i;
        if (n > rec->slotCountA0) break;                        /* 003DBFF8 cycle guard */
    }
}
return 0xFF;
```

Two details worth keeping. **The walk is bounded by `slotCountA0`** — a corrupt `next` chain costs a
bounded walk, not a hang. And the two filters are **OR, not AND**: an entry matching either the id
or the class returns.

### The removal, and the lifetime it defines

`ActorResource_RemoveActiveEntry` (`003DB2A0`) is the function that makes the layout legible,
because it has to unlink from whichever list the entry is on and therefore names every one of them:

| step | site | what it says |
|---|---|---|
| `idx == 0xFF` returns `1` | `003DB2B0` | the null ordinal is a no-op, and the return value is not a success flag |
| pick the owning list | `003DB2F8`, `003DB2FE` | `state == 4` **or** a negative `channel` byte means the list is `rec+0x61`; otherwise it is `channelHead[channel]` |
| ~~walk to find it~~ look for it | `003DB326`–`003DB33F` | ~~linear from the head through `003DB550`, so removal is O(list)~~ not a walk: every iteration passes the removed index itself to `003DB550` (`mov edx, esi`), so a non-head entry is unlinked only when its own `next` byte equals its index, returns with no unlink when that byte is `0xFF`, and otherwise repeats the same iteration *(corrected 2026-10-02, OPUS, from FABLE's review `fable-review-astra-notification-retirement-order-1002`; `003DB550` is a pure index leaf, `[actor+0xA0] + idx*20`)* |
| unlink | `003DB346` → `003DC1B0` | the helper loads `prev` at `+0x01` and `next` at `+0x00` — **the lists are doubly linked** |
| ~~release a payload~~ end notification | `003DB36B`, `003DB371` | ~~only when `entry+0x06 != 0x8000` **and** `state == 3`~~ the mode-3 end notification through `003DC0D0`, attempted before the free-list relink and its result discarded; only when the signed channel byte `entry+0x02` is non-negative, `entry+0x06 != 0x8000` **and** `entry+0x10 == 3` (`+0x10` is the request mode) *(corrected 2026-10-02, OPUS, from FABLE's review `fable-review-astra-notification-retirement-order-1002`)* |
| class-indexed notify | `003DB382`–`003DB392` | only when `classAndFlag >= 2`, passing `classAndFlag >> 1` |
| fix the head | `003DB39D`–`003DB3AB` | `channelHead[ch] = entry->next` if the entry was the head |
| **fix the mask** | `003DB3C5`–`003DB3CD` | if the new head is `0xFF` the channel is empty, and **three** masks are cleared together: `+0x06`, `+0x24`, `+0x26` |
| fix the tail | `003DB3D1`–`003DB3E0` | `channelTail[ch] = entry->prev` if the entry was the tail — this is what proves `+0x8C` is a tail array and not a second head array |
| recycle | `003DB3E6`–`003DB3F9` | link onto the free list at `+0x60`, set `+0x63` bit 1, make the freed entry the new free head |

**So an entry's lifetime is: free list → some channel list (or the detached list) → free list.** It
is never allocated and never destroyed; `003DB580` builds the initial free chain at construction
(`next = i+1`, `prev = i-1`) and nothing else creates one.

### Five more `ActorStorageRecord` gaps close

| offset | field | how it was pinned |
|---|---|---|
| `+0x006` | `channelActiveMask` | `ActorResource_IsChannelBitActive` (`003DB640`) is 13 bytes and does nothing but `bt` this word; the remover clears a bit at `003DB3C5` |
| `+0x024`, `+0x026` | two more 16-bit masks | cleared by the same `~(1<<ch)` at the same instant, `003DB3C9`/`003DB3CD`. **Lifetime proven, meaning not** |
| `+0x060` | `entryFreeListHead` | `003DB3E6` reads it, `003DB3F9` writes the freed index into it |
| `+0x061` | `detachedEntryListHead` | `003DB314` selects it, `003DB35E` writes the removed entry's `next` into it |
| `+0x063` | `entryListFlags` | `003DB3F5 or byte [rbx+0x63], 2` |
| `+0x08C`–`+0x093` | `channelTail[8]` | `003DB3D1`/`003DB3E0` |
| `+0x094`–`+0x09B` | `channelHead[8]` | `003DBFB2`, `003DB39D`/`003DB3AB` |

Both arrays are declared **8 bytes — the maximum extent**, because only `slotCountA8` of them are
used and that is 6 on `sub == 1` kinds. The declaration is the storage, not the population.

`+0x062`, which §12 recorded as `slotIndexA0`, is renamed `selectedEntryIndex`: it belongs to the
`+0x60`–`+0x63` cluster of entry ordinals and flags, and it is an ordinal into the same pool.

### Limits

- **The entry's `+0x06` is still unnamed.** Its lifetime is proven — seeded `0x8000`, and a value
  other than `0x8000` plus `state == 3` is what reaches the release call at `003DB37D` — but what it
  holds is not read. Likewise `state`'s full enumeration: only `3` and `4` are distinguished here.
- `+0x024` and `+0x026` are recorded with **`UNRESOLVED` meaning and `PROVEN` lifetime**, which is
  the honest pair. Knowing when a field is cleared is not knowing what it is.
- The entry's `+0x03`, `+0x08`–`+0x0F`, `+0x11` and `+0x13` are undeclared. `+0x10`/`+0x11` are
  zeroed together as a word at `003DB5C7`, which again does not make them one field.
- `003DC0D0` (the payload release) and `00263050` (the class-indexed notify) are **not read**, so
  what removal actually releases is not established.
- Everything here is static. **No runtime observation confirms a live list.**

## 14. The `+0xA8` slots are wait slots, and they are why an actor can be driven several times a frame (2026-09-10)

§13 said the `+0xA8` array is *"one `0x28`-byte state block per channel"*, inferred from the fact
that `slotCountA8` bounds both the array and the channel scan in `003DBF60`. **That inference is now
replaced by direct evidence, and it happens to hold.** `0025E09B` passes `(int8)rec[0x11]` — the
very byte that indexes the `+0xA8` array — as the **channel** argument to
`ActorResource_FindScriptRequestEntry`. Wait slot *i* and resource channel *i* are one index space,
because one byte is used as both.

What the block actually is, though, is a **wait slot**: `ActorWaitSlot`, `0x28` bytes.

### The dispatch

`WorldActor_UpdateRuntimeAndScriptExecutionState` (`0025DF00`) loads
`slot = rec->slotsA8 + (int8)rec->currentWaitSlot * 0x28`, then switches on `slot->waitKind`
through the eight-entry jump table at `0025E3CC`. *(That address is data, not a function, and `verify_doc_addresses.py` flags it for review: `0025DF00` is 1,228 bytes, so it ends at exactly `0025E3CC` and the table sits immediately after its own function — confirmed in context.)*

| kind | arm | waits until | settles with |
|---:|---|---|---|
| 0 | `0025E127` | — **nothing; the slot parks immediately** | — |
| 1, 2 | `0025E0BE` | — **runnable**: publishes the record to `02099D80` and calls the bytecode interpreter `0025E4C0` | — |
| 3 | `0025E027` | `ActorResource_FindActiveEntryByIdOrClass(target, slot->waitResourceId, class)` returns `0xFF` | `waitKind = 1`, `settled = 1` |
| 4 | `0025E091` | `ActorResource_FindScriptRequestEntry(rec, rec->currentWaitSlot, slot->stamp - rec[+0x58])` returns `0xFF` | **removes the entry first** (`003DB2A0`), then `waitKind = 1` |
| 5 | `0025E00A` | `002674B0(managerSlot, &slot->targetRef)` returns 0 | `waitKind = 1` |
| 6 | `0025E058` | `ActorResource_IsChannelBitActive(target, slot->waitChannel)` returns 0 | `waitKind = 1`, `settled = 1` |
| 7 | `0025E083` | `ScriptVM_WaitList_HasAnyActorChannelActive(managerSlot, &slot->targetRef)` returns 0 | `waitKind = 1` |

Three things fall straight out of the table.

**Kind 4 is the only one that consumes what it waited on** — which is exactly the correction
[`the-field-runtime-pass`](../the-field-runtime-pass.md) §Evidence recorded in 2026-09-03, that the
removal lives in the caller rather than in the pure reader `003DC050`. This is the same fact seen
from the type side: the wait slot's kind is what selects that behaviour.

**`settled` is not a generic settle marker.** Kinds 3 and 6 set it; kinds 4 and 5 settle without it.
Anything reading `+0x27` as *"the wait finished"* would be wrong for half the kinds.

**`targetRef` is a base-relative reference, not a pointer and not a handle.** `0020E600` is three
instructions — `mov eax, ecx / add rax, [01F83530] / ret` — so the field is a **32-bit offset from a
global heap base**. Kinds 3 and 6 resolve it; kinds 5 and 7 pass `&slot->targetRef` as the address
of a descriptor instead, so the same four bytes are read two different ways depending on the kind.

### `parked` is the drive loop's terminator

`the-field-runtime-pass` §7 warns that a hook on this function *"will be called several times per
actor per frame"*, and its §Evidence observes that the loop terminates because *"each pass either
blocks on a wait or executes bytecode"*. `+0x16` is the field that makes that true:

```
0025DFA0  loop top
0025DFD9 / 0025DFEC   slot->parked = 0        (bpl is 0 from 0025DF1F onward)
   ... dispatch ...
0025E127  slot->parked = 1                    every blocked arm lands here
0025E11A  slot->parked = 1                    bytecode ran but did not finish
```

So the loop clears the flag on entry and any outcome that made no progress sets it again. Under
HALFRATE, clearing a flag that **was** set costs an extra `001ED180` test that can abort the whole
pass — the same half-rate family that gates the widget tree.

### An inherited conflict at `+0x58`, recorded rather than resolved

Wait kind 4 reads a **dword** at `rec + 0x58` (`0025E097 sub r8d, dword [rdi+0x58]`). The store
declares `+0x058` as **4 bytes** with ctype `void*` — a 4-byte pointer, which cannot be right on
x64 — and its evidence is *"written with a pointer"*. The constructor's actual store is
`002667CA mov qword ptr [rbx + 0x58], rax`, **eight** bytes.

Those cannot all hold. The qword store proves eight bytes are written; the dword read proves a
four-byte consumer at `+0x58`; and `+0x5C`, which would be the other half, is one of the five
offsets the crude field scan promoted and the disciplined taint does **not** re-find (§12). **Left
as it stands, flagged here.** Fixing it needs a reader for `+0x5C` or for the upper half of the
qword, and inventing one to make the rows tidy is exactly what the store refuses.

### Limits

- **The wait kinds' argument layout is only partly recovered.** `+0x04`–`+0x13`, `+0x15`, `+0x17`,
  `+0x1C`–`+0x1F` and `+0x22`–`+0x25` are undeclared. `002674B0` and `00267420` take
  `&slot->targetRef` as a descriptor and neither is read, so how much of the block they consume is
  unknown.
- **Who sets a non-1 `waitKind` is not established here.** Every site in this function *clears* a
  wait; the bytecode interpreter `0025E4C0` is the obvious candidate and was not read.
- `+0x18`–`+0x27` are **not** cleared at construction — the initialiser's clear loop stops at
  `+0x16` — so a slot's argument bytes carry whatever the previous wait left until a new wait is
  armed.
- Entirely static. No runtime observation of a live wait slot.

## 15. Who arms a wait, and the 32-bit reference the engine uses instead of pointers (2026-09-10)

§14 recovered the wait slot and every site that *clears* a wait, and said plainly that **who sets a
non-runnable `waitKind` was not established**. It is the bytecode interpreter, and the arming
sequence is regular enough to read as a contract.

### The arm sequence

`WorldActorScriptVM_InterpretBytecode` (`0025E4C0`) arms a wait slot from **eleven** sites that
share one shape. Taking `0025F57F`–`0025F5D4` as the exemplar:

```asm
0025F57F  mov   byte  [rsi + 0x26], dil        ; waitChannel
0025F586  call  00358940                       ; ActorManager_GetRecordByOrdinal(mgr, ebx)
0025F593  call  003DB640                       ; ActorResource_IsChannelBitActive(rec, channel)
0025F59A  je    0025F653                       ; NOT active -> arm NOTHING, fall through
0025F5A3  call  0020E620                       ; record -> base-relative reference
0025F5B7  mov   dword [rsi + 0x18], eax        ; targetRef
0025F5C1  mov   word  [rsi + 0x24], bx         ; targetOrdinal
0025F5C7  mov   word  [rsi + 0x20], r12w       ; waitResourceId
0025F5CC  mov   byte  [rsi + 0x27], 0          ; settled = 0
0025F5D4  mov   word  [rsi + 0x14], 0x0106     ; waitKind = 6 AND armed = 1, in one store
```

Four things this establishes.

**A wait is only armed if the thing being waited on is already busy.** The `je` at `0025F59A`
skips the entire arm when the channel is inactive, so the script proceeds without ever entering a
wait. A reimplementation that always armed and then immediately settled would produce the same
final state by a different number of frames.

**`waitKind` and `commandPhase` are written as one 16-bit store.** `mov word [rsi+0x14], 0x0106`
sets `waitKind = 6` and `+0x15 = 1` together. *(Renamed from `armed` 2026-09-16 (FABLE), answering `OPUS-REQ-FABLE-IS-0X15-ONE-STATE-BYTE`: `+0x15` takes **four** values and is **one ordered phase** — 0 begin pending, 1 polling, 2 int32 result pending, 3 float32 result pending — because `VMNativeCommand_ExecuteLifecycle` (`002621D0`) branches on it as three ordered cases and fetches a different one of the verb's three callbacks for each. `armed` was a correct **predicate**, `commandPhase != 0`, and an incomplete field name; the re-entry reading below is right about what state 1 does.)* So what the store writes is **phase 1**, the opcode's **re-entry marker**. Twelve `cmp byte [rsi+0x15], 0 / jne` sites take the resume path when it is set, and
twelve `mov byte [rsi+0x15], 0` sites clear it when the opcode finishes. The kinds armed with a
byte-only store — 3 at `00261596`, 4 at `002602EE`, 5 at `00261D24` — deliberately leave it alone.

**`settled` is cleared at arm time**, which confirms §14's reading of `+0x27` from the other end.

**`targetOrdinal` and `targetRef` are two different things**, and keeping them apart matters:
`+0x24` is the ordinal `ActorManager_GetRecordByOrdinal` takes, `+0x18` is a reference to the record
itself. The resume path reloads `+0x24` and `+0x20` and pushes them into a **64-entry** script wait
list near `02099AC0` (`0025F74B`–`0025F773`, bound `cmp r9d, 0x3f`), which is what
`ScriptVM_WaitList_HasAnyActorChannelActive` (`00267420`) later scans.

### The reference ABI: a 32-bit offset where you would expect a pointer

`0020E600` and `0020E620` are an encode/decode pair, three instructions each, and together they
define how this engine stores a reference to a heap object in four bytes:

```asm
0020E620  sub  ecx, dword ptr [01F83530]    ; encode: ptr -> offset   (32-bit subtract)
0020E626  mov  eax, ecx
0020E628  ret

0020E600  mov  eax, ecx                     ; decode: offset -> ptr   (zero-extends)
0020E602  add  rax, qword ptr [01F83530]    ;                         (64-bit add)
0020E609  ret
```

**The asymmetry is the contract.** The encoder subtracts 32 bits and the decoder adds 64, so a
round trip is only faithful while every referenced object lives **within 4 GiB above
`*(01F83530)`** and at or above it — an object below the base encodes to a large positive offset
and decodes to the wrong address. That is a real constraint on any reimplementation's allocator,
and it is invisible unless both halves are read.

**Consequences for the type store.** A field holding one of these is **not** a pointer and **not** a
handle: it has no validity bit, no generation, and no null encoding other than whatever offset
happens to be zero. `ActorWaitSlot.targetRef` is recorded as `uint32` for exactly that reason.

### Limits

- **Eleven arm sites, one read in full.** The other ten match by instruction shape and by the
  displacement scan, not by having been read end to end. The kind 3, 4 and 5 arms were located but
  their argument setup was not read.
- **What the opcodes mean is not claimed here.** This is the type-side half: which fields the
  interpreter writes and when. The opcode semantics belong to the script-VM work.
- The 64-entry wait list near `02099AC0` is named from its bound and its two writers; its element
  layout is **not** recovered — `{byte at +4, byte 6 at +0x44, dword at +0x84, dword at +0x184}` is
  what the two stores touch, which is a stride pattern, not a type.
- Static throughout.

## 16. The 1,476-byte tail was never unknown — it is the embedded sub-objects (2026-09-10)

[The undeclared tail](#the-undeclared-tail--what-a-static-scan-can-and-cannot-see-2026-09-08)
concluded that *"eight observed offsets across 1,476 bytes is close to nothing, and that is the
finding"*, and that recovering the tail needed a different instrument or runtime observation.

**Neither was needed.** §12 recovered the region map and §13–§15 recovered the two element strides
and their counts. Put together they account for the tail arithmetically, with no new evidence at
all — the facts were already in hand and had not been added up.

For kind 3, sequences 5 and 6 — the `0x6E0` size the type row carries:

| span | size | region | fixed by |
|---|---:|---|---|
| `+0x11C`–`+0x120` | 4 | still undeclared | — |
| `+0x120`–`+0x350` | `0x230` | **`movementContext`**, what `contextPtr` at `+0xB8` points at | `00266B54` plants the pointer, `00266B62 add rax, 0x230` walks past it |
| `+0x350`–`+0x4D8` | `0x188` | **`secondaryContext`**, what `+0xC0` points at | `00266B68` plants it, `00266B6F lea r8, [rax+0x188]` walks past it |
| `+0x4D8`–`+0x5A0` | `0xC8` | **`resourceEntryPool`**, 10 × `0x14` | `00266B79` plants `slotsA0`; the count is `003DB580`'s `r8d` |
| `+0x5A0`–`+0x6E0` | `0x140` | **`waitSlotArray`**, 8 × `0x28` | `00266B9B` plants `slotsA8`; `0x5A0 + 0x140 = 0x6E0` exactly |

**1,472 of the 1,476 bytes.** The record's undeclared tail is now four bytes.

**ONE REFINEMENT THE SPAN TABLE DOES NOT CARRY - 2026-09-16 (FABLE).** Re-read `00266B40`'s planting sequence to verify §16 independently. All four anchors decode exactly as stated - `00266B54 lea rax, [rdx + 0x120]` into `+0xB8`, `00266B62 add rax, 0x230` into `+0xC0`, `00266B6F lea r8, [rax + 0x188]` into `+0xA0` - and the arithmetic is exact: `0x230 + 0x188 + 0xC8 + 0x140 = 1,472`, leaving the stated 4 bytes. **But the fourth region's size is chosen at runtime, not fixed.** `00266B83` tests the per-sequence table byte `[r9 + rax*4 + 0x1CEC329]` against 1, then ~~`00266B8C` loads **`0xC8`** if it matches and `00266B93` **`0xA0`** if it does not~~ `00266B8C` loads `0xC8` and `00266B93` replaces it with `0xA0` when the byte is 1 *(corrected 2026-10-02, OPUS: `00266B91 jne 00266B98` skips the `0xA0` load when the byte is not 1; rows 2, 4 and 7 of `01E0C328` carry 1)*, before `add rax, r8` plants `+0xA8`. So `resourceEntryPool` is **10 × `0x14`** in the kind-3 / sequences-5-6 case the table is scoped to, and **8 × `0x14` wherever that byte is ~~not~~ 1** - which moves `waitSlotArray` to `+0x578` and makes the sequence-7 record ~~**`0x6B8`, not `0x6E0`**~~ **`0x668`** *(corrected 2026-10-02, OPUS: the table's size word for row 7 at `01E0C344` is 1,640 = `0x668`, with six wait slots, `0x578 + 6 × 0x28`)*. **The §16 table is correct for the case it names and easy to over-read as universal.** The record's layout is **sequence-dependent**, and the 1,472-of-1,476 accounting holds for the `0x6E0` variant only. ~~*I did not read the table at `01CEC329` to say which sequences take which branch.*~~ *(answered: the table is `01E0C328` — `r9` holds the image base, so `[r9 + rax*4 + 0x1CEC329]` is `01E0C329`, the `+1` byte — and rows 2, 4 and 7 take the `0xA0` branch; 2026-10-02, OPUS)*

### Why the earlier instrument saw nothing there, and why that was the right answer

The kind-decode scan found eight offsets beyond `+0x118` and the page called that *"close to
nothing"*. It was right, and now it is explained: **there is nothing there to find by that method.**
The tail is not a flat continuation of the header — it is four embedded objects, and code touching
them holds a pointer to the *sub-object*, not to the record. `0026AEA3 mov rcx, [rcx+0xB8]` is
precisely that, and §12 showed it is also what made the crude scan over-count.

So the tail's fields belong to `movementContext`, `secondaryContext`, `ActorResourceEntry` and
`ActorWaitSlot`, and they are recovered by following those pointers — which is exactly what §13–§15
did for the last two. The page's own conclusion, *"recovering it needs a different instrument —
following the pointer through the systems that own it"*, was correct; this is that, done.

### The per-kind warning, which the type store cannot express

`_types/` carries one layout per type, and `ActorStorageRecord`'s size is `0x6E0` — the kind 3
sequence 5/6 size. **The four region rows are that sequence's offsets.** The other six sizes place
the same regions elsewhere; §12's table has them. A reader resolving anything at or above `+0x120`
**must branch on `rec[3] & 0x1F` first**, and each region row says so in its own `meaning` column so
the warning travels with the data rather than living only here.

The two arrays also vary in *length*, not just position: `sub == 1` kinds get 8 entries and 6 wait
slots instead of 10 and 8, so `resourceEntryPool` is `0xA0` and `waitSlotArray` is `0xF0` there.

### What is left

`ActorStorageRecord` now declares 1,667 of its 1,760 bytes. The residue is twelve gaps totalling
**93 bytes**, the largest a 28-byte span at `+0x6C`–`+0x88`, and they are all in the header where
the kind-decode scan already works — local, bounded, and reachable by the instrument that exists.

Still open and **not** closed by this: `movementContext` and `secondaryContext` have their extents
but no internal layout at all. `+0x0B0`–`+0x0B8` and `+0x0C8`–`+0x0E8` remain, and the `+0x58`
size conflict §14 recorded is untouched.

## 17. The last header gap is a pointer block, and it comes from the resource payload (2026-09-10)
> ### CORRECTED 2026-09-10 — the bind's record is the ActorManager slot, not this record (`OPUS-CONTRA-REC60`)
>
> `ActorManager_BindLoadedDefinitionPayload` (`0026C8C0`) computes its `rdi` in the prologue as
> `02098E10 + slot × 0x288` (`0026C8FE lea rdi, [r14 + 0x1F78E10]`; `0026C907 imul r8, rbp, 0x288`;
> `0026C90E add rdi, r8`) and stores it in `02099D70` (`0026C911`), writing the slot index at `+0x28`
> (`0026C957`) — **the actor-manager record** of stride `0x288`
> ([the world-tick page](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md) §2),
> not an `ActorStorageRecord`. Its qword stores at `+0x50` / `+0x58` / `+0x60` / `+0x68`
> (`0026CB17`–`0026CB43`) are that record's pointer block; the writes to `+0x15`, `+0x16`, `+0x30`,
> `+0xA0`, `+0xA8` in the same body are its fields at the same offsets. On *this* record `+0x60` is
> the byte free-list head §13 reads (`003DB3E6` / `003DB3F9`), and a typed field scan seeded by
> `ActorManager_GetRecordByOrdinal` (`00358940`) reaches those byte accesses and never reaches
> `0026C8C0`. The pointer-block reading below stands for the manager record; the field rows it
> proposed belong to `ActorManagerRecord`, not here.


§16 left twelve header gaps, the largest 28 bytes at `+0x6C`–`+0x88`. It is not a gap. It is the
back half of a **block of six pointers that binding installs from the actor's definition payload**,
and the reason a displacement scan never saw it as fields is that four of the six had been recorded
at the wrong width.

### `ActorManager_BindLoadedDefinitionPayload`, read in one block

`0026CB04`–`0026CB76`, with `rdi` the record and `r15` the loaded payload:

```asm
0026CB04  mov     eax,  dword ptr [r15 + 0x48]     ; unsigned
0026CB0F  add     rax,  r15
0026CB17  mov     qword ptr [rdi + 0x50], rax      ; payloadSectionA
0026CB26  lea     rax,  [rip + 0x1e2d2c3]          ; -> 02099DF0, a static bank
0026CB2D  mov     qword ptr [rdi + 0x58], rax      ; payloadSectionB  (default)
0026CB31  lea     rax,  [rip + 0x1e2d4b8]          ; -> 02099FF0, a static bank
0026CB38  mov     qword ptr [rdi + 0x60], rax      ; ** see the contradiction below **
0026CB3C  movsxd  rax,  dword ptr [r15 + 0x20]     ; SIGNED
0026CB43  mov     qword ptr [rdi + 0x68], rax      ; payloadSectionC
0026CB4E  mov     qword ptr [rdi + 0x70], rax      ; payloadSectionD   <- [r15+0x24]
0026CB59  mov     qword ptr [rdi + 0x80], rax      ; payloadSectionF   <- [r15+0x2C]
0026CB6B  mov     qword ptr [rdi + 0x78], rax      ; payloadSectionE   <- [r15+0x28]
```

**The payload is position independent.** Its header carries 32-bit offsets at `+0x14`, `+0x20`,
`+0x24`, `+0x28`, `+0x2C` and `+0x48`, and binding is the step that turns them into pointers. The
section offsets are read **signed** (`movsxd`) while `+0x48` is read **unsigned** (`mov eax`) —
a real difference, not a transcription artefact, and it means a section may sit *before* the payload
base while `+0x48`'s may not.

`payloadSectionA` at `+0x50` is installed **twice by different producers and the same way**: the
initialiser builds it as `base + [desc+0x14]` (`002667A6`–`002667B9`), the binder as
`r15 + [r15+0x48]`. Two independent paths, one shape.

### Four widths corrected, two offsets withdrawn

| offset | was | is | why |
|---|---|---|---|
| `+0x058` | `4` bytes, ctype `void*` | **8** | a 4-byte `void*` is not a possible field on x64; both writers store a qword. The wait-kind-4 path reads only the **low dword** (`0025E097 sub r8d, dword [rdi+0x58]`), which is what made it look narrow |
| `+0x05C` | its own `uint8` row | **withdrawn** | **zero** references across the six bodies proven to hold a record |
| ~~`+0x068`~~ | ~~`4` bytes~~ | ~~**8**~~ | ~~`0026CB43` stores a qword~~ **WITHDRAWN 2026-09-16 (OPUS) — wrong type, see below** |
| ~~`+0x070`, `+0x078`, `+0x080`~~ | ~~undeclared~~ | ~~**8** each~~ | ~~`0026CB4E`, `0026CB6B`, `0026CB59`~~ **WITHDRAWN 2026-09-16 (OPUS)** |

> **Those four cited stores write an `ActorManagerSlot`, not this record (OPUS, 2026-09-16).** All
> four are in `ActorManager_BindLoadedDefinitionPayload` (`0026C8C0`) and all four go through `rdi`,
> which that function sets once and never reassigns: `lea rdi, [r14 + 0x1F78E10]` with `r14` the
> image base, then `add rdi, r8` (`0026C8FE`–`0026C90E`). `0x120000 + 0x1F78E10 = 0x02098E10`, and
> `_types/types.tsv` declares `ActorManagerSlot` at exactly **`0x02098E10 + slot * 0x288`**. This
> record is `0x6E0` bytes and a different array.
>
> The slot's own rows already hold every one of them, at 8 bytes, with meanings that match the
> instructions exactly — `payloadSectionC` is *"payload base plus the SIGNED 32-bit offset at
> payload+0x20"*, and the code is `movsxd rax, dword [r15+0x20]; add rax, r15; mov [rdi+0x68], rax`.
> `+0x70` takes payload+0x24, `+0x78` (`variableDescriptorTable`) payload+0x28, `+0x80`
> (`payloadSectionF`) payload+0x2C. The same sequence writes `+0x60` (`groupPersistentBank`) and
> `+0x98` (`localVariableResolver`) — and `+0x60` is the tell, because **this** record documents
> `+0x60`–`+0x63` as four one-byte list heads, which a qword store there could not coexist with.
>
> **The type store was right and was never changed**: it still carries `vmRegI0`–`vmRegI3` at
> `+0x64`…`+0x70` and `vmRegF0`–`vmRegF3` at `+0x74`…`+0x80`, four bytes each. Accepting these four
> rows would have merged eight named VM registers into four 8-byte fields on the strength of another
> type's initialiser. The other rows in this table stand: `+0x058` rests on a `void*` being 8 bytes
> on x64, and `+0x106` on `002666E5`, both independent of `0026C8C0`.
| `+0x106` | `1` byte, ctype `uint16` | **2** | its own evidence is a **word** store, `002666E5` |
| `+0x107` | its own `uint8` row | **withdrawn** | **zero** references across the same six bodies |

**Positive control for both withdrawals.** The same scan over the same six bodies returns **9**
references for displacement `+0x03`, the proven kind byte. The instrument sees what it should; the
two offsets are absent from it, not invisible to it.

**Search boundary.** Those six functions only — `0025DF00`, `00266530`, `0026AE90`, `0026C8C0`,
`0025E4C0`, `002679F0`. `+0x5C` and `+0x107` each had two hits from the *crude* scan, in functions
whose base register was never proven to be a record; the disciplined taint does not reproduce
either. **Withdrawn is not refuted** — it means nothing that provably holds a record touches them.

### The contradiction at `+0x60`, recorded and not resolved

`0026CB38` writes a **full qword** at `+0x60`. §13 recorded `+0x60` as `entryFreeListHead`, a
**byte**, from `ActorResource_RemoveActiveEntry` — which also uses `+0x61`, `+0x62` and `+0x63` as
three more separate bytes, all inside that qword. A byte store at `003DB3F9` would destroy the low
byte of the installed pointer.

Both readings have direct instruction evidence and `rdi`/`rbx` is provably the record in both
functions. What decides between them is not in hand, so **both are preserved**: the byte rows stand,
the row carries the conflict, and the ticket is `OPUS-CONTRA-REC60`.

One measurement narrows it. A displacement scan over the **1,147** `Actor*`/`Spawn*`/`Movement`/
`Combat*`/`Battle*` bodies, positive control `+0x03` returning 175 references, finds **no qword
read of `+0x60` anywhere** — only the binder's write. So the installed pointer has no consumer that
this scan can see, which is consistent with the store being vestigial, but a scan bounded to those
owners is not a proof of absence across the image.

**What would settle it:** a consumer for the `+0x60` pointer, or evidence that a record's resource
lists and its bound payload are never live at the same time.

### Where the record stands

**1,698 of 1,760 bytes declared.** *(2026-09-27, FI-1: the `+0xC8`–`+0xE8` gap below is the initialiser's `rep stosw`
span, an 18-slot `u16` override array - [the FI-1 record](../../_index/candidates/fi1-offset-names/README.md).)* Ten gaps totalling **62 bytes**, the largest 32 at
`+0xC8`–`+0xE8`. The record began this session at 284 declared bytes with a 1,476-byte tail its own
page called unrecoverable by static means.

## 18. CORRECTION — §17 attributed a pointer block to the wrong type (2026-09-10)

**§17 is wrong about whose fields those are, and the mistake is the one §12 was written to warn
about.**

§17 read `ActorManager_BindLoadedDefinitionPayload` (`0026C8C0`) and attributed its `rdi` stores —
`+0x50`, `+0x58`, `+0x60`, `+0x68`, `+0x70`, `+0x78`, `+0x80` and several others — to this record.
`rdi` is not this record:

```asm
0026C8FE  lea   rdi, [r14 + 0x1f78e10]     ; r14 = 0x00120000, so rdi = 0x02098E10
0026C907  imul  r8,  rbp, 0x288
0026C90E  add   rdi, r8                     ; = the ActorManagerSlot for slot rbp
0026C911  mov   qword ptr [rip + …], rdi    ; published to 02099D70
```

It is an **`ActorManagerSlot`**, and the function goes on to write `[rdi+0x244]`, `[rdi+0x24C]`
and `[rdi+0x254]` — inside `0x288`, and far outside anything §17 claimed.

**How the error happened, stated plainly.** The function writes `[rdi+0x30]`, `[rdi+0xA0]` and
`[rdi+0xA8]`, and this record already had fields at all three. I matched by displacement and did
not prove the base — which is **exactly** the failure §12 documented in the crude field scan, and
exactly what `0026AEA3 mov rcx,[rcx+0xB8]` had already demonstrated. Writing the warning did not
stop me making the mistake.

**Found by FABLE**, from the other end: a typed scan seeded by `ActorManager_GetRecordByOrdinal`
reaches `003DB2A0`, `003DBCF0` and `003DC130` — the byte users of `+0x60` — and **never reaches
`0026C8C0`**. Two types, two `+0x60`s.

### What is corrected

| row | outcome |
|---|---|
| `+0x068`, `+0x070`, `+0x078`, `+0x080` | **removed from this record.** They were justified only by the misattributed function, and they are now `ActorManagerSlot` fields |
| `+0x050`, `+0x058` | **kept.** Both have the initialiser's own stores — `002667B9` and `002667CA`, with `rbx` provably this record — which are independent of the withdrawn evidence. `+0x58` stays 8 bytes on `002667CA` alone |
| `+0x015` | **meaning withdrawn.** *"set to `(bindArg != 3)`"* was the manager's field, not this one |
| `+0x016`, `+0x011`, `+0x030`, `+0x0A0`, `+0x0A8` | bogus *"cleared at 0026CC…"* clauses removed; each row's own evidence stands |
| `+0x5C`, `+0x107` | **still withdrawn.** Their withdrawal rested on the six-body scan and its positive control, not on this function |

The 28-byte gap §17 claimed to close is therefore **open again** — now 36 bytes at
`+0x64`–`+0x88` *(answered: CLOSED 2026-09-12 — the script VM's register file, four `int32` at `+0x64`–`+0x70` and four `float` at `+0x74`–`+0x80`; see §2's `+0x64` row; 2026-10-02, OPUS)*. `ActorStorageRecord` declares 1,662 of 1,760 bytes, not 1,698.

### And the contradiction it resolves

`OPUS-CONTRA-REC60` asked whether `+0x60` is a qword pointer or a byte free-list head. **Both, on
different types.** The qword belongs to `ActorManagerSlot`; the byte free-list head belongs here,
and stays `uint8`. There was never a conflict inside one structure — only a misattribution
manufacturing one.

**A second thing it settles.** `ActorManagerSlot`'s `+0x58` and `+0x60` bank pointers lacked a
writer. The bind is it: it installs the static defaults `02099DF0` and `02099FF0`.

> **Both addresses above were wrong when first published, and so was the sentence that followed
> them. See [§21](#21-two-fabricated-addresses-a-false-absence-and-what-produced-each-2026-09-11).**

## 19. Charter §26 readiness assessment — actor storage (2026-09-10, OPUS)

§26 says: *"Do not call a subsystem reconstruction-ready merely because a lot is known."* A great
deal is now known about this record — 1,662 of 1,760 bytes declared, four embedded regions, two
element types, a resolved contradiction. This section answers §26's own question list instead of
counting bytes, because the counting is exactly what §26 warns against.

**This is one subsystem's assessment. It is not a project gate decision**, which §§26–27 require the
three identities to take together.

| §26 asks | answer | verdict |
|---|---|---|
| responsibilities | the per-actor storage record: identity, kind, resource channels, wait slots, and the embedded movement/secondary contexts | **answered** |
| owner | `ActorManagerSlot`, one of five, through `recordPool` at `+0x08` | **answered** |
| what it owns | nothing by pointer: `+0xA0`, `+0xA8`, `+0xB8`, `+0xC0` are **interior** and `+0x30` is a non-owning back-pointer | **answered** |
| key types | `ActorResourceEntry` `0x14`, `ActorWaitSlot` `0x28`, both promoted | **answered** |
| initialization | `002679F0` carves and stamps `+0x03`; `00266530` initialises; `00266AD0` plants the region map per sequence; `003DB580` builds the free list | **answered** |
| update ordering | `World_UpdateSimulationTick` → `ActorManager_RunFieldRuntimePass` → `WorldActor_UpdateRuntimeAndScriptExecutionState`, several times per actor per frame, terminated by the `parked` byte | **answered** |
| lifetime / destruction | ~~**no destructor identified.**~~ *(answered: see "RETRACTED 2026-09-21 (OPUS): the pool IS released"; 2026-10-02, OPUS)* The pool is carved once and records are re-bound, not freed — but nothing has been read that proves records are never destroyed | ~~**NOT answered**~~ answered *(answered: RETRACTED 2026-09-21; 2026-10-02, OPUS)* |
| inputs / outputs | inputs: the definition payload and the wait slots' armed state. Outputs: the channel lists and the bytecode the wait slots release | **partly** — the payload's own format is not recovered |
| state transitions | the wait-slot machine is explicit: eight kinds, who arms, who clears, and the `parked` flag that ends the drive loop | **answered** |
| important globals | the manager array at `02098E10`, the record pool through `+0x08`, the half-rate family | **answered** |
| callers / callees | the drive chain is read; `003DC0D0`, `00263050`, `002674B0`, `00267420` are cited and **not** decoded | **partly** |
| script dependencies | the bytecode interpreter arms waits from eleven sites and consumes them | **answered** |
| resource dependencies | the definition payload is bound by `0026C8C0` from self-relative offsets — but **what is inside those sections is unknown** | **NOT answered** |
| RNG | no RNG reaches this record on any path read | **answered (negatively, and the search boundary is the drive chain only)** |
| persistence | the record is **not** in the save image; the battle-side stats it points at are | **answered** |
| edge states | the pool exhausting, a null `battleUnit`, `0xFF` null ordinals, the cycle guard on channel walks | **partly** — pool exhaustion behaviour is not read |
| observable behaviour | ~~nothing in this subsystem has been observed live~~ **AMENDED 2026-09-11 — the region map and array counts now have a live control in two zone states ([§22](#22-the-region-map-has-a-live-control-in-two-zone-states-and-what-it-does-not-cover-2026-09-11)). Behaviour over time is still unobserved** | **partly** |
| major assumptions runtime validated? | ~~no~~ **AMENDED 2026-09-11 — the layout assumptions are; the lifetime, free-list and scheduling assumptions are not** | **partly** |
| can meaningful parity tests be constructed? | for the *layout* yes — a record can be built and compared byte-for-byte. For *behaviour* not yet: the drive loop needs the interpreter and the four undecoded callees | **partly** |

### Verdict

**Not reconstruction-ready**, and the blockers are specific rather than diffuse:

1. ~~**No runtime observation of anything in this family.**~~ **NARROWED 2026-09-11 by EXP-026,
   not cleared.** The region map, the per-sequence extents and the array counts now have a live
   positive control in two zone states — see [§22](#22-the-region-map-has-a-live-control-in-two-zone-states-and-what-it-does-not-cover-2026-09-11).
   What remains unobserved is everything that happens *over time*: the half-rate phase behaviour,
   the wait-slot drive loop and the free-list discipline are still static readings of code nobody
   has watched run. The blocker is now about **behaviour**, where it used to be about **everything**.
2. **The definition payload's section formats are unknown.** Four pointers are planted from it and
   none of the four targets has a recovered layout, so a reimplementation can bind the pointers and
   still have nothing to put behind them.
3. **No destructor, and no proof one is absent.** "Carved once and re-bound" is what has been read,
   not what has been established.

### What would change the verdict

- A runtime capture of one record across a zone change — enough to confirm the region map on a live
  object, the wait-slot cursor, and whether `+0x60`'s bytes behave as the free list says. **This is
  a discriminating runtime request and belongs to ASTRA**, not to more static reading.
- The definition payload's four section formats, which is resource-pipeline work.
- A reader for `movementContext` and `secondaryContext`, whose extents are known and whose
  internals are not.

**What is NOT a blocker:** the 98 undeclared bytes across twelve header gaps. They are local,
bounded, and exactly the kind of residue §26 says should not decide the question.

## 20. Blocker 3: nothing frees the pool, and almost nothing in this engine frees anything (2026-09-10)

§19 listed *"no destructor, and no proof one is absent"* as the third blocker on the readiness
verdict. This is that proof, built to the [absence-claim gate](../../_index/ABSENCE-CLAIM-GATE.md)'s
standard — which exists because *"nothing reads this"* is the class of claim this database has been
provably worst at, wrong in 3 of 3 recorded cases.

### Four instruments, each with a positive control

| question | instrument | control | result |
|---|---|---|---|
| does anything free the pool through the pointer the carver stored? | every memory operand of the 1,147 `Actor*`/`Spawn*`/`Movement`/`Combat*`/`Battle*` bodies at displacement `+0x1F0` | `+0x88`, **67 references** | **two qword accesses, both WRITES** — `00267AA8` (the carver) and `0026CAD9` (the binder). No read |
| does the CRT free reach the actor subsystem? | IAT caller census on `api-ms-win-crt-heap-l1-1-0!free` | the same census finds `malloc`'s **12** callers, including `00210EC0` | **10 callers image-wide**, six of them the VP8 video decoder (`vp8_destroy`, `vp8_de_alloc_frame_buffers`, …). **None in the actor or battle chain** |
| is there a matching *virtual* deallocator beside the virtual allocator? | every `call qword ptr [reg + 0x80…0xA8]` in the same 1,147 bodies | the allocator slot `+0x88` itself, found | **exactly two sites.** `+0x88` is the allocator; `+0x98` at `0026D49D` is one arm of a getter dispatch whose sibling arms merely load `[r14+0x40]`, `+0x48`, `+0x58` — a value return, not a release |
| do the recovered types have destructors? | the `dtor` column of `_types/types.tsv`, excluding Phyre | 30 non-Phyre game types | **one.** `Widget`, `00244F00` — and that is a pool-slot teardown, not a free |

### The claim — **WITHDRAWN 2026-09-21 (OPUS), see the retraction below**

> **WITHDRAWN 2026-09-21 (OPUS) — the pool IS released, at `00262D9F`. Kept as history; do not build from it.**

~~**The actor record pool is allocated once and never freed, and that is the engine's general habit
rather than a quirk of this subsystem.**~~ Everything this database has recovered as storage is
static or interior: the battle state block lives *inside the save image*, the manager slots are a
static array, the `BattleUnit` pool is static, the world-loot nodes are a static pool, the inventory
class descriptors are static, the binding-record banks are static, the gambit order sets are static,
and the actor record's own sub-objects are interior regions rather than allocations.

### RETRACTED 2026-09-21 (OPUS): the pool IS released

**`ASTRA-RETURN-OPUS-ACTOR-POOL-RELEASE-BOUNDARY` refutes the claim above, and everything in
this section that follows from it is withdrawn: "allocated once and never freed", "interior
pointers are valid for the life of the process", and the reconstruction advice that adding a
release is "adding behaviour the original does not have". The reverse is true.** Verified here
against the image rather than accepted on report.

**The release chain**, in the unload `002628B0`, with `rbx` the manager block:

```
00262D96  mov   rcx, qword ptr [rbx + 8]     ; the pool - the OWNING pointer
00262D9A  test  rcx, rcx
00262D9D  je    0x262da8                     ; null-guarded
00262D9F  call  0x3697f0                     ; release the owning allocation
00262DA4  mov   qword ptr [rbx + 8], rbp     ; null the owner - rbp zeroed at 0026292A,
                                             ;   the ONLY write to rbp in the body
00262DA8  and   byte ptr [rbx + 0x10], 0xfe  ; clear the live bit
00262DAC  and   byte ptr [rbx + 0x200], 0xfb
00262DB3  mov   byte ptr [rbx + 0x13], bpl
```

`003697F0` is thirteen bytes and is not a CRT import: `test rcx,rcx / je ret / xor edx,edx /
jmp 0x369860`. It is a null-guarded tail into the engine's own allocator release with the
second argument zeroed.

### Why four instruments with controls all missed it (OPUS, 2026-09-21)

Each instrument was sound and each answer was true of what it asked. They missed for five
separate reasons, and a reader should know all five:

| the instrument | why it could not see this release |
|---|---|
| every memory operand at displacement `+0x1F0` | the release goes through **`+0x08`**. `+0x1F0` is a DERIVED interior pointer - allocation base plus aligned header - so "two writes, no read" was correct and irrelevant. The section already flagged `+0x1F0` as the wrong root; the search used it anyway |
| the CRT `free` IAT census | `003697F0` is the engine's own allocator release, not the CRT |
| `call qword ptr [reg + 0x80..0xA8]` | `00262D9F` is an **ordinary direct call**, not a virtual dispatch |
| the `dtor` column of `types.tsv` | there is no destructor. The release lives in an unload function, which is not the same shape |
| **the population itself was name-filtered** | `002628B0` is **`FUN_002628b0`** - unnamed. It falls outside an `Actor*`/`Spawn*`/`Movement`/`Combat*`/`Battle*` set whether the filter is a prefix (469 bodies) or a substring (575). **The body that frees was never in the searched set.** The cruel detail: the function that IS named `ActorSystem_ReleaseManagerRecords` (`0025B070`) is the semantic cleanup, and it does **not** release the allocation |

**The Limits section above got this exactly right and was not believed hard enough.** It says:
*"A custom allocator with its own internal free would be invisible to every instrument above.
The pool comes from a virtual call, so its allocator is not identified; if that object has a
release path not reachable through `[reg+0x80...0xA8]` in the actor-owned set, this misses it."*
That is precisely what happened. The hedge was correct while the headline was stated in bold as
guidance, and the headline is what a reimplementer would have read. When a limit describes a
live possibility this specifically, the claim it qualifies should not be stated as a habit of
the engine.

### What the lifetime actually is (OPUS, 2026-09-21)

**Teardown is two phases, and they are separable** - `00262D2C cmp edi, 4 / je 0x262d96` sends
one arm straight past the first phase into the second:

1. **Semantic cleanup** - `00262D34 call 0x25b070` (`ActorSystem_ReleaseManagerRecords`) and the
   mode-dependent subsystem calls that follow it. Logical teardown; the allocation still exists.
2. **Owning-allocation release** - the block above. The pool is freed, `manager+0x08` is nulled,
   and the live bit is cleared in the same breath.

**The ownership roots, which is what the type store needs:**

* `manager+0x08` is the **owning pointer**. Installed at `0026CEB8` from the virtual allocator
  called at `0026CEB0`, released and nulled at `00262D9F`/`00262DA4`. Manager identity is
  `02098E10 + sign_extend(index) * 0x288`.
* `manager+0x1F0` is a **derived interior pointer**, allocation base plus aligned header size,
  stored at `00267AA8`. It is not an independent allocation and must not be treated as a root.
* **The pool is a counted pointer table, not a record array.** `00358940` reads
  `pool = [manager+0x08]`, then fails closed to zero on three guards - pool non-null, ordinal
  non-negative, `ordinal < dword[pool+0x00]` - and returns `qword[pool + 0x08 + ordinal*8]`. So
  `+0x00` is a `uint32` count and `+0x08` begins an array of record POINTERS. Record addresses
  are table entries; there is no uniform record stride to compute from.

**Therefore interior pointers are NOT valid for the life of the process.** `contextPtr`,
`slotsA0`, `slotsA8`, `+0xC0` and every record address obtained from `00358940` are valid for
the life of the **allocation**, which ends at `00262D9F`. A reimplementation needs a release
path; one that allocates and never frees is the one diverging from the original.

**What this does NOT establish, stated so the correction is not over-read:** when `002628B0`
runs in an ordinary session, how often, or whether any holder actually retains an interior
pointer across it. This is a static ownership result - the release exists, its root is
`manager+0x08`, and the lifetime bound is real. Whether anything dangles in practice is a
different question and is not answered here. The other storage the section lists as static -
the battle state block inside the save image, the manager slots, the `BattleUnit` pool, the
world-loot nodes - is untouched by this and was not re-tested.

### Why this matters more than a missing destructor row — **WITHDRAWN 2026-09-21 (OPUS)**

> **Both paragraphs below are WITHDRAWN.** They are kept as history because the reasoning is
> worth seeing, not because it holds. The pool is released at `00262D9F` and the owner nulled
> at `00262DA4`; interior pointers are bounded by the ALLOCATION's lifetime, not the process's.
> **The reconstruction advice in the second paragraph is reversed** — a reimplementation needs a
> release path. See the retraction block above.

~~**Interior pointers are valid for the life of the process.**~~ *(WITHDRAWN 2026-09-21 (OPUS))* `contextPtr`, `slotsA0`, `slotsA8`,
`+0xC0`, the manager's section pointers, `BattleUnit.statsRecord` — none of them can dangle,
because nothing they point into is ever released. Code all over the engine is entitled to hold them
indefinitely, and evidently does.

~~**So a reimplementation that adds destructors and frees is not being tidy — it is adding behaviour
the original does not have**~~ *(WITHDRAWN 2026-09-21 (OPUS) — THIS IS BACKWARDS; the original DOES free, and a
reimplementation that never releases is the one that diverges)*, and it breaks the lifetime assumption every holder of an interior
pointer depends on. The right shape is arena or static allocation with no teardown.

### Limits, stated plainly

- **This is not "no code in the image frees anything".** `LocalFree` has 46 sites across 31
  callers, all in the `0x0015xxxx` library region, and CRT `free` has its ten. The claim is about
  the actor and battle storage chain.
- **A custom allocator with its own internal free would be invisible to every instrument above.**
  The pool comes from a *virtual* call, so its allocator is not identified; if that object has a
  release path not reachable through `[reg+0x80…0xA8]` in the actor-owned set, this misses it.
- The function population is those 1,147 bodies, not the image's 34,270.
- **Static only**, like everything else in §19. A live capture showing the pool address unchanged
  across a zone change would convert this from "no free was found" to "the pool survives", which
  are different statements. That is already requested as `OPUS-REQ-ASTRA-ACTORLIVE`.

### Blocker 3, resolved as far as static evidence can take it

§19's verdict stands — the subsystem is still not reconstruction-ready — but this blocker changes
character. It was *"no destructor, and no proof one is absent"*. It is now **a controlled absence
claim with four instruments and a named boundary**, which is what the charter asks for. What
remains is the runtime confirmation, and that is blocker 1. *(answered: the absence claim is retracted — see "RETRACTED 2026-09-21 (OPUS): the pool IS released"; 2026-10-02, OPUS)*

## 21. Two fabricated addresses, a false absence, and what produced each (2026-09-11)

§18 was a correction caught by FABLE. This one nobody caught, because nobody else was looking at it.
I went looking on purpose, at rows I had written myself, and three of the four claims about
`ActorManagerSlot`'s bank pointers were wrong.

### What the instructions actually say

`0026CB26` and `0026CB31` are `lea rax, [rip + disp]`. The target is *next instruction + disp*, and
nobody had done that arithmetic:

| site | next insn | disp | target | stored at |
|---|---|---|---|---|
| `0026CB26` | `0026CB2D` | `+0x1E2D2C3` | **`02099DF0`** | `+0x58` |
| `0026CB31` | `0026CB38` | `+0x1E2D4B8` | **`02099FF0`** | `+0x60` |

The page had said `02099FF0` and `0209A1F0`. Both wrong — and wrong in a specific, legible way:
**each was shifted one step down a real `+0x200` sequence.** `02099DF0`, `02099FF0`, `0209A1F0` are
three consecutive 512-byte regions, so the pattern I extrapolated from exists. That is precisely why
the error survived reading: a fabricated address that fits an observed sequence looks like a
verified one. The rule §12 of this page states — *prove the base, never match the displacement* —
has a twin, and this is it: **resolve the target, never continue the sequence.**

### The banks are 0x200 bytes, and one of them persists

The accessors index `+0x58`'s bank as 64 `u16` and `+0x60`'s as 32 `u16` — 128 and 64 bytes. Neither
is the region's size. Both are **512 bytes**, from two independent instruments:

- **Clearing.** `WorldPersistence_ResetBanksForFieldTransition` (`0026DB30`) calls
  `memset(02099DF0, 0, 0x200)` at `0026DB73` and `memset(02099FF0, 0, 0x200)` at `0026DC04`.
  `WorldPersistence_ResetBanksAndMarkInitializationState` (`00268320`) and `00266D10` do the same
  pair with the same size.
- **Copying.** `WorldPersistence_ExportGroupPersistentBank` (`0025D8E0`) and
  `WorldPersistence_ImportGroupPersistentBank` (`00269A20`) are unrolled `movups` loops: 4
  iterations of `0x80` bytes = `0x200` exactly, to and from a caller buffer.

So **`02099FF0` is persistent state** — exported and imported whole — and the accessor pair reaches
only the first 64 bytes of it. The other 448 bytes have no accessor in anything read here. That is
now an open question rather than an unnoticed assumption.

### `0209A1F0` is not a manager bank at all — it is the party roster

The address I invented for `+0x60` turns out to be a real object owned by another category, and the
`11-Party` pages already describe it correctly as a flat four-entry array. Their reading is right,
and `ActorStorage_InitializeRecord` corroborates it from the actor side:

```asm
00266744  movsx   edx, byte ptr [rbx + 0x12]      ; the record's party slot
0026674F  cmp     edx, 3
00266752  ja      0x266775                        ; UNSIGNED - rejects negatives too
00266754  movsx   rax, dl
00266758  mov     rdx, qword ptr [r11 + rax*8 + 0x1f7a1f0]   ; read the slot's occupant
00266760  mov     qword ptr [r11 + rax*8 + 0x1f7a1f0], r13   ; clear it (r13 = 0)
0026676D  mov     byte ptr [rdx + 0x12], 0xff     ; evict: old occupant loses its slot
00266771  mov     byte ptr [rdx + 0x0f], 3
0026677C  mov     qword ptr [r11 + rax*8 + 0x1f7a1f0], rbx   ; install this record
```

`r11` is proven: `0026654F lea r11, [rip - 0x146556]` with the next instruction at `00266556`, so
`r11 = 0x00120000`, the image base — the same convention this database has now recorded six times.
Stride `rax*8`, bound 0..3, **four qwords**, and the reset function zeroes exactly 32 bytes of it
with two `movdqu` stores at `0026DB52` and `0026DB5A`. Four pointers, 32 bytes, agreeing three ways.

**Joining a record to a party slot evicts whoever held it**, writing `0xFF` and `3` into the old
occupant. That is a roster invariant the actor side enforces, and it belongs to `11-Party`'s pages
rather than mine — routed as `OPUS-REQ-FABLE-ROSTER`, not written into their prose here.

### The false absence, and where it came from

`+0x60` was recorded *"write-only so far: no reader found"* and `+0x48` *"read-only so far: no
writer found"*. Enumerating every reference to the three globals gives three complete getter/setter
pairs:

| field | global | bound | getter | setter |
|---|---|---|---|---|
| `+0x48` | `02098E58` | `0x100` | `00264640` | **`0026ABA0`** |
| `+0x58` | `02098E68` | `0x40` | `00264D20` | `0026ADC0` |
| `+0x60` | `02098E70` | `0x20` | **`00264800`** | `0026AD10` |

plus `0026B730`, which writes `+0x48`'s element 0 with no index at all.

**The provenance matters more than the fix.** My inbox records a FABLE sweep listing
`0026ADC0`/`00264D20`, `0026AD10`, and `00264640`. That sweep never claimed to be exhaustive — it
listed what it found. I turned its *silence* into my *negative*, and published "no reader found"
about a function I had simply never looked for. **A peer's partial result is evidence of presence,
never of absence**, and converting one into the other is a way to manufacture an absence claim
without ever running an instrument. Neither of these went through
[the absence-claim gate](../../_index/ABSENCE-CLAIM-GATE.md), which would have demanded a positive
control and would have caught both.

### A defect worth reproducing deliberately

All six accessors guard with `cmp ecx, N` / `jge` — a **signed** compare. It rejects indices at or
above the bound and **admits negative ones**, which the following `movsxd` turns into a negative
displacement: a 2-byte read or write *before* the bank. The party-roster path above guards an index
of the same shape with an unsigned `ja` and is safe, so this is not the engine's house style — it is
two idioms, one of which is wrong.

A faithful reimplementation must copy the signed compare, because a caller passing `-1` today gets
defined-by-accident behaviour that some other code may depend on. It should copy it **knowingly**,
with the hazard recorded at the call site, which is what this section is for.

### What this does not change

The `+0x50`/`+0x68`/`+0x70`/`+0x78`/`+0x80` payload-section pointers in the same block are
unaffected: they are computed from the payload base at runtime, not from a `lea`, and their
arithmetic was read correctly. §18's correction also stands. What changed is three claims about the
two *static* defaults and one about who reads them.

## 22. The region map has a live control in two zone states, and what it does not cover (2026-09-11)

§19's first blocker was *"no runtime observation of anything in this family"*, and I filed
`OPUS-REQ-ASTRA-ACTORLIVE` because static reading could not clear it. ASTRA returned **EXP-026**
(commit `868396e`). This section integrates it, and is careful to integrate only what it shows.

**I checked the direction of the evidence before accepting it.** The predictions EXP-026 tested came
from §16 of this page — the per-sequence table at lines *"5, 6 → 0x6E0"* and *"7 → 0x668"*. So this
is a real test: the numbers were published first and the capture could have refuted them.

### What was observed

Two kind-3 actors, each resolved independently through the active `BattleUnit` **and** through
manager 0's pointer table, 40 samples each, before and after a Rabanastre boundary crossing:

| | Stepping | Eastgate | static prediction |
|---|---:|---:|---|
| sequence (`byte3 & 0x1F`) | 5 | 7 | — |
| record extent | `0x6E0` | `0x668` | §16, per sequence |
| `+0xB8` − base | `0x120` | `0x120` | `00266B5B` |
| `+0xC0` − base | `0x350` | `0x350` | `00266B62` `add rax, 0x230` |
| `+0xA0` − base | `0x4D8` | `0x4D8` | `00266B6F` `lea r8, [rax+0x188]` |
| `+0xA8` − base | `0x5A0` | `0x578` | `00266B8C`/`00266B93`, `0xC8` or `0xA0` |
| counts `+0x88`/`+0x89` | 8 / 10 | 6 / 8 | the same sub-byte branch |
| cursor `+0x11` | 7 | 5 | within 8 and 6 |

All 40 samples in each state match its column.

### Why the second state is worth more than a repeat

The two captures did not merely sample the same shape twice. **They exercised both arms of the one
branch that shapes the record**, and that branch is a single discriminator with three dependents:

```asm
00266B83  cmp     byte ptr [r9 + rax*4 + 0x1cec329], 1   ; rax = kind & 0x1F
00266B8C  mov     eax, 0xc8
00266B91  jne     0x266b98
00266B93  mov     eax, 0xa0
00266B98  add     rax, r8
00266B9B  mov     qword ptr [rdx + 0xa8], rax            ; wait array base
```

The **same** sub-byte selects `0xC8` or `0xA0` for the wait array's base *and* selects 8-or-6 for
`+0x88` *and* 10-or-8 for `+0x89`. Stepping landed on the `jne` arm (`0x5A0`, counts 8/10); Eastgate
landed on the other (`0x578`, counts 6/8). **Both arms now have a live control, and the three
dependent quantities moved together in each**, which is what a shared discriminator predicts and
what three independent fields would not do by coincidence.

### One thing the disassembly adds that the capture could not

Reading `00266AD0` whole for this integration turned up a **third** arm neither state sampled:

```asm
00266B36  xor     r8d, r8d
00266B40  mov     qword ptr [rdx + 0xc0], r8      ; NULL
```

**`+0xC0` is nullable.** On that arm the field is deliberately zeroed, so a consumer that assumes a
valid `secondaryContext` pointer is wrong for some kinds. The field was `UNRESOLVED`/`PROBABLE`
before this pass and is now named `secondaryContextPtr` at `SIGNATURE RESOLVED`/`HIGH` — named from
the static planter, corroborated live, and carrying its nullability. A reimplementation must
null-check it; EXP-026 would never have shown that, because neither actor it sampled took that arm.

### What EXP-026 explicitly does not establish, kept as ASTRA wrote it

- **`+0x60`..`+0x63` read `00 FF 00 00` in both states.** Unchanged bytes are not evidence of byte
  independence, free-list mutation, or recycling. The four-separate-bytes reading remains static.
- **No lifetime claim.** The address changed and the ordinal changed (9 → 74). That identifies two
  different storage selections; it does **not** show the old record was freed, and the old address
  was never read back. §20's absence claim is untouched by this.
- **No scheduling claim.** The cursor was in range in every sample, which says nothing about its
  intermediate values or about half-rate phase.
- 80 samples across **two states**, not 80 states. Reads are non-atomic; a matching frame counter
  does not make them a snapshot.

### Effect on the readiness verdict: narrowed, not cleared

§19 stays **not reconstruction-ready**, and blocker 1 is amended rather than struck. The honest
statement of it is now:

> The **layout** assumptions are runtime validated. The **behavioural** ones — free-list discipline,
> half-rate phase, and record lifetime — are not, and the instrument that would settle them is a
> trace over time rather than another paired capture.

This page's frontmatter stays at `SIGNATURE RESOLVED`. It is worth saying why, since the temptation
runs the other way: the charter's ladder puts `RUNTIME VALIDATED` above `BEHAVIORALLY UNDERSTOOD`,
and a document asserting a rung asserts every rung beneath it. Validating a *layout* does not make
the subsystem behaviourally understood, so claiming the rung here would assert something EXP-026
specifically declined to support.

*(A note for whoever next raises a document to that rung: `charter_grade_audit.py` currently hard-codes
`RUNTIME VALIDATED` as unmet for every document — `# nothing in the database reaches it`. That was
true when it was written. It is a tool change with a real trigger now, but not until some document
actually earns the rung, and this one does not.)*

## 23. Two identical banks, and only one of them is saved (2026-09-11)

§21 established that `ActorManagerSlot +0x58` and `+0x60` point at two 512-byte banks, `02099DF0`
and `02099FF0`, sitting `0x200` apart with the party roster `0x200` above them. They have the same
size, the same shape of accessor, and adjacent slots in the same structure. **They do not have the
same lifetime, and a reimplementation that treats them alike will corrupt saves.**

### The complete census, with a control

A stride-4 range scan over each whole bank, control `02098E10` (61 references, passing):

- `02099DF0`: **1 of 128** interior addresses referenced — only the base.
- `02099FF0`: **1 of 128** — only the base.

So no code anywhere in the image addresses either bank's interior. Everything that touches them
touches the base, and the complete list of those is twelve sites:

| | `+0x58` bank `02099DF0` | `+0x60` bank `02099FF0` |
|---|---|---|
| installed by | `0026CB26` (bind) | `0026CB31` (bind) |
| indexed accessors | `00264D20` get / `0026ADC0` set, bound `0x40` | `00264800` get / `0026AD10` set, bound `0x20` |
| `0026DB30` field transition | `0026DB73` — **unconditional** | `0026DC04`, `0026DC21` — **both gated** |
| `00268320` init state | `0026834C` — **unconditional** | `00268338` — **gated** on two dword tests |
| `00266D10` | `00267173` | `00267181` |
| `002695A0` | `002695C6` | **absent** |
| exported | **none found** | `0025D8E0`, 0x200 bytes |
| imported | **none found** | `00269A20`, 0x200 bytes |

### What the asymmetry means

**`+0x58`'s bank is scratch.** It is wiped unconditionally on every field transition and on
initialisation, and nothing ever copies it anywhere. Its contents cannot outlive a zone change.

**`+0x60`'s bank is saved state.** Every one of its wipes sits behind a guard — two dword tests at
`00268324`/`0026832D`, the `edi`/`ebx` comparison at `0026DBEB`, `test al, 8` at `0026DC1B` — and it
is copied out by `WorldPersistence_ExportGroupPersistentBank` and back in by
`WorldPersistence_ImportGroupPersistentBank`, whose callers include
`SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG`.

**`002695A0` is the cleanest single witness.** It clears `+0x58`'s bank and the party roster and
deliberately steps over `+0x60`'s. A function that wipes one of two adjacent identical banks is
choosing, and what it chooses to spare is the one that persists.

That the gating and the export/import agree is the point: **two independent instruments, one
pointing at clear-discipline and the other at copy-paths, separate the same two banks the same
way.** Neither alone would be worth much; together they are a lifetime distinction.

### For reconstruction

- `+0x58`'s bank may be a plain zero-initialised array reset at every transition.
- `+0x60`'s bank must round-trip through the save image byte-for-byte, **including the 448 bytes
  past its accessor's bound**, which no code reads but which the copy moves regardless. A
  reimplementation that allocates only the 64 addressable bytes writes a short record and breaks
  save compatibility in a way no gameplay test would surface.
- The two must not share an allocation or a reset path, however alike they look in a header.

### Limits

- **Where these land in the save image is not settled here.** `OPUS-CONTRA-GROUPBANK` disputes the
  save payload map's placement of the group banks, and until that is resolved this section claims
  only that the `+0x60` bank *is copied to and from the capture staging buffer*, not where.
- The census sees direct references. A bank base loaded into a register and passed through a call
  chain would be reached only through the slot field, and the slot field's own readers are the two
  accessors above — but a pointer copied out of a slot by some path not read here would be
  invisible to this instrument.
- What the bank's ~~`u16`~~ `int16` *(corrected 2026-10-02, OPUS: `003211C2` / `003211D7` / `003211EC` `movsx ecx, ax` on kinds 1–3, §24)* entries *mean* is still unknown for both. This section is about lifetime,
  not semantics.

## 24. The banks are operand storage, and there is a ten-kind get/set family over them (2026-09-11)

§21 recovered where the banks are and §23 how long they live. Neither said what they *hold*, and a
lifetime without a meaning cannot carry a contract. This section closes the structural half of that.

### One reader and one writer, each a ten-arm dispatch

The complete caller census of all seven bank accessors (control `002EF2B0`, **121 call sites in 70
distinct containing functions**, passing)
collapses to two functions. Every getter is called from `AiTargetSelector_ResolveOperandValue`
(`00321190`) and every setter from `00329E60`, at three consecutive sites each. Both are jump
tables over the same index space:

```asm
00321190  dec     ecx                 ; caller passes kind 1..10
0032119B  cmp     ecx, 9
0032119E  ja      0x32129b            ; -> *out = 0, return -1
003211A7  lea     rcx, [rip - 0x2011ae]         ; rcx = 0x00120000
003211AE  mov     eax, dword ptr [rcx + rax*4 + 0x2012ac]   ; table at 0x003212AC
003211B5  add     rax, rcx
003211B8  jmp     rax
```

The writer is the same shape with its table at `0x00329F40`. Both resolved against image base
`0x00120000` — the engine's self-relative convention again, now a seventh sighting.

| kind | read (`00321190`) | write (`00329E60`) | bound | notes |
|---:|---|---|---|---|
| 1 | `00264D20` | `0026ADC0` | 64 | **`+0x58` scratch bank** |
| 2 | `00264800` | `0026AD10` | 32 | **`+0x60` persistent bank** |
| 3 | `00264640` | `0026ABA0` | 256 | **`+0x48` bank** |
| 4 | `0046B240` | `0046B3F0` | — | write coerces to boolean |
| 5 | `0046B1A0` | `0046B290` | — | write coerces to boolean |
| 6 | `0046B180` | **error** | — | **read-only kind** |
| 7 | `0046B0D0` | **error** | — | **read-only kind** |
| 8 | `0032A920` | `0032ABE0` | — | write coerces to boolean |
| 9 | inline `0208D334` | inline `0208D334` | 16 | unsigned both ways |
| 10 | pointer arm | pointer arm | — | guarded on a non-null `rdx` |

So the three banks this page has been tracking are **operand kinds 1, 2 and 3 of a general operand
store**, and `AiTargetSelector_ResolveOperandValue` is the function that turns an authored operand
into a number. `gambit-evaluation-and-enmity.md` already places `00321190` on the gambit path.

### The elements are signed, and the proof is inside the same function

The bank rows said `uint16`. The getters return `movzx`, but that is only how a 16-bit value reaches
`eax`; what decides the type is the consumer:

```asm
003211BD  call    0x264d20
003211C2  movsx   ecx, ax          ; kind 1 - SIGN-extended
003211D7  movsx   ecx, ax          ; kind 2 - SIGN-extended
003211E9  movsx   ecx, ax          ; kind 3 - SIGN-extended
...
0032125C  movzx   ecx, word ptr [rcx + rax*2 + 0x1f6d334]   ; kind 9 - ZERO-extended
```

**Kind 9 is the positive control.** The same function, ten lines away, reads its own table with
`movzx` and writes it with `mov word` — unsigned in both directions. So the `movsx` on kinds 1–3 is
a deliberate distinction and not a compiler idiom, and the banks hold **`int16`**. A reimplementation
that stores them unsigned turns every negative operand into a number above 32767; a gambit condition
comparing against a negative threshold then silently inverts.

### Two failure conventions, and both report success where it matters least

| situation | reader | writer |
|---|---|---|
| kind outside 1..10 | `*out = 0` **and** returns `-1` | returns `-1`, no write |
| kind 6 or 7 | returns the value | returns `-1` — the kind is read-only |
| **index outside the bank** | **`*out = 0`, returns `0` — success** | **write dropped, returns `0` — success** |
| bank pointer null, or slot-0 gate clear | same as above: zero / dropped, success | same |

The third row is the one that matters. **An out-of-range index is not an error at this layer** — the
accessor returns early, the dispatch arm zeroes and reports success, and a caller that checks the
return value learns nothing. A reimplementation that raises on out-of-bounds, or that returns an
error code, changes behaviour authored content may depend on: an authored operand naming a
nonexistent index reads as `0` today, forever and silently.

The same is true of the gate. All seven accessors test bit 0 of the byte at `02098E20` — **slot 0's**
`+0x10`, not the slot being addressed — so before the first manager slot goes live every operand of
kinds 1–3 reads `0` and every write is discarded, with success reported throughout.

### What this answers, and what is not mine to close

`OPEN-QUESTIONS.md` **EE-9** asks who reads `u16` slot 3 of the 64-entry bank — the slot
`SpawnGroup_DispatchPendingCompletionSignals` posts the completed group number into at `00307063`.
The dispatch answers the structural half: **an authored operand of kind 1, index 3**, resolved
through `00321190` arm 1. Combined with §23, it also says that value is *scratch* — the kind-1 bank
is wiped unconditionally at every field transition, so a completed-group number does not survive
zoning, while a kind-2 operand would.

**EE-9 is not mine to close.** It belongs to the spawn/AI owners, and what remains of it — what the
gambit layer *does* with that operand, and the two dispatch blockers in `00233D20` — is semantic
work. Routed as `OPUS-REQ-FABLE-OPERAND` together with the `uint16` → `int16` correction to
`CONTRACT-group-completion-and-respawn.md`, whose accessor row states the element type this section
contradicts.

### Limits

- **Kinds 4–8 and 10 are named and not decoded.** Their targets are recorded above because the jump
  tables are decoded; what those functions read and write is not established here.
- The boolean coercion on kinds 4, 5 and 8 is read off `test r9d, r9d / setne dl` at the dispatch.
  It says the *argument* is narrowed to 0 or 1, not that the storage behind it is one bit.
- **What the bank entries mean individually is still unknown**, except index 3 of kind 1. This
  section establishes the access family, the element type and the failure ABI — the shape a contract
  needs — not the semantics of 352 individual slots.

## 25. The third bank is not a bank — it is a window into the save (2026-09-11)

§24 left one thing unresolved. Kinds 1 and 2 point at statics in `.data`; **kind 3's pointer is a
function return**, and a return value is not an address until somebody resolves it.

```asm
0026CAF8  call    0x2ef2b0                  ; SaveImage_GetPersistentPayloadBase
0026CAFD  mov     qword ptr [rdi + 0x48], rax

002EF2B4  call    0x2ef640                  ; SaveImage_GetActiveRuntimeBuffer
002EF2B9  add     rax, 0x200

002EF640  lea     rax, [rip + 0x1e74c39]    ; next instruction 002EF647
002EF647  ret
```

`0x002EF647 + 0x1E74C39 = 0x02164280` — **the save image base this database already recorded**,
reached here from an entirely different direction. So slot `+0x48` holds `0x02164480`, and its 256
`int16` entries occupy **save buffer `+0x200`–`+0x400`**, which is **payload `+0x000`–`+0x1FF`** in
the payload-relative coordinates the save payload map states.

A stride-4 range scan of that span (control `02164280`, 4 references, passing) finds **0 of 129**
addresses referenced. Nothing reaches those bytes except through this pointer and the three
accessors that read it.

### Three operand kinds, three different persistence models

This is the part that matters for reconstruction, and it is not guessable from the header — the
three fields are adjacent qwords that look identical:

| kind | slot | storage | how it persists |
|---:|---|---|---|
| 1 | `+0x58` | static `02099DF0` | **never.** Wiped unconditionally every field transition, no exporter |
| 2 | `+0x60` | static `02099FF0` | **by copy.** Exported and imported whole, into one of two save slots |
| 3 | `+0x48` | **inside the save image** | **by residence.** No copy step exists or is needed |

A kind-3 write lands directly in the in-memory save image. A kind-2 write lands in a static mirror
that only reaches the image when a capture runs. A kind-1 write reaches nothing that outlives the
zone. **Three adjacent pointer fields, three lifetimes, and the only way to tell them apart is to
resolve where each one points** — which is the whole argument of §21 restated in a case where
getting it wrong would silently destroy save data rather than merely mislabel a row.

### A naming hazard worth flagging

This page has been calling `02099DF0` and `02099FF0` "bank A" and "bank B". The save payload map
uses **"group bank A" and "group bank B" for something else**: the two *save-side slots*
(`+0xE040` and `+0x2E250`) that one static bank — kind 2's — alternates between, chosen by
`00236760`. Two pages, two A/B pairs, different referents. Prefer **"the kind-N bank"** across both.

### The payload map does not cover this region

The map's region table begins at payload `+0x1044`. **Payload `+0x000`–`+0x1FF` appears nowhere in
it**, although `SaveImage_GetPersistentPayloadBase` is listed among its seven seeds — the getter was
seeded and never resolved to a region. That is a complementary finding rather than a correction:
that page worked outward from the save side and this came from the consumer side, and they meet at
an offset neither could have named alone. **Routed as `OPUS-REQ-FABLE-PAYLOAD0`; their page is not
edited here.**

### Limits

- **What the 256 entries mean is unknown.** Their persistence, extent, element type and access path
  are established; their semantics are not, and 256 persistent `int16` in a save is exactly the
  shape a reader should be most careful about guessing at.
- The scan sees direct references. Another pointer to the same payload region obtained from a
  different getter would be invisible to it, though `002EF2B0`'s own callers are a bounded set.
- Whether payload `+0x000`–`+0x1FF` is *only* this bank is not established — the region is
  unreferenced apart from this path, which is consistent with the bank owning it exactly, and also
  with it owning part of a larger region nothing else has claimed yet.

## Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

Every §9 claim is a count over one body — `00266530 ActorStorage_InitializeRecord`, **1,439 bytes,
381 instructions** — so every one was re-derived from it.

### Confirmed exactly

| claim | measured |
|---|---|
| **the base register is the record throughout** | **exactly two writes to `rbx` in the whole body**: the load `0026656A mov rbx, [rdx + r10*8 + 8]` and the epilogue restore `00266AAE mov rbx, [rsp+0x60]` — precisely the two §9 names, and nothing else |
| `+0x00` is the slot index | ~~`0026656B mov word ptr [rbx], r10w`~~ `002665EB mov word ptr [rbx], r10w` *(corrected 2026-10-02, OPUS: `0026656B` is not an instruction boundary)* |
| the table is pointers with an 8-byte header | `[rdx + r10*8 + 8]`, the same instruction that loads the base |
| **eleven read-modify-write masks** | **eleven distinct mask constants** — `0x3C`, `0x04`, `0x400`, `0x7F`, `0x8F`, `0xDF`, `0xF0`, `0xFE`, `0xFFFFDEFF`, `0xFFFFFBFF`, `0xFFFFFFFB` |
| `003DBB60` called 4× | 4 |
| the body is 1,439 bytes | 1,439 |

> **The eleven is a count of distinct CONSTANTS, and the unit matters.** The same evidence gives
> **16** masking instructions, **9** offsets masked in place, or **12** offsets read-modify-written by
> any route. Only "distinct mask constants" gives eleven — which is what §2 lists, and it is right.
> Three plausible units, three different answers, one correct.

### Corrected: `0020E600` is called seven times, not six

§6 says *"called 6×"*. There are **seven** sites: `00266798`, `002667A9`, `00266903`, `00266976`,
`002669C5`, `00266A1F`, `00266A69`. Corrected in place.

### Open: "41 fields" needs its unit stated

§9 claims *"41 fields and their widths"*. Measuring stores through `rbx` gives **39 distinct offsets**
and **40 `(offset, width)` pairs** — the difference being `+0x10`, which is written both as a **byte**
(`inc byte ptr [rbx+0x10]`, three times) and as a **word**. Neither count is 41.

Since §9 also establishes — and this pass confirms — that the record lives *only* in `rbx`, a field
written through some other register would have to be reached by a `lea` handed to a callee, which the
enumeration would not see. **The claim is not refuted; its unit is unstated and neither reading
reproduces it.** Recorded here rather than adjusted, because guessing which of 39, 40 or 41 the author
meant would replace a checkable number with a chosen one.

**Not claimed:** ~~the record's true size stays `UNKNOWN` (`0x11C` remains a lower bound), and~~ *(answered: the size was settled later — "Records are 720 to 1,760 bytes, by kind"; 2026-10-02, OPUS)* no field's
meaning is established by this pass.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Core — SERVICE.** A cited function calls a 62-byte body labelled Core.
- **CoreRuntimeScheduling — CLIENT and SERVICE.** Cited functions are called by the 978-byte core start-up root and the 2,001-byte core frame body. They call three small core helpers (7, 27 and 61 bytes).
- **Presentation — CLIENT and SERVICE, 20 edges.** Cited functions are called by five Presentation bodies (963 to 4,782 bytes). They call small Presentation helpers (42 bytes twice, 59, 84 and 271 bytes) and `Actor_RefreshPresentationVisibility`.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Audio — SERVICE.** `00266D10` on this page calls `FUN_00362f70`, owned by that layer. What it reaches is a 516-byte audio-state initialiser: it clears the block from `022CBA70` to `022CBB70`, stamps the two id arrays that end at `022CBB70` with `0xFFFFFFFF` sentinels, and seeds the `0x7F`, `0x64` and 1.0 defaults; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Input — CLIENT.** `InputGameplay_ArbitrateDigitalInputAndModalState`, owned by that layer, calls `00236760` on this page. That caller is the input arbitration, in a `0x118`-byte frame with a stack cookie: it refreshes state only when `byte[02092750]` is not already **3**, and gives up early when the modal query answers non-zero; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**PlatformOnlineAchievements — CLIENT.** `FUN_00316480`, owned by that layer, calls `0046B180` on this page. That caller is a 289-byte walk of the achievement table at `[022C2550] + 8`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Story_Event_Quest_Hunt — CLIENT (13 edges through 2 of this page's functions).** The Story_Event_Quest_Hunt layer reaches this page at `002EF2B0`, `0026C8C0`. `PersistentFlag_QueryPrimaryOrAuthoredTable` is the worked example, read in full - it is the flag query whose id is masked to `0x3FFF` while **bit 14 selects between the primary and the authored table**; **6 of the 13 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Status_Periodic_Terminal — CLIENT, and this crossing arrived with today's `EH-4` narrowing.** `BattleUnit_RecoverFromTerminalStatusSetIfClear` (`00301140`, 452 B), owned by that layer, calls `BattleUnit_RefreshActorRuntimeFromDefinition` (`00238BF0`) — the function this page now cites as the writer of `+0x0E`'s low nibble and the caller of `00269FE0` and `00267CC0`. That caller is the recovery from a terminal status: it vetoes on `(dword[[unit+0x698]+0x64] | dword[[unit+0x698]+0x3C]) & 0x80000003` (`00301156`), and when `002E9600(actorRecord)` answers zero and unit flag bit 26 is clear it runs `00311F70`, then `00238BF0` (`0030118D`), then one more unit-side call **not named here, deliberately** — naming it would drag its own far end in and the guard refused exactly that on the first attempt — zeroes `+0x748` / `+0x770` / `+0x74C` / `+0xDCC`, clears `+0x788` bit 10 and `+0x6B0` bit 1, raises `+0x04` bit 21 and `+0x00` bit 30, writes `+0x74 = -1` and clears four status masks including the 64-bit `0xFFFFFFFDFFE7FFFD`. **The crossing is that the layer consults a function this page cites, not that this page owns anything in that layer** — `00238BF0` is `ActorEntity`'s. Read from the shipping bytes 2026-09-16 (FABLE), after `check_publish_neighbours.py` refused the publish for naming the far end without this sentence, which is the guard doing exactly what it was written for.

**UI — SERVICE.** `0026CE60` on this page calls `FUN_00253a30`, owned by that layer. What it reaches is a 67-byte teardown: eight calls in fixed order, `[020927C8]` and `[020927CC]` zeroed, and a tail-jump to a ninth; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Movement — CONSULTED BOTH DIRECTIONS (SWE2-EC7, batch 170, 138 edges).** The shared helpers this page's sweep and storage families cite - `001ED180`, `00226640`, `00237F40`, `00238B40` and the `00263FF0`/`00358940` ordinal walk the batch-170 `0035A590` release sweep rides - are also consulted by Movement-filed bodies (`0025DF00`, `0026C3E0`, `00263560` among them) while the actor records feed that layer's consumers in return - shared-helper fan-in, not a movement responsibility of this page.

**Script_VM_Native_Bridge — CLIENT (SWE2-EC7, batch 170, 179 edges).** The storage accessors this page cites (`001ED180`, `00236760` among them) are also called by bridge-filed bodies (`0034CF90`, `0034D790`, `0034E630`) - the script VM drives actor storage through the same helpers; fan-in on shared callees, no shared ownership.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**CombatAI — CLIENT (8 edges).** `AiTargetSelector_ResolveOperandValue` `00321190`, called by `AiOrder_EvaluateTargetSelector` `00301AD0`, calls seven of §24's operand-bank getters. They are the indexed getters `00264640`, `00264800` and `00264D20`, and the kind-4 to kind-7 getters `0046B240`, `0046B1A0`, `0046B180` and `0046B0D0`. §24's ten-arm reader is how a gambit condition reads an operand, so the AI layer is the reader of these banks and does not own them.

**Gameplay — SERVICE and CLIENT (5 edges).** Five single edges touch Gameplay. `00268530` calls `WorldActor_QueryCombatStanceState` `0030BFB0`, and `BattleUnit_DispatchActorPresentationEvent` `003299B0` calls the motion-bind clear `002EB030`. The recovery helper `00311F70` reads `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15`, and `BattleUnit_HandleActionTimelineEvent` `00325260` calls `003257D0`. The `stdmotionreadsync` poll `0034B8D0` reads `WorldActor_GetDefinitionByte12OrMinus1` `002E9C00`. These are battle-state queries and presentation events on either side of the record's motion-bind bit and stance, and the record is the object they read or stamp.

**Party — CLIENT and SERVICE (28 edges).** Eight record-side bodies read the focus getter `PartyFocus_GetCurrentPackedActorHandle` `003590D0`: `00263050`, `00263230`, `002681E0`, `0026C8C0`, `002C64C0`, `002E5180`, `00346FA0` and `00355830`. The unload `002628B0` calls `PartyFocus_ClearCurrentActorIfEligible` `00358B40` and `PartyControl_SetMovementSuppressionBit` `00359200`. `002695A0` and `WorldPersistence_ResetBanksForFieldTransition` `0026DB30` call `PartyFocus_ResetState` `003590E0`. §23's witness `002695A0` clears the `+0x58` bank and the party roster together. `0025C830` and `ActorSystem_InitializeManagerRuntime` `0026CE60` commit through `PartyFocus_CommitPendingPackedActorHandle_Thunk` `00358BB0`, and `00237F40` reads `BattleUnit_GetPartyLeader` `003272A0`. In the other direction, six party suppression and override setters call `Actor_StopRequestedMovement` `0026D6D0`, among them `PartyControl_SetSuppressionMask0Bit` `00359250` and `PartyFocus_SetTemporaryControlledActorOverride` `003593A0`. `PartyRoster_AssignActorToSlot` `00269C70` calls `002681E0`, and `PartyControl_ApplyAnalogLocomotionToActor` `00358CB0` calls `00264DF0`. `PartyFocus_ProcessActorControlPresentationState` `00358F90` calls `002E97B0`, `PartyFocus_TryGetCurrentActorWorldPosition` `00359150` calls `002E9FE0`, the `camerachange` verb `00351F40` reads `PartyRoster_IsFourSlotIndex` `002647C0`, and `0050C610` calls `00358BB0`. The party focus layer steers and suppresses actors that live in these records, and the record lifecycle (bind, unload, bank reset) clears or re-commits the party focus through that layer's own bodies.

**Resource — SERVICE (1 edge).** The unload `002628B0` calls `0032E520` (107 B, Resource, not read here) in its release chain. Releasing an area's actor pool hands resource-side state back to the resource layer. This page cites the chain and not that callee's behaviour.

**Save_Load_Settings and SaveLoad — CLIENT and SERVICE (37 edges).** §25 shows that the kind-3 bank is a window into the save. `SaveImage_GetPersistentPayloadBase` `002EF2B0` is `SaveImage_GetActiveRuntimeBuffer` `002EF640` plus `0x200`, and the page cites both. Eighteen save bodies call `002EF640`, among them `SaveRuntime_RebindImageBackedGameplayState` `00238A80`, `SaveWrite_PrepareAndSubmitFullImage` `0057E310`, `SaveImage_FinalizeHeaderAndChecksum` `00583D60` and `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` `00584210`. The bank getters and setters `0046B0D0` to `0046B3F0`, and the record bodies `002628B0`, `00268320`, `0026C8C0` and `0026DB30`, call `002EF2B0`. `00584210` calls `WorldPersistence_ImportGroupPersistentBank` `00269A20`, and `00266D10` calls `002EF2D0`. `SaveloadManager_ShouldAutosaveForTransition` `001C1720`, `SaveImage_CopyCaptureToWriteSubmissionBuffer` `002EF690` and `00583D60` read `00236760`, a one-bit getter that returns bit 12 of the battle-state block's `+4`. The SaveLoad-domain body `00280140` calls `00268320`, `002EF2B0` and `002EF640`. The save layer owns the image whose payload backs the kind-3 bank and the persistent group bank, so the record's banks are saved and restored by that layer's own capture, import and normalize bodies, and §23's asymmetry is what that layer chooses to save.

**Spawn_Encounter_Lifecycle — CLIENT and SERVICE (4 edges).** `SpawnGroup_DispatchPendingCompletionSignals` `00307030` calls `00233D20` and the kind-bank setter `0026ADC0`. `SpawnUnit_FinalizeSpawnEntryActivation` `0023A410` calls `BattleUnit_RefreshActorRuntimeFromDefinition` `00238BF0`, the writer of `+0x0E`'s low nibble. `BattleUnit_HandleReactionAnimationEvent` `003250F0` calls `SpawnGroup_MarkCompletionPendingAfterReaction` `00307110`. Spawn activation refreshes an actor's record from its definition, and group completion writes an operand bank. Both go through this page's writers.

**WorldAreaField and World — CLIENT and SERVICE (64 edges).** Twenty-three world-transition accessors read their state through `002EF2B0`, among them `WorldTransition_StageFieldTransition` `003145E0`, `WorldTransition_GetActiveOrPendingFieldId` `003148F0`, `WorldTransition_SetOptions` `00314DA0` and `WorldField_InitializeCurrentFieldRuntimeParameters` `0026D910`. The transition state lives in the same persistent payload that the kind-3 bank windows. `00229B40`, `003145E0` and `005843E0` call `002EF640`. The snapshot pair `WorldTransitionSnapshot_CapturePersistencePairForActiveSlot` `00584580` and `WorldTransitionSnapshot_RestorePersistencePairForActiveSlot` `005843E0` calls the bank export `0025D8E0`, the import `00269A20` and `00236760`. The field-entry body `00266D10` (World) calls `BattleSystem_InitializeAreaState` `002342F0`, `MapRef_BeginLoadResources` `00268750`, `WorldTransition_ResetState` `00314970`, `00377CC0`, `00263560` and `0026DB30`. `0026DB30` reads the transition getters `00314870`, `003148D0`, `003148F0` and `003149E0`, `World_UpdateSimulationTick` `00314020` calls `0025BFB0`, and `0026CE60` calls `002342F0`. The rest are predicate reads: `00237F40`, `00325090`, `003250F0` and `00325260` read `00313F60`, `0025C830` reads `00377C20`, and `00263230` and `00268D10` read `00377700`. `002628B0` calls `00378230`, `003DFA50` and `003EAA00`, `0046B3F0` reads `003148F0`, and `001ED180` reads `WorldTransition_GetTransitionFieldId` `00314910`. The World bodies `0025E400` and `002623A0` walk records through `ActorManager_GetRecordByOrdinal` `00358940` and `002E5180`. A field transition is what creates, resets and snapshots this record pool and its banks, so the world layer drives the record lifecycle, and the records share the save-backed payload with that layer's transition state.

## The `00265B60` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00265B60` ~~(~90 B)~~ (1,067 B) *(corrected 2026-10-02, OPUS: the body runs to the `ret` at `00265F8A`)* — `qword[rcx+0xC0]` null-gate then `byte[+0x29] &=
0xFC` (clears the low flag pair) on the sub-record (`00265B69`/
`00265B79`).

| member | role | interior |
| --- | --- | --- |
| `002E6090` (33 B) | safe `+0xC0` sub-record setter — null → ret; `byte[+0x14C] = dl`, `byte[+0x14D] = r8b` (`002E609C`/`002E60A9`) | [`002E609C`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## The `00265FF0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00265FF0` ~~(~97 B)~~ (1,339 B) *(corrected 2026-10-02, OPUS: the body runs to the 5-byte `jmp` at `00266526`)* — frame record op under a `rax = rsp` prologue.

| member | role | interior |
| --- | --- | --- |
| `0026AA60` | comiss sign-pick — `xmm3 < 0` loads `00915620`, else `01CEBC50` into `xmm4` (`0026AA66`/`0026AA6B`) | [`0026AA66`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## The `0032F1B0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`0032F1B0` (`ActorResource_FinalizeManagerRuntimeAfterLoads`, ~42 B) —
`movsxd rbx, ecx`, `ecx <= 0` out (`0032F1B6`/`0032F1BB`).

| member | role | interior |
| --- | --- | --- |
| `0037B290` | `ecx x10` index into `02EBF420 + 0x18` (80-byte stride records), non-null gate (`0037B290`/`0037B2A1`) | [`0037B290`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## Interior citation — frontier hub `003DBB60` (2026-09-17, SWE2-EC7)

`003DBB60` — 120 B, 10 A-measured callers at census; `ActorResource_SubmitRequestDescriptor`,
whose stack-record layout this page's table already spells out. Interior anchor only: the
kind remap (`r9-1`->0, `r9-2`->2, else keep with flag bit 0 set) lands at
[`003DBB7B`](../../_index/ADDRESS-INDEX.md)–`003DBB9D`, the nine-byte descriptor packs at
`003DBBA0`–`003DBBC9`, and `call 003DBCF0` at `003DBBCE` is the submit. Matches the documented
`{kind, 1, dl, r8w, 0x8000, flags}` layout field for field.

