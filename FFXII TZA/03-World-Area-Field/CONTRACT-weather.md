---
contract: decide, commit and materialise which of a field's three weather slots is in force - the retention roll, the one-shot latch that runs it, the restore gate that can discard the result, and the split publication into gameplay and presentation
category: 03-World-Area-Field
scope: subsystem
level: L2
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 03-World-Area-Field/Weather/weather-slot-state-model.md, 03-World-Area-Field/Weather/weather-probability-and-transition-roll.md, 03-World-Area-Field/Weather/weather-apply-and-environment-materialization.md, 03-World-Area-Field/Weather/mweather-resource-format.md, 03-World-Area-Field/choosing-the-field-environment-variant.md
entries: ["002620E0", "0025ACA0", "0025ABA0", "002658B0", "0026D910", "002E3D40", "003777C0", "003565C0", "0026D8F0", "00265920"]
registry_slots: []
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: every body named in section 2 was disassembled from the authority image with
    disasm_fn.py on 2026-09-21 (OPUS) and is cited at interior addresses, not at its entry.
    The authored side was decoded from the shipped archive - map_ref.bin extracted from
    FFXII_TZA.vbf and decoded with the offsets the code itself uses. Nothing here is carried
    from a page without being re-read; where a page's claim did not survive the re-reading it
    is named in section 14 and filed in CONTRADICTIONS.tsv.
last_reviewed: 2026-09-21
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-29
  last_pass_state: opus-falsification-pass-1-2026-09-29-exe-73461d08
  crossref_clean: false
  reopened_count: 0
---

# Contract — the weather subsystem

> **Why this exists.** S-12 (weather) carried **no contract at all** — its L2 verdict read
> `NOT MET` with the contract cell as the binding gap. Four pages describe the parts
> ([slot state](Weather/weather-slot-state-model.md),
> [the roll](Weather/weather-probability-and-transition-roll.md),
> [the apply](Weather/weather-apply-and-environment-materialization.md),
> [the MWeather record](Weather/mweather-resource-format.md)) and a fifth
> ([the environment variant](choosing-the-field-environment-variant.md)) reads the same apply
> function from a different angle. What none of them states is what holds **across** those
> operations: which slot each published value is derived from, when the roll may run, and what
> the authored data can actually contain. Those are the invariants below, and two of them
> contradict what the pages say.
>
> **Provenance.** Everything in sections 2, 4, 7, 9, 10 and 12 is **NATIVE/STATIC** — read from the
> authority image on 2026-09-21. Section 8's populations are **authored-data** measurements over the
> shipped archive. Section 13 is **empty**: nothing here has been observed live.

## 1. Purpose

Every field area is in one of three weather configurations. Which one you get when you walk in is
decided once, by a retention roll against a per-slot probability the zone's own script authors; the
decision survives save and load, and a story script can override it. Weather is not cosmetic: the
same authored record that picks the sky also publishes the class the combat formula reads, so the
weather decides whether your Fire spells are weaker right now.

This contract specifies that whole path — decide, commit, materialise — as one operation with one
set of invariants.

## 2. Interface

The subsystem has **four entry points**, and they are not peers: one decides, one applies, one
arms, one reads.

| | |
|---|---|
| entry point(s) | `002620E0` field-runtime init core, 231 B — the only thing that runs the roll · `0025ACA0` the roll, 107 B · `0026D910` the apply, 418 B · `003565C0` the `setweatherslot` verb handler, 99 B · `0026D8F0` arm-restore, 21 B · `00265920` the canonical getter, 41 B |
| calling convention | Microsoft x64. `002620E0(rcx = ActorManager record)`; `0025ACA0()` takes nothing; `0026D910(ecx = slot, authored 1..3 domain)`; `00265920()` takes nothing; `003565C0(rcx, rdx = actor record, r8, r9 = VM stack)` — the standard result-class native signature. |
| parameters | `0026D910`'s `ecx` is the **requested** slot in the authored `1..3` domain. It is clamped, never validated: see I-2. |
| return type | `0026D910` has **no return value of its own** — it ends in `jmp 002E3D40` at `0026DAAD`, so the caller sees whatever the presentation refresh returns. `0025ACA0` likewise tail-jumps into it at `0025AD06`. `00265920` returns `int` in `1..3`. `002658B0` returns `int8` probability. |
| return semantics | `0025ABA0` returns the slot to switch to, in `1..3`, **and may return the slot it was asked to leave** (I-5). |
| callbacks / indirect dispatch | none on this path. `003565C0` is reached through the ScriptVM verb table as call id `0x021A`; the table is the dispatch, the handler is a direct body. |

## 3. Types

The subsystem owns **two persistent bytes, five published globals and one authored table shape**.
It declares no object of its own.

| offset | size | field | type | meaning | evidence |
|---|---|---|---|---|---|
| payload `+0x1060` | 1 | `currentWeatherSlot` | `s8` | the durable committed slot, **zero-based `0..2`** | written `0026D95E`, read `0026D96F`, `0026D9BB`, `0025ACC1`, `0026593B` |
| payload `+0x1061` | 1 | `bInitializationRestoreState` | `u8` | world-transition policy; gates the commit and is consumed by it | tested `0026D951`, cleared `0026DA92`, set `0026D8F9` |
| debug singleton `+0xAAC` | 4 | `debugWeatherSlotOverride` | `s32` | positive value forces the slot | `0017D490`, called at `0026D921`/`0026D92A`/`00265924` |

`payload` is the SaveImage persistent payload from `SaveImage_GetPersistentPayloadBase`
(`002EF2B0`, 20 B) — obtained **four separate times** inside one `0026D910` call
(`0026D94C`, `0026D959`, `0026D96A`, `0026D9AF`, `0026DA83`; five call sites, four of them before
the tail).

**The authored table: `map_ref.bin`, magic `MRF` + `02` (`4D 52 46 02` at `+0`).** Published at
`[02099D88]`, with `[02099D90]` as the "loaded" guard that `0026D910` (`0026D98F`, `0026D9CC`) and
`00264F10` (`00264F1C`) both test. Header offsets, each an image-relative `s32`:

| header | holds | shipped (`in` locale, 12,288 B) |
|---|---|---|
| `+0x00` | magic `MRF` + version byte `02` | — |
| `+0x04` | field-row array, stride 8 | `0x30`, **1,315 rows** |
| `+0x08` | 16-byte block array | `0x2948`, **93 blocks** |
| `+0x10` | dword count, then `u32[]` — the environment-class table | `0x2F18`, **16 entries**, values `{4,4,4,0,0,1,2,2,3,0,0,0,0,0,0,0}` |
| `+0x14` | dword count, then `u32[]` — not read by this subsystem | `0x2F5C`, 32 entries |
| `+0x18` | dword count, then `u8[]` — the boolean table | `0x2FE0`, **16 entries**, values `{0,0,0,1,1,0,0,0,0,1,0,0,0,0,0,0}` |
| `+0x0C`, `+0x1C` | zero in the shipped file; nothing reads them | — |
| `+0x20`–`+0x2F` | zero in the shipped file; nothing reads them. The row array begins at `+0x30`, so the header region is `0x30` bytes and half of it is unobserved | — |

