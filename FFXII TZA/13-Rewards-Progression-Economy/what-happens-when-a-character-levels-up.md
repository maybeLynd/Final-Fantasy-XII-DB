---
system: What happens when a character levels up
category: 13-Rewards-Progression-Economy
status: AUDITED
owner_layer: CodeDomain — Battle stats
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 15 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  parent_tag: GN159
last_reviewed: 2026-09-13
registry_slots:
  - "0x02EBF108"
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-level-up-pass-1 - all 570 bytes re-read and every cited figure holds; CORRECTED: the result applier is NOT the silent path (its 0xFF byte is the target level and the caller skips the call, arg3 is a literal 0) and 0046A690 runs on the FINAL iteration gated by the record kind byte; NEW: all six growth calls are skipped when stats+5 is non-zero, r12 is the 'from' level passed to 0035D8C0 rather than only a flag, and the fourth caller is the console's 'Set level to max' (id 201) through 00305960, which levels every roster member to 99 through the ordinary path with the fanfare on
  crossref_clean: true
  reopened_count: 0
---

# What happens when a character levels up

`BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` (`0030C650`, 570 B) was on the *leaned on and never
opened* cut — three documents citing it, none reading it. Two of them stop at its door: the defeat
reward path hands it a target level, and the result applier hands it `+0x11C`/`+0x11D`.

**Extent checked**: 150 instructions, ends `ret` at `0030C889`, no `jmp` leaves the extent, one loop.

## 1. What the player sees

The level-up. **Every stat gain, the cap at 99, and the fanfare all come out of this one function**,
and it walks the character up **one level at a time** — a character who earns four levels from one
kill runs the growth arithmetic four times, not once.

## 2. Level is stored, and this function is its writer

The caller re-derives a *target* level from the experience total. **This function does not re-derive
anything** — it reads the stored level, increments it, and writes it back:

```asm
0030C7A7  movzx eax, byte ptr [rdi + 0x1c2]
0030C7B3  inc   eax
0030C7B5  cmp   eax, 0x63
0030C7B8  cmova eax, ecx                    ; ecx = 0x63
0030C7BB  mov   byte ptr [rdi + 0x1c2], al
```

> **`stats + 0x1C2` is the level, one byte, and it is the authority.** A concern raised before this
> read — that if this function also re-derived, "level" would be stored nowhere — **is settled: it is
> stored here, and nothing else in this function recomputes it.**

**That is the same `+0x1C2` the foe-stat formula reads** as the left half of its
`growth × (level − base) + base` term, so the byte this function writes is the byte that decides how
strong a foe is.

## 3. It cannot go down

Two independent guards make levelling monotonic:

```asm
0030C686  cmp  ecx, r14d       ; current vs target
0030C689  jge  return          ; already at or above -> do nothing at all
```

and the loop only ever `inc`s. **A target below the current level is not an error and not a
decrease — it is a no-op.** Nothing in this function can lower a level.

**The cap is 99 and it is applied twice**: once to the target on entry (`mov eax, 0x63` / `cmovg`) and
once to each increment (`cmp eax, 0x63` / `cmova`). **Belt and braces on the same constant.**

## 4. Stats are grown per level, not recomputed

Each iteration applies four growth calls, each taking a **growth byte from the character's own growth
record** — **but only when the record kind byte `stats + 5` is zero** (`0030C6D9`, §11); for any
other kind the whole growth block is skipped and only the level byte moves:

| stat field | width | growth call | growth byte |
|---|---|---|---|
| `stats + 0x08` | dword | `002F9A60(level, value, 0)` | table `02EBF108[level].hp` (u8) — see below |
| `stats + 0x0C` | word | `002F9B20(level, value, 0)` | table `02EBF108[level].mp` (u8) — see below |
| `stats + 0x10` | float | `002F9BD0(level, growth, 0, value)` | `record + 0x1F` |
| `stats + 0x14` | float | `002F9BD0` | `record + 0x22` |
| `stats + 0x18` | float | `002F9BD0` | `record + 0x25` |
| `stats + 0x1C` | float | `002F9BD0` | `record + 0x28` |

**Four of the six are floats sharing one growth function**, differing only by which byte of the record
they read — and the record bytes are `0x03` apart, so the growth parameters are a packed array.

The record is located by indexing an authored table:

```asm
0030C70B  mov   rcx, qword ptr [02EBF130]
0030C712  movzx ebp, word ptr [rcx + 8]      ; the stride
0030C716  movzx ecx, byte ptr [rdi + 4]      ; the character id
0030C71A  imul  ebp, ecx
0030C71D  add   ebp, eax                     ; + the resolved base
```

**`02EBF130` is classes 1 and 2 in the registry's class map**, indexed here by the character id at
`stats + 4` — so that slot is **the per-character growth table**, identified by a second consumer
rather than by this one alone.

**`BattleStats_RecomputeDerivedStateAndAutoStatuses` runs once, on the final level only**
(`lea eax, [r14-1]; cmp esi, eax; jne skip`). **The derived layer is not rebuilt per level** — a
four-level gain rebuilds it once, at the end.

## 5. The third argument is a silence flag

```asm
0030C660  mov  r13d, r8d
0030C663  shr  r13d, 1
0030C669  not  r13d
0030C676  and  r13d, 1        ; r13 = NOT bit 1 of arg3
...
0030C6A8  lea  eax, [r14 - 1]
0030C6AC  cmp  esi, eax
0030C6AE  jne  0x30c6b5
0030C6B0  mov  r12d, ecx      ; final level, and bit 1 clear -> notify
0030C6B5  or   r12d, 0xffffffff
0030C6C7  not  ebx
0030C6C9  shr  ebx, 0x1f      ; ebx = (r12 >= 0)
```

