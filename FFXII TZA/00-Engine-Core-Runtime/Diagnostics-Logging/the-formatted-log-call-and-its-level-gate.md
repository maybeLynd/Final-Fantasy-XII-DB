---
system: The formatted log call, the singleton behind it, and the vsnprintf underneath it
category: 00-Engine-Core-Runtime
status: DOCUMENTED — the sink class (Phyre::PTTYCallback) and slot 1's behaviour answered 2026-09-18 (§7): only channel 4 does anything (a debugger break), the text goes nowhere; a census of 245 call sites resolves 202 to channels 0-3 and none to 4 or above; every one of the 245 sites passes channel 0-3, none passes 4 (RC-9, answered); no caller gates its call on a verbosity control (RC-10, answered); owner read 2026-09-30 (OPUS, `_index/candidates/dd-owner-read-b1-0930/` round 3)
owner_layer: Runtime.Diagnostics.Logging — from the ledger, not inferred from callers
evidence_tier: 1
level: L1
readiness: SIGNATURE RESOLVED
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 50 addresses cited - 9 data, 12 entry, 29 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-08
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-formatted-log-pass-1
  crossref_clean: false
  reopened_count: 0
---

# The formatted log call, ~~its per-thread level gate~~ the singleton behind it, and the `vsnprintf` underneath it

> **The filename still says `level-gate`.** It is kept so every existing link and index entry
> resolves; **there is no level gate** (§9, 2026-09-13). A rename would touch `ADDRESS-INDEX.md`
> and every citation, and is a separate change.

## 1. What the player sees

Nothing, and that is the point. **A shipped build still carries its developers' logging**, the text
is still formatted, and a sink object still decides where it goes. What the player gets is the
cost: every one of these calls builds a **16 KB buffer on the stack**, formats into it, and hands
it to the sink — **on every call, with nothing to switch it off.**

> **⚠ Corrected 2026-09-13 (§9) — there is no level gate.** This section read *"switched on per
> thread at runtime … the verbosity is still consulted"*, and *"the switch is **data, not code**.
> Two globals and a thread-local decide whether a message is emitted."* **What §5 read as a
> verbosity gate is the MSVC thread-safe-static initialisation check for the sink singleton.**
> `005CDAA0` has one exit and no early return. **The cost claim survives and gets stronger:**
> there is no gate that could ever have skipped the 16 KB frame or the format.

## 2. Why these two functions

`EL-1` ranks the largest genuinely uncited functions by caller count. After removing those that
turned out to be documented already (§5), the two that remain are the top two:

| entry | body | non-EH callers | what it is |
|---|---:|---:|---|
| `005CDAA0` | 239 B | **136** | the formatted log call ~~, with the level gate~~ — it formats and emits unconditionally (§9) |
| `0019C5D0` | 86 B | **120** | a `vsnprintf`-family wrapper returning `-1` on failure |

Both are variadic, and both go through the same three-instruction MSVC idiom, which is what makes
them identifiable at all.

## 3. `0016D670` is `__local_stdio_printf_options`, and it explains both

```text
0016D670  lea rax, [rip + 0x2D4CD59]   ; -> 02EBA3D0
0016D677  ret
```

Eight bytes returning the address of one qword. Modern MSVC expands every `printf`-family call as

```c
__stdio_common_vsprintf(*__local_stdio_printf_options(), /* ... */);
```

so **`rcx = [rax]` immediately after an 8-byte call is the signature of that expansion**, and it
appears at `005CDB05` and `0019C60C`. `0016D670` has **23** non-EH callers, which is the number of
places this executable formats a string this way.

**The options qword lives at `02EBA3D0`, and its value is `4`.** *(Established 2026-09-21 (FABLE),
consuming `ASTRA-RETURN-FABLE-UQ146-PRINTF-INITIALIZER`; this line used to say the value was not
read here.)* The qword is zero-initialised and **`0016D670` is its only rip-relative reference in
the image**, so every access goes through the accessor — and of the accessor's 23 call sites,
**exactly one writes through the returned pointer**: the C initializer `00809C50`, registered in
the C table and run by `_initterm_e` before the C++ walk and before game entry, whose first
instruction pair is `call 0016D670` / `or qword ptr [rax], 4`. The other 22 do `mov rcx, [rax]` and
pass the value on. So the options argument every formatter in this executable hands the CRT is `4`,
fixed from C-initializer time, and nothing in the image can change it afterwards. *(A control ran
on the same instrument: it must classify the one known writer as a writer, and it does.)*

