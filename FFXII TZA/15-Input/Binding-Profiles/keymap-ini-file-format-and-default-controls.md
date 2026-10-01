---
system: keymap.ini — the control config file, its format, and the shipped default controls
category: 15-Input
status: AUDITED
owner_layer: PrimaryOwner:Input
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN158 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN158 this document cites none of batch R109's 109; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: complete bodies of the reader (00198000) and the writer (001993B0) read at
    instruction level; the three key-name tables, the reserved-id table and the three
    authored default tables read raw from the image; the resulting format checked against
    the keymap.ini actually on disk on this machine (byte-identical client, see
    _index/EVIDENCE-STANDARD.md "Tier 10 has no different-build caveat")
last_reviewed: 2026-09-12
audit:
  passes: 2
  last_pass: 2026-09-03
  last_pass_state: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  crossref_clean: false        # 2026-09-30 (SWE2-DATA): false until the pass-22 UNACCOUNTED NEIGHBOUR findings are accounted (FRONTIER-REQ-SWE2-DATA-PASS22-DEBT; OPUS-REQ-DATA-PASS30-CROSSREF-CLEAN-0930)
  reopened_count: 0
---

# keymap.ini — the control config file, its format, and the shipped default controls

> The plain-text file that stores your keyboard controls, written out in the game's own
> vocabulary — `Circle=80`, `WalkMode=118` — and read back at startup. This document gives the
> complete format, the exact shipped defaults, what every number means, and the one line in the
> file the game will silently swap for you.

## 1. What the player sees

FFXII on PC is played on a keyboard mapped onto a PlayStation controller. Every action in the
game is still called by its controller name — Circle confirms, Cross cancels, L1 opens the map,
Triangle is the Battle Menu — and what the keyboard actually does is decided by a small text
file the game writes into your Documents folder.

**Three complete keyboard layouts are live at the same time.** Out of the box the game ships:

- a **letter layout** — walk with W A S D, look with the arrow keys, move the cursor with
  I J K L, confirm with **Space**, cancel with **C**, Triangle on **R**, Square on **F**;
- a **numpad layout** — the numpad digits drive the cursor, **Enter** confirms and
  **Backspace** cancels;
- a **short third layout** — **Q** and **E**, **Z** and **X**, and the mouse buttons for
  confirm and cancel.

They all work at once. Pressing Space and pressing Enter both confirm, because they are bound
to the same action in two different layouts. This is why the game refuses to let the same key
appear twice: **one key may only mean one thing across all three layouts.**

The file also carries the four PC-only controls that have no PlayStation button at all.
**F1, F2 and F3 are the game-speed keys** — F1 puts you back to normal, F2 gives you 2× speed
and F3 gives you 4×, and **pressing the same one again turns it off**. **Left Shift is Walk
Mode**, and it is a *switch, not a hold*: tap it once and your character walks until you tap it
again.

Two of the PlayStation buttons are special too. **L2 and R2 are asked about directly** rather
than going through the same path as every other button, which is why nothing else in the game
sees them the way it sees Circle or Square. They are still yours to rebind in the file.

Two things about this file surprise people:

**It records what the file calls Circle and Cross, not what confirms.** If you have set the
game to confirm with Cross rather than Circle, the game **exchanges those two lines for you**
after it reads the file, every time it builds the controls. The file always describes the
buttons; the setting decides which one accepts.

**If the file is even slightly wrong, the whole thing is thrown away.** There is no partial
recovery and no error message. Duplicate a key, leave one of the twenty-eight actions on a key
the game does not recognise, and every layout you wrote is discarded and the shipped defaults
come back — including the two layouts you did not touch.

## 2. Native mechanism

### Where the file lives

`InputManager_BuildKeymapPath` (`00197EE0`) assembles the path once, into a fixed buffer, and
creates each directory as it goes (`_waccess`, then `_wmkdir` if missing):

```
SHGetFolderPathW(CSIDL_PERSONAL = 5)          ->  <Documents>
  + "\My Games\"
  + "FINAL FANTASY XII THE ZODIAC AGE\"
  + <Steam account id, decimal>
  + "\keymap.ini"
```

The account-id component comes from `FUN_001f3ed0`, which asks Steam for the current user's
64-bit id and formats it with `%llu`. **It is guarded** — `if (steamUser != NULL)` — and the
buffer it formats into was zeroed first, so when Steam is not up the component is the **empty
string** and the file lands directly in the `FINAL FANTASY XII THE ZODIAC AGE` folder (with a
doubled backslash in the path, which Windows accepts). That is where the file sits on the
machine this document was written on.

The same buffer, `01F80D90`, is used by the reader and by the writer, so **the game reads back
exactly the file it wrote** — there is no reader/writer path mismatch.

### The file is read once, at input-manager startup

`InputManager_Initialize` (`00195060`) does, in order:

1. `memset(01F80F90, 0, 0x150)` — **clear all three profiles**, 336 bytes;
2. `BuildKeymapPath()`;
3. `LoadKeymapIni()` — parse the file straight into that cleared array;
4. `ValidateBindingUniqueness()` — no id may repeat, none may be reserved;
5. `ValidateBindingIdRanges()` — profile 1 must be *completely* filled with legal ids;
6. **both clean → `00195DF0`, publish what was loaded.** Anything else → `00198B60`, install
   the shipped defaults over the top.

There is no third outcome. A file that fails either check contributes nothing at all.

### Parsing (`InputManager_LoadKeymapIni`, `00198000`)

The file is opened as a `std::basic_ifstream<wchar_t>` through
`_Fiopen(path, mode = 0x23, prot = 0x40)` — `in | out | binary`, share-deny-none. `in|out`
means **the file must already exist**; if it does not, the stream takes `failbit` and nothing is
parsed. The game then `seekg`s to the end and reads `tellg`: a **zero-length file is skipped**
before a single line is read.

Although the stream is wide, the file itself is **byte-oriented text**. `FUN_00197a50` installs
the locale's `codecvt` only when `always_noconv()` is false, so each byte of the file becomes one
`wchar_t`. The file on disk is plain ASCII. *(The narrowing is MSVC library behaviour — tier 6 —
but the file on disk is directly observed as ASCII, tier 10.)*

Then, per line, `getline(line, 0x80)` — **at most 127 characters plus a terminator**:

```c
len = wcslen(line);
if (len == 0)                                  continue;          /* blank line: skipped */
if (wcsncmp(&line[1], L"Keyboard", 8) == 0) {                     /* NOTE: line[0] is not checked */
    end = wcschr(line, L']');
    if (end == NULL)                           goto close_and_stop;
    wcsncpy(scratch, &line[9], end - &line[9]);                   /* the digits between them */
    profileIndex = wcstol(scratch, &p, 10) - 1;                   /* 1-based in the file */
    continue;
}
eq = wcschr(line, L'=');
if (eq == NULL)                                goto close_and_stop;
wcsncpy(key, line, eq - line);                                    /* the name before '=' */
code = wcstol(eq + 1, &p, 10);                                    /* the number after it   */
/* ... name lookup, below ... */
```

Three behaviours here matter to anyone editing the file:

- **A blank line is skipped.** Blank lines between sections are harmless.
- **Any other line that is neither a `[Keyboard…]` header nor contains `=` stops the load
  immediately**, keeping everything parsed so far and discarding the rest of the file. There is
  no comment syntax: a `;` or `#` line terminates the parse.
- **`line[0]` is never examined.** The test is on characters 2–9. `[Keyboard1]` works because
  `[` is skipped, not because it is required — `xKeyboard1]` parses identically.

`wcstol` failures are not tolerated: a value with no digits at all raises
`std::invalid_argument` ("invalid stoi argument") and a value that overflows raises
`std::out_of_range`, both through the MSVC throw helpers.

### Name lookup — the same table drives reading, writing and the slot order

Having a `key` and a `code`, the parser walks **three tables of sixteen name pointers each**,
starting at `01DF11E0` and stepping `0x80` bytes per group, in lock-step with the profile's slot
pointer:

```c
for (group = 0; group < 3; group++) {
    slot = groupBase[group] + profileIndex * 0x70;      /* 01F80F90 / 01F80FD0 / 01F80FF0 */
    names = (wchar_t **)(0x01DF11E0 + group * 0x80);
    for (i = 0; i < 0x10; i++) {
        if (names[i] == NULL) break;                    /* NULL-terminated per group */
        if (_wcsicmp(key, names[i]) == 0)
            *(u32 *)(slot + i * 4) = code;              /* name index i == slot index i */
        /* no break: the scan continues through all three groups */
    }
}
```

Two consequences fall straight out of this loop, and both are load-bearing for §4:

- **The name's index in the table *is* the slot's index in the profile.** Nothing else maps
  them. The writer (`FUN_001993b0`) uses the identical pair of pointers, so a saved file's line
  order is the slot order, exactly.
- **Key names are matched case-insensitively** (`_wcsicmp`), and **an unrecognised name is
  silently ignored** — the loop simply finds no match and the line has no effect.

`profileIndex` is **never range-checked.** It starts at `-1` and is only ever set from the file.
A `Name=value` line that appears before any `[KeyboardN]` header writes `0x70` bytes *below* the
binding array; `[Keyboard99]` writes far above it. See §6.

### Writing (`FUN_001993b0`, working name `InputManager_SaveKeymapIni`)

The writer opens the same path buffer with `_Fiopen(path, 0x26)` — `out | ate | binary`, i.e.
create-and-truncate — and emits, with no blank lines and a bare `\n` terminator:

```
for (p = 0; p < 3; p++) {
    out << L"[Keyboard" << (p + 1) << L"]" << L"\n";
    for (group = 0; group < 3; group++)
        for (i = 0; names[group][i] != NULL && i < 0x10; i++)
            out << names[group][i] << L"=" << slot[group][p][i] << L"\n";
}
```

That is 3 × (1 header + 16 + 8 + 4 keys) = **87 lines**, always, with every slot written whether
it is bound or not. Unset slots are written as `0`.

### The Circle/Cross exchange (the answer to BP-1)

`InputManager_RestoreDefaultBindingProfiles` (`00195DF0` — see the naming correction in §5)
copies each profile's sixteen button slots into a profile record with four SSE moves, one to
one, then:

```asm
00195F03  call  0x1DFA70                          ; InputBinding_ShouldKeepAuthoredPairOrderForPlatformState
00195F08  test  al, al
00195F0A  jne   0x195F2C                          ; keep authored order
00195F0C  mov   ecx, [record + 0x34]
00195F14  mov   eax, [record + 0x38]
00195F1C  mov   [record + 0x34], eax
00195F24  mov   [record + 0x38], ecx
```

The copy at `[rdi-0x48]`/`[rdi-0x38]`/`[rdi-0x28]`/`[rdi-0x18]` is byte-for-byte in order, so
record `+0x34` is profile dword **13** and record `+0x38` is dword **14** — and the name table
at `01DF11E0` gives index 13 = **`Circle`** and index 14 = **`Cross`**.

**The platform pair swap is the Circle/Cross confirm-button convention, and it swaps the two
bindings themselves.** The predicate is `*(int *)(GameSetting + 0x64) == 0`, and slot `+0x64` of
the settings object is `DecideButton` (`Circle` = 0, `Cross` = 1) — see
[the settings object](../../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md).
So with `DecideButton=Cross`, the key the file lists under `Circle` becomes the key that cancels
and the key under `Cross` becomes the key that confirms — the bindings trade places, and the
file on disk is not rewritten.

A second, wholly independent site does the same arithmetic. `FUN_001967d0` reads the same
setting through `FUN_0022a540` and then indexes:

```c
int q = FUN_0022a540();                                      /* = (cachedDecideButton == 0) */
int *binding = (int *)(0x01DF1738 + (0xD + (q != 0)) * 4);   /* dword 13 or dword 14 */
if ((unsigned)(*binding - 1) < 3) { /* the binding is a code in 1..3 */ }
```

`0xD` and `0xD + 1` are slots 13 and 14 again, selected by the same setting. Two functions,
different jobs, same pair. *(Which of the two this one selects is not asserted here — it picks
the slot the flag names, and what it then does with a 1–3 code was not read in this pass.)*

### Where the file's bindings are actually read — and the two groups that bypass the mask

Most of the file feeds the per-frame control mask, but **six of the twenty-eight slots never
reach it.** They are read on demand instead, through one accessor, and this is why the
publishers zero two of them.

`FUN_00197710` is the whole read surface for those six:

```c
u32 GetBinding(void *mgr /*ignored*/, u8 profile, u8 group, u8 slot)
{
    if (group == 0) return *(u32 *)(0x01F80F90 + (profile * 0x1C + slot) * 4);
    if (group == 1) return *(u32 *)(0x01F80F90 + (profile * 0x1C + slot) * 4 + 0x40);
    if (group == 2) return *(u32 *)(0x01F80F90 + (profile * 0x1C + slot) * 4 + 0x60);
    return 0;                                       /* any other group */
}
```

Every one of its six callers reads **profile 1 only** and hands the code straight to
`InputBackend_IsControlCode28To283ActiveForBank(backend, code, 0)`:

| Caller | Reads | Meaning |
|---|---|---|
| `0017DDC0` | group 0, slot **8** — `L2` | "is L2 held right now?" |
| `0017DE10` | group 0, slot **9** — `R2` | "is R2 held right now?" |
| `0017DEA0` | group 2, slots **0, 1, 2** — `Speed1/2/3` | the game-speed keys |
| `0017DFC0` | group 2, slot **3** — `WalkMode` | "is the walk key held?" |
| `001E0BD0`, `001E0AA0` | any `(profile, group, slot)` | generic getters, for the config screen |

**That closes the `L2`/`R2` puzzle.** Both publishers write `0` over record `+0x20`/`+0x24`
before the record is used, so `L2` and `R2` are deliberately absent from the per-frame mask —
because two dedicated predicates query them directly from the binding array instead. The file's
`L2=` and `R2=` lines are live; they simply take a different road.

#### `Speed1`, `Speed2`, `Speed3` — the 1× / 2× / 4× game-speed toggles

`0017DEA0` is called from the main loop (`0022A770`, under its own `"[PS2]fast mode"` /
`"FAST MODE"` debug markers) and is a three-way edge-latched poll:

```c
if      (IsActive(GetBinding(0, 2, 0))) { if (!latch) { latch = 1; SetSpeedMode(1); } return 1; }
else if (IsActive(GetBinding(0, 2, 1))) { if (!latch) { latch = 1; SetSpeedMode(2); } return 1; }
else if (IsActive(GetBinding(0, 2, 2))) { if (!latch) { latch = 1; SetSpeedMode(4); } return 1; }
else                                    { latch = 0; return 0; }        /* latch = 01F7F4E9 */
```

`SetSpeedMode` (`00239790`) then, exactly:

```c
void SetSpeedMode(int n)                        /* n = 1, 2 or 4 */
{
    int cur = g_speedMode;                      /* 01FD4A98 */
    if (n == 2) { if (cur == 1) goto reset;  Present_SetSpeedField(0); g_speedMode = 1; g_fastActive = 1; Notify(1); return; }
    if (n == 4) { if (cur == 2) goto reset;  Present_SetSpeedField(1); g_speedMode = 2; g_fastActive = 1; Notify(2); return; }
reset:          g_speedMode = 0; g_fastActive = 0; Notify(0);           /* g_fastActive = 0208E6B4 */
}
```

and the main loop turns the mode into the scalar every frame:

```c
if (g_fastModeEnabled == 0)  g_speedScalar = 1.0f;                      /* 02064AD2 == 0 */
else                         g_speedScalar = speedTable[g_speedMode];   /* 02064AC4 */

speedTable @ 0x00908BA8 = { 1.0f, 2.0f, 4.0f }
```

**So `Speed1` returns to normal speed, `Speed2` toggles 2×, `Speed3` toggles 4×** — and because
each branch resets when it is already in that mode, **pressing the same key twice turns the
speed-up off**. Shipped, they are `F1`, `F2` and `F3`.

**This settles open question Z-10 in the negative, and names the alternative.** `DAT_01DFE0B8`
is *not* the 2×/4× speed-mode scalar: `0x02064AC4` is, and it comes from a three-entry table
indexed by a mode word that only this key handler writes. See §8 for what `01DFE0B8` turned out
to be.

#### `WalkMode` — a toggle, not a hold

`0017DFC0` reports whether the walk key is held; `PartyControl_BuildAnalogMovementVectorFromInputHistory`
(`003594E0`) turns that into a latched toggle before it builds the movement vector:

```c
if (FUN_001E0C10() != 0)  g_walk = 0;                       /* gate closed: forced off */
else if (!IsWalkKeyHeld()) g_walkEdge = 0;
else { if (!g_walkEdge) g_walk = (g_walk == 0);  g_walkEdge = 1; }   /* rising edge -> flip */
                                                            /* g_walk = 022C800C, edge = 022C7FF9 */
```

so **tapping Left Shift switches walking on and leaves it on** — it is not a hold-to-walk
modifier. The flag is then consumed by `PartyControl_ComputeAnalogMovementScale` (`00358A20`),
whose result multiplies the analog movement vector.

### A third, independent agreement: the mask bit and the slot index

The same setting has a second consequence, documented from the settings side in
[the button convention](../../19-Save-Load-Settings/Language-And-Locale/language-selection-and-locale-ids.md):
`0022A4F0` writes the confirm mask `01E0C2A0` and the cancel mask `01E0C2A4`, and

```c
if (DecideButton == 0) { confirm = 0x2000; cancel = 0x4000; }
else                   { confirm = 0x4000; cancel = 0x2000; }
```

`0x2000` is **bit 13** and `0x4000` is **bit 14** — the same two indices as the swapped binding
slots, and `00197160` builds its control mask with `mask[i >> 3] &= ~(1 << (i & 7))` on the slot
index `i`, so bit position and slot index are the same axis. With `DecideButton = Circle`,
confirm is bit 13 and slot 13 is `Circle`. **Two mechanisms, derived from opposite ends of the
engine, agree on which index is Circle.** This is corroboration for slot 13 = `Circle`, not the
proof of it — that comes from the name table — and no claim is made here that all sixteen mask
bits map to slots.

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `00195060` | `InputManager_Initialize` | 153 B | clears the array, loads the file, validates, chooses publisher |
| `00197EE0` | `InputManager_BuildKeymapPath` | 273 B | builds the path, creating each directory |
| `00198000` | `InputManager_LoadKeymapIni` | 1,644 B | **the parser** — sections, `name=value`, name→slot lookup |
| `001993B0` | `InputManager_SaveKeymapIni` *(working name; ledger leaves it `FUN_001993b0`)* | 971 B | **the writer** — emits the 87 lines |
| `00197A50` | `Filebuf_OpenWithMode` *(working name)* | 229 B | `basic_filebuf<wchar_t>::open` → `_Fiopen(path, mode, prot)` |
| `00196550` | `InputManager_ValidateBindingUniqueness` | 135 B | no repeated id across 84 slots; no reserved id |
| `001965E0` | `InputManager_ValidateBindingIdRanges` | 159 B | all 28 slots of **profile 1** in `[1,152]` |
| `00195DF0` | `InputManager_RestoreDefaultBindingProfiles` | 526 B | **publishes the loaded/edited array** + the Circle/Cross swap |
| `00198B60` | `InputManager_MaterializeRuntimeBindingProfiles` | 782 B | **installs the shipped defaults** into the array and the records |
| `001DFA70` | `InputBinding_ShouldKeepAuthoredPairOrderForPlatformState` | 8 B | `return DecideButton == 0` |
| `0022A4F0` | `ApplyButtonConvention` *(working name)* | 66 B | writes the `0x2000`/`0x4000` confirm/cancel masks from the same field |
| `00196FF0` | `InputManager_PollAndBuildControlState` | 356 B | polls five records at `01DF1480`, then two conditional banks |
| `00197160` | `InputManager_TranslateBindingProfileToControlState` | 1,406 B | one record → the per-frame control mask |
| `00197710` | `InputManager_GetBinding` *(working name)* | 99 B | `(profile, group, slot)` → the stored code; the only reader of group 2 **as a binding** (§10) |
| `00196290` | `InputProfiles_CopyLiveRecordsBackToBank` *(working name)* | 488 B | copies 2 records `01F80130` → `01DF1738` |
| `001967D0` | `InputProfiles_ApplyConfirmBindingToPointerDevice` *(working name)* | 499 B | reads dword 13/14 keyed on `DecideButton` |
| `001E0F40` | `InputConfig_SaveKeymap` *(working name)* | 36 B | singleton → the writer |
| `001E0F70` | `InputConfig_ResetBindingsToShippedDefaults` *(working name)* | 49 B | `Materialize` then `Restore` |
| `001E1050` | `InputConfig_AssignBindingAndRepublish` *(working name)* | 164 B | assign one binding, map the result code, republish |
| `00198A00` | `InputManager_AssignBindingWithConflictPolicy` | 349 B | the single in-memory writer (documented by the neighbour) |
| `001F3ED0` | `Platform_GetSteamAccountIdString` *(working name)* | 159 B | `ISteamUser::GetSteamID` formatted `%llu`, or empty |
| `001F3EA0` | `Path_CreateDirectoryIfMissing` *(working name)* | 43 B | `_waccess` then `_wmkdir` |
| `00194EF0` | `Format_VSwprintfS` *(working name)* | 89 B | `__stdio_common_vswprintf_s`, 0x200-char bound |
| `0017DDC0` | `InputQuery_IsL2Held` *(working name)* | 67 B | `GetBinding(0, 0, 8)` → backend; the only reader of slot 8 |
| `0017DE10` | `InputQuery_IsR2Held` *(working name)* | 67 B | `GetBinding(0, 0, 9)` → backend; the only reader of slot 9 |
| `0017DEA0` | `InputQuery_PollSpeedModeKeys` *(working name)* | 276 B | `Speed1/2/3` → `SetSpeedMode(1/2/4)`, edge-latched |
| `0017DFC0` | `InputQuery_IsWalkModeKeyHeld` *(working name)* | 67 B | `GetBinding(0, 2, 3)` → backend |
| `001E0BD0` | `InputConfig_GetBinding` *(working name)* | 62 B | generic `(profile, group, slot)` getter, **10 distinct callers / 15 call sites** (§10) |
| `001E0AA0` | `InputConfig_GetBindingPacked` *(working name)* | 90 B | same, with a packed group/slot from `FUN_001e0650` |
| `00239790` | `GameSpeed_SetMode` *(working name)* | 141 B | 1 → normal, 2 → toggle 2×, 4 → toggle 4× |
| `00229ED0` | `GameSpeed_SetModeRaw` *(working name)* | 7 B | `g_speedMode = n` |
| `00229E20` | `GameSpeed_GetMode` *(working name)* | 7 B | `return g_speedMode` |
| `00229E00` | `GameSpeed_GetMultiplier` *(working name)* | 20 B | `return speedTable[g_speedMode]` |
| `002DE250` | `Present_SetSpeedField` *(working name)* | 24 B | packs `n & 0xF` into bits 23–26 of `[0215E6E0 + 4]` |
| `00182FB0` | `GameSpeed_NotifySubsystem` *(working name)* | 28 B | forwards the mode to `FUN_001d85c0` |
| `0022A770` | `MainLoop_RunFrame` *(working name)* | 2,001 B | polls the speed keys, computes `g_speedScalar` |
| `003594E0` | `PartyControl_BuildAnalogMovementVectorFromInputHistory` | 461 B | latches `WalkMode` into a toggle, builds the movement vector |
| `00358A20` | `PartyControl_ComputeAnalogMovementScale` | 274 B | consumes the walk flag |
| `001EDDC0` | `HostTiming_SelectFrameBaseAndTimerPeriod` *(working name)* | 165 B | **the sole writer of `01DFE0B4/B8/BC`** — see §8 |
| `0017D8F0` | `GameSetting_GetFrameLimit` *(working name)* | 11 B | `return *(u32 *)(GameSetting + 0x48)` |
| `0022BDF0` | `Startup_ParseCommandLineAndSelectFrameBase` *(working name)* | 146 B | `-nologo`, then `HostTiming_Select(FrameLimit == 1)` |

Addresses are Ghidra image base `0x00120000`. Every row above is a function and its body size is
an exact-current body extent from `DumpFullCoverageGraph.java` at the GN158 checkpoint.

### Data addresses cited by this document

**Data, not functions** — no body extent.

| Address | Name | Kind | Contents |
|---|---|---|---|
| `01F80F90` | binding array, group 0 base | `u32[84]`, 336 B | 3 profiles × 28 slots. **Not backed by raw file data** — zero at load |
| `01F80FD0` | group 1 base | — | `01F80F90 + 0x40`; profile stride `0x70` |
| `01F80FF0` | group 2 base | — | `01F80F90 + 0x60`; profile stride `0x70` |
| `01DF11E0` | key-name table, group 0 | 16 × `wchar_t *` | `Select` … `Square` |
| `01DF1260` | key-name table, group 1 | 8 names + NULL | `RX_P` … `LY_N` |
| `01DF12E0` | key-name table, group 2 | 4 names + NULL | `Speed1`, `Speed2`, `Speed3`, `WalkMode` |
| `01DF1360` | key-name table, group 3 | 3 names + NULL | `Mouse1`, `Mouse2`, `Mouse3` — **never iterated**, see §6 |
| `01DF13E0` | reserved control ids | `u32[35]`, 140 B | ids the config refuses; see §4 |
| `01DF09C0` | shipped defaults, group 0 | 3 × 0x40 B | the 16 button codes per profile |
| `01DF0A80` | shipped defaults, record tail | 3 × 0x100 B | 16 × `{kind, 4, codeA, codeB}`; group 1 comes from records 0–3 |
| `01DF1470` | shipped defaults, group 2 | `u32[4]`, 16 B | `65, 66, 67, 118` — Speed1/2/3 + WalkMode, **profile 1 only** |
| `01DF1480` | runtime profile bank | 5 × `0x15C` B | polled every frame; records 2–4 are the keyboard profiles |
| `01DF1738` | keyboard profile records | `01DF1480 + 2 × 0x15C` | where the swap happens, before the copy out |
| `01F80130` | published profile table | 3 × `0x15C` B | the second destination of the publish |
| `01F80D90` | keymap path buffer | wide string | written by `BuildKeymapPath`, read by both parser and writer |
| `01F82D20` | GameSetting.ini object pointer | object pointer | `+0x64` is `DecideButton` |
| `008F3988` | `L"[Keyboard"` | wide literal | the section prefix, written and (as `L"Keyboard"`, `008F39E0`) matched |
| `008F3984` | `L"]"` | wide literal | section terminator emitted by the writer |
| `008F3980` | `L"\n"` | wide literal | **line terminator — LF, not CRLF** |
| `008F399C` | `L"="` | wide literal | key/value separator emitted by the writer |
| `008F38A8` | `L"keymap.ini"` | wide literal | the file name |
| `008F3848` | `L"\\My Games\\"` | wide literal | path segment |
| `008F3860` | `L"FINAL FANTASY XII THE ZODIAC AGE\\"` | wide literal | path segment |
| `008F3160` | `L"\\My Games\\FINAL FANTASY XII THE ZODIAC AGE\\keymap.ini"` | wide literal | **no code reference found**; see §7 |
| ~~`01F45700`~~ **`01F456C8`** | `PInputKeySemantic` member records | ~~95~~ **97** × 32 B | **CORRECTED 2026-09-08.** `123 … 28` plus `Empty = 0`; node is `{typeRef, namePtr, next, value}`. The old span was anchored on the **value field at node + 0x18** and stopped one record short at each end, omitting `Empty` and **`Key_A` (28)**. Stride and value range were right. [the input name registry](../Input-Name-Registry/the-input-name-registry-and-channel-aliases.md) §5 |
| `01CD84D8` | `PInputKeySemantic` name strings | ASCII run | `Key_A` … `Key_Right_Alt` |
| `00908BA8` | game-speed multiplier table | 3 × `f32`, `.rdata` | **`1.0f, 2.0f, 4.0f`** |
| `01FD4A98` | current game-speed mode | `s32` | 0 / 1 / 2 — **1 writer, 4 readers** |
| `02064AC4` | published game-speed scalar | `f32` | `speedTable[mode]`, or `1.0f` when disabled |
| `02064AD2` | game-speed feature enable | `u8` | 2 writers, 3 readers, all in the main loop |
| `0208E6B4` | "a speed-up is active" flag | `s32` | set/cleared by `GameSpeed_SetMode` |
| `01F7F4E9` | speed-key edge latch | `u8` | stops a held key retriggering |
| `022C800C` | walk-mode flag | `u32` | toggled on the walk key's rising edge |
| `022C7FF9` | walk-key edge latch | `u8` | |
| `01DFE0B4` | frame-base integer | `s32` | ships `1`; `2` when `FrameLimit = 60` |
| `01DFE0B8` | frame-base multiplier | `f32` | ships `1.0`; `2.0` when `FrameLimit = 60` |
| `01DFE0BC` | per-tick locomotion multiplier | `f32` | ships `1.0`; `0.5` when `FrameLimit = 60` |
| `01CEBC08` / `01CEBB70` | the two constants written into them | `f32` | `2.0f` and `0.5f` |
| `01DFD050` | GameSetting key table | 31 × `char *` | index 18 = `FrameLimit`, index 25 = `DecideButton` |
| `01DFD150` | GameSetting value-name table | 31 × 9 × `char *` | row 18 = `{"30", "60"}`, row 25 = `{"Circle", "Cross"}` |

## 4. Data structures and formulas

### The file

```
[Keyboard1]<LF>
Select=40<LF>
...                       28 lines
[Keyboard2]<LF>
...                       28 lines
[Keyboard3]<LF>
...                       28 lines
```

Plain ASCII, **LF line endings**, no trailing blank line, 87 lines. The shipped default file is
699 bytes.

Grammar as the parser actually accepts it:

```
line      := blank | section | binding | <anything else: STOPS THE LOAD>
blank     := ""                                   /* skipped */
section   := <any one char> "Keyboard" <digits> "]" <anything>
             /* char 1 unchecked; digits parsed by wcstol; index = value - 1 */
binding   := <name> "=" <digits>
             /* name compared case-insensitively; unknown name silently ignored */
```

### Slot map — the 28 names, in file order and slot order

Name index in the table **is** the dword index in the profile. Profile stride is `0x70`
(28 dwords, 112 bytes).

