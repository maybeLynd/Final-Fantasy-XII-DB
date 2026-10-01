# B-2/c: the 136 magic statics without an `_Init_thread_abort` funclet, verified one by one (OPUS, 2026-09-26)

**Evidence class: STATIC. `live_game: false`.**

**The question.** The funclet page says the 136 lazily-built statics with no `_Init_thread_abort` funclet are the ones
whose construction cannot throw, but it only assumed this; B-2/c asked for each one to be checked. `check.py` checks
each one: for every construction site, it takes the code from `call _Init_thread_header` (`008092FC`) to that site's
own `call _Init_thread_footer` (`0080929C`), and follows every call in it to the end of its direct-call and tail-jump
closure.

**5 / 5 pass. `run_output.txt` is byte-identical over two runs; `result.json` md5 `7ce2ec8edcfee9295570cbb9554b1729`.**

| case | observed |
|---|---|
| `C1` | The population reproduces from the image: **1,732** header sites and **1,681** guards. **1,545** guards have an abort funclet and **136** do not. |
| `C2` | Every site of every one of the 136 reaches its own footer. The footer is matched by the last `lea rcx, [rip+guard]` before it. |
| `C3` | **None of the 136 can reach a C++ throw or an unresolved call.** **103** construct with no call at all; the other **33** call only code whose whole closure is resolved and throw-free. |
| `C4` | **Control.** The same code, run over the 1,545 funclet guards, finds that **947** reach an unresolved call. It finds none among the 136. |
| `C5` | The one indirect call in any of the 136 closures is named from the bytes. `_Init_thread_wait` (`008093C0`) calls through `call rbx` (`0080940B`), using the pointer that `00809130` stores at `[02EAED78]` (`008091E0`), rotated and XORed with the security cookie. That pointer is `GetProcAddress(…, "SleepConditionVariableCS")` (the `lea` at `00809170`), a Win32 wait. |

**What the 33 call.**

| n | calls in the construction region | what reaches |
|---:|---|---|
| 24 | `00808B90` only | `_crt_atexit` / `_register_onexit_function`: the static's destructor is registered, and nothing else happens |
| 6 | another magic-static accessor (`005CDA30`, `005D8D70`, `005D8CA0`, `00637800` ×2, `006316C0` + `00808B90`) | a nested magic static. Its closure is `EnterCriticalSection` / `LeaveCriticalSection` / `SetEvent` / `ResetEvent` / `WaitForSingleObjectEx`, plus `_Init_thread_wait` (C5) |
| 1 | `0075F410` + `00808B90` | atexit only |
| 1 | `LoadLibraryA` | Win32 |
| 1 | `GetProcAddress` ×3 | Win32 |

**Classification rules.**
- An import raises a C++ exception only if it is `_CxxThrowException` or one of msvcp140's `?_X…` helpers.
- Any other msvcp140 import is unresolved, as is any indirect call.
- vcruntime `mem*` / `str*`, the UCRT and Win32 are C functions and raise no C++ exception.
- Imports are resolved through their IAT slots and through the image's `jmp [IAT]` thunks. `_CxxThrowException` is
  such a thunk at `00861ECC`.

**What it also shows, about the other side.** **598** of the 1,545 funclet guards are statically throw-free by the same
test. So a funclet records the compiler's assumption from declarations (any call not known to be `noexcept` may throw),
not a construction that can actually throw. The page's direction holds (no funclet → cannot throw), but its converse
does not.

**Not covered.** SEH faults inside a constructor are not C++ exceptions and are outside `/EHsc` unwinding, so they are
outside the question.

**C4's threshold was revised once, openly.** It was first written as "at least 1,000 unresolved" while
`_Init_thread_wait` still counted as unresolved, when the figure was 1,290. With that call named (C5), it is 947. The
case is now the contrast itself: a majority of the control, and none of the 136.

**Run:** `python check.py` (a few minutes). It needs `Tools/work/exe/FFXII_TZA.exe` and `Tools/work/graph/functions.tsv`.