The same initializer ORs `2` into the separate qword behind `0018A320`, the scanf-side accessor the
[yebis source map](../../23-Third-Party-Libraries/PostEffects-Yebis-PPFX/yebis-ppfx-source-map.md)
identifies — image value `0x0003F6E0`, so `0x0003F6E2` afterwards, and again by the only writer
among that accessor's five callers. The `4`/`2` pair on those two accessors is the shape MSVC emits
for the legacy-wide-specifier link option; **that identification is from the compiler's known
pattern, not from this image**, which only shows the constants.

## 4. `0019C5D0` — `vsnprintf`, and nothing more

```c
/* FUN_0019C5D0(char *buf /*rcx*/, size_t size /*rdx*/, const char *fmt /*r8*/, ...) */
va_list ap = &stack_args;                       /* rbp = rsp + 0x78 */
int n = __stdio_common_vsprintf(*__local_stdio_printf_options(),
                                buf, size, fmt, /* locale */ NULL, ap);   /* import 008C2E10 */
return (n < 0) ? -1 : n;                        /* test eax,eax / cmovs */
```

The `cmovs` at `0019C61A` is the whole of the wrapper's own logic: **a negative return is clamped to
`-1`**. That is the documented `vsnprintf` contract, reproduced by hand around a `_s`-suffixed
import.

**Disposition C — proven implementation machinery.** Upstream named, boundary stated: the exact
imported symbol behind `008C2E10` was **not resolved**, only its family and its argument order.
*Resolved since (2026-09-13, §9, by parsing the import directory; pointer added 2026-09-30, SWE2-CONTRACT):*
`008C2E10` is `api-ms-win-crt-stdio-l1-1-0.dll!__stdio_common_vsprintf_s`. Tier 1.

## 5. `005CDAA0` — ~~format first, decide afterwards~~ format, then emit

> **⚠ The whole "gate" reading below is withdrawn (2026-09-13, §9).** Every instruction it
> quotes is decoded correctly; they were fitted to the wrong idiom. `02EAED3C` is the **PE TLS
> directory's `AddressOfIndex`** — the module's `_tls_index` — `[slot + 4]` is
> `_Init_thread_epoch`, and `02CB6158` is the **guard variable** of the static at `02CB6150`.
> The `jg` at `005CDB2F` does not return: it branches to `_Init_thread_header`, constructs the
> singleton, and **rejoins the emit path**. Read §9 instead of the block below.

```c
/* FUN_005CDAA0(int channel /*ecx*/, const char *fmt /*rdx*/, ...) */
char buf[0x4000];                               /* __chkstk for a 0x4050 frame at 005CDAB7 */
va_list ap = &stack_args;                       /* rsi = rsp + 0x4080 */

__stdio_common_vsprintf(*__local_stdio_printf_options(),
                        buf, /* size */ 0x4000, fmt, /* locale */ (void *)-1, ap);  /* 008C2DE0 */

/* the gate, and it is per-thread */
void *slot  = ((void **)__readgsqword(0x58))[*(uint32_t *)0x02EAED3C];
int32_t lvl = *(int32_t *)((char *)slot + 4);
if (*(int32_t *)0x02CB6158 > lvl)               /* cmp / jg at 005CDB29 */
    return;                                     /* dropped */

Sink *s = *(Sink **)0x02CB6150;
(*(void (**)(Sink *, int, char *))((*(void ***)s) + 1))(s, channel, buf);   /* vtable slot 1 */
```

Four things a reimplementation must not get wrong:

1. **The message is formatted before the gate is consulted.** The `vsprintf` call is at `005CDB08`
   and the comparison at `005CDB29`. A dropped message still costs the full format and the full
   16 KB frame. **That is a real per-call cost in a shipped build**, not a debug-only path.
2. **The threshold is global and the level is per-thread.** `02EAED3C` holds a TLS *index*; the slot
   is read from `gs:[0x58]`, and the comparison uses the `int32` at **+4** inside it. The global at
   `02CB6158` is the other operand.
3. **The sense of the test.** `cmp [02CB6158], lvl / jg skip` — the message is emitted when
   **`*(int32*)0x02CB6158 <= lvl`**, and dropped otherwise. Written out because the operand order of
   a `cmp` is the easiest thing in this function to invert by accident.