```
map_ref field row (stride 8, indexed by field id)
  +0x00  u16  mweatherSelector     -> the MWeather table's selector; shipped range 1..775
  +0x02  s16  blockIndex           -> which 16-byte block; shipped range 0..92, never negative
  +0x04  s32  (not read by weather)

map_ref 16-byte block (stride 0x10, one per blockIndex)
  +0x00  u8[4]  lane 0   -- NEVER read by weather (the slot index is biased by +1)
  +0x04  u8[4]  lane for weather slot 1
  +0x08  u8[4]  lane for weather slot 2
  +0x0C  u8[4]  lane for weather slot 3
     lane +0  u8  environmentIndex   -> indexes BOTH the +0x10 and the +0x18 tables
     lane +1  u8  (not read by weather)
     lane +2  u8  -> published verbatim to 02099DB0
     lane +3  u8  (not read by weather)
```

**Total size is the file's own**; the layout above is complete for what this subsystem reads and
explicitly partial for what it does not. The block is **not allocated by this subsystem** — it is a
loaded file image, addressed through `ImageAddress_ResolveRuntimePointer` like every authored table
in this engine.

**The MWeather record** (`[02ADD0B0]`, published by `00378F70`) carries its selector count at `+6`
and its bits from `+8`; its per-entry layout is
[the MWeather page](Weather/mweather-resource-format.md) §4 and is not restated here. What **is**
restated, because it is an ABI fact and not a format fact, is I-4 below.

## 4. Preconditions · postconditions · invariants

**P-1 — the roll runs only from the primary ActorManager, once per field setup.** `002620E0`
returns immediately unless `dword[rcx+0x28] == 0` (`002620E6`), and skips its whole body when
`byte[rcx+0x10] & 4` is already set (`002620F3`). It sets that bit itself at `002621A4`.

**P-2 — but the latch does not skip everything.** When the init bit is already set, control jumps to
`002621A8`, which still runs `003601C0(0x0B)` and tail-jumps `003601C0(0x0C)` — **the two event
notifications fire on every pass, latched or not.** Only the non-primary-manager arm (`+0x28 != 0`)
returns having done nothing (`002621C1`). *This corrects "skips its whole body", which the F-2
answer on [the roll page](Weather/weather-probability-and-transition-roll.md) states.*

**I-1 — the authored and persisted slot domains differ by one, everywhere.** Authored/runtime is
`1..3`; persisted is `0..2`. Every crossing is an explicit `+1`/`-1` in the code
(`0026D933`, `00265942`, `0025ACC8`, `002658B8`, `0026DA04`, `0026DA2E`).

**I-2 — an out-of-range slot request never fails; it saturates.** `0026D910` computes
`slot-1` and clamps to `[0,2]` with `jns`/`cmovg` (`0026D936`–`0026D943`); `002658B0` does the
identical clamp (`002658B8`–`002658C8`). `setweatherslot(0)` and `setweatherslot(1)` both select
slot 1; `setweatherslot(9)` selects slot 3. **Nothing reports.** The verb handler clamps a second
time, to `1..3`, before it calls (`003565F6`–`00356609`).

**I-3 — the restore gate discards; it does not defer.** When `payload[0x1061] != 0` the requested
slot is thrown away at `0026D957` and the committed one kept. There is no queue, no retry and no
signal to the caller. The flag is then cleared at `0026DA92`, which sits on the **common tail** that
the resource bail-outs at `0026DA83` also reach — so it is consumed exactly once per apply, whether
or not the table lookup found anything.

**I-4 — the MWeather extractors take the slot in the authored `1..3` domain, and the conversion is
inside the bit arithmetic.** `003777C0(ecx = selector, edx = slot, r8d = bitOffset, r9d = width)`
forms `9 * (3*selector + slot)` (`003777DC`–`003777E9`) and then starts the bit walk at
`base + bitOffset + width - 10` (`003777F9`–`00377809`), decrementing. **That `-10` is a `-9` for the
slot bias and a `-1` for the MSB-first walk**: the effective entry index is `3*selector + slot - 1`,
and the field occupies bits `[9E + bitOffset, 9E + bitOffset + width - 1]` with the low bit first.
The shipped `gramap_weatherinfo.bin` is sized for `776 x 3` **zero-based** entries, which is the
reading this arithmetic produces and not the one a literal `3*selector + slot` would need.

**I-5 — only the selector is bounds-checked. The slot is not.** `003777C0` tests
`ecx < word[record+6]` (`003777D3`) and returns `0` on failure or on a null record (`00377849`).
**No test is applied to `edx`.** A slot of `0` would address the previous selector's last lane and a
slot of `4` the next selector's first; the clamps of I-2 are the only thing that prevents it, and
they live in the callers, not here.

**I-6 — the alternate resolver can return the slot it was asked to leave.** All three arms of
`0025ABA0` fall back to the current slot when no alternate has a non-zero probability: slot 2 at
~~`0025AC24`/`0025ABF0` via `edx=0`→`eax=2`~~ **`0025AC1D`/`0025ABF0`, via `setle cl`/`setg cl` and then
`lea eax, [rcx+1]`/`[rcx+2]`** *(CORRECTED 2026-09-29, falsification pass 1: `0025AC24` is not an instruction boundary.
It falls inside `0025AC20 mov rbx, [rsp+0x30]`, and the register is `ecx`, not `edx`)*, slot 1 at `0025AC88` with `ebx`
left at 1, slot 3 at `0025AC47` with `edi` left at 3. **`weatherProbability = {0,0,0}` therefore pins the weather
permanently** rather than forcing a change — which is the opposite of what "probability 0 → the
current slot cannot be retained" implies.

**I-7 — THE APPLY IS NOT SLOT-ATOMIC.** This is the subsystem's load-bearing invariant and it is a
*violated* one. Within one `0026D910` call the MWeather preset is extracted **twice, from two
different slots**:

- the **gameplay** class at `0026DA2C`–`0026DA31` calls `00377850(ebp = selector, edx = edi + 1)`,
  where `edi` is the **clamped requested** slot — the local, never re-read;
- the **presentation** path, reached by the tail jump, calls `00377850(edi = selector,
  edx = 00265920())` at `002E3D6E`–`002E3D79` — the **committed** slot.

When the restore gate of I-3 fires, those two differ, and the shipped consequence is concrete:
after a scripted `setweatherslot(3)` arms the flag, the next field-entry roll landing on slot 1
publishes **slot 1's combat weather under slot 3's sky**. On the ungated path the commit makes them
equal and the divergence is invisible, which is why it has not been noticed.

The `00180620` publication (`0026D976`) and the two authored-table lookups (`0026D9BB` onward) all
take the **committed** slot, so the gameplay element class is the only published value on the
requested side.