| Slot | Byte off. | Name | Group | Meaning |
|---:|---|---|---:|---|
| 0 | `+0x00` | `Select` | 0 | Select |
| 1 | `+0x04` | `L3` | 0 | left stick click |
| 2 | `+0x08` | `R3` | 0 | right stick click |
| 3 | `+0x0C` | `Start` | 0 | Start |
| 4 | `+0x10` | `Up` | 0 | D-pad up |
| 5 | `+0x14` | `Right` | 0 | D-pad right |
| 6 | `+0x18` | `Down` | 0 | D-pad down |
| 7 | `+0x1C` | `Left` | 0 | D-pad left |
| 8 | `+0x20` | `L2` | 0 | **zeroed by both publishers** |
| 9 | `+0x24` | `R2` | 0 | **zeroed by both publishers** |
| 10 | `+0x28` | `L1` | 0 | L1 |
| 11 | `+0x2C` | `R1` | 0 | R1 |
| 12 | `+0x30` | `Triangle` | 0 | Triangle |
| **13** | **`+0x34`** | **`Circle`** | 0 | **swapped with slot 14 when `DecideButton != 0`** |
| **14** | **`+0x38`** | **`Cross`** | 0 | **swapped with slot 13 when `DecideButton != 0`** |
| 15 | `+0x3C` | `Square` | 0 | Square |
| 16 | `+0x40` | `RX_P` | 1 | right stick, +X |
| 17 | `+0x44` | `RX_N` | 1 | right stick, −X |
| 18 | `+0x48` | `RY_P` | 1 | right stick, +Y |
| 19 | `+0x4C` | `RY_N` | 1 | right stick, −Y |
| 20 | `+0x50` | `LX_P` | 1 | left stick, +X |
| 21 | `+0x54` | `LX_N` | 1 | left stick, −X |
| 22 | `+0x58` | `LY_P` | 1 | left stick, +Y |
| 23 | `+0x5C` | `LY_N` | 1 | left stick, −Y |
| 24 | `+0x60` | `Speed1` | 2 | game-speed setting 1 |
| 25 | `+0x64` | `Speed2` | 2 | game-speed setting 2 |
| 26 | `+0x68` | `Speed3` | 2 | game-speed setting 3 |
| 27 | `+0x6C` | `WalkMode` | 2 | walk instead of run |

Flat index arithmetic, exactly as reader, writer and the accessor all compute it:

```c
group 0:  addr = 0x01F80F90 + profile * 0x70 + slot * 4;   /* slot 0..15 */
group 1:  addr = 0x01F80FD0 + profile * 0x70 + slot * 4;   /* slot 0..7  */
group 2:  addr = 0x01F80FF0 + profile * 0x70 + slot * 4;   /* slot 0..3  */
```

### The control-code space, for the keyboard range

The numbers on the right of `=` are control codes. `InputManager_ValidateBindingIdRanges`
requires every one of profile 1's twenty-eight to satisfy `1 <= code <= 152`, and
`InputManager_TranslateBindingProfileToControlState` routes them by band —
`(code - 1) < 3`, `(code - 0x0B) < 0x11`, `(code - 0x1C) < 0x7D`, i.e. **1–3**, **11–27** and
**28–152**. Codes 4–10 are polled by nothing.

Band **28–152** is the keyboard. Its codes are the engine's Phyre `PInputKeySemantic`
enumeration **minus one**:

```
keymapCode = PInputKeySemantic - 1
```

| Codes | Keys |
|---|---|
| 28 – 53 | `A` … `Z`, in alphabetical order |
| 54 – 63 | `1` `2` `3` `4` `5` `6` `7` `8` `9` `0` |
| 64 | `Escape` |
| 65 – 76 | `F1` … `F12` |
| 77 – 80 | `Enter`, `Backspace`, `Tab`, `Space` |
| 81 – 90 | `-` `=` `[` `]` `\` `;` `'` `,` `.` `/` |
| 91 – 94 | `Left`, `Right`, `Up`, `Down` |
| 95 – 100 | `Home`, `End`, `PageUp`, `PageDown`, `Insert`, `Delete` |
| 101 – 110 | `Numpad1` … `Numpad9`, `Numpad0` |
| 111 – 116 | `Numpad/`, `Numpad*`, `Numpad-`, `Numpad+`, `NumpadEnter`, `Numpad.` |
| 117 – 122 | `LeftCtrl`, `LeftShift`, `LeftAlt`, `RightCtrl`, `RightShift`, `RightAlt` |
| 123 – 152 | above the keyboard; not identified here — see §7 |

Worked check, using the shipped defaults and this table alone: `LX_N = 28` = `A`,
`LX_P = 31` = `D`, `LY_N = 50` = `W`, `LY_P = 46` = `S` — **W A S D, with +Y pointing down**;
`RX_N/RX_P/RY_N/RY_P = 91/92/93/94` — **the four arrow keys**; `Up/Left/Down/Right =
36/37/38/39` — **I J K L**; `Speed1/2/3 = 65/66/67` — **F1 F2 F3**; `WalkMode = 118` —
**Left Shift**; `Circle = 80` — **Space**.

### The 35 reserved control ids at `01DF13E0`

Read raw from the image, in stored order:

```
2, 81, 82, 84, 85, 88, 89, 90, 123, 119, 122, 130, 125, 131, 132, 133, 134, 135,
136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152
```

Decoded with the table above, the ones inside the keyboard range are:

```
 81 '-'        82 '='        84 ']'        85 '\'
 88 ','        89 '.'        90 '/'
119 LeftAlt   122 RightAlt
```