**`ebx` gates the entire notification block**, and it is set only when **bit 1 of the third argument is
clear** *and* the iteration is the last one. So:

- **Both known callers pass `0`**, so both notify — **the two callers do mean the same thing by it.**
- ~~**The applier's value comes from a byte that can be `-1`**, and `-1` has bit 1 **set** — so
  **that path is silent.**~~ **Wrong — corrected §11.** The `-1` byte is the applier's *second*
  argument (the target level), not the third: `003113E9` reads `byte [rbx+0x11D]`, **`cmp al, 0xFF`
  skips the call entirely**, and otherwise `movsx edx, al` passes it as the target while
  `xor r8d, r8d` passes **`0`**. **The applier notifies.** The flag's purpose — suppress the
  fanfare, not change the stats — stands, on the evidence of `0030C470`.
- **The notification fires once per call, on the final level** — a four-level gain plays one fanfare.

> ### CORRECTED 2026-09-10 — a third caller passes the silence flag
>
> The two callers read here pass `0`. The level grower `0030C470` (unnamed in the ledger;
> `0030C562`–`0030C56E`) — the function every unit initialisation runs — calls this
> function with **`2`**, bit 1 set, after zeroing `+0x1C2`: initial growth from level 0 to the
> authored level is silent. "Both known callers" stands for the two this page read; the flag's
> purpose (suppress the fanfare, not change the stats) is confirmed by the third.
> [The unit-definition page](../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md) §2.6.

## 6. The fanfare, and a join with the audio boundary

```asm
0030C831  mov  ecx, 7
0030C836  call 003A1180        ; -> (liveBank << 9) + 7; 7 is the BANK-LOCAL slot
0030C83B  cmp  eax, -1
0030C83E  je   skip
0030C840  mov  edx, 0x40       ; pan
0030C847  lea  r8d, [rdx+0x3f] ; = 0x7F, volume
0030C84B  call 002DF220
```

**These are the two audio-boundary functions read independently in
[`../18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md`](../18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md)**,
called with exactly the literals that document decodes: **`0x40` is centre pan** (the formula's
`pan − 0x40` yields offset 0) and **`0x7F` is full volume** (`clamp(v,0,127)/127 = 1.0`).

> **Two documents read hours apart by the same session, from opposite ends of the engine, meeting on one call
> site** — the audio document derived what `0x40` and `0x7F` mean from the mixer, and this function is a
> caller that passes exactly those values for a level-up. **Neither read informed the other.**

## 7. Modding notes

- **Level is one byte at `stats + 0x1C2`, capped at 99.** Writing it directly changes the level but
  **runs no growth arithmetic**, so stats will not follow.
- **Going up four levels applies growth four times** but rebuilds derived state once. **That is a
  correctness consequence, not just a performance one:** the six base stats are already at their new
  values while the derived layer still reflects the old ones, so **anything that reads derived state
  part-way through a multi-level gain sees an inconsistent character.** The window is inside one call,
  so only a hook or a callee reached from the growth functions can observe it.
- **Bit 1 of the third argument silences the level-up notification.** Stats are unaffected.
- **There is no path here that lowers a level.** A lower target is a no-op.

## 8. What is not known

- [x] **UQ-134.** ~~Which stats `+0x08`, `+0x0C`, `+0x10`, `+0x14`, `+0x18`, `+0x1C` are~~ **ANSWERED — the answer was
  already on [where a stat number comes from](../08-Combat-Formula/where-a-stat-number-comes-from.md) (`CB-12`, FABLE,
  2026-09-14) and never reached this box; propagated and re-read 2026-09-25 (FABLE, Claude Opus 5.5).** On a party
  record `+0x08` is **HP** and `+0x0C` **MP** (the HP and MP slots of `BattleStats_RebuildEffectiveStatsAndAffinityState`,
  `002FF078` / `002FF084`). The four floats are **Strength** (`+0x10`, `002FF0C2`), **Magick Power** (`+0x14`,
  `002FF0CD`), **Vitality** (`+0x18`, `002FF099`) and **Speed** (`+0x1C`, `002FF0B7`). They are converted with
  `cvttss2si`, clamped, and stored as the effective bytes 6, 7, 8 and 9 (`002FF840`–`002FF88E`), in that order.
  *(Original text: which stats they are; the note 2026-09-11 follows)* (note 2026-09-11: the four
  f32 at `+0x10`–`+0x1C` exist only for party records of type `0x1B`–`0x27`; a spawn-backed record
  holds eight i16 in the same bytes — [the field map](../08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md) §2.2). **Their widths, growth
      functions and growth-record bytes are read; their names are not.**
- [x] ~~What the two non-float growth functions (`002F9A60`, `002F9B20`) compute — neither takes a growth
      byte, so their curve is internal.~~ **Read 2026-09-11:** the curve is a table — registry slot
      `02EBF108` (`battle_pack.bin` directory `+0x28`), 99 rows of `{u8 hp, u8 mp}` indexed by the level
      (`002F9A9B`–`002F9AAF` with the row stride at `+8`; `002F9B6F` reads the second byte). Each
      function returns `value + b + trunc((rng mod trunc(b / 5 × 100)) / 100)` — the base `b` plus a
      random bonus below a fifth of it — when `b / 5 ≥ 0.01`, else `value + b` (`002F9AB2`–`002F9B0A`,
      constants `0.01`, `5`, `100` at `008F30E4`, `009146E4`, `008F3134`; the roll is
      `RNG_MT19937_NextU32_Thunk` `00379CD0`). The shipped rows: level 0 `10 / 3`, rising one HP per
      level to `20 / 4` at level 10, `28 / 5` at 30, `51 / 4` at 50, `23 / 3` at 70, `51 / 1` at 98.