**Postcondition.** After any complete `0026D910`, `payload[0x1061] == 0`, `02099DA8`, `02099DAC`,
`02099DB0` and `02099DBC` have all been written on the full path (`02099DBC` twice — see S below),
and `0040AAD0` has been entered with the committed slot's preset, azimuth and elevation.

## 5. State

| | fields / globals | evidence |
|---|---|---|
| read | payload `+0x1060`, `+0x1061`; `[02099D88]` map_ref root; `[02099D90]` loaded guard; `[02ADD0B0]` MWeather root; debug `+0xAAC`; MT19937 state `02EB3870`/index `02EB4230`/init flag `02EB4234` | `0026D951`, `0026D96F`, `0026D9BB`, `0026D980`, `0026D98F`, `003777C4`, `00863C18` |
| written | payload `+0x1060` (gated), `+0x1061` (set `0026D8F9`, cleared `0026DA92`); `02099DA8` (`0026DA26`), `02099DAC` (`0026DA3C`/`0026DA4E`), `02099DB0` (`0026DA5B`), `02099DBC` (**zeroed `0026D946`, then written `0026DA7D`**); ActorManager `+0x10` bit 4 (`002621A4`) | as cited |
| allocated | **nothing.** No allocation occurs anywhere on this path. | complete bodies of `0026D910`, `0025ACA0`, `0025ABA0`, `002620E0` |
| deallocated | nothing | as above |

**Reader/writer census** (`globals_index.py`, whose blind spot is that it sees **RIP-relative
references only**; an indirect or computed access would not appear):

| global | writers | readers | what the reader is |
|---|---|---|---|
| `02099DA8` | `0026D910` only | `00263E10` (7 B) | reached via thunk `00321490` from `00301AD0` and the combat stage `0038B220` |
| `02099DAC` | `0026D910` only | `00263E20` (7 B) | thunk `003214A0`, from `003895D0`, `00389610`, `0038B220` |
| `02099DB0` | `0026D910` only | **none** | — |
| `02099DBC` | `0026D910` **and `0026AB40`** | `00264D50` (7 B) | from `002E9D90` |

**`02099DB0` is published and never read.** Two independent facts say so: no RIP-relative reader
exists, and the byte it carries — lane `+2` — is **`0` in all 279 authored lanes** of the shipped
table. It is inert in the shipped build by both routes.

> **2026-09-24 (SWE2-CONTRACT, GB-3 — resolved):** the publication is a **mirror block
> consumed field-by-field, and `02099DB0` is its one cell with no accessor.** The block
> `02099DA8`–`02099DBC` is written together by `0026D910` and read through dedicated 7-byte
> getter thunks — `00263E10` returns `02099DA8`, `00263E20` returns `02099DAC`, `00264D50`
> returns `02099DBC`, `02099DB4` is read by five `cmp` sites (`0026324D`, `00265450`,
> `00267605`, `0026778E`, `00268DDE`, `0026C4A2`, `0026C678`, `0026C6A9`, `0026E012`),
> `02099DB8` by `00264180`. Every cell has a reader **except `02099DB0`** — the full
> rip-relative census of `02099DA0`–`02099DBF` shows its only access is the `0026DA5B`
> store, and no wider access (qword/vector load spanning `02099DAC`/`02099DA8`) covers it.
> The non-RIP-relative blind spot is bounded too: the only pointer materialisations in the
> `02099Dxx` region are the bases `02099DE8` (a `test byte [base + idx>>3]` bitmap at
> `0025C10E`, domain `idx ≥ 0`) and the `02099DF0`/`02099FF0` scratch banks (script-slot
> `slot*4` forward indexing, slots 0..127) — reaching `02099DB0` would need a negative
> index outside every documented access domain, and no `lea` targets the block itself.
> So byte `+2`'s mirror cell is vestigial publication: it was laid out with the block but
> shipped code never reads it. Residual: a read through a pointer arriving by means other
> than a rip-relative `lea` (e.g. negative-offset arithmetic on a `02099DF0` pointer) is
> not statically excludable — the standard absence-claim caveat — but every pointer base
> in the region has a non-negative index domain.

**`0026AB40` corroborates `02099DBC`'s type.** That 14-byte body is
`eax = (ecx != 0); [02099DBC] = eax` — a boolean setter, which is exactly the domain the authored
`+0x18` table supplies (`{0,1}`).

## 6. Relationships

```
ActorManager_RunFieldRuntimePass 0025D9E0
  -> 002620E0   [gate: manager index 0, init bit 4 clear]
       -> 00259B30, 003E8980(0)                    ordering: both precede the roll
       -> 0025ACA0  the roll  -- tail --> 0026D910  the apply -- tail --> 002E3D40 -> 0040AAD0
       -> 0026FAD0(0,    committedSlot+1, managerIndex)     EFB channel 0
       -> 0026FAD0(0x1F, committedSlot+1, managerIndex)     EFB channel 0x1F
       -> 00379860(committedSlot+1) ; 00379290 ; 003DE920(0,1,0) ; 00363B40
       -> set init bit 4 at 002621A4
       -> 003601C0(0x0B) ; 003601C0(0x0C)          <-- also reached when latched (P-2)

ScriptVM verb 0x021A setweatherslot
  -> 003565C0  [three guards, then clamp 1..3]
       -> 0026D910(slot)     apply
       -> 0026D8F0()         arm the restore gate for the NEXT apply

boot: 0022A0B0 -> 00266D10 -> 0026D910(1) at 00266E74, then again at 00266E7B
```

Callees excluded as substrate: `ImageAddress_ResolveRuntimePointer` (`0020E600`, 815 callers across
18 owner subsystems — its census is in
[the apply page](Weather/weather-apply-and-environment-materialization.md)) and
`SaveImage_GetPersistentPayloadBase` (`002EF2B0`).

**Three re-reads of the debug override that a reimplementation must not cache.** `002620E0` calls
`0017D490` twice per post and does this three times (`0026210E`/`00262117`, `00262139`/`00262142`,
`00262167`/`00262170`); `0026D910` calls it twice (`0026D921`/`0026D92A`); `00265920` calls it
twice (`00265924`, then the tail jump at `00265931`); `0025ACA0` calls it twice
(`0025ACAA`/`0025ACB3`). **The test and the take are separate calls in every one of these.** They
agree in practice because `0017D490` is a 20-byte single-field accessor — but the call pattern is
part of the contract, and a cached value changes it.

## 7. State transitions

The durable state is one byte with three values; the transitions are the roll and the verb.

