# repos-ec — inbox for the coordinator (repos-55)

Session block: **BP-6 (keymap file format) and BP-1 (the platform pair swap)**, 15-Input.
Program state: GN158 parent, `Verify-GfzCheckpoint.ps1` **PASS** in project
`work\proj_hec\GFZ_HEC` — ledger 38,161 / 38,003 / **158** / 99.58596, snapshot
`46f02e26…7bbbb2`, embedded EXE `73461d08…721f8`, residual `c5d4b7f7…d338ff`.

Deliverable: `15-Input/Binding-Profiles/keymap-ini-file-format-and-default-controls.md`
(`DOCUMENTED`, all sections, no falsification pass yet).

Checkers run: `check_links.py` **PASS** (182 files / 924 links, all resolve) ·
`verify_doc_addresses.py` **ok** (83 cited: 33 data, 27 entry, 23 interior, **0 non-function
`.text` citations to confirm**) · `check_layout_units.py` **clean for this document** (the one
suspect stride in the database is in `18-Audio/.../how-a-sound-request-becomes-a-voice.md`,
not mine) · `check_names.py` **TRUNCATED 0**, all my `NOT IN THE LEDGER` entries are declared
`Working name` or are RTTI/CRT identifiers.

**Not run / for you:** `check_coverage.py` will now under-count `15-Input` by one — I am not
permitted to edit `COVERAGE.md`. See the COVERAGE section below.

---

## COVERAGE

`15-Input` gains **1** document.

| Category | Was | Now | Added |
|---|---:|---:|---|
| 15-Input | *(increment by 1)* | +1 | `Binding-Profiles/keymap-ini-file-format-and-default-controls.md` — the on-disk control config: path, grammar, the 28 action names, the shipped defaults, the keyboard code space, the validation gate, and the Circle/Cross exchange |

Also add it to `15-Input/README.md`'s "Systems in this category" list — that list currently
names only `Gameplay-Capability-Policy` and omits the two `Binding-Profiles` / `Input-Stack`
documents that already exist, so it is stale by three, not one. I did not edit it (it is a
category README, not `_index`, but it is shared surface — your call).

**Increment, do not set.** The known failure mode is a hardcoded count where an increment was
needed.

---

## OPEN-QUESTIONS

### Closures

| Existing id | Disposition |
|---|---|
| **BP-6** — the binding profile **file** format; `00198000` unread | **ANSWERED — read in full, and confirmed against the file on disk.** `keymap.ini` is plain ASCII with **LF** terminators, **87 lines**, at `<Documents>\My Games\FINAL FANTASY XII THE ZODIAC AGE\<SteamID64>\keymap.ini` (the id component is **empty when Steam is not initialised**, which is why the real file sits at the folder root). Three sections `[Keyboard1..3]`, each 28 `Name=Number` lines. The 28 names come from three NULL-terminated pointer tables at `01DF11E0` / `01DF1260` / `01DF12E0`, and **a name's index in the table is its dword index in the profile**: `Select, L3, R3, Start, Up, Right, Down, Left, L2, R2, L1, R1, Triangle, Circle, Cross, Square` / `RX_P, RX_N, RY_P, RY_N, LX_P, LX_N, LY_P, LY_N` / `Speed1, Speed2, Speed3, WalkMode`. Writer recovered too: `FUN_001993b0` (971 B), same path buffer `01F80D90`, `L"[Keyboard" << n << L"]" << L"\n"` then `name << L"=" << code << L"\n"`. Grammar, failure modes and the full shipped-default table are in the new document. |
| **BP-1** — what the platform pair swap swaps, in player terms | **ANSWERED — it swaps `Circle` and `Cross`.** `00195DF0` copies the 16 button slots into the profile record with four 1:1 SSE moves, then exchanges record `+0x34` / `+0x38` = dwords **13** and **14**, and the name table gives index 13 = `Circle`, 14 = `Cross`. The predicate `001DFA70` is `GameSetting[0x64] == 0` = `DecideButton`. **Same field, same object as `AU-1`/`AU-5`** — confirmed here from the input side: `rcx` at the `00195F03` call site is loaded from `01F82D20` at `00195E42`. So one setting has **two consequences**: it exchanges the confirm/cancel button masks (`0022A4F0`) *and* it exchanges the two authored bindings. Third agreement: the masks are `0x2000` = bit **13** and `0x4000` = bit **14** — the same two indices. |
| **AU-1** | Strengthened, not changed. The pair is now named. |
| **AP-5** (LARGELY ANSWERED, "still open: the on-disk keymap format — BG-6") | The remaining half is now closed; **BG-6 / BP-6 can both be marked ANSWERED.** Note these two ids appear to be the same question under two prefixes. |
| **AU-2** — what distinguishes the three profiles | **PARTIALLY ANSWERED.** They are **three alternative key sets for the same 28 actions, all live at once** — not per-player, per-device or per-preset. Two independent supports: (a) `00196FF0` polls five records at `01DF1480` into **one shared control mask**, and records 2–4 of that bank are the three keyboard profiles; (b) `ValidateBindingUniqueness` (`00196550`) scans **all 84 slots** for duplicates, which is only meaningful if the three share one key space. The shipped defaults are non-overlapping by construction: letters / numpad / mouse+QE+ZX. *(What records 0 and 1 of the bank are is still open — see the new questions.)* |

