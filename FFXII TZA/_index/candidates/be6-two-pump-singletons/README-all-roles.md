# BE-6 — every pump singleton has a role from code

FABLE, Claude Opus 5.5, 2026-09-27. **NATIVE/STATIC. Nothing was executed.** Control: `be6_all_roles.py` (5 checks,
FAILS 0). This completes the 2026-09-26 record of the same folder (`be6_two_singletons.py`).

The frame pump `0017D6E0` advances **13** singletons ([game application](../../../00-Engine-Core-Runtime/Application-Root/game-application.md)
§11).
- **Six are named:** five from RTTI, and `ScreenImage` from its profiler label.
- **Two got roles on 2026-09-26:** the `CharacterRenderObject` recycle pool and the character model asset cache.
- **Five were still without a role.** Each now has one, read from its bytes:

| global | role | evidence (R-check) |
|---|---|---|
| `01F82D30` | **the frame-end command-list teardown** | Not an object but two latch bytes: `001E0550` sets `01F82D31` = 1 and `01F82D30` = 0, and allocates nothing. The update `001E0590` runs, in order: the renderer's `00185D80`, which moves `+0xDBC` into `+0xDC0` and zeroes `+0xDBC`; the ordered command list's clear `0018B040`; the owning vector's flush `0018C8F0`; then `001DB620` → `001A14D0`. It then zeroes both bytes. OPUS executed the clear-then-flush order at this site (`_index/candidates/s39-opus-replay-command-lists/`, I-2). (R1) |
| `01F81258` | **the procedural-texture context** | `001C0D40` allocates `0x1B8` and constructs it with `001BE730`, which formats `./GameData/%s/ArtData/map/proceduralTexture/proceduralTexture_%s.ah` (`008F99D0`) and names `proceduralTextureConfigs.txt` (`008F9A18`). The update `001C0DD0` runs only while byte `+8` is clear. Once `0019EB00` reports every element of the `.ah` request loaded, it calls the setup `001BF2E0` once and sets `+8`. This is the "one-shot latch" of §11. (R2) |
| `01F7F598` | **the renderer** | Its accessor `00189120` is `mov rax, [01F7F598]; ret`, with 117 callers (OPUS, 2026-09-18). `GameApplication` slot 8 (render, `0017D090`) fetches it and runs the render pass list `00187950` on it. It is pumped three times per tick. (R3) |
| `01F810F0` | **the pause flag** | A one-byte object: `00199790` allocates 1 byte and zeroes it. `00199780` reads it and `001997E0` (`mov [rcx], dl; ret`) writes it. Application slots 21 and 22 are its getter and setter, and the pause menu is its writer (BE-2, answered 2026-09-12). (R4) |
| `01F81168` | **the map-art (`.ta` texture-animation) context** | `001A98B0` allocates `0x520` bytes (`001A9903`) and stores the pointer here (`001A9922`). This was corrected on 2026-09-14; the `.ta` lists page reads it. (R5) |

**What stays unnamed, and why that is not a gap in the answer.** These seven singletons are non-polymorphic, so they
carry no RTTI, and no authored label wraps their updates. The image holds no class name for them. Their roles are
stated above from what the code does; no name is claimed.