| previous | resulting | condition, and the exact test |
|---|---|---|
| slot *s* | slot *s* | `prob(s) >= 100` — `cmp edi, 0x64` / `jge` at `0025ACD8` |
| slot *s* | slot *s* | `1 <= prob(s) <= 99` **and** `roll < prob(s)` — `cmp rcx, rdi` / `jb` at `0025ACEC` |
| slot *s* | resolver(*s*) | `prob(s) == 0` (`test eax,eax`/`je` at `0025ACD4`) **or** `roll >= prob(s)` |
| slot *s* | slot *s* | resolver fell through: no alternate has non-zero probability (I-6) |
| slot *s* | clamp(*n*) | `setweatherslot(n)` — unconditional, bypasses the roll and the latch |
| slot *s* | slot *s* | **any apply while `+0x1061` is set** — the request is discarded (I-3) |

**`resolver(s)` in full** (`0025ABA0`, and this is where the pages are wrong):

| from | preference order | draws the RNG? |
|---|---|---|
| slot 1 | 2, then 3, then stay at 1 | **no** |
| slot 3 | 2, then 1, then stay at 3 | **no** |
| slot 2 | `roll < 50` → 3 then 1; `roll >= 50` → 1 then 3; then stay at 2 | **yes, before testing eligibility** |

The single `call 00379CD0` in the body is at `0025ABB8`, inside the `current == 2` arm only. *From
slot 1 or slot 3 the alternate is chosen deterministically even when both candidates are eligible —
slot 2 always wins.* The page's "draws MT19937 only when two remain" describes neither the
condition nor the arms.

## 8. Script · resource · event interactions

**The probability is authored per zone, in the zone's own script.** `002658B0` reads the loaded
script container at `[02098E10]`, guarded by `byte[02098E20] & 1` and by `word[container] >= 7`
(`002658CB`–`002658E9`), resolves the header cell at `+0x64` through `0020E600`
(`002658EB`–`002658EE`) and returns `signed byte[section + 1 + slotIndex]` (`00265900`). The
section is `count`-then-`u8[count]`, which is the high-level language's
`option weatherProbability = {100, 0, 0}`.

**If the script resource is unavailable the answer is 33** (`mov eax, 0x21` at `00265910`), for
every slot — so an unloaded zone rolls at a uniform 33 % retention and every slot is eligible.

**Verbs.** `0x021A setweatherslot` is the only one that reaches this machinery;
`0x2024 debug_setweather`, `0x209F debug_setlockweatherslot`, `0x03DD changeenvsoundweather` and
`0x040C getweatherslot` do not (F-2). **And `setweatherslot` is gated three ways before it applies**
(`003565D7`–`003565F4`): the singleton at `[02099D70]` must have `dword[+0x28] == 0` and
`byte[+0x12] != 0`, and `word[*(singleton) + 0x50]` must equal `word[actorRecord]` — the VM's arg1,
which is the resolved actor record the call executes on. **A script whose actor id is not the
field's own calls `setweatherslot` and nothing happens at all** — no apply, no arm, no report.

**Events.** `003601C0(0x0B)` and `003601C0(0x0C)` are posted at the end of every `002620E0` pass
(P-2). The EFB binding posts `0026FAD0(0, slot+1, …)` and `0026FAD0(0x1F, slot+1, …)` instantiate
the field's always-on layer and its weather-selective layer; the per-slot enable bytes are the EFB
row's `+7+value`, censused on [the roll page](Weather/weather-probability-and-transition-roll.md).

**Authored populations, measured from the shipped archive** (`map_ref.bin`, `in` and `ch` copies
**byte-identical**, sha256 `7c63552f…`; extracted from `FFXII_TZA.vbf` and decoded with the offsets
§3 lists):

| quantity | shipped |
|---|---|
| field rows | 1,315 |
| distinct MWeather selectors referenced | 531, range 1..775 |
| 16-byte blocks | 93 → **279 weather lanes** (93 × 3 slots) |
| lane `environmentIndex` histogram | `0`×163, `1`×64, `2`×19, `3`×7, `4`×4, `5`×1, `6`×2, `7`×2, `8`×16, `9`×1 |
| reachable `02099DA8` | `{0, 1, 2, 3, 4}` — **`4` for 246 of the 279 lanes** |
| reachable `02099DBC` | `{0, 1}` |
| lane `+2` (→`02099DB0`) | `0` in all 279 |

## 9. Determinism

**RNG — the gameplay MT19937, and nothing else.** `0025ACA0` and `0025ABA0` both call
`00379CD0` (`RNG_MT19937_NextU32_Thunk`, a 5-byte `jmp`) into `00863BF0`
(`RNG_MT19937_NextU32`, 141 B), whose state is `02EB3870` (624 dwords), index `02EB4230` and
initialised flag `02EB4234`. The tempering at `00863C54`–`00863C76` is MT19937's exactly — the
compiler pre-shifted the masks (`0xFF3A58AD << 7` for `0x9D2C5680`, `0xFFFFDF8C << 15` for
`0xEFC60000`), which is why a mask search for the standard constants misses it. **If the flag is
clear the generator lazily seeds itself with `0x1571` = 5489** (`00863C09`), the canonical MT19937
default — so a roll taken before anything seeds the stream is reproducible from that constant.

**Draws per decision: at most two, and usually zero or one.**

| case | draws |
|---|---|
| `prob >= 100` | **0** |
| `prob == 0`, current slot 1 or 3 | **0** |
| `prob == 0`, current slot 2 | **1** |
| `1..99`, retained | **1** |
| `1..99`, not retained, current 1 or 3 | **1** |
| `1..99`, not retained, current 2 | **2** |

**The scaling expression, with real constants and in evaluation order**, identical in both bodies:

```
u  = MT19937_NextU32()                     ; 0025ACDD / 0025ABB8
r  = (uint64(u) * 100) >> 32               ; 0025ACE4-0025ACE8 / 0025ABBF-0025ABC3  -> 0..99
retain  <=>  r <  prob                     ; 0025ACEC  cmp/jb
prefer3 <=>  r <  50                       ; 0025ABC7  cmp rcx, 0x32 / jb
```

The multiply-high form is *not* a modulo: it is uniform up to the `2^32 mod 100` residue, and a
reimplementation using `u % 100` will diverge on specific draws even with an identical stream.

**Timing / ordering.** The roll runs inside the field-runtime pass, after `00259B30` and
`003E8980(0)` and before the EFB posts, once per qualifying manager-record lifecycle. **There is no
weather timer**; weather does not drift while the player stands still.

**Threading.** Not established. No lock, no interlocked instruction and no thread identity check
appears in any body on this path — which is evidence about these bodies, not a proof that the caller
is single-threaded. Open question F-1 owns this.
*F-1 SUPERSEDED 2026-09-26 (FABLE, Claude Opus 5.5) under the runtime rule, because the static half is settled. Every in-image path to
`0026D910` starts at one of three application entries on the main-loop thread: GameApplication's setup, its update
slot (through `MainLoop_UpdateAndRenderFrame`), and the `setweatherslot` script verb. No thread procedure the image
starts reaches any of them, and the path takes no lock. Control: `_index/candidates/f1-weather-apply-thread/f1_thread_reach.py` (3 checks). The blind spot is the
handshake page's: indirect thread starts. The receiver-safe live call the row asks for is not queued.*