### New — proposed ids, please assign real prefixes at merge

| Proposed id | Question |
|---|---|
| `PROPOSED-reposec-1` | What control codes **123, 125 and 130–152** are, and why the reserved set at `01DF13E0` contains `-` `=` `]` `\` `,` `.` `/` but not `[` `;` `'`. The keyboard range 28–122 is decoded in the new document; `152` is exactly the top of the polling band, so the reserved set ends where the code space does. |
| `PROPOSED-reposec-2` | What the **1–3** and **11–27** control-code bands are. `[Keyboard3]` ships `Circle=1` / `Cross=3`, which are 1–3 codes, and mouse buttons are the obvious reading — **explicitly not asserted**. The Phyre `PInputMouseButtonSemantic` / `PInputJoypadButtonSemantic` member tables give conflicting values for shared names under one record framing (see AUDIT-LOG below), and no consumer was read. *Separating observation: read `InputBackend_IsPrimaryControlCode1To3Active` (`0079E6D0`, 36 B) and see which device state it indexes.* |
| `PROPOSED-reposec-3` | Where **`Speed1` / `Speed2` / `Speed3` / `WalkMode`** are consumed. They are parsed, validated, saved, and readable through the accessor `FUN_00197710`, but `00195DF0` reads the binding array only from `+0x00` to `+0x5F` — **group 2 is never copied into a profile record**. Likely relevant to **Z-10** (the 2x/4x speed-mode scalar `DAT_01DFE0B8`), which is looking for a player-facing speed control. |
| `PROPOSED-reposec-4` | What **records 0 and 1** of the five-record bank at `01DF1480` are, and what the two conditional banks at `01F80550` and `01F80970` (polled by `00196FF0` under manager flag bits 1 and 0/2) hold. This is most of the answer to **AU-4** — the 2,872-byte live region that "three profiles account for only 1,044" of: there are **three banks of three**, plus a five-record bank in `.data`. |
| `PROPOSED-reposec-5` | What the `{u32 kind, u32 4, u32 codeA, u32 codeB}` records at profile-record `+0x40 .. +0x13F` mean beyond `kind == 2` = an axis pair and `kind == 1` = a single code. This is **AU-3** (`{2,4}` written into four 16-byte slots) — the `{2,4}` is not standalone, it is the header of a 16-byte record whose second half is a binding pair. |
| `PROPOSED-reposec-6` | Why `008F3160` — the complete `\My Games\FINAL FANTASY XII THE ZODIAC AGE\keymap.ini` literal — has **no recorded code reference** (`DumpDataXrefs.java`, 13 targets, 56 rows, 0 bad), when the path is otherwise assembled from three separate segments at `008F3848` / `008F3860` / `008F38A8`. |
| `PROPOSED-reposec-7` | Whether `FUN_001f3ed0` returning a pointer into **its own stack frame** is a live defect. `BuildKeymapPath` consumes it only after calling `FUN_00194ef0`, which reuses that stack region. Observable consequence would be a garbage or empty account-id path component. |
| `PROPOSED-reposec-8` | `InputManager_ValidateBindingIdRanges` (`001965E0`) has an outer `for (i = 0; i < 3; i++)` whose inner scan base `r11` is loaded **once**, at `001965EB`, and never advanced — so it validates **profile 1 three times** and never checks profiles 2 and 3. Is this a shipped bug, and does anything else range-check the other two profiles? |

---

## AUDIT-LOG

### Corrections this block makes to existing documents

**1. The two publishers' ledger names are the wrong way round.** This is the highest-value
correction here because both existing Input documents repeat it.

| | `00195DF0` "RestoreDefaultBindingProfiles" | `00198B60` "MaterializeRuntimeBindingProfiles" |
|---|---|---|
| reads | `01F80F90` — the **editable** array (what the file loaded / the player just remapped) | `01DF09C0`, `01DF0A80`, `01DF1470` — **authored constants** |
| writes | the profile records only | the records **and** `01F80F90` |
| actually does | **publishes the current bindings** | **overwrites the current bindings with the shipped defaults** |

Settled without reading either body, by two call sites:
`001E0F70` ("reset to defaults") calls **Materialize then Restore** — incoherent unless
Materialize is the defaults-installer; `001E1050` (assign one binding) calls **Restore alone**
after the assignment, which is the publish. The GFZ names are kept verbatim in the new
document's tables and the disagreement is stated inline, per the naming-discipline rule.

**2. `01DF1738` is not a staging buffer.** `../Input-Stack/input-stack-device-channel-and-bindings.md`
§11 calls `01DF15DC` / `01DF1738` "the scratch area the defaults are assembled in". It is
`01DF1480 + 2 × 0x15C` — **records 2, 3 and 4 of a five-record profile bank that
`00196FF0` polls every frame**. The three keyboard profiles live there permanently. That
document should reopen for this and for correction 1.

**3. `binding-profiles-remapping-and-control-state.md` §7** lists the file format as unread and
`01DF1738` as a staging buffer; both are superseded. Its §2 "Default profiles and the platform
pair swap" is correct as far as it goes but names neither the pair nor the setting. Suggest
reopen → re-`DOCUMENTED`.

**4. The `{2,4}` constants (AU-3) are record headers, not standalone.** See
`PROPOSED-reposec-5`.

**5. The band bound.** I re-derived `(unsigned)(code - 0x1C) < 0x7D` = **28–152** independently
at the `00197160` call site and it agrees with your correction. The neighbour still says 28–283.
Separately: **152 is also the largest reserved id and the top of the range validator's
`[1,152]`**, so three independent sites agree on that ceiling.

### Falsification work done, and what failed to break it

- **Killer observation for BP-1** — *"if slot 13 is not `Circle`, the writer would emit `Circle=`
  at a different line position."* Searched: the file on disk has `Circle=80` as the **14th line**
  of `[Keyboard1]` (header + 13 keys), i.e. index 13. Did not break it.
- **Killer observation for the code mapping** — *"if letters are not contiguous from 28, the
  shipped defaults will not resolve to a coherent scheme."* Solved `c0` from `A/D/S/W` in the
  analog defaults (three equations, one unknown, all satisfied at `c0 = 28`), then checked
  **16 further letters** from the other two profiles: all land on distinct, sensible keys, and
  the whole 84-value default set resolves to W A S D + arrows + I J K L + numpad + F1–F3 +
  Left Shift + Space. Did not break it.
- **Second route to BP-1, not proposed by either of us** — `FUN_001967d0` reads
  `01DF1738 + (0xD + (FUN_0022a540() != 0)) * 4`, i.e. dword **13 or 14 keyed on the same
  setting**, in a function with an unrelated job. Independent agreement.
- **Third route** — `0022A4F0`'s masks are `0x2000` (bit 13) and `0x4000` (bit 14), the same two
  indices. Recorded as corroboration only; no claim that all sixteen bits map to slots.
- **Positive control on the "`Mouse1..3` are never reached" claim** — a fourth name table exists
  at `01DF1360`, and both the reader and the writer are bounded at three groups. The same loop
  demonstrably *does* reach group 2 (`Speed1`…`WalkMode` are matched), so the bound is real and
  the negative is not an instrument failure.
- **Positive control on the "`[Button]`/`[Setting]`/`[Mouse]` are not this binary's format"
  claim** — the same scan, same run, returns a hit for `[Keyboard` at `008F3988`. (A
  `keymap.ini` in that other format exists in the MP-mod `ConfigData` folders; it comes from
  some other tool.)

### Instrument failures — two, both of the "plausible output from a broken tool" family

1. **A `.text` linear sweep for RIP-relative references returned 0 hits for all 13 targets**,
   including `01DF11E0`, which is provably referenced at `0019847F`. Capstone's linear disasm
   desynchronised on inline data and never resynchronised. **The zero looked exactly like a
   clean negative.** Replaced with `DumpDataXrefs.java` (13 targets, 56 rows, 0 bad). Anyone
   writing an ad-hoc xref scan should use the Ghidra script, not a sweep.
2. **A helper script named `dis.py` shadowed the standard library's `dis` module**, which
   `capstone` imports transitively. It raised `AttributeError: partially initialized module
   'capstone' … has no attribute 'Cs'` **and still printed a page of correct-looking
   disassembly.** Renamed. Worth a line in the standard: a scratch script's *filename* is part
   of the instrument.
3. **Phyre enum record framing is ambiguous across copies.** The `{value, typeRef, namePtr, 0}`
   32-byte framing is internally consistent for `PInputKeySemantic` — the run at `01F45700` is
   contiguous `123 … 29` over exactly `(0x1F462C0 - 0x1F45700) / 32 = 94 = 123 - 29` records —
   but three copies of the mouse/joypad tables disagree on the values of shared names
   (`Empty` = 11 / 28, `Button_MiddleMB` = 0 / 13). I did **not** publish those values. The key
   table is used only as corroboration for a mapping that is independently anchored in the
   shipped defaults.

### Method note carried forward from your message

I did not run any write-vs-read reference census by hand; the only access-role classification in
this block comes from `DumpDataXrefs.java`, which classifies read/write/data itself.

---

## CALL-CHAINS / ADDRESS-INDEX

### CALL-CHAINS — new cross-subsystem transitions

```
Save_Load_Settings -> Input      GameSetting.ini[25] "DecideButton"  (01F82D20 + 0x64)
                                   -> InputBinding_ShouldKeepAuthoredPairOrderForPlatformState 001DFA70
                                      -> InputManager_RestoreDefaultBindingProfiles   00195DF0
                                      -> InputManager_MaterializeRuntimeBindingProfiles 00198B60
                                         => exchanges profile dwords 13/14 = Circle/Cross
                                   -> ApplyButtonConvention 0022A4F0
                                         => exchanges the confirm/cancel masks 01E0C2A0/01E0C2A4
   TRIGGER, not an owner transition: Input owns both consequences; Save_Load_Settings owns the field.

PlatformOnlineAchievements -> Input   FUN_001f3ed0 (ISteamUser::GetSteamID)
                                   -> InputManager_BuildKeymapPath 00197EE0
   TRIGGER. The Steam account id is a path component of keymap.ini.

Input (file) -> Input (runtime)   InputManager_Initialize 00195060
                                   -> LoadKeymapIni 00198000 -> 01F80F90
                                   -> Validate{Uniqueness,IdRanges} 00196550 / 001965E0
                                   -> Restore 00195DF0 | Materialize 00198B60 -> 01DF1738, 01F80130
                                   -> PollAndBuildControlState 00196FF0 -> 5 x 00197160
   OWNER TRANSITION at 00195060: above it the bindings are a file, below they are Input state.

UI/options -> Input               001E0F40 (save) | 001E0F70 (reset) | 001E1050 (assign)
                                   callers: 0023CE10 -> 001E0F40 ; 0017CDC0 -> 0017D670 -> 001993B0
   TRIGGER.
```

### ADDRESS-INDEX — new entries

Functions (all `Input` owner unless noted; body sizes from `graph_gn/functions.tsv`):

```
00195060  153   InputManager_Initialize                              clear, load, validate, publish
00195DF0  526   InputManager_RestoreDefaultBindingProfiles            publishes the editable array (see correction 1)
00196290  488   FUN_00196290    (wn InputProfiles_CopyLiveRecordsBackToBank)
00196550  135   InputManager_ValidateBindingUniqueness                84-slot duplicate + reserved scan
001965E0  159   InputManager_ValidateBindingIdRanges                  profile 1 only, [1,152] x 28
001967D0  499   FUN_001967d0    (wn InputProfiles_ApplyConfirmBindingToPointerDevice)
00196FF0  356   InputManager_PollAndBuildControlState                 5 records at 01DF1480 + 2 gated banks
00197710   99   FUN_00197710    (wn InputManager_GetBinding)          only reader of group 2 found
00197A50  229   FUN_00197a50    (wn Filebuf_OpenWithMode)             _Fiopen(path, mode, prot)
00197EE0  273   InputManager_BuildKeymapPath                          SHGetFolderPathW + mkdir chain
00198000 1644   InputManager_LoadKeymapIni                            THE PARSER
001993B0  971   FUN_001993b0    (wn InputManager_SaveKeymapIni)       THE WRITER, 87 lines
00198B60  782   InputManager_MaterializeRuntimeBindingProfiles        installs shipped defaults (see correction 1)
001DFA70    8   InputBinding_ShouldKeepAuthoredPairOrderForPlatformState
001E0F40   36   FUN_001e0f40    (wn InputConfig_SaveKeymap)
001E0F70   49   FUN_001e0f70    (wn InputConfig_ResetBindingsToShippedDefaults)
001E1050  164   FUN_001e1050    (wn InputConfig_AssignBindingAndRepublish)
0022A4F0   66   FUN_0022a4f0    (wn ApplyButtonConvention)            re-derived here, agrees with 19-Save-Load-Settings
0022A540   12   FUN_0022a540    (wn ButtonConvention_Query)           return DAT_01FD4A64 == 0
001F3EA0   43   FUN_001f3ea0    (wn Path_CreateDirectoryIfMissing)    _waccess + _wmkdir     [no owner]
001F3ED0  159   FUN_001f3ed0    (wn Platform_GetSteamAccountIdString) [PlatformOnlineAchievements]
00194EF0   89   FUN_00194ef0    (wn Format_VSwprintfS)                [no owner]
```

Data (no body extent — do **not** let these reach a Key-addresses table):

```
01DF11E0  16 x wchar_t*   key-name table, group 0   Select .. Square
01DF1260   8 + NULL       key-name table, group 1   RX_P .. LY_N
01DF12E0   4 + NULL       key-name table, group 2   Speed1, Speed2, Speed3, WalkMode
01DF1360   3 + NULL       key-name table, group 3   Mouse1..3 -- DEFINED BUT NEVER ITERATED
01DF13E0  u32[35]         reserved control ids
01DF09C0  3 x 0x40        shipped defaults, group 0 (16 button codes per profile)
01DF0A80  3 x 0x100       shipped defaults, record tail: 16 x {kind, 4, codeA, codeB}
01DF1470  16 B            shipped defaults, group 2: 65, 66, 67, 118 -- PROFILE 1 ONLY
01DF1480  5 x 0x15C       runtime profile bank, polled every frame
01DF1738  = 01DF1480+2x0x15C   the three keyboard profile records; the swap happens here
01F80130  3 x 0x15C       published profile table
01F80F90  u32[84], 336 B  the editable binding array (groups at +0x00 / +0x40 / +0x60, stride 0x70)
01F80D90  wide string     the keymap.ini path buffer -- reader and writer share it
008F3988 / 008F3984 / 008F3980 / 008F399C   L"[Keyboard" / L"]" / L"\n" / L"="
008F3848 / 008F3860 / 008F38A8              path segments + L"keymap.ini"
008F3160  wide string     full legacy-shaped path literal -- NO CODE REFERENCE FOUND
01F45700  95 x 32 B       PInputKeySemantic member records, contiguous 123 .. 29
01CD84D8  ASCII run       PInputKeySemantic name strings, Key_A .. Key_Right_Alt
```

---

## The one-paragraph version, if you only read one thing

**The three keyboard layouts a PC player uses are one 699-byte ASCII file with 87 lines, and the
game throws all of it away if any single line is wrong.** The file names bindings after
PlayStation buttons — `Circle=80`, `Cross=30`, `WalkMode=118` — and slot 13 is `Circle`, slot 14
is `Cross`, which is exactly the pair `RestoreDefaultBindingProfiles` exchanges at record
`+0x34`/`+0x38` when `DecideButton` says Cross confirms. **BP-1's hypothesis was right and is now
shown, not assumed**, and it is the same `+0x64` the settings side reached: one setting, two
consequences — the button masks *and* the bindings. The shipped defaults decode to W A S D +
arrow keys + I J K L + numpad + F1/F2/F3 for the speed toggles + Left Shift to walk, from a
control-code space that is Phyre's `PInputKeySemantic` minus one.

---
---

# repos-ec — BLOCK 2: where the group-2 bindings go, and Z-10 answered

Follow-on to the block above, taking the coordinator's option 2. Same program state (GN158,
verified). Same document extended:
`15-Input/Binding-Profiles/keymap-ini-file-format-and-default-controls.md`.