- [x] **UQ-135 ANSWERED 2026-09-15 (OPUS) — both halves, and the first half's premise was
      backwards.**
      - **There is no “bank 7”. The `7` is the bank-LOCAL index.** `003A1180` returns
        **`(bankWord << 9) + ecx`** — `003A11D7`–`003A11DC` — so the argument is added to a
        base. **512 is the id-space STRIDE, not a slot count:** `.seb` gives each block a **128**-slot
        index ([seb-se-block-index.md](../18-Audio/Sound-Bank-And-Voice-Formats/seb-se-block-index.md) §3.4),
        so positions 128–511 of a block's id range are not addressable through it. `0030C831 mov ecx, 7` is therefore *slot 7 of whichever
        bank is live*, which is the same *bank-local index* vocabulary `UQ-149` already uses.
      - **The bank is runtime state, not a constant.** `003A1180` reads the packed handle at
        **`02AEF3FC`**, returns `-1` if it is `-1`, then **validates it**: the handle's low word
        indexes a **`0x18`-stride table at `02AEEDC0`**, and the entry's two words at `+8` and
        `+0xA` are rebuilt into a dword that must equal the handle with bit 31 cleared
        (`003A11AB`–`003A11D1`); it also rejects a negative low word. Only then is the id formed.
        [The shared-neighbours page](../00-Engine-Core-Runtime/Shared-State-Accessors/the-shared-neighbours-pass-22-keeps-finding.md)
        already reads `003A1180` as *“resolve the current packed handle → id”*, which is the same
        function seen from the other side.
      - ⚠ **§6's listing comment is corrected in this commit.** It read *“resolve a sound id in
        bank 7”*; it is slot 7 within the live bank.
      - **`0046A690` IS a second presentation hook, and it is a message rather than a sound.** The
        body (68 B) returns immediately on a null unit, builds a zeroed `0x38`-byte context, sets
        **`edx = 4`**, copies the unit's level byte **`+0x1C2`** into the context's `+0x1C`
        (`0046A6BF`–`0046A6C6`) and calls `0046AB10`. **That is one row of the documented poster
        family:**
        [the post-result events page](../07-Combat-Action/Post-Result-Events/the-post-result-events-and-the-battle-message-table.md)
        already lists `0046A690` → event `0x04` → *“… is now level {level}”*, with `ctx +0x1C`
        named as the unit's `+0x1C2`. Reading the body confirms both the event code and the field.
      - **What is still not static:** *which sound* slot 7 of the live bank is. The bank comes from
        a runtime handle, so the identity is authored data and a breakpoint question, not a byte
        one. **UQ-135.**
  **Corrected §11: it is called on the *final* iteration**, inside the `esi == r14-1` branch after
  the recompute, gated on the notify flag **and on `byte [rdi+5] == 0`** — not on non-final levels,
  and the gate is the record kind byte. Its only caller image-wide is this function.
- [x] **UQ-136.** What `002EACD0` does with `0x1` and `0x71`, between the level write and the sound —
  *narrowed §11*: it is called as `(unitId, 1, &unit[8], 0x71)`, returns 0 when the second
  argument is zero, and otherwise forwards to `003B02A0(unitId, &unitId, 1, 0x71, 5)`. ~~**What
  `003B02A0` does is not read.**~~

  **Narrowed 2026-09-25 (FABLE, Claude Opus 5.5): the call spawns presentation number `0x71` on the levelling unit,
  as a class-5 record that the battle-frame record driver plays.** Static; the bodies were read.
  - **The arguments.** `1` is a target count and `&unit[8]` the target list. `003B02A0` walks that many ids
    (`003B04F0`–`003B054F`). Each id must resolve to a live battle actor, a `0x740`-stride record under
    `022C6F28`, and each one that does is appended to the record's `+0x10` list, counted at `+0x372`. That is why
    a zero second argument returns without doing anything.
  - **The id.** `0x71` is a presentation number, stored at `+0x373` (`003B05AC`). The per-id byte table
    `01EFE260` flags `0x71`, and a flagged id skips the cap, under which an unflagged one is refused once two live counts sum to 24
    (`003B0371`–`003B0388`). So a level-up is
    always shown, however busy the battle is.
  - **The record.** A `0x3B0`-byte record of class 5: byte 0 is the class, the dword at `+4` a serial with the
    class in its top nibble, scale 1.0, colour `0x80808080`, and state `+0x370` = 2. It is bound to the loaded
    class-5 section found at `003B03FE` (`+0x340`), copied to the heap, and linked at the head of class list
    `020910F0[5]` (`0024B31F`–`0024B35A`). That is the class-chained registry `BI-11` asks about.
  - **Who plays it.** The battle-frame record driver described on
    [the world-tick page](../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md) steps
    these records by `+0x370`. It reads `+0x373` to index the section's entry table,
    `[+0x340] + 0x40 + id × 8` (`0024BC6A`–`0024BC7F`), and hands the id on (`0024BD30`, `0024BDAC`).
  - **The siblings.** The same wrapper is called with other numbers:
    - `0x7B` from the terminal-status recovery (`00301216`) and at `00239316`;
    - `0x82` and `0x86` from action-target processing (`00307749`, `0030777D`), and `0x84` at `0030838F`;
    - `0x76` and `0x0F` from periodic combat maintenance (`00311208`, `0031106B`), and `0x72` at `00317898`.

    So `0x71` is the level-up member of a family of battle system presentations.

  ~~*Still open:* which resource the class-5 section is, and what its entry `0x71` shows.~~ **The section is
  `c_all.efx` (same day, FABLE).** The only builder of a class-5 key-0 section is the effect-file loader `003B0660`
  (`003B0730`–`003B073A`), which loads resource kind 10, id 0. That is `effect_finish\jp\common\c_all.efx`,
  1,017,904 bytes, the only EFX that size, as
  [the EFX container page](../17-Presentation-Rendering/Effect-File-Formats/efx-and-efb-effect-containers.md)
  records for type 5. The section's `+0x40` block is a 256-slot table of `0xA0`-byte runtime objects, created per
  id on first use (`003A78C2`–`003A792C`). So `0x71` is the id the level-up asks the common effect pack for.
  ~~*Still open:* which of `c_all.efx`'s authored effects id `0x71` resolves to, and what it looks like on screen.~~
  **ANSWERED the same day (FABLE, Claude Opus 5.5): id `0x71` is the effect group at file offset `0x29A60` of
  `c_all.efx`.** Static reading plus a decode of the shipped file.
  - **How ids bind.** The EFX loader files each `0x600` chunk into the section's `+0x40` table under its byte `+0xD`
    (`003A79C0`, the store at `003A7A10`). `0x610` and `0x620` chunks attach to the effect named by their byte
    `+0xC`, through `003A7B50` (`003A7B6A`) and `003A77F0` (`003A7814`). `0x700` chunks go to a different table
    with keys 1–`0x30`.
  - **The decode.** The file's chunk stream, walked `{u32 length, u16 flag, u16 type}` from `+0x10`, ends
    exactly at the file size (2,800 chunks). Its 191 `0x600` chunks carry 191 distinct ids, `0x01`–`0xBF`.
  - **Effect `0x71`.** It is the `0x600` header at `0x29A60`, followed by two `0x610` and six `0x620` chunks, all
    keyed `0x71`, up to `0x29CEF`.
  - **The control.** All twenty ids the siblings use resolve the same way: `0x0F`, `0x72`–`0x76`, `0x7B`, `0x82`,
    `0x84`, `0x86`–`0x8D`, `0x95` and `0x96`. So the family is the numbered effect list of the common effect
    pack.

  *Not established:* what the group looks like on screen. That needs the `0x610` / `0x620` element fields read
  through the renderer, or a live capture.

