---
system: The runtime service surface — what the game asks Windows for, and the diagnostics it still ships
category: 24-Compiler-And-CRT-Runtime
status: AUDITED
owner_layer: CodeDomain:CRT.RuntimeServices; no PrimaryOwner
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 19 cited function entries, 0 of them among the 109 records that changed GN160 -> GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0), established for this document 2026-09-14 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  project: work/headless_gn160/GFZ_GN160, CHECKPOINT VERIFIED 2026-09-07
last_reviewed: 2026-09-07
audit:
  passes: 1
  last_pass: 2026-09-07
  last_pass_state: GN160-xiionline-61-self-attack
  last_pass_kind: attack
  crossref_clean: true
  reopened_count: 0
---

# The runtime service surface

> **The shipping game still talks.** Attach a debug viewer to FFXII: The Zodiac Age and **253
> functions narrate what they are doing** — the whole audio engine and the whole post-processing
> library, live, in a retail build.
>
> **And it still writes crash dumps.** The symbol machinery, the stack walker and the minidump
> writer are all present *and all reachable*.

## 1. What the player sees

Nothing, unless they go looking. But for anyone modding the game, two facts change what is possible.

**The game narrates its own failures.** Sound and post-processing were built with diagnostic messages
naming the exact method that failed — *"IGPUDevice::CreateDevice() failed"*, and hundreds more — and
**those messages were never compiled out.** They go to the Windows debug channel, which any debug
viewer can read without a debugger attached and without modifying the game. **If a sound will not
play or an effect will not initialise, the game has already said why.**

**And when it crashes, it can say where.** The build carries the machinery to walk its own call
stack, turn addresses into function names and line numbers, and write a minidump.

The game asks Windows for surprisingly little else. **Text is not converted through Windows.** The
usual Windows call for turning bytes into characters is **not imported at all**; what conversion
happens goes through the C++ standard library instead. That matters to anyone editing text files:
the encoding contract is the game's own, not the operating system's.

## 2. Native mechanism

### The import surface

**30 DLLs, 538 imported symbols.** `iat_xrefs.py` reports **417 of those 538 slots reached by an
`FF 15` indirect call**, over **3,543 indirect call sites**.

| DLL | symbols | | DLL | symbols |
|---|---:|---|---|---:|
| `MSVCP140` | 115 | | `dbghelp` | **9** |
| `KERNEL32` | 110 | | `steam_api64` | 9 |
| `USER32` | 59 | | `ole32` | 6 |
| `api-ms-win-crt-stdio` | 45 | | `WINMM` | 4 |
| `api-ms-win-crt-math` | 45 | | `IMM32` | 3 |
| `api-ms-win-crt-string` | 31 | | `api-ms-win-crt-locale` | 3 |
| `api-ms-win-crt-runtime` | 24 | | `d3d11` | **2** |
| `VCRUNTIME140` | 21 | | `XINPUT9_1_0` | 2 |
| `ADVAPI32` | 10 | | `dxgi` · `D3DCOMPILER_47` · `DINPUT8` · `IPHLPAPI` | 1 each |

> **Two symbols from `d3d11`, one from `dxgi`, one from `D3DCOMPILER_47`.** The renderer barely
> touches Direct3D directly — PhyreEngine owns the device, and everything else goes through it.
> `MSVCP140` at 115 is the largest single dependency, which is a C++ standard-library bill, not a
> platform one.

The busiest imports by call site:

| import | sites | callers |
|---|---:|---:|
| `_invalid_parameter` | 434 | 80 |
| `LeaveCriticalSection` | 310 | 126 |
| `EnterCriticalSection` | 286 | 134 |
| `memmove` | 244 | 169 |
| **`OutputDebugStringA`** | **150** | **93** |
| `strstr` | 61 | 20 |
| `std::_Xlength_error` | 59 | 46 |
| `_stricmp` | 56 | 15 |
| `GetProcAddress` | 51 | 16 |
| `rand` | 48 | 30 |

`rand`'s 48 sites are the process-global CRT stream already documented in
[`../../21-RNG-And-Determinism/rng-streams.md`](../../21-RNG-And-Determinism/rng-streams.md).

### The debug channel — 253 functions, in two populations

**`OutputDebugStringA` has 150 direct call sites in 93 functions**, and that count is *misleading on
its own*:

| population | functions | sites |
|---|---:|---:|
| Audio (SEAD), calling the API directly | **90** | 147 |
| Steam callbacks (`PlatformOnlineAchievements`) | 2 | 2 |
| **the wrapper `006DF480`** | 1 | 1 |
| **callers of that wrapper** | **160** | **801** |
| | **253 total** | |

**The two populations do not overlap at all** — no function appears in both.

**`006DF480` is a printf-style logging wrapper.** It saves four register arguments to the shadow
space, formats into an **`0x800`-byte** buffer, and calls `OutputDebugStringA` at **`006DF4FA`**:

```asm
006DF480  mov  [rsp+8], rcx        ; the varargs home
006DF485  mov  [rsp+0x10], rdx
006DF48A  mov  [rsp+0x18], r8
006DF48F  mov  [rsp+0x20], r9
006DF4BF  mov  r8d, 0x800          ; buffer size
006DF4CC  call qword ptr [rip+...] ; format
006DF4FA  call qword ptr [008C2120]; OutputDebugStringA
```

> **Counting a subsystem's diagnostics at the API undercounts it by a factor of eight.** One wrapper
> stands between 160 functions and the call the census was looking for. **This is the same hazard
> [`../Thunk-Layer/the-thunk-layer-and-why-call-counts-disagree.md`](../Thunk-Layer/the-thunk-layer-and-why-call-counts-disagree.md)
> documents for thunks, in a different disguise** — there an extra `jmp`, here an extra `call`.

### ⚠ `H-3` answered: the renderer **does** narrate