Re-checked after the extension: `check_links.py` **PASS** (185 files / 940 links) ·
`verify_doc_addresses.py` **ok** — **122 cited**, 45 entry / 26 interior / 51 data,
**0 non-function `.text` citations to confirm**.

## COVERAGE

No new document. `15-Input` count unchanged from block 1 (still +1 in total).

## OPEN-QUESTIONS

### Closures

| Existing id | Disposition |
|---|---|
| `PROPOSED-reposec-3` (mine) — where `Speed1..3` / `WalkMode` are consumed | **ANSWERED, completely.** `FUN_00197710` is the *only* reader that reaches group 2, and its six callers all read **profile 1 only**. `Speed1/2/3` → `0017DEA0` (called from the main loop under its own `"[PS2]fast mode"` marker) → `GameSpeed_SetMode` (`00239790`) → `g_speedMode` (`01FD4A98`) → `g_speedScalar` (`02064AC4`) `= speedTable[mode]`, where `speedTable` at `00908BA8` is `{1.0f, 2.0f, 4.0f}`. `WalkMode` → `0017DFC0` → `PartyControl_BuildAnalogMovementVectorFromInputHistory` (`003594E0`), which **latches it into a toggle** and hands the flag to `PartyControl_ComputeAnalogMovementScale` (`00358A20`). |
| **Z-10** — is `DAT_01DFE0B8` the 2x/4x speed-mode scalar? | **ANSWERED: NO — and the separating observation Z-10 itself named has now been made.** Z-10 asked for *"identify the object at `0x01F82D20` and read field `+0x48`"*. `FUN_0017d8f0` is eleven bytes: `return *(u32 *)(01F82D20 + 0x48)`. Key-table index 18 is **`FrameLimit`**, and its value-name row is literally **`{"30", "60"}`**, default `0` = 30. `0022BDF0` (the command-line handler) calls `HostTiming_SelectFrameBaseAndTimerPeriod(FrameLimit == 1)`, and on that branch `001EDDC0` writes `01DFE0B4 = 2`, `01DFE0B8 = 2.0f` (from `01CEBC08`) and `01DFE0BC = 0.5f` (from `01CEBB70`). **`DAT_01DFE0B8` is the frame-rate base: `1.0` at 30 fps, `2.0` at 60 fps.** The real 2x/4x control is `02064AC4`, from a three-entry table driven by the `Speed1/2/3` keymap bindings. |
| **K-8** — are `01DFE0BC` / `01DFE0B8` ever written away from `1.0` during play? | **ANSWERED: never during play, but they are not always `1.0`.** Access-role census this session (`DumpDataXrefs.java`): `01DFE0B4` **211 R / 1 W**, `01DFE0B8` **46 R / 1 W**, `01DFE0BC` **182 R / 1 W** — all three writes inside `001EDDC0`, at startup, on the `FrameLimit = 60` branch. A player running at 60 fps plays the whole game with `01DFE0B8 = 2.0` and `01DFE0BC = 0.5`. |
| **Z-3** — the unit of the decay interval `DAT_01DFE0B8 * DAT_008F8D80` | **RESOLVES, given the above.** The interval is `DAT_01DFE0B8 * 30.0` **ticks**, and the tick rate is `30 * DAT_01DFE0B8` per second — `spawn-placement-and-retirement.md` divides raw ticks by exactly that to get seconds. So the interval is **one second at both FrameLimit settings**: 30 ticks at 30 fps, 60 at 60. *This closure leans on the spawn document's seconds conversion; if that reopens, so does this.* |
| **AU-3** (`{2,4}` in four 16-byte slots) | Restated as `PROPOSED-reposec-5` in block 1: it is a record header, not a standalone constant. |