## 10. Failure paths and edge conditions

1. **MWeather record null or selector out of range** → `003777C0` returns `0` (`00377849`) → preset
   `0` → gameplay class `0` (`0026DA3C`). Indistinguishable from an authored preset of 0.
2. **map_ref root null, or the `[02099D90]` guard clear** → `0026D910` jumps to `0026DA83`,
   **skipping all four published globals** except the `02099DBC` pre-zero at `0026D946`. The flag is
   still cleared and the tail still runs. So a failed lookup leaves `02099DA8`/`02099DAC`/`02099DB0`
   holding the **previous field's** values while presentation is refreshed for the new one.
3. **Script container absent** → probability 33 for every slot (`00265910`).
4. **`environmentIndex >= 16`** → `0026DA1C`/`0026DA76` leave `edx`/`ebx` at `0` — a silent default.
   *Sharpened by pass 1:*
   - the guard is a **signed `jge` against each table's own count dword** (`cmp eax, [rcx]` / `cmp edx, [rcx]`),
     not a literal 16. The shipped count is 16;
   - the default is `ebx`, zeroed once at `0026D931` and not written again before `0026DA78`;
   - a patched table with a different count moves the bound with it.
   No shipped lane reaches it (§8), but block lane 0, which weather never reads, holds values up to
   24, so the guard is not vestigial.
5. **Out-of-range slot request** → saturates, silently (I-2).
6. **`setweatherslot` from a non-field actor** → returns having done nothing (§8).
7. **Restore gate set** → the request is discarded and I-7's divergence is live.

## 11. Observable behaviour

- The developer overlay prints `Weather Slot:%d (Triangle/Cross to toggle)` from the same
  `[singleton+0xAAC]` the override is read from.
- `payload+0x1060` is in the save image: save, reload, and the slot is unchanged.
- Combat damage is the sharpest external probe. With `02099DAC == 2` the combat stage
  `0038B220` applies the strong-wind multipliers; with `02099DA8` at `0`, `1`, `2` or `3` it applies
  the matching environmental ones, and **at `4` it applies none**, because every arm of that stage is
  an equality test (`test eax,eax` at `0038B2A8` and `0038B3F4`; `cmp eax, 2` at `0038B478`;
  `cmp eax, 1` at `0038B4FE`; `cmp eax, 3` at `0038B584`) with no default arm.
- **I-7 is externally observable and is the differential test this contract most wants run**:
  arm the restore gate with a scripted `setweatherslot`, then re-enter a field whose roll lands
  elsewhere, and compare the elemental multiplier in effect against the sky on screen.

## 12. Reproduction formula

```
apply(requested):                                 # 0026D910
    ovr = debugOverride()                         # 0017D490, called twice
    if ovr > 0: requested = debugOverride()
    req = clamp(requested - 1, 0, 2)              # saturating
    [02099DBC] = 0
    if payload[0x1061] == 0: payload[0x1060] = req
    committed = (int8)payload[0x1060]             # RE-READ, not req
    publishEnvironmentBank(committed)             # 00180620 -> 001A7E40
    field = activeFieldId()                       # 003148F0
    if mapRefRoot == 0 or mapRefLoaded == 0: goto tail
    row      = mapRefRoot + hdr[+4] + field*8
    selector = u16(row[+0])
    lane     = mapRefRoot + hdr[+8] + (s16(row[+2]) << 4) + (committed + 1)*4
    envIdx   = u8(lane[+0])
    A = mapRefRoot + hdr[+0x10]
    [02099DA8] = (envIdx < u32(A[0])) ? u32(A[4 + envIdx*4]) : 0
    preset = mweather(selector, req + 1, bit 0, width 3)        # <-- req, NOT committed
    [02099DAC] = (preset == 0) ? 0 : ((preset >= 4) ? 2 : 1)
    [02099DB0] = u8(lane[+2])
    B = mapRefRoot + hdr[+0x18]
    [02099DBC] = (envIdx < u32(B[0])) ? u8(B[4 + envIdx]) : 0
  tail:
    payload[0x1061] = 0
    return presentationRefresh(0,0,0,0)           # 002E3D40, a TAIL JUMP

mweather(selector, slot, bitOffset, width):       # 003777C0
    if record == 0 or selector >= u16(record[+6]): return 0
    p = 9*(3*selector + slot) + bitOffset + width - 10
    v = 0
    for i in range(width):                        # MSB first
        v = (v << 1) | ((record[8 + (p >> 3)] >> (p & 7)) & 1)
        p -= 1
    return v

roll():                                           # 0025ACA0
    s = (debugOverride() > 0) ? debugOverride() : payload[0x1060] + 1
    p = probability(s)                            # 002658B0
    if p == 0:            s = resolve(s)
    elif p < 100 and ((u64(mt()) * 100) >> 32) >= p: s = resolve(s)
    return apply(s)                               # TAIL JUMP

resolve(s):                                       # 0025ABA0
    if s == 1: return probability(2) > 0 ? 2 : (probability(3) > 0 ? 3 : 1)
    if s == 3: return probability(2) > 0 ? 2 : (probability(1) > 0 ? 1 : 3)
    if ((u64(mt()) * 100) >> 32) < 50:            # s == 2, the ONLY draw here
        return probability(3) > 0 ? 3 : (probability(1) > 0 ? 1 : 2)
    return probability(1) > 0 ? 1 : (probability(3) > 0 ? 3 : 2)

probability(s):                                   # 002658B0
    i = clamp(s - 1, 0, 2)
    if not scriptLoaded: return 33
    return (int8) section64[1 + i]
```

## 13. Runtime validation

**Empty. Nothing in this contract has been observed on a running game.** Every claim is static —
the shipping image and the shipped archive. That is what holds this contract at
`BEHAVIORALLY UNDERSTOOD` rather than `RUNTIME VALIDATED`, and it is what §16 routes.

| claim | how it was observed live | date | result |
|---|---|---|---|
| — | — | — | — |

## 14. Unresolved

Each of these is filed in `OPEN-QUESTIONS.md`; the first three are new with this contract.

1. **Is I-7's divergence a defect or a design?** The binary carries the divergence, not the reason.
   *Resolved by:* a live run that arms the gate and measures the multiplier against the sky — the
   probe §11 names. Routed to ASTRA.
2. **What does `02099DA8` = 4 mean?** It is what 246 of 279 authored lanes select and the one value
   the combat stage has no arm for. "No environmental element scaling" is what the code does with
   it; whether the designers had a name for it is not in the image. *Resolved by:* the authoring
   tool's vocabulary, if it is ever recovered — otherwise this stays a naming residue.