[`../../17-Presentation-Rendering/Post-Processing/ppfx-function-identification.md`](../../17-Presentation-Rendering/Post-Processing/ppfx-function-identification.md)
asks whether PPFX/Yebis diagnostics reach `OutputDebugStringA` *"as SEAD's do — if so the renderer
narrates its failures live too."*

**They do.** Re-identifying PPFX functions by their diagnostic-string prefixes — `CPostEffect::`,
`IGPUDevice::`, `CRenderGlare::`, `TEXSHADERSET::`, `CRenderDepthOfField::`, `CRenderToneMap::`,
`IGPUEffect::` — gives **102 functions**, and

> **90 of those 102 call the wrapper at `006DF480`.**

The wrapper's 160 callers span `006DA8F0`–`00790160`, which contains the RVA `0x782289` that
document reports for PPFX. **`006DF480` is Yebis's own logging routine**, and the reason PPFX looked
silent is that it never calls the Windows API by name.

*The 102 here is a subset of that document's 135 — seven class prefixes against its twenty — so this
is a floor, not a re-derivation of its census.*

### The crash handler is present and reachable

`dbghelp.dll` contributes nine symbols: `SymSetOptions`, `SymInitialize`, `SymCleanup`,
`SymFromAddr`, `SymGetLineFromAddr64`, `SymGetModuleBase64`, `SymFunctionTableAccess64`,
`StackWalk64`, `MiniDumpWriteDump`.

**`005CCD00`** (926 B, tagged `Phyre.DebugUtils.AddressInformation`) is the symbolised stack walker:
`SymInitialize` at `005CCD57`, `SymFromAddr` at `005CCF0C`, `StackWalk64` at `005CCEB6` and
`005CCFE1`. **`MiniDumpWriteDump` is reached from `005CCB39` and `0079ADCA`** — the first in the same
`005CCxxx` neighbourhood as the stack walker.

> **Both were nearly published as dead.** A scan for `call qword ptr [rip+disp]` returns **zero**
> sites for `MiniDumpWriteDump` and **zero** for `GetAdaptersInfo`. Both figures are real and both
> conclusions would have been wrong: each import is reached through a **`jmp qword ptr [rip+disp]`
> import thunk** — `0080F2BC` for the minidump writer, `0078A968` for `GetAdaptersInfo` — and each
> thunk has two callers. **`data_xref_scan.py` matches both addressing forms and found them; my
> call-only scan did not.** The correct finding is the opposite of the first one: **the retail build
> ships a working crash handler.**

### Text does not go through Windows

- **`MultiByteToWideChar` is not in the import table at all.**
- `WideCharToMultiByte` is imported (slot `008C22D8`) with **2 call sites in 1 function**.
- `api-ms-win-crt-locale` contributes exactly three symbols: `setlocale`, `localeconv`,
  `_configthreadlocale`.

What *is* linked is the **C++ locale machinery** — `std::codecvt<char>` and `std::codecvt<wchar_t>`,
`std::ctype<char>`, `std::collate<char>`, `std::locale::facet` and the `imbue`/`getloc` pair, all
from `MSVCP140`. **Conversion goes through the standard library, not the Win32 codepage API**, and
the game's own text encoding — the control-code language in
[`../../16-UI/Text-And-Number-Rendering/the-text-control-code-language.md`](../../16-UI/Text-And-Number-Rendering/the-text-control-code-language.md)
— is not a Windows codepage at all.

## 3. Key addresses

| address | what |
|---|---|
| `006DF480` | the Yebis printf-style log wrapper; 801 sites from 160 functions |
| `006DF4FA` | its `OutputDebugStringA` call |
| `008C2120` | `OutputDebugStringA` IAT slot |
| `005CCD00` | Phyre symbolised stack walker, 926 B |
| `005CCB39`, `0079ADCA` | the two calls that reach `MiniDumpWriteDump` |
| `0080F2BC` | `MiniDumpWriteDump` import thunk (`jmp`, not `call`) |
| `0078A968` | `GetAdaptersInfo` import thunk |
| `008C22D8` | `WideCharToMultiByte` IAT slot |
| `008C3098` | `rand` IAT slot *(named in the RNG document)* |

## 4. Modding notes

- **Run a debug viewer and the game narrates.** No debugger, no patching. Audio failures come
  straight from SEAD; post-processing failures come through `006DF480`. **This is the cheapest
  diagnostic in the game and it costs nothing to switch on, because it is already on.**
- **To capture everything in one place, hook `006DF480`** rather than `OutputDebugStringA` — it sees
  all 801 post-processing messages with their format arguments still intact, before they are
  flattened into a string.
- **To silence the channel**, patching `OutputDebugStringA`'s IAT slot at `008C2120` catches all 253
  narrators at once, both populations.
- **The crash handler is live.** If you are chasing a crash, the game will already walk and symbolise
  its own stack — `005CCD00` is the function to breakpoint.
- **Do not assume an import is unused because nothing `call`s it.** Two of the most interesting
  imports in this binary are reached only by `jmp` thunks.
- **Text conversion is not Windows'.** Do not expect a codepage to govern the game's strings.

## 5. What is not known

