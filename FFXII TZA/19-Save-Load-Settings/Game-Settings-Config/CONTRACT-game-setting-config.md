---
contract: The GameSetting.ini configuration object — construct, load, parse, apply, serialize
category: 19-Save-Load-Settings
scope: subsystem
readiness: RUNTIME VALIDATED   # EXP-001, controlled A/B, 2026-09-08; layout/initialisation corrected 2026-09-10
confidence: PROVEN
implements: game-settings-ini-and-runtime-config.md
entries: [007980A0, 001DE050, 001DED50, 001DE5D0, 001DEE90, 001DFD40, 001DF240, 001DE4F0, 0017D8F0, 0022BDF0, 001EDDC0]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 66 addresses cited - 15 data, 24 entry, 25 interior, 2 literal, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-10
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-game-setting-config-pass-1  # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — the GameSetting.ini configuration object

> **The first behavioural contract in this database.** It formalises
> [`game-settings-ini-and-runtime-config.md`](game-settings-ini-and-runtime-config.md), which is
> `L1` prose, into something an engineer can reimplement and a differential test can be written
> from. **Type layout lives in `_types/` (`GameSettingConfig`, 39 fields; 1 undeclared byte of tail padding at `+0x65B`).**
>
> **Readiness is `RUNTIME VALIDATED`.** *(This line said "`CONTRACT READY` … §13 is empty" until
> 2026-09-08. It was stale: `EXP-001` populated §13 with a controlled A/B, and §13a has since added
> a 31-way prediction. The frontmatter has said `RUNTIME VALIDATED` throughout, so the document
> contradicted itself.)*

## 1. Purpose

Holds every option the player can set — language, resolution, screen mode, graphics quality, volume,
mouse sensitivity, the confirm button, the frame rate — as **31 integers**, persists them as text to
`GameSetting.ini`, and hands them to the engine at startup. It is constructed **before `main`** and
lives for the whole process.

## 2. Interface

| operation | entry | conv | signature | returns |
|---|---|---|---|---|
| construct singleton | `007980A0` (2153 B) | MS x64 | `(…)` — builds path, allocates `0x65C`, stores to `0x01F82D20` | — |
| init defaults + path | `001DE050` (293 B) | MS x64 | `(Config* rcx, const wchar_t* path rdx)` | `rax = rcx` |
| load or create file | `001DED50` (278 B) | MS x64 | `(Config* rcx)` | `eax = 0` on the load path |
| parse text | `001DE5D0` (1919 B) | MS x64 | `(Config* rcx, char* buf rdx)` | — |
| serialize text | `001DEE90` (944 B) | MS x64 | `(Config* rcx, char* out rdx)` — `rdx = NULL` measures | `eax` = length |
| write file | `001DFD40` (214 B) | MS x64 | `(Config* rcx)` | — |
| init value tables | `001DF240` (110 B) | MS x64 | `(Config* rcx)` | `eax = 0` |
| apply quality preset | `001DE4F0` (71 B) | MS x64 | `(Config* rcx, int quality edx)` | — |
| get FrameLimit | `0017D8F0` (11 B) | MS x64 | `()` | `eax = cfg->setting[18]` |
| apply frame limit | `001EDDC0` (165 B) | MS x64 | `(int isSixty ecx)` | — |

**Return semantics.** `001DED50` returns `0` on the *load* path and reaches the create path only when
`_wfopen_s` yields `NULL`; the value is not an error code. `0017D8F0` dereferences `0x01F82D20`
**without a null check** — safe only because construction precedes `main` (§4).

## 3. Types

**`GameSettingConfig`, size `0x65C`.** Full layout in `_types/fields.tsv`; regenerate with
`types_index.py --type GameSettingConfig`. Summary:

| offset | size | field | notes |
|---|---:|---|---|
| `+0x000`–`+0x078` | 124 | `setting[31]` | `int32`, **offset = index × 4** |
| `+0x07C` | 324 | `valueTableA` | 81 dwords from `01DFDA10`; **meaning UNRESOLVED**, and **no reader exists** — see the no-reader invariant below |
| `+0x1C0` | 324 | `valueTableB` | 81 dwords from `01DFDB60`; **meaning UNRESOLVED**, and **no reader exists** — see the no-reader invariant below |
| `+0x304` | 324 | `valueTableC` | 81 dwords from `01DFDCB0`; **meaning UNRESOLVED**, and **no reader exists** — see the no-reader invariant below |
| `+0x448` | 4 | `valueTableCount` | `81` **after `001DF240`**; uninitialised before it — §4a |
| `+0x44C` | 4 | ~~UNRESOLVED~~ **`msaaModeSupportMask`** *(2026-09-14, FABLE)* | set to `1` before the defaults copy; bits 1–5 are set by the D3D11 `CheckMultisampleQualityLevels` probe `00628690` → `0017D9C0` → `001DF2B0`, and read by the MSAA cycle `001DF2C0` ([the console slice I](../../00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-I-ids-268-293.md) §9) |
| `+0x450` | **520** | `iniPath` | **`wchar_t[0x104]`**, `+0x450`–`+0x657` — see the note below |
| ~~`+0x554`~~ | — | ~~UNRESOLVED span~~ | **NOT A FIELD** — the second half of `iniPath`; row removed from `_types/fields.tsv` 2026-09-10 |

> **`iniPath` is wide, and it is one field, not two.** `007980A0` builds it for `_wfopen_s`, so the
> characters are `wchar_t`. **The ABI settles the capacity, not the arithmetic** (strengthened
> 2026-09-10): the PE import directory resolves the copy's target `008C3008` to
> `api-ms-win-crt-string-l1-1-0!wcscpy_s`, whose second parameter is `rsize_t numberOfElements`
> — **wide characters**. `001DE152` loads `0x104` into it, so the destination is declared
> `wchar_t[260]`. The argument *order* is independently decisive: `rdx` carries the immediate and
> `r8` the source pointer, which fits `wcscpy_s(dest,count,src)` and rules out
> `wcsncpy(dest,src,count)`. It is the image's only `wcscpy_s` call site. The arithmetic then
> merely agrees: `0x450 + 0x104 × 2 = 0x658`,
> which is exactly where the next known field begins. A `wchar_t[0x104]` therefore occupies
> `+0x450`–`+0x657` and **swallows the "unresolved 260-byte span" at `+0x554` entirely**.
>
> That also dissolves the puzzle §11 recorded — *"no config function writes `+0x554`"*. Nothing
> writes it **as a separate field** because it is not one; it is the tail of a path buffer that is
> only ever filled to its used length. Read live, the path was 104 characters — 208 bytes — so the
> bytes at `+0x554` were **all zero**, exactly as an unused tail should be.
>
> **Read as narrow the field yields `"C"`** — the first character followed by a NUL high byte —
> which is how it came to be recorded as a 260-byte field with a mysterious twin.
| `+0x658` | 2 | UNRESOLVED | `0x0101` at construction, `0` after a successful load |
| `+0x65A` | 1 | UNRESOLVED | `1` at construction, `0` after a successful load |