## 9. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Level is a byte at `+0x1C2`, written by this function | `0030C7A7`–`0030C7BB`, read-inc-write | 1 |
| It cannot decrease | `0030C689` `jge return`, and the loop only `inc`s | 1 |
| Cap 99 applied twice | `0030C67A`/`cmovg` on the target, `0030C7B5`/`cmova` per increment | 1 |
| Six stat fields grown per level | the four growth calls at `0030C730`–`0030C7A2` with their stores | 1 |
| Growth record from `02EBF130` by character id | `0030C70B`–`0030C71D` | 1 |
| Derived state rebuilt once, on the final level | `0030C7C1`–`0030C7CE` guarded by `cmp esi, r14-1` | 1 |
| Arg 3 bit 1 gates the notification | `0030C660`–`0030C676` and the `ebx` gate at `0030C6C7` | 1 |
| The fanfare uses centre pan and full volume | `0030C840`/`0030C847` passing `0x40` / `0x7F` | 1 |

**Control.** The absence claim is *"nothing here lowers a level"*. The same reading positively finds
both the entry guard and the increment, and finds **no** `dec` or subtracting store to `+0x1C2` in the
body — so the zero is a measurement over a fully decoded function, not a search that found nothing.

## 10. Related

- [`experience-and-license-point-award.md`](experience-and-license-point-award.md) — the caller that
  derives the target level
- [`../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md`](../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md)
  — the class map that identifies `02EBF130`
- [`../18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md`](../18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md)
  — the pan and volume literals this function passes

## 11. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run on the addresses this pass introduced. Static only: all 570 bytes
re-read from the image, plus a rel32 caller census. Nothing executed.)*

### What reproduces

The extent (`ret` at `0030C889`, one loop, no `jmp` out); `+0x1C2` read-inc-write at
`0030C7A7`–`0030C7BB`; the entry guard `cmp ecx, r14d / jge`; the cap applied twice; the six growth
calls with record bytes `+0x1F`, `+0x22`, `+0x25`, `+0x28` three apart; `02EBF130` indexed by
`byte [rdi+4]` with the stride at `+8`; the recompute guarded by `cmp esi, r14-1`; and the fanfare's
`0x40` / `0x7F` into `002DF220`. **The absence claim holds too** — no `dec` and no subtracting store
to `+0x1C2` anywhere in the body.

### ✖ Corrected: the result applier is **not** the silent path

§5 reasons that the applier's `-1` byte has bit 1 set and is therefore silent. The call site says
otherwise:

```asm
003113E9  movzx eax, byte ptr [rbx + 0x11D]
003113F0  cmp   al, 0xFF
003113F2  je    0x311402          ; 0xFF -> the call is SKIPPED, not silenced
003113F4  movsx edx, al           ; arg2: the TARGET LEVEL
003113F7  xor   r8d, r8d          ; arg3: 0
003113FA  mov   rcx, rbp
003113FD  call  0x30C650
```

**The `-1` byte is argument two, not argument three.** `0xFF` makes the *caller* skip the call, and
what does reach the flag is a literal `0`, so **the applier notifies**. The defeat path `00312280`
also passes `0` (`0031249B`). The flag's meaning is unchanged — `0030C470` passes `2` and is silent,
exactly as the 2026-09-10 correction says — but one of the two paths §5 calls silent is not.

### ✖ Corrected: `0046A690` runs on the final iteration, gated by the record kind

