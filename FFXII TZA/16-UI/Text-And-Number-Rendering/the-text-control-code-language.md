---
system: The text control-code language
category: 16-UI
owner_layer: CodeDomain — Text and number rendering
status: AUDITED — every escape arm read and every field placed or shown write-only (UQ-177 answered 2026-09-18 with an archive census: `9` is authored by no shipped text, `#` bit 26 and `+`'s nibble are written and never read); the token units (UQ-178, four blanks and two column markers) answered 2026-09-17
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation delta - every function this document cites whose record differs between the stamped snapshot and GN161's gained a plate comment and tags ONLY (empty comment before, tag set a subset, checked field by field), and this document makes no uncorrected absence claim about any of them; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 2 cited address(es) among the 128 records changed across GN158..GN161; each differs only in comment and tags; 0 live absence claims (check_stranded_absence.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-DELTA-RELIANCE-BASIS; re-measured and applied for this document 2026-09-14 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708, on SNAPSHOT-IDENTITY - replaced rather than re-targeted because that basis is FALSE for this document, which cites a record that changed
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  parent_tag: GN159
last_reviewed: 2026-09-13
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-text-control-codes-pass-1 - everything structural reproduces to the entry: the 7,489-byte body and the next function at 002AE450, all three tables tiling exactly, all fifteen first-table arms with both shared groups, the seven callers at every published site, and the callee counts 19 / 7 / 4 and the parser family's 11 functions over 32 sites; CORRECTED: there are 34 distinct escape arms, not 32 - the page's own table lists 34, and the 35th table entry is 002ACFC2 repeated at indices 13 and 34 for the selectors 0 and _
  crossref_clean: false
  reopened_count: 0
---

# The text control-code language

`002AC5F0` is **7,489 bytes, the largest body in the executable that was still residual when the 158 were surveyed — classified at GN162 as `UI.Text.ControlCodeInterpreter`**, and
[`../../99-Unresolved-Residual/Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md`](../../99-Unresolved-Residual/Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md)
carries it in an open question phrased *"what `002AC5F0`, `002AAE40` and `002AF960` draw"*.

**It draws nothing.** It is the interpreter for the control codes embedded in the game's text, and
the reason it is the largest function is that it is the **only** implementation of that language —
every pass that walks a string calls this one function.

**Extents checked**: 7,489 B, 1,658 instructions, ends `002AE32C jmp 0x2acfe7` (into the shared
epilogue), 61 backward jumps, 2 indirect jumps, both jump tables decoded below.

## 1. What the player sees

Game text is not a plain string. A line of dialogue carries **codes inside it** — the ones that
change colour, insert an icon or a party member's name, pause, or start a new page. Every one of
those is a byte or two in the string, and this function is what turns them into an effect.

**The same interpreter runs during measurement as during drawing.** A line whose width is being
measured for a text box goes through exactly the same code path as the line being painted, so a code
that changes the layout is accounted for before anything is drawn.

## 2. Native mechanism

### 2.1 Signature and the loop it lives in

```asm
002AC625  mov   r14, rcx                  ; the caller's text context
002AC62B  mov   rdi, rdx                  ; a POINTER to the cursor (char **)
002AC63F  mov   r12, r8                   ; a float out-parameter
002AC61D  mov   qword ptr [rsp + 0x60], r9
002AC628  mov   dword ptr [r9], r15d      ; a second out-parameter, zeroed on entry
002AC642  mov   rcx, qword ptr [rdx]      ; cursor = *arg2
002AC645  movzx edx, byte ptr [rcx]       ; the byte under the cursor
002AC648  test  dl, dl
002AC64A  je    0x2ae31c                  ; NUL -> stop
```

**`002AC5F0(ctx, char **cursor, float *out, int *out2)`** — the cursor is passed **by reference**
because the function advances it past whatever it consumes.

**The return value is "call me again".** ~~All seven call sites use the identical shape:~~ Five of the seven call sites use this shape; `002B1FB0` and `002B5730` call once and read only the advanced cursor *(corrected 2026-10-02, OPUS: `002B1FB0+0xCE`, `002B5730+0xF3`; no `test eax` follows)*:

```asm
call  0x2ac5f0
test  eax, eax
je    <stop>
```

`002ACFC2 mov eax, 1` is the consumed-a-code exit; `002AC6CA xor eax, eax` and the NUL path at
`002AE32A` are the stop exits. **So a caller loops on it, and drops out when the cursor reaches an
ordinary character or the end of the string.**

### 2.2 One byte selects among fifteen token kinds

```asm
002AC67F  movzx eax, dl
002AC682  dec   eax
002AC694  cmp   eax, 0xe
002AC697  ja    0x2ac6ca                  ; >= 0x10: an ordinary character -> return 0
002AC69B  lea   rsi, [rip - 0x18c6a2]     ; rsi = 00120000, the image base
002AC6A2  mov   eax, dword ptr [rsi + rax*4 + 0x18e334]
002AC6A9  add   rax, rsi
002AC6AC  jmp   rax
```

**Bytes `0x01`–`0x0F` are control tokens**; everything from `0x10` up is text. The table is 15
dwords at `002AE334`.

| byte | arm | note |
|---|---|---|
| `0x01`, `0x04`, `0x06`, `0x07` | `002ACB96` | four codes share one arm |
| `0x02` | `002AC6D1` | measures: calls `002B2150`, `002B1F20`, `002B2C50`, writes floats to the out-parameter |
| `0x03` | `002AC6AE` | advances one byte, clears `painter + 0x10FC`, calls the font API with `0`, **returns 0** |
| `0x05` | `002ACCF3` | |
| `0x08` | `002AD011` | advances the cursor by **3** |
| `0x09` | `002AD008` | advances the cursor by **1** |
| `0x0A` | `002ACE25` | |
| `0x0B`, `0x0C`, `0x0D` | `002AC6CA` | **the ordinary-character arm — these three are not codes** |
| `0x0E` | `002AC825` | |
| `0x0F` | `002AD01A` | **the escape prefix** — see 2.3 |

**`0x03` does work and still returns 0**, so it is a code that both acts and ends the run.

### 2.3 `0x0F` introduces a two-byte escape, and the second byte is ASCII

```asm
002AD01A  inc   rcx
002AD01D  mov   qword ptr [rdi], rcx      ; step past the 0x0F
002AD020  movzx ebx, byte ptr [rcx]
002AD023  lea   eax, [rbx - 0x20]
002AD026  cmp   eax, 0x50
002AD029  ja    0x2acfc2                  ; outside 0x20..0x70 -> consume and continue   <- corrected 2026-10-02, OPUS - not consumed: the cursor already points at the selector byte (002AC5F0+0xA2A), so the caller prints it
002AD02D  movzx eax, byte ptr [rsi + rax + 0x18e3fc]   ; case index, 0x51 bytes at 002AE3FC
002AD035  mov   edx, dword ptr [rsi + rax*4 + 0x18e370] ; 35 targets at 002AE370
002AD03F  jmp   rdx
```

**The selector byte is printable ASCII, `0x20` to `0x70`**, which is why the codes are writable in an
authoring tool as `0x0F` followed by a letter.

**The three tables tile exactly**: `002AE334` + 15×4 = `002AE370`; + 35×4 = `002AE3FC`; + 0x51 =
`002AE44D`, immediately before the next function at `002AE450`. **That the three lengths implied by
three separate `cmp` bounds fit end to end with no gap is the check that they were read correctly.**

**Disposition of the `verify_doc_addresses` review flag.** `002AE334`, `002AE370`, `002AE3FC` and
`002AE44D` are `.text` addresses that are not function entries. They are this function's trailing
switch data: the body ends at `002AE32F` (`002AE32C jmp` is its last instruction), the tables begin
two bytes later and run to `002AE44D`, and `002AE450` is the next function. **The tiling above is the
confirmation the gate asks for** — each base is reached by a `lea`/`mov` pair inside the function,
and each length is fixed by a `cmp` bound in the same basic block.

### 2.4 Every arm has the same three lines, and they are what makes the codes variable-length

```asm
002AE308  lea   rdx, [rsp + 0x40]        ; a small buffer for the code's payload
002AE30D  call  0x3ffab0                 ; parse it; returns a BYTE COUNT
002AE312  mov   eax, eax                 ; zero-extend
002AE314  add   qword ptr [rdi], rax     ; advance the cursor by that many bytes
002AE317  jmp   0x2acfc2                 ; return 1
```

**The parser returns how far to advance**, so the interpreter itself never needs to know how long a
code is. `003FFAB0` is called **19 times** — the most-called callee — and it belongs to a family of
**11 functions in the band `003FFAB0`–`003FFF10`, 32 call sites in total**, all reached this way.

Three sampled arms show the variation: `'m'` and `'n'` use `003FFB90` with two zero arguments,
`'l'` uses `003FFCE0` with five, and the `0x20` arm parses and then treats the payload byte as a
number — `002AD062 movsx eax, al`, `002AD069 cvtdq2ps`, `002AD06C divss` against a constant —
**a numeric parameter scaled into a float.**

### 2.5 The escape catalogue

**Thirty-four** distinct arms — the table below lists thirty-four, and the count here said thirty-two (corrected §9). **Their addresses are read; ~~what all but four of them do is not.~~** *(answered: see the arm table and the 2026-09-14 and 2026-09-18 notes on this page; 2026-10-02, OPUS)*

| selector | arm | | selector | arm |
|---|---|---|---|---|
| `0x20` (space) | `002AD041` | | `1` | `002ADBF5` |
| `!` | `002AD151` | | `2` | `002ADC71` |
| `"` | `002AD1ED` | | `3` | `002ADC5A` |
| `#` | `002AD205` | | `4` | `002ADD03` |
| `$` | `002AD252` | | `5` | `002ADD19` |
| `%` `&` `'` | `002AD289` | | `6` | `002ADD62` |
| `(` | `002AD2F4` | | `7` | `002AD38A` |
| `)` | `002AD3F7` | | `8` | `002ADD96` |
| `*` | `002AD47C` | | `9` | `002AE190` |
| `+` | `002AD76B` | | `:` | `002AE1B1` |
| `-` | `002AD8AB` | | `<` | `002AE1C5` |
| `.` | `002AD8F9` | | `=` | `002AE1DB` |
| `l` | `002ADC34` | | `>` | `002ADE90` |
| `m` | `002ADC0C` | | `?` | `002AE03E` |
| `n` | `002ADC20` | | `V` | `002AE2F0` |
| `o` | `002ADCDD` | | `,` `/` `;` `p` | `002AE308` |
| `0` `_` | `002ACFC2` | ~~**consume and continue, no action**~~ **printed**: return 1 with the cursor on the selector byte *(corrected 2026-10-02, OPUS: `002AC5F0+0xA2A` stores the cursor at the selector before the dispatch, and both selectors map to the exit `002AC5F0+0x9D2`)* | | |
| 42 others | `002AE1F1` | `@`–`U`, `W`–`^`, `` ` ``, `a`–`k` | | |

**`V` is cut out of that 42-character block and given its own arm.** ~~It is the only selector that also writes
the second out-parameter (`002AE2FF mov dword ptr [r13], r15d`).~~ *Corrected 2026-09-14 (FABLE), §2.6:* eight
arms write it, and `V`'s store writes the zero that entry already wrote.

### 2.6 What each arm does — every arm read, 2026-09-14 (FABLE)

*Each arm was followed along its control flow to the shared exits (`002ACFC2` return 1, `002AC6CA` return 0),
and the anchored readings were checked by hand. "Skipped" means the arm parses its payload, advances the cursor,
and does nothing else. Offsets without a base are fields of the caller's text context (`r14`); `painter` is the
`0209CC40` object (§4).*

**The second out-parameter is a character count.** The emitter spends it one unit at a time: it decrements
painter `+0x10D8` and `+0x10DC` once per unit, and while `+0x10DC` is not positive it also takes a step off the
`+0x10E4` budget (`002AA6B5`–`002AA6FF`). `002AAE40` adds it to its own running count (`002AB5C6`). Arms write it
as follows:

- **1** at `002ACCE3` (tokens `0x01`/`0x04`/`0x06`/`0x07`), `002ACDD0` (`0x05`), `002ACEF0` (`0x0A`), `002AE183`
  (`?`) and `002AE2E3` (the 42-selector block).
- **The inserted string's count** at `002ADAA4` / `002ADADF` (`.`).
- **0** at `002AD8F0` (`-`) and `002AE2FF` (`V`). `r15d` is zeroed at entry (`002AC622`) and is set to 1 only
  inside the `.` and `>` arms (`002ADA77`, `002ADF97`), so on these two paths the store repeats the entry zero
  (`002AC628`).

The two alpha-fading arms (`?` and the 42 block) use the same pair: while painter `+0x10DC` is positive the glyph
keeps the context alpha `+0x33`; after that the alpha is `+0x33 × +0x10E4`, clamped to `[0, 128]`
(`002AE0D3`–`002AE104`, `002AE27E`–`002AE2B0`).

| selector | arm | payload | what the arm does |
|---|---|---|---|
| `)` | `002AD3F7` | `003FFBC0` writes straight into `+0x30` | **text colour.** RGB goes into `+0x30` and the previous alpha `+0x33` is put back; a parsed 0 becomes the default `0x80808080`. The colour is copied to painter `+0x10D0`, then the arm joins `+`'s tail, which closes the open glyph packet (`002AD7F9`–`002AD81A`). A colour change therefore starts a new batch |
| `+` | `002AD76B` | 3 bytes | **render-state byte `+0x9F`** from the payload (`0xFF` → 0). Closes the glyph packet and emits a state command built from `+0x9F`'s high nibble (`002AD821`–`002AD86F`). What the nibble selects is not read |
| `(` | `002AD2F4` | 3 bytes | **`+0x34 = payload / 24`** (`008F3128` = 24), further scaled by bits 4–8 of `[+0x68]` / 24 when `+0x68` is set and the 41-byte global predicate the arm calls is non-zero. When that predicate is 0: `+0x44 = (payload − 24) × 0.25` for payloads ≥ 24, else 0 |
| `7` | `002AD38A` | 3 bytes | **`+0x34 = payload / 100`** (`008F3134` = 100). When that predicate is 0: `+0x44 = (payload − 100) / 16.6` for payloads ≥ 100, else 0. `+0x34` is the factor the space arm multiplies its advance by (`002AD0BB`, with `+0x38`), so `(` and `7` set one size factor in 24ths and in percent |
| space | `002AD041` | 3 bytes | writes `+0x40` from the payload and the pen advance `0209CC68`, scaled by `+0x34` and `+0x38`; tests `+0x44` bit 11 |
| `2` | `002ADC71` | 3 bytes | **tab.** Payload 0 stores the caller's current float (arg 3) as painter `+0x10E0`. Payload `n` sets the pen advance to `2n − (x − [+0x10E0])` when that is positive (`002ADC9F`–`002ADCD0`), so it moves forward only |
| `5` / `6` | `002ADD19` / `002ADD62` | 3 bytes, into `+0xAA` | **indent.** `5` keeps the payload and `6` negates it. The value goes to `+0xAA` and painter `+0x10FD`. At a line start (painter `+0x1102` set) `5` also writes it as the pen's x. The line break `0x02` puts a positive `+0xAA` into x for each new line (`002AC7B8`–`002AC7CE`) |
| `.` | `002AD8F9` | `003FFC60` | **inserts argument `n`** from the caller's array at `+0x70` (16-byte entries, `n` = payload byte). Kinds 1 and 2 insert the string at entry `+8` through the nested measure/emit and return its count. Kind 0 formats the number at entry `+8` through `002AE610`, handing it a copy of this code at `01E0CE08` with its second byte set to `0xFF` (`002ADAE8`–`002ADB07`). Other kinds insert nothing. Painter `+0x10D8`/`+0x10DC`/`+0x10E4` are saved (`002AD9CB`–`002AD9E2`) and restored (`002ADBD5`–`002ADBE8`) |
| `-` | `002AD8AB` | `003FFC60` | **a number:** hands the code, the float and out2 to `002AE610` (number → digits → glyph advances), then stores 0 in out2 |
| `8` | `002ADD96` | `003FFB00`, an `i16` | **inserts the name for that id** (`002639E0`, [the NPC name dictionary](../../04-Actor-Entity/Actor-Names/the-npc-name-dictionary.md)) through the nested measure/emit; nothing when the lookup is null |
| `>` | `002ADE90` | 3 bytes | **inserts the display name of the context's actor** at `+0x78` (`00263990`, [the NPC name dictionary](../../04-Actor-Entity/Actor-Names/the-npc-name-dictionary.md)); nothing when null |
| `?` | `002AE03E` | 3 bytes | **inserts one glyph** through `002AE450` (one character through the font's code map). The payload falls into three bands (< 10, 10–19, ≥ 20), each with its own code base and arguments (`002AE11A`–`002AE177`). Counts 1 and fades |
| 42 selectors `@`–`k` bar `V` | `002AE1F1` | `002AEB20` returns the advance | **an inline glyph drawn by `002AEB20`** with the cursor and the faded alpha. Before drawing, `002AEB20` reads the input manager's analog-moved byte (`001E0C10`, called at `002AEB74`; [keymap](../../15-Input/Binding-Profiles/keymap-ini-file-format-and-default-controls.md)). Which glyph a letter selects is not read. Counts 1 and clears `+0xA9` |
| `*` | `002AD47C` | `003FFD70` | nested: copies the context and runs `002B43C0`, the measure pass and the emitter |
| `!` | `002AD151` | none; advances 1 (`002AD1E5`) | fetches the entry for byte `+0xA6` from the 256-slot table `02AEE810` (`0039BA30`) into `+0x68` and `+0x60`, and sets `+0x44` bit 11 (the bit the space arm tests) |
| `#` | `002AD205` | 3 bytes | `+0x88` = payload, the same word the markup parser writes for `#`; low byte of `+0xB0` = 5 with bits 19 and 26 set; `+0x9B` = 1 |
| `$` | `002AD252` | 3 bytes | `+0x4C` = signed payload as a float, unless `+0xB0` bit 25 is set |
| `%` `&` `'` | `002AD289` | 3 bytes | **justification: left, right, centre.** `+0x99` = payload (a margin); `+0x9A` and painter `+0x1104` = the selector character. `002B1F20` switches on `+0x9A`: `%` gives `x = +0x99`, `&` gives `x = (+0x94 − width) + +0x99`, and `'` gives `x = (+0x94 − width) / 2 + +0x99`. Here `width` is the measured line and `+0x94` is the word it is subtracted from (`002B1F20`, read whole). At a line start the arm measures the rest of the line (`002B2150`) and writes the justified x into the pen. The line break re-justifies every following line the same way |
| `9` | `002AE190` | 3 bytes | sets `+0xB0` bit 21 |
| `o` / `:` | `002ADCDD` / `002AE1B1` | `003FFB00` / 3 bytes | clear `0209E598` and reset the font painter descriptor, the same reset token `0x03` does (`002ACFB4`–`002ACFBD`); `o` also returns its `i16` through arg 3 |
| `"` `1` `3` `4` ~~`<`~~ `=` `l` `m` `n` `,` `/` `;` `p` `V` | §2.5 | 3 or 4 bytes | *Corrected 2026-09-27 (FABLE, Claude Opus 5.5): `<` is not skipped. `002AE1C5` reads its payload into context byte `+0xAB`, as `002B0280` does at `002B19BE`, and the glyph path adds `+0xAB` to each glyph's Y (`002B0948`, `002B0AED`): a baseline shift (Y-1, the `NAOverHeadTextOffsetY` rows).* **skipped.** Five of these (`"` `/` `;` `=` `p`) write render-state fields in the markup parser `002A8C50` ([numeric formatting](numeric-formatting-and-character-mapping.md) §13), so their effect belongs to that pass |
| `0` `_` | `002ACFC2` | none | nothing (§2.5) |

**Token arms.**

| byte | arm | what it does |
|---|---|---|
| `0x02` | `002AC6D1` | **line break.** Measures the next line from the following byte (`002B2150`) and sets the pen's x from the justification `002B1F20` plus `002B2C50`'s result (`002AC6F3`–`002AC72D`). Advances the pen's y by `[0209CC3C] × +0x34 × +0x3C` plus a gap: painter `+0x10E8`, or the value the measure returned, which then replaces `+0x10E8` (`002AC737`–`002AC79D`). Clears the spacing pair `0209CC60`/`0209CC68`, applies the indent, and sets the line-start flag painter `+0x1102` (`002AC6DD`) |
| `0x08` | `002AD011` | skips a 3-byte token |
| `0x09` | `002AD008` | skips itself |
| `0x01`, `0x04`, `0x06`, `0x07` | `002ACB96` | a one-character unit: it writes the pen advance (`0209CC68`, `0209CC64`), counts 1 and advances one byte |
| `0x05`, `0x0A` | `002ACCF3`, `002ACE25` | a measured one-character unit: they set painter `+0x1100` and measure through `002B2150`. `0x05` also writes painter `+0x10EC`/`+0x10F4` and `0x0A` writes `+0x10F0`/`+0x10F8`. Both count 1 |
| `0x0E` | `002AC825` | the embedded selection list (`UQ-174`, [numeric formatting](numeric-formatting-and-character-mapping.md) §13) |

> **The inserting codes are exactly the lookahead class.** The markup parser groups `.`, `8` and `>` in one
> `bt` set and handles none of them. Here they are the three arms that splice other text into the line: an
> argument, a name by id, and the actor's name. Both name resolvers choose between two names with a persistent story
> flag (the 2,048-flag bank query in the name dictionary's chain). **What still has no reading:** `+`'s state nibble, the meanings
> of `+0x40`, `+0x44`, `+0x4C`, `+0x88`, `+0x99`/`+0x9A`, `+0xAA` and `+0xB0`'s bits, which glyph `002AEB20`
> draws for each of the 42 letters, and the `0x01`–`0x0A` units' content.

## 3. Why it is the largest function

**Seven callers, and they are the text pipeline:**

| caller | site |
|---|---|
| `002A8C50` | `002A9726` |
| `002A9F00` (the glyph emitter) | `002AA6A8` |
| `002AAE40` | `002AB5B0` |
| `002AF340` | `002AF783` |
| `002B1FB0` | `002B207E` |
| `002B2150` | `002B2393` |
| `002B5730` | `002B5823` |

**`002B2150` and `002A9F00` are both callers *and* callees of this function** — `002AC5F0` calls
`002B2150` seven times and `002A9F00` four times. The interpreter and the measure/emit passes are
mutually recursive, which is how a code that inserts text (a name, a number) gets that text measured
and drawn by the same machinery that is currently interpreting it.

**That is the whole reason for the size.** The language is implemented once, and everything that
walks a string — measuring, emitting, the two passes above them — enters here.

> This settles the open question in the glyph-run document. **`002AC5F0` does not draw**; it is the
> function the three drawing passes call, and two of the three named in that question
> (`002AAE40`, and the emitter) are among its seven callers.

## 4. The painter singleton

```asm
002AC650  mov   r8, qword ptr [rip + 0x1df05e9]    ; -> 0209CC40
002AC657  mov   rax, qword ptr [r8 + 0x10c8]
```

`0209CC40` holds the painter object, and this function touches `+0x10C8`, `+0x10FC` and `+0x1102`.
**`+0x1102` is the field `002AF960` sets to 1 during initialisation**, and `+0x10E4` — the per-run
budget established across three functions in the glyph-run document — lives in the same object.
**The interpreter and the emitter share one painter, reached through a global rather than passed.**

## 5. Modding notes

- **The control-code language is `0x01`–`0x0F`, with `0x0F` + an ASCII letter for the extended set.**
  Bytes `0x0B`, `0x0C` and `0x0D` are *not* codes — they route to the ordinary-character arm.
- **Code lengths are decided by the parser, not the interpreter.** `003FFAB0` and its ten siblings
  return a byte count that becomes the cursor advance, so adding a payload byte to a code means
  changing the parser, not this function.
- **An unknown selector inside `0x20`–`0x70` is not an error** — it lands on a shared arm, ~~and the
  cursor still advances~~ **which leaves the cursor on the selector, so the next call prints it** (the contract's I-3/I-6;
  corrected 2026-09-29). Outside that range ~~the escape is consumed and skipped~~ **only the `0x0F` is consumed and
  the selector byte is printed by the next call** (`002AD029 ja 0x2acfc2`; *corrected 2026-09-29, OPUS, propagating
  the contract's I-6 correction of 2026-09-25 (FABLE, on OPUS block 313's execution)*).
- **`0x03` ends the run.** It is the only token arm that does work and still returns 0.

## 6. What is not known

- [x] **UQ-177.** **What 28 of the 32 escape codes do.** Their arm addresses are read and tabulated; four were
      sampled. **Nothing above assigns a meaning to any selector.**
      *Narrowed 2026-09-14 (FABLE), §2.6:* every arm has now been read. The anchored ones are colour `)`, the size
      factor `(` / `7`, tab `2`, the signed offset `5` / `6`, the inserts `.` `8` `>` `?`, the number `-`, the
      42-letter inline glyph, and the fourteen skipped selectors. `+`, space, `!`, `#`, `$`, `%&'`, `9`, `*`, `o`
      and `:` are read as field writes without a consumer. *Later the same day:* `%&'` is justification (left, right,
      centre, through `002B1F20`) and `5` / `6` is the indent the line break applies. Neither is in the residue now.
      ***NARROWED 2026-09-17 (FABLE), two of the consumerless fields placed:** `+0x4C` (the `$` payload) is the extra advance every blank unit and space adds before scaling (`002ACC97`), a letter-spacing term; and `+0x44` bit 11 (set by `!`) widens token `0x04` by `[01CEBBA8]` when the option `00254A10` is clear (`002ACC1B`..`002ACC35`). Still without a consumer here: `+`'s state nibble, `+0x40`, `+0x88`, `+0xAA` and the `+0xB0` bits.*
      ***NARROWED 2026-09-18 (FABLE): four more of the consumerless fields placed, by scanning the text range `002A8000`..`002B5000` for every reader.** *`#` is the page wait.* Its payload `+0x88` is a tick count: the per-tick state machine `002ABF70` ([the numeric-formatting page](numeric-formatting-and-character-mapping.md)'s stepper, driven from `002A9945`), in the mode-5 arm `002ABF9F`, decrements `+0x88` each tick and at zero writes the accumulator `+0x9B` to 30 (its firing value), mode 0, and advances the target line (`+0x92` = `+0x90`, `+0x90` += `+0xA0`, `002ABFBC`..`002ABFEF`); the pager `002A9980`, in its mode-3 arm, treats `+0x88` == 10,000 (`002A99CA`) as wait for the decide button, testing the pad words `02F9736A` / `02F97362` against the mask `01E0C2A0` (`002A99DC`..`002A99F3`) before it steps the line words and clears bit 19 (`002A9A09`). Bit 19 of `+0xB0` is the waiting flag: the parser `002A8C50` tests it at a page end (`002A97D3`) and, when clear, inserts the same wait itself (mode 5, bit 19, `+0x9D` = `+0x9E`, `002A97E3`..`002A97FB`), setting bit 26 first. *The space payload `+0x40` is a fixed-advance switch.* The spacing builder `002AC2F0` (`002AC4B8`..`002AC50C`) and the second glyph pass `002B0280` (`002B0670`..`002B068D`) read it only for glyphs whose descriptor has bit 31 set: when `+0x40` is non-zero they add the constant `1.5` (`00901B3C`), or `0.5` (`01CEBB70`) when the option `00254A10` is clear, to the advance on top of `+0x4C`. *`+0xAA` (the `5` / `6` indent) is consumed by the draw `002AAE40`* at `002AB711`: when positive it becomes the pen's starting x. *Bit 25* (the `$` guard) is tested at `002AD261` and by `002B0280` at `002B1586`, and set by no code in the range. *Still without a consumer:* `9`'s bit 21 is cleared by the draw `002AF960` (`002AF9FA`) and by `002B0280` (`002B0362`, set again at `002B1660`) but tested nowhere in the range; `#`'s bit 26 is set and never tested there; and `+`'s state nibble is unread. Static, every site named.*
      ***ANSWERED 2026-09-18 (FABLE) — every arm is read and every field is placed or shown write-only; the last three close on the shipped data.** An archive census of every `.bin` / `.dat` under the nine language trees, kept to the text formats by magic (407 `st2e` banks, 101 `hdat` handbooks, 53 bank-format files; 24,702 `)` escapes as the control), gives each selector its authored count. **`9` is authored nowhere** (0 occurrences of `0F 39` in any text-format file; the only such bytes in the language trees are inside `himg` images), so its bit-21 set at `002B1660` and the clears at `002AF9FA` / `002B0362` can never fire from shipped text, and the table it would index (`00916560`, UQ-176 on [the numeric-formatting page](numeric-formatting-and-character-mapping.md)) is dead data. **`#` is authored** — 16 times in the `st2e` banks (`listhelp_eventitem.bin` 9, `basic_skill.bin` 6, `listhelp_daijinamono.bin` 1), 27 more in `texpack_ys.bin` — and does what the 2026-09-18 narrowing read: the page wait through `+0x88` and bit 19; its bit 26 is set by those authored tags and read by nothing in the text range, so it is write-only state in the shipped game. **`+` is authored** — 16 times in `st2e` (`battle_message.bin` 14, `basic_skill.bin` 2) and 14 in `battle_pack.bin` — and its state nibble likewise has no reader: written, never consumed. Of the other consumerless fields, all were placed earlier today and on 2026-09-17 (`$` letter-spacing, `!` widening, space's fixed advance, `%&'` justification, `5`/`6` indent, `o`/`:` painter reset, `*`, `#` wait). So the 32 selectors are: the 28 read arms with their effects in §2.6 and the table above, one selector no shipped text uses (`9`), and two whose authored occurrences leave a write-only field behind (`#` bit 26, `+`'s nibble). What those two fields were for in the authoring pipeline is not recoverable from the image, and no shipped behaviour depends on them. Static for the arms; DATA for the census.*
- [x] ~~**UQ-178.** What the eleven token arms other than `0x02`, `0x03` and `0x0F` do.~~
      *Narrowed 2026-09-14 (FABLE), §2.6:* `0x08` / `0x09` skip; `0x0B`–`0x0D` are text; `0x0E` is the selection
      list; `0x01`/`0x04`/`0x06`/`0x07` and `0x05`/`0x0A` are one-character units that write the pen advance and
      count 1. What those units draw is not read.
      ***ANSWERED 2026-09-17 (FABLE): the six units draw nothing; four are blanks of different widths and two are column-alignment markers.** The emitter confirms it: after the dispatcher returns for a unit it only spends the count and adds the advance `0209CC68` to the pen (`002AA6B5`..`002AA74C`), drawing no glyph. The four-code arm `002ACB96` reads the token byte and picks a width: `0x01` the font metric `0017F920(0)`, `0x04` the metric `0017F920(1)`, the space the charset names; `0x06` the fixed width `[008F8180]`; `0x07` 26 units when the option `00254A10` is clear and ~~the frame mode~~ the cached locale value `00229E40` (`01E02814`) is 7 — a branch that never runs, since `00254A10` returns 1 for 7 (`00254A10+0xE` mask `0xD81`) *(corrected 2026-10-02, OPUS: `002AC5F0+0x5DA`–`002AC5F0+0x5ED`)* — otherwise `0024ABA0()` times `[008F8180]` (`002ACBA8`..`002ACC0F`). With the option clear, token `0x04` under `+0x44` bit 11 gains `[01CEBBA8]`, and otherwise the current painter descriptor `[0209E598]` adds a kerning term, from the metric object's `0017F9C0(+0x10)` pair less `[008F311C]` when one is bound, or from the descriptor's own bit fields `(desc >> 20) & 0x1F` less `(desc >> 32) & 0x1F` less 3 when not (`002ACC1B`..`002ACC93`). Every width then adds `+0x4C` and scales by `+0x34` and `+0x38`, the vertical advance `0209CC64` comes from `0017F880()` times `+0x34` and `+0x3C`, and the arm counts 1 (`002ACC97`..`002ACCE3`). `0x05` and `0x0A` (`002ACCF3`, `002ACE25`) set painter `+0x1100` when `+0x1101` is clear, take the same blank advance, and measure the following line through `002B2150`: `0x05` records the width at `+0x10EC` and `+0x10F4`, `0x0A` keeps the maximum at `+0x10F0` and the remainder at `+0x10F8` (`002ACF57`..`002ACF7A`). The line layout `002B24B0` zeroes those four at entry (`002B25A8`..`002B25B5`), accumulates `+0x10F4` (`002B26F6`) and returns `+0x10EC` and `+0x10F0` through its out-parameters (`002B2721`..`002B274E`): the two tokens mark the first and second column of an aligned pair of lines. Static, dispatcher, emitter and layout read.*
- [x] ~~What `003FFAB0` (78 B) parses, and how the eleven parsers differ. **The claim here is only that
      its return value becomes the cursor advance**, which is read at every one of the 19 sites.~~
      **ANSWERED 2026-09-13 (OPUS): `003FFAB0` parses a THREE-BYTE code into one output byte, and
      the eleven differ by the LENGTH of the code they consume — which is exactly why the return is
      the cursor advance.**

      **`003FFAB0`, all 78 bytes.** It reads `[rcx+1]` and `[rcx+2]`, masks them
      (`r9b = [rcx+1] & 0xC0` then doubled; `r8b = [rcx+2] & 0x7F`), and branches on
      `test byte [rcx+1], 7`:

      - **low three bits zero** → `0039BA00(r8b)` returns a pointer and the output byte is `[rax]`
        — **a table lookup keyed by the 7-bit value**;
      - **otherwise** → the output byte is the composed `(b2 & 0x7F) | ((b1 & 0xC0) << 1)`.

      Either way it writes **one byte** through `rdx` and returns **3**.

      **The family separates on record width, and the return tracks it exactly:**

      | parser | size | returns | record bytes read |
      |---|---:|---|---|
      | `003FFAB0`, `003FFB90`, `003FFC60`, `003FFDA0`, `003FFEE0` | 78/33/115/67/33 | **3** | `+1`, `+2` |
      | `003FFCE0`, `003FFF10` | 134/47 | **4** | `+1`, `+2`, `+3` |
      | `003FFB00`, `003FFBC0` | 141/154 | **`ebx`** — computed | `+1`,`+2` / `+1` |
      | `003FFDF0` | 233 | computed, via `0x24924925` / `0x92492493` — **the magic constants for division by 7** | `+1`, `+2`, `+3` |

      **Every fixed-length parser returns (bytes read) + 1**, the `+1` being the code byte at `+0`
      that the dispatcher already consumed. **So the return IS the total code length**, which is the
      claim §7 says is all that was established — and it is now established from the parsers rather
      than from the 19 call sites that use it.
      **Three of the eleven are variable-length**, which is the real difference the question was
      after: two compute the advance in `ebx`, and `003FFDF0` divides by seven, the signature of a
      code carrying a run of seven-bit fields.
      **`003FFD70` (41 B) is not resolved by this sweep** — no `mov eax, <imm>` return was matched,
      so its advance comes from another path and is not claimed here.
      **Not established:** what any code MEANS. This separates the family by shape only.
- [x] ~~**UQ-179.** What the second out-parameter means — only the `V` arm and the entry zeroing were seen.~~
      **ANSWERED 2026-09-14 (FABLE), §2.6:** a character count. The emitter spends it one unit at a time against
      painter `+0x10D8` / `+0x10DC` / `+0x10E4` (`002AA6B5`–`002AA6FF`), and `002AAE40` adds it to its running
      count (`002AB5C6`). It is 1 for five arms, the inserted string's count for `.`, and 0 otherwise.
- [x] ~~**UQ-180.** Why `V` is special-cased out of the 42-selector block.~~ **ANSWERED 2026-09-14 (FABLE),
      §2.6, by behaviour:** the block draws an inline glyph through `002AEB20` and counts one character. `V`'s
      arm parses three bytes, draws nothing and counts none. What `V` carries for any other pass is not claimed.

## 7. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Cursor is by reference and advanced in place | `002AC642`, and `add qword ptr [rdi], rax` at every parser arm | 1 |
| Return 1 = consumed, 0 = stop | `002ACFC2`, `002AC6CA`, `002AE32A`, and the ~~identical `test/je` at all seven call sites~~ `test/je` at five of the seven call sites *(corrected 2026-10-02, OPUS: `002B1FB0+0xCE` and `002B5730+0xF3` call once)* | 1 |
| Bytes `>= 0x10` are ordinary text | `002AC694`-`002AC697` | 1 |
| Fifteen token arms, table at `002AE334` | `002AC69B`-`002AC6AC`, image base resolved from the `lea` | 1 |
| `0x0F` reads a second byte in `0x20`-`0x70` | `002AD01A`-`002AD03F` | 1 |
| Thirty-five targets, `0x51` case bytes | complete decode of `002AE370` and `002AE3FC` | 1 |
| The three tables tile with no gap | `002AE334` + `0x3C` + `0x8C` + `0x51` = `002AE44D`, and `002AE450` is the next function | 1 |
| The parser return is the cursor advance | `002AE308`-`002AE317`, the same shape at 19 `003FFAB0` sites | 1 |
| Seven callers, mutual recursion with two of them | caller scan over 38,161 functions with a body; `002B2150` and `002A9F00` appear on both sides | 2 |
| The painter is a global at `0209CC40` | `002AC650` | 1 |

**Control on the caller count.** The scan that reports seven callers is the same one that positively
returns 44 distinct callees and 108 call sites **inside** this function, and it found `002B2150` and
`002A9F00` in both directions — so it is not filtering one direction of the edge.

**Limit on the catalogue.** The selector-to-arm mapping is a complete decode of the two published
tables. **It is a map of where the code goes, not of what it does**, and section 6 says so for 28 of
the 32 arms rather than leaving the table to imply otherwise.

## 8. Related

- [`../../99-Unresolved-Residual/Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md`](../../99-Unresolved-Residual/Glyph-Run-Rendering/how-a-line-of-text-becomes-glyph-quads.md)
  — the emitter, the `+0x10E4` budget, and the open question this document answers
- [`../../99-Unresolved-Residual/Glyph-Run-Rendering/painting-a-line-of-text-into-a-render-target.md`](../../99-Unresolved-Residual/Glyph-Run-Rendering/painting-a-line-of-text-into-a-render-target.md)
  — the record the painter fills
- [`../../99-Unresolved-Residual/Glyph-Run-Rendering/choosing-the-render-target-for-a-text-run.md`](../../99-Unresolved-Residual/Glyph-Run-Rendering/choosing-the-render-target-for-a-text-run.md)
  — where the run is drawn
- [`numeric-formatting-and-character-mapping.md`](numeric-formatting-and-character-mapping.md) — the
  character mapping this language sits on top of

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

*(Static only — the shipped image, its function list and a rel32 census. Nothing executed.)*

### ✔ Everything structural reproduces, to the entry

| claim | measured |
|---|---|
| the body is **7,489 B**, and the next function is `002AE450` | **7,489**, and the next entry in the function list is **`002AE450`** |
| **the three tables tile** — `002AE334` + 15×4 = `002AE370` + 35×4 = `002AE3FC` + `0x51` = `002AE44D` | **all three, exactly** |
| the 15-dword table's arms | **all fifteen**, including the two shared arms: `002ACB96` for bytes `01`/`04`/`06`/`07` and `002AC6CA` for `0B`/`0C`/`0D` — **ten distinct arms** over the fifteen bytes |
| the `0x51` case-index table feeds a 35-target table | its bytes run **0–34 and use all 35**, so the two tables are exactly matched |
| **seven callers** | **7 sites in 7 functions**, at `002A9726`, `002AA6A8`, `002AB5B0`, `002AF783`, `002B207E`, `002B2393`, `002B5823` — **every address as published** |
| `003FFAB0` called **19** times; `002B2150` **seven**; `002A9F00` **four** | **19 / 7 / 4** |
| the parser family is **11 functions, 32 call sites** | inside this function: **11 distinct callees in `003FFAB0`–`003FFF10`, 32 sites** |

The tiling is worth restating as the check it is: three bounds taken from three different `cmp`
instructions imply three lengths, and the three lengths **lay end to end with no gap and stop two
bytes before the next function**. That is not a coincidence a misread would survive.

### ✖ Corrected: thirty-four distinct arms, not thirty-two

§2.5 opens *"Thirty-two distinct arms"*. The 35-entry target table holds **34 distinct addresses**,
and **§2.5's own table lists thirty-four of them** — the prose undercounts the table beneath it.

The 35th entry is not a 35th arm: **`002ACFC2` appears twice**, at table indices **13 and 34**, and
it is the arm the page already names *"consume and continue, no action"* — reached from selectors
**`0`** and **`_`**. So the three numbers are: **35 table entries, 34 distinct arms, 0x51 selectors**,
and the duplicate is what separates the first two.

### The distribution, since it is cheap to state

Of the 34 arms, **30 serve exactly one selector**; `002ACFC2` serves two (`0`, `_`), `002AD289`
three (`%`, `&`, `'`), `002AE308` four (`,`, `/`, `;`, `p`) and `002AE1F1` **forty-two** — which is
§2.5's "42 others", and it is the largest single block in the language. **`V` really is cut out of
that block**: it is `002AE2F0`, its own arm, exactly as the page says.

**Not claimed.** What any arm *does* — **no arm body was read in this pass**, and §2.5's "what all but
four of them do is not" stands. Whether `003FFAB0`'s return is a byte count: §2.4 reads it that way
from the `add qword [rdi], rax` that follows, and **that callee was not re-read here**. Nothing was
executed.

## Crossings into other layers — FINAL-AUDIT pass 22 (OPUS, 2026-09-18)

Three crossings, each read at its call site. Two of them are the **locale id** this page's helpers
serve, reached by two different callers — so they are one fact, not two.

*Helpers on the far side of an edge are described by role rather than by address. A first version of
this section named three of them and imported their neighbours in turn, adding two findings while
clearing three; citing a shared entry pulls in everything it touches, which is the same shape this
pass keeps finding.*

- **Audio — this page is the CALLER.** `002A9980` calls the 51-byte audio request helper `00249C60`
  at **six** sites: `002A9CAE`, `002A9CC1`, `002A9D08`, `002A9D57`, `002A9D66`, `002A9EB0`. That
  helper refuses while a global gate is non-zero (`00249C64`), resolves an id through a lookup, drops
  out on `-1` (`00249C72`), and otherwise tail-jumps the sound-request path with `edx = 0x40` and
  `r8d = 0x7F` (`00249C77`–`00249C7E`). **Text rendering asks for sounds; it owns nothing in Audio.**
- **Rewards_Progression_Economy — SERVICE.** `EnemyChain_UpdateOnDefeat` (`00317ED0`), owned by that
  layer, calls this page's locale getter `00229E40` at **three** sites — `00317F2D`, `0031804B`,
  `0031806C`. The getter is seven bytes: it returns the cached locale dword and nothing else. That
  use is already documented from the other end on
  [the loot and enemy-chain page](../../13-Rewards-Progression-Economy/loot-drops-and-enemy-chain.md).
- **Save_Load_Settings — SERVICE.** `SaveSlotMetadata_BuildSubmissionDescriptor` (`005832B0`) calls
  `00254A10` at **`00583358`**. That helper is the same getter plus a membership test: it refuses an
  id above `0xB` (`00254A19`) and otherwise returns 1 only for the bits set in `0xD81`
  (`00254A1E`–`00254A26`) — **`{0, 7, 8, 10, 11}`**. Against
  [the locale page](../../19-Save-Load-Settings/Language-And-Locale/language-selection-and-locale-ids.md)'s
  returned-id table those are `kr` 7, `ch` 8, `jp` 10 and `cn` 11, **plus id 0**, which that page's
  `AV-1` records as being handled as CJK although the selector never produces it. **So the save-slot
  descriptor is asking "is this a CJK locale".** The `0xD81` set is named there and is cited here
  rather than re-derived.

*Easy to confuse with the neighbouring predicate: `00229E50` tests `{0, 7, 10, 11}` — the same set
**without** `ch` (8). `00254A10` includes it.*



**Input — SERVICE (SWE2-EC7-161, 8 edges).** `002AB8F0` — the control-code dispatch this page
measured — calls `001E0C10`, which calls `00197780`/`00198790` on the Input layer; `002A9980`
calls `001E0A10` there too. The language's opcode path consults input state; no shared
ownership.
- **ActorEntity - CLIENT (5 edges).** `00263990` is called by bodies filed to ActorEntity: `0025C230`, `0025C830`, `00268D10`, `00272CB0` (+1 more) - shared machinery across the layer boundary, no shared ownership.
- **Party - CLIENT (1 edge).** `001E0C10` is called by bodies filed to Party: PartyControl_BuildAnalogMovementVectorFromInputHistory (`003594E0`) - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (4 edges).** `00229E40`, `00229E50`, PersistentFlag_QueryBank2048 (`0032A930`) are called by bodies filed to Script_VM_Native_Bridge: `0033FED0`, `0034BA00`, `0034C010`, `0034E980` - shared machinery across the layer boundary, no shared ownership.
- **Story_Event_Quest_Hunt - SERVICE (2 edges).** `00263990`, `002639E0` reach bodies filed to Story_Event_Quest_Hunt: PersistentFlag_QueryBank2048 (`0032A930`) - shared machinery across the layer boundary, no shared ownership.

## SWE2-EC7-26 update (2026-09-18) — `003FFDF0` control-code operand unpacker

`003FFDF0` (233 B) decodes one control-code's operands: three optional
`& 0x7F` bytes from `[rcx+1..3]` go to `rdx`/`r8`/`r9`; two bit fields
of `[rcx+4]` (`>>1&1`, `>>5&1`) go to two stack outs; then
`[rcx+4] & 1` selects — set: `*[rsp+0x38] = rcx+1` and the cursor
advances by the 7-byte-strided operand span derived from the first
unpacked count byte (`0x24924925`/`0x92492493` reciprocal divide);
clear: `*[rsp+0x38] = 0`. `*[rsp+0x40]` gets `rcx+1`, then a
`& 0x7F`-terminated chain walk accumulates the consumed length, which
is the return value. Interior anchor `003FFEC0` (the walk loop).

## SWE2-EC7-28 update (2026-09-18) — `002B43C0` scoped measure + `+0x84` bit-select trio + `002B1F20` alignment arm

`002B43C0` (375 B) is the measure pass this page names: installs a
`{r8b, 0}` record at `[rip-object + 0x10C8]`, copies the caller's
`0xD0`-byte context twice (work + argument), `strlen`s `rdx` into
`word[+0xEC]`, calls `002AF340` over the copy, then restores
`+0x10C8` — a scoped draw-parameter override around the emitter.
Interior anchor `002B4466` (the `+0x10C8` swap).

`002B2D20` (58 B), `002B2CE0` (54 B) and `002B2CA0` (55 B) — reached
through `002A8C50`/`002A9980`/`002A6190` — are the `dword[+0x84]`
bitfield selects: `002B2D20` `rol`-walks to return the index of the
`edx`-th set bit (`edx > 0x20` passes through); `002B2CE0` returns the
position of the `edx`-th clear bit within `r8d`; `002B2CA0` counts
clear bits bounded by `edx`/`r8d`. Interior anchors `002B2D40` /
`002B2D00` / `002B2CB5` (the walks).

> **Correction 2026-09-18 (FABLE), from the bytes.** `002B2D20` does not return a bit's index: it returns **how many of the first `edx` bits are clear** (the running value advances only on a clear bit), which is the number of options a selection list actually shows. `002B2CE0` is as described. `002B2CA0` **clamps** a visible index to that count. The dword is the list's *omitted-options* mask, set by the script verb `setaskselectignore`; the whole path is under `UQ-381` on [the numeric page](numeric-formatting-and-character-mapping.md).

`002B1F20` (137 B) is the three-arm position select `byte[+0x9A]`
keys: `0x25` returns `byte[+0x99]` as float; `0x26` returns
`word[+0x94] - xmm1 + byte[+0x99]` truncated back to float; `0x27`
returns `(word[+0x94] - xmm1)/2 + byte[+0x99]` — the left/center/right
alignment arms for the control-code position op. Interior anchor
`002B1F37` (the arm select).

## SWE2-EC7-61 update (2026-09-19) - `003FFBC0`

`003FFBC0` (154 B) is a `003FFxxx` wrapper over `0039BA00` - single call. Interior anchor `003FFBF6` (a `0039BA00` call).



## SWE2-EC7-64 update (2026-09-19) - `003FFB00`

`003FFB00` (141 B) is a `003FFxxx` wrapper - `0039BA00` single call. Interior anchor `003FFB51` (a `0039BA00` call).



## SWE2-EC7-66 update (2026-09-19) - `003FFCE0`

`003FFCE0` (134 B) is a call-free control-code payload arm - `byte[r10+2]` low nibble -> `[rcx]`, high nibble >>4 &3 -> `[rsp+0x38]` record. Interior anchor `003FFCFF` (the `al & 0xF` nibble extract).


## SWE2-EC7-73 update (2026-09-19) - `003FFF10` + `003FFB90` + `0039BA00` field/string helpers measured

`003FFF10` (47 B) is the three-out field splitter: each non-NULL of
`rdx`/`r8`/`r9` receives `byte[+1] & 0xF`, `byte[+2] & 0xF`,
`byte[+3] & 0x7F`; returns 4 (the consumed record size).
Interior anchor `003FFF22` (the `+2` nibble store).

`003FFB90` (33 B) is the two-out sibling: `byte[+1] & 0xF` -> `rdx`,
`byte[+2] & 0xF` -> `r8` when non-NULL; returns 3 - the same packed
record minus the third field.
Interior anchor `003FFBA2` (the `+2` nibble store).

`0039BA00` (36 B) is the `02AEE870` blob index accessor: `ecx & 0x1FF`
nonzero returns `rdx + 1 + idx*5`, else `rdx + 1` - the base+strided
element pointer the text readers compute.
Interior anchor `0039BA17` (the `idx*4` fold).

## SWE2-EC7-86 update (2026-09-20) - `003FFDA0` normalized byte-pair decode measured

`003FFDA0` (67 B) is the packed-percent decode the text/glyph
callers run: `byte[rcx+1]` and `byte[rcx+2]` are each masked
`& 0x7F`, converted `cvtdq2ps`, divided by the `008F8180`
constant (10.0f), and stored to `[rdx]` and `[r8]` - two
7-bit fields become two float fractions.
Interior anchor `003FFDB9` (the first `divss`).

## SWE2-EC7-102 update (2026-09-20) - `0039BB00` measured

`0039BB00` (23 B) is the three-arm dispatch
`00242970`, `002AE450` and `002AEB20` call: `ecx == 1`
tail-jumps `002441D0`, `ecx == 2` tail-jumps
`0035D460`, anything else tail-jumps `002441F0` - the
code-class selector the text arms reach through.
Interior anchor `0039BB03` (the first `je`).

## SWE2-EC7-105 update (2026-09-20) - `002639E0` measured

`002639E0` (42 B) is the bit-14-masked relay
`002AC5F0`, `002B0280` and `002B5240` call:
`btr ecx, 0xE` strips the flag before
`0032A930(ecx)` runs, its result feeds
`edx = (eax != 0)`, the bit is stripped
again, and the pair tails
`003EAC10(ecx, edx)` - the
mask-resolve-forward sequence the text arms
share.
Interior anchor `002639EE` (the `0032A930`
call).

## Two corrections from the S-37 contract (OPUS, 2026-09-21)

Both found by reading bodies and tables this page already names, while assembling
[`CONTRACT-text-control-codes-and-dyngeo-draw.md`](../CONTRACT-text-control-codes-and-dyngeo-draw.md).
Filed as `CON-152` and `CON-153`.

**There is a third stop condition, and it is not NUL (`CON-152`).** §2.1 gives two — the NUL test at
`002AC64A` and the ordinary-character arm at `002AC6CA` — and §5 carries the same two. Four
instructions past the NUL test, `002AC650` loads the painter singleton from `[0209CC40]`, `002AC657`
reads `+0x10C8`, and when that pointer is non-null `002AC663` loads the **word** at it and `002AC666`
compares it with the word under the cursor: `002AC669 je 0x2ae31c` jumps to **the same exit the NUL
test reaches**. So a two-byte terminator held on the painter ends a run exactly as end-of-string
does, and it is tested **before the token dispatch on every call**. Because the exit is shared, a
caller cannot distinguish the two from the return value — which is why the omission is invisible from
outside and expensive inside: a reimplementation that stops only at NUL runs past the intended end of
every line whose caller has set that field. ~~**Who sets `+0x10C8` and to what is not read**~~ *Answered 2026-09-25 by
OPUS (`PROPOSED-OPUS-S37-2`; [the contract](../CONTRACT-text-control-codes-and-dyngeo-draw.md) §14 item 2), propagated
here by FABLE (Claude Opus 5.5):* the painter is the **static** `0x1108`-byte object at `0209D490`, which `002B3550` zeroes
and publishes in `[0209CC40]`. So `+0x10C8` starts NULL. Seven functions set it around a draw and restore it afterwards,
to a terminator control code (`0F 23` in `002ABB20`, `0F 2F` in `002B3E90`), a stack-built word, an argument, or NULL.
A caller draws a run up to a chosen escape code. `002B43C0` above is one of the seven.

**Three populations, and none of them is 32 (`CON-153`).** The 2026-09-13 falsification pass
corrected the arm count 32 → 34 and §2.5 says thirty-four — but the `UQ-177` answer in §6 still
reasons over *"the 32 selectors"* and decomposes them as 28 + 1 + 2, which is 31 and is a count of
arms where the sentence says selectors. Decoded from the image: **the selectors are 81** (the bound
at `002AD026` is `cmp eax, 0x50` / `ja` after `lea eax, [rbx - 0x20]`, so `0x20`–`0x70` inclusive,
and the case table at `002AE3FC` is `0x51` bytes); **the case indices are 35**, values `0..34` with
none missing; **the distinct arms are 34**, because the 35-entry target table holds `002ACFC2` at
indices 13 and 34, which the case table maps from the selectors `0` and `_`. The tables tile exactly
— `002AE334` + 15×4 = `002AE370`, + 35×4 = `002AE3FC`, + `0x51` = `002AE44D`, next function
`002AE450` — and all 50 targets land inside the body. **The census results `UQ-177` rests on are
unaffected**; only the frame they are counted into is.

**And one measurement §2.4 leaves open.** "The parser returns how far to advance" is right, and the
returns are now quantified across all eleven: `003FFAB0`, `003FFB90`, `003FFC60`, `003FFDA0` and
`003FFEE0` return the constant **3** on every path; `003FFCE0` and `003FFF10` return the constant
**4**; `003FFD70` returns **`word[payload] + 3`** (`003FFD91`–`003FFD95`), a length the code carries
itself; `003FFDF0` returns a scanned difference (`003FFED3`); and `003FFB00` and `003FFBC0` return a
computed `ebx`. So the language is genuinely variable-length — two fixed widths, one self-describing
and three computed — and **nothing bounds the advance at the call site**, which is
`add qword ptr [rdi], rax` and nothing else (`PROPOSED-OPUS-S37-3`).

`002AFDC0` (1208 B) is the glyph-run emit body the `002AE450` inserter calls: `0209CC48`/`0209CC40` null-gate the text state, `002B4730` x2 wraps `0017FC90`, `002DD860` x2 with `002DD8B0` positions the run, and `00181560`/`001819A0`/`00181870`/`00181460`/`001816B0`/`00181910`/`00181330` emit the glyph cells before the cookie check - the per-glyph emission half of the `?` arm's insert path.

Interior anchor `002B00A2` (function `002AFDC0`).

`002ABB20` (918 B) is the per-tick state machine `002ABF70` calls: `byte[rsi+rax]` scans for the terminator, `002AF340` x2 and `002B20B0` run the span copy/format passes under the cookie check - the mode-5 pager's string-stage helper.

Interior anchor `002ABCEC` (function `002ABB20`).

`002B35A0` (458 B) is the call-free bitfield rewrite `002A8C50` uses: zeroes `+0x54`/`+0x58`/`byte+0xA2`, `btr`/`or`-writes `+0xB0` (`(ecx & 1 | 0xC) << 0x1B`), and under `bt +0xB0,0x1B` a `[r11+0x1D8]`-bounded loop folds `[r11+0x1C8] << 0xC` into `+0x58` bits 12-17 with `bts 0x1C` marking - the control record's field repack.

Interior anchor `002B3611` (function `002B35A0`).

`002B4550` (420 B) is the string-field copy `002B49F0` calls: `byte[r8]`/`byte[r8+1]` both zero picks `r8+2` as source else `r14` (the caller's fallback), `002B1FB0` measures and `00861EBA` copies under the `ecx` bound - the text field's null-pair source select.

Interior anchor `002B45E3` (function `002B4550`).

`002AB8F0` (365 B) is the control-code dispatch `002AEB20` calls: `001E0C10` resolves the context, `ecx - 0x20 <= 0xB` bounds the `0x18B9E4` jump table - arms 0x20-0x2B handle the language's mode codes, arm for `word[01E0C2A0]` tails into `002ABA20`, unmatched codes return 0 - the text control's opcode table.

Interior anchor `002AB8F8` (function `002AB8F0`).

`002B3B20` (269 B) is the wrap-around cursor move `002A9980` runs for the `dx & 0x1000` keys: bit `0x10` of `r9b` decrements `word[rcx+0x58]` toward 0 or - on bit `0x10` of `r8b` - wraps it to `byte[+0xA1] - 1`; bit `0x40` of `r9b` increments it while under `byte[+0xA1] - 1`, wrapping to 0 on bit `0x40` of `r8b`; every firing arm writes result 2 (direction up) or 1 (direction down) into `*[rsp+0x28]` - the page/entry scroll the control-code handler applies to its `+0x58` index over the `+0xA1` row count.

Interior anchor `002B3B40` (function `002B3B20`).

`002DD8B0` (85 B) is the int-to-float position scatter: `edx`, `r9d`, `r8d` and the stack arg convert via `cvtdq2ps` into `+0x20/+0x24`, `+0x50/+0x54`, `+0x80`, `+0x84` and `+0xB0/+0xB4` - the quad/rect float write the two text-control callers share.

Interior anchor `002DD8C5` (function `002DD8B0`).
