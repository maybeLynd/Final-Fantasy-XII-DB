---
system: The aspect fit and the super-wide bound - what setResolutionSize does with a shape it did not expect
category: 17-Presentation-Rendering
status: DOCUMENTED — every register row is answered (UE-1 to UE-4, 2026-09-14): the record's readers are the mode and the clamped size, branch C is a defect in fields nothing reads, the resolution entry is a DXGI_MODE_DESC and mode 1 is Super Wide by code; the entry's last three names (Format / ScanlineOrdering / Scaling) rest on the layout match as UE-3 states, and no listed body reads those fields (swept 2026-09-18), so no behaviour depends on them; owner read 2026-09-29 (OPUS)
owner_layer: PrimaryOwner:Presentation
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: both functions decoded in full, every rip-relative operand resolved to its target, both
    call sites read for argument provenance, and the two float constants read from the image
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_kind: derivation
  last_pass_state: opus-aspect-fit-1 - reached from UD-1 by asking what the twelve
    referenced-but-unlisted bodies mean. 001DDAC0 is one of them; it is the fit itself, and it is
    not in the function census.
  crossref_clean: false
  reopened_count: 0
---

# The aspect fit and the super-wide bound

> `001DDBA0` logs `[Screen Mode]setResolutionSize w = %d ,h = %d Screen Mode = %d` and then **tail-
> jumps** into `001DDAC0`, which is where the width and height are actually decided. **`001DDAC0` is
> not in the function census** - the list kept the logger and never recorded the arithmetic.

## 1. The two numbers the fit is built around

| constant | value | at |
|---|---:|---|
| `16 / 9` | `1.7777778` | `008C5B38` |
| `16 / 3` | `5.3333335` | `00900A0C` |

Beside the log line sit the names this build uses for its display modes - **`Super Wide Mode`**
(`00900960`), `Normal Mode` (`00900970`), `Window` (`0090097C`), `FullScreen` (`00900988`),
`BorderLess` (`00900998`), and `%d X %d ,%dHz, %dHz` (`009009A8`).

## 2. The record

`001DDAC0(rcx = record, edx = W, r8d = H)` writes a 0x18-byte record. Argument order is fixed by the
logger that tail-jumps into it: the format string prints `w` then `h`, and the same registers are
forwarded.

| off | written | by which branch |
|---|---|---|
| `+0x00` | mode - **0** or **1** | A writes 0, B and C write 1 |
| `+0x04` | `1.0f` in A and B; **something else in C** | all three |
| `+0x08` | `1.0f` | A and B only - **C never writes it** |
| `+0x0C` | `0` in A and B; a computed float in C | all three |
| `+0x10` | `W` on entry, **overwritten by B** | entry, then B |
| `+0x14` | `H` on entry, **overwritten by A** | entry, then A |

## 3. Three branches on one ratio

`ratio = (float)W / (float)H`, computed at `001DDAEC`.

**A - `ratio <= 16/9`** (`001DDAF5`-`001DDB18`). Both scales `1.0f`, offset `0`, mode `0`, and
**`+0x14` is replaced by `(int)(W / (16/9))`**. A screen narrower than widescreen keeps its width and
has its height cut to the 16:9 height for that width.

**B - `ratio > 16/3`** (`001DDB26`-`001DDB52`). Both scales `1.0f`, offset `0`, mode `1`, `+0x14`
keeps `H`, and **`+0x10` is replaced by `(int)(H * 16/3)`**. Past the super-wide bound the width is
clamped instead. **`16/3` is the widest shape this function will describe.**

**C - `16/9 < ratio <= 16/3`** (`001DDB53`-`001DDB9E`). Mode `1`, `+0x14` keeps `H`, and then:

```
+0x04 = (float)( W - (H / W) )        ; H / W is an INTEGER divide - 001DDB63
+0x0C = (float)( (W - H) / W ) * 0.5  ; also an INTEGER divide - 001DDB7D, 001DDB90
+0x08   is not written at all
```

## 4. The asymmetry, stated and not explained

Branches A and B are symmetric: clamp one dimension, leave both scales at `1.0f`. **Branch C is not
built like either of them.**