### New — proposed ids

| Proposed id | Question |
|---|---|
| `PROPOSED-reposec-9` | What `FUN_001e0c10` (21 B, `Input`) gates. When it is non-zero, walk mode is **forced off** before the key is even read. |
| `PROPOSED-reposec-10` | What `Present_SetSpeedField` (`002DE250`) controls. It packs `n & 0xF` into **bits 23-26** of `*(u32 *)(DAT_0215E6E0 + 4)`, and the speed setter passes `0` for the 2x mode and `1` for the 4x mode. The field's meaning is unread. |
| `PROPOSED-reposec-11` | What `GameSpeed_NotifySubsystem` (`00182FB0` → `FUN_001d8210` / `FUN_001d85c0`) tells its subsystem when the speed mode changes. Audio pitch is the obvious guess and is **not asserted**. |
| `PROPOSED-reposec-12` | The **gamepad** route into the speed modes. When the keys are inactive the main loop tests `InputGameplay_GetRemappedHistoryMask04() >> 10 & 1` **and** `...Mask0C() >> 10 & 1`, then calls `FUN_0023b200`. Bit 10 is `L1` under the slot/bit correspondence from block 1 — but that correspondence is only *shown* for bits 13/14, so this is a **lead, not a finding**. |
| `PROPOSED-reposec-13` | Why `02064AC4` shows **5 writes and 1 read** in an access-role census. A published per-frame scalar with more writers than readers is the shape of a value consumed through a computed base, so the reader census is probably incomplete — worth knowing before anyone quotes it. |

