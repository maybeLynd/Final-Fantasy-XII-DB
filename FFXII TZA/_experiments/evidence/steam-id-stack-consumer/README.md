# ASTRA — original returned-stack text consumed by the native Windows formatter

Question: UQ-146 on the keymap/settings-path page. Does the installed native CRT
overwrite the text that `001F3ED0` returns in its released stack frame before the
next original formatter consumes it? Consumers: FABLE's UQ-146 semantic account,
OPUS's input/platform path boundary. This is **Method B**, isolated shipping-code
execution with the native host CRT, not the live game.

The existing matching account folder cannot distinguish correct current execution
from a copied or older artifact. The competing explanations tested here are intact
consumption of a supplied ID versus corruption during this bounded caller/formatter
sequence. No new game session, Steam API call, directory creation or PC control was
needed. Actual initialization and normal startup remain outside the experiment.

## ASTRA result and player meaning

On `ucrtbase.dll` **10.0.26100.9444**, SHA-256
`5c52e3a303baaac0e0af8bd9b96134993da34bc9d834a31ef37e1d2cdc7fe192`, the tested
17-digit ID and the 20-digit unsigned-64 maximum were both consumed intact when
the supplied printf-options word was **4**. The alias was exactly **0x220 below
the caller's RSP**. Stable-ID controls produced the same complete output.

The original pointer is still dangling. This result does not make its lifetime
valid, predict other CRTs/stacks/callers or establish real FF12 startup options.
It refutes an unconditional claim that this specific formatter necessarily destroys
these supplied strings on this host.

Player version: the game hands its settings-path formatter account-ID text kept
in temporary stack space. In this test the full ID survived. Deliberately changing
that temporary text changed the resulting path, while retaining a stable copy
prevented that effect. This is a concrete compatibility observation, not proof
that every Windows version or game startup handles the pointer safely.

An additional prerequisite matters: with the supplied options word **0**, even
the stable control produced `C7`, consuming the first narrow character of each
wide string. Option **4** is `_CRT_INTERNAL_PRINTF_LEGACY_WIDE_SPECIFIERS` in the
pinned local SDK. `reference.json` records that definition and the zero-initialized
image storage, not the actual initialized game value. Canonical preparation must
name this state rather than saying only "the installed CRT".

## ASTRA exact executed boundary and interventions

Reference EXE SHA-256:
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
The child maps the image at its original **00120000** base, preserving the measured
instructions and their relative addresses. Before/after checks cover the retained
original ranges. Original instruction bytes and complete disassembly are in each
accepted `before.json`; executable sections are made read/execute before invocation.

1. An explicit staging thunk supplies the **post-format string state** in a
   `0x248` helper frame, including the cookie expected by the original epilogue.
   It enters shipping code at **001F3F52**, which returns the pointer at stack+30
   through the original cookie check **00808C40**. The helper's earlier Steam,
   `%llu` formatting and logging are **omitted**, not stubbed effects credited as
   native initialization. The selected input is decimal text of a valid u64;
   the maximum-value control is a formatting boundary, not a real Steam account.
2. A copy using volatile registers records the returned 512-byte window without
   making another call or changing RSP. The stable control substitutes its
   retained input buffer for the returned alias. The clobber control explicitly
   changes the alias's first UTF-16 code unit to `X` after this before snapshot.
3. Original **00197F7A..00197F92** stages the actual formatter arguments and calls
   **00194EF0**. That complete wrapper executes its original options getter
   **0016D670** and calls the host `__stdio_common_vswprintf_s` through **008C2E88**.
   The original format at **008F38C0** is **`%s%s`**. The prefix is supplied at the
   caller's stack+30 and is both the first source and the destination, matching
   this caller fragment's aliasing. No new format is substituted.
4. A jump at **00197F93**, outside that measured fragment, returns to the recorder
   before the next directory-creation call. The recorder preserves the formatter
   return, resulting text and post-return alias window, restores its frame and
   nonvolatile register, and returns a sentinel to Python.