4. **The sink is a virtual call, slot 1.** `*(void ***)s` then `[rax + 8]`, with the channel id in
   `edx` and the buffer in `r8`. Which class implements it is **not** established here. *Established since
   (2026-09-18, §7; pointer 2026-09-30, SWE2-CONTRACT): `Phyre::PTTYCallback`, whose slot 1 `005CDB90` breaks into
   an attached debugger on channel 4 and ignores the text.*

## 6. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `005CDAA0` | the formatted log call | 239 B | 136 non-EH callers |
| `0019C5D0` | `vsnprintf` wrapper | 86 B | 120 non-EH callers; clamps negative to `-1` |
| `0016D670` | `__local_stdio_printf_options` | 8 B | 23 non-EH callers; returns `&02EBA3D0` |
| `00808F10` | `_alloca_probe` | 81 B | the `0x4050` frame |
| `008C2DE0` | import slot | — | `__stdio_common_vsprintf` family, used by the log call |
| `008C2E10` | import slot | — | the same family, used by the `vsnprintf` wrapper |
| `02EBA3D0` | the printf options qword | 8 B | ~~value not read here~~ `4`, set once by the C initializer `00809C50` (§3, 2026-09-21; cell updated 2026-09-30, SWE2-CONTRACT) |
| `02EAED3C` | **the module's `_tls_index`** — the PE TLS directory's `AddressOfIndex`; ~~the log's TLS index~~ | 4 B | read by **709** functions (§9) |
| `02CB6158` | **the magic-static guard** for `02CB6150`; ~~the global threshold~~ | 4 B | written by `_Init_thread_header` / `_Init_thread_footer` |
| `02CB6150` | the sink object pointer | 8 B | virtual slot 1 receives `(channel, text)` |
| `005CDA30` | ~~the sink's constructor~~ **a second magic-static accessor** | 112 B | guard `02CB6148`, static `02CB6140` (§9) |

## 7. What this document does not establish

- **What the channel id means**, or its range. It is passed through untouched.
  **Answered functionally 2026-09-30 (SWE2-CONTRACT):** channel **4** is the debugger-break channel — the only value
  the sink `Phyre::PTTYCallback`'s slot 1 acts on, and then only with a debugger attached (§7 below, `005CDB90`);
  channels **0–3** have no effect in the sink; and no call in the image passes 4 (RC-9 below). *Limit, not a question:*
  the developers' names for the channels are not in the image.
  *Range measured 2026-09-30 (SWE2-CONTRACT), static:* the 136 caller functions make 245 call or tail-jump sites;
  202 load a literal channel, and every literal is 0, 1, 2 or 3 (16, 80, 80 and 26 sites); none passes 4 or above.
  The format strings beside them read as informational text on 0 (`[FileCache] …`), engine and screen messages on 1
  and 2, and unexpected-value errors on 3, which is a reading of the strings, not a name the image gives. Since slot 1
  acts only on 4, **no literal channel in the image does anything but format**. Control
  [`log_channels.py`](../../_index/candidates/swe2contract-ddres-b1-0930/log_channels.py) (output `log_channels.out`,
  control: the edge list reproduces the 136 callers), tier 1.
- [x] **RC-9.** What channel the 43 log-call sites whose channel is computed pass (`lea ecx, [reg + n]` or a
  register copy, in 34 functions, mostly PhyreEngine bodies; `log_channels.out` lists each), and so whether any site
  in the image passes 4, the one channel the sink acts on. Registered 2026-09-30 (SWE2-CONTRACT); static.
  **ANSWERED 2026-09-30 (static; SWE2-CONTRACT on OPUS's record
  [`rc9-log-channels-0930`](../../_index/candidates/rc9-log-channels-0930/README.md), commit `e65c88dee`): every one of
  the 245 sites passes channel 0–3, and none passes 4.** The 43 computed sites resolve to channel 1 at 23, 2 at 17 and
  3 at 3: each `lea ecx, [reg + n]` adds to a register the path has proved 0 (a `test`/`jne` on a call result) or to a
  compared value (`cmp eax, 2`). Controls: 245 sites in 136 functions reached (22 only through switch tables), all 202
  literals contained, six sites read by hand. *Correction to this page's literal count:* the literal site `00685115`
  (in `00684F60`) is also entered with `ecx` = 3 through `jmp 0x685115` at `00685078`, so it passes 2 or 3; the 202
  literal sites stand, one of them also reached with 3. So in the shipped image **no log call breaks into a debugger**,
  and no call does anything but format. Tier 1.
