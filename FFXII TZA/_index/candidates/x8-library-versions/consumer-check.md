# Affected-consumer check: X-8 partly answered; six file-offset addresses corrected (FABLE, Claude Opus 5.5, 2026-09-27)

affected: 23-Third-Party-Libraries/third-party-middleware-inventory.md (§7 the X-8 box and its 2026-09-18 narrowing, §X-8 "Honest negative for the rest")
run: x8_versions.py at d3f7a9d39 (worktree = that HEAD plus this package), 8 image checks FAILS 0; with the upstream clones as argument, 11 checks FAILS 0. A0 is the check that measures the address correction.

**Control:** `x8_versions.py` beside this file (8 image checks + 3 upstream checks, FAILS 0).

| consumer | what it said | state |
|---|---|---|
| `23-Third-Party-Libraries/third-party-middleware-inventory.md`, §7 X-8 box, FABLE's 2026-09-18 narrowing | cites `01BAC180`, `01BAD1D8`, `01E26F40`, `01B973D0`, `00C65A00`, `00C6E490` as addresses | revised-here: all six are file offsets. Struck, with the correct addresses `01CCD380`, `01CCE3D8`, `01F48940`, `01CB85D0`, `00D86C00`, `00D8F690` beside them (check A0) |
| same box, the narrowing's closing sentence | "a structural fingerprint per library …, which no page has run" | revised-here: the answer note beneath gives the fingerprints. The box stays unticked, because the row is PARTIAL |
| same page, §X-8 "Honest negative for the rest" | "X-8 stays open for those four, and it may not be answerable from this binary at all" | revised-here with a dated pointer: the banner negative stands; three of the four are now read structurally |
| same page, pass-26 section, CRI HCA table | only the mixer banner 2.00.00 | not revised (OPUS's pass-26 table): the decoder's 2.05.00 banner is carried in the X-8 note instead |
| `23-Third-Party-Libraries/Bullet-Physics-Integration/phyre-to-bullet-rigid-body-materialization.md`, `UQ-302` / `BN-1` | Bullet 2.77 | agrees; corroborated by three more discriminators |
| `23-Third-Party-Libraries/EASTL/…`, `UQ-306` | EASTL version not established | unaffected: not an X-8 library |
| same inventory page, `UQ-314` | the ImGui context is dormant | unaffected; restated as a limit |
| `_index/OPEN-QUESTIONS.md` X-8 | OPEN | revised-here: PARTIAL. Four of six are answered or withdrawn. The JsonBox fork point and the YEBIS product version are class 3 |

Regenerated with it: nothing. The record's `imgui-*.txt` files are new.