**Three parallel image tables drive it**, and the count **31** is established five independent ways
(loop bound, key-table NULL terminator, value-table end, `memset` origin at `0x7C`, mask length):

```
keys          0x01DFD050   31 × char*
value names   0x01DFD150   31 × 9 × char* — 9 is the row width, not a terminator guarantee: row 0 (Language) uses all nine slots (jp en fr de it es kr ch cn); other rows NULL-pad the tail (corrected 2026-09-25, OPUS-REQ-CONTRACT-THREE-STATE-CORRECTIONS-BLOCK-214)
preset matrix 0x00900CE0   31 × 16 B  — four int32 columns, indexed by Quality
preset mask   0x00900CC0   31 × 1 B   — 1 = the quality preset drives this setting
```

## 4. Preconditions · postconditions · invariants

**Preconditions.** `001DE050` requires a `0x65C` block. **It is *not* zeroed** — corrected
2026-09-10: `00798239` `mov ecx,0x65C` tail-calls through `00210EC0` -> `0085E730` -> IAT
`008C2B40` = `api-ms-win-crt-heap-l1-1-0!malloc`. A reimplementation must not assume zero fill;
see the initialisation extent in §4a. `0017D8F0` requires the
singleton to exist — guaranteed because `007980A0` is reached from `007A3770` ← `00808D78`
(`MSVCCRT.ExecutableStartup`), i.e. **CRT static initialisation, before `main`**, and `0022BDF0` is
the *first call* in `0022A0B0`.

**Postconditions.** After `001DE050`: all 31 settings hold **column 0** of the preset matrix, except
`setting[0]` (locale-derived, §8) and `setting[1]`/`setting[11]` (desktop-derived); `+0x07C..+0x447`
zeroed — and **only** that span, by the single `memset` at `001DE138`
(`008C2A60` = `VCRUNTIME140!memset`, `r8d = 0x3CC`); `+0x448` **uninitialised heap** until
`001DF240`; `+0x44C = 1`; `+0x658 = 0x0101`; `+0x65A = 1`.

**Invariants.**
- `setting` offset **= index × 4**, always.
- **Exactly one write path per field**: no literal `[reg+0xNN]` store to a setting exists anywhere;
  all writes go through a computed index. A displacement-keyed scan cannot see them — this is a
  recorded blind-spot shape.
- `valueTableCount == 81` whenever the tables are initialised.
- **NOTHING READS `valueTableA/B/C`, AND THEY ARE LIVE ONLY ON A FIRST RUN.** *(OPUS 2026-09-20;
  CON-122.)* `001DF240` is their only writer and `001DED50` calls it **only** where `_wfopen_s`
  yields `NULL`, immediately followed by `001DFD40` writing the file out. The parser `001DE5D0`
  touches **no** displacement in `+0x07C..+0x447`, so the ini cannot set them; `001DFD40` touches
  only `+0x450`, so they are never persisted. **Therefore on every run after the first, `memset(obj
  + 0x7C, 0, 0x3CC)` clears the block and nothing refills or reads it.** A call-graph fixpoint
  census over the config pointer — **77 functions**: all ~~**60**~~ that load `*(0x01F82D20)` — 63 functions with 158 reads and 1 write by `retool.py refs 01F82D20` *(corrected 2026-10-02, OPUS: no page figure matches the image)* — plus
  `001DE050` and `001DED50` seeded at `rcx` from the construction site, propagating `rcx`/`rdx`/
  `r8`/`r9` into callees and carrying **interior-pointer offsets** so that `001DF240`'s
  `[rax-0x144]`/`[rax]`/`[rax+0x144]` resolve to `+0x07C`/`+0x1C0`/`+0x304` — finds **exactly four
  accesses in the whole `0x3CC` range, and all four are those writes**. `00798261` is the only
  store of the object pointer, so nothing reaches them by another route.
  **For reconstruction this is a licence, not a gap**: reproduce the copy on the no-file branch for
  byte-fidelity, and **do not wire the tables to any consumer** — the original has none, so any
  consumer added is a divergence, not a completion. *Bound: the census is an intra-procedural linear
  scan without control-flow merge that follows callees only through argument registers; it can
  under-report and does not exclude a reader reached by a pointer chain it does not model.* **Computed-offset accesses were tested separately, because that is the exact shape that has defeated absence claims in this database before (`UQ-339`, `W-9` — names composed at run time, missed by a literal census).** The analogue here is an offset carried in an index register rather than a literal displacement, which a displacement-keyed census logs at `+0x00`. Re-run recording every `[cfg + reg*scale + disp]` through a tainted base, the whole fixpoint yields **five** such accesses — `001DEC90`, `001DF343` and three in `001DF350` — and **all five are WRITES of the form `mov dword [cfg + reg*4], value`, i.e. `setting[index] = value`. None is a read, and none lands in the table range.** The no-reader result survives the test it was most likely to fail.