3. ~~**Why is `02099DB0` published?** Written by one function, read by none, and zero in every shipped
   lane. *Resolved by:* a non-RIP-relative reader, if one exists — `globals_index.py` cannot see one.~~
   **BOUNDED 2026-09-23 (SWE2-CONTRACT): it is a write-only dead global — no reader exists by any
   route form.** Whole-image census over all `.pdata` bodies plus raw data: exactly one accessor
   total — the store `mov dword [rip+0x1E2C34F], eax` at `0026DA5B`, inside `0026D910` itself.
   Zero rip-relative readers, zero immediate references, zero data-section qword slots, zero
   `lea`s. A fifth form is also negative: the image-base-relative idiom (`lea reg,[rip→0x120000]`
   + disp32 RVA — the form the recipe tables use) would leave the bytes of RVA `0x1F79DB0`
   anywhere in `.text`, and a raw byte scan finds none (sibling `0x1F79DA8` likewise). ~~(Sibling
   `02099DA8` has the same shape: one store, `0026DA26`, same body.)~~ *Corrected 2026-09-30
   (SWE2-CONTRACT, on SWE2-DATA's `DATA-REQ-CONTRACT-WEATHER-02099DA8-0930`): `02099DA8` is not the same
   shape. It has a reader, the 7-byte getter `00263E10`, as this contract's own §5 census row states; the
   store `0026DA26` is its one writer. Control: SWE2-DATA's `_index/candidates/dd-data-4-0930/pf_env_checks.py` E8
   (`4415dba48`), re-run identical in `_index/candidates/swe2contract-ddres-b6-0930/rerun_pf_env_checks.out`. The
   raw RVA scan's negative for `0x1F79DA8` stands: the getter reads it rip-relative.* "Published"
   is therefore the wrong frame: it is diagnostic residue — a value emitted for a consumer that
   was never shipped or was deleted. *Residual:* a reader that reaches the global through a
   pointer derived from something other than its own address is outside
   this census, and the design intent stays naming residue with item 2.
4. **F-1 — thread/frame requirements for calling `0026D910` safely.** Unchanged and still open.
   *2026-09-26 (FABLE, Claude Opus 5.5): the static half is settled and the row is SUPERSEDED; see the Threading paragraph.*
5. **D-4 — what the published direction basis physically is.** Owned by
   [the MWeather page](Weather/mweather-resource-format.md); narrowed, not answered.
6. **The designer's reason for the duplicate bootstrap apply.** Retired as an intent residue on
   [the apply page](Weather/weather-apply-and-environment-materialization.md); the mechanism is
   read and the reason is not a fact the binary carries.

## 15. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| The apply's full ordering, the gate and the tail jump | complete body of `0026D910` (418 B, `1703f5dc…b4d2`), disassembled 2026-09-21 | 1 | PROVEN |
| I-7 — two extractions, two slots | `0026DA2C`–`0026DA31` against `002E3D6E`–`002E3D79`; `edi` unmodified between `0026D943` and `0026DA2E` | 1 | PROVEN |
| I-4/I-5 — the `-10`, and the missing slot bound | complete body of `003777C0` (144 B, `a3688ce2…cd2e`); corroborated by `gramap_weatherinfo.bin`'s size, which fits 776×3 zero-based entries and not 1-based | 1 + data | PROVEN |
| The resolver's arms and its single draw site | complete body of `0025ABA0` (253 B, `e667fef7…ddd4`); the only `call 00379CD0` is at `0025ABB8` | 1 | PROVEN |
| I-6 — fallback to the current slot | `0025ABF0`, ~~`0025AC24`~~ `0025AC1D` (pass 1), `0025AC47`, `0025AC88` | 1 | PROVEN |
| The retention rule and the scaling expression | complete body of `0025ACA0` (107 B, `1b3c8438…c464`) | 1 | PROVEN |
| Probability read and the 33 default | complete body of `002658B0` (112 B, `9689942f…c8e7`) | 1 | PROVEN |
| P-1/P-2 — the latch, and what it does not skip | complete body of `002620E0` (231 B, `7605a770…182f`); `002620F7` targets `002621A8` | 1 | PROVEN |
| The presentation path takes the committed slot | complete body of `002E3D40` (116 B, `064ffe13…26f0`) | 1 | PROVEN |
| `setweatherslot`'s three guards and its own clamp | complete body of `003565C0` (99 B, `5819ab38…aa9a`); `002640C0` returns `[02099D70]` | 1 | PROVEN |
| The generator is the gameplay MT19937, lazily seeded 5489 | complete body of `00863BF0` (141 B, `b158ad91…3c2d`); tempering masks pre-shifted | 1 | PROVEN |
| map_ref layout, populations and reachable global values | `map_ref.bin` from the shipped `FFXII_TZA.vbf`, `in` and `ch` byte-identical (`7c63552f…`), decoded with the code's own header offsets | data (2026-09-21) | PROVEN |
| `02099DB0` has no reader; `02099DBC` has a second writer | `globals_index.py --addr`, RIP-relative only — a negative from it is bounded by that blind spot | 1 | VERY HIGH |
| `02099DB0` is a write-only dead global — one accessor total, the store | five-form census over all `.pdata` bodies + raw image 2026-09-23 (SWE2-CONTRACT): exactly one hit, the `mov dword [rip+0x1E2C34F], eax` store at `0026DA5B` in `0026D910`; zero rip-readers, zero immediates, zero data qwords, zero `lea`s, and zero `0x1F79DB0` disp32-RVA bytes in `.text` (the image-base-relative form); sibling `02099DA8` identical (one store, `0026DA26`). Residual: aliased access not derived from the global's own address | 1 (static) | PROVEN |
| The combat stage has no arm for `02099DA8` = 4 | `0038B2A8`, `0038B3F4`, `0038B478`, `0038B4FE`, `0038B584`, and `003214A0` arms at `0038B387`, `0038B609`, `0038B66E` | 1 | PROVEN |

**Superseded by this contract** — each also filed in `CONTRADICTIONS.tsv`:

- *Old:* `0025ABA0` "draws MT19937 only when two remain." *New:* it draws only when the current slot
  is **2**, and from 1 or 3 the choice is deterministic with slot 2 preferred.
- *Old:* `02099DA8` is a "global environment class **0..3**." *New:* the authored table supplies
  **0..4**, and 4 — the value with no combat arm — is what most lanes select.
- *Old:* the latch makes `002620E0` "skip its whole body." *New:* it skips to `002621A8` and the two
  event notifications still fire.

## 16. Parity plan

| dimension | tested how |
|---|---|
| **STRUCTURAL** | map_ref header and lane layout against the decoder in §12; the MWeather bit walk against `003777C0`'s own arithmetic |
| **CALCULATION** | the retention and preference expressions of §9 over an exhaustive `u` sweep — the multiply-high form is the specific thing to diff |
| **RNG** | draw *counts* per case (§9's table) as well as values; a reimplementation that draws once where the original draws twice desynchronises every later gameplay roll on the shared stream |
| **STATE-TRANSITION** | the table in §7, including the three fallback-to-current edges |
| **EDGE-CASE** | I-2's saturation, §10's seven paths, and I-5's unchecked slot |
| **CONTRACT** | I-7 specifically: assert the two extractions and compare their arguments |

**Not tested, and why:**

- **TIMING** and **INTEGRATION** — the frame phase and thread requirements are open (§14.4). A
  parity claim on ordering would assert what is not established.
- **PRESENTATION** — everything past `0040AAD0` belongs to
  [the MWeather page](Weather/mweather-resource-format.md) and to S-40/S-39, not to this contract.
- **SERIALIZATION** — the two payload bytes are covered by the save-image layout, which owns its own
  parity.
- **FULL SUBSYSTEM** — cannot be claimed while §13 is empty.

## Falsification pass 1 — 2026-09-29 (OPUS): every invariant holds; one citation was mid-instruction

Every claim was re-derived from the shipping image (`73461d08…`) and the shipped archive by
[`falsify_weather_contract.py`](../../Tools/analysis-kit/gfz-scripts/falsify_weather_contract.py). Each check states its
killer first. `audit_crossrefs.py` ran on this folder first.

| check | killer searched for | result |
|---|---|---|
| W0 §15 | an extent or body hash that differs | survives: all nine cited hashes (sha256 of the body bytes) and both small extents |
| W1 P-1/P-2 | a latched path that skips the two posts | survives: `002620F7` → `002621A8`, then `ecx=0xB` call and `ecx=0xC` tail jump |
| W2 I-1 | a cited crossing that is not ±1 | survives: all six |
| W3 I-2 | a failure branch in either clamp | survives: `jns`/`cmovg` in both; the verb clamps 1..3 again |
| W4 I-3 | the commit stored while the flag is set; a bail-out that skips the clear | survives: `jne` over `0026D95E`; four branches reach `0026DA83`, which falls through to the `0026DA92` clear |
| W5 I-4/I-5 | another index arithmetic; a compare on the slot | survives: `9·(3·sel+slot)`, then `+bitOffset + (width−1) − 9`; the only bound is `cmp ecx, word[+6]` / `jge` (signed). `gramap_weatherinfo.bin` is 2,628 B: 776×3 zero-based needs 2,627, one-based 2,629 |
| W6 I-6 / §7 | a second RNG call in the resolver; a fallback that changes slot | survives: one draw at `0025ABB8`; **citation corrected**: `0025AC24` → `0025AC1D` (see I-6) |
| W7 I-7 | `edi` rewritten before the gameplay extraction; presentation not taking `00265920()` | survives: no write to `edi` between the clamp and `0026DA2E`; presentation passes `00265920()`'s result |
| W8 §5 | another writer or reader of the four globals | survives, **whole-image**: every listed body decoded; writers and readers exactly as tabled; `02099DB0` unread |
| W9 §5 | an allocator call on the path | survives: none among 44 direct callees |
| W10 §7 | another retention test | survives: `test`/`je` at `0025ACD4`, `cmp edi, 0x64`/`jge`, `cmp rcx, rdi`/`jb` |
| W11 §8 | another default or container read | survives: `mov eax, 0x21`; `[02098E10]`, `[02098E20]`; `+0x64` |
| W12 §8 | a verb path that applies without the three guards | survives: `+0x28 == 0`, `+0x12 != 0`, the `+0x50` actor match |
| W13 §9 | another generator or scaling | survives: 5-byte thunk; seed `0x1571`; both pre-shifted masks; `imul 100` / `shr 32`; `cmp rcx, 0x32` |
| W14 §6 | a cached override read | survives: the separate test and take calls at every cited site; `0017D490` is 20 B |
| W15 §10.4 | a non-zero default | survives, **sharpened**: a signed `jge` against each table's own count; `ebx` zeroed once at `0026D931` |
| W16 §11 | a compare with 4, a computed jump, or a default arm in `0038B220` | survives: none |
| W17 §8 | any authored population differing | survives: `in`/`ch` byte-identical `7c63552f…`, 12,288 B; 1,315 rows, 93 blocks, 279 lanes; 531 selectors 1..775; both tables; the histogram; `02099DA8 = 4` on 246 lanes; lane `+2` zero in all 279 |

**My own checks were wrong five times before the page was.** W1, W5, W10 and W15 read the wrong neighbouring
instruction or the wrong branch form, and W8's first whole-`.text` sweep stopped at the first undecodable byte and
returned an empty census. None of those is recorded as a page defect. The one page defect is W6's citation.

**Crossref (audit_crossrefs, this folder): recorded rather than resolved.** Neighbour edges into 22 layers are reported.
- Almost all arrive through substrate that §6 names and excludes: `00379CD0`'s MT19937 callers (CombatFormula 54,
  Rewards 2, Status 1, CoreRuntime 1), `002EF2B0`'s payload callers (Story 12, Save 11, SaveLoad 1), and `003148F0`'s
  field-id callers.
- The rest reach this subsystem through the field-runtime pass (`0025D9E0`: ActorEntity 30, Movement 11) and the boot
  chain (`0022A0B0`).

`crossref_clean` stays `false`.

**Not attacked by this pass:**
- §8's EFB per-slot enable bytes (the roll page's census);
- the MWeather per-entry layout (its page);
- `0040AAD0` and everything past it.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