- [x] ~~**What `006DF480`'s messages actually say.** Only **2 of the 150** direct sites pass a literal
  string in `rcx`; the rest format first, so the message text lives in the callers' format-string
  arguments and has **not** been extracted. `CV-1`.~~
  **CV-1 ANSWERED 2026-09-12 (FABLE): the channel is YEBIS's own log, and every message is now
  listed.** A function-list-independent `E8` index gives the wrapper `006DF480` **801** call sites;
  **797** load a literal format string into `rcx` / `rdx` before the call (4 pass a computed one),
  and they resolve to **385 distinct strings**, catalogued with their counts and owning functions in
  [`ppfx-diagnostic-strings.tsv`](ppfx-diagnostic-strings.tsv). They are all PPFX (YEBIS) diagnostics:
  the dominant forms are source-path prefixes with a build date — `..\src\GPU\GPUPostEffect.cpp(%d) :
  Feb 18 2016 PPFX ERROR: ` (113 sites), `…PPFX WARNING: ` (26), `…PPFX: ` (29), and the same for
  `GPUTextureUtil.cpp`, `GPUInterfaceDevice.cpp`, `TinyEffect.cpp`, `ppfx.cpp`, `GPUDepthOfField.cpp`,
  `GPURenderGlare.cpp`, `GPUInterfaceBuffer.cpp`, `GPUInterfaceSurface.cpp`, `GPURenderTexture(Array).cpp`,
  `ppfxRenderToTexture.cpp` — the prefix call is followed by the message call at the same site — plus
  the specific messages (`Invalid pGlobalParameter->m_eType: %d: %s`, the `IPfxBaseContext::
  Initialize() / Uninitialize()` banners, `CPostEffect::…` failure reports with `(0x%x: %s)`, the
  texture-allocation line `%s %s: %4d x %4d, %s (0x%04x), MSAA(%2dx, %2d), Usage 0x%08x, Flags
  0x%08x`). **The game's own code contributes nothing to this channel**: every owner lies in the
  YEBIS range `006DA8F0`–`00790160`, and the two literal `OutputDebugStringA` sites outside the
  wrapper are the only non-PPFX messages. The middleware's build date, **18 February 2016**, is
  stamped on 300 of the sites. `CV-1`.
- [x] ~~**What gates the channel at runtime.** Whether the wrapper checks a verbosity level or a
  global before formatting is **not read** — only its prologue and its `OutputDebugStringA` call
  were disassembled.~~ **`CV-2` ANSWERED 2026-09-12 (FABLE): nothing gates it.** `006DF480` (137 B,
  read whole) tests no level and no flag: it formats unconditionally — `__stdio_common_vsprintf`
  (IAT `008C2F08`, options `| 1`) into the 2,048-byte buffer `02EA0BA0` (`006DF4AC`–`006DF4CC`) —
  and then delivers the text through **a hook pointer at `02EA0B88` if one is installed, else
  `OutputDebugStringA`** (`006DF4E3`–`006DF500`). The hook slot is written by exactly one function,
  an 8-byte setter at `006DF3A0` that the function list does not contain (`mov [02EA0B88], rcx ;
  ret`, found by the gap-code operand index), and **no `E8`/`E9` site in the image calls that
  setter** — so in the shipped build the slot stays zero and every message reaches
  `OutputDebugStringA`. The channel is "already on" and not switchable from data; the only switch
  is code that calls `006DF3A0`, which a mod could do.
- [x] **When the crash handler runs.** `005CCB39` and `0079ADCA` reach the minidump writer, but
  neither containing function has been read, so whether it is wired to an unhandled-exception filter
  or only to an explicit developer call is unestablished. `CV-3`.
  *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (CV-3):* **a player's crash leaves a dump. The
  framework installs the writer as the unhandled-exception filter on every boot.**
  - **`0079AD50` is the filter.** `007980A0`, the framework startup ([what the engine fixes at boot](../../00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md)),
    loads its address and calls `SetUnhandledExceptionFilter` (`007980F0` `lea rcx`, `007980F7`). It is reached on every
    boot through `007A3770` from the CRT entry `00808D78`. In the filter, the gate `01F40128` has no writer and is `1` in the
    image, so it always runs. It records the current thread id and the incoming `EXCEPTION_POINTERS`, opens a file named by
    `0079B1E0`, and calls `MiniDumpWriteDump(GetCurrentProcess(), GetProcessId(…), file, 0x1826, &exceptionInfo, 0, 0)`
    (`0079AD59`–`0079ADCA`). ~~It then closes the file, calls `ShowCursor(1)` (`0079AE0E`) and loads text `0x7837`
    (`0019A510`). What it shows and how it ends were not followed past that point.~~
    *Corrected and completed 2026-09-28 (FABLE, Claude Opus 5.5, on ASTRA's filter-tail and message-resource returns;
    static, [`cv3-filter-tail-fable`](../../_index/candidates/cv3-filter-tail-fable/README.md) O, I, S):* the text is
    requested **before** `ShowCursor`, and the filter ends in a message box:
    1. `CloseHandle(file)` (`0079ADD2`), then `SysFreeString(NULL)`, a no-op free (`0079ADDA`).
    2. String `0x7837` through `0019A510` (`0079ADE5`).
       - The lookup's receiver `02EAF320` is ATL's `CAtlBaseModule`. No static writer fills its resource-instance array, so,
         provided its constructor ran (`0016A2A0`) and no computed write fills that array, only the game image's own
         resources are searched. Actual initialisation and live main-module-only behaviour are not established (OPUS,
         [`native-filter-abi-opus`](../../_index/candidates/native-filter-abi-opus/README.md) M, N).
       - The selector `0019A5B0` walks `id & 0xF` counted entries and checks only that each prefix starts before the
         resource's end. It returns the pointer to the length prefix, or NULL for a count of 0. **It does not check that
         the full `count` code units fit** (ASTRA 83; `filter_tail.py` P).
       - The filter copies the text into a BSTR with `SysAllocStringLen(ptr + 2, count)`, and with no text it keeps NULL.
         All nine shipped language copies carry the string whole. English reads "Fatal error encountered."
    3. `ShowCursor(1)` (`0079AE0E`), then `MessageBoxW(NULL, text, L"error", MB_ICONERROR)` (`0079AE26`), then
       `SysFreeString(text)`.
    4. It returns 1, `EXCEPTION_EXECUTE_HANDLER`.

    With the gate at 0 the filter would return 1 at once, with no dump and no box. For an unhandled exception, the documented
    meaning of 1 is that the process ends after the filter. Not observed here: which language copy is chosen at run time,
    that the box appears, or how the process ends.
  - **`005CCAB0` is a second writer on its own thread.** `005CCD00` calls `SymSetOptions(0x16)` and `SymInitialize` (the
    imports `008C30C8` / `008C30E8`), then starts `005CCAB0` with `CreateThread` (`005CD019` `lea r8`, `005CD03D`). That
    thread creates the file named at `[ctx + 0x10]` and writes a type-`0x1B27` dump with `ctx` as the exception parameter
    (`005CCAE8`–`005CCB39`). `005CCD00`'s only caller is `005CCBF0`, whose only caller is `008A5AD0` in the handler-funclet
    region, so this looks like a structured-exception report path. Its trigger, and whether it can run before the filter,
    are not read. The handshake page lists `005CCAB0` among the thread start routines as a "D3D worker"; it is this dump thread.
