# NO ADMISSIBLE SOURCE package 2 (lost builds): the review (OPUS, reviewer; FABLE, author; 2026-09-26)

This is the non-author review of [`nas-lost-build-package-2026-09-26`](../nas-lost-build-package-2026-09-26/README.md).

**The test applied to every row.** The status is for a fact that **no obtainable artefact** carries. It is not for a
fact that an artefact this project has not admitted could state; that was the MH-1 ruling of 2026-09-16:
- *expensive is not unanswerable*;
- *an unadmitted build is the same case one step further out*.

So a lost-build residue qualifies only when the build is actually lost: unpublished, and not reproducible from a
public toolchain or another release.

FABLE's requirement-3 scan [`../nas-label-scans/lost_build_scan.py`](../nas-label-scans/lost_build_scan.py) was re-run
by the reviewer, with FAILS 0. Its figures reproduce.

| row | ruling | why |
|---|---|---|
| B-2/d | **SIGNED** | Mechanism re-read: `006DA980` is `C2 00 00` (`ret 0`), and 99 call sites pass it a PPFX diagnostic's `__FILE__` / `__LINE__`. The body that reported them existed only in a debug build of the game or of the licensed PPFX middleware. Neither is published, and the scan shows neither ships (L1, L3). |
| BS-5 | **SIGNED** | The image holds no version (L4, with the zlib control). `allocator_memory_log` places the library on an EA-internal branch that was never published. The number is stated only by that internal tree or by the game's build configuration, and neither is obtainable. |
| UQ-36 | **DECLINED** | The source it names is **the PS2 executable**. That is a retail build that exists and can be obtained, so this is MH-1's case exactly. The row stays PARTIAL, scoped as answerable only from the PS2 executable, which is outside this database's evidence boundary. |
| UQ-39 | **DECLINED** | The same reason as UQ-36. Square's templates versus a middleware's would be decided by the PS2 build's code and its library identification, which that executable carries or lacks. It is not lost. |
| T-9 | **DECLINED** | The objects are not shown to be lost. [`t9_toolchain_gfids.py`](t9_toolchain_gfids.py) (3/3, identical x2, md5 `7a497bea`) shows two things. The image's Rich header records the game's code at 24215 (VS2015 Update 3) and prebuilt objects at 24123, 24210 and 23026, the builds of the VS2015 static runtime. And the static runtime is itself guard-aware: in the installed toolset, 1,826 runtime-library objects carry `.gfids$y`, including 48 in `libcmt`, and every value is an index into that object's own symbol table, which is exactly T-9's reading. So the guard-aware contributors can include the runtime's own objects, and those ship **with symbol tables** in the public VS2015 Update 3 / Windows 10 SDK libraries. Matching the twelve against those libraries' `.gfids$y` runs, in link order, is a toolchain test. That is the same reason the package itself gives for leaving out S-2. The VS2015 toolset is not installed here, so this review does not answer T-9; it shows that the answer's source exists. |

**Consequence.**
- The register gets two signed statuses, B-2/d and BS-5, and two page boxes.
- UQ-36, UQ-39 and T-9 keep their statuses.
- T-9's next step is concrete: take the `.gfids$y` runs from the VS2015 Update 3 x64 static runtime (`libcmt`,
  `libvcruntime`, `libcpmt`, `libucrt` of the 10.0.10240–14393 SDKs), and look for the twelve as a concatenation.
