# ASTRA — the original formatter-options initializer and its startup registration

**Result: Method A establishes a registered original initializer that ORs `4`
into FF12's printf-options qword.** The earlier UQ146 native formatter test's
supplied wide-text bit has an original-code basis. This is not a new live sample,
an assertion that the whole options word always equals `4`, or closure of the
returned-stack pointer's lifetime question.

Player version: FF12's startup code requests the text-handling mode used in the
earlier filename test. We can establish that from the executable and its startup
table without opening the game. This does not make the game's temporary account
ID buffer safe under every caller or Windows runtime.

## ASTRA — question, method and boundaries

Consumers: FABLE's UQ146 settings-path semantics and CRT initialization page;
OPUS's platform/input lifetime, formatter-option and startup-state contracts.
The existing UQ146 native evidence and independent review remain separate.

Competing explanations were: the zero-filled image storage is the relevant
formatter mode; an original initializer sets the legacy-wide bit before later
startup consumers; or an original writer exists without a validated registration
route. The discriminator is the exact getter/write plus the pointer-table and
caller route. **Static evidence is sufficient for this claim.** No isolated
execution or fresh live observation was selected. A future question about an
actual process's final word, altered startup or other writers is distinct.

Known starting evidence is [the original returned-stack/native CRT package](../steam-id-stack-consumer/README.md).
Its option0 stable controls returned `C7`; supplied option4 preserved the tested
wide strings. Its pinned SDK excerpt defines mask4 as
`_CRT_INTERNAL_PRINTF_LEGACY_WIDE_SPECIFIERS`. Neither that native test nor the
PE's zero-filled storage observed real FF12 initialization. The previously
retained `00808C40` body is a cookie check, not this options initializer.

Reference: SHA-256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`,
PE32+ image base `00120000`, entry `00808EE4`. `reference.json` retains PE headers,
exact file offsets/bytes/hashes for the selected code/table/import records,
virtual-section evidence and tool identity. `disassembly.txt` is decoded from
those retained bytes. It is not an independent experiment.

## ASTRA — exact original effect and route

| Boundary | Original evidence | What it establishes |
|---|---|---|
| printf getter | `0016D670: lea rax,[rip+02D4CD59]; ret` | Returns `02EBA3D0` |
| original initializer | `00809C54: call 0016D670`; `00809C59: or qword [rax],4` | Sets bit2 while preserving other bits |
| separate scanf state | `00809C5D: call 0018A320`; `00809C62: or qword [rax],2` | Separate getter returns `01F7F5B0`; its mask is not the printf mask |
| C-table callback | `00808D4C..00808D5B` calls `00809C50`, zeroes EAX, returns | Successful normal return supplies zero to the initializer walker |
| registration | `.rdata` qword `008C5690 = 00808D4C` | Exact callback is inside the C table |
| C startup call | `00808DCD/00808DD4` load end `008C56A0` / begin `008C5680`; `00808DDB` calls `00862022` | Thunk resolves through IAT `008C2DB8` to `_initterm_e` |
| later startup | Zero walker return reaches `00808DEE`, then `_initterm` via `00808DFC`; game entry call at `00808E8A` | Registered C initialization precedes the C++ table and game entry on this path |
| UQ146 formatter | `00194F11` calls the same getter; `00194F30` loads `[rax]` into RCX | `00194F33` passes that word to `__stdio_common_vswprintf_s`, IAT `008C2E88` |

The retained five C-table qwords, including boundary nulls, are:

```text
008C5680: 0
008C5688: 00808C90
008C5690: 00808D4C
008C5698: 00809124
008C56A0: 0
```

The PE entry tail-jumps to `00808D78`. Its table path is conditional on successful
CRT preparation and startup state0; reentry/state branches are not silently
treated as another initialization. A nonzero `_initterm_e` return takes the
`0xFF` failure return before the C++ walk/game entry. The ordering interpretation
uses the imported standard `_initterm_e`/`_initterm` walker semantics; this package
does not execute or newly prove the host CRT implementations of those imports.

Both option words lie in `.data`'s virtual tail beyond its file-backed end
`01F7E400`. Their image-zero premise is PE zero fill, **not eight literal bytes
read from that file location**. If the printf initializer receives a zero word,
its local result is4. Its effect for a different word is `old | 4`; this package
does not exhaustively exclude other writers or sample the final live value.

## ASTRA — a startup-state address correction

The existing initialization page's T-1 discussion calls `026A5EED` the
startup-state global. That is the displacement encoded at `00808E01`.
**The absolute four-byte field is `02EAECF8`.** Three independent operands agree:

```text
00808DAA + instruction length6  + 026A5F48 = 02EAECF8  read
00808DC3 + instruction length10 + 026A5F2B = 02EAECF8  write1
00808E01 + instruction length10 + 026A5EED = 02EAECF8  write2
```

The field is written2 after the C++ initializer call returns on the normal path.
That does not make one live read an atomic proof of every earlier side effect.
The original page's broad claim that cookie initialization is the first call
in the process is also outside this evidence: the recorded route begins at the
EXE entry, after any omitted loader/imported-module work.

Affected canonical files, routed under peer ownership:

- [Static initialization and timing](../../../24-Compiler-And-CRT-Runtime/Static-Initialization-And-Lifetime/static-initialization-order-and-injection-timing.md):
  correct the absolute state field and enrich the `00808D4C`/`00809C50` subtree
  with the original option effects and exact C-table registration.
- [Formatted logging](../../../00-Engine-Core-Runtime/Diagnostics-Logging/the-formatted-log-call-and-its-level-gate.md):
  shared getter semantics gain an initialized-bit producer; keep its own
  statement that that research pass did not read the value historically true.
- UQ146's keymap/settings-path prose and corresponding OPUS contracts: replace
  the missing static-producer prerequisite with this qualified route; retain
  omitted Steam/logging state, dangling lifetime and native/live limitations.

## ASTRA — falsification, receipts and cleanup

Run `check.py --mutations` with the repository analysis Python. It re-extracts
the exact reference file, compares the whole retained package and validates
the getter/global, qword masks, callback return, registration, import identities,
conditional startup route, consumer and all three state operands. The known
formatter/getter and `_initterm` neighboring route are positive controls for
the address/import interpretation. It rejects corrupted option mask, callback
registration, getter global and import name even when their local byte hashes
are recomputed. These are **corrupted-evidence controls**, not original-code
execution or a game mutation campaign.

`observation.json` is the normalized result. `development-failures.md` and the
initial checker retain preparation failures, including an incorrect expected
state address rejected before any reference was accepted. `manifest.json` seals
package files and pins the prior SDK/formatter reference dependency.

No game/native child, native API, PC control, breakpoint, save/config/reference
write, or restoration action occurred. Cleanup is therefore not applicable to
a game session; the original EXE is rehashed during replay. Historical live
restoration receipts are not represented as new checks here. Independent review
and canonical consumption remain pending; this is not database completion.
