# Consumer check: the EASTL allocator's "attribution by name" corrected (OPUS, 2026-09-30)

- **Corrects:** "the shipping game retains the ability to attribute allocations by name", with its two follow-ons (the
  modding note's "free attribution", and §10's "can attribute allocations per container kind").
- **Affected:** 23-Third-Party-Libraries/EASTL/eastl-strings-containers-and-the-logging-allocator.md. The same publish
  also corrects the "20 callers" count on that page.
- **Correction:** the constructor `001EDF00` never reads the name argument (BS-6, answered 2026-09-14), so the build
  cannot attribute allocations by it.
- **Consumers:**

  | consumer | state |
  |---|---|
  | the EASTL page, §2, §6 and §10 | revised-here |
  | the EASTL page's "20 callers" | revised-here: 17 functions, 669 sites |
  | the-ordered-container-runtime.md | agrees: it cites `eastl::allocator_memory_log` only for the library identification, never attribution |
  | rtti-vtable-object-model.md | agrees: its "attributed" is about vtable slots, not allocations |
  | _index/OPEN-QUESTIONS.md BS-6 | agrees: it is the row that answered "the name is not kept" |
  | _index/AUDIT-LOG.md line ~12038 | history, not a current claim; left as dated history |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-dd-eastl-0930/eastl_dd_check.py, N1 and F2. Run verified at
  3dac81ee9 (worktree at HEAD 3dac81ee9, FAILS 0).
