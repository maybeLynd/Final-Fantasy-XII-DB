# One original three-selector update: negative is not always skip

Question: does each negative selector independently skip its field group, or does the second selected row supply a default when the third selector is negative? **Method A is sufficient**: original signed branches, the EDX-to-R9D transfer and file-backed table rows distinguish the hypotheses. No game, original-code harness or reconstructed execution was run. Conditional recipes below are source calculations, not original-runtime observations.

Original `00712180`, 353 bytes, certificate SHA256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, is reused unchanged from the committed one-row extent package `69ef8ebc14a79f07162c539017764d4b6c7bb7cc`. That boundary delivery is not semantic admission. FABLE's ruling, existing independent corroboration and FRONTIER GO requirements still apply. The other 49 held rows are untouched. This package does not classify the executable or award population changes.

The leaf preserves the incoming target RCX in R10 and returns it. Null target branches directly to return with no stores. EDX, R8D and R9D are tested as signed low32 selectors. The first negative selector skips its group; otherwise it is capped at7. The second negative selector skips its group; otherwise its upper cap is10 when byte `00D9F05E` is zero and19 when nonzero. The third nonnegative selector is capped at9.

**The third negative selector is coupled to the second group.** A selected second row loads its word at `+10` into EDX (`00712207`), writes that word to target `+8C` (`0071220A`), and, if the supplied third selector is negative, copies EDX into R9D (`0071222A`) before the final sign test. Every one of the20 bounded original second rows supplies a nonnegative value1..5 there. Thus, with a selected second row and the original stable tables, a negative third selector selects its row default instead of leaving the third group untouched. If the second selector is also negative, a negative third selector skips the group. A nonnegative third selector takes precedence, but target+8C still stores the second row's default, **not necessarily the effective third row index**.

The exact DWORD copy recipes are:

| Group | Original table / row stride / bounded rows | Ordered target offsets |
|---|---|---|
| First | 01F3C5B0 / 8 / 8 | 4C,54 |
| Second | 01F3C5F0 / 28 / 20 (mode cap10 or19) | 7C,84,88,CC,8C,E4,E8 |
| Third | 01F3C820 / 56 / 10 | 90,94,98,9C,A0,A4,A8,AC,B0,B4,B8,BC,C0,C4 |

The current file bytes, PE section/raw backing, source/provider/reader/shared adapter identities, original instruction records and exact table bytes are retained. DWORD transfer does not prove integer versus float semantic types. The physical field envelope through+E8 width4 is not a constructor/object size. The file byte flag's sampled value is not proof of its runtime meaning or stability. No named graphics/game-setting/Phyre object is inferred from offsets or float-looking constants; its major-system and type linkage remain **unassigned** for FABLE/OPUS.

Discriminating conditional example: with nonnull disjoint valid target, first=-1, second=0, third=-1, the original second row defaults to1, producing7 second-group plus14 third-group stores. A private source-only replacement of `MOV R9D,EDX` with three NOPs leaves R9D negative and gives only the7 second-group stores in the derived recipe. The patch is refused by shipping identity; it was never executed or deployed. With explicit third=9, the third row becomes9 while target+8C still gets1. Upper selectors clamp to[7,10,9] in zero mode and[7,19,9] in nonzero mode. Null/all-negative examples leave all groups untouched. These are bounded source/control calculations; no extra native tests are claimed.

check.py verifies the exact original branch/CMOV/transfer/return instructions, extracts load/store pairs from adjacent original instructions, binds all table and flag addresses/bytes/backing, validates the source-only control and recipes, and checks tool/preimages. source.py's actual default invocation uses the shared reviewed `reg_tracking.op_kind` adapter; original stores are classified `w` and table LEAs `addr`. No raw Capstone access flags bypass that policy. There are no memory read-modify-write instructions in this leaf; the affected actual INC classification was already controlled in the prior grid package. No new general observer/disposition/reporter is introduced.

Reproduce the retained evidence reduction from repo root:

```
Collaboration/Tools/analysis/venv/Scripts/python.exe "Database/FFXII TZA/_experiments/evidence/native-preset-selector-coupling/check.py"
```

Limits: valid stable table memory, writable target disjoint from tables/mode byte, normal entry ABI, no intervening callback. General overlap safety, native object ownership/initialization, caller occurrence, mode changes, presentation, scalar meaning and system assignment are not established. FABLE semantic and OPUS ABI/contract consumers must review and assign the actual context before canonical naming. Independent SPEC acceptance is separate from producer controls, frozen integrity and sent requests. Published inputs/results remain immutable.

Cleanup: read-only reference, existing committed evidence and tools; owned W/E changes only. PC OFF, no FF12/input/memory instrumentation/save/config/reference/peer consumer writes. S19's spent setup allowance and unapproved extension persist. Full L1+L2 database NOT_MET; L3 later.

Player view: the code has a linked default: leaving the third choice negative can load values associated with the second choice. We have not yet identified which player-visible setting or object uses this routine.
