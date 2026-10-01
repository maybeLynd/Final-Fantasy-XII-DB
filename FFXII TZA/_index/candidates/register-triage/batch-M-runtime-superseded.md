# Register batch M: two more runtime rows closed SUPERSEDED (FABLE, Claude Opus 5.5, 2026-09-26)

This uses batch E's rule, which is `check_questions.py`'s own: a runtime row closes SUPERSEDED when its claim is already
tier-1 static, and its status names where the live remainder is carried, or says "not queued".

| row | static claim (tier 1) | live evidence or remainder | carried by |
|---|---|---|---|
| F-1 | Every in-image path to the weather apply `0026D910` starts at one of three application entries on the main-loop thread: GameApplication's setup (`0017D000` via `0017D150`), its update slot `0017CCD0` (with `MainLoop_UpdateAndRenderFrame` on the paths), and the `setweatherslot` verb `003565C0`. A forward walk from all eleven thread procedures the image starts reaches none of them, and the path takes no lock (weather contract). Control: `_index/candidates/f1-weather-apply-thread/f1_thread_reach.py` (3 checks). | The receiver-safe live call the row asks for. Blind spot: indirect thread starts, as on the handshake page (CG-3). | not queued |
| CI-1 | The header requests: `DllCharacteristics 0x8120`, with `NX_COMPAT` set and `DYNAMIC_BASE` clear (the hardening page). | **ASLR, observed live:** four launches across both test clients log `Module base: 0x120000`, the preferred image base. These are the mod loader's `hook.log`, `hook.pre_B1R1_live_20260826T145518.log` and `hook.valid_abort_persistent_20260826T145518.log` in TestClient1, and `hook.log` in TestClient2. **DEP:** the page protection of the data sections was not observed. | not queued |

Evidence classes are kept apart. F-1's claim is static. CI-1's ASLR half is a live observation from the mod loader's
logs, which sit in the test clients and not in this repository. Its DEP half has no observation.