§8 places it "on non-final levels when the unit is party-class". It is at `0030C7E1`, **inside** the
`cmp esi, r14-1 / jne` branch — the same branch as the recompute — and its guards are `test ebx, ebx`
(the notify flag) and **`cmp byte [rdi+5], 0`**. Final iteration, and the gate is the record kind
byte. `0046A690`'s only caller in the image is this function.

### ✔ New: growth is gated on the record kind byte, and the gate is the first thing in the loop

```asm
0030C6CC  cmp   byte ptr [rdi + 0x1C2], 0x63
0030C6D3  jae   0x30C85C          ; already 99 -> skip the whole body, keep counting
0030C6D9  cmp   byte ptr [rdi + 5], 0
0030C6DD  jne   0x30C7A7          ; not kind 0 -> skip ALL SIX growth calls
```

**For any record whose kind byte is not zero, levelling raises `+0x1C2` and grows nothing.** §1 says
*"every stat gain … comes out of this one function"*; that is true, and it is also true that for
non-kind-0 records this function produces none. It is the same `+5` byte the equipment and licence
pages use as the record kind, and it is what protects the layout note in §8: the four `f32` at
`+0x10`–`+0x1C` are only written for the kind that has them.

### ✔ New: `r12` is the "from" level, not only a flag

```asm
0030C806  movzx r8d, byte ptr [rdi + 0x1C2]   ; the new level
0030C80E  mov   edx, r12d                     ; the level this call started from
0030C811  mov   ecx, dword ptr [r15 + 8]      ; the unit id
0030C815  call  0x35D8C0
```

So the notification carries **(unit, from, to)**, and `-1` is both "silent" and an impossible level.
And "from" is the level at **entry**, not the previous iteration's: `0030C85C` restores `ecx` from
`[rsp+0x60]` — the value captured at `0030C67C` — before every re-entry, so a four-level gain reports
one step of four rather than four of one. `0035D8C0`'s only caller is this function.

**A transcription note.** §5's listing runs `mov r12d, ecx` straight into `or r12d, 0xFFFFFFFF`,
which as printed makes the notification impossible. The `jmp 0x30C6B9` at `0030C6B3` is missing, and
so is the loop back-edge `0030C865 → 0030C6A3` that re-enters the block each iteration. **The
conclusion is right; the listing does not support it.**

### ✔ New: a fourth caller — the console's *Set level to max*

`0030C650` has **four** callers, not the three §5 accounts for. The fourth is `00305960`, which walks
a roster at `[r14 + rsi*8]` and calls `0030C650(member, 0x63, 0)` — **target 99, notification on** —
for each member. Its only caller is `001D3ED0`, and that is
[console command **201, *"Set level to max:"***](../00-Engine-Core-Runtime/Developer-Tuning-Console/console-command-names.md).
The arm catalogue records id 201 as a boolean toggle *"preceded by two calls"*; **the two calls are
the command.**

> **The same shape as `Debug_SetGilToMaximum`** on
> [the gil page](gil-storage-clamp-and-every-path-that-moves-it.md): the console does not cheat
> around the system, it calls the ordinary path. So *Set level to max* runs the growth arithmetic
> once per level for every member and plays the fanfare, exactly as earning the levels would.

### ○ Small additions

`002EACD0` is called as `(unitId, 1, &unit[8], 0x71)` — `lea edx, [r9 - 0x70]` with `r9d = 0x71` is
where the `1` comes from — returns 0 when its second argument is zero, and otherwise forwards to
`003B02A0(unitId, &unitId, 1, 0x71, 5)`. §6 stops the fanfare at `002DF220`; two instructions later
the block ends `mov edx, eax / mov ecx, 1 / call 00329210`, with the voice handle `002DF220` returned.

**Not claimed.** What `0035D8C0`, `0046A690`, `003B02A0`, `00329210` or bank 7 do — **their bodies
were not read beyond their argument shapes.** Which stats the six fields are. Nothing was executed.

*Since answered in part (2026-09-29, FABLE, Claude Opus 5.5): the six growth calls write HP `+0x08`, MP `+0x0C` and the four
f32 base stats `+0x10`, `+0x14`, `+0x18`, `+0x1C` ([the level-advance contract](CONTRACT-level-advance-and-growth.md) §3, LU-5, LU-8).
In order they are the base Strength, Magick Power, Vitality and Speed: the stat rebuild stores them, capped at 99, at
`+0x2A`-`+0x2D` (`_index/candidates/exp-level-stats-fable/`, statmap.py; item E4 of
[`PKG-GP-EXP-LEVEL-UP`](../_index/completion-packages/PKG-GP-EXP-LEVEL-UP.md)).*

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL and recorded in the registry.*

- **Gameplay — CLIENT.** The level-rank function `0030C470` is also called by
  `DefinitionRuntime_ActivateAndApplyConfiguredSideEffects`, so activating a definition can level a character.
- **Movement — SERVICE and CLIENT.**
  - `002EACD0`, which the level-up path calls, is also called by the 68-byte stance-bit setter.
  - `BattleUnit_ProcessDefeatRewardsAndLoot` calls a 148-byte helper that resolves the party focus actor.
- **PlatformOnlineAchievements — SERVICE.** `BattleUnit_ProcessDefeatRewardsAndLoot` fires achievement counter 11 with
  the licence points, and counter 4 through its defeat wrapper
  ([the achievement catalogue](../20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md) AB-7).