Both of its divisions are `div r10d` on integers. For any ordinary landscape resolution `H < W`, so
`H / W` truncates to **0** and `+0x04` receives **`(float)W`** - not a scale near `1.0f` but the
pixel width itself. `(W - H) / W` truncates to **0** ~~for everything up to `W = 2H`~~ for every `W > H`, the whole branch *(corrected 2026-10-02, OPUS: `001DDAC0`+0xBD `div r10d` with `0 < W - H < W`)*, so `+0x0C`
receives **`0.0f`** across the whole ordinary ultrawide range. And `+0x08`, which both other branches
set to `1.0f`, **is left holding whatever it held before.**

> **What this does on screen is not established and is not claimed here.** Three readings survive
> the instructions: the fields mean something different under mode 1 and the values are correct;
> the integer divides are a defect and ultrawide scaling is wrong between 16:9 and 16:3; or a
> consumer re-derives these fields and never reads them. **Separating them needs the consumers, and
> ~~this pass did not find them.~~** *(answered: see §6, UE-1 answered 2026-09-14 - the three fields branch C writes have no reader, and "a consumer re-derives these fields" is the reading the code supports; 2026-10-02, OPUS)* What is certain is the arithmetic, because it was read.

## 5. Where the sizes come from

Two callers, and they disagree about the source:

- `00182F70` fetches the record from the accessor `001DDAB0` - eight bytes, `mov rax, [01F82D18] / ret` - and passes a width and height it already holds.
- `001DC730` indexes **a `0x1C`-stride table**: `[obj+0x24]` is the selected index, `[obj+0x28]` the table base, and the entry's `+0x00` and `+0x04` are the width and height (`001DC754`-`001DC764`). **That is the resolution list.**

The logger separately reads a second global, `01F82D20`, and prints its `+0x08` as the screen mode.

## 6. What is not known

- [x] **What reads the record.** No consumer census was run; §4 turns on it.
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (UE-2):* **the mode and the clamped size,
      and nothing else.** The record starts the singleton object at `[01F82D18]`. That global has two RIP reads (the
      getter `001DDAB0` and `00182440`) and one write. The getter has 72 direct call sites: 43 pass the object on to 24
      methods, and the rest only test it for null ([`members/aspect-record-consumers.txt`](members/aspect-record-consumers.txt),
      from [`members/getter_consumers.py`](members/getter_consumers.py)). Across those methods and the direct reads, the
      record fields read are:
      - `+0x00` **mode**: `001DD8C0` returns `mode == 1` (its second test is the constant-0 stub `005C5230`); `001DCE20`
        names it (below); `001DD120` and `00182440` test it.
      - `+0x10` **width**: `00225680` (`mov eax, [rcx+0x10]; ret`) and `001DD120`.
      - `+0x14` **height**: `002256A0` and `001DD120`, which returns `(float)width / (float)height` when `mode == 1`, and the
        constant `16/9` (`008C5B38`) otherwise (`001DD126`–`001DD164`).

      **No reader of `+0x04`, `+0x08` or `+0x0C` was found.** Limits: the object's methods were scanned for reads through
      their `this` register, and the linear tracker does not follow a pointer to the object stored elsewhere and reloaded.
- [x] **Whether branch C is a defect.** Stated as three surviving readings, not resolved.
      *Answered on the page 2026-09-14 (FABLE) within the census above, box left for the ledger mirror (UE-1):* **the arithmetic
      is wrong, and nothing reads its result.** The three fields branch C writes badly (`+0x04`, `+0x0C`) or skips (`+0x08`) have
      no reader. What the game uses from the fit is the mode and the clamped width and height, and branch C writes those
      correctly: mode 1 and `H` kept. The aspect the engine reports is `W / H` in mode 1 and `16/9` in mode 0 (`001DD120`). Of
      the three readings in §4, "a consumer re-derives these fields" is the one the code supports. The integer divides are a
      defect in fields that are never read, so on-screen scaling cannot follow from them. The census limit above applies.