- **THE INI KEY LOOKUP IS BOUNDED; THE SETTER IT FEEDS IS NOT, AND THE BOUND LIVES ENTIRELY IN THE
  CALLERS.** *(OPUS 2026-09-20.)* Stated as two separate facts because only the first is proven end
  to end.
  **Proven**: the key lookup at `001DE882`–`001DE8AD` walks the 31-entry key table
  (`mov rdx,[r12 + rdi*8 + 0x1CDD050]`, `r12 = 0x120000`, so `01DFD050`) under a hard
  `cmp ebx, 0x1F` / `jb`, and `ebx == 0x1F` is the **not-found** path: `001DE8B2 jne` falls through
  to the diagnostic `0017D280` with `00901060 = "[ConfigFile] invalid key at [%s].
"` and **writes
  nothing**. So a *matched key* resolves to **0..30** and an *unmatched key* produces no write.
  **Not proven, and deliberately not claimed**: that this index is the one reaching the store. The
  settings writes are all computed-index stores — `mov dword [cfg + reg*4], v` at `001DEC90`
  (`001DE5D0`), `001DF343` (`001DF340`) and three sites in `001DF350` — and **neither setter bounds
  its own index**. `001DF340` is the whole of it:
  `movsxd rax, edx ; mov dword ptr [rcx + rax*4], r8d ; xor eax,eax ; ret` — ten bytes, no
  comparison, and the `movsxd` means a **negative** index writes *below* the object. `001DF350`
  takes its index as the fourth argument (`r15 = r9` at `001DF39A`) and has no `cmp` against 31
  near its three stores; the nearby comparisons are string-SSO and value-range tests. `001DF340` has
  ~~roughly twenty-five callers across the `0079xxxx` settings-load band~~ 38 call sites in 15 functions *(corrected 2026-10-02, OPUS: `retool.py callers 001DF340`; language-selection-and-locale-ids.md AV-3 counts the same 38)*.
  **For reconstruction**: the safety of `+0x7C` and beyond rests on *every caller* passing a bounded
  index, not on the setter. A reimplementation that adds a bounds check inside the setter changes
  behaviour the original does not have, and one that trusts the setter while relaxing a caller opens
  a write past the settings array. **Which callers establish the bound is not traced here** — only
  the ini-key path is, and only as far as the lookup.

### 4a. Initialisation extent — what construction leaves undefined

Established 2026-09-10 by reading the allocation and every bulk write in the constructor.

| span | who initialises it | state after `001DE050` returns |
|---|---|---|
| `+0x000`–`+0x078` | the 31-iteration defaults copy `001DE092`–`001DE0A3` | defined |
| `+0x07C`–`+0x447` | `memset(obj+0x7C, 0, 0x3CC)` at `001DE138` | zero |
| `+0x448` | **nobody** — `001DF2A0` writes `0x51` later, in `001DF240` | **undefined** |
| `+0x44C` | `001DE075` | `1` |
| `+0x450`–`+0x657` | `wcscpy_s` at `001DE157`, **and only when `rdx != NULL`** | the path and its NUL; **every byte past that NUL undefined** |
| `+0x658`, `+0x65A` | `001DE069`, `001DE07B` | `0x0101`, `1` |
| `+0x65B` | nobody observed | **undefined** (1 byte of tail padding to `0x65C`) |

**This resolves the `+0x448` contradiction §13 recorded.** §3 said *"always 81"*, §4 said *"unset
until `001DF240`"*, and the live read returned **0**. All three are consistent once the allocation
is known to be `malloc`: `+0x448` is uninitialised heap, and a fresh page from the OS reads zero.
`valueTableCount == 81` is an invariant **only after `001DF240` has run**, not a construction
postcondition — `_types/fields.tsv` now says so.

**Consequence for reconstruction.** A C reimplementation that declares the object as a static or
`calloc`s it will diverge from the original in `+0x448` and in the `iniPath` tail before the
respective writers run. No consumer of those bytes is known, so the divergence is currently
unobservable — but it is a real difference, and a differential harness that poisons the whole
object will see it.

## 5. State

| | detail |
|---|---|
| **read** | `0x01DFD050`, `0x01DFD150`, `0x00900CE0`, `0x00900CC0`, `0x01DFDA10/B60/CB0` |
| **written** | `0x01F82D20` (the singleton pointer, **1 write in the whole image**, at `00798261`); the object; and on the `FrameLimit` path `0x01DFE0B4/B8/BC`, `0x01F82E38/3C/40` |
| **allocated** | one `0x65C` block at `00798239` via `malloc` (IAT `008C2B40`), **not zeroed**; the parse and serialize paths `alloca` a file-sized buffer |
| **deallocated** | none — the singleton is never freed; **no destructor identified** |

`globals_index.py --addr 01F82D20` → **1 writer, ~~61 readers~~** 63 functions referencing it, 158 reads and 1 write *(corrected 2026-10-02, OPUS: `retool.py refs 01F82D20`)* (RIP-relative instrument).

## 6. Relationships

`00808D78` → `007A3770` → `007980A0` → { `001DE050`, `001DED50` } → { `001DE5D0` parse | `001DF240` + `001DFD40` create }.
Consumers: `0017E070` is the Config screen's per-row reader — a **23-arm jump table returning one
value**, covering **16 distinct settings across all arms** (corrected 2026-09-08; it was described here
as reading 16 settings in one pass, which the count justified and the mechanism did not — see
[the Config screen](../../16-UI/Config-Screen/the-config-screen-and-what-a-setting-change-runs.md) section 8); `001D5120` applies the graphics preset then
pushes settings into the renderer; `0017D8F0` → `0022BDF0` → `001EDDC0` applies `FrameLimit`.

**The trigger for the whole graphics-apply chain is now established:** a left/right press on a Config
screen row. `AX-6a` is answered, and `AX-6` is answered **NO** — nothing applies a quality preset at
startup.
**EH funclet edges excluded throughout.**

## 7. State transitions

```
(no object)
   ──[007980A0 allocates 0x65C]──▶ RAW
RAW ──[001DE050]──▶ DEFAULTED          setting[] = preset column 0, +0x658=0x0101, +0x65A=1
DEFAULTED ──[001DED50, file opens]──▶ LOADED    +0x658=0, +0x65A=0, then 001DE5D0 parses over it
DEFAULTED ──[001DED50, no file]──▶ CREATED      001DF240 fills the three tables, 001DFD40 writes the file
LOADED|CREATED ──[001DE4F0, quality != current]──▶ PRESET-APPLIED
```

**`001DE4F0` is guarded by `if (cfg->setting[3] == quality) return;`** — re-applying the same quality
is a no-op, so a startup call with the current value cannot reconcile the mismatch noted in §10.

## 8. Script · resource · event interactions

None. The only external inputs are the OS (locale, desktop metrics) and `GameSetting.ini` itself.

**Locale mapping** (`001DE0C0`, primary id = `LANGID & 0x3F`):