- **Presentation — CLIENT and SERVICE (FABLE, Claude Opus 5.5, 2026-09-25, for UQ-136).**
  - **The level-up hands its visual to that layer.** `002EACD0` calls `003B02A0`, which builds the class-5 effect
    record through `0024B270`, whose own callees `003A72A0`, `003A8000` and `003A8900` belong to Presentation.
    `003B0660` loads `c_all.efx` through the EFX loader `003EDAD0`. The record driver `0024B9B0` calls
    Presentation's `003A74F0`, `003A7050`, `003A7300`, `003A7EE0` and `003A93F0`.
  - **Everything else is fan-in or a stub.** Presentation-owned screens (`002B7B80`, `002BAF80`, `00579420` and
    others) also call the shared widget helpers this page cites (`00244F00`, `00246AC0`, `00247870`, `00275440`,
    `0024A5A0`) and the folded stub `005C5230`.

  The level-up owns the request; Presentation owns the effect and its playback.

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CombatFormula — CLIENT and SERVICE, 62 edges.**
  - Cited functions are called by `BattleFormula_ApplyTargetResult` (3), `BattleStats_InitializeDefinitionRecord`, `BattleFormula_PrepareMagickPowerAttackVsDefense` and formula bodies of 120 and 219 bytes.
  - They call `BattleStats_GetByMappedBattleSlot` (2), `BattleStats_ReconcileResourcesToEffectiveCapacity`, `BattleStats_ReconcileCurrentHpToEffectiveMaximum` and `BattleStats_FindOwningBattleUnit`.
- **CoreRuntimeScheduling — CLIENT.** A cited function is called by a 255-byte boot-mode body and a 219-byte core body.
- **Status_Periodic_Terminal — CLIENT and SERVICE.** Cited functions are called by `BattleUnit_RecoverFromTerminalStatusSetIfClear`, `BattleUnit_RunPeriodicCombatMaintenance`, `BattleStats_ChangeStatusAndProcessSideEffects` and `BattleFormula_AdvanceStatusTimersAndBuildResult`. They call `BattleStats_RecomputeDerivedStateAndAutoStatuses` (2) and `BattleStats_RemoveStatusesFromMaskAndRecompute`.

- **UI — CLIENT (36 edges through `00273A20`).** `00279E20`, `0028F970`, `00290630`, `00290680` and
  32 more, owned by that layer, call `00273A20` — the 9-B accessor whose `== 1` results gate the
  level-up UI arms this page describes (`00290653`/`002906A7`). The crossing is the UI layer reading
  the same predicate for its display work; fan-in, not shared ownership. Read from `edges.tsv`
  2026-09-17 (SWE2-FRONTIER).

  `00279E20` (3,006 B) interior read, 2026-09-17 (SWE2-FRONTIER): the UI layer's level-up
  **arm dispatcher** — 46 outbound edges, dozens of arms each terminating in `jmp 0027A9B7`
  (the shared epilogue; CFG guard `00808C40` at `0027A9BE`). The `00273A20` predicate is
  re-polled inside the arms (`0027A7DB`); arms register per-event callbacks through
  `00245000` with `r8 =` the handler (`0027C870` at `0027A13E` — interior read 2026-09-17, SWE2-FRONTIER: 1,164 B, `001E0C10` first at [`0027C89B`](../_index/ADDRESS-INDEX.md), `0027B290` ×2 + `0027DCA0`), `0027AA70` at `0027A369`,
  `00276D30` at `0027A402`), bracketed by `00244960`/`00246AC0` pairs, and one arm reaches
  the `0028F800`/`00296B80`/`0028F970` sibling triple (`0027A3D0`/`0027A3D8`/`0027A3E2`).
  `005C5230` contract checks at `0027A5A7`/`0027A9B2`. Entry is entry-only — no inbound
  `edges.tsv` rows; reached indirectly (vtable/table dispatch), consistent with a UI
  command-table body.

  Two crossings the note above names: **Input — CLIENT (1 edge):** `001E0C10`, owned by that
  layer, calls `0027C870` — one of the callbacks `00279E20`'s arms register through
  `00245000`. **Save_Load_Settings — CLIENT (4 edges):** `SaveWrite_OperationStateCallback`,
  `SaveSlotScan_ControllerCallback`, `SaveStorageQueue_ControllerStateHandler` and one more
  call `00244960`, the bracket helper the dispatch arms pair around `00245000`. Both are
  far-end clients of helpers this page names; the crossing is the consult, not shared
  ownership. Read from `edges.tsv` 2026-09-17 (SWE2-FRONTIER).

**Resource — SERVICE (SWE2-EC7-168, 1 edge).** `00279E20` — the level-up layer's UI arm this
page measured — calls `0024A5A0` on the Resource layer. Consultation, not shared ownership.
Edge list from `edges.tsv`.

- **Script_VM_Native_Bridge — CLIENT (SWE2-EC7, 5 edges).** `002DF220` is also called by
  `00357040`, the `0036A100` pool allocator `00334000` uses by `0050D8F0`, and `00379CD0` by
  `00354BF0`/`00355140` plus one further native-bridge caller — the script layer fans into the
  helpers this page shares; the crossing is the consult, not a script relationship this page
  owns. Edge list from `edges.tsv`.
- **WorldAreaField — CLIENT and SERVICE (SWE2-EC7, 8 edges).** Cited bodies `00311B20`,
  `00312280` and `0031EB20` call the field-side helpers `00377C20`/`00313F60`, and `0036A100`
  is also called by `00267930` on that layer among four further edges — the field layer reads
  the same allocator and row-resolve helpers; fan-in, not ownership. Edge list from
  `edges.tsv`.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**Audio — SERVICE and CLIENT (7 edges).** The level-set `BattleStats_AdvanceLevelToTargetAndRecomputeGrowth` `0030C650` calls the sound-id resolver `003A1180` and the sound-play entry `002DF220` (section 6); `002DF220` calls the voice-request entry `001DBDB0` and is also called by `00249CA0`, `00271500` and `003A0E20`, and `00271500` also calls `003A1180`. The level-up fanfare is an ordinary audio request, bank-local slot 7 at centre pan and full volume, made through the audio boundary's two functions, which UI sound helpers and the spatial audio code call as well.