The weather chain (§6) runs through shared hubs. Its entry is the field runtime pass, its roll draws the
gameplay Mersenne stream, its apply publishes globals that combat code reads, and its state lives in the save
image. Every layer below reaches this page through one of those hubs.

**CombatFormula — SERVICE and shared state, 54 edges: the weather roll and the combat rolls draw one stream.** The roll
(`0025ACA0` / `0025ABA0`) calls `RNG_MT19937_NextU32_Thunk` (`00379CD0`), whose other 53 callers are combat formula
rolls: `BattleFormula_BuildCandidateStatusMask`, `BattleFormula_RollSpecialGuardOutcome`,
`BattleFormula_ComputeKnockbackChance`, `BattleFormula_RollKnockback` and more. Because the draws share the state at
`02EB3870`, a weather roll moves the position of every later combat draw (§9). The combat stage `0038B220`, one of the
readers of `02099DAC`, also calls `BattleStats_FindOwningBattleUnit`.

The same stream has callers in six more layers, each drawing it:
- **Status_Periodic_Terminal**, one edge: `BattleFormula_AdvanceStatusTimersAndBuildResult`;
- **Rewards_Progression_Economy**, two: `002F9A60` and `002F9B20`;
- **CombatAction**, two: `BattleUnit_TryTriggerNearbyAuthoredFieldAction` and `002FA740`, which also read the field id;
- **CoreRuntimeScheduling**, two: `0022B6E0` and `0022B7E0`;
- **Script_VM_Native_Bridge**, two: `00354BF0` and `00355140`.

**RNG_Random_Selection — SERVICE, five edges.** `RNG_MT19937_NextU32` (`00863BF0`) calls `RNG_MT19937_TwistState` and
`RNG_MT19937_SeedState`. The boot `0022A0B0` seeds it through `RNG_MT19937_Seed`, and the two roll bodies reach it
through the thunk.