## AUDIT-LOG

### The finding, and why it is the shape of a correct answer

**The group of bindings the publisher skips entirely turned out to be the group with the most
interesting consumers.** `00195DF0` reads the binding array only from `+0x00` to `+0x5F`, so
`Speed1/2/3` and `WalkMode` never enter a profile record — and the reason is that **six of the
twenty-eight slots are not mask-driven at all.** One accessor, `FUN_00197710`, is their entire
read surface, and its six callers ask for `L2`, `R2`, `Speed1`, `Speed2`, `Speed3` and
`WalkMode`, always from profile 1.

That also closes a loose end block 1 left explicitly open: **the publishers zero `L2` and `R2` on
purpose**, because `0017DDC0` and `0017DE10` query those two slots directly from the binding
array. Block 1 recorded the zeroing as measured-but-unexplained; it is now explained.

A consequence worth surfacing to modders, and now in the document: **binding any of those six in
`[Keyboard2]` or `[Keyboard3]` has no effect.** The value is stored, validated and saved, and
never read. That is the second silent no-op in this format, after control codes 4-10.

### Corrections to existing documents

**1. `09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md` — Z-10 closes NO.** The document
is careful and its refusal to assert was right; the answer is simply that `01DFE0B8` belongs to a
different mechanism. Its `(int)(DAT_01DFE0B8 * 30.0)` expressions are all correct and now have a
meaning: **ticks per second, 30 or 60**.