```
LANGID ∈ {0x0404, 0x0C04, 0x1404}      → 7  ch (Traditional)     [0x1C04 explicitly excluded]
0x11 → 0 jp | 0x0C → 2 fr | 0x07 → 3 de | 0x10 → 4 it | 0x0A → 5 es | 0x12 → 6 kr | 0x04 → 8 cn
anything else                          → 1  en
```

## 9. Determinism

**RNG:** none. **Timing:** entirely pre-`main` except the preset applier, which runs from a
`lea`-registered graphics callback whose firing time is ~~**UNRESOLVED**~~ a left/right press on a Config-screen row *(answered: see "The trigger for the whole graphics-apply chain is now established", after the call chain; 2026-10-02, OPUS)* (`AX-6a`). **Threading:** all
observed access is single-threaded during startup; no synchronisation primitive appears in any of the
eleven entries. **Not proven to be single-threaded afterwards.**

## 10. Failure paths and edge conditions

- `_wfopen_s` fails → create path; the file is written from defaults.
- Parse errors emit `[ConfigFile] invalid key/line/Resolution at [%s]` and **skip the line**.
- `001DE4F0` with `quality == 3` (`VQ_CUSTOM`) **writes nothing** — column 3 is never read.
- **The startup mismatch:** init copies **column 0 (`VQ_LOW`)** into every preset-driven setting while
  `Quality`'s own column-0 value is **`1` (`VQ_MEDIUM`)**. Until something reconciles them the config
  says "Medium" while holding Low values, and the guard in §7 means a same-value call will not fix it.
  **Whether this is ever observable is UNRESOLVED.**
- `FrameLimit` reduces to a boolean: **any value that is not exactly `1` yields `0`**.

## 11. Observable behaviour

- `GameSetting.ini` contains `Key=ValueName` per line; `Resolution`/`WindowSize` as `1920*1080`,
  stored as **`(width << 16) | height`** (§13a);
  single-value settings as a raw integer.
- `DecideButton` selects Circle vs Cross at runtime and re-applies the masks immediately.
- `FrameLimit=60` doubles every authored 30 fps duration and **releases** the multimedia timer;
  `FrameLimit=30` leaves `{1, 1.0f, 1.0f}` standing and **raises** it via `timeBeginPeriod`.
- A fresh install writes a file whose `Resolution` matches the desktop and whose `Language` matches
  the OS UI language.

## 12. Reproduction formula

```c
/* offset of setting i */                 offset = i * 4;
/* default of setting i */                cfg->setting[i] = matrix[i].col[0];
/* quality preset */                      if (mask[i] && quality != 3) cfg->setting[i] = matrix[i].col[quality];
/* resolution encoding */                 packed = (width << 16) | height;      /* 1920*1080 = 0x07800438 */
/* frame-limit mode */                    isSixty = (cfg->setting[18] == 1);
/* authored duration → frames */          frames  = authored30fpsFrames * timeBase;   /* timeBase ∈ {1,2} */
/* angle-bias style unit conversion */    /* none in this subsystem */
```

## 13. Runtime validation

**DONE 2026-09-08, and it is a controlled experiment rather than an observation.** [`EXP-001`](../../_experiments/EXP-001-gamesetting-frametimebase.md), run autonomously against a verified-clean process.

The three cheap confirmations this section asked for all passed — `setting[18]`, the time base
reading `1` or `2`, and `+0x658`/`+0x65A` reading `0` after a load. **Then the input was
varied.**

| row | `FrameLimit=60` | `FrameLimit=30` |
|---|---:|---:|
| `setting[18]` `+0x48` | **1** | **0** |
| `0x01DFE0B4` time base | **2** | **1** |
| `0x01DFE0B8` scale | **2.0** | **1.0** |
| `0x01DFE0BC` inverse | **0.5** | **1.0** |
| `0x01F82E38` 60 Hz gate | **1** | **0** |
| Language / Quality / Shadow / DecideButton *(not varied)* | 1 / 3 / 2 / 1 | 1 / 3 / 2 / 1 |

> **One edited line in `GameSetting.ini` moved all five predicted values and left four control
> fields untouched.** §15's *“`FrameLimit` drives the time base”* was `PROVEN` from the static
> chain; it is now proven again by **intervention**, which is a different and stronger thing.

**Two runtime facts this section did not predict:**

1. **The application is not atomic with construction.** Observed at the first instant the
   settings singleton is non-null, `setting[18]` was already `1` while the time base was still
   `1` — the engine starts on the 30 fps base and switches later in startup. `PROBABLE`; the
   window's length is unmeasured.
2. **`+0x448` is not `81` at these moments.** Three runs gave `0`, `0x69705F70` and
   `0x41505F50` — the latter two ASCII text. §4 already qualifies the claim as holding *“whenever
   the tables are initialised”*; what the field holds before that is **unresolved**, `EO-1`.
   *Status 2026-09-26 (FABLE, Claude Opus 5.5): `EO-1` is ANSWERED from this contract's own §4a and the CON-122 note,
   re-checked on the bytes. 81 is written by one instruction in the image, `001DF2A0`, inside `001DF240`. Its only caller
   reaches it on the NULL-handle branch of the ini open (`001DED97`), so the field is 81 only after a run that creates
   the settings file. Before that, and on every run that finds the file, it is uninitialised heap. Control:
   `_index/candidates/eo1-value-table-count/eo1_448.py`.*

**Environment:** the vanilla Steam install, structurally verified clean and hashing to the
authority build, with no mod module in the live process. Settings file hashed before the change
and restored to the same hash after.

### 13a. Every setting predicted, then read — 2026-09-08

`EXP-001` varied **one** setting and watched five values move. This is the complementary run: **all
31 predicted in advance from sources independent of the object**, then read once.

**The oracle.** `GameSetting.ini` on disk says what the player chose; the key table at `01DFD050`
(31 pointers, **NULL terminator at index 31**, confirming the count a sixth way) and the value-name
table at `01DFD150` say how a name becomes an integer; this contract says the integer lives at
`index × 4`. Nothing in that chain reads the object.

| | |
|---|---|
| predicted exactly | **29 of 31** |
| mismatched | **0** |
| not predictable from the name tables | **2** — `Resolution` and `WindowSize`, resolved below |