**CombatAI — CLIENT (1 edge).** `BattleMenu_BuildCommandEntryList` `0031EB20` calls `GambitConfig_ClassifyActionTargetPairCompatibility` `00327A10`. The command-list fill the level-up arms use through `0027AF80` also asks the gambit layer's action–target compatibility test; as the EC7-103 note says, the page owns no AI relationship.

**RNG_Random_Selection — SERVICE (2 edges).** The HP and MP growth functions `002F9A60` and `002F9B20` call `RNG_MT19937_NextU32_Thunk` `00379CD0`. The two non-float growth functions draw their per-level variation from the shared MT19937 stream.

**Spawn_Encounter_Lifecycle — CLIENT (1 edge).** `002398F0` calls the level grower `0030C470`. That spawn-filed body (read) resolves the unit, and unless bit 0 or bit 2 of the first byte of its `+0x6A0` record is set it draws a level between a base and base + range from the shared gameplay LCG and grows the unit to it through `0030C470`, the grower that makes the growth silent (flag 2, the CORRECTED box above).

## The `0035D8C0` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

`0035D8C0` — the from-level callee the growth loop passes `r12` into —
is a five-byte thunk tail-jumping to `002905D0` (`0035D8C0`). `002905D0`
(57 B) is a `[0209BE80]`-manager dispatch: the manager pointer loads
(`002905D7`, `00290610`, `00290634`, `00290688`, `002906B0`,
`002906D4`), `002966E0` runs the bounded match (`002905FA`),
`00273A20`'s `== 1` result gates (`00290653`/`002906A7`), and the tail
is `00296960` (`002906C5`).