- [x] **The 121 import slots with no `FF 15` call site.** Given that two of them turned out to be
  live through `jmp` thunks, the residue needs the thunk-aware scan before any of it is called
  unused. `CV-4`.
  *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (CV-4): none of the 121 is unreferenced. Every
  one of the 538 import slots has a code reference.* Instrument: [`members/iat_any_reference.py`](members/iat_any_reference.py),
  output [`members/iat-any-reference.tsv`](members/iat-any-reference.tsv).
  - **Method.** A byte-wise rel32 scan of all of `.text` at every offset for a rip-relative displacement onto each slot, each
    candidate confirmed by decoding the containing instruction (the longest decode first, so a REX-prefixed `48 FF 25`
    starts at its prefix). A `jmp` site is then followed to its `E8`/`E9` callers and to any absolute or image-relative
    pointer to it.
  - **Controls.** The 417 slots with a `call` reference equal `iat_xrefs.py`'s 417. The two known thunk cases come out
    reached: `GetAdaptersInfo` (jump stub, 2 callers) and `MiniDumpWriteDump` (2 callers and 1 data pointer).

  | how the 121 are reached | slots |
  |---|---:|
  | through a `jmp [IAT]` stub that has `E8`/`E9` callers or a data pointer (vtables for the `std::basic_streambuf` virtuals, `_purecall` 681 pointers, `__C_specific_handler` 9) | **104** |
  | through a `jmp [IAT]` tail jump inside a function body (`DebugBreak` in `005CDB90`, `SetThreadUILanguage` in `007A0FC0`, `InitializeSListHead` in `00809C40`, `TerminateProcess` in `00809620`, `DestroyWindow` in `0079B190`, `_wmkdir` in `001F3EA0`, `_lock_file` in `0019B800`, `_unlock_file` in `0019B8A0`, `_aligned_malloc` in `0019C580` / `001EDF10`) | **9** |
  | as a loaded value, not a call target: the `std::locale` facet ids, `std::cout`, `std::_BADOFF` (data imports), and `SymGetModuleBase64` / `SymFunctionTableAccess64`, loaded as callback pointers | **8** |

  - **Limit.** A slot counted as reached is referenced, not proven to execute; some stubs sit in CRT or `std` paths the game
    may never take.
- [x] What the single `IPHLPAPI!GetAdaptersInfo` call is for in a single-player game. **CV-5.**
  *Answered on the page 2026-09-14 (FABLE), box left for the ledger mirror (CV-5):* **YEBIS's licence check. It binds a
  licence to a network adapter's MAC address, and the shipped licence is unbound, so the call never happens.**
  - **Who calls it.** Both call sites `00781F80` and `00781FD7` are in `00781EC0` (758 B). That function sizes and then
    fills the adapter list with `GetAdaptersInfo` and formats each address as `%02x-%02x-%02x-%02x-%02x-%02x`
    (`00DAC628`, `00782040`). Its only caller is `00781DD0`, which is called only from YEBIS's licence verifier
    `0071D9E0`, at `0071DDAA` and `0071DE8E`.
  - **When it is skipped.** The verifier first runs `strncmp(licence MacAddress, "00-00-00-00-00-00", 17)` (`00D9B260`,
    `0071DD64`–`0071DD73`). When the licence names no adapter it jumps straight to the date check. Only a non-zero MAC
    enumerates the adapters (`00781D00`, `00781DD0`). The verifier sets status 1, *License is not valid*, when no adapter
    address can be read (`0071DDB3`); the per-adapter comparison after that was not traced.
  - **The shipped licence.** `FeatureId = YEBIS_D3D11 … MacAddress = 00-00-00-00-00-00` (`00D86C51`), so on retail
    `GetAdaptersInfo` is linked and reachable in code but skipped by that branch. It is not a Steam or multiplayer
    identity call. See the dates half on
    [the middleware inventory, X-2](../../23-Third-Party-Libraries/third-party-middleware-inventory.md).
- [x] **UQ-328.** *(status restated in the register 2026-09-26, FABLE, Claude Opus 5.5: see the row)* The two literal messages are Steam's — *"Received stats and achievements from Steam"*
  (`0020C974`) and *"Steam overlay now inactive"* (`008655BC`); the rest of the Steam surface is not
  examined here.

## 6. Evidence