**2. `06-Movement-And-Navigation/heading-speed-to-position-delta.md` — K-8 closes.** Its
`world_ctx[+0xC8] = DAT_01DFE0B8 * 30.0 * 3.6 * speed` is `108.0 * speed` at 30 fps and
`216.0 * speed` at 60 — and `DAT_01DFE0BC`, which multiplies every authored locomotion speed,
becomes `0.5` on the same branch. **The two changes cancel**: twice as many ticks, half the
distance per tick. That is what a frame-base switch looks like, and it is a good check that the
reading is right rather than merely consistent.

**3. The "a function's identity is not uniform across its branches" case in `EVIDENCE-STANDARD.md`
is confirmed first-hand.** The standard records a document that called `001EDDC0` *"the
host-timing initialiser — it calls `timeGetDevCaps` and `timeBeginPeriod`"* and attributed the
store to it. Reading the body: those two calls are on the `param == 0` branch, and **all three
scalar writes are on the other one**, next to `timeEndPeriod`. Exactly as recorded.

### Falsification work, and what failed to break it

- **Killer observation for "group 2 is unreachable through the mask"** — *if any other function
  read `01F80FF0`, the claim is false.* `DumpDataXrefs.java` on `01F80FF0` returns **7
  references**: one write, four `LEA`s inside the parser/writer/assigner, and exactly one indexed
  read. `01F80FF4` / `F8` / `FC` return **nothing at all**. Cross-checked against `01F80F90`'s own
  reference list, which closes at nine functions, all `Input`, all named. Did not break it.
