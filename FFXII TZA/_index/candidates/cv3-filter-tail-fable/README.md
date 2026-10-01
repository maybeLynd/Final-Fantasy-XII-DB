# CV-3: the crash filter's tail, in order (FABLE, Claude Opus 5.5, 2026-09-28)

**Requests:** ASTRA-REQ-FABLE-NATIVE-FILTER-TAIL (81) and ASTRA-REQ-FABLE-NATIVE-FILTER-RESOURCE (82). Evidence:
- ASTRA's `_experiments/evidence/native-exception-filter-tail/` and `native-filter-message-resource/`;
- OPUS's [`native-filter-abi-opus`](../native-filter-abi-opus/README.md) (08728b024), which carries the ABI and the ATL module
  (`CAtlBaseModule`) behind the text lookup.

The consumer is FABLE's own 2026-09-14 CV-3 answer on
[what the game asks Windows for](../../../24-Compiler-And-CRT-Runtime/Runtime-Service-Surface/what-the-game-asks-windows-for.md).
It had the tail in the wrong order and stopped at the text lookup.

**Evidence class:** static. [`filter_tail.py`](filter_tail.py) ([output](filter_tail.out)) checks O, I and S, FAILS 0. It reads
the certified image only.

- **O, the order after the dump:**
  1. `CloseHandle`, then `SysFreeString(NULL)`.
  2. Text `0x7837` through `0019A510`.
  3. `SysAllocStringLen(ptr + 2, count)` when the text is found.
  4. `ShowCursor(1)`.
  5. `MessageBoxW(NULL, text, L"error", 0x10)`.
  6. `SysFreeString(text)`.
  7. Return 1.

  A gate of 0 returns 1 straight after `GetCurrentThreadId`. The call positions reject the page's old order, `ShowCursor` before
  the text.
- **I:** the three OLEAUT32 slots are ordinals 6, 4 and 6: `SysFreeString`, `SysAllocStringLen`, `SysFreeString`.
- **S:** the caption at `008F3DC0` is `L"error"`. String `0x7837` (block `0x784`, entry 7) is in all nine language copies;
  English is "Fatal error encountered." (24 code units).

**Not claimed:**
- which language copy the lookup picks at run time;
- that the box is shown;
- what the OS does after `EXCEPTION_EXECUTE_HANDLER`: the page states only the documented meaning;
- the cause of any observed crash (EXP-127 stays as its owner left it);
- the "no writer" of the gate `01F40128`, which is the 2026-09-14 static claim, unchanged.

**Consumer check.**
affected: `24-Compiler-And-CRT-Runtime/Runtime-Service-Surface/what-the-game-asks-windows-for.md` (the CV-3 bullet "`0079AD50` is the
filter").
corrects: "It then closes the file, calls `ShowCursor(1)` (`0079AE0E`) and loads text `0x7837` (`0019A510`). What it shows and how it
ends were not followed past that point."

| consumer | action | agreement |
|---|---|---|
| runtime-service page, CV-3 bullet | old sentence struck; the full tail in order, the message box, return 1, the gate-0 path | revised-here |
| `image-hardening-cfg-aslr-dep-and-stack-cookies.md` ("the crash filter `0079AD50` calls the resource lookup `0019A510`"; the fast-fail paths never reach the filter) | consistent | agrees |
| `OPEN-QUESTIONS.md` CV-3 row (installation, gate, dump type) | states nothing about the tail | agrees |
| OPUS `native-filter-abi-opus` (`atl_filter.py`) | the same order, imports and resource | agrees |
| ASTRA packages 81 and 82 | the same order, branches, ordinals, caption and text | agrees |

Regression: `filter_tail.py` O, I, S. O derives the call order from the decoded calls, so it rejects the old ShowCursor-first
order. run: filter_tail.py at de2871230, FAILS 0.

## Addendum: the lookup's receiver and what the selector checks (FABLE, Claude Opus 5.5, 2026-09-28)

**Requests:** OPUS-NOTICE-FABLE-CV3-ATL-MODULE; ASTRA-REQ-FABLE-RESOURCE-PREFIX-BOUNDARY (83).

- **Receiver.** OPUS's M and N are cited on the page, not re-derived here: `02EAF320` is ATL's `CAtlBaseModule`, and with no
  static writer of its instance array only the game image's resources are searched.
- **P, selector `0019A5B0`.** Its walk compares only the current pointer with the end (`0019A610`, `0019A625`). A zero count
  gives NULL (`cmove`), and otherwise it returns the length-prefix pointer. No instruction checks `prefix + 2 + 2*count <= end`.
  - Model: a 16-byte resource whose entry 7 has count 1 at offset 14 still returns 14; a full-span model returns NULL.
  - The shipped nine strings are whole (S), so the qualification changes no shipped outcome. It removes a guarantee the page
    must not imply.
  - What Windows does with a malformed resource is not claimed.

| consumer | action | agreement |
|---|---|---|
| runtime-service page, CV-3 step 2 | receiver (OPUS M/N) and the selector's prefix-only check stated; "if found" replaced | revised-here |
| OPUS `native-filter-abi-opus`, ASTRA packages 82/83 | the same receiver and selector branches | agrees |

Regression: filter_tail.py O I S P (P rejects the full-span model). run: filter_tail.py at 2f8dac6d7, FAILS 0.

## Addendum 2: the receiver claim is conditional (FABLE, Claude Opus 5.5, 2026-09-29)

**Request:** OPUS-REQ-FABLE-CV3-N-CONDITIONAL. OPUS qualified its N in `native-filter-abi-opus` (23269643e): a missing
static writer supports only a **conditional** main-image lookup. It holds provided the constructor ran and no computed
write fills the array. CV-3 step 2 now carries that condition, and it states that actual initialisation and live
behaviour are not established.

| consumer | action | agreement |
|---|---|---|
| runtime-service page, CV-3 step 2 receiver sentence | the condition added | revised-here |
| OPUS `native-filter-abi-opus` N (corrected 2026-09-29) | the source of the qualification | agrees |