| claim | evidence | tier |
|---|---|---|
| 30 DLLs, 538 symbols, per-DLL counts | the PE import directory, walked | 1 |
| 417/538 slots reached, 3,543 indirect sites | `iat_xrefs.py` against the GN160 function table | 1 |
| `OutputDebugStringA` 150 sites / 93 functions | disassembly from every function entry bounded by its recorded size, IAT slot resolved from the import directory | 1 |
| The 90/2/1 split of direct callers | owner tags of those 93 functions | 1 |
| `006DF480` reaches the API at `006DF4FA` | its own disassembled body | 1 |
| **801** sites / 160 functions into the wrapper | census over all function bodies of **both** `E8 call rel32` (800) and `E9 jmp rel32` (1, a tail call at `00788471`) — **the call-only count of 800 was corrected by this document's own audit pass**; the function containing the tail call already appears via its `call`, so the function count is unchanged | 1 |
| No overlap between the two populations | set intersection, empty | 1 |
| **`H-3`: 90 of 102 PPFX functions call the wrapper** | `string_xref.py` over 7 diagnostic prefixes (102 functions), intersected with the wrapper's caller set | 1 |
| The stack walker at `005CCD00` | its `SymInitialize` / `SymFromAddr` / `StackWalk64` call sites | 1 |
| `MiniDumpWriteDump` and `GetAdaptersInfo` are live | `data_xref_scan.py` with `OutputDebugStringA` (150 refs) as the passing control, then the thunks' callers | 1 |
| `MultiByteToWideChar` absent from the import table | the import directory walk, which finds `WideCharToMultiByte` and not it | 1 |
| The `std::locale` / `codecvt` surface | the `MSVCP140` import names | 1 |
| **`006DF480` is Yebis's logger** | its caller set spans `006DA8F0`–`00790160`, containing the `0x782289` the PPFX document reports, and 90 of its callers carry PPFX diagnostic strings — **an address-range argument plus a string join, not a body read** | 2 |

## 7. Related

- [`../Thunk-Layer/the-thunk-layer-and-why-call-counts-disagree.md`](../Thunk-Layer/the-thunk-layer-and-why-call-counts-disagree.md)
  — the hazard that nearly buried the crash handler, in its original form.
- [`../Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md`](../Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md)
  — the other half of the hooking picture: fixed image base, ASLR off, CFG shipped disabled.
- [`../../17-Presentation-Rendering/Post-Processing/ppfx-function-identification.md`](../../17-Presentation-Rendering/Post-Processing/ppfx-function-identification.md)
  — **whose `H-3` this answers.**
- [`../../18-Audio/sead-function-identification.md`](../../18-Audio/sead-function-identification.md)
  — SEAD's diagnostics, the population already documented.
- [`../../21-RNG-And-Determinism/rng-streams.md`](../../21-RNG-And-Determinism/rng-streams.md)
  — the CRT `rand` stream in the busiest-imports table.

## Falsification pass — 2026-09-07, `xiionline-61`

**Self-attack, same day as authorship.** The session that wrote this document had a demonstrated
error rate, so its own claims were re-derived rather than re-read.

**The systematic attack:** every "only caller" / "N callers" statement in the day's four documents was
made with a scan that matched `E8 call rel32` only. **The CRT block later established that this
binary reaches things through `E9 jmp rel32` tail calls and import thunks**, so every one of those
claims was re-run against **both** instruction forms, and against `data_xref_scan.py` for
address-taken references (vtables, pointer tables) with a passing control.

### Result for this document — **one count corrected, by its own lesson**

This document is the one that established that a call-only scan misses `jmp` thunks. **Applying its
own rule to itself found a miss.**

| claim re-tested | result |
|---|---|
| **801** sites into the wrapper `006DF480` | **was 800** — the census counted `E8 call` only, and there is also an **`E9 jmp` tail call at `00788471`**. Corrected throughout. |
| **160** functions call the wrapper | **stands** — the function holding that tail call already appears via its own `call` at `00788460`, so no narrator was missed. |
| **253** functions narrate, two non-overlapping populations | **stands** |
| `MiniDumpWriteDump` and `GetAdaptersInfo` are live through thunks | **stands** — this was itself the correction that produced the rule. |

> **The document warned about exactly this failure and still contained an instance of it.** Writing
> the rule down is not the same as having applied it everywhere; the audit is what applies it.

**Not attacked:** the per-DLL import counts, the busiest-import table, and the claim that
`MultiByteToWideChar` is absent from the import table — all read directly from the PE and not
re-derived here.

## `BK-5` answered — the nine `__C_specific_handler` users (FABLE, 2026-09-14)

*Read from `.pdata`: every `RUNTIME_FUNCTION` whose `UNWIND_INFO` names the handler RVA of the `__C_specific_handler`
thunk `00861ED8`, with each scope table decoded as `{Begin, End, Handler, JumpTarget}`. Exactly nine match, which agrees with
the nine data pointers to the thunk in [`members/iat-any-reference.tsv`](members/iat-any-reference.tsv).*

> **PASS-6 RULING — FABLE, 2026-09-16, on `OPUS-REQ-FABLE-PASS6-SCOPE-TABLE-TRY-RANGES`. The
> range column is admissible, and here is its independent support.**
>
> OPUS accepted the *count* (nine, agreeing with nine admissible data pointers) and doubted the
> **range** column, whose values come from decoded scope tables with nothing corroborating them in
> this section. That doubt was right to raise: `check_banned_evidence`'s `SUBJECT_DIR` rule exempts
> only `Exception/` and `Unwind/` directories, and this page is in `Runtime-Service-Surface`, so
> the instrument does **not** exempt it.
>
> **The ruling follows the pass-6 principle already recorded in `FINAL-AUDIT-PROTOCOL.md`:
> unwind data is banned as evidence for what the program EXECUTES, not for what the exception
> DISPATCHER does, and it is never banned as a method of FINDING something that is then checked
> elsewhere.** Here the scope tables are the method of enumeration. What matters is whether the
> values survive without them.
>
> **They do, and this was measured rather than assumed.** Each function was decoded linearly from
> its **entry address in `.text`**, with no `.pdata` read at all, and every quoted `Begin` and
> `End` was tested against the instruction boundaries that decode produces: **18 of 18 land exactly
> on a boundary.** A wrong or misdecoded range lands mid-instruction, so this is a real check and
> not a tautology.
>
> **The behavioural claims check too.** `WinMain`'s first guarded instruction is literally
> `call 007980A0`, the crash-dump filter this table names. `005CD1E0` and `00863430` each decode to
> `mov ecx, 0x406D1388` followed by `call [IAT]`, the debugger thread-naming exception this table
> names. `005CCBA0`'s guarded span is `mov rcx, rbx` / `call rdi` — the `fn(arg)` call itself,
> with the `[ctx+8]` / `[ctx+0x10]` loads correctly sitting *before* the range.
>
> **So no claim on this page rests on exception metadata**, and pass 6 is satisfied for `BK-5`
> without withdrawing the column. **The check also found one cell that overstated its range**, now
> narrowed in the table above — which is the argument for corroborating rather than exempting: the
> exemption would have preserved the error.