- **Killer observation for Z-10** — *if `00239790` wrote `01DFE0B8`, Z-10 would be YES.* It does
  not; `01DFE0B8` has exactly one writer and it is the startup frame-base selector. Two censuses
  agree — this session's, and the earlier 45 R / 1 W.
- **The `FrameLimit` identification does not rest on the peer document.** The key table
  (`01DFD050`), the value-name table (`01DFD150`) and the defaults (`00900CE0`) were re-derived
  here from the image and agree with `19-Save-Load-Settings` on all 31 keys, including row 18
  `{"30","60"}` and row 25 `{"Circle","Cross"}`. **Two derivations from opposite ends, one table.**
- **A trap avoided.** `Speed1/2/3` invites "1x, 2x, 4x" read straight off the names — but the
  *arguments* are `1`, `2`, `4`, the *modes stored* are `0`, `1`, `2`, and the multipliers come
  from the table, not from either. I read the disassembly rather than the decompiler's argument
  list, which had dropped arguments on two `FUN_002de250` calls and one `FUN_00197710` call — a
  decompiler's argument list is a claim about a signature, and here it was wrong three times in
  one function.

## CALL-CHAINS / ADDRESS-INDEX

### CALL-CHAINS

```
Input (file) -> CoreRuntimeScheduling     keymap Speed1/2/3 (group 2, slots 0-2, profile 1)
    MainLoop_RunFrame 0022A770  ["[PS2]fast mode"]
      -> InputQuery_PollSpeedModeKeys 0017DEA0
         -> GameSpeed_SetMode 00239790 -> g_speedMode 01FD4A98
      -> g_speedScalar 02064AC4 = {1.0,2.0,4.0}[mode] @ 00908BA8
   OWNER TRANSITION at 00239790: Input reads the binding, CoreRuntimeScheduling owns the mode.

Input (file) -> Party                     keymap WalkMode (group 2, slot 3, profile 1)
    PartyControl_BuildAnalogMovementVectorFromInputHistory 003594E0
      -> InputQuery_IsWalkModeKeyHeld 0017DFC0
      -> g_walk 022C800C -> PartyControl_ComputeAnalogMovementScale 00358A20
   OWNER TRANSITION at 003594E0.

Save_Load_Settings -> CoreRuntimeScheduling   GameSetting.ini[18] "FrameLimit" {"30","60"}
    Startup_ParseCommandLineAndSelectFrameBase 0022BDF0
      -> GameSetting_GetFrameLimit 0017D8F0
      -> HostTiming_SelectFrameBaseAndTimerPeriod 001EDDC0
         -> 01DFE0B4 / 01DFE0B8 / 01DFE0BC   (the sole writes to all three)
   TRIGGER. This is the edge Movement, Spawn and Combat-AI all read downstream of.
```

