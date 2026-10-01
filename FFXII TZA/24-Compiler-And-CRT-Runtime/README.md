# Compiler and CRT Runtime

**Engine category.** MSVC CRT, exception handling and unwind machinery, thunks, Control Flow Guard, and compiler-generated C++ lifecycle code.

| | |
|---|---|
| Classification source | CodeDomain: CompilerGenerated* / Microsoft / Thunk |
| Functions | ~5,150 |
| Status | see [`../_index/COVERAGE.md`](../_index/COVERAGE.md) |

## Systems in this category

- [`Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md`](Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md) —
  **DOCUMENTED, tier 1.** The most actionable page in the database for hooking FFXII: fixed
  `ImageBase 0x00120000`, **ASLR off**, **CFG compiled in but shipped disabled** (the check is
  `ret 0`, the dispatch is `jmp rax`), DEP and `/GS` cookies genuinely enforced.

- [`Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md`](Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md) —
  **DOCUMENTED, tier 1.** 1,172 initializers run before `main`; **zero TLS callbacks.** Answers
  "when is it safe to touch engine state?" — and closes S-1 and S-4. **Reopened and corrected
  2026-09-02 (section 12):** its "117 lazy magic statics" was a tag-population count, not a
  census. The mechanism count is **1,681 statics at 1,732 guarded sites across 707 functions**.

- [`Lazy-Static-Initialization/lazy-statics-and-the-one-time-init-lock.md`](Lazy-Static-Initialization/lazy-statics-and-the-one-time-init-lock.md) —
  **DOCUMENTED, tier 1, one falsification pass.** The **1,681 objects FFXII builds on first use**,
  three quarters of them PhyreEngine's own type metadata, all behind **one** `CRITICAL_SECTION`.
  Contains the hazard that matters most to this project: a detour that leaves a guarded region
  without reaching `_Init_thread_footer` strands the guard at `-1`, and every later thread waits
  on it **forever, 100 ms at a time** — a silent hang on a loading screen, no crash, normal CPU.
  Also: how to find the stuck guard from outside the process, and how to read the guards as a
  free startup trace.

- [`Cxx-Runtime-Families/object-construction-destruction-and-static-lifetime.md`](Cxx-Runtime-Families/object-construction-destruction-and-static-lifetime.md) —
  **DOCUMENTED, tier 1, one falsification pass.** The category's four remaining families —
  `CompilerGeneratedCpp` 417, `CxxObjectLifecycle` 226, `CxxStandardLibrary` 167, `Microsoft` 106,
  **916 functions** *(GN161; R109 added one `CxxObjectLifecycle` member)*. Seven mechanisms re-derived from the image, **all scoring 100 %**: the
  **deleting-destructor idiom** in both its spellings (226/226), the **1,172-entry CRT registration
  table** (90/90 and 11/11), the **lazy-static guard** (117/117 and 23/23) and **vtable install**
  (60/60, 25/25). A deleting destructor also gives you `sizeof` for its class. One label,
  `CxxStandardLibrary.NativeQualified`, is called out as unsupported by its own name.

- [`Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md`](Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md) —
  **DOCUMENTED, tier 1, one falsification pass.** Answers open question **B-2**: of the 3,895
  functions tagged `CompilerGeneratedEH`, **3,893 are genuine funclets, 2 are not, and 6 genuine
  ones are missing from the tag.** Also the complete EH configuration (`__CxxFrameHandler3`
  4,377 · `__GSHandlerCheck` 5,372 · `__C_specific_handler` 9), and the **1,545 unwind funclets**
  that release a lazy-static guard when a constructor throws.

**Composition of this category** (by CodeDomain tag): EH unwind funclets 3,813 · Runtime.Callback
402 · StaticIntrusiveListTeardown 224 · ContainerAllocator 168 · StaticLifetimeInfrastructure 145 ·
CFG StaticGuardAdapter 145 · ThreadSafeStaticRecordAccessor 117 · StaticObjectInitializer 90 ·
ScalarDeletingDestructor 88 · Container 88 · remaining ~3,800.

## How to add a system here

1. Copy [`../_templates/SYSTEM.md`](../_templates/SYSTEM.md) into a descriptively-named
   subfolder (or as a `.md` file if it is a single mechanism).
2. Fill all eight sections. A missing section means `STUB` or `PARTIAL`, never `DOCUMENTED`.
3. Mirror every "What is not known" entry into
   [`../_index/OPEN-QUESTIONS.md`](../_index/OPEN-QUESTIONS.md).
4. Register any cross-subsystem chain in
   [`../_index/CALL-CHAINS.md`](../_index/CALL-CHAINS.md).
5. Obey [`../_index/EVIDENCE-STANDARD.md`](../_index/EVIDENCE-STANDARD.md).
   No banned evidence class, ever.