For observed arms, the IAT points through a small tail-call shim that copies the
second vararg's source window immediately before CRT entry. Its decoded instructions
use no push/pop/call or RSP write and change only volatile registers; it leaves
floating-point state alone. It is an **intervention**. Stable and alias direct-call
comparisons produce the same outputs without it; that is a bounded observer control,
not universal transparency. There are no breakpoints, exception hooks or thread
context operations in this experiment.

At CRT entry the captured varargs pointer equals caller-RSP+10, and CRT-RSP equals
caller-RSP-58. The second argument points either at the original returned alias or
the explicit stable buffer, as selected. These checks prevent reading the wrong
argument or calling the stable control an alias observation.

## ASTRA observations, controls and limits

Only **`verified-*`** directories supply accepted observations. `observation.json`
normalizes their raw `native.bin`, `before.json`, cleanup and process receipts.

| Supplied state | Result |
|---|---|
| Wide option4, 17-digit ID, original alias | Complete ID appended; direct and observer arms agree |
| Wide option4, stable 17-digit ID | Same output; direct and observer arms agree |
| Wide option4, alias explicitly changed to `X6561198045890736` | Changed first character reaches output |
| Same explicit alias overwrite, stable ID argument | Original ID reaches output |
| Wide option4, maximum u64 text `18446744073709551615` | Complete text through alias and stable control |
| Option0, stable wide ID | `C7`, in both direct and observed arms |

The **entire 512-byte window is not preserved**. In accepted non-clobber alias
arms, the earliest changed byte before CRT entry is **+1C8**; after the formatter
returns it is **+170**. Both are beyond the tested 17/20-digit text and terminator.
The raw offset lists remain in the normalized record. Do not call this whole-buffer
preservation or attribute every changed byte to a particular internal CRT instruction.

Boundary snapshots and the resulting formatted string establish consumption of
these tested values. They do not record every intermediate CRT load/write or prove
that no transient overwrite occurred and was restored. Stack addresses and input
state are controlled, not observations of real game initialization or scheduling.
The current host DLL is identified by its loaded path and before/after file hash;
this is not a full loaded-module/page/IAT census of an FF12 process.

`check.py` is read-only by default. It independently checks expected text, alias
distance, observed varargs identity, option state, output/return, native-parent
relationship, source versions and cleanup. Six corrupted receipts are rejected:
failed cleanup, wrong native parent, changed initial ID, wrong observed alias,
narrow output promoted to wide, and an erased clobber label. Empty data, missing
receipts or truncated native buffers cannot pass.

## ASTRA retained failures and restoration

`feasibility-stable-shim` failed the exact format-literal guard **before execution**:
the first design incorrectly selected the adjacent `%s\%s` literal. Its original
sources, stderr and cleanup are retained. All three allocations were released;
the child exited1, no native result exists, and this run stays invalid.

The first ten native folders retain useful raw observations but their process
receipt named the Python launcher without recording its relationship to the native
Python child. The checker caught the PID mismatch; none was promoted by deleting
the assertion. `pre-ownership-source` preserves that version. The corrected wrapper
records the native parent PID and actual executable path: on this host the child
is `C:\Python314\python.exe` and its parent is the Popen-owned launcher. All affected
arms were rerun as `verified-*`; a wrong-parent regression control now rejects the
same missing identity relationship. `observed-source` preserves the earlier source
used before clobber/length controls were added. Each plan pins its exact source.

All accepted native children and their launchers exited0; no timeout or forced kill
occurred. Each child released all three allocations and reported no debugger.
No save/config/reference file was modified and no game process or PC control was
used. The historical FF12 restoration receipt is unchanged, not re-verified here.

Next consumer action: incorporate the **tested CRT/entry/state condition**, preserve
the static dangling-pointer fact, and resolve the actual printf-options initializer
through cheaper original-code evidence if possible. Further live work needs a
remaining claim that depends on real startup. This package is not whole-game L1/L2
completion and does not start reconstruction or L3 parity.