Two of the 29 are the ones worth having, because a careless reader gets them wrong:
**`Anisotropic=16` stores as `4`** (an index into `1, 2, 4, 8, 16`, not the value 16) and
**`FrameLimit=60` stores as `1`** (an index into `30, 60`). A reimplementation writing the literal
would be wrong on both.

### `Resolution` and `WindowSize` are packed, and the `*` is a separator

The two the name tables could not explain hold **`(width << 16) | height`**:

```text
ini:  WindowSize=1916*1033
live: 125568009 = 0x077C0409       0x077C = 1916      0x0409 = 1033
```

**The `*` in the file is a separator, not multiplication** — the product is 1,979,228, which is not
the stored value. Both fields hold the same packing.

### The path names the per-account file, and doubles a separator

```text
C:\Users\<user>\Documents\My Games\FINAL FANTASY XII THE ZODIAC AGE\76561198045890736\\GameSetting.ini
```

**The engine reads the Steam-ID subdirectory's copy, not the one beside it in the parent folder** —
there are three `GameSetting.ini` files on this machine and the object names exactly one. Note the
**doubled backslash** before the filename, which Windows tolerates; a reimplementation joining paths
more carefully would produce a different string and the same file.

### The other fields, against what this contract claims

| field | live | the contract says | verdict |
|---|---|---|---|
| `+0x448` | **0** | §3 *"always 81"*; §4 *"unset until `001DF240`"* | **§4 was right and §3 has been corrected.** Cause established 2026-09-10 (§4a): the block is `malloc`ed, the constructor's `memset` stops at `+0x447`, so `+0x448` is uninitialised heap until `001DF240` — and a fresh OS page reads zero, which is what was observed. Consistent with `EXP-001` and `EO-1` |
| `+0x44C` | **1**, then **15** on a second run | *"set to 1 before the defaults copy"* | **not a constant.** Evidence added to `AX-5` |
| `+0x658` | `0x0000` | `0x0101` at construction, `0` after a load | **confirms a load happened** |
| `+0x65A` | `0` | `1` at construction, `0` after a load | **confirms a load happened** |

**Base control passed** (the module loads at its PE `ImageBase`), and the singleton at `01F82D20`
was non-null, as §4 requires of anything constructed before `main`.

**Experiment records that name this contract** — found by `OPUS-CONTRACT-RUNTIME-AUDIT`, 2026-09-13. Each names this
contract in its own `contract:` frontmatter while this section did not cite it back.

- [`EXP-041`](../../_experiments/EXP-041-config-pointer-closure.md) — **method A**, retained-evidence assessment, live_game: false.

**None of these is a live run**, so none of them changes the evidence-class statement at the
top of this section. They are listed because a reader auditing what has been executed against
this contract should not have to find them from the experiment side only.

## 14. Unresolved

1. `valueTableA/B/C` — 3 × 81 dwords, layout proven, **meaning unknown**.
2. ~~The **260-byte span at `+0x554`**.~~ **RESOLVED 2026-09-10 — it was never a field.** See
   §5's note and §15: `008C3008` is `wcscpy_s`, whose second argument counts **wide characters**,
   so `edx = 0x104` declares a `wchar_t[260]` = 520 bytes at `+0x450`, ending at `+0x657`. The
   "span" was the second half of `iniPath`. `_types/fields.tsv` no longer carries the phantom row.
3. ~~`+0x44C`~~ **is the MSAA AVAILABILITY MASK** — one bit per sample count, built by probing the
   device. `00628690` loops counts 2..32 calling `ID3D11Device::CheckMultisampleQualityLevels`
   (vtable `+0xF0`) with `DXGI_FORMAT_R8G8B8A8_UNORM`, and for each count whose `levels > 0` sets a
   bit: **2x -> bit 1, 4x -> bit 2, 8x -> bit 3 (and bit 4 when `levels > 16`), 16x -> bit 5**; bit 0
   is the constructor's `1`. So the 1-then-15 a reader sees is **the D3D11 probe having run or not**,
   not a magic number.

   > **Why the displacement census found no writer:** the only post-construction writer is the bit
   > setter `001DF2B0` (`bts [rcx+0x44C], edx`), reached through the thunk `0017D9C0`
   > (`edx = ecx`, `rcx = [01F82D20]`, `jmp 001DF2B0`), and **neither is in the function list's
   > caller graph**. A raw `E8` scan of `.text` finds the thunk's two call sites in `00628690`,
   > called once from the device set-up `00625830`. **The second contract in this backlog whose
   > missing writer was hiding behind a thunk** — see `V-6` in CONTRACT-save-image-buffers.

   `+0x658` and `+0x65A` remain written at known points with meaning unknown (`AX-5`). Folded from
   FABLE's AX-5 note by OPUS 2026-09-13.
   > *Answered 2026-09-12 (FABLE, AX-5). **FOLDED BY OPUS 2026-09-13**; the item above carries it, and `+0x658` / `+0x65A` stay open.* **`+0x44C`
   > is the MSAA availability mask, and the 1-then-15 is the D3D11 probe having run or not.** The
   > only writer after construction is a bit setter, `001DF2B0` (`bts [rcx+0x44C], edx`), reached
   > through the thunk `0017D9C0` (`edx = ecx`, `rcx = [01F82D20]`, `jmp 001DF2B0`) — neither is in
   > the function list's caller graph, which is why the displacement census found no writer; a raw
   > `E8` scan of `.text` finds the thunk's two call sites in **`00628690`**, called once from the
   > device set-up `00625830` (`00625E7C`). `00628690` loops sample counts 2..32 calling the device's
   > vtable slot 30 (`+0xF0`) with format `0x1C` and `&levels` — `ID3D11Device::
   > CheckMultisampleQualityLevels(DXGI_FORMAT_R8G8B8A8_UNORM, count, &levels)` — and for each count
   > with `levels > 0` sets a bit: **2× → bit 1, 4× → bit 2, 8× → bit 3 (and bit 4 when `levels >
   > 16`), 16× → bit 5** (`006286D7`–`00628714`); bit 0 is the constructor's `1` (`001DE075`), the
   > "off" option. So `15` is a GPU offering 2×, 4× and 8× at R8G8B8A8, and `1` is a read taken
   > before the device probe or on a device without MSAA. **The reader** is `001DF2C0`, called only
   > by the debug menu `001D1660` (`001D4A53`): from the current index in `[01F82D20]+0x20`
   > (setting index 8) it steps forward or back **modulo 5** to the next set bit (`001DF2CB`–
   > `001DF325`), stores the pick back to `+0x20` and returns it — a five-option cycler (off, 2×,
   > 4×, 8×, 8× high-quality) that can never reach bit 5. **`+0x658` and `+0x65A`** (`0x0101` and
   > `1` at construction, both zeroed by `GameSettingConfig_LoadOrCreateFile` after a successful
   > open, `001DED9F` / `001DEDA8`) have **no reader on this object anywhere in the image** (every
   > `+0x658` / `+0x65A` load belongs to other types), so they are fresh-defaults markers whose
   > value is never consulted — a reimplementation may carry them for byte fidelity but cannot
   > diverge on them. Live discriminator for the mask: read `+0x44C` after `00625830` returns.