- **Which class the sink is**, or what slot 1 does with the text.
  **Answered 2026-09-18 (FABLE): the sink is a `Phyre::PTTYCallback`, and slot 1 never touches the text.** `005CDA30` is the magic-static constructor of the object at `02CB6140` (guard `02CB6148`): it stores the vtable `00D360A0`, whose RTTI locator names `.?AVPTTYCallback@Phyre@@`, and registers `008AADA0` with `atexit` (`005CDA78`–`005CDA8D`); the second magic static `005CD9C0` publishes that object's address as the sink pointer `02CB6150`. The vtable has two slots: slot 0 `005CD8F0`, the deleting destructor (which re-seats the sink pointer to a fresh singleton if it pointed at the object being destroyed, `005CD91E`–`005CD932`), and slot 1 `005CDB90` (35 B), which compares the channel with 4 and, when `IsDebuggerPresent()` returns non-zero, tail-calls `DebugBreak()` (`005CDB94`–`005CDBA7`) — it ignores the text. So in this build the formatted text goes nowhere; channel 4 is the break channel, and what the other channel ids mean stays open. Static: the two constructors, the vtable and its RTTI, both virtuals.
- [x] ~~**What writes `02CB6158` or the per-thread level**, so the gate's *policy* is unknown — only
  its mechanism.~~ **Dissolved 2026-09-13 (§9): there is no policy and no per-thread level.**
  `02CB6158` is a magic-static guard, written by `_Init_thread_header` (`008092FC`) and
  `_Init_thread_footer` (`0080929C`).
- [x] ~~**The exact imported symbols.** Both slots are identified by call shape and argument order,
  not by resolving the import directory.~~ **Answered 2026-09-13 (§9) by parsing the import
  directory: `008C2DE0` is `api-ms-win-crt-stdio-l1-1-0.dll!__stdio_common_vsnprintf_s` and
  `008C2E10` is `api-ms-win-crt-stdio-l1-1-0.dll!__stdio_common_vsprintf_s`** — **two different
  symbols**, which corrects §5's argument reading.
- **Any runtime observation.** Static disassembly at the certified hash.

## 8. Falsification checklist

- [x] **`0016D670` is `__local_stdio_printf_options`.** *Killer:* a body that does anything but
      return a constant address. It is `lea rax, [rip+…] ; ret`, and both callers immediately use
      `[rax]` as the first argument to a `__stdio_common_*` import — the documented expansion.
- [x] **The format happens before the gate.** *Killer:* the comparison preceding the call. The call
      is at `005CDB08`, the `cmp` at `005CDB29`.
- [x] **The buffer is 16 KB.** *Killer:* a different size argument. `mov r8d, 0x4000` at `005CDAFA`,
      inside a `0x4050` frame.
- [x] ~~**The level is thread-local.** *Killer:* a plain global read. `mov rax, gs:[0x58]` at
      `005CDB14`, indexed by `[02EAED3C]`.~~ **⚠ This item is the cautionary one (§9).** The killer
      was *satisfied* — the read really is thread-local — **and the conclusion is still wrong**,
      because `gs:[0x58]` indexed by the module's `_tls_index` is what **every** magic static in
      this image does. **A killer a wrong reading passes is not a killer.** It has to be able to
      distinguish the claim from its nearest rival, and "is it thread-local?" cannot separate a
      log level from `_Init_thread_epoch`.
- [x] **`0019C5D0` clamps to `-1`.** *Killer:* returning the raw result. `or ecx, -1 / test eax,eax /
      cmovs eax, ecx`.