| function | `__try` range | filter / handler | what it guards |
|---|---|---|---|
| `007A3770` (`WinMain`) | `007A378D`–`007A3798` | `008A5AD0` → `005CCBF0` | the whole application, `007980A0` — **the crash-dump filter** |
| `005CCBA0` | `005CCBC3`–`005CCBCC` | `008A5AD0` | a thread start trampoline: `fn(arg)` from `[ctx+8]` / `[ctx+0x10]` — the same filter per thread |
| `005CD1E0` | `005CD2C8`–`005CD2E0` | `0089BEF0`, returns −1 | `RaiseException(0x406D1388)`, the debugger thread-name exception |
| `00863430` | `008634CC`–`008634E4` | filter constant `1` | **only** the `0x406D1388` naming exception. *(Narrowed 2026-09-16 (FABLE): this cell used to read “`CreateThread` + `SetThreadPriority`, then the same `0x406D1388` naming exception”. The two calls at `0086348B` and `008634A6` are **outside** the range — the guarded span is `008634CC`–`008634E4` and decodes to `lea r9,[rsp+0x30]` / `xor edx,edx` / `mov ecx,0x406D1388` / `lea r8d,[r14+3]` / `call [IAT]` / `jmp`, and nothing else. The function does make those two calls; the `__try` does not cover them.)* |
| `00808D78` (`__scrt_common_main_seh`) | `00808DA3`–`00808EB8` | `008A5B94` | CRT startup |
| `00808A54` (`__scrt_is_nonwritable_in_current_image`) | `00808A5B`–`00808AE6` | `008A5B7C` | CRT section probe |
| `00808FE4` (`eh vector constructor iterator`) | `00809015`–`0080903E` | `008A5BB2`, termination handler | compiler-generated `__finally` |
| `00809054` (`eh vector destructor iterator`) | `00809087`–`008090B3` | `008A5BDE`, termination handler | compiler-generated `__finally` |
| `008090C0` (`__ArrayUnwind`) | `008090E4`–`0080910C` | `008A5C0A` | compiler-generated |