4. **No destructor identified.**
5. ~~When the graphics callback fires, hence whether §10's mismatch is observable (`AX-6a`).~~ *(answered: on a left/right press on a Config row, so §10's mismatch stands until the player moves `Quality`; `AX-6a`, game-settings-ini-and-runtime-config.md "Resolved 2026-09-08"; 2026-10-02, OPUS)*
6. ~~Which of the 31 the options UI exposes versus ini-only (`AX-2`).~~ *(answered: 22 of 31 — game-settings-ini-and-runtime-config.md `AX-2` and the Config screen page §11; 2026-10-02, OPUS)*

## 15. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| size `0x65C`, singleton `0x01F82D20`, 1 writer | `mov ecx,0x65C` at `00798239`; store at `00798261`; whole-image access scan | 1 | PROVEN |
| 31 settings, offset = index × 4 | five independent derivations (§3) | 1 (static) | PROVEN |
| key / value-name / matrix / mask tables | read from the image; layout re-derived 2026-09-08 | 1 | PROVEN |
| preset matrix columns are indexed by Quality | `[r11 + (quality + i*4)*4]` at `001DE521` | 1 | PROVEN |
| construction precedes `main` | `00808D78` tagged `MSVCCRT.ExecutableStartup`; `0022BDF0` first call in `0022A0B0` | 1 | PROVEN |
| `FrameLimit` drives the time base | full chain read; `mode=NULL`-style boolean reduction at `0022BE18` | 1 | PROVEN |
| ~~`+0x554` unwritten by config code~~ **withdrawn — the claim was about a field that does not exist** | superseded 2026-09-10. The differential and the displacement scan were both correct and both irrelevant: nothing writes `+0x554` *as a field* because `+0x554` is the middle of `iniPath`. The measurement stands as evidence about `001DE4F0`; it never was evidence about a separate span |
| `001DE4F0` writes nothing outside the 31 settings | **measured 2026-09-08** — both sides given the whole `0x65C` object, poisoned byte by byte, compared by hash: **0 bytes changed beyond the settings over 600 cases**. This is the claim the earlier `+0x554` row should have made; a differential on one entry point can support this and never "all config code" | 4 (executed) | PROVEN for this entry point |
| `iniPath` is `wchar_t[260]` at `+0x450`, 520 bytes, `+0x450`–`+0x657` | PE import directory: `008C3008` = `api-ms-win-crt-string-l1-1-0!wcscpy_s`, second parameter a count **in elements**; `001DE152 mov edx,0x104`. Argument order is independently decisive — `rdx` holds the immediate and `r8` the source pointer, which fits `wcscpy_s(dest,count,src)` and not `wcsncpy(dest,src,count)`. It is the image's **only** `wcscpy_s` call site. `0x450 + 0x104*2 = 0x658` = the next PROVEN field | 1 | PROVEN |
| no separate field exists anywhere in `+0x450`–`+0x657` | every memory operand of `001DE050`, `001DED50`, `001DFD40`, `001DF240` and `007980A0` decoded over the full recorded body length; the only displacement in `[0x440,0x660)` other than `+0x448`, `+0x44C`, `+0x658`, `+0x65A` is `+0x450` itself. **Positive control:** `+0x450` appears in three of the four config functions. **Boundary:** these five functions only; code outside them was not searched | 1 | PROVEN for the config functions |
| the `0x65C` block is `malloc`ed, never zeroed | `00798239` -> `00210EC0` -> `0085E730` -> IAT `008C2B40` = `malloc`; the constructor's only bulk clear is `memset(obj+0x7C,0,0x3CC)` at `001DE138` (IAT `008C2A60`) | 1 | PROVEN |
| meaning of the three value tables | **not established** | none | UNKNOWN |
| any runtime observation | ~~**none exists**~~ `EXP-001`, a controlled A/B run 2026-09-08 (§13) *(corrected 2026-10-02, OPUS: the front matter says `RUNTIME VALIDATED # EXP-001`)* | ~~none~~ runtime | ~~UNKNOWN~~ PROVEN |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

This contract's load-bearing claims are two **negatives** and one piece of arithmetic. All three were
re-derived, and the negatives were given the populations that make them mean something.

### "One writer" — and the 156 reads that make it a finding

A whole-image scan for rip-relative references to the singleton `01F82D20`, classifying by operand
position:

| | count |
|---|---:|
| **writers** | **1** — `00798261 mov qword [rip → 01F82D20], rax`, in `FUN_007980A0` |
| readers | ~~**156 references across 61 distinct functions**~~ **158 reads in 63 functions** *(corrected 2026-10-02, OPUS: `retool.py refs 01F82D20`, beside the one write)* |
| `lea` (address taken) | **0** |

**The allocation is `00798239 mov ecx, 0x65C` / `call 00210EC0`**, and the pointer it returns is
stored 0x28 bytes later — one store, in the same function, exactly as §15 says.

> **A single writer beside 61 reading functions is the claim; a single writer beside no readers would
> be an accident.** And **zero `lea`s** matters as much: nothing anywhere in the image takes the
> singleton's *address*, so the one store is the only way its value can ever change.

### "No separate field exists in `+0x450`–`+0x657`" — every operand, not a sample

The span is `wchar_t[260]` = **520 bytes**, and `0x450 + 520 − 1 =` **`0x657`** — the stated end,
exactly. Across all five functions §15 names, **every** memory operand whose displacement falls in
that range is:

```
001DE148  lea rcx, [rsi + 0x450]
001DED78  lea rdx, [rcx + 0x450]
001DFD68  lea rdx, [rcx + 0x450]
```

**Three operands, all at `0x450`, all `lea`.** Not one access anywhere *inside* the 520 bytes, and
not one that reads or writes rather than taking the address. The buffer is only ever handed to
something whole. **The negative holds over the whole span rather than over the offsets someone
thought to check.**

**Not claimed:** the meaning of the three value tables is still `UNKNOWN`, and nothing here is a
runtime observation. The withdrawn `+0x554` row stays withdrawn — this pass found no field there
either, which is consistent with why it was withdrawn.

## 16. Parity plan

**Testable now, statically:** `STRUCTURAL` (layout vs `_types/`), `CALCULATION` (default selection,
preset application, resolution packing, locale mapping), `SERIALIZATION` (round-trip a
`GameSetting.ini` through parse → serialize and compare bytes).

**Requires the running game:** `STATE-TRANSITION`, `INTEGRATION`, `TIMING`.

**Will not be tested, and why:** `RNG` — this subsystem draws none. `PRESENTATION` — the settings'
visual consequences belong to the renderer, not here.

**A parity claim covering only the first group must say so.** Passing a serialization round-trip is
not evidence that the object is built correctly at startup.

## 17. One operation reimplemented and differential-tested — 2026-09-08

**Reconstruction:** [`../../../../Reconstruction/Game/Config/quality_preset.c`](../../../../Reconstruction/Game/Config/quality_preset.c)
**Test:** [`../../../../Reconstruction/Tests/Differential/diff_quality_preset.py`](../../../../Reconstruction/Tests/Differential/diff_quality_preset.py)

**`GameSettingConfig_ApplyQualityPreset` (`001DE4F0`) only.** 600 cases, **0 mismatches** — 532 of
them changing the settings array, 68 leaving it untouched.

### ⚠ The subsystem's readiness does not move

This contract covers **construct, load, parse, apply, serialize**. **One of those five operations is
now differential-tested.** ~~`readiness` stays **`CONTRACT READY`**, because promoting the whole~~
~~subsystem on the strength of its smallest operation is exactly the overstatement the readiness ladder~~
~~exists to prevent.~~ *(corrected 2026-10-02, OPUS: the front matter says `readiness: RUNTIME VALIDATED   # EXP-001`, on §13's controlled A/B, not on this one differential-tested operation)*

### Why this operation was chosen as the second pilot

It is a **different shape** from the first. `FieldMusic_Select` returns a value; this returns nothing
and its entire effect is on the settings array — so the harness had to compare **resulting memory**,
which is what it was written to prove it could do.

It is also **stronger evidence** than the music test in one respect: the mask and matrix are in
`.rdata`, so the emulator feeds both sides **the game's own shipped tables**. The music table is built
at runtime and could only be tested synthetically. **This is parity over real data, not merely over an
algorithm.**

### What the test tries that a careless one would not

**Out-of-range qualities.** The original does not validate `quality`, so `-1`, `4` and `7` index the
matrix outside the intended row — reading a neighbouring row's column, or off the end. Those cases
are in the suite and **both sides agree**, which is the only way to know the reconstruction reproduces
the original's *undefined* behaviour and not merely its intended behaviour.

### Deliberate interface difference

The original reads its tables from fixed addresses; the reconstruction **takes them as parameters**.
A reimplementation that hardcoded the shipped bytes would be transcribing the game rather than
reimplementing it, and could never be run against a modified table. **Behaviour is what is compared,
not the signature.**

### Parity status, for this operation only

| dimension | status |
|---|---|
| `CALCULATION` | **parity**, over the game's own tables |
| `STATE-TRANSITION` | **parity** — the full 31-int array compared after every call |
| `EDGE-CASE` | parity — no-op path, `VQ_CUSTOM`, and out-of-range qualities |
| `INTEGRATION` | **NOT TESTED** — nothing here shows *when* the game calls this, or that the settings object it receives is in the state the test assumes |

**The four other operations in this contract are untested**~~, and `AX-6a` — when the graphics-apply~~
~~callback fires — remains the open question that would make `INTEGRATION` testable at all.~~ *(answered: `AX-6a` is answered — the apply runs on a left/right press on a Config row; 2026-10-02, OPUS)*.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL.*

- **Audio — CLIENT.** The console body `001D1660` calls the console's two audio legs (9 B and 46 B).
- **Movement — SERVICE.** The frame-base setup `001EDDC0` (the `timeBeginPeriod` body) calls a 71-byte movement helper.
  Which value it passes on is not read here.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — CLIENT.** The frame-base setup and an 11-byte cited body are called by the 146-byte core start-up helper, which the start-up subtree's root calls, so both run during core start-up.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**ActorEntity — SERVICE.** `0022A0B0` on this page calls `BattleStorage_InitializeWorkArrays`, owned by that layer. What it reaches is an initialiser: it writes +inf to `[02F973B8]`, zeroes `[02089300]`, sets `[0208E6A0]` to `0x20` and calls `003844F0`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).
- **Input - SERVICE (2 edges).** `0022A0B0`, `007980A0` reach bodies filed to input: `0035B270`, `0079E520` - shared machinery across the layer boundary, no shared ownership.
- **Platform - CLIENT and SERVICE (11 edges).** `0017D8F0`, `0017D9C0`, `001DF340` are also called by bodies filed to platform: `001DD420`, `00628690`, `001DD170` (+2 more); `00625830`, `007980A0` reach bodies filed to platform: `00623320`, `00624F70`, `00625210` (+3 more) - shared machinery across the layer boundary, no shared ownership.
- **PlatformOnlineAchievements - CLIENT and SERVICE (9 edges).** `001DF340` is also called by bodies filed to platform/online achievements: `007A0C60`; `007980A0` reaches bodies filed to platform/online achievements: `001F3ED0`, `0020CD30`, `0020CD80` (+5 more) - shared machinery across the layer boundary, no shared ownership.
- **Presentation - CLIENT and SERVICE (15 edges).** `001DDAB0`, `001D5120`, `001DE4F0` are also called by bodies filed to presentation/rendering: `001D1660`, `001CD0E0`, `001D5120`; `00625830`, `001D1660`, `0022A0B0` reach bodies filed to presentation/rendering: `001C7360`, `001C7520`, `001D5120` (+6 more) - shared machinery across the layer boundary, no shared ownership.
- **RNG_Random_Selection - SERVICE (1 edge).** `0022A0B0` reaches bodies filed to random selection: `00379CF0` - shared machinery across the layer boundary, no shared ownership.
- **Resource - CLIENT and SERVICE (10 edges).** `0017D280` is also called by bodies filed to resource: `0017D9D0`, `001B14E0`, `001F4340` (+1 more); `0022A0B0`, `001D1660` reach bodies filed to resource: `002EEEE0`, `00259DF0`, `002DF9A0` (+3 more) - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (24 edges).** `0017D280` is also called by bodies filed to script VM / native bridge: `0050C670`, `0050C8D0`, `0050C990` (+21 more) - shared machinery across the layer boundary, no shared ownership.
- **World - SERVICE (1 edge).** `0022A0B0` reaches bodies filed to world: `00266D10` - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT (1 edge).** `0017D280` is also called by bodies filed to world area: `00314020` - shared machinery across the layer boundary, no shared ownership.
### Interior citation — frontier hub 0017E070 (2026-09-18, SWE2-EC7)

**0017E070** (254 B, 4 A-measured callers) — the settings read dispatcher. Bounds-checks an index (`ecx <= 0x16`, 23 cases), loads a jump table at `01B1322C` (`mov rax, [rip-0x5e089]` → `01D20000` + `[rip+0x5e1ac]` slot fetch → `jmp rax`), and each arm ~~pulls a field off the settings record `[01F7CD80]` — `+0x18` word, `+0xB0` byte, `+0x68` byte, `+0x12` byte, `+0x14` byte, `+0x6C` byte —~~ loads a field of the GameSettingConfig object `[01F82D20]` (`+0xC`, `+8`, `+0x10`, `+0x14`, `+0x44`, `+0x48`) or calls the display object's `001DDAB0` *(corrected 2026-10-02, OPUS: checked at `0017E070`–`0017E108`, the 23-case table at `0017E1AC`; the Config screen's per-row reader, after the call chain above)*, normalising each to `eax`. This is the read-side counterpart of the write path (`0017DDD0`→`0017E140`): the config screen writes, the console reads, both through index tables on the same record. In-scope: dispatch `jmp rax` [`0017E093`](../../_index/ADDRESS-INDEX.md); arm `+0x18` read [`0017E0AE`](../../_index/ADDRESS-INDEX.md) — 4 callers, all A.