> **Killers run 2026-09-14 (FABLE); all four hold, and one wording is too narrow.**
> - `0016D670` is `lea rax, [02EBA3D0] ; ret` (8 bytes). It has **23 direct call sites, not two**, among them `005CDADE`
>   and `0019C5F0`, and both of those dereference `[rax]` as the options argument of a `__stdio_common_*` import.
> - The format runs before the gate. `005CDAA0` calls `__stdio_common_vsnprintf_s` (IAT `008C2DE0`) at `005CDB08`,
>   and the level `cmp` is at `005CDB29`.
> - The buffer is 16 KB: `mov r8d, 0x4000` at `005CDAFA`, buffer `rsp+0x40`, in a frame of `0x4050` bytes probed by
>   `00808F10`.
> - `0019C5D0` calls `__stdio_common_vsprintf_s` (IAT `008C2E10`), then `or ecx, -1 / test eax, eax / cmovs eax, ecx`
>   at `0019C615`–`0019C61A`.

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run first, one address at a time and read in full, per
[`EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md) amendment 2026-09-13b.)*

### ⚠ There is no level gate. It is the magic-static check for the sink singleton.

`005CDAA0`, decoded end to end:

```asm
005CDB0E  mov  ecx, [rip + 0x28E1228]     ; -> 02EAED3C
005CDB14  mov  rax, gs:[0x58]
005CDB1D  mov  edx, 4
005CDB22  mov  rax, [rax + rcx*8]
005CDB26  mov  ecx, [rdx + rax]           ; [slot + 4]
005CDB29  cmp  dword [rip + 0x26E8629], ecx   ; -> 02CB6158
005CDB2F  jg   0x5CDB60                   ; <- NOT a return
...
005CDB31  mov  rcx, [rip + 0x26E8618]     ; -> 02CB6150, the sink
005CDB3F  mov  rax, [rcx]
005CDB42  call [rax + 8]                  ; virtual slot 1 (edx = channel, r8 = buffer)
005CDB5F  ret                             ; the ONLY ret in the function
...
005CDB60  lea  rcx, [rip + 0x26E85F1]     ; -> 02CB6158
005CDB67  call 0x8092FC                   ; _Init_thread_header
005CDB6C  cmp  dword [rip + ...], -1      ; -> 02CB6158
005CDB73  jne  0x5CDB31                   ; already built -> emit
005CDB75  call 0x5CDA30                   ; build it
005CDB81  mov  [rip + 0x26E85C8], rax     ; -> 02CB6150
005CDB88  call 0x80929C                   ; _Init_thread_footer
005CDB8D  jmp  0x5CDB31                   ; -> emit
```

**Both branches reach `005CDB31`.** The function has exactly one `ret`, at `005CDB5F`, after the
virtual call. **No message is ever dropped, and nothing is ever consulted about verbosity.**

Three pieces of evidence, the first from the file's own structure rather than from reading code:

1. **`02EAED3C` is the PE TLS directory's `AddressOfIndex`.** Parsed from data directory 9: the TLS
   directory at RVA `01BCBED8` gives `AddressOfIndex = 0x02EAED3C`. It is the module's `_tls_index`,
   written by the loader — **not a logging index**. `[slot + 4]` is therefore `_Init_thread_epoch`.
2. **The population says the same.** `02EAED3C` is read by **709** functions, and **707** call
   `_Init_thread_header`. The idiom is the whole module's, not this function's.
3. **`005CD9C0` is the same sequence with the same two globals**, and it is unmistakably an accessor:
   guard `02CB6158`, `lea rax, [02CB6150]`, return. Two functions share the preamble because both
   are getting the *same singleton*.
4. **The database already had it right, one chapter over.**
   [Lazy statics and the one-time init lock](../../24-Compiler-And-CRT-Runtime/Lazy-Static-Initialization/lazy-statics-and-the-one-time-init-lock.md)
   names `02EAED3C` as **`_tls_index`** and TLS block `+0x04` as **`_Init_thread_epoch`** in its own
   address table, and writes the test as `if (thread_epoch < guard)`. **So this is not a new reading
   — it is that page's reading, arriving at a function that had been given a different one.**

> **Which means the finding is a contradiction, not a discovery.** Two documents described the same
> two globals — one as `_tls_index` and `_Init_thread_epoch`, the other as a logging TLS index and a
> per-thread level — and nothing caught it. `check_consistency.py` compares how an *address* is
> described, and both pages called `02EAED3C` "the TLS index"; the conflict was in what `[slot + 4]`
> **means**, which no checker in this repository compares.

> **Every instruction §5 quotes is decoded correctly.** The `cmp`'s operand order, the `+4`, the
> `gs:[0x58]` — all right. They were fitted to the wrong idiom, and the reading then explained
> everything: a global threshold, a per-thread level, a sense-of-test warning, a modding note about
> two globals and a thread-local. **A coherent story is not a control.** The control that breaks it is
> the one the page could not take from the disassembly at all — the TLS directory field.

**What survives, and is stronger for it.** §1's cost claim: `mov eax, 0x4050` / `call 0x808F10`
(`_alloca_probe`) at `005CDAB2`–`005CDAB7`, and `mov r8d, 0x4000` at `005CDAFA`. A 16 KB frame and a
full `vsnprintf` on **every** call — and now with no gate that could ever have skipped them.

### §7's fourth unknown, answered by parsing the import directory

| slot | symbol |
|---|---|
| `008C2DE0` | `api-ms-win-crt-stdio-l1-1-0.dll!` **`__stdio_common_vsnprintf_s`** |
| `008C2E10` | `api-ms-win-crt-stdio-l1-1-0.dll!` **`__stdio_common_vsprintf_s`** |

**They are different symbols, and that corrects §5's argument reading.** `vsnprintf_s` takes
`(options, buffer, sizeOfBuffer, count, format, locale, arglist)`, so in `005CDAA0`:
`rdx` = buffer, `r8d` = `0x4000` = sizeOfBuffer, **`r9 = -1` is `count`, i.e. `_TRUNCATE`**, and the
locale is the **`0`** written to `[rsp + 0x28]`. §5 reads the `-1` as the locale and omits `count`.
`0019C5D0` passes `(options, buf, size, fmt, 0, ap)` to `vsprintf_s`, as §4 says.

### `005CDA30` is not a constructor

It is **another magic-static accessor** — same `gs:[0x58]` / `_tls_index` / `[slot+4]` / `cmp` / `jg`
shape, guard **`02CB6148`**, static **`02CB6140`**, `_Init_thread_header` and `_Init_thread_footer` on
the cold path. So the log call reaches **two nested lazy singletons**: `02CB6150`, whose initialiser
returns `005CDA30`'s singleton at `02CB6140`.

### Everything else reproduces

| claim | measured |
|---|---|
| `005CDAA0` 239 B / **136** callers | **239 / 136** |
| `0019C5D0` 86 B / **120** callers | **86 / 120** |
| `0016D670` 8 B / **23** callers, `lea rax, [rip] ; ret` → `02EBA3D0` | **8 / 23**, and the body is exactly those two instructions |
| `mov rcx, [rax]` after the 8-byte call, at `005CDB05` and `0019C60C` | both |
| the 16 KB buffer inside a `0x4050` frame | `mov eax, 0x4050` at `005CDAB2`, `mov r8d, 0x4000` at `005CDAFA` |
| `0019C5D0` clamps to `-1` | `0019C615 or ecx, -1` / `0019C618 test eax, eax` / `0019C61A cmovs eax, ecx` |
| the sink is virtual slot 1, channel in `edx`, buffer in `r8` | `005CDB3F mov rax, [rcx]` / `005CDB42 call [rax + 8]`, `edx = edi` (the first argument), `r8 = &buf` |

**Not claimed.** Which class the sink is — §7's second unknown stands, though `005CDA30` and the
singleton at `02CB6140` are now the thread to pull. What the channel id means. What
`02EBA3D0` holds. Whether any caller of `005CDAA0` is itself gated, which is where a verbosity
control would have to live if one exists — **not searched for here, and its absence is not claimed.**
Nothing was executed and nothing was observed live.
*(Since, 2026-09-30, SWE2-CONTRACT: the sink class is answered in §7 (2026-09-18); `02EBA3D0` holds `4` (§3,
2026-09-21); the channel range is measured in §7 with RC-9 left; the caller-side gate is
RC-10, answered the same day: none.)*

- [x] **RC-10.** Whether any of the 136 callers of `005CDAA0` conditions its call on a global or per-thread value that
  acts as a verbosity control. Not searched; its absence is not claimed. Since slot 1 ignores the text, such a gate
  could only save the format cost, not change what is shown. Registered 2026-09-30 (SWE2-CONTRACT); static.
  **ANSWERED 2026-09-30 (static, a negative with controls; SWE2-CONTRACT on OPUS's record
  [`rc10-log-gates-0930`](../../_index/candidates/rc10-log-gates-0930/README.md), `rc10_log_gates.py`, commit 6690d0b9f): no
  caller-side verbosity control.** The census covers all 245 `rel32` sites in the 136 functions (the page's own counts,
  the positive control). 26 sites are never skipped and 195 only by local conditions. 24 sit behind 20 globals, and none
  of those globals gates sites in two functions or is per-thread: 18 are written by their own subsystem's code (for
  example `02EAC278`, an init-once flag written at `0079A16C`), and 2 are never written (`02EA5220` / `02EA5228`, the
  dead input-script facility's switches; the L2 verdict for that facility is in `_index/L2-VERDICTS.md`). There is no 8-byte pointer to `005CDAA0` and no RVA reference but its
  `.pdata` entry, so no indirect call was missed. Tier 1.

## Call chain (SWE2-CONTRACT, 2026-09-30)

```
136 caller functions (Tools/work/graph/edges.tsv), 245 sites: game systems, the resource cache, PhyreEngine
  -> 005CDAA0 (channel, fmt, ...)                                   <- THIS SYSTEM
       16 KB frame (_alloca_probe 00808F10); 0016D670 -> options 4
       __stdio_common_vsnprintf_s (IAT 008C2DE0) into the buffer
       magic-static guard 02CB6158 -> first call builds the sink: 005CDA30 -> 02CB6140 (Phyre::PTTYCallback)
       [02CB6150] -> vtable slot 1 005CDB90 (channel, text)
            channel == 4 and IsDebuggerPresent() -> DebugBreak(); otherwise nothing
0019C5D0 (the vsnprintf wrapper, 120 callers) -> __stdio_common_vsprintf_s (IAT 008C2E10), clamps to -1
```

**Upstream (who causes this):** any engine or middleware code that logs.

**Downstream (what this causes):** a formatted string that nothing reads, and a debugger break on channel 4 when a
debugger is attached.

**Do not confuse with:** the one-time-init lock ([lazy statics](../../24-Compiler-And-CRT-Runtime/Lazy-Static-Initialization/lazy-statics-and-the-one-time-init-lock.md)),
whose `_tls_index` / `_Init_thread_epoch` test §5 misread as a level gate.

## Modding notes (SWE2-CONTRACT, 2026-09-30)

- **Best intervention point:** the sink's vtable slot 1 `005CDB90`. Replacing it (or the sink pointer `02CB6150`
  after its first construction) receives every formatted message with its channel, which is how a mod would see the
  shipped log text.
- **Cost to know:** every call formats into a 16 KB stack buffer whether or not anything reads it.
- **Breaks if:** the sink pointer is replaced before the magic static has run; the first log call would then build and
  install the stock sink over it.
- **Multiplayer / XIIOnline:** diagnostic only; no game state.

## Evidence — claims, evidence and tier (SWE2-CONTRACT, 2026-09-30)

| Claim | Evidence | Tier |
|---|---|---|
| `0016D670` is `__local_stdio_printf_options`; options are `4` from C-init | its two instructions; the one writer `00809C50` (§3) | 1 |
| The log call formats into 16 KB and always emits; there is no level gate | §9's decode: one `ret`, both branches reach `005CDB31`; the TLS directory's `AddressOfIndex` = `02EAED3C` | 1 |
| The import symbols are `__stdio_common_vsnprintf_s` and `__stdio_common_vsprintf_s` | the import directory (§9) | 1 |
| The sink is `Phyre::PTTYCallback`; slot 1 acts only on channel 4 | the vtable `00D360A0` and its RTTI; `005CDB90` read (§7) | 1 |
| Literal channels are 0–3 only | `log_channels.py`, 202 of 245 sites | 1 |
| Every one of the 245 sites passes channel 0–3, none passes 4 (RC-9) | `rc9-log-channels-0930` (OPUS, `e65c88dee`); agrees with FABLE's record `rc789-fable-0930` (commit `8bdf31fcb`) | 1 |
| No caller gates its log call on a verbosity control (RC-10) | `rc10-log-gates-0930` (OPUS); agrees with FABLE's record `rc789-fable-0930` (commit `8bdf31fcb`) | 1 |
| `0019C5D0` clamps a negative return to −1 | `0019C615`–`0019C61A` | 1 |

## Residual placements — 2026-09-14 (SWE2-FRONTIER, residual-placement package)

| function | size | role (call-signature read) |
|---|---:|---|
| `005BF110` | 380 | thin logging thunk on `[r14+0x1C]`: only calls `00808F10` + stack-cookie `00808C40`; callers `005BF0E0`/`005BFEA0` |

*(Pass 22 adjacency, 2026-09-14: `0016D670` is called by **audio** `007A5570` (1 edge) — the log
call is the shared diagnostic sink; an audio body logging through it is the mechanism working as
designed, not an audio-owned logger.)*