- [x] **The `0x1C`-stride resolution table's other 20 bytes.** Only `+0x00` and `+0x04` are read here.
      *Narrowed 2026-09-14 (FABLE, UE-3):* the entry is one 28-byte unit of dword, dword, 8 bytes, a double at `+0x10`, and a
      dword at `+0x18`. `001DD8E0` sorts the table by width, then height, and moves each entry as `movups [+0]`,
      `movsd [+0x10]` and `mov [+0x18]` (`001DD9E0`–`001DDA3F`). It also keeps the selected index's position current at
      object `+0x38` (`001DDA48`). What the double and the two middle dwords hold stays open; the `%d X %d ,%dHz, %dHz` format
      suggests refresh rates and is not asserted.
      *Answered 2026-09-14 (FABLE), box left for the ledger mirror (UE-3): the entry is a `DXGI_MODE_DESC`, and `+0x08` / `+0x0C` are
      the refresh-rate numerator and denominator.*
      - **The refresh pair is read as integers.** `001DC730` loads the selected entry and stores `[entry+0x08] ÷ [entry+0x0C]`
        (unsigned `div`) at object `+0x30` (`001DC76F`–`001DC784`), after applying `+0x00`/`+0x04` through `001DDBA0`.
      - **There is no double.** The `movsd [+0x10]` above is the compiler's 8-byte copy idiom, which moves the two dwords
        `+0x10` and `+0x14` together. Nothing reads `+0x10` as a float.
      - **The layout is exactly `DXGI_MODE_DESC`** (28 bytes): `Width`, `Height`, `RefreshRate.Numerator`,
        `RefreshRate.Denominator`, `Format`, `ScanlineOrdering`, `Scaling`. The adapter layer that fills these tables stores
        DXGI-layout records elsewhere too: the 0x130-byte adapter descriptions of
        [the Config screen](../../16-UI/Config-Screen/the-config-screen-and-what-a-setting-change-runs.md) §11.
      - **Not read:** a consumer of `+0x10`–`+0x18`, so `Format` / `ScanlineOrdering` / `Scaling` rest on the layout match.
      - *Swept 2026-09-18 (FABLE):* every listed function that strides 28-byte entries (`imul …, 0x1C`) was tested for a read at `+0x10`, `+0x14` or `+0x18` off that stride. Only two touch them, and neither consumes them: `001DD420` copies an entry (`movsd [+0x10]`, `mov [+0x18]`, `001DD626`–`001DD642`) and `001DD8E0` sorts (`001DDA09`–`001DDA1E`). No function reads `Format`, `ScanlineOrdering` or `Scaling` as fields, so the layout match remains the only evidence for those three names, and the swap chain must take its format from elsewhere. A consumer reached through a pointer copied out of the table would escape this sweep.
- [x] **What the mode names map to.** `Super Wide Mode` and `Normal Mode` sit beside `Window`, `FullScreen` and `BorderLess`; whether mode `0`/`1` in this record is that same enumeration is **not** established.
      *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (UE-4):* **by code, not adjacency.** `001DCE20`
      tests `[record] == 1` and passes `"Super Wide Mode"` (`00900960`) for mode 1 or `"Normal Mode"` (`00900970`) for mode 0 to
      `001A1E40`, writing into object `+0x80` (`001DCE26`–`001DCE43`). `Window`, `FullScreen` and `BorderLess` are not selected
      by this field.
- [x] ~~**`01F82D18` and `01F82D20`** - two globals eight bytes apart, neither laid out.~~
      *Answered 2026-09-14 (FABLE): `01F82D20` is the settings singleton and `01F82D18` the display object; the eight bytes
      are adjacency, not a relationship.* No register id carries this box, so it is not queued.
      - **`01F82D20`** is `GameSettingConfig`: 31 `u32` settings at `index × 4`, stored once at `00798261` after
        `GameSettingConfig_InitDefaultsAndPath`
        ([game settings](../../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md) §2).
      - **`01F82D18`** is the 0x180-byte display object. `001DDA70` builds it, `001DC5C0` constructs it, and the getter is
        `001DDAB0`. The fields read so far
        ([the Config screen](../../16-UI/Config-Screen/the-config-screen-and-what-a-setting-change-runs.md) §11, `UE-2`, `UE-3`):

        | field | contents |
        |---|---|
        | `+0x00` | aspect mode (1 = super wide, `001DCE20`) |
        | `+0x10` / `+0x14` | fitted width / height |
        | `+0x18` | live screen mode, copied from setting 2 |
        | `+0x20` | mode count |
        | `+0x24` / `+0x28` | display-mode index / `DXGI_MODE_DESC` table |
        | `+0x30` | refresh rate, integer Hz |
        | `+0x38` / `+0x40` | window-size index / table |
        | `+0x48` / `+0x4C` | selected / current adapter |
        | `+0x50` / `+0x58` | adapter count / usable mask |
        | `+0x60` / `+0x64` | monitor, selected and current |
        | `+0x78` | adapter table: 0x140-byte records, a 0x130-byte description plus the output count and outputs |