| member | role | interior |
| --- | --- | --- |
| `002905D0` (57 B) | the dispatch body the thunk names — see above | [`002905FA`](../_index/ADDRESS-INDEX.md) |
| `002966E0` (384 B) | bounded match — `00299A30(rdi, ebx)` first (`00296702`), `dword[rcx]` vs `r15d` (`00296720`), `rdx` vs `3` bound (`00296730`) | [`00296720`](../_index/ADDRESS-INDEX.md) |
| `00299A30` (133 B) | three-field record match — `00273A20` `== 1` gate (`00299A67`–`00299A6C`), then `[rbx-0x2C]` / `[rbx]` / `[rbx+4]` compares vs `esi` (`00299A71`–`00299A7B`) | [`00299A71`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00273A20`, `00296960`. This is the
same `[0209BE80]` manager-verification family the `0030AF30` subtree's
`00290540`/`00296E00`/`00289F50` chain uses — the level-up path routes
through it to validate the growth target's record before applying.

## Interior citation — frontier hub `00273A20` (2026-09-17, SWE2-EC7)

`00273A20` — 9 B, 37 frontier callers at census; the null-pointer predicate this page already
describes as the `== 1` gate. Interior verified: the whole body is `xor eax,eax` / `cmp [rcx],rax`
/ [`00273A25`](../_index/ADDRESS-INDEX.md) `setne al` / `ret` — it answers "does this slot hold a
pointer", nothing more. No field walk, no dereference of the pointed-to object.

NOT claimed: what the pointed-to record is — the predicate is type-agnostic.


### Interior citation — frontier hub `00275440` (2026-09-18, SWE2-EC7)

`00275440` — 68 B, 14 callers (the `00276D30` notify path above). A
callback-chain walk: `[rcx+0x10]` is the head of a `{vfn, pad, next}` list; each
non-null `vfn` is invoked as `vfn(node, rdx)` at
[`0027546E`](../_index/ADDRESS-INDEX.md) and the walk continues through
`[node+0x10]`. The observer fan-out the level-up path publishes to.

### Interior citation — frontier hub `0028F970` (2026-09-18, SWE2-EC7)

`0028F970` — 112 B, 5 callers: the flag-reset arm of the `0028F800`/
`00296B80`/`0028F970` triple — requires bit `0x2000` of `[0209BE80]+0x10F68`,
clears bits `0x10` and `0x400`, zeroes word `+0x10FA0`, calls
`00273A20([0209BE78]+0xAB30)` at [`0028F9C4`](../_index/ADDRESS-INDEX.md),
and on success sets `+0x10CFC |= 0x40`.
## SWE2-EC7-23 update (2026-09-18) — `003C94F0` global reconcile arm

`003C94F0` (87 B) is the `[02B47730]` global reconcile arm the level-up/reward
callers reach: `byte[rax+0xC0] & 4` gate -> `0035BAF0` resolve, `[rax] &
0x8000` veto, `[rax+4] == [rax+8]` compare -> `jmp 003C93E0` continuation;
else `[rax+0xC8] = 0` — the state-reconcile the `0027xxxx` reward/UI callers
run before publishing. Interior anchor `003C9500` (the `+0xC0` flag test).

## SWE2-EC7-30 update (2026-09-18) — `0028F800` `+0x10F78` getter

`0028F800` (15 B) is the trivial end of the `0028F800`/`00296B80`/
`0028F970` sibling triple: it returns `[[0209BE80] + 0x10F78]` — the
bank object's sub-record pointer — with no null check on the bank
itself (the siblings add the guards). Interior anchor `0028F807`
(the `+0x10F78` load).

## SWE2-EC7-35 update (2026-09-19) - `0027AA70`

`0027AA70` (765 B) is a level-up fan body - `00915BB0` rdata, `02F9736A`/`01E0C2A4` state, four `00275440` plus `00249C60`/`00244F00`/`005C5230`/`00311CD0`/`002F9860`. Interior anchor `0027AACF` (a `00275440` call).

## SWE2-EC7-40 update (2026-09-19) - `0027DCA0`

`0027DCA0` (386 B) is a level-up body - `00247870` triple plus `001E0C10`/`0027B120`. Interior anchor `0027DCB8` (an `001E0C10` call).

## SWE2-EC7-43 update (2026-09-19) - `0027B290`

`0027B290` (279 B) is a call-free flag-masked delta accumulator - `r8d` selects masks 1/2/8 (and normalizes `edx` bits), then `movsx word[+4]` diffs along `[+0x60]` slot chains accumulate into `r11d`. Interior anchor `0027B2F1` (the first flag-test join).

## SWE2-EC7-56 update (2026-09-19) - `0027B120`

`0027B120` (222 B) is a call-free masked accumulator - `r11b` bit tests summing `word[+4]` deltas across `[rcx+0x60]`/`[r9+0x60]` chains. Interior anchor `0027B166` (the first `movsx` delta).


## SWE2-EC7-73 update (2026-09-19) - `003C93E0` verified singleton field write measured

`003C93E0` (61 B) is the `02B47730`-singleton `+0xC8` write: when the
singleton and `ecx` are both nonzero it runs `00273710()` and, only if
that gate passes, `0035BAD0()` - a result equal to `ecx` folds the
write back to 0 - then `[singleton+0xC8] = ebx`.
Interior anchor `003C9411` (the `+0xC8` store).

## SWE2-EC7-76 update (2026-09-19) - `00296B80` gated flag cleanup measured

`00296B80` (90 B) is the `+0xB4A` bit cleanup: bit 2 cleared first;
if bit 3 still stands, `00273A20(rcx+0xC0)` runs and a nonzero return
adds `00244F00(rcx+0xC0)`; then bit 3 is cleared - the level-up
family's gated teardown.
Interior anchor `00296B92` (the `and word [rcx+0xB4A]` mask).

## SWE2-EC7-95 update (2026-09-20) - `00311CD0` measured

`00311CD0` (26 B) is the five-argument trampoline `002778C0`,
`0027AA70` and `0027C3D0` call: it repacks `(rcx, edx, 0,
r8w, r9d-through-stack)` and falls into `00311B20` - the
argument-shuffle shim into the shared apply.
Interior anchor `00311CE0` (the `00311B20` call).

## SWE2-EC7-103 update (2026-09-20) - `0027AF80` measured

`0027AF80` (262 B) is the in-place filter-compact
`00276960` and `0027C870` call: `0031EB20` fills a
`0x1088`-byte stack record and returns a count
(negatives clamp to 0), then the `rsp + 0x70`
qword array is compacted in place - `ebp == 1`
gates `byte[+4]`-bit-1-clear entries on
`00273710`, every entry is masked by `002647E0`
against 4 (`ebp == 0`) or 1, survivors are copied
to the front of the same array, and the return is
`esi > 0` - the collect-and-count the level-up
arms run.
Interior anchor `0027B023` (the `002647E0`
call).

Cross-subsystem note: the `0031EB20` citation above
also reaches 1 CombatAI-layer callee (`00327A10` in
`edges.tsv`). `0031EB20` is a shared record-fill
consulted by both this layer and the CombatAI side -
the crossing is fan-in on one helper, not a CombatAI
relationship this page owns. (MECHANICAL,
SWE2-EC7-103, `edges.tsv`.)

`00276830` (301 B) is the mode publish `00279E20` calls: `(edx-0x10) <= 3` gates the four modes; each of the `[r8+0x60]` node's `+0x10`/`+0x18`/`+0x20`/`+0x28` records gets `byte[+0x39] = byte[[+0x20] + word[+0xA]*8 + 7] + (edx != mode_table[i])` against the `{0x10,0x11,0x14,0x15}` table, then `word[r8+0xC8] = r10w` - the level-up layer's four-record mode flag write.

Interior anchor `00276916` (function `00276830`).

`00333C80` (889 B) is the record-layout repack the level-up path runs on the party record: keyed on the global version word `01EFF3B0` it copies the 0xA0-byte record to a scratch frame and writes it back field-by-field under the version-9 layout (byte splits of the head qword, the `+0xA` byte string, bit merges at `+0x16`/`+0x17`, tail words `+0x18`..`+0x2A`) or the shifted version-8 layout, then folds the `+0xA` string's 0xB-capped length into the high nibble of `+0x16` and returns `r9 + 0xA0` - the converter that lets old-layout records ride the current shape.

Interior anchor `00333FC0` (function `00333C80`).

`00334000` (189 B) is the get-or-create slot primitive `003A77F0` runs against the record's `+0x2C` dword table: `edx` nonzero selects `rcx + edx*4` directly and wins only if its `0020E600` resolution stays live; `edx == 0` instead scans indices `0..0x1C` for the first dead slot - a found slot `0036A100`s a fresh `0x320`-byte record, `0020E620`-publishes the handle into `+0x2C`, `0046F330` initialises the record and `0046F290` binds it to the slot index; when all 29 slots are live it returns 0

Interior anchor `0033405C` (function `00334000`).

`0046F290` (160 B) is the 192-entry id-table refresh `00334000` runs: each dword slot at `[rsi+0x20]+i*4` resolves through `0020E600`, the result's `byte[+0]` indexes the slot's back-reference, a live entry frees through `003697F0` and re-seeds via `0020E620`, the head cell gets `0020E620(0)`, and `bp = 0xC0`/`r15b` stamp `+1`/`+0` on exit

Interior anchor `0046F2C2` (function `0046F290`).