### ADDRESS-INDEX — new entries

```
0017DDC0   67  FUN_0017ddc0  (wn InputQuery_IsL2Held)                        Input
0017DE10   67  FUN_0017de10  (wn InputQuery_IsR2Held)                        Input
0017DEA0  276  FUN_0017dea0  (wn InputQuery_PollSpeedModeKeys)               [no owner]
0017DFC0   67  FUN_0017dfc0  (wn InputQuery_IsWalkModeKeyHeld)               Input
0017D8F0   11  FUN_0017d8f0  (wn GameSetting_GetFrameLimit)                  [no owner]
00182FB0   28  FUN_00182fb0  (wn GameSpeed_NotifySubsystem)                  [no owner]
001E0AA0   90  FUN_001e0aa0  (wn InputConfig_GetBindingPacked)               Input
001E0BD0   62  FUN_001e0bd0  (wn InputConfig_GetBinding)                     Input
001E0C10   21  FUN_001e0c10  (the walk-mode gate)                            Input
001EDDC0  165  FUN_001eddc0  (wn HostTiming_SelectFrameBaseAndTimerPeriod)   CoreRuntimeScheduling
00229E00   20  FUN_00229e00  (wn GameSpeed_GetMultiplier)                    CoreRuntimeScheduling
00229E20    7  FUN_00229e20  (wn GameSpeed_GetMode)                          CoreRuntimeScheduling
00229ED0    7  FUN_00229ed0  (wn GameSpeed_SetModeRaw)                       CoreRuntimeScheduling
00239790  141  FUN_00239790  (wn GameSpeed_SetMode)                          [no owner]
0022A770 2001  FUN_0022a770  (wn MainLoop_RunFrame)                          CoreRuntimeScheduling
0022BDF0  146  FUN_0022bdf0  (wn Startup_ParseCommandLineAndSelectFrameBase) CoreRuntimeScheduling
002DE250   24  FUN_002de250  (wn Present_SetSpeedField)                      [no owner]
003594E0  461  PartyControl_BuildAnalogMovementVectorFromInputHistory        Party
00358A20  274  PartyControl_ComputeAnalogMovementScale                       Party
```

Data (no body extent):

```
00908BA8  3 x f32 .rdata   game-speed multiplier table = { 1.0, 2.0, 4.0 }
01FD4A98  s32              current speed mode 0/1/2      -- 1 writer, 4 readers
02064AC4  f32              published speed scalar        -- 5 writes, 1 read recorded (reposec-13)
02064AD2  u8               speed feature enable          -- 2 writers, 3 readers, all main loop
0208E6B4  s32              "a speed-up is active"
01F7F4E9  u8               speed-key edge latch
022C800C  u32              walk-mode flag (toggled)
022C7FF9  u8               walk-key edge latch
01DFE0B4  s32              frame base: 1 (30 fps) / 2 (60 fps)     -- 211 R, 1 W
01DFE0B8  f32              frame base: 1.0 / 2.0                   --  46 R, 1 W
01DFE0BC  f32              per-tick locomotion: 1.0 / 0.5          -- 182 R, 1 W
01CEBC08  f32 = 2.0        the constant written into 01DFE0B8
01CEBB70  f32 = 0.5        the constant written into 01DFE0BC
01DFD050  31 x char*       GameSetting key table    -- index 18 FrameLimit, 25 DecideButton
01DFD150  31 x 9 x char*   GameSetting value names  -- row 18 {"30","60"}, row 25 {"Circle","Cross"}
00900CE0  31 x 16 B        GameSetting defaults, col 0 -- FrameLimit default 0 = "30"
```

## The one-paragraph version

**The four PC-only keys in keymap.ini are the game-speed and walk controls, and following them
answered a question three other documents were carrying.** `F1`/`F2`/`F3` toggle 1x / 2x / 4x —
pressing the active one again turns it off — through a `{1.0, 2.0, 4.0}` table at `00908BA8`
whose published scalar is `02064AC4`. Left Shift is a **walk toggle, not a hold**. Which means
`DAT_01DFE0B8` is *not* the speed-mode scalar: it is the **`FrameLimit` frame base**, `1.0` at 30
fps and `2.0` at 60, written once at startup from `GameSetting + 0x48`, whose value names are
literally `{"30","60"}` — **exactly the separating observation Z-10 asked for.** Z-10 closes NO,
K-8 closes, Z-3's unit resolves to one second at either setting, and the six slots that never
enter the per-frame mask — `L2`, `R2` and the four PC-only keys — are explained.