**ActorEntity — CLIENT, 30 edges.**
- **The entry.** The chain starts inside `ActorManager_RunFieldRuntimePass` (`0025D9E0`), which also resolves actor
  handles and records (`ActorHandle_ResolveRegistryEntryByPackedId`, `ActorManager_GetRecordByOrdinal`, `0025B250`
  and more).
- **The target selector.** `AiOrder_EvaluateTargetSelector` (`00301AD0`), cited as a reader of `02099DA8` through
  the thunk `00321490`, walks the battle units (`BattleUnit_FindByDefinitionSelector`, `BattleUnit_GetBySlotIndex`,
  `BattleUnit_GetSlotCount`, `ActorWork_GetBattleUnit`).
- **Shared getters.** `SaveImage_GetPersistentPayloadBase` and `WorldTransition_GetActiveOrPendingFieldId` are
  also read by `ActorManager_BindLoadedDefinitionPayload`, `BattleSlotMap_InitializeMappingClasses` and the area
  unload `002628B0`.
- **The remaining edges.** `003DE920` is called from `ActorResource_FinalizeManagerRuntimeAfterLoads`. The boot
  calls `BattleStorage_InitializeWorkArrays`, and the area initialiser `00266D10` calls `003B6ED0`.

The actor-manager pages own the pass. This contract owns the weather step inside it.

**Script_VM_Native_Bridge — CLIENT, 26 edges.**
- The `setweatherslot` verb `003565C0` pops its slot and calls the arm and apply `0026D8F0` / `0026D910`.
- Script handlers also call:
  - the event notifier `003601C0`, from `00345140`, `003464D0`, `0034C370` and `003506A0`;
  - the `02099DBC` reader path `002E9D90`, from `0034B7C0`, `0034C210` and `0034CA40`;
  - the `02099DB8` reader `00264180`;
  - `00265920` and `002E3D40`;
  - the field-id getter and `MapRef_GetPrimaryFieldValue`;
  - `00265450`, the second `02099DBC` writer `0026AB40`, `0026FAD0` and `003DE920`.
- The area initialiser calls `VMNativeCommandDispatch_InitializeFamilyTables`.

The verbs are the script VM's.

**Presentation — CLIENT, 14 edges.**
- The apply's tail `002E3D40` → `0040AAD0` sets the environment preset, azimuth and elevation, and `0040AAD0` calls
  `0040B3B0` / `0040B430`.
- The boot loads motion tables (`AddMotion_LoadSkeletonMapping`, `AddMotion_LoadHighModelReplace`).
- The area initialiser calls `CameraSystem_InitializeRecords` and `003EB750`, and `CameraSystem_InitializeRecords`
  calls `00259B30`.
- `0026FAD0` calls `0026F470`, and `0046CC70` reaches `002E9D90`.
- The HUD-mask writers `002B7B80` / `002BAF80` read the field id.
- The selector calls `BattleUnit_TestActorViewFrustumAtCurrentPosition`.

**Audio — CLIENT, 13 edges.**
- The chain's step `00363B40` (run by `002620E0`) calls the audio bodies `002DF190`, `003636A0`, `00363840` and
  `00363E40`.
- `00265920` is also called by `002DE800` and `00361810`.
- The audio-filed `00261F90` reads the field pass, the field id and the persistent base.
- The area initialiser calls `00362F70`, and `00361460` calls the notifier.

The weather's sound belongs to the 18 pages.

**Save_Load_Settings and SaveLoad — DEPENDENCY, twelve edges: weather state lives in the save image.**
- The chain reads through `SaveImage_GetPersistentPayloadBase`:
  - the field pass;
  - `0025ACA0`, `002620E0` and `00265920`;
  - the arm `0026D8F0` and `WorldField_InitializeCurrentFieldRuntimeParameters` (`0026D910`);
  - the field-id getter.
- The field pass also asks `SaveWrite_GetBusyFlag`.
- `SaveImage_FinalizeHeaderAndChecksum` reads the field id.
- The area initialiser calls `002EF2D0`.
- The SaveLoad-filed `00280140` reads the persistent base.

**Story_Event_Quest_Hunt — MECHANICAL, twelve edges.** `SaveImage_GetPersistentPayloadBase` is the base every
persistent-flag query reads (`PersistentFlag_QueryPrimaryOrAuthoredThresholdGate`, `PersistentFlag_QueryBank2048`,
`PersistentFlag_QueryBank64A` / `64B` and more). The story pages own the flags.

**Movement — CLIENT, eleven edges.**
- The area initialiser calls `00263560`, `002EBE40` and `003DAE30`.
- The movement bodies `0033A720`, `003ED190` and `003ED3F0` read the field id.
- `003DE920` is reached from `00379080` / `00379110`.
- `00259B30` calls `00380D30`.
- The field pass calls `WorldActor_UpdateRuntimeAndScriptExecutionState`.
- `00379290` calls `0026E8D0`.

**CombatAI, CombatAction, Gameplay and Party — CLIENT, 23 edges through the selector and the field pass.**
- The selector `00301AD0` calls its usual gambit callees:
  - `AiOrder_ComputeBoundedSelectorScalar`, `BattleTarget_MatchesRelationMode` and the distance tests;
  - `BattleAction_GetSubtype3Field22OrFFFF`, `BattleTarget_ClassifyRelationshipClass` and the eligibility tests;
  - `BattleEncodedId_DispatchQueryMode0Value` and `BattleTargetBuffer_ResetPreservingFlag0`;
  - `BattleUnit_ResolveByFocusHandle`, `BattleUnit_GetPartyLeader` and `PartyFocus_IsCurrentPackedActorHandle`.

  The weather page cites it only as a reader of a weather global. Its gambit role is `CONTRACT-gambit-walk`'s.
- The field pass also calls `00234150` and `PartyFocus_GetCurrentPackedActorHandle`.
- `VMPartyCommand_RemoveSelector00To06_Async` calls the notifier.

**CoreRuntimeScheduling, Resource and Input — MECHANICAL, eleven edges through the boot.** The boot `0022A0B0` is cited
for the startup apply `00266D10` → `0026D910(1)`. Its other legs are:
- `0017D4C0` and `0022BDF0`, in the scheduling layer;
- the resource set-up bodies `00259DF0`, `002DF9A0`, `0032EAE0` and `00379D20`;
- the input fix-up `0035B270`.

The area initialiser also calls the input-filed `00226BE0`.

**UI, PlatformOnlineAchievements and Spawn_Encounter_Lifecycle — CLIENT, seven edges on one getter.**
`WorldTransition_GetActiveOrPendingFieldId` is also read by:
- the UI bodies `0029C530`, `003C5F00`, `003C80C0` and `003F92B0`;
- the achievements body `003160C0`;
- `SpawnKeep_RotatePersistenceBanksForAreaTransition`.

*Tier 2: ledger names, sizes and `edges.tsv`, roles as this page reads them; no new body read (OPUS, 2026-09-29,
pass-22 debt `42a617a9a`).*