## 7. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| the two constants are `16/9` and `16/3` | read from `008C5B38` and `00900A0C` | 1 |
| the three branches and every field each writes | full disassembly of `001DDAC0` | 1 |
| **branch C divides integers and never writes `+0x08`** | `001DDB63`, `001DDB7D`, and the absence of any store to `+8` between `001DDB53` and `001DDB9E` | 1 |
| the argument order is `(record, W, H)` | the logger's format string and the registers it forwards at `001DDC22`-`001DDC39` | 1 |
| the `0x1C`-stride resolution table | `001DC754`-`001DC764` | 1 |
| `001DDAC0` is absent from the function census | literal lookup; it is reached only by the tail jump | 1 |
| **what any of this looks like on screen** | **not established** | - |

## 8. Related

- [`../../99-Unresolved-Residual/Unlisted-Code/referenced-code-the-list-never-had.md`](../../99-Unresolved-Residual/Unlisted-Code/referenced-code-the-list-never-had.md) - where `001DDAC0` was found
- [`../../00-Engine-Core-Runtime/Developer-Tuning-Console/what-the-console-tunes.md`](../../00-Engine-Core-Runtime/Developer-Tuning-Console/what-the-console-tunes.md) - the other place these mode strings appear
- [`../../19-Save-Load-Settings/Game-Settings-Config/`](../../19-Save-Load-Settings/Game-Settings-Config/) - where a chosen resolution would be persisted

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Application — CLIENT.** `FUN_0017d6b0`, owned by that layer, calls `001DDA70` on this page. That caller is a 45-byte startup sequencer: six calls in fixed order and a tail-jump into a final one, with no work of its own; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Input — CLIENT.** `FUN_001e0c30`, owned by that layer, calls `00225680` on this page. That caller is a 25-byte forwarder: it takes the singleton, reads its `[+0xDF8]` member and tail-jumps with it; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Audio — MECHANICAL (SWE2-CONTRACT 2026-09-15, 38 edges).** All 38 edges are Audio bodies calling
three shared helpers this page cites — `001DDAB0`, `00225680` and `002256A0` — the same
mode/option-state reads the whole audio layer makes. The fan-in belongs to the helpers, not to the
aspect-fit mechanism.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

**Platform — DEPENDENCY, four edges: the fit reads a mode list the platform layer builds.**
- The display object's constructor `001DC5C0` calls the platform-filed `001DD170` and the mode-list builder
  `001DD420`.
- `001DD420` enumerates monitor modes through the DXGI output walk `006242C0`, then inserts each mode through the
  sorted `0x1C`-record find-or-append `001DD8E0` that this page cites.

The width, height and aspect this page fits against therefore come from that list. How the list is enumerated
belongs to the platform/display pages (`game-settings-ini-and-runtime-config`); this page makes no claim about it.

**Save_Load_Settings — DEPENDENCY, one edge.** The resolution setter `001DDBA0` (`[Screen Mode]setResolutionSize`)
calls `GameSettingConfig_WriteFile` (`001DFD40`), so a mode change is persisted to the settings file. The file's
format and the other settings belong to the settings layer's `CONTRACT-game-setting-config`.

*Tier 2: ledger names, sizes and `edges.tsv`, with roles as the cited pages read them; no body read for this note.
The two R6 tripwires through `0017D6B0` (Platform, Resource) are held by R6 and are not findings.*