- **Why only nine.** Five belong to the CRT and the compiler's array iterators. The game adds two idioms that genuinely need
  SEH rather than C++ exceptions.
  - **The crash reporter** wraps `WinMain`'s body and every thread started through `005CCBA0`. Both take a
    `IsDebuggerPresent` fast path that calls the function **without** the `__try` (`007A3774`–`007A3783`, `005CCBB2`–`005CCBC1`),
    so a debugger sees the fault first. The filter `008A5AD0` calls `005CCBF0`, the minidump path above.
  - **Thread naming** raises `0x406D1388`, which only a debugger consumes, and swallows it with an `__except` that either
    continues execution (`0089BEF0` returns −1) or runs the handler (`00863430`'s filter `1`).
- **Consequence for a detour or an injected DLL.** A fault inside the application or a `005CCBA0` thread is caught by the
  dump filter unless a debugger is attached. A hook that faults there produces a minidump, not a plain crash.

> **The two game-side `__try` ranges are corroborated by the instruction stream, to the byte — added
> 2026-09-16 (FABLE), answering `OPUS-REQ-FABLE-PASS6-SCOPE-TABLE-TRY-RANGES`.** The scope tables are
> decoded from `.xdata`; these reads are from `.text` and are independent of them.
>
> - **`WinMain`.** `007A3774` calls `IsDebuggerPresent` through the IAT slot at `008C2180`; `007A377C`
>   branches on the result. The **debugger** arm calls `007980A0` at `007A377E` and jumps away at
>   `007A3783`. The other arm sets the result slot to `-1` at `007A3785` and calls `007980A0` again at
>   **`007A378D`** — **exactly the scope table's `Begin`** — stores the result at `007A3792`, and the
>   `__except` continuation reads it back at **`007A3798`**, **exactly the `End`**. So the range
>   brackets one call and its result store, and **the identical call on the debugger arm sits outside
>   it**, which is what the fast-path claim above asserts and what a `__try` around a single arm looks
>   like.
> - **`005CCBA0`.** Same shape: `IsDebuggerPresent` at `005CCBB2`, the unguarded `mov rcx, rbx` /
>   `call rdi` pair at `005CCBBC`–`005CCBBF`, and the guarded twin at **`005CCBC3`** — **the `Begin`** —
>   with the result store at `005CCBC8` and the jump at **`005CCBCC`**, **the `End`**.
>
> **Why this was worth doing rather than ruling alone.** The ruling
> ([FINAL-AUDIT-PROTOCOL](../../_index/FINAL-AUDIT-PROTOCOL.md)) is that a `__try` range is a claim
> about the exception dispatcher, for which the scope table is the mechanism rather than metadata —
> so the column was admissible either way. **But an admissible claim with a second, independent source
> is strictly better than an admissible claim without one**, and the duplicated call either side of
> the boundary is the kind of corroboration that would have caught a decoding error.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

**Resource — CLIENT.**

- The resource lookup `0019A510` (`FindResourceW`) is also called by a 1,099-byte Resource-filed body.
- The Phyre thread creator `005CD1E0` (`CreateThread`, the `PhyreEngineThread` name exception) is called by a
  112-byte Resource-filed body. **Some resource code starts its own Phyre thread.** Which thread it starts is not read
  here.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Input — CLIENT.** `FUN_00197ee0`, owned by that layer, calls `001F3EA0` on this page. That caller is a 273-byte OS query in an **`0x848`-byte frame** with a stack cookie: it asks the import at `008C27E8` with mode 5 and abandons the call on a negative result; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Platform — SERVICE (SWE2-EC7, batch 167, 79 edges).** The batch-167 entries name `00159420`, the module-load helper this layer owns, because the Setupapi/Advapi32/Shell32 arms all resolve their DLLs through it; that helper is itself reached from Platform bodies `00159AA0`/`00159F90`/`0015A0E0` and others - the traffic is Platform code consulting the same loader the enumeration arms use, not a shared owner of this surface.

## SWE2-EC7-44 update (2026-09-19) - `005CCBF0`

`005CCBF0` (265 B) is a body - `008C21F0`/`008C2160` import calls, `0019C5D0`/`005CCD00`/`00808C40`/`00861EC0`. Interior anchor `005CCC2C` (a `0019C5D0` call).

## SWE2-EC7-44 update (2026-09-19) - `0079B1E0`

`0079B1E0` (261 B) is a body - `008C2280`/`008C2178`/`008C28C0`/`008C28C8` import calls, `0017D2E0`/`00808C40`/`00861EC0`. Interior anchor `0079B212` (a `0017D2E0` call).

`001595F0` (356 B) is the wide-string `.dll`-name probe the service/driver enumeration layer shares (`0015A780`, `0015AC50`, `0015AE60`): `00861EEA` finds the last `\` in the wide name, `repne scasw` measures the tail, and a backwards walk from the end stops at `\` (0x5C) or `.` (0x2E) so `00861F20` can compare the candidate extension against the `01CC6BF8` literal `.dll` - returns 1 on match, else falls into a second pass on `rdx`'s alternate name.

Interior anchor `00159605` (function `001595F0`).

`0015B440` (265 B) is the wide path join the enumeration layer calls to glue a directory and a leaf name (`0015B5F0`, `0015B820`): two `repne scasw` lengths, an `ebp = 1` separator flag only when the left part does not already end in `\` and the right part does not begin with one, `(len1 + sep + len2) * 2 + pad` sized allocation through IAT `008C2348`, then `001597E0`/`001599D0` copy both halves into the fresh buffer - a manual PathCombineW.

Interior anchor `0015B4D5` (function `0015B440`).

`0015A240` (235 B) is the lazy OS-build cache `0015B110`/`0015B820`/`0015BB30` consult: if `dword[02EAECE0]` is zero it calls `0015A0E0` with `rcx = 0xFFFFFFFF80000002` (HKEY_LOCAL_MACHINE) against `SOFTWARE\Microsoft\Windows NT\CurrentVersion` / `CurrentBuildNumber` (`01CC6CA0`/`01CC6D00`), and only when the read returns success with a single value does it walk the string through `00861FD4` (`iswdigit`) accumulating `ecx*10 + digit` into `02EAECE0` - a non-digit resets the cache to 0.

Interior anchor `0015A28D` (function `0015A240`).

`0015B110` (805 B) is the driver-store probe of the device-enumeration layer (`0015B820` is the caller): loads `Setupapi.dll` through `00159420`, then resolves and drives `SetupGetInfDriverStoreLocationW` (`01CC6E58`), `SetupDiGetDevicePropertyW` (`01CC6E78`) and `SetupDiDestroyDeviceInfoList` (`01CC6D40`), with `00861EEA`/`0015A330`/`0015B41A`/`0015B412`/`0015B3CE` path and compare helpers around them - the INF driver-store location read.

Interior anchor `0015B15C` (function `0015B110`).

`0015A9B0` (671 B) is the registry-property arm of the same device enumeration (`0015B820`): loads `Setupapi.dll` via `00159420` and calls `SetupDiGetDeviceRegistryPropertyW` (`01CC6E30`) plus `SetupDiDestroyDeviceInfoList` (`01CC6D40`) through `00159420`-resolved handles, looping rows through `0015A780`/`0015AC03` - the legacy `SPDRP_*` read path.

Interior anchor `0015AA18` (function `0015A9B0`).

`0015A780` (555 B) is the service-control query (`0015A9B0` calls it): `00159420` loads `Advapi32.dll` (`01CC6C68`) and the body drives `OpenSCManagerW`, `OpenServiceW`, `QueryServiceConfigW` and `CloseServiceHandle` (`01CC6E20`/`01CC6E10`/`01CC6DF8`/`01CC6DE0`), calling the `.dll` probe `001595F0` on the resolved service path and `00159E60` for the tail free - answers whether a named service exists and how it is configured.

Interior anchor `0015A7C2` (function `0015A780`).

`0015B5F0` (545 B) is the device-class registry walker (`0015B820` calls it): loads `Setupapi.dll`, joins `SYSTEM\CurrentControlSet\Control\Class\` (`01CC6EA0`) onto the class key through `0015B440`, reads per-entry properties with `SetupDiGetDeviceRegistryPropertyW` (`01CC6E30`) and destroys the info list at the end (`01CC6D40`) - the `Class\{GUID}` enumeration used to find display adapters.

Interior anchor `0015B637` (function `0015B5F0`).

`00159B10` (387 B) is the lazy `SHGetFolderPathW` resolver (`00159CA0` calls it): zeroes a 0x20A-byte stack buffer via `00861EC0`, and only when the `02EAEAE0` cache slot is empty does it `00159420`-load `Shell32.dll` (`01CC6C20`), fetch the ordinal target through the two IAT pair-calls `008C2368`/`008C21F8`, then invoke it - a once-per-process resolution of the special-folder path.

Interior anchor `00159B4D` (function `00159B10`).

`00159420` (248 B) is the System32-path join the whole service layer loads through (`0015A330`, `0015A780`, `00159B10`, `0015A0E0`, `0015B110`, `0015B5F0` and four more): `008C2350` (GetSystemDirectoryW) measures then fills a fresh `008C2348`-allocated buffer, a `\` is appended only when the directory lacks a trailing one, and the caller's wide name is copied on after it via a `repne scasw` length - the hand-rolled PathCchCombine the batch-167 DLL arms all reached.

Interior anchor `0015944F` (function `00159420`).

`0015A330` (786 B) is the lazy Setupapi resolver and display-interface enumerator `0015A9B0`/`0015B110`/`0015B5F0` lean on: when `02EAEAA0` is empty it `00159420`-joins `Setupapi.dll` (`01CC6DC0`), `008C2368`-loads it and `008C2130`-resolves `SetupDiGetClassDevsW`, `SetupDiEnumDeviceInterfaces`, `SetupDiGetDeviceInterfaceDetailW` and `SetupDiDestroyDeviceInfoList` into `02EAEAA8`..`02EAEAD0`, then runs `GetClassDevs(r14, 0x12)` (DIGCF_PRESENT|DEVICEINTERFACE) and per-index `EnumDeviceInterfaces` + a two-call `GetDeviceInterfaceDetailW` (size probe into `rsp+0x30`, then an `008C2348` buffer and the fill) - the hardware-key enumeration the batch-167 arms documented at name level.

Interior anchor `0015A3FD` (function `0015A330`).

`00159E60` (137 B) is the wide-string heap duplicate the layer shares (`0015A650`, `0015A780`, `0015AC50`, `0015AE60`, `0015B440`): null in, null out; else `repne scasw` for the length, `(len+1)*2` plus the `0x40` base through `008C2348`, copy by `00159760`, and `008C21F8` frees the buffer and returns null if the copy reports failure - a wcsdup with the layer's tagged allocator.

Interior anchor `00159EC2` (function `00159E60`).

`0015A0E0` (338 B) is the registry read wrapper `0015A240` (`CurrentBuildNumber`) calls: lazily `00159420`+`008C2368`-loads `Advapi32.dll` (`01CC6C68`) into `02EAEB38`, resolves `RegOpenKeyExW`/`RegCloseKey` into `02EAEB40`/`02EAEB58`, opens the caller's `r13`/`r12` key into `[rsp+0x30]`, delegates the value query to `00159F90` and always `RegCloseKey`s - fail-closed through `008C20A8` when resolution fails.

Interior anchor `0015A202` (function `0015A0E0`).

`001599D0` (206 B) is the byte-count variant of the layer's bounded wide-copy (`0015A650`, `0015B440` call it): `r10 = rdx >> 1` converts bytes to elements, bounds-checked at `0x7fffffff`, and the copy loop emits `0x80070057` on truncation or `0x8007007A` when the destination is short - a `StringCchCopyNW`-faithful implementation with HRESULT returns.

Interior anchor `00159A12` (function `001599D0`).

`00159900` (206 B) is the char-count sibling of `001599D0` (`00159B10` calls it): identical scan-then-copy shape but `rdx` is already an element count, same `0x80070057`/`0x8007007A` HRESULT contract and the same `r11 - rcx` source-destination aliasing guard - the pair is the wide Strsafe surface the shell-path and registry helpers sit on.

Interior anchor `00159940` (function `00159900`).

`00159EF0` (158 B) is the bounded heap duplicate (`0015A650`, `0015B110` call it): `repne scasw` for the source length, `rbp = min(len, rdx)` via `cmovb`, the `(rbp+1)*2`-class allocation through `008C2348`, then `00159870` copies `rbp+1` chars from `r9`'s base - `strndup`-style clamping with the same fail-free tail as `00159E60`.

Interior anchor `00159F68` (function `00159EF0`).

`00159760` (123 B) is the copy engine `00159E60`/`001599D0`/`00159EF0` delegate to: `rdx == 0` or `rdx > 0x7FFFFFFF` returns `0x80070057`, the element loop copies until NUL with an `r8 - rcx` aliasing guard and a `0x7FFFFFFE - rdx` headroom bound, a truncated source or short destination writes the NUL and returns `0x8007007A` - the HRESULT-reporting wide `StringCchCopyN` core the layer's wrappers share.

Interior anchor `0015979A` (function `00159760`).

`00159F90` (327 B) is the registry-value query `0015A0E0` delegates to: when `02EAEB38` is empty it `00159420`-joins + `008C2368`-loads `Advapi32.dll` (`01CC6C68`), resolves `RegQueryValueExW` (`01CC6C88`) into `02EAEB50`, then runs the two-call pattern - first query probes the size at `[rsp+0x30]`, `008C2348` allocates `size + 0x40`, second query fills `rsi`'s out-buffer and frees it back through `008C21F8` on error - the value-read arm the `CurrentBuildNumber` consumer rides.

Interior anchor `0015A060` (function `00159F90`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

**Presentation, 5, and Audio, 1 — SERVICE.**
- The `_aligned_malloc` wrapper `0019C580` is called by the motion loaders and the skeleton pose code
  (`AddMotion_LoadSkeletonMapping`, `AddMotion_LoadHighModelReplace`, `AddMotion_ApplyBonePose`,
  `Skeleton_UpdateFinalPoseAndCombatLook`) and by `0053AB50`.
- The SEH-filter parent `005CD1E0` is called by the audio body `00212130`.

These are clients of the Windows services this page lists.

*Tier 2: ledger names, sizes and `edges.tsv`; no new body read (OPUS, 2026-09-29, pass-22 slice OPUS-P22-SLICE-24-99).*

`00159870` (138 B) is the bounded wide-char copy primitive `00159EF0` wraps: `0x80070057` (E_INVALIDARG) returns on a null-size or `r9 > 0x7FFFFFFE` capacity (destination NULed on the latter), u16s copy until source NUL or capacity with `0x8007007A` (INSUFFICIENT_BUFFER) reporting truncation - the `StringCchCopyW`-class safe-string body of the service surface.

Interior anchor `001598B9` (function `00159870`).