## SWE2-EC7-34 update (2026-09-19) - `001DEE90`

`001DEE90` (944 B) is a config-table consumer - `00901098` table lea, two `008C25xx` import-thunk calls, then 10 `00194B00` calls plus `00210EB0`/`001E00D0`/`001DF8C0`. Interior anchor `001DEF3F` (an `001DDFD0` call).

`001DF7D0` (228 B) is the buffer-commit `001DE5D0` runs for an `r8`-byte payload `rdx` when `r8` is non-null and `r9d & 6 != 6`: `+0x70` takes `r9d` as flags, `001DF990` positions the `rcx+0x74` region, `00861EBA` copies the bytes, `+0x68` takes the end cursor; flags bit `4` clear writes the begin pointer into `*[+0x18]` and `*[+0x38]` with `esi` into `*[+0x50]`, bit `2` clear writes the `{begin, end, size}` triple through `*[+0x20]`/`*[+0x40]`/`*[+0x58]` (`end` chosen by bits `0x18`), and a still-null `*[+0x38]` additionally takes `rdi` into `*[+0x18]` and `edi` into `*[+0x50]` - then `+0x70` gains bit `0`

Interior anchor `001DF861` (function `001DF7D0`).

`001DF990` (98 B) is the aligned allocator `001DF7D0` and `001DFA80` call for their buffers: `rdx == 0` returns `0`; `rdx >= 0x1000` allocates `rdx + 0x27` through `00210EC0`, aligns the result up `0x20` and stores the raw base at `[aligned - 8]` (the `aligned_malloc`/`_free` pair convention); smaller sizes take a plain `00210EC0(rdx)` - both paths route null through the `008C2DA8` invalid-parameter import

Interior anchor `001DF9CD` (function `001DF990`).

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-contract-game-setting-config-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `001DDFD0` | 119 B | calls through the pointer at `008C2798` with `rcx`, stores the address `00900F20` at qword `+0` of `rcx`, zeroes qword `+0x68` and stores at dword `+0x70` a mask built from `edx`: 4 when `edx` bit 0 is clear, plus 2 when bit 1 is clear, plus 8 when bit 3 is set, plus 0x10 when bit 2 is set; returns `rcx` | `001DDFE9`, `001DDFF7`, `001DE013`, `001DE023`, `001DE036` |
| `001E00D0` | 35 B | calls `001E0100` with `rcx` + 8, the incoming `rdx`, `r8` and `r9`, and 0 as the fifth (stack) argument, then returns the incoming `rdx` | `001E00D6`, `001E00DA`, `001E00E5`, `001E00EA` |

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-contract-game-setting-config-ee-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `001E0100` | 600 B | returns `rdx` as a std::string built from `b` = `rcx` (mode dword `[b+0x70]`): when the mode lacks `0x2` and qword `[qword [b+0x40]]` is non-null, from base qword `[qword [b+0x20]]` up to the larger (unsigned) of that pointer and qword `[b+0x68]`; else when it lacks `0x4` and qword `[qword [b+0x38]]` is non-null, from qword `[qword [b+0x18]]` up to that pointer plus the sign-extended dword `[qword [b+0x50]]`; else empty; the bytes go to a stack string through `001A5630`, the result is set empty (capacity 0xF) and given it by `001A4C90`, and a stack string of capacity 0x10 or more is freed with `00210EB0` (when capacity + 1 is 0x1000 or more it frees the stored base qword before the pointer instead, first checking: a pointer with any of `0x1F` set, a stored base not below it, or a gap under 8 or over 0x27 calls `_invalid_parameter_noinfo_noreturn` (IAT `008C2DA8`)); stack cookie `01F44830`, checked by `00808C40` | `001E0128`, `001E014E`, `001E016B`, `001E0209`, `001E0338` |