`2` sits in the 1–3 band; `123`, `125` and the contiguous run `130`–`152` are above the keyboard
range. `152` is exactly the top of the polling band, so the reserved set ends where the code
space does. Reserving both Alt keys is consistent with Windows owning `Alt+Tab` / `Alt+F4`; why
`-` `=` `]` `\` `,` `.` `/` are reserved while `[` `;` `'` are not is **not established**.

**The reserved test runs on every slot the file fills**, inside
`ValidateBindingUniqueness` — so one reserved id anywhere in the file discards the entire file.

### The shipped defaults, decoded

Read from `01DF09C0` (group 0), `01DF0A80` (group 1, the `codeA`/`codeB` fields of records 0–3)
and `01DF1470` (group 2). These are also, byte for byte, the contents of the keymap.ini that
ships to a new player.

| Slot | Name | Keyboard1 | Keyboard2 | Keyboard3 |
|---:|---|---|---|---|
| 0 | `Select` | 40 `M` | 114 `Numpad+` | 53 `Z` |
| 1 | `L3` | 79 `Tab` | 0 | 0 |
| 2 | `R3` | 35 `H` | 110 `Numpad0` | 51 `X` |
| 3 | `Start` | 64 `Escape` | 0 | 0 |
| 4 | `Up` | 36 `I` | 108 `Numpad8` | 0 |
| 5 | `Right` | 39 `L` | 106 `Numpad6` | 32 `E` |
| 6 | `Down` | 38 `K` | 102 `Numpad2` | 0 |
| 7 | `Left` | 37 `J` | 104 `Numpad4` | 44 `Q` |
| 8 | `L2` | 55 `2` | 0 | 0 |
| 9 | `R2` | 117 `LeftCtrl` | 0 | 0 |
| 10 | `L1` | 54 `1` | 0 | 0 |
| 11 | `R1` | 56 `3` | 0 | 0 |
| 12 | `Triangle` | 45 `R` | 0 | 0 |
| 13 | `Circle` | 80 `Space` | 77 `Enter` | 1 *(band 1–3)* |
| 14 | `Cross` | 30 `C` | 78 `Backspace` | 3 *(band 1–3)* |
| 15 | `Square` | 33 `F` | 0 | 0 |
| 16 | `RX_P` | 92 `Right` | 0 | 0 |
| 17 | `RX_N` | 91 `Left` | 0 | 0 |
| 18 | `RY_P` | 94 `Down` | 0 | 0 |
| 19 | `RY_N` | 93 `Up` | 0 | 0 |
| 20 | `LX_P` | 31 `D` | 0 | 0 |
| 21 | `LX_N` | 28 `A` | 0 | 0 |
| 22 | `LY_P` | 46 `S` | 0 | 0 |
| 23 | `LY_N` | 50 `W` | 0 | 0 |
| 24 | `Speed1` | 65 `F1` | 0 | 0 |
| 25 | `Speed2` | 66 `F2` | 0 | 0 |
| 26 | `Speed3` | 67 `F3` | 0 | 0 |
| 27 | `WalkMode` | 118 `LeftShift` | 0 | 0 |

Note that only profile 1 gets group-2 defaults: `01DF1470` is written to `01F80FF0` **outside**
the three-profile loop, as a single 16-byte SSE store.

### The two validators, exactly

```c
/* 00196550 — returns 1 if ANY problem is found, 0 if clean */
for (flat = 0; flat <= 0x53; flat++) {                   /* all 84 slots */
    id = bindings[flat];
    for (j = flat + 1; j <= 0x53; j++)
        if (id != 0 && id == bindings[j]) return 1;      /* duplicate (0 does not count) */
    for (k = 0; k < 35; k++)
        if (id == reserved[k])          return 1;        /* reserved id */
}
return 0;
```

```c
/* 001965E0 — returns 0 if profile 1 is completely valid, 1 otherwise */
n = 0;
for (slot = 0; slot < 28; slot++) {
    v = bindings[slot];                                  /* PROFILE 1 ONLY: base 01F80F90 */
    if ((unsigned)(v - 1) > 0x97) break;                 /* i.e. v < 1 || v > 152 */
    n++;
}
return !(n >= 0x1C);                                     /* 0 == "all 28 are legal" */
```

The outer `for (i = 0; i < 3; i++)` around that scan re-runs it on the **same** base three times
— the profile index is never applied. Profiles 2 and 3 are therefore range-checked by nothing.
(Instruction-level: `r11` is loaded once with `01F80F94` at `001965EB` and is not modified
inside the loop at `00196600`.)

Composed gate, as `InputManager_Initialize` evaluates it:

```c
if (ValidateBindingUniqueness() == 0 && ValidateBindingIdRanges() == 0)
        RestoreDefaultBindingProfiles();      /* publish what the file loaded */
else    MaterializeRuntimeBindingProfiles();  /* install the shipped defaults */
```

With no file at all the array is 336 zero bytes: uniqueness passes (0 is neither a duplicate nor
reserved), the range check fails at slot 0, and the defaults are installed.

### The profile record the publishers build

```
ProfileRecord — 0x15C bytes; the bank at 01DF1480 holds five, the table at 01F80130 holds three

  +0x00 .. +0x3F   16 x u32   group 0 button codes, copied 1:1 from the binding array
                              (+0x20/+0x24, i.e. L2 and R2, are then overwritten with 0)
                              (+0x34 <-> +0x38, i.e. Circle and Cross, exchanged if DecideButton != 0)
  +0x40 .. +0x13F  16 x 16 B  { u32 kind, u32 4, u32 codeA, u32 codeB }
                              kind 2 = an axis pair (group-1 slots), kind 1 = a single code
  +0x140 .. +0x15B 0x1C B     zeroed by the defaults path
```

`RestoreDefaultBindingProfiles` reads the binding array only from `+0x00` to `+0x5F` — groups 0
and 1. **The four group-2 slots are not read by it at all**; the only reader of group 2 found in
this pass is the accessor `FUN_00197710`, which indexes `01F80FF0` directly.

## 5. Call chain

> **The owner transition is `00198750`, not `00195060`** — corrected while labelling under
> `CALL-CHAINS.md` rule 6, 2026-09-18. The marker used to sit on `00195060`, but both of those are
> Input's own functions; the crossing is one row above, where `0017D4C0` — Engine Core Runtime's
> startup — first calls into this subsystem. **AUTHORITY** because Input decides everything that
> follows: the caller passes nothing, and the keymap path, the Steam account id and the ini
> contents are all read on this side.

```
startup                                                        0017D4C0, Engine Core Runtime
  -> InputManager_CreateSingleton                 00198750      [AUTHORITY 00 -> 15]
     -> InputManager_Initialize                   00195060
        -> memset(01F80F90, 0, 0x150)
        -> InputManager_BuildKeymapPath           00197EE0
             -> SHGetFolderPathW / _waccess / _wmkdir / wsprintfW
             -> Platform_GetSteamAccountIdString  001F3ED0  -> SteamInternal_ContextInit
        -> InputManager_LoadKeymapIni             00198000
             -> _Fiopen via FUN_00197a50, getline, wcschr, wcsncpy, _wcsicmp, wcstol
             -> writes 01F80F90 through the name tables at 01DF11E0
        -> InputManager_ValidateBindingUniqueness 00196550
        -> InputManager_ValidateBindingIdRanges   001965E0
        -> clean  -> InputManager_RestoreDefaultBindingProfiles   00195DF0
                       -> InputBinding_ShouldKeepAuthoredPairOrderForPlatformState 001DFA70
                          -> GameSetting[0x64] "DecideButton"
                       -> Circle/Cross exchange at record +0x34 / +0x38
                       -> 01DF1738 (bank records 2-4) and 01F80130
        -> not clean -> InputManager_MaterializeRuntimeBindingProfiles 00198B60
                       -> 01DF09C0 / 01DF0A80 / 01DF1470  ->  01F80F90 and the same records

options screen
  -> InputConfig_AssignBindingAndRepublish        001E1050
       -> InputManager_AssignBindingWithConflictPolicy 00198A00   [the only in-memory writer]
       -> InputManager_RestoreDefaultBindingProfiles   00195DF0   (republish)
  -> InputConfig_ResetBindingsToShippedDefaults   001E0F70
       -> Materialize, then Restore
  -> InputConfig_SaveKeymap                       001E0F40
       -> InputManager_SaveKeymapIni              001993B0        [file written here, not before]

per frame
  -> InputManager_PollAndBuildControlState        00196FF0
       -> 5 x TranslateBindingProfileToControlState over the bank at 01DF1480
          (records 2-4 are the three keyboard profiles) into ONE shared mask

per frame, NOT through the mask -- the six on-demand slots
  -> MainLoop_RunFrame                           0022A770   ["[PS2]fast mode"]
       -> InputQuery_PollSpeedModeKeys           0017DEA0
            -> GetBinding(profile 1, group 2, slots 0/1/2)  = Speed1 / Speed2 / Speed3
            -> GameSpeed_SetMode 00239790 -> g_speedMode 01FD4A98
       -> g_speedScalar 02064AC4 = speedTable[g_speedMode]   { 1.0, 2.0, 4.0 } @ 00908BA8
  -> PartyControl_BuildAnalogMovementVectorFromInputHistory  003594E0
       -> InputQuery_IsWalkModeKeyHeld           0017DFC0
            -> GetBinding(profile 1, group 2, slot 3)        = WalkMode
       -> toggles g_walk 022C800C -> PartyControl_ComputeAnalogMovementScale 00358A20
  -> InputQuery_IsL2Held / IsR2Held              0017DDC0 / 0017DE10
            -> GetBinding(profile 1, group 0, slots 8/9)     = L2 / R2

startup, unrelated to the keymap but sharing the settings object
  -> Startup_ParseCommandLineAndSelectFrameBase   0022BDF0
       -> GameSetting_GetFrameLimit               0017D8F0   -> GameSetting + 0x48  {"30","60"}
       -> HostTiming_SelectFrameBaseAndTimerPeriod 001EDDC0
            -> FrameLimit=60: 01DFE0B4=2, 01DFE0B8=2.0f, 01DFE0BC=0.5f
            -> FrameLimit=30: timeGetDevCaps + timeBeginPeriod, the three keep 1 / 1.0 / 1.0
```

**Upstream (who causes this):** the input manager's own construction, and the options screen
through the three small `001E0F40` / `001E0F70` / `001E1050` entry points. The **owner
transition** is `InputManager_Initialize` — above it the bindings are a file, below it they are
`Input`-owned runtime state.

**Downstream (what this causes):** the per-frame control mask built by `00197160`, described in
[binding profiles and control-state translation](binding-profiles-remapping-and-control-state.md),
and from there the
[capability policy](../Gameplay-Capability-Policy/capability-inhibition-policy.md).

**Do not confuse with:**

- **`GameSetting.ini` is a different file with a different parser.** It lives beside
  `keymap.ini` and holds `DecideButton` — the setting that drives the Circle/Cross swap — but it
  is read by `001DF350`, not by anything here. See
  [the settings object](../../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md).
- **A `keymap.ini` with `[Setting]` / `[Button]` / `[Analog]` / `[KeyFunction]` / `[Mouse]`
  sections and `keyN=` lines is not this file.** That format's section names do not occur
  anywhere in this executable, while `[Keyboard` does — the same scan, same run. Such a file in
  a mod's `ConfigData` folder comes from some other tool.
- **The two publishers' names are the wrong way round**, see below. This is the single easiest
  mistake to make when reading this subsystem.

### Naming correction — `Restore…` publishes, `Materialize…` restores

The ledger names are `InputManager_RestoreDefaultBindingProfiles` (`00195DF0`) and
`InputManager_MaterializeRuntimeBindingProfiles` (`00198B60`). Their bodies do the opposite of
what those names suggest, and this document uses the bodies:

| | `00195DF0` "Restore" | `00198B60` "Materialize" |
|---|---|---|
| reads | `01F80F90` — **the editable array**, i.e. what the file loaded or the player just remapped | `01DF09C0` / `01DF0A80` / `01DF1470` — **authored constants** |
| writes | the profile records only | the records **and** `01F80F90` |
| effect | **publishes the current bindings** | **overwrites the current bindings with the shipped defaults** |

Two call sites settle it independently of any reading of the bodies:

- `001E0F70` — "reset to defaults" — calls **`Materialize` and then `Restore`**, in that order.
  That sequence is only coherent as *install the shipped defaults into the editable array, then
  publish that array*. If `Restore` restored defaults, the first call would be pointless.
- `001E1050` — "assign one binding" — calls the assigner and then **only `Restore`**. Publishing
  the array the assigner just edited is the only thing that makes the remap take effect.

The GFZ is not overwritten and its names are kept in the tables above.

## 6. Modding notes

- **Best intervention point: the file.** `keymap.ini` is authored data, plain ASCII, and the
  supported surface. Edit it with the game closed; it is read exactly once, at input-manager
  construction, and written only when the options screen asks.

- **Write all 87 lines.** The validator requires **all twenty-eight of profile 1's slots** to
  hold a code in `[1,152]`. Leaving one at `0` — including `Speed1`, `Speed2`, `Speed3` and
  `WalkMode`, which many hand-written files omit — discards the *entire* file, all three
  profiles, silently.

- **Never repeat a code, in any profile.** The uniqueness scan spans all 84 slots. Binding `W`
  in `Keyboard1` and again in `Keyboard3` throws the file away. Zeros are exempt.

- **Do not use a reserved code**: `2`, `81`, `82`, `84`, `85`, `88`, `89`, `90`, `119`, `122`,
  `123`, `125`, `130`–`152`. One of them anywhere discards the file.

- **Codes 4–10 are accepted by the validator and polled by nothing.** A slot holding 4 through
  10 passes every check and then does nothing at all — the worst failure mode in this format,
  because it looks correct.

- **Regenerates itself:** the profile records at `01DF1480` and `01F80130` are rebuilt from
  `01F80F90` every time anything republishes. Write the array (or the file), never the records.

- **`Circle` and `Cross` may trade places after loading.** If you are computing what a key will
  do, read `DecideButton` from `GameSetting.ini` first: with `Cross`, the file's `Circle` line is
  the cancel key and its `Cross` line is the confirm key.

- **`L2` and `R2` are zeroed on the way out — and that is deliberate, not a bug.** Both
  publishers write `0` over record `+0x20`/`+0x24`, so `L2` and `R2` never appear in the
  per-frame mask; two dedicated predicates (`0017DDC0`, `0017DE10`) read those two slots
  straight out of the binding array instead. Rebinding them in the file works normally.

- **Six slots are read from profile 1 only.** `L2`, `R2`, `Speed1`, `Speed2`, `Speed3` and
  `WalkMode` are all fetched as `GetBinding(profile 1, …)`. **Binding them in `[Keyboard2]` or
  `[Keyboard3]` has no effect** — the value is stored, saved and validated, and never read. This
  is the second silent-no-op in the format, after codes 4–10.

- **The speed keys are the only keyboard route to 2× and 4×.** If you want a different speed key,
  change `Speed2` / `Speed3` in `[Keyboard1]`; there is no other binding surface for them.

- **`Mouse1`, `Mouse2`, `Mouse3` are defined and unreachable.** A fourth name table exists at
  `01DF1360`, but both the parser and the writer iterate exactly three groups
  (`while (group + 1 < 3)`, `for (group = 0; group < 3; group++)`), so those lines are ignored on
  read and never emitted on save. *(Positive control: the same loop does reach group 2 —
  `Speed1`…`WalkMode` are matched — so this is a bound, not a broken instrument.)*

- **Breaks if:**
  - A `Name=value` line appears **before** any `[KeyboardN]` header. The profile index starts at
    `-1` and is never bounds-checked, so the write lands at
    `0x01F80F90 - 0x70 = 0x01F80F20` — outside the array. `[Keyboard0]` does the same;
    `[Keyboard99]` writes at `0x01F80F90 + 98 * 0x70`.
  - Any non-blank line lacks both a `Keyboard…]` header shape and an `=`. The load stops there
    and the rest of the file is discarded. **There is no comment syntax.**
  - A line exceeds 127 characters — `getline` fails and the load stops.
  - More than five digits sit between `[Keyboard` and `]`: the destination scratch is 12 bytes.
  - You expect CRLF. The writer emits bare `\n`; editors that rewrite the file as CRLF leave a
    stray `\r` at the end of every value, which `wcstol` stops at, so the values still parse —
    but a `\r` on a section line lands inside the digits.

- **Multiplayer / XIIOnline:** `keymap.ini` is **local input configuration and must never be
  replicated.** Two clients with different keymaps must produce identical gameplay effects. What
  belongs on the wire is the resulting intent, never the control code that produced it — and
  never `DecideButton`, which changes what a given control code means locally.

- **Mod compatibility:** two mods that both ship a `keymap.ini` overwrite each other completely;
  the format has no versioning, no partial merge and no per-key ownership. Shipping the file at
  all replaces the player's own bindings.

## 7. What is not known

- [x] **DM-2.** What control codes `123`, `125` and `130`–`152` are, and why `-` `=` `]` `\` `,` `.` `/`
      are reserved while `[` `;` `'` are not.
      **Narrowed 2026-09-18 (FABLE): the thirty codes are named from the keyboard's own scancode table; the reserved-set rationale stays open.* The physical keyboard is DirectInput (`DINPUT8.dll` is imported), and `DirectInputKeyboard_PollState` (`007A1640`) turns keymap codes into scancodes through a **125-byte table at `01F3DAB0`, indexed by `code − 28`**: after `GetDeviceState` (device vtable `+0x38`, retried on `DIERR_INPUTLOST`) it walks the table (`007A1730`–`007A1758`) and, for every non-zero entry, sets the device's per-code byte at `+0x231 + (code − 28)` when bit 7 of the DirectInput state byte at that scancode is set. Entries 0–94 (codes 28–122) reproduce §4's table exactly (`A` = `DIK_A 0x1E` … `RightAlt` = `DIK_RMENU 0xB8`), which is the check. **Codes 123–152 are**: 123 the grave key `` ` `` (`DIK_GRAVE`), 124 `CapsLock`, 125 `LeftWindows`, 126 `NumLock`, 127 `ScrollLock`, 128 `Pause`, 129 `SysRq`, 130 `Apps`, 131 `RightWindows`, 132–134 `F13`–`F15`, 135 unmapped (entry `0`), 136 `ABNT_C1`, 137 `Convert`, 138 `NoConvert`, 139 `Yen`, 140 `ABNT_C2`, 141 `Numpad=`, 142 `PrevTrack`, 143 `AT`, 144 `Colon`, 145 `Underline`, 146 `Kanji`, 147 `Stop`, 148 `AX`, 149 `Unlabeled`, 150 `NextTrack`, 151 `Mute`, 152 `Numpad,` — the DirectInput scancode set past the main keyboard, in `DIK_` order; entry 153 onward is zero, which is why 152 tops the polling band. So the reserved run 130–152 is the Apps, Windows, `F13`–`F15`, Japanese and Brazilian layout and media keys, 125 the left Windows key and 123 the grave key. **Why `-` `=` `]` `\` `,` `.` `/` and both Alts are reserved while `[` `;` `'` are not is still not established**: no caller of the keyboard pollers `0079E6A0` / `0079E650` asks for any code by constant (all fifteen sites take the code from a profile slot), so the reservation is not enforced by a competing fixed binding in this image. A second, unrelated 128-byte table precedes it at `01F3DA30`: ASCII character → keymap code (`A` or `a` → 28, `1` → 54, `Esc` → 64, space → 80), used by the injected-key handlers `00797EE0` / `00797F20` / `00797F60`. Static: the poll body and the two tables read from the image.*
- [x] **The 11–26 band is ANSWERED 2026-09-08: the sixteen pad buttons, and the "conflicting
      values" are ALIASES.** `PInputChannelSemantic` registers **143 names over 113 channels**;
      channels 11–26 each carry a bare index, an Xbox letter, a PlayStation glyph and — for 11,
      12, 13 — a mouse button. Mouse and joypad names share one channel space by design, so a
      framing that expects two disjoint tables must read it as a conflict.
      [the input name registry](../Input-Name-Registry/the-input-name-registry-and-channel-aliases.md) §4. ~~**The 1–3 band and 27 remain open**~~ **Codes 1–3 answered 2026-09-12 (FABLE): the three mouse buttons.** `InputBackend_IsPrimaryControlCode1To3Active` (`0079E6D0`) returns byte `+0x1E0 + (code − 1)` of the device at backend `+0x150`, and `0079D010` fills those three bytes by asking that device for **channels 11, 12 and 13** (`lea edx, [r13 + 0xB]`, loop bound 3, `0079D140`–`0079D1A3`) — the channels whose registered aliases include the mouse buttons — storing a byte only when the state changed. So control codes 1–3 are `Mouse1`–`Mouse3` (the never-iterated name table at `01DF1360`) read from input device **type 0** — backend `+0x150` is filled by `0079A430` with `00796FC0(0, 0)`, the first registered device whose type method returns 0, while types 3 and 4 are looked up per player (`0079DE7A`, `0079E10C`); that type 0 is the mouse rests on the channel aliases and the name table, not on a read type enum *(wording narrowed the same day)* — separately from the pad band 11–26 that shares those channel numbers. **Channel 27 remains open**; no registered channel name has a
      value in `1 … 10` or `27`. `DM-2`. *(Marker normalised 2026-09-30 (FABLE, [record](../../_index/candidates/qid-marker-truth-fable-0930/README.md)): every code band is answered, and DM-2 is closed NO ADMISSIBLE SOURCE.)*
      *Narrowed 2026-09-27 (FABLE, Claude Opus 5.5): code 27 is the 17th pad slot, and only a DirectInput pad fills it.*
      The band readers map `code − 11 ≤ 16` onto the controller's raw bytes `+0x43C`..`+0x44C`. The XInput and Steam
      polls fill slots 0–15 only, the sixteen buttons named on channels 11–26. The DirectInput poll alone copies
      `rgbButtons[16]` into slot 16. So 27 is a DirectInput pad's 17th button, always 0 on XInput and Steam pads, and
      that is why no channel name carries it. [The code-27 record](../../_index/candidates/dm2-code27/README.md),
      control `dm2_code27.py`, 5 checks. With this, every code DM-2 names is identified. The reserved-set rationale
      in the box above is the only residue; nothing in the image separates the two groups but the blacklist, and it
      is with OPUS as [review package 5](../../_index/candidates/nas-package-5-2026-09-27/README.md).
      ***CLOSED 2026-09-27: NO ADMISSIBLE SOURCE for the rationale, REVIEWED AND SIGNED by OPUS (kind b, intent; FABLE, Claude Opus 5.5, author).** OPUS re-ran `nas5_reserved.py` R1-R5 and added a Win32 virtual-key compare negative; nothing in the image separates `-` `=` `]` `\` `,` `.` `/` and the Alts from `[` `;` `'` except the blacklist itself. Every code the row names is identified (above); why the designers reserved one group and not the other is intent the build does not carry.*
- [x] ~~What `FUN_001E0C10` (21 B, `Input`) gates — it forces walk mode off when non-zero.~~ **Answered 2026-09-14 (FABLE): whether
      an analog axis moved.** `001E0C10` returns the byte `InputManager + 0x38` (`InputManager_GetSingleton` `00198790`, then
      `00197780`).
      - **Set.** Its one setter is `InputManager_TranslateBindingProfileToControlState` `00197160`. It stores `1` at
        `0019744B` when the scaled value from `InputBackend_GetFilteredAnalogAxisValue` (`001973F4`) is non-zero. It skips
        the store only when `[01F81268] == 1`, and that object is always 0 (`DC-2`,
        [binding profiles](binding-profiles-remapping-and-control-state.md)).
      - **Cleared or set explicitly.** `00198E70(mgr, value)` writes it, called from `0017D1E0` and `001E1100`. The
        constructor `00195060` stores word `0x100` at `+0x38`, which makes `+0x38 = 0` and `+0x39 = 1`.

      So walk mode is forced off while a stick is giving graded movement. Its eleven callers (`00276AF6` … `00393C6E`)
      were not each read.
- [x] **UQ-142.** What `Present_SetSpeedField` (`002DE250`) bits 23–26 of `[0215E6E0 + 4]` control, and what
      `GameSpeed_NotifySubsystem` (`00182FB0` → `FUN_001d85c0`) tells its subsystem. Both are
      downstream of the speed mode and neither was read.
      *Narrowed 2026-09-14 (FABLE), not answered: the field is read; the notified subsystem is not named.*
      - **The field is the saved fast-forward choice.** It is a 4-bit field in the saved options record `*(0215E6E0)` (the
        record whose `+0x08`–`+0x0C` words hold the three category volumes). Its writer `002DE250` is also **settings command
        `0x0E`** (`002407F0` arm `002408B8`), which calls `0023B2E0` right after storing. Its getter `002DDDA0` is read by
        `0023B2E0`, by the settings getter `002403F0` (`00240493`) and by `00233700`.
      - **`0023B2E0` re-applies the choice only while fast mode is on** (`01FD4A98 != 0`). Field 0 sets the speed mode to 1
        and calls `00182FB0(1)`; field 1 sets it to 2 and calls `00182FB0(2)`. So changing the option mid-fast-forward
        switches between 2× and 4× at once.
      - **`00182FB0(n)`** fetches the lazily built `0x90`-byte singleton `[01F82CD0]` (`001D8210`, created by `001D8150`;
        [game application](../../00-Engine-Core-Runtime/Application-Root/game-application.md)). `001D85C0` then writes
        `+0x60 = 255.0`, `+0x64 = 6.0`, `+0x6C = 1.5`, `+0x69 = 1`, and copies `+0x58` into `+0x40` for `n == 2`, or
        `+0x48` otherwise. That is the shape of a timed on-screen indicator with two presets, but what the object draws
        was not traced.
      **ANSWERED 2026-09-18 (FABLE) — the notified subsystem is the `ExtraUI` overlay, and the notification arms the on-screen fast-forward icon.** The `0x90`-byte singleton `[01F82CD0]` that `00182FB0` fetches installs the vtable `00900370` (`001D8195`), whose RTTI locator names the class **`ExtraUI`**; its constructor `001D8150` zeroes the record and sets `+0x6C = 1.0`. `001D7150` fills it from the record table `[0209AC30] + 0xA0` (`0027E9D0`) through `ImageAddress_ResolveRuntimePointer` `0020E600`, `002A0060` and `0024B0C0`: a first icon set at `+0x10` .. `+0x28` and `+0x70` .. `+0x80`, and a second set at `+0x30` .. `+0x38` with three sprite records `+0x48`, `+0x50`, `+0x58`. **`001D85C0(n)` arms the second icon:** `+0x40` (the sprite to draw) becomes `+0x58` for `n == 2` (4×) and `+0x48` otherwise (2×), `+0x60` (alpha) = 255.0, `+0x64` (fade direction) = +6.0, `+0x69` (pulse) = 1 and `+0x6C` (scale) = 1.5. **The render pass `001D7280` draws it** (from the pass list `00187950`): after the save-busy branch it tests `00229DF0()` — the byte `02064AD2`, this page's `g_fastModeEnabled` — and the per-frame byte `+0x68` (`001D72B5`–`001D72C2`), then runs `001D8520`, which raises the alpha by 0.5 per frame (1.0 when the present interval `00184950()` is 2), lifts it to a 63.0 floor (`00900380`) from below and holds it at 255.0 (`008C5B40`) from above — `+0x64` receives −6 at the top and +6 at the floor and has no reader in the `ExtraUI` range — and tail-calls `001D7DD0(this, alpha)`, which draws the sprite quad at `+0x40` and, while `+0x69` is set, shrinks `+0x6C` by 0.1 (`008C5F6C`, `001D80A0`) times a frame factor until it reaches 1.0 and clears `+0x69` (`001D80B7`). `+0x68` is the visibility latch: the field frame `0022A770` sets it to 1 through `0017F740` when `00358550()` holds (the byte `022C7F9A == 0x1F`, `0022AD02`–`0022AD14`), and `0022B8C0`, `0022BC20` and the skip handler `00360120` clear it. So **what `00182FB0(n)` tells the subsystem is: show the 2× or 4× fast-forward badge at full alpha with a 1.5× pulse**, and the badge then stays at full alpha for as long as fast mode is on. The same object owns the first icon set: `001D7280` draws it through `001D72F0` with the alpha at `+0x88` (faded by `001D8240` at ±6 per frame) while `SaveWrite_GetBusyFlag` `00583920` (`[02CA99E8]`) or the save-load manager's `+0x40` byte (`001C18E0`, `001D728E`) is set — the saving indicator — and the slot-4 pump path `0017D6E0` → `001D8AB0` → `001D7A20` spins a quad for it (`001D8790` rotates four vertices about the sprite centre by `elapsed × π`, `01CEBC50`). Which atlas records the two sets resolve to (the ids at `+0x10` / `+0x20` of the `[0209AC30] + 0xA0` table) is the record table's to name and is not read here. Static: the eleven `ExtraUI` bodies and the two frame callers.
- [x] ~~Which value the `Speed2` and `Speed3` branches pass to `Present_SetSpeedField` means what:
      `0` for 2× and `1` for 4× is measured, but the field's meaning is not.~~ **Answered 2026-09-14 (FABLE):** the field
      remembers which fast speed the player last chose, `0` = 2× and `1` = 4×. Settings command `0x0E` writes the same
      field (which screen row issues it was not traced), and `0023B2E0` turns it back into speed mode 1 or 2 while fast mode is active (see
      the box above).
- [x] **UQ-143.** *(status restated in the register 2026-09-26, FABLE, Claude Opus 5.5: see the row)* What records 0 and 1 of the five-record bank at `01DF1480` are, and what the conditional
      banks at `01F80550` and `01F80970` polled by `00196FF0` hold.
      **Narrowed 2026-09-18 (FABLE): records 0 and 1 are the gamepad and the mouse profiles; the two conditional banks are alternate profiles gated by the input-mode bits.* **Record 0** is authored in the image: its sixteen group-0 codes are `19, 21, 22, 20, 23, 24, 25, 26, 17, 18, 15, 16, 14, 13, 12, 11` — every one in the pad band 11–26, in slot order Select … Square — and its `+0x40` block holds four kind-3 records `{3, 2}`, `{3, 3}`, `{3, 0}`, `{3, 1}` (pad axes 2, 3, 0, 1 onto the RX, RY, LX, LY slots) followed by twelve kind-1 records `{1, 4, 24 … 11}`; so it is **the gamepad profile**. **Record 1** ships zeroed and is built by the initialiser `0015C280`: its head is copied from the live binding array `01F800F0` and its `+0x40` block from the constant template `01DF0D80` — `{4, 2}` and `{4, 3}` in the RX and RY slots (mouse X and Y drive the right stick), `{4, 4, 3, 0}` in the Up slot and `{4, 4, 0, 3}` in the Down slot (the wheel's two directions as D-pad up and down); so it is **the mouse profile** (see UQ-144 for the kinds). The same initialiser fills records 2–4 from the keyboard templates `01DF09C0` / `01DF0A80` and `01DF0A00` / `01DF0B80` (records 2 and 3 heads `40, 79, 35, 64 …` and `114, 0, 110 …`). **The conditional banks** `01F80550` and `01F80970` hold three records each, built by `0015C0D0` and `0015BF20` from one head template `01DF0980` (`53` = `Z` at Select, `51` = `X` at R3, the rest 0) and the runtime block `01F7FFF0` for their `+0x40`; `InputManager_PollAndBuildControlState` polls the first when bit 1 of the manager byte `+0x3A` is set (`001970C8`) and the second when bit 0 or bit 2 is (`001970F8`). Those bits are toggled by six tiny setters (`00198670` sets bit 2, `00198710` clears bit 1, and so on), each marking `+0x3B` dirty, reached through the wrappers `00182CD0`–`00182DA0` from the system-stop registry paths `00225CD0` / `00225EB0` / `00227680`, the main loop, the save-load controller handler and the signal widget `002D5EB0`. What is not established: which game mode each bit stands for, and what the runtime block `01F7FFF0` carries when the banks are polled. Static: the bank bytes, the three initialisers, the poll body, the setters.*
      **NARROWED AGAIN 2026-09-25 (FABLE, Claude Opus 5.5): the three mode bits follow system-stop slots, so the two conditional banks are the battle-menu bank and the menu/cutscene-lock bank.** The setters' only callers are the per-stop-slot record builder `00227680`, a 28-way jump table on the slot (`0022773A`, table `00227CB4`), and two script verbs. Read from the arms:
      - **slot 0** sets bit 1 when options bit 3 (`002DDC30`) is clear (`002277C1`–`0022780F`). Slot 0 is the Battle
        Menu's stop, UI requests 1/4/20.
      - **slot 12** sets bit 0 (`00227AB3` → `00227B67`); it is the verb `settutorial00timestop`.
      - **slot 13** sets bit 2 (`00227B6C` → `00227BAF`); it is the full-screen menus, UI requests 2, 6, 15, 17, 18,
        19 and 22.
      - **slot 15** sets bit 2 (`002277D8`–`002277E5`); it is `002E2240`'s stop.
      - **slot 17** sets bit 0 (`00227966`–`00227975`); it is the verb `ucon`.
      - The script verbs `0x5CD` / `0x5CE` (`00341030` / `003413E0`) set and clear bit 1 directly.
      
      Slot names are from [the stop registry](../../00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md). The clears come from the stop-registry release paths `00225CD0` / `00225EB0`, the main loop, the save-load controller and the signal widget. A field transition resets the byte to `0x100`. So `01F80550` (bit 1) is polled while the Battle Menu's stop is held, and `01F80970` (bits 0 or 2) while a full-screen menu, the tutorial time stop, `ucon` or `002E2240`'s stop is held. Their heads bind `Z` to Select and `X` to R3 (above). *Still open: what the runtime block `01F7FFF0` holds in those states. The reading of the bits as "battle menu" and "menu or locked" comes from the slot names, not from a live observation.*
      **The runtime block, read 2026-09-25 (FABLE, Claude Opus 5.5).** `01F7FFF0`, the source of both conditional banks'
      `+0x40` halves (`0x100` bytes, 2 × `0x80`), lies past `.data`'s file-backed end `01F7E400`, so the image
      initialises it to **zero**. Its address is formed only by the two initialisers' `lea`s, which use it as a copy
      source (`0015BF27`, `0015C0D7`). No rip-relative store lands in `01F7FFF0`–`01F800EF`. The globals just below it
      (`01F7FFC0`–`01F7FFE0`, the last being the input-manager singleton pointer) are single qwords reached by `mov`,
      not a block whose writes could run on. An all-zero record is kind 0, which falls through every arm of the
      translator's kind dispatch (`001972A0`–`001972C1` → `00197685`), and a zero head code matches none of its
      three code ranges. **So, within that domain, the two conditional banks bind only their heads**: while the
      Battle Menu's stop or a menu / script-lock stop is held, `Z` also drives Select and `X` also drives R3. *Not
      excluded: a computed-address writer outside the sweep. Not observed live.*
- [x] **UQ-144.** What the `{kind, 4, codeA, codeB}` records at record `+0x40` mean beyond `kind == 2` being
      an axis pair and `kind == 1` a single code.
      ***ANSWERED 2026-09-18 (FABLE) — the four fields are `{kind, subKind, codeA, codeB}`, and the constant 4 is a sub-kind that only the mouse kind reads.** `InputManager_TranslateBindingProfileToControlState` (`00197160`) walks the sixteen records with `rbp` at each record's `+8` and dispatches on the kind at `[rbp−8]` (`001972A0`–`001972C1`): **kind 1** (`0019760E`) reads one control code, `codeA`, and polls it in its band; **kind 2** (`0019748E`) reads `codeA` and `codeB` (`00197494`, `00197545`) as the positive and negative halves of an axis; **kind 3** (`001973E5`) is a **gamepad analog axis** — the second field is the axis index passed to `0079D1D0(backend, axis)`, the value scaled by the sensitivity constant and doubled again by the invert bytes `[01F7FFE0]+8` (axes 2) and `+9` (axes 3) (`00197406`–`00197428`); **kind 4** is the **mouse**: with the second field 2 or 3 it is the mouse X or Y axis onto the slot, taken only while `GetForegroundWindow` (`001973DA`) and the singleton byte `+0xC35` allow; with the second field 4, `codeA` 11 / 13 / 12 are the three mouse buttons (device bytes `+0x170` / `+0x171` / `+0x172` at `001972D1`–`00197320`), and `codeA` 3 is the **wheel** — axis 3 of the device at backend `+0x150`, divided by the step constant, accumulated into `[01F7FFE0]+0xC` and stored at `+0x10` through `00196480` (`00197355`–`001973C3`). Neither the kind-1 nor the kind-2 arm reads the second field, so the `4` the keyboard templates carry there is inert for them. Static: the translate body, every arm read.*
- [x] **UQ-145.** Why `008F3160` — the full `\My Games\FINAL FANTASY XII THE ZODIAC AGE\keymap.ini` literal —
      has no recorded code reference, when the path is otherwise assembled from three separate
      segments.
      *Narrowed 2026-09-14 (FABLE), not answered: it has a data reference, and that reference (`01DF0978`) is itself unreferenced.* The UTF-16 string
      at `008F3160` is pointed to by one qword, `01DF0978` in `.data`. That slot has no RIP-relative reader or writer. Its
      neighbours are addressed separately: `00196480` reads the float at `01DF0970`, and `0015BF20` / `0015C0D0` load the
      `xmmword` at `01DF0980`, which covers `01DF0980`–`01DF098F`. No read spans `01DF0978`. Two slots below, `01DF0960`
      and `01DF0968` point to the shader paths `/GameData/D3D11/ArtData/shaders/depthmask.fx.phyre` and `…/BrightnessShader.fx.phyre`. So the full path survives as an
      initialised pointer nothing loads, consistent with the runtime building the path from three segments. A
      base-plus-index read of that table is not excluded by this scan.
      ***ANSWERED 2026-09-18 (FABLE) — the literal is dead: its only reference is an initialised pointer that no addressing mode reaches.** The two ways an x64 image can reach a `.data` slot are a rip-relative operand and a 64-bit absolute immediate. A sweep of every rip-relative operand in every listed body into the 128 bytes `01DF0940`–`01DF09BF` finds nine references, none to `01DF0978`: the four `xmmword` loads at `01DF0980`, `01DF0990`, `01DF09A0`, `01DF09B0` by each of `0015BF20` and `0015C0D0` — the head template of the two conditional profile banks (UQ-143) — and the float at `01DF0970` read by `00196480`; sixteen-byte loads from `01DF0980` upward cannot cover a slot that ends at `01DF097F`. A byte search of the whole image for the slot's absolute address as an immediate finds nothing, and for the string's absolute address finds exactly one occurrence: the slot itself. So no base-plus-index read of a table containing the slot exists either, because no instruction forms a pointer into that neighbourhood by any means. The full path survives as the compiled remnant of a `static const wchar_t*` initialiser the shipped code never consults; the path it actually opens is assembled from the three segments §2 describes. Static: the two sweeps, both with the neighbouring template loads as positive controls.*
- [x] **UQ-146.** Whether `001F3ED0` returning a pointer into its own stack frame is a live defect. The
      caller consumes it only after further calls that reuse that stack region.
      **Narrowed 2026-09-14 (FABLE): the dangling return is certain, and whether it corrupts depends only on the installed CRT.**
      - **The return.** `001F3ED0` returns `lea rax, [rsp + 0x30]` (`001F3F52`), a 510-byte buffer in its own `0x248` frame. It therefore points about `0x220` bytes below the caller's stack pointer once it has returned.
      - **The callers.** All four hand the pointer to a formatter as an argument:
        - `00197F7A` and `007981EF` pass it in `r9` to `00194EF0`;
        - `0079FA94` and `00862B38` pass it on the stack to `00408ED0`;
        - `00862B24` also reads its first character first, before any call.
      - **The image cannot clobber it.** Both formatters are thin wrappers, `0x48`–`0x58` bytes of frame, around `__stdio_common_vswprintf_s` and `__stdio_common_vswprintf` (IAT `008C2E88` / `008C2DE8`, `api-ms-win-crt-stdio-l1-1-0.dll`). No code in the image grows the stack within `0x220` bytes of the buffer before the string is read.
      - **What remains.** The only frames that can overwrite it before its `%s` is consumed are the Universal CRT formatter's own. Whether they reach that deep is a property of the installed `ucrtbase.dll`, not decidable from this executable.
      - ~~**A live check is enough.** Compare the SteamID64 folder name the game creates under `My Games` with the account's id.~~
      - ***That check has now been run, it passed, and it closed nothing — 2026-09-21 (FABLE, consuming
        `ASTRA-RETURN-FABLE-KEYMAP-EXISTING-IDENTITY`).*** ASTRA compared the existing artifacts against the live host
        profile: the account-named directory below the settings root is **`76561198045890736`**, matching the observed
        profile on three independent keys — the registry `ActiveUser` low 32, the account-name hash, and a **uniquely**
        selected `loginusers.vdf` record — and the root `keymap.ini` and the account folder's `keymap.ini` are both
        **699 bytes** with SHA-256 `8d98f85e0b571d819dc155c8774aad553f6e6119d6ede1cdd62245cfb9f6cf6d`, both matching
        their entries in the retained `old-save-start-p` capture. *(Artifact reading only, at
        `2026-09-21T09:24:31Z`, Steam PID 54064, client `10.96.30.42`, with before/after identity brackets; **host
        metadata, not `ISteamUser::GetSteamID` called by FF12**. No game process, game API call, formatter execution or
        returned-pointer access was observed.)*
      - **Why the pass settles nothing, which is the part I got wrong.** A matching folder is produced by a correct
        formatter call, by an **older or copied artifact**, or by a startup that behaved differently from the one that
        would run now — the file timestamps predate the observation and name no writer and no build. **And the converse
        fails too:** an *empty* account component could not have indicted the stack either, because §8's evidence
        table already carries the uninitialised-Steam path that writes an empty string — the
        `if (*(void **)(ctx + 8) != NULL)` guard over a `memset`-zeroed buffer. **Both outcomes of the test I proposed
        are compatible with both answers**, so it was never a test of this question. *A folder name is an endpoint, and
        this one has many causes.*
      - **What would discriminate**, and it is not a folder comparison: bounded execution of the verified original
        caller/formatter path — `001F3ED0` into `00194EF0` or `00408ED0` — **with the relevant `ucrtbase` and an
        explicit stack and input state**, observing whether the returned buffer still holds its string at the point the
        `%s` is consumed. That is the only place the question lives, because the bullet above already shows the image
        itself cannot clobber it. Until then `UQ-146` stays open on the CRT dependence, exactly as the narrowing left it.

      - ***The state that test has to be run in is now fixed, and it was the thing that was missing — 2026-09-21
        (FABLE, consuming `ASTRA-RETURN-FABLE-UQ146-ORIGINAL-CRT` and
        `ASTRA-RETURN-FABLE-UQ146-PRINTF-INITIALIZER`).*** ASTRA ran the bounded execution this row asks for against a
        host `ucrtbase` and reported that the 17- and 20-digit supplied strings came through intact **with the printf
        options word set to 4**, and *not* with it set to 0 — so the CRT's identity alone was not enough state to
        reproduce the game's formatter, and the options word was the missing precondition. **Which value FF12 actually
        passes is decidable from this image, and it is `4`.**
        - The qword is zero-initialised and its accessor `0016D670` (`__local_stdio_printf_options`, named on
          [the formatted log call](../../00-Engine-Core-Runtime/Diagnostics-Logging/the-formatted-log-call-and-its-level-gate.md))
          is its **only** rip-relative reference in the image. Of that accessor's 23 call sites, **exactly one writes
          through the returned pointer** — the C initializer `00809C50`, run by `_initterm_e` before the C++ walk and
          before game entry, which does `or qword ptr [rax], 4`. The other 22, `00194EF0` on this page's own path
          among them, load the value and pass it on.
        - So the formatter on the dangling-pointer path is called with options `4`, fixed from C-initializer time, and
          nothing in the image changes it afterwards. **A future run of the discriminating test has no freedom left in
          that argument**, and a run that used `0` was testing a formatter this game never invokes.
        - *What this does not do.* It fixes one input to the test; it does not run it. ASTRA's strings were **supplied**
          at a stage boundary rather than produced by `001F3ED0`, no FF12 process, Steam API call or returned-pointer
          access was observed, and the dangling return's lifetime is untouched. `UQ-146` stays open on exactly the
          clause above — whether `ucrtbase`'s own frames reach the buffer before the `%s` is consumed.
      - ***SUPERSEDED 2026-09-27 (FABLE, Claude Opus 5.5) under the runtime rule; the live half is carried by
        `FABLE-REQ-ASTRA-UQ146-IN-PROCESS-FORMATTER-READ`.*** The static claim is complete and tier 1: the return
        dangles (`001F3F52`); no code in the image grows the stack into the buffer before its `%s` is read; and the
        formatter runs with printf options `4`, fixed at C-initializer time. What remains is a property of the
        installed `ucrtbase.dll`, not of this executable, and only an in-process observation can settle it. ASTRA's
        host-CRT run with options `4` consumed the supplied strings intact; it did not observe the game's own path.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Path is `<Documents>\My Games\FINAL FANTASY XII THE ZODIAC AGE\<SteamID64>\keymap.ini`, directories created as built | complete body of `00197EE0`: `SHGetFolderPathW(…,5,…)`, the three wide literals, `_waccess`/`_wmkdir` in `001F3EA0`, `%llu` of `ISteamUser::GetSteamID` in `001F3ED0` | 1 |
| The id component is empty when Steam is not initialised | the `if (*(void **)(ctx + 8) != NULL)` guard in `001F3ED0` over a `memset`-zeroed buffer | 1 |
| Reader and writer use the same path buffer | `DumpDataXrefs.java` on `01F80D90`: three sites — `00197FCC` (build), `001980F3` (read), `001994AB` (write) | 1 |
| File is ASCII with LF terminators, 87 lines | the writer emits `L"\n"` (`008F3980` = `0A 00 00 00`); the file on disk is 699 bytes / 87 lines, first bytes `5b 4b 65 79 62 6f 61 72 64 31 5d 0a` | 1 + 10 |
| Grammar: blank skipped, `[…Keyboard<n>]` section, `name=number`, anything else stops the load | complete disassembly of `00198000` `0x198210`–`0x198525`: `je 0x198515` (continue) on `len == 0`; `je 0x198546` (close) on a missing `]` or `=` | 1 |
| `line[0]` is not checked | `lea rcx,[rbp+0xa2]` (= line + 1 wchar) with `r8d = 8` into `wcsncmp` at `0019824C` | 1 |
| Section index is `wcstol(...) - 1` and never bounds-checked | `dec edi` at `0019834A`; `movsxd rax, edi` / `imul r14, rax, 0x70` at `001984B8`; `edi` initialised `-1` at `001981EA` | 1 |
| Name index == slot index; three groups of 16/8/4; group bases `01F80F90`/`01F80FD0`/`01F80FF0` | the parser's paired increments at `0x1984D0`–`0x1984F9` (`rdi += 8`, `rbx += 4`) and the identical pairing in the writer `001993B0` | 1 |
| The 28 names and their order | raw read of the three pointer tables at `01DF11E0`, `01DF1260`, `01DF12E0` | 1 |
| Slot 13 = `Circle`, slot 14 = `Cross` | name table index 13/14, plus the shipped file's line order: `Circle` is the 14th line of `[Keyboard1]` | 1 + 10 |
| **The pair swap exchanges `Circle` and `Cross`** | `00195F0C`–`00195F2B` exchanges record `+0x34` / `+0x38`; the preceding `movups [rdi-0x48]…[rdi-0x18]` copy is 1:1, so those are dwords 13 and 14 | 1 |
| The swap is keyed on `DecideButton` | `001DFA70` is `CMP [RCX+0x64],0 / SETZ AL / RET`; `rcx` is `01F82D20` loaded at `00195E42`; `+0x64` is settings index 25, value names `{Circle, Cross}` | 1 |
| A second, independent site indexes the same pair on the same flag | `001967D0`: `FUN_0022a540()` then `01DF1738 + (0xD + (flag != 0)) * 4` | 1 |
| The confirm/cancel masks the same setting swaps are bits 13 and 14 | complete body of `0022A4F0` re-derived here: `01E0C2A0 = 0x2000`, `01E0C2A4 = 0x4000` when the field is 0, exchanged otherwise; `0022A540` is `return DAT_01FD4A64 == 0`. `0x2000` = bit 13, `0x4000` = bit 14 — the same indices as the swapped slots. Which mask is confirm is established in the neighbour document from `002778C0` | 1 |
| Shipped defaults, all 84 values | raw read of `01DF09C0` (3 × 0x40), the `codeA`/`codeB` fields of records 0–3 at `01DF0A80`, and `01DF1470` (16 B) | 1 |
| The shipped defaults are what a player's file contains | the keymap.ini on disk matches all 84 values exactly, including the zeros | 10 |
| Group 2 defaults reach profile 1 only | `movups xmmword ptr [rip -> 01F80FF0], xmm0` at `00198E5A`, **after** the loop exit at `00198E39` | 1 |
| Keyboard codes are `PInputKeySemantic - 1` | the enum member run at `01F45700` is contiguous `123 … 29` over 95 records of 32 bytes (`(0x1F462C0 - 0x1F45700)/32 = 94 = 123 - 29`); subtracting 1 makes the shipped defaults resolve to W A S D, the four arrow keys, I J K L, F1–F3, Left Shift and Space — 28 of 28 | 4 + 1 |
| Validator semantics (0 = clean; profile 1 only; scan bound `0x53`) | complete bodies of `00196550` and `001965E0`; `r11` fixed at `01F80F94` across the outer loop at `00196600` | 1 |
| `00195DF0` publishes and `00198B60` installs defaults | their read sets (`01F80F90` vs `01DF09C0`/`01DF0A80`/`01DF1470`) and write sets from `DumpDataXrefs.java`; plus `001E0F70` calling Materialize **then** Restore, and `001E1050` calling Restore alone after an assignment | 1 |
| `L2`/`R2` are zeroed in the record | `mov qword ptr [rsi+r15+0x1cd1758], r13` at `00195E86` with `r13 = 0`; the same store in `00198B60` | 1 |
| `Mouse1..3` exist but are never iterated | the table at `01DF1360`; both loops bounded at three groups (`cmp r15d, 3` at `00198502`; `iVar5 < 3` in `001993B0`). Positive control: group 2 *is* reached, so the bound is real | 1 |
| The reserved-id list | raw read of `01DF13E0`, 35 dwords, and the loop bound `< 0x1DF146C` in `00196550` | 1 |
| `[Button]`/`[Setting]`/`[Mouse]` are not this binary's format | a byte scan for those literals (ASCII and UTF-16) returns zero, in the same run in which `[Keyboard` returns a hit at `008F3988` | 1 |
| `FUN_00197710` is the only reader that reaches group 2 **as a binding** — the uniqueness validator and the writer read those dwords too (§10) | `DumpDataXrefs.java` on `01F80FF0`: 7 references — 1 write (`00198E5A`, Materialize), 4 `LEA`s in the writer/assigner/parser, and one indexed read, `MOV EAX,[RAX+RDX*4+0x60]` at `0019773B`. `01F80FF4/F8/FC` have **no** references at all. Cross-checked against `01F80F90`'s own reference list, which is closed at nine functions, all `Input`, all accounted for | 1 |
| `L2`/`R2` are read by two dedicated predicates, not by the mask | complete bodies of `0017DDC0` and `0017DE10`: `GetBinding(mgr, 0, 0, 8)` and `(…, 0, 0, 9)` into `IsControlCode28To283ActiveForBank(be, code, 0)` | 1 |
| `Speed1/2/3` drive `SetSpeedMode(1/2/4)`, edge-latched | complete body of `0017DEA0`; latch `01F7F4E9` | 1 |
| The speed table is `{1.0f, 2.0f, 4.0f}` and is indexed by the mode | raw read of `0x00908BA8` (`.rdata`); the main-loop store `g_speedScalar = speedTable[01FD4A98]` at `0022AAAF`/`0022AAB6`; `GameSpeed_GetMultiplier` (`00229E00`) is the same expression in 20 bytes | 1 |
| Pressing the same speed key again turns it off | disassembly of `00239790`: `cmp eax, ebx / je reset` on the 4× branch and `cmp eax, 1 / je reset` on the 2× branch | 1 |
| `WalkMode` is a **toggle**, not a hold | complete body of `003594E0`: `if (!edge) g_walk = (g_walk == 0); edge = 1;` on the rising edge only | 1 |
| **`DAT_01DFE0B8` is the `FrameLimit` time base, not the speed-mode scalar** | its sole writer is `FUN_001eddc0`, on the branch selected by `GameSetting[+0x48]` (`FUN_0017d8f0` is `return *(u32 *)(01F82D20 + 0x48)`); the GameSetting key table at `01DFD050` index 18 is `FrameLimit` and its value-name row is literally **`{"30", "60"}`**, default `0` = 30. Access-role census, this session: `01DFE0B4` 211 R / **1 W**, `01DFE0B8` 46 R / **1 W**, `01DFE0BC` 182 R / **1 W** — all three writes inside `001EDDC0` | 1 |
| The three frame-base constants and their two settings | raw read: shipped `01DFE0B4 = 1`, `01DFE0B8 = 1.0f`, `01DFE0BC = 1.0f`; the writer stores `2`, `01CEBC08 = 2.0f`, `01CEBB70 = 0.5f` | 1 |
| The GameSetting key and value-name tables | **re-derived here** from `01DFD050` / `01DFD150` / `00900CE0`, independently of the 19-Save-Load-Settings document, and agreeing with it on all 31 keys and on rows 18 and 25 | 1 |
| Body extents | `DumpFullCoverageGraph.java` at the GN158 checkpoint (`functions.tsv`) | 1 |

**Instrument notes, recorded because both nearly produced a wrong answer:**

- A `.text` linear sweep for RIP-relative references to these globals returned **0 hits** for
  every target, including `01DF11E0`, which is provably referenced at `0019847F`. Linear sweep
  desynchronises on inline data and never resynchronised. The counts in this document come from
  `DumpDataXrefs.java` instead. A zero from that sweep was not evidence of anything.
- The first disassembly helper was written to a file named `dis.py`, which shadows the standard
  library's `dis` module that `capstone` imports transitively. It raised, **and still printed
  partially correct output** — the exact shape of a plausible result from a broken instrument.

**Superseded readings:** none — this is the document's first version.

**Correction to this paragraph, 2026-09-03 (§11 pass on the neighbour).** It originally said the
neighbouring [binding profiles](binding-profiles-remapping-and-control-state.md) document *"lists
the keymap file format as unread and calls `01DF1738` a staging buffer"*. **The second half was
already stale when written here**: that document's §3 and §8 say explicitly that `01DF1738` is
**not** a staging buffer and give the same `01DF1480 + 2 × 0x15C` arithmetic. The document still
carrying "staging" is
[`../Input-Stack/input-stack-device-channel-and-bindings.md`](../Input-Stack/input-stack-device-channel-and-bindings.md)
§11, as the Related list below says. The first half — the file format listed as unread — was true
and is now closed by this document.

## 9. Related

- [`binding-profiles-remapping-and-control-state.md`](binding-profiles-remapping-and-control-state.md) — the in-memory binding array, the conflict-swap assigner and the per-frame control mask; **this document supplies the file format it says it does not cover, and identifies the swapped pair**
- [`../Input-Stack/input-stack-device-channel-and-bindings.md`](../Input-Stack/input-stack-device-channel-and-bindings.md) — the device/channel layer; its §11 calls `01DF15DC`/`01DF1738` a staging cluster, corrected here
- [`../Gameplay-Capability-Policy/capability-inhibition-policy.md`](../Gameplay-Capability-Policy/capability-inhibition-policy.md) — whether an intent is permitted, as opposed to bound
- [`../../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md`](../../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md) — `GameSetting.ini` and the `DecideButton` slot that drives the Circle/Cross exchange
- [`../../19-Save-Load-Settings/Language-And-Locale/language-selection-and-locale-ids.md`](../../19-Save-Load-Settings/Language-And-Locale/language-selection-and-locale-ids.md) — the `0x2000`/`0x4000` confirm/cancel masks written from the same setting
- [`../../22-Middleware-PhyreEngine/`](../../22-Middleware-PhyreEngine/) — `PInputKeySemantic` and the reflection member tables the key names come from
- [`../../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md`](../../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md) — carries **Z-10**, which §2 and §8 answer in the negative: `01DFE0B8` is the `FrameLimit` 30/60 base, and the 2×/4× scalar is `02064AC4`
- [`../../06-Movement-And-Navigation/heading-speed-to-position-delta.md`](../../06-Movement-And-Navigation/heading-speed-to-position-delta.md) — carries **K-8**; `01DFE0BC` has exactly one writer and is `0.5` when `FrameLimit = 60`
- [`../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md`](../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md) — its `ticks / (int)(DAT_01DFE0B8 * 30.0)` seconds conversion is what makes the frame-base reading concrete
- [`../../11-Party/`](../../11-Party/) — `PartyControl_BuildAnalogMovementVectorFromInputHistory` and `PartyControl_ComputeAnalogMovementScale`, the `WalkMode` consumers

## Audit dispositions (repos-2d, 2026-09-03)

`audit_crossrefs.py` against `Tools/work/graph_gn` reported **1 GHOST ADDRESS** and **6
UNACCOUNTED NEIGHBOUR** findings for this document.

### GHOST ADDRESS `01DF1470` — a real presentation defect, now fixed

The finding is correct and the document's *content* was not wrong: `01DF1470` really is the
shipped group-2 default block, really is 16 bytes, and really holds `65, 66, 67, 118`. The defect
is that its row in the **data** table wrote the size as a bare `16 B` in the third column — the
same column and the same shape the function table uses for a body extent. The checker reads that
as "this document says `01DF1470` is a function with a 16-byte body", which is a false claim about
the binary, and is exactly what the template warns a data row must not make.

Every sibling row in the same table already avoids this by writing the shape first —
`` `u32[35]`, 140 B ``, `3 × 0x40 B`, `5 × `0x15C` B`. This row now matches that convention. **The
fix is to the presentation, not to the finding**: the row was formatted like a function and is now
formatted like data.

### Two large host functions account for fifteen of the sixteen neighbour edges

**`0022A770` (Core runtime scheduling, 2,001 B)** is cited here for its role in the input/settings
path. It is a host frame routine, and the flagged edges are its own callees: **Presentation**
(11 edges — `0022B0B0`, `0036F2C0`, `003323D0`, `0037D4C0` and seven more), **Audio**
(`0036F460`), **Resource** (`00324510`) and **Platform/Online/Achievements** (`00316930`). That is
what a frame routine calls. *Irrelevant to the keymap format, cited for a different edge.*

**`002778C0` `BattleMenu_UpdateCommandSelectionAndDispatch` (UI, 9,374 B)** is cited for the
DecideButton work. The flagged edges are its own callees: **Audio** (`00249C60`) and **Combat
Action** (`00311B20` `BattleUnit_IssueCommandByFocusHandlesWithOptionalPartyFanout`, `00311CD0`).
A battle menu issuing commands and playing sounds is that document's subject, not this one's.
*Irrelevant here, with the reason stated.*

**`00358A20` `PartyControl_ComputeAnalogMovementScale` → the packed-actor-handle resolver
(Actor/Entity)** — the analog-scale function resolves an actor handle, which is how it reaches the
unit it is scaling movement for. A one-edge Actor/Entity dependency of a function cited here for its
analog reading. *Explained, not a keymap relationship.*

**The resolver is deliberately named and not cited by address.** It has **180 callers across 11
owner subsystems** — more than any of the three hubs `cross-subsystem-accessor-hubs.md`
enumerates — so citing its address in a one-line aside would import a census this document has no
business explaining, and the first pass of this very disposition did exactly that (it drew fresh
`CombatFormula` and `World` findings through `BattleStats_ResolveByActorHandle` and two unowned
callers). The claim does not need the hex; the hex would need a census.

### The Steam account id — already explained, but never named as a subsystem

`00197EE0` `InputManager_BuildKeymapPath` → `001F3ED0` (159 B), whose own callers are `0079FA00`
and `00862A40`. All three carry the ledger owner **`PlatformOnlineAchievements`** — the Steam
integration layer. §2 of this document already
explains this in prose — *"the account-id component comes from `FUN_001f3ed0`, which asks Steam for
the current user's 64-bit id and formats it with `%llu`"*, guarded by `if (steamUser != NULL)`. The
relationship was documented; only the subsystem's name was missing, so the audit could not see it.

**That is worth stating as a caution rather than quietly fixing:** a document can explain a
relationship correctly, in the ledger's own vocabulary, and still be reported as ignoring it. The
correct response is to name the subsystem *because the relationship is real* — never to insert a
keyword the document has not earned.

## 10. Falsification pass 2026-09-03 (repos-2d)

Run against snapshot `46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2`,
parent `2ed8affb…`, embedded EXE `73461d08…`.

**Why this document, and a disclosure.** This session used it twice as a *source* — the binding
lookup that identified R2 for
[the R2 toggle](../Modal-Toggles/r2-force-fight-toggle.md), and its *"the name's index is the
slot's index"* rule. One part was verified at the time (`00197710`'s body) and **the rest was
accepted**. This pass attacks the parts that were accepted, first.

### SURVIVED — "name index == slot index", re-derived from the parser

This is the load-bearing claim: it is what lets a *name* in the file identify a *slot*, and it is
what this session relied on to say group 0 slot 9 is `R2`. §8 cites the paired increments; the
whole loop was re-read, and it proves more than the increments alone:

```asm
0019847C  mov  r15d, esi           ; group counter := 0, executed ONCE on entry
00198486  <dispatch on r15d>       ; <- the loop-back target
   group 0 -> rax = 01F80F90 ; group 1 -> 01F80FD0 ; group 2 -> 01F80FF0
0019849B  imul r14, rax, 0x70      ; profileIndex * 0x70
001984C6  add  r14, rax
001984C9  mov  rbx, r14            ; slot pointer, index 0 of this profile+group
001984CC  mov  rdi, r13            ; name pointer, index 0 of this group
001984D0  mov  rdx, [rdi]          ; the name; NULL ends the group
001984E9  mov  [rbx], r12d         ; on _wcsicmp match: write the code
001984EE  add  rdi, 8              ; next name
001984F2  add  rbx, 4              ; next slot
001984F6  cmp  esi, 0x10           ; bounded at 16 for every group
001984FB  inc  r15d                ; next group
001984FE  sub  r13, -0x80          ; next name table (+0x80)
0019850A  mov  esi, 0              ; <- slot counter reset PER GROUP
0019850F  jl   0x198486            ; back to the dispatch, NOT to 0019847C
```

Two things the increments alone do not establish, both true: **the slot counter is explicitly
reset to zero for every group** (`mov esi, 0` at `0019850A`), and **the loop-back target skips the
group-counter initialisation** (`0x198486`, not `0x19847C`), so `mov r15d, esi` runs only once,
when `esi` is 0. Both pointers therefore start at index 0 in every group and advance one entry per
iteration. **Name index is slot index, proven, not inferred.**

*Not broken. The use this session made of it was sound.*

### SURVIVED — profiles 2 and 3 are range-checked by nothing

The document's most consequential claim about a defect in the shipped game. Re-derived from
`001965E0`: `r11` is loaded once with `01F80F94` at `001965EB`, the outer pass re-executes
`mov rax, r11` at `00196602`, and `r11` is never modified. All three passes scan the same 28
dwords from `01F80F90`. The `sub r9, rbx / jne` at `0019666E` gives exactly three passes.

The document's pseudocode also collapses two *different* encodings of the same bound —
`(unsigned)(v - 1) > 0x97` on the first slot of each unrolled group of four, and
`v <= 0 || v >= 0x99` on the other three. They are equivalent (`v < 1 || v > 152`), and collapsing
them is correct rather than sloppy.

*Not broken.*

### SURVIVED — the uniqueness validator, instruction for instruction

§4's pseudocode matches `00196550` exactly, including the two details easiest to get wrong: the
`test ecx, ecx / je` that **excludes 0 from duplicate detection**, and the inner scan running to
`01F810E0`, the end of the **whole 84-dword array**, so a duplicate is rejected across profile
boundaries. That is what makes §1's *"one key may only mean one thing across all three layouts"*
true.

### SURVIVED — three absence claims, on an instrument with a working control

The document itself records that a linear `.text` sweep failed here, missing `01DF11E0`'s
reference at `0019847F`. This pass used a per-function-entry sweep, which resynchronises at every
function, and **the control fires**: `01DF11E0` is found at `0019847F` and `0019956D`.

| Absence claim | Result |
|---|---|
| `008F3160` (the composed path literal) has no code reference | **0 references** — survives |
| `01F80FF4` / `F8` / `FC` have no references | **0 references** — survives |
| `[Button]` / `[Setting]` / `[Mouse]` are not this format | **0 hits** ASCII and UTF-16, while `[Keyboard` returns exactly the cited hit at `008F3988` — survives |

`Keyboard1` as a whole literal also returns 0, which independently corroborates §2's account of the
writer *composing* the section header from `L"[Keyboard"`, the number and `L"]"` rather than
storing it.

### SURVIVED — the caller counts, now checked against the thunk route

The counts had never been checked against thunks or tail calls — the defect that produced two wrong
answers elsewhere in this database. A `call`/`jmp rel32` instruction census, with
`FieldData_GetActiveFieldRecordBit15` as a positive control (80 sites / 66 distinct, matching its
own document):

| Function | Document | Thunks | Instruction census | Verdict |
|---|---|---:|---|---|
| `00197710` `GetBinding` | "its six callers" | 0 | 8 sites / **6 distinct** | survives |
| `0017DDC0` `IsL2Held` | only reader of slot 8 | 0 | 1 site / 1 caller | survives |
| `0017DE10` `IsR2Held` | only reader of slot 9 | 0 | 1 site / 1 caller | survives |
| `0017DFC0` `IsWalkModeKeyHeld` | — | 0 | 1 site / 1 caller | survives |

### CORRECTED — "10 call sites" is 10 callers and 15 sites

§3 lists `001E0BD0` `InputConfig_GetBinding` as *"generic `(profile, group, slot)` getter, **10 call
sites**"*. The graph gives 10 **distinct callers**; the instruction census gives **15 call sites**,
because `002B5C90` calls it **six times** and the other nine call it once each.

Both numbers are right about different populations, and the document states the one it did not
measure. This is the edge-count-versus-call-site confusion the evidence standard already carries a
rule for; it is recorded here rather than quietly amended, and the row now reads *"10 distinct
callers, 15 call sites"*.

### CORRECTED — "the only reader that reaches group 2" is true only of binding getters

§3 and §8 say `00197710` is *"the only reader that reaches group 2"*. As literally worded that is
false, and **this document's own §4 is the evidence**: `InputManager_ValidateBindingUniqueness`
reads all **84** dwords — group 2 included — and the writer reads them to emit them.

The intended sense is right and is what §8's evidence actually enumerates ("1 write, 4 `LEA`s … and
one **indexed read**"): `00197710` is the only function that reads a group-2 slot **as a binding**,
i.e. the only path by which a group-2 key can reach a consumer. The wording is now qualified in
both places.

**Why this mattered enough to chase:** group 2 is reached as `01F80F90 + 0x60`, *not* by referencing
`01F80FF0`. A second group-2 reader would therefore be invisible to the very test §8 cites. The
check that closes it is the base's own reference list — 8 sites across 6 functions
(`00195060`, `00196550`, `00197710`, `00198000`, `00198A00`, `001993B0`), all Input, each accounted
for above. No seventh reader exists.

### Population note, not a defect

§8 reports **7** references to `01F80FF0` from `DumpDataXrefs.java`; a rip-relative operand sweep
finds **5** (4 `LEA`s + 1 `movups` write). The difference is the two computed accesses Ghidra
resolves to the symbol, including `MOV EAX,[RAX+RDX*4+0x60]` at `0019773B`, which is not a
reference to `01F80FF0` in the encoding at all. **Both counts are correct for their instrument.**
Recorded so a later reader does not "fix" one to match the other.

### Physical verification

`verify_doc_addresses.py` at the GN158 checkpoint: all cited addresses resolve, no `GHOST ADDRESS`,
no `BODY DRIFT`. `audit_crossrefs.py`: 0 findings. `check_links.py`: all relative links resolve.

### What was not attacked

- The tier-10 claims that rest on the `keymap.ini` on this machine (the 699-byte / 87-line file and
  the 84 shipped values matching it) were not re-read from disk this pass.
- `PInputKeySemantic`'s 95-record enum run at `01F45700` was taken as given from the RTTI/reflection
  work rather than re-parsed.
- The `Speed1/2/3` and `WalkMode` consumer chains were spot-checked only where they touch the
  binding tables.

### Status after this pass

`audit.passes` goes 0 → 1 and the pass is recorded above against a named program state, satisfying
criteria 7-9 of the `AUDITED` bar (pass recorded; `audit_crossrefs` clean; every cross-subsystem
neighbour dispositioned). **The status stayed `DOCUMENTED` after this pass**, because criterion 10 — *every* claim has a
stated killer that was searched for and not found — was not met: the three areas listed under
*What was not attacked* had not been given one.

**Closed by pass 2 (§11), 2026-09-03**, which attacked all three. Status is now `AUDITED`; §11
states the residual coverage plainly.

## 11. Falsification pass 2, 2026-09-03 (repos-2d) — closing the gap named in §10

Same program state. This pass exists to attack the three areas §10 listed as **not attacked**, which
is the condition §10 itself set for `AUDITED`. All three survive; nothing was overturned.

### The tier-10 rows: the file on disk

**Two copies exist**, and their locations are themselves evidence:

```
<Documents>\My Games\FINAL FANTASY XII THE ZODIAC AGE\keymap.ini                    699 B
<Documents>\My Games\FINAL FANTASY XII THE ZODIAC AGE\76561198045890736\keymap.ini  699 B
```

They are **byte-identical**. §2 says the path carries a `<SteamID64>` component and §8 says *"the id
component is empty when Steam is not initialised"*. ~~The two files are that claim observed from
disk: the same build wrote the same content to both the with-id and the without-id path.~~ **A
tier-1 guard corroborated at tier 10 by an artefact nobody planted.**

> **The struck sentence claims a writer the artefacts cannot name — corrected 2026-09-21 (FABLE, on
> `ASTRA-RETURN-FABLE-KEYMAP-EXISTING-IDENTITY`).** What is observed is **two identical files at those two
> paths**. *A copy produces exactly that*, and so does one build writing twice at different Steam-init
> states, and so does an older artefact left by a build that is not the one installed now — the file
> timestamps predate every observation of them and identify no writer and no build. **"Nobody planted it"
> is not "the game wrote it here, this way, for this reason".** The tier-1 guard in `001F3ED0` stands on
> its own static reading and does not need this corroboration; what §11 legitimately adds is that the
> on-disk content matches the format the writer emits, which the measured table below is. *(ASTRA
> re-read both files on 2026-09-21: still 699 bytes, still one SHA-256,
> `8d98f85e0b571d819dc155c8774aad553f6e6119d6ede1cdd62245cfb9f6cf6d`, and the account folder matches the
> live host profile on three independent keys — see `UQ-146` in §7.)*

| Claim | Measured |
|---|---|
| 699 bytes | **699** |
| 87 lines | **87** |
| LF, not CRLF | **0** `0x0D` bytes in the file |
| first bytes `5b 4b 65 79 62 6f 61 72 64 31 5d 0a` | identical |
| `Circle` is the 14th line of `[Keyboard1]` | 14th ✓ (slot index 13) |
| all 84 shipped values match the image defaults | **0 mismatches** |

The 84-value check was run three-way — the file, the image tables (`01DF09C0` group 0,
`01DF0A80` records 0-3 for group 1, `01DF1470` group 2) and §4's decoded table — including the
zeros and profile 3's `Circle = 1` / `Cross = 3`. The `{kind, 4, codeA, codeB}` record layout is
confirmed: records 0-3 read `(2, 4, 92, 91)`, `(2, 4, 94, 93)`, `(2, 4, 31, 28)`, `(2, 4, 46, 50)`.

**Testability note.** This check only works because the file on this machine is unmodified. Had the
player rebound anything, the claim would have become *untestable here*, not false — worth knowing
before someone re-runs it on a different machine and reports a defect.

### `PInputKeySemantic`, re-parsed rather than inherited

§8 carried this at tier 4+1 from the reflection work. Re-parsed from the image: the record is
`{u64 value, u64 typeRef, u64 namePtr, u64 0}` — **95 records at `01F45700`, values 123 down to 29,
strictly descending by one**, exactly the arithmetic §8 states.

Resolving the 28 shipped profile-1 codes through `PInputKeySemantic - 1` gives **28 of 28**, and
every name matches §4's decode: `Key_M`, `Key_Tab`, `Key_H`, `Key_Escape`, `Key_I`, `Key_L`,
`Key_K`, `Key_J`, `Key_2`, `Key_Left_Control`, `Key_1`, `Key_3`, `Key_R`, `Key_Space`, `Key_C`,
`Key_F`, the four arrows, `Key_D`/`Key_A`/`Key_S`/`Key_W`, `Key_F1`-`Key_F3`, `Key_Left_Shift`.

**The control is the part worth recording.** Resolving the codes *without* the `-1` still hits
**27 of 28** — so a coverage-based test could not have distinguished the two hypotheses. What
separates them is the semantic fit:

| slot | code | `code + 1` | `code` |
|---|---:|---|---|
| `LX_N` (left) | 28 | **`Key_A`** | *(nothing)* |
| `LX_P` (right) | 31 | **`Key_D`** | `Key_C` |
| `LY_N` (forward) | 50 | **`Key_W`** | `Key_V` |
| `LY_P` (back) | 46 | **`Key_S`** | `Key_R` |

One hypothesis yields WASD; the other yields `C`, `V`, `R` and a hole. §4's worked check was the
right discriminator, and it is now shown to be the *only* one available — the hit count is not.

### The `Speed` and `WalkMode` chains, end to end

| Claim | Result |
|---|---|
| speed table `{1.0f, 2.0f, 4.0f}` at `00908BA8` | raw read: **`(1.0, 2.0, 4.0)`** |
| `Speed1/2/3` → `SetSpeedMode(1/2/4)` | `0017DEA0` reads `GetBinding(0, 2, 0/1/2)` and calls `00239790` with `ecx` = **1, 2, 4** |
| edge-latched on one shared latch | all three paths test and set `01F7F4E9` before calling |
| pressing the same key again turns it off | `00239790`: `cmp eax, 1 / je` on the 2x branch, `cmp eax, ebx(=2) / je` on the 4x branch — exact |
| `WalkMode` is a toggle | `003594E0`: `sete al` on `g_walk == 0` then `mov [022C800C], eax`, guarded by latch `022C7FF9`, set to 1 after — the rising edge only |

The mode encoding is worth stating because two numbering schemes meet here: the **argument** is
1/2/4 while `g_speedMode` holds **0/1/2**, the index into the three-float table. The comparisons in
`00239790` are against the index, which is why they read `1` and `2` rather than `2` and `4`.

### Four more rows attacked while in the neighbourhood

- `001DFA70` — `cmp dword [rcx+0x64], 0 / sete al / ret`, 8 bytes. Exact.
- `0022A4F0` — `ax = 0x4000`, `cx = 0x2000`, exchanged by paired `cmove` when the flag is 0, then
  stored to `01E0C2A0` / `01E0C2A4`, with the flag cached to `01FD4A64`. Exact.
- `01DF13E0` — the reserved list is **exactly 35 dwords** to `01DF146C`:
  `2, 81, 82, 84, 85, 88, 89, 90, 123, 119, 122, 130, 125, 131…152`.
- The frame-base rows — shipped `01DFE0B4 = 1`, `01DFE0B8 = 1.0f`, `01DFE0BC = 1.0f`; writer
  constants `01CEBC08 = 2.0f`, `01CEBB70 = 0.5f`; and **all three stores are inside `001EDDC0`**,
  on the `ecx != 0` branch (`movss`, `movss`, `mov …, 2`). This is the claim carrying **Z-10** and
  **K-8** in two other documents, and it holds.
- `00197EE0` — the path builder: one import call, then three `Format_VSwprintfS` →
  `Path_CreateDirectoryIfMissing` pairs, then `001F3ED0` for the Steam id. Structure exact.

### A second population note

§8's access-role census gives `01DFE0B8` **46 reads / 1 write**; a rip-relative operand sweep finds
**46 sites total** (45 reads + the `movss` write at `001EDDD8`). The same sweep matches §8 exactly
on the other two — `01DFE0B4` 212 = 211 + 1, `01DFE0BC` 183 = 182 + 1 — so this is a **single-site
instrument difference on one global**, not a systematic one, and the load-bearing part (one writer,
inside `001EDDC0`) is confirmed by reading the function. Recorded like the `01F80FF0` note in §10:
two instruments, both correct for what they count.

### Coverage, stated plainly

Directly re-derived across the two passes: the name-index rule, the two validators, the group-2
reader closure, three absence claims, four caller counts, the on-disk file and all 84 defaults,
`PInputKeySemantic` and the 28 key names, the speed table and both speed chains, the walk toggle,
the swap predicate, the confirm/cancel masks, the reserved list, the frame-base globals and their
sole writer, and the path builder — plus the physical checks.

**Not directly re-derived**, and corroborated only indirectly: the parser's two grammar
micro-claims (`line[0]` unchecked; `wcstol(...) - 1`), the writer's emission loop, and the
publishers' read/write sets. All three are observed *through their output* — the 87-line file with
its exact section order and 84 matching values is what those three produce — but none was read
instruction by instruction in either pass.

**Status → `AUDITED`.** Criteria 7-9 were met at pass 1; criterion 10's gap was the three areas
§10 named, and they are closed. The three rows above are named so the next reader knows exactly
where the remaining thinness is rather than inheriting a clean stamp.

## The `00182FB0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00182FB0` (~50 B) — `001D8210()` resolves, then tail-forwards `(result,
ecx)` (`00182FB8`/`00182FC2`).

| member | role | interior |
| --- | --- | --- |
| `001D85C0` | profile defaults — `+0x64 = 6.0f`, `+0x60 = 255.0f`, `+0x69 = 1`, `+0x6C = 1.5f`; `edx - 1` switch (`001D85C0`/`001D85D9`) | [`001D85C0`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `001D8210`.

## SWE2-EC7-36 update (2026-09-19) - `0015C280`

`0015C280` (644 B) is the call-free keymap block copier - 0x80-stride `movups` loop copying `[rcx]` rows into the `01DF09C0`/`01DF15EC`/`01DF15FC`/`01DF160C` block. Interior anchor `0015C2D7` (the loop-head `movups` load).

## SWE2-EC7-38 update (2026-09-19) - `00196290`

`00196290` (488 B) is the `InputProfiles_CopyLiveRecordsBackToBank` body the page names - call-free `movups` 0x80-step copy `01F80130`/`01F8028C`/`01F803E8` into `01DF1738`. Interior anchor `001962B7` (inside the copy loop).

## SWE2-EC7-39 update (2026-09-19) - `0015BF20`

`0015BF20` (420 B) is the `01F80970` conditional-bank builder the page names - call-free `movaps` head template `01DF0980`..`01DF09B0` then a `movups` copy loop from `01F7FFF0` into `01F80970`..`01F80ACC`. Interior anchor `0015BF53` (the `01F80970` store).

## SWE2-EC7-39 update (2026-09-19) - `0015C0D0`

`0015C0D0` (420 B) is the `01F80550` conditional-bank builder - same call-free shape, head template `01DF0980`+ then `movups` from `01F7FFF0` into `01F80550`..`01F806AC`. Interior anchor `0015C103` (the `01F80550` store).

## SWE2-EC7-42 update (2026-09-19) - `001D7150`

`001D7150` (296 B) is a keymap body - `0027E9D0` triple/`0020E600` pair/`002A0060` pair/`0024B0C0` pair. Interior anchor `001D7167` (a `0027E9D0` call).

## SWE2-EC7-43 update (2026-09-19) - `0017DEA0`

`0017DEA0` (276 B) is `InputQuery_PollSpeedModeKeys` - `01F7F4E9` edge-latch, `00198790`/`00197710` binding-resolve triple then `0079E6A0`/`00239790` with `ecx` = 1/2/4 (`Speed1/2/3`). Interior anchor `0017DEA6` (an `00198790` call).

## SWE2-EC7-46 update (2026-09-19) - `00197A50`

`00197A50` (229 B) is a body - `00194F50` plus `008C2740`/`008C2698`/`008C2680`/`008C2638` import calls. Interior anchor `00197A83` (the `00194F50` call).

## SWE2-EC7-49 update (2026-09-19) - `00196480`

`00196480` (194 B) is the keymap float reader - `005CC930` single call (reads the float at `01DF0970`). Interior anchor `001964A3` (the `005CC930` call).

## SWE2-EC7-61 update (2026-09-19) - `00797F60`

`00797F60` (151 B) is an indirect-only keymap writer - `byte[rdx]&0x7F` through the `01F3DA30` scancode table minus `0x1C` -> `byte[+0x30]=1` flag array, then `call [rax+0x38]`. Interior anchor `00797FAA` (the `byte[+0x30]=1` flag store).



## SWE2-EC7-64 update (2026-09-19) - `00239790`

`00239790` (141 B) is the `SetSpeedMode` body - `00229E20`/`00229ED0`/`002DE250` plus `0208E6B4`. Interior anchor `00239798` (a `00229E20` call).



## SWE2-EC7-64 update (2026-09-19) - `002A0060`

`002A0060` (140 B) is the `+0x0C` `u16` -> atlas-object resolver - `0020E600`/`0024A5F0`/`0024A610`. Interior anchor `002A0081` (a `0020E600` call).

## Crossing accounted 2026-09-19 (FABLE): Developer

**Developer - SERVICE.** The slot-4 pump `0017D6E0` on this page calls `001C2F50`, owned by the Developer layer, once a
pass. What it reaches is an overlay routine that asks the settings object for its byte `+0x10D4`, tests the byte
`01F8127C`, and **returns at once unless both are set** - switched off in a shipped configuration. Only that head was
read (the body is 1,046 bytes). The crossing is that call; nothing about key bindings passes through it.

## SWE2-EC7-78 update (2026-09-20) - `00796FC0` nth-match list find measured

`00796FC0` (137 B) is the `01F401E8` intrusive-list scan the binding
callers use: it walks `+8` links from the `01F401E8` head (node =
link - 8), calls each node's vtable `+8` slot, counts matches
against `ecx` in `edi`, and returns the node when `edi` reaches
`edx` - an nth-occurrence find. Empty list or count shortfall
returns 0.
Interior anchor `00797006` (the `call [rax+8]`).

## SWE2-EC7-102 update (2026-09-20) - `00290C80` measured

`00290C80` (28 B) is the `0209BE80`-rooted forward
`002778C0` and `0027B880` call: when the root is
nonnull it tail-jumps `002BE230` with
`rcx = root + 0x8FA0` and `edx = movzx(cx)`; a null
root returns - the presence-gated trampoline the
binding paths share.
Interior anchor `00290C8F` (the `+0x8FA0`
add).

## SWE2-EC7-111 update (2026-09-20) - `001969D0` measured

`001969D0` (127 B) is the
detach-and-reset `00195180`,
`00198000` and `001993B0`
run: a null `qword[+0x80]`
answers 0 with the flags
still cleared; else
`00195940()` decides whether
`rbx` survives, the
`008C2F00` IAT call takes
`[+0x80]` as its argument and
a nonzero return vetoes the
survival, `byte[+0x7C]` and
`byte[+0x72]` clear, the
`008C2698` virtual call runs
on `rbx`, `[+0x80]` zeroes,
`[+0x74]` relatches the
`01F810E0` global and
`[+0x68]` clears - returning
`rbx` only when both gates
passed.
Interior anchor `001969F7`
(the `[+0x80]` argument
fetch).

`0024A610` (75 B) is the atlas-compare helper `002A0060` and `0029F130` call: `0208F580` bases the record table, `byte[r9+0x38] & 0x20` gates each candidate, then a byte-wise `sub` scan compares the name - the `+0x38`-flagged string match.

Interior anchor `0024A620` (function `0024A610`).

`0024A5F0` (19 B) is the atlas indexer `002A0060` and `0029F130` call: `ecx * 9 * 8` strides into `0208F580` - the 72-byte record's element address, call-free.

Interior anchor `0024A5F7` (function `0024A5F0`).

`001D82D0` (581 B) is the layout arm `001D7DD0` calls: `[rcx+0x30]`'s shorts `+4`/`+6`/`+8`/`+0xA` sum into `ebx`/`edi`, `001B1620` gates, then `001B1C00` + `byte[+0x3A98]` pick between the `008C5B5C`/`008C5B48` constant pairs before the xmm6-13 float work - the profile's rect compute.

Interior anchor `001D833B` (function `001D82D0`).

`00196C40` (419 B) is the binding-record assembly `00196FF0` calls: `01F80970`/`01F80FEC`/`01F8113C` globals seed the `[rbp-0x40]` frame, four `00796E20`/`0079AE90` pairs parse and store each field, `00808C40` checks the cookie - the keymap's per-entry fill.

Interior anchor `00196CC5` (function `00196C40`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-EC7-159)

**Developer — SERVICE (SWE2-EC7-159, 2 edges).** `001C2F50` sits on both sides of this page's
binding helpers — the slot-4 pump `0017D6E0` calls it and it calls `00796E20` — the Developer
overlay routine that returns early unless settings byte `+0x10D4` and `01F8127C` are both set.
Shared helper exchange, not a keymap responsibility.

**PlatformOnlineAchievements — MECHANICAL (SWE2-EC7-159, 13 edges).** `00197EE0` calls `001F3ED0`,
which is itself called by `0079FA00`/`00862A40`/`0022A770` — platform-layer helpers the keymap
parse path neighbours. Shared-helper exchange only.

**Presentation — MECHANICAL (SWE2-EC7-159, 107 edges).** `0017D6E0` calls Presentation-tagged
bodies `00189CE0`/`001BC190`/`001BDAC0`/`001CCxxx` et al. — the binding pump's fan-in to shared
presentation helpers. Not a keymap responsibility.

**Resource — MECHANICAL (SWE2-EC7-159, 14 edges).** `0017D4C0` calls `001A11B0`/`001DB1E0`,
`0017D6E0` calls `001A1220`, `0022A770` calls `00324510` — resource-layer helpers neighbouring the
binding helpers.

**CoreRuntimeScheduling — MECHANICAL (FABLE, Claude Opus 5.5, 2026-09-25).** The system-stop registry's slot-record
builder `00227680` and its release paths, together with the binding pump's frame drivers, are that layer's. `UQ-143`
cites them only for which stop slot sets or clears each input-mode bit. Nothing else they do is a keymap claim.

**UI — MECHANICAL (SWE2-EC7-159, 62 edges).** `0017DDC0`/`001E0C10` are called by UI bodies
`003C8B70`/`00276960`/`0027C870`/`0027DCA0` — UI fan-in to the shared binding helpers.
