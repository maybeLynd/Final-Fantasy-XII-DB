# Reconstruction readiness, pass 2 — `FFXII TZA/15-Input/`

| | |
|---|---|
| Stream | R2 (reconstruction readiness, pass 2), per [`docs/cloud-briefs/re-readiness-r2.md`](../../docs/cloud-briefs/re-readiness-r2.md), part A |
| Lane | FABLE (cloud session r2-16) |
| Pass 1 | [`cloud-reports/re-readiness/15-input.md`](../re-readiness/15-input.md) (2026-10-01, rated **MOSTLY**) |
| Date | 2026-10-03 |
| Snapshot | this repo's text snapshot (synced from XIIOnline `f9d9053b9`); no executable, Ghidra or live game was used |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every verdict quotes or paraphrases a page, with its location. |

Citation form: `page:line`, with the path relative to `FFXII TZA/`. Pass 1 limited "not stated" to the 15-Input pages
and the one 16-UI section they defer to. This pass reads the current 15-Input pages and the register
(`_index/OPEN-QUESTIONS.md`). It also follows pass-1 gaps to other systems' pages when a page there now carries the
answer. In that case the verdict says the 15-Input page lacks the pointer (class DOC).

Pages re-read: `15-Input/README.md`, `CONTRACT-input-subsystem.md`, `how-a-gamepad-becomes-a-controller-object.md`,
`Input-Stack/input-stack-device-channel-and-bindings.md`, `Binding-Profiles/CONTRACT-binding-profiles.md`,
`Binding-Profiles/binding-profiles-remapping-and-control-state.md`,
`Binding-Profiles/keymap-ini-file-format-and-default-controls.md`, `Input-Name-Registry/CONTRACT-input-name-registry.md`,
`Input-Name-Registry/the-input-name-registry-and-channel-aliases.md`,
`Gameplay-Capability-Policy/capability-inhibition-policy.md`, `Modal-Toggles/r2-force-fight-toggle.md`. Pages outside
15-Input that were followed are cited where used.

---

## 1. Summary

**Pass-1 gaps: 52** (18 page-stated G-L, 7 G-A, 6 G-B, 5 G-C, 5 G-D, 2 G-E, 9 contradictions G-*x).

| verdict | count | ids |
|---|---:|---|
| **CLOSED** | **10** | G-L7, G-B5, G-B6, G-C1x, G-C2x, G-C3x, G-C4x, G-C5x, G-C6x, G-C7x |
| **NARROWED** | **15** | G-L2, G-L6, G-L9, G-L12, G-L16, G-A3, G-A4, G-A5, G-B3, G-B4, G-C4, G-C5, G-D2, G-E1, G-C8x |
| **OPEN** | **26** | G-L1, G-L3, G-L4, G-L5, G-L8, G-L10, G-L11, G-L13, G-L14, G-L15, G-L17, G-L18, G-A1, G-A2, G-A6, G-B1, G-B2, G-C1, G-C2, G-C3, G-D1, G-D3, G-D4, G-D5, G-E2, G-C9x |
| **WRONG-IN-PASS-1** | **1** | G-A7 |

The 41 gaps still OPEN or NARROWED, by the class of their remaining part:

| class | OPEN | NARROWED |
|---|---:|---:|
| STATIC | 20 | 9 |
| RUNTIME | 5 (G-L1, G-L3, G-L4, G-L8, G-L17) | 3 (G-L2, G-L9, G-L16) |
| DATA | 0 | 1 (G-A4) |
| DOC | 1 (G-C9x) | 2 (G-C8x, G-D2) |

**New gaps: 12**, of which **DOC 8**, **STATIC 4**, RUNTIME 0, DATA 0. Seven of the DOC gaps are stale text: a
contract or section that still lists as open something another page or the register has since answered. The other
DOC gap and the four STATIC gaps are disagreements between pages, or callees that are named but not described.

**Rating: MOSTLY (pass 1: MOSTLY).** Unchanged. The register closed several rows behind pass-1 gaps (AU-4, GG-1, C-7,
DM-1, DM-3, the binding contract's §14 items), and three of pass 1's contradictions were corrected at the bytes on
2026-10-01. The two whole-function blockers are only narrowed, not closed: the arbiter's decision logic, and the
pad and backend device bodies. See §4.

---

## 2. Pass-1 gaps

Abbreviations for the 15-Input pages: **SUB** = `15-Input/CONTRACT-input-subsystem.md`; **PAD** =
`15-Input/how-a-gamepad-becomes-a-controller-object.md`; **STK** =
`15-Input/Input-Stack/input-stack-device-channel-and-bindings.md`; **BPC** =
`15-Input/Binding-Profiles/CONTRACT-binding-profiles.md`; **BPR** =
`15-Input/Binding-Profiles/binding-profiles-remapping-and-control-state.md`; **KMI** =
`15-Input/Binding-Profiles/keymap-ini-file-format-and-default-controls.md`; **NRC** =
`15-Input/Input-Name-Registry/CONTRACT-input-name-registry.md`; **NRS** =
`15-Input/Input-Name-Registry/the-input-name-registry-and-channel-aliases.md`; **CAP** =
`15-Input/Gameplay-Capability-Policy/capability-inhibition-policy.md`; **R2T** =
`15-Input/Modal-Toggles/r2-force-fight-toggle.md`; **REG** = `_index/OPEN-QUESTIONS.md`.

The class column applies to what is still missing (OPEN or NARROWED); it is blank for CLOSED and WRONG-IN-PASS-1.

### 2.1 Gaps the pages state themselves (pass 1 §2.1)

| id | verdict | evidence (quote + `page:line`) | still missing | class |
|---|---|---|---|---|
| G-L1 no live frame order | OPEN | "**Anything live.** No frame order here has been observed in a running process. Readiness is `CONTRACT READY`, not `RECONSTRUCTION READY`." (SUB:415-416) | any live capture of the §3 order | RUNTIME |
| G-L2 GG-1 reader placement | NARROWED | Register GG-1: "**ANSWERED 2026-09-28 (SWE2-FRONTIER ruling …): 50 of 51 readers statically placed, and `003C87B0` is placed on its arbiter and world-tick paths. The residue is bounded and owned: `003C87B0`'s paths through `00254B40` and the widget message-1/12/18 handlers are runtime-only**" (REG:3349, status cell) | `003C87B0`'s placement on its `00254B40` and widget message-1/12/18 paths; the live values of the `0022AB83` gates ("the game's MXCSR and the accumulator's live values are unobserved", SUB:348-349). SUB's own GG-1 bullet is stale (new gap N1) | RUNTIME |
| G-L3 GG-3 residue | OPEN | "**Not established:** the real handler's behaviour inside a live widget tree, and which frames reach the walk in play." (SUB:394-395) | unchanged | RUNTIME |
| G-L4 assignment never observed live | OPEN | "**Not validated:** assignment, the conflict swap, publication, the pair swap, the three-bank poll order, and channel timing. **No experiment has driven `00198A00` or observed `01F80130` change.**" (BPC:486-487) | unchanged | RUNTIME |
| G-L5 translator and assigner not reimplemented | OPEN | "One operation of the write path is done; assignment (`00198A00`) and the translator (`00197160`) are not, and nothing here has been observed in a live process." (BPC:655-657) | a reconstruction and differential test of `00197160` and `00198A00` | STATIC |
| G-L6 pad polls, `EnumObjects`, mouse/keyboard arms, removal | NARROWED | The mouse arm is now read: `00797460` "entered from `00796230` + 0x3C", which calls DirectInput slots `+0x58` (with `01CC7130`), `+0x68` (with qword `02EA5248` and 6) and `+0x38` (PAD:260). The pad polls are named, but only on KMI: "The XInput and Steam polls fill slots 0–15 only … The DirectInput poll alone copies `rgbButtons[16]` into slot 16" (KMI:884-886). The record `_index/candidates/dm2-code27/README.md` gives their addresses (`007A2140`, `007A1CD0`, `007A1A50`). | PAD still says "**Not read:** the mouse and keyboard arms; each kind's poll; the `EnumObjects` callback; what happens on removal." (PAD:123) and "Whether the duplicates cause doubled input depends on each kind's poll, which is still not read." (PAD:243). Not stated: the polls' stick and trigger stores; the `EnumObjects` callback; what a removed pad's poll does; whether duplicate Steam objects double input. PAD lacks a pointer to KMI:884-886. | STATIC |
| G-L7 AU-4 blocks 2 and 3 | CLOSED | Register AU-4: "**ANSWERED 2026-09-26 (OPUS), STATIC: three blocks of three `InputBindingRecord`s, and the stated end is a record's axis table, not a short third block.** … Blocks 2 and 3 therefore hold three records each, like block 1." (REG:492) | — (BPR's own AU-4 section is stale, new gap N7) | |
| G-L8 UQ-146 dangling stack return | OPEN | Register UQ-146: "**SUPERSEDED 2026-09-27 (FABLE …) under the runtime rule; live carrier FABLE-REQ-ASTRA-UQ146-IN-PROCESS-FORMATTER-READ.**" (REG:2860); KMI: "What remains is a property of the installed `ucrtbase.dll`, not of this executable, and only an in-process observation can settle it." (KMI:1022-1023) | whether `ucrtbase`'s frames clobber the buffer before the `%s` is read | RUNTIME |
| G-L9 UQ-147 leader / mode-1 counterpart | NARROWED | Register UQ-147: "the mode-1 counterpart is the Esper summon sequence's acting member (+0x5AD5 on the battle-state block page, writer and clearer named). Whether initialized gameplay reaches the null-leader state is live and carried by FABLE-REQ-ASTRA-LEADER-STATS-NULL" (REG:2861). CAP: "So a unit that `003272A0` returns always has a non-null `+0x698`." (CAP:1185) | the live check; CAP lists the routes its typed census cannot see (CAP:1189-1192) | RUNTIME |
| G-L10 name-registry integration | OPEN | "**One of the five is reconstructed**; the other four are understood and not reimplemented." (NRS:331-332); "**Still not reconstructed**, which is a different thing" (NRC:302) | reimplementation of the destructor, the two lookups and the enumerator | STATIC |
| G-L11 no analog names | OPEN | "**Anything about axes.** Every name recovered is a button or a key." (NRS:402) | unchanged; the axis indices exist only as the kind-3 `subKind` of binding records (KMI:952) | STATIC |
| G-L12 `0023C5C0`'s screen, command `0x2CA1`, row 0 | NARROWED | The screen is now identified on another page: the Controls pane's record walk sends "kinds 1-2 -> `0023C5C0` (key-bind rows)" (`19-Save-Load-Settings/Game-Settings-Config/the-settings-command-table.md:203-207`) | BPR still says "Which screen `0023CE10` builds, and what `0x2CA1` and row 0 are, are not read." (BPR:790-791). Not stated anywhere read: what command `0x2CA1` and row 0 are. BPR lacks the pointer. | STATIC |
| G-L13 `001967D0` with a 1–3 code | OPEN | "what it then does with a 1–3 code was not read in this pass." (KMI:251-252) | the body after the `(code - 1) < 3` test | STATIC |
| G-L14 `001E0C10`'s eleven callers | OPEN | "Its eleven callers (`00276AF6` … `00393C6E`) were not each read." (KMI:902-903) | unchanged | STATIC |
| G-L15 mouse wheel channel; accumulator consumers | OPEN | "the device driver was not read to confirm channel 3." (BPR:1062) | the mouse device's channel 3; any reader of `[01F7FFE0]+0x0C` / `+0x10` (none is named) | STATIC |
| G-L16 rumble cut-off in wall time | NARROWED | Still "The update rate per second is not read here." (BPR:365). The poll rate is now stated per frame: "The poll runs once per dispatcher frame in modes 2, 3 and 5" (STK:270). SD-9 adds that the worker deadline "paces nothing" (STK:532-534). | the dispatcher's frames per second in play. KMI ties `FrameLimit` 30/60 to the frame base (KMI:454-456), but no page links that to the input poll | RUNTIME |
| G-L17 meaning of `+0x3A` bits | OPEN | "The reading of the bits as \"battle menu\" and \"menu or locked\" comes from the slot names, not from a live observation." (KMI:939) | live confirmation | RUNTIME |
| G-L18 UQ-152 bound | OPEN | Register UQ-152 is ANSWERED (REG:2866), but its bound stands: "**An indirect call from inside a thread cone into one of the four would not appear here.**" (R2T:515) | an indirect-call resolution over the thread cones | STATIC |

### 2.2 Gaps pass 1 found while mapping (pass 1 §2.2)

| id | verdict | evidence (quote + `page:line`) | still missing | class |
|---|---|---|---|---|
| G-A1 snapshot field map past channel 0 | OPEN | Channel 0's eight words are now named in order: "**In the gameplay snapshot** `02F97360` these are, in order, `+0x06`, `+0x0E`, `+0x0A`, `+0x12`, `+0x04`, `+0x0C`, `+0x08`, `+0x10`" (STK:465-466). The rebuilder still ORs "for each of the two channels (a 0x14-byte record)" (`16-UI/Config-Screen/the-config-screen-and-what-a-setting-change-runs.md:200`). | The meaning of `02F97370`–`02F9739B`: channel 1's words, the per-index bytes `byte[02F97370 + 20·i]` / `byte[02F97371 + 20·i]` (SUB:297-298), and `02F97392`, which SUB names only as "the snapshot's filtered word" (SUB:129). Also how eight u16 words fit a "0x14-byte record". | STATIC |
| G-A2 rebuilder lookback count | OPEN | "ORs eight history mask fields over the lookback frames" (Config-Screen page :200-201); STK: "`+0x08` u8 history lookback count: the per-frame cursor step stores the write-to-read distance here (B4)" (STK:364) | how many frames the rebuilder ORs, and which function performs "the per-frame cursor step"; "B4" is a control in a candidate record, not a page | STATIC |
| G-A3 arbiter decision logic | NARROWED | Parts are now written on 16-UI and Engine Core pages. "Triangle, mask `0x1000`, posts request 2 with parameter 0"; both `0x21` posts follow "`cmp ebp, ebx` with `ebx = 1`" (`16-UI/Request-Router/ui-request-router.md:458`). "Decide/Square -> request 1 \| `00253C70` tests `01E0C2A0 \| 0x8000` then hardcodes requestId 1" (ibid. :675). The arbiter's 22-member subtree is tabulated, gates included (`00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md:882-899`). | Still no single statement of `00253C70`'s branch order: which press raises which request under which modal state, and what each of its 11 direct callees decides. SUB keeps to reads and writes (SUB:120-152), and no 15-Input page points to the parts above. | STATIC |
| G-A4 story flag in the arbiter | NARROWED | "`00253F21` passes **`0x5E`** … Bit 14 is clear, so this is the primary route"; "`002540AF` passes **`0x4008`** … this one takes the authored route with id 8." (`00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md:452-456`); flag `0x5E` set selects "script operand-bank word 2" as request 2's parameter (`16-UI/Request-Router/ui-request-router.md:461-466`) | What the authored id 8 gates in the arbiter. The authored name of flag `0x5E` ("*Not established:* … the authored name of flag `0x5E`", ui-request-router.md:468-469). SUB still says "Which flag, and what it gates, is not read here" (SUB:467-468) and has no pointer. | DATA |
| G-A5 `0035EF10(0,0)` and `[[0209AC30]+0x308]` | NARROWED | "`0035EF10` (86 B) bounds-checks `ecx < 2`, strides `ecx * 0x294` into `022CAE90`, then adds `r8d` to `byte[+1]` … and returns `word[rdx + (index+2)*36]`" (`22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md:1269-1272`); the widget page calls it "the history mask (`0035EF10(0,0)`)" (`16-UI/Widget-Object-Model/the-widget-message-protocol.md:729`) | which of the eight history mask words `0035EF10` returns (no frame offset is named); what the object at `[[0209AC30] + 0x308]` is ("the `+0x308` record of `0209AC30`", ibid. :728); SUB lacks both pointers | STATIC |
| G-A6 producer/consumer threading | OPEN | The poll runs on the vsync-callback thread `00369100` (STK:245-247); the rebuild runs on the frame path at `0022B908` (SUB:90) | how the frame path and the poll thread are synchronised, and whether the rebuild can read a half-written history frame | STATIC |
| G-A7 tick field-arm dead branch | WRONG-IN-PASS-1 | "`esi` is loaded from `r13d` at `003141BA`, and `r13d` was zeroed at `003140D9` and never written again" (SUB:113-114); §3: "`r13d = 0 (003140D9)`" (SUB:96). `r13d` is zeroed inside `00314020` itself, so no caller can pass a non-zero value; pass 1's question misread the register as an argument. | — | |

**B. Capability policy**

| id | verdict | evidence (quote + `page:line`) | still missing | class |
|---|---|---|---|---|
| G-B1 aggregate bit 19 and `00360360(0x10)` | OPEN | "the same code as `002E0FA0`, including `btr ebx, 0x13` when `00360360(0x10)` is set" (`16-UI/CONTRACT-ui-request-router.md:150-151`); CAP:311-312 unchanged | the meaning of policy bit 19 and the body of `00360360` | STATIC |
| G-B2 initial value of the 16 rows | OPEN | CAP:317-322 gives the shape only; `002E1CD0` sets or clears `0x139203` wholesale on rows 0, 3 and 6 "from the field-entry, area-unload and notify functions" (CAP:219-223) | the rows' initial value (section, initialiser) and any reset on boot or area change | STATIC |
| G-B3 row-ownership map | NARROWED | SD-3's census: "A census of all 77 set/clear call sites also finds row-1 writers in the movie player (`001B7690`, `001B7F30`, `001B8400`, `001B82A0`), the spawn-verb body `0023FBE0`, `002CEB40` and the title-asset consumer `003939B0`; a row-0 writer, the title singleton's handler `00394070`; and the rows 2/8 restore loop `00229510`." (CAP:238-242) | owners and bits for rows 4, 5, 7 and 9–15 (none named); row 8's writer other than the restore loop | STATIC |
| G-B4 meaning of directly-tested bits | NARROWED | C-7 census: "**bit 4** is tested by `002736B0`, `00273950` and `002C64C0` … and by nothing else; **bits 7, 11, 12 and 20 are tested by no reader at all**"; "The remaining aggregate bits with readers are 5 (`00283270`), 10 (ten functions …), 18 (`003C8B70`) and 21" (CAP:226-230); bit 21 = the pause-menu gate (CAP:234-238) | the behavioural meaning of bits 0, 6 and 9 outside the UI projection (CAP:118-119 lists them as tested); what `00283270` (bit 5) and `003C8B70` (bit 18) do with the bit | STATIC |
| G-B5 UI requests 14 and 21 | CLOSED | "**C-1 / C-2 closed 2026-09-12 (FABLE): not in the image — neither id has a dedicated handler at any level.** … the two ids are **unused generic-arm request numbers**" (`16-UI/Request-Router/ui-request-router.md:433-446`) | — CAP:100-102 still says "two valid-but-unnamed slots" with no pointer | |
| G-B6 `00237260` | CLOSED | "`00237260()`: every *active* member of kind 0 outside the guest range 7–25 is incapacitated (`0023728D`–`002372B2`); request `0x18`" (`00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md:338`) | — R2T:291 still says only "policy-side predicate … ORs with policy bit 10", no pointer | |

**C. Channel layer and feedback**

| id | verdict | evidence (quote + `page:line`) | still missing | class |
|---|---|---|---|---|
| G-C1 who sets the feedback inputs | OPEN | BP-4: the motors are written "while record `+0x09` bit 2 is set: motor 0 = `strength(+0x07) × accumulator >> 14` … motor 1 = bit 7 of `strength(+0x06) × accumulator >> 14`" (BPR:365); only the initialiser's clear of flag bit 1 is stated (STK:365) | the writer of `+0x09` bit 2 (feedback enable) and bit 4 (timing "held"), and of strengths `+0x06` / `+0x07`; a game-side "start rumble" entry | STATIC |
| G-C2 channel 1 | OPEN | "channel 0 on every tick (the skip bit is set only on an availability value the always-1 stub never returns)" (STK:249) | what channel 1 is and when it is polled | STATIC |
| G-C3 caller of `0035F260` | OPEN | the body is now described ("clears `022CB3C0` + ch x `0x100` (`0035F29A`) and the channel record `022CAE90` + ch x `0x294` (`0035F2E3`) with two `memset` calls", `19-Save-Load-Settings/Game-Settings-Config/ff12config-and-debglobal.md:189`) | its caller and when it runs | STATIC |
| G-C4 `007A2440` and `0079D1D0` bodies | NARROWED | "`0079D1D0` (327 B) is the aggregate variant `00197160` calls: the same four-member threshold reads, but it walks all `0x12` `+0x88` entries accumulating into `xmm3` and early-exits on the first nonzero pick" (`99-Unresolved-Residual/Glyph-Run-Rendering/painting-a-line-of-text-into-a-render-target.md:812-822`); two callees of `007A2440` are described, `007A3150` and `007A0410` (ibid. :749-786) | `007A2440` (3,269 B) as a whole, so the backend's resolved-state pass and its stick dead zone; how `0079D1D0` uses its axis argument (the description gives an `edx` dispatch, not the axis mapping). STK:303-304 lacks pointers. | STATIC |
| G-C5 deadline constants | NARROWED | "`0035E7A0` … adds dword `022CA5D0` to dword `022CA5C4` … with P = 0x108 when `00290180()` returns 2, else 0x13A" (STK:1169); "**paces nothing: the result is the constant 528 (264 in mode 3), stored at `022CA5DC` and never read**" (STK:533-534) | what the worker's wait on the doubles −16.0 / 17.0 (`00908D60` / `00908D58`, STK:497-498) measures in wall time | STATIC |

**D. Bindings**

| id | verdict | evidence (quote + `page:line`) | still missing | class |
|---|---|---|---|---|
| G-D1 kind-3 sensitivity constant | OPEN | "the value scaled by the sensitivity constant and doubled again by the invert bytes" (KMI:952); BPC's §12 formula has no such factor (BPC:400-409) | the constant's address and value, and the corrected kind-3 formula | STATIC |
| G-D2 `+0xC35` gate | NARROWED | Named on Engine Core pages: "`+0xC35` Enable mouse control camera" and "**`+0xC35` mouse camera.** `00197160` gates on it (`001973C8`–`001973D4`)" (`00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-F-ids-172-203.md:268`, `:281`); it is console arm 187, a "boolean toggle" (ibid. :120) on the settings singleton read through `001D50D0` | its value at boot (no page read states the constructor's store); KMI:952 still says only "the singleton byte `+0xC35`", with no pointer | DOC |
| G-D3 callers of `001E0F40` / `001E0F70` | OPEN | bodies described elsewhere (`24-Compiler-And-CRT-Runtime/Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md:970`; `24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/object-construction-destruction-and-static-lifetime.md:1135`); KMI:385-386 gives no caller | which screen action calls each | STATIC |
| G-D4 record bytes `+0x140`..`+0x15B` | OPEN | BPC: "the `0x1C` bytes per record beyond the translator's `0x140`" (BPC:510); register AU-4: "The records' `+0x140` tail (28 bytes) is not written by the initialisers" (REG:492) | whether anything reads them; KMI:685 says "zeroed by the defaults path" | STATIC |
| G-D5 hot-plug failure return 9 | OPEN | "A failed re-enumeration returns 9 and skips that frame's poll (`00799A19`)" (PAD:234); "a negative answer returns 9" (BPR:1676-1677) | what `00196FF0` does with the 9; whether the translator still runs on that frame | STATIC |

**E. Modal toggle (R2)**

| id | verdict | evidence (quote + `page:line`) | still missing | class |
|---|---|---|---|---|
| G-E1 `00862CF0` | NARROWED | "`00862CF0` (68 B — lazy `00862C70` init if `02EAF8F0` unset, then an indirect `call qword ptr [02EBA3F0]` with args `(0, &02EBA3E0)` … returns 1 iff the returned word `02EBA3E4` carries `0x400`)" (`00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md:895`); PAD: `00862C70` "loads `.\xinput1_3.dll` … and resolves **ordinal 100** into `02EBA3F0`" (PAD:232) | which control bit `0x400` of the returned word is (not stated); R2T:104 has no pointer to either page | STATIC |
| G-E2 mode register `022C83EC` | OPEN | R2T: "bit 0 gates the battle-menu build; bits 2-3 written here" (R2T:314); `0028E5F0` "stores bit 1 of `022C83EC`" (R2T:441) | a writer census and the meaning of each of bits 0–3 | STATIC |

### 2.3 Contradictions between pages (pass 1 §2.3)

| id | verdict | evidence (quote + `page:line`) | still missing | class |
|---|---|---|---|---|
| G-C1x what `001965E0` checks | CLOSED | "~~returns 1 when no profile is fully in range~~ returns 1 unless profile 1 is fully in range … *(corrected 2026-10-01, OPUS, from the 15-Input reconstruction-readiness map, re-read at the bytes …)*" (STK:300); also STK:400 | — | |
| G-C2x records copied by `00196290` | CLOSED | "copies ~~2 records `01F80130` → `01DF1738`~~ **3 records of `0x15C`** … (the `2` at `00196290` is the inner `0x80`-byte round count) *(corrected 2026-10-01, OPUS …)*" (KMI:383) | — | |
| G-C3x sign of a two-code axis | CLOSED | "the `invert` above is per ENTRY, not one flag. Entry 0 uses the input manager's byte `+0x08` … entry 1 its `+0x09` … entries 2 and 3 are always inverted … entries 4-15 never." (BPC:419-424) | — BPC adds: "Which on-screen direction a low or high right-stick value turns the camera is not established here." (BPC:425-426) | |
| G-C4x `01DF1738` "staging" | CLOSED | "*(Corrected 2026-10-01, OPUS: `0x01DF15DC` and `0x01DF1738` are records 1 and 2 of the five-record bank the poll walks every frame …)*" (STK:799) | — KMI still says STK §11 carries "staging" (new gap N8) | |
| G-C5x BPC §14 / §17 items answered elsewhere | CLOSED | each listed item is now struck with "*(Superseded: … propagated 2026-10-01, OPUS, from the system page; register rows answered.)*" — `DC-2`, `DC-3`, `BP-3`, `BP-4`, `BP-5`, the bank writers (BPC:503-511), records 0 and 1, group 2's consumer, the axis entry's `+0x04` (BPC:665-676) | — other BPC rows were left stale (new gap N2) | |
| G-C6x NRC §14 `DM-1` / `DM-3` | CLOSED | NRC:288-293 superseded "**ANSWERED 2026-09-22 (FABLE)**" for both; NRS §7's `DM-1` bullet is struck, "Struck 2026-10-01, OPUS" (NRS:396-397); register rows DM-1 and DM-3 ANSWERED (REG:415, REG:417) | — | |
| G-C7x C-7 row's "all but 1 / 5 / 10" | CLOSED | Register C-7: "~~one condition for all but 1 / 5 / 10~~ all but 1 / 10 - bit 5 follows the selection too, written at `00313AA0`-`00313AA8`; corrected 2026-10-01, SWE2-DATA" (REG:143); CAP:1163 records the check | — | |
| G-C8x body banners vs status lines | NARROWED | STK: "~~**PARTIAL.**~~ *(Superseded 2026-10-01, OPUS: the status line reads DOCUMENTED …)*" (STK:32) | R2T still opens "**PARTIAL, deliberately.**" (R2T:32) under a DOCUMENTED status line (R2T:4) | DOC |
| G-C9x profile numbering | OPEN | R2T: "`GetBinding(mgr, /*profile*/ 0, /*group*/ 0, /*slot*/ 9)`" (R2T:74); KMI: "Every one of its six callers reads **profile 1 only**" (KMI:272) and "`GetBinding(profile 1, group 2, slots 0/1/2)`" (KMI:739) | one stated convention (0-based index vs `[Keyboard1]` naming) | DOC |
